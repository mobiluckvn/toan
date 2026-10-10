/**
 * CỔNG MÀN NHÀ — bốn quyển một trải nghiệm, và mọi màn đều có đường về.
 * chạy: node test/mannha.test.mjs
 *
 * Hai thứ phép kiểm này canh, và cả hai đều thuộc loại HỎNG CÂM:
 *
 *  1. TRANG CHÍNH CỦA QUYỂN PHẢI DÙNG CHUNG MỘT TỆP. Trước đây có hai (`Home.jsx`
 *     cho lớp 5, `HomeLop2.jsx` cho lớp 2·3·4), nên mỗi lần sửa phải làm hai lần —
 *     và quên một lần thì hai quyển lệch nhau mà chẳng có gì báo. Tệp chung ấy cũng
 *     không được gõ cứng con số của riêng lớp 5 (14 chương · 12 bài mỗi chương ·
 *     tiền tố `DL:KSN5Q1.`): gõ cứng thì mở lớp 4 ra là ba chương ma hiện lên.
 *
 *  2. MỌI MÀN GỐC PHẢI CÓ ĐƯỜNG VỀ KỆ SÁCH. Màn chủ đề không thuộc quyển nào, vòng
 *     luyện vào được từ đó, Mùa giải vào được từ hai lối — đi sâu ba tầng mà chỉ có
 *     nút "lùi một bước" thì bé phải bấm ba lần mới ra. Đọc MÃ NGUỒN chứ không đọc
 *     dữ liệu: máy khẳng định được điều này, đừng để nó cho mắt người.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../src/', import.meta.url).pathname;
const APP = readFileSync(new URL('../src/App.jsx', import.meta.url).pathname, 'utf8');

/* Giao diện nay nằm hai cây: `chung/components` (tầng vỏ) và `mon/<môn>/components`.
   Quét đệ quy rồi tra theo TÊN TỆP — phép kiểm này quan tâm màn nào có mặt và nó
   viết gì, không quan tâm nó ngồi ở thư mục nào. */
function quet(thuMuc, ra = {}) {
  for (const x of readdirSync(thuMuc, { withFileTypes: true })) {
    const p = join(thuMuc, x.name);
    if (x.isDirectory()) quet(p, ra);
    else if (x.name.endsWith('.jsx')) ra[x.name] = p;
  }
  return ra;
}
const DUONG = quet(G);
const doc = (f) => readFileSync(DUONG[f] || join(G, f), 'utf8');
/* Bỏ chú thích trước khi soi: mọi thứ dưới đây được phép NHẮC TỚI trong lời ghi —
   cái cấm là dùng chúng để dựng màn hình. Soi cả chú thích thì phép kiểm báo oan,
   mà phép kiểm báo oan là phép kiểm bị bỏ qua. */
const boGhi = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
const APP_MA = boGhi(APP);
const MT = boGhi(doc('ManToan.jsx'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ══ 1 · MỘT TRANG CHÍNH CHO CẢ BỐN QUYỂN ══ */
const ds = Object.keys(DUONG);
t('có HomeQuyen.jsx — trang chính dùng chung', ds.includes('HomeQuyen.jsx'));
for (const cu of ['Home.jsx', 'HomeLop2.jsx']) {
  t(`không còn ${cu} (đã gộp vào HomeQuyen)`, !ds.includes(cu));
}
t('App không còn rẽ đôi theo nhịp đọc để chọn trang chính',
  !/nhipDocCham\(chuongTrinh\)/.test(APP_MA));
/* Từ khi tách hai môn, VỎ không dựng trang chính nữa — nó giao cho môn. Trang chính
   của quyển do `mon/toan/components/ManToan.jsx` dựng. Đây là điều đáng canh hơn:
   vỏ mà dựng thẳng HomeQuyen thì "tách" chỉ là tách thư mục. */
t('vỏ giao màn cho môn, không tự dựng trang chính',
  /<Man\b/.test(APP_MA) && !/<HomeQuyen/.test(APP_MA));
t('môn Toán dựng trang chính bằng HomeQuyen', /<HomeQuyen/.test(MT));

const HQ = doc('HomeQuyen.jsx');
const HQ_MA = boGhi(HQ);
const CAM = [
  [/length:\s*14/, 'gõ cứng 14 chương'],
  [/\/\s*12\b/, 'gõ cứng 12 bài mỗi chương'],
  [/DL:KSN5Q1\./, 'gõ cứng tiền tố mã bài lớp 5'],
  [/Toán Tư Duy lớp \d/, 'gõ cứng tên quyển'],
  [/===\s*'lop[2345]'/, 'so tên quyển thay vì hỏi cờ trong sổ đăng ký'],
  [/CHAPTER_NAMES|const CHUONG_NAMES/, 'bảng tên chương gõ cứng trong giao diện'],
];
for (const [re, viSao] of CAM) t(`HomeQuyen không ${viSao}`, !re.test(HQ_MA));
t('HomeQuyen hỏi cờ khoá bài từ sổ đăng ký', /ct\.khoaBai/.test(HQ));
t('HomeQuyen hỏi cờ quyển luyện thi từ sổ đăng ký', /ct\.quyen2/.test(HQ));
t('HomeQuyen dựng chỉ mục bằng napChiMuc', /napChiMuc/.test(HQ));

/* Bài đề xuất RIÊNG cho từng chương — thứ ba quyển đọc chậm chưa từng có. */
t('HomeQuyen hiện bài đề xuất của từng chương', /c\.deXuat/.test(HQ));
t('phép đếm nằm ở lib/hocba.js, không viết lại trong màn hình',
  /from '\.\.\/lib\/hocba\.js'/.test(HQ));

/* ══ 2 · ĐƯỜNG VỀ KỆ SÁCH ══ */
t('có ThanhTren.jsx — đầu trang dùng chung', ds.includes('ThanhTren.jsx'));

/* Màn GỐC: đứng ở đây mà không có nút nhà thì bé mắc kẹt. KeSach chính là nhà nên
   không cần, các màn trong phòng học có nút Thoát riêng theo mạch bài. */
const GOC = {
  'HomeQuyen.jsx': /onVeKeSach/,
  'ChuDe.jsx': /onVeNha/,
  'LuyenChuDe.jsx': /onVeNha/,
  'MuaGiai.jsx': /onVeKeSach/,
};
for (const [f, re] of Object.entries(GOC)) {
  t(`${f} nhận cửa về kệ sách`, !!DUONG[f] && re.test(doc(f)));
}
/* App phải THẬT SỰ truyền cửa ấy xuống — nhận mà không ai truyền thì nút biến mất
   trong im lặng, đúng kiểu hỏng chỉ lộ khi mở mắt xem. */
t('vỏ chuyền cửa về kệ sách xuống môn', APP_MA.includes('veKeSach={veKeSach}'));
for (const p of ['onVeKeSach={veKeSach}', 'onVeNha={veKeSach}']) {
  t(`ManToan truyền ${p}`, MT.includes(p));
}
t('ManToan truyền cửa về kệ sách cho Mùa giải',
  /<MuaGiai[\s\S]{0,600}?onVeKeSach=\{veKeSach\}/.test(MT));

/* Màn chủ đề: cả ba tầng phải cùng một đầu trang, không tầng nào tự vẽ lấy. */
const CD = doc('ChuDe.jsx');
t('ChuDe không còn tự vẽ đầu trang riêng', !/<header className="bg-navy/.test(boGhi(CD)));
t('ChuDe dùng ThanhTren', /<ThanhTren/.test(CD));

/* ══ 3 · SỔ BỐ MẸ VÀ BẢNG CÔ GIÁO NHÌN ĐƯỢC CẢ BỐN QUYỂN ══ */
const PR = doc('ParentReport.jsx');
/* Sổ bố mẹ nay HỎI MÔN thay vì tự đếm — đó là điều làm nó vẽ được môn thứ hai mà
   không phải viết lại. Canh đúng chỗ ấy, đừng canh cách nó tự tính. */
t('sổ bố mẹ hỏi học bạ của môn', /\bm\?\.hocBa\(/.test(PR));
t('sổ bố mẹ có trục theo lớp và trục theo chủ đề',
  /'lop'/.test(PR) && /'chude'/.test(PR));
t('sổ bố mẹ không còn chia cứng cho 12', !/b\.done \/ 12/.test(PR));
t('sổ bố mẹ không còn dựng 14 ô chương', !/length:\s*14/.test(PR));

const HS = doc('HocSinhChiTiet.jsx');
t('bảng cô giáo có màn học bạ từng em', ds.includes('HocSinhChiTiet.jsx'));
t('học bạ từng em: theo lớp · theo chủ đề · nhật ký',
  /'lop'/.test(HS) && /'chude'/.test(HS) && /nhatKy/.test(HS));
t('học bạ từng em hỏi môn, không tự đọc dữ liệu Toán',
  /hocBaCuaEm/.test(HS) && /nhatKyCuaEm/.test(HS) && !HS.includes('mon/toan'));

/* ══ 4 · KỆ SÁCH XẾP THEO thuTu ══ */
const KS = doc('KeSach.jsx');
t('kệ sách xếp theo thuTu, không theo thứ tự khai trong tệp', /thuTu/.test(KS));

console.log(`\n   soi ${ds.length} tệp giao diện · ${Object.keys(GOC).length} màn gốc phải có cửa về nhà`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
