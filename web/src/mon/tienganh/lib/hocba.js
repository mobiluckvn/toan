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

export const hocBaTu = (tienDo) => ({
  quyen: quyenHoc().map((ct) => hocBaQuyen(tienDo, ct)),
  /* Màn "học theo chủ đề" là ma trận của TOÁN. Tiếng Anh có thang tiên quyết riêng
     (10 mối trong lớp 1) nhưng chưa dựng thành màn — trả null chứ không trộn vào. */
  chuDe: null,
  trinhDo: null,
});
