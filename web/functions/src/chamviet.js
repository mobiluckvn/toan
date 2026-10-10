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
 * MẮT XÍCH 1b — CHỈ LIỆT KÊ CHỖ BÉ LÀM ĐƯỢC. Chạy SONG SONG với mắt xích 1.
 *
 * ── VÌ SAO TÁCH KHỎI MẮT XÍCH 1, VÀ VÌ SAO KHÔNG GỘP VÀO MẮT XÍCH 2 ──
 * Trước V10, lời khen do mắt xích 2 viết — cùng một lượt với việc sửa lỗi. Lượt ấy
 * vừa đọc một danh sách lỗi xong, nên lời khen nó viết ra hay là lời khen về chính
 * cái bài vừa bị liệt ra năm lỗi: "con viết được ba câu rồi" — đúng mà rỗng, vì nó
 * chưa đi tìm chỗ nào đáng khen, nó chỉ cần điền vào trường "khen".
 *
 * Tách ra thành một lượt RIÊNG, lượt ấy chỉ có đúng một việc: đọc bài bé và tìm chỗ
 * làm được. Nó không thấy danh sách lỗi, nên không bị cái danh sách ấy lái.
 *
 * Và vì hai việc KHÔNG phụ thuộc nhau, chúng chạy song song — thêm một lượt gọi mà
 * gần như không thêm giây chờ nào. Đó là chỗ mẫu #3 cắm vào.
 *
 * ⚠ CẤM SỬA, Y NHƯ MẮT XÍCH 1. Cho nó viết câu đúng thì nó lại viết bằng từ hay
 * nhất nó biết — cùng một cửa cho chữ ngoài vốn mà cả V4 sinh ra để đóng.
 */
export function loiDanTimKhen({ de, viet, vonTu, mauCau, lop }) {
  return [
    ...dauChung({ de, vonTu, mauCau, lop }),
    'VIỆC CỦA BẠN LÚC NÀY: CHỈ TÌM CHỖ BÉ LÀM ĐƯỢC. KHÔNG SỬA, KHÔNG CHẤM ĐIỂM,',
    'KHÔNG NÓI LỖI.',
    'Mỗi chỗ một mục, và chỉ gồm hai thứ:',
    '- "cau": câu bé viết, NGUYÊN VĂN, không chữa một chữ nào;',
    '- "vi": nhiều nhất 15 chữ tiếng Việt, nói rõ CÁI GÌ trong câu ấy đúng',
    '  (dùng đúng từ nào, đúng mẫu câu nào, đúng ý nào của đề).',
    'Chỉ khen cái NHÌN THẤY ĐƯỢC trong bài. Không khen tính cách, không khen',
    'chung chung kiểu "viết tốt".',
    'Bài không có chỗ nào đáng khen thì trả "khen": [] — thà trống còn hơn khen',
    'một câu sai.',
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:',
    '{"khen": [{"cau":"…","vi":"…"}]}',
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
export function loiDanSua(
  { de, viet, vonTu, mauCau, lop }, loiDs = [], tuLaTruoc = [], khenDs = [],
) {
  const ds = (loiDs || []).map((l, i) => `${i + 1}. "${l?.cau ?? ''}"`
    + ` — ${l?.loai || 'khac'}${l?.ghiChu ? `: ${l.ghiChu}` : ''}`);
  /* Danh sách khen của mắt xích 1b, ĐÃ qua `gopKhen` ở phía gọi. */
  const kds = (khenDs || []).map((k, i) => `${i + 1}. "${k?.cau ?? ''}" — ${k?.vi ?? ''}`);
  return [
    ...dauChung({ de, vonTu, mauCau, lop }),
    ...(ds.length
      ? ['DANH SÁCH LỖI ĐÃ TÌM ĐƯỢC — chấm theo đúng danh sách này, đừng thêm lỗi mới:', ...ds, '']
      : ['KHÔNG CÓ LỖI NÀO ĐƯỢC TÌM RA trong bài này.', '']),
    /* ── CHỖ ĐÁNG KHEN, do một lượt RIÊNG tìm ra (việc V10) ──
       Đưa vào đây để lời khen dựa trên một phép đọc bài THẬT, chứ không phải điền
       vào trường "khen" sau khi vừa đọc năm lỗi. Danh sách rỗng thì không dựng dòng
       nào: nói "không có gì đáng khen" là mời nó bịa ra một câu khen cho đủ. */
    ...(kds.length
      ? ['CHỖ BÉ LÀM ĐƯỢC — ĐÃ TÌM RA SẴN, lời khen phải lấy từ đúng danh sách này:',
        ...kds, '']
      : []),
    'LUẬT CHẤM — theo đủ, không bỏ điều nào:',
    ...(kds.length
      ? ['1. Trường "khen" viết lại danh sách trên thành một hai câu cho bé nghe.',
        '   KHÔNG thêm chỗ đáng khen nào ngoài danh sách ấy.']
      : ['1. Khen CỤ THỂ: nói rõ bé làm được gì (câu nào đúng, dùng đúng từ nào).',
        '   Không khen chung chung kiểu "giỏi lắm".']),
    '2. Với MỖI lỗi trên, viết "sua" (câu đúng, TIẾNG ANH) và "viSao"',
    '   (tiếng Việt, nhiều nhất 20 chữ, cho bé tám tuổi hiểu).',
    /* ⚠ GIỮ BA DÒNG. Bản đầu viết bảy dòng cho đúng luật này, và mắt xích 2 cạn
       token ngay lượt gọi đầu: Groq trả 400 `json_validate_failed`. Lời dặn dài thì
       `gpt-oss-120b` nghĩ lâu hơn, mà phần nghĩ ăn chung trần với phần viết — đúng
       cái bẫy đã ghi ở `goiMot`. Nới luật thì nới bằng chữ ngắn. */
    '3. Câu sửa và câu gợi ý CHỈ ĐƯỢC dùng: từ trong bảng vốn, từ CHÍNH BÉ đã viết,',
    '   và dạng biến hình của chúng (-s, -es, -ed, -ing). Sửa "two friend" thành',
    '   "two friends" LÀ ĐƯỢC. Ngoài ba thứ ấy thì không dạy từ mới, dù hay hơn.',
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
export const khungCham = (lop, coMauCau) => {
  const rong = { de: '', viet: '', vonTu: [], mauCau: coMauCau ? ['—'] : [], lop };
  return [
    /* ⚠ KHUNG = MỌI MẮT XÍCH GHÉP LẠI (từ V4, nay BỐN từ V10). Lời dặn là một chuỗi,
       nên khung của nó phải là khung của cả chuỗi — dựng từ một mắt xích thôi thì
       mấy mắt xích kia sửa bao nhiêu cũng không làm vân tay đổi, và bảng so ΔC gom
       lẫn hai mẫu khác nhau mà không ai thấy. */
    loiDanTimLoi(rong),
    loiDanTimKhen(rong),
    /* ⚠ Dựng mắt xích 2 với danh sách khen RỖNG lẫn CÓ: từ V10 nó có hai nhánh luật
       1 khác nhau, và khung chỉ dựng một nhánh thì nửa lời dặn kia nằm ngoài vân
       tay. Một mục "—" là đủ để nhánh "có khen" mọc ra. */
    loiDanSua(rong, [], [], []),
    loiDanSua(rong, [], [], [{ cau: '—', vi: '—' }]),
    loiDanBoMe({ lop }, null),
  ].join('\n');
};

/** Nhiều nhất bao nhiêu lần xin lại mắt xích 2 khi nó dùng chữ ngoài vốn. */
export const SUA_LAI_TOI_DA = 2;

/**
 * Trần token RIÊNG từng mắt xích, và tổng phải dưới trần cũ.
 *
 * Mắt xích 1 chỉ liệt kê lỗi nên ngắn; mắt xích 2 viết sửa + khen + gợi ý nên dài
 * nhất; mắt xích 3 đúng hai câu. Tổng 1800 (từ 10-10-2026, trước là 1300) — cổng
 * `tienganh_chamviet` canh con số ấy và ghi lý do vì sao nó nhích lên.
 */
export const TOKEN_TIM_LOI = 400;
export const TOKEN_TIM_KHEN = 300;   // chỉ liệt kê, ngắn hơn mắt xích tìm lỗi
/* 900, không phải 700: luật 3 dài thêm mấy chữ (vá 10-10-2026) là mô hình nghĩ lâu
   thêm, và nghĩ hết trần thì Groq trả 400 `json_validate_failed` — bé thấy "chưa
   chấm được". Đo thật: 700 vỡ, 900 qua. */
export const TOKEN_SUA = 900;
export const TOKEN_BO_ME = 200;

/**
 * Nhiều nhất bao nhiêu chỗ khen được đưa sang mắt xích 2, và mỗi chỗ dài bao nhiêu.
 *
 * Ba là đủ: bé tám tuổi nghe quá ba điều một lúc thì không giữ được điều nào, và
 * lời khen dài thì phần phải sửa bị đẩy xuống dưới chỗ bé còn đọc.
 */
export const KHEN_TOI_DA = 3;
export const KHEN_TOI_DA_CHU = 80;

/** Đếm số lần phải xin lại mắt xích 2. Máy chủ không ghi gì — chỉ đếm. */
export const LOI_SUA_LAI = { so: 0, thanh: 0, ganNhat: null };

/**
 * GỘP "LỖI ∥ KHEN" BẰNG MÃ — không để mô hình tự hoà giải hai danh sách (việc V10).
 *
 * Hai lượt chạy song song nên chúng KHÔNG thấy nhau. Thế là tốt cho việc đọc bài,
 * nhưng nó để lại đúng hai chỗ hỏng mà chỉ mã mới bịt được:
 *
 * ── 1 · KHEN MỘT CÂU BÉ KHÔNG HỀ VIẾT ──
 * Lượt tìm khen được dặn "nguyên văn", nhưng cái nó hay làm là khen câu bé ĐÁNG LẼ
 * viết: bé viết "I have two cat", nó khen "I have two cats". Khen một câu đúng mà
 * bé không viết là dạy sai và khen oan cùng lúc. Nên mỗi câu khen phải TÌM THẤY
 * ĐƯỢC trong bài viết của bé; không thấy thì bỏ mục ấy.
 *
 * Đây là phép soi mà mô hình không làm thay được, vì nó cần đối chiếu với bản gốc
 * mà chính nó vừa diễn giải.
 *
 * ── 2 · CÙNG MỘT CÂU VỪA ĐƯỢC KHEN VỪA BỊ LIỆT LỖI ──
 * Chuyện này xảy ra thật, và nó là hệ quả của việc chạy song song: lượt khen thấy
 * "I have two cat" dùng đúng từ `cat` và đúng mẫu `I have…`, còn lượt tìm lỗi thấy
 * nó thiếu `s`. Cả hai đều đúng. Nhưng nói với bé "câu này con viết đúng lắm" rồi
 * ba dòng sau "câu này sai, phải sửa thành…" thì bé không biết tin dòng nào.
 *
 * LỖI THẮNG. Bé còn phải sửa câu ấy, nên câu ấy không được nằm trong phần khen —
 * phần khen còn những câu khác, và nếu không còn câu nào thì thà không khen câu nào
 * hơn là khen đúng câu đang sai.
 */
const xepPhang = (x) => String(x ?? '')
  .toLowerCase()
  .replace(/[^a-z0-9\s']/g, ' ')
  .replace(/\s+/g, ' ')
  .trim();

export function gopKhen(loiDs, khenDs, viet) {
  const baiPhang = xepPhang(viet);
  /* Câu đã bị liệt lỗi — so bằng bản xếp phẳng, vì mắt xích 1 và 1b trích cùng một
     câu ra có thể lệch nhau dấu phẩy hoặc chữ hoa. */
  const coLoi = new Set((loiDs || []).map((l) => xepPhang(l?.cau)).filter(Boolean));
  const daCo = new Set();
  const ra = [];
  for (const k of khenDs || []) {
    const cau = String(k?.cau ?? '').trim();
    const vi = String(k?.vi ?? '').trim();
    if (!cau || !vi) continue;
    const phang = xepPhang(cau);
    if (!phang) continue;
    /* ⚠ `includes` trên bản xếp phẳng, KHÔNG so bằng nhau: mắt xích 1b hay trích
       một câu trong bài nhiều câu, và nó cắt chỗ nào là chuyện của nó. Soi bằng
       phép so bằng là bỏ gần hết mục đúng. */
    if (!baiPhang.includes(phang)) continue;
    if (coLoi.has(phang)) continue;
    if (daCo.has(phang)) continue;
    daCo.add(phang);
    ra.push({ cau, vi: vi.slice(0, KHEN_TOI_DA_CHU) });
    if (ra.length >= KHEN_TOI_DA) break;
  }
  return ra;
}

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
  /* `beViet` — chữ chính bé vừa viết cũng tính là chữ bé biết. Máy con chuyền đúng
     thứ này vào `soiLoiCham`, hai bên phải dựng kho GIỐNG HỆT nhau. */
  const kho = { vonTu: goi.vonTu, mauCau: goi.mauCau, beViet: goi.viet };

  /* ── MẮT XÍCH 1 ∥ 1b — HAI LƯỢT SONG SONG (việc V10) ──
     Tìm lỗi và tìm chỗ đáng khen là hai việc KHÔNG phụ thuộc nhau, nên chúng chạy
     cùng lúc: cả cặp tốn đúng quãng chờ của lượt chậm hơn, không phải tổng hai.
     Quãng chờ ở đây là lúc bé đã bấm "nhờ cô chấm" và đang ngồi nhìn màn hình.

     ⚠ MỖI NHÁNH TỰ ĐỠ LẤY, KHÔNG DÙNG `Promise.all` TRỰC TIẾP TRÊN LỜI GỌI.
     `Promise.all` hỏng một nhánh là hỏng cả cặp — mà ở đây hỏng một nhánh phải đi
     tiếp được: mất danh sách lỗi thì mắt xích 2 tự tìm lỗi như bản trước V4; mất
     danh sách khen thì nó tự khen như bản trước V10. Dừng cả lời chấm vì một trong
     hai lượt phụ trượt thì bé mất hết. Nên mỗi nhánh bắt lỗi NGAY TRONG nhánh và
     trả về mảng rỗng. */
  const [loiDs, khenTho] = await Promise.all([
    (async () => {
      try {
        const b1 = bocJSON(await goiMot(client, loiDanTimLoi(goi),
          { nhiet: 0.1, token: TOKEN_TIM_LOI }));
        return Array.isArray(b1?.loi) ? b1.loi : [];
      } catch (e) {
        /* Gói sai thì vẫn phải ném ra ngoài — đó là lỗi của máy con, không phải
           trục trặc của mô hình, và che nó đi là che một lỗi lập trình. */
        if (e instanceof LoiGoi && e.ma !== 'tra-loi-rong') throw e;
        return [];
      }
    })(),
    (async () => {
      try {
        const b = bocJSON(await goiMot(client, loiDanTimKhen(goi),
          { nhiet: 0.2, token: TOKEN_TIM_KHEN }));
        return Array.isArray(b?.khen) ? b.khen : [];
      } catch (e) {
        if (e instanceof LoiGoi && e.ma !== 'tra-loi-rong') throw e;
        return [];
      }
    })(),
  ]);

  /* Gộp BẰNG MÃ, không để mô hình tự hoà giải — xem `gopKhen`. */
  const khenDs = gopKhen(loiDs, khenTho, goi.viet);

  /* ── MẮT XÍCH 2, VÀ VÒNG XIN LẠI ── */
  let cham = null;
  let chuTho = '';
  let lanSuaLai = 0;
  let tuLa = [];
  for (let i = 0; i <= SUA_LAI_TOI_DA; i += 1) {
    chuTho = await goiMot(client, loiDanSua(goi, loiDs, tuLa, khenDs),
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
    /* Số chỗ đáng khen CÒN LẠI sau phép gộp. Đo được thì mới biết mắt xích 1b có
       đáng một lượt gọi hay không — xem `tools/doc_delta_c.mjs`. */
    soKhen: khenDs.length,
    soKhenBo: khenTho.length - khenDs.length,
    ...vanTay('chamviet', khungCham(goi.lop, goi.mauCau.length > 0), {
      moHinh: MO_HINH, nhiet: 0.2, token: TOKEN_SUA,
    }),
  };
}
