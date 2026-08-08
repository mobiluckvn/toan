/**
 * Nạp nội dung bài học từ thư mục tĩnh (Hosting/CDN) — không cần API.
 * Cấu trúc thư mục public/:
 *    content/lessons/DL_KSN5Q1_B49_M1.json
 *    content/figures/KSN5Q1_B49_M1_F1.png
 */
const BASE = import.meta?.env?.BASE_URL || '/';
export const CONTENT = BASE.replace(/\/$/, '') + '/content';

/**
 * Dấu phiên bản nội dung — vite.config.js băm public/content rồi dán vào đây.
 * Nội dung để `immutable` 7 ngày mà tên tệp không đổi, nên không có dấu này thì
 * sửa bài xong đẩy lên, máy đã từng mở trang vẫn học bản cũ suốt một tuần.
 * Chạy bằng node (bộ kiểm) thì không có biến, lùi về 'dev' — vô hại.
 */
export const NOI_DUNG_V =
  typeof __NOI_DUNG_V__ === 'string' ? __NOI_DUNG_V__ : 'dev';

/** Gắn dấu phiên bản vào một đường dẫn nội dung */
export const dongDau = (url, v = NOI_DUNG_V) =>
  (v && v !== 'dev' ? `${url}?v=${v}` : url);

/** DL:KSN5Q1.B49.M1 → DL_KSN5Q1_B49_M1 */
export const idToFile = (microId) => microId.replace('DL:', 'DL_').replace(/\./g, '_');

/* ─────────── HAI CHƯƠNG TRÌNH, MỘT BỘ MÃ ───────────
 * Lớp 2 và lớp 5 dùng chung mọi màn hình; khác nhau chỉ ở NỘI DUNG và ở nhịp đọc.
 * Chỗ khai khác biệt duy nhất là data/chuong_trinh.json — đừng rải điều kiện
 * "nếu là lớp 2 thì…" ra khắp các component, vì thêm lớp thứ ba là phải đi sửa lại
 * từng chỗ một.
 */
/* Sổ đăng ký chương trình. Đọc từ content/chuong_trinh.json khi app khởi động; có
   sẵn bản tối thiểu để bộ kiểm chạy bằng node (không có mạng) vẫn dùng được.
   THÊM LỚP/MÔN MỚI thì thêm mục trong data/chuong_trinh.json, KHÔNG sửa tệp này. */
let SO_DK = {
  mon: { toan: { ten: 'Toán', bieuTuong: '🔢' } },
  chuongTrinh: {
    lop2: { ma: 'lop2', mon: 'toan', lop: 2, thuMuc: 'lop2', tienTo: 'DL:KSN2.',
            ten: 'Toán Tư Duy lớp 2', soBai: 33, doc: { chuTo: true } },
    lop5: { ma: 'lop5', mon: 'toan', lop: 5, thuMuc: 'lessons', tienTo: 'DL:KSN5Q1.',
            ten: 'Toán Tư Duy lớp 5', soBai: 168, doc: { chuTo: false } },
  },
  sapCo: [], luyenThi: [],
};

export const soDangKy = () => SO_DK;
export const dsChuongTrinh = () => Object.values(SO_DK.chuongTrinh || {});
export const chuongTrinh = (ma) => (SO_DK.chuongTrinh || {})[ma] || SO_DK.chuongTrinh.lop5;
export const cachDoc = (id) => chuongTrinh(chuongTrinhCua(id)).doc || {};

export async function napSoDangKy() {
  try {
    const r = await fetch(dongDau(`${CONTENT}/chuong_trinh.json`));
    if (r.ok) SO_DK = { ...SO_DK, ...(await r.json()) };
  } catch { /* mất mạng: dùng bản mặc định, không chặn bé học */ }
  return SO_DK;
}

/** Bài thuộc chương trình nào — tra TIỀN TỐ mã bài trong sổ đăng ký.
 *  Trước đây so cứng 'DL:KSN2.' trong mã; thêm lớp thứ ba là phải sửa hàm này. */
export const chuongTrinhCua = (id) => {
  const s = String(id || '');
  for (const ct of dsChuongTrinh()) if (ct.tienTo && s.startsWith(ct.tienTo)) return ct.ma;
  return 'lop5';
};

const THU_MUC_CUA = (ma) => chuongTrinh(ma).thuMuc || 'lessons';

/* Chương của từng bài lớp 2 nằm trong dữ liệu (8 chương, số bài mỗi chương khác
   nhau) chứ không suy ra được bằng công thức như lớp 5. Nạp chỉ mục là ghi nhớ. */
const chuongCua = new Map();
const baiCua = new Map();          // mã chương trình → danh sách bài đúng thứ tự học
export function ghiNhoChuong(danhSach) {
  const ids = [];
  for (const b of danhSach || []) {
    if (!b?.id) continue;
    ids.push(b.id);
    if (b.chuong) chuongCua.set(b.id, b.chuong);
  }
  if (ids.length) baiCua.set(chuongTrinhCua(ids[0]), ids);
}

/** B49.M1 (dạng gọn người dùng gõ) → DL:KSN5Q1.B49.M1 */
export const shortToId = (s) => (s.startsWith('DL:') ? s : `DL:KSN5Q1.${s}`);

const cache = new Map();

export async function loadLesson(microId) {
  if (cache.has(microId)) return cache.get(microId);
  const url = dongDau(`${CONTENT}/${THU_MUC_CUA(chuongTrinhCua(microId))}/${idToFile(microId)}.json`);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Không nạp được bài ${microId} (${res.status})`);
  const data = await res.json();
  cache.set(microId, data);
  return data;
}

/**
 * figureSpec lưu "figures/KSN5Q1_B49_M1_F1.png" → URL đầy đủ.
 * Mỗi hình đã có mã kiểm riêng, dùng luôn làm dấu phiên bản: vẽ lại MỘT hình thì
 * chỉ hình ấy được tải lại, 671 hình còn lại vẫn nằm yên trong bộ nhớ đệm.
 */
export const figureSrc = (fig) =>
  (fig?.file ? dongDau(`${CONTENT}/${fig.file}`, fig.sha256_16 || NOI_DUNG_V) : null);

/** Danh sách 168 micro theo đúng thứ tự học */
export function allMicroIds(ct = 'lop5') {
  if (ct !== 'lop5') return baiCua.get(ct) || [];
  const out = [];
  for (let b = 1; b <= 56; b++) for (const k of [1, 2, 3]) out.push(`DL:KSN5Q1.B${b}.M${k}`);
  return out;
}

/** Micro kế tiếp / trước đó — ưu tiên series.next trong dữ liệu, không có thì theo thứ tự */
export function neighborIds(microId, lesson) {
  const list = allMicroIds();
  const i = list.indexOf(microId);
  const next = lesson?.series?.next && lesson.series.next.startsWith('DL:')
    ? lesson.series.next : (i >= 0 && i < list.length - 1 ? list[i + 1] : null);
  const prev = lesson?.series?.prev && lesson.series.prev.startsWith('DL:')
    ? lesson.series.prev : (i > 0 ? list[i - 1] : null);
  return { prev, next };
}

/** Chương của một bài. Lớp 5 suy ra bằng công thức, lớp 2 tra bảng đã ghi nhớ. */
export const chapterOf = (microId) => {
  if (chuongCua.has(microId)) return chuongCua.get(microId);
  if (chuongTrinhCua(microId) === 'lop2') return 1;   // chưa nạp chỉ mục
  const b = Number(String(microId).split('.B')[1]?.split('.M')[0]);
  return Number.isFinite(b) ? Math.ceil(b / 4) : 1;
};
