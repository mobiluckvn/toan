/**
 * CỔNG GỢI Ý — thứ bé nhận được khi làm sai.
 * chạy: node test/goi_y.test.mjs
 *
 * Giao diện có sẵn cơ chế hai tầng (`hintState`): sai lần 1 hiện gợi ý 1, sai lần
 * 2 hiện gợi ý 2, sai lần 3 mở đáp án. Nhưng suốt một thời gian dài dữ liệu TRỐNG
 * ở lớp 2·3·4 — 984 câu, không một gợi ý nào — mà chẳng có gì báo, vì cơ chế vẫn
 * chạy đúng khi mảng rỗng.
 *
 * Điều đáng canh nhất KHÔNG phải "có gợi ý chưa", mà là **gợi ý có nói ra đáp án
 * không**. Đã suýt dính: bản đầu định suy gợi ý từ bước tính đầu tiên của lời
 * giải, và 329/720 câu có bước đầu chính là đáp án.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const D = new URL('../public/content/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (ds) => ds.slice(0, 5).forEach((d) => console.log('     ', d));

const QUYEN = [['lop2', 'lop2'], ['lop3', 'lop3'], ['lop4', 'lop4'], ['lop5', 'lessons']];
const cau = [];
for (const [q, thu] of QUYEN) {
  const dir = join(D, thu);
  if (!existsSync(dir)) continue;
  for (const f of readdirSync(dir).filter((x) => x.startsWith('DL_'))) {
    const b = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    for (const ds of Object.values(b.practice?.pools || {})) {
      for (const it of ds) cau.push({ q, bai: b.id, it });
    }
  }
}
t(`đọc được câu luyện tập (${cau.length})`, cau.length > 1500);

/* ── 1 · GỢI Ý KHÔNG ĐƯỢC NÓI RA ĐÁP ÁN ──
   Phép kiểm quan trọng nhất của tệp này. Hai chỗ phải cẩn thận, cả hai đều đã
   bắt oan ở bản đầu:

   · SO CHUỖI CON thì "420" chứa "20", "2,4 giờ" chứa "4 giờ", "11/12" chứa "11"
     — 36 báo động mà phần lớn vô can. Nay so theo BIÊN TỪ.
   · Số đã có SẴN TRONG ĐỀ thì gợi ý nhắc lại là chuyện bình thường ("Cắm mốc
     100" khi đề đã cho 100). Chỉ tính là lộ khi con số ấy KHÔNG có trong đề —
     tức gợi ý mang vào một con số mới, mà con số mới ấy đúng bằng đáp án. */
const dapAn = (it) => {
  const ak = it.answerKey || {};
  const v = [ak.value, ak.choice, ...(ak.parts || []).map((p) => p.value), ...(ak.values || [])];
  return v.filter((x) => x !== undefined && x !== null && String(x).trim())
    .map((x) => String(x).replace(/\s/g, '').toLowerCase())
    /* Đáp một chữ số thì gần như câu nào cũng chứa — so kiểu này chỉ gây báo oan,
       mà một chữ số đứng lẫn trong lời giảng cũng không phải là "nói ra đáp án". */
    .filter((x) => x.length >= 2);
};
/* Đề viết phân số bằng LaTeX (`$\frac{4}{5}$`) còn đáp án viết trần ("4/5"), nên
   so thẳng thì "đã có trong đề" luôn trượt và gợi ý bị báo oan. Quy cả hai về một
   dạng trước khi so. */
const vePhang = (s) => String(s)
  .replace(/\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, '$1/$2')
  .replace(/\\times/g, '×').replace(/\$/g, '');
const thoat = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const coRoi = (chuoi, tu) => new RegExp(`(^|[^\\d,.])${thoat(tu)}([^\\d,.]|$)`)
  .test(vePhang(chuoi).replace(/\s/g, ''));
const lo = [];
for (const { q, bai, it } of cau) {
  const hs = it.hints || [];
  if (!hs.length) continue;
  const de = vePhang(it.text || '').replace(/\s/g, '').toLowerCase();
  for (const a of dapAn(it)) {
    if (coRoi(de, a)) continue;                 // số đã có trong đề — không phải lộ
    if (hs.some((h) => coRoi(String(h).toLowerCase(), a))) {
      lo.push(`${q} ${bai} ${it.id}: gợi ý mang vào đáp "${a}"`);
    }
  }
}
t(`không gợi ý nào nói ra đáp án (lộ: ${lo.length})`, lo.length === 0);
in5(lo);

/* ── 2 · PHỦ ─── câu nào cũng phải được giúp khi làm sai */
/* ⚠ NGƯỠNG 90% CHÍNH LÀ THỨ ĐẺ RA MÓN NỢ 216 CÂU.
   Suốt năm đợt, bài video ra đời không gợi ý nào mà cổng vẫn xanh, vì tỉ lệ chung
   còn trên chín phần mười. Ngưỡng ấy che một lỗ đang lớn dần — mất một bài trọn vẹn
   cũng chỉ tụt hơn một phần trăm.
   Nay cả bốn quyển đều ĐỦ, nên siết lên trọn vẹn: thiếu một câu là đỏ. */
const thieu = cau.filter((c) => !(c.it.hints || []).length);
t(`MỌI câu đều có gợi ý (${cau.length - thieu.length}/${cau.length})`,
  thieu.length === 0);
in5(thieu.map((c) => `${c.q} ${c.bai} ${c.it.id}`));

/* ── 3 · NGẮN ─── gợi ý dài hơn đề bài thì bé đọc gợi ý còn lâu hơn tự làm */
const dai = cau.flatMap((c) => (c.it.hints || [])
  .filter((h) => String(h).length > 160)
  .map((h) => `${c.bai} ${c.it.id}: ${String(h).length} chữ`));
t(`gợi ý không quá 160 chữ (quá: ${dai.length})`, dai.length === 0);
in5(dai);

/* ── 4 · KHÔNG CẮT GIỮA CÔNG THỨC ─── dấu $ lẻ là bé thấy một ký tự lạ */
const le = cau.flatMap((c) => (c.it.hints || [])
  .filter((h) => (String(h).match(/\$/g) || []).length % 2)
  .map((h) => `${c.bai} ${c.it.id}: ${String(h).slice(0, 50)}`));
t(`không gợi ý nào có dấu $ lẻ (${le.length})`, le.length === 0);
in5(le);

/* ── 5 · GỢI Ý PHẢI RIÊNG THEO CÂU, KHÔNG DÙNG CHUNG THEO BÀI ──
   Bản đầu suy gợi ý từ câu chốt và bước giảng đầu, nên MỌI câu trong một bài
   nhận y hệt hai dòng. Nay 984 câu lớp 2·3·4 đã có gợi ý viết tay riêng
   (`data/goi_y_tay.json`). Phép kiểm này canh để đừng ai lặng lẽ tụt về bậc cũ:
   trong cùng một bài, hai câu khác nhau không được mang cùng một dòng gợi ý.

   Cố ý CHỈ canh tầng 1 — vài câu cùng bài có thể trùng nhau ở nước đi đầu
   ("Nhân đôi bán kính"), mà đó là trùng hợp lành, không phải dùng chung. */
/* ⚠ MÓN NỢ ĐANG CÓ, KHAI RA CHỨ KHÔNG GIẤU.
   24 bài mới của chương 3 tới 9 dùng VIDEO thay lời giảng, nên `mantra` và
   `statements` rỗng — bộ suy gợi ý không có gì để lấy, và 216 câu ra đời không một
   gợi ý nào. Cổng phủ đặt ngưỡng 90% nên nó xanh suốt, mãi tới khi số bài video đủ
   nhiều mới tụt xuống dưới ngưỡng mà lộ ra.

   Tạm thời `goi_y.py` lấy mục tiêu bài và dòng "Gợi ý 1" viết tay ở mục chỗ hay
   nhầm — có gợi ý còn hơn không, nhưng CẢ BÀI DÙNG CHUNG một dòng, đúng cái bậc cũ
   mà phép kiểm này sinh ra để chặn.

   Nên miễn trừ cho bài video, nhưng ĐẾM chúng ra và ghim con số lại: nợ chỉ được
   giảm, không được tăng. Trả nợ = viết gợi ý riêng từng câu vào `goi_y_tay.json`.  */
/* ── MÓN NỢ ĐÃ TRẢ XONG 15-08, GIỮ LẠI PHÉP ĐẾM ──
   Bộ suy gợi ý lấy từ `mantra` và bước giảng đầu, mà bài dùng video thì hai chỗ ấy
   cố ý rỗng. Nên 24 bài của chương 3 tới 9 từng ra đời với 216 câu không một gợi ý
   riêng nào. Cổng phủ đặt ngưỡng 90% nên nó xanh suốt năm đợt, mãi tới khi số bài
   video đủ nhiều mới tụt xuống dưới ngưỡng mà lộ.

   Nay 216 câu đã có gợi ý viết tay riêng, nợ về KHÔNG. Giữ lại phép đếm và ghim ở
   0 để nó không lặng lẽ mọc lại: thêm một bài video mà quên viết gợi ý là đỏ ngay,
   thay vì đợi tỉ lệ tụt xuống dưới ngưỡng. */
const NO_TOI_DA = 0;
const chungTheoBai = {};
for (const { bai, it } of cau) {
  const h1 = (it.hints || [])[0];
  if (!h1) continue;
  (chungTheoBai[bai] ??= new Map()).set(h1, (chungTheoBai[bai].get(h1) || 0) + 1);
}
const baiNo = Object.entries(chungTheoBai)
  .filter(([, m]) => [...m.values()].some((n) => n > 1)).map(([b]) => b);
t(`nợ gợi ý viết tay: ${baiNo.length} bài dùng chung gợi ý (ghim ${NO_TOI_DA}, chỉ được giảm)`,
  baiNo.length <= NO_TOI_DA);
in5(baiNo);

const theoBai = {};
for (const { q, bai, it } of cau) {
  const h1 = (it.hints || [])[0];
  if (!h1) continue;
  theoBai[bai] ??= { q, m: new Map() };
  const m = theoBai[bai].m;
  m.set(h1, (m.get(h1) || 0) + 1);
}
const dungChung = [];
for (const [bai, { q, m }] of Object.entries(theoBai)) {
  for (const [h, n] of m) {
    if (n > 1) dungChung.push(`${q} ${bai}: ${n} câu chung "${h.slice(0, 45)}…"`);
  }
}
t(`gợi ý tầng 1 riêng theo từng câu (dùng chung: ${dungChung.length})`, dungChung.length === 0);
in5(dungChung);

const theoQ = {};
for (const c of cau) {
  theoQ[c.q] ??= { tong: 0, co: 0 };
  theoQ[c.q].tong++;
  if ((c.it.hints || []).length) theoQ[c.q].co++;
}
console.log('\n   ' + Object.entries(theoQ)
  .map(([q, x]) => `${q}: ${x.co}/${x.tong}`).join(' · '));
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
