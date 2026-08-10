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

/* ═══════════ LUYỆN THEO CHỦ ĐỀ — thang lùi/tiến ═══════════
 *
 * Khác hẳn `micros`/`chapters` ở trên: hai thứ ấy đo "con đã học xong bài nào",
 * còn lát này đo "con vững chủ đề nào tới lớp mấy". Cùng một chủ đề trải bốn lớp,
 * nên chỗ hổng của con là một CON SỐ LỚP, không phải một danh sách bài.
 *
 * Luật đi: đạt thì lên bậc trên, kém thì lùi bậc dưới, chạm sàn thì dừng tử tế.
 * Viết thành hàm thuần ở đây (không nhét trong component) để phép kiểm chạy được
 * mọi ngả — nhất là hai ngả bìa, chạm sàn và chạm trần, là chỗ dễ rơi vào hư không.
 */

/** Đạt là đúng 2/3 số câu — cân với ngưỡng 8/10 của kỳ sát hạch. */
export const nguongDat = (tong) => Math.max(1, Math.ceil((tong * 2) / 3));

/**
 * Bậc con nên bắt đầu: bậc CAO NHẤT không vượt lớp của con. Thang thiếu bậc đúng
 * lớp ấy thì lấy bậc dưới gần nhất; thấp hơn mọi bậc thì lấy bậc thấp nhất — thà
 * cho con làm bài trên lớp mình còn hơn không có gì để làm.
 */
export function bacBatDau(thang = [], lopCon = 5) {
  const lops = thang.map((b) => b.lop);
  if (!lops.length) return null;
  const vua = lops.filter((l) => l <= lopCon);
  return vua.length ? vua[vua.length - 1] : lops[0];
}

/**
 * Sau một lượt luyện thì đi đâu.
 *   { hanh: 'len',   lop }  đạt rồi, còn bậc trên
 *   { hanh: 'xong' }        đạt ở bậc cao nhất — vững chủ đề này
 *   { hanh: 'xuong', lop }  chưa đạt, lùi một bậc cho chắc gốc
 *   { hanh: 'san' }         chưa đạt mà đã ở bậc thấp nhất — dừng, báo bố mẹ
 */
export function buocSau(thang = [], lop, dat = 0, tong = 0) {
  const lops = thang.map((b) => b.lop);
  const i = lops.indexOf(lop);
  if (i < 0) return { hanh: 'san' };
  if (dat >= nguongDat(tong)) {
    return i === lops.length - 1 ? { hanh: 'xong' } : { hanh: 'len', lop: lops[i + 1] };
  }
  return i === 0 ? { hanh: 'san' } : { hanh: 'xuong', lop: lops[i - 1] };
}

/** Ghi kết quả một lượt luyện chủ đề tại một bậc. */
export function ghiLuyenChuDe(progress, maDang, lop, { dat = 0, tong = 0 } = {}) {
  const cu = progress.chuDe?.[maDang] || { bac: {} };
  const bacCu = cu.bac[String(lop)] || {};
  return {
    ...progress,
    chuDe: {
      ...(progress.chuDe || {}),
      [maDang]: {
        ...cu,
        bac: {
          ...cu.bac,
          [String(lop)]: {
            dat, tong,
            pass: dat >= nguongDat(tong),
            /* `best` giữ lần cao nhất: lùi xuống rồi lên lại thì lần sau đè lên lần
               trước, mà cái đáng nhớ là con ĐÃ từng làm được tới đâu. */
            best: Math.max(bacCu.best || 0, dat),
            lan: (bacCu.lan || 0) + 1,
            at: new Date().toISOString(),
          },
        },
        dangO: lop,
      },
    },
  };
}

/** Bậc cao nhất con đã đạt ở một chủ đề — null nếu chưa đạt bậc nào. */
export function bacDaVung(progress, maDang) {
  const bac = progress.chuDe?.[maDang]?.bac || {};
  const dat = Object.entries(bac).filter(([, v]) => v.pass).map(([l]) => Number(l));
  return dat.length ? Math.max(...dat) : null;
}
