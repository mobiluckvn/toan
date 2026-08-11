/**
 * LỚP DỮ LIỆU HỌC — dựng bản ghi attempts và hàng đợi đồng bộ.
 * Tách khỏi Firebase SDK để chạy test được bằng node (test/sync.test.mjs).
 *
 * Nguyên tắc: ghi NHẬT KÝ THÔ (mỗi lượt trả lời một dòng), không chỉ ghi điểm tổng —
 * sau này mới trả lời được "bẫy nào cả lớp hay sập nhất", "câu nào con làm lâu mà vẫn sai".
 */

/**
 * MỘT TÀI KHOẢN = MỘT HỌC SINH.
 * Phụ huynh và con dùng chung một tài khoản, nên `learnerId` trong mọi bản ghi
 * CHÍNH LÀ `uid` của tài khoản đăng nhập. Không có hồ sơ con tách rời.
 */
export const COLLECTIONS = {
  users: 'users',                 // learner · teacher · admin — role nằm trong doc
  otpCodes: 'otpCodes',           // chỉ Cloud Function đụng tới
  attempts: 'attempts',
  mastery: (uid) => `mastery/${uid}/units`,
  progress: (uid) => `progress/${uid}/micros`,
  reviewQueue: (uid) => `reviewQueue/${uid}/cards`,
  report: 'report',               // sổ học của từng người, Function dựng mỗi đêm
  teacherBoard: 'teacherBoard',   // bảng toàn hệ thống cho giáo viên
};

// ROLES · normalizeEmail · buildUserDoc dùng chung từ functions/src/user.js
export { ROLES, normalizeEmail, buildUserDoc } from '../../functions/src/user.js';


/**
 * Đã có hồ sơ con THẬT trên máy chủ chưa?
 * 'local' là mã tạm khi con học mà chưa đăng nhập. Đẩy lên với mã đó thì luật bảo mật
 * từ chối (không có learners/local) — mà từ chối thì im lặng, bài học coi như bay mất.
 * Chưa đăng nhập thì CHỈ xếp hàng đợi, giữ nguyên cho đến khi có tài khoản.
 */
export const isCloudLearner = (id) => !!id && id !== 'local';

/** id ổn định để ghi lại nhiều lần không sinh bản trùng (idempotent) */
export const attemptId = (learnerId, sessionId, microId, itemId, seq) =>
  `${learnerId}_${sessionId}_${microId.replace('DL:KSN5Q1.', '')}_${itemId}_${seq}`;

/**
 * PHIÊN BẢN BẢN GHI. Nhật ký là BẤT BIẾN — không sửa lại được, kể cả admin — nên
 * dòng ghi bằng luật cũ sẽ nằm lẫn với dòng mới mãi mãi.
 *
 *   v < 2  (hoặc không có v): `ms` là thời gian tính từ lúc MỞ BÀI chứ không phải
 *          thời gian làm riêng câu ấy, và cả loạt dùng chung một mốc `ts`.
 *          Đem tính "câu con làm lâu" hay "số phút học" là ra số SAI.
 *   v = 2  ms đo riêng từng câu, ts riêng từng lượt, có answer/expected/mode.
 *
 * Thống kê theo thời gian chỉ được dùng dòng v ≥ 2. Thà nói "chưa có số liệu" còn
 * hơn hiện một con số sai cho bố mẹ tin theo.
 */
export const PHIEN_BAN_BAN_GHI = 2;

/** Đáp án con gõ có thể là mảng nhiều ô — gọn lại thành một chuỗi đọc được, cắt ngắn */
export const CHU_TOI_DA = 120;
export function goiDapAn(v) {
  const s = Array.isArray(v) ? v.filter((x) => x !== undefined).join(' | ') : String(v ?? '');
  const g = s.replace(/\s+/g, ' ').trim();
  return g.length > CHU_TOI_DA ? `${g.slice(0, CHU_TOI_DA - 1)}…` : g;
}

/**
 * Chuyển nhật ký một phiên học thành các bản ghi attempts.
 *
 * MỘT DÒNG CHO MỘT LƯỢT BẤM "Kiểm tra", không phải một dòng cho một câu. Con sai
 * hai lần rồi mới đúng thì có ba dòng — cô giáo nhìn ra con sai CÁI GÌ trước khi
 * làm được, chứ không chỉ thấy "cuối cùng cũng xong".
 *
 * events: [{phase, itemId, ok, tries, hintsUsed, ms, mustPass, bktUnit,
 *           answer, expected, mode, revealed}]
 *   · phase   'practice' | 'assess' | 'check' | 'worked'  (luật bảo mật nhận cả bốn)
 *   · answer  con gõ/bấm gì — trường quý nhất để cô đoán ra con hiểu sai chỗ nào
 *   · ms      thời gian làm RIÊNG câu ấy, không phải tính từ lúc mở bài
 */
export function buildAttempts({
  learnerId, sessionId, microId, bktUnit, dangBai, events,
  serverTs = null, now = Date.now,
}) {
  if (!learnerId || !sessionId || !microId) throw new Error('thiếu learnerId/sessionId/microId');
  const ts = now();
  /* Dạng bài của ma trận — MẢNG, vì một bài dạy được nhiều dạng (bài 9 lớp 4 dạy cả
     "dấu hiệu chia hết" lẫn "lập số chẵn - lẻ"). Rỗng thì ghi null cho gọn sổ. */
  const dang = (Array.isArray(dangBai) ? dangBai : dangBai ? [dangBai] : []).filter(Boolean);
  return events.map((e, i) => ({
    id: attemptId(learnerId, sessionId, microId, e.itemId, i),
    learnerId, sessionId, microId,
    bktUnit: e.bktUnit || bktUnit || null,
    /* `bktUnit` nói con mắc ở MICRO nào; `dangBai` nói bài ấy thuộc DẠNG nào của ma
       trận. Hai trục khác nhau: cô giáo cần trục sau mới thấy cả lớp đang yếu mảng
       kiến thức nào, thay vì một danh sách bài rời rạc. */
    dangBai: dang.length ? dang : null,
    itemId: e.itemId,
    phase: e.phase,
    correct: !!e.ok,
    tries: e.tries ?? 1,
    hintsUsed: e.hintsUsed ?? 0,
    mustPass: !!e.mustPass,
    ms: e.ms ?? null,
    /* Con TRẢ LỜI GÌ — không có trường này thì cô chỉ biết "sai", không biết sai ra sao,
       mà hai con sai hai kiểu khác nhau cần hai cách giúp khác nhau. */
    answer: e.answer === undefined ? null : goiDapAn(e.answer),
    expected: e.expected === undefined ? null : goiDapAn(e.expected),
    mode: e.mode || null,                 // so · bieuthuc · dungsai · chondapan · tuluan
    revealed: !!e.revealed,               // con chịu thua, đã xem đáp án
    /**
     * Mốc RIÊNG của từng lượt trả lời (`khiNao` do màn hình đóng ngay lúc con bấm).
     *
     * Trước đây cả loạt dùng chung một `ts` đóng lúc GỬI, nên 11 lượt của một buổi
     * học trùng y một thời điểm — "số phút con học" tính theo khoảng cách giữa các
     * mốc luôn ra 0, và dòng thời gian trong sổ dồn cục thành một điểm.
     */
    v: PHIEN_BAN_BAN_GHI,
    ts: e.khiNao ?? ts,
    // ts là giờ máy của con — con chỉnh đồng hồ máy tính bảng là lệch. serverTs do máy chủ
    // đóng dấu, dùng cho mọi thống kê mà cô giáo nhìn vào.
    serverTs,
  }));
}

/** Tóm tắt phiên để ghi vào progress/{learner}/micros/{micro} */
export function buildProgressDoc({ microId, grade, events, sessionId, serverTs = null, now = Date.now }) {
  const practice = events.filter((e) => e.phase === 'practice');
  return {
    microId,
    serverTs,
    state: grade.pass ? 'passed' : 'tried',
    pass: !!grade.pass,
    mustPassOK: !!grade.mustOK,
    score: grade.right ?? 0,
    total: grade.total ?? 0,
    practiceFirstTry: practice.filter((e) => e.ok && (e.tries ?? 1) === 1).length,
    practiceTotal: practice.length,
    sessionId,
    at: now(),
  };
}

/* ─────────── Hàng đợi ngoại tuyến ─────────── */
const QKEY = 'ttd5.queue.v1';

export function readQueue(storage = globalThis.localStorage) {
  try { return JSON.parse(storage?.getItem(QKEY) || '[]'); } catch { return []; }
}

export function writeQueue(items, storage = globalThis.localStorage) {
  try { storage?.setItem(QKEY, JSON.stringify(items)); } catch { /* bỏ qua */ }
  return items;
}

/** Đưa các bản ghi vào hàng đợi — trùng id thì ghi đè, không nhân bản */
export function enqueue(records, storage = globalThis.localStorage) {
  const q = readQueue(storage);
  const map = new Map(q.map((r) => [r.id, r]));
  for (const r of records) map.set(r.id, r);
  return writeQueue([...map.values()], storage);
}

/**
 * Đẩy hàng đợi lên máy chủ. writer(records) phải trả về Promise.
 * Thất bại (mất mạng) → GIỮ NGUYÊN hàng đợi để lần sau gửi lại.
 */
export async function flushQueue(writer, storage = globalThis.localStorage, batchSize = 200) {
  const q = readQueue(storage);
  if (q.length === 0) return { sent: 0, left: 0 };
  let sent = 0;
  try {
    for (let i = 0; i < q.length; i += batchSize) {
      const chunk = q.slice(i, i + batchSize);
      await writer(chunk);
      sent += chunk.length;
    }
  } catch {
    const left = q.slice(sent);
    writeQueue(left, storage);
    return { sent, left: left.length, error: true };
  }
  writeQueue([], storage);
  return { sent, left: 0 };
}

/**
 * Đăng nhập xong thì SANG TÊN toàn bộ hàng đợi cho tài khoản thật.
 *
 * Con học thử trước khi đăng nhập, mọi bản ghi mang mã tạm 'local'. Đẩy nguyên lên là
 * luật bảo mật từ chối (`isMine('local')` sai), mà từ chối thì im lặng — công học của
 * con bay sạch. Phải viết lại cả learnerId lẫn id (id có nhúng learnerId bên trong).
 *
 * Ghi đè theo id mới nên chạy lại nhiều lần cũng không sinh bản trùng.
 */
export function reassignQueue(uid, storage = globalThis.localStorage) {
  if (!isCloudLearner(uid)) return { moved: 0 };
  const q = readQueue(storage);
  let moved = 0;
  const out = new Map();
  for (const r of q) {
    if (r.learnerId === uid) { out.set(r.id, r); continue; }
    const seq = String(r.id).split('_').pop();
    const next = { ...r, learnerId: uid, id: attemptId(uid, r.sessionId, r.microId, r.itemId, seq) };
    out.set(next.id, next);
    moved++;
  }
  writeQueue([...out.values()], storage);
  return { moved };
}

/** Phiên học: một id cho cả lượt học một micro */
export const newSessionId = (rnd = Math.random) =>
  `s${Date.now().toString(36)}${Math.floor(rnd() * 1e6).toString(36)}`;
