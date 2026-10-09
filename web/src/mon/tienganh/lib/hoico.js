/**
 * BÉ HỎI LẠI THÌ CHO CÔ ĐI TRA (việc V11, mẫu #5 ReAct) — luật THUẦN của máy con.
 *
 * Ba tầng, đúng khuôn mọi phần gọi mô hình của kho này:
 *     hoico.js        luật thuần: rẽ hay không, gói `kho` gồm gì       ← tệp này
 *     goiPhongNoi.js  gọi máy chủ
 *     PhongNoi.jsx    vẽ, và phát clip khi cô xin
 *
 * ── VÌ SAO LUẬT RẼ NẰM Ở ĐÂY, KHÔNG NẰM TRONG `.jsx` HAY Ở MÁY CHỦ ──
 * Nó là một điều kiện hai nhánh quyết định buổi học của bé đi đường nào, nên nó
 * phải thử được bằng `node`. Để trong `.jsx` thì chỉ mở trình duyệt mới biết; để ở
 * máy chủ thì máy chủ phải biết bé học lớp mấy và nhãn lượt là gì — tức phải nhận
 * thêm hai thứ về bé mà nó không cần cho việc gì khác.
 *
 * ── VÀ VÌ SAO CHỈ LỚP 3 TRỞ LÊN ──
 * Không phải vì bé lớp 1–2 không biết hỏi. Chúng hỏi nhiều hơn. Lý lẽ ban đầu là:
 * câu hỏi của bé bé gần như luôn về MỘT chữ trong bài đang học, mà bài lớp 1 chỉ có
 * tám chữ — bảng vốn trong lời dặn ngắn tới mức mô hình không thể tra sai; từ lớp 3
 * vốn mới trộn thêm hai ba unit cũ nên bảng dài hẳn ra.
 *
 * ⚠ ĐO XONG THÌ LÝ LẼ ẤY KHÔNG ĐỨNG ĐƯỢC, và nó là lý do nhánh này MẶC ĐỊNH TẮT.
 * Bảng vốn một bài lớp 3–5 đo ra chỉ 7–13 chữ, không phải "hàng trăm" như tôi viết
 * khi dựng tệp này. Lý lẽ đầy đủ và bốn con số đo bằng mô hình thật: xem
 * `BAT_NHANH_TRA` ngay dưới. Giữ mốc lớp 3 vì nếu có ngày bật lại thì mốc ấy vẫn là
 * mốc đúng — nhưng đừng đọc đoạn trên như một sự thật đã kiểm.
 */
import { mucThaoCua, NGUONG_THAO, NGUONG_YEU } from './zpd.js';
import { nhanNut } from './doThi.js';
import { moiTuDuocDung } from './phongnoi.js';

/** Từ lớp này trở lên mới rẽ sang nhánh tra. Xem khối chú thích trên. */
export const LOP_TOI_THIEU = 3;

/**
 * ⚠ NHÁNH NÀY MẶC ĐỊNH **TẮT**, VÀ ĐÂY LÀ LÝ DO ĐẦY ĐỦ.
 *
 * Mã đã xong, đủ cổng (108 phép kiểm ở `test/luyennoi_tool.test.mjs`), có trần
 * bước, bắt lặp, và có đường lùi về nhánh cũ khi hỏng. Nhưng đo bằng Groq THẬT trên
 * 25 lượt (`node tools/do_hoi_co.mjs`) thì nó KHÔNG hơn nhánh cũ một chỗ nào:
 *
 *   bé hỏi nghĩa một chữ TRONG bài     cũ 10/10   ·  tra 10/10
 *   bé hỏi một chữ NGOÀI bài           cũ 10/10   ·  tra 10/10   (đúng = không dạy)
 *   bé hỏi chữ ấy ĐỌC THẾ NÀO                     ·  tra  0/5    ← tiêu chí §7
 *   tool được gọi                                 ·  4/25 lượt
 *
 * Ba điều rút ra, và điều thứ ba mới là điều quan trọng:
 *
 * 1 · GIẢ THUYẾT BAN ĐẦU SAI. Tôi viết ở trên rằng "từ lớp 3 bảng vốn dài tới mức
 *     tra thành việc làm theo cảm giác". Đo ra thì bảng một bài chỉ 7–13 chữ — ngắn
 *     tới mức mô hình không thể tra sai. Nó không cần tool để tìm một chữ trong
 *     mười ba chữ.
 *
 * 2 · HÀNG RÀO VỐN TỪ ĐÃ GIỮ ĐƯỢC MÀ KHÔNG CẦN TOOL. Chỗ tôi tưởng là lỗ hổng —
 *     bé hỏi `elephant` thì cô dịch luôn, tức dạy một chữ ngoài vốn — hoá ra lời
 *     dặn nhãn `hoiLai` (§9 A7) một mình đã chặn đủ: 10/10 lượt cô hẹn "mình học
 *     sau nhé" và KHÔNG dịch.
 *
 * 3 · TOOL `nghe_lai` TRÙNG VỚI MỘT KÊNH ĐÃ CÓ. Bé hỏi "đọc thế nào" thì mô hình
 *     đặt chính chữ ấy vào `en` — và `PhongNoi.jsx` vốn ĐỌC TO `tra.en` ở mọi lượt.
 *     Nghĩa là "phát chữ ấy cho bé nghe" là hành vi MẶC ĐỊNH, không phải một khả
 *     năng phải xin. Tool ấy không được gọi vì nó không có việc gì để làm. Tiêu chí
 *     "kèm clip" của §7 thật ra ĐÃ đạt — chỉ là đạt bằng đường cũ.
 *
 * Nên bật nó lên là thêm một callable, thêm một chặng mạng, thêm một mặt hỏng — để
 * đổi lấy đúng con số không. Giữ mã lại thì rẻ và có ích về sau: ngày nào một quyển
 * có bảng vốn vài trăm chữ, hay ngày nào cần một tool tra thứ mà lời dặn KHÔNG mang
 * sẵn (lịch ôn, bài trước đó), thì chỗ cắm đã có và đã được canh.
 *
 * Số phải xem trước khi bật: `LOI_HOI_CO.buoc / LOI_HOI_CO.goi` ở `goiPhongNoi.js`.
 * Quanh 0 thì không ai dùng tool, và lúc ấy việc đúng vẫn là để tắt.
 */
export const BAT_NHANH_TRA = false;

/**
 * Trần gói `kho` — PHẢI khớp trần bên `functions/src/tool_phongnoi.js`.
 *
 * ⚠ Hai bên hai hằng là cố ý, và có cổng canh chúng bằng nhau. Nhập chéo
 * `src/` ↔ `functions/` thì cổng `ranh_gioi.test.mjs` bác; mà bỏ trần ở một bên thì
 * bên kia bác cả gói và bé mất lượt. Nên: hai hằng, một phép kiểm.
 */
export const TOM_TAT_TOI_DA_CHU = 300;
export const TU_KHO_TOI_DA = 400;
export const CAU_KHO_TOI_DA = 80;

/** Nhiều nhất bao nhiêu chữ mỗi bên trong câu tóm tắt mức thạo. */
export const TU_MOI_BEN = 6;

/**
 * Lượt này có rẽ sang nhánh tra không?
 *
 * Ba điều phải đủ cả, và thiếu một là đi nhánh cũ — nhánh cũ vẫn trả lời được câu
 * hỏi của bé, chỉ là bằng bảng vốn trong lời dặn.
 *
 * ⚠ BÀI TẢ TRANH KHÔNG RẼ. Lời dặn của nó là lời dặn RIÊNG (bác chốt 19-08: "xoá
 * hết prompt cũ"), và nó không có bảng vốn theo khuôn cũ. Ghép thêm bốn tool vào đó
 * là mời mô hình quay về dạy nhại câu — đúng điều lời dặn ấy sinh ra để chặn.
 */
export function canHoiCo({ nhan, lop, laTranh = false, bat = BAT_NHANH_TRA } = {}) {
  /* Cờ đứng TRƯỚC mọi điều kiện khác, và nhận được qua tham số để cổng thử được cả
     hai trạng thái — một cờ chỉ thử được ở trạng thái mặc định là một cờ mà nửa
     đường còn lại không ai canh. */
  if (!bat) return false;
  if (laTranh) return false;
  if (nhan !== 'hoiLai') return false;
  return Number.isFinite(Number(lop)) && Number(lop) >= LOP_TOI_THIEU;
}

/**
 * TÓM TẮT MỨC THẠO — một câu tiếng Việt, KHÔNG SỐ.
 *
 * ⚠ KHÔNG SỐ, và đây không phải chuyện gu. Câu này đi vào kết quả tool, rồi mô hình
 * đọc nó và viết lời tiếng Việt cho bé nghe. Có con số trong đó thì sớm muộn cô nói
 * "con thạo chữ này tám mươi phần trăm" — một câu vô nghĩa với bé bảy tuổi, và là
 * một con số về bé đi ra khỏi chỗ nó được phép ở. Cùng lý lẽ với `dongHoSoAI` và
 * `tomTatChoLoiDan`.
 *
 * Thiếu dữ liệu thì trả CHUỖI RỖNG, đừng đoán: tool đọc chuỗi rỗng rồi nói "chưa có
 * ghi chú nào", và đó là một câu trả lời thật.
 */
export function tomTatMucThao({ von, mucThao, doThi } = {}) {
  if (!von || !mucThao || !doThi) return '';
  const moiTu = moiTuDuocDung(von);
  if (!moiTu.length) return '';

  /* Mã nút → chữ tiếng Anh. Nhãn nút từ vựng là `mango — quả xoài`, nên chữ đứng
     đầu nhãn là chữ cần. Đi từ NÚT sang CHỮ (không ngược lại) vì mã nút có tiền tố
     theo lớp và unit (`v_g5_u1_city`), mà máy con ở đây không biết tiền tố nào. */
  const chac = [];
  const chenh = [];
  const daCo = new Set();
  for (const ma of Object.keys(mucThao)) {
    const nhan = nhanNut(doThi, ma);
    if (!nhan) continue;
    const chu = String(nhan).split('—')[0].trim().toLowerCase();
    if (!chu || daCo.has(chu)) continue;
    /* CHỈ chữ của bài đang học (hoặc phần ôn) — mục thạo có cả nút của quyển khác,
       và nhắc một chữ bé chưa gặp trong buổi này thì chẳng giúp gì. */
    if (!moiTu.some((t) => String(t).toLowerCase() === chu)) continue;
    const p = mucThaoCua(mucThao, ma);
    if (p === null) continue;
    daCo.add(chu);
    if (p >= NGUONG_THAO) chac.push(chu);
    else if (p < NGUONG_YEU) chenh.push(chu);
  }
  if (!chac.length && !chenh.length) return '';

  const phan = [];
  if (chac.length) phan.push(`chữ con đã chắc: ${chac.slice(0, TU_MOI_BEN).join(', ')}`);
  if (chenh.length) phan.push(`chữ con còn ngại: ${chenh.slice(0, TU_MOI_BEN).join(', ')}`);
  return phan.join(' · ').slice(0, TOM_TAT_TOI_DA_CHU);
}

/**
 * DỰNG GÓI `kho` GỬI LÊN MÁY CHỦ.
 *
 * ⚠ CHỈ BA TRƯỜNG, và không trường nào mang chữ BÉ NÓI. Vốn từ và mẫu câu là dữ
 * liệu SÁCH (đã nằm trong lời dặn từ lâu, chỉ là ở dạng một dòng dài); tóm tắt mức
 * thạo là chữ về bé, nhưng là chữ máy con tự dựng, không số, và không lưu ở đâu cả.
 *
 * Câu hỏi của bé KHÔNG vào `kho` — nó đã nằm trong lời dặn (`chiTiet.beNoi`, có
 * `DAU_RIENG` lọc khỏi vân tay). Đưa thêm một bản vào `kho` là nhân đôi vô cớ một
 * mẩu tiếng nói của trẻ con đi ra khỏi máy.
 */
export function dungKho({ von, mucThao = null, doThi = null } = {}) {
  const tu = [];
  const daCo = new Set();
  for (const nhom of [von?.loi, ...(von?.on || [])]) {
    for (const v of nhom?.tu || []) {
      const t = String(v?.tu ?? '').trim();
      if (!t || daCo.has(t.toLowerCase())) continue;
      daCo.add(t.toLowerCase());
      tu.push({ tu: t, nghia: String(v?.nghia ?? '').trim() });
      if (tu.length >= TU_KHO_TOI_DA) break;
    }
    if (tu.length >= TU_KHO_TOI_DA) break;
  }

  const cau = [];
  const daCau = new Set();
  for (const nhom of [von?.loi, ...(von?.on || [])]) {
    for (const c of nhom?.cau || []) {
      /* CÔNG THỨC, không phải câu ví dụ: công thức mới nói được "mẫu câu của bài",
         còn câu ví dụ đã điền sẵn một chữ vào ô trống rồi. */
      const x = String(c?.congThuc || c?.cau || '').trim();
      if (!x || daCau.has(x)) continue;
      daCau.add(x);
      cau.push(x);
      if (cau.length >= CAU_KHO_TOI_DA) break;
    }
    if (cau.length >= CAU_KHO_TOI_DA) break;
  }

  return { vonTu: tu, mauCau: cau, mucThaoTomTat: tomTatMucThao({ von, mucThao, doThi }) };
}

/**
 * CÔ CÓ XIN PHÁT CLIP KHÔNG — và chữ nào.
 *
 * Tool `nghe_lai` ở máy chủ KHÔNG phát gì (nó thuần, xem `tool_phongnoi.js`). Nó chỉ
 * công nhận chữ ấy thuộc bài. Việc phát là của màn hình, sau khi đọc danh sách bước.
 *
 * ⚠ CHỈ PHÁT MỘT CHỮ, chữ ĐẦU TIÊN. Mô hình gọi `nghe_lai` hai lần trong một lượt
 * là chuyện có thể, và hai clip nối nhau thì bé không kịp nghe chữ nào — mà clip
 * thứ hai lại đè lên tiếng cô đang nói.
 */
export function tuCanPhat(buocTool) {
  for (const b of buocTool || []) {
    if (b?.ten !== 'nghe_lai') continue;
    const t = String(b?.args?.tu ?? '').trim();
    /* Chữ ngoài bài thì tool đã bác, và kết quả nói thẳng là "NOT in this lesson".
       Đọc lại dấu ấy ở đây chứ không tin mình: máy con phát clip theo chữ này, mà
       clip của một chữ ngoài bài thì không có, và lúc ấy nút nghe im lặng vô cớ. */
    if (!t || /NOT in this lesson/i.test(String(b?.ra || ''))) continue;
    return t;
  }
  return null;
}
