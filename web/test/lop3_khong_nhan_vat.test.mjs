/* ═══════════ LỚP 3 KHÔNG CÒN NHÂN VẬT THƯƠNG HIỆU ═══════════
 * chạy: node test/lop3_khong_nhan_vat.test.mjs
 *
 * Bác chốt 16-08-2026: bỏ hẳn Su Kem · Su Bống · Trí Long khỏi quyển lớp 3, cho
 * bốn quyển một giọng. 267 chỗ trong bản dựng, 34 bài.
 *
 * ── BA CỬA SAU TÊN ĐÃ CHUI VỀ ──
 *
 * Dọn xong lời văn rồi quét lại vẫn thấy tên. Ba lần, ba cửa khác nhau, và không
 * cửa nào tìm ra được bằng `grep "Trí Long"` trong tệp đích:
 *
 *   ① TIÊU ĐỀ MỤC · 34 chỗ. `khuon_chung.py` SUY dòng dấu hiệu từ tiêu đề mục
 *      'TRÍ LONG ƠI, NHẦM RỒI!' → 'Bé làm theo cách Trí Long vừa nói.' Tiêu đề
 *      viết HOA nên mọi phép thay theo chữ thường đều trượt qua.
 *   ② LỜI CHÀO · 3 chỗ. `data/loi_chao.json` giữ lời chào của CẢ BỐN quyển trong
 *      một tệp phẳng, nằm ngoài `data/lop3/` nên phép dọn theo thư mục không với
 *      tới — mà đó lại là dòng ĐẦU TIÊN bé đọc khi mở bài.
 *   ③ PHỤ ĐỀ QUYỂN · 2 chỗ. `dung_khuon_chung_lop3.py` ghim cứng phụ đề rồi GHI ĐÈ
 *      `chuong_trinh.json` mỗi lần chạy. Bộ dọn báo "2 phụ đề đã đổi" xong, chạy
 *      bộ dựng một phát là tên quay về — bộ dọn vẫn xanh, vẫn báo đã làm.
 *
 * Nên phép dưới đây soi BẢN DỰNG — thứ bé thật sự đọc — chứ không soi bản gốc.
 * Bản gốc sạch mà bản dựng bẩn là chuyện đã xảy ra ba lần trong một buổi.
 *
 * `data/lop3_tho.json` (316 chỗ) CỐ Ý giữ nguyên văn sách để còn đối chiếu với
 * sách giấy — nó không đi vào app, và `chuan_lop3.py` gọi `bo_nhan_vat_lop3.py` ở
 * bước cuối nên dựng lại vẫn sạch. Có phép canh đúng chuyện ấy ở dưới.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const NHAN_VAT = ['Su Kem', 'Su Bống', 'Trí Long', 'Cáo Đề'];
const co = (s) => NHAN_VAT.filter((n) => s.includes(n));

/* ── ① bài học ── */
const thu = join(G, 'web/public/content/lop3');
const bai = readdirSync(thu).filter((f) => /^DL_KSN3_B.*\.json$/.test(f));
t(`đọc được ${bai.length} bài lớp 3`, bai.length === 34);

let ban = 0;
const cho = [];
for (const f of bai) {
  const s = readFileSync(join(thu, f), 'utf8');
  const thay = co(s);
  if (thay.length) { ban += 1; cho.push(`${f} · ${thay.join(', ')}`); }
}
t(`không bài nào còn nhân vật (${ban} bài còn)`, ban === 0);
cho.slice(0, 5).forEach((x) => console.log('     ', x));

/* ── ② kỳ ôn tập và ải ── */
const rv = join(G, 'web/public/content/reviews');
const kyL3 = readdirSync(rv).filter((f) => /^DCR_KSN3_/.test(f));
t(`đọc được ${kyL3.length} kỳ của lớp 3`, kyL3.length === 11);
t('không kỳ nào còn nhân vật',
  kyL3.every((f) => !co(readFileSync(join(rv, f), 'utf8')).length));

/* ── ③ phụ đề quyển · CẢ HAI NƠI ──
   Bản dựng là thứ app đọc, nhưng bản gốc mới là thứ lần dựng sau lấy làm nguồn.
   Sạch một nơi thôi thì lần chạy sau bẩn lại. */
for (const p of ['data/chuong_trinh.json', 'web/public/content/chuong_trinh.json']) {
  const s = readFileSync(join(G, p), 'utf8');
  const l3 = s.slice(s.indexOf('"ma": "lop3"'), s.indexOf('"ma": "lop3"') + 400);
  t(`${p} · khối lớp 3 không còn nhân vật`, !co(l3).length);
}

/* ── ④ lời chào · chỉ khoá lớp 3 ──
   Tệp dùng chung bốn quyển. Lớp 3 và lớp 5 VẪN giữ nhân vật của mình, nên phép
   này phải lọc theo mã bài — đòi cả tệp sạch là bắt dọn nhầm sang quyển khác. */
const lc = JSON.parse(readFileSync(join(G, 'data/loi_chao.json'), 'utf8'));
const khoaL3 = Object.keys(lc).filter((k) => k.startsWith('DL:KSN3.'));
t(`có lời chào lớp 3 để mà soi (${khoaL3.length} lời)`, khoaL3.length > 0);
t('lời chào lớp 3 không còn nhân vật',
  khoaL3.every((k) => !co(String(lc[k])).length));
/* Đảo chiều: phải chứng minh mình dọn ĐÚNG QUYỂN, chứ không quét sạch cả kho.
   ⚠ Đừng lấy chính `loi_chao.json` làm đối chứng — bản đầu của phép này làm thế và
   ĐỎ OAN: tệp ấy chỉ chứa lời chào của lớp 2·3·4, mà lớp 2 và lớp 4 đã bỏ nhân vật
   từ trước. Đối chứng thật nằm ở lớp 5 Quyển 1: quyển ấy VẪN giữ Su Kem · Su Bống,
   và không đợt dọn nào được phép đụng vào. */
const l5 = join(G, 'web/public/content/lessons');
const tepL5 = readdirSync(l5).filter((f) => /^DL_.*\.json$/.test(f));
const conL5 = tepL5.filter((f) => co(readFileSync(join(l5, f), 'utf8')).length).length;
t(`(đối chứng) lớp 5 VẪN giữ nhân vật của mình (${conL5} bài)`, conL5 > 0);

/* ── ⑤ ba cửa sau, soi thẳng vào mã ── */
const bnv = readFileSync(join(G, 'tools/bo_nhan_vat_lop3.py'), 'utf8');
t('bộ dọn có xử TIÊU ĐỀ MỤC (cửa ①)', /muc\.suKemNham\.ten/.test(bnv));
t('bộ dọn có xử LỜI CHÀO (cửa ②)', /loi_chao\.json/.test(bnv));
const dkc = readFileSync(join(G, 'tools/dung_khuon_chung_lop3.py'), 'utf8');
t('bộ dựng KHÔNG còn ghim cứng phụ đề cũ (cửa ③)',
  !co(dkc.slice(dkc.indexOf('KHAI_SO'), dkc.indexOf('KHAI_SO') + 900)).length);

/* ── ⑥ chạy lại dây chuyền vẫn sạch ──
   `lop3_tho.json` giữ nguyên văn sách, nên `chuan_lop3.py` dựng lại là nhân vật về
   đủ 267 chỗ. Nó chỉ sạch vì bước dọn được gọi ở CUỐI bộ ấy. Mất lời gọi đó thì
   không gì kêu cho tới lần dựng sau — mà lần ấy thường cách đây vài tháng. */
const chuan = readFileSync(join(G, 'tools/chuan_lop3.py'), 'utf8');
t('`chuan_lop3.py` có gọi bộ dọn ở bước cuối',
  /import bo_nhan_vat_lop3/.test(chuan) && /bo_nhan_vat_lop3\.main\(/.test(chuan));
const tho = join(G, 'data/lop3_tho.json');
t('(đối chứng) bản trích thô VẪN giữ nguyên văn sách',
  existsSync(tho) && co(readFileSync(tho, 'utf8')).length > 0);

console.log(`\n   ${bai.length} bài · ${kyL3.length} kỳ · ${khoaL3.length} lời chào `
  + '· không còn Su Kem · Su Bống · Trí Long\n');
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
