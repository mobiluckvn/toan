/**
 * CỔNG · TRÍ NHỚ CỦA CÔ GIÁO MÁY VỀ MỘT BÉ (mẫu Memory, việc V3).
 *
 * Đây là thứ duy nhất trong cả môn còn lại SAU khi bé tắt máy và quay lại hôm sau.
 * Nên tệp này canh đúng những thứ làm nó khác một cái hồ sơ:
 *
 *   1. CHỈ DỮ LIỆU HỌC — không một chữ nào bé tự nói ra, không nhận xét, không số;
 *   2. CÓ HẠN — bài học hết buổi thì đi, nút bé đã thạo thì đi;
 *   3. CÓ TRẦN — ký tự và số phần tử, vì nó đi vào lời dặn mỗi lượt;
 *   4. XOÁ ĐƯỢC SẠCH — và sau khi xoá, lời dặn không còn khối ấy;
 *   5. KHÔNG LỌT VÀO VÂN TAY prompt.
 *
 * Toàn bộ chạy bằng `node`, không mạng: mọi thứ suy từ con số `chamCau` đã tính.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  TRAN_KY_TU, HAN_BUOI, TRAN_PHAN_TU, LAP_DE_NHO, BAI_HOC_TOI_DA_CHU,
  hoSoRong, capNhatTuBuoi, themBaiHoc, donHoSo, dongHoSoAI, xoaHoSoAI,
} from '../src/mon/tienganh/lib/hosoai.js';
import { vonTu, loiDan, DAU_KHOI_RIENG, CUOI_KHOI_RIENG } from '../src/mon/tienganh/lib/phongnoi.js';
import { soRong, gopTienDo } from '../src/mon/tienganh/lib/progress.js';
import { locKhung, vanTay, KHOI_RIENG } from '../functions/src/vantay.js';
import { NGUONG_THAO } from '../src/mon/tienganh/lib/zpd.js';

const beNoi = (o) => ({ vai: 'be', chu: 'x', diem: 4, mau: 'Hello!', thieu: [],
                        thieuChucNang: [], ...o });

const B01 = {
  id: 'B01', title: 'Unit 1',
  knowledgeCore: {
    vocabulary: [{ tu: 'fish', nghia: 'cá' }, { tu: 'milk', nghia: 'sữa' }],
    mauCauDs: [{ cau: 'I like fish.', congThuc: 'I like + [Noun].', dungDe: 'để nói' }],
  },
};
const VON = vonTu({ baiNay: B01 });

/* ═══════════ 1 · RÚT RA TỪ MỘT BUỔI ═══════════ */

test('capNhatTuBuoi rút loiLap từ thieuChucNang LẶP, không từ một lần sót', () => {
  const ls = [beNoi({ thieuChucNang: ['a'] }), beNoi({ thieuChucNang: ['a', 'is'] }),
              beNoi({ diem: 8 })];
  const hs = capNhatTuBuoi(hoSoRong(), { lichSu: ls, bayGio: 7 });
  assert.ok(hs.loiLap.includes('a'), 'sót "a" hai lần → phải nhớ');
  assert.ok(!hs.loiLap.includes('is'), 'sót "is" một lần là chuyện tình cờ, đừng nhớ');
  assert.equal(hs.buoiThu, 1);
  assert.equal(hs.capNhatLuc, 7);
  assert.equal(LAP_DE_NHO, 2);
});

/**
 * ⚠ LUẬT SỐ MỘT CỦA CẢ TỆP: KHÔNG LƯU LỜI BÉ NÓI.
 *
 * `cauDungGanNhat` giữ CÂU ĐÍCH của sách (`luotBe.mau`), không giữ `luotBe.chu`.
 * Hai thứ ấy khác nhau hẳn: một cái là câu bài dạy, một cái là tiếng bé vừa phát
 * ra. Lấy lẫn thì trí nhớ này thành một bản ghi âm chép lại.
 */
test('KHÔNG một chữ nào bé tự nói ra được lưu lại', () => {
  const ls = [beNoi({ diem: 9, chu: 'con noi gi do rat rieng tu', mau: 'I like fish.' })];
  const hs = capNhatTuBuoi(hoSoRong(), { lichSu: ls, hoSo: { thich: 'fish' }, bayGio: 1 });
  const ca = JSON.stringify(hs);
  assert.ok(!ca.includes('rieng tu'), 'lời bé nói lọt vào hồ sơ');
  assert.ok(ca.includes('I like fish.'), 'câu ĐÍCH của sách thì phải giữ');
});

test('lượt chưa chấm được KHÔNG vào hồ sơ', () => {
  /* `diem == null` ở bước không có câu mẫu để so. Đếm nó là đếm một lượt không ai
     chấm, và `buoiThu` thì vẫn tăng — hồ sơ đầy lên bằng những lượt rỗng. */
  const hs = capNhatTuBuoi(hoSoRong(), {
    lichSu: [{ vai: 'be', chu: 'x', diem: null, mau: 'Hello!' }], bayGio: 1,
  });
  assert.deepEqual(hs.cauDungGanNhat, []);
  assert.deepEqual(hs.loiLap, []);
});

test('câu MỚI đẩy câu CŨ ra, không phải ngược lại', () => {
  let hs = hoSoRong();
  for (const c of ['A.', 'B.', 'C.', 'D.', 'E.']) {
    hs = capNhatTuBuoi(hs, { lichSu: [beNoi({ diem: 9, mau: c })], bayGio: 1 });
  }
  assert.equal(hs.cauDungGanNhat.length, TRAN_PHAN_TU.cauDungGanNhat);
  assert.deepEqual(hs.cauDungGanNhat, ['C.', 'D.', 'E.'],
    'giữ câu cũ nhất thì sang buổi sau cô vẫn khen một câu bé đã quên');
});

/* ═══════════ 2 · CÓ HẠN, CÓ TRẦN ═══════════ */

test('bài học hết hạn thì bị dọn', () => {
  let hs = themBaiHoc(hoSoRong(), { chu: 'Con hay quên chữ "a".', nut: 'n1', buoi: 1 });
  assert.equal(hs.baiHoc[0].hetHanBuoi, 1 + HAN_BUOI);
  assert.equal(donHoSo(hs, { buoiHienTai: 1 + HAN_BUOI - 1 }).baiHoc.length, 1);
  assert.equal(donHoSo(hs, { buoiHienTai: 1 + HAN_BUOI }).baiHoc.length, 0,
    'tới hạn là đi — trí nhớ không có hạn thì nó là một cái hồ sơ');
  /* Bài học dài bị cắt, không bị bỏ. */
  hs = themBaiHoc(hoSoRong(), { chu: 'x'.repeat(400), buoi: 0 });
  assert.ok(hs.baiHoc[0].chu.length <= BAI_HOC_TOI_DA_CHU);
});

test('nút bé ĐÃ THẠO thì mục về nút ấy bị dọn', () => {
  /* Nhắc lại chỗ bé đã qua là vừa tốn chỗ vừa nói sai về bé. */
  const hs = {
    ...hoSoRong(),
    baiHoc: [{ chu: 'còn mắc chỗ này', nut: 'x', hetHanBuoi: 99 },
             { chu: 'chỗ khác', nut: 'y', hetHanBuoi: 99 }],
    loiLap: [{ chu: 'a', nut: 'x' }, 'is'],
  };
  const ra = donHoSo(hs, { mucThao: { x: { p: NGUONG_THAO + 0.05 }, y: { p: 0.2 } }, buoiHienTai: 1 });
  assert.equal(ra.baiHoc.length, 1);
  assert.equal(ra.baiHoc[0].nut, 'y');
  assert.deepEqual(ra.loiLap, ['is'], 'lỗi ở nút đã thạo phải đi, chuỗi trần thì ở lại');
});

test('trần KÝ TỰ và trần SỐ PHẦN TỬ', () => {
  const hs = {
    ...hoSoRong(),
    soThich: Array.from({ length: 20 }, (_, i) => `so-thich-rat-dai-so-${i}`),
    cauDungGanNhat: Array.from({ length: 20 }, (_, i) => `Mot cau rat dai so ${i}.`),
    baiHoc: Array.from({ length: 20 }, () => ({ chu: 'y'.repeat(150), nut: null, hetHanBuoi: 99 })),
    buoiThu: 1,
  };
  const ra = donHoSo(hs, { buoiHienTai: 1 });
  assert.ok(JSON.stringify(ra).length <= TRAN_KY_TU,
    `hồ sơ ${JSON.stringify(ra).length} ký tự, quá trần ${TRAN_KY_TU}`);
  for (const [k, n] of Object.entries(TRAN_PHAN_TU)) {
    assert.ok((ra[k] || []).length <= n, `${k} có ${ra[k].length} mục, quá trần ${n}`);
  }
});

test('hình dạng CỐ ĐỊNH — mọi trường đều có, kể cả khi rỗng', () => {
  const kh = Object.keys(hoSoRong()).sort();
  assert.deepEqual(Object.keys(donHoSo(hoSoRong(), {})).sort(), kh);
  assert.deepEqual(Object.keys(capNhatTuBuoi(null, {})).sort(), kh);
  assert.deepEqual(Object.keys(themBaiHoc(null, { chu: 'x' })).sort(), kh);
  assert.deepEqual(Object.keys(xoaHoSoAI()).sort(), kh);
});

/* ═══════════ 3 · KHỐI LỜI DẶN ═══════════ */

const DAY_DU = () => donHoSo(themBaiHoc(capNhatTuBuoi(hoSoRong(), {
  lichSu: [beNoi({ diem: 9, mau: 'I like fish.' }),
           beNoi({ thieuChucNang: ['a'] }), beNoi({ thieuChucNang: ['a'] }),
           beNoi({ diem: 2, nhamThanh: 'milk', mau: 'fish' })],
  hoSo: { thich: 'fish' }, bayGio: 1,
}), { chu: 'Con hay quên chữ "a" trước danh từ.', buoi: 1 }), { buoiHienTai: 1 });

test('dongHoSoAI: không số, ≤ 8 dòng, đọc to lên cũng không sao', () => {
  const s = dongHoSoAI(DAY_DU(), 'Bo');
  assert.ok(s, 'hồ sơ đầy đủ mà không ra dòng nào');
  assert.ok(!/\d/.test(s), `có chữ số: ${s}`);
  assert.ok(s.split('\n').length <= 8, `${s.split('\n').length} dòng, quá 8`);
  /* Quy ước của `dongHoSo`: KHÔNG nhắc điểm trước mặt bé — mô hình rất dễ nhại
     nguyên văn, và "Con được 42%" thì không phải câu đọc to lên được. */
  for (const x of [/score/i, /percent/i, /%/, /\bmark\b/i, /lazy/i, /\bweak\b/i]) {
    assert.ok(!x.test(s), `lọt chữ không được nói trước mặt bé: ${x}`);
  }
});

test('chữ số do mô hình viết cũng bị cắt — cắt ở ĐÚNG một chỗ', () => {
  /* Bài học do mô hình viết (Reflexion) là đường dễ lọt số nhất. Lọc ở từng dòng
     thì thêm một dòng mới mà quên lọc là con số vào thẳng lời dặn. */
  const hs = themBaiHoc({ ...hoSoRong(), buoiThu: 1 },
    { chu: 'Con nói đúng 7 trên 10 câu hôm nay, 70%.', buoi: 1 });
  const s = dongHoSoAI(hs, 'Bo');
  assert.ok(!/\d/.test(s), `số lọt vào lời dặn: ${s}`);
  assert.ok(!s.includes('%'));
});

test('buổi ĐẦU thì không có khối nào — đừng dựng khối rỗng', () => {
  assert.equal(dongHoSoAI(hoSoRong(), 'Bo'), '');
  assert.equal(dongHoSoAI(null, 'Bo'), '');
  const d = loiDan({ von: VON, tenBe: 'Bo', lop: 1, hoSo: { thich: 'fish' } });
  assert.ok(!d.includes('ABOUT THIS CHILD'));
});

test('buổi THỨ HAI thì lời dặn có khối, và xoá xong thì hết', () => {
  const hs = DAY_DU();
  const co = loiDan({ von: VON, tenBe: 'Bo', lop: 1, hoSo: { thich: 'fish', ai: hs } });
  assert.match(co, /ABOUT THIS CHILD/);
  assert.match(co, /fish/, 'phải mang theo ít nhất một mục từ buổi trước');

  const het = loiDan({ von: VON, tenBe: 'Bo', lop: 1, hoSo: { thich: 'fish', ai: xoaHoSoAI() } });
  assert.ok(!het.includes('ABOUT THIS CHILD'), 'bố mẹ xoá rồi mà khối vẫn còn');
});

/* ═══════════ 4 · KHÔNG LỌT VÀO VÂN TAY ═══════════ */

test('khối RIÊNG bị locKhung bỏ SẠCH — hai bé khác nhau, một vân tay', () => {
  assert.equal(DAU_KHOI_RIENG, KHOI_RIENG.mo, 'dấu mở lệch giữa hai tệp');
  assert.equal(CUOI_KHOI_RIENG, KHOI_RIENG.dong, 'dấu đóng lệch giữa hai tệp');

  const mk = (ten, thich, cau) => loiDan({
    von: VON, tenBe: ten, lop: 1,
    hoSo: { thich, mucNam: 'yeu', ai: capNhatTuBuoi(hoSoRong(), {
      lichSu: [beNoi({ diem: 9, mau: cau })], hoSo: { thich }, bayGio: 1 }) },
  });
  const a = mk('Lan', 'fish', 'I like fish.');
  const b = mk('Minh', 'milk', 'I like milk.');
  assert.equal(locKhung(a), locKhung(b),
    'vân tay đổi theo bé → vừa không gom lại được để so mẫu, vừa thành mã theo dõi');
  assert.equal(vanTay('luyennoi', locKhung(a)).vanTayPrompt,
    vanTay('luyennoi', locKhung(b)).vanTayPrompt);
  /* ⚠ ĐỪNG SOI MẤY CHỮ TRÙNG VỚI VỐN TỪ CỦA BÀI. `fish` · `milk` · `I like fish.`
     đều có mặt trong khung một cách HỢP LỆ — chúng nằm ở bảng vốn và bảng mẫu câu
     của luật 1 · 2, và bảng ấy LÀ khung: `vantay.js` nói rõ "hai bé khác nhau học
     CÙNG unit cho ra CÙNG một vân tay", nên dữ liệu của BÀI phải ở lại.
     Thứ phải mất là thứ riêng của BÉ và không trùng với bài: tên bé, và cả khối
     hồ sơ. (Phép soi đầu tiên của tôi đòi cả `fish` phải mất — nó đỏ, và nó đỏ
     ĐÚNG: đòi sai thứ.) */
  for (const x of ['Lan', 'Minh', 'ABOUT THIS CHILD', 'ABOUT THE CHILD',
                   KHOI_RIENG.mo, KHOI_RIENG.dong]) {
    assert.ok(!locKhung(a).includes(x), `khung còn giữ "${x}"`);
  }
  /* Nhưng KHUNG phải còn thật, không phải chuỗi rỗng — băm chuỗi rỗng thì mọi mẫu
     ra cùng một vân tay và phép so chết lặng. */
  assert.ok(locKhung(a).length > 500, 'khung ngắn bất thường, có phải lọc mất cả khối luật?');
  assert.match(locKhung(a), /HARD RULES/);
});

test('TÊN BÉ không được nằm ở dòng khung', () => {
  /* Dòng đầu lời dặn xưa ghi "…Vietnamese child named Lan." — `locKhung` không có
     cách nào nhận ra nó là dữ liệu riêng mà không ghim vào chính tả. Nay tên bé chỉ
     còn trong khối `<<RIENG`. */
  const d = loiDan({ von: VON, tenBe: 'Quynhanh', lop: 1 });
  assert.match(d, /name is Quynhanh/, 'cô vẫn phải biết bé tên gì');
  assert.ok(!locKhung(d).includes('Quynhanh'), 'tên bé lọt vào vân tay');
});

/* ═══════════ 5 · SỔ TIẾN ĐỘ ═══════════ */

test('gộp sổ: bản có capNhatLuc MỚI HƠN thắng, không trộn hai bên', () => {
  /* ⚠ Không gộp hai bên như `dinhDang`: hồ sơ là một BẢN CHỤP của cả trí nhớ, trộn
     ra một hồ sơ chưa từng tồn tại — bài học của bản này, hạn dùng của bản kia. */
  const a = { ...soRong(), hoSoAI: { ...hoSoRong(), soThich: ['fish'], capNhatLuc: 100 } };
  const b = { ...soRong(), hoSoAI: { ...hoSoRong(), soThich: ['milk'], capNhatLuc: 200 } };
  assert.deepEqual(gopTienDo(a, b).hoSoAI.soThich, ['milk']);
  assert.deepEqual(gopTienDo(b, a).hoSoAI.soThich, ['milk']);
  /* Một bên rỗng thì lấy bên có. */
  assert.deepEqual(gopTienDo({ ...soRong() }, b).hoSoAI.soThich, ['milk']);
  assert.deepEqual(gopTienDo(a, { ...soRong() }).hoSoAI.soThich, ['fish']);
  assert.equal('hoSoAI' in soRong(), true, 'sổ rỗng phải khai sẵn trường này');
});

test('bốn chỗ phải khớp nhau khi thêm loại vào học bạ', () => {
  /* Ghi ở `firestore.rules`: thêm một loại là phải sửa BỐN chỗ. Cổng
     `hocba_khop_luat.test.mjs` soi ba chỗ đầu; chỗ này soi riêng `hoSoAI` để nếu ai
     gỡ một đầu thì biết ngay là gỡ đầu nào. */
  const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
  assert.match(doc('../firestore.rules'), /'hoSoAI'/, 'luật Firestore chưa cho loại này');
  assert.match(doc('../src/mon/tienganh/lib/duLieu.js'), /v\.loai === 'hoSoAI'/,
    'bên đọc chưa nhặt — ghi lên rồi bỏ đó');
  assert.match(doc('../src/mon/tienganh/lib/duLieu.js'), /hoSoAI: hb\.hoSoAI/,
    'đọc được mà không chuyền lên sổ — bé đổi máy là cô quên sạch');
  assert.match(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'),
    /luuMucHocBa\(learnerId, 'hoSoAI'/, 'màn hình chưa đẩy lên máy chủ');
});

test('ghi hồ sơ ĐÚNG MỘT LẦN mỗi buổi', () => {
  /* `buoi.trangThai` được tính lại mỗi nhịp 30 giây và mỗi lượt. Không chốt thì
     `buoiThu` tăng vài lần cho đúng một buổi, rồi bài học hết hạn sớm hơn hẳn — mà
     chẳng ai lần ra, vì con số vẫn trông hợp lý. */
  const pn = readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8');
  assert.match(pn, /daGhiHoSo\.current/, 'không có chốt ghi một lần');
  assert.match(pn, /luotLuyen\(lichSu\)\.length/,
    'mở ra rồi thoát ngay cũng ghi một buổi — buổi ấy không có gì để nhớ');
});
