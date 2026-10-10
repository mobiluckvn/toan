import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { sinhNhatKy, nhipDay, taoNgauNhien, MAC_DINH } from '../functions/src/moPhongHoc.js';
import { hocNuaDoi, quetLuoiTheta, hocBKT } from '../functions/src/hocNguong.js';
import { BO_MAC_DINH, KHOANG, layNguong } from '../functions/src/nguong.js';

/**
 * NGƯỜI HỌC MÔ PHỎNG — kịch bản KB1 (Bảng 3.24).
 *
 * ⚠ HAI THỨ KHỐI CỔNG NÀY CANH, VÀ CHÚNG QUAN TRỌNG HƠN «HÀM CHẠY ĐƯỢC KHÔNG»:
 *
 *   1. Dữ liệu mô phỏng KHÔNG được lẫn vào dữ liệu thật. Lẫn vào thì mọi chỉ số
 *      của Bảng 3.22 nói về một đám trẻ không tồn tại, và nhật ký là BẤT BIẾN nên
 *      không có đường lùi.
 *
 *   2. Thế giới mô phỏng phải CÓ CHỖ ĐỂ SAI. Bản đầu của `moPhongHoc.js` không cho
 *      trẻ quên, và KB1 chạy trên nó cho NG06 = 60 với NG07 = 0,70 — cả hai đụng
 *      BIÊN của khoảng hợp lệ. Hai con số đụng biên không phải kết quả hiệu chỉnh;
 *      chúng là lời khai rằng mô phỏng không nói được gì về hai ngưỡng ấy.
 */

const nhomCua = (l) => {
  const m = new Map();
  for (const a of l) {
    const k = `${a.learnerId}::${a.bktUnit}`;
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(a);
  }
  return m;
};

/* ── 1 · KHÔNG LẪN VÀO DỮ LIỆU THẬT ─────────────────────────────────────── */

test('mọi lượt mô phỏng tự khai `moPhong: true`', () => {
  /* Nếu một ngày có ai ghi chúng xuống thì ít nhất còn lọc ra được. */
  const l = sinhNhatKy(BO_MAC_DINH, { soBe: 5 });
  assert.ok(l.length > 0);
  for (const a of l) assert.equal(a.moPhong, true);
});

test('mã người học và mã nút mang tiền tố riêng, không đụng mã thật', () => {
  const l = sinhNhatKy(BO_MAC_DINH, { soBe: 5 });
  for (const a of l) {
    assert.match(a.learnerId, /^mp_/, `mã bé mô phỏng trùng dạng mã thật: ${a.learnerId}`);
    assert.match(a.bktUnit, /^mp_nut_/, `mã nút mô phỏng trùng dạng mã thật: ${a.bktUnit}`);
  }
});

test('⚠ TỆP MÔ PHỎNG KHÔNG ĐƯỢC ĐỤNG FIRESTORE', () => {
  /* Chốt lớn nhất, và nó đọc mã nguồn vì đó là cách duy nhất canh được «tệp này
     không có khả năng ghi». Một lời gọi `db.collection(...)` lọt vào đây là mở
     đường cho nhật ký mô phỏng trôi vào kho thật. */
  const src = readFileSync(new URL('../functions/src/moPhongHoc.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  for (const cam of ['firebase-admin', 'getFirestore', 'db.', 'collection(', 'doc(']) {
    assert.ok(!src.includes(cam), `moPhongHoc.js có nhắc tới \`${cam}\``);
  }
});

/* ── 2 · THẾ GIỚI MÔ PHỎNG CÓ CHỖ ĐỂ SAI ────────────────────────────────── */

test('⚠ CHU KỲ BÁN RÃ HỌC RA PHẢI TĂNG THEO CHU KỲ THẬT', () => {
  /* Đây là phép thử có giá trị nhất của cả KB1: thế giới quên nhanh hơn thì `h`
     học ra phải nhỏ hơn. Không có tính chất này thì quét lưới chỉ đang đọc một
     hằng số nào đó của phép dựng, chứ không đo thế giới.
     ⚠ KHÔNG đòi khớp CHÍNH XÁC: mô phỏng cho trạng thái ẩn ĐẢO về «chưa thạo», còn
     `quenDan` của hệ thống kéo `p` về 0,5 — hai hình dạng quên khác nhau, nên con
     số học ra không phải con số thật. Tính chất đơn điệu mới là thứ đúng. */
  const ra = [3, 7, 14].map((h) => {
    const l = sinhNhatKy(BO_MAC_DINH, { soBe: 400, nuaDoiThat: h, seed: 99 });
    return { that: h, hoc: hocNuaDoi(nhomCua(l), BO_MAC_DINH).h };
  });
  for (let i = 1; i < ra.length; i += 1) {
    assert.ok(ra[i].hoc > ra[i - 1].hoc,
      `h học ra không tăng theo h thật: ${JSON.stringify(ra)}`);
  }
  const [lo, hi] = KHOANG.NG06;
  for (const x of ra) {
    assert.ok(x.hoc > lo && x.hoc < hi,
      `h = ${x.hoc} đụng biên khoảng [${lo}, ${hi}] — mô phỏng không nói được gì về NG06`);
  }
});

test('⚠ CHU KỲ BÁN RÃ DÀI HƠN CỬA SỔ QUAN SÁT thì KHÔNG đo được', () => {
  /* Một giới hạn thật, ghi lại để không ai đọc nhầm kết quả KB1. Với ~3 buổi trải
     6 ngày, một thế giới quên với h = 30 gần như không để lại dấu vết nào — và
     phép quét lưới chững lại quanh 19, không với tới 30. Muốn hiệu chỉnh một chu
     kỳ dài thì phải mô phỏng một quãng học dài hơn. */
  const dai = sinhNhatKy(BO_MAC_DINH, { soBe: 400, nuaDoiThat: 30, seed: 99 });
  const h30 = hocNuaDoi(nhomCua(dai), BO_MAC_DINH).h;
  assert.ok(h30 < 30, `bất ngờ đo tới được h = 30 (ra ${h30}) — nếu thật thì sửa chú thích này`);
});

test('θ quét ra KHÔNG đụng biên khoảng hợp lệ', () => {
  /* θ dính đáy nghĩa là công nhận sớm không bao giờ phải trả giá — tức thế giới
     mô phỏng không có ai quên, và θ không có gì để phân xử. */
  const l = sinhNhatKy(BO_MAC_DINH, { soBe: 400, seed: 7 });
  const q = quetLuoiTheta(nhomCua(l), BO_MAC_DINH);
  const [lo, hi] = KHOANG.NG07;
  assert.ok(q.theta > lo && q.theta < hi, `θ đụng biên: ${q.theta} trong [${lo}, ${hi}]`);
});

test('thời gian trả lời KHÁC NHAU theo dạng câu', () => {
  /* Dữ liệu THẬT chênh gấp chín lần giữa các dạng (chon 30,5 giây · bieuthuc
     269,6). Một mô phỏng cho mọi dạng cùng một con số thì không dùng để hiệu chỉnh
     NG16 được — nó sẽ đề xuất một ngưỡng chung, đúng cái sai ta vừa bỏ. */
  const l = sinhNhatKy(BO_MAC_DINH, { soBe: 200, seed: 11 });
  const tb = {};
  for (const a of l) {
    const o = tb[a.mode] || (tb[a.mode] = { tong: 0, n: 0 });
    o.tong += a.ms; o.n += 1;
  }
  const ds = Object.entries(tb).map(([k, v]) => [k, v.tong / v.n]);
  assert.ok(ds.length >= 3, 'phải sinh nhiều dạng câu');
  const giay = ds.map(([, v]) => v);
  assert.ok(Math.max(...giay) / Math.min(...giay) > 2,
    `các dạng câu quá giống nhau: ${JSON.stringify(ds.map(([k, v]) => [k, Math.round(v / 1000)]))}`);
});

/* ── 3 · TÍNH CHẤT CHUNG ────────────────────────────────────────────────── */

test('sinh TẤT ĐỊNH — cùng hạt giống, cùng nhật ký', () => {
  /* Hai lần chạy ra hai tập khác nhau thì không ai tái tạo lại được kết quả KB1,
     và một đề xuất đã duyệt không truy ngược về dữ liệu sinh ra nó. */
  const a = sinhNhatKy(BO_MAC_DINH, { soBe: 20, seed: 5 });
  const b = sinhNhatKy(BO_MAC_DINH, { soBe: 20, seed: 5 });
  assert.deepEqual(a, b);
  const c = sinhNhatKy(BO_MAC_DINH, { soBe: 20, seed: 6 });
  assert.notDeepEqual(a, c, 'đổi hạt giống mà ra y hệt — bộ sinh không dùng hạt giống');
  assert.equal(taoNgauNhien(3)(), taoNgauNhien(3)());
});

test('EM tìm lại được bộ tham số đã sinh ra thế giới mô phỏng', () => {
  /* Khép vòng: mô phỏng dựng từ bộ ngưỡng, rồi EM đọc lại nhật ký và phải tìm ra
     xấp xỉ chính bộ ấy. Lệch nhiều thì hoặc bộ sinh sai, hoặc EM sai — và cả hai
     đều làm mọi kết quả KB1 vô nghĩa. */
  const l = sinhNhatKy(BO_MAC_DINH, {
    soBe: 500, seed: 31, dangCau: ['chon'], bac: [1], nuaDoiThat: 1e9,
  });
  const em = hocBKT([...nhomCua(l).values()].map((c) => c.map((x) => x.correct)));
  for (const [ma, k] of [['NG01', 'L0'], ['NG03', 'slip'], ['NG04', 'guess']]) {
    const that = layNguong(BO_MAC_DINH, ma, { dangCau: 'chon', bac: '1' });
    assert.ok(Math.abs(em[k] - that) < 0.06,
      `${ma}: sinh bằng ${that}, EM đọc ra ${em[k].toFixed(3)}`);
  }
});

test('nhịp dạy: θ cao hơn thì tốn NHIỀU CÂU hơn và công nhận ÍT nút hơn', () => {
  const l = sinhNhatKy(BO_MAC_DINH, { soBe: 300, seed: 17 });
  const thap = nhipDay(l, BO_MAC_DINH, 0.75);
  const cao = nhipDay(l, BO_MAC_DINH, 0.95);
  assert.ok(cao.soCauToiThao > thap.soCauToiThao, 'θ cao mà tốn ít câu hơn');
  assert.ok(cao.tiLeDuocCongNhan < thap.tiLeDuocCongNhan, 'θ cao mà công nhận nhiều nút hơn');
});

test('số bé mặc định đúng con số KB1 của Bảng 3.24', () => {
  assert.equal(MAC_DINH.soBe, 1000, 'Bảng 3.24 khai 1.000 người học mô phỏng');
});
