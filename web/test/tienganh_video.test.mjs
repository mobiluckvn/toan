/**
 * VIDEO TIẾNG ANH — bài khai tệp nào thì tệp ấy phải có, dài đúng chừng ấy.
 * chạy: node test/tienganh_video.test.mjs
 *
 * ── VÌ SAO CÓ CỔNG NÀY ──
 *
 * Môn Toán có `video_toan.test.mjs` hỏi "bài khai video thì tệp có không". Tiếng
 * Anh thì KHÔNG có gì hỏi câu ấy suốt ba quyển — app đọc `bai.video.tu` rồi dựng
 * thẳng đường dẫn, tệp thiếu thì bé thấy một ô đen và một nút xám, còn `onLoi` mở
 * khoá đi tiếp nên chẳng ai biết là đã mất một bài giảng.
 *
 * Nay lại thêm chỗ lệch mới: từ 18-08 video từ mới TÁCH THEO NHÓM NGHĨA, và tên
 * tệp do `sinh_bai_tienganh.py` đặt còn tệp thì do `dung_video.py` đẻ ra. HAI CHỖ
 * cùng tính một cái tên là sớm muộn lệch — mà lệch kiểu này im lặng tuyệt đối.
 *
 * ── BỐN CÂU HỎI ──
 *   1. bài khai tệp nào cũng có thật (và ngược lại: không tệp nào mồ côi)
 *   2. nhóm nghĩa khớp HAI CHIỀU với `vocabulary` — không từ nào rơi ra ngoài,
 *      không nhóm nào khai một từ bài không dạy
 *   3. video từ mới dài trong khoảng bé ngồi được
 *   4. video mẫu câu: món nợ cũ chỉ được GIẢM
 *
 * ⚠ Phép 1 CHỐT SỐ TỆP trước khi soi. Glob rỗng thì mọi vòng lặp chạy 0 lần và
 * cổng xanh trơn — cái bẫy đã sập một lần ở đợt hình lớp 1.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';

const R = new URL('../../', import.meta.url).pathname;
const V = join(R, 'web/public/content/tienganh/video');
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const quyens = ['ta1', 'ta2', 'ta3'].filter((q) => existsSync(join(R, 'web/public/content', q)));
if (!quyens.length || !existsSync(V)) {
  console.log('   ⏸ chưa có bài hoặc chưa có thư mục video');
  console.log('\n0 PASS · 0 FAIL');
  process.exit(0);
}

/* ── gom mọi tệp bài khai ── */
const khai = new Map();      // tên tệp → { bai, loai }
const bais = [];
for (const q of quyens) {
  const tm = join(R, 'web/public/content', q);
  for (const f of readdirSync(tm).filter((x) => /^DL_.*\.json$/.test(x)).sort()) {
    const b = JSON.parse(readFileSync(join(tm, f), 'utf8'));
    bais.push({ q, f, b });
    for (const g of (b.video?.tu || [])) khai.set(g.tep, { bai: f, loai: 'tu', g });
    for (const c of (b.video?.cau || [])) khai.set(c.tep, { bai: f, loai: 'cau' });
  }
}
const tep = readdirSync(V).filter((f) => f.endsWith('.mp4'));
t(`đếm được bài và video trước khi soi (${bais.length} bài · ${tep.length} mp4 · `
  + `${khai.size} tệp bài khai)`, bais.length > 40 && tep.length > 40 && khai.size > 40);

/* ══ 1 · KHAI GÌ CÓ NẤY, VÀ NGƯỢC LẠI ══ */
const coTep = new Set(tep);
const thieu = [...khai.keys()].filter((x) => !coTep.has(x));
t(`mọi video bài khai đều có tệp thật (thiếu ${thieu.length})`, !thieu.length);
in5(thieu);

const moCoi = tep.filter((x) => !khai.has(x));
t(`không video nào mồ côi — dựng ra mà không bài nào dùng (${moCoi.length})`, !moCoi.length);
in5(moCoi);

/* ══ 2 · NHÓM NGHĨA KHỚP HAI CHIỀU VỚI TỪ CỦA BÀI ══
   Nhóm khai thiếu một từ thì từ ấy không video nào dạy, mà thanh VIỆC CỦA CON vẫn
   đủ ô nên nhìn không ra. Nhóm khai thừa thì video gọi một từ bài không có, và
   `kich_ban.py` dừng — nhưng chỉ dừng lúc DỰNG, tức là sau khi đã sai từ lâu. */
const lechNhom = [], nhomXau = [];
for (const { f, b } of bais) {
  const nhom = b.video?.tu || [];
  if (!Array.isArray(nhom)) { nhomXau.push(`${f}: video.tu không phải danh sách`); continue; }
  if (!nhom.length) { nhomXau.push(`${f}: không nhóm video từ mới nào`); continue; }
  for (const g of nhom) {
    if (!g.ma || !g.ten || !g.tep) nhomXau.push(`${f}: nhóm thiếu ma/ten/tep`);
    if (!(g.tu || []).length) nhomXau.push(`${f}/${g.ma}: nhóm rỗng từ`);
    if (!String(g.tep).startsWith(f.replace('.json', '')))
      nhomXau.push(`${f}/${g.ma}: tên tệp ${g.tep} không mang mã bài`);
  }
  const trong = nhom.flatMap((g) => g.tu || []);
  const day = (b.knowledgeCore?.vocabulary || []).map((v) => v.tu);
  const roi = day.filter((x) => !trong.includes(x));
  const thua = trong.filter((x) => !day.includes(x));
  const trung = trong.filter((x, i) => trong.indexOf(x) !== i);
  if (roi.length || thua.length || trung.length) {
    lechNhom.push(`${f}: rơi ngoài nhóm [${roi}] · thừa [${thua}] · trùng [${trung}]`);
  }
}
t(`nhóm nghĩa khai đủ hình dạng (${nhomXau.length} chỗ hỏng)`, !nhomXau.length);
in5(nhomXau);
t(`mọi từ của bài nằm trong ĐÚNG một nhóm video (${lechNhom.length} bài lệch)`, !lechNhom.length);
in5(lechNhom);

/* ══ 3 · DÀI BAO LÂU ══ */
const giay = (f) => Number(execFileSync('ffprobe',
  ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', join(V, f)],
  { encoding: 'utf8' }).trim());
const doDai = tep.map((f) => ({ f, s: giay(f), loai: khai.get(f)?.loai }));
t('đo được độ dài thật (không cái nào ra 0)', doDai.every((x) => x.s > 1));

/* Video TỪ MỚI: đo thật là ≈4 giây một từ, cộng phần khung.
     · nhóm ĐẦU của bài còn cõng bìa và cảnh "chữ hôm nay" — thêm ~15 giây;
     · nhóm sau chỉ có một câu dẫn — thêm ~4 giây.
   Nên tệp ngắn nhất (3 từ, nhóm sau) là ~14 giây, dài nhất (8 từ, nhóm đầu) ~50.
   Trần 50 chính là lý do cả việc tách nhóm tồn tại — nới nó ra là bỏ luôn việc vừa
   làm. Sàn 12 để chặn nhóm một từ: một video tám giây thì không phải bài giảng. */
const NGAN_TU = 12, DAI_TU = 50;
const tuXau = doDai.filter((x) => x.loai === 'tu' && (x.s < NGAN_TU || x.s > DAI_TU));
t(`video TỪ MỚI đều nằm trong ${NGAN_TU}–${DAI_TU} giây (${tuXau.length} cái lệch)`,
  !tuXau.length);
in5(tuXau.map((x) => `${x.f} · ${x.s.toFixed(1)}s`));

/* ── VIDEO MẪU CÂU: MÓN NỢ CÓ THẬT, NIÊM PHONG CHỨ KHÔNG GIẢ VỜ SẠCH ──
 *
 * Khuôn video mẫu câu (tách mẩu → ba câu cùng khuôn → tập nói ba tốc độ có khoảng
 * lặng → chỗ dễ nhầm) dài 50 tới 100 giây, và nó dùng chung cho cả ba quyển. Đợt
 * 18-08 chỉ tách VIDEO TỪ MỚI; viết lại 82 kịch bản mẫu câu là việc khác.
 *
 * Con số dưới đây là ảnh chụp hôm nay và CHỈ ĐƯỢC GIẢM. Đặt ngưỡng "lớp 3 phải
 * sạch" thì cổng đỏ liên miên vì một việc chưa ai nhận làm — rồi người ta tắt nó
 * đi, và mất luôn cả phần đang canh được. Ghi đúng món nợ vẫn hơn.
 */
const DAI_CAU = 70;
const NO_CAU = 31;   // chốt lại 18-08: đang 31, đừng để bò lên nữa
const TRAN_CAU = 100;
const cauDai = doDai.filter((x) => x.loai === 'cau' && x.s > DAI_CAU)
  .sort((a, b) => b.s - a.s);
t(`video mẫu câu quá ${DAI_CAU} giây không nhiều hơn ${NO_CAU} (đang ${cauDai.length})`,
  cauDai.length <= NO_CAU);
if (cauDai.length < NO_CAU) {
  console.log(`     ↓ đã bớt: ${cauDai.length}/${NO_CAU} — hạ \`NO_CAU\` xuống để chốt lại.`);
}
in5(cauDai.map((x) => `${x.f} · ${x.s.toFixed(1)}s`));

const quaTran = doDai.filter((x) => x.s > TRAN_CAU);
t(`không video nào vượt trần cứng ${TRAN_CAU} giây (${quaTran.length})`, !quaTran.length);
in5(quaTran.map((x) => `${x.f} · ${x.s.toFixed(1)}s`));

const tong = doDai.reduce((a, x) => a + x.s, 0);
console.log(`\n   ${tep.length} video · ${(tong / 60).toFixed(1)} phút · `
  + `từ mới ${doDai.filter((x) => x.loai === 'tu').length} `
  + `· mẫu câu ${doDai.filter((x) => x.loai === 'cau').length}\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
