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
  soiCau, loiNhacSua, loiNhacSuaViet, SUA_CO_TOI_DA, luotLuyen,
} from './phongnoi.js';
import { nhanLuot, NHAN_TRONG_KICH_BAN } from './nhanluot.js';
import { canHoiCo, dungKho } from './hoico.js';
import { buocHienTai, dongBuocKeHoach } from './kehoach.js';
import { loiDanTomTat, docTomTat, soiGoiTomTat } from './baihoc.js';

/** Collection riêng của Tiếng Anh — hậu tố TA để không bao giờ lẫn với Toán. */
export const KHO_PHONG_NOI = (uid) => `phongNoiTA/${uid}/buoi`;

/**
 * MỘT lời gọi lên callable `luyenNoi` — TÁCH RA để tiêm được hàm giả trong cổng.
 *
 * Vòng gọi lại của V1 chỉ đo được bằng cách đếm SỐ LẦN gọi mạng, mà `httpsCallable`
 * viết thẳng trong thân hàm thì không có chỗ nào đếm được. §0 luật 7 của bản rà
 * 09-10 nói rõ: tiêm hàm mạng qua tham số, không mock module — nên phần mạng gom
 * về đúng một hàm, và `hoiCoGiao` nhận nó qua `{ goi }`.
 *
 * Chốt "chưa nối được mạng" nằm luôn ở đây, không nằm đầu `hoiCoGiao`: tiêm hàm
 * giả thì không có Firebase nào cả, mà cổng vẫn phải chạy được bằng `node`.
 */
async function goiMay(messages) {
  if (!hasFirebase || !fns) {
    const e = new Error('Máy chưa nối được lên mạng.');
    e.code = 'functions/unavailable';
    throw e;
  }
  return httpsCallable(fns, 'luyenNoi')({ messages });
}

/**
 * MỘT lời gọi lên callable `luyenNoiTool` — nhánh ReAct của việc V11.
 *
 * Tách riêng khỏi `goiMay` chứ không thêm một tham số: hai callable khác nhau, hai
 * chốt cửa khác nhau, và quan trọng hơn — cổng phải đếm được RIÊNG số lần đi nhánh
 * tra. Gộp vào một hàm thì "đã gọi mấy lần" không còn nói được nhánh nào đã chạy.
 */
async function goiMayCoTool(messages, kho) {
  if (!hasFirebase || !fns) {
    const e = new Error('Máy chưa nối được lên mạng.');
    e.code = 'functions/unavailable';
    throw e;
  }
  return httpsCallable(fns, 'luyenNoiTool')({ messages, kho });
}

/**
 * Đếm vòng gọi lại. `so` = số lần phải xin lại, `thanh` = số lần xin lại ĂN.
 *
 * Tỉ số `thanh/so` là thứ DUY NHẤT nói được vòng này có tác dụng hay chỉ tốn thêm
 * một lời gọi mạng. Không hiện ra màn hình — bé đang học thì không việc gì phải
 * thấy — nhưng cũng không nuốt im, đúng lối `LOI_LUU` và `LOI_LOI_VIET`.
 */
export const LOI_SUA_CO = { so: 0, thanh: 0, ganNhat: null };

/**
 * Đếm nhánh tra (việc V11). `goi` = số lượt rẽ vào, `buoc` = tổng số bước tool đã
 * chạy, `hong` = số lần phải lùi về nhánh cũ.
 *
 * Tỉ số `buoc/goi` là thứ nói được mô hình có THẬT SỰ tra hay chỉ trả lời ngay: nếu
 * nó quanh 0 thì cả nhánh này chỉ tốn thêm một callable mà không ai dùng tool, và
 * lúc ấy việc đúng là bỏ nhánh đi chứ không phải dặn thêm.
 */
export const LOI_HOI_CO = { goi: 0, buoc: 0, hong: 0, ganNhat: null };

/** Trần ký tự khi trả CÂU BỊ BÁC lại cho mô hình xem. */
export const TRA_LAI_TOI_DA_CHU = 600;

/* Lượt bị bác phải quay lại gói dưới vai `assistant`: mô hình cần thấy CHÍNH câu
   nó vừa nói mới hiểu "câu ấy" trong lời nhắc là câu nào. Cắt ngắn trước khi gửi —
   `soiGoi` chặn lượt dài quá `TOI_DA_CHU_MOT_LUOT`, và một câu đã bị bác thì không
   đáng tốn thêm chỗ. Vẫn là JSON đúng khuôn mô hình được dặn trả. */
const laiNoi = (tra) => JSON.stringify({
  en: String(tra?.en || '').slice(0, TRA_LAI_TOI_DA_CHU),
  vi: String(tra?.vi || '').slice(0, TRA_LAI_TOI_DA_CHU),
});

/**
 * Hỏi cô giáo máy một lượt.
 *
 * @param goi  hàm gọi mạng — mặc định `goiMay`; cổng tiêm hàm giả vào đây.
 * @return {{en, vi, thoJSON, lanSua}} — đã bóc sẵn để màn hình đọc hai thứ tiếng
 *         riêng; `lanSua` là số lần phải xin lại câu tiếng Anh ở lượt này.
 * @throws lỗi có `.code` của Firebase để màn hình nói đúng chỗ hỏng.
 */
export async function hoiCoGiao({
  von, lichSu, tenBe, lop, haDoKho = false, hoSo = null, kichBan = null,
  /* BẢNG TRẠNG THÁI (việc V6) — đường chính từ nay. `hoSo` rời vẫn nhận, vì mọi
     cổng hiện có truyền nó, và `bang.hoSo` giữ đúng hình dạng cũ nên hai đường ra
     cùng một chỗ. */
  bang = null,
}, { goi = goiMay, goiTool = goiMayCoTool } = {}) {
  const hs = bang?.hoSo || hoSo;
  /* Việc của lượt này do MÁY CON quyết rồi ghép vào lời dặn — xem `viecTiepTheo`.
     Lời dặn dựng lại mỗi lượt (chứ không giữ nguyên từ đầu buổi) chính là chỗ cắm
     được việc mới vào. */
  /* CÓ KỊCH BẢN thì câu tiếng Anh lấy thẳng từ đó, mô hình chỉ viết lời tiếng Việt.
     Không có (bài chưa sinh kịch bản) thì rơi về cách cũ — máy con tự chọn việc. */
  /* Lượt vừa rồi của bé — kèm ĐIỂM và những chữ bé bỏ sót. `goiGui` cắt sạch mấy
     thứ ấy khi gửi lịch sử (nó chỉ gửi vai + chữ), nên nếu không đi đường này thì
     mô hình không có cách nào biết bé nói được mấy điểm. Xem `dongBuoc`. */
  const luotBe = luotBeCuoi(lichSu);
  /* ── NHÃN CHO LƯỢT VỪA RỒI CỦA BÉ ── (việc V2, mẫu Routing)
     Thuần code, không tốn một lời gọi nào: nhãn suy ra từ chính con số `chamCau`
     đã tính. Nó lái HAI thứ — việc của lượt này (`viecTiepTheo`) và lời dặn
     (`loiDan`) — nên phải tính TRƯỚC cả hai. */
  const { nhan, doTin, chiTiet } = nhanLuot(luotBe, { von });
  const buoc = kichBan ? buocTiepTheo({ kichBan, lichSu, hoSo: hs, haDoKho }) : null;
  /* ── KẾ HOẠCH BUỔI (việc V7) ──
     Kịch bản của bài vẫn ĐI TRƯỚC: nó biết trước câu đúng, còn kế hoạch chỉ xếp
     thứ tự. Kế hoạch áp cho phần luyện TỰ DO, tức nhánh không kịch bản.
     ⚠ Bước kế hoạch KHÔNG đổi khi bé đang đuối: `viecGiuLai` bên trong
     `viecTiepTheo` vẫn thắng, vì bé vừa sai thì việc của lượt là sửa đúng câu ấy. */
  const buocKH = buoc ? null : buocHienTai(bang?.keHoach);
  const viec = buoc ? null
    : viecTiepTheo({ von, lichSu, haDoKho, hoSo: hs, nhan, buocKH });
  const dongKH = buoc ? '' : dongBuocKeHoach(bang?.keHoach);
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
  /* CÓ KỊCH BẢN thì chỉ ghép BA nhãn mà kịch bản không có chỗ nào nói tới — xem
     `NHAN_TRONG_KICH_BAN`. Ghép cả chín vào là `dongBuoc` và dòng nhãn cùng ra
     lệnh về một câu, và mô hình nghe cái nào thì không ai đoán được. */
  const nhanKB = NHAN_TRONG_KICH_BAN.has(nhan) ? nhan : null;
  const dan = laTranh
    ? loiDanTranh({ tenBe, lop, kichBan, buoc, luotBe })
    : (buoc
      ? `${loiDan({ von, tenBe, lop, viec: null, hoSo: hs, unit, nhan: nhanKB, chiTiet, bang })}\n${dongBuoc(buoc, { tenBe, thich: hs?.thich }, luotBe)}`
      : loiDan({ von, tenBe, lop, viec, hoSo: hs, unit, nhan, chiTiet, bang,
                 dongKeHoach: dongKH }));
  const messages = [{ role: 'system', content: dan }, ...goiGui(lichSu)];

  /* ── BÉ HỎI LẠI VÀ TỪ LỚP 3: CHO CÔ ĐI TRA TRƯỚC KHI ĐÁP (việc V11) ──
     Luật rẽ ở `hoico.js`, thuần và có cổng. Nhánh này gửi thêm gói `kho` để bốn
     tool chạy được trên dữ liệu bài — máy chủ không có dữ liệu riêng.

     ⚠ HỎNG THÌ LÙI VỀ NHÁNH CŨ, KHÔNG ĐỂ BÉ MẤT LƯỢT. Nhánh tra là đường THÊM: nó
     tốn một lượt gọi nữa và dùng một callable mới, nên nó có nhiều chỗ hỏng hơn —
     chưa deploy hàm mới, mô hình không chịu gọi tool, Groq bác gói có `tools`. Lùi
     về `goi(messages)` thì bé vẫn được trả lời bằng bảng vốn trong lời dặn, đúng
     như trước V11. */
  const traLoiBangTool = canHoiCo({ nhan, lop, laTranh });
  let data;
  let buocTool = null;
  if (traLoiBangTool) {
    try {
      const r = await goiTool(messages, dungKho({
        von, mucThao: bang?.mucThao || null, doThi: bang?.doThi || null,
      }));
      data = r?.data;
      buocTool = data?.buocTool || null;
      LOI_HOI_CO.goi += 1;
      LOI_HOI_CO.buoc += buocTool?.length || 0;
      LOI_HOI_CO.ganNhat = data?.lyDoDung || null;
    } catch (e) {
      LOI_HOI_CO.hong += 1;
      LOI_HOI_CO.ganNhat = e?.code || e?.message || 'khong-ro';
      data = null;
    }
  }
  if (!data) ({ data } = await goi(messages));
  const tra = docTraLoi(data?.chu);
  /* Vân tay lời dặn đi kèm ra ngoài — cùng lý do với `goiChamViet.js`: mục 2.5.2
     đòi mỗi bản ghi biết nó do mẫu prompt nào sinh ra. `luyennoi.js` sinh sẵn từ
     21-08, chỉ là chưa ai chuyền tiếp. */
  if (tra) {
    tra.mauPrompt = data?.mauPrompt || null;
    tra.phienBanMau = data?.phienBanMau ?? null;
    tra.vanTayPrompt = data?.vanTayPrompt || null;
    /* Gắn vào `tra` chứ không thêm vào từng câu `return`: hàm này có BỐN đường ra
       (hai ở nhánh kịch bản, hai ở nhánh thường) và cả bốn đều `...tra`. Thêm tay
       vào từng đường thì sớm muộn sót một đường, mà đường sót chính là đường ít ai
       đi qua — tức nhãn mất ở đúng chỗ khó lần ra nhất.
       ⚠ KHÔNG gắn `chiTiet`: trong đó có chữ bé vừa nói, và `tra` thì đi thẳng vào
       `lichSu` rồi lên `phongNoiTA`. Lời bé nói đã được lưu một lần ở lượt của
       chính bé; lưu thêm một bản trong lượt của cô là nhân đôi vô cớ. */
    tra.nhan = nhan;
    tra.doTin = doTin;
    /* Lượt mà máy chủ phải NỚI KHUÔN JSON mới lấy được câu trả lời. Đếm được thì
       mới biết lỗi 400 của buổi dài đã hết hẳn hay chỉ bị đẩy xuống một tầng —
       xem `LOI_NOI_KHUON` ở `functions/src/luyennoi.js`. */
    tra.noiKhuon = data?.noiKhuon === true;
    /* Lượt này thuộc bước kế hoạch thứ mấy — màn hình giữ lại để `capNhatSauLuot`
       biết đang chấm bước nào, và để bản ghi buổi đếm được bước nào hay mắc. */
    tra.buocKeHoach = buocKH?.i ?? null;
    /* Danh sách bước tra của nhánh ReAct. Màn hình đọc nó để biết có phải phát
       clip hay không (`tuCanPhat`), và bản ghi buổi đếm được nhánh ấy chạy mấy lần.
       ⚠ Không mang chữ nào của bé — tham số tool là chữ tiếng Anh của bài. */
    tra.buocTool = buocTool;
  }

  /* SOI LẠI CÂU TIẾNG ANH. Dặn dò không đủ: đã bảo rõ ô trống của `Bye, + [Name].`
     là chỗ của tên người, mô hình vẫn sinh ra "Bye, bike." Bé 6 tuổi đang tập nhại
     thì một câu sai là dạy sai. Không hợp lệ thì thay bằng câu máy con tự dựng —
     luôn đúng, vì nó ghép từ chính dữ liệu bài. */
  const cauTruocThat = [...lichSu].reverse().find((x) => x.vai === 'may')?.en || '';
  /* ══ LƯỢT GIỮ VIỆC THÌ TẮT LUẬT CHỐNG LẶP ══
     Đo thật 09-10 với Groq: bé sai thì KHÔNG LẦN NÀO cô nhắc lại đúng câu bé đang
     tập, kể cả sau khi lời dặn đã nói thẳng "SAY IT AGAIN, unchanged". Chỗ hỏng
     không ở lời dặn mà ở ĐÂY.

     `soiCau` bác câu trùng lượt trước với lý do `lap` — luật ấy đúng và sinh ra để
     chữa "nó cứ nói đi nói lại". Nhưng ở lượt GIỮ VIỆC thì lặp lại CHÍNH LÀ việc
     cần làm, nên mô hình trả về câu đúng và bị chốt soi gạt. Rồi vòng gọi lại của
     V1 đọc `bac === 'lap'` và nhắc nó "Say a DIFFERENT sentence — change the word
     in the slot", tức ĐẨY nó đi sai. Ba tầng đều làm đúng phận mình và cộng lại
     thành hỏng: cô không bao giờ đọc lại được câu bé cần.

     Nhánh kịch bản không gặp chuyện này vì nó bỏ qua `cauHopLe` khi đã biết câu
     đúng. Nhánh thường nay làm điều tương đương: không có "lượt trước" để so.
     ⚠ Chỉ TẮT ĐÚNG MỘT LUẬT. Bốn đường công nhận vốn từ vẫn soi như cũ — câu vẫn
     phải nằm trong vốn của bài. */
  const cauTruoc = viec?.giuViec ? '' : cauTruocThat;

  /* CÓ KỊCH BẢN: câu đúng đã biết trước, nên không cần đoán — sai thì ép về đúng
     câu ấy. Đây là chỗ chữ "đảm bảo hơn" của bác thành thật: mô hình có chệch thì
     bé vẫn nghe đúng câu của bài. */
  if (buoc) {
    const dung = dienBuoc(buoc, { tenBe, thich: hs?.thich });
    /* ⚠ BƯỚC KHÔNG CÓ CÂU VIẾT SẴN VẪN PHẢI SOI.
       `hoiThich` không mang câu tiếng Anh nào — thẻ chọn hình do máy con tự vẽ. Nên
       `dung` rỗng, và dòng dưới cho `tra.en` đi thẳng. Mà nhánh có kịch bản thì cố
       ý bỏ qua `cauHopLe` (câu đã biết trước, soi làm gì) — cộng lại thành đúng MỘT
       lượt mỗi buổi mà câu của mô hình không ai soi. Đúng lượt thứ hai, lượt bé
       vừa mới vào phòng. Không gì kêu: câu ấy thường vẫn đúng. */
    if (!dung && !cauHopLe(tra.en, { von, tenBe, cauTruoc: cauTruocThat })) {
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
    /* ⚠ TÍNH `vi` TRƯỚC KHI DỰNG OBJECT, không viết `vi: await ...` trong object.
       `{ ...tra, vi: await f(tra) }` sao chép `tra` XONG rồi mới chờ — nên mấy
       trường `f` gắn thêm vào `tra` (`lanSuaViet`) bị object này bỏ lại phía sau.
       `beNoi` đi kèm để lời SỬA được phép trích lại đúng chữ bé vừa nói — không có
       nó thì lượt sửa nào cũng bị gạt rồi lui về câu chung chung. */
    const vi = await loiVietGoiLai({
      goi, messages, tra, von, cauDich: en, lui: buoc.vi, beNoi: luotBe?.chu,
    });
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
      vi,
      daThay: en !== tra.en };
  }

  /* ── VÒNG GỌI LẠI (mẫu Evaluator–Optimizer, việc V1 của bản rà 09-10) ──
     Bác một câu rồi rơi thẳng về `cauThayThe` là bỏ mất cô giáo đúng lượt bé cần
     cô nhất — xem lập luận dài ở `SUA_CO_TOI_DA` trong `phongnoi.js`. Nên nói cho
     mô hình biết nó sai CHỖ NÀO (`xet.bac` có tên hẳn hoi) rồi xin lại câu khác.

     ⚠ `cauTruoc` KHÔNG đổi giữa các vòng. Câu bị bác không vào `lichSu` hiển thị,
     nên "lượt trước" của luật chống lặp vẫn là lượt cô đã nói THẬT với bé. Lấy câu
     vừa bị bác làm `cauTruoc` thì vòng hai bác nó vì "lặp" — bác chính cái câu mà
     vòng một vừa bác vì lý do khác, và lời nhắc chỉ đúng chỗ sai mới nhất.

     Gói gửi lên dài nhất: 1 lời dặn + 12 lượt lịch sử + 2×2 (vòng câu Anh) + 2
     (vòng lời Việt) = 19 ≤ `TOI_DA_LUOT` 24 của `luyennoi.js`. Luật máy chủ không
     phải đổi một chữ. */
  let xet = soiCau(tra.en, { von, tenBe, cauTruoc });
  let lanSua = 0;
  while (!xet.ok && lanSua < SUA_CO_TOI_DA) {
    messages.push({ role: 'assistant', content: laiNoi(tra) });
    messages.push({ role: 'user',
      content: loiNhacSua(xet.bac, { von, cauTruoc, en: tra.en, tenBe }) });
    lanSua += 1;
    LOI_SUA_CO.so += 1;
    LOI_SUA_CO.ganNhat = xet.bac;
    const { data: lai } = await goi(messages);
    const moi = docTraLoi(lai?.chu);
    /* Ghi ĐÈ lên `tra`, không dựng object mới: `mauPrompt` · `phienBanMau` ·
       `vanTayPrompt` phải giữ nguyên, vì lời dặn (thứ vân tay ấy mô tả) không đổi
       một chữ giữa các vòng — chỉ có lượt `user` nhắc sửa là mới. */
    tra.en = moi.en;
    tra.vi = moi.vi;
    tra.thoJSON = moi.thoJSON;
    xet = soiCau(tra.en, { von, tenBe, cauTruoc });
    if (xet.ok) LOI_SUA_CO.thanh += 1;
  }
  if (lanSua && import.meta.env?.DEV) {
    // eslint-disable-next-line no-console
    console.info('[tienganh] xin lại câu của cô', lanSua, 'lần —',
      xet.ok ? `đã qua (${xet.duong})` : `vẫn trượt (${xet.bac}), lui về câu máy dựng`);
  }

  if (!xet.ok) {
    const thay = cauThayThe(viec, tenBe, cauTruoc);
    /* Thay thì thay CẢ CẶP. Giữ lời tiếng Việt cũ là để nó tả một câu đã bị bỏ —
       đã thấy thật: cô nói "Hi, I'm Bill." mà lời Việt vẫn là "Chào tạm biệt bike".
       Bé nghe hai thứ ngược nhau còn rối hơn là nghe câu sai. */
    if (thay) {
      return { ...tra, en: thay.en, vi: thay.vi, buoc: null, lanSua, daThay: true };
    }
  }
  const vi = await loiVietGoiLai({
    goi, messages, tra, von, cauDich: tra.en, beNoi: luotBe?.chu,
  });
  return { ...tra, buoc: null, lanSua, vi };
}

/**
 * LỜI TIẾNG VIỆT: XIN LẠI MỘT LẦN TRƯỚC KHI LUI.
 *
 * `loiVietSach` lui ngay về lời viết sẵn của bước — an toàn, nhưng lời viết sẵn
 * chung chung, và nó lui đúng lượt cần lời cụ thể nhất: lượt cô SỬA cho bé. Hai lý
 * do hỏng hay gặp (gọi bé bằng "bạn"; nhắc lại một chữ bài không dạy) đều là lỗi
 * DIỄN ĐẠT, nói ra là mô hình sửa được.
 *
 * ⚠ ĐÚNG MỘT VÒNG, không phải `SUA_CO_TOI_DA` vòng. Câu tiếng Anh — thứ bé sẽ nhại
 * — đã đúng rồi; cái còn lại chỉ là một dòng cô giảng, mà bé thì đang ngồi đợi.
 *
 * Mất mạng giữa buổi thì LUI, không làm hỏng cả lượt: câu tiếng Anh đã có trong
 * tay, không có lý gì để bé mất luôn nó vì một lời giảng không xin lại được.
 */
export async function loiVietGoiLai({
  goi, messages, tra, von, cauDich = '', lui = '', beNoi = '',
}) {
  const kq = loiVietHopLe(tra.vi, { von, cauDich, beNoi });
  if (kq.ok) return tra.vi;
  LOI_SUA_CO.so += 1;
  LOI_SUA_CO.ganNhat = `vi: ${kq.vi}`;
  try {
    messages.push({ role: 'assistant', content: laiNoi(tra) });
    messages.push({ role: 'user',
      content: loiNhacSuaViet(kq, { en: cauDich || tra.en, von }) });
    const { data } = await goi(messages);
    const moi = docTraLoi(data?.chu);
    if (loiVietHopLe(moi.vi, { von, cauDich, beNoi }).ok) {
      LOI_SUA_CO.thanh += 1;
      tra.lanSuaViet = 1;
      return moi.vi;
    }
  } catch (e) {
    LOI_SUA_CO.ganNhat = `vi-goi-lai-hong: ${String(e?.code || e?.message || e)}`;
  }
  /* Vẫn hỏng thì đi đúng đường cũ — `loiVietSach` đếm `LOI_LOI_VIET` như xưa, nên
     con số "số lần phải lui" không đổi nghĩa vì có thêm vòng này. */
  return loiVietSach(tra.vi, { von, cauDich, lui, beNoi });
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
 * Đếm số lần lượt tóm tắt cuối buổi KHÔNG lấy được bài học nào.
 *
 * Tách `hong` (mạng · máy chủ) khỏi `bac` (soi bác sạch): hai con số ấy đòi hai cách
 * chữa khác nhau — một cái là hạ tầng, một cái là lời dặn. Gộp lại thì nhìn con số
 * không biết phải sửa gì.
 */
export const LOI_TOM_TAT = { goi: 0, hong: 0, bac: 0, ganNhat: null };

/**
 * TÓM TẮT CUỐI BUỔI — một lượt gọi, và chỉ một (mẫu Reflexion, việc V8).
 *
 * ── DÙNG LẠI CALLABLE `luyenNoi`, KHÔNG THÊM CALLABLE MỚI ──
 * §7 cho hai cách. Chọn cách này vì gói gửi lên có HÌNH DẠNG Y HỆT một lượt nói
 * chuyện: một `system` + lịch sử. `soiGoi` chốt cửa đúng như cũ, và máy chủ không
 * phải đổi một dòng nào — thêm một callable là thêm một chỗ phải khai secret, khai
 * region, và deploy. Lời dặn khác thì `locKhung` ra vân tay khác, nên bảng so ΔC
 * vẫn tách được hai mẫu.
 *
 * ── KHÔNG CHỜ, VÀ KHÔNG NUỐT IM ──
 * Chỗ gọi không `await` cái này: buổi đã kết, bé đang xem màn kết, và một lời gọi
 * mạng nữa không được phép giữ màn hình lại. Hỏng thì bỏ qua — nhưng `LOI_TOM_TAT`
 * đếm, vì "không có bài học nào" mà không ai biết thì cả việc V8 thành vô dụng mà
 * vẫn trông như đang chạy.
 *
 * @return {{baiHoc, khen, boQua}} — ĐÃ SOI. Chỗ gọi chỉ việc `themBaiHoc`.
 */
export async function tomTatBuoi({ von, lichSu, tenBe, lop }, { goi = goiMay } = {}) {
  LOI_TOM_TAT.goi += 1;
  const rong = { baiHoc: [], khen: '', boQua: [] };
  /* Buổi quá ngắn thì không có gì để ngẫm — đừng tốn một lời gọi. Hai lượt luyện là
     sàn: một lượt thì không có cái gì "lặp lại", mà bài học phải là cái LẶP LẠI. */
  if (luotLuyen(lichSu || []).length < 2) return rong;
  const messages = [
    { role: 'system', content: loiDanTomTat({ von, tenBe, lop }) },
    ...goiGui(lichSu),
  ];
  let tt = null;
  try {
    const { data } = await goi(messages);
    tt = docTomTat(data?.chu);
  } catch (e) {
    LOI_TOM_TAT.hong += 1;
    LOI_TOM_TAT.ganNhat = String(e?.code || e?.message || e);
    return rong;
  }
  if (!tt) {
    LOI_TOM_TAT.hong += 1;
    LOI_TOM_TAT.ganNhat = 'không đọc được JSON';
    return rong;
  }
  const kq = soiGoiTomTat(tt, { von });
  if (!kq.baiHoc.length && kq.boQua.length) {
    LOI_TOM_TAT.bac += 1;
    LOI_TOM_TAT.ganNhat = kq.boQua[0]?.vi || 'bị soi bác';
  }
  return kq;
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
      /* `lanSua` đi theo bản ghi buổi, không theo màn hình — xem `PhongNoi.jsx`. */
      luot: lichSu.map((x) => ({
        vai: x.vai, chu: x.chu, en: x.en || null, vi: x.vi || null,
        lanSua: x.lanSua ?? null, lanSuaViet: x.lanSuaViet ?? null,
        nhan: x.nhan ?? null, doTin: x.doTin ?? null, noiKhuon: x.noiKhuon ?? null,
      })),
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
