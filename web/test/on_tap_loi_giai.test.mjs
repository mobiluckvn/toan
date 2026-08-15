/* ═══════════ LỜI GIẢI KỲ SÁT HẠCH PHẢI ĐÚNG CÂU ═══════════
 *
 * Bé làm xong một câu ôn tập thì màn hình chìa ra lời giải để bé tự soi. Suốt một
 * thời gian dài, ở bốn chương lời giải hiện ra là CỦA MỘT CÂU KHÁC:
 *
 *   ôn tập 7 · C1 hỏi "Tỉ số hai số là 2 : 5, cả hai gộp lại gồm mấy phần?"
 *             lời giải hiện ra "một phần 20 : 4 = 5 → 5 viên và 15 viên"
 *
 * ── VÌ SAO KHÔNG AI BIẾT ──
 * Mấy đợt làm video có viết lại đề của một số kỳ ôn tập cho khớp bài mới tách. Đề
 * đổi và ô nhập đổi theo, nhưng lời giải thì không — mà nó đánh khoá theo SỐ THỨ TỰ
 * CÂU (`OT7#C1`), nên khoá vẫn khớp còn nội dung đã là của câu cũ. Máy vẫn chấm
 * đúng, cổng vẫn xanh, chỉ đoạn chữ bé đọc là của bài khác.
 *
 * Đo lúc tìm ra: 39 câu đề chính ở chương 3, 5, 6, 7 và 34 câu đề B ở bốn chương.
 *
 * ── PHÉP DƯỚI ĐÂY ──
 * Máy không đọc hiểu được "lời giải này có phải của câu này không". Nhưng ô nhập
 * và lời giải cùng nói về MỘT đáp số, nên mọi giá trị SỐ của ô nhập phải xuất hiện
 * nguyên văn trong lời giải. Lệch câu là con số lệch theo ngay.
 *
 * NGƯỠNG ĐẶT Ở ĐÚNG CHỖ DỮ LIỆU ĐANG ĐỨNG: sau khi vá, cả 240 câu của mười một
 * chương đều khớp. Nên đòi 0 lệch, và từ nay chỉ được siết chứ không được nới.
 *
 * ⚠ Phép này KHÔNG soi được câu mà đáp án là chữ ("có/không", "góc tù"), vì chữ ấy
 * hay nằm sẵn trong đề. Nó chỉ canh phần đáp số bằng con số — mà đó cũng đúng là
 * phần đã hỏng.
 */
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';

const GOC = path.resolve(import.meta.dirname, '..', '..');
const doc = (p) => JSON.parse(fs.readFileSync(path.join(GOC, p), 'utf8'));

const ky = fs
  .readdirSync(path.join(GOC, 'web/public/content/reviews'))
  .filter((f) => /^DCR_KSN4_C\d+\.json$/.test(f))
  .map((f) => doc(`web/public/content/reviews/${f}`))
  .sort((a, b) => a.chapter - b.chapter);

/* Mọi giá trị của khoá đáp án, phẳng ra một mảng. */
const giaTri = (k) => {
  if (!k) return [];
  if (k.parts) return k.parts.map((p) => p.value);
  if (k.values) return k.values;
  return [k.value];
};

const soLe = (van, v) =>
  new RegExp(`(?<![0-9])${v}(?![0-9])`).test(String(van).replace(/\s/g, ''));

for (const k of ky) {
  for (const [nhan, ds] of [['đề chính', k.examA], ['đề B', k.deB]]) {
    test(`ch${k.chapter} · ${nhan}: lời giải nhắc đủ đáp số của ô nhập`, () => {
      const lech = [];
      for (const q of ds) {
        const so = giaTri(q.answerKey).filter((v) => typeof v === 'number');
        if (!so.length) continue;
        const thieu = so.filter((v) => !soLe(q.answer || '', v));
        if (thieu.length) {
          lech.push(`câu ${q.qno}: ô nhập có ${thieu.join(', ')} mà lời giải không nhắc`
            + ` — "${(q.answer || '').slice(0, 50)}…"`);
        }
      }
      assert.deepEqual(lech, [], 'lời giải không khớp câu hỏi');
    });
  }
}

/* Và lời giải không được để trống — bé bấm xem lời giải mà không có gì hiện ra thì
   im lặng y như lúc nó hiện ra lời giải sai. */
test('lớp 4 · mọi câu ôn tập đều có lời giải', () => {
  const trong = [];
  for (const k of ky) {
    for (const q of [...k.examA, ...k.deB]) {
      if (!(q.answer || '').trim()) trong.push(`ch${k.chapter} câu ${q.qno}`);
    }
  }
  assert.deepEqual(trong, [], 'câu không có lời giải');
});
