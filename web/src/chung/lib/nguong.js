/**
 * BỘ NGƯỠNG — bản MÁY CON. Ràng buộc R7 của luận văn (mục 3.8).
 *
 * ── VÌ SAO TỆP NÀY NẰM Ở `chung/`, KHÔNG Ở `mon/tienganh/` ──
 * Bác chốt 10-10-2026: hai môn dùng CHUNG một bộ ngưỡng. Mà cổng `ranh_gioi` cấm
 * `mon/toan/**` import của `mon/tienganh/**` (luật 1) và chỉ cho `mon/**` import
 * `chung/**` (luật 3). Nên chỗ duy nhất cả hai môn với tới được là đây.
 *
 * ── VÌ SAO CÓ HAI BẢN CHÉP ──
 * Bản kia ở `functions/src/nguong.js`. KHÔNG import chéo được: `functions/` lên
 * Cloud Functions với `package.json` riêng và chỉ mang theo thư mục của nó, còn
 * `src/` đi qua Vite. Đúng lối `chula.js` ↔ `lib/chamviet.js` đã dùng, và cũng
 * kèm theo đúng cái giá của nó:
 *
 * ⚠ SỬA MỘT BÊN LÀ PHẢI SỬA BÊN KIA, VÀ SỬA CẢ `data/nguong.json`. Cổng
 *   `nguong_hai_ban.test.mjs` so BA bản; lệch một con số là nó đỏ. Lệch ở đây hỏng
 *   theo kiểu khó thấy nhất: BKT chấm bằng θ này, màn hình quyết định bằng θ kia,
 *   và không gì báo.
 *
 * ── ĐỢT 1 LÀM TỚI ĐÂU ──
 * Mới có nấc phạm vi `toanHe`. `layNguong` đã nhận `nguCanh` ngay từ bây giờ để
 * đợt sau mở nấc hẹp mà KHÔNG phải sửa lại chỗ gọi — thêm giá trị theo phạm vi là
 * thêm dữ liệu, không phải sửa mã.
 */

/** Thang phạm vi, HẸP TRƯỚC RỘNG SAU. `layNguong` duyệt đúng thứ tự này. */
export const THANG_PHAM_VI = ['nut', 'dangCau', 'bac', 'loaiNut', 'khoiLop', 'mon', 'toanHe'];

/** Phiên bản bộ ngưỡng mặc định. Bản ghi lượt mang số này ở `nguongVer`. */
export const PHIEN_BAN = 1;

/**
 * GIÁ TRỊ MẶC ĐỊNH — đúng bằng con số đang chạy trước khi có R7.
 *
 * ⚠ Đưa ngưỡng ra dữ liệu KHÔNG ĐƯỢC ĐỔI HÀNH VI. Mọi giá trị ở đây phải bằng
 * đúng hằng số cũ; 103 cổng hiện có chính là phép kiểm cho điều đó.
 */
export const MAC_DINH = {
  NG01: 0.10,
  NG02: 0.08,
  NG03: 0.10,
  NG04: 0.30,
  NG05: { slip: 0.06, guess: 0.15 },
  NG06: 14,
  NG07: 0.85,
  NG08: 0.30,
  NG09: 3,
  NG10: 4,
  NG11: 3,
  NG12: 0.6,
  NG13: 14,
  NG14: 2,
  NG15: 3,
  NG16: 45,
  NG17: { ti: 0.25, toiThieuMoiNua: 3 },
  NG18: 8,
  NG19: 5,
  NG20: 4,
  NG21: 200,
};

/** Khoảng hợp lệ — GIỚI HẠN CỨNG, chuyên gia lẫn máy đều không ra ngoài được. */
export const KHOANG = {
  NG01: [0.01, 0.50], NG02: [0.01, 0.40], NG03: [0.01, 0.49], NG04: [0.05, 0.49],
  NG05: [0.01, 0.30], NG06: [3, 60], NG07: [0.70, 0.98], NG08: [0.10, 0.78],
  NG09: [2, 6], NG10: [1, 6], NG11: [1, 5], NG12: [0.3, 0.9], NG13: [3, 60],
  NG14: [1, 5], NG15: [2, 10], NG16: [15, 120], NG17: [0.10, 0.60], NG18: [5, 30],
  NG19: [3, 50], NG20: [3, 10], NG21: [50, 5000],
};

/**
 * LẤY MỘT NGƯỠNG — hàm THUẦN, không đọc mạng, không đọc giờ.
 *
 * Thuần là điều kiện tiên quyết của "quét lưới" ở mục 3.8.3: chạy lại cả nhật ký
 * với một dãy giá trị chỉ làm được khi hàm quyết định không giấu trạng thái nào.
 *
 * @param bo       bộ ngưỡng: { macDinh: {ma: giaTri}, theoPhamVi?: {loai: {khoa: {ma: giaTri}}} }
 * @param ma       mã ngưỡng, 'NG01'…'NG21'
 * @param nguCanh  { nut, dangCau, bac, loaiNut, khoiLop, mon } — thiếu khoá nào thì bỏ qua nấc ấy
 */
export function layNguong(bo, ma, nguCanh = {}) {
  const theo = bo?.theoPhamVi || {};
  for (const loai of THANG_PHAM_VI) {
    if (loai === 'toanHe') break;
    const khoa = nguCanh?.[loai];
    if (khoa == null) continue;
    const v = theo?.[loai]?.[khoa]?.[ma];
    if (v !== undefined) return v;
  }
  const chung = theo?.toanHe?.[ma];
  if (chung !== undefined) return chung;
  const mac = (bo?.macDinh ?? MAC_DINH)[ma];
  if (mac === undefined) throw new Error(`layNguong: không có ngưỡng ${ma}`);
  return mac;
}

/** Bộ ngưỡng chỉ gồm giá trị mặc định — dùng khi chưa tải được bộ của chuyên gia. */
export const BO_MAC_DINH = { phienBan: PHIEN_BAN, macDinh: MAC_DINH, theoPhamVi: {} };

/**
 * BỘ ĐANG HÀNH — một ô nhớ, đặt MỘT LẦN lúc mở phiên rồi thôi.
 *
 * ── VÌ SAO LÀ BIẾN, TRONG KHI `layNguong` PHẢI THUẦN ──
 * `layNguong` vẫn thuần: nó nhận bộ ngưỡng làm tham số. Ô nhớ này chỉ là chỗ CẤT bộ
 * đã tải, tách hẳn khỏi phép tính. Nhờ vậy quét lưới (mục 3.8.3) vẫn chạy lại được
 * cả nhật ký với một dãy giá trị mà không phải đụng vào ô này.
 *
 * ── VÌ SAO ĐẶT MỘT LẦN, KHÔNG ĐỔI GIỮA CHỪNG ──
 * Mục 3.8.2: "Máy người học tải tệp này cùng với `do_thi.json` khi mở bài và dùng nó
 * cho cả phiên", và 3.8.4: "Phiên bản mới chỉ có hiệu lực từ phiên tiếp theo; phiên
 * đang chạy giữ nguyên bộ ngưỡng đã tải." Đổi ngưỡng giữa buổi thì nửa đầu buổi và
 * nửa sau chấm theo hai luật, mà bản ghi chỉ mang được một số `nguongVer`.
 *
 * ⚠ Mọi hằng ngưỡng trong `mon/**` đọc ô này LÚC NẠP MODULE. Nên `main.jsx` phải
 * `await napNguong()` TRƯỚC khi import `App.jsx` — nếu không, mấy hằng ấy chụp đúng
 * bộ mặc định và tệp tải về chẳng tác dụng gì. Cổng `nguong_phien.test.mjs` canh.
 */
let _bo = BO_MAC_DINH;

/** Bộ ngưỡng đang dùng cho phiên này. */
export const boNguong = () => _bo;

/** Đặt bộ cho cả phiên. Trả về chính bộ đã đặt, để chỗ gọi ghi `nguongVer`. */
export function datBoNguong(bo) {
  const sach = bo && typeof bo === 'object' && bo.macDinh ? bo : BO_MAC_DINH;
  _bo = { phienBan: sach.phienBan ?? PHIEN_BAN,
          macDinh: { ...MAC_DINH, ...(sach.macDinh || {}) },
          theoPhamVi: sach.theoPhamVi || {} };
  return _bo;
}

/* Mấy ngưỡng mang HAI con số thì soi theo trường nào. */
const TRUONG_SO = { NG05: ['slip', 'guess'], NG17: ['ti'] };

const trongKhoang = (ma, v) => {
  const k = KHOANG[ma];
  if (!k) return false;
  const so = TRUONG_SO[ma] ? TRUONG_SO[ma].map((t) => v?.[t]) : [v];
  return so.every((x) => typeof x === 'number' && Number.isFinite(x)
                         && x >= k[0] && x <= k[1]);
};

/**
 * SOI MỘT BỘ NGƯỠNG — ba loại điều kiện của mục 3.8.4, trả về danh sách chỗ sai.
 *
 * ⚠ TRẢ VỀ DANH SÁCH, KHÔNG NÉM. Chuyên gia sửa một lần nhiều ngưỡng thì phải thấy
 * HẾT chỗ sai, chứ không phải sửa một chỗ rồi lại gặp chỗ sau — đúng lẽ `soiLoiCham`
 * đã dùng ở phần chấm viết.
 *
 * Phép kiểm thứ ba của mục 3.8.4 — NHỊP TINH THÔNG phải nằm trong 3–6 câu — KHÔNG
 * làm ở đây: nó cần chạy Thuật toán 3.1 (BKT), mà BKT nằm ở máy chủ. Màn hình quản
 * lý ngưỡng gọi riêng; xem mục 3.8.4 và `ke_hoach_r7_bang_nguong.md` đợt 3.
 */
export function soiNguong(bo) {
  const loi = [];
  const lay = (ma, nguCanh) => {
    try { return layNguong(bo, ma, nguCanh); } catch { return undefined; }
  };
  for (const ma of Object.keys(KHOANG)) {
    const v = lay(ma, {});
    if (v === undefined) { loi.push({ ma, vi: 'không có giá trị' }); continue; }
    if (!trongKhoang(ma, v)) {
      loi.push({ ma, vi: `ngoài khoảng [${KHOANG[ma][0]}, ${KHOANG[ma][1]}]`, giaTri: v });
    }
  }
  /* Ràng buộc GIỮA các ngưỡng — mục 3.8.4. */
  const theta = lay('NG07', {});
  const yeu = lay('NG08', {});
  if (typeof theta === 'number' && typeof yeu === 'number' && yeu > theta - 0.20) {
    loi.push({ ma: 'NG08', vi: `θ_yếu phải ≤ θ − 0,20 (θ = ${theta})`, giaTri: yeu });
  }
  for (const [ma, truong] of [['NG03', null], ['NG04', null],
                              ['NG05', 'slip'], ['NG05', 'guess']]) {
    const v = truong ? lay(ma, {})?.[truong] : lay(ma, {});
    if (typeof v === 'number' && v >= 0.5) {
      loi.push({ ma, vi: `${truong || ma} phải < 0,5 để mô hình không suy biến`, giaTri: v });
    }
  }
  return loi;
}
