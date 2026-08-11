/**
 * CỔNG ĐÁP ÁN QUYỂN 2 — 314 câu đấu phải MÁY CHẤM ĐƯỢC, và chấm ĐÚNG.
 * chạy: node test/quyen2_dapan.test.mjs
 *
 * ── VÌ SAO ──
 * Quyển 2 vốn chỉ máy chấm 102/314 câu; 212 câu còn lại con tự chấm bằng ô tích
 * "Bài của con ĐÚNG như lời chữa". Đúng tinh thần "chữa đề kiểu giám khảo", nhưng
 * cái giá là sổ phụ huynh và bảng cô giáo KHÔNG ĐO ĐƯỢC GÌ ở quyển luyện thi — mà
 * đây lại là quyển cần đo nhất, vì nó có đồng hồ và có barem.
 *
 * 212 đáp án ấy nay viết TAY trong `data/quyen2_dapan_tay.json`. Viết tay thì sai
 * kiểu khác: gõ nhầm một chữ số, hay khai một con số sách không hề nói tới. Sai kiểu
 * ấy TỆ HƠN cả tự chấm — con làm đúng mà máy báo sai thì con mất tin vào phần mềm,
 * và điểm sai chảy thẳng vào sổ của bố mẹ.
 *
 * Nên phép kiểm này không đo "có đáp án chưa", nó đo BỐN việc:
 *
 *   1. MÁY CHẤM ĐƯỢC     mọi câu phải có ô trả lời, không câu nào rơi về tự luận;
 *   2. CHẤM ĐÚNG         nạp ngược chính đáp án vào bộ chấm — phải ra ĐÚNG;
 *   3. KHÔNG CHẤM BỪA    nạp một câu trả lời sai — phải ra SAI (bắt câu "gật đầu
 *                        với mọi thứ", lỗi đã có thật ở Quyển 1 với 68 câu);
 *   4. ĐÁP ÁN CÓ TRONG SÁCH  mọi con số của đáp án phải có mặt trong lời chữa.
 *                        Đây là chốt chặn duy nhất bắt được lỗi gõ nhầm và lỗi bịa,
 *                        vì máy không thể tự giải bài để đối chiếu.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import {
  checkAnswer, answerFields, answerMode, inputCount, normText,
} from '../src/mon/toan/lib/flow.js';

const D = new URL('../public/content/quyen2/', import.meta.url).pathname;
const GOC = new URL('../../data/', import.meta.url).pathname;

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const khoi = readdirSync(D).filter((f) => /^DR_KSN5Q2_[VTK]\d+\.json$/.test(f))
  .map((f) => JSON.parse(readFileSync(join(D, f), 'utf8')))
  .sort((a, b) => a.id.localeCompare(b.id));
const tay = JSON.parse(readFileSync(join(GOC, 'quyen2_dapan_tay.json'), 'utf8'));

const cau = khoi.flatMap((k) => k.cau.map((c) => ({ ...c, khoi: k.id, ma: k.id.split('.').pop() })));
t(`đọc đủ ${khoi.length} khối · ${cau.length} câu`, khoi.length === 21 && cau.length === 314);

/* ══ 1 · MỌI CÂU ĐỀU MÁY CHẤM ĐƯỢC ══
   `tuLuan` là cờ cũ đánh dấu câu để con tự chấm. Còn sót cờ ấy trên câu đã có đáp án
   thì hai nguồn sự thật đá nhau — màn chữa đề hiện cả ô tự chấm lẫn kết quả máy. */
const thieu = cau.filter((c) => !c.answerKey);
t(`câu nào cũng có đáp án (thiếu: ${thieu.length})`, thieu.length === 0);
in5(thieu.map((c) => `${c.ma}#${c.id}`));

const conTuLuan = cau.filter((c) => c.tuLuan);
t(`không còn cờ tuLuan sót lại (${conTuLuan.length})`, conTuLuan.length === 0);

const khongCoO = cau.filter((c) => inputCount(c) === 0 || answerMode(c) === 'tuluan');
t(`câu nào cũng dựng được ô trả lời (${khongCoO.length} câu không có ô)`, khongCoO.length === 0);
in5(khongCoO.map((c) => `${c.ma}#${c.id} · ${answerMode(c)}`));

/* ══ 2 · NẠP NGƯỢC ĐÁP ÁN VÀO BỘ CHẤM — PHẢI RA ĐÚNG ══
   Đây là phép kiểm đắt nhất tệp này: nó chạy đúng đường mà con sẽ đi, chứ không đọc
   dữ liệu suông. Khai một đáp án bộ chấm không hiểu (dãy so sánh ba vế, phân số viết
   liền chữ…) là đỏ ngay tại đây, không đợi con làm bài mới lộ. */
function dapDung(c) {
  const key = c.answerKey || {};
  if (c.format === 'mcq') return key.choice;
  if (key.values) return key.values.join('; ');
  if (key.parts) {
    return key.parts.filter((p) => Array.isArray(p.options) || String(p.value).length <= 26)
      .map((p) => String(p.value));
  }
  return String(key.value);
}

const chamSai = [];
for (const c of cau) {
  const r = checkAnswer(c, dapDung(c));
  if (!r.ok || r.mode === 'selfcheck') chamSai.push(`${c.ma}#${c.id} · ${r.mode} · mong "${r.expected}"`);
}
t(`nạp đúng đáp án thì bộ chấm nhận (${chamSai.length} câu không nhận)`, chamSai.length === 0);
in5(chamSai);

/* ══ 3 · KHÔNG CHẤM BỪA ══
   Câu "gật đầu với mọi thứ" nguy hiểm hơn câu chấm sai: con bỏ trống cũng ĐẠT, nên
   điểm trong sổ là điểm ma. Ở Quyển 1 đã có thật — 68 câu Đúng/Sai nhận ô rỗng
   thành `false` rồi chấm đúng. Thử hai câu trả lời chắc chắn sai với MỌI câu. */
const gatDau = [];
for (const c of cau) {
  const n = Math.max(inputCount(c), 1);
  for (const bua of ['', 'zzz']) {
    const r = checkAnswer(c, c.format === 'mcq' ? bua : Array(n).fill(bua));
    if (r.ok && r.mode !== 'selfcheck') { gatDau.push(`${c.ma}#${c.id} · nhận "${bua || '(bỏ trống)'}"`); break; }
  }
}
t(`bỏ trống hoặc gõ bừa thì bị chấm SAI (${gatDau.length} câu gật đầu)`, gatDau.length === 0);
in5(gatDau);

/* ══ 4 · ĐÁP ÁN PHẢI CÓ MẶT TRONG LỜI CHỮA CỦA SÁCH ══
   Máy không tự giải được bài để đối chiếu, nhưng nó khẳng định được điều này: mọi
   con số trong đáp án phải xuất hiện trong lời chữa. Gõ nhầm 4,1 thành 4,7 hay bịa
   ra một đáp số là đỏ ngay — không phải trông vào việc ai đó soi lại 212 câu.

   Bỏ dấu phân nghìn trước khi so: sách viết "1 050", đáp án có thể ghi "1050". */
const boNghin = (s) => String(s ?? '').replace(/(\d)[\s ](?=\d)/g, '$1');
const SO = /-?\d[\d.,]*/g;

const lac = [];
for (const c of cau) {
  const key = c.answerKey || {};
  const nguon = boNghin(normText(`${c.loiChua} ${c.text}`));
  const dinh = c.format === 'mcq' ? [key.choice]
    : key.values ? key.values
      : key.parts ? key.parts.map((p) => p.value)
        : [key.value];
  for (const v of dinh) {
    for (const so of String(v ?? '').match(SO) || []) {
      const s = boNghin(so).replace(/[.,;]+$/, '');
      /* Chữ số lẻ loi (0-9) bỏ qua: một con số một chữ số gần như luôn có mặt đâu đó
         trong lời chữa, nên phép kiểm không nói lên điều gì — mà lại dễ đỏ oan. */
      if (s.length < 2) continue;
      if (!nguon.includes(s)) lac.push(`${c.ma}#${c.id} · "${so}" không có trong lời chữa`);
    }
  }
}
t(`mọi con số của đáp án đều có trong lời chữa (${lac.length} chỗ lạc)`, lac.length === 0);
in5(lac);

/* ══ 5 · TRẮC NGHIỆM: MỒI PHẢI ĐỦ, KHÁC NHAU, VÀ ĐÁP ÁN PHẢI NẰM TRONG BỘ NÚT ══
   Lệch một chữ là con bấm đúng mà máy báo sai — mà con thì tin máy chứ không tin mình. */
const mcq = cau.filter((c) => c.format === 'mcq');
const loiMcq = [];
for (const c of mcq) {
  const ds = c.choices || [];
  if (ds.length < 2) loiMcq.push(`${c.ma}#${c.id} · chỉ ${ds.length} nút`);
  if (new Set(ds.map(normText)).size !== ds.length) loiMcq.push(`${c.ma}#${c.id} · có hai nút trùng chữ`);
  if (!ds.some((x) => normText(x) === normText(c.answerKey.choice)))
    loiMcq.push(`${c.ma}#${c.id} · đáp án không nằm trong bộ nút`);
}
t(`trắc nghiệm dựng đúng (${mcq.length} câu · ${loiMcq.length} lỗi)`, loiMcq.length === 0);
in5(loiMcq);

/* Ô bấm chọn nằm TRONG `parts` cũng chịu đúng luật ấy. */
const loiChon = [];
for (const c of cau) {
  for (const p of c.answerKey?.parts || []) {
    if (!Array.isArray(p.options)) continue;
    if (p.options.length < 2) loiChon.push(`${c.ma}#${c.id} · ô "${p.label}" chỉ một nút`);
    if (!p.options.some((x) => normText(x) === normText(p.value)))
      loiChon.push(`${c.ma}#${c.id} · ô "${p.label}" đáp án ngoài bộ nút`);
  }
}
t(`ô bấm chọn trong parts dựng đúng (${loiChon.length} lỗi)`, loiChon.length === 0);
in5(loiChon);

/* ══ 6 · Ô NÀO CŨNG CÓ NHÃN, VÀ NHÃN KHÔNG ĐƯA SẴN ĐÁP ÁN ══ */
const loiNhan = [];
for (const c of cau) {
  const ps = c.answerKey?.parts || [];
  if (ps.length > 1 && ps.some((p) => !String(p.label || '').trim()))
    loiNhan.push(`${c.ma}#${c.id} · có ô thiếu nhãn`);
  if (new Set(ps.map((p) => normText(p.label))).size !== ps.length)
    loiNhan.push(`${c.ma}#${c.id} · hai ô trùng nhãn`);
  for (const p of ps) {
    if (Array.isArray(p.options)) continue;              // ô bấm chọn thì nhãn không lộ gì
    if (normText(p.label).includes(normText(p.value)) && String(p.value).length >= 2)
      loiNhan.push(`${c.ma}#${c.id} · nhãn "${p.label}" cho không đáp án`);
  }
  /* Chữ mờ trong ô cũng không được lộ đáp án — con nhìn vào là đọc ra đáp số. */
  for (const f of answerFields(c)) {
    const ph = normText(f.placeholder);
    const dap = normText(String(c.answerKey?.value ?? ''));
    if (dap.length >= 2 && ph.includes(dap))
      loiNhan.push(`${c.ma}#${c.id} · chữ mờ lộ đáp án "${dap}"`);
  }
}
t(`nhãn và chữ mờ không lộ đáp án (${loiNhan.length} lỗi)`, loiNhan.length === 0);
in5(loiNhan);

/* ══ 7 · SỔ TAY KHỚP DỮ LIỆU ══
   Khoá thừa trong sổ tay nghĩa là câu ấy đã bị đổi mã hoặc bị bỏ — đáp án viết ra
   không tới được đâu cả, mà chạy công cụ vẫn êm. */
const khoaTay = Object.keys(tay).filter((k) => !k.startsWith('_'));
const coThat = new Set(cau.map((c) => `${c.ma}#${c.id}`));
const thuaKhoa = khoaTay.filter((k) => !coThat.has(k));
t(`sổ tay không có khoá thừa (${thuaKhoa.length})`, thuaKhoa.length === 0);
in5(thuaKhoa);
t(`sổ tay khai đủ 212 câu`, khoaTay.length === 212);

/* ══ 8 · BẢN GỐC VÀ BẢN DỰNG KHAI CÙNG MỘT ĐÁP ÁN ══
   `data/quyen2` là bản gốc, `public/content/quyen2` là bản đã qua bộ định dạng. Hai
   nơi lệch đáp án thì bản chạy chấm một kiểu, bản gốc ghi một kiểu — và chỉ lộ ra
   khi có người ngồi so từng câu. */
const GOC_Q2 = new URL('../../data/quyen2/', import.meta.url).pathname;
const lechGoc = [];
for (const k of khoi) {
  const g = JSON.parse(readFileSync(join(GOC_Q2, `${k.id.replace('DR:', 'DR_').replace(/\./g, '_')}.json`), 'utf8'));
  const m = new Map(g.cau.map((c) => [c.id, c]));
  for (const c of k.cau) {
    const gc = m.get(c.id);
    if (JSON.stringify(gc?.answerKey) !== JSON.stringify(c.answerKey)
        || gc?.format !== c.format)
      lechGoc.push(`${k.id.split('.').pop()}#${c.id}`);
  }
}
t(`bản gốc và bản dựng cùng một đáp án (${lechGoc.length} chỗ lệch)`, lechGoc.length === 0);
in5(lechGoc);

/* ─────────── tổng kết ─────────── */
const theoKieu = {};
for (const c of cau) theoKieu[answerMode(c)] = (theoKieu[answerMode(c)] || 0) + 1;
console.log(`\n   ${cau.length} câu · máy chấm ${cau.length - thieu.length}/${cau.length}`
  + ` (trước đợt này 102) · ${mcq.length} câu trắc nghiệm`);
console.log('   kiểu trả lời: '
  + Object.entries(theoKieu).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(' · '));
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
