/**
 * ĐỒNG HỒ HỌC — đo THỜI GIAN THẬT con ở trong bài, từng bước một.
 *
 * ── VÌ SAO PHẢI VIẾT CÁI NÀY ──
 *
 * Trước nay "số phút con học" suy ra bằng cách cộng KHOẢNG CÁCH giữa hai lượt bấm
 * "Kiểm tra" (`minutesStudied` trong functions/src/report.js), quãng nghỉ quá 5 phút
 * thì bỏ. Phép ấy hợp lý khi bài học là một xấp câu hỏi. Nhưng nay CẢ BỐN QUYỂN đã
 * chuyển sang video: phần giảng là 405 video, cộng lại **390,7 phút**, và không một
 * giây nào trong đó được đếm — vì xem video thì con không bấm gì cả.
 *
 * Hệ quả thật, không phải giả định: con xem trọn video sáu mươi lăm giây rồi trả lời
 * đúng ngay câu chốt thì sổ ghi **học 0 phút**. Con càng chịu khó xem giảng thì sổ
 * càng ghi ít. Hai lỗ nhỏ đi kèm: câu ĐẦU TIÊN của buổi không có khoảng cách đứng
 * trước nên luôn tính 0, và quãng sau câu cuối cũng mất.
 *
 * ── ĐO THẾ NÀO ──
 *
 * Đo theo BƯỚC, không theo lượt trả lời: mỗi lần con rời một bước thì cộng khoảng
 * vừa ở vào đúng tên bước ấy. Nhờ thế bước xem video cũng có số như mọi bước khác.
 *
 * Hai cái chặn, vì "ở trong bài" không đồng nghĩa với "đang học":
 *
 *   · TRẦN MỖI LẦN (`TRAN_MOT_LAN`) — con mở bài rồi đi ăn cơm, hai tiếng sau quay
 *     lại: quãng ấy phải cắt, không thì một buổi ra một trăm hai mươi phút. Cắt ở 5
 *     phút cho khớp đúng ngưỡng quãng nghỉ mà phép cũ vẫn dùng, để hai con số cùng
 *     một cách hiểu về "nghỉ".
 *   · TẠM DỪNG KHI KHUẤT MÀN HÌNH — chuyển sang tab khác thì gọi `roi()`, quay lại
 *     gọi `vao()`. Không có cái này thì trần 5 phút vẫn cho không công mỗi lần con
 *     chuyển tab, mà trẻ con chuyển tab suốt.
 *
 * Ra hai con số tách nhau, vì chúng trả lời hai câu khác nhau:
 *   · `giayXem` — thời gian NHẬN (video, ví dụ mẫu, màn kết)
 *   · `giayLam` — thời gian TRẢ LỜI (câu chốt, luyện tập, sát hạch)
 * Bé xem nhiều mà làm nhanh, với bé bỏ qua video rồi vật lộn ở phần làm, là hai
 * đứa trẻ khác nhau và cần hai cách giúp khác nhau. Cộng chung lại thì mất hẳn.
 */

/** Quãng dài hơn mức này coi như con đã rời đi, không tính. */
export const TRAN_MOT_LAN = 5 * 60 * 1000;

/** Bước nào là NHẬN, bước nào là TRẢ LỜI. Bước lạ coi như nhận. */
const BUOC_LAM = new Set(['check', 'practice', 'assess']);
export const laBuocLam = (b) => BUOC_LAM.has(b);

/**
 * Cộng một quãng vào sổ giờ.
 *
 * Hàm THUẦN: nhận sổ cũ, trả sổ mới. Không đụng đồng hồ máy, nên cổng thử được mọi
 * ngả — kể cả ngả "quãng âm" (con chỉnh lại đồng hồ máy giữa buổi).
 */
export function cong(so, buoc, ms) {
  const d = Math.min(Math.max(Number(ms) || 0, 0), TRAN_MOT_LAN);
  if (!d) return so;
  const cu = so[buoc] || 0;
  return { ...so, [buoc]: cu + d };
}

/** Sổ giờ → hai con số giây, đã làm tròn. */
export function tomTat(so = {}) {
  let xem = 0, lam = 0;
  for (const [buoc, ms] of Object.entries(so)) {
    if (laBuocLam(buoc)) lam += ms; else xem += ms;
  }
  return {
    giay: Math.round((xem + lam) / 1000),
    giayXem: Math.round(xem / 1000),
    giayLam: Math.round(lam / 1000),
  };
}

/**
 * Mã ngày theo giờ VIỆT NAM, để cộng dồn theo ngày.
 *
 * ⚠ Đừng dùng `toISOString()`: nó trả giờ UTC, nên con học lúc 22h tối thứ Ba bị ghi
 * sang thứ Tư. Chuỗi ngày học ("con học liền mấy hôm") đứt oan ngay chỗ ấy, và đó lại
 * đúng giờ nhiều bé ngồi vào bàn.
 */
export const maNgay = (khi = Date.now()) => new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Asia/Ho_Chi_Minh', year: 'numeric', month: '2-digit', day: '2-digit',
}).format(new Date(khi));

/**
 * Đồng hồ có trạng thái, cho màn hình dùng. Bọc quanh `cong` ở trên.
 *
 * `doiBuoc` gọi mỗi lần đổi bước · `roi`/`vao` gọi khi khuất/hiện màn hình ·
 * `chot` gọi lúc nộp bài. Gọi thừa cũng không sao: `roi()` hai lần liên tiếp thì lần
 * sau cộng 0, vì mốc đã bị xoá.
 */
export function dongHo(now = Date.now) {
  let so = {};
  let buoc = null;
  let moc = null;

  const dong = () => {
    if (buoc !== null && moc !== null) so = cong(so, buoc, now() - moc);
    moc = null;
  };
  return {
    doiBuoc(b) { dong(); buoc = b; moc = now(); },
    roi() { dong(); },
    vao() { if (buoc !== null && moc === null) moc = now(); },
    chot() { dong(); return { so: { ...so }, ...tomTat(so) }; },
    doc() { return { ...so }; },
  };
}
