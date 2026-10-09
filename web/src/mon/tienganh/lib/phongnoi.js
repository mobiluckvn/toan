/**
 * PHÒNG LUYỆN NÓI — luật vốn từ và ngữ cảnh, để riêng khỏi giao diện và khỏi mạng.
 *
 * Màn hình là một cuộc trò chuyện: máy nói một câu tiếng Anh kèm một lời giải thích
 * tiếng Việt, bé nghe rồi nói lại. Khác chặng "Nói chuyện" ở chỗ chặng ấy đi theo
 * kịch bản viết sẵn, còn ở đây câu do máy sinh — nên bé hỏi lại được, nói sai thì
 * được nói lại theo cách khác, và không bao giờ hết câu.
 *
 * ── VÌ SAO PHẢI BÓ VỐN TỪ, VÀ BÓ THEO UNIT ──
 * Bác chốt 13-08: phòng này nằm TRONG từng unit, nên nó phải xoay quanh đúng từ và
 * cấu trúc của unit ấy. Thả cho máy dùng từ tự do thì nó nói "Do you like chips?"
 * với bé vừa xong unit 1 — bé không hiểu, và cái bé học được không phải tiếng Anh
 * mà là "mình kém". Đúng cái bẫy mà luật đi lần lượt sinh ra để tránh.
 *
 * Nhưng bó CỨNG vào một unit thì bé xong unit rồi vẫn chỉ được nói mãi bốn từ, mà
 * quên từ cũ mới là chuyện hay xảy ra nhất với bé lớp 1. Nên hai chế độ:
 *
 *   chưa đạt unit → CHỈ từ và cấu trúc của chính unit ấy
 *   đạt rồi      → cộng thêm từ và cấu trúc của các unit bé ĐÃ ĐẠT trước đó
 *
 * Vế sau là phần thưởng nhìn thấy được: học xong thì phòng nói rộng ra.
 *
 * ── VÌ SAO TỆP NÀY KHÔNG BIẾT GÌ VỀ MẠNG ──
 * Toàn bộ ở đây là hàm thuần: nhận dữ liệu bài + sổ tiến độ, trả về vốn từ và lời
 * dặn cho máy. Không `fetch`, không Firebase. Nhờ thế cổng chạy được bằng `node`
 * và soi được đúng cái dễ sai nhất — vốn từ bị nới ra lúc nào không biết.
 */
/* ⚠ Tệp này xưa nay KHÔNG import gì — luật thuần, chạy được bằng `node` trần. Hai
   import dưới giữ nguyên tính ấy: `nhanluot` và `loidan_nhan` cũng thuần, cũng
   không biết tới mạng, và không tệp nào trong ba tệp gọi ngược lại tệp kia (đã
   kiểm: không có vòng). Lời dặn theo nhãn phải nằm trong `loiDan` chứ không ghép
   ở chỗ gọi, vì chỗ ghép mới là chỗ quyết định nó đứng TRƯỚC hay SAU `dongViec`. */
import { NHAN_GIU_VIEC } from './nhanluot.js';
import { dongTheoNhan } from './loidan_nhan.js';
/* Khối "ABOUT THE CHILD" nay do BẢNG TRẠNG THÁI dựng — một chỗ duy nhất, xem
   `lib/bangtrangthai.js`. Trước V6 nó nằm ở `dongHoSo` trong tệp này và
   `dongHoSoAI` ở `hosoai.js`: hai hàm, hai tệp, cùng một khối. */
import { dungBang, tomTatChoLoiDan } from './bangtrangthai.js';

/**
 * DẤU BỌC KHỐI RIÊNG của bé trong lời dặn — tái xuất từ `bangtrangthai.js`.
 *
 * ⚠ Hai chuỗi này là GIAO ƯỚC với `locKhung` ở `functions/src/vantay.js`. Đổi ở
 * đấy mà không đổi ở đây thì chữ của bé lọt vào vân tay prompt, và không gì báo —
 * đúng chỗ sót mà `luyennoi.js` đã nói trước là sẽ sót. Cổng `vantay_prompt` soi
 * bằng cách dựng hai bé khác hẳn nhau rồi đòi khung bằng nhau.
 */
export { DAU_KHOI_RIENG, CUOI_KHOI_RIENG } from './bangtrangthai.js';

/** Nhiều nhất bao nhiêu unit CŨ được trộn vào. Đủ để ôn, không đủ để loãng. */
export const UNIT_CU_TOI_DA = 3;

/**
 * Bao nhiêu lượt gần nhất được gửi lên máy chủ.
 *
 * Ngữ cảnh do CLIENT giữ (bác chốt: server không lưu gì), nên chính client phải cắt.
 * Không cắt thì buổi nói chuyện dài dần, mỗi lượt gửi lại toàn bộ lịch sử — tiền và
 * độ trễ tăng theo bình phương số lượt, mà bé thì chẳng thấy gì khác.
 */
export const LUOT_GUI_TOI_DA = 12;

/** Chặn câu quá dài trước khi gửi. Bé 6 tuổi không gõ, nên dài bất thường là hỏng. */
export const CHU_TOI_DA = 300;

/* ─────────── vốn từ ─────────── */

/* `so_nhieu`·`so_it`·`dang_ing`·`dang_qk` mang theo để ĐIỀN Ô CÔNG THỨC — xem chỗ
   `dienDuoc` trong `cauHopLe`. Không mang thì ô `[Plural Noun]` chỉ điền được dạng
   gốc, và câu của chính sách ("The cakes are on the table.") bị gạt. */
const goiTu = (v) => ({
  tu: v.tu, nghia: v.nghia, ipa: v.ipa,
  so_nhieu: v.so_nhieu, so_it: v.so_it, dang_ing: v.dang_ing, dang_qk: v.dang_qk,
});
const goiCau = (m) => ({ cau: m.cau, congThuc: m.congThuc, dungDe: m.dungDe });

const chuTrongCau = (s) => String(s || '').toLowerCase().match(/[a-z']+/g) || [];

/**
 * SỐ ĐẾM — vốn nền sách MẶC ĐỊNH bé đã có, chứ không dạy.
 *
 * Đã dò cả 16 bài: KHÔNG bài nào có một con số trong danh sách từ mới. Nhưng hai
 * bài lại có công thức đòi hẳn một ô `[Number]` (`How many + [Noun-plural]? -
 * [Number].`), và câu ví dụ của chính sách thì dùng one · two · three · six.
 *
 * Nghĩa là sách coi số đếm là thứ bé biết sẵn — bé lớp 1 đếm tới mười ở giờ Toán
 * trước khi vào giờ tiếng Anh. Đúng, nhưng phải NÓI RA ở đây, vì luật của phòng
 * này là "không từ nào ngoài vốn của bé", mà số thì không nằm trong vốn nào cả.
 *
 * ── CHỖ NÀY KHÁC HẲN "blue" ──
 * Unit 6 có `"It's a blue pen."` mà cả quyển không dạy "blue". Nhìn qua thì giống
 * nhau, nhưng khác ở gốc: MÀU thì sách CÓ dạy thành từ mới ("red" là từ của Unit
 * 6), nên một màu nằm ngoài danh sách là chỗ HỞ của sách. Số thì sách không dạy
 * cái nào cả, ở bất cứ đâu — đó là chủ ý, không phải bỏ sót.
 *
 * Nên: số được nhận, "blue" thì không. Có cổng canh đúng hai chiều ấy, để lần sau
 * đừng ai lấy cớ này mà nới cho một từ lạ khác.
 */
export const SO_DEM = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'];

/**
 * CÂU SẴN CỦA SÁCH — `canonicalExamples`, thứ trước nay bỏ không.
 *
 * ── VÌ SAO PHẢI LẤY ──
 * Ba bài có công thức HAI ô trống (`It's a + [Colour] + [Noun].` ·
 * `How many + [Noun-plural]? - [Number].`). Máy không đoán được ô nào nhận màu, ô
 * nào nhận danh từ — bài không khai — nên bản sinh tự động bỏ hẳn bước "thay" của
 * ba bài ấy. Nhưng SÁCH thì đã tự điền sẵn rồi: "It's a red bell." nằm ngay trong
 * `canonicalExamples`. Không cần đoán, chỉ cần đọc.
 *
 * ── VÌ SAO PHẢI LỌC, DÙ ĐÂY LÀ CÂU CỦA CHÍNH SÁCH ──
 * Unit 6 có `"It's a blue pen."` trong khi cả quyển KHÔNG bài nào dạy từ "blue" —
 * đã dò cả 16 bài. Đây là chỗ hở của sách, không phải của mình, nhưng cứ lấy vào
 * là bé gặp một màu chưa ai dạy và không có gì báo.
 *
 * Nên chỉ nhận câu mà MỌI CHỮ đều là thứ chính bài ấy đã đưa ra: từ mới, hoặc chữ
 * nằm trong mẫu câu / công thức của bài. Không nới ra "cả quyển" — bé mở Unit 6
 * chưa chắc đã học Unit 12.
 *
 * ── VÌ SAO TÁCH ĐÔI Ở " - " ──
 * `"How many clocks? - Two."` là MỘT LƯỢT HỎI và MỘT LƯỢT ĐÁP, không phải một câu.
 * Bắt bé đọc cả cụm là dạy sai nhịp nói. Chính sách cũng tách đôi như thế trong
 * phần `hoiThoai` của nó.
 */
function cauSachCuaBai(k) {
  const mau = k.mauCauDs?.length ? k.mauCauDs : (k.mauCau ? [k.mauCau] : []);
  const biet = new Set([
    ...(k.vocabulary || []).flatMap((v) => chuTrongCau(v.tu)),
    ...mau.flatMap((m) => [...chuTrongCau(m.cau), ...chuTrongCau(m.congThuc)]),
    /* Số đếm chỉ được cộng vào khi công thức của CHÍNH bài ấy đòi một con số. Bài
       nào không có ô `[Number]` thì số vẫn là từ lạ như mọi từ khác. */
    ...(mau.some((m) => /\[Number\]/i.test(m.congThuc || '')) ? SO_DEM : []),
  ]);
  const ra = [];
  for (const c of k.canonicalExamples || []) {
    for (const nua of String(c).split(' - ')) {
      /* ── TÁCH CẢ HAI LỐI ĐÁP CỦA MẪU YES/NO ──
         45 câu của lớp 2·3 viết cả hai lối đáp trong một chuỗi:
         `"Yes, it is. / No, it isn't."`. Không tách thì túi câu hợp lệ chỉ có
         chuỗi ghép ấy, nên "Yes, it is." — một câu trọn của sách, và đúng thứ bé
         phải nói — lại bị `cauHopLe` gạt. Cổng bắt được khi kịch bản lớp 2·3 lần
         đầu được đem ra soi.
         ⚠ `sinh_kichban_noi.py` (`tach_lua_chon`) tách y hệt. Hai bên lệch nhau
         thì câu ở kịch bản rơi ra ngoài túi này, và không gì kêu. */
      for (const x of nua.split('/')) {
        const s = x.trim();
        if (!s || !chuTrongCau(s).every((w) => biet.has(w))) continue;
        if (!ra.includes(s)) ra.push(s);
      }
    }
  }
  return ra;
}

/** Rút phần dạy được của MỘT bài: từ mới, mẫu câu, và câu sẵn của sách. */
export function vonCuaBai(bai) {
  const k = bai?.knowledgeCore || {};
  const cau = k.mauCauDs?.length ? k.mauCauDs : (k.mauCau ? [k.mauCau] : []);
  return {
    id: bai?.id || null,
    ten: bai?.title || '',
    tu: (k.vocabulary || []).map(goiTu),
    cau: cau.map(goiCau),
    cauSach: cauSachCuaBai(k),
  };
}

/**
 * Vốn từ cho một buổi luyện nói.
 *
 * @param baiNay   dữ liệu bài của unit đang mở
 * @param baiCu    [bài] các unit ĐỨNG TRƯỚC unit này, theo đúng thứ tự học
 * @param baiTQ    [bài] các unit TIÊN QUYẾT tra từ đồ thị — xem ghi chú dưới
 * @param daDat    unit này bé đã đạt chưa
 * @param datCu    (id) => bé đã đạt unit ấy chưa
 *
 * ── HAI NGUỒN CHO PHẦN ÔN, VÀ CHÚNG TRẢ LỜI HAI CÂU KHÁC NHAU ──
 *   `baiCu`  — bé VỪA học gì (gần thì còn nhớ, trộn vào là ôn đúng lúc);
 *   `baiTQ`  — bài này DỰNG TRÊN gì (tra bằng cạnh REQUIRES của đồ thị).
 *
 * Đo trên cả 94 bài: cửa sổ tuần tự bỏ sót tiên quyết ở 40 bài, 2 trong số đó
 * nằm ở QUYỂN KHÁC — cửa sổ "ba bài gần nhất" không bao giờ với tới, vì nó nới
 * trong cùng quyển. Nhưng nếu THAY hẳn bằng đồ thị thì 87/94 bài vốn từ HẸP ĐI,
 * nhiều bài về rỗng (phần lớn từ vựng không có cạnh tiên quyết nào — đúng, vì
 * `book` chẳng cần `pen` trước). Nên GỘP.
 *
 * ⚠ CẢ HAI NGUỒN ĐỀU LỌC QUA `datCu`. Bài bé CHƯA ĐẠT thì vốn từ của nó không
 * được vào — kể cả khi đồ thị bảo bài này cần nó. Bỏ chốt ấy là cô giáo máy nói
 * bằng từ bé chưa từng học, tức là tự tay chọc thủng tầng chống ảo giác.
 */
export function vonTu({
  baiNay, baiCu = [], baiTQ = [], daDat = false, datCu = () => false,
} = {}) {
  const loi = vonCuaBai(baiNay);
  if (!daDat) return { loi, on: [], moRong: false };

  /* Lấy các unit gần nhất TRƯỚC unit này mà bé đã đạt — gần thì còn nhớ, và cũng
     là thứ bé vừa học xong nên trộn vào là ôn đúng lúc. */
  const gan = baiCu
    .filter((b) => datCu(b?.id))
    .slice(-UNIT_CU_TOI_DA);

  /* Rồi ĐẮP THÊM bài tiên quyết mà cửa sổ trên bỏ sót. Trùng thì bỏ — `on` là
     danh sách để trộn vốn từ, một bài xuất hiện hai lần chẳng thêm được chữ nào
     mà làm lời dặn dài ra vô ích. */
  const daCo = new Set(gan.map((b) => b?.id));
  const them = (baiTQ || []).filter(
    (b) => b?.id && !daCo.has(b.id) && b.id !== baiNay?.id && datCu(b.id),
  );

  const on = [...gan, ...them].map(vonCuaBai);
  return { loi, on, moRong: on.length > 0 };
}

/** Gộp thành một danh sách phẳng — chỗ nào cần "máy được dùng từ nào" thì hỏi đây. */
export const moiTuDuocDung = (v) =>
  [...v.loi.tu, ...v.on.flatMap((x) => x.tu)].map((t) => t.tu);

export const moiCauDuocDung = (v) =>
  [...v.loi.cau, ...v.on.flatMap((x) => x.cau)].map((c) => c.cau);

/* ─────────── lời dặn cho máy ─────────── */

/**
 * Dựng lời dặn (system prompt). Viết bằng tiếng Anh vì mô hình theo lệnh tiếng Anh
 * chắc tay hơn, nhưng NỘI DUNG bắt nó nói với bé bằng hai thứ tiếng.
 *
 * Bốn điều bắt buộc, và cả bốn đều có lý do đắt:
 *
 *  1. CHỈ dùng từ trong danh sách. Đây là cả lý do phòng này tồn tại.
 *  2. Mỗi lượt đúng MỘT câu tiếng Anh ngắn. Bé 6 tuổi không nhại lại được hai câu.
 *  3. Luôn kèm một lời tiếng Việt ngắn — bé chưa hiểu tiếng Anh thì cần người dịch,
 *     mà bố mẹ không phải lúc nào cũng ngồi cạnh.
 *  4. Trả về JSON, vì màn hình cần TÁCH câu tiếng Anh (để đọc giọng en-GB và để
 *     chấm phát âm) khỏi lời tiếng Việt (đọc giọng vi-VN). Trộn hai thứ tiếng vào
 *     một dòng là bộ đọc sai giọng — kho này đã chốt "mỗi dòng chỉ MỘT thứ tiếng".
 */
/**
 * LỜI LỚP HỌC — nhúm câu cô được nói ngoài vốn từ của bài.
 *
 * Phát hiện khi gọi Groq thật lượt đầu tiên: bé chào "Chào cô", cô đáp "I like
 * milk." Không phải máy sai — unit 5 chỉ có ĐÚNG MỘT mẫu câu, nên cô bị bó tới mức
 * không có gì để chào lại. Cứ thế thì mọi lượt đều là "I like ...", và cái đó
 * không phải trò chuyện.
 *
 * Nên mở đúng một khe hẹp: mấy câu nghi thức của lớp học. Chúng KHÔNG phải từ bé
 * phải học thuộc — chúng là lời của CÔ, bé nghe mãi rồi hiểu qua ngữ cảnh, đúng như
 * trong lớp thật. Danh sách CỐ ĐỊNH và ngắn, khai ở đây để nhìn thấy được và để
 * cổng đếm; nới nó ra là quay lại đúng chỗ hỏng mà việc bó vốn từ sinh ra để tránh.
 */
export const LOI_LOP_HOC = [
  'Hello!', 'Hi!', 'Goodbye!', 'Your turn.', 'Say it with me.',
  'Listen.', 'Again, please.', 'Good job!', 'Well done!', 'Nice!',
  'Almost!', 'Try again.', 'Yes!', 'No.',
];

/* ─────────── việc của từng lượt ─────────── */

/**
 * VIỆC CỦA LƯỢT NÀY — do MÁY CON quyết, không phó mặc cho mô hình.
 *
 * Bác bắt 13-08: "nó cứ nói đi nói lại hello với mấy câu nhàm chán". Dựng lại thì
 * còn tệ hơn: sáu lượt liền cô nói đúng một câu `Hi, I'm Bill.`
 *
 * Lỗi ở LỜI DẶN, không ở mô hình. Bản trước viết "chỉ được dùng những MẪU CÂU
 * sau" rồi đưa đúng một câu ví dụ. Unit 1 có một mẫu — nên nó không còn gì khác
 * để nói, và nó đang tuân lệnh răm rắp. Thả cho mô hình "tự nói cho phong phú"
 * cũng không xong: hoặc nó lặp, hoặc nó bịa ra từ ngoài vốn của bé.
 *
 * Nên đảo lại: máy con CHỌN SẴN từ mục tiêu và kiểu việc cho từng lượt, mô hình
 * chỉ lo diễn đạt. Biến "cho phong phú" — thứ không kiểm được — thành một phép
 * đếm chạy được bằng `node` và soi được bằng cổng.
 */
export const KIEU_VIEC = {
  tu: 'tu',        // cô nói một TỪ, bé nhắc lại
  mau: 'mau',      // cô nói CẢ CÂU theo công thức, bé nhắc lại
  thay: 'thay',    // cô thay từ khác vào công thức — chỗ bé thấy mẫu câu "sống"
  khen: 'khen',    // bé vừa nói đúng: khen rồi sang việc mới
};

/**
 * Đếm xem từ nào bé đã được luyện trong buổi này, rồi chọn từ ÍT gặp nhất.
 *
 * Cố tình không dùng ngẫu nhiên: chạy hai lần ra hai kiểu thì không cổng nào canh
 * được, mà đây đúng là chỗ vừa hỏng.
 */
/**
 * GIỮ NGUYÊN CÂU BÉ ĐANG TẬP — và có trần, vì giữ mãi là một cái bẫy.
 *
 * Câu đích lấy từ `luotBe.mau`: `PhongNoi.jsx` giữ lại ngay trong lượt của bé đúng
 * câu đã dùng để chấm, nên đây là câu BÉ ĐANG CỐ NÓI, không phải câu cô vừa nói.
 * Hai thứ ấy khác nhau ở bài tả tranh và ở mọi bước hỏi–đáp: cô hỏi "What can you
 * see?" mà bé phải đáp.
 *
 * ⚠ TRẦN DÙNG LẠI `SUA_TOI_DA`, không đặt số mới. Nhánh kịch bản đã đi qua đúng
 * cái bẫy này rồi và `buocSua` đã ghi lại: bé đuối thì kịch bản đứng yên, lượt sửa
 * chen lên trước, và cả hai mươi phút chỉ còn một câu — "mười lượt liền đều là
 * Hello!". Sửa hai lần là đủ cho một chỗ khó; lần thứ ba thì cái bé cần là một
 * việc DỄ HƠN (`haDoKho`), nên tới đó nhường đường cho vòng luyện.
 */
function viecGiuLai(von, lichSu, tu, datNguong) {
  const be = luotBeCuoi(lichSu);
  const dich = be?.mau;
  if (!dich) return null;

  /* Đếm lượt trượt LIÊN TIẾP trên CÙNG câu ấy — cùng phép đếm với `buocSua`, cố ý
     giống, vì hai chỗ đang trả lời đúng một câu hỏi. */
  const ds = luotLuyen(lichSu);
  let lien = 0;
  for (let i = ds.length - 1; i >= 0; i -= 1) {
    if (ds[i].mau !== dich || ds[i].diem >= datNguong) break;
    lien += 1;
  }
  if (lien > SUA_TOI_DA) return null;

  /* Từ mục tiêu suy từ CHÍNH câu ấy — `tuTrongCau` đã biết cách bỏ chữ đứng sau
     chủ ngữ (đó là động từ, không phải danh từ của bài). Không ra từ nào thì lấy
     từ đầu bài, vì `cauThayThe` cần một `tu` để còn dựng được đường lui. */
  const coTu = tuTrongCau(dich, von);
  return {
    tu: coTu[0] || tu[0],
    kieu: KIEU_VIEC.mau,
    /* Không đi tra xem câu này thuộc mẫu nào: lời dặn theo nhãn đòi cô đọc lại
       ĐÚNG câu ấy, không đòi điền lại khuôn. Dựng một `mau` chỉ có `cau` là vừa
       đủ cho `dongViec`, và không có `congThuc` thì không ai điền bừa vào. */
    mau: { cau: dich, congThuc: null, dungDe: 'câu bé đang tập' },
    daNhac: lien,
    theoSoThich: false,
    giuViec: true,
  };
}

export function viecTiepTheo({
  von, lichSu = [], haDoKho = false, hoSo = null, nhan = null, datNguong = 6,
} = {}) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  if (!tu.length) return null;

  /* ── VIỆC CHỈ TIẾN KHI BÉ NÓI ĐÚNG ── (việc V2)
     Bé vừa sót chữ, đảo thứ tự, nói tiếng Việt, hỏi lại hay im lặng thì việc của
     lượt này là ĐÚNG CÂU ẤY, không phải một câu mới. Trước bản này việc xoay vòng
     theo SỐ LƯỢT, bất kể bé vừa làm gì — nên câu bé chưa nói được trôi qua sau
     đúng một lượt, và cô đi dạy câu khác. Xem `NHAN_GIU_VIEC`. */
  const giu = nhan && NHAN_GIU_VIEC.has(nhan)
    ? viecGiuLai(von, lichSu, tu, datNguong) : null;
  if (giu) return giu;

  const cuaCo = lichSu.filter((x) => x.vai === 'may');
  const dem = new Map(tu.map((t) => [t.tu, 0]));
  for (const l of cuaCo) {
    for (const t of tu) {
      if (new RegExp(`\\b${t.tu}\\b`, 'i').test(l.en || '')) dem.set(t.tu, dem.get(t.tu) + 1);
    }
  }
  /* Từ ít được nhắc nhất; hoà thì lấy từ đứng trước trong bài — cùng thứ tự bé đã
     học ở chặng Từ mới, nên nghe quen tai. */
  const dich = tu.reduce((a, b) => (dem.get(b.tu) < dem.get(a.tu) ? b : a), tu[0]);

  /* Xoay vòng ba kiểu việc theo SỐ LƯỢT, để không lượt nào giống lượt trước. Có
     mẫu câu thì mới xoay tới hai kiểu câu; bài chưa có mẫu thì chỉ luyện từ. */
  /* Bé đang đuối thì lùi về việc dễ nhất: chỉ nói TỪ. Không đuổi bé ra khỏi phòng
     — xem `tinhBuoi`. */
  const vong = (haDoKho || !cau.length)
    ? [KIEU_VIEC.tu]
    : [KIEU_VIEC.tu, KIEU_VIEC.mau, KIEU_VIEC.thay];
  const kieu = vong[cuaCo.length % vong.length];
  const mau = cau.length ? cau[cuaCo.length % cau.length] : null;

  /* Ô trống của công thức ưu tiên điền THỨ BÉ THÍCH, nếu bé đã chọn và từ ấy nằm
     trong vốn từ. "I like fish." khi bé thật sự thích cá thì bé nói ra một câu về
     CHÍNH MÌNH — khác hẳn nhại một câu về sữa của người khác. */
  const thich = hoSo?.thich && tu.find((t) => t.tu === hoSo.thich);
  return {
    tu: (kieu === KIEU_VIEC.thay && thich) ? thich : dich,
    kieu, mau, daNhac: dem.get(dich.tu), theoSoThich: !!(kieu === KIEU_VIEC.thay && thich),
  };
}

/**
 * Ô TRỐNG CỦA CÔNG THỨC nhận loại gì.
 *
 * Đã hỏng thật khi thử với Groq: công thức `Bye, + [Name].` mà lời dặn bảo "nhét
 * một từ được phép vào ô trống", nên mô hình sinh ra **"Bye, book."** — vô nghĩa,
 * và tệ hơn là dạy bé một câu sai. Ô trống có LOẠI: chỗ của tên người thì phải là
 * tên người, chỗ của danh từ mới nhận từ vựng của bài.
 */
/**
 * ⚠ BA LOẠI Ô NỮA, SUY THẲNG TỪ DỮ LIỆU — vá 09-10-2026.
 *
 * Bản cũ chỉ biết hai loại: ô tên người, và "ô nhận từ bất kỳ". Nên mọi ô khác
 * nhận MỌI từ của bài, và đo thật qua Groq thì nó đẻ ra những câu như:
 *
 *   "Do you live in this sixteen? - Yes, I do."   ô `[place]` nhận một CON SỐ
 *   "Who's this? - It's my sure."                 ô `[Family member]` nhận `sure`
 *
 * Cả hai đi qua `soiCau` SẠCH, vì `sixteen` và `sure` đều là từ bài có dạy. Đúng
 * họ với "Bye, bike." bác bắt 14-08 — lần ấy chỉ vá riêng ô tên, và mười một tháng
 * sau mọi ô còn lại vẫn hở y nguyên.
 *
 * ── CHỈ KHAI LOẠI NÀO DỮ LIỆU TỰ NÓI ĐƯỢC ──
 * Mục từ vựng KHÔNG có trường từ loại (740 mục: `tu` · `ma` · `ipa` · `nghia` ·
 * `so_nhieu` · `dang_ing` · `dang_qk` · `am` · `amO`). Nên bốn loại dưới đây là
 * hết những gì suy được mà KHÔNG phải đoán:
 *
 *   ten     tên người        — như cũ
 *   so      con số           — `nghia` của mục từ có chữ số ("mười một (11)"), hoặc
 *                              nằm trong `SO_DEM`. 28/740 mục, 12 ô trong dữ liệu.
 *   ing·qk·nhieu  dạng biến đổi — ô tự khai nó muốn dạng nào, và dạng ấy nằm NGAY
 *                              trong mục từ (`dang_ing` · `dang_qk` · `so_nhieu`).
 *                              27 ô trong dữ liệu.
 *
 * `[Family member]` · `[place]` · `[Food]` thì dữ liệu KHÔNG nói được. Đoán từ lời
 * chú tiếng Việt ("bố" là người, "chắc chắn" thì không) là dựng một cổng ghim vào
 * CHÍNH TẢ của lời chú — đúng cái bẫy đã dính bốn lần ở kho này. Việc còn lại là
 * việc của DỮ LIỆU: thêm một trường từ loại vào mục từ vựng. Nói thẳng ra đây để
 * không ai tưởng chỗ này đã kín.
 */
export function loaiOTrong(congThuc) {
  const m = String(congThuc || '').match(/\[([^\]]+)\]/);
  if (!m) return null;
  const o = m[1].toLowerCase();
  if (/name|tên/i.test(o)) return 'ten';
  /* Đặt TRƯỚC `so`: `[Number of things]` hiếm, mà `[Noun-plural]` thì không. */
  if (/plural|số nhiều/.test(o)) return 'nhieu';
  if (/-ing|^v-?ing|\bing\b/.test(o)) return 'ing';
  if (/past|\bqk\b|\bv2\b/.test(o)) return 'qk';
  if (/number|age|tuổi|\bsố\b/.test(o)) return 'so';
  return 'tu';
}

/* Đầu mục đã ở dạng -ing sẵn — tiếng ĐẦU của nó kết thúc bằng "ing". Soi tiếng đầu
   chứ không soi cả chuỗi: `playing tug of war` có "ing" ở tiếng đầu, còn
   `go upstairs` thì không có ở đâu cả. */
const laDangIng = (x) => /ing$/i.test(String(x || '').trim().split(/\s+/)[0] || '');

/**
 * ĐIỀN HẾT MỌI Ô của một khung, mỗi ô theo ĐÚNG loại của nó. Thiếu một ô → `null`.
 *
 * ⚠ VÌ SAO PHẢI CÓ: `cauThayThe` chú thích là "LUÔN ĐÚNG, vì nó ghép từ chính dữ
 * liệu bài". Đo thật trên cả bốn quyển, 846 lượt: 80 câu thay thế KHÔNG hợp lệ, và
 * hỏng theo kiểu tệ nhất — còn nguyên dấu ngoặc:
 *
 *   "It's a bell [Noun]."          "How many clocks? - [Number]."
 *
 * Vì phép điền cũ dùng `replace(/\[[^\]]+\]/, d)` — thay ĐÚNG MỘT ô, ô thứ hai còn
 * nguyên. `soiCau` bác nó (luật `oTrong`, thêm 26-08), nhưng `hoiCoGiao` lấy câu
 * của `cauThayThe` rồi TRẢ THẲNG, không soi lại — vì nó tin lời chú trên. Thế là bé
 * nghe cô đọc to cả dấu ngoặc vuông.
 *
 * Thiếu filler cho một ô thì trả `null` chứ KHÔNG điền bừa: `cauThayThe` còn hai
 * đường lui luôn an toàn (chính từ mục tiêu, và câu ví dụ của sách).
 */
export function dienHetO(khung, tu, tenBe = '') {
  let ra = String(khung || '').replace(/\s*\+\s*/g, ' ');
  for (let i = 0; i < 6 && /\[[^\]]+\]/.test(ra); i += 1) {
    const o = ra.match(/\[[^\]]+\]/)[0];
    const d = dienDuocVaoO(loaiOTrong(o), tu, tenBe).find(Boolean);
    if (!d) return null;
    ra = ra.replace(o, d);
  }
  return /\[|\]/.test(ra) ? null : ra;
}

/** Mục từ này là một CON SỐ. Suy từ lời chú của sách, không từ một danh sách tay. */
export const laTuSo = (t) => SO_DEM.includes(String(t?.tu || '').toLowerCase())
  || /\(\s*\d+\s*\)|^\s*\d+\s*$/.test(String(t?.nghia || ''));

/**
 * NHỮNG GÌ ĐIỀN ĐƯỢC VÀO MỘT Ô.
 *
 * Tách ra khỏi `soiCau` để `cauThayThe` và cổng dùng CÙNG một luật — hai bản của
 * cùng một luật là chỗ sửa một bên rồi hai bên nhận khác nhau.
 */
export function dienDuocVaoO(loai, tu, tenBe = '') {
  if (loai === 'ten') return [tenBe, 'Bill', 'Mai'];
  /* ⚠ MỤC TỪ CÓ THỂ ĐÃ LÀ DẠNG ẤY SẴN, và lúc ấy trường dẫn xuất để `null`.
     Lớp 4 unit 20 dạy hẳn mục từ `putting up a tent` · `telling a story` với
     `dang_ing: null` — vì chính đầu mục đã là dạng -ing. Chỉ nhận `dang_ing` thì
     sáu câu của CHÍNH SÁCH bị bác. Đã đo: so bản mới với bản cũ trên 711 câu sách,
     đúng sáu câu ấy là lỗi mới, và đây là chỗ sinh ra chúng. */
  if (loai === 'ing') return tu.flatMap((t) => [t.dang_ing, laDangIng(t.tu) ? t.tu : null]);
  if (loai === 'qk') return tu.flatMap((t) => [t.dang_qk, t.dang_qk ? null : t.tu]);
  if (loai === 'nhieu') return tu.flatMap((t) => [t.so_nhieu, t.so_nhieu ? null : t.tu]);
  if (loai === 'so') return tu.filter(laTuSo).map((t) => t.tu);
  /* ⚠ Ô THƯỜNG THÌ TRỪ CON SỐ RA. Đó là chỗ "this sixteen" lọt qua: `sixteen` là
     từ bài có dạy, nên nó điền được vào mọi ô. Con số đã có ô riêng của nó. */
  return tu.filter((t) => !laTuSo(t))
    .flatMap((t) => [t.tu, t.so_nhieu, t.so_it, t.dang_ing, t.dang_qk]);
}

/** Lời dặn riêng cho lượt này, ghép vào cuối lời dặn chung. */
function dongViec(v, tenBe) {
  if (!v) return '';
  const { tu, kieu, mau } = v;
  if (kieu === KIEU_VIEC.tu) {
    return `THIS TURN: say just the word "${tu.tu}" (means "${tu.nghia}") for the child to repeat.`;
  }
  if (kieu === KIEU_VIEC.mau && mau) {
    /* ĐÚNG NGUYÊN VĂN. Để nó tự thay tên ở lượt này thì lượt `mau` và lượt `thay`
       ra cùng một câu — đã thấy thật: hai lượt liền đều "Hi, I'm Bo." */
    const dong = `THIS TURN: say exactly this sentence, word for word: "${mau.cau}"`
      + ' — do not substitute anything.';
    if (!v.giuViec) return dong;
    /* ══ PHẢI GỠ LUẬT 4 RA, KHÔNG THÌ CẢ V2 VÔ NGHĨA ══
       Đo thật 09-10 với Groq, 27 lượt: bé sai thì KHÔNG LẦN NÀO (0/9) cô nhắc lại
       đúng câu bé đang tập. Cô đổi chữ trong ô — bé cần nghe lại "It's my brother."
       thì cô nói "It's my sister."

       Vì lời dặn đang tự chọi nhau. Luật 4 nằm trong khối HARD RULES ("breaking any
       of these makes the lesson useless") và viết thẳng: NEVER say the same English
       sentence you said in your previous turn — Vary the word in the slot. Hai dòng
       dưới nó (dòng theo nhãn, và chính dòng này) thì đòi đọc lại NGUYÊN câu ấy.
       Mô hình chọn bên được gọi là "hard rule", và nó chọn đúng theo lời ta dặn.

       Luật 4 vẫn đúng ở lượt thường — nó sinh ra để chữa "cô cứ nói đi nói lại".
       Nhưng lượt SỬA thì lặp lại chính là việc cần làm. Nên gỡ ra ĐÚNG lượt ấy,
       bằng đúng cách `dongBuoc` đã làm cho bước `sua` từ 18-08: nói thẳng ra rằng
       dòng này thắng luật kia. Không nói thì mô hình không có cách nào biết. */
    /* ⚠ KHÔNG mở đầu bằng `THIS TURN:` nữa. Lượt giữ việc đã có một dòng
       `THIS TURN:` của nhãn ở ngay trên; hai dòng cùng mở đầu như thế là hai lệnh
       ngang hàng, và mô hình không có cách nào biết dòng nào mới là việc. */
    return `${dong.replace(/^THIS TURN: /, 'SAME TASK AS LAST TURN: ')}`
      + '\n  She has NOT said it right yet, so SAY IT AGAIN, unchanged.'
      + '\n  This overrides HARD RULE 4 ("never repeat yourself"): repeating is the'
      + '\n  whole job this turn. Do not vary the word in the slot.';
  }
  if (kieu === KIEU_VIEC.thay && mau) {
    const khung = mau.congThuc || mau.cau;
    const loai = loaiOTrong(mau.congThuc);
    /* Ô tên người thì CHỈ nhận tên. Nhét `book` vào là ra "Bye, book." */
    const dien = loai === 'ten'
      ? `put the child's name ${tenBe} in the slot (a NAME goes there — never a thing)`
      : `put the word "${tu.tu}" in the slot`;
    return `THIS TURN: take the pattern ${khung} and ${dien}.`
      + ' Do not repeat the example sentence word for word.';
  }
  return '';
}

/* Mặc định là "con", KHÔNG phải "bạn nhỏ". Bản cũ để "bạn nhỏ" nên chính lời dặn
   gieo chữ "bạn" vào rồi trách mô hình dùng nó — xem `XUNG_HO_CAM`. */
export function loiDan({
  von, tenBe = 'con', lop = 1, viec = null, hoSo = null, unit = null,
  nhan = null, chiTiet = null, bang = null,
}) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  const bangTu = tu.map((t) => `${t.tu} (${t.nghia})`).join(', ');
  const bangCau = cau.map((c) => `"${c.cau}"${c.congThuc ? ` [${c.congThuc}]` : ''}`).join('; ');

  /* Câu ví dụ ĐI KÈM công thức, và công thức mới là thứ đáng học: mẫu câu là cái
     KHUNG bé thay từ vào, không phải một câu để đọc thuộc. Bản trước chỉ liệt kê
     câu ví dụ, nên mô hình nói đúng câu ấy sáu lượt liền — nó không sai, nó không
     có gì khác để nói. */
  const bangKhung = cau
    .map((c) => `${c.congThuc || c.cau} (ví dụ: "${c.cau}")`)
    .join('; ');

  return [
    /* ⚠ KHÔNG ĐẶT TÊN BÉ Ở DÒNG NÀY. Dòng đầu là KHUNG — nó đi vào vân tay prompt
       (`locKhung` không có cách nào nhận ra "named Lan" là dữ liệu riêng mà không
       ghim vào chính tả). Tên bé đã nằm trong khối `<<RIENG` ở dưới, nơi `locKhung`
       bỏ sạch. Đo được 09-10 lúc làm V3: hai bé cùng unit ra HAI vân tay khác nhau,
       tức bảng so ΔC không gom lại được, và vân tay thành mã theo dõi từng bé —
       đúng hai chỗ hỏng mà `vantay.js` sinh ra để tránh. */
    `You are a warm, patient English tutor for a ${lop === 1 ? 'six-year-old' : `grade ${lop}`} Vietnamese child.`,
    /* ── VIỆC CỦA CÔ, NÓI NGAY DÒNG ĐẦU ── (bác chốt 18-08)
       "AI đóng vai trò là Cô giáo dạy học sinh nói được các câu giao tiếp hoàn
       chỉnh chứ không như máy như giờ." Lời dặn cũ mở bằng "a warm, patient English
       tutor" rồi đi thẳng vào mười điều cấm — không chỗ nào nói cô phải DẠY cái gì.
       Mô hình đọc xong biết mình không được nói gì, không biết mình phải làm gì. */
    'Your job: get her SAYING WHOLE SENTENCES out loud, and fix what goes wrong.',
    'A real lesson has three beats, and every turn of yours is one of them:',
    '  TEACH  — show the sentence and what it is for;',
    '  SPEAK  — make her say it, or answer you, or ask you;',
    '  FIX    — name what went wrong in her last try, then let her try again.',
    'You are her teacher, not a flashcard machine. Never drill a bare word when a',
    'whole sentence would do — a child who can only say "cooking" cannot talk.',
    ...(unit ? dongUnit(unit) : []),
    '',
    'HARD RULES — breaking any of these makes the lesson useless:',
    `1. Use ONLY these English words: ${bangTu}.`,
    '   Plus the bare function words needed to fill the patterns below.',
    '   Never introduce an English word outside this list, not even an easy one.',
    `2. Sentence patterns you may build: ${bangKhung || bangCau}.`,
    '   A pattern is a FRAME: put the allowed words (or the child\'s name) in the slot.',
    '   The example is one filling of it, not the only thing you may say.',
    `   You may also use these fixed classroom phrases: ${LOI_LOP_HOC.join(' ')}`,
    '   Those phrases are yours to say — they are not words the child must produce.',
    '3. Say exactly ONE short English sentence per turn. Never two.',
    '4. NEVER say the same English sentence you said in your previous turn.',
    '   Vary the word in the slot. Repeating yourself is the worst thing you can do here.',
    '5. Do not greet more than once in a conversation. Greet only on your first turn.',
    '6. Always add ONE short Vietnamese line explaining what you just said and what',
    '   the child should do. Write it for a six-year-old, not for an adult.',
    /* ── LUẬT 7 · 8 · 8b CŨ ĐÃ CHUYỂN SANG `loidan_nhan.js` ── (việc V2)
       Ba luật ấy đều nói về MỘT tình huống riêng: bé nói lạc đề (7), bé nói đúng
       (8), bé nói sai (8b). Để chung ở đây thì lượt nào mô hình cũng đọc cả ba,
       rồi tự đoán cái nào đang áp dụng — và nó đoán theo thứ chiếm nhiều chữ
       nhất. Nay mỗi cái thành nội dung của đúng nhánh cần nó, ghép vào bằng
       `dongTheoNhan` ở dưới. KHÔNG để lại bản thứ hai ở đây: lặp hai nơi thì sửa
       một bên là hai bên nói khác nhau, và mô hình nghe bên dài hơn.

       ⚠ LUẬT 8c THÌ GIỮ, dù §7 kể nó trong danh sách phải gỡ. Nó KHÔNG nói về
       lượt vừa rồi của bé mà nói về lịch sử của CHÍNH CÔ ("đừng dùng lại lời Việt
       cũ"), nên nó áp dụng ở cả chín nhãn. Gỡ khỏi đây mà không nhãn nào gánh thì
       mất hẳn một luật đã chữa được một lời bác bắt ("feel like a machine"); còn
       chép vào cả chín nhãn thì đúng là cái lặp vừa nói ở trên. Nên nó ở lại khối
       chung, mang số 7. */
    '7. Do not reuse your own Vietnamese wording from an earlier turn. Saying',
    '   "Con nghe rồi nói lại nhé" every single turn is exactly what makes a lesson',
    '   feel like a machine. Talk to her about THIS sentence.',
    /* Hai luật dưới đây bác chốt 14-08, và cả hai đều CÓ CHỐT SOI LẠI ở
       `loiVietHopLe` — dặn dò một mình chưa bao giờ đủ trong phòng này. */
    '8. Vietnamese pronouns are FIXED: call yourself "cô", call the child "con".',
    `   Never "bạn", "em", "tớ", "cậu" — you are her teacher, not her classmate.`,
    '   ("mình" meaning "we/us together" is fine: "hôm nay mình tập nói nhé".)',
    '9. When you quote English inside the Vietnamese line, quote it EXACTLY as it',
    '   appears above or as the child actually said it. Never reshape a word to fit',
    '   your sentence. Quoting a word the child never said teaches her a wrong word,',
    '   and it will be read aloud in the wrong voice.',
    '',
    /* ── VIỆC CỦA ĐÚNG LƯỢT NÀY, THEO NHÃN ── (việc V2)
       Đứng SAU khối luật và TRƯỚC `dongViec` là có ý: luật là thứ không đổi, nhãn
       nói tình huống, `dongViec` nói câu cụ thể. Đọc xuôi từ chung tới riêng thì
       dòng sau bao giờ cũng thắng dòng trước — mà dòng sau mới là dòng của lượt
       này.
       ⚠ Dòng nào mang chữ của bé thì mở đầu bằng `CHILD:` và bị `locKhung` bỏ
       khỏi vân tay — giao ước ghi ở đầu `loidan_nhan.js`. */
    nhan ? dongTheoNhan(nhan, chiTiet || {}) : '',
    dongViec(viec, tenBe),
    /* ⚠ `bang` LÀ ĐƯỜNG CHÍNH, `hoSo` chỉ là đường tương thích. Mọi chỗ gọi cũ
       truyền `hoSo` rời, và chúng vẫn phải chạy đúng — nên dựng một bảng tối giản
       quanh nó. Bỏ đường ấy thì phải sửa cùng lúc bốn màn, mà sửa bốn chỗ trong
       một bản là bốn chỗ có thể sai. */
    tomTatChoLoiDan(bang || dungBang({ hoSo }), tenBe),
    '',
    'Reply as JSON only: {"en": "<the English sentence>", "vi": "<the Vietnamese line>"}',
  ].filter((x) => x !== null).join('\n');
}

/* ═══════════ BÀI TẢ TRANH — LỜI DẶN RIÊNG, KHÔNG DÙNG LỜI DẶN CŨ ═══════════ */

/**
 * CÂU BÉ CẦN NÓI ở lượt tới — KHÔNG phải câu cô vừa nói.
 *
 * ══ CHỖ HỎNG NẶNG NHẤT, BÁC BẮT 19-08-2026 ══
 *
 *     "Phần nói là AI đóng vai trò giáo viên hướng dẫn học sinh tả tranh chứ không
 *      phải là bắt học sinh nói theo mấy câu kiểu What can you see. Mấy câu What
 *      can you see dùng để hướng dẫn học sinh nói thôi."
 *
 * Cả phòng nói tới giờ dựng trên một giả định: BÉ NHẠI LẠI CÂU CÔ VỪA NÓI. Chấm
 * điểm cũng thế — `PhongNoi.jsx` so lời bé với `cauCoVuaNoi`.
 *
 * Với bài tả tranh thì giả định ấy sai hẳn. Cô hỏi "What can you see?", bé phải
 * ĐÁP ("I can see a kite."), không phải nhại lại câu hỏi. Trải một buổi ra giấy
 * thấy rõ: bé nói "what can you see?" và được **9/10** — hệ thống đang KHEN bé vì
 * nhại đúng câu hỏi của cô. Không lỗi đỏ ở đâu, điểm còn cao.
 *
 * Nên mỗi lượt của cô nay mang theo `can`: những câu ĐƯỢC TÍNH LÀ ĐÚNG.
 *
 *   taTranh  bé tả gì cũng được, miễn có trong tranh → cả bản mô tả
 *   goiY     cô hỏi một chi tiết → đúng một câu đáp
 *   caDoan   cả đoạn
 *   còn lại  giữ nguyên lối cũ (nhại lại câu cô nói) — 20 kịch bản kia không đổi
 */
export function canNoi(buoc, kichBan) {
  if (!buoc) return [];
  const moTa = kichBan?.moTaTranh || [];
  if (buoc.loai === 'taTranh') return [...moTa];
  if (buoc.loai === 'goiY') return buoc.dapMau ? [buoc.dapMau] : [...moTa];
  if (buoc.loai === 'caDoan') return [buoc.en];
  return buoc.en ? [buoc.en] : [];
}

/**
 * LỜI DẶN CHO BÀI TẢ TRANH — dựng lại từ đầu, không mượn `loiDan`.
 *
 * Bác bảo "Hãy xoá hết prompt cũ để cài đặt lại." Đúng: lời dặn cũ dài mười điều,
 * và gần như điều nào cũng nói về việc DẠY NHẠI CÂU — "say exactly ONE short
 * English sentence", "take the pattern and put the word in the slot", "she repeats
 * after you". Ghép thêm vài dòng về tranh vào đấy thì mô hình vẫn đọc ra "dạy bé
 * nói theo mẫu", vì chín phần mười lời dặn nói thế.
 *
 * Lời dặn này ngắn, và chỉ nói đúng một việc: cô hướng dẫn bé TẢ BỨC TRANH.
 */
export function loiDanTranh({ tenBe = 'con', lop = 3, kichBan, buoc, luotBe = null }) {
  const moTa = kichBan?.moTaTranh || [];
  const d = [
    `You are a warm, patient English teacher for a grade ${lop} Vietnamese child named ${tenBe}.`,
    '',
    'THE ONE THING YOU ARE DOING: helping her DESCRIBE A PICTURE in English.',
    'She is looking at the picture. You cannot see it — you only have these lines,',
    'which are everything that is true about it:',
    ...moTa.map((c) => `  · ${c}`),
    '',
    'HOW THIS WORKS:',
    '1. She talks about the picture. Anything she says that matches a line above is',
    '   RIGHT — even if she says it in a different order, or only part of it.',
    '2. You are NOT teaching her to repeat your sentences. Questions like',
    '   "What can you see?" are YOUR tool for prompting her — she must never be',
    '   asked to say them back. If she repeats your question instead of answering,',
    '   tell her gently in Vietnamese that you want HER words about the picture.',
    '3. When she is stuck, ask ONE small question about one detail, wait, then check',
    '   her answer against the lines above. Wrong number or wrong thing → say so.',
    '4. NEVER read the whole description out to her. She has to find the words.',
    '5. At the end you will string her sentences into one short paragraph and have',
    '   her say all of it. That is the goal of the whole session.',
    '',
    'HOW YOU SPEAK:',
    '6. ONE short English sentence per turn, and it must be the exact sentence given',
    '   below. Everything else you say is the ONE Vietnamese line.',
    '7. Vietnamese pronouns are FIXED: call yourself "cô", call the child "con".',
    '   Never "bạn", "em", "tớ", "cậu".',
    '8. Write the Vietnamese for an eight-year-old, warm and short. Praise what was',
    '   right first, then the one thing to fix.',
    '',
    dongBuocTranh(buoc, luotBe, moTa),
    '',
    'Reply as JSON only: {"en": "<the English sentence>", "vi": "<the Vietnamese line>"}',
  ];
  return d.filter((x) => x !== null).join('\n');
}

/** Lời dặn của riêng lượt này, cho bài tả tranh. */
export function dongBuocTranh(buoc, luotBe, moTa) {
  if (!buoc || buoc.loai === 'ket') return '';
  const d = [`THIS TURN: your English sentence MUST be exactly: "${buoc.en}"`,
    '  Copy it character for character.'];
  if (buoc.loai === 'taTranh') {
    d.push('  ROLE: invite her to describe the picture, then WAIT. Do not list',
      '  anything for her. Whatever she says next that matches a line above counts.');
  } else if (buoc.loai === 'goiY') {
    d.push('  ROLE: she is stuck, so you are prompting with ONE detail question.',
      `  The true answer is "${buoc.dapMau || '(see the lines above)'}".`,
      '  Ask it and wait. Do NOT answer it yourself, and do NOT ask her to repeat',
      '  the question — you want her ANSWER.');
  } else if (buoc.loai === 'sua') {
    /* ── DẪN BÉ TỚI CÂU ĐÚNG, KHÔNG CHỈ CHÊ ── (bác chốt 19-08-2026)
       "Khi học sinh nói chưa đúng → Giúp học sinh nói đúng theo nội dung đang hỏi."
       Ở bài tả tranh bé thường sai vì ĐÁP NHẦM CÂU HỎI, không phải vì thiếu chữ.
       Nên lượt sửa phải nhắc lại câu hỏi trước đã, rồi mới tới chỗ lệch. */
    d.push('  ROLE: this is a CORRECTION turn. She answered the wrong thing.');
    if (buoc.hoiLai) d.push(`  You had asked: "${buoc.hoiLai}"`);
    d.push(`  The answer that fits that question is "${buoc.en}".`,
      '  In Vietnamese: say what she DID get right, then name the ONE thing that is',
      '  off (wrong number? wrong object? answered a different question?), then say',
      '  the English answer once and ask her to say it back. Do not move on.');
  } else if (buoc.loai === 'caDoan') {
    d.push('  ROLE: string it all together. Say the whole description once, then ask',
      '  her to say all of it herself. This is what the session was for.');
  }
  if (luotBe?.diem != null) {
    d.push('WHAT THE CHILD JUST SAID:',
      `  "${luotBe.chu}" — scored ${luotBe.diem}/10 against "${luotBe.mau}".`);
    const thieu = [...(luotBe.thieu || []), ...(luotBe.thieuChucNang || [])].filter(Boolean);
    if (thieu.length) d.push(`  Words she left out: ${thieu.join(', ')}.`);
    /* Chỗ dễ hỏng nhất của bài tả tranh, và mô hình không tự nhận ra: bé nhại lại
       câu hỏi thay vì đáp. Điểm phát âm khi ấy rất cao, nên nếu chỉ nhìn điểm thì
       cô lại khen. */
    if (moTa.length && luotBe.chu && /\?$/.test(String(luotBe.chu).trim())) {
      d.push('  ⚠ She repeated your QUESTION instead of answering it. Say so kindly',
        '  in Vietnamese and ask again for her own words about the picture.');
    }
  }
  if (buoc.vi) {
    d.push(`  Your Vietnamese line MUST get this across: "${buoc.vi}"`);
  }
  return d.join('\n');
}

/* ─────────── ngữ cảnh ─────────── */

/**
 * Cắt lịch sử trước khi gửi. Giữ lượt MỚI NHẤT, bỏ lượt cũ.
 *
 * Cắt ở client chứ không ở server, vì server không giữ gì cả — nó nhận sao gửi vậy.
 * Nếu quên cắt thì không có gì báo: câu trả lời vẫn đúng, chỉ có hoá đơn dài ra.
 */
export function catNguCanh(ds = [], toiDa = LUOT_GUI_TOI_DA) {
  const sach = ds.filter((x) => x && (x.vai === 'may' || x.vai === 'be') && x.chu);
  return sach.slice(-toiDa);
}

/** Dạng gửi lên máy chủ — chỉ vai và chữ, không kèm điểm hay dấu thời gian. */
export const goiGui = (ds) => catNguCanh(ds).map((x) => ({
  role: x.vai === 'may' ? 'assistant' : 'user',
  content: String(x.chu).slice(0, CHU_TOI_DA),
}));

/* ─────────── hình cho từ đang nói tới ─────────── */

/**
 * Máy vừa nói câu này thì màn hình phải vẽ HÌNH của những từ trong đó.
 *
 * Bác dặn 13-08: "bổ sung thêm hình ảnh với các từ khi học về hình, lấy trong dữ
 * liệu chúng ta". Đúng chỗ cần: bé lớp 1 chưa đọc được `chicken`, nhưng nhìn 🍗 là
 * hiểu ngay. Không có hình thì phòng này quay về thành một khối chữ — mà cả quyển
 * dựng trên nguyên tắc không bắt bé đọc chữ.
 *
 * So theo TỪNG TIẾNG, không phải `includes`: `includes('can')` sẽ khớp cả trong
 * "I can see". Dấu câu bị bóc trước khi so, vì "chips." không bao giờ khớp "chips".
 *
 * ── MỘT CHỮ, HAI NGHĨA ──
 * Nhưng so theo tiếng vẫn chưa đủ: `can` là CÙNG MỘT CHỮ cho "cái lon" (unit 3) và
 * "có thể" (unit 14). Vẽ hình cái lon lúc máy nói "I can see" thì bé học ngược hẳn
 * nghĩa — tệ hơn là không vẽ gì.
 *
 * Luật vị trí, nhỏ mà đủ: chỗ NGAY SAU một đại từ làm chủ ngữ là chỗ của ĐỘNG TỪ,
 * không phải của danh từ. "I can see" → bỏ; "A can, please" → giữ. Không phải phép
 * phân tích ngữ pháp, chỉ là một chốt chặn đúng chỗ hay va nhất ở vốn từ lớp 1.
 *
 * Hình lấy qua `hinhCuaTu` ở `lib/noiDung.js` — cùng nguồn với thẻ từ và thanh
 * việc. Đừng đọc lại `bai.hinhTu` ở đây.
 */
const CHU_NGU = new Set(['i', 'you', 'we', 'they', 'he', 'she', 'it']);

export function tuTrongCau(cau, von) {
  const tieng = String(cau || '').toLowerCase().split(/[^a-z']+/).filter(Boolean);
  const co = new Set(tieng);
  const sauChuNgu = new Set(
    tieng.filter((_, i) => i > 0 && CHU_NGU.has(tieng[i - 1])),
  );
  const moi = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const thay = [];
  for (const t of moi) {
    if (thay.some((x) => x.tu === t.tu)) continue;
    /* Từ nhiều tiếng ("ice cream") thì đòi có ĐỦ các tiếng của nó. */
    const phan = t.tu.toLowerCase().split(/\s+/).filter(Boolean);
    if (!phan.length || !phan.every((p) => co.has(p))) continue;
    /* Từ một tiếng mà đứng ngay sau chủ ngữ thì đang làm động từ — đừng vẽ. */
    if (phan.length === 1 && sauChuNgu.has(phan[0])) continue;
    thay.push(t);
  }
  return thay;
}

/**
 * Đọc câu trả lời của máy. Mô hình được dặn trả JSON, nhưng KHÔNG được tin là nó
 * luôn làm đúng — trả về chữ trần thì vẫn phải dùng được, đừng để màn trắng.
 */
export function docTraLoi(chu) {
  const s = String(chu || '').trim();
  const json = s.match(/\{[\s\S]*\}/);
  if (json) {
    try {
      const o = JSON.parse(json[0]);
      if (o && (o.en || o.vi)) {
        return { en: String(o.en || '').trim(), vi: String(o.vi || '').trim(), thoJSON: false };
      }
    } catch { /* rơi xuống dưới */ }
  }
  /* Không phải JSON: đoán dòng nào là tiếng Anh bằng dấu tiếng Việt. Đoán sai thì
     bé nghe sai giọng một câu — vẫn hơn là không hiện gì. */
  const dong = s.split('\n').map((x) => x.trim()).filter(Boolean);
  const coDauViet = (x) => /[àáảãạăâèéẻẽẹêìíỉĩịòóỏõọôơùúủũụưỳýỷỹỵđ]/i.test(x);
  return {
    en: dong.find((x) => !coDauViet(x)) || '',
    vi: dong.find(coDauViet) || '',
    thoJSON: true,
  };
}

/* ─────────── soi lại câu cô nói ─────────── */

/**
 * CÂU CÔ NÓI CÓ DÙNG ĐƯỢC KHÔNG.
 *
 * Dặn dò là chưa đủ. Thử thật với Groq: đã bảo rõ ô trống của `Bye, + [Name].` là
 * chỗ của TÊN NGƯỜI, nó vẫn sinh ra **"Bye, bike."** Với người lớn thì đó là một
 * câu buồn cười; với bé 6 tuổi đang tập nhại thì đó là dạy sai, và bé sẽ nhớ.
 *
 * Nên đảo từ TIN sang SOI: máy con tự kiểm câu cô nói, không hợp lệ thì thay bằng
 * câu do chính máy con dựng. Mô hình vẫn có ích ở chỗ nó hiểu bé vừa nói gì và
 * viết được lời tiếng Việt; nhưng câu tiếng Anh — thứ bé sẽ nhại — thì không thả.
 *
 * Hợp lệ khi câu ấy là MỘT trong:
 *   · một từ trong vốn từ                     ("ball")
 *   · một câu nghi thức của lớp               ("Good job!")
 *   · một câu ví dụ của bài                   ("Hi, I'm Bill.")
 *   · một công thức đã điền đúng LOẠI ô trống ("Hi, I'm Bo." · "I like fish.")
 */
/**
 * MỘT CÂU SÁCH TÁCH RA THÀNH NHỮNG CÂU BÉ NÓI ĐƯỢC.
 *
 * `" - "` chia lượt HỎI và lượt ĐÁP; `"/"` chia hai lối đáp của mẫu yes/no. Cả cặp
 * nguyên vẫn được giữ, vì bước `mau` đọc cả cặp làm mẫu.
 * `sinh_kichban_noi.py` (`tach_doi` · `tach_lua_chon`) tách y hệt — lệch nhau thì
 * câu ở kịch bản rơi ra ngoài vốn hợp lệ, và không gì kêu.
 */
const nuaCua = (s) => {
  const t = String(s || '').trim();
  const ra = [t];
  for (const a of t.split(' - ')) for (const b of a.split('/')) ra.push(b.trim());
  return ra.filter(Boolean);
};

const gonCau = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9' ]/g, '').replace(/\s+/g, ' ').trim();

/**
 * NĂM ĐƯỜNG CÔNG NHẬN — tên dùng chung với Thuật toán 3.12 của luận văn.
 *
 * Khai thành hằng để bộ đo an toàn nội dung (`tools/do_an_toan_noi_dung.mjs`,
 * kịch bản KB3) gọi tên được từng đường: đo tỷ lệ bác bỏ RIÊNG theo đường, và
 * chạy được phép thử ĐẢO CHIỀU — tắt từng đường rồi xem tỷ lệ bác có tăng đúng ở
 * nhóm câu tương ứng không. Không có tên thì không đo riêng được, mà không đo
 * riêng thì "mỗi đường đều có tác dụng" chỉ là một lời nói.
 */
export const DUONG_CONG_NHAN = ['tu', 'nghiThuc', 'nuaMauCau', 'cauSach', 'congThuc'];

/** Lý do BÁC một câu — bốn lý do này khác loại nhau, đừng gộp khi báo cáo. */
export const LY_DO_BAC = ['rong', 'lap', 'oTrong', 'ngoaiVon'];

/**
 * SOI MỘT CÂU, VÀ NÓI RA NÓ ĐI QUA ĐƯỜNG NÀO.
 *
 * Trả `{ ok, duong, bac }`:
 *   ok     câu có được đưa cho bé không
 *   duong  tên đường công nhận đã nhận nó (null khi bị bác)
 *   bac    lý do bác (null khi được nhận)
 *
 * `tat` là tập tên đường bị TẮT — chỉ dùng cho phép thử đảo chiều của KB3. Lúc
 * chạy thật không ai truyền tham số này, nên hành vi không đổi một li.
 *
 * ⚠ Đây là thân hàm thật; `cauHopLe` bên dưới chỉ là vỏ boolean giữ nguyên API cũ
 * cho bốn chỗ gọi hiện có. Đừng nhân đôi lô-gic sang đó.
 */
export function soiCau(en, { von, tenBe = '', cauTruoc = '', tat = null } = {}) {
  const bo = (x) => !!tat && (tat.has ? tat.has(x) : tat.includes(x));
  const c = gonCau(en);
  if (!c) return { ok: false, duong: null, bac: 'rong' };
  /* Lặp Y HỆT lượt trước thì dù đúng ngữ pháp vẫn hỏng — đó chính là cái bác bắt:
     "nó cứ nói đi nói lại". Đã thấy thật hai lượt liền cùng ra "Hi, I'm Bo." */
  if (cauTruoc && gonCau(cauTruoc) === c) return { ok: false, duong: null, bac: 'lap' };

  /* ⚠ Ô TRỐNG CHƯA ĐIỀN — bác thẳng, tìm ra 26-08 bằng `tools/do_an_toan_noi_dung.mjs`.
     Ba bài có công thức HAI ô (`Is your sports day in + [Month A]? - … It's in +
     [Month B].`). Phép điền ở dưới — cả ở đây lẫn ở chỗ mô hình bắt chước — chỉ
     thay ô ĐẦU, nên ô sau còn nguyên. Mà `gonCau` bóc sạch dấu ngoặc trước khi so,
     nên hai bên khớp nhau và câu ĐƯỢC NHẬN. Bé nghe cô đọc "It's in month B."
     Câu tiếng Anh cho trẻ sáu tuổi không bao giờ có dấu ngoặc vuông, nên phép kiểm
     này an toàn tuyệt đối và không cần biết ô ấy đáng lẽ nhận gì.
     ⚠ Phải đặt TRƯỚC năm đường công nhận: đường `nuaMauCau` và `congThuc` đều
     dựng chuỗi so sánh bằng `gonCau`, tức là cả hai đều mù với dấu ngoặc. */
  if (/[[\]]/.test(String(en))) return { ok: false, duong: null, bac: 'oTrong' };

  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  const nhan = (duong) => ({ ok: true, duong, bac: null });

  /* ⚠ MỘT TỪ RỜI, KỂ CẢ DẠNG BIẾN ĐỔI CỦA NÓ.
     Đường `congThuc` đã nhận `so_nhieu · so_it · dang_ing · dang_qk` từ lâu, nhưng
     đường này thì không — nên "playing the violin" bị bác trong khi bài lớp 5 unit
     4 dạy hẳn mục từ `play the violin` với `dang_ing: "playing the violin"`. Lệch
     nhau giữa hai đường của cùng một hàng rào là chỗ không ai ngờ để mà đi tìm.
     Đo được 26-08 lúc nối phụ đạo: 12 trên 129 ca có nút gốc rễ khác nút mắc bị
     bác SẠCH câu chỉ vì một phương án nhiễu dùng dạng -ing.
     KHÔNG phải nới rào: các dạng ấy lấy từ CHÍNH mục từ vựng bé đã học, đúng lập
     luận đã ghi ở đường `congThuc` bên dưới. Từ nào bài không dạy thì vẫn không có
     đường vào. */
  if (!bo('tu') && tu.some((t) => [t.tu, t.so_nhieu, t.so_it, t.dang_ing, t.dang_qk]
    .some((x) => x && gonCau(x) === c))) return nhan('tu');
  if (!bo('nghiThuc') && LOI_LOP_HOC.some((x) => gonCau(x) === c)) return nhan('nghiThuc');
  /* Cả cặp, VÀ từng nửa của cặp. Mẫu `How are you? - Fine, thank you.` không có ô
     trống nào và cũng không nằm trong `canonicalExamples`, nên nửa đáp của nó
     không có đường nào khác để được công nhận — mà đó chính là câu bé phải nói ở
     bước `noiCa`. Cổng bắt được ở lớp 3 unit 1. */
  if (!bo('nuaMauCau')
      && cau.some((x) => nuaCua(x.cau).some((n) => gonCau(n) === c))) return nhan('nuaMauCau');
  /* Câu sẵn của sách — đã lọc theo từ ở `cauSachCuaBai`. Mở chỗ này ăn hai đường:
     ba bài công thức hai ô nay có câu để luyện, và cô giáo máy bớt nhàm vì có
     nhiều câu đúng để chọn thay vì đúng một mẫu. */
  const sach = [...(von.loi.cauSach || []), ...von.on.flatMap((x) => x.cauSach || [])];
  if (!bo('cauSach') && sach.some((x) => gonCau(x) === c)) return nhan('cauSach');

  /* Công thức đã điền: dựng mọi cách điền HỢP LỆ rồi so. Số cách rất nhỏ (số mẫu
     câu × số từ), nên cứ dựng hết còn hơn đoán bằng biểu thức chính quy. */
  for (const x of (bo('congThuc') ? [] : cau)) {
    if (!x.congThuc) continue;
    /* ── NỬA CỦA MỘT CẶP HỎI–ĐÁP CŨNG LÀ CÔNG THỨC ──
       Từ 18-08 phòng nói dạy theo lối đối đáp: cô hỏi nửa trước, bé đáp nửa sau.
       Nên câu hợp lệ của một lượt thường là NỬA của mẫu, không phải cả cặp:
       `What's your hobby? - It's + [Hobby].` → bé nói `It's cooking.`
       Bản cũ chỉ điền vào cả cặp, nên mọi câu đáp lẻ đều rơi ra ngoài — cổng bắt
       được ở lớp 2 unit 9 ("I want some yogurt." bị gạt dù là đúng khuôn sách).
       Vẫn thử cả cặp NGUYÊN, vì bước `mau` nói cả cặp. */
    for (const khung of [x.congThuc, ...x.congThuc.split(' - ')]) {
      const loai = loaiOTrong(khung);
      if (!loai) continue;
      /* ⚠ Ô CÓ KIỂU thì DẠNG BIẾN ĐỔI cũng điền được.
         Lớp 2 unit 12 dạy CẢ HAI mẫu: "The cake is on the table." và "The grapes
         are on the table." — tức sách dạy hẳn lối số nhiều. Nhưng chỗ này chỉ điền
         dạng gốc, nên "The cakes are on the table." bị gạt, dù nó là câu của chính
         sách và đúng cái mẫu vừa dạy.
         Không phải nới rào: dạng biến đổi lấy từ CHÍNH mục từ vựng bé đã học
         (`so_nhieu` · `so_it` · `dang_ing` · `dang_qk`), không phải chữ mới. Từ nào
         bài không dạy thì vẫn không có đường vào — "They are riding cars." vẫn bị
         gạt vì `car` không nằm trong vốn của bài ấy. */
      const dienDuoc = dienDuocVaoO(loai, tu, tenBe);
      for (const d of dienDuoc) {
        if (!d) continue;
        const thu = khung.replace(/\s*\+\s*/g, ' ').replace(/\[[^\]]+\]/, d);
        if (gonCau(thu) === c) return nhan('congThuc');
      }
    }
  }
  return { ok: false, duong: null, bac: 'ngoaiVon' };
}

/**
 * Vỏ boolean — bốn chỗ gọi hiện có (`goiPhongNoi.js`, `phudao.js`) dùng cái này.
 * Giữ nguyên chữ ký cũ để không phải sửa chỗ gọi nào.
 */
export const cauHopLe = (en, opt = {}) => soiCau(en, opt).ok;

/* ─────────── gọi lại cô giáo khi câu bị bác ─────────── */

/**
 * BÁC MỘT CÂU RỒI THÔI LÀ BỎ MẤT CÔ GIÁO — NÊN XIN LẠI, NHIỀU NHẤT HAI LẦN.
 *
 * ── VÌ SAO ──
 * `soiCau` bác xong thì `cauThayThe` dựng một câu LUÔN ĐÚNG từ dữ liệu bài. An
 * toàn, nhưng đó là câu của MÁY CON: nó không biết bé vừa nói gì, không khen được,
 * không sửa được, và lượt nào bị bác cũng ra đúng một khuôn. Thử với mô hình giả
 * "lặp 40%" thì 40% số lượt rơi về đấy — tức gần nửa buổi bé nói chuyện với một
 * cái máy điền chỗ trống, dù mô hình chỉ cần được NHẮC một câu là sửa được ngay.
 *
 * Nên thêm một nấc ở giữa: nói cho mô hình biết nó sai CHỖ NÀO rồi xin câu khác.
 * Lý do bác đã có tên sẵn (`LY_DO_BAC`), mỗi tên một lời nhắc riêng — nhắc chung
 * chung ("câu này không dùng được") thì nó sửa đoán, và thường sửa sang lỗi khác.
 *
 * ⚠ KHÔNG BỎ `cauThayThe`. Nó vẫn là đường lùi CUỐI: hết vòng mà vẫn trượt thì bé
 * phải nghe một câu đúng, chứ không nghe câu sai và cũng không nghe sự im lặng.
 *
 * Trần là HẰNG export, không phải con số viết thẳng trong vòng lặp: mỗi vòng là
 * một lời gọi mạng nữa, mà bé sáu tuổi đang ngồi đợi cô trả lời. Cổng canh hằng.
 */
export const SUA_CO_TOI_DA = 2;

/** Trần ký tự MỘT lời nhắc sửa. Nhắc dài thì nó lấn chỗ của lịch sử nói chuyện. */
export const NHAC_SUA_TOI_DA_CHU = 300;

/* Cắt cho vừa trần mà vẫn nhìn ra là đã bị cắt. Dùng `...` chứ không dùng dấu ba
   chấm liền: lời nhắc sửa là tiếng Anh thuần, và cổng soi đúng chỗ ấy. */
const catChu = (s, n) => (String(s || '').length > n
  ? `${String(s).slice(0, n - 3).trim()}...` : String(s || ''));

/* Mọi chữ tiếng Anh BÀI CÓ DẠY — để chỉ đúng tên chữ lạ trong câu vừa bị bác.
   ⚠ Không gộp với túi `cho` của `loiVietHopLe`, dù hai túi trông giống nhau: túi
   bên ấy còn nhận NGHĨA tiếng Việt và CHỮ BÉ VỪA NÓI, hai thứ không phải là "từ
   cô được dùng". Gộp lại là lời nhắc sửa lặng lẽ nới rào vốn từ. */
const chuDaHoc = (von, tenBe = '') => new Set([
  ...[...von.loi.tu, ...von.on.flatMap((x) => x.tu)]
    .flatMap((t) => [t.tu, t.so_nhieu, t.so_it, t.dang_ing, t.dang_qk]),
  ...[...von.loi.cau, ...von.on.flatMap((x) => x.cau)]
    .flatMap((c) => [c.cau, c.congThuc]),
  ...(von.loi.cauSach || []), ...von.on.flatMap((x) => x.cauSach || []),
  /* `Bill` · `Mai` nằm đây vì chính `soiCau` điền hai tên ấy vào ô `[Name]` — hai
     bên phải cùng một danh sách, lệch nhau thì lời nhắc gọi tên một chữ mà phép
     soi lại chấp nhận, và mô hình bị nhắc sai. */
  ...LOI_LOP_HOC, tenBe, 'Bill', 'Mai',
].filter(Boolean)
  /* Bóc TÊN Ô TRỐNG trước khi tách chữ: để nguyên `Hi, I'm + [Name].` thì "name"
     thành một từ được phép, và "What is your name?" đi lọt mà không ai thấy. */
  .flatMap((x) => chuTrongCau(String(x).replace(/\[[^\]]*\]/g, ' '))));

/**
 * Những chữ trong câu mà bài KHÔNG dạy — thứ phải đọc tên ra trong lời nhắc sửa.
 *
 * ⚠ KHÔNG dùng `tuTrongCau` được, dù nghe thì đúng là nó: hàm ấy trả về các MỤC TỪ
 * của bài CÓ MẶT trong câu, tức trả lời câu hỏi ngược lại, và nó bỏ qua sạch mọi
 * chữ ngoài vốn — đúng những chữ ta đang cần gọi tên.
 */
const tuLaTrongCau = (en, von, tenBe = '') => {
  const cho = chuDaHoc(von, tenBe);
  const ra = [];
  for (const w of chuTrongCau(en)) if (!cho.has(w) && !ra.includes(w)) ra.push(w);
  return ra;
};

/**
 * MỘT LƯỢT `user` NGẮN, BẰNG TIẾNG ANH, NÓI ĐÚNG CHỖ SAI.
 *
 * Bốn lý do bác của `soiCau` là bốn lỗi KHÁC LOẠI nhau, nên bốn lời nhắc khác
 * nhau — bản nháp ở §9 mục B1–B5 của `docs/REVIEW_18_MAU_AI_AGENT_TIENG_ANH.md`.
 *
 * Tiếng Anh thuần và không dấu tiếng Việt: lời nhắc này là lời nói VỚI MÔ HÌNH,
 * không phải lời cho bé đọc, và trộn hai thứ tiếng vào một lượt thì mô hình hay
 * trả lời lẫn theo.
 *
 * Vai `user`, không phải `system` thứ hai — `soiGoi` bác thẳng gói có lời dặn nằm
 * ở vị trí khác 0 (xem `functions/src/luyennoi.js`).
 */
export function loiNhacSua(bac, { von = null, cauTruoc = '', en = '', tenBe = '' } = {}) {
  if (bac === 'rong') {
    return 'Your reply had no English sentence. Reply as JSON {"en": "...", "vi": "..."}'
      + ' with ONE English sentence using only the allowed words.';
  }
  if (bac === 'lap') {
    return `You repeated your previous sentence: "${catChu(cauTruoc, 120)}".`
      + ' Say a DIFFERENT sentence for the same task - change the word in the slot.'
      + ' Reply as JSON.';
  }
  if (bac === 'oTrong') {
    return 'Your sentence still contains an unfilled slot like [Name] or [Month].'
      + " Fill every slot with an allowed word or the child's name. Reply as JSON.";
  }
  if (bac === 'ngoaiVon') {
    const la = von ? tuLaTrongCau(en, von, tenBe) : [];
    /* ⚠ `ngoaiVon` KHÔNG LUÔN LUÔN LÀ "CÓ CHỮ LẠ". Đó là lý do bác CUỐI của
       `soiCau` — câu không đi qua được đường công nhận nào. Một câu chỉ gồm từ bé
       đã học vẫn rơi vào đây nếu nó không phải MẪU CÂU nào của bài ("Book ball
       bike."). Nhắc nó "có chữ lạ" lúc ấy là nhắc sai chỗ, và mô hình sẽ đi đổi
       từ — thứ vốn đã đúng — rồi trượt tiếp đúng một kiểu. */
    if (!la.length) {
      return 'Your sentence is not one of the taught sentence patterns.'
        + ' Use a PATTERN from your instructions, or say just ONE word from the'
        + ' word list. Rewrite for the same task. Reply as JSON.';
    }
    const dau = `Your sentence used words that are NOT allowed: ${catChu(la.join(', '), 60)}.`
      + ' Use ONLY words from the WORD LIST in your instructions';
    const duoi = '. Rewrite the sentence for the same task. Reply as JSON.';
    /* ⚠ "for example" là chữ BẮT BUỘC, không phải cho đẹp. Bảng vốn ĐẦY ĐỦ đã nằm
       trong lời dặn; ở đây chỉ còn chỗ cho vài từ làm mốc. Liệt kê cụt mà viết
       "chỉ được dùng mấy từ này" là tự tay thu vốn của bé xuống còn đúng số từ
       vừa lọt trần 300 ký tự — mô hình tuân lệnh răm rắp, và buổi học nghèo đi. */
    let vd = '';
    for (const t of (von ? von.loi.tu : [])) {
      const thu = vd ? `${vd}, ${t.tu}` : t.tu;
      if (dau.length + ` (for example: ${thu})`.length + duoi.length
          > NHAC_SUA_TOI_DA_CHU) break;
      vd = thu;
    }
    return `${dau}${vd ? ` (for example: ${vd})` : ''}${duoi}`;
  }
  /* Lý do lạ — vẫn phải XIN LẠI, chứ không im lặng rơi thẳng về câu máy con dựng.
     `LY_DO_BAC` mà dài ra một tên nữa thì chỗ này đỡ, không phải chỗ này hỏng. */
  return 'Your sentence could not be used. Reply as JSON with ONE English sentence'
    + ' using only the allowed words.';
}

/**
 * NHẮC SỬA LỜI TIẾNG VIỆT — giữ nguyên câu tiếng Anh, viết lại đúng một dòng.
 *
 * @param kq  chính `loiVietHopLe(...)` trả về; `kq.vi` là LÝ DO hỏng.
 *
 * Khác `loiNhacSua` ở chỗ lời nhắc này CÓ tiếng Việt, và phải có: lỗi hay gặp nhất
 * là cô gọi bé bằng "bạn", mà nói điều ấy bằng tiếng Anh thì mô hình không biết
 * phải thay bằng chữ nào. Nên đưa thẳng hai chữ "cô" và "con" vào lời nhắc.
 *
 * Chỉ dùng cho MỘT vòng (xem `loiVietGoiLai`): câu tiếng Anh đã đúng rồi nên đây
 * chỉ còn là chuyện diễn đạt, mà lời viết sẵn của bước thì luôn có đó.
 */
export function loiNhacSuaViet(kq, { en = '', von = null } = {}) {
  /* ⚠ TRẦN PHẢI SUY RA, đừng cắt mỗi mẩu một con số đoán sẵn. Bản đầu cắt `en` ở
     80 và lý do ở 110, cộng với phần chữ cố định là 320 — vượt trần mà không có
     chỗ nào kêu, vì chốt duy nhất lúc ấy chỉ canh cái đuôi thêm vào. Cổng
     `tienganh_phongnoi.test.mjs` bắt được ngay bằng một lý do dài 500 ký tự. */
  const dau = `Keep the English sentence exactly: "${catChu(en, 70)}".`
    + ' Rewrite ONLY the Vietnamese line: ';
  const duoi = '. Call yourself "cô" and the child "con". Reply as JSON.';
  const lyDo = catChu(kq?.vi || 'lời Việt không dùng được',
    Math.max(20, NHAC_SUA_TOI_DA_CHU - dau.length - duoi.length));
  let s = `${dau}${lyDo}${duoi}`;
  /* Lý do hỏng thường gặp thứ hai là NHẮC LẠI MỘT CHỮ BÀI KHÔNG DẠY, nên đưa luôn
     mấy từ của bài vào làm mốc trích dẫn — nhưng chỉ khi còn chỗ trong trần. */
  const tu = (von ? von.loi.tu : []).map((t) => t.tu).filter(Boolean);
  if (tu.length) {
    const them = ` Quote English words only from: ${tu.join(', ')}.`;
    if (s.length + them.length <= NHAC_SUA_TOI_DA_CHU) s += them;
  }
  return s;
}


/**
 * Câu dựng sẵn cho việc của lượt này — dùng khi câu của cô không qua được phép soi.
 * Luôn đúng, vì nó ghép từ chính dữ liệu bài chứ không sinh ra từ đâu cả.
 */
export function cauThayThe(viec, tenBe = 'con', cauTruoc = '') {
  if (!viec) return null;
  const { tu, kieu, mau } = viec;

  /* Điền HẾT ô, mỗi ô theo loại của nó — xem `dienHetO`. Không điền nổi thì trả
     `null`, và mấy đường lui dưới gánh.
     ⚠ CHỈ NHẬN KHUNG MỘT Ô. Khung hai ô thì ta chỉ có đúng MỘT từ mục tiêu để
     điền, nên cả hai ô nhận cùng chữ ấy: "It's a bell bell." · "Can you village a
     village?" — 62 câu như thế trên bốn quyển. Và `soiCau` cũng không soi nổi khung
     hai ô (nó chỉ điền ô đầu rồi bác phần còn lại), nên câu dựng ra không có đường
     nào được công nhận. Gặp khung hai ô thì nhường cho hai đường lui dưới: chính từ
     mục tiêu, và câu ví dụ của sách — cả hai luôn hợp lệ. */
  const dienVao = (m, dsTu) => {
    if (!m.congThuc) return m.cau;
    if ((m.congThuc.match(/\[[^\]]+\]/g) || []).length !== 1) return null;
    return dienHetO(m.congThuc, dsTu, tenBe);
  };

  /* Xếp sẵn mấy phương án, rồi lấy phương án ĐẦU TIÊN khác câu lượt trước.
     Bản đầu chỉ dựng đúng một câu — mà nếu chính nó trùng câu trước thì luật chống
     lặp thành vô nghĩa: chặn lặp xong lại thay bằng đúng câu vừa chặn. Đã thấy
     thật trên bản chạy: hai lượt liền cùng ra "Hi, I'm Bo." */
  const chon = [];
  if (kieu === KIEU_VIEC.tu || !mau) {
    chon.push({ en: tu.tu, vi: `Con nghe rồi nói lại từ “${tu.tu}” nhé — nghĩa là ${tu.nghia}.` });
  } else if (kieu === KIEU_VIEC.mau) {
    chon.push({ en: mau.cau, vi: 'Con nghe rồi nói lại cả câu này nhé.' });
  } else {
    /* ⚠ ĐIỀN THEO ĐÚNG LUẬT CỦA Ô, dùng chung `dienDuocVaoO` với `soiCau`. Bản cũ
       nhét `tu.tu` vào mọi ô không phải ô tên — nên ô `[Verb-ing]` nhận dạng gốc và
       ô `[Number]` nhận một danh từ, tức đường lui cuối tự sinh ra câu hỏng. */
    const en = dienVao(mau, [tu]);
    if (en) {
      chon.push({ en, vi: `Cùng một mẫu câu, nay điền từ của bài vào. Con nói lại nhé.` });
    }
  }
  /* Đường lui luôn có: chính TỪ mục tiêu, và câu ví dụ. Một trong hai bao giờ cũng
     khác câu lượt trước, vì một cái là từ rời còn một cái là cả câu. */
  chon.push({ en: tu.tu, vi: `Con nghe rồi nói lại từ “${tu.tu}” nhé — nghĩa là ${tu.nghia}.` });
  if (mau) chon.push({ en: mau.cau, vi: 'Con nghe rồi nói lại cả câu này nhé.' });

  const gon = (x) => String(x || '').toLowerCase().replace(/[^a-z0-9' ]/g, '').trim();
  return chon.find((c) => gon(c.en) !== gon(cauTruoc)) || chon[0];
}

/* ─────────── tách một dòng lẫn hai thứ tiếng ─────────── */

/**
 * TÁCH LỜI GIẢI THÍCH THEO THỨ TIẾNG.
 *
 * Bác bắt 13-08: "phần giải thích khi có từ tiếng Anh phát bằng tiếng Việt rất
 * không okay." Đúng, và tệ ở chỗ kho này đã chốt luật ấy từ hồi làm dây chuyền âm
 * — "mỗi dòng chỉ MỘT thứ tiếng" — rồi chính chỗ này vi phạm:
 *
 *     Con nói lại từ "ball" nhé, nghĩa là quả bóng.
 *        → đọc cả dòng bằng vi-VN, và "ball" phát ra thành tiếng Việt
 *
 * Bé đang tập nhại mà nghe từ tiếng Anh đọc giọng Việt thì học sai đúng chỗ mình
 * đang dạy. Cấm mô hình nhắc lại từ tiếng Anh cũng không xong: nhắc lại là việc
 * TỐT ("con nói lại từ ball nhé"), chỉ có đọc sai giọng mới hỏng.
 *
 * ── VÌ SAO KHÔNG ĐOÁN NGÔN NGỮ ──
 * Không cần bộ đoán tiếng nào cả: mình BIẾT TRƯỚC bé đang học những từ nào. Chỉ
 * tách đúng những chuỗi nằm trong vốn từ và câu mẫu của bài — phép xác định, chạy
 * được bằng `node`, và không bao giờ nhận nhầm một chữ tiếng Việt thành tiếng Anh.
 *
 * Tên bé (Bo, Minh An…) CỐ Ý không tách: đó là tên Việt, đọc giọng Việt mới đúng.
 */
export function tachTheoTieng(chu, von, them = []) {
  const s = String(chu || '');
  if (!s.trim()) return [];
  /* Chưa có vốn VÀ chưa có mốc nào thì đừng đọc gì cả — `von` là null khi bài chưa
     nạp xong, và đọc bừa lúc ấy là đọc một dòng chưa thuộc về bài nào. Giữ đúng
     hành vi cũ; cái mới chỉ là: CÓ mốc thì tách được kể cả khi `von` chưa về. */
  if (!von && !them.length) return [];

  const tu = von ? [...von.loi.tu, ...von.on.flatMap((x) => x.tu)].map((t) => t.tu) : [];
  const cau = von ? [...von.loi.cau, ...von.on.flatMap((x) => x.cau)].map((c) => c.cau) : [];

  /**
   * ⚠ MẨU TRONG NGOẶC KÉP CŨNG LÀ TIẾNG ANH — bác bắt 19-08-2026:
   *
   *     "Ở phần hướng dẫn khi có cả tiếng việt và tiếng anh thì bạn lại phát hết
   *      bằng tiếng Việt khiến từ tiếng anh rất khó đọc."
   *
   * Phép tách cũ chỉ nhận ra tiếng Anh khi mẩu ấy nằm trong VỐN TỪ CỦA UNIT. Đúng
   * cho bài thường, hỏng hẳn ở bài tả tranh: câu cô trích là câu của kho TÍCH LUỸ
   * ("How many kites can you see?"), mà vốn của unit 0 chỉ có mười con số — nên cả
   * câu rơi vào nhánh `vi` và Kokoro-VI đọc "kites" theo vần Việt.
   *
   * Đo được: `tachTheoTieng('Cô đang hỏi "How many kites can you see?"…')` trả về
   * ĐÚNG MỘT mẩu, gắn cờ `vi`.
   *
   * Nay lấy thêm hai nguồn mốc, cả hai đều chắc hơn vốn từ:
   *   · mẩu trong NGOẶC KÉP mà không mang dấu tiếng Việt — cô trích thì phải là
   *     tiếng Anh (cùng luật `loiVietHopLe` đang dùng để soi lời Việt);
   *   · `them` — câu cô ĐÃ NÓI trong buổi và bản mô tả tranh, do chỗ gọi đưa vào.
   */
  const trich = [];
  for (const m of s.matchAll(MOC_NGOAC)) {
    const t = (m[1] ?? m[2] ?? '').trim();
    if (t && !CO_DAU_VIET.test(t)) trich.push(t);
  }

  /* Dài trước: "I like milk." phải khớp trọn câu, đừng để nó bị xé thành "milk"
     rời rồi đọc lệch nhịp. Trích dẫn và `them` đứng cùng nhóm câu. */
  const moc = [...trich, ...them, ...cau, ...tu, ...LOI_LOP_HOC].filter(Boolean)
    .sort((a, b) => b.length - a.length);
  if (!moc.length) return [{ chu: s, tieng: 'vi' }];

  const thoat = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  /* Ranh giới từ hai đầu — nếu không, "can" khớp cả trong "cần", và "book" khớp
     trong "bookmark". Dấu câu cuối câu mẫu đã nằm trong chính chuỗi mốc. */
  const re = new RegExp(`(?<![\\p{L}])(${moc.map(thoat).join('|')})(?![\\p{L}])`, 'giu');

  const ra = [];
  let i = 0;
  for (const m of s.matchAll(re)) {
    if (m.index > i) ra.push({ chu: s.slice(i, m.index), tieng: 'vi' });
    ra.push({ chu: m[0], tieng: 'en' });
    i = m.index + m[0].length;
  }
  if (i < s.length) ra.push({ chu: s.slice(i), tieng: 'vi' });

  /**
   * DỌN DẤU MỒ CÔI KHỎI MẨU TIẾNG VIỆT — bác bắt 19-08-2026:
   * "Khi đọc tiếng Việt bạn đọc cả dấu . đâu cần thiết như vậy."
   *
   * Cắt một câu ra làm ba thì dấu câu ở chỗ cắt thành mồ côi:
   *
   *     Cô đang hỏi “   |  How many kites can you see?  |  ”. Con nhìn tranh…
   *                  ↑                                     ↑↑
   * `docDoan` đưa thẳng chuỗi cho bộ đọc, mà giọng Việt thì đọc luôn cái ngoặc kép
   * và cái chấm ấy thành chữ — nghe ra "ngoặc kép chấm". Dấu ngoặc vốn chỉ là ký
   * hiệu cho MẮT, và cái chấm ở đây thuộc về câu tiếng Anh vừa đọc xong, không
   * phải của câu tiếng Việt đứng sau.
   *
   * Chỉ dọn ở mẩu VIỆT. Mẩu tiếng Anh giữ nguyên dấu — dấu hỏi cuối câu là thứ làm
   * nên ngữ điệu hỏi, bỏ đi thì "How many kites can you see" đọc ra như câu kể.
   */
  const donViet = (x) => x
    .replace(/[“”„‟"]/g, ' ')          // ngoặc kép: ký hiệu cho mắt, không phải để đọc
    .replace(/^[\s\p{P}]+/u, '')       // dấu mồ côi ở ĐẦU — của mẩu tiếng Anh vừa rồi
    .replace(/\s+([,.;:!?])/g, '$1')   // khoảng trắng lọt vào trước dấu câu
    .replace(/\s+/g, ' ')
    .trim();

  /* Bỏ mẩu chỉ còn dấu câu hoặc khoảng trắng — đọc lên nghe như bị nấc. */
  return ra
    .map((x) => ({ ...x, chu: x.tieng === 'vi' ? donViet(x.chu) : x.chu.trim() }))
    .filter((x) => /[\p{L}\p{N}]/u.test(x.chu));
}

/* ─────────── soi LỜI TIẾNG VIỆT ─────────── */

/**
 * XƯNG HÔ SAI LÀ ĐỔI CẢ QUAN HỆ.
 *
 * Bác bắt 14-08. Trên bản chạy mô hình viết "Bạn vừa nói câu hỏi…" — với người
 * lớn thì chỉ là lệch giọng, nhưng đây là lớp học của bé sáu tuổi: cô giáo gọi
 * học trò bằng "bạn" thì không còn là cô giáo nữa, và bé mất chỗ dựa. Cả app này
 * xưng "cô" gọi "con" ở mọi màn — riêng phòng nói thì mô hình tự chọn.
 *
 * ⚠ Chính giá trị mặc định của `loiDan` từng là `'bạn nhỏ'`, tức là lời dặn TỰ
 * GIEO chữ "bạn" vào rồi trách mô hình dùng nó.
 *
 * KHÔNG cấm "mình": "Hôm nay mình tập nói nhé" là "chúng ta", đúng và ấm.
 */
export const XUNG_HO_CAM = ['bạn', 'em', 'tớ', 'cậu'];

/**
 * NHỮNG CHỮ ĐI SAU LÀM CHO NÓ THÀNH DANH TỪ, không còn là đại từ gọi bé.
 *
 * "bạn" đã có ngoại lệ từ 14-08 vì sách chú `girl` là "bạn gái". Nay thêm "em":
 * sách chú `brother` là "anh trai, em trai" và `sister` là "chị gái, em gái" —
 * lời viết sẵn của kịch bản lớp 2·3 nhắc lại đúng lời chú ấy, và bị chặn oan. Chặn
 * oan ở đây không kêu thành lỗi: `loiVietSach` lặng lẽ lui về câu chung chung, nên
 * bé mất lời giảng nghĩa mà chẳng ai biết.
 *
 * Cổng bắt được ngay lần đầu soi kịch bản lớp 2 — trước đó cổng chỉ soi lớp 1, mà
 * lớp 1 không dạy "brother".
 *
 * Nới đúng chỗ, KHÔNG nới cả chữ: "Em nói lại đi." vẫn phải bị chặn.
 */
const SAU_KHONG_CAM = {
  bạn: '(?!\\s+(gái|trai|nhỏ|ấy|bè|học))',
  em: '(?!\\s+(gái|trai|bé|nhỏ|ấy|họ))',
};

/* Chữ chỉ có trong tiếng Việt — dùng để biết một mẩu trong ngoặc kép là lời Việt
   hay là tiếng Anh. Không cần bộ đoán ngôn ngữ, chỉ cần dấu. */
const CO_DAU_VIET = /[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/i;

/**
 * MẨU NẰM TRONG NGOẶC KÉP — chỗ cô trích lại một câu tiếng Anh.
 *
 * ⚠ DẤU NHÁY GIỮA MỘT TỪ KHÔNG PHẢI DẤU MỞ NGOẶC. Bản cũ viết `'([^']{2,})'`, nên
 * một dòng có HAI chữ rút gọn tiếng Anh là hỏng ngay: `He's/She's + [Number].` bị
 * đọc thành mẩu trích `s/She`, rồi báo `chữ "s" không có trong bài`. Câu hoàn toàn
 * đúng mà bị gạt — và gạt thì `loiVietSach` lặng lẽ lui về lời chung chung, không
 * ai biết là đã mất một lời dẫn.
 *
 * Mà tiếng Anh lớp 1·2·3 thì đầy chữ rút gọn: It's · What's · He's · isn't. Nên
 * đây không phải ca hiếm, chỉ là chưa có kịch bản nào dùng tới hai cái một dòng.
 * Cổng bắt được ngay lần đầu soi kịch bản lớp 2.
 *
 * Nay dấu nháy chỉ được coi là ngoặc khi nó KHÔNG dính vào chữ ở phía ngoài.
 */
const MOC_NGOAC = /[""“”]([^""“”]+)[""“”]|(?<![\p{L}\p{N}])'([^']{2,})'(?![\p{L}\p{N}])/gu;

/**
 * SOI LỜI TIẾNG VIỆT CỦA CÔ. Trả `{ ok, vi }` — `vi` là lý do khi hỏng.
 *
 * ── VÌ SAO PHẢI SOI, DÙ ĐÃ DẶN ──
 * Câu tiếng Anh đã có chốt từ lâu (`cauHopLe`, và có kịch bản thì ép thẳng về câu
 * đúng). Lời tiếng Việt thì chưa bị soi một lần nào — và đó đúng là chỗ hai lỗi
 * bác vừa bắt sống được.
 *
 * ── HAI THỨ SOI ──
 * 1. XƯNG HÔ — xem trên.
 * 2. NHẮC LẠI SAI TỪ. Trên bản chạy: cô nhắc `"How many washes can you see?"` —
 *    một câu bé chưa từng nói và không có trong sách. Hỏng kép: bé nghe nhầm mình
 *    đã nói thế, VÀ mẩu ấy không nằm trong vốn nên `tachTheoTieng` không tách ra,
 *    thành thử nó bị đọc bằng GIỌNG VIỆT — đúng cái luật "mỗi dòng một thứ tiếng"
 *    mà bác đã bắt sửa hôm 13-08.
 *
 * Chỉ soi mẩu TRONG NGOẶC KÉP, vì đó là chỗ mô hình nhắc lại lời, và cũng là chỗ
 * duy nhất tách được chắc chắn. Mẩu nào có dấu tiếng Việt thì bỏ qua — `"đỏ"` là
 * lời Việt, không phải tiếng Anh.
 *
 * ── ĐÁNH ĐỔI, NÓI THẲNG ──
 * Một chữ tiếng Việt KHÔNG DẤU nằm trong ngoặc (`"con"`) sẽ bị coi nhầm là tiếng
 * Anh và câu bị trả về. Chấp nhận: hỏng theo hướng ấy chỉ mất một lời dẫn hay,
 * còn hỏng theo hướng kia là bé học sai. Và đường lui luôn có — lời viết sẵn của
 * chính bước ấy.
 */
export function loiVietHopLe(vi, { von, cauDich = '', beNoi = '' } = {}) {
  const s = String(vi || '');
  if (!s.trim()) return { ok: false, vi: 'lời Việt rỗng' };

  /* ⚠ "bạn" KHÔNG phải lúc nào cũng là đại từ gọi bé. Sách chú `girl` là "bạn
     gái", `friend` là "bạn bè" — ở đó nó là DANH TỪ, và chặn nhầm là chặn luôn
     lời giải nghĩa của chính sách. Cổng bắt được thật: Unit 7, từ "girl".
     Nên trừ mấy dạng ghép ra. Danh sách ngắn và có cổng canh cả hai chiều. */
  /* ⚠ BỎ PHẦN TRONG NGOẶC KÉP TRƯỚC KHI SOI ĐẠI TỪ.
     Luật này canh CÁCH CÔ GỌI BÉ, không canh chữ. Mà sách chú `you` là "bạn, các
     bạn" và `friend` là "bạn, bạn bè" — cô giảng nghĩa thì phải nhắc lại đúng lời
     chú ấy. Bản cũ chặn luôn, và chặn thì `loiVietSach` lặng lẽ lui về lời chung
     chung: bé mất hẳn lời giảng nghĩa mà không ai biết. Cổng bắt được ở lớp 3
     unit 1 — trước đó cổng chỉ soi lớp 1, mà lớp 1 không dạy "you".
     Trong ngoặc là TRÍCH DẪN, ngoài ngoặc mới là lời cô nói với bé. `Bạn nói lại
     đi.` vẫn bị chặn như cũ vì nó không nằm trong ngoặc nào. */
  const ngoaiNgoac = s.replace(/[""“”][^""“”]*[""“”]/g, ' ');
  const xau = XUNG_HO_CAM.find((x) => new RegExp(
    `(?<![\\p{L}])${x}(?![\\p{L}])${SAU_KHONG_CAM[x] || ''}`, 'iu').test(ngoaiNgoac));
  if (xau) return { ok: false, vi: `gọi bé bằng "${xau}" — cô phải gọi "con"` };

  if (!von) return { ok: true, vi: '' };
  /**
   * Soi theo TỪNG CHỮ, không đòi khớp trọn câu.
   *
   * Bản đầu đòi mẩu trong ngoặc phải là NGUYÊN một câu của sách, và cổng bắt được
   * ngay chính lời viết tay của Unit 9: `mở đầu bằng "How many" nhé` — một MẨU
   * của câu, mà trỏ vào mẩu mở đầu lại đúng là cách dạy hay nhất ở đó.
   *
   * Soi theo chữ thì vừa cho mẩu đi qua, vừa vẫn bắt được đúng chỗ hỏng thật:
   * `"How many washes can you see?"` — how·many·can·you·see đều có trong bài,
   * riêng "washes" thì không (bài dạy "wash", và "washes" là một chữ khác).
   */
  const cho = new Set([
    ...[...von.loi.tu, ...von.on.flatMap((x) => x.tu)].map((t) => t.tu),
    ...[...von.loi.cau, ...von.on.flatMap((x) => x.cau)].map((c) => c.cau),
    ...(von.loi.cauSach || []), ...von.on.flatMap((x) => x.cauSach || []),
    ...LOI_LOP_HOC, cauDich,
    /* ⚠ CHỮ BÉ VỪA NÓI CŨNG ĐƯỢC PHÉP NHẮC LẠI — nếu không thì lượt SỬA tự bóp cổ
       mình. Cô sửa bé thì phải trích đúng cái bé vừa nói ("con nói 'It cooking',
       thiếu chữ 's' "), mà cái bé nói lại chính là một chữ KHÔNG có trong bài —
       nên `loiVietHopLe` gạt, và `loiVietSach` lui về câu viết sẵn. Lời sửa cụ thể
       bị vứt đi đúng lượt cần nó nhất, và không gì kêu cả.
       Mở chỗ này KHÔNG phá luật 10: luật cấm cô BỊA ra một chữ bé chưa từng nói,
       chứ không cấm cô nhắc lại chữ bé vừa nói ra miệng. */
    beNoi,
    /* ⚠ LỜI CHÚ NGHĨA CỦA SÁCH CŨNG ĐƯỢC PHÉP TRÍCH.
       Phép soi này đoán "trong ngoặc là tiếng Anh hay tiếng Việt" bằng DẤU. Mà
       tiếng Việt không phải lúc nào cũng có dấu: sách chú `top` là "con quay",
       `ba` là "cha" — không một ký tự nào có dấu, nên mẩu ấy bị soi như tiếng Anh
       và "con" hoá thành chữ lạ. Cô giảng nghĩa đúng lời sách mà bị gạt, rồi
       `loiVietSach` lặng lẽ lui về câu chung chung. Cổng bắt được ở lớp 1 unit 14.
       Nghĩa nằm ngay trong `von`, nên nhận chúng vào túi là đủ và không nới thêm
       gì ngoài đúng lời sách. */
    ...[...von.loi.tu, ...von.on.flatMap((x) => x.tu)].map((t) => t.nghia),
  ].filter(Boolean).flatMap((x) => chuTrongCau(x)));

  for (const m of s.matchAll(MOC_NGOAC)) {
    const trong = (m[1] ?? m[2] ?? '').trim();
    if (!trong || CO_DAU_VIET.test(trong)) continue;   // lời Việt, không phải tiếng Anh
    const la = chuTrongCau(trong).find((w) => !cho.has(w));
    if (la) {
      return { ok: false, vi: `nhắc lại "${trong}" — chữ "${la}" không có trong bài` };
    }
  }
  return { ok: true, vi: '' };
}

/* ─────────── một buổi có mở có kết ─────────── */

/**
 * BUỔI LUYỆN NÓI PHẢI CÓ CHỖ KẾT.
 *
 * Bác dặn 13-08: cô phải chủ động kết thúc khi bé đã nắm bài (khen rồi dừng), hạ
 * độ khó khi bé đuối, và mỗi phiên tối đa 20 phút.
 *
 * Bản trước không có chỗ kết nào: cô hỏi mãi, bé trả lời mãi. Với bé 6 tuổi thì
 * một việc không có vạch đích là một việc không bao giờ thấy mình làm được — mà
 * "thấy mình làm được" mới là thứ giữ bé quay lại.
 *
 * Ba đường kết, và cả ba đều do MÁY CON quyết chứ không hỏi mô hình:
 *
 *   xongGioi   bé đạt liên tiếp đủ số lượt   → khen thật, rồi dừng
 *   hetGio     quá 20 phút                    → dừng tử tế, hẹn lần sau
 *   haDoKho    bé đuối liên tiếp              → KHÔNG dừng, mà hạ xuống chỉ luyện TỪ
 *
 * `haDoKho` cố ý không phải một đường KẾT: bé đang đuối mà bị đuổi ra khỏi phòng
 * thì thông điệp bé nhận được là "con dốt quá". Hạ độ khó rồi cho làm tiếp mới
 * đúng — cùng tinh thần với luật "thử thật 2 lần" ở `dandat.js`.
 */
export const PHUT_TOI_DA = 20;
export const DAT_LIEN_DE_XONG = 3;
export const KEM_LIEN_DE_HA = 3;

/**
 * @param lichSu  các lượt, lượt của bé có `diem` (null nếu không chấm được)
 * @param batDau  mốc thời gian mở phòng (ms)
 * @param bayGio  ms — tiêm vào để cổng chạy được mà không phụ thuộc đồng hồ thật
 */
/**
 * NHỮNG LƯỢT CỦA BÉ THẬT SỰ LÀ MỘT LẦN LUYỆN.
 *
 * ⚠ LƯỢT ĐÁP LỜI CHÀO KHÔNG PHẢI MỘT LẦN LUYỆN, và bỏ sót chuyện này làm hỏng hai
 * thứ cùng lúc — cả hai chỉ lộ ra khi trải từng lượt của một buổi ra giấy:
 *
 *   · BUỔI KẾT SỚM MỘT NẤC. `DAT_LIEN_DE_XONG = 3`, mà lượt "hello" của bé đã ăn
 *     mất một suất. Bé giỏi chỉ phải nói ĐÚNG HAI câu là được khen "con nắm bài
 *     rồi" — trong khi bác chốt con số 3 là ba lần NẮM BÀI.
 *   · BƯỚC ĐẦU BỊ NHẢY CÓC. Bước luyện chọn theo `soDat % n`; lượt chào đẩy chỉ số
 *     lên 1, nên bước thứ 0 — bước `mau`, chỗ cô LÀM MẪU — không bao giờ tới lượt.
 *     Bé bị hỏi "What's your hobby?" ngay khi chưa hề nghe mẫu câu nào.
 *
 * Không có gì đỏ ở cả hai chỗ: cô vẫn nói đúng câu của bài, màn kết vẫn chúc mừng.
 *
 * Biết được lượt nào là luyện nhờ mỗi lượt của cô nay mang theo `buoc` — loại bước
 * đã sinh ra nó (`goiPhongNoi.js` trả về, `PhongNoi.jsx` giữ lại). Buổi cũ không có
 * trường ấy thì coi như luyện: thà đếm rộng còn hơn bỏ mất tiến độ đã có của bé.
 */
const BUOC_KHONG_LUYEN = new Set(['chao', 'hoiThich', 'ket']);

export function luotLuyen(lichSu = []) {
  const ra = [];
  for (let i = 0; i < lichSu.length; i += 1) {
    const x = lichSu[i];
    if (x?.vai !== 'be' || x.diem == null) continue;
    const truoc = lichSu.slice(0, i).reverse().find((y) => y?.vai === 'may');
    if (truoc?.buoc && BUOC_KHONG_LUYEN.has(truoc.buoc)) continue;
    ra.push(x);
  }
  return ra;
}

export function tinhBuoi({ lichSu = [], batDau = null, bayGio = null, datNguong = 6,
                          dichCaDoan = false } = {}) {
  const cuaBe = luotLuyen(lichSu);
  /* `batDau == null` mới là "chưa bấm giờ". Viết `batDau ? … : 0` thì mốc 0 — một
     con số hợp lệ — bị coi là chưa bắt đầu, và đồng hồ không bao giờ chạy. Cùng họ
     với lỗi `Date.parse(0)` ra năm 2000 đã ghi trong sổ. */
  const coGio = batDau != null && bayGio != null;
  const phut = coGio ? Math.max(0, (bayGio - batDau) / 60000) : 0;

  /* Đếm chuỗi ĐUÔI: chỉ tính mấy lượt gần đây nhất, không tính cả buổi. Bé vào
     phòng lúc còn lóng ngóng rồi khá dần lên là chuyện thường — lấy cả buổi ra
     tính thì mãi mãi không đạt. */
  let datLien = 0;
  let kemLien = 0;
  for (let i = cuaBe.length - 1; i >= 0; i -= 1) {
    if (cuaBe[i].diem >= datNguong) { if (kemLien) break; datLien += 1; } else { if (datLien) break; kemLien += 1; }
  }

  const hetGio = phut >= PHUT_TOI_DA;

  /* ══ BÀI TẢ TRANH KẾT Ở CHỖ KHÁC ══ (bác chốt 19-08-2026)
     "sau vài câu trả lời thì cô xâu chuỗi lại thành 01 đoạn nói cho học sinh nói cả
     đoạn đó" — bước `caDoan` LÀ ĐÍCH của cả buổi.

     Mà `DAT_LIEN_DE_XONG = 3` thì cắt buổi ở lượt thứ ba, tức là ngay trước khi tới
     đó: trải ra giấy thấy buổi kết sau taTranh + hai câu gợi ý, bé chưa bao giờ nói
     cả đoạn. Không lỗi, không cảnh báo, màn kết vẫn chúc mừng — đúng kiểu hỏng đã
     gặp mấy lần ở phòng này.

     Nên buổi tả tranh chỉ xong khi bé đã NÓI ĐƯỢC CẢ ĐOẠN. Chưa được thì cứ tiếp,
     và `hetGio` vẫn là cái phanh cuối. */
  const daCaDoan = dichCaDoan && lichSu.some((x, i) => x.vai === 'may' && x.buoc === 'caDoan'
    && lichSu.slice(i + 1).some((y) => y.vai === 'be' && y.diem >= datNguong));
  const xongGioi = dichCaDoan ? daCaDoan : datLien >= DAT_LIEN_DE_XONG;
  return {
    trangThai: xongGioi ? 'xongGioi' : hetGio ? 'hetGio' : 'dang',
    haDoKho: !xongGioi && kemLien >= KEM_LIEN_DE_HA,
    datLien,
    kemLien,
    phut,
    phutConLai: Math.max(0, PHUT_TOI_DA - phut),
    soLuotBe: cuaBe.length,
    soDat: cuaBe.filter((x) => x.diem >= datNguong).length,
  };
}

/** Lời kết — nói thẳng bé làm được gì, không phải một câu khen chung chung. */
export function loiKet(buoi) {
  if (!buoi) return null;
  if (buoi.trangThai === 'xongGioi') {
    return {
      bieuTuong: '🎉',
      en: 'Well done! Goodbye!',
      tieuDe: 'Con nói được rồi!',
      chu: `Con nói đúng ${buoi.datLien} câu liền. Hôm nay thế là giỏi lắm — mai mình nói tiếp nhé.`,
    };
  }
  if (buoi.trangThai === 'hetGio') {
    return {
      bieuTuong: '⏰',
      en: 'Good job! Goodbye!',
      tieuDe: 'Hết giờ nói chuyện rồi',
      chu: `Con đã nói ${buoi.soLuotBe} lượt, đúng ${buoi.soDat} lượt. Nghỉ mắt một lát rồi mai mình nói tiếp nhé.`,
    };
  }
  return null;
}

/**
 * CÂU KẾT CŨNG PHẢI NGHE ĐƯỢC — bác dặn 14-08.
 *
 * Cả buổi bé nghe từng câu một, tới lúc chia tay thì màn hình đưa ra một khối chữ
 * im lặng. Bé lớp 1 chưa đọc chữ: với bé thì phòng học vừa tắt tiếng giữa chừng.
 * Mà lời chia tay lại đúng là thứ ĐÁNG học nhất — ngày nào cũng dùng.
 *
 * ── VÌ SAO CHỈ ĐƯỢC DÙNG LỜI LỚP HỌC ──
 * Câu này do MÁY CON viết, không qua mô hình, nên không có gì chặn nó dùng từ lạ.
 * "See you tomorrow." nghe rất tự nhiên — và có ba từ bé chưa từng gặp. Câu cuối
 * cùng của buổi mà bé không nhại nổi thì buổi học kết thúc bằng một thất bại.
 *
 * Nên bó vào đúng `LOI_LOP_HOC`, và có cổng đếm từng chữ. Muốn thêm câu chia tay
 * mới thì thêm vào `LOI_LOP_HOC` trước — chỗ ấy mô hình cũng dùng, nên hai bên
 * không bao giờ lệch nhau.
 */
const chuCai = (s) => String(s || '').toLowerCase().split(/[^a-z']+/).filter(Boolean);

export function tuLoiKetHopLe(en) {
  const cho = new Set(LOI_LOP_HOC.flatMap(chuCai));
  const tu = chuCai(en);
  return tu.length > 0 && tu.every((t) => cho.has(t));
}

/* ─────────── hồ sơ của chính bé ─────────── */

/**
 * DÙNG THÔNG TIN CỦA CHÍNH BÉ, KHÔNG PHẢI CÂU TĨNH.
 *
 * Bác dặn 13-08: "cần có kịch bản hỏi thông tin cá nhân của học sinh để khi nói
 * chuyện sẽ dùng thông tin ấy để luyện, thay vì các thông tin tĩnh."
 *
 * Bé nói "I like milk." trong khi bé ghét sữa thì đó là nhại một câu của người
 * khác. Nói "I like fish." vì bé thật sự thích cá thì bé đang NÓI VỀ MÌNH — cùng
 * một mẫu câu, nhưng một bên là học vẹt còn một bên là dùng tiếng Anh.
 *
 * ── HỎI THẾ NÀO, VÀ VÌ SAO KHÔNG ĐỂ MÔ HÌNH HỎI ──
 * Chính APP hỏi, bằng tiếng Việt, và bé trả lời bằng cách BẤM VÀO HÌNH — không gõ,
 * không nói tự do. Ba lý do:
 *
 *   · bé 6 tuổi không gõ được, mà nói tự do thì bộ nhận dạng nghe ra gì cũng được;
 *   · câu trả lời rơi đúng vào vốn từ của bài, nên không rò từ lạ vào phòng;
 *   · KHÔNG có thông tin riêng tư nào mới rời khỏi máy — chỉ là một từ trong sách,
 *     đúng thứ bé vừa học. Tên và lớp thì app đã có sẵn từ hồ sơ.
 *
 * Cố ý KHÔNG hỏi tuổi, trường, nhà ở đâu, hay bất cứ thứ gì nhận dạng được bé.
 */
export function cauHoiSoThich(von) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  if (tu.length < 2) return null;
  return {
    hoi: 'Con thích cái nào nhất?',
    chon: tu,
  };
}

/**
 * BUỔI HÔM NAY DẠY GÌ — lấy từ chính kịch bản của unit.
 *
 * Bác dặn 18-08: "xây dựng kịch bản/prompt cho AI theo từng Unit mới đảm bảo sát
 * nội dung". Câu tiếng Anh thì đã sát từ trước (kịch bản ép từng câu một), nhưng
 * cái KHUNG buổi học thì chưa: lời dặn cũ chỉ đưa một bảng từ và một bảng công
 * thức: đủ để nói đúng, không đủ để biết đang dạy bài gì.
 *
 * Ba dòng, và cả ba đều đã có sẵn trong bài — `objective.text` là năng lực sách
 * khai cho unit, `tinhHuong` là hoàn cảnh sách đặt ra cho mẫu câu. Không soạn tay,
 * nên không lệch với sách được.
 */
function dongUnit(u) {
  const d = [];
  if (u.ten) d.push(`TODAY'S UNIT: ${u.ten}`);
  if (u.muc_tieu) d.push(`  By the end she should be able to: ${u.muc_tieu}`);
  if (u.tinh_huong) d.push(`  The situation the book sets up: ${u.tinh_huong}`);
  /* ══ BỨC TRANH — CÔ CÓ BẢN MÔ TẢ, BÉ THÌ KHÔNG ══ (bác chốt 19-08-2026)
     "AI sẽ có phần mô tả bức tranh bằng chữ còn học sinh thì chỉ được nhìn tranh
     thôi."
     Đây là chỗ phòng nói làm được việc mà nó chưa bao giờ làm được: SỬA Ý. Trước
     nay cô chỉ có câu mẫu, nên bé nói sai số hay sai vật thì cô không biết — chấm
     phát âm vẫn cao. Nay cô biết trong tranh có gì. */
  if (u.moTaTranh?.length) {
    d.push('THE PICTURE — she can see it, you only have these words for it:');
    for (const c of u.moTaTranh) d.push(`  · ${c}`);
    d.push('  Ask her about the picture and check her answer against these lines.',
      '  If she says a wrong number or names a thing that is not there, correct THAT',
      '  — not just her pronunciation. Never read the whole description out to her:',
      '  she is meant to find the words herself.');
  }
  return d;
}

/** Lời dặn thêm về bé — chỉ những gì app đã có, không hỏi thêm gì. */
function dongHoSo(hoSo, tenBe) {
  /* ⚠ KHÔNG lui sớm khi `hoSo` rỗng. Từ 09-10 tên bé CHỈ còn ở khối này (dòng đầu
     lời dặn đã bỏ nó ra, xem ghi chú trên), nên lui sớm là cô giáo máy không biết
     bé tên gì — và mọi ô `[Name]` nhận "con". Bé chưa có hồ sơ nào là chuyện
     thường: buổi đầu tiên. */
  const d = [];
  if (tenBe) d.push(`The child's name is ${tenBe} — use it in [Name] slots.`);
  if (!hoSo) return d.length ? `${DAU_KHOI_RIENG}\nABOUT THE CHILD: ${d.join(' ')}\n${CUOI_KHOI_RIENG}` : '';
  if (hoSo.thich) {
    d.push(`The child told you they like "${hoSo.thich}".`
      + ' Prefer that word when a pattern needs a thing — it makes the sentence about them.');
  }

  /* ══ VECTOR TRẠNG THÁI S = [C, T, P, M] (mục 2.1.2 luận văn) ══
     Bốn chiều đã đo xong ở các đợt trước, nhưng cho tới đây chúng nằm rời: chiều
     C ở `mastery`, T ở thẻ ôn và phép quên, P ở bảng định dạng, M ở sở thích.
     Gom lại thành MỘT khối để cô giáo máy biết mình đang nói với ai.

     ⚠ NÓI BẰNG CÂU NGƯỜI ĐỌC ĐƯỢC, ĐỪNG ĐỔ SỐ VÀO. "p=0.42" thì mô hình không
     biết làm gì với nó, mà chỗ nào cũng có thể hiểu khác đi. "She is still shaky
     on this unit" thì rõ một nghĩa.

     ⚠ KHÔNG NHẮC TỚI ĐIỂM SỐ TRƯỚC MẶT BÉ. Lời dặn này đi vào prompt, và mô hình
     rất dễ nhại lại nguyên văn. Nên câu nào ở đây cũng phải là câu KHÔNG SAO nếu
     lỡ bị đọc to lên. "Con được 42%" thì không phải câu như thế. */
  if (hoSo.mucNam === 'yeu') {
    d.push('She is still shaky on this unit — keep sentences short, stay with words'
      + ' she has met many times, and praise small correct bits.');
  } else if (hoSo.mucNam === 'vung') {
    d.push('She is solid on this unit — you may ask slightly longer questions and'
      + ' let her lead more of the turns.');
  }
  if (hoSo.dangManh) {
    d.push(`She answers best in "${hoSo.dangManh}" style tasks.`);
  }
  if (hoSo.hayQuen) {
    d.push('She has not touched some of this for a while — bring back one or two'
      + ' older words on purpose.');
  }
  if (hoSo.deMet) {
    d.push('She slows down towards the end of a session — keep this one brisk.');
  }

  /* ── TRÍ NHỚ QUA NHIỀU BUỔI ── (việc V3, `lib/hosoai.js`)
     Mấy dòng trên nói về buổi NÀY; khối này nói về những buổi TRƯỚC. Giữ nguyên
     quy ước của khối trên: không số, và câu nào cũng phải KHÔNG SAO nếu lỡ bị đọc
     to lên — `dongHoSoAI` tự chặn chữ số ở đúng một chỗ trước khi trả về. */
  const nho = dongHoSoAI(hoSo.ai, tenBe);

  const than = [d.length ? `ABOUT THE CHILD: ${d.join(' ')}` : '', nho]
    .filter(Boolean).join('\n');
  if (!than) return '';
  /* ⚠ BỌC CẢ KHỐI TRONG DẤU RIÊNG. Mọi chữ của bé trong lời dặn nằm giữa hai dấu
     này, và `locKhung` ở `functions/src/vantay.js` bỏ SẠCH phần giữa — nên vân tay
     prompt không bao giờ đổi theo bé. Dấu khối chắc hơn dấu từng dòng: thêm một
     dòng mới vào khối thì nó tự động được che, không phải khai thêm mẫu nào. */
  return `${DAU_KHOI_RIENG}\n${than}\n${CUOI_KHOI_RIENG}`;
}

/* ─────────── kịch bản viết sẵn cho từng bài ─────────── */

/**
 * ĐI THEO KỊCH BẢN CỦA CHÍNH BÀI ẤY.
 *
 * Bác chốt 13-08: "viết sẵn kịch bản theo từng bài học để AI theo bài nào thì
 * dùng kịch bản đó sẽ đảm bảo hơn."
 *
 * Có bằng chứng cho chữ "đảm bảo hơn". Trong một buổi đi thử, mô hình đã hai lần
 * KHÔNG theo lời dặn dù lời dặn viết rất rõ: sinh ra "Bye, bike." (nhét đồ vật vào
 * ô của tên người), và nói y một câu hai lượt liền ngay sau khi được dặn đừng lặp.
 *
 * Dặn dò là thứ mô hình CÓ THỂ theo. Kịch bản là thứ nó KHÔNG CẦN theo — câu tiếng
 * Anh đã nằm sẵn trong `ta1/kichban_noi.json`, nó chỉ còn viết lời tiếng Việt và
 * phản ứng với cái bé vừa nói. Rút đúng cái quyền hay hỏng ra khỏi tay nó.
 *
 * ── BƯỚC TIẾN THEO SỐ LƯỢT BÉ ĐẠT, KHÔNG THEO SỐ LƯỢT ĐÃ NÓI ──
 * Bé chưa đạt thì đứng yên ở bước ấy để được thử lại. Tiến theo số lượt đã nói thì
 * bé nói sai cũng bị đẩy sang bài mới — đúng cái làm bé hụt hơi rồi bỏ.
 */
/**
 * NHỮNG BƯỚC NẰM TRONG VÒNG LUYỆN THƯỜNG — TOÀN LÀ BƯỚC CÂU.
 *
 * ⚠ `tu` KHÔNG còn ở đây, và đó là chỗ sửa chính của bản 18-08.
 *
 * Bác xem phòng rồi bảo "chẳng có hiệu quả gì". Trải kịch bản ra thì rõ: unit 5
 * lớp 3 có 15 bước, tám bước là MỘT CHỮ TRẦN ("cooking", "dancing"). Mà buổi kết
 * thúc ở `DAT_LIEN_DE_XONG = 3` lần nói đúng — nên bé giỏi làm xong buổi mà chưa
 * hề nói một câu nào. Bé học được tám cái nhãn, không học được cách nói.
 *
 * Nay bước `tu` chỉ còn là ĐƯỜNG LUI: bé trượt mấy lượt liền thì `haDoKho` bật và
 * vòng luyện thu về đúng mấy bước ấy. Bỏ hẳn chúng đi thì bé đuối không còn gì
 * bám — xem nhánh `haDoKho` ngay dưới.
 */
const BUOC_LUYEN = new Set(['mau', 'noiCa', 'hoiBe', 'doiVai', 'thay',
  /* ── BA NHỊP CỦA BÀI TẢ TRANH ── (bác chốt 19-08-2026)
     "Chỉ để một bức tranh sau đó yêu cầu học sinh mô tả bức tranh. […] học sinh
     không biết tả thì cô hỏi how many kite in the picture. […] sau vài câu trả lời
     thì cô xâu chuỗi lại thành 01 đoạn nói cho học sinh nói cả đoạn đó."
       taTranh  cô mời bé tả
       goiY     bé bí thì cô hỏi từng chi tiết
       caDoan   tả được rồi thì nói CẢ ĐOẠN — đích của buổi */
  'taTranh', 'goiY', 'caDoan']);

/** Bước lùi về khi bé đuối — dễ nhất, và chỉ có ở đây. */
/* Bước lùi về khi bé đuối. Với bài TẢ TRANH thì đường lui là CÂU HỎI GỢI Ý — bé
   không tả nổi thì được hỏi từng chi tiết một, đúng như bác tả. Nên kịch bản tranh
   không cần bước `tu` nào. */
const BUOC_DE = new Set(['tu', 'goiY']);

/** Điền {ten} và {thich} vào câu của bước. Thiếu thì dùng `mac_dinh` đã ghi sẵn. */
export function dienBuoc(buoc, { tenBe = '', thich = '' } = {}) {
  if (!buoc?.en) return '';
  /* ⚠ THỨ BÉ THÍCH CHỈ ĐIỀN ĐƯỢC VÀO Ô THƯỜNG — vá 09-10-2026.
     Bé thích "bus" thì ô `[Number]` của mẫu tuổi nhận "bus": "He's bus." Chỗ hỏng
     thứ BA của cùng một lỗi (hai chỗ kia: `soiCau` và bộ sinh kịch bản Python), và
     là chỗ duy nhất chỉ lộ ra lúc CHẠY, vì nó phụ thuộc vào sở thích của từng bé —
     nhìn tệp JSON thì kịch bản trông sạch.
     Ô có kiểu thì dùng `mac_dinh`: bộ sinh nay tính nó theo đúng loại ô. Mất một
     chút "nói về thứ con thích" ở mấy mẫu ấy, nhưng câu thì không bao giờ sai —
     và một câu sai thì bé nhại theo. */
  const loai = loaiOTrong(buoc.khung);
  const duocThich = !loai || loai === 'tu';
  return buoc.en
    .replace(/\{ten\}/g, tenBe || buoc.mac_dinh || 'con')
    .replace(/\{thich\}/g, (duocThich && thich) || buoc.mac_dinh || '');
}

export function buocTiepTheo({
  kichBan, lichSu = [], hoSo = null, haDoKho = false, datNguong = 6,
} = {}) {
  const ds = kichBan?.buoc || [];
  if (!ds.length) return null;

  /* Chỉ đếm lượt LUYỆN — lượt đáp lời chào không đẩy kịch bản đi được. Xem
     `luotLuyen`: bỏ sót chỗ này thì bước `mau` bị nhảy cóc, và bé bị hỏi trước khi
     nghe mẫu. */
  const soDat = luotLuyen(lichSu).filter((x) => x.diem >= datNguong).length;
  const daChao = lichSu.some((x) => x.vai === 'may');

  /* Lọc những bước KHÔNG còn phải làm nữa: chào rồi thì thôi chào, bé chọn sở
     thích rồi thì thôi hỏi lại. Đuối thì lùi hẳn về các bước TỪ. */
  const soLuotBe = lichSu.filter((x) => x.vai === 'be' && x.diem != null).length;

  const conLai = ds.filter((b) => {
    if (b.loai === 'ket') return false;
    if (b.loai === 'chao') return !daChao;
    /**
     * ⚠ HỎI SỞ THÍCH CHỈ ĐƯỢC CHIẾM ĐÚNG MỘT LƯỢT.
     *
     * Bản cũ viết `return !hoSo?.thich` — nghe rất hợp lý: bé chưa chọn thì còn
     * phải hỏi. Nhưng bé KHÔNG BẮT BUỘC phải chọn, và thẻ hỏi thì máy con tự vẽ
     * chứ không cần lượt nào của cô. Bé cứ nói mà không bấm hình là điều kiện ấy
     * đúng mãi mãi, và `buocTiepTheo` trả về `hoiThich` cho MỌI lượt còn lại.
     *
     * Mà `dongBuoc` của `hoiThich` là chuỗi RỖNG. Nghĩa là suốt buổi mô hình
     * không nhận được một dòng dẫn nào — cả tầng kịch bản viết sẵn nằm đó không
     * chạy. Đã dò cả 16 bài: bài nào cũng thế.
     *
     * Không có gì đỏ, không có gì chậm, cô vẫn nói năng trôi chảy — vì `cauHopLe`
     * vẫn gác vốn từ nên câu nào lọt ra cũng đúng. Chỉ là nó tự nghĩ, đúng cái
     * việc bác bảo phải rút khỏi tay nó. Chỉ lộ khi trải thử từng lượt một.
     *
     * Nay: hỏi khi bé chưa chọn VÀ bé chưa nói câu nào. Bé đáp lời chào là hết
     * cửa hỏi — thẻ chọn hình vẫn còn đó cho bé bấm lúc nào cũng được, nhưng
     * kịch bản thì đi tiếp.
     */
    if (b.loai === 'hoiThich') return !hoSo?.thich && soLuotBe === 0;
    return haDoKho ? BUOC_DE.has(b.loai) : BUOC_LUYEN.has(b.loai);
  });
  /* Kịch bản không có bước dễ nào (mấy bản sửa tay của lớp 1) thì đừng trả rỗng:
     rỗng nghĩa là cả tầng kịch bản tắt, và bé đang đuối lại rơi vào chỗ mô hình tự
     nghĩ câu — đúng lúc ít chịu nổi nhất. */
  const ds2 = conLai.length ? conLai
    : ds.filter((b) => BUOC_LUYEN.has(b.loai));
  if (!ds2.length) return null;

  /* Bước MỘT LẦN (chào · hỏi sở thích) làm cho xong trước, và KHÔNG đếm chung với
     bước luyện: chào không phải một lần "đạt". Bản đầu trộn hai loại vào cùng phép
     đếm nên bước hỏi sở thích bị nhảy cóc — bé chưa kịp chọn gì thì đã sang luyện
     từ, và cả phần "nói về chính bé" thành vô dụng. */
  /* ⚠ "Bước một lần" là bước KHÔNG thuộc vòng luyện NÀO — kể cả vòng dễ. Bản đầu
     viết `!BUOC_LUYEN.has(...)`, mà từ 18-08 `tu` đã rời khỏi `BUOC_LUYEN`; thế là
     mọi bước `tu` bị coi là bước một lần và hàm này trả về CÙNG MỘT TỪ cho mọi
     lượt của buổi. Không có gì đỏ — cô vẫn nói, chỉ là nói mãi một chữ. */
  const motLan = ds2.filter((b) => !BUOC_LUYEN.has(b.loai) && !BUOC_DE.has(b.loai));
  if (motLan.length) return motLan[0];

  /* ── LƯỢT SỬA ĐỨNG TRƯỚC MỌI BƯỚC KHÁC ── (bác chốt 18-08)
     "Cần dạy học sinh nói rồi hướng dẫn học sinh sửa."
     Bé vừa nói trượt thì việc của lượt này là SỬA đúng câu ấy, không phải đi tiếp.
     Trước nay không có bước nào làm việc này: bé được 3 điểm thì `soDat` không
     tăng, nên kịch bản đứng yên và cô nhắc lại y nguyên câu cũ với y nguyên lời
     dặn — bé nghe lại lần hai chứ không được chỉ sai ở đâu. */
  const sua = buocSua(lichSu, datNguong);
  if (sua) return sua;

  /* Hết kịch bản thì QUAY VÒNG phần luyện, đừng dừng: buổi kết là việc của
     `tinhBuoi` (đạt đủ, hoặc hết giờ), không phải của việc hết bước. */
  const luyen = ds2.filter((b) => BUOC_LUYEN.has(b.loai) || BUOC_DE.has(b.loai));
  if (!luyen.length) return null;
  const thu = xenKe(luyen);
  return thu[soDat % thu.length];
}

/** Lượt gần nhất bé nói VÀ được chấm. Chưa nói câu nào thì `null`. */
export const luotBeCuoi = (lichSu = []) => [...lichSu].reverse()
  .find((x) => x?.vai === 'be' && x.diem != null) || null;

/**
 * BƯỚC SỬA — dựng lúc chạy, không nằm trong `kichban_noi.json`.
 *
 * Không sinh sẵn được, vì nó phụ thuộc vào CÂU BÉ VỪA NÓI: câu ấy chỉ có lúc chạy,
 * và mỗi bé mỗi khác. Câu tiếng Anh của bước là chính câu bé đang cố nói (`mau` —
 * `PhongNoi.jsx` giữ lại ngay trong lượt của bé), nên cô đọc lại đúng thứ bé cần
 * chứ không đọc một câu khác.
 *
 * ── VÌ SAO KHÔNG ĐẶT NGƯỠNG RIÊNG ──
 * Dùng luôn `datNguong` của cả phòng (6/10, `DAT` ở `chamnoi.js`). Đặt thêm một
 * ngưỡng "đáng sửa" thứ hai thì có hai con số nói về cùng một việc, và sớm muộn
 * lệch nhau: bé "đạt" mà vẫn bị sửa, hoặc "chưa đạt" mà không ai sửa.
 *
 * ── CÓ SỢ SỬA MÃI KHÔNG ──
 * Không. Bé trượt liên tiếp thì `tinhBuoi` bật `haDoKho`, và vòng luyện thu về
 * mấy bước TỪ — câu ngắn hẳn lại. Đó mới là đường lui, chứ không phải bỏ sửa.
 */
export const SUA_TOI_DA = 2;

export function buocSua(lichSu = [], datNguong = 6) {
  /* ⚠ CHỈ SỬA LƯỢT LUYỆN. Lượt bé đáp lời chào cũng được chấm, nên không lọc thì
     bé lí nhí chữ "hello" là bị cô bắt sửa ngay trước khi vào bài — trải buổi ra
     giấy mới thấy: lượt 2 của cả buổi đã là một lượt sửa. */
  const ds = luotLuyen(lichSu);
  const be = ds.at(-1);
  if (!be || be.diem >= datNguong || !be.mau) return null;

  /**
   * ⚠ SỬA HAI LẦN RỒI ĐI TIẾP — nếu không thì phòng này thành cái bẫy.
   *
   * `soDat` chỉ tăng khi bé ĐẠT, nên bé chưa nói được thì kịch bản đứng yên; mà
   * lượt sửa lại chen lên trước cả vòng luyện. Cộng hai thứ ấy: bé đuối bị hỏi
   * đúng một câu cho tới hết 20 phút, kể cả khi `haDoKho` đã bật — vì mấy bước TỪ
   * dễ hơn không bao giờ tới lượt. Đã trải ra giấy và thấy tận mắt: mười lượt liền
   * đều là "Hello!".
   *
   * Sửa hai lần là đủ cho một chỗ khó. Lần thứ ba mà vẫn chưa được thì cái bé cần
   * không phải nghe lại lần nữa, mà là một việc DỄ HƠN — đó đúng là việc của
   * `haDoKho`. Nên tới đó thì nhường đường cho vòng luyện.
   */
  let lien = 0;
  for (let i = ds.length - 1; i >= 0; i -= 1) {
    if (ds[i].mau !== be.mau || ds[i].diem >= datNguong) break;
    lien += 1;
  }
  if (lien > SUA_TOI_DA) return null;
  const thieu = (be.thieu || []).filter(Boolean);

  /* ── SỬA THEO ĐÚNG NỘI DUNG ĐANG HỎI ── (bác chốt 19-08-2026)
     "Khi học sinh nói chưa đúng → Giúp học sinh nói đúng theo nội dung đang hỏi."

     Bước sửa cũ chỉ đọc lại câu đích và nói "con thiếu chữ X". Ở bài tả tranh thì
     thế là hụt hẳn một nửa: bé sai vì không biết ĐÁP CÂU HỎI NÀO. Cô hỏi
     "How many kites can you see?" mà bé nói "I can see a kite." — không thiếu chữ
     nào cả, chỉ là đáp nhầm câu. Bảo "thiếu chữ three" thì bé càng rối.

     Nên bước sửa mang theo CÂU HỎI vừa rồi. Cô nhắc lại câu hỏi, chỉ ra chỗ lệch,
     rồi mới cho nói lại. */
  const truoc = [...lichSu].reverse().find((x) => x?.vai === 'may' && x.en);
  const hoiLai = (truoc?.buoc === 'goiY' || truoc?.buoc === 'taTranh') ? truoc.en : null;
  return {
    loai: 'sua',
    hoiLai,
    en: be.mau,
    vi: hoiLai
      ? `Cô đang hỏi “${hoiLai}”. Con nhìn tranh rồi nói lại cho đúng câu hỏi ấy nhé.`
      : (thieu.length
        ? `Con nói lại câu này nhé — lần vừa rồi chưa có chữ “${thieu[0]}”.`
        : 'Con nói lại câu này, chậm hơn một chút nhé.'),
  };
}

/**
 * XEN KẼ TỪ VÀ CÂU — hai từ rồi một câu, rồi lại thế.
 *
 * ── VÌ SAO KHÔNG ĐI THEO ĐÚNG THỨ TỰ KỊCH BẢN ──
 * Kịch bản xếp hết từ mới trước rồi mới tới câu, và xếp thế là đúng cho người đọc.
 * Nhưng bước được chọn theo `soDat` — SỐ LẦN BÉ NÓI ĐÚNG — mà buổi thì kết thúc ở
 * `DAT_LIEN_DE_XONG = 3`. Nên bé nói đúng hết chỉ đi tới vị trí thứ 3, trong khi
 * câu đầu tiên nằm ở vị trí thứ 4 (Unit 6 và Unit 9 đều có bốn từ mới).
 *
 * Kết quả: bé giỏi luyện xong ba TỪ LẺ rồi được khen "con nói được rồi" — chưa hề
 * nói một câu nào. Đúng cái buổi ấy đáng lẽ phải dạy mẫu câu.
 *
 * Đã dò tận nơi trên bản chạy: Unit 9 đi clocks → locks → mops rồi kết thúc.
 *
 * Chỗ này KHÔNG lộ ra ở đâu cả: không lỗi, không cảnh báo, và màn kết thì vẫn vui
 * vẻ chúc mừng. Chỉ trải từng lượt ra mới thấy.
 *
 * ── VÌ SAO KHÔNG NỚI `DAT_LIEN_DE_XONG` ──
 * Con số 3 là bác chốt ("thấy học sinh đã nắm bài thì khen ngợi và kết thúc").
 * Sửa thứ tự đi thì giữ nguyên được luật của bác, mà bé vẫn gặp câu. Nới con số
 * là đổi luật của bác để chữa lỗi của mình — sai chỗ.
 *
 * Hai từ trước một câu: bé cần nghe vài từ rồi mới ghép được, nhưng không cần
 * nghe hết cả bốn từ mới được ghép.
 */
export function xenKe(ds) {
  /* ── BẢN 18-08: XEN GIỮA "NHẮC LẠI" VÀ "TỰ NÓI" ──
     Từ rời không còn nằm trong vòng luyện thường nữa (xem `BUOC_LUYEN`), nên phép
     xen cũ — hai TỪ rồi một CÂU — không còn gì để xen. Cái cần xen nay là hai
     việc khác hẳn nhau về chất:

       · NHẮC LẠI (`mau` · `noiCa`)  — cô cho sẵn câu, bé nói theo;
       · TỰ NÓI  (`hoiBe` · `doiVai` · `thay`) — bé phải tự nghĩ ra nội dung.

     Đi hết vế nhắc lại rồi mới tới vế tự nói thì bé giỏi xong buổi ở lượt thứ ba,
     tức là chưa bao giờ phải tự đáp một câu nào — đúng cái lỗi cũ, chỉ dời lên
     một tầng. Nên cứ một bước nhắc lại thì một bước tự nói.

     HAI nhắc lại rồi MỘT tự nói, chứ không một-một. Buổi kết ở ba lần đạt, nên ba
     bước đầu là tất cả những gì bé giỏi được gặp — và ba bước ấy phải đúng ba nhịp
     của một buổi dạy: LÀM MẪU → NÓI LẠI → TỰ NÓI. Xen một-một thì nhịp thành
     làm mẫu → tự nói, bé bị hỏi khi chưa kịp nói câu ấy lần nào.

     `mau` đứng đầu là cố ý: bé phải NGHE mẫu trước khi bị hỏi. */
  const nhac = ds.filter((b) => b.loai === 'mau' || b.loai === 'noiCa' || b.loai === 'tu');
  const tuNoi = ds.filter((b) => !['mau', 'noiCa', 'tu'].includes(b.loai));
  if (!nhac.length || !tuNoi.length) return ds;
  const ra = [];
  let i = 0;
  let j = 0;
  while (ra.length < ds.length) {
    for (let k = 0; k < 2 && i < nhac.length; k += 1, i += 1) ra.push(nhac[i]);
    if (j < tuNoi.length) { ra.push(tuNoi[j]); j += 1; }
    if (i >= nhac.length && j >= tuNoi.length) break;
  }
  return ra;
}

/** Lời dặn cho lượt này khi ĐÃ CÓ kịch bản — câu tiếng Anh không để mô hình nghĩ. */
export function dongBuoc(buoc, hoSo, luotBe = null) {
  if (!buoc) return '';
  if (buoc.loai === 'ket' || buoc.loai === 'hoiThich') return '';
  const en = dienBuoc(buoc, hoSo);
  const d = [
    `THIS TURN: your English sentence MUST be exactly: "${en}"`,
    '  Copy it character for character. Do not rephrase, extend, or substitute.',
    '  This overrides the "never repeat yourself" rule: the script decides.',
    '  Your only job is the Vietnamese line: react to what the child just said',
    '  (praise a good try, gently fix a wrong one), then point at this sentence.',
    /* VIỆC CỦA BÉ Ở LƯỢT NÀY — thứ mô hình không suy ra được từ câu tiếng Anh.
       "What's your hobby?" xuất hiện ở HAI bước khác hẳn nhau: `hoiBe` (cô hỏi
       thật, bé đáp) và `doiVai` (bé hỏi, cô đáp). Cùng một câu, ngược hẳn vai.
       Không nói ra thì mô hình đoán, và đoán sai thì bé được dặn làm nhầm việc. */
    dongViecBe(buoc),
  ].filter(Boolean);

  /* ── CÁI BÉ VỪA NÓI, VÀ ĐIỂM ── (bác chốt 18-08)
     `goiGui` cố ý cắt bỏ điểm khi gửi lịch sử (nó chỉ gửi vai + chữ), nên trước
     nay mô hình KHÔNG hề biết bé nói được 9 điểm hay 2 điểm — nó chỉ thấy một
     dòng chữ mà bộ nhận dạng nghe ra. Thế nên lời khen lượt nào cũng như lượt
     nào, và không lượt nào chỉ ra chỗ sai. Đúng chỗ bác gọi là "như máy".
     Điểm và chữ THIẾU đi qua đường này, không qua lịch sử: lịch sử là lời nói,
     còn đây là lời dặn. */
  if (luotBe?.diem != null && luotBe.mau) {
    const t = [`  She was trying to say: "${luotBe.mau}"`,
      `  She actually said: "${luotBe.chu}" — scored ${luotBe.diem}/10.`];
    const thieu = [...(luotBe.thieu || []), ...(luotBe.thieuChucNang || [])].filter(Boolean);
    if (thieu.length) t.push(`  Words she left out: ${thieu.join(', ')}.`);
    d.push('WHAT THE CHILD JUST DID:', ...t);
  }
  /**
   * CHỖ KHÓ CỦA BƯỚC NÀY — thứ mô hình KHÔNG thể tự biết.
   *
   * Kịch bản viết tay ghi sẵn cái bẫy riêng của từng bài: Unit 6 là "màu đứng
   * TRƯỚC đồ vật" (ngược tiếng Việt), Unit 16 là "đáp phải nói cả I can see rồi
   * mới tới số, khác bài đếm ở cửa hàng". Đó là `misconceptions` của sách, không
   * suy ra được từ câu tiếng Anh.
   *
   * ⚠ Trước 14-08 dòng này KHÔNG được gửi đi. `buoc.vi` chỉ là đường lui trong
   * `goiPhongNoi.js` (`tra.vi || buoc.vi`), mà mô hình thì lượt nào cũng trả lời
   * lời Việt — nên đường lui không bao giờ tới lượt. Công viết tay nằm trong tệp
   * JSON, không ai đọc. Cũng chẳng có gì báo: lời Việt của mô hình vẫn trôi chảy,
   * chỉ là nó nói chung chung và bỏ qua đúng chỗ bé hay sai.
   */
  if (buoc.vi) {
    d.push(`  Your Vietnamese line MUST get this teaching point across: "${buoc.vi}"`,
      '  Say it in your own words, warmly — but do not drop the point.');
  }
  /* Ngữ cảnh SÁCH đặt ra cho mẫu câu này. Cố ý không nằm trong `buoc.vi`: mấy dòng
     ấy dùng chữ "bạn" theo nghĩa DANH TỪ ("đứng cạnh một bạn chưa quen"), mà
     `loiVietHopLe` thì cấm chữ "bạn" vì cô không được gọi bé là bạn. Ghép thẳng
     vào lời viết sẵn là lời viết sẵn tự nó trượt phép soi — cổng bắt được thật ở
     lớp 1 unit 1. Đưa sang đây thì mô hình kể lại bằng lời của nó, đúng đại từ. */
  if (buoc.dungDe) d.push(`  What this sentence is for: ${buoc.dungDe}`);
  if (buoc.cho && buoc.vaiCho) {
    d.push(`  The changeable slot here is "${buoc.cho}" — the book calls it: ${buoc.vaiCho}`);
  }
  if (buoc.tinhHuong) {
    d.push(`  The situation the book pictures: ${buoc.tinhHuong}`,
      '  Retell it in your own Vietnamese words — call yourself "cô", the child "con".');
  }
  /* Cái bẫy SÁCH khai cho đúng mẫu câu này (`misconceptions[].why`). Chỉ đi kèm
     bước `mau` — nói lượt nào cũng nói thì nó thành tiếng ồn và bé bỏ ngoài tai. */
  if (buoc.bay) {
    d.push(`  The book warns about this mistake — work it in: "${buoc.bay}"`);
  }
  return d.join('\n');
}

/**
 * VIỆC CỦA BÉ Ở LƯỢT NÀY, nói bằng tiếng Anh cho mô hình.
 *
 * Tách hẳn ra khỏi `buoc.vi` vì hai thứ khác nhau: `buoc.vi` là Ý PHẢI TRUYỀN ĐẠT
 * (viết bằng tiếng Việt, cho bé), còn đây là LUẬT CỦA LƯỢT (viết bằng tiếng Anh,
 * cho mô hình). Trộn vào nhau thì mô hình dịch nguyên luật ra cho bé nghe.
 */
function dongViecBe(buoc) {
  switch (buoc.loai) {
    case 'mau':
      return '  ROLE: you are DEMONSTRATING the whole exchange — both the question'
        + ' and the answer. She may just listen, or repeat after you; say which.';
    case 'noiCa':
      return '  ROLE: she repeats the WHOLE sentence after you, not just one word.';
    case 'hoiBe':
      return '  ROLE: you are ASKING her a real question. She must answer it herself'
        + ` with a full sentence${buoc.dapMau ? ` like "${buoc.dapMau}"` : ''}.`
        + ' Do NOT answer it for her.';
    case 'doiVai':
      return '  ROLE: roles swap — SHE asks this question, you will answer next turn.'
        + ' Tell her it is her turn to be the one asking.';
    case 'thay':
      return '  ROLE: same frame, but the sentence is now about HER, not about you.';
    case 'sua':
      return '  ROLE: this is a CORRECTION turn. Name the one thing that went wrong,'
        + ' say what was already good, then have her try the same sentence again.'
        + ' Do not move on to new material.';
    case 'tu':
      return '  ROLE: one bare word — she is struggling, so keep it to that one word.';
    case 'taTranh':
      return '  ROLE: you are ASKING HER TO DESCRIBE THE PICTURE, in her own words.'
        + ' She can see it; you only have the written description. Do NOT read that'
        + ' description out — invite her, then wait. Anything she says that matches'
        + ' the picture counts.';
    case 'goiY':
      return '  ROLE: she got stuck, so you are HELPING with one small question about'
        + ` the picture${buoc.dapMau ? ` — the true answer is "${buoc.dapMau}"` : ''}.`
        + ' Ask it, let her answer, and tell her if the number or the thing is wrong.'
        + ' One question only. Never answer it for her.';
    case 'caDoan':
      return '  ROLE: she has described the pieces; now STRING THEM TOGETHER. Say the'
        + ' whole description once, then ask her to say all of it herself. This is'
        + ' what the whole session was for — do not cut it short.';
    default:
      return '';
  }
}
