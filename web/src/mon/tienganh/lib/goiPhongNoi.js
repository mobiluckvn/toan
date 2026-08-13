/**
 * GỌI PHÒNG LUYỆN NÓI — chỗ DUY NHẤT trong máy con biết tới mạng.
 *
 * Tách khỏi `phongnoi.js` (luật, thuần, cổng chạy bằng node) và khỏi `PhongNoi.jsx`
 * (vẽ). Ba tầng, mỗi tầng một việc — hỏng ở đâu thì biết ngay ở đâu.
 *
 * Máy chủ KHÔNG lưu gì (bác chốt), nên mọi thứ về ngữ cảnh là việc của tệp này và
 * của màn hình: cắt lịch sử trước khi gửi, và tự đẩy buổi nói chuyện lên Firestore.
 */
import { httpsCallable } from 'firebase/functions';
import { doc, setDoc, serverTimestamp } from 'firebase/firestore';
import { fns, db, hasFirebase } from '../../../chung/lib/nenTang.js';
import {
  loiDan, goiGui, docTraLoi, viecTiepTheo, cauHopLe, cauThayThe,
} from './phongnoi.js';

/** Collection riêng của Tiếng Anh — hậu tố TA để không bao giờ lẫn với Toán. */
export const KHO_PHONG_NOI = (uid) => `phongNoiTA/${uid}/buoi`;

/**
 * Hỏi cô giáo máy một lượt.
 *
 * @return {{en, vi, thoJSON}} — đã bóc sẵn để màn hình đọc hai thứ tiếng riêng.
 * @throws lỗi có `.code` của Firebase để màn hình nói đúng chỗ hỏng.
 */
export async function hoiCoGiao({ von, lichSu, tenBe, lop }) {
  if (!hasFirebase || !fns) {
    const e = new Error('Máy chưa nối được lên mạng.');
    e.code = 'functions/unavailable';
    throw e;
  }
  /* Việc của lượt này do MÁY CON quyết rồi ghép vào lời dặn — xem `viecTiepTheo`.
     Lời dặn dựng lại mỗi lượt (chứ không giữ nguyên từ đầu buổi) chính là chỗ cắm
     được việc mới vào. */
  const viec = viecTiepTheo({ von, lichSu });
  const messages = [
    { role: 'system', content: loiDan({ von, tenBe, lop, viec }) },
    ...goiGui(lichSu),
  ];
  const { data } = await httpsCallable(fns, 'luyenNoi')({ messages });
  const tra = docTraLoi(data?.chu);

  /* SOI LẠI CÂU TIẾNG ANH. Dặn dò không đủ: đã bảo rõ ô trống của `Bye, + [Name].`
     là chỗ của tên người, mô hình vẫn sinh ra "Bye, bike." Bé 6 tuổi đang tập nhại
     thì một câu sai là dạy sai. Không hợp lệ thì thay bằng câu máy con tự dựng —
     luôn đúng, vì nó ghép từ chính dữ liệu bài. */
  const cauTruoc = [...lichSu].reverse().find((x) => x.vai === 'may')?.en || '';
  if (!cauHopLe(tra.en, { von, tenBe, cauTruoc })) {
    const thay = cauThayThe(viec, tenBe, cauTruoc);
    /* Thay thì thay CẢ CẶP. Giữ lời tiếng Việt cũ là để nó tả một câu đã bị bỏ —
       đã thấy thật: cô nói "Hi, I'm Bill." mà lời Việt vẫn là "Chào tạm biệt bike".
       Bé nghe hai thứ ngược nhau còn rối hơn là nghe câu sai. */
    if (thay) return { ...tra, en: thay.en, vi: thay.vi, daThay: true };
  }
  return tra;
}

/**
 * Lưu buổi nói chuyện lên máy chủ — CLIENT làm, không phải server.
 *
 * Ghi ĐÈ một tài liệu cho mỗi buổi (mỗi lần bé mở phòng của một unit), không phải
 * mỗi lượt một tài liệu: một buổi nói chuyện là MỘT thứ, và bố mẹ mở sổ ra muốn
 * đọc cả buổi chứ không phải ba mươi mẩu rời.
 *
 * KHÔNG chờ kết quả ở chỗ gọi: mất mạng thì bé vẫn nói chuyện được bình thường,
 * chỉ là buổi ấy không lên máy chủ. Nhưng cũng KHÔNG nuốt im — `LOI_LUU` đếm để
 * còn lần ra, đúng cách `duLieu.js` đang làm.
 */
export const LOI_LUU = { tuChoi: 0, ganNhat: null };

export async function luuBuoi(uid, { maBuoi, quyen, baiId, tenBai, lichSu }) {
  if (!hasFirebase || !db || !uid || !maBuoi) return false;
  try {
    await setDoc(doc(db, KHO_PHONG_NOI(uid), maBuoi), {
      quyen, baiId, tenBai,
      luot: lichSu.map((x) => ({ vai: x.vai, chu: x.chu, en: x.en || null, vi: x.vi || null })),
      soLuot: lichSu.length,
      at: new Date().toISOString(),
      serverTs: serverTimestamp(),
    }, { merge: true });
    return true;
  } catch (e) {
    LOI_LUU.tuChoi += 1;
    LOI_LUU.ganNhat = String(e?.code || e?.message || e);
    if (import.meta.env?.DEV) {
      // eslint-disable-next-line no-console
      console.warn('[tienganh] không lưu được buổi luyện nói:', LOI_LUU.ganNhat,
        '— đã deploy firestore.rules cho phongNoiTA chưa?');
    }
    return false;
  }
}
