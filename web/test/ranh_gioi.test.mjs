/**
 * CỔNG RANH GIỚI — hai môn không được với sang nhau.
 * chạy: node test/ranh_gioi.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Bác dặn: "có làm gì cũng không được ảnh hưởng đến môn Toán cho các cháu học."
 * Một lời hứa thì không giữ được — sáu tháng nữa ai đó cần một hàm tiện tay, `import`
 * một dòng từ `mon/toan/lib/flow.js` sang Tiếng Anh, và thế là hai môn dính lại. Từ
 * đó, sửa bộ chấm tiếng Anh có thể làm sai điểm của 1 612 câu Toán đang chạy thật.
 *
 * Tệp này biến lời hứa thành hàng rào MÁY GÁC:
 *
 *   1. `mon/toan/**`     KHÔNG được import từ `mon/tienganh/**`, và ngược lại;
 *   2. `chung/**`        KHÔNG được import từ `mon/**` — tầng vỏ phải mù về môn.
 *      Nó chỉ biết GIAO ƯỚC (`chung/lib/soMon.js`), không biết môn nào làm gì bên trong;
 *   3. `mon/**`          ĐƯỢC import từ `chung/**` — một chiều, và chỉ chiều ấy;
 *   4. mỗi môn khai đủ giao ước, để bốn màn tổng vẽ được mà không cần biết gì thêm.
 *
 * Luật 2 là luật dễ vỡ nhất và cũng đắt nhất: chỉ cần `KeSach.jsx` gọi một hàm của
 * Toán là kệ sách vĩnh viễn không dựng nổi môn thứ hai.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, relative, dirname, resolve } from 'node:path';

const SRC = new URL('../src/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

/** Mọi tệp mã nguồn, kèm đường dẫn tương đối từ `src/`. */
function quet(thuMuc, ra = []) {
  for (const x of readdirSync(thuMuc, { withFileTypes: true })) {
    const p = join(thuMuc, x.name);
    if (x.isDirectory()) quet(p, ra);
    else if (/\.jsx?$/.test(x.name)) ra.push(p);
  }
  return ra;
}
const TEP = quet(SRC);
const tuongDoi = (p) => relative(SRC, p);

/** Các đường `import … from '…'` trỏ vào trong kho (bỏ qua thư viện ngoài). */
function nhapCua(p) {
  const s = readFileSync(p, 'utf8');
  const ra = [];
  for (const m of s.matchAll(/from\s+'(\.[^']+)'/g)) {
    ra.push({ thoTuc: m[1], dich: tuongDoi(resolve(dirname(p), m[1])) });
  }
  return ra;
}

const vung = (p) => (p.startsWith('mon/toan/') ? 'toan'
  : p.startsWith('mon/tienganh/') ? 'tienganh'
    : p.startsWith('chung/') ? 'chung' : 'vo');

/* ══ 1 · HAI MÔN KHÔNG ĐƯỢC VỚI SANG NHAU ══ */
const cheo = [];
for (const p of TEP) {
  const tu = vung(tuongDoi(p));
  if (tu !== 'toan' && tu !== 'tienganh') continue;
  for (const { dich, thoTuc } of nhapCua(p)) {
    const den = vung(dich);
    if ((den === 'toan' || den === 'tienganh') && den !== tu) {
      cheo.push(`${tuongDoi(p)} → ${thoTuc}`);
    }
  }
}
t(`môn này không import từ môn kia (${cheo.length} đường)`, cheo.length === 0);
in5(cheo);

/* ══ 2 · TẦNG CHUNG PHẢI MÙ VỀ MÔN ══
   Đây là hàng rào đắt nhất. Kệ sách · bảng xếp hạng · sổ bố mẹ · bảng cô giáo đều ở
   tầng chung; chỉ cần MỘT trong bốn màn ấy gọi thẳng vào Toán là chúng vĩnh viễn
   không dựng nổi môn thứ hai, và mỗi lần thêm môn lại phải sửa cả bốn. */
const chungNhinXuong = [];
for (const p of TEP) {
  if (vung(tuongDoi(p)) !== 'chung') continue;
  for (const { dich, thoTuc } of nhapCua(p)) {
    if (dich.startsWith('mon/')) chungNhinXuong.push(`${tuongDoi(p)} → ${thoTuc}`);
  }
}
t(`tầng chung không nhìn vào môn nào (${chungNhinXuong.length} đường)`, chungNhinXuong.length === 0);
in5(chungNhinXuong);

/* ══ 3 · MÔN ĐƯỢC DÙNG TẦNG CHUNG — một chiều ══ */
const dungChung = TEP.filter((p) => vung(tuongDoi(p)).startsWith('to')
  && nhapCua(p).some((x) => x.dich.startsWith('chung/')));
t('môn Toán có dùng tầng chung (một chiều)', dungChung.length > 0);

/* ══ 4 · VỎ APP chỉ được biết GIAO ƯỚC ══
   `App.jsx` và `main.jsx` đứng ngoài cả ba vùng. Chúng được phép nạp sổ môn, nhưng
   KHÔNG được với thẳng vào ruột một môn — nếu không thì "tách" chỉ là tách thư mục. */
const voVaoRuot = [];
for (const p of TEP) {
  if (vung(tuongDoi(p)) !== 'vo') continue;
  for (const { dich, thoTuc } of nhapCua(p)) {
    if (dich.startsWith('mon/') && !dich.endsWith('/index.js')) {
      voVaoRuot.push(`${tuongDoi(p)} → ${thoTuc}`);
    }
  }
}
t(`vỏ app chỉ vào cửa index.js của môn (${voVaoRuot.length} đường lách)`, voVaoRuot.length === 0);
in5(voVaoRuot);

/* ══ 5 · MỖI MÔN KHAI ĐỦ GIAO ƯỚC ══ */
const GIAO_UOC = ['ma', 'ten', 'Man'];
const monCo = readdirSync(join(SRC, 'mon'), { withFileTypes: true })
  .filter((x) => x.isDirectory()).map((x) => x.name);
t(`có ít nhất hai môn (${monCo.join(' · ')})`, monCo.length >= 2);
for (const m of monCo) {
  const cua = join(SRC, 'mon', m, 'index.js');
  t(`${m} có cửa index.js`, existsSync(cua));
  if (!existsSync(cua)) continue;
  const s = readFileSync(cua, 'utf8');
  const thieu = GIAO_UOC.filter((k) => !new RegExp(`\\b${k}\\s*[:,]`).test(s));
  t(`${m} khai đủ giao ước (thiếu: ${thieu.join() || 'không'})`, thieu.length === 0);
}

/* ══ 6 · SỔ MÔN LÀ NƠI DUY NHẤT BIẾT CÓ NHỮNG MÔN NÀO ══
   Nó nằm ở tầng VỎ (`src/soMon.js`), KHÔNG ở `chung/` — vì `chung/` phải mù hẳn về
   môn, mà sổ thì buộc phải gọi tên từng môn. Đặt nhầm chỗ là luật 2 mất hiệu lực. */
const soMon = join(SRC, 'soMon.js');
t('có sổ đăng ký môn', existsSync(soMon));
if (existsSync(soMon)) {
  const s = readFileSync(soMon, 'utf8');
  for (const m of monCo) t(`sổ môn có khai ${m}`, s.includes(`mon/${m}/index.js`) || s.includes(`../../mon/${m}`));
}

/* ══ 7 · MỌI LÕI PHẢI NẠP VÀ GỌI ĐƯỢC THẬT ══
   Xẻ một tệp làm đôi rất dễ để lại một TÊN TREO: hàm ở nửa này gọi một biến vốn nằm
   ở nửa kia, mà `export … from` chỉ chuyển tiếp ra ngoài chứ KHÔNG đưa tên vào phạm
   vi tệp. Cổng đọc mã nguồn không thấy, vì lỗi chỉ nổ lúc CHẠY.

   Dính thật ngay đợt tách này: `loadLesson` gọi `THU_MUC_CUA` đã ở lại nửa kia — cổng
   xanh 1 095 phép, mà mở app ra là "THU_MUC_CUA is not defined", cả bốn quyển câm.

   Nạp module thôi thì KHÔNG bắt được: thân hàm chưa chạy. Nên phải GỌI THỬ từng hàm
   xuất ra. Chỉ soi `ReferenceError` — đó đúng là dấu hiệu tên treo; `TypeError` hay
   lỗi thiếu tham số thì bỏ qua, vì gọi khống thì sai kiểu là chuyện đương nhiên. */
const loi = [];
for (const p of TEP) {
  const rel = tuongDoi(p);
  if (!/\/lib\/[\w.]+\.js$/.test(rel)) continue;         // chỉ lõi JS thuần
  let m;
  try { m = await import(p); } catch (e) { loi.push(`${rel}: nạp vỡ — ${e.message.slice(0, 60)}`); continue; }
  for (const [ten, v] of Object.entries(m)) {
    if (typeof v !== 'function') continue;
    const bat = (e) => { if (e instanceof ReferenceError) loi.push(`${rel}: ${ten}() → ${e.message}`); };
    try {
      const kq = v();
      /* Hàm `async` KHÔNG ném ra ngoài — nó trả về một promise BỊ TỪ CHỐI. Nuốt bằng
         `.catch(() => {})` là nuốt luôn cả tên treo, đúng lỗi bản đầu của cổng này
         mắc phải: nó xanh trong khi `loadLesson` đang vỡ thật. */
      if (kq && typeof kq.then === 'function') await kq.then(() => {}, bat);
    } catch (e) { bat(e); }
  }
}
t(`lõi nạp và gọi được, không tên nào treo (${loi.length} chỗ)`, loi.length === 0);
in5(loi);

/* ─────────── tổng kết ─────────── */
const dem = { chung: 0, toan: 0, tienganh: 0, vo: 0 };
for (const p of TEP) dem[vung(tuongDoi(p))]++;
console.log(`\n   ${TEP.length} tệp · chung ${dem.chung} · toán ${dem.toan}`
  + ` · tiếng anh ${dem.tienganh} · vỏ ${dem.vo}`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
