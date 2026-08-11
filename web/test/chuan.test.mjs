/**
 * CỔNG CHUẨN — docs/CHUAN_DUA_SACH_VAO_APP.md có còn ĐÚNG không.
 * chạy: node test/chuan.test.mjs
 *
 * Tài liệu chuẩn nói dối là tệ hơn không có tài liệu: người sau đọc rồi làm theo,
 * dính đúng cái bẫy mà tài liệu tưởng đã rào. Nên những gì chuẩn KHẲNG ĐỊNH được
 * thì soi bằng máy, đừng để nó mục ruỗng theo mỗi lần đổi mã.
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
const CHUAN = join(G, 'docs/CHUAN_DUA_SACH_VAO_APP.md');

/* Số viết bằng chữ, để soi tiêu đề "Bốn mươi cái bẫy" khớp số mục thật sự có. */
const SO_CHU = { 31: 'Ba mươi mốt', 35: 'Ba mươi lăm', 40: 'Bốn mươi', 42: 'Bốn mươi hai', 44: 'Bốn mươi bốn',
                 45: 'Bốn mươi lăm', 50: 'Năm mươi' };

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

t('tài liệu chuẩn có thật', existsSync(CHUAN));
const md = readFileSync(CHUAN, 'utf8');

/* Chuẩn dẫn tệp nào thì tệp ấy phải có thật — dẫn sai là người sau đi tìm mỏi mắt. */
const dan = [...md.matchAll(/`((?:tools|docs|data|web|figforge)\/[\w./<>-]+)`/g)]
  .map((m) => m[1]).filter((p) => !p.includes('<'));
const thieu = [...new Set(dan)].filter((p) => !existsSync(join(G, p)));
t(`mọi tệp chuẩn dẫn ra đều có thật (${new Set(dan).size} tệp)`, thieu.length === 0);
if (thieu.length) console.log('     thiếu:', thieu.join(' · '));

/* Số liệu chuẩn nêu phải khớp dữ liệu — số cũ làm người sau ước lượng sai. */
const so = (re) => Number((md.match(re) || [])[1]);
const sotay = JSON.parse(readFileSync(join(G, 'data/lop2_hinh_manifest.json'), 'utf8'));
const tay = JSON.parse(readFileSync(join(G, 'data/lop2_dapan_tay.json'), 'utf8'));
const dapan = JSON.parse(readFileSync(join(G, 'data/lop2_dapan.json'), 'utf8'));
t(`số hình khớp (${Object.keys(sotay).length})`, so(/tổng (\d+) hình · \d+ nguyên mẫu/) === Object.keys(sotay).length);
t(`số câu viết tay khớp (${Object.keys(tay).length})`,
  so(/\| viết tay \| (\d+) \/ 281 \|/) === Object.keys(tay).length);
t(`số câu suy máy khớp (${Object.keys(dapan).length - Object.keys(tay).length})`,
  so(/soát tay từng câu\) \| (\d+) \/ 281 \|/) === Object.keys(dapan).length - Object.keys(tay).length);

/* Các dạng khoá đáp án chuẩn liệt kê phải là dạng bộ chấm THẬT SỰ hiểu. */
const flow = readFileSync(join(G, 'web/src/mon/toan/lib/flow.js'), 'utf8');
for (const k of ['key.values', 'key.accept', 'key.parts', 'key.choice'])
  t(`bộ chấm hiểu ${k}`, flow.includes(k));

/* Dây chuyền chuẩn mô tả 7 bước — thêm/bớt bước mà quên sửa chuẩn thì lệch. */
const lam = readFileSync(join(G, 'tools/lam_lop2.py'), 'utf8');
const soBuoc = (lam.match(/^\s{4}\('/gm) || []).length;
t(`dây chuyền đúng 7 bước (${soBuoc})`, soBuoc === 7);
t('chuẩn cũng nói 7 bước', /bảy bước/i.test(md));

/* Ba tầng dữ liệu chuẩn nêu phải tồn tại và KHÁC nhau (cố ý). */
t('tầng gốc và tầng khuôn chung đều có',
  readdirSync(join(G, 'data/lop2')).length > 30
  && readdirSync(join(G, 'web/public/content/lop2')).length > 30);

/* Số chữ màn mở chuẩn NÊU RA phải khớp dữ liệu thật — chuẩn khoe "còn 66 chữ" mà
   thực tế phình lại thì người sau tưởng đã gọn rồi, không soi nữa. Cho lệch 15%
   vì thêm bài mới thì trung bình xê dịch, nhưng phình gấp đôi là phải biết. */
const trungBinh = (thuMuc, tienTo) => {
  const ds = readdirSync(join(G, thuMuc)).filter((f) => f.startsWith(tienTo));
  const n = ds.map((f) => {
    const d = JSON.parse(readFileSync(join(G, thuMuc, f), 'utf8'));
    const hook = (d.lecture?.screens || []).find((x) => x.kind === 'hook');
    return (hook?.narration || '').length;
  }).filter((x) => x > 0);
  return n.reduce((a, b) => a + b, 0) / (n.length || 1);
};
for (const [ten, thuMuc, tienTo, mau] of [
  ['lớp 5', 'data/lessons', 'DL_KSN5Q1_', /lớp 5 còn\s+(\d+) chữ/],
  ['lớp 2', 'web/public/content/lop2', 'DL_KSN2_', /lớp 2 còn (\d+) chữ/]]) {
  const noi = so(mau), that = trungBinh(thuMuc, tienTo);
  t(`màn mở ${ten} còn ${Math.round(that)} chữ, chuẩn nói ${noi}`,
    Number.isFinite(noi) && Math.abs(that - noi) <= noi * 0.15);
}

/* Danh sách bẫy đánh số liên tục, và tiêu đề phải khớp số cuối cùng.
   CẮT ĐÚNG PHẦN BẪY trước đã: tài liệu còn vài danh sách đánh số khác (ba loại
   hình, bốn luật màn mở) — quét cả tài liệu thì đếm ra 47 thay vì 40. */
// lát cắt bắt đầu NGAY TẠI dòng "## 9 ·" nên phần tử [0] của split là rỗng
const phanBay = (md.slice(md.search(/^## \d+ · [^\n]*cái bẫy/m))
  .split(/^## /m)[1] || '');
const soBay = [...phanBay.matchAll(/^(\d+)\. \*\*/gm)].map((m) => Number(m[1]));
t(`danh sách bẫy đánh số liên tục 1..${soBay.length}`,
  soBay.every((n, i) => n === i + 1));
t(`tiêu đề nói đúng ${soBay.length} bẫy`,
  !!SO_CHU[soBay.length] && md.includes(`${SO_CHU[soBay.length]} cái bẫy`));

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
