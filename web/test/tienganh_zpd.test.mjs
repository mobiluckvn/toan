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
import { TOI_THIEU_MAU } from '../src/mon/tienganh/lib/hoso.js';
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

/* ── CHIỀU SƯ PHẠM: định dạng làm khoá xếp PHỤ ─────────────────────────────── */

const cauD = (id, maNut, format) => ({ id, maNut, format });
/** hồ sơ định dạng: {format: tỉ lệ đúng}, tự bơm cho đủ mẫu */
const hs = (o) => Object.fromEntries(Object.entries(o).map(([k, ti]) => [k, {
  tong: TOI_THIEU_MAU * 4, dung: Math.round(TOI_THIEU_MAU * 4 * ti),
}]));

test('chỗ CHÔNG CHÊNH: định dạng bé MẠNH lên trước', () => {
  /* Nội dung đã khó rồi; chồng thêm dạng câu bé cũng vật vã là bắt bé đánh nhau
     với hai thứ cùng lúc, và khi sai thì không ai biết bé sai vì chưa hiểu bài
     hay vì chưa quen cách hỏi. */
  const ds = [cauD('yeu', 'v_a', 'go'), cauD('manh', 'v_b', 'chon')];
  const m = mt({ v_a: 0.5, v_b: 0.5 });                     // cùng nhóm chông chênh
  const r = xepTheoZPD(ds, m, hs({ chon: 0.9, go: 0.3 }));
  assert.equal(r[0].id, 'manh');
});

test('chỗ ĐÃ THẠO: đảo chiều — định dạng bé YẾU lên trước', () => {
  /* Nội dung an toàn nên đây là chỗ RẺ NHẤT để tập cách hỏi bé còn ngại. */
  const ds = [cauD('manh', 'v_a', 'chon'), cauD('yeu', 'v_b', 'go')];
  const m = mt({ v_a: 0.95, v_b: 0.95 });
  const r = xepTheoZPD(ds, m, hs({ chon: 0.9, go: 0.3 }));
  assert.equal(r[0].id, 'yeu');
});

test('⚠ ĐỊNH DẠNG CHỈ LÀ KHOÁ PHỤ — nhóm ZPD vẫn quyết trước', () => {
  /* Cho định dạng thắng nhóm là đảo ngược cả mục đích của việc xếp.
     ⚠ CHỌN CA CHO ĐÚNG. Bản đầu tôi so nhóm ĐÃ THẠO với nhóm CHÔNG CHÊNH — ca ấy
     KHÔNG phân biệt được: nhóm đã thạo đảo chiều nên `d` của nó luôn ≥ 0, còn hai
     nhóm kia luôn ≤ 0, hai dải không chồng nhau, đổi thứ tự khoá cũng ra kết quả
     y hệt. Đảo chiều thử mới lộ ra là phép canh đang canh hụt.
     Ca phân biệt được phải nằm giữa hai nhóm CÙNG dấu: chưa-biết (1) và yếu (2). */
  const ds = [
    cauD('yeu_hopDang', 'v_yeu', 'chon'),      // nhóm 2, định dạng rất mạnh
    cauD('moi_khoDang', 'v_moi', 'go'),        // nhóm 1, định dạng yếu
  ];
  const m = mt({ v_yeu: 0.05 });               // v_moi không có số → chưa biết
  const r = xepTheoZPD(ds, m, hs({ chon: 0.95, go: 0.2 }));
  assert.equal(r[0].id, 'moi_khoDang',
    'nhóm phải quyết trước: thứ bé CHƯA BIẾT đứng trên thứ bé YẾU HẲN, kể cả khi '
    + 'thứ yếu hẳn kia rơi vào dạng câu bé làm tốt nhất');
});

test('hồ sơ CHƯA ĐỦ MẪU thì không xê dịch gì', () => {
  const ds = [cauD('a', 'v_a', 'go'), cauD('b', 'v_b', 'chon')];
  const m = mt({ v_a: 0.5, v_b: 0.5 });
  const it = { chon: { dung: 2, tong: 2 }, go: { dung: 0, tong: 2 } };
  assert.deepEqual(xepTheoZPD(ds, m, it).map((c) => c.id), ['a', 'b']);
  /* Và MỘT dạng đủ mẫu cũng chưa đủ — mọi câu cùng hạng thì xếp lại chẳng đổi gì. */
  const mot = hs({ chon: 0.9 });
  assert.deepEqual(xepTheoZPD(ds, m, mot).map((c) => c.id), ['a', 'b']);
});

test('có hồ sơ định dạng mà CHƯA có mức thạo thì vẫn dùng được', () => {
  const ds = [cauD('yeu', null, 'go'), cauD('manh', null, 'chon')];
  const r = xepTheoZPD(ds, null, hs({ chon: 0.9, go: 0.3 }));
  assert.equal(r[0].id, 'manh', 'chưa biết nội dung thì ít ra chọn được cách hỏi');
});

test('câu thiếu format không bị đẩy đi đâu vô cớ', () => {
  const ds = [cauD('a', 'v_a', undefined), cauD('b', 'v_b', 'chon')];
  const m = mt({ v_a: 0.5, v_b: 0.5 });
  const r = xepTheoZPD(ds, m, hs({ chon: 0.9, go: 0.3 }));
  assert.equal(r.length, 2);
  assert.deepEqual([...r].map((c) => c.id).sort(), ['a', 'b']);
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
  assert.match(man, /hoSoDang=\{tienDo\.dinhDang/,
    'bảng định dạng đo rồi mà bộ chọn câu không nhận — đo mà chưa dùng thì chưa là '
    + 'thích ứng, đúng chỗ hụt của chiều Nhận thức sau Đợt 1');
});
