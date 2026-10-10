/**
 * QUY ĐỔI P(L) SANG THANG CEFR — và nói rõ phép quy đổi này KHÔNG đo cái mà CEFR đo.
 *
 * Chương 2 hứa một con số bậc năng lực. Đây là chỗ làm ra con số ấy, kèm đủ hàng
 * rào để nó không bị đọc thành thứ nó không phải.
 *
 * ── ⚠ ĐIỀU PHẢI ĐỌC TRƯỚC KHI DÙNG SỐ NÀY VÀO LUẬN VĂN ──
 * CEFR định nghĩa bậc bằng MÔ TẢ LÀM ĐƯỢC GÌ ("can-do descriptors"): bé nói được
 * gì với ai, trong tình huống nào. Nó KHÔNG định nghĩa bậc bằng số đơn vị kiến
 * thức đã nắm. Cho nên phép ở đây là một QUY ƯỚC BẮC CẦU hai nhịp:
 *
 *     P(L) của từng nút  →  % phủ vốn của một khối lớp  →  bậc CEFR của khối ấy
 *                        (đo được)                      (do Bộ GD-ĐT ấn định)
 *
 * Nhịp thứ hai KHÔNG phải phép đo của phần mềm này — nó lấy nguyên mục tiêu đã
 * ấn định cho từng khối lớp trong Chương trình GDPT 2018 môn Tiếng Anh (tiểu học
 * lớp 3–5 nhắm Bậc 1 = A1; lớp 1–2 là chương trình làm quen, dưới Bậc 1). Phần
 * mềm chỉ đo được nhịp thứ nhất: bé đã nắm bao nhiêu phần vốn của khối ấy.
 *
 * Vậy câu đọc ĐÚNG là: "con đã vững 34% vốn kiến thức của khối lớp mà chương
 * trình xếp ở bậc A1". Câu đọc SAI là: "con đạt A1". Hàm này trả về đủ số để nói
 * câu đúng, và cố ý KHÔNG trả về bậc khi chưa đủ căn cứ (xem `mucDat`).
 *
 * ── VÌ SAO MẪU SỐ LÀ TOÀN BỘ VỐN CỦA KHỐI, KHÔNG PHẢI SỐ NÚT BÉ ĐÃ CHẠM ──
 * Lấy mẫu số là "số nút đã chạm" thì một bé mới học đúng 5 nút và nắm cả 5 sẽ ra
 * 100% — tức là phép đo thưởng cho việc HỌC ÍT. Phủ vốn phải tính trên toàn khối
 * thì con số mới tăng theo lượng bé thật sự học được.
 *
 * Hệ quả phải chấp nhận: mấy tuần đầu con số sẽ rất nhỏ (1–3%). Đó là số ĐÚNG,
 * không phải lỗi — và màn hình phải bày nó như vậy chứ không làm tròn cho đẹp.
 */

import { nguongThao, mucThaoCua } from './zpd.js';

/**
 * Nút nào được tính vào mẫu số.
 *
 * Đồ thị có cả nút CHỨA (course · theme · unit · review · fun_time) — chúng là
 * ngăn xếp tổ chức, không phải thứ bé nắm hay không nắm. Đếm chúng vào mẫu số là
 * pha nước vào phép đo.
 *
 * ⚠ `'?'` NẰM TRONG DANH SÁCH NÀY LÀ CÓ CHỦ Ý. 79 nút mẫu câu lớp 1 trong đồ thị
 * bị bỏ trống trường `t`. Chúng là kiến thức thật (`sp_g1_u10_1` = "That's a +
 * [Noun]."), loại ra thì mẫu số lớp 1 hụt gần một nửa và % phủ vọt lên giả tạo.
 */
const LOAI_HOC_DUOC = new Set([
  'vocabulary', 'vocabulary_item', 'grammar', 'pronunciation',
  'letter_sound', 'prior_knowledge', '?',
]);

/**
 * Khối lớp → bậc CEFR. Lấy theo Chương trình GDPT 2018, KHÔNG phải phép tự đặt.
 *
 * ⚠ `toiThieuNut` là hàng rào chống con số vô nghĩa: khối lớp 6 trong đồ thị chỉ
 * có 4 nút (vài mục bắc cầu sang cấp hai). Một bé nắm 1 nút sẽ ra "25% A2" —
 * con số ấy nói lên đúng là không có gì. Khối nào dưới ngưỡng thì vẫn hiện nhưng
 * mang cờ `dangTin: false`, và KHÔNG bao giờ được lấy làm `mucDat`.
 */
export const KHOI = [
  { ma: 'preA1', ten: 'Làm quen (dưới A1)', lop: [1, 2], moTa: 'lớp 1–2' },
  { ma: 'A1', ten: 'Bậc 1 — A1', lop: [3, 4, 5], moTa: 'lớp 3–5' },
  { ma: 'A2', ten: 'Bậc 2 — A2', lop: [6], moTa: 'bắc cầu cấp hai' },
];

/** Dưới bằng này nút thì % phủ không đáng tin để kết luận. */
export const TOI_THIEU_NUT = 30;

/**
 * Phủ bao nhiêu phần vốn của khối thì mới gọi là ĐẠT bậc ấy.
 *
 * 0,6 là một LỰA CHỌN, không phải hằng số của CEFR — CEFR không có ngưỡng phần
 * trăm nào cả. Chọn 0,6 vì hai lẽ: (a) đòi 100% thì không bé nào đạt, vì đồ thị
 * chứa cả nút chưa có bài dạy; (b) dưới 0,5 thì "đạt" mà quá nửa vốn còn chưa
 * nắm, nói ra không xuôi. Bác đổi số này thì nhớ là nó đổi NGHĨA của chữ "đạt",
 * không phải đổi độ chính xác của phép đo.
 */
export const PHU_DAT = 0.6;

/**
 * Đo mức phủ vốn theo từng khối.
 *
 * @param dt       đồ thị tri thức (`napDoThi()`), cần `dt.nut`
 * @param mucThao  sổ `mastery/{uid}/units` đã nạp về máy con
 * @param nguong   ngưỡng coi là đã vững một nút (mặc định = ngưỡng thạo của BKT)
 * @returns {{mucDat, banDo, tongNut, tongVung, coSo}}
 *   `mucDat` = khối CAO NHẤT đạt `PHU_DAT` **và** đáng tin, hoặc `null` khi chưa
 *   khối nào đạt. `null` KHÔNG có nghĩa "bé kém" — nghĩa là chưa đủ căn cứ để
 *   nói một bậc, và màn hình phải nói đúng như thế.
 */
export function bacCefr(dt, mucThao, { nguong = nguongThao() } = {}) {
  const nut = dt?.nut || {};
  const banDo = KHOI.map((k) => ({
    ...k, tong: 0, vung: 0, phu: 0, dangTin: false, dat: false,
  }));
  const theoLop = new Map();
  banDo.forEach((b) => b.lop.forEach((g) => theoLop.set(g, b)));

  let coSo = 0;
  for (const [ma, n] of Object.entries(nut)) {
    if (!LOAI_HOC_DUOC.has(n?.t ?? '?')) continue;
    const b = theoLop.get(n?.g);
    if (!b) continue;
    b.tong += 1;
    const p = mucThaoCua(mucThao, ma);
    if (Number.isFinite(p)) {
      coSo += 1;
      if (p >= nguong) b.vung += 1;
    }
  }

  banDo.forEach((b) => {
    b.phu = b.tong ? b.vung / b.tong : 0;
    b.dangTin = b.tong >= TOI_THIEU_NUT;
    b.dat = b.dangTin && b.phu >= PHU_DAT;
  });

  /* Lấy khối ĐẠT cao nhất. Duyệt ngược vì `KHOI` xếp từ thấp lên cao. */
  let mucDat = null;
  for (let i = banDo.length - 1; i >= 0; i -= 1) {
    if (banDo[i].dat) { mucDat = banDo[i]; break; }
  }

  return {
    mucDat,
    banDo,
    tongNut: banDo.reduce((s, b) => s + b.tong, 0),
    tongVung: banDo.reduce((s, b) => s + b.vung, 0),
    coSo,
  };
}

/**
 * Một câu tiếng Việt cho người lớn đọc — và câu này là phần dễ sai nhất của cả
 * tệp, nên nó nằm ngay đây chứ không rải trong .jsx.
 *
 * Quy tắc: KHÔNG BAO GIỜ ghép chữ "con đạt" với tên bậc khi `mucDat` là null.
 * Lúc ấy nói theo khối bé đang học dở, kèm đúng phần trăm thật.
 */
export function cauMoTa(kq) {
  if (!kq || !kq.tongNut) return 'Chưa có dữ liệu để quy đổi.';
  if (kq.mucDat) {
    return `Con đã vững ${Math.round(kq.mucDat.phu * 100)}% vốn của khối ${kq.mucDat.moTa} `
      + `— khối mà chương trình xếp ở ${kq.mucDat.ten}.`;
  }
  const dang = kq.banDo.filter((b) => b.dangTin && b.vung > 0).pop()
    || kq.banDo.find((b) => b.dangTin);
  if (!dang || !dang.vung) {
    return 'Con mới bắt đầu — chưa đủ dữ liệu để nói một bậc năng lực.';
  }
  return `Con đang vững ${dang.vung}/${dang.tong} phần vốn của khối ${dang.moTa} `
    + `(${Math.round(dang.phu * 100)}%). Chưa đủ để nói con đạt ${dang.ten}.`;
}
