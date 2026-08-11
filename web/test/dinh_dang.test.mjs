/**
 * CỔNG ĐỊNH DẠNG — canh chiều NGƯỢC: có chỗ nào bị bọc NHẦM không.
 * chạy: node test/dinh_dang.test.mjs
 *
 * Cổng `chu_vao_man.test.mjs` canh "công thức có được vẽ không". Tệp này canh cái
 * ngược lại, và nó mới là cái nguy hiểm: **bọc nhầm một mẩu lời văn vào `$…$` thì
 * xấu hơn hẳn lúc chưa sửa** — bé thấy một cục chữ đơn cách nằm giữa câu.
 *
 * Vì sao cần canh: luật phân số vừa được nới để nhận ẩn bằng chữ cái
 * (`1/(a × b) = 1/a − 1/b`). Nới thêm một bước nữa là dính ngay, vì trong năm
 * quyển có 991 cụm `X/Y` mang chữ mà đại đa số KHÔNG phải phân số:
 *
 *     Đúng/Sai 230 · km/h 224 · m/s 115 · thêm/bớt 15 · phần/giờ 15
 *     vòng/giờ 15 · m/giây 14 · 1/năm 5 · 2/g 2 (gam) · Sxq/Stp 2
 *
 * Nên luật chỉ nhận đúng mười chữ cái THƯỜNG, ĐƠN LẺ: a b c d k m n p q t.
 * Ai nới nữa thì tệp này báo — đừng chờ mắt người bắt.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const D = new URL('../public/content/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (ds) => ds.slice(0, 5).forEach((d) => console.log('     ', d));

const QUYEN = [['lop2', 'lop2'], ['lop3', 'lop3'], ['lop4', 'lop4'],
  ['lop5', 'lessons'], ['lop5q2', 'quyen2']];

/* Đọc TOÀN VĂN từng tệp: bọc nhầm ở trường nào cũng là bọc nhầm, không cần biết
   tên trường. Giữ nguyên chuỗi JSON để đếm được cả dấu `$` lẻ. */
const tep = [];
for (const [q, thu] of QUYEN) {
  const dir = join(D, thu);
  if (!existsSync(dir)) continue;
  for (const f of readdirSync(dir).filter((x) => x.startsWith('DL_') || x.startsWith('DR_'))) {
    tep.push({ q, f, van: readFileSync(join(dir, f), 'utf8') });
  }
}
t(`đọc được tệp nội dung (${tep.length})`, tep.length > 250);

/* ── 1 · KHÔNG BỌC NHẦM LỜI VĂN VÀO PHÂN SỐ ──
   Tử hay mẫu chỉ được là: một số, hoặc MỘT chữ cái thường trong danh sách, hoặc
   một cụm ngoặc gồm bấy nhiêu thứ ấy. Thấy chữ có dấu tiếng Việt, chữ hoa, hay
   một từ nhiều chữ cái là bọc nhầm. */
const HANG = String.raw`(?:\d+(?:[.,]\d+)?|[abcdkmnpqt])`;
const HOP_LE = new RegExp(
  `^(?:${HANG}|\\(?\\s*${HANG}(?:\\s*(?:\\\\times|[-+])\\s*` +
  `(?:${HANG}|\\(\\s*${HANG}\\s*[-+]\\s*${HANG}\\s*\\)))?\\s*\\)?)$`);

const R_FRAC = /\\{1,2}d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g;
const bocNham = [];
for (const { q, f, van } of tep) {
  for (const m of van.matchAll(R_FRAC)) {
    for (const phan of [m[1], m[2]]) {
      const s = phan.replace(/\\\\/g, '\\').trim();
      if (!HOP_LE.test(s)) bocNham.push(`${q} ${f}: \\frac{${m[1]}}{${m[2]}}`);
    }
  }
}
t(`không phân số nào bọc nhầm lời văn (${bocNham.length})`, bocNham.length === 0);
in5([...new Set(bocNham)]);

/* ── 2 · MẤY CỤM ĐÍCH DANH PHẢI CÒN NGUYÊN ──
   Liệt tên ra để người sau đọc cổng là hiểu ngay vì sao luật hẹp đến thế. */
const PHAI_NGUYEN = ['km/h', 'm/s', 'Đúng/Sai', 'km/giờ', 'm/giây', 'thêm/bớt',
  'vòng/giờ', 'phần/giờ', 'tổng/hiệu', 'chẵn/lẻ', 'cộng/trừ', 'Sxq/Stp'];
const hong = [];
for (const cum of PHAI_NGUYEN) {
  const [tu, mau] = cum.split('/');
  const dau = `{${tu}}{${mau}}`;
  for (const { q, f, van } of tep) {
    if (van.includes(dau)) hong.push(`${q} ${f}: "${cum}" bị bọc thành phân số`);
  }
}
t(`đơn vị và lời văn còn nguyên (${hong.length})`, hong.length === 0);
in5(hong);

/* ── 3 · KHÔNG CÓ LỆNH LATEX DÍNH LIỀN ──
   `\times` là một LỆNH. Sách viết `1/(1×2)` không dấu cách, nên bộ chuyển phải TỰ
   đặt khoảng — dán liền thành `\timesb` là bộ vẽ đọc ra một lệnh lạ tên `\timesb`
   rồi in NGUYÊN VĂN ra màn hình. Đã suýt dính khi nới luật cho ẩn bằng chữ. */
const LENH = ['times', 'div', 'cdot', 'frac', 'dfrac', 'text', 'le', 'ge'];
const dinhLien = [];
for (const { q, f, van } of tep) {
  for (const m of van.matchAll(/\\{1,2}([a-zA-Z]+)/g)) {
    const ten = m[1];
    if (LENH.includes(ten)) continue;
    const goc = LENH.find((l) => ten.startsWith(l) && ten.length > l.length);
    if (goc) dinhLien.push(`${q} ${f}: \\${ten}`);
  }
}
t(`không lệnh LaTeX nào dính vào chữ sau (${dinhLien.length})`, dinhLien.length === 0);
in5([...new Set(dinhLien)]);

/* ── 4 · DẤU $ PHẢI CHẴN Ở TỪNG TRƯỜNG ──
   Lẻ một dấu là từ đó tới cuối trường bị bộ vẽ coi là công thức. */
const le = [];
const soi = (o, bai, q) => {
  if (typeof o === 'string') {
    if ((o.match(/\$/g) || []).length % 2) le.push(`${q} ${bai}: ${o.slice(0, 60)}`);
  } else if (Array.isArray(o)) o.forEach((x) => soi(x, bai, q));
  else if (o && typeof o === 'object') Object.values(o).forEach((x) => soi(x, bai, q));
};
for (const { q, f, van } of tep) soi(JSON.parse(van), f, q);
t(`không trường nào có dấu $ lẻ (${le.length})`, le.length === 0);
in5(le);

const dem = {};
for (const { q, van } of tep) {
  dem[q] ??= 0;
  dem[q] += (van.match(R_FRAC) || []).length;
}
console.log('\n   phân số theo quyển — '
  + Object.entries(dem).map(([q, n]) => `${q}: ${n}`).join(' · '));
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
