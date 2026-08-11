/**
 * CỔNG BỘ GIẢ LẬP — cờ chạy thử tại máy KHÔNG được lọt lên mạng.
 * chạy: node test/gia_lap.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Soát 11-08-2026 mới lộ ra: `.env.local` trỏ thẳng vào dự án THẬT, nên `npm run dev`
 * xưa nay nói chuyện với Firebase thật — đi thử màn đăng nhập là gửi mail thật và lập
 * tài khoản thật. Vì thế bốn màn của mục H (đăng nhập · hồ sơ lần đầu · bảng xếp hạng
 * · bảng cô giáo) chưa bao giờ được ai đi thử, và ba tab của bảng cô giáo vỡ trắng
 * suốt mà không ai biết.
 *
 * Nay có cờ `VITE_FB_EMULATOR=1` kéo cả ba đường về máy. Nhưng một cái cờ như thế mà
 * lọt vào bản đưa lên mạng thì app thật đi tìm `127.0.0.1` và chết câm với mọi người
 * dùng. Nên cờ phải BUỘC kèm `import.meta.env.DEV` — Vite thay hằng ấy bằng `false`
 * lúc dựng, cả khối bị cắt khỏi bản dựng, không phải trông vào trí nhớ của ai.
 *
 * Hai chốt dưới đây gác đúng điều đó.
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';

const SRC = new URL('../src/', import.meta.url).pathname;
const DIST = new URL('../dist/assets/', import.meta.url).pathname;

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── 1 · Cờ phải kèm DEV ── */
const nen = readFileSync(`${SRC}chung/lib/nenTang.js`, 'utf8');
const dong = nen.split('\n').find((l) => l.includes('VITE_FB_EMULATOR')) || '';
t('cờ giả lập có khai', !!dong);
t('cờ giả lập BUỘC kèm import.meta.env.DEV',
  /DEV/.test(dong) || /DEV[\s\S]{0,120}VITE_FB_EMULATOR/.test(nen));

/* Chỉ MỘT nơi được quyết định có dùng giả lập hay không. Rải cờ ra nhiều tệp là sớm
   muộn có chỗ quên kèm DEV. */
function quet(thuMuc, ra = []) {
  for (const x of readdirSync(thuMuc, { withFileTypes: true })) {
    const p = `${thuMuc}/${x.name}`;
    if (x.isDirectory()) quet(p, ra);
    else if (/\.jsx?$/.test(x.name)) ra.push(p);
  }
  return ra;
}
const noiKhai = quet(SRC).filter((p) => readFileSync(p, 'utf8').includes('VITE_FB_EMULATOR'));
t(`chỉ MỘT nơi đọc cờ giả lập (${noiKhai.length})`, noiKhai.length === 1);

/* ── 2 · Bản dựng phải SẠCH ──
   Chỉ soi được khi đã `npm run build`; chưa dựng thì bỏ qua, đừng báo sai. */
if (existsSync(DIST)) {
  const js = readdirSync(DIST).filter((f) => f.endsWith('.js'))
    .map((f) => readFileSync(DIST + f, 'utf8')).join('\n');
  for (const dau of ['127.0.0.1:9099', '127.0.0.1:8080', '127.0.0.1:5001',
    'connectAuthEmulator', 'BỘ GIẢ LẬP']) {
    t(`bản dựng không mang "${dau}"`, !js.includes(dau));
  }
} else {
  console.log('  · chưa có dist/, bỏ qua phần soi bản dựng');
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
