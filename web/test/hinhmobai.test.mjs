/**
 * Kiểm 168 HÌNH MỞ BÀI — chạy: node test/hinhmobai.test.mjs
 *
 * Hình mở bài là một đoạn ĐỐI THOẠI: Trí Long (hoặc Cáo Đề) nói cái sai mà trẻ hay
 * mắc, Su Kem hích nhẹ để bạn tự nhận ra. Con mở bài ra là phải đọc hiểu ngay.
 *
 * Bộ sinh figureSpec ngày trước dùng regex bắt lời thoại trong ngoặc kép. Regex ấy
 * hỏng theo bốn kiểu, đều làm hình không đọc được:
 *   1. bong bóng RỖNG — Su Kem đứng im, khung trắng trơ ra
 *   2. bong bóng nuốt CẢ LỜI DẪN — Trí Long "nói" luôn cả đoạn kể về Su Kem
 *   3. lời thoại bị CẮT CỤT ngay dấu ngoặc — 'Su Kem: 100" cho số 3,5.'
 *   4. gán NHẦM NHÂN VẬT — Su Bống đọc lời chỉ dẫn sân khấu
 * Bốn phép kiểm dưới đây khoá cả bốn kiểu lại.
 *
 * Giới hạn đã biết: phép kiểm (2) chỉ bắt được đoạn cắt NGUYÊN SI từ lời dẫn — đúng
 * dấu vết mà bộ sinh để lại. Người viết tay một câu kể lể tự chế thì nó không bắt.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const LESSONS = new URL('../public/content/lessons/', import.meta.url).pathname;
const FIGURES = new URL('../public/content/figures/', import.meta.url).pathname;
const MANIFEST = new URL('../../data/figure_manifest.json', import.meta.url).pathname;

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const NHAN_VAT = ['Su Kem', 'Trí Long', 'Cáo Đề', 'Su Bống', 'sư phụ'];
const TOI_DA = 130;   // dài hơn thì tràn bong bóng, con phải căng mắt đọc
const gon = (s) => String(s ?? '').split(/\s+/).join(' ').trim();

const bai = readdirSync(LESSONS).filter((f) => f.endsWith('.json'))
  .map((f) => JSON.parse(readFileSync(join(LESSONS, f), 'utf8')));
const manifest = JSON.parse(readFileSync(MANIFEST, 'utf8'));

t('đọc đủ 168 bài', bai.length === 168);

const rong = [], daiQua = [], nuot = [], cut = [], moiMot = [], saiVai = [], shaLech = [];

for (const j of bai) {
  const mid = j.id.replace('DL:KSN5Q1.', '');
  const dan = gon(j.lecture?.screens?.[0]?.narration);

  for (const s of j.figureSpec ?? []) {
    /* mã kiểm trong bài và trong manifest phải khớp PNG THẬT — nếu không, sửa lời
       thoại xong mà quên vẽ lại thì con vẫn xem hình cũ. */
    const png = `${j.id.replace('DL:', '').replace(/\./g, '_')}_${s.id}.png`;
    const that = createHash('sha256').update(readFileSync(join(FIGURES, png))).digest('hex').slice(0, 16);
    if (s.sha256_16 && s.sha256_16 !== that) shaLech.push(`${mid}#${s.id} (bài)`);
    if (manifest[`${j.id}#${s.id}`]?.sha256_16 !== that) shaLech.push(`${mid}#${s.id} (manifest)`);

    if (s.archetype !== 'character_speech') continue;

    const lines = s.params?.lines ?? [];
    if (lines.length < 2) moiMot.push(mid);

    for (const [i, L] of lines.entries()) {
      const say = gon(L.say), who = L.who;
      const o = `${mid}[${i}]`;

      if (!say) { rong.push(o); continue; }
      if (say.length > TOI_DA) daiQua.push(`${o} ${say.length} ký tự`);

      // (2) kể về nhân vật KHÁC ở ngôi thứ ba, cắt nguyên si từ lời dẫn → là lời kể
      if (say.length > 50 && dan.includes(say)
          && NHAN_VAT.some((c) => c !== who && say.includes(c))) nuot.push(o);

      // (3) lẻ dấu ngoặc = câu bị xén giữa chừng
      const le = (ch) => (say.split(ch).length - 1) % 2 === 1;
      if (le('"') || le("'") || say.split('“').length !== say.split('”').length) cut.push(`${o} ${say.slice(0, 40)}`);

      // (4) Su Kem là người GỠ — không bao giờ bị tô đỏ như kẻ mắc bẫy
      if (who === 'Su Kem' && L.tone === 'wrong') saiVai.push(`${o} Su Kem mà tone=wrong`);
    }

    /* Màu bong bóng dạy con ai đúng ai sai TRƯỚC khi đọc chữ. Lời gỡ (xanh) phải
       đứng SAU cái sai (đỏ) — đảo lại là tô xanh cho chính câu sai. Bài mở đầu cố ý
       để ngỏ "con theo phe nào?" nên cả hai bong bóng đều 'normal', không tính. */
    const tones = lines.map((L) => L.tone);
    const doDau = tones.indexOf('wrong'), xanhDau = tones.indexOf('right');
    if (doDau >= 0 && xanhDau >= 0 && xanhDau < doDau) {
      saiVai.push(`${mid} lời gỡ (xanh) đứng TRƯỚC cái sai (đỏ)`);
    }
  }
}

t(`không bong bóng nào rỗng (${rong.length})`, rong.length === 0);
t(`mọi hình đều có đủ hai bong bóng (${moiMot.length})`, moiMot.length === 0);
t(`không lời thoại nào quá ${TOI_DA} ký tự (${daiQua.length})`, daiQua.length === 0);
t(`không bong bóng nào nuốt cả lời dẫn (${nuot.length})`, nuot.length === 0);
t(`không lời thoại nào bị cắt cụt ở dấu ngoặc (${cut.length})`, cut.length === 0);
t(`không hình nào gán nhầm vai nhân vật (${saiVai.length})`, saiVai.length === 0);
t(`mã kiểm hình khớp PNG thật (${shaLech.length})`, shaLech.length === 0);

for (const [ten, ds] of [['rỗng', rong], ['một bong bóng', moiMot], ['dài quá', daiQua],
                         ['nuốt lời dẫn', nuot], ['cắt cụt', cut], ['sai vai', saiVai],
                         ['sha lệch', shaLech]]) {
  if (ds.length) console.log(`    ${ten}:`, ds.slice(0, 8).join(' · '), ds.length > 8 ? `… +${ds.length - 8}` : '');
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
