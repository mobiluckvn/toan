/**
 * ĐỌC LÊN — bọc quanh `speechSynthesis` của trình duyệt.
 *
 * Bác chốt 13-08: phòng luyện nói dùng Web Speech cho CẢ HAI thứ tiếng. Câu ở đây
 * do máy sinh ra ngay lúc nói chuyện, nên không có clip Kokoro nào sẵn — mà chờ
 * sinh clip thì bé ngồi đợi, còn gọi TTS trên mạng thì mỗi câu thêm một vòng.
 *
 * ── MỘT LỜI ĐỌC, MỘT THỨ TIẾNG ──
 * Kho này đã chốt "mỗi dòng chỉ MỘT thứ tiếng" từ hồi làm dây chuyền âm, và ở đây
 * cũng thế: câu tiếng Anh đọc giọng `en-GB`, lời tiếng Việt đọc giọng `vi-VN`. Trộn
 * vào một lời là máy đọc tiếng Anh bằng giọng Việt — bé bắt chước theo thì hỏng
 * đúng cái mình đang dạy.
 *
 * ── VÌ SAO `en-GB` ──
 * Cùng chuẩn với giọng mẫu `bf_emma` của Kokoro và với bộ chấm (`TIENG = 'en-GB'`).
 * Để `en-US` thì bé nghe mẫu Anh ở bài học rồi nghe giọng Mỹ ở phòng nói, mà hai
 * chuẩn khác nhau ở đúng những âm lớp 1 đang học.
 */

const CO = typeof window !== 'undefined' && 'speechSynthesis' in window;

/** Máy này đọc được không. Màn hình hỏi câu này TRƯỚC khi vẽ nút nghe. */
export const docDuoc = () => CO;

/**
 * Trình duyệt nạp danh sách giọng KHÔNG đồng bộ: gọi `getVoices()` ngay lúc mở
 * trang thường trả về mảng rỗng, và thế là mọi câu đọc bằng giọng mặc định của
 * máy — tiếng Anh phát ra giọng Việt. Nên phải đợi sự kiện `voiceschanged`.
 */
let dsGiong = [];
if (CO) {
  const nap = () => { dsGiong = window.speechSynthesis.getVoices() || []; };
  nap();
  window.speechSynthesis.addEventListener?.('voiceschanged', nap);
}

/**
 * Chọn giọng khớp thứ tiếng. Không có thì trả `null` và để trình duyệt tự lo —
 * vẫn hơn là không đọc gì.
 */
export function giongCho(tieng) {
  const ma = tieng.toLowerCase();
  const goc = ma.split('-')[0];
  return dsGiong.find((g) => g.lang?.toLowerCase() === ma)
      ?? dsGiong.find((g) => g.lang?.toLowerCase().startsWith(goc))
      ?? null;
}

/** Máy có giọng cho thứ tiếng này không — để màn hình nói thật với bố mẹ. */
export const coGiong = (tieng) => !!giongCho(tieng);

export function thoiDoc() { if (CO) window.speechSynthesis.cancel(); }

/**
 * Đọc một câu. Trả về lời hứa xong-thì-báo, để đọc liền hai câu theo đúng thứ tự.
 *
 * ── VÌ SAO CÓ ĐỒNG HỒ CHẶN ──
 * `onend` của `speechSynthesis` là thứ không đáng tin: có máy không bao giờ gọi nó
 * (nhất là khi tab mất tiêu điểm giữa chừng). Không có đồng hồ thì lời hứa treo
 * mãi, và câu tiếng Việt sau nó KHÔNG BAO GIỜ được đọc — bé ngồi đợi một thứ đã
 * chết. Thà cắt sớm còn hơn treo.
 */
export function doc(chu, tieng = 'en-GB', { nhanh = 1 } = {}) {
  const s = String(chu || '').trim();
  if (!CO || !s) return Promise.resolve(false);

  return new Promise((xong) => {
    const l = new SpeechSynthesisUtterance(s);
    l.lang = tieng;
    const g = giongCho(tieng);
    if (g) l.voice = g;
    /* Chậm hơn người lớn một chút: bé 6 tuổi cần kịp nghe từng tiếng để nhại lại. */
    l.rate = nhanh;

    let da = false;
    const het = (ok) => { if (da) return; da = true; clearTimeout(dongHo); xong(ok); };
    /* Ước lượng rộng tay: ~90ms một ký tự, tối thiểu 3 giây. */
    const dongHo = setTimeout(() => het(false), Math.max(3000, s.length * 90));

    l.onend = () => het(true);
    l.onerror = () => het(false);
    window.speechSynthesis.speak(l);
  });
}

/**
 * Đọc câu tiếng Anh rồi tới lời tiếng Việt — đúng thứ tự ấy.
 *
 * Tiếng Anh TRƯỚC vì đó là thứ bé phải nhại; lời giải thích đến sau khi bé đã nghe
 * mẫu. Đảo lại thì bé nghe giải thích xong đã quên mất câu.
 */
export async function docCapDoi({ en, vi, nhanhEn = 0.9 } = {}) {
  thoiDoc();
  if (en) await doc(en, 'en-GB', { nhanh: nhanhEn });
  if (vi) await doc(vi, 'vi-VN');
}
