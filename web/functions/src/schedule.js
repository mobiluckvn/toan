/**
 * HÀNG ĐỢI ÔN TẬP — dựng từ spacedReview.schedule có sẵn trong mỗi micro.
 * Chuỗi dạng: "+1 ngày: flashcard" · "+3 ngày: câu generator P1" · "+7 ngày: câu P3 (bộ ba)"
 */
const DAY = 24 * 60 * 60 * 1000;

/** "+3 ngày: câu generator P1" → {days: 3, what: 'câu generator P1'} */
export function parseSchedule(line) {
  const m = String(line).match(/\+\s*(\d+)\s*ngày\s*:?\s*(.*)$/i);
  return m ? { days: Number(m[1]), what: m[2].trim() } : null;
}

/** Toàn bộ lịch của một micro → danh sách mốc ngày */
export function scheduleOf(lesson) {
  return (lesson?.spacedReview?.schedule || [])
    .map(parseSchedule)
    .filter(Boolean)
    .sort((a, b) => a.days - b.days);
}

/**
 * Tạo thẻ ôn khi con vừa học xong một micro.
 * Box (Leitner) bắt đầu 0; mỗi mốc trong lịch là một thẻ.
 */
/**
 * Các nút tri thức của một bài — gắn vào thẻ ôn lúc tạo.
 *
 * ⚠ VÌ SAO GẮN VÀO THẺ CHỨ KHÔNG TRA LÚC ÔN: máy con chỉ tải nội dung của bài ĐANG
 * mở, nên lúc bày danh sách thẻ nó không biết nút của những bài kia. Hàm nền thì có
 * sẵn cả bài trong tay. Gắn một lần lúc tạo là chỗ rẻ nhất.
 *
 * Thẻ cũ không có trường này — chúng chỉ không được xét vượt ải, tức giữ nguyên
 * hành vi cũ. Fail-closed: thiếu dữ liệu thì bé cứ ôn, không ai bị bỏ sót bài.
 */
export function nutCuaBai(lesson) {
  const ra = new Set();
  const hang = [lesson];
  while (hang.length) {
    const y = hang.pop();
    if (Array.isArray(y)) { hang.push(...y); continue; }
    if (!y || typeof y !== 'object') continue;
    if (y.maNut) ra.add(String(y.maNut));
    for (const m of (y.maNutDs || [])) if (m) ra.add(String(m));
    for (const v of Object.values(y)) if (v && typeof v === 'object') hang.push(v);
  }
  return [...ra];
}

export function buildReviewCards({ learnerId, microId, lesson, at = Date.now() }) {
  const maNutDs = nutCuaBai(lesson);
  return scheduleOf(lesson).map((s, i) => ({
    id: `${microId.replace('DL:KSN5Q1.', '')}_r${i}`,
    learnerId, microId,
    kind: /flashcard/i.test(s.what) ? 'flashcard' : 'item',
    what: s.what,
    box: 0,
    dueAt: at + s.days * DAY,
    createdAt: at,
    /* Nút của bài — để máy con hỏi được hàm chính sách "bài này bé đã vững chưa"
       mà không phải tải lại nội dung bài. */
    maNutDs,
  }));
}

/** Thẻ đến hạn — lấy tối đa n thẻ, ưu tiên quá hạn lâu nhất */
export function dueCards(cards, now = Date.now(), n = 3) {
  return cards.filter((c) => c.dueAt <= now).sort((a, b) => a.dueAt - b.dueAt).slice(0, n);
}

/**
 * Sau khi ôn một thẻ: đúng thì lên hộp (giãn ra), sai thì về hộp 0 (ôn lại sớm).
 * Khoảng cách theo hộp: 1 · 3 · 7 · 14 · 30 ngày.
 */
export const BOX_DAYS = [1, 3, 7, 14, 30];
export function reviewCard(card, ok, now = Date.now()) {
  const box = ok ? Math.min((card.box ?? 0) + 1, BOX_DAYS.length - 1) : 0;
  return { ...card, box, lastResult: !!ok, reviewedAt: now, dueAt: now + BOX_DAYS[box] * DAY };
}

/** Bao nhiêu thẻ đang quá hạn — dùng cho huy hiệu nhắc nhở ở trang chính */
export const overdueCount = (cards, now = Date.now()) => cards.filter((c) => c.dueAt <= now).length;
