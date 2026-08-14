/**
 * CHUYỂN TIẾN ĐỘ SANG SỐ BÀI MỚI CỦA LỚP 4 — chạy MỘT LẦN cho mỗi bé.
 *
 * ── VÌ SAO CẦN ──
 * 14-08-2026 cụm dãy số lớp 4 tách thành năm bài (khái niệm → thứ n → đếm → tổng →
 * thuộc dãy), nên B13 cũ lùi thành B18 và 31 bài sau đó dồn theo 5 chỗ.
 *
 * Nhưng tiến độ của bé lưu theo MÃ BÀI — `micros['DL:KSN4.B14']`. Không chuyển đổi
 * thì bé từng học xong "DÃY SỐ HAI TẦNG" (B14 cũ) mở app ra thấy mình đã qua "SỐ
 * HẠNG THỨ n" (B14 mới) — một bài chưa từng học. Huy hiệu gắn nhầm bài, sao vẫn
 * đếm đủ, và KHÔNG CÓ GÌ BÁO. Bé chỉ thấy app nhớ sai về mình.
 *
 * Bác đã biết và chấp nhận rủi ro khi chọn cách đánh số lại. Tệp này là để rủi ro
 * ấy không thành thiệt hại.
 *
 * ── ĐI TỪ SỐ LỚN XUỐNG SỐ NHỎ ──
 * B44→B49 trước, rồi B43→B48… Làm ngược lại thì B13→B18 xong, tới lượt B18 (vừa
 * mới thành) lại bị dời tiếp thành B23 — dồn hai lần. Cùng cái bẫy của
 * `tools/don_so_lop4.py`, và ở đây nó ăn vào dữ liệu THẬT của bé.
 *
 * ── CHẠY ĐÚNG MỘT LẦN ──
 * Có cờ `donSoLop4` trong chính sổ tiến độ. Chạy lần hai là dời thêm 5 chỗ nữa —
 * mã trôi ra ngoài dải bài và bé mất sạch tiến độ lớp 4. Cờ nằm TRONG sổ chứ không
 * ở một khoá localStorage riêng, để nó theo sổ lên máy chủ và về máy khác.
 *
 * ── KHÔNG ĐỤNG MÔN KHÁC ──
 * Chỉ mã bắt đầu `DL:KSN4.B`. Lớp 2, lớp 3, lớp 5, Quyển 2 và Tiếng Anh giữ nguyên.
 */

/** Dải bài phải dời, và dời bao nhiêu chỗ. Trùng với `tools/don_so_lop4.py`. */
export const DAI = { tu: 13, den: 44, dich: 5 };

/** Cờ đánh dấu ĐÃ chuyển. Đổi tên cờ là chạy lại lần nữa — đừng đổi. */
export const CO = 'donSoLop4';

const MA = /^DL:KSN4\.B(\d{2})$/;

/** Mã mới của một mã cũ. Trả về chính nó nếu không thuộc diện dời. */
export function maMoi(id) {
  const m = MA.exec(String(id || ''));
  if (!m) return id;
  const n = Number(m[1]);
  if (n < DAI.tu || n > DAI.den) return id;
  return `DL:KSN4.B${String(n + DAI.dich).padStart(2, '0')}`;
}

/**
 * Dời mọi khoá của một bảng khoá-theo-mã-bài. Đi từ số LỚN xuống — xem đầu tệp.
 *
 * Khoá đích ĐÃ CÓ SẴN thì giữ bản đang có: bé chưa chuyển đổi mà đã học bài B18
 * mới (bài kết hợp) thì bản ấy mới là thật, đừng để bản cũ đè lên.
 */
function doiBang(bang) {
  if (!bang || typeof bang !== 'object') return bang;
  const ra = { ...bang };
  for (let n = DAI.den; n >= DAI.tu; n -= 1) {
    const cu = `DL:KSN4.B${String(n).padStart(2, '0')}`;
    if (!(cu in ra)) continue;
    const moi = maMoi(cu);
    if (!(moi in ra)) ra[moi] = ra[cu];
    delete ra[cu];
  }
  return ra;
}

/**
 * Khoá chương của lớp 4 có dạng `lop4.4` (mã quyển + số chương) — KHÔNG mang mã
 * bài, nên không phải dời. Chép lại điều này ra đây vì nhìn qua rất dễ tưởng
 * ngược lại và đi dời nhầm, làm hỏng huy hiệu chương của bé.
 */
export function chuyenSo(so) {
  if (!so || typeof so !== 'object') return so;
  if (so[CO]) return so;                       // đã chuyển rồi — tuyệt đối không chạy lại
  /* CHỈ `micros`. Chỗ-con-đang-học-dở KHÔNG phải trường riêng — nó nằm ngay trong
     `micros[maBai].step`, nên dời `micros` là dời luôn cả nó. Bản đầu của tệp này
     có thêm một nhánh `so.spot`, tức là dời một trường KHÔNG TỒN TẠI: không hỏng gì,
     nhưng là mã chết, và mã chết thì người sau đọc sẽ tưởng có trường ấy thật. */
  return { ...so, micros: doiBang(so.micros), [CO]: true };
}

/** Đã chuyển chưa — để chỗ gọi biết có cần ghi lại sổ không. */
export const daChuyen = (so) => !!(so && so[CO]);
