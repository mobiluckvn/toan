/**
 * CỔNG · ĐI LẦN LƯỢT — canh cái lỗ mà bác bắt được: "con có thể bỏ qua nhiều bài
 * mà không làm ấy".
 *
 * Lỗ ấy không nằm ở một dòng nào cả, nên không cổng nào bắt được: dữ liệu đủ, bản
 * dựng xanh, mọi màn vẽ đúng. Nó nằm ở chỗ KHÔNG CÓ luật nào — `khoaBai: false`,
 * và nút "Tiếp" bấm là đi. Nên tệp này canh chính cái luật, chứ không canh giao
 * diện: luật ở `lib/dandat.js`, chạy được bằng node.
 *
 * Ba việc phải giữ, và cả ba đều là chỗ dễ bị gỡ ra vì "cho tiện":
 *   1. bài sau chỉ mở khi bài trước ĐẠT hoặc đã THỬ 2 lần;
 *   2. quay lại chặng cũ KHÔNG được làm mất các chặng sau;
 *   3. bỏ qua một câu phải sau khi gợi ý đã hiện, và câu ấy phải để lại dấu.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  THU_TOI_THIEU, HIEN_GOI_Y, daThuDu, moBai, trangThaiBai, baiNenHoc, baiConNo,
  changCua, trangThaiChang, duocBoQua, conNoTrongMuc,
} from '../src/mon/tienganh/lib/dandat.js';

const DS = ['B01', 'B02', 'B03'];
const so = (micros) => ({ micros });

/* ═══════════ TẦNG 1 · BÀI ═══════════ */

test('bài đầu luôn mở, kể cả sổ trắng tinh', () => {
  assert.equal(moBai(so({}), 'B01', DS), true);
  assert.equal(trangThaiBai(so({}), 'B01', DS), 'mo');
});

test('bài sau KHOÁ khi bài trước chưa động tới', () => {
  assert.equal(moBai(so({}), 'B02', DS), false);
  assert.equal(trangThaiBai(so({}), 'B02', DS), 'khoa');
  assert.equal(trangThaiBai(so({}), 'B03', DS), 'khoa');
});

test('ĐẠT bài trước thì mở bài sau — và chỉ MỘT bài sau', () => {
  const p = so({ B01: { pass: true, done: true, attempts: 1 } });
  assert.equal(moBai(p, 'B02', DS), true);
  /* Chỗ này quan trọng: đạt bài 1 KHÔNG được mở luôn bài 3. Nếu `moBai` lỡ đếm
     "có bài nào đạt chưa" thay vì "bài NGAY TRƯỚC đã đạt chưa" thì cả quyển mở
     toang lại từ bài thứ hai trở đi — mà màn hình nhìn vẫn y hệt. */
  assert.equal(moBai(p, 'B03', DS), false);
});

test('THỬ ĐỦ 2 LẦN mà chưa đạt cũng mở bài sau — bé không bị tắc vĩnh viễn', () => {
  const mot = so({ B01: { done: true, pass: false, attempts: 1 } });
  assert.equal(moBai(mot, 'B02', DS), false, 'một lần thì chưa đủ');
  const hai = so({ B01: { done: true, pass: false, attempts: THU_TOI_THIEU } });
  assert.equal(moBai(hai, 'B02', DS), true);
  /* Nhưng đi vòng KHÔNG phải là đạt: bài ấy vẫn nằm trong danh sách còn nợ. */
  assert.equal(trangThaiBai(hai, 'B01', DS), 'chuaDat');
  assert.deepEqual(baiConNo(hai, DS), ['B01']);
});

test('mở lướt một bài rồi thoát KHÔNG tính là đã thử', () => {
  const p = so({ B01: { chang: 2 } });
  assert.equal(daThuDu(p.micros.B01), false);
  assert.equal(moBai(p, 'B02', DS), false);
  assert.equal(trangThaiBai(p, 'B01', DS), 'dangDo');
});

test('bài NÊN HỌC: đang dở trước, rồi tới bài còn nợ, rồi mới tới bài mới', () => {
  assert.equal(baiNenHoc(so({}), DS), 'B01');
  /* Đạt B01 → chỉ sang B02 */
  assert.equal(baiNenHoc(so({ B01: { pass: true, done: true, attempts: 1 } }), DS), 'B02');
  /* B01 còn nợ mà B02 đã mở: vẫn chỉ về B01 trước — món nợ không được trôi đi. */
  const no = so({ B01: { done: true, pass: false, attempts: 2 } });
  assert.equal(baiNenHoc(no, DS), 'B01');
  /* Đang học dở B02 thì về đúng B02, không lôi bé về B01 */
  const do_ = so({ B01: { pass: true, done: true, attempts: 1 }, B02: { chang: 2 } });
  assert.equal(baiNenHoc(do_, DS), 'B02');
});

test('danh sách bài RỖNG thì đóng hết, không mở toang', () => {
  /* Nạp chỉ mục hỏng thì thà không vào được bài nào — thấy ngay là hỏng — còn hơn
     mở cả quyển vì `indexOf` trả -1 rồi bị hiểu thành "không bị chặn". */
  assert.equal(moBai(so({}), 'B01', []), false);
  assert.equal(moBai(so({}), 'khong-co-that', DS), false);
});

test('tắt cờ khoaBai thì không bài nào bị khoá', () => {
  const p = so({});
  assert.equal(trangThaiBai(p, 'B03', DS, { khoaBai: false }), 'mo');
  assert.equal(trangThaiBai(p, 'B03', DS, { khoaBai: true }), 'khoa');
});

/* ═══════════ TẦNG 2 · CHẶNG ═══════════ */

test('chuỗi chặng hỏi CHÍNH BÀI, không cắm số cứng', () => {
  const coNoi = { knowledgeCore: { hoiThoai: { luot: [{ ai: 'be' }] } } };
  const khong = { knowledgeCore: {} };
  assert.deepEqual(changCua(coNoi), ['tu', 'cau', 'luyen', 'noi', 'sat']);
  assert.deepEqual(changCua(khong), ['tu', 'cau', 'luyen', 'sat']);
  /* Kịch bản khai rỗng cũng phải tính là KHÔNG có, nếu không chặng nói chuyện mở
     ra một màn trắng và bé kẹt ở đó. */
  assert.deepEqual(changCua({ knowledgeCore: { hoiThoai: { luot: [] } } }),
                   ['tu', 'cau', 'luyen', 'sat']);
});

test('QUAY LẠI chặng cũ không làm mất chặng sau', () => {
  /* Bé đã đi tới chặng 4, nay đứng ở chặng 1 xem lại từ mới. */
  const tai = 1, xa = 4;
  assert.equal(trangThaiChang(1, tai, xa), 'dang');
  assert.equal(trangThaiChang(0, tai, xa), 'xong');
  /* Đây là chỗ bản cũ hỏng: chặng 2·3·4 phải VẪN MỞ, không khoá lại. */
  assert.equal(trangThaiChang(2, tai, xa), 'xong');
  assert.equal(trangThaiChang(4, tai, xa), 'xong');
});

test('chặng chưa tới thì vẫn khoá', () => {
  assert.equal(trangThaiChang(3, 0, 0), 'khoa');
  assert.equal(trangThaiChang(1, 0, 0), 'khoa');
});

/* ═══════════ TẦNG 3 · CÂU ═══════════ */

test('gợi ý hiện TRƯỚC, nút bỏ qua hiện SAU — không cùng lúc', () => {
  assert.equal(duocBoQua(1), false, 'sai một lần thì chưa được bỏ');
  assert.equal(duocBoQua(HIEN_GOI_Y), false,
    'đúng lúc gợi ý vừa hiện thì CHƯA cho bỏ — nếu không, không bé nào đọc gợi ý '
    + 'khi đáp án nằm ngay bên cạnh');
  assert.equal(duocBoQua(HIEN_GOI_Y + 1), true, 'có gợi ý rồi mà vẫn sai thì cho qua');
  /* Vẫn phải đúng lời bác: "ít nhất 2 lần". */
  assert.ok(HIEN_GOI_Y + 1 > THU_TOI_THIEU);
});

test('câu bỏ qua để lại DẤU, không biến mất', () => {
  const ket = [{ id: 'c1', dung: true }, { id: 'c2', boQua: true },
               { id: 'c3', dung: true }, { id: 'c4', boQua: true }];
  assert.deepEqual(conNoTrongMuc(ket), ['c2', 'c4']);
  assert.deepEqual(conNoTrongMuc([]), []);
});

/* ═══════════ CẮM VÀO THẬT ═══════════ */

test('sổ đăng ký BẬT khoá bài cho quyển ta1', () => {
  /* Luật viết xong mà cờ để `false` thì cổng vẫn xanh còn app vẫn mở toang — đúng
     kiểu hỏng đã dính ở `soMon.js`. Nên phải soi chính tệp sổ. */
  const ct = JSON.parse(readFileSync(new URL('../public/content/chuong_trinh.json', import.meta.url)));
  assert.equal(ct.chuongTrinh.ta1.khoaBai, true);
  assert.equal(ct.chuongTrinh.ta1.bai.length, 16, 'thứ tự học phải đủ 16 bài');
});

test('màn học THẬT SỰ gọi tới luật, không tự viết lại', () => {
  const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');

  const man = doc('../src/mon/tienganh/components/ManTiengAnh.jsx');
  assert.match(man, /from '\.\.\/lib\/dandat\.js'/, 'trang chính phải hỏi luật');
  assert.match(man, /moBai\(/, 'trang chính phải khoá bài theo luật');
  assert.match(man, /ct\?\.khoaBai/, 'phải hỏi CỜ trong sổ, không so tên quyển');

  const bh = doc('../src/mon/tienganh/components/BaiHoc.jsx');
  assert.match(bh, /trangThaiChang\(/, 'thanh chặng phải hỏi luật');
  assert.doesNotMatch(bh, /disabled=\{i > tai\}/,
    'cách khoá cũ chỉ có MỘT con số — quay lại ôn là mất hết chặng sau');

  const ch = doc('../src/mon/tienganh/components/CauHoi.jsx');
  assert.match(ch, /duocBoQua\(/, 'nút bỏ qua phải hỏi luật, không cắm số');
  assert.match(ch, /boQua: !kq\.ok/, 'bỏ qua phải báo lên trên để gom lại làm lại');
});

test('nút đi tiếp của hai chặng XEM đều có thể bị TẮT', () => {
  /* Đây là chính cái lỗ: nút "Tiếp" không đòi hỏi gì thì bé bấm liền mấy cái là
     ra thẳng sát hạch. Cổng soi chỗ dựng nút, chứ hành vi thì phải đi thử thật. */
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  const soLanTat = (bh.match(/tat=\{!moKhoa\}/g) || []).length;
  assert.equal(soLanTat, 2, 'cả chặng TỪ MỚI và chặng MẪU CÂU đều phải khoá nút đi tiếp');
  assert.match(bh, /viSao=/, 'nút xám phải kèm một dòng nói vì sao');
});
