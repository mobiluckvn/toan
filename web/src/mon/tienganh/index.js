/**
 * CỬA CỦA MÔN TIẾNG ANH — nơi DUY NHẤT tầng vỏ được nhìn vào.
 *
 * Mọi thứ khác trong `mon/tienganh/**` là ruột: vỏ app và bốn màn tổng (kệ sách ·
 * bảng xếp hạng · sổ bố mẹ · bảng cô giáo) không được import thẳng vào đó, cổng
 * `ranh_gioi.test.mjs` chặn. Giao ước đầy đủ ghi ở `src/soMon.js`.
 *
 * ── QUYỂN ĐẦU TIÊN: TIẾNG ANH LỚP 1 ──
 * 16 unit · 395 câu luyện tập · 80 câu sát hạch · 333 clip âm.
 * Sinh từ `data/ban_do_tieng_anh.json` + `data/tienganh/lop1_bu.json` bằng
 * `tools/chuan_tienganh.py` → `tools/sinh_bai_tienganh.py`. ĐỪNG sửa tay tệp bài
 * trong `public/content/ta1/` — chạy lại bộ sinh, nếu không lần dựng sau mất hết.
 *
 * ── BỐN CHỖ CỐ Ý KHÔNG DÙNG CHUNG VỚI TOÁN ──
 *   1. `lib/cham.js`      bộ chấm riêng. `flow.js` bỏ chấm đáp án dài quá 26 ký tự,
 *                         mà câu dài nhất của lớp 1 là 46 — bê nguyên là bé mất ô nhập.
 *   2. `lib/progress.js`  khoá sổ riêng `ttd5.tienganh.v1`, tách theo chỗ.
 *   3. bktUnit            `UNIT:n@TA1` — kèm mã quyển, không thì huy hiệu lây quyển.
 *   4. không figureSpec   hình là emoji đi thẳng cùng từ; figforge chỉ dựng sơ đồ toán.
 */
import ManTiengAnh from './components/ManTiengAnh.jsx';
import { napTienDo, luuTienDo, gopTienDo, soRong } from './lib/progress.js';
import { quyenHoc, tienDoQuyen, hocBaTu } from './lib/hocba.js';
import {
  tienDoTuMay, bangXepHang as xepHangTA, lamMoiBangXepHang, soMayChu, lamMoiSoMayChu,
  nhatKyCuaEm,
} from './lib/duLieu.js';

export default {
  ma: 'tienganh',
  ten: 'Tiếng Anh',
  bieuTuong: '🔤',

  dangCo: true,
  Man: ManTiengAnh,

  napTienDo,
  luuTienDo,
  gopTienDo,
  /* Đọc sổ trên máy chủ rồi để `gopTienDo` trộn với sổ tại máy — bản nào MỚI HƠN
     thắng, từng bài một. Hỏng mạng hay chưa deploy luật thì trả rỗng: bé vẫn học
     bằng sổ tại máy, đó mới là nguồn chính. */
  napTuMay: async (uid) => ({ ...soRong(), ...(await tienDoTuMay(uid)) }),

  dsQuyen: quyenHoc,
  tienDoQuyen,
  hocBa: async (tienDo) => hocBaTu(tienDo),
  /* Cô giáo xem một em: đọc sổ của em trên máy chủ rồi dựng học bạ bằng ĐÚNG hàm
     sổ bố mẹ dùng — hai màn không được kể hai câu chuyện khác nhau về cùng một bé. */
  hocBaCuaEm: async (uid) => {
    const tienDo = { ...soRong(), ...(await tienDoTuMay(uid)) };
    return { ...hocBaTu(tienDo), tienDo };
  },

  /* Bảng xếp hạng dùng CHUNG tài liệu `bangXepHang/global` với Toán — thêm bảng
     thứ hai là mở thêm một lối rò dữ liệu bé. Trong tài liệu ấy mỗi môn một bảng. */
  bangXepHang: xepHangTA,
  lamMoiBangXepHang,
  /* Sổ học máy chủ là MỘT tài liệu cho cả hai môn — xem `lib/duLieu.js`. */
  soMayChu,
  lamMoiSoMayChu,
  bangCoGiao: async () => null,
  lamMoiBangCoGiao: async () => {},
  nhatKyCuaEm,

  napBanDoDang: async () => ({}),
  tenDang: (ma) => ma,
  dangCuaBai: () => [],
};
