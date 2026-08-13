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
import { LOP_HOC, gomNhomKeSach } from '../src/chung/lib/soQuyen.js';

const D = new URL('../public/content/', import.meta.url).pathname;
const dk = JSON.parse(readFileSync(join(D, 'chuong_trinh.json'), 'utf8'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

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
/* Thứ tự trên kệ phải SUY RA ĐƯỢC, không phải một danh sách tên gõ cứng.
   Bản đầu so với đúng chuỗi 'lop2 lop3 lop4 lop5 lop5q2', nên quyển Tiếng Anh lớp 1
   vừa khai vào sổ là cổng đỏ — dù nó xếp hoàn toàn đúng chỗ (lớp 1 đứng trước lớp 2).
   Đây đúng loại "ghim cứng tên quyển" mà kho này đã dính nhiều lần.

   Luật thật: xếp theo LỚP tăng dần, và trong cùng một lớp thì quyển HỌC đứng trước
   quyển ÔN THI. `thuTu` phải khớp đúng thứ tự ấy. */
const khoa = (c) => [c.lop, c.loai === 'giai' ? 1 : 0];
const nen = ct.slice().sort((a, b) => khoa(a)[0] - khoa(b)[0] || khoa(a)[1] - khoa(b)[1]);
t(`thuTu khớp thứ tự lớp rồi tới quyển ôn thi (${xep.map((c) => c.ma).join(' → ')})`,
  xep.map((c) => c.ma).join(' ') === nen.map((c) => c.ma).join(' '));

/* ── LỚP CON KHAI ĐƯỢC PHẢI PHỦ MỌI QUYỂN ĐANG CÓ ──
   `LOP_HOC` mở đầu từ lớp 2 suốt từ đầu, vì quyển nhỏ nhất khi ấy là Toán lớp 2.
   Thêm Tiếng Anh lớp 1 thì bé 6 tuổi — bạn NHỎ NHẤT của app — lập hồ sơ mà không
   khai được đúng lớp mình: phải khai lớp 2, rồi con số sai ấy đi thẳng vào bảng
   xếp hạng và vào bậc xuất phát của vòng luyện.

   Không cổng nào bắt được, vì màn hình vẫn vẽ ra bình thường. Nên soi ở đây: có
   sách cho lớp nào thì bé lớp ấy phải khai được. */
const lopThieu = [...new Set(ct.map((c) => c.lop))]
  .filter((l) => Number.isFinite(l) && !LOP_HOC.includes(l));
t(`mọi lớp có sách đều khai được trong hồ sơ (${lopThieu.length} lớp thiếu)`,
  lopThieu.length === 0);
in5(lopThieu.map((l) => `lớp ${l} có sách mà LOP_HOC không có`));

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

/* ── NHÓM TRÊN KỆ SÁCH ──
   Kệ sách gom quyển theo `nhom` chứ không theo mã môn: bốn quyển lớp 2·3·4·5 là
   "Toán cấp 1", mai kia có cấp 2 thì tách ra mà không phải sửa giao diện. */
t('quyển nào cũng khai nhóm trên kệ',
  ct.every((c) => typeof c.nhom === 'string' && c.nhom.length > 2));

/* Cửa phụ ("Học theo chủ đề") khai `nhom` trong tệp index.js của từng môn, còn
   quyển khai trong sổ này. HAI NƠI, và phải TRÙNG TỪNG CHỮ — lệch một chữ thì cửa
   rơi ra thành một nhóm riêng chỉ có mình nó, giao diện vẫn vẽ đẹp, không có gì
   báo. Đây đúng loại hỏng câm nên phải có cổng. */
{
  const nhomCuaQuyen = new Set(ct.map((c) => c.nhom));
  const src = readFileSync(new URL('../src/mon/toan/index.js', import.meta.url), 'utf8');
  const khai = [...src.matchAll(/nhom:\s*'([^']+)'/g)].map((m) => m[1]);
  t('cửa phụ của Toán có khai nhóm', khai.length > 0);
  t('nhóm của cửa phụ trùng với nhóm của quyển',
    khai.every((n) => nhomCuaQuyen.has(n)));
  if (!khai.every((n) => nhomCuaQuyen.has(n))) {
    in5(khai.filter((n) => !nhomCuaQuyen.has(n)).map((n) => `cửa phụ khai "${n}" — không quyển nào thuộc nhóm này`));
  }
}

/* Quyển đã lên kệ rồi mà mục "sắp có" vẫn ghi môn ấy đang biên soạn thì hai chỗ
   trên cùng MỘT màn nói ngược nhau. Đã dính thật: Tiếng Anh lớp 1 chạy được từ
   12-08 mà mục sắp có vẫn ghi "Đang biên soạn". */
t('môn đã có quyển thì mục sắp có không được ghi "Đang biên soạn"',
  (dk.sapCo || []).every((s) => !(ct.some((c) => c.mon === s.mon) && /đang biên soạn/i.test(s.ten))));

/* ── PHÉP GOM NHÓM ──
   Luật ở `gomNhomKeSach`, không ở JSX, nên soi được bằng node. Dựng sổ giả để thử
   đúng cái luật chứ không phụ thuộc nội dung thật. */
{
  const q = (ma, mon, nhom, dangLam = 0, gio = 0) =>
    ({ ct: { ma, mon, nhom }, td: { dangLam, gio, xong: 0, tong: 10 } });
  const tenMon = (m) => ({ toan: 'Toán', tienganh: 'Tiếng Anh' }[m] || m);

  const nh = gomNhomKeSach(
    [q('lop2', 'toan', 'Toán cấp 1'), q('lop3', 'toan', 'Toán cấp 1', 1, 500),
     q('ta1', 'tienganh', 'Tiếng Anh', 1, 900)],
    [{ ma: 'toan', cuaPhu: [{ trang: 'chuDe', nhom: 'Toán cấp 1', ten: 'Học theo chủ đề' }] }],
    tenMon,
  );
  t('gom đúng số nhóm', nh.length === 2);
  const toan = nh.find((x) => x.ten === 'Toán cấp 1');
  const ta = nh.find((x) => x.ten === 'Tiếng Anh');
  t('cửa phụ nằm TRONG nhóm của nó', toan.cua.length === 1 && ta.cua.length === 0);

  /* Đây là chỗ bản trước hỏng: MỘT thẻ học tiếp cho cả app, nên bé học dở cả hai
     môn thì một môn biến mất khỏi chỗ dễ thấy nhất. */
  t('MỖI nhóm có chỗ học tiếp riêng',
    toan.tiep?.ct.ma === 'lop3' && ta.tiep?.ct.ma === 'ta1');
  /* Quyển đang học VẪN nằm trong danh sách. Bản đầu lấy nó ra cho khỏi lặp, nhưng
     thế là nhóm Tiếng Anh (một quyển) không còn danh sách lớp nào — mà "chọn bài
     theo nhu cầu" thì phải nhìn thấy đủ các lớp mới chọn được. */
  t('danh sách nhóm liệt kê ĐỦ mọi quyển, kể cả quyển đang học tiếp',
    toan.sach.length === 2 && toan.sach.some((x) => x.ct.ma === 'lop3')
    && ta.sach.length === 1);

  /* Chưa học gì thì không có thẻ học tiếp — thẻ trống chỉ tổ làm bé tưởng đang dở. */
  const sach = gomNhomKeSach([q('lop2', 'toan', 'Toán cấp 1')], [], tenMon);
  t('sổ trắng thì nhóm không mọc thẻ học tiếp',
    sach[0].tiep === null && sach[0].sach.length === 1);

  /* Quyển quên khai `nhom` phải rơi về tên môn, đừng rơi vào nhóm "undefined". */
  const thieu = gomNhomKeSach([q('lopX', 'toan', undefined)], [], tenMon);
  t('quyển quên khai nhóm rơi về tên môn', thieu[0].ten === 'Toán');

  /* Nhiều quyển cùng dở thì chọn quyển ĐỘNG VÀO GẦN NHẤT, không phải quyển đầu. */
  const hai = gomNhomKeSach(
    [q('lop2', 'toan', 'Toán cấp 1', 1, 100), q('lop4', 'toan', 'Toán cấp 1', 1, 900)], [], tenMon);
  t('học tiếp chỉ vào quyển động vào gần nhất', hai[0].tiep.ct.ma === 'lop4');
}
t('đề ôn thi nào cũng khai trạng thái',
  (dk.luyenThi || []).every((s) => s.ma && s.ten && s.trangThai));

console.log(`\n   ${ct.length} chương trình · ${(dk.sapCo || []).length} nhóm sắp có`
  + ` · ${(dk.luyenThi || []).length} đề ôn thi`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
