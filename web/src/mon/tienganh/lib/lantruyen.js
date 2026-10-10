import { layNguong, boNguong } from '../../../chung/lib/nguong.js';
/**
 * LAN TRUYỀN TRÊN ĐỒ THỊ — tìm chỗ hổng THẬT, không phải chỗ lộ ra (mục 2.3.3).
 *
 * ── VẤN ĐỀ NÓ GIẢI ──
 * Bé sai câu "How many books are there?" ở unit 12. Chỗ LỘ RA là unit 12. Nhưng
 * bé có thể sai vì chưa vững số đếm học từ unit 2 — và luyện thêm mẫu câu unit 12
 * thì bé vẫn sai, vì cái hổng nằm chỗ khác. Đây là chỗ một hệ thống "thích ứng"
 * khác hẳn một hệ thống chỉ đếm đúng/sai.
 *
 * ── HAI CHIỀU, HAI VIỆC KHÁC NHAU ──
 *   NGƯỢC (α) đi tìm NGUYÊN NHÂN: từ nút bé sai, lần ngược theo cạnh tiên quyết,
 *     mỗi bước nhân độ ngờ với α. Nút nào vừa bị nghi vừa có P(L) thấp thì đáng
 *     ngờ nhất — đó là nút gốc rễ.
 *   XUÔI (β) đi CỘNG HƯỞNG: bé thạo một nút thì các nút mà nó làm nền cho cũng
 *     đáng tin hơn đôi chút.
 *
 * ── ⚠ β CHỈ CỘNG, KHÔNG ĐƯỢC ĐẨY QUA NGƯỠNG THẠO ──
 * Để β đẩy một nút lên thẳng "đã thạo" khi bé CHƯA LÀM câu nào của nút ấy là
 * tuyên thạo khống — và tuyên khống thì hệ thống bỏ qua bài bé chưa từng học, im
 * lặng. Đây là lỗi nguy nhất của cả mục này, nên `NGUONG_TRAN` chặn cứng.
 */
import { duyetNguoc, duyetXuoi, nhanNut } from './doThi.js';
import { NGUONG_THAO, mucThaoCua } from './zpd.js';

/** Mỗi bước lùi thì độ ngờ còn lại bấy nhiêu. */
export const ALPHA = layNguong(boNguong(), 'NG12');

/** Mỗi bước tiến thì cộng thêm bấy nhiêu, nhân với mức thạo của nút nguồn. */
export const BETA = 0.08;

/**
 * ⚠ TRẦN CỦA LAN TRUYỀN XUÔI. Cộng hưởng không bao giờ được đưa một nút TỚI
 * ngưỡng thạo — chỉ bài bé thật sự làm mới làm được điều đó.
 */
export const NGUONG_TRAN = NGUONG_THAO - 0.05;

/**
 * NÚT GỐC RỄ — bé sai ở `maNut`, thật ra hổng ở đâu.
 *
 * Trả `[{ ma, doNgo, p, buoc }]`, đáng ngờ nhất đứng trước.
 *
 * `doNgo` = α^bước × (1 − P(L)). Hai thành phần, và cần cả hai:
 *   · α^bước  — càng xa chỗ sai thì càng khó gọi là nguyên nhân;
 *   · 1−P(L)  — nút bé đã vững thì không phải thủ phạm, dù nó là tiên quyết.
 *
 * ⚠ NÚT CHƯA CÓ SỐ thì coi như P(L) = L0 (bé chưa học) — tức là RẤT đáng ngờ, và
 * đúng thế: một tiên quyết bé chưa từng chạm chính là lý do hay gặp nhất. Nhưng
 * KHÔNG coi nó là 0 tuyệt đối, vì "chưa có tin" vẫn khác "đã đo và thấy hổng".
 */
export const P_MAC_DINH = 0.1;

/** NG10 · d — đi ngược xa nhất mấy bước khi tìm nút gốc rễ. */
export const SAU_TOI_DA = layNguong(boNguong(), 'NG10');
/** NG11 · m — trả về nhiều nhất mấy nút gốc. */
export const NUT_GOC_TOI_DA = layNguong(boNguong(), 'NG11');

export function nutGocRe(dt, mucThao, maNut,
                         { sauToiDa = SAU_TOI_DA, toiDa = NUT_GOC_TOI_DA } = {}) {
  if (!maNut) return [];
  const ds = duyetNguoc(dt, maNut, { sauToiDa });
  return ds
    .map(({ ma, buoc }) => {
      const p = mucThaoCua(mucThao, ma) ?? P_MAC_DINH;
      return { ma, buoc, p, doNgo: (ALPHA ** buoc) * (1 - p) };
    })
    /* Nút bé đã THẠO thì loại hẳn, không xếp hạng thấp: giữ lại là màn hình có
       thể bày ra "chỗ hổng gốc rễ" trỏ vào một thứ bé làm đúng mãi. */
    .filter((x) => x.p < NGUONG_THAO)
    .sort((a, b) => b.doNgo - a.doNgo)
    .slice(0, toiDa);
}

/**
 * CỘNG HƯỞNG XUÔI — bé thạo nút này thì các nút dựng trên nó nhích lên đôi chút.
 *
 * Trả về map `{ maNut: p_moi }` CHỈ gồm những nút có thay đổi. Bên gọi tự quyết
 * dùng hay không — hàm này không sửa `mucThao` gốc.
 *
 * ⚠ BA CHỐT, thiếu chốt nào cũng thành tuyên thạo khống:
 *   1. chỉ lan từ nút bé THẬT SỰ đã thạo;
 *   2. mức cộng nhỏ dần theo bước (β / bước);
 *   3. kết quả bị KẸP dưới `NGUONG_TRAN` — không bao giờ chạm ngưỡng thạo.
 */
export function congHuong(dt, mucThao, { sauToiDa = 2, beta = BETA } = {}) {
  const ra = {};
  const nguon = Object.keys(mucThao || {}).filter(
    (ma) => (mucThaoCua(mucThao, ma) ?? 0) >= NGUONG_THAO,
  );
  for (const g of nguon) {
    const pg = mucThaoCua(mucThao, g) ?? 0;
    for (const { ma, buoc } of duyetXuoi(dt, g, { sauToiDa })) {
      const cu = ra[ma] ?? mucThaoCua(mucThao, ma) ?? P_MAC_DINH;
      /* Đã thạo rồi thì cộng hưởng không có việc gì làm. */
      if (cu >= NGUONG_THAO) continue;
      const them = (beta / buoc) * pg;
      ra[ma] = Math.min(NGUONG_TRAN, cu + them);
    }
  }
  return ra;
}

/**
 * MA TRẬN TRẠNG THÁI — một dòng cho mỗi nút bé đang chật vật, kèm nút gốc rễ.
 *
 * Đây là thứ màn cô giáo cần: không phải "em này sai 12 câu", mà "em này sai ở
 * mẫu câu unit 12, mà gốc là số đếm unit 2".
 *
 * ⚠ CHỈ NHẬN NÚT ĐÃ CÓ SỐ. Nút bé chưa từng chạm không phải "đang chật vật" —
 * gộp chúng vào là bảng đầy những dòng nói "em chưa học phần này", đúng nhưng vô
 * dụng, và nó dìm mất mấy dòng thật sự đáng xem.
 */
export function maTranTrangThai(dt, mucThao, { nguong = 0.5, toiDa = 10 } = {}) {
  return Object.keys(mucThao || {})
    /* ⚠ GIẢI MÃ KHOÁ. Tên tài liệu `mastery` là `encodeURIComponent(bktUnit)`, nên
       khoá thô có thể là `CHUONG%3A1%40G3`. Bày thẳng ra là bố mẹ đọc một chuỗi mã
       hoá URL — đã xảy ra thật ngày 22-08. */
    .map((k) => { try { return decodeURIComponent(k); } catch { return k; } })
    /* ⚠ CHỈ NHẬN NÚT CÓ TRONG ĐỒ THỊ TIẾNG ANH. `mastery/{uid}/units` dùng CHUNG
       với môn Toán (chủ ý — xem `duLieu.js`), nên không lọc thì mã của Toán
       (`CHUONG:1@G3`) lọt thẳng vào bảng của Tiếng Anh. Đúng lỗi bác bắt được
       22-08. Lọc theo đồ thị vừa chặn được điều đó vừa đúng về nguyên tắc: nút
       không có trong đồ thị thì cũng chẳng lan truyền chẩn đoán được. */
    .filter((ma) => !!dt?.nut?.[ma])
    .map((ma) => ({ ma, p: mucThaoCua(mucThao, ma), nhan: nhanNut(dt, ma) }))
    .filter((x) => x.p !== null && x.p < nguong)
    .sort((a, b) => a.p - b.p)
    .slice(0, toiDa)
    .map((x) => {
      const g = nutGocRe(dt, mucThao, x.ma, { toiDa: 1 })[0] || null;
      return { ...x, goc: g ? { ...g, nhan: nhanNut(dt, g.ma) } : null };
    });
}
