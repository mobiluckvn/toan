/**
 * CỔNG · BỎ DỞ GIỮA CHẶNG THÌ KHÔNG ĐƯỢC MẤT VIỆC ĐÃ LÀM  (Lỗi B)
 * chạy: node test/tienganh_moc.test.mjs
 *
 * ── LỖI ĐÃ XẢY RA THẬT ──
 *
 * `ghiChang` chỉ nhớ ĐANG Ở CHẶNG NÀO. Trong chặng luyện tập còn ba mức, mỗi mức
 * chín câu, và toàn bộ chuyện ấy nằm trong `useState` của màn hình.
 *
 *     Làm xong 9 câu mức ★, sang mức ★★, thoát ra, vào lại
 *     → về đúng chặng luyện tập ✔
 *     → nhưng ★★ KHOÁ LẠI, và ★ về "câu 1/9 · đúng 0/0".
 *
 * Bé phải làm lại cả mức. Với bé lớp một thì bị mẹ gọi đi ăn cơm là mất một buổi.
 *
 * Không cổng nào bắt được, vì chẳng có gì hỏng: màn hình vẽ đúng, sổ ghi đúng cái
 * nó biết ghi. Chỗ thiếu là một thứ CHƯA TỪNG ĐƯỢC LƯU.
 *
 * ── PHÉP DƯỚI ĐÂY SOI GÌ ──
 *
 * ① `ghiMoc` giữ được mốc, và giữ RIÊNG theo từng chặng;
 * ② không đổi thì trả NGUYÊN KHỐI CŨ — đây là điều kiện sống còn, không phải tối
 *    ưu: vỏ gộp sổ thấy sổ đổi là vẽ lại, vẽ lại thì hàm `datTienDo` truyền xuống
 *    cũng mới, mà màn hình có effect canh chính hàm ấy để ghi mốc → vòng lặp không
 *    đáy. Đã vỡ thật một lần, xem `test/so_tien_do.test.mjs`;
 * ③ KHÔNG đụng `at` — `gopTienDo` so `at` để chọn bản thắng khi hoà sổ máy chủ;
 * ④ làm xong bài thì mốc phải BIẾN MẤT, không thì lần sau mở lại bài để ôn, bé bị
 *    thả vào giữa mức cũ thay vì được bắt đầu từ đầu;
 * ⑤ mốc KHÔNG được đẩy lên máy chủ — `luuBai` nhặt từng trường một, và `moc` cố ý
 *    không nằm trong danh sách ấy;
 * ⑥ ba màn con phải THẬT SỰ đọc và ghi mốc — soi thẳng mã nguồn, vì phần trên chỉ
 *    chứng minh cái kho chạy được chứ không chứng minh có ai dùng nó.
 */
import { readFileSync } from 'node:fs';
import {
  soRong, ghiBai, ghiChang, ghiMoc, docMoc, gopTienDo,
} from '../src/mon/tienganh/lib/progress.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const ID = 'DL:TA1.B04';
const MOC = { m: 1, xaM: 1, i: 3, dem: { dung: 7, tong: 9 }, no: ['C2'], tt: ['dung'] };

/* ── ① giữ được mốc, và giữ riêng theo chặng ── */
let p = ghiMoc(soRong(), ID, 'luyen', MOC);
t('ghi rồi đọc lại ra đúng mốc',
  JSON.stringify(docMoc(p, ID, 'luyen')) === JSON.stringify(MOC));
t('chặng chưa ghi thì đọc ra null', docMoc(p, ID, 'tu') === null);
t('bài chưa ghi thì đọc ra null', docMoc(p, 'DL:TA1.B09', 'luyen') === null);

p = ghiMoc(p, ID, 'tu', { daXem: true, daNghe: ['a'], soNoi: {}, iTu: 2 });
t('ghi chặng khác KHÔNG xoá mốc của chặng cũ',
  JSON.stringify(docMoc(p, ID, 'luyen')) === JSON.stringify(MOC));
t('và chặng mới cũng đọc ra được', docMoc(p, ID, 'tu')?.iTu === 2);

/* ── ② không đổi thì trả NGUYÊN khối cũ ── */
t('ghi lại y hệt → trả về CHÍNH sổ cũ, không dựng khối mới',
  ghiMoc(p, ID, 'luyen', MOC) === p);
t('đổi một con số thì mới dựng khối mới',
  ghiMoc(p, ID, 'luyen', { ...MOC, i: 4 }) !== p);
t('chặng rỗng thì không ghi gì', ghiMoc(p, ID, '', MOC) === p);
t('chặng undefined cũng không ghi gì', ghiMoc(p, ID, undefined, MOC) === p);

/* ── ③ không đụng `at` ──
   ⚠ ĐẶT `at` BẰNG TAY, đừng lấy `at` mà `ghiBai` vừa sinh ra. Bản đầu của phép này
   gọi `ghiBai` rồi `ghiMoc` liền nhau, hai lần `new Date().toISOString()` rơi vào
   CÙNG MỘT MILI GIÂY nên hai chuỗi bằng nhau — phép kiểm xanh kể cả khi `ghiMoc`
   có ghi đè `at` thật. Đã thử phá và nó không kêu. */
const AT_CU = '2020-01-01T00:00:00.000Z';
const cóAt = {
  ...soRong(),
  micros: { [ID]: { done: true, pass: true, best: 9, total: 9, at: AT_CU } },
};
const sauMoc = ghiMoc(cóAt, ID, 'luyen', MOC);
t('ghi mốc KHÔNG đổi `at`', sauMoc.micros[ID].at === AT_CU);
t('ghi mốc KHÔNG đụng `best`', sauMoc.micros[ID].best === 9);
t('ghi mốc KHÔNG đụng `pass`', sauMoc.micros[ID].pass === true);

/* Và `gopTienDo` phải xử đúng: bản máy chủ mới hơn thì thắng, nhưng mốc chỉ có ở
   bản tại máy nên không được kéo bản máy chủ về làm mất chỗ học dở một cách vô cớ.
   Ở đây chỉ đòi hỏi tối thiểu: gộp xong không vỡ và giữ được `best` cao nhất. */
const may = ghiMoc(ghiBai(soRong(), ID, { pass: false, dung: 4, tong: 9 }),
                   ID, 'luyen', MOC);
const chu = ghiBai(soRong(), ID, { pass: true, dung: 8, tong: 9 });
const gop = gopTienDo(may, chu);
t('gộp sổ xong vẫn giữ điểm cao nhất', gop.micros[ID].best === 8);
t('gộp sổ không làm vỡ mốc đang có',
  gop.micros[ID].moc === undefined
    || JSON.stringify(gop.micros[ID].moc.luyen) === JSON.stringify(MOC));

/* ── ④ làm xong bài thì mốc biến mất ──
   ⚠ `ghiBai` dựng khối MỚI hoàn toàn, không rải `...cu` vào, nên mốc rơi ra ngoài
   một cách tự nhiên. Phép kiểm dưới đây vì thế xanh kể cả khi xoá dòng `moc:
   undefined` — đã thử. Nó chỉ có nghĩa khi ai đó sửa `ghiBai` thành có rải `...cu`
   (một kiểu dọn mã rất dễ nghĩ ra), và lúc ấy mốc sẽ sống sót nếu thiếu dòng ấy.
   Nên giữ CẢ HAI: dòng `moc: undefined` trong `ghiBai`, và phép kiểm này. */
const xongBai = ghiBai(ghiMoc(soRong(), ID, 'luyen', MOC), ID,
                       { pass: true, dung: 9, tong: 9 });
t('làm xong bài thì XOÁ mốc', !xongBai.micros[ID].moc);
/* Và soi thẳng mã: `ghiBai` phải nói rõ ra là nó bỏ mốc đi, để lần dọn mã sau
   người ta thấy dòng ấy mà không xoá nhầm. */
const pgJs = readFileSync(
  new URL('../src/mon/tienganh/lib/progress.js', import.meta.url), 'utf8');
const thanGhiBai = pgJs.slice(pgJs.indexOf('export function ghiBai'),
                              pgJs.indexOf('export', pgJs.indexOf(
                                'export function ghiBai') + 10));
t('`ghiBai` khai rõ là bỏ mốc đi', /moc:\s*undefined/.test(thanGhiBai));
t('làm xong bài thì cũng xoá dấu chặng', xongBai.micros[ID].chang === 0);
t('`ghiChang` vẫn chạy như cũ', ghiChang(soRong(), ID, 2).micros[ID].chang === 2);

/* ── ⑤ mốc KHÔNG lên máy chủ ── */
const duLieu = readFileSync(
  new URL('../src/mon/tienganh/lib/duLieu.js', import.meta.url), 'utf8');
const thanLuuBai = duLieu.slice(duLieu.indexOf('export async function luuBai'),
                                duLieu.indexOf('export', duLieu.indexOf(
                                  'export async function luuBai') + 10));
t('`luuBai` không đẩy `moc` lên máy chủ', !/\bmoc\b/.test(thanLuuBai));
t('(và phép trên có đọc đúng thân hàm)', thanLuuBai.includes('microId'));

/* ── ⑥ ba màn con THẬT SỰ dùng mốc ──
   Phần trên chỉ chứng minh cái kho chạy được. Kho chạy được mà không màn nào gọi
   tới thì bé vẫn mất bài y như cũ — đúng cái bẫy đã dính ở chỗ khác: cổng thử đúng
   thứ mà app KHÔNG gửi. */
const bh = readFileSync(
  new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
for (const [ten, ham] of [['LuyenTap', 'function LuyenTap'],
                          ['ManTu', 'function ManTu'],
                          ['ManCau', 'function ManCau']]) {
  const i = bh.indexOf(ham);
  const j = bh.indexOf('\nfunction ', i + 10);
  const than = bh.slice(i, j < 0 ? undefined : j);
  t(`${ten} nhận mốc qua props`, /\{[^}]*\bmoc\b[^}]*\bonMoc\b/.test(than));
  /* "Có đọc mốc" = trong thân hàm có nhắc `moc` ở chỗ KHÁC cái tên `onMoc`. Đếm
     như thế thay vì khớp một khuôn `useState(...)` cụ thể: khuôn ấy đổi theo cách
     viết, còn "có dùng tới mốc hay không" thì không. */
  const nhacMoc = (than.match(/(?<!on)\bmoc\b/g) || []).length;
  t(`${ten} có ĐỌC mốc khi dựng state (${nhacMoc} chỗ nhắc)`, nhacMoc >= 2);
  t(`${ten} có GHI mốc lại`, /onMoc\?\.\(/.test(than));
}
t('BaiHoc đọc `moc` từ sổ lúc mở bài', /micros\?\.\[id\]\?\.moc/.test(bh));
t('BaiHoc truyền ba hàm ghi mốc ỔN ĐỊNH (useCallback)',
  /useCallback\(\(m\) => onMoc\?\.\('luyen', m\)/.test(bh));

const man = readFileSync(
  new URL('../src/mon/tienganh/components/ManTiengAnh.jsx', import.meta.url), 'utf8');
t('ManTiengAnh nối `onMoc` xuống BaiHoc', /onMoc=\{\(chang, m\) =>/.test(man));
t('ManTiengAnh gọi `ghiMoc`', /datTienDo\(\(p\) => ghiMoc\(/.test(man));

console.log(`\n   mốc giữ được ${Object.keys(docMoc(p, ID, 'luyen')).length} thứ `
  + `của chặng luyện tập, và ${Object.keys(docMoc(p, ID, 'tu')).length} thứ của `
  + `chặng từ mới\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
