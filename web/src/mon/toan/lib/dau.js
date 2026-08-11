/**
 * LÕI VÒNG ĐẤU (Quyển 2) — thuần hàm, chạy test bằng node.
 *
 * Quyển 2 chấm khác hẳn Quyển 1. Sách nói thẳng: "điểm của màn 1 chỉ là số liệu;
 * giá trị thật của vòng đấu nằm ở màn 2 và màn 3". Nên ở đây có BA TẦNG:
 *
 *   1. ĐÁP SỐ    máy chấm — số liệu khách quan, dùng để mở khoá vòng sau
 *   2. BAREM     con tự chấm 4 mốc — đây mới là bài học của Quyển 2 (bài T2)
 *   3. PHIÊN TÒA con tự soi 12 bẫy — chẩn đoán, nối ngược về micro Quyển 1
 *
 * Ép tất cả về máy chấm là phá đúng cái sách định dạy; để tự chấm hết thì cô giáo
 * không có số liệu tin được. Ba tầng giữ được cả hai.
 */

/* ─────────── Barem 4 mốc (bài T2) ─────────── */
export const BAREM = [
  { id: 'canCu', diem: 0.25, ten: 'Căn cứ / tóm tắt',
    goi: 'có dòng cho thấy con nhận đúng dạng bài' },
  { id: 'phepTinh', diem: 0.5, ten: 'Phép tính đúng',
    goi: 'có lời dẫn và có đơn vị khi cần' },
  { id: 'dapSo', diem: 0.25, ten: 'Đáp số',
    goi: 'có chữ "Đáp số:" và đúng đơn vị đề hỏi' },
  { id: 'thuLai', diem: 0, ten: 'Thử lại',
    goi: 'không tính điểm, nhưng viết được thì sai ít hẳn' },
];

/** Điểm trình bày của MỘT câu theo các mốc con đã tick */
export function diemBarem(tick = {}) {
  return BAREM.reduce((s, m) => s + (tick[m.id] ? m.diem : 0), 0);
}

/* ─────────── Tầng 1 · điểm đáp số ─────────── */
/**
 * @param ketQua { [maCau]: {ok:boolean, tuChamDung?:boolean} }
 * Câu máy chấm lấy `ok`; câu tự luận lấy `tuChamDung` (con tự nhận đúng/sai sau
 * khi xem lời chữa) — không có cách nào khác, và đó đúng là thiết kế của sách.
 */
export function diemDapSo(khoi, ketQua = {}) {
  let dung = 0;
  for (const c of khoi.cau) {
    const r = ketQua[c.id];
    if (!r) continue;
    if (c.answerKey ? r.ok : r.tuChamDung) dung++;
  }
  return { dung, tong: khoi.cau.length };
}

/** Đạt hay chưa — ngưỡng lấy từ chính sách (12/15, 8/10 …) */
export function datChua(khoi, ketQua = {}) {
  const { dung } = diemDapSo(khoi, ketQua);
  const can = khoi.dat ?? Math.ceil(khoi.cau.length * 0.8);
  return { dat: dung >= can, dung, can, tong: khoi.cau.length };
}

/* ─────────── Tầng 3 · phiên tòa bẫy ─────────── */
/**
 * @param toa { [maBay]: 'sap' | 'thoat' }
 * Trả về danh sách micro Quyển 1 cần ôn — trục nối hai quyển. Con sập bẫy CĐ-4.2
 * thì mở thẳng micro B4.M2, không phải đi tìm.
 */
export function keDonOn(khoi, toa = {}) {
  const sap = (khoi.bay || []).filter((b) => toa[b.ma] === 'sap');
  return {
    soSap: sap.length,
    soBay: (khoi.bay || []).length,
    micro: [...new Set(sap.map((b) => b.micro))],
    bay: sap.map((b) => ({ ma: b.ma, ten: b.ten, micro: b.micro, thanChu: b.thanChu })),
  };
}

/** Lời tuyên án theo số bẫy đã sập — đúng thang của sách */
export function tuyenAn(soSap, soBay = 12) {
  if (soSap <= 2) return 'Xuất sắc — con đã biến hồ sơ bẫy thành phản xạ.';
  if (soSap <= 5) return 'Bình thường ở vòng này — đọc lại đúng những mã đã sập là ổn.';
  return `Sập ${soSap}/${soBay} bẫy — nên ôn lại các micro Quyển 1 ở dưới trước khi sang vòng sau.`;
}

/* ─────────── Đồng hồ ─────────── */
/**
 * Thời gian còn lại, tính từ MỐC BẮT ĐẦU THẬT chứ không đếm lùi từng giây.
 *
 * Vì sao: con khoá máy tính bảng giữa chừng, hoặc chuyển sang ứng dụng khác, thì
 * trình duyệt ngưng chạy bộ đếm — đếm lùi bằng biến sẽ đứng yên và con được thêm
 * giờ không công. Lấy hiệu hai mốc thời gian thì khoá máy bao lâu cũng đúng.
 */
export function conLai(batDauMs, phut, bayGio = Date.now()) {
  const het = batDauMs + phut * 60000;
  return Math.max(0, het - bayGio);
}

export const hetGio = (batDauMs, phut, bayGio = Date.now()) =>
  conLai(batDauMs, phut, bayGio) === 0;

/** 154000 → "2:34" */
export function docGio(ms) {
  const giay = Math.floor(ms / 1000);
  return `${Math.floor(giay / 60)}:${String(giay % 60).padStart(2, '0')}`;
}

/* ─────────── Tầng 2 (đề trộn) · chấm kép ─────────── */
/**
 * Đề trộn chấm HAI CỘT RIÊNG, không cộng lại: điểm TOÁN và điểm ĐỊNH DẠNG.
 * Sách giải thích rõ vì sao — hai loại lỗi cần hai loại thuốc khác nhau: sai toán
 * thì ôn dạng, còn gọi sai tên dạng thì luyện nhịp 3 của bài T1.
 */
export function chamKep(khoi, ketQua = {}, dinhDang = {}) {
  const { dung, tong } = diemDapSo(khoi, ketQua);
  const dungDang = khoi.cau.filter((c) => dinhDang[c.id]?.dung).length;
  const can = khoi.dat ?? Math.ceil(tong * 0.8);
  return {
    toan: dung, dinhDang: dungDang, tong, can,
    dat: dung >= can && dungDang >= can,
  };
}

/* ─────────── Mở khoá ─────────── */
/**
 * Vòng đấu n mở khi con đã học xong CHƯƠNG n của Quyển 1 (đã chốt với bố mẹ).
 * Học xen kẽ được, không phải đợi hết 168 micro mới được luyện thi.
 *
 * Đề trộn và kỳ thi thử mở theo chương cao nhất mà nó phủ.
 */
export function moKhoa(khoi, chuongDaXong = new Set()) {
  const can = khoi.chuongQ1;
  if (!can) return true;
  return chuongDaXong.has(can);
}

/**
 * Các chương QUYỂN 1 con đã học xong (mọi micro trong chương đều đạt).
 *
 * ⚠ PHẢI LỌC LẤY BÀI CỦA QUYỂN 1. Sổ `progress.micros` là sổ CHUNG của cả bốn quyển —
 * đó là chủ ý, để sổ phụ huynh và bảng cô giáo nhìn được một mối. Nhưng ở đây thì
 * `chuongCua` là hàm chia chương của Quyển 1: đưa mã bài lớp 2·3·4 vào, nó trả về
 * chương 1 cho tất cả. Chỉ cần con học dở MỘT bài lớp 3 là chương 1 của Quyển 1 bị
 * coi là chưa xong, và VÒNG ĐẤU 1 KHOÁ CỨNG dù con đã học hết 12 micro của nó.
 *
 * Đã dính thật: bé học lớp 4 rồi quay sang lớp 5, xong chương 1, mà Mùa giải vẫn báo
 * "Mở khi con học xong chương 1" — không kèm dòng "còn N bài nữa", nên nhìn như app
 * hỏng chứ không như một điều kiện chưa đạt.
 */
export function chuongDaXong(progressMicros = {}, chuongCua, laQuyen1 = LA_QUYEN1) {
  const cua = Object.keys(progressMicros).filter(laQuyen1);
  const xong = new Set();
  for (let c = 1; c <= 14; c++) {
    const ms = cua.filter((id) => chuongCua(id) === c);
    if (ms.length && ms.every((id) => progressMicros[id]?.pass)) xong.add(c);
  }
  return xong;
}

/* Tiền tố mã bài Quyển 1. Để ngay cạnh `laQuyen2` ở trên — hai mặt của một luật, và
   dau.js vốn là tệp RIÊNG của Mùa giải nên biết cả hai mã là đúng chỗ. */
const LA_QUYEN1 = (id) => String(id).startsWith('DL:KSN5Q1.');
