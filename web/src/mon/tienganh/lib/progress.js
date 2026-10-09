/**
 * SỔ TIẾN ĐỘ TIẾNG ANH — lưu tại máy.
 *
 * Khoá RIÊNG, không dùng chung với Toán. Hai môn chung một khoá thì `micros` lẫn
 * vào nhau: mã bài `DL:TA1.B04` và `DL:KSN2.B04` khác nhau nên chưa trùng ngay,
 * nhưng mọi phép đếm "xong bao nhiêu bài" đều phải lọc theo tiền tố — và chỗ nào
 * quên lọc thì con số sai mà không ai biết. Tách khoá thì không có gì để quên.
 *
 * Và PHẢI TÁCH THEO CHỖ như bên Toán: máy tính bảng dùng chung cả nhà, mỗi bé một
 * "chỗ". Không tách thì em vừa đăng nhập đã thấy bài của anh.
 */
import { choDangDung, CHO_DAU } from '../../../chung/lib/nguoiDung.js';
import { ghiDinhDang } from './hoso.js';

const KEY_GOC = 'ttd5.tienganh.v1';
const khoa = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? KEY_GOC : `${KEY_GOC}.${cho}`;
};

export const soRong = () => ({
  micros: {}, chapters: {}, docHieu: {}, baiViet: {}, soThich: {},
  dinhDang: {},
  /* MỘT hồ sơ cho cả môn, KHÔNG theo bài — trí nhớ của cô giáo máy về bé (việc V3,
     `lib/hosoai.js`). Không khoá theo quyển vì nó nói về BÉ, không về quyển: bé hay
     sót chữ "a" thì sót ở mọi quyển, chia nhỏ ra chỉ làm mỗi mảnh không đủ dấu
     vết. Cùng lý do với `dinhDang`. */
  hoSoAI: null,
  updatedAt: null,
});

export function napTienDo(kho = globalThis.localStorage) {
  try {
    const raw = kho?.getItem(khoa());
    return raw ? { ...soRong(), ...JSON.parse(raw) } : soRong();
  } catch { return soRong(); }
}

export function luuTienDo(p, kho = globalThis.localStorage) {
  try { kho?.setItem(khoa(), JSON.stringify({ ...p, updatedAt: new Date().toISOString() })); }
  catch { /* chế độ riêng tư — bỏ qua, học vẫn chạy */ }
  return p;
}

/**
 * Ghi kết quả một bài.
 *
 * `best` giữ số câu đúng CAO NHẤT từ trước tới nay, không phải lần gần nhất: bé làm
 * lại bài đã đạt mà hôm ấy mệt, làm kém hơn, thì không được tụt sao đã có.
 */
export function ghiBai(p, id, kq) {
  const cu = p.micros[id] || {};
  return {
    ...p,
    micros: {
      ...p.micros,
      [id]: {
        done: true,
        pass: !!kq.pass || !!cu.pass,
        best: Math.max(cu.best || 0, kq.dung || 0),
        total: kq.tong || 0,
        /* Bậc cao nhất bé đã qua trong bài này — cái này mới là thứ đáng khoe với
           bố mẹ. "Xong bài" thì bé nào cũng xong; "gõ lại được cả câu" thì không. */
        bac: Math.max(cu.bac || 0, kq.bac || 0),
        attempts: (cu.attempts || 0) + 1,
        /* Làm hết bài rồi thì không còn "đang dở" nữa — xoá dấu chặng, nếu không
           bài đã đạt vẫn đội nhãn "đang học dở" trên danh sách. Xoá luôn `moc`:
           giữ lại thì lần sau mở bài ra làm lại, bé bị thả vào giữa mức cũ chứ
           không được bắt đầu từ đầu. */
        chang: 0,
        moc: undefined,
        at: new Date().toISOString(),
      },
    },
  };
}

/**
 * Đánh dấu bé đang học DỞ tới chặng nào của một bài.
 *
 * Ba điều cố ý ở đây:
 *
 * 1. KHÔNG đụng `at`. `gopTienDo` so `at` để quyết định bản nào thắng khi hoà sổ
 *    máy chủ; đổi `at` mỗi lần bé bấm sang chặng khác thì một buổi học dở trên máy
 *    này sẽ đè lên KẾT QUẢ THẬT đã ghi từ máy khác.
 *
 * 2. KHÔNG ghi khi `chang <= 0`. Chỉ mở bài ra xem rồi thoát thì không tạo mục —
 *    nếu không, mở lướt cả 16 bài là sổ đầy 16 mục "đang học dở" mà bé chưa học gì.
 *
 * 3. Chỉ giữ TẠI MÁY, không đẩy lên máy chủ. Đổi máy giữa chừng thì bé vào lại từ
 *    đầu bài — mất mấy phút, không mất bài nào. Đẩy lên thì phải ghi máy chủ mỗi
 *    lần bấm chặng, tốn mà chẳng đổi được gì.
 */
export function ghiChang(p, id, chang) {
  if (!(chang > 0)) return p;
  const cu = p.micros[id] || {};
  if ((cu.chang || 0) >= chang) return p;
  return { ...p, micros: { ...p.micros, [id]: { ...cu, chang } } };
}

/**
 * Nhớ chỗ đang dở BÊN TRONG một chặng — mức nào, câu thứ mấy, đúng mấy câu.
 *
 * ── VÌ SAO CẦN, VÀ VÌ SAO KHÔNG PHẢI `ghiChang` LÀ ĐỦ ──
 *
 * `ghiChang` chỉ nhớ ĐANG Ở CHẶNG NÀO. Trong chặng luyện tập còn ba mức, mỗi mức
 * chín câu, và toàn bộ chuyện ấy nằm trong `useState` của màn hình. Đi thử thật:
 * làm xong 9 câu mức ★, sang mức ★★, thoát ra, vào lại → về đúng chặng luyện tập
 * nhưng ★★ KHOÁ LẠI, ★ về "câu 1/9 · đúng 0/0". Bé phải làm lại cả mức. Với bé lớp
 * một thì bị mẹ gọi đi ăn cơm là mất một buổi học.
 *
 * ── BỐN ĐIỀU CỐ Ý ──
 *
 * 1. KHOÁ THEO CHẶNG. `moc` là một khối `{ tu: …, cau: …, luyen: … }`. Ghi chung
 *    một chỗ thì bé nhảy từ luyện tập về từ mới là xoá mất chỗ dở của chặng kia.
 *
 * 2. KHÔNG ĐỤNG `at`. Y như `ghiChang`: `gopTienDo` so `at` để chọn bản thắng khi
 *    hoà sổ máy chủ. Đổi `at` mỗi lần bé làm xong một câu thì một buổi học dở trên
 *    máy này sẽ đè lên KẾT QUẢ THẬT ghi từ máy khác.
 *
 * 3. KHÔNG ĐỔI THÌ TRẢ NGUYÊN KHỐI CŨ. Đây không phải chuyện tiết kiệm: vỏ gộp sổ
 *    thấy sổ đổi là vẽ lại, vẽ lại thì hàm `datTienDo` truyền xuống cũng mới, mà
 *    màn hình lại có effect canh chính hàm ấy để ghi mốc — thành vòng lặp không
 *    đáy. Đã vỡ thật một lần, xem `test/so_tien_do.test.mjs`.
 *
 * 4. CHỈ GIỮ TẠI MÁY. `luuBai` nhặt từng trường một khi đẩy lên máy chủ, và `moc`
 *    không nằm trong danh sách ấy — cố ý. Đổi máy giữa chừng thì bé vào lại từ đầu
 *    chặng, mất mấy phút chứ không mất bài nào.
 */
export function ghiMoc(p, id, chang, moc) {
  if (!chang) return p;
  const cu = p.micros[id] || {};
  const truoc = cu.moc || {};
  if (JSON.stringify(truoc[chang]) === JSON.stringify(moc)) return p;
  return {
    ...p,
    micros: { ...p.micros, [id]: { ...cu, moc: { ...truoc, [chang]: moc } } },
  };
}

/** Đọc mốc của một chặng. Trả `null` khi chưa có — màn hình tự dựng mặc định. */
export const docMoc = (p, id, chang) => p?.micros?.[id]?.moc?.[chang] || null;

/** Khoá chương PHẢI kèm mã quyển — khoá số trần làm huy hiệu lây giữa các quyển. */
export const khoaChuong = (ma, chuong) => `${ma}:C${chuong}`;

export function ghiChuong(p, ma, chuong, kq) {
  const k = khoaChuong(ma, chuong);
  const cu = p.chapters[k] || {};
  return {
    ...p,
    chapters: {
      ...p.chapters,
      [k]: {
        dat: !!kq.dat || !!cu.dat,
        best: Math.max(cu.best || 0, kq.dung || 0),
        tong: kq.tong || 0,
        at: new Date().toISOString(),
      },
    },
  };
}

/** Khoá bài đọc hiểu. Chữ D chứ không phải C — xem `ghiDocHieu`. */
/* `phamVi` tách bài của UNIT khỏi bài của CHƯƠNG: `ta3:D2` là bài đọc chương 2,
   `ta3:DU2` là bài đọc unit 2. Không tách thì hai bài khác hẳn nhau ghi đè lên nhau,
   và bé làm bài unit xong thì thẻ chương cũng sáng lên. Khoá của chương giữ NGUYÊN
   hình dạng cũ để sổ đang có trong máy bé không mất. */
export const khoaDocHieu = (ma, so, phamVi = 'chuong') =>
  `${ma}:D${phamVi === 'unit' ? 'U' : ''}${so}`;

/**
 * XONG MỘT BÀI ĐỌC HIỂU.
 *
 * ⚠ Ở BẢNG RIÊNG, KHÔNG nhét chung vào `chapters`.
 *
 * Nhét chung thì trông tiện — cùng hình dạng, cùng phạm vi một chương. Nhưng
 * `hocBaQuyen()` đếm huy hiệu chương bằng cách quét MỌI khoá bắt đầu bằng mã quyển:
 *
 *     chuongDat = Object.entries(chapters).filter(([k, v]) => k.startsWith('ta3:') && v.dat)
 *
 * Thêm năm khoá `ta3:D*` vào đó là sổ bố mẹ hiện "10/5 chương" — một con số vô
 * nghĩa, ở đúng chỗ bố mẹ tin nhất. Cùng dòng họ với cái bẫy "khoá chương phải kèm
 * mã quyển" đã sập một lần.
 *
 * Bài đọc hiểu CHƯA đẩy lên máy chủ: `hocBaTA` chỉ nhận `loai: 'chuong'`, và thêm
 * một `loai` là phải sửa cùng lúc `firestore.rules` · bên gửi · bên đọc, rồi deploy
 * rules. Bác chốt bài đọc hiểu không cần vào sổ, nên để tại máy — nhưng ghi rõ ở
 * đây rằng đó là một lựa chọn, không phải một chỗ sót.
 */
export function ghiDocHieu(p, ma, so, kq, phamVi = 'chuong') {
  const k = khoaDocHieu(ma, so, phamVi);
  const cu = (p.docHieu || {})[k] || {};
  return {
    ...p,
    docHieu: {
      ...(p.docHieu || {}),
      [k]: {
        dat: !!kq.dat || !!cu.dat,
        best: Math.max(cu.best || 0, kq.dung || 0),
        tong: kq.tong || 0,
        at: new Date().toISOString(),
      },
    },
  };
}

/** Khoá bài viết ngắn của một chương. */
export const khoaBaiViet = (ma, so, phamVi = 'chuong') =>
  `${ma}:V${phamVi === 'unit' ? 'U' : ''}${so}`;

/**
 * XONG MỘT BÀI VIẾT — giữ bài bé viết, điểm, và lời chấm.
 *
 * ⚠ GIỮ CẢ BÀI VIẾT, không chỉ điểm. Bác chốt "bố mẹ đọc được bài viết và lời
 * chấm": giữ mỗi con số thì bố mẹ mở sổ ra thấy "8/10" mà không biết con viết gì,
 * và cũng không biết máy chấm đúng hay sai. Con số một mình không kiểm tra được.
 *
 * ⚠ `nguon: 'ai'` ĐI KÈM MỌI CHỖ. Điểm này do máy chấm, và chỗ nào hiện nó ra cũng
 * phải nói điều đó. Một con số không nhãn trong sổ học bạ sẽ được đọc thành điểm
 * của cô giáo — đó là hiểu nhầm mà bố mẹ không có cách nào tự phát hiện.
 */
export function ghiBaiViet(p, ma, so, { viet, cham }, phamVi = 'chuong') {
  const k = khoaBaiViet(ma, so, phamVi);
  const cu = (p.baiViet || {})[k] || {};
  const diem = Number(cham?.diem);
  return {
    ...p,
    baiViet: {
      ...(p.baiViet || {}),
      [k]: {
        viet: String(viet || ''),
        diem: Number.isFinite(diem) ? diem : null,
        best: Math.max(cu.best || 0, Number.isFinite(diem) ? diem : 0),
        khen: cham?.khen || '',
        soLoi: (cham?.loi || []).length,
        choBoMe: cham?.choBoMe || '',
        nguon: 'ai',
        at: new Date().toISOString(),
      },
    },
  };
}

/** Khoá sở thích — MỘT mục cho cả quyển, không phải mỗi unit một mục. */
export const khoaSoThich = (ma) => `${ma}:ST`;

/**
 * BÉ THÍCH TỪ NÀO NHẤT — để cô giáo máy lấy đúng thứ ấy làm ngữ cảnh.
 *
 * Phòng nói xưa nay CÓ hỏi ("Con thích cái nào nhất?") và CÓ dùng — `dongHoSo()`
 * đưa thẳng vào lời dặn LLM. Nhưng câu trả lời chỉ sống trong `useState` của một
 * phiên: bé đóng màn là quên, mở lại là hỏi lại từ đầu. Đo theo mục 2.1.2 của
 * luận văn thì chiều Động lực chỉ đạt một nửa vì đúng chỗ này.
 *
 * ── MỘT MỤC CHO CẢ QUYỂN, VÀ VÌ SAO KHÔNG PHẢI MỖI UNIT MỘT MỤC ──
 * Mỗi unit một mục thì lại thành hỏi lại mỗi bài — không khác gì cũ. Vốn từ của
 * phòng nói là vốn TÍCH LUỸ (`vonTu()` gom cả unit trước), nên từ bé chọn ở unit
 * 3 vẫn nằm trong vốn khi bé học unit 12: nhớ một lần là dùng được cả quyển.
 *
 * ⚠ BÊN ĐỌC PHẢI SOI LẠI TỪ NÀY CÓ TRONG VỐN KHÔNG. Sổ sống lâu hơn nội dung:
 * đổi sách, dồn unit, hay bé mang sổ quyển này sang quyển khác thì từ nhớ được có
 * thể nằm NGOÀI vốn hiện tại — mà `dongHoSo()` nhét thẳng nó vào lời dặn LLM. Thế
 * là chính tầng chống ảo giác từ vựng bị mình chọc thủng từ bên trong. Chỗ soi
 * nằm ở `PhongNoi.jsx`, và cổng `tienganh_sothich.test.mjs` canh.
 */
export function ghiSoThich(p, ma, tu, unit = null) {
  const k = khoaSoThich(ma);
  return {
    ...p,
    soThich: {
      ...(p.soThich || {}),
      [k]: { tu: String(tu || ''), unit, at: new Date().toISOString() },
    },
  };
}

/**
 * BÉ LÀM TỐT DẠNG CÂU NÀO — chiều Sư phạm của mục 2.1.2.
 *
 * Cộng dồn theo `format` của câu. Luật cộng ở `lib/hoso.js` để cổng chạy được
 * bằng node; ở đây chỉ là chỗ cất.
 */
export function ghiDangCau(p, format, dung) {
  return { ...p, dinhDang: ghiDinhDang(p.dinhDang, format, dung) };
}

/** Gộp sổ tại máy với sổ trên máy chủ — bản nào MỚI HƠN thì thắng, từng bài một. */
export function gopTienDo(a, b) {
  if (!b) return a;
  const micros = { ...a.micros };
  for (const [k, v] of Object.entries(b.micros || {})) {
    const cu = micros[k];
    if (!cu || String(v.at || '') > String(cu.at || '')) micros[k] = v;
    else micros[k] = { ...v, ...cu, best: Math.max(cu.best || 0, v.best || 0),
                       bac: Math.max(cu.bac || 0, v.bac || 0) };
  }
  const chapters = { ...a.chapters };
  for (const [k, v] of Object.entries(b.chapters || {})) {
    const cu = chapters[k];
    if (!cu || String(v.at || '') > String(cu.at || '')) chapters[k] = v;
  }
  /* Bài viết cũng phải gộp, cùng luật "bản mới hơn thì thắng". Quên nó thì bé viết
     bài trên máy bảng, mở laptop ra là bài biến mất — mà bài viết là thứ bé bỏ công
     nhất trong cả quyển. */
  const baiViet = { ...(a.baiViet || {}) };
  for (const [k, v] of Object.entries(b.baiViet || {})) {
    const cu = baiViet[k];
    if (!cu || String(v.at || '') > String(cu.at || '')) baiViet[k] = v;
  }
  const soThich = { ...(a.soThich || {}) };
  for (const [k, v] of Object.entries(b.soThich || {})) {
    const cu = soThich[k];
    if (!cu || String(v.at || '') > String(cu.at || '')) soThich[k] = v;
  }
  /* ⚠ ĐỊNH DẠNG thì CỘNG hai bên, KHÔNG lấy bên mới hơn như mọi thứ khác. Đây là
     phép đếm tích luỹ: bé làm 40 câu trên máy bảng và 30 câu trên laptop thì hồ sơ
     phải là 70, chứ lấy "bản mới hơn" là vứt đi 40 câu. */
  const dinhDang = { ...(a.dinhDang || {}) };
  for (const [k, v] of Object.entries(b.dinhDang || {})) {
    const cu = dinhDang[k] || { dung: 0, tong: 0 };
    dinhDang[k] = { dung: cu.dung + (v.dung || 0), tong: cu.tong + (v.tong || 0) };
  }
  /* ⚠ HỒ SƠ AI gộp theo `capNhatLuc`, KHÔNG gộp hai bên như `dinhDang`. Nó là một
     BẢN CHỤP của cả trí nhớ, không phải phép đếm tích luỹ: trộn hai bản là ra một
     hồ sơ chưa từng tồn tại, với bài học của bản này và hạn dùng của bản kia. Lấy
     bản mới hơn thì cùng lắm mất một buổi, mà hình dạng thì luôn đúng. */
  const hoSoAI = (b.hoSoAI?.capNhatLuc || 0) > (a.hoSoAI?.capNhatLuc || 0)
    ? b.hoSoAI : (a.hoSoAI || b.hoSoAI || null);
  return { ...a, micros, chapters, baiViet, soThich, dinhDang, hoSoAI };
}
