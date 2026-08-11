/**
 * TÀI KHOẢN — đăng nhập, vai trò, hồ sơ, biệt danh.
 *
 * Đây là phần DUY NHẤT về người dùng mà hai môn chia nhau. Mọi thứ khác — nhật ký
 * học, tiến độ, học bạ, bảng của cô giáo — mỗi môn giữ một bộ riêng, để sửa môn này
 * không thể chạm vào dữ liệu môn kia.
 */
import { doc, getDoc, setDoc } from 'firebase/firestore';
import {
  onAuthStateChanged, signInWithCustomToken, signInWithEmailAndPassword,
  signOut, getIdTokenResult,
} from 'firebase/auth';
import { httpsCallable } from 'firebase/functions';
import { db, auth, fns } from './nenTang.js';
import { lopHopLe } from './soQuyen.js';
import { normalizeEmail } from '../../../functions/src/user.js';

/** Hồ sơ người dùng — collection DÙNG CHUNG duy nhất. */
export const NGUOI_DUNG = 'users';
export { ROLES, normalizeEmail, buildUserDoc } from '../../../functions/src/user.js';

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
  const snap = await getDoc(doc(db, NGUOI_DUNG, uid));
  return snap.exists() ? snap.data() : null;
}

export async function saveProfile(uid, { displayName, grade, bietDanh }) {
  if (!db) return;
  /* Chặn lớp lạ ngay tại đây: luật Firestore cho chính chủ sửa hồ sơ và KHÔNG soi
     trường `grade`, nên một con số bậy ghi được thẳng lên — rồi hiện ra bảng xếp
     hạng thành "Bạn nhỏ lớp 99" cho cả trường đọc. */
  const muc = { displayName, grade: lopHopLe(grade), profileComplete: true };
  /* Biệt danh chỉ ghi khi màn gọi có nói tới. Màn chào lần đầu không hỏi biệt danh —
     truyền thẳng `undefined` vào đây là XOÁ MẤT biệt danh con đã đặt từ trước. */
  if (bietDanh !== undefined) muc.bietDanh = String(bietDanh).slice(0, 24);
  await setDoc(doc(db, NGUOI_DUNG, uid), muc, { merge: true });
}

/**
 * Dựng lại SỔ HỌC ngay, không chờ 21:00.
 * Con vừa học xong mà bố mẹ mở sổ thấy trống thì tưởng công học không được lưu.
 */

/* ═══════════ BẢNG XẾP HẠNG ═══════════ */

/**
 * Biệt danh và bạn đang đuổi — hai thứ con tự đặt, nằm trong hồ sơ của chính con.
 *
 * Luật Firestore cho chính chủ sửa hồ sơ miễn là KHÔNG đụng `role`, `uid`, `email`,
 * nên hai trường này ghi thẳng được, không cần Cloud Function.
 */
export async function luuBietDanh(uid, bietDanh) {
  if (!db || !uid || uid === 'local') return false;
  await setDoc(doc(db, NGUOI_DUNG, uid),
    { bietDanh: String(bietDanh || '').trim().slice(0, 24) }, { merge: true });
  return true;
}

export async function luuDuoiKip(uid, maBan) {
  if (!db || !uid || uid === 'local') return false;
  await setDoc(doc(db, NGUOI_DUNG, uid), { duoiKip: maBan || null }, { merge: true });
  return true;
}

/** Bảng toàn hệ thống — chỉ giáo viên và admin đọc được */
