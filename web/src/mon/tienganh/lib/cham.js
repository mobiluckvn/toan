/**
 * BỘ CHẤM TIẾNG ANH — JS thuần, không React, KHÔNG import gì từ `mon/toan/**`.
 *
 * ── VÌ SAO KHÔNG DÙNG LẠI `flow.js` ──
 * Bộ chấm Toán nới đúng những chỗ tiếng Anh phải SIẾT, và siết đúng chỗ tiếng Anh
 * phải NỚI. Ba chỗ đã soi tận nơi, không đoán:
 *
 *   1. `isSelfCheck` — đáp án dài quá 26 ký tự thì flow.js bỏ chấm, cho bé "tự đối
 *      chiếu". Mà câu dài nhất của lớp 1 là
 *          "How many windows can you see? - I can see six."   (46 ký tự)
 *      Bê nguyên là bé MẤT Ô NHẬP ở đúng bậc 4 — bậc mà bác muốn có nhất. Hỏng kiểu
 *      im lặng: dữ liệu vẫn hợp lệ, cổng vẫn xanh, chỉ bé là không gõ được.
 *
 *   2. `toNumber` · `matchList` · `nearEq` — quy đáp án về SỐ, và nhận dãy số không
 *      kể thứ tự. Với tiếng Anh thì thứ tự từ CHÍNH LÀ ngữ pháp: "a dog is this"
 *      không phải "this is a dog".
 *
 *   3. `answerCore` cắt phần sau gạch ngang dài (—, –) coi là lời giải thích. Câu
 *      tiếng Anh dùng gạch ngắn "- " để ngăn hỏi/đáp ("How many clocks? - Two.")
 *      — cắt đi là mất nửa câu.
 *
 * Ngược lại, tiếng Anh cần ba phép nới mà Toán không có: dấu nháy cong, chữ hoa
 * đầu câu, và dấu chấm cuối. Xem `chuanTA` bên dưới.
 *
 * ── SIẾT Ở ĐÂU ──
 * Sai chính tả là SAI. Không có "gần đúng", không sửa hộ, không bỏ qua chữ thiếu.
 * Vì bậc 4 đang kiểm đúng cái đó — viết lại được từ. Nới ở đây là dạy bé sai.
 */

/* ─────────── Chuẩn hoá một câu trả lời ─────────── */

/**
 * Dấu nháy: bàn phím iPad/iPhone TỰ ĐỔI `'` (U+0027) thành `’` (U+2019) khi bé gõ
 * "I'm". Dữ liệu bản đồ dùng dấu thẳng (đã soát cả 19 mẫu câu lớp 1: 20/20 là
 * U+0027). Không gộp hai dấu này thì bé gõ đúng y hệt vẫn bị chấm sai, và bé thì
 * tin máy chứ không tin mình.
 */
const gopNhay = (s) => String(s ?? '').replace(/[‘’ʼ´`]/g, "'")
  .replace(/[“”]/g, '"')
  .replace(/[‐‑‒–—]/g, '-');

/**
 * Chuẩn hoá để so khớp. Nới đúng BỐN chỗ, và chỉ bốn chỗ:
 *   1. dấu nháy cong ↔ thẳng          (bàn phím tự đổi — xem trên)
 *   2. hoa ↔ thường                   (bé 6 tuổi chưa dùng phím Shift)
 *   3. khoảng trắng thừa, kể cả quanh dấu gạch ngăn hỏi/đáp
 *   4. dấu chấm câu Ở CUỐI            (. ! ?)
 *
 * KHÔNG nới: thứ tự từ · chính tả · dấu câu GIỮA câu · số ↔ chữ.
 */
export function chuanTA(s) {
  return gopNhay(s)
    .toLowerCase()
    .replace(/\s*-\s*/g, ' - ')     // "clocks?-Two" và "clocks? -  Two" về một dạng
    .replace(/\s+/g, ' ')
    .replace(/[.!?]+$/, '')
    .trim();
}

/** Bé chưa gõ gì thì là CHƯA ĐÚNG — không phải "đúng vì rỗng khớp rỗng". */
const coTraLoi = (v) => String(v ?? '').trim() !== '';

/* ─────────── So một ô ─────────── */

/**
 * So một ô GÕ TAY. Nhận thêm các cách viết khác cùng đúng qua `nhanThem`
 * (ví dụ "Two" và "2" ở câu How many — do người soạn khai, KHÔNG do máy suy).
 */
export function chamO(dapAn, batDau, nhanThem = []) {
  if (!coTraLoi(batDau)) return false;
  const b = chuanTA(batDau);
  return [dapAn, ...nhanThem].some((x) => chuanTA(x) === b);
}

/**
 * So một ô BẤM CHỌN. Bé bấm nút nên không có lỗi gõ — chỉ đối chiếu chữ trên nút.
 * Vẫn dùng `chuanTA` để dấu nháy trên nút và trong đáp án không lệch nhau.
 */
export function chamNut(dapAn, batDau) {
  return coTraLoi(batDau) && chuanTA(dapAn) === chuanTA(batDau);
}

/**
 * So bài XẾP THẺ. Bé kéo các thẻ chữ thành câu; đúng khi đủ thẻ VÀ đúng thứ tự.
 *
 * Cố ý so từng thẻ chứ không ghép chuỗi rồi so: ghép chuỗi thì "This is" + "a dog"
 * và "This" + "is a dog" ra cùng một câu, trong khi bé thứ hai chưa hề tách đúng
 * từ. Ở lớp 1 thì việc nhận ra RANH GIỚI TỪ chính là một phần bài học.
 */
export function chamThe(dapAn, batDau) {
  const a = [].concat(dapAn || []);
  const b = [].concat(batDau || []);
  if (!a.length || a.length !== b.length) return false;
  return a.every((x, i) => chuanTA(x) === chuanTA(b[i]));
}

/* ─────────── Chấm cả câu ─────────── */

/**
 * @returns {{ok:boolean, mode:'auto'|'selfcheck', expected:string, parts?:Array}}
 *
 * Cùng HÌNH DẠNG trả về với `checkAnswer` của Toán — cố ý, để LessonPlayer và sổ
 * tiến độ dùng chung được mà không cần biết đang chấm môn nào. Giống hình dạng
 * KHÔNG có nghĩa là chung mã nguồn: hai hàm nằm hai vùng, cổng `ranh_gioi` gác.
 *
 * Năm dạng câu của lớp 1 (xem docs/lop1_tieng_anh_khao_sat_va_thiet_ke.md mục 4.1):
 *   'chon'    bậc 1-2 · nghe/nhìn rồi bấm            → key.choice
 *   'dungsai' bậc 2   · đúng hay sai                  → key.value (boolean)
 *   'the'     bậc 3   · xếp thẻ chữ thành câu         → key.the (mảng, đúng thứ tự)
 *   'go'      bậc 4   · gõ lại từ hoặc câu            → key.value (+ key.nhanThem)
 *   'nhieuO'  bài ôn  · nhiều ô trong một câu         → key.parts
 */
export function chamTiengAnh(item, batDau) {
  const key = item?.answerKey || {};

  if (key.the) {
    const arr = Array.isArray(batDau) ? batDau : String(batDau ?? '').trim().split(/\s+/);
    return { ok: chamThe(key.the, arr), mode: 'auto', expected: key.the.join(' ') };
  }

  if (item?.format === 'chon' || key.choice !== undefined) {
    const got = Array.isArray(batDau) ? batDau[0] : batDau;
    return { ok: chamNut(key.choice, got), mode: 'auto', expected: String(key.choice) };
  }

  if (typeof key.value === 'boolean') {
    /* Chưa bấm gì phải là CHƯA ĐÚNG. Đọc ô rỗng thành `false` là bẫy mà bộ chấm
       Toán đã dính thật: 68 câu có đáp án SAI được chấm đúng dù bé chưa trả lời. */
    const got = typeof batDau === 'boolean' ? batDau
      : { 'đúng': true, true: true, yes: true, sai: false, false: false, no: false }[chuanTA(batDau)];
    return { ok: got !== undefined && got === key.value, mode: 'auto',
             expected: key.value ? 'ĐÚNG' : 'SAI' };
  }

  if (key.parts) {
    const arr = Array.isArray(batDau) ? batDau : [batDau];
    const parts = key.parts.map((p, i) => ({
      label: p.label,
      expected: String(p.value ?? ''),
      ok: p.options ? chamNut(p.value, arr[i]) : chamO(p.value, arr[i], p.nhanThem),
    }));
    return {
      ok: parts.every((p) => p.ok),
      mode: 'auto',
      expected: key.parts.map((p) => `${p.label}: ${p.value}`).join(' · '),
      parts,
    };
  }

  if (key.value !== undefined) {
    const got = Array.isArray(batDau) ? batDau[0] : batDau;
    /* KHÔNG có ngưỡng "dài quá thì thôi chấm" như bên Toán. Câu dài nhất lớp 1 là
       46 ký tự và nó VẪN phải chấm được — đó chính là bậc 4. */
    return { ok: chamO(key.value, got, key.nhanThem), mode: 'auto', expected: String(key.value) };
  }

  return { ok: true, mode: 'selfcheck', expected: item?.loiChua || '' };
}

/* ─────────── Dựng thẻ cho bài xếp câu ─────────── */

/**
 * Cắt một câu thành các thẻ để bé xếp lại.
 *
 * Dấu câu đi LIỀN với từ đứng trước ("clocks?" chứ không phải "clocks" + "?"), vì
 * bắt bé lớp 1 xếp riêng một thẻ dấu hỏi là thêm một việc mới không dạy điều gì.
 * Riêng dấu gạch ngăn hỏi/đáp thì thành MỘT thẻ riêng — nó ngăn hai vế, bé cần
 * thấy chỗ ngăn ấy.
 *
 *   "This is a dog."               → ['This', 'is', 'a', 'dog.']
 *   "How many clocks? - Two."      → ['How', 'many', 'clocks?', '-', 'Two.']
 */
export function catThe(cau) {
  return String(cau ?? '').trim().split(/\s+/).filter(Boolean);
}

/**
 * Bao nhiêu thẻ thì quá sức bé lớp 1.
 * Câu 5 thẻ trở xuống xếp được; dài hơn thì cho bé xếp NỬA câu (vế trả lời), phần
 * còn lại hiện sẵn. Ngưỡng này để bộ sinh bài hỏi, đừng gõ tay ở mỗi chỗ dùng.
 */
export const THE_TOI_DA = 5;
export const xepDuoc = (cau) => catThe(cau).length <= THE_TOI_DA;
