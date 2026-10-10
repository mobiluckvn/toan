/**
 * CỔNG · BỘ NGƯỠNG — SO BA BẢN, và canh cơ chế chứ không canh con số.
 *
 * ── VÌ SAO TỆP NÀY TỒN TẠI ──
 * Ràng buộc R7 đưa 21 ngưỡng ra thành dữ liệu. Nhưng dữ liệu ấy phải có mặt ở BA
 * nơi: `data/nguong.json` (bản gốc người sửa đọc), `src/chung/lib/nguong.js` (máy
 * con), `functions/src/nguong.js` (máy chủ). Không import chéo được — xem chú thích
 * đầu hai tệp ấy.
 *
 * Ba bản thì sớm muộn lệch. Và lệch ở đây hỏng theo kiểu khó thấy nhất: BKT chấm
 * bằng θ này, màn hình quyết định bằng θ kia, không gì báo. Kho đã trả giá đúng kiểu
 * ấy một lần với `chula.js` ↔ `lib/chamviet.js`, nên lần này dựng cổng ngay từ đợt 1.
 *
 * ── VÀ MỘT CÁI BẪY RIÊNG CỦA VIỆC "ĐƯA NGƯỠNG RA DỮ LIỆU" ──
 * Nếu cổng ĐỌC bộ ngưỡng đang hành thì chuyên gia đổi θ là cổng vẫn xanh trong khi
 * hành vi đã khác — cổng tự chạy theo cấu hình thì nó không canh gì nữa. Nên tệp
 * này chỉ canh CƠ CHẾ (thang phạm vi, khoảng hợp lệ, ràng buộc chéo) và canh BA BẢN
 * KHỚP NHAU. Hành vi theo từng con số vẫn do 103 cổng cũ canh, với bộ MẶC ĐỊNH.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as con from '../src/chung/lib/nguong.js';
import * as may from '../functions/src/nguong.js';

const GOC = JSON.parse(readFileSync(new URL('../../data/nguong.json', import.meta.url), 'utf8'));

/* ═══════════ BA BẢN PHẢI KHỚP ═══════════ */

test('hai bản chép giống nhau TỪNG KÝ TỰ dưới khối chú thích đầu', () => {
  // Cắt từ SAU khối chú thích đầu tiên tới HẾT tệp. Dùng `split` theo dấu đóng
  // khối thì chỉ được một mẩu giữa hai dấu, tức bỏ qua phần lớn thân — cổng xanh
  // mà chẳng so gì. (Và viết dấu ấy vào trong một khối chú thích là tự đóng khối.)
  const than = (p) => {
    const s = readFileSync(new URL(p, import.meta.url), 'utf8');
    return s.slice(s.indexOf('*/') + 2);
  };
  assert.equal(than('../functions/src/nguong.js'), than('../src/chung/lib/nguong.js'),
    'thân hai tệp lệch nhau — sửa một bên thì phải sửa bên kia');
});

test('hai bản chép xuất ra cùng một bộ giá trị', () => {
  assert.deepEqual(may.MAC_DINH, con.MAC_DINH);
  assert.deepEqual(may.KHOANG, con.KHOANG);
  assert.deepEqual(may.THANG_PHAM_VI, con.THANG_PHAM_VI);
  assert.equal(may.PHIEN_BAN, con.PHIEN_BAN);
});

test('`data/nguong.json` khớp với mã: đủ 21 mã, cùng giá trị, cùng khoảng', () => {
  const ds = GOC.nguong;
  assert.equal(ds.length, 21, 'Bảng 3.19 có 21 ngưỡng');
  assert.deepEqual(ds.map((x) => x.ma).sort(), Object.keys(con.MAC_DINH).sort());
  for (const x of ds) {
    assert.deepEqual(con.MAC_DINH[x.ma], x.giaTri, `${x.ma}: giá trị lệch với bản gốc`);
    assert.deepEqual(con.KHOANG[x.ma], [x.canDuoi, x.canTren], `${x.ma}: khoảng lệch`);
  }
});

test('mỗi ngưỡng khai rõ nó đang nằm ở đâu trong mã', () => {
  /* Cột `oDau` là thứ giữ cho danh mục không trôi khỏi mã. Thiếu nó thì nửa năm
     sau không ai biết NG12 là hằng nào nữa. */
  for (const x of GOC.nguong) {
    assert.ok(String(x.oDau || '').trim(), `${x.ma}: thiếu trường oDau`);
  }
});

/* ═══════════ CƠ CHẾ: THANG PHẠM VI ═══════════ */

test('layNguong lấy ở phạm vi HẸP NHẤT có khai, rồi mới tới rộng hơn', () => {
  const bo = {
    macDinh: con.MAC_DINH,
    theoPhamVi: {
      nut: { v_g3_u1_how: { NG07: 0.95 } },
      khoiLop: { 3: { NG07: 0.80 } },
      toanHe: { NG07: 0.88 },
    },
  };
  assert.equal(con.layNguong(bo, 'NG07', { nut: 'v_g3_u1_how', khoiLop: 3 }), 0.95, 'nút thắng');
  assert.equal(con.layNguong(bo, 'NG07', { khoiLop: 3 }), 0.80, 'khối lớp thắng toàn hệ');
  assert.equal(con.layNguong(bo, 'NG07', {}), 0.88, 'không ngữ cảnh thì lấy toàn hệ');
  assert.equal(con.layNguong({ macDinh: con.MAC_DINH }, 'NG07', {}), 0.85, 'không khai thì mặc định');
});

test('thang phạm vi đúng thứ tự của mục 3.8.1, và `toanHe` đứng cuối', () => {
  assert.deepEqual(con.THANG_PHAM_VI.slice(-1), ['toanHe']);
  const i = (x) => con.THANG_PHAM_VI.indexOf(x);
  assert.ok(i('nut') < i('loaiNut'), 'nút hẹp hơn loại nút');
  assert.ok(i('loaiNut') < i('khoiLop'), 'loại nút hẹp hơn khối lớp');
  assert.ok(i('khoiLop') < i('mon'), 'khối lớp hẹp hơn môn');
});

test('hỏi một mã không có thì NÉM, không trả undefined trong im lặng', () => {
  assert.throws(() => con.layNguong(con.BO_MAC_DINH, 'NG99', {}));
});

/* ═══════════ CƠ CHẾ: KHOẢNG HỢP LỆ VÀ RÀNG BUỘC CHÉO ═══════════ */

test('bộ mặc định phải SẠCH — không thì cả hệ đang chạy ngoài khoảng của chính nó', () => {
  assert.deepEqual(con.soiNguong(con.BO_MAC_DINH), []);
});

test('giá trị ngoài khoảng bị bắt', () => {
  const loi = con.soiNguong({ macDinh: { ...con.MAC_DINH, NG09: 99 } });
  assert.ok(loi.some((x) => x.ma === 'NG09'), 'NG09 = 99 phải bị bắt');
});

test('ràng buộc θ_yếu ≤ θ − 0,20 bị bắt', () => {
  const loi = con.soiNguong({ macDinh: { ...con.MAC_DINH, NG07: 0.85, NG08: 0.70 } });
  assert.ok(loi.some((x) => x.ma === 'NG08' && /θ_yếu/.test(x.vi)));
});

test('P(S) và P(G) phải < 0,5, kể cả của câu bẫy', () => {
  assert.ok(con.soiNguong({ macDinh: { ...con.MAC_DINH, NG03: 0.6 } }).some((x) => x.ma === 'NG03'));
  assert.ok(con.soiNguong({ macDinh: { ...con.MAC_DINH, NG04: 0.6 } }).some((x) => x.ma === 'NG04'));
  const bay = { ...con.MAC_DINH, NG05: { slip: 0.6, guess: 0.15 } };
  assert.ok(con.soiNguong({ macDinh: bay }).some((x) => x.ma === 'NG05'));
});

test('soiNguong trả HẾT chỗ sai một lượt, không dừng ở chỗ đầu', () => {
  const loi = con.soiNguong({ macDinh: { ...con.MAC_DINH, NG09: 99, NG12: 9 } });
  assert.ok(loi.filter((x) => ['NG09', 'NG12'].includes(x.ma)).length >= 2);
});
