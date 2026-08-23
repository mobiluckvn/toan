/**
 * CỔNG · HỒ SƠ BÉ — chiều Sư phạm và CEFR mức bé (mục 2.1.2-P · 2.3.1).
 *
 * ── CÁI BẪY LỚN NHẤT: KẾT LUẬN KHI CHƯA ĐỦ MẪU ──
 * Bé làm 2 câu gõ chữ, sai cả 2 → "bé yếu dạng gõ chữ, 0%". Kết luận ấy sai, và
 * sai theo cách tự nuôi chính nó: nó dẫn tới việc cho bé ÍT câu gõ chữ đi, nên
 * mẫu không bao giờ lớn thêm, nên cái nhãn sai không bao giờ được sửa.
 *
 * Nguy hơn nữa vì nó là nhãn dán lên MỘT ĐỨA TRẺ, hiện ra cho bố mẹ đọc.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  ghiDinhDang, tiLeDung, xepDinhDang, manhNhat, yeuNhat,
  tenDinhDang, TOI_THIEU_MAU,
} from '../src/mon/tienganh/lib/hoso.js';
import { soRong, ghiDangCau, gopTienDo } from '../src/mon/tienganh/lib/progress.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');

/** n lượt của một định dạng, `dung` lượt đúng. */
const bo = (hs, format, tong, dung) => {
  let r = hs;
  for (let i = 0; i < tong; i += 1) r = ghiDinhDang(r, format, i < dung);
  return r;
};

test('cộng dồn đúng, và không sửa hồ sơ cũ tại chỗ', () => {
  const a = {};
  const b = ghiDinhDang(a, 'chon', true);
  assert.deepEqual(a, {}, 'sửa tại chỗ thì React không thấy state đổi');
  assert.deepEqual(b.chon, { dung: 1, tong: 1 });
  assert.deepEqual(ghiDinhDang(b, 'chon', false).chon, { dung: 1, tong: 2 });
});

test('định dạng rỗng thì bỏ qua, không đẻ khoá rác', () => {
  assert.deepEqual(ghiDinhDang({}, '', true), {});
  assert.deepEqual(ghiDinhDang({}, null, true), {});
  assert.deepEqual(ghiDinhDang(undefined, undefined, true), {});
});

test('⚠ CHƯA ĐỦ MẪU thì trả null — "chưa biết", không phải "kém"', () => {
  const hs = bo({}, 'go', TOI_THIEU_MAU - 1, 0);
  assert.equal(tiLeDung(hs, 'go'), null,
    'kết luận trên vài câu sẽ tự nuôi chính nó: nhãn "yếu" → ít câu dạng ấy hơn → '
    + 'mẫu không lớn thêm → nhãn không bao giờ được sửa');
  assert.deepEqual(xepDinhDang(hs), []);
  assert.equal(manhNhat(hs), null);

  const du = bo({}, 'go', TOI_THIEU_MAU, 0);
  assert.equal(tiLeDung(du, 'go'), 0, 'đủ mẫu rồi thì mới được nói, kể cả nói 0%');
});

test('"yếu nhất" cần ÍT NHẤT HAI định dạng đủ mẫu', () => {
  const mot = bo({}, 'chon', 20, 18);
  assert.notEqual(manhNhat(mot), null);
  assert.equal(yeuNhat(mot), null,
    'một mình nó thì vừa mạnh nhất vừa yếu nhất — câu ấy không có nghĩa gì');

  const hai = bo(mot, 'go', 20, 6);
  assert.equal(manhNhat(hai).ma, 'chon');
  assert.equal(yeuNhat(hai).ma, 'go');
});

test('xếp hạng: mạnh trước yếu sau, và mang theo cỡ mẫu', () => {
  let hs = bo({}, 'chon', 20, 19);
  hs = bo(hs, 'the', 20, 12);
  hs = bo(hs, 'go', 20, 4);
  hs = bo(hs, 'tf', 3, 3);                       // chưa đủ mẫu → không có mặt
  const r = xepDinhDang(hs);
  assert.deepEqual(r.map((x) => x.ma), ['chon', 'the', 'go']);
  assert.ok(r.every((x) => x.tong >= TOI_THIEU_MAU));
  assert.ok(r.every((x) => typeof x.ten === 'string' && x.ten.length > 0));
});

test('định dạng lạ thì hiện chính mã, đừng giấu', () => {
  assert.equal(tenDinhDang('chon'), 'chọn đáp án');
  assert.equal(tenDinhDang('dangLa'), 'dangLa',
    'trả về chuỗi rỗng thì bố mẹ thấy một dòng trống và không ai lần ra vì sao');
  assert.equal(tenDinhDang(null), '—');
});

/* ── CEFR mức bé: ĐÃ CHUYỂN CHỖ ───────────────────────────────────────────────
 * `cefrCuaBe()` bị bỏ ngày 23-08-2026 (mã chết, xem chú ở `hoso.js`). Phép quy
 * đổi CEFR nay ở `lib/cefr.js`, cổng riêng là `test/cefr_quy_doi.test.mjs`.
 */

/* ── nối vào sổ ───────────────────────────────────────────────────────────── */

test('sổ tại máy giữ được bảng định dạng', () => {
  let p = soRong();
  p = ghiDangCau(p, 'chon', true);
  p = ghiDangCau(p, 'chon', false);
  assert.deepEqual(p.dinhDang.chon, { dung: 1, tong: 2 });
});

test('⚠ GỘP hai máy thì CỘNG, không lấy bên mới hơn', () => {
  /* Đây là phép đếm tích luỹ: bé làm 40 câu trên máy bảng và 30 câu trên laptop
     thì hồ sơ phải là 70. Lấy "bản mới hơn" như mọi thứ khác là vứt đi 40 câu. */
  const may = { ...soRong(), dinhDang: { chon: { dung: 30, tong: 40 } } };
  const chu = { ...soRong(), dinhDang: { chon: { dung: 20, tong: 30 }, go: { dung: 1, tong: 5 } } };
  const g = gopTienDo(may, chu);
  assert.deepEqual(g.dinhDang.chon, { dung: 50, tong: 70 });
  assert.deepEqual(g.dinhDang.go, { dung: 1, tong: 5 });
  /* Gộp phải đối xứng cho phép cộng. */
  assert.deepEqual(gopTienDo(chu, may).dinhDang.chon, { dung: 50, tong: 70 });
  /* Một bên rỗng thì không mất gì. */
  assert.deepEqual(gopTienDo(may, soRong()).dinhDang.chon, { dung: 30, tong: 40 });
});

test('CHỈ đếm lượt ĐẦU của mỗi câu', () => {
  /* Đếm cả lượt thử lại thì dạng nào cho phép thử nhiều lần tự nhiên có tỉ lệ
     đúng thấp hơn — mà đó là tính chất của DẠNG CÂU, không phải của bé. */
  const ma = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(ma, /e\.lan === 1 && e\.cau\?\.format/,
    'đang cộng cả lượt thử lại vào bảng định dạng');
});

test('màn hình IM LẶNG khi chưa có gì để nói', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(ma, /if \(!manh && !cefr\) return null;/,
    'thà trống còn hơn dán cho bé một cái nhãn dựng trên hai câu');
  assert.match(ma, /\{manh\.tong\} câu|\{yeu\.tong\} câu/,
    'phải hiện CỠ MẪU: "làm tốt nhất dạng chọn đáp án" dựng trên 9 câu hay 900 câu '
    + 'thì bố mẹ tin như nhau, mà hai con số ấy khác hẳn');
});

test('sổ đăng ký có khai cefr cho cả 5 quyển Tiếng Anh', () => {
  const dk = JSON.parse(doc('../public/content/chuong_trinh.json'));
  for (const ma of ['ta1', 'ta2', 'ta3', 'ta4', 'ta5']) {
    assert.ok(dk.chuongTrinh[ma]?.cefr,
      `${ma} chưa khai cefr — hồ sơ bé sẽ im lặng ở mục trình độ`);
  }
});
