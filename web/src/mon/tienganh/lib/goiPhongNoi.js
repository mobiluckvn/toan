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
  buocTiepTheo, dienBuoc, dongBuoc, loiVietHopLe, luotBeCuoi,
  loiDanTranh, canNoi,
} from './phongnoi.js';

/** Collection riêng của Tiếng Anh — hậu tố TA để không bao giờ lẫn với Toán. */
export const KHO_PHONG_NOI = (uid) => `phongNoiTA/${uid}/buoi`;

/**
 * Hỏi cô giáo máy một lượt.
 *
 * @return {{en, vi, thoJSON}} — đã bóc sẵn để màn hình đọc hai thứ tiếng riêng.
 * @throws lỗi có `.code` của Firebase để màn hình nói đúng chỗ hỏng.
 */
export async function hoiCoGiao({
  von, lichSu, tenBe, lop, haDoKho = false, hoSo = null, kichBan = null,
}) {
  if (!hasFirebase || !fns) {
    const e = new Error('Máy chưa nối được lên mạng.');
    e.code = 'functions/unavailable';
    throw e;
  }
  /* Việc của lượt này do MÁY CON quyết rồi ghép vào lời dặn — xem `viecTiepTheo`.
     Lời dặn dựng lại mỗi lượt (chứ không giữ nguyên từ đầu buổi) chính là chỗ cắm
     được việc mới vào. */
  /* CÓ KỊCH BẢN thì câu tiếng Anh lấy thẳng từ đó, mô hình chỉ viết lời tiếng Việt.
     Không có (bài chưa sinh kịch bản) thì rơi về cách cũ — máy con tự chọn việc. */
  const buoc = kichBan ? buocTiepTheo({ kichBan, lichSu, hoSo, haDoKho }) : null;
  const viec = buoc ? null : viecTiepTheo({ von, lichSu, haDoKho, hoSo });
  /* Lượt vừa rồi của bé — kèm ĐIỂM và những chữ bé bỏ sót. `goiGui` cắt sạch mấy
     thứ ấy khi gửi lịch sử (nó chỉ gửi vai + chữ), nên nếu không đi đường này thì
     mô hình không có cách nào biết bé nói được mấy điểm. Xem `dongBuoc`. */
  const luotBe = luotBeCuoi(lichSu);
  const unit = kichBan
    ? { ten: kichBan.ten,
        muc_tieu: kichBan.muc_tieu,
        tinh_huong: kichBan.tinh_huong,
        /* Bản mô tả BỨC TRANH — thứ CÔ có mà BÉ không có. Nhờ nó cô sửa được cả Ý,
           không chỉ sửa tiếng: bé nói "I can see two kites." thì cô biết sai SỐ, vì
           bản mô tả ghi ba. Bác chốt 19-08. */
        moTaTranh: kichBan.moTaTranh || null }
    : null;
  /* ⚠ BÀI TẢ TRANH DÙNG LỜI DẶN RIÊNG, KHÔNG GHÉP THÊM VÀO LỜI DẶN CŨ.
     Bác chốt 19-08: "Hãy xoá hết prompt cũ để cài đặt lại. Đảm bảo AI là một giáo
     viên hướng dẫn học sinh mô tả tranh không phải đi dạy học sinh nói câu hỏi."
     Lời dặn cũ dài mười điều và gần như điều nào cũng nói về DẠY NHẠI CÂU. Ghép
     thêm mấy dòng về tranh vào đấy thì mô hình vẫn đọc ra "dạy bé nói theo mẫu",
     vì chín phần mười lời dặn nói thế. */
  const laTranh = kichBan?.dang === 'tranh';
  const dan = laTranh
    ? loiDanTranh({ tenBe, lop, kichBan, buoc, luotBe })
    : (buoc
      ? `${loiDan({ von, tenBe, lop, viec: null, hoSo, unit })}\n${dongBuoc(buoc, { tenBe, thich: hoSo?.thich }, luotBe)}`
      : loiDan({ von, tenBe, lop, viec, hoSo, unit }));
  const messages = [{ role: 'system', content: dan }, ...goiGui(lichSu)];
  const { data } = await httpsCallable(fns, 'luyenNoi')({ messages });
  const tra = docTraLoi(data?.chu);

  /* SOI LẠI CÂU TIẾNG ANH. Dặn dò không đủ: đã bảo rõ ô trống của `Bye, + [Name].`
     là chỗ của tên người, mô hình vẫn sinh ra "Bye, bike." Bé 6 tuổi đang tập nhại
     thì một câu sai là dạy sai. Không hợp lệ thì thay bằng câu máy con tự dựng —
     luôn đúng, vì nó ghép từ chính dữ liệu bài. */
  const cauTruoc = [...lichSu].reverse().find((x) => x.vai === 'may')?.en || '';

  /* CÓ KỊCH BẢN: câu đúng đã biết trước, nên không cần đoán — sai thì ép về đúng
     câu ấy. Đây là chỗ chữ "đảm bảo hơn" của bác thành thật: mô hình có chệch thì
     bé vẫn nghe đúng câu của bài. */
  if (buoc) {
    const dung = dienBuoc(buoc, { tenBe, thich: hoSo?.thich });
    /* ⚠ BƯỚC KHÔNG CÓ CÂU VIẾT SẴN VẪN PHẢI SOI.
       `hoiThich` không mang câu tiếng Anh nào — thẻ chọn hình do máy con tự vẽ. Nên
       `dung` rỗng, và dòng dưới cho `tra.en` đi thẳng. Mà nhánh có kịch bản thì cố
       ý bỏ qua `cauHopLe` (câu đã biết trước, soi làm gì) — cộng lại thành đúng MỘT
       lượt mỗi buổi mà câu của mô hình không ai soi. Đúng lượt thứ hai, lượt bé
       vừa mới vào phòng. Không gì kêu: câu ấy thường vẫn đúng. */
    if (!dung && !cauHopLe(tra.en, { von, tenBe, cauTruoc })) {
      /* Lui về một lời lớp học cố định. Không dùng `cauThayThe`: nó cần một `viec`,
         mà nhánh kịch bản thì không có `viec` nào — gọi vào là nhận `null` rồi lại
         thả câu hỏng đi tiếp, tức là chốt soi có mà như không. */
      return { ...tra,
        en: 'Your turn.',
        vi: 'Con chọn một hình con thích nhất nhé, rồi mình tập nói về nó.',
        buoc: buoc.loai,
        daThay: true };
    }
    const en = dung && tra.en !== dung ? dung : tra.en;
    return { ...tra,
      en,
      /* Câu bé CẦN nói ở lượt tới — KHÔNG phải câu cô vừa nói. Với bài tả tranh, cô
         hỏi "What can you see?" mà bé phải ĐÁP; chấm theo câu cô nói thì hệ thống
         khen bé vì nhại đúng câu hỏi. Xem `canNoi`. */
      can: canNoi(buoc, kichBan),
      /* Lượt này do bước NÀO sinh ra. Màn hình giữ lại trong lịch sử, để
         `luotLuyen` biết lượt đáp lời chào không phải một lần luyện — thiếu nó thì
         buổi kết sớm một nấc và bước làm mẫu bị nhảy cóc. */
      buoc: buoc.loai,
      /* `beNoi` đi kèm để lời SỬA được phép trích lại đúng chữ bé vừa nói — không
         có nó thì lượt sửa nào cũng bị gạt rồi lui về câu chung chung. */
      vi: loiVietSach(tra.vi, { von, cauDich: en, lui: buoc.vi, beNoi: luotBe?.chu }),
      daThay: en !== tra.en };
  }

  if (!cauHopLe(tra.en, { von, tenBe, cauTruoc })) {
    const thay = cauThayThe(viec, tenBe, cauTruoc);
    /* Thay thì thay CẢ CẶP. Giữ lời tiếng Việt cũ là để nó tả một câu đã bị bỏ —
       đã thấy thật: cô nói "Hi, I'm Bill." mà lời Việt vẫn là "Chào tạm biệt bike".
       Bé nghe hai thứ ngược nhau còn rối hơn là nghe câu sai. */
    if (thay) return { ...tra, en: thay.en, vi: thay.vi, buoc: null, daThay: true };
  }
  return { ...tra, buoc: null, vi: loiVietSach(tra.vi, { von, cauDich: tra.en, beNoi: luotBe?.chu }) };
}

/**
 * Lời tiếng Việt đã soi. Hỏng thì LUI, chứ không sửa chữa nửa vời.
 *
 * Sửa tay một câu hỏng ("bạn" → "con") nghe thì tiện, nhưng câu ấy có thể hỏng cả
 * ý chứ không chỉ hỏng một chữ — cô nhắc lại một từ bé chưa từng nói thì đổi đại
 * từ không cứu được gì. Thà lui hẳn về lời viết sẵn của bước ấy: nó chung chung
 * hơn, nhưng luôn đúng và luôn nói trúng chỗ khó của bài.
 *
 * Không có lời viết sẵn (bài chưa có kịch bản) thì dùng một câu mời tối giản —
 * bé phải biết mình cần làm gì, dù cô có nói vụng.
 */
const LUI_CHUNG = 'Con nghe rồi nói lại nhé.';

export function loiVietSach(vi, { von, cauDich = '', lui = '', beNoi = '' } = {}) {
  const kq = loiVietHopLe(vi, { von, cauDich, beNoi });
  if (kq.ok) return vi;
  LOI_LOI_VIET.so += 1;
  LOI_LOI_VIET.ganNhat = kq.vi;
  return lui || LUI_CHUNG;
}

/**
 * Đếm số lần phải lui. Không hiện ra màn hình — bé đang học thì không việc gì
 * phải thấy — nhưng cũng KHÔNG nuốt im: lui nhiều nghĩa là lời dặn đang không ăn,
 * và không có con số thì chẳng ai biết để mà sửa lời dặn.
 */
export const LOI_LOI_VIET = { so: 0, ganNhat: null };

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
