import { layNguong, boNguong } from '../../../chung/lib/nguong.js';
/**
 * NÚT THIẾU CÂU — NG20 "số câu hỏi tối thiểu mỗi nút" (Bảng 4.7, điểm 6).
 *
 * Trước 22-11 NG20 nằm trong bảng ngưỡng, hiện trên màn chuyên gia, mà KHÔNG CHỖ NÀO
 * ĐỌC — đổi nó không đổi được gì. Một ngưỡng không ai đọc thì tệ hơn không có: chuyên
 * gia tưởng mình vừa siết chất lượng kho câu, còn hệ thống vẫn y nguyên.
 *
 * Nay nó có hai chỗ đọc:
 *   · cổng soát kho `nguong_ng20.test.mjs` — đếm câu mỗi nút trên NỘI DUNG THẬT và
 *     in danh sách nút dưới NG20 (đúng phép đếm "nút dưới 4 câu" của bảng đối chiếu);
 *   · `dungPhuDao` — lúc gom câu tĩnh cho nút gốc rễ, kho của nút ấy dưới NG20 thì
 *     bài phụ đạo mang cờ `thieuCau`, để màn hình và nhật ký biết bài ấy dựng trên một
 *     kho mỏng (và vì sao nó phải nhờ tới mô hình).
 *
 * ── PHÉP ĐẾM ──
 * Cùng luật với `tools/doi_chieu_v4.py`: một câu là một đối tượng có `id` và
 * (`format` hoặc `answerKey`); nó tính cho MỌI nút trong `maNutDs`, hoặc cho `maNut`
 * khi không có `maNutDs`. Chỉ nút CÓ trong đồ thị, và bỏ nút phát âm `ph_*` (chúng
 * dạy bằng nghe – nói, không bằng câu hỏi). Lệch luật với bảng đối chiếu là hai con
 * số "nút thiếu câu" khác nhau cùng đội một tên.
 */

/** NG20 đọc LÚC GỌI, kèm ngữ cảnh (thường là `{ nut }`). */
export const soCauToiThieuMoiNut = (nc) => layNguong(boNguong(), 'NG20', nc);

/** Duyệt mọi câu trong một cây dữ liệu bài (bài, mảng bài, hay cả tệp). */
export function* moiCauTrong(x) {
  const hang = [x];
  while (hang.length) {
    const y = hang.pop();
    if (Array.isArray(y)) { hang.push(...y); continue; }
    if (!y || typeof y !== 'object') continue;
    if (y.id && (y.format || y.answerKey)) yield y;
    for (const v of Object.values(y)) if (v && typeof v === 'object') hang.push(v);
  }
}

/** Đếm câu theo nút: `Map<maNut, số câu>`. */
export function demCauTheoNut(nguon) {
  const dem = new Map();
  for (const c of moiCauTrong(nguon)) {
    const ds = Array.isArray(c.maNutDs) && c.maNutDs.length ? c.maNutDs : (c.maNut ? [c.maNut] : []);
    for (const m of ds) dem.set(m, (dem.get(m) || 0) + 1);
  }
  return dem;
}

/**
 * Những nút có câu mà CHƯA ĐỦ NG20 câu.
 *
 * @param dt     đồ thị (`dt.nut`). Thiếu đồ thị thì xét mọi mã gặp được.
 * @param nguon  bài, mảng bài, hay cả tệp nội dung
 * @param toiThieu  ghi đè NG20 (cho quét lưới); bỏ trống = đọc NG20 theo từng nút
 * @returns `[{ ma, co, can }]`, thiếu nhiều nhất đứng trước
 */
export function nutThieuCau(dt, nguon, { toiThieu = null } = {}) {
  const ra = [];
  for (const [ma, co] of demCauTheoNut(nguon)) {
    if (dt?.nut && !dt.nut[ma]) continue;
    if (ma.startsWith('ph_')) continue;
    const can = toiThieu ?? soCauToiThieuMoiNut({ nut: ma });
    if (co < can) ra.push({ ma, co, can });
  }
  return ra.sort((a, b) => (a.co - b.co) || a.ma.localeCompare(b.ma));
}

/**
 * Kho câu của MỘT nút có mỏng hơn NG20 không — chỗ `dungPhuDao` gọi.
 * Trả `{ ma, co, can }` khi thiếu, `null` khi đủ (hoặc không có nút).
 */
export function canhBaoThieuCau(baiDs, maNut) {
  if (!maNut) return null;
  const co = demCauTheoNut(baiDs).get(maNut) || 0;
  const can = soCauToiThieuMoiNut({ nut: maNut });
  return co < can ? { ma: maNut, co, can } : null;
}
