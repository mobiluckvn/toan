/** Kiểm lớp dữ liệu học & hàng đợi ngoại tuyến — node test/sync.test.mjs */
import {
  buildAttempts, buildProgressDoc, attemptId, enqueue, readQueue, writeQueue,
  flushQueue, newSessionId, COLLECTIONS, reassignQueue, isCloudLearner,
} from '../src/lib/sync.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const mem = () => { let s = {}; return { getItem: (k) => s[k] ?? null, setItem: (k, v) => { s[k] = v; } }; };

const ev = [
  { phase: 'practice', itemId: 'P1', ok: true, tries: 1, hintsUsed: 0, ms: 8200 },
  { phase: 'practice', itemId: 'P2', ok: false, tries: 3, hintsUsed: 2, ms: 41000 },
  { phase: 'assess', itemId: 'A1', ok: true, tries: 1, mustPass: true, ms: 5100 },
  { phase: 'assess', itemId: 'A2', ok: false, tries: 1, ms: 6000 },
];
const base = { learnerId: 'L1', sessionId: 'S1', microId: 'DL:KSN5Q1.B49.M1', bktUnit: 'CASE:IV.4.1#1@G5', events: ev, now: () => 1700000000000 };

/* 1 · dựng attempts */
const recs = buildAttempts(base);
t('mỗi lượt trả lời một dòng', recs.length === 4);
t('giữ đủ trường chẩn đoán', recs.every((r) => 'tries' in r && 'hintsUsed' in r && 'ms' in r && 'phase' in r));
t('gắn bktUnit cho mọi bản ghi', recs.every((r) => r.bktUnit === 'CASE:IV.4.1#1@G5'));
t('đánh dấu câu bẫy', recs.find((r) => r.itemId === 'A1').mustPass === true);

/* 1b · DẠNG BÀI — trục thứ hai của sổ cô giáo, bên cạnh `bktUnit`.
   `bktUnit` trả lời "con mắc ở micro nào"; `dangBai` trả lời "cả lớp yếu mảng kiến
   thức nào" — nhìn theo bài thì không bao giờ thấy. Một bài dạy được nhiều dạng nên
   trường này là MẢNG; không có dạng thì để `null` cho gọn sổ, đừng ghi mảng rỗng. */
const cóDang = buildAttempts({ ...base, dangBai: ['PT:I.6.1', 'PT:I.6.4'] });
t('đóng dấu dangBai lên mọi bản ghi',
  cóDang.every((r) => Array.isArray(r.dangBai) && r.dangBai.length === 2));
t('không có dạng thì dangBai là null', recs.every((r) => r.dangBai === null));
t('một mã lẻ cũng gói thành mảng',
  buildAttempts({ ...base, dangBai: 'PT:I.1.1' })[0].dangBai[0] === 'PT:I.1.1');
t('mảng rỗng vẫn ra null', buildAttempts({ ...base, dangBai: [] })[0].dangBai === null);
t('id ổn định (ghi lại không sinh trùng)',
  buildAttempts(base)[0].id === recs[0].id);
t('id chứa đủ khoá', attemptId('L1', 'S1', 'DL:KSN5Q1.B49.M1', 'A1', 2) === 'L1_S1_B49.M1_A1_2');
t('thiếu learnerId → báo lỗi', (() => { try { buildAttempts({ ...base, learnerId: '' }); return false; } catch { return true; } })());

/* 2 · tóm tắt tiến độ */
const g = { pass: false, mustOK: false, right: 1, total: 2 };
const doc = buildProgressDoc({ microId: base.microId, grade: g, events: ev, sessionId: 'S1', now: () => 1 });
t('trạng thái "tried" khi chưa đạt', doc.state === 'tried');
t('đếm đúng số câu luyện đúng-ngay', doc.practiceFirstTry === 1 && doc.practiceTotal === 2);

/* 3 · hàng đợi ngoại tuyến */
const st = mem();
enqueue(recs, st);
t('vào hàng đợi đủ 4 bản ghi', readQueue(st).length === 4);
enqueue(recs, st);
t('ghi lại lần hai KHÔNG nhân bản', readQueue(st).length === 4);

/* 4 · gửi thành công thì dọn sạch */
let got = [];
const okWriter = async (chunk) => { got = got.concat(chunk); };
const r1 = await flushQueue(okWriter, st);
t(`gửi hết ${r1.sent} bản ghi`, r1.sent === 4 && r1.left === 0);
t('hàng đợi rỗng sau khi gửi', readQueue(st).length === 0);

/* 5 · MẤT MẠNG giữa chừng → giữ lại phần chưa gửi */
const st2 = mem();
const many = Array.from({ length: 500 }, (_, i) => ({ id: 'r' + i, v: i }));
enqueue(many, st2);
let n = 0;
const flaky = async (chunk) => { n += chunk.length; if (n > 200) throw new Error('mất mạng'); };
const r2 = await flushQueue(flaky, st2);
t('báo lỗi khi mất mạng', r2.error === true);
t(`giữ lại ${r2.left} bản ghi chưa gửi`, r2.left === 300 && readQueue(st2).length === 300);
const r3 = await flushQueue(okWriter, st2);
t('nối mạng lại gửi nốt', r3.sent === 300 && readQueue(st2).length === 0);

/* 6 · không có localStorage vẫn không vỡ */
t('không có storage → hàng đợi rỗng', readQueue(null).length === 0);
t('flush khi rỗng trả 0', (await flushQueue(okWriter, null)).sent === 0);

/* 7 · sessionId */
const a = newSessionId(() => 0.1), b = newSessionId(() => 0.9);
t('sessionId khác nhau', a !== b);
t('đường dẫn collection theo learner', COLLECTIONS.mastery('L1') === 'mastery/L1/units');


/* ── Học thử trước, đăng nhập sau: hàng đợi phải SANG TÊN cho tài khoản thật ──
   Không sang tên thì luật bảo mật từ chối, mà từ chối thì im lặng — công học bay sạch. */
const mem2 = (() => { let s = {}; return { getItem: (k) => s[k] ?? null, setItem: (k, v) => { s[k] = v; } }; })();
const local = buildAttempts({
  learnerId: 'local', sessionId: 'sA', microId: 'DL:KSN5Q1.B1.M1',
  events: [{ phase: 'practice', itemId: 'P1', ok: true }, { phase: 'assess', itemId: 'A1', ok: false }],
});
enqueue(local, mem2);
t('trước khi đăng nhập, hàng đợi mang mã tạm', readQueue(mem2).every((r) => r.learnerId === 'local'));

const moved = reassignQueue('UID_THAT', mem2);
const after = readQueue(mem2);
t('sang tên đủ cả hai bản ghi', moved.moved === 2 && after.length === 2);
t('learnerId đã đổi sang uid thật', after.every((r) => r.learnerId === 'UID_THAT'));
t('id cũng viết lại theo uid mới', after.every((r) => r.id.startsWith('UID_THAT_')));
t('id mới khớp đúng công thức',
  after.some((r) => r.id === attemptId('UID_THAT', 'sA', 'DL:KSN5Q1.B1.M1', 'P1', '0')));
t('không mất nội dung bài làm',
  after.filter((r) => r.correct).length === 1 && after.filter((r) => !r.correct).length === 1);

const twice = reassignQueue('UID_THAT', mem2);
t('chạy lại lần nữa không sinh bản trùng', twice.moved === 0 && readQueue(mem2).length === 2);
t('chưa đăng nhập thì không sang tên bừa', reassignQueue('local', mem2).moved === 0);
t('uid rỗng cũng không đụng vào hàng đợi', reassignQueue(null, mem2).moved === 0 && readQueue(mem2).length === 2);
t('isCloudLearner phân biệt đúng mã tạm', !isCloudLearner('local') && isCloudLearner('UID_THAT'));

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
