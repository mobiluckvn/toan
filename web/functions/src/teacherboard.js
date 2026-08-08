/**
 * BẢNG GIÁO VIÊN — tổng hợp nhật ký thô của TOÀN BỘ học sinh thành MỘT document.
 *
 * Vì sao dựng sẵn: vài trăm học sinh học một tuần sinh ra hàng chục nghìn dòng attempts.
 * Cô mở app mà quét từng ấy dòng thì vừa chậm vừa tốn tiền đọc. Function chạy đêm,
 * cô đọc đúng MỘT document.
 *
 * Thuần hàm, không đụng Firestore — chạy test bằng node (test/teacherboard.test.mjs).
 */

/** Ưu tiên mốc máy chủ; chưa có thì đành dùng giờ máy của học sinh */
export const stampOf = (a) => (typeof a.serverTs === 'number' ? a.serverTs : a.ts);

export const inWindow = (attempts, from, to) =>
  attempts.filter((a) => { const t = stampOf(a); return t >= from && t <= to; });

/**
 * Bẫy nhiều em sập nhất — thứ cô cần nhất để biết tiết sau dạy lại cái gì.
 * Đếm theo SỐ EM chứ không theo số lượt: một em làm đi làm lại 5 lần không
 * biến một bài thành vấn đề của cả trường.
 */
export function topTraps(attempts, index = {}, n = 8) {
  const byMicro = new Map();
  for (const a of attempts) {
    if (!a.mustPass || a.correct) continue;
    if (!byMicro.has(a.microId)) byMicro.set(a.microId, new Set());
    byMicro.get(a.microId).add(a.learnerId);
  }
  return [...byMicro.entries()]
    .map(([microId, set]) => {
      const meta = index[microId.replace(/[:.]/g, '_')] || {};
      return { microId, learners: set.size, trapName: meta.trapName || '', title: meta.title || '' };
    })
    .sort((x, y) => y.learners - x.learners || x.microId.localeCompare(y.microId))
    .slice(0, n);
}

/**
 * Em đang TẮC: thử một bài từ `minTries` lần trở lên mà vẫn chưa qua.
 * Đây là danh sách cô gọi tên, nên phải chắc — chỉ tính bài CHƯA đạt.
 */
export function stuckLearners(attempts, progress = {}, { minTries = 3, n = 20 } = {}) {
  const tries = new Map();
  for (const a of attempts) {
    if (a.phase !== 'practice' && a.phase !== 'assess') continue;
    const k = `${a.learnerId}|${a.microId}`;
    tries.set(k, (tries.get(k) || 0) + 1);
  }
  const out = [];
  for (const [k, count] of tries) {
    if (count < minTries) continue;
    const [learnerId, microId] = k.split('|');
    if (progress[learnerId]?.[microId]?.pass) continue;
    out.push({ learnerId, microId, tries: count });
  }
  return out.sort((x, y) => y.tries - x.tries || x.learnerId.localeCompare(y.learnerId)).slice(0, n);
}

/** Một dòng cho mỗi học sinh — kể cả em tuần này chưa vào học buổi nào */
/**
 * Bản ghi thuộc Quyển 2 hay Quyển 1 — nhận ra bằng tiền tố của mã nội dung.
 * Quyển 1 ghi "DL:KSN5Q1.B1.M1", Quyển 2 ghi "DR:KSN5Q2.V01".
 * Không tách thì cô nhìn một cục "đã trả lời 300 câu" mà không biết con đang học
 * bài hay đang luyện thi — hai việc cần hai cách hỗ trợ khác nhau.
 */
export const laQuyen2 = (a) => String(a?.microId || '').startsWith('DR:KSN5Q2');

export function learnerRows(attempts, roster = [], progress = {}) {
  const rows = new Map(roster.map((r) => [r.uid, {
    uid: r.uid, displayName: r.displayName || '', email: r.email || '',
    sessions: new Set(), answered: 0, correct: 0, lastAt: null,
    q2Answered: 0, q2Correct: 0, q2Vong: new Set(),
  }]));
  for (const a of attempts) {
    const row = rows.get(a.learnerId);
    if (!row) continue;                       // tài khoản đã xoá — không dựng dòng ma
    row.sessions.add(a.sessionId);
    row.answered++;
    if (a.correct) row.correct++;
    if (laQuyen2(a)) {
      row.q2Answered++;
      if (a.correct) row.q2Correct++;
      row.q2Vong.add(a.microId);
    }
    const t = stampOf(a);
    if (row.lastAt === null || t > row.lastAt) row.lastAt = t;
  }
  return [...rows.values()].map((r) => ({
    uid: r.uid,
    displayName: r.displayName,
    email: r.email,
    sessions: r.sessions.size,
    answered: r.answered,
    correctRate: r.answered ? Math.round((r.correct / r.answered) * 100) : null,
    microsPassed: Object.values(progress[r.uid] || {}).filter((m) => m.pass).length,
    /* Cột riêng cho Quyển 2 — luyện thi có đồng hồ, khác hẳn học bài */
    q2Answered: r.q2Answered,
    q2CorrectRate: r.q2Answered ? Math.round((r.q2Correct / r.q2Answered) * 100) : null,
    q2Vong: r.q2Vong.size,
    lastAt: r.lastAt,
  })).sort((x, y) => x.displayName.localeCompare(y.displayName, 'vi'));
}

/**
 * Dựng bảng giáo viên cho một khoảng (mặc định 7 ngày).
 * roster:   [{uid, displayName, email}]  — mọi tài khoản vai trò learner
 * progress: { uid: { microId: {pass, ...} } }
 */
export function buildTeacherBoard({
  roster = [], attempts = [], progress = {}, index = {}, now = Date.now(), days = 7,
}) {
  const from = now - days * 86400000;
  const win = inWindow(attempts, from, now);
  const rows = learnerRows(win, roster, progress);
  const answered = win.length;
  const active = rows.filter((r) => r.answered > 0);
  const q2 = win.filter(laQuyen2);

  return {
    periodDays: days,
    generatedAt: now,
    learners: roster.length,
    activeLearners: active.length,
    idleLearners: rows.filter((r) => r.answered === 0).map((r) => r.uid),
    answered,
    correctRate: answered ? Math.round((win.filter((a) => a.correct).length / answered) * 100) : 0,
    avgMicrosPassed: rows.length
      ? Math.round((rows.reduce((s, r) => s + r.microsPassed, 0) / rows.length) * 10) / 10
      : 0,
    /* Số liệu Quyển 2 để RIÊNG, không trộn vào cột chung: học bài và luyện thi có
       đồng hồ là hai việc khác nhau, cô cần nhìn tách ra mới biết giúp kiểu gì. */
    q2Answered: q2.length,
    q2CorrectRate: q2.length
      ? Math.round((q2.filter((a) => a.correct).length / q2.length) * 100) : null,
    q2Learners: new Set(q2.map((a) => a.learnerId)).size,
    q2Vong: new Set(q2.map((a) => a.microId)).size,
    topTraps: topTraps(win, index),
    stuck: stuckLearners(win, progress),
    rows,
  };
}

/** Câu mở đầu cô đọc lướt trong 3 giây */
export function boardHeadline(r) {
  if (!r.answered) return 'Tuần này chưa em nào vào học.';
  const t = r.topTraps[0];
  return `${r.activeLearners}/${r.learners} em có học, trả lời ${r.answered} câu, đúng ${r.correctRate}%.`
    + (t ? ` Bẫy nhiều em sập nhất: ${t.trapName || t.title || t.microId} — ${t.learners} em.` : '');
}
