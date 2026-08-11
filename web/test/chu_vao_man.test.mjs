/**
 * CỔNG "CHỮ VÀO MÀN" — mọi trường có LaTeX phải đi qua bộ vẽ <Chu>.
 * chạy: node test/chu_vao_man.test.mjs
 *
 * Từ khi nội dung sang markdown + LaTeX, một chỗ in thẳng `{item.text}` là bé
 * thấy nguyên văn `$\frac{3}{4}$` trên màn. Đã dính THẬT hai lần, và cả hai chỉ
 * lộ khi mở mắt xem bản chạy:
 *
 *   · màn giảng dùng `step.screen.narration` (không có `?.`) nên phép thay hàng
 *     loạt trượt qua;
 *   · lời chào ở màn mở bài in thẳng `{loiChao}`.
 *
 * Phép kiểm này đọc MÃ NGUỒN, không đọc dữ liệu: tìm chỗ nào nội suy thẳng một
 * trường vốn có thể chứa LaTeX mà không bọc <Chu>. Máy khẳng định được điều ấy,
 * nên đừng để nó cho mắt người.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../src/components/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* Trường có thể chứa LaTeX — lấy từ TRUONG_CHU của tools/dinh_dang.py. */
const TRUONG = ['text', 'narration', 'solutionNarrative', 'problem', 'show',
  'kidText', 'mantra', 'wrong', 'fix', 'signal', 'counterExample', 'hint',
  'title', 'caption', 'onComplete', 'homeActivity', 'watchFor', 'answer',
  'solution', 'screenText', 'why', 'note', 'prompt', 'back', 'expected',
  /* Ba trường RIÊNG CỦA QUYỂN 2, lượt đầu bỏ sót cả ba. `loiChua` là chỗ đau nhất:
     nó hiện ở MỌI câu của màn chữa đề, và từ khi cả 314 câu đều máy chấm thì bé
     nào cũng đọc nó — mà nó in ra nguyên văn `$4,5 \\times 100 = 450$`. */
  'loiChua', 'thanChu', 'moTa'];
/* Cố ý KHÔNG canh `label`: ở AnswerFields nó là nhãn ô nhập (đã bọc <Chu>), còn ở
   StepView và mấy nút bấm thì `label` là TÊN NÚT — canh chung thì mọi cái nút đều
   bị báo, mà phép kiểm báo oan là phép kiểm bị bỏ qua. */

/* `{ x.text }` hoặc `{x?.text}` … đứng một mình trong JSX, không có <Chu> quanh. */
const R = new RegExp(
  String.raw`\{\s*[\w.?\[\]]*\b(${TRUONG.join('|')})\b\s*(\|\|[^}]*)?\}`, 'g');

const boSot = [];
for (const f of readdirSync(G).filter((x) => x.endsWith('.jsx') && x !== 'Chu.jsx')) {
  const src = readFileSync(join(G, f), 'utf8');
  for (const dong of src.split('\n')) {
    const d = dong.trim();
    if (d.startsWith('//') || d.startsWith('*') || d.startsWith('/*')) continue;
    if (d.includes('<Chu')) continue;                 // dòng đã bọc rồi
    const m = d.match(R);
    if (!m) continue;
    /* Chỉ tính khi nó thật sự được VẼ RA: nằm trong JSX, không phải một prop
       hay một tham số hàm. Dấu hiệu: dòng có thẻ, hoặc chuỗi đứng giữa hai thẻ. */
    if (!/[<>]/.test(d)) continue;
    /* `title` đứng một mình là tiêu đề MÀN (bảng cô giáo, thẻ hôm nay), không phải
       tên bài — tên bài luôn đi kèm `lesson.` hay `we.`. */
    if (/\{\s*title\s*\}/.test(d)) continue;
    /* `{back}` là nhãn nút "← quay lại", cùng lý do với `label`. */
    if (/\{\s*back\s*\}/.test(d)) continue;
    /* `{note}` ở màn đăng nhập là lời nhắn của hệ thống ("đã gửi mã"), không phải
       nội dung bài — không bao giờ chứa công thức. */
    if (/\{\s*note\s*\}/.test(d)) continue;
    if (/\w+=\{/.test(d) && !/>[^<]*\{/.test(d)) continue;   // là prop, không phải nội dung
    boSot.push(`${f}: ${d.slice(0, 88)}`);
  }
}
t(`mọi chỗ in trường có LaTeX đều qua <Chu> (bỏ sót: ${boSot.length})`, boSot.length === 0);
boSot.slice(0, 8).forEach((x) => console.log('     ', x));

console.log(`\n   soi ${readdirSync(G).filter((x) => x.endsWith('.jsx')).length} tệp giao diện`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
