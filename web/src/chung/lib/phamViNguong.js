/**
 * CÁC PHẠM VI MÀN CHUYÊN GIA CHỌN ĐƯỢC — Bảng 4.7, điểm 2.
 *
 * Trước 22-11 màn quản lý ngưỡng chỉ sửa được giá trị `toanHe`, trong khi cả thang
 * phạm vi (mục 3.8.1) và máy chủ đã hiểu đủ bảy nấc. Tức là chuyên gia muốn nới θ
 * cho riêng khối lớp 1 thì vẫn phải nhờ người viết mã ghi thẳng vào Firestore —
 * đúng câu "phải nhờ người viết mã" mà R7 sinh ra để bỏ.
 *
 * ── VÌ SAO DANH SÁCH KHOÁ NẰM Ở ĐÂY, KHÔNG ĐỌC TỪ `mon/**` ──
 * Cổng `ranh_gioi` không cho `chung/**` với vào ruột một môn. Nên dạng câu của hai môn
 * được chép vào đây, và cổng `nguong_bang47` so danh sách này với `TEN_DINH_DANG` của
 * Tiếng Anh — thêm một dạng câu mới mà quên chỗ này là cổng đỏ.
 *
 * ⚠ KHOÁ LUÔN LÀ CHUỖI. Hàm nền dựng ngữ cảnh bằng `String(...)` (`nguCanhLuot`), máy
 *   con cũng thế (`datNguCanh`). Lưu `khoa: 3` dạng số thì luật Firestore so `id` với
 *   một số, và hai phía tra hai kiểu khoá khác nhau.
 */

export const PHAM_VI_CHON = [
  { loai: 'toanHe', ten: 'Toàn hệ thống', khoa: null },
  { loai: 'mon', ten: 'Môn', khoa: [['toan', 'Toán'], ['tienganh', 'Tiếng Anh']] },
  { loai: 'khoiLop', ten: 'Khối lớp',
    khoa: [['1', 'Lớp 1'], ['2', 'Lớp 2'], ['3', 'Lớp 3'], ['4', 'Lớp 4'], ['5', 'Lớp 5']] },
  { loai: 'loaiNut', ten: 'Loại nút (Tiếng Anh)',
    khoa: [['vocabulary', 'từ vựng'], ['vocabulary_item', 'mục từ'], ['grammar', 'mẫu câu'],
           ['pronunciation', 'phát âm'], ['letter_sound', 'chữ cái – âm'],
           ['prior_knowledge', 'kiến thức nền'], ['review', 'ôn tập']] },
  { loai: 'dangCau', ten: 'Dạng câu',
    khoa: [['chon', 'TA · chọn đáp án'], ['the', 'TA · xếp thẻ'], ['go', 'TA · gõ lại chữ'],
           ['tf', 'TA · đúng / sai'], ['nghenhin', 'TA · nghe rồi nhìn hình'], ['noi', 'TA · nói theo'],
           ['so', 'Toán · điền số'], ['bieuthuc', 'Toán · biểu thức'], ['dungsai', 'Toán · đúng / sai'],
           ['chondapan', 'Toán · chọn đáp án'], ['tuluan', 'Toán · tự luận']] },
  /* Hai nấc dưới không có danh sách đóng: bậc là số do người soạn khai, nút là mã
     của đồ thị (hơn nghìn mã). Màn hình cho gõ — và `phamViHopLe` soi trước khi ghi. */
  { loai: 'bac', ten: 'Bậc của câu', khoa: 'go' },
  { loai: 'nut', ten: 'Một nút cụ thể', khoa: 'go' },
];

/**
 * Phạm vi này ghi được không. Trả chuỗi lý do khi KHÔNG, `''` khi được.
 *
 * Khoá không được chứa `/` (mã tài liệu Firestore cấm) và không được rỗng — một khoá
 * rỗng thì `boTuBang` coi dòng ấy là toàn hệ, tức một giá trị định cho một nút lại đè
 * lên cả hệ thống.
 */
export function phamViHopLe(phamVi) {
  const loai = phamVi?.loai || 'toanHe';
  const muc = PHAM_VI_CHON.find((x) => x.loai === loai);
  if (!muc) return `nấc phạm vi lạ: ${loai}`;
  if (loai === 'toanHe') return '';
  const khoa = String(phamVi?.khoa ?? '').trim();
  if (!khoa) return 'chưa chọn khoá cho phạm vi';
  if (/[/\s]/.test(khoa) || khoa.includes('__')) return 'khoá không được chứa dấu /, khoảng trắng hay "__"';
  if (Array.isArray(muc.khoa) && !muc.khoa.some(([k]) => k === khoa)) return `khoá lạ cho ${muc.ten}: ${khoa}`;
  return '';
}

/** Tên đọc được của một phạm vi, cho tiêu đề và lời báo. */
export function tenPhamVi(phamVi) {
  const loai = phamVi?.loai || 'toanHe';
  const muc = PHAM_VI_CHON.find((x) => x.loai === loai);
  if (!muc || loai === 'toanHe') return 'Toàn hệ thống';
  const khoa = String(phamVi?.khoa ?? '');
  const nhan = Array.isArray(muc.khoa) ? (muc.khoa.find(([k]) => k === khoa)?.[1] || khoa) : khoa;
  return `${muc.ten}: ${nhan}`;
}
