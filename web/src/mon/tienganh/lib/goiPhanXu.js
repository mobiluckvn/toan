/**
 * NHỜ MÁY PHÂN XỬ LƯỢT NÓI MƠ HỒ — chỗ DUY NHẤT của phần nói biết tới mạng (V10).
 *
 * Ba tầng, đúng khuôn phòng luyện nói · chấm viết · phụ đạo:
 *     chamnoi.js     luật thuần (vùng mơ hồ, phép áp phiếu), chạy được bằng node
 *     goiPhanXu.js   gọi máy chủ, canh giờ, không bao giờ ném        ← tệp này
 *     NutNoi.jsx     vẽ
 *
 * ── TỆP NÀY KHÔNG BAO GIỜ NÉM ──
 * Khác `goiPhuDao.js` (được phép ném, vì `dungPhuDao` bắt và lùi về kho tĩnh), ở
 * đây KHÔNG có ai bắt hộ: `NutNoi` gọi xong là hiện điểm cho bé. Nên mọi đường ra
 * của tệp này đều là một con số: hỏng · mất mạng · chưa có khoá · quá giờ đều trả
 * `dieuChinh: 0`, và 0 nghĩa là giữ nguyên điểm bộ chấm chuỗi đã cho.
 *
 * §7 chốt: "Mất mạng → giữ điểm cũ, không báo lỗi cho bé." Bé không biết là có
 * phần phân xử, nên một dòng đỏ về nó chỉ làm bé tưởng mình vừa làm sai cái gì.
 *
 * ── VÀ NÓ PHẢI CÓ TRẦN GIỜ ──
 * Lượt này nằm giữa lúc bé nói xong và lúc thấy điểm. Groq thường đáp trong một
 * giây, nhưng "thường" không phải là một bảo đảm, và một lượt gọi treo là nút "Đang
 * chấm…" treo theo — bé sáu tuổi bỏ đi trước khi nó nhả. Nên có `CHO_TOI_DA_MS`:
 * hết giờ thì bỏ phiếu, hiện điểm cũ ngay.
 */
import { httpsCallable } from 'firebase/functions';
import { fns, hasFirebase } from '../../../chung/lib/nenTang.js';

/**
 * Chờ nhiều nhất bao lâu cho cả hai phiếu.
 *
 * ⚠ Hằng xuất ra và có cổng canh: nới rộng là để bé ngồi nhìn nút xoay, thu hẹp là
 * phần phân xử gần như không bao giờ kịp về.
 */
export const CHO_TOI_DA_MS = 4000;

/** Đếm để còn lần ra. Không hiện ra cho bé, không ghi xuống Firestore. */
export const LOI_PHAN_XU = { goi: 0, hong: 0, quaGio: 0, chinh: 0, ganNhat: null };

/** Đường ra duy nhất khi không phân xử được. */
const GIU = { gan: 'khac', dieuChinh: 0, nhatTri: false };

/**
 * Lời gọi thật. Tách ra để cổng tiêm được hàm giả — KHÔNG mock cả module.
 *
 * ⚠ CHỐT MẠNG NẰM Ở ĐÂY, KHÔNG NẰM TRONG `nhoPhanXu`. Chạy bằng `node` thì
 * `hasFirebase` luôn sai (không có `import.meta.env`), nên một dòng
 * `if (!hasFirebase) return …` đặt trong `nhoPhanXu` sẽ chặn mọi lối trước khi hàm
 * tiêm vào kịp chạy — cổng xanh mà chưa gọi tới một dòng nào của phần đang thử.
 * Đúng cái bẫy đã gỡ ở `goiPhongNoi.js` hồi V1.
 */
export const goiMay = (du) => {
  if (!hasFirebase || !fns) throw new Error('Máy chưa nối được lên mạng.');
  return httpsCallable(fns, 'phanXuNoi')(du);
};

/**
 * Nhờ phân xử. Trả `{gan, dieuChinh, nhatTri}` — `dieuChinh` luôn là −1, 0 hay 1.
 *
 * @param goi  hàm gọi mạng, tiêm được khi thử
 */
export async function nhoPhanXu({ nghe, dich, canhTranh }, { goi = goiMay } = {}) {
  if (!nghe || !dich || !canhTranh) return GIU;
  /* Hai chữ trùng nhau thì chẳng có gì phân xử — bác ngay tại máy con, đừng tốn
     một lượt gọi để máy chủ bác hộ (`soiGoiPhanXu` cũng bác, hai tầng là cố ý). */
  if (String(dich).toLowerCase() === String(canhTranh).toLowerCase()) return GIU;

  LOI_PHAN_XU.goi += 1;
  /* ⚠ `Promise.race` KHÔNG huỷ được lời gọi kia — nó vẫn chạy tới lúc xong. Thế là
     chấp nhận được: nó không ghi gì, không vẽ gì, và tốn đúng cái đã tốn rồi. Điều
     phải tránh là để nó TRẢ LỜI MUỘN rồi đổi điểm sau khi bé đã thấy — nên kết quả
     muộn bị bỏ ở đây, không đi đâu được nữa. */
  let hetGio;
  const dongHo = new Promise((xong) => {
    hetGio = setTimeout(() => xong('QUA_GIO'), CHO_TOI_DA_MS);
  });
  try {
    /* `goi(...)` phải nằm TRONG `try`: `goiMay` ném ngay (đồng bộ) khi chưa nối
       mạng, và lời ném đồng bộ không chui vào `Promise.race` được. */
    const ra = await Promise.race([
      Promise.resolve().then(() => goi({ nghe, dich, canhTranh })).then((r) => r?.data ?? null),
      dongHo,
    ]);
    if (ra === 'QUA_GIO') {
      LOI_PHAN_XU.quaGio += 1;
      return GIU;
    }
    const b = Number(ra?.dieuChinh);
    if (!Number.isFinite(b) || b === 0) return { ...GIU, gan: ra?.gan || 'khac' };
    LOI_PHAN_XU.chinh += 1;
    LOI_PHAN_XU.ganNhat = `${dich}/${canhTranh} → ${ra?.gan} ${b > 0 ? '+1' : '−1'}`;
    /* Kẹp ±1 ở đây NỮA, dù máy chủ chỉ trả ±1: mức điều chỉnh là con số duy nhất
       từ ngoài mạng đi thẳng vào điểm của bé, nên nó không được tin một tầng. */
    return { gan: ra.gan, dieuChinh: Math.sign(b), nhatTri: !!ra.nhatTri };
  } catch {
    LOI_PHAN_XU.hong += 1;
    return GIU;
  } finally {
    clearTimeout(hetGio);
  }
}
