/**
 * BÀI HỌC CUỐI BUỔI — cô giáo máy tự ngẫm lại buổi vừa rồi (mẫu Reflexion).
 *
 * ── VÌ SAO CẦN ──
 * V3 đã dựng chỗ CHỨA trí nhớ (`hosoai.js`) và `themBaiHoc` chờ sẵn, nhưng chưa ai
 * viết bài học vào đấy: trí nhớ của cô chỉ có những thứ suy được bằng code (chữ bé
 * hay sót, câu bé đã nói được). Thứ code không suy được là cái NHÌN RA từ cả buổi:
 * "con hay bỏ chữ 'a' trước danh từ", "con lẫn 'this' với 'that'". Một lượt gọi mô
 * hình cuối buổi làm được việc ấy.
 *
 * ── MỘT LƯỢT, CUỐI BUỔI, KHÔNG CHỜ ──
 * Không gọi giữa buổi: bé đang nói chuyện thì mỗi lời gọi thêm là một lần bé ngồi
 * đợi. Và không chờ kết quả ở chỗ gọi — mất mạng thì buổi vẫn kết bình thường, chỉ
 * là không có bài học nào. Đếm bằng `LOI_TOM_TAT`, không nuốt im.
 *
 * ── CÁI DỄ HỎNG NHẤT, VÀ VÌ SAO CÓ `soiBaiHoc` ──
 * Đây là chỗ DUY NHẤT trong cả môn mà một câu do mô hình viết được GHI LẠI và đọc
 * lại ở những buổi sau. Nó đi vào lời dặn, vào Góc bố mẹ, và sống năm buổi. Nên ba
 * thứ phải chặn ngay tại cửa:
 *
 *   1. NHẬN XÉT VỀ TÍNH CÁCH. "Bé lười nói" nằm trong hồ sơ một đứa trẻ sáu tuổi và
 *      bố mẹ đọc nó — đó là thứ không ai có quyền viết hộ. Chặn bằng danh sách từ.
 *   2. CHỮ ANH NGOÀI VỐN. Bài học đi vào lời dặn, nên một chữ lạ ở đây là tự tay mời
 *      mô hình dùng chữ bé chưa học — chọc thủng hàng rào TỪ BÊN TRONG, đúng chỗ
 *      `tienganh_sothich` đã canh cho sở thích.
 *   3. SỐ. Lời dặn rất dễ bị nhại nguyên văn, và "Con nói được 3/5 câu" đọc to lên
 *      trước mặt bé là một câu không ai muốn bé nghe. Quy ước này có từ `dongHoSo`.
 */
import { CO_DAU_VIET } from './chamviet.js';

/** Trần ký tự lời dặn tóm tắt. Nó là một lời dặn, nên chịu trần của lời dặn. */
export const TOM_TAT_TOI_DA_CHU = 1500;

/** Trần ký tự MỘT bài học — khớp với `BAI_HOC_TOI_DA_CHU` của `hosoai.js`. */
export const BAI_HOC_TOI_DA_CHU = 160;

/** Trần ký tự lời khen cuối buổi. */
export const KHEN_TOI_DA_CHU = 120;

/** Nhiều nhất mấy bài học một buổi. Nhiều hơn thì không còn là "điều đáng nhớ". */
export const BAI_HOC_MOI_BUOI = 3;

/**
 * TỪ CẤM — nói về CON NGƯỜI bé, không về việc học.
 *
 * ⚠ Danh sách này cố ý RỘNG và cố ý chặn cả từ nghe "nhẹ" ("chậm", "yếu"): đây là
 * hồ sơ một đứa trẻ sáu tuổi, bố mẹ đọc nó, và nó sống năm buổi. Chặn oan một bài
 * học hay thì mất một lời nhắc; để lọt một chữ thì dán nhãn cho một đứa trẻ.
 *
 * Soi theo TIẾNG, không theo chuỗi con — "kém" phải bắt được mà "kẹm"… thì không có,
 * nhưng "chậm" không được bắt oan "chậm rãi"? Bắt oan thì chịu: xem lập luận trên.
 */
export const TU_CAM = [
  'lười', 'kém', 'dốt', 'chậm', 'ngốc', 'đần', 'tệ', 'dở', 'yếu',
  'không thông minh', 'thiếu tập trung', 'lơ là', 'hư', 'nghịch',
  'buồn', 'chán', 'sợ', 'mệt', 'khó tính', 'nhút nhát',
];

/** Lời dặn cho lượt tóm tắt — bản nháp ở §9 mục C1 của bản rà 09-10. */
export function loiDanTomTat({ von, tenBe = 'con', lop = 1 } = {}) {
  const tu = [...(von?.loi?.tu || []), ...(von?.on || []).flatMap((x) => x.tu || [])];
  /* Bảng vốn CẮT NGẮN có chủ đích: lời dặn này chịu trần 1500, mà vốn lớp 5 mở rộng
     lên tới vài trăm mục. Phần trích tiếng Anh của bài học chỉ cần vài chữ, và
     `soiBaiHoc` soi lại bằng vốn ĐẦY ĐỦ — nên cắt ở đây không nới rào. */
  const bang = [];
  for (const t of tu) {
    const thu = bang.length ? `${bang.join(', ')}, ${t.tu}` : t.tu;
    if (thu.length > 420) break;
    bang.push(t.tu);
  }
  const than = [
    `You are reviewing a short English practice session of a Vietnamese child named ${tenBe}`
      + ` (grade ${lop}). The conversation is below.`,
    '',
    "Write, IN VIETNAMESE, for the teacher's private notebook:",
    `- "baiHoc": ${BAI_HOC_MOI_BUOI} short notes at most (each at most ${BAI_HOC_TOI_DA_CHU}`
      + ' characters) about SPECIFIC language mistakes that REPEATED — a missing word,',
    '  a swapped word order, a confused pair. One note, one mistake.',
    `- "khen": one sentence (at most ${KHEN_TOI_DA_CHU} characters) naming one thing she did well.`,
    '',
    'HARD RULES for every note:',
    '1. VIETNAMESE only. You may quote an English word in "double quotes", but the',
    `   quoted word MUST come from this list: ${bang.join(', ')}.`,
    '2. NO numbers, NO scores, NO percentages. Not even "3/5".',
    '3. NOTHING about the child as a person — not her character, her mood, her effort,',
    '   her attention. Only what the LANGUAGE did. Never words like "lazy" or "slow".',
    '4. ONE mistake, ONE note. Never write the same mistake twice with a different',
    '   word: "she forgets \'my\' before brother" and "…before mother" are the SAME',
    '   note. Say the mistake once, and name the words together if you must.',
    '5. If nothing repeated, return an empty list. An empty list is a good answer.',
    '',
    'Reply as JSON only: {"baiHoc":[{"chu":"…","nut":null}],"khen":"…"}',
  ].join('\n');
  return than.length > TOM_TAT_TOI_DA_CHU
    ? `${than.slice(0, TOM_TAT_TOI_DA_CHU - 3)}...` : than;
}

/**
 * Đọc câu trả lời. Mô hình được dặn trả JSON, nhưng KHÔNG được tin là nó luôn làm
 * đúng — "Sure! {…} bye" là chuyện thường. Cùng lối `docTraLoi` của phòng nói.
 */
export function docTomTat(chu) {
  const m = String(chu || '').match(/\{[\s\S]*\}/);
  if (!m) return null;
  try {
    const o = JSON.parse(m[0]);
    if (!o || typeof o !== 'object') return null;
    const ds = Array.isArray(o.baiHoc) ? o.baiHoc : [];
    return {
      baiHoc: ds.map((x) => (typeof x === 'string' ? { chu: x, nut: null }
        : { chu: String(x?.chu || ''), nut: x?.nut || null }))
        .filter((x) => x.chu.trim()),
      khen: String(o.khen || '').trim(),
    };
  } catch { return null; }
}

/* Mẩu trong ngoặc kép — chỗ mô hình trích lại chữ tiếng Anh. Cùng biểu thức với
   `loiVietHopLe` của phòng nói, và cùng lý do: đó là chỗ duy nhất tách được chắc. */
const MOC_NGOAC = /[""“”]([^""“”]+)[""“”]|(?<![\p{L}\p{N}])'([^']{2,})'(?![\p{L}\p{N}])/gu;
const chuTrongCau = (s) => String(s || '').toLowerCase().match(/[a-z']+/g) || [];

/**
 * SOI MỘT BÀI HỌC. Trả `{ ok, vi }` — `vi` là lý do khi bác.
 *
 * ⚠ BÁC THÌ BỎ HẲN BÀI HỌC ẤY, không sửa chữa nửa vời. Một câu đã nói sai về bé thì
 * sửa một chữ không cứu được, mà nó sẽ sống năm buổi trong hồ sơ.
 */
export function soiBaiHoc(chu, { von = null } = {}) {
  const s = String(chu || '').trim();
  if (!s) return { ok: false, vi: 'bài học rỗng' };
  if (s.length > BAI_HOC_TOI_DA_CHU) {
    return { ok: false, vi: `dài ${s.length} ký tự, quá trần ${BAI_HOC_TOI_DA_CHU}` };
  }

  /* ── SỐ ── Chặn cả "3/5" lẫn "70%". Lời dặn rất dễ bị nhại nguyên văn. */
  if (/\d/.test(s)) return { ok: false, vi: 'có chữ số — không nhắc điểm trước mặt bé' };

  /* ── TÍNH CÁCH ── Soi theo TIẾNG để "tệ" không bắt oan "tệp". */
  const xau = TU_CAM.find((x) => new RegExp(`(?<![\\p{L}])${x}(?![\\p{L}])`, 'iu').test(s));
  if (xau) return { ok: false, vi: `nhận xét về con người bé: "${xau}"` };

  /* ── PHẢI LÀ TIẾNG VIỆT ──
     Bài học là ghi chú cho sổ của cô và cho Góc bố mẹ đọc, nên nó phải là tiếng
     Việt. Một câu tiếng Anh thuần ("She forgets 'chips'") thì vừa sai người đọc,
     vừa bị `tachTheoTieng` đọc bằng GIỌNG VIỆT nếu lỡ đọc to lên — đúng luật "mỗi
     dòng một thứ tiếng" bác bắt sửa 13-08. */
  if (!CO_DAU_VIET.test(s)) {
    return { ok: false, vi: 'không phải tiếng Việt — bài học viết cho sổ của cô' };
  }

  /* ── CHỮ ANH NGOÀI VỐN ── Chỉ soi mẩu TRONG NGOẶC: ngoài ngoặc là tiếng Việt. */
  if (von) {
    const cho = new Set([
      ...[...(von.loi?.tu || []), ...(von.on || []).flatMap((x) => x.tu || [])]
        .flatMap((t) => [t.tu, t.so_nhieu, t.so_it, t.dang_ing, t.dang_qk]),
      ...[...(von.loi?.cau || []), ...(von.on || []).flatMap((x) => x.cau || [])]
        .map((c) => c.cau),
      ...(von.loi?.cauSach || []), ...(von.on || []).flatMap((x) => x.cauSach || []),
    ].filter(Boolean).flatMap((x) => chuTrongCau(x)));
    for (const m of s.matchAll(MOC_NGOAC)) {
      const trong = (m[1] ?? m[2] ?? '').trim();
      if (!trong || CO_DAU_VIET.test(trong)) continue;   // lời Việt, không phải chữ Anh
      const la = chuTrongCau(trong).find((w) => !cho.has(w));
      if (la) return { ok: false, vi: `trích chữ "${la}" không có trong bài` };
    }
  }
  return { ok: true, vi: '' };
}

/** Soi cả gói, trả về phần ĐÃ LỌC kèm những bài bị bỏ — để còn đếm được. */
export function soiGoiTomTat(tt, { von = null } = {}) {
  const giu = [];
  const boQua = [];
  /* ⚠ DỌN BÀI HỌC TRÙNG NHAU — đo thật 09-10 bắt được: mô hình trả về ba bài học
     cho CÙNG MỘT lỗi, chỉ khác cái từ bị bỏ ("thiếu 'my' trước brother" ·
     "…trước mother" · "…trước father"). Ba dòng chiếm chỗ trong lời dặn mà chỉ nói
     một điều, và `loiLap` của V3 đã nói điều ấy gọn hơn rồi.
     Đã siết lời dặn (luật 4), nhưng lời dặn là lời DẶN: chốt phải ở đây.
     ⚠ DẤU HIỆU TRÙNG LÀ KHUÔN CÂU TIẾNG VIỆT, không phải tập chữ trích. Phép soi
     đầu của tôi đòi hai bài học trích CÙNG tập chữ — mà ba bài trong phép đo trích
     ba tập khác nhau (`my|father` · `my|brother` · `father|mother`), nên nó không
     bắt được gì. Thứ GIỐNG nhau là lời Việt: bỏ hết phần trong ngoặc ra thì cả ba
     còn đúng một khuôn "Lặp lại thiếu từ trước trong câu". Đó mới là "cùng một
     lỗi"; mấy chữ trong ngoặc chỉ là chỗ lỗi ấy xảy ra. */
  const daCo = new Set();
  const dauVet = (chu) => String(chu)
    .replace(MOC_NGOAC, ' ')
    .replace(/[^\p{L}\s]/gu, ' ')
    .toLowerCase().replace(/\s+/g, ' ').trim();
  for (const b of (tt?.baiHoc || [])) {
    if (giu.length >= BAI_HOC_MOI_BUOI) break;
    const kq = soiBaiHoc(b.chu, { von });
    if (!kq.ok) { boQua.push({ ...b, vi: kq.vi }); continue; }
    const v = dauVet(b.chu);
    if (v && daCo.has(v)) { boQua.push({ ...b, vi: 'trùng lỗi với một bài học khác' }); continue; }
    if (v) daCo.add(v);
    giu.push(b);
  }
  /* Lời khen chịu đúng mấy luật ấy, chỉ khác cái trần. */
  const kKhen = tt?.khen
    ? soiBaiHoc(String(tt.khen).slice(0, BAI_HOC_TOI_DA_CHU), { von }) : { ok: false };
  return {
    baiHoc: giu,
    khen: kKhen.ok ? String(tt.khen).slice(0, KHEN_TOI_DA_CHU) : '',
    boQua,
  };
}
