/**
 * PHÉP ĐẾM CỦA MÔN TIẾNG ANH — mọi con số tiến độ hỏi ở ĐÂY.
 *
 * Đặt trong `lib/` chứ không trong `index.js`, và đó là chủ ý: `index.js` import
 * component `.jsx`, mà `node` không nạp được `.jsx` — nên phép kiểm chạy bằng node
 * KHÔNG với tới được hàm nào nằm trong đó. Hàm thuần thì phải để chỗ gọi thử được.
 *
 * Chuyện này không phải lo xa: giao ước ở `src/soMon.js` từng ghi tham số thứ hai
 * của `tienDoQuyen` là `ma`, trong khi `KeSach.jsx` truyền cả MỤC chương trình.
 * Môn này làm theo lời ghi nên kệ sách hiện "0 unit" cho quyển 16 bài — cổng chỉ
 * soi TÊN hàm nên xanh suốt, chỉ có con số trên màn hình là sai.
 */
import { quyenTiengAnh } from './noiDung.js';

export const quyenHoc = () => quyenTiengAnh().filter((c) => c.loai === 'hoc');

/**
 * Tiến độ một quyển — cho kệ sách vẽ vạch. Kệ sách KHÔNG được tự đếm.
 * `ct` là CẢ MỤC chương trình. Nhận cả mã chuỗi cho chắc.
 */
export function tienDoQuyen(tienDo, ctHoacMa) {
  const ct = typeof ctHoacMa === 'string'
    ? quyenTiengAnh().find((c) => c.ma === ctHoacMa)
    : ctHoacMa;
  const ds = ct?.bai || [];
  const m = tienDo?.micros || {};
  const xong = ds.filter((id) => m[id]?.pass).length;
  const dangLam = ds.filter((id) => m[id] && !m[id].pass).length;
  return {
    xong,
    dangLam,
    tong: ds.length || ct?.soBai || 0,
    phanTram: ds.length ? Math.round((xong / ds.length) * 100) : 0,
    /* Chưa đo giờ học thật. Trả 0 chứ KHÔNG bịa: sổ bố mẹ hiện "chưa có" thì bố mẹ
       biết là chưa đo, còn hiện một con số ước lượng thì tin nhầm. */
    gio: 0,
  };
}

/**
 * Số bài suy từ MÃ BÀI: `DL:TA3.B07` → 7, `DL:TA1.B00` → 0.
 *
 * Trả `null` khi mã không đúng khuôn — để chỗ vẽ bỏ qua mục ấy, chứ đừng ghép
 * một số bịa vào câu tiếng Việt cho bố mẹ đọc.
 */
export function soBaiTuMa(ma) {
  const m = /\.B(\d+)$/.exec(String(ma || ''));
  return m ? Number(m[1]) : null;
}

/** Mốc gần nhất bé động vào một bài, mili-giây; 0 khi không có dấu. `at` có thể là
    chuỗi ISO (máy con ghi) hoặc số (bản ghi cũ) — nhận cả hai. */
const mocBai = (m) => (typeof m?.at === 'number' ? m.at : Date.parse(m?.at || '') || 0);

/** Học bạ một quyển — đúng khuôn `HocBaMon` mà bốn màn tổng cùng đọc. */
export function hocBaQuyen(tienDo, ct) {
  const ds = ct.bai || [];
  const m = tienDo?.micros || {};
  const datBai = ds.filter((id) => m[id]?.pass).length;
  const chuongDat = Object.entries(tienDo?.chapters || {})
    .filter(([k, v]) => k.startsWith(`${ct.ma}:`) && v.dat);
  return {
    ma: ct.ma,
    ten: ct.ten,
    tongBai: ds.length,
    datBai,
    phanTram: ds.length ? Math.round((datBai / ds.length) * 100) : 0,
    tongChuong: ct.soChuong || 0,
    masterChuong: chuongDat.length,
    huyHieu: [],
    daBatDau: ds.some((id) => m[id]),
    /* Mốc bé động vào quyển này gần nhất — `trinhDoTu` chọn "quyển đang học" theo nó. */
    ganNhat: Math.max(0, ...ds.map((id) => mocBai(m[id]))),
    chuong: [],
    /* Bài bé làm rồi mà CHƯA đạt — đúng chỗ bố mẹ cần nhìn, không phải danh sách
       bài chưa mở.
       ⚠ TÊN TRƯỜNG PHẢI ĐÚNG KHUÔN `soMon.js`, KHÔNG ĐƯỢC TỰ ĐẶT. Bản đầu nộp
       `{ma, best, tong}` trong khi màn dùng chung `ParentReport.jsx` đọc `so` ·
       `ten` · `chuong` · `lan` · `dung` — nên Sổ bố mẹ hiện thẳng chữ "Cần cố
       gắng: Bài undefined" lên bản chạy thật. Lỗi này không cổng nào bắt vì hai
       bên đều đúng một mình; khuôn phần tử trước đây chưa ai ghi ra.
       `so` suy từ chính mã bài (`DL:TA3.B07` → 7) chứ không đếm vị trí trong sổ
       đăng ký: đếm vị trí thì thêm hay bớt một bài là mọi số nhảy một nấc. */
    canCoGang: ds.filter((id) => m[id] && !m[id].pass).slice(0, 5)
      .map((id) => ({
        id,
        so: soBaiTuMa(id),
        ten: '',
        micro: 1,
        chuong: null,
        lan: m[id].attempts || 0,
        dung: m[id].score || 0,
        tong: m[id].total || 0,
      })),
  };
}

/**
 * TRÌNH ĐỘ HIỆN TẠI của môn Tiếng Anh — khối đầu Sổ bố mẹ.
 *
 * ⚠ TRƯỚC 22-11-2026 HÀM NÀY KHÔNG CÓ: `hocBaTu` trả `trinhDo: null`, nên khối đầu
 * Sổ bố mẹ báo "Con chưa học bài nào" cho MỌI em học Tiếng Anh — kể cả em đã xong
 * 16/16 unit, mà danh sách quyển ngay bên dưới vẫn ghi đúng 16/16. Hai con số trái
 * nhau trên cùng một màn.
 *
 * Cùng khuôn với `trinhDo` của Toán (`ParentReport.jsx` đọc chung): quyển đang học là
 * quyển bé động vào GẦN NHẤT; `bacChuDe` để `null` vì Tiếng Anh chưa có màn chủ đề.
 */
export function trinhDoTu(dsHocBa) {
  const daHoc = dsHocBa.filter((h) => h.daBatDau);
  const ganNhat = daHoc.slice().sort((a, b) => (b.ganNhat || 0) - (a.ganNhat || 0))[0] || null;
  return {
    quyen: ganNhat,
    soQuyenDangHoc: daHoc.length,
    tongBaiDat: dsHocBa.reduce((s, h) => s + h.datBai, 0),
    tongChuongMaster: dsHocBa.reduce((s, h) => s + h.masterChuong, 0),
    bacChuDe: null,
    soChuDeDoDuoc: 0,
  };
}

export const hocBaTu = (tienDo) => {
  const quyen = quyenHoc().map((ct) => hocBaQuyen(tienDo, ct));
  return {
    quyen,
    /* Màn "học theo chủ đề" là ma trận của TOÁN. Tiếng Anh có thang tiên quyết riêng
       (10 mối trong lớp 1) nhưng chưa dựng thành màn — trả null chứ không trộn vào. */
    chuDe: null,
    trinhDo: trinhDoTu(quyen),
  };
};

/* ═══════════ ĐIỂM MÁY CHẤM Ở TRẠNG THÁI "TẠM" (việc V5, mẫu Human-in-the-loop) ═══════════ */

/**
 * ── VÌ SAO CẦN ──
 * Điểm bài viết do mô hình chấm. Màn hình đã nói rõ "máy chấm (AI), không phải điểm
 * của cô giáo" từ lâu — nhưng đó chỉ là một dòng chữ. Con số thì vẫn nằm trong sổ
 * học bạ y như mọi điểm khác, và sổ học bạ là thứ bố mẹ đọc để biết con đang ở đâu.
 *
 * Nên thêm một trạng thái: điểm máy chấm là ĐIỂM TẠM cho tới khi người lớn xem. Bố
 * mẹ đồng ý thì nó thành điểm đã xác nhận; thấy máy chấm sai thì sửa. Cả hai đường
 * đều một chạm, và cả hai đều để lại dấu — không có đường nào lặng lẽ đổi điểm.
 *
 * ── BA ĐIỀU KHÔNG ĐƯỢC PHÁ ──
 *  1. `attempts` VẪN BẤT BIẾN. Việc này không sửa một bản ghi nào đã có; nó chỉ
 *     thêm trường vào mục học bạ.
 *  2. KHÔNG CÓ NÚT NÀO CHO BÉ. Xác nhận điểm của chính mình thì không còn là xác
 *     nhận. Mấy nút này chỉ nằm trong Góc bố mẹ.
 *  3. BKT KHÔNG ĐỔI — xem ghi chú ở `diemHienThi`.
 */
export const TRANG_THAI_DIEM = { tam: 'tam', xacNhan: 'xacNhan' };

/**
 * Đổi sang số, mà `null` thì VẪN LÀ `null`.
 *
 * ⚠ `Number(null)` LÀ 0, VÀ `Number.isFinite(0)` LÀ TRUE. Viết
 * `Number.isFinite(Number(x)) ? Number(x) : null` là `null` hoá thành số 0 — và lỗi
 * ấy tôi viết ra HAI LẦN trong cùng tệp này trong cùng một buổi:
 *   · `diemHienThi`   → `diemNguoi: null` ("bố mẹ ĐỒNG Ý") thành "bố mẹ sửa: 0",
 *                        tức bấm Đồng ý là điểm bé tụt về 0;
 *   · `baiChoXacNhan` → bài CHƯA CHẤM (`diem: null`) lọt vào danh sách chờ xác nhận.
 * Nên nó phải là MỘT hàm, không phải một dòng viết lại mỗi chỗ. Hỏi `== null` TRƯỚC,
 * rồi mới đổi sang số.
 */
const soHoacNull = (x) => (x === null || x === undefined || x === ''
  ? null : (Number.isFinite(Number(x)) ? Number(x) : null));

/**
 * Bố mẹ xác nhận (hoặc sửa) điểm một bài viết. TRẢ BẢN MỚI.
 *
 * @param diemNguoi  `null` nghĩa là ĐỒNG Ý với điểm máy chấm. Có số nghĩa là sửa.
 * @param luc        mốc thời gian, tiêm vào để cổng chạy tiền định.
 *
 * ⚠ KHÔNG SỬA TẠI CHỖ. Mục này nằm trong sổ tiến độ, mà sổ ấy đi vào `useMemo` của
 * React — sửa tại chỗ thì màn hình không thấy nó đổi, và bố mẹ bấm nút mà không
 * thấy gì xảy ra. Cùng lý do với `ghiLuot` của bảng trạng thái.
 *
 * ⚠ VÀ KHÔNG ĐỤNG `diem`. Con số máy chấm giữ nguyên ở đó, kể cả khi bố mẹ sửa:
 * `diemNguoi` nằm cạnh nó, không đè lên. Đè lên thì mất bằng chứng máy chấm bao
 * nhiêu, và câu hỏi "máy chấm có hay sai không" hết đường trả lời.
 */
export function xacNhanDiem(muc, { diemNguoi = null, luc = Date.now() } = {}) {
  if (!muc) return muc;
  const d = diemNguoi === null || diemNguoi === undefined ? null : Number(diemNguoi);
  return {
    ...muc,
    trangThai: TRANG_THAI_DIEM.xacNhan,
    diemNguoi: Number.isFinite(d) ? d : null,
    xacNhanLuc: new Date(luc).toISOString(),
  };
}

/**
 * ĐIỂM ĐỂ HIỆN RA, KÈM NHÃN NGUỒN — và nhãn là phần quan trọng hơn con số.
 *
 * Mọi chỗ hiện điểm bài viết phải đi qua hàm này. Không phải chuyện gu kiến trúc:
 * con số không nhãn sẽ được đọc thành điểm của cô giáo, và đó là hiểu nhầm bố mẹ
 * KHÔNG có cách nào tự phát hiện. Ba chỗ con số ấy lộ ra (thẻ bài · màn lời chấm ·
 * Góc bố mẹ) đã từng mỗi chỗ tự viết một dòng chữ khác nhau.
 *
 * ⚠ BKT ĐỌC `diem`, KHÔNG ĐỌC HÀM NÀY — và đó là quyết định, không phải sơ sót.
 * `onAttempt` pha `worked` nhận bản ghi viết ngay khi máy chấm xong. Bắt nó chờ bố
 * mẹ xác nhận thì engine đứng lại ở mọi bài viết của mọi bé chưa có người lớn ngồi
 * cạnh — tức phần thích ứng tắt hẳn vì một việc của người lớn. Nên: ENGINE cứ chạy
 * bằng điểm máy chấm, còn MÀN HÌNH thì nói rõ điểm ấy đã được ai xem. Hai việc
 * khác nhau, và chỉ một trong hai cần người.
 */
export function diemHienThi(muc) {
  if (!muc) return { diem: null, nhan: '', nhanDay: '', choXacNhan: false };
  const may = soHoacNull(muc.diem);
  const nguoi = soHoacNull(muc.diemNguoi);
  /* Mục cũ trong sổ không có `trangThai` — sổ sống lâu hơn mã. Coi là `tam`: nói
     "chờ bố mẹ" về một bài bố mẹ đã xem thì chỉ hơi sai, còn nói "đã xác nhận" về
     một bài chưa ai xem thì sai hẳn về phía nguy hiểm. */
  const tt = muc.trangThai || TRANG_THAI_DIEM.tam;
  /* ⚠ HAI NHÃN, VÀ CẢ HAI ĐỀU CẦN.
     `nhan` — ba giá trị ngắn của §7, dùng ở chỗ hẹp và là thứ cổng canh.
     `nhanDay` — nhãn ĐẦY ĐỦ, và nó LUÔN nói điểm từ đâu ra. Màn hình dùng cái này.
     Vì sao phải có: `nhan` của ca "đã xác nhận" là "bố mẹ đã xác nhận" — đúng, mà
     không còn một chữ nào nói con số ấy do MÁY chấm. Thẻ bài viết hiện "8/10 điểm ·
     bố mẹ đã xác nhận" thì vẫn đọc được thành điểm của cô giáo, đúng hiểu nhầm mà
     bác bắt sửa từ đầu và bố mẹ không có cách nào tự phát hiện. Cổng cũ ghim chuỗi
     "Máy chấm (AI)" nên nó đỏ lên và chỉ ra đúng chỗ mất mát này. */
  if (tt !== TRANG_THAI_DIEM.xacNhan) {
    return { diem: may, nhan: 'máy chấm – chờ bố mẹ', choXacNhan: true,
             nhanDay: 'Máy chấm (AI) – chờ bố mẹ xem' };
  }
  if (nguoi !== null && nguoi !== may) {
    return { diem: nguoi, nhan: `bố mẹ sửa: ${nguoi}`, choXacNhan: false, diemMay: may,
             nhanDay: `Bố mẹ sửa thành ${nguoi} – Máy chấm (AI) cho ${may}` };
  }
  return { diem: may, nhan: 'bố mẹ đã xác nhận', choXacNhan: false,
           nhanDay: 'Máy chấm (AI) – bố mẹ đã xác nhận' };
}

/** Những bài viết đang CHỜ bố mẹ xem — danh sách cho Góc bố mẹ. */
export function baiChoXacNhan(tienDo) {
  return Object.entries(tienDo?.baiViet || {})
    .filter(([, m]) => soHoacNull(m?.diem) !== null && diemHienThi(m).choXacNhan)
    .map(([khoa, m]) => ({ khoa, muc: m, ...diemHienThi(m) }));
}
