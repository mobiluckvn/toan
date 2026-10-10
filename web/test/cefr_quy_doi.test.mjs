/**
 * CỔNG: phép quy đổi P(L) → CEFR không được nói quá.
 *
 * Cổng này không kiểm "tính đúng công thức" — công thức là phép chia, khó sai.
 * Nó kiểm bốn chỗ mà phép quy đổi DỄ NÓI DỐI, và cả bốn đều từng là bẫy thật ở
 * những phép đếm khác trong repo này:
 *
 *   1. mẫu số lấy theo "nút đã chạm" → học ít thì điểm cao (xem `ngưỡng phần
 *      trăm che lỗ thủng`);
 *   2. đếm cả nút CHỨA (unit · theme) vào vốn → pha loãng, % tụt giả;
 *   3. khối 4 nút vẫn được kết luận thành một bậc;
 *   4. câu tiếng Việt ghép chữ "đạt <bậc>" trong khi `mucDat` là null.
 *
 * Mỗi phép dưới đây đều có VẾ NGƯỢC: dựng sổ mastery giả sao cho nếu bỏ hàng rào
 * thì cổng phải đỏ. Cổng chỉ xanh vì mã đúng, không phải vì phép kiểm dễ.
 */

import { readFileSync } from 'node:fs';
import {
  bacCefr, cauMoTa, PHU_DAT, TOI_THIEU_NUT, KHOI,
} from '../src/mon/tienganh/lib/cefr.js';

const dt = JSON.parse(readFileSync(
  new URL('../public/content/tienganh/do_thi.json', import.meta.url), 'utf8',
));

let pass = 0; let fail = 0;
const ok = (dieu, ten, them = '') => {
  if (dieu) { pass += 1; } else { fail += 1; console.log(`  ✗ ${ten}${them ? ` — ${them}` : ''}`); }
};

/* ── 1. Bé mới học 5 nút và nắm cả 5 thì KHÔNG được ra bậc nào ────────────── */
{
  const nam5 = Object.entries(dt.nut)
    .filter(([, n]) => n.g === 3 && n.t === 'vocabulary').slice(0, 5);
  const so = Object.fromEntries(nam5.map(([ma]) => [ma, { p: 0.99 }]));
  const kq = bacCefr(dt, so);
  ok(kq.mucDat === null, 'học 5 nút mà nắm hết thì chưa ra bậc',
    `lại ra ${kq.mucDat?.ma}`);
  /* ⚠ KHÔNG ghim chuỗi "đạt A1". Câu trung thực NÀO cũng có thể chứa chữ ấy ở
     thể phủ định ("Chưa đủ để nói con đạt Bậc 1"), và cổng bản đầu đã đỏ đúng
     vào một câu đúng. Ghim TÍNH CHẤT: chưa ra bậc thì câu phải mang mệnh đề phủ
     định rõ ràng. */
  ok(/Chưa đủ|mới bắt đầu/.test(cauMoTa(kq)),
    'chưa ra bậc thì câu mô tả phải nói rõ là chưa đủ căn cứ', cauMoTa(kq));
  const a1 = kq.banDo.find((b) => b.ma === 'A1');
  ok(a1.phu < 0.02, 'mẫu số là TOÀN khối chứ không phải số nút đã chạm',
    `phu=${a1.phu}`);
}

/* ── 2. Nút CHỨA không được vào mẫu số ────────────────────────────────────── */
{
  const kq = bacCefr(dt, {});
  const chua = Object.values(dt.nut).filter(
    (n) => ['course', 'theme', 'unit', 'review', 'fun_time'].includes(n.t),
  ).length;
  ok(chua > 0, 'đồ thị thật có nút chứa để mà loại (nếu không, phép kiểm này rỗng)');
  ok(kq.tongNut + chua === Object.keys(dt.nut).length,
    'tổng vốn + nút chứa = toàn đồ thị',
    `${kq.tongNut} + ${chua} ≠ ${Object.keys(dt.nut).length}`);
  /* ── CHỐT BÁO ĐỘNG: ĐỒ THỊ ĐỔI THÌ BA CON SỐ CỦA LUẬN VĂN ĐỔI THEO ──
     Con số này ghim cố ý. Nó KHÔNG canh một tính chất (hai phép trên đã canh rồi) —
     nó canh việc đồ thị vừa đổi mà có thể chưa ai cập nhật luận văn, vì mẫu số của
     phép quy đổi CEFR là thứ phải bảo vệ được khi phản biện.
     Đỏ ở đây thì việc cần làm KHÔNG phải sửa số cho xanh, mà là: xem đồ thị đổi vì
     cái gì, rồi sửa CẢ luận văn lẫn dòng này.

     1062 → 1063 ngày 10-10-2026: khai `sp_g3_starter_1` vào bản đồ. Bài DL:TA3.B00
     dạy thật mẫu câu ấy nhưng bản đồ chưa bao giờ có nút, nên 6 câu mồ côi và nút
     cầu `sp_g3_numbers` (mà ba mẫu câu lớp 4 khai «cần») không có bài nào dạy —
     đúng một trong «19 nút gốc rễ không có bài dạy» của Bảng 3.25.
     Kéo theo: 1.194 → 1.195 đỉnh · 253 → 254 cạnh. */
  ok(kq.tongNut === 1063, 'vốn đếm được đúng 1063 nút học được', `ra ${kq.tongNut}`);
}

/* ── 3. Khối quá bé thì mang cờ không đáng tin, và không bao giờ thành mucDat ─ */
{
  const nutA2 = Object.entries(dt.nut).filter(([, n]) => n.g === 6);
  const so = Object.fromEntries(nutA2.map(([ma]) => [ma, { p: 1 }]));
  const kq = bacCefr(dt, so);
  const a2 = kq.banDo.find((b) => b.ma === 'A2');
  ok(a2.tong < TOI_THIEU_NUT, 'khối A2 trong đồ thị đúng là bé (tiền đề của phép kiểm)',
    `tong=${a2.tong}`);
  ok(a2.phu === 1, 'nắm hết khối bé thì phủ đúng 100%');
  ok(a2.dangTin === false, 'khối bé mang cờ dangTin=false');
  ok(kq.mucDat === null, 'phủ 100% một khối 4 nút vẫn KHÔNG ra bậc',
    `lại ra ${kq.mucDat?.ma}`);
}

/* ── 4. Đủ phủ thật thì PHẢI ra bậc — vế ngược của cả ba phép trên ────────── */
{
  const nutA1 = Object.entries(dt.nut).filter(
    ([, n]) => [3, 4, 5].includes(n.g)
      && !['course', 'theme', 'unit', 'review', 'fun_time'].includes(n.t),
  );
  const canNam = Math.ceil(nutA1.length * (PHU_DAT + 0.02));
  const so = Object.fromEntries(nutA1.slice(0, canNam).map(([ma]) => [ma, { p: 0.9 }]));
  const kq = bacCefr(dt, so);
  ok(kq.mucDat?.ma === 'A1', 'nắm 62% vốn lớp 3–5 thì ra A1', `ra ${kq.mucDat?.ma}`);
  ok(/A1/.test(cauMoTa(kq)), 'câu mô tả nêu đúng bậc khi đã đạt', cauMoTa(kq));
}

/* ── 5. p dưới ngưỡng thạo KHÔNG được tính là vững ────────────────────────── */
{
  const nutA1 = Object.entries(dt.nut).filter(([, n]) => [3, 4, 5].includes(n.g));
  const so = Object.fromEntries(nutA1.map(([ma]) => [ma, { p: 0.84 }]));
  const kq = bacCefr(dt, so);
  ok(kq.tongVung === 0, 'p=0,84 (sát dưới 0,85) không được kể là vững',
    `lại đếm ${kq.tongVung}`);
  ok(kq.coSo > 0, 'nhưng vẫn phải nhận là CÓ dữ liệu (coSo > 0)');
  ok(kq.mucDat === null, 'không nút nào vững thì không ra bậc');
}

/* ── 6. Mọi khối trong bảng đều có nút thật — bảng KHOI không lệch với đồ thị ─ */
{
  const kq = bacCefr(dt, {});
  KHOI.forEach((k) => {
    const b = kq.banDo.find((x) => x.ma === k.ma);
    ok(b.tong > 0, `khối ${k.ma} có nút thật trong đồ thị`, `tong=${b.tong}`);
  });
  const lopCoNut = new Set(Object.values(dt.nut).map((n) => n.g));
  const lopDaXep = new Set(KHOI.flatMap((k) => k.lop));
  const bo = [...lopCoNut].filter((g) => !lopDaXep.has(g));
  ok(bo.length === 0, 'không lớp nào trong đồ thị bị bỏ ngoài bảng khối',
    `bỏ sót lớp ${bo.join(', ')}`);
}

console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
