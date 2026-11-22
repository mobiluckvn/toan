/**
 * HỌC SINH MÔ PHỎNG — tách khỏi số liệu thật.
 *
 * Thêm 22-11-2026 cho phần thực nghiệm của luận văn: 30 học sinh ẢO sinh bằng
 * `tools/mo_phong/hoc_sinh_ao.mjs`, sống CHUNG dự án với học sinh thật. Mọi tài
 * liệu của các em mang `moPhong: true` (hồ sơ, nhật ký, mức thạo, tiến độ).
 *
 * ⚠ HAI CHỖ GOM SỐ LIỆU TOÀN HỆ PHẢI LOẠI CÁC EM RA:
 *   thống kê ngưỡng · học ngưỡng     — θ đề xuất phải học từ trẻ thật, không phải
 *                                      từ chính mô hình sinh ra dữ liệu ảo.
 * Bảng xếp hạng và bảng giáo viên thì CÓ em ảo, tên như mọi em (chốt 22-11-2026:
 * mọi tài khoản hiện có đều do tác giả tạo; cô cần mở từng em để xem biểu đồ).
 * Sổ học RIÊNG của từng em ảo thì vẫn dựng: nó chỉ nói về em ấy.
 *
 * Lọc theo HAI tầng, vì một tầng không đủ:
 *   · `a.moPhong` trên từng lượt — lượt sinh bằng script;
 *   · uid nằm trong danh sách em ảo — lượt em ảo làm TRỰC TIẾP trên app (buổi học
 *     quay lại cho hội đồng xem). App không biết em là ảo nên không gắn cờ lượt.
 */
export const laAo = (d) => d?.moPhong === true;

/** Tập uid học sinh ảo. Một lượt đọc có lọc — không quét cả `users`. */
export async function dsHocSinhAo(db) {
  const snap = await db.collection('users').where('moPhong', '==', true).get();
  return new Set(snap.docs.map((d) => d.id));
}

/** Lượt này có phải của học sinh ảo không. */
export const luotAo = (a, ao) => laAo(a) || (!!a?.learnerId && ao.has(a.learnerId));
