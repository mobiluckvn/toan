/**
 * CỔNG SỔ NGƯỜI DÙNG — nhiều bé chung một máy.
 * chạy: node test/nguoi_dung.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Máy tính bảng là của cả nhà: anh lớp 5, em lớp 2. Firebase Auth chỉ giữ MỘT phiên
 * cho mỗi thể hiện app, nên mỗi bé được cấp một "chỗ" và phiên nằm riêng trong chỗ ấy.
 *
 * Thứ dễ vỡ nhất KHÔNG phải phiên đăng nhập mà là SỔ TẠI MÁY. Lúc đi thử đã dính đúng
 * một lần: em vừa đăng nhập xong đã thấy "đã học xong 2 trên 33 bài" của anh, vì sổ
 * tiến độ và hàng đợi dùng chung một khoá localStorage. Trộn sổ đã tệ, nhưng hàng đợi
 * còn tệ hơn: `reassignQueue` sang tên CẢ hàng cho tài khoản vừa đăng nhập, nên bài
 * anh vừa làm bị ghi lên máy chủ dưới tên em — mà nhật ký thì bất biến.
 */
import {
  dsNguoi, ghiNguoi, xoaNguoi, choTrong, choDangDung, doiCho, dangThemBe,
  tenHien, chuDau, CHO_DAU,
} from '../src/chung/lib/nguoiDung.js';

/** localStorage giả — mỗi phép kiểm một kho sạch. */
const kho = () => {
  let s = {};
  return {
    getItem: (k) => (k in s ? s[k] : null),
    setItem: (k, v) => { s[k] = String(v); },
    removeItem: (k) => { delete s[k]; },
    _raw: () => s,
  };
};

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── 1 · Ghi và đọc sổ ── */
let K = kho();
t('máy mới thì sổ rỗng', dsNguoi(K).length === 0);
t('chỗ mặc định là chỗ đầu', choDangDung(K) === CHO_DAU);

ghiNguoi({ cho: 'c1', uid: 'u1', email: 'anh@x.test', ten: 'Minh', lop: 5, lanCuoi: 100 }, K);
ghiNguoi({ cho: 'c2', uid: 'u2', email: 'em@x.test', ten: 'Lan', lop: 2, lanCuoi: 200 }, K);
t('nhớ đủ hai bé', dsNguoi(K).length === 2);
t('bé động vào gần nhất lên đầu', dsNguoi(K)[0].ten === 'Lan');

/* Một CHỖ chỉ giữ được một phiên, nên ghi đè theo chỗ mới đúng. */
ghiNguoi({ cho: 'c2', uid: 'u3', email: 'be3@x.test', ten: 'Bống', lop: 3, lanCuoi: 300 }, K);
t('bé mới vào cùng chỗ thì THAY bé cũ, không nhân đôi', dsNguoi(K).length === 2);
t('chỗ ấy nay là bé mới', dsNguoi(K).find((n) => n.cho === 'c2').ten === 'Bống');

/* ── 2 · Cấp chỗ ── */
t('chỗ trống tiếp theo là c3', choTrong(K) === 'c3');
xoaNguoi('c1', K);
t('bé rời đi thì chỗ ấy dùng lại được', choTrong(K) === 'c1');
t('xoá rồi thì sổ còn một bé', dsNguoi(K).length === 1);

/* ── 3 · Đổi chỗ và dấu "vừa thêm bé" ── */
K = kho();
let daTaiLai = 0;
doiCho('c7', { kho: K, taiLai: () => { daTaiLai++; } });
t('đổi chỗ thì ghi lại chỗ đang mở', choDangDung(K) === 'c7');
t('đổi chỗ thì TẢI LẠI trang', daTaiLai === 1);
t('đổi sang bé đã có thì KHÔNG đánh dấu "vừa thêm"', dangThemBe(K) === false);

doiCho('c8', { kho: K, taiLai: () => {}, moi: true });
t('cấp chỗ trống cho bé mới thì có đánh dấu', dangThemBe(K) === true);
/* Đọc xong là xoá — nếu không, lần mở app SAU vẫn bỏ qua màn "ai đang học". */
t('dấu chỉ dùng được MỘT lần', dangThemBe(K) === false);

/* ── 4 · Tên hiện lên nút ── */
t('có tên thì lấy tên', tenHien({ ten: 'Minh', email: 'a@b.test' }) === 'Minh');
t('không tên thì lấy phần trước @', tenHien({ email: 'be.lan@x.test' }) === 'be.lan');
t('không có gì thì vẫn có chữ để hiện', tenHien({}) === 'Bạn nhỏ');
t('chữ cái đầu viết hoa', chuDau({ ten: 'minh' }) === 'M');

/* ── 5 · SỔ TẠI MÁY PHẢI TÁCH THEO BÉ ──
   Chốt chặn quan trọng nhất của cả tệp này. Kiểm bằng chính hàm thật của môn Toán,
   không dựng lại công thức khoá — viết lại là hai bên trôi khỏi nhau lúc nào không hay. */
const { loadProgress, saveProgress, emptyProgress, recordMicro } =
  await import('../src/mon/toan/lib/progress.js');
const { readQueue, writeQueue } = await import('../src/mon/toan/lib/sync.js');

const KHO = kho();
const cu = globalThis.localStorage;
globalThis.localStorage = KHO;                 // `choDangDung()` đọc kho toàn cục
try {
  KHO.setItem('ttd5.choDangDung.v1', CHO_DAU);
  saveProgress(recordMicro(emptyProgress(), 'DL:KSN2.B01',
    { pass: true, mustOK: true, right: 9, total: 9 }), KHO);
  writeQueue([{ id: 'x_1', learnerId: 'u1' }], KHO);
  const soAnh = Object.keys(loadProgress(KHO).micros).length;
  t('bé đầu ghi được sổ', soAnh === 1);

  KHO.setItem('ttd5.choDangDung.v1', 'c2');    // em vừa đăng nhập vào chỗ khác
  t('bé thứ hai KHÔNG thấy sổ của anh', Object.keys(loadProgress(KHO).micros).length === 0);
  t('bé thứ hai KHÔNG thấy hàng đợi của anh', readQueue(KHO).length === 0);

  saveProgress(recordMicro(emptyProgress(), 'DL:KSN2.B02',
    { pass: true, mustOK: true, right: 9, total: 9 }), KHO);
  KHO.setItem('ttd5.choDangDung.v1', CHO_DAU);
  t('em học xong, sổ của anh vẫn NGUYÊN', Object.keys(loadProgress(KHO).micros).length === 1);
  t('chỗ đầu vẫn dùng khoá cũ — máy đang chạy không mất sổ',
    KHO.getItem('ttd5.progress.v1') !== null);
} finally { globalThis.localStorage = cu; }

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
