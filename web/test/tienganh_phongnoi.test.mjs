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
  vonCuaBai, vonTu, moiTuDuocDung, moiCauDuocDung, SO_DEM,
  loiDan, catNguCanh, goiGui, docTraLoi, tuTrongCau, LOI_LOP_HOC,
  viecTiepTheo, cauHopLe, cauThayThe, loaiOTrong, tachTheoTieng,
  tinhBuoi, loiKet, tuLoiKetHopLe, cauHoiSoThich, PHUT_TOI_DA, DAT_LIEN_DE_XONG,
  buocTiepTheo, dienBuoc, dongBuoc, xenKe,
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

/* ═══════════ TÁCH LỜI GIẢI THÍCH THEO THỨ TIẾNG ═══════════ */

const vonB01 = () => vonTu({ baiNay: B01, baiCu: [], daDat: false });

test('từ tiếng Anh trong lời Việt được tách ra để đọc giọng Anh', () => {
  /* Bác bắt 13-08: "phần giải thích khi có từ tiếng Anh phát bằng tiếng Việt rất
     không okay". Bé đang tập nhại mà nghe `ball` đọc giọng Việt thì học sai đúng
     chỗ mình đang dạy — mà kho này đã chốt "mỗi dòng chỉ MỘT thứ tiếng" từ lâu. */
  const ds = tachTheoTieng('Con nói lại từ "ball" nhé, nghĩa là quả bóng.', vonB01());
  assert.deepEqual(ds.map((x) => x.tieng), ['vi', 'en', 'vi']);
  assert.equal(ds[1].chu, 'ball');
});

test('cả câu mẫu giữ nguyên KHỐI, không bị xé lẻ', () => {
  /* Xé "Hi, I'm Bill." thành mấy mẩu rồi đọc rời thì mất nhịp câu — mà nhịp mới là
     thứ bé đang tập. Nên khớp câu TRƯỚC, khớp từ SAU. */
  const ds = tachTheoTieng("Cô vừa nói: Hi, I'm Bill. Bây giờ con lặp lại.", vonB01());
  assert.equal(ds.filter((x) => x.tieng === 'en').length, 1);
  assert.equal(ds.find((x) => x.tieng === 'en').chu, "Hi, I'm Bill.");
});

test('KHÔNG nhận nhầm chữ tiếng Việt thành từ tiếng Anh', () => {
  /* Chỗ này mà sai thì lời giải thích tiếng Việt bị đọc lắp bắp giọng Anh giữa
     chừng — nghe còn tệ hơn cái lỗi đang sửa. */
  const von = vonTu({ baiNay: bai('Bx', ['can', 'hat', 'bag'], []), baiCu: [], daDat: false });
  for (const c of ['Con cần cố gắng nhé.', 'Cái bàn có hạt dưa.', 'Bé mang bao gạo.']) {
    const ds = tachTheoTieng(c, von);
    assert.equal(ds.filter((x) => x.tieng === 'en').length, 0, `nhận nhầm trong: ${c}`);
  }
});

test('tên bé KHÔNG bị tách — tên Việt thì đọc giọng Việt', () => {
  const ds = tachTheoTieng('Tạm biệt Bo, con nói lại nhé.', vonB01());
  assert.equal(ds.filter((x) => x.tieng === 'en').length, 0);
});

test('không mọc ra mẩu chỉ có dấu câu', () => {
  /* Mẩu rỗng hoặc chỉ còn dấu chấm thì bộ đọc phát ra một tiếng nấc giữa câu. */
  const ds = tachTheoTieng('ball. bike!', vonB01());
  assert.ok(ds.every((x) => /[\p{L}\p{N}]/u.test(x.chu)), 'còn mẩu rỗng');
  assert.deepEqual(ds.map((x) => x.chu), ['ball', 'bike']);
});

test('câu thuần Việt trả về đúng MỘT đoạn', () => {
  const ds = tachTheoTieng('Con làm tốt lắm, cố lên nhé!', vonB01());
  assert.equal(ds.length, 1);
  assert.equal(ds[0].tieng, 'vi');
});

test('câu rỗng không làm vỡ gì', () => {
  assert.deepEqual(tachTheoTieng('', vonB01()), []);
  assert.deepEqual(tachTheoTieng('abc', null), []);
});

test('màn phòng nói KHÔNG đọc lời Việt bằng một giọng duy nhất nữa', () => {
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /docDoan\(tachTheoTieng\(/, 'lời Việt phải đi qua phép tách');
  assert.doesNotMatch(pn, /docLen\([^)]*\.vi[^)]*'vi-VN'/, 'không được đọc thẳng cả dòng vi');
});

/* ═══════════ THỨ TỰ TIN NHẮN ═══════════ */

test('phòng nói bày tin MỚI Ở DƯỚI, và TỰ CUỘN xuống', () => {
  /* Bác chốt 14-08, sau khi đi qua cả hai chiều:
       · mới ở dưới, không tự cuộn (bản đầu) → bé ngồi nhìn câu cũ;
       · mới ở trên (13-08)                  → chữa được cuộn, nhưng đọc ngược đời.
     Nay chiều tự nhiên VÀ tự cuộn. Cặp này phải đi cùng nhau: bỏ chiều thì khó
     đọc, bỏ cuộn thì bé không thấy cô trả lời — mà bỏ cuộn KHÔNG có gì đỏ cả. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.doesNotMatch(pn, /\.reverse\(\)/, 'danh sách KHÔNG đảo nữa — cũ trên, mới dưới');
  assert.match(pn, /scrollIntoView\(\{[^}]*block:\s*'end'/,
    'phải cuộn xuống ĐÁY khi có lượt mới, nếu không bé không thấy cô trả lời');
  assert.match(pn, /cuoiDs/, 'phải có neo cuộn ở cuối');

  /* Đánh số chỉ số THẬT rồi mới lọc: nút "nói lại" sửa đúng một ô trong `lichSu`,
     mà lọc trước thì số thứ tự xê dịch và bé bấm ô này lại sửa ô khác. */
  const iSo = pn.indexOf('.map((x, i) => ({ x, i }))');
  const iLoc = pn.indexOf('.filter(({ x, i })');
  assert.ok(iSo > 0 && iLoc > iSo, 'phải ĐÁNH SỐ trước rồi mới LỌC');
});

test('neo cuộn đứng SAU nút nói — bé thấy câu mới và cái nút cùng lúc', () => {
  /* Neo đặt ngay sau danh sách thì cuộn xong cái nút vẫn nằm dưới mép màn hình,
     và bé không biết phải bấm gì tiếp. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.ok(pn.indexOf('<ol') < pn.indexOf('Đến lượt con'),
    'danh sách lượt phải nằm trước nút nói');
  assert.ok(pn.indexOf('Đến lượt con') < pn.indexOf('ref={cuoiDs}'),
    'neo cuộn phải nằm SAU nút nói');
});

/* ═══════════ CÂU KẾT CÓ TIẾNG · NÓI LẠI ═══════════ */

test('câu kết có câu tiếng Anh để bé NGHE và học', () => {
  /* Bác dặn 14-08: "câu kết thúc thì cũng nên chuyển sang Voice". Cả buổi mọi thứ
     đều có tiếng, tới lúc chia tay thì im bặt — với bé chưa đọc chữ thì đó là
     phòng học tắt tiếng giữa chừng. */
  for (const tt of [
    tinhBuoi({ lichSu: [9, 8, 9].map((d) => ({ vai: 'be', diem: d })), batDau: 0, bayGio: 60000 }),
    tinhBuoi({ lichSu: [{ vai: 'be', diem: 3 }], batDau: 0, bayGio: PHUT_TOI_DA * 60000 }),
  ]) {
    const k = loiKet(tt);
    assert.ok(k, 'phải có màn kết');
    assert.ok(k.en && k.en.trim(), 'màn kết phải có câu tiếng Anh');
  }
});

test('câu kết CHỈ dùng lời lớp học — không được bịa từ lạ vào phút cuối', () => {
  /* Câu này máy con tự viết, KHÔNG qua mô hình, nên không có gì chặn nó dùng từ
     lạ. "See you tomorrow." nghe rất tự nhiên và có ba từ bé chưa từng gặp — câu
     cuối cùng của buổi mà bé không nhại nổi thì buổi học kết thúc bằng thất bại. */
  for (const tt of [
    tinhBuoi({ lichSu: [9, 8, 9].map((d) => ({ vai: 'be', diem: d })), batDau: 0, bayGio: 60000 }),
    tinhBuoi({ lichSu: [{ vai: 'be', diem: 3 }], batDau: 0, bayGio: PHUT_TOI_DA * 60000 }),
  ]) {
    assert.ok(tuLoiKetHopLe(loiKet(tt).en),
      `câu kết "${loiKet(tt).en}" có từ ngoài LOI_LOP_HOC`);
  }
  assert.ok(!tuLoiKetHopLe('See you tomorrow.'), 'phép kiểm phải BẮT được từ lạ');
  assert.ok(!tuLoiKetHopLe(''), 'rỗng không phải là hợp lệ');
});

test('màn hình ĐỌC câu kết, và đọc mỗi thứ tiếng một giọng', () => {
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /docLen\(ket\.en, 'en-GB'/, 'câu tiếng Anh của màn kết phải đọc giọng en-GB');
  assert.match(pn, /docDoan\(tachTheoTieng\(ket\.chu/, 'lời Việt của màn kết phải đi qua phép tách');
  /* Chốt bằng ref chứ không bằng deps: `ket` dựng lại mỗi lần vẽ, mà nhịp 30 giây
     thì cứ nửa phút vẽ một lần — để nó vào deps là cứ 30 giây cô chào tạm biệt. */
  assert.match(pn, /daDocKet\.current/, 'phải có chốt đọc MỘT LẦN, không đọc lại mỗi nhịp');
});

test('nói lại: lượt của bé phải GIỮ câu mẫu đã chấm theo', () => {
  /* Lúc bé bấm "nói lại" thì cô đã nói sang câu khác rồi. Không giữ câu mẫu ngay
     trong lượt thì phép chấm lấy câu MỚI NHẤT — chấm một câu bé không hề định
     nói, và bé càng sửa càng thấp điểm mà không hiểu vì sao. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /mau:\s*cauCoVuaNoi/, 'lượt của bé phải ghi lại câu mẫu');
  assert.match(pn, /chamTot\(chamCau,\s*cu\.mau/, 'nói lại phải chấm theo câu mẫu CỦA CHÍNH lượt ấy');
  assert.doesNotMatch(pn, /chamTot\(chamCau,\s*cauCoVuaNoi,[^)]*\)\s*;?\s*const hon/,
    'nói lại KHÔNG được chấm theo câu mới nhất');
});

test('nói lại KHÔNG gọi cô, chỉ sửa tại chỗ', () => {
  /* Thêm lượt mới thì cuộc trò chuyện phình ra toàn câu hỏng của chính bé, và cô
     trả lời từng lần thử — bé chỉ muốn đọc lại cho tròn tiếng. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  const than = pn.slice(pn.indexOf('const noiLai = useCallback'), pn.indexOf('const noiLaiTuDau'));
  assert.ok(than.length > 100, 'không tìm thấy thân hàm noiLai');
  assert.doesNotMatch(than, /guiLuot\(/, 'nói lại không được gọi cô giáo');
  assert.match(than, /lichSu\.map\(\(x, i\) => \(i !== chiSo/, 'phải sửa ĐÚNG một ô, không thêm lượt');
  assert.match(than, /luuBuoi\(/, 'sửa xong phải lưu lại buổi, nếu không đổi máy là mất');
});

test('nói lại giữ LẦN TỐT NHẤT, và giữ cả câu của lần ấy', () => {
  /* Giữ điểm cao mà hiện chữ của lần mới nhất thì thẻ nói dối: "con nói X, 9 điểm"
     trong khi 9 điểm là của lần trước. Hai thứ phải đi cùng nhau. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /chu:\s*hon \? r\.noiGi : x\.chu/, 'câu phải đi theo lần tốt nhất');
  assert.match(pn, /diem:\s*hon \? kq\.diem : x\.diem/, 'điểm phải là lần tốt nhất');
  assert.doesNotMatch(pn, /Math\.max\(x\.diem/, 'không được lấy max điểm rời khỏi câu');
});

test('có đường NÓI LẠI TỪ ĐẦU — màn kết không phải ngõ cụt', () => {
  /* Xong buổi thì nút micro biến mất (đúng), nhưng không có đường quay lại thì bé
     phải thoát ra vào lại — mà bé 6 tuổi không nghĩ ra chuyện đó. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  const than = pn.slice(pn.indexOf('const noiLaiTuDau'), pn.indexOf('const dsTu'));
  assert.match(than, /maBuoi\.current = /, 'buổi mới phải có mã mới, không ghi đè buổi vừa xong');
  assert.match(than, /daChao\.current = false/, 'phải cho cô chào lại');
  /* `daChao` là ref nên đổi nó KHÔNG làm effect chào chạy lại — thiếu con số này
     trong deps là bấm nút xong màn hình trắng trơn, không ai chào cả. */
  assert.match(than, /datLanBuoi\(/, 'phải có con số trong deps để effect chào chạy lại');
  assert.match(pn, /\[bai, kbXong, guiLuot, lanBuoi\]/, 'effect chào phải ngó tới lanBuoi');
});

test('lặp Y HỆT lượt trước là KHÔNG hợp lệ, dù câu ấy đúng', () => {
  /* Đây chính là cái bác bắt: "nó cứ nói đi nói lại". Nhìn tận mắt trên bản chạy
     thấy hai lượt liền cùng ra "Hi, I'm Bo." — câu đúng ngữ pháp, đúng vốn từ,
     nhưng lặp thì vẫn hỏng. Đúng ngữ pháp KHÔNG đủ để là câu dùng được. */
  const von = vonB01();
  assert.ok(cauHopLe("Hi, I'm Bo.", { von, tenBe: 'Bo' }), 'tự nó thì hợp lệ');
  assert.ok(!cauHopLe("Hi, I'm Bo.", { von, tenBe: 'Bo', cauTruoc: "Hi, I'm Bo." }),
    'nhưng lặp lượt trước thì không');
  assert.ok(!cauHopLe('ball', { von, tenBe: 'Bo', cauTruoc: 'ball.' }),
    'so sau khi bỏ dấu câu — "ball" và "ball." là một');
  assert.ok(cauHopLe('bike', { von, tenBe: 'Bo', cauTruoc: 'ball' }), 'khác thì qua');
});

test('chỗ gọi CÓ truyền câu lượt trước vào phép soi', () => {
  const g = readFileSync(new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(g, /cauTruoc/, 'không truyền thì luật chống lặp thành vô nghĩa');
});

test('câu thay thế KHÔNG được trùng câu lượt trước', () => {
  /* Chặn lặp mà cái dùng để thay lại chính là câu vừa chặn thì bằng không. Đã thấy
     thật trên bản chạy: chặn "Hi, I'm Bo." xong thay bằng đúng "Hi, I'm Bo." */
  const von = vonB01();
  const ls = Array.from({ length: 2 }, () => ({ vai: 'may', en: 'x' }));
  const v = viecTiepTheo({ von, lichSu: ls });
  const thang = cauThayThe(v, 'Bo');
  const khac = cauThayThe(v, 'Bo', thang.en);
  assert.notEqual(khac.en, thang.en, 'phải đổi sang phương án khác');
  assert.ok(cauHopLe(khac.en, { von, tenBe: 'Bo' }), 'và phương án ấy vẫn phải hợp lệ');
});

test('mọi lượt đều có đường lui khác câu trước', () => {
  const von = vonB01();
  for (let n = 0; n < 9; n += 1) {
    const ls = Array.from({ length: n }, () => ({ vai: 'may', en: 'x' }));
    const v = viecTiepTheo({ von, lichSu: ls });
    const a = cauThayThe(v, 'Bo');
    const b = cauThayThe(v, 'Bo', a.en);
    assert.notEqual(b.en, a.en, `lượt ${n} không tìm được câu khác`);
  }
});

/* ═══════════ MỘT BUỔI CÓ MỞ CÓ KẾT ═══════════ */

const be = (...d) => d.map((x) => ({ vai: 'be', diem: x }));

test('đạt liên tiếp đủ số lượt thì cô KHEN rồi dừng', () => {
  const b = tinhBuoi({ lichSu: be(2, 8, 9, 7) });
  assert.equal(b.trangThai, 'xongGioi');
  assert.equal(b.datLien, DAT_LIEN_DE_XONG);
  assert.match(loiKet(b).chu, /3 câu liền/, 'lời khen phải nói THẲNG bé làm được gì');
});

test('chỉ đếm chuỗi ĐUÔI, không đếm cả buổi', () => {
  /* Bé vào phòng lúc còn lóng ngóng rồi khá dần lên là chuyện thường. Lấy cả buổi
     ra tính thì mãi mãi không đạt, mà bé thì đang nói đúng liên tục. */
  assert.equal(tinhBuoi({ lichSu: be(1, 1, 1, 9, 8, 7) }).trangThai, 'xongGioi');
  /* Ngược lại: đạt xong rồi tụt thì KHÔNG được tính là đã xong. */
  assert.equal(tinhBuoi({ lichSu: be(9, 9, 9, 2) }).trangThai, 'dang');
});

test('quá 20 phút thì dừng tử tế', () => {
  const b = tinhBuoi({ lichSu: be(3), batDau: 0, bayGio: (PHUT_TOI_DA + 1) * 60000 });
  assert.equal(b.trangThai, 'hetGio');
  assert.match(loiKet(b).chu, /nghỉ mắt/i);
});

test('MỐC GIỜ BẰNG 0 vẫn là mốc hợp lệ', () => {
  /* Viết `batDau ? … : 0` thì số 0 — một mốc hoàn toàn hợp lệ — bị coi là "chưa
     bấm giờ", và đồng hồ không bao giờ chạy. Cùng họ với lỗi `Date.parse(0)` ra
     năm 2000 đã ghi trong sổ. Phép thử của chính mình bắt được lúc dựng. */
  assert.equal(tinhBuoi({ lichSu: be(3), batDau: 0, bayGio: 25 * 60000 }).trangThai, 'hetGio');
  assert.equal(tinhBuoi({ lichSu: be(3) }).trangThai, 'dang', 'chưa bấm giờ thì đừng đếm');
});

test('chưa tới 20 phút thì chưa dừng', () => {
  assert.equal(tinhBuoi({ lichSu: be(3), batDau: 0, bayGio: (PHUT_TOI_DA - 1) * 60000 }).trangThai, 'dang');
});

test('bé đuối thì HẠ ĐỘ KHÓ, KHÔNG đuổi ra khỏi phòng', () => {
  /* Bé đang đuối mà bị dừng buổi thì thông điệp nhận được là "con dốt quá". Cùng
     tinh thần với luật "thử thật 2 lần" ở dandat.js. */
  const b = tinhBuoi({ lichSu: be(9, 2, 1, 3) });
  assert.equal(b.haDoKho, true);
  assert.equal(b.trangThai, 'dang', 'vẫn ở lại phòng');
  assert.equal(loiKet(b), null, 'không có màn kết');
});

test('hạ độ khó thì chỉ còn luyện TỪ', () => {
  const von = vonB01();
  for (let n = 0; n < 5; n += 1) {
    const ls = Array.from({ length: n }, () => ({ vai: 'may', en: 'x' }));
    assert.equal(viecTiepTheo({ von, lichSu: ls, haDoKho: true }).kieu, 'tu');
  }
});

/* ═══════════ THÔNG TIN CỦA CHÍNH BÉ ═══════════ */

test('hỏi sở thích bằng HÌNH, và chỉ trong vốn từ của bài', () => {
  /* Bé 6 tuổi không gõ được, mà nói tự do thì bộ nhận dạng nghe ra gì cũng được.
     Chọn trong vốn từ thì không có từ lạ nào lọt vào phòng, và KHÔNG có thông tin
     riêng tư nào mới rời khỏi máy — chỉ là một từ trong sách. */
  const von = vonTu({ baiNay: B05, baiCu: [], daDat: false });
  const h = cauHoiSoThich(von);
  assert.ok(h.hoi.length > 5);
  assert.deepEqual(h.chon.map((t) => t.tu), ['chicken', 'chips', 'fish', 'milk']);
  /* Bài chỉ có một từ thì không hỏi — chọn giữa một cái không phải là chọn. */
  assert.equal(cauHoiSoThich(vonTu({ baiNay: bai('B0', ['x'], []), baiCu: [], daDat: false })), null);
});

test('bé chọn rồi thì câu luyện dùng ĐÚNG thứ bé thích', () => {
  const von = vonTu({ baiNay: B05, baiCu: [], daDat: false });
  const ls = [{ vai: 'may', en: 'a' }, { vai: 'may', en: 'b' }];   // lượt "thay"
  assert.equal(viecTiepTheo({ von, lichSu: ls }).theoSoThich, false);
  const v = viecTiepTheo({ von, lichSu: ls, hoSo: { thich: 'fish' } });
  assert.equal(v.tu.tu, 'fish');
  assert.equal(v.theoSoThich, true);
});

test('sở thích ngoài vốn từ thì BỎ QUA, không nhét vào câu', () => {
  const von = vonTu({ baiNay: B05, baiCu: [], daDat: false });
  const ls = [{ vai: 'may', en: 'a' }, { vai: 'may', en: 'b' }];
  const v = viecTiepTheo({ von, lichSu: ls, hoSo: { thich: 'pizza' } });
  assert.notEqual(v.tu.tu, 'pizza');
  assert.ok(moiTuDuocDung(von).includes(v.tu.tu));
});

test('lời dặn KHÔNG hỏi thêm thông tin nhận dạng được bé', () => {
  /* Cố ý không hỏi tuổi, trường, nhà ở đâu. App chỉ dùng thứ nó đã có (tên, lớp)
     và một từ bé vừa chọn trong sách. */
  const s = loiDan({ von: vonB01(), tenBe: 'Bo', hoSo: { thich: 'ball' } });
  for (const cam of [/how old/i, /where do you live/i, /your school/i, /phone/i, /address/i]) {
    assert.doesNotMatch(s, cam, `lời dặn không được hỏi: ${cam}`);
  }
  assert.match(s, /they like "ball"/);
});

test('màn phòng nói CÓ chỗ kết và CÓ chỗ hỏi sở thích', () => {
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /tinhBuoi\(/, 'phải tính trạng thái buổi');
  assert.match(pn, /cauHoiSoThich\(/, 'phải có chỗ hỏi bé thích gì');
  assert.match(pn, /buoi\.trangThai !== 'dang' \? null/, 'buổi kết rồi thì ẩn nút nói');
  assert.match(pn, /haDoKho/, 'phải truyền cờ hạ độ khó xuống');
});

test('buổi vừa kết thì KHÔNG hỏi cô thêm lượt nữa', () => {
  /* Đã thấy thật lúc đi thử: bé nói đúng lượt thứ ba, màn khen hiện lên, và ngay
     dưới lời khen là dòng "Cô giáo máy chưa trả lời được" — vì lượt ấy vẫn gọi
     lên cô. Bé vừa được khen xong lại thấy báo lỗi. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /sauKhiNoi\.trangThai !== 'dang'/, 'phải tính lại trạng thái SAU lượt vừa nói');
  const iChan = pn.indexOf("sauKhiNoi.trangThai !== 'dang'");
  const iGoi = pn.indexOf('guiLuot(sau)');
  assert.ok(iChan > 0 && iChan < iGoi, 'phải chặn TRƯỚC khi gọi cô');
});

test('đồng hồ 20 phút KHÔNG được vô hiệu khi ai đó dọn mã', () => {
  /* Bản đầu viết `Date.now() + nhip * 0` — chạy đúng, nhưng nhân 0 thì ai đọc cũng
     tưởng thừa rồi xoá, mà xoá `nhip` là màn hình không vẽ lại nữa và đồng hồ chết
     im lặng: bé nói mãi quá 20 phút mà không có gì cắt. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /setInterval\(/, 'phải có nhịp vẽ lại, nếu không đồng hồ đứng');
  assert.doesNotMatch(pn, /nhip \* 0/, 'phép nhân 0 là mã chết, dễ bị xoá nhầm');
  assert.match(pn, /phutConLai/, 'còn bao lâu phải HIỆN RA, tính rồi mà không dùng thì tính làm gì');
});

/* ═══════════ KỊCH BẢN VIẾT SẴN CHO TỪNG BÀI ═══════════ */

const KB = JSON.parse(readFileSync(
  new URL('../public/content/ta1/kichban_noi.json', import.meta.url), 'utf8'));

test('mỗi bài có đúng một kịch bản, không thiếu bài nào', () => {
  assert.equal(KB.length, 16);
  assert.equal(new Set(KB.map((k) => k.bai)).size, 16, 'mã bài không được trùng');
});

test('kịch bản nào cũng mở bằng CHÀO và đóng bằng KẾT', () => {
  for (const k of KB) {
    assert.equal(k.buoc[0].loai, 'chao', `${k.bai} không mở bằng lời chào`);
    assert.equal(k.buoc.at(-1).loai, 'ket', `${k.bai} không có chỗ kết`);
  }
});

test('MỌI câu trong kịch bản đều hợp lệ với chính bài của nó', () => {
  /* Đây là phép kiểm đáng giá nhất của cả tệp kịch bản. Sinh sai một câu thì bé
     nghe câu sai suốt buổi, mà nhìn tệp JSON thì không ai thấy. */
  const bai = (id) => JSON.parse(readFileSync(new URL(
    `../public/content/ta1/${id.replace('DL:', 'DL_').replace(/\./g, '_')}.json`,
    import.meta.url), 'utf8'));
  for (const k of KB) {
    const von = vonTu({ baiNay: bai(k.bai), baiCu: [], daDat: false });
    for (const b of k.buoc) {
      if (!b.en) continue;
      const en = dienBuoc(b, { tenBe: 'Bo', thich: k.tu[0] });
      assert.ok(cauHopLe(en, { von, tenBe: 'Bo' }),
        `${k.bai} · bước "${b.loai}" sinh ra câu KHÔNG hợp lệ: "${en}"`);
    }
  }
});

test('bé KHÔNG bấm chọn sở thích thì kịch bản VẪN đi tiếp', () => {
  /* ⚠ CHỖ NÀY TỪNG LÀM CHẾT CẢ TẦNG KỊCH BẢN, ở cả 16 bài, mà không có gì báo.
     Bản cũ: `if (b.loai === 'hoiThich') return !hoSo?.thich` — nghe rất hợp lý.
     Nhưng bé không bắt buộc phải bấm hình, nên điều kiện ấy đúng mãi mãi, và
     `buocTiepTheo` trả `hoiThich` cho MỌI lượt. Mà `dongBuoc('hoiThich')` là chuỗi
     rỗng → suốt buổi mô hình không nhận một dòng dẫn nào.

     Không đỏ, không chậm, cô vẫn nói trôi chảy (vì `cauHopLe` vẫn gác vốn từ) —
     chỉ là nó TỰ NGHĨ, đúng cái việc kịch bản sinh ra để lấy khỏi tay nó. */
  const dat = (n) => Array(n).fill(0).flatMap(() => [{ vai: 'may', en: 'x' }, { vai: 'be', diem: 9 }]);
  for (const k of KB) {
    for (const n of [1, 2, 5]) {
      const b = buocTiepTheo({ kichBan: k, lichSu: dat(n), hoSo: {} });
      assert.ok(b, `${k.bai}: hết bước sau ${n} lượt`);
      assert.notEqual(b.loai, 'hoiThich',
        `${k.bai}: sau ${n} lượt vẫn kẹt ở hoiThich — kịch bản không dẫn được lượt nào`);
      assert.ok(dongBuoc(b, {}).length > 0,
        `${k.bai}: lượt thứ ${n + 1} có lời dặn RỖNG — mô hình tự nghĩ câu`);
    }
  }
});

test('bé nói ĐÚNG HẾT vẫn phải gặp ít nhất MỘT CÂU trước khi buổi kết', () => {
  /* ⚠ Lỗi câm thứ hai của cùng một buổi soát. Bước được chọn theo `soDat` — số lần
     bé nói đúng — mà buổi kết ở `DAT_LIEN_DE_XONG = 3`. Kịch bản thì xếp hết TỪ
     trước rồi mới tới CÂU, mà Unit 6 và Unit 9 đều có bốn từ. Nên bé giỏi luyện
     xong ba từ lẻ rồi được khen "con nói được rồi" — chưa nói một câu nào, đúng
     cái buổi ấy đáng lẽ phải dạy mẫu câu.

     Không lỗi, không cảnh báo, màn kết vẫn chúc mừng vui vẻ. Chỉ trải từng lượt ra
     mới thấy — nên phải có cổng trải đúng như thế. */
  for (const k of KB) {
    let ls = [{ vai: 'be', chu: 'chào' }];
    const gap = [];
    for (let i = 0; i < 8; i += 1) {
      if (tinhBuoi({ lichSu: ls, batDau: 0, bayGio: 1000 }).trangThai !== 'dang') break;
      const b = buocTiepTheo({ kichBan: k, lichSu: ls, hoSo: {} });
      if (!b) break;
      gap.push(b.loai);
      ls = [...ls, { vai: 'may', en: dienBuoc(b, { tenBe: 'An' }) }, { vai: 'be', diem: 9 }];
    }
    assert.ok(gap.some((l) => l === 'mau' || l === 'thay'),
      `${k.bai}: bé nói đúng hết mà chỉ gặp [${gap}] — hết buổi chưa nói câu nào`);
  }
});

test('xen kẽ KHÔNG được đánh rơi bước nào', () => {
  /* Phần luyện quay vòng, nên bước bị rơi khỏi thứ tự là bước bé KHÔNG BAO GIỜ
     gặp — mất hẳn một từ hoặc một câu mà chẳng ai thấy. */
  for (const k of KB) {
    const luyen = k.buoc.filter((b) => ['tu', 'mau', 'thay'].includes(b.loai));
    const sau = xenKe(luyen);
    assert.equal(sau.length, luyen.length, `${k.bai}: số bước đổi sau khi xen kẽ`);
    assert.deepEqual(new Set(sau), new Set(luyen), `${k.bai}: xen kẽ làm rơi hoặc nhân đôi bước`);
  }
  /* Một bên rỗng thì trả nguyên — đừng dựng mảng mới cho khác đi. */
  const chiTu = [{ loai: 'tu' }, { loai: 'tu' }];
  assert.deepEqual(xenKe(chiTu), chiTu);
  assert.deepEqual(xenKe([]), []);
});

test('vẫn hỏi sở thích ĐÚNG MỘT LẦN, ngay sau lời chào', () => {
  /* Sửa chỗ kẹt mà bỏ luôn câu hỏi thì mất phần "nói về chính bé" bác dặn 13-08. */
  for (const k of KB) {
    if (!k.buoc.some((b) => b.loai === 'hoiThich')) continue;
    const sauChao = [{ vai: 'may', en: 'Hello!' }];
    assert.equal(buocTiepTheo({ kichBan: k, lichSu: sauChao, hoSo: {} }).loai, 'hoiThich',
      `${k.bai}: phải hỏi sở thích ngay sau lời chào`);
  }
});

/* ═══════════ BA KỊCH BẢN VIẾT TAY · U6 · U9 · U16 ═══════════ */

const baiCua = (id) => JSON.parse(readFileSync(new URL(
  `../public/content/ta1/${id.replace('DL:', 'DL_').replace(/\./g, '_')}.json`,
  import.meta.url), 'utf8'));

test('ba bài công thức HAI Ô nay có câu để luyện, không còn cụt', () => {
  /* `sinh_kichban_noi.py` bỏ bước "thay" của ba bài này vì công thức hai ô trống
     — bỏ có lý (bản đầu đẻ ra "It's a bell bell."), nhưng hậu quả là cả buổi chỉ
     có một hai câu, lặp mãi. Nay viết tay, lấy câu sẵn của sách. */
  for (const id of ['DL:TA1.B06', 'DL:TA1.B09', 'DL:TA1.B16']) {
    const k = KB.find((x) => x.bai === id);
    assert.ok(k?.tay, `${id} phải đánh dấu tay: true, nếu không lần sinh sau đè mất`);
    const cau = k.buoc.filter((b) => b.loai === 'mau' || b.loai === 'thay');
    assert.ok(cau.length >= 3, `${id} chỉ có ${cau.length} câu — vẫn còn cụt`);
    assert.equal(new Set(cau.map((b) => b.en)).size, cau.length, `${id} có câu trùng`);
  }
});

test('kịch bản tay KHÔNG bịa câu — mọi câu là câu SẴN CỦA SÁCH', () => {
  /* Đây là phép kiểm đáng giá nhất của phần viết tay. Viết tay là chỗ gõ nhầm một
     chữ cũng không ai thấy: câu vẫn trôi chảy, vẫn đúng ngữ pháp, chỉ là bé đang
     học một câu không có trong sách. Nên soi từng câu về đúng `cauSach`. */
  for (const k of KB.filter((x) => x.tay)) {
    const von = vonCuaBai(baiCua(k.bai));
    const chinhChu = new Set(von.cauSach.map((s) => s.toLowerCase()));
    for (const b of k.buoc) {
      if (b.loai !== 'mau' && b.loai !== 'thay') continue;
      assert.ok(chinhChu.has(String(b.en).toLowerCase()),
        `${k.bai}: "${b.en}" KHÔNG phải câu của sách — sách có [${von.cauSach.join(' | ')}]`);
    }
  }
});

test('bước THAY viết tay: điền `dien` vào `khung` phải ra ĐÚNG câu đã ghi', () => {
  /* Hai trường mô tả cùng một thứ thì sớm muộn lệch nhau — sửa `en` mà quên sửa
     `dien` là không có gì báo. Nên bắt chúng khớp bằng phép tính. */
  for (const k of KB.filter((x) => x.tay)) {
    for (const b of k.buoc) {
      if (b.loai !== 'thay') continue;
      assert.ok(Array.isArray(b.dien) && b.dien.length, `${k.bai}: bước thay thiếu \`dien\``);
      let i = 0;
      const dung = b.khung.replace(/\s*\+\s*/g, ' ').replace(/\[[^\]]+\]/g, () => b.dien[i++]);
      assert.equal(i, b.dien.length, `${k.bai}: số ô trống lệch số giá trị điền`);
      assert.equal(dung, b.en, `${k.bai}: điền ${JSON.stringify(b.dien)} ra "${dung}", không khớp "${b.en}"`);
    }
  }
});

test('chỗ khó viết tay phải ĐI THEO lời dặn tới mô hình', () => {
  /* ⚠ Suýt thành công cốc. `buoc.vi` chỉ là ĐƯỜNG LUI trong goiPhongNoi.js
     (`tra.vi || buoc.vi`), mà mô hình thì lượt nào cũng có lời Việt — nên đường
     lui không bao giờ tới lượt, và công viết tay nằm im trong tệp JSON.

     Không gì báo cả: lời Việt của mô hình vẫn trôi chảy, chỉ là nói chung chung
     và bỏ qua đúng chỗ bé hay sai ("màu đứng TRƯỚC đồ vật"). */
  const b = { loai: 'mau', en: "It's a red pen.", vi: 'Màu đứng TRƯỚC đồ vật nhé.' };
  const d = dongBuoc(b, {});
  assert.ok(d.includes('Màu đứng TRƯỚC đồ vật nhé.'),
    'chỗ khó của bước phải nằm trong lời dặn gửi lên, không chỉ nằm trong tệp');
  assert.match(d, /do not drop the point/i, 'và phải dặn rõ là không được bỏ qua');
  /* Bước không có lời dẫn thì đừng thêm dòng rỗng vào lời dặn. */
  assert.ok(!dongBuoc({ loai: 'tu', en: 'ball' }, {}).includes('teaching point'));
});

test('lời tiếng Việt viết tay phải chỉ ra chỗ khó RIÊNG của bài', () => {
  /* Viết tay mà vẫn dùng câu chung "Con nghe rồi nói lại cả câu này nhé" thì công
     viết tay chẳng để làm gì — đó đúng là thứ bản sinh tự động đã cho sẵn. */
  const chung = 'Con nghe rồi nói lại cả câu này nhé.';
  for (const k of KB.filter((x) => x.tay)) {
    for (const b of k.buoc) {
      if (b.loai !== 'mau' && b.loai !== 'thay') continue;
      assert.notEqual(b.vi, chung, `${k.bai}: "${b.en}" vẫn dùng lời chung chung`);
      assert.ok(b.vi && b.vi.length > 15, `${k.bai}: "${b.en}" thiếu lời dẫn`);
    }
  }
});

test('câu sẵn của sách bị LỌC THEO TỪ — "blue" không lọt', () => {
  /* Unit 6 có `"It's a blue pen."` trong canonicalExamples mà cả 16 bài KHÔNG bài
     nào dạy "blue" — chỗ hở của sách. Cứ lấy vào là bé gặp một màu chưa ai dạy. */
  const von = vonCuaBai(baiCua('DL:TA1.B06'));
  assert.ok(von.cauSach.includes("It's a red bell."), 'câu đúng phải được nhận');
  assert.ok(!von.cauSach.some((s) => /blue/i.test(s)),
    'câu có từ ngoài vốn của bài phải bị loại, dù nó nằm trong sách');
  assert.ok(!cauHopLe("It's a blue pen.", { von: { loi: von, on: [] } }),
    'và phép soi câu cũng phải từ chối');
});

test('SỐ ĐẾM chỉ được nhận ở bài mà công thức ĐÒI một con số', () => {
  /* Số đếm là vốn nền sách mặc định bé có (không bài nào dạy), nên phải nhận —
     nếu không Unit 16 chỉ còn đúng một câu trả lời "six" cho cả buổi.
     Nhưng nới cho số KHÔNG được thành cái cớ nới cho từ khác: bài nào không có ô
     `[Number]` thì số vẫn là từ lạ như mọi từ lạ khác. */
  const b16 = vonCuaBai(baiCua('DL:TA1.B16'));
  for (const n of ['one', 'two', 'three']) {
    assert.ok(b16.cauSach.some((s) => s.toLowerCase().includes(n)), `thiếu câu có "${n}"`);
  }
  const b12 = vonCuaBai(baiCua('DL:TA1.B12'));   // không có ô [Number]
  assert.ok(!/\[Number\]/i.test(JSON.stringify(b12.cau)), 'B12 quả thật không có ô số');
  assert.ok(!cauHopLe('Look at the two lemons.', { von: { loi: b12, on: [] } }),
    'bài không đòi số thì số vẫn là từ lạ');
  assert.equal(SO_DEM.length, 10, 'một tới mười — đủ cho lớp 1, đừng nới thêm');
});

test('ô của TÊN không bao giờ bị điền đồ vật', () => {
  /* "Bye, book." — mô hình đã sinh ra thật khi được thả tự do. Kịch bản không được
     phép mắc lại lỗi ấy, và đây là chỗ soi. */
  for (const k of KB) {
    for (const b of k.buoc) {
      if (b.loai !== 'thay' || b.o !== 'ten') continue;
      assert.match(b.en, /\{ten\}/, `${k.bai}: ô tên phải điền {ten}, không phải từ vựng`);
    }
  }
});

test('bước tiến theo số lượt ĐẠT, chưa đạt thì đứng yên để thử lại', () => {
  /* Tiến theo số lượt đã NÓI thì bé nói sai cũng bị đẩy sang bài mới — đúng cái
     làm bé hụt hơi rồi bỏ. */
  const k = KB[0];
  const hoSo = { tenBe: 'Bo', thich: 'ball' };
  const sai = [{ vai: 'may', en: 'x' }, { vai: 'be', diem: 2 },
               { vai: 'may', en: 'x' }, { vai: 'be', diem: 1 }];
  const a = buocTiepTheo({ kichBan: k, lichSu: sai, hoSo });
  const b = buocTiepTheo({ kichBan: k, lichSu: [...sai, { vai: 'may', en: 'x' }, { vai: 'be', diem: 1 }], hoSo });
  assert.deepEqual(a, b, 'chưa đạt thì phải đứng yên ở bước ấy');
});

test('bước MỘT LẦN làm xong trước, không bị nhảy cóc', () => {
  /* Bản đầu trộn bước một-lần vào cùng phép đếm với bước luyện, nên bước "hỏi sở
     thích" bị nhảy cóc — bé chưa kịp chọn gì thì đã sang luyện từ, và cả phần
     "nói về chính bé" thành vô dụng. */
  const k = KB[0];
  assert.equal(buocTiepTheo({ kichBan: k, lichSu: [], hoSo: {} }).loai, 'chao');

  /* ⚠ MỐC NÀY ĐÃ ĐỔI 14-08, và đổi có chủ ý. Bản cũ đặt mốc SAU khi bé đã nói một
     câu có điểm, vì hồi ấy `hoiThich` không có hạn — hỏi tới lúc nào bé chịu bấm
     mới thôi. Đó chính là chỗ làm chết cả tầng kịch bản: bé không bấm thì nó kẹt
     mãi ở đấy. Nay `hoiThich` chỉ được đúng một lượt, ngay sau lời chào, nên mốc
     thử phải là lúc bé CHƯA nói câu nào có điểm. */
  const vuaChao = [{ vai: 'be', chu: 'Chào cô' }, { vai: 'may', en: 'Hello!' }];
  assert.equal(buocTiepTheo({ kichBan: k, lichSu: vuaChao, hoSo: {} }).loai, 'hoiThich');
  assert.equal(
    buocTiepTheo({ kichBan: k, lichSu: vuaChao, hoSo: { thich: 'ball' } }).loai, 'tu',
    'chọn rồi thì thôi hỏi lại');
});

test('đuối thì lùi hẳn về bước TỪ', () => {
  const k = KB[0];
  const ls = [{ vai: 'may', en: 'x' }, { vai: 'be', diem: 9 }];
  for (let n = 0; n < 6; n += 1) {
    const b = buocTiepTheo({ kichBan: k, lichSu: [...ls, ...Array(n).fill({ vai: 'be', diem: 9 })],
                             hoSo: { thich: 'ball' }, haDoKho: true });
    assert.equal(b.loai, 'tu');
  }
});

test('hết kịch bản thì QUAY VÒNG, không đứng lại', () => {
  /* Buổi kết là việc của `tinhBuoi` (đạt đủ, hoặc hết giờ), không phải của việc
     hết bước. Hết bước mà dừng thì bé đang hăng lại bị đuổi ra. */
  const k = KB[0];
  const dat = (n) => Array.from({ length: n }, () => ({ vai: 'be', diem: 9 }));
  for (const n of [8, 12, 30]) {
    assert.ok(buocTiepTheo({ kichBan: k, lichSu: [{ vai: 'may', en: 'x' }, ...dat(n)],
                             hoSo: { thich: 'ball' } }), `hết bước ở lượt ${n}`);
  }
});

test('lời dặn khi CÓ kịch bản: ép chép nguyên văn, không cho diễn giải', () => {
  const b = { loai: 'mau', en: "Hi, I'm Bill." };
  const s = dongBuoc(b, { tenBe: 'Bo' });
  assert.match(s, /MUST be exactly: "Hi, I'm Bill\."/);
  assert.match(s, /Do not rephrase/i);
  assert.match(s, /Vietnamese line/i, 'việc còn lại của mô hình là lời tiếng Việt');
});

test('chỗ gọi ÉP câu về đúng kịch bản khi mô hình chệch', () => {
  const g = readFileSync(new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(g, /buocTiepTheo\(/, 'phải hỏi kịch bản');
  assert.match(g, /tra\.en !== dung/, 'chệch kịch bản thì phải ép về đúng câu');
});

test('ĐỢI kịch bản rồi mới chào', () => {
  /* Kịch bản nạp không đồng bộ. Chào ngay thì lượt ĐẦU TIÊN — lượt định ra cả buổi
     — rơi về lối cũ, cô nói thẳng "ball" thay vì "Hello!". Nhìn màn hình mới thấy,
     cổng cũ không bắt được vì cả hai lối đều "chạy đúng". */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /!kbXong\) return;/, 'chưa nạp xong kịch bản thì chưa chào');
  assert.match(pn, /\.finally\(\(\) => \{ if \(song\) datKbXong\(true\)/,
    'nạp HỎNG cũng phải đặt cờ, nếu không bé đứng chờ một tệp không bao giờ về');
});

/* ═══════════ TÊN THẬT CỦA BÉ ═══════════ */

test('vỏ app TRUYỀN hồ sơ con xuống môn', () => {
  /* Bác bắt 13-08: "bạn đang fix tên của học sinh là Bo nhỉ?" — đúng, nhưng không
     phải vì ghim cứng. `ManTiengAnh` có đọc `hoSo?.displayName`, chỉ là `App.jsx`
     dựng màn của môn mà KHÔNG truyền `hoSo` xuống. Nên `displayName` luôn rỗng, và
     cái tên dự phòng hoá ra là tên DUY NHẤT: mọi bé đều bị gọi là "Bo".

     Không cổng nào bắt được vì cả hai phía đều "đúng" khi nhìn riêng — chỉ hỏng ở
     chỗ nối. Đã thử tận tay: đổi tên thành "Nguyễn Minh An", màn hồ sơ hiện đúng,
     mà cô vẫn chào "Bo". */
  const app = readFileSync(new URL('../src/App.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  const than = app.slice(app.indexOf('const Man = mon.Man'));
  assert.match(than, /hoSo=\{profile\}/, 'màn của môn phải nhận hồ sơ con');

  const man = readFileSync(new URL('../src/mon/tienganh/components/ManTiengAnh.jsx', import.meta.url), 'utf8');
  assert.match(man, /hoSo\?\.displayName/, 'và môn phải đọc tên thật từ đó');
});

test('tên dự phòng lấy TỪ SÁCH, không bịa tên lạ', () => {
  /* Bé chưa khai tên mà bị gọi bằng một cái tên bịa sẵn thì đó là tên người khác.
     Lấy tên trong chính câu ví dụ của bài thì ít nhất bé đang nhại đúng nhân vật. */
  const kb = JSON.parse(readFileSync(
    new URL('../public/content/ta1/kichban_noi.json', import.meta.url), 'utf8'));
  for (const k of kb) {
    for (const b of k.buoc) {
      if (b.o !== 'ten') continue;
      assert.ok(b.mac_dinh, `${k.bai}: ô tên thiếu giá trị dự phòng`);
      assert.notEqual(b.mac_dinh, 'Bo', `${k.bai}: vẫn bịa tên "Bo"`);
      /* Phải là cái tên CHÍNH SÁCH dùng — tìm thấy trong một câu ví dụ của bài. */
      const coTrongSach = k.buoc.some((x) => x.loai === 'mau' && x.en?.includes(b.mac_dinh));
      assert.ok(coTrongSach, `${k.bai}: "${b.mac_dinh}" không có trong câu ví dụ nào của bài`);
    }
  }
});

test('có tên thật thì DÙNG tên thật, không dùng dự phòng', () => {
  const b = { loai: 'thay', o: 'ten', en: "Hi, I'm {ten}.", mac_dinh: 'Bill' };
  assert.equal(dienBuoc(b, { tenBe: 'An' }), "Hi, I'm An.");
  assert.equal(dienBuoc(b, { tenBe: '' }), "Hi, I'm Bill.", 'chưa khai tên thì dùng tên trong sách');
});
