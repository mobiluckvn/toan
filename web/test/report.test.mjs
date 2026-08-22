/** Kiểm chính sách adaptive & sổ phụ huynh — node test/report.test.mjs */
import fs from 'fs';
import {
  startLevel, nextLevel, pickMicro, pendingExam, planSession, weakestUnits, keyOf, masteryOfMicro,
} from '../src/mon/toan/lib/adaptive.js';
import { emptyProgress, recordMicro, recordChapter } from '../src/mon/toan/lib/progress.js';
import { allMicroIds, chapterOf } from '../src/mon/toan/lib/noiDung.js';
import {
  minutesStudied, phutHoc, topTraps, stuckItems, buildParentReport, reportHeadline, inRange,
  duongCongHoc,
} from '../functions/src/report.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const list = allMicroIds();
const index = JSON.parse(fs.readFileSync('public/content/index_micro.json', 'utf8'));
const PASS = { pass: true, mustOK: true, right: 3, total: 3 };

/* ── chọn mức luyện theo mức thạo ── */
t('chưa có dữ liệu → khởi động', startLevel(null) === 'warmup');
t('p = 0,2 → khởi động', startLevel(0.2) === 'warmup');
t('p = 0,55 → cơ bản', startLevel(0.55) === 'standard');
t('p = 0,8 → thử thách', startLevel(0.8) === 'challenge');
t('đúng 2 câu liên tiếp thì lên mức', nextLevel('warmup', 2) === 'standard');
t('đúng 1 câu chưa lên', nextLevel('warmup', 1) === 'warmup');
t('đã ở mức cao nhất thì giữ nguyên', nextLevel('challenge', 5) === 'challenge');

/* ── chỉ mục nối micro với đơn vị kỹ năng ── */
t('chỉ mục có đủ 168 micro', Object.keys(index).length === 168);
const mid = 'DL:KSN5Q1.B49.M1';
t('đọc được bktUnit từ chỉ mục', !!index[keyOf(mid)]?.bktUnit);
const unit = index[keyOf(mid)].bktUnit;
t('đọc mức thạo theo micro', masteryOfMicro({ [unit]: { p: 0.6 } }, mid, index) === 0.6);

/* ── chọn bài tiếp theo ── */
let P = emptyProgress();
t('bắt đầu từ bài đầu tiên', pickMicro({ progress: P, index, list }).microId === list[0]);
P = recordMicro(P, list[0], PASS);
t('học xong bài 1 → gợi ý bài 2', pickMicro({ progress: P, index, list }).microId === list[1]);

/* bài đã đạt nhưng ĐÃ QUÊN (mức thạo tụt) thì được gợi ý học lại */
const u0 = index[keyOf(list[0])].bktUnit;
const forgot = pickMicro({ progress: P, mastery: { [u0]: { p: 0.4 } }, index, list });
t('bài đã đạt mà quên → gợi ý ôn lại', forgot.microId === list[0] && forgot.reason === 'đã quên bớt');
const remembered = pickMicro({ progress: P, mastery: { [u0]: { p: 0.92 } }, index, list });
t('bài đã đạt và còn nhớ → đi tiếp bài mới', remembered.microId === list[1]);

/* ── kỳ sát hạch chờ ── */
let Q = emptyProgress();
list.filter((id) => chapterOf(id) === 1).forEach((id) => { Q = recordMicro(Q, id, PASS); });
t('học hết chương 1 → kỳ sát hạch chờ', pendingExam({ progress: Q, list }) === 1);
Q = recordChapter(Q, 'lop5', 1, { pass: true, right: 13, total: 15 });
t('thi đạt rồi → không còn chờ', pendingExam({ progress: Q, list }) === null);

/* ── kế hoạch phiên: THẺ ÔN ĐI TRƯỚC ── */
const DAY = 86400000, now = 1_700_000_000_000;
const cards = [
  { id: 'c1', microId: list[0], dueAt: now - 2 * DAY },
  { id: 'c2', microId: list[1], dueAt: now - 1 * DAY },
  { id: 'c3', microId: list[2], dueAt: now - 3 * DAY },
  { id: 'c4', microId: list[3], dueAt: now + 5 * DAY },
];
const plan = planSession({ progress: Q, cards, index, now, list });
t('lấy đúng 3 thẻ đến hạn, bỏ thẻ chưa tới hạn', plan.reviews.length === 3 && !plan.reviews.find((c) => c.id === 'c4'));
t('thẻ quá hạn lâu nhất lên trước', plan.reviews[0].id === 'c3');
t('vẫn gợi ý bài mới sau khi ôn', plan.micro.microId === list[12]);
t('mức luyện mặc định là khởi động', plan.level === 'warmup');

/* ── đơn vị yếu nhất ── */
const w = weakestUnits({ A: { p: 0.9, nAttempts: 5 }, B: { p: 0.3, nAttempts: 4 }, C: { p: 0.6, nAttempts: 2 }, D: { p: 0.1, nAttempts: 0 } }, 2);
t('xếp yếu nhất lên đầu', w[0].unit === 'B' && w[1].unit === 'C');
t('bỏ đơn vị chưa từng làm', !w.find((x) => x.unit === 'D'));

/* ── sổ phụ huynh ── */
/* v: 2 = bản ghi ĐỦ TIN CẬY để tính thời gian (ms đo riêng từng câu, ts riêng từng
   lượt). Bản ghi cũ không có v thì bị loại khỏi mọi thống kê theo thời gian. */
const mk = (o) => ({ learnerId: 'L1', sessionId: 's1', microId: mid, correct: true, ts: now, ms: 5000, v: 2, ...o });
const atts = [
  mk({ ts: now - 10 * 60000 }), mk({ ts: now - 9 * 60000 }), mk({ ts: now - 8 * 60000 }),
  mk({ ts: now - 60 * 60000, sessionId: 's2' }),                       // buổi khác, cách xa
  mk({ correct: false, mustPass: true, ts: now - 7 * 60000 }),
  mk({ correct: false, mustPass: true, ts: now - 6 * 60000 }),
  mk({ correct: false, ms: 62000, itemId: 'P3', ts: now - 5 * 60000 }),
  mk({ ts: now - 20 * DAY }),                                          // ngoài khoảng 7 ngày
];
t('lọc đúng khoảng thời gian', inRange(atts, now - 7 * DAY, now).length === 7);
t('không cộng khoảng nghỉ dài vào giờ học', minutesStudied(inRange(atts, now - 7 * DAY, now)) < 20);
t('tìm được bẫy hay sập', topTraps(atts, index)[0].times === 2);
t('tìm được câu bế tắc (làm lâu mà sai)', stuckItems(atts)[0].seconds === 62);

const rep = buildParentReport({ learnerId: 'L1', attempts: atts, index,
  progress: { m1: { pass: true }, m2: { pass: true } },
  mastery: { u1: { p: 0.9 }, u2: { p: 0.5 } }, now });
t('đếm đúng số buổi', rep.sessions === 2);
t('đếm đúng số micro đã đạt', rep.microsPassed === 2);
t('đếm đúng đơn vị đã thạo', rep.unitsMastered === 1 && rep.unitsTotal === 2);
t('tỉ lệ đúng hợp lý', rep.correctRate > 0 && rep.correctRate < 100);
t('có câu tóm tắt cho bố mẹ', reportHeadline(rep).includes('phút'));

/* ── bản ghi CŨ không được làm hỏng thống kê thời gian ──
   Nhật ký bất biến, nên dòng ghi bằng luật cũ (ms tính từ lúc mở bài, cả loạt
   chung một mốc ts) nằm lẫn với dòng mới mãi mãi. Thà nói "chưa có số liệu" còn
   hơn hiện một con số sai cho bố mẹ tin theo. */
const cu = (o) => { const a = mk(o); delete a.v; return a; };
const lanLon = [
  cu({ ms: 300000, correct: false, itemId: 'A5', ts: now - 3 * 60000 }),   // 300s = tính từ lúc mở bài
  cu({ ms: 250000, correct: false, itemId: 'P5', ts: now - 3 * 60000 }),
  mk({ ms: 62000, correct: false, itemId: 'P9', ts: now - 2 * 60000 }),
];
const bt = stuckItems(lanLon);
t('không lấy bản ghi cũ làm "câu con làm lâu"', bt.length === 1 && bt[0].itemId === 'P9');
t('bản ghi cũ cùng một mốc ts không thổi phồng số phút học',
  minutesStudied([cu({ ts: now }), cu({ ts: now }), cu({ ts: now })]) === 0);
t('bản ghi mới vẫn tính được số phút học',
  minutesStudied([mk({ ts: now - 120000 }), mk({ ts: now - 60000 }), mk({ ts: now })]) === 2);

const repCu = buildParentReport({ learnerId: 'L1', attempts: lanLon, index, now });
t('sổ nói rõ có bao nhiêu lượt thiếu dữ liệu giờ giấc', repCu.luotThieuGio === 2);
t('lượt cũ vẫn được đếm vào tổng số câu đã làm', repCu.answered === 3);
t('chưa học thì báo rõ', reportHeadline({ answered: 0, topTraps: [] }).includes('chưa vào học'));

/* ═══ SỐ PHÚT HỌC: ĐO THẬT thay cho SUY RA ═══
 *
 * Phép suy ra cộng khoảng cách giữa các lượt trả lời. Từ khi cả bốn quyển chuyển
 * sang video, nó đếm hụt nặng: 405 video cộng lại 390,7 phút giảng, mà xem video thì
 * con không bấm gì. Nay máy con bấm giờ từng bước rồi cộng dồn theo ngày.
 */
{
  const ngayNay = new Date(now).toISOString().slice(0, 10);
  const soGio = [{ ngay: ngayNay, giay: 900, giayXem: 300, giayLam: 600 }];

  const doThat = phutHoc([], soGio, { from: now - 7 * 86400000, to: now });
  t('có sổ giờ thì lấy số ĐO THẬT', doThat.phut === 15 && doThat.nguon === 'do');
  t('và tách được xem với làm', doThat.phutXem === 5 && doThat.phutLam === 10);

  /* Đây là ca cả tính năng sinh ra để chữa: con XEM TRỌN VIDEO rồi trả lời đúng ngay
     câu chốt. Chỉ một lượt trả lời nên phép suy ra không có khoảng cách nào để cộng. */
  const motLuot = [mk({ ts: now })];
  t('phép SUY RA ra 0 phút khi con chỉ xem giảng rồi trả lời một câu',
    minutesStudied(motLuot) === 0);
  t('phép ĐO THẬT thấy đúng 15 phút của cùng buổi ấy',
    phutHoc(motLuot, soGio, { from: now - 86400000, to: now }).phut === 15);

  const suyRa = phutHoc([mk({ ts: now - 120000 }), mk({ ts: now })], [], {});
  t('không có sổ giờ thì lùi về phép cũ và NÓI RÕ là suy ra',
    suyRa.phut === 2 && suyRa.nguon === 'suyRa' && suyRa.phutXem === null);

  /* Ngày ngoài khoảng thì không được cộng vào — nếu không, "tuần này" hoá ra "từ
     trước tới nay" và con số cứ phình mãi. */
  const cu2 = [{ ngay: '2020-01-01', giay: 9999, giayXem: 0, giayLam: 9999 }];
  t('ngày ngoài khoảng bị loại',
    phutHoc([], cu2, { from: now - 86400000, to: now }).nguon === 'suyRa');

  const rep = buildParentReport({ learnerId: 'L1', attempts: motLuot, soGio, index, now });
  t('sổ phụ huynh lấy số đo thật', rep.minutes === 15 && rep.nguonGio === 'do');
  t('sổ nói rõ mấy phút xem giảng, mấy phút làm bài',
    rep.phutXem === 5 && rep.phutLam === 10);
  const repCu2 = buildParentReport({ learnerId: 'L1', attempts: motLuot, index, now });
  t('không có sổ giờ thì sổ vẫn chạy và khai là suy ra', repCu2.nguonGio === 'suyRa');
}

/* ── ĐƯỜNG CONG HỌC TẬP (mục 2.5.3) ────────────────────────────────────────
   Hai phép canh quan trọng nhất là hai cái BẪY, không phải đường cong đẹp hay
   xấu: (1) lượt cũ bị đánh nhầm số thứ tự, (2) điểm ít mẫu được vẽ lên. */
{
  const luot = (nut, ds, t0 = 0) =>
    ds.map((ok, i) => ({ bktUnit: nut, correct: ok, ts: t0 + i }));

  const day = [];
  for (let n = 0; n < 5; n += 1) day.push(...luot(`v_${n}`, [false, false, true, true, true]));
  const mastery = {};
  for (let n = 0; n < 5; n += 1) mastery[`v_${n}`] = { nAttempts: 5 };

  const r = duongCongHoc(day, mastery);
  t('đường cong: tỉ lệ sai giảm dần theo số lần luyện',
    r.duong.every((d, i, a) => i === 0 || d.tiLeSai <= a[i - 1].tiLeSai));
  t('mỗi điểm mang theo cỡ mẫu', r.duong.every((d) => d.soMau > 0));

  /* ⚠ BẪY 1 — nút bé đã học từ TRƯỚC kỳ này phải bị LOẠI. Sổ chỉ lấy 7 ngày, nên
     lượt thứ 12 của nó sẽ bị đánh thành "lần thứ 1" và pha loãng điểm đầu tiên:
     đường cong nói dối theo hướng ĐẸP LÊN. Nhận ra bằng `nAttempts` của hồ sơ
     nút ≠ số lượt đếm được trong cửa sổ. */
  const cuMoi = [...day, ...luot('v_cu', [true, true, true])];
  const rLoc = duongCongHoc(cuMoi, { ...mastery, v_cu: { nAttempts: 20 } });
  t('nút đã học từ trước kỳ bị loại khỏi đường cong', rLoc.soNutDaLoc === 1);
  t('loại rồi thì điểm lần 1 không bị pha loãng',
    rLoc.duong[0].tiLeSai === r.duong[0].tiLeSai);

  const rKhongLoc = duongCongHoc(cuMoi, { ...mastery, v_cu: { nAttempts: 3 } });
  t('đảo chiều: KHÔNG loại thì điểm lần 1 đẹp lên thật',
    rKhongLoc.duong[0].tiLeSai < r.duong[0].tiLeSai);

  /* Không có hồ sơ nút thì KHÔNG được đoán là đủ lịch sử. */
  t('thiếu hồ sơ nút thì loại, không đoán bừa',
    duongCongHoc(day, {}).soNut === 0 && duongCongHoc(day, {}).duong.length === 0);

  /* ⚠ BẪY 2 — điểm ít mẫu phải BỎ HẲN. Đuôi đường cong luôn thưa; một điểm dựng
     trên 2 mẫu nhảy 0% hay 100% tuỳ một câu, mà mắt người nhìn biểu đồ tin ngay. */
  const thua = luot('v_x', [false, false, false, false, false, false, false, false, false, false]);
  const rThua = duongCongHoc(thua, { v_x: { nAttempts: 10 } });
  t('điểm dưới ngưỡng mẫu bị bỏ hẳn', rThua.duong.length === 0);
  t('hạ ngưỡng xuống 1 thì mới hiện — chứng minh phép lọc có chạy',
    duongCongHoc(thua, { v_x: { nAttempts: 10 } }, { toiThieuMau: 1 }).duong.length > 0);

  /* Lượt không gắn nút nào thì bỏ, không ném lỗi. */
  t('lượt thiếu bktUnit không làm hỏng phép tính',
    duongCongHoc([{ correct: true, ts: 1 }, ...day], mastery).duong.length === r.duong.length);

  /* Và sổ bố mẹ phải mang nó ra. */
  const rep = buildParentReport({
    learnerId: 'L1', attempts: day.map((a) => ({ ...a, ts: Date.now(), microId: 'DL:TA5.B01' })),
    mastery, now: Date.now(),
  });
  t('sổ bố mẹ có mảng đường cong', Array.isArray(rep.duongCong?.duong));
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
