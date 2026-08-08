/**
 * CLOUD FUNCTIONS — cập nhật mức thạo và hàng đợi ôn tập.
 * Toàn bộ toán học nằm ở src/bkt.js và src/schedule.js (đã có test chạy trên dữ liệu thật).
 * File này chỉ nối dây: đọc — tính — ghi.
 */
import { onDocumentCreated, onDocumentWritten } from 'firebase-functions/v2/firestore';
import { onSchedule } from 'firebase-functions/v2/scheduler';
import { onCall, HttpsError } from 'firebase-functions/v2/https';
import { setGlobalOptions } from 'firebase-functions/v2';
import { defineSecret } from 'firebase-functions/params';
import { initializeApp } from 'firebase-admin/app';
import { getFirestore, FieldValue } from 'firebase-admin/firestore';
import { getAuth } from 'firebase-admin/auth';
import { applyAttempt } from './src/bkt.js';
import { buildReviewCards } from './src/schedule.js';
import { buildParentReport } from './src/report.js';
import { buildTeacherBoard } from './src/teacherboard.js';
import { makeCode, canSend, nextRecord, verify, otpEmail } from './src/otp.js';
import { normalizeEmail, buildUserDoc } from './src/user.js';

setGlobalOptions({ region: 'asia-southeast1', maxInstances: 10 });
initializeApp();
const db = getFirestore();

/** Mỗi lượt trả lời → cập nhật mức thạo của đơn vị kỹ năng tương ứng */
export const onAttempt = onDocumentCreated('attempts/{attemptId}', async (event) => {
  const a = event.data?.data();
  if (!a?.learnerId || !a?.bktUnit) return;
  if (a.phase !== 'practice' && a.phase !== 'assess') return;   // chỉ tính lượt làm bài thật

  const ref = db.doc(`mastery/${a.learnerId}/units/${encodeURIComponent(a.bktUnit)}`);
  await db.runTransaction(async (tx) => {
    const snap = await tx.get(ref);
    const next = applyAttempt(snap.exists ? snap.data() : undefined, a, () => Date.now());
    tx.set(ref, { ...next, unit: a.bktUnit, learnerId: a.learnerId }, { merge: true });
  });
});

/** Học xong một micro → sinh thẻ ôn theo lịch +1 / +3 / +7 ngày của chính bài đó */
export const onMicroDone = onDocumentWritten('progress/{learnerId}/micros/{microDoc}', async (event) => {
  const after = event.data?.after?.data();
  const before = event.data?.before?.data();
  if (!after?.pass || before?.pass) return;                     // chỉ khi VỪA đạt lần đầu

  const { learnerId } = event.params;
  const microId = after.microId;
  const lessonSnap = await db.doc(`contentIndex/${microId.replace(/[:.]/g, '_')}`).get();
  const schedule = lessonSnap.exists ? lessonSnap.data().schedule : null;

  const cards = buildReviewCards({
    learnerId, microId,
    lesson: { spacedReview: { schedule: schedule || ['+1 ngày: flashcard', '+3 ngày: câu luyện', '+7 ngày: câu thử thách'] } },
    at: Date.now(),
  });

  const batch = db.batch();
  for (const c of cards) batch.set(db.doc(`reviewQueue/${learnerId}/cards/${c.id}`), c, { merge: true });
  batch.set(db.doc(`users/${learnerId}`), { lastStudiedAt: FieldValue.serverTimestamp() }, { merge: true });
  await batch.commit();
});

/**
 * SỔ HỌC — tổng hợp 21h mỗi đêm thành MỘT document cho mỗi tài khoản.
 * Mở app đọc 1 lần, thay vì quét hàng nghìn attempts (rẻ và nhanh hơn nhiều).
 */
/**
 * Dựng SỔ HỌC của MỘT tài khoản từ dữ liệu hiện tại, ghi vào report/{uid}.
 * Tách riêng vì có hai nơi gọi: lịch chạy đêm, và nút "Cập nhật ngay" của bố mẹ.
 *
 * Lọc theo `serverTs` chứ không theo `ts`. `ts` là giờ máy của con — máy tính bảng
 * đặt sai ngày là bản ghi rơi ra ngoài cửa sổ 7 ngày, sổ trống mà không ai hiểu vì
 * sao. Quy luôn `ts` về giờ máy chủ trước khi tính, để "số phút con học" cũng không
 * bị đồng hồ lệch làm hỏng. (Chỉ mục learnerId + serverTs đã có sẵn.)
 */
async function dungSoHoc(learnerId, index, soNgay = 7) {
  const since = new Date(Date.now() - soNgay * 86400000);
  const [attSnap, progSnap, mastSnap] = await Promise.all([
    db.collection('attempts').where('learnerId', '==', learnerId).where('serverTs', '>=', since).get(),
    db.collection(`progress/${learnerId}/micros`).get(),
    db.collection(`mastery/${learnerId}/units`).get(),
  ]);
  const attempts = attSnap.docs.map((d) => {
    const a = d.data();
    const sv = a.serverTs?.toMillis ? a.serverTs.toMillis() : a.serverTs;
    return { ...a, serverTs: sv, ts: sv ?? a.ts };
  });
  const progress = {}; progSnap.forEach((d) => { progress[d.id] = d.data(); });
  const mastery = {}; mastSnap.forEach((d) => { mastery[d.id] = d.data(); });

  const report = buildParentReport({ learnerId, attempts, progress, mastery, index, days: soNgay });
  await db.doc(`report/${learnerId}`).set(report, { merge: true });
  return report;
}

export const nightlyReport = onSchedule(
  { schedule: '0 21 * * *', timeZone: 'Asia/Ho_Chi_Minh', timeoutSeconds: 540, memory: '512MiB' },
  async () => {
    const index = await loadContentIndex();
    // Quét theo LÔ, không đọc hết một lần: một trường vài nghìn học sinh thì
    // câu .get() cũ vừa ngốn bộ nhớ vừa chạm trần 540 giây.
    let done = 0;
    for await (const L of eachDoc(db.collection('users').where('role', '==', 'learner'))) {
      await dungSoHoc(L.id, index);
      done++;
    }
    console.log(`sổ học: đã dựng cho ${done} tài khoản`);
  },
);

/**
 * "Cập nhật ngay" cho SỔ HỌC.
 *
 * Sổ cũng chỉ dựng lúc 21:00 mỗi đêm, nên con vừa học xong mà bố mẹ mở ra thì thấy
 * trống trơn — tưởng công học của con không được lưu. Bố mẹ chỉ dựng lại sổ CỦA
 * MÌNH; thầy cô và quản trị dựng được cho bất kỳ em nào.
 */
export const refreshMyReport = onCall(
  { region: 'asia-southeast1', timeoutSeconds: 300, memory: '512MiB' },
  async (req) => {
    const uid = req.auth?.uid;
    if (!uid) throw new HttpsError('unauthenticated', 'Cần đăng nhập.');
    const vai = req.auth?.token?.role;
    const target = String(req.data?.uid || uid);
    if (target !== uid && vai !== 'teacher' && vai !== 'admin') {
      throw new HttpsError('permission-denied', 'Chỉ xem được sổ học của mình.');
    }
    const index = await loadContentIndex();
    const report = await dungSoHoc(target, index, Number(req.data?.soNgay) || 7);
    return { ok: true, uid: target, generatedAt: report.generatedAt ?? Date.now() };
  },
);

/**
 * BẢNG GIÁO VIÊN — 21h15 mỗi đêm, MỘT document cho toàn hệ thống.
 * Cô mở app đọc đúng một lần, thay vì quét hàng chục nghìn dòng nhật ký.
 */
/**
 * Dựng bảng giáo viên từ dữ liệu HIỆN TẠI và ghi vào teacherBoard/global.
 * Tách riêng vì có HAI nơi gọi: lịch chạy đêm, và nút "Cập nhật ngay" của cô giáo.
 */
async function dungBangGiaoVien(soNgay = 7) {
  const since = Date.now() - soNgay * 86400000;
  const index = await loadContentIndex();

  const roster = [];
  for await (const U of eachDoc(db.collection('users').where('role', '==', 'learner'))) {
    const d = U.data();
    roster.push({ uid: U.id, displayName: d.displayName || '', email: d.email || '' });
  }

  const attSnap = await db.collection('attempts').where('serverTs', '>=', new Date(since)).get();
  const attempts = attSnap.docs.map((d) => {
    const a = d.data();
    // Firestore trả Timestamp; teacherboard.js làm việc với mili-giây
    return { ...a, serverTs: a.serverTs?.toMillis ? a.serverTs.toMillis() : a.serverTs };
  });

  const progress = {};
  for (const r of roster) {
    const s = await db.collection(`progress/${r.uid}/micros`).get();
    const m = {}; s.forEach((d) => { m[d.data().microId || d.id] = d.data(); });
    progress[r.uid] = m;
  }

  const board = buildTeacherBoard({ roster, attempts, progress, index });
  await db.doc('teacherBoard/global').set(board, { merge: true });
  return board;
}

export const nightlyTeacherBoard = onSchedule(
  { schedule: '15 21 * * *', timeZone: 'Asia/Ho_Chi_Minh', timeoutSeconds: 540, memory: '512MiB' },
  async () => {
    const board = await dungBangGiaoVien();
    console.log(`bảng giáo viên: ${board.learners} học sinh · ${board.answered} lượt trả lời`);
  },
);

/**
 * "Cập nhật ngay" — cô giáo bấm là dựng lại bảng tức thì.
 *
 * Vì sao cần: bảng chỉ dựng lúc 21:15 mỗi đêm, nên con học sáng nay thì mãi tối cô
 * mới thấy — mà cô cần biết NGAY để còn kèm con trong buổi học. Bảng dựng lần đầu
 * lúc 07:00 còn sớm hơn cả lúc tài khoản học sinh được tạo, nên cô mở ra thấy toàn
 * số 0 và tưởng hệ thống hỏng.
 */
export const refreshTeacherBoard = onCall(
  { region: 'asia-southeast1', timeoutSeconds: 300, memory: '512MiB' },
  async (req) => {
    const vai = req.auth?.token?.role;
    if (vai !== 'teacher' && vai !== 'admin') {
      throw new HttpsError('permission-denied', 'Chỉ giáo viên và quản trị dựng lại bảng được.');
    }
    const board = await dungBangGiaoVien(Number(req.data?.soNgay) || 7);
    return { ok: true, learners: board.learners, answered: board.answered,
             generatedAt: board.generatedAt };
  },
);

/* ─────────── Tiện ích chung ─────────── */
async function loadContentIndex() {
  const snap = await db.collection('contentIndex').get();
  const index = {};
  snap.forEach((d) => { index[d.id] = d.data(); });
  return index;
}

/** Duyệt một collection theo lô 200 doc — không giữ cả bảng trong bộ nhớ */
async function* eachDoc(query, pageSize = 200) {
  let cursor = null;
  for (;;) {
    let q = query.orderBy('__name__').limit(pageSize);
    if (cursor) q = q.startAfter(cursor);
    const snap = await q.get();
    if (snap.empty) return;
    for (const d of snap.docs) yield d;
    if (snap.size < pageSize) return;
    cursor = snap.docs[snap.docs.length - 1];
  }
}

/* ══════════════════════════════════════════════════════════════════════════════
   ĐĂNG NHẬP BẰNG MÃ OTP GỬI QUA EMAIL
   Không có màn đăng ký: nhập email → nhận mã → vào. Chưa có hồ sơ thì lập luôn.
   Admin KHÔNG đi đường này (xem ghi chú cuối file).
   ══════════════════════════════════════════════════════════════════════════════ */

/** Bí mật máy chủ để băm mã. Đặt bằng: firebase functions:secrets:set OTP_PEPPER */
const OTP_PEPPER = defineSecret('OTP_PEPPER');

/**
 * Tài khoản gửi mail — để RỜI hai mảnh, không gộp thành một URL.
 *
 * Vì sao: tên đăng nhập là địa chỉ email, mà email có dấu @. Nhét vào URL kiểu
 * smtps://congvt@mobiluck.vn:matkhau@smtp.gmail.com:465 thì bộ đọc URL cắt nhầm chỗ,
 * gửi mail hỏng mà không báo lỗi rõ ràng. Muốn đúng phải nhớ đổi @ thành %40 — một
 * cái bẫy không đáng có. Để rời thì dán sao dùng vậy.
 */
const SMTP_USER = defineSecret('SMTP_USER');   // vd: bome@gmail.com
const SMTP_PASS = defineSecret('SMTP_PASS');   // mật khẩu ỨNG DỤNG 16 ký tự, không phải mật khẩu thường
const SMTP_HOST = defineSecret('SMTP_HOST');   // để trống thì mặc định smtp.gmail.com

/** Trả lời GIỐNG HỆT NHAU dù email có trong hệ thống hay không — không để lộ ai đang dùng app */
const SAME_ANSWER = { ok: true, message: 'Nếu email hợp lệ, mã đã được gửi. Kiểm tra hộp thư nhé.' };

export const requestOtp = onCall(
  { secrets: [OTP_PEPPER, SMTP_USER, SMTP_PASS, SMTP_HOST], region: 'asia-southeast1' },
  async (req) => {
    const email = normalizeEmail(req.data?.email);
    if (!email) throw new HttpsError('invalid-argument', 'Email không hợp lệ.');

    const ref = db.doc(`otpCodes/${encodeURIComponent(email)}`);
    const snap = await ref.get();
    const gate = canSend(snap.exists ? snap.data() : null, Date.now());
    if (!gate.ok) {
      const giay = Math.ceil(gate.retryAfterMs / 1000);
      throw new HttpsError('resource-exhausted',
        gate.reason === 'quá nhanh'
          ? `Bạn vừa xin mã rồi. Thử lại sau ${giay} giây nhé.`
          : `Xin mã quá nhiều lần. Thử lại sau ${Math.ceil(giay / 60)} phút nhé.`);
    }

    const code = makeCode();
    await ref.set(nextRecord(snap.exists ? snap.data() : null,
      { email, code, pepper: OTP_PEPPER.value(), now: Date.now() }));

    await sendMail(email, otpEmail(code));
    return SAME_ANSWER;
  },
);

export const verifyOtp = onCall(
  { secrets: [OTP_PEPPER], region: 'asia-southeast1' },
  async (req) => {
    const email = normalizeEmail(req.data?.email);
    const code = String(req.data?.code ?? '').trim();
    if (!email || !code) throw new HttpsError('invalid-argument', 'Thiếu email hoặc mã.');

    const ref = db.doc(`otpCodes/${encodeURIComponent(email)}`);
    const snap = await ref.get();
    const res = verify(snap.exists ? snap.data() : null,
      { email, code, pepper: OTP_PEPPER.value(), now: Date.now() });

    if (!res.ok) {
      // ghi lại số lần sai TRƯỚC khi báo lỗi, nếu không kẻ dò mã cứ thử vô hạn
      if (res.burn) await ref.delete().catch(() => {});
      else if (res.wrong != null) await ref.update({ wrong: res.wrong }).catch(() => {});
      throw new HttpsError('permission-denied', hoaChu(res.reason));
    }
    await ref.delete().catch(() => {});      // mã dùng xong là huỷ

    // Tìm hoặc lập tài khoản. Vai trò do MÁY CHỦ đặt — mặc định là học sinh.
    const auth = getAuth();
    let user = await auth.getUserByEmail(email).catch(() => null);
    if (!user) user = await auth.createUser({ email, emailVerified: true });

    const uref = db.doc(`users/${user.uid}`);
    const usnap = await uref.get();
    let isNew = false;
    if (!usnap.exists) {
      await uref.set(buildUserDoc({ uid: user.uid, email }));
      isNew = true;
    }
    const role = isNew ? 'learner' : (usnap.data().role || 'learner');

    // Nhét vai trò vào token để luật bảo mật khỏi phải đọc Firestore mỗi lần kiểm quyền
    await auth.setCustomUserClaims(user.uid, { role });
    const token = await auth.createCustomToken(user.uid, { role });
    return { token, role, isNew };
  },
);

const hoaChu = (s) => String(s).charAt(0).toUpperCase() + String(s).slice(1) + '.';

/**
 * Gửi mail qua SMTP.
 * Chưa đặt SMTP_USER/SMTP_PASS thì KHÔNG gửi mà in mã ra log — tiện chạy thử tại máy,
 * nhưng chạy thật mà quên đặt là không ai đăng nhập được. Log có ghi rõ cảnh báo.
 */
async function sendMail(to, { subject, text }) {
  const user = SMTP_USER.value();
  const pass = SMTP_PASS.value();
  if (!user || !pass) {
    console.warn(`[OTP] CHƯA ĐẶT SMTP_USER/SMTP_PASS — không gửi được mail. Mã cho ${to}: ${subject}`);
    return;
  }
  const nodemailer = (await import('nodemailer')).default;
  const transport = nodemailer.createTransport({
    host: SMTP_HOST.value() || 'smtp.gmail.com',
    port: 465,
    secure: true,
    // Mật khẩu ứng dụng Google hiển thị theo nhóm 4 ký tự có dấu cách — người ta hay
    // dán cả dấu cách vào. Bỏ khoảng trắng ở đây để khỏi phải dặn dò.
    auth: { user, pass: pass.replace(/\s+/g, '') },
  });
  await transport.sendMail({
    from: `Kỹ Sư Nhí <${user}>`,
    to, subject, text,
  });
}

/* ADMIN không dùng OTP: tạo thẳng trong Firebase Console (Authentication → Add user,
   email + mật khẩu), rồi đặt users/{uid}.role = 'admin' và custom claim role=admin.
   Xem docs/DEPLOY.md bước 7c. */
