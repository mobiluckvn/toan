/**
 * Chạy: node test/flow.test.mjs
 * Kiểm lõi logic trên DỮ LIỆU THẬT của cả 168 micro.
 */
import fs from 'fs';
import {
  parseNum, nearEq, checkAnswer, inputCount, buildFlow, gradeMicro, hintState, PHASES, isSelfCheck,
  buildWorkedSteps, sampleParts, askIsMcq,
  parseRange, isArithmeticRule, evalRule, canGenerate, makeVariant,
  inputPlaceholder, choicesFromText, splitAside, parseCompare, buildTeachSteps,
  answerFields, answerBrief, answerCore, isNumberList,
} from '../src/lib/flow.js';

const DIR = 'public/content/lessons';
const ids = [];
for (let b = 1; b <= 56; b++) for (const k of [1, 2, 3]) ids.push(`DL_KSN5Q1_B${b}_M${k}.json`);
const lessons = ids.map((f) => JSON.parse(fs.readFileSync(`${DIR}/${f}`, 'utf8')));

let pass = 0, fail = 0;
const t = (name, cond) => { cond ? pass++ : (fail++, console.log('  ✗', name)); };

/* ── 1. parse số kiểu Việt ── */
t('parseNum "0,785"', nearEq(parseNum('0,785'), 0.785));
t('parseNum "1 256"', nearEq(parseNum('1 256'), 1256));
t('parseNum rỗng → NaN', Number.isNaN(parseNum('')));
t('nearEq sai số 0,004', nearEq(3.14, 3.144));
t('nearEq bác 0,01', !nearEq(3.14, 3.15));

/* ── 2. chấm đủ mọi format có trong dữ liệu ── */
const fmts = new Set();
let items = 0, autoOK = 0, autoTot = 0, selfCnt = 0;
for (const L of lessons) {
  const all = [
    ...Object.values(L.practice?.pools || {}).flat(),
    ...(L.assessment?.items || []),
  ];
  for (const it of all) {
    items++; fmts.add(it.format);
    const key = it.answerKey || {};
    let input;
    if (it.format === 'tf') input = key.value;
    else if (it.format === 'mcq') input = key.choice;
    else if (key.values) input = key.values.join('; ');
    else if (key.accept) input = String([].concat(key.accept)[0]);
    else if (key.parts) input = key.parts.filter((p) => !isSelfCheck(p.value)).map((p) => String(p.value).replace('.', ','));
    else if (key.value !== undefined) input = String(key.value).replace('.', ',');
    const r = checkAnswer(it, input);
    if (r.mode === 'selfcheck') { selfCnt++; continue; }
    autoTot++;
    if (r.ok) autoOK++;
    else console.log('  ✗ chấm sai:', L.id, it.id, it.format, JSON.stringify(key).slice(0, 80));
  }
}
t(`chấm đúng đáp án chuẩn: ${autoOK}/${autoTot}`, autoOK === autoTot);
console.log(`   tổng câu ${items} · máy chấm ${autoTot} · tự đối chiếu ${selfCnt}`);
console.log('   format gặp trong dữ liệu:', [...fmts].join(', '));

/* ── 3. đáp SAI phải bị chấm sai ── */
let wrongOK = 0, wrongTot = 0;
for (const L of lessons.slice(0, 40)) {
  for (const it of (L.assessment?.items || [])) {
    const key = it.answerKey || {};
    let bad;
    if (it.format === 'tf') bad = !key.value;
    else if (it.format === 'mcq') bad = (it.choices || []).find((c) => c !== key.choice);
    else if (key.value !== undefined && typeof key.value === 'number') bad = String(key.value + 7);
    else continue;
    if (bad === undefined) continue;
    wrongTot++;
    if (!checkAnswer(it, bad).ok) wrongOK++;
  }
}
t(`bác đáp sai: ${wrongOK}/${wrongTot}`, wrongOK === wrongTot);

/* ── 4. dựng flow cho cả 168 micro ── */
let minSteps = 1e9, maxSteps = 0, noFig = 0, badPhase = 0;
for (const L of lessons) {
  const flow = buildFlow(L);
  minSteps = Math.min(minSteps, flow.length); maxSteps = Math.max(maxSteps, flow.length);
  if (!flow.some((s) => s.figure)) noFig++;
  if (!flow.every((s) => PHASES.some((p) => p.id === s.phase))) badPhase++;
  const types = flow.map((s) => s.type);
  if (!types.includes('intro') || !types.includes('finale')) console.log('  ✗ thiếu đầu/cuối:', L.id);
  if (!types.includes('teach')) console.log('  ✗ thiếu chặng GIẢNG:', L.id);
  if (!types.includes('practice')) console.log('  ✗ thiếu LUYỆN:', L.id);
  if (!types.includes('assess')) console.log('  ✗ thiếu SÁT HẠCH:', L.id);
}
t('mọi micro dựng được flow', minSteps > 0);
t('mọi bước có phase hợp lệ', badPhase === 0);
t('mọi micro có ít nhất 1 hình trong flow', noFig === 0);
console.log(`   số bước mỗi micro: ${minSteps} – ${maxSteps}`);

/* ── 5. luật đạt ── */
const A1 = { id: 'A1', ok: true, mustPass: true };
t('3 đúng → đạt', gradeMicro([A1, { ok: true }, { ok: true }], '≥ 2/3, bắt buộc đúng A1').pass);
t('sai câu bẫy → KHÔNG đạt',
  !gradeMicro([{ id: 'A1', ok: false, mustPass: true }, { ok: true }, { ok: true }], '≥ 2/3').pass);
t('chỉ 1 đúng → không đạt', !gradeMicro([A1, { ok: false }, { ok: false }], '≥ 2/3').pass);
t('luật ≥3/4 đọc đúng ngưỡng', gradeMicro([A1, { ok: true }, { ok: true }, { ok: false }], '≥ 3/4').need === 3);

/* ── 6. gợi ý hai tầng ── */
const withHints = lessons.flatMap((L) => Object.values(L.practice?.pools || {}).flat())
  .find((i) => (i.hints || []).length >= 2);
t('sai 1 lần → 1 gợi ý', hintState(withHints, 1).show.length === 1);
t('sai 2 lần → 2 gợi ý', hintState(withHints, 2).show.length === 2);
t('sai 3 lần → mở đáp án', hintState(withHints, 3).reveal === true);

/* ── 7. số ô nhập ── */
const mb = lessons.flatMap((L) => Object.values(L.practice?.pools || {}).flat())
  .find((i) => i.answerKey?.parts?.filter((p) => typeof p.value === 'number').length >= 2);
t('câu nhiều phần → nhiều ô nhập', inputCount(mb) >= 2);
t('câu trắc nghiệm → 0 ô nhập', inputCount({ format: 'mcq', choices: ['a', 'b'] }) === 0);
t('đáp chữ ngắn vẫn chấm được', checkAnswer({format:'mb', answerKey:{parts:[{label:'đến', value:'7 giờ 05 phút'}]}}, ['7 giờ 05 phút']).ok);
t('chấm chữ bỏ qua hoa/thường', checkAnswer({format:'mb', answerKey:{parts:[{label:'đuổi', value:'HIỆU'}]}}, ['hiệu']).ok);
t('đáp chữ sai bị bác', !checkAnswer({format:'mb', answerKey:{parts:[{label:'đuổi', value:'HIỆU'}]}}, ['tổng']).ok);
t('giải thích dài → tự đối chiếu', checkAnswer({format:'mb', answerKey:{parts:[{label:'căn cứ', value:'Hai tam giác ABM và AMC có chung chiều cao hạ từ A'}]}}, ['']).mode === 'selfcheck');

/* ── 7b. NỚI CHẤM: con làm đúng toán thì không được đánh trượt vì cách gõ ── */
const one = (v, input) => checkAnswer({ format: 'num', answerKey: { value: v } }, input).ok;

/* đơn vị đo: gõ kèm hay không cũng nhận */
t('"60000" cho đáp "60 000 đồng"',      one('60 000 đồng', '60000'));
t('"60 000" cho đáp "60 000 đồng"',     one('60 000 đồng', '60 000'));
t('"60000 đ" cho đáp "60 000 đồng"',    one('60 000 đồng', '60000 đ'));
t('"25" cho đáp "25%"',                 one('25%', '25'));
t('"25%" cho đáp "25%"',                one('25%', '25%'));
t('"19 cây" cho đáp số trần 19',        one(19, '19 cây'));
t('"19" cho đáp số trần 19',            one(19, '19'));
t('sai số thì vẫn bác dù đúng đơn vị',  !one('60 000 đồng', '50 000 đồng'));

/* phần chữ ĐỔI NGHĨA thì vẫn phải bác */
t('"2 năm nữa" KHÔNG phải "2 năm trước"', !one('2 năm trước', '2 năm nữa'));
t('"2" vẫn nhận cho "2 năm trước"',        one('2 năm trước', '2'));
t('"TĂNG" không phải "GIẢM"',             !one('GIẢM', 'TĂNG'));

/* dấu Unicode trong dữ liệu vs dấu con gõ được */
t('"1 - 1/20" cho đáp "1 − 1/20"',      one('1 − 1/20', '1 - 1/20'));
t('"co - 11 x 8" cho đáp "có — 11 × 8"', one('có — 11 × 8', 'có - 11 x 8'));

/* phân số ↔ thập phân */
t('"0,75" cho đáp "3/4"',               one('3/4', '0,75'));
t('"3/4" cho đáp "3/4"',                one('3/4', '3/4'));
t('"1/3" KHÔNG phải "1/2"',             !one('1/2', '1/3'));
t('"19/20" cho đáp "19/20"',            one('19/20', '19/20'));

/* danh sách nhiều số: dấu ngăn cách nào cũng nhận, thiếu số là sai */
const lstItem = { format: 'lst', answerKey: { values: [12, 24, 36, 48], ordered: true } };
const lstOK = (input) => checkAnswer(lstItem, input).ok;
t('danh sách ngăn bằng ";"',            lstOK('12; 24; 36; 48'));
t('danh sách ngăn bằng ","',            lstOK('12, 24, 36, 48'));
t('danh sách ngăn bằng khoảng trắng',   lstOK('12 24 36 48'));
t('danh sách thiếu một số → sai',      !lstOK('12; 24; 36'));
t('danh sách sai thứ tự → sai',        !lstOK('24; 12; 36; 48'));
t('danh sách không còn tự-động-đúng',   checkAnswer(lstItem, '').mode === 'auto' && !lstOK(''));
t('câu danh sách có 1 ô nhập',          inputCount(lstItem) === 1);

/* ── 7c. TƯỜNG MINH: ô nhập nói rõ chờ dạng gì, và bớt bắt gõ chữ ── */
/* lý do trong ngoặc là "vì sao", không phải đáp án */
t('"bằng nhau" cho đáp "bằng nhau (0 đuôi bỏ được)"', one('bằng nhau (0 đuôi bỏ được)', 'bằng nhau'));
t('vẫn nhận nếu con gõ cả phần ngoặc',   one('bằng nhau (0 đuôi bỏ được)', 'bằng nhau (0 đuôi bỏ được)'));
t('"khác nhau" không phải "bằng nhau"', !one('bằng nhau (0 đuôi bỏ được)', 'khác nhau'));
t('đáp dài nhưng lõi ngắn → chấm được', !isSelfCheck('KHÁC nhau (0 giữa giữ chỗ hàng phần mười)'));
t('đáp dài thật vẫn tự đối chiếu',       isSelfCheck('Hai tam giác ABM và AMC có chung chiều cao hạ từ A'));

/* so sánh: viết ngược lại vẫn là một khẳng định */
t('"7/8 < 9/10" đúng',                   one('7/8 < 9/10', '7/8 < 9/10'));
t('"9/10 > 7/8" cũng đúng',              one('7/8 < 9/10', '9/10 > 7/8'));
t('"7/8 > 9/10" thì SAI',               !one('7/8 < 9/10', '7/8 > 9/10'));
t('so sánh dùng thập phân cũng nhận',    one('7/8 < 9/10', '0,875 < 0,9'));

/* đáp "X = Y" trong một ô: ngăn cách kiểu nào cũng nhận */
t('"0,75 = 75%" đúng',                   one('0,75 = 75%', '0,75 = 75%'));
t('"0,75; 75%" cũng đúng',               one('0,75 = 75%', '0,75; 75%'));
t('"0,75 = 70%" thì SAI',               !one('0,75 = 75%', '0,75 = 70%'));

/* chữ mờ trong ô: mô tả dạng, KHÔNG lộ đáp án */
const ph = (v, item = {}) => inputPlaceholder(item, null, v);
t('ô so sánh gợi ý dạng',                ph('7/8 < 9/10') === 'vd: 3/4 > 2/5');
t('chữ mờ không lộ đáp án',             !ph('7/8 < 9/10').includes('9/10'));
t('ô có đơn vị hiện tên đơn vị',         ph('60 000 đồng') === 'điền số, đơn vị là đồng');
t('ô phần trăm hiện dấu %',              ph('25%') === 'điền số, đơn vị là %');
t('chữ mờ đơn vị không lộ con số',      !/\d/.test(ph('60 000 đồng')));
t('ô số trơn vẫn nói rõ điền số',        inputPlaceholder({}, 'chiều dài', 12) === 'điền số');
t('ô đáp án bằng chữ nói rõ gõ chữ',     ph('không đổi') === 'trả lời bằng chữ');
t('không ô nào còn hiện dấu "?" trơ trọi',
  ['12', '25%', 'không đổi', '7/8 < 9/10'].every((v) => ph(v) !== '?'));

/* đề tự nói bộ đáp án → cho bấm chọn */
t('rút được lựa chọn từ đề',
  JSON.stringify(choicesFromText({ text: 'Điền TĂNG hoặc GIẢM: quên dấu phẩy ở số TRỪ thì hiệu ...' }))
  === JSON.stringify(['TĂNG', 'GIẢM']));
t('rút được lựa chọn có ngoặc kép',
  JSON.stringify(choicesFromText({ text: 'Điền "tổng" hoặc "hiệu": đuổi nhau cùng chiều chia ... vận tốc.' }))
  === JSON.stringify(['tổng', 'hiệu']));
t('đề không nói thì không đoán bừa',     choicesFromText({ text: 'Tính 25% của 240 000 đồng.' }) === null);

/* ── 7d. CHẶNG GIẢNG: không còn màn trống, lời giảng đúng nguyên tắc ── */
let teachEmpty = 0, teachLost = 0, teachOrphan = 0, teachMax = 0, teachSteps = 0;
for (const L of lessons) {
  const ts = buildTeachSteps(L);
  const K = (L.knowledgeCore?.statements || []).map((s) => s.id);
  const shown = ts.flatMap((s) => s.statements.map((x) => x.id));
  teachSteps += ts.length;
  teachMax = Math.max(teachMax, ts.length);
  if (K.length !== shown.length || K.some((id) => !shown.includes(id))) teachLost++;
  for (const s of ts) {
    // màn chỉ có mỗi một dòng chữ, không hình không lời giảng — thứ con bấm qua mà không học được gì
    if (!s.screen?.narration && !s.figure) teachEmpty++;
    // lời giảng phải nói về đúng những nguyên tắc đứng cùng màn
    const t = s.screen?.teaches || [];
    if (t.length && s.statements.length && !s.statements.some((x) => t.includes(x.id))) teachOrphan++;
  }
}
t(`không micro nào mất nguyên tắc: ${168 - teachLost}/168`, teachLost === 0);
t(`không còn màn GIẢNG trống trơn (${teachEmpty} màn)`, teachEmpty === 0);
t(`lời giảng khớp nguyên tắc cùng màn (${teachOrphan} lệch)`, teachOrphan === 0);
console.log(`   chặng GIẢNG: ${teachSteps} màn cho 168 micro (nhiều nhất ${teachMax} màn/micro)`);

/* ── 8. ví dụ dẫn dắt bung thành chuỗi bước ── */
let weTot = 0, weAsk = 0, weBad = 0, weMin = 1e9, weMax = 0;
for (const L of lessons) {
  const we = L.workedExample;
  if (!we) { console.log('  ✗ thiếu workedExample:', L.id); weBad++; continue; }
  const seq = buildWorkedSteps(we);
  weTot++; weMin = Math.min(weMin, seq.length); weMax = Math.max(weMax, seq.length);
  const shows = seq.filter((s) => s.kind === 'show').length;
  if (shows !== we.steps.length) { console.log('  ✗ lệch số bước show:', L.id); weBad++; }
  for (const s of seq.filter((x) => x.kind === 'ask')) {
    weAsk++;
    if (!s.item.text) { console.log('  ✗ câu hỏi xen giữa thiếu đề:', L.id); weBad++; }
    // câu hỏi xen giữa phải chấm được bằng đúng bộ chấm chung
    const key = s.item.answerKey || {};
    const input = askIsMcq(s.item) ? key.choice
      : (key.value !== undefined ? String(key.value).replace('.', ',') : null);
    if (input !== null && !checkAnswer(s.item, input).ok) {
      console.log('  ✗ không chấm được câu xen giữa:', L.id, JSON.stringify(key).slice(0, 60)); weBad++;
    }
  }
}
t(`bung ví dụ dẫn dắt cho ${weTot} micro`, weTot === 168 && weBad === 0);
console.log(`   bước con mỗi ví dụ: ${weMin} – ${weMax} · tổng câu hỏi xen giữa: ${weAsk}`);

/* ── 9. tách nhãn ca mẫu ── */
const exs = lessons.flatMap((L) => L.knowledgeCore?.canonicalExamples || []);
const parsed = exs.map(sampleParts);
t('mọi ca mẫu có đề và lời giải', parsed.every((p) => p.problem && p.solution));
t('tách được nhãn loại ca', parsed.filter((p) => p.kind).length / parsed.length > 0.9);
console.log(`   tổng ca mẫu: ${exs.length} · có nhãn loại: ${parsed.filter((p) => p.kind).length}`);
/* ── 10. hình được gắn đúng chặng ── */
let sampleWithFig = 0, workedWithFig = 0, teachWithFig = 0;
for (const L of lessons) {
  const flow = buildFlow(L);
  if (flow.filter((s) => s.type === 'sample' && s.figure).length > 0) sampleWithFig++;
  if (flow.some((s) => s.type === 'worked' && s.figure)) workedWithFig++;
  if (flow.filter((s) => s.type === 'teach' && s.figure).length >= 2) teachWithFig++;
}
t(`ca mẫu có hình: ${sampleWithFig}/168`, sampleWithFig === 168);
t(`ví dụ dẫn dắt có hình: ${workedWithFig}/168`, workedWithFig === 168);
t(`chặng GIẢNG có ≥ 2 hình: ${teachWithFig}/168`, teachWithFig === 168);

/* ── 11. mọi hình gắn vào flow đều tồn tại trong figureSpec ── */
let badFig = 0;
for (const L of lessons) {
  const files = new Set((L.figureSpec || []).map((f) => f.file));
  for (const s of buildFlow(L)) if (s.figure && !files.has(s.figure.file)) badFig++;
}
t('không có hình lạc', badFig === 0);

/* ── 12. sinh đề biến thể — đo tỉ lệ metadata đủ dùng ── */
t('parseRange "1–9"', parseRange('1–9')?.hi === 9);
t('parseRange mô tả bằng lời → null', parseRange('số tự nhiên 4 chữ số') === null);
t('evalRule "a × b + c"', evalRule('a × b + c', { a: 3, b: 4, c: 2 }) === 14);
t('evalRule dấu chia ":"', evalRule('S : T', { S: 45, T: 3 }) === 15);
t('evalRule chặn tên lạ', Number.isNaN(evalRule('a + fetch', { a: 1 })));

const gens = lessons.flatMap((L) => Object.values(L.practice?.pools || {}).flat()).filter((i) => i.generator);
const okGen = gens.filter((i) => canGenerate(i));
console.log(`   câu có generator: ${gens.length} · sinh biến thể được: ${okGen.length} (${Math.round(okGen.length / gens.length * 100)}%)`);
t('có ít nhất vài câu sinh được', okGen.length > 0);

let seed = 42; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
let vOK = 0;
for (const it of okGen) {
  const v = makeVariant(it, rnd);
  if (!v) continue;
  if (!/\{/.test(v.text) && checkAnswer(v, String(v.answerKey.value).replace('.', ',')).ok) vOK++;
}
t(`biến thể sinh ra tự chấm đúng: ${vOK}/${okGen.length}`, vOK === okGen.length);
t('câu không đủ metadata → null (không sinh bừa)', makeVariant({ generator: { template: 'x {a}', constraints: { a: 'một chữ số' }, answerRule: 'a' } }) === null);

/* ── 13. mô phỏng một lượt học trọn micro (không cần trình duyệt) ── */
function playThrough(L, answerRight = true) {
  const flow = buildFlow(L);
  const log = { practice: [], assess: [] };
  for (const s of flow) {
    if (s.type === 'practice' || s.type === 'assess') {
      const key = s.item.answerKey || {};
      let input;
      if (s.item.format === 'tf') input = answerRight ? key.value : !key.value;
      else if (s.item.format === 'mcq')
        input = answerRight ? key.choice : (s.item.choices || []).find((c) => c !== key.choice);
      else if (key.values) input = answerRight ? key.values.join('; ') : '0';
      else if (key.parts) input = key.parts.filter((p) => !isSelfCheck(p.value))
        .map((p) => answerRight ? String(p.value).replace('.', ',') : 'sai');
      else if (key.value !== undefined) input = answerRight ? String(key.value).replace('.', ',') : 'sai';
      const r = checkAnswer(s.item, input);
      log[s.type === 'practice' ? 'practice' : 'assess'].push(
        s.type === 'assess' ? { id: s.item.id, ok: r.ok, mustPass: !!s.item.mustPass }
                            : { id: s.item.id, ok: r.ok, tries: 1 });
    }
  }
  return gradeMicro(log.assess, L.assessment?.passRule || '');
}
let passAll = 0, failAll = 0;
for (const L of lessons) {
  if (playThrough(L, true).pass) passAll++;
  if (!playThrough(L, false).pass) failAll++;
}
t(`làm đúng hết → ĐẠT ở ${passAll}/168 micro`, passAll === 168);
t(`làm sai hết → KHÔNG đạt ở ${failAll}/168 micro`, failAll === 168);

/* ══════════════════════════════════════════════════════════════════════════
   CON CÓ LÀM ĐƯỢC BÀI KHÔNG — soi 100% câu hỏi trong 168 micro.

   Đây là hàng rào chặn đúng những lỗi đã gặp: câu không có chỗ điền, ô nhập
   không nhãn, nhiều ô mà nhãn trùng nhau, chữ mờ trơ trọi dấu "?".
   ══════════════════════════════════════════════════════════════════════════ */
function everyItem(L) {
  const out = [];
  for (const [lv, arr] of Object.entries(L.practice?.pools || {}))
    arr.forEach((it, i) => out.push([`practice.${lv}[${i}]`, it]));
  (L.assessment?.items || []).forEach((it, i) => out.push([`assessment[${i}]`, it]));
  (L.lecture?.screens || []).forEach((s, i) => s.item && out.push([`screens[${i}].item`, s.item]));
  (L.workedExample?.steps || []).forEach((s, i) => {
    for (const k of ['askBefore', 'askAfter']) if (s[k]) out.push([`worked[${i}].${k}`, s[k]]);
  });
  return out;
}

const bad = { noWay: [], noLabel: [], dupLabel: [], bareQ: [], noBrief: [] };
let qs = 0, boxes = 0;
for (const L of lessons) {
  for (const [where, it] of everyItem(L)) {
    qs++;
    const isChoice = it.format === 'tf' || it.format === 'mcq';
    const fields = answerFields(it);
    boxes += fields.length;
    const ref = `${L.id} ${where}`;

    // trắc nghiệm phải có ít nhất 2 lựa chọn để bấm
    if (isChoice && it.format === 'mcq' && (it.choices || []).length < 2) bad.noWay.push(ref);
    // không phải trắc nghiệm, không có ô nhập → chỉ chấp nhận khi ĐÚNG là câu tự luận
    if (!isChoice && fields.length === 0) {
      const k = it.answerKey || {};
      const prose = k.parts ? k.parts.every((p) => isSelfCheck(p.value)) : isSelfCheck(k.value);
      if (!prose) bad.noWay.push(ref);
    }
    if (!answerBrief(it)) bad.noBrief.push(ref);

    const labels = fields.map((f) => f.label);
    if (labels.some((l) => !l || !String(l).trim())) bad.noLabel.push(ref);
    if (fields.length >= 2 && new Set(labels).size < labels.length) bad.dupLabel.push(`${ref} ${JSON.stringify(labels)}`);

    // Bài NHIỀU ô phải có nhãn THẬT trong dữ liệu. answerFields có nhãn dự phòng
    // ("ô thứ 2") để con không bao giờ thấy ô trống tên, nhưng dự phòng thì vô nghĩa —
    // kiểm ở đây trên dữ liệu gốc, nếu không hàng rào này không bao giờ đỏ được.
    if (fields.length >= 2) {
      const raw = (it.answerKey?.parts || []).filter((p) => !isSelfCheck(p.value))
        .map((p) => String(p.label || '').trim());
      if (raw.length < fields.length || raw.some((l) => !l)) bad.noLabel.push(`${ref} (nhãn dự phòng)`);
    }
    for (const f of fields) if (f.placeholder === '?' || !f.placeholder) bad.bareQ.push(ref);
  }
}
/** đạt khi danh sách RỖNG; không đạt thì in ra vài ví dụ để lần ra ngay */
const tEmpty = (name, list) => {
  if (list.length) console.log('   ', list.slice(0, 3).join(' | ') + (list.length > 3 ? ` …+${list.length - 3}` : ''));
  t(name, list.length === 0);
};
tEmpty(`mọi câu đều có cách trả lời (${qs} câu)`, bad.noWay);
tEmpty('mọi ô nhập đều có nhãn', bad.noLabel);
tEmpty('bài nhiều ô: nhãn không trùng nhau', bad.dupLabel);
tEmpty('không ô nào chỉ hiện dấu "?"', bad.bareQ);
tEmpty('mọi câu đều có dòng nói rõ phải làm gì', bad.noBrief);
console.log(`   soi ${qs} câu · ${boxes} ô nhập · nhãn + đơn vị + dạng cần điền đủ cả`);

/* ── chữ bị cắt cụt: chỉ cho phép "…" sau DÃY SỐ (nghĩa "và cứ thế") ── */
const SEQ_TAIL = /[\d)\]\s,;→+\-−×÷=/.]{2,}…$/;
const cut = [];
const walkStr = (o, p, hit) => {
  if (typeof o === 'string') hit(p, o);
  else if (Array.isArray(o)) o.forEach((v, i) => walkStr(v, `${p}[${i}]`, hit));
  else if (o && typeof o === 'object') for (const k of Object.keys(o)) walkStr(o[k], `${p}.${k}`, hit);
};
// chỉ soi những chỗ con ĐỌC hoặc NHÌN: đề bài, gợi ý, thẻ công thức, lời thoại
for (const L of lessons) {
  for (const [where, it] of everyItem(L)) walkStr(it, `${L.id} ${where}`, (p, s) => {
    if (s.trimEnd().endsWith('…') && !SEQ_TAIL.test(s.trimEnd())) cut.push(p);
  });
  // Lời thoại BỎ LỬNG là có chủ ý ("Công bằng mà…") — nhận ra bằng cách đối chiếu
  // với lời dẫn của chính bài: nếu lời dẫn cũng viết y hệt thì đó là văn, không phải
  // chữ bị cắt. Ngày nào ai đó cắt cụt một lời thoại, nó lệch lời dẫn và bị bắt ngay.
  const narration = (L.lecture?.screens || []).map((s) => s.narration || '').join(' ⟡ ');
  (L.figureSpec || []).forEach((f, i) => {
    for (const k of ['formulas', 'lines', 'right', 'wrong'])
      walkStr(f.params?.[k], `${L.id} fig[${i}].${k}`, (p, s) => {
        const v = s.trimEnd();
        if (!v.endsWith('…') || SEQ_TAIL.test(v)) return;
        if (k === 'lines' && narration.includes(v)) return;
        cut.push(p);
      });
  });
}
tEmpty('không đề bài / gợi ý / thẻ công thức nào bị cắt cụt', cut);

/* ── bong bóng thoại rỗng: con nhìn thấy khung trắng trơn ── */
const emptySay = [];
for (const L of lessons)
  (L.figureSpec || []).forEach((f, i) =>
    (f.params?.lines || []).forEach((ln, k) => {
      if (!String(ln.say || '').trim()) emptySay.push(`${L.id} fig[${i}].lines[${k}] (${ln.who})`);
    }));
console.log(`   bong bóng thoại rỗng trong dữ liệu: ${emptySay.length} (hình bỏ qua, không vẽ khung trắng)`);

/* ══ Mục tiêu bài học con ĐỌC ĐƯỢC ══
   Bản gốc viết cho người lớn: trung vị 61 chữ, có bài 9 cặp ngoặc lồng nhau — con
   lớp 5 mở màn đầu tiên ra là lướt qua. Hàng rào này canh bản dành cho con. */
const objBad = { thieu: [], dai: [], ngoac: [], matGoc: [], trungGoc: [] };
let objW = [];
for (const L of lessons) {
  const o = L.objective || {};
  const kid = (o.kidText || '').trim();
  if (!kid) { objBad.thieu.push(L.id); continue; }
  if (!o.text) objBad.matGoc.push(L.id);            // bản cho bố mẹ phải còn nguyên
  if (kid === o.text) objBad.trungGoc.push(L.id);   // chép lại y hệt là chưa viết lại
  const w = kid.split(/\s+/).length;
  objW.push(w);
  if (w > 35) objBad.dai.push(`${L.id} (${w} chữ)`);
  if ((kid.match(/\(/g) || []).length > 1) objBad.ngoac.push(L.id);
}
objW.sort((a, b) => a - b);
tEmpty('bài nào cũng có mục tiêu viết cho con', objBad.thieu);
tEmpty('vẫn giữ nguyên mục tiêu gốc cho bố mẹ', objBad.matGoc);
tEmpty('mục tiêu cho con không phải bản chép lại', objBad.trungGoc);
tEmpty('mục tiêu cho con không quá 35 chữ', objBad.dai);
tEmpty('mục tiêu cho con không lồng nhiều ngoặc', objBad.ngoac);
console.log(`   mục tiêu cho con: ngắn nhất ${objW[0]} chữ · trung vị ${objW[Math.floor(objW.length / 2)]} · dài nhất ${objW[objW.length - 1]}`);

/* ── lõi đáp án: tách được phần lý do để con chỉ phải gõ cái chính ── */
t('tách lý do trong ngoặc',   answerCore('bằng nhau (0 đuôi bỏ được)') === 'bằng nhau');
t('tách lý do sau gạch ngang', answerCore('có — 11 × 8') === 'có');
t('không cắt nhầm dấu trừ',    answerCore('12 − 5') === '12 − 5');
t('dãy số dài vẫn máy chấm được', isNumberList('29, 38, 47, 56, 65, 74, 83, 92'));
t('câu chữ dài vẫn là tự đối chiếu', isSelfCheck('12 tháng — 13 bạn: 13 chim chui 12 chuồng, ít nhất một tháng có từ 2 bạn'));

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
