/**
 * NHÃN CHUNG CHO HỌC BẠ — chữ hiện lên màn, không thuộc môn nào.
 *
 * Bốn mức của một chương và bốn tình trạng của một chủ đề là NGÔN NGỮ CHUNG mà mọi
 * môn phải nói: sổ bố mẹ và bảng cô giáo vẽ theo chúng. Trước đây hai bảng nhãn này
 * nằm trong `mon/toan/lib/hocba.js`, nên tầng chung phải với sang ruột Toán mới đọc
 * được chữ để in ra.
 */
export const NHAN_MUC_CHUONG = {
  master: 'đã master', xongBai: 'xong bài, chưa qua kỳ sát hạch',
  dangHoc: 'đang học', chuaHoc: 'chưa học',
};

export const NHAN_TINH_TRANG = {
  vung: 'đã vững', dangHoc: 'đang học', canCoGang: 'cần cố gắng', chuaHoc: 'chưa học',
};

/**
 * Năm trạng thái của MỘT BÀI — cũng là ngôn ngữ chung.
 *
 * Việc CHẤM ra trạng thái nào là của môn (mỗi môn một luật mở khoá riêng); còn chữ
 * hiện lên màn thì nằm ở đây, để bảng cô giáo in được mà không phải với sang ruột môn.
 */
export const NHAN_TRANG_THAI_BAI = {
  dat: 'con đã đạt', dangDo: 'đang học dở', chuaDat: 'chưa qua câu bẫy',
  mo: 'học được ngay', khoa: 'chưa mở',
};
