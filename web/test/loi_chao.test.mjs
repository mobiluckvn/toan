/**
 * CỔNG LỜI CHÀO MỞ BÀI — dòng ĐẦU TIÊN bé đọc khi mở một bài.
 * chạy: node test/loi_chao.test.mjs
 *
 * Bác đọc mở bài phần chuyển động mà không hiểu gì, và soi ra thì màn mở của ba
 * quyển đọc chậm đang in nguyên MỤC TIÊU GIÁO ÁN: dài, ba bốn câu, đầy chữ nghề,
 * lại nói sẵn cách làm. Bé đọc là muốn bỏ.
 *
 * Nay lời chào viết tay ở `data/loi_chao.json`. Cổng này canh ba thứ, và cả ba đều
 * là thứ đã sai thật chứ không phải phòng xa:
 *
 *   1. NGẮN — dài quá thì bé không đọc hết trước khi chán;
 *   2. KHÔNG CHỮ NGHỀ — "rút về đơn vị", "đại lượng", ký hiệu S · t · v;
 *   3. ĐỦ BÀI — thiếu bài nào là bài ấy âm thầm rơi về mục tiêu giáo án, mà nhìn
 *      màn hình thì chẳng có gì báo.
 *
 * KHÔNG canh "có lộ cách làm không" — máy không khẳng định được điều ấy. Chỗ đó
 * dựa vào luật ghi trong `data/loi_chao.json` và mắt người soi.
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
const D = new URL('../public/content/', import.meta.url).pathname;

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (ds) => ds.slice(0, 5).forEach((d) => console.log('     ', d));

const raw = JSON.parse(readFileSync(join(G, 'data/loi_chao.json'), 'utf8'));
const loiChao = Object.fromEntries(
  Object.entries(raw).filter(([k]) => !k.startsWith('_')));

/* Ba quyển đọc chậm — quyển lớp 5 có lời chào riêng từ khi soạn, không đi qua đây. */
const QUYEN = ['lop2', 'lop3', 'lop4'];
const bai = [];
for (const q of QUYEN) {
  const dir = join(D, q);
  if (!existsSync(dir)) continue;
  for (const f of readdirSync(dir).filter((x) => x.startsWith('DL_'))) {
    bai.push({ q, ...JSON.parse(readFileSync(join(dir, f), 'utf8')) });
  }
}
t(`đọc được bài của ba quyển (${bai.length})`, bai.length >= 100);

/* ── 1 · ĐỦ BÀI ── */
const thieu = bai.filter((b) => !loiChao[b.id]);
t(`bài nào cũng có lời chào (thiếu ${thieu.length})`, thieu.length === 0);
in5(thieu.map((b) => `${b.id} · ${b.title}`));

const thua = Object.keys(loiChao).filter((k) => !bai.some((b) => b.id === k));
t(`không có lời chào cho bài không tồn tại (thừa ${thua.length})`, thua.length === 0);
in5(thua);

/* ── 2 · NGẮN ──
   170 chữ là mốc đo được từ hiện trạng cũ: dưới mốc ấy thì lời đọc trôi, trên thì
   thành đoạn văn. Lớp 5 — quyển đọc dễ nhất — có 0/168 bài vượt mốc. */
const dai = bai.filter((b) => (b.objective?.kidText || '').length > 170);
t(`lời chào không quá 170 chữ (quá: ${dai.length})`, dai.length === 0);
in5(dai.map((b) => `${b.id}: ${b.objective.kidText.length} chữ`));

const nhieuCau = bai.filter((b) =>
  ((b.objective?.kidText || '').match(/[.!?]/g) || []).length > 2);
t(`lời chào không quá hai câu (quá: ${nhieuCau.length})`, nhieuCau.length === 0);
in5(nhieuCau.map((b) => `${b.id}: ${b.objective.kidText.slice(0, 70)}…`));

/* ── 3 · KHÔNG CHỮ NGHỀ ──
   Danh sách lấy từ chính những dòng đã sai: "Rút về đơn vị: từ 'đi t giờ được
   S km'…" là lời mở bài THẬT của bài 42 trước đợt này. */
const NGHE = /rút về đơn vị|đại lượng|tổng quát|công thức|biểu thức|quy về|tỉ lệ thức|vận dụng|xác định được|thành thạo|nắm chắc|thuộc luật|phân biệt rạch ròi/i;
const KY_HIEU = /(^|[\s(])[Svtk]\s*[=×:]|\ba\s*×\s*b\b/;
const nghe = bai.filter((b) => NGHE.test(b.objective?.kidText || ''));
t(`lời chào không dùng chữ nghề (dính: ${nghe.length})`, nghe.length === 0);
in5(nghe.map((b) => `${b.id}: ${b.objective.kidText.slice(0, 70)}…`));

const kh = bai.filter((b) => KY_HIEU.test(b.objective?.kidText || ''));
t(`lời chào không dùng ký hiệu (dính: ${kh.length})`, kh.length === 0);
in5(kh.map((b) => `${b.id}: ${b.objective.kidText.slice(0, 70)}…`));

/* ── 4 · MỜI GỌI ──
   Câu chào phải kết bằng một câu hỏi hoặc một lời rủ, nếu không nó lại thành lời
   thông báo — đúng thứ vừa bỏ đi. */
const moi = bai.filter((b) => {
  const s = (b.objective?.kidText || '').trim();
  return /[?]\s*$/.test(s) || /(nhé|nào|nhỉ|xem|không)[.!?]?\s*$/i.test(s);
});
t(`ít nhất 90% lời chào kết bằng câu hỏi hoặc lời rủ (${moi.length}/${bai.length})`,
  moi.length >= bai.length * 0.9);
in5(bai.filter((b) => !moi.includes(b))
  .map((b) => `${b.id}: …${(b.objective?.kidText || '').slice(-50)}`));

/* ── 5 · KHÔNG PHẢI BẢN SAO CỦA MỤC TIÊU ──
   Lỗi gốc: `kidText` vốn được gán bằng chính `text`. Nếu bộ dựng lại trượt về nếp
   ấy thì mọi phép kiểm trên vẫn xanh nếu mục tiêu tình cờ ngắn — nên canh thẳng. */
const saoChep = bai.filter((b) =>
  (b.objective?.kidText || '') === (b.objective?.text || ''));
t(`lời chào không phải bản sao của mục tiêu (sao chép: ${saoChep.length})`,
  saoChep.length === 0);
in5(saoChep.map((b) => b.id));

const dd = bai.map((b) => (b.objective?.kidText || '').length);
console.log(`\n   ${bai.length} bài · lời chào dài trung bình `
  + `${Math.round(dd.reduce((a, c) => a + c, 0) / dd.length)} chữ `
  + `(dài nhất ${Math.max(...dd)})`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
