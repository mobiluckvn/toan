/**
 * CỔNG · HÀM CHÍNH SÁCH, PHỤ ĐẠO, A-R-A (Đợt 4 — mục 2.5.1 · 2.5.3 · 2.1.2).
 *
 * Bốn thứ canh ở đây, xếp theo mức nguy cho BÉ:
 *
 *  1. VƯỢT ẢI SAI CHỖ. Cho bé bỏ qua một bài chưa vững là mất một mắt xích, và
 *     mắt xích ấy đỡ cho những bài sau. Hỏng lặng lẽ: mọi con số tổng đều đẹp.
 *  2. PHỤ ĐẠO KHÔNG CÓ ĐƯỜNG LÙI. Bé vừa sai ba câu liền, màn hình hứa sẽ giúp,
 *     rồi mất mạng và bé nhận màn trắng — hỏng NẶNG HƠN không có phụ đạo.
 *  3. CÂU LLM KHÔNG QUA HẬU KIỂM. Đây là chỗ DUY NHẤT trong app mà câu hỏi không
 *     do bộ sinh dựng sẵn, tức là không cổng nào soi trước khi tới tay bé.
 *  4. A-R-A ĐO LẠI BẰNG CÂU CŨ. Đo trí nhớ ngắn hạn chứ không đo hiểu bài, và sai
 *     theo hướng ĐẸP LÊN: mọi bài phụ đạo đều trông như hiệu quả.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  VIEC, viecTiepCuaNut, viecTiepCuaBai, duocVuotAi, vectorS, SAI_LIEN_TIEP_MAC,
} from '../src/mon/tienganh/lib/chinhsach.js';
import {
  cauTinhCuaNut, dungPhuDao, SO_CAU_PHU_DAO, enCuaCau, cauHoiHopLe,
} from '../src/mon/tienganh/lib/phudao.js';
import { vonTu } from '../src/mon/tienganh/lib/phongnoi.js';
import { capHopLe, deltaC, gomTheoMau, mauTotNhat, TOI_THIEU_CAP } from '../functions/src/ara.js';
import { NGUONG_THAO, NGUONG_YEU } from '../src/mon/tienganh/lib/zpd.js';
import { MASTERY_THRESHOLD } from '../functions/src/bkt.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
const mt = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k,
  (typeof v === 'number' ? { p: v } : v)]));

/* ── ngưỡng ──────────────────────────────────────────────────────────────── */

test('⚠ NGƯỠNG VƯỢT ẢI LẤY TỪ MỘT CHỖ, và là 0,85 bác chốt', () => {
  /* Luận văn viết 0,95. Bác chốt giữ 0,85 (21-08) vì con số ấy hiệu chỉnh bằng
     thực nghiệm. Gõ lại số ở `chinhsach.js` là hai nơi hai số, và hai số thì sớm
     muộn lệch — lúc ấy "đã vững" ở màn này khác "đã vững" ở màn kia. */
  assert.equal(NGUONG_THAO, MASTERY_THRESHOLD);
  const ma = chiMa(doc('../src/mon/tienganh/lib/chinhsach.js'));
  assert.doesNotMatch(ma, /0\.95|0\.85/,
    'chinhsach.js gõ cứng ngưỡng — phải lấy từ `zpd.js` → `bkt.js`');
});

/* ── một nút ─────────────────────────────────────────────────────────────── */

test('ba nhánh của một nút', () => {
  assert.equal(viecTiepCuaNut({ p: 0.95 }).viec, VIEC.vuotAi);
  assert.equal(viecTiepCuaNut({ p: 0.5 }).viec, VIEC.tiep);
  assert.equal(viecTiepCuaNut({ p: 0.1 }).viec, VIEC.phuDao);
  assert.equal(viecTiepCuaNut({}).viec, VIEC.tiep, 'chưa có số thì cứ đi tiếp');
});

test('⚠ ĐANG MẮC xét TRƯỚC mức thạo', () => {
  /* Bé có thể có P(L) tàm tạm mà vẫn vừa sai ba câu liền — lúc ấy con số trung
     bình không phải thứ đáng nghe. */
  const r = viecTiepCuaNut({ p: 0.7, saiLienTiep: SAI_LIEN_TIEP_MAC });
  assert.equal(r.viec, VIEC.phuDao);
  assert.match(r.vi_sao, /liên tiếp/);
  /* Kể cả nút bé đã "vững" theo P(L). */
  assert.equal(viecTiepCuaNut({ p: 0.99, saiLienTiep: 3 }).viec, VIEC.phuDao);
});

test('sai hai lần liền thì CHƯA gọi phụ đạo', () => {
  /* Sai hai lần là chuyện thường của việc học; gọi phụ đạo ở đó thì bé bị ngắt
     mạch liên tục. */
  assert.equal(viecTiepCuaNut({ p: 0.6, saiLienTiep: 2 }).viec, VIEC.tiep);
});

test('mỗi quyết định đều giải thích được', () => {
  /* Quyết định về việc học của một đứa trẻ mà chỉ trả về một mã lệnh thì không ai
     cãi lại được, kể cả khi nó sai. */
  for (const ho of [{ p: 0.95 }, { p: 0.5 }, { p: 0.1 }, { saiLienTiep: 3 }, {}]) {
    assert.ok(viecTiepCuaNut(ho).vi_sao, `thiếu lý do cho ${JSON.stringify(ho)}`);
  }
});

/* ── cả bài ──────────────────────────────────────────────────────────────── */

test('⚠ PHỤ ĐẠO THẮNG VƯỢT ẢI', () => {
  /* 9 nút vững, 1 nút bé đang mắc → việc cần làm là gỡ nút ấy, không phải cho bé
     bay qua cả bài. Cho vượt ải ở đây là bỏ lại đúng chỗ bé cần giúp nhất. */
  const m = mt({ a: 0.95, b: 0.95, c: 0.05 });
  const r = viecTiepCuaBai(m, ['a', 'b', 'c']);
  assert.equal(r.viec, VIEC.phuDao);
  assert.equal(r.nutMac, 'c', 'phải chỉ đúng nút mắc nặng nhất');
});

test('⚠ VƯỢT ẢI ĐÒI MỌI NÚT ĐỀU VỮNG, VÀ ĐỦ SỐ LIỆU', () => {
  assert.equal(viecTiepCuaBai(mt({ a: 0.95, b: 0.95, c: 0.9 }), ['a', 'b', 'c']).viec,
    VIEC.vuotAi);
  /* Một nút CHƯA CÓ SỐ là một nút bé chưa từng làm — cho vượt là tuyên thạo khống.
     ⚠ Chỗ chặn nằm ở `viecTiepCuaNut`: nút không có `p` rơi vào nhánh `tiep`, nên
     `every(vuotAi)` hỏng ngay. Phép canh dưới đây kiểm ĐÚNG đường ấy, chứ không
     kiểm một chốt riêng — vì chốt riêng ở tầng bài là mã chết (đã đảo chiều thử). */
  assert.equal(viecTiepCuaNut({}).viec, VIEC.tiep, 'nút chưa có số phải rơi vào `tiep`');
  assert.equal(viecTiepCuaBai(mt({ a: 0.95, b: 0.95 }), ['a', 'b', 'c']).viec,
    VIEC.tiep, 'nút thiếu số liệu mà vẫn cho vượt ải');
});

test('cửa BỎ QUA BÀI hẹp: cần cả ba điều kiện', () => {
  const m = mt({ a: 0.95, b: 0.95, c: 0.95 });
  assert.equal(duocVuotAi(m, ['a', 'b', 'c'], true), true);
  assert.equal(duocVuotAi(m, ['a', 'b', 'c'], false), false, 'chưa ĐẠT thì không bỏ qua');
  assert.equal(duocVuotAi(m, ['a', 'b'], true), false, 'quá ít nút thì lời nói ấy vô nghĩa');
  assert.equal(duocVuotAi(mt({ a: 0.95, b: 0.5, c: 0.95 }), ['a', 'b', 'c'], true), false);
  assert.equal(duocVuotAi(null, ['a'], true), false);
});

/* ── phụ đạo ─────────────────────────────────────────────────────────────── */

const baiGia = {
  practice: {
    pools: {
      warmup: [{ id: 'C1', maNut: 'goc' }, { id: 'C2', maNut: 'goc' }],
      standard: [{ id: 'S1', maNut: 'goc' }, { id: 'S2', maNut: 'khac' }],
      challenge: [{ id: 'T1', maNutDs: ['goc'] }],
    },
  },
};
const DT = {
  nut: { goc: { t: 'vocabulary', b: 'DL:TA1.B01' }, mac: { t: 'grammar' } },
  canh: [{ can: 'goc', truoc_khi: 'mac', loai: 'ban_do' }],
};

test('câu tĩnh: ưu tiên bậc THẤP, và chỉ lấy câu của đúng nút', () => {
  const r = cauTinhCuaNut([baiGia], 'goc');
  assert.deepEqual(r.map((c) => c.id), ['C1', 'C2', 'S1', 'T1']);
  assert.ok(!r.some((c) => c.id === 'S2'), 'lấy nhầm câu của nút khác');
});

test('phụ đạo nhắm vào NÚT GỐC RỄ, không nhắm chỗ lộ ra', () => {
  const r = { };
  return dungPhuDao({
    dt: DT, mucThao: mt({ goc: 0.1, mac: 0.2 }), maNutMac: 'mac', baiDs: [baiGia],
  }).then((kq) => {
    assert.equal(kq.nutGoc, 'goc',
      'bé sai ở `mac` nhưng gốc là `goc` — luyện thêm `mac` thì bé sai tiếp');
    assert.equal(kq.baiGoc, 'DL:TA1.B01');
    Object.assign(r, kq);
  });
});

test('không tìm được gốc thì vá NGAY TẠI CHỖ MẮC, không trả rỗng', async () => {
  /* Nhiều nút không có tiên quyết nào, và chính nó là gốc. Đó không phải thất bại. */
  const kq = await dungPhuDao({
    dt: { nut: {}, canh: [] }, mucThao: mt({ goc: 0.1 }), maNutMac: 'goc',
    baiDs: [baiGia],
  });
  assert.equal(kq.nutGoc, 'goc');
  assert.ok(kq.cau.length > 0);
});

test('⚠ LLM HỎNG thì VẪN RA BÀI, và có cờ luiVe', async () => {
  /* Bé vừa sai ba câu liền, màn hình hứa sẽ giúp. Mất mạng mà bé nhận màn trắng
     là hỏng NẶNG HƠN không có phụ đạo: mất mạch học, và mất niềm tin vào cái nút
     vừa bấm. */
  const it = { practice: { pools: { warmup: [{ id: 'C1', maNut: 'goc' }] } } };
  const kq = await dungPhuDao({
    dt: DT, mucThao: mt({ goc: 0.1 }), maNutMac: 'goc', baiDs: [it],
    goiLLM: async () => { throw new Error('mất mạng'); },
  });
  assert.equal(kq.cau.length, 1, 'mất phần tĩnh đã có trong tay');
  assert.equal(kq.luiVe, true, 'phải nói ra là đã lùi, không giấu');
});

test('⚠ CÂU LLM SINH RA PHẢI QUA HẬU KIỂM', async () => {
  /* Đây là chỗ DUY NHẤT trong app mà câu hỏi không do bộ sinh dựng, tức là không
     cổng nào soi trước khi tới tay bé. `soiCau` là hàng rào cuối cùng. */
  const it = { practice: { pools: { warmup: [{ id: 'C1', maNut: 'goc' }] } } };
  const kq = await dungPhuDao({
    dt: DT, mucThao: mt({ goc: 0.1 }), maNutMac: 'goc', baiDs: [it],
    goiLLM: async () => [{ id: 'X1', ban: true }, { id: 'X2', ban: false }],
    soiCau: (c) => !c.ban,
  });
  assert.deepEqual(kq.cau.map((c) => c.id), ['C1', 'X2'], 'câu bẩn lọt qua hậu kiểm');
  assert.equal(kq.luiVe, true, 'có câu bị loại thì phải ghi nhận');
});

test('kho tĩnh đủ thì KHÔNG gọi LLM', async () => {
  let goi = 0;
  await dungPhuDao({
    dt: DT, mucThao: mt({ goc: 0.1 }), maNutMac: 'goc', baiDs: [baiGia],
    goiLLM: async () => { goi += 1; return []; },
  });
  assert.equal(goi, 0, 'gọi mạng khi không cần là bắt bé chờ vô cớ');
});

/**
 * ⚠ HẬU KIỂM CỦA PHỤ ĐẠO NHẬN **ĐỐI TƯỢNG CÂU HỎI**, KHÔNG PHẢI CHUỖI.
 *
 * Chú thích cũ của `dungPhuDao` ghi "chỗ gọi thật PHẢI truyền `cauHopLe`", nhưng
 * `cauHopLe(en, opt)` nhận một CHUỖI. Truyền thẳng nó vào thì nó đem một object đi
 * chuẩn hoá, ra chuỗi vô nghĩa, và BÁC SẠCH mọi câu — bài phụ đạo luôn rỗng, mà
 * rỗng thì trông y hệt "kho tĩnh không có gì". Tìm ra 26-08 lúc nối vào màn học.
 */
test('vỏ hậu kiểm cho CÂU HỎI: lấy đúng chuỗi tiếng Anh bé phải đọc', () => {
  assert.deepEqual(enCuaCau({ choices: ['ball', 'bike'] }), ['ball', 'bike']);
  /* Thẻ CHỮ ghép bằng dấu cách; thẻ CHỮ CÁI (có ô trống làm thẻ) ghép liền. */
  assert.deepEqual(enCuaCau({ the: ['I', 'like', 'fish.'] }), ['I like fish.']);
  assert.deepEqual(enCuaCau({ the: ['b', 'a', 'l', 'l'] }), ['ball']);
  assert.deepEqual(enCuaCau({ the: ['b', 'r', 'e', 'a', 'k', ' ', 't', 'i', 'm', 'e'] }),
    ['break time']);
  /* KHÔNG lấy lời dẫn và gợi ý — chúng là tiếng Việt, soi bằng vốn từ tiếng Anh
     thì bác nhầm gần hết. */
  assert.deepEqual(enCuaCau({ text: 'Nghe rồi bấm hình đúng.', hints: ['Từ này dài 4 chữ.'] }), []);
});

test('vỏ hậu kiểm bác câu có từ NGOÀI VỐN, nhận câu trong vốn', () => {
  const b = {
    id: 'X1',
    title: 'Unit X',
    knowledgeCore: {
      vocabulary: [{ tu: 'ball', nghia: 'quả bóng' }, { tu: 'bike', nghia: 'xe đạp' }],
      mauCauDs: [], canonicalExamples: [],
    },
    practice: { pools: {} },
  };
  const von = vonTu({ baiNay: b, baiCu: [], daDat: false });
  assert.equal(cauHoiHopLe({ choices: ['ball', 'bike'] }, { von }), true);
  assert.equal(cauHoiHopLe({ choices: ['ball', 'automobile'] }, { von }), false,
    'một phương án ngoài vốn là cả câu bị bác');
  /* Câu không bày chuỗi tiếng Anh nào (nghe rồi chọn hình) thì không có gì để bác. */
  assert.equal(cauHoiHopLe({ text: 'Nghe rồi bấm hình.' }, { von }), true);
  /* Không có vốn thì không soi được — cho qua, chứ đừng bác sạch. */
  assert.equal(cauHoiHopLe({ choices: ['automobile'] }, {}), true);
});

test('bài phụ đạo NGẮN — đây là chỗ gỡ, không phải bài học mới', async () => {
  const kq = await dungPhuDao({
    dt: DT, mucThao: mt({ goc: 0.1 }), maNutMac: 'goc', baiDs: [baiGia],
  });
  assert.ok(kq.cau.length <= SO_CAU_PHU_DAO);
});

/* ── A-R-A và ΔC ─────────────────────────────────────────────────────────── */

const cap = (pa, pb, ia, ib, mau = 'phudao', v = 1) => ({
  truoc: { p: pa, itemIds: ia }, sau: { p: pb, itemIds: ib },
  mauPrompt: mau, phienBanMau: v,
});

test('⚠ LẦN ĐO SAU DÙNG LẠI CÂU CŨ thì cặp BỊ BÁC', () => {
  /* Hỏi lại đúng mấy câu vừa chữa thì bé đúng vì vừa NHÌN THẤY đáp án — đo trí
     nhớ ngắn hạn, và sai theo hướng ĐẸP LÊN: mọi bài phụ đạo đều trông hiệu quả. */
  const r = capHopLe(cap(0.3, 0.8, ['a', 'b'], ['b', 'c']));
  assert.equal(r.ok, false);
  assert.match(r.vi, /dùng lại/);
  assert.equal(deltaC(cap(0.3, 0.8, ['a'], ['a'])), null);
  assert.ok(Math.abs(deltaC(cap(0.3, 0.8, ['a'], ['b'])) - 0.5) < 1e-9);
});

test('cặp thiếu dữ liệu thì bác, không đoán', () => {
  assert.equal(capHopLe(null).ok, false);
  assert.equal(capHopLe(cap(0.3, null, ['a'], ['b'])).ok, false);
  assert.equal(capHopLe(cap(0.3, 0.8, [], ['b'])).ok, false);
});

test('gom theo mẫu: dưới cỡ mẫu thì KHÔNG đưa ra con số', () => {
  const it = Array.from({ length: TOI_THIEU_CAP - 1 },
    (_, i) => cap(0.2, 0.9, [`a${i}`], [`b${i}`]));
  const g = gomTheoMau(it);
  assert.equal(g[0].deltaTB, null,
    'khen hay chê một mẫu prompt dựa trên vài cặp là kết luận tự nuôi chính nó');
  assert.equal(g[0].duMau, false);
  assert.equal(g[0].soCap, TOI_THIEU_CAP - 1);
});

test('gom theo mẫu: HIỆN số cặp bị bỏ qua, không giấu', () => {
  const ds = [
    ...Array.from({ length: TOI_THIEU_CAP }, (_, i) => cap(0.2, 0.9, [`a${i}`], [`b${i}`])),
    cap(0.2, 0.9, ['x'], ['x']),           // trùng câu → bị bác
  ];
  const g = gomTheoMau(ds)[0];
  assert.equal(g.soCap, TOI_THIEU_CAP);
  assert.equal(g.boQua, 1,
    'một mẫu có 40 cặp mà 35 bị loại thì trung bình của 5 cặp còn lại không đáng tin');
});

test('gom theo PHIÊN BẢN MẪU, không theo mã băm', () => {
  /* Mã băm đổi cả khi sửa một lỗi chính tả, nên gom theo băm là chẻ dữ liệu ra
     vụn. `phienBanMau` do người sửa khai tay — nó nói đúng "đây là lần đổi đáng kể". */
  const ma = chiMa(doc('../functions/src/ara.js'));
  assert.match(ma, /phienBanMau/);
  assert.doesNotMatch(ma, /vanTayPrompt/,
    'gom theo mã băm thì mỗi nhóm vài mẫu, chẳng so được gì');
});

test('mẫu tốt nhất: cần ÍT NHẤT HAI mẫu đủ mẫu', () => {
  const mot = Array.from({ length: TOI_THIEU_CAP },
    (_, i) => cap(0.2, 0.9, [`a${i}`], [`b${i}`], 'A', 1));
  assert.equal(mauTotNhat(mot), null,
    'một mẫu thì nó vừa tốt nhất vừa tệ nhất — câu ấy không có nghĩa gì');
  const hai = [...mot, ...Array.from({ length: TOI_THIEU_CAP },
    (_, i) => cap(0.2, 0.3, [`c${i}`], [`d${i}`], 'B', 1))];
  const r = mauTotNhat(hai);
  assert.equal(r.tot.mau, 'A');
  assert.equal(r.kem.mau, 'B');
});

/* ── vector S ────────────────────────────────────────────────────────────── */

test('vector S trả NHÃN, không trả số', () => {
  /* Chỗ nhận là lời dặn cho mô hình. Số thô thì mô hình không biết làm gì, và tệ
     hơn: nó có thể nhại lại nguyên văn trước mặt bé. */
  const s = vectorS({ mucThao: mt({ a: 0.9, b: 0.95 }), maNutDs: ['a', 'b'] });
  assert.equal(s.mucNam, 'vung');
  for (const v of Object.values(s)) {
    assert.ok(typeof v !== 'number', `vector S lọt số thô: ${JSON.stringify(s)}`);
  }
});

test('vector S: bốn chiều, và im khi chưa có số', () => {
  assert.equal(vectorS({ mucThao: mt({ a: 0.1 }), maNutDs: ['a'] }).mucNam, 'yeu');
  assert.equal(vectorS({ mucThao: mt({ a: 0.5 }), maNutDs: ['a'] }).mucNam, 'dangHoc');
  const trong = vectorS({ mucThao: {}, maNutDs: ['a'] });
  assert.equal(trong.mucNam, null, 'bé mới học buổi đầu không đáng bị đoán già');
  assert.equal(trong.hayQuen, false);
});

test('vector S: lâu không gặp thì bật cờ hayQuen', () => {
  const NGAY = 86400000;
  const m = { a: { p: 0.6, lastSeen: 0 }, b: { p: 0.6, lastSeen: 20 * NGAY } };
  assert.equal(vectorS({ mucThao: m, maNutDs: ['a', 'b'], bayGio: 20 * NGAY }).hayQuen,
    true, 'một nút bị bỏ quên là đủ để đáng nhắc lại');
  assert.equal(vectorS({ mucThao: { b: m.b }, maNutDs: ['b'], bayGio: 20 * NGAY }).hayQuen,
    false);
});

test('lời dặn LLM nhận vector S, và KHÔNG nhắc điểm số', () => {
  /* ⚠ SOI `bangtrangthai.js`, KHÔNG soi `phongnoi.js`.
     Việc V6 chuyển khối «về bé» sang đó (`tomTatChoLoiDan`); hàm `dongHoSo` cũ nằm
     lại trong `phongnoi.js` không ai gọi. Cổng này vẫn tìm chuỗi `hoSo.mucNam`
     trong tệp cũ và vẫn XANH — nhưng xanh nhờ MÃ CHẾT, không nhờ mã đang chạy. Gỡ
     mã chết ngày 10-10 thì cổng đỏ, và đó là lần đầu nó nói thật.
     Bài học: một cổng tìm chuỗi trong một tệp thì nó canh TỆP ẤY, không canh tính
     chất — chuyển việc sang tệp khác là nó canh nhầm chỗ mà không ai biết. */
  const ma = chiMa(doc('../src/mon/tienganh/lib/bangtrangthai.js'));
  assert.match(ma, /\bmucNam\b/, 'vector S chưa vào lời dặn');
  const i = ma.indexOf('function tomTatChoLoiDan');
  assert.ok(i >= 0, 'không thấy hàm dựng khối lời dặn');
  const khoi = ma.slice(i, i + 2500);
  assert.doesNotMatch(khoi, /\$\{[^}]*\bp\b[^}]*\}|Math\.round\([^)]*p /,
    'lời dặn đổ số vào — mô hình có thể nhại lại nguyên văn trước mặt bé');
});

test('ma trận trạng thái ĐÃ CÓ MÀN BÀY RA', () => {
  /* Đợt 3 tính được mà không ai xem thì cũng như chưa có — cùng dạng `reviewQueue`. */
  const man = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(man, /maTranTrangThai/);
  assert.match(man, /<MaTran/);
});
