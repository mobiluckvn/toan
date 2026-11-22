/**
 * MỘT CHỖ DUY NHẤT BIẾT NHÀ CUNG CẤP MÔ HÌNH.
 *
 * Trước 22-11-2026 mỗi callable tự `new Groq(...)`, và mỗi module tự nhắc tên mô
 * hình — đổi nhà cung cấp là phải đi sửa năm chỗ, sót một chỗ là một tính năng
 * âm thầm chạy mô hình cũ. Nay mọi lời gọi đi qua `taoClientLLM`, và mọi module
 * lấy `MO_HINH` từ đây.
 *
 * ── VÌ SAO GỌI BẰNG `fetch` CHỨ KHÔNG THÊM SDK ──
 * Gemini có cổng tương thích OpenAI (`/v1beta/openai/chat/completions`): cùng
 * hình dạng gói `messages` / `tools` / `response_format` / `reasoning_effort` mà
 * code đang dùng với Groq. Nên chỉ cần một vỏ mỏng có đúng một hàm
 * `chat.completions.create` — các module và mọi phép thử (vốn tiêm client giả)
 * không phải đổi một dòng nào. Node 22 có sẵn `fetch`, không thêm phụ thuộc.
 *
 * ── BA CHỖ GEMINI KHÁC GROQ, ĐÃ XỬ Ở VỎ NÀY ──
 *   1. `temperature`: Google dặn với Gemini 3.x là ĐỂ MẶC ĐỊNH (1.0); hạ thấp làm
 *      mô hình dễ lặp hoặc tụt chất lượng. Vỏ BỎ trường này trước khi gửi. Các
 *      module vẫn khai nhiệt độ (phép thử canh nó), nhưng nó chỉ còn ý nghĩa với
 *      nhà cung cấp cũ.
 *   2. Token phần nghĩ tính chung vào trần `max_tokens`. Các trần 200–900 đặt cho
 *      `gpt-oss` là quá chặt — đúng cái lỗi "nghĩ hết token, `content` rỗng" đã
 *      ghi ở `luyennoi.js`. Vỏ nâng mọi trần lên ít nhất `TOKEN_SAN`. Chỉ tốn
 *      theo số token thật dùng, nên trần cao không làm đắt thêm.
 *   3. Không đặt `reasoning_effort` thì Gemini nghĩ mức `medium` — chậm. Vỏ mặc
 *      định `low` cho lời gọi nào quên khai.
 *   4. Gói CHỈ có lượt `system` (chấm viết, phụ đạo, phân xử gửi thế) thì Gemini
 *      bác vì không có nội dung nào để đáp. Vỏ thêm một lượt `user` ngắn ở cuối.
 */

/** Đổi được bằng biến môi trường `LLM_MODEL` khi cần so A/B, không phải sửa mã. */
export const MO_HINH = process.env.LLM_MODEL || 'gemini-3.8-flash';

export const CONG_LLM = 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions';

/** Trần token tối thiểu cho MỌI lời gọi — xem mục 2 ở trên. */
export const TOKEN_SAN = 2048;

/** Một lời gọi chờ tối đa chừng này. Quá thì bỏ, để bé không ngồi nhìn cả phút. */
export const CHO_TOI_DA_MS = 25000;

/** Lỗi tạm (quá tải, hết hạn mức phút) thì thử lại ĐÚNG MỘT LẦN. */
const LOI_TAM = new Set([429, 500, 502, 503, 504]);
const NGHI_TRUOC_THU_LAI_MS = 700;

/** Lỗi trả về giữ đúng hình dạng của SDK cũ (`e.status`, `e.error.error.code`),
    để `laLoiKhuon` và các nhánh bắt 401/403 ở `index.js` khỏi phải đổi. */
class LoiNhaCungCap extends Error {
  constructor(status, than) {
    const goc = Array.isArray(than) ? than[0]?.error : than?.error;
    super(goc?.message || `Nhà cung cấp mô hình trả ${status}`);
    this.status = status;
    this.error = { error: { code: goc?.status || goc?.code || '', message: goc?.message || '' } };
  }
}

const LUOT_GIUC = { role: 'user', content: 'Follow the instructions above and reply now.' };

export function soanGoi(p) {
  const { temperature, ...con } = p;
  const ds = p.messages || [];
  return {
    ...con,
    messages: ds.some((m) => m.role !== 'system') ? ds : [...ds, LUOT_GIUC],
    max_tokens: Math.max(Number(p.max_tokens) || 0, TOKEN_SAN),
    reasoning_effort: p.reasoning_effort || 'low',
  };
}

async function guiMotLan(khoa, than, choMs) {
  const ngat = new AbortController();
  const hen = setTimeout(() => ngat.abort(), choMs);
  try {
    const r = await fetch(CONG_LLM, {
      method: 'POST',
      headers: { 'content-type': 'application/json', authorization: `Bearer ${khoa}` },
      body: JSON.stringify(than),
      signal: ngat.signal,
    });
    const chu = await r.text();
    let json = null;
    try { json = JSON.parse(chu); } catch { json = null; }
    if (!r.ok) throw new LoiNhaCungCap(r.status, json);
    return json;
  } catch (e) {
    if (e?.name === 'AbortError') {
      const het = new Error('Mô hình trả lời quá lâu.');
      het.status = 504;
      throw het;
    }
    throw e;
  } finally {
    clearTimeout(hen);
  }
}

/**
 * Client có đúng hình dạng mà các module đã quen: `client.chat.completions.create`.
 */
export function taoClientLLM(khoa, { choMs = CHO_TOI_DA_MS } = {}) {
  return {
    chat: {
      completions: {
        async create(p) {
          const than = soanGoi(p);
          try {
            return await guiMotLan(khoa, than, choMs);
          } catch (e) {
            if (!LOI_TAM.has(e?.status)) throw e;
            await new Promise((x) => setTimeout(x, NGHI_TRUOC_THU_LAI_MS));
            return guiMotLan(khoa, than, choMs);
          }
        },
      },
    },
  };
}

/**
 * Lỗi này có phải "bị bác vì KHUÔN JSON" không — chứ không phải khoá sai hay mạng.
 *
 * Groq có mã riêng (`json_validate_failed`, `output_parse_failed`). Gemini không
 * soi JSON trên máy chủ như thế; nó bác gói 400 `INVALID_ARGUMENT` khi không chịu
 * `response_format` (vd. đi chung `tools`). Cả hai đều đáng một lần nới khuôn.
 */
export const LOI_KHUON_JSON = ['json_validate_failed', 'output_parse_failed'];
export function laLoiKhuon(e) {
  if (e?.status !== 400) return false;
  const ma = e?.error?.error?.code || e?.error?.code || '';
  const loi = String(e?.message || '');
  if (LOI_KHUON_JSON.some((x) => ma === x || loi.includes(x))) return true;
  return /response_format|response_mime_type|json/i.test(loi);
}

/**
 * Gọi đòi JSON, bị bác vì khuôn thì nới ĐÚNG MỘT LẦN (bỏ `response_format`).
 * Dùng cho chấm viết, phụ đạo, phân xử — trước đây ba chỗ ấy không có đường nới,
 * nên một lần bác là mất trắng (phân xử còn mất trong im lặng).
 */
export async function goiDoiJson(client, p) {
  try {
    return await client.chat.completions.create({ ...p, response_format: { type: 'json_object' } });
  } catch (e) {
    if (!laLoiKhuon(e)) throw e;
    const { response_format, ...long } = p;
    return client.chat.completions.create(long);
  }
}
