/** Kiểm luật mở khoá & tiến độ — chạy: node test/progress.test.mjs */
import {
  emptyProgress, recordMicro, recordChapter, isMicroUnlocked, isChapterExamUnlocked,
  nextToStudy, chapterStats, overallStats, microState, loadProgress, saveProgress,
  saveSpot, resumeSpot, clearSpot,
} from '../src/lib/progress.js';
import { allMicroIds, chapterOf } from '../src/lib/content.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const list = allMicroIds();
const PASS = { pass: true, mustOK: true, right: 3, total: 3 };
const FAILTRAP = { pass: false, mustOK: false, right: 2, total: 3 };

t('có đúng 168 micro', list.length === 168);
t('chương của B49.M1 là 13', chapterOf('DL:KSN5Q1.B49.M1') === 13);

let P = emptyProgress();
t('micro đầu luôn mở', isMicroUnlocked(P, list[0], list));
t('micro thứ hai khoá lúc đầu', !isMicroUnlocked(P, list[1], list));

P = recordMicro(P, list[0], PASS);
t('đạt micro 1 → mở micro 2', isMicroUnlocked(P, list[1], list));
t('micro 3 vẫn khoá', !isMicroUnlocked(P, list[2], list));

/* CỔNG mustPass: sai câu bẫy thì KHÔNG mở bài sau dù đúng 2/3 */
let Q = recordMicro(emptyProgress(), list[0], FAILTRAP);
t('sai câu bẫy → không mở bài sau', !isMicroUnlocked(Q, list[1], list));
t('trạng thái hiển thị "tried"', microState(Q, list[0], list) === 'tried');
t('bài sau hiển thị "locked"', microState(Q, list[1], list) === 'locked');

/* kỳ sát hạch chương */
let R = emptyProgress();
const c1 = list.filter((id) => chapterOf(id) === 1);
t('chương 1 có 12 micro', c1.length === 12);
c1.slice(0, 11).forEach((id) => { R = recordMicro(R, id, PASS); });
t('còn 1 micro → chưa mở kỳ sát hạch', !isChapterExamUnlocked(R, 1, list));
R = recordMicro(R, c1[11], PASS);
t('đủ 12/12 → mở kỳ sát hạch', isChapterExamUnlocked(R, 1, list));

const st = chapterStats(R, 1, list);
t('thống kê chương: 12/12 = 100%', st.done === 12 && st.percent === 100);
R = recordChapter(R, 1, { pass: true, right: 13, total: 15 });
t('ghi huy hiệu chương', chapterStats(R, 1, list).examPassed === true);
t('tổng huy hiệu = 1', overallStats(R, list).badges === 1);
t('tiến độ tổng 12/168', overallStats(R, list).done === 12);

/* bài học tiếp theo */
t('gợi ý học bài 13 tiếp theo', nextToStudy(R, list) === list[12]);
t('học hết → không còn bài', nextToStudy(list.reduce((p, id) => recordMicro(p, id, PASS), emptyProgress()), list) === null);

/* lưu / nạp */
const mem = (() => { let s = {}; return { getItem: (k) => s[k] ?? null, setItem: (k, v) => { s[k] = v; } }; })();
saveProgress(R, mem);
const back = loadProgress(mem);
t('lưu rồi nạp lại giữ nguyên tiến độ', overallStats(back, list).done === 12);
t('không có localStorage vẫn chạy', overallStats(loadProgress(null), list).done === 0);

/* ── Học dở thoát ra rồi quay lại phải về ĐÚNG chỗ ── */
const M0 = list[0];
let S = emptyProgress();
t('chưa học thì không có chỗ nào để quay lại', resumeSpot(S, M0) === null);

S = saveSpot(S, M0, 12, 23);
t('nhớ đúng bước đang dở', resumeSpot(S, M0)?.step === 12);
t('nhớ cả tổng số bước để hiện 12/23', resumeSpot(S, M0)?.steps === 23);

t('bước 0 thì không đánh dấu', resumeSpot(saveSpot(emptyProgress(), M0, 0, 23), M0) === null);
t('lưu lại cùng bước thì giữ nguyên đối tượng', saveSpot(S, M0, 12, 23) === S);

// đánh dấu chỗ học dở KHÔNG được làm micro trông như đã làm bài
t('đang học dở vẫn là bài đang mở', microState(S, M0, list) === 'open');
t('đang học dở không tính là đã xong', overallStats(S, list).done === 0);
t('đang học dở không mở khoá bài sau', !isMicroUnlocked(S, list[1], list));

const S2 = clearSpot(S, M0);
t('chọn học lại từ đầu thì xoá dấu', resumeSpot(S2, M0) === null);

// học xong rồi thì mở lại là học lại từ đầu, không nhảy vào giữa bài cũ
const S3 = recordMicro(S, M0, PASS);
t('đã đạt thì không còn chỗ dở', resumeSpot(S3, M0) === null);
t('đã đạt thì không ghi đè dấu mới', resumeSpot(saveSpot(S3, M0, 5, 23), M0) === null);

// đánh dấu phải sống sót qua lưu — hết pin giữa chừng vẫn quay lại được
const mem2 = (() => { let s = {}; return { getItem: (k) => s[k] ?? null, setItem: (k, v) => { s[k] = v; } }; })();
saveProgress(saveSpot(emptyProgress(), M0, 7, 23), mem2);
t('tắt máy mở lại vẫn nhớ chỗ dở', resumeSpot(loadProgress(mem2), M0)?.step === 7);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
