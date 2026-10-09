/**
 * CỔNG · PHỤ ĐẠO CÓ HAI VÒNG, GRADER, CHẨN ĐOÁN BẰNG LỜI, VÀ ĐƯỜNG MÔ HÌNH (V9).
 *
 * ── CÁI DỄ HỎNG NHẤT ──
 * Câu do mô hình soạn là câu DUY NHẤT trong app không đi qua bộ sinh và 83 cổng.
 * Khối chú thích cuối `PhuDao.jsx` nói đúng vì sao đường ấy từng để ngỏ: hậu kiểm
 * vốn từ trả lời "câu này dùng chữ bé đã học không" — nó KHÔNG nói được câu ấy có
 * hai đáp án đúng, có gợi ý lộ đáp án, hay đáp án nằm ngoài danh sách phương án.
 *
 * Nên tệp này canh ba tầng, và canh cả thứ tự của chúng:
 *   1. kho TĨNH đi trước, HAI vòng (nút gốc rễ #1 rồi #2) — câu đã qua 83 cổng;
 *   2. `soiCauAI` soi sáu luật của một câu hỏi mà vốn từ không nói được;
 *   3. luật thứ bảy cần NGƯỜI — nên câu phải qua hàng đợi `choDuyetTA`.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  dungPhuDao, cauHoiHopLe, soiCauAI, soiBoCauAI,
  SO_CAU_PHU_DAO, VONG_TOI_DA, SO_CHON_TOI_THIEU,
} from '../src/mon/tienganh/lib/phudao.js';
import {
  cauChanDoan, chamCauTinh, chuDeNut, CHAN_DOAN_TOI_DA_CHU, NUT_TOI_DA_MOT_CAU,
} from '../src/mon/tienganh/lib/chandoan.js';
import {
  soiGoiPhuDao, loiDanSinhPhuDao, khungPhuDao, sinhPhuDao,
  TOI_DA_TU_VON, SO_CAU_TOI_DA, TOKEN_PHU_DAO,
} from '../functions/src/phudao.js';
import { PHIEN_BAN_MAU } from '../functions/src/vantay.js';
import { nhanNut } from '../src/mon/tienganh/lib/doThi.js';

const doc = (p) => JSON.parse(readFileSync(new URL(p, import.meta.url), 'utf8'));
const DT_THAT = doc('../public/content/tienganh/do_thi.json');

/* Đồ thị ba nút chuỗi: n0 (bé mắc) ← g1 ← g2. */
const DT = {
  nut: { n0: { n: 'Nút mắc', b: 'B3' }, g1: { n: 'Nút giữa', b: 'B2' }, g2: { n: 'Nút gốc', b: 'B1' } },
  canh: [{ can: 'g1', truoc_khi: 'n0', loai: 'ban_do' },
         { can: 'g2', truoc_khi: 'g1', loai: 'ban_do' }],
};
const MUC_THAO = { n0: { p: 0.2 }, g1: { p: 0.15 }, g2: { p: 0.1 } };
const cauTinh = (id, nut, them = {}) => ({ id, maNut: nut, choices: ['ball'], text: 'x', ...them });
/* ⚠ VỐN PHẢI CÓ ĐỦ TỪ ĐỂ DỰNG MỘT CÂU HỎI HỢP LỆ. Fixture đầu của tôi chỉ có
   `ball`, nên hai câu "đúng" cuối cùng dùng phương án nhiễu `ball ball` — một chuỗi
   KHÔNG nằm trong vốn, và `cauHoiHopLe` bác đúng. Phép thử đỏ vì FIXTURE, không vì
   mã: nó đòi 4 câu mà tự dựng dữ liệu chỉ cho ra 2. */
const VON = { loi: { tu: [{ tu: 'ball' }, { tu: 'cat' }, { tu: 'dog' }, { tu: 'fish' }],
  cau: [], cauSach: [] }, on: [] };
const soi = (c) => cauHoiHopLe(c, { von: VON }) && (c.nguon !== 'ai' || soiCauAI(c).ok);

/* ═══════════ 1 · HAI VÒNG KHO TĨNH ═══════════ */

test('vòng 2 chạy khi vòng 1 không đủ câu', async () => {
  /* Một câu tĩnh của nút #2 vẫn là câu đã qua bộ sinh và 83 cổng, còn câu mô hình
     sinh thì chỉ có hậu kiểm đỡ. Rẻ hơn, chắc hơn, không tốn lời gọi nào. */
  const baiDs = [{ practice: { pools: { warmup: [
    cauTinh('c1', 'g1'), cauTinh('c2', 'g1'), cauTinh('c3', 'g2'), cauTinh('c4', 'g2'),
  ] } } }];
  let goiDa = 0;
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs,
    von: VON, soiCau: soi, goiLLM: async () => { goiDa += 1; return []; } });
  assert.equal(r.cau.length, SO_CAU_PHU_DAO);
  assert.equal(r.nguon, 'tinh');
  assert.equal(r.soVong, 2, 'không chạy vòng hai — mô hình bị gọi quá sớm');
  assert.deepEqual(r.nutDaThu, ['g1', 'g2']);
  assert.equal(goiDa, 0, 'đủ câu tĩnh mà vẫn tốn một lời gọi mô hình');
  assert.equal(VONG_TOI_DA, 2);
});

test('vòng 1 ĐỦ câu thì KHÔNG chạy vòng hai', async () => {
  const baiDs = [{ practice: { pools: { warmup: [1, 2, 3, 4].map((i) => cauTinh(`c${i}`, 'g1')) } } }];
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs, von: VON, soiCau: soi });
  assert.equal(r.soVong, 1);
  assert.deepEqual(r.nutDaThu, ['g1']);
});

/* ═══════════ 2 · GRADER CHO CÂU TĨNH ═══════════ */

/**
 * ⚠ `cauTinhCuaNut` nhận câu khi nút nằm trong `maNutDs` — mà `maNutDs` là MỌI nút
 * câu ấy chạm tới, nên một câu ôn tập cuối chương "thuộc" cả năm nút. Lấy nó đi phụ
 * đạo cho một nút cụ thể thì bé làm một câu rộng hơn hẳn chỗ nó đang mắc, mà hệ
 * thống vẫn ghi "đã phụ đạo nút ấy" — ΔC đo ra một con số về một việc không xảy ra.
 */
test('chamCauTinh loại câu ÔN TẬP chạm quá nhiều nút', () => {
  assert.equal(chamCauTinh({ id: 'c', maNut: 'A' }, { maNut: 'A' }), 1, 'nút chính');
  assert.equal(chamCauTinh({ id: 'c', maNut: 'B', maNutDs: ['A', 'B'] }, { maNut: 'A' }), 1, 'nút phụ, ít nút');
  assert.equal(chamCauTinh({ id: 'c', maNut: 'B', maNutDs: ['A', 'B', 'C'] }, { maNut: 'A' }), 0,
    `chạm hơn ${NUT_TOI_DA_MOT_CAU} nút là câu ôn tập, không phải câu của một nút`);
  assert.equal(chamCauTinh({ id: 'c', maNut: 'B' }, { maNut: 'A' }), 0, 'không liên quan');
  assert.equal(chamCauTinh(null, { maNut: 'A' }), 0);
  assert.equal(chamCauTinh({ id: 'c', maNut: 'A' }, {}), 0);
});

test('câu ÔN TẬP không lọt vào bài phụ đạo', async () => {
  const baiDs = [{ practice: { pools: { warmup: [
    cauTinh('ok', 'g1'),
    cauTinh('rong', 'z', { maNutDs: ['g1', 'a', 'b', 'c'] }),
  ] } } }];
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs, von: VON, soiCau: soi });
  assert.deepEqual(r.cau.map((c) => c.id), ['ok']);
});

/* ═══════════ 3 · ĐƯỜNG MÔ HÌNH, VÀ BA TẦNG ĐỠ ═══════════ */

/* ⚠ LỜI DẪN PHẢI KHÁC NHAU. Fixture đầu của tôi dùng chung một lời dẫn cho mọi
   câu, nên `soiBoCauAI` dọn chúng thành MỘT — và phép canh đỏ vì fixture, không vì
   mã. Trùng lời dẫn ĐÚNG là trùng câu: bé thấy đúng một câu hỏi hai lần. */
const cauAI = (i, chon, dap, them = {}) => ({
  id: `ai${i}`, maNut: 'g1', nguon: 'ai', format: 'chondapan',
  text: `Chọn từ đúng, câu ${'x'.repeat(i)}`, choices: chon, answerKey: dap, hints: [], ...them,
});

test('mô hình trả 6 câu, 2 ngoài vốn → chỉ 4 vào bài, hai câu AI đeo nhãn', async () => {
  const it = [{ practice: { pools: { warmup: [cauTinh('c1', 'g1'), cauTinh('c2', 'g1')] } } }];
  const goiLLM = async () => [
    cauAI(1, ['delicious', 'ball'], 'delicious'),   // ngoài vốn
    cauAI(2, ['wonderful', 'ball'], 'wonderful'),   // ngoài vốn
    cauAI(3, ['ball', 'ball'], 'ball'),             // hai phương án TRÙNG
    cauAI(4, ['ball'], 'ball'),                     // một phương án
    cauAI(5, ['ball', 'cat', 'dog', 'fish'], 'ball'),
    cauAI(6, ['cat', 'dog', 'fish', 'ball'], 'cat'),
  ];
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs: it,
    von: VON, soiCau: soi, goiLLM });
  assert.equal(r.cau.length, SO_CAU_PHU_DAO, 'bài phải đủ 4 câu');
  assert.deepEqual(r.cau.map((c) => c.nguon), ['tinh', 'tinh', 'ai', 'ai']);
  assert.equal(r.nguon, 'tron');
  /* Hàng đợi duyệt chỉ nhận câu BÉ THẬT SỰ LÀM, không phải mọi câu hợp lệ. */
  assert.equal(r.choDuyet.length, 2);
  assert.ok(r.choDuyet.every((c) => c.nguon === 'ai'));
});

test('mô hình ném lỗi → vẫn có phần tĩnh, và trangThai dùng được', async () => {
  const it = [{ practice: { pools: { warmup: [cauTinh('c1', 'g1'), cauTinh('c2', 'g1')] } } }];
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs: it,
    von: VON, soiCau: soi, goiLLM: async () => { throw new Error('mất mạng'); } });
  assert.equal(r.cau.length, 2, 'mô hình hỏng mà mất luôn phần tĩnh');
  assert.equal(r.nguon, 'tinh');
  assert.equal(r.luiVe, true, 'phải NÓI RA là đã phải lùi — không thì không ai đếm được');
  assert.deepEqual(r.choDuyet ?? [], []);
});

/**
 * ⚠ SÁU LUẬT MÀ VỐN TỪ KHÔNG NÓI ĐƯỢC MỘT CHỮ NÀO.
 * Đây là tầng mà khối chú thích cuối `PhuDao.jsx` đòi phải có TRƯỚC khi cắm mô
 * hình: "sinh thiếu một luật là ra một câu hỏi hai đáp án đúng, hoặc một gợi ý lộ
 * luôn đáp án; hậu kiểm theo vốn từ KHÔNG bắt được những lỗi ấy."
 */
test('soiCauAI bắt sáu lỗi của một câu hỏi', () => {
  const ca = [
    [cauAI(1, ['cat', 'dog', 'fish', 'ball'], 'cat', { hints: ['con vật kêu meo'] }), true, 'câu đúng'],
    [cauAI(2, ['cat', 'cat', 'fish'], 'cat'), false, 'hai phương án trùng → HAI đáp án đúng'],
    [cauAI(3, ['dog', 'fish'], 'cat'), false, 'đáp án ngoài danh sách'],
    [cauAI(4, ['cat', 'dog'], 'cat', { hints: ['đáp án là cat'] }), false, 'gợi ý lộ đáp án'],
    [cauAI(5, ['cat'], 'cat'), false, 'một phương án'],
    [cauAI(6, ['cat', 'dog'], 'cat', { text: '' }), false, 'lời dẫn rỗng'],
    [cauAI(7, ['cat', 'dog'], 'cat', { text: 'Chọn 1 trong 2' }), false, 'lời dẫn có số'],
  ];
  for (const [c, mong, vi] of ca) {
    assert.equal(soiCauAI(c).ok, mong, `${vi}: ra ${soiCauAI(c).ok} (${soiCauAI(c).vi})`);
    if (!mong) assert.ok(soiCauAI(c).vi, 'bác mà không nói lý do');
  }
  assert.equal(SO_CHON_TOI_THIEU, 2);
  /* ⚠ Và KHÔNG bắt oan: gợi ý chỉ CHỨA một phần đáp án thì vẫn qua. */
  assert.equal(soiCauAI(cauAI(8, ['cat', 'dog'], 'cat', { hints: ['con chọn chữ có ba chữ cái'] })).ok, true);
});

test('câu AI vẫn phải qua hậu kiểm VỐN TỪ — hai tầng, không thay nhau', () => {
  /* Một câu đúng hình dạng mà dùng chữ ngoài vốn thì `soiCauAI` cho qua —
     `cauHoiHopLe` mới là tầng bắt nó. Bỏ một trong hai là hở một đường. */
  const c = cauAI(9, ['delicious', 'ball'], 'delicious');
  assert.equal(soiCauAI(c).ok, true, 'soiCauAI KHÔNG soi vốn từ — đó là việc của tầng kia');
  assert.equal(cauHoiHopLe(c, { von: VON }), false);
  assert.equal(soi(c), false, 'hai tầng ghép lại phải bác');
});

/* ═══════════ 4 · CHẨN ĐOÁN BẰNG LỜI ═══════════ */

test('cauChanDoan: ≤ 120 ký tự, có nhãn nút gốc rễ, tiếng Việt', () => {
  const goc = Object.keys(DT_THAT.nut).find((k) => k.startsWith('v_g1_') && DT_THAT.nut[k].n);
  const s = cauChanDoan({ dt: DT_THAT, nutSai: 'sp_g1_u12_1', nutGocRe: goc, nhan: 'thieuTu' });
  assert.ok(s.length <= CHAN_DOAN_TOI_DA_CHU, `${s.length} ký tự, quá ${CHAN_DOAN_TOI_DA_CHU}`);
  assert.match(s, /[àáảãạăâèéẻẽẹêìíỉĩịòóỏõọôơùúủũụưỳýỷỹỵđ]/i, 'phải là tiếng Việt');
  /* Nhãn nút phải CÓ MẶT — không thì bé không biết đang ôn cái gì. */
  const chu = chuDeNut(DT_THAT, goc).split(',')[0].trim();
  assert.ok(s.includes(chu), `thiếu nhãn nút gốc rễ "${chu}": ${s}`);
  /* Và KHÔNG được có mã máy. */
  assert.ok(!s.includes(goc), 'bày mã nút ra cho bé — đúng lỗi đã xảy ra 22-08');
});

test('gốc rễ TRÙNG nút sai thì nói khác đi, không bịa ra "cái trước nó"', () => {
  /* Nhiều nút không có tiên quyết nào, và chính nó là gốc. */
  const s = cauChanDoan({ dt: DT, nutSai: 'n0', nutGocRe: 'n0', nhan: 'imLang' });
  assert.match(s, /ôn lại/);
  assert.ok(!/dựng trên/.test(s), 'nói "dựng trên" về một cái không tồn tại');
});

test('mọi nhãn lượt của V2 đều ra một câu dùng được', () => {
  for (const nhan of ['dung', 'thieuTu', 'saiThuTu', 'nhamTu', 'tiengViet',
                      'hoiLai', 'imLang', 'lacDe', 'moDau', null, 'nhan-la']) {
    const s = cauChanDoan({ dt: DT, nutSai: 'n0', nutGocRe: 'g1', nhan });
    assert.ok(s.trim().length > 10, `nhãn ${nhan}: câu rỗng`);
    assert.ok(s.length <= CHAN_DOAN_TOI_DA_CHU, `nhãn ${nhan}: ${s.length} ký tự`);
    assert.ok(!/\bundefined\b|\bnull\b/.test(s), `nhãn ${nhan}: lọt chữ máy — ${s}`);
  }
});

test('chuDeNut bóc công thức thành chữ đọc được', () => {
  assert.equal(chuDeNut({ nut: { a: { n: "She's + [Verb-ing]." } } }, 'a'), "She's …");
  assert.equal(chuDeNut({ nut: { a: { n: 'mango — quả xoài' } } }, 'a'), 'mango, quả xoài');
  assert.equal(chuDeNut({ nut: {} }, 'a'), '');
  assert.equal(chuDeNut(null, 'a'), '');
});

test('chẩn đoán đi tới bài phụ đạo, và màn hình ĐỌC nó', () => {
  const r = { chanDoan: cauChanDoan({ dt: DT, nutSai: 'n0', nutGocRe: 'g1', nhan: 'thieuTu' }) };
  assert.ok(r.chanDoan);
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
  const ma = bo(readFileSync(new URL('../src/mon/tienganh/components/PhuDao.jsx', import.meta.url), 'utf8'));
  assert.match(ma, /bai\.chanDoan/, 'màn hình không hiện câu chẩn đoán');
  assert.match(ma, /tachTheoTieng\(bai\.chanDoan/,
    'đọc câu chẩn đoán bằng giọng Việt trọn câu — mẩu tiếng Anh sẽ ra một thứ tiếng không phải tiếng nào');
});

/* ═══════════ 5 · PHÍA MÁY CHỦ ═══════════ */

test('soiGoiPhuDao chốt cửa: nhãn · vốn · số câu', () => {
  const ok = { nhan: 'mango, quả xoài', vonTu: [{ tu: 'mango', nghia: 'quả xoài' }],
    mauCau: ['I like + [Noun].'], soCau: 2, lop: 1 };
  assert.equal(soiGoiPhuDao(ok).soCau, 2);
  for (const [ten, du] of [
    ['thiếu nhãn', { ...ok, nhan: '' }],
    ['nhãn quá dài', { ...ok, nhan: 'x'.repeat(500) }],
    ['thiếu vốn', { ...ok, vonTu: [] }],
    ['vốn quá lớn', { ...ok, vonTu: Array.from({ length: TOI_DA_TU_VON + 1 }, () => ({ tu: 'a' })) }],
    ['số câu 0', { ...ok, soCau: 0 }],
    ['số câu quá trần', { ...ok, soCau: SO_CAU_TOI_DA + 1 }],
  ]) {
    assert.throws(() => soiGoiPhuDao(du), undefined, `${ten} KHÔNG bị chặn`);
  }
});

test('lời dặn sinh câu đòi ĐÚNG hình dạng câu bấm chọn', () => {
  /* Thả cho mô hình tự chọn hình dạng thì nó sinh câu điền-vào-ô — mà ô nhập chỉ
     dành cho SỐ (luật của cả app), và một câu đòi bé GÕ CHỮ tiếng Anh là bắt bé tự
     nghĩ ra chính tả của một chữ nó đang mắc. */
  const d = loiDanSinhPhuDao(soiGoiPhuDao({ nhan: 'x', vonTu: [{ tu: 'ball' }], soCau: 2, lop: 1 }));
  assert.match(d, /KHÔNG câu điền vào ô/);
  assert.match(d, /đúng 1 phương/);
  assert.match(d, /CHỈ ĐƯỢC lấy từ bảng vốn từ/);
  assert.match(d, /Dễ trước, khó sau/);
  assert.match(d, /"answer" PHẢI là một trong "choices"/);
  assert.ok(d.length <= 4000);
});

test('khung vân tay không chứa một chữ nào của bé, và mẫu đã khai phiên bản', () => {
  const k = khungPhuDao(1, 2, true);
  for (const x of ['mango', 'quả xoài', 'I like']) assert.ok(!k.includes(x), `khung lọt "${x}"`);
  assert.ok(k.length > 300, 'khung ngắn bất thường');
  assert.equal(typeof PHIEN_BAN_MAU.phudao, 'number', 'mẫu phudao chưa khai phiên bản');
  /* Số câu và lớp KHÁC nhau là hai mẫu khác nhau — gom chung khi so ΔC là gom nhầm. */
  assert.notEqual(khungPhuDao(1, 2, true), khungPhuDao(5, 2, true));
  assert.notEqual(khungPhuDao(1, 2, true), khungPhuDao(1, 4, true));
});

test('sinhPhuDao trả CHỮ TRẦN kèm vân tay, và đúng nút vặn', async () => {
  let daGoi = null;
  const gia = () => ({ chat: { completions: { create: async (o) => {
    daGoi = o;
    return { choices: [{ message: { content: '{"cau":[{"text":"x","choices":["ball","cat"],"answer":"ball"}]}' } }] };
  } } } });
  const r = await sinhPhuDao({ nhan: 'x', vonTu: [{ tu: 'ball' }], soCau: 1, lop: 1 }, gia);
  assert.match(r.chu, /"cau"/, 'phải trả CHỮ TRẦN — bóc JSON là việc của máy con');
  assert.equal(r.mauPrompt, 'phudao');
  assert.equal(r.phienBanMau, PHIEN_BAN_MAU.phudao);
  assert.match(r.vanTayPrompt, /^[0-9a-f]{12}$/);
  assert.equal(daGoi.max_tokens, TOKEN_PHU_DAO);
  assert.equal(daGoi.response_format?.type, 'json_object');
  assert.ok(daGoi.temperature <= 0.5, 'đây là soạn bài, không phải chỗ sáng tác');

  /* Mô hình trả RỖNG thì NÓI RA, đừng đưa chuỗi rỗng xuống máy con. */
  const rong = () => ({ chat: { completions: { create: async () => ({ choices: [{ finish_reason: 'length', message: { content: '' } }] }) } } });
  await assert.rejects(() => sinhPhuDao({ nhan: 'x', vonTu: [{ tu: 'a' }], soCau: 1 }, rong),
    (e) => e.ma === 'tra-loi-rong');
});

test('máy chủ KHÔNG lưu gì, kể cả ở đường phụ đạo', () => {
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  const src = bo(readFileSync(new URL('../functions/src/phudao.js', import.meta.url), 'utf8'));
  assert.ok(!/firestore|getFirestore|db\./i.test(src), 'máy chủ đụng tới Firestore');
  assert.ok(!/console\.(log|info|warn)/.test(src), 'máy chủ ghi nội dung ra log');
});

/* ═══════════ 6 · LUẬT THỨ BẢY CẦN NGƯỜI ═══════════ */

test('hàng đợi duyệt: bé GHI được, bé KHÔNG đọc được', () => {
  /* Luật thứ bảy — "phương án nhiễu có thật là cái sai trẻ hay mắc hay chỉ là một
     chữ bừa" — không kiểm được bằng code. Nên câu phải chờ người lớn.
     ⚠ Để bé ĐỌC thì đây thành một kho câu chưa ai kiểm mà bé lấy ra làm được. */
  const luat = readFileSync(new URL('../firestore.rules', import.meta.url), 'utf8');
  const i = luat.indexOf('match /choDuyetTA/');
  assert.notEqual(i, -1, 'chưa có luật cho hàng đợi duyệt — máy chủ sẽ từ chối, im lặng');
  const khoi = luat.slice(i, luat.indexOf('\n    }', i));
  assert.match(khoi, /allow read:\s*if isTeacher\(\) \|\| isAdmin\(\)/, 'bé đọc được hàng đợi duyệt');
  assert.match(khoi, /allow create: if isMine\(/, 'bé không ghi được thì hàng đợi luôn rỗng');
  assert.match(khoi, /nguon == 'ai'/, 'luật không chốt nguồn — câu tĩnh cũng lọt vào hàng đợi');
  assert.match(khoi, /trangThai == 'cho'/);
  assert.ok(!/allow update: if isMine\(/.test(khoi), 'bé tự duyệt được câu của chính mình');

  /* Và ba chỗ phải khớp: luật · đường ghi · chỗ gọi. */
  const du = readFileSync(new URL('../src/mon/tienganh/lib/duLieu.js', import.meta.url), 'utf8');
  assert.match(du, /'choDuyetTA'/, 'không có đường ghi lên hàng đợi');
  const pd = readFileSync(new URL('../src/mon/tienganh/components/PhuDao.jsx', import.meta.url), 'utf8');
  assert.match(pd, /luuCauChoDuyet\(/, 'màn hình không đẩy câu lên hàng đợi');
});

test('đường TĨNH vẫn là đường chính — không mạng vẫn có phụ đạo', async () => {
  /* Ràng buộc của §7: đường lùi tĩnh giữ nguyên. */
  const baiDs = [{ practice: { pools: { warmup: [1, 2, 3, 4].map((i) => cauTinh(`c${i}`, 'g1')) } } }];
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs, von: VON, soiCau: soi });
  assert.equal(r.cau.length, SO_CAU_PHU_DAO);
  assert.equal(r.nguon, 'tinh');
  /* Và không truyền `goiLLM` thì KHÔNG có đường nào gọi mạng. */
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, ' ');
  const src = bo(readFileSync(new URL('../src/mon/tienganh/lib/phudao.js', import.meta.url), 'utf8'));
  assert.ok(!/httpsCallable|fetch\(/.test(src), 'lib/phudao.js biết tới mạng — nó phải thuần');
});

/* ═══════════ 7 · HAI CHỖ CHỈ THẤY KHI GỌI MÔ HÌNH THẬT ═══════════ */

/**
 * ⚠ ĐÁP ÁN LỘ TRONG LỜI DẪN, KHÔNG CHỈ TRONG GỢI Ý.
 * Đo thật 09-10: mô hình sinh lời dẫn tiếng Việt `Bạn của tôi luôn nói: I like
 * fish.` cho câu có đáp án đúng `I like fish`. Bé chỉ việc chép lại. Bản đầu của
 * `soiCauAI` chỉ ngó `hints`, nên câu ấy đi lọt — 20 phép canh đều xanh.
 */
test('lời dẫn chứa thẳng đáp án thì BỊ BÁC', () => {
  const lo = { text: 'Bạn của tôi luôn nói: I like fish.',
    choices: ['I like fish', 'I like milk'], answerKey: 'I like fish' };
  assert.equal(soiCauAI(lo).ok, false);
  assert.match(soiCauAI(lo).vi, /lời dẫn lộ/);
  /* Và KHÔNG bắt oan lời dẫn chỉ trùng MỘT phần đáp án. */
  assert.equal(soiCauAI({ text: 'Con thích cá thì chọn câu nào?',
    choices: ['I like fish', 'I like milk'], answerKey: 'I like fish' }).ok, true);
  assert.equal(soiCauAI({ text: 'Tôi thích cá.',
    choices: ['I like fish', 'I like milk'], answerKey: 'I like fish' }).ok, true);
});

/**
 * ⚠ BỐN CÂU Y HỆT NHAU — thứ soi từng câu một KHÔNG thấy được.
 * Đo thật 09-10: mô hình trả về bốn câu với ĐÚNG MỘT bộ phương án và ĐÚNG MỘT đáp
 * án (`I like fish` bốn lần, chỉ khác lời dẫn). Từng câu đều hợp lệ; cả bộ thì là
 * một câu hỏi lặp bốn lần, và bé làm bốn lần cùng một việc.
 */
test('bộ câu trùng nhau chỉ giữ MỘT', () => {
  const bo = [1, 2, 3, 4].map((i) => ({ id: `a${i}`, text: `Lời dẫn khác nhau ${'x'.repeat(i)}`,
    choices: ['I like fish', 'I like milk'], answerKey: 'I like fish' }));
  for (const c of bo) assert.equal(soiCauAI(c).ok, true, 'từng câu một thì đều hợp lệ');
  const r = soiBoCauAI(bo);
  assert.equal(r.cau.length, 1, 'không dọn được bộ câu trùng');
  assert.equal(r.boQua.length, 3);
  assert.ok(r.boQua.every((x) => x.vi));

  /* ⚠ Và KHÔNG dọn oan: đổi ĐÁP ÁN là một câu hỏi khác, dù cùng bộ phương án. */
  const khac = soiBoCauAI([
    { id: 'a', text: 'x', choices: ['cat', 'dog'], answerKey: 'cat' },
    { id: 'b', text: 'y', choices: ['cat', 'dog'], answerKey: 'dog' },
  ]);
  assert.equal(khac.cau.length, 2);
  /* Trùng LỜI DẪN cũng là trùng — bé thấy đúng một câu hỏi hai lần. */
  assert.equal(soiBoCauAI([
    { id: 'a', text: 'Chọn từ đúng', choices: ['cat', 'dog'], answerKey: 'cat' },
    { id: 'b', text: 'Chọn từ đúng', choices: ['fish', 'ball'], answerKey: 'fish' },
  ]).cau.length, 1);
});

test('dungPhuDao lọc cả BỘ trước khi lọc từng câu', async () => {
  const it = [{ practice: { pools: { warmup: [cauTinh('c1', 'g1')] } } }];
  /* Bốn câu hợp lệ nhưng TRÙNG nhau — chỉ một được vào bài. */
  const goiLLM = async () => [1, 2, 3, 4].map((i) => cauAI(i, ['ball', 'cat'], 'ball',
    { text: `Lời dẫn số ${'x'.repeat(i)}` }));
  const r = await dungPhuDao({ dt: DT, mucThao: MUC_THAO, maNutMac: 'n0', baiDs: it,
    von: VON, soiCau: soi, goiLLM });
  assert.equal(r.cau.filter((c) => c.nguon === 'ai').length, 1,
    'bốn câu y hệt nhau cùng vào bài — bé làm bốn lần một việc');
});
