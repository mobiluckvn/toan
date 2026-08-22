/**
 * BKT — Bayesian Knowledge Tracing (thuần toán, không phụ thuộc Firebase).
 *
 * Bốn tham số:
 *   L0    xác suất đã thạo từ trước khi học
 *   T     xác suất học được sau mỗi lần luyện (transit)
 *   slip  đã thạo nhưng vẫn trả lời sai (sẩy tay)
 *   guess chưa thạo nhưng đoán trúng
 */
/* Hiệu chỉnh bằng thực nghiệm (xem test/bkt.test.mjs):
   cần ~4 câu đúng liên tiếp mới đạt thạo, và MỘT câu sai sau đó kéo tụt dưới ngưỡng.
   Tham số cũ (L0 .25 · guess .20) tuyên thạo chỉ sau 2 câu — quá dễ dãi với trẻ. */
export const DEFAULT_PARAMS = { L0: 0.10, T: 0.08, slip: 0.10, guess: 0.30 };
export const MASTERY_THRESHOLD = 0.85;

/** Một lần trả lời → cập nhật xác suất thạo */
export function bktUpdate(p, correct, params = DEFAULT_PARAMS) {
  const { T, slip, guess } = { ...DEFAULT_PARAMS, ...params };
  const prior = clamp(p);
  const post = correct
    ? (prior * (1 - slip)) / (prior * (1 - slip) + (1 - prior) * guess)
    : (prior * slip) / (prior * slip + (1 - prior) * (1 - guess));
  return clamp(post + (1 - post) * T);
}

const clamp = (x) => (Number.isFinite(x) ? Math.min(0.999, Math.max(0.001, x)) : DEFAULT_PARAMS.L0);

/** Chạy cả chuỗi trả lời */
export function bktSequence(answers, params = DEFAULT_PARAMS, start = null) {
  let p = start ?? (params.L0 ?? DEFAULT_PARAMS.L0);
  for (const ok of answers) p = bktUpdate(p, ok, params);
  return p;
}

export const isMastered = (p, th = MASTERY_THRESHOLD) => p >= th;

/**
 * Câu BẮT BUỘC ĐÚNG (bẫy) đáng tin hơn câu thường: trả lời đúng nhờ đoán khó hơn.
 * → giảm guess, tăng trọng số. Sai câu bẫy thì kéo mức thạo xuống mạnh hơn.
 */
export function paramsFor(item = {}) {
  return item.mustPass
    ? { ...DEFAULT_PARAMS, guess: 0.15, slip: 0.06 }
    : DEFAULT_PARAMS;
}

/**
 * Cập nhật một bản ghi mastery từ một attempt.
 * doc: {p, nAttempts, nCorrect, lastSeen, saiLienTiep, pTruoc} | undefined
 *
 * ── `saiLienTiep` — SỐ LẦN SAI LIÊN TIẾP TẠI NÚT NÀY ──
 * Khác hẳn `nAttempts`, và khác hẳn `attempts` trong sổ tiến độ (đếm số lần làm
 * CẢ BÀI). Đây là `struggle_count` của mục 2.3.1 luận văn: bé sai mấy lần LIỀN
 * NHAU ở đúng nút này. Ba lần liền là dấu hiệu bé không tự thoát ra được — hai
 * đại lượng kia không nói ra điều đó, vì bé sai 3 lần rồi đúng 10 lần thì
 * `nCorrect/nAttempts` trông vẫn đẹp.
 *
 * Đúng MỘT lần là về 0. Cố ý: cái cần đo là "đang bí", không phải "từng bí".
 *
 * ── `pTruoc`/`p` — MỨC THẠO TRƯỚC VÀ SAU LƯỢT NÀY ──
 * Mục 2.5.2 đòi lưu P(L) trước và sau mỗi lượt để tính ΔC. Giá trị `pTruoc` đã
 * nằm sẵn trong tay ở dòng `cur` — trước nay chỉ là không ai ghi nó ra.
 *
 * ⚠ TỆP NÀY DÙNG CHUNG VỚI MÔN TOÁN ĐANG CHẠY THẬT. Ba trường thêm vào đều là
 * trường MỚI, không đổi `p` · `mastered` · `nAttempts` · `nCorrect` — nên số cũ
 * của bé không xê dịch. Cổng `bkt.test.mjs` canh chính điều đó.
 */
export function applyAttempt(doc, attempt, now = Date.now) {
  const cur = doc?.p ?? DEFAULT_PARAMS.L0;
  const dung = !!attempt.correct;
  const p = bktUpdate(cur, dung, paramsFor(attempt));
  const n = (doc?.nAttempts ?? 0) + 1;

  /* ── RT_avg và H_req — GỘP DẦN, không giữ cả dãy ──
     Mục 2.3.1 khai hai trường này ngay trong hồ sơ người học. Số thô từng lượt
     thì `attempts` đã có, nhưng bắt mọi chỗ đọc phải quét cả nghìn dòng rồi tự
     cộng là vừa chậm vừa dễ mỗi nơi cộng một kiểu.

     Cộng dồn bằng TỔNG chứ không nhân trung bình cũ với n: `(cũ*(n-1)+mới)/n`
     trôi số dần sau vài trăm lượt, mà tài liệu này sống suốt đời học của bé.

     ⚠ `ms` có thể thiếu (bản ghi đời cũ, hoặc màn chưa bấm giờ). Thiếu thì KHÔNG
     tính vào mẫu — chứ không coi là 0. Coi là 0 thì mỗi dòng thiếu kéo trung bình
     xuống, và "bé trả lời nhanh dần" thành một kết luận do lỗi ghi sinh ra. */
  const coMs = Number.isFinite(attempt.ms);
  const msTong = (doc?.msTong ?? 0) + (coMs ? attempt.ms : 0);
  const msDem = (doc?.msDem ?? 0) + (coMs ? 1 : 0);
  const goiTong = (doc?.goiTong ?? 0) + (Number(attempt.hintsUsed) || 0);

  return {
    p,
    /* Mức thạo TRƯỚC lượt này. Lần đầu chạm nút thì là L0 — vẫn ghi ra, để phép
       trừ `p - pTruoc` lúc nào cũng có nghĩa mà không phải xử lý trường hợp riêng. */
    pTruoc: cur,
    mastered: isMastered(p),
    nAttempts: n,
    nCorrect: (doc?.nCorrect ?? 0) + (dung ? 1 : 0),
    saiLienTiep: dung ? 0 : (doc?.saiLienTiep ?? 0) + 1,
    msTong,
    msDem,
    /* RT_avg. `null` khi chưa có lượt nào đo được — thà nói "chưa có số liệu" còn
       hơn hiện một con số 0 cho bố mẹ tin theo. */
    msTrungBinh: msDem ? Math.round(msTong / msDem) : null,
    goiTong,
    /* H_req — số gợi ý trung bình mỗi lượt tại nút này. */
    goiTrungBinh: n ? +(goiTong / n).toFixed(2) : 0,
    lastMicroId: attempt.microId ?? doc?.lastMicroId ?? null,
    lastSeen: now(),
  };
}
