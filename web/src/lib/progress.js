/**
 * TIẾN ĐỘ HỌC — lưu tại máy (localStorage) ở giai đoạn B.
 * Giai đoạn C sẽ đồng bộ lên Firestore nhưng GIỮ NGUYÊN hình dạng dữ liệu này.
 */
import { allMicroIds, chapterOf } from './content.js';

const KEY = 'ttd5.progress.v1';

export const emptyProgress = () => ({ micros: {}, chapters: {}, updatedAt: null });

export function loadProgress(storage = globalThis.localStorage) {
  try {
    const raw = storage?.getItem(KEY);
    return raw ? { ...emptyProgress(), ...JSON.parse(raw) } : emptyProgress();
  } catch { return emptyProgress(); }
}

export function saveProgress(p, storage = globalThis.localStorage) {
  try { storage?.setItem(KEY, JSON.stringify({ ...p, updatedAt: new Date().toISOString() })); }
  catch { /* chế độ riêng tư — bỏ qua, học vẫn chạy */ }
  return p;
}

/** Ghi kết quả một micro sau khi con bấm xong trang kết */
export function recordMicro(progress, microId, grade) {
  const prev = progress.micros[microId] || {};
  return {
    ...progress,
    micros: {
      ...progress.micros,
      [microId]: {
        done: true,
        pass: !!grade.pass,
        mustPassOK: !!grade.mustOK,
        best: Math.max(prev.best || 0, grade.right || 0),
        total: grade.total || 0,
        attempts: (prev.attempts || 0) + 1,
        at: new Date().toISOString(),
      },
    },
  };
}

/* ─────────── Nhớ chỗ đang học dở ─────────── */
/**
 * Con học nửa chừng rồi thoát (mẹ gọi ăn cơm, hết pin, bấm nhầm nút quay lại) —
 * lần sau mở lại phải về ĐÚNG chỗ đó, không bắt làm lại 15 bước đã làm.
 * Chỉ nhớ khi đã đi được vài bước và bài chưa đạt; bài đạt rồi thì mở lại từ đầu.
 */
export function saveSpot(progress, microId, step, total) {
  if (!(step > 0) || progress.micros[microId]?.pass) return progress;
  const prev = progress.micros[microId] || {};
  if (prev.step === step) return progress;
  return {
    ...progress,
    micros: { ...progress.micros, [microId]: { ...prev, step, steps: total } },
  };
}

/** Bước con đang dở ở micro này — 0 nghĩa là học từ đầu */
export function resumeSpot(progress, microId) {
  const m = progress.micros[microId];
  return m && !m.pass && m.step > 0 ? { step: m.step, steps: m.steps || 0 } : null;
}

/** Xoá chỗ đánh dấu — dùng khi con chủ động chọn học lại từ đầu, hoặc đã đạt */
export function clearSpot(progress, microId) {
  const m = progress.micros[microId];
  if (!m || !m.step) return progress;
  const { step, steps, ...rest } = m;
  return { ...progress, micros: { ...progress.micros, [microId]: rest } };
}

export function recordChapter(progress, chapter, grade) {
  const prev = progress.chapters[chapter] || {};
  return {
    ...progress,
    chapters: {
      ...progress.chapters,
      [chapter]: {
        done: true, pass: !!grade.pass,
        best: Math.max(prev.best || 0, grade.right || 0),
        total: grade.total || 0,
        attempts: (prev.attempts || 0) + 1,
        at: new Date().toISOString(),
      },
    },
  };
}

/* ─────────── Luật mở khoá ─────────── */
/**
 * Micro mở khi micro TRƯỚC đã đạt (đủ điểm VÀ đúng câu bẫy).
 * Micro đầu tiên luôn mở. Cổng mustPass là điểm mấu chốt: sai câu bẫy thì không đi tiếp.
 */
/* ─────────── Hai chế độ học ─────────── */
/**
 * 'chuongtrinh' — đi theo chương trình đề xuất: học lần lượt từ bài đầu đến bài cuối.
 *                 Đúng thứ tự sư phạm, bài sau dùng lại bẫy của bài trước.
 * 'tuchon'      — con thích chủ đề nào thì vào chủ đề đó. TRONG một chương vẫn phải
 *                 học lần lượt, vì các bài trong chương xây chồng lên nhau.
 */
export const MODES = ['chuongtrinh', 'tuchon'];
export const modeOf = (progress) => (MODES.includes(progress?.mode) ? progress.mode : 'chuongtrinh');
export const setMode = (progress, mode) =>
  (MODES.includes(mode) ? { ...progress, mode } : progress);

export function isMicroUnlocked(progress, microId, list = allMicroIds()) {
  const i = list.indexOf(microId);
  if (i < 0) return false;
  if (i === 0) return true;

  if (modeOf(progress) === 'tuchon') {
    // Bài đầu của MỖI chương luôn mở — con chọn chủ đề nào cũng vào được ngay.
    const ch = chapterOf(microId);
    const dauChuong = list.find((id) => chapterOf(id) === ch);
    if (microId === dauChuong) return true;
  }

  const prev = progress.micros[list[i - 1]];
  return !!(prev?.pass);
}

/** Kỳ sát hạch chương mở khi TẤT CẢ micro của chương đã đạt */
export function isChapterExamUnlocked(progress, chapter, list = allMicroIds()) {
  const ms = list.filter((id) => chapterOf(id) === chapter);
  return ms.length > 0 && ms.every((id) => progress.micros[id]?.pass);
}

/** Micro tiếp theo con nên học (bài đầu tiên chưa đạt và đã mở) */
export function nextToStudy(progress, list = allMicroIds()) {
  for (const id of list) {
    if (!progress.micros[id]?.pass && isMicroUnlocked(progress, id, list)) return id;
  }
  return null;
}

/* ─────────── Thống kê hiển thị ─────────── */
export function chapterStats(progress, chapter, list = allMicroIds()) {
  const ms = list.filter((id) => chapterOf(id) === chapter);
  const done = ms.filter((id) => progress.micros[id]?.pass).length;
  return {
    total: ms.length, done,
    percent: Math.round((done / ms.length) * 100),
    examUnlocked: isChapterExamUnlocked(progress, chapter, list),
    examPassed: !!progress.chapters[chapter]?.pass,
  };
}

export function overallStats(progress, list = allMicroIds()) {
  const done = list.filter((id) => progress.micros[id]?.pass).length;
  const badges = Object.values(progress.chapters).filter((c) => c.pass).length;
  return { total: list.length, done, percent: Math.round((done / list.length) * 100), badges };
}

/** Trạng thái hiển thị của một micro trong danh sách */
export function microState(progress, microId, list = allMicroIds()) {
  const m = progress.micros[microId];
  if (m?.pass) return 'passed';
  if (m?.done) return 'tried';
  return isMicroUnlocked(progress, microId, list) ? 'open' : 'locked';
}
