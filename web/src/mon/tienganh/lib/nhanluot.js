/**
 * PHÂN LOẠI LƯỢT CỦA BÉ — một nhãn cho mỗi lượt, bằng CODE, không gọi mạng.
 *
 * ── VÌ SAO PHẢI CÓ ──
 * Trước bản này cô giáo máy nhận MỘT lời dặn cho mọi tình huống: bé nói đúng, bé
 * sót chữ, bé đảo thứ tự, bé hỏi lại, bé im lặng — mười điều luật y như nhau. Mà
 * mười điều thì mô hình phải tự đoán điều nào đang áp dụng, và nó đoán theo thứ
 * nhiều chữ nhất: "dạy bé nhại câu". Nên lượt nào cũng ra một lời khen chung chung
 * rồi đi tiếp, kể cả lượt bé vừa trượt. Đúng chỗ bác gọi là "như máy".
 *
 * Việc chọn lời dặn nào thì KHÔNG phải việc của mô hình: nó suy được từ chính con
 * số `chamCau` đã tính (`diem` · `thieu` · `mau`), tức suy được bằng code. Và suy
 * bằng code thì không tốn một lời gọi nào, chạy được bằng `node`, và cổng soi được.
 *
 * ── MỘT NHÃN, KHÔNG PHẢI MỘT ĐIỂM SỐ ──
 * Nhãn trả về kèm `doTin` để chỗ gọi biết nhãn ấy chắc đến đâu: suy từ điểm và
 * chữ thiếu thì chắc (bằng 1), suy từ dấu tiếng Việt thì chỉ là đoán (0,6). Có
 * `doTin` thì về sau thêm nhánh đoán mới không phải sửa chỗ gọi.
 */
import { DAT } from './chamnoi.js';

/**
 * CHÍN NHÃN. Khai thành hằng để cổng đếm được, và để `loidan_nhan.js` không bao
 * giờ lệch một chữ với tệp này — lệch một chữ là một nhãn không có lời dặn, và
 * lượt ấy rơi về lời dặn rỗng mà không gì kêu.
 */
export const NHAN = {
  dung: 'dung',
  thieuTu: 'thieuTu',
  saiThuTu: 'saiThuTu',
  nhamTu: 'nhamTu',
  tiengViet: 'tiengViet',
  hoiLai: 'hoiLai',
  imLang: 'imLang',
  lacDe: 'lacDe',
  moDau: 'moDau',
};

/**
 * NHÃN NÀO GIỮ NGUYÊN VIỆC CỦA LƯỢT TRƯỚC.
 *
 * ⚠ LỆCH VỚI BẢN RÀ, CÓ Ý. §7 chỉ kể ba nhãn `thieuTu · saiThuTu · nhamTu`. Nhưng
 * đọc chính chín lời dặn ở §9 thì bốn nhãn còn lại cũng đòi y như thế:
 *   A6 `tiengViet` — "invite her to try the SAME English target again"
 *   A7 `hoiLai`    — "otherwise the current target sentence"
 *   A8 `imLang`    — "the FIRST word of the target"
 *   A9 `lacDe`     — "Restate the target task"
 * Để `viecTiepTheo` xoay sang việc MỚI ở bốn nhãn ấy thì `dongViec` nói "nói câu
 * A" trong khi dòng theo nhãn ngay trên nói "cho bé thử lại câu B" — hai nửa của
 * cùng một lời dặn chọi nhau, và mô hình nghe nửa nào thì không ai biết. Đó đúng
 * là chỗ hỏng mà V2 sinh ra để dẹp, nên dẹp cho trọn.
 *
 * Còn lại đúng hai nhãn được đi tới việc mới: `dung` (bé nói được rồi) và `moDau`
 * (chưa có việc nào mà giữ). Thành một luật dễ nhớ và dễ bảo vệ: VIỆC CHỈ TIẾN KHI
 * BÉ NÓI ĐÚNG.
 *
 * ⚠ Và vì thế nó phải CÓ TRẦN — xem `SUA_TOI_DA` ở `phongnoi.js`. Giữ việc vô hạn
 * thì bé đuối bị hỏi đúng một câu cho tới hết hai mươi phút; chuyện ấy đã xảy ra
 * thật một lần ở nhánh kịch bản ("mười lượt liền đều là Hello!", ghi ở `buocSua`).
 */
export const NHAN_GIU_VIEC = new Set([
  'thieuTu', 'saiThuTu', 'nhamTu', 'tiengViet', 'hoiLai', 'imLang', 'lacDe',
]);

/**
 * NHÃN NÀO ĐƯỢC GHÉP THÊM VÀO LỜI DẶN KHI BÀI ĐÃ CÓ KỊCH BẢN.
 *
 * Nhánh kịch bản đã biết trước câu đúng và `dongBuoc` đã nói rõ việc của bước —
 * ghép thêm sáu nhãn kia vào là hai chỗ cùng ra lệnh về một câu. Nhưng BA tình
 * huống này thì kịch bản không có chỗ nào nói tới, vì chúng không nằm trong bài:
 * bé hỏi lại, bé nói tiếng Việt, bé im lặng. Thiếu chúng thì cô cứ đọc tiếp bước
 * kế như không có gì xảy ra — đúng cái "như máy".
 */
export const NHAN_TRONG_KICH_BAN = new Set(['hoiLai', 'tiengViet', 'imLang']);

/** Suy từ ĐIỂM và CHỮ THIẾU — những con số `chamCau` đã tính, không phải đoán. */
export const TIN_CHAC = 1;
/** Suy từ DẤU TIẾNG VIỆT — đoán, và đoán sai được. Xem ghi chú ở `laTiengViet`. */
export const TIN_DOAN = 0.6;
/** Dưới ngưỡng này thì nhãn không đáng tin, coi như `lacDe`. */
export const NGUONG_TIN = 0.5;

/* Cùng bộ dấu với `docTraLoi` ở `phongnoi.js`. Không gộp làm một hằng dùng chung:
   hai chỗ trả lời hai câu hỏi khác nhau ("dòng này của mô hình là tiếng gì" ·
   "bé vừa nói tiếng gì"), và gộp lại thì sửa một bên là đổi luôn bên kia. */
const CO_DAU_VIET = /[àáảãạăâèéẻẽẹêìíỉĩịòóỏõọôơùúủũụưỳýỷỹỵđ]/i;

/* Bé ĐANG HỎI, không phải đang kể. Dấu hiệu: câu hỏi, hoặc đang hỏi nghĩa một chữ.
   ⚠ KHÔNG lấy "cô ơi" làm dấu hiệu, dù bản nháp §7 có ghi. Hai ví dụ của chính
   bản rà đều mở đầu bằng "cô ơi" — một cái là hỏi ("cô ơi dog là gì?"), một cái
   không ("cô ơi con không biết"). Thứ có ở CẢ HAI bên thì không phân biệt được bên
   nào; ghim nó vào là nhãn `tiengViet` chết hẳn, vì bé sáu tuổi gọi "cô ơi" trước
   gần như mọi câu. */
const HOI_LAI = /\?|là gì|nghĩa là|nghĩa của|sao ạ|thế nào/i;

const laTiengViet = (s) => CO_DAU_VIET.test(s);

/**
 * NHÃN CHO MỘT LƯỢT CỦA BÉ.
 *
 * @param luotBe  lượt bé gần nhất ĐÃ ĐƯỢC CHẤM — đúng hình dạng `PhongNoi.jsx`
 *                đẩy vào `lichSu`: `{ chu, diem, mau, thieu, thieuChucNang,
 *                nhamThanh? }`. `null` nghĩa là bé chưa nói câu nào được chấm.
 * @return { nhan, doTin, chiTiet } — `chiTiet` là thứ lời dặn cần trích lại:
 *         mảng chữ thiếu (`thieuTu`), hoặc `{ dich, nham }` (`nhamTu`).
 *
 * Thứ tự các nhánh là CÓ Ý: nhánh nào suy từ dữ liệu chắc hơn thì đứng trước.
 */
export function nhanLuot(luotBe, { von = null, datNguong = DAT } = {}) {
  const ra = (nhan, doTin, chiTiet = null) => chotTin({ nhan, doTin, chiTiet });

  /* ── CHƯA NÓI CÂU NÀO ĐƯỢC CHẤM → MỞ ĐẦU ──
     Không phải "lịch sử rỗng": `PhongNoi.jsx` mở màn bằng một lượt bé viết sẵn
     ("Chào cô, con muốn tập nói.") KHÔNG có điểm, và `luotBeCuoi` bỏ qua lượt
     không điểm. Nên lượt mở màn thật cũng về đúng nhãn này. */
  if (!luotBe) return ra(NHAN.moDau, TIN_CHAC);

  const chu = String(luotBe.chu ?? '').trim();

  /* ── IM LẶNG ── Bấm nút rồi không nói gì, hoặc máy không nghe ra tiếng nào.
     Đứng trước mọi nhánh khác vì không có chữ thì chẳng nhánh nào suy được gì. */
  if (!chu) return ra(NHAN.imLang, TIN_CHAC);

  /* ── BÉ NÓI TIẾNG VIỆT ── Phải xét TRƯỚC điểm: câu tiếng Việt đem so với một
     câu tiếng Anh thì bao giờ cũng ra điểm thấp, và điểm thấp sẽ bị đọc thành
     "bé nói sai câu" — trong khi bé không hề đang nói sai, bé đang nói với cô.
     Đoán bằng dấu, nên `doTin` chỉ 0,6: "ok" hay "yes" không dấu nào cả. */
  if (laTiengViet(chu)) {
    return HOI_LAI.test(chu)
      ? ra(NHAN.hoiLai, TIN_DOAN, { beNoi: chu })
      : ra(NHAN.tiengViet, TIN_DOAN, { beNoi: chu });
  }

  /* Chưa chấm được (bé kể tự do, bước không có câu mẫu) thì KHÔNG được suy tiếp:
     mấy nhánh dưới đều đọc `diem`, và `diem == null` sẽ lọt xuống `saiThuTu` —
     tức vu cho bé đảo thứ tự một câu chẳng ai đặt ra. */
  if (luotBe.diem == null) return ra(NHAN.lacDe, TIN_DOAN, { beNoi: chu });

  /* ── NÓI ĐÚNG ── Dùng đúng `DAT` của cả phòng, không đặt ngưỡng thứ hai. */
  if (luotBe.diem >= datNguong) return ra(NHAN.dung, TIN_CHAC, { beNoi: chu });

  /* ── NHẦM SANG MỘT CHỮ KHÁC CỦA BÀI ── `chamnoi.chamTu` tính sẵn `nhamThanh`.
     ⚠ Đường này hiện KHÔNG có nguồn trên bản chạy: phòng nói chấm bằng `chamCau`,
     mà `chamCau` không tính `nhamThanh` (chỉ `chamTu` tính). Nhãn vẫn làm, vì nó
     là nhãn đúng cho tình huống ấy và lời dặn của nó khác hẳn `thieuTu`; nhưng
     nói thẳng ra đây để không ai tưởng nó đang chạy. Nối nguồn là việc của V10. */
  if (luotBe.nhamThanh) {
    return ra(NHAN.nhamTu, TIN_CHAC,
      { beNoi: chu, nham: luotBe.nhamThanh, dich: luotBe.mau || null });
  }

  /* ── SÓT CHỮ ── Chữ CÓ NGHĨA bé không nói ra. `thieuChucNang` (is · a · the)
     cố ý KHÔNG tính: bắt bé sáu tuổi chữa mạo từ là bắt sai chỗ. */
  if (Array.isArray(luotBe.thieu) && luotBe.thieu.length) {
    return ra(NHAN.thieuTu, TIN_CHAC,
      { beNoi: chu, thieu: luotBe.thieu, dich: luotBe.mau || null });
  }

  /* ── ĐỦ CHỮ MÀ ĐIỂM THẤP → ĐẢO THỨ TỰ ── Nói đủ chữ có nghĩa, không sót chữ
     nào, mà vẫn dưới ngưỡng: chỗ trượt còn lại là thứ tự (`dayChung` trong
     `chamCau`). Đòi có `mau` vì không có câu đích thì không nói được "đảo so với
     cái gì". */
  if (luotBe.mau) {
    return ra(NHAN.saiThuTu, TIN_CHAC, { beNoi: chu, dich: luotBe.mau });
  }

  /* ── CÒN LẠI ── Nói một thứ không ăn vào việc nào. */
  return ra(NHAN.lacDe, TIN_DOAN, { beNoi: chu });
}

/**
 * Nhãn không đủ tin thì hạ về `lacDe` — lời dặn của `lacDe` là lời dặn KHÔNG ĐOÁN
 * gì về bé, nên nó an toàn cho mọi tình huống.
 *
 * ⚠ NÓI THẲNG: với chín nhánh hiện có, hàm này KHÔNG BAO GIỜ đổi được nhãn nào —
 * nhánh thấp nhất là 0,6, vẫn trên `NGUONG_TIN` 0,5. Giữ nó lại vì nó là chỗ DUY
 * NHẤT biết luật "nhãn yếu thì đừng tin", và thêm một nhánh đoán mới (nhận dạng
 * tiếng nói chẳng hạn) là nó có việc ngay. Cổng gọi thẳng hàm này để nó không
 * thành mã chết — chứ không chờ một nhánh thật rơi xuống dưới ngưỡng.
 */
export function chotTin(kq) {
  if (kq.nhan !== NHAN.lacDe && kq.doTin < NGUONG_TIN) {
    return { nhan: NHAN.lacDe, doTin: kq.doTin, chiTiet: kq.chiTiet, haTu: kq.nhan };
  }
  return kq;
}
