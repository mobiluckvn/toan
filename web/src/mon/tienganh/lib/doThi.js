/**
 * ĐỒ THỊ TRI THỨC — bản rút gọn, duyệt được ngay trên máy con.
 *
 * ── VÌ SAO TỚI ĐỢT 3 MỚI CÓ ──
 * `data/ban_do_tieng_anh.json` (3989 nút · 7602 cạnh) chỉ dùng LÚC DỰNG; app đọc
 * tệp bài phẳng đã sinh sẵn. Nghĩa là suốt thời gian qua, lúc chạy máy con KHÔNG
 * có đồ thị nào để duyệt — nên hai mục của luận văn đứng im: 2.2.1 (duyệt để chẩn
 * đoán) và 2.3.3 (lan truyền).
 *
 * `tools/xuat_do_thi_con.py` cắt xuống còn 1194 nút · 253 cạnh, 80 KB. Nó CHỈ giữ
 * QUAN HỆ — không nhãn, không ví dụ, không nghĩa tiếng Việt. Bài học đã mang đủ
 * chữ nghĩa rồi; chép lại vào đây là nhân đôi dữ liệu, mà nhân đôi thì sớm muộn
 * hai bản lệch nhau và không ai biết bản nào đúng.
 *
 * ── HƯỚNG CỦA CẠNH, ĐỌC CHO KỸ ──
 *     { can: A, truoc_khi: B }   nghĩa là PHẢI CÓ A TRƯỚC KHI HỌC B.
 * Nên `truoc(B)` trả về A, và `sau(A)` trả về B. Đảo nhầm hai đầu thì lan truyền
 * chẩn đoán chạy đúng chiều ngược lại: bé sai một từ ở unit 1 mà hệ thống đi tìm
 * nguyên nhân ở unit 20 — sai mà nghe vẫn có lý, nên không ai cãi.
 *
 * ── ⚠ BA LOẠI CẠNH, KHÔNG DÙNG LẪN ──
 *   ban_do     REQUIRES của bản đồ gốc (195). Ràng buộc tiên quyết THẬT.
 *   noi_bai    bắc cầu giữa hai unit của một nhóm từ vựng có thứ tự (5). Cũng là
 *              ràng buộc thật — xem `thang_tu_vung` trong `chuan_tienganh.py`.
 *   trong_bai  thứ tự ĐỌC của hai từ liền nhau trong CÙNG một bài (53).
 *              ⚠ KHÔNG PHẢI cửa ải. Sách dạy cả khối trong một buổi; ai lấy loại
 *              này đi khoá bài là chặn bé giữa chính bài đang học.
 * Mặc định các phép duyệt BỎ `trong_bai`, phải xin mới có.
 */
import { CONTENT, dongDau } from '../../../chung/lib/soQuyen.js';

/** Loại cạnh dùng được cho việc GÁC và CHẨN ĐOÁN. */
export const CANH_THAT = new Set(['ban_do', 'noi_bai']);

/* Nạp MỘT LẦN cho cả phiên. Đồ thị không đổi giữa chừng, và 80 KB thì không đáng
   tải lại mỗi lần mở bài. Hỏng thì trả đồ thị RỖNG chứ không ném: mọi phép dưới
   đây tự trả rỗng, bên gọi lùi về lối cũ, bé học bình thường. */
const RONG = { nut: {}, canh: [] };
let nho = null;
let dangNap = null;

export async function napDoThi() {
  if (nho) return nho;
  if (!dangNap) {
    dangNap = (async () => {
      try {
        const r = await fetch(dongDau(`${CONTENT}/tienganh/do_thi.json`));
        nho = r.ok ? await r.json() : RONG;
      } catch { nho = RONG; }
      if (!nho?.nut || !nho?.canh) nho = RONG;
      return nho;
    })();
  }
  return dangNap;
}

/** Chỉ dùng trong cổng — bơm đồ thị giả để khỏi phải fetch. */
export function datDoThi(d) { nho = d && d.nut && d.canh ? d : RONG; dangNap = null; }

const locCanh = (canh, keCaTrongBai) =>
  (canh || []).filter((c) => keCaTrongBai || CANH_THAT.has(c.loai || 'ban_do'));

/** Những nút PHẢI CÓ TRƯỚC nút này. */
export function truoc(dt, ma, { keCaTrongBai = false } = {}) {
  if (!ma) return [];
  return locCanh(dt?.canh, keCaTrongBai)
    .filter((c) => c.truoc_khi === ma)
    .map((c) => c.can);
}

/** Những nút DỰNG TRÊN nút này. */
export function sau(dt, ma, { keCaTrongBai = false } = {}) {
  if (!ma) return [];
  return locCanh(dt?.canh, keCaTrongBai)
    .filter((c) => c.can === ma)
    .map((c) => c.truoc_khi);
}

/**
 * Duyệt theo một chiều, trả về `[{ ma, buoc }]` — `buoc` là số cạnh đã đi.
 *
 * ⚠ HAI LƯỚI ĐỠ, VÀ CHÚNG ĐỠ HAI THỨ KHÁC NHAU — đừng nhầm.
 *
 * `sauToiDa` (trần độ sâu) là thứ giữ cho phép duyệt LUÔN DỪNG, kể cả gặp chu
 * trình. Nó có mặt trước hết vì ý nghĩa: nguyên nhân cách chỗ sai bảy bước thì
 * không còn là "nguyên nhân" theo nghĩa dạy được nữa.
 *
 * `daTham` KHÔNG phải để chống treo — trần độ sâu đã lo việc ấy. Nó chống hai
 * chuyện khác: (1) cùng một nút bị trả về nhiều lần, nên bảng chẩn đoán hiện một
 * nút ba dòng; (2) số nhánh phình theo cấp số nhân khi đồ thị có nhiều đường tới
 * cùng một nút. Đã đo bằng cách gỡ nó ra: không treo, nhưng kết quả sai.
 *
 * Nói cho đúng như thế vì một cảnh báo nói quá thì lần sau người đọc trừ hao cả
 * những cảnh báo đúng.
 */
function duyet(dt, ma, lay, { sauToiDa = 4, keCaTrongBai = false } = {}) {
  if (!ma || !dt?.canh?.length) return [];
  const daTham = new Set([ma]);
  const ra = [];
  let bien = [ma];
  for (let b = 1; b <= sauToiDa && bien.length; b += 1) {
    const tiep = [];
    for (const u of bien) {
      for (const v of lay(dt, u, { keCaTrongBai })) {
        if (daTham.has(v)) continue;
        daTham.add(v);
        ra.push({ ma: v, buoc: b });
        tiep.push(v);
      }
    }
    bien = tiep;
  }
  return ra;
}

/** Mọi nút cần có TRƯỚC nút này, gần trước xa sau. */
export const duyetNguoc = (dt, ma, opt) => duyet(dt, ma, truoc, opt);

/** Mọi nút DỰNG TRÊN nút này. */
export const duyetXuoi = (dt, ma, opt) => duyet(dt, ma, sau, opt);

/** Nút này có trong đồ thị không — để bên gọi biết mà lùi về lối cũ. */
export const coNut = (dt, ma) => !!(ma && dt?.nut?.[ma]);

/** Loại của một nút (`vocabulary` · `grammar` · …), hoặc null. */
export const loaiNut = (dt, ma) => dt?.nut?.[ma]?.t || null;

/** Lớp của một nút, hoặc null. Cạnh xuyên lớp nhận ra bằng hai đầu khác lớp. */
export const lopNut = (dt, ma) => {
  const g = dt?.nut?.[ma]?.g;
  return Number.isFinite(g) ? g : null;
};

/**
 * Nhãn ĐỌC ĐƯỢC của một nút — "city — thành phố" chứ không phải `v_g5_u1_city`.
 *
 * Không có nhãn thì trả về `null`, và bên gọi PHẢI xử lý: bày mã máy ra cho bố mẹ
 * đọc là đúng thứ đã xảy ra ngày 22-08 (Góc bố mẹ hiện `CHUONG%3A1%40G3`).
 */
export const nhanNut = (dt, ma) => dt?.nut?.[ma]?.n || null;

/** Bài nào DẠY nút này. Đây là cầu từ "mã nút" sang thứ dạy được cho bé. */
export const baiCuaNut = (dt, ma) => dt?.nut?.[ma]?.b || null;

/**
 * BÀI TIÊN QUYẾT của một bài — đi từ các nút của bài này, lần ngược theo cạnh,
 * rồi hỏi "nút ấy dạy ở bài nào".
 *
 * ── VÌ SAO CẦN, KHI ĐÃ CÓ CỬA SỔ "BA BÀI GẦN NHẤT" ──
 * Đo trên cả 94 bài: cửa sổ tuần tự BỎ SÓT tiên quyết ở 40 bài, trong đó 2 bài
 * sót tiên quyết nằm ở QUYỂN KHÁC (`DL:TA2.B02` cần `DL:TA1.B11`) — đúng cái
 * `cross_grade` mà luận văn nêu ở mục 2.2.2. Cửa sổ ba bài không bao giờ với tới
 * đó được, dù nới rộng bao nhiêu cũng thế: nó nới trong CÙNG quyển.
 *
 * ── ⚠ VÀ VÌ SAO KHÔNG THAY HẲN CỬA SỔ ẤY ──
 * Đo tiếp: nếu THAY, thì 87/94 bài có vốn từ HẸP ĐI, nhiều bài về RỖNG — vì phần
 * lớn từ vựng không có cạnh tiên quyết nào (đúng: `book` không cần `pen` trước).
 * Cô giáo máy sẽ cụt từ ở 87 bài để đổi lấy 40 bài đúng hơn. Nên GỘP, không thay.
 *
 * Trả về `[maBai]`, KHÔNG gồm chính bài đang mở.
 */
export function baiTienQuyet(dt, maNutDs, { boQua = null, sauToiDa = 2 } = {}) {
  const ra = [];
  const da = new Set();
  for (const n of (maNutDs || [])) {
    for (const { ma } of duyetNguoc(dt, n, { sauToiDa })) {
      const b = baiCuaNut(dt, ma);
      if (!b || b === boQua || da.has(b)) continue;
      da.add(b);
      ra.push(b);
    }
  }
  return ra;
}
