/**
 * TIẾN ĐỘ HỌC — lưu tại máy (localStorage) ở giai đoạn B.
 * Giai đoạn C sẽ đồng bộ lên Firestore nhưng GIỮ NGUYÊN hình dạng dữ liệu này.
 */
import { allMicroIds, chapterOf } from './noiDung.js';
import { chuongTrinhCua } from '../../../chung/lib/soQuyen.js';
import { choDangDung, CHO_DAU } from '../../../chung/lib/nguoiDung.js';
import { chuyenSo } from './donSoLop4.js';

/**
 * Khoá sổ tiến độ tại máy — RIÊNG CHO TỪNG BÉ.
 *
 * Máy tính bảng dùng chung cả nhà: anh lớp 5 và em lớp 2 mỗi bé một tài khoản, nhưng
 * sổ tại máy trước đây dùng CHUNG một khoá. Em vừa đăng nhập là thấy ngay "đã học
 * xong 2 trên 33 bài" của anh — hai sổ trộn vào nhau, và bé nào học sau thì đè lên
 * bé học trước.
 *
 * Chỗ ĐẦU giữ nguyên khoá cũ `ttd5.progress.v1`: máy đang dùng từ trước bản này có
 * cả sổ ở đó, đổi khoá là bé đang học mất sạch bài trong mắt mình.
 */
const KEY_GOC = 'ttd5.progress.v1';
const khoa = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? KEY_GOC : `${KEY_GOC}.${cho}`;
};

export const emptyProgress = () => ({ micros: {}, chapters: {}, gio: {}, updatedAt: null });

/**
 * SỔ GIỜ TẠI MÁY, cộng dồn theo NGÀY — `{ '2026-08-17': {giay, giayXem, giayLam, luot} }`.
 *
 * Vì sao giữ một bản ở máy khi máy chủ đã có: bé chưa đăng nhập vẫn phải thấy số
 * phút của mình, và bé đã đăng nhập cũng không nên phải chờ hàm chạy đêm mới biết
 * hôm nay mình học bao lâu. Sổ máy chủ trả lời cho bố mẹ và cô giáo; sổ này trả lời
 * cho chính bé, ngay lập tức.
 *
 * Cắt còn `SO_NGAY_GIU` ngày gần nhất: sổ tại máy nằm trong localStorage, để nó phình
 * mãi thì đến lúc nào đó ghi hỏng, mà ghi hỏng ở đây là mất luôn cả tiến độ học.
 */
export const SO_NGAY_GIU = 60;

export function congGio(progress, ngay, gio) {
  if (!gio || !gio.giay) return progress;
  const cu = progress.gio?.[ngay] || { giay: 0, giayXem: 0, giayLam: 0, luot: 0 };
  const moi = {
    ...(progress.gio || {}),
    [ngay]: {
      giay: cu.giay + gio.giay,
      giayXem: cu.giayXem + (gio.giayXem || 0),
      giayLam: cu.giayLam + (gio.giayLam || 0),
      luot: cu.luot + 1,
    },
  };
  const giu = Object.keys(moi).sort().slice(-SO_NGAY_GIU);
  return { ...progress, gio: Object.fromEntries(giu.map((k) => [k, moi[k]])) };
}

/** Phút học của một ngày (mặc định hôm nay) — 0 khi chưa học. */
export const phutNgay = (progress, ngay) =>
  Math.round(((progress?.gio || {})[ngay]?.giay || 0) / 60);

/** Phút học cộng dồn `n` ngày gần nhất, tính cả hôm nay. */
export function phutGanDay(progress, dsNgay) {
  const g = progress?.gio || {};
  return Math.round(dsNgay.reduce((s, n) => s + (g[n]?.giay || 0), 0) / 60);
}

export function loadProgress(storage = globalThis.localStorage) {
  try {
    const raw = storage?.getItem(khoa());
    if (!raw) return emptyProgress();
    /* ⚠ CHUYỂN SỐ BÀI LỚP 4 ngay tại cửa nạp, trước khi bất kỳ ai đọc sổ.
       Cụm dãy số tách năm bài 14-08 nên B13 cũ lùi thành B18 và 31 bài dồn theo.
       Sổ của bé thì khoá theo MÃ BÀI — không chuyển thì huy hiệu gắn nhầm bài mà
       không có gì báo. Đặt ở đây vì đây là chỗ DUY NHẤT sổ tại máy đi vào app;
       chuyển ở chỗ khác là sót đường nào đó. `chuyenSo` tự có cờ chống chạy hai
       lần — chạy lần hai là dời thêm 5 chỗ và bé mất sạch tiến độ lớp 4. */
    return chuyenSo({ ...emptyProgress(), ...JSON.parse(raw) });
  } catch { return emptyProgress(); }
}

export function saveProgress(p, storage = globalThis.localStorage) {
  try { storage?.setItem(khoa(), JSON.stringify({ ...p, updatedAt: new Date().toISOString() })); }
  catch { /* chế độ riêng tư — bỏ qua, học vẫn chạy */ }
  return p;
}

/** Ghi kết quả một micro sau khi con bấm xong trang kết */
export function recordMicro(progress, microId, grade) {
  const prev = progress.micros[microId] || {};
  return {
    ...progress,
    micros: {
      ...progress.micros,
      [microId]: {
        done: true,
        pass: !!grade.pass,
        mustPassOK: !!grade.mustOK,
        best: Math.max(prev.best || 0, grade.right || 0),
        total: grade.total || 0,
        attempts: (prev.attempts || 0) + 1,
        at: new Date().toISOString(),
      },
    },
  };
}

/* ─────────── Nhớ chỗ đang học dở ─────────── */
/**
 * Con học nửa chừng rồi thoát (mẹ gọi ăn cơm, hết pin, bấm nhầm nút quay lại) —
 * lần sau mở lại phải về ĐÚNG chỗ đó, không bắt làm lại 15 bước đã làm.
 * Chỉ nhớ khi đã đi được vài bước và bài chưa đạt; bài đạt rồi thì mở lại từ đầu.
 */
export function saveSpot(progress, microId, step, total) {
  if (!(step > 0) || progress.micros[microId]?.pass) return progress;
  const prev = progress.micros[microId] || {};
  if (prev.step === step) return progress;
  return {
    ...progress,
    /* Đóng dấu `at` NGAY khi con đi thêm một bước, đừng đợi tới lúc xong bài. Kệ sách
       và sổ bố mẹ đều xếp "quyển động vào gần nhất" theo mốc này — không có dấu thì
       quyển con đang học dở luôn thua quyển con học xong từ tháng trước, và thẻ HỌC
       TIẾP chỉ tay sang quyển cũ. */
    micros: {
      ...progress.micros,
      [microId]: { ...prev, step, steps: total, at: new Date().toISOString() },
    },
  };
}

/** Bước con đang dở ở micro này — 0 nghĩa là học từ đầu */
export function resumeSpot(progress, microId) {
  const m = progress.micros[microId];
  return m && !m.pass && m.step > 0 ? { step: m.step, steps: m.steps || 0 } : null;
}

/** Xoá chỗ đánh dấu — dùng khi con chủ động chọn học lại từ đầu, hoặc đã đạt */
export function clearSpot(progress, microId) {
  const m = progress.micros[microId];
  if (!m || !m.step) return progress;
  const { step, steps, ...rest } = m;
  return { ...progress, micros: { ...progress.micros, [microId]: rest } };
}

/* ─────────── Kỳ sát hạch: MỘT KHOÁ CHO MỘT QUYỂN ───────────
 *
 * Sổ cũ khoá bằng SỐ CHƯƠNG trần: `chapters[3]`. Bốn quyển đều đánh chương từ 1, nên
 * con thi chương 3 của lớp 2 là huy hiệu chương 3 của lớp 5 cũng sáng lên — và ngược
 * lại, thi lại ở quyển kia là đè mất kết quả cũ. Không có gì báo, vì dữ liệu vẫn hợp lệ.
 *
 * Nay khoá là `lop3.5`. Khoá cũ vẫn đọc được, nhưng chỉ khi suy ra được nó thuộc
 * quyển nào — xem `ketQuaChuong`.
 */
export const khoaChuong = (ma, so) => `${ma}.${so}`;

/** Những quyển con đã từng động vào (có ít nhất một bài trong sổ). */
export function quyenDaCham(progress) {
  const s = new Set();
  for (const id of Object.keys(progress?.micros || {})) s.add(chuongTrinhCua(id));
  return s;
}

/** Kết quả kỳ sát hạch một chương của một quyển — null nếu chưa thi. */
export function ketQuaChuong(progress, ma, so) {
  const ch = progress?.chapters || {};
  const moi = ch[khoaChuong(ma, so)];
  if (moi) return moi;
  const cu = ch[so] ?? ch[String(so)];
  if (!cu) return null;
  /* Bản ghi theo khoá cũ không nói nó thuộc quyển nào. Con mới học đúng MỘT quyển
     thì chắc chắn là của quyển ấy; học từ hai quyển trở lên thì thà không hiện còn
     hơn gắn huy hiệu của lớp 5 vào sổ lớp 2. */
  const cham = quyenDaCham(progress);
  return cham.size === 1 && cham.has(ma) ? cu : null;
}

export function recordChapter(progress, ma, chapter, grade) {
  const k = khoaChuong(ma, chapter);
  const prev = ketQuaChuong(progress, ma, chapter) || {};
  return {
    ...progress,
    chapters: {
      ...progress.chapters,
      [k]: {
        done: true, pass: !!grade.pass,
        chuongTrinh: ma, chuong: chapter,
        best: Math.max(prev.best || 0, grade.right || 0),
        total: grade.total || 0,
        attempts: (prev.attempts || 0) + 1,
        at: new Date().toISOString(),
      },
    },
  };
}

/* ─────────── Luật mở khoá ─────────── */
/**
 * Micro mở khi micro TRƯỚC đã đạt (đủ điểm VÀ đúng câu bẫy).
 * Micro đầu tiên luôn mở. Cổng mustPass là điểm mấu chốt: sai câu bẫy thì không đi tiếp.
 */
/* ─────────── Hai chế độ học ─────────── */
/**
 * 'chuongtrinh' — đi theo chương trình đề xuất: học lần lượt từ bài đầu đến bài cuối.
 *                 Đúng thứ tự sư phạm, bài sau dùng lại bẫy của bài trước.
 * 'tuchon'      — con thích chủ đề nào thì vào chủ đề đó. TRONG một chương vẫn phải
 *                 học lần lượt, vì các bài trong chương xây chồng lên nhau.
 */
export const MODES = ['chuongtrinh', 'tuchon'];
export const modeOf = (progress) => (MODES.includes(progress?.mode) ? progress.mode : 'chuongtrinh');
export const setMode = (progress, mode) =>
  (MODES.includes(mode) ? { ...progress, mode } : progress);

export function isMicroUnlocked(progress, microId, list = allMicroIds()) {
  const i = list.indexOf(microId);
  if (i < 0) return false;
  if (i === 0) return true;

  if (modeOf(progress) === 'tuchon') {
    // Bài đầu của MỖI chương luôn mở — con chọn chủ đề nào cũng vào được ngay.
    const ch = chapterOf(microId);
    const dauChuong = list.find((id) => chapterOf(id) === ch);
    if (microId === dauChuong) return true;
  }

  const prev = progress.micros[list[i - 1]];
  return !!(prev?.pass);
}

/** Kỳ sát hạch chương mở khi TẤT CẢ micro của chương đã đạt */
export function isChapterExamUnlocked(progress, chapter, list = allMicroIds()) {
  const ms = list.filter((id) => chapterOf(id) === chapter);
  return ms.length > 0 && ms.every((id) => progress.micros[id]?.pass);
}

/** Micro tiếp theo con nên học (bài đầu tiên chưa đạt và đã mở) */
export function nextToStudy(progress, list = allMicroIds()) {
  for (const id of list) {
    if (!progress.micros[id]?.pass && isMicroUnlocked(progress, id, list)) return id;
  }
  return null;
}

/* ─────────── Thống kê hiển thị ─────────── */
export function chapterStats(progress, chapter, list = allMicroIds(), ma = 'lop5') {
  const ms = list.filter((id) => chapterOf(id) === chapter);
  const done = ms.filter((id) => progress.micros[id]?.pass).length;
  return {
    total: ms.length, done,
    percent: ms.length ? Math.round((done / ms.length) * 100) : 0,
    examUnlocked: isChapterExamUnlocked(progress, chapter, list),
    examPassed: !!ketQuaChuong(progress, ma, chapter)?.pass,
  };
}

export function overallStats(progress, list = allMicroIds(), ma = 'lop5') {
  const done = list.filter((id) => progress.micros[id]?.pass).length;
  /* Huy hiệu đếm THEO QUYỂN, và số chương suy TỪ DANH SÁCH BÀI. Bản cũ đếm cả
     `progress.chapters` nên trang lớp 2 khoe "9/14 huy hiệu" trong khi 8 cái là của
     lớp 5 — vừa sai quyển vừa sai mẫu số. */
  const chuong = [...new Set(list.map(chapterOf))];
  const badges = chuong.filter((c) => ketQuaChuong(progress, ma, c)?.pass).length;
  return {
    total: list.length, done,
    percent: list.length ? Math.round((done / list.length) * 100) : 0,
    badges, soChuong: chuong.length,
  };
}

/** Trạng thái hiển thị của một micro trong danh sách */
export function microState(progress, microId, list = allMicroIds()) {
  const m = progress.micros[microId];
  if (m?.pass) return 'passed';
  if (m?.done) return 'tried';
  return isMicroUnlocked(progress, microId, list) ? 'open' : 'locked';
}

/* ═══════════ LUYỆN THEO CHỦ ĐỀ — thang lùi/tiến ═══════════
 *
 * Khác hẳn `micros`/`chapters` ở trên: hai thứ ấy đo "con đã học xong bài nào",
 * còn lát này đo "con vững chủ đề nào tới lớp mấy". Cùng một chủ đề trải bốn lớp,
 * nên chỗ hổng của con là một CON SỐ LỚP, không phải một danh sách bài.
 *
 * Luật đi: đạt thì lên bậc trên, kém thì lùi bậc dưới, chạm sàn thì dừng tử tế.
 * Viết thành hàm thuần ở đây (không nhét trong component) để phép kiểm chạy được
 * mọi ngả — nhất là hai ngả bìa, chạm sàn và chạm trần, là chỗ dễ rơi vào hư không.
 */

/** Đạt là đúng 2/3 số câu — cân với ngưỡng 8/10 của kỳ sát hạch. */
export const nguongDat = (tong) => Math.max(1, Math.ceil((tong * 2) / 3));

/**
 * Bậc con nên bắt đầu: bậc CAO NHẤT không vượt lớp của con. Thang thiếu bậc đúng
 * lớp ấy thì lấy bậc dưới gần nhất; thấp hơn mọi bậc thì lấy bậc thấp nhất — thà
 * cho con làm bài trên lớp mình còn hơn không có gì để làm.
 */
export function bacBatDau(thang = [], lopCon = 5) {
  const lops = thang.map((b) => b.lop);
  if (!lops.length) return null;
  const vua = lops.filter((l) => l <= lopCon);
  return vua.length ? vua[vua.length - 1] : lops[0];
}

/**
 * Sau một lượt luyện thì đi đâu.
 *   { hanh: 'len',   lop }  đạt rồi, còn bậc trên
 *   { hanh: 'xong' }        đạt ở bậc cao nhất — vững chủ đề này
 *   { hanh: 'xuong', lop }  chưa đạt, lùi một bậc cho chắc gốc
 *   { hanh: 'san' }         chưa đạt mà đã ở bậc thấp nhất — dừng, báo bố mẹ
 */
export function buocSau(thang = [], lop, dat = 0, tong = 0) {
  const lops = thang.map((b) => b.lop);
  const i = lops.indexOf(lop);
  if (i < 0) return { hanh: 'san' };
  if (dat >= nguongDat(tong)) {
    return i === lops.length - 1 ? { hanh: 'xong' } : { hanh: 'len', lop: lops[i + 1] };
  }
  return i === 0 ? { hanh: 'san' } : { hanh: 'xuong', lop: lops[i - 1] };
}

/** Ghi kết quả một lượt luyện chủ đề tại một bậc. */
export function ghiLuyenChuDe(progress, maDang, lop, { dat = 0, tong = 0 } = {}) {
  const cu = progress.chuDe?.[maDang] || { bac: {} };
  const bacCu = cu.bac[String(lop)] || {};
  return {
    ...progress,
    chuDe: {
      ...(progress.chuDe || {}),
      [maDang]: {
        ...cu,
        bac: {
          ...cu.bac,
          [String(lop)]: {
            dat, tong,
            pass: dat >= nguongDat(tong),
            /* `best` giữ lần cao nhất: lùi xuống rồi lên lại thì lần sau đè lên lần
               trước, mà cái đáng nhớ là con ĐÃ từng làm được tới đâu. */
            best: Math.max(bacCu.best || 0, dat),
            lan: (bacCu.lan || 0) + 1,
            at: new Date().toISOString(),
          },
        },
        dangO: lop,
      },
    },
  };
}

/** Bậc cao nhất con đã đạt ở một chủ đề — null nếu chưa đạt bậc nào. */
export function bacDaVung(progress, maDang) {
  const bac = progress.chuDe?.[maDang]?.bac || {};
  const dat = Object.entries(bac).filter(([, v]) => v.pass).map(([l]) => Number(l));
  return dat.length ? Math.max(...dat) : null;
}

/* ═══════════ GỘP SỔ MÁY NÀY VỚI SỔ TRÊN MẠNG ═══════════
 *
 * Trước đây đăng nhập xong app chỉ ĐẨY LÊN, không bao giờ KÉO VỀ. Con học ở máy tính
 * bảng rồi mở máy tính của bố mẹ là thấy một quyển trắng tinh — công học vẫn còn
 * nguyên trên máy chủ, nhưng màn hình không biết, nên bố mẹ tưởng mất.
 *
 * Gộp theo MỐC THỜI GIAN của từng mục, không lấy nguyên một bên: con học bài 3 ở máy
 * bảng và bài 7 ở máy bàn thì cả hai đều phải còn. Mục nào không có mốc thì ưu tiên
 * bản ĐÃ ĐẠT — thà giữ thừa một dấu đạt còn hơn xoá mất công học thật.
 */
const mocCua = (m) => Date.parse(m?.at || 0) || 0;

function gopMuc(a, b) {
  if (!a) return b;
  if (!b) return a;
  const ta = mocCua(a), tb = mocCua(b);
  if (ta || tb) return tb > ta ? b : a;
  return b.pass && !a.pass ? b : a;
}

function gopBang(a = {}, b = {}) {
  const ra = { ...a };
  for (const [k, v] of Object.entries(b)) ra[k] = gopMuc(a[k], v);
  return ra;
}

/** Gộp sổ chủ đề: từng BẬC một, vì hai máy có thể luyện hai bậc khác nhau. */
function gopChuDe(a = {}, b = {}) {
  const ra = { ...a };
  for (const [ma, v] of Object.entries(b)) {
    const cu = a[ma];
    if (!cu) { ra[ma] = v; continue; }
    const bac = gopBang(cu.bac || {}, v.bac || {});
    /* `dangO` lấy theo bậc động vào SAU CÙNG — không lấy bậc cao hơn, vì con lùi
       xuống lớp dưới là có lý do, kéo ngược lên là xoá mất việc đang làm dở. */
    const mocA = Math.max(0, ...Object.values(cu.bac || {}).map(mocCua));
    const mocB = Math.max(0, ...Object.values(v.bac || {}).map(mocCua));
    ra[ma] = { ...cu, ...v, bac, dangO: mocB >= mocA ? v.dangO ?? cu.dangO : cu.dangO };
  }
  return ra;
}

export function gopTienDo(a = {}, b = {}) {
  if (!b || !Object.keys(b).length) return a;
  return {
    ...a,
    micros: gopBang(a.micros, b.micros),
    chapters: gopBang(a.chapters, b.chapters),
    chuDe: gopChuDe(a.chuDe, b.chuDe),
    dau: gopBang(a.dau, b.dau),
  };
}
