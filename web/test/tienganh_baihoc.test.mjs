/**
 * CỔNG · BÀI HỌC CUỐI BUỔI (mẫu Reflexion, việc V8).
 *
 * ── CHỖ NÀY LÀ CHỖ DUY NHẤT MỘT CÂU DO MÔ HÌNH VIẾT ĐƯỢC GHI LẠI ──
 * Mọi câu khác của cô giáo máy sống đúng một lượt rồi trôi. Bài học thì đi vào trí
 * nhớ (`hosoai.js`), vào lời dặn của những buổi sau, vào Góc bố mẹ, và sống năm
 * buổi. Nên tệp này canh nặng nhất vào `soiBaiHoc` — cái cửa duy nhất.
 *
 * Ba thứ phải chặn, và cả ba đều có lý do cụ thể:
 *   1. NHẬN XÉT VỀ TÍNH CÁCH — "Bé lười nói" nằm trong hồ sơ một đứa trẻ sáu tuổi
 *      và bố mẹ đọc nó. Đó là thứ không ai có quyền viết hộ.
 *   2. CHỮ ANH NGOÀI VỐN — bài học đi vào lời dặn, nên một chữ lạ ở đây là tự tay
 *      mời mô hình dùng chữ bé chưa học: chọc thủng hàng rào TỪ BÊN TRONG.
 *   3. SỐ — lời dặn rất dễ bị nhại nguyên văn, và "Con nói được 3/5 câu" đọc to lên
 *      trước mặt bé là câu không ai muốn bé nghe.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  loiDanTomTat, docTomTat, soiBaiHoc, soiGoiTomTat,
  TOM_TAT_TOI_DA_CHU, BAI_HOC_TOI_DA_CHU, BAI_HOC_MOI_BUOI, TU_CAM,
} from '../src/mon/tienganh/lib/baihoc.js';
import { tomTatBuoi, LOI_TOM_TAT } from '../src/mon/tienganh/lib/goiPhongNoi.js';
import { vonTu } from '../src/mon/tienganh/lib/phongnoi.js';
import { hoSoRong, themBaiHoc, donHoSo, dongHoSoAI } from '../src/mon/tienganh/lib/hosoai.js';
import { TOI_DA_CHU_LOI_DAN, soiGoi } from '../functions/src/luyennoi.js';

const doc = (p) => JSON.parse(readFileSync(new URL(p, import.meta.url), 'utf8'));
const B05 = doc('../public/content/ta1/DL_TA1_B05.json');
const VON = vonTu({ baiNay: B05 });
/* Vốn nhỏ gọn cho bốn ca của §8 — `a` và `dog` phải nằm trong vốn. */
const VON_NHO = { loi: { tu: [{ tu: 'a' }, { tu: 'dog' }, { tu: 'chips' }], cau: [], cauSach: [] }, on: [] };

/* ═══════════ 1 · SOI BÀI HỌC ═══════════ */

test('soiBaiHoc: bác tính cách · bác không-phải-tiếng-Việt · bác số', () => {
  /* Bốn ca của §8, đúng thứ tự, kỳ vọng false · false · false · true. */
  const ca = [
    ['Bé lười nói', false, 'nhận xét về tính cách'],
    ['She forgets "chips"', false, 'không phải tiếng Việt'],
    ['Nói được 3/5 câu', false, 'có số'],
    ['Bé hay bỏ chữ "a" trước "dog"', true, 'bài học ĐÚNG — phải cho qua'],
  ];
  for (const [chu, mong, vi] of ca) {
    const kq = soiBaiHoc(chu, { von: VON_NHO });
    assert.equal(kq.ok, mong, `${vi}: ${JSON.stringify(chu)} → ${kq.ok} (${kq.vi})`);
    if (!mong) assert.ok(kq.vi, 'bác mà không nói lý do thì không ai sửa được lời dặn');
  }
});

test('MỌI từ cấm đều bị bắt, và bắt theo TIẾNG', () => {
  for (const t of TU_CAM) {
    assert.equal(soiBaiHoc(`Bé hơi ${t} ở phần này`, { von: VON_NHO }).ok, false,
      `từ cấm "${t}" đi lọt`);
  }
  /* Soi theo tiếng, nên "tệp" không bị bắt oan vì có "tệ". */
  assert.equal(soiBaiHoc('Con đọc tệp bài rất kỹ', { von: VON_NHO }).ok, true);
});

test('chữ Anh NGOÀI VỐN bị bác; chữ TRONG VỐN thì qua', () => {
  /* Bài học đi vào lời dặn — một chữ lạ ở đây là tự mời mô hình dùng chữ bé chưa
     học. Cùng chỗ hỏng `tienganh_sothich` canh cho sở thích. */
  assert.equal(soiBaiHoc('Con hay quên chữ "delicious"', { von: VON }).ok, false);
  assert.equal(soiBaiHoc('Con hay quên chữ "fish"', { von: VON }).ok, true);
  /* Mẩu trong ngoặc có DẤU TIẾNG VIỆT là lời Việt, không phải chữ Anh — đừng soi. */
  assert.equal(soiBaiHoc('Con nói "cá" thay vì tiếng Anh', { von: VON }).ok, true);
  /* Không truyền vốn thì KHÔNG soi phần ấy — nhưng cũng không được vỡ. */
  assert.equal(soiBaiHoc('Con hay quên chữ "delicious"').ok, true);
});

test('bài học rỗng hoặc quá dài bị bác', () => {
  assert.equal(soiBaiHoc('', { von: VON }).ok, false);
  assert.equal(soiBaiHoc('   ', { von: VON }).ok, false);
  assert.equal(soiBaiHoc(`Con ${'ê'.repeat(BAI_HOC_TOI_DA_CHU)}`, { von: VON }).ok, false);
});

test('soiGoiTomTat giữ phần lành, bỏ phần hỏng, và NÓI RA phần bị bỏ', () => {
  /* Bỏ ĐÚNG phần hỏng: một bài học sai thì bỏ bài ấy, mấy bài kia vẫn còn. Vứt cả
     gói vì một câu là mất luôn phần cô nhìn ra đúng. */
  const kq = soiGoiTomTat({
    baiHoc: [{ chu: 'Bé hay bỏ chữ "fish"' }, { chu: 'Bé lười' }, { chu: 'Nói đúng 2 câu' }],
    khen: 'Con nói to và rõ.',
  }, { von: VON });
  assert.equal(kq.baiHoc.length, 1);
  assert.equal(kq.boQua.length, 2);
  assert.ok(kq.boQua.every((x) => x.vi), 'phần bị bỏ phải kèm lý do');
  assert.equal(kq.khen, 'Con nói to và rõ.');

  /* Lời khen cũng chịu đúng mấy luật ấy. */
  assert.equal(soiGoiTomTat({ baiHoc: [], khen: 'Con hơi chậm nhưng cố gắng' }, { von: VON }).khen, '');
  /* Và trần số bài học một buổi. */
  const nhieu = soiGoiTomTat({
    baiHoc: Array.from({ length: 9 }, (_, i) => ({ chu: `Bé hay bỏ chữ "fish" lần ${'x'.repeat(i)}` })),
    khen: '',
  }, { von: VON });
  assert.ok(nhieu.baiHoc.length + nhieu.boQua.length <= BAI_HOC_MOI_BUOI);
});

/* ═══════════ 2 · ĐỌC CÂU TRẢ LỜI ═══════════ */

test('docTomTat bóc được JSON lẫn chữ thừa', () => {
  const tt = docTomTat('Sure! {"baiHoc":[{"chu":"Bé hay bỏ chữ a"}],"khen":"Con nói to."} bye');
  assert.equal(tt.baiHoc.length, 1);
  assert.equal(tt.baiHoc[0].chu, 'Bé hay bỏ chữ a');
  assert.equal(tt.khen, 'Con nói to.');
  /* Phần tử là CHUỖI TRẦN cũng nhận — mô hình hay trả hình dạng ấy. */
  assert.equal(docTomTat('{"baiHoc":["chuỗi trần"],"khen":""}').baiHoc[0].chu, 'chuỗi trần');
  /* Danh sách rỗng là một câu trả lời TỐT, không phải lỗi. */
  assert.deepEqual(docTomTat('{"baiHoc":[],"khen":"ổn"}').baiHoc, []);
  for (const x of ['không có json', '{hỏng', '', null]) {
    assert.equal(docTomTat(x), null, `${JSON.stringify(x)} phải ra null`);
  }
});

/* ═══════════ 3 · LỜI DẶN TÓM TẮT ═══════════ */

test('lời dặn tóm tắt dưới trần, và dưới trần MÁY CHỦ', () => {
  for (const [ten, von] of [['vốn nhỏ', VON_NHO], ['vốn thật', VON]]) {
    const d = loiDanTomTat({ von, tenBe: 'Lan', lop: 1 });
    assert.ok(d.length <= TOM_TAT_TOI_DA_CHU, `${ten}: ${d.length} ký tự, quá ${TOM_TAT_TOI_DA_CHU}`);
    assert.ok(d.length <= TOI_DA_CHU_LOI_DAN, `${ten}: quá trần lời dặn của máy chủ`);
    /* Ba luật phải CÓ MẶT trong lời dặn, không chỉ ở phép soi: chặn ở cửa ra thì bé
       mất một bài học; dặn trước thì mô hình không viết ra nó ngay từ đầu. */
    assert.match(d, /VIETNAMESE only/);
    assert.match(d, /NO numbers/);
    assert.match(d, /NOTHING about the child as a person/);
    assert.match(d, /Reply as JSON only/);
  }
});

test('lời dặn tóm tắt vẫn dưới trần với vốn MỞ RỘNG của quyển lớp 5', () => {
  /* Vốn mở rộng gộp cả unit cũ — đây là ca lời dặn DÀI NHẤT. Thử một bài lẻ ở chế
     độ hẹp là thử đúng cái ca không bao giờ vỡ. */
  const ds = JSON.parse(readFileSync(
    new URL('../public/content/ta5/kichban_noi.json', import.meta.url), 'utf8'))
    .map((k) => doc(`../public/content/ta5/${k.bai.replace('DL:', 'DL_').replace(/\./g, '_')}.json`));
  let dai = 0;
  for (let i = 0; i < ds.length; i += 1) {
    const von = vonTu({ baiNay: ds[i], baiCu: ds.slice(0, i), daDat: true, datCu: () => true });
    const d = loiDanTomTat({ von, tenBe: 'Quynhanh', lop: 5 });
    dai = Math.max(dai, d.length);
    assert.ok(d.length <= TOM_TAT_TOI_DA_CHU,
      `${ds[i].id}: lời dặn ${d.length} ký tự, quá trần ${TOM_TAT_TOI_DA_CHU}`);
  }
  assert.ok(dai > 600, `lời dặn dài nhất chỉ ${dai} ký tự — có phải bảng vốn bị cắt sạch?`);
});

test('gói tóm tắt đi qua được chốt cửa của MÁY CHỦ', () => {
  /* Dùng lại callable `luyenNoi`, nên gói phải lọt `soiGoi` — thêm một callable mới
     là thêm một chỗ phải khai secret, khai region, và deploy. */
  const messages = [{ role: 'system', content: loiDanTomTat({ von: VON, tenBe: 'Lan', lop: 1 }) },
    { role: 'user', content: 'hello' }];
  assert.doesNotThrow(() => soiGoi({ messages }));
  assert.equal(soiGoi({ messages })[0].role, 'system', 'lời dặn phải đứng ĐẦU gói');
});

/* ═══════════ 4 · MỘT LƯỢT, CUỐI BUỔI, KHÔNG CHỜ ═══════════ */

const luot = (n, diem) => Array.from({ length: n }, () => ([
  { vai: 'may', chu: 'I like fish.', en: 'I like fish.', vi: 'x', buoc: 'mau' },
  { vai: 'be', chu: 'i like fish', diem, mau: 'I like fish.', thieu: [], thieuChucNang: [] },
])).flat();

test('tomTatBuoi: một lượt gọi, trả về bản ĐÃ SOI', async () => {
  let soLan = 0; let dan = null;
  const goi = async (ms) => {
    soLan += 1; dan = ms;
    return { data: { chu: JSON.stringify({
      baiHoc: [{ chu: 'Bé hay bỏ chữ "fish"' }, { chu: 'Bé lười nói' }],
      khen: 'Con nói to và rõ.',
    }) } };
  };
  const kq = await tomTatBuoi({ von: VON, lichSu: luot(3, 8), tenBe: 'Lan', lop: 1 }, { goi });
  assert.equal(soLan, 1, 'phải gọi ĐÚNG một lượt — bé đang xem màn kết');
  assert.equal(kq.baiHoc.length, 1, 'bài học nhận xét tính cách phải bị bỏ');
  assert.equal(kq.boQua.length, 1);
  assert.equal(kq.khen, 'Con nói to và rõ.');
  /* Lịch sử buổi phải thật sự đi vào gói — không thì mô hình ngẫm về hư không. */
  assert.ok(dan.length > 1, 'gói chỉ có lời dặn, không có lịch sử buổi');
  assert.equal(dan[0].role, 'system');
});

test('buổi QUÁ NGẮN thì không tốn một lời gọi nào', async () => {
  /* Một lượt thì không có cái gì "lặp lại", mà bài học phải là cái LẶP LẠI. */
  let soLan = 0;
  const goi = async () => { soLan += 1; return { data: { chu: '{}' } }; };
  const kq = await tomTatBuoi({ von: VON, lichSu: luot(1, 8), tenBe: 'Lan', lop: 1 }, { goi });
  assert.equal(soLan, 0);
  assert.deepEqual(kq.baiHoc, []);
});

test('mạng hỏng · JSON hỏng → bỏ qua, nhưng ĐẾM', async () => {
  const truoc = { ...LOI_TOM_TAT };
  const hong = async () => { throw Object.assign(new Error('mất mạng'), { code: 'functions/unavailable' }); };
  assert.deepEqual((await tomTatBuoi({ von: VON, lichSu: luot(3, 8), tenBe: 'L', lop: 1 }, { goi: hong })).baiHoc, []);
  const rac = async () => ({ data: { chu: 'xin chào, không có json nào' } });
  assert.deepEqual((await tomTatBuoi({ von: VON, lichSu: luot(3, 8), tenBe: 'L', lop: 1 }, { goi: rac })).baiHoc, []);
  assert.equal(LOI_TOM_TAT.hong - truoc.hong, 2, 'hỏng mà không đếm thì cả việc V8 thành vô dụng mà vẫn trông như chạy');

  /* Soi bác SẠCH thì đếm riêng — hai con số ấy đòi hai cách chữa khác nhau. */
  const bac = async () => ({ data: { chu: JSON.stringify({ baiHoc: [{ chu: 'Bé lười' }], khen: '' }) } });
  await tomTatBuoi({ von: VON, lichSu: luot(3, 8), tenBe: 'L', lop: 1 }, { goi: bac });
  assert.equal(LOI_TOM_TAT.bac - truoc.bac, 1);
});

test('màn hình gọi cuối buổi, KHÔNG chờ, và cộng dồn đúng bản mới', () => {
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
  const ma = bo(readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8'));
  assert.match(ma, /tomTatBuoi\(/, 'màn hình không gọi tóm tắt — trí nhớ của cô không bao giờ có bài học');
  /* ⚠ KHÔNG `await`: buổi đã kết, bé đang xem màn kết. */
  assert.ok(!/await tomTatBuoi/.test(ma), 'await giữ màn kết lại chờ một lời gọi mạng');
  assert.match(ma, /\.then\(\(\{ baiHoc \}\)/);
  assert.match(ma, /themBaiHoc\(/);
  /* ⚠ Cộng dồn lên bản VỪA GHI (`may`), không đọc lại `tienDo?.hoSoAI` cũ: giữa hai
     lệnh ghi có một quãng chờ mạng. */
  assert.match(ma, /let sau = may;/,
    'cộng bài học lên bản cũ — xoá mất phần capNhatTuBuoi vừa ghi');
});

/* ═══════════ 5 · BÀI HỌC ĐI TỚI BUỔI SAU ═══════════ */

test('bài học vào trí nhớ rồi hiện ở lời dặn buổi sau', () => {
  /* "Định nghĩa XONG" của §7: buổi sau, lời dặn chứa ≥1 bài học của buổi trước. */
  let hs = { ...hoSoRong(), buoiThu: 1 };
  hs = themBaiHoc(hs, { chu: 'Bé hay bỏ chữ "fish"', nut: null, buoi: 1 });
  hs = donHoSo(hs, { buoiHienTai: 1 });
  const khoi = dongHoSoAI(hs, 'Lan');
  assert.match(khoi, /Note from an earlier session/);
  assert.match(khoi, /fish/);
  /* Và nó vẫn không mang chữ số nào — `dongHoSoAI` cắt ở đúng một chỗ. */
  assert.ok(!/\d/.test(khoi));
});

/* ═══════════ 6 · BẢNG ΔC KHÔNG BAO GIỜ TỰ SỬA LỜI DẶN ═══════════ */

test('tools/doc_delta_c.mjs chỉ IN đề xuất, không ghi tệp nào', () => {
  const src = readFileSync(new URL('../tools/doc_delta_c.mjs', import.meta.url), 'utf8');
  /* Đây là chốt của cả việc: một vòng "mô hình tự sửa lời dặn của chính nó" thì
     không ai còn kiểm được điều gì. */
  assert.ok(!/writeFileSync|appendFileSync|rmSync|unlinkSync/.test(src),
    'công cụ ΔC có lệnh GHI tệp — nó phải chỉ in ra');
  assert.match(src, /KHÔNG BAO GIỜ TỰ SỬA/);
  assert.match(src, /PHIEN_BAN_MAU/, 'phải nhắc người sửa tăng số phiên bản mẫu');
  /* Và nó phải chạy được KHÔNG CẦN MẠNG để còn kiểm được. */
  assert.match(src, /--tep/);
});

/* ═══════════ 7 · BÀI HỌC TRÙNG NHAU ═══════════ */

/**
 * ⚠ ĐO THẬT 09-10 BẮT ĐƯỢC: mô hình trả về BA bài học cho CÙNG MỘT lỗi, chỉ khác
 * cái từ bị bỏ — "thiếu 'my' trước brother" · "…trước mother" · "…trước father".
 * Ba dòng chiếm chỗ trong lời dặn mà chỉ nói một điều, và `loiLap` của V3 đã nói
 * điều ấy gọn hơn rồi.
 *
 * Dấu hiệu trùng là KHUÔN CÂU TIẾNG VIỆT, không phải tập chữ trích: phép soi đầu
 * của tôi đòi cùng tập chữ, mà ba bài ấy trích ba tập khác nhau nên nó không bắt
 * được gì. Bỏ phần trong ngoặc ra thì cả ba còn đúng một khuôn.
 */
test('ba bài học cho CÙNG một lỗi chỉ giữ MỘT', () => {
  const von = { loi: { tu: [{ tu: 'my' }, { tu: 'brother' }, { tu: 'mother' }, { tu: 'father' }],
    cau: [], cauSach: [] }, on: [] };
  const kq = soiGoiTomTat({ baiHoc: [
    { chu: 'Lặp lại thiếu từ "my" trước "father" trong câu' },
    { chu: 'Lặp lại thiếu từ "my" trước "brother" trong câu' },
    { chu: 'Lặp lại thiếu từ "my" trước "mother" trong câu' },
    { chu: 'Bé hay lẫn "mother" với "father"' },
  ], khen: '' }, { von });
  assert.equal(kq.baiHoc.length, 2, 'không dọn được bài học trùng');
  assert.equal(kq.boQua.filter((x) => /trùng/.test(x.vi)).length, 2);
  /* ⚠ Và KHÔNG dọn oan: hai lỗi KHÁC nhau thì cả hai phải ở lại, dù cùng trích một
     từ. Dọn theo tập chữ trích sẽ gộp chúng — đó là phép soi sai tôi đã thử. */
  assert.ok(kq.baiHoc.some((x) => /lẫn/.test(x.chu)), 'dọn oan một lỗi khác');
});

test('lời dặn tóm tắt CÓ dặn đừng viết trùng', () => {
  /* Chốt ở mã là lưới đỡ; dặn trước thì mô hình không viết ra nó ngay từ đầu — và
     mỗi bài học thừa là một lời gọi tốn chỗ trong lời dặn buổi sau. */
  assert.match(loiDanTomTat({ von: VON, tenBe: 'Lan', lop: 1 }), /ONE mistake, ONE note/);
  assert.match(loiDanTomTat({ von: VON, tenBe: 'Lan', lop: 1 }), /the SAME/);
});
