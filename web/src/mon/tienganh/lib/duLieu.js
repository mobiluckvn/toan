/**
 * DỮ LIỆU HỌC CỦA MÔN TIẾNG ANH — tiến độ và học bạ trên máy chủ.
 *
 * Mọi collection ở đây là CỦA RIÊNG TIẾNG ANH. Chỉ dùng chung với môn khác đúng hai
 * thứ: thể hiện Firebase (`chung/lib/nenTang.js`) và tài khoản (`chung/lib/taiKhoan.js`).
 *
 * ── VÌ SAO KHÔNG DÙNG CHUNG `progress/{uid}/micros` VỚI TOÁN ──
 * Không phải vì sợ trùng mã bài (`DL:TA1.B04` khác `DL:KSN2.B04` sẵn rồi). Lý do thật:
 * Cloud Function nền chạy trên MỌI tài liệu của thư mục ấy và xử theo luật của Toán —
 * tính mức thạo BKT theo ma trận Toán, dựng sổ học theo dạng bài Toán. Đổ bài tiếng
 * Anh vào đó là hàm nền âm thầm tính sai cho cả hai môn, mà không có gì báo.
 *
 * ── ⚠ PHẢI DEPLOY LUẬT TRƯỚC KHI GHI ──
 * `firestore.rules` kết bằng `match /{document=**} { allow read, write: if false; }`.
 * Nghĩa là collection MỚI bị từ chối — và Firestore từ chối **trong im lặng** với
 * lệnh ghi không chờ kết quả: bé học xong, máy báo xong, mà máy chủ không có gì.
 * Đây là lỗi đã dính thật một lần khi làm học bạ (xem sổ ghi nhớ).
 *
 * Nên: luật cho `progressTA` và `hocBaTA` đã viết sẵn trong `firestore.rules`, nhưng
 * **phải `firebase deploy --only firestore:rules`** thì mới có tác dụng. Trước khi
 * deploy thì `LOI_GHI` dưới đây đếm số lần bị từ chối để còn biết mà lần ra.
 */
import {
  doc, getDoc, setDoc, collection, getDocs, serverTimestamp,
} from 'firebase/firestore';
import { db, hasFirebase } from '../../../chung/lib/nenTang.js';

/** Tên collection — gõ MỘT chỗ. Hậu tố TA để không bao giờ lẫn với Toán. */
export const KHO = {
  tienDo: (uid) => `progressTA/${uid}/micros`,
  hocBa: (uid) => `hocBaTA/${uid}/muc`,
};

/* Mã bài có dấu ':' và '.', mà tên tài liệu Firestore thì không chứa '/' và nên
   tránh dấu lạ — quy về gạch dưới, và quy NGƯỢC lại được để đọc ra. */
const maTep = (id) => String(id).replace(/[:.]/g, '_');

/**
 * Đếm số lần máy chủ từ chối. Không ném lỗi ra màn hình — bé đang học thì không
 * việc gì phải thấy — nhưng cũng KHÔNG nuốt im: có số thì người sửa lần ra được.
 */
export const LOI_GHI = { tuChoi: 0, ganNhat: null };

const nuot = (e) => {
  LOI_GHI.tuChoi += 1;
  LOI_GHI.ganNhat = String(e?.code || e?.message || e);
  if (import.meta.env?.DEV) {
    // eslint-disable-next-line no-console
    console.warn('[tienganh] máy chủ từ chối ghi:', LOI_GHI.ganNhat,
      '— đã deploy firestore.rules cho progressTA/hocBaTA chưa?');
  }
};

const dungDuoc = (uid) => !!(hasFirebase && db && uid);

/* ─────────── GHI ─────────── */

/**
 * Lưu kết quả một bài lên máy chủ.
 *
 * `merge: true` chứ không ghi đè: bé làm lại bài trên máy khác thì hai lần ghi
 * không xoá nhau, và `gopTienDo` ở tầng trên chọn bản mới hơn.
 */
export async function luuBai(uid, id, m) {
  if (!dungDuoc(uid)) return false;
  try {
    await setDoc(doc(db, KHO.tienDo(uid), maTep(id)), {
      microId: id,
      pass: !!m.pass,
      /* `score` và `pass` là hai trường luật Firestore ĐÒI phải có và đúng kiểu.
         Thiếu một trong hai là bị từ chối — và từ chối im lặng. */
      score: Number(m.best || 0),
      total: Number(m.total || 0),
      bac: Number(m.bac || 0),
      attempts: Number(m.attempts || 1),
      at: m.at || new Date().toISOString(),
      serverTs: serverTimestamp(),
    }, { merge: true });
    return true;
  } catch (e) { nuot(e); return false; }
}

/** Lưu một mục học bạ (kỳ ôn tập chương). */
export async function luuMucHocBa(uid, loai, khoa, du) {
  if (!dungDuoc(uid)) return false;
  try {
    await setDoc(doc(db, KHO.hocBa(uid), `${loai}__${maTep(khoa)}`), {
      loai, khoa, ...du, at: new Date().toISOString(), serverTs: serverTimestamp(),
    }, { merge: true });
    return true;
  } catch (e) { nuot(e); return false; }
}

/* ─────────── ĐỌC ─────────── */

async function docTienDo(uid) {
  const snap = await getDocs(collection(db, KHO.tienDo(uid)));
  const micros = {};
  snap.forEach((d) => {
    const v = d.data();
    if (v.microId) {
      micros[v.microId] = {
        done: true, pass: !!v.pass, best: v.score || 0, total: v.total || 0,
        bac: v.bac || 0, attempts: v.attempts || 1, at: v.at || null,
      };
    }
  });
  return micros;
}

async function docHocBa(uid) {
  const snap = await getDocs(collection(db, KHO.hocBa(uid)));
  const chapters = {};
  snap.forEach((d) => {
    const v = d.data();
    /* `|| {}` chứ KHÔNG `|| v`. Bản cũ đỡ lấy cả tài liệu khi thiếu `giaTri`, và
       cái đỡ ấy chính là thứ che mất chuyện bên ghi đang gửi sai hình dạng: đọc ra
       vẫn có gì đó, chỉ là thiếu `best` — thẻ huy hiệu hiện "undefined/undefined".
       Nay chỉ nhận đúng một hình dạng, giống hệt Toán (`toan/lib/duLieu.js`). */
    if (v.loai === 'chuong' && v.khoa) chapters[v.khoa] = v.giaTri || {};
  });
  return chapters;
}

/**
 * Sổ tiến độ đầy đủ từ máy chủ. Hỏng chỗ nào thì trả rỗng chỗ ấy — bé vẫn học
 * được bằng sổ tại máy, đó mới là nguồn chính.
 */
export async function tienDoTuMay(uid) {
  if (!dungDuoc(uid)) return { micros: {}, chapters: {} };
  const [micros, chapters] = await Promise.all([
    docTienDo(uid).catch((e) => { nuot(e); return {}; }),
    docHocBa(uid).catch((e) => { nuot(e); return {}; }),
  ]);
  return { micros, chapters };
}

/**
 * BẢNG XẾP HẠNG — đọc chung một tài liệu với Toán, và đó là CỐ Ý.
 *
 * `bangXepHang/global` là tài liệu DUY NHẤT một bé đọc được về bé khác, nên nó là
 * chỗ cẩn thận nhất của cả bộ luật: Cloud Function dựng nó và chỉ đặt vào biệt danh ·
 * lớp · sao. Dựng thêm một bảng thứ hai cho tiếng Anh nghĩa là mở thêm một lối rò dữ
 * liệu nữa — đắt hơn nhiều so với cái lợi.
 *
 * Nhưng hàm nền hiện CHỈ đếm sao của Toán. Nên ở đây trả `null` cho tới khi hàm ấy
 * biết tính cả tiếng Anh — trả một bảng chỉ có điểm Toán mà gắn nhãn "Tiếng Anh" thì
 * còn tệ hơn không có bảng.
 */
export async function bangXepHang() {
  if (!dungDuoc('x')) return null;
  try {
    const snap = await getDoc(doc(db, 'bangXepHang/global'));
    const d = snap.exists() ? snap.data() : null;
    return d && d.coTiengAnh ? d : null;
  } catch { return null; }
}
