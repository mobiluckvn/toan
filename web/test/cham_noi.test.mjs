/**
 * BỘ CHẤM BÀI NÓI.
 * chạy: node test/cham_noi.test.mjs
 *
 * ── PHÉP KIỂM NÀY THỬ BẰNG GÌ ──
 * Không thử bằng chuỗi lý tưởng, mà bằng ĐÚNG NHỮNG GÌ máy nhận dạng trả về khi
 * một đứa bé đọc: viết tắt bung ra, số thành chữ số, thừa mạo từ, thừa "um", thừa
 * cả câu dẫn. Bé đọc ĐÚNG mà bộ chấm cho 4 điểm thì bé nghỉ — nên chỗ đắt nhất ở
 * đây là KHÔNG ĐƯỢC PHẠT OAN.
 *
 * Nhưng cũng có một chỗ tuyệt đối không được nới: `dog` và `duck` là hai từ CÙNG
 * MỘT UNIT. Nới ở đó thì bài nói mất hết ý nghĩa, và tệ hơn — bé tưởng mình đúng.
 */
import {
  chuanHoa, giongNhau, chamTu, chamCau, chamTot, loiKhen, datNoi, DAT,
} from '../src/mon/tienganh/lib/chamnoi.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ══ 1 · TIỀN XỬ LÝ — chỗ quyết định độ chính xác ══ */
console.log('\n── tiền xử lý ──');
t('bung viết tắt: I\'m → i am', chuanHoa("Hi, I'm Bill.") === 'hi i am bill');
t('bung viết tắt sau khi gộp nháy cong', chuanHoa('She’s running.') === 'she is running');
t('chữ số → chữ: 6 → six', chuanHoa('I can see 6.') === 'i can see six');
t('bỏ dấu câu', chuanHoa('How many clocks? - Two.') === 'how many clocks two');
t('bỏ tiếng đệm', chuanHoa('um... this is a dog') === 'this is a dog');
t('gộp khoảng trắng thừa', chuanHoa('  this   is  a dog  ') === 'this is a dog');
t('hai vế cùng dạng thì khớp',
  chuanHoa("It's a red pen.") === chuanHoa('it is a red pen'));

/* ══ 2 · TỪ — KHÔNG PHẠT OAN ══
   Mỗi dòng dưới đây là một cách STT thật sự trả về khi bé đọc đúng chữ "dog". */
console.log('\n── chấm từ: bé đọc ĐÚNG ──');
const DOI = ['desk', 'dog', 'door', 'duck'];
for (const [nghe, ten] of [
  ['dog', 'đọc trơn'],
  ['Dog.', 'STT thêm hoa và chấm'],
  ['a dog', 'bé nói thừa mạo từ'],
  ['the dog', 'bé nói thừa "the"'],
  ['um dog', 'bé ngập ngừng'],
  ['it is a dog', 'bé nói cả câu'],
]) {
  const k = chamTu('dog', nghe, { doiThu: DOI });
  t(`"${nghe}" (${ten}) → 10 điểm, được ${k.diem}`, k.diem === 10);
}

console.log('\n── chấm từ: bé đọc NHẦM SANG TỪ BÊN CẠNH ──');
for (const nham of ['duck', 'door', 'desk']) {
  const k = chamTu('dog', nham, { doiThu: DOI });
  t(`nói "${nham}" khi hỏi "dog" → tối đa 3 điểm, được ${k.diem}`, k.diem <= 3);
  t(`  và nói rõ nhầm thành "${nham}"`, k.lyDo === 'nhamTu' && k.nhamThanh === nham);
}
/* Không khai đối thủ thì KHÔNG được tự bịa ra — "duck" lúc ấy chỉ là đọc lệch. */
t('không có danh sách đối thủ thì không báo nhầm',
  chamTu('dog', 'duck').lyDo !== 'nhamTu');

console.log('\n── chấm từ: đọc lệch, không phải từ nào khác ──');
t('"dogg" (thừa một chữ) vẫn ≥ 7', chamTu('dog', 'dogg', { doiThu: DOI }).diem >= 7);
t('"teddy bear" nói đủ hai chữ → 10',
  chamTu('teddy bear', 'teddy bear', { doiThu: [] }).diem === 10);
t('"teddy" thiếu nửa sau → dưới 8', chamTu('teddy bear', 'teddy').diem < 8);
t('im lặng → 0 điểm', chamTu('dog', '').diem === 0);
t('im lặng có lý do riêng', chamTu('dog', '  ').lyDo === 'khongNghe');

/* ══ 3 · CÂU ══ */
console.log('\n── chấm câu ──');
const C = 'This is a dog.';
t('đọc đúng → 10', chamCau(C, 'This is a dog.').diem === 10);
t('STT bung viết tắt vẫn 10', chamCau("It's a red pen.", 'it is a red pen').diem === 10);
t('thừa câu dẫn vẫn ≥ 8', chamCau(C, 'I think this is a dog').diem >= 8);
{
  /* Thiếu MẠO TỪ là lỗi nhỏ — bé nói được cái nó định nói. */
  const k = chamCau(C, 'this is dog');
  t(`thiếu "a" vẫn ≥ 8 (được ${k.diem})`, k.diem >= 8);
  t('  và chỉ ra đúng chữ còn thiếu', k.thieuChucNang.includes('a'));
}
{
  /* Thiếu DANH TỪ là chưa nói được ý — phải nặng hơn hẳn. */
  const k = chamCau(C, 'this is a');
  t(`thiếu danh từ → dưới 7 (được ${k.diem})`, k.diem < 7);
  t('  và chỉ ra "dog" còn thiếu', k.thieu.includes('dog'));
}
t('thiếu danh từ phải nặng hơn thiếu mạo từ',
  chamCau(C, 'this is a').diem < chamCau(C, 'this is dog').diem);
{
  const dung = chamCau(C, 'this is a dog').diem;
  const dao = chamCau(C, 'dog a is this').diem;
  t(`đảo thứ tự phải thấp hơn đúng thứ tự (${dao} < ${dung})`, dao < dung);
}
t('nói câu khác hẳn → dưới 4', chamCau(C, 'I like milk').diem < 4);
t('im lặng → 0', chamCau(C, '').diem === 0);
t('câu dài đọc đúng → 10',
  chamCau('How many windows can you see?', 'how many windows can you see').diem === 10);

/* ══ 4 · KHÍCH LỆ — luật quan trọng nhất với bé 6 tuổi ══ */
console.log('\n── khích lệ ──');
{
  const xau = loiKhen(chamCau(C, 'I like milk'));
  t('điểm thấp: câu ĐẦU không phải lời chê',
    !/sai|kém|chưa được|dở/i.test(xau.chinh));
  t('điểm thấp: vẫn nói rõ phải sửa gì', !!xau.them && xau.them.length > 8);
}
{
  const nham = loiKhen(chamTu('dog', 'duck', { doiThu: DOI }));
  t('đọc nhầm từ: khen phần nói rõ trước', /rõ|tốt|được/i.test(nham.chinh));
  t('đọc nhầm từ: nói ra bé vừa đọc thành chữ gì', nham.chinh.includes('duck'));
}
t('hơn lần trước thì được ghi nhận',
  loiKhen(chamCau(C, 'this is a dog'), 6).chinh.includes('Hơn lần trước'));
t('10 điểm → 3 sao', loiKhen(chamCau(C, 'this is a dog')).sao === 3);
t('không nghe thấy → 0 sao, và bảo bé nói to hơn',
  loiKhen(chamTu('dog', '')).sao === 0 && /to hơn/.test(loiKhen(chamTu('dog', '')).them));

/* ══ 4B · NHIỀU PHƯƠNG ÁN NGHE ══
   Web Speech trả tới ba phương án, và với giọng trẻ con thì phương án ĐÚNG rất hay
   không đứng đầu. Chỉ đọc phương án đầu là phạt oan bé một cách có hệ thống. */
console.log('\n── nhiều phương án ──');
t('lấy phương án tốt nhất, không phải phương án đầu',
  chamTot(chamTu, 'dog', ['duck', 'dock', 'dog'], { doiThu: [] }).diem === 10);
t('phương án đầu đã đúng thì vẫn 10',
  chamTot(chamTu, 'dog', ['dog', 'dock'], { doiThu: [] }).diem === 10);
t('mọi phương án đều sai thì vẫn thấp',
  chamTot(chamCau, C, ['I like milk', 'I like fish']).diem < 4);
t('không có phương án nào → 0', chamTot(chamTu, 'dog', []).diem === 0);
t('nhận cả chuỗi đơn lẻ', chamTot(chamTu, 'dog', 'dog', { doiThu: [] }).diem === 10);
t('có ghi lại đã xét mấy phương án',
  chamTot(chamTu, 'dog', ['a', 'b', 'dog'], { doiThu: [] }).soPhuongAn === 3);
/* Đọc nhầm sang từ bên cạnh thì NHIỀU phương án cũng không cứu được. */
t('nhiều phương án KHÔNG cứu được việc đọc nhầm từ',
  chamTot(chamTu, 'dog', ['duck', 'ducks'], { doiThu: DOI }).diem <= 3);

/* ══ 5 · NGƯỠNG ĐẠT ══ */
console.log('\n── ngưỡng ──');
t(`ngưỡng đạt là ${DAT}/10 — thấp có chủ ý, đây là lần ĐẦU bé nói tiếng Anh`, DAT === 6);
t('thiếu mạo từ vẫn ĐẠT', datNoi(chamCau(C, 'this is dog').diem));
t('thiếu danh từ thì CHƯA đạt', !datNoi(chamCau(C, 'this is a').diem));
t('đọc nhầm sang từ khác thì CHƯA đạt',
  !datNoi(chamTu('dog', 'duck', { doiThu: DOI }).diem));

/* ══ 6 · KHÔNG BAO GIỜ RA ĐIỂM VÔ LÝ ══ */
console.log('\n── biên ──');
const thu = ['', ' ', 'dog', 'DOG!!!', 'a a a a a', '123', '???', 'this is a dog',
  'um uh er', 'x'.repeat(200)];
let ngoai = 0;
for (const x of thu) {
  for (const k of [chamTu('dog', x, { doiThu: DOI }), chamCau(C, x)]) {
    if (!Number.isInteger(k.diem) || k.diem < 0 || k.diem > 10) ngoai += 1;
  }
}
t(`mọi đầu vào lạ vẫn ra điểm nguyên 0..10 (${ngoai} chỗ lệch)`, ngoai === 0);
t('giongNhau nằm trong 0..1', [['a', 'b'], ['', ''], ['abc', 'abc']]
  .every(([a, b]) => giongNhau(a, b) >= 0 && giongNhau(a, b) <= 1));

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
