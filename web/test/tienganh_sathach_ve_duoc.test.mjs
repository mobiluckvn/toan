/**
 * CỔNG · MỌI CÂU SÁT HẠCH PHẢI CÓ ĐƯỜNG VẼ TRẢ LỜI ĐÚNG ĐƯỢC.
 *
 * ── LỖI ĐÃ CHẠY THẬT, 22-08-2026 ──
 * `SatHach` dựng `CauNgheNhin` cho MỌI câu. Bản cũ của component ấy chỉ biết dạng
 * đúng/sai — nó chấm bằng `answerKey.value`. Nhưng 62 câu sát hạch là dạng
 * nghe-chọn, khoá `answerKey.choice`. `value` là `undefined`, nên `v === undefined`
 * SAI với cả hai nút: bé bấm gì cũng bị chấm sai.
 *
 * 9 bài mà CẢ kỳ sát hạch không có lấy một câu trả lời đúng được. Bé làm hai lượt,
 * 0/5 cả hai lần, rồi màn hình bảo "Cần 4 câu đúng".
 *
 * ── VÌ SAO 75 CỔNG CŨ KHÔNG BẮT ĐƯỢC ──
 * Vì tất cả đều soi DỮ LIỆU, mà dữ liệu thì đúng: câu có `format`, có `choices`,
 * có `answerKey.choice` hợp lệ. Chỗ hỏng nằm ở CHỖ NỐI giữa dữ liệu và component
 * vẽ nó — không tệp nào sở hữu chỗ ấy, nên không cổng nào nghĩ tới.
 *
 * `OnTap.jsx` dùng cùng dữ liệu ấy mà KHÔNG hỏng, vì nó rẽ nhánh theo `nhinNghe`.
 * Hai màn, một đúng một sai, cùng một kho dữ liệu.
 *
 * ── NÊN CỔNG NÀY SOI GÌ ──
 * Nối hai đầu lại: với mỗi HÌNH DẠNG câu có thật trong kho, component có nhánh vẽ
 * được nó và chấm bằng ĐÚNG cái khoá mà dữ liệu mang không.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const json = (p) => JSON.parse(doc(p));
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];

function moiCauSatHach() {
  const ra = [];
  for (const q of QUYEN) {
    for (const f of readdirSync(new URL(`../public/content/${q}/`, import.meta.url))) {
      if (!/^DL_TA\d_B\d+\.json$/.test(f)) continue;
      const b = json(`../public/content/${q}/${f}`);
      for (const i of (b.assessment?.items || [])) ra.push({ bai: b.id, cau: i });
    }
  }
  return ra;
}

test('mỗi câu sát hạch chỉ mang ĐÚNG MỘT khoá đáp án đã biết', () => {
  const biet = new Set(['value', 'choice']);
  for (const { bai, cau } of moiCauSatHach()) {
    const ks = Object.keys(cau.answerKey || {});
    assert.equal(ks.length, 1, `${bai} ${cau.id}: có ${ks.length} khoá đáp án (${ks})`);
    assert.ok(biet.has(ks[0]),
      `${bai} ${cau.id}: khoá '${ks[0]}' chưa có nhánh vẽ nào trong CauNgheNhin`);
  }
});

test('câu nghe-chọn phải có đủ `choices` để bày ra', () => {
  let n = 0;
  for (const { bai, cau } of moiCauSatHach()) {
    if (!(cau.answerKey || {}).choice) continue;
    n += 1;
    assert.ok(Array.isArray(cau.choices) && cau.choices.length >= 2,
      `${bai} ${cau.id}: khoá là 'choice' mà không có danh sách để chọn`);
    assert.ok(cau.choices.includes(cau.answerKey.choice),
      `${bai} ${cau.id}: đáp án đúng KHÔNG nằm trong các ô để chọn — `
      + 'bé bấm gì cũng sai, đúng lỗi đã chạy thật ngày 22-08');
  }
  assert.ok(n > 0, 'không lọc ra câu nghe-chọn nào — phép canh tự chứng minh với chính nó');
});

test('câu đúng/sai phải có `value` là kiểu boolean', () => {
  let n = 0;
  for (const { bai, cau } of moiCauSatHach()) {
    if (!('value' in (cau.answerKey || {}))) continue;
    n += 1;
    assert.equal(typeof cau.answerKey.value, 'boolean',
      `${bai} ${cau.id}: 'value' không phải boolean — phép so \`v === value\` sẽ luôn sai`);
  }
  assert.ok(n > 0, 'không lọc ra câu đúng/sai nào');
});

test('CauNgheNhin có nhánh cho CẢ HAI khoá, và chấm bằng đúng khoá ấy', () => {
  /* Soi MÃ, không soi chú thích — bẫy đã sập hai lần trong kho này. */
  const ma = chiMa(doc('../src/mon/tienganh/components/CauNgheNhin.jsx'));
  assert.match(ma, /answerKey/, 'component không đọc answerKey');

  /* ⚠ SOI CHÍNH ĐIỀU KIỆN RẼ NHÁNH, không soi việc chữ `choices` có xuất hiện.
     Bản đầu tôi viết `assert.match(ma, /choices/)` — đảo chiều thử bằng cách đổi
     điều kiện thành `if (false)` thì cổng VẪN XANH, vì chữ `choices` còn nguyên
     trong nhánh đã chết. Một cổng soi sự-có-mặt-của-chữ thì gần như không canh
     được gì: nhánh còn đó mà không bao giờ chạy tới là đúng thứ cần bắt. */
  assert.match(ma, /if\s*\(\s*cau\.choices[^)]*\)\s*\{/,
    'CauNgheNhin không rẽ nhánh THEO `cau.choices` — 62 câu sẽ lại không trả lời '
    + 'đúng được. (Nhánh có mặt nhưng điều kiện bị vô hiệu hoá cũng tính là hỏng.)');
  assert.match(ma, /===\s*k\.choice|===\s*cau\.answerKey\.choice/,
    'nhánh nghe-chọn không chấm bằng khoá `choice`');
  assert.match(ma, /===\s*k\.value|===\s*cau\.answerKey\.value/,
    'nhánh đúng/sai không chấm bằng khoá `value`');
});

test('SatHach và OnTap phải cùng dựng được mọi dạng câu', () => {
  /* Bản cũ: OnTap rẽ nhánh theo `nhinNghe`, SatHach thì không — và chính chỗ lệch
     ấy sinh ra lỗi. Nay cả hai đều gọi CauNgheNhin, mà CauNgheNhin tự rẽ nhánh
     bên trong. Cổng này canh để không ai gỡ nhánh ấy ra rồi bắt màn gọi tự lo. */
  const bai = chiMa(doc('../src/mon/tienganh/components/BaiHoc.jsx'));
  assert.match(bai, /<CauNgheNhin[\s\S]{0,200}?cau=\{q\}/,
    'SatHach không còn dựng CauNgheNhin');
  const on = chiMa(doc('../src/mon/tienganh/components/OnTap.jsx'));
  assert.match(on, /CauNgheNhin/, 'OnTap không còn dựng CauNgheNhin');
});
