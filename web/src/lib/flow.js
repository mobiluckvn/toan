/**
 * LÕI LOGIC BÀI HỌC — JS thuần, không phụ thuộc React.
 * Tách riêng để chạy test được bằng node (xem test/flow.test.mjs).
 */

/* ─────────── Số kiểu Việt Nam ─────────── */
export function parseNum(s) {
  if (s === null || s === undefined) return NaN;
  if (typeof s === 'number') return s;
  const t = String(s).trim().replace(/\s|\u00A0/g, '').replace(',', '.');
  return t === '' ? NaN : Number(t);
}

export function fmtNum(v) {
  return String(v).replace('.', ',');
}

export const EPS = 0.005;
export const nearEq = (a, b, eps = EPS) =>
  Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) < eps;

/* ─────────── Chấm một câu hỏi ─────────── */
/**
 * Gộp các dấu toán mà bàn phím thường KHÔNG có về dạng con gõ được.
 * Dữ liệu bài dùng − (U+2212), × , ÷ ; con gõ - , x , : — cùng nghĩa, phải chấm như nhau.
 */
const foldSigns = (s) => String(s ?? '')
  .replace(/[−–—]/g, '-')
  .replace(/[×✕✖]/g, 'x')
  .replace(/÷/g, ':');

/** Chuẩn hoá chuỗi để so khớp: bỏ hoa/thường, gộp khoảng trắng, bỏ dấu chấm cuối */
export function normText(s) {
  return foldSigns(s)
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[.;]+$/, '')
    .trim();
}

/* ─────────── Đọc số: thập phân kiểu Việt HOẶC phân số ─────────── */
const FRACTION = /^\s*([+-]?\d+)\s*\/\s*(\d+)\s*$/;

/** "0,75" → 0,75 · "3/4" → 0,75 · không đọc được → NaN */
export function toNumber(v) {
  if (typeof v === 'number') return v;
  const m = String(v ?? '').match(FRACTION);
  if (m) return Number(m[2]) === 0 ? NaN : Number(m[1]) / Number(m[2]);
  return parseNum(v);
}

/* ─────────── Phần giải thích trong ngoặc ─────────── */
/**
 * Nhiều đáp án viết kiểu "lời đáp (vì sao)": "bằng nhau (0 đuôi bỏ được)".
 * Phần trong ngoặc là LÝ DO, không phải đáp án — tách ra để chấm cái lõi,
 * còn lý do thì hiện lên sau khi con trả lời.
 */
export function splitAside(v) {
  const m = typeof v === 'string' && v.match(/^\s*(.+?)\s*\(([^()]+)\)\s*$/);
  return m && m[1].trim() ? { core: m[1].trim(), aside: m[2].trim() } : { core: v, aside: '' };
}

/**
 * Cùng ý đó nhưng viết bằng gạch ngang: "có — 11 × 8", "ĐÚNG — năng suất biết cộng".
 * Phần sau gạch là LÝ DO. Tách ra thì cái con phải gõ chỉ còn "có", "ĐÚNG" — gõ được;
 * để nguyên cả câu thì dài quá 26 ký tự, bị xếp nhầm vào loại "tự đối chiếu" và con
 * MẤT LUÔN ô nhập. Đây là chỗ 46 đáp án đang mắc.
 */
export function answerCore(v) {
  const inParen = splitAside(v).core;
  if (typeof inParen !== 'string') return inParen;
  const m = inParen.match(/^\s*(.+?)\s+[—–]\s+(.+)$/);
  if (!m || !m[1].trim()) return inParen;
  // Chỉ tách khi phần đầu là một LỜI PHÁN ("có", "ĐÚNG", "gấp đôi", "không số nào").
  // Nếu phần đầu là SỐ thì gạch ngang đang nối ý, không phải mở lời giải thích:
  // "12 tháng — 13 bạn: 13 chim chui 12 chuồng" cả câu mới là đáp, không phải "12 tháng".
  return numAndTail(m[1].trim()) ? inParen : m[1].trim();
}

/* ─────────── Đáp án là một phép so sánh ─────────── */
/** "7/8 < 9/10" → {a:'7/8', op:'<', b:'9/10'} · có thêm lời văn → null */
export function parseCompare(v) {
  const m = normText(v).match(/^([^<>=]+?)\s*([<>=])\s*([^<>=]+)$/);
  if (!m) return null;
  const a = m[1].trim(), b = m[3].trim();
  return a && b && !/[—:;]/.test(a + b) ? { a, op: m[2], b } : null;
}
const FLIP = { '<': '>', '>': '<', '=': '=' };

/* ─────────── Số kèm đơn vị ─────────── */
/**
 * Đơn vị ĐO thuần tuý — bỏ đi không đổi nghĩa đáp số, nên chấm thì lờ đi.
 * Cố tình KHÔNG gồm các từ chỉ chiều/hướng ("trước", "nữa", "tăng", "giảm")
 * vì bỏ chúng là đổi hẳn đáp án.
 */
const MEASURE = /^(%|phần trăm|đ|đồng|nghìn|nghìn đồng|triệu|km\/h|m\/phút|m\/giây|mm|cm|dm|km|cm2|cm²|m2|m²|dm2|dm²|km2|km²|cm3|cm³|m3|m³|m|kg|g|tấn|tạ|yến|lít|ml|l|giờ|phút|giây|ngày|tuần|tháng|tuổi|lần|phần|đơn vị|viên|quyển|cuốn|cái|chiếc|con|quả|cây|bông|hộp|túi|người|bạn|em|học sinh|điểm|câu|số)$/;

/**
 * Tách "số + phần chữ đi kèm".
 * "60 000 đồng" → {n: 60000, tail: ''}   (đồng là đơn vị đo → bỏ)
 * "2 năm trước" → {n: 2, tail: 'năm trước'}  (giữ lại vì đổi nghĩa)
 * "31; 33; 35"  → null  (còn chữ số phía sau → là danh sách, không phải số + đơn vị)
 */
function numAndTail(v) {
  if (typeof v === 'number') return Number.isFinite(v) ? { n: v, tail: '' } : null;
  const m = normText(v).match(/^([+-]?[\d.,\s ]*\d)\s*(.*)$/);
  if (!m) return null;
  const tail = m[2].trim();
  if (/\d/.test(tail)) return null;
  const n = parseNum(m[1]);
  if (!Number.isFinite(n)) return null;
  return { n, tail: MEASURE.test(tail) ? '' : tail };
}

/* ─────────── Đáp án dạng danh sách nhiều số ─────────── */
/**
 * Nhặt từng số trong câu trả lời, thay vì cắt theo dấu ngăn cách — nhờ vậy con
 * viết "12; 24" hay "12, 24" hay "12 và 24" đều nhận, mà dấu phẩy THẬP PHÂN
 * trong "0,85" không bị tưởng nhầm là dấu ngăn cách.
 */
const NUM_TOKEN = /[+-]?\d+(?:[.,]\d+)?(?:\s*\/\s*\d+)?/g;
export function parseList(input) {
  return String(input ?? '').match(NUM_TOKEN) || [];
}

/** answerKey {values, ordered} — thiếu/thừa một số là sai, nhưng dấu ngăn cách thì tuỳ con */
export function matchList(key, input) {
  const got = parseList(input).map(toNumber);
  const want = (key.values || []).map(toNumber);
  if (want.length === 0 || got.length !== want.length) return false;
  if (got.some((n) => !Number.isFinite(n))) return false;
  if (key.ordered) return want.every((w, i) => nearEq(w, got[i]));
  const pool = [...got];
  return want.every((w) => {
    const k = pool.findIndex((g) => nearEq(w, g));
    if (k < 0) return false;
    pool.splice(k, 1);
    return true;
  });
}

/**
 * Đáp án dạng chữ dài (giải thích) thì KHÔNG chấm máy — để con tự đối chiếu.
 * Đo trên phần LÕI, bỏ lý do trong ngoặc: "KHÁC nhau (0 giữa giữ chỗ hàng phần mười)"
 * lõi chỉ là "khác nhau" — chấm được, nên con có ô để trả lời thay vì mất hẳn câu.
 */
/** Lõi đáp án chỉ gồm số và dấu ngăn cách, từ 2 số trở lên: "29, 38, 47, 56" */
const NUM_ONLY = /^[\d\s.,;/·và+-]+$/;
export function isNumberList(v) {
  const core = answerCore(v);
  return typeof core === 'string' && NUM_ONLY.test(normText(core)) && parseList(core).length >= 2;
}

/**
 * Dài quá thì coi là văn xuôi, con tự đối chiếu. NHƯNG một dãy số dài vẫn là dãy số —
 * máy chấm được. Trước đây "29, 38, 47, 56, 65, 74, 83, 92" bị tính là văn xuôi chỉ vì
 * 30 ký tự, con MẤT ô nhập dù đây đúng là câu "tìm tất cả các số".
 */
const SELFCHECK_LEN = 26;
export const isSelfCheck = (v) =>
  typeof v === 'string' && !isNumberList(v) && normText(answerCore(v)).length > SELFCHECK_LEN;

/**
 * Phần đáp án có sẵn BỘ CHỌN thì luôn chấm được — dù lời đáp dài bao nhiêu.
 * Con BẤM chứ không gõ, nên độ dài không còn là vấn đề. Nhờ vậy câu "… Vì sao?"
 * giữ được đủ hai ô: một ô đáp số, một ô chọn lý do.
 */
export const isPickable = (p) => Array.isArray(p?.options) && p.options.length >= 2;
export const gradableParts = (parts = []) => parts.filter((p) => isPickable(p) || !isSelfCheck(p.value));

/**
 * So một ô đáp án. Nới đúng ba chỗ trẻ hay vấp mà KHÔNG sai về toán:
 *   1. dấu −  ×  ÷  gõ thành  -  x  :          ("1 − 1/20"  ↔  "1 - 1/20")
 *   2. phân số ↔ thập phân                      ("3/4"       ↔  "0,75")
 *   3. đơn vị đo có gõ hay không cũng được      ("60 000 đồng" ↔ "60000" ↔ "60000 đ")
 * Vẫn BÁC khi phần chữ đi kèm đổi nghĩa: "2 năm nữa" không phải "2 năm trước".
 */
/**
 * Bỏ dấu phân nghìn kiểu Việt: khoảng trắng NẰM GIỮA HAI CHỮ SỐ.
 *
 * Sách viết "2 000 + 400 + 30 + 5", con gõ "2000 + 400 + 30 + 5" — cùng một đáp án,
 * mà so chuỗi thì lệch. Trước khi có phép nới này, bé lớp 3 gõ ĐÚNG vẫn bị báo sai
 * ở mọi câu tách số theo hàng; chấm sai một câu là bé mất tin vào cả phần mềm.
 *
 * Chỉ bỏ khi khoảng trắng kẹp GIỮA hai chữ số. Hai số khác nhau trong tiếng Việt
 * luôn có dấu ngăn (dấu ; dấu phẩy hay phép tính) chứ không bao giờ đứng cạnh nhau
 * bằng mỗi khoảng trắng, nên phép nới này không gộp nhầm hai số thành một.
 */
const boPhanNghin = (s) => String(s ?? '').replace(/(\d)[\s ](?=\d)/g, '$1');

function matchAtom(expected, input) {
  const a = normText(expected), b = normText(input);
  if (a === b) return true;
  if (boPhanNghin(a) === boPhanNghin(b)) return true;

  const na = toNumber(expected), nb = toNumber(input);   // "12" ↔ "12,0" ↔ "12/1"
  if (Number.isFinite(na) && Number.isFinite(nb)) return nearEq(na, nb);

  const ea = numAndTail(expected), eb = numAndTail(input);
  if (ea && eb && nearEq(ea.n, eb.n)) return eb.tail === '' || eb.tail === ea.tail;

  return false;
}

/**
 * So một ô có BỘ CHỌN. Con bấm đúng một nút, nên chỉ cần đối chiếu chữ trên nút —
 * KHÔNG dùng các phép nới của ô gõ tay.
 *
 * Nới lỏng ở đây là chấm sai người đúng lẫn chấm đúng người sai:
 *   · "8 - 24 - 24 - 8" (đỉnh-cạnh-mặt-lõi) và "8 - 24 - 8 - 24" cùng bộ số, khác
 *     thứ tự — nhánh "dãy số bỏ qua thứ tự" nhận cả hai, con bấm nhầm vẫn được điểm.
 *   · "6/9 và 6/8" với "2/3 và 3/4" bằng nhau về GIÁ TRỊ; câu hỏi lại đang hỏi con
 *     đã quy đồng tử chưa, nên phép so số không phân biệt nổi.
 * Vẫn tha phần chú thích trong ngoặc / sau gạch ngang, vì nút chỉ in phần cốt lõi.
 */
function matchPick(expectedRaw, input) {
  const { core } = splitAside(expectedRaw);
  const bare = answerCore(expectedRaw);
  const b = normText(input);
  return [expectedRaw, core, bare].some((e) => normText(e) === b);
}

function matchOne(expectedRaw, input) {
  const { core } = splitAside(expectedRaw);              // lý do trong ngoặc không phải đáp án
  const bare = answerCore(expectedRaw);                  // lý do sau gạch ngang cũng vậy
  if (matchAtom(expectedRaw, input) || matchAtom(core, input) || matchAtom(bare, input)) return true;

  // Đáp án là một dãy số: con viết "29; 38" hay "29, 38" hay "38 và 29" đều nhận —
  // đủ số và đúng số là được, dấu ngăn cách và thứ tự thì tuỳ con.
  if (isNumberList(bare)) return matchList({ values: parseList(bare) }, input);

  const ce = parseCompare(core);
  if (ce) {
    const ci = parseCompare(input);
    // "9/10 > 7/8" cũng đúng như "7/8 < 9/10" — cùng một khẳng định, viết ngược lại thôi
    if (ci) {
      return (ci.op === ce.op && matchAtom(ce.a, ci.a) && matchAtom(ce.b, ci.b))
          || (ci.op === FLIP[ce.op] && matchAtom(ce.a, ci.b) && matchAtom(ce.b, ci.a));
    }
    // đáp "0,75 = 75%" — con viết hai giá trị, ngăn cách kiểu gì cũng nhận
    if (ce.op === '=') {
      const got = String(input ?? '').split(/\s*[=;]\s*|\s{2,}/).map((t) => t.trim()).filter(Boolean);
      if (got.length === 2) return matchAtom(ce.a, got[0]) && matchAtom(ce.b, got[1]);
    }
  }
  return false;
}

/**
 * @returns {{ok:boolean, mode:'auto'|'selfcheck', expected:string, parts?:Array}}
 * mode='selfcheck' → hiện lời giải mẫu, con tự đối chiếu (không chấm sai)
 */
export function checkAnswer(item, input) {
  const key = item.answerKey || {};

  if (item.format === 'tf') {
    /**
     * Nhận cả nút "ĐÚNG"/"SAI" lẫn boolean. CHƯA TRẢ LỜI thì phải là CHƯA ĐÚNG:
     * trước đây ô rỗng bị đọc thành `false`, nên 68 câu có đáp án SAI được chấm
     * đúng dù con chưa bấm gì.
     */
    const got = typeof input === 'boolean' ? input
      : { 'đúng': true, 'true': true, 'sai': false, 'false': false }[normText(input)];
    return { ok: got !== undefined && got === key.value, mode: 'auto',
             expected: key.value ? 'ĐÚNG' : 'SAI' };
  }

  if (item.format === 'mcq') {
    const got = Array.isArray(input) ? input[0] : input;
    return { ok: !!String(got ?? '').trim() && normText(got) === normText(key.choice),
             mode: 'auto', expected: String(key.choice) };
  }

  // Đáp án là DANH SÁCH số ("tìm tất cả các số…"). Trước đây rơi vào nhánh tự-đối-chiếu
  // nên luôn tính ĐÚNG — kể cả câu bắt buộc đúng, làm thủng cổng mustPass.
  if (key.values) {
    return { ok: matchList(key, Array.isArray(input) ? input[0] : input), mode: 'auto',
             expected: key.values.join('; ') };
  }

  // Đáp án viết được nhiều cách đều đúng ("4 507 = 4 000 + 500 + 7" hay "4000 + 500 + 7").
  // Trước đây checkAnswer không biết khoá này nên rơi xuống nhánh cuối, luôn trả selfcheck —
  // con MẤT ô nhập, chỉ còn nút xem lời giải.
  if (key.accept) {
    const list = [].concat(key.accept);
    const got = Array.isArray(input) ? input[0] : input;
    return { ok: list.some((a) => matchOne(a, got)), mode: 'auto', expected: String(list[0]) };
  }

  if (key.parts) {
    const gradable = gradableParts(key.parts);
    const expected = key.parts.map((p) => `${p.label}: ${p.value}`).join(' · ');
    if (gradable.length === 0) return { ok: true, mode: 'selfcheck', expected };
    const arr = Array.isArray(input) ? input : [input];
    const parts = gradable.map((p, i) => ({
      label: p.label,
      expected: typeof p.value === 'number' ? fmtNum(p.value) : String(p.value),
      ok: isPickable(p) ? matchPick(p.value, arr[i]) : matchOne(p.value, arr[i]),
    }));
    return {
      ok: parts.every((p) => p.ok),
      mode: key.parts.length > gradable.length ? 'mixed' : 'auto',
      expected, parts,
    };
  }

  if (key.value !== undefined) {
    if (typeof key.value === 'boolean') {
      const got = typeof input === 'boolean' ? input : String(input).toLowerCase() === 'true';
      return { ok: got === key.value, mode: 'auto', expected: key.value ? 'ĐÚNG' : 'SAI' };
    }
    if (isSelfCheck(key.value)) return { ok: true, mode: 'selfcheck', expected: String(key.value) };
    const got = Array.isArray(input) ? input[0] : input;
    return { ok: matchOne(key.value, got), mode: 'auto',
             expected: typeof key.value === 'number' ? fmtNum(key.value) : String(key.value) };
  }

  return { ok: true, mode: 'selfcheck', expected: item.solutionNarrative || '' };
}

/* ─────────── NĂM KIỂU TRẢ LỜI — một nguồn sự thật duy nhất ───────────
 * Con mở bài ra phải biết NGAY mình phải làm gì. Mọi màn hình (luyện tập, chốt
 * nhanh, sát hạch) đều hỏi hàm này chứ không tự đoán theo `format`.
 *
 *   'so'        điền một con số
 *   'bieuthuc'  điền biểu thức toán (phân số, tỉ số, giờ, dãy số, so sánh)
 *   'dungsai'   bấm ĐÚNG hoặc SAI
 *   'chondapan' bấm một đáp án trong danh sách
 *   'tuluan'    làm ra nháp rồi xem lời giải mẫu để tự so — không phải nhập gì
 */
export const CACH_TRA_LOI = {
  so:        'Con điền một con số vào ô.',
  bieuthuc:  'Con điền biểu thức toán vào ô (xem chữ mờ trong ô để biết dạng).',
  dungsai:   'Con bấm chọn ĐÚNG hoặc SAI.',
  chondapan: 'Con bấm chọn một đáp án.',
  tuluan:    'Con làm ra giấy nháp. Xong bấm nút để xem lời giải mẫu rồi tự so.',
};
const KIEU_BIEUTHUC = ['fraction', 'ratio', 'time', 'minutes', 'divmod', 'numlist', 'list', 'compare'];

export function answerMode(item) {
  if (item?.format === 'tf') return 'dungsai';
  if (item?.format === 'mcq') return 'chondapan';
  const fs = answerFields(item);
  if (fs.length === 0) return 'tuluan';
  if (fs.some((f) => f.kind === 'pick')) return 'chondapan';
  if (fs.some((f) => KIEU_BIEUTHUC.includes(f.kind))) return 'bieuthuc';
  return 'so';
}

/** Số ô nhập cần hiển thị cho một câu */
export function inputCount(item) {
  // Đúng/Sai và trắc nghiệm CŨNG là một ô trả lời — trước đây trả 0, nên màn
  // luyện tập không dựng nút nào cho 90 câu: 68 câu được chấm ĐÚNG dù con chưa
  // trả lời, 22 câu bị chấm SAI rồi kẹt cứng vì không có gì để sửa.
  if (item.format === 'tf' || item.format === 'mcq') return 1;
  const key = item.answerKey || {};
  if (key.values) return 1;              // danh sách nhiều số → một ô, con tự ngăn cách
  if (key.accept) return 1;              // viết cách nào cũng được → vẫn phải có chỗ mà viết
  if (key.parts) {
    const n = gradableParts(key.parts).length;
    // Câu tự luận ("giải thích vì sao…") vẫn phải có MỘT chỗ để con viết ra suy nghĩ.
    // Chỉ đưa cái nút "xem lời giải" thì con chưa nghĩ đã bấm — mất hết tác dụng.
    return n || (key.parts.length ? 1 : 0);
  }
  if (key.value !== undefined && isSelfCheck(key.value)) return 1;
  if (key.value === undefined) return 0;
  return 1;
}

/** Đơn vị đo đứng cuối đáp án: "60 000 đồng" → "đồng" · "12" → '' */
export function unitOf(expected) {
  const core = answerCore(expected);
  if (typeof core !== 'string') return '';
  const tail = normText(core).replace(/^[+-]?[\d.,\s ]*\d\s*/, '');
  return tail && tail !== normText(core) && MEASURE.test(tail) ? tail : '';
}

/**
 * Chữ mờ trong ô nhập — nói cho con biết ô này chờ DẠNG gì.
 * Chỉ mô tả DẠNG, tuyệt đối không để lộ đáp án: câu so sánh thì đưa ví dụ bằng số
 * khác hẳn, câu có đơn vị thì chỉ nhắc tên đơn vị.
 *
 * Trước đây trả về "?" trơ trọi cho 458 câu — con nhìn vào không biết nên gõ số,
 * gõ chữ hay gõ phân số. Giờ luôn nói rõ dạng cần điền.
 */
export function inputPlaceholder(item, label, expected) {
  if (item?.answerKey?.values) return 'các số, cách nhau bằng dấu ;';
  if (item?.answerKey?.accept) return 'con viết lời giải của mình';
  const core = expected === undefined ? undefined : answerCore(expected);
  const cmp = core === undefined ? null : parseCompare(core);
  if (cmp) return cmp.op === '=' ? 'vd: 0,5 = 50%' : 'vd: 3/4 > 2/5';
  const nt = core === undefined ? null : numAndTail(core);
  if (nt) {
    const unit = unitOf(expected);
    if (unit) return `điền số, đơn vị là ${unit}`;
    return nt.tail ? 'điền số kèm chữ' : 'điền số';
  }
  const m = core === undefined ? null : mathKind(core);
  if (m) return m.hint;
  if (typeof core === 'string') return 'trả lời bằng chữ';
  return label ? `${label} = ?` : 'điền đáp án';
}

const LETTERS = ['a', 'b', 'c', 'd', 'e', 'g'];

/**
 * Mô tả TỪNG ô nhập cho giao diện: nhãn hiện thường trực, đơn vị, dạng cần điền.
 *
 * Vì sao cần: trước đây nhãn chỉ nằm trong chữ mờ của ô — con gõ ký tự đầu tiên là
 * nhãn biến mất, 295 câu nhiều ô thành ra không biết ô nào hỏi gì. Và khi đáp án có
 * đơn vị thì nhãn bị đơn vị chiếm chỗ, hai ô cùng hiện "? %" y hệt nhau.
 */
export const DUNG_SAI = ['ĐÚNG', 'SAI'];

export function answerFields(item) {
  const key = item?.answerKey || {};

  // Đúng/Sai và trắc nghiệm: một ô BẤM CHỌN, dựng ở đây để mọi màn hình dùng chung
  // một khối ô trả lời — trước đây chỉ AnswerInput biết dựng, PracticeItem thì không.
  if (item?.format === 'tf') {
    return [{ index: 0, letter: '', label: 'Câu này đúng hay sai?', unit: '',
              kind: 'pick', placeholder: '', options: DUNG_SAI }];
  }
  if (item?.format === 'mcq') {
    const opts = (item.choices || []).filter((c) => String(c ?? '').trim());
    if (opts.length >= 2) {
      return [{ index: 0, letter: '', label: 'Chọn đáp án đúng', unit: '',
                kind: 'pick', placeholder: '', options: opts }];
    }
    return [];
  }

  const n = inputCount(item);
  if (n === 0) return [];
  const parts = key.parts || [];
  const gradable = gradableParts(parts);
  /**
   * Tự luận là khi CÓ phần trả lời nhưng không phần nào máy chấm được.
   * Câu không có `parts` thì đáp số nằm ở `key.value` / `key.accept` — vẫn chấm
   * được như thường. Thiếu vế `parts.length > 0`, 211 câu ĐÁP SỐ LÀ SỐ bị dựng
   * thành ô viết văn: con được mời "viết cách làm của mình", gõ "Tận cùng là 2"
   * rồi bị chấm SAI vì máy chỉ nhận đúng "2" — và cổng mustPass chặn luôn bài sau.
   */
  const essay = parts.length > 0 && gradable.length === 0;
  const prose = essay ? parts[0] : null;
  const expects = gradable.length ? gradable.map((p) => p.value)
                : key.accept ? [[].concat(key.accept)[0]]
                : [prose ? prose.value : key.value];
  const options = choicesFromText(item);

  return Array.from({ length: n }, (_, i) => {
    const expected = expects[i];
    const raw = (gradable[i]?.label || '').trim();
    /**
     * Bộ chọn lấy theo thứ tự ưu tiên:
     *   1. options đặt sẵn trong dữ liệu cho RIÊNG ô này (đáp án bằng chữ)
     *   2. bộ đề tự nêu ra ("Điền TĂNG hoặc GIẢM: …")
     * Có bộ chọn thì con BẤM, khỏi phải đoán gõ chữ gì.
     */
    const own = gradable[i]?.options;
    const pick = Array.isArray(own) && own.length >= 2 ? own : options;
    if (essay) {
      return {
        index: i, letter: '',
        label: (prose?.label || 'lời giải của con').trim(),
        unit: '', kind: 'essay',
        placeholder: 'con viết cách làm của mình vào đây',
        options: null,
      };
    }
    return {
      index: i,
      letter: n > 1 ? LETTERS[i] || String(i + 1) : '',
      label: raw || (n > 1 ? `ô thứ ${i + 1}` : 'đáp số'),
      unit: pick ? '' : unitOf(expected),
      kind: pick ? 'pick' : fieldKind(item, expected),
      placeholder: inputPlaceholder(item, raw, expected),
      options: pick,
    };
  });
}

/**
 * Đáp án viết bằng KÝ HIỆU TOÁN — con gõ được, không cần bấm chọn.
 * Trước đây gộp hết vào 'text' nên ô phân số cũng bị nhắc "trả lời bằng chữ",
 * mà con thì đang định gõ 3/4.
 */
const DANG_TOAN = [
  ['fraction', /^[+-]?\d+\s*\/\s*\d+$/,            'điền phân số, vd 3/4'],
  ['ratio',    /^\d+\s*[:：]\s*\d+$/,               'điền tỉ số, vd 3 : 4'],
  ['divmod',   /^\d+\s*dư\s*\d+$/,                  'điền dạng: 9 dư 2'],
  ['time',     /^\d+\s*giờ(\s*\d+\s*phút)?$/,       'điền dạng: 2 giờ 24 phút'],
  ['minutes',  /^\d+\s*phút$/,                      'điền số phút'],
  ['numlist',  /^[\d\s.,;và]*\d[\d\s.,;và]*$/,      'các số, cách nhau bằng dấu ;'],
];

export function mathKind(core) {
  if (typeof core !== 'string') return null;
  const s = core.trim();
  for (const [kind, re, hint] of DANG_TOAN) if (re.test(s)) return { kind, hint };
  return null;
}

function fieldKind(item, expected) {
  if (item?.answerKey?.values) return 'list';
  if (item?.answerKey?.accept) return 'free';
  const core = expected === undefined ? undefined : answerCore(expected);
  if (core !== undefined && parseCompare(core)) return 'compare';
  if (core !== undefined && numAndTail(core)) return 'number';
  const m = core === undefined ? null : mathKind(core);
  if (m) return m.kind;
  return 'text';
}

/** Một dòng nói thẳng bài này đòi con làm gì — hiện ngay trên các ô nhập. */
export function answerBrief(item) {
  const mode = answerMode(item);
  if (mode === 'dungsai' || mode === 'tuluan') return CACH_TRA_LOI[mode];
  if (item?.format === 'mcq') return CACH_TRA_LOI.chondapan;
  const n = inputCount(item);
  // Đề hỏi mấy việc nhưng chỉ mấy việc chấm được bằng máy — phần giải thích để con
  // nói ra nháp. Không nói trước thì con điền xong vẫn tưởng mình còn thiếu.
  const parts = item?.answerKey?.parts || [];
  const prose = parts.length - gradableParts(parts).length;
  const tail = prose > 0
    ? ` Phần giải thích con nói ra nháp — bấm Kiểm tra xong sẽ có lời giải mẫu để đối chiếu.`
    : '';

  if (item?.answerKey?.values)
    return 'Con điền tất cả các số vào một ô, cách nhau bằng dấu chấm phẩy.' + tail;
  if (n === 1) return 'Bài này cần điền 1 ô.' + tail;
  return `Bài này cần điền ${n} ô — điền đủ cả ${n} rồi bấm Kiểm tra.` + tail;
}

/**
 * Đề tự nói ra bộ đáp án ("Điền TĂNG hoặc GIẢM: …") → cho con BẤM chọn,
 * khỏi phải gõ đúng từng chữ. Không đoán mò: chỉ nhận khi đề ghi rõ.
 */
export function choicesFromText(item) {
  const m = String(item?.text || '')
    .match(/[Đđ]iền\s+"?([^":.,]{1,24}?)"?\s+hoặc\s+"?([^":.,]{1,24}?)"?\s*[:.]/);
  return m ? [m[1].trim(), m[2].trim()] : null;
}

/* ─────────── Dựng dòng chảy 5 chặng ─────────── */
/**
 * Đi lại trong bài: đốt nào con bấm vào được trên thanh tiến trình.
 *
 * Bài vốn chỉ đi MỘT CHIỀU — lỡ tay bấm Tiếp là mất luôn phần vừa đọc, muốn xem
 * lại hay làm lại cho nhớ cũng chịu. Nay lùi được, và bấm thẳng vào phần đã học
 * được. Nhưng KHÔNG cho vượt lên phần chưa học: nhảy thẳng tới sát hạch là bỏ qua
 * cả mạch giảng bài lẫn cổng mustPass — luật sư phạm, không phải chuyện trang trí.
 *
 * `daDi` là bước XA NHẤT con từng tới, không phải bước đang đứng: lùi về xem lại
 * rồi vẫn phải tiến lại được tới chỗ cũ.
 */
export const bamDuocDot = (k, hienTai, daDi) => k <= daDi && k !== hienTai;

export const PHASES = [
  { id: 'intro', label: 'MỞ BÀI' },
  { id: 'teach', label: 'GIẢNG' },
  { id: 'sample', label: 'BÀI MẪU' },
  { id: 'practice', label: 'LUYỆN TẬP' },
  { id: 'assess', label: 'SÁT HẠCH' },
];

const figFor = (lesson, block) =>
  (lesson.figureSpec || []).find((f) => (f.usedIn || []).includes(block)) || null;

const TEACH_KINDS = ['guided_discovery', 'explain', 'trap'];

/**
 * Dựng chặng GIẢNG.
 *
 * Trước đây mỗi K-statement là MỘT màn, ghép với màn giảng thứ i theo đúng thứ tự.
 * Bài nào cũng có nhiều nguyên tắc hơn màn giảng (B1.M1: 5 nguyên tắc / 2 màn) nên
 * những nguyên tắc cuối ra màn TRỐNG TRƠN — trơ mỗi một dòng chữ, không hình,
 * không lời giảng — mà lời giảng thì lại rơi nhầm sang nguyên tắc khác.
 *
 * Giờ gom theo `screen.teaches` có sẵn trong dữ liệu: mỗi màn giảng kéo về đúng
 * những nguyên tắc nó dạy. Nguyên tắc không màn nào nhận thì theo nguyên tắc liền
 * trước — không bao giờ để trôi mất.
 */
export function buildTeachSteps(lesson) {
  const K = lesson.knowledgeCore || {};
  const statements = K.statements || [];
  const screens = (lesson.lecture?.screens || []).filter((s) => TEACH_KINDS.includes(s.kind));
  const misconception = (K.misconceptions || [])[0] || null;

  if (screens.length === 0 || statements.length === 0) {
    return statements.length
      ? [{ type: 'teach', phase: 'teach', statements, screen: screens[0] || null,
           figure: figFor(lesson, 'teach_domain'), misconception }]
      : [];
  }

  const owner = statements.map((st) =>
    screens.findIndex((s) => (s.teaches || []).includes(st.id)));
  for (let i = 0; i < owner.length; i++) {
    if (owner[i] >= 0) continue;
    let j = i - 1;
    while (j >= 0 && owner[j] < 0) j--;
    if (j >= 0) { owner[i] = owner[j]; continue; }
    let k = i + 1;
    while (k < owner.length && owner[k] < 0) k++;
    owner[i] = k < owner.length ? owner[k] : 0;
  }

  const groups = screens.map((screen) => ({ screen, statements: [] }));
  statements.forEach((st, i) => groups[owner[i]].statements.push(st));

  // màn giảng không kéo được nguyên tắc nào mà cũng chẳng có lời giảng thì bỏ hẳn
  const kept = groups.filter((g) => g.statements.length || g.screen?.narration);
  return kept.map((g, i) => ({
    type: 'teach', phase: 'teach',
    statements: g.statements,
    screen: g.screen,
    /* Hình chỉ đích danh màn ('screen:S3') thì theo nó — bài nào có nhiều hình
       trong phần giảng mà mỗi hình thuộc một bước riêng thì xếp theo thứ tự
       khái niệm/cách làm là đặt sai chỗ, lời văn treo giữa chừng.
       Không chỉ đích danh thì giữ nguyên nếp cũ của lớp 5. */
    figure: figFor(lesson, `screen:${g.screen?.id}`)
          || (i === 0 ? figFor(lesson, 'teach_domain')
          : (i === 1 ? figFor(lesson, 'teach_core') : null)),
    misconception: i === kept.length - 1 ? misconception : null,
    /* Hình của CHỖ HAY NHẦM đi kèm đúng màn in ra chỗ hay nhầm. Ô `trap` vốn có
       trong dữ liệu từ lâu mà chưa nơi nào gọi tới — 168 hình lời thoại của lớp 5
       nằm ở màn MỞ BÀI, tức bé thấy một câu SAI được nói chắc nịch trước khi học
       gì. Nay chúng dọn về đây, sau khi giảng xong, đúng chỗ để soi lại cái bẫy. */
    figureBay: i === kept.length - 1 ? figFor(lesson, 'trap') : null,
  }));
}

/**
 * lesson: nội dung một file DL_*.json
 * @returns {Array<{type,phase,...}>}
 */
export function buildFlow(lesson) {
  const steps = [];
  const K = lesson.knowledgeCore || {};

  steps.push({ type: 'intro', phase: 'intro', figure: figFor(lesson, 'mantra') });

  const hook = (lesson.lecture?.screens || []).find((s) => s.kind === 'hook');
  if (hook) steps.push({ type: 'hook', phase: 'intro', screen: hook, figure: figFor(lesson, 'hook') });

  buildTeachSteps(lesson).forEach((s) => steps.push(s));

  const check = (lesson.lecture?.screens || []).find((s) => s.item);
  if (check) steps.push({ type: 'check', phase: 'teach', item: check.item });

  steps.push({ type: 'mantra', phase: 'teach', text: K.mantra, vocabulary: K.vocabulary });

  const figDomain = figFor(lesson, 'teach_domain');
  const figCore = figFor(lesson, 'teach_core');
  (K.canonicalExamples || []).forEach((ex, i) =>
    steps.push({ type: 'sample', phase: 'sample', example: ex, index: i + 1,
                 total: (K.canonicalExamples || []).length,
                 figure: i === 0 ? figDomain : (i === 1 ? figCore : null) }));

  if (lesson.workedExample)
    steps.push({ type: 'worked', phase: 'sample', we: lesson.workedExample, figure: figDomain });

  /* Hình của RIÊNG một câu hỏi ('item:C8'). Có câu mà ĐỀ NẰM TRONG HÌNH — thiếu
     hình thì bé không có gì mà làm, chứ không phải chỉ mất phần minh hoạ.
     'item:C8:giai' là hình của LỜI GIẢI, chỉ hiện sau khi bé làm xong: bài đếm
     hình thì lời giải phải chỉ ra TỪNG hình tìm được ngay trên hình vẽ, chứ kể
     bằng lời thì bé vẫn không biết mình sót cái nào. Để chung một hình với đề là
     lộ đáp án ngay lúc bé chưa làm. */
  const pools = lesson.practice?.pools || {};
  ['warmup', 'standard', 'challenge'].forEach((lv) =>
    (pools[lv] || []).forEach((item) => steps.push({
      type: 'practice', phase: 'practice', item, level: lv,
      figure: figFor(lesson, `item:${item.id}`),
      figureGiai: figFor(lesson, `item:${item.id}:giai`) })));

  (lesson.assessment?.items || []).forEach((item, i) =>
    steps.push({ type: 'assess', phase: 'assess', item, index: i + 1,
                 figure: figFor(lesson, `item:${item.id}`),
                 figureGiai: figFor(lesson, `item:${item.id}:giai`),
                 total: (lesson.assessment?.items || []).length }));

  steps.push({ type: 'finale', phase: 'assess' });
  return steps;
}

/* ─────────── Luật đạt của micro ─────────── */
/**
 * log: [{id, ok, mustPass}]
 * passRule ví dụ: "≥ 2/3, bắt buộc đúng A1" | "≥ 3/4, bắt buộc đúng A1 và A4"
 */
export function gradeMicro(log, passRule = '') {
  const total = log.length;
  const right = log.filter((a) => a.ok).length;
  const mustOK = log.filter((a) => a.mustPass).every((a) => a.ok);
  const m = String(passRule).match(/(\d+)\s*\/\s*(\d+)/);
  const need = m ? Number(m[1]) : Math.ceil(total * 2 / 3);
  return { right, total, mustOK, need, pass: right >= need && mustOK };
}

/* ─────────── Gợi ý theo số lần sai (adaptiveRules trong dữ liệu) ─────────── */
export function hintState(item, tries) {
  const hints = item.hints || [];
  return {
    show: hints.slice(0, Math.min(tries, hints.length)),
    reveal: tries >= 3,
    solution: tries >= 3 ? (item.solutionNarrative || '') : '',
  };
}

/** Đường dẫn ảnh: figureSpec lưu "figures/xxx.png" */
export const figureUrl = (fig, base = '/') =>
  fig && fig.file ? base.replace(/\/$/, '') + '/' + fig.file : null;

/* ─────────── Ví dụ dẫn dắt: bung thành chuỗi bước con ─────────── */
/**
 * workedExample.steps có thể kèm askBefore / askAfter.
 * Bung thành mạch tuyến tính để UI đi từng nhịp:
 *   [{kind:'ask', item, at:'before', stepIndex}, {kind:'show', text, stepIndex}, ...]
 * @returns {Array}
 */
export function buildWorkedSteps(we) {
  const out = [];
  (we?.steps || []).forEach((st, idx) => {
    if (st.askBefore) out.push({ kind: 'ask', at: 'before', stepIndex: idx, item: st.askBefore });
    out.push({ kind: 'show', stepIndex: idx, text: st.show });
    if (st.askAfter) out.push({ kind: 'ask', at: 'after', stepIndex: idx, item: st.askAfter });
  });
  return out;
}

/** Câu hỏi xen giữa của ví dụ dẫn dắt vẫn dùng chung bộ chấm */
export const askIsMcq = (item) => Array.isArray(item?.choices) && item.choices.length > 0;

/* ─────────── Ca mẫu: tách nhãn cho UI ─────────── */
export function sampleParts(ex) {
  return {
    tag: (ex.case || '').replace(/\s*\(.*?\)\s*$/, '').trim(),   // "chu vi từ r (ca nền)" → "chu vi từ r"
    kind: (ex.case || '').match(/\(([^)]+)\)/)?.[1] || '',        // → "ca nền"
    problem: ex.problem || '',
    solution: ex.solution || '',
    why: ex.why || '',
  };
}

/* ─────────── Sinh đề biến thể (chỉ khi metadata đủ máy đọc) ─────────── */
/** "1–9" | "1-9" | "2 – 20" → {lo, hi}; không khớp → null */
export function parseRange(s) {
  const m = String(s).match(/^\s*(\d+)\s*[–\-—]\s*(\d+)\s*$/);
  return m ? { lo: Number(m[1]), hi: Number(m[2]) } : null;
}

/** Biểu thức số học thuần: chỉ biến, số, + − × : ( ) */
const ARITH = /^[\sA-Za-z0-9+\-×:()·,.]+$/;
export function isArithmeticRule(rule, vars) {
  const r = String(rule || '');
  if (!ARITH.test(r)) return false;
  const names = r.match(/[A-Za-z]+/g) || [];
  return names.length > 0 && names.every((n) => vars.includes(n));
}

/** Tính giá trị biểu thức với bộ biến — không dùng eval tự do */
export function evalRule(rule, env) {
  const expr = String(rule).replace(/×/g, '*').replace(/:/g, '/').replace(/·/g, '*').replace(/,/g, '.');
  const names = Object.keys(env);
  if (!/^[\s0-9+\-*/().A-Za-z]+$/.test(expr)) return NaN;
  for (const n of (expr.match(/[A-Za-z]+/g) || [])) if (!names.includes(n)) return NaN;
  try {
    // eslint-disable-next-line no-new-func
    const f = new Function(...names, `"use strict"; return (${expr});`);
    const v = f(...names.map((n) => env[n]));
    return Number.isFinite(v) ? Math.round(v * 1e6) / 1e6 : NaN;
  } catch { return NaN; }
}

/** Câu này có sinh biến thể được không? */
export function canGenerate(item) {
  const g = item?.generator;
  if (!g?.template || !g?.answerRule) return false;
  const vars = [...new Set([...String(g.template).matchAll(/\{(\w+)\}/g)].map((m) => m[1]))];
  if (vars.length === 0) return false;
  const cons = g.constraints || {};
  const ranges = {};
  for (const v of vars) {
    const raw = cons[v] ?? Object.entries(cons).find(([k]) => k.split(/[,\s]+/).includes(v))?.[1];
    const r = parseRange(raw);
    if (!r) return false;                       // ràng buộc mô tả bằng lời → không sinh được
    ranges[v] = r;
  }
  return isArithmeticRule(g.answerRule, vars) ? { vars, ranges } : false;
}

/**
 * Sinh một đề biến thể. Trả null nếu không đủ metadata (UI khi đó ẩn nút "Đề khác").
 * rnd: hàm ngẫu nhiên (bơm vào để test tái lập được)
 */
export function makeVariant(item, rnd = Math.random) {
  const cap = canGenerate(item);
  if (!cap) return null;
  const env = {};
  for (const v of cap.vars) {
    const { lo, hi } = cap.ranges[v];
    env[v] = lo + Math.floor(rnd() * (hi - lo + 1));
  }
  const val = evalRule(item.generator.answerRule, env);
  if (!Number.isFinite(val)) return null;
  const text = String(item.generator.template).replace(/\{(\w+)\}/g, (_, k) => fmtNum(env[k]));
  return {
    ...item,
    id: item.id + '·biến-thể',
    text,
    answerKey: { value: val },
    hints: item.hints,
    solutionNarrative: `Đáp án: ${fmtNum(val)}`,
    _variant: true,
  };
}
