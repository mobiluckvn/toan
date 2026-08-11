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

/* ── THỨ TỰ TRÊN KỆ ──
   Sổ khai theo thứ tự LÀM XONG quyển (lop2, lop5, lop5q2, lop3, lop4), nên bày đúng
   theo tệp là lớp 5 và Mùa giải chen giữa lớp 2 và lớp 3. `thuTu` là thứ giao diện
   hỏi; thiếu hoặc trùng thì kệ sách xếp lung tung mà chẳng có gì báo. */
t('chương trình nào cũng khai thuTu', ct.every((c) => Number.isFinite(c.thuTu)));
const tt2 = ct.map((c) => c.thuTu);
t('thuTu không trùng nhau', new Set(tt2).size === tt2.length);
const xep = ct.slice().sort((a, b) => a.thuTu - b.thuTu);
t('xếp xong thì lớp tăng dần', xep.every((c, i) => i === 0 || c.lop >= xep[i - 1].lop));
t('quyển ôn thi đứng SAU quyển học cùng lớp',
  xep.every((c, i) => c.loai !== 'giai' || xep.slice(0, i).some((x) => x.lop === c.lop && x.loai === 'hoc')));
t('đúng thứ tự lớp 2 → 3 → 4 → 5 → tổng ôn lớp 5',
  xep.map((c) => c.ma).join(' ') === 'lop2 lop3 lop4 lop5 lop5q2');

/* ── CỜ CHÍNH SÁCH mà trang chính dùng chung hỏi tới ──
   Trang chính của bốn quyển nay là MỘT tệp, khác biệt đọc từ mấy cờ này. Thiếu cờ
   thì quyển ấy im lặng mất một tính năng: mất khoá bài, hoặc mất cửa sang Mùa giải. */
const hoc = ct.filter((c) => c.loai === 'hoc');
t('quyển học nào cũng khai khoaBai', hoc.every((c) => typeof c.khoaBai === 'boolean'));
t('quyển học nào cũng khai soChuong', hoc.every((c) => c.soChuong > 0));
t('quyển 2 nối được về quyển mẹ',
  ct.filter((c) => c.loai === 'giai').every((c) => dk.chuongTrinh[c.choQuyen]
                                                  && dk.chuongTrinh[c.choQuyen].quyen2 === c.ma));

/* ── DANH MỤC KỲ ÔN TẬP — phải có thật và phủ đủ chương ──
   Thiếu tệp thì chương nào cũng mất dòng "kỳ sát hạch", mà màn hình vẫn vẽ ra bình
   thường: bé học xong chương rồi không có chỗ chốt, huy hiệu treo mãi. */
for (const c of hoc) {
  const tep = c.tepOnTap || `${c.thuMuc}/ontap.json`;
  const p = join(D, tep);
  t(`${c.ma}: có danh mục kỳ ôn tập (${tep})`, existsSync(p));
  if (!existsSync(p)) continue;
  const ds = JSON.parse(readFileSync(p, 'utf8'));
  const ky = ds.filter((o) => o.loai !== 'ai').map((o) => o.chapter).sort((a, b) => a - b);
  t(`${c.ma}: mỗi chương đúng một kỳ (${ky.length}/${c.soChuong})`,
    ky.length === c.soChuong
    && ky.every((n, i) => n === i + 1));
  t(`${c.ma}: kỳ nào cũng khai số câu`, ds.every((o) => o.soCau > 0));
  /* `need` CÓ THỂ vắng: ba cửa ải của lớp 3 không đặt ngưỡng, sách chỉ bảo "làm hết
     10 câu". Nhưng khai rồi thì phải nằm trong số câu — và màn hình phải có lời thay
     cho lúc vắng, nếu không bé đọc được đúng chữ "làm đúng null câu là qua". */
  t(`${c.ma}: ngưỡng đạt (nếu có) không vượt số câu`,
    ds.every((o) => o.need == null || (o.need > 0 && o.need <= o.soCau)));
  /* Ba cửa ải đánh số chương TIẾP SAU chương cuối — trùng vào chương thật thì kết
     quả ải đè lên huy hiệu chương, hai thứ khác hẳn nhau. */
  t(`${c.ma}: cửa ải không trùng số chương thật`,
    ds.filter((o) => o.loai === 'ai').every((o) => o.chapter > c.soChuong));
}

/* Lớp 5 không đánh chương trong dữ liệu bài (suy bằng công thức), nên tên chương
   phải khai ở sổ — thiếu thì trang chính hiện "Chương 7" trần. */
const l5 = dk.chuongTrinh.lop5;
t('lớp 5 khai đủ tên chương',
  (l5.chuong || []).length === l5.soChuong
  && l5.chuong.every((c, i) => c.so === i + 1 && c.ten && c.ten.length > 2));

t('mục sắp có nào cũng có môn và tên',
  (dk.sapCo || []).every((s) => dk.mon[s.mon] && s.nhom && s.ten));
t('đề ôn thi nào cũng khai trạng thái',
  (dk.luyenThi || []).every((s) => s.ma && s.ten && s.trangThai));

console.log(`\n   ${ct.length} chương trình · ${(dk.sapCo || []).length} nhóm sắp có`
  + ` · ${(dk.luyenThi || []).length} đề ôn thi`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
