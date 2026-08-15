/* ═══════════ PHỤ ĐỀ QUYỂN KHÔNG ĐƯỢC GỌI TÊN NGƯỜI ĐÃ ĐI KHỎI QUYỂN ═══════════
 * chạy: node test/phu_de_dung_nhan_vat.test.mjs
 *
 * ── LỖI ĐÃ XẢY RA THẬT ──
 *
 * Trang chính lớp 2 chào bé bằng dòng "Cùng Trí Long khám phá Vương quốc Số", trong
 * khi cả 71 bài của quyển ấy KHÔNG còn một chữ "Trí Long" nào — bác chốt bỏ hẳn nhân
 * vật cho lớp 2 và lớp 4, viết lại như lớp 4. Bé đọc dòng chào, chờ gặp Trí Long
 * suốt cả quyển, và không bao giờ gặp.
 *
 * Đợt viết lại quét sạch nội dung BÀI. Phụ đề nằm ở `data/chuong_trinh.json` — một
 * tệp khác, không ai coi là "nội dung", nên nó sống sót. Lại là lỗi ở chỗ nối: cả
 * hai bên đều đúng phần mình, chỉ không ai hỏi câu nối giữa hai bên.
 *
 * ── PHÉP DƯỚI ĐÂY SOI GÌ ──
 *
 * Với MỖI quyển: tên nhân vật nào xuất hiện trong phụ đề thì phải xuất hiện trong
 * nội dung quyển ấy. Không cấm nhân vật — lớp 3 và lớp 5 vẫn giữ Su Kem, Su Bống —
 * chỉ cấm HỨA suông.
 *
 * Chiều ngược lại (quyển có nhân vật mà phụ đề không nhắc) là chuyện bình thường,
 * không soi.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
const ND = join(G, 'web/public/content');

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* Cùng danh sách với `test/hinhmobai.test.mjs`. Thêm tên mới thì thêm ở CẢ HAI —
   hoặc gộp lại một chỗ, nhưng đừng để hai nơi biết hai danh sách khác nhau. */
const NHAN_VAT = ['Su Kem', 'Trí Long', 'Cáo Đề', 'Su Bống'];

/* Quyển nào đọc bài ở thư mục nào. Tên thư mục không suy được từ mã quyển
   (`lop5` → `lessons`), nên khai thẳng. */
const THU_MUC = { lop2: 'lop2', lop3: 'lop3', lop4: 'lop4', lop5: 'lessons' };

const ct = JSON.parse(readFileSync(join(ND, 'chuong_trinh.json'), 'utf8'));
const quyen = [];
(function di(o) {
  if (Array.isArray(o)) return o.forEach(di);
  if (o && typeof o === 'object') {
    if (o.phuDe && o.ma) quyen.push(o);
    Object.values(o).forEach(di);
  }
}(ct));

t(`đọc được sổ chương trình (${quyen.length} quyển có phụ đề)`, quyen.length >= 4);

let soSoi = 0;
for (const q of quyen) {
  const goiTen = NHAN_VAT.filter((n) => q.phuDe.includes(n));
  if (!goiTen.length) continue;                      // phụ đề không hứa gì — bỏ qua

  const tm = THU_MUC[q.ma];
  if (!tm || !existsSync(join(ND, tm))) {
    t(`${q.ma} · phụ đề gọi tên ${goiTen.join(', ')} mà không tìm ra thư mục bài`, false);
    continue;
  }
  const chu = readdirSync(join(ND, tm))
    .filter((f) => /^DL_.*\.json$/.test(f))
    .map((f) => readFileSync(join(ND, tm, f), 'utf8'))
    .join('\n');

  for (const n of goiTen) {
    soSoi += 1;
    const co = chu.includes(n);
    t(`${q.ma} · phụ đề hứa "${n}" thì bài phải có "${n}"`, co);
    if (!co) console.log(`      phụ đề: “${q.phuDe}” — mà ${tm}/ không có chữ nào`);
  }
}

/* Đảo chiều: phép trên chỉ có nghĩa nếu nó THẬT SỰ đọc được nội dung bài. Lớp 3 và
   lớp 5 đang giữ nhân vật, nên phải có ít nhất một lời hứa được soi và soi ra CÓ. */
t(`có lời hứa nào để mà soi (${soSoi} lượt)`, soSoi > 0);
const l3 = readdirSync(join(ND, 'lop3')).filter((f) => /^DL_/.test(f))
  .map((f) => readFileSync(join(ND, 'lop3', f), 'utf8')).join('');
t('(đối chứng) lớp 3 vẫn còn nhân vật thật trong bài', /Su Kem|Su Bống/.test(l3));
const l2 = readdirSync(join(ND, 'lop2')).filter((f) => /^DL_/.test(f))
  .map((f) => readFileSync(join(ND, 'lop2', f), 'utf8')).join('');
t('(đối chứng) lớp 2 đã sạch nhân vật',
  !NHAN_VAT.some((n) => l2.includes(n)));

console.log(`\n   ${quyen.length} quyển · ${soSoi} lời hứa được soi\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
