/**
 * Kiểm DẤU PHIÊN BẢN NỘI DUNG — chạy: node test/dauphienban.test.mjs
 *
 * Bài học và hình gắn `max-age=604800, immutable` mà tên tệp không đổi khi sửa nội
 * dung. Máy nào đã mở trang rồi sẽ giữ bản cũ tới BẢY NGÀY, không hỏi lại máy chủ:
 * sửa xong đẩy lên mà con vẫn học bài cũ, không ai biết.
 *
 * Chữa bằng cách dán mã băm nội dung vào đường dẫn (`?v=…`). Ba điều phải đúng:
 *   1. nội dung đổi → mã đổi (nếu không thì dán cũng vô ích)
 *   2. nội dung KHÔNG đổi → mã giữ nguyên (nếu không thì mỗi lần dựng lại là con
 *      phải tải lại 672 hình — tốn 3G của bố mẹ)
 *   3. mỗi hình lấy mã kiểm CỦA CHÍNH NÓ, để vẽ lại một hình không bắt tải lại cả bộ
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { dongDau, figureSrc, CONTENT, NOI_DUNG_V } from '../src/mon/toan/lib/noiDung.js';
/* Băm bằng ĐÚNG hàm vite.config.js dùng, không chép lại — chép lại thì sửa một
   bên mà bên kia vẫn xanh. */
import { bamNoiDung } from '../tools/noidung_version.mjs';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const GOC = new URL('../public/content', import.meta.url).pathname;
/** băm, có thể giả vờ một tệp mang nội dung khác để thử */
const bam = (doi = null) => bamNoiDung(GOC,
  (p) => (doi && p.endsWith(doi.ten) ? Buffer.from(doi.noi) : readFileSync(p)));

const v1 = bam();
t('băm ra mã 12 ký tự hex', /^[0-9a-f]{12}$/.test(v1));
t('băm hai lần cho cùng một mã (không đổi thì đừng bắt tải lại)', bam() === v1);

/* đổi ĐÚNG MỘT bài thì mã phải khác — nếu không, dán dấu cũng bằng thừa */
const motBai = readdirSync(join(GOC, 'lessons')).find((f) => f.endsWith('.json'));
const goc = readFileSync(join(GOC, 'lessons', motBai), 'utf8');
t('sửa một bài → mã đổi', bam({ ten: motBai, noi: goc.replace('}', ' }') }) !== v1);

/* ══ ĐỔI MỘT VIDEO THÌ MÃ CŨNG PHẢI ĐỔI ══ (bác bắt 19-08-2026)

   Bác dựng lại video xong, mở app ra vẫn thấy y bản cũ. Gốc: `bamNoiDung` chỉ băm
   JSON. Hình thì không sao — mỗi bài giữ `sha256_16` của hình mình dùng nên hình
   đổi là JSON đổi theo. Nhưng VIDEO thì `bai.video.tu[].tep` chỉ khai TÊN TỆP:

       video mới trên máy chủ  →  JSON không đổi  →  `?v=` không đổi
                               →  trình duyệt giữ bản cũ ĐỦ BẢY NGÀY

   Mà đó đúng là kiểu việc hay làm nhất — sửa lời kịch bản rồi dựng lại 158 video,
   không đụng một chữ nào trong bài học. Không có gì đỏ ở bất cứ đâu, chỉ có bé là
   xem bản cũ.

   Phép thử này giả vờ một video đổi kích thước. Nó chạy được vì `bamNoiDung` cho
   tệp nặng đi qua đúng đường tiêm `doc` như tệp JSON. */
{
  const tenVideo = (() => {
    const d = join(GOC, 'tienganh/video');
    try { return readdirSync(d).find((f) => f.endsWith('.mp4')); } catch { return null; }
  })();
  if (!tenVideo) {
    console.log('   ⏸ chưa có video nào để thử');
  } else {
    t('đổi MỘT video → mã đổi (nếu không, dựng lại video xong bé vẫn xem bản cũ)',
      bam({ ten: tenVideo, noi: 'x'.repeat(999) }) !== v1);
    /* Chiều ngược: đừng bắt tải lại khi không có gì đổi. */
    t('video không đổi thì mã giữ nguyên', bam() === v1);
  }
}

/* ── dán dấu vào đường dẫn ── */
t('dán dấu vào đường dẫn bài học',
  dongDau('/content/lessons/a.json', 'abc123') === '/content/lessons/a.json?v=abc123');
t('mỗi mã cho một đường dẫn khác nhau',
  dongDau('/x.json', 'aaa') !== dongDau('/x.json', 'bbb'));
/* Chạy bằng node thì không có biến dựng — phải lùi êm chứ không được nổ. */
t('không có mã dựng thì để nguyên đường dẫn', dongDau('/x.json', 'dev') === '/x.json');
t('mã mặc định luôn là chuỗi', typeof NOI_DUNG_V === 'string');

/* ── hình lấy mã kiểm CỦA CHÍNH NÓ ── */
const hinh = { file: 'figures/KSN5Q1_B1_M1_F1.png', sha256_16: '0123456789abcdef' };
t('hình dùng mã kiểm riêng của nó',
  figureSrc(hinh) === `${CONTENT}/figures/KSN5Q1_B1_M1_F1.png?v=0123456789abcdef`);
t('hai hình khác nội dung → hai đường dẫn khác',
  figureSrc(hinh) !== figureSrc({ ...hinh, sha256_16: 'fedcba9876543210' }));
t('cùng một hình, vẽ lại y hệt → đường dẫn giữ nguyên',
  figureSrc(hinh) === figureSrc({ ...hinh }));
t('hình không có mã kiểm vẫn ra đường dẫn dùng được', !!figureSrc({ file: 'figures/x.png' }));
t('không có hình thì trả null', figureSrc(null) === null);

/* ── mã kiểm trong dữ liệu phải thật, không phải chỗ trống ── */
const bai = readdirSync(join(GOC, 'lessons')).filter((f) => f.endsWith('.json'));
let soHinh = 0, thieu = 0;
for (const f of bai) {
  for (const s of JSON.parse(readFileSync(join(GOC, 'lessons', f), 'utf8')).figureSpec || []) {
    soHinh++;
    if (!/^[0-9a-f]{16}$/.test(s.sha256_16 || '')) thieu++;
  }
}
t(`cả ${soHinh} hình đều có mã kiểm hợp lệ (${thieu} thiếu)`, thieu === 0);

console.log(`\n   mã nội dung hiện tại: ${v1} · ${bai.length} bài · ${soHinh} hình`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
