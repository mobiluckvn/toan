import { vanTay, locKhung } from './vantay.js';
import {
  TOOLS_GUI, TEN_TRA_LOI, BUOC_TOI_DA, chayTool, chuKyTool, soiKho, LOI_TOOL,
} from './tool_phongnoi.js';
/**
 * PHÒNG LUYỆN NÓI — phần máy chủ. Chỉ có ĐÚNG một việc: chuyển lời lên Groq rồi
 * đem câu trả lời về.
 *
 * ── VÌ SAO MÁY CHỦ KHÔNG LƯU GÌ ──
 * Bác chốt 13-08: "Server thuần tuý chỉ là gọi lên Groq và lấy câu trả lời về,
 * không lưu gì hết. Việc quản lý context là phía client làm và save lên Firebase."
 *
 * Nên tệp này KHÔNG import `firebase-admin/firestore`, không ghi log nội dung, và
 * không giữ lại gì giữa hai lượt gọi. Có một lý do thực tế đằng sau: đây là tiếng
 * nói của trẻ con và câu chuyện riêng của từng bé. Chỗ nào không lưu thì chỗ ấy
 * không bao giờ rò.
 *
 * ── VÌ SAO VẪN PHẢI CÓ CHỐT, DÙ "THUẦN TUÝ" ──
 * Khoá Groq là khoá của mình, nên bất kỳ ai gọi được hàm này là tiêu tiền của mình.
 * Ba chốt, và cả ba đều KHÔNG cần lưu gì:
 *
 *   1. phải đăng nhập  — `request.auth`;
 *   2. chặn số lượt và độ dài từng lượt — gói phình to là chặn ngay tại cửa;
 *   3. chặn tổng số chữ — mười lượt ngắn vẫn có thể là một gói khổng lồ.
 *
 * Cái KHÔNG làm được nếu không lưu gì: đếm số lượt gọi mỗi bé mỗi ngày. Muốn có
 * thì phải giữ một bộ đếm ở đâu đó — để bác quyết, đừng lặng lẽ thêm vào.
 */

/** Mô hình chốt ở `llm.js` (22-11-2026: chuyển sang Gemini). Đổi thì đổi ở ĐÚNG đó. */
import { MO_HINH, LOI_KHUON_JSON, laLoiKhuon } from './llm.js';
export { MO_HINH, LOI_KHUON_JSON, laLoiKhuon };

/* Ba chốt cửa. Rộng rãi so với một buổi nói chuyện thật của bé, nhưng đủ chặn
   một gói bất thường. */
export const TOI_DA_LUOT = 24;
/**
 * Hai mức trần khác nhau, và khác nhau là CÓ LÝ.
 *
 * Lượt của BÉ do bé nói ra — bé 6 tuổi không nói nổi 2000 ký tự, nên dài hơn thế
 * là bất thường và đáng chặn. LỜI DẶN thì do chính app sinh: nó liệt kê vốn từ,
 * mẫu câu, lời lớp học và việc của lượt này, nên dài là chuyện thường.
 *
 * Gộp hai thứ vào một mức trần đã hỏng thật: thêm phần "việc của lượt này" vào lời
 * dặn là nó dài 2077 ký tự, vượt trần 2000, và bị CHÍNH CHỐT CỦA MÌNH chặn ngay
 * tại cửa — 2ms, chưa kịp ra tới Groq. Trên màn hình bé chỉ thấy "cô chưa trả lời
 * được", không ai đoán được vì sao.
 */
export const TOI_DA_CHU_MOT_LUOT = 2000;
export const TOI_DA_CHU_LOI_DAN = 8000;
export const TOI_DA_CHU_CA_GOI = 20000;

export class LoiGoi extends Error {
  constructor(ma, loi) { super(loi); this.ma = ma; }
}

/**
 * Soi gói client gửi lên. Trả về mảng `messages` đã sạch, hoặc ném `LoiGoi`.
 *
 * Tách hẳn khỏi phần gọi mạng để chạy được bằng `node` mà không cần khoá API —
 * chỗ dễ sai ở đây là mấy con số chốt cửa, mà chúng thì không cần mạng để thử.
 */
export function soiGoi(du) {
  const ds = du?.messages;
  if (!Array.isArray(ds) || ds.length === 0) {
    throw new LoiGoi('thieu-loi', 'Không có lời nào để gửi.');
  }
  if (ds.length > TOI_DA_LUOT) {
    throw new LoiGoi('qua-nhieu-luot', `Nhiều nhất ${TOI_DA_LUOT} lượt một lần gọi.`);
  }

  let tong = 0;
  const sach = ds.map((m, i) => {
    const role = m?.role;
    if (!['system', 'user', 'assistant'].includes(role)) {
      throw new LoiGoi('vai-la', `Lượt ${i + 1} khai vai không hợp lệ.`);
    }
    const content = String(m?.content ?? '');
    if (!content.trim()) throw new LoiGoi('loi-rong', `Lượt ${i + 1} rỗng.`);
    const tran = role === 'system' ? TOI_DA_CHU_LOI_DAN : TOI_DA_CHU_MOT_LUOT;
    if (content.length > tran) {
      throw new LoiGoi('luot-qua-dai', `Lượt ${i + 1} dài quá ${tran} ký tự.`);
    }
    tong += content.length;
    return { role, content };
  });

  if (tong > TOI_DA_CHU_CA_GOI) {
    throw new LoiGoi('goi-qua-dai', `Cả gói dài quá ${TOI_DA_CHU_CA_GOI} ký tự.`);
  }
  /* Lời dặn phải là lượt ĐẦU. Để nó nằm giữa thì mấy lượt trước đó không chịu luật
     nào cả — đúng chỗ vốn từ có thể rò ra mà không ai thấy. */
  if (sach.some((m, i) => m.role === 'system' && i !== 0)) {
    throw new LoiGoi('loi-dan-sai-cho', 'Lời dặn phải đứng đầu gói.');
  }
  return sach;
}

/**
 * Gọi Groq. `taoClient` tiêm vào để cổng thử được mà không cần mạng lẫn khoá.
 *
 * `temperature` thấp có chủ ý: đây là lớp học, không phải chỗ sáng tác. Máy càng
 * bay bổng thì càng dễ chèn từ ngoài vốn của bé.
 */
/**
 * ⚠ `gpt-oss-120b` LÀ MÔ HÌNH CÓ SUY NGHĨ — hai nút vặn dưới đây là bắt buộc.
 *
 * Đã hỏng thật trên bản production 13-08, và hỏng theo kiểu khó lần nhất: sáng đi
 * thử trên bộ giả lập thì chạy, chiều bác bấm trên bản thật thì lỗi. Khác nhau ở
 * chỗ lời dặn — bản thử là câu gõ tay ngắn, bản thật là `loiDan()` đầy đủ.
 *
 * Mô hình tiêu token cho phần `reasoning` TRƯỚC khi viết `content`. Lời dặn dài
 * hơn thì nó nghĩ lâu hơn, và với `max_tokens: 300` nó tiêu hết sạch vào phần
 * nghĩ: `finish_reason: "length"`, `content` RỖNG. Kèm `response_format` nghiêm
 * ngặt thì Groq đem chuỗi rỗng ấy đi soi JSON và trả 400 `json_validate_failed`.
 *
 *   reasoning_effort: 'low'  thắt phần nghĩ lại
 *   max_tokens: 800          và vẫn chừa dư, phòng khi nó nghĩ dài
 *
 * Hai lớp cho cùng một chỗ hỏng là cố ý: chỉ nới token thì lời dặn dài thêm một
 * đoạn nữa là hỏng lại, mà lần sau chẳng ai nhớ vì sao.
 */
export const NGHI_NGAN = 'low';
export const TOKEN_TRA_LOI = 800;

/**
 * ══ HAI NÚT VẶN TRÊN CHƯA ĐỦ — ĐO THẬT 09-10-2026 ══
 *
 * Khối chú thích trên nói đúng chỗ hỏng nhưng chưa nói hết đường hỏng. Chạy thật
 * 54 lượt qua Groq: buổi dài tới lượt 6 trở đi vẫn 400, và quyển ta5/B11 chết LIỀN
 * NĂM LƯỢT (l6→l10) — bé chỉ thấy "Cô giáo máy chưa trả lời được". Đã kiểm riêng
 * để chắc không phải do vòng gọi lại của V1: 10/10 lần hỏng nằm ở lời gọi THỨ NHẤT
 * của lượt, tức gói y như bản trước V1.
 *
 * Hai hình dạng, và chúng khác nhau:
 *   `failed_generation: ""`            — đúng ca khối trên nói: tiêu hết token vào
 *                                        phần nghĩ. Nới token chỉ đẩy nó xa ra.
 *   `failed_generation: "Yes, I did…"`  — mô hình trả CHỮ TRẦN, hoặc kèm lời dẫn
 *                                        quanh khối JSON.
 *
 * Hình dạng thứ hai mới là chỗ đau, vì máy con ĐÃ CÓ SẴN đường đỡ nó: `docTraLoi`
 * ở `lib/phongnoi.js` viết rõ "mô hình được dặn trả JSON, nhưng KHÔNG được tin là
 * nó luôn làm đúng — trả về chữ trần thì vẫn phải dùng được, đừng để màn trắng", và
 * nó bóc được khối `{…}` nằm giữa lời dẫn. Nhưng `response_format` nghiêm ngặt làm
 * Groq bác NGAY TRÊN MÁY CHỦ NÓ, nên chữ ấy không bao giờ về tới. Đường đỡ có thật,
 * có chú thích tử tế, và chết câm. Chốt `tra-loi-rong` dưới đây cũng thế.
 *
 * ── VÌ SAO KHÔNG BỎ HẲN `response_format` ──
 * Thử 3 lần không có nó: cả 3 đều về được chữ dùng được, NHƯNG 2/3 câu rồi bị
 * `soiCau` bác (mô hình gộp cả câu hỏi lẫn câu đáp vào `en`). Bỏ hẳn là đổi một
 * lỗi 400 cứng thành một lần bị soi bác ở MỌI lượt — đắt hơn hẳn.
 *
 * Nên giữ đường nghiêm ngặt làm đường chính, và chỉ NỚI KHUÔN ĐÚNG MỘT LẦN khi
 * Groq bác vì khuôn. Lượt thường không đổi một li; lượt đáng lẽ chết thì nay có
 * cơ hội thứ hai, và `docTraLoi` cuối cùng được làm việc nó sinh ra để làm.
 */

/** Đếm số lần phải nới khuôn. Không log (máy chủ không ghi gì) — chỉ đếm. */
export const LOI_NOI_KHUON = { so: 0, thanh: 0, ganNhat: null };

const goiGroq = (client, messages, nghiemNgat) => client.chat.completions.create({
  model: MO_HINH,
  messages,
  temperature: 0.4,
  max_tokens: TOKEN_TRA_LOI,
  reasoning_effort: NGHI_NGAN,
  /* Nới khuôn = BỎ `response_format`, không phải đổi sang khuôn lỏng hơn: Groq chỉ
     có một kiểu, và chính nó là chỗ bác. */
  ...(nghiemNgat ? { response_format: { type: 'json_object' } } : {}),
});

export async function hoiMay(du, taoClient) {
  const messages = soiGoi(du);
  const client = taoClient();
  let noiKhuon = false;
  let kq;
  try {
    kq = await goiGroq(client, messages, true);
  } catch (e) {
    if (!laLoiKhuon(e)) throw e;
    /* ⚠ ĐÚNG MỘT LẦN. Nới khuôn rồi vẫn hỏng thì đó không còn là chuyện khuôn, và
       thử mãi chỉ làm bé ngồi đợi lâu hơn trước khi thấy cùng một dòng lỗi. */
    noiKhuon = true;
    LOI_NOI_KHUON.so += 1;
    LOI_NOI_KHUON.ganNhat = e?.error?.error?.code || e?.error?.code || 'khong-ro';
    kq = await goiGroq(client, messages, false);
    LOI_NOI_KHUON.thanh += 1;
  }
  const chon = kq?.choices?.[0];
  const chu = chon?.message?.content || '';

  /* Rỗng thì NÓI RA, đừng trả về chuỗi rỗng. Máy con nhận chuỗi rỗng sẽ vẽ một
     bong bóng trắng và bé ngồi nhìn — không ai biết hỏng ở đâu. Đây đúng là hình
     dạng của lỗi vừa gặp, nên phải có chốt riêng. */
  if (!chu.trim()) {
    throw new LoiGoi('tra-loi-rong',
      `Cô giáo máy không trả lời được (finish_reason: ${chon?.finish_reason || 'không rõ'}).`);
  }
  /* Trả về CHỮ TRẦN. Việc bóc JSON là của client (`lib/phongnoi.js` có cổng canh),
     để đúng một chỗ biết hình dạng câu trả lời.

     ── VÂN TAY LỜI DẶN, và vì sao ở đây nó YẾU HƠN bên chấm viết ──
     Bên `chamviet` máy chủ SỞ HỮU hàm dựng lời dặn, nên lấy được khung chính xác
     bằng cách gọi lại hàm ấy với dữ liệu rỗng. Ở đây thì không: lời dặn do MÁY
     CON dựng (`lib/phongnoi.js` → `loiDan()`) và gửi lên đã thành chữ. Máy chủ
     chỉ còn cách LỌC THEO DẤU HIỆU — mà lọc theo dấu hiệu thì sót được: thêm một
     dòng mới mang tên bé vào `loiDan()` mà quên khai vào `DAU_RIENG` là dòng ấy
     lọt vào vân tay, và không có gì báo.

     Chấp nhận, vì cái giá của chỗ sót này thấp: vân tay lọt một mẩu riêng thì
     bảng so ΔC nhiễu thêm vài nhóm, chứ không lộ gì ra ngoài (băm một chiều) và
     không đụng tới bé. Còn `phienBanMau` — thứ bảng so ĐANG THẬT SỰ gom theo —
     thì do người sửa khai tay nên không sót được. Muốn chắc hơn thì đổi
     `loiDan()` trả về kèm khung, và đó là việc của máy con. */
  const loiDan = messages.find((m) => m.role === 'system')?.content || '';
  return {
    chu,
    moHinh: MO_HINH,
    /* Lượt phải nới khuôn đi ra kèm dấu, để máy con còn đếm được trên bản thật. */
    noiKhuon,
    ...vanTay('luyennoi', locKhung(loiDan), {
      moHinh: MO_HINH, nhiet: 0.4, token: TOKEN_TRA_LOI,
      /* ⚠ CHỈ THÊM KHOÁ NÀY Ở LƯỢT NỚI KHUÔN. Thêm ở mọi lượt là mọi vân tay cũ
         đổi hết, và bảng so ΔG mất sạch phần đã gom được. Còn gom lượt nới khuôn
         lẫn với lượt thường thì cũng sai: bỏ `response_format` là đổi cách sinh,
         mà "thứ gì đổi thì kết quả đổi, nên phải tính" — đúng lời `vantay.js`. */
      ...(noiKhuon ? { khuon: 'long' } : {}),
    }),
  };
}

/* ═════════════ NHÁNH ReAct CHO LƯỢT BÉ HỎI LẠI (việc V11) ═════════════ */

/**
 * HỎI MÁY, CHO PHÉP NÓ TRA TRƯỚC KHI TRẢ LỜI.
 *
 * Chỉ máy con mới rẽ vào đây, và chỉ khi nhãn lượt là `hoiLai` và bé từ lớp 3 —
 * luật rẽ nằm ở `lib/hoico.js`, có cổng canh. Lớp 1–2 đi nhánh cũ: ở tuổi ấy câu
 * hỏi của bé gần như luôn là một chữ trong bài, mà một chữ thì lời dặn đủ sức.
 *
 * ── BA CHỐT, VÀ CẢ BA ĐỀU LÀ CHỐT CHỐNG VÒNG LẶP ──
 * Vòng ReAct hỏng theo đúng một kiểu: mô hình gọi tool, đọc kết quả, rồi gọi lại
 * chính tool ấy. Nó không "treo" — nó cứ chạy, tốn lượt gọi, và bé ngồi nhìn.
 *
 *   1. TRẦN BƯỚC `BUOC_TOI_DA` — cứng, không bàn.
 *   2. BẮT LẶP: cùng tool + cùng tham số lần thứ hai là dừng NGAY, không đợi hết
 *      trần. Lặp một lần đã là bằng chứng nó không dùng được kết quả vừa nhận.
 *   3. LƯỢT CHỐT KHÔNG CÓ TOOL: dừng vì bất cứ lý do gì thì lượt cuối gọi lại với
 *      `tools` BỎ HẲN. Còn để `tools` trong gói là mời nó gọi tiếp, và lúc ấy ta
 *      phải bỏ câu trả lời — tức tốn một lượt mà không được gì.
 *
 * ── VÌ SAO LƯỢT CHỐT MỚI ĐÒI JSON ──
 * `response_format: json_object` và `tools` chung một gói là chỗ Groq hay bác, và
 * ta đã dính một lần đúng kiểu ấy (xem `LOI_KHUON_JSON`). Nên mấy lượt tra để
 * TRỐNG khuôn, và chỉ lượt chốt mới ép JSON — lượt chốt là lượt duy nhất mà máy
 * con phải bóc ra `{en, vi}`.
 *
 * Nếu mô hình tự ý trả lời ngay mà KHÔNG gọi tool nào, và câu ấy đã có dạng JSON,
 * thì nhận luôn — đừng gọi thêm một lượt chốt cho vui.
 *
 * ── TRẢ VỀ ──
 * Chữ TRẦN như `hoiMay`, cộng `buocTool` — danh sách bước đã chạy. Máy con cần nó
 * để biết có phải phát clip hay không (`nghe_lai`), và để đếm được trên bản thật.
 * ⚠ `buocTool` KHÔNG mang chữ nào của bé: tham số tool là chữ TIẾNG ANH của bài,
 * còn câu hỏi của bé nằm trong lời dặn và không đi ra theo đường này.
 */
export async function hoiMayCoTool(du, taoClient) {
  const goc = soiGoi(du);
  const nem = (ma, loi) => { throw new LoiGoi(ma, loi); };
  const kho = soiKho(du?.kho, nem);
  const client = taoClient();
  LOI_TOOL.goi += 1;

  const messages = [...goc];
  /* ── TÁCH HAI KÊNH, VÀ PHẢI NÓI THẲNG RA ──
     Đo thật với Groq: 10/10 lượt chết với 400 `tool_use_failed` —
     *attempted to call tool 'json' which was not in request.tools*. Mô hình KHÔNG
     gọi tool nào của ta; nó thấy lời dặn (`loiDan`) đòi "trả lời dạng JSON
     {en, vi}" và thấy gói có `tools`, nên nó đi trả lời QUA kênh tool, bằng một
     tool nó tự đặt tên là `json`. Groq bác, và bé mất lượt.

     Đây đúng họ với chỗ hỏng của V1–V2 (`loi-dan-tu-choi-nhau`): một dòng ở dưới
     không tự thắng được một luật ở trên, phải NÓI THẲNG là nó thắng. Nên lượt tra
     có một dòng riêng, nói rõ ba điều: chưa trả lời bé, ĐỪNG dùng JSON lượt này,
     và không cần tra thì nói đúng một chữ. Lượt chốt (bỏ `tools`) mới đòi JSON. */
  messages.push({
    role: 'user',
    content: 'TOOLS ARE AVAILABLE THIS TURN. You may first look things up with '
      + 'tra_tu / mau_cau_cua_unit / muc_thao / nghe_lai. When you are ready, give '
      + `your reply by calling ${TEN_TRA_LOI} with {en, vi} — that call IS your `
      + 'answer, so do not also write it as plain text.',
  });
  const buocTool = [];
  const daGoi = new Set();
  let lyDoDung = 'tu-tra-loi';
  let chu = '';

  for (let i = 0; i < BUOC_TOI_DA; i += 1) {
    const kq = await client.chat.completions.create({
      model: MO_HINH,
      messages,
      temperature: 0.4,
      max_tokens: TOKEN_TRA_LOI,
      reasoning_effort: NGHI_NGAN,
      tools: TOOLS_GUI,
      tool_choice: 'auto',
    });
    const tin = kq?.choices?.[0]?.message;
    const goiTool = tin?.tool_calls || [];

    /* ── CÂU TRẢ LỜI ĐI QUA KÊNH TOOL ──
       Xem `TOOL_TRA_LOI`. Dựng lại đúng khối JSON mà máy con vẫn bóc (`docTraLoi`),
       nên không tầng nào phía dưới phải biết là nó đã đi đường khác. */
    const traLoi = goiTool.find((g) => g?.function?.name === TEN_TRA_LOI);
    if (traLoi) {
      let a = {};
      try { a = JSON.parse(traLoi.function?.arguments || '{}'); } catch { a = {}; }
      if (a?.en || a?.vi) {
        return ketQua(JSON.stringify({ en: String(a.en ?? ''), vi: String(a.vi ?? '') }),
          goc, { buocTool, lyDoDung: buocTool.length ? 'tra-roi-tra-loi' : 'tra-loi-ngay' });
      }
      /* Gọi `tra_loi_be` mà rỗng ruột: đừng trả một bong bóng trắng cho bé — xuống
         lượt chốt, nơi khuôn JSON bị ép và lỗi rỗng có chốt riêng. */
      lyDoDung = 'tra-loi-rong-o-tool';
      break;
    }

    if (!goiTool.length) {
      /* Không gọi tool nữa. `READY` là đường mong đợi; nhưng nó cũng có thể trả
         thẳng một khối JSON dù vừa bị dặn đừng — nhận luôn thì đỡ một lượt gọi.
         ⚠ KHÔNG nhận một câu trần làm câu trả lời: máy con `docTraLoi` cần
         `{en, vi}`, mà một câu trần thì không có lời tiếng Việt lẫn câu tiếng Anh
         tách ra được — nó sẽ thành một bong bóng nửa vời cho bé. */
      chu = tin?.content || '';
      if (/\{[\s\S]*\}/.test(chu)) {
        return ketQua(chu, goc, { buocTool, lyDoDung: i === 0 ? 'tra-loi-ngay' : 'tu-tra-loi' });
      }
      lyDoDung = /^\s*READY\b/i.test(chu) ? 'khong-can-tra' : 'tra-loi-khong-phai-json';
      break;
    }

    /* ⚠ GIỮ NGUYÊN lượt `assistant` kèm `tool_calls` TRƯỚC khi đẩy kết quả vào.
       Bỏ nó thì gói gửi lên có `role: 'tool'` mà không có lời gọi nào đi trước, và
       Groq bác cả gói — hỏng ở lượt thứ hai, tức chỉ hỏng khi mô hình THẬT SỰ gọi
       tool, tức không lộ ra ở phép thử nào chỉ có một bước. */
    messages.push({ role: 'assistant', content: tin.content || '', tool_calls: goiTool });

    let coLap = false;
    for (const g of goiTool) {
      const ten = g?.function?.name || '';
      /* Kênh trả lời đã xử ở trên; đừng cho nó đi qua `chayTool`. */
      if (ten === TEN_TRA_LOI) continue;
      let args = {};
      try { args = JSON.parse(g?.function?.arguments || '{}'); } catch { args = {}; }
      const ky = chuKyTool(ten, args);
      const ra = chayTool(ten, args, kho);
      buocTool.push({ ten, args, ra });
      messages.push({ role: 'tool', tool_call_id: g?.id || `t${buocTool.length}`, content: ra });
      if (daGoi.has(ky)) coLap = true;
      daGoi.add(ky);
    }

    if (coLap) {
      LOI_TOOL.lap += 1;
      LOI_TOOL.ganNhat = buocTool[buocTool.length - 1]?.ten || null;
      lyDoDung = 'lap';
      break;
    }
    if (i === BUOC_TOI_DA - 1) {
      LOI_TOOL.hetBuoc += 1;
      lyDoDung = 'het-buoc';
    }
  }

  /* ── LƯỢT CHỐT: KHÔNG TOOL, ÉP JSON ── */
  messages.push({
    role: 'user',
    content: 'Now answer the child. Do not call any more tools. Use what you looked up. '
      + 'Reply as JSON {"en": …, "vi": …} with ONE English sentence using only the allowed words.',
  });
  let kq;
  try {
    kq = await goiGroq(client, messages, true);
  } catch (e) {
    if (!laLoiKhuon(e)) throw e;
    LOI_NOI_KHUON.so += 1;
    LOI_NOI_KHUON.ganNhat = e?.error?.error?.code || e?.error?.code || 'khong-ro';
    kq = await goiGroq(client, messages, false);
    LOI_NOI_KHUON.thanh += 1;
  }
  const chon = kq?.choices?.[0];
  chu = chon?.message?.content || '';
  if (!chu.trim()) {
    throw new LoiGoi('tra-loi-rong',
      `Cô giáo máy không trả lời được (finish_reason: ${chon?.finish_reason || 'không rõ'}).`);
  }
  return ketQua(chu, goc, { buocTool, lyDoDung });
}

/**
 * Gói kết quả nhánh ReAct — dựng ở MỘT chỗ vì `hoiMayCoTool` có hai đường ra.
 *
 * ⚠ Vân tay tính từ LỜI DẶN GỐC, không từ `messages` đã mọc thêm mấy lượt tool.
 * Vân tay là để so MẪU lời dặn; gom cả kết quả tool vào thì mỗi lượt một vân tay
 * (kết quả tool khác nhau theo chữ bé hỏi) — vừa vô dụng cho phép so, vừa thành
 * một mã theo dõi được từng lượt. Đúng lý lẽ ở đầu `vantay.js`.
 *
 * Và `nhanhTool: true` vào vân tay: cùng một lời dặn mà đi nhánh ReAct thì cách
 * sinh khác hẳn, nên "thứ gì đổi thì kết quả đổi, nên phải tính".
 */
function ketQua(chu, goc, { buocTool, lyDoDung }) {
  const loiDan = goc.find((m) => m.role === 'system')?.content || '';
  return {
    chu,
    moHinh: MO_HINH,
    noiKhuon: false,
    buocTool,
    lyDoDung,
    ...vanTay('luyennoi', locKhung(loiDan), {
      moHinh: MO_HINH, nhiet: 0.4, token: TOKEN_TRA_LOI, nhanhTool: true,
    }),
  };
}
