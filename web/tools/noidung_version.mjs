/**
 * Băm nội dung thành DẤU PHIÊN BẢN — nguồn duy nhất.
 *
 * vite.config.js dán mã này vào gói, test/dauphienban.test.mjs kiểm nó. Hai nơi
 * phải dùng CHUNG một hàm: nếu mỗi nơi tự chép một bản, sửa cách băm ở vite mà
 * test vẫn xanh, rồi con lại học bài cũ suốt bảy ngày mà không ai hay.
 *
 * Băm JSON là đủ cho HÌNH: mỗi bài giữ `figureSpec[].sha256_16` của hình mình
 * dùng, nên vẽ lại hình thì JSON của bài cũng đổi theo.
 *
 * ══ NHƯNG KHÔNG ĐỦ CHO VIDEO VÀ CLIP TIẾNG ══ (bác bắt 19-08-2026)
 *
 * Bác dựng lại video xong, mở app ra vẫn thấy y bản cũ. Lý do nằm đúng ở đây:
 * `bai.video.tu[].tep` chỉ khai TÊN TỆP (`DL_TA3_B00_tu_so1.mp4`), không khai vân
 * tay như hình. Dựng lại video mà không sửa chữ nào trong bài thì:
 *
 *     video mới trên máy chủ  →  JSON không đổi  →  dấu `?v=` không đổi
 *                             →  trình duyệt giữ bản cũ ĐỦ BẢY NGÀY
 *
 * Và đó chính là kiểu việc hay làm nhất: sửa lời kịch bản, dựng lại 158 video,
 * đẩy lên — không đụng một chữ nào trong bài học. Bé xem bản cũ, người lớn xem
 * bản cũ, mà máy chủ thì có bản mới nằm đó. Không có gì đỏ ở bất cứ đâu.
 *
 * Nay băm cả `.mp4` và `.mp3`, theo TÊN + KÍCH THƯỚC chứ không đọc nội dung: 158
 * video là mấy trăm MB, đọc hết mỗi lần dựng thì `npm run build` chậm hẳn, mà đổi
 * một video thì kích thước gần như chắc chắn đổi. Muốn chắc tuyệt đối thì phải
 * đặt vân tay vào tên tệp — việc lớn hơn, và chưa cần.
 */
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

/** Tệp nào đóng góp vào dấu, và đóng góp bằng gì. */
const NANG = /\.(mp4|mp3|m4a|webm|ogg|wav)$/i;

export function bamNoiDung(goc = 'public/content', doc = readFileSync) {
  const h = createHash('sha256');
  const di = (d) => {
    for (const ten of readdirSync(d).sort()) {
      const p = join(d, ten);
      if (statSync(p).isDirectory()) di(p);
      else if (ten.endsWith('.json')) { h.update(ten); h.update(doc(p)); }
      /* Tệp NẶNG: chỉ tên + kích thước. `doc` là đường tiêm của bộ kiểm — nó trả
         về một Buffer giả để thử "đổi nội dung thì mã có đổi không", nên ở đây
         cũng phải đi qua nó, không thì phép thử ấy không với tới được. */
      else if (NANG.test(ten)) {
        const noi = doc === readFileSync ? null : doc(p);
        h.update(ten);
        h.update(String(noi ? noi.length : statSync(p).size));
      }
    }
  };
  try { di(goc); } catch { return 'dev'; }
  return h.digest('hex').slice(0, 12);
}
