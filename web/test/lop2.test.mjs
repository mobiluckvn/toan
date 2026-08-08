/**
 * CỔNG LỚP 2 — dữ liệu đủ chưa, và lời văn đã đủ DỄ ĐỌC cho bé 7-8 tuổi chưa.
 * chạy: node test/lop2.test.mjs
 *
 * Khác hai cổng trước: ở đây có thêm phép đo NGÔN NGỮ. Bé lớp 2 đọc chậm, câu dài
 * là bé bỏ cuộc — mà lỗi ấy không bao giờ làm phần mềm vỡ, nên không có phép kiểm
 * thì chẳng ai phát hiện.
 *
 * Bản gốc của sách luôn được giữ trong `muc[*].goc` để đối chiếu: viết lại lời văn
 * là việc nhạy cảm, phải chứng minh được mình đổi gì.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const D = new URL('../public/content/lop2/', import.meta.url).pathname;
const tep = readdirSync(D).filter((f) => f.startsWith('DL_KSN2_'));
const bai = tep.map((f) => JSON.parse(readFileSync(join(D, f), 'utf8')))
  .sort((a, b) => a.so - b.so);
const idx = JSON.parse(readFileSync(join(D, 'index.json'), 'utf8'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const TOI_DA = 20;                       // số chữ tối đa một câu cho bé lớp 2
const CON_DOC = ['mucTieu', 'chuyenMoBai', 'khamPha', 'viDuMau', 'suKemNham', 'luyenTap', 'quiz'];
const cauCua = (s) => String(s).split(/(?<=[.!?…])\s+/).map((x) => x.trim()).filter(Boolean);

/* ── 1. đủ bài, đủ mục ── */
t('33 bài', bai.length === 33);
t('chỉ mục có đủ 33 bài', idx.length === 33);
t('8 chương', new Set(bai.map((b) => b.chuong)).size === 8);
t('bài nào cũng đủ 8 mục', bai.every((b) => Object.keys(b.muc).length === 8));
t('bài nào cũng có tên', bai.every((b) => String(b.ten || '').length > 3));
t('số bài liên tục 1–33',
  bai.every((b, k) => b.so === k + 1));

/* ── 2. câu luyện tập ── */
const cau = bai.flatMap((b) => b.cau.map((c) => [b, c]));
t(`có câu luyện tập (${cau.length})`, cau.length > 250);
t('mã câu không trùng trong một bài',
  bai.every((b) => new Set(b.cau.map((c) => c.id)).size === b.cau.length));
t('câu nào cũng có đề bài', cau.every(([, c]) => String(c.text || '').length > 5));
const thieuChua = cau.filter(([, c]) => !String(c.loiChua || '').trim());
t(`hầu hết câu có lời giải để bé tự chấm (${thieuChua.length} thiếu)`, thieuChua.length <= 3);

/* ── 3. DỄ ĐỌC — phép kiểm riêng của lớp 2 ──
   Chỉ soi phần CON đọc. "Góc bố mẹ" dài là bình thường, người lớn đọc. */
let tongCau = 0, quaDai = 0;
const viDu = [];
for (const b of bai) {
  for (const k of CON_DOC) {
    for (const d of b.muc[k]?.dong || []) {
      for (const c of cauCua(d)) {
        tongCau++;
        if (c.split(/\s+/).length > TOI_DA) {
          quaDai++;
          if (viDu.length < 4) viDu.push(`bài ${b.so}·${k}: ${c.slice(0, 70)}…`);
        }
      }
    }
  }
}
const tiLe = Math.round((quaDai / tongCau) * 100);
t(`câu quá ${TOI_DA} chữ dưới 8% (đang ${tiLe}%, ${quaDai}/${tongCau})`, tiLe < 8);
if (tiLe >= 8) console.log('    ', viDu.join(' · '));

/* Bản gốc phải còn nguyên để đối chiếu — viết lại lời văn mà xoá mất bản gốc thì
   sau này không ai kiểm được đã đổi gì, đúng hay sai. */
t('mọi mục con đọc đều giữ bản gốc của sách',
  bai.every((b) => CON_DOC.every((k) => Array.isArray(b.muc[k]?.goc))));

/* Viết lại phải LÀM DỄ HƠN, không được làm khó thêm. */
let xauDi = 0;
for (const b of bai) {
  for (const k of CON_DOC) {
    const g = (b.muc[k]?.goc || []).flatMap(cauCua).filter((c) => c.split(/\s+/).length > TOI_DA).length;
    const m = (b.muc[k]?.dong || []).flatMap(cauCua).filter((c) => c.split(/\s+/).length > TOI_DA).length;
    if (m > g) xauDi++;
  }
}
t(`không mục nào bị viết lại thành KHÓ HƠN (${xauDi})`, xauDi === 0);

/* Không được làm mất chữ: bản mới phải giữ ít nhất 90% lượng chữ của bản gốc
   (ngắt câu thì thêm dấu chấm, không mất nội dung). */
const chuGoc = bai.reduce((s, b) => s + CON_DOC.reduce((x, k) =>
  x + (b.muc[k]?.goc || []).join(' ').length, 0), 0);
const chuMoi = bai.reduce((s, b) => s + CON_DOC.reduce((x, k) =>
  x + (b.muc[k]?.dong || []).join(' ').length, 0), 0);
t(`viết lại không làm mất nội dung (${Math.round((chuMoi / chuGoc) * 100)}% chữ)`,
  chuMoi >= chuGoc * 0.9);


/* ── 5. hình trong bài ──
   Bẫy đã dính ở Quyển 2 lớp 5: chạy lại bộ dựng dữ liệu xoá sạch hình vừa gắn mà
   dữ liệu vẫn hợp lệ và bài vẫn chạy. Không có phép kiểm này thì mất hình im lặng. */
const soTay = JSON.parse(readFileSync(new URL('../../data/lop2_hinh_manifest.json', import.meta.url).pathname, 'utf8'));
const hinhTrongBai = bai.flatMap((b) =>
  Object.entries(b.muc).flatMap(([mk, m]) => (m.hinh || []).map((h) => [b, mk, m, h])));

t(`hình đã gắn vào bài (${hinhTrongBai.length})`,
  hinhTrongBai.length === Object.keys(soTay).length);
t('mã hình không trùng nhau',
  new Set(hinhTrongBai.map(([, , , h]) => h.id)).size === hinhTrongBai.length);
t('hình nào cũng neo vào một dòng có thật',
  hinhTrongBai.every(([, , m, h]) => h.sauDong >= 0 && h.sauDong < m.dong.length));
t('hình nào cũng có lời chú', hinhTrongBai.every(([, , , h]) => String(h.caption || '').length > 5));

const F = new URL('../public/content/figures/', import.meta.url).pathname;
const lechSha = hinhTrongBai.filter(([, , , h]) => {
  const p = join(F, h.file.replace('figures/', ''));
  if (!existsSync(p)) return true;
  return createHash('sha256').update(readFileSync(p)).digest('hex').slice(0, 16) !== h.sha256_16;
});
t(`ảnh có thật và đúng bản đã ghi sổ (${lechSha.length} lệch)`, lechSha.length === 0);

console.log(`\n   ${bai.length} bài · ${cau.length} câu · câu dài ${quaDai}/${tongCau} (${tiLe}%)`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
