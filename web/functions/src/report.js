/**
 * SỔ PHỤ HUYNH — tổng hợp từ nhật ký thô thành MỘT document.
 * Bố mẹ mở app đọc 1 lần, thay vì quét hàng nghìn attempts.
 * Thuần hàm, có test (test/report.test.mjs).
 */

/** Gom các lượt trả lời trong khoảng thời gian */
export const inRange = (attempts, from, to) => attempts.filter((a) => a.ts >= from && a.ts <= to);

/**
 * Dòng ghi đủ tin cậy để tính THỜI GIAN.
 * Bản ghi cũ (v < 2) có `ms` tính từ lúc mở bài và cả loạt chung một mốc `ts` —
 * đem tính số phút học hay "câu làm lâu" là ra số sai. Nhật ký bất biến nên
 * không sửa được; chỉ có thể loại chúng ra khỏi thống kê thời gian.
 */
export const DU_TIN_CAY = (a) => (a?.v ?? 1) >= 2;

/** Ước lượng số phút học: tổng thời gian giữa các lượt, ngắt quãng > 5 phút thì không tính */
export function minutesStudied(attempts, gapMs = 5 * 60 * 1000) {
  const ts = attempts.filter(DU_TIN_CAY).map((a) => a.ts).sort((x, y) => x - y);
  let total = 0;
  for (let i = 1; i < ts.length; i++) {
    const d = ts[i] - ts[i - 1];
    if (d > 0 && d <= gapMs) total += d;
  }
  return Math.round(total / 60000);
}

/** Bẫy hay sập nhất — thứ bố mẹ và cô giáo cần nhất */
export function topTraps(attempts, index = {}, n = 3) {
  const miss = {};
  for (const a of attempts) {
    if (!a.mustPass || a.correct) continue;
    const k = a.microId;
    miss[k] = (miss[k] || 0) + 1;
  }
  return Object.entries(miss)
    .sort((x, y) => y[1] - x[1])
    .slice(0, n)
    .map(([microId, times]) => ({
      microId, times,
      trapName: index[microId.replace(/[:.]/g, '_')]?.trapName || '',
    }));
}

/** Câu làm lâu mà vẫn sai — dấu hiệu con đang bế tắc chứ không phải ẩu */
export function stuckItems(attempts, msThreshold = 45000, n = 3) {
  return attempts
    .filter((a) => DU_TIN_CAY(a) && !a.correct && (a.ms ?? 0) >= msThreshold)
    .sort((x, y) => (y.ms ?? 0) - (x.ms ?? 0))
    .slice(0, n)
    .map((a) => ({ microId: a.microId, itemId: a.itemId, seconds: Math.round((a.ms ?? 0) / 1000) }));
}

/**
 * Dựng sổ phụ huynh cho một khoảng (mặc định 7 ngày).
 * lessonsIndex: { DL_KSN5Q1_B49_M1: {microId, homeActivity, watchFor, title} }
 */
export function buildParentReport({ learnerId, attempts, progress = {}, mastery = {},
                                    index = {}, now = Date.now(), days = 7 }) {
  const from = now - days * 86400000;
  const win = inRange(attempts, from, now);
  const micros = [...new Set(win.map((a) => a.microId))];
  const passed = Object.values(progress).filter((m) => m.pass).length;
  const units = Object.values(mastery);
  const mastered = units.filter((u) => (u.p ?? 0) >= 0.85).length;

  const traps = topTraps(win, index);
  const focus = traps[0]?.microId;
  const tip = focus ? index[focus.replace(/[:.]/g, '_')] : null;

  return {
    learnerId,
    periodDays: days,
    generatedAt: now,
    minutes: minutesStudied(win),
    /* Bao nhiêu lượt trong kỳ này KHÔNG dùng được cho thống kê thời gian. > 0 thì
       màn hình phải nói rõ, đừng để bố mẹ tưởng con học 0 phút. */
    luotThieuGio: win.filter((a) => !DU_TIN_CAY(a)).length,
    sessions: new Set(win.map((a) => a.sessionId)).size,
    answered: win.length,
    correctRate: win.length ? Math.round((win.filter((a) => a.correct).length / win.length) * 100) : 0,
    microsTouched: micros.length,
    microsPassed: passed,
    unitsMastered: mastered,
    unitsTotal: units.length,
    topTraps: traps,
    stuck: stuckItems(win),
    suggestion: tip?.homeActivity || '',
    watchFor: tip?.watchFor || '',
    focusMicro: focus || null,
  };
}

/** Câu văn ngắn cho bố mẹ đọc lướt */
export function reportHeadline(r) {
  if (!r.answered) return 'Tuần này con chưa vào học buổi nào.';
  const t = r.topTraps[0];
  return `Con học ${r.minutes} phút trong ${r.sessions} buổi, trả lời ${r.answered} câu, đúng ${r.correctRate}%.`
    + (t ? ` Bẫy hay sập nhất: ${t.trapName || t.microId} (${t.times} lần).` : '');
}
