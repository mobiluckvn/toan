/**
 * Nạp nội dung bài học từ thư mục tĩnh (Hosting/CDN) — không cần API.
 * Cấu trúc thư mục public/:
 *    content/lessons/DL_KSN5Q1_B49_M1.json
 *    content/figures/KSN5Q1_B49_M1_F1.png
 */
const BASE = import.meta?.env?.BASE_URL || '/';
export const CONTENT = BASE.replace(/\/$/, '') + '/content';

/** DL:KSN5Q1.B49.M1 → DL_KSN5Q1_B49_M1 */
export const idToFile = (microId) => microId.replace('DL:', 'DL_').replace(/\./g, '_');

/** B49.M1 (dạng gọn người dùng gõ) → DL:KSN5Q1.B49.M1 */
export const shortToId = (s) => (s.startsWith('DL:') ? s : `DL:KSN5Q1.${s}`);

const cache = new Map();

export async function loadLesson(microId) {
  if (cache.has(microId)) return cache.get(microId);
  const url = `${CONTENT}/lessons/${idToFile(microId)}.json`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Không nạp được bài ${microId} (${res.status})`);
  const data = await res.json();
  cache.set(microId, data);
  return data;
}

/** figureSpec lưu "figures/KSN5Q1_B49_M1_F1.png" → URL đầy đủ */
export const figureSrc = (fig) => (fig?.file ? `${CONTENT}/${fig.file}` : null);

/** Danh sách 168 micro theo đúng thứ tự học */
export function allMicroIds() {
  const out = [];
  for (let b = 1; b <= 56; b++) for (const k of [1, 2, 3]) out.push(`DL:KSN5Q1.B${b}.M${k}`);
  return out;
}

/** Micro kế tiếp / trước đó — ưu tiên series.next trong dữ liệu, không có thì theo thứ tự */
export function neighborIds(microId, lesson) {
  const list = allMicroIds();
  const i = list.indexOf(microId);
  const next = lesson?.series?.next && lesson.series.next.startsWith('DL:')
    ? lesson.series.next : (i >= 0 && i < list.length - 1 ? list[i + 1] : null);
  const prev = lesson?.series?.prev && lesson.series.prev.startsWith('DL:')
    ? lesson.series.prev : (i > 0 ? list[i - 1] : null);
  return { prev, next };
}

/** Chương của một micro (1–14) */
export const chapterOf = (microId) => {
  const b = Number(microId.split('.B')[1].split('.M')[0]);
  return Math.ceil(b / 4);
};
