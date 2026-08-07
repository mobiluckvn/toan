/**
 * ĐĂNG NHẬP BẰNG MÃ OTP GỬI QUA EMAIL — phần logic thuần, không đụng Firestore.
 * Có test chạy bằng node (test/otp.test.mjs).
 *
 * Bốn nguyên tắc, mỗi cái vá một đường tấn công thật:
 *   1. KHÔNG lưu mã — chỉ lưu bản băm. Rò cơ sở dữ liệu cũng không ai đăng nhập hộ được.
 *   2. Đếm số lần nhập sai — 5 lần là huỷ mã. Không thì 6 chữ số chỉ là một triệu lần thử.
 *   3. Chặn spam gửi mã — không thì hộp thư người ta bị dội, mà tiền gửi mail mình chịu.
 *   4. Trả lời GIỐNG HỆT NHAU dù email có trong hệ thống hay không — không thì kẻ xấu
 *      dò được ai đang dùng app.
 */
import { createHash, randomInt, timingSafeEqual } from 'node:crypto';

export const CODE_DIGITS = 6;
export const TTL_MS = 10 * 60 * 1000;        // mã sống 10 phút
export const MAX_WRONG = 5;                  // nhập sai quá số này là huỷ mã
export const RESEND_COOLDOWN_MS = 60 * 1000; // gửi lại sớm nhất sau 60 giây
export const MAX_PER_HOUR = 5;               // tối đa 5 mã mỗi email mỗi giờ

/** Mã 6 chữ số, sinh bằng nguồn ngẫu nhiên MẬT MÃ (không dùng Math.random) */
export function makeCode(rand = randomInt) {
  return String(rand(0, 10 ** CODE_DIGITS)).padStart(CODE_DIGITS, '0');
}

/**
 * Băm mã kèm email và một chuỗi bí mật của máy chủ.
 * Kèm email để mã của người này không dùng được cho người kia; kèm pepper để kẻ
 * đọc trộm cơ sở dữ liệu không dựng nổi bảng tra sẵn cho vỏn vẹn một triệu mã.
 */
export function hashCode(email, code, pepper = '') {
  return createHash('sha256').update(`${email}|${code}|${pepper}`).digest('hex');
}

/** So hai chuỗi băm theo thời gian HẰNG ĐỊNH — so bằng === là lộ dần từng ký tự */
export function safeEqual(a, b) {
  const x = Buffer.from(String(a ?? ''), 'utf8');
  const y = Buffer.from(String(b ?? ''), 'utf8');
  return x.length === y.length && timingSafeEqual(x, y);
}

/**
 * Có được phép gửi mã mới không?
 * rec: bản ghi hiện có của email đó (hoặc null)
 * @returns {{ok:true} | {ok:false, reason:'quá nhanh'|'quá nhiều', retryAfterMs:number}}
 */
export function canSend(rec, now = Date.now()) {
  if (!rec) return { ok: true };

  const since = now - (rec.sentAt ?? 0);
  if (since < RESEND_COOLDOWN_MS) {
    return { ok: false, reason: 'quá nhanh', retryAfterMs: RESEND_COOLDOWN_MS - since };
  }
  // cửa sổ trượt một giờ
  const window = (rec.sentTimes || []).filter((t) => now - t < 3600_000);
  if (window.length >= MAX_PER_HOUR) {
    return { ok: false, reason: 'quá nhiều', retryAfterMs: 3600_000 - (now - window[0]) };
  }
  return { ok: true };
}

/** Bản ghi mới để lưu sau khi gửi mã */
export function nextRecord(rec, { email, code, pepper = '', now = Date.now() }) {
  const window = (rec?.sentTimes || []).filter((t) => now - t < 3600_000);
  return {
    email,
    hash: hashCode(email, code, pepper),
    expiresAt: now + TTL_MS,
    wrong: 0,
    sentAt: now,
    sentTimes: [...window, now],
  };
}

/**
 * Kiểm mã người dùng nhập.
 * @returns {{ok:true} | {ok:false, reason:string, wrong?:number, burn:boolean}}
 *          burn=true nghĩa là phải XOÁ bản ghi (hết hạn, hết lượt, hoặc đã dùng xong)
 */
export function verify(rec, { email, code, pepper = '', now = Date.now() }) {
  if (!rec) return { ok: false, reason: 'chưa yêu cầu mã nào', burn: false };
  if (now > (rec.expiresAt ?? 0)) return { ok: false, reason: 'mã đã hết hạn', burn: true };
  if ((rec.wrong ?? 0) >= MAX_WRONG) return { ok: false, reason: 'nhập sai quá nhiều lần', burn: true };

  if (!safeEqual(rec.hash, hashCode(email, String(code ?? '').trim(), pepper))) {
    const wrong = (rec.wrong ?? 0) + 1;
    return {
      ok: false,
      reason: wrong >= MAX_WRONG ? 'nhập sai quá nhiều lần' : 'mã không đúng',
      wrong,
      burn: wrong >= MAX_WRONG,           // hết lượt thì huỷ luôn, bắt xin mã mới
    };
  }
  return { ok: true, burn: true };         // dùng xong là huỷ — mỗi mã chỉ vào được MỘT lần
}

/** Nội dung email — ngắn, không kèm liên kết nào để khỏi tập cho phụ huynh thói bấm bừa */
export function otpEmail(code, appName = 'Toán Tư Duy lớp 5') {
  const mins = Math.round(TTL_MS / 60000);
  return {
    subject: `${code} là mã đăng nhập ${appName}`,
    text: [
      `Mã đăng nhập của bạn: ${code}`,
      ``,
      `Mã có hiệu lực ${mins} phút và chỉ dùng được một lần.`,
      `Nhập mã vào màn hình đang mở sẵn trên máy của bạn.`,
      ``,
      `Không phải bạn yêu cầu? Bỏ qua thư này — chưa ai vào được tài khoản.`,
      `Đừng đọc mã này cho bất kỳ ai, kể cả người tự xưng là nhân viên hỗ trợ.`,
    ].join('\n'),
  };
}
