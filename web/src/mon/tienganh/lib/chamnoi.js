/**
 * CHẤM BÀI NÓI — so lời bé đọc với câu mẫu, cho điểm trên thang 10.
 *
 * JS thuần, không đụng micro, không đụng React: mọi phép chấm ở đây kiểm được bằng
 * `node` mà không cần trình duyệt. Phần nghe nằm ở `nghenoi.js`.
 *
 * ── VÌ SAO KHÔNG SO CHUỖI THÔ ──
 * Máy nhận dạng tiếng nói (STT) trả về chữ đã qua tay nó: viết tắt bung ra
 * ("I'm" → "I am"), số thành chữ số ("six" → "6"), thêm dấu câu, thêm "um". Bé đọc
 * ĐÚNG mà so chuỗi thô thì trượt. Nên phải TIỀN XỬ LÝ cả hai vế về một dạng trước
 * khi so — đó là chỗ quyết định độ chính xác, không phải công thức chấm.
 *
 * ── VÀ VÌ SAO KHÔNG NỚI PHÁT ÂM QUÁ TAY ──
 * Cám dỗ lớn nhất là chấm thật rộng cho bé vui. Nhưng `dog` và `duck` là HAI TỪ
 * CÙNG MỘT UNIT: bé đọc nhầm sang từ kia mà vẫn 10 điểm thì bài nói thành vô nghĩa.
 * Nên bộ chấm nhận thêm danh sách TỪ ĐANG CẠNH TRANH (các từ khác của unit), và nếu
 * lời bé giống một từ khác hơn giống từ đích thì hạ điểm — kèm lời nói rõ bé vừa
 * đọc thành từ nào. Đó là phản hồi có ích, không phải lời chê.
 */

/* ─────────────────────────── TIỀN XỬ LÝ ─────────────────────────── */

/** Viết tắt → dạng đầy đủ. STT hay trả dạng đầy đủ, câu mẫu thì viết tắt. */
const VIET_TAT = [
  [/\bi'm\b/g, 'i am'], [/\bhe's\b/g, 'he is'], [/\bshe's\b/g, 'she is'],
  [/\bit's\b/g, 'it is'], [/\bthat's\b/g, 'that is'], [/\bthere's\b/g, 'there is'],
  [/\bwhat's\b/g, 'what is'], [/\bwe're\b/g, 'we are'], [/\bthey're\b/g, 'they are'],
  [/\byou're\b/g, 'you are'], [/\bcan't\b/g, 'cannot'], [/\bdon't\b/g, 'do not'],
  [/\bisn't\b/g, 'is not'], [/\blet's\b/g, 'let us'],
];

/**
 * DẠNG VIẾT TẮT KHÔNG CÓ DẤU NHÁY — bộ nhận dạng hay trả về như thế.
 *
 * Đã đo được: mẫu `"Hi, I'm Bill."` mà bé nói đúng y hệt, Web Speech trả về
 * `"hi im bill"` (không nháy) thì chỉ được 7/10. Bé nói ĐÚNG mà bị trừ điểm vì
 * cái máy gõ thiếu một dấu nháy — đó là chấm sai, không phải chấm chặt.
 *
 * Áp SAU khi đã bung dạng có nháy, và chỉ áp cho những chuỗi không thể là từ khác:
 * `im` `dont` `cant` `isnt` `lets` `thats` `theres` `whats` `youre` `theyre` `were`
 * — `were` CỐ Ý không có, vì nó là một từ thật ("they were here").
 */
const VIET_TAT_KHONG_NHAY = [
  [/\bim\b/g, 'i am'], [/\bhes\b/g, 'he is'], [/\bshes\b/g, 'she is'],
  [/\bits\b/g, 'it is'], [/\bthats\b/g, 'that is'], [/\btheres\b/g, 'there is'],
  [/\bwhats\b/g, 'what is'], [/\btheyre\b/g, 'they are'],
  [/\byoure\b/g, 'you are'], [/\bcant\b/g, 'cannot'], [/\bdont\b/g, 'do not'],
  [/\bisnt\b/g, 'is not'], [/\blets\b/g, 'let us'],
];

/** Chữ số → chữ. STT trả "6" cho "six", "2" cho "two". */
const SO_CHU = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
  'eight', 'nine', 'ten'];

/** Tiếng đệm khi bé ngập ngừng — bỏ đi, không tính là sai. */
const DEM = new Set(['um', 'uh', 'erm', 'hmm', 'ah', 'oh', 'er', 'eh', 'mm']);

/**
 * Đưa một câu về dạng so được. Cả câu mẫu lẫn lời bé đều đi qua đây.
 *
 * Thứ tự CÓ NGHĨA: bung viết tắt TRƯỚC khi bỏ dấu nháy, nếu không "I'm" thành
 * "im" và không còn khớp "i am" nữa.
 */
export function chuanHoa(s) {
  let t = String(s ?? '').normalize('NFC').toLowerCase();
  for (const [re, thay] of VIET_TAT) t = t.replace(re, thay);
  t = t.replace(/[’‘`´]/g, "'");
  for (const [re, thay] of VIET_TAT) t = t.replace(re, thay);   // sau khi gộp nháy
  t = t.replace(/(\d+)/g, (m) => (Number(m) <= 10 ? SO_CHU[Number(m)] : m));
  t = t.replace(/[^a-z0-9\s]/g, ' ');
  /* Sau khi dấu nháy đã bị bóc: bắt nốt dạng viết tắt KHÔNG nháy mà bộ nhận dạng
     hay trả về. Phải đứng SAU bước bóc dấu, nếu không "i'm" chưa kịp thành "im". */
  for (const [re, thay] of VIET_TAT_KHONG_NHAY) t = t.replace(re, thay);
  return t.split(/\s+/).filter((w) => w && !DEM.has(w)).join(' ');
}

export const tach = (s) => chuanHoa(s).split(' ').filter(Boolean);

/**
 * BỎ HẲN DẤU CÁCH ĐỂ SO — bác dặn 13-08, và đo ra lỗi thật.
 *
 * Bộ nhận dạng tách chỗ cách theo ý nó, không theo sách:
 *
 *     mẫu "teddy bear"  ·  máy nghe ra "teddybear"   → 9/10
 *     mẫu "goodbye"     ·  máy nghe ra "good bye"    → 9/10
 *
 * Bé nói đúng y hệt, chỉ khác chỗ cách — mà chỗ cách thì bé có nói ra đâu. Trừ
 * điểm ở đây là chấm cái máy gõ, không phải chấm bé.
 *
 * CHỈ dùng làm phép so BẰNG NHAU, không thay cho phép chấm từng từ: bỏ hết dấu
 * cách rồi đo độ giống thì "I like milk" và "Ilovemilk" hoá ra rất giống nhau, mà
 * chúng khác hẳn.
 */
export const bopCach = (s) => chuanHoa(s).replace(/ /g, '');
export const trungKhiBoCach = (a, b) => {
  const x = bopCach(a);
  return !!x && x === bopCach(b);
};

/* Từ CHỨC NĂNG — nghe khó, và sai một chữ ở đây không phải là chưa thuộc bài.
   Bé nói "This is dog" thay vì "This is a dog" thì vẫn đáng 8 điểm: nó nói được
   cái nó định nói. Thiếu DANH TỪ mới là chưa thuộc. */
const CHUC_NANG = new Set(['a', 'an', 'the', 'is', 'am', 'are', 'to', 'at', 'of',
  'my', 'your', 'his', 'her', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
  'this', 'that', 'there', 'can', 'do', 'does', 'and', 'not', 'us']);

/* ─────────────────────────── ĐỘ GIỐNG ─────────────────────────── */

/** Khoảng cách sửa (Levenshtein). Dùng cho cả ký tự lẫn mảng từ. */
export function khoangCach(a, b) {
  const m = a.length, n = b.length;
  if (!m) return n;
  if (!n) return m;
  let truoc = Array.from({ length: n + 1 }, (_, j) => j);
  for (let i = 1; i <= m; i += 1) {
    const nay = [i];
    for (let j = 1; j <= n; j += 1) {
      nay[j] = Math.min(
        truoc[j] + 1, nay[j - 1] + 1,
        truoc[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1),
      );
    }
    truoc = nay;
  }
  return truoc[n];
}

/** 0..1 — 1 là giống hệt. */
export function giongNhau(a, b) {
  const x = String(a), y = String(b);
  if (!x && !y) return 1;
  const d = khoangCach([...x], [...y]);
  return 1 - d / Math.max(x.length, y.length, 1);
}

/**
 * Dãy con chung dài nhất, theo TỪ — đo bé có giữ đúng THỨ TỰ không.
 * Thứ tự từ chính là ngữ pháp; nói đủ từ mà đảo lộn thì chưa phải nói được câu.
 */
function dayChung(a, b) {
  const m = a.length, n = b.length;
  const B = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 1; i <= m; i += 1) {
    for (let j = 1; j <= n; j += 1) {
      B[i][j] = a[i - 1] === b[j - 1]
        ? B[i - 1][j - 1] + 1
        : Math.max(B[i - 1][j], B[i][j - 1]);
    }
  }
  return B[m][n];
}

/* ─────────────────────────── CHẤM ─────────────────────────── */

/**
 * Điểm → BẬC. `loiKhen` chọn câu cô nói theo bậc, không theo điểm.
 *
 * ⚠ XUẤT RA từ V10: phần bỏ phiếu chỉnh điểm ±1 nên phải dựng lại bậc cho khớp.
 * Để bậc cũ lại thì điểm hiện 5 mà cô vẫn nói câu của bậc "tốt" — hai con số trên
 * cùng một thẻ nói hai điều khác nhau, và bé tin cái nào cũng sai.
 */
export const bacCua = (d) => (d >= 9 ? 'xuatSac' : d >= 7 ? 'tot' : d >= 5 ? 'kha' : d >= 3 ? 'gan' : 'chuaRo');
const BAC = bacCua;

/** Làm tròn về thang 10, không bao giờ âm, không bao giờ quá 10. */
const thang10 = (x) => Math.max(0, Math.min(10, Math.round(x * 10)));

/**
 * Chấm MỘT TỪ.
 *
 * @param dich   từ cần đọc, vd "dog"
 * @param nghe   lời STT nghe được, vd "the dog" hoặc "duck"
 * @param doiThu các từ khác CÙNG UNIT — để bắt việc bé đọc nhầm sang từ bên cạnh
 */
export function chamTu(dich, nghe, { doiThu = [] } = {}) {
  /* Chỉ khác chỗ cách thì coi như nói đúng — xem `bopCach`. */
  if (trungKhiBoCach(dich, nghe)) {
    return { diem: 10, dung: true, nghe: String(nghe ?? '').trim(), giong: 1, boCach: true };
  }
  const d = chuanHoa(dich);
  const tuNghe = tach(nghe);
  if (!tuNghe.length) return ket(0, 'khongNghe', { dich: d });

  /* Bé hay nói cả cụm ("it's a dog", "the dog"). Lấy từ khớp NHẤT trong câu bé nói
     chứ không so cả cụm — nói thừa không phải là nói sai. */
  let tot = 0, tuTot = tuNghe[0];
  for (const w of tuNghe) {
    const g = giongNhau(d, w);
    if (g > tot) { tot = g; tuTot = w; }
  }
  /* Cả cụm cũng thử, phòng từ ghép như "teddy bear". */
  const gCum = giongNhau(d, tuNghe.join(' '));
  if (gCum > tot) { tot = gCum; tuTot = tuNghe.join(' '); }

  /* ĐỌC NHẦM SANG TỪ BÊN CẠNH — chỗ tuyệt đối không được nới.
     `dog` và `duck` cùng một unit; nghe thành từ kia mà vẫn điểm cao thì bài nói
     mất hết ý nghĩa. So với TỪNG đối thủ, ai giống hơn thì bé đã đọc ra từ ấy. */
  let nhamThanh = null, gNham = 0;
  for (const x of doiThu) {
    const c = chuanHoa(x);
    if (c === d) continue;
    const g = Math.max(...tuNghe.map((w) => giongNhau(c, w)), giongNhau(c, tuNghe.join(' ')));
    if (g > gNham) { gNham = g; nhamThanh = c; }
  }
  if (nhamThanh && gNham > tot + 0.05) {
    /* Trần 3 điểm: bé CÓ nói, và nói rõ tới mức máy nhận ra một từ đã học — đáng
       ghi nhận, nhưng không phải từ đang hỏi. */
    return ket(Math.min(3, thang10(tot)), 'nhamTu',
      { dich: d, nghe: tuTot, nhamThanh, doGiong: tot });
  }

  /* ── TỪ CẠNH TRANH GẦN NHẤT — báo ra KỂ CẢ KHI NÓ KHÔNG THẮNG (việc V10) ──
     Nhánh `nhamTu` trên chỉ nổ khi từ bên cạnh thắng HẲN, và lúc ấy điểm bị ép trần
     3. Nên `nhamThanh` không bao giờ có mặt ở vùng điểm giữa — mà vùng giữa mới
     đúng là chỗ máy KHÔNG BIẾT bé nói từ nào: `dog` 0.62 với `duck` 0.58 thì hai
     chữ ấy thực chất ngang nhau, và bộ chấm đang chọn một trong hai bằng một con số
     lẻ sau dấu phẩy.
     Trước V10 chỗ ấy câm: bé được chấm theo từ đích, không ai hỏi lại. Nay nó được
     báo ra để phần bỏ phiếu còn biết có cái gì mơ hồ mà xử. Báo ra KHÔNG phải là
     trừ điểm — điểm trả về không đổi một ly. */
  return ket(thang10(tot), null, {
    dich: d, nghe: tuTot, doGiong: tot,
    doiThuGan: nhamThanh && tot - gNham <= GAN_NHAU
      ? { tu: nhamThanh, doGiong: gNham }
      : null,
  });
}

/**
 * Chấm MỘT CÂU.
 *
 * Ba phần, cộng lại thành 10:
 *   6 điểm  TỪ NỘI DUNG — danh từ, động từ, màu… Thiếu chúng là chưa nói được ý.
 *   2 điểm  THỨ TỰ      — đủ từ mà đảo lộn thì chưa phải một câu.
 *   2 điểm  TỪ CHỨC NĂNG — "a", "is", "the". Nghe khó nhất, nên nhẹ điểm nhất,
 *                          nhưng KHÔNG bỏ hẳn: chính chúng là chỗ bài đang dạy.
 */
export function chamCau(dich, nghe) {
  if (trungKhiBoCach(dich, nghe)) {
    return { diem: 10, dung: true, nghe: String(nghe ?? '').trim(), giong: 1, boCach: true };
  }
  const D = tach(dich);
  const N = tach(nghe);
  if (!N.length) return ket(0, 'khongNghe', { dich: D.join(' ') });
  if (!D.length) return ket(0, null, { dich: '' });

  const khop = (w, ds) => ds.some((x) => giongNhau(w, x) >= 0.8);
  const noiDung = D.filter((w) => !CHUC_NANG.has(w));
  const chucNang = D.filter((w) => CHUC_NANG.has(w));

  const dNoiDung = noiDung.length ? noiDung.filter((w) => khop(w, N)).length / noiDung.length : 1;
  const dChucNang = chucNang.length ? chucNang.filter((w) => khop(w, N)).length / chucNang.length : 1;
  const dThuTu = dayChung(D, N) / D.length;

  /* Nói THỪA nhiều thì trừ nhẹ — bé lan man chứ không sai. Trừ nặng là phạt oan
     đứa nói cả câu dẫn ("I think this is a dog"). */
  const thua = Math.max(0, N.length - D.length);
  const phatThua = Math.min(0.1, thua * 0.02);

  const diem = thang10(0.6 * dNoiDung + 0.2 * dThuTu + 0.2 * dChucNang - phatThua);
  const thieu = noiDung.filter((w) => !khop(w, N));
  return ket(diem, thieu.length ? 'thieuTu' : null, {
    dich: D.join(' '), nghe: N.join(' '), thieu,
    thieuChucNang: chucNang.filter((w) => !khop(w, N)),
  });
}

function ket(diem, ly, them) {
  return { diem, bac: BAC(diem), lyDo: ly, ...them };
}

/* ─────────────────────────── KHÍCH LỆ ─────────────────────────── */

/**
 * Lời cô nói sau khi chấm.
 *
 * Ba luật, rút từ chỗ bé 6 tuổi dễ bỏ cuộc nhất:
 *   1. NÓI CÁI ĐÚNG TRƯỚC. Kể cả khi sai, bé vẫn vừa làm được một việc: mở miệng
 *      nói tiếng Anh. Câu đầu tiên không bao giờ là lời chê.
 *   2. NÓI RÕ PHẢI SỬA GÌ, bằng một việc cụ thể — "đọc chậm lại chữ cuối", không
 *      phải "phát âm chưa chuẩn".
 *   3. SO VỚI CHÍNH BÉ LẦN TRƯỚC, không so với ai khác. Hơn lần trước là thắng.
 */
export function loiKhen(kq, lanTruoc = null) {
  const { diem, bac, lyDo } = kq;
  const hon = lanTruoc != null && diem > lanTruoc;

  if (lyDo === 'khongNghe') {
    return { sao: 0, chinh: 'Cô chưa nghe thấy gì.',
             them: 'Con bấm nút rồi nói to hơn một chút nhé.' };
  }
  if (lyDo === 'nhamTu') {
    return { sao: 1, chinh: `Con nói rõ lắm — nhưng đó là chữ “${kq.nhamThanh}”.`,
             them: `Lần này mình đọc “${kq.dich}” nhé. Nghe lại rồi thử tiếp.` };
  }

  const sao = diem >= 9 ? 3 : diem >= 7 ? 2 : diem >= 5 ? 1 : 0;
  const chinh = {
    xuatSac: 'Chuẩn luôn! Con đọc đúng rồi.',
    tot: 'Gần đúng hẳn rồi, cô nghe rõ lắm.',
    kha: 'Cô nghe ra rồi đấy.',
    gan: 'Con nói được rồi — mình sửa một chút thôi.',
    chuaRo: 'Cô nghe chưa rõ lắm.',
  }[bac];

  let them;
  if (kq.thieu?.length) them = `Lần sau nhớ nói cả chữ “${kq.thieu[0]}” nhé.`;
  else if (kq.thieuChucNang?.length) them = `Còn thiếu chữ nhỏ “${kq.thieuChucNang[0]}”.`;
  else if (diem >= 9) them = 'Con nói lại một lần nữa cho quen miệng nhé.';
  else them = 'Con nghe lại rồi đọc chậm hơn một chút nhé.';

  return { sao, chinh: hon ? `Hơn lần trước rồi! ${chinh}` : chinh, them };
}

/**
 * Chấm trên NHIỀU phương án máy nghe được, lấy phương án tốt nhất cho bé.
 *
 * Web Speech API trả về tới ba phương án. Với giọng trẻ con nói tiếng nước ngoài,
 * phương án đúng RẤT HAY không đứng đầu — máy đoán theo xác suất của người bản ngữ.
 * Chỉ đọc phương án đầu là phạt oan bé một cách có hệ thống.
 *
 * Lấy phương án tốt nhất KHÔNG phải là nới tay: bé chỉ được điểm cho cái bé thật sự
 * nói ra, chỉ là mình không bắt bé chịu thay cho lần đoán trượt của máy.
 */
export function chamTot(cham, dich, phuongAn, opt) {
  const ds = (Array.isArray(phuongAn) ? phuongAn : [phuongAn]).filter((x) => x != null);
  if (!ds.length) return cham(dich, '', opt);
  let tot = null;
  for (const x of ds) {
    const k = cham(dich, x, opt);
    /* `nghe` — CHÍNH phương án được chấm điểm này. Màn hình phải hiện và lưu đúng
       câu ấy: hiện phương án đầu mà điểm là của phương án khác thì thẻ nói dối. */
    if (!tot || k.diem > tot.diem) tot = { ...k, nghe: x };
  }
  return { ...tot, soPhuongAn: ds.length };
}

/** Đạt hay chưa — ngưỡng thấp có chủ ý, vì đây là lần ĐẦU bé nói tiếng Anh. */
export const DAT = 6;
export const datNoi = (diem) => diem >= DAT;

/* ═══════════════════ VÙNG MƠ HỒ, VÀ AI ĐƯỢC XỬ (việc V10) ═══════════════════ */

/**
 * Hai chữ coi là NGANG NHAU khi độ giống của chúng cách nhau không quá chừng này.
 *
 * ⚠ Con số này quyết định phần bỏ phiếu có chạy hay không, nên nó phải là hằng xuất
 * ra và có cổng canh. Nới rộng là gọi mô hình cho cả những lượt máy đã biết rõ (tốn
 * lượt gọi, chậm cho bé); thu hẹp là phần bỏ phiếu lại câm như trước V10.
 */
export const GAN_NHAU = 0.15;

/**
 * VÙNG MƠ HỒ — chỉ ở trong khoảng này mới được nhờ mô hình phân xử.
 *
 * Dưới 5: máy nghe chẳng ra gì giống từ nào, phân xử cũng chỉ là đoán. Trên 7: máy
 * đã nghe rõ, hỏi thêm là mời một ý kiến thứ hai vào chỗ không cần.
 *
 * ⚠ VÀ NÓ CHỨA ĐÚNG NGƯỠNG `DAT` (6) Ở GIỮA. Đó là chủ ý, không phải tình cờ:
 * phiếu chỉ đổi điểm ±1 trong [5, 7], nên chỗ duy nhất nó đổi được kết cục là
 * quanh 6 — đúng chỗ bộ chấm đang phải quyết "đạt / chưa đạt" bằng một con số lẻ.
 * Ngoài khoảng ấy, phiếu không được phép lật gì cả.
 */
export const VUNG_MO_HO = [5, 7];
export const vungMoHo = (d) => Number.isFinite(d) && d >= VUNG_MO_HO[0] && d <= VUNG_MO_HO[1];

/**
 * Lượt này có đáng nhờ mô hình phân xử không?
 *
 * Ba điều phải đủ cả: điểm trong vùng mơ hồ · có một từ cạnh tranh ở gần · và máy
 * có nghe được tiếng. Thiếu một là giữ nguyên điểm và KHÔNG gọi mạng.
 */
export function moHoCanBoPhieu(kq) {
  if (!kq || kq.lyDo === 'khongNghe' || kq.lyDo === 'nhamTu') return false;
  if (!kq.doiThuGan?.tu) return false;
  return vungMoHo(kq.diem);
}

/**
 * Áp phiếu vào điểm. Thuần, không mạng — nên cổng canh được mọi ca biên.
 *
 * ⚠ KẸP LẠI TRONG `VUNG_MO_HO`. Phiếu là bằng chứng YẾU: hai lượt gọi cùng một mô
 * hình, cùng một lời dặn. Cho nó kéo điểm xuống 2 hay lên 9 là để một phép đoán
 * quyết cả bài. Trong [5, 7] thì nó chỉ nhích đúng một bậc — đủ lật "đạt / chưa",
 * không đủ để thành lời phán.
 *
 * ⚠ `Number(null) === 0` VÀ `Number.isFinite(0) === true`. Cái bẫy này đã cắn hai
 * lần ở `hocba.js` (xem `soHoacNull`): điểm chưa có mà đi qua phép kẹp thì ra 0, và
 * 0 trông như một điểm thật. Nên chặn `null`/`undefined` TRƯỚC khi đổi sang số.
 */
export function apDungPhieu(diem, dieuChinh) {
  if (diem == null) return diem;
  const d = Number(diem);
  if (!vungMoHo(d)) return d;
  const b = dieuChinh == null ? 0 : Number(dieuChinh);
  if (!Number.isFinite(b) || b === 0) return d;
  const moi = d + Math.sign(b);
  return Math.max(VUNG_MO_HO[0], Math.min(VUNG_MO_HO[1], moi));
}
