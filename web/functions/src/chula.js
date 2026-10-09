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
export function chuLa(cau, { vonTu = [], mauCau = [] } = {}) {
  const kho = new Set();
  for (const v of vonTu) chuTiengAnh(typeof v === 'string' ? v : v?.tu).forEach((w) => kho.add(w));
  for (const m of mauCau) chuTiengAnh(m).forEach((w) => kho.add(w));
  return chuTiengAnh(cau).filter((w) => !kho.has(w));
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
