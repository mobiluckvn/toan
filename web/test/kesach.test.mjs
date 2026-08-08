/**
 * CỔNG KỆ SÁCH — sổ đăng ký chương trình có dùng được không.
 * chạy: node test/kesach.test.mjs
 *
 * Kệ sách dựng HOÀN TOÀN từ data/chuong_trinh.json: thêm lớp mới hay môn mới thì
 * thêm một mục ở đó, không sửa giao diện. Nên sổ sai là kệ sách hỏng, mà hỏng kiểu
 * im lặng — mục thiếu trường thì chỉ mất một dòng chữ, không ai thấy.
 */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const D = new URL('../public/content/', import.meta.url).pathname;
const dk = JSON.parse(readFileSync(join(D, 'chuong_trinh.json'), 'utf8'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const ct = Object.values(dk.chuongTrinh || {});
t(`có chương trình (${ct.length})`, ct.length >= 2);
t('mã trong khoá khớp trường ma',
  Object.entries(dk.chuongTrinh).every(([k, v]) => k === v.ma));

/* Trường nào thiếu thì kệ sách mất một mẩu mà không báo — nên soi từng cái. */
for (const truong of ['ma', 'mon', 'ten', 'bieuTuong', 'tienTo', 'thuMuc', 'soBai']) {
  t(`chương trình nào cũng khai "${truong}"`, ct.every((c) => c[truong] !== undefined));
}
t('môn của chương trình phải có trong danh mục môn',
  ct.every((c) => (dk.mon || {})[c.mon]));
t('soBai > 0', ct.every((c) => c.soBai > 0));

/* TIỀN TỐ là thứ map mã bài → chương trình. Trùng nhau hoặc là tiền tố của nhau
   thì bài của lớp này bị tính sang lớp kia, tiến độ hiện sai mà chẳng có gì báo. */
const tt = ct.map((c) => c.tienTo);
t('tiền tố không trùng nhau', new Set(tt).size === tt.length);
t('tiền tố không phải tiền tố của nhau',
  tt.every((a) => tt.filter((b) => b !== a).every((b) => !b.startsWith(a))));

/* Thư mục nội dung phải có thật, nếu không mở bài ra là lỗi 404. */
t('thư mục nội dung có thật',
  ct.every((c) => existsSync(join(D, c.thuMuc))));

/* soBai phải khớp số bài THẬT — lệch thì thanh tiến độ nói dối con. */
const lop2 = dk.chuongTrinh.lop2;
t(`soBai của lớp 2 khớp danh sách bài (${lop2.soBai})`,
  lop2.soBai === (lop2.bai || []).length);

t('mục sắp có nào cũng có môn và tên',
  (dk.sapCo || []).every((s) => dk.mon[s.mon] && s.nhom && s.ten));
t('đề ôn thi nào cũng khai trạng thái',
  (dk.luyenThi || []).every((s) => s.ma && s.ten && s.trangThai));

console.log(`\n   ${ct.length} chương trình · ${(dk.sapCo || []).length} nhóm sắp có`
  + ` · ${(dk.luyenThi || []).length} đề ôn thi`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
