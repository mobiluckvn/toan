/**
 * CỔNG · MÀN ÔN LẠI NGẮT QUÃNG.
 *
 * ── VÌ SAO MÀN NÀY RA ĐỜI MUỘN, VÀ VÌ SAO ĐÓ LÀ MỘT BÀI HỌC ──
 * Hàm nền sinh thẻ ôn theo lịch +1 / +3 / +7 ngày từ lâu. Luật Firestore cũng đã
 * cho máy con đọc `reviewQueue`. Cả hai đầu đều đúng khi nhìn riêng — nhưng
 * KHÔNG màn nào đọc thư mục ấy, kể cả môn Toán. Thẻ sinh ra rồi nằm đó, và
 * "lặp lại ngắt quãng" tồn tại trên giấy suốt thời gian dài.
 *
 * Không cổng nào bắt được, vì mỗi cổng chỉ soi phần việc của mình: cổng lịch soi
 * `buildReviewCards` (đúng), cổng luật soi `firestore.rules` (đúng). Cái thiếu là
 * một câu hỏi mà không tệp nào sở hữu: "ai ĐỌC thứ này ra?"
 *
 * Nên phép canh cuối tệp này hỏi đúng câu ấy — và hỏi cho CẢ HAI MÔN.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import {
  theDenHan, demDenHan, chonCauOn, theQua, daySauKhiOn, BOX_NGAY,
  SO_CAU_MOI_THE, SO_THE_MOI_LUOT,
} from '../src/mon/tienganh/lib/onlai.js';
import { BOX_DAYS, reviewCard } from '../functions/src/schedule.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
const NGAY = 86400000;

const the = (id, microId, dueAt, extra = {}) => ({ id, microId, dueAt, box: 0, ...extra });

test('chỉ lấy thẻ ĐẾN HẠN, quá hạn lâu nhất đứng trước', () => {
  const bay = 1000 * NGAY;
  const ds = [
    the('a', 'DL:TA5.B01', bay - 1 * NGAY),
    the('b', 'DL:TA5.B02', bay - 20 * NGAY),
    the('c', 'DL:TA5.B03', bay + 5 * NGAY),      // chưa tới hạn
  ];
  const r = theDenHan(ds, { quyen: 'ta5', bayGio: bay });
  assert.deepEqual(r.map((x) => x.id), ['b', 'a'],
    'thẻ trễ 20 ngày phải đứng trước thẻ trễ 1 ngày — xếp theo thứ tự tạo thì thẻ '
    + 'trễ bị đẩy mãi ra sau và không bao giờ tới lượt');
});

test('LỌC THEO QUYỂN — không bày thẻ môn khác hay quyển khác', () => {
  const bay = 1000 * NGAY;
  const ds = [
    the('t', 'DL:KSN2.B04', bay - NGAY),         // môn Toán
    the('x', 'DL:TA4.B01', bay - NGAY),          // quyển khác
    the('y', 'DL:TA5.B01', bay - NGAY),
  ];
  assert.deepEqual(theDenHan(ds, { quyen: 'ta5', bayGio: bay }).map((x) => x.id), ['y'],
    'bày thẻ quyển khác thì bé bấm vào là nhảy sang một bài lạ hoắc');
  assert.equal(demDenHan(ds, { quyen: 'ta4', bayGio: bay }), 1);
  /* Không khai quyển thì lấy tất — dùng cho chỗ đếm chung, phải còn đường ấy. */
  assert.equal(demDenHan(ds, { bayGio: bay }), 3);
});

test('thẻ hỏng hình dạng thì bỏ, không ném', () => {
  const bay = 1000 * NGAY;
  const ds = [null, {}, { microId: 'DL:TA5.B01' }, the('ok', 'DL:TA5.B01', bay - NGAY)];
  assert.equal(theDenHan(ds, { quyen: 'ta5', bayGio: bay }).length, 1);
});

test('nhiều nhất SO_THE_MOI_LUOT thẻ một lượt', () => {
  const bay = 1000 * NGAY;
  const ds = Array.from({ length: 12 }, (_, i) => the(`t${i}`, 'DL:TA5.B01', bay - i * NGAY));
  assert.equal(theDenHan(ds, { quyen: 'ta5', bayGio: bay }).length, SO_THE_MOI_LUOT);
  assert.equal(demDenHan(ds, { quyen: 'ta5', bayGio: bay }), 12,
    'phép ĐẾM không được bị cắt theo số thẻ mời — thẻ mời hiện sai con số');
});

/* ── chọn câu ─────────────────────────────────────────────────────────────── */

const baiGia = {
  practice: {
    pools: {
      warmup: [{ id: 'C1' }, { id: 'C2' }, { id: 'C3' }, { id: 'C4' }],
      standard: [{ id: 'S1' }, { id: 'S2' }],
      challenge: [{ id: 'T1' }],
    },
  },
};

test('flashcard lấy bậc khởi động; thẻ thường ưu tiên bậc ráp câu', () => {
  const fc = chonCauOn(baiGia, { kind: 'flashcard' });
  assert.deepEqual(fc.map((c) => c.id), ['C1', 'C2', 'C3']);
  const it = chonCauOn(baiGia, { kind: 'item' });
  assert.deepEqual(it.map((c) => c.id), ['S1', 'S2', 'T1'],
    'mốc +3 và +7 ngày kiểm bé còn DÙNG được, không chỉ còn NHỚ');
});

test('THIẾU KHO THÌ LÙI, không trả rỗng', () => {
  /* Unit chỉ dạy từ, không có bậc ráp câu. Đòi bằng được thì buổi ôn ra màn
     trắng — ôn hơi dễ vẫn hơn không ôn. */
  const chiTu = { practice: { pools: { warmup: [{ id: 'C1' }, { id: 'C2' }, { id: 'C3' }] } } };
  assert.equal(chonCauOn(chiTu, { kind: 'item' }).length, 3);
  /* Nhưng bài rỗng hẳn thì phải trả rỗng để màn còn biết mà bỏ qua thẻ. */
  assert.deepEqual(chonCauOn({ practice: { pools: {} } }, { kind: 'item' }), []);
  assert.deepEqual(chonCauOn(null, { kind: 'item' }), []);
});

test('hai lượt ôn cùng một bài KHÔNG ra y hệt một bộ câu', () => {
  const l1 = chonCauOn(baiGia, { kind: 'flashcard' }, { batDau: 0 });
  const l2 = chonCauOn(baiGia, { kind: 'flashcard' }, { batDau: 1 });
  assert.notDeepEqual(l1.map((c) => c.id), l2.map((c) => c.id));
  /* Xoay vòng chứ không ngẫu nhiên — có ngẫu nhiên thì cổng không kiểm được. */
  assert.deepEqual(chonCauOn(baiGia, { kind: 'flashcard' }, { batDau: 4 }).map((c) => c.id),
    l1.map((c) => c.id), 'quay đủ một vòng phải về đúng bộ cũ');
});

/* ── qua hay không qua ─────────────────────────────────────────────────────── */

test('ĐÚNG HẾT mới qua — nghiêm hơn bài học thường, và cố ý', () => {
  assert.equal(theQua([true, true, true]), true);
  assert.equal(theQua([true, false, true]), false,
    'cho qua khi mới đúng 2/3 là giãn khoảng cách cho thứ bé chưa vững — hỏng đúng '
    + 'cái cơ chế lặp lại ngắt quãng');
  assert.equal(theQua([]), false);
  assert.equal(theQua(null), false);
});

test('sai thì VỀ HỘP 0, không lùi một nấc', () => {
  const cao = the('a', 'DL:TA5.B01', 0, { box: 4 });
  const sai = daySauKhiOn(cao, false, 0);
  assert.equal(sai.box, 0);
  assert.equal(sai.dueAt, BOX_NGAY[0] * NGAY,
    'lùi từ hộp 4 xuống hộp 3 thì vẫn còn 7 ngày nữa mới gặp lại thứ bé vừa quên');
  const dung = daySauKhiOn(cao, true, 0);
  assert.equal(dung.box, 4, 'hộp cao nhất thì đứng yên, không tràn');
  assert.equal(dung.dueAt, BOX_NGAY[4] * NGAY);
});

test('đếm số lần đã ôn — để xoay vòng bộ câu', () => {
  let t = the('a', 'DL:TA5.B01', 0);
  t = daySauKhiOn(t, true, 0);
  t = daySauKhiOn(t, true, 0);
  assert.equal(t.soLanOn, 2);
});

test('⚠ LUẬT HỘP Ở MÁY CON PHẢI KHỚP MÁY CHỦ', () => {
  /* `lib/onlai.js` CHÉP `functions/src/schedule.js` vì không import được (mã máy
     chủ kéo theo firebase-admin). Chép thì phải có người canh. */
  assert.deepEqual(BOX_NGAY, BOX_DAYS, 'hai bản khoảng cách hộp đã trôi xa nhau');
  for (const qua of [true, false]) {
    for (const box of [0, 2, 4]) {
      const t = { id: 'a', microId: 'DL:TA5.B01', box };
      const may = daySauKhiOn(t, qua, 0);
      const chu = reviewCard(t, qua, 0);
      assert.equal(may.box, chu.box, `hộp lệch ở box=${box} qua=${qua}`);
      assert.equal(may.dueAt, chu.dueAt, `ngày hẹn lệch ở box=${box} qua=${qua}`);
    }
  }
});

/* ── câu hỏi mà trước nay không tệp nào sở hữu ─────────────────────────────── */

test('CÓ MÀN NÀO ĐỌC reviewQueue KHÔNG — cho cả hai môn', () => {
  const nguon = [];
  const quet = (thuMuc) => {
    for (const f of readdirSync(new URL(thuMuc, import.meta.url), { withFileTypes: true })) {
      if (f.isDirectory()) quet(`${thuMuc}${f.name}/`);
      else if (/\.(jsx?|mjs)$/.test(f.name)) nguon.push(chiMa(doc(`${thuMuc}${f.name}`)));
    }
  };
  quet('../src/');
  const ma = nguon.join('\n');
  assert.match(ma, /reviewQueue/,
    'không mã nào ở máy con đọc `reviewQueue` — thẻ ôn sinh ra rồi nằm đó, và '
    + '"lặp lại ngắt quãng" chỉ tồn tại trên giấy. Đây đúng là chỗ đã hổng suốt '
    + 'một thời gian dài mà không cổng nào bắt.');

  /* Và phải có màn thật sự BÀY nó ra, không chỉ khai tên thư mục. */
  const man = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(man, /docTheOn\(/, 'ManTiengAnh không nạp thẻ ôn');
  assert.match(man, /<OnLai/, 'không có màn ôn lại nào được dựng');
  assert.match(man, /luuTheOn|daySauKhiOn/, 'ôn xong mà không ghi lại hộp Leitner');
});

test('thẻ mời chỉ hiện khi CÓ thẻ tới hạn', () => {
  /* Hiện thường trực với số 0 thì thành nút chết, và bé học được cách bỏ qua nó
     — rồi bỏ qua luôn những hôm nó có số thật. */
  const man = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(man, /soTheOn > 0 &&/, 'thẻ mời ôn tập không có điều kiện hiện');
});

test('lượt ôn CŨNG vào nhật ký — nếu không thì phép quên không bao giờ được gỡ', () => {
  const on = chiMa(doc('../src/mon/tienganh/components/OnLai.jsx'));
  assert.match(on, /onLuot/,
    'ôn xong mà không ghi `attempts` thì BKT không thấy, `lastSeen` không nhích, '
    + 'và mức thạo cứ tụt dần dù bé vẫn ôn đều');
  assert.equal(SO_CAU_MOI_THE > 0 && SO_THE_MOI_LUOT > 0, true);
});
