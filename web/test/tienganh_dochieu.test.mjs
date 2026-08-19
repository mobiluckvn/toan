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

const R = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const quyens = ['ta1', 'ta2', 'ta3']
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
    if (!k.cau?.length) hinhDang.push(`${k.id}: không câu hỏi nào`);
    if (!(k.need >= 2 && k.need <= (k.cau || []).length)) {
      hinhDang.push(`${k.id}: cần ${k.need}/${(k.cau || []).length} câu — vô lý`);
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
  const theoUnitSap = ds.filter((k) => k.phamVi === 'unit')
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
      const khuon = en.map((x) => `${(x.split(' ')[0] || '').toLowerCase()}|${x.split(' ').length}`);
      if (new Set(khuon).size !== khuon.length) {
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
    for (const d of (k.doan || [])) {
      const kh = `${(d.cau.split(' ')[0] || '').toLowerCase()}|${d.cau.split(' ').length}`;
      dem.set(kh, (dem.get(kh) || 0) + 1);
    }
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
    /* Câu hỏi đếm phải có ít nhất một cái — đó là chỗ bài tranh hơn hẳn bài chữ. */
    if (!(k.cau || []).some((c) => /mấy/.test(c.text || ''))) {
      tranhHong.push(`${k.id}: không có câu hỏi đếm nào`);
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
