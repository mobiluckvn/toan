/**
 * CỔNG · HAI BẢN `chuLa` PHẢI GIỐNG HỆT NHAU.
 *
 * Máy chủ và máy con không import chéo được (cổng `ranh_gioi.test.mjs` chặn, và
 * chặn vì đúng: hai bên hai `package.json`, hai cách dựng). Nên phép soi chữ lạ là
 * bản CHÉP — đúng lối `lib/onlai.js` ↔ `functions/src/schedule.js`.
 *
 * Chép thì phải có cổng so, nếu không nó lệch mà không ai thấy. Và lệch ở đây hỏng
 * theo kiểu khó thấy nhất: máy chủ soi rồi bảo "sạch", máy con soi lại bằng luật
 * khác rồi bỏ mất một mục — bé thấy lời chấm thiếu, mà hai bên đều báo mình đúng.
 *
 * ⚠ So KẾT QUẢ trên nhiều đầu vào, không so chuỗi mã. So mã thì một dấu cách cũng
 * đỏ; so kết quả thì bắt đúng cái đáng bắt.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as may from '../functions/src/chula.js';
import * as con from '../src/mon/tienganh/lib/chamviet.js';

const KHO = {
  vonTu: [{ tu: 'school' }, { tu: 'big' }, { tu: 'friend' }, 'cat',
          { tu: "don't" }, { tu: 'ice cream' }],
  mauCau: ['My school is + [Adjective].', 'I like + [Noun].', 'Thank you.'],
};

/* Ba mươi đầu vào, cố ý gồm mọi chỗ hai bản có thể lệch. */
const CA = [
  '', null, undefined, '   ', 'school', 'School', 'SCHOOL.', 'school!',
  'My school is big.', 'My school is delicious.', 'I like cat.',
  'I like dogs.', "don't", "Don't do that.", 'ice cream', 'icecream',
  'Thank you.', 'thank-you', 'a b c', '123', 'école', 'naïve',
  'My school is big. I like cat.', '  school  ', 'school school school',
  "I don't like ice cream.", 'Cat, cat; cat: cat', 'school(big)',
  'My friend is big — I like my friend.', 'xyz',
];

const VIET = [
  'Con viết đúng rồi!',
  'Con thử viết thêm câu cảm ơn: Thank you.',
  'Con nên dùng "big" thay vì "delicious".',
  'Câu "My school is delicious." có chữ chưa học.',
  'Good job!',
  'Con nhớ viết hoa chữ đầu câu nhé: My school is big.',
  '',
  'Thêm từ ice cream vào câu nhé',
];

test('chuTiengAnh: hai bản ra cùng kết quả trên 30 đầu vào', () => {
  for (const c of CA) {
    assert.deepEqual(may.chuTiengAnh(c), con.chuTiengAnh(c),
      `lệch ở ${JSON.stringify(c)}`);
  }
});

test('chuLa: hai bản ra cùng kết quả trên 30 đầu vào', () => {
  for (const c of CA) {
    assert.deepEqual(may.chuLa(c, KHO), con.chuLa(c, KHO), `lệch ở ${JSON.stringify(c)}`);
    /* Và cả khi kho rỗng — chỗ dễ lệch vì một bên có thể lui về "không soi". */
    assert.deepEqual(may.chuLa(c, {}), con.chuLa(c, {}), `kho rỗng, lệch ở ${JSON.stringify(c)}`);
  }
});

test('chuLaTrongViet: hai bản ra cùng kết quả', () => {
  for (const c of [...VIET, ...CA]) {
    assert.deepEqual(may.chuLaTrongViet(c, KHO), con.chuLaTrongViet(c, KHO),
      `lệch ở ${JSON.stringify(c)}`);
  }
});

test('CO_DAU_VIET: hai bản cùng một biểu thức', () => {
  assert.equal(String(may.CO_DAU_VIET), String(con.CO_DAU_VIET));
});

/**
 * ĐẢO CHIỀU: cổng này chỉ có nghĩa nếu nó ĐỎ khi hai bản thật sự lệch. Dựng một
 * bản "lệch" ngay tại đây rồi đòi phép so bắt được.
 */
test('cổng này ĐỎ được — thử với một bản cố ý lệch', () => {
  const lech = (cau, kho) => may.chuLa(cau, kho).filter((w) => w !== 'xyz');
  let batDuoc = false;
  for (const c of CA) {
    try { assert.deepEqual(lech(c, KHO), con.chuLa(c, KHO)); } catch { batDuoc = true; }
  }
  assert.ok(batDuoc, 'phép so không bắt được một bản lệch — nó đang canh hư không');
});

test('chuLaTrongCham gom đủ mọi trường mà máy con cũng soi', () => {
  /* Máy chủ phải soi ĐÚNG những trường `soiLoiCham` soi, không thừa không thiếu:
     thiếu thì nó bảo "sạch" rồi máy con bỏ mục ấy; thừa thì nó gọi lại vô cớ. */
  const cham = {
    diem: 8, khen: 'Con dùng đúng từ "school".',
    loi: [{ cau: 'My school is delicious.', sua: 'My school is big.', viSao: 'dùng "big"' },
          { cau: 'x', sua: 'My school is wonderful.', viSao: 'chữ "wonderful" chưa học' }],
    goiY: 'Con thử viết: I like cat.', choBoMe: 'Con làm tốt.',
  };
  const la = may.chuLaTrongCham(cham, KHO);
  assert.ok(la.includes('wonderful'), 'không bắt được chữ lạ trong `sua`');
  assert.ok(!la.includes('big') && !la.includes('school'), 'bắt oan chữ của bài');
  assert.ok(!la.includes('con') && !la.includes('thu'),
    'chữ Việt không dấu trong lời gợi ý bị coi là chữ lạ — lời gợi ý ĐÚNG sẽ bị bỏ');
  /* Lời chấm sạch thì không có chữ lạ nào. */
  assert.deepEqual(may.chuLaTrongCham({
    diem: 9, khen: 'Tốt', loi: [{ cau: 'x', sua: 'I like cat.', viSao: 'ổn' }],
    goiY: 'Viết thêm nhé', choBoMe: 'ổn',
  }, KHO), []);
});

/* ── HAI VẾ NỚI THÊM 10-10-2026, và chúng phải nới GIỐNG HỆT nhau ──
   Lệch ở đây hỏng theo kiểu khó thấy nhất: máy chủ duyệt một câu sửa rồi máy con
   bỏ đúng câu ấy — hai bên đều tin mình đúng, bé thì thấy lời chấm thiếu. */
const KHO_BE = { ...KHO, beViet: 'I can see two friend at the school gate.' };

test('chuLa: chữ chính bé vừa viết — hai bản tha giống nhau', () => {
  for (const c of [...CA, 'I can see two friends at the school gate.',
                   'The gate is big.', 'at the gate']) {
    assert.deepEqual(may.chuLa(c, KHO_BE), con.chuLa(c, KHO_BE),
      `lệch ở ${JSON.stringify(c)}`);
  }
  /* Và nó phải THẬT SỰ tha, không phải cả hai cùng bác. */
  assert.deepEqual(may.chuLa('at the gate', KHO_BE), []);
  assert.ok(may.chuLa('at the gate', KHO).length > 0);
});

test('gocBienHinh: đuôi đều thì tha, không có gốc thì vẫn bác', () => {
  for (const w of ['friends', 'friend', 'schools', 'has', 'the', 'is',
                   "friend's", 'cats', 'studies', 'playing', 'liked', 's', '']) {
    assert.deepEqual(may.gocBienHinh(w), con.gocBienHinh(w), `lệch ở ${w}`);
  }
  assert.deepEqual(may.chuLa('friends', KHO), []);            // friend → friends
  assert.deepEqual(may.chuLa('She has a cat', KHO), ['she', 'has', 'a']);
});
