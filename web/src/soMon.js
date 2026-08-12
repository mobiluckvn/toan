/**
 * SỔ ĐĂNG KÝ MÔN — nơi DUY NHẤT trong cả kho biết có những môn nào.
 *
 * Đặt ở tầng VỎ (`src/`), không đặt trong `chung/`, và đó là chủ ý: `chung/` phải MÙ
 * hẳn về môn. Kệ sách, bảng xếp hạng, sổ bố mẹ, bảng cô giáo đều nằm ở `chung/` — chỉ
 * cần một trong bốn màn ấy gọi thẳng vào Toán là chúng vĩnh viễn không dựng nổi môn
 * thứ hai, và thêm môn lần nào cũng phải sửa cả bốn. Cổng `ranh_gioi.test.mjs` chặn
 * đúng đường ấy.
 *
 * ── GIAO ƯỚC MỘT MÔN PHẢI NỘP ──
 * Bốn màn chung KHÔNG được biết gì hơn những trường dưới đây về bất kỳ môn nào:
 *
 *   ma          mã môn, khớp trường `mon` trong data/chuong_trinh.json
 *   ten         tên đọc được
 *   bieuTuong   biểu tượng hiện trên kệ sách
 *   dangCo      false thì môn chưa hiện ra (đang biên soạn)
 *   Man         component vẽ MỌI màn của môn; vỏ chỉ dựng nó rồi tránh ra.
 *               Nhận `quyen` là MÃ CHUỖI ('ta1'), KHÔNG phải mục chương trình —
 *               `App.jsx` gọi `setQuyen(ma)`. Dùng thẳng như một object thì màn
 *               chính của quyển hiện rỗng mà không cổng nào báo.
 *
 *   napTienDo()              → sổ tiến độ của môn (đọc tại máy). Vỏ giữ trong state
 *                              để mọi màn cùng vẽ lại, nhưng KHÔNG BAO GIỜ soi vào
 *                              bên trong — với vỏ nó chỉ là một khối đục.
 *   tienDoQuyen(tienDo, ct)  → {xong, tong, phanTram, gio}  cho kệ sách
 *                              `ct` là CẢ MỤC chương trình (có `ma`, `soBai`, `bai`),
 *                              không phải mã. Dòng này trước ghi là `ma`, và môn
 *                              Tiếng Anh làm theo lời ghi nên kệ sách hiện "0 unit"
 *                              cho quyển 16 bài. Cổng chỉ soi TÊN hàm nên không bắt được.
 *   hocBa(tienDo)            → Promise<HocBaMon>            cho sổ bố mẹ
 *   hocBaCuaEm(uid)          → Promise<HocBaMon>            cho bảng cô giáo
 *   bangXepHang()            → Promise<doc|null>            cho bảng xếp hạng
 *
 * `HocBaMon` là hình dạng CỐ ĐỊNH, môn nào cũng phải nộp đúng khuôn:
 *   { quyen: [{ma, ten, tongBai, datBai, phanTram, tongChuong, masterChuong,
 *               huyHieu, daBatDau, chuong: [...], canCoGang: [...]}],
 *     chuDe: {mang, dem, tong} | null,
 *     trinhDo: {quyen, tongBaiDat, tongChuongMaster, bacChuDe, soChuDeDoDuoc} }
 */
import toan from './mon/toan/index.js';
import tienganh from './mon/tienganh/index.js';

/** Mọi môn đã khai. Môn `dangCo: false` vẫn ở đây nhưng không hiện ra cho bé. */
export const MON_TAT_CA = [toan, tienganh];

/** Môn đang mở cho bé học. */
export const MON = MON_TAT_CA.filter((m) => m.dangCo !== false);

export const monCua = (ma) => MON.find((m) => m.ma === ma) || MON[0];
