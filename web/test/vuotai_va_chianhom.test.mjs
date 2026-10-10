import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { theDenHan, theHoan, duocHoan, hoanVuotAi, demDenHan, BOX_NGAY } from '../src/mon/tienganh/lib/onlai.js';
import { nhomCua, laNhomThu, nhanNhom, THU_NGHIEM, NHOM } from '../src/chung/lib/chiaNhom.js';
import { nutCuaBai, buildReviewCards } from '../functions/src/schedule.js';
import { nguCanhLuot } from '../functions/src/bkt.js';
import { chiSoNG09, chiSoNG16, tinhThongKe } from '../functions/src/thongke.js';
import { BO_MAC_DINH } from '../functions/src/nguong.js';

/**
 * BỐN VIỆC NỐI THÊM — 10-10-2026.
 *
 *   C-08  nhánh VƯỢT ẢI của hàm chính sách nay CÓ CHỖ CHẠY (thẻ ôn)
 *   C-04  bản ghi lượt mang `bac` → nấc `bac` của thang phạm vi dùng được
 *   C-06  bản ghi lượt mang `sauPhuDao` → tách lượt tự gỡ khỏi lượt sau can thiệp
 *   C-09  cờ chia nhóm tất định cho KB4 và KB5
 */

const mt = (p) => Object.fromEntries(Object.entries(p).map(([k, v]) => [k, { p: v }]));
const the = (id, nut, them = {}) => ({ id, microId: `DL:TA3.${id}`, dueAt: 1, maNutDs: nut, box: 1, ...them });

/* ── C-08 · VƯỢT ẢI ─────────────────────────────────────────────────────── */

test('thẻ ôn của bài bé đã VỮNG HẲN thì hoãn, không bày ra', () => {
  /* Thẻ ôn là chỗ DUY NHẤT hệ thống bắt bé làm lại một bài đã đạt, nên cũng là chỗ
     duy nhất nhánh VƯỢT ẢI của hàm chính sách (mục 3.5.1) có nghĩa. Trước 10-10
     `duocVuotAi` và `viecTiepCuaBai` chỉ có cổng và công cụ gọi — tức với người học
     là chưa tồn tại. */
  const ds = [the('B01', ['a', 'b', 'c']), the('B02', ['a', 'b', 'c'])];
  const vung = mt({ a: 0.95, b: 0.95, c: 0.95 });

  assert.equal(theDenHan(ds, { quyen: 'ta3', bayGio: 9, mucThao: vung }).length, 0);
  assert.equal(theHoan(ds, { quyen: 'ta3', bayGio: 9, mucThao: vung }).length, 2);
  assert.equal(demDenHan(ds, { quyen: 'ta3', bayGio: 9, mucThao: vung }), 0,
    'con số trên thẻ mời phải khớp số thẻ bé thực sự gặp');
});

test('FAIL-CLOSED: thiếu dữ liệu thì bé CỨ ÔN', () => {
  /* Thà ôn thừa một bài đã vững (mất vài phút) còn hơn bỏ qua một bài bé chưa vững.
     Ba đường thiếu dữ liệu đều phải cho ra hành vi CŨ. */
  const ds = [the('B01', ['a', 'b', 'c'])];
  const vung = mt({ a: 0.95, b: 0.95, c: 0.95 });

  assert.equal(theDenHan(ds, { quyen: 'ta3', bayGio: 9 }).length, 1,
    'chưa tải xong mucThao → không hoãn');
  assert.equal(theDenHan([{ id: 'x', microId: 'DL:TA3.B01', dueAt: 1 }],
    { quyen: 'ta3', bayGio: 9, mucThao: vung }).length, 1,
    'thẻ đời cũ không có maNutDs → không hoãn');
  assert.equal(duocHoan(the('B01', []), vung), false, 'bài không có nút nào → không hoãn');
});

test('cửa vượt ải vẫn HẸP — một nút yếu là đủ để bé phải ôn', () => {
  const ds = [the('B01', ['a', 'b', 'c'])];
  assert.equal(theDenHan(ds, { quyen: 'ta3', bayGio: 9, mucThao: mt({ a: 0.95, b: 0.40, c: 0.95 }) }).length, 1);
  assert.equal(theDenHan(ds, { quyen: 'ta3', bayGio: 9, mucThao: mt({ a: 0.95, b: 0.95 }) }).length, 1,
    'nút chưa có số liệu là nút bé chưa từng làm — không được tính là vững');
  assert.equal(theDenHan([the('B01', ['a', 'b'])], { quyen: 'ta3', bayGio: 9, mucThao: mt({ a: 0.95, b: 0.95 }) }).length, 1,
    'bài quá ít nút thì lời "đã vững cả bài" vô nghĩa (NG15)');
});

test('hoãn KHÔNG được ghi như thể bé vừa ôn đúng', () => {
  /* Bé không trả lời câu nào. Ghi `lastResult: true` là bịa một lượt học không có
     thật vào sổ — mà sổ ấy là thứ bố mẹ đọc. */
  const t = hoanVuotAi({ id: 'x', box: 1, soLanOn: 4 }, 1000);
  assert.equal(t.lastResult, undefined, 'không được khai là bé ôn đạt');
  assert.equal(t.soLanOn, 4, 'số lần ôn KHÔNG tăng');
  assert.equal(t.box, 2, 'nhưng hộp vẫn giãn ra');
  assert.equal(t.hoanVuotAi, 1, 'và ghi rõ vì sao hộp giãn');
  assert.equal(t.dueAt, 1000 + BOX_NGAY[2] * 86400000);
});

test('hoãn KHÔNG xoá thẻ — quên thì thẻ quay lại', () => {
  /* Đẩy hộp chứ không xoá: phép quên vẫn chạy, bé nghỉ lâu thì P(L) tụt, vượt ải
     thôi đúng, và thẻ tới hạn trở lại. Xoá thì không có đường về. */
  const t = hoanVuotAi(the('B01', ['a', 'b', 'c']), 1000);
  assert.deepEqual(t.maNutDs, ['a', 'b', 'c'], 'thẻ còn nguyên');
  assert.equal(duocHoan(t, mt({ a: 0.95, b: 0.20, c: 0.95 })), false,
    'khi mức thạo tụt thì không hoãn nữa');
});

test('thẻ ôn mang danh sách nút của bài', () => {
  const bai = {
    practice: { pools: { warmup: [{ id: 'q1', maNut: 'v_a' }, { id: 'q2', maNutDs: ['v_b', 'v_c'] }] } },
    assessment: { items: [{ id: 'q3', maNut: 'v_a' }] },
    /* `buildReviewCards` chỉ tạo thẻ cho những mốc khai trong `spacedReview` — bài
       không khai lịch ôn thì không có thẻ nào, và đó là hành vi đúng. */
    spacedReview: { schedule: ['+1 ngày: flashcards', '+3 ngày: items', '+7 ngày: items'] },
  };
  assert.deepEqual(nutCuaBai(bai).sort(), ['v_a', 'v_b', 'v_c']);
  const cards = buildReviewCards({ learnerId: 'b', microId: 'DL:TA3.B01', lesson: bai, at: 0 });
  assert.ok(cards.length > 0);
  for (const c of cards) assert.deepEqual(c.maNutDs.sort(), ['v_a', 'v_b', 'v_c']);
});

/* ── C-04 · NẤC `bac` ───────────────────────────────────────────────────── */

test('bậc của câu vào ngữ cảnh phạm vi', () => {
  assert.equal(nguCanhLuot({ bac: 3 }).bac, '3');
  assert.equal(nguCanhLuot({ bac: 0 }).bac, '0', 'bậc 0 là một bậc, không phải thiếu');
  assert.equal(nguCanhLuot({}).bac, undefined, 'dòng v ≤ 5 không có bậc → bỏ qua nấc ấy');
  assert.equal(nguCanhLuot({ bac: null }).bac, undefined);
});

test('chỉ số hành vi gom theo CẶP (dạng câu, bậc) — Bảng 3.22', () => {
  const l = (mode, bac, ms) => ({ learnerId: 'b', bktUnit: 'v', correct: true, ts: 1, mode, bac, ms });
  const r = chiSoNG16([l('chon', 1, 1000), l('chon', 1, 99000), l('chon', 4, 1000), l('go', null, 1000)],
    BO_MAC_DINH);
  assert.equal(r.theoDangCau['chon·1'].coMau, 2);
  assert.equal(r.theoDangCau['chon·1'].tiLeBeTac, 0.5);
  assert.equal(r.theoDangCau['chon·4'].coMau, 1);
  assert.equal(r.theoDangCau['go·—'].coMau, 1, 'dòng không có bậc vẫn đếm được, và KHÔNG lẫn vào nhóm có bậc');
});

/* ── C-06 · TÁCH LƯỢT SAU CAN THIỆP ─────────────────────────────────────── */

test('NG09 tách lượt TỰ GỠ khỏi lượt SAU CAN THIỆP', () => {
  /* Đo lần đầu trên dữ liệu thật ra dãy bật ngược đúng tại k = ngưỡng đang hành,
     vì lượt kế tiếp ở đó là lượt sau khi bé được giúp. `tiLeTuGo` chỉ đếm lượt
     KHÔNG nằm sau can thiệp — đó mới là "bé có tự gỡ được không". */
  const nut = (kq, sau) => kq.map((c, i) => ({
    learnerId: 'b', bktUnit: 'v', correct: c === 'd', ts: i * 1000, sauPhuDao: sau[i],
  }));
  const m = new Map([['b::v', nut(['s', 's', 's', 'd'], [false, false, false, true])]]);
  const r = chiSoNG09(m, BO_MAC_DINH);

  assert.equal(r.k3.coMau, 1, 'vẫn đếm đủ mọi lượt');
  assert.equal(r.k3.tiLeDung, 1);
  assert.equal(r.k3.coMauTuGo, 0, 'nhưng lượt sau can thiệp KHÔNG vào phép đo tự gỡ');
  assert.equal(r.k3.tiLeTuGo, null, 'chưa có mẫu tự gỡ thì nói "chưa biết", đừng trả 1');
  assert.equal(r.k3.sauCanThiep, true);
});

test('dòng nhật ký đời cũ (v ≤ 5) vẫn đếm y như trước', () => {
  /* Không có cờ `sauPhuDao` thì rơi vào `tuGo` — cách đọc cũ giữ nguyên, không dòng
     nào bị mất. Một bản ghi đời cũ phải đọc được, chứ không được ném. */
  const m = new Map([['b::v', ['s', 's', 'd'].map((c, i) => ({
    learnerId: 'b', bktUnit: 'v', correct: c === 'd', ts: i * 1000,
  }))]]);
  const r = chiSoNG09(m, BO_MAC_DINH);
  assert.equal(r.k2.coMau, 1);
  assert.equal(r.k2.coMauTuGo, 1);
  assert.equal(r.k2.tiLeTuGo, r.k2.tiLeDung);
});

test('hai trường mới đi được tới tận tài liệu thống kê', () => {
  const ds = [];
  for (let i = 0; i < 6; i += 1) {
    ds.push({ learnerId: 'b', bktUnit: 'v', correct: i % 2 === 0, ts: i * 1000,
      mode: 'chon', bac: 2, ms: 4000, sauPhuDao: i > 3 });
  }
  const r = tinhThongKe(ds, BO_MAC_DINH);
  assert.ok(r.NG16.theoDangCau['chon·2'], 'gom theo cặp (dạng, bậc)');
  assert.ok('coMauTuGo' in r.NG09.k1, 'NG09 mang cả hai phép đếm');
});

/* ── C-09 · CỜ CHIA NHÓM ────────────────────────────────────────────────── */

test('mọi thử nghiệm MẶC ĐỊNH TẮT — hệ thống chạy y như trước', () => {
  /* Bật một thử nghiệm là QUYẾT ĐỊNH về việc dạy trẻ, không phải việc kỹ thuật:
     `kb4_phudao_llm` nới ràng buộc R3 (câu do mô hình soạn tới tay bé trước khi
     người lớn duyệt), `kb5_zpd` để nhóm đối chứng học bằng thứ tự kém hơn. */
  for (const [ten, t] of Object.entries(THU_NGHIEM)) {
    assert.equal(t, 0, `thử nghiệm ${ten} đang BẬT — phải là một quyết định có chủ ý`);
    assert.equal(nhomCua('be1', ten), NHOM.doiChung);
  }
  assert.equal(nhanNhom('be1'), null, 'tắt hết thì KHÔNG ghi nhãn nào vào nhật ký');
});

test('chia nhóm TẤT ĐỊNH — cùng bé, cùng nhóm, mọi lúc mọi máy', () => {
  /* Dùng `Math.random()` thì bé đổi nhóm mỗi lần mở app và phép so hai nhóm mất
     sạch nghĩa — mất trong im lặng, vì số liệu vẫn ra đẹp. */
  for (let i = 0; i < 50; i += 1) {
    const a = nhomCua(`be${i}`, 'kb5_zpd', 0.5);
    assert.equal(a, nhomCua(`be${i}`, 'kb5_zpd', 0.5));
    assert.ok(a === NHOM.thu || a === NHOM.doiChung);
  }
});

test('hai thử nghiệm chia ĐỘC LẬP với nhau', () => {
  /* Dùng chung một phép băm thì bé ở nhóm A của KB5 cũng luôn ở nhóm A của KB4 —
     hai phép đo dính vào nhau và không tách được tác dụng của từng thứ. */
  let khac = 0;
  const n = 2000;
  for (let i = 0; i < n; i += 1) {
    if (nhomCua(`be${i}`, 'kb4_phudao_llm', 0.5) !== nhomCua(`be${i}`, 'kb5_zpd', 0.5)) khac += 1;
  }
  assert.ok(khac / n > 0.45 && khac / n < 0.55, `hai thử nghiệm dính nhau: khác ${(khac / n).toFixed(3)}`);
});

test('tỉ lệ chia đúng, và các trường hợp biên cho ra HÀNH VI CŨ', () => {
  let thu = 0;
  const n = 10000;
  for (let i = 0; i < n; i += 1) if (laNhomThu(`be${i}`, 'kb5_zpd', 0.3)) thu += 1;
  assert.ok(Math.abs(thu / n - 0.3) < 0.02, `tỉ lệ lệch: ${thu / n}`);

  assert.equal(nhomCua(null, 'kb5_zpd', 0.5), NHOM.doiChung, 'chưa biết mã bé → đối chứng');
  assert.equal(nhomCua('be1', 'khong_co_thu_nghiem_nay'), NHOM.doiChung, 'thử nghiệm chưa khai → đối chứng');
  assert.equal(nhomCua('be1', 'kb5_zpd', 1), NHOM.thu);
  assert.equal(nhomCua('be1', 'kb5_zpd', 0), NHOM.doiChung);
});

/* ── phiên bản bản ghi ──────────────────────────────────────────────────── */

test('hai môn khai CÙNG một phiên bản bản ghi, và đã lên 6', () => {
  const doc = (d) => readFileSync(new URL(d, import.meta.url), 'utf8');
  const so = (s) => Number(s.match(/PHIEN_BAN_BAN_GHI = (\d+)/)[1]);
  const ta = so(doc('../src/mon/tienganh/lib/suKien.js'));
  const toan = so(doc('../src/mon/toan/lib/sync.js'));
  assert.equal(ta, toan, 'hai môn lệch số thì bên đọc nhật ký phải nhớ hai luật');
  assert.ok(ta >= 6, 'thêm trường vào bản ghi thì phải lên phiên bản');
});
