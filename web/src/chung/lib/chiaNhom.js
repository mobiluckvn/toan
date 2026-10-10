/**
 * CHIA NHÓM CHO THỬ NGHIỆM CÓ ĐỐI CHỨNG — kịch bản KB4 và KB5 (mục 3.9).
 *
 * Hai kịch bản ấy đều đang dừng ở cùng một chỗ: «cần cờ chia nhóm». KB5 đo tác dụng
 * của việc xếp câu theo vùng phát triển gần; KB4 so các mẫu lời nhắc bằng ΔC. Cả
 * hai đòi chia người học thành nhóm và giữ nguyên nhóm ấy suốt đợt đo.
 *
 * ── ⚠ CHIA TẤT ĐỊNH TỪ MÃ NGƯỜI HỌC, KHÔNG DÙNG `Math.random()` ──
 * Nhóm phải GIỮ NGUYÊN qua mọi phiên, mọi máy, mọi lần tải lại. Random thì bé đổi
 * nhóm mỗi lần mở app, và phép so hai nhóm mất sạch nghĩa — tệ hơn, nó mất nghĩa
 * trong im lặng, vì số liệu vẫn ra đẹp. Băm mã người học cho cùng một câu trả lời
 * ở mọi nơi mà không phải lưu gì.
 *
 * ── ⚠ MỖI THỬ NGHIỆM MỘT HẠT GIỐNG RIÊNG ──
 * Dùng chung một phép băm cho mọi thử nghiệm thì bé ở nhóm A của KB5 cũng luôn ở
 * nhóm A của KB4 — hai phép đo dính vào nhau và không tách được tác dụng của từng
 * thứ. Tên thử nghiệm đi vào phép băm nên hai thử nghiệm chia độc lập.
 *
 * ── ⚠ MẶC ĐỊNH LÀ TẮT, VÀ ĐÓ LÀ CHỦ Ý ──
 * `THU_NGHIEM` khai tỉ lệ của từng thử nghiệm, và cả hai đang để 0 — tức mọi bé đều
 * ở nhóm đối chứng, hệ thống chạy y như trước. Bật một thử nghiệm là một QUYẾT ĐỊNH
 * về việc dạy trẻ, không phải một việc kỹ thuật:
 *
 *   · `kb4_phudao_llm` đẩy một phần bé sang đường mô hình của bài phụ đạo. Câu do
 *     mô hình soạn có đi qua hai tầng hậu kiểm, nhưng tới tay bé TRƯỚC khi người
 *     lớn duyệt — nới chỗ ấy là nới ràng buộc R3. Người quyết định phải là bác.
 *   · `kb5_zpd` tắt phép xếp câu theo vùng phát triển gần cho nhóm đối chứng. Nhóm
 *     ấy học bằng thứ tự thường, tức kém hơn một chút trong suốt đợt đo.
 */

/** Băm chuỗi thành số không dấu — FNV-1a, 32 bit. Đủ đều cho việc chia nhóm. */
function bam(s) {
  let h = 0x811c9dc5;
  const t = String(s || '');
  for (let i = 0; i < t.length; i += 1) {
    h ^= t.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}

/**
 * Tỉ lệ người học vào nhóm THỬ của từng thử nghiệm.
 *
 * 0 = tắt hẳn (mọi bé ở nhóm đối chứng) · 0.5 = chia đôi · 1 = mọi bé vào nhóm thử.
 * Đổi số ở đây là đổi hành vi với trẻ thật — xem khối cảnh báo ở đầu tệp.
 */
export const THU_NGHIEM = {
  /* KB4 — so các mẫu lời nhắc bằng ΔC. TẮT: bật là câu do mô hình soạn tới tay bé
     nhiều hơn hẳn, trong khi hàng đợi duyệt mới chỉ là đường đi SAU đó. */
  kb4_phudao_llm: 0,
  /* KB5 — hiệu quả của việc xếp câu theo vùng phát triển gần. TẮT: nhóm đối chứng
     sẽ học bằng thứ tự thường suốt đợt đo. */
  kb5_zpd: 0,
};

export const NHOM = { thu: 'thu', doiChung: 'doiChung' };

/**
 * Bé này thuộc nhóm nào của một thử nghiệm.
 *
 * Trả `doiChung` khi: thử nghiệm chưa khai · tỉ lệ 0 · chưa biết mã người học. Ba
 * trường hợp ấy đều phải cho ra HÀNH VI CŨ, không phải một nhóm ngẫu nhiên.
 */
export function nhomCua(uid, ten, tiLe = null) {
  const t = tiLe == null ? THU_NGHIEM[ten] : tiLe;
  if (!uid || !t || t <= 0) return NHOM.doiChung;
  if (t >= 1) return NHOM.thu;
  /* Chia theo 10.000 bậc: đủ mịn cho mọi tỉ lệ ta dùng, và không phụ thuộc số thực. */
  return (bam(`${ten}::${uid}`) % 10000) / 10000 < t ? NHOM.thu : NHOM.doiChung;
}

/** Có ở nhóm THỬ của thử nghiệm này không. */
export const laNhomThu = (uid, ten, tiLe = null) => nhomCua(uid, ten, tiLe) === NHOM.thu;

/**
 * Nhãn ghi vào bản ghi lượt để phép đo tách được hai nhóm.
 *
 * ⚠ Chỉ ghi những thử nghiệm ĐANG BẬT. Ghi cả thử nghiệm đã tắt thì mọi dòng nhật
 * ký mang một nhãn vô nghĩa, và sáu tháng sau không ai biết nhãn ấy có hiệu lực
 * trong khoảng thời gian nào.
 */
export function nhanNhom(uid) {
  const ra = {};
  for (const [ten, t] of Object.entries(THU_NGHIEM)) {
    if (t > 0) ra[ten] = nhomCua(uid, ten);
  }
  return Object.keys(ra).length ? ra : null;
}
