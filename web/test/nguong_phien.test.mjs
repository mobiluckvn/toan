/**
 * CỔNG · BỘ NGƯỠNG CỦA MỘT PHIÊN — ba chỗ dễ vỡ của R7 đợt 2.
 *
 * Đợt 2 cho ngưỡng đi từ tệp/Firestore vào mã. Ba chỗ hỏng được mà KHÔNG ai thấy:
 *
 *   1. `main.jsx` import `App.jsx` kiểu TĨNH → cả cây module nạp trước khi
 *      `napNguong()` kịp chạy, mọi hằng ngưỡng chụp bộ mặc định, và tệp tải về
 *      chẳng tác dụng gì. Màn hình vẫn chạy ngon, không lỗi nào.
 *   2. Máy chủ đọc hằng chụp-lúc-nạp thay vì đọc lúc GỌI → chuyên gia sửa xong
 *      phải chờ hàm nền khởi động lại mới ăn, tức vẫn phải nhờ người viết mã.
 *   3. Bản ghi lượt thiếu `nguongVer` → kết quả cũ không còn tính lại được, và hai
 *      bộ ngưỡng không so được trên cùng một nhật ký.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');

/* ═══════════ 1 · ĐIỂM VÀO PHẢI NẠP NGƯỠNG TRƯỚC ═══════════ */

test('main.jsx await napNguong() TRƯỚC, rồi mới import App động', () => {
  const s = doc('../src/main.jsx');
  assert.match(s, /await\s+napNguong\(\)/, 'main.jsx không chờ nạp bộ ngưỡng');
  assert.match(s, /await\s+import\(\s*['"]\.\/App\.jsx['"]\s*\)/,
    'App.jsx phải import ĐỘNG — import tĩnh chạy trước mọi dòng lệnh');
  assert.doesNotMatch(s, /^import\s+App\s+from/m,
    'còn import tĩnh App.jsx: cả cây module nạp trước khi có bộ ngưỡng');
  const iNap = s.indexOf('napNguong()');
  const iApp = s.indexOf("import('./App.jsx')");
  assert.ok(iNap > -1 && iApp > iNap, 'phải nạp ngưỡng xong mới import App');
});

/* ═══════════ 2 · HAI PHÍA ĐỌC BỘ ĐANG HÀNH, KHÔNG ĐỌC BẢN CHỤP ═══════════ */

test('mọi hằng ngưỡng ở máy con đọc boNguong(), không đọc BO_MAC_DINH', () => {
  const tep = ['../src/mon/tienganh/lib/zpd.js', '../src/mon/tienganh/lib/chinhsach.js',
               '../src/mon/tienganh/lib/lantruyen.js', '../src/mon/tienganh/lib/dandat.js',
               '../src/mon/tienganh/lib/hoso.js', '../src/mon/toan/lib/adaptive.js'];
  for (const p of tep) {
    const s = doc(p);
    assert.doesNotMatch(s, /layNguong\(BO_MAC_DINH/,
      `${p}: còn đọc bản chụp — chuyên gia sửa ngưỡng sẽ không ăn ở đây`);
    assert.match(s, /layNguong\(boNguong\(\)/, `${p}: phải đọc bộ đang hành`);
  }
});

test('BKT ở máy chủ đọc tham số LÚC GỌI — đổi bộ là đổi kết quả ngay', async () => {
  const n = await import('../functions/src/nguong.js');
  const b = await import('../functions/src/bkt.js');
  n.datBoNguong(n.BO_MAC_DINH);
  const truoc = b.paramsFor({}).guess;
  n.datBoNguong({ macDinh: { NG04: 0.10 } });
  const sau = b.paramsFor({}).guess;
  n.datBoNguong(n.BO_MAC_DINH);                       // trả lại cho cổng khác
  assert.equal(truoc, 0.30);
  assert.equal(sau, 0.10, 'paramsFor còn chụp hằng lúc nạp module');
});

test('quên dần đi theo NG06 lúc gọi', async () => {
  const n = await import('../functions/src/nguong.js');
  const b = await import('../functions/src/bkt.js');
  n.datBoNguong(n.BO_MAC_DINH);
  const a = b.quenDan(0.9, 14);
  n.datBoNguong({ macDinh: { NG06: 3 } });
  const c = b.quenDan(0.9, 14);
  n.datBoNguong(n.BO_MAC_DINH);
  assert.ok(c < a, 'bán rã ngắn hơn thì phải quên nhanh hơn');
});

/* ═══════════ 3 · ĐƯỜNG ĐỌC CỦA MÁY CHỦ ═══════════ */

const giaDb = (ds, nem = false) => ({
  collection: () => ({ get: async () => {
    if (nem) throw new Error('mất mạng');
    return { forEach: (f) => ds.forEach((x) => f({ data: () => x })) };
  } }),
});

test('đọc Firestore: giá trị toàn hệ và giá trị theo phạm vi', async () => {
  const m = await import('../functions/src/napNguong.js');
  const n = await import('../functions/src/nguong.js');
  m.quenNguong();
  const bo = await m.layBoNguong(giaDb([
    { ma: 'NG07', giaTri: 0.92, phienBan: 4, phamVi: { loai: 'toanHe' } },
    { ma: 'NG09', giaTri: 5, phienBan: 4, phamVi: { loai: 'khoiLop', khoa: '3' } },
  ]));
  assert.equal(n.layNguong(bo, 'NG07'), 0.92);
  assert.equal(n.layNguong(bo, 'NG09', { khoiLop: '3' }), 5);
  assert.equal(n.layNguong(bo, 'NG09', { khoiLop: '1' }), 3, 'khối khác giữ mặc định');
  assert.equal(bo.phienBan, 4);
  m.quenNguong(); n.datBoNguong(n.BO_MAC_DINH);
});

test('Firestore hỏng thì LÙI về mặc định, KHÔNG ném', async () => {
  const m = await import('../functions/src/napNguong.js');
  const n = await import('../functions/src/nguong.js');
  m.quenNguong();
  const truoc = m.LOI_DOC.lui;
  const bo = await m.layBoNguong(giaDb([], true));
  assert.equal(n.layNguong(bo, 'NG07'), 0.85);
  assert.equal(m.LOI_DOC.lui, truoc + 1, 'phải ĐẾM số lần lùi — không nuốt im');
  m.quenNguong(); n.datBoNguong(n.BO_MAC_DINH);
});

test('bảng `nguong` rỗng (chưa tới đợt 3) cũng lùi về mặc định', async () => {
  const m = await import('../functions/src/napNguong.js');
  const n = await import('../functions/src/nguong.js');
  m.quenNguong();
  const bo = await m.layBoNguong(giaDb([]));
  assert.equal(n.layNguong(bo, 'NG07'), 0.85);
  m.quenNguong(); n.datBoNguong(n.BO_MAC_DINH);
});

test('nhớ tạm: trong hạn thì KHÔNG đọc Firestore lần nữa', async () => {
  const m = await import('../functions/src/napNguong.js');
  const n = await import('../functions/src/nguong.js');
  m.quenNguong();
  let lanDoc = 0;
  const db = { collection: () => ({ get: async () => {
    lanDoc += 1;
    return { forEach: (f) => f({ data: () => ({ ma: 'NG07', giaTri: 0.9, phamVi: { loai: 'toanHe' } }) }) };
  } }) };
  let gio = 1000;
  await m.layBoNguong(db, { bayGio: () => gio });
  await m.layBoNguong(db, { bayGio: () => gio });
  assert.equal(lanDoc, 1, 'đọc lại trong hạn nhớ → một lượt đọc cho mỗi câu trẻ làm');
  gio += m.HAN_NHO_MS + 1;
  await m.layBoNguong(db, { bayGio: () => gio });
  assert.equal(lanDoc, 2, 'hết hạn thì phải đọc lại');
  m.quenNguong(); n.datBoNguong(n.BO_MAC_DINH);
});

/* ═══════════ 4 · `nguongVer` TRÊN BẢN GHI LƯỢT ═══════════ */

test('bản ghi lượt của CẢ HAI MÔN mang nguongVer', () => {
  for (const p of ['../src/mon/tienganh/lib/suKien.js', '../src/mon/toan/lib/sync.js']) {
    assert.match(doc(p), /nguongVer:\s*boNguong\(\)/, `${p}: bản ghi thiếu nguongVer`);
  }
});

test('hàm nền ghi nguongVer vào tài liệu mastery, và nạp bộ TRƯỚC khi chấm', () => {
  const s = doc('../functions/index.js');
  assert.match(s, /await layBoNguong\(db\)/, 'chưa nạp bộ ngưỡng trước khi chấm');
  assert.match(s, /nguongVer:/, 'tài liệu mastery thiếu nguongVer');
  assert.ok(s.indexOf('layBoNguong(db)') < s.indexOf('applyAttempt('),
    'phải nạp bộ TRƯỚC khi gọi applyAttempt');
});

test('tệp chạy `content/nguong.json` có mặt và khớp bản gốc', () => {
  const chay = JSON.parse(doc('../public/content/nguong.json'));
  const goc = JSON.parse(doc('../../data/nguong.json'));
  assert.equal(chay.phienBan, goc.phienBan);
  assert.equal(Object.keys(chay.macDinh).length, 21);
  for (const x of goc.nguong) {
    assert.deepEqual(chay.macDinh[x.ma], x.giaTri, `${x.ma}: tệp chạy lệch bản gốc`);
  }
});
