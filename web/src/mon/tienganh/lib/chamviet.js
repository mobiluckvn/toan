/**
 * BÀI VIẾT NGẮN — LUẬT THUẦN của phần chấm bằng AI.
 *
 * Ba tầng như phòng luyện nói, và tách vì cùng một lý do: tệp này chạy được bằng
 * `node` (cổng `tienganh_chamviet.test.mjs` gọi thẳng), không biết gì về mạng lẫn
 * về React.
 *
 *     chamviet.js       luật · bóc lời chấm · SOI lại lời chấm     ← tệp này
 *     goiChamViet.js    gọi máy chủ, ghi học bạ
 *     VietBai.jsx       vẽ
 *
 * ── VÌ SAO PHẢI SOI LẠI LỜI CHẤM ──
 * Máy chấm được dặn rất rõ: chỉ dùng từ trong bảng vốn đã học. Nhưng dặn dò là thứ
 * mô hình *có thể* theo — cả môn này đã trả giá hai lần (sinh `"Bye, bike."` sau
 * khi được dặn ô ấy là tên người; nói lặp y một câu ngay sau khi được dặn đừng
 * lặp). Bé tám tuổi đọc lời chấm là tin, nên một câu sửa chứa từ chưa học thì
 * không phải "gợi ý hay hơn", nó là DẠY MỘT THỨ BÉ KHÔNG CÓ CÁCH NÀO HIỂU.
 *
 * Nên: chữ lạ trong câu sửa hay trong gợi ý thì GẮN CỜ. Màn hình vẫn hiện lời khen
 * và điểm, nhưng phần có chữ lạ bị giấu đi và nói rõ vì sao — thà thiếu một gợi ý
 * còn hơn dạy sai.
 */

/** Điểm tối đa. Trùng với thang bé quen ở trường. */
export const DIEM_TOI_DA = 10;

/** Ghi rõ ai chấm — con số không nhãn là con số sẽ bị đọc nhầm thành điểm cô giáo. */
export const NGUON_CHAM = 'ai';

/**
 * Bóc lời chấm từ chữ máy chủ trả về.
 *
 * Mô hình được dặn trả JSON, nhưng KHÔNG được tin là nó luôn làm đúng — cùng lối
 * với `docTraLoi()` của phòng luyện nói. Bóc không ra thì trả `null` để chỗ gọi
 * nói "chưa chấm được, con thử lại", chứ đừng dựng một lời chấm rỗng.
 */
export function docLoiCham(chu) {
  const s = String(chu || '').trim();
  const json = s.match(/\{[\s\S]*\}/);
  if (!json) return null;
  let o;
  try { o = JSON.parse(json[0]); } catch { return null; }
  if (!o || typeof o !== 'object') return null;

  const diem = Number(o.diem);
  return {
    /* Điểm ngoài thang thì KẸP về thang, đừng vứt cả lời chấm: mô hình trả 95 (thang
       100) là chuyện xảy ra được, và lúc ấy phần khen với phần sửa vẫn dùng tốt. */
    diem: Number.isFinite(diem)
      ? Math.max(0, Math.min(DIEM_TOI_DA, Math.round(diem)))
      : null,
    khen: String(o.khen || '').trim(),
    loi: (Array.isArray(o.loi) ? o.loi : []).map((x) => ({
      cau: String(x?.cau || '').trim(),
      sua: String(x?.sua || '').trim(),
      viSao: String(x?.viSao || x?.vi_sao || '').trim(),
    })).filter((x) => x.cau || x.sua),
    goiY: String(o.goiY || o.goi_y || '').trim(),
    choBoMe: String(o.choBoMe || o.cho_bo_me || '').trim(),
  };
}

/** Chữ tiếng Anh trong một câu, thường hoá. Dấu nháy giữ lại: `I'm` là một chữ. */
export const chuTiengAnh = (s) => String(s || '').toLowerCase().match(/[a-z']+/g) || [];

/**
 * Những chữ KHÔNG nằm trong vốn từ đã học.
 *
 * Vốn từ gồm cả CỤM nhiều chữ (`thank you` · `art room` · `teddy bear`), nên phải
 * rải cụm ra thành từng chữ — so nguyên cụm thì `thank` và `you` đều thành chữ lạ.
 *
 * Và phải cộng thêm chữ trong MẪU CÂU: công thức của sách có `is` · `are` · `the` ·
 * `your` mà bảng từ vựng không khai — chúng là chữ bé gặp mỗi ngày trong bài, chỉ
 * là không phải "từ mới" của unit nào.
 */
/**
 * GỐC CỦA MỘT CHỮ BIẾN HÌNH — `friends` → `friend`, `playing` → `play`/`playe`.
 *
 * ⚠ ĐÂY LÀ CHỖ NỚI HÀNG RÀO, nên nới hẹp nhất có thể. Trả về mấy GỐC CÓ THỂ, rồi
 * `chuLa` chỉ tha khi một gốc ấy THẬT SỰ có trong vốn. Không có gốc nào trúng thì
 * chữ vẫn là chữ lạ: `has` không lọt nhờ `ha`, `the` không lọt nhờ gì cả.
 *
 * ── VÌ SAO PHẢI CÓ ──
 * Đi thử bản thật 10-10-2026: bé viết *"I can see two friend"*, mô hình sửa đúng
 * thành *"two friends"*, rồi `friends` bị bác vì bảng vốn chỉ khai `friend` — câu
 * sửa bị bỏ, và bé nhận điểm 6/10 kèm câu "cô không tìm thấy lỗi nào trong bài của
 * con". Dạy đúng cái đuôi `-s` ấy CHÍNH LÀ việc của lời chấm; gọi nó là "từ mới"
 * thì phần sửa lỗi ngữ pháp không bao giờ tới được bé.
 */
export function gocBienHinh(w) {
  const s = String(w || '');
  const ra = [];
  if (s.endsWith("'s") && s.length > 3) ra.push(s.slice(0, -2));
  if (s.endsWith('ies') && s.length > 4) ra.push(`${s.slice(0, -3)}y`);
  if (s.endsWith('es') && s.length > 3) ra.push(s.slice(0, -2));
  if (s.endsWith('s') && s.length > 2) ra.push(s.slice(0, -1));
  if (s.endsWith('ing') && s.length > 4) ra.push(s.slice(0, -3), `${s.slice(0, -3)}e`);
  if (s.endsWith('ed') && s.length > 3) ra.push(s.slice(0, -2), s.slice(0, -1));
  return ra;
}

export function chuLa(cau, { vonTu = [], mauCau = [], beViet = '' } = {}) {
  const kho = new Set();
  for (const v of vonTu) chuTiengAnh(typeof v === 'string' ? v : v?.tu).forEach((w) => kho.add(w));
  for (const m of mauCau) chuTiengAnh(m).forEach((w) => kho.add(w));
  /* ── CHỮ CHÍNH BÉ VỪA VIẾT ──
     Câu sửa là câu bé viết được viết lại cho đúng, nên những chữ bé vừa dùng không
     thể là "chữ bé chưa học" — hàng rào này dựng lên để chặn mô hình DẠY từ mới,
     không phải để chặn nó nhắc lại từ bé vừa viết. Bỏ vế này thì ở Unit 1 cả
     `the` · `at` · `school` · `gate` — bốn chữ bé tự gõ ra — đều bị kể là chữ lạ,
     và mọi câu sửa đều rơi. */
  for (const w of chuTiengAnh(beViet)) kho.add(w);
  return chuTiengAnh(cau)
    .filter((w) => !kho.has(w) && !gocBienHinh(w).some((g) => kho.has(g)));
}

/** Dấu tiếng Việt — dấu hiệu chắc chắn nhất một mẩu chữ là lời Việt, không phải câu Anh. */
export const CO_DAU_VIET = /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i;

/**
 * Chữ lạ trong một câu TIẾNG VIỆT có lẫn tiếng Anh (lời gợi ý, lời giải thích).
 *
 * ⚠ ĐỪNG đem cả câu đi so với vốn từ tiếng Anh. "Con thử viết thêm câu cảm ơn:
 * Thank you." — mọi chữ Việt trong đó (`con` · `thu` · `viet` · `them`…) đều "không
 * có trong vốn từ", và lời gợi ý ĐÚNG lại bị bỏ. Đã sập ngay trong lượt thử đầu.
 *
 * Nên chỉ soi những MẨU không mang dấu tiếng Việt — đúng lối `loiVietHopLe()` của
 * phòng luyện nói đang dùng, và cùng một lý do.
 */
export function chuLaTrongViet(cau, kho) {
  const mau = String(cau || '').split(/[:.;“”"'()\n]|(?:\s-\s)/);
  const ra = [];
  for (const m of mau) {
    const s = m.trim();
    if (!s || CO_DAU_VIET.test(s) || !/[a-z]/i.test(s)) continue;
    ra.push(...chuLa(s, kho));
  }
  return [...new Set(ra)];
}

/**
 * Soi lời chấm, trả về bản ĐÃ LỌC kèm danh sách chỗ bị bỏ.
 *
 * Bỏ ĐÚNG phần hỏng, giữ lại phần lành: một câu sửa có chữ lạ thì bỏ câu sửa ấy
 * thôi, lời khen và điểm vẫn còn. Vứt cả lời chấm vì một chữ là bé mất luôn phần
 * nó xứng đáng được nghe.
 */
export function soiLoiCham(cham, { vonTu = [], mauCau = [], beViet = '' } = {}) {
  if (!cham) return { cham: null, boQua: [] };
  const boQua = [];
  /* `beViet` — bài CHÍNH BÉ vừa viết. Phải chuyền tới đây, nếu không máy chủ soi
     bằng một kho rộng hơn máy con, rồi máy con bỏ mất đúng mục máy chủ vừa duyệt
     — hai bên đều báo mình đúng mà bé thì thấy lời chấm thiếu. */
  const kho = { vonTu, mauCau, beViet };
  /* Câu SỬA là tiếng Anh thuần — soi trọn câu. Lời GỢI Ý là tiếng Việt có lẫn
     tiếng Anh — chỉ soi mẩu tiếng Anh trong đó. Hai phép khác nhau vì hai thứ chữ
     khác nhau; dùng chung một phép thì hoặc bỏ oan lời Việt, hoặc thả lọt câu Anh. */
  const sach = (s, viet = false) => {
    const la = viet ? chuLaTrongViet(s, kho) : chuLa(s, kho);
    return la.length ? (boQua.push({ cau: s, chuLa: la }), '') : s;
  };
  const loi = cham.loi.map((x) => {
    /* ⚠ Mô hình ĐƯỢC PHÉP để `sua` rỗng (luật 5 của lời dặn, nhánh xin lại). Bản
       trước lọc thẳng mục ấy đi và không đếm vào `boQua` — thế là màn hình nói
       "cô không tìm thấy lỗi nào trong bài của con" kèm một con điểm dưới 10, hai
       câu chọi nhau. Đếm nó vào `boQua` thì bé đọc được "cô có giấu một chỗ", đúng
       sự thật. Bắt được khi đi thử bản thật 10-10-2026. */
    if (!String(x?.sua || '').trim()) {
      boQua.push({ cau: String(x?.cau || ''), chuLa: [] });
      return { ...x, sua: '' };
    }
    return { ...x, sua: sach(x.sua) };
  })
    /* Lỗi mà câu sửa bị bỏ thì còn lại "câu con viết sai" và không có câu đúng —
       chỉ ra chỗ sai rồi bỏ đó còn tệ hơn không nói. Bỏ cả mục. */
    .filter((x) => x.sua);
  return {
    cham: { ...cham, loi, goiY: sach(cham.goiY, true) },
    boQua,
  };
}

/**
 * Bài viết có ĐỦ SỐ CÂU chưa — chặn ngay tại máy con, trước khi tốn một lượt gọi.
 *
 * Đếm bằng dấu chấm câu, và câu cuối không có dấu vẫn tính: bé tám tuổi quên dấu
 * chấm là chuyện thường, mà chặn vì cái đó thì bé không hiểu mình sai gì.
 */
export function demCau(viet) {
  return String(viet || '').split(/[.!?]+/).map((x) => x.trim()).filter(Boolean).length;
}

export function duocGui(viet, toiThieu = 2) {
  const chu = String(viet || '').trim();
  if (!chu) return { ok: false, vi: 'Con viết vài câu rồi cô chấm cho nhé.' };
  if (demCau(chu) < toiThieu) {
    return { ok: false, vi: `Con viết ít nhất ${toiThieu} câu nhé.` };
  }
  return { ok: true, vi: '' };
}
