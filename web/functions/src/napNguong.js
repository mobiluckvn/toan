/**
 * ĐỌC BỘ NGƯỠNG Ở MÁY CHỦ — bảng `nguong` trên Firestore, có NHỚ TẠM.
 *
 * Bác chốt 10-10-2026 (câu ③): máy chủ đọc Firestore chứ không gói kèm lúc deploy.
 * Lý do: chuyên gia sửa ngưỡng xong là có hiệu lực ngay, không phải nhờ người viết
 * mã deploy lại — mà "không phải nhờ người viết mã" chính là điều R7 đòi.
 *
 * ── VÌ SAO TÁCH KHỎI `nguong.js` ──
 * `nguong.js` có hai bản chép giống hệt nhau từng ký tự; phần ĐỌC thì mỗi phía một
 * kiểu (máy con `fetch` tệp tĩnh, máy chủ đọc Firestore). Nhét vào tệp dùng chung là
 * phá luôn phép so của cổng `nguong_hai_ban`.
 *
 * ── NHỚ TẠM, VÀ VÌ SAO KHÔNG ĐỌC MỖI LƯỢT ──
 * Hàm nền chạy cho MỌI lượt trả lời của mọi bé. Đọc Firestore mỗi lượt là thêm một
 * lượt đọc cho mỗi câu trẻ làm — tốn tiền và chậm, đổi lấy một thứ gần như không bao
 * giờ đổi. Nhớ `HAN_NHO_MS` rồi đọc lại là đủ tươi: ngưỡng mới có hiệu lực chậm nhất
 * sau ngần ấy, và mục 3.8.4 vốn đã nói phiên bản mới chỉ áp cho phiên tiếp theo.
 *
 * ⚠ HỎNG THÌ LÙI VỀ MẶC ĐỊNH, KHÔNG NÉM. Firestore trục trặc mà làm hỏng cả đường
 *   chấm BKT thì một sự cố đọc cấu hình thành một sự cố mất điểm của trẻ.
 *
 * ⚠ BẢNG `nguong` CHƯA TỒN TẠI cho tới đợt 3 — lúc ấy đọc ra rỗng và hàm này lùi về
 *   bộ mặc định, đúng như mong muốn. Khi bảng có thật thì nó tự dùng, không phải sửa.
 */
import { datBoNguong, BO_MAC_DINH, boNguong } from './nguong.js';

/** Nhớ bao lâu thì đọc lại. */
export const HAN_NHO_MS = 5 * 60 * 1000;

let hetHan = 0;
let dangDoc = null;

/** Đếm số lần phải lùi về bộ mặc định. */
export const LOI_DOC = { lui: 0, ganNhat: null };

/** Chỉ dùng cho cổng: quên bộ đã nhớ. */
export function quenNguong() { hetHan = 0; dangDoc = null; }

/**
 * Trả về bộ ngưỡng đang hành ở máy chủ.
 *
 * @param db    Firestore (tiêm vào để cổng chạy được mà không cần mạng)
 * @param bayGio hàm lấy giờ, tiêm vào để cổng đo được chuyện hết hạn
 */
export async function layBoNguong(db, { bayGio = Date.now } = {}) {
  const gio = bayGio();
  if (gio < hetHan) return boNguong();
  if (dangDoc) return dangDoc;
  dangDoc = (async () => {
    let tho = null;
    try {
      const snap = await db.collection('nguong').get();
      const macDinh = {};
      const theoPhamVi = {};
      let phienBan = BO_MAC_DINH.phienBan;
      snap.forEach((d) => {
        const x = d.data() || {};
        if (!x.ma) return;
        if (Number.isFinite(x.phienBan)) phienBan = Math.max(phienBan, x.phienBan);
        const pv = x.phamVi;
        if (!pv || pv.loai === 'toanHe' || !pv.khoa) { macDinh[x.ma] = x.giaTri; return; }
        theoPhamVi[pv.loai] = theoPhamVi[pv.loai] || {};
        theoPhamVi[pv.loai][pv.khoa] = theoPhamVi[pv.loai][pv.khoa] || {};
        theoPhamVi[pv.loai][pv.khoa][x.ma] = x.giaTri;
      });
      if (Object.keys(macDinh).length || Object.keys(theoPhamVi).length) {
        tho = { phienBan, macDinh, theoPhamVi };
      }
    } catch (e) {
      LOI_DOC.ganNhat = String(e?.code || e?.message || e);
    }
    if (!tho) { LOI_DOC.lui += 1; tho = BO_MAC_DINH; }
    hetHan = bayGio() + HAN_NHO_MS;
    dangDoc = null;
    return datBoNguong(tho);
  })();
  return dangDoc;
}
