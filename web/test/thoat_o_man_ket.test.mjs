/* ═══════════ THOÁT Ở MÀN KẾT THÌ VẪN PHẢI GHI KẾT QUẢ ═══════════
 * chạy: node test/thoat_o_man_ket.test.mjs
 *
 * ── LỖI ĐÃ XẢY RA THẬT (soi bằng tay trên bản chạy, 15-08-2026) ──
 *
 * Đi trọn bài `DL:KSN2.B01`, sát hạch 5/5, màn kết hiện "Đạt rồi! · con mở khoá
 * micro tiếp theo". Rồi bấm ⌂ Thoát ở góc trên — nút to nhất, quen tay nhất, và là
 * nút DUY NHẤT nằm cố định trên đầu suốt cả bài.
 *
 * Sổ tiến độ sau đó:
 *     micros['DL:KSN2.B01'] = { step: 15, steps: 16, at: … }
 *
 * Không `done`, không `pass`, không `best`. Tức là: không sao, không mở khoá bài
 * sau, học bạ không có gì, và lần sau mở lại `resumeSpot` thả con vào bước 15/16 —
 * ngay trước kỳ sát hạch — bắt làm lại cả năm câu vừa làm đúng hết.
 *
 * ── VÌ SAO 60+ CỔNG KHÔNG BẮT ĐƯỢC ──
 *
 * Lỗi ở CHỖ NỐI. `onExit` làm đúng phần việc của nó (đổi màn). `recordMicro` làm
 * đúng phần việc của nó (ghi khi được gọi). `FinaleCard` có nút gọi `onFinish` đàng
 * hoàng. Không tệp nào sai, nên không tệp nào có cổng để đỏ. Chỗ sai là một câu hỏi
 * KHÔNG AI SỞ HỮU: "đứng ở màn kết mà thoát thì tính là gì?"
 *
 * ── PHÉP DƯỚI ĐÂY SOI GÌ ──
 *
 * ① `recordMicro` và `saveSpot` cư xử đúng như mô tả trên (dựng lại đúng cảnh hỏng);
 * ② `LessonPlayer` KHÔNG nối thẳng `onExit` vào nút Thoát nữa, mà qua một chỗ có
 *    hỏi "đang ở màn kết không";
 * ③ `ManToan` có truyền `onGhiRoiThoat` xuống, và đường ấy dẫn tới `finishMicro`;
 * ④ hai đường ra khỏi màn kết dùng CHUNG một nguồn kết quả — không thì sau này sửa
 *    cách chấm ở một chỗ, chỗ kia lặng lẽ chấm kiểu cũ.
 */
import { readFileSync } from 'node:fs';
import { emptyProgress, recordMicro, saveSpot, resumeSpot } from '../src/mon/toan/lib/progress.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const ID = 'DL:KSN2.B01';

/* ── ① dựng lại đúng cảnh đã hỏng ── */
const doHoc = saveSpot(emptyProgress(), ID, 15, 16);
t('học tới bước 15/16 thì sổ nhớ chỗ dở', doHoc.micros[ID].step === 15);
t('và chỗ dở ấy CHƯA phải là đạt', !doHoc.micros[ID].pass);
t('mở lại sẽ bị thả vào bước 15 — ngay trước sát hạch',
  resumeSpot(doHoc, ID)?.step === 15);

const daGhi = recordMicro(doHoc, ID, { pass: true, right: 5, total: 5, mustOK: true });
t('ghi kết quả rồi thì có dấu đạt', daGhi.micros[ID].pass === true);
t('và điểm cao nhất là 5', daGhi.micros[ID].best === 5);
t('đạt rồi thì mở lại KHÔNG bị thả vào giữa bài', resumeSpot(daGhi, ID) === null);
/* Đây chính là chỗ mất mát: chỉ đổi màn thì sổ y nguyên như lúc học dở. */
t('(đối chứng) chỉ đổi màn, không ghi → sổ vẫn là "học dở, chưa đạt"',
  !doHoc.micros[ID].done && !doHoc.micros[ID].pass);

/* ── ② nút Thoát không được nối thẳng vào `onExit` ── */
const lp = readFileSync(
  new URL('../src/mon/toan/components/LessonPlayer.jsx', import.meta.url), 'utf8');
/* Tìm đúng thẻ nút mang nhãn "Thoát khỏi bài học" — đừng grep cả tệp, vì `onExit`
   còn được nhắc ở danh sách props và ở thân hàm xử lý, cả hai đều hợp lệ. */
const nut = lp.slice(lp.lastIndexOf('<button', lp.indexOf('aria-label="Thoát khỏi bài học"')),
                     lp.indexOf('>', lp.indexOf('aria-label="Thoát khỏi bài học"')));
t('(phép trên có tìm ra đúng thẻ nút)', nut.includes('aria-label="Thoát khỏi bài học"'));
t('nút Thoát KHÔNG gọi thẳng `onExit`', !/onClick=\{onExit\}/.test(nut));
t('nút Thoát đi qua chỗ có xét màn hiện tại', /onClick=\{thoat\}/.test(nut));

const thanThoat = lp.slice(lp.indexOf('const thoat ='), lp.indexOf('return (', lp.indexOf('const thoat =')));
t('chỗ ấy hỏi "có đang ở màn kết không"', /step\?\.type === 'finale'/.test(thanThoat));
t('ở màn kết thì ghi', /onGhiRoiThoat\(/.test(thanThoat));
t('không ở màn kết thì vẫn thoát như cũ', /onExit\?\.\(\)/.test(thanThoat));
t('`LessonPlayer` nhận `onGhiRoiThoat` qua props',
  /function LessonPlayer\(\{[^}]*onGhiRoiThoat/.test(lp));

/* ── ③ vỏ có nối dây xuống không ── */
const mt = readFileSync(
  new URL('../src/mon/toan/components/ManToan.jsx', import.meta.url), 'utf8');
t('`ManToan` truyền `onGhiRoiThoat` xuống bộ chơi', /onGhiRoiThoat=\{/.test(mt));
const day = mt.slice(mt.indexOf('onGhiRoiThoat={'), mt.indexOf('onGhiRoiThoat={') + 260);
t('và đường ấy dẫn tới `finishMicro`', /finishMicro\(/.test(day));
t('`finishMicro` là chỗ gọi `recordMicro`',
  /setProgress\(\(p\) => recordMicro\(p, microId, grade\)\)/.test(mt));

/* ── ④ hai đường ra dùng CHUNG một nguồn kết quả ──
   Nút "Micro tiếp theo ▶" và nút Thoát phải chấm y hệt nhau. Bản đầu chép
   `gradeMicro(...)` hai lần; sửa cách chấm ở một chỗ là chỗ kia lặng lẽ lệch. */
/* Dòng `import { gradeMicro }` không có dấu mở ngoặc nên không lọt vào phép đếm. */
const soLanCham = (lp.match(/gradeMicro\(/g) || []).length;
t(`chỉ có MỘT chỗ chấm bài trong bộ chơi (đang ${soLanCham})`, soLanCham === 1);
t('và cả hai đường ra đều gọi nguồn chung `ketQua()`',
  (lp.match(/\.\.\.ketQua\(\)/g) || []).length === 2);

console.log(`\n   ${pass} phép · cảnh hỏng: 5/5 rồi bấm Thoát → sổ chỉ có `
  + `step ${doHoc.micros[ID].step}/${doHoc.micros[ID].steps}, không có dấu đạt\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
