/**
 * CỔNG · KẾ HOẠCH MỘT BUỔI (mẫu Plan-and-Execute, việc V7).
 *
 * ── VIỆC NÀY LÀM GÌ ──
 * Trước V7 việc của từng lượt do `viecTiepTheo` xoay vòng theo SỐ LƯỢT. Không ai —
 * kể cả bé — biết buổi học gồm mấy việc và còn mấy việc; buổi kết vì "hết" (hết giờ,
 * hoặc ba lượt đạt liền) chứ không vì "xong".
 *
 * ── CÁI DỄ HỎNG ──
 * Kế hoạch là tầng thứ BA cùng ra lệnh về một lượt, sau lời dặn theo nhãn (V2) và
 * `dongViec`. Ba tầng cùng nói thì chúng chọi nhau — đúng chỗ đã hỏng thật hai lần
 * trong kho này. Nên tệp này canh nặng nhất vào chuyện ấy: kế hoạch và lời dặn phải
 * nói về CÙNG MỘT TỪ.
 *
 * Và canh hai cái trần: replan ≤ 2, số bước 5–7. Buổi phình ra vô hạn thì bé không
 * bao giờ tới màn kết — cái bẫy `buocSua` đã ghi ("mười lượt liền đều là Hello!").
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  SO_BUOC, REPLAN_TOI_DA, SAI_DE_HA, SAI_DE_PHU_DAO, BAC_KHO, LY_DO_TOI_DA_CHU,
  lapKeHoach, buocHienTai, capNhatSauLuot, xongKeHoach,
  loiGioiThieu, dongBuocKeHoach, oThanhViec, conThieu,
} from '../src/mon/tienganh/lib/kehoach.js';
import {
  vonTu, viecTiepTheo, loiDan, tinhBuoi, moiTuDuocDung, DAT_LIEN_DE_XONG,
} from '../src/mon/tienganh/lib/phongnoi.js';
import { dungBang, datKeHoach } from '../src/mon/tienganh/lib/bangtrangthai.js';

const doc = (p) => JSON.parse(readFileSync(new URL(p, import.meta.url), 'utf8'));
const B05 = doc('../public/content/ta1/DL_TA1_B05.json');
const B01 = doc('../public/content/ta1/DL_TA1_B01.json');

/* Vốn ở hai chế độ: chưa đạt unit nào (không có bài ôn), và đã đạt (có bài ôn). */
const VON = vonTu({ baiNay: B05 });
const VON_ON = vonTu({ baiNay: B05, baiCu: [B01], daDat: true, datCu: () => true });

const NAY = 1_700_000_000_000;
const bangCua = (them = {}) => dungBang({
  bai: B05, thich: 'fish', quyen: 'ta1', bayGio: NAY, ...them,
});
const THE = [{ microId: 'DL:TA1.B01', dueAt: NAY - 1000 }];

/* ═══════════ 1 · HÌNH DẠNG KẾ HOẠCH ═══════════ */

test('kế hoạch 5–7 bước, mọi từ thuộc VỐN của buổi', () => {
  for (const [ten, von] of [['chưa có bài ôn', VON], ['có bài ôn', VON_ON]]) {
    const kh = lapKeHoach(bangCua({ cards: THE }), { von, bayGio: NAY });
    assert.ok(kh, `${ten}: không dựng được kế hoạch`);
    assert.ok(kh.buoc.length >= SO_BUOC[0] && kh.buoc.length <= SO_BUOC[1],
      `${ten}: ${kh.buoc.length} bước, ngoài khoảng ${SO_BUOC.join('–')}`);
    const cho = moiTuDuocDung(von);
    for (const b of kh.buoc) {
      assert.ok(cho.includes(b.tu?.tu),
        `${ten}: bước ${b.i} dùng từ "${b.tu?.tu}" ngoài vốn của buổi`);
      assert.ok(BAC_KHO.includes(b.kieu), `${ten}: bước ${b.i} kiểu lạ "${b.kieu}"`);
      assert.equal(b.trangThai, 'cho');
      assert.ok(b.lyDo && b.lyDo.length <= LY_DO_TOI_DA_CHU,
        `${ten}: lý do bước ${b.i} dài ${b.lyDo?.length} ký tự`);
    }
    /* Số bước liền mạch từ 1 — thanh bước hiện "việc thứ mấy / mấy". */
    assert.deepEqual(kh.buoc.map((b) => b.i), kh.buoc.map((_, i) => i + 1));
  }
});

test('thẻ đến hạn lên ĐẦU — cái sắp quên mới là cái đáng ôn', () => {
  const kh = lapKeHoach(bangCua({ cards: THE }), { von: VON_ON, bayGio: NAY });
  assert.equal(kh.buoc[0].loai, 'on');
  assert.equal(kh.buoc[0].nut, 'DL:TA1.B01', 'bước đầu không trỏ vào thẻ đến hạn');
});

/**
 * ⚠ BƯỚC "ÔN LẠI BÀI CŨ" PHẢI DÙNG TỪ CỦA BÀI CŨ.
 * Bản đầu lui về `tu[0]` khi `von.on` rỗng, nên lý do ghi "Ôn lại bài cũ sắp quên"
 * mà từ lại là từ của bài HÔM NAY — nói một điều không đúng với bé và với bố mẹ đọc
 * thanh bước. Bé chưa đạt unit nào thì nhường cho nhánh chông chênh.
 */
test('chưa có bài ôn thì KHÔNG dựng bước "ôn lại bài cũ"', () => {
  const kh = lapKeHoach(bangCua({ cards: THE }), { von: VON, bayGio: NAY });
  const on = kh.buoc.filter((b) => b.loai === 'on' && /bài cũ/.test(b.lyDo));
  assert.deepEqual(on, [], 'nói "ôn lại bài cũ" trong khi chưa có bài cũ nào');
});

test('bài KHÔNG có từ nào thì trả null, không trả kế hoạch RỖNG', () => {
  /* Kế hoạch 0 bước thì `xongKeHoach` ra true ngay từ đầu — buổi kết trước khi bé
     nói câu nào, và màn kết vẫn chúc mừng. Đúng kiểu hỏng đã gặp ở phòng này. */
  const von = vonTu({ baiNay: { id: 'X', knowledgeCore: { vocabulary: [], mauCauDs: [] } } });
  assert.equal(lapKeHoach(bangCua(), { von }), null);
  assert.equal(xongKeHoach(null), false);
  assert.equal(xongKeHoach({ buoc: [] }), false, 'kế hoạch rỗng KHÔNG được coi là đã xong');
});

/* ═══════════ 2 · ĐI THEO KẾ HOẠCH ═══════════ */

test('sai 2 lần HẠ BẬC, sai 3 chèn PHỤ ĐẠO, replan ≤ trần', () => {
  /* ⚠ HÌNH DẠNG CẠNH PHẢI ĐÚNG DỮ LIỆU THẬT: `{ can, truoc_khi }` nghĩa là PHẢI CÓ
     `can` TRƯỚC KHI học `truoc_khi` (xem `lib/doThi.js`). Fixture đầu của tôi viết
     `{ tu, den }` nên `duyetNguoc` trả rỗng, `nutGocRe` lui về chính nút mắc, và
     phép soi đỏ — đỏ vì FIXTURE sai, không vì mã sai. */
  const bang = bangCua({
    doThi: { nut: { g0: {}, n1: {} },
      canh: [{ can: 'g0', truoc_khi: 'n1', loai: 'ban_do' }] },
    mucThao: { n1: { p: 0.1 }, g0: { p: 0.1 } }, maNutMac: 'n1' });
  let kh = lapKeHoach(bang, { von: VON, bayGio: NAY });
  const dau = buocHienTai(kh);
  const bacDau = BAC_KHO.indexOf(dau.kieu);

  kh = capNhatSauLuot(kh, { nhan: 'thieuTu', diem: 3, bang });
  assert.equal(buocHienTai(kh).kieu, dau.kieu, 'sai MỘT lần đã hạ bậc — hạ quá nhanh');

  kh = capNhatSauLuot(kh, { nhan: 'thieuTu', diem: 3, bang });
  assert.equal(BAC_KHO.indexOf(buocHienTai(kh).kieu), Math.min(bacDau + 1, BAC_KHO.length - 1),
    `sai ${SAI_DE_HA} lần phải hạ đúng MỘT bậc`);

  kh = capNhatSauLuot(kh, { nhan: 'thieuTu', diem: 3, bang });
  assert.equal(buocHienTai(kh).loai, 'phuDao', `sai ${SAI_DE_PHU_DAO} lần phải chèn phụ đạo`);
  assert.equal(buocHienTai(kh).nut, 'g0', 'bước phụ đạo không trỏ vào nút GỐC RỄ');
  assert.ok(kh.buoc.some((b) => b.trangThai === 'bo'), 'bước đang mắc phải được đánh dấu bỏ');
  assert.equal(kh.soReplan, 1);

  /* ── TRẦN REPLAN ── Chèn phụ đạo mãi thì buổi phình vô hạn. */
  for (let i = 0; i < 20; i += 1) kh = capNhatSauLuot(kh, { nhan: 'thieuTu', diem: 3, bang });
  assert.ok(kh.soReplan <= REPLAN_TOI_DA, `replan ${kh.soReplan} lần, quá trần ${REPLAN_TOI_DA}`);
  assert.ok(kh.buoc.length <= SO_BUOC[1] + REPLAN_TOI_DA,
    `kế hoạch phình thành ${kh.buoc.length} bước`);
});

test('bé đúng thì bước XONG và sang bước sau', () => {
  let kh = lapKeHoach(bangCua(), { von: VON, bayGio: NAY });
  const n = kh.buoc.length;
  for (let i = 0; i < n; i += 1) {
    const b = buocHienTai(kh);
    assert.ok(b, `hết bước sớm ở lượt ${i + 1}/${n}`);
    kh = capNhatSauLuot(kh, { nhan: 'dung', diem: 9 });
  }
  assert.equal(buocHienTai(kh), null);
  assert.equal(xongKeHoach(kh), true);
  assert.equal(conThieu(kh), 0);
});

/**
 * ⚠ MẤY NHÃN KHÔNG NÓI GÌ VỀ VIỆC BÉ LÀM ĐƯỢC HAY KHÔNG thì KHÔNG tính là sai.
 * Trừ điểm bé vì nó hỏi cô một câu là dạy nó đừng hỏi nữa.
 */
test('bé hỏi lại · nói tiếng Việt · im lặng → KHÔNG tính một lần sai', () => {
  let kh = lapKeHoach(bangCua(), { von: VON, bayGio: NAY });
  const kieuDau = buocHienTai(kh).kieu;
  for (const nhan of ['hoiLai', 'tiengViet', 'imLang', 'hoiLai', 'imLang']) {
    kh = capNhatSauLuot(kh, { nhan, diem: 0 });
  }
  assert.equal(buocHienTai(kh).kieu, kieuDau, 'hạ bậc vì bé hỏi cô một câu');
  assert.equal(buocHienTai(kh).sai, 0);
  assert.equal(kh.soReplan, 0);
});

/* ═══════════ 3 · BA TẦNG PHẢI NÓI CÙNG MỘT TỪ ═══════════ */

/**
 * ⚠ ĐÂY LÀ PHÉP CANH ĐÁNG GIÁ NHẤT CỦA CẢ TỆP.
 *
 * Kế hoạch là tầng thứ BA cùng ra lệnh về một lượt. Bản đầu của tôi đưa `mau` TRẦN
 * vào việc, mà `dongViec` ở kiểu `mau` dặn cô đọc đúng nguyên văn `mau.cau` — câu ví
 * dụ của sách. Thế là lời dặn ra hai dòng nói về HAI TỪ KHÁC NHAU:
 *     THIS STEP (1 of 5): practise the word "chicken" …
 *     THIS TURN: say exactly this sentence …: "I like milk."
 * Mô hình đọc hai lệnh thì chọn bừa, và bước kế hoạch coi như không có.
 */
test('dòng THIS STEP và dòng THIS TURN nói về CÙNG một từ', () => {
  let kh = lapKeHoach(bangCua(), { von: VON, bayGio: NAY });
  for (let i = 0; i < kh.buoc.length; i += 1) {
    const b = buocHienTai(kh);
    if (!b) break;
    const viec = viecTiepTheo({ von: VON, lichSu: [], buocKH: b });
    const d = loiDan({ von: VON, tenBe: 'Lan', lop: 1, viec,
      dongKeHoach: dongBuocKeHoach(kh) });
    const step = d.split('\n').find((x) => x.startsWith('THIS STEP'));
    const turn = d.split('\n').find((x) => /^THIS TURN: (say|take)/.test(x));
    assert.ok(step, `bước ${b.i}: thiếu dòng THIS STEP`);
    assert.ok(turn, `bước ${b.i}: thiếu dòng việc của lượt`);
    assert.ok(step.includes(`"${b.tu.tu}"`), `bước ${b.i}: THIS STEP không nêu từ của bước`);
    assert.ok(turn.includes(b.tu.tu),
      `bước ${b.i}: hai dòng nói hai từ khác nhau\n  ${step}\n  ${turn}`);
    kh = capNhatSauLuot(kh, { nhan: 'dung', diem: 9 });
  }
});

test('viecTiepTheo ƯU TIÊN bước kế hoạch, nhưng SAU lượt sửa', () => {
  const kh = lapKeHoach(bangCua(), { von: VON, bayGio: NAY });
  const b = buocHienTai(kh);

  /* Có kế hoạch → việc của lượt là bước ấy, không phải lượt-thứ-mấy-chia-lấy-dư. */
  const v = viecTiepTheo({ von: VON, lichSu: [], buocKH: b });
  assert.equal(v.tu.tu, b.tu.tu);
  assert.equal(v.buocKeHoach, b.i);

  /* ⚠ Nhưng bé vừa SAI thì việc của lượt là SỬA ĐÚNG CÂU ẤY, kể cả khi kế hoạch
     đang trỏ sang bước khác. Đảo hai khối là lời dặn lại tự chọi nhau. */
  const lichSu = [{ vai: 'may', chu: 'I like milk.', en: 'I like milk.', vi: 'x', buoc: 'mau' },
                  { vai: 'be', chu: 'x', diem: 4, mau: 'I like milk.', thieu: ['like'] }];
  const sua = viecTiepTheo({ von: VON, lichSu, nhan: 'thieuTu', buocKH: b });
  assert.equal(sua.giuViec, true, 'kế hoạch đè mất lượt sửa — bé mất chỗ đang mắc');
  assert.equal(sua.mau.cau, 'I like milk.');

  /* Không có kế hoạch thì xoay vòng NHƯ CŨ — V7 không được đổi hành vi cũ. */
  const cu = viecTiepTheo({ von: VON, lichSu: [] });
  assert.equal(cu.buocKeHoach, undefined);
});

/* ═══════════ 4 · BUỔI CÓ ĐÍCH THẬT ═══════════ */

test('xong kế hoạch là một ĐÍCH của buổi, bên cạnh hết giờ và ba lượt đạt', () => {
  /* Trước V7 phòng này chỉ có hai cái PHANH; buổi kết vì "hết" chứ không vì "xong". */
  const be = (n, diem) => Array.from({ length: n }, () => ({ vai: 'be', chu: 'x', diem, buoc: 'mau' }));
  const ls = [{ vai: 'may', en: 'x', buoc: 'mau' }, ...be(2, 4)];
  assert.equal(tinhBuoi({ lichSu: ls }).trangThai, 'dang');
  assert.equal(tinhBuoi({ lichSu: ls, xongKeHoach: true }).trangThai, 'xongGioi');
  /* Và đường cũ vẫn còn: ba lượt đạt liền. */
  assert.equal(tinhBuoi({ lichSu: [{ vai: 'may', en: 'x', buoc: 'mau' }, ...be(DAT_LIEN_DE_XONG, 9)] })
    .trangThai, 'xongGioi');
});

/* ═══════════ 5 · BÉ THẤY VÀ NGHE ĐƯỢC KẾ HOẠCH ═══════════ */

test('lời giới thiệu đọc được bằng giọng Việt — KHÔNG lẫn chữ tiếng Anh', () => {
  /* Nó được đọc bằng giọng Việt (xem `tachTheoTieng`), nên một câu lẫn hai thứ
     tiếng ra một thứ tiếng không phải tiếng nào. */
  const kh = lapKeHoach(bangCua({ cards: THE }), { von: VON_ON, bayGio: NAY });
  const loi = loiGioiThieu(kh);
  assert.match(loi, new RegExp(`${kh.buoc.length} việc`));
  for (const t of moiTuDuocDung(VON_ON)) {
    assert.ok(!new RegExp(`\\b${t}\\b`, 'i').test(loi), `lời giới thiệu lẫn chữ Anh "${t}"`);
  }
  assert.equal(loiGioiThieu(null), '');
});

test('thanh bước: một ô một việc, bỏ bước đã bỏ, có trạng thái', () => {
  let kh = lapKeHoach(bangCua(), { von: VON, bayGio: NAY });
  let o = oThanhViec(kh);
  assert.equal(o.length, kh.buoc.length);
  assert.ok(o.every((x) => x.ma && x.nhan && x.tt === 'chua' && x.bieuTuong));
  assert.equal(conThieu(kh), kh.buoc.length);

  kh = capNhatSauLuot(kh, { nhan: 'dung', diem: 9 });
  o = oThanhViec(kh);
  assert.equal(o[0].tt, 'xong');
  assert.equal(conThieu(kh), kh.buoc.length - 1);

  /* Bước bị BỎ không hiện ra — bé không cần thấy việc cô đã rút lại. */
  const bang = bangCua();
  let k2 = lapKeHoach(bang, { von: VON, bayGio: NAY });
  for (let i = 0; i < SAI_DE_PHU_DAO; i += 1) k2 = capNhatSauLuot(k2, { nhan: 'thieuTu', diem: 3, bang });
  assert.ok(k2.buoc.some((b) => b.trangThai === 'bo'));
  assert.equal(oThanhViec(k2).length, k2.buoc.filter((b) => b.trangThai !== 'bo').length);
});

test('màn hình: thanh bước dùng lại ThanhViec, và ĐỢI kế hoạch rồi mới chào', () => {
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
  const ma = bo(readFileSync(new URL('../src/mon/tienganh/components/PhongNoi.jsx', import.meta.url), 'utf8'));
  assert.match(ma, /<ThanhViec/, 'không vẽ thanh bước — bé không thấy kế hoạch');
  assert.match(ma, /oThanhViec\(keHoach\)/);
  assert.match(ma, /loiGioiThieu\(keHoach\)/, 'không đọc lời giới thiệu — bé chưa đọc được chữ');
  /* ⚠ Chào trước khi có kế hoạch thì lượt ĐẦU TIÊN rơi về vòng xoay cũ. */
  assert.match(ma, /if \(!kichBan && !keHoach\) return;/,
    'chào trước khi có kế hoạch — lượt đầu không có bước nào để đi theo');
  /* ⚠ Kế hoạch phải là `state`, KHÔNG phải `useMemo`: useMemo dựng lại từ đầu mỗi
     khi `bang` đổi, tức mọi tiến độ bị xoá sau đúng một lượt. */
  assert.match(ma, /useState\(null\)/);
  assert.ok(!/useMemo\(\(\) => lapKeHoach/.test(ma), 'kế hoạch nằm trong useMemo — tiến độ bị xoá mỗi lượt');
  /* Bài tả tranh không lập kế hoạch: kịch bản đã là kế hoạch của nó. */
  assert.match(ma, /if \(keHoach \|\| kichBan/);
});

test('bảng trạng thái giữ kế hoạch, và giữ BẤT BIẾN', () => {
  const b = bangCua();
  const kh = lapKeHoach(b, { von: VON, bayGio: NAY });
  const b2 = datKeHoach(b, kh);
  assert.notEqual(b, b2);
  assert.equal(b.keHoach, null, 'bảng cũ bị sửa tại chỗ');
  assert.equal(b2.keHoach, kh);
  assert.equal(datKeHoach(b, null).keHoach, null);
});
