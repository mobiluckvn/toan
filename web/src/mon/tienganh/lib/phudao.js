/**
 * BÀI PHỤ ĐẠO — vá đúng chỗ bé đang mắc (mục 2.5.1 nhánh ba · 2.4.1).
 *
 * Bé sai ba lần liền ở một nút. Luyện thêm câu cùng loại thì bé sai tiếp — cái
 * hổng có thể nằm ở nút TIÊN QUYẾT chứ không ở đây (mục 2.3.3 đã tìm ra nó ở Đợt
 * 3). Bài phụ đạo nhắm vào nút gốc rễ ấy.
 *
 * ── BA BƯỚC, VÀ BƯỚC BA LÀ BƯỚC KHÔNG ĐƯỢC BỎ ──
 *   1. tìm nút gốc rễ                    (`nutGocRe`, Đợt 3)
 *   2. gom câu quanh nút ấy               — TĨNH trước, LLM sau
 *   3. SOI LẠI mọi câu bằng `cauHopLe()`  — kể cả câu tĩnh
 *
 * ── ⚠ ĐƯỜNG LÙI LÀ BẮT BUỘC, KHÔNG PHẢI TÍNH NĂNG PHỤ ──
 * Bé đang học dở, vừa sai ba câu liền, và màn hình hứa sẽ giúp. Nếu lúc ấy gọi
 * mạng hỏng mà bé nhận được màn trắng thì đó là hỏng NẶNG HƠN không có phụ đạo:
 * bé vừa mất mạch học, vừa mất niềm tin vào cái nút vừa bấm.
 *
 * Nên thứ tự là NGƯỢC với trực giác: lấy câu TĨNH của chính nút gốc rễ TRƯỚC, đủ
 * rồi thì thôi. LLM chỉ được gọi khi kho tĩnh không đủ — và gọi hỏng thì vẫn còn
 * phần tĩnh đã có trong tay.
 *
 * ── ⚠ CÂU LLM SINH RA CŨNG PHẢI QUA HẬU KIỂM ──
 * Đây là chỗ duy nhất trong cả app mà câu hỏi KHÔNG do bộ sinh dựng sẵn, tức là
 * không có 83 cổng nào soi trước khi tới tay bé. `cauHopLe()` là hàng rào duy
 * nhất còn lại. Bỏ nó đi để "cho nhanh" là mở đúng cái cửa mà cả tầng chống ảo
 * giác từ vựng sinh ra để đóng.
 */
import { nutGocRe } from './lantruyen.js';
import { baiCuaNut } from './doThi.js';
import { soiCau as soiMotCau } from './phongnoi.js';
import { cauChanDoan, chamCauTinh } from './chandoan.js';

/** Bài phụ đạo dài bao nhiêu câu. Ngắn — đây là chỗ gỡ, không phải bài học mới. */
export const SO_CAU_PHU_DAO = 4;

/**
 * Gom câu TĨNH quanh một nút, từ những bài đã tải sẵn.
 *
 * @param baiDs  [bài] các bài đang có trong tay (bài hiện tại + bài tiên quyết)
 *
 * ⚠ Ưu tiên câu BẬC THẤP. Bé đang mắc thì đừng đưa câu khó nhất của nút ấy —
 * mục đích là gỡ, và gỡ thì bắt đầu từ chỗ bé làm được.
 */
export function cauTinhCuaNut(baiDs, maNut, { soCau = SO_CAU_PHU_DAO } = {}) {
  if (!maNut) return [];
  const uu = ['warmup', 'standard', 'challenge'];
  const ra = [];
  for (const khoa of uu) {
    for (const b of (baiDs || [])) {
      for (const c of (b?.practice?.pools?.[khoa] || [])) {
        if (!c?.id) continue;
        if (c.maNut !== maNut && !(c.maNutDs || []).includes(maNut)) continue;
        if (ra.some((x) => x.id === c.id)) continue;
        ra.push(c);
        if (ra.length >= soCau) return ra;
      }
    }
  }
  return ra;
}

/**
 * MỌI CHUỖI TIẾNG ANH MÀ MỘT CÂU HỎI BÀY RA CHO BÉ.
 *
 * Chỉ lấy phần bé PHẢI ĐỌC hoặc PHẢI NÓI:
 *   · `choices`  — các phương án của câu bấm chọn, mỗi phương án một từ/cụm;
 *   · `the`      — dãy thẻ, ghép lại thành câu (thẻ chữ cái thì ghép ra một từ).
 * KHÔNG lấy `text` (lời dẫn tiếng Việt) và `hints` (gợi ý tiếng Việt), cũng không
 * lấy `solutionNarrative` — chuỗi ấy trộn tiếng Anh với nghĩa tiếng Việt trong một
 * dòng, soi nó bằng vốn từ tiếng Anh thì bác nhầm gần hết.
 */
export function enCuaCau(cau) {
  const ra = [];
  for (const c of (cau?.choices || [])) if (typeof c === 'string') ra.push(c);
  if (Array.isArray(cau?.the) && cau.the.length) {
    /* ⚠ THẺ CHỮ CÁI GHÉP LIỀN, THẺ TỪ GHÉP BẰNG DẤU CÁCH.
       Bậc "Gõ lại" phát thẻ từng CHỮ CÁI (`['b','a','l','l']` → "ball", và khoảng
       trắng cũng là một thẻ: `['b','r','e','a','k',' ','t','i','m','e']`). Bậc
       "Ráp câu" phát thẻ từng TỪ (`['I','like','fish.']` → "I like fish.").
       Phân biệt theo ĐỘ DÀI thẻ, không theo "có thẻ khoảng trắng không": bản đầu
       dùng dấu hiệu ấy nên `['b','a','l','l']` — thẻ chữ cái của một từ KHÔNG có
       khoảng trắng — ghép ra "b a l l" rồi bị hậu kiểm bác oan. Cổng bắt được ngay
       lượt chạy đầu tiên. */
    const laChuCai = cau.the.every((x) => String(x).length <= 1);
    ra.push(cau.the.join(laChuCai ? '' : ' '));
  }
  return ra.filter((x) => String(x || '').trim());
}

/**
 * HẬU KIỂM MỘT CÂU HỎI — vỏ nối `soiCau` (nhận CHUỖI) với `dungPhuDao` (đưa CÂU).
 *
 * ⚠ VÌ SAO PHẢI CÓ VỎ NÀY. Chú thích cũ của `dungPhuDao` ghi "chỗ gọi thật PHẢI
 * truyền `cauHopLe`", nhưng `cauHopLe(en, opt)` nhận một CHUỖI còn `soiCau` ở đây
 * được gọi với cả ĐỐI TƯỢNG câu hỏi. Truyền thẳng `cauHopLe` vào thì nó đem một
 * object đi chuẩn hoá, ra chuỗi vô nghĩa, và BÁC SẠCH mọi câu — bài phụ đạo luôn
 * rỗng. Hỏng lặng lẽ, vì "không có câu nào" trông y hệt "kho tĩnh không có gì".
 * Tìm ra 26-08 lúc nối phụ đạo vào màn học.
 *
 * Trả `true` khi MỌI chuỗi tiếng Anh của câu đều hợp lệ. Câu không bày chuỗi tiếng
 * Anh nào (ví dụ câu nghe rồi chọn hình) thì không có gì để bác — cho qua.
 */
export function cauHoiHopLe(cau, { von, tenBe = '' } = {}) {
  if (!von) return true;                     // không có vốn thì không soi được
  return enCuaCau(cau).every((en) => soiMotCau(en, { von, tenBe }).ok);
}

/**
 * Dựng một bài phụ đạo.
 *
 * @param goiLLM  async ({maNut, von, soCau}) => [câu] — KHÔNG bắt buộc. Thiếu, hay
 *                ném lỗi, hay trả rỗng: phụ đạo vẫn ra bài bằng phần tĩnh.
 * @param soiCau  (câu) => bool — hậu kiểm, nhận ĐỐI TƯỢNG CÂU HỎI. Chỗ gọi thật
 *                truyền `cauHoiHopLe` (xem vỏ ngay trên), KHÔNG phải `cauHopLe`.
 *
 * Trả `{ nutGoc, cau, nguon, luiVe }`:
 *   nguon  'tinh' | 'llm' | 'tron'
 *   luiVe  true khi đã phải lùi vì LLM hỏng — để màn hình và nhật ký biết.
 */
export const VONG_TOI_DA = 2;

export async function dungPhuDao({
  dt, mucThao, maNutMac, baiDs = [], von = null, nhan = null,
  goiLLM = null, soiCau = () => true, soCau = SO_CAU_PHU_DAO,
  toiDaVong = VONG_TOI_DA,
}) {
  /* Nút gốc rễ — nếu không tìm được thì vá ngay tại chỗ bé mắc. Đó không phải
     thất bại: nhiều nút không có tiên quyết nào, và chính nó là gốc. */
  const xepGoc = nutGocRe(dt, mucThao, maNutMac, { toiDa: Math.max(1, toiDaVong) });
  const goc = xepGoc[0]?.ma || maNutMac;

  /* ── VÒNG 1: nút gốc rễ #1, kho TĨNH ──
     ⚠ CHẤM TỪNG CÂU BẰNG `chamCauTinh`, không chỉ lọc theo `cauTinhCuaNut`. Hàm ấy
     nhận câu khi nút nằm trong `maNutDs` — mà `maNutDs` là MỌI nút câu ấy chạm tới,
     nên một câu ôn tập cuối chương "thuộc" cả năm nút. Lấy nó đi phụ đạo cho một
     nút cụ thể thì bé làm một câu rộng hơn hẳn chỗ nó đang mắc, mà hệ thống vẫn ghi
     "đã phụ đạo nút ấy" — ΔC đo ra một con số về một việc không xảy ra. */
  const lay = (nut) => cauTinhCuaNut(baiDs, nut, { soCau })
    .filter((c) => chamCauTinh(c, { maNut: nut, doThi: dt }) && soiCau(c));

  const tinh = lay(goc);
  /* ── VÒNG 2: nút gốc rễ #2 ──
     Vòng 1 thiếu câu thì thử nút gốc rễ KẾ TIẾP trước khi nghĩ tới mô hình: một câu
     tĩnh của nút #2 vẫn là câu đã qua bộ sinh và 83 cổng, còn câu mô hình sinh thì
     chỉ có `soiCau` đỡ. Rẻ hơn, chắc hơn, và không tốn lời gọi nào. */
  const vong = [{ nut: goc, cau: tinh }];
  for (let i = 1; i < Math.min(toiDaVong, xepGoc.length) && tongCau(vong) < soCau; i += 1) {
    const nut = xepGoc[i]?.ma;
    if (!nut || nut === goc) continue;
    vong.push({ nut, cau: lay(nut).filter((c) => !coCau(vong, c)) });
  }
  const tinhCaVong = vong.flatMap((v) => v.cau);

  if (tinhCaVong.length >= soCau || !goiLLM) {
    return {
      nutGoc: goc, cau: tinhCaVong.slice(0, soCau), nguon: 'tinh', luiVe: false,
      baiGoc: baiCuaNut(dt, goc) || null,
      soVong: vong.length,
      nutDaThu: vong.map((v) => v.nut),
      chanDoan: cauChanDoan({ dt, nutSai: maNutMac, nutGocRe: goc, nhan }),
    };
  }
  const tinh2 = tinhCaVong;

  /* Kho tĩnh không đủ → nhờ LLM. Hỏng thì GIỮ phần tĩnh đã có, không ném lên. */
  let them = [];
  let luiVe = false;
  try {
    /* ⚠ ĐÚNG MỘT LỜI GỌI cho mỗi lần phụ đạo (trần của §7). Bé đang chờ một bài
       tập, không chờ một cuộc hội thoại. */
    const r = await goiLLM({ maNut: goc, von, nhan, soCau: soCau - tinh2.length });
    them = Array.isArray(r) ? r : [];
  } catch { luiVe = true; them = []; }
  if (!them.length) luiVe = true;

  /* ⚠ HẬU KIỂM TỪNG CÂU MỘT. Câu LLM sinh là câu DUY NHẤT trong app không đi qua
     bộ sinh và 83 cổng; `soiCau` là hàng rào cuối cùng. */
  /* Lọc cả BỘ trước khi lọc từng câu: bốn câu y hệt nhau thì từng câu đều hợp lệ,
     cả bộ thì là một câu hỏi lặp bốn lần. Xem `soiBoCauAI`. */
  const { cau: themGon } = soiBoCauAI(them.filter((c) => c && c.id));
  const sach = themGon.filter((c) => soiCau(c))
    /* Câu do mô hình sinh phải ĐEO NHÃN NGUỒN. Đây là câu DUY NHẤT trong app không
       đi qua bộ sinh và 83 cổng; không đeo nhãn thì sau này nhìn nhật ký không biết
       câu nào do ai sinh, mà đó đúng là thứ cần biết nhất khi đo. */
    .map((c) => ({ ...c, nguon: 'ai' }));
  const cau = [...tinh2.map((c) => ({ ...c, nguon: c.nguon || 'tinh' })), ...sach]
    .slice(0, soCau);
  return {
    nutGoc: goc,
    cau,
    nguon: sach.length ? (tinh2.length ? 'tron' : 'llm') : 'tinh',
    luiVe: luiVe || sach.length < them.length,
    baiGoc: baiCuaNut(dt, goc) || null,
    soVong: vong.length,
    nutDaThu: vong.map((v) => v.nut),
    chanDoan: cauChanDoan({ dt, nutSai: maNutMac, nutGocRe: goc, nhan }),
    /* Câu mô hình sinh CHỜ NGƯỜI LỚN DUYỆT trước khi vào kho tĩnh — xem
       `choDuyetTA` trong `firestore.rules`. Trả ra đây để màn hình đẩy lên.
       ⚠ CHỈ những câu BÉ THẬT SỰ LÀM, không phải mọi câu hợp lệ mô hình trả về.
       `sach` có thể nhiều hơn chỗ trống trong bài; đẩy cả lên thì hàng đợi duyệt
       đầy những câu chưa ai thấy, và người lớn duyệt một câu không biết nó đã dạy
       bé điều gì. */
    choDuyet: cau.filter((c) => c.nguon === 'ai'),
  };
}

/* Hai phép đếm nhỏ cho vòng — gom lại để thân hàm trên đọc được. */
const tongCau = (vong) => vong.reduce((n, v) => n + v.cau.length, 0);
const coCau = (vong, c) => vong.some((v) => v.cau.some((x) => x.id === c.id));

/* ═══════════ HẬU KIỂM RIÊNG CHO CÂU DO MÔ HÌNH SINH (việc V9) ═══════════ */

/**
 * ── VÌ SAO `cauHoiHopLe` MỘT MÌNH KHÔNG ĐỦ ──
 * Khối chú thích ở cuối `PhuDao.jsx` nói đúng chỗ khó: `cauHoiHopLe` soi VỐN TỪ —
 * nó trả lời "câu này có dùng chữ bé đã học không". Một CÂU HỎI thì còn sáu thứ nữa
 * có thể sai mà vốn từ không nói được một chữ nào:
 *
 *   · hai phương án TRÙNG NHAU và một trong hai là đáp án → câu có HAI đáp án đúng,
 *     bé chọn đúng mà bị chấm sai;
 *   · đáp án KHÔNG nằm trong danh sách phương án → không có cách nào trả lời đúng;
 *   · gợi ý LỘ THẲNG đáp án → câu thành câu đọc chép;
 *   · chỉ một phương án → không phải câu hỏi;
 *   · lời dẫn rỗng → bé không biết phải làm gì;
 *   · lời dẫn có số → vi phạm luật chung của phần phụ đạo.
 *
 * Sáu thứ ấy đều KIỂM ĐƯỢC BẰNG CODE, nên không có lý gì thả chúng. Đây là tầng
 * hậu kiểm mà chú thích cũ nói "phải thêm cùng lúc với mô hình" — nay thêm rồi.
 *
 * ⚠ Nó KHÔNG kiểm được cái thứ bảy: phương án nhiễu có thật là "cái sai trẻ hay
 * mắc" hay chỉ là một chữ bừa trong vốn. Chuyện ấy cần người đọc — và đó đúng là
 * việc của hàng đợi `choDuyetTA`.
 */
/**
 * ĐÁP ÁN CỦA MỘT CÂU — đọc được cả hai hình dạng, và đó không phải sự tuỳ tiện.
 *
 * Câu của kho tĩnh để đáp án ở `answerKey.choice`; mô hình thì trả về một chuỗi
 * `answer`. Phép hậu kiểm chạy TRƯỚC lúc `dungCau` chuẩn hoá (nó soi cả gói thô
 * mô hình vừa trả), nên nó phải đọc được cả hai — còn `cham.js` thì CHỈ hiểu
 * `answerKey.choice`, và đó là lý do `dungCau` phải dựng đúng hình dạng ấy.
 *
 * ⚠ Bản trước đọc `String(cau.answerKey)` nên khi `answerKey` thành object thì ra
 * `"[object Object]"` và mọi câu đều bị bác "đáp án không nằm trong các phương án".
 */
export const dapCuaCau = (c) => String(
  (c?.answerKey && typeof c.answerKey === 'object' ? c.answerKey.choice : c?.answerKey)
  ?? c?.answer ?? '',
).trim();

export const SO_CHON_TOI_THIEU = 2;

export function soiCauAI(cau) {
  if (!cau) return { ok: false, vi: 'không có câu' };
  const text = String(cau.text || '').trim();
  if (!text) return { ok: false, vi: 'lời dẫn rỗng' };
  if (/\d/.test(text)) return { ok: false, vi: 'lời dẫn có chữ số' };

  const chon = (cau.choices || []).map((c) => String(c || '').trim()).filter(Boolean);
  if (chon.length < SO_CHON_TOI_THIEU) {
    return { ok: false, vi: `chỉ ${chon.length} phương án — không phải câu hỏi` };
  }
  const gon = (x) => x.toLowerCase().replace(/[^a-z0-9' ]/g, '').replace(/\s+/g, ' ').trim();
  if (new Set(chon.map(gon)).size !== chon.length) {
    return { ok: false, vi: 'có hai phương án trùng nhau' };
  }
  const dap = dapCuaCau(cau);
  if (!dap) return { ok: false, vi: 'không có đáp án' };
  if (!chon.map(gon).includes(gon(dap))) {
    return { ok: false, vi: 'đáp án không nằm trong các phương án' };
  }
  /* ⚠ ĐÁP ÁN LỘ TRONG LỜI DẪN — không chỉ trong gợi ý.
     Đo thật 09-10 bắt được: mô hình sinh ra lời dẫn tiếng Việt `Bạn của tôi luôn
     nói: I like fish.` cho câu có đáp án đúng là `I like fish`. Bé chỉ việc chép
     lại. Bản đầu của phép soi chỉ ngó `hints`, nên câu ấy đi lọt.
     So theo TIẾNG, không `includes`: gợi ý "con chọn chữ có ba chữ cái" không được
     bắt oan chỉ vì đáp án là "cat" và trong đó có "ca". */
  const tiengCua = (x) => new Set(String(x || '').toLowerCase()
    .split(/[^a-z']+/).filter(Boolean));
  const tuDap = gon(dap).split(' ').filter(Boolean);
  const lo = (x) => {
    const t = tiengCua(x);
    return tuDap.length > 0 && tuDap.every((w) => t.has(w));
  };
  if (lo((cau.hints || []).join(' '))) return { ok: false, vi: 'gợi ý lộ thẳng đáp án' };
  if (lo(text)) return { ok: false, vi: 'lời dẫn lộ thẳng đáp án' };
  return { ok: true, vi: '' };
}

/**
 * SOI CẢ BỘ CÂU — thứ soi từng câu một không thấy được.
 *
 * ⚠ Đo thật 09-10: mô hình trả về BỐN câu với ĐÚNG MỘT bộ phương án và ĐÚNG MỘT
 * đáp án (`I like fish` bốn lần, chỉ khác lời dẫn tiếng Việt). Từng câu một thì cả
 * bốn đều hợp lệ; cả bộ thì đó là một câu hỏi lặp bốn lần, và bé làm bốn lần cùng
 * một việc rồi hệ thống ghi "đã phụ đạo bốn câu".
 *
 * Trả về bộ ĐÃ LỌC kèm những câu bị bỏ — để `LOI_SINH` còn đếm được.
 */
export function soiBoCauAI(ds = []) {
  const giu = [];
  const boQua = [];
  const gon = (x) => String(x || '').toLowerCase().replace(/[^a-z0-9' ]/g, '')
    .replace(/\s+/g, ' ').trim();
  const daCo = new Set();
  for (const c of ds) {
    /* Dấu vết của một câu = ĐÁP ÁN + TẬP PHƯƠNG ÁN. Hai câu cùng dấu vết là cùng
       một câu hỏi, dù lời dẫn tiếng Việt viết khác đi. */
    const dap = gon(dapCuaCau(c));
    const chon = (c?.choices || []).map(gon).sort().join('|');
    const t = gon(c?.text);
    /* ⚠ KHÔNG CÓ DẤU VẾT THÌ ĐỪNG DỌN. Một câu không có đáp án lẫn phương án lẫn
       lời dẫn thì mọi câu như thế ra CÙNG một dấu vết rỗng, và phép dọn gộp chúng
       làm một — trong khi chúng có thể là hai câu khác nhau. Câu rỗng hình dạng thì
       đã có `soiCauAI` bác; dọn chúng ở đây vừa vô nghĩa vừa đổi hành vi của chỗ
       gọi dùng phép hậu kiểm khác. Cổng `CÂU LLM SINH RA PHẢI QUA HẬU KIỂM` bắt
       được đúng chỗ này. */
    const v = (dap || chon) ? `${dap}@${chon}` : null;
    if (v && daCo.has(v)) { boQua.push({ cau: c, vi: 'trùng câu hỏi khác trong cùng bộ' }); continue; }
    if (t && daCo.has(`t:${t}`)) { boQua.push({ cau: c, vi: 'trùng lời dẫn' }); continue; }
    if (v) daCo.add(v);
    if (t) daCo.add(`t:${t}`);
    giu.push(c);
  }
  return { cau: giu, boQua };
}
