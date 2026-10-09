/**
 * BỐN TOOL CHO PHÒNG LUYỆN NÓI (việc V11, mẫu #5 ReAct).
 *
 * ── CHỖ HỎNG NÓ ĐI CHỮA ──
 * Nhãn `hoiLai` (việc V2) bắt được lúc bé ĐẶT CÂU HỎI: "cô ơi dog là gì?". Lời dặn
 * của nhãn ấy (§9 mục A7) nói: "nếu từ ấy nằm trong bảng vốn thì trả lời nghĩa của
 * nó LẤY TỪ BẢNG". Nhưng bảng vốn trong lời dặn là một dòng dài hàng trăm chữ, và
 * mô hình phải tự tìm chữ bé hỏi trong đó rồi tự nhớ nghĩa — ở lớp 3 trở lên vốn đã
 * trộn thêm hai ba unit cũ, nên dòng ấy dài tới mức việc "tìm trong bảng" thành việc
 * nó làm theo cảm giác. Mà nhớ sai một nghĩa là dạy sai một chữ.
 *
 * Nên đảo lại: đừng bắt nó NHỚ, cho nó TRA. Bốn tool, mỗi tool một câu hỏi rất hẹp,
 * và câu trả lời là chữ lấy thẳng từ dữ liệu bài.
 *
 * ── TOOL LÀ HÀM THUẦN TRÊN GÓI `kho` MÁY CON GỬI LÊN ──
 * Máy chủ KHÔNG có dữ liệu riêng và KHÔNG đọc Firestore ở đây. Cả bốn tool chạy
 * trên đúng gói `kho` đi kèm lời gọi, rồi gói ấy biến mất cùng lời gọi. Giao ước
 * "máy chủ không lưu gì" giữ nguyên — và nó không chỉ giữ được mà còn DỄ giữ hơn:
 * một tool biết tự đi tìm dữ liệu là một tool cần quyền đọc, mà quyền đọc là chỗ
 * dữ liệu của bé bắt đầu rò.
 *
 * ── VÀ KHÔNG TOOL NÀO CÓ TÁC DỤNG PHỤ ──
 * Bản thiết kế chốt thế, và đây là chỗ dễ phá nhất vì `nghe_lai` NGHE NHƯ một tool
 * có tác dụng phụ (phát tiếng). Nó không: ở đây nó chỉ soi xem chữ ấy có trong bài
 * không rồi nói "được". Việc phát clip là của MÁY CON, sau khi đọc danh sách bước —
 * xem `lib/hoico.js`. Ranh giới ấy không phải chuyện gu: một tool phát được tiếng là
 * một tool mô hình có thể gọi mười lần, và bé thì không có nút tắt.
 */

/**
 * Trần số bước ReAct.
 *
 * Ba là đủ cho mọi câu hỏi bé sáu tới mười tuổi đặt ra trong phòng nói: tra chữ ·
 * xem mẫu câu · nghe lại. Nới rộng là mở cửa cho vòng lặp mà bé phải ngồi đợi, và
 * mỗi bước là một lượt gọi mạng trả tiền thật.
 */
export const BUOC_TOI_DA = 3;

/**
 * Trần độ dài MỘT kết quả tool.
 *
 * ⚠ Đây là chốt quan trọng hơn vẻ ngoài của nó. Kết quả tool đi THẲNG vào ngữ cảnh
 * của lượt gọi sau, nên một kết quả dài là một lời dặn thứ hai không ai soi — và nó
 * mang chữ của dữ liệu bài, tức mang được cả những chữ KHÔNG thuộc vốn của bé nếu
 * gói `kho` bị dựng sai. Cắt ngắn lại là giới hạn thiệt hại của chỗ ấy.
 */
export const KET_QUA_TOI_DA_CHU = 300;

/** Trần gói `kho`. Rộng cho một bài thật ở lớp 5, đủ chặn một gói bất thường. */
export const TOI_DA_TU_KHO = 400;
export const TOI_DA_CAU_KHO = 80;
export const TOI_DA_CHU_TOM_TAT = 300;

/** Đếm để còn lần ra. Máy chủ KHÔNG ghi gì xuống Firestore. */
export const LOI_TOOL = { goi: 0, lap: 0, hetBuoc: 0, khongRo: 0, ganNhat: null };

/**
 * Khai báo tool gửi cho mô hình.
 *
 * ⚠ MÔ TẢ PHẢI NÓI RÕ GIỚI HẠN, không chỉ nói công dụng. "Tra nghĩa một từ" thì mô
 * hình gọi nó cho mọi từ tiếng Anh trên đời rồi nhận về "không có trong bài" ba lần
 * và hết lượt. Nói thẳng "chỉ những từ bài này dạy" thì nó biết trước là vô ích.
 */
export const TOOLS = [
  {
    type: 'function',
    function: {
      name: 'tra_tu',
      description: 'Look up the Vietnamese meaning of ONE English word, but only '
        + 'for words this lesson teaches. Any other word returns "not in this lesson".',
      parameters: {
        type: 'object',
        properties: { tu: { type: 'string', description: 'the English word' } },
        required: ['tu'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'mau_cau_cua_unit',
      description: 'List the sentence patterns this lesson teaches. No arguments.',
      parameters: { type: 'object', properties: {}, required: [] },
    },
  },
  {
    type: 'function',
    function: {
      name: 'muc_thao',
      description: 'A short note, in Vietnamese, on which words this child is '
        + 'already solid on and which are still shaky. No arguments.',
      parameters: { type: 'object', properties: {}, required: [] },
    },
  },
  {
    type: 'function',
    function: {
      name: 'nghe_lai',
      description: 'Ask for ONE word of this lesson to be read aloud to the child. '
        + 'Use it when she asks how a word sounds. Only words this lesson teaches.',
      parameters: {
        type: 'object',
        properties: { tu: { type: 'string', description: 'the English word' } },
        required: ['tu'],
      },
    },
  },
];

/** Tên bốn tool TRA, rút từ CHÍNH `TOOLS` — đừng viết lại danh sách thứ hai. */
export const TEN_TOOL = TOOLS.map((t) => t.function.name);

/**
 * TOOL THỨ NĂM: TRẢ LỜI BÉ. Không phải tool tra — nó là KÊNH GIAO CÂU TRẢ LỜI.
 *
 * ── VÌ SAO PHẢI CÓ, VÀ VÌ SAO LÀ MỘT TOOL ──
 * Đo thật với Groq, 19/20 lượt chết với 400:
 *     attempted to call tool 'json' which was not in request.tools
 * Mô hình KHÔNG gọi tool tra nào. Lời dặn (`loiDan`) đòi "trả lời dạng JSON
 * {en, vi}" trong khối HARD RULES; gói lại có `tools`. Thế là nó đi trả lời QUA
 * kênh tool, bằng một tool nó tự đặt tên là `json` — và `failed_generation` cho
 * thấy nội dung bên trong ĐÚNG hình dạng ta cần: `{"en": …, "vi": …}`.
 *
 * Bản vá đầu của tôi là chèn một dòng "đừng trả JSON lượt này". Nó KHÔNG ăn — vẫn
 * 19/20 chết y như trước. Vì dòng ấy nằm DƯỚI khối HARD RULES, và chỗ hỏng
 * `loi-dan-tu-choi-nhau` của V1 đã nói rõ: HARD RULES thắng mọi dòng ở dưới. Đây là
 * lần thứ ba cùng một họ lỗi, và lần này tôi tự chuốc lấy nó.
 *
 * Nên đừng chống nữa: mô hình đang nói rõ nó muốn giao diện nào. Khai đúng tool ấy,
 * và cái nó vẫn làm trở thành đường đúng. Đổi lại được hai thứ:
 *   · hết hẳn lỗi 400 ấy;
 *   · và RẺ HƠN bản trước — trả lời ngay ở lượt một, không cần lượt chốt.
 *
 * ⚠ KHÔNG đưa nó vào `TOOLS`: `TOOLS` là bốn tool TRA, và `chayTool` chỉ chạy bốn
 * cái ấy. Tool này không "chạy" — nó được ĐỌC. Gộp vào một danh sách thì sớm muộn
 * có người cho nó đi qua `chayTool` và câu trả lời của cô biến thành một chuỗi
 * "there is no tool called…".
 */
export const TOOL_TRA_LOI = {
  type: 'function',
  function: {
    name: 'tra_loi_be',
    description: 'Give your final reply to the child. Call this when you are ready — '
      + 'it is the ONLY way to answer. Do not write the answer as plain text.',
    parameters: {
      type: 'object',
      properties: {
        en: { type: 'string', description: 'ONE English sentence, allowed words only' },
        vi: { type: 'string', description: 'what you say to her in Vietnamese' },
      },
      required: ['en', 'vi'],
    },
  },
};

export const TEN_TRA_LOI = TOOL_TRA_LOI.function.name;

/** Cái THẬT SỰ gửi lên mô hình: bốn tool tra, cộng kênh trả lời. */
export const TOOLS_GUI = [...TOOLS, TOOL_TRA_LOI];

const chuan = (s) => String(s ?? '').trim().toLowerCase();

/**
 * Soi gói `kho` máy con gửi lên. Trả gói đã sạch, hoặc ném.
 *
 * Tách khỏi phần gọi mạng để chạy được bằng `node` mà không cần khoá — cùng khuôn
 * `soiGoi` và `soiGoiPhuDao`.
 *
 * ⚠ KHÔNG ném khi `kho` RỖNG: nhánh ReAct phải chạy được với một gói nghèo (bài
 * chưa có mẫu câu, bé chưa có mục thạo nào). Lúc ấy tool trả "không có", mà "không
 * có" là một câu trả lời tử tế — còn ném thì bé mất cả lượt vì một thứ bé không
 * biết là có.
 */
export function soiKho(kho, nem) {
  const tu = Array.isArray(kho?.vonTu) ? kho.vonTu : [];
  const cau = Array.isArray(kho?.mauCau) ? kho.mauCau : [];
  if (tu.length > TOI_DA_TU_KHO) nem('kho-qua-lon', `Vốn từ nhiều quá ${TOI_DA_TU_KHO} mục.`);
  if (cau.length > TOI_DA_CAU_KHO) nem('kho-qua-lon', `Mẫu câu nhiều quá ${TOI_DA_CAU_KHO} mục.`);
  const tomTat = String(kho?.mucThaoTomTat ?? '').trim().slice(0, TOI_DA_CHU_TOM_TAT);
  return {
    vonTu: tu
      .map((v) => ({ tu: String(v?.tu ?? '').trim(), nghia: String(v?.nghia ?? '').trim() }))
      .filter((v) => v.tu),
    mauCau: cau.map((x) => String(x ?? '').trim()).filter(Boolean),
    mucThaoTomTat: tomTat,
  };
}

/** Tìm một từ trong kho. Trả mục, hoặc `null`. */
const timTu = (kho, t) => (kho?.vonTu || []).find((v) => chuan(v.tu) === chuan(t)) || null;

/**
 * CHẠY MỘT TOOL. Thuần, không mạng — nên cổng canh được mọi đường ra.
 *
 * Trả về CHUỖI, luôn luôn, và luôn ≤ `KET_QUA_TOI_DA_CHU`. Không ném: một tool ném
 * là cả vòng ReAct đổ, mà vòng ReAct đổ thì bé mất lượt. Tên tool lạ · thiếu tham
 * số · kho rỗng đều có một câu trả lời tử tế, và mô hình đọc câu ấy rồi đi tiếp.
 */
export function chayTool(ten, args, kho) {
  const cat = (s) => String(s).slice(0, KET_QUA_TOI_DA_CHU);
  const a = args && typeof args === 'object' ? args : {};

  switch (ten) {
    case 'tra_tu': {
      const t = String(a.tu ?? '').trim();
      if (!t) return cat('No word given.');
      const v = timTu(kho, t);
      /* ⚠ "KHÔNG CÓ TRONG BÀI" PHẢI NÓI RÕ RÀNG, và phải nói thêm là ĐỪNG TỰ DỊCH.
         Thiếu câu sau thì mô hình đọc "not in this lesson" rồi vẫn trả lời bé bằng
         nghĩa nó tự biết — tức chữ ngoài vốn đi vào buổi học qua đúng cái cửa mà
         tool này sinh ra để đóng. */
      if (!v) {
        return cat(`"${t}" is NOT in this lesson. Do not translate it yourself — `
          + 'tell the child kindly that you will learn it later.');
      }
      return cat(`"${v.tu}" means "${v.nghia || '(no meaning recorded)'}" in Vietnamese.`);
    }

    case 'mau_cau_cua_unit': {
      const ds = kho?.mauCau || [];
      if (!ds.length) return cat('This lesson records no sentence patterns.');
      return cat(`Patterns in this lesson: ${ds.join(' | ')}`);
    }

    case 'muc_thao': {
      const s = kho?.mucThaoTomTat || '';
      if (!s) return cat('No progress note for this child yet.');
      return cat(s);
    }

    case 'nghe_lai': {
      const t = String(a.tu ?? '').trim();
      if (!t) return cat('No word given.');
      const v = timTu(kho, t);
      if (!v) {
        return cat(`"${t}" is NOT in this lesson, so it cannot be played. `
          + 'Do not say it yourself.');
      }
      /* Tool này KHÔNG phát gì — nó chỉ công nhận chữ ấy phát được. Máy con đọc
         danh sách bước rồi tự phát clip; xem khối chú thích đầu tệp. */
      return cat(`OK — the child will hear "${v.tu}" read aloud. `
        + 'Mention in the Vietnamese line that she should listen.');
    }

    default:
      LOI_TOOL.khongRo += 1;
      LOI_TOOL.ganNhat = `tool lạ: ${ten}`;
      return cat(`There is no tool called "${ten}". Answer the child directly.`);
  }
}

/** Chữ ký một lời gọi tool — dùng để bắt vòng lặp. */
export const chuKyTool = (ten, args) => {
  let x = '';
  try { x = JSON.stringify(args ?? {}); } catch { x = String(args); }
  return `${ten}(${x})`;
};
