/**
 * Kiểm LÕI VÒNG ĐẤU (Quyển 2) — chạy: node test/dau.test.mjs
 *
 * Ba tầng chấm và cái đồng hồ. Chỗ dễ hỏng nhất là đồng hồ: đếm lùi bằng biến thì
 * con khoá máy tính bảng giữa chừng sẽ được thêm giờ không công, mà lỗi ấy không
 * bao giờ lộ ra khi thử trên máy bàn.
 */
import {
  BAREM, diemBarem, diemDapSo, datChua, keDonOn, tuyenAn,
  conLai, hetGio, docGio, chamKep, moKhoa, chuongDaXong,
} from '../src/mon/toan/lib/dau.js';
import { readFileSync } from 'node:fs';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── barem 4 mốc ── */
t('barem có đúng 4 mốc', BAREM.length === 4);
t('ba mốc tính điểm cộng lại đúng 1 điểm',
  Math.abs(BAREM.reduce((s, m) => s + m.diem, 0) - 1) < 1e-9);
t('tick đủ ba mốc được trọn 1 điểm',
  diemBarem({ canCu: true, phepTinh: true, dapSo: true }) === 1);
t('chỉ có phép tính đúng được 0,5', diemBarem({ phepTinh: true }) === 0.5);
t('thử lại không cộng điểm', diemBarem({ thuLai: true }) === 0);
t('không tick gì thì 0 điểm', diemBarem({}) === 0);

/* ── tầng 1 · điểm đáp số ── */
const khoi = {
  id: 'DR:KSN5Q2.V01', dat: 12, chuongQ1: 1,
  cau: [
    { id: 'C1', answerKey: { value: '1' } },
    { id: 'C2', answerKey: { value: '2' } },
    { id: 'C3', tuLuan: true },
  ],
  bay: [
    { ma: 'CĐ-1.1', ten: 'bẫy một', micro: 'DL:KSN5Q1.B1.M1', thanChu: 'a' },
    { ma: 'CĐ-2.2', ten: 'bẫy hai', micro: 'DL:KSN5Q1.B2.M2', thanChu: 'b' },
  ],
};
t('câu máy chấm tính theo ok',
  diemDapSo(khoi, { C1: { ok: true }, C2: { ok: false } }).dung === 1);
/* Câu tự luận KHÔNG có ok — nếu lấy nhầm `ok` thì mọi câu tự luận đều thành sai,
   tức 212/314 câu của Quyển 2 bị chấm 0 điểm oan. */
t('câu tự luận tính theo con TỰ CHẤM',
  diemDapSo(khoi, { C3: { tuChamDung: true } }).dung === 1);
t('câu tự luận mà chỉ có ok thì không tính',
  diemDapSo(khoi, { C3: { ok: true } }).dung === 0);
t('chưa làm câu nào thì 0 điểm', diemDapSo(khoi, {}).dung === 0);

/* ── ngưỡng đạt lấy từ sách ── */
const day = (n) => Object.fromEntries(
  Array.from({ length: n }, (_, i) => [`C${i + 1}`, { ok: true }]));
const k15 = { dat: 12, cau: Array.from({ length: 15 }, (_, i) => ({ id: `C${i + 1}`, answerKey: {} })) };
t('12/15 là ĐẠT', datChua(k15, day(12)).dat === true);
t('11/15 là CHƯA đạt', datChua(k15, day(11)).dat === false);
t('không có ngưỡng thì lấy 80%', datChua({ cau: k15.cau }, day(12)).dat === true);

/* ── tầng 3 · phiên tòa bẫy → kê đơn ôn ngược Quyển 1 ── */
const don = keDonOn(khoi, { 'CĐ-1.1': 'sap', 'CĐ-2.2': 'thoat' });
t('đếm đúng số bẫy đã sập', don.soSap === 1);
t('kê đúng micro Quyển 1 cần ôn', don.micro[0] === 'DL:KSN5Q1.B1.M1');
t('bẫy thoát được thì không kê đơn', !don.micro.includes('DL:KSN5Q1.B2.M2'));
t('chưa soi bẫy nào thì đơn rỗng', keDonOn(khoi, {}).soSap === 0);
t('tuyên án nhẹ khi sập ít', tuyenAn(1).startsWith('Xuất sắc'));
t('tuyên án nặng khi sập nhiều', tuyenAn(8).includes('ôn lại'));

/* ── đồng hồ ── */
const T0 = 1_000_000;
t('mới bấm thì còn đủ 45 phút', conLai(T0, 45, T0) === 45 * 60000);
t('trôi 10 phút thì còn 35', conLai(T0, 45, T0 + 10 * 60000) === 35 * 60000);
t('quá giờ thì còn 0, không âm', conLai(T0, 45, T0 + 60 * 60000) === 0);
t('hết giờ báo đúng', hetGio(T0, 45, T0 + 45 * 60000) === true);
t('chưa hết giờ báo đúng', hetGio(T0, 45, T0 + 44 * 60000) === false);
/* Con khoá máy 20 phút rồi mở lại: thời gian VẪN trôi. Đếm lùi bằng biến sẽ đứng
   yên và con được thêm 20 phút không công. */
t('khoá máy giữa chừng vẫn bị trừ giờ',
  conLai(T0, 45, T0 + 20 * 60000) === 25 * 60000);
t('đọc giờ đúng định dạng', docGio(154000) === '2:34');
t('đọc giờ có đệm số 0', docGio(65000) === '1:05');
t('hết giờ đọc là 0:00', docGio(0) === '0:00');

/* ── chấm kép cho đề trộn ── */
const kTron = { dat: 8, cau: Array.from({ length: 10 }, (_, i) => ({ id: `C${i + 1}`, answerKey: {} })) };
const okHet = day(10);
const dangHet = Object.fromEntries(kTron.cau.map((c) => [c.id, { dung: true }]));
const kq = chamKep(kTron, okHet, dangHet);
t('chấm kép cho hai cột riêng', kq.toan === 10 && kq.dinhDang === 10);
t('hai cột đủ ngưỡng thì đạt', kq.dat === true);
/* Sách nói rõ: chỉ cần MỘT cột dưới ngưỡng là chưa đạt — hai loại lỗi cần hai
   loại thuốc, cộng gộp lại là giấu mất chỗ con yếu. */
const kem = chamKep(kTron, okHet, {});
t('giỏi toán nhưng gọi sai tên dạng thì CHƯA đạt', kem.dat === false);
t('hai cột không cộng gộp vào nhau', kem.toan === 10 && kem.dinhDang === 0);

/* Ca then chốt: toán 10/10 nhưng định dạng 6/10, ngưỡng 8. Cộng gộp rồi chia đôi
   ra đúng 8 → "đạt", che mất việc con gọi sai tên dạng 4 câu. Chấm đúng phải là
   CHƯA đạt. Ca 10-và-0 ở trên không phân biệt được hai cách tính. */
const buTru = chamKep(kTron, okHet,
  Object.fromEntries(kTron.cau.slice(0, 6).map((c) => [c.id, { dung: true }])));
t('giỏi toán KHÔNG bù được cho định dạng kém (10 và 6, ngưỡng 8)',
  buTru.toan === 10 && buTru.dinhDang === 6 && buTru.dat === false);

/* ── mở khoá theo chương Quyển 1 ── */
t('chưa xong chương 1 thì vòng 1 còn khoá', moKhoa(khoi, new Set()) === false);
t('xong chương 1 thì vòng 1 mở', moKhoa(khoi, new Set([1])) === true);
t('xong chương khác không mở hộ vòng 1', moKhoa(khoi, new Set([2, 3])) === false);
t('khối không gắn chương thì mở tự do', moKhoa({ cau: [] }, new Set()) === true);

const chuongCua = (id) => Math.ceil(Number(id.split('.B')[1].split('.M')[0]) / 4);
const tienDo = {};
for (let b = 1; b <= 4; b++) for (const m of [1, 2, 3]) tienDo[`DL:KSN5Q1.B${b}.M${m}`] = { pass: true };
t('học hết 12 micro của chương 1 → chương 1 xong',
  chuongDaXong(tienDo, chuongCua).has(1));
/* Sổ tiến độ là sổ CHUNG của bốn quyển. Bài lớp 2·3·4 lọt vào đây thì `chuongCua`
   (hàm chia chương của Quyển 1) trả về chương 1 cho tất cả — chỉ cần con học dở một
   bài lớp 3 là VÒNG ĐẤU 1 khoá cứng dù đã học hết 12 micro của chương 1. Dính thật. */
t('bài của quyển khác KHÔNG làm hỏng phép đếm chương Quyển 1',
  chuongDaXong({ ...tienDo, 'DL:KSN4.B30': { pass: false }, 'DL:KSN3.B01': { pass: false } },
               chuongCua).has(1));

tienDo['DL:KSN5Q1.B4.M3'] = { pass: false };
t('còn một micro chưa đạt thì chương CHƯA xong',
  !chuongDaXong(tienDo, chuongCua).has(1));

/* ── chạy trên dữ liệu THẬT của Quyển 2 ── */
const D = new URL('../public/content/quyen2/', import.meta.url).pathname;
const idx = JSON.parse(readFileSync(D + 'index.json', 'utf8'));
t('chỉ mục có đủ 21 khối', idx.length === 21);
const v1 = JSON.parse(readFileSync(D + 'DR_KSN5Q2_V01.json', 'utf8'));
t('vòng 1 mở khi xong chương 1', moKhoa(v1, new Set([1])) === true);
t('vòng 1 có ngưỡng đạt hợp lệ', v1.dat > 0 && v1.dat <= v1.thang);
t('làm đúng hết vòng 1 thì ĐẠT',
  datChua(v1, Object.fromEntries(v1.cau.map((c) => [c.id, { ok: true, tuChamDung: true }]))).dat);
t('làm sai hết vòng 1 thì KHÔNG đạt',
  !datChua(v1, Object.fromEntries(v1.cau.map((c) => [c.id, { ok: false }]))).dat);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
