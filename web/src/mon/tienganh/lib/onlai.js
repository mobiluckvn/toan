/**
 * ÔN LẠI — chọn câu cho một thẻ ôn đến hạn.
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Hàm nền đã sinh thẻ ôn theo lịch +1 / +3 / +7 ngày từ lâu, và luật Firestore
 * cũng đã cho máy con đọc `reviewQueue`. Nhưng soi cả kho ngày 22-08-2026 thì
 * KHÔNG mã nào đọc thư mục ấy — kể cả môn Toán. Thẻ sinh ra rồi nằm đó suốt, và
 * "lặp lại ngắt quãng" mới xong nửa đường ống: có lịch, không có buổi ôn.
 *
 * Tệp này là nửa còn lại, phần TÍNH TOÁN. Nó không đụng Firebase và không đụng
 * React, nên cổng chạy được bằng node.
 *
 * ── MỘT THẺ LÀ MỘT BÀI, KHÔNG PHẢI MỘT CÂU ──
 * Thẻ chỉ mang `microId` và `kind`. Câu thì lấy từ chính bài ấy — không sinh mới,
 * không soạn thêm. Ôn tập mà hỏi câu bé chưa từng gặp thì đó là bài mới đội lốt.
 */

/**
 * KHOẢNG CÁCH THEO HỘP LEITNER — 1 · 3 · 7 · 14 · 30 ngày.
 *
 * ⚠ CHÉP TỪ `functions/src/schedule.js` (`BOX_DAYS`), CỐ Ý KHÔNG IMPORT.
 * `functions/` là mã máy chủ; kéo nó vào gói trình duyệt là mang theo cả
 * `firebase-admin`. Cái giá của việc chép là hai bản trôi xa nhau — nên cổng
 * `tienganh_onlai.test.mjs` đọc CẢ HAI tệp rồi so, và nó đỏ nếu ai sửa một bên.
 */
export const BOX_NGAY = [1, 3, 7, 14, 30];

/**
 * Đẩy hộp sau một lượt ôn: đúng thì giãn ra, sai thì VỀ HỘP 0.
 *
 * Về hộp 0 chứ không lùi một nấc: thẻ bé vừa quên thì phải gặp lại NGÀY MAI, chứ
 * lùi từ hộp 4 xuống hộp 3 vẫn còn tận 7 ngày nữa.
 */
export function daySauKhiOn(the, qua, bayGio = Date.now()) {
  const box = qua ? Math.min((the?.box ?? 0) + 1, BOX_NGAY.length - 1) : 0;
  return {
    ...the,
    box,
    lastResult: !!qua,
    reviewedAt: bayGio,
    dueAt: bayGio + BOX_NGAY[box] * 86400000,
    soLanOn: (Number(the?.soLanOn) || 0) + 1,
  };
}

/** Bao nhiêu câu cho một lượt ôn. Ngắn là cố ý — ôn tập phải xong trong vài phút. */
export const SO_CAU_MOI_THE = 3;

/** Bao nhiêu thẻ mời bé làm một lần. */
export const SO_THE_MOI_LUOT = 3;

/**
 * Thẻ nào ĐẾN HẠN — và có bài để mà ôn.
 *
 * ⚠ LỌC THEO QUYỂN. Sổ thẻ là của cả tài khoản, chứa cả thẻ môn Toán
 * (`DL:KSN2.*`) lẫn mọi quyển Tiếng Anh. Bày thẻ của quyển khác vào trang chính
 * quyển này thì bé bấm vào là nhảy sang một bài lạ hoắc.
 *
 * ⚠ QUÁ HẠN LÂU NHẤT ĐỨNG TRƯỚC. Thẻ trễ ba tuần đáng ôn hơn thẻ vừa tới hạn
 * sáng nay; xếp theo thứ tự tạo thì thẻ trễ bị đẩy mãi ra sau và không bao giờ
 * tới lượt.
 */
export function theDenHan(cards, { quyen, bayGio = Date.now(), toiDa = SO_THE_MOI_LUOT } = {}) {
  const tien = quyen ? `DL:${String(quyen).toUpperCase()}.` : null;
  return (cards || [])
    .filter((c) => c?.microId && Number.isFinite(c.dueAt) && c.dueAt <= bayGio)
    .filter((c) => !tien || String(c.microId).startsWith(tien))
    .sort((a, b) => a.dueAt - b.dueAt)
    .slice(0, toiDa);
}

/** Có bao nhiêu thẻ đang chờ — cho con số trên thẻ mời ở trang chính. */
export const demDenHan = (cards, opt = {}) =>
  theDenHan(cards, { ...opt, toiDa: Infinity }).length;

/**
 * Chọn câu cho một thẻ, lấy từ chính bài của thẻ ấy.
 *
 * `kind: 'flashcard'` → bậc KHỞI ĐỘNG (nghe rồi bấm hình). Đó đúng là việc của
 *   một tấm thẻ từ vựng: gặp lại mặt chữ và tiếng đọc, không phải giải bài.
 * `kind: 'item'`      → bậc RÁP CÂU và THỬ THÁCH, vì mốc +3 và +7 ngày là lúc
 *   kiểm xem bé còn DÙNG được chứ không chỉ còn NHỚ.
 *
 * ⚠ THIẾU KHO THÌ LÙI, ĐỪNG TRẢ RỖNG. Bài nào không có bậc ráp câu (unit chỉ dạy
 * từ) mà đòi bằng được thì buổi ôn ra màn trắng. Lùi về bậc khởi động: ít đúng ý
 * hơn, nhưng bé vẫn ôn được, và ôn hơi dễ vẫn hơn không ôn.
 */
export function chonCauOn(bai, the, { soCau = SO_CAU_MOI_THE, batDau = 0 } = {}) {
  const kho = bai?.practice?.pools || {};
  const uu = the?.kind === 'flashcard'
    ? ['warmup', 'standard', 'challenge']
    : ['standard', 'challenge', 'warmup'];

  const gom = [];
  for (const k of uu) {
    for (const c of (kho[k] || [])) {
      if (c?.id) gom.push(c);
    }
    if (gom.length >= soCau) break;
  }
  if (!gom.length) return [];

  /* Xoay vòng theo `batDau` để hai lượt ôn cùng một bài không ra y hệt một bộ
     câu. `batDau` do chỗ gọi truyền vào (số lần đã ôn thẻ ấy), nên không cần
     ngẫu nhiên — mà không ngẫu nhiên thì cổng kiểm được. */
  const d = ((batDau % gom.length) + gom.length) % gom.length;
  return [...gom.slice(d), ...gom.slice(0, d)].slice(0, soCau);
}

/**
 * Kết quả một thẻ: bé làm ĐÚNG HẾT thì mới tính là qua.
 *
 * Nghiêm hơn bài học thường (ở đó sai vẫn đi tiếp được) là cố ý: cả điểm của lặp
 * lại ngắt quãng nằm ở chỗ thẻ nào chưa chắc thì quay lại SỚM. Cho qua khi mới
 * đúng 2/3 là giãn khoảng cách cho một thứ bé chưa vững, tức là làm hỏng đúng cái
 * cơ chế mình vừa dựng.
 */
export const theQua = (ketQua) =>
  Array.isArray(ketQua) && ketQua.length > 0 && ketQua.every(Boolean);
