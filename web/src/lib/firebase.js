/**
 * Lớp mỏng bọc Firebase SDK.
 * Toàn bộ logic dữ liệu nằm ở sync.js (đã có test) — file này chỉ nối dây.
 *
 * QUAN TRỌNG: bật persistentLocalCache — trẻ học trên máy tính bảng, mạng chập chờn.
 * Thiếu dòng này là mất bài giữa chừng, và trẻ mất bài một lần là nản luôn.
 */
import { initializeApp } from 'firebase/app';
import {
  initializeFirestore, persistentLocalCache, persistentMultipleTabManager,
  doc, getDoc, setDoc, writeBatch, collection, query, where, orderBy, limit, getDocs,
  serverTimestamp,
} from 'firebase/firestore';
import {
  getAuth, onAuthStateChanged, signInWithCustomToken, signInWithEmailAndPassword,
  signOut, getIdTokenResult,
} from 'firebase/auth';
import { getFunctions, httpsCallable } from 'firebase/functions';
import {
  COLLECTIONS, buildAttempts, buildProgressDoc, enqueue, flushQueue, newSessionId,
  isCloudLearner, normalizeEmail, maHocBa,
} from './sync.js';
import { napBanDoDang, dangCuaBai } from './content.js';

/** Điền từ Firebase Console → Project settings. Đặt trong .env.local, không commit. */
const cfg = {
  apiKey: import.meta.env?.VITE_FB_API_KEY,
  authDomain: import.meta.env?.VITE_FB_AUTH_DOMAIN,
  projectId: import.meta.env?.VITE_FB_PROJECT_ID,
  storageBucket: import.meta.env?.VITE_FB_STORAGE_BUCKET,
  messagingSenderId: import.meta.env?.VITE_FB_SENDER_ID,
  appId: import.meta.env?.VITE_FB_APP_ID,
};

export const hasFirebase = !!cfg.projectId;

let app = null, db = null, auth = null, fns = null;
if (hasFirebase) {
  app = initializeApp(cfg);
  db = initializeFirestore(app, {
    localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }),
  });
  auth = getAuth(app);
  fns = getFunctions(app, 'asia-southeast1');
}
export { db, auth };

/* ─────────── Đăng nhập bằng mã OTP gửi qua email ─────────── */
/**
 * Không có màn đăng ký: nhập email → nhận mã → vào. Chưa có hồ sơ thì máy chủ lập luôn.
 * Vai trò do máy chủ đặt và nằm trong token — app chỉ đọc lại để biết hiện màn nào.
 */
export const watchAuth = (cb) => (auth ? onAuthStateChanged(auth, cb) : (cb(null), () => {}));
export const logout = () => signOut(auth);

/** Bước 1 — xin mã. Trả lời giống nhau dù email có trong hệ thống hay không. */
export async function requestOtp(email) {
  const mail = normalizeEmail(email);
  if (!mail) throw new Error('Email chưa đúng. Bạn kiểm tra lại giúp nhé.');
  if (!fns) throw new Error('Chưa cấu hình máy chủ.');
  const { data } = await httpsCallable(fns, 'requestOtp')({ email: mail });
  return data;
}

/** Bước 2 — nhập mã. Đúng thì đổi lấy token và vào thẳng. */
export async function verifyOtp(email, code) {
  const mail = normalizeEmail(email);
  if (!mail) throw new Error('Email chưa đúng.');
  if (!fns) throw new Error('Chưa cấu hình máy chủ.');
  const { data } = await httpsCallable(fns, 'verifyOtp')({ email: mail, code });
  await signInWithCustomToken(auth, data.token);
  return data;                       // { token, role, isNew }
}

/** Admin KHÔNG dùng OTP — vào bằng email và mật khẩu tạo sẵn trong Console */
export const loginAdmin = (email, pw) => signInWithEmailAndPassword(auth, email, pw);

/** Vai trò lấy từ token, không lấy từ Firestore (Firestore thì người dùng ghi được) */
export async function myRole(user) {
  if (!user) return null;
  const res = await getIdTokenResult(user, true);
  return res.claims.role || 'learner';
}

/* ─────────── Đọc hồ sơ và sổ học ─────────── */
export async function myProfile(uid) {
  if (!db) return null;
  const snap = await getDoc(doc(db, COLLECTIONS.users, uid));
  return snap.exists() ? snap.data() : null;
}

export async function saveProfile(uid, { displayName, grade }) {
  if (!db) return;
  await setDoc(doc(db, COLLECTIONS.users, uid),
    { displayName, grade, profileComplete: true }, { merge: true });
}

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

/* ═══════════ BẢNG XẾP HẠNG ═══════════ */

/** Bảng xếp hạng — MỘT tài liệu, bé nào đăng nhập cũng đọc được. */
export async function bangXepHang() {
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

/**
 * Biệt danh và bạn đang đuổi — hai thứ con tự đặt, nằm trong hồ sơ của chính con.
 *
 * Luật Firestore cho chính chủ sửa hồ sơ miễn là KHÔNG đụng `role`, `uid`, `email`,
 * nên hai trường này ghi thẳng được, không cần Cloud Function.
 */
export async function luuBietDanh(uid, bietDanh) {
  if (!db || !isCloudLearner(uid)) return false;
  await setDoc(doc(db, COLLECTIONS.users, uid),
    { bietDanh: String(bietDanh || '').trim().slice(0, 24) }, { merge: true });
  return true;
}

export async function luuDuoiKip(uid, maBan) {
  if (!db || !isCloudLearner(uid)) return false;
  await setDoc(doc(db, COLLECTIONS.users, uid), { duoiKip: maBan || null }, { merge: true });
  return true;
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
  return { micros, chapters: {}, chuDe: {}, dau: {}, ...hb, micros };
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
export async function submitSession({ learnerId, sessionId, microId, bktUnit, events, tomTat, grade }) {
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
      { ...buildProgressDoc({ microId, grade, events: tomTat || events, sessionId }), serverTs: serverTimestamp() },
      { merge: true },
    );
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
