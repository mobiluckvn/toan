/**
 * CỔNG · XẾP CÂU THEO VÙNG PHÁT TRIỂN GẦN (ZPD).
 *
 * Đợt 1 mới GHI được P(L) vào `mastery`. Ghi mà không ai đọc thì bé vẫn học y hệt
 * như trước — con số nằm trong Firestore không đổi được một buổi học nào. Đây là
 * phần ĐỌC, và cổng này canh ba chuyện, cả ba đều hỏng lặng lẽ nếu sai:
 *
 *  1. KHÔNG BỎ CÂU NÀO. Chỉ đổi thứ tự. Thanh đếm câu, sổ tiến độ và phép chấm
 *     đều dựa trên SỐ CÂU — bớt một câu là lệch hết, mà lệch thì không có gì đỏ.
 *  2. KHÔNG ĐỘNG VÀO KHI CHƯA CÓ SỐ. Bé chưa đăng nhập, mất mạng, hay hàm nền
 *     chưa chạy — cả ba đều phải cho ra ĐÚNG thứ tự cũ.
 *  3. "CHƯA CÓ TIN" KHÔNG PHẢI "BÉ RẤT YẾU". Coi `p` thiếu thành 0 là xếp nhầm
 *     cả nhóm chưa học xuống cuối buổi.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  xepTheoZPD, nhomCua, mucThaoCua, nutChongChenh, NHOM, NGUONG_THAO, NGUONG_YEU,
} from '../src/mon/tienganh/lib/zpd.js';
import { MASTERY_THRESHOLD } from '../functions/src/bkt.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');

const cau = (id, maNut) => ({ id, maNut });
const mt = (o) => Object.fromEntries(Object.entries(o).map(([k, p]) => [k, { p }]));

test('ngưỡng thạo khớp với máy chủ — hai nơi hai số là hai hệ thống khác nhau', () => {
  assert.equal(NGUONG_THAO, MASTERY_THRESHOLD);
});

test('phân nhóm đúng bốn vùng', () => {
  assert.equal(nhomCua(0.5), NHOM.chongChenh);
  assert.equal(nhomCua(NGUONG_THAO), NHOM.daThao);
  assert.equal(nhomCua(0.99), NHOM.daThao);
  assert.equal(nhomCua(NGUONG_YEU - 0.01), NHOM.yeu);
  assert.equal(nhomCua(NGUONG_YEU), NHOM.chongChenh, 'đúng ngưỡng thì đã vào vùng học được');
});

test('⚠ "chưa có tin" KHÔNG phải "bé rất yếu"', () => {
  for (const x of [null, undefined, NaN, 'abc', {}]) {
    assert.equal(nhomCua(x), NHOM.chuaBiet,
      `p=${JSON.stringify(x)} bị xếp nhầm — coi "chưa có tin" thành "yếu" là đẩy `
      + 'cả nhóm bé chưa học xuống cuối buổi');
  }
  assert.notEqual(nhomCua(null), nhomCua(0));
});

test('xếp: chông chênh → chưa biết → yếu → đã thạo', () => {
  const ds = [
    cau('a', 'v_thao'), cau('b', 'v_yeu'), cau('c', 'v_moi'), cau('d', 'v_chenh'),
  ];
  const m = mt({ v_thao: 0.95, v_yeu: 0.05, v_chenh: 0.5 });   // v_moi không có số
  assert.deepEqual(xepTheoZPD(ds, m).map((c) => c.id), ['d', 'c', 'b', 'a']);
});

test('⚠ YẾU HẲN xếp SAU chông chênh, không phải trước', () => {
  /* Mở đầu buổi bằng ba câu bé chắc chắn sai thì bé nghỉ. Chỗ ấy cần bài PHỤ ĐẠO
     (Đợt 4), không phải thêm lượt luyện cùng kiểu. */
  const ds = [cau('yeu', 'v_yeu'), cau('chenh', 'v_chenh')];
  const r = xepTheoZPD(ds, mt({ v_yeu: 0.05, v_chenh: 0.6 }));
  assert.equal(r[0].id, 'chenh');
});

test('⚠ KHÔNG BỎ CÂU NÀO — chỉ đổi thứ tự', () => {
  const ds = Array.from({ length: 12 }, (_, i) => cau(`c${i}`, `v_${i}`));
  const m = mt(Object.fromEntries(ds.map((c, i) => [`v_${i}`, (i % 10) / 10])));
  const r = xepTheoZPD(ds, m);
  assert.equal(r.length, ds.length, 'mất câu → thanh đếm câu và phép chấm lệch hết');
  assert.deepEqual([...r].map((c) => c.id).sort(), [...ds].map((c) => c.id).sort());
});

test('ỔN ĐỊNH trong từng nhóm — giữ thứ tự người soạn đặt', () => {
  const ds = [cau('a', 'v1'), cau('b', 'v2'), cau('c', 'v3')];
  const m = mt({ v1: 0.5, v2: 0.5, v3: 0.5 });     // cùng nhóm hết
  assert.deepEqual(xepTheoZPD(ds, m).map((c) => c.id), ['a', 'b', 'c']);
});

test('⚠ CHƯA CÓ SỐ thì trả về ĐÚNG mảng cũ', () => {
  const ds = [cau('a', 'v1'), cau('b', 'v2')];
  assert.equal(xepTheoZPD(ds, null), ds, 'phải là chính mảng cũ, không phải bản sao');
  assert.equal(xepTheoZPD(ds, {}), ds);
  /* Có sổ nhưng KHÔNG nút nào của bài này có số → cũng đừng động vào. */
  assert.equal(xepTheoZPD(ds, mt({ v_khac: 0.5 })), ds);
  assert.deepEqual(xepTheoZPD([], mt({ v1: 0.5 })), []);
});

test('câu thiếu maNut không làm hỏng phép xếp', () => {
  const ds = [{ id: 'a' }, cau('b', 'v_chenh'), null];
  const r = xepTheoZPD(ds, mt({ v_chenh: 0.5 }));
  assert.equal(r.length, 3);
  assert.equal(r[0].id, 'b', 'câu có số và đang chông chênh phải lên đầu');
});

test('tra mức thạo chịu được cả hai dạng khoá', () => {
  assert.equal(mucThaoCua({ 'v_g5_u1_city': { p: 0.7 } }, 'v_g5_u1_city'), 0.7);
  assert.equal(mucThaoCua({ [encodeURIComponent('a b')]: { p: 0.4 } }, 'a b'), 0.4);
  assert.equal(mucThaoCua({}, 'v_x'), null);
  assert.equal(mucThaoCua(null, null), null);
  assert.equal(mucThaoCua({ v_x: { p: 'hong' } }, 'v_x'), null);
});

test('nút chông chênh nhất đứng trước', () => {
  const r = nutChongChenh(mt({ a: 0.8, b: 0.35, c: 0.95, d: 0.1, e: 0.6 }));
  assert.deepEqual(r.map((x) => x.ma), ['b', 'e', 'a'],
    'đã thạo và yếu hẳn đều không thuộc vùng học được');
});

test('màn học có gọi phép xếp, và gọi TRONG useMemo', () => {
  /* ⚠ Không dùng useMemo thì thứ tự dựng lại mỗi lần màn vẽ. Bé đang làm câu thứ
     3, một lần vẽ lại là `i` vẫn bằng 3 nhưng pool đã khác — câu đang làm dở biến
     mất và một câu khác nhảy vào chỗ đó. Không có gì đỏ, chỉ bé thấy lạ. */
  const ma = chiMa(doc('../src/mon/tienganh/components/BaiHoc.jsx'));
  assert.match(ma, /xepTheoZPD/, 'màn học không dùng phép xếp — P(L) ghi ra rồi bỏ đó');
  const i = ma.indexOf('xepTheoZPD(bai.practice.pools');
  assert.notEqual(i, -1);
  assert.match(ma.slice(Math.max(0, i - 200), i), /useMemo/,
    'phép xếp không nằm trong useMemo — thứ tự đổi giữa buổi thì bé mất câu đang làm dở');

  const man = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(man, /docMucThao\(/, 'không ai nạp mức thạo từ máy chủ');
});
