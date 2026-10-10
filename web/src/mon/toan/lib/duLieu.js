/**
 * DỮ LIỆU HỌC CỦA MÔN TOÁN — nhật ký, tiến độ, học bạ, sổ bố mẹ, bảng cô giáo.
 *
 * Mọi collection ở đây là CỦA RIÊNG TOÁN. Môn khác có bộ collection riêng, để một lỗi
 * ghi bên môn này không nằm lẫn trong sổ của môn kia — xem `docs/tach_hai_mon.md`.
 *
 * Chỉ dùng chung với môn khác đúng hai thứ: thể hiện Firebase (`chung/lib/nenTang.js`)
 * và tài khoản người dùng (`chung/lib/taiKhoan.js`).
 */
import {
  doc, getDoc, setDoc, writeBatch, collection, query, where, orderBy, limit, getDocs,
  serverTimestamp, increment,
} from 'firebase/firestore';
import { httpsCallable } from 'firebase/functions';
import { db, fns, hasFirebase } from '../../../chung/lib/nenTang.js';
import {
  COLLECTIONS, buildAttempts, buildProgressDoc, enqueue, flushQueue, newSessionId,
  isCloudLearner, maHocBa,
} from './sync.js';
import { napBanDoDang, dangCuaBai } from './noiDung.js';
import { maNgay } from './dongHo.js';

/**
 * Dựng lại SỔ HỌC ngay, không chờ 21:00.
 * Con vừa học xong mà bố mẹ mở sổ thấy trống thì tưởng công học không được lưu.
 */
export async function refreshMyReport(uid, soNgay = 7) {
  if (!fns) throw new Error('chưa cấu hình Firebase');
  const { data } = await httpsCallable(fns, 'refreshMyReport')({ uid, soNgay });
  return data;
}

/** Sổ học của một tài khoản — chính chủ và giáo viên cùng đọc được */
export async function myReport(uid) {
  if (!db) return null;
  const snap = await getDoc(doc(db, COLLECTIONS.report, uid));
  return snap.exists() ? snap.data() : null;
}

/**
 * Dựng lại bảng NGAY, không chờ lịch chạy đêm.
 * Bảng vốn chỉ tổng hợp lúc 21:15, nên con học sáng nay thì tối cô mới thấy —
 * mà cô cần biết trong buổi học để còn kèm con.
 */
export async function refreshTeacherBoard(soNgay = 7) {
  if (!fns) throw new Error('chưa cấu hình Firebase');
  const { data } = await httpsCallable(fns, 'refreshTeacherBoard')({ soNgay });
  return data;
}


/** Bảng toàn hệ thống — chỉ giáo viên và admin đọc được */
export async function teacherBoard() {
  if (!db) return null;
  const snap = await getDoc(doc(db, `${COLLECTIONS.teacherBoard}/global`));
  return snap.exists() ? snap.data() : null;
}

/* ═══════════ HỌC BẠ ĐẦY ĐỦ — đọc và ghi ═══════════
 *
 * Sổ tiến độ có bốn phần, mà trước nay chỉ MỘT phần lên được mạng:
 *   micros   → progress/{uid}/micros     ✔ đã có
 *   chapters → hocBa/{uid}/muc  (loai chuong)  ✘ chỉ nằm ở máy
 *   chuDe    → hocBa/{uid}/muc  (loai chuDe)   ✘ chỉ nằm ở máy
 *   dau      → hocBa/{uid}/muc  (loai dau)     ✘ chỉ nằm ở máy
 *
 * Ba phần thiếu là ba phần bố mẹ hỏi nhiều nhất: con qua kỳ sát hạch nào, vững chủ
 * đề nào, đấu tới vòng mấy. Đổi máy là mất sạch, và cô giáo thì không bao giờ thấy.
 */

/** Ghi một mục học bạ. Mất mạng thì bỏ qua — sổ ở máy vẫn đúng, lần sau ghi lại. */
export async function luuMucHocBa(uid, loai, khoa, du) {
  if (!db || !isCloudLearner(uid)) return false;
  await setDoc(doc(db, COLLECTIONS.hocBa(uid), maHocBa(loai, khoa)),
    { ...du, loai, khoa: String(khoa), serverTs: serverTimestamp() }, { merge: true });
  return true;
}

/**
 * Đọc TOÀN BỘ học bạ của một tài khoản, trả về đúng hình dạng của sổ tiến độ tại
 * máy — để `gopTienDo` gộp thẳng vào, không phải dịch qua lại ở nơi gọi.
 */
export async function docHocBa(uid) {
  if (!db || !isCloudLearner(uid)) return {};
  const snap = await getDocs(collection(db, COLLECTIONS.hocBa(uid)));
  const chapters = {}, chuDe = {}, dau = {};
  snap.forEach((d) => {
    const v = d.data();
    if (v.loai === 'chuong') chapters[v.khoa] = v.giaTri || {};
    else if (v.loai === 'chuDe') chuDe[v.khoa] = v.giaTri || {};
    else if (v.loai === 'dau') dau[v.khoa] = v.giaTri || {};
  });
  return { chapters, chuDe, dau };
}

/** Tiến độ từng bài trên máy chủ — khoá tài liệu là mã bài đã thay ':' '.' bằng '_' */
export async function docTienDoMicro(uid) {
  if (!db || !isCloudLearner(uid)) return {};
  const snap = await getDocs(collection(db, COLLECTIONS.progress(uid)));
  const micros = {};
  snap.forEach((d) => {
    const v = d.data();
    if (!v.microId) return;
    micros[v.microId] = {
      done: true, pass: !!v.pass, mustPassOK: !!v.mustPassOK,
      best: v.score || 0, total: v.total || 0,
      attempts: v.attempts || 1,
      at: typeof v.at === 'number' ? new Date(v.at).toISOString() : v.at || null,
    };
  });
  return micros;
}

/** Sổ tiến độ đầy đủ của một tài khoản — dùng cho cả lúc đăng nhập lẫn bảng cô giáo. */
export async function tienDoTuMay(uid) {
  const [micros, hb] = await Promise.all([
    docTienDoMicro(uid).catch(() => ({})),
    docHocBa(uid).catch(() => ({})),
  ]);
  /* ⚠ `micros` ĐỨNG SAU `...hb`, và chỉ đứng ở đó. Bản cũ khai nó HAI lần (cả
     trước lẫn sau phép trải) — khoá trùng trong một object literal: bản sau lặng lẽ
     đè bản trước, nên bản trước là mã chết. Thứ tự này cố ý: sổ tiến độ micro là
     nguồn riêng, không được để học bạ đè lên. ESLint `no-dupe-keys` tìm ra. */
  return { chapters: {}, chuDe: {}, dau: {}, ...hb, micros };
}

/** Cô lần vào nhật ký từng câu của MỘT em */
export async function learnerAttempts(uid, n = 200) {
  if (!db) return [];
  const q = query(collection(db, COLLECTIONS.attempts),
    where('learnerId', '==', uid), orderBy('serverTs', 'desc'), limit(n));
  return (await getDocs(q)).docs.map((d) => d.data());
}

/* ─────────── Ghi dữ liệu học ─────────── */
async function writeRecords(records) {
  if (!db) throw new Error('chưa cấu hình Firebase');
  const batch = writeBatch(db);
  for (const r of records) {
    // Đóng dấu máy chủ ĐÚNG LÚC GỬI. Bản ghi nằm chờ trong hàng đợi mấy ngày vì mất mạng
    // thì ts (giờ máy con) vẫn giữ nguyên lúc con làm bài — hai mốc phục vụ hai việc khác nhau.
    batch.set(doc(db, COLLECTIONS.attempts, r.id), { ...r, serverTs: serverTimestamp() }, { merge: true });
  }
  await batch.commit();
}

/**
 * ĐẨY DẦN trong lúc con đang học — gọi sau MỖI lượt trả lời.
 *
 * Trước đây chỉ gửi ở màn KẾT BÀI. Con làm 20/23 bước rồi mẹ gọi ăn cơm, hết pin,
 * hay bấm nhầm nút quay lại thì mất trắng — trung bình 7 câu mỗi bài, tối đa 1141
 * câu trên toàn bộ chương trình. Mà cô giáo cũng phải đợi con học xong mới thấy gì.
 *
 * Dựng lại bản ghi từ TOÀN BỘ nhật ký của phiên chứ không chỉ lượt mới: mã bản ghi
 * nhúng số thứ tự nên dựng lại cho ra đúng mã cũ, hàng đợi ghi đè theo mã — chạy
 * bao nhiêu lần cũng không sinh dòng trùng.
 */
export async function pushAttempts({ learnerId, sessionId, microId, bktUnit, events }) {
  if (!events?.length) return { sent: 0, left: 0 };
  await napBanDoDang().catch(() => {});
  const recs = buildAttempts({
    learnerId, sessionId, microId, bktUnit, events, dangBai: dangCuaBai(microId),
  });
  enqueue(recs);
  if (!isCloudLearner(learnerId) || !hasFirebase) return { sent: 0, left: recs.length, offlineOnly: true };
  return flushQueue(writeRecords);
}

/**
 * Kết thúc một lượt học micro: xếp hàng đợi trước (an toàn khi mất mạng), rồi thử gửi.
 * Không có Firebase (chế độ chỉ-học-máy) thì chỉ xếp hàng, không lỗi.
 */
/**
 * SỔ GIỜ THEO NGÀY — `hocBa/{uid}/muc/gio_2026_08_17`.
 *
 * Vì sao phải có, khi `progress/{uid}/micros` đã ghi giây từng bài: tài liệu bài bị
 * GHI ĐÈ mỗi lần con học lại, nên cộng tất cả lại không ra "tuần này con học bao
 * lâu" mà ra "tổng của các lượt gần nhất" — một con số không có nghĩa gì. Sổ theo
 * ngày cộng dồn bằng `increment`, nên học lại bao nhiêu lượt cũng đúng.
 *
 * Cộng bằng `increment` chứ không đọc-rồi-ghi: hai máy tính bảng cùng mở một tài
 * khoản (anh em dùng chung) thì đọc-rồi-ghi làm mất lượt của máy kia trong im lặng.
 *
 * Nằm trong `hocBa` cho khớp ba loại đã có (`chuong` · `chuDe` · `dau`), và cố ý
 * KHÔNG nằm trong `progress/{uid}/micros`: hàm nền `onMicroDone` chạy trên mọi tài
 * liệu thư mục ấy và đọc thẳng `after.microId` — thả một bản ghi khác hình dạng vào
 * là hàm đêm ném lỗi, còn `microsPassed` thì đếm phồng lên.
 */
async function congGioTrongNgay(uid, gio, microId) {
  if (!db || !gio || !gio.giay) return;
  const ngay = maNgay();
  await setDoc(
    doc(db, COLLECTIONS.hocBa(uid), maHocBa('gio', ngay)),
    {
      loai: 'gio', ngay,
      giay: increment(gio.giay),
      giayXem: increment(gio.giayXem),
      giayLam: increment(gio.giayLam),
      soLuot: increment(1),
      baiCuoi: microId,
      at: Date.now(),
      serverTs: serverTimestamp(),
    },
    { merge: true },
  );
}

export async function submitSession({ learnerId, sessionId, microId, bktUnit, events, tomTat, grade, gio = null }) {
  // serverTs để null trong hàng đợi: dấu máy chủ chỉ đóng được lúc GỬI THẬT, không
  // đóng trước rồi cất vào localStorage được.
  await napBanDoDang().catch(() => {});
  const recs = buildAttempts({
    learnerId, sessionId, microId, bktUnit, events, dangBai: dangCuaBai(microId),
  });
  enqueue(recs);
  if (!isCloudLearner(learnerId)) return { sent: 0, left: recs.length, offlineOnly: true };
  if (db && learnerId) {
    await setDoc(
      doc(db, COLLECTIONS.progress(learnerId), microId.replace(/[:.]/g, '_')),
      /* Tiến độ tính trên sổ TÓM TẮT (mỗi câu một dòng). Đưa sổ thô vào đây thì
         "làm đúng ngay lần đầu" sẽ đếm cả những lượt sai giữa chừng — sai nghĩa. */
      { ...buildProgressDoc({ microId, grade, events: tomTat || events, sessionId, gio }),
        serverTs: serverTimestamp() },
      { merge: true },
    );
    /* Sổ giờ theo ngày hỏng thì ĐỪNG kéo cả lượt nộp bài hỏng theo: mất một con số
       thống kê là chuyện nhỏ, mất kết quả học của con mới là chuyện lớn. */
    await congGioTrongNgay(learnerId, gio, microId).catch(() => {});
  }
  return hasFirebase ? flushQueue(writeRecords) : { sent: 0, left: recs.length };
}

/** Gọi khi app khởi động và mỗi lần online trở lại */
export const syncPending = () => (hasFirebase ? flushQueue(writeRecords) : Promise.resolve({ sent: 0, left: 0 }));

if (typeof window !== 'undefined') window.addEventListener('online', () => syncPending());

/* ─────────── Đọc lại lịch sử ─────────── */
export async function recentAttempts(learnerId, n = 50) {
  if (!db) return [];
  const q = query(collection(db, COLLECTIONS.attempts),
    where('learnerId', '==', learnerId), orderBy('ts', 'desc'), limit(n));
  return (await getDocs(q)).docs.map((d) => d.data());
}

/** Bẫy hay sập nhất — câu hỏi mà sổ phụ huynh và giáo viên cần nhất */
export async function trapMisses(learnerId, n = 200) {
  if (!db) return [];
  const q = query(collection(db, COLLECTIONS.attempts),
    where('learnerId', '==', learnerId), where('mustPass', '==', true), where('correct', '==', false),
    limit(n));
  return (await getDocs(q)).docs.map((d) => d.data());
}

export { newSessionId, isCloudLearner };

/**
 * BẢNG XẾP HẠNG CỦA MÔN TOÁN — tài liệu riêng của môn.
 * Mỗi môn có bảng riêng, màn chung ghép lại thành các tab. Nhờ vậy hàm nền của môn
 * này dựng lại bảng cũng không đụng tới con số của môn kia.
 */
export async function bangXepHangToan() {
  if (!db) return null;
  const snap = await getDoc(doc(db, 'bangXepHang/global'));
  return snap.exists() ? snap.data() : null;
}

/** Dựng lại bảng ngay. Máy chủ tự chặn dội nếu vừa dựng xong dưới hai phút. */
export async function lamMoiBangXepHang() {
  if (!fns) throw new Error('chưa cấu hình Firebase');
  const { data } = await httpsCallable(fns, 'refreshBangXepHang')({});
  return data;
}

