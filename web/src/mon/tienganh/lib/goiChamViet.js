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
  const { cham, boQua } = soiLoiCham(tho, { vonTu, mauCau, beViet: viet });
  if (boQua.length) {
    LOI_CHU_LA.so += boQua.length;
    LOI_CHU_LA.ganNhat = boQua[0];
  }
  /* VÂN TAY LỜI DẶN đi kèm ra ngoài. `chamviet.js` đã sinh nó từ 21-08 với đúng ý
     này — chú thích ở đó ghi "vân tay trả về cho máy con, máy con ghi kèm bản ghi
     của chính bé" — nhưng không ai chuyền tiếp nên nó rơi ngay tại dòng này. Nối
     nốt 23-08: thiếu nó thì không trả lời được câu "lời chấm này do mẫu prompt nào
     sinh ra", tức mục 2.5.2 của luận văn hụt một trường. */
  return {
    cham,
    boQua,
    /* Số lần máy chủ phải XIN LẠI mắt xích 2 vì nó dùng chữ ngoài vốn (việc V4), và
       chữ lạ còn sót sau khi hết vòng. Đếm được thì mới biết chuỗi ba mắt xích có
       thật sự dẹp được chữ lạ hay chỉ đẩy nó xuống một tầng — xem `LOI_CHU_LA` dưới
       và `LOI_SUA_LAI` ở `functions/src/chamviet.js`. */
    lanSuaLai: data?.lanSuaLai ?? 0,
    chuLaConLai: data?.chuLaConLai || [],
    moHinh: data?.moHinh || null,
    mauPrompt: data?.mauPrompt || null,
    phienBanMau: data?.phienBanMau ?? null,
    vanTayPrompt: data?.vanTayPrompt || null,
  };
}

/**
 * Đếm số câu bị bỏ vì có chữ chưa học. Không hiện ra cho bé — nhưng cũng KHÔNG
 * nuốt im: đếm nhiều nghĩa là lời dặn đang không ăn, và không có con số thì chẳng
 * ai biết để mà sửa lời dặn. Cùng lối với `LOI_LOI_VIET` của phòng luyện nói.
 */
export const LOI_CHU_LA = { so: 0, ganNhat: null };
