/**
 * Kiểm NHẬT KÝ HỌC gửi lên máy chủ — chạy: node test/nhatky.test.mjs
 *
 * Cô giáo chỉ giúp được con nếu nhìn thấy con VẤP Ở ĐÂU. Muốn thế thì nhật ký phải
 * đủ ba thứ mà bản cũ thiếu:
 *   1. đủ BỐN chặng. Bản cũ chỉ ghi 'practice' và 'assess', bỏ trắng 'check'
 *      (chốt nhanh) và 'worked' (câu xen giữa ví dụ) — mất 513/1654 câu, tức 31%
 *      số câu con thực làm.
 *   2. mọi câu phải có MÃ ổn định. 513 câu kia trước đây không có mã, ghi lên thì
 *      cô cũng không biết đó là câu nào.
 *   3. con TRẢ LỜI GÌ. Chỉ biết "sai" thì không đoán được con hiểu lệch chỗ nào —
 *      hai con sai hai kiểu cần hai cách giúp khác nhau.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { buildAttempts, goiDapAn, attemptId, CHU_TOI_DA } from '../src/lib/sync.js';

const D = new URL('../public/content/lessons/', import.meta.url).pathname;
const lessons = readdirSync(D).filter((f) => f.endsWith('.json'))
  .map((f) => JSON.parse(readFileSync(join(D, f), 'utf8')));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── 1. mọi câu con trả lời được đều phải có MÃ, và không trùng trong cùng bài ── */
const CHANG = ['practice', 'assess', 'check', 'worked'];
let soCau = 0;
const thieuMa = [], trungMa = [];
const dem = { practice: 0, assess: 0, check: 0, worked: 0 };

for (const L of lessons) {
  const mid = L.id.replace('DL:KSN5Q1.', '');
  const ids = [];
  const ghi = (chang, it) => {
    soCau++; dem[chang]++;
    if (!String(it?.id ?? '').trim()) thieuMa.push(`${mid} [${chang}]`);
    else ids.push(it.id);
  };
  for (const arr of Object.values(L.practice?.pools || {})) arr.forEach((it) => ghi('practice', it));
  (L.assessment?.items || []).forEach((it) => ghi('assess', it));
  (L.lecture?.screens || []).forEach((s) => s.item && ghi('check', s.item));
  (L.workedExample?.steps || []).forEach((s) => {
    for (const k of ['askBefore', 'askAfter']) if (s[k]) ghi('worked', s[k]);
  });
  const lap = ids.filter((x, i) => ids.indexOf(x) !== i);
  if (lap.length) trungMa.push(`${mid}: ${[...new Set(lap)].join(',')}`);
}

t(`cả ${soCau} câu đều có mã (${thieuMa.length} thiếu)`, thieuMa.length === 0);
if (thieuMa.length) console.log('    ', thieuMa.slice(0, 6).join(' · '));
t(`mã không trùng trong cùng một bài (${trungMa.length})`, trungMa.length === 0);
if (trungMa.length) console.log('    ', trungMa.slice(0, 6).join(' · '));
t('có đủ câu ở cả bốn chặng', CHANG.every((c) => dem[c] > 0));

/* ── 2. bản ghi giữ đủ những gì cô cần ── */
const rec = buildAttempts({
  learnerId: 'u1', sessionId: 's1', microId: 'DL:KSN5Q1.B1.M1', bktUnit: 'CASE:x',
  events: [
    { phase: 'check', itemId: 'C1', ok: false, tries: 1, ms: 4200,
      answer: '3,5', expected: '35,46', mode: 'so', hintsUsed: 1 },
    { phase: 'check', itemId: 'C1', ok: true, tries: 2, ms: 9100,
      answer: '35,46', expected: '35,46', mode: 'so' },
    { phase: 'worked', itemId: 'W1', ok: true, tries: 1, mode: 'chondapan', answer: ['ĐÚNG'] },
  ],
  now: () => 1000,
});

t('mỗi lượt bấm một dòng, không gộp thành một', rec.length === 3);

/* Mỗi lượt phải mang mốc RIÊNG. Dùng chung một mốc đóng lúc gửi thì "số phút con
   học" (tính theo khoảng cách giữa các mốc) luôn ra 0. */
const rec2 = buildAttempts({
  learnerId: 'u1', sessionId: 's1', microId: 'DL:KSN5Q1.B1.M1',
  events: [{ phase: 'practice', itemId: 'P1', ok: true, khiNao: 5000 },
           { phase: 'practice', itemId: 'P2', ok: true, khiNao: 95000 }],
  now: () => 1000,
});
t('mỗi lượt giữ mốc thời gian riêng', rec2[0].ts === 5000 && rec2[1].ts === 95000);
t('không có mốc riêng thì lùi về mốc chung', rec[0].ts === 1000);
t('hai lượt của CÙNG một câu không đè lên nhau', rec[0].id !== rec[1].id);
t('giữ lại con đã trả lời gì', rec[0].answer === '3,5');
t('giữ lại đáp án đúng để đối chiếu', rec[0].expected === '35,46');
t('giữ lại kiểu trả lời', rec[0].mode === 'so');
t('giữ số gợi ý con đã mở', rec[0].hintsUsed === 1);
t('giữ thời gian làm RIÊNG câu đó', rec[0].ms === 4200 && rec[1].ms === 9100);
t('chặng check được ghi', rec[0].phase === 'check');
t('chặng worked được ghi', rec[2].phase === 'worked');
t('đáp án nhiều ô gộp thành chuỗi đọc được', rec[2].answer === 'ĐÚNG');
t('không có answer thì để null chứ không phải "undefined"', rec[2].expected === null);

/* Luật bảo mật đòi đúng 6 khoá này; thiếu một là Firestore từ chối IM LẶNG,
   công học của con bay mất mà không ai biết. */
for (const k of ['learnerId', 'microId', 'itemId', 'phase', 'correct', 'ts']) {
  t(`bản ghi có khoá bắt buộc "${k}"`, rec.every((r) => r[k] !== undefined));
}
t('correct luôn là boolean (luật bảo mật kiểm kiểu)', rec.every((r) => typeof r.correct === 'boolean'));
t('phase luôn nằm trong bốn chặng luật cho phép', rec.every((r) => CHANG.includes(r.phase)));

/* ── 3. gọn đáp án ── */
t('gộp nhiều ô bằng dấu |', goiDapAn(['3', '4']) === '3 | 4');
t('cắt bớt đáp án dài quá', goiDapAn('x'.repeat(400)).length === CHU_TOI_DA);
t('đáp án dài bị cắt có dấu … cho biết còn nữa', goiDapAn('x'.repeat(400)).endsWith('…'));
t('rỗng thì ra chuỗi rỗng, không phải "null"', goiDapAn('') === '');
t('mã lượt trả lời ổn định', attemptId('u', 's', 'DL:KSN5Q1.B1.M1', 'P1', 0) === 'u_s_B1.M1_P1_0');

console.log(`\n   ${soCau} câu · luyện ${dem.practice} · sát hạch ${dem.assess}`
  + ` · chốt nhanh ${dem.check} · xen ví dụ ${dem.worked}`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
