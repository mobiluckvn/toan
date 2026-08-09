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
t(`số hình khớp (${Object.keys(sotay).length})`, so(/(\d+) hình · 17 nguyên mẫu/) === Object.keys(sotay).length);
t(`số câu viết tay khớp (${Object.keys(tay).length})`,
  so(/\| viết tay \| (\d+) \/ 281 \|/) === Object.keys(tay).length);
t(`số câu suy máy khớp (${Object.keys(dapan).length - Object.keys(tay).length})`,
  so(/soát tay từng câu\) \| (\d+) \/ 281 \|/) === Object.keys(dapan).length - Object.keys(tay).length);

/* Các dạng khoá đáp án chuẩn liệt kê phải là dạng bộ chấm THẬT SỰ hiểu. */
const flow = readFileSync(join(G, 'web/src/lib/flow.js'), 'utf8');
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

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
