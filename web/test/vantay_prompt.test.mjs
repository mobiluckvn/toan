/**
 * CỔNG · VÂN TAY PROMPT KHÔNG ĐƯỢC MANG THEO CHỮ NÀO CỦA BÉ.
 *
 * Bác chốt 21-08-2026: lưu VÂN TAY prompt thay vì nguyên văn — đủ để so "mẫu lời
 * dặn nào dạy hiệu quả hơn" (ΔC, mục 2.5.3) mà giữ nguyên giao ước "máy chủ KHÔNG
 * lưu gì".
 *
 * Giao ước ấy chỉ đứng vững nếu vân tay đúng là vân tay của KHUNG. Hai cách hỏng:
 *
 *  1. BĂM CẢ PROMPT. Prompt có tên bé, vốn từ của unit, cả lịch sử hội thoại —
 *     nên mỗi lượt ra một vân tay riêng. Vừa vô dụng cho việc so mẫu (không nhóm
 *     lại được), vừa thành một mã theo dõi được từng lượt của từng bé.
 *
 *  2. HAI BÉ CÙNG UNIT RA HAI VÂN TAY. Cùng triệu chứng, cùng nguyên nhân.
 *     Phép canh dưới đây bắt bằng cách dựng hai bé khác hẳn nhau rồi đòi bằng nhau.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { vanTay, locKhung, PHIEN_BAN_MAU } from '../functions/src/vantay.js';
import { khungCham, loiDanCham } from '../functions/src/chamviet.js';
import { dongTheoNhan } from '../src/mon/tienganh/lib/loidan_nhan.js';
import { NHAN } from '../src/mon/tienganh/lib/nhanluot.js';

const beA = {
  de: 'Viết 3 câu về trường của em.',
  viet: 'My school is big. I like my school.',
  vonTu: [{ tu: 'school', nghia: 'trường' }, { tu: 'big', nghia: 'to' }],
  mauCau: ['My school is + [Adjective].'],
  lop: 5,
};
const beB = {
  de: 'Viết 3 câu về con vật em thích.',
  viet: 'I like dogs. Dogs are friendly. My dog is small.',
  vonTu: [{ tu: 'dog', nghia: 'con chó' }, { tu: 'friendly', nghia: 'thân thiện' }],
  mauCau: ['I like + [Animal].'],
  lop: 5,
};

test('hai bé khác hẳn nhau, cùng lớp → CÙNG một vân tay', () => {
  const a = vanTay('chamviet', khungCham(beA.lop, true));
  const b = vanTay('chamviet', khungCham(beB.lop, true));
  assert.equal(a.vanTayPrompt, b.vanTayPrompt,
    'vân tay đổi theo bé → không nhóm lại được để so mẫu, và thành mã theo dõi từng lượt');
});

test('lớp khác nhau thì vân tay khác — lời dặn thật sự khác', () => {
  const a = vanTay('chamviet', khungCham(3, true));
  const b = vanTay('chamviet', khungCham(5, true));
  assert.notEqual(a.vanTayPrompt, b.vanTayPrompt,
    'câu đầu lời dặn ghi rõ lớp, gom chung lớp 3 với lớp 5 là gom nhầm hai mẫu');
});

test('khung KHÔNG chứa một chữ nào của bé', () => {
  const k = khungCham(5, true);
  for (const x of [...beA.vonTu.map((v) => v.tu), ...beA.vonTu.map((v) => v.nghia),
                   ...beA.mauCau, beA.de, beA.viet]) {
    assert.ok(!k.includes(x), `khung lọt dữ liệu của bé: ${JSON.stringify(x)}`);
  }
  /* Nhưng vẫn phải còn KHUNG thật, không phải chuỗi rỗng — băm chuỗi rỗng thì mọi
     mẫu ra cùng một vân tay và phép so chết lặng. */
  assert.ok(k.length > 300, 'khung ngắn bất thường — có phải đã lọc mất cả luật chấm?');
  assert.match(k, /LUẬT CHẤM/, 'khung mất phần luật chấm — đó chính là thứ cần so');
});

test('khung dựng lại từ CHÍNH hàm lời dặn, nên sửa lời dặn là khung tự đổi', () => {
  /* Không có bảng nào phải nhớ cập nhật — đây là điểm khác `locKhung`. */
  const that = loiDanCham({ ...beA });
  const khung = khungCham(beA.lop, true);
  assert.match(that, /LUẬT CHẤM/);
  assert.match(khung, /LUẬT CHẤM/);
  assert.ok(that.length > khung.length, 'lời dặn thật phải dài hơn khung');
});

test('có mẫu câu hay không là hai khung khác nhau', () => {
  assert.notEqual(vanTay('chamviet', khungCham(5, true)).vanTayPrompt,
                  vanTay('chamviet', khungCham(5, false)).vanTayPrompt,
    'khối "MẪU CÂU BÉ ĐÃ HỌC" có/không là khác cấu trúc lời dặn thật');
});

test('đổi mô hình hay nhiệt độ thì vân tay đổi', () => {
  const k = khungCham(5, true);
  assert.notEqual(vanTay('chamviet', k, { moHinh: 'a' }).vanTayPrompt,
                  vanTay('chamviet', k, { moHinh: 'b' }).vanTayPrompt,
    'đổi mô hình mà vân tay không đổi → so ΔG giữa hai mô hình sẽ gom nhầm làm một');
  assert.notEqual(vanTay('chamviet', k, { nhiet: 0.2 }).vanTayPrompt,
                  vanTay('chamviet', k, { nhiet: 0.9 }).vanTayPrompt);
});

test('vân tay là một chiều và ngắn gọn', () => {
  const v = vanTay('chamviet', khungCham(5, true));
  assert.match(v.vanTayPrompt, /^[0-9a-f]{12}$/, 'vân tay phải là băm hex 12 ký tự');
  assert.ok(!v.vanTayPrompt.includes('cô giáo'), 'vân tay lộ chữ của lời dặn');
  assert.equal(v.mauPrompt, 'chamviet');
  assert.equal(v.phienBanMau, PHIEN_BAN_MAU.chamviet);
});

test('locKhung bỏ được dòng mang dữ liệu của bé', () => {
  /* Đây là lưới đỡ cho phòng nói — nơi lời dặn do máy con dựng nên máy chủ không
     gọi lại được hàm dựng. Nó lọc THEO DẤU HIỆU nên sót được; cổng này chỉ canh
     những dấu hiệu ĐÃ KHAI, và chỗ gọi phải biết giới hạn ấy. */
  const loi = [
    'You are an English teacher for a Vietnamese child.',
    'Vốn từ bé đã học: dog · cat · bird',
    'The child told you they like "dolphin".',
    'Tên bé là Bo.',
    '- Hi, how are you?',
    'Answer in JSON only.',
  ].join('\n');
  const k = locKhung(loi);
  assert.ok(k.includes('You are an English teacher'));
  assert.ok(k.includes('Answer in JSON only.'));
  for (const x of ['dolphin', 'Bo', 'dog · cat · bird', 'Hi, how are you']) {
    assert.ok(!k.includes(x), `locKhung để lọt: ${x}`);
  }
});

test('hai lượt nói của HAI bé khác nhau vẫn ra cùng vân tay', () => {
  const khung = 'You are an English teacher.\nAnswer in JSON only.';
  const a = `${khung}\nTên bé là An.\nVốn từ bé đã học: dog`;
  const b = `${khung}\nTên bé là Bình.\nVốn từ bé đã học: cat · fish`;
  assert.equal(vanTay('luyennoi', locKhung(a)).vanTayPrompt,
               vanTay('luyennoi', locKhung(b)).vanTayPrompt);
});

test('mọi mẫu đều phải khai số phiên bản', () => {
  for (const m of ['luyennoi', 'chamviet']) {
    assert.equal(typeof PHIEN_BAN_MAU[m], 'number',
      `mẫu '${m}' chưa khai phiên bản — bảng so ΔC gom theo số này`);
  }
});

/**
 * DÒNG LỜI DẶN THEO NHÃN (việc V2) MANG CHỮ BÉ VỪA NÓI.
 *
 * Phòng luyện nói là chỗ vân tay YẾU NHẤT: lời dặn do MÁY CON dựng rồi gửi lên đã
 * thành chữ, nên máy chủ chỉ còn cách lọc theo dấu hiệu (`locKhung`) — và
 * `luyennoi.js` đã nói trước là lọc theo dấu hiệu thì sót được. V2 thêm hẳn chín
 * dòng mới mang chữ của bé, tức thêm chín chỗ có thể sót.
 *
 * Nên giao ước thành một dấu DUY NHẤT và khai sẵn: mọi dòng mang dữ liệu của bé
 * mở đầu bằng `CHILD:` (xem `loidan_nhan.js`). Phép canh dưới đây dựng hai bé khác
 * hẳn nhau rồi đòi khung BẰNG NHAU — cùng cách đã dùng cho bên chấm viết.
 */
test('lời dặn theo nhãn: hai bé khác nhau → CÙNG một khung', () => {
  const beA = { beNoi: 'con noi im bo', dich: "Hi, I'm Bo.", thieu: ['hi'], nham: 'duck' };
  const beB = { beNoi: 'con noi la mi', dich: 'My name is Mai.', thieu: ['name'], nham: 'cat' };
  for (const nhan of Object.keys(NHAN)) {
    assert.equal(
      locKhung(dongTheoNhan(nhan, beA)), locKhung(dongTheoNhan(nhan, beB)),
      `nhãn ${nhan}: vân tay đổi theo bé → vừa không nhóm lại được để so mẫu, vừa thành mã theo dõi`,
    );
  }
});

test('nhưng TÊN NHÃN thì phải còn trong khung', () => {
  /* Lọc sạch cả tên nhãn thì chín nhánh ra cùng một vân tay, và bảng so ΔC (V8)
     không trả lời được câu "nhánh nào dạy tốt hơn" — tức mất đúng cái nó sinh ra
     để đo. Đây là nửa còn lại của phép canh trên: một nửa đòi BỎ, nửa này đòi GIỮ. */
  const k = locKhung(dongTheoNhan(NHAN.thieuTu, { beNoi: 'x', dich: 'y', thieu: ['z'] }));
  assert.match(k, /TURN TYPE: thieuTu/);
  assert.notEqual(
    locKhung(dongTheoNhan(NHAN.thieuTu, {})), locKhung(dongTheoNhan(NHAN.dung, {})),
    'hai nhãn khác nhau phải ra hai khung khác nhau',
  );
});
