/**
 * TẢI BỘ NGƯỠNG VỀ MÁY CON — việc duy nhất của tệp này.
 *
 * ── VÌ SAO TÁCH KHỎI `nguong.js` ──
 * `nguong.js` có HAI BẢN CHÉP giống hệt nhau từng ký tự (máy con và máy chủ), và cổng
 * `nguong_hai_ban` canh điều đó. Nhưng hai phía TẢI theo hai cách khác nhau (máy con
 * phải lo mất mạng, chưa đăng nhập, chế độ riêng tư; máy chủ thì không). Nhét cả hai
 * vào tệp dùng chung là phá luôn phép so ấy — nên phần tải nằm riêng, mỗi bên một bản.
 * Phần ĐỔI dòng bảng thành bộ thì vẫn chung: `boTuBang` ở `nguong.js`.
 *
 * ── BỐN NGUỒN, THEO ĐÚNG THỨ TỰ NÀY (Bảng 4.7, điểm 1) ──
 *   1. BẢNG `nguong` trên Firestore — nguồn THẬT, nơi chuyên gia phát hành. Trước
 *      22-11 máy con chỉ đọc tệp xuất lúc dựng, nên chuyên gia phát hành xong thì máy
 *      chủ chấm theo bộ mới mà màn hình của bé vẫn quyết định theo bộ cũ cho tới lần
 *      dựng sau — hai nửa hệ thống chạy hai luật, và không gì báo.
 *   2. BẢN NHỚ TẠI MÁY (`localStorage`) — bộ đọc được từ bảng ở lần mở trước. Mất
 *      mạng thì bé vẫn học bằng bộ chuyên gia đã phát hành gần nhất, chứ không tụt
 *      về bộ mặc định chỉ vì sóng yếu (R4).
 *   3. TỆP TĨNH `content/nguong.json` — bộ xuất lúc dựng. Máy mới tinh, chưa đăng
 *      nhập, chưa từng đọc được bảng thì đây là thứ tốt nhất còn lại.
 *   4. `BO_MAC_DINH` — bộ nằm sẵn trong mã. Không bao giờ hỏng.
 *
 * ── CÙNG KHUÔN `napDoThi()` ──
 * Nhớ lại kết quả, gộp lời gọi song song, và HỎNG THÌ LÙI chứ không ném.
 *
 * ── MỘT LẦN MỖI PHIÊN ──
 * Mục 3.8.4: "Phiên bản mới chỉ có hiệu lực từ phiên tiếp theo; phiên đang chạy
 * giữ nguyên bộ ngưỡng đã tải." Nên tệp này đọc bảng ĐÚNG MỘT LẦN lúc mở app rồi
 * nhớ; không nghe thay đổi, không đọc lại giữa buổi.
 */
import { CONTENT, dongDau } from './soQuyen.js';
import { datBoNguong, BO_MAC_DINH, boTuBang } from './nguong.js';

/**
 * Chờ tối đa bao lâu cho cả việc tải. `main.jsx` chờ hàm này TRƯỚC khi vẽ bất kỳ thứ
 * gì, nên mỗi mili-giây ở đây là màn trắng trước mặt bé. Ba giây là đủ cho mạng di
 * động chậm mà không thành "app treo".
 */
export const CHO_TOI_DA_MS = 3000;
/** Tệp tĩnh luôn được ít nhất ngần này, kể cả khi bước đọc bảng đã ăn gần hết hạn. */
const CHO_TEP_TOI_THIEU_MS = 800;

/** Khoá bản nhớ trong `localStorage`. Đổi hình dạng bản nhớ thì tăng số cuối. */
export const KHOA_NHO = 'ksn.nguong.v1';

let nho = null;
let dangNap = null;

/**
 * Bộ đã nạp từ ĐÂU và lùi mấy lần. Không hiện cho bé — có số thì còn lần ra.
 * `nguon`: 'bang' | 'nhoTam' | 'tep' | 'macDinh'.
 */
export const LOI_NAP = { lui: 0, ganNhat: null, nguon: null };

/** Một lời hứa có hạn chót. Hết hạn thì NÉM (để bước sau chạy), và luôn dọn bộ hẹn giờ. */
function henGio(hua, ms) {
  let id = null;
  const het = new Promise((_, nem) => { id = setTimeout(() => nem(new Error(`quá ${ms} ms`)), ms); });
  return Promise.race([hua, het]).finally(() => clearTimeout(id));
}

/**
 * Đọc bảng `nguong` — đường THẬT. Trả mảng dữ liệu các dòng, hoặc `null` khi không
 * thể đọc (không có Firebase, chưa đăng nhập).
 *
 * ⚠ IMPORT ĐỘNG `nenTang.js`. Tệp này được `main.jsx` import TĨNH; kéo tĩnh cả Firebase
 * vào đây thì cổng chạy bằng `node` không nạp nổi nó. Bản dựng thì không mất gì: App
 * vốn đã import `nenTang.js`, nên đây chỉ là trỏ vào cùng một module.
 *
 * ⚠ PHẢI CHỜ PHIÊN ĐĂNG NHẬP. Luật Firestore chỉ cho tài khoản đã đăng nhập đọc
 * `nguong`, mà lúc `main.jsx` chạy thì Firebase chưa kịp khôi phục phiên từ IndexedDB.
 * Đọc ngay là bị từ chối dù bé đã đăng nhập từ hôm qua.
 */
async function docBangFirestore() {
  const nt = await import('./nenTang.js');
  if (!nt.hasFirebase || !nt.db) return null;
  if (typeof nt.auth?.authStateReady === 'function') await nt.auth.authStateReady();
  if (!nt.auth?.currentUser) return null;
  const { collection, getDocs } = await import('firebase/firestore');
  const snap = await getDocs(collection(nt.db, 'nguong'));
  return snap.docs.map((d) => d.data());
}

/** Tệp tĩnh xuất lúc dựng. */
async function taiTepTinh() {
  /* ⚠ PHẢI `dongDau`. Nội dung được phục vụ `immutable, max-age=604800`, nên không
     đóng dấu phiên bản thì trình duyệt giữ bản cũ MỘT TUẦN. Cổng `cache_noi_dung`
     bắt được đúng chỗ này. */
  const r = await fetch(dongDau(`${CONTENT}/nguong.json`));
  return r.ok ? r.json() : null;
}

/**
 * Kho nhớ tại máy. Mọi lời gọi bọc `try`: chế độ riêng tư của Safari, kho bị chặn,
 * hay hết chỗ đều NÉM ở đây — và một lỗi ghi bản nhớ không được làm hỏng việc học.
 */
function khoMacDinh() {
  try { return typeof localStorage !== 'undefined' ? localStorage : null; } catch { return null; }
}

function docNho(kho) {
  try {
    const x = JSON.parse(kho?.getItem(KHOA_NHO) || 'null');
    return x?.bo?.macDinh ? x.bo : null;
  } catch { return null; }
}

function ghiNho(kho, bo) {
  try { kho?.setItem(KHOA_NHO, JSON.stringify({ luc: Date.now(), bo })); } catch { /* bỏ qua */ }
}

function xoaNho(kho) {
  try { kho?.removeItem(KHOA_NHO); } catch { /* bỏ qua */ }
}

/**
 * Nạp bộ ngưỡng rồi ĐẶT làm bộ của cả phiên.
 *
 * ⚠ PHẢI GỌI TRƯỚC KHI IMPORT `App.jsx` (xem `main.jsx`).
 *
 * Mọi tham số chỉ để cổng tiêm vào; chỗ gọi thật không truyền gì.
 * @param docBang  async () => [dòng] | null
 * @param kho      thứ có getItem/setItem/removeItem (mặc định `localStorage`)
 * @param taiTep   async () => bộ | null
 * @param choToiDa hạn chót cho cả việc tải (mili-giây)
 */
export async function napNguong({
  docBang = docBangFirestore, kho = khoMacDinh(), taiTep = taiTepTinh,
  choToiDa = CHO_TOI_DA_MS, bayGio = Date.now,
} = {}) {
  if (nho) return nho;
  if (!dangNap) {
    dangNap = (async () => {
      const hanChot = bayGio() + choToiDa;
      const conLai = () => Math.max(0, hanChot - bayGio());
      let tho = null;
      let nguon = null;
      let bangRong = false;
      LOI_NAP.ganNhat = null;

      /* 1 · BẢNG `nguong`. */
      try {
        const dong = await henGio(Promise.resolve().then(docBang), conLai());
        if (Array.isArray(dong)) {
          tho = boTuBang(dong);
          if (tho) { nguon = 'bang'; ghiNho(kho, tho); }
          /* Đọc ĐƯỢC mà bảng RỖNG: chưa ai phát hành, hoặc đã gỡ hết. Bản nhớ cũ khi
             ấy chắc chắn lỗi thời — xoá đi, để tệp tĩnh trả lời. */
          else { bangRong = true; xoaNho(kho); }
        }
      } catch (e) {
        LOI_NAP.ganNhat = String(e?.code || e?.message || e);
      }

      /* 2 · BẢN NHỚ TẠI MÁY — chỉ khi KHÔNG đọc được bảng (mất mạng, chưa đăng nhập). */
      if (!tho && !bangRong) {
        const bn = docNho(kho);
        if (bn) { tho = bn; nguon = 'nhoTam'; }
      }

      /* 3 · TỆP TĨNH. */
      if (!tho) {
        try {
          const t = await henGio(Promise.resolve().then(taiTep),
            Math.max(CHO_TEP_TOI_THIEU_MS, conLai()));
          if (t?.macDinh) { tho = t; nguon = 'tep'; }
        } catch (e) {
          LOI_NAP.ganNhat = LOI_NAP.ganNhat || String(e?.message || e);
        }
      }

      /* 4 · BỘ MẶC ĐỊNH. */
      if (!tho) {
        LOI_NAP.lui += 1;
        LOI_NAP.ganNhat = LOI_NAP.ganNhat || 'tệp không có trường macDinh';
        tho = BO_MAC_DINH;
        nguon = 'macDinh';
      }
      LOI_NAP.nguon = nguon;
      nho = datBoNguong(tho);
      return nho;
    })();
  }
  return dangNap;
}

/** Chỉ dùng cho cổng: quên bộ đã nhớ để nạp lại từ đầu. */
export function quenNguong() { nho = null; dangNap = null; }
