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
  changCua, trangThaiChang, duocBoQua, conNoTrongMuc, viecChangTu, viecChangCau,
  noiDuoc, NHAN_CHANG, CHANG_KHONG_KHOA,
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
  assert.deepEqual(changCua(coNoi), ['tu', 'cau', 'luyen', 'noi', 'sat', 'phong']);
  assert.deepEqual(changCua(khong), ['tu', 'cau', 'luyen', 'sat', 'phong']);
  /* Kịch bản khai rỗng cũng phải tính là KHÔNG có, nếu không chặng nói chuyện mở
     ra một màn trắng và bé kẹt ở đó. */
  assert.deepEqual(changCua({ knowledgeCore: { hoiThoai: { luot: [] } } }),
                   ['tu', 'cau', 'luyen', 'sat', 'phong']);
  /* Chặng nào cũng phải có nhãn, nếu không thanh chặng hiện một nút trống. */
  for (const k of changCua(coNoi)) assert.ok(NHAN_CHANG[k], `chặng "${k}" chưa có nhãn`);
});

test('PHÒNG LUYỆN NÓI mở sẵn, không phải cửa ải', () => {
  /* Bắt bé qua sát hạch mới được vào thì đúng những bé cần tập nói nhất lại là
     những bé không vào được. */
  const ds = changCua({ knowledgeCore: {} });          // tu · cau · luyen · sat · phong
  const iPhong = ds.indexOf('phong');
  assert.equal(trangThaiChang(iPhong, 0, 0, ds), 'mo', 'phòng nói phải mở từ đầu');
  assert.equal(trangThaiChang(ds.indexOf('sat'), 0, 0, ds), 'khoa', 'sát hạch thì vẫn khoá');
  assert.ok(CHANG_KHONG_KHOA.has('phong'));
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

test('quyển ta1 MỞ mọi unit — bé tự chọn bài', () => {
  /* Bác đổi ý 13-08: "cho các con vào chọn unit để học chứ không nhất thiết phải
     học tuần tự từ bài 1". Nên `khoaBai` của ta1 nay là `false`.

     Đây KHÔNG phải gỡ bỏ luật đi lần lượt — nó chỉ tắt ở TẦNG 1 (bài trong quyển).
     Hai tầng còn lại giữ nguyên và vẫn có cổng canh ở trên: chặng trong bài vẫn
     khoá tuần tự, câu trong mức vẫn ba nấc. Kỳ ôn tập chương vẫn đòi đủ bốn bài
     của chương — đó mới là chỗ đòi món nợ.

     Vẫn phải soi CHÍNH tệp sổ: cờ khai một đằng mà màn hình đọc một nẻo thì cổng
     xanh còn app vẫn khoá, đúng kiểu hỏng đã dính ở `soMon.js`. */
  const ct = JSON.parse(readFileSync(new URL('../public/content/chuong_trinh.json', import.meta.url)));
  assert.equal(ct.chuongTrinh.ta1.khoaBai, false);
  assert.equal(ct.chuongTrinh.ta1.bai.length, 16, 'thứ tự học phải đủ 16 bài');
  /* Tắt khoá mà vẫn phải giữ ĐÚNG THỨ TỰ trong sổ: thẻ "Bài tiếp theo" suy từ
     danh sách này, mất thứ tự thì nó chỉ lung tung. */
  assert.equal(trangThaiBai({ micros: {} }, ct.chuongTrinh.ta1.bai[7], ct.chuongTrinh.ta1.bai,
                            { khoaBai: false }), 'mo',
    'bài giữa quyển phải mở sẵn khi tắt khoá');
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
     ra thẳng sát hạch. Cổng soi chỗ dựng nút, chứ hành vi thì phải đi thử thật.

     Đếm `tat={!...}` chứ không đếm đúng tên biến: bản trước ghim `tat={!moKhoa}`,
     nên lúc chặng Từ mới đổi tên biến sang `mo` là cổng kêu oan. Cổng phải canh
     VIỆC (nút có khoá được không), đừng canh CHỮ — xem bẫy #11. */
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  const soLanTat = (bh.match(/tat=\{!\w+\}/g) || []).length;
  assert.equal(soLanTat, 2, 'cả chặng TỪ MỚI và chặng MẪU CÂU đều phải khoá nút đi tiếp');
  assert.match(bh, /viSao=/, 'nút xám phải kèm một dòng nói vì sao');
});

/* ═══════════ TẦNG 2b · VIỆC CỦA CON TRONG CHẶNG TỪ MỚI ═══════════ */

/**
 * Thanh việc sinh ra vì điều kiện đi tiếp trước đây chỉ được nói bằng MỘT DÒNG
 * CHỮ — mà bé lớp 1 chưa đọc được. Nhóm này canh hai thứ:
 *
 *   1. thanh có đếm đúng việc còn thiếu không (bé nhìn vào phải tin được);
 *   2. đường "micro hỏng thì tự mở" có còn không.
 *
 * Cái thứ hai mới là cái phải canh kỹ: nó CHỈ chạy khi có sự cố, nên đi thử tay
 * gần như không bao giờ chạm tới — đúng chỗ sáu lỗi câm đợt trước đã nấp.
 */
const BA_TU = [
  { tu: 'ball', nghia: 'quả bóng' },
  { tu: 'bike', nghia: 'xe đạp' },
  { tu: 'book', nghia: 'quyển sách' },
];
const tuMoi = (t = {}) => viecChangTu({ dsTu: BA_TU, coVideo: true, ...t });

/* Sổ nói: `dat(...)` là nói đạt điểm, `thu(...)` là thử thật đủ lần mà chưa đạt. */
const dat = (...tu) => Object.fromEntries(tu.map((t) => [t, { caoNhat: 8, lan: 1 }]));
const thu = (...tu) => Object.fromEntries(tu.map((t) => [t, { caoNhat: 3, lan: THU_TOI_THIEU }]));
const BA = ['ball', 'bike', 'book'];

test('sổ trắng: mọi ô đều chưa làm, và nút đi tiếp đóng', () => {
  const r = tuMoi();
  assert.equal(r.mo, false);
  assert.equal(r.viec.length, 4, 'một ô video + ba ô từ');
  assert.equal(r.conThieu, 4);
  assert.ok(r.viec.every((x) => x.tt === 'chua'));
});

test('ô nhúc nhích NGAY lần bấm đầu, chưa cần xong cả hai việc', () => {
  /* Nghe xong một từ mà ô vẫn trắng thì công vừa bỏ ra không để lại dấu gì — và
     đó đúng là lúc bé bỏ cuộc. */
  const r = tuMoi({ daNghe: ['ball'] });
  const o = r.viec.find((x) => x.ma === 'ball');
  assert.equal(o.tt, 'dang');
  assert.equal(o.daNghe, true);
  assert.equal(o.daNoi, false);
});

test('một từ chỉ XONG khi đã nghe VÀ đã nói', () => {
  assert.equal(tuMoi({ daNghe: ['ball'] }).viec.find((x) => x.ma === 'ball').tt, 'dang');
  assert.equal(tuMoi({ soNoi: dat('ball') }).viec.find((x) => x.ma === 'ball').tt, 'dang');
  assert.equal(
    tuMoi({ daNghe: ['ball'], soNoi: dat('ball') }).viec.find((x) => x.ma === 'ball').tt,
    'xong',
  );
});

/* ── ngưỡng "đã nói được": đạt HOẶC đã thử thật 2 lần ── */

test('nói đạt điểm thì tính là nói được', () => {
  assert.equal(noiDuoc({ caoNhat: 6, lan: 1 }), 'dat');
  assert.equal(noiDuoc({ caoNhat: 9, lan: 1 }), 'dat');
});

test('chưa đạt mà đã thử thật đủ lần thì VẪN đi tiếp được', () => {
  /* Bé ngọng, bé nói giọng miền, micro rẻ — cả ba đều có thể không bao giờ chạm
     ngưỡng. Khoá cứng theo "phải đạt" thì bé tắc là tắc vĩnh viễn. */
  assert.equal(noiDuoc({ caoNhat: 2, lan: THU_TOI_THIEU }), 'thu');
  assert.equal(noiDuoc({ caoNhat: 0, lan: THU_TOI_THIEU }), 'thu');
});

test('thử một lần rồi bỏ thì CHƯA tính', () => {
  assert.equal(noiDuoc({ caoNhat: 3, lan: 1 }), 'chua');
  assert.equal(noiDuoc(), 'chua');
  assert.equal(noiDuoc({}), 'chua');
});

test('ngưỡng "đã nói" dùng lại ĐÚNG con số của luật ba tầng', () => {
  /* Cắm số 2 riêng cho phần nói thì mai kia đổi luật một chỗ, ba chỗ kia lệch. */
  assert.equal(noiDuoc({ caoNhat: 0, lan: THU_TOI_THIEU - 1 }), 'chua');
  assert.equal(noiDuoc({ caoNhat: 0, lan: THU_TOI_THIEU }), 'thu');
});

test('thanh phân biệt ⭐ đạt với ✓ mới thử thật', () => {
  const r = tuMoi({ daNghe: BA, soNoi: { ...dat('ball'), ...thu('bike') } });
  assert.equal(r.viec.find((x) => x.ma === 'ball').mucNoi, 'dat');
  assert.equal(r.viec.find((x) => x.ma === 'bike').mucNoi, 'thu');
  assert.equal(r.viec.find((x) => x.ma === 'book').mucNoi, 'chua');
});

test('cả ba từ mới thử thật mà chưa đạt thì VẪN mở được chặng', () => {
  assert.equal(tuMoi({ daNghe: BA, soNoi: thu(...BA) }).mo, true);
});

test('nghe đủ mọi từ mà CHƯA NÓI thì vẫn chưa được đi tiếp', () => {
  /* Đây là đổi mới so với bản trước: nghe xong là đi được, nên phần nói thành
     thứ trang trí và bé không bao giờ mở miệng. */
  const r = tuMoi({ daNghe: BA });
  assert.equal(r.mo, false);
  assert.equal(r.conThieu, 4, 'ba từ còn thiếu việc nói, cộng ô video chưa xem');
});

test('xem hết video vẫn chưa đủ — video không nói hộ được phần nói', () => {
  assert.equal(tuMoi({ daXem: true }).mo, false);
});

test('nghe đủ và nói đủ thì mở, không cần xem video', () => {
  const r = tuMoi({ daNghe: BA, soNoi: dat(...BA) });
  assert.equal(r.mo, true);
  assert.equal(r.conThieu, 1, 'chỉ còn ô video, mà ô ấy không chặn đường');
});

test('xem hết video và nói đủ thì mở, không cần bấm nghe từng từ', () => {
  assert.equal(tuMoi({ daXem: true, soNoi: dat(...BA) }).mo, true);
});

test('VIDEO HỎNG không được để bé kẹt', () => {
  const r = tuMoi({ videoHong: true, soNoi: dat(...BA) });
  assert.equal(r.mo, true);
  assert.equal(r.viec[0].tt, 'hong', 'ô video phải mang dáng riêng, không phải "xong"');
  assert.equal(r.conThieu, 3, 'ô hỏng không tính là việc bé còn nợ');
});

test('MICRO HỎNG mở đường ngay — đường này chỉ chạy khi có sự cố', () => {
  /* Micro hỏng vì lý do chẳng liên quan gì tới bé: máy không có micro, chưa được
     cho phép, hoặc mất mạng. Bé kẹt vì mấy thứ ấy là rơi đúng cái bẫy mà
     THU_TOI_THIEU sinh ra để tránh. */
  const r = tuMoi({ daNghe: BA, micHong: true });
  assert.equal(r.mo, true);
  assert.equal(r.vuongMicro, true, 'phải báo lên để màn hình nói rõ là do máy');
  const o = r.viec.find((x) => x.ma === 'ball');
  assert.equal(o.boQuaNoi, true);
  assert.equal(o.daNoi, false, 'micro hỏng KHÔNG được ghi khống là bé đã nói');
});

test('micro hỏng mà chưa nghe gì thì VẪN đóng', () => {
  /* Micro hỏng chỉ tha cho việc NÓI. Tha luôn cả việc nghe là mở toang chặng. */
  assert.equal(tuMoi({ micHong: true }).mo, false);
});

test('micro hỏng nhưng bé nói được hết thì không kêu ca gì', () => {
  const r = tuMoi({ daNghe: BA, soNoi: dat(...BA), micHong: true });
  assert.equal(r.vuongMicro, false);
});

test('bài không có video thì không mọc ra ô video trắng', () => {
  const r = viecChangTu({ dsTu: BA_TU, coVideo: false });
  assert.equal(r.viec.length, 3);
  assert.equal(r.mo, false, 'vẫn phải nghe và nói đủ');
});

test('im lặng ba lần KHÔNG được tính là đã nói', () => {
  /* `NutNoi` chỉ báo `coTieng` khi máy nghe ra chữ; `no-speech` thì không. Thiếu
     chốt ấy là bé bấm mấy cái trong im lặng rồi qua chặng. Cổng soi chỗ nối. */
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  assert.match(bh, /kq\?\.coTieng/, 'chỉ ghi "đã nói" khi máy thật sự nghe ra tiếng');
  const nn = readFileSync(new URL('../src/mon/tienganh/components/NutNoi.jsx', import.meta.url), 'utf8');
  assert.match(nn, /coTieng:/, 'NutNoi phải báo lên là có nghe ra tiếng hay không');
  assert.match(nn, /onHong\?\.\(/, 'trục trặc thuộc về MÁY phải báo lên trên');
});

test('thẻ từ và thanh việc hỏi hình qua HÀM CHUNG', () => {
  /* Đã dính thật lúc dựng: thanh việc tự đọc `v.ve`/`v.hinh` từ `vocabulary` —
     hai trường ấy không tồn tại ở đó, hình nằm ở `bai.hinhTu`. Kết quả: cả bốn ô
     vẽ ra dấu ❔ trong khi thẻ từ ngay dưới vẫn đủ hình. Cổng xanh, bản dựng xanh,
     chỉ có nhìn mới thấy.

     Nay có BA chỗ vẽ hình từ (thẻ từ · thanh việc · phòng luyện nói), nên nguồn
     dọn hẳn sang `lib/noiDung.js`. Phép đếm "đúng một chỗ được đụng `bai.hinhTu`"
     chuyển sang `tienganh_phongnoi.test.mjs` vì nó phải soi cả ba tệp; ở đây chỉ
     còn canh hai chỗ gọi trong chính tệp này. */
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  assert.match(bh, /hinhCuaTu\(bai, v\.tu\)/, 'thẻ từ phải hỏi qua hàm chung');
  assert.match(bh, /\.\.\.hinhCuaTu\(bai, v\.tu\)\s*\}\)\)/, 'thanh việc cũng phải hỏi qua hàm chung');
});

/* ── chặng MẪU CÂU: cùng khuôn, cùng luật ── */

const HAI_MAU = [
  { tep: 'b01_cau1.mp4', cau: "Hi, I'm Bill.", vai: 'cau' },
  { tep: 'b01_cau2.mp4', cau: 'Bye, Bill.', vai: 'cau' },
];
const mauCau = (t = {}) => viecChangCau({ dsCau: HAI_MAU, ...t });
const datC = (...c) => Object.fromEntries(c.map((x) => [x, { caoNhat: 8, lan: 1 }]));

test('mẫu câu: sổ trắng thì mỗi mẫu một ô, cả hai còn trắng', () => {
  const r = mauCau();
  assert.equal(r.viec.length, 2);
  assert.equal(r.conThieu, 2);
  assert.equal(r.mo, false);
  assert.deepEqual(r.viec[0].viecCon.map((c) => c.ma), ['xem', 'noi']);
});

test('mẫu câu: XEM ĐỦ mà chưa nói thì CHƯA được đi tiếp', () => {
  /* Đây là chỗ đổi so với bản trước — bản trước chỉ đòi xem hết video, nên ô nói
     thành thứ trang trí y hệt chuyện đã xảy ra ở chặng Từ mới. */
  const r = mauCau({ daXem: HAI_MAU.map((c) => c.tep) });
  assert.equal(r.mo, false);
});

test('mẫu câu: nói đủ mà chưa xem cũng CHƯA được đi tiếp', () => {
  assert.equal(mauCau({ soNoi: datC("Hi, I'm Bill.", 'Bye, Bill.') }).mo, false);
});

test('mẫu câu: xem đủ VÀ nói đủ thì mở', () => {
  const r = mauCau({
    daXem: HAI_MAU.map((c) => c.tep),
    soNoi: datC("Hi, I'm Bill.", 'Bye, Bill.'),
  });
  assert.equal(r.mo, true);
  assert.equal(r.conThieu, 0);
});

test('mẫu câu: VIDEO HỎNG không để bé kẹt, nhưng vẫn phải nói', () => {
  assert.equal(mauCau({ videoHong: true }).mo, false, 'video hỏng không tha việc nói');
  assert.equal(
    mauCau({ videoHong: true, soNoi: datC("Hi, I'm Bill.", 'Bye, Bill.') }).mo, true,
  );
});

test('mẫu câu: MICRO HỎNG tha việc nói, KHÔNG tha việc xem', () => {
  assert.equal(mauCau({ micHong: true }).mo, false, 'chưa xem thì vẫn đóng');
  const r = mauCau({ micHong: true, daXem: HAI_MAU.map((c) => c.tep) });
  assert.equal(r.mo, true);
  assert.equal(r.vuongMicro, true);
  assert.equal(r.viec[0].daNoi, false, 'micro hỏng KHÔNG được ghi khống là bé đã nói');
});

test('mẫu câu: ngưỡng nói dùng CHUNG một luật với chặng Từ mới', () => {
  const daXem = HAI_MAU.map((c) => c.tep);
  const thuThat = { caoNhat: 1, lan: THU_TOI_THIEU };
  const r = mauCau({ daXem, soNoi: { "Hi, I'm Bill.": thuThat, 'Bye, Bill.': thuThat } });
  assert.equal(r.mo, true, 'thử thật đủ lần mà chưa đạt vẫn qua được');
  assert.equal(r.viec[0].mucNoi, 'thu');
});

test('hai chặng cùng sinh ra MỘT hình dạng ô', () => {
  /* ThanhViec chỉ vẽ, không được biết đang ở chặng nào. Hai bên lệch hình dạng
     thì thanh phải mọc thêm nhánh `if`, và nhánh ấy là chỗ lỗi câm sẽ nấp. */
  const a = tuMoi().viec.at(-1);
  const b = mauCau().viec.at(-1);
  for (const k of ['ma', 'loai', 'nhan', 'tt', 'viecCon', 'mucNoi', 'boQuaNoi']) {
    assert.ok(k in a, `ô chặng Từ mới thiếu "${k}"`);
    assert.ok(k in b, `ô chặng Mẫu câu thiếu "${k}"`);
  }
  assert.deepEqual(Object.keys(a.viecCon[1]).sort(), Object.keys(b.viecCon[1]).sort());
});

test('dãy chấm phân biệt bốn dáng bằng HÌNH, không chỉ bằng màu', () => {
  const tc = readFileSync(new URL('../src/mon/tienganh/components/ThanhCau.jsx', import.meta.url), 'utf8');
  assert.match(tc, /border-dashed/, 'chấm chưa tới phải khác về nét');
  assert.match(tc, /aria-label=\{chu\}/, 'mỗi chấm phải tự nói nó là câu mấy, trạng thái gì');
  assert.match(tc, /aria-current/, 'phải chỉ ra chỗ bé đang đứng');
});

test('dãy chấm TỰ ẨN khi chỉ có một câu', () => {
  /* Có thật ở Unit 5: hội thoại chỉ có MỘT lượt của bé, và một chấm đơn độc trong
     khung to không nói được gì — bé còn phải đoán xem nó nghĩa là gì. Chặn ở CẢ
     HAI nơi: chính dãy chấm, và cái khung bọc nó (khung rỗng vẫn chiếm chỗ). */
  const tc = readFileSync(new URL('../src/mon/tienganh/components/ThanhCau.jsx', import.meta.url), 'utf8');
  assert.match(tc, /if \(tong < 2\) return null/, 'dãy chấm phải tự ẩn');
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  const ht = readFileSync(new URL('../src/mon/tienganh/components/HoiThoai.jsx', import.meta.url), 'utf8');
  assert.match(bh, /ds\.length > 1 && \(/, 'sát hạch không được để lại khung rỗng');
  assert.match(ht, /luotBe\.length > 1 && \(/, 'nói chuyện không được để lại khung rỗng');
});

test('cả ba chặng nhiều câu đều dùng dãy chấm, không ai tự vẽ lại', () => {
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  const ht = readFileSync(new URL('../src/mon/tienganh/components/HoiThoai.jsx', import.meta.url), 'utf8');
  assert.equal((bh.match(/<ThanhCau/g) || []).length, 2, 'luyện tập và sát hạch');
  assert.match(ht, /<ThanhCau/, 'nói chuyện phải cho bé biết còn mấy lượt của mình');
  assert.doesNotMatch(bh, /Câu \{i \+ 1\}\/\{ds\.length\}/,
    'dòng "Câu 1/5" bằng chữ đã được thay bằng dãy chấm');
});

test('phần luyện từ đi MỘT từ một lượt, và nút NÓI là thứ to nhất', () => {
  /* Bản trước bày cả bốn từ cùng lúc, mỗi thẻ hai nút tròn 🔈 và 🎤 to bằng nhau,
     nên nói trông như một việc ngang hàng với nghe — trong khi video vừa dạy âm
     xong rồi, tới đây NÓI mới là đích. Cổng canh cả hai chỗ dễ trôi ngược. */
  const bh = readFileSync(new URL('../src/mon/tienganh/components/BaiHoc.jsx', import.meta.url), 'utf8');
  assert.match(bh, /Từ \{i \+ 1\} \/ \{ds\.length\}/, 'phải nói rõ đang ở từ thứ mấy');
  assert.doesNotMatch(bh, /vocabulary\.map\(\(v\) => \(\s*<div/,
    'không được quay lại lối bày cả lưới thẻ từ');
  assert.match(bh, /noiBat/, 'ô nói phải dùng dáng nổi bật');

  const nn = readFileSync(new URL('../src/mon/tienganh/components/NutNoi.jsx', import.meta.url), 'utf8');
  assert.match(nn, /noiBat \? 'px-6 py-6 text-2xl'/, 'dáng nổi bật phải TO hơn dáng thường');
});

test('thanh việc bấm được, và không dùng mỗi màu để mang tin', () => {
  const tv = readFileSync(new URL('../src/mon/tienganh/components/ThanhViec.jsx', import.meta.url), 'utf8');
  assert.match(tv, /onChon/, 'bấm vào ô phải tới được chỗ phải làm');
  assert.match(tv, /aria-label=\{nhanDayDu\}/, 'máy đọc màn hình phải nghe đủ việc còn thiếu');
  assert.match(tv, /border-dashed/, 'ô chưa làm phải khác về NÉT, không chỉ khác màu');
});
