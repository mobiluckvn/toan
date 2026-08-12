/**
 * DẪN DẮT — luật "đi lần lượt", để riêng khỏi giao diện.
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Quyển này mở ra là thấy cả 16 bài, bài nào bấm cũng vào. Bé 6 tuổi bấm bài 16
 * trước bài 1 không phải vì nghịch — nó chưa đọc được tên bài, thấy ô nào cũng
 * như nhau. Mà 16 unit này dựng chồng lên nhau: chưa có `a`/`the` của unit 1 thì
 * unit 16 chỉ là những chữ lạ. Bỏ qua bài không phải đi nhanh, là đi hụt.
 *
 * Toán lớp 5 đã có cờ `khoaBai` và luật "bài trước ĐẠT thì bài sau mở". Môn này
 * đi theo, nhưng KHÔNG import sang `mon/toan/` — hai môn không được với vào ruột
 * nhau (cổng `ranh_gioi` gác). Chép luật thì rẻ hơn là mở một lối đi giữa hai môn
 * mà sau này không ai dám đóng lại.
 *
 * ── MỘT LUẬT DUY NHẤT, DÙNG CHO CẢ BA TẦNG ──
 *
 *     ĐI TIẾP ĐƯỢC KHI: đã ĐẠT — hoặc đã THỬ THẬT ít nhất 2 lần.
 *
 * Vế sau mới là vế quan trọng. Khoá cứng theo "phải đạt" thì bé nào tắc ở unit 7
 * là tắc vĩnh viễn: không qua được thì không có bài nào khác để học, và cái bé
 * học được ở lớp 1 không phải tiếng Anh mà là "mình học dốt". Cho qua ngay lần
 * đầu thì lại thành không khoá gì cả.
 *
 * Hai lần là chỗ đứng giữa: đủ để chắc bé đã THỬ chứ không phải bấm cho xong, mà
 * không đủ để thành hình phạt. Và bài đi vòng ấy KHÔNG được ghi là đạt — nó nằm
 * lại trong danh sách "còn nợ", có nhãn riêng, bấm vào làm lại lúc nào cũng được.
 *
 * Con số này dùng lại nguyên vẹn ở ba chỗ: mở bài sau · mở chặng sau · bỏ qua một
 * câu. Ba chỗ cùng một luật thì bé học được luật ấy một lần rồi áp dụng ở mọi
 * chỗ, thay vì mỗi màn một kiểu.
 */
import { NHAN_TRANG_THAI_BAI } from '../../../chung/lib/nhanHocBa.js';

export { NHAN_TRANG_THAI_BAI as NHAN_TRANG_THAI };

/** Số lần THỬ THẬT tối thiểu trước khi được đi vòng qua. Xem đầu tệp. */
export const THU_TOI_THIEU = 2;

/** Đã thử đủ số lần để được đi tiếp dù chưa đạt chưa? */
export const daThuDu = (m) => (m?.attempts || 0) >= THU_TOI_THIEU;

/* ═══════════ TẦNG 1 · MỘT BÀI TRONG QUYỂN ═══════════ */

/**
 * Bài này đã mở chưa?
 *
 * `ds` là danh sách mã bài THEO ĐÚNG THỨ TỰ HỌC (`ct.bai`). Truyền danh sách rỗng
 * thì mọi bài đều đóng — chủ ý: thà không vào được bài nào và thấy ngay là hỏng,
 * còn hơn mở toang cả quyển vì nạp chỉ mục lỗi.
 */
export function moBai(tienDo, id, ds = []) {
  const i = ds.indexOf(id);
  if (i < 0) return false;
  if (i === 0) return true;                      // bài đầu luôn mở
  const truoc = tienDo?.micros?.[ds[i - 1]];
  return !!truoc?.pass || daThuDu(truoc);
}

/**
 * Trạng thái hiện lên màn của một bài. Dùng ĐÚNG năm tên mà `chung/nhanHocBa.js`
 * đã đặt, để sổ bố mẹ và bảng cô giáo in ra cùng một thứ tiếng với màn học.
 *
 *   dat     đã qua sát hạch
 *   dangDo  đang học dở, còn chặng đánh dấu
 *   chuaDat đã làm hết mà chưa đủ điểm  → đây là chỗ bé cần quay lại
 *   mo      học được ngay
 *   khoa    chưa tới lượt
 */
export function trangThaiBai(tienDo, id, ds = [], { khoaBai = true } = {}) {
  const m = tienDo?.micros?.[id];
  if (m?.pass) return 'dat';
  if (m?.done) return 'chuaDat';
  if (m?.chang > 0) return 'dangDo';
  if (khoaBai && !moBai(tienDo, id, ds)) return 'khoa';
  return 'mo';
}

/**
 * Bài bé NÊN học tiếp — thứ mà trang chính chỉ mũi tên vào.
 *
 * Thứ tự ưu tiên, và thứ tự này có lý do:
 *   1. bài đang học DỞ   → về đúng chỗ cũ, không bắt làm lại từ đầu
 *   2. bài đầu tiên CHƯA ĐẠT mà đã mở  → gồm cả bài đi vòng còn nợ
 *   3. hết  → quyển đã xong
 *
 * Điểm 2 gộp "chưa từng học" với "học rồi mà chưa qua" vào một chỗ, và đó là chủ
 * ý: với bé thì cả hai đều là "bài mình chưa làm được", không cần phân biệt.
 */
export function baiNenHoc(tienDo, ds = [], opt = {}) {
  const tt = (id) => trangThaiBai(tienDo, id, ds, opt);
  return ds.find((id) => tt(id) === 'dangDo')
      ?? ds.find((id) => tt(id) === 'chuaDat' || tt(id) === 'mo')
      ?? null;
}

/** Bài đã mở mà chưa đạt — danh sách "còn nợ" hiện cho bé và bố mẹ. */
export const baiConNo = (tienDo, ds = [], opt = {}) =>
  ds.filter((id) => ['chuaDat', 'dangDo'].includes(trangThaiBai(tienDo, id, ds, opt)));

/* ═══════════ TẦNG 2 · CÁC CHẶNG TRONG MỘT BÀI ═══════════ */

/**
 * Chuỗi chặng của một bài. Bài nào có kịch bản hội thoại thì có thêm chặng NÓI
 * CHUYỆN; hỏi chính dữ liệu bài chứ không đếm số cứng, vì không phải bài nào cũng
 * có, và cắm số 5 vào đây là lúc thêm bài không có hội thoại thì lệch hết.
 */
export const NHAN_CHANG = {
  tu: 'Từ mới', cau: 'Mẫu câu', luyen: 'Luyện tập',
  noi: 'Nói chuyện', sat: 'Sát hạch',
};

export function changCua(bai) {
  const coNoi = !!bai?.knowledgeCore?.hoiThoai?.luot?.length;
  return ['tu', 'cau', 'luyen', ...(coNoi ? ['noi'] : []), 'sat'];
}

/**
 * Trạng thái một chặng trên thanh điều hướng.
 *
 *   xong  đã làm qua  → bấm vào LÀM LẠI được, và làm lại không mất chặng sau
 *   dang  đang ở đây
 *   khoa  chưa tới
 *
 * Chỗ này từng sai theo kiểu khó thấy: bản cũ chỉ giữ MỘT con số `tai`, và nút
 * trên thanh khoá theo `i > tai`. Nghĩa là bé đang ở chặng 4, quay lại chặng 1
 * nghe lại từ mới, thì chặng 2·3·4 khoá lại hết — muốn về chỗ cũ phải làm lại cả
 * bài. Quay lại ôn là việc TỐT, mà app lại phạt. Nên phải có HAI con số: đang
 * đứng ở đâu (`tai`), và đã đi xa nhất tới đâu (`xa`).
 */
export function trangThaiChang(i, tai, xa) {
  if (i === tai) return 'dang';
  return i <= xa ? 'xong' : 'khoa';
}

/* ═══════════ TẦNG 3 · MỘT CÂU ═══════════ */

/**
 * Được bỏ qua câu này chưa? `lan` là số lần bé ĐÃ NỘP và sai.
 *
 * Thang ba nấc, và ba nấc là cố ý:
 *
 *   sai lần 1        → chỉ bảo thử lại. Bé chưa kịp nghĩ.
 *   sai lần 2        → hiện GỢI Ý. Đây là nấc `THU_TOI_THIEU`: đã thử thật.
 *   sai lần 3 trở đi → hiện đáp án, và cho để lại sau.
 *
 * Nếu mở nút bỏ qua ngay ở nấc 2 thì gợi ý và đáp án hiện CÙNG LÚC — không bé nào
 * đọc gợi ý khi đáp án nằm ngay bên cạnh, và cái nấc gợi ý coi như không tồn tại.
 * Nên phải để bé có đúng một lượt được thử VỚI gợi ý trong tay.
 *
 * Vẫn đúng lời "ít nhất 2 lần": đây là 3, mà 3 thì nhiều hơn 2.
 *
 * Câu bỏ qua bị ĐẾM lại — xem `conNoTrongMuc` — để cuối mức bé được mời làm lại
 * đúng những câu ấy.
 */
export const HIEN_GOI_Y = THU_TOI_THIEU;
export const duocBoQua = (lan) => lan > THU_TOI_THIEU;

/** Trong một mức luyện tập: những câu bé bỏ qua, để mời làm lại. */
export const conNoTrongMuc = (ketQua = []) => ketQua.filter((k) => k?.boQua).map((k) => k.id);

/* ═══════════ KỲ ÔN TẬP CHƯƠNG ═══════════ */

/**
 * Kỳ ôn tập chương đã mở chưa?
 *
 * Ở đây KHÔNG có cửa "thử 2 lần" như khi mở bài. Cố ý: mở bài là để bé còn có
 * đường đi tiếp khi tắc; còn kỳ ôn tập là chỗ CHỐT một chương và ghi vào học bạ.
 * Cho vào khi còn bốn bài chưa đạt thì huy hiệu ấy không nói lên điều gì, mà đó
 * lại đúng là thứ bố mẹ nhìn vào để tin.
 *
 * Bé đi vòng qua vài bài vẫn học tiếp được bình thường — chỉ là muốn lấy huy hiệu
 * thì phải quay lại làm cho xong những bài còn nợ. Đó là chỗ món nợ được đòi.
 */
export const moKyOnTap = (tienDo, dsBai = []) =>
  dsBai.length > 0 && dsBai.every((id) => tienDo?.micros?.[id]?.pass);

/** Còn mấy bài nữa thì mở được kỳ ôn tập — để nói cho bé biết còn bao xa. */
export const conThieuChoOnTap = (tienDo, dsBai = []) =>
  dsBai.filter((id) => !tienDo?.micros?.[id]?.pass).length;
