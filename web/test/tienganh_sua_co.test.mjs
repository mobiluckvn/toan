/**
 * CỔNG · XIN LẠI CÂU CỦA CÔ (vòng gọi lại, mẫu Evaluator–Optimizer).
 *
 * Phép soi câu (`soiCau`) có từ lâu và chặn tốt. Nhưng chặn xong thì bản cũ rơi
 * THẲNG về `cauThayThe` — một câu máy con tự ghép, luôn đúng mà cũng luôn vô cảm:
 * không biết bé vừa nói gì, không khen, không sửa. Với mô hình giả "lặp 40%" thì
 * gần nửa buổi bé nói chuyện với cái máy ghép câu ấy.
 *
 * Nên thêm một nấc: nói cho mô hình biết nó sai CHỖ NÀO rồi xin lại. Tệp này canh
 * đúng bốn thứ dễ hỏng của nấc ấy, cả bốn chạy được bằng `node` không cần mạng:
 *   1. ĐẾM ĐƯỢC số lời gọi mạng — vòng có trần cứng, và trần là HẰNG;
 *   2. qua rồi thì KHÔNG gọi thêm (vòng không được tự chạy cho đủ số);
 *   3. hết vòng vẫn trượt thì `cauThayThe` VẪN LÀ đường lùi cuối;
 *   4. lượt bị bác KHÔNG lọt vào lịch sử bé thấy — bé không bao giờ nghe cô
 *      "nói nhầm rồi tự sửa".
 *
 * Tiêm hàm mạng qua tham số (`{ goi }`), không mock module — §0 luật 7.
 */
import { test, mock } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { vonTu, SUA_CO_TOI_DA, NHAC_SUA_TOI_DA_CHU } from '../src/mon/tienganh/lib/phongnoi.js';
import {
  hoiCoGiao, LOI_SUA_CO, LOI_LOI_VIET, TRA_LAI_TOI_DA_CHU,
} from '../src/mon/tienganh/lib/goiPhongNoi.js';

/* Fixture giống `tienganh_phongnoi.test.mjs`: mẫu câu THẬT luôn có công thức với ô
   trống, và loại ô trống quyết định điền được gì vào. */
const bai = (id, tu, cau) => ({
  id,
  title: `Unit ${id}`,
  hinhTu: [],
  knowledgeCore: {
    vocabulary: tu.map((t) => ({ tu: t, nghia: `nghĩa ${t}`, ipa: `/${t}/` })),
    mauCauDs: cau.map((c) => (Array.isArray(c)
      ? { cau: c[0], congThuc: c[1], dungDe: 'để nói' }
      : { cau: c, congThuc: c, dungDe: 'để nói' })),
  },
});

const U1 = bai('U1', ['ball', 'bike', 'book'], [["Hi, I'm Bill.", "Hi, I'm + [Name]."]]);
const VON = vonTu({ baiNay: U1 });

/* Lịch sử: cô đã nói "Hi, I'm Bo.", bé đã nhại lại và được 8 điểm. Chính câu ấy là
   `cauTruoc` của luật chống lặp. */
const LICH_SU = () => ([
  { vai: 'may', chu: "Hi, I'm Bo.", en: "Hi, I'm Bo.", vi: 'Con nghe rồi nói lại nhé.' },
  { vai: 'be', chu: 'hi im bo', diem: 8 },
]);

/** Hàm mạng giả: trả lần lượt theo danh sách, và CHỤP LẠI gói gửi lên mỗi lần.
 *
 *  ⚠ Phải chụp bản SAO. `hoiCoGiao` push thêm lượt vào chính mảng `messages` ấy,
 *  nên giữ tham chiếu thì cả ba lần gọi cùng trỏ vào một mảng — xem gói "lần 2"
 *  thì thấy luôn cả lượt của lần 3, và cổng xanh mà chẳng canh gì. */
function mayGia(ds) {
  const goi = [];
  const f = mock.fn(async (messages) => {
    goi.push(messages.map((m) => ({ ...m })));
    const o = ds[Math.min(goi.length - 1, ds.length - 1)];
    return { data: { chu: JSON.stringify(o), mauPrompt: 'luyennoi', phienBanMau: 1,
                     vanTayPrompt: 'abc123' } };
  });
  f.goi = goi;
  return f;
}

const dem = () => ({ ...LOI_SUA_CO });

/* ═══════════ VÒNG GỌI LẠI ═══════════ */

test('lặp lượt trước → gọi lại 1 lần rồi nhận câu mới', async () => {
  const truoc = dem();
  const goi = mayGia([
    { en: "Hi, I'm Bo.", vi: 'Con nghe rồi nói lại nhé.' },   // lặp → bị bác
    { en: "Hi, I'm Lan.", vi: 'Con nghe rồi nói lại nhé.' },  // khác → qua
  ]);
  const lichSu = LICH_SU();
  const tra = await hoiCoGiao({ von: VON, lichSu, tenBe: 'Lan', lop: 1 }, { goi });

  assert.equal(goi.mock.callCount(), 2, 'phải gọi lại ĐÚNG một lần');
  assert.equal(tra.en, "Hi, I'm Lan.");
  assert.equal(tra.lanSua, 1);
  assert.equal(tra.daThay, undefined, 'không phải thay bằng câu máy dựng');

  /* Lời nhắc sửa đi dưới vai `user`, không phải `system` thứ hai — `soiGoi` bác
     thẳng gói có lời dặn nằm ở vị trí khác 0. */
  const lan2 = goi.goi[1];
  const nhac = lan2[lan2.length - 1];
  assert.equal(nhac.role, 'user');
  assert.match(nhac.content, /repeated/);
  assert.equal(lan2.filter((m) => m.role === 'system').length, 1,
    'chỉ được MỘT lời dặn, và nó phải ở đầu gói');
  assert.equal(lan2[0].role, 'system');
  /* Câu bị bác phải quay lại dưới vai `assistant` — không có nó thì "câu ấy" trong
     lời nhắc không trỏ vào đâu cả. */
  assert.equal(lan2[lan2.length - 2].role, 'assistant');
  assert.match(lan2[lan2.length - 2].content, /Hi, I'm Bo\./);

  const sau = dem();
  assert.equal(sau.so - truoc.so, 1);
  assert.equal(sau.thanh - truoc.thanh, 1);
});

test('trượt cả 2 vòng → lui về cauThayThe, daThay true', async () => {
  const truoc = dem();
  /* "chips" không có trong vốn U1 — bác với lý do `ngoaiVon` lần nào cũng thế. */
  const goi = mayGia([{ en: 'I like chips.', vi: 'Con nghe rồi nói lại nhé.' }]);
  const tra = await hoiCoGiao({ von: VON, lichSu: LICH_SU(), tenBe: 'Lan', lop: 1 }, { goi });

  assert.equal(goi.mock.callCount(), 1 + SUA_CO_TOI_DA, 'một lần đầu + đủ trần vòng');
  assert.equal(tra.lanSua, SUA_CO_TOI_DA);
  assert.equal(tra.daThay, true);
  assert.ok([U1.knowledgeCore.vocabulary[0].tu, "Hi, I'm Bill."].includes(tra.en),
    `câu lùi phải là TỪ hoặc CÂU của bài, nhận được: ${tra.en}`);

  const sau = dem();
  assert.equal(sau.so - truoc.so, SUA_CO_TOI_DA);
  assert.equal(sau.thanh - truoc.thanh, 0);
  assert.equal(sau.ganNhat, 'ngoaiVon', 'lý do bác gần nhất phải có tên');
});

test('qua ngay → KHÔNG gọi lại', async () => {
  const truoc = dem();
  const goi = mayGia([{ en: 'ball', vi: 'Con nghe rồi nói lại từ “ball” nhé.' }]);
  const tra = await hoiCoGiao({ von: VON, lichSu: LICH_SU(), tenBe: 'Lan', lop: 1 }, { goi });

  assert.equal(goi.mock.callCount(), 1);
  assert.equal(tra.lanSua, 0);
  assert.equal(tra.en, 'ball');
  assert.equal(dem().so - truoc.so, 0, 'qua ngay thì không được đếm là một lần xin lại');
});

test('lượt bị bác KHÔNG lọt vào lịch sử bé thấy', async () => {
  const goi = mayGia([
    /* Câu bị bác là một câu HẲN HOI, chỉ dùng từ ngoài bài — nếu nó rò ra ngoài
       thì tìm chữ "chips" là thấy ngay. */
    { en: 'Hello chips!', vi: 'Con nghe rồi nói lại nhé.' },
    { en: 'bike', vi: 'Con nghe rồi nói lại nhé.' },
  ]);
  const lichSu = LICH_SU();
  const tra = await hoiCoGiao({ von: VON, lichSu, tenBe: 'Lan', lop: 1 }, { goi });

  assert.equal(tra.en, 'bike');
  assert.equal(tra.lanSua, 1);
  assert.equal(lichSu.length, 2, 'hoiCoGiao KHÔNG được đụng vào lịch sử truyền vào');
  /* Không một trường nào của lượt trả về mang câu đã bị bác, và cũng không có mảng
     lượt phụ nào đi kèm. */
  for (const [k, v] of Object.entries(tra)) {
    assert.ok(!Array.isArray(v), `trường "${k}" là mảng — lượt phụ đang rò ra ngoài`);
    assert.ok(!String(v ?? '').includes('chips'),
      `trường "${k}" còn mang câu đã bị bác`);
  }
});

/* ═══════════ VÒNG CHO LỜI TIẾNG VIỆT ═══════════ */

test('lời Việt hỏng → xin lại MỘT lần trước khi lui', async () => {
  const truoc = { ...LOI_LOI_VIET };
  const goi = mayGia([
    /* Câu tiếng Anh ĐÚNG ngay, chỉ lời Việt gọi bé bằng "bạn" — đúng lỗi bác bắt. */
    { en: 'ball', vi: 'Bạn nói lại đi.' },
    { en: 'ball', vi: 'Con nghe rồi nói lại nhé.' },
  ]);
  const tra = await hoiCoGiao({ von: VON, lichSu: LICH_SU(), tenBe: 'Lan', lop: 1 }, { goi });

  assert.equal(goi.mock.callCount(), 2);
  assert.equal(tra.lanSua, 0, 'câu tiếng Anh không phải sửa lần nào');
  assert.equal(tra.lanSuaViet, 1);
  assert.equal(tra.vi, 'Con nghe rồi nói lại nhé.');
  assert.equal(LOI_LOI_VIET.so - truoc.so, 0, 'xin lại ăn thì KHÔNG phải lui');

  const nhac = goi.goi[1][goi.goi[1].length - 1];
  assert.equal(nhac.role, 'user');
  assert.match(nhac.content, /Rewrite ONLY the Vietnamese line/);
  assert.match(nhac.content, /"ball"/, 'phải dặn giữ nguyên câu tiếng Anh đã đúng');
});

test('xin lại lời Việt vẫn hỏng → lui về lời viết sẵn, ĐÚNG một vòng', async () => {
  const truoc = { ...LOI_LOI_VIET };
  const goi = mayGia([{ en: 'ball', vi: 'Bạn nói lại đi.' }]);
  const tra = await hoiCoGiao({ von: VON, lichSu: LICH_SU(), tenBe: 'Lan', lop: 1 }, { goi });

  assert.equal(goi.mock.callCount(), 2, 'lời Việt chỉ được xin lại MỘT lần, không phải hai');
  assert.equal(tra.lanSuaViet, undefined);
  assert.equal(tra.vi, 'Con nghe rồi nói lại nhé.', 'lui về LUI_CHUNG');
  assert.equal(LOI_LOI_VIET.so - truoc.so, 1, 'lui thì vẫn phải đếm như xưa');
});

test('mất mạng giữa vòng xin lại lời Việt thì LUI, không làm hỏng cả lượt', async () => {
  let lan = 0;
  const goi = async () => {
    lan += 1;
    if (lan === 1) return { data: { chu: JSON.stringify({ en: 'ball', vi: 'Bạn nói lại đi.' }) } };
    const e = new Error('mất mạng');
    e.code = 'functions/unavailable';
    throw e;
  };
  const tra = await hoiCoGiao({ von: VON, lichSu: LICH_SU(), tenBe: 'Lan', lop: 1 }, { goi });
  assert.equal(tra.en, 'ball', 'câu tiếng Anh đã có trong tay thì không được mất');
  assert.equal(tra.vi, 'Con nghe rồi nói lại nhé.');
});

/* ═══════════ VÂN TAY VÀ TRẦN ═══════════ */

test('vân tay lời dặn KHÔNG đổi qua các vòng — lời dặn không đổi một chữ', async () => {
  const goi = mayGia([
    { en: "Hi, I'm Bo.", vi: 'Con nghe rồi nói lại nhé.' },
    { en: "Hi, I'm Lan.", vi: 'Con nghe rồi nói lại nhé.' },
  ]);
  const tra = await hoiCoGiao({ von: VON, lichSu: LICH_SU(), tenBe: 'Lan', lop: 1 }, { goi });
  assert.equal(tra.mauPrompt, 'luyennoi');
  assert.equal(tra.phienBanMau, 1);
  assert.equal(tra.vanTayPrompt, 'abc123');
  /* Lời dặn ở gói lần 2 phải Y NGUYÊN lời dặn lần 1: vòng gọi lại chỉ thêm lượt
     `user`, không được sửa lời dặn — sửa thì vân tay nói dối về mẫu đã dùng. */
  assert.equal(goi.goi[1][0].content, goi.goi[0][0].content);
});

test('gói gửi lên vẫn dưới trần lượt của máy chủ dù đã sửa đủ vòng', async () => {
  const goi = mayGia([{ en: 'I like chips.', vi: 'Con nghe rồi nói lại nhé.' }]);
  /* Lịch sử dài hơn `LUOT_GUI_TOI_DA` — `goiGui` cắt còn 12. */
  const dai = [];
  for (let i = 0; i < 30; i += 1) {
    dai.push({ vai: i % 2 ? 'be' : 'may', chu: `luot ${i}`, en: `luot ${i}` });
  }
  await hoiCoGiao({ von: VON, lichSu: dai, tenBe: 'Lan', lop: 1 }, { goi });
  const { TOI_DA_LUOT } = await import('../functions/src/luyennoi.js');
  for (const g of goi.goi) {
    assert.ok(g.length <= TOI_DA_LUOT, `gói ${g.length} lượt, quá trần ${TOI_DA_LUOT}`);
  }
});

test('TRẦN LÀ HẰNG, không phải số viết thẳng trong vòng lặp', () => {
  const src = readFileSync(new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8');
  assert.match(src, /lanSua < SUA_CO_TOI_DA/,
    'vòng phải so với hằng — ghim số vào đây thì cổng này canh một con số không ai dùng');
  assert.ok(!/lanSua < \d/.test(src), 'có số viết thẳng làm trần vòng');
  assert.equal(SUA_CO_TOI_DA, 2);
  assert.equal(NHAC_SUA_TOI_DA_CHU, 300);
  assert.equal(TRA_LAI_TOI_DA_CHU, 600);
  /* `cauThayThe` là đường lùi CUỐI — gỡ nó ra là bé nghe câu sai. */
  assert.match(src, /cauThayThe\(viec, tenBe, cauTruoc\)/);
});
