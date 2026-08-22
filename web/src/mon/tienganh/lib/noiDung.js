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
 *
 * ── ⚠ NHỚ THEO TỪNG QUYỂN, VÀ CHẶN CUỘC ĐUA (sửa 22-08-2026) ──
 * Bản cũ nhớ vào MỘT biến chung cho mọi quyển, và `BaiHoc.jsx` gọi `napSoAm()`
 * KHÔNG THAM SỐ — mặc định `ta1`. Hai lời gọi chạy song song khi bé mở một bài:
 * `ManTiengAnh` gọi với quyển thật, `BaiHoc` gọi với ta1. Cả hai cùng thấy `soAm`
 * còn rỗng nên cùng tải, và LỜI GỌI NÀO XONG SAU thì thắng.
 *
 * Thua cuộc đua thì sổ âm trong bộ nhớ là của lớp 1, mọi mã clip của lớp 3·4·5
 * tra ra null, và `NutNghe` TỰ ẨN. Bé mất nút "Nghe cô đọc" ở chặng Từ mới và
 * Mẫu câu — tức là mất phần NGHE TRƯỚC KHI NÓI, đúng thứ chặng ấy sinh ra để làm.
 * Màn hình vẫn đủ chữ nên nhìn lướt không ra; bác bắt được ngày 22-08.
 *
 * Lỗi này có từ `0b65a94c` (lúc dựng quyển Tiếng Anh đầu tiên), không phải mới —
 * nhưng nó là CUỘC ĐUA nên lúc lộ lúc không, tuỳ máy và tuỳ mạng.
 *
 * Nay: nhớ theo `ma`, và giữ lời hứa đang bay để hai lời gọi cùng quyển dùng
 * chung một lần tải.
 */
const khoAm = new Map();
const dangNapAm = new Map();

export async function napSoAm(ma = 'ta1') {
  if (khoAm.has(ma)) { soAm = khoAm.get(ma); return soAm; }
  if (dangNapAm.has(ma)) return dangNapAm.get(ma);
  const chay = napSoAmThat(ma);
  dangNapAm.set(ma, chay);
  try { return await chay; } finally { dangNapAm.delete(ma); }
}

async function napSoAmThat(ma) {
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
    khoAm.set(ma, soAm);
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

/**
 * Bài đọc hiểu của một quyển — mỗi chương một bài.
 *
 * Quyển chưa có thì trả MẢNG RỖNG, không ném: lớp 1·2 chưa dựng bài đọc hiểu, và
 * một tệp 404 không được phép làm trang chính của chúng trắng màn. Cùng lối với
 * `napOnTap` ngay trên.
 */
export async function napDocHieu(ma = 'ta1') {
  const ct = chuongTrinh(ma);
  try {
    const r = await fetch(dongDau(`${CONTENT}/${ct.thuMuc || ma}/dochieu.json`));
    return r.ok ? await r.json() : [];
  } catch { return []; }
}

/** Đề bài viết ngắn của một quyển — mỗi chương một đề. Chưa có thì mảng rỗng. */
export async function napVietBai(ma = 'ta1') {
  const ct = chuongTrinh(ma);
  try {
    const r = await fetch(dongDau(`${CONTENT}/${ct.thuMuc || ma}/vietbai.json`));
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

/**
 * HÌNH CỦA MỘT TỪ.
 *
 * Hình KHÔNG nằm trong `knowledgeCore.vocabulary` mà ở `bai.hinhTu` — hai chỗ khác
 * nhau, và đó chính là chỗ đã dính lỗi thật: thanh VIỆC CỦA CON tự đọc `v.ve`/`v.hinh`
 * từ `vocabulary`, không có nên cả bốn ô vẽ ra dấu ❔ trong khi thẻ từ ngay dưới vẫn
 * đủ 🍗🍟🐟🥛. Cổng xanh, bản dựng xanh, chỉ mở ra nhìn mới thấy.
 *
 * Nên hàm này là NGUỒN DUY NHẤT. Ba chỗ vẽ hình từ — thẻ từ, thanh việc, và phòng
 * luyện nói — đều phải hỏi nó. Chỗ nào tự đọc lại `bai.hinhTu` là chỗ ấy sẽ lệch,
 * mà lệch kiểu không cổng nào bắt được. Xem [[mot-nguon-cho-hai-ben-ve]].
 */
export const hinhCuaTu = (bai, tu) => (bai?.hinhTu || []).find((h) => h.tu === tu) || {};

/**
 * VIDEO TỪ MỚI CỦA MỘT BÀI — luôn là một DANH SÁCH.
 *
 * Lớp 1·2 mỗi unit 3,5 từ nên một video là đủ. Lớp 3 là 9,7 từ, nhiều nhất 15 — giữ
 * một tệp thì video dài 54 tới 75 giây, mà bé lớp ba ngồi không nổi thì nó bấm bỏ
 * qua và cả bài giảng thành công cốc. Nên `sinh_bai_tienganh.py` tách theo NHÓM
 * NGHĨA (`vai` đã chia sẵn) và khai ra `video.tu` một danh sách.
 *
 * Hàm này là NGUỒN DUY NHẤT trả danh sách ấy, kể cả với bài chỉ có một nhóm. Chỗ
 * nào tự đọc `bai.video.tu` rồi tự đoán "chuỗi hay mảng" là chỗ sẽ đoán sai — cùng
 * họ với `hinhCuaTu` ở trên, và cùng một cách chữa.
 *
 * Bài cũ (`"tu": "…_tu.mp4"`) vẫn đọc được: bọc thành một nhóm. Không phải để giữ
 * tương thích mãi mãi, mà để một bản dựng cũ còn nằm trong cache trình duyệt không
 * làm bé mất hẳn ô video.
 */
export function dsVideoTu(bai) {
  const v = bai?.video?.tu;
  if (!v) return [];
  if (typeof v === 'string') return [{ ma: 'tu', ten: 'Từ mới', tep: v, tu: [] }];
  return v.filter((g) => g && g.tep);
}

/**
 * Mã của tối đa `n` bài ĐỨNG TRƯỚC bài này, theo đúng thứ tự học.
 *
 * Phòng luyện nói cần chúng để mở rộng vốn từ khi bé đã đạt unit. Hỏi sổ đăng ký
 * chứ không suy từ mã bài: mã có tăng dần thật, nhưng suy từ chuỗi là ghim cứng
 * cách đánh số của quyển này vào chỗ chẳng liên quan gì.
 */
export function maBaiTruoc(id, n = 3) {
  /* ⚠ `quyenCua` trả về MỘT CHUỖI mã ('ta3'), không phải mục chương trình. Bản đầu
     viết `const ct = quyenCua(id); const ds = ct?.bai` — `'ta3'.bai` là undefined,
     nên hàm này trả mảng RỖNG cho mọi bài, mọi quyển, từ ngày viết. Phòng luyện
     nói vì thế không bao giờ mở rộng vốn từ sang mấy unit trước dù bé đã đạt: cờ
     `von.moRong` luôn tắt, và dòng "có cả từ mấy bài trước con đã học" không bao
     giờ hiện. Không lỗi, không cảnh báo — chỉ là một tính năng nằm im.
     `hangXom` ngay trên cùng tệp này làm đúng: `chuongTrinh(quyenCua(id))`. */
  const ds = chuongTrinh(quyenCua(id))?.bai || [];
  const i = ds.indexOf(id);
  if (i <= 0) return [];
  return ds.slice(Math.max(0, i - n), i);
}

/**
 * Kịch bản phòng luyện nói của cả quyển — sinh bằng `tools/sinh_kichban_noi.py`.
 *
 * ⚠ NHỚ THEO TỪNG QUYỂN, KHÔNG NHỚ CHUNG MỘT Ô.
 *
 * Bản đầu giữ đúng một biến `khoKichBan` và một tham số `ma = 'ta1'`. Hai chỗ hỏng
 * chồng lên nhau, và cả hai đều câm:
 *
 *   · `PhongNoi.jsx` gọi `napKichBanNoi()` KHÔNG tham số, nên lớp 2 và lớp 3 tải
 *     về kịch bản của LỚP 1. `kichBanCua(ds, 'DL:TA3.B05')` không thấy bài nào →
 *     `kichBan = null` → cả tầng kịch bản tắt, phòng rơi về lối mô hình tự nghĩ
 *     câu. Đúng cái bác nhìn thấy khi bảo "chẳng có hiệu quả gì".
 *   · Kể cả có truyền mã, ô nhớ chung cũng trả về quyển tải trước đó — bé học
 *     xong lớp 2 rồi mở lớp 3 trong cùng một phiên là dính.
 *
 * Không có gì đỏ: `napKichBanNoi` trả về một mảng hợp lệ, chỉ là mảng của quyển
 * khác. Chỉ lộ khi mở phòng lớp 3 rồi so từng lượt với tệp kịch bản.
 */
const khoKichBan = new Map();
export async function napKichBanNoi(ma = 'ta1') {
  if (khoKichBan.has(ma)) return khoKichBan.get(ma);
  const ct = chuongTrinh(ma);
  const url = dongDau(`${CONTENT}/${ct.thuMuc || ma}/kichban_noi.json`);
  const r = await fetch(url);
  if (!r.ok) throw new Error(`Không mở được kịch bản luyện nói (${r.status})`);
  const ds = await r.json();
  khoKichBan.set(ma, ds);
  return ds;
}
export const kichBanCua = (ds, id) => (ds || []).find((k) => k.bai === id) || null;
