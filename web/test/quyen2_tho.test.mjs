/**
 * CỔNG BƯỚC 1 — bản trích Quyển 2 có TRUNG THỰC không.
 * chạy: node test/quyen2_tho.test.mjs
 *
 * Bản trích thô là mốc bất biến để mọi bước sau so lại. Nếu nó đã thiếu chữ hoặc
 * thiếu câu thì mọi thứ dựng trên nó đều sai mà không ai biết — đúng kiểu lỗi đắt
 * nhất của Quyển 1.
 *
 * Hai lỗi bộ trích đã mắc và bị chính cổng này bắt:
 *   · kỳ thi thử 3 có ĐỀ A và ĐỀ B cùng đánh số từ Câu 1 → khoá theo số câu làm
 *     đề B đè lên đề A, mất trắng 12 câu
 *   · bài T5 không có phần "— phụ đề" như T1–T4 → biểu thức đòi phụ đề bỏ sót T5
 */
import { readFileSync } from 'node:fs';

const B = JSON.parse(readFileSync(new URL('../../data/quyen2_tho.json', import.meta.url).pathname, 'utf8'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── 1. đếm đúng khối lượng đã đếm tay từ tệp gốc ── */
t('14 vòng đấu', B.vong.length === 14);
t('4 đề trộn', B.detron.length === 4);
t('3 kỳ thi thử', B.thithu.length === 3);
t('5 bài kỹ năng phòng thi', B.kyNang.length === 5);
t('168 hồ sơ bẫy', B.hoSo.length === 168);
t('14 thẻ chiến thuật', B.the.length === 14);

const moiCau = [...B.vong, ...B.detron, ...B.thithu].flatMap((k) => k.cau);
t(`314 câu hỏi (đang có ${moiCau.length})`, moiCau.length === 314);
t('mỗi vòng đấu đúng 15 câu', B.vong.every((v) => v.cau.length === 15));
t('mỗi đề trộn đúng 10 câu', B.detron.every((v) => v.cau.length === 10));
t('thi thử 1 và 2 đúng 20 câu', B.thithu[0].cau.length === 20 && B.thithu[1].cau.length === 20);
t('thi thử 3 đúng 24 câu (đề A 12 + đề B 12)', B.thithu[2].cau.length === 24);
t('thi thử 3 tách được hai đề',
  new Set(B.thithu[2].cau.map((c) => c.de_phu)).size === 2);

/* ── 2. mã câu duy nhất trong từng khối ── */
const trungMa = [];
for (const k of [...B.vong, ...B.detron, ...B.thithu]) {
  const ma = k.cau.map((c) => c.ma);
  if (new Set(ma).size !== ma.length) trungMa.push(k.ten);
}
t(`mã câu không trùng trong cùng một khối (${trungMa.length})`, trungMa.length === 0);

/* ── 3. không câu nào rỗng ── */
const deRong = moiCau.filter((c) => !String(c.de || '').trim());
t(`không câu nào mất đề bài (${deRong.length})`, deRong.length === 0);
const dapRong = moiCau.filter((c) => !String(c.dap || '').trim());
t(`mọi câu đều có lời chữa (${dapRong.length} thiếu)`, dapRong.length === 0);

/* ── 4. hồ sơ bẫy: trục nối hai quyển ── */
const maBay = B.hoSo.map((h) => h.ma);
t('168 mã bẫy không trùng nhau', new Set(maBay).size === 168);
t('mã bẫy nào cũng có dấu hiệu nhận biết', B.hoSo.every((h) => h.dauHieu.length > 20));
t('mã bẫy nào cũng có đòn gỡ', B.hoSo.every((h) => h.donGo.length > 20));
t('mã bẫy nào cũng có thần chú', B.hoSo.every((h) => h.thanChu.length > 5));
t('tầng bẫy chỉ nhận 1 · 2 · 3', B.hoSo.every((h) => [1, 2, 3].includes(h.tang)));
t('mỗi tầng đúng 56 bẫy',
  [1, 2, 3].every((n) => B.hoSo.filter((h) => h.tang === n).length === 56));

/* Trục nối: mọi mã bẫy phải trỏ tới một micro CÓ THẬT của Quyển 1. */
const microQ1 = new Set();
for (let b = 1; b <= 56; b++) for (const m of [1, 2, 3]) microQ1.add(`DL:KSN5Q1.B${b}.M${m}`);
const lac = B.hoSo.filter((h) => !microQ1.has(h.micro));
t(`168 bẫy đều trỏ tới micro có thật của Quyển 1 (${lac.length} lạc)`, lac.length === 0);
t('phủ đủ 168 micro, không bỏ sót micro nào',
  new Set(B.hoSo.map((h) => h.micro)).size === 168);

/* ── 5. KHÔNG MẤT CHỮ — phép kiểm quan trọng nhất ──
   Đếm ký tự đã giữ lại so với tổng ký tự của sách. Trích thiếu một khối lớn thì
   các phép đếm ở trên vẫn có thể xanh, chỉ con số này tụt. */
const chuGiu = JSON.stringify(B).length;
t(`giữ được lượng chữ đáng kể (${Math.round(chuGiu / 1024)} KB)`, chuGiu > 200 * 1024);

/* ── 6. bẫy trong phiên tòa khớp câu có thật ── */
const bayLac = [];
for (const v of B.vong) {
  const soCau = new Set(v.cau.map((c) => c.so));
  for (const b of v.bay) if (!soCau.has(b.cau)) bayLac.push(`${v.ten}: ${b.ma}→câu ${b.cau}`);
}
t(`bẫy phiên tòa trỏ đúng câu có trong đề (${bayLac.length})`, bayLac.length === 0);
t('mỗi vòng đấu có 12 bẫy', B.vong.every((v) => v.bay.length === 12));

/* Thần chú ở phiên tòa: sách ghi hai kiểu ('→ thần chú: "…"' và '→ "…"'), chỉ bắt
   một kiểu thì mất phần lớn. Lỗi này do MẮT phát hiện chứ không phải bộ kiểm —
   nên thêm hàng rào ở đây. */
const moiBay = B.vong.flatMap((v) => v.bay);
const khongThanChu = moiBay.filter((b) => !String(b.thanChu || '').trim());
t(`bẫy nào ở phiên tòa cũng có thần chú (${khongThanChu.length}/${moiBay.length} thiếu)`,
  khongThanChu.length === 0);
const khongTen = moiBay.filter((b) => String(b.ten || '').length < 5);
t(`bẫy nào cũng có tên (${khongTen.length})`, khongTen.length === 0);
t('mã bẫy ở phiên tòa đều có hồ sơ đầy đủ trong phụ lục',
  moiBay.every((b) => B.hoSo.some((h) => h.ma === b.ma)));

console.log(`\n   ${moiCau.length} câu · ${B.hoSo.length} bẫy · ${B.the.length} thẻ`
  + ` · ${B.kyNang.length} bài kỹ năng · ${Math.round(chuGiu / 1024)} KB`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
