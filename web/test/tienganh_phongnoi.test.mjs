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
  viecTiepTheo, cauHopLe, soiCau, cauThayThe, loaiOTrong, tachTheoTieng,
  tinhBuoi, loiKet, tuLoiKetHopLe, cauHoiSoThich, PHUT_TOI_DA, DAT_LIEN_DE_XONG,
  loiVietHopLe, XUNG_HO_CAM,
  laTuSo, dienDuocVaoO, dienHetO,
  buocTiepTheo, dienBuoc, dongBuoc, xenKe, buocSua, luotBeCuoi, luotLuyen, SUA_TOI_DA,
  LY_DO_BAC, loiNhacSua, loiNhacSuaViet, SUA_CO_TOI_DA, NHAC_SUA_TOI_DA_CHU,
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

/**
 * Ô TRỐNG CHƯA ĐIỀN — lỗ hổng tìm ra 26-08 bằng `tools/do_an_toan_noi_dung.mjs`.
 *
 * Ba bài (TA4.B09 · TA4.B18 · TA5.B01 · TA5.B11) có công thức HAI ô. Phép điền chỉ
 * thay ô ĐẦU — cả trong `soiCau` lẫn ở chỗ mô hình bắt chước — nên ô sau còn nguyên
 * `[Month B]`. Mà `gonCau` bóc sạch dấu ngoặc trước khi so, nên chuỗi ấy khớp với
 * chính nó và ĐƯỢC NHẬN: cô giáo máy đọc cho bé nghe "It's in month B."
 *
 * Chốt mới bác thẳng mọi câu còn dấu ngoặc vuông. An toàn tuyệt đối vì câu tiếng
 * Anh cho trẻ sáu tuổi không bao giờ có dấu ngoặc — và không cần biết ô ấy đáng lẽ
 * nhận gì, thứ mà chính bài học cũng không khai.
 */
test('ô trống CHƯA ĐIỀN bị bác — dù chuỗi khớp sau khi bóc dấu ngoặc', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const soi = (s, cauTruoc = '') => soiCau(s, { von, tenBe: 'Bo', cauTruoc });

  assert.equal(soi("Hi, I'm [Name].").bac, 'oTrong', 'ô tên còn nguyên dấu ngoặc');
  assert.equal(soi("It's in [Month B].").bac, 'oTrong', 'ô thứ hai của công thức hai ô');
  assert.equal(soi('I like [Noun].').bac, 'oTrong');
  /* Bác vì Ô TRỐNG, không phải vì ngoài vốn — hai lý do khác loại nhau, gộp lại là
     mất đúng thông tin cần để lần ra chỗ hỏng. */
  assert.notEqual(soi("Hi, I'm [Name].").bac, 'ngoaiVon');
  /* Và chốt mới KHÔNG được đụng tới câu hợp lệ. */
  assert.equal(soi("Hi, I'm Bo.").ok, true, 'câu đã điền đủ vẫn qua');
});

test('soiCau nói ra ĐƯỜNG công nhận — điều kiện của phép thử đảo chiều (KB3)', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const soi = (s) => soiCau(s, { von, tenBe: 'Bo' });
  assert.equal(soi('ball').duong, 'tu');
  assert.equal(soi('Good job!').duong, 'nghiThuc');
  assert.equal(soi("Hi, I'm Bo.").duong, 'congThuc');
  /* Tắt một đường thì câu đi qua đường ấy phải rơi — nếu không thì đường ấy là mã
     chết và mọi con số "đóng góp của từng đường" đều vô nghĩa. */
  assert.equal(soiCau('Good job!', { von, tenBe: 'Bo', tat: new Set(['nghiThuc']) }).ok, false);
  assert.equal(soiCau('ball', { von, tenBe: 'Bo', tat: new Set(['tu']) }).ok, false);
  /* Còn `cauHopLe` thì vẫn là vỏ boolean cũ, không đổi một li. */
  assert.equal(cauHopLe('ball', { von, tenBe: 'Bo' }), true);
  assert.equal(cauHopLe('automobile', { von, tenBe: 'Bo' }), false);
});

/**
 * DẠNG BIẾN ĐỔI CỦA MỘT TỪ RỜI — vá 26-08.
 *
 * Đường `congThuc` nhận `so_nhieu · so_it · dang_ing · dang_qk` từ lâu, đường `tu`
 * thì không. Nên "playing the violin" bị bác trong khi lớp 5 unit 4 dạy hẳn mục từ
 * `play the violin` với `dang_ing` đúng bằng chuỗi ấy. Đo lúc nối phụ đạo: 12/129
 * ca có nút gốc rễ khác nút mắc bị bác SẠCH câu chỉ vì một phương án nhiễu dùng
 * dạng -ing. Hai đường của cùng một hàng rào mà lệch luật là chỗ không ai đi tìm.
 */
test('dạng biến đổi của từ ĐÃ HỌC được nhận ở đường `tu`', () => {
  const b = {
    id: 'X1',
    title: 'Unit X',
    knowledgeCore: {
      vocabulary: [{ tu: 'play the violin', nghia: 'chơi vi-ô-lông', dang_ing: 'playing the violin' },
        { tu: 'read books', nghia: 'đọc sách', dang_ing: 'reading books', dang_qk: 'read books' }],
      mauCauDs: [], canonicalExamples: [],
    },
    practice: { pools: {} },
  };
  const von = vonTu({ baiNay: b, baiCu: [], daDat: false });
  const soi = (s) => soiCau(s, { von, tenBe: 'Bo' });
  assert.equal(soi('play the violin').ok, true, 'dạng gốc');
  assert.equal(soi('playing the violin').duong, 'tu', 'dạng -ing của CHÍNH mục từ ấy');
  assert.equal(soi('reading books').duong, 'tu');
  /* ⚠ VÀ KHÔNG ĐƯỢC NỚI THÊM GÌ. Dạng biến đổi lấy từ mục từ vựng bé đã học; từ
     nào bài không dạy thì vẫn không có đường vào, kể cả khi nó rất giống. */
  assert.equal(soi('playing the piano').ok, false, 'từ bài KHÔNG dạy');
  assert.equal(soi('writing books').ok, false);
});

/* ═══════════ LỜI NHẮC SỬA ═══════════ */

/**
 * Bác một câu rồi im là bỏ mất cô giáo; nên phải NÓI RA chỗ sai. Bốn lý do bác của
 * `soiCau` là bốn lỗi khác loại nhau, nên bốn lời nhắc khác nhau — nhắc chung
 * chung ("câu này không dùng được") thì mô hình sửa đoán, và thường sửa sang lỗi
 * khác. Bản nháp lời nhắc ở §9 mục B1–B5 của bản rà 09-10.
 */
test('loiNhacSua: mỗi lý do bác một lời nhắc RIÊNG, đúng chỗ sai', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const ctx = { von, cauTruoc: "Hi, I'm Bo.", tenBe: 'Lan' };

  assert.match(loiNhacSua('rong', ctx), /no English sentence/);
  assert.match(loiNhacSua('lap', ctx), /repeated your previous sentence/);
  assert.match(loiNhacSua('lap', ctx), /Hi, I'm Bo\./, 'phải trích đúng câu đã lặp');
  assert.match(loiNhacSua('oTrong', ctx), /unfilled slot/);
  /* Chữ LẠ phải được gọi tên. "Nói chung là sai" thì mô hình đi đổi chữ khác. */
  const nv = loiNhacSua('ngoaiVon', { ...ctx, en: 'I want chips.' });
  assert.match(nv, /NOT allowed/);
  assert.match(nv, /chips/);
  /* ⚠ Và phải ghi "for example": bảng vốn đầy đủ nằm trong lời dặn, ở đây chỉ còn
     chỗ cho vài từ. Liệt kê cụt mà viết "chỉ dùng mấy từ này" là tự tay thu vốn
     của bé xuống còn đúng số từ vừa lọt trần 300 ký tự. */
  assert.match(nv, /for example/);
});

/**
 * ⚠ `ngoaiVon` KHÔNG LUÔN LUÔN LÀ "CÓ CHỮ LẠ". Đó là lý do bác CUỐI của `soiCau` —
 * câu không đi qua được đường công nhận nào. Một câu chỉ gồm từ bé đã học vẫn rơi
 * vào đấy nếu nó chẳng phải mẫu câu nào của bài. Nhắc nó "có chữ lạ" lúc ấy là
 * nhắc sai chỗ, và mô hình sẽ đi đổi từ — thứ vốn đã đúng.
 */
test('loiNhacSua: câu toàn từ ĐÃ HỌC mà sai mẫu thì nhắc về MẪU CÂU', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const en = 'Book ball bike.';
  assert.equal(soiCau(en, { von, tenBe: 'Lan' }).bac, 'ngoaiVon');
  const s = loiNhacSua('ngoaiVon', { von, en, tenBe: 'Lan' });
  assert.match(s, /not one of the taught sentence patterns/);
  assert.ok(!/NOT allowed/.test(s), 'không được vu cho nó dùng chữ lạ');
});

test('loiNhacSua: TIẾNG ANH THUẦN, dưới trần, và không lý do nào bị bỏ sót', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  /* Lời nhắc là lời nói VỚI MÔ HÌNH, không phải lời cho bé đọc. Trộn hai thứ tiếng
     vào một lượt thì mô hình hay trả lời lẫn theo. */
  const coDauViet = /[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/i;
  for (const bac of [...LY_DO_BAC, 'mot-ly-do-chua-co']) {
    const s = loiNhacSua(bac, {
      von, cauTruoc: 'x'.repeat(400), en: 'I want chips and automobiles.', tenBe: 'Lan',
    });
    assert.ok(s.trim(), `lý do "${bac}" không có lời nhắc nào`);
    assert.ok(s.length <= NHAC_SUA_TOI_DA_CHU,
      `lý do "${bac}": lời nhắc ${s.length} ký tự, quá trần ${NHAC_SUA_TOI_DA_CHU}`);
    assert.ok(!coDauViet.test(s), `lý do "${bac}": lời nhắc có dấu tiếng Việt`);
    /* Mô hình phải biết trả về khuôn nào — thiếu dòng này nó trả chữ trần, và
       `docTraLoi` lại phải đi đoán dòng nào là tiếng Anh. */
    assert.match(s, /JSON/);
  }
});

test('loiNhacSuaViet: giữ câu tiếng Anh, chỉ viết lại một dòng', () => {
  const von = vonTu({ baiNay: B01, baiCu: [], daDat: false });
  const kq = loiVietHopLe('Bạn nói lại đi.', { von });
  assert.equal(kq.ok, false);
  const s = loiNhacSuaViet(kq, { en: "Hi, I'm Lan.", von });
  assert.match(s, /Keep the English sentence exactly/);
  assert.match(s, /Hi, I'm Lan\./);
  assert.match(s, /Rewrite ONLY the Vietnamese line/);
  /* Lỗi hay gặp nhất là cô gọi bé bằng "bạn" — nói điều ấy bằng tiếng Anh thì mô
     hình không biết phải thay bằng chữ nào. Nên đưa thẳng hai chữ vào lời nhắc. */
  assert.match(s, /"cô"/);
  assert.match(s, /"con"/);
  assert.ok(s.length <= NHAC_SUA_TOI_DA_CHU, `${s.length} ký tự, quá trần`);

  /* Lý do dài bất thường vẫn phải lọt trần — mô hình có thể nhắc lại cả một câu. */
  const dai = loiNhacSuaViet({ ok: false, vi: 'x'.repeat(500) }, { en: 'y'.repeat(500), von });
  assert.ok(dai.length <= NHAC_SUA_TOI_DA_CHU, `${dai.length} ký tự, quá trần`);
});

test('SUA_CO_TOI_DA là một con số nhỏ — mỗi vòng là một lần bé ngồi đợi', () => {
  assert.ok(Number.isInteger(SUA_CO_TOI_DA) && SUA_CO_TOI_DA >= 1 && SUA_CO_TOI_DA <= 3,
    `SUA_CO_TOI_DA = ${SUA_CO_TOI_DA} — nới quá thì bé đợi cô cả chục giây`);
});

test('ô trống biết mình thuộc loại nào', () => {
  assert.equal(loaiOTrong("Hi, I'm + [Name]."), 'ten');
  assert.equal(loaiOTrong('I like + [Noun].'), 'tu');
  assert.equal(loaiOTrong('không có ô trống'), null);
  /* ── BỐN LOẠI Ô NỮA, vá 09-10-2026 ── */
  assert.equal(loaiOTrong("He's + [Number]."), 'so');
  assert.equal(loaiOTrong('How old is she? - She\'s + [Age].'), 'so');
  assert.equal(loaiOTrong("He's + [Verb-ing]."), 'ing');
  assert.equal(loaiOTrong("They're + [V-ing]."), 'ing');
  assert.equal(loaiOTrong('I + [past verb] + yesterday.'), 'qk');
  assert.equal(loaiOTrong('How many + [Noun-plural]?'), 'nhieu');
  assert.equal(loaiOTrong('The + [Plural Noun] + are here.'), 'nhieu');
});

/**
 * ══ Ô TRỐNG NHẬN BỪA MỌI TỪ CỦA BÀI — vá 09-10-2026 ══
 *
 * Bản cũ chỉ biết hai loại ô: tên người, và "ô nhận từ bất kỳ". Đo thật qua Groq,
 * cô giáo máy nói ra những câu này và cả hai đi qua `soiCau` SẠCH:
 *
 *   "Do you live in this sixteen? - Yes, I do."    ô `[place]` nhận một CON SỐ
 *   "He's truck."                                   ô `[Number]` nhận một danh từ
 *
 * Đúng họ với "Bye, bike." bác bắt 14-08 — lần ấy chỉ vá riêng ô tên, và mọi ô còn
 * lại hở y nguyên cho tới nay.
 */
test('ô kiểu SỐ chỉ nhận con số, và ô thường thì TRỪ con số ra', () => {
  const b = bai('X', ['truck', 'bus'], [["He's six.", "He's + [Number]."]]);
  b.knowledgeCore.vocabulary.push({ tu: 'six', nghia: 'sáu (6)' });
  const von = vonTu({ baiNay: b });
  assert.equal(soiCau("He's six.", { von, tenBe: 'Bo' }).ok, true, 'câu của chính sách');
  assert.equal(soiCau("He's truck.", { von, tenBe: 'Bo' }).ok, false,
    'ô [Number] nhận một danh từ — đúng câu cô giáo máy đã nói ra thật');

  /* Chiều ngược: con số không được điền vào ô thường. */
  const c = bai('Y', ['tower'], [['Do you live in this tower?', 'Do you live in this + [place]?']]);
  c.knowledgeCore.vocabulary.push({ tu: 'sixteen', nghia: 'mười sáu (16)' });
  const v2 = vonTu({ baiNay: c });
  assert.equal(soiCau('Do you live in this tower?', { von: v2, tenBe: 'Bo' }).ok, true);
  assert.equal(soiCau('Do you live in this sixteen?', { von: v2, tenBe: 'Bo' }).ok, false,
    'con số điền vào ô [place] — đúng câu đã đo được trên bản thật');
});

test('CON SỐ nhận ra từ lời chú của sách, không từ một danh sách gõ tay', () => {
  /* Lời chú của sách luôn kèm chữ số: "mười một (11)" · "hai mươi (20)". Gõ tay một
     danh sách thì quyển sau thêm số mới là nó lọt, mà không gì kêu. */
  assert.equal(laTuSo({ tu: 'eleven', nghia: 'mười một (11)' }), true);
  assert.equal(laTuSo({ tu: 'twenty', nghia: 'hai mươi (20)' }), true);
  assert.equal(laTuSo({ tu: 'two', nghia: 'hai' }), true, 'SO_DEM vẫn là lưới thứ hai');
  assert.equal(laTuSo({ tu: 'brother', nghia: 'anh, em trai' }), false);
  assert.equal(laTuSo({ tu: 'sure', nghia: 'chắc chắn' }), false);
});

test('ô DẠNG BIẾN ĐỔI nhận cả mục từ ĐÃ Ở dạng ấy sẵn', () => {
  /* ⚠ Lớp 4 unit 20 dạy hẳn mục từ `putting up a tent` với `dang_ing: null` — vì
     chính đầu mục đã là dạng -ing. Chỉ nhận `dang_ing` thì SÁU câu của chính sách
     bị bác. Đã đo bằng cách so bản mới với bản cũ trên 711 câu sách. */
  const t = [{ tu: 'putting up a tent', nghia: 'dựng lều', dang_ing: null },
             { tu: 'read', nghia: 'đọc', dang_ing: 'reading', dang_qk: 'read' }];
  assert.ok(dienDuocVaoO('ing', t).includes('putting up a tent'));
  assert.ok(dienDuocVaoO('ing', t).includes('reading'));
  assert.ok(!dienDuocVaoO('ing', t).includes('read'), 'dạng gốc KHÔNG điền vào ô -ing');
});

/**
 * ══ ĐƯỜNG LUI CUỐI TỰ SINH RA CÂU HỎNG — vá 09-10-2026 ══
 *
 * `cauThayThe` chú thích là "LUÔN ĐÚNG, vì nó ghép từ chính dữ liệu bài". Đo thật
 * trên cả bốn quyển, 846 lượt: 80 câu KHÔNG hợp lệ, hỏng theo kiểu tệ nhất — còn
 * nguyên dấu ngoặc, và bé nghe cô đọc to cả dấu ngoặc:
 *
 *   "It's a bell [Noun]."        "How many clocks? - [Number]."
 *
 * Vì phép điền cũ thay ĐÚNG MỘT ô. `soiCau` bác nó (luật `oTrong`), nhưng
 * `hoiCoGiao` lấy câu của `cauThayThe` rồi TRẢ THẲNG — nó tin lời chú trên.
 *
 * Cổng cũ `câu thay thế LUÔN hợp lệ` chỉ thử B01 — một bài MỘT ô — nên chưa bao giờ
 * đi qua chỗ hỏng. Nay thử trên DỮ LIỆU THẬT của cả bốn quyển.
 */
test('câu thay thế LUÔN hợp lệ — trên dữ liệu THẬT của cả bốn quyển', () => {
  let thu = 0;
  for (const ma of QUYEN) {
    for (const k of kbCua(ma)) {
      const b = baiTrong(ma, k.bai);
      const von = vonTu({ baiNay: b, baiCu: [], daDat: false });
      for (let n = 0; n < 9; n += 1) {
        const v = viecTiepTheo({ von, lichSu: Array.from({ length: n }, () => ({ vai: 'may', en: 'x' })) });
        if (!v) continue;
        const t = cauThayThe(v, 'Bo');
        thu += 1;
        assert.ok(t && t.en && t.vi, `${ma}/${b.id} lượt ${n}: không dựng được câu thay thế`);
        assert.ok(!/[[\]]/.test(t.en),
          `${ma}/${b.id} lượt ${n}: câu thay thế còn dấu ngoặc — bé sẽ nghe đọc to: "${t.en}"`);
        assert.ok(cauHopLe(t.en, { von, tenBe: 'Bo' }),
          `${ma}/${b.id} lượt ${n}: câu thay thế "${t.en}" lại KHÔNG hợp lệ`);
      }
    }
  }
  assert.ok(thu > 500, `chỉ thử được ${thu} lượt — có phải vòng lặp hỏng?`);
});

/**
 * ⚠ CHỖ HỎNG THỨ BA của cùng một lỗi, và là chỗ chỉ lộ ra LÚC CHẠY.
 *
 * Bé thích "bus" thì ô `[Number]` của mẫu tuổi nhận "bus" → "He's bus." Nhìn tệp
 * kịch bản thì sạch, vì `{thich}` chỉ được điền lúc chạy, theo sở thích TỪNG BÉ.
 * (Hai chỗ kia: `soiCau` và bộ sinh kịch bản `tools/sinh_kichban_noi.py`.)
 */
test('thứ bé THÍCH chỉ điền vào ô thường, không điền vào ô có kiểu', () => {
  const b = { loai: 'thay', khung: "He's + [Number].", en: "He's {thich}.", mac_dinh: 'sixteen' };
  assert.equal(dienBuoc(b, { thich: 'bus' }), "He's sixteen.",
    'ô kiểu SỐ phải dùng mac_dinh, không dùng thứ bé thích');
  const c = { loai: 'thay', khung: 'I like + [Noun].', en: 'I like {thich}.', mac_dinh: 'milk' };
  assert.equal(dienBuoc(c, { thich: 'fish' }), 'I like fish.',
    'ô thường thì VẪN phải nói về thứ bé thích — đừng vá rộng quá');
  assert.equal(dienBuoc(c, {}), 'I like milk.');
});

/**
 * Cổng này soi DỮ LIỆU ĐÃ PHÁT HÀNH, không soi mã: bốn câu dưới đây từng nằm thật
 * trong `kichban_noi.json` và bé nghe chúng suốt buổi.
 *   ta1/B11  "She's bus."  "He's bus."     ta2/B12  "The grape are on the table."
 *   ta2/B14  "He's/She's brother."
 * Bộ sinh Python đã vá; cổng này giữ cho chúng đừng bò lại vào sau một lần sinh lại.
 */
test('kịch bản đã phát hành KHÔNG còn câu nào sai kiểu ô', () => {
  const xau = [];
  for (const k of MOI_KB) {
    if (k.dang === 'tranh') continue;
    const von = vonCua(k);
    for (const b of k.buoc) {
      if (!b.en) continue;
      /* Thử CẢ HAI đường điền: mặc định, và theo sở thích của bé. */
      for (const thich of ['', ...(k.tu || []).slice(0, 4)]) {
        const en = dienBuoc(b, { tenBe: 'Bo', thich });
        if (!cauHopLe(en, { von, tenBe: 'Bo' })) xau.push(`${k.ma}/${k.bai} [${b.loai}] "${en}"`);
      }
    }
  }
  assert.deepEqual(xau, [], `câu sai trong kịch bản đã phát hành:\n  ${xau.join('\n  ')}`);
});

test('ĐIỀN HẾT ô, hoặc chịu — không bao giờ để sót một ô', () => {
  const t = [{ tu: 'bell', nghia: 'cái chuông' }];
  assert.equal(dienHetO('It\'s a + [Noun].', t), "It's a bell.");
  /* Khung hai ô mà chỉ có một từ thì phải CHỊU, chứ không điền cùng chữ vào cả hai:
     "It's a bell bell." · "Can you village a village?" — 62 câu như thế. */
  assert.equal(dienHetO('How many + [Noun]? - [Number].', t), null,
    'không có số để điền ô thứ hai thì phải trả null');
});

/**
 * ⚠ KHÔNG PHẢI CHỖ NÀO CŨNG VÁ ĐƯỢC, và nói thẳng ra đây.
 *
 * `"Who's this? - It's my sure."` VẪN đi qua, vì ta3 unit 11 có dạy từ `sure`, và
 * mục từ vựng KHÔNG có trường từ loại (740 mục: tu · ma · ipa · nghia · so_nhieu ·
 * dang_ing · dang_qk · am · amO). Đoán "bố là người, chắc chắn thì không" từ lời
 * chú tiếng Việt là dựng một cổng ghim vào CHÍNH TẢ của lời chú — đúng cái bẫy đã
 * dính bốn lần ở kho này.
 *
 * Việc còn lại là việc của DỮ LIỆU: thêm trường từ loại vào mục từ vựng. Phép canh
 * này ĐÒI nó vẫn đi qua, để ngày nào có trường ấy thì cổng đỏ lên và nhắc người sửa
 * quay lại đây — chứ không nằm im như một chỗ đã quên.
 */
test('chỗ CHƯA vá được: ô kiểu loại từ mà dữ liệu không nói được', () => {
  const b = bai('Z', ['brother', 'sure'], [["It's my brother.", "It's my + [Family member]."]]);
  const von = vonTu({ baiNay: b });
  assert.equal(soiCau("It's my brother.", { von, tenBe: 'Bo' }).ok, true);
  assert.equal(soiCau("It's my sure.", { von, tenBe: 'Bo' }).ok, true,
    'nếu câu này ĐÃ bị bác thì dữ liệu đã có từ loại — quay lại loaiOTrong và khai thêm');
  assert.ok(!('tuLoai' in (b.knowledgeCore.vocabulary[0] || {})),
    'mục từ vựng nay CÓ trường từ loại — đã đến lúc vá ô kiểu loại từ');
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
  /* ⚠ Tên biến đổi 19-08: không còn là `cauCoVuaNoi` (câu CÔ vừa nói) mà là câu bé
     CẦN nói. Bác bắt: cô hỏi "What can you see?" thì bé phải ĐÁP, không phải nhại
     câu hỏi — chấm theo câu cô nói là khen bé vì nhại đúng. Điều phép này canh thì
     không đổi: lượt của bé phải GIỮ LẠI câu đã chấm theo. */
  assert.match(pn, /mau: kq\?\.mau \|\| luotCoCuoi\?\.en/, 'lượt của bé phải ghi lại câu mẫu');
  assert.match(pn, /canNoiGi/, 'phải chấm theo câu bé CẦN nói, không theo câu cô vừa nói');

  /* ⚠ VÀ CHỖ NỐI PHẢI GỬI `can` ĐI THẬT. `canNoi` tính đúng mà `goiPhongNoi` không
     gọi nó thì màn hình nhận `can` rỗng, rơi về `[luotCoCuoi.en]` — tức là quay
     đúng về lối cũ: chấm bé theo câu CÔ vừa nói. Tính rồi không gửi thì y như
     không tính, và đó là cái bẫy đã sập một lần với `thieu` của bộ chấm. */
  const gp = readFileSync(new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(gp, /can: canNoi\(buoc, kichBan\)/, 'lượt của cô phải mang theo `can`');
  assert.match(gp, /loiDanTranh\(\{/, 'bài tả tranh phải dùng lời dặn riêng');
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
  /* `kq.nghe` là đúng phương án nhận dạng được chấm điểm ấy (`chamTot`). */
  assert.match(pn, /chu:\s*hon \? \(kq\.nghe \?\? r\.noiGi\) : x\.chu/, 'câu phải đi theo lần tốt nhất');
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
  /* ⚠ SOI TÍNH CHẤT, ĐỪNG GHIM CẢ MẢNG DEPS. Bản đầu đòi đúng chuỗi
     `[bai, kbXong, guiLuot, lanBuoi]`; việc V7 thêm hai phụ thuộc nữa vào chính
     effect ấy và cổng đỏ dù tính chất — "effect chào phải ngó tới `lanBuoi`" —
     không đổi. Nên tìm mảng deps của effect chào rồi đòi `lanBuoi` CÓ TRONG đó. */
  const iChao = pn.indexOf('daChao.current = true');
  assert.notEqual(iChao, -1);
  const deps = pn.slice(iChao).match(/\}, \[([^\]]*)\]\);/)?.[1] || '';
  assert.match(deps, /\blanBuoi\b/, 'effect chào phải ngó tới lanBuoi');

  /* ⚠ VÀ PHẢI XOÁ KẾ HOẠCH CŨ (việc V7). Kế hoạch cũ đã xong hết, mà `xongKeHoach`
     nay là một ĐÍCH của buổi — nên lượt đầu của buổi MỚI thấy "xong" và màn kết
     hiện ra trước khi bé nói câu nào. Đúng chỗ phép canh này vừa bắt được. */
  assert.match(than, /datKeHoachState\(null\)/,
    'nói lại từ đầu mà không xoá kế hoạch cũ — buổi mới kết ngay khi vừa mở');
  assert.match(than, /daDocKeHoach\.current = false/,
    'không đọc lại lời giới thiệu kế hoạch cho buổi mới');
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
  const iGoi = pn.indexOf('guiLuot(sau');
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

/**
 * ⚠ SOI CẢ BA QUYỂN, KHÔNG CHỈ QUYỂN 1.
 *
 * Bản cũ chỉ đọc `ta1/kichban_noi.json`. Lớp 2 và lớp 3 có kịch bản riêng từ lâu
 * mà chưa một phép kiểm nào đụng tới — mà chính hai quyển ấy mới là chỗ hỏng: máy
 * con gọi `napKichBanNoi()` không tham số nên chúng KHÔNG BAO GIỜ được nạp. Cổng
 * soi một quyển thì "0 lỗi" chỉ có nghĩa là quyển ấy sạch, không có nghĩa là môn
 * này sạch — cùng họ với chuyện glob rỗng báo 0 lỗi đã ghi trong sổ.
 */
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];
/* ⚠ ĐẾM TỪ SỔ ĐĂNG KÝ, đừng gõ tay. Bảng gõ tay `{ta1:16, ta2:16, ta3:21}` thiếu
   `ta4` nên phép so ra "21 !== undefined" — nghe như thiếu kịch bản, thật ra là
   thiếu MỘT DÒNG TRONG CỔNG. Cùng họ "ghim cứng tên quyển". */
const _dk = JSON.parse(readFileSync(
  new URL('../public/content/chuong_trinh.json', import.meta.url), 'utf8'));
const SO_BAI = Object.fromEntries(Object.values(_dk.chuongTrinh)
  .filter((c) => c.mon === 'tienganh').map((c) => [c.ma, c.soBai]));
const kbCua = (ma) => JSON.parse(readFileSync(
  new URL(`../public/content/${ma}/kichban_noi.json`, import.meta.url), 'utf8'));
const baiTrong = (ma, id) => JSON.parse(readFileSync(new URL(
  `../public/content/${ma}/${id.replace('DL:', 'DL_').replace(/\./g, '_')}.json`,
  import.meta.url), 'utf8'));

const KB = kbCua('ta1');
/** Mọi kịch bản của mọi quyển, mỗi cái mang theo mã quyển của nó. */
const MOI_KB = QUYEN.flatMap((ma) => kbCua(ma).map((k) => ({ ...k, ma })));
const vonCua = (k) => vonTu({ baiNay: baiTrong(k.ma, k.bai), baiCu: [], daDat: false });

/** Bước DẠY CÂU — thứ bác đòi phải là phần chính của buổi. */
const BUOC_CAU = new Set(['mau', 'noiCa', 'hoiBe', 'doiVai', 'thay',
  // Ba nhịp của bài TẢ TRANH — cũng là dạy câu, chỉ khác cách.
  'taTranh', 'goiY', 'caDoan']);

test('mỗi bài có đúng một kịch bản, không thiếu bài nào', () => {
  for (const ma of QUYEN) {
    const kb = kbCua(ma);
    assert.equal(kb.length, SO_BAI[ma], `${ma}: thiếu hoặc thừa kịch bản`);
    assert.equal(new Set(kb.map((k) => k.bai)).size, SO_BAI[ma], `${ma}: mã bài trùng`);
  }
});

test('kịch bản nào cũng mở bằng CHÀO và đóng bằng KẾT', () => {
  for (const k of MOI_KB) {
    /* ⚠ Kịch bản TẢ TRANH cố ý KHÔNG chào. Bác chốt 19-08: "Phần Nói bạn hãy xoá
       tất cả các thứ đi. Chỉ để một bức tranh sau đó yêu cầu học sinh mô tả bức
       tranh. […] Đừng làm những thứ khác ngoài mấy thứ đó ra." Để lại lời chào là
       để lại đúng thứ bác bảo xoá — và nó ăn mất lượt đầu, lượt định ra cả buổi. */
    if (k.dang === 'tranh') {
      assert.equal(k.buoc[0].loai, 'taTranh',
        `${k.ma}/${k.bai}: bài tả tranh phải mở bằng lời MỜI TẢ, không phải gì khác`);
      assert.equal(k.buoc.at(-1).loai, 'ket', `${k.ma}/${k.bai} không có chỗ kết`);
      assert.ok(k.buoc.some((b) => b.loai === 'caDoan'),
        `${k.ma}/${k.bai}: thiếu bước XÂU CHUỖI — cả buổi là để tới đó`);
      assert.ok(!k.buoc.some((b) => ['chao', 'tu', 'mau', 'noiCa'].includes(b.loai)),
        `${k.ma}/${k.bai}: còn sót bước của kịch bản cũ`);
      continue;
    }
    assert.equal(k.buoc[0].loai, 'chao', `${k.ma}/${k.bai} không mở bằng lời chào`);
    assert.equal(k.buoc.at(-1).loai, 'ket', `${k.ma}/${k.bai} không có chỗ kết`);
  }
});

test('MỌI câu trong kịch bản đều hợp lệ với chính bài của nó', () => {
  /* Đây là phép kiểm đáng giá nhất của cả tệp kịch bản. Sinh sai một câu thì bé
     nghe câu sai suốt buổi, mà nhìn tệp JSON thì không ai thấy. */
  for (const k of MOI_KB) {
    /* ⚠ KỊCH BẢN TẢ TRANH SOI BẰNG LUẬT KHÁC, và luật ấy CHẶT HƠN.
       `cauHopLe` hỏi "câu này có nằm trong vốn của UNIT này không" — đúng cho kịch
       bản thường, sai cho bài tả tranh: bức tranh cố ý dùng cả vốn tích luỹ từ lớp
       1 (bác chốt 19-08: "không giới hạn trong chính bài học đó khiến nội dung
       nhàm chán"). Nới `cauHopLe` ra cho nó thì mất luôn chốt cho 20 kịch bản kia.
       Nên hỏi thẳng: mọi câu của kịch bản tranh phải nằm trong BẢN MÔ TẢ bức tranh
       ấy, hoặc là tên một vật CÓ trong tranh. Không câu nào được ở ngoài. */
    if (k.dang === 'tranh') {
      /* Được phép nói: từng câu của BẢN MÔ TẢ, cả đoạn ghép lại (bước `caDoan`),
         và những CÂU HỎI GỢI Ý đã khai sẵn ở bản khai tranh. Không gì khác. */
      const cho = new Set([...(k.moTaTranh || []), ...(k.tu || []),
        (k.moTaTranh || []).join(' ')]);
      for (const b of k.buoc) if (b.loai === 'goiY' || b.loai === 'taTranh') cho.add(b.en);
      for (const b of k.buoc) {
        if (!b.en) continue;
        assert.ok(cho.has(b.en),
          `${k.ma}/${k.bai} · bước "${b.loai}" nói “${b.en}” — không có trong bản mô tả tranh`);
      }
      continue;
    }
    const von = vonCua(k);
    for (const b of k.buoc) {
      if (!b.en) continue;
      const en = dienBuoc(b, { tenBe: 'Bo', thich: k.tu[0] });
      assert.ok(cauHopLe(en, { von, tenBe: 'Bo' }),
        `${k.ma}/${k.bai} · bước "${b.loai}" sinh ra câu KHÔNG hợp lệ: "${en}"`);
    }
  }
});

test('phần luyện của MỌI bài là dạy CÂU, không phải đọc từ rời', () => {
  /* ⚠ ĐÂY LÀ CỔNG CHO ĐÚNG CHỖ BÁC CHỈ RA 18-08: "dạy học sinh nói được các câu
     giao tiếp hoàn chỉnh chứ không như máy như giờ".

     Bản cũ: unit 5 lớp 3 có 15 bước thì 8 bước là MỘT CHỮ TRẦN. Đếm được, nhưng
     không cổng nào đếm — nên nó nằm đó từ ngày dựng phòng. Nay bước `tu` chỉ còn
     là đường lui lúc bé đuối, và phép kiểm này giữ cho nó đừng bò lại vào vòng
     luyện thường. */
  for (const k of MOI_KB) {
    const cau = k.buoc.filter((b) => BUOC_CAU.has(b.loai));
    assert.ok(cau.length >= 2,
      `${k.ma}/${k.bai}: chỉ ${cau.length} bước dạy câu — buổi này vẫn là đọc từ rời`);
    /* Và từ rời KHÔNG được nằm trong vòng luyện: `buocTiepTheo` khi bé nói đúng
       không bao giờ được trả về một bước `tu`. */
    const dat = (n) => Array.from({ length: n }, () => ({ vai: 'be', diem: 9 }));
    for (const n of [0, 1, 2, 3, 5, 9]) {
      const b = buocTiepTheo({ kichBan: k, lichSu: [{ vai: 'may', en: 'x' }, ...dat(n)],
                               hoSo: { thich: k.tu[0] } });
      assert.notEqual(b?.loai, 'tu',
        `${k.ma}/${k.bai}: lượt thứ ${n + 1} vẫn là một chữ trần "${b?.en}"`);
    }
  }
});

test('bé phải gặp một câu NGAY TRONG BA LƯỢT ĐẦU', () => {
  /* Buổi kết ở `DAT_LIEN_DE_XONG = 3`. Bé giỏi nói đúng ba lượt liền là XONG — nên
     ba lượt ấy phải chứa việc đáng học nhất. Đếm tới lượt thứ tư là đếm một chỗ bé
     giỏi không bao giờ tới. */
  for (const k of MOI_KB) {
    let ls = [{ vai: 'be', chu: 'chào' }];
    const gap = [];
    for (let i = 0; i < 4; i += 1) {
      const b = buocTiepTheo({ kichBan: k, lichSu: ls, hoSo: { thich: k.tu[0] } });
      if (!b) break;
      gap.push(b.loai);
      ls = [...ls, { vai: 'may', en: dienBuoc(b, { tenBe: 'An' }) }, { vai: 'be', diem: 9 }];
    }
    assert.ok(gap.slice(0, 3).some((l) => BUOC_CAU.has(l)),
      `${k.ma}/${k.bai}: ba lượt đầu là [${gap.slice(0, 3)}] — chưa câu nào`);
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
  for (const k of MOI_KB) {
    for (const n of [1, 2, 5]) {
      const b = buocTiepTheo({ kichBan: k, lichSu: dat(n), hoSo: {} });
      assert.ok(b, `${k.ma}/${k.bai}: hết bước sau ${n} lượt`);
      assert.notEqual(b.loai, 'hoiThich',
        `${k.ma}/${k.bai}: sau ${n} lượt vẫn kẹt ở hoiThich — kịch bản không dẫn được lượt nào`);
      assert.ok(dongBuoc(b, {}).length > 0,
        `${k.ma}/${k.bai}: lượt thứ ${n + 1} có lời dặn RỖNG — mô hình tự nghĩ câu`);
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
  for (const k of MOI_KB) {
    let ls = [{ vai: 'be', chu: 'chào' }];
    const gap = [];
    for (let i = 0; i < 8; i += 1) {
      if (tinhBuoi({ lichSu: ls, batDau: 0, bayGio: 1000 }).trangThai !== 'dang') break;
      const b = buocTiepTheo({ kichBan: k, lichSu: ls, hoSo: {} });
      if (!b) break;
      gap.push(b.loai);
      ls = [...ls, { vai: 'may', en: dienBuoc(b, { tenBe: 'An' }) }, { vai: 'be', diem: 9 }];
    }
    assert.ok(gap.some((l) => BUOC_CAU.has(l)),
      `${k.ma}/${k.bai}: bé nói đúng hết mà chỉ gặp [${gap}] — hết buổi chưa nói câu nào`);
  }
});

test('xen kẽ KHÔNG được đánh rơi bước nào', () => {
  /* Phần luyện quay vòng, nên bước bị rơi khỏi thứ tự là bước bé KHÔNG BAO GIỜ
     gặp — mất hẳn một từ hoặc một câu mà chẳng ai thấy. */
  for (const k of MOI_KB) {
    const luyen = k.buoc.filter((b) => BUOC_CAU.has(b.loai));
    const sau = xenKe(luyen);
    assert.equal(sau.length, luyen.length, `${k.ma}/${k.bai}: số bước đổi sau khi xen kẽ`);
    assert.deepEqual(new Set(sau), new Set(luyen),
      `${k.ma}/${k.bai}: xen kẽ làm rơi hoặc nhân đôi bước`);
  }
  /* Một bên rỗng thì trả nguyên — đừng dựng mảng mới cho khác đi. */
  const chiTu = [{ loai: 'tu' }, { loai: 'tu' }];
  assert.deepEqual(xenKe(chiTu), chiTu);
  assert.deepEqual(xenKe([]), []);
});

test('vẫn hỏi sở thích ĐÚNG MỘT LẦN, ngay sau lời chào', () => {
  /* Sửa chỗ kẹt mà bỏ luôn câu hỏi thì mất phần "nói về chính bé" bác dặn 13-08. */
  for (const k of MOI_KB) {
    if (!k.buoc.some((b) => b.loai === 'hoiThich')) continue;
    const sauChao = [{ vai: 'may', en: 'Hello!' }];
    assert.equal(buocTiepTheo({ kichBan: k, lichSu: sauChao, hoSo: {} }).loai, 'hoiThich',
      `${k.ma}/${k.bai}: phải hỏi sở thích ngay sau lời chào`);
  }
});

/* ═══════════ SOI LỜI TIẾNG VIỆT CỦA CÔ ═══════════ */

const vonB09 = () => vonTu({
  baiNay: JSON.parse(readFileSync(
    new URL('../public/content/ta1/DL_TA1_B09.json', import.meta.url), 'utf8')),
  baiCu: [], daDat: false,
});

test('cô phải gọi bé bằng "con" — bắt được cả HAI câu hỏng thật', () => {
  /* Hai câu dưới đây LẤY NGUYÊN từ bản chạy 14-08, không phải bịa ra để thử. */
  const von = vonB09();
  const a = loiVietHopLe('Bạn vừa nói câu hỏi này rất tốt!', { von });
  assert.ok(!a.ok, 'gọi bé bằng "bạn" phải bị bắt');
  assert.match(a.vi, /bạn/, 'phải nói rõ hỏng ở chữ nào');
  for (const x of ['em', 'tớ', 'cậu']) {
    assert.ok(!loiVietHopLe(`Nào ${x} nói lại đi.`, { von }).ok, `"${x}" phải bị bắt`);
  }
  assert.ok(loiVietHopLe('Con nói lại nhé, cô nghe đây.', { von }).ok, 'lời đúng phải qua');
});

test('"bạn" làm DANH TỪ thì không bị chặn nhầm', () => {
  /* Cổng bắt được thật: sách chú `girl` là "bạn gái", và bản đầu của phép soi
     chặn luôn lời giải nghĩa của chính sách. "bạn" ở đó là danh từ, không phải
     đại từ gọi bé — hai thứ khác hẳn nhau. */
  const von = vonB09();
  assert.ok(loiVietHopLe('Con nói lại từ này nhé — nghĩa là bạn gái.', { von }).ok);
  assert.ok(loiVietHopLe('Con kể cho bạn ấy nghe nhé.', { von }).ok);
  /* Nhưng nới cho danh từ KHÔNG được thành cửa cho đại từ lọt qua. */
  assert.ok(!loiVietHopLe('Bạn nói lại đi.', { von }).ok);
  assert.ok(!loiVietHopLe('Rất tốt, bạn giỏi lắm!', { von }).ok);
});

test('"mình" nghĩa là chúng ta — KHÔNG được cấm nhầm', () => {
  /* Cấm cả "mình" thì chính lời chào của 16 kịch bản bị chặn, và cô mất luôn cách
     nói ấm nhất: "hôm nay MÌNH tập nói nhé". */
  assert.ok(loiVietHopLe('Chào con! Hôm nay mình tập nói nhé.', { von: vonB09() }).ok);
});

test('cô KHÔNG được nhắc lại một từ bé chưa từng nói', () => {
  /* Trên bản chạy: cô nhắc `"How many washes can you see?"` — câu bé chưa nói và
     không có trong sách. Hỏng kép: bé tưởng mình đã nói thế, VÀ mẩu ấy không nằm
     trong vốn nên `tachTheoTieng` không tách ra → bị đọc bằng GIỌNG VIỆT. */
  const von = vonB09();
  const x = loiVietHopLe('Con vừa nói "How many washes can you see?" đúng không?', { von });
  assert.ok(!x.ok, 'câu bịa phải bị bắt');
  assert.match(x.vi, /washes/, 'phải chỉ ra đúng mẩu hỏng');

  assert.ok(loiVietHopLe('Con nói lại từ "clocks" nhé.', { von }).ok, 'từ CÓ trong bài thì qua');
  assert.ok(loiVietHopLe('Con nói "How many clocks?" nhé.', { von }).ok, 'câu CÓ trong bài thì qua');

  /* MẨU của một câu cũng phải qua — trỏ vào chỗ mở đầu là cách dạy hay nhất, và
     chính lời viết tay của Unit 9 làm thế. Cổng đã bắt được bản soi quá chặt. */
  assert.ok(loiVietHopLe('Mở đầu bằng "How many" nhé.', { von }).ok, 'mẩu của câu phải qua');

  /* Nhưng nới cho mẩu KHÔNG được thành cửa cho chữ lạ. "wash" có trong Unit 16,
     "washes" là một chữ KHÁC — đúng chỗ mô hình đã trượt trên bản chạy. */
  const v16 = vonTu({
    baiNay: JSON.parse(readFileSync(
      new URL('../public/content/ta1/DL_TA1_B16.json', import.meta.url), 'utf8')),
    baiCu: [], daDat: false,
  });
  assert.ok(loiVietHopLe('Con nói lại "wash" nhé.', { von: v16 }).ok, '"wash" có trong bài');
  const w = loiVietHopLe('Con vừa nói "How many washes can you see?" nhỉ.', { von: v16 });
  assert.ok(!w.ok, '"washes" phải bị bắt dù mọi chữ khác đều có trong bài');
  assert.match(w.vi, /washes/, 'phải chỉ đúng chữ hỏng');
});

test('mẩu trong ngoặc có DẤU tiếng Việt thì không bị soi như tiếng Anh', () => {
  /* Chính lời viết tay của Unit 6 có `Mình nói "đỏ" rồi mới nói "bút"` — soi nhầm
     mẩu ấy là chặn luôn lời dẫn tốt nhất của bài. */
  assert.ok(loiVietHopLe('Mình nói "đỏ" rồi mới nói "bút chì" nhé.', { von: vonB09() }).ok);
});

test('câu ĐÍCH của lượt này luôn được nhắc lại', () => {
  /* Cô phải chỉ vào câu bé sắp nói. Không cho nhắc thì lời dẫn hoá vô nghĩa. */
  const von = vonB09();
  assert.ok(loiVietHopLe('Con nói "I can see six." nhé.',
    { von, cauDich: 'I can see six.' }).ok);
  assert.ok(!loiVietHopLe('Con nói "I can see six." nhé.', { von }).ok,
    'không phải câu đích, cũng không có trong bài thì phải bị bắt');
});

test('lời dặn CÓ dặn hai luật ấy, chứ không chỉ soi ngầm', () => {
  /* Chỉ soi mà không dặn thì lượt nào cũng phải lui về lời viết sẵn — mất hết
     phần cô phản ứng với cái bé vừa nói. Dặn và soi phải đi cùng nhau. */
  const s = loiDan({ von: vonB09(), tenBe: 'An', lop: 1 });
  assert.match(s, /call yourself "cô", call the child "con"/i);
  assert.match(s, /quote it EXACTLY/i);
  assert.ok(!/bạn nhỏ/.test(loiDan({ von: vonB09() })),
    'lời dặn không được TỰ GIEO chữ "bạn" bằng giá trị mặc định');
});

test('ĐƯỜNG LUI phải sạch — mọi lời viết sẵn tự nó qua được phép soi', () => {
  /* Lui về một lời cũng gọi bé bằng "bạn" thì chốt soi thành vô dụng: chặn được
     câu hỏng của mô hình rồi thay bằng một câu hỏng khác. Cả 16 kịch bản, kể cả
     ba bản viết tay. */
  assert.ok(XUNG_HO_CAM.includes('bạn'), 'danh sách cấm phải có "bạn"');
  for (const k of MOI_KB) {
    const von = vonCua(k);
    for (const b of k.buoc) {
      if (!b.vi) continue;
      const kq = loiVietHopLe(b.vi, { von, cauDich: b.en || '' });
      assert.ok(kq.ok, `${k.ma}/${k.bai} · "${b.en}": lời viết sẵn tự nó hỏng — ${kq.vi}`);
    }
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
  for (const k of MOI_KB) {
    for (const b of k.buoc) {
      if (b.loai !== 'thay' || b.o !== 'ten') continue;
      assert.match(b.en, /\{ten\}/, `${k.ma}/${k.bai}: ô tên phải điền {ten}, không phải từ vựng`);
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
  /* ⚠ MỐC NÀY ĐỔI LẦN NỮA 18-08. Bản cũ đòi bước kế tiếp là `tu` — đúng với thiết
     kế cũ, nơi vòng luyện mở đầu bằng từ rời. Nay vòng luyện toàn bước CÂU và `tu`
     lùi về làm đường lui, nên đòi `tu` ở đây là đòi đúng cái vừa bỏ đi. */
  const sau = buocTiepTheo({ kichBan: k, lichSu: vuaChao, hoSo: { thich: 'ball' } });
  assert.notEqual(sau.loai, 'hoiThich', 'chọn rồi thì thôi hỏi lại');
  assert.ok(BUOC_CAU.has(sau.loai),
    `chọn xong phải vào luyện CÂU, không phải "${sau.loai}"`);
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
  for (const k of MOI_KB) {
    for (const b of k.buoc) {
      if (b.o !== 'ten') continue;
      assert.ok(b.mac_dinh, `${k.ma}/${k.bai}: ô tên thiếu giá trị dự phòng`);
      assert.notEqual(b.mac_dinh, 'Bo', `${k.ma}/${k.bai}: vẫn bịa tên "Bo"`);
      /* Phải là cái tên CHÍNH SÁCH dùng — tìm thấy trong một câu ví dụ của bài. */
      const coTrongSach = k.buoc.some((x) => x.loai === 'mau' && x.en?.includes(b.mac_dinh));
      assert.ok(coTrongSach,
        `${k.ma}/${k.bai}: "${b.mac_dinh}" không có trong câu ví dụ nào của bài`);
    }
  }
});

test('có tên thật thì DÙNG tên thật, không dùng dự phòng', () => {
  const b = { loai: 'thay', o: 'ten', en: "Hi, I'm {ten}.", mac_dinh: 'Bill' };
  assert.equal(dienBuoc(b, { tenBe: 'An' }), "Hi, I'm An.");
  assert.equal(dienBuoc(b, { tenBe: '' }), "Hi, I'm Bill.", 'chưa khai tên thì dùng tên trong sách');
});

/* ═══════════ DẠY NÓI VÀ SỬA LỖI — bác chốt 18-08-2026 ═══════════ */

test('bé nói trượt thì lượt sau là lượt SỬA, không phải bài mới', () => {
  /* ⚠ ĐÂY LÀ CHỖ BÁC CHỈ RA: "Cần dạy học sinh nói rồi hướng dẫn học sinh sửa."
     Trước 18-08 không có bước nào làm việc này. Bé được 3 điểm thì `soDat` không
     tăng, kịch bản đứng yên, và cô nhắc lại Y NGUYÊN câu cũ với Y NGUYÊN lời dặn
     — bé nghe lại lần hai chứ không được chỉ sai ở đâu. Không lỗi, không cảnh
     báo; nhìn màn hình thì thấy cô vẫn nói năng tử tế. */
  const k = MOI_KB[0];
  const truot = [{ vai: 'may', en: "Hi, I'm Bill." },
                 { vai: 'be', chu: 'hi im bi', diem: 3, mau: "Hi, I'm Bill.", thieu: ['bill'] }];
  const b = buocTiepTheo({ kichBan: k, lichSu: truot, hoSo: { thich: k.tu[0] } });
  assert.equal(b.loai, 'sua', 'trượt mà không có lượt sửa thì chỗ hỏng nằm lại đó');
  assert.equal(b.en, "Hi, I'm Bill.", 'phải sửa ĐÚNG câu bé đang cố nói');
  assert.match(b.vi, /bill/i, 'lời viết sẵn phải chỉ ra chữ bé bỏ sót');

  /* Đạt rồi thì thôi sửa — sửa một câu bé đã nói được là làm bé mất tự tin. */
  const dat = [{ vai: 'may', en: "Hi, I'm Bill." },
               { vai: 'be', chu: "hi i'm bill", diem: 9, mau: "Hi, I'm Bill." }];
  assert.notEqual(
    buocTiepTheo({ kichBan: k, lichSu: dat, hoSo: { thich: k.tu[0] } })?.loai, 'sua');
});

test('bé nói lung tung KHÔNG theo câu nào thì đừng sửa', () => {
  /* Không có `mau` nghĩa là bé tự nói chứ không nhại — chấm theo một câu bé không
     định nói đã là sai, sửa theo câu ấy còn sai hơn. */
  assert.equal(buocSua([{ vai: 'be', chu: 'con thích cái này', diem: 2 }]), null);
  assert.equal(buocSua([]), null);
  assert.equal(luotBeCuoi([{ vai: 'be', chu: 'chào cô' }]), null,
    'lượt chưa chấm thì không tính');
});

test('lời dặn MANG THEO cái bé vừa nói, điểm, và chữ bỏ sót', () => {
  /* `goiGui` cố ý cắt sạch điểm khi gửi lịch sử (chỉ vai + chữ). Nên nếu không đi
     đường `dongBuoc` thì mô hình KHÔNG có cách nào biết bé được 9 hay 2 điểm — và
     lời khen lượt nào cũng như lượt nào. Đúng chỗ bác gọi là "như máy". */
  const luot = { vai: 'be', chu: 'it cooking', diem: 4,
                 mau: "It's cooking.", thieu: [], thieuChucNang: ["it's"] };
  const d = dongBuoc({ loai: 'sua', en: "It's cooking.", vi: 'x' }, {}, luot);
  assert.match(d, /it cooking/, 'phải chở CÂU BÉ VỪA NÓI lên');
  assert.match(d, /4\/10/, 'phải chở ĐIỂM lên');
  assert.match(d, /it's/i, 'phải chở chữ bỏ sót lên');
  assert.match(d, /CORRECTION turn/i, 'và nói rõ đây là lượt sửa');
  assert.match(d, /Do not move on/i, 'sửa xong mới đi tiếp, không bỏ qua');

  /* Chưa có lượt nào của bé thì đừng dựng khối rỗng. */
  assert.doesNotMatch(dongBuoc({ loai: 'mau', en: 'Hello!' }, {}, null),
    /WHAT THE CHILD JUST DID/);
});

test('mỗi loại bước nói rõ VIỆC CỦA BÉ — cùng một câu, ngược hẳn vai', () => {
  /* "What's your hobby?" xuất hiện ở hai bước khác hẳn nhau: `hoiBe` (cô hỏi thật,
     bé đáp) và `doiVai` (bé hỏi, cô đáp). Không nói ra thì mô hình đoán, và đoán
     sai thì bé được dặn làm nhầm việc — mà câu tiếng Anh thì vẫn đúng nên không
     gì kêu. */
  const en = "What's your hobby?";
  const a = dongBuoc({ loai: 'hoiBe', en, dapMau: "It's cooking." }, {});
  const b = dongBuoc({ loai: 'doiVai', en }, {});
  assert.match(a, /ASKING her a real question/i);
  assert.match(a, /Do NOT answer it for her/i);
  assert.match(b, /roles swap/i);
  assert.match(b, /SHE asks/i);
  assert.notEqual(a, b, 'cùng một câu mà hai bước phải dặn khác nhau');
  assert.match(dongBuoc({ loai: 'noiCa', en: "It's cooking." }, {}), /WHOLE sentence/i);
});

test('lời dặn nói rõ CÔ PHẢI DẠY GÌ, không chỉ liệt kê điều cấm', () => {
  /* Bản cũ mở bằng "a warm, patient English tutor" rồi đi thẳng vào mười điều cấm.
     Mô hình đọc xong biết mình KHÔNG được nói gì, không biết mình PHẢI làm gì —
     nên nó chọn việc an toàn nhất: đọc từng từ cho bé nhại. */
  const s = loiDan({ von: vonB09(), tenBe: 'An', lop: 1 });
  assert.match(s, /WHOLE SENTENCES/);
  assert.match(s, /TEACH/); assert.match(s, /SPEAK/); assert.match(s, /FIX/);
  assert.match(s, /Do not reuse your own Vietnamese wording/i);

  /* ── VIỆC SỬA LỖI: nay nằm Ở HAI CHỖ, không còn ở khối chung ── (việc V2)
     Luật 8b cũ ("CORRECT HER" · "One fix per turn") đã rời khối chung sang
     `loidan_nhan.js`, vì nó chỉ nói về MỘT tình huống: bé vừa nói sai. Để chung thì
     lượt nào mô hình cũng đọc nó và phải tự đoán có đang áp dụng hay không.

     ⚠ Chuyển chỗ thì phép canh phải chuyển theo, chứ KHÔNG được nới. Đòi hỏi của
     bác không đổi một chữ ("dạy học sinh nói rồi hướng dẫn học sinh sửa"), nên dưới
     đây soi đủ CẢ HAI đường tới được lượt sửa — rộng hơn bản cũ, vì bản cũ chỉ soi
     khối chung và chưa bao giờ soi nhánh kịch bản. */
  for (const nhan of ['thieuTu', 'saiThuTu', 'nhamTu']) {
    const d = loiDan({ von: vonB09(), tenBe: 'An', lop: 1, nhan,
                       chiTiet: { beNoi: 'im bo', dich: 'Hi.', thieu: ['hi'], nham: 'duck' } });
    assert.match(d, /\bONLY\b|\bONE\b|\bone\b/,
      `nhãn ${nhan}: không dặn "mỗi lượt sửa MỘT thứ" — sáu tuổi không ôm nổi ba lỗi`);
    assert.match(d, /Do not move on|try the target|say the target/i,
      `nhãn ${nhan}: không dặn phải Ở LẠI câu ấy — bỏ qua chỗ sai là đúng cái bác bắt`);
  }
  /* Nhánh CÓ kịch bản không ghép dòng nhãn (xem `NHAN_TRONG_KICH_BAN`); ở đấy việc
     sửa do bước `sua` của `dongBuoc` gánh. */
  const bSua = buocSua([{ vai: 'may', en: 'Hi.', buoc: 'mau' },
                        { vai: 'be', chu: 'x', diem: 4, mau: 'Hi.', thieu: ['hi'] }]);
  assert.equal(bSua?.loai, 'sua');
  const dSua = dongBuoc(bSua, { tenBe: 'An' }, { chu: 'x', diem: 4, thieu: ['hi'] });
  assert.match(dSua, /CORRECTION turn/i, 'nhánh kịch bản mất hẳn lời dặn sửa lỗi');
  assert.match(dSua, /Name the one thing that went wrong/i);
  assert.match(dSua, /Do not move on/i);
});

test('lời dặn mang BỐI CẢNH của chính unit ấy', () => {
  /* Bác dặn 18-08: "kịch bản/prompt theo từng Unit mới đảm bảo sát nội dung". Câu
     tiếng Anh thì sát từ trước (kịch bản ép từng câu), nhưng cái KHUNG buổi học
     thì chưa — lời dặn cũ chỉ đưa một bảng từ và một bảng công thức. */
  const u = { ten: 'Unit 5 · Sở thích', muc_tieu: 'Nói mình thích làm gì',
              tinh_huong: 'Bạn hỏi con thích làm gì lúc rảnh.' };
  const s = loiDan({ von: vonB09(), tenBe: 'An', lop: 3, unit: u });
  assert.match(s, /TODAY'S UNIT: Unit 5/);
  assert.match(s, /Nói mình thích làm gì/);
  assert.ok(!loiDan({ von: vonB09() }).includes("TODAY'S UNIT"),
    'không có kịch bản thì đừng dựng khối rỗng');

  /* Và mọi kịch bản phải MANG được bối cảnh ấy — sinh thiếu thì lời dặn rỗng. */
  for (const k of MOI_KB) {
    assert.ok(k.muc_tieu || k.tay, `${k.ma}/${k.bai}: thiếu mục tiêu unit`);
  }
});

test('chỗ gọi TRUYỀN điểm của bé và bối cảnh unit lên lời dặn', () => {
  /* Tính ra mà không gửi đi thì y như không tính — đúng cái đã xảy ra với `thieu`:
     `chamCau` tính nó từ lâu, `PhongNoi.jsx` vứt ngay tại chỗ nhận. */
  const g = readFileSync(new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(g, /luotBeCuoi\(lichSu\)/, 'phải lấy lượt vừa rồi của bé');
  assert.match(g, /dongBuoc\(buoc, \{[^}]*\}, luotBe\)/, 'và gửi kèm lời dặn');
  assert.match(g, /unit\b/, 'bối cảnh unit phải đi cùng');

  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /thieu: kq\?\.thieu/, 'chữ bé bỏ sót phải được GIỮ trong lượt');
  assert.match(pn, /thieuChucNang/, 'cả chữ chức năng');
});

test('phòng nói mở ĐÚNG QUYỂN của bài, không phải lúc nào cũng quyển 1', () => {
  /* ⚠ Lỗi câm sống lâu nhất của phòng này. `napKichBanNoi()` gọi không tham số nên
     mặc định `'ta1'`; lớp 2 và lớp 3 tải về kịch bản LỚP 1, `kichBanCua` không
     thấy bài nào, `kichBan = null`, và cả tầng kịch bản tắt — phòng rơi về lối mô
     hình tự nghĩ câu. Không có gì đỏ: tệp tải về hợp lệ, chỉ là của quyển khác.
     Kèm theo đó `lop` mặc định 1 (lời dặn gọi bé lớp 3 là "a six-year-old") và
     `quyen: 'ta1'` ghi cứng vào sổ trên máy chủ. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /napKichBanNoi\(ma\)/, 'phải nạp kịch bản theo mã quyển của bài');
  assert.match(pn, /const ma = bai\?\.quyen/, 'mã quyển suy từ chính bài');
  assert.match(pn, /const lop = bai\?\.grade/, 'lớp cũng thế');
  assert.doesNotMatch(pn, /quyen: 'ta1'/, 'không được ghi cứng quyển khi lưu buổi');

  const nd = readFileSync(new URL('../src/mon/tienganh/lib/noiDung.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\*\*[\s\S]*?\*\//g, '');
  assert.match(nd, /khoKichBan = new Map\(\)/, 'ô nhớ phải tách theo quyển');
  assert.match(nd, /chuongTrinh\(quyenCua\(id\)\)\?\.bai/,
    'maBaiTruoc phải tra sổ đăng ký, `quyenCua` chỉ trả về một CHUỖI mã');
});

test('dấu nháy giữa một từ tiếng Anh KHÔNG phải dấu mở ngoặc', () => {
  /* `He's/She's + [Number].` từng bị đọc thành mẩu trích `s/She`, rồi báo
     `chữ "s" không có trong bài` — câu hoàn toàn đúng mà bị gạt. Mà tiếng Anh ba
     quyển này đầy chữ rút gọn: It's · What's · He's · isn't. */
  const von = vonB09();
  assert.ok(loiVietHopLe("Con đáp theo khuôn: He's/She's + [Number].", { von }).ok);
  /* Nhưng dấu nháy đứng riêng thì vẫn là ngoặc, và vẫn phải soi. */
  assert.ok(!loiVietHopLe("Con vừa nói 'washes machine' nhỉ.", { von }).ok);
});

test('cô được trích lại LỜI CHÚ NGHĨA của sách, kể cả khi nó dùng chữ "bạn"', () => {
  /* Sách chú `you` là "bạn, các bạn" và `top` là "con quay". Chặn cả hai thì cô
     mất hẳn cách giảng nghĩa — mà chặn ở đây không kêu thành lỗi: `loiVietSach`
     lặng lẽ lui về câu chung chung. Hai kiểu hỏng khác nhau, cùng một hậu quả:
       · "bạn"      → phép soi ĐẠI TỪ tưởng cô gọi bé là bạn;
       · "con quay" → phép soi CHỮ LẠ tưởng đó là tiếng Anh (không dấu nào cả). */
  const v14 = vonTu({
    baiNay: JSON.parse(readFileSync(
      new URL('../public/content/ta1/DL_TA1_B14.json', import.meta.url), 'utf8')),
    baiCu: [], daDat: false,
  });
  assert.ok(loiVietHopLe('Chỉ một chữ thôi: “top” — nghĩa là “con quay”.', { von: v14 }).ok);
  /* Nới cho lời chú KHÔNG được thành cửa cho đại từ lọt: ngoài ngoặc vẫn chặn. */
  assert.ok(!loiVietHopLe('Bạn nói lại từ “top” đi.', { von: v14 }).ok);
});

test('cô được trích lại đúng câu BÉ VỪA NÓI để mà sửa', () => {
  /* Không mở chỗ này thì lượt sửa tự bóp cổ mình: cô trích cái bé vừa nói ("con
     nói It cooking"), mà cái ấy vốn KHÔNG phải chữ của bài — nên bị gạt, và lời
     sửa cụ thể bị vứt đi đúng lượt cần nó nhất. */
  const von = vonB09();
  const s = 'Con vừa nói "How many clock" — thiếu mất chữ cuối.';
  assert.ok(!loiVietHopLe(s, { von }).ok, 'không kèm lời bé thì vẫn phải gạt');
  assert.ok(loiVietHopLe(s, { von, beNoi: 'how many clock' }).ok,
    'kèm lời bé thì cô được nhắc lại để sửa');
});

test('lượt đáp LỜI CHÀO không phải một lần luyện', () => {
  /* ⚠ Hai chỗ hỏng cùng một gốc, và cả hai chỉ lộ khi trải một buổi ra giấy:
       · buổi kết ở `DAT_LIEN_DE_XONG = 3`, mà lượt "hello" ăn mất một suất — bé
         giỏi chỉ phải nói đúng HAI câu là được khen "con nắm bài rồi";
       · bước luyện chọn theo `soDat % n`, lượt chào đẩy chỉ số lên 1, nên bước
         `mau` — chỗ cô LÀM MẪU — không bao giờ tới lượt. Bé bị hỏi
         "What's your hobby?" khi chưa hề nghe một mẫu câu nào.
     Không có gì đỏ ở cả hai: cô vẫn nói đúng câu của bài, màn kết vẫn chúc mừng. */
  const ls = [{ vai: 'be', chu: 'chào cô' },
              { vai: 'may', en: 'Hello!', buoc: 'chao' },
              { vai: 'be', chu: 'hello', diem: 9, mau: 'Hello!' }];
  assert.equal(luotLuyen(ls).length, 0, 'đáp lời chào không tính là luyện');
  assert.equal(tinhBuoi({ lichSu: ls }).datLien, 0, 'và không đẩy buổi tới gần vạch kết');

  /* Lấy một kịch bản THƯỜNG. ⚠ Không tìm trong ta3 nữa: từ 19-08 CẢ 21 unit lớp 3
     đều là bài tả tranh, nên `find` trả undefined và phép kiểm nổ ở `k.tu[0]` —
     không phải vì luật sai mà vì hết mẫu để thử. Lấy quyển còn kịch bản thường. */
  const k = MOI_KB.find((x) => x.dang !== 'tranh' && x.tu?.length);
  assert.equal(buocTiepTheo({ kichBan: k, lichSu: ls, hoSo: { thich: k.tu[0] } }).loai,
    'mau', 'bước luyện ĐẦU TIÊN phải là cô làm mẫu');

  /* Buổi cũ chưa có trường `buoc` thì vẫn phải đếm — thà rộng còn hơn xoá mất
     tiến độ bé đã có. */
  const cu = [{ vai: 'may', en: 'Hello!' }, { vai: 'be', chu: 'hello', diem: 9 }];
  assert.equal(luotLuyen(cu).length, 1);
});

test('sửa nhiều nhất HAI lần rồi nhường đường cho việc dễ hơn', () => {
  /* ⚠ Không có chốt này thì phòng nói thành cái bẫy: `soDat` chỉ tăng khi bé ĐẠT,
     mà lượt sửa lại chen lên trước cả vòng luyện — nên bé đuối bị hỏi đúng MỘT câu
     suốt 20 phút, kể cả khi `haDoKho` đã bật. Trải ra giấy thấy mười lượt liền đều
     là "Hello!". Không lỗi, không cảnh báo, đồng hồ vẫn chạy. */
  const may = { vai: 'may', en: "It's cooking.", buoc: 'noiCa' };
  const truot = { vai: 'be', chu: 'it cook', diem: 3, mau: "It's cooking.", thieu: ['cooking'] };
  const n = (lan) => Array.from({ length: lan }, () => [may, truot]).flat();
  assert.equal(buocSua(n(1))?.loai, 'sua', 'lần đầu phải sửa');
  assert.equal(buocSua(n(SUA_TOI_DA))?.loai, 'sua', `sửa đủ ${SUA_TOI_DA} lần`);
  assert.equal(buocSua(n(SUA_TOI_DA + 1)), null, 'quá thì thôi, để bé làm việc dễ hơn');

  /* Và lúc ấy vòng luyện phải nhận được đường — dưới `haDoKho` là bước TỪ. */
  const k = MOI_KB.find((x) => x.dang !== 'tranh' && x.tu?.length);
  const b = buocTiepTheo({ kichBan: k, lichSu: n(SUA_TOI_DA + 1),
                           hoSo: { thich: k.tu[0] }, haDoKho: true });
  assert.equal(b.loai, 'tu', 'đuối mãi thì phải được lùi về một chữ');

  /* Bài TẢ TRANH thì đường lui là CÂU HỎI GỢI Ý — bác chốt 19-08: "học sinh không
     biết tả thì cô hỏi how many kite in the picture". Bí thì được hỏi, chứ không
     phải bị đẩy về nhại một chữ. */
  const kt = MOI_KB.find((x) => x.dang === 'tranh');
  if (kt) {
    const bt = buocTiepTheo({ kichBan: kt, lichSu: n(SUA_TOI_DA + 1),
                              hoSo: {}, haDoKho: true });
    assert.equal(bt.loai, 'goiY', 'tả tranh mà bí thì cô phải HỎI, không bắt nhại từ');
  }

  /* Câu KHÁC thì đếm lại từ đầu — bé sai chỗ mới vẫn được sửa. */
  const khac = [...n(SUA_TOI_DA + 1), { vai: 'may', en: "It's dancing.", buoc: 'noiCa' },
                { vai: 'be', chu: 'it dan', diem: 3, mau: "It's dancing." }];
  assert.equal(buocSua(khac)?.loai, 'sua');
});

test('lượt CHÀO không bị đem ra sửa', () => {
  /* Bé lí nhí chữ "hello" mà bị cô bắt sửa ngay trước khi vào bài thì buổi học mở
     đầu bằng một lời chê. Trải ra giấy: lượt 2 của cả buổi đã là một lượt sửa. */
  const ls = [{ vai: 'may', en: 'Hello!', buoc: 'chao' },
              { vai: 'be', chu: '', diem: 2, mau: 'Hello!' }];
  assert.equal(buocSua(ls), null);
});

test('lượt hỏi sở thích: câu của mô hình VẪN bị soi', () => {
  /* ⚠ Đúng MỘT lượt mỗi buổi lọt lưới, và là lượt thứ hai — lúc bé vừa vào phòng.
     `hoiThich` không mang câu tiếng Anh nào (thẻ chọn hình do máy con vẽ), nên
     `dienBuoc` trả chuỗi rỗng; mà nhánh CÓ kịch bản thì cố ý bỏ qua `cauHopLe` vì
     câu đã biết trước. Hai điều đúng riêng lẻ, ghép lại thành một lỗ. */
  const g = readFileSync(new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(g, /!dung && !cauHopLe\(/, 'bước không có câu viết sẵn thì phải soi');
  assert.ok(!/cauThayThe\(null/.test(g),
    '`cauThayThe` cần một `viec`; nhánh kịch bản không có, gọi vào là nhận null');
  assert.ok(LOI_LOP_HOC.includes('Your turn.'), 'câu lui phải là lời lớp học có sẵn');
});

/* ═══════════ BÀI TẢ TRANH — CÔ HƯỚNG DẪN, KHÔNG DẠY NHẠI CÂU HỎI ═══════════ */

test('bé phải ĐÁP câu hỏi của cô, không nhại lại câu hỏi', async () => {
  /* ⚠ CHỖ HỎNG NẶNG NHẤT CỦA CẢ PHÒNG NÀY, bác bắt 19-08-2026:

       "Phần nói là AI đóng vai trò giáo viên hướng dẫn học sinh tả tranh chứ không
        phải là bắt học sinh nói theo mấy câu kiểu What can you see. Mấy câu What
        can you see dùng để hướng dẫn học sinh nói thôi."

     Cả phòng nói dựng trên giả định BÉ NHẠI LẠI CÂU CÔ VỪA NÓI, và phép chấm cũng
     thế. Với bài tả tranh thì sai hẳn. Trải một buổi ra giấy: bé nói
     "what can you see?" và được **9/10** — hệ thống KHEN bé vì nhại đúng câu hỏi
     của cô. Không có gì đỏ, điểm còn cao hơn khi bé tả thật. */
  const { canNoi } = await import('../src/mon/tienganh/lib/phongnoi.js');
  const kb = { dang: 'tranh', moTaTranh: ['I can see a kite.', 'This is a kitten.'] };

  const hoi = { loai: 'goiY', en: 'How many kites can you see?', dapMau: 'I can see three.' };
  assert.deepEqual(canNoi(hoi, kb), ['I can see three.'],
    'cô HỎI thì câu đúng là câu ĐÁP, không phải câu hỏi');
  assert.ok(!canNoi(hoi, kb).includes(hoi.en), 'câu hỏi của cô KHÔNG được tính là đúng');

  /* Bước mời tả: bé nói câu nào trong tranh cũng đúng — bắt khớp một câu là chấm
     sai đứa tả đúng theo thứ tự khác. */
  const moi = { loai: 'taTranh', en: 'What can you see?' };
  assert.deepEqual(canNoi(moi, kb), kb.moTaTranh);

  /* Bài THƯỜNG giữ nguyên lối cũ — 20 kịch bản kia không được đổi hành vi. */
  assert.deepEqual(canNoi({ loai: 'noiCa', en: "It's cooking." }, null), ["It's cooking."]);
});

test('lời dặn bài tả tranh KHÔNG mượn lời dặn cũ', async () => {
  /* Bác chốt: "Hãy xoá hết prompt cũ để cài đặt lại." Lời dặn cũ dài mười điều và
     gần như điều nào cũng nói về DẠY NHẠI CÂU. Ghép thêm mấy dòng về tranh vào đấy
     thì mô hình vẫn đọc ra "dạy bé nói theo mẫu", vì chín phần mười lời dặn nói
     thế — nên phải là một lời dặn RIÊNG, ngắn, chỉ nói một việc. */
  const { loiDanTranh } = await import('../src/mon/tienganh/lib/phongnoi.js');
  const kb = { dang: 'tranh', moTaTranh: ['I can see a kite.', 'This is a kitten.'] };
  const s = loiDanTranh({ tenBe: 'An', lop: 3, kichBan: kb,
    buoc: { loai: 'goiY', en: 'How many kites can you see?', dapMau: 'I can see three.' } });

  assert.match(s, /DESCRIBE A PICTURE/i, 'phải nói rõ việc là tả tranh');
  assert.match(s, /NOT teaching her to repeat your sentences/i);
  assert.match(s, /she must never be/i);
  assert.match(s, /NEVER read the whole description out/i,
    'đọc hết bản mô tả ra là làm hộ bé cả bài');
  assert.match(s, /call yourself "cô", call the child "con"/i, 'xưng hô vẫn phải gác');

  /* Và KHÔNG được có dấu vết của lời dặn cũ. */
  assert.ok(!/put the word "?\w+"? in the slot/i.test(s), 'còn sót lối dạy điền ô trống');
  assert.ok(!/A pattern is a FRAME/i.test(s), 'còn sót bảng công thức của lời dặn cũ');

  /* Bé nhại lại câu hỏi thì lời dặn phải BẮT được — điểm phát âm lúc ấy rất cao,
     nên chỉ nhìn điểm thì cô lại khen. */
  const s2 = loiDanTranh({ tenBe: 'An', lop: 3, kichBan: kb,
    buoc: { loai: 'goiY', en: 'How many kites can you see?', dapMau: 'I can see three.' },
    luotBe: { chu: 'how many kites can you see?', diem: 9, mau: 'I can see three.' } });
  assert.match(s2, /repeated your QUESTION instead of answering/i);
});

test('màn phòng nói KHÔNG bày sẵn vốn từ ở bài tả tranh', () => {
  /* Bác chốt 19-08: "Bỏ phần: Con nói về". Khối ấy liệt kê từng vật kèm HÌNH —
     kite · yo-yo · kitten · teddy bear. Với bài tả tranh thì đó chính là đáp án bày
     ra trước mặt: bé đọc bảng chứ không nhìn tranh mà tìm chữ. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\{\/\*[\s\S]*?\*\/\}/g, '');
  assert.match(pn, /laTranh \? null : \(/, 'bài tả tranh phải giấu khối vốn từ');
  assert.match(pn, /const laTranh = kichBan\?\.dang === 'tranh'/);
  /* Nhưng bài THƯỜNG thì giữ — đó là vốn từ của unit, đúng việc của nó. */
  assert.match(pn, /Con nói về/, 'bài thường vẫn còn bảng vốn từ');
});

test('bé đáp nhầm thì cô DẪN VỀ ĐÚNG CÂU HỎI, không chỉ chê', async () => {
  /* Bác chốt 19-08-2026: "Khi học sinh nói chưa đúng → Giúp học sinh nói đúng theo
     nội dung đang hỏi nhé."

     Bước sửa cũ chỉ đọc lại câu đích và nói "con thiếu chữ X". Ở bài tả tranh thì
     hụt hẳn một nửa: bé sai vì ĐÁP NHẦM CÂU HỎI, không phải vì thiếu chữ. Cô hỏi
     "How many kites can you see?" mà bé nói "I can see a kite." — không thiếu chữ
     nào cả. Bảo "thiếu chữ three" thì bé càng rối. */
  const { buocSua, loiDanTranh } = await import('../src/mon/tienganh/lib/phongnoi.js');
  const ls = [
    { vai: 'may', en: 'How many kites can you see?', buoc: 'goiY' },
    { vai: 'be', chu: 'I can see a kite.', diem: 3, mau: 'I can see three.', thieu: [] },
  ];
  const b = buocSua(ls);
  assert.equal(b.loai, 'sua');
  assert.equal(b.hoiLai, 'How many kites can you see?', 'bước sửa phải NHỚ câu đang hỏi');
  assert.equal(b.en, 'I can see three.', 'và đọc câu đáp ĐÚNG cho câu hỏi ấy');
  assert.match(b.vi, /How many kites can you see\?/, 'lời viết sẵn phải nhắc lại câu hỏi');

  const s = loiDanTranh({ tenBe: 'An', lop: 3, buoc: b,
    kichBan: { dang: 'tranh', moTaTranh: ['I can see a kite.'] },
    luotBe: ls[1] });
  assert.match(s, /You had asked: "How many kites can you see\?"/);
  assert.match(s, /answer that fits that question/i);
  assert.match(s, /answered a different question/i, 'phải kể ra ca đáp nhầm câu');
  assert.match(s, /Do not move on/i, 'sửa xong mới đi tiếp');

  /* Bài THƯỜNG không có câu hỏi trước thì giữ nguyên lối cũ — 20 kịch bản kia
     không được đổi hành vi. */
  const bt = buocSua([{ vai: 'may', en: "It's cooking.", buoc: 'noiCa' },
    { vai: 'be', chu: 'it cook', diem: 3, mau: "It's cooking.", thieu: ['cooking'] }]);
  assert.equal(bt.hoiLai, null);
  assert.match(bt.vi, /chưa có chữ/);
});

test('bài tả tranh KHÔNG hỏi "con thích cái nào nhất"', () => {
  /* Bác chốt 19-08: "Bỏ phần con thích cái nào nhất."
     Thẻ ấy sinh ra cho bài thường — bé chọn một thứ rồi cô điền nó vào ô trống của
     mẫu câu. Bài tả tranh không có ô trống nào, và cũng không hỏi bé THÍCH gì; nó
     hỏi bé NHÌN THẤY gì. Để lại là chen một việc lạ vào giữa, lại còn bày sẵn tên
     mấy vật trong tranh kèm hình — tức là cho sẵn đáp án lần nữa. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\{\/\*[\s\S]*?\*\/\}/g, '');
  /* ⚠ KHÔNG ghim cả biểu thức. Bản đầu viết `/!laTranh && !thich && hoiThich/` —
     ghim đúng từng chữ, kể cả cái mà cổng này KHÔNG quan tâm. Nên khi sở thích
     được cho nhớ qua buổi (`thich` → `thichDung`, xem `tienganh_sothich.test.mjs`)
     thì cổng đỏ lên, trong khi điều nó canh — bài tả tranh giấu thẻ — vẫn nguyên.

     Cổng ghim quá chặt thì mỗi lần sửa việc khác lại đỏ một lần, và cách người ta
     dập nó nhanh nhất là nới toang ra; thế là mất luôn phép canh thật. Nên chỉ
     ghim ĐÚNG hai đầu: `!laTranh` phải đứng trước, và `hoiThich` là thứ bị chặn.
     Ở giữa để `!thich\w*` — cho `thich` lẫn `thichDung`, không cho bỏ trống. */
  assert.match(pn, /!laTranh\s*&&\s*!thich\w*\s*&&\s*hoiThich/,
    'bài tả tranh phải giấu thẻ sở thích');
  assert.match(pn, /Con thích cái nào nhất\?|cauHoiSoThich/, 'bài thường vẫn còn thẻ ấy');
});

test('mẩu tiếng Anh trong lời hướng dẫn phải đọc bằng GIỌNG ANH', async () => {
  /* ⚠ Bác bắt 19-08-2026: "Ở phần hướng dẫn khi có cả tiếng việt và tiếng anh thì
     bạn lại phát hết bằng tiếng Việt khiến từ tiếng anh rất khó đọc."

     Phép tách cũ chỉ nhận ra tiếng Anh khi mẩu ấy nằm trong VỐN TỪ CỦA UNIT. Đúng
     cho bài thường; hỏng hẳn ở bài tả tranh, vì câu cô trích là câu của kho TÍCH
     LUỸ ("How many kites can you see?") mà vốn của unit 0 chỉ có mười con số. Cả
     câu rơi vào nhánh `vi` và Kokoro-VI đọc "kites" theo vần Việt.

     Không có gì đỏ: `docDoan` vẫn chạy, vẫn phát ra tiếng. Chỉ tai mới biết. */
  const { readFileSync } = await import('node:fs');
  const bai = JSON.parse(readFileSync(
    new URL('../public/content/ta3/DL_TA3_B00.json', import.meta.url), 'utf8'));
  const von = vonTu({ baiNay: bai, baiCu: [], daDat: false });

  const loi = 'Cô đang hỏi “How many kites can you see?”. Con nhìn tranh rồi nói lại nhé.';
  const ra = tachTheoTieng(loi, von);
  assert.ok(ra.some((x) => x.tieng === 'en' && /How many kites/.test(x.chu)),
    'mẩu trong ngoặc kép phải được đánh dấu tiếng Anh');
  assert.ok(ra.some((x) => x.tieng === 'vi' && /Cô đang hỏi/.test(x.chu)),
    'phần tiếng Việt vẫn phải là tiếng Việt');

  /* Mẩu trong ngoặc mà CÓ dấu tiếng Việt thì vẫn là tiếng Việt — cô trích lời mình
     chứ không trích tiếng Anh. Cùng luật `loiVietHopLe` đang dùng. */
  const v = tachTheoTieng('Mình nói “đỏ” rồi mới nói “bút chì” nhé.', von);
  assert.ok(!v.some((x) => x.tieng === 'en'), 'trích tiếng Việt thì đừng đọc giọng Anh');

  /* Và nguồn mốc thứ hai: câu cô ĐÃ NÓI trong buổi, do màn hình đưa vào. */
  const r2 = tachTheoTieng('Con nói lại I can see three. nhé.', von, ['I can see three.']);
  assert.ok(r2.some((x) => x.tieng === 'en' && x.chu === 'I can see three.'));
});

test('màn phòng nói ĐƯA nguồn mốc tiếng Anh của buổi vào phép tách', () => {
  /* Tính đúng mà không truyền đi thì y như không tính — `tachTheoTieng` nhận `them`
     mà màn hình gọi thiếu tham số thì mọi câu của kho tích luỹ lại rơi về giọng
     Việt. Đúng cái bẫy đã sập với `thieu` và với `can`. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.match(pn, /const mocEn = React\.useMemo/, 'phải gom mốc tiếng Anh của buổi');
  assert.match(pn, /moTaTranh \|\| \[\]/, 'bản mô tả tranh phải nằm trong mốc');
  for (const m of pn.matchAll(/tachTheoTieng\(([^)]*)\)/g)) {
    assert.match(m[1], /mocEn/, `còn chỗ gọi thiếu mốc: tachTheoTieng(${m[1]})`);
  }
});

test('mẩu tiếng Việt không mang dấu mồ côi để đọc thành chữ', async () => {
  /* Bác bắt 19-08-2026: "Khi đọc tiếng Việt bạn đọc cả dấu . đâu cần thiết như vậy."

     Cắt một câu ra làm ba thì dấu ở chỗ cắt thành mồ côi:

         Cô đang hỏi “  |  How many kites can you see?  |  ”. Con nhìn tranh…

     `docDoan` đưa thẳng chuỗi cho bộ đọc, mà giọng Việt đọc luôn cái ngoặc kép và
     cái chấm ấy thành chữ — nghe ra "ngoặc kép chấm". Dấu ngoặc vốn là ký hiệu cho
     MẮT, còn cái chấm thuộc về câu tiếng Anh vừa đọc xong.

     Không có gì đỏ: chuỗi hợp lệ, bộ đọc chạy bình thường. Chỉ tai mới biết. */
  const { readFileSync } = await import('node:fs');
  const bai = JSON.parse(readFileSync(
    new URL('../public/content/ta3/DL_TA3_B00.json', import.meta.url), 'utf8'));
  const von = vonTu({ baiNay: bai, baiCu: [], daDat: false });

  const ra = tachTheoTieng(
    'Cô đang hỏi “How many kites can you see?”. Con nhìn tranh rồi nói lại nhé.', von);
  const viet = ra.filter((x) => x.tieng === 'vi').map((x) => x.chu);
  assert.deepEqual(viet, ['Cô đang hỏi', 'Con nhìn tranh rồi nói lại nhé.']);
  for (const x of viet) {
    assert.ok(!/[“”"]/.test(x), `mẩu Việt còn ngoặc kép: ${JSON.stringify(x)}`);
    assert.ok(!/^[\s\p{P}]/u.test(x), `mẩu Việt mở đầu bằng dấu: ${JSON.stringify(x)}`);
  }

  /* ⚠ Mẩu TIẾNG ANH giữ nguyên dấu. Dấu hỏi cuối câu là thứ làm nên ngữ điệu hỏi;
     bỏ đi thì "How many kites can you see" đọc ra như một câu kể. */
  assert.ok(ra.some((x) => x.tieng === 'en' && x.chu.endsWith('?')),
    'câu hỏi tiếng Anh phải giữ dấu hỏi');

  /* Và dấu chấm CUỐI câu tiếng Việt thì giữ — nó là chỗ ngắt nhịp tự nhiên. */
  assert.ok(viet[1].endsWith('.'));
});
