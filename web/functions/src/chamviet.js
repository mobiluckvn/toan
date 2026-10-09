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
import { vanTay } from './vantay.js';
import { chuLaTrongCham } from './chula.js';

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
/* Phần ĐẦU dùng chung cho hai mắt xích đầu: vai, đề, bảng vốn, mẫu câu. Dựng một
   chỗ để hai mắt xích không bao giờ nói khác nhau về vốn từ của bé. */
function dauChung({ de, vonTu, mauCau, lop }) {
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
  ];
}

/**
 * ══ VÌ SAO TÁCH MỘT LỜI DẶN THÀNH BA (mẫu Prompt Chaining, việc V4) ══
 *
 * Bản cũ bắt mô hình làm BỐN việc trong một lượt: tìm lỗi, sửa lỗi, khen, và viết
 * lời cho bố mẹ. Bốn việc một lượt thì nó làm việc dễ nhất cho tròn và làm việc khó
 * nhất cho xong — mà việc khó nhất đúng là việc quan trọng nhất: sửa đúng chỗ sai
 * BẰNG VỐN TỪ CỦA BÉ.
 *
 * Tách ra thì mỗi lượt một việc, và quan trọng hơn: CHEN ĐƯỢC MỘT PHÉP SOI VÀO
 * GIỮA. Sau mắt xích 2 ta soi chữ lạ ngay trên máy chủ (`chula.js`), có chữ lạ thì
 * gọi lại mắt xích 2 kèm danh sách chữ cấm. Trước V4 phép soi chỉ có ở máy con,
 * tức tới lúc biết thì đã hết lượt gọi và `soiLoiCham` chỉ còn cách BỎ mục ấy đi.
 */

/**
 * MẮT XÍCH 1 — CHỈ LIỆT KÊ LỖI, CẤM SỬA.
 *
 * ⚠ Chữ "KHÔNG SỬA" là chốt của cả mắt xích này. Cho nó sửa luôn thì nó sửa bằng
 * từ hay nhất nó biết, và từ hay nhất thường là từ bé chưa học — đúng chỗ hỏng mà
 * cả việc V4 sinh ra để chữa. Ở đây nó chỉ được CHỈ RA, nên không có cửa nào để
 * một chữ mới chui vào.
 */
export function loiDanTimLoi({ de, viet, vonTu, mauCau, lop }) {
  return [
    ...dauChung({ de, vonTu, mauCau, lop }),
    'VIỆC CỦA BẠN LÚC NÀY: CHỈ LIỆT KÊ LỖI. KHÔNG SỬA, KHÔNG KHEN, KHÔNG GỢI Ý.',
    'Mỗi lỗi một mục, và chỉ gồm ba thứ:',
    '- "cau": câu bé viết, NGUYÊN VĂN, không chữa một chữ nào;',
    '- "loai": một trong chinhTa | thieuTu | thuTu | mauCau | khac;',
    '- "ghiChu": nhiều nhất 15 chữ tiếng Việt, nói lỗi NẰM Ở ĐÂU (không nói cách sửa).',
    'Đừng khắt khe về viết hoa và dấu chấm câu.',
    'Bài không có lỗi nào thì trả "loi": [].',
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:',
    '{"loi": [{"cau":"…","loai":"thieuTu","ghiChu":"…"}]}',
    '',
    'BÀI VIẾT CỦA BÉ:',
    viet,
  ].join('\n');
}

/**
 * MẮT XÍCH 2 — SỬA, KHEN, GỢI Ý. Nhận sẵn danh sách lỗi của mắt xích 1.
 *
 * @param loiDs      mảng lỗi mắt xích 1 tìm ra
 * @param tuLaTruoc  những chữ NGOÀI VỐN mà lượt trước nó vừa dùng. Có thì lời dặn
 *                   mọc thêm một dòng cấm đúng mấy chữ ấy — đây là chỗ mẫu
 *                   Evaluator–Optimizer cắm vào.
 */
export function loiDanSua({ de, viet, vonTu, mauCau, lop }, loiDs = [], tuLaTruoc = []) {
  const ds = (loiDs || []).map((l, i) => `${i + 1}. "${l?.cau ?? ''}"`
    + ` — ${l?.loai || 'khac'}${l?.ghiChu ? `: ${l.ghiChu}` : ''}`);
  return [
    ...dauChung({ de, vonTu, mauCau, lop }),
    ...(ds.length
      ? ['DANH SÁCH LỖI ĐÃ TÌM ĐƯỢC — chấm theo đúng danh sách này, đừng thêm lỗi mới:', ...ds, '']
      : ['KHÔNG CÓ LỖI NÀO ĐƯỢC TÌM RA trong bài này.', '']),
    'LUẬT CHẤM — theo đủ, không bỏ điều nào:',
    '1. Khen CỤ THỂ: nói rõ bé làm được gì (câu nào đúng, dùng đúng từ nào).',
    '   Không khen chung chung kiểu "giỏi lắm".',
    '2. Với MỖI lỗi trên, viết "sua" (câu đúng, TIẾNG ANH) và "viSao"',
    '   (tiếng Việt, nhiều nhất 20 chữ, cho bé tám tuổi hiểu).',
    '3. Câu sửa và câu gợi ý CHỈ ĐƯỢC dùng từ trong bảng vốn từ ở trên.',
    '   Tuyệt đối không dạy từ mới, dù từ ấy hay hơn.',
    '4. Điểm từ 0 tới 10. Bé viết đủ số câu, đúng ngữ pháp, đúng đề thì 9–10.',
    '   Đừng khắt khe về chính tả hoa thường và dấu chấm câu — trừ nhiều nhất 1 điểm.',
    /* ── DÒNG CẤM, chỉ mọc ra khi lượt trước đã dùng chữ ngoài vốn ──
       Nói TÊN mấy chữ ấy, không nói chung chung "đừng dùng từ mới": lượt trước nó
       đã đọc luật 3 rồi và vẫn dùng, nên nhắc lại luật 3 là nhắc một điều nó đã
       nghe. Gọi tên thì nó biết chính xác phải bỏ chữ nào.
       Và cho phép BỎ TRỐNG câu sửa: ép nó phải sửa bằng mọi giá là ép nó bịa thêm
       một chữ khác. Thiếu một câu sửa thì `soiLoiCham` của máy con vẫn còn đó. */
    ...(tuLaTruoc.length ? [
      `5. ⚠ LẦN TRƯỚC bạn đã dùng những từ KHÔNG có trong bảng vốn: ${tuLaTruoc.join(', ')}.`,
      '   KHÔNG được dùng lại bất kỳ từ nào trong số đó.',
      '   Nếu không diễn đạt được câu sửa bằng bảng vốn thì để "sua": "" — bỏ trống',
      '   còn hơn dạy bé một chữ bé chưa học.',
    ] : []),
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:',
    '{"diem": 8, "khen": "…", "loi": [{"cau":"…","sua":"…","viSao":"…"}], "goiY": "…"}',
    '- "khen", "viSao", "goiY": TIẾNG VIỆT.',
    '- "cau", "sua": TIẾNG ANH.',
    '- Bài không có lỗi nào thì "loi": [].',
    '',
    'BÀI VIẾT CỦA BÉ:',
    viet,
  ].join('\n');
}

/**
 * MẮT XÍCH 3 — HAI CÂU CHO BỐ MẸ.
 *
 * ⚠ KHÔNG đưa bài viết của bé vào đây, chỉ đưa LỜI CHẤM. Bố mẹ cần biết "con làm
 * được gì, tuần này nên tập gì" — hai câu ấy suy từ lời chấm là đủ, mà bớt một bản
 * bài viết nữa thì bớt một chỗ chữ của bé đi qua.
 */
export function loiDanBoMe({ lop }, cham = null) {
  return [
    `Dưới đây là lời chấm một bài viết tiếng Anh của bé lớp ${lop}.`,
    'Viết ĐÚNG HAI câu tiếng Việt cho BỐ MẸ:',
    '(1) con làm được gì; (2) tuần này nên tập gì.',
    'CHỈ dùng tên từ và mẫu câu đã có trong lời chấm — không thêm nhận xét nào về',
    'tính cách con, không nhắc điểm số.',
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON: {"choBoMe": "…"}',
    '',
    'LỜI CHẤM:',
    JSON.stringify(cham ?? {}),
  ].join('\n');
}

/**
 * Lời dặn MỘT LƯỢT của bản trước V4 — GIỮ LẠI, và giữ có lý do.
 *
 * `khungCham` dựng vân tay bằng cách gọi lại hàm dựng lời dặn với dữ liệu rỗng, và
 * bảng so ΔC đã gom lượt của mẫu 1 theo chính khung ấy. Xoá hàm này là xoá luôn khả
 * năng dựng lại khung của mẫu 1, tức mất phần đã gom được.
 */
export function loiDanCham({ de, viet, vonTu, mauCau, lop }) {
  return [
    ...dauChung({ de, vonTu, mauCau, lop }),
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
/**
 * KHUNG của lời dặn — dựng bằng CHÍNH `loiDanCham` với phần riêng để rỗng.
 *
 * Không lọc đoán bằng `locKhung`: ở đây ta SỞ HỮU hàm dựng lời dặn, nên gọi lại
 * nó với dữ liệu rỗng là ra đúng phần khung, không sót không thừa. Sửa lời dặn
 * thì khung tự đổi theo — không có bảng nào phải nhớ cập nhật.
 *
 * `lop` GIỮ LẠI trong khung, cố ý: lời dặn cho bé lớp 3 và lớp 5 là hai mẫu khác
 * nhau thật (câu đầu ghi rõ lớp), nên gom chung khi so ΔC là gom nhầm.
 */
export const khungCham = (lop, coMauCau) => [
  /* ⚠ KHUNG = BA KHUNG GHÉP LẠI (từ V4). Lời dặn nay là một CHUỖI ba mắt xích, nên
     khung của nó phải là khung của cả ba — dựng từ một mắt xích thôi thì hai mắt
     xích kia sửa bao nhiêu cũng không làm vân tay đổi, và bảng so ΔC gom lẫn hai
     mẫu khác nhau mà không ai thấy. */
  loiDanTimLoi({ de: '', viet: '', vonTu: [], mauCau: coMauCau ? ['—'] : [], lop }),
  loiDanSua({ de: '', viet: '', vonTu: [], mauCau: coMauCau ? ['—'] : [], lop }, []),
  loiDanBoMe({ lop }, null),
].join('\n');

/** Nhiều nhất bao nhiêu lần xin lại mắt xích 2 khi nó dùng chữ ngoài vốn. */
export const SUA_LAI_TOI_DA = 2;

/**
 * Trần token RIÊNG từng mắt xích, và tổng phải dưới trần cũ.
 *
 * Mắt xích 1 chỉ liệt kê lỗi nên ngắn; mắt xích 2 viết sửa + khen + gợi ý nên dài
 * nhất; mắt xích 3 đúng hai câu. Tổng 1300 — chừa dư so với 900 của một lượt cũ, vì
 * nay là ba lượt, nhưng mỗi lượt lại nhẹ hơn hẳn.
 */
export const TOKEN_TIM_LOI = 400;
export const TOKEN_SUA = 700;
export const TOKEN_BO_ME = 200;

/** Đếm số lần phải xin lại mắt xích 2. Máy chủ không ghi gì — chỉ đếm. */
export const LOI_SUA_LAI = { so: 0, thanh: 0, ganNhat: null };

/* Một lượt gọi Groq. Gom về một chỗ để ba mắt xích không lệch nhau mấy nút vặn. */
async function goiMot(client, dan, { nhiet, token }) {
  const kq = await client.chat.completions.create({
    model: MO_HINH,
    messages: [{ role: 'system', content: dan }],
    temperature: nhiet,
    max_tokens: token,
    reasoning_effort: NGHI_NGAN,
    response_format: { type: 'json_object' },
  });
  const chon = kq?.choices?.[0];
  const chu = chon?.message?.content || '';
  if (!chu.trim()) {
    throw new LoiGoi('tra-loi-rong',
      `Máy chấm không trả lời được (finish_reason: ${chon?.finish_reason || 'không rõ'}).`);
  }
  return chu;
}

/* Bóc JSON. Mô hình được dặn trả đúng một khối, nhưng KHÔNG được tin là nó luôn
   làm đúng — kèm lời dẫn quanh khối là chuyện thường. */
function bocJSON(chu) {
  const m = String(chu || '').match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch { return null; }
}

/**
 * CHẤM MỘT BÀI — chuỗi ba mắt xích, có một phép soi chen vào giữa (việc V4).
 *
 *   1  tìm lỗi (CẤM sửa)          → danh sách lỗi
 *   2  sửa + khen + gợi ý         → lời chấm
 *   ⌐  soi chữ lạ NGAY TẠI MÁY CHỦ (`chula.js`) — có thì quay lại 2 kèm chữ cấm,
 *      nhiều nhất `SUA_LAI_TOI_DA` lần
 *   3  hai câu cho bố mẹ           → ghép vào
 *
 * ⚠ MỘT LỜI GỌI CỦA MÁY CON, BA LƯỢT Ở MÁY CHỦ. §7 cho hai cách; chọn cách này để
 * máy con không phải biết về chuỗi, và quan trọng hơn: vòng gọi lại phải nằm cùng
 * phía với phép soi, nếu không thì tới lúc biết đã hết lượt gọi.
 *
 * ⚠ HỎNG Ở MẮT XÍCH 3 THÌ KHÔNG LÀM HỎNG CẢ LỜI CHẤM. Lời cho bố mẹ là phần phụ;
 * mất nó thì bé vẫn có đủ điểm, lời khen và chỗ sửa. Mất cả lời chấm vì hai câu
 * tiếng Việt cho người lớn thì không đáng.
 *
 * Máy chủ vẫn KHÔNG lưu gì.
 */
export async function chamBaiViet(du, taoClient) {
  const goi = soiBaiViet(du);
  const client = taoClient();
  const kho = { vonTu: goi.vonTu, mauCau: goi.mauCau };

  /* ── MẮT XÍCH 1 ── Trượt thì vẫn đi tiếp với danh sách lỗi RỖNG: mắt xích 2 tự
     tìm lỗi được như bản cũ, chỉ là kém hơn. Dừng cả lời chấm thì bé mất hết. */
  let loiDs = [];
  try {
    const b1 = bocJSON(await goiMot(client, loiDanTimLoi(goi),
      { nhiet: 0.1, token: TOKEN_TIM_LOI }));
    if (Array.isArray(b1?.loi)) loiDs = b1.loi;
  } catch (e) {
    if (e instanceof LoiGoi && e.ma !== 'tra-loi-rong') throw e;
  }

  /* ── MẮT XÍCH 2, VÀ VÒNG XIN LẠI ── */
  let cham = null;
  let chuTho = '';
  let lanSuaLai = 0;
  let tuLa = [];
  for (let i = 0; i <= SUA_LAI_TOI_DA; i += 1) {
    chuTho = await goiMot(client, loiDanSua(goi, loiDs, tuLa),
      { nhiet: 0.2, token: TOKEN_SUA });
    cham = bocJSON(chuTho);
    const laMoi = chuLaTrongCham(cham, kho);
    if (!laMoi.length) {
      if (i > 0) LOI_SUA_LAI.thanh += 1;
      tuLa = [];
      break;
    }
    if (i === SUA_LAI_TOI_DA) { tuLa = laMoi; break; }
    /* Dồn chữ cấm qua các vòng: bỏ chữ A rồi dùng chữ B, vòng sau lại quay về A là
       chuyện đã thấy ở vòng gọi lại của phòng nói. */
    tuLa = [...new Set([...tuLa, ...laMoi])];
    lanSuaLai += 1;
    LOI_SUA_LAI.so += 1;
    LOI_SUA_LAI.ganNhat = laMoi.join(', ');
  }

  /* ── MẮT XÍCH 3 ── Ghép `choBoMe` vào lời chấm. */
  if (cham && !cham.choBoMe) {
    try {
      const b3 = bocJSON(await goiMot(client, loiDanBoMe(goi, cham),
        { nhiet: 0.3, token: TOKEN_BO_ME }));
      if (b3?.choBoMe) cham = { ...cham, choBoMe: String(b3.choBoMe) };
    } catch { /* phần phụ — mất thì thôi, xem ghi chú trên */ }
  }

  /* Trả CHỮ TRẦN như bản cũ: việc bóc JSON và SOI lời chấm vẫn là của máy con
     (`lib/chamviet.js`, có cổng canh) — `soiLoiCham` là hàng rào CUỐI và không
     được bỏ, kể cả khi máy chủ đã soi một lần. Hai tầng cho cùng một chỗ hỏng là
     cố ý: tầng này gọi lại được, tầng kia thì bỏ đúng mục hỏng. */
  return {
    chu: cham ? JSON.stringify(cham) : chuTho,
    moHinh: MO_HINH,
    /* Số lần phải xin lại, và chữ lạ CÒN SÓT sau khi hết vòng — máy con ghi vào
       `hocBaTA` để còn đếm trên bản thật. */
    lanSuaLai,
    chuLaConLai: tuLa,
    ...vanTay('chamviet', khungCham(goi.lop, goi.mauCau.length > 0), {
      moHinh: MO_HINH, nhiet: 0.2, token: TOKEN_SUA,
    }),
  };
}
