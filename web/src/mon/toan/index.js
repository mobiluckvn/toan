/**
 * CỬA CỦA MÔN TOÁN — nơi DUY NHẤT tầng vỏ được nhìn vào.
 *
 * Mọi thứ khác trong `mon/toan/**` là ruột: vỏ app và bốn màn tổng (kệ sách · bảng
 * xếp hạng · sổ bố mẹ · bảng cô giáo) không được import thẳng vào đó, cổng
 * `ranh_gioi.test.mjs` chặn. Nhờ vậy đổi cách Toán lưu tiến độ, đổi cách nó chấm bài,
 * thêm bớt màn — không màn chung nào phải sửa, và môn Tiếng Anh không hề hay biết.
 *
 * Giao ước đầy đủ ghi ở `src/soMon.js`.
 */
import ManToan from './components/ManToan.jsx';
import { loadProgress, saveProgress, gopTienDo } from './lib/progress.js';
import { reassignQueue } from './lib/sync.js';
import { chuongTrinhCua, napChiMuc, dsChuongTrinhSapXep, napBanDoDang, CONTENT, dongDau }
  from './lib/noiDung.js';
import { hocBaQuyen, hocBaChuDe, baiCanCoGang, trinhDo, tienDoQuyen } from './lib/hocba.js';
import { tenDang, dangCuaBai } from './lib/noiDung.js';
import {
  tienDoTuMay, myReport, refreshMyReport, bangXepHangToan, lamMoiBangXepHang,
  learnerAttempts, teacherBoard, refreshTeacherBoard,
} from './lib/duLieu.js';

/** Các quyển của môn này, theo đúng thứ tự trên kệ. */
const quyenCuaToan = () => dsChuongTrinhSapXep().filter((c) => c.mon === 'toan');
const quyenHoc = () => quyenCuaToan().filter((c) => c.loai === 'hoc');

/**
 * Mốc con động vào một bài, tính bằng mili giây; 0 nghĩa là chưa có dấu.
 *
 * Đừng viết `Date.parse(m.at || 0)`: bài chưa có dấu thì `0` bị ép thành chuỗi "0"
 * và đọc ra NĂM 2000 — một con số thật, khác 0, nên `|| 0` phía sau không cứu được.
 * Bài chưa có dấu hoá ra lại xếp trên bài có dấu thật của năm 1999 trở về trước, và
 * quan trọng hơn: nó KHÔNG còn là đáy như người viết tưởng.
 */
const mocCua = (m) => (m?.at ? Date.parse(m.at) || 0 : 0);

/**
 * Tiến độ một quyển — cho kệ sách vẽ vạch.
 * Kệ sách KHÔNG được tự đếm: nó không biết mã bài của Toán trông thế nào, và nếu nó
 * biết thì thêm môn thứ hai là phải viết thêm một nhánh `if` ở đó.
 */

/**
 * HỌC BẠ CỦA MÔN — hình dạng CỐ ĐỊNH mà sổ bố mẹ và bảng cô giáo cùng vẽ.
 * Môn nào cũng phải nộp đúng khuôn này; hai màn kia không biết gì hơn.
 */
async function hocBa(tienDo) {
  const [chiMuc, banDo] = await Promise.all([
    Promise.all(quyenHoc().map((c) => napChiMuc(c.ma))),
    fetch(dongDau(`${CONTENT}/chu_de.json`)).then((r) => (r.ok ? r.json() : null)).catch(() => null),
  ]);

  const quyen = chiMuc.map((cm) => ({
    ...hocBaQuyen(cm, tienDo, { khoaBai: cm.khoaBai }),
    canCoGang: baiCanCoGang(cm, tienDo, 6),
  }));

  /* Quyển động vào GẦN NHẤT — suy từ mốc `at` của từng bài, vì bố mẹ mở sổ từ kệ
     sách thì không có quyển nào đang mở để mà hỏi. */
  const gio = {};
  for (const [id, m] of Object.entries(tienDo?.micros || {})) {
    const t = mocCua(m);
    for (const cm of chiMuc) {
      if (cm.bai.some((b) => b.id === id)) gio[cm.ma] = Math.max(gio[cm.ma] || 0, t);
    }
  }

  return {
    quyen,
    chuDe: banDo ? hocBaChuDe(banDo, tienDo) : null,
    trinhDo: trinhDo(quyen, tienDo, { gioCua: (ma) => gio[ma] || 0 }),
  };
}

/** Học bạ của MỘT em, cho cô giáo xem — đọc thẳng từ máy chủ. */
async function hocBaCuaEm(uid) {
  const tienDo = await tienDoTuMay(uid);
  return { ...(await hocBa(tienDo)), tienDo };
}

export default {
  ma: 'toan',
  ten: 'Toán',
  bieuTuong: '🔢',
  dangCo: true,

  /** Mọi màn của môn, gói trong một cửa. */
  Man: ManToan,

  /* ── Sổ tiến độ: vỏ giữ, môn hiểu ── */
  napTienDo: loadProgress,
  luuTienDo: saveProgress,
  gopTienDo,
  napTuMay: tienDoTuMay,

  /**
   * VỪA ĐĂNG NHẬP XONG — môn tự dọn phần của mình trước khi kéo sổ về.
   *
   * Với Toán, việc phải làm là SANG TÊN HÀNG ĐỢI. Con học thử trước khi đăng nhập
   * (app mời đúng như thế: "Để sau — cho con học thử trước", kèm lời hứa "Đăng nhập
   * lúc nào thì toàn bộ kết quả được đẩy lên, không mất gì"), mọi bản ghi khi ấy mang
   * mã tạm 'local'. Đăng nhập rồi mà không sang tên thì luật bảo mật từ chối
   * `isMine('local')` — và vì cả hàng đợi đi chung MỘT lô ghi, một bản ghi 'local'
   * kẹt lại là **cả lô hỏng, mãi mãi**: bài học sau khi đăng nhập cũng không lên nổi.
   * Từ chối thì im lặng, màn hình vẫn vui vẻ. Đúng lời hứa bị vỡ, mà không ai biết.
   *
   * Vỏ không được với vào ruột môn (xem `test/ranh_gioi.test.mjs`), nên việc này phải
   * đi qua giao ước chứ không gọi thẳng `reassignQueue`.
   */
  dangNhapXong: (uid) => reassignQueue(uid),

  /**
   * CỬA PHỤ trên kệ sách — lối vào của môn KHÔNG đi qua một quyển nào.
   *
   * "Học theo chủ đề" cắt ngang cả bốn quyển Toán, nên nó không thuộc quyển nào và
   * không có chỗ nào khác để đứng. Trước đây kệ sách gọi thẳng màn ấy — nghĩa là tầng
   * chung biết tên một màn của Toán. Nay môn tự khai, kệ sách chỉ vẽ ra cái nút.
   */
  cuaPhu: [{
    trang: 'chuDe',
    ten: 'Học theo chủ đề',
    mo: 'Chọn chủ đề rồi học xuyên các lớp — kém thì lùi về lớp dưới cùng chủ đề',
    bieuTuong: '🗺️',
  }],

  /* ── Nộp cho bốn màn tổng ── */
  dsQuyen: quyenCuaToan,
  tienDoQuyen,
  hocBa,
  hocBaCuaEm,
  bangXepHang: bangXepHangToan,
  lamMoiBangXepHang,

  /* Sổ do máy chủ dựng mỗi đêm — sổ bố mẹ đọc thêm phần này nếu có. */
  soMayChu: myReport,
  lamMoiSoMayChu: refreshMyReport,

  /* ── Bảng cô giáo: nhật ký từng câu và cách gọi tên dạng bài ──
     Ba thứ này của riêng Toán (mã bài `DL:KSN5Q1.…`, ma trận 82 dạng). Bảng cô giáo
     chỉ gọi qua giao ước nên không cần biết. */
  bangCoGiao: teacherBoard,
  lamMoiBangCoGiao: refreshTeacherBoard,
  nhatKyCuaEm: learnerAttempts,
  napBanDoDang,
  tenDang,
  dangCuaBai,
};
