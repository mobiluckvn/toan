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

export async function hoiMay(du, taoClient) {
  const messages = soiGoi(du);
  const client = taoClient();
  const kq = await client.chat.completions.create({
    model: MO_HINH,
    messages,
    temperature: 0.4,
    max_tokens: TOKEN_TRA_LOI,
    reasoning_effort: NGHI_NGAN,
    response_format: { type: 'json_object' },
  });
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
     để đúng một chỗ biết hình dạng câu trả lời. */
  return { chu, moHinh: MO_HINH };
}
