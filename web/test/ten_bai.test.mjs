/**
 * CỔNG TÊN BÀI — tên hiện cho bé phải NGẮN, và phải KHỚP ở cả ba nơi.
 * chạy: node test/ten_bai.test.mjs
 *
 * Tên bài lớp 5 vốn dài tới 105 chữ và tự đọc trước cách làm ("Vòng bốn 2·3·7·8:
 * chia số thừa số cho 4 — đọc dư như máy định vị"). Nay rút ngắn bằng
 * `tools/ten_bai_lop5.py`, tên gốc dời sang `titleDay`.
 *
 * Hai thứ dễ hỏng mà không có gì báo, nên canh ở đây:
 *
 *   · TÊN NẰM BA NƠI — `data/lessons/`, bản dựng, và `index_micro.json`. Sửa sót
 *     một nơi thì kệ sách hiện tên này, màn học hiện tên kia, cùng một bài.
 *   · CHẠY LẠI CÔNG CỤ chồng tên ngắn lên chính nó thì `titleDay` mất tên gốc —
 *     mất hẳn, vì tệp gốc cũng đã bị ghi đè.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const D = new URL('../public/content/', import.meta.url).pathname;
const G = new URL('../../data/lessons/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (ds) => ds.slice(0, 5).forEach((d) => console.log('     ', d));

const DAI_NHAT = 60;

/* Bản DỰNG đã đi qua `tools/dinh_dang.py` nên tên bài ở đó là LaTeX
   (`$\frac{1}{n}$`), còn bản gốc vẫn là `1/n`. Đo độ dài trên chuỗi thô là đếm cả
   mã lệnh — một cái tên 47 chữ hoá ra "84 chữ" và cổng báo oan. Trải phẳng về đúng
   thứ BÉ THẤY TRÊN MÀN rồi mới đo, và cũng chính nhờ vậy mà so được gốc với dựng. */
/* `\frac{1}{n \times (n+1)}` phải trải thành `1/(n×(n+1))`, KHÔNG phải `1/n×(n+1)`:
   cặp ngoặc nằm sẵn trong cấu trúc `{…}` của LaTeX, bỏ nó đi là hai chuỗi cùng
   nghĩa hoá ra khác nhau và cổng báo oan một cái tên hoàn toàn đúng. */
const bocNeuGhep = (x) => (/[\s+\-−×:]/.test(x.trim()) && !/^\(.*\)$/.test(x.trim())
  ? `(${x.trim()})` : x.trim());
const vePhang = (s) => String(s ?? '')
  .replace(/\\{1,2}times/g, '×')
  .replace(/\\{1,2}div/g, ':')
  .replace(/\\{1,2}d?frac\s*\{([^{}]*(?:\([^()]*\))?[^{}]*)\}\s*\{([^{}]*(?:\([^()]*\))?[^{}]*)\}/g,
           (_, a, b) => `${bocNeuGhep(a)}/${bocNeuGhep(b)}`)
  .replace(/\$/g, '')
  .replace(/\s+/g, ' ')
  .trim();
/* So gốc với dựng thì bỏ luôn khoảng trắng: bộ chuyển tự đặt dấu cách quanh `\times`
   nên `1/(n×(n+1))` và `1/(n × (n + 1))` là MỘT tên, không phải hai. */
const soDuoc = (s) => vePhang(s).replace(/\s/g, '');

const dung = {};
for (const f of readdirSync(join(D, 'lessons')).filter((x) => x.startsWith('DL_'))) {
  const b = JSON.parse(readFileSync(join(D, 'lessons', f), 'utf8'));
  dung[b.id] = b;
}
const goc = {};
if (existsSync(G)) {
  for (const f of readdirSync(G).filter((x) => x.endsWith('.json'))) {
    const b = JSON.parse(readFileSync(join(G, f), 'utf8'));
    goc[b.id] = b;
  }
}
const dm = JSON.parse(readFileSync(join(D, 'index_micro.json'), 'utf8'));

t(`đọc được bài lớp 5 (${Object.keys(dung).length})`, Object.keys(dung).length > 160);

/* ── 1 · NGẮN ── */
const dai = Object.values(dung)
  .filter((b) => vePhang(b.title).length > DAI_NHAT)
  .map((b) => `${b.id}: ${vePhang(b.title).length} chữ`);
t(`tên bài không quá ${DAI_NHAT} chữ (quá: ${dai.length})`, dai.length === 0);
in5(dai);

/* ── 2 · KHÔNG TRÙNG ──
   Hai micro cùng tên thì trên kệ sách và thang chủ đề bố mẹ không phân biệt nổi. */
const theoTen = {};
for (const b of Object.values(dung)) (theoTen[vePhang(b.title)] ||= []).push(b.id);
const trung = Object.entries(theoTen).filter(([, v]) => v.length > 1)
  .map(([k, v]) => `"${k}" ← ${v.join(', ')}`);
t(`không hai bài nào trùng tên (${trung.length})`, trung.length === 0);
in5(trung);

/* ── 3 · BA NƠI KHỚP NHAU ── */
const lechDm = Object.values(dung)
  .filter((b) => dm[b.id.replace('DL:', 'DL_').replace(/\./g, '_')])
  .filter((b) => soDuoc(dm[b.id.replace('DL:', 'DL_').replace(/\./g, '_')].title) !== soDuoc(b.title))
  .map((b) => b.id);
t(`danh mục khớp bản dựng (lệch: ${lechDm.length})`, lechDm.length === 0);
in5(lechDm);

const lechGoc = Object.values(dung)
  .filter((b) => goc[b.id] && soDuoc(goc[b.id].title) !== soDuoc(b.title))
  .map((b) => b.id);
t(`bản gốc khớp bản dựng (lệch: ${lechGoc.length})`, lechGoc.length === 0);
in5(lechGoc);

/* ── 4 · TÊN ĐẦY ĐỦ KHÔNG BỊ MẤT ──
   `titleDay` phải là tên GỐC, tức phải DÀI hơn tên ngắn. Bằng nhau nghĩa là công
   cụ đã chạy chồng lên chính nó và tên gốc bay mất. */
const coDay = Object.values(dung).filter((b) => b.titleDay);
t(`có tên đầy đủ được giữ lại (${coDay.length})`, coDay.length > 100);
const hong = coDay.filter((b) => vePhang(b.titleDay).length <= vePhang(b.title).length)
  .map((b) => `${b.id}: đầy ${vePhang(b.titleDay).length} ≤ ngắn ${vePhang(b.title).length}`);
t(`tên đầy đủ luôn dài hơn tên ngắn (${hong.length})`, hong.length === 0);
in5(hong);

const n = Object.values(dung).map((b) => vePhang(b.title).length);
console.log(`\n   tên bài: dài nhất ${Math.max(...n)} chữ · trung bình `
  + `${Math.round(n.reduce((a, b) => a + b, 0) / n.length)} chữ`
  + ` · ${coDay.length} bài giữ tên đầy đủ`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
