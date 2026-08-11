/**
 * CỬA CỦA MÔN TIẾNG ANH — khung rỗng, chưa có nội dung.
 *
 * Dựng sẵn để hai việc thành sự thật ngay từ bây giờ, chứ không phải một lời hứa:
 *
 *   1. cổng `ranh_gioi.test.mjs` có hai môn để mà so, nên nó chặn được đường đi tắt
 *      giữa hai môn NGAY LÚC NÀY — không đợi tới khi có nội dung mới dựng hàng rào,
 *      lúc ấy thì đã có sẵn vài đường tắt để mà tranh cãi;
 *   2. giao ước ở `src/soMon.js` được một môn thứ hai kiểm chứng. Một giao ước chỉ
 *      có đúng một bên thực hiện thì chưa phải giao ước, mới là mô tả cách bên ấy làm.
 *
 * `dangCo: false` nên môn này KHÔNG hiện ra cho bé. Kệ sách vẫn chỉ có Toán.
 *
 * ── VIỆC CÒN LẠI, THEO THỨ TỰ ──
 * Đọc `docs/khao_sat_ban_do_tieng_anh.md` và `docs/khao_sat_tieng_anh.md` trước.
 *   · bản đồ tri thức đã có: `data/ban_do_tieng_anh.json` (3 989 node, lớp 1-12)
 *   · nên bắt đầu từ LỚP 4 và 5 — hai lớp duy nhất đủ 100% nghĩa Việt và 100% IPA
 *   · phải quyết ÂM THANH trước khi bóc tách, vì nó đổi hình dạng dữ liệu
 *   · bộ chấm riêng (`lib/cham.js`), KHÔNG đụng `mon/toan/lib/flow.js`
 *   · collection riêng (`attemptsTA` · `progressTA` · `hocBaTA`), KHÔNG dùng chung
 */
export default {
  ma: 'tienganh',
  ten: 'Tiếng Anh',
  bieuTuong: '🔤',

  /** Chưa mở cho bé. Đổi thành `true` khi có quyển đầu tiên. */
  dangCo: false,

  /** Chưa có màn nào. Vỏ không dựng tới vì `dangCo` là false. */
  Man: null,

  /* ── Giao ước: trả về rỗng nhưng ĐÚNG HÌNH DẠNG ──
     Trả `null` hay `undefined` thì bốn màn tổng phải rải `?.` khắp nơi để đỡ; trả
     đúng khuôn rỗng thì chúng vẽ ra "chưa có gì" một cách tự nhiên. */
  napTienDo: () => ({ micros: {} }),
  luuTienDo: () => {},
  gopTienDo: (a) => a,
  napTuMay: async () => ({ micros: {} }),

  dsQuyen: () => [],
  tienDoQuyen: () => ({ xong: 0, dangLam: 0, tong: 0, phanTram: 0, gio: 0 }),
  hocBa: async () => ({ quyen: [], chuDe: null, trinhDo: null }),
  hocBaCuaEm: async () => ({ quyen: [], chuDe: null, trinhDo: null }),
  bangXepHang: async () => null,
  lamMoiBangXepHang: async () => ({ boQua: true }),
  soMayChu: async () => null,
  lamMoiSoMayChu: async () => {},
  bangCoGiao: async () => null,
  lamMoiBangCoGiao: async () => {},
  nhatKyCuaEm: async () => [],
  napBanDoDang: async () => ({}),
  tenDang: (ma) => ma,
  dangCuaBai: () => [],
};
