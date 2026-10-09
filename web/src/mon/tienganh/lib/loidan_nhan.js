/**
 * CHÍN LỜI DẶN NGẮN — mỗi nhãn một việc duy nhất cho lượt này.
 *
 * ── VÌ SAO TÁCH KHỎI `loiDan` ──
 * Lời dặn chung dài mười điều, và mười điều thì mô hình phải tự đoán điều nào đang
 * áp dụng. Nó đoán theo thứ chiếm nhiều chữ nhất — "dạy bé nhại câu" — nên lượt
 * nào cũng ra một lời khen chung chung rồi đi tiếp, kể cả lượt bé vừa trượt.
 *
 * Nay luật 7 · 8 · 8b của khối chung chuyển hẳn vào đây, thành nội dung của đúng
 * nhánh cần nó. KHÔNG lặp hai nơi: lặp thì sửa một bên là hai bên nói khác nhau,
 * và mô hình nghe bên dài hơn.
 *
 * ══ HAI LOẠI DÒNG, VÀ ĐÓ LÀ MỘT GIAO ƯỚC ══
 * Mỗi lời dặn gồm:
 *
 *   `TURN TYPE: <nhãn>`   dòng KHUÔN — không một chữ nào của bé. Nó ở lại trong
 *                         vân tay, nhờ thế bảng so ΔC (V8) phân biệt được chín
 *                         nhánh với nhau.
 *   `CHILD: …`            dòng RIÊNG — mang chữ bé vừa nói, chữ bé nhầm, câu đích.
 *                         `locKhung` ở `functions/src/vantay.js` BỎ cả dòng này.
 *
 * ⚠ Mọi chữ của bé phải nằm trên dòng mở đầu bằng `CHILD:` — không có ngoại lệ.
 * Dán một mẩu bé nói vào dòng khuôn là nó lọt vào vân tay, và vân tay thì mỗi bé
 * một mã, tức vừa vô dụng cho việc so mẫu vừa thành mã theo dõi từng lượt. Cổng
 * `tienganh_nhanluot.test.mjs` soi đúng tính chất ấy: nó đem TỪNG giá trị của
 * `ctx` đi tìm trong phần `locKhung` giữ lại, chứ không soi chính tả tên dòng.
 */
import { NHAN } from './nhanluot.js';

/** Trần ký tự MỘT lời dặn theo nhãn. Khối chung đã dài, chỗ này phải ngắn. */
export const DAN_NHAN_TOI_DA_CHU = 600;

/** Dấu mở đầu dòng mang dữ liệu riêng của bé. Phải khớp với `DAU_RIENG`. */
export const DAU_DONG_RIENG = 'CHILD:';

/* Cắt ngắn mẩu của bé. Bé sáu tuổi không nói câu dài, nhưng máy nhận tiếng nói có
   lúc trả về cả một đoạn nhiễu — và một đoạn nhiễu dài làm lời dặn vượt trần. */
const cat = (s, n = 90) => {
  const t = String(s ?? '').replace(/\s+/g, ' ').trim();
  return t.length > n ? `${t.slice(0, n - 3)}...` : t;
};

const dsChu = (ds) => cat(Array.isArray(ds) ? ds.join(', ') : ds, 70);

/**
 * CHÍN LỜI DẶN. Khoá lấy thẳng từ `NHAN` — khai tay thì sớm muộn lệch một chữ,
 * và lệch một chữ là một nhãn không có lời dặn, lượt ấy rơi về chuỗi rỗng mà
 * không gì kêu. Cổng đòi `Object.keys(NHAN)` và khoá ở đây trùng khít.
 */
export const LOI_DAN_THEO_NHAN = {
  [NHAN.moDau]: () => [
    'THIS TURN: this is your first turn. Greet her once by name, then give her the',
    'first task. Exactly ONE short English sentence.',
  ],

  [NHAN.dung]: ({ beNoi } = {}) => [
    'THIS TURN: her last sentence was CORRECT. Put a short, SPECIFIC praise in the',
    'Vietnamese line — name the word she got right — then give the NEXT task in',
    'English. Never praise with a bare "good job" and nothing else. Do not repeat',
    'the sentence she just said. Exactly ONE English sentence.',
    `${DAU_DONG_RIENG} she said "${cat(beNoi)}", and it was right.`,
  ],

  [NHAN.thieuTu]: ({ beNoi, dich, thieu } = {}) => [
    'THIS TURN: she LEFT A WORD OUT. In the Vietnamese line, say the one thing that',
    'was already right, then name ONLY the missing word, quoted exactly as it is',
    'written in the word list. In English, say the target sentence again, unchanged.',
    'Do not move on to a new task, and never say "sai rồi" on its own.',
    `${DAU_DONG_RIENG} she said "${cat(beNoi)}"; the target was "${cat(dich)}";`
      + ` she left out: ${dsChu(thieu)}.`,
  ],

  [NHAN.saiThuTu]: ({ beNoi, dich } = {}) => [
    'THIS TURN: she said the right words in the WRONG ORDER. In Vietnamese, tell her',
    'which word comes FIRST — just that one thing. In English, say the target',
    'sentence again: the same words in the right order, ONE sentence, nothing added.',
    'Do not move on to a new task.',
    `${DAU_DONG_RIENG} she said "${cat(beNoi)}"; the target was "${cat(dich)}".`,
  ],

  [NHAN.nhamTu]: ({ nham, dich } = {}) => [
    'THIS TURN: she said a DIFFERENT word from this unit, not the one you asked for.',
    'In Vietnamese, give the meaning of each of the two words, taken from the word',
    'list above — do not translate them yourself. Then ask her to try the target',
    'word. In English, say just that ONE word.',
    `${DAU_DONG_RIENG} she said "${cat(nham, 40)}" instead of "${cat(dich, 40)}".`,
  ],

  [NHAN.tiengViet]: ({ beNoi } = {}) => [
    'THIS TURN: she spoke VIETNAMESE to you, not English. Answer her in the',
    'Vietnamese line kindly and briefly — one sentence — then invite her to try the',
    'SAME English target again. In English, say that target sentence. Do not change',
    'the task, and do not treat this as a wrong answer.',
    `${DAU_DONG_RIENG} she said, in Vietnamese: "${cat(beNoi)}".`,
  ],

  [NHAN.hoiLai]: ({ beNoi } = {}) => [
    'THIS TURN: she ASKED you a question. If it is about a word in the list above,',
    'answer with THAT word\'s meaning from the list, in the Vietnamese line. If it is',
    'about anything else, say gently in Vietnamese that you will learn it later.',
    'In English: the word she asked about if it is in the list, otherwise the current',
    'target sentence. Exactly ONE English sentence.',
    `${DAU_DONG_RIENG} she asked: "${cat(beNoi)}".`,
  ],

  [NHAN.imLang]: () => [
    'THIS TURN: she said NOTHING. Do not scold her, and do not mention the silence.',
    'In Vietnamese, say what the target sentence means in a playful way and ask her',
    'to try — even just the first word. In English, say only the FIRST word of the',
    'target: just ONE word, so it is easy to copy.',
  ],

  [NHAN.lacDe]: ({ beNoi } = {}) => [
    'THIS TURN: her reply does not match the task. Do not comment on what she said',
    'and do not follow it — bring her back to the words above. Restate the task in',
    'Vietnamese with ONE concrete hint: which word to start with. In English, say the',
    'target sentence.',
    `${DAU_DONG_RIENG} she said "${cat(beNoi)}".`,
  ],
};

/**
 * Dòng lời dặn cho lượt này. Nhãn lạ → chuỗi rỗng, KHÔNG ném: một nhãn khai thiếu
 * không đáng làm bé mất cả lượt nói, và cổng thì đã canh đủ chín nhãn.
 */
export function dongTheoNhan(nhan, ctx = {}) {
  const lam = LOI_DAN_THEO_NHAN[nhan];
  if (!lam) return '';
  const than = lam(ctx).join('\n');
  /* Dòng KHUÔN đứng đầu, mang tên nhãn và không một chữ nào của bé — xem giao ước
     ở đầu tệp. Nhờ nó vân tay phân biệt được chín nhánh dù phần dưới bị lọc sạch. */
  return `TURN TYPE: ${nhan}\n${than}`;
}
