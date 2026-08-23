/**
 * CỔNG: danh sách pha mà `onAttempt` nhận phải phủ hết pha HAI MÔN thật sự phát.
 *
 * ── VÌ SAO ──
 * `onAttempt` chỉ cập nhật P(L) cho những pha nằm trong danh sách trắng. Một pha
 * bé thật sự trả lời mà rơi ngoài danh sách thì lượt ấy biến mất khỏi mô hình
 * người học — im lặng, vì bản ghi vẫn nằm trong `attempts` đầy đủ.
 *
 * Đã xảy ra: trước 23-08-2026 danh sách chỉ có `practice`·`assess`, nên `check`
 * (câu chốt nhanh) và `worked` (câu xen giữa ví dụ mẫu) của môn TOÁN bị bỏ trắng
 * — 31% số câu bé thực làm, theo chính ghi chú trong `LessonPlayer.jsx`.
 *
 * Và khi nới ra, lời ghi kèm theo lại khẳng định "hai pha ấy chỉ Tiếng Anh phát,
 * không đụng gì Toán" — cũng sai: soi máy chủ thấy 49 lượt Toán mang chúng. Một
 * lời ghi sai trong mã còn nguy hơn không ghi gì, vì người sau tin theo rồi thu
 * hẹp danh sách lại. Nên nay đọc từ MÃ NGUỒN, không tin lời ghi.
 *
 * ── ⚠ PHÉP NÀY CỐ Ý KHÔNG ĐÒI "PHỦ HẾT MỌI PHA" ──
 * `intro`·`sample`·`teach` của Toán BỊ LOẠI có chủ ý: ở đó máy đang làm mẫu, bé
 * chưa tự trả lời. Nên phép kiểm là: mọi pha phát ra phải NẰM TRONG danh sách
 * trắng HOẶC nằm trong danh sách loại-có-chủ-ý. Pha thứ ba xuất hiện mà không
 * khai vào đâu cả thì cổng đỏ, và người thêm nó phải tự quyết định nó thuộc bên
 * nào — đúng chỗ cần một quyết định của con người.
 */

import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const doc = (d) => readFileSync(new URL(d, import.meta.url), 'utf8');
const chiMa = (s) => s
  .replace(/\/\*[\s\S]*?\*\//g, ' ')
  .replace(/^[ \t]*\/\/.*$/gm, ' ');

let pass = 0; let fail = 0;
const ok = (dieu, ten, them = '') => {
  if (dieu) { pass += 1; } else { fail += 1; console.log(`  ✗ ${ten}${them ? ` — ${them}` : ''}`); }
};

/* ── Danh sách trắng, đọc thẳng từ `functions/index.js` ───────────────────── */
const nen = chiMa(doc('../functions/index.js'));
const m = nen.match(/if \(!\[([^\]]+)\]\.includes\(a\.phase\)\) return;/);
ok(!!m, 'tìm được danh sách pha trong onAttempt');
const trang = new Set((m?.[1] || '').match(/'([a-z]+)'/g)?.map((x) => x.slice(1, -1)) || []);
console.log(`  danh sách trắng: ${[...trang].join(' · ')}`);

/* Pha loại CÓ CHỦ Ý — máy làm mẫu, bé chưa trả lời. */
const LOAI_CO_CHU_Y = new Set(['intro', 'sample', 'teach']);

/* ── Pha mà mã nguồn hai môn thật sự phát ─────────────────────────────────── */
const dsTep = (thuMuc, ra = []) => {
  for (const t of readdirSync(thuMuc)) {
    const d = join(thuMuc, t);
    if (statSync(d).isDirectory()) dsTep(d, ra);
    else if (/\.(js|jsx)$/.test(t)) ra.push(d);
  }
  return ra;
};

for (const mon of ['toan', 'tienganh']) {
  const goc = new URL(`../src/mon/${mon}/`, import.meta.url).pathname;
  const phat = new Set();
  for (const tep of dsTep(goc)) {
    const ma = chiMa(readFileSync(tep, 'utf8'));
    /* Ba lối phát pha đang dùng thật:
         phase: 'x'            — dựng bản ghi
         onRecord?.('x', …)    — màn con báo lên
         record('x', …)        — ghi vào nhật ký
       Đọc cả ba chứ không đoán theo một lối: mỗi môn viết một kiểu. */
    for (const re of [/phase:\s*'([a-z]+)'/g, /onRecord\?\.\('([a-z]+)'/g, /\brecord\('([a-z]+)'/g]) {
      for (const x of ma.matchAll(re)) phat.add(x[1]);
    }
  }
  console.log(`  môn ${mon} phát: ${[...phat].sort().join(' · ') || '(không thấy)'}`);
  ok(phat.size > 0, `đọc được pha môn ${mon} từ mã nguồn (tiền đề của phép kiểm)`);
  for (const p of phat) {
    ok(trang.has(p) || LOAI_CO_CHU_Y.has(p),
      `pha \`${p}\` của môn ${mon} có chỗ đứng`,
      'không nằm trong danh sách trắng của onAttempt, cũng không khai là loại có chủ ý '
      + '→ mọi lượt ở pha này biến mất khỏi mô hình người học, IM LẶNG');
  }
}

/* ── Và không được thu hẹp lại: hai pha đã lấy lại 31% số câu ─────────────── */
for (const p of ['check', 'worked']) {
  ok(trang.has(p), `danh sách trắng vẫn giữ \`${p}\``,
    'bỏ ra là mất lại 31% số câu bé thực làm — xem ghi chú ở LessonPlayer.jsx');
}

console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
