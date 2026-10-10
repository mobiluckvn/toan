/**
 * CHỮ LẠ — bản CHÉP của `src/mon/tienganh/lib/chamviet.js` cho phía máy chủ.
 *
 * ── VÌ SAO CHÉP, KHÔNG IMPORT ──
 * Máy chủ (`functions/`) và máy con (`src/`) KHÔNG được import chéo — cổng
 * `ranh_gioi.test.mjs` chặn, và chặn vì đúng: `functions/` đi lên Cloud Functions
 * với `package.json` riêng, còn `src/` đi qua Vite. Một import chéo là bản deploy
 * vỡ, mà vỡ lúc deploy thì không có cổng nào bắt trước.
 *
 * Nên theo đúng lối kho này đã dùng cho `lib/onlai.js` ↔ `functions/src/schedule.js`:
 * CHÉP, rồi viết một cổng SO HAI BẢN. Cổng `test/chula_hai_ban.test.mjs` đem cùng
 * một tập đầu vào cho cả hai bản và đòi kết quả y hệt — lệch một li là nó đỏ.
 *
 * ⚠ SỬA MỘT BÊN LÀ PHẢI SỬA BÊN KIA. Và lệch nhau ở đây hỏng theo kiểu khó thấy
 * nhất: máy chủ tự soi lời chấm rồi bảo "sạch", máy con soi lại bằng luật khác rồi
 * bỏ mất một mục — bé thấy lời chấm thiếu, mà hai bên đều báo mình đúng.
 *
 * ── VÌ SAO MÁY CHỦ CẦN NÓ ──
 * Việc V4 chạy chuỗi ba mắt xích ngay trên máy chủ, và giữa mắt xích 2 với 3 phải
 * soi xem mô hình có dùng chữ ngoài vốn không — soi NGAY để còn gọi lại được. Trước
 * V4 phép soi chỉ có ở máy con, tức tới lúc biết thì đã hết lượt gọi.
 */

/** Mọi chữ tiếng Anh trong một chuỗi. Dấu câu bóc sạch, dấu nháy giữ (`don't`). */
export const chuTiengAnh = (s) => String(s || '').toLowerCase().match(/[a-z']+/g) || [];

/** Những chữ trong câu KHÔNG nằm trong vốn từ của bài. */
/**
 * GỐC CỦA MỘT CHỮ BIẾN HÌNH — `friends` → `friend`, `playing` → `play`/`playe`.
 *
 * ⚠ ĐÂY LÀ CHỖ NỚI HÀNG RÀO, nên nới hẹp nhất có thể. Trả về mấy GỐC CÓ THỂ, rồi
 * `chuLa` chỉ tha khi một gốc ấy THẬT SỰ có trong vốn. Không có gốc nào trúng thì
 * chữ vẫn là chữ lạ: `has` không lọt nhờ `ha`, `the` không lọt nhờ gì cả.
 *
 * ── VÌ SAO PHẢI CÓ ──
 * Đi thử bản thật 10-10-2026: bé viết *"I can see two friend"*, mô hình sửa đúng
 * thành *"two friends"*, rồi `friends` bị bác vì bảng vốn chỉ khai `friend` — câu
 * sửa bị bỏ, và bé nhận điểm 6/10 kèm câu "cô không tìm thấy lỗi nào trong bài của
 * con". Dạy đúng cái đuôi `-s` ấy CHÍNH LÀ việc của lời chấm; gọi nó là "từ mới"
 * thì phần sửa lỗi ngữ pháp không bao giờ tới được bé.
 */
export function gocBienHinh(w) {
  const s = String(w || '');
  const ra = [];
  if (s.endsWith("'s") && s.length > 3) ra.push(s.slice(0, -2));
  if (s.endsWith('ies') && s.length > 4) ra.push(`${s.slice(0, -3)}y`);
  if (s.endsWith('es') && s.length > 3) ra.push(s.slice(0, -2));
  if (s.endsWith('s') && s.length > 2) ra.push(s.slice(0, -1));
  if (s.endsWith('ing') && s.length > 4) ra.push(s.slice(0, -3), `${s.slice(0, -3)}e`);
  if (s.endsWith('ed') && s.length > 3) ra.push(s.slice(0, -2), s.slice(0, -1));
  return ra;
}

export function chuLa(cau, { vonTu = [], mauCau = [], beViet = '' } = {}) {
  const kho = new Set();
  for (const v of vonTu) chuTiengAnh(typeof v === 'string' ? v : v?.tu).forEach((w) => kho.add(w));
  for (const m of mauCau) chuTiengAnh(m).forEach((w) => kho.add(w));
  /* ── CHỮ CHÍNH BÉ VỪA VIẾT ──
     Câu sửa là câu bé viết được viết lại cho đúng, nên những chữ bé vừa dùng không
     thể là "chữ bé chưa học" — hàng rào này dựng lên để chặn mô hình DẠY từ mới,
     không phải để chặn nó nhắc lại từ bé vừa viết. Bỏ vế này thì ở Unit 1 cả
     `the` · `at` · `school` · `gate` — bốn chữ bé tự gõ ra — đều bị kể là chữ lạ,
     và mọi câu sửa đều rơi. */
  for (const w of chuTiengAnh(beViet)) kho.add(w);
  return chuTiengAnh(cau)
    .filter((w) => !kho.has(w) && !gocBienHinh(w).some((g) => kho.has(g)));
}

/** Dấu tiếng Việt — dấu hiệu chắc chắn nhất một mẩu chữ là lời Việt, không phải câu Anh. */
export const CO_DAU_VIET = /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i;

/**
 * Chữ lạ trong một câu TIẾNG VIỆT có lẫn tiếng Anh (lời gợi ý, lời giải thích).
 *
 * ⚠ ĐỪNG đem cả câu đi so với vốn từ tiếng Anh. "Con thử viết thêm câu cảm ơn:
 * Thank you." — mọi chữ Việt trong đó (`con` · `thu` · `viet` · `them`…) đều "không
 * có trong vốn từ", và lời gợi ý ĐÚNG lại bị bỏ. Đã sập ngay trong lượt thử đầu.
 */
export function chuLaTrongViet(cau, kho) {
  const mau = String(cau || '').split(/[:.;“”"'()\n]|(?:\s-\s)/);
  const ra = [];
  for (const m of mau) {
    const s = m.trim();
    if (!s || CO_DAU_VIET.test(s) || !/[a-z]/i.test(s)) continue;
    ra.push(...chuLa(s, kho));
  }
  return [...new Set(ra)];
}

/**
 * MỌI CHỮ LẠ TRONG CẢ MỘT LỜI CHẤM — thứ mắt xích 2 của V4 cần để biết có phải
 * gọi lại hay không.
 *
 * Soi đúng những trường mà máy con cũng soi (`soiLoiCham`): `loi[].sua` là TIẾNG
 * ANH, còn `goiY` · `khen` · `viSao` là tiếng Việt có lẫn tiếng Anh.
 */
export function chuLaTrongCham(cham, kho = {}) {
  const ra = [];
  for (const l of (cham?.loi || [])) {
    ra.push(...chuLa(l?.sua, kho));
    ra.push(...chuLaTrongViet(l?.viSao, kho));
  }
  ra.push(...chuLaTrongViet(cham?.goiY, kho));
  ra.push(...chuLaTrongViet(cham?.khen, kho));
  return [...new Set(ra.filter(Boolean))];
}
