/**
 * CỔNG BƯỚC 2+3 — dữ liệu Quyển 2 đã dùng được chưa.
 * chạy: node test/quyen2.test.mjs
 *
 * Chuyển thẳng các hàng rào đã cứu Quyển 1 sang đây, cộng thêm hàng rào riêng của
 * Quyển 2. Phép kiểm quan trọng nhất vẫn là cái cũ: CON LÀM ĐÚNG THÌ CÓ ĐƯỢC CÔNG
 * NHẬN KHÔNG — ở Quyển 1 đúng chỗ này hỏng mà không ai biết suốt nhiều tuần.
 *
 * Riêng Quyển 2 có một nguy cơ mới: đáp số phải RÚT TỪ VĂN XUÔI của lời chữa, mà
 * lời chữa chứa cả số trung gian của phép tính. Rút nhầm là con làm đúng bị báo
 * sai. Nên chỗ nào không chắc thì để tự luận, và ở đây kiểm rằng câu tự luận vẫn
 * có đủ lời chữa để con tự chấm.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { checkAnswer, answerFields } from '../src/lib/flow.js';

const D = new URL('../public/content/quyen2/', import.meta.url).pathname;
const tep = readdirSync(D).filter((f) => f.startsWith('DR_') && f.endsWith('.json'));
const khoi = tep.map((f) => JSON.parse(readFileSync(join(D, f), 'utf8')));
const hoSo = JSON.parse(readFileSync(join(D, 'ho_so_bay.json'), 'utf8'));
const the = JSON.parse(readFileSync(join(D, 'the_chien_thuat.json'), 'utf8'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const moiCau = khoi.flatMap((k) => k.cau.map((c) => [k, c]));

/* ── 1. đủ khối, đủ câu ── */
t('21 khối (14 vòng + 4 đề trộn + 3 thi thử)', khoi.length === 21);
t('14 vòng đấu', khoi.filter((k) => k.loai === 'vong').length === 14);
t(`314 câu (đang có ${moiCau.length})`, moiCau.length === 314);

/* ── 2. mã câu: có và không trùng ── */
const thieuMa = moiCau.filter(([, c]) => !String(c.id || '').trim());
t(`câu nào cũng có mã (${thieuMa.length})`, thieuMa.length === 0);
const trung = khoi.filter((k) => new Set(k.cau.map((c) => c.id)).size !== k.cau.length);
t(`mã câu không trùng trong một khối (${trung.length})`, trung.length === 0);

/* ── 3. câu nào cũng có đề và lời chữa ── */
t('câu nào cũng có đề bài', moiCau.every(([, c]) => String(c.text || '').trim().length > 8));
const thieuChua = moiCau.filter(([, c]) => String(c.loiChua || '').trim().length < 2);
t(`câu nào cũng có lời chữa của sách (${thieuChua.length})`, thieuChua.length === 0);

/* ── 4. MÁY CHẤM: làm đúng phải được công nhận, làm sai phải bị bác ──
   Đây là hàng rào đắt nhất của Quyển 1, giữ nguyên tinh thần. */
const mayCham = moiCau.filter(([, c]) => c.answerKey);
const khongNhan = [], nhanBua = [];
for (const [k, c] of mayCham) {
  const dung = String(c.answerKey.value);
  if (!checkAnswer(c, dung)?.ok) khongNhan.push(`${k.id} ${c.id} đợi "${dung}"`);
  /* Giá trị SAI THẬT. Thêm số 0 vào đuôi thập phân ("8,03" → "8,030000") là CÙNG
     một số — bộ kiểm tự bịa ra 8 ca "hỏng" không có thật. Cộng thêm 1 mới chắc sai. */
  const n = Number(dung.replace(/\./g, '').replace(',', '.'));
  const sai = Number.isFinite(n) ? String(n + 1) : `${dung}-sai`;
  if (checkAnswer(c, sai)?.ok) nhanBua.push(`${k.id} ${c.id}`);
}
t(`làm ĐÚNG được công nhận (${khongNhan.length}/${mayCham.length} hỏng)`, khongNhan.length === 0);
if (khongNhan.length) console.log('    ', khongNhan.slice(0, 5).join(' · '));
t(`làm SAI bị bác (${nhanBua.length})`, nhanBua.length === 0);
const rong = moiCau.filter(([, c]) => c.answerKey && !String(c.answerKey.value ?? '').trim());
t(`không đáp án nào rỗng (${rong.length})`, rong.length === 0);
t('câu máy chấm nào cũng dựng được ô trả lời',
  mayCham.every(([, c]) => answerFields(c).length > 0));

/* ── 5. TỰ LUẬN: phải có lời chữa đủ dài để con tự chấm theo barem ── */
const tuLuan = moiCau.filter(([, c]) => c.tuLuan);
/* Câu tự luận phải có lời chữa để con tự chấm. Ngưỡng thấp thôi: sách có những câu
   rất dễ mà lời chữa chỉ là "425." — ngắn nhưng ĐỦ để tự chấm, không phải thiếu. */
const chuaMong = tuLuan.filter(([, c]) => String(c.loiChua).trim().length < 2);
t(`câu tự luận có lời chữa để tự chấm (${chuaMong.length}/${tuLuan.length} thiếu)`,
  chuaMong.length === 0);
t('mỗi câu đúng một kiểu: máy chấm HOẶC tự luận',
  moiCau.every(([, c]) => !!c.answerKey !== !!c.tuLuan));

/* ── 6. bẫy: trục nối về Quyển 1 ── */
const microQ1 = new Set();
for (let b = 1; b <= 56; b++) for (const m of [1, 2, 3]) microQ1.add(`DL:KSN5Q1.B${b}.M${m}`);
t('168 hồ sơ bẫy', hoSo.length === 168);
t('mọi hồ sơ bẫy trỏ tới micro có thật', hoSo.every((h) => microQ1.has(h.micro)));
t('14 thẻ chiến thuật', the.length === 14);
const vong = khoi.filter((k) => k.loai === 'vong');
t('mỗi vòng đấu có 12 bẫy', vong.every((k) => k.bay.length === 12));
const mãHS = new Set(hoSo.map((h) => h.ma));
t('mã bẫy trong vòng đấu đều có hồ sơ',
  vong.every((k) => k.bay.every((b) => mãHS.has(b.ma))));

/* ── 7. luật mở khoá & thang điểm ── */
t('vòng đấu nào cũng gắn với một chương Quyển 1',
  vong.every((k) => k.chuongQ1 >= 1 && k.chuongQ1 <= 14));
t('14 vòng phủ đủ 14 chương, không trùng',
  new Set(vong.map((k) => k.chuongQ1)).size === 14);
/* Đề trộn và kỳ thi thử phủ NHIỀU chương → phải mở theo chương CAO NHẤT nó phủ.
   Thiếu chuongQ1 thì khối mở tự do: con mới xong chương 1 đã vào được kỳ chung kết
   phủ 14 chương. Lỗi này chỉ lộ khi chạy thử end-to-end, bộ kiểm cũ không thấy. */
t('khối nào cũng gắn chương mở khoá', khoi.every((k) => k.chuongQ1 >= 1 && k.chuongQ1 <= 14));
const theoPham = { 'DR:KSN5Q2.T01': 3, 'DR:KSN5Q2.T02': 6, 'DR:KSN5Q2.T03': 9,
                   'DR:KSN5Q2.T04': 13, 'DR:KSN5Q2.K01': 5, 'DR:KSN5Q2.K02': 11,
                   'DR:KSN5Q2.K03': 14 };
const saiPham = Object.entries(theoPham)
  .filter(([id, ch]) => khoi.find((k) => k.id === id)?.chuongQ1 !== ch);
t(`đề trộn & thi thử mở đúng theo phạm vi sách ghi (${saiPham.length} sai)`, saiPham.length === 0);
if (saiPham.length) console.log('    ', saiPham.map(([id, ch]) => `${id} cần ${ch}`).join(' · '));

t('khối nào cũng có số phút làm bài', khoi.every((k) => k.phut > 0));
t('ngưỡng đạt luôn nhỏ hơn thang điểm', khoi.every((k) => k.dat > 0 && k.dat <= k.thang));

/* ── 8. hai lỗi đã trả giá ở Quyển 1 ── */
const coMau = moiCau.filter(([, c]) => /#[0-9A-Fa-f]{6}/.test(JSON.stringify(c)));
t(`dữ liệu không chứa mã màu (${coMau.length})`, coMau.length === 0);
const DON_VI = /\?\s*(kg|g|cm²|m²|cm|m|viên|đồng|tuổi|trang|phút|giờ)(?![\p{L}])/u;
const dienTin = moiCau.filter(([, c]) => DON_VI.test(c.text) || /→[^?]*\?\s*\S*\?/.test(c.text));
t(`đề không viết tắt kiểu điện tín (${dienTin.length})`, dienTin.length === 0);

/* ── 9. sơ đồ chiến thuật (Bước 5) ──
   Vẽ bằng FigForge chứ không dùng 48 ảnh bitmap của sách: ảnh lệch bảng màu vừa
   đồng bộ theo icon, thiếu mất 49 chỗ, và sửa nội dung sau này không vẽ lại được. */
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
const HINH = new URL('../public/content/figures/', import.meta.url).pathname;
const soDo = khoi.flatMap((k) => (k.soDo || []).map((s) => [k, s]));
t(`có sơ đồ chiến thuật (${soDo.length})`, soDo.length >= 40);
const thieuTep = soDo.filter(([, s]) => !existsSync(join(HINH, s.file.split('/').pop())));
t(`sơ đồ nào cũng có tệp PNG thật (${thieuTep.length} thiếu)`, thieuTep.length === 0);
const shaLech = soDo.filter(([, s]) => {
  const p = join(HINH, s.file.split('/').pop());
  if (!existsSync(p)) return false;
  return createHash('sha256').update(readFileSync(p)).digest('hex').slice(0, 16) !== s.sha256_16;
});
t(`mã kiểm sơ đồ khớp PNG thật (${shaLech.length} lệch)`, shaLech.length === 0);
t('sơ đồ nào cũng có tiêu đề', soDo.every(([, s]) => String(s.caption || '').length > 8));
/* 14 bảng phiên tòa đã dựng thành giao diện bấm được ở màn 3 — vẽ thêm ảnh tĩnh
   là thừa và hai bên dễ lệch nhau. */
t('không vẽ lại bảng phiên tòa thành ảnh tĩnh',
  soDo.every(([, s]) => !s.caption.includes('BIÊN BẢN PHIÊN TÒA')));

console.log(`\n   ${khoi.length} khối · ${moiCau.length} câu · ${soDo.length} sơ đồ`
  + ` · máy chấm ${mayCham.length} · tự luận ${tuLuan.length}`
  + ` · ${hoSo.length} bẫy · ${the.length} thẻ`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
