/**
 * HỒ SƠ BÉ — ba thứ hệ thống biết về bé, ngoài "đã xong bài nào".
 *
 * Mục 2.3.1 của luận văn khai hồ sơ người học gồm CEFR hiện tại, sở thích, và
 * định dạng bài tập bé hợp nhất. Sở thích đã làm ở Đợt 0. Hai thứ còn lại ở đây.
 *
 * ── CHIỀU SƯ PHẠM (mục 2.1.2-P) ──
 * Hệ thống có 6 định dạng câu và xoay vòng theo BẬC — nhưng xoay theo luật chung,
 * không theo bé. Bé nào nghe tốt mà gõ chữ kém thì vẫn nhận đúng chừng ấy câu gõ
 * chữ như bạn ngược lại. Đo được điều đó thì mới nói tới thích ứng.
 *
 * Sau Đợt 1, mỗi lượt trả lời đã mang `mode` (chính là `format` của câu). Đây là
 * chỗ cộng chúng lại.
 *
 * ── ⚠ ĐỪNG KẾT LUẬN KHI CHƯA ĐỦ MẪU ──
 * Bé làm 2 câu gõ chữ, sai cả 2 → "bé yếu dạng gõ chữ 0%". Kết luận ấy sai, và
 * sai theo cách nguy: nó dẫn tới việc cho bé ÍT câu gõ chữ đi, nên mẫu không bao
 * giờ lớn thêm, và cái nhãn sai tự nuôi chính nó. Nên mọi phép đọc đều đòi
 * `TOI_THIEU_MAU`, và dưới ngưỡng thì trả `null` — "chưa biết", không phải "kém".
 */

/** Dưới chừng này lượt thì chưa nói được gì về một định dạng. */
export const TOI_THIEU_MAU = 8;

/** Tên đọc được cho bố mẹ. Định dạng lạ thì hiện chính mã, đừng giấu. */
export const TEN_DINH_DANG = {
  chon: 'chọn đáp án',
  the: 'xếp thẻ thành câu',
  go: 'gõ lại chữ',
  tf: 'đúng / sai',
  nghenhin: 'nghe rồi nhìn hình',
  noi: 'nói theo',
};

export const tenDinhDang = (ma) => TEN_DINH_DANG[ma] || String(ma || '—');

/**
 * Cộng một lượt vào hồ sơ. Trả về hồ sơ MỚI, không sửa tại chỗ.
 *
 * `hs` dạng `{ [format]: { dung, tong } }`.
 */
export function ghiDinhDang(hs, format, dung) {
  const k = String(format || '').trim();
  if (!k) return hs || {};
  const cu = (hs || {})[k] || { dung: 0, tong: 0 };
  return {
    ...(hs || {}),
    [k]: { dung: cu.dung + (dung ? 1 : 0), tong: cu.tong + 1 },
  };
}

/** Tỉ lệ đúng của một định dạng, hoặc `null` khi chưa đủ mẫu. */
export function tiLeDung(hs, format) {
  const d = (hs || {})[format];
  if (!d || d.tong < TOI_THIEU_MAU) return null;
  return d.dung / d.tong;
}

/**
 * Xếp hạng các định dạng ĐÃ ĐỦ MẪU, mạnh trước yếu sau.
 * Chưa đủ mẫu thì không có mặt — không xếp hạng thứ mình chưa biết.
 */
export function xepDinhDang(hs) {
  return Object.keys(hs || {})
    .map((k) => ({ ma: k, ten: tenDinhDang(k), ti: tiLeDung(hs, k), tong: hs[k].tong }))
    .filter((x) => x.ti !== null)
    .sort((a, b) => b.ti - a.ti);
}

export const manhNhat = (hs) => xepDinhDang(hs)[0] || null;
export const yeuNhat = (hs) => {
  const ds = xepDinhDang(hs);
  /* Cần ÍT NHẤT HAI định dạng đủ mẫu mới nói được "yếu nhất". Một mình nó thì nó
     vừa mạnh nhất vừa yếu nhất — câu ấy không có nghĩa gì. */
  return ds.length >= 2 ? ds[ds.length - 1] : null;
};

/**
 * CEFR CỦA BÉ — suy từ quyển cao nhất bé đã học xong, không khai tay.
 *
 * `dsQuyen` là danh sách `{ ma, cefr, bai: [...] }` của sổ đăng ký. Một quyển
 * tính là xong khi bé đạt HẾT bài của nó.
 *
 * ⚠ ĐANG HỌC DỞ THÌ KHÔNG TÍNH. Bé mới xong 3/20 bài của quyển A1 mà đã dán nhãn
 * A1 là nói quá về bé — và nhãn ấy đi vào lời dặn LLM, tức là cô giáo máy sẽ nói
 * với bé bằng vốn từ bé chưa có.
 */
export function cefrCuaBe(tienDo, dsQuyen) {
  const xong = (dsQuyen || []).filter((q) => {
    const bai = q?.bai || [];
    return bai.length > 0 && bai.every((id) => tienDo?.micros?.[id]?.pass);
  });
  if (!xong.length) return null;
  /* Quyển sau trong sổ đăng ký là quyển cao hơn — thứ tự ấy do `thuTu` của sổ
     quyết, không phải do so chuỗi 'Pre-A1' với 'A1' (so chuỗi thì 'A1' < 'Pre-A1'
     theo bảng chữ cái, tức là ngược hẳn). */
  return xong[xong.length - 1]?.cefr || null;
}
