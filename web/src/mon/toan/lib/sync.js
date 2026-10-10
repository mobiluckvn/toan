import { boNguong, nguCanhPhien } from '../../../chung/lib/nguong.js';
import { nhanNhom } from '../../../chung/lib/chiaNhom.js';
/**
 * LỚP DỮ LIỆU HỌC — dựng bản ghi attempts và hàng đợi đồng bộ.
 * Tách khỏi Firebase SDK để chạy test được bằng node (test/sync.test.mjs).
 *
 * Nguyên tắc: ghi NHẬT KÝ THÔ (mỗi lượt trả lời một dòng), không chỉ ghi điểm tổng —
 * sau này mới trả lời được "bẫy nào cả lớp hay sập nhất", "câu nào con làm lâu mà vẫn sai".
 */
import { choDangDung, CHO_DAU } from '../../../chung/lib/nguoiDung.js';

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
  /**
   * HỌC BẠ — mọi thứ KHÔNG phải "đã học xong bài nào".
   *
   * `progress/{uid}/micros` chỉ ghi từng bài. Ba thứ còn lại của sổ tiến độ —
   * kỳ sát hạch chương, bậc chủ đề đã vững, vòng đấu Mùa giải — trước nay nằm
   * NGUYÊN Ở MÁY, không bao giờ lên mạng. Nghĩa là bố mẹ mở sổ ở máy khác thì
   * mất sạch, và cô giáo thì không bao giờ thấy được con vững chủ đề nào.
   *
   * Để riêng chứ không nhét chung vào `micros`: hàm `onMicroDone` chạy trên MỌI
   * tài liệu của thư mục ấy và đọc thẳng `after.microId` — thả một bản ghi khác
   * hình dạng vào là hàm đêm ném lỗi, còn `microsPassed` thì đếm phồng lên.
   */
  hocBa: (uid) => `hocBa/${uid}/muc`,
};

/** Mã tài liệu học bạ — Firestore cấm '/' trong mã, mà mã dạng bài thì có dấu chấm. */
export const maHocBa = (loai, khoa) =>
  `${loai}_${String(khoa).replace(/[^A-Za-z0-9]+/g, '_')}`;

// ROLES · normalizeEmail · buildUserDoc dùng chung từ functions/src/user.js
export { ROLES, normalizeEmail, buildUserDoc } from '../../../../functions/src/user.js';


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
/* 4 từ 10-10-2026: thêm `khoiLop` — nấc phạm vi của bộ ngưỡng (R7, mục 3.8.1).
   Dòng v ≤ 3 không có trường ấy, và máy chủ đã chấm chúng bằng bộ `toanHe`.
   6 từ 10-10-2026 (tối): Tiếng Anh thêm `bac` và `sauPhuDao`. Toán KHÔNG có hai
   trường ấy (câu Toán không khai bậc, và Toán chưa có phụ đạo) — nhưng hai môn phải
   khai CÙNG một số phiên bản, nếu không bên đọc nhật ký phải nhớ hai luật.
   5 từ 10-10-2026 (chiều): bản ghi Toán thêm `mon`. Trước đó Toán KHÔNG khai môn,
   nên 3075/3212 dòng nhật ký rơi ngoài mọi phép gom theo môn — xem chú thích ở
   chỗ ghi trường ấy. Hai môn vẫn phải khai CÙNG một số. */
export const PHIEN_BAN_BAN_GHI = 6;

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
    /* ── PHIÊN BẢN BỘ NGƯỠNG (R7, mục 3.8.2) ──
       Từ 10-10-2026 hai môn dùng CHUNG một bộ ngưỡng (θ ở `NG07`), nên bản ghi của
       Toán cũng phải mang số phiên bản — thiếu nó thì một mức thạo cũ không còn
       biết được tính bằng θ nào, và hai bộ ngưỡng không so được trên cùng nhật ký. */
    nguongVer: boNguong()?.phienBan ?? null,
    /* ── MÔN — nấc `mon` của thang phạm vi (R7 · mục 3.8.1) ──
       ⚠ TOÁN CHƯA BAO GIỜ KHAI TRƯỜNG NÀY. Soi máy chủ bằng khoá quản trị thấy
       3075/3212 lượt trong nhật ký không có `mon` — tức mọi phép thống kê theo môn
       đang bỏ qua 96% dữ liệu, mà bảng vẫn hiện ra một con số trông bình thường
       cho riêng Tiếng Anh. Trước R7 điều đó vô hại vì chỉ có một bộ ngưỡng; từ khi
       có nấc `mon` thì nó là một lỗ thủng câm.

       Hằng chuỗi chứ không đọc từ ngữ cảnh phiên: tệp này CHỈ Toán dùng, và một
       lượt Toán thì là Toán kể cả khi ngữ cảnh phiên chưa kịp đặt. */
    mon: 'toan',
    /* ── NHÃN CHIA NHÓM (KB4 · KB5, mục 3.9) ──
       `null` khi mọi thử nghiệm đang tắt — tức hiện nay. Ghi cả nhãn của thử nghiệm
       đã tắt thì sáu tháng sau không ai biết nhãn ấy có hiệu lực trong khoảng nào. */
    nhomThuNghiem: nhanNhom(learnerId),
    /* ── KHỐI LỚP (R7 · mục 3.8.1, nấc `khoiLop` của thang phạm vi) ──
       Để hàm nền chấm lượt này bằng đúng bộ tham số của khối lớp ấy. KHAI THẲNG
       từ ngữ cảnh phiên, chứ KHÔNG để máy chủ suy từ hình dạng mã nút (`v_g5_…`):
       mã nút là chuỗi do bộ sinh nội dung đặt, đổi quy ước đặt tên một lần là mọi
       lượt im lặng rơi về bộ `toanHe` mà không gì kêu. Thiếu thì `null` — máy chủ
       lùi về `toanHe`, đúng hành vi trước R7.
       ⚠ Luật Firestore dùng `hasAll` nên trường thêm không bị chặn; nhưng nhật ký
       là BẤT BIẾN, nên dòng cũ mãi mãi không có trường này. Vì vậy `v` lên 4. */
    khoiLop: nguCanhPhien()?.khoiLop ?? null,
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

/** Tóm tắt phiên để ghi vào progress/{learner}/micros/{micro}
 *
 * `gio` là sổ đồng hồ do `LessonPlayer` chốt (xem `lib/dongHo.js`). Ba con số giây
 * ghi ở đây là của LƯỢT HỌC VỪA RỒI, không cộng dồn — tài liệu này bị ghi đè mỗi lần
 * con học lại bài. Muốn cộng dồn thì đó là việc của sổ giờ theo NGÀY, và nó nằm ở
 * `hocBa/{uid}/muc` với `loai='gio'`; hai nơi trả lời hai câu khác nhau:
 *   · ở đây      — "bài NÀY con mất bao lâu" (so được giữa các bài, tìm bài con tắc)
 *   · sổ theo ngày — "hôm nay con học bao lâu" (số bố mẹ và cô giáo nhìn)
 */
export function buildProgressDoc({ microId, grade, events, sessionId, gio = null,
                                  serverTs = null, now = Date.now }) {
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
    /* Không có đồng hồ (bản cũ, hoặc màn khác gọi vào) thì để null chứ ĐỪNG để 0:
       0 giây là một lời khẳng định sai, null là "chưa đo được". Sổ và bảng cô giáo
       đều phân biệt hai thứ ấy — thà nói chưa có số còn hơn hiện số sai. */
    giay: gio ? gio.giay : null,
    giayXem: gio ? gio.giayXem : null,
    giayLam: gio ? gio.giayLam : null,
    sessionId,
    at: now(),
  };
}

/* ─────────── Hàng đợi ngoại tuyến ─────────── */
/**
 * Hàng đợi cũng phải RIÊNG TỪNG BÉ, cùng lý do với sổ tiến độ.
 *
 * Nguy hơn sổ tiến độ một bậc: `reassignQueue` sang tên CẢ hàng đợi cho tài khoản vừa
 * đăng nhập. Dùng chung một hàng thì em đăng nhập là bài anh vừa làm bị gán sang tên
 * em — nhật ký sai người, mà nhật ký thì BẤT BIẾN, ghi lên máy chủ rồi không sửa được.
 *
 * Chỗ đầu giữ khoá cũ để máy đang dùng không mất những bản ghi còn nằm chờ.
 */
const QKEY_GOC = 'ttd5.queue.v1';
const qkey = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? QKEY_GOC : `${QKEY_GOC}.${cho}`;
};

/**
 * SỔ "ĐÃ LÊN MÁY CHỦ RỒI" — cùng một cái bẫy với môn Tiếng Anh, xem chú thích dài
 * ở `mon/tienganh/lib/suKien.js`. Tóm tắt:
 *
 *   `attempts` là nhật ký BẤT BIẾN (`allow update, delete: if false`), mà mỗi lượt
 *   màn hình lại dựng LẠI bản ghi của cả phiên rồi gửi. Bản ghi nào đã lên máy chủ
 *   thì lệnh gửi lại là `update` → bị từ chối; `writeBatch` nguyên khối nên CẢ LÔ
 *   rơi. Hễ một lượt lọt sớm là mọi lượt sau của phiên ấy mất vĩnh viễn.
 *
 * ── VÌ SAO MÔN TOÁN CHƯA MẤT DỮ LIỆU, VÀ VÌ SAO VẪN PHẢI VÁ ──
 * Soi máy chủ 23-08-2026: 43/43 phiên Toán còn đủ lượt. Nhưng soi kỹ hơn thì MỌI
 * bản ghi của một phiên mang ĐÚNG MỘT dấu `serverTs` — tức cả phiên lên bằng một
 * lô duy nhất, và những lần đẩy giữa chừng đều đã hỏng sẵn. Toán sống được nhờ
 * MAY: chưa lần nào có lô nào lọt sớm. Đổi nhịp mạng, đổi thời điểm đăng nhập, hay
 * một lần đẩy lọt là mất cả phiên — mà mất thì không có gì kêu.
 */
const DA_GUI_GOC = 'ttd5.daGui.v1';
const dgkey = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? DA_GUI_GOC : `${DA_GUI_GOC}.${cho}`;
};

/** Giữ tối đa bằng này mã; vượt thì bỏ mã CŨ NHẤT (thuộc phiên đã đóng). */
export const DA_GUI_TOI_DA = 3000;

export function readSent(storage = globalThis.localStorage) {
  try { return new Set(JSON.parse(storage?.getItem(dgkey()) || '[]')); } catch { return new Set(); }
}

export function markSent(ids, storage = globalThis.localStorage) {
  if (!ids?.length) return readSent(storage);
  let ds;
  try { ds = JSON.parse(storage?.getItem(dgkey()) || '[]'); } catch { ds = []; }
  const co = new Set(ds);
  for (const id of ids) if (!co.has(id)) { ds.push(id); co.add(id); }
  if (ds.length > DA_GUI_TOI_DA) ds = ds.slice(ds.length - DA_GUI_TOI_DA);
  try { storage?.setItem(dgkey(), JSON.stringify(ds)); } catch { /* bỏ qua */ }
  return new Set(ds);
}

export function readQueue(storage = globalThis.localStorage) {
  try { return JSON.parse(storage?.getItem(qkey()) || '[]'); } catch { return []; }
}

export function writeQueue(items, storage = globalThis.localStorage) {
  try { storage?.setItem(qkey(), JSON.stringify(items)); } catch { /* bỏ qua */ }
  return items;
}

/** Đưa các bản ghi vào hàng đợi — trùng id thì ghi đè, không nhân bản */
export function enqueue(records, storage = globalThis.localStorage) {
  /* ⚠ BỎ HẲN mã đã lên máy chủ — xem `DA_GUI_GOC` ở trên. Lọc ở đây chứ không ở
     chỗ gửi: chỗ gửi lọc thì mã cũ vẫn nằm lại hàng đợi và phình mãi. */
  const daGui = readSent(storage);
  const q = readQueue(storage);
  const map = new Map(q.filter((r) => !daGui.has(r.id)).map((r) => [r.id, r]));
  for (const r of records) if (!daGui.has(r.id)) map.set(r.id, r);
  return writeQueue([...map.values()], storage);
}

/** Mã lỗi Firestore trả khi luật từ chối — phân biệt với mất mạng (`unavailable`). */
const LOI_TU_CHOI = 'permission-denied';

/**
 * Đẩy hàng đợi lên máy chủ. writer(records) phải trả về Promise.
 * Mất mạng → GIỮ NGUYÊN hàng đợi để lần sau gửi lại.
 *
 * ── LÔ HỎNG THÌ THỬ LẺ, ĐỂ GỠ ĐỘC CHO HÀNG ĐỢI CŨ ──
 * Xem chú thích dài ở `mon/tienganh/lib/suKien.js`. Tóm tắt: `attempts` bất biến,
 * nên một bản ghi đã lên máy chủ mà còn nằm trong hàng đợi sẽ làm CẢ LÔ bị từ
 * chối, mãi mãi. Thử lẻ thì tách được bản ghi hỏng ra khỏi những bản ghi lành.
 *
 * ⚠ Phân biệt "luật từ chối" với "mất mạng" bằng MÃ LỖI. Cứ hỏng là bỏ thì mất
 *    mạng đồng nghĩa mất trắng công học của con.
 */
export async function flushQueue(writer, storage = globalThis.localStorage, batchSize = 200) {
  const q = readQueue(storage);
  if (q.length === 0) return { sent: 0, left: 0 };
  let sent = 0; let skipped = 0;
  const xong = new Set();
  let matMang = false;

  for (let i = 0; i < q.length && !matMang; i += batchSize) {
    const chunk = q.slice(i, i + batchSize);
    try {
      await writer(chunk);
      chunk.forEach((r) => xong.add(r.id));
      markSent(chunk.map((r) => r.id), storage);
      sent += chunk.length;
    } catch {
      for (const r of chunk) {
        try {
          await writer([r]);
          markSent([r.id], storage);
          xong.add(r.id);
          sent += 1;
        } catch (e) {
          if (e?.code === LOI_TU_CHOI) {
            markSent([r.id], storage);
            xong.add(r.id);
            skipped += 1;
          } else { matMang = true; break; }
        }
      }
    }
  }

  const left = matMang ? q.filter((r) => !xong.has(r.id)) : [];
  writeQueue(left, storage);
  return { sent, skipped, left: left.length, ...(matMang ? { error: true } : {}) };
}

/**
 * Đăng nhập xong thì NHẬN VỀ những bản ghi học thử — và CHỈ những bản ghi ấy.
 *
 * Con học thử trước khi đăng nhập, mọi bản ghi mang mã tạm 'local'. Đẩy nguyên lên là
 * luật bảo mật từ chối (`isMine('local')` sai), mà từ chối thì im lặng — công học của
 * con bay sạch. Phải viết lại cả learnerId lẫn id (id có nhúng learnerId bên trong).
 *
 * ── ⚠ TUYỆT ĐỐI KHÔNG NHẬN BẢN GHI CỦA MỘT BÉ THẬT KHÁC ──
 * Bản cũ viết `if (r.learnerId === uid) giữ; else sang tên` — tức nó sang tên MỌI
 * bản ghi lạ, kể cả bản ghi của một bé CÓ THẬT khác. Ghép với lỗi hàng đợi nghẽn
 * (xem `DA_GUI_GOC`), cảnh sau đã xảy ra THẬT và đo được trên máy chủ 23-08-2026:
 *
 *   bé A học trên một chỗ → đúng 1 lượt lên được, phần còn lại kẹt trong hàng đợi;
 *   ít ngày sau bé B đăng nhập vào CHÍNH chỗ ấy → hàm này sang tên cả xấp của A
 *   thành của B → bài của A được ghi vào học bạ của B.
 *
 * Đo được 7 phiên như thế, 130/398 bản ghi mang tên sai chủ. Hỏng cả hai đầu: B
 * được cộng công không phải của mình, A mất trắng buổi học — và mô hình người học
 * của cả hai đều sai.
 *
 * Nên nay chỉ nhận bản ghi CHƯA CÓ CHỦ (`local`). Bản ghi của bé thật khác thì bỏ
 * khỏi hàng đợi và ĐẾM vào `boLai`: chúng không gửi lên được (luật đòi `isMine`),
 * mà giữ lại thì chặn đường cả lô. Bỏ trong im lặng mới là điều không được làm.
 */
export function reassignQueue(uid, storage = globalThis.localStorage) {
  if (!isCloudLearner(uid)) return { moved: 0, boLai: 0 };
  const q = readQueue(storage);
  let moved = 0; let boLai = 0;
  const out = new Map();
  for (const r of q) {
    if (r.learnerId === uid) { out.set(r.id, r); continue; }
    if (isCloudLearner(r.learnerId)) { boLai += 1; continue; }   // của bé THẬT khác
    const seq = String(r.id).split('_').pop();
    const next = { ...r, learnerId: uid, id: attemptId(uid, r.sessionId, r.microId, r.itemId, seq) };
    out.set(next.id, next);
    moved++;
  }
  writeQueue([...out.values()], storage);
  return { moved, boLai };
}

/** Phiên học: một id cho cả lượt học một micro */
export const newSessionId = (rnd = Math.random) =>
  `s${Date.now().toString(36)}${Math.floor(rnd() * 1e6).toString(36)}`;
