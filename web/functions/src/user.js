/**
 * HỒ SƠ NGƯỜI DÙNG — NGUỒN DUY NHẤT, dùng chung cho cả Cloud Functions lẫn app.
 * Đặt ở functions/ vì máy chủ mới là nơi có thẩm quyền đặt vai trò; app chỉ đọc lại
 * để hiển thị. Có hai bản chép là sớm muộn cũng lệch nhau.
 */

export const ROLES = ['learner', 'teacher', 'admin'];

/** Chuẩn hoá email: bỏ khoảng trắng, về chữ thường. Sai định dạng → null. */
export function normalizeEmail(s) {
  const e = String(s ?? '').trim().toLowerCase();
  return /^[^\s@]+@[^\s@.]+\.[^\s@]{2,}$/.test(e) ? e : null;
}

/**
 * Một tài khoản là một học sinh — phụ huynh và con dùng chung.
 * Vai trò do MÁY CHỦ đặt, không bao giờ nhận từ máy con: nếu không thì ai cũng tự
 * phong mình làm giáo viên rồi đọc kết quả của cả trường.
 */
export function buildUserDoc({ uid, email, displayName = '', grade = 5, role = 'learner', now = Date.now }) {
  if (!uid) throw new Error('thiếu uid');
  const mail = normalizeEmail(email);
  if (!mail) throw new Error('email không hợp lệ');
  if (!ROLES.includes(role)) throw new Error('vai trò lạ: ' + role);
  const name = String(displayName || '').trim();
  return {
    uid, email: mail, role, grade,
    // Tên tạm lấy phần trước @ để chỗ nào cũng có cái mà hiện.
    displayName: name || mail.split('@')[0],
    /**
     * Cờ RIÊNG cho biết đã hỏi tên con chưa.
     * Không suy từ displayName được: máy chủ luôn điền sẵn tên tạm nên trường đó
     * không bao giờ trống, và màn "Con tên là gì nhỉ?" sẽ không bao giờ hiện ra.
     */
    profileComplete: !!name,
    createdAt: now(),
    lastStudiedAt: null,
  };
}
