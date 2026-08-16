/* ═══════════ VIDEO DÀI BAO LÂU ═══════════
 * chạy: node test/video_dai_bao_lau.test.mjs
 *
 * Bác chốt 14-08-2026: video giảng dài **45 tới 70 giây**. Ngắn quá thì chưa kịp
 * dạy gì; dài quá thì bé lớp hai lớp ba ngồi không nổi — mà bé ngồi không nổi thì
 * nó bấm bỏ qua, và cả bài giảng thành công cốc.
 *
 * ── VÌ SAO CẦN CỔNG ──
 *
 * Con số ấy KHÔNG có gì canh, nên nó trôi dần. Ngày 16-08 đếm lại: chín video vượt
 * 70 giây, trong đó bảy của lớp 4 đã deploy từ lâu, dài nhất 77,5 giây. Không ai cố
 * ý — mỗi lần thêm một câu giải thích thì nó dài thêm vài giây, và không có gì kêu.
 *
 * Đây đúng dòng họ "ngưỡng phần trăm che lỗ thủng": một con số ai cũng nhớ mà không
 * ai đo thì sớm muộn chỉ còn là câu nói.
 *
 * ── NGƯỠNG ĐẶT Ở ĐÚNG CHỖ DỮ LIỆU ĐANG ĐỨNG ──
 *
 * Đòi cả kho về đúng 45–70 giây NGAY thì phải viết lại bảy kịch bản lớp 4 đang chạy
 * tốt, và cổng sẽ đỏ liên miên cho tới lúc ấy — rồi người ta tắt nó đi. Nên:
 *   · video MỚI phải nằm trong khoảng;
 *   · số video vượt khoảng CHỈ ĐƯỢC GIẢM, niêm phong đúng con số hôm nay.
 * Sửa được cái nào thì hạ `NO` xuống chốt lại.
 */
import { readdirSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const V = new URL('../public/content/toan/video/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const NGAN = 45, DAI = 70;
/* Món nợ cũ, niêm phong đúng con số ngày 16-08-2026. CHỈ ĐƯỢC GIẢM.
   Cả HAI đầu đều đã trôi, không riêng đầu dài: 16 video ngắn dưới 45 giây (ngắn
   nhất 39,4s) và 7 video dài quá 70 giây (dài nhất 77,5s). Tất cả đều của lớp 2 và
   lớp 4, đã chạy trên bản thật. Viết lại 23 kịch bản ngay bây giờ là việc khác,
   không phải việc của đợt này — nhưng để nó trôi tiếp thì không. */
const NO_DAI = 7;
const NO_NGAN = 16;

if (!existsSync(V)) {
  console.log('   (chưa có thư mục video — bỏ qua)');
  process.exit(0);
}

const tep = readdirSync(V).filter((f) => f.endsWith('.mp4'));
t(`có video để mà đo (${tep.length} tệp)`, tep.length > 50);

const giay = (f) => Number(execFileSync('ffprobe',
  ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', V + f],
  { encoding: 'utf8' }).trim());

const doDai = tep.map((f) => ({ f, s: giay(f) }));
t('đo được độ dài thật (không cái nào ra 0)', doDai.every((x) => x.s > 1));

const quaDai = doDai.filter((x) => x.s > DAI).sort((a, b) => b.s - a.s);
const quaNgan = doDai.filter((x) => x.s < NGAN).sort((a, b) => a.s - b.s);

t(`video ngắn dưới ${NGAN} giây không được nhiều hơn ${NO_NGAN} (đang ${quaNgan.length})`,
  quaNgan.length <= NO_NGAN);
if (quaNgan.length < NO_NGAN) {
  console.log(`     ↓ đã bớt: ${quaNgan.length}/${NO_NGAN} — hạ \`NO_NGAN\` xuống để chốt lại.`);
}
quaNgan.slice(0, 4).forEach((x) => console.log(`      ${x.f} · ${x.s.toFixed(1)}s`));

t(`video dài quá ${DAI} giây không được nhiều hơn ${NO_DAI} (đang ${quaDai.length})`,
  quaDai.length <= NO_DAI);
if (quaDai.length < NO_DAI) {
  console.log(`     ↓ đã bớt: ${quaDai.length}/${NO_DAI} — hạ \`NO_DAI\` xuống để chốt lại.`);
}
quaDai.slice(0, 4).forEach((x) => console.log(`      ${x.f} · ${x.s.toFixed(1)}s`));

/* Mọi video của LỚP 3 là hàng mới, không được nợ cái nào. */
const l3 = doDai.filter((x) => x.f.includes('KSN3'));
t(`lớp 3 (${l3.length} video) không cái nào vượt khoảng`,
  l3.every((x) => x.s >= NGAN && x.s <= DAI));
l3.filter((x) => x.s > DAI || x.s < NGAN)
  .forEach((x) => console.log(`      ${x.f} · ${x.s.toFixed(1)}s`));

const tong = doDai.reduce((a, x) => a + x.s, 0);
console.log(`\n   ${tep.length} video · trung bình ${(tong / tep.length).toFixed(1)}s `
  + `· dài nhất ${Math.max(...doDai.map((x) => x.s)).toFixed(1)}s `
  + `· ngắn nhất ${Math.min(...doDai.map((x) => x.s)).toFixed(1)}s\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
