/**
 * SỔ TIẾN ĐỘ CỦA VỎ — gộp một môn vào sổ chung, giữ nguyên các môn còn lại.
 *
 * Vỏ giữ sổ của TỪNG môn trong một khối duy nhất (`{ toan: …, tienganh: … }`) để kệ
 * sách và sổ bố mẹ cùng vẽ lại khi con học xong một bài. Hình dạng bên trong mỗi ô
 * là chuyện riêng của môn — ở đây không được soi vào.
 *
 * ── LUẬT SỐNG CÒN: KHÔNG ĐỔI THÌ TRẢ NGUYÊN KHỐI CŨ ──
 * Môn trả về đúng cái sổ nó vừa nhận nghĩa là "lần này chẳng có gì đổi". Khi ấy hàm
 * này phải trả về nguyên `soCu`, tuyệt đối đừng dựng `{ ...soCu }`.
 *
 * Dựng khối mới thì React thấy sổ đã đổi và vẽ lại cả vỏ; vẽ lại thì hàm `datTienDo`
 * truyền xuống môn cũng là hàm mới; mà trong phòng học có một effect canh đúng hàm
 * ấy để ghi chỗ con đang học dở — hàm mới là nó chạy lại, lại gọi vào đây, lại vẽ.
 * Vòng ấy không có đáy: máy quay hết công suất, localStorage bị ghi hàng nghìn lần
 * một giây, và React chỉ kêu "Maximum update depth exceeded" ở console — màn hình
 * thì vẫn trông bình thường, nên không mở console ra soi là không ai biết.
 *
 * @param {object} soCu   sổ chung hiện tại, khoá theo mã môn
 * @param {string} ma     mã môn đang ghi
 * @param {*} f           sổ mới của môn, hoặc hàm (sổ cũ của môn) → sổ mới
 */
export function gopTienDoMon(soCu, ma, f) {
  const truoc = soCu[ma];
  const sau = typeof f === 'function' ? f(truoc) : f;
  return sau === truoc ? soCu : { ...soCu, [ma]: sau };
}
