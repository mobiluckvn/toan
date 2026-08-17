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

/**
 * Mã SÁCH của một bài, suy từ chính mã bài: `DL:KSN5Q1.B1.M1` → `KSN5Q1`.
 *
 * Đọc từ mã chứ không tra sổ đăng ký: hàm nền chạy trên máy chủ, không có sổ ấy, mà
 * chép sổ sang đây là hai bản dễ lệch nhau. Màn hình dịch ngược `KSN2` → "lớp 2"
 * bằng `maKy()` của sổ đăng ký, nên thêm quyển mới không phải đụng vào đây.
 */
/* Nhận cả hai cách viết: mã bài `DL:KSN5Q1.B1.M1` và mã tài liệu `DL_KSN5Q1_B1_M1`
   (tài liệu cũ thiếu trường `microId` thì chỉ còn mã tài liệu để mà suy). */
export const maSach = (id) => (String(id || '').match(/^[A-Z]+[:_]([A-Za-z0-9]+)[._]/) || [])[1] || '?';

/**
 * SỐ PHÚT HỌC của một em — cùng công thức với sổ phụ huynh: cộng khoảng cách giữa
 * các lượt, ngắt quãng quá `gapMs` thì coi như đã nghỉ.
 *
 * Chỉ tính dòng ghi từ bản v ≥ 2: dòng cũ dùng chung một mốc `ts` cho cả loạt nên
 * cộng ra 0, mà hiện "0 phút" thì cô đọc thành "em không học".
 */
export function minutesOf(attempts, gapMs = 5 * 60 * 1000) {
  const ts = attempts.filter((a) => (a?.v ?? 1) >= 2).map((a) => a.ts).sort((x, y) => x - y);
  let total = 0;
  for (let i = 1; i < ts.length; i++) {
    const d = ts[i] - ts[i - 1];
    if (d > 0 && d <= gapMs) total += d;
  }
  return Math.round(total / 60000);
}

/**
 * Số phút ĐO THẬT của một em trong khoảng, lấy từ sổ giờ theo ngày.
 * Trả `null` khi em chưa có sổ giờ nào — để nơi gọi biết mà lùi về phép suy ra,
 * chứ không hiện 0 phút rồi cô đọc thành "em không học".
 */
export function phutDoThat(mucHocBa = [], from = null, to = null) {
  const gio = mucHocBa.filter((m) => m?.loai === 'gio' && typeof m.giay === 'number');
  if (!gio.length) return null;
  const trong = gio.filter((g) => {
    const t = Date.parse(`${g.ngay}T00:00:00+07:00`);
    if (Number.isNaN(t)) return false;
    return (from === null || t + 86399999 >= from) && (to === null || t <= to);
  });
  if (!trong.length) return null;
  return Math.round(trong.reduce((s, g) => s + (g.giay || 0), 0) / 60);
}

export function learnerRows(attempts, roster = [], progress = {}, hocBa = {}, khoang = {}) {
  const rows = new Map(roster.map((r) => [r.uid, {
    uid: r.uid, displayName: r.displayName || '', email: r.email || '',
    sessions: new Set(), answered: 0, correct: 0, lastAt: null,
    q2Answered: 0, q2Correct: 0, q2Vong: new Set(), luot: [],
  }]));
  for (const a of attempts) {
    const row = rows.get(a.learnerId);
    if (!row) continue;                       // tài khoản đã xoá — không dựng dòng ma
    row.sessions.add(a.sessionId);
    row.answered++;
    row.luot.push(a);
    if (a.correct) row.correct++;
    if (laQuyen2(a)) {
      row.q2Answered++;
      if (a.correct) row.q2Correct++;
      row.q2Vong.add(a.microId);
    }
    const t = stampOf(a);
    if (row.lastAt === null || t > row.lastAt) row.lastAt = t;
  }
  return [...rows.values()].map((r) => {
    /* BÀI ĐẠT TÁCH THEO SÁCH — "em ấy đạt 47 bài" không nói lên trình độ, vì 47 bài
       lớp 2 và 47 bài lớp 5 là hai chuyện khác hẳn. Cô cần biết em đang ở quyển nào. */
    const theoSach = {};
    for (const [id, m] of Object.entries(progress[r.uid] || {})) {
      if (!m?.pass) continue;
      const s = maSach(m.microId || id);
      theoSach[s] = (theoSach[s] || 0) + 1;
    }
    return {
      uid: r.uid,
      displayName: r.displayName,
      email: r.email,
      sessions: r.sessions.size,
      answered: r.answered,
      correctRate: r.answered ? Math.round((r.correct / r.answered) * 100) : null,
      microsPassed: Object.values(progress[r.uid] || {}).filter((m) => m.pass).length,
      theoSach,
      /* Thời gian học thật, không phải số buổi: hai em cùng "3 buổi" mà một em ngồi
         12 phút, em kia 70 phút thì cần hai cách nhắc khác nhau. */
      /* ĐO THẬT khi có, không thì suy ra như cũ. Phép suy ra không thấy phần xem
         giảng — mà phần giảng nay là toàn bộ video của bốn quyển. */
      minutes: phutDoThat(hocBa[r.uid], khoang.from ?? null, khoang.to ?? null)
        ?? minutesOf(r.luot),
      nguonGio: phutDoThat(hocBa[r.uid], khoang.from ?? null, khoang.to ?? null) === null
        ? 'suyRa' : 'do',
      /* Cột riêng cho Quyển 2 — luyện thi có đồng hồ, khác hẳn học bài */
      q2Answered: r.q2Answered,
      q2CorrectRate: r.q2Answered ? Math.round((r.q2Correct / r.q2Answered) * 100) : null,
      q2Vong: r.q2Vong.size,
      lastAt: r.lastAt,
    };
  }).sort((x, y) => x.displayName.localeCompare(y.displayName, 'vi'));
}

/**
 * EM NÀO ĐANG YẾU — và YẾU KIỂU GÌ.
 *
 * `stuckLearners` ở trên trả lời "em nào tắc ở BÀI nào". Câu cô hỏi trước đó một
 * bậc là "sáng mai tôi nên gọi em nào", và câu ấy phải xếp theo EM chứ không theo bài.
 *
 * ── VÌ SAO PHẢI CÓ THỜI GIAN MỚI TRẢ LỜI ĐƯỢC ──
 *
 * Chỉ nhìn phần trăm đúng thì hai em cùng "đúng 40%" trông y hệt nhau, trong khi
 * chúng cần hai cách giúp ngược nhau:
 *
 *   · ẨU        — trả lời rất nhanh rồi sai. Em hiểu bài nhưng bấm bừa; cần nhắc
 *                 đọc kỹ, không cần giảng lại.
 *   · BỎ GIẢNG  — bấm vượt video rồi lao vào làm. Cần bảo em xem hết đã.
 *   · HỔNG      — ngồi lâu, thử đi thử lại, vẫn sai. Em thiếu phần GIẢNG; giao thêm
 *                 bài tập chỉ để em sai thêm một lượt nữa.
 *
 * Phân biệt bằng `giay`/`giayXem` mỗi bài trong `progress` (máy con bấm giờ từng
 * bước — xem `src/mon/toan/lib/dongHo.js`). Chưa đo được thì trả `'chuaRo'` chứ
 * KHÔNG đoán bừa: cô gọi nhầm em đắt hơn hẳn việc thiếu một cái nhãn.
 *
 * Ngưỡng: phải làm đủ `toiThieuCau` câu mới xét — ba câu sai liền không đủ để kết
 * luận gì về một đứa trẻ.
 */
export const NHANH_GIAY = 12;      // dưới ngần này giây một bài là bấm quá nhanh

export function emCanGiup(rows, progress = {}, {
  nguongDung = 60, toiThieuCau = 8, n = 20,
} = {}) {
  const ra = [];
  for (const r of rows) {
    if (r.answered < toiThieuCau) continue;
    if (r.correctRate === null || r.correctRate >= nguongDung) continue;

    /* Giây mỗi bài, chỉ lấy bài ĐO ĐƯỢC. `giay === null` là "chưa đo", khác hẳn 0. */
    const bai = Object.values(progress[r.uid] || {})
      .filter((m) => typeof m?.giay === 'number' && m.giay > 0);
    const giayTB = bai.length
      ? Math.round(bai.reduce((s, m) => s + m.giay, 0) / bai.length) : null;
    /* Bài mà phần XEM gần như bằng không là em bấm vượt video. */
    const boQuaGiang = bai.length
      ? bai.filter((m) => (m.giayXem ?? 0) < 5).length / bai.length : null;

    let vi = 'chuaRo';
    if (giayTB !== null) {
      if (giayTB < NHANH_GIAY) vi = 'au';
      else if (boQuaGiang !== null && boQuaGiang >= 0.5) vi = 'boQuaGiang';
      else vi = 'hong';
    }
    ra.push({
      uid: r.uid, displayName: r.displayName,
      correctRate: r.correctRate, answered: r.answered,
      minutes: r.minutes, giayMoiBai: giayTB, viSao: vi,
      /* Nặng nhất lên trước, nhưng có nhân với "đã làm bao nhiêu câu" (chặn ở 3 lần)
         để em làm 8 câu sai không nhảy lên trên em làm 60 câu cũng sai. */
      nang: Math.round((nguongDung - r.correctRate) * Math.min(r.answered / toiThieuCau, 3)),
    });
  }
  return ra.sort((x, y) => y.nang - x.nang || x.uid.localeCompare(y.uid)).slice(0, n);
}

/**
 * Dựng bảng giáo viên cho một khoảng (mặc định 7 ngày).
 * roster:   [{uid, displayName, email}]  — mọi tài khoản vai trò learner
 * progress: { uid: { microId: {pass, ...} } }
 */
export function buildTeacherBoard({
  roster = [], attempts = [], progress = {}, hocBa = {}, index = {}, now = Date.now(), days = 7,
}) {
  const from = now - days * 86400000;
  const win = inWindow(attempts, from, now);
  const rows = learnerRows(win, roster, progress, hocBa, { from, to: now });
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
    /* Xếp theo EM, kèm lý do yếu — thứ cô nhìn trước khi nhìn bất cứ cột nào khác. */
    canGiup: emCanGiup(rows, progress),
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
