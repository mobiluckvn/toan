import { vanTay, locKhung } from './vantay.js';
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

/** Bác chốt mô hình. Đổi thì đổi ở ĐÚNG đây, đừng rải ra nhiều chỗ. */
export const MO_HINH = 'openai/gpt-oss-120b';

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
export const LOI_KHUON_JSON = ['json_validate_failed', 'output_parse_failed'];

/** Đếm số lần phải nới khuôn. Không log (máy chủ không ghi gì) — chỉ đếm. */
export const LOI_NOI_KHUON = { so: 0, thanh: 0, ganNhat: null };

/** Lỗi này có phải "Groq bác vì KHUÔN" không — chứ không phải khoá sai hay mạng. */
export function laLoiKhuon(e) {
  if (e?.status !== 400) return false;
  const ma = e?.error?.error?.code || e?.error?.code || '';
  const loi = String(e?.message || '');
  return LOI_KHUON_JSON.some((x) => ma === x || loi.includes(x));
}

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
