/**
 * CỔNG · NHẬT KÝ TỪNG LƯỢT TRẢ LỜI CỦA TIẾNG ANH.
 *
 * Ba thứ canh ở đây, và cả ba đều hỏng TRONG IM LẶNG nếu sai:
 *
 *  1. ĐỦ SÁU TRƯỜNG LUẬT ĐÒI. `firestore.rules` bắt buộc
 *     `['learnerId','microId','itemId','phase','correct','ts']`. Thiếu một cái là
 *     Firestore từ chối — mà lệnh ghi không chờ kết quả, nên bé học xong, màn hình
 *     báo xong, máy chủ trống. Đúng lỗi đã dính một lần khi làm học bạ.
 *
 *  2. MÃ BẢN GHI ỔN ĐỊNH. Dựng lại cùng một phiên phải ra cùng bộ mã, nếu không
 *     mỗi lần đẩy lại sinh một dòng mới và nhật ký phồng lên. Nhưng hai LƯỢT khác
 *     nhau của cùng một câu thì phải ra HAI mã — không thì bé sai hai lần rồi mới
 *     đúng chỉ còn một dòng, mất đúng thứ nhật ký thô sinh ra để giữ.
 *
 *  3. MỘT NÚT CHÍNH CHO MỘT LƯỢT. `bktUnit` lấy từ `maNut`, không phải `maNutDs`.
 *     Ghi hai nút là một câu đúng được tính công hai lần, mức thạo phồng lên, và
 *     hệ thống hoá ra LẠC QUAN về bé — cho bé đi tiếp khi bé chưa vững.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  dungSuKien, maSuKien, maPhienMoi, xepHang, docHangDoi, ghiHangDoi,
  dayHangDoi, sangTenHangDoi, laHocSinhThat, goiDapAn, PHIEN_BAN_BAN_GHI,
} from '../src/mon/tienganh/lib/suKien.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');

/** localStorage giả — đủ dùng cho hàng đợi. */
const khoGia = () => {
  const m = new Map();
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
  };
};

const luot = (n = 2) => Array.from({ length: n }, (_, i) => ({
  itemId: 'C1',
  maNut: 'v_g5_u1_city',
  maNutDs: ['v_g5_u1_city'],
  ok: i === n - 1,
  tries: i + 1,
  hintsUsed: i,
  ms: 1000 + i,
  phase: 'practice',
  answer: 'city',
  expected: { choice: 'city' },
  khiNao: 1_700_000_000_000 + i,
}));

test('đủ SÁU trường mà firestore.rules đòi', () => {
  /* Đọc danh sách THẲNG TỪ LUẬT, không chép sang đây — chép là sớm muộn lệch, mà
     lệch ở đúng chỗ này thì lại im lặng. */
  const luat = chiMa(doc('../firestore.rules'));
  const i = luat.indexOf('match /attempts/{attemptId}');
  assert.notEqual(i, -1, 'firestore.rules không còn khối attempts');
  const m = luat.slice(i, i + 900).match(/hasAll\(\s*\[([^\]]+)\]/);
  assert.ok(m, 'khối attempts không chốt danh sách trường bắt buộc');
  const can = m[1].split(',').map((s) => s.trim().replace(/^'|'$/g, ''));

  const [r] = dungSuKien({
    learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01', viec: luot(1),
  });
  for (const k of can) {
    assert.ok(r[k] !== undefined && r[k] !== null,
      `bản ghi thiếu '${k}' — máy chủ TỪ CHỐI, và từ chối trong im lặng`);
  }
});

test('phase phải nằm trong danh sách luật cho', () => {
  const luat = chiMa(doc('../firestore.rules'));
  const i = luat.indexOf('match /attempts/{attemptId}');
  const m = luat.slice(i, i + 900).match(/data\.phase in \[([^\]]+)\]/);
  assert.ok(m, 'luật không chốt danh sách phase');
  const cho = m[1].split(',').map((s) => s.trim().replace(/^'|'$/g, ''));
  for (const p of ['practice', 'assess']) {
    assert.ok(cho.includes(p), `màn Tiếng Anh gửi phase '${p}' mà luật không cho`);
  }
  const [r] = dungSuKien({
    learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01', viec: luot(1),
  });
  assert.ok(cho.includes(r.phase));
});

test('bktUnit lấy từ maNut — MỘT nút, không phải cả danh sách', () => {
  const [r] = dungSuKien({
    learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01',
    viec: [{ ...luot(1)[0], maNut: 'sp_g5_u1_1', maNutDs: ['sp_g5_u1_1', 'v_g5_u1_city'] }],
  });
  assert.equal(r.bktUnit, 'sp_g5_u1_1');
  assert.equal(typeof r.bktUnit, 'string', 'bktUnit phải là MỘT chuỗi, không phải mảng');
  assert.deepEqual(r.maNutDs, ['sp_g5_u1_1', 'v_g5_u1_city'],
    'maNutDs vẫn phải giữ đủ, để lan truyền chẩn đoán sau này dùng');
});

test('dựng lại cùng phiên ra cùng bộ mã; hai LƯỢT thì hai mã', () => {
  const d = { learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01' };
  const a = dungSuKien({ ...d, viec: luot(2) });
  const b = dungSuKien({ ...d, viec: luot(2) });
  assert.deepEqual(a.map((x) => x.id), b.map((x) => x.id),
    'dựng lại ra mã khác → mỗi lần đẩy lại sinh dòng mới, nhật ký phồng lên');
  assert.notEqual(a[0].id, a[1].id,
    'hai lượt của cùng một câu trùng mã → mất dòng, chỉ còn lượt cuối');

  /* Và thêm một lượt nữa thì hai mã cũ KHÔNG đổi — đây là điều làm cho "gửi lại
     cả phiên sau mỗi lượt" không sinh rác. */
  const c = dungSuKien({ ...d, viec: luot(3) });
  assert.deepEqual(c.slice(0, 2).map((x) => x.id), a.map((x) => x.id));
});

test('mã bản ghi không chứa ký tự Firestore cấm', () => {
  const id = maSuKien('u1', 'p1', 'DL:TA5.B01', 'C1', 0);
  assert.doesNotMatch(id, /[/.]/, "tên tài liệu Firestore không được chứa '/' hay '.'");
  assert.match(id, /^u1_p1_DL_TA5_B01_C1_0$/);
});

test('thiếu learnerId/maPhien/microId thì NÉM, không ghi bừa', () => {
  for (const thieu of ['learnerId', 'maPhien', 'microId']) {
    const d = { learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01', viec: luot(1) };
    delete d[thieu];
    assert.throws(() => dungSuKien(d), undefined, `thiếu ${thieu} mà vẫn dựng được`);
  }
});

test('hàng đợi: ghi đè theo mã, không nhân bản', () => {
  const kho = khoGia();
  const d = { learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01' };
  xepHang(dungSuKien({ ...d, viec: luot(2) }), kho);
  xepHang(dungSuKien({ ...d, viec: luot(3) }), kho);
  assert.equal(docHangDoi(kho).length, 3, 'đẩy lại cả phiên mà hàng đợi phình ra');
});

test('gửi hỏng thì GIỮ NGUYÊN phần chưa gửi', async () => {
  const kho = khoGia();
  ghiHangDoi(dungSuKien({
    learnerId: 'u1', maPhien: 'p1', microId: 'DL:TA5.B01', viec: luot(3),
  }), kho);
  const r = await dayHangDoi(async () => { throw new Error('mất mạng'); }, kho);
  assert.equal(r.daGui, 0);
  assert.equal(r.loi, true);
  assert.equal(docHangDoi(kho).length, 3, 'mất mạng mà hàng đợi bị xoá → mất công học của bé');

  /* Gửi được thì dọn sạch, không giữ lại để gửi lần hai. */
  const r2 = await dayHangDoi(async () => {}, kho);
  assert.equal(r2.daGui, 3);
  assert.equal(docHangDoi(kho).length, 0);
});

test('đăng nhập xong thì sang tên hàng đợi, và mã đổi theo', () => {
  const kho = khoGia();
  ghiHangDoi(dungSuKien({
    learnerId: 'local', maPhien: 'p1', microId: 'DL:TA5.B01', viec: luot(2),
  }), kho);
  assert.equal(sangTenHangDoi('u9', kho).doi, 2);
  const q = docHangDoi(kho);
  assert.ok(q.every((r) => r.learnerId === 'u9'));
  assert.ok(q.every((r) => r.id.startsWith('u9_')),
    'mã nhúng learnerId, sang tên mà không dựng lại mã thì luật vẫn từ chối');
  assert.equal(new Set(q.map((r) => r.id)).size, 2, 'sang tên làm trùng mã');

  /* Chưa đăng nhập thì KHÔNG đụng vào gì. */
  assert.equal(sangTenHangDoi('local', kho).doi, 0);
  assert.equal(laHocSinhThat('local'), false);
});

test('đáp án dài bị cắt, không nuốt cả bài của bé vào một dòng', () => {
  const dai = 'x'.repeat(500);
  assert.ok(goiDapAn(dai).length <= 120);
  assert.equal(goiDapAn(['a', 'b']), 'a | b');
  assert.equal(goiDapAn(undefined), '');
});

test('KHÔNG import gì từ mon/toan — cổng ranh_gioi cấm hai môn dính nhau', () => {
  const ma = chiMa(doc('../src/mon/tienganh/lib/suKien.js'));
  assert.doesNotMatch(ma, /mon\/toan|\.\.\/\.\.\/toan/,
    'suKien.js import từ Toán — chép là cố ý, xem chú thích đầu tệp');
});

test('hàng đợi tại máy phải TÁCH khoá với Toán', () => {
  /* Chung collection trên máy chủ thì đúng; chung KHOÁ localStorage thì mất bản
     ghi: hai môn cùng đọc-sửa-ghi một khoá, môn này ghi đè mất phần môn kia vừa
     thêm, và mỗi bên đều thấy lệnh ghi của mình thành công. */
  const ta = chiMa(doc('../src/mon/tienganh/lib/suKien.js'));
  const toan = chiMa(doc('../src/mon/toan/lib/sync.js'));
  const khoaTA = ta.match(/QKEY_GOC\s*=\s*'([^']+)'/)?.[1];
  const khoaToan = toan.match(/QKEY_GOC\s*=\s*'([^']+)'/)?.[1];
  assert.ok(khoaTA && khoaToan, 'không đọc được khoá hàng đợi của một trong hai môn');
  assert.notEqual(khoaTA, khoaToan, 'hai môn dùng chung khoá hàng đợi → mất bản ghi');
});

test('phiên bản bản ghi trùng với Toán — bên đọc chỉ cần một luật', () => {
  const toan = chiMa(doc('../src/mon/toan/lib/sync.js'));
  const v = Number(toan.match(/PHIEN_BAN_BAN_GHI\s*=\s*(\d+)/)?.[1]);
  assert.equal(PHIEN_BAN_BAN_GHI, v,
    'hai môn khai hai số phiên bản khác nhau cho cùng một hình dạng bản ghi');
});

test('mã phiên mới thì khác nhau', () => {
  const ds = new Set(Array.from({ length: 50 }, () => maPhienMoi()));
  assert.equal(ds.size, 50, 'mã phiên trùng → hai buổi học dính vào nhau');
});
