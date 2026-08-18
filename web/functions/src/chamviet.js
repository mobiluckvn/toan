/**
 * CHẤM BÀI VIẾT NGẮN — phần máy chủ. Cùng khuôn với `luyennoi.js`: chuyển lời lên
 * Groq rồi đem câu trả lời về, KHÔNG lưu gì.
 *
 * ── BỐN ĐIỀU BÁC CHỐT 18-08, VÀ CHÚNG NẰM Ở ĐÂU ──
 *
 *   1. sửa lỗi và khen CỤ THỂ      → `loiDanCham()` bắt trả `khen` và `loi[]`,
 *                                     mỗi lỗi phải có câu sai · câu sửa · vì sao
 *   2. có điểm để vào sổ           → trường `diem` 0–10, và màn hình ghi rõ AI chấm
 *   3. chỉ gợi ý bằng vốn đã học   → bảng từ đi kèm lời dặn, và `lib/chamviet.js`
 *                                     SOI LẠI lời chấm để bắt chữ lạ
 *   4. bố mẹ đọc được              → trường `choBoMe`, tiếng Việt, cho người lớn
 *
 * ── VÌ SAO SOI LẠI, DÙ ĐÃ DẶN ──
 * Cả môn này đã trả giá hai lần cho niềm tin vào lời dặn: mô hình sinh
 * `"Bye, bike."` sau khi được dặn rõ ô ấy là tên người, và nói lặp y một câu ngay
 * sau khi được dặn "đừng lặp". Dặn dò là thứ mô hình CÓ THỂ theo. Nên chỗ nào chặn
 * được bằng luật thì chặn bằng luật — xem `soiLoiCham()` bên máy con.
 *
 * ── VÌ SAO ĐIỂM DO MÁY CHẤM MÀ VẪN VÀO SỔ ──
 * Vì bố mẹ hỏi "con viết được chưa" thì cần một câu trả lời. Nhưng con số ấy phải
 * đeo NHÃN: `nguon: 'ai'` đi kèm mọi chỗ ghi, và màn hình nói thẳng "máy chấm".
 * Con số không nhãn là con số sẽ bị đọc nhầm thành điểm của cô giáo.
 */

/** Cùng mô hình với phòng luyện nói. Đổi thì đổi ở `luyennoi.js` rồi sửa cả đây. */
export { MO_HINH, NGHI_NGAN, LoiGoi } from './luyennoi.js';
import { MO_HINH, NGHI_NGAN, LoiGoi } from './luyennoi.js';

/* Bé lớp 3 viết 2–3 câu. 600 ký tự đã rộng gấp mấy lần, mà vẫn chặn được một gói
   bất thường — khoá Groq là khoá của mình, ai gọi được là tiêu tiền của mình. */
export const TOI_DA_CHU_BAI_VIET = 600;
export const TOI_DA_TU_VON = 400;      // vốn từ cả quyển lớp 3 là 204
export const TOKEN_CHAM = 900;         // lời chấm dài hơn một lượt nói chuyện

/**
 * Soi gói máy con gửi lên. Trả về gói đã sạch, hoặc ném `LoiGoi`.
 *
 * Tách hẳn khỏi phần gọi mạng để chạy được bằng `node` mà không cần khoá API.
 */
export function soiBaiViet(du) {
  const viet = String(du?.viet ?? '').trim();
  if (!viet) throw new LoiGoi('bai-rong', 'Con chưa viết gì cả.');
  if (viet.length > TOI_DA_CHU_BAI_VIET) {
    throw new LoiGoi('bai-qua-dai', `Bài viết dài quá ${TOI_DA_CHU_BAI_VIET} ký tự.`);
  }
  const de = String(du?.de ?? '').trim();
  if (!de) throw new LoiGoi('thieu-de', 'Thiếu đề bài.');

  const von = Array.isArray(du?.vonTu) ? du.vonTu : [];
  if (!von.length) throw new LoiGoi('thieu-von', 'Thiếu bảng vốn từ đã học.');
  if (von.length > TOI_DA_TU_VON) {
    throw new LoiGoi('von-qua-nhieu', `Vốn từ nhiều quá ${TOI_DA_TU_VON} mục.`);
  }
  const sachVon = von.map((v) => ({
    tu: String(v?.tu ?? '').trim(),
    nghia: String(v?.nghia ?? '').trim(),
  })).filter((v) => v.tu);
  if (!sachVon.length) throw new LoiGoi('thieu-von', 'Bảng vốn từ rỗng.');

  const mau = (Array.isArray(du?.mauCau) ? du.mauCau : [])
    .map((x) => String(x ?? '').trim()).filter(Boolean).slice(0, 20);

  return { viet, de, vonTu: sachVon, mauCau: mau, lop: Number(du?.lop) || 3 };
}

/**
 * LỜI DẶN CHO MÁY CHẤM.
 *
 * Viết ở đây, KHÔNG ở máy con: lời dặn là thứ quyết định chất lượng lời chấm, và
 * để nó ở máy con thì mỗi bản dựng cũ còn nằm trong cache trình duyệt lại chấm
 * theo một luật khác. Máy chủ đổi một lần, mọi máy con đổi theo.
 */
export function loiDanCham({ de, viet, vonTu, mauCau, lop }) {
  const bang = vonTu.map((v) => `${v.tu}${v.nghia ? ` (${v.nghia})` : ''}`).join(' · ');
  return [
    `Bạn là cô giáo tiếng Anh tiểu học, đang chấm bài viết của một bé lớp ${lop} người Việt.`,
    '',
    `ĐỀ BÀI (tiếng Việt, bé đã đọc): ${de}`,
    '',
    'VỐN TỪ BÉ ĐÃ HỌC — đây là TOÀN BỘ tiếng Anh bé biết:',
    bang,
    '',
    ...(mauCau.length ? ['MẪU CÂU BÉ ĐÃ HỌC:', ...mauCau.map((x) => `- ${x}`), ''] : []),
    'LUẬT CHẤM — theo đủ, không bỏ điều nào:',
    '1. Khen CỤ THỂ: nói rõ bé làm được gì (câu nào đúng, dùng đúng từ nào).',
    '   Không khen chung chung kiểu "giỏi lắm".',
    '2. Mỗi lỗi phải chỉ ra: câu bé viết sai, câu sửa lại cho đúng, và vì sao —',
    '   giải thích bằng TIẾNG VIỆT thật ngắn, cho bé tám tuổi hiểu.',
    '3. Câu sửa và câu gợi ý CHỈ ĐƯỢC dùng từ trong bảng vốn từ ở trên.',
    '   Tuyệt đối không dạy từ mới, dù từ ấy hay hơn.',
    '4. Điểm từ 0 tới 10. Bé viết đủ số câu, đúng ngữ pháp, đúng đề thì 9–10.',
    '   Đừng khắt khe về chính tả hoa thường và dấu chấm câu — trừ nhiều nhất 1 điểm.',
    '5. Lời cho bố mẹ: một hai câu tiếng Việt, nói con làm được gì và nên tập gì.',
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:',
    '{"diem": 8, "khen": "…", "loi": [{"cau":"…","sua":"…","viSao":"…"}],',
    ' "goiY": "…", "choBoMe": "…"}',
    '- "khen", "viSao", "goiY", "choBoMe": TIẾNG VIỆT.',
    '- "cau", "sua": TIẾNG ANH.',
    '- Bài không có lỗi nào thì "loi": [].',
    '',
    'BÀI VIẾT CỦA BÉ:',
    viet,
  ].join('\n');
}

/**
 * Gọi Groq. `taoClient` tiêm vào để cổng thử được mà không cần mạng lẫn khoá.
 *
 * `temperature` thấp có chủ ý — đây là chấm bài, không phải chỗ sáng tác. Và
 * `reasoning_effort: 'low'` là bắt buộc: `gpt-oss-120b` tiêu token cho phần nghĩ
 * TRƯỚC khi viết, lời dặn dài (bảng vốn từ 200 mục) thì nó nghĩ lâu, và nghĩ hết
 * token là `content` rỗng — xem chú thích dài ở `luyennoi.js`.
 */
export async function chamBaiViet(du, taoClient) {
  const goi = soiBaiViet(du);
  const client = taoClient();
  const kq = await client.chat.completions.create({
    model: MO_HINH,
    messages: [{ role: 'system', content: loiDanCham(goi) }],
    temperature: 0.2,
    max_tokens: TOKEN_CHAM,
    reasoning_effort: NGHI_NGAN,
    response_format: { type: 'json_object' },
  });
  const chon = kq?.choices?.[0];
  const chu = chon?.message?.content || '';
  if (!chu.trim()) {
    throw new LoiGoi('tra-loi-rong',
      `Máy chấm không trả lời được (finish_reason: ${chon?.finish_reason || 'không rõ'}).`);
  }
  /* Trả CHỮ TRẦN. Việc bóc JSON và SOI lời chấm là của máy con
     (`lib/chamviet.js`, có cổng canh) — đúng một chỗ biết hình dạng câu trả lời. */
  return { chu, moHinh: MO_HINH };
}
