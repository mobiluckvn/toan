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
import { maMoi, chuyenSo, daChuyen, daChay, DOT, CO } from '../src/mon/toan/lib/donSoLop4.js';


/** Đích cuối của một mã sau KHI qua hết mọi đợt — tính bằng chính DOT, không gõ số.
    Gõ số thì thêm một đợt là phải sửa tay khắp tệp, và sửa sót thì cổng nói dối. */
const dichCuoi = (id) => DOT.reduce((x, d) => maMoi(x, d), id);

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

test('MỌI ĐƯỜNG ĐỀU HỘI TỤ — bé chạy đợt 1 rồi hay chưa cũng về cùng một chỗ', () => {
  /* ⚠ Đây là phép kiểm quan trọng nhất của tệp, và là lý do phải đổi cờ đúng/sai
     thành ĐẾM ĐỢT. Bản cũ chỉ có một cờ `true`: bé chạy đợt 1 rồi thì cờ bật, và
     đợt 2 KHÔNG BAO GIỜ chạy cho bé ấy — tiến độ đứng yên trong khi bài đã dời.

     Ba đường phải cùng đích: bé chưa chạy đợt nào · bé mang cờ `true` của bản cũ ·
     bé đã lưu số đợt. */
  const dich = (so) => Object.keys(chuyenSo(so).micros)[0];
  // B14 gốc: qua đợt 1 thành B19, qua đợt 2 thành B24
  const goc = 'DL:KSN4.B14';
  const cuoi = dichCuoi(goc);                       // đích sau KHI qua hết mọi đợt
  const sauDot1 = maMoi(goc, DOT[0]);               // bé đã chạy đợt 1 đang ở đây
  assert.equal(dich({ micros: { [goc]: { x: 1 } } }), cuoi, 'bé chưa chạy đợt nào');
  assert.equal(dich({ micros: { [sauDot1]: { x: 1 } }, [CO]: true }), cuoi,
    'bé mang cờ true của bản cũ — phải hiểu là đã xong đợt 1');
  assert.equal(dich({ micros: { [sauDot1]: { x: 1 } }, [CO]: 1 }), cuoi,
    'bé đã lưu số đợt');
  assert.equal(dich({ micros: { [cuoi]: { x: 1 } }, [CO]: DOT.length }), cuoi,
    'đã chạy đủ thì đứng yên');
});

test('CỜ CŨ `true` phải được hiểu là ĐÃ XONG ĐỢT 1, không phải xong hết', () => {
  /* Hiểu nhầm thành "xong hết" thì bé chạy đợt 1 rồi sẽ không bao giờ được dời tiếp.
     Hiểu nhầm thành "chưa chạy gì" thì bé bị dời HAI LẦN và mất sạch. */
  assert.equal(daChay({ [CO]: true }), 1);
  assert.equal(daChay({ [CO]: 2 }), 2);
  assert.equal(daChay({}), 0);
  assert.equal(daChay(null), 0);
});

test('dời đi từ số LỚN xuống — không dồn hai lần', () => {
  /* Đây là cái bẫy kinh điển của mọi phép đánh số lại: dời B13→B18 trước thì tới
     lượt B18 (vừa mới thành) lại bị dời tiếp thành B23. Đưa cả dải vào một lúc để
     bắt đúng chuyện ấy. */
  const micros = {};
  for (let n = DOT[0].tu; n <= DOT[0].den; n += 1) {
    micros[`DL:KSN4.B${String(n).padStart(2, '0')}`] = { pass: true, danhDau: n };
  }
  const sau = chuyenSo({ micros }).micros;
  assert.equal(Object.keys(sau).length, DOT[0].den - DOT[0].tu + 1, 'không được mất bài nào');
  for (let n = DOT[0].tu; n <= DOT[0].den; n += 1) {
    const k = dichCuoi(`DL:KSN4.B${String(n).padStart(2, '0')}`);
    assert.ok(sau[k], `thiếu ${k}`);
    assert.equal(sau[k].danhDau, n, `${k} phải mang đúng bản ghi của B${n}, không phải bài khác`);
  }
});

test('CHẠY HAI LẦN không dời thêm — đây là chỗ mất sạch dữ liệu', () => {
  const goc = { micros: { 'DL:KSN4.B14': { pass: true, danhDau: 'x' } } };
  const mot = chuyenSo(goc);
  const hai = chuyenSo(mot);
  const ba = chuyenSo(hai);
  assert.ok(mot.micros[dichCuoi('DL:KSN4.B14')], 'lần một phải dời qua ĐỦ mọi đợt');
  assert.deepEqual(hai.micros, mot.micros, 'lần hai KHÔNG được đụng gì');
  assert.deepEqual(ba.micros, mot.micros, 'lần ba cũng thế');
  /* Cờ nay giữ SỐ ĐỢT đã chạy, không phải `true`. Bản cũ so với `true` —
     để nguyên thì phép kiểm này xanh mãi kể cả khi cờ sai. */
  assert.ok(daChuyen(mot), 'phải đánh dấu đã chạy đủ');
  assert.equal(mot[CO], DOT.length, 'cờ phải bằng số đợt đã chạy');
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
  assert.equal(sau[dichCuoi('DL:KSN4.B13')].danhDau, 'B13 cũ');
  assert.equal(sau[dichCuoi('DL:KSN4.B18')].danhDau, 'B18 cũ');
  assert.notEqual(dichCuoi('DL:KSN4.B13'), dichCuoi('DL:KSN4.B18'),
    'hai bài khác nhau không được rơi vào cùng một chỗ');
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

test('ĐÓNG BĂNG: không được thêm đợt dồn nào nữa', () => {
  /* Bản cũ so dải ở đây với `tools/don_so_lop4.py`. Công cụ ấy đã bỏ: bác chốt lối
     C, mã bài từ nay đứng yên mãi và số hiển thị đếm từ vị trí, nên KHÔNG CÒN đợt
     dồn nào cần chạy nữa.

     Phần chuyển dưới đây vẫn phải sống, vì bé nào chưa mở app từ trước đợt 1 thì sổ
     trong máy vẫn mang mã cũ và vẫn cần dời một lần. Nhưng nó đông cứng tại đây.

     Thêm một dòng vào DOT là dấu hiệu ai đó lại đi dồn số — việc mà lối C sinh ra để
     khỏi phải làm. Đỏ ở đây rẻ hơn nhiều so với dời nhầm tiến độ của các bé. */
  assert.equal(DOT.length, 1,
    'DOT phải đứng nguyên một đợt. Cần chèn bài mới thì thêm dòng vào '
    + 'data/lop4/thu_tu.json, đừng dồn số.');
  assert.deepEqual(DOT[0], { tu: 13, den: 44, dich: 5 },
    'đợt 1 đã chạy thật trên máy các bé — sửa dải này là sổ của bé lệch đi');
});
