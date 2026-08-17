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

/**
 * SỐ PHÚT SUY RA — cộng khoảng cách giữa các lượt trả lời, nghỉ > 5 phút thì bỏ.
 *
 * ⚠ ĐÂY LÀ PHÉP CŨ, GIỮ LẠI CHO DỮ LIỆU CŨ. Nó đếm hụt nặng kể từ khi cả bốn quyển
 * chuyển sang video: phần giảng là 405 video, cộng lại 390,7 phút, mà xem video thì
 * con không bấm gì nên không một giây nào được đếm. Con xem trọn video sáu mươi lăm
 * giây rồi trả lời đúng ngay câu chốt thì phép này ra 0 phút. Nó còn bỏ luôn quãng
 * làm câu ĐẦU TIÊN (không có lượt nào đứng trước) và quãng sau câu cuối.
 *
 * Số ĐO THẬT nay do máy con ghi (`src/mon/toan/lib/dongHo.js`) rồi cộng dồn theo
 * ngày ở `hocBa/{uid}/muc` `loai='gio'`. Dùng `phutHoc()` bên dưới, nó tự chọn.
 */
export function minutesStudied(attempts, gapMs = 5 * 60 * 1000) {
  const ts = attempts.filter(DU_TIN_CAY).map((a) => a.ts).sort((x, y) => x - y);
  let total = 0;
  for (let i = 1; i < ts.length; i++) {
    const d = ts[i] - ts[i - 1];
    if (d > 0 && d <= gapMs) total += d;
  }
  return Math.round(total / 60000);
}

/**
 * Số phút học của một khoảng — LẤY SỐ ĐO THẬT khi có, không thì suy ra như cũ.
 *
 * Trả về cả `nguon` để màn hình nói thật với bố mẹ: `'do'` là máy con bấm giờ từng
 * bước (có tính cả lúc xem giảng), `'suyRa'` là ước lượng từ khoảng cách giữa các
 * câu trả lời và **chắc chắn thiếu phần xem giảng**. Hai con số khác nhau về bản
 * chất; trộn làm một rồi hiện chung một nhãn là nói dối bố mẹ.
 *
 * `soGio` là các tài liệu `loai='gio'` trong khoảng: [{ngay, giay, giayXem, giayLam}].
 */
export function phutHoc(attempts, soGio = [], { from = null, to = null } = {}) {
  const trong = soGio.filter((g) => {
    if (!g || typeof g.giay !== 'number') return false;
    const m = Date.parse(`${g.ngay}T00:00:00+07:00`);
    if (Number.isNaN(m)) return false;
    /* So theo NGÀY: một tài liệu là trọn một ngày, nên chỉ cần ngày ấy chạm khoảng. */
    return (from === null || m + 86399999 >= from) && (to === null || m <= to);
  });
  if (trong.length) {
    const giay = trong.reduce((s, g) => s + (g.giay || 0), 0);
    return {
      phut: Math.round(giay / 60),
      phutXem: Math.round(trong.reduce((s, g) => s + (g.giayXem || 0), 0) / 60),
      phutLam: Math.round(trong.reduce((s, g) => s + (g.giayLam || 0), 0) / 60),
      nguon: 'do',
      soNgayCoHoc: trong.filter((g) => (g.giay || 0) > 0).length,
    };
  }
  return {
    phut: minutesStudied(attempts),
    phutXem: null, phutLam: null,
    nguon: 'suyRa',
    soNgayCoHoc: new Set(attempts.filter(DU_TIN_CAY)
      .map((a) => new Date(a.ts).toISOString().slice(0, 10))).size,
  };
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
                                    soGio = [], index = {}, now = Date.now(), days = 7 }) {
  const from = now - days * 86400000;
  const win = inRange(attempts, from, now);
  const micros = [...new Set(win.map((a) => a.microId))];
  const passed = Object.values(progress).filter((m) => m.pass).length;
  const units = Object.values(mastery);
  const mastered = units.filter((u) => (u.p ?? 0) >= 0.85).length;

  const gio = phutHoc(win, soGio, { from, to: now });
  const traps = topTraps(win, index);
  const focus = traps[0]?.microId;
  const tip = focus ? index[focus.replace(/[:.]/g, '_')] : null;

  return {
    learnerId,
    periodDays: days,
    generatedAt: now,
    minutes: gio.phut,
    /* Số phút này ĐO ĐƯỢC hay SUY RA — màn hình phải nói thật, vì bản suy ra không
       thấy phần xem giảng, mà phần giảng nay là toàn bộ video của bốn quyển. */
    nguonGio: gio.nguon,
    phutXem: gio.phutXem,
    phutLam: gio.phutLam,
    soNgayCoHoc: gio.soNgayCoHoc,
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
