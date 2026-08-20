/**
 * CỔNG · BÀI ĐỌC HIỂU NGẮN.
 * chạy: node test/tienganh_dochieu.test.mjs
 *
 * Bài đọc hiểu là chỗ ĐẦU TIÊN của cả môn bắt bé ĐỌC tiếng Anh. Mọi thứ trước đó
 * đều có tiếng hoặc có hình đỡ; ở đây chữ là chính. Nên hai thứ phải chắc:
 *
 *   1. MỌI CHỮ TRONG ĐOẠN ĐỀU LÀ CHỮ ĐÃ HỌC — tính tới đúng chương ấy, gộp cả lớp
 *      1 và lớp 2. Một chữ lạ trong đoạn văn thì bé đọc tới đó là dừng, và nó
 *      không có cách nào tự gỡ ra: không hình, không tiếng Việt, không ai giảng.
 *      Đây là phép kiểm bác dặn phải có.
 *
 *   2. CÂU HỎI PHẢI TRẢ LỜI ĐƯỢC BẰNG CHÍNH ĐOẠN VĂN. Đáp án "câu nào CÓ trong bài"
 *      phải thật sự có trong đoạn, và mồi nhử phải thật sự KHÔNG có — sai chiều nào
 *      thì câu hỏi cũng thành câu bẫy, và bé đọc đúng vẫn bị chấm sai.
 *
 * Cùng họ với `tienganh_bai.test.mjs` phép 2 ("mọi chữ trong câu sinh ra đều có
 * gốc"), nhưng chặt hơn một nấc: ở đó túi từ là CẢ QUYỂN, ở đây là tới chương này.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

/* Bản khai bức tranh — thứ ĐẺ RA ảnh, nên soi nó là soi đúng nguồn. Đọc ảnh để đếm
   diều thì phải nhận dạng hình, mà bản khai đã nói sẵn "3 × kite". */
/* ⚠ MỘT BẢN KHAI CHO MỖI QUYỂN. Bản đầu ghim cứng `tranh_lop3.json`, nên khi có
   lớp 4 thì cổng đem ĐOẠN VĂN LỚP 4 so với TRANH LỚP 3 — cùng số unit nên nó khớp
   được, và báo "5 vật mà đoạn có 7 câu" ở cả 21 bài. Sai hoàn toàn, mà nghe rất
   giống một lỗi nội dung thật. Đây đúng họ "cổng chỉ soi một quyển". */
const khaiTranh = (lop) => {
  try {
    return JSON.parse(readFileSync(
      new URL(`../../data/tienganh/tranh_lop${lop}.json`, import.meta.url), 'utf8'));
  } catch { return []; }
};

/* ══ CÂU NỐI — nói THÊM về vật của câu ngay trước ══ (thêm 20-08-2026)

   Ba phép kiểm dưới đây đều ngầm cho rằng MỖI CÂU NÊU MỘT VẬT: đếm câu là đếm
   vật, câu nào không nêu vật là câu tả thứ không có trên tranh, và hai câu cùng
   khuôn là đoạn văn lặp.

   Bức "Màu sắc" phá cả ba, mà phá ĐÚNG: nó tả bốn vật bằng tám câu —

       This is an apple. It's red.  I can see a leaf. It's green.
       That's a box.     It's brown. There's a square. It's blue.

   "It's red." không nêu vật nào, và bốn câu màu thì cùng một khuôn. Nhưng đó
   chính là khuôn unit 9 dạy (`What colour is it? - It's + [Colour].`) — bỏ chúng
   đi thì bức "Màu sắc" không nhắc tới màu nào.

   Nên định nghĩa hẹp, đúng một dạng: câu KHÔNG nêu vật nào của tranh, mang đúng
   khuôn "It's + [một màu ĐÃ HỌC].", và câu NGAY TRƯỚC có nêu vật. Lỏng hơn thế —
   ví dụ cho mọi câu không nêu vật đi qua — là mở cửa lại cho đúng thứ ba phép
   kiểm ấy sinh ra để bắt. */
/* Hình vẽ tay — cùng tệp mà màn hình và video đọc; cờ `nguoi` xem `_nguoi` trong đó. */
const hinhVe = (() => {
  try {
    return JSON.parse(readFileSync(
      new URL('../src/mon/tienganh/lib/hinh_ve.json', import.meta.url), 'utf8')).hinh;
  } catch { return {}; }
})();

const MAU_HOC = new Set(['black', 'blue', 'brown', 'green', 'orange', 'red',
  'white', 'yellow']);
const laCauNoi = (khai, cau, truoc) => {
  if (!khai) return false;
  const m = /^It's (\w+)\.$/.exec(String(cau || '').trim());
  if (!m || !MAU_HOC.has(m[1].toLowerCase())) return false;
  const neuVat = (c) => (khai.nhom || [])
    .some((n) => String(c || '').toLowerCase().includes(n.tu.toLowerCase()));
  return !neuVat(cau) && neuVat(truoc);
};

const R = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const quyens = ['ta1', 'ta2', 'ta3', 'ta4']
  .filter((q) => existsSync(join(R, 'web/public/content', q, 'dochieu.json')));
if (!quyens.length) {
  console.log('   ⏸ chưa quyển nào có bài đọc hiểu');
  console.log('\n0 PASS · 0 FAIL');
  process.exit(0);
}

const chu = (s) => String(s || '').toLowerCase().match(/[a-z']+/g) || [];

for (const q of quyens) {
  const lop = Number(q.slice(2));
  const ds = JSON.parse(readFileSync(join(R, 'web/public/content', q, 'dochieu.json'), 'utf8'));
  const bais = readdirSync(join(R, 'web/public/content', q))
    .filter((f) => /^DL_.*\.json$/.test(f)).sort()
    .map((f) => JSON.parse(readFileSync(join(R, 'web/public/content', q, f), 'utf8')));
  const chuongCua = Object.fromEntries(bais.map((b) => [b.so, b.chuong]));
  const soChuong = new Set(bais.map((b) => b.chuong)).size;

  /* Hai PHẠM VI, đếm riêng: mỗi chương một bài, và mỗi unit một bài — trừ những
     unit vốn câu quá mỏng, `sinh_dochieu_tienganh.py` in ra tên chúng khi dựng. */
  const theoChuong = ds.filter((k) => k.phamVi !== 'unit');
  const theoUnit = ds.filter((k) => k.phamVi === 'unit');
  t(`${q} · mỗi chương một bài đọc (${theoChuong.length}/${soChuong})`,
    theoChuong.length === soChuong);
  t(`${q} · bài đọc theo unit phủ gần hết quyển (${theoUnit.length}/${bais.length})`,
    theoUnit.length >= bais.length - 2);
  t(`${q} · đọc được danh sách và có bài để soi`, ds.length > 0 && bais.length > 0);

  /* Túi từ ĐÃ HỌC TỚI CHƯƠNG NÀY — dựng lại ở đây chứ không gọi bộ sinh: bộ sinh tự
     kiểm lấy mình thì cùng một lỗi nằm ở cả hai bên và không bên nào thấy. */
  const khoDen = (den) => {
    const kho = new Set();
    const nap = (s) => chu(s).forEach((w) => kho.add(w));
    for (let l = 1; l <= lop; l += 1) {
      const cn = JSON.parse(readFileSync(join(R, `data/tienganh/chuan_lop${l}.json`), 'utf8'));
      for (const u of cn.unit) {
        if (l === lop && (chuongCua[u.so] ?? 99) > den) continue;
        for (const x of u.tu) [x.tu, x.so_it, x.so_nhieu, x.dang_ing].forEach(nap);
        for (const m of u.mau_cau) {
          nap(String(m.cong_thuc || '').replace(/\[[^\]]*\]/g, ' '));
          nap(m.vi_du);
        }
      }
      for (const nhom of ['so_dem', 'mau', 'ten']) {
        for (const m of (cn.them?.[nhom]?.muc) || []) nap(typeof m === 'string' ? m : m.word);
      }
    }
    return kho;
  };

  const chuLa = [], hinhDang = [], hoiHong = [], amThieu = [];
  const soAm = JSON.parse(readFileSync(
    join(R, `web/public/content/tienganh/lop${lop}_am.json`), 'utf8'));
  const coClip = new Set((soAm.clip || []).map((c) => c.id));

  for (const k of ds) {
    const kho = khoDen(k.chapter);
    const doan = (k.doan || []).map((d) => d.cau);

    /* Bài theo CHƯƠNG gom câu của bốn unit nên luôn đủ 4–6 dòng. Bài theo UNIT chỉ
       có vốn câu một unit; ba dòng vẫn là một đoạn đọc, còn đòi đủ bốn thì ba unit
       mất hẳn bài. */
    /* Bài theo CHƯƠNG gom bốn unit, mà một lượt đối đáp ăn HAI dòng — sáu dòng chỉ
       đủ ba lượt, chưa đi hết chương đã hết chỗ. Nên trần của bài chương là 8. */
    const sanDong = k.phamVi === 'unit' ? 3 : 4;
    /* Bài TẢ TRANH: mỗi cặp hỏi–đáp trong bản mô tả thành HAI dòng, nên nó luôn
       dài hơn đoạn hội thoại thường. Bù lại bé có bức tranh đỡ — không phải giữ cả
       đoạn trong đầu, chỉ cần đối chiếu từng dòng với hình. */
    const tranDong = k.dang === 'tranh' ? 12 : (k.phamVi === 'unit' ? 8 : 10);
    if (doan.length < sanDong || doan.length > tranDong) {
      hinhDang.push(`${k.id}: đoạn ${doan.length} câu (cần ${sanDong}–${tranDong})`);
    }
    /* ⚠ BÀI TẢ TRANH KHÔNG CÓ CÂU HỎI, và đó là chủ ý. Bác chốt 19-08: "Rõ ràng
       mô tả tranh thì làm gì có câu hỏi mà nhét câu hỏi vô làm gì. Câu hỏi dùng cho
       cô giáo gợi ý học sinh để tả thôi." Bé đọc đoạn mô tả rồi nhìn tranh — đối
       chiếu được là xong. Câu hỏi chuyển hẳn sang phòng nói, làm công cụ của cô. */
    if (k.dang !== 'tranh') {
      if (!k.cau?.length) hinhDang.push(`${k.id}: không câu hỏi nào`);
      if (!(k.need >= 2 && k.need <= (k.cau || []).length)) {
        hinhDang.push(`${k.id}: cần ${k.need}/${(k.cau || []).length} câu — vô lý`);
      }
    } else {
      /* ⚠ ĐẢO LẠI 19-08 (lần hai). Lượt trước bác bảo "mô tả tranh thì làm gì có câu
         hỏi mà nhét câu hỏi vô làm gì", nên phép này đòi bài tranh KHÔNG có câu hỏi.
         Nay bác nói rõ hơn: "Thiếu phần câu hỏi sau khi đọc. Và đọc xong rồi thì
         phải trả lời câu hỏi." Hai điều không mâu thuẫn — lần ấy tôi nhét câu hỏi
         vào GIỮA đoạn mô tả, nay là ĐỌC XONG RỒI mới hỏi. */
      if (!k.cau?.length) hinhDang.push(`${k.id}: bài tả tranh mà không có câu hỏi nào`);
      if (!(k.cau || []).some((c) => c.loai === 'yChinh')) {
        hinhDang.push(`${k.id}: thiếu câu hỏi TỔNG QUAN`);
      }
      if (!(k.cau || []).some((c) => c.loai === 'chiTiet')) {
        hinhDang.push(`${k.id}: thiếu câu hỏi CHI TIẾT`);
      }
    }

    for (const d of (k.doan || [])) {
      for (const w of chu(d.cau)) {
        if (!kho.has(w)) chuLa.push(`${k.id}: “${d.cau}” — chữ lạ “${w}”`);
      }
      /* Câu tiếng Anh phải mở đầu bằng chữ HOA và đóng bằng dấu câu — dấu vết của
         một phép cắt hỏng thì lộ ra ở đây trước khi lộ ra với bé. */
      if (!/^[A-Z]/.test(d.cau)) hinhDang.push(`${k.id}: “${d.cau}” không mở đầu chữ hoa`);
      if (!/[.?!]$/.test(d.cau)) hinhDang.push(`${k.id}: “${d.cau}” không có dấu câu cuối`);
      if (/\/|\[|\]| - /.test(d.cau)) hinhDang.push(`${k.id}: “${d.cau}” còn dấu ghép câu`);
      if (!coClip.has(d.am)) amThieu.push(`${k.id}: dòng “${d.cau}” chưa có clip ${d.am}`);
    }

    for (const c of k.cau || []) {
      const dap = c.answerKey?.choice;
      if (!c.choices?.length || dap === undefined) {
        hoiHong.push(`${k.id}/${c.id}: thiếu lựa chọn hoặc đáp án`);
        continue;
      }
      if (!c.choices.includes(dap)) hoiHong.push(`${k.id}/${c.id}: đáp án không có trong nút`);
      if (new Set(c.choices).size !== c.choices.length) {
        hoiHong.push(`${k.id}/${c.id}: hai nút trùng chữ`);
      }
      if (c.am && !coClip.has(c.am)) amThieu.push(`${k.id}/${c.id}: chưa có clip ${c.am}`);
      /* Chữ lạ ở NÚT cũng là chữ lạ: bé phải đọc cả bốn nút mới chọn được.
         Chỉ soi nút TIẾNG ANH. Câu ý chính có nút là tên chương bằng tiếng Việt
         ("Cơ thể, sở thích, trường lớp"), và đem nó đi so với túi từ tiếng Anh thì
         mọi âm tiết đều "lạ" — cổng kêu 170 lỗi mà không lỗi nào có thật. Dấu nhận
         biết: chữ Việt có ký tự ngoài bảng ASCII. */
      /* Câu hỏi khai `tiengViet` thì lựa chọn của nó là TIẾNG VIỆT — đừng soi bằng
         túi từ tiếng Anh. Tiếng Việt KHÔNG DẤU ("Con voi") trông hệt tiếng Anh, nên
         phép dò dấu ở dòng dưới không đủ; phải để người khai nói ra. Cùng bẫy với
         "con quay" đã dính ở phòng nói. */
      if (c.tiengViet) continue;
      for (const x of c.choices) {
        if (!/[a-z]/i.test(x) || /[^\x20-\x7E’‘]/.test(x)) continue;
        for (const w of chu(x)) {
          if (!kho.has(w)) chuLa.push(`${k.id}/${c.id}: nút “${x}” — chữ lạ “${w}”`);
        }
      }
      /* ĐÚNG CHIỀU VÀ NGƯỢC CHIỀU — chỗ dễ sai nhất của dạng "câu nào có trong bài".
         Mồi mà lỡ nằm trong đoạn thì có HAI đáp án đúng, và bé đọc kỹ lại bị chấm sai. */
      if (c.text === 'Câu nào CÓ trong bài đọc?') {
        if (!doan.includes(dap)) hoiHong.push(`${k.id}/${c.id}: đáp án KHÔNG có trong đoạn`);
        for (const x of c.choices) {
          if (x !== dap && doan.includes(x)) {
            hoiHong.push(`${k.id}/${c.id}: mồi “${x}” LẠI CÓ trong đoạn`);
          }
        }
      }
      if (/có trong bài đọc không\?$/.test(c.text || '')) {
        const trong = (c.text.match(/“([^”]+)”/) || [])[1];
        if (doan.includes(trong)) hoiHong.push(`${k.id}/${c.id}: hỏi câu ĐANG CÓ mà đáp "Không"`);
        if (dap !== 'Không') hoiHong.push(`${k.id}/${c.id}: đáp án phải là "Không"`);
      }
    }
  }

  /* ══ BÀI ĐỌC PHẢI CÓ THÔNG TIN, KHÔNG PHẢI CHÀO HỎI ══ (bác bắt 19-08-2026)

     "Cả một chương bạn toàn có nói về mấy câu chào hỏi. […] Căn bản đoạn văn nó
     phải có ý nghĩa một chút thay vì chỉ chào hỏi linh tinh. Phần chào hỏi, luyện
     tập nên để ở phần Luyện nói. Đọc nên là một bài đọc ngắn có thông tin."

     Đoạn cũ mở bằng HAI dòng chào và đóng bằng một lời tạm biệt, trong khi cả đoạn
     chỉ dài 4–7 dòng — gần một nửa bài đọc không mang mẩu thông tin nào. Bé đọc
     xong không biết thêm điều gì về ai.

     Chào hỏi vẫn còn, nhưng đúng chỗ: PHÒNG LUYỆN NÓI và nhóm "Mở đầu" của BÀI
     VIẾT. Bài đọc thì không. */
  const XA_GIAO = /^(Hello|Hi|Bye|Goodbye|How are you|Fine, thank you)\b/i;
  const xaGiao = [];
  for (const k of ds) {
    for (const d of (k.doan || [])) {
      if (XA_GIAO.test(d.cau)) xaGiao.push(`${k.id}: “${d.cau}”`);
    }
  }
  t(`${q} · đoạn đọc không có dòng chào hỏi suông (${xaGiao.length})`, xaGiao.length === 0);
  in5(xaGiao);

  /* ══ ĐOẠN NGẮN Ở ĐẦU QUYỂN, DÀI DẦN VỀ CUỐI ══
     "Mấy bài đầu bạn có thể viết một đoạn ngắn thôi rồi tăng dần độ dài về cuối."
     Unit 0 bé mới có mười một từ; bắt đọc tám dòng thì tám dòng ấy chỉ có thể là
     tám biến thể của một câu. Đo bằng trung bình nửa đầu so với nửa sau — từng bài
     một thì nhiễu, vì có unit vốn nghèo mẫu câu. */
  /* ⚠ Phép này dành cho đoạn HỘI THOẠI, nơi độ dài do bộ dựng chọn. Bài TẢ TRANH
     thì độ dài = SỐ VẬT TRONG TRANH, và số vật do sách có bao nhiêu từ vẽ được
     quyết định — unit cuối không nhất thiết nhiều vật hơn unit đầu. Đòi nó dài dần
     là đòi một thứ bức tranh không hứa. Bài tranh có phép riêng ngay dưới. */
  const theoUnitSap = ds.filter((k) => k.phamVi === 'unit' && k.dang !== 'tranh')
    .sort((a, b) => a.unit - b.unit);
  if (theoUnitSap.length >= 8) {
    const giua = Math.floor(theoUnitSap.length / 2);
    const tb = (xs) => xs.reduce((a, k) => a + (k.doan?.length || 0), 0) / xs.length;
    const dau = tb(theoUnitSap.slice(0, giua));
    const cuoi = tb(theoUnitSap.slice(giua));
    t(`${q} · đoạn dài dần về cuối quyển (${dau.toFixed(1)} → ${cuoi.toFixed(1)} dòng)`,
      cuoi > dau);
  }

  /* ══ LỰA CHỌN PHẢI KHÁC NHAU ĐỦ ĐỂ BÉ CHỌN ĐƯỢC ══
     "Câu hỏi phải đảm bảo con dễ dàng trả lời chứ nhiều câu trả lời ý same same
     nhau rất khó cho con chọn câu trả lời đúng."

     Bản cũ CỐ Ý lấy mồi cùng khuôn (`It's a nose.` ↔ `It's a hair.`) để buộc bé đọc
     kỹ. Với bé lớp 3 mới tập đọc thì việc ấy không còn là đọc hiểu mà là dò chính
     tả — bé hiểu đúng vẫn chọn sai.

     ⚠ Nhưng nới sang chiều kia cũng hỏng, và đã hỏng thật ở bản sửa đầu tiên:
         It's a face. · It's a hair. · It's a hand. · What's this? ✓
     ba mồi giống hệt nhau, đáp án lẻ loi — bé chọn đúng bằng HÌNH DẠNG, không cần
     đọc một chữ. Nên luật là MỌI lựa chọn khác khuôn nhau, kể cả mồi với mồi. */
  const samSam = [];
  for (const k of ds) {
    for (const c of k.cau || []) {
      const en = (c.choices || []).filter((x) => /^[A-Za-z]/.test(x) && !/[^\x20-\x7E'’]/.test(x));
      if (en.length < 3) continue;              // câu Có/Không thì không áp
      const dang = (x) => `${(x.split(' ')[0] || '').toLowerCase()}|${x.split(' ').length}`;
      const khuon = en.map(dang);
      if (k.dang === 'tranh') {
        /* ⚠ BÀI TẢ TRANH HỎI KIỂU KHÁC, NÊN CANH KIỂU KHÁC.
           Câu "What number is it?" thì cả bốn lựa chọn PHẢI cùng khuôn — It's three
           · four · five · six — vì việc của bé là đọc CON SỐ, không phải phân biệt
           hình dạng câu. Đòi chúng khác khuôn nhau là đòi ngược.
           Cái thật sự cần chặn vẫn còn nguyên: ĐÁP ÁN không được là lựa chọn DUY
           NHẤT mang khuôn của nó — lúc ấy bé chọn đúng bằng mắt mà không cần đọc.
           Đó đúng là ca hỏng cũ: [It's a face. · It's a hair. · It's a hand. ·
           What's this? ✓] — ba mồi giống hệt, đáp án lẻ loi. */
        const dapKhuon = dang(c.answerKey?.choice || '');
        if (khuon.filter((x) => x === dapKhuon).length === 1 && en.length > 2) {
          samSam.push(`${k.id}/${c.id}: đáp án lẻ loi về hình dạng — [${en.join(' · ')}]`);
        }
      } else if (new Set(khuon).size !== khuon.length) {
        samSam.push(`${k.id}/${c.id}: [${en.join(' · ')}]`);
      }
    }
  }
  t(`${q} · các lựa chọn khác khuôn nhau, bé phân biệt được (${samSam.length} chỗ)`,
    samSam.length === 0);
  in5(samSam);

  /* ══ ĐỪNG LẶP ══ (bác bắt 19-08-2026)

     "sao nhiều câu lặp lại quá đi kiểu như Hello, I'm ben .... Bài đọc bạn nên dùng
     vốn câu tích luỹ từ lớp 1 đến bài đó của lớp 3 chứ không nhất thiết là trong
     bài đó của lớp 3."

     Lặp ở HAI TẦNG, và cổng cũ không đo tầng nào:

       · TRONG một đoạn — nguồn câu chỉ có mấy ví dụ của chính unit, mà bốn ví dụ
         thì chỉ khác nhau ở một chữ, nên đoạn thành bảng cửu chương;
       · GIỮA các bài — bài nào cũng mở bằng đúng "Hi, I'm Bill. / Hello. I'm Mai.",
         vì bộ dựng luôn lấy cái tên đầu danh sách. Bé đọc tới bài thứ ba là thuộc
         hai dòng ấy rồi lướt qua không đọc nữa.

     Cả hai đều KHÔNG sai một chữ nào, nên không có phép kiểm nào cũ bắt được. Phải
     đo thẳng cái người đọc thấy: bao nhiêu dòng cùng khuôn, và bao nhiêu bài mở
     đầu giống hệt nhau. */
  const lap = [];
  for (const k of ds) {
    const dem = new Map();
    const khaiK = k.dang === 'tranh' ? khaiTranh(lop).find((x) => x.unit === k.unit) : null;
    (k.doan || []).forEach((d, i) => {
      if (laCauNoi(khaiK, d.cau, k.doan[i - 1]?.cau)) return;
      const kh = `${(d.cau.split(' ')[0] || '').toLowerCase()}|${d.cau.split(' ').length}`;
      dem.set(kh, (dem.get(kh) || 0) + 1);
    });
    for (const [kh, n] of dem) {
      if (n > 2) lap.push(`${k.id}: ${n} dòng cùng khuôn “${kh}”`);
    }
  }
  t(`${q} · trong một đoạn không quá 2 dòng cùng khuôn (${lap.length} chỗ)`,
    lap.length === 0);
  in5(lap);

  const theoUnitDs = ds.filter((k) => k.phamVi === 'unit');
  if (theoUnitDs.length >= 5) {
    const dauTien = new Map();
    for (const k of theoUnitDs) {
      const d0 = k.doan?.[0]?.cau || '';
      dauTien.set(d0, (dauTien.get(d0) || 0) + 1);
    }
    const nhieuNhat = Math.max(...dauTien.values());
    /* Ngưỡng là MỘT PHẦN BA số bài. Không đòi mỗi bài một câu mở khác nhau — sách
       chỉ có ngần ấy lời chào — nhưng quá một phần ba thì bé nhận ra ngay. */
    const tran = Math.ceil(theoUnitDs.length / 3);
    t(`${q} · câu mở đầu không lặp quá ${tran}/${theoUnitDs.length} bài (đang ${nhieuNhat})`,
      nhieuNhat <= tran);
    if (nhieuNhat > tran) {
      in5([...dauTien].filter(([, n]) => n === nhieuNhat).map(([c, n]) => `${n} bài mở bằng “${c}”`));
    }
  }

  /* ══ ĐOẠN PHẢI LÀ MỘT CUỘC TRÒ CHUYỆN, KHÔNG PHẢI MẤY CÂU RỜI ══

     Bác đọc thử rồi bắt 18-08-2026: "Bài đọc phải là một đoạn văn hoặc đoạn hội
     thoại có ý nghĩa chứ không phải mấy câu rời rạc chẳng liên quan gì đến nhau."

     Đoạn cũ của lớp 3 unit 1 có bốn dòng, ba dòng là Lucy tự giới thiệu với ba
     người khác nhau:

         Hello. I'm Ben.
         Hello. I'm Lucy.
         Hello, Minh. I'm Lucy.      ← Lucy giới thiệu lần hai
         Hello, Ben. I'm Lucy.       ← lần ba

     Không một chữ nào sai: từ nào cũng đã học, câu nào cũng của sách. Cổng cũ soi
     TỪNG DÒNG nên dòng nào cũng qua. Chỉ đọc CẢ ĐOẠN mới thấy — nên phép kiểm này
     phải hỏi đúng những câu người đọc hỏi. */
  const XUNG = /\b(?:I'm|I am|My name's|My name is)\s+((?:Ms |Mr )?[A-Z][a-z]+)/g;
  const GOI = /\b(?:Hello|Hi|Bye|Goodbye),\s+((?:Ms |Mr )?[A-Z][a-z]+)/g;
  const roiRac = [];
  for (const k of ds) {
    /* ⚠ Bài TẢ TRANH không có người nói, và đúng là không nên có: đó là một đoạn
       MÔ TẢ, không phải hai bạn nói chuyện. Miễn phép này cho nó — nhưng miễn ĐÚNG
       một phép, mọi phép khác (chữ đã học · clip · lựa chọn khác khuôn) vẫn áp. */
    if (k.dang === 'tranh') continue;
    const doan = k.doan || [];
    if (!doan.every((d) => d.ai)) { roiRac.push(`${k.id}: có dòng không rõ ai nói`); continue; }
    const nguoi = [...new Set(doan.map((d) => d.ai))];
    if (nguoi.length !== 2) roiRac.push(`${k.id}: ${nguoi.length} người nói (phải đúng 2)`);
    for (const d of doan) {
      const ban = nguoi.find((x) => x !== d.ai);
      for (const m of d.cau.matchAll(XUNG)) {
        if (m[1] !== d.ai) roiRac.push(`${k.id}: ${d.ai} nói “${d.cau}” — xưng tên người khác`);
      }
      for (const m of d.cau.matchAll(GOI)) {
        if (m[1] !== ban) roiRac.push(`${k.id}: ${d.ai} chào “${m[1]}” — người không có trong đoạn`);
      }
    }
    /* Không ai được nói ba lượt liền: đoạn thành một bài độc thoại chứ không phải
       trò chuyện. Hai lượt liền thì được — kể xong rồi hỏi là chuyện thường. */
    for (let i = 2; i < doan.length; i += 1) {
      if (doan[i].ai === doan[i - 1].ai && doan[i].ai === doan[i - 2].ai) {
        roiRac.push(`${k.id}: ${doan[i].ai} nói ba lượt liền`);
      }
    }
  }
  t(`${q} · đoạn đọc là một cuộc trò chuyện nhất quán (${roiRac.length} chỗ)`,
    roiRac.length === 0);
  in5(roiRac);

  t(`${q} · mọi chữ trong đoạn và trong nút đều ĐÃ HỌC (${chuLa.length} chữ lạ)`,
    chuLa.length === 0);
  in5(chuLa);
  t(`${q} · đoạn và câu đúng hình dạng (${hinhDang.length} chỗ)`, hinhDang.length === 0);
  in5(hinhDang);
  t(`${q} · câu hỏi trả lời được bằng chính đoạn văn (${hoiHong.length} chỗ)`,
    hoiHong.length === 0);
  in5(hoiHong);
  t(`${q} · mọi dòng và mọi câu hỏi đều có clip tiếng (${amThieu.length} thiếu)`,
    amThieu.length === 0);
  in5(amThieu);

  /* ══ BÀI TẢ TRANH PHẢI CÓ TRANH, VÀ TRANH PHẢI CÓ THẬT ══ (bác chốt 19-08-2026)

     "Bài đọc sẽ là các dạng như một bức tranh: mô tả về bức tranh đó."

     Khai `dang: 'tranh'` mà thiếu tệp ảnh thì màn hình hiện một ô vỡ, còn câu hỏi
     thì hỏi "trong tranh có mấy con diều" — bé không có gì để đếm. Không lỗi đỏ ở
     đâu cả, vì `<img>` hỏng không làm React nổ. */
  const tranhHong = [];
  for (const k of ds.filter((x) => x.dang === 'tranh')) {
    if (!k.tranh) { tranhHong.push(`${k.id}: khai dạng tranh mà không có ảnh`); continue; }
    if (!existsSync(join(R, 'web/public/content', k.tranh))) {
      tranhHong.push(`${k.id}: thiếu tệp ${k.tranh}`);
    }
    /* ══ ĐOẠN PHẢI ĐỒNG BỘ VỚI TRANH ══ (bác bắt 19-08-2026)
       "Trên hình là 3 cái diều. Câu mô tả lại lại I can see a kite. Nội dung phải
       đồng bộ với Tranh bạn nhé."

       Đúng, và không có cách sửa CÂU cho khớp tranh: tới unit 0 sách chưa có khuôn
       nào nói "ba con diều" trong một câu kể — chỉ có "I can see a tiger." (một
       vật) và "I can see six." (trần một con số). Nên phải sửa TRANH.

       Phép đo: mỗi vật khai `so > 1` thì đoạn phải có một câu nói được số ấy; chưa
       có khuôn thì tranh không được vẽ nhiều. Máy không nhìn ảnh, nhưng bản khai
       tranh thì đọc được — và bản khai chính là thứ đẻ ra ảnh. */
    const khai = khaiTranh(lop).find((x) => x.unit === k.unit);
    if (khai) {
      for (const n of khai.nhom || []) {
        if (n.so > 1 && !(khai.doan || []).some((c) => /\b(two|three|four|five|six|seven|eight|nine|ten)\b/i.test(c))) {
          tranhHong.push(`${k.id}: tranh vẽ ${n.so} ${n.tu} mà đoạn không nói số nào`);
        }
      }
      /* Và ngược chiều: đoạn nhắc tới vật nào thì tranh phải CÓ vật ấy — trừ CÂU
         NỐI, thứ nói thêm về vật của câu ngay trước (xem `laCauNoi` đầu tệp). */
      (khai.doan || []).forEach((c, i) => {
        const co = (khai.nhom || []).some((n) => c.toLowerCase().includes(n.tu.toLowerCase()));
        if (!co && !laCauNoi(khai, c, khai.doan[i - 1])) {
          tranhHong.push(`${k.id}: đoạn tả “${c}” mà tranh không có vật ấy`);
        }
      });
      /* ══ CÂU "She's …ing." THÌ TRÊN TRANH PHẢI CÓ NGƯỜI ══ (lộ ra 19-08-2026)

         Bức "Ở vườn thú" viết *"He's counting."* mà trên tranh là cái bàn phím số
         🔢; unit 18 viết *"She's reading."* mà tranh là quyển sách 📖. Cả hai đều
         qua được phép kiểm cũ, vì phép kiểm cũ chỉ hỏi "từ này CÓ hình không" —
         có, nhưng hình là ĐỒ VẬT. Bé nhìn quyển sách thì bé nói "a book"; không ai
         nói được "She's reading" từ một quyển sách nằm trên kệ.

         Đây là loại lỗi cổng xanh không bắt được nếu không hỏi đúng câu hỏi, và
         chỉ lộ khi rút bức tranh ra nhìn — cùng họ với [[hình trong video phải
         khớp lời đọc]]. */
      const hinhCua = Object.fromEntries(
        bais.flatMap((b) => (b.hinhTu || []).map((h) => [h.tu, h])));
      /* Hình VẼ TAY thì không đoán được bằng mã emoji — hỏi thẳng cờ `nguoi` khai
         trong hinh_ve.json, cùng nguồn với bộ soạn (`soan_tranh_lop3.la_nguoi`). */
      const coNguoi = (h) => {
        if (h?.ve) return !!hinhVe[h.ve]?.nguoi;
        return [...String(h?.hinh || '')].some((ch) => {
          const m = ch.codePointAt(0);
          return (m >= 0x1F466 && m <= 0x1F478) || (m >= 0x1F481 && m <= 0x1F487)
            || (m >= 0x1F574 && m <= 0x1F57A) || (m >= 0x1F645 && m <= 0x1F64F)
            || (m >= 0x1F3C3 && m <= 0x1F3CC) || (m >= 0x1F6B4 && m <= 0x1F6B6)
            || (m >= 0x1F930 && m <= 0x1F93E) || (m >= 0x1F9CD && m <= 0x1F9DF);
        });
      };
      for (const c of khai.doan || []) {
        const m = /^(?:She|He)'s (\w+ing)\.$/.exec(c.trim());
        if (m && !coNguoi(hinhCua[m[1]])) {
          tranhHong.push(`${k.id}: đoạn nói “${c}” mà hình của “${m[1]}” là đồ vật, không có người`);
        }
      }
    }

    /* ══ CÂU HỎI HỎI BẰNG TIẾNG ANH, VÀ CHỈ BẰNG KHUÔN ĐÃ HỌC ══ (bác chốt 19-08)
       "phần câu hỏi và câu trả lời của bài đọc hãy dùng tiếng anh bạn ơi."

       Nhưng hỏi bằng một khuôn bé chưa gặp thì bài đọc hiểu hoá ra bài ĐOÁN ĐỀ —
       bé không hiểu người ta hỏi gì. Nên `text` của câu hỏi cũng phải đi qua đúng
       túi từ như đoạn văn. Phép soi chữ lạ ở khối trên đã lo phần LỰA CHỌN; đây
       lo phần ĐỀ BÀI. */
    const khoDe = khoDen(k.chapter);
    for (const c of k.cau || []) {
      if (!/[A-Za-z]/.test(c.text || '') || /[^\x20-\x7E’‘]/.test(c.text || '')) continue;
      for (const w of chu(c.text)) {
        if (!khoDe.has(w)) tranhHong.push(`${k.id}/${c.id}: đề hỏi “${c.text}” — chữ lạ “${w}”`);
      }
      /* Và phải có dòng phụ tiếng Việt: hỏi tiếng Anh mà bé chưa đọc nổi đề thì bé
         ngồi nhìn. Dòng phụ là chỗ bám, không phải câu hỏi — màn hình để nó nhỏ. */
      if (!c.phu) tranhHong.push(`${k.id}/${c.id}: đề tiếng Anh mà không có dòng phụ tiếng Việt`);
    }

    /* Đoạn mô tả phải là câu KỂ, không phải hỏi–đáp: bác bắt đúng chỗ này —
       "viết thành một đoạn không viết rời rạc như bạn đang làm". */
    for (const d of k.doan || []) {
      if (/\?/.test(d.cau)) tranhHong.push(`${k.id}: đoạn mô tả còn câu hỏi “${d.cau}”`);
    }
    if ((k.doan || []).length < 3) tranhHong.push(`${k.id}: đoạn mô tả quá ngắn`);
    /* Mỗi vật trong tranh phải có ĐÚNG một câu tả nó, và ngược lại. Thừa câu thì bé
       tìm không ra; thừa vật thì bé nhìn thấy thứ không ai tả. */
    if (khai) {
      const soVat = (khai.nhom || []).length;
      // Đếm câu NÊU VẬT, không đếm câu nối — bức dạy màu có hai câu cho một vật.
      const soCau = (k.doan || [])
        .filter((d, i) => !laCauNoi(khai, d.cau, k.doan[i - 1]?.cau)).length;
      if (soCau !== soVat) {
        tranhHong.push(`${k.id}: ${soVat} vật mà đoạn có ${soCau} câu nêu vật`);
      }
    }
  }
  t(`${q} · bài tả tranh có đủ tranh và câu hỏi về tranh (${tranhHong.length})`,
    tranhHong.length === 0);
  in5(tranhHong);

  const tongDong = ds.reduce((a, k) => a + (k.doan || []).length, 0);
  const tongCau = ds.reduce((a, k) => a + (k.cau || []).length, 0);
  console.log(`   ${q}: ${ds.length} bài đọc · ${tongDong} dòng · ${tongCau} câu hỏi`);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
