/**
 * TẢI BỘ NGƯỠNG VỀ MÁY CON — việc duy nhất của tệp này.
 *
 * ── VÌ SAO TÁCH KHỎI `nguong.js` ──
 * `nguong.js` có HAI BẢN CHÉP giống hệt nhau từng ký tự (máy con và máy chủ), và cổng
 * `nguong_hai_ban` canh điều đó. Nhưng hai phía TẢI theo hai cách hoàn toàn khác:
 * máy con `fetch` một tệp tĩnh, máy chủ đọc Firestore. Nhét cả hai vào tệp dùng chung
 * là phá luôn phép so ấy — nên phần tải nằm riêng, mỗi bên một bản của mình.
 *
 * ── CÙNG KHUÔN `napDoThi()` ──
 * Nhớ lại kết quả, gộp lời gọi song song, và HỎNG THÌ LÙI VỀ BỘ MẶC ĐỊNH chứ không
 * ném. Mất mạng là bé vẫn học được (R4) — chỉ là học với bộ ngưỡng mặc định, đúng
 * cái bộ đã nằm sẵn trong mã.
 */
import { CONTENT, dongDau } from './soQuyen.js';
import { datBoNguong, BO_MAC_DINH } from './nguong.js';

let nho = null;
let dangNap = null;

/** Đếm số lần phải lùi về bộ mặc định. Không hiện cho bé — có số thì còn lần ra. */
export const LOI_NAP = { lui: 0, ganNhat: null };

/**
 * Tải `content/nguong.json` rồi ĐẶT làm bộ của cả phiên.
 *
 * ⚠ PHẢI GỌI TRƯỚC KHI IMPORT `App.jsx`. Mọi hằng ngưỡng trong `mon/**` đọc bộ đang
 * hành lúc nạp module; gọi sau thì chúng đã chụp xong bộ mặc định rồi.
 */
export async function napNguong() {
  if (nho) return nho;
  if (!dangNap) {
    dangNap = (async () => {
      let tho = null;
      try {
        /* ⚠ PHẢI `dongDau`. Nội dung được phục vụ `immutable, max-age=604800`, nên
           không đóng dấu phiên bản thì trình duyệt giữ bản cũ MỘT TUẦN — chuyên gia
           sửa ngưỡng xong, bé vẫn học bằng bộ cũ bảy ngày mà không gì báo. Cổng
           `cache_noi_dung` bắt được đúng chỗ này. */
        const r = await fetch(dongDau(`${CONTENT}/nguong.json`));
        tho = r.ok ? await r.json() : null;
      } catch (e) {
        LOI_NAP.ganNhat = String(e?.message || e);
      }
      if (!tho?.macDinh) {
        LOI_NAP.lui += 1;
        LOI_NAP.ganNhat = LOI_NAP.ganNhat || 'tệp không có trường macDinh';
        tho = BO_MAC_DINH;
      }
      nho = datBoNguong(tho);
      return nho;
    })();
  }
  return dangNap;
}

/** Chỉ dùng cho cổng: quên bộ đã nhớ để nạp lại từ đầu. */
export function quenNguong() { nho = null; dangNap = null; }
