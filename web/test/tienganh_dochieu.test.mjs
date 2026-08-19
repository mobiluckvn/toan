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
    const tranDong = k.phamVi === 'unit' ? 6 : 8;
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

  const tongDong = ds.reduce((a, k) => a + (k.doan || []).length, 0);
  const tongCau = ds.reduce((a, k) => a + (k.cau || []).length, 0);
  console.log(`   ${q}: ${ds.length} bài đọc · ${tongDong} dòng · ${tongCau} câu hỏi`);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
