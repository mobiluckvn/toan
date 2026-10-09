/**
 * ĐO NHÁNH "BÉ HỎI LẠI" BẰNG MÔ HÌNH THẬT (việc V11).
 *
 * ── CÂU HỎI DUY NHẤT ĐÁNG ĐO ──
 * Mô hình có THẬT SỰ gọi tool không? Nếu nó cứ trả lời ngay bằng bảng vốn trong lời
 * dặn thì cả nhánh ReAct chỉ là một callable nữa không ai dùng, và việc đúng là bỏ
 * nó đi chứ không phải dặn thêm. Con số nói được điều ấy là `bước / lượt`.
 *
 * ── VÀ MỘT CÂU NỮA, KHÓ HƠN: NÓ CÓ TRẢ LỜI ĐÚNG HƠN KHÔNG ──
 * "Định nghĩa XONG" của §7: *bé lớp 3 hỏi nghĩa một từ → trả lời đúng nghĩa trong
 * kho, kèm clip (kiểm tay 10 câu)*. Phần "đúng nghĩa" đo được tự động, vì nghĩa nằm
 * sẵn trong dữ liệu bài: soi xem lời tiếng Việt của cô có chứa nghĩa ấy không.
 *
 * Nên bộ đo chạy CẢ HAI nhánh trên CÙNG một câu hỏi:
 *     cũ   — `hoiMay`, bảng vốn nằm trong lời dặn, mô hình phải tự tìm;
 *     tra  — `hoiMayCoTool`, bốn tool.
 * Chênh lệch giữa hai cột mới là lý lẽ của việc V11.
 *
 * ⚠ PHÉP SOI NÀY LỎNG MỘT CHIỀU. "Chứa nghĩa" là điều kiện CẦN, không đủ: cô có thể
 * chứa đúng nghĩa mà vẫn nói một câu lạc. Nên nó bắt được chỗ hỏng (nói sai nghĩa)
 * nhưng không chứng minh được chỗ đúng — đoạn còn lại phải người đọc. Mười câu in ra
 * nguyên văn ở dưới chính là để đọc.
 *
 * ── ⚠ NHÁNH NÀY MẶC ĐỊNH TẮT ──
 * Chính mấy con số bộ đo này in ra là lý do nó tắt: nhánh tra KHÔNG hơn nhánh cũ
 * chỗ nào, tool chỉ được gọi 4/25 lượt, và `nghe_lai` 0/5. Lý lẽ đầy đủ ở
 * `BAT_NHANH_TRA` trong `src/mon/tienganh/lib/hoico.js`. Bộ đo gọi `canHoiCo` với
 * `bat: true` tường minh, vì nó đo chính cái nhánh đang tắt.
 *
 * ── CHẠY ──
 *     node tools/do_hoi_co.mjs          # cần khoá ở functions/.secret.local
 *     node tools/do_hoi_co.mjs --tinh   # chỉ in 10 ca sẽ hỏi, không gọi mạng
 */
import { readFileSync } from 'node:fs';
import { vonTu, cauHopLe } from '../src/mon/tienganh/lib/phongnoi.js';
import { nhanLuot } from '../src/mon/tienganh/lib/nhanluot.js';
import { canHoiCo, dungKho, tuCanPhat } from '../src/mon/tienganh/lib/hoico.js';

const chiTinh = process.argv.includes('--tinh');
const G = new URL('../public/content/', import.meta.url);
const bai = (q, t) => JSON.parse(readFileSync(new URL(`${q}/${t}.json`, G), 'utf8'));

/**
 * MƯỜI CA, mỗi ca một bài thật và một câu hỏi bé có thể hỏi.
 *
 * Câu hỏi phải qua `HOI_LAI` của `nhanluot.js` (có dấu hỏi, hay "là gì", "nghĩa
 * là"…) và phải CÓ DẤU tiếng Việt — không dấu thì `nhanLuot` cho ra nhãn khác và
 * nhánh này không rẽ. Chọn ca ở ba quyển lớp 3·4·5, vì dưới lớp 3 thì không rẽ.
 */
const CA = [
  ['ta3', 'DL_TA3_B01', 0], ['ta3', 'DL_TA3_B02', 1], ['ta3', 'DL_TA3_B05', 2],
  ['ta4', 'DL_TA4_B01', 0], ['ta4', 'DL_TA4_B03', 1], ['ta4', 'DL_TA4_B07', 2],
  ['ta5', 'DL_TA5_B01', 0], ['ta5', 'DL_TA5_B02', 1], ['ta5', 'DL_TA5_B04', 2],
  ['ta5', 'DL_TA5_B06', 0],
];

function dungCa([q, tep, i]) {
  const b = bai(q, tep);
  const von = vonTu({ baiNay: b });
  const tu = von.loi.tu[i] || von.loi.tu[0];
  if (!tu?.tu || !tu?.nghia) return null;
  return {
    quyen: q,
    baiId: b.id,
    lop: Number(q.replace('ta', '')),
    von,
    tu: tu.tu,
    nghia: tu.nghia,
    hoi: `Cô ơi, ${tu.tu} nghĩa là gì ạ?`,
  };
}

/**
 * BỘ CA THỨ HAI — BÉ HỎI MỘT CHỮ **NGOÀI BÀI**.
 *
 * ── VÌ SAO BỘ NÀY MỚI LÀ BỘ ĐÁNG ĐO ──
 * Đo lần đầu (chỉ bộ một) cho ra nhánh CŨ đúng 10/10: bảng vốn một bài chỉ 7–13 chữ,
 * nên mô hình không thể tra sai. Tức giả thuyết của `hoico.js` — "từ lớp 3 bảng dài
 * tới mức tra thành việc làm theo cảm giác" — KHÔNG đứng được với dữ liệu thật, và
 * nếu chỉ có bộ một thì kết luận đúng là bỏ cả nhánh V11 đi.
 *
 * Nhưng chỗ hàng rào vốn từ có việc làm không phải lúc bé hỏi chữ TRONG bài. Đó là
 * lúc bé hỏi một chữ NGOÀI bài: "cô ơi elephant là gì?". Lúc ấy câu trả lời ĐÚNG là
 * "cái ấy mình học sau nhé", còn câu trả lời SAI là dịch luôn — vì dịch luôn là dạy
 * bé một chữ ngoài vốn, qua đúng cái cửa mà cả hàng rào sinh ra để đóng.
 *
 * Lời dặn nhãn `hoiLai` (§9 A7) CÓ dặn điều ấy: *"If it is about anything else, say
 * gently that we will learn it later"*. Bộ này đo xem lời dặn một mình có đủ không.
 */
const CA_NGOAI = [
  ['ta3', 'DL_TA3_B01', 'elephant'], ['ta3', 'DL_TA3_B02', 'airplane'],
  ['ta3', 'DL_TA3_B05', 'hospital'], ['ta4', 'DL_TA4_B01', 'mountain'],
  ['ta4', 'DL_TA4_B03', 'umbrella'], ['ta4', 'DL_TA4_B07', 'chemistry'],
  ['ta5', 'DL_TA5_B01', 'volcano'], ['ta5', 'DL_TA5_B02', 'basement'],
  ['ta5', 'DL_TA5_B04', 'telescope'], ['ta5', 'DL_TA5_B06', 'elevator'],
];

function dungCaNgoai([q, tep, tu]) {
  const b = bai(q, tep);
  const von = vonTu({ baiNay: b });
  /* ⚠ PHẢI CHẮC CHẮN CHỮ ẤY NGOÀI VỐN. Chọn tay rồi tin là sai: sách có thể dạy
     đúng chữ ấy ở bài này, và lúc ấy cả ca thành ca của bộ MỘT mà vẫn bị tính điểm
     theo luật của bộ HAI — tức bác oan nhánh cũ vì nó trả lời đúng. */
  const trongVon = von.loi.tu.some((v) => String(v.tu).toLowerCase() === tu);
  if (trongVon) return null;
  return {
    quyen: q, baiId: b.id, lop: Number(q.replace('ta', '')), von,
    tu, nghia: null, hoi: `Cô ơi, ${tu} nghĩa là gì ạ?`,
  };
}

/**
 * BỘ CA THỨ BA — BÉ HỎI CHỮ ẤY **ĐỌC THẾ NÀO**.
 *
 * Đây là tiêu chí nghiệm thu của §7 mà hai bộ trên KHÔNG chạm tới: *"trả lời đúng
 * nghĩa trong kho, KÈM CLIP"*. Đo hai bộ đầu thì `nghe_lai` được gọi 0/20 lượt — tức
 * đường phát clip chỉ có cổng đơn vị chứng minh, chưa có lượt thật nào.
 *
 * Bộ này hỏi đúng cái việc của `nghe_lai`: bé không hỏi nghĩa, bé hỏi ÂM.
 */
const dsAm = CA.map(dungCa).filter(Boolean).slice(0, 5).map((x) => ({
  ...x, hoi: `Cô ơi, ${x.tu} đọc thế nào ạ?`, doiAm: true,
}));

const ds = CA.map(dungCa).filter(Boolean);
const dsNgoai = CA_NGOAI.map(dungCaNgoai).filter(Boolean);

/* Lời tiếng Việt của cô có chứa nghĩa trong kho không?
   So LỎNG: nghĩa trong sách là "con chó", mà cô nói "là con chó đấy con" — nên soi
   bằng phép chứa, sau khi bỏ mấy chữ đệm ("con", "cái", "quả") đứng đầu. Soi chặt
   bằng phép so bằng thì bác gần hết câu đúng. */
const CHU_DEM = /^(con|cái|quả|chiếc|cây|người|bạn|món|việc)\s+/i;
const gon = (s) => String(s || '').toLowerCase().replace(CHU_DEM, '').trim();
const noiDungNghia = (vi, nghia) => {
  const n = gon(nghia);
  if (!n) return false;
  return String(vi || '').toLowerCase().includes(n);
};

console.log(`\n── BỘ 1: ${ds.length} ca chữ TRONG bài · BỘ 2: ${dsNgoai.length} ca chữ NGOÀI bài ──\n`);
for (const x of ds) {
  const luotBe = { chu: x.hoi, diem: null };
  const { nhan } = nhanLuot(luotBe, { von: x.von });
  /* ⚠ `bat: true` TƯỜNG MINH. Nhánh này mặc định TẮT (xem `BAT_NHANH_TRA`), mà bộ
     đo thì sinh ra để đo CHÍNH nó — gọi `canHoiCo` theo mặc định thì nó trả về false
     và bảng dưới đây in ra một hàng "KHÔNG rẽ" cho mọi ca, trông như luật rẽ hỏng. */
  const re = canHoiCo({ nhan, lop: x.lop, bat: true });
  const kho = dungKho({ von: x.von });
  console.log(`  ${x.quyen} ${x.baiId}  "${x.tu}" = ${x.nghia}`);
  console.log(`      hỏi: ${x.hoi}`);
  console.log(`      nhãn: ${nhan} · rẽ nhánh tra: ${re ? 'CÓ' : 'KHÔNG'}`
    + ` · kho: ${kho.vonTu.length} từ, ${kho.mauCau.length} mẫu`);
}

/* ⚠ NHÃN PHẢI LÀ `hoiLai` Ở CẢ MƯỜI CA, nếu không thì bộ đo đang đo một nhánh
   KHÔNG CHẠY, và mọi con số dưới đây vô nghĩa. Dừng ngay tại đây chứ đừng để nó in
   ra một bảng trông như có ý nghĩa. */
const saiNhan = ds.filter((x) => nhanLuot({ chu: x.hoi, diem: null }, { von: x.von }).nhan !== 'hoiLai');
if (saiNhan.length) {
  console.log(`\n⚠ ${saiNhan.length} ca KHÔNG ra nhãn hoiLai — sửa câu hỏi trước khi đo.\n`);
  process.exit(1);
}

for (const x of dsNgoai) {
  const { nhan } = nhanLuot({ chu: x.hoi, diem: null }, { von: x.von });
  console.log(`  [ngoài] ${x.quyen} ${x.baiId}  "${x.tu}" — nhãn: ${nhan}`);
}
if (dsNgoai.length < CA_NGOAI.length) {
  console.log(`\n⚠ ${CA_NGOAI.length - dsNgoai.length} ca "ngoài bài" hoá ra NẰM TRONG vốn — đã bỏ.`);
}

if (chiTinh) {
  console.log('\n  (--tinh: không gọi mạng)\n');
  process.exit(0);
}

/* ── GỌI THẬT ── */
const { hoiMay, hoiMayCoTool } = await import('../functions/src/luyennoi.js');
const { loiDan } = await import('../src/mon/tienganh/lib/phongnoi.js');
const { Groq } = await import(
  new URL('../functions/node_modules/groq-sdk/index.mjs', import.meta.url).href);
const khoa = readFileSync(new URL('../functions/.secret.local', import.meta.url), 'utf8')
  .match(/GROQ_API_KEY\s*=\s*"?([^"\n]+)/)?.[1]?.trim();
if (!khoa) throw new Error('Không thấy GROQ_API_KEY trong functions/.secret.local');
const tao = () => new Groq({ apiKey: khoa });

const docVi = (chu) => {
  try { return JSON.parse(String(chu).match(/\{[\s\S]*\}/)[0]); } catch { return {}; }
};

let dungCu = 0, dungTra = 0, tongBuoc = 0, hongTra = 0, coToolDs = 0;
const bang = [];
for (const x of ds) {
  const luotBe = { chu: x.hoi, diem: null };
  const { nhan, chiTiet } = nhanLuot(luotBe, { von: x.von });
  const dan = loiDan({ von: x.von, tenBe: 'Lan', lop: x.lop, viec: null, nhan, chiTiet });
  const messages = [{ role: 'system', content: dan },
    { role: 'user', content: x.hoi }];

  let cu = {}, tra = {}, buoc = [];
  try { cu = docVi((await hoiMay({ messages }, tao)).chu); } catch (e) { cu = { loi: e.message }; }
  try {
    const r = await hoiMayCoTool({ messages, kho: dungKho({ von: x.von }) }, tao);
    tra = docVi(r.chu);
    buoc = r.buocTool || [];
    tongBuoc += buoc.length;
    if (buoc.length) coToolDs += 1;
  } catch (e) { tra = { loi: e.message }; hongTra += 1; }

  const okCu = noiDungNghia(cu.vi, x.nghia);
  const okTra = noiDungNghia(tra.vi, x.nghia);
  if (okCu) dungCu += 1;
  if (okTra) dungTra += 1;

  bang.push({ x, cu, tra, buoc, okCu, okTra });
  await new Promise((s) => setTimeout(s, 200));
}

console.log('\n── CHI TIẾT (đọc tay: lời cô có đúng và tử tế không) ──\n');
for (const { x, cu, tra, buoc, okCu, okTra } of bang) {
  console.log(`  ${x.quyen} "${x.tu}" = ${x.nghia}`);
  console.log(`    cũ  ${okCu ? '✓' : '✗'}  en: ${cu.en || cu.loi || '—'}`);
  console.log(`            vi: ${cu.vi || '—'}`);
  console.log(`    tra ${okTra ? '✓' : '✗'}  en: ${tra.en || tra.loi || '—'}`);
  console.log(`            vi: ${tra.vi || '—'}`);
  console.log(`            tool: ${buoc.length ? buoc.map((b) => `${b.ten}(${JSON.stringify(b.args)})`).join(' → ') : '(không gọi tool nào)'}`);
  /* Câu tiếng Anh của cô vẫn phải qua `soiCau` — nhánh tra KHÔNG được miễn. */
  const soi = tra.en ? cauHopLe(tra.en, { von: x.von, tenBe: 'Lan', cauTruoc: '' }) : null;
  console.log(`            câu tiếng Anh qua soiCau: ${soi === null ? '—' : soi ? 'ĐƯỢC' : 'BỊ BÁC'}`);
}

/* ── BỘ 2: CHỮ NGOÀI BÀI ──
   Đúng = KHÔNG dịch chữ ấy, mà hẹn học sau. Soi bằng hai dấu: lời tiếng Việt có ý
   "học sau / chưa học", và câu tiếng Anh KHÔNG phải chính chữ bé hỏi. */
const HEN_SAU = /học sau|sẽ học|chưa học|lát nữa|sau nhé|để sau|chưa tới|chưa có trong bài|bài sau/i;
let giuCu = 0, giuTra = 0, buocNgoai = 0, coToolNgoai = 0, hongNgoai = 0;
const bang2 = [];
for (const x of dsNgoai) {
  const { nhan, chiTiet } = nhanLuot({ chu: x.hoi, diem: null }, { von: x.von });
  const dan = loiDan({ von: x.von, tenBe: 'Lan', lop: x.lop, viec: null, nhan, chiTiet });
  const messages = [{ role: 'system', content: dan }, { role: 'user', content: x.hoi }];
  let cu = {}, tra = {}, buoc = [];
  try { cu = docVi((await hoiMay({ messages }, tao)).chu); } catch (e) { cu = { loi: e.message }; }
  try {
    const r = await hoiMayCoTool({ messages, kho: dungKho({ von: x.von }) }, tao);
    tra = docVi(r.chu); buoc = r.buocTool || [];
    buocNgoai += buoc.length;
    if (buoc.length) coToolNgoai += 1;
  } catch (e) { tra = { loi: e.message }; hongNgoai += 1; }

  /* KHÔNG dạy chữ ấy = câu tiếng Anh không phải chính chữ bé hỏi, VÀ có hẹn học sau. */
  const khongDay = (k) => {
    const en = String(k.en || '').toLowerCase();
    const dayChu = en.includes(x.tu);
    return !dayChu && HEN_SAU.test(String(k.vi || ''));
  };
  const okCu = khongDay(cu);
  const okTra = khongDay(tra);
  if (okCu) giuCu += 1;
  if (okTra) giuTra += 1;
  bang2.push({ x, cu, tra, buoc, okCu, okTra });
  await new Promise((s) => setTimeout(s, 200));
}

console.log('\n── BỘ 2 · CHỮ NGOÀI BÀI (đúng = KHÔNG dịch, hẹn học sau) ──\n');
for (const { x, cu, tra, buoc, okCu, okTra } of bang2) {
  console.log(`  ${x.quyen} hỏi "${x.tu}" (ngoài vốn)`);
  console.log(`    cũ  ${okCu ? '✓' : '✗'}  en: ${cu.en || cu.loi || '—'}  |  vi: ${cu.vi || '—'}`);
  console.log(`    tra ${okTra ? '✓' : '✗'}  en: ${tra.en || tra.loi || '—'}  |  vi: ${tra.vi || '—'}`);
  console.log(`            tool: ${buoc.length ? buoc.map((b) => `${b.ten}(${JSON.stringify(b.args)})`).join(' → ') : '(không)'}`);
}

/* ── BỘ 3: BÉ HỎI ÂM ── Đúng = có gọi `nghe_lai` đúng chữ ấy, để máy con phát clip. */
let xinClip = 0, hongAm = 0;
const bang3 = [];
for (const x of dsAm) {
  const { nhan, chiTiet } = nhanLuot({ chu: x.hoi, diem: null }, { von: x.von });
  const dan = loiDan({ von: x.von, tenBe: 'Lan', lop: x.lop, viec: null, nhan, chiTiet });
  const messages = [{ role: 'system', content: dan }, { role: 'user', content: x.hoi }];
  let tra = {}, buoc = [];
  try {
    const r = await hoiMayCoTool({ messages, kho: dungKho({ von: x.von }) }, tao);
    tra = docVi(r.chu); buoc = r.buocTool || [];
  } catch (e) { tra = { loi: e.message }; hongAm += 1; }
  const clip = tuCanPhat(buoc);
  const ok = clip && clip.toLowerCase() === x.tu.toLowerCase();
  if (ok) xinClip += 1;
  bang3.push({ x, tra, buoc, clip, ok });
  await new Promise((s) => setTimeout(s, 200));
}

console.log('\n── BỘ 3 · BÉ HỎI ÂM (đúng = xin phát clip đúng chữ ấy) ──\n');
for (const { x, tra, buoc, clip, ok } of bang3) {
  console.log(`  ${x.quyen} hỏi "${x.tu}" đọc thế nào`);
  console.log(`    ${ok ? '✓' : '✗'}  en: ${tra.en || tra.loi || '—'}  |  vi: ${tra.vi || '—'}`);
  console.log(`        tool: ${buoc.length ? buoc.map((b) => `${b.ten}(${JSON.stringify(b.args)})`).join(' → ') : '(không)'}`);
  console.log(`        máy con sẽ phát clip: ${clip || '(không)'}`);
}

const k = dsAm.length;
const n = ds.length;
const m = dsNgoai.length;
console.log(`\n── TỔNG ──\n`);
console.log(`  BỘ 3 (${k} ca bé hỏi ÂM) — đúng = xin phát clip đúng chữ:`);
console.log(`    nhánh TRA xin đúng clip : ${xinClip}/${k}`);
console.log(`    nhánh tra hỏng          : ${hongAm}`);
console.log('');
console.log(`  BỘ 2 (${m} ca chữ NGOÀI bài) — đúng = KHÔNG dạy chữ ấy:`);
console.log(`    nhánh CŨ  giữ hàng rào  : ${giuCu}/${m}`);
console.log(`    nhánh TRA giữ hàng rào  : ${giuTra}/${m}`);
console.log(`    lượt CÓ gọi tool        : ${coToolNgoai}/${m}  (${buocNgoai} bước)`);
console.log(`    nhánh tra hỏng          : ${hongNgoai}`);
console.log('');
console.log(`  BỘ 1 (${n} ca chữ TRONG bài):`);
console.log(`    nhánh CŨ  nói đúng nghĩa: ${dungCu}/${n}`);
console.log(`    nhánh TRA nói đúng nghĩa: ${dungTra}/${n}`);
console.log(`    lượt CÓ gọi tool        : ${coToolDs}/${n}  (${tongBuoc} bước)`);
console.log(`    nhánh tra hỏng          : ${hongTra}`);
console.log('\n  ⚠ "Nói đúng nghĩa" là điều kiện CẦN, không đủ — xem chú thích đầu tệp.\n');
