/**
 * HỌC BẠ — trả lời ba câu hỏi mà cả bốn màn hình đều cần, bằng cùng một phép tính.
 *
 *   1. "Con đang học cái gì, nên học tiếp cái gì?"      → trang chính của quyển
 *   2. "Con master chương nào, chủ đề nào, cần cố gắng chỗ nào?" → sổ bố mẹ
 *   3. "Em này trình độ tới đâu, chi tiết từng chương từng bài?" → bảng cô giáo
 *
 * Trước đây mỗi màn tự tính lấy: trang chính lớp 5 có luật riêng, trang lớp 2 có luật
 * khác, sổ bố mẹ đếm kiểu thứ ba (chia cứng cho 12), bảng cô giáo chỉ đếm tổng. Bốn
 * phép đếm cho bốn con số khác nhau về cùng một đứa trẻ — và không ai biết cái nào đúng.
 *
 * TOÀN BỘ TỆP NÀY LÀ HÀM THUẦN: vào là `chiMuc` (đã nạp) + `progress`, ra là số. Không
 * fetch, không React, không Firebase — nên phép kiểm chạy được bằng node trên mọi ngả,
 * kể cả hai ngả bìa hay rơi vào hư không: quyển chưa học bài nào, và quyển đã xong hết.
 */
import {
  isMicroUnlocked, resumeSpot, ketQuaChuong, nguongDat, bacDaVung,
} from './progress.js';

/* ═══════════ TẦNG 1 · MỘT BÀI ═══════════ */

/**
 * Trạng thái hiển thị của một bài.
 *   dat     đã đạt (đủ điểm và đúng câu bẫy)
 *   dangDo  đang học dở, còn chỗ đánh dấu
 *   chuaDat đã học hết mà chưa qua câu bẫy
 *   mo      học được ngay
 *   khoa    chưa mở (chỉ quyển nào khoá bài mới có)
 */
export function trangThaiBai(progress, id, { list = [], khoaBai = false } = {}) {
  const m = progress?.micros?.[id];
  if (m?.pass) return 'dat';
  if (m?.step > 0) return 'dangDo';
  if (m?.done) return 'chuaDat';
  if (khoaBai && !isMicroUnlocked(progress, id, list)) return 'khoa';
  return 'mo';
}

export const NHAN_TRANG_THAI = {
  dat: 'con đã đạt', dangDo: 'đang học dở', chuaDat: 'chưa qua câu bẫy',
  mo: 'học được ngay', khoa: 'chưa mở',
};

/* ═══════════ TẦNG 2 · MỘT CHƯƠNG ═══════════ */

/**
 * BÀI ĐỀ XUẤT CỦA MỘT CHƯƠNG — thứ trang chính chỉ vào.
 *
 * Luật, theo đúng thứ tự:
 *   1. bài con đang học DỞ trong chương này  → về đúng chỗ cũ, không bắt làm lại;
 *   2. bài đầu tiên CHƯA ĐẠT mà đã mở        → chưa từng học thì đây là BÀI ĐẦU CHƯƠNG;
 *   3. không có gì                            → chương đã xong.
 *
 * Điểm 2 là chỗ bốn quyển từng lệch nhau: lớp 5 chỉ đó bài kế tiếp trong toàn quyển,
 * còn lớp 2·3·4 chỉ có duy nhất một thẻ "bài tiếp theo" cho cả sách — mở chương 6 ra
 * thì không biết bắt đầu từ đâu.
 */
export function baiDeXuatChuong(progress, chuong, { list = [], khoaBai = false } = {}) {
  const ds = chuong?.bai || [];
  const doDang = ds.find((b) => resumeSpot(progress, b.id));
  if (doDang) return { bai: doDang, viSao: 'dangDo' };
  for (const b of ds) {
    if (progress?.micros?.[b.id]?.pass) continue;
    if (khoaBai && !isMicroUnlocked(progress, b.id, list)) continue;
    const daCham = !!progress?.micros?.[b.id];
    return { bai: b, viSao: daCham ? 'chuaDat' : 'moi' };
  }
  return null;
}

/** Đếm của một chương: bài đạt, phần trăm, kỳ sát hạch. */
export function thongKeChuong(progress, chuong, ma) {
  const ds = chuong?.bai || [];
  const dat = ds.filter((b) => progress?.micros?.[b.id]?.pass).length;
  const cham = ds.filter((b) => progress?.micros?.[b.id]).length;
  const ky = (chuong?.onTap || [])[0] || null;
  const kq = ketQuaChuong(progress, ma, chuong?.so);
  return {
    tong: ds.length, dat, cham,
    phanTram: ds.length ? Math.round((dat / ds.length) * 100) : 0,
    xongBai: ds.length > 0 && dat === ds.length,
    coKy: !!ky,
    kyDat: !!kq?.pass,
    kyDaThi: !!kq,
    kyLanTruoc: kq ? { dung: kq.best || 0, tong: kq.total || 0, lan: kq.attempts || 0 } : null,
    /* MASTER một chương = xong hết bài VÀ qua kỳ sát hạch. Chương không có kỳ (chưa
       soạn) thì xong hết bài là đủ — chứ không phải mãi mãi không master được. */
    master: ds.length > 0 && dat === ds.length && (!ky || !!kq?.pass),
  };
}

export const MUC_CHUONG = (tk) => (tk.master ? 'master'
  : tk.xongBai ? 'xongBai' : tk.dat > 0 || tk.cham > 0 ? 'dangHoc' : 'chuaHoc');

export const NHAN_MUC_CHUONG = {
  master: 'đã master', xongBai: 'xong bài, chưa qua kỳ sát hạch',
  dangHoc: 'đang học', chuaHoc: 'chưa học',
};

/* ═══════════ TẦNG 3 · MỘT QUYỂN ═══════════ */

/**
 * Học bạ của một quyển: đếm tổng, từng chương, và VIỆC TIẾP THEO.
 *
 * `khoaBai` đọc từ sổ đăng ký (`ct.khoaBai`), không suy từ tên quyển: lớp 5 khoá bài
 * tuần tự, ba quyển đọc chậm thì không khoá vì bé chưa có nhu cầu "mở khoá".
 */
export function hocBaQuyen(chiMuc, progress, { khoaBai = false } = {}) {
  const ma = chiMuc?.ma;
  const bai = chiMuc?.bai || [];
  const list = bai.map((b) => b.id);
  const chuong = (chiMuc?.chuong || []).map((c) => {
    const tk = thongKeChuong(progress, c, ma);
    return {
      ...c,
      tk,
      muc: MUC_CHUONG(tk),
      deXuat: baiDeXuatChuong(progress, c, { list, khoaBai }),
    };
  });

  const dat = bai.filter((b) => progress?.micros?.[b.id]?.pass).length;
  const cham = bai.filter((b) => progress?.micros?.[b.id]).length;
  const master = chuong.filter((c) => c.tk.master).length;

  /* VIỆC TIẾP THEO của cả quyển = đề xuất của chương ĐẦU TIÊN còn việc. Đi theo
     chương chứ không quét phẳng danh sách bài: con học dở chương 6 rồi bỏ sang
     chương 2 thì thứ nên chỉ vào vẫn là chỗ dở gần nhất theo mạch sách. */
  const doDang = chuong.find((c) => c.deXuat?.viSao === 'dangDo');
  const tiep = doDang || chuong.find((c) => c.deXuat);

  /* Kỳ sát hạch ĐANG CHỜ: chương đã xong hết bài mà chưa qua kỳ. Đây là việc quan
     trọng hơn học bài mới của chương sau — học xong mà không chốt thì huy hiệu treo. */
  const kyChoNo = chuong.find((c) => c.tk.xongBai && c.tk.coKy && !c.tk.kyDat) || null;

  return {
    ma,
    ten: chiMuc?.ten || ma,
    tongBai: bai.length,
    datBai: dat,
    chamBai: cham,
    phanTram: bai.length ? Math.round((dat / bai.length) * 100) : 0,
    tongChuong: chuong.length,
    masterChuong: master,
    huyHieu: chuong.filter((c) => c.tk.kyDat).length,
    chuong,
    ai: chiMuc?.ai || [],
    daBatDau: cham > 0,
    xongQuyen: bai.length > 0 && dat === bai.length,
    deXuat: tiep ? { ...tiep.deXuat, chuong: tiep } : null,
    kyChoNo,
  };
}

/**
 * BÀI CẦN CỐ GẮNG — đã thử mà chưa qua, nặng nhất lên đầu.
 * Xếp theo số lần thử rồi tới khoảng cách còn thiếu: bài thử 4 lần vẫn tắc cần giúp
 * trước bài mới trượt một lần.
 */
export function baiCanCoGang(chiMuc, progress, n = 8) {
  const out = [];
  for (const b of chiMuc?.bai || []) {
    const m = progress?.micros?.[b.id];
    if (!m || m.pass) continue;
    out.push({
      ...b,
      lan: m.attempts || 0,
      dung: m.best || 0,
      tong: m.total || 0,
      dangDo: m.step > 0,
    });
  }
  return out
    .sort((x, y) => y.lan - x.lan
      || (x.tong ? x.dung / x.tong : 1) - (y.tong ? y.dung / y.tong : 1))
    .slice(0, n);
}

/* ═══════════ TẦNG 4 · HỌC BẠ THEO CHỦ ĐỀ ═══════════
 *
 * Trục thứ hai, cắt ngang mọi quyển. Sổ theo lớp trả lời "con học tới bài nào";
 * sổ theo chủ đề trả lời "con VỮNG cái gì" — hai câu khác hẳn nhau, vì cùng một chủ
 * đề nằm rải ở bốn quyển dưới bốn tên chương khác nhau.
 */

/** Bậc thang đã học xong chưa — mọi bài của bậc đều phải đạt. */
export const xongBac = (progress, bac) =>
  (bac?.bai || []).length > 0 && bac.bai.every((i) => progress?.micros?.[i]?.pass);

/**
 * Tình trạng của một DẠNG BÀI.
 *   vung       đã vững tới bậc cao nhất của thang
 *   dangHoc    đã đạt vài bài / vài bậc, chưa tới đỉnh
 *   canCoGang  đã luyện hoặc đã học mà CHƯA đạt — chỗ bố mẹ cần để mắt
 *   chuaHoc    chưa động tới
 *
 * `canCoGang` xét TRƯỚC `dangHoc`: con đạt bậc lớp 3 rồi trượt bậc lớp 4 thì thứ đáng
 * nói là chỗ trượt, không phải chỗ đã qua.
 */
export function tinhTrangDang(progress, d) {
  const thang = d?.thang || [];
  const bai = thang.flatMap((b) => b.bai || []);
  const dat = bai.filter((i) => progress?.micros?.[i]?.pass).length;
  const cham = bai.filter((i) => progress?.micros?.[i]).length;
  const vungToi = bacDaVung(progress, d.__ma);
  const bacLuyen = progress?.chuDe?.[d.__ma]?.bac || {};
  const truot = Object.entries(bacLuyen)
    .filter(([, v]) => (v.lan || 0) > 0 && !v.pass)
    .map(([l]) => Number(l));
  const dinh = thang.length ? thang[thang.length - 1].lop : null;

  let tinhTrang = 'chuaHoc';
  if (bai.length > 0 && dat === bai.length) tinhTrang = 'vung';
  else if (vungToi !== null && dinh !== null && vungToi >= dinh) tinhTrang = 'vung';
  else if (truot.length || cham > dat) tinhTrang = 'canCoGang';
  else if (dat > 0 || vungToi !== null) tinhTrang = 'dangHoc';

  return {
    tinhTrang,
    soBai: bai.length,
    baiDat: dat,
    baiCham: cham,
    vungToi,
    bacTruot: truot.sort((a, b) => a - b),
    bacDinh: dinh,
    bacXong: thang.filter((b) => xongBac(progress, b)).map((b) => b.lop),
  };
}

export const NHAN_TINH_TRANG = {
  vung: 'đã vững', dangHoc: 'đang học', canCoGang: 'cần cố gắng', chuaHoc: 'chưa học',
};

/**
 * Học bạ theo chủ đề, dựng từ `chu_de.json`.
 * Trả về 5 mảng → chủ đề → dạng, mỗi tầng kèm đếm bốn tình trạng.
 */
export function hocBaChuDe(banDo, progress) {
  if (!banDo?.mang) return { mang: [], dem: { vung: 0, dangHoc: 0, canCoGang: 0, chuaHoc: 0 }, tong: 0 };
  const dem = { vung: 0, dangHoc: 0, canCoGang: 0, chuaHoc: 0 };
  let tong = 0;

  const mang = Object.entries(banDo.mang).map(([maM, m]) => {
    const demM = { vung: 0, dangHoc: 0, canCoGang: 0, chuaHoc: 0 };
    const chuDe = (m.chuDe || []).map((maCd) => {
      const c = banDo.chuDe?.[maCd];
      if (!c) return null;
      const demC = { vung: 0, dangHoc: 0, canCoGang: 0, chuaHoc: 0 };
      const dang = (c.dang || []).filter((k) => banDo.dang?.[k]).map((k) => {
        const d = { ...banDo.dang[k], __ma: k };
        const tt = tinhTrangDang(progress, d);
        demC[tt.tinhTrang]++; demM[tt.tinhTrang]++; dem[tt.tinhTrang]++; tong++;
        return { ma: k, ten: d.ten, thang: d.thang || [], moTaLop: d.moTaLop || {}, ...tt };
      });
      return { ma: maCd, ten: c.ten, dang, dem: demC };
    }).filter(Boolean);
    return { ma: maM, ten: m.ten, chuDe, dem: demM };
  });

  return { mang, dem, tong };
}

/**
 * TRÌNH ĐỘ HIỆN TẠI — một dòng cô giáo đọc trong ba giây.
 *
 * Không có một con số nào tự nó nói lên trình độ, nên ghép hai thứ đo được:
 *   · quyển con động vào GẦN NHẤT và học tới đâu trong đó;
 *   · bậc chủ đề con đã vững tới lớp mấy (trung vị, không phải cao nhất — một chủ đề
 *     vững tới lớp 5 không có nghĩa cả người ở lớp 5).
 */
export function trinhDo(dsHocBa, progress, { gioCua = () => 0 } = {}) {
  const daHoc = dsHocBa.filter((h) => h.daBatDau);
  const ganNhat = daHoc.slice().sort((a, b) => gioCua(b.ma) - gioCua(a.ma))[0] || null;
  const bac = Object.keys(progress?.chuDe || {})
    .map((ma) => bacDaVung(progress, ma))
    .filter((x) => x !== null)
    .sort((a, b) => a - b);
  const giua = bac.length ? bac[Math.floor((bac.length - 1) / 2)] : null;
  return {
    quyen: ganNhat,
    soQuyenDangHoc: daHoc.length,
    tongBaiDat: dsHocBa.reduce((s, h) => s + h.datBai, 0),
    tongChuongMaster: dsHocBa.reduce((s, h) => s + h.masterChuong, 0),
    bacChuDe: giua,
    soChuDeDoDuoc: bac.length,
  };
}

export { nguongDat };
