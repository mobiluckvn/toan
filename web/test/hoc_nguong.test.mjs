import test from 'node:test';
import assert from 'node:assert/strict';

import {
  hocBKT, kiemTraCheo, hocNuaDoi, quetLuoiTheta, phanVi, khoangWilson,
  hocNguongHanhVi, dungDeXuat, hocMoiPhamVi,
} from '../functions/src/hocNguong.js';
import { BO_MAC_DINH, KHOANG, layNguong } from '../functions/src/nguong.js';

/**
 * CỔNG CHO HÀM HỌC NGƯỠNG — mục 3.8.3.
 *
 * ⚠ THỨ NGUY HIỂM Ở ĐÂY KHÔNG PHẢI MỘT CON SỐ SAI, MÀ LÀ MỘT ĐỀ XUẤT TRÔNG ĐÚNG.
 * Đề xuất đi thẳng tới chuyên gia và tới quyết định về cách dạy trẻ. Một con số có
 * cỡ mẫu 46 nhưng nằm trong một phạm vi 3.213 lượt trông đủ chuẩn mà đứng trên gần
 * như không có gì. Nên cổng ở đây canh CHỖ ĐỀ XUẤT BỊ TỪ CHỐI nhiều hơn canh chỗ nó
 * được đưa ra.
 */

/* Bộ sinh tất định — chạy hai lần phải ra hai kết quả y hệt. */
function tao(seed) {
  let s = seed >>> 0;
  return () => { s = (Math.imul(s, 1103515245) + 12345) >>> 0; return s / 4294967296; };
}

/**
 * Sinh chuỗi trả lời từ một bộ tham số BKT ĐÃ BIẾT.
 *
 * ⚠ TRẢI RA NHIỀU BUỔI, KHÔNG DỒN VÀO MỘT PHÚT. Bản đầu tôi đặt mọi lượt cách nhau
 * một phút, và `quetLuoiTheta` trả `null` — đúng, vì "công nhận sớm" theo định nghĩa
 * đòi câu đầu ở lần gặp sau CÁCH ÍT NHẤT MỘT NGÀY, mà dữ liệu bịa ấy không có cái
 * khoảng nghỉ nào. Một vỏ dữ liệu không giống thật thì cổng dựng trên nó chỉ canh
 * một thế giới không tồn tại.
 *
 * Nên: mỗi buổi `moiBuoi` lượt, các buổi cách nhau `cachNgay` ngày.
 */
function sinhChuoi(that, { soBe = 60, soNut = 6, soLuot = 12, seed = 7,
                           moiBuoi = 4, cachNgay = 2 } = {}) {
  const rnd = tao(seed);
  const NGAY = 86400000;
  const luots = [];
  for (let b = 0; b < soBe; b += 1) {
    for (let n = 0; n < soNut; n += 1) {
      let thao = rnd() < that.L0;
      for (let t = 0; t < soLuot; t += 1) {
        const buoi = Math.floor(t / moiBuoi);
        luots.push({
          learnerId: `be${b}`, bktUnit: `v_${n}`,
          correct: thao ? rnd() > that.slip : rnd() < that.guess,
          ts: Date.UTC(2026, 0, 1) + buoi * cachNgay * NGAY + (t % moiBuoi) * 60000,
        });
        if (!thao && rnd() < that.T) thao = true;
      }
    }
  }
  return luots;
}

const nhomCua = (luots) => {
  const m = new Map();
  for (const a of luots) {
    const k = `${a.learnerId}::${a.bktUnit}`;
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(a);
  }
  return m;
};
const beCua = (luots) => {
  const m = new Map();
  for (const [k, ds] of nhomCua(luots)) {
    const b = k.split('::')[0];
    if (!m.has(b)) m.set(b, []);
    m.get(b).push(ds);
  }
  return m;
};

/* ── EM ─────────────────────────────────────────────────────────────────── */

test('EM TÌM LẠI ĐƯỢC bộ tham số đã sinh ra dữ liệu', () => {
  /* Phép thử mạnh nhất cho một bộ ước lượng: sinh dữ liệu từ một bộ tham số BIẾT
     TRƯỚC rồi xem nó có tìm lại được không. Sai ở đâu đó trong công thức tiến–lùi
     thì phép này đỏ ngay, còn mọi phép "kết quả nằm trong [0,1]" thì vẫn xanh. */
  const that = { L0: 0.15, T: 0.12, slip: 0.08, guess: 0.25 };
  const chuoi = [...nhomCua(sinhChuoi(that, { soBe: 80, seed: 42 })).values()]
    .map((c) => c.map((x) => x.correct));
  const r = hocBKT(chuoi);
  for (const k of ['L0', 'T', 'slip', 'guess']) {
    assert.ok(Math.abs(r[k] - that[k]) < 0.03, `${k}: tìm ra ${r[k].toFixed(3)}, thật là ${that[k]}`);
  }
  assert.ok(r.vong > 1 && r.vong <= 200, 'phải hội tụ trong số vòng cho phép');
});

test('EM KHÔNG đi vào vùng suy biến (P(S) hay P(G) ≥ 0,5)', () => {
  /* Baker và cộng sự (2008): vượt 0,5 thì mô hình đổi vai hai trạng thái — "đã thạo"
     thành "hay trả lời sai". Con số vẫn khớp dữ liệu, chỉ là nó mô tả một thế giới
     ngược. Dữ liệu dưới đây cố tình dụ nó sang vùng ấy: bé toàn trả lời sai. */
  const chuoi = Array.from({ length: 50 }, () => Array.from({ length: 10 }, () => false));
  const r = hocBKT(chuoi);
  assert.ok(r.slip < 0.5, `slip suy biến: ${r.slip}`);
  assert.ok(r.guess < 0.5, `guess suy biến: ${r.guess}`);
});

test('EM chịu được chuỗi dài mà không tụt số về 0', () => {
  /* Không chia thang tỉ lệ thì tích các xác suất tụt rất nhanh và mọi tham số ra
     NaN. Chuỗi 400 lượt là quá đủ để lộ chuyện ấy. */
  const chuoi = [Array.from({ length: 400 }, (_, i) => i % 3 !== 0)];
  const r = hocBKT(chuoi);
  for (const k of ['L0', 'T', 'slip', 'guess']) assert.ok(Number.isFinite(r[k]), `${k} = ${r[k]}`);
});

test('EM trả `null` khi không có chuỗi nào, không ném', () => {
  assert.equal(hocBKT([]), null);
  assert.equal(hocBKT(null), null);
  assert.equal(hocBKT([[]]), null, 'chuỗi rỗng không phải một chuỗi');
});

/* ── KIỂM TRA CHÉO ──────────────────────────────────────────────────────── */

test('kiểm tra chéo chia theo NGƯỜI HỌC, và đòi đủ người để chia', () => {
  /* Chia theo lượt thì lượt của cùng một bé nằm cả hai bên, mô hình đã thấy bé ấy
     rồi, và AUC đo được cao hơn sự thật — cao có hệ thống nên không ai nghi. */
  const luots = sinhChuoi({ L0: 0.15, T: 0.12, slip: 0.08, guess: 0.25 }, { soBe: 40, seed: 3 });
  const r = kiemTraCheo(beCua(luots));
  assert.ok(r && r.soPhan === 5, 'phải chia đủ 5 phần');
  assert.ok(r.aucTrungBinh > 0.6, `AUC quá thấp: ${r.aucTrungBinh}`);

  const it = new Map([...beCua(luots)].slice(0, 3));
  assert.equal(kiemTraCheo(it), null, 'ít hơn 5 người học thì KHÔNG chia được — trả null, đừng bịa');
});

/* ── HỒI QUY BÁN RÃ ─────────────────────────────────────────────────────── */

test('hồi quy bán rã chỉ lấy lượt ĐẦU SAU NGHỈ ≥ 1 ngày', () => {
  /* Lượt trong cùng phiên không nói gì về việc quên, và chúng đông hơn hàng chục
     lần — đưa vào thì mọi h đều cho cùng một sai số. */
  const T0 = Date.UTC(2026, 0, 1);
  const trongPhien = Array.from({ length: 20 }, (_, i) => ({
    learnerId: 'b', bktUnit: 'v', correct: true, ts: T0 + i * 60000,
  }));
  assert.equal(hocNuaDoi(nhomCua(trongPhien), BO_MAC_DINH), null,
    'toàn lượt trong cùng phiên → không có mẫu nào');

  const coNghi = [...trongPhien, { learnerId: 'b', bktUnit: 'v', correct: false, ts: T0 + 10 * 86400000 }];
  const r = hocNuaDoi(nhomCua(coNghi), BO_MAC_DINH);
  assert.equal(r.coMau, 1);
  const [lo, hi] = KHOANG.NG06;
  assert.ok(r.h >= lo && r.h <= hi, 'h phải nằm trong khoảng hợp lệ của Bảng 3.19');
});

/* ── QUÉT LƯỚI ──────────────────────────────────────────────────────────── */

test('quét lưới trả về CẢ ĐƯỜNG CONG, không chỉ một con số', () => {
  /* «Cân bằng tốt nhất» đòi nói rõ một câu lớn bằng mấy câu nhỏ — đó là câu hỏi SƯ
     PHẠM, không dữ liệu nào trả lời được. Giấu phép cân bằng và chỉ đưa một con số
     là đưa một quyết định sư phạm dưới dạng một kết quả tính toán. */
  const luots = sinhChuoi({ L0: 0.15, T: 0.2, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 16, seed: 5 });
  const r = quetLuoiTheta(nhomCua(luots), BO_MAC_DINH);
  assert.ok(r && Array.isArray(r.duong) && r.duong.length > 5, 'phải kèm đường cong');
  assert.ok(r.lamda != null, 'phải ghi rõ phép cân bằng đã dùng');
  const [lo, hi] = KHOANG.NG07;
  assert.ok(r.theta >= lo && r.theta <= hi);
  for (const d of r.duong) {
    assert.ok(d.congNhanSom >= 0 && d.congNhanSom <= 1);
    assert.ok(d.soCau > 0);
  }
});

test('θ cao hơn thì phải tốn NHIỀU CÂU HƠN — đường cong đi đúng chiều', () => {
  /* Nếu đường cong đi ngược thì hoặc phép chạy lại sai, hoặc θ không còn là ngưỡng
     tinh thông nữa. Một đề xuất dựng trên đường cong sai thì sai theo hướng không
     ai nhìn ra từ con số cuối. */
  const luots = sinhChuoi({ L0: 0.1, T: 0.15, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 20, seed: 11 });
  const d = quetLuoiTheta(nhomCua(luots), BO_MAC_DINH).duong;
  const thap = d.filter((x) => x.theta <= 0.8);
  const cao = d.filter((x) => x.theta >= 0.95);
  if (thap.length && cao.length) {
    const tb = (ds) => ds.reduce((s, x) => s + x.soCau, 0) / ds.length;
    assert.ok(tb(cao) >= tb(thap), `θ cao mà tốn ít câu hơn: ${tb(cao)} < ${tb(thap)}`);
  }
});

/* ── PHÂN VỊ VÀ KHOẢNG TIN CẬY ──────────────────────────────────────────── */

test('phân vị nội suy đúng, và khoảng Wilson không nói điều bất khả', () => {
  assert.equal(phanVi([1, 2, 3, 4, 5], 0.5), 3);
  assert.equal(phanVi([1, 2, 3, 4], 0.5), 2.5, 'phải nội suy, không làm tròn xuống');
  assert.equal(phanVi([], 0.5), null);

  /* Khoảng Wald vỡ ở đúng chỗ hay gặp: tỉ lệ sát 0 hoặc 1, cỡ mẫu nhỏ — nó cho cận
     dưới ÂM hoặc cận trên QUÁ 1, tức một khoảng tin cậy nói điều không thể xảy ra. */
  for (const [d, t] of [[0, 10], [10, 10], [1, 5], [30, 100]]) {
    const [lo, hi] = khoangWilson(d, t);
    assert.ok(lo >= 0 && hi <= 1 && lo <= hi, `khoảng vô lý cho ${d}/${t}: [${lo}, ${hi}]`);
  }
  assert.equal(khoangWilson(0, 0), null);
});

test('ngưỡng hành vi KHÔNG kết luận khi nhóm quá ít mẫu', () => {
  const it = Array.from({ length: 5 }, (_, i) => ({ mode: 'chon', bac: 1, ms: 1000 * i }));
  assert.equal(hocNguongHanhVi(it), null, 'năm lượt không nói được gì về một dạng câu');
});

/* ── DỰNG ĐỀ XUẤT ───────────────────────────────────────────────────────── */

test('chưa đủ NG21 lượt thì KHÔNG sinh đề xuất nào', () => {
  const r = dungDeXuat(sinhChuoi({ L0: 0.1, T: 0.1, slip: 0.1, guess: 0.2 }, { soBe: 2, soNut: 1, soLuot: 5 }),
    BO_MAC_DINH);
  assert.equal(r.duMau, false);
  assert.deepEqual(r.deXuat, []);
  assert.match(r.viSao, /cần \d+ lượt/);
});

test('CỠ MẪU XÉT THEO TỪNG NGƯỠNG, không theo tổng phạm vi', () => {
  /* Mục 3.8.3: «với MỖI NGƯỠNG và mỗi phạm vi». Bản đầu tôi chốt ở tổng phạm vi, và
     nó cho ra đề xuất đổi θ với cỡ mẫu 46 trong một phạm vi 3.213 lượt — trông đủ
     chuẩn mà đứng trên gần như không có gì. */
  const luots = sinhChuoi({ L0: 0.1, T: 0.15, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 12, seed: 9 });
  const r = dungDeXuat(luots, BO_MAC_DINH);
  assert.equal(r.duMau, true);
  const toiThieu = layNguong(BO_MAC_DINH, 'NG21');
  for (const d of r.deXuat) {
    if (d.giaTriDeXuat === null) continue;
    assert.ok(d.coMau >= toiThieu,
      `${d.ma} đề xuất ${d.giaTriDeXuat} với chỉ ${d.coMau} mẫu, cần ${toiThieu}`);
  }
  const thieu = r.deXuat.filter((d) => d.thieuMau);
  for (const d of thieu) {
    assert.equal(d.giaTriDeXuat, null);
    assert.notEqual(d.giaTriTho, null, 'vẫn ghi giá trị tính thô, để thấy dữ liệu nghiêng về đâu');
    assert.match(d.canCu, /KHÔNG đề xuất/);
  }
});

test('giá trị NGOÀI KHOẢNG HỢP LỆ thì không đề xuất, và KHÔNG kẹp im lặng', () => {
  /* Bảng 3.19 gọi khoảng này là giới hạn CỨNG: thuật toán cũng không được vượt. Kẹp
     im lặng về biên là biến dấu hiệu «mô hình đang nói điều vô lý» thành một con số
     trông hợp lệ. Dữ liệu dưới đây có thời gian trả lời rất dài (bé để tab mở). */
  const T0 = Date.UTC(2026, 0, 1);
  const luots = [];
  for (let b = 0; b < 30; b += 1) {
    for (let t = 0; t < 12; t += 1) {
      luots.push({ learnerId: `be${b}`, bktUnit: 'v_1', correct: t % 2 === 0, ts: T0 + (b * 12 + t) * 60000,
        mode: 'so', bac: 1, ms: 600000 });
    }
  }
  const d = dungDeXuat(luots, BO_MAC_DINH).deXuat.find((x) => x.ma === 'NG16' && x.khoa === 'so');
  assert.ok(d, 'phải có đề xuất cho dạng câu `so`');
  assert.equal(d.giaTriDeXuat, null, 'ngoài khoảng thì KHÔNG đề xuất');
  assert.ok(d.ngoaiKhoang, 'và phải GHI LẠI là đã ra ngoài');
  assert.deepEqual(d.ngoaiKhoang.khoang, KHOANG.NG16);
});

test('mỗi đề xuất mang đủ thứ để TỰ BẢO VỆ', () => {
  /* Mục 3.8.3 đòi lưu kèm cỡ mẫu, phương pháp, và chỉ số trên nhật ký với giá trị cũ
     và mới. Thiếu phần cuối thì chuyên gia duyệt một con số trần, và «duyệt» khi ấy
     chỉ là bấm nút. */
  const luots = sinhChuoi({ L0: 0.1, T: 0.15, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 12, seed: 13 });
  for (const d of dungDeXuat(luots, BO_MAC_DINH).deXuat) {
    assert.ok(d.ma && d.phamVi, 'phải biết đang nói về ngưỡng nào, phạm vi nào');
    assert.ok(d.phuongPhap, `${d.ma} thiếu phương pháp`);
    assert.ok(Number.isFinite(d.coMau), `${d.ma} thiếu cỡ mẫu`);
    assert.ok(d.canCu, `${d.ma} thiếu căn cứ`);
    assert.equal(d.trangThai, 'cho', 'đề xuất sinh ra ở trạng thái CHỜ, không tự áp dụng');
    assert.notEqual(d.giaTriHienTai, undefined, `${d.ma} thiếu giá trị đang hành để so`);
  }
});

test('tham số BKT chỉ được đề xuất khi HƠN trên dữ liệu GIỮ LẠI', () => {
  /* Bộ khớp dữ liệu đã thấy mà kém hơn bộ đang hành trên dữ liệu giữ lại thì nó
     đang học thuộc, không phải học. Đo trên nhật ký thật 10-10: EM cho AUC giữ lại
     0,682 so với 0,735 của bộ đang hành — nên KHÔNG đề xuất, và đó là kết quả đúng. */
  const luots = sinhChuoi({ L0: 0.1, T: 0.15, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 12, seed: 17 });
  const ds = dungDeXuat(luots, BO_MAC_DINH).deXuat.filter((d) => ['NG01', 'NG02', 'NG03', 'NG04'].includes(d.ma));
  assert.equal(ds.length, 4, 'phải xét cả bốn tham số');
  for (const d of ds) {
    assert.match(d.phuongPhap, /CHIA THEO NGƯỜI HỌC/);
    if (d.giaTriDeXuat !== null) {
      assert.ok(d.chiSoSau?.aucTrungBinh > d.chiSoTruoc.auc,
        `${d.ma} đề xuất dù AUC giữ lại không hơn`);
    }
  }
});

test('học ở MỌI phạm vi, và phạm vi hẹp thiếu mẫu thì lặng lẽ bỏ qua', () => {
  /* Mục 3.8.3: «nếu chưa đủ, hàm học ở phạm vi rộng hơn». Phạm vi hẹp không đủ mẫu
     thì không sinh đề xuất — và vì phạm vi rộng vẫn chạy, ngưỡng ở đó vẫn được học. */
  const luots = sinhChuoi({ L0: 0.1, T: 0.15, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 12, seed: 19 })
    .map((a, i) => ({ ...a, mon: 'tienganh', khoiLop: i < 20 ? '3' : '5' }));
  const ra = hocMoiPhamVi(luots, BO_MAC_DINH);
  const toanHe = ra.find((x) => x.phamVi === 'toanHe');
  assert.equal(toanHe.duMau, true);
  const lop3 = ra.find((x) => x.phamVi === 'khoiLop' && x.khoa === '3');
  assert.equal(lop3.duMau, false, '20 lượt thì chưa đủ cho một khối lớp');
  assert.deepEqual(lop3.deXuat, []);
});

test('chạy hai lần cho KẾT QUẢ Y HỆT', () => {
  /* Hai lần chạy ra hai bộ đề xuất khác nhau thì chuyên gia không biết tin bộ nào,
     và không ai tái tạo lại được kết quả đã duyệt. */
  const luots = sinhChuoi({ L0: 0.1, T: 0.15, slip: 0.1, guess: 0.2 }, { soBe: 30, soLuot: 12, seed: 23 });
  const a = dungDeXuat(luots, BO_MAC_DINH, { bayGio: 1000 });
  const b = dungDeXuat(luots, BO_MAC_DINH, { bayGio: 1000 });
  assert.deepEqual(a, b);
});
