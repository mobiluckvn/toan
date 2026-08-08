/**
 * ĐÓNG VAI HỌC SINH LỚP 5 — đi hết 168 bài, không sót bài nào.
 *
 * Nguyên tắc: chỉ dùng những gì HIỆN RA MÀN HÌNH (answerFields / answerBrief) để
 * quyết định gõ gì, bấm gì. Không đọc lén answerKey để "biết đáp án rồi trả lời" —
 * làm thế thì mọi câu đều qua, chẳng phát hiện được gì.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import {
  buildFlow, answerFields, answerBrief, answerMode, checkAnswer, hintState, CACH_TRA_LOI,
} from '../src/lib/flow.js';

const R = new URL('../public/content/', import.meta.url).pathname;
const les = readdirSync(R + 'lessons').filter((f) => f.endsWith('.json'))
  .map((f) => JSON.parse(readFileSync(join(R + 'lessons', f), 'utf8')))
  .sort((a, b) => a.id.localeCompare(b.id, 'vi', { numeric: true }));

const V = {};                                    // loại lỗi → danh sách
const ghi = (loai, s) => (V[loai] ??= []).push(s);
const chuan = (s) => String(s ?? '').toLowerCase().replace(/\s+/g, ' ').trim();

/** Nút mà con SẼ bấm nếu con làm đúng — tìm bằng đáp án, để kiểm cả chuyện
 *  bộ nút có chứa đáp án hay không. */
function nutDung(item, f) {
  if (item.format === 'tf') return item.answerKey?.value ? 'ĐÚNG' : 'SAI';
  if (item.format === 'mcq') {
    return f.options.find((o) => chuan(o) === chuan(item.answerKey?.choice)) ?? null;
  }
  const p = (item.answerKey?.parts || []).find((x) => (x.label || '').trim() === f.label);
  if (p === undefined) return null;
  const v = chuan(p.value);
  return f.options.find((o) => chuan(o) === v || v.startsWith(chuan(o) + ' (') || v.startsWith(chuan(o) + ' —')) ?? null;
}

/** Con gõ gì vào ô nhập tay nếu con làm đúng */
function goDung(item, f, fields) {
  const k = item.answerKey || {};
  if (k.values) return k.values.join(' ; ');
  if (k.accept) return String([].concat(k.accept)[0]);
  const p = (k.parts || []).find((x) => (x.label || '').trim() === f.label);
  const v = p !== undefined ? p.value : (fields.length === 1 ? k.value : undefined);
  return v === undefined ? null : String(v).replace(/\./g, ',');
}

let soBai = 0, soCau = 0, soBuoc = 0;

for (const L of les) {
  soBai++;
  const mid = L.id.replace('DL:KSN5Q1.', '');
  let flow;
  try { flow = buildFlow(L); } catch (e) { ghi('bài không mở được', `${mid}: ${e.message}`); continue; }
  if (!flow?.length) { ghi('bài không có bước nào', mid); continue; }
  soBuoc += flow.length;

  for (const s of flow) {
    const item = s.item;
    if (!item || !item.answerKey) continue;
    soCau++;
    const ref = `${mid} ${item.id || s.type}`;
    const fields = answerFields(item);
    const mode = answerMode(item);

    /* 1. con có chỗ nào để trả lời không */
    if (mode !== 'tuluan' && fields.length === 0) { ghi('không có chỗ trả lời', ref); continue; }

    /* 2. màn hình có nói con phải làm gì không */
    const brief = answerBrief(item);
    if (!brief || !brief.trim()) ghi('không nói con phải làm gì', ref);

    if (mode === 'tuluan') continue;

    /* 3. dựng câu trả lời ĐÚNG bằng đúng thứ con nhìn thấy */
    const traLoi = [];
    let dungDuoc = true;
    for (const f of fields) {
      const v = f.kind === 'pick' ? nutDung(item, f) : goDung(item, f, fields);
      if (v === null || v === undefined) {
        dungDuoc = false;
        ghi(f.kind === 'pick' ? 'bộ nút KHÔNG chứa đáp án đúng' : 'không suy ra được đáp án cho ô',
            `${ref} ô"${f.label}"${f.options ? ' nút: ' + JSON.stringify(f.options) : ''}`);
      }
      traLoi.push(v ?? '');
    }
    if (!dungDuoc) continue;

    /* 4. LÀM ĐÚNG PHẢI ĐƯỢC CÔNG NHẬN — phép kiểm quan trọng nhất.
          Con làm đúng mà máy báo sai thì cổng mustPass chặn, con học không tiếp được. */
    const rD = checkAnswer(item, fields.length <= 1 ? traLoi[0] : traLoi);
    if (!rD.ok && rD.mode !== 'selfcheck') {
      ghi('làm ĐÚNG mà máy chấm SAI', `${ref} [${mode}] gửi ${JSON.stringify(traLoi)} · máy đợi "${rD.expected}"`);
    }

    /* 5. chưa trả lời thì không được tính là đúng */
    const rT = checkAnswer(item, fields.length <= 1 ? '' : fields.map(() => ''));
    if (rT.ok) ghi('chưa trả lời đã được chấm ĐÚNG', `${ref} [${mode}]`);

    /* 6. trả lời bừa phải bị bác */
    const bua = fields.map((f) => (f.kind === 'pick'
      ? (f.options.find((o) => chuan(o) !== chuan(nutDung(item, f))) ?? 'xxx') : 'xxx'));
    const rB = checkAnswer(item, fields.length <= 1 ? bua[0] : bua);
    if (rB.ok) ghi('trả lời BỪA vẫn được chấm ĐÚNG', `${ref} [${mode}] gửi ${JSON.stringify(bua)}`);

    /* 7. ô gõ tay phải nói rõ dạng cần điền; ô bấm phải có từ 2 nút */
    for (const f of fields) {
      if (f.kind === 'pick') {
        if ((f.options || []).length < 2) ghi('ô bấm chọn có dưới 2 nút', `${ref} ô"${f.label}"`);
        if (new Set(f.options.map(chuan)).size !== f.options.length) ghi('bộ nút có nút lặp', `${ref} ô"${f.label}"`);
      } else if (!String(f.placeholder || '').trim()) {
        ghi('ô gõ tay không nói dạng cần điền', `${ref} ô"${f.label}"`);
      }
      if (!String(f.label || '').trim()) ghi('ô không có nhãn', ref);
    }

    /* 8. đề hỏi mấy việc mà chỉ có mấy ô — con điền xong vẫn thấy thiếu */
    const hoi = (item.text || '').match(/\?/g)?.length ?? 0;
    if (hoi >= 2 && fields.length < hoi && mode !== 'chondapan' && mode !== 'dungsai') {
      ghi('đề hỏi nhiều việc hơn số ô', `${ref} ${hoi} dấu hỏi · ${fields.length} ô — ${(item.text || '').slice(0, 90)}`);
    }

    /* 9. sai thì phải có gợi ý để bấu víu (câu luyện tập) */
    if (s.type === 'practice' && !(item.hints || []).length) ghi('sai mà không có gợi ý nào', ref);

    /* 10. đề viết TẮT KIỂU ĐIỆN TÍN — con lớp 5 không đọc ra đang phải làm gì.
       Hai dấu hiệu: dùng "?" làm chỗ trống giữa câu ("còn ? kg", "→ đáy? cao?"),
       và đề toàn ký hiệu, không có lấy một động từ ra lệnh. */
    const de = (item.text || '').trim();
    const DON_VI = /\?\s*(kg|g|cm²|m²|cm|m|viên|đồng|tuổi|trang|phút|giờ)(?![\p{L}])/iu;
    if (DON_VI.test(de) || /→[^?]*\?\s*\S*\?/.test(de)) {
      ghi('đề viết tắt kiểu điện tín', `${ref} — ${de.slice(0, 80)}`);
    }

    /* 11. đề quá dài cho lớp 5 */
    const chu = (item.text || '').split(/\s+/).length;
    if (chu > 60) ghi('đề dài quá cho lớp 5', `${ref} ${chu} chữ`);
  }
}

/* Vài kiểu chỉ để ghi nhận, không đánh trượt: dấu "?" dùng làm chỗ trống trong đề
   ("Thêm ? g đường") là cách viết quen thuộc, không phải câu hỏi thiếu ô. */
const CHI_GHI_NHAN = new Set(['đề hỏi nhiều việc hơn số ô', 'đề dài quá cho lớp 5']);

let pass = 0, fail = 0;
const keys = Object.keys(V).sort((a, b) => V[b].length - V[a].length);
for (const k of keys) {
  console.log(`   ${CHI_GHI_NHAN.has(k) ? '·' : '✗'} ${k}: ${V[k].length}`);
  for (const x of V[k].slice(0, 6)) console.log('      ', x);
  if (V[k].length > 6) console.log(`       …còn ${V[k].length - 6}`);
  if (!CHI_GHI_NHAN.has(k)) fail++;
}
if (!keys.length) pass++;
console.log(`\n   đi hết ${soBai} bài · ${soBuoc} bước · ${soCau} câu hỏi`);
if (soBai !== 168) { fail++; console.log('  ✗ không đi đủ 168 bài'); } else pass++;
if (soCau < 1200) { fail++; console.log('  ✗ số câu soi được ít bất thường'); } else pass++;
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
