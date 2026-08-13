/**
 * SỔ ĐĂNG KÝ — tầng VỎ của app, KHÔNG thuộc môn nào.
 *
 * Chỉ giữ ba thứ mà mọi môn đều cần và không môn nào được sửa:
 *   · sổ đăng ký QUYỂN (`data/chuong_trinh.json`) — kệ sách dựng hoàn toàn từ đây;
 *   · các lớp con có thể đang học (2 → 12);
 *   · đường dẫn nội dung tĩnh và dấu phiên bản.
 *
 * ⚠ TUYỆT ĐỐI KHÔNG đưa gì của riêng một môn vào đây. Phần nạp bài, chia chương,
 * bản đồ dạng bài… của Toán nằm ở `mon/toan/lib/noiDung.js`. Đó là cả điểm của việc
 * tách: sửa môn này không được đụng tới hành vi môn kia, và cổng `ranh_gioi.test.mjs`
 * chặn mọi đường import qua lại.
 */
const BASE = import.meta?.env?.BASE_URL || '/';
export const CONTENT = BASE.replace(/\/$/, '') + '/content';

/**
 * Dấu phiên bản nội dung — vite.config.js băm public/content rồi dán vào đây.
 * Nội dung để `immutable` 7 ngày mà tên tệp không đổi, nên không có dấu này thì
 * sửa bài xong đẩy lên, máy đã từng mở trang vẫn học bản cũ suốt một tuần.
 * Chạy bằng node (bộ kiểm) thì không có biến, lùi về 'dev' — vô hại.
 */
export const NOI_DUNG_V =
  typeof __NOI_DUNG_V__ === 'string' ? __NOI_DUNG_V__ : 'dev';

/** Gắn dấu phiên bản vào một đường dẫn nội dung */
export const dongDau = (url, v = NOI_DUNG_V) =>
  (v && v !== 'dev' ? `${url}?v=${v}` : url);

/** DL:KSN5Q1.B49.M1 → DL_KSN5Q1_B49_M1 */
export const idToFile = (microId) => microId.replace('DL:', 'DL_').replace(/\./g, '_');

/* ─────────── HAI CHƯƠNG TRÌNH, MỘT BỘ MÃ ───────────
 * Lớp 2 và lớp 5 dùng chung mọi màn hình; khác nhau chỉ ở NỘI DUNG và ở nhịp đọc.
 * Chỗ khai khác biệt duy nhất là data/chuong_trinh.json — đừng rải điều kiện
 * "nếu là lớp 2 thì…" ra khắp các component, vì thêm lớp thứ ba là phải đi sửa lại
 * từng chỗ một.
 */
/* Sổ đăng ký chương trình. Đọc từ content/chuong_trinh.json khi app khởi động; có
   sẵn bản tối thiểu để bộ kiểm chạy bằng node (không có mạng) vẫn dùng được.
   THÊM LỚP/MÔN MỚI thì thêm mục trong data/chuong_trinh.json, KHÔNG sửa tệp này. */
let SO_DK = {
  mon: { toan: { ten: 'Toán', bieuTuong: '🔢' } },
  chuongTrinh: {
    lop2: { ma: 'lop2', mon: 'toan', lop: 2, thuMuc: 'lop2', tienTo: 'DL:KSN2.',
            ten: 'Toán Tư Duy lớp 2', soBai: 33, doc: { chuTo: true } },
    lop5: { ma: 'lop5', mon: 'toan', lop: 5, thuMuc: 'lessons', tienTo: 'DL:KSN5Q1.',
            ten: 'Toán Tư Duy lớp 5', soBai: 168, doc: { chuTo: false } },
  },
  sapCo: [], luyenThi: [],
};

export const soDangKy = () => SO_DK;
export const dsChuongTrinh = () => Object.values(SO_DK.chuongTrinh || {});

/**
 * CÁC LỚP CON CÓ THỂ ĐANG HỌC — lớp 1 đến lớp 12.
 *
 * KHÔNG phải danh sách quyển sách đang có. Hai thứ khác nhau: app mới có sách Toán
 * lớp 2·3·4·5 và Tiếng Anh lớp 1, nhưng anh chị lớp 6-12 vẫn dùng app (ôn lại nền,
 * hoặc chờ sách của mình). Hỏi "con học lớp mấy" mà chỉ cho chọn 4·5·6 thì anh lớp 8
 * phải khai sai ngay ở màn đầu tiên — và con số sai ấy đi thẳng vào bảng xếp hạng
 * ("Bạn nhỏ lớp 5") lẫn vào bậc xuất phát của vòng luyện chủ đề.
 *
 * ── VÌ SAO THÊM LỚP 1 ──
 * Danh sách này mở đầu từ lớp 2 suốt từ đầu, vì quyển nhỏ nhất khi ấy là Toán lớp 2.
 * Nay có Tiếng Anh lớp 1, và bé 6 tuổi là bạn NHỎ NHẤT của app — mà lập hồ sơ lại
 * không khai được đúng lớp mình. Bé phải khai lớp 2, rồi con số sai ấy đi vào bảng
 * xếp hạng và vào bậc xuất phát.
 *
 * Đây đúng loại "ghim cứng theo quyển đang có" mà chính lời chú thích trên đã cảnh
 * báo — và vẫn dính, vì lúc viết thì lớp 2 là biên dưới thật.
 *
 * Để ở đây vì đây là nơi giữ sổ đăng ký; sửa một chỗ, mọi màn theo.
 */
export const LOP_HOC = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

/** Lớp mặc định khi con chưa khai — lấy quyển đầy đủ nhất đang có. */
export const LOP_MAC_DINH = 5;

/** Giữ lớp trong khoảng có thật. Luật Firestore không soi trường này. */
export const lopHopLe = (g) => (LOP_HOC.includes(Number(g)) ? Number(g) : LOP_MAC_DINH);

/**
 * Các quyển theo ĐÚNG THỨ TỰ HIỆN LÊN KỆ SÁCH: lớp 2 → 3 → 4 → 5 → tổng ôn lớp 5.
 *
 * Thứ tự khai trong tệp KHÔNG dùng được: sổ vốn khai theo thứ tự làm xong quyển
 * (lop2, lop5, lop5q2, lop3, lop4), nên kệ sách hiện lớp 5 nằm giữa lớp 2 và lớp 3.
 * Chèn quyển mới vào giữa thì chỉ sửa `thuTu`, không phải chép lại cả sổ.
 *
 * Quyển chưa khai `thuTu` xuống cuối chứ không lên đầu — quyển mới thêm mà quên khai
 * thì nó nằm sau các quyển đã xếp, không đội lên trên đầu kệ.
 */
export const dsChuongTrinhSapXep = () => dsChuongTrinh()
  .slice()
  .sort((a, b) => (a.thuTu ?? 99) - (b.thuTu ?? 99)
                  || String(a.ma).localeCompare(String(b.ma)));
/**
 * GOM KỆ SÁCH THÀNH NHÓM — luật để riêng khỏi giao diện, để cổng chạy được bằng node.
 *
 * Ba việc, và cả ba đều từng hoặc sắp hỏng câm nếu để trong JSX:
 *
 * 1. GOM THEO `nhom`, KHÔNG theo mã môn. Bốn quyển lớp 2·3·4·5 là "Toán cấp 1";
 *    gom theo môn thì tiêu đề chỉ có thể là "TOÁN", và mai kia thêm Toán cấp 2 là
 *    chín quyển đổ chung một đống. Quyển không khai `nhom` rơi về tên môn như cũ.
 *
 * 2. CỬA PHỤ ("Học theo chủ đề") đứng TRONG nhóm nó cắt ngang. Tên nhóm của cửa
 *    khai ở tệp index.js của môn, còn của quyển khai ở sổ đăng ký — HAI NƠI, phải
 *    trùng từng chữ. Lệch một chữ thì cửa rơi ra thành nhóm riêng chỉ có mình nó,
 *    giao diện vẫn vẽ đẹp. Cổng `kesach.test.mjs` canh chỗ này.
 *
 * 3. MỖI NHÓM MỘT CHỖ "HỌC TIẾP". Bản trước có đúng một thẻ cho cả app: bé đang
 *    học dở cả Toán lẫn Tiếng Anh thì một trong hai biến mất khỏi chỗ dễ thấy nhất.
 *
 *    Quyển ấy VẪN NẰM trong danh sách bên dưới. Bản đầu lấy nó ra cho khỏi lặp,
 *    nhưng thế là nhóm Tiếng Anh (mới có một quyển) không còn danh sách lớp nào cả
 *    — mà "chọn bài theo nhu cầu" thì phải NHÌN THẤY đủ các lớp mới chọn được.
 *    Thẻ vàng là LỐI TẮT, danh sách là KỆ SÁCH; bỏ kệ đi để giữ lối tắt là hỏng
 *    đúng cái quan trọng hơn.
 *
 * @param ds    [{ ct, td }] đã xếp theo `thuTu`
 * @param mon   danh sách hồ sơ môn (mỗi môn có `ma` và `cuaPhu`)
 * @param tenMon (ma) => tên môn, để quyển không khai `nhom` có chỗ rơi về
 */
export function gomNhomKeSach(ds = [], mon = [], tenMon = (m) => m, bieuTuongMon = () => '📘') {
  const theoNhom = new Map();
  const lay = (ten, maMon) => {
    if (!theoNhom.has(ten)) {
      theoNhom.set(ten, { ten, bieuTuong: bieuTuongMon(maMon), sach: [], cua: [] });
    }
    return theoNhom.get(ten);
  };
  for (const x of ds) lay(x.ct.nhom || tenMon(x.ct.mon), x.ct.mon).sach.push(x);
  for (const m of mon) {
    for (const c of m.cuaPhu || []) lay(c.nhom || tenMon(m.ma), m.ma).cua.push({ m, c });
  }
  return [...theoNhom.values()].map((nh) => {
    const dangHoc = nh.sach.filter((x) => x.td?.dangLam > 0)
      .sort((a, b) => (b.td.gio || 0) - (a.td.gio || 0));
    return { ...nh, tiep: dangHoc[0] || null };
  });
}

export const chuongTrinh = (ma) => (SO_DK.chuongTrinh || {})[ma] || SO_DK.chuongTrinh.lop5;
export const cachDoc = (id) => chuongTrinh(chuongTrinhCua(id)).doc || {};

/**
 * Đặt sổ đăng ký từ một đối tượng đã có sẵn.
 *
 * Bộ kiểm chạy bằng node thì không fetch được, mà bản mặc định ở trên chỉ có lớp 2 và
 * lớp 5 — nên `chuongTrinhCua('DL:KSN3.B01')` lùi về 'lop5' và mọi phép đếm theo quyển
 * lệch trong im lặng. Có cửa này thì phép kiểm nạp thẳng tệp thật, đo đúng cái đang chạy.
 */
export function datSoDangKy(json) {
  if (json?.chuongTrinh) SO_DK = { ...SO_DK, ...json };
  return SO_DK;
}

export async function napSoDangKy() {
  try {
    const r = await fetch(dongDau(`${CONTENT}/chuong_trinh.json`));
    if (r.ok) datSoDangKy(await r.json());
  } catch { /* mất mạng: dùng bản mặc định, không chặn bé học */ }
  return SO_DK;
}

/** Bài thuộc chương trình nào — tra TIỀN TỐ mã bài trong sổ đăng ký.
 *  Trước đây so cứng 'DL:KSN2.' trong mã; thêm lớp thứ ba là phải sửa hàm này. */
export const chuongTrinhCua = (id) => {
  const s = String(id || '');
  for (const ct of dsChuongTrinh()) if (ct.tienTo && s.startsWith(ct.tienTo)) return ct.ma;
  return 'lop5';
};

export const thuMucCua = (ma) => chuongTrinh(ma).thuMuc || 'lessons';

/** Quyển này có đi theo NHỊP ĐỌC CHẬM không (chữ to, mỗi màn một mục)?
 *
 *  Trước đây App.jsx hỏi thẳng `chuongTrinh === 'lop2'`. Đúng chừng nào chỉ có một
 *  quyển đọc chậm — thêm lớp 3 là bốn chỗ phải sửa, và quên một chỗ thì bé lớp 3 rơi
 *  vào phòng học của lớp 5: chữ nhỏ, dồn nhiều khối một màn. Sổ đăng ký đã khai sẵn
 *  cờ này, hỏi cờ thì thêm quyển thứ ba, thứ tư cũng không phải sửa gì.
 */
export const nhipDocCham = (ma) => !!(chuongTrinh(ma).doc || {}).moiManMotMuc;
export const baiDocCham = (id) => nhipDocCham(chuongTrinhCua(id));

/** Tiền tố tệp kỳ sát hạch: 'DL:KSN3.' → 'KSN3' (tệp reviews/DCR_KSN3_C1.json). */
export const maKy = (ma) => (chuongTrinh(ma).tienTo || 'DL:KSN5Q1.')
  .replace(/^[A-Z]+:/, '').replace(/\.$/, '');