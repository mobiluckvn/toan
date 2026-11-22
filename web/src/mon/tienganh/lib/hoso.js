import { layNguong, boNguong } from '../../../chung/lib/nguong.js';
/**
 * HỒ SƠ BÉ — ba thứ hệ thống biết về bé, ngoài "đã xong bài nào".
 *
 * Mục 2.3.1 của luận văn khai hồ sơ người học gồm CEFR hiện tại, sở thích, và
 * định dạng bài tập bé hợp nhất. Sở thích đã làm ở Đợt 0. Hai thứ còn lại ở đây.
 *
 * ── CHIỀU SƯ PHẠM (mục 2.1.2-P) ──
 * Hệ thống có 6 định dạng câu và xoay vòng theo BẬC — nhưng xoay theo luật chung,
 * không theo bé. Bé nào nghe tốt mà gõ chữ kém thì vẫn nhận đúng chừng ấy câu gõ
 * chữ như bạn ngược lại. Đo được điều đó thì mới nói tới thích ứng.
 *
 * Sau Đợt 1, mỗi lượt trả lời đã mang `mode` (chính là `format` của câu). Đây là
 * chỗ cộng chúng lại.
 *
 * ── ⚠ ĐỪNG KẾT LUẬN KHI CHƯA ĐỦ MẪU ──
 * Bé làm 2 câu gõ chữ, sai cả 2 → "bé yếu dạng gõ chữ 0%". Kết luận ấy sai, và
 * sai theo cách nguy: nó dẫn tới việc cho bé ÍT câu gõ chữ đi, nên mẫu không bao
 * giờ lớn thêm, và cái nhãn sai tự nuôi chính nó. Nên mọi phép đọc đều đòi
 * `TOI_THIEU_MAU`, và dưới ngưỡng thì trả `null` — "chưa biết", không phải "kém".
 */

/** Dưới chừng này lượt thì chưa nói được gì về một định dạng. */
export const toiThieuMau = (nc) => layNguong(boNguong(), 'NG18', nc);
/* Hằng chụp bộ của phiên — cho cổng và chỗ chỉ HIỂN THỊ. Quyết định dùng hàm trên. */
export const TOI_THIEU_MAU = layNguong(boNguong(), 'NG18');

/** Tên đọc được cho bố mẹ. Định dạng lạ thì hiện chính mã, đừng giấu. */
export const TEN_DINH_DANG = {
  chon: 'chọn đáp án',
  the: 'xếp thẻ thành câu',
  go: 'gõ lại chữ',
  tf: 'đúng / sai',
  nghenhin: 'nghe rồi nhìn hình',
  noi: 'nói theo',
};

export const tenDinhDang = (ma) => TEN_DINH_DANG[ma] || String(ma || '—');

/**
 * Cộng một lượt vào hồ sơ. Trả về hồ sơ MỚI, không sửa tại chỗ.
 *
 * `hs` dạng `{ [format]: { dung, tong } }`.
 */
export function ghiDinhDang(hs, format, dung) {
  const k = String(format || '').trim();
  if (!k) return hs || {};
  const cu = (hs || {})[k] || { dung: 0, tong: 0 };
  return {
    ...(hs || {}),
    [k]: { dung: cu.dung + (dung ? 1 : 0), tong: cu.tong + 1 },
  };
}

/** Tỉ lệ đúng của một định dạng, hoặc `null` khi chưa đủ mẫu. */
export function tiLeDung(hs, format) {
  const d = (hs || {})[format];
  /* Ngữ cảnh `dangCau` = chính định dạng đang xét: một dạng câu khó gom mẫu (nói
     theo) có thể được chuyên gia hạ ngưỡng riêng mà không kéo cả bảng xuống. */
  if (!d || d.tong < toiThieuMau({ dangCau: String(format) })) return null;
  return d.dung / d.tong;
}

/**
 * Xếp hạng các định dạng ĐÃ ĐỦ MẪU, mạnh trước yếu sau.
 * Chưa đủ mẫu thì không có mặt — không xếp hạng thứ mình chưa biết.
 */
export function xepDinhDang(hs) {
  return Object.keys(hs || {})
    .map((k) => ({ ma: k, ten: tenDinhDang(k), ti: tiLeDung(hs, k), tong: hs[k].tong }))
    .filter((x) => x.ti !== null)
    .sort((a, b) => b.ti - a.ti);
}

export const manhNhat = (hs) => xepDinhDang(hs)[0] || null;
export const yeuNhat = (hs) => {
  const ds = xepDinhDang(hs);
  /* Cần ÍT NHẤT HAI định dạng đủ mẫu mới nói được "yếu nhất". Một mình nó thì nó
     vừa mạnh nhất vừa yếu nhất — câu ấy không có nghĩa gì. */
  return ds.length >= 2 ? ds[ds.length - 1] : null;
};

/* ── ĐÃ BỎ `cefrCuaBe()` NGÀY 23-08-2026 ──────────────────────────────────────
 *
 * Hàm ấy suy bậc CEFR từ quyển cao nhất bé đã học XONG HẾT bài. Nó đúng về lô-gic
 * và có cổng riêng, nhưng KHÔNG MÀN NÀO GỌI kể từ lúc viết — bảng đối chiếu Chương
 * 2 lại lấy nó làm bằng chứng cho tiêu chí "CEFR của bé", nên suốt mấy tuần tiêu
 * chí ấy được ghi là ĐÁP ỨNG trong khi màn hình chỉ bày `ct.cefr`, tức nhãn của
 * QUYỂN học liệu.
 *
 * Nay phép quy đổi thật nằm ở `lib/cefr.js` — `bacCefr()` tính từ P(L) trên đồ
 * thị. Giữ lại hàm cũ là để hai con số CEFR khác nghĩa cùng tồn tại, mà cái không
 * ai gọi thì không ai phát hiện được lúc nó lệch.
 *
 * ⚠ Nếu sau này cần lại lối "suy từ quyển đã xong": nó nằm trong lịch sử git,
 * commit a2f50032 trở về trước. Đừng viết lại từ đầu — bản cũ có hai cái bẫy đã
 * xử: thứ tự bậc phải lấy theo SỔ ĐĂNG KÝ chứ không so chuỗi ('A1' < 'Pre-A1'
 * theo bảng chữ cái, tức ngược hẳn thang trình độ), và quyển khai rỗng bài thì
 * không được tính là đã xong.
 */
