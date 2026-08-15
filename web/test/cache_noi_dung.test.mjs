/* ═══════════ NỘI DUNG ĐỂ IMMUTABLE — NÊN MỌI ĐƯỜNG NẠP PHẢI ĐÓNG DẤU ═══════════
 * chạy: node test/cache_noi_dung.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 *
 * `/content/**` mang `Cache-Control: public, max-age=604800, immutable`, mà tên tệp
 * thì KHÔNG mang mã băm: `DL_KSN2_B01.json` hôm nay và sau mười lần sửa vẫn là một
 * đường dẫn. Một mình dòng ấy là một cái bẫy chết người — `immutable` bảo trình
 * duyệt đừng hỏi lại máy chủ, kể cả khi bé bấm tải lại. Sửa đáp án xong đẩy lên, bé
 * đã từng mở app vẫn học bản cũ suốt BẢY NGÀY.
 *
 * Chuyện ấy KHÔNG xảy ra, vì có một cơ chế thứ hai gánh: `dongDau()` dán
 * `?v=<mã băm của toàn bộ JSON trong public/content>` vào mọi đường dẫn nội dung.
 * Nội dung đổi → mã đổi → thành URL mới → cache cũ không dính dáng gì nữa.
 *
 * Hai cơ chế ấy chỉ đúng KHI ĐI CÙNG NHAU. Bỏ một, cái còn lại thành lỗi:
 *
 *   · bỏ `dongDau` ở MỘT đường nạp → riêng tệp ấy đông cứng bảy ngày, mà là đông
 *     cứng LẶNG LẼ: bản dựng xanh, máy mới xanh, chỉ máy cũ sai;
 *   · bỏ `immutable` mà giữ `dongDau` → tốn một lượt hỏi lại cho mỗi bài, vô ích.
 *
 * Chỗ nguy là vế thứ nhất: viết `fetch(`${CONTENT}/...`)` là việc rất tự nhiên, và
 * KHÔNG có gì kêu lên cả. Tệp này chính là cái kêu ấy.
 *
 * ── ĐÃ SUÝT SỬA NHẦM (15-08-2026) ──
 *
 * Sau một lần deploy, mở bản thật rồi `fetch('/content/chuong_trinh.json')` bằng tay
 * trong console thì thấy nội dung CŨ — và suýt kết luận "header immutable là lỗi,
 * đổi hết sang no-cache". Sai: chính lần fetch bằng tay ấy mới là đường KHÔNG đóng
 * dấu. Giao diện app luôn hiện đúng bản mới. Muốn soi bản thật thì soi cái app vẽ
 * ra, hoặc tự thêm `?v=` — chứ đừng lấy fetch trần làm bằng chứng.
 *
 * ── PHÉP DƯỚI ĐÂY SOI GÌ ──
 *
 * ① header vẫn là cặp đã tính: nội dung cache dài + immutable, index.html no-cache;
 * ② MỌI chỗ dựng đường dẫn `${CONTENT}/…` trong mã đều nằm trong một lời gọi
 *    `dongDau(...)` — đây là phép chính;
 * ③ dấu phiên bản có thật, và ĐỔI khi nội dung đổi (không thì nó chỉ là trang trí).
 */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const G = new URL('../', import.meta.url).pathname;

/* ── ① header vẫn là cặp đã tính ── */
const fb = JSON.parse(readFileSync(join(G, 'firebase.json'), 'utf8'));
const luat = fb.hosting.headers || [];
const cc = (s) => {
  const l = luat.find((x) => x.source === s);
  return l ? (l.headers.find((h) => h.key === 'Cache-Control') || {}).value || '' : '';
};
t('nội dung vẫn cache dài + immutable', /immutable/.test(cc('/content/**'))
  && /max-age=\d{5,}/.test(cc('/content/**')));
t('index.html vẫn no-cache', /no-cache/.test(cc('/index.html')));
t('gói .js/.css vẫn immutable', /immutable/.test(cc('**/*.@(js|css)')));

/* ── ② mọi đường nạp nội dung đều đóng dấu ──
   Quét toàn bộ mã nguồn tìm chuỗi dựng đường dẫn nội dung, rồi hỏi: có nằm trong
   `dongDau(` không. Bắt theo VỊ TRÍ chứ không theo dòng — nhiều chỗ xuống dòng
   giữa `fetch(dongDau(` và đường dẫn. */
const tep = [];
(function di(d) {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) { if (f !== 'node_modules') di(p); }
    else if (/\.(js|jsx)$/.test(f)) tep.push(p);
  }
}(join(G, 'src')));

const quen = [];
let soCho = 0;
for (const p of tep) {
  const s = readFileSync(p, 'utf8');
  /* Nơi khai chính `dongDau` thì bỏ qua — nó là cái định nghĩa, không phải chỗ dùng. */
  if (p.endsWith('chung/lib/soQuyen.js')) continue;
  const re = /\$\{CONTENT\}/g;
  let m;
  while ((m = re.exec(s))) {
    soCho += 1;
    /* Nhìn lui 60 ký tự: một trong hai cửa đóng dấu phải nằm ngay trước đường dẫn,
       và không có dấu `)` chen giữa (nghĩa là lời gọi ấy đã đóng trước khi tới đây).
       HAI cửa, không phải một: `napJson` cố ý nhận đường dẫn TRẦN rồi tự đóng dấu
       bên trong — có phép kiểm riêng ngay dưới canh chuyện ấy. */
    const truoc = s.slice(Math.max(0, m.index - 60), m.index);
    const i = Math.max(truoc.lastIndexOf('dongDau('), truoc.lastIndexOf('napJson('));
    const ok = i >= 0 && !truoc.slice(i).includes(')');
    if (!ok) {
      const dong = s.slice(0, m.index).split('\n').length;
      quen.push(`${p.replace(G, '')}:${dong}`);
    }
  }
}
t(`có chỗ để mà soi (${soCho} chỗ dựng đường dẫn nội dung)`, soCho >= 15);
t(`mọi chỗ đều đóng dấu phiên bản (${quen.length} chỗ quên)`, quen.length === 0);
quen.slice(0, 8).forEach((x) => console.log('      quên `dongDau`:', x));

/* Và `napJson` — cửa nạp chung của Toán — phải tự đóng dấu, vì chỗ gọi nó truyền
   đường dẫn TRẦN vào (đúng như thiết kế). Mất dòng ấy là ba tệp chỉ mục đông cứng. */
const nd = readFileSync(join(G, 'src/mon/toan/lib/noiDung.js'), 'utf8');
const than = nd.slice(nd.indexOf('async function napJson'), nd.indexOf('export', nd.indexOf('async function napJson')));
t('`napJson` tự đóng dấu cho đường dẫn trần', /fetch\(dongDau\(url\)\)/.test(than));

/* ── ③ dấu phiên bản có tới được BẢN DỰNG THẬT không ──
   Bản thân phép băm đã có `test/dauphienban.test.mjs` soi kỹ (mã 12 ký tự, sửa bài
   thì mã đổi, hình dùng mã kiểm riêng…) nên đừng chép lại ở đây. Chỗ tệp ấy KHÔNG
   với tới là quãng cuối: từ `vite.config.js` ra tới gói `.js` nằm trong `dist/`.
   Rơi ở quãng ấy thì `NOI_DUNG_V` lùi về 'dev', `dongDau` trả đường dẫn TRẦN, và
   toàn bộ nội dung đông cứng bảy ngày — im lặng, vì mọi phép kiểm khác vẫn xanh. */
const vc = readFileSync(join(G, 'vite.config.js'), 'utf8');
t('bản dựng có dán `__NOI_DUNG_V__`', /__NOI_DUNG_V__:\s*JSON\.stringify\(bamNoiDung\(\)\)/.test(vc));

const { bamNoiDung } = await import(join(G, 'tools/noidung_version.mjs'));
const v1 = bamNoiDung();
t(`băm ra một mã thật (${v1})`, /^[0-9a-f]{12}$/.test(v1));

const dist = join(G, 'dist/assets');
if (existsSync(dist)) {
  const js = readdirSync(dist).filter((f) => /^index-.*\.js$/.test(f))
    .map((f) => readFileSync(join(dist, f), 'utf8')).join('');
  t(`mã phiên bản có mặt trong gói đã dựng (${v1})`, js.includes(v1));
} else {
  console.log('   (chưa có dist/ — bỏ qua phép cuối)');
}

console.log(`\n   ${soCho} đường nạp nội dung · dấu phiên bản ${v1} · `
  + `nội dung ${cc('/content/**')}\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
