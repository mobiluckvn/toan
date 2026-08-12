/**
 * NẠP NỘI DUNG TIẾNG ANH — bài học, danh mục chương, và sổ âm.
 *
 * Dùng lại `chung/lib/soQuyen.js` (đường dẫn, sổ đăng ký, đóng dấu phiên bản) vì
 * đó là tầng CHUNG, được phép. KHÔNG import gì từ `mon/toan/**` — cổng
 * `ranh_gioi.test.mjs` chặn, và chặn đúng: bộ nạp của Toán biết những thứ chỉ Toán
 * mới có (chủ đề, dạng bài, ma trận), còn tiếng Anh thì cần một thứ Toán không có —
 * SỔ ÂM.
 */
import { CONTENT, dongDau, idToFile, chuongTrinh, dsChuongTrinh } from '../../../chung/lib/soQuyen.js';

/** Các quyển của môn này, theo thứ tự trên kệ. */
export const quyenTiengAnh = () => dsChuongTrinh()
  .filter((c) => c.mon === 'tienganh')
  .sort((a, b) => (a.thuTu ?? 99) - (b.thuTu ?? 99));

export const quyenDau = () => quyenTiengAnh()[0] || null;

/** Tra một quyển theo mã. Vỏ app truyền MÃ CHUỖI xuống màn của môn, không phải
    mục chương trình — xem `src/soMon.js`. */
export const timQuyen = (ma) => quyenTiengAnh().find((c) => c.ma === ma) || null;

/** 'DL:TA1.B04' → 'ta1' */
export const quyenCua = (id) => (quyenTiengAnh()
  .find((c) => String(id).startsWith(c.tienTo || '§')) || {}).ma || null;

const kho = new Map();

/** Nạp một bài, có nhớ — mở lại bài vừa học thì không tải lần nữa. */
export async function napBai(id) {
  if (kho.has(id)) return kho.get(id);
  const ma = quyenCua(id);
  if (!ma) throw new Error(`không rõ bài ${id} thuộc quyển nào`);
  const tm = chuongTrinh(ma).thuMuc;
  const r = await fetch(dongDau(`${CONTENT}/${tm}/${idToFile(id)}.json`));
  if (!r.ok) throw new Error(`không mở được bài ${id} (${r.status})`);
  const d = await r.json();
  kho.set(id, d);
  return d;
}

/* ─────────── SỔ ÂM ───────────
   Mỗi clip có `van_tay` là sha256 của CHỮ. Sửa một câu thì vân tay đổi, và cổng
   `tienganh_am.test.mjs` bắt được là clip ấy chưa sinh lại. Ở đây chỉ cần tra
   `id → tệp`, nhưng giữ nguyên cả sổ để màn hình nào cần cũng hỏi được. */
let soAm = null;

const SO_AM_RONG = { clip: {}, thuMuc: '' };

/**
 * Nạp sổ âm, có nhớ.
 *
 * CHỈ NHỚ KHI THÀNH CÔNG. Bản đầu nhớ cả lần hỏng, và nó hỏng thật: hàm này chạy
 * trước khi `napSoDangKy()` kịp tải xong, nên `chuongTrinh('ta1')` chưa thấy quyển,
 * `ct.am` là undefined, và sổ rỗng bị ghi vào bộ nhớ VĨNH VIỄN. Từ đó mọi nút nghe
 * đều tra ra null và tự ẩn — cả quyển câm, mà màn hình vẫn đủ chữ nên nhìn không
 * ra. Cổng cũng không thấy: dữ liệu đủ, 333 clip nằm đúng chỗ, chỉ là không ai gọi.
 *
 * Nhớ một kết quả RỖNG không tiết kiệm được gì đáng kể, mà mất thì mất cả môn.
 */
export async function napSoAm(ma = 'ta1') {
  if (soAm) return soAm;
  const ct = chuongTrinh(ma);
  const duong = (ct.am || {}).so;
  if (!duong) return SO_AM_RONG;          // chưa có sổ đăng ký → THỬ LẠI lần sau
  try {
    const r = await fetch(dongDau(`${CONTENT}/${duong}`));
    if (!r.ok) return SO_AM_RONG;
    const d = await r.json();
    const clip = Object.fromEntries((d.clip || []).map((c) => [c.id, c]));
    if (!Object.keys(clip).length) return SO_AM_RONG;
    soAm = { thuMuc: (ct.am || {}).thuMuc || 'tienganh/audio', clip };
  } catch {
    /* Mất sổ âm thì bài VẪN học được, chỉ là không có tiếng. Với lớp 1 đó là mất
       một nửa, nhưng thà mất một nửa còn hơn màn hình trắng — và lần sau còn thử lại. */
    return SO_AM_RONG;
  }
  return soAm;
}

/** Đường dẫn tệp tiếng của một mã clip, hoặc null nếu chưa sinh. */
export function duongAm(maClip) {
  if (!maClip || !soAm) return null;
  const c = soAm.clip[maClip];
  return c ? dongDau(`${CONTENT}/${soAm.thuMuc}/${c.tep}`) : null;
}

/* ─────────── CHƯƠNG ─────────── */

/**
 * 16 bài gom thành 4 chương, đọc TỪ CHÍNH BÀI (`chuong` + `tenChuong`).
 *
 * Không đọc từ sổ đăng ký và cũng không tự chia 4 bài một chương: sách chia thế
 * nào thì bài khai thế ấy, và lớp 2 có thể chia khác. Tự chia ở đây là chỗ sẽ lệch
 * lặng lẽ khi thêm quyển.
 */
export function chuongCua(bais) {
  const m = new Map();
  for (const b of bais) {
    if (!m.has(b.chuong)) m.set(b.chuong, { so: b.chuong, ten: b.tenChuong, bai: [] });
    m.get(b.chuong).bai.push(b);
  }
  return [...m.values()].sort((a, b) => a.so - b.so);
}

/** Danh mục kỳ ôn tập của một quyển. */
export async function napOnTap(ma = 'ta1') {
  const ct = chuongTrinh(ma);
  try {
    const r = await fetch(dongDau(`${CONTENT}/${ct.tepOnTap || `${ct.thuMuc}/ontap.json`}`));
    return r.ok ? await r.json() : [];
  } catch { return []; }
}

/** Mã bài liền trước / liền sau, suy từ chính danh sách trong sổ. */
export function hangXom(id) {
  const ma = quyenCua(id);
  const ds = (chuongTrinh(ma).bai) || [];
  const i = ds.indexOf(id);
  return { truoc: i > 0 ? ds[i - 1] : null, sau: i >= 0 && i < ds.length - 1 ? ds[i + 1] : null };
}
