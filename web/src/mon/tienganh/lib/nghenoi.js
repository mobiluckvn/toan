/**
 * NGHE BÉ NÓI — bọc quanh Web Speech API của trình duyệt.
 *
 * Chỉ lo việc NGHE và trả về chữ. Phần chấm nằm ở `chamnoi.js`, tách hẳn để chấm
 * được kiểm bằng `node` mà không cần micro.
 *
 * ── ⚠ TIẾNG CỦA BÉ ĐI ĐÂU ──
 * Chrome KHÔNG nhận dạng ngay trên máy: nó gửi tiếng lên máy chủ Google rồi nhận
 * chữ về. Nghĩa là giọng bé rời khỏi máy, và phải có mạng mới dùng được. Đây là
 * điều bố mẹ có quyền biết, nên màn hình phải nói ra chứ không giấu.
 *
 * Muốn đổi đường thì thay ĐÚNG tệp này — mọi chỗ khác chỉ gọi `batDauNghe()`:
 *   · Whisper chạy trên máy chủ mình  (kín hơn, tốn tiền và có độ trễ)
 *   · whisper.cpp biên dịch ra WASM   (chạy hẳn trên máy, nặng với máy tính bảng)
 *
 * ── VÌ SAO KHÔNG DÙNG `continuous` ──
 * `continuous = false` để trình duyệt TỰ nhận ra bé nói xong rồi dừng. Bé 6 tuổi
 * không biết bấm nút "dừng" đúng lúc; bắt bé bấm hai lần là mất một nửa số lần thử.
 * Vẫn có đồng hồ chặn ở đây, vì có máy không tự dừng bao giờ.
 */

const SR = typeof window !== 'undefined'
  && (window.SpeechRecognition || window.webkitSpeechRecognition);

/** Máy này nghe được không. Màn hình hỏi câu này TRƯỚC khi vẽ nút nói. */
export const ngheDuoc = () => !!SR;

/**
 * Giọng Anh-Anh, khớp với giọng đọc mẫu (`bf_emma`). Khai `en-US` thì máy chấm
 * theo chuẩn Mỹ trong khi bé vừa nghe mẫu Anh — hai chuẩn khác nhau ở đúng những
 * âm bài đang dạy (`/ɒ/` trong dog, `/ɑː/` trong car).
 */
export const TIENG = 'en-GB';

/** Bé 6 tuổi ngập ngừng lâu; cắt sớm là cắt mất câu. */
const HAN_GIO = 8000;

export class LoiNghe extends Error {
  constructor(ma, loi) { super(loi); this.ma = ma; }
}

const LOI_NOI = {
  'not-allowed': 'Máy chưa cho phép dùng micro. Bố mẹ bật giúp con nhé.',
  'service-not-allowed': 'Máy chưa cho phép dùng micro. Bố mẹ bật giúp con nhé.',
  'no-speech': 'Cô chưa nghe thấy gì cả.',
  'audio-capture': 'Máy không tìm thấy micro.',
  network: 'Cần có mạng thì cô mới nghe được.',
  'khong-ho-tro': 'Máy này chưa nghe được. Con vẫn học các phần khác bình thường nhé.',
  'qua-lau': 'Cô đợi hơi lâu rồi. Con thử nói lại nhé.',
};

export const loiDocDuoc = (ma) => LOI_NOI[ma] || 'Có trục trặc khi nghe. Con thử lại nhé.';

/**
 * Nghe một lượt.
 *
 * @returns {{dung:Function, xong:Promise<{chu:string, tinCay:number}>}}
 *   `dung()` để bé chủ động dừng; `xong` là lời hứa trả về chữ nghe được.
 *
 * `onTam` được gọi liên tục với chữ đang nghe dở — để màn hình hiện ngay, bé thấy
 * máy đang nghe mình thật. Không có phản hồi tức thời thì bé tưởng máy hỏng.
 */
export function batDauNghe({ onTam = () => {}, tieng = TIENG } = {}) {
  if (!SR) {
    return { dung() {}, xong: Promise.reject(new LoiNghe('khong-ho-tro')) };
  }
  const r = new SR();
  r.lang = tieng;
  r.continuous = false;          // trình duyệt tự nhận ra bé nói xong — xem đầu tệp
  r.interimResults = true;
  r.maxAlternatives = 3;

  let xong = false;
  let dongHo = null;
  const thoi = () => { clearTimeout(dongHo); dongHo = null; };

  const loiHua = new Promise((nhan, tuChoi) => {
    /* Giữ MỌI phương án máy đưa ra, không chỉ phương án đầu. Với giọng trẻ con,
       phương án đúng thường không đứng đầu — bộ chấm sẽ chọn cái nào hợp nhất. */
    const phuongAn = [];

    r.onresult = (e) => {
      let tam = '';
      for (let i = e.resultIndex; i < e.results.length; i += 1) {
        const kq = e.results[i];
        if (kq.isFinal) {
          for (let j = 0; j < kq.length; j += 1) phuongAn.push(kq[j].transcript);
        } else {
          tam += kq[0].transcript;
        }
      }
      if (tam) onTam(tam.trim());
    };
    r.onerror = (e) => {
      if (xong) return;
      xong = true; thoi();
      /* `no-speech` KHÔNG phải lỗi hỏng — bé chỉ chưa nói. Trả về chuỗi rỗng để
         bộ chấm xử như "chưa nghe thấy", đúng một đường đi thay vì hai. */
      if (e.error === 'no-speech') { nhan({ chu: '', phuongAn: [], tinCay: 0 }); return; }
      tuChoi(new LoiNghe(e.error, loiDocDuoc(e.error)));
    };
    r.onend = () => {
      if (xong) return;
      xong = true; thoi();
      nhan({ chu: (phuongAn[0] || '').trim(), phuongAn, tinCay: phuongAn.length ? 1 : 0 });
    };

    dongHo = setTimeout(() => { try { r.stop(); } catch { /* đã dừng */ } }, HAN_GIO);
  });

  try { r.start(); } catch { /* đang chạy rồi */ }
  return {
    dung() { try { r.stop(); } catch { /* đã dừng */ } },
    huy() { xong = true; thoi(); try { r.abort(); } catch { /* đã dừng */ } },
    xong: loiHua,
  };
}

/**
 * Xin quyền micro TRƯỚC khi vào bài.
 *
 * Hỏi quyền ngay giữa lúc bé đang nói là hỏng cả lượt: hộp thoại che màn hình, bé
 * mất đà, và lần thử ấy không tính. Hỏi trước một lần thì cả buổi học trôi.
 */
export async function xinMicro() {
  if (!navigator.mediaDevices?.getUserMedia) return false;
  try {
    const s = await navigator.mediaDevices.getUserMedia({ audio: true });
    s.getTracks().forEach((x) => x.stop());     // xin xong thì trả lại ngay
    return true;
  } catch { return false; }
}
