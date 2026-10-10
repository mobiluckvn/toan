import test from 'node:test';
import assert from 'node:assert/strict';

import { docLuotTuMoc, soTheoConTro } from '../functions/src/docLuot.js';

/**
 * CỔNG CHO PHÉP PHÂN TRANG NHẬT KÝ.
 *
 * Mươi dòng ấy đã sai ba lần, cả ba đều im lặng: câu truy vấn ném lúc chạy trong
 * một hàm nền hằng tuần · phép lọc trùng nuốt lượt thật · phân trang theo riêng
 * `ts` không đi qua nổi một đoạn dài các lượt chung một mốc. Lần thứ ba chính cổng
 * này bắt được, nên nó ở lại đây.
 *
 * Kho giả dựng đúng thứ tự Firestore sắp khi `orderBy('ts').orderBy('__name__')`.
 */

const khoGia = (ds) => {
  const sapXep = [...ds].sort(soTheoConTro);
  let soLanHoi = 0;
  const lay = async (sau, soLuong) => {
    soLanHoi++;
    if (soLanHoi > 1000) throw new Error('lặp vô tận: phân trang không tiến');
    const tu = sau ? sapXep.findIndex((d) => soTheoConTro(d, sau) > 0) : 0;
    return tu < 0 ? [] : sapXep.slice(tu, tu + soLuong);
  };
  lay.soLanHoi = () => soLanHoi;
  return lay;
};

/* Mã tài liệu đệm 0 cho đủ chữ số: Firestore sắp mã theo CHUỖI, nên 'a10' đứng
   trước 'a9'. Kho giả phải sắp y như thế, nếu không cổng đang thử một thứ tự khác
   với thứ tự thật. */
const dung = (n, ts) => ({ id: `a${String(n).padStart(5, '0')}`, ts, learnerId: 'b1', bktUnit: 'v_x' });

test('đọc đủ khi nhật ký dài hơn một trang', async () => {
  const ds = Array.from({ length: 1250 }, (_, i) => dung(i, 1000 + i));
  const ra = await docLuotTuMoc(khoGia(ds), { trang: 500 });
  assert.equal(ra.length, 1250);
  assert.equal(new Set(ra.map((x) => x.id)).size, 1250, 'không được trùng');
});

test('ĐOẠN DÀI các lượt chung một mốc ts vẫn đọc đủ', async () => {
  /* Cái bẫy thật: cả loạt lượt của một phiên được gửi lên cùng lúc, mang đúng một
     `ts`. Phân trang theo riêng `ts` thì tới đây hoặc mất phần dư, hoặc lặp mãi.
     Con trỏ `(ts, mã)` là duy nhất nên không có trường hợp riêng nào. */
  const ds = [
    ...Array.from({ length: 10 }, (_, i) => dung(i, 1000 + i)),
    ...Array.from({ length: 700 }, (_, i) => dung(100 + i, 5000)),
    ...Array.from({ length: 10 }, (_, i) => dung(900 + i, 9000 + i)),
  ];
  const ra = await docLuotTuMoc(khoGia(ds), { trang: 500 });
  assert.equal(ra.length, 720);
  assert.equal(ra.filter((x) => x.ts === 5000).length, 700, 'nuốt mất lượt ở mốc trùng');
  assert.ok(ra.some((x) => x.ts === 9009), 'phải đi được QUA đoạn mốc trùng');
});

test('TOÀN BỘ nhật ký chung một mốc cũng đọc đủ', async () => {
  const ds = Array.from({ length: 1700 }, (_, i) => dung(i, 5000));
  const ra = await docLuotTuMoc(khoGia(ds), { trang: 500 });
  assert.equal(ra.length, 1700);
});

test('hai lượt khác nhau cùng (bé, nút, ts) đều được giữ', async () => {
  /* Chuyện có thật khi cả loạt gửi lên một lần. Lọc trùng theo bộ ba ấy là nuốt
     mất một lượt — nên phép phân trang này không lọc trùng gì cả, con trỏ lo. */
  const ds = [
    { id: 'a1', ts: 5000, learnerId: 'b1', bktUnit: 'v_x', correct: true },
    { id: 'a2', ts: 5000, learnerId: 'b1', bktUnit: 'v_x', correct: false },
  ];
  const ra = await docLuotTuMoc(khoGia(ds), { trang: 500 });
  assert.equal(ra.length, 2);
});

test('trang cuối ngắn hơn một trang thì dừng — không hỏi thêm vô ích', async () => {
  const ds = Array.from({ length: 300 }, (_, i) => dung(i, 1000 + i));
  const kho = khoGia(ds);
  assert.equal((await docLuotTuMoc(kho, { trang: 500 })).length, 300);
  assert.equal(kho.soLanHoi(), 1);
});

test('trần cứng chặn lại, không đọc vô hạn', async () => {
  const ds = Array.from({ length: 3000 }, (_, i) => dung(i, 1000 + i));
  const ra = await docLuotTuMoc(khoGia(ds), { trang: 500, tran: 1200 });
  assert.equal(ra.length, 1200);
});

test('kho rỗng trả mảng rỗng, không ném', async () => {
  assert.deepEqual(await docLuotTuMoc(khoGia([]), { trang: 500 }), []);
});

test('thứ tự con trỏ khớp cách Firestore sắp mã tài liệu (theo CHUỖI)', () => {
  assert.ok(soTheoConTro({ ts: 1, id: 'a10' }, { ts: 1, id: 'a9' }) < 0,
    "'a10' đứng TRƯỚC 'a9' — mã sắp theo chuỗi, không theo số");
  assert.ok(soTheoConTro({ ts: 2, id: 'a1' }, { ts: 1, id: 'z9' }) > 0, 'ts đứng trước mã');
});
