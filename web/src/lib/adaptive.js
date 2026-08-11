/**
 * CHÍNH SÁCH THÍCH ỨNG — quyết định phiên học tiếp theo.
 * Thuần logic, không phụ thuộc React/Firebase (xem test/adaptive.test.mjs).
 *
 * Thứ tự ưu tiên trong một phiên ~15 phút:
 *   1. Thẻ ôn ĐẾN HẠN (1–3 thẻ)  — kiến thức cũ sắp quên quan trọng hơn kiến thức mới
 *   2. Micro chưa thạo & đã mở khoá
 *   3. Trong micro: chọn mức luyện theo mức thạo hiện có
 */
import { allMicroIds, chapterOf } from './content.js';
import { isMicroUnlocked, isChapterExamUnlocked, ketQuaChuong } from './progress.js';

export const MASTERY_THRESHOLD = 0.85;
export const MAX_REVIEW_PER_SESSION = 3;

/** Mức thạo của micro: đọc theo bktUnit trong chỉ mục */
export function masteryOfMicro(mastery, microId, index) {
  const unit = index?.[keyOf(microId)]?.bktUnit;
  return unit ? (mastery?.[unit]?.p ?? null) : null;
}
export const keyOf = (microId) => microId.replace(/[:.]/g, '_');

/** Mức luyện nên bắt đầu — không bắt bé giỏi làm lại câu khởi động */
export function startLevel(p) {
  if (p === null || p === undefined) return 'warmup';
  if (p < 0.4) return 'warmup';
  if (p < 0.7) return 'standard';
  return 'challenge';
}

/** Lên mức khi đúng 2 câu liên tiếp (đúng adaptiveRules trong dữ liệu) */
export function nextLevel(level, streak) {
  const order = ['warmup', 'standard', 'challenge'];
  const i = order.indexOf(level);
  return streak >= 2 && i < order.length - 1 ? order[i + 1] : level;
}

/**
 * Micro nên học tiếp: bài đầu tiên CHƯA THẠO, đã mở khoá.
 * Đã đạt bài nhưng mức thạo tụt dưới ngưỡng (quên) thì vẫn được gợi ý học lại.
 */
export function pickMicro({ progress, mastery = {}, index = {}, list = allMicroIds() }) {
  for (const id of list) {
    if (!isMicroUnlocked(progress, id, list)) continue;
    const done = progress.micros?.[id]?.pass;
    const p = masteryOfMicro(mastery, id, index);
    if (!done) return { microId: id, reason: 'chưa học', mastery: p };
    if (p !== null && p < MASTERY_THRESHOLD) return { microId: id, reason: 'đã quên bớt', mastery: p };
  }
  return null;
}

/**
 * Kỳ sát hạch chương đang mở mà chưa đạt — ưu tiên hơn học bài mới của chương sau.
 *
 * Số chương suy TỪ DANH SÁCH BÀI, không ghim 14: lớp 4 có 11 chương, lớp 2·3 có 8.
 * Và kết quả tra qua `ketQuaChuong` vì sổ khoá theo `<quyển>.<chương>` — hỏi thẳng
 * `chapters[c]` là huy hiệu chương 3 của lớp 5 trả lời thay cho lớp 2.
 */
export function pendingExam({ progress, list = allMicroIds(), ma = 'lop5' }) {
  const chuong = [...new Set(list.map(chapterOf))].sort((a, b) => a - b);
  for (const c of chuong) {
    if (isChapterExamUnlocked(progress, c, list) && !ketQuaChuong(progress, ma, c)?.pass) return c;
  }
  return null;
}

/**
 * Dựng kế hoạch một phiên học.
 * @returns {{reviews:Array, exam:number|null, micro:object|null, level:string}}
 */
export function planSession({ progress, mastery = {}, cards = [], index = {}, now = Date.now(), list = allMicroIds() }) {
  const due = cards.filter((c) => c.dueAt <= now)
    .sort((a, b) => a.dueAt - b.dueAt)
    .slice(0, MAX_REVIEW_PER_SESSION);
  const exam = pendingExam({ progress, list });
  const micro = pickMicro({ progress, mastery, index, list });
  return {
    reviews: due,
    exam,
    micro,
    level: startLevel(micro?.mastery ?? null),
  };
}

/** Đơn vị kỹ năng yếu nhất — dùng cho sổ phụ huynh và gợi ý ôn */
export function weakestUnits(mastery = {}, n = 5) {
  return Object.entries(mastery)
    .map(([unit, m]) => ({ unit, p: m.p ?? 0, nAttempts: m.nAttempts ?? 0 }))
    .filter((x) => x.nAttempts > 0)
    .sort((a, b) => a.p - b.p)
    .slice(0, n);
}

/** Chương đang học (chương của micro được gợi ý) */
export const currentChapter = (plan) => (plan?.micro ? chapterOf(plan.micro.microId) : null);
