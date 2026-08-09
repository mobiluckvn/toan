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
  const soTho = new Set(bai.map((b) => `DL:KSN3.B${String(b.so).padStart(2, '0')}`));
  const lechBang = Object.keys(gan).filter((k) => !soTho.has(k));
  t('bảng đường lùi không trỏ từ bài lớp 3 không có thật', lechBang.length === 0);
  in5(lechBang);
  console.log(`   ${bai.length} bài · ${bai.reduce((a, b) => a + (b.cau || []).length, 0)} câu`
    + ` · ${bai.reduce((a, b) => a + (b.sauBai || []).length, 0)} dòng ôn tập/ải/đáp án`);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
