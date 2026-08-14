/**
 * CỔNG · CHUYỂN TIẾN ĐỘ SANG SỐ BÀI MỚI CỦA LỚP 4.
 *
 * 14-08-2026 cụm dãy số tách thành năm bài, nên B13 cũ lùi thành B18 và 31 bài sau
 * đó dồn theo 5 chỗ. Tiến độ của bé khoá theo MÃ BÀI, nên phải chuyển — và đây là
 * loại việc chỉ được làm ĐÚNG MỘT LẦN trên dữ liệu thật của bé:
 *
 *   · chạy thiếu → huy hiệu gắn nhầm bài, bé thấy mình đã qua bài chưa từng học;
 *   · chạy thừa  → dời thêm 5 chỗ nữa, mã trôi ra ngoài dải và bé MẤT SẠCH tiến độ.
 *
 * Cả hai đều không có gì báo. Nên cổng này soi kỹ hơn bình thường.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { maMoi, chuyenSo, daChuyen, DAI, CO } from '../src/mon/toan/lib/donSoLop4.js';

test('mã trong dải dời đúng 5 chỗ, ngoài dải giữ nguyên', () => {
  assert.equal(maMoi('DL:KSN4.B13'), 'DL:KSN4.B18');
  assert.equal(maMoi('DL:KSN4.B44'), 'DL:KSN4.B49');
  assert.equal(maMoi('DL:KSN4.B12'), 'DL:KSN4.B12', 'B12 chưa tới lượt dời');
  assert.equal(maMoi('DL:KSN4.B01'), 'DL:KSN4.B01');
  /* Mã MỚI (B45–B49) không được dời tiếp — đó chính là dấu hiệu chạy hai lần. */
  assert.equal(maMoi('DL:KSN4.B49'), 'DL:KSN4.B49');
});

test('KHÔNG đụng quyển khác', () => {
  for (const id of ['DL:KSN2.B13', 'DL:KSN3.B13', 'DL:KSN5Q1.B13_M1', 'DL:TA1.B13']) {
    assert.equal(maMoi(id), id, `${id} không thuộc lớp 4, phải giữ nguyên`);
  }
});

test('dời đi từ số LỚN xuống — không dồn hai lần', () => {
  /* Đây là cái bẫy kinh điển của mọi phép đánh số lại: dời B13→B18 trước thì tới
     lượt B18 (vừa mới thành) lại bị dời tiếp thành B23. Đưa cả dải vào một lúc để
     bắt đúng chuyện ấy. */
  const micros = {};
  for (let n = DAI.tu; n <= DAI.den; n += 1) {
    micros[`DL:KSN4.B${String(n).padStart(2, '0')}`] = { pass: true, danhDau: n };
  }
  const sau = chuyenSo({ micros }).micros;
  assert.equal(Object.keys(sau).length, DAI.den - DAI.tu + 1, 'không được mất bài nào');
  for (let n = DAI.tu; n <= DAI.den; n += 1) {
    const k = `DL:KSN4.B${String(n + DAI.dich).padStart(2, '0')}`;
    assert.ok(sau[k], `thiếu ${k}`);
    assert.equal(sau[k].danhDau, n, `${k} phải mang đúng bản ghi của B${n}, không phải bài khác`);
  }
});

test('CHẠY HAI LẦN không dời thêm — đây là chỗ mất sạch dữ liệu', () => {
  const goc = { micros: { 'DL:KSN4.B14': { pass: true, danhDau: 'x' } } };
  const mot = chuyenSo(goc);
  const hai = chuyenSo(mot);
  const ba = chuyenSo(hai);
  assert.ok(mot.micros['DL:KSN4.B19'], 'lần một phải dời');
  assert.deepEqual(hai.micros, mot.micros, 'lần hai KHÔNG được đụng gì');
  assert.deepEqual(ba.micros, mot.micros, 'lần ba cũng thế');
  assert.ok(daChuyen(mot) && mot[CO] === true);
});

test('bài NGOÀI dải và môn khác đi qua nguyên vẹn', () => {
  const goc = { micros: {
    'DL:KSN4.B01': { pass: true }, 'DL:KSN4.B12': { pass: true },
    'DL:KSN2.B20': { pass: true }, 'DL:TA1.B04': { pass: true },
  } };
  const sau = chuyenSo(goc).micros;
  for (const k of Object.keys(goc.micros)) assert.ok(sau[k], `${k} phải còn nguyên`);
});

test('huy hiệu CHƯƠNG không bị đụng — khoá chương không mang mã bài', () => {
  /* `chapters` khoá dạng `lop4.4` (mã quyển + số chương). Nhìn qua rất dễ tưởng nó
     mang mã bài rồi đi dời nhầm, làm hỏng huy hiệu chương của bé. */
  const goc = { micros: { 'DL:KSN4.B13': { pass: true } },
    chapters: { 'lop4.4': { pass: true, best: 9 } } };
  const sau = chuyenSo(goc);
  assert.deepEqual(sau.chapters, goc.chapters);
});

test('sổ CHƯA chuyển thì MỌI bản ghi đều là số cũ — dời hết, không giữ lại cái nào', () => {
  /* Bản đầu của phép kiểm này giả định bé có thể vừa có B13 cũ vừa có "B18 mới".
     KHÔNG THỂ: phép chuyển chạy ngay tại cửa nạp sổ, trước khi bất kỳ bản ghi nào
     theo số mới kịp được ghi. Nên một bản ghi ở B18 trong sổ chưa chuyển chính là
     B18 CŨ (THÊM MỘT SỐ VÀO NHÓM) và phải dời tiếp thành B23.
     Nhầm chỗ này thì bé mất đúng một bài, và mất im lặng. */
  const goc = { micros: {
    'DL:KSN4.B13': { pass: true, danhDau: 'B13 cũ' },
    'DL:KSN4.B18': { pass: true, danhDau: 'B18 cũ' },
  } };
  const sau = chuyenSo(goc).micros;
  assert.equal(sau['DL:KSN4.B18'].danhDau, 'B13 cũ', 'B13 cũ về đúng chỗ B18');
  assert.equal(sau['DL:KSN4.B23'].danhDau, 'B18 cũ', 'B18 cũ phải đi tiếp tới B23');
  assert.ok(!sau['DL:KSN4.B13'], 'mã cũ phải được dọn đi');
  assert.equal(Object.keys(sau).length, 2, 'không đẻ thêm cũng không mất bài nào');
});

test('cửa nạp sổ CÓ gọi phép chuyển — không thì cả tệp này vô dụng', () => {
  /* Viết đúng hàm mà quên cắm vào chỗ nạp thì mọi phép trên vẫn xanh, còn bé thì
     vẫn thấy huy hiệu gắn nhầm bài. Soi thẳng chỗ nối. */
  const src = readFileSync(new URL('../src/mon/toan/lib/progress.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(src, /import \{ chuyenSo \} from '\.\/donSoLop4\.js'/);
  assert.match(src, /return chuyenSo\(/, 'loadProgress phải trả về sổ ĐÃ chuyển');
});

test('dải dời khớp với công cụ dồn số bên tools', () => {
  /* Hai nơi cùng khai một dải: `tools/don_so_lop4.py` dồn NỘI DUNG, tệp này dồn
     TIẾN ĐỘ. Lệch nhau là bé và bài nói về hai bài khác nhau. */
  const py = readFileSync(new URL('../../tools/don_so_lop4.py', import.meta.url), 'utf8');
  const m = /DICH = (\d+)[\s\S]*?TU, DEN = (\d+), (\d+)/.exec(py);
  assert.ok(m, 'không đọc được dải trong don_so_lop4.py');
  assert.equal(Number(m[1]), DAI.dich, 'số chỗ dời lệch nhau');
  assert.equal(Number(m[2]), DAI.tu, 'đầu dải lệch nhau');
  assert.equal(Number(m[3]), DAI.den, 'cuối dải lệch nhau');
});
