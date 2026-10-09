/**
 * KẾ HOẠCH MỘT BUỔI — lập bằng CODE, không gọi mô hình (mẫu Plan-and-Execute).
 *
 * ── VÌ SAO CẦN ──
 * Trước bản này việc của từng lượt do `viecTiepTheo` xoay vòng theo SỐ LƯỢT: lượt
 * chẵn nói từ, lượt lẻ nói mẫu câu, cứ thế. Không ai — kể cả bé — biết buổi học này
 * gồm mấy việc và còn mấy việc. Bé sáu tuổi vào phòng, nói mười lượt, rồi buổi kết
 * vì hết ba lượt đạt liền: nó giống một cuộc trò chuyện tình cờ hơn là một buổi học.
 *
 * Nên lập sẵn 5–7 việc đầu buổi, bày ra cho bé thấy, rồi đi theo. Cô giáo biết hôm
 * nay dạy gì; bé biết còn mấy việc; và `tinhBuoi` có thêm một đích thật ("xong kế
 * hoạch") thay vì chỉ có hai cái phanh (hết giờ · ba lượt đạt liền).
 *
 * ── PLANNER LÀ CODE, KHÔNG PHẢI MÔ HÌNH ──
 * Thả cho mô hình lập kế hoạch thì nó lập một kế hoạch nghe rất hay rồi chọn từ
 * ngoài vốn của bé — đúng chỗ hỏng mà cả môn này đang dẹp. Mà kế hoạch thì suy
 * được hết từ `bangTrangThai` (V6): thẻ nào đến hạn, nút nào chông chênh, bé thích
 * gì. Suy bằng code thì không tốn lời gọi nào, chạy được bằng `node`, và cổng soi
 * được từng bước.
 *
 * ── KHÔNG BỎ GÌ CỦA BÀI ──
 * Kế hoạch chỉ XẾP THỨ TỰ và chọn KIỂU việc. Nó không bỏ từ nào, không bỏ mẫu câu
 * nào, và nhánh có kịch bản thì kịch bản vẫn đi trước — kế hoạch chỉ áp cho phần
 * luyện tự do.
 */
import { KIEU_VIEC, moiTuDuocDung } from './phongnoi.js';
import { NHOM, nhomCua, mucThaoCua } from './zpd.js';

/** Buổi có từ 5 tới 7 việc. Ít hơn thì không ra một buổi; nhiều hơn thì bé đuối. */
export const SO_BUOC = [5, 7];

/** Lập lại kế hoạch nhiều nhất bao nhiêu lần trong một buổi. */
export const REPLAN_TOI_DA = 2;

/** Sai mấy lần LIỀN ở cùng một bước thì hạ kiểu việc xuống bậc dễ hơn. */
export const SAI_DE_HA = 2;

/** Sai mấy lần thì chèn một bước phụ đạo và bỏ bước đang mắc. */
export const SAI_DE_PHU_DAO = 3;

/**
 * BA BẬC KHÓ, từ khó xuống dễ. Hạ bậc là đi sang PHẢI.
 *
 *   thay  cô đưa khuôn, bé thay từ vào        — khó nhất, bé phải hiểu khuôn
 *   mau   cô đọc cả câu, bé nhắc lại          — vừa
 *   tu    cô đọc một từ, bé nhắc lại          — dễ nhất, và là đường lui cuối
 *
 * ⚠ Dùng CHUNG `KIEU_VIEC` của `phongnoi.js`, không khai lại ba chuỗi ở đây: lệch
 * một chữ thì `dongViec` không nhận ra kiểu và lượt ấy ra lời dặn rỗng.
 */
export const BAC_KHO = [KIEU_VIEC.thay, KIEU_VIEC.mau, KIEU_VIEC.tu];

const haBac = (kieu) => {
  const i = BAC_KHO.indexOf(kieu);
  return i < 0 || i === BAC_KHO.length - 1 ? BAC_KHO[BAC_KHO.length - 1] : BAC_KHO[i + 1];
};

/** Trần ký tự một lý do. Nó hiện cho bé và bố mẹ đọc, nên phải ngắn. */
export const LY_DO_TOI_DA_CHU = 60;

const cat = (s) => {
  const t = String(s || '').trim();
  return t.length > LY_DO_TOI_DA_CHU ? `${t.slice(0, LY_DO_TOI_DA_CHU - 3)}...` : t;
};

/* Mẫu câu có ô tên người — dùng cho bước "nói về mình". */
const mauCoTen = (cau) => cau.find((c) => /\[[^\]]*(name|tên)[^\]]*\]/i.test(c.congThuc || ''));

/**
 * LẬP KẾ HOẠCH.
 *
 * @param bang  bảng trạng thái (V6) — thẻ đến hạn, mức thạo, sở thích, trí nhớ
 * @param von   vốn từ của buổi
 *
 * Thứ tự có ý: ÔN trước, MỚI sau, rồi mới tới hai bước "của riêng bé".
 *   1–2  ôn    thẻ đến hạn, hoặc nút chông chênh (ZPD) — thứ sắp quên đi trước
 *   2–3  mới   nút của chính bài này
 *   1    thay  thay thứ bé THÍCH vào khuôn — câu về chính bé
 *   1    veMinh nói một câu có TÊN bé
 *
 * ⚠ KHÔNG CÓ TỪ NÀO thì trả `null`, chứ không trả một kế hoạch rỗng: `viecTiepTheo`
 * phải rơi về xoay vòng như cũ, và một kế hoạch 0 bước thì `tinhBuoi` coi là "xong
 * ngay từ đầu" — buổi kết trước khi bé nói câu nào.
 */
export function lapKeHoach(bang, { von, bayGio = Date.now() } = {}) {
  const tu = [...(von?.loi?.tu || [])];
  const tuOn = (von?.on || []).flatMap((x) => x.tu || []);
  const cau = [...(von?.loi?.cau || [])];
  if (!tu.length) return null;

  const mucThao = bang?.mucThao || null;
  const thich = bang?.hoSo?.thich || null;
  const buoc = [];
  const them = (b) => { if (buoc.length < SO_BUOC[1]) buoc.push(b); };

  /* ── 1. ÔN ── Thẻ đến hạn đi TRƯỚC: cái sắp quên mới là cái đáng ôn, còn cái
     chưa học thì lúc nào học cũng được. `bang.theDenHan` là `null` khi màn hình
     không nạp thẻ — khác hẳn `[]` ("có nạp, không thẻ nào"), xem `dungBang`. */
  /* ⚠ ĐÒI PHẢI CÓ TỪ CỦA BÀI CŨ. Thiếu nó thì bước này dùng từ của bài HÔM NAY mà
     lý do vẫn ghi "ôn lại bài cũ sắp quên" — nói một điều không đúng với bé và với
     bố mẹ đọc thanh bước. Bé chưa đạt unit nào thì `von.on` rỗng (xem `vonTu`), và
     lúc ấy nhường cho nhánh chông chênh ở dưới. */
  if (tuOn.length) {
    for (const the of (bang?.theDenHan || []).slice(0, 2)) {
      const t = tuOn[buoc.length % tuOn.length];
      them({ loai: 'on', nut: the.microId || null, tu: t,
        mau: cau[0] || null, kieu: KIEU_VIEC.mau,
        lyDo: cat('Ôn lại bài cũ sắp quên') });
    }
  }
  /* Chưa đủ hai bước ôn thì lấy nút CHÔNG CHÊNH của bài — chỗ bé đang ở giữa,
     không phải chỗ đã thạo (ôn lại thì nhàm) cũng không phải chỗ chưa biết gì. */
  if (buoc.length < 2) {
    const chenh = tu.filter((t) => nhomCua(mucThaoCua(mucThao, t.ma)) === NHOM.chongChenh);
    for (const t of chenh.slice(0, 2 - buoc.length)) {
      them({ loai: 'on', nut: t.ma || null, tu: t, mau: cau[0] || null,
        kieu: KIEU_VIEC.mau, lyDo: cat('Chỗ con đang gần được') });
    }
  }

  /* ── 2. MỚI ── Nút của chính bài này, lấy từ đầu bài xuống (đúng thứ tự bé đã
     gặp ở chặng Từ mới, nên nghe quen tai). Bỏ những từ đã vào kế hoạch. */
  const daCo = new Set(buoc.map((b) => b.tu?.tu));
  const moi = tu.filter((t) => !daCo.has(t.tu));
  for (const [k, t] of moi.slice(0, 3).entries()) {
    them({ loai: 'moi', nut: t.ma || null, tu: t,
      mau: cau[k % Math.max(1, cau.length)] || null,
      kieu: cau.length ? KIEU_VIEC.mau : KIEU_VIEC.tu,
      lyDo: cat('Từ mới của bài hôm nay') });
  }

  /* ── 3. THỨ BÉ THÍCH ── Câu về CHÍNH BÉ, không phải câu về sữa của người khác. */
  const tThich = thich && tu.find((t) => t.tu === thich);
  if (cau.length) {
    them({ loai: 'thay', nut: (tThich || tu[0]).ma || null, tu: tThich || tu[0],
      mau: cau[0], kieu: KIEU_VIEC.thay,
      lyDo: cat(tThich ? `Nói về thứ con thích: ${thich}` : 'Thay từ khác vào khuôn câu') });
  }

  /* ── 4. NÓI VỀ MÌNH ── Mẫu có ô tên người nếu bài có; không thì một câu thường. */
  const mTen = mauCoTen(cau);
  if (mTen) {
    them({ loai: 'veMinh', nut: null, tu: tu[0], mau: mTen, kieu: KIEU_VIEC.thay,
      lyDo: cat('Nói một câu về chính con') });
  }

  /* ── ĐỦ SÀN 5 BƯỚC ── Thiếu thì đắp thêm từ của bài, kiểu dễ nhất. Bài ít từ
     (unit 1 có ba từ) thì đắp bằng chính mấy từ ấy ở bậc `tu` — nhắc lại một từ ở
     bậc dễ hơn vẫn là một việc thật, khác hẳn dựng một bước rỗng cho đủ số. */
  for (let i = 0; buoc.length < SO_BUOC[0]; i += 1) {
    const t = tu[i % tu.length];
    them({ loai: 'moi', nut: t.ma || null, tu: t, mau: null, kieu: KIEU_VIEC.tu,
      lyDo: cat(`Nhắc lại từ "${t.tu}"`) });
    if (i > 20) break;   // chặn vòng vô tận nếu `tu` rỗng bất thường
  }

  return {
    buoc: buoc.map((b, i) => ({ ...b, i: i + 1, trangThai: 'cho', sai: 0 })),
    tao: bayGio,
    soReplan: 0,
  };
}

/** Bước đang làm — bước ĐẦU TIÊN chưa xong và chưa bỏ. Hết thì `null`. */
export function buocHienTai(kh) {
  return (kh?.buoc || []).find((b) => b.trangThai === 'cho' || b.trangThai === 'dang') || null;
}

/** Kế hoạch đã xong hết chưa — `tinhBuoi` đọc cái này làm một đích thật. */
export const xongKeHoach = (kh) => !!kh?.buoc?.length && !buocHienTai(kh);

/**
 * CẬP NHẬT SAU MỘT LƯỢT — trả BẢN MỚI.
 *
 * Ba đường, và cả ba đều là đường ĐI TIẾP, không có đường nào bỏ bé lại:
 *   bé đúng            → bước xong, sang bước sau
 *   sai `SAI_DE_HA`    → HẠ BẬC kiểu việc (thay → mau → tu), vẫn ở bước ấy
 *   sai `SAI_DE_PHU_DAO` → bỏ bước ấy, chèn một bước PHỤ ĐẠO ở nút gốc rễ
 *
 * ⚠ TRẢ BẢN MỚI, không sửa tại chỗ. Kế hoạch nằm trong bảng trạng thái, mà bảng đi
 * vào `useMemo` của React — sửa tại chỗ thì màn hình không thấy nó đổi và thanh
 * bước đứng im. Cùng lý do với `ghiLuot`.
 *
 * ⚠ REPLAN CÓ TRẦN. Chèn phụ đạo mãi thì buổi phình ra vô hạn và bé không bao giờ
 * tới màn kết — đúng cái bẫy `buocSua` đã ghi ("mười lượt liền đều là Hello!").
 */
export function capNhatSauLuot(kh, { nhan = null, diem = null, bang = null, datNguong = 6 } = {}) {
  if (!kh?.buoc?.length) return kh;
  const b = buocHienTai(kh);
  if (!b) return kh;

  const dat = nhan === 'dung' || (Number.isFinite(diem) && diem >= datNguong);
  /* Mấy nhãn KHÔNG nói gì về việc bé làm được hay không (bé hỏi lại, bé nói tiếng
     Việt, bé im lặng) thì KHÔNG tính là một lần sai: trừ điểm bé vì nó hỏi cô một
     câu là dạy nó đừng hỏi nữa. */
  const khongTinh = new Set(['hoiLai', 'tiengViet', 'imLang', 'moDau']);
  if (!dat && khongTinh.has(nhan)) {
    return { ...kh, buoc: kh.buoc.map((x) => (x.i === b.i ? { ...x, trangThai: 'dang' } : x)) };
  }

  if (dat) {
    return { ...kh, buoc: kh.buoc.map((x) => (x.i === b.i ? { ...x, trangThai: 'xong' } : x)) };
  }

  const sai = (b.sai || 0) + 1;

  /* ── SAI ĐỦ NGƯỠNG → PHỤ ĐẠO ── */
  if (sai >= SAI_DE_PHU_DAO && (kh.soReplan || 0) < REPLAN_TOI_DA) {
    const goc = bang?.nutGocRe || b.nut || null;
    const them = { i: 0, loai: 'phuDao', nut: goc, tu: b.tu, mau: null,
      kieu: KIEU_VIEC.tu, lyDo: cat('Quay lại chỗ gốc của bài này'),
      trangThai: 'cho', sai: 0 };
    const ds = [];
    for (const x of kh.buoc) {
      if (x.i === b.i) { ds.push({ ...x, sai, trangThai: 'bo' }); ds.push(them); }
      else ds.push(x);
    }
    return { ...kh, soReplan: (kh.soReplan || 0) + 1,
      buoc: ds.map((x, i) => ({ ...x, i: i + 1 })) };
  }

  /* ── SAI ĐỦ NGƯỠNG → HẠ BẬC ── Hạ ở ĐÚNG mốc `SAI_DE_HA`, không hạ mỗi lần sai:
     hạ liên tục thì hai lần sai là về bậc dễ nhất và bé không bao giờ gặp lại khuôn
     câu. */
  const kieu = sai >= SAI_DE_HA ? haBac(b.kieu) : b.kieu;
  return { ...kh,
    buoc: kh.buoc.map((x) => (x.i === b.i
      ? { ...x, sai, kieu, trangThai: 'dang',
          mau: kieu === KIEU_VIEC.tu ? null : x.mau }
      : x)) };
}

/**
 * LỜI GIỚI THIỆU KẾ HOẠCH, giọng Việt, đọc to được cho bé nghe.
 *
 * ⚠ KHÔNG đọc tên từ tiếng Anh ra trong câu này. Nó được đọc bằng GIỌNG VIỆT (xem
 * `tachTheoTieng`), nên "Hôm nay mình tập school nhé" ra một thứ tiếng không phải
 * tiếng nào. Chỉ nói SỐ VIỆC và loại việc.
 */
export function loiGioiThieu(kh) {
  const n = kh?.buoc?.length || 0;
  if (!n) return '';
  const co = (l) => kh.buoc.some((b) => b.loai === l);
  const ke = [];
  if (co('on')) ke.push('ôn lại bài cũ');
  if (co('moi')) ke.push('học từ mới');
  if (co('thay')) ke.push('nói về thứ con thích');
  if (co('veMinh')) ke.push('nói một câu về chính con');
  return `Hôm nay mình làm ${n} việc nhé: ${ke.join(', ')}.`;
}

/** Dòng `THIS STEP` ghép vào lời dặn — tiếng Anh, ngắn, không số nào ngoài i/n. */
export function dongBuocKeHoach(kh) {
  const b = buocHienTai(kh);
  if (!b) return '';
  const n = kh.buoc.length;
  const khung = b.mau?.congThuc || b.mau?.cau || null;
  /* Mẫu câu đã mang dấu chấm của chính nó (`I like + [Noun].`), nên thêm một dấu
     nữa là ra `[Noun]..` — chi tiết nhỏ, nhưng lời dặn là thứ mô hình đọc từng ký
     tự và nó hay nhại lại nguyên văn. */
  return `THIS STEP (${b.i} of ${n}): practise the word "${b.tu?.tu}"`
    + (khung ? ` with the pattern ${khung}` : '.');
}

/** Thanh bước cho màn hình — một ô một việc. Dùng chung `ThanhViec.jsx`. */
export function oThanhViec(kh) {
  const BIEU_TUONG = { on: '🔁', moi: '✨', thay: '💛', veMinh: '🙋', phuDao: '🧩' };
  return (kh?.buoc || []).filter((b) => b.trangThai !== 'bo').map((b) => ({
    ma: `kh${b.i}`,
    nhan: b.tu?.tu || '—',
    nghia: b.lyDo,
    tt: b.trangThai === 'xong' ? 'xong' : b.trangThai === 'dang' ? 'dang' : 'chua',
    bieuTuong: BIEU_TUONG[b.loai] || '•',
    viecCon: [],
  }));
}

/** Còn mấy việc nữa — thanh bước hiện con số này. */
export const conThieu = (kh) => (kh?.buoc || [])
  .filter((b) => b.trangThai !== 'xong' && b.trangThai !== 'bo').length;
