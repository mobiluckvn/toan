/** Kiểm chính sách adaptive & sổ phụ huynh — node test/report.test.mjs */
import fs from 'fs';
import {
  startLevel, nextLevel, pickMicro, pendingExam, planSession, weakestUnits, keyOf, masteryOfMicro,
} from '../src/mon/toan/lib/adaptive.js';
import { emptyProgress, recordMicro, recordChapter } from '../src/mon/toan/lib/progress.js';
import { allMicroIds, chapterOf } from '../src/mon/toan/lib/noiDung.js';
import {
  minutesStudied, topTraps, stuckItems, buildParentReport, reportHeadline, inRange,
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

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
