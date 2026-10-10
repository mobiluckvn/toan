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

/* ────────────────────────────────────────────────────────────────────────────
   PHẠM VI HẸP (R7 · mục 3.8.1) — bốn nấc thấp của thang, phía máy chủ.

   Máy con đặt ngữ cảnh PHIÊN lúc bé mở quyển; hàm nền thì phải dựng lại ngữ cảnh
   từ chính bản ghi, mỗi lượt một lần. Khối cổng này canh đúng chỗ dễ vỡ ấy.
   ──────────────────────────────────────────────────────────────────────────── */

test('ngữ cảnh lượt chỉ đọc trường bản ghi TỰ KHAI, không suy từ mã nút', async () => {
  const { nguCanhLuot } = await import('../functions/src/bkt.js');

  assert.deepEqual(
    nguCanhLuot({ mon: 'tienganh', khoiLop: 5, bktUnit: 'v_g5_u1_city' }),
    { mon: 'tienganh', khoiLop: '5', nut: 'v_g5_u1_city' },
  );

  /* Dòng nhật ký đời cũ (v ≤ 3) KHÔNG có `khoiLop`. Mã nút mang chữ `g5` nhưng đó
     là quy ước đặt tên, không phải lời khai — không được suy ra. */
  const cu = nguCanhLuot({ mon: 'tienganh', bktUnit: 'v_g5_u1_city' });
  assert.equal(cu.khoiLop, undefined,
    'suy khối lớp từ hình dạng mã nút: đổi quy ước đặt tên một lần là mọi lượt rơi về toanHe trong im lặng');

  /* Chuỗi rỗng cũng là THIẾU, không phải một khoá phạm vi tên "" */
  assert.equal(nguCanhLuot({ khoiLop: '' }).khoiLop, undefined);
  assert.deepEqual(nguCanhLuot({}), {}, 'bản ghi trắng → không nấc nào, tức toanHe');
});

test('hàm nền chấm một lượt theo đúng phạm vi của bản ghi', async () => {
  const n = await import('../functions/src/nguong.js');
  const b = await import('../functions/src/bkt.js');

  const bo = {
    phienBan: 77,
    macDinh: { ...n.MAC_DINH },
    theoPhamVi: {
      toanHe: { NG07: 0.85 },
      khoiLop: { 5: { NG07: 0.60, NG04: 0.05 } },
      nut: { 'v_g5_u1_city': { NG07: 0.99 } },
    },
  };
  n.datBoNguong(bo);

  const lanDau = { learnerId: 'b', bktUnit: 'v_g5_u1_sun', correct: true, phase: 'practice' };

  /* Cùng MỘT mức thạo, ba phạm vi, ba kết luận "đã thạo" khác nhau — và đó chính
     là điều Thầy đòi: chuyên gia nới θ cho khối lớp 5 mà không ai sửa mã. */
  const chung = b.applyAttempt({ p: 0.5, lastSeen: Date.now(), nAttempts: 9 }, lanDau);
  assert.equal(chung.mastered, false, 'không khai khoiLop → θ toanHe 0,85');

  const lop5 = b.applyAttempt({ p: 0.5, lastSeen: Date.now(), nAttempts: 9 },
                              { ...lanDau, khoiLop: 5 });
  assert.equal(lop5.mastered, true, 'khai khoiLop 5 → θ 0,60');

  const hep = b.applyAttempt({ p: 0.5, lastSeen: Date.now(), nAttempts: 9 },
                             { ...lanDau, khoiLop: 5, bktUnit: 'v_g5_u1_city' });
  assert.equal(hep.mastered, false, 'nút hẹp hơn khối lớp → θ 0,99 thắng');

  /* Bốn tham số BKT cũng phải theo phạm vi, không chỉ θ. */
  const ts = b.paramsFor({ khoiLop: 5, bktUnit: 'v_g5_u1_sun' });
  assert.equal(ts.guess, 0.05, 'NG04 của khối lớp 5');
  assert.equal(b.paramsFor({}).guess, n.MAC_DINH.NG04, 'không ngữ cảnh → bộ chung');

  n.datBoNguong(null);
});

test('hàm nền KHÔNG giữ ngữ cảnh giữa hai lượt của hai bé', async () => {
  const n = await import('../functions/src/nguong.js');
  const b = await import('../functions/src/bkt.js');
  n.datBoNguong({
    phienBan: 78, macDinh: { ...n.MAC_DINH },
    theoPhamVi: { toanHe: { NG07: 0.85 }, khoiLop: { 5: { NG07: 0.60 } } },
  });

  const ho = () => ({ p: 0.5, lastSeen: Date.now(), nAttempts: 9 });
  b.applyAttempt(ho(), { learnerId: 'a', bktUnit: 'u', correct: true, khoiLop: 5 });
  /* Lượt NGAY SAU của một bé khác, không khai khối lớp. Hàm nền sống chung cho mọi
     bé, nên một ngữ cảnh rò qua lượt sau là chấm bé này bằng ngưỡng của bé kia. */
  const sau = b.applyAttempt(ho(), { learnerId: 'z', bktUnit: 'u', correct: true });
  assert.equal(sau.mastered, false, 'ngữ cảnh của bé trước rò sang bé sau');

  n.datBoNguong(null);
});

test('hai môn khai CÙNG một phiên bản bản ghi, và bản ghi mang khoiLop', async () => {
  const ta = await import('../src/mon/tienganh/lib/suKien.js');
  const to = await import('../src/mon/toan/lib/sync.js');
  assert.equal(ta.PHIEN_BAN_BAN_GHI, to.PHIEN_BAN_BAN_GHI,
    'hai môn lệch số phiên bản thì bên đọc nhật ký phải nhớ hai luật');
  assert.ok(ta.PHIEN_BAN_BAN_GHI >= 4, 'thêm trường vào bản ghi thì phải lên phiên bản');

  const n = await import('../src/chung/lib/nguong.js');
  n.datNguCanh({ mon: 'tienganh', khoiLop: 3 });
  const [d] = ta.dungSuKien({
    learnerId: 'b', maPhien: 'p', microId: 'm',
    viec: [{ itemId: 'i1', maNut: 'v_g3_u1_x', ok: true }],
  });
  assert.equal(d.khoiLop, '3', 'bản ghi phải KHAI khối lớp cho hàm nền dùng');
  n.datNguCanh({});
});

test('dạng câu: nấc đọc từ `mode`, và nút vẫn hẹp hơn nó', async () => {
  const n = await import('../functions/src/nguong.js');
  const b = await import('../functions/src/bkt.js');

  assert.equal(b.nguCanhLuot({ mode: 'chon' }).dangCau, 'chon');
  assert.equal(b.nguCanhLuot({}).dangCau, undefined, 'lượt không khai mode → không có nấc');

  n.datBoNguong({
    phienBan: 79, macDinh: { ...n.MAC_DINH },
    theoPhamVi: {
      toanHe: { NG04: 0.30 },
      /* Đúng lý do nấc này tồn tại: đoán trúng câu bốn lựa chọn ~0,25, gõ lại chữ
         thì gần 0. Một con số chung là sai cho cả hai. */
      dangCau: { chon: { NG04: 0.25 }, go: { NG04: 0.02 } },
      nut: { 'v_kho': { NG04: 0.40 } },
    },
  });

  assert.equal(b.paramsFor({ mode: 'chon' }).guess, 0.25);
  assert.equal(b.paramsFor({ mode: 'go' }).guess, 0.02);
  assert.equal(b.paramsFor({ mode: 'noi' }).guess, 0.30, 'dạng chưa cấu hình → bộ chung');
  assert.equal(b.paramsFor({ mode: 'chon', bktUnit: 'v_kho' }).guess, 0.40,
    'nút đứng TRƯỚC dạng câu trên thang phạm vi');

  n.datBoNguong(null);
});

test('hai môn không được dùng trùng một mã dạng câu', async () => {
  /* `dangCau` là MỘT không gian khoá dùng chung cho cả hai môn. Hiện hai môn dùng
     hai bộ từ rời nhau nên không ô ngưỡng nào mang hai nghĩa — nhưng đó là may, chứ
     không phải thiết kế. Đổi tên `chondapan` của Toán thành `chon` là từ đó chuyên
     gia sửa ngưỡng cho câu trắc nghiệm Tiếng Anh thì câu trắc nghiệm Toán đổi theo,
     và chẳng gì kêu. Cổng này kêu.

     ⚠ KHÔNG CHÉP DANH SÁCH MÃ VÀO ĐÂY. Bản đầu tôi viết regex ghim đúng năm chữ của
     Toán — tức ghim CHÍNH TẢ chứ không ghim tính chất, cái bẫy kho này đã dính bốn
     lần: thêm dạng câu mới mà quên sửa cổng thì cổng vẫn xanh, và nó xanh về một
     thứ không còn đúng. Bản thứ hai tôi tự bịa vỏ câu để gọi `answerMode` — cũng
     hỏng, vì vỏ bịa không đúng hình dạng thật nên bốn trong năm nhánh rơi hết về
     `so` mà cổng vẫn xanh.

     Nên cổng này đo trên NỘI DUNG THẬT đang chạy: quét `public/content`, chạy
     `answerMode` lên từng câu, và lấy đúng những mã thực sự xuất hiện. Thêm dạng
     câu mới vào sách là cổng thấy ngay, không phải nhớ sửa chỗ nào. */
  const fs = await import('node:fs');
  const path = await import('node:path');
  const { answerMode } = await import('../src/mon/toan/lib/flow.js');
  const { TEN_DINH_DANG } = await import('../src/mon/tienganh/lib/hoso.js');

  const goc = new URL('../public/content', import.meta.url).pathname;
  const tep = [];
  (function di(d) {
    for (const f of fs.readdirSync(d, { withFileTypes: true })) {
      const q = path.join(d, f.name);
      if (f.isDirectory()) di(q); else if (f.name.endsWith('.json')) tep.push(q);
    }
  }(goc));

  const dangToan = new Map();
  for (const t of tep) {
    let d; try { d = JSON.parse(fs.readFileSync(t, 'utf8')); } catch { continue; }
    const hang = [d];
    while (hang.length) {
      const x = hang.pop();
      if (Array.isArray(x)) { hang.push(...x); continue; }
      if (!x || typeof x !== 'object') continue;
      if (x.answerKey || x.format) {
        const m = answerMode(x);
        dangToan.set(m, (dangToan.get(m) || 0) + 1);
      }
      for (const v of Object.values(x)) if (v && typeof v === 'object') hang.push(v);
    }
  }

  /* Năm nhánh của `answerMode` đều có câu thật. Hụt một nhánh nghĩa là phép so
     trùng dưới đây đang soi thiếu một mã — phải kêu ở đây, không được im rồi báo
     "không trùng". */
  assert.equal(dangToan.size, 5,
    `đọc hụt dạng câu Toán: ${[...dangToan.keys()].join(' · ')}`);

  const dangTA = new Set(Object.keys(TEN_DINH_DANG));
  assert.ok(dangTA.size >= 5, `đọc hụt dạng câu Tiếng Anh: ${[...dangTA]}`);

  const trung = [...dangTA].filter((x) => dangToan.has(x));
  assert.deepEqual(trung, [], `hai môn trùng mã dạng câu: ${trung.join(', ')}`);
});
