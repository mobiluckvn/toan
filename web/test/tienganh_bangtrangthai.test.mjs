/**
 * CỔNG · BẢNG TRẠNG THÁI (mẫu Blackboard, việc V6).
 *
 * Trạng thái của một bé xưa nằm rải ở SÁU chỗ, mỗi màn tự đi gom phần nó cần. Mỗi
 * màn gom một kiểu thì không màn nào thấy đủ, và hai màn có thể nói hai điều khác
 * nhau về cùng một bé. Tệp này canh bốn thứ:
 *
 *   1. dựng ĐỦ TRƯỜNG từ sáu nguồn, và THIẾU thì để RỖNG chứ không đoán;
 *   2. BẤT BIẾN — mọi hàm ghi trả bản mới, không sửa tại chỗ;
 *   3. tóm tắt cho lời dặn ≤ 900 ký tự, KHÔNG số, cắt theo ƯU TIÊN;
 *   4. bốn màn đều đi qua MỘT hàm — `vectorS(` không còn ở đâu khác.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  dungBang, ghiLuot, tomTatChoLoiDan, nutCuaBai,
  TRAN_BANG_KY_TU, TRAN_TOM_TAT, DAU_KHOI_RIENG, CUOI_KHOI_RIENG,
} from '../src/mon/tienganh/lib/bangtrangthai.js';
import { hoSoRong, capNhatTuBuoi, themBaiHoc } from '../src/mon/tienganh/lib/hosoai.js';
import { loiDan, vonTu } from '../src/mon/tienganh/lib/phongnoi.js';
import { locKhung } from '../functions/src/vantay.js';
import { NGUONG_THAO } from '../src/mon/tienganh/lib/zpd.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');

/* ── FIXTURE: một bé, 6 nút, 2 thẻ đến hạn, hồ sơ AI có 1 lỗi lặp ── */
const NAY = 1_700_000_000_000;
const MUC_THAO = {
  n1: { p: 0.9, lastSeen: NAY }, n2: { p: 0.88, lastSeen: NAY },
  n3: { p: 0.92, lastSeen: NAY }, n4: { p: 0.95, lastSeen: NAY },
  n5: { p: 0.9, lastSeen: NAY }, n6: { p: 0.87, lastSeen: NAY },
};
const BAI = {
  id: 'DL:TA1.B05', title: 'Unit 5',
  knowledgeCore: {
    vocabulary: [{ tu: 'fish', nghia: 'cá' }, { tu: 'milk', nghia: 'sữa' }],
    mauCauDs: [{ cau: 'I like fish.', congThuc: 'I like + [Noun].', dungDe: 'để nói' }],
  },
  practice: { pools: {
    nhanBiet: [{ id: 'c1', maNut: 'n1' }, { id: 'c2', maNut: 'n2' }, { id: 'c3', maNut: 'n3' }],
    thongHieu: [{ id: 'c4', maNut: 'n4' }, { id: 'c5', maNut: 'n5' }, { id: 'c6', maNut: 'n6' }],
  } },
};
const THE = [
  { microId: 'DL:TA1.B01', dueAt: NAY - 1000 },
  { microId: 'DL:TA1.B02', dueAt: NAY - 2000 },
  { microId: 'DL:TA1.B03', dueAt: NAY + 9e9 },          // chưa đến hạn
  { microId: 'DL:TA3.B01', dueAt: NAY - 1000 },          // quyển khác
];
const HO_SO_AI = themBaiHoc(capNhatTuBuoi(hoSoRong(), {
  lichSu: [{ vai: 'be', chu: 'x', diem: 9, mau: 'I like fish.', thieu: [], thieuChucNang: [] },
           { vai: 'be', chu: 'x', diem: 4, mau: 'I like milk.', thieu: [], thieuChucNang: ['a'] },
           { vai: 'be', chu: 'x', diem: 4, mau: 'I like milk.', thieu: [], thieuChucNang: ['a'] }],
  hoSo: { thich: 'fish' }, bayGio: NAY,
}), { chu: 'Con hay quên chữ "a" trước danh từ.', buoi: 1 });

const BANG = () => dungBang({
  bai: BAI, mucThao: MUC_THAO, cards: THE, hoSoAI: HO_SO_AI, quyen: 'ta1',
  cauDs: BAI.practice.pools.nhanBiet, thich: 'fish', bayGio: NAY,
});

/* ═══════════ 1 · DỰNG ĐỦ TRƯỜNG ═══════════ */

test('dựng bảng đủ trường từ sáu nguồn', () => {
  const b = BANG();
  assert.ok(Array.isArray(b.nhomZPD), 'thiếu thứ tự ZPD');
  assert.equal(b.nhomZPD.length, 3, 'KHÔNG được bỏ câu nào — chỉ đổi thứ tự');
  assert.equal(b.theDenHan.length, 2, 'thẻ chưa đến hạn và thẻ quyển khác không được tính');
  assert.equal(b.hoSo.mucNam, 'vung', 'sáu nút đều trên ngưỡng thạo');
  assert.equal(b.hoSo.thich, 'fish');
  assert.equal(b.hoSo.ai.loiLap[0], 'a', 'trí nhớ V3 phải vào bảng');
  assert.equal(b.buoiThu, 1);
  assert.equal(b.bai, 'DL:TA1.B05');
  assert.equal(b.quyen, 'ta1');
  /* Đầu buổi thì CHƯA có lượt nào — `null` ở đây là đúng, không phải thiếu sót. */
  assert.equal(b.luotGanNhat, null);
  assert.equal(b.nhanGanNhat, null);
  /* `keHoach` khai sẵn cho V7 — để hình dạng bảng khỏi đổi lần nữa. */
  assert.equal(b.keHoach, null);
  assert.ok(JSON.stringify(b).length <= TRAN_BANG_KY_TU,
    `bảng ${JSON.stringify(b).length} ký tự, quá trần ${TRAN_BANG_KY_TU}`);
});

test('nút gốc rễ dựng được khi có đồ thị', () => {
  const dt = { canh: [{ tu: 'n0', den: 'n1', loai: 'REQUIRES' }] };
  const b = dungBang({ doThi: dt, mucThao: { n1: { p: 0.2 }, n0: { p: 0.1 } }, maNutMac: 'n1' });
  assert.ok(b.nutGocRe, 'có đồ thị và nút mắc thì phải ra một nút gốc rễ');
});

/**
 * ⚠ THIẾU THÌ ĐỂ RỖNG, ĐỪNG ĐOÁN.
 *
 * Một màn chỉ nạp `mucThao` mà bảng tự bịa `theDenHan: []` thì nghe như "không có
 * thẻ nào đến hạn" — trong khi thật ra là "màn này không biết". Hai điều ấy khác
 * nhau, và chỗ đọc phải phân biệt được: `null` là không biết, `[]` là không có.
 */
test('thiếu nguồn thì trường ấy là null, KHÔNG phải mảng rỗng', () => {
  const b = dungBang({ mucThao: MUC_THAO });
  assert.equal(b.theDenHan, null, 'không có `cards` thì không được nói "không thẻ nào"');
  assert.equal(b.nhomZPD, null, 'không có kho câu thì không được nói "không câu nào"');
  assert.equal(b.nutGocRe, null);
  /* Và có `cards` mà không thẻ nào đến hạn thì ĐÚNG là `[]`. */
  assert.deepEqual(dungBang({ cards: [{ microId: 'x', dueAt: NAY + 9e9 }], bayGio: NAY }).theDenHan, []);
});

test('dựng bảng rỗng cũng không vỡ', () => {
  const b = dungBang();
  assert.equal(b.buoiThu, 0);
  assert.equal(b.hoSo.mucNam, null);
  assert.equal(tomTatChoLoiDan(b), '', 'không biết gì thì đừng dựng khối rỗng');
});

test('nutCuaBai gom đúng mã nút, không trùng', () => {
  assert.deepEqual(nutCuaBai(BAI).sort(), ['n1', 'n2', 'n3', 'n4', 'n5', 'n6']);
  assert.deepEqual(nutCuaBai(null), []);
});

/* ═══════════ 2 · BẤT BIẾN ═══════════ */

test('ghiLuot trả BẢN MỚI, không sửa bảng cũ', () => {
  /* ⚠ Lý do thực tế, không phải sạch sẽ cho vui: bảng đi vào `useMemo`/`useEffect`
     của React. Sửa tại chỗ thì React không thấy nó đổi — màn vẽ lại bằng dữ liệu
     cũ, và chỗ hỏng ấy không hiện thành một lỗi, chỉ thành "sao cô không biết con
     vừa nói gì". */
  const b = BANG();
  const truoc = JSON.stringify(b);
  const b2 = ghiLuot(b, { vai: 'be', chu: 'x', diem: 4 }, 'thieuTu');
  assert.notEqual(b, b2, 'phải là hai đối tượng khác nhau');
  assert.equal(JSON.stringify(b), truoc, 'bảng cũ bị sửa tại chỗ');
  assert.equal(b2.nhanGanNhat, 'thieuTu');
  assert.equal(b2.luotGanNhat.diem, 4);
  /* Mọi trường khác giữ nguyên. */
  assert.equal(b2.buoiThu, b.buoiThu);
  assert.deepEqual(b2.theDenHan, b.theDenHan);
});

test('ghiLuot trên bảng null vẫn ra một bảng dùng được', () => {
  const b = ghiLuot(null, null, 'moDau');
  assert.equal(b.nhanGanNhat, 'moDau');
  assert.ok('hoSo' in b && 'keHoach' in b);
});

/* ═══════════ 3 · TÓM TẮT CHO LỜI DẶN ═══════════ */

test('tomTatChoLoiDan: dưới trần, KHÔNG số, bọc dấu riêng', () => {
  const s = tomTatChoLoiDan(BANG(), 'Bo');
  assert.ok(s.length <= TRAN_TOM_TAT + DAU_KHOI_RIENG.length + CUOI_KHOI_RIENG.length + 2,
    `${s.length} ký tự, quá trần ${TRAN_TOM_TAT}`);
  assert.ok(!/\d/.test(s), `có chữ số: ${s}`);
  assert.ok(s.startsWith(DAU_KHOI_RIENG));
  assert.ok(s.trimEnd().endsWith(CUOI_KHOI_RIENG));
  assert.match(s, /name is Bo/);
  assert.match(s, /solid on this unit/, 'sáu nút đều thạo thì phải nói ra');
  assert.match(s, /due for review/, 'có thẻ đến hạn thì phải nhắc');
});

test('câu sẵn của sách CÓ chữ số cũng bị cắt sạch', () => {
  /* "It's 45 Ba Trieu Street." là câu của chính sách (ta5 unit 2), và nó vào hồ sơ
     qua `cauDungGanNhat`. Cắt chữ số ở ĐÚNG MỘT CHỖ nên nó không lọt. */
  const ai = capNhatTuBuoi(hoSoRong(), {
    lichSu: [{ vai: 'be', chu: 'x', diem: 9, mau: "It's 45 Ba Trieu Street.", thieu: [], thieuChucNang: [] }],
    bayGio: NAY,
  });
  const s = tomTatChoLoiDan(dungBang({ hoSoAI: ai }), 'Bo');
  assert.ok(!/\d/.test(s), `số của sách lọt vào lời dặn: ${s}`);
});

/**
 * CẮT THEO ƯU TIÊN, không cắt bừa. Thứ tự giữ (§7 việc V6): nhãn > ZPD > bài học >
 * sở thích. Tức vượt trần thì SỞ THÍCH đi trước, TÊN BÉ ở lại tới cùng.
 */
test('vượt trần thì cắt từ ƯU TIÊN THẤP lên', () => {
  const ai = { ...hoSoRong(), buoiThu: 3,
    baiHoc: Array.from({ length: 5 }, () => ({ chu: `Mot bai hoc rat dai cua co giao so ${'x'.repeat(120)}`, nut: null, hetHanBuoi: 99 })),
    soThich: ['fish'], cauDungGanNhat: ['I like fish.'] };
  const b = dungBang({ bai: BAI, mucThao: MUC_THAO, cards: THE, hoSoAI: ai,
    quyen: 'ta1', thich: 'fish', bayGio: NAY });
  const s = tomTatChoLoiDan(b, 'Quynhanh');
  assert.ok(s.length <= TRAN_TOM_TAT + 20, `${s.length} ký tự`);
  assert.match(s, /name is Quynhanh/, 'TÊN BÉ phải ở lại tới cùng — ô [Name] cần nó');
  assert.ok(!/they like/.test(s), 'sở thích phải bị bỏ TRƯỚC khi bỏ tên bé');
});

test('khối tóm tắt bị locKhung bỏ SẠCH khỏi vân tay', () => {
  const von = vonTu({ baiNay: BAI });
  const mk = (ten) => loiDan({ von, tenBe: ten, lop: 1,
    bang: dungBang({ bai: BAI, mucThao: MUC_THAO, cards: THE, hoSoAI: HO_SO_AI,
      quyen: 'ta1', thich: 'fish', bayGio: NAY }) });
  const a = mk('Lan'); const b = mk('Minh');
  assert.equal(locKhung(a), locKhung(b), 'vân tay đổi theo bé');
  for (const x of ['Lan', 'Minh', 'ABOUT THE CHILD', 'ABOUT THIS CHILD']) {
    assert.ok(!locKhung(a).includes(x), `khung còn giữ "${x}"`);
  }
  assert.match(locKhung(a), /HARD RULES/, 'lọc mất cả khối luật');
});

test('loiDan nhận CẢ `bang` và `hoSo` rời — đường cũ không được hỏng', () => {
  /* Mọi cổng hiện có truyền `hoSo` đã tính sẵn (họ không có `mucThao`). Bỏ đường ấy
     thì `mucNam`·`dangManh`·`hayQuen`·`deMet` lặng lẽ về null, lời dặn mất mấy dòng,
     và không cổng nào kêu vì chúng chỉ soi `loiDan` với `hoSo`. */
  const von = vonTu({ baiNay: BAI });
  const cu = loiDan({ von, tenBe: 'Bo', lop: 1,
    hoSo: { thich: 'fish', mucNam: 'yeu', dangManh: 'chọn đáp án', hayQuen: true, deMet: true } });
  assert.match(cu, /still shaky/);
  assert.match(cu, /answers best in "chọn đáp án"/);
  assert.match(cu, /not touched some of this for a while/);
  assert.match(cu, /slows down towards the end/);
  assert.match(cu, /they like "fish"/);
  /* Và `hoSo` thiếu trường thì không được xoá mất phần `vectorS` vừa tính. */
  const b = dungBang({ bai: BAI, mucThao: MUC_THAO, hoSo: { thich: 'milk' }, bayGio: NAY });
  assert.equal(b.hoSo.mucNam, 'vung', '`hoSo` thiếu `mucNam` đã xoá mất bản vừa tính');
  assert.equal(b.hoSo.thich, 'milk');
});

/* ═══════════ 4 · BỐN MÀN ĐI QUA MỘT HÀM ═══════════ */

test('vectorS chỉ còn được GỌI ở bangtrangthai.js', () => {
  /* "Định nghĩa XONG" của §7 việc V6. Một màn tự gọi lại là một màn có thể nói
     khác về cùng một bé. */
  for (const p of ['../src/mon/tienganh/components/PhongNoi.jsx',
                   '../src/mon/tienganh/components/BaiHoc.jsx',
                   '../src/mon/tienganh/components/PhuDao.jsx',
                   '../src/mon/tienganh/components/ManTiengAnh.jsx',
                   '../src/mon/tienganh/components/OnLai.jsx']) {
    assert.ok(!/vectorS\(/.test(chiMa(doc(p))), `${p} còn tự gọi vectorS`);
  }
  assert.match(chiMa(doc('../src/mon/tienganh/lib/bangtrangthai.js')), /vectorS\(/);
});

test('bốn màn lấy trạng thái qua dungBang', () => {
  const can = {
    '../src/mon/tienganh/components/PhongNoi.jsx': /dungBang\(\{/,
    '../src/mon/tienganh/components/BaiHoc.jsx': /dungBang\(\{[\s\S]{0,120}cauDs:/,
    '../src/mon/tienganh/components/PhuDao.jsx': /dungBang\(\{[\s\S]{0,80}doThi:/,
    '../src/mon/tienganh/components/ManTiengAnh.jsx': /dungBang\(\{[\s\S]{0,80}cards:/,
  };
  for (const [p, re] of Object.entries(can)) {
    assert.match(chiMa(doc(p)), re, `${p} chưa đi qua bảng`);
  }
  /* Và không màn nào còn gọi thẳng ba hàm nguồn. */
  for (const [p, ten] of [['../src/mon/tienganh/components/BaiHoc.jsx', 'xepTheoZPD'],
                          ['../src/mon/tienganh/components/PhuDao.jsx', 'nutGocRe'],
                          ['../src/mon/tienganh/components/ManTiengAnh.jsx', 'theDenHan']]) {
    assert.ok(!new RegExp(`${ten}\\(`).test(chiMa(doc(p))), `${p} còn gọi thẳng ${ten}`);
  }
});

test('bangtrangthai.js THUẦN — không fetch, không Firebase', () => {
  const src = doc('../src/mon/tienganh/lib/bangtrangthai.js');
  for (const x of [/fetch\(/, /firebase/i, /firestore/i, /nenTang/, /localStorage/]) {
    assert.ok(!x.test(src), `bảng phải thuần, mà có ${x}`);
  }
  /* Cùng đầu vào thì ra cùng một bảng — nhờ `bayGio` tiêm vào, không gọi
     `Date.now()` ngầm giữa thân hàm. */
  assert.deepEqual(BANG(), BANG());
});

test('ngưỡng thạo vẫn là MỘT con số dùng chung', () => {
  /* Bảng không được đặt ngưỡng riêng: hai con số nói về cùng một việc thì sớm muộn
     lệch nhau, và lúc ấy bé "vững" ở màn này mà "yếu" ở màn kia. */
  assert.ok(!/0\.8\d/.test(chiMa(doc('../src/mon/tienganh/lib/bangtrangthai.js'))),
    'có ngưỡng viết thẳng trong bảng — phải dùng NGUONG_THAO của zpd.js');
  assert.equal(NGUONG_THAO, 0.85);
});

/* ═══════════ 5 · HAI CHỖ KÉM CHỈ THẤY KHI ĐỌC LỜI DẶN THẬT ═══════════ */

/**
 * ⚠ ĐỪNG NÓI SỞ THÍCH HAI LẦN. `hoSo.thich` (chọn trong buổi này) và
 * `hoSoAI.soThich` (nhớ từ buổi trước) rất hay là CÙNG MỘT TỪ — V3 và V6 mỗi bên
 * dựng một dòng, và khối ra hai câu gần như y nhau. Chỉ thấy khi in lời dặn thật
 * ra đọc; 96 tệp cổng đều xanh.
 */
test('nhớ được rồi thì KHÔNG nói sở thích hai lần', () => {
  const ai = capNhatTuBuoi(hoSoRong(), {
    lichSu: [{ vai: 'be', chu: 'x', diem: 9, mau: 'I like fish.', thieu: [], thieuChucNang: [] }],
    hoSo: { thich: 'fish' }, bayGio: NAY,
  });
  const trung = tomTatChoLoiDan(dungBang({ hoSoAI: ai, thich: 'fish' }), 'Lan');
  /* ⚠ Soi đúng HAI CÂU KHAI SỞ THÍCH, đừng soi chữ "like fish": câu ví dụ của bài
     ("I like fish.") cũng khớp, và nó ở đó một cách hợp lệ. Phép soi đầu của tôi
     đếm được 2 và đỏ — đỏ vì đòi sai thứ, không vì mã sai. */
  assert.equal((trung.match(/told you (she|they) likes?/g) || []).length, 1,
    `sở thích nói hai lần:\n${trung}`);
  assert.ok(!/The child told you they like "fish"/.test(trung));

  /* Nhưng thích thứ KHÁC với thứ đã nhớ thì phải nói CẢ HAI — bé đổi ý là chuyện
     thường, và dập mất dòng mới là cô dùng sở thích cũ. */
  const khac = tomTatChoLoiDan(dungBang({ hoSoAI: ai, thich: 'milk' }), 'Lan');
  assert.match(khac, /they like "milk"/);
  assert.match(khac, /likes: fish/);
});

test('THỨ TỰ IN khác THỨ TỰ CẮT — và cả hai đều đúng việc của mình', () => {
  /* Dùng luôn thứ tự giữ để in thì khối trí nhớ "ABOUT THIS CHILD" đứng TRƯỚC, rồi
     một dòng sở thích lủng lẳng phía sau nó. Mô hình đọc xuôi từ trên xuống, nên
     dòng rời rạc ở cuối là dòng dễ bị hiểu thành một lệnh mới. */
  const ai = { ...hoSoRong(), buoiThu: 2, soThich: ['fish'] };
  const s = tomTatChoLoiDan(dungBang({ hoSoAI: ai, thich: 'milk', hoSo: { mucNam: 'yeu' } }), 'Lan');
  const iThich = s.indexOf('they like "milk"');
  const iNho = s.indexOf('ABOUT THIS CHILD');
  assert.ok(iThich > -1 && iNho > -1);
  assert.ok(iThich < iNho, 'dòng sở thích phải đứng TRƯỚC khối trí nhớ, không lủng lẳng sau');

  /* Nhưng khi CẮT thì sở thích vẫn là thứ bỏ TRƯỚC — thứ tự in không được kéo theo
     thứ tự cắt. */
  const dai = { ...hoSoRong(), buoiThu: 2,
    baiHoc: Array.from({ length: 5 }, () => ({ chu: 'z'.repeat(150), nut: null, hetHanBuoi: 99 })) };
  const c = tomTatChoLoiDan(dungBang({ hoSoAI: dai, thich: 'milk', hoSo: { mucNam: 'yeu' } }), 'Lan');
  assert.ok(!/they like "milk"/.test(c), 'cắt mà vẫn giữ sở thích — sai thứ tự ưu tiên');
  assert.match(c, /name is Lan/);
});
