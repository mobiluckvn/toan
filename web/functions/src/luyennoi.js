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
export const TOI_DA_CHU_MOT_LUOT = 2000;
export const TOI_DA_CHU_CA_GOI = 12000;

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
    if (content.length > TOI_DA_CHU_MOT_LUOT) {
      throw new LoiGoi('luot-qua-dai', `Lượt ${i + 1} dài quá ${TOI_DA_CHU_MOT_LUOT} ký tự.`);
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
export async function hoiMay(du, taoClient) {
  const messages = soiGoi(du);
  const client = taoClient();
  const kq = await client.chat.completions.create({
    model: MO_HINH,
    messages,
    temperature: 0.4,
    max_tokens: 300,
    response_format: { type: 'json_object' },
  });
  const chu = kq?.choices?.[0]?.message?.content || '';
  /* Trả về CHỮ TRẦN. Việc bóc JSON là của client (`lib/phongnoi.js` có cổng canh),
     để đúng một chỗ biết hình dạng câu trả lời. */
  return { chu, moHinh: MO_HINH };
}
