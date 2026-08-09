/**
 * LỚP 5 — lời văn và hình có còn đúng tầm học sinh lớp 5 không.
 * chạy: node test/lop5.test.mjs
 *
 * Ba điều dưới đây đã phải sửa một lần trên cả 168 bài. Không có bài kiểm thì lần
 * sau nạp thêm nội dung, chúng mọc lại từng chỗ một mà chẳng ai thấy — mỗi chỗ
 * riêng lẻ đọc vẫn trôi, gộp lại mới thành quyển sách bé không hiểu.
 *
 * Chỉ soi TRƯỜNG BÉ ĐỌC. `mechanism`, `skills`, `videoSpec`, `numberRange` là ghi
 * chú của người soạn, không hiện lên màn hình — soi cả những chỗ ấy thì bài kiểm
 * đỏ vì lý do không ai cần sửa, rồi người sau sẽ tắt nó đi.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
const DATA = join(G, 'data/lessons');

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const BE_DOC = new Set([
  'title', 'objective.kidText', 'objective.text', 'objective.passRule',
  'knowledgeCore.mantra', 'knowledgeCore.statements[].text',
  'knowledgeCore.canonicalExamples[].problem', 'knowledgeCore.canonicalExamples[].solution',
  'knowledgeCore.canonicalExamples[].why', 'knowledgeCore.canonicalExamples[].case',
  'knowledgeCore.misconceptions[].wrong', 'knowledgeCore.misconceptions[].signal',
  'knowledgeCore.misconceptions[].fix', 'knowledgeCore.misconceptions[].counterExample',
  'lecture.screens[].narration', 'lecture.screens[].display.caption',
  'workedExample.title', 'workedExample.problem', 'workedExample.steps[].show',
  'workedExample.steps[].askBefore.text',
  'assessment.passRule', 'assessment.items[].text',
  'assessment.items[].solutionNarrative', 'assessment.items[].wrongFeedback',
  'figureSpec[].caption',
]);
const beDoc = (p) => BE_DOC.has(p)
  || /^practice\.pools\.(warmup|standard|challenge)\[\]\.(text|solutionNarrative|wrongFeedback|hints\[\])$/.test(p)
  || p.startsWith('figureSpec[].params.')
  || p === 'knowledgeCore.vocabulary[]';

/* Lớp 5 CHƯA học tập hợp, chia hết ký hiệu, ≤ ≥, suy ra. Dấu < > = ≠ thì học rồi. */
const VUOT_CAP = /[∈∉⊂∪∩⋮∤≡∀∃⇒⇔≤≥±∞⊥∥≈]/;
/* Mã của người soạn lọt ra màn hình: "K3 — hỏi ngược:", "Đ5.1", "Ca chuẩn K1+K2". */
const MA_NOI_BO = /^\s*(?:Ca\s+)?K\d+\b|\bĐ\d+\.\d+\b/;
/* Ví von bọc ngoài câu toán — bé cần biết đây là CÁCH TÍNH, không phải phép thuật. */
const VI_VON = /thần chú|bí kíp|phép thuật|phù thu[ỷy]/i;
/* Tiêu đề hình dài hơn ngưỡng này là một đoạn văn đè lên đầu hình, không ai đọc. */
const NGUONG_TIEU_DE = 120;

const kh = [], ma = [], vv = [], dai = [];
let soBai = 0, soHinh = 0;

const di = (o, p, id) => {
  if (Array.isArray(o)) return o.forEach((v) => di(v, `${p}[]`, id));
  if (o && typeof o === 'object') {
    return Object.entries(o).forEach(([k, v]) => di(v, p ? `${p}.${k}` : k, id));
  }
  if (typeof o !== 'string' || !beDoc(p)) return;
  if (VUOT_CAP.test(o)) kh.push(`${id} · ${p} · ${o.slice(0, 60)}`);
  if (MA_NOI_BO.test(o)) ma.push(`${id} · ${p} · ${o.slice(0, 60)}`);
  if (VI_VON.test(o)) vv.push(`${id} · ${p} · ${o.slice(0, 60)}`);
};

for (const ten of readdirSync(DATA).filter((x) => x.startsWith('DL_KSN5Q1_'))) {
  const d = JSON.parse(readFileSync(join(DATA, ten), 'utf8'));
  soBai++;
  di(d, '', d.id);
  for (const f of d.figureSpec || []) {
    soHinh++;
    const ti = f.params?.title || '';
    if (ti.length > NGUONG_TIEU_DE) dai.push(`${d.id}#${f.id} · ${ti.length} chữ`);
  }
}

t(`có đủ bài lớp 5 để soi (${soBai})`, soBai === 168);
const in3 = (xs) => xs.slice(0, 3).forEach((x) => console.log('     ', x));
t(`không ký hiệu vượt cấp lớp 5 (soi ${soHinh} hình + ${soBai} bài)`, kh.length === 0); in3(kh);
t('không mã nội bộ của người soạn lọt ra màn hình', ma.length === 0); in3(ma);
t('không ví von bọc ngoài câu toán', vv.length === 0); in3(vv);
t(`tiêu đề hình đủ ngắn để đọc (≤ ${NGUONG_TIEU_DE} chữ)`, dai.length === 0); in3(dai);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
