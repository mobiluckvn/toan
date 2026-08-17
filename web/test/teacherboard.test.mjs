/** Kiểm bảng giáo viên — chạy: node test/teacherboard.test.mjs */
import {
  buildTeacherBoard, topTraps, stuckLearners, learnerRows, boardHeadline, stampOf,
  maSach, minutesOf, phutDoThat, emCanGiup, NHANH_GIAY,
} from '../functions/src/teacherboard.js';
import { buildAttempts, isCloudLearner } from '../src/mon/toan/lib/sync.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const NOW = 1_700_000_000_000;
const D = (n) => NOW - n * 86400000;
const att = (learnerId, microId, o = {}) => ({
  learnerId, microId, sessionId: o.sid || 's1', itemId: o.item || 'A1',
  phase: o.phase || 'assess', correct: o.ok ?? true, mustPass: o.trap ?? false,
  tries: o.tries ?? 1, ms: o.ms ?? 1000, ts: o.ts ?? D(1), serverTs: o.serverTs ?? null,
});

/* ── 1 · mốc thời gian: ưu tiên máy chủ, con chỉnh đồng hồ máy cũng không lệch ── */
t('có serverTs thì lấy serverTs', stampOf({ ts: 1, serverTs: 999 }) === 999);
t('chưa có serverTs thì đành lấy giờ máy', stampOf({ ts: 1, serverTs: null }) === 1);
t('giờ máy con lệch vẫn lọt cửa sổ nhờ serverTs',
  buildTeacherBoard({
    roster: [{ uid: 'L1' }], now: NOW,
    attempts: [att('L1', 'M1', { ts: D(400), serverTs: D(1) })],   // máy con đặt lùi hơn một năm
  }).answered === 1);

/* ── 2 · bẫy: đếm theo SỐ EM, không theo số lượt ── */
const trapAtts = [
  att('L1', 'DL:KSN5Q1.B10.M1', { trap: true, ok: false }),
  att('L1', 'DL:KSN5Q1.B10.M1', { trap: true, ok: false }),   // cùng một em, làm lại
  att('L1', 'DL:KSN5Q1.B10.M1', { trap: true, ok: false }),
  att('L2', 'DL:KSN5Q1.B10.M1', { trap: true, ok: false }),
  att('L3', 'DL:KSN5Q1.B7.M2', { trap: true, ok: false }),
  att('L4', 'DL:KSN5Q1.B7.M2', { trap: true, ok: false }),
  att('L5', 'DL:KSN5Q1.B7.M2', { trap: true, ok: false }),
  att('L6', 'DL:KSN5Q1.B1.M1', { trap: true, ok: true }),      // đúng thì không tính
];
const traps = topTraps(trapAtts);
t('bài 3 em sập xếp trên bài 2 em sập', traps[0].microId === 'DL:KSN5Q1.B7.M2' && traps[0].learners === 3);
t('một em làm lại 3 lần vẫn chỉ tính 1 em', traps[1].learners === 2);
t('câu bẫy làm ĐÚNG không vào bảng', !traps.some((x) => x.microId === 'DL:KSN5Q1.B1.M1'));
t('lấy được tên bẫy từ chỉ mục',
  topTraps(trapAtts, { 'DL_KSN5Q1_B7_M2': { trapName: 'từ khác giữa' } })[0].trapName === 'từ khác giữa');

/* ── 3 · em đang tắc: chỉ tính bài CHƯA đạt ── */
const stuckAtts = [
  ...Array.from({ length: 4 }, () => att('L1', 'M1', { phase: 'practice', ok: false })),
  ...Array.from({ length: 5 }, () => att('L2', 'M2', { phase: 'practice', ok: false })),
  ...Array.from({ length: 2 }, () => att('L3', 'M3', { phase: 'practice', ok: false })),
];
const stuck = stuckLearners(stuckAtts, { L2: { M2: { pass: true } } });
t('em thử 4 lần chưa qua thì vào danh sách tắc', stuck.some((s) => s.learnerId === 'L1'));
t('em thử 5 lần NHƯNG đã đạt thì không tắc', !stuck.some((s) => s.learnerId === 'L2'));
t('mới thử 2 lần thì chưa gọi là tắc', !stuck.some((s) => s.learnerId === 'L3'));

/* ── 4 · một dòng mỗi em, kể cả em chưa học buổi nào ── */
const roster = [{ uid: 'L1', displayName: 'An' }, { uid: 'L2', displayName: 'Bình' },
                { uid: 'L3', displayName: 'Cúc' }];
const rows = learnerRows(
  [att('L1', 'M1', { ok: true }), att('L1', 'M1', { ok: false }), att('L2', 'M1', { ok: true })],
  roster, { L1: { M1: { pass: true } } });
t('mọi học sinh đều có một dòng', rows.length === 3);
t('em chưa học vẫn có dòng, tỉ lệ đúng để trống', rows.find((r) => r.uid === 'L3').correctRate === null);
t('tính đúng tỉ lệ đúng của từng em', rows.find((r) => r.uid === 'L1').correctRate === 50);
t('đếm đúng số bài đã đạt', rows.find((r) => r.uid === 'L1').microsPassed === 1);
t('xếp theo tên tiếng Việt', rows.map((r) => r.displayName).join(',') === 'An,Bình,Cúc');
t('lượt của tài khoản đã xoá không dựng dòng ma',
  learnerRows([att('LX', 'M1')], roster, {}).every((r) => r.answered === 0));

/* ── 5 · bảng giáo viên trọn vẹn ── */
const rep = buildTeacherBoard({
  roster, progress: { L1: { M1: { pass: true } } },
  attempts: [...trapAtts.map((a) => ({ ...a, learnerId: 'L1' })), att('L2', 'M1', { ok: true })],
  index: {}, now: NOW,
});
t('đếm đúng tổng số học sinh', rep.learners === 3);
t('đếm đúng số em có học', rep.activeLearners === 2);
t('chỉ mặt em chưa học buổi nào', rep.idleLearners.join() === 'L3');
t('có câu mở đầu đọc lướt', boardHeadline(rep).includes('2/3 em có học'));
t('chưa ai học thì nói thẳng',
  boardHeadline(buildTeacherBoard({ roster, now: NOW })).includes('chưa em nào'));
t('bảng là dữ liệu thuần, đem lưu được', typeof JSON.parse(JSON.stringify(rep)).answered === 'number');

/* ── 6 · attempts vẫn giữ chỗ cho mốc máy chủ ── */
const recs = buildAttempts({
  learnerId: 'L1', sessionId: 's1', microId: 'DL:KSN5Q1.B1.M1', serverTs: 'SENTINEL',
  events: [{ phase: 'practice', itemId: 'P1', ok: true }], now: () => NOW,
});
t('mỗi lượt có chỗ cho mốc máy chủ', recs[0].serverTs === 'SENTINEL');
t('learnerId chính là uid tài khoản', recs[0].learnerId === 'L1');

/* ── 7 · chưa đăng nhập thì KHÔNG đẩy lên máy chủ ──
   Đây là lỗi âm thầm nguy hiểm nhất: learnerId 'local' không có hồ sơ trên máy chủ,
   luật bảo mật từ chối, mà từ chối thì không ai biết — bài học của con bay mất. */
t('chưa đăng nhập thì không coi là học sinh trên máy chủ', !isCloudLearner('local'));
t('chưa có id thì cũng không', !isCloudLearner(null) && !isCloudLearner(''));
t('có hồ sơ thật thì mới đẩy lên', isCloudLearner('LxYz123'));




/* ══ Quyển 2 tách riêng khỏi Quyển 1 ══
   Học bài (Quyển 1) và luyện thi có đồng hồ (Quyển 2) là hai việc khác nhau; trộn
   vào một cột thì cô nhìn "đã trả lời 300 câu" mà không biết giúp con kiểu gì. */
const { laQuyen2 } = await import('../functions/src/teacherboard.js');
t('nhận ra bản ghi Quyển 2', laQuyen2({ microId: 'DR:KSN5Q2.V01' }) === true);
t('không nhầm bản ghi Quyển 1', laQuyen2({ microId: 'DL:KSN5Q1.B1.M1' }) === false);
t('thiếu mã nội dung thì không tính là Quyển 2', laQuyen2({}) === false);

const ros2 = [{ uid: 'u1', displayName: 'An', email: 'a@x' }];
const att2 = [
  { learnerId: 'u1', sessionId: 's1', microId: 'DL:KSN5Q1.B1.M1', correct: true, ts: NOW },
  { learnerId: 'u1', sessionId: 's1', microId: 'DL:KSN5Q1.B1.M1', correct: false, ts: NOW },
  { learnerId: 'u1', sessionId: 'd1', microId: 'DR:KSN5Q2.V01', correct: true, ts: NOW },
  { learnerId: 'u1', sessionId: 'd1', microId: 'DR:KSN5Q2.V01', correct: true, ts: NOW },
  { learnerId: 'u1', sessionId: 'd2', microId: 'DR:KSN5Q2.V02', correct: false, ts: NOW },
];
const b2 = buildTeacherBoard({ roster: ros2, attempts: att2, now: NOW });
t('cột chung vẫn đếm cả hai quyển', b2.answered === 5);
t('cột Quyển 2 chỉ đếm Quyển 2', b2.q2Answered === 3);
t('tỉ lệ đúng của Quyển 2 tính riêng', b2.q2CorrectRate === 67);
t('đếm đúng số vòng đấu đã đụng tới', b2.q2Vong === 2);
t('đếm đúng số học sinh có luyện thi', b2.q2Learners === 1);
const r2 = b2.rows[0];
t('dòng từng em cũng tách Quyển 2', r2.q2Answered === 3 && r2.answered === 5);
/* "0%" và "chưa làm" là hai chuyện khác hẳn: 0% nghĩa là con làm SAI HẾT, còn
   chưa luyện thi thì phải để trống. Cô nhìn 0% sẽ tưởng con đang bế tắc. */
const chuaThi = buildTeacherBoard({ roster: ros2, attempts: [att2[0]], now: NOW });
t('em chưa luyện thi thì cột Q2 của em để trống', chuaThi.rows[0].q2CorrectRate === null);
t('cả bảng chưa ai luyện thi thì cũng để trống', chuaThi.q2CorrectRate === null);
t('làm sai hết thì mới là 0%',
  buildTeacherBoard({ roster: ros2, now: NOW,
    attempts: [{ learnerId: 'u1', sessionId: 'd', microId: 'DR:KSN5Q2.V01', correct: false, ts: NOW }],
  }).q2CorrectRate === 0);

/* ── 8 · TRÌNH ĐỘ VÀ THỜI GIAN HỌC CỦA TỪNG EM ──
   "Em ấy đạt 47 bài" không nói lên trình độ: 47 bài lớp 2 và 47 bài lớp 5 là hai
   chuyện khác hẳn. Và "3 buổi" cũng vậy — ngồi 12 phút hay 70 phút cần hai cách
   nhắc khác nhau. */
t('mã sách suy được từ mã bài',
  maSach('DL:KSN5Q1.B1.M1') === 'KSN5Q1' && maSach('DL:KSN2.B01') === 'KSN2'
  && maSach('DR:KSN5Q2.V01') === 'KSN5Q2');
t('mã sách suy được cả từ mã tài liệu (bản ghi cũ thiếu microId)',
  maSach('DL_KSN4_B03') === 'KSN4');
t('mã lạ thì nói không biết, đừng đoán bừa', maSach('') === '?' && maSach(null) === '?');

const tienDo = {
  u1: {
    'DL:KSN2.B01': { pass: true, microId: 'DL:KSN2.B01' },
    'DL:KSN2.B02': { pass: true, microId: 'DL:KSN2.B02' },
    'DL:KSN4.B01': { pass: true, microId: 'DL:KSN4.B01' },
    'DL:KSN4.B02': { pass: false, microId: 'DL:KSN4.B02' },   // chưa đạt thì không đếm
  },
};
const rTd = learnerRows([], [{ uid: 'u1', displayName: 'A' }], tienDo)[0];
t('bài đạt tách theo từng sách',
  rTd.theoSach.KSN2 === 2 && rTd.theoSach.KSN4 === 1 && rTd.microsPassed === 3);
t('bài chưa đạt không lọt vào bảng theo sách', rTd.theoSach.KSN4 !== 2);

/* Số phút: cộng khoảng cách giữa các lượt, nghỉ quá 5 phút thì cắt. */
const P = 60000;
t('cộng đúng khoảng cách trong một mạch',
  minutesOf([{ v: 2, ts: 0 }, { v: 2, ts: 2 * P }, { v: 2, ts: 5 * P }]) === 5);
t('nghỉ quá 5 phút thì không tính vào giờ học',
  minutesOf([{ v: 2, ts: 0 }, { v: 2, ts: 2 * P }, { v: 2, ts: 60 * P }]) === 2);
/* Dòng ghi bằng luật cũ dùng chung một mốc cho cả loạt — tính ra 0, mà hiện "0 phút"
   thì cô đọc thành "em không học". Loại hẳn chúng ra. */
t('bỏ qua dòng ghi bằng luật cũ',
  minutesOf([{ ts: 0 }, { ts: 2 * P }, { v: 2, ts: 3 * P }, { v: 2, ts: 4 * P }]) === 1);
t('một lượt lẻ thì chưa đo được', minutesOf([{ v: 2, ts: 0 }]) === 0);

const rPhut = learnerRows(
  [att('u1', 'DL:KSN2.B01', { ts: 0 }), att('u1', 'DL:KSN2.B01', { ts: 3 * P })]
    .map((a) => ({ ...a, v: 2 })),
  [{ uid: 'u1', displayName: 'A' }], {})[0];
t('dòng từng em mang theo số phút', rPhut.minutes === 3);

/* ═══ SỐ PHÚT ĐO THẬT, VÀ "EM NÀO ĐANG YẾU" ═══ */
{
  const ngay = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Ho_Chi_Minh',
    year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(D(1)));
  const so = [{ loai: 'gio', ngay, giay: 1800, giayXem: 600, giayLam: 1200 }];
  t('phutDoThat cộng đúng', phutDoThat(so, D(7), NOW) === 30);
  t('chưa có sổ giờ thì trả null, KHÔNG trả 0',
    phutDoThat([{ loai: 'chuong', khoa: 'c1' }], D(7), NOW) === null);
  t('ngày ngoài khoảng thì cũng null',
    phutDoThat([{ loai: 'gio', ngay: '2020-01-01', giay: 999 }], D(7), NOW) === null);

  /* Đúng ca cả tính năng sinh ra: em xem giảng nhiều, trả lời ít lượt. Phép suy ra
     thấy gần như 0 phút; phép đo thật thấy 30 phút. */
  const luot = [att('u1', 'DL:KSN2.B01', { ts: D(1), sid: 's1' })].map((a) => ({ ...a, v: 2 }));
  const rDo = learnerRows(luot, [{ uid: 'u1', displayName: 'A' }], {},
    { u1: so }, { from: D(7), to: NOW })[0];
  t('cột phút của cô lấy số ĐO THẬT', rDo.minutes === 30 && rDo.nguonGio === 'do');
  const rSuy = learnerRows(luot, [{ uid: 'u1', displayName: 'A' }], {}, {}, {})[0];
  t('không có sổ giờ thì lùi về suy ra và nói rõ', rSuy.nguonGio === 'suyRa');
}

{
  /* Ba em cùng đúng 40% — nhìn phần trăm thì y hệt nhau, mà cần ba cách giúp khác nhau. */
  const rows = [
    { uid: 'au', displayName: 'Ẩu', answered: 20, correctRate: 40, minutes: 5 },
    { uid: 'hong', displayName: 'Hổng', answered: 20, correctRate: 40, minutes: 40 },
    { uid: 'vuot', displayName: 'Vượt', answered: 20, correctRate: 40, minutes: 20 },
    { uid: 'gioi', displayName: 'Giỏi', answered: 30, correctRate: 92, minutes: 30 },
    { uid: 'itqua', displayName: 'Ít', answered: 3, correctRate: 0, minutes: 1 },
  ];
  const prog = {
    au:   { a: { giay: 8, giayXem: 4, giayLam: 4 }, b: { giay: 6, giayXem: 3, giayLam: 3 } },
    hong: { a: { giay: 300, giayXem: 90, giayLam: 210 }, b: { giay: 250, giayXem: 80, giayLam: 170 } },
    vuot: { a: { giay: 120, giayXem: 1, giayLam: 119 }, b: { giay: 100, giayXem: 0, giayLam: 100 } },
  };
  const ds = emCanGiup(rows, prog);
  const tra = (u) => ds.find((x) => x.uid === u);
  t('em giỏi KHÔNG bị gọi tên', !tra('gioi'));
  t('em mới làm 3 câu chưa đủ để kết luận', !tra('itqua'));
  t(`bấm quá nhanh rồi sai → "au" (dưới ${NHANH_GIAY} giây/bài)`, tra('au')?.viSao === 'au');
  t('ngồi lâu vẫn sai → "hong"', tra('hong')?.viSao === 'hong');
  t('bỏ qua video rồi lao vào làm → "boQuaGiang"', tra('vuot')?.viSao === 'boQuaGiang');

  /* Chưa đo được giờ thì ĐỪNG đoán bừa — cô gọi nhầm em đắt hơn thiếu một cái nhãn. */
  const chuaDo = emCanGiup([{ uid: 'x', displayName: 'X', answered: 20, correctRate: 30, minutes: 9 }], {});
  t('chưa đo được giờ thì trả "chuaRo", không đoán', chuaDo[0].viSao === 'chuaRo');

  /* Đảo chiều: danh sách phải THẬT SỰ lọc, không phải trả về tất cả. */
  t('có lọc thật (3 em trong danh sách, không phải cả 5)', ds.length === 3);
  t('em sai nhiều câu hơn xếp trên em sai ít câu hơn',
    emCanGiup([
      { uid: 'p', displayName: 'P', answered: 8, correctRate: 30, minutes: 5 },
      { uid: 'q', displayName: 'Q', answered: 40, correctRate: 30, minutes: 5 },
    ], {})[0].uid === 'q');
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
