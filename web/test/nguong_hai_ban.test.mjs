/**
 * CỔNG · BỘ NGƯỠNG — SO BA BẢN, và canh cơ chế chứ không canh con số.
 *
 * ── VÌ SAO TỆP NÀY TỒN TẠI ──
 * Ràng buộc R7 đưa 21 ngưỡng ra thành dữ liệu (từ 22-11-2026 là 30 — Bảng 4.7).
 * Nhưng dữ liệu ấy phải có mặt ở BA
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

test('`data/nguong.json` khớp với mã: đủ 30 mã, cùng giá trị, cùng khoảng', () => {
  const ds = GOC.nguong;
  /* 21 ngưỡng của Bảng 3.19, cộng NG22–NG30 thêm 22-11-2026 (Bảng 4.7, điểm 5) — hằng
     số trước đây gõ cứng trong mã. */
  assert.equal(ds.length, 30, 'Bảng 3.19 có 21 ngưỡng, cộng 9 ngưỡng của Bảng 4.7');
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

/* ═══════════ NHỊP TINH THÔNG — Bảng 3.21, và luật chỉ CODE mới bắt được ═══════════ */

test('mã tái tạo ĐÚNG Bảng 3.21 của luận văn', () => {
  /* Đây là chỗ buộc mã và luận văn vào nhau. Luận văn in bốn dòng ấy từ "Thuật toán
     3.1 chạy trực tiếp"; nếu một ngày tham số BKT đổi mà bảng trong luận văn không
     đổi theo, cổng này đỏ — chứ không phải sáu tháng sau mới có người đọc ra. */
  const BANG = [
    { theta: 0.80, soCau: 3, mucKhiDat: 0.837, sauKhiSai: 0.470 },
    { theta: 0.85, soCau: 4, mucKhiDat: 0.944, sauKhiSai: 0.730 },
    { theta: 0.90, soCau: 4, mucKhiDat: 0.944, sauKhiSai: 0.730 },
    { theta: 0.95, soCau: 5, mucKhiDat: 0.982, sauKhiSai: 0.896 },
  ];
  for (const d of BANG) {
    const bo = { macDinh: { ...con.MAC_DINH, NG07: d.theta } };
    const r = con.nhipTinhThong(bo);
    assert.equal(r.soCau, d.soCau, `θ=${d.theta}: số câu lệch với Bảng 3.21`);
    assert.equal(+r.mucKhiDat.toFixed(3), d.mucKhiDat, `θ=${d.theta}: mức khi đạt lệch`);
    assert.equal(+r.sauKhiSai.toFixed(3), d.sauKhiSai, `θ=${d.theta}: sau khi sai lệch`);
  }
});

test('θ 0,85 và 0,90 cho CÙNG một nhịp — điều chỉ bảng này mới nói ra', () => {
  const nhip = (t) => con.nhipTinhThong({ macDinh: { ...con.MAC_DINH, NG07: t } }).soCau;
  assert.equal(nhip(0.85), nhip(0.90),
    'mất tính chất này thì lập luận "đổi θ từ 0,85 lên 0,90 không đổi gì" sai');
  assert.ok(nhip(0.80) < nhip(0.85), 'hạ θ phải cần ít câu hơn');
});

test('một bộ mà TỪNG ngưỡng đều hợp lệ vẫn có thể cho nhịp vô lý', () => {
  /* Chính là lý do phép kiểm thứ ba tồn tại: khoảng hợp lệ soi từng con số một,
     không thấy được hậu quả của việc GHÉP chúng lại. */
  const bo = { macDinh: { ...con.MAC_DINH, NG07: 0.70, NG02: 0.40 } };
  for (const ma of ['NG07', 'NG02']) {
    const [d, t] = con.KHOANG[ma];
    assert.ok(bo.macDinh[ma] >= d && bo.macDinh[ma] <= t, `${ma} vẫn trong khoảng`);
  }
  const loi = con.soiNguong(bo);
  assert.ok(loi.some((x) => /nhịp tinh thông/.test(x.vi)), 'phải bắt được nhịp 2 câu');
});

test('công thức BKT chỉ có MỘT bản — bkt.js gọi xuống nguong.js', () => {
  const s = readFileSync(new URL('../functions/src/bkt.js', import.meta.url), 'utf8');
  assert.match(s, /capNhatBKT\(/, 'bktUpdate phải gọi xuống bản dùng chung');
  assert.doesNotMatch(s, /1 - slip\)\) \/ \(/, 'bkt.js còn giữ công thức riêng → hai bản sẽ trôi');
});

test('bktUpdate của máy chủ và capNhatBKT cho CÙNG kết quả', async () => {
  const b = await import('../functions/src/bkt.js');
  const ts = con.thamSoBKT(con.BO_MAC_DINH);
  for (const p of [0.1, 0.3, 0.5, 0.85, 0.99]) {
    for (const dung of [true, false]) {
      assert.equal(b.bktUpdate(p, dung), con.capNhatBKT(p, dung, ts));
    }
  }
});

/* ═══════════ LUẬT FIRESTORE CHO BỐN BẢNG ═══════════ */

test('luật khai đủ bốn bảng ngưỡng và vai trò chuyên gia', () => {
  const r = readFileSync(new URL('../firestore.rules', import.meta.url), 'utf8');
  assert.match(r, /function isChuyenGia\(\)/, 'thiếu vai trò thứ tư');
  for (const bang of ['nguong', 'nguong_lich_su', 'nguong_de_xuat', 'thong_ke_nguong']) {
    assert.match(r, new RegExp(`match /${bang}/`), `thiếu luật cho bảng ${bang}`);
  }
});

test('lịch sử ngưỡng CHỈ THÊM, và đề xuất thì máy con không tạo được', () => {
  const r = readFileSync(new URL('../firestore.rules', import.meta.url), 'utf8');
  /* Cắt TỪ SAU tiêu đề khối, không cắt từ chính nó — lát cắt bắt đầu bằng
     `match /` thì `split` trả về một mẩu rỗng, và cổng khẳng định trên chuỗi rỗng
     là cổng không khẳng định gì. */
  const khoi = (ten) => {
    const dau = r.indexOf(`match /${ten}/`);
    assert.ok(dau > -1, `không thấy khối ${ten}`);
    return r.slice(dau + `match /${ten}/`.length).split('match /')[0];
  };
  assert.match(khoi('nguong_lich_su'), /allow update, delete: if false/,
    'sửa hay xoá được lịch sử thì nó không còn là bằng chứng');
  assert.match(khoi('nguong_de_xuat'), /allow create, delete: if false/,
    'máy con tạo được đề xuất thì "máy học ra" thành chỗ nhập tay');
  assert.match(khoi('thong_ke_nguong'), /allow write: if false/);
});
