/**
 * GỌI MÁY CHẤM BÀI VIẾT — chỗ DUY NHẤT của phần này biết tới mạng.
 *
 * Ba tầng, đúng khuôn phòng luyện nói:
 *     chamviet.js      luật thuần, chạy được bằng node
 *     goiChamViet.js   gọi máy chủ, soi lại lời chấm      ← tệp này
 *     VietBai.jsx      vẽ
 *
 * Máy chủ KHÔNG lưu gì (cùng lối với `luyenNoi`). Bài viết và lời chấm do MÁY CON
 * đẩy lên `hocBaTA` — xem `ghiBaiViet` và `luuMucHocBa`.
 */
import { httpsCallable } from 'firebase/functions';
import { fns, hasFirebase } from '../../../chung/lib/nenTang.js';
import { docLoiCham, soiLoiCham } from './chamviet.js';

/**
 * Nhờ cô giáo máy chấm một bài.
 *
 * @return {{cham, boQua, moHinh}} — `cham` đã SOI, `boQua` là những câu bị bỏ vì
 *   chứa từ chưa học. Màn hình phải nói ra `boQua` chứ đừng giấu: giấu thì lời
 *   chấm trông đầy đủ trong khi nó vừa mất một mục.
 * @throws lỗi có `.code` của Firebase để màn hình nói đúng chỗ hỏng.
 */
export async function nhoCham({ de, viet, vonTu, mauCau, lop = 3 }) {
  if (!hasFirebase || !fns) {
    const e = new Error('Máy chưa nối được lên mạng.');
    e.code = 'functions/unavailable';
    throw e;
  }
  const { data } = await httpsCallable(fns, 'chamViet')({ de, viet, vonTu, mauCau, lop });
  const tho = docLoiCham(data?.chu);
  if (!tho) {
    const e = new Error('Máy chấm trả lời không đọc được.');
    e.code = 'functions/internal';
    throw e;
  }
  /* SOI LẠI, dù đã dặn. Xem chú thích dài ở `chamviet.js`: dặn dò là thứ mô hình
     CÓ THỂ theo, và bé tám tuổi đọc lời chấm là tin. */
  const { cham, boQua } = soiLoiCham(tho, { vonTu, mauCau });
  if (boQua.length) {
    LOI_CHU_LA.so += boQua.length;
    LOI_CHU_LA.ganNhat = boQua[0];
  }
  return { cham, boQua, moHinh: data?.moHinh || null };
}

/**
 * Đếm số câu bị bỏ vì có chữ chưa học. Không hiện ra cho bé — nhưng cũng KHÔNG
 * nuốt im: đếm nhiều nghĩa là lời dặn đang không ăn, và không có con số thì chẳng
 * ai biết để mà sửa lời dặn. Cùng lối với `LOI_LOI_VIET` của phòng luyện nói.
 */
export const LOI_CHU_LA = { so: 0, ganNhat: null };
