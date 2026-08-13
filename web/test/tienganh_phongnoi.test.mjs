/**
 * CỔNG · PHÒNG LUYỆN NÓI — canh cái dễ nới ra nhất: VỐN TỪ.
 *
 * Phòng này gọi lên một mô hình ngôn ngữ, nên phần dễ hỏng không phải mã mà là LỜI
 * DẶN: nới một câu trong đó là máy bắt đầu dùng từ bé chưa học, và không có gì báo —
 * câu trả lời vẫn trôi chảy, vẫn đúng ngữ pháp, chỉ có bé là không hiểu. Cái bé học
 * được lúc ấy không phải tiếng Anh mà là "mình kém".
 *
 * Nên tệp này canh ba thứ, cả ba đều chạy được bằng node mà không cần mạng:
 *   1. vốn từ đúng chế độ: chưa đạt unit → chỉ unit ấy; đạt rồi → cộng unit cũ;
 *   2. ngữ cảnh bị CẮT trước khi gửi (client cắt, vì server không giữ gì);
 *   3. đọc được câu trả lời kể cả khi mô hình không trả đúng JSON.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  UNIT_CU_TOI_DA, LUOT_GUI_TOI_DA, CHU_TOI_DA,
  vonCuaBai, vonTu, moiTuDuocDung, moiCauDuocDung,
  loiDan, catNguCanh, goiGui, docTraLoi, tuTrongCau, LOI_LOP_HOC,
  viecTiepTheo, cauHopLe, cauThayThe, loaiOTrong,
} from '../src/mon/tienganh/lib/phongnoi.js';

const bai = (id, tu, cau, hinh = []) => ({
  id,
  title: `Unit ${id}`,
  hinhTu: hinh,
  knowledgeCore: {
    vocabulary: tu.map((t) => ({ tu: t, nghia: `nghĩa ${t}`, ipa: `/${t}/` })),
    /* Mẫu câu thật LUÔN có công thức với ô trống (`Hi, I'm + [Name].`), và loại ô
       trống là thứ quyết định điền được gì vào. Fixture bản đầu để công thức trùng
       luôn câu ví dụ — không có ô trống nào — nên nó thử một thứ không tồn tại
       trong dữ liệu thật. Dữ liệu giả phải giống dữ liệu thật ở đúng chỗ đang canh. */
    mauCauDs: cau.map((c) => (Array.isArray(c)
      ? { cau: c[0], congThuc: c[1], dungDe: 'để nói' }
      : { cau: c, congThuc: c, dungDe: 'để nói' })),
  },
});

const B01 = bai('B01', ['ball', 'bike', 'book'], [["Hi, I'm Bill.", "Hi, I'm + [Name]."]]);
const B02 = bai('B02', ['cake', 'car', 'cat'], ['This is a cat.']);
const B03 = bai('B03', ['apple', 'bag'], ['I have a bag.']);
const B04 = bai('B04', ['desk', 'dog'], ['A dog.']);
const B05 = bai('B05', ['chicken', 'chips', 'fish', 'milk'], [['I like milk.', 'I like + [Noun].']]);

/* ═══════════ VỐN TỪ ═══════════ */

test('chưa đạt unit thì CHỈ được dùng từ của chính unit ấy', () => {
  const v = vonTu({ baiNay: B05, baiCu: [B01, B02, B03, B04], daDat: false, datCu: () => true });
  assert.deepEqual(moiTuDuocDung(v), ['chicken', 'chips', 'fish', 'milk']);
  assert.deepEqual(moiCauDuocDung(v), ['I like milk.']);
  assert.equal(v.moRong, false);
});

test('đạt rồi thì cộng thêm từ của các unit ĐÃ ĐẠT trước đó', () => {
  const v = vonTu({ baiNay: B05, baiCu: [B01, B02, B03, B04], daDat: true, datCu: () => true });
  assert.equal(v.moRong, true);
  const tu = moiTuDuocDung(v);
  assert.ok(tu.includes('chicken'), 'vẫn phải có từ của chính unit');
  assert.ok(tu.includes('desk'), 'và từ của unit cũ');
});

test('unit cũ bé CHƯA đạt thì không được trộn vào', () => {
  /* Đây là chỗ dễ sai nhất: "đã học" không phải "đã đạt". Trộn cả unit bé mới mở
     ra xem rồi thoát thì máy nói bằng từ bé chưa hề học. */
  const v = vonTu({
    baiNay: B05, baiCu: [B01, B02, B03, B04], daDat: true,
    datCu: (id) => id === 'B01',
  });
  const tu = moiTuDuocDung(v);
  assert.ok(tu.includes('ball'), 'B01 đã đạt thì có');
  assert.ok(!tu.includes('cat'), 'B02 chưa đạt thì KHÔNG có');
  assert.ok(!tu.includes('dog'), 'B04 chưa đạt thì KHÔNG có');
});

test('chỉ trộn vài unit gần nhất, không đổ cả quyển vào', () => {
  const cu = [B01, B02, B03, B04];
  const v = vonTu({ baiNay: B05, baiCu: cu, daDat: true, datCu: () => true });
  assert.equal(v.on.length, UNIT_CU_TOI_DA);
  /* Giữ unit GẦN nhất, bỏ unit xa nhất — gần thì bé còn nhớ, và cũng vừa học xong. */
  assert.ok(!v.on.some((x) => x.id === 'B01'));
  assert.ok(v.on.some((x) => x.id === 'B04'));
});

test('unit ĐẦU quyển: đạt rồi cũng không có gì để trộn, và vẫn chạy', () => {
  const v = vonTu({ baiNay: B01, baiCu: [], daDat: true, datCu: () => true });
  assert.equal(v.moRong, false);
  assert.deepEqual(moiTuDuocDung(v), ['ball', 'bike', 'book']);
});

test('bài rỗng không làm vỡ gì', () => {
  const v = vonTu({ baiNay: {}, baiCu: [], daDat: false });
  assert.deepEqual(moiTuDuocDung(v), []);
  assert.equal(vonCuaBai(undefined).tu.length, 0);
});

/* ═══════════ LỜI DẶN ═══════════ */

test('lời dặn LIỆT KÊ đủ từ và cấm dùng từ ngoài danh sách', () => {
  const v = vonTu({ baiNay: B05, baiCu: [], daDat: false });
  const s = loiDan({ von: v, tenBe: 'Bo', lop: 1 });
  for (const t of ['chicken', 'chips', 'fish', 'milk']) assert.ok(s.includes(t), `thiếu từ ${t}`);
  assert.match(s, /ONLY these English words/i);
  assert.match(s, /Never introduce an English word outside this list/i);
  assert.match(s, /ONE short English sentence per turn/i);
  assert.match(s, /Vietnamese line/i, 'phải có lời tiếng Việt cho bé hiểu');
  assert.match(s, /JSON/, 'phải đòi JSON để tách hai thứ tiếng ra');
  assert.ok(s.includes('Bo'), 'gọi đúng tên bé');
});

test('lời lớp học: có, nhưng NGẮN và cố định', () => {
  /* Phát hiện khi gọi Groq thật: unit 5 chỉ có MỘT mẫu câu, nên bé chào "Chào cô"
     thì cô đáp "I like milk." — không phải máy sai, mà là cô không có gì để chào
     lại. Nhúm câu nghi thức này mở đúng một khe hẹp.

     Nới nó ra là quay lại đúng chỗ hỏng mà việc bó vốn từ sinh ra để tránh, nên
     cổng chặn số lượng và chặn cả việc lén thêm từ khó vào. */
  assert.ok(LOI_LOP_HOC.length <= 16, 'nhúm này phải NGẮN — nới ra là vốn từ rò');
  const s = loiDan({ von: vonTu({ baiNay: B05, baiCu: [], daDat: false }) });
  assert.ok(s.includes('Hello!'), 'lời dặn phải liệt kê nhúm này');
  assert.match(s, /not words the child must produce/i,
    'phải nói rõ đây là lời của CÔ, không phải từ bé phải học thuộc');
  /* Toàn câu ngắn, quen thuộc trong lớp — không phải chỗ nhét từ vựng mới vào. */
  for (const c of LOI_LOP_HOC) {
    assert.ok(c.split(/\s+/).length <= 4, `"${c}" dài quá cho một câu nghi thức`);
  }
});

test('lời dặn KHÔNG rò từ của unit bé chưa đạt', () => {
  const v = vonTu({ baiNay: B05, baiCu: [B01], daDat: false, datCu: () => true });
  const s = loiDan({ von: v });
  assert.ok(!s.includes('ball'), 'chưa đạt unit này thì không được nhắc từ unit khác');
});

/* ═══════════ NGỮ CẢNH ═══════════ */

test('ngữ cảnh bị CẮT, giữ lượt mới nhất', () => {
  const ds = Array.from({ length: 40 }, (_, i) => ({ vai: i % 2 ? 'be' : 'may', chu: `c${i}` }));
  const cat = catNguCanh(ds);
  assert.equal(cat.length, LUOT_GUI_TOI_DA);
  assert.equal(cat.at(-1).chu, 'c39', 'phải giữ lượt cuối');
});

test('lượt hỏng bị loại trước khi gửi', () => {
  const ds = [{ vai: 'may', chu: 'a' }, null, { vai: 'be' }, { vai: 'lung tung', chu: 'x' },
              { vai: 'be', chu: 'b' }];
  assert.deepEqual(catNguCanh(ds).map((x) => x.chu), ['a', 'b']);
});

test('gói gửi đổi đúng vai và chặn câu quá dài', () => {
  const g = goiGui([{ vai: 'may', chu: 'hello' }, { vai: 'be', chu: 'x'.repeat(1000) }]);
  assert.deepEqual(g.map((x) => x.role), ['assistant', 'user']);
  assert.equal(g[1].content.length, CHU_TOI_DA);
});

/* ═══════════ ĐỌC CÂU TRẢ LỜI ═══════════ */

test('đọc được JSON đúng chuẩn', () => {
  const r = docTraLoi('{"en":"I like milk.","vi":"Cô nói: con thích sữa."}');
  assert.equal(r.en, 'I like milk.');
  assert.equal(r.vi, 'Cô nói: con thích sữa.');
  assert.equal(r.thoJSON, false);
});

test('đọc được JSON lẫn trong chữ thừa', () => {
  const r = docTraLoi('Sure!\n```json\n{"en":"A cat.","vi":"Con mèo."}\n```');
  assert.equal(r.en, 'A cat.');
});

test('mô hình KHÔNG trả JSON thì vẫn phải dùng được', () => {
  /* Không được để màn trắng chỉ vì mô hình quên định dạng — bé đang ngồi đợi. */
  const r = docTraLoi('I like fish.\nCon nói theo cô nhé.');
  assert.equal(r.en, 'I like fish.');
  assert.equal(r.vi, 'Con nói theo cô nhé.');
  assert.equal(r.thoJSON, true);
});

test('câu rỗng không làm vỡ gì', () => {
  const r = docTraLoi('');
  assert.equal(r.en, '');
  assert.equal(r.vi, '');
});

/* ═══════════ HÌNH CHO TỪ ĐANG NÓI TỚI ═══════════ */

test('dò đúng từ trong câu để màn hình vẽ hình', () => {
  const v = vonTu({ baiNay: B05, baiCu: [], daDat: false });
  assert.deepEqual(tuTrongCau('I like milk.', v).map((t) => t.tu), ['milk']);
  assert.deepEqual(tuTrongCau('Chicken and chips!', v).map((t) => t.tu), ['chicken', 'chips']);
});

test('so theo TỪNG TIẾNG, không phải chuỗi con', () => {
  /* `includes('can')` khớp cả trong "I can see" — bé sẽ thấy hình cái LON trong khi
     máy đang nói "có thể". Đây là lỗi thật chứ không phải giả định. */
  const v = vonTu({ baiNay: bai('Bx', ['can', 'hat'], ['A can.']), baiCu: [], daDat: false });
  assert.deepEqual(tuTrongCau('I can see it.', v).map((t) => t.tu), []);
  assert.deepEqual(tuTrongCau('A can, please.', v).map((t) => t.tu), ['can']);
  assert.deepEqual(tuTrongCau('That hat is nice.', v).map((t) => t.tu), ['hat']);
});

test('dấu câu không làm mất hình', () => {
  const v = vonTu({ baiNay: B05, baiCu: [], daDat: false });
  assert.deepEqual(tuTrongCau('chips.', v).map((t) => t.tu), ['chips']);
  assert.deepEqual(tuTrongCau('Fish?', v).map((t) => t.tu), ['fish']);
});

test('không dò ra từ của unit bé chưa được dùng', () => {
  const v = vonTu({ baiNay: B05, baiCu: [B01], daDat: false, datCu: () => true });
  assert.deepEqual(tuTrongCau('I have a ball.', v).map((t) => t.tu), []);
});

/* ═══════════ CẮM VÀO THẬT ═══════════ */

test('hình của từ chỉ có MỘT nguồn', () => {
  /* Ba chỗ vẽ hình từ: thẻ từ, thanh việc, phòng luyện nói. Chỗ nào tự đọc lại
     `bai.hinhTu` là chỗ ấy sẽ lệch — đã dính thật một lần hôm nay (cả bốn ô vẽ ra
     dấu ❔ trong khi thẻ từ ngay dưới vẫn đủ hình). */
  const bo = (p) => readFileSync(new URL(p, import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  const nd = bo('../src/mon/tienganh/lib/noiDung.js');
  assert.equal((nd.match(/hinhTu/g) || []).length, 1, 'nguồn nằm ở đây, đúng một chỗ');
  for (const p of ['../src/mon/tienganh/components/BaiHoc.jsx',
                   '../src/mon/tienganh/lib/phongnoi.js']) {
    assert.equal((bo(p).match(/\.hinhTu/g) || []).length, 0,
      `${p} phải gọi hinhCuaTu(), không được tự đọc bai.hinhTu`);
  }
});

/* ═══════════ MICRO TREO — không được để bé kẹt ═══════════ */

test('xin micro có ĐỒNG HỒ CHẶN, không treo im lặng', async () => {
  /* Bắt được khi đi thử bản production 13-08: `getUserMedia` TREO — không trả lời
     mà cũng không từ chối, đo được 8 giây không hồi âm. Bản trước chỉ bắt trường
     hợp TỪ CHỐI, nên bé bấm "Đến lượt con" là KHÔNG CÓ GÌ xảy ra: không báo lỗi,
     không hiện "Đang nghe". Mà từ 13-08 việc NÓI là bắt buộc mới qua được chặng
     Từ mới — nên bé trên máy như thế kẹt luôn trong unit, không một dòng giải
     thích. Bé kẹt vì cái micro, chứ không vì sức học. */
  const cu = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  const dat = (v) => Object.defineProperty(globalThis, 'navigator', { value: v, configurable: true });
  dat({ mediaDevices: { getUserMedia: () => new Promise(() => {}) } });
  try {
    const { xinMicroChiTiet, MICRO, loiDocDuoc } = await import('../src/mon/tienganh/lib/nghenoi.js');
    const t0 = Date.now();
    const kq = await xinMicroChiTiet({ hanGio: 300 });
    assert.equal(kq, MICRO.khongTraLoi, 'treo thì phải cắt, không đợi mãi');
    assert.ok(Date.now() - t0 < 2000, 'phải cắt đúng hạn, không treo theo');
    assert.match(loiDocDuoc(kq), /micro/i, 'và phải có lời nói rõ cho bé');
  } finally { if (cu) Object.defineProperty(globalThis, 'navigator', cu); }
});

test('micro bị TỪ CHỐI vẫn phân biệt được với micro TREO', async () => {
  /* Hai chuyện khác hẳn nhau: từ chối thì bố mẹ bật lại được, treo thì không.
     Gộp làm một câu là bố mẹ đi bật quyền cho một cái máy chẳng có micro. */
  const cu = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  const dat = (v) => Object.defineProperty(globalThis, 'navigator', { value: v, configurable: true });
  const { xinMicroChiTiet, MICRO } = await import('../src/mon/tienganh/lib/nghenoi.js');
  try {
    dat({ mediaDevices: { getUserMedia: () => Promise.reject(new Error('x')) } });
    assert.equal(await xinMicroChiTiet({ hanGio: 300 }), MICRO.tuChoi);
    dat({});
    assert.equal(await xinMicroChiTiet({ hanGio: 300 }), MICRO.khongCo);
  } finally { if (cu) Object.defineProperty(globalThis, 'navigator', cu); }
});

test('cả hai chỗ xin micro đều dùng bản CÓ ĐỒNG HỒ', () => {
  const bo = (p) => readFileSync(new URL(p, import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  for (const p of ['../src/mon/tienganh/components/NutNoi.jsx',
                   '../src/mon/tienganh/components/PhongNoi.jsx']) {
    const s = bo(p);
    assert.match(s, /xinMicroChiTiet\(\)/, `${p} phải dùng bản có đồng hồ chặn`);
    assert.doesNotMatch(s, /await xinMicro\(\)/, `${p} không được dùng bản trần`);
  }
});

/* ═══════════ SOI LẠI CÂU CÔ NÓI ═══════════ */

test('câu hợp lệ: từ vựng · lời lớp học · câu ví dụ · công thức đã điền', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const ok = (s) => cauHopLe(s, { von, tenBe: 'Bo' });
  assert.ok(ok('ball'), 'một từ trong vốn từ');
  assert.ok(ok('Good job!'), 'lời lớp học');
  assert.ok(ok("Hi, I'm Bill."), 'câu ví dụ của bài');
  assert.ok(ok("Hi, I'm Bo."), 'công thức điền TÊN bé');
});

test('câu KHÔNG hợp lệ bị chặn — kể cả khi nghe rất xuôi tai', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const ok = (s) => cauHopLe(s, { von, tenBe: 'Bo' });
  /* Đã sinh ra thật khi thử với Groq, dù lời dặn đã nói rõ ô trống là chỗ của TÊN.
     Với bé 6 tuổi đang tập nhại thì đây là dạy sai, và bé sẽ nhớ. */
  assert.ok(!ok('Bye, book.'), 'nhét đồ vật vào ô của tên người');
  assert.ok(!ok('Bye, bike.'), 'y hệt, và đây là câu Groq đã sinh ra thật');
  assert.ok(!ok('Do you like chips?'), 'từ ngoài vốn của bé');
  assert.ok(!ok('I have a ball.'), 'mẫu câu bài này chưa dạy');
  assert.ok(!ok(''), 'câu rỗng');
});

test('ô trống biết mình thuộc loại nào', () => {
  assert.equal(loaiOTrong("Hi, I'm + [Name]."), 'ten');
  assert.equal(loaiOTrong('I like + [Noun].'), 'tu');
  assert.equal(loaiOTrong('không có ô trống'), null);
});

test('câu thay thế LUÔN hợp lệ — đó là cả lý do nó tồn tại', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  for (let n = 0; n < 9; n += 1) {
    const ls = Array.from({ length: n }, () => ({ vai: 'may', en: 'x' }));
    const v = viecTiepTheo({ von, lichSu: ls });
    const t = cauThayThe(v, 'Bo');
    assert.ok(t && t.en && t.vi, `lượt ${n} không dựng được câu thay thế`);
    assert.ok(cauHopLe(t.en, { von, tenBe: 'Bo' }),
      `lượt ${n}: câu thay thế "${t.en}" lại KHÔNG hợp lệ`);
  }
});

test('việc xoay vòng — không lượt nào giống lượt trước', () => {
  /* Bác bắt: "nó cứ nói đi nói lại hello với mấy câu nhàm chán". Dựng lại thì cô
     nói đúng một câu sáu lượt liền. Nay việc do máy con chọn, nên đếm được. */
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const ds = [];
  const ls = [];
  for (let n = 0; n < 6; n += 1) {
    const v = viecTiepTheo({ von, lichSu: ls });
    ds.push(`${v.kieu}:${v.tu.tu}`);
    ls.push({ vai: 'may', en: cauThayThe(v, 'Bo').en });
  }
  for (let i = 1; i < ds.length; i += 1) {
    assert.notEqual(ds[i], ds[i - 1], `lượt ${i} lặp y hệt lượt trước: ${ds[i]}`);
  }
  assert.ok(new Set(ds).size >= 4, `mới có ${new Set(ds).size} kiểu việc khác nhau trong 6 lượt`);
});

test('chọn từ ÍT được nhắc nhất, không phải từ đầu bảng', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const ls = [{ vai: 'may', en: 'ball' }, { vai: 'may', en: 'ball' }, { vai: 'may', en: 'bike' }];
  const v = viecTiepTheo({ von, lichSu: ls });
  assert.equal(v.tu.tu, 'book', 'book chưa được nhắc lần nào');
});
