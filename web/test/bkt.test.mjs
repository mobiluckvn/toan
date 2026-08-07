/** Kiểm BKT & hàng đợi ôn tập trên dữ liệu thật — node test/bkt.test.mjs */
import fs from 'fs';
import {
  bktUpdate, bktSequence, isMastered, applyAttempt, paramsFor,
  DEFAULT_PARAMS, MASTERY_THRESHOLD,
} from '../functions/src/bkt.js';
import {
  parseSchedule, scheduleOf, buildReviewCards, dueCards, reviewCard, overdueCount, BOX_DAYS,
} from '../functions/src/schedule.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const ids = []; for (let b = 1; b <= 56; b++) for (const k of [1, 2, 3]) ids.push(`DL_KSN5Q1_B${b}_M${k}.json`);
const lessons = ids.map((f) => JSON.parse(fs.readFileSync('public/content/lessons/' + f, 'utf8')));

/* ── BKT: hành vi cơ bản ── */
t('đúng thì mức thạo TĂNG', bktUpdate(0.3, true) > 0.3);
t('sai thì mức thạo GIẢM so với đúng', bktUpdate(0.3, false) < bktUpdate(0.3, true));
t('luôn nằm trong (0,1)', [0, 1, 0.5].every((p) => { const v = bktUpdate(p, true); return v > 0 && v < 1; }));
t('giá trị lạ → không vỡ', Number.isFinite(bktUpdate(NaN, true)));

/* ── đúng liên tiếp phải vượt ngưỡng thạo ── */
let need = 0, p = DEFAULT_PARAMS.L0;
while (p < MASTERY_THRESHOLD && need < 20) { p = bktUpdate(p, true); need++; }
t(`đúng liên tiếp ${need} lần thì vượt ngưỡng 0,85`, need >= 3 && need <= 6);
console.log(`   từ L0 = ${DEFAULT_PARAMS.L0} cần ${need} câu đúng liên tiếp để đạt thạo`);

t('sai một câu sau khi thạo → tụt xuống dưới ngưỡng',
  !isMastered(bktUpdate(bktSequence([true, true, true, true]), false)));
t('thạo rồi sai rồi đúng lại → thạo lại',
  isMastered(bktSequence([true, true, true, true, false, true, true])));

/* ── câu bẫy có trọng số riêng ── */
const pm = paramsFor({ mustPass: true });
t('câu bẫy: guess thấp hơn', pm.guess < DEFAULT_PARAMS.guess);
t('đúng câu bẫy tăng mạnh hơn câu thường',
  bktUpdate(0.4, true, pm) > bktUpdate(0.4, true, DEFAULT_PARAMS));
t('sai câu bẫy tụt sâu hơn câu thường',
  bktUpdate(0.7, false, pm) < bktUpdate(0.7, false, DEFAULT_PARAMS));

/* ── applyAttempt tích luỹ ── */
let doc;
for (const ok of [true, true, true]) doc = applyAttempt(doc, { correct: ok, microId: 'DL:KSN5Q1.B49.M1' }, () => 1);
t('đếm đủ số lượt và số đúng', doc.nAttempts === 3 && doc.nCorrect === 3);
t('ghi nhớ micro gần nhất', doc.lastMicroId === 'DL:KSN5Q1.B49.M1');
t('cờ mastered khớp ngưỡng', doc.mastered === isMastered(doc.p));

/* ── lịch ôn: đọc được từ dữ liệu thật ── */
t('đọc "+3 ngày: câu generator P1"', parseSchedule('+3 ngày: câu generator P1')?.days === 3);
t('dòng không hợp lệ → null', parseSchedule('ôn khi rảnh') === null);

let withSched = 0, totCards = 0, dayset = new Set();
for (const L of lessons) {
  const s = scheduleOf(L);
  if (s.length) withSched++;
  s.forEach((x) => dayset.add(x.days));
  totCards += buildReviewCards({ learnerId: 'L1', microId: L.id, lesson: L, at: 0 }).length;
}
t(`mọi micro có lịch ôn: ${withSched}/168`, withSched === 168);
t('tổng thẻ ôn sinh ra hợp lý', totCards === 168 * 3);
console.log(`   mốc ngày gặp trong dữ liệu: ${[...dayset].sort((a, b) => a - b).join(' · ')} · tổng ${totCards} thẻ`);

/* ── đến hạn & Leitner ── */
const DAY = 86400000;
const cards = buildReviewCards({ learnerId: 'L1', microId: 'DL:KSN5Q1.B49.M1', lesson: lessons[144], at: 0 });
t('mới học xong thì chưa có thẻ nào đến hạn', dueCards(cards, 0).length === 0);
t('sau 1 ngày có thẻ đến hạn', dueCards(cards, 1.1 * DAY).length >= 1);
t('sau 7 ngày cả ba thẻ đến hạn', dueCards(cards, 7.1 * DAY, 9).length === 3);
t('chỉ lấy tối đa n thẻ mỗi phiên', dueCards(cards, 30 * DAY, 2).length === 2);

const c0 = cards[0];
const up = reviewCard(c0, true, 0);
t('ôn đúng → lên hộp, giãn ra', up.box === 1 && up.dueAt === BOX_DAYS[1] * DAY);
const down = reviewCard(up, false, 0);
t('ôn sai → về hộp 0, ôn lại sớm', down.box === 0 && down.dueAt === BOX_DAYS[0] * DAY);
t('đếm thẻ quá hạn', overdueCount(cards, 4 * DAY) === 2);

/* ── bktUnit có mặt trong dữ liệu để gắn mastery ── */
const units = new Set(lessons.map((L) => L.skills?.bktUnit).filter(Boolean));
t(`mọi micro có bktUnit: ${lessons.filter((L) => L.skills?.bktUnit).length}/168`,
  lessons.every((L) => L.skills?.bktUnit));
console.log(`   số đơn vị kỹ năng khác nhau: ${units.size}`);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
