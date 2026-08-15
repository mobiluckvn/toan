/* ═══════════ LỜI CHÀO PHẢI NÓI VỀ CHÍNH BÀI ẤY ═══════════
 * chạy: node test/loi_chao_dung_bai.test.mjs
 *
 * ── HAI LỖI ĐÃ XẢY RA THẬT, CÙNG MỘT NGÀY ──
 *
 * Lời chào viết tay ở `data/loi_chao.json`, khoá là mã bài. Khi một bài chữ tách
 * thành mấy bài video, NỘI DUNG bài đổi hết mà lời chào thì giữ nguyên khoá cũ —
 * và không có gì kêu, vì lời chào vẫn còn, vẫn ngắn, vẫn kết bằng câu rủ.
 *
 *   · B10 nay dạy DÃY GẤP ĐÔI 1, 2, 4, 8. Lời chào vẫn mời bé đoán tiếp dãy
 *     2, 3, 5, 8, 12 — dãy ấy nay là của B44, bài BẬC THANG. Bé mở bài ra, đọc lời
 *     chào về một dãy, rồi xem video về một dãy khác hẳn.
 *   · B11 nay chỉ dạy nhìn chữ số tận cùng. Lời chào vẫn hỏi "26 cộng 13 chẵn hay
 *     lẻ" — đúng câu của B47, bài đứng sau nó hai bài. Lại còn nhắc tên nhân vật,
 *     thứ bác đã bảo bỏ hẳn khỏi mọi bài dùng video.
 *
 * Cổng `loi_chao.test.mjs` cũ soi HÌNH DẠNG của lời chào: có hay không, dài bao
 * nhiêu, mấy câu, có chữ nghề không. Cả bốn phép ấy đều xanh với hai lời chào trên,
 * vì chúng hỏng ở chỗ NỘI DUNG chứ không hỏng ở hình dạng.
 *
 * ── HAI PHÉP DƯỚI ĐÂY SOI NỘI DUNG, BẰNG THỨ MÁY ĐẾM ĐƯỢC ──
 *
 * ① Mọi CON SỐ trong lời chào phải có mặt đâu đó trong bài.
 * ② Mọi DÃY SỐ trong lời chào (từ ba số trở lên) phải có mặt NGUYÊN VẸN trong bài.
 *
 * Phép ② mạnh hơn phép ①: các số 2, 3, 5, 8, 12 của B10 đều lẻ tẻ có trong bài nên
 * phép ① tha, nhưng cả dãy liền nhau thì không.
 *
 * NGƯỠNG ĐẶT Ở ĐÚNG CHỖ DỮ LIỆU ĐANG ĐỨNG: đo trên toàn bộ 120 bài video của lớp 2
 * và lớp 4, cả hai phép đều 0 chỗ lệch sau khi sửa hai lời chào trên. Nên đòi 0, và
 * từ nay chỉ được siết thêm.
 *
 * ⚠ Chỉ soi bài DÙNG VIDEO. Bài chữ giữ nguyên lời mở bài của sách, trong đó có câu
 * chuyện dẫn nhắc tới đồ vật và con số không thuộc phần toán — soi vào là báo oan.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
const ND = join(G, 'web/public/content');

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (ds) => ds.slice(0, 5).forEach((x) => console.log('     ', x));

/* Lớp 4 viết dãy bằng dấu chấm phẩy ("5 ; 10 ; 15"), lời chào thì viết bằng dấu
   phẩy. Không quy về một dạng thì phép ② báo oan đúng năm bài — đã đo thật. */
const phang = (s) => String(s).replace(/\s+/g, '').replace(/;/g, ',');
const SO = /(?<!\d)\d+(?!\d)/g;
const DAY = /\d+(?:\s*[,;]\s*\d+){2,}/g;

const QUYEN = ['lop2', 'lop3', 'lop4'].filter((q) => existsSync(join(ND, q)));

let tongVideo = 0, tongNeuDay = 0;
for (const q of QUYEN) {
  const bai = readdirSync(join(ND, q))
    .filter((f) => /^DL_KSN\d+_B\d+\.json$/.test(f))
    .map((f) => JSON.parse(readFileSync(join(ND, q, f), 'utf8')))
    .filter((b) => b.video?.giang);
  if (!bai.length) continue;
  tongVideo += bai.length;

  const than = (b) => {
    const { objective, ...con } = b;      // bỏ chính lời chào ra, không tự soi mình
    return JSON.stringify(con);
  };

  /* ① con số lẻ. */
  const lacSo = [];
  for (const b of bai) {
    const chao = b.objective?.kidText || '';
    const co = new Set(than(b).match(SO) || []);
    const thieu = [...new Set(chao.match(SO) || [])].filter((x) => !co.has(x));
    if (thieu.length) lacSo.push(`${b.id}: số ${thieu.join(', ')} — "${chao.slice(0, 54)}…"`);
  }
  t(`${q} · mọi số trong lời chào đều có trong bài (${bai.length} bài video)`,
    lacSo.length === 0);
  in5(lacSo);

  /* ② cả dãy. */
  const lacDay = [];
  for (const b of bai) {
    const chao = b.objective?.kidText || '';
    const day = chao.match(DAY) || [];
    if (day.length) tongNeuDay++;
    const co = phang(than(b));
    const lac = day.filter((d) => !co.includes(phang(d)));
    if (lac.length) lacDay.push(`${b.id}: dãy "${lac.join(' · ')}" không có trong bài`);
  }
  t(`${q} · mọi dãy số trong lời chào đều có trong bài`, lacDay.length === 0);
  in5(lacDay);

  /* ③ Bài dùng video thì KHÔNG nhân vật — video đã bỏ hẳn, lời chào cũng phải bỏ.
     Đây là chỗ B11 lộ ra: lời chào cũ còn nguyên tên nhân vật của sách. */
  const VO = /(Su Kem|Trí Long)/i;
  const conVo = bai.filter((b) => VO.test(b.objective?.kidText || ''))
    .map((b) => `${b.id}: "${VO.exec(b.objective.kidText)[0]}"`);
  t(`${q} · lời chào bài video không nhắc tên nhân vật`, conVo.length === 0);
  in5(conVo);
}

t(`có bài video để mà soi (${tongVideo})`, tongVideo > 0);
t(`có lời chào nêu dãy số để phép ② làm việc (${tongNeuDay})`, tongNeuDay > 0);

console.log(`\n   ${QUYEN.length} quyển · ${tongVideo} bài video · `
  + `${tongNeuDay} lời chào có nêu dãy số\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
