/**
 * PHÒNG LUYỆN NÓI — luật vốn từ và ngữ cảnh, để riêng khỏi giao diện và khỏi mạng.
 *
 * Màn hình là một cuộc trò chuyện: máy nói một câu tiếng Anh kèm một lời giải thích
 * tiếng Việt, bé nghe rồi nói lại. Khác chặng "Nói chuyện" ở chỗ chặng ấy đi theo
 * kịch bản viết sẵn, còn ở đây câu do máy sinh — nên bé hỏi lại được, nói sai thì
 * được nói lại theo cách khác, và không bao giờ hết câu.
 *
 * ── VÌ SAO PHẢI BÓ VỐN TỪ, VÀ BÓ THEO UNIT ──
 * Bác chốt 13-08: phòng này nằm TRONG từng unit, nên nó phải xoay quanh đúng từ và
 * cấu trúc của unit ấy. Thả cho máy dùng từ tự do thì nó nói "Do you like chips?"
 * với bé vừa xong unit 1 — bé không hiểu, và cái bé học được không phải tiếng Anh
 * mà là "mình kém". Đúng cái bẫy mà luật đi lần lượt sinh ra để tránh.
 *
 * Nhưng bó CỨNG vào một unit thì bé xong unit rồi vẫn chỉ được nói mãi bốn từ, mà
 * quên từ cũ mới là chuyện hay xảy ra nhất với bé lớp 1. Nên hai chế độ:
 *
 *   chưa đạt unit → CHỈ từ và cấu trúc của chính unit ấy
 *   đạt rồi      → cộng thêm từ và cấu trúc của các unit bé ĐÃ ĐẠT trước đó
 *
 * Vế sau là phần thưởng nhìn thấy được: học xong thì phòng nói rộng ra.
 *
 * ── VÌ SAO TỆP NÀY KHÔNG BIẾT GÌ VỀ MẠNG ──
 * Toàn bộ ở đây là hàm thuần: nhận dữ liệu bài + sổ tiến độ, trả về vốn từ và lời
 * dặn cho máy. Không `fetch`, không Firebase. Nhờ thế cổng chạy được bằng `node`
 * và soi được đúng cái dễ sai nhất — vốn từ bị nới ra lúc nào không biết.
 */

/** Nhiều nhất bao nhiêu unit CŨ được trộn vào. Đủ để ôn, không đủ để loãng. */
export const UNIT_CU_TOI_DA = 3;

/**
 * Bao nhiêu lượt gần nhất được gửi lên máy chủ.
 *
 * Ngữ cảnh do CLIENT giữ (bác chốt: server không lưu gì), nên chính client phải cắt.
 * Không cắt thì buổi nói chuyện dài dần, mỗi lượt gửi lại toàn bộ lịch sử — tiền và
 * độ trễ tăng theo bình phương số lượt, mà bé thì chẳng thấy gì khác.
 */
export const LUOT_GUI_TOI_DA = 12;

/** Chặn câu quá dài trước khi gửi. Bé 6 tuổi không gõ, nên dài bất thường là hỏng. */
export const CHU_TOI_DA = 300;

/* ─────────── vốn từ ─────────── */

const goiTu = (v) => ({ tu: v.tu, nghia: v.nghia, ipa: v.ipa });
const goiCau = (m) => ({ cau: m.cau, congThuc: m.congThuc, dungDe: m.dungDe });

/** Rút phần dạy được của MỘT bài: từ mới và mẫu câu. */
export function vonCuaBai(bai) {
  const k = bai?.knowledgeCore || {};
  const cau = k.mauCauDs?.length ? k.mauCauDs : (k.mauCau ? [k.mauCau] : []);
  return {
    id: bai?.id || null,
    ten: bai?.title || '',
    tu: (k.vocabulary || []).map(goiTu),
    cau: cau.map(goiCau),
  };
}

/**
 * Vốn từ cho một buổi luyện nói.
 *
 * @param baiNay   dữ liệu bài của unit đang mở
 * @param baiCu    [bài] các unit ĐỨNG TRƯỚC unit này, theo đúng thứ tự học
 * @param daDat    unit này bé đã đạt chưa
 * @param datCu    (id) => bé đã đạt unit ấy chưa
 */
export function vonTu({ baiNay, baiCu = [], daDat = false, datCu = () => false } = {}) {
  const loi = vonCuaBai(baiNay);
  if (!daDat) return { loi, on: [], moRong: false };

  /* Lấy các unit gần nhất TRƯỚC unit này mà bé đã đạt — gần thì còn nhớ, và cũng
     là thứ bé vừa học xong nên trộn vào là ôn đúng lúc. */
  const on = baiCu
    .filter((b) => datCu(b?.id))
    .slice(-UNIT_CU_TOI_DA)
    .map(vonCuaBai);

  return { loi, on, moRong: on.length > 0 };
}

/** Gộp thành một danh sách phẳng — chỗ nào cần "máy được dùng từ nào" thì hỏi đây. */
export const moiTuDuocDung = (v) =>
  [...v.loi.tu, ...v.on.flatMap((x) => x.tu)].map((t) => t.tu);

export const moiCauDuocDung = (v) =>
  [...v.loi.cau, ...v.on.flatMap((x) => x.cau)].map((c) => c.cau);

/* ─────────── lời dặn cho máy ─────────── */

/**
 * Dựng lời dặn (system prompt). Viết bằng tiếng Anh vì mô hình theo lệnh tiếng Anh
 * chắc tay hơn, nhưng NỘI DUNG bắt nó nói với bé bằng hai thứ tiếng.
 *
 * Bốn điều bắt buộc, và cả bốn đều có lý do đắt:
 *
 *  1. CHỈ dùng từ trong danh sách. Đây là cả lý do phòng này tồn tại.
 *  2. Mỗi lượt đúng MỘT câu tiếng Anh ngắn. Bé 6 tuổi không nhại lại được hai câu.
 *  3. Luôn kèm một lời tiếng Việt ngắn — bé chưa hiểu tiếng Anh thì cần người dịch,
 *     mà bố mẹ không phải lúc nào cũng ngồi cạnh.
 *  4. Trả về JSON, vì màn hình cần TÁCH câu tiếng Anh (để đọc giọng en-GB và để
 *     chấm phát âm) khỏi lời tiếng Việt (đọc giọng vi-VN). Trộn hai thứ tiếng vào
 *     một dòng là bộ đọc sai giọng — kho này đã chốt "mỗi dòng chỉ MỘT thứ tiếng".
 */
/**
 * LỜI LỚP HỌC — nhúm câu cô được nói ngoài vốn từ của bài.
 *
 * Phát hiện khi gọi Groq thật lượt đầu tiên: bé chào "Chào cô", cô đáp "I like
 * milk." Không phải máy sai — unit 5 chỉ có ĐÚNG MỘT mẫu câu, nên cô bị bó tới mức
 * không có gì để chào lại. Cứ thế thì mọi lượt đều là "I like ...", và cái đó
 * không phải trò chuyện.
 *
 * Nên mở đúng một khe hẹp: mấy câu nghi thức của lớp học. Chúng KHÔNG phải từ bé
 * phải học thuộc — chúng là lời của CÔ, bé nghe mãi rồi hiểu qua ngữ cảnh, đúng như
 * trong lớp thật. Danh sách CỐ ĐỊNH và ngắn, khai ở đây để nhìn thấy được và để
 * cổng đếm; nới nó ra là quay lại đúng chỗ hỏng mà việc bó vốn từ sinh ra để tránh.
 */
export const LOI_LOP_HOC = [
  'Hello!', 'Hi!', 'Goodbye!', 'Your turn.', 'Say it with me.',
  'Listen.', 'Again, please.', 'Good job!', 'Well done!', 'Nice!',
  'Almost!', 'Try again.', 'Yes!', 'No.',
];

/* ─────────── việc của từng lượt ─────────── */

/**
 * VIỆC CỦA LƯỢT NÀY — do MÁY CON quyết, không phó mặc cho mô hình.
 *
 * Bác bắt 13-08: "nó cứ nói đi nói lại hello với mấy câu nhàm chán". Dựng lại thì
 * còn tệ hơn: sáu lượt liền cô nói đúng một câu `Hi, I'm Bill.`
 *
 * Lỗi ở LỜI DẶN, không ở mô hình. Bản trước viết "chỉ được dùng những MẪU CÂU
 * sau" rồi đưa đúng một câu ví dụ. Unit 1 có một mẫu — nên nó không còn gì khác
 * để nói, và nó đang tuân lệnh răm rắp. Thả cho mô hình "tự nói cho phong phú"
 * cũng không xong: hoặc nó lặp, hoặc nó bịa ra từ ngoài vốn của bé.
 *
 * Nên đảo lại: máy con CHỌN SẴN từ mục tiêu và kiểu việc cho từng lượt, mô hình
 * chỉ lo diễn đạt. Biến "cho phong phú" — thứ không kiểm được — thành một phép
 * đếm chạy được bằng `node` và soi được bằng cổng.
 */
export const KIEU_VIEC = {
  tu: 'tu',        // cô nói một TỪ, bé nhắc lại
  mau: 'mau',      // cô nói CẢ CÂU theo công thức, bé nhắc lại
  thay: 'thay',    // cô thay từ khác vào công thức — chỗ bé thấy mẫu câu "sống"
  khen: 'khen',    // bé vừa nói đúng: khen rồi sang việc mới
};

/**
 * Đếm xem từ nào bé đã được luyện trong buổi này, rồi chọn từ ÍT gặp nhất.
 *
 * Cố tình không dùng ngẫu nhiên: chạy hai lần ra hai kiểu thì không cổng nào canh
 * được, mà đây đúng là chỗ vừa hỏng.
 */
export function viecTiepTheo({ von, lichSu = [], haDoKho = false, hoSo = null } = {}) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  if (!tu.length) return null;

  const cuaCo = lichSu.filter((x) => x.vai === 'may');
  const dem = new Map(tu.map((t) => [t.tu, 0]));
  for (const l of cuaCo) {
    for (const t of tu) {
      if (new RegExp(`\\b${t.tu}\\b`, 'i').test(l.en || '')) dem.set(t.tu, dem.get(t.tu) + 1);
    }
  }
  /* Từ ít được nhắc nhất; hoà thì lấy từ đứng trước trong bài — cùng thứ tự bé đã
     học ở chặng Từ mới, nên nghe quen tai. */
  const dich = tu.reduce((a, b) => (dem.get(b.tu) < dem.get(a.tu) ? b : a), tu[0]);

  /* Xoay vòng ba kiểu việc theo SỐ LƯỢT, để không lượt nào giống lượt trước. Có
     mẫu câu thì mới xoay tới hai kiểu câu; bài chưa có mẫu thì chỉ luyện từ. */
  /* Bé đang đuối thì lùi về việc dễ nhất: chỉ nói TỪ. Không đuổi bé ra khỏi phòng
     — xem `tinhBuoi`. */
  const vong = (haDoKho || !cau.length)
    ? [KIEU_VIEC.tu]
    : [KIEU_VIEC.tu, KIEU_VIEC.mau, KIEU_VIEC.thay];
  const kieu = vong[cuaCo.length % vong.length];
  const mau = cau.length ? cau[cuaCo.length % cau.length] : null;

  /* Ô trống của công thức ưu tiên điền THỨ BÉ THÍCH, nếu bé đã chọn và từ ấy nằm
     trong vốn từ. "I like fish." khi bé thật sự thích cá thì bé nói ra một câu về
     CHÍNH MÌNH — khác hẳn nhại một câu về sữa của người khác. */
  const thich = hoSo?.thich && tu.find((t) => t.tu === hoSo.thich);
  return {
    tu: (kieu === KIEU_VIEC.thay && thich) ? thich : dich,
    kieu, mau, daNhac: dem.get(dich.tu), theoSoThich: !!(kieu === KIEU_VIEC.thay && thich),
  };
}

/**
 * Ô TRỐNG CỦA CÔNG THỨC nhận loại gì.
 *
 * Đã hỏng thật khi thử với Groq: công thức `Bye, + [Name].` mà lời dặn bảo "nhét
 * một từ được phép vào ô trống", nên mô hình sinh ra **"Bye, book."** — vô nghĩa,
 * và tệ hơn là dạy bé một câu sai. Ô trống có LOẠI: chỗ của tên người thì phải là
 * tên người, chỗ của danh từ mới nhận từ vựng của bài.
 */
export function loaiOTrong(congThuc) {
  const m = String(congThuc || '').match(/\[([^\]]+)\]/);
  if (!m) return null;
  return /name|tên/i.test(m[1]) ? 'ten' : 'tu';
}

/** Lời dặn riêng cho lượt này, ghép vào cuối lời dặn chung. */
function dongViec(v, tenBe) {
  if (!v) return '';
  const { tu, kieu, mau } = v;
  if (kieu === KIEU_VIEC.tu) {
    return `THIS TURN: say just the word "${tu.tu}" (means "${tu.nghia}") for the child to repeat.`;
  }
  if (kieu === KIEU_VIEC.mau && mau) {
    /* ĐÚNG NGUYÊN VĂN. Để nó tự thay tên ở lượt này thì lượt `mau` và lượt `thay`
       ra cùng một câu — đã thấy thật: hai lượt liền đều "Hi, I'm Bo." */
    return `THIS TURN: say exactly this sentence, word for word: "${mau.cau}"`
      + ' — do not substitute anything.';
  }
  if (kieu === KIEU_VIEC.thay && mau) {
    const khung = mau.congThuc || mau.cau;
    const loai = loaiOTrong(mau.congThuc);
    /* Ô tên người thì CHỈ nhận tên. Nhét `book` vào là ra "Bye, book." */
    const dien = loai === 'ten'
      ? `put the child's name ${tenBe} in the slot (a NAME goes there — never a thing)`
      : `put the word "${tu.tu}" in the slot`;
    return `THIS TURN: take the pattern ${khung} and ${dien}.`
      + ' Do not repeat the example sentence word for word.';
  }
  return '';
}

export function loiDan({ von, tenBe = 'bạn nhỏ', lop = 1, viec = null, hoSo = null }) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  const bangTu = tu.map((t) => `${t.tu} (${t.nghia})`).join(', ');
  const bangCau = cau.map((c) => `"${c.cau}"${c.congThuc ? ` [${c.congThuc}]` : ''}`).join('; ');

  /* Câu ví dụ ĐI KÈM công thức, và công thức mới là thứ đáng học: mẫu câu là cái
     KHUNG bé thay từ vào, không phải một câu để đọc thuộc. Bản trước chỉ liệt kê
     câu ví dụ, nên mô hình nói đúng câu ấy sáu lượt liền — nó không sai, nó không
     có gì khác để nói. */
  const bangKhung = cau
    .map((c) => `${c.congThuc || c.cau} (ví dụ: "${c.cau}")`)
    .join('; ');

  return [
    `You are a warm, patient English tutor for a ${lop === 1 ? 'six-year-old' : `grade ${lop}`} Vietnamese child named ${tenBe}.`,
    '',
    'HARD RULES — breaking any of these makes the lesson useless:',
    `1. Use ONLY these English words: ${bangTu}.`,
    '   Plus the bare function words needed to fill the patterns below.',
    '   Never introduce an English word outside this list, not even an easy one.',
    `2. Sentence patterns you may build: ${bangKhung || bangCau}.`,
    '   A pattern is a FRAME: put the allowed words (or the child\'s name) in the slot.',
    '   The example is one filling of it, not the only thing you may say.',
    `   You may also use these fixed classroom phrases: ${LOI_LOP_HOC.join(' ')}`,
    '   Those phrases are yours to say — they are not words the child must produce.',
    '3. Say exactly ONE short English sentence per turn. Never two.',
    '4. NEVER say the same English sentence you said in your previous turn.',
    '   Vary the word in the slot. Repeating yourself is the worst thing you can do here.',
    '5. Do not greet more than once in a conversation. Greet only on your first turn.',
    '6. Always add ONE short Vietnamese line explaining what you just said and what',
    '   the child should do. Write it for a six-year-old, not for an adult.',
    '7. If the child says something off-topic, gently steer back to the words above.',
    '   Never discuss anything other than practising these words.',
    '8. If the child repeated correctly, put the praise in the VIETNAMESE line and',
    '   still do this turn\'s task in English — praise is not a turn of its own.',
    '',
    dongViec(viec, tenBe),
    dongHoSo(hoSo, tenBe),
    '',
    'Reply as JSON only: {"en": "<the English sentence>", "vi": "<the Vietnamese line>"}',
  ].filter((x) => x !== null).join('\n');
}

/* ─────────── ngữ cảnh ─────────── */

/**
 * Cắt lịch sử trước khi gửi. Giữ lượt MỚI NHẤT, bỏ lượt cũ.
 *
 * Cắt ở client chứ không ở server, vì server không giữ gì cả — nó nhận sao gửi vậy.
 * Nếu quên cắt thì không có gì báo: câu trả lời vẫn đúng, chỉ có hoá đơn dài ra.
 */
export function catNguCanh(ds = [], toiDa = LUOT_GUI_TOI_DA) {
  const sach = ds.filter((x) => x && (x.vai === 'may' || x.vai === 'be') && x.chu);
  return sach.slice(-toiDa);
}

/** Dạng gửi lên máy chủ — chỉ vai và chữ, không kèm điểm hay dấu thời gian. */
export const goiGui = (ds) => catNguCanh(ds).map((x) => ({
  role: x.vai === 'may' ? 'assistant' : 'user',
  content: String(x.chu).slice(0, CHU_TOI_DA),
}));

/* ─────────── hình cho từ đang nói tới ─────────── */

/**
 * Máy vừa nói câu này thì màn hình phải vẽ HÌNH của những từ trong đó.
 *
 * Bác dặn 13-08: "bổ sung thêm hình ảnh với các từ khi học về hình, lấy trong dữ
 * liệu chúng ta". Đúng chỗ cần: bé lớp 1 chưa đọc được `chicken`, nhưng nhìn 🍗 là
 * hiểu ngay. Không có hình thì phòng này quay về thành một khối chữ — mà cả quyển
 * dựng trên nguyên tắc không bắt bé đọc chữ.
 *
 * So theo TỪNG TIẾNG, không phải `includes`: `includes('can')` sẽ khớp cả trong
 * "I can see". Dấu câu bị bóc trước khi so, vì "chips." không bao giờ khớp "chips".
 *
 * ── MỘT CHỮ, HAI NGHĨA ──
 * Nhưng so theo tiếng vẫn chưa đủ: `can` là CÙNG MỘT CHỮ cho "cái lon" (unit 3) và
 * "có thể" (unit 14). Vẽ hình cái lon lúc máy nói "I can see" thì bé học ngược hẳn
 * nghĩa — tệ hơn là không vẽ gì.
 *
 * Luật vị trí, nhỏ mà đủ: chỗ NGAY SAU một đại từ làm chủ ngữ là chỗ của ĐỘNG TỪ,
 * không phải của danh từ. "I can see" → bỏ; "A can, please" → giữ. Không phải phép
 * phân tích ngữ pháp, chỉ là một chốt chặn đúng chỗ hay va nhất ở vốn từ lớp 1.
 *
 * Hình lấy qua `hinhCuaTu` ở `lib/noiDung.js` — cùng nguồn với thẻ từ và thanh
 * việc. Đừng đọc lại `bai.hinhTu` ở đây.
 */
const CHU_NGU = new Set(['i', 'you', 'we', 'they', 'he', 'she', 'it']);

export function tuTrongCau(cau, von) {
  const tieng = String(cau || '').toLowerCase().split(/[^a-z']+/).filter(Boolean);
  const co = new Set(tieng);
  const sauChuNgu = new Set(
    tieng.filter((_, i) => i > 0 && CHU_NGU.has(tieng[i - 1])),
  );
  const moi = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const thay = [];
  for (const t of moi) {
    if (thay.some((x) => x.tu === t.tu)) continue;
    /* Từ nhiều tiếng ("ice cream") thì đòi có ĐỦ các tiếng của nó. */
    const phan = t.tu.toLowerCase().split(/\s+/).filter(Boolean);
    if (!phan.length || !phan.every((p) => co.has(p))) continue;
    /* Từ một tiếng mà đứng ngay sau chủ ngữ thì đang làm động từ — đừng vẽ. */
    if (phan.length === 1 && sauChuNgu.has(phan[0])) continue;
    thay.push(t);
  }
  return thay;
}

/**
 * Đọc câu trả lời của máy. Mô hình được dặn trả JSON, nhưng KHÔNG được tin là nó
 * luôn làm đúng — trả về chữ trần thì vẫn phải dùng được, đừng để màn trắng.
 */
export function docTraLoi(chu) {
  const s = String(chu || '').trim();
  const json = s.match(/\{[\s\S]*\}/);
  if (json) {
    try {
      const o = JSON.parse(json[0]);
      if (o && (o.en || o.vi)) {
        return { en: String(o.en || '').trim(), vi: String(o.vi || '').trim(), thoJSON: false };
      }
    } catch { /* rơi xuống dưới */ }
  }
  /* Không phải JSON: đoán dòng nào là tiếng Anh bằng dấu tiếng Việt. Đoán sai thì
     bé nghe sai giọng một câu — vẫn hơn là không hiện gì. */
  const dong = s.split('\n').map((x) => x.trim()).filter(Boolean);
  const coDauViet = (x) => /[àáảãạăâèéẻẽẹêìíỉĩịòóỏõọôơùúủũụưỳýỷỹỵđ]/i.test(x);
  return {
    en: dong.find((x) => !coDauViet(x)) || '',
    vi: dong.find(coDauViet) || '',
    thoJSON: true,
  };
}

/* ─────────── soi lại câu cô nói ─────────── */

/**
 * CÂU CÔ NÓI CÓ DÙNG ĐƯỢC KHÔNG.
 *
 * Dặn dò là chưa đủ. Thử thật với Groq: đã bảo rõ ô trống của `Bye, + [Name].` là
 * chỗ của TÊN NGƯỜI, nó vẫn sinh ra **"Bye, bike."** Với người lớn thì đó là một
 * câu buồn cười; với bé 6 tuổi đang tập nhại thì đó là dạy sai, và bé sẽ nhớ.
 *
 * Nên đảo từ TIN sang SOI: máy con tự kiểm câu cô nói, không hợp lệ thì thay bằng
 * câu do chính máy con dựng. Mô hình vẫn có ích ở chỗ nó hiểu bé vừa nói gì và
 * viết được lời tiếng Việt; nhưng câu tiếng Anh — thứ bé sẽ nhại — thì không thả.
 *
 * Hợp lệ khi câu ấy là MỘT trong:
 *   · một từ trong vốn từ                     ("ball")
 *   · một câu nghi thức của lớp               ("Good job!")
 *   · một câu ví dụ của bài                   ("Hi, I'm Bill.")
 *   · một công thức đã điền đúng LOẠI ô trống ("Hi, I'm Bo." · "I like fish.")
 */
const gonCau = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9' ]/g, '').replace(/\s+/g, ' ').trim();

export function cauHopLe(en, { von, tenBe = '', cauTruoc = '' } = {}) {
  const c = gonCau(en);
  if (!c) return false;
  /* Lặp Y HỆT lượt trước thì dù đúng ngữ pháp vẫn hỏng — đó chính là cái bác bắt:
     "nó cứ nói đi nói lại". Đã thấy thật hai lượt liền cùng ra "Hi, I'm Bo." */
  if (cauTruoc && gonCau(cauTruoc) === c) return false;

  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];

  if (tu.some((t) => gonCau(t.tu) === c)) return true;
  if (LOI_LOP_HOC.some((x) => gonCau(x) === c)) return true;
  if (cau.some((x) => gonCau(x.cau) === c)) return true;

  /* Công thức đã điền: dựng mọi cách điền HỢP LỆ rồi so. Số cách rất nhỏ (số mẫu
     câu × số từ), nên cứ dựng hết còn hơn đoán bằng biểu thức chính quy. */
  for (const x of cau) {
    if (!x.congThuc) continue;
    const loai = loaiOTrong(x.congThuc);
    const dienDuoc = loai === 'ten' ? [tenBe, 'Bill', 'Mai'] : tu.map((t) => t.tu);
    for (const d of dienDuoc) {
      if (!d) continue;
      const thu = x.congThuc.replace(/\s*\+\s*/g, ' ').replace(/\[[^\]]+\]/, d);
      if (gonCau(thu) === c) return true;
    }
  }
  return false;
}

/**
 * Câu dựng sẵn cho việc của lượt này — dùng khi câu của cô không qua được phép soi.
 * Luôn đúng, vì nó ghép từ chính dữ liệu bài chứ không sinh ra từ đâu cả.
 */
export function cauThayThe(viec, tenBe = 'con', cauTruoc = '') {
  if (!viec) return null;
  const { tu, kieu, mau } = viec;

  const dienVao = (m, d) => (m.congThuc
    ? m.congThuc.replace(/\s*\+\s*/g, ' ').replace(/\[[^\]]+\]/, d)
    : m.cau);

  /* Xếp sẵn mấy phương án, rồi lấy phương án ĐẦU TIÊN khác câu lượt trước.
     Bản đầu chỉ dựng đúng một câu — mà nếu chính nó trùng câu trước thì luật chống
     lặp thành vô nghĩa: chặn lặp xong lại thay bằng đúng câu vừa chặn. Đã thấy
     thật trên bản chạy: hai lượt liền cùng ra "Hi, I'm Bo." */
  const chon = [];
  if (kieu === KIEU_VIEC.tu || !mau) {
    chon.push({ en: tu.tu, vi: `Con nghe rồi nói lại từ “${tu.tu}” nhé — nghĩa là ${tu.nghia}.` });
  } else if (kieu === KIEU_VIEC.mau) {
    chon.push({ en: mau.cau, vi: 'Con nghe rồi nói lại cả câu này nhé.' });
  } else {
    const loai = loaiOTrong(mau.congThuc);
    const dien = loai === 'ten' ? tenBe : tu.tu;
    chon.push({ en: dienVao(mau, dien), vi: `Cùng một mẫu câu, nay thay bằng “${dien}”. Con nói lại nhé.` });
  }
  /* Đường lui luôn có: chính TỪ mục tiêu, và câu ví dụ. Một trong hai bao giờ cũng
     khác câu lượt trước, vì một cái là từ rời còn một cái là cả câu. */
  chon.push({ en: tu.tu, vi: `Con nghe rồi nói lại từ “${tu.tu}” nhé — nghĩa là ${tu.nghia}.` });
  if (mau) chon.push({ en: mau.cau, vi: 'Con nghe rồi nói lại cả câu này nhé.' });

  const gon = (x) => String(x || '').toLowerCase().replace(/[^a-z0-9' ]/g, '').trim();
  return chon.find((c) => gon(c.en) !== gon(cauTruoc)) || chon[0];
}

/* ─────────── tách một dòng lẫn hai thứ tiếng ─────────── */

/**
 * TÁCH LỜI GIẢI THÍCH THEO THỨ TIẾNG.
 *
 * Bác bắt 13-08: "phần giải thích khi có từ tiếng Anh phát bằng tiếng Việt rất
 * không okay." Đúng, và tệ ở chỗ kho này đã chốt luật ấy từ hồi làm dây chuyền âm
 * — "mỗi dòng chỉ MỘT thứ tiếng" — rồi chính chỗ này vi phạm:
 *
 *     Con nói lại từ "ball" nhé, nghĩa là quả bóng.
 *        → đọc cả dòng bằng vi-VN, và "ball" phát ra thành tiếng Việt
 *
 * Bé đang tập nhại mà nghe từ tiếng Anh đọc giọng Việt thì học sai đúng chỗ mình
 * đang dạy. Cấm mô hình nhắc lại từ tiếng Anh cũng không xong: nhắc lại là việc
 * TỐT ("con nói lại từ ball nhé"), chỉ có đọc sai giọng mới hỏng.
 *
 * ── VÌ SAO KHÔNG ĐOÁN NGÔN NGỮ ──
 * Không cần bộ đoán tiếng nào cả: mình BIẾT TRƯỚC bé đang học những từ nào. Chỉ
 * tách đúng những chuỗi nằm trong vốn từ và câu mẫu của bài — phép xác định, chạy
 * được bằng `node`, và không bao giờ nhận nhầm một chữ tiếng Việt thành tiếng Anh.
 *
 * Tên bé (Bo, Minh An…) CỐ Ý không tách: đó là tên Việt, đọc giọng Việt mới đúng.
 */
export function tachTheoTieng(chu, von) {
  const s = String(chu || '');
  if (!s.trim() || !von) return [];

  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)].map((t) => t.tu);
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)].map((c) => c.cau);
  /* Câu TRƯỚC từ, và trong mỗi nhóm thì dài trước: "I like milk." phải khớp trọn
     câu, đừng để nó bị xé thành "milk" rời rồi đọc lệch nhịp. */
  const moc = [...cau, ...tu, ...LOI_LOP_HOC].filter(Boolean)
    .sort((a, b) => b.length - a.length);
  if (!moc.length) return [{ chu: s, tieng: 'vi' }];

  const thoat = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  /* Ranh giới từ hai đầu — nếu không, "can" khớp cả trong "cần", và "book" khớp
     trong "bookmark". Dấu câu cuối câu mẫu đã nằm trong chính chuỗi mốc. */
  const re = new RegExp(`(?<![\\p{L}])(${moc.map(thoat).join('|')})(?![\\p{L}])`, 'giu');

  const ra = [];
  let i = 0;
  for (const m of s.matchAll(re)) {
    if (m.index > i) ra.push({ chu: s.slice(i, m.index), tieng: 'vi' });
    ra.push({ chu: m[0], tieng: 'en' });
    i = m.index + m[0].length;
  }
  if (i < s.length) ra.push({ chu: s.slice(i), tieng: 'vi' });

  /* Bỏ mẩu chỉ còn dấu câu hoặc khoảng trắng — đọc lên nghe như bị nấc. */
  return ra.filter((x) => /[\p{L}\p{N}]/u.test(x.chu)).map((x) => ({ ...x, chu: x.chu.trim() }));
}

/* ─────────── một buổi có mở có kết ─────────── */

/**
 * BUỔI LUYỆN NÓI PHẢI CÓ CHỖ KẾT.
 *
 * Bác dặn 13-08: cô phải chủ động kết thúc khi bé đã nắm bài (khen rồi dừng), hạ
 * độ khó khi bé đuối, và mỗi phiên tối đa 20 phút.
 *
 * Bản trước không có chỗ kết nào: cô hỏi mãi, bé trả lời mãi. Với bé 6 tuổi thì
 * một việc không có vạch đích là một việc không bao giờ thấy mình làm được — mà
 * "thấy mình làm được" mới là thứ giữ bé quay lại.
 *
 * Ba đường kết, và cả ba đều do MÁY CON quyết chứ không hỏi mô hình:
 *
 *   xongGioi   bé đạt liên tiếp đủ số lượt   → khen thật, rồi dừng
 *   hetGio     quá 20 phút                    → dừng tử tế, hẹn lần sau
 *   haDoKho    bé đuối liên tiếp              → KHÔNG dừng, mà hạ xuống chỉ luyện TỪ
 *
 * `haDoKho` cố ý không phải một đường KẾT: bé đang đuối mà bị đuổi ra khỏi phòng
 * thì thông điệp bé nhận được là "con dốt quá". Hạ độ khó rồi cho làm tiếp mới
 * đúng — cùng tinh thần với luật "thử thật 2 lần" ở `dandat.js`.
 */
export const PHUT_TOI_DA = 20;
export const DAT_LIEN_DE_XONG = 3;
export const KEM_LIEN_DE_HA = 3;

/**
 * @param lichSu  các lượt, lượt của bé có `diem` (null nếu không chấm được)
 * @param batDau  mốc thời gian mở phòng (ms)
 * @param bayGio  ms — tiêm vào để cổng chạy được mà không phụ thuộc đồng hồ thật
 */
export function tinhBuoi({ lichSu = [], batDau = null, bayGio = null, datNguong = 6 } = {}) {
  const cuaBe = lichSu.filter((x) => x.vai === 'be' && x.diem != null);
  /* `batDau == null` mới là "chưa bấm giờ". Viết `batDau ? … : 0` thì mốc 0 — một
     con số hợp lệ — bị coi là chưa bắt đầu, và đồng hồ không bao giờ chạy. Cùng họ
     với lỗi `Date.parse(0)` ra năm 2000 đã ghi trong sổ. */
  const coGio = batDau != null && bayGio != null;
  const phut = coGio ? Math.max(0, (bayGio - batDau) / 60000) : 0;

  /* Đếm chuỗi ĐUÔI: chỉ tính mấy lượt gần đây nhất, không tính cả buổi. Bé vào
     phòng lúc còn lóng ngóng rồi khá dần lên là chuyện thường — lấy cả buổi ra
     tính thì mãi mãi không đạt. */
  let datLien = 0;
  let kemLien = 0;
  for (let i = cuaBe.length - 1; i >= 0; i -= 1) {
    if (cuaBe[i].diem >= datNguong) { if (kemLien) break; datLien += 1; } else { if (datLien) break; kemLien += 1; }
  }

  const hetGio = phut >= PHUT_TOI_DA;
  const xongGioi = datLien >= DAT_LIEN_DE_XONG;
  return {
    trangThai: xongGioi ? 'xongGioi' : hetGio ? 'hetGio' : 'dang',
    haDoKho: !xongGioi && kemLien >= KEM_LIEN_DE_HA,
    datLien,
    kemLien,
    phut,
    phutConLai: Math.max(0, PHUT_TOI_DA - phut),
    soLuotBe: cuaBe.length,
    soDat: cuaBe.filter((x) => x.diem >= datNguong).length,
  };
}

/** Lời kết — nói thẳng bé làm được gì, không phải một câu khen chung chung. */
export function loiKet(buoi) {
  if (!buoi) return null;
  if (buoi.trangThai === 'xongGioi') {
    return {
      bieuTuong: '🎉',
      tieuDe: 'Con nói được rồi!',
      chu: `Con nói đúng ${buoi.datLien} câu liền. Hôm nay thế là giỏi lắm — mai mình nói tiếp nhé.`,
    };
  }
  if (buoi.trangThai === 'hetGio') {
    return {
      bieuTuong: '⏰',
      tieuDe: 'Hết giờ nói chuyện rồi',
      chu: `Con đã nói ${buoi.soLuotBe} lượt, đúng ${buoi.soDat} lượt. Nghỉ mắt một lát rồi mai mình nói tiếp nhé.`,
    };
  }
  return null;
}

/* ─────────── hồ sơ của chính bé ─────────── */

/**
 * DÙNG THÔNG TIN CỦA CHÍNH BÉ, KHÔNG PHẢI CÂU TĨNH.
 *
 * Bác dặn 13-08: "cần có kịch bản hỏi thông tin cá nhân của học sinh để khi nói
 * chuyện sẽ dùng thông tin ấy để luyện, thay vì các thông tin tĩnh."
 *
 * Bé nói "I like milk." trong khi bé ghét sữa thì đó là nhại một câu của người
 * khác. Nói "I like fish." vì bé thật sự thích cá thì bé đang NÓI VỀ MÌNH — cùng
 * một mẫu câu, nhưng một bên là học vẹt còn một bên là dùng tiếng Anh.
 *
 * ── HỎI THẾ NÀO, VÀ VÌ SAO KHÔNG ĐỂ MÔ HÌNH HỎI ──
 * Chính APP hỏi, bằng tiếng Việt, và bé trả lời bằng cách BẤM VÀO HÌNH — không gõ,
 * không nói tự do. Ba lý do:
 *
 *   · bé 6 tuổi không gõ được, mà nói tự do thì bộ nhận dạng nghe ra gì cũng được;
 *   · câu trả lời rơi đúng vào vốn từ của bài, nên không rò từ lạ vào phòng;
 *   · KHÔNG có thông tin riêng tư nào mới rời khỏi máy — chỉ là một từ trong sách,
 *     đúng thứ bé vừa học. Tên và lớp thì app đã có sẵn từ hồ sơ.
 *
 * Cố ý KHÔNG hỏi tuổi, trường, nhà ở đâu, hay bất cứ thứ gì nhận dạng được bé.
 */
export function cauHoiSoThich(von) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  if (tu.length < 2) return null;
  return {
    hoi: 'Con thích cái nào nhất?',
    chon: tu,
  };
}

/** Lời dặn thêm về bé — chỉ những gì app đã có, không hỏi thêm gì. */
function dongHoSo(hoSo, tenBe) {
  if (!hoSo) return '';
  const d = [];
  if (tenBe) d.push(`The child's name is ${tenBe} — use it in [Name] slots.`);
  if (hoSo.thich) {
    d.push(`The child told you they like "${hoSo.thich}".`
      + ' Prefer that word when a pattern needs a thing — it makes the sentence about them.');
  }
  return d.length ? `ABOUT THE CHILD: ${d.join(' ')}` : '';
}
