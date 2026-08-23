/**
 * CỔNG: không hook nào được đứng SAU một `return` sớm.
 *
 * ── VÌ SAO PHẢI CÓ CỔNG NÀY, VÀ VÌ SAO NÓ RA ĐỜI MUỘN ──
 * React đếm hook theo THỨ TỰ GỌI. Một component có `if (!bai) return …` ở giữa,
 * rồi `useRef` ở dưới, sẽ gọi ÍT hook hơn ở lần vẽ đầu (lúc `bai` còn null) so
 * với lần vẽ sau. React ném lỗi #310 và cả màn hình TRẮNG BỐC.
 *
 * Chuyện này đã xảy ra HAI LẦN trong repo này, và cả hai lần đều lọt qua:
 *   · 88 cổng xanh — không cổng nào đọc thứ tự hook;
 *   · `vite build` xanh — cú pháp hợp lệ, đây là lỗi LÚC CHẠY;
 *   · deploy trót lọt — chỉ lộ khi MỞ ĐÚNG màn ấy trên bản thật.
 * Lần thứ hai (23-08-2026) tệp `BaiHoc.jsx` thậm chí đã có sẵn một khối chú thích
 * dài cảnh báo đúng cái bẫy này, đặt ngay trên chỗ vi phạm. Chú thích không chặn
 * được ai — nên nay chặn bằng cổng.
 *
 * ── PHÉP SOI, VÀ CHỖ NÓ CỐ Ý THÔ ──
 * Đọc theo THỤT LỀ chứ không dựng cây cú pháp: trong thân một `function Ten(…) {`
 * viết hoa đầu (quy ước component của React), tìm lệnh `return` ở mức thụt lề gốc
 * (2 dấu cách), rồi đòi không dòng nào SAU nó gọi `useX(` ở cùng mức ấy.
 *
 * ⚠ CỐ Ý BỎ QUA hook nằm sâu hơn 2 dấu cách: đó là hook của HÀM KHÁC lồng bên
 * trong (hàm con, callback), thứ tự của chúng không liên quan. Bỏ sót kiểu này
 * chấp nhận được; bắt nhầm thì cổng ép người ta viết mã xấu đi cho cổng xanh —
 * cái giá đắt hơn nhiều, và đã dính 4 lần với các cổng ghim chính tả.
 */

import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const GOC = new URL('../src/', import.meta.url).pathname;

const dsTep = (thuMuc, ra = []) => {
  for (const t of readdirSync(thuMuc)) {
    const d = join(thuMuc, t);
    if (statSync(d).isDirectory()) dsTep(d, ra);
    else if (t.endsWith('.jsx')) ra.push(d);
  }
  return ra;
};

/* Bỏ chú thích để chữ "return" hay "useRef" trong lời giải thích không bị tính. */
const chiMa = (s) => s
  .replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '))
  .replace(/^([ \t]*)\/\/.*$/gm, '$1');

let pass = 0; const loi = [];

for (const tep of dsTep(GOC)) {
  const dong = chiMa(readFileSync(tep, 'utf8')).split('\n');
  let trong = null;      // tên component đang đọc
  let daReturn = 0;      // số dòng của lệnh `return` gốc đầu tiên

  dong.forEach((d, i) => {
    const moHam = d.match(/^(?:export default )?function ([A-Z]\w*)\s*\(/);
    if (moHam) { trong = moHam[1]; daReturn = 0; return; }
    if (/^\}/.test(d)) { trong = null; daReturn = 0; return; }
    if (!trong) return;

    /* `return` ở mức gốc: hai dấu cách rồi `return`, hoặc `if (…) return …`
       một dòng. Cả hai đều cắt luồng vẽ trước khi tới phần dưới. */
    if (!daReturn && /^ {2}(return\b|if \(.*\)\s*return\b)/.test(d)) daReturn = i + 1;

    /* Hook ở mức gốc, sau lệnh `return` ấy. */
    if (daReturn && /^ {2}(?:const|let)\s+[\w[{,\s\]}]+=\s*(?:React\.)?use[A-Z]\w*\(/.test(d)) {
      loi.push({ tep: tep.slice(GOC.length), ham: trong, dong: i + 1, tai: daReturn, ma: d.trim() });
    }
    /* Dạng gọi trần: `useEffect(() => …)` không gán vào biến nào. */
    if (daReturn && /^ {2}(?:React\.)?use[A-Z]\w*\(/.test(d)) {
      loi.push({ tep: tep.slice(GOC.length), ham: trong, dong: i + 1, tai: daReturn, ma: d.trim() });
    }
  });
  pass += 1;
}

if (loi.length) {
  console.log(`✗ ${loi.length} hook đứng sau \`return\` sớm — React sẽ ném lỗi #310, MÀN TRẮNG:`);
  for (const x of loi) {
    console.log(`   ${x.tep}:${x.dong}  trong <${x.ham}>  (return sớm ở dòng ${x.tai})`);
    console.log(`      ${x.ma}`);
  }
  console.log('   → Dời khai báo hook lên TRƯỚC mọi lệnh `return` của component.');
}
console.log(`${pass} tệp .jsx đã soi · ${loi.length} FAIL`);
process.exit(loi.length ? 1 : 0);
