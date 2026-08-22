/**
 * CỔNG GÁC LỚP DỮ LIỆU MÁY CHỦ CỦA MÔN TIẾNG ANH.
 * chạy: node test/tienganh_may_chu.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * `firestore.rules` kết bằng `match /{document=**} { allow read, write: if false; }`.
 * Nghĩa là mọi collection MỚI bị chặn cho tới khi có luật riêng — và Firestore từ
 * chối **trong im lặng** với lệnh ghi không chờ kết quả:
 *
 *     bé học xong → màn hình báo "Giỏi lắm!" → sổ tại máy có → MÁY CHỦ TRỐNG
 *
 * Không có gì đỏ, không có gì báo. Sổ bố mẹ mở ra trống, và người sửa đi tìm ở
 * tầng giao diện trong khi lỗi nằm ở một dòng luật chưa viết. Đây là lỗi đã dính
 * thật một lần khi làm học bạ (ghi trong sổ ghi nhớ).
 *
 * Nên cổng này soi đúng chỗ ấy: MỌI collection mã nguồn ghi vào đều phải có một
 * khối luật tương ứng. Nó KHÔNG kiểm được luật đã deploy hay chưa — việc ấy chỉ
 * máy chủ biết — nhưng nó chặn được nửa còn lại: quên viết luật.
 */
import { readFileSync, existsSync } from 'node:fs';

const R = new URL('../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const luat = readFileSync(`${R}firestore.rules`, 'utf8');
const nguon = `${R}src/mon/tienganh/lib/duLieu.js`;

if (!existsSync(nguon)) {
  console.log('   ⏸ môn Tiếng Anh chưa có lớp dữ liệu máy chủ');
  console.log('\n0 PASS · 0 FAIL');
  process.exit(0);
}
const ma = readFileSync(nguon, 'utf8');

/* ══ 1 · MỌI COLLECTION MÃ NGUỒN DÙNG ĐỀU PHẢI CÓ LUẬT ══
   Đọc thẳng bảng `KHO` trong mã nguồn chứ không gõ tay danh sách ở đây: thêm một
   collection mà quên viết luật thì cổng đỏ ngay, không ai phải nhớ. */
const kho = [...ma.matchAll(/^\s*\w+:\s*\(uid\)\s*=>\s*`([\w/${}]+)`/gm)]
  .map((m) => m[1].split('/')[0]);
t(`đọc được bảng collection từ mã nguồn (${kho.join(' · ') || 'không thấy'})`, kho.length > 0);

const thieuLuat = kho.filter((c) => !new RegExp(`match\\s+/${c}/`).test(luat));
t(`mọi collection đều có khối luật (${thieuLuat.length} thiếu)`, thieuLuat.length === 0);
in5(thieuLuat.map((c) => `${c}: chưa có "match /${c}/…" trong firestore.rules`));

/** Thân của một khối luật, cắt đúng collection ấy — xem lý do ở mục 3. */
const khoiCua = (c) => {
  const i = luat.indexOf(`match /${c}/`);
  return i < 0 ? '' : luat.slice(i, luat.indexOf('\n    }', i));
};

/* ══ 2 · LUẬT PHẢI THẬT SỰ CHẶN NGƯỜI LẠ ══
   Viết luật mà quên `isMine` thì bé A ghi được vào sổ của bé B. Đây là chỗ đắt
   nhất để sai, nên soi từng khối. */
/* ⚠ SOI TÍNH CHẤT, ĐỪNG ĐÒI ĐÚNG MỘT CHỮ.
   Bản đầu đòi bằng được `allow read: if canRead(`. Nhưng `reviewQueue` viết
   `isMine(userId) || isAdmin()` — CHẶT HƠN `canRead` (không cho giáo viên đọc),
   thế mà cổng vẫn kêu "hở". Cổng đòi một cách viết thay vì đòi một tính chất thì
   sớm muộn ép người ta NỚI luật ra cho cổng xanh — đúng chiều ngược lại với việc
   nó sinh ra để làm.
   Nay: quyền đọc phải gác bằng `canRead(` HOẶC `isMine(`. Cả hai đều chặn người
   lạ; `if true` thì vẫn bị bắt ở dòng dưới. */
const hong = [];
for (const c of kho) {
  const than = khoiCua(c);
  if (!/allow write:\s*if\s+isMine\(/.test(than)) hong.push(`${c}: quyền ghi không gác bằng isMine()`);
  if (!/allow read:\s*if\s+(canRead|isMine)\(/.test(than)) {
    hong.push(`${c}: quyền đọc không gác bằng canRead() hay isMine()`);
  }
  if (/allow (read|write)[^;]*:\s*if\s+true/.test(than)) hong.push(`${c}: có "if true" — mở toang`);
}
t(`luật của mỗi collection đều gác chính chủ (${hong.length} chỗ hở)`, hong.length === 0);
in5(hong);

/* ══ 3 · TRƯỜNG BẮT BUỘC PHẢI ĐƯỢC GHI ══
   Luật đòi `pass is bool` và `score is number`. Mã nguồn quên một trường, hoặc ghi
   sai kiểu, là bị từ chối — lại im lặng. Soi bằng cách đọc chính đoạn setDoc. */
/* CHỈ soi khối luật của môn này. Bản đầu quét cả tệp nên vớ luôn `correct is bool`
   của collection `attempts` bên Toán rồi đòi duLieu.js của Tiếng Anh phải ghi
   trường ấy — báo oan. Phép kiểm báo oan nguy hơn phép kiểm bỏ sót: lần sau người
   ta tắt nó đi. */
const doiTruong = kho.flatMap((c) =>
  [...khoiCua(c).matchAll(/request\.resource\.data\.(\w+)\s+is\s+(\w+)/g)]
    .map((m) => [m[1], m[2]]));
const thieuTruong = doiTruong
  .filter(([f]) => !new RegExp(`\\b${f}:`).test(ma))
  .map(([f, k]) => `luật đòi "${f}" (${k}) mà duLieu.js không ghi trường ấy`);
t(`mã nguồn ghi đủ trường luật đòi (${thieuTruong.length} thiếu)`, thieuTruong.length === 0);
in5(thieuTruong);

/* ══ 4 · KHÔNG ĐƯỢC NUỐT LỖI IM LẶNG ══
   `catch {}` trơn là chỗ lỗi biến mất. Phải có bộ đếm để người sửa lần ra được. */
t('có bộ đếm lần bị từ chối (LOI_GHI)', /LOI_GHI/.test(ma));
const nuotIm = (ma.match(/catch\s*(\([^)]*\))?\s*\{\s*\}/g) || []).length;
t(`không có catch rỗng nuốt lỗi (${nuotIm} chỗ)`, nuotIm === 0);

/* ══ 5 · KHÔNG ĐƯỢC GHI VÀO SÂN CỦA TOÁN ══
   Đổ bài tiếng Anh vào `progress/{uid}/micros` là hàm nền tính mức thạo theo ma
   trận Toán cho cả hai môn — sai âm thầm, không gì báo. */
/* Bỏ chú thích trước khi soi. Bản đầu quét cả tệp nên vớ đúng dòng chú thích đang
   GIẢI THÍCH vì sao không được dùng `progress/{uid}/micros` của Toán — cổng đỏ vì
   chính lời dặn đừng làm thế. */
const maSach = ma.replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
const lanSan = [...maSach.matchAll(/`(progress|hocBa|attempts|mastery)\//g)].map((m) => m[1]);
t(`không ghi vào collection của Toán (${lanSan.join(', ') || 'không'})`, lanSan.length === 0);

/* ══ 6 · BẢNG XẾP HẠNG CHỈ ĐƯỢC ĐỌC ══
   Tài liệu DUY NHẤT một bé đọc được về bé khác. Máy con ghi được vào đó là tự đặt
   điểm cho mình hoặc sửa tên bạn. */
t('không ghi vào bảng xếp hạng', !/setDoc\([^)]*bangXepHang/.test(ma));
const khoiXH = luat.slice(luat.indexOf('match /bangXepHang/'));
t('luật bảng xếp hạng vẫn cấm ghi',
  /allow write:\s*if\s+false/.test(khoiXH.slice(0, khoiXH.indexOf('\n    }'))));

/* ══ 7 · TỆP LUẬT PHẢI CÒN NGUYÊN HÌNH ══
   KHÔNG thay được cho việc chạy thật: chỉ bộ giả lập Firestore (cần Java) hoặc
   chính máy chủ mới biên dịch được bộ luật. Máy này chưa có Java, nên đây là lưới
   đỡ tối thiểu — bắt cái sai thường gặp nhất khi chèn khối mới: lệch ngoặc.

   Lệch ngoặc thì `firebase deploy` từ chối cả tệp, và bộ luật ĐANG CHẠY giữ nguyên
   bản cũ — tức là hai collection mới vẫn bị chặn, vẫn im lặng, y như chưa làm gì. */
const moc = luat.split('').reduce((n, c) => n + (c === '{') - (c === '}'), 0);
t(`ngoặc trong firestore.rules cân bằng (lệch ${moc})`, moc === 0);
const soMatch = (luat.match(/match\s+\/[\w{}$/=*.]+\s*\{/g) || []).length;
const soAllow = (luat.match(/allow\s+[\w, ]+:/g) || []).length;
t(`mọi khối match đều có allow (${soMatch} match · ${soAllow} allow)`, soAllow >= soMatch);
t('vẫn còn chốt chặn cuối "mặc định cấm"',
  /match \/\{document=\*\*\}\s*\{\s*allow read, write: if false;/.test(luat));

console.log(`\n   collection của môn: ${kho.join(' · ')}`);
console.log('   ⚠ cổng này KHÔNG kiểm được luật đã deploy chưa — chạy'
  + ' `firebase deploy --only firestore:rules` rồi mới ghi được lên máy chủ.');
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
