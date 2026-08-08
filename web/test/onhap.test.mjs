/**
 * Kiểm Ô NHẬP CÂU TRẢ LỜI — chạy: node test/onhap.test.mjs
 *
 * Yêu cầu của bố mẹ: con mở bài ra phải biết ngay phải điền gì.
 *   · trả lời bằng SỐ  → ô nhập số
 *   · trả lời bằng CHỮ → bấm chọn trong danh sách, không bắt con đoán gõ chữ gì
 * Nghĩa là KHÔNG còn ô viết văn tự do nào.
 *
 * Hai lỗi thật đã bắt được, nay khoá lại:
 *   1. `answerFields` coi "không có parts" là câu tự luận, nên 211 câu ĐÁP SỐ LÀ SỐ
 *      bị dựng thành ô viết văn: mời con "viết cách làm của mình vào đây", con gõ
 *      "Tận cùng là 2" rồi bị chấm SAI vì máy chỉ nhận đúng "2" — cổng mustPass
 *      chặn luôn bài sau. (kiểm 1 + 3)
 *   2. Ô có bộ chọn vẫn dùng phép so nới lỏng của ô gõ tay, nên NHIỀU nút cùng được
 *      chấm đúng: "8 - 24 - 24 - 8" và "8 - 24 - 8 - 24" cùng bộ số khác thứ tự;
 *      "6/9 và 6/8" và "2/3 và 3/4" bằng nhau về giá trị. (kiểm 2)
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { answerFields, checkAnswer } from '../src/lib/flow.js';

const D = new URL('../public/content/lessons/', import.meta.url).pathname;
const lessons = readdirSync(D).filter((f) => f.endsWith('.json'))
  .map((f) => JSON.parse(readFileSync(join(D, f), 'utf8')));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

t('đọc đủ 168 bài', lessons.length === 168);

function* everyItem(L) {
  for (const pool of Object.values(L.practice?.pools || {})) for (const it of pool) yield it;
  for (const s of L.lecture?.screens || []) for (const q of s.checks || s.questions || []) yield q;
  for (const q of L.check?.items || L.check?.questions || []) yield q;
}
const mid = (L) => L.id.replace('DL:KSN5Q1.', '');

/* ── 1. không còn ô viết văn tự do ── */
const VIET_VAN = ['essay', 'free', 'text'];
const vietVan = [], kinds = {};
let soO = 0;
for (const L of lessons) for (const it of everyItem(L)) {
  for (const f of answerFields(it) || []) {
    soO++; kinds[f.kind] = (kinds[f.kind] || 0) + 1;
    if (VIET_VAN.includes(f.kind)) vietVan.push(`${mid(L)} ${it.id} [${f.label}]`);
  }
}
t(`không ô nào bắt con viết văn tự do (${vietVan.length})`, vietVan.length === 0);
if (vietVan.length) console.log('    ', vietVan.slice(0, 10).join(' · '));

/* ── 2. mỗi ô CHỌN có đúng MỘT phương án được chấm đúng ──
   Không phải chuyện phong cách: nhận 2 nút thì con bấm bừa cũng qua, mà cổng
   mustPass lại dựa vào chính kết quả chấm này. */
const lech = [];
let soChon = 0;
for (const L of lessons) for (const it of everyItem(L)) {
  const fs = answerFields(it) || [];
  if (!fs.length) continue;
  // nền: mỗi ô điền đúng cái máy mong đợi, để chỉ còn ô đang xét là biến
  const nen = fs.map((f) => {
    const p = (it.answerKey?.parts || []).find((x) => (x.label || '').trim() === f.label);
    return p !== undefined ? String(p.value) : String(it.answerKey?.value ?? '');
  });
  for (const f of fs) {
    if (!f.options) continue;
    soChon++;
    const nhan = f.options.filter((o) => {
      const v = [...nen]; v[f.index] = o;
      const r = checkAnswer(it, v);
      return r?.parts?.[f.index]?.ok ?? r?.ok;
    });
    if (nhan.length !== 1) {
      lech.push(`${mid(L)} ${it.id} ô"${f.label}" nhận ${nhan.length}/${f.options.length}`);
    }
  }
}
t(`mỗi ô chọn có đúng một phương án đúng (${lech.length} lệch / ${soChon} ô)`, lech.length === 0);
if (lech.length) console.log('    ', lech.slice(0, 10).join(' · '));

/* ── 3. câu đáp số là SỐ phải được ô nhập SỐ ──
   Đây là phép bắt trực tiếp lỗi 211 câu: `answerKey.value` là số mà ô lại kind='essay'. */
const nhamO = [];
for (const L of lessons) for (const it of everyItem(L)) {
  const k = it.answerKey || {};
  if (typeof k.value !== 'number') continue;
  const fs = answerFields(it) || [];
  if (fs.length !== 1 || fs[0].kind !== 'number') {
    nhamO.push(`${mid(L)} ${it.id} value=${k.value} → ${fs.length} ô [${fs.map((f) => f.kind)}]`);
  }
}
t(`câu đáp số là số đều được ô nhập số (${nhamO.length})`, nhamO.length === 0);
if (nhamO.length) console.log('    ', nhamO.slice(0, 10).join(' · '));

/* ── 4. mọi ô đều nói cho con biết phải điền gì ── */
const camNin = [];
for (const L of lessons) for (const it of everyItem(L)) {
  for (const f of answerFields(it) || []) {
    if (!f.options && !String(f.placeholder || '').trim()) camNin.push(`${mid(L)} ${it.id} [${f.label}]`);
    if (!String(f.label || '').trim()) camNin.push(`${mid(L)} ${it.id} ô${f.index} thiếu nhãn`);
  }
}
t(`ô nào cũng có nhãn và lời nhắc dạng cần điền (${camNin.length})`, camNin.length === 0);
if (camNin.length) console.log('    ', camNin.slice(0, 10).join(' · '));

/* ── 5. không có hai nút TRÙNG NGHĨA mà một trong hai là ĐÁP ÁN ĐÚNG ──
   "2" và "2,0" là một số: nếu "2" là đáp án thì con bấm nút nào cũng thấy vô lý,
   mà máy chỉ nhận một nút. Phép kiểm 2 không bắt được vì lỗi nằm ở ĐỀ chứ không
   ở chấm điểm.
   Hai phương án SAI trùng nghĩa nhau thì hợp lệ, và đôi khi là cả ý đồ ra đề:
   "Số nào KHÔNG bằng 7,3?" với 7,30 · 7,300 · 7,03 — hai cái đầu bằng nhau chính
   là để con nhận ra chỉ 7,03 mới khác. */
const chuan = (s) => String(s).toLowerCase().replace(/\s+/g, ' ').trim();
const soCua = (s) => {
  const t = chuan(s).replace(/\./g, '').replace(/,/g, '.');
  return /^-?\d+(\.\d+)?$/.test(t) ? Number(t) : NaN;
};
const trung = [];
for (const L of lessons) for (const it of everyItem(L)) {
  for (const f of answerFields(it) || []) {
    if (!f.options) continue;
    // nút nào là đáp án đúng của ô này
    const dung = it.format === 'mcq' ? String(it.answerKey?.choice ?? '')
      : it.format === 'tf' ? (it.answerKey?.value ? 'ĐÚNG' : 'SAI')
      : String((it.answerKey?.parts || []).find((p) => (p.label || '').trim() === f.label)?.value ?? '');
    const laDapAn = (o) => {
      const nо = soCua(o), nd = soCua(dung);
      return chuan(o) === chuan(dung)
        || (Number.isFinite(nо) && Number.isFinite(nd) && nо === nd)
        || chuan(dung).startsWith(chuan(o));   // đáp án có chú thích trong ngoặc
    };
    for (let i = 0; i < f.options.length; i++) for (let j = i + 1; j < f.options.length; j++) {
      const a = f.options[i], b = f.options[j];
      const na = soCua(a), nb = soCua(b);
      const trungNhau = chuan(a) === chuan(b) || (Number.isFinite(na) && Number.isFinite(nb) && na === nb);
      if (trungNhau && (laDapAn(a) || laDapAn(b))) {
        trung.push(`${mid(L)} ${it.id} ô"${f.label}": "${a}" ≡ "${b}" (một trong hai là đáp án)`);
      }
    }
  }
}
t(`không bộ chọn nào có hai nút trùng nghĩa (${trung.length})`, trung.length === 0);
if (trung.length) console.log('    ', trung.slice(0, 10).join(' · '));

console.log(`\n   ${soO} ô nhập · ${soChon} ô chọn · theo loại:`,
  Object.entries(kinds).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(' · '));
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
