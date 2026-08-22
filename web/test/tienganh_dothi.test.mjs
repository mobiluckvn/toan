/**
 * CỔNG · ĐỒ THỊ LÚC CHẠY VÀ LAN TRUYỀN CHẨN ĐOÁN (mục 2.2.1 · 2.3.3).
 *
 * Ba chuyện canh ở đây, xếp theo mức nguy:
 *
 *  1. CHU TRÌNH. Một vòng lặp không đáy ở phép duyệt nghĩa là máy của bé ĐỨNG
 *     HÌNH giữa buổi học. Hôm nay đồ thị không có chu trình, nhưng thêm một cạnh
 *     sai là có ngay — nên canh cả dữ liệu lẫn phép duyệt.
 *
 *  2. TUYÊN THẠO KHỐNG. Lan truyền xuôi mà đẩy một nút lên "đã thạo" khi bé chưa
 *     làm câu nào của nút ấy thì hệ thống bỏ qua bài bé chưa từng học, im lặng.
 *
 *  3. HƯỚNG CẠNH. Đảo nhầm hai đầu thì chẩn đoán chạy đúng chiều ngược lại: bé
 *     sai ở unit 1 mà hệ thống đi tìm nguyên nhân ở unit 20 — sai mà nghe vẫn có
 *     lý, nên không ai cãi.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  truoc, sau, duyetNguoc, duyetXuoi, coNut, loaiNut, lopNut, datDoThi, CANH_THAT,
  baiCuaNut, baiTienQuyet,
} from '../src/mon/tienganh/lib/doThi.js';
import { vonTu } from '../src/mon/tienganh/lib/phongnoi.js';
import {
  nutGocRe, congHuong, maTranTrangThai, ALPHA, BETA, NGUONG_TRAN, P_MAC_DINH,
} from '../src/mon/tienganh/lib/lantruyen.js';
import { NGUONG_THAO } from '../src/mon/tienganh/lib/zpd.js';

const THAT = JSON.parse(readFileSync(
  new URL('../public/content/tienganh/do_thi.json', import.meta.url), 'utf8'));

const mt = (o) => Object.fromEntries(Object.entries(o).map(([k, p]) => [k, { p }]));

/* Đồ thị giả: a → b → c (a phải có trước b, b trước c), và d đứng riêng. */
const GIA = {
  nut: { a: { t: 'vocabulary', g: 1 }, b: { t: 'vocabulary', g: 1 },
         c: { t: 'grammar', g: 2 }, d: { t: 'vocabulary', g: 1 } },
  canh: [
    { can: 'a', truoc_khi: 'b', loai: 'ban_do' },
    { can: 'b', truoc_khi: 'c', loai: 'ban_do' },
    { can: 'd', truoc_khi: 'b', loai: 'trong_bai' },
  ],
};

/* ── dữ liệu thật ────────────────────────────────────────────────────────── */

test('đồ thị con có thật, và đủ nhỏ để tải mỗi phiên', () => {
  const kb = readFileSync(
    new URL('../public/content/tienganh/do_thi.json', import.meta.url)).length / 1024;
  assert.ok(kb < 250, `đồ thị ${kb.toFixed(0)} KB — máy con tải mỗi lần mở quyển`);
  assert.ok(Object.keys(THAT.nut).length > 1000);
  assert.ok(THAT.canh.length > 200);
});

test('⚠ KHÔNG CÓ CHU TRÌNH trong đồ thị thật', () => {
  const ke = new Map();
  for (const c of THAT.canh) {
    if (!ke.has(c.can)) ke.set(c.can, []);
    ke.get(c.can).push(c.truoc_khi);
  }
  const mau = new Map();
  const chuTrinh = [];
  const di = (u) => {
    mau.set(u, 1);
    for (const v of (ke.get(u) || [])) {
      if (mau.get(v) === 1) chuTrinh.push(`${u} → ${v}`);
      else if (!mau.has(v)) di(v);
    }
    mau.set(u, 2);
  };
  for (const u of Object.keys(THAT.nut)) if (!mau.has(u)) di(u);
  assert.deepEqual(chuTrinh, [],
    'chu trình → phép duyệt lặp không đáy → máy của bé đứng hình giữa buổi học');
});

test('không cạnh nào trỏ vào nút không có trong đồ thị', () => {
  const mo = THAT.canh.filter((c) => !THAT.nut[c.can] || !THAT.nut[c.truoc_khi]);
  assert.deepEqual(mo, [],
    'cạnh trỏ vào hư không → phép duyệt ngược dừng giữa chừng mà không gì báo');
});

test('⚠ HƯỚNG CẠNH đúng như ví dụ luận văn nêu ở mục 2.2.2c', () => {
  const c = THAT.canh.find((x) => x.can === 'v_g3_ustarter_ten');
  assert.ok(c, 'mất cạnh số đếm — ví dụ đích danh của luận văn');
  assert.equal(c.truoc_khi, 'v_g3_u11_eleven',
    'phải là "cần ten TRƯỚC KHI học eleven", không phải ngược lại');
});

test('mọi maNut trong tệp bài đều có mặt trong đồ thị', async () => {
  const { readdirSync } = await import('node:fs');
  const thieu = new Set();
  for (const q of ['ta1', 'ta2', 'ta3', 'ta4', 'ta5']) {
    for (const f of readdirSync(new URL(`../public/content/${q}/`, import.meta.url))) {
      if (!/^DL_TA\d_B\d+\.json$/.test(f)) continue;
      const b = JSON.parse(readFileSync(
        new URL(`../public/content/${q}/${f}`, import.meta.url), 'utf8'));
      const it = [...Object.values(b.practice?.pools || {}).flat(),
                  ...(b.assessment?.items || [])];
      for (const i of it) if (i.maNut && !THAT.nut[i.maNut]) thieu.add(i.maNut);
    }
  }
  /* `sp_g3_starter_1` là mẫu SOẠN THÊM, không có nút bản đồ — ngoại lệ đã khai ở
     `tienganh_manut.test.mjs`. Đồ thị con lấy từ bản đồ nên cũng không có nó. */
  thieu.delete('sp_g3_starter_1');
  assert.deepEqual([...thieu], [],
    'câu trỏ vào nút không có trong đồ thị → lan truyền chẩn đoán không đi được');
});

/* ── phép duyệt ──────────────────────────────────────────────────────────── */

test('truoc/sau đọc đúng hướng, và BỎ cạnh trong_bai', () => {
  assert.deepEqual(truoc(GIA, 'b'), ['a'], 'cạnh trong_bai (d→b) không được tính');
  assert.deepEqual(sau(GIA, 'a'), ['b']);
  assert.deepEqual(truoc(GIA, 'b', { keCaTrongBai: true }).sort(), ['a', 'd']);
  assert.deepEqual(truoc(GIA, 'a'), []);
  assert.deepEqual(truoc(GIA, null), []);
});

test('duyệt nhiều bước, mang theo số bước', () => {
  assert.deepEqual(duyetNguoc(GIA, 'c'), [{ ma: 'b', buoc: 1 }, { ma: 'a', buoc: 2 }]);
  assert.deepEqual(duyetXuoi(GIA, 'a'), [{ ma: 'b', buoc: 1 }, { ma: 'c', buoc: 2 }]);
  assert.deepEqual(duyetNguoc(GIA, 'c', { sauToiDa: 1 }), [{ ma: 'b', buoc: 1 }]);
});

test('⚠ CHU TRÌNH thì phép duyệt vẫn phải DỪNG', () => {
  const vong = {
    nut: { x: {}, y: {}, z: {} },
    canh: [
      { can: 'x', truoc_khi: 'y', loai: 'ban_do' },
      { can: 'y', truoc_khi: 'z', loai: 'ban_do' },
      { can: 'z', truoc_khi: 'x', loai: 'ban_do' },
    ],
  };
  /* ⚠ ĐO RỒI MỚI NÓI: gỡ `daTham` ra thì KHÔNG treo — trần `sauToiDa` giữ cho nó
     dừng. Cái hỏng là kết quả: cùng một nút trả về nhiều lần, và số nhánh phình
     theo cấp số nhân. Phép canh dưới đây bắt đúng chuyện đó (đòi ĐÚNG 2 nút), chứ
     không phải bắt treo máy. */
  const r = duyetNguoc(vong, 'x', { sauToiDa: 50 });
  assert.equal(r.length, 2);
  assert.deepEqual(r.map((x) => x.ma).sort(), ['y', 'z']);
});

test('đồ thị rỗng hay hỏng thì trả rỗng, không ném', () => {
  for (const d of [null, undefined, {}, { nut: {} }, { canh: null }]) {
    assert.deepEqual(duyetNguoc(d, 'a'), []);
    assert.deepEqual(truoc(d, 'a'), []);
  }
  assert.equal(coNut(null, 'a'), false);
  assert.equal(loaiNut(GIA, 'c'), 'grammar');
  assert.equal(lopNut(GIA, 'c'), 2);
  assert.equal(lopNut(GIA, 'khong_co'), null);
});

test('CANH_THAT không gồm trong_bai', () => {
  assert.ok(CANH_THAT.has('ban_do') && CANH_THAT.has('noi_bai'));
  assert.ok(!CANH_THAT.has('trong_bai'),
    'thứ tự đọc trong cùng một bài KHÔNG phải cửa ải — lấy nó đi khoá bài là chặn '
    + 'bé giữa chính bài đang học');
});

/* ── lan truyền ──────────────────────────────────────────────────────────── */

test('nút gốc rễ: càng xa chỗ sai càng bớt đáng ngờ', () => {
  const m = mt({ a: 0.2, b: 0.2 });
  const r = nutGocRe(GIA, m, 'c');
  assert.deepEqual(r.map((x) => x.ma), ['b', 'a'], 'b cách 1 bước, a cách 2');
  assert.ok(Math.abs(r[0].doNgo - ALPHA * 0.8) < 1e-9);
  assert.ok(Math.abs(r[1].doNgo - (ALPHA ** 2) * 0.8) < 1e-9);
});

test('nút bé ĐÃ THẠO bị loại khỏi danh sách nghi', () => {
  /* Giữ lại là màn hình có thể bày ra "chỗ hổng gốc rễ" trỏ vào một thứ bé làm
     đúng mãi — bố mẹ và cô giáo đọc xong sẽ không tin cái bảng ấy nữa. */
  const r = nutGocRe(GIA, mt({ b: 0.95, a: 0.2 }), 'c');
  assert.deepEqual(r.map((x) => x.ma), ['a']);
});

test('nút CHƯA CÓ SỐ vẫn đáng ngờ, nhưng không tuyệt đối', () => {
  const r = nutGocRe(GIA, mt({ b: 0.5 }), 'c');   // a không có số
  const a = r.find((x) => x.ma === 'a');
  assert.ok(a, 'tiên quyết bé chưa từng chạm là lý do hay gặp nhất');
  assert.equal(a.p, P_MAC_DINH, 'chưa có tin vẫn khác đã-đo-và-thấy-hổng');
});

test('⚠ CỘNG HƯỞNG KHÔNG ĐƯỢC TUYÊN THẠO KHỐNG', () => {
  /* Bé thạo `a`. `b` và `c` dựng trên nó, nhưng bé CHƯA LÀM câu nào của chúng.
     Đẩy chúng lên "đã thạo" là hệ thống bỏ qua bài bé chưa từng học, im lặng. */
  const r = congHuong(GIA, mt({ a: 0.99 }));
  for (const [ma, p] of Object.entries(r)) {
    assert.ok(p < NGUONG_THAO, `${ma} bị cộng hưởng đẩy tới ngưỡng thạo (${p})`);
    assert.ok(p <= NGUONG_TRAN, `${ma} vượt trần cộng hưởng`);
  }
  assert.ok(r.b > P_MAC_DINH, 'phải có cộng thật, nếu không phép này vô nghĩa');
});

test('cộng hưởng nhỏ dần theo bước, và bỏ qua nút đã thạo', () => {
  const r = congHuong(GIA, mt({ a: 1 }));
  assert.ok(r.b > r.c, 'nút gần nguồn phải được cộng nhiều hơn nút xa');
  const r2 = congHuong(GIA, mt({ a: 1, b: 0.9 }));
  assert.equal(r2.b, undefined, 'nút đã thạo thì cộng hưởng không có việc gì làm');
});

test('cộng hưởng KHÔNG sửa sổ gốc', () => {
  const m = mt({ a: 0.99 });
  congHuong(GIA, m);
  assert.equal(m.b, undefined, 'sửa sổ gốc thì mức thạo thật lẫn với mức suy ra');
});

test('ma trận trạng thái: nút yếu nhất trước, kèm nút gốc rễ', () => {
  const m = mt({ c: 0.2, b: 0.4, a: 0.9 });
  const r = maTranTrangThai(GIA, m);
  assert.deepEqual(r.map((x) => x.ma), ['c', 'b']);
  assert.equal(r[0].goc?.ma, 'b', 'sai ở c thì gốc đáng ngờ nhất là b');
  assert.ok(!r.some((x) => x.ma === 'a'), 'nút bé vững không phải "đang chật vật"');
});

test('ma trận CHỈ nhận nút đã có số', () => {
  /* Nút bé chưa từng chạm không phải "đang chật vật" — gộp vào là bảng đầy những
     dòng nói "em chưa học phần này", đúng nhưng vô dụng, và dìm mất dòng đáng xem. */
  const r = maTranTrangThai(GIA, { c: { p: 0.2 }, d: {} });
  assert.deepEqual(r.map((x) => x.ma), ['c']);
});

test('hằng số có nghĩa và trong khoảng hợp lệ', () => {
  assert.ok(ALPHA > 0 && ALPHA < 1, 'α phải làm độ ngờ GIẢM theo bước');
  assert.ok(BETA > 0 && BETA < 0.2, 'β lớn quá là cộng hưởng lấn át số đo thật');
  assert.ok(NGUONG_TRAN < NGUONG_THAO);
});

/* ── RETRIEVER: đồ thị làm nguồn thứ hai cho vốn từ ────────────────────────── */

const GIA_B = {
  nut: {
    a: { t: 'vocabulary', b: 'DL:TA1.B11' },
    b: { t: 'vocabulary', b: 'DL:TA2.B02' },
    c: { t: 'grammar', b: 'DL:TA2.B05' },
  },
  canh: [
    { can: 'a', truoc_khi: 'b', loai: 'ban_do' },
    { can: 'b', truoc_khi: 'c', loai: 'ban_do' },
  ],
};

test('bài tiên quyết: đi từ nút sang BÀI dạy nút ấy', () => {
  assert.equal(baiCuaNut(GIA_B, 'a'), 'DL:TA1.B11');
  assert.deepEqual(baiTienQuyet(GIA_B, ['c'], { boQua: 'DL:TA2.B05' }),
    ['DL:TA2.B02', 'DL:TA1.B11']);
  assert.deepEqual(baiTienQuyet(GIA_B, ['a']), []);
  assert.deepEqual(baiTienQuyet(GIA_B, []), []);
});

test('bài tiên quyết vươn được sang QUYỂN KHÁC', () => {
  /* Cửa sổ "ba bài gần nhất" nới bao nhiêu cũng không tới, vì nó nới trong CÙNG
     quyển. Đây là ca `cross_grade` mà luận văn nêu ở mục 2.2.2. */
  const r = baiTienQuyet(GIA_B, ['b'], { boQua: 'DL:TA2.B02' });
  assert.deepEqual(r, ['DL:TA1.B11']);
});

test('trên đồ thị THẬT, tiên quyết xuyên quyển có tồn tại', () => {
  const nuts = Object.keys(THAT.nut).filter((n) => THAT.nut[n].b);
  let xuyen = 0;
  for (const n of nuts) {
    const q = String(THAT.nut[n].b).split('.')[0];
    for (const b of baiTienQuyet(THAT, [n], { boQua: THAT.nut[n].b, sauToiDa: 1 })) {
      if (String(b).split('.')[0] !== q) xuyen += 1;
    }
  }
  assert.ok(xuyen > 0,
    'không có tiên quyết xuyên quyển nào — nếu thế thì cả việc dựng đồ thị lúc '
    + 'chạy chẳng thêm được gì so với cửa sổ tuần tự');
});

/* ── vonTu: GỘP hai nguồn, và không được hẹp đi ───────────────────────────── */

const baiGia = (id, tu) => ({
  id, title: id,
  knowledgeCore: { vocabulary: tu.map((t) => ({ tu: t, nghia: t })), mauCauDs: [] },
});

test('⚠ ĐỒ THỊ CHỈ ĐƯỢC LÀM RỘNG THÊM, KHÔNG ĐƯỢC LÀM HẸP ĐI', () => {
  /* Đo trên 94 bài: nếu THAY cửa sổ tuần tự bằng đồ thị thì 87 bài vốn từ hẹp đi,
     nhiều bài về rỗng — cô giáo máy cụt từ. Nên phép này canh đúng một điều: thêm
     nguồn đồ thị vào không bao giờ được làm mất bài nào của lối cũ. */
  const nay = baiGia('DL:TA2.B05', ['now']);
  const cu = [baiGia('DL:TA2.B03', ['old1']), baiGia('DL:TA2.B04', ['old2'])];
  const tq = [baiGia('DL:TA1.B11', ['xa'])];
  const datCu = () => true;

  const khongDT = vonTu({ baiNay: nay, baiCu: cu, daDat: true, datCu });
  const coDT = vonTu({ baiNay: nay, baiCu: cu, baiTQ: tq, daDat: true, datCu });

  const ten = (v) => v.on.map((x) => x.id);
  for (const b of ten(khongDT)) {
    assert.ok(ten(coDT).includes(b), `thêm đồ thị làm MẤT bài ${b} của lối cũ`);
  }
  assert.ok(ten(coDT).includes('DL:TA1.B11'), 'bài tiên quyết xa không được thêm vào');
  assert.ok(coDT.on.length > khongDT.on.length);
});

test('⚠ BÀI BÉ CHƯA ĐẠT thì KHÔNG được vào vốn, dù đồ thị bảo là tiên quyết', () => {
  /* Bỏ chốt này là cô giáo máy nói bằng từ bé chưa từng học — tự tay chọc thủng
     tầng chống ảo giác từ bên trong, đúng cùng dạng với lỗi sở thích ở Đợt 0. */
  const nay = baiGia('DL:TA2.B05', ['now']);
  const tq = [baiGia('DL:TA1.B11', ['chuaHoc'])];
  const v = vonTu({
    baiNay: nay, baiCu: [], baiTQ: tq, daDat: true, datCu: () => false,
  });
  assert.deepEqual(v.on, []);
  const moi = [...v.loi.tu, ...v.on.flatMap((x) => x.tu)].map((t) => t.tu);
  assert.ok(!moi.includes('chuaHoc'));
});

test('bài tiên quyết TRÙNG với cửa sổ tuần tự thì không đắp hai lần', () => {
  const nay = baiGia('DL:TA2.B05', ['now']);
  const cu = [baiGia('DL:TA2.B04', ['old'])];
  const v = vonTu({
    baiNay: nay, baiCu: cu, baiTQ: [baiGia('DL:TA2.B04', ['old'])],
    daDat: true, datCu: () => true,
  });
  assert.equal(v.on.length, 1, 'một bài xuất hiện hai lần chỉ làm lời dặn dài ra');
});

test('chưa đạt bài hiện tại thì KHÔNG mở rộng vốn, kể cả có đồ thị', () => {
  const v = vonTu({
    baiNay: baiGia('DL:TA2.B05', ['now']),
    baiCu: [baiGia('DL:TA2.B04', ['old'])],
    baiTQ: [baiGia('DL:TA1.B11', ['xa'])],
    daDat: false, datCu: () => true,
  });
  assert.deepEqual(v.on, []);
  assert.equal(v.moRong, false);
});

test('⚠ HÌNH DẠNG TRẢ VỀ của vonTu KHÔNG ĐỔI', () => {
  /* `cauHopLe()` và `loiVietHopLe()` — cả tầng chống ảo giác — ăn thẳng kết quả
     này. Đổi hình dạng là gãy tầng ấy, mà gãy thì cô giáo máy nói gì cũng bị bác
     và buổi học đứng im. */
  const v = vonTu({
    baiNay: baiGia('DL:TA2.B05', ['now']), baiCu: [], baiTQ: [], daDat: true,
    datCu: () => true,
  });
  assert.deepEqual(Object.keys(v).sort(), ['loi', 'moRong', 'on']);
  assert.deepEqual(Object.keys(v.loi).sort(), ['cau', 'cauSach', 'id', 'ten', 'tu']);
  assert.ok(Array.isArray(v.on));
});

test('datDoThi chỉ nhận đồ thị đúng hình dạng', () => {
  datDoThi({ nut: { q: {} }, canh: [] });
  datDoThi(null);
  assert.deepEqual(truoc({ nut: {}, canh: [] }, 'q'), []);
});
