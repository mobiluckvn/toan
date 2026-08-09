/**
 * LỚP 3 — đường lùi về lớp 2 có trỏ đúng chỗ không.
 * chạy: node test/lop3.test.mjs
 *
 * Bảng `data/lop3_gan_lop2.json` là đường LÙI: học lớp 3 mà đuối thì quay về luyện
 * lại bài lớp 2 cùng chủ đề. Trỏ sai còn tệ hơn không trỏ — bé bấm vào rồi lạc sang
 * một bài chẳng liên quan, mất niềm tin vào chính cái nút ấy.
 *
 * Ba điều máy khẳng định được: bài lớp 2 được trỏ tới phải CÓ THẬT; mọi bài lớp 3
 * đều phải có một dòng trong bảng (kể cả dòng nói "không có bài tương ứng" — im lặng
 * bỏ trống thì không phân biệt được "chưa làm" với "đã xét và kết luận là không có");
 * và căn cứ phải là một trong ba giá trị đã khai.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const BANG = join(G, 'data/lop3_gan_lop2.json');
t('bảng đường lùi có thật', existsSync(BANG));
const b = JSON.parse(readFileSync(BANG, 'utf8'));
const gan = b.gan || {};

/* bài lớp 2 được trỏ tới phải có tệp thật */
const coL2 = new Set(readdirSync(join(G, 'data/lop2'))
  .filter((f) => f.startsWith('DL_KSN2_'))
  .map((f) => f.replace('.json', '').replace('DL_KSN2_', 'DL:KSN2.')));
const lac = [];
for (const [ma, v] of Object.entries(gan)) {
  for (const ve of v.ve || []) if (!coL2.has(ve)) lac.push(`${ma} → ${ve} (không có bài này)`);
}
t(`mọi đích đến đều là bài lớp 2 CÓ THẬT (${coL2.size} bài)`, lac.length === 0);
in5(lac);

/* đủ 34 bài lớp 3, không sót dòng nào */
const thieu = [];
for (let i = 1; i <= 34; i += 1) {
  const ma = `DL:KSN3.B${String(i).padStart(2, '0')}`;
  if (!gan[ma]) thieu.push(ma);
}
t(`đủ 34 bài lớp 3 trong bảng (${Object.keys(gan).length})`, thieu.length === 0);
in5(thieu);

/* căn cứ phải nằm trong ba giá trị đã khai ở `_canCu` */
const hopLe = new Set(Object.keys(b._canCu || {}));
const sai = Object.entries(gan).filter(([, v]) => !hopLe.has(v.canCu)).map(([k]) => k);
t(`căn cứ nào cũng được khai nghĩa (${[...hopLe].join(' · ')})`, sai.length === 0);
in5(sai);

/* dòng "khong" phải RỖNG đích đến — khai không có mà vẫn trỏ đi đâu đó là mâu thuẫn */
const mauThuan = Object.entries(gan)
  .filter(([, v]) => v.canCu === 'khong' && (v.ve || []).length > 0).map(([k]) => k);
t('dòng "không có bài tương ứng" thì không trỏ đi đâu cả', mauThuan.length === 0);
in5(mauThuan);

const theoCanCu = Object.values(gan).reduce((a, v) => {
  a[v.canCu] = (a[v.canCu] || 0) + 1; return a;
}, {});
console.log('   căn cứ:', Object.entries(theoCanCu).map(([k, v]) => `${k} ${v}`).join(' · '));

/* ── bản trích thô: mốc bất biến, mất chữ ở đây thì mọi bước sau đều thiếu ── */
const THO = join(G, 'data/lop3_tho.json');
let soTho = new Set();          /* mã 34 bài có thật — mọi đích đến đều phải nằm trong đây */
if (existsSync(THO)) {
  const d = JSON.parse(readFileSync(THO, 'utf8'));
  const bai = d.bai || [];
  t(`trích đủ 34 bài (${bai.length})`, bai.length === 34);
  const MUC = ['mucTieu', 'chuyenMoBai', 'khamPha', 'viDuMau',
               'suKemNham', 'luyenTap', 'quiz', 'gocBoMe'];
  const thieuMuc = bai.filter((b) => MUC.some((m) => !b.muc?.[m])).map((b) => b.so);
  t('bài nào cũng đủ 8 mục ①…⑧', thieuMuc.length === 0);
  in5(thieuMuc);
  /* Mỗi bài 5 câu quiz — sách nói vậy, và nhiệt kế cũng 5 mức. Lệch là mẫu tách
     câu bỏ sót: lớp 2 từng mất 165 câu quiz vì mẫu chỉ nhận dấu chấm. */
  const saiQuiz = bai.filter((b) => (b.cau || []).filter((c) => c.phan === 'quiz').length !== 5)
    .map((b) => `B${b.so}`);
  t('bài nào cũng đúng 5 câu quiz', saiQuiz.length === 0);
  in5(saiQuiz);
  /* `hatMam` là đường lùi về lớp 2 — thiếu là mất luôn lý do tồn tại của bảng gán */
  const khongHatMam = bai.filter((b) => !b.hatMam).map((b) => `B${b.so}`);
  t('bài nào cũng có HẠT MẦM NĂM NGOÁI', khongHatMam.length === 0);
  in5(khongHatMam);
  /* mã bài trong bảng đường lùi phải khớp số bài có thật trong bản trích */
  soTho = new Set(bai.map((b) => `DL:KSN3.B${String(b.so).padStart(2, '0')}`));
  const lechBang = Object.keys(gan).filter((k) => !soTho.has(k));
  t('bảng đường lùi không trỏ từ bài lớp 3 không có thật', lechBang.length === 0);
  in5(lechBang);
  console.log(`   ${bai.length} bài · ${bai.reduce((a, b) => a + (b.cau || []).length, 0)} câu`
    + ` · ${bai.reduce((a, b) => a + (b.sauBai || []).length, 0)} dòng ôn tập/ải/đáp án`);
}

/* ── đáp án: phải khớp 1:1 với câu hỏi ──
   Lớp 2 từng có 60 lời giải gắn SAI CÂU vì đáp án ôn tập cũng đánh C1, C2… và
   ghi đè lên đáp án bài (bẫy 6). Kiểu hỏng ấy không làm app vỡ, không làm số
   liệu lệch — chỉ làm bé đọc lời giải của một câu khác. Chỉ đếm khớp mới bắt được. */
const DA = join(G, 'data/lop3_dapan.json');
if (existsSync(THO) && existsSync(DA)) {
  const tho = JSON.parse(readFileSync(THO, 'utf8')).bai || [];
  const da = JSON.parse(readFileSync(DA, 'utf8'));
  const lech = [];
  for (const b of tho) {
    const ma = `DL:KSN3.B${String(b.so).padStart(2, '0')}`;
    for (const [phan, key] of [['luyenTap', 'luyenTap'], ['quiz', 'quiz']]) {
      const hoi = (b.cau || []).filter((c) => c.phan === phan).map((c) => c.maSach);
      const dap = Object.keys(da[ma]?.[key] || {});
      const thieuDap = hoi.filter((x) => !dap.includes(x));
      const thuaDap = dap.filter((x) => !hoi.includes(x));
      if (thieuDap.length) lech.push(`${ma} ${phan}: thiếu đáp án ${thieuDap.join(',')}`);
      if (thuaDap.length) lech.push(`${ma} ${phan}: thừa đáp án ${thuaDap.join(',')} (đè từ ôn tập?)`);
    }
  }
  t('mọi câu hỏi đều có đáp án, và không đáp án nào thừa', lech.length === 0);
  in5(lech);
  const n = Object.values(da).reduce((a, v) =>
    a + Object.keys(v.luyenTap || {}).length + Object.keys(v.quiz || {}).length, 0);
  console.log(`   ${Object.keys(da).length} bài · ${n} đáp án`);
}

/* ── ôn tập & ải: mối nối "sai câu nào, ôn bài đó" ──
   Bộ tách đầu tiên nhận nhầm dòng BẢNG TỰ SOI thành câu hỏi — 5/8 ôn tập thừa 1-5
   câu. Cái thừa thì bộ đếm kêu; cái THIẾU đi kèm mới nguy: mối nối trượt là câu ấy
   mất đường về bài, hoặc tệ hơn, cả ôn tập tụt xuống "suy theo chương" và trỏ mỗi
   câu về cả 5 bài. Bé bấm vào rồi phải tự đoán học lại bài nào — đúng cái việc mà
   nút này sinh ra để khỏi phải làm. */
const ON = join(G, 'data/lop3_ontap.json');
if (existsSync(ON)) {
  const o = JSON.parse(readFileSync(ON, 'utf8'));
  const khoi = Object.values(o.khoi || {});
  const on = khoi.filter((v) => v.loai === 'onTap');
  t(`đủ 8 ôn tập và 3 ải (${on.length} · ${khoi.length - on.length})`,
    on.length === 8 && khoi.length - on.length === 3);

  const ten = (v) => `${v.loai === 'onTap' ? 'Ôn tập' : 'Ải'} ${v.so}`;
  /* số câu tách được phải bằng con số chính sách nêu ("Đạt 8/10", "Phá 6/8 vụ án") */
  const lechSo = khoi.filter((v) => (v.cau || []).length !== v.tong)
    .map((v) => `${ten(v)}: tách ${v.cau.length}, sách nói ${v.tong}`);
  t('số câu mỗi khối khớp con số sách nêu', lechSo.length === 0);
  in5(lechSo);

  /* số câu liền mạch 1…n — thủng một số là mẫu bỏ sót đúng câu ấy */
  const thung = khoi.filter((v) => (v.cau || []).some((c, i) => c.so !== i + 1))
    .map((v) => ten(v));
  t('số câu chạy liền mạch 1…n', thung.length === 0);
  in5(thung);

  /* dòng bảng tự soi lọt vào làm câu hỏi — kiểu hỏng gốc. Dấu nhận biết KHÔNG phải
     mũi tên: sách dùng → ngay trong đề ("Bán kính 4 cm → đường kính?"). Chỉ mũi tên
     TRỎ TỚI MỘT SỐ BÀI mới là mối nối. */
  const lot = khoi.flatMap((v) => (v.cau || []).concat(v.cauDeB || [])
    .filter((c) => /→[^→]*Bài\s*\d/.test(c.text))
    .map((c) => `${ten(v)} ${c.id}: ${c.text.slice(0, 60)}`));
  t('không dòng bảng tự soi nào lọt vào làm câu hỏi', lot.length === 0);
  in5(lot);

  /* sách chỉ đích danh từng câu — phải đọc được, không được tụt xuống suy theo chương */
  const phaiSuy = on.filter((v) => v.canCu !== 'sach').map((v) => ten(v));
  t('mọi ôn tập đều đọc được mối nối SÁCH CHỈ ĐÍCH DANH', phaiSuy.length === 0);
  in5(phaiSuy);

  /* mọi câu có đường về, và đích đến phải là bài lớp 3 CÓ THẬT */
  const hong = [];
  for (const v of on) {
    for (const c of v.cau || []) {
      const ve = v.veCau?.[c.id] || [];
      if (!ve.length) hong.push(`${ten(v)} ${c.id}: không trỏ về bài nào`);
      for (const x of ve) if (!soTho.has(x)) hong.push(`${ten(v)} ${c.id} → ${x} (không có bài này)`);
    }
  }
  t('mọi câu ôn tập đều trỏ về một bài lớp 3 có thật', hong.length === 0);
  in5(hong);

  /* đề B là thứ bé làm khi chưa đạt — thiếu câu nào là chỗ ấy không luyện lại được */
  const lechB = on.filter((v) => (v.cauDeB || []).length !== v.tong)
    .map((v) => `${ten(v)}: đề B ${v.cauDeB.length} câu, đề chính ${v.tong}`);
  t('đề B đủ câu như đề chính', lechB.length === 0);
  in5(lechB);

  console.log(`   ${on.length} ôn tập · ${khoi.length - on.length} ải`
    + ` · ${khoi.reduce((a, v) => a + v.cau.length, 0)} câu`
    + ` · ${khoi.reduce((a, v) => a + v.cauDeB.length, 0)} câu đề B`);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
