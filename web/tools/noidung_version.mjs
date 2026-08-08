/**
 * Băm nội dung thành DẤU PHIÊN BẢN — nguồn duy nhất.
 *
 * vite.config.js dán mã này vào gói, test/dauphienban.test.mjs kiểm nó. Hai nơi
 * phải dùng CHUNG một hàm: nếu mỗi nơi tự chép một bản, sửa cách băm ở vite mà
 * test vẫn xanh, rồi con lại học bài cũ suốt bảy ngày mà không ai hay.
 *
 * Chỉ băm JSON là đủ cho cả hình: mỗi bài giữ `figureSpec[].sha256_16` của hình
 * mình dùng, nên vẽ lại hình thì JSON của bài cũng đổi theo.
 */
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

export function bamNoiDung(goc = 'public/content', doc = readFileSync) {
  const h = createHash('sha256');
  const di = (d) => {
    for (const ten of readdirSync(d).sort()) {
      const p = join(d, ten);
      if (statSync(p).isDirectory()) di(p);
      else if (ten.endsWith('.json')) { h.update(ten); h.update(doc(p)); }
    }
  };
  try { di(goc); } catch { return 'dev'; }
  return h.digest('hex').slice(0, 12);
}
