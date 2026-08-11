/**
 * CHỮ VIẾT — đọc một chuỗi markdown + LaTeX rời thành cây để React vẽ.
 *
 * ── VÌ SAO KHÔNG DÙNG KATEX ──
 *
 * Bác yêu cầu "dùng markdown, latex để show bài toán", nên DỮ LIỆU viết bằng
 * LaTeX thật (`$\frac{3}{4}$`, `$2 : 3$`). Nhưng bộ vẽ thì viết riêng, vì đã đếm
 * toàn bộ bốn quyển xem thật sự cần những gì:
 *
 *     phân số a/b 5097 · tỉ số a : b 3193 · dấu × 5263 · phần trăm 1726
 *     m² cm² 488 · phân số lồng 183 · lũy thừa 25 · hỗn số 17 · CĂN: 0
 *
 * Toàn bộ là số học tiểu học — không căn, gần như không mũ, không tích phân.
 * KaTeX nặng ~270 KB kèm bộ phông riêng, cho một app trẻ con mở bằng điện thoại
 * và mạng 3G thì đó là cái giá vô lý để vẽ mấy cái phân số. Bộ này chỉ nhận đúng
 * tập ký hiệu đã đếm được, vẽ bằng thẻ HTML nên thừa hưởng luôn phông và màu
 * thương hiệu.
 *
 * Dữ liệu vẫn là LaTeX chuẩn, nên hôm nào cần công thức nặng hơn thì thay bộ vẽ
 * này bằng KaTeX mà KHÔNG phải sửa một chữ nào trong nội dung.
 *
 * Nhận:
 *   markdown  **đậm** · *nghiêng* · `mã` · xuống dòng · gạch đầu dòng "- "
 *             · danh sách đánh số "1." · tiêu đề nhỏ "### "
 *   LaTeX     $…$ với \frac{}{}, \times, \div, \cdot, ^{}, _{}, \%,
 *             \dfrac, \left( \right), và chữ thường đi kèm
 */

/* ── 1 · TÁCH ĐOẠN LATEX RA KHỎI LỜI VĂN ────────────────────────────────────
   Cắt theo dấu `$` chứ không dò từng công thức: lời văn tiếng Việt đầy dấu
   ngoặc và dấu hai chấm, dò mò thì cắt nhầm giữa câu. */
export function tachToan(s) {
  const ra = [];
  let i = 0;
  const t = String(s ?? '');
  while (i < t.length) {
    const mo = t.indexOf('$', i);
    if (mo < 0) { ra.push({ loai: 'chu', t: t.slice(i) }); break; }
    if (mo > i) ra.push({ loai: 'chu', t: t.slice(i, mo) });
    const dong = t.indexOf('$', mo + 1);
    if (dong < 0) { ra.push({ loai: 'chu', t: t.slice(mo) }); break; }
    ra.push({ loai: 'toan', t: t.slice(mo + 1, dong) });
    i = dong + 1;
  }
  return ra.filter((x) => x.t !== '');
}

/* ── 2 · ĐỌC MỘT BIỂU THỨC LATEX ────────────────────────────────────────────
   Trả cây phẳng gồm: {k:'chu'} · {k:'phanso', tu, mau} · {k:'mu', goc, mu}
   Chỉ nhận những lệnh THẬT SỰ có trong sách; gặp lệnh lạ thì trả nguyên văn
   chứ không nuốt mất — thà bé thấy "\sqrt" còn hơn thấy chỗ trống. */
const KY_HIEU = {
  '\\times': '×', '\\div': ':', '\\cdot': '·', '\\%': '%',
  '\\le': '≤', '\\ge': '≥', '\\ne': '≠', '\\approx': '≈',
  '\\to': '→', '\\Rightarrow': '⇒', '\\pm': '±',
  '\\left(': '(', '\\right)': ')', '\\left[': '[', '\\right]': ']',
  '\\,': ' ', '\\;': ' ', '\\ ': ' ', '\\quad': '  ',
};

function docNhom(s, i) {
  /* Đọc phần nằm sau một lệnh: `{…}` cân ngoặc, hoặc đúng MỘT ký tự. */
  if (s[i] === '{') {
    let sau = 1, j = i + 1;
    while (j < s.length && sau > 0) {
      if (s[j] === '{') sau++;
      else if (s[j] === '}') sau--;
      if (sau > 0) j++;
    }
    return [s.slice(i + 1, j), j + 1];
  }
  return [s.slice(i, i + 1), i + 1];
}

export function docToan(bt) {
  const s = String(bt ?? '');
  const ra = [];
  let dem = '';
  const xa = () => { if (dem) { ra.push({ k: 'chu', t: dem }); dem = ''; } };
  let i = 0;
  while (i < s.length) {
    if (s[i] !== '\\') { dem += s[i++]; continue; }
    const lenh = s.slice(i).match(/^\\[a-zA-Z]+|^\\[^a-zA-Z]/);
    if (!lenh) { dem += s[i++]; continue; }
    const ten = lenh[0];
    if (ten === '\\frac' || ten === '\\dfrac' || ten === '\\tfrac') {
      xa();
      const [tu, j] = docNhom(s, i + ten.length);
      const [mau, k] = docNhom(s, j);
      ra.push({ k: 'phanso', tu: docToan(tu), mau: docToan(mau) });
      i = k;
      continue;
    }
    if (KY_HIEU[ten] !== undefined) { dem += KY_HIEU[ten]; i += ten.length; continue; }
    if (ten === '\\text' || ten === '\\mathrm') {
      const [noi, j] = docNhom(s, i + ten.length);
      dem += noi; i = j; continue;
    }
    dem += ten; i += ten.length;          // lệnh lạ: giữ nguyên, đừng nuốt
  }
  xa();

  /* Mũ và chỉ số đọc SAU cùng, trên chuỗi đã phẳng — `m^2` hay `a_1` chỉ bám
     vào đúng một ký tự hoặc một nhóm `{}`, nên xử ở đây gọn hơn trong vòng trên. */
  const ra2 = [];
  for (const o of ra) {
    if (o.k !== 'chu') { ra2.push(o); continue; }
    let t = o.t, vt = 0, dem2 = '';
    while (vt < t.length) {
      if (t[vt] === '^' || t[vt] === '_') {
        const tren = t[vt] === '^';
        const [noi, j] = docNhom(t, vt + 1);
        if (dem2) { ra2.push({ k: 'chu', t: dem2 }); dem2 = ''; }
        ra2.push({ k: tren ? 'mu' : 'chiso', t: noi });
        vt = j;
      } else dem2 += t[vt++];
    }
    if (dem2) ra2.push({ k: 'chu', t: dem2 });
  }
  return ra2;
}

/* ── 2b · LÀM ĐẸP PHÂN SỐ TRẦN, CHỈ LÚC VẼ ──────────────────────────────────
   `answerKey.value`, `choices`, `options`, `label` là DỮ LIỆU MÁY CHẤM: bộ chấm
   so khớp nguyên văn, nên bọc `$…$` vào đó là hỏng chấm điểm của mọi câu trắc
   nghiệm và mọi ô nhập. Nhưng chúng lại là thứ BÉ NHÌN THẤY — nút chọn in
   "3/4" nằm cạnh dòng văn đã có phân số xếp dọc, hai kiểu trên một màn.

   Nên dữ liệu giữ nguyên từng byte, còn ở đây — LÚC VẼ — đổi `a/b` trần thành
   phân số. Chỉ làm khi chuỗi CHƯA có `$` nào (tác giả chưa tự viết LaTeX).

   Chừa tỉ số điểm ("4/5 câu"): xếp dọc thì nó thành phân số, không còn là điểm. */
const R_PS_TRAN = /(?<![\d/$])(\d+)\s*\/\s*(\d+)(?![\d/])(?!\s*(câu|bài|điểm|ô)\b)/g;

export function tuDep(s) {
  const t = String(s ?? '');
  if (t.includes('$')) return t;
  return t.replace(R_PS_TRAN, (_, a, b) => `$\\frac{${a}}{${b}}$`);
}

/* ── 3 · ĐỌC MARKDOWN THEO DÒNG ─────────────────────────────────────────────
   Chỉ những thứ nội dung thật sự dùng. Cố ý KHÔNG nhận bảng, trích dẫn, liên
   kết: chưa dòng nào cần, mà nhận thừa thì mỗi thứ là một chỗ vẽ sai. */
export function docKhoi(s) {
  const dong = String(s ?? '').split('\n');
  const khoi = [];
  let ds = null;
  const dongDs = (kieu) => {
    if (!ds || ds.kieu !== kieu) { ds = { k: 'ds', kieu, muc: [] }; khoi.push(ds); }
    return ds;
  };
  for (const d of dong) {
    const t = d.trim();
    if (!t) { ds = null; continue; }
    let m;
    if ((m = t.match(/^#{1,4}\s+(.*)$/))) { ds = null; khoi.push({ k: 'de', t: m[1] }); continue; }
    if ((m = t.match(/^[-*•]\s+(.*)$/))) { dongDs('cham').muc.push(m[1]); continue; }
    if ((m = t.match(/^(\d+)[.)]\s+(.*)$/))) { dongDs('so').muc.push(m[2]); continue; }
    ds = null;
    khoi.push({ k: 'doan', t });
  }
  return khoi;
}

/** Cắt **đậm** · *nghiêng* · `mã` — chạy TRÊN phần chữ, sau khi đã tách LaTeX. */
export function docNhanManh(s) {
  const ra = [];
  const r = /(\*\*[^*]+\*\*|(?<![*\w])\*[^*\n]+\*(?![*\w])|`[^`]+`)/g;
  let cuoi = 0, m;
  while ((m = r.exec(String(s ?? '')))) {
    if (m.index > cuoi) ra.push({ k: 'chu', t: s.slice(cuoi, m.index) });
    const x = m[0];
    if (x.startsWith('**')) ra.push({ k: 'dam', t: x.slice(2, -2) });
    else if (x.startsWith('`')) ra.push({ k: 'ma', t: x.slice(1, -1) });
    else ra.push({ k: 'nghieng', t: x.slice(1, -1) });
    cuoi = m.index + x.length;
  }
  if (cuoi < String(s ?? '').length) ra.push({ k: 'chu', t: s.slice(cuoi) });
  return ra;
}
