/** Kiểm luật mở khoá & tiến độ — chạy: node test/progress.test.mjs */
import {
  emptyProgress, recordMicro, recordChapter, isMicroUnlocked, isChapterExamUnlocked,
  nextToStudy, chapterStats, overallStats, microState, loadProgress, saveProgress,
  saveSpot, resumeSpot, clearSpot, modeOf, setMode, MODES,
} from '../src/mon/toan/lib/progress.js';
import { allMicroIds, chapterOf } from '../src/mon/toan/lib/noiDung.js';

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
R = recordChapter(R, 'lop5', 1, { pass: true, right: 13, total: 15 });
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


/* ── Hai chế độ học ──
   Chế độ đề xuất: đi tuần tự cả 168 bài.
   Chế độ tự chọn: vào chủ đề nào cũng được, NHƯNG trong chương vẫn tuần tự. */
const dauC1 = list[0];                       // B1.M1
const haiC1 = list[1];                       // B1.M2
const dauC2 = list.find((id) => chapterOf(id) === 2);
const haiC2 = list[list.indexOf(dauC2) + 1];
const dauC14 = list.find((id) => chapterOf(id) === 14);

let M = emptyProgress();
t('mặc định là chế độ theo chương trình', modeOf(M) === 'chuongtrinh');
t('chỉ có đúng hai chế độ', MODES.join() === 'chuongtrinh,tuchon');
t('chế độ lạ thì bỏ qua, giữ nguyên', modeOf(setMode(M, 'linh tinh')) === 'chuongtrinh');

t('theo chương trình: chương 2 còn khoá', !isMicroUnlocked(M, dauC2, list));
t('theo chương trình: chương 14 còn khoá', !isMicroUnlocked(M, dauC14, list));

M = setMode(M, 'tuchon');
t('đổi chế độ thì nhớ', modeOf(M) === 'tuchon');
t('tự chọn: bài ĐẦU chương 2 mở ngay', isMicroUnlocked(M, dauC2, list));
t('tự chọn: bài đầu chương 14 cũng mở ngay', isMicroUnlocked(M, dauC14, list));
t('tự chọn: bài THỨ HAI của chương vẫn khoá', !isMicroUnlocked(M, haiC2, list));
t('tự chọn: bài đầu cả bộ vẫn mở', isMicroUnlocked(M, dauC1, list));

// học xong bài đầu chương 2 thì bài hai của chương 2 mở ra
const M2 = recordMicro(M, dauC2, PASS);
t('tự chọn: học xong bài đầu thì bài kế mở', isMicroUnlocked(M2, haiC2, list));
// học chương 2 không được phép mở hộ bài THỨ HAI của chương khác
const dauC3 = list.find((id) => chapterOf(id) === 3);
const haiC3 = list[list.indexOf(dauC3) + 1];
t('tự chọn: học chương 2 KHÔNG mở hộ bài 2 của chương 3', !isMicroUnlocked(M2, haiC3, list));
t('tự chọn: bài đầu chương 3 vẫn mở như mọi chương', isMicroUnlocked(M2, dauC3, list));
t('tự chọn: bài 2 của chương 1 vẫn khoá vì chưa học bài 1', !isMicroUnlocked(M2, haiC1, list));

// đổi về chế độ đề xuất thì khoá siết lại như cũ
const M3 = setMode(M2, 'chuongtrinh');
t('quay lại chế độ đề xuất thì khoá siết lại', !isMicroUnlocked(M3, dauC2, list));
t('nhưng bài đã ĐẠT vẫn còn nguyên', overallStats(M3, list).done === 1);



/* ══ Đi lại trong bài: quay lại xem/làm lại, nhưng KHÔNG nhảy cóc ══
   Bài vốn chỉ đi một chiều — lỡ bấm Tiếp là mất phần vừa đọc. Nay lùi được, và
   bấm thẳng vào đốt đã học được. Nhưng bấm vượt lên phần chưa học thì phải chặn:
   nhảy thẳng tới sát hạch là bỏ qua cả mạch giảng bài lẫn cổng mustPass. */
import { bamDuocDot } from '../src/mon/toan/lib/flow.js';

t('bấm được đốt ĐÃ HỌC để xem lại', bamDuocDot(2, 5, 5) === true);
t('bấm được đốt ngay trước đó', bamDuocDot(4, 5, 5) === true);
t('KHÔNG bấm được đốt chưa học', bamDuocDot(9, 5, 5) === false);
t('KHÔNG bấm được đốt ngay sau chỗ xa nhất', bamDuocDot(6, 5, 5) === false);
t('bấm vào chính đốt đang đứng thì không làm gì', bamDuocDot(5, 5, 5) === false);

/* Lùi về xem lại rồi vẫn tiến lại được tới chỗ cũ: mốc "xa nhất" giữ nguyên. */
t('lùi về phần 2 vẫn bấm lại được phần 5 đã đi qua', bamDuocDot(5, 2, 5) === true);
t('lùi về phần 2 vẫn không vượt quá chỗ xa nhất', bamDuocDot(6, 2, 5) === false);
t('ở phần đầu thì không có đốt nào để lùi', bamDuocDot(0, 0, 0) === false);


/* ═══════════ THANG LÙI / TIẾN CỦA LUYỆN CHỦ ĐỀ ═══════════
 *
 * Đây là chỗ quyết định con được đẩy đi đâu sau mỗi lượt luyện, nên sai là sai
 * lặng lẽ: con vẫn có bài để làm, chỉ là làm sai bậc. Hai NGẢ BÌA nguy nhất —
 * chạm sàn (không còn lớp dưới) và chạm trần (không còn lớp trên) — vì làm hụt
 * là đẩy con vào một bậc không tồn tại.
 */
import {
  nguongDat, bacBatDau, buocSau, ghiLuyenChuDe, bacDaVung,
} from '../src/mon/toan/lib/progress.js';

const THANG4 = [{ lop: 2 }, { lop: 3 }, { lop: 4 }, { lop: 5 }];
const THANG_TREN = [{ lop: 4 }, { lop: 5 }];        // chủ đề chỉ có ở lớp trên
const THANG1 = [{ lop: 5 }];                        // dạng riêng lớp 5

t('đạt là 2/3 số câu (6 câu → 4)', nguongDat(6) === 4);
t('ngưỡng không bao giờ bằng 0', nguongDat(1) === 1 && nguongDat(0) === 1);

t('bắt đầu ở đúng lớp của con', bacBatDau(THANG4, 4) === 4);
t('con lớp 3 mà chủ đề chỉ có từ lớp 4 thì bắt đầu ở bậc thấp nhất',
  bacBatDau(THANG_TREN, 3) === 4);
t('con lớp 5 mà thang thiếu bậc 5 thì lấy bậc dưới gần nhất',
  bacBatDau([{ lop: 2 }, { lop: 4 }], 5) === 4);
t('thang rỗng thì không có bậc nào để bắt đầu', bacBatDau([], 5) === null);

t('đạt ở bậc giữa thì LÊN', JSON.stringify(buocSau(THANG4, 4, 4, 6))
  === JSON.stringify({ hanh: 'len', lop: 5 }));
t('đạt ở bậc CAO NHẤT thì XONG, không đẩy lên bậc không có',
  buocSau(THANG4, 5, 6, 6).hanh === 'xong');
t('kém ở bậc giữa thì XUỐNG', JSON.stringify(buocSau(THANG4, 4, 1, 6))
  === JSON.stringify({ hanh: 'xuong', lop: 3 }));
t('kém ở bậc THẤP NHẤT thì dừng, không lùi vào hư không',
  buocSau(THANG4, 2, 0, 6).hanh === 'san');
t('thang một bậc: đạt là xong ngay', buocSau(THANG1, 5, 5, 6).hanh === 'xong');
t('thang một bậc: kém là chạm sàn ngay', buocSau(THANG1, 5, 1, 6).hanh === 'san');
t('bậc không có trong thang thì coi như chạm sàn, không nổ',
  buocSau(THANG4, 9, 6, 6).hanh === 'san');
t('lùi từng bậc MỘT, không nhảy hai bậc',
  buocSau(THANG4, 5, 0, 6).lop === 4);

/* Ghi sổ: mỗi bậc một dòng, và `best` giữ lần cao nhất — lùi xuống rồi lên lại
   thì lần sau đè lên lần trước, mà cái đáng nhớ là con ĐÃ từng làm được tới đâu. */
let p = emptyProgress();
p = ghiLuyenChuDe(p, 'PT:I.1.1', 5, { dat: 2, tong: 6 });
t('ghi một lượt luyện chủ đề', p.chuDe['PT:I.1.1'].bac['5'].dat === 2);
t('2/6 là chưa đạt', p.chuDe['PT:I.1.1'].bac['5'].pass === false);
t('chưa đạt bậc nào thì bacDaVung là null', bacDaVung(p, 'PT:I.1.1') === null);
p = ghiLuyenChuDe(p, 'PT:I.1.1', 4, { dat: 5, tong: 6 });
t('ghi thêm bậc khác không xoá bậc cũ', Object.keys(p.chuDe['PT:I.1.1'].bac).length === 2);
t('5/6 là đạt', p.chuDe['PT:I.1.1'].bac['4'].pass === true);
t('bacDaVung lấy bậc CAO NHẤT đã đạt', bacDaVung(p, 'PT:I.1.1') === 4);
p = ghiLuyenChuDe(p, 'PT:I.1.1', 5, { dat: 1, tong: 6 });
t('làm lại kém hơn thì best vẫn giữ lần cao nhất', p.chuDe['PT:I.1.1'].bac['5'].best === 2);
t('đếm số lần luyện của một bậc', p.chuDe['PT:I.1.1'].bac['5'].lan === 2);
t('lát chuDe không đụng vào micros', Object.keys(p.micros).length === 0);
t('chủ đề chưa luyện thì bacDaVung là null', bacDaVung(p, 'PT:V.9.9') === null);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
