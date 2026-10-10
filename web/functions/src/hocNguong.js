import { layNguong, KHOANG, capNhatBKT } from './nguong.js';
import { chayLaiChuoi, chiSoNG07, chatLuongMoHinh } from './thongke.js';

/**
 * HỌC NGƯỠNG TỪ DỮ LIỆU — mục 3.8.3 của luận văn.
 *
 * ── ⚠ HỌC ĐỂ ĐỀ XUẤT, KHÔNG TỰ ÁP DỤNG ──
 * Đây là nguyên tắc của cả mục 3.8: «giá trị học được chỉ là đề xuất; chỉ chuyên gia
 * mới phát hành được một phiên bản ngưỡng mới» (Amershi và cộng sự, 2014 — người có
 * chuyên môn trong vòng lặp ra quyết định, đúng ràng buộc R2: mô hình có thể sai).
 * Nên tệp này KHÔNG ghi vào bảng `nguong`. Nó chỉ dựng ra các ĐỀ XUẤT, và
 * `firestore.rules` cũng chốt thêm một lần: máy con không tạo được đề xuất, và
 * chuyên gia chỉ đổi được `trangThai` chứ không sửa được con số máy học ra.
 *
 * ── BỐN CÁCH HỌC, TÙY LOẠI NGƯỠNG (mục 3.8.3) ──
 *   NG01–NG05  tham số BKT        → EM trên chuỗi trả lời của từng nút
 *   NG06, NG13 tham số quên       → hồi quy chu kỳ bán rã (Settles & Meeder, 2016)
 *   NG07–NG12  ngưỡng quyết định  → quét lưới, chạy lại nhật ký với từng giá trị
 *   NG16–NG18  ngưỡng hành vi     → phân vị của phân bố thật (Wise, 2017)
 *
 * ── ⚠ TỆP NÀY THUẦN TOÁN ──
 * Vào: mảng lượt. Ra: mảng đề xuất. Không đụng Firestore, nên cổng chạy lại được, và
 * — quan trọng hơn — mỗi đề xuất mang theo CHỈ SỐ TRƯỚC và SAU tính trên chính nhật
 * ký ấy. Đó là bước «chạy thử lại» mà mục 3.8.3 đòi: chuyên gia thấy hậu quả của
 * một thay đổi TRƯỚC khi duyệt, chứ không duyệt một con số trần.
 */

const NGAY = 86400000;

/* ════════════════════════ NG01–NG05 · EM ════════════════════════ */

/**
 * Ước lượng bốn tham số BKT bằng EM trên các chuỗi trả lời.
 *
 * Mô hình Markov ẩn hai trạng thái (Hình 2.4): chưa thạo → thạo với xác suất T, và
 * KHÔNG có đường ngược (BKT chuẩn không quên trong phiên). Quan sát: đã thạo mà sai
 * là sơ suất (slip), chưa thạo mà đúng là đoán trúng (guess).
 *
 * ── ⚠ CÓ THANG TỈ LỆ, KHÔNG NHÂN TRẦN ──
 * Chuỗi dài vài chục lượt thì tích các xác suất tụt rất nhanh về 0 và mọi tham số ra
 * `NaN`. Chia thang ở từng bước giữ số trong khoảng dùng được, và không đổi kết quả.
 *
 * ── ⚠ CHỐT P(S) < 0,5 VÀ P(G) < 0,5 ──
 * Baker và cộng sự (2008): vượt mức ấy thì mô hình SUY BIẾN — nó đổi vai hai trạng
 * thái cho nhau, và "đã thạo" trở thành "hay trả lời sai". Con số vẫn khớp dữ liệu,
 * chỉ là nó mô tả một thế giới ngược. Khoảng hợp lệ của Bảng 3.19 cũng chốt đúng
 * chỗ ấy, nhưng chốt ngay trong vòng lặp thì EM không bao giờ đi vào vùng suy biến.
 */
export const EM_MAC_DINH = { lap: 200, hoiTu: 1e-6, san: 1e-4 };

export function hocBKT(chuoiDs, { lap, hoiTu, san } = EM_MAC_DINH, batDau = null) {
  const ds = (chuoiDs || []).filter((c) => Array.isArray(c) && c.length > 0);
  if (!ds.length) return null;

  let p = batDau || { L0: 0.1, T: 0.1, slip: 0.1, guess: 0.2 };
  const ep = { lap: lap ?? EM_MAC_DINH.lap, hoiTu: hoiTu ?? EM_MAC_DINH.hoiTu, san: san ?? EM_MAC_DINH.san };
  let logLikCu = -Infinity;
  let vong = 0;

  for (; vong < ep.lap; vong += 1) {
    let tL0 = 0;
    let tChuyen = 0;
    let tChuaThao = 0;      // Σ γ(chưa thạo) trên t = 1..T-1, mẫu số của T
    let gDung0 = 0;
    let gTong0 = 0;
    let gSai1 = 0;
    let gTong1 = 0;
    let logLik = 0;

    for (const o of ds) {
      const n = o.length;
      const B = (s, dung) => (s === 1 ? (dung ? 1 - p.slip : p.slip) : (dung ? p.guess : 1 - p.guess));

      /* Tiến, có thang tỉ lệ */
      const a = Array.from({ length: n }, () => [0, 0]);
      const c = new Array(n).fill(1);
      a[0][0] = (1 - p.L0) * B(0, o[0]);
      a[0][1] = p.L0 * B(1, o[0]);
      c[0] = a[0][0] + a[0][1];
      if (!(c[0] > 0)) return null;
      a[0][0] /= c[0]; a[0][1] /= c[0];
      for (let t = 1; t < n; t += 1) {
        a[t][0] = a[t - 1][0] * (1 - p.T) * B(0, o[t]);
        a[t][1] = (a[t - 1][0] * p.T + a[t - 1][1]) * B(1, o[t]);
        c[t] = a[t][0] + a[t][1];
        if (!(c[t] > 0)) return null;
        a[t][0] /= c[t]; a[t][1] /= c[t];
      }
      for (const x of c) logLik += Math.log(x);

      /* Lùi, dùng CÙNG thang tỉ lệ của bước tiến */
      const b = Array.from({ length: n }, () => [0, 0]);
      b[n - 1][0] = 1; b[n - 1][1] = 1;
      for (let t = n - 2; t >= 0; t -= 1) {
        b[t][0] = ((1 - p.T) * B(0, o[t + 1]) * b[t + 1][0] + p.T * B(1, o[t + 1]) * b[t + 1][1]) / c[t + 1];
        b[t][1] = (B(1, o[t + 1]) * b[t + 1][1]) / c[t + 1];
      }

      const g = (t, s) => a[t][s] * b[t][s];
      tL0 += g(0, 1);
      for (let t = 0; t < n; t += 1) {
        gTong0 += g(t, 0); gTong1 += g(t, 1);
        if (o[t]) gDung0 += g(t, 0); else gSai1 += g(t, 1);
        if (t < n - 1) {
          tChuaThao += g(t, 0);
          tChuyen += (a[t][0] * p.T * B(1, o[t + 1]) * b[t + 1][1]) / c[t + 1];
        }
      }
    }

    const kep = (x, lo, hi) => Math.min(hi, Math.max(lo, x));
    const moi = {
      L0: kep(tL0 / ds.length, ep.san, 1 - ep.san),
      T: kep(tChuaThao > 0 ? tChuyen / tChuaThao : p.T, ep.san, 1 - ep.san),
      /* ⚠ Trần 0,49: xem khối chú thích trên. Đây là chốt chống suy biến, không
         phải một phép làm đẹp số. */
      guess: kep(gTong0 > 0 ? gDung0 / gTong0 : p.guess, ep.san, 0.49),
      slip: kep(gTong1 > 0 ? gSai1 / gTong1 : p.slip, ep.san, 0.49),
    };
    p = moi;
    if (Math.abs(logLik - logLikCu) < ep.hoiTu) { vong += 1; break; }
    logLikCu = logLik;
  }

  return { ...p, soChuoi: ds.length, soLuot: ds.reduce((s, x) => s + x.length, 0), vong, logLik: logLikCu };
}

/**
 * Chia người học thành k phần và đo AUC trên phần GIỮ LẠI.
 *
 * ⚠ CHIA THEO NGƯỜI HỌC, KHÔNG CHIA THEO LƯỢT (mục 2.4.5.a). Chia theo lượt thì
 * lượt của cùng một bé nằm cả hai bên, mô hình đã thấy bé ấy rồi, và AUC đo được
 * cao hơn sự thật — cao một cách có hệ thống, nên không ai nghi.
 */
export function kiemTraCheo(theoBe, k = 5) {
  const be = [...theoBe.keys()].sort();
  if (be.length < k) return null;
  const ra = [];

  for (let i = 0; i < k; i += 1) {
    const giu = new Set(be.filter((_, j) => j % k === i));
    const hoc = [];
    for (const [b, chuoi] of theoBe) if (!giu.has(b)) hoc.push(...chuoi.map((c) => c.map((x) => !!x.correct)));
    const ts = hocBKT(hoc);
    if (!ts) continue;

    const buoc = [];
    for (const [b, chuoi] of theoBe) {
      if (!giu.has(b)) continue;
      for (const c of chuoi) {
        let pl = ts.L0;
        for (const a of c) {
          buoc.push({ pDuDoan: pl * (1 - ts.slip) + (1 - pl) * ts.guess, dung: !!a.correct });
          pl = capNhatBKT(pl, !!a.correct, ts);
        }
      }
    }
    const d = chatLuongMoHinh(buoc);
    if (d.auc != null) ra.push(d.auc);
  }

  if (!ra.length) return null;
  const tb = ra.reduce((s, x) => s + x, 0) / ra.length;
  /* ── SAI SỐ CHUẨN CỦA TRUNG BÌNH, để biết một cải thiện có hơn NHIỄU không ──
     Năm phần chia khác nhau cho năm con AUC khác nhau; chênh lệch giữa chúng chính
     là mức nhiễu của phép đo. Một cải thiện nhỏ hơn mức ấy KHÔNG phải bằng chứng. */
  const pq = ra.length > 1
    ? ra.reduce((x, y) => x + (y - tb) ** 2, 0) / (ra.length - 1) : 0;
  return {
    aucTrungBinh: tb,
    soPhan: ra.length,
    tungPhan: ra.map((x) => +x.toFixed(4)),
    saiSoChuan: Math.sqrt(pq / ra.length),
  };
}

/* ════════════════════════ NG06 · HỒI QUY BÁN RÃ ════════════════════════ */

/**
 * Học chu kỳ bán rã từ độ chính xác ở lượt ĐẦU sau một khoảng nghỉ.
 *
 * Settles & Meeder (2016): quét h, với mỗi h chạy lại phép quên trên chính nhật ký
 * rồi đo sai số bình phương giữa xác suất dự đoán và kết quả thật. Chọn h cho sai số
 * nhỏ nhất.
 *
 * ⚠ CHỈ LẤY LƯỢT ĐẦU SAU NGHỈ ≥ 1 NGÀY. Lượt trong cùng phiên không nói gì về việc
 * quên, và đưa chúng vào thì chúng áp đảo mẫu (chúng đông hơn hàng chục lần) và mọi
 * h đều cho cùng một sai số.
 */
export function hocNuaDoi(nhom, bo, { luoi = null } = {}) {
  const mau = [];
  for (const ds of nhom.values()) {
    const buoc = chayLaiChuoi(ds, bo);
    for (let i = 1; i < buoc.length; i += 1) {
      const cach = ((buoc[i].a.ts ?? 0) - (buoc[i - 1].a.ts ?? 0)) / NGAY;
      if (cach < 1) continue;
      mau.push({ p: buoc[i - 1].pSau, cach, dung: buoc[i].dung, nc: buoc[i].nc });
    }
  }
  if (!mau.length) return null;

  const [lo, hi] = KHOANG.NG06;
  const ds = luoi || Array.from({ length: Math.round(hi - lo) + 1 }, (_, i) => lo + i);
  let tot = null;
  const duong = [];
  for (const h of ds) {
    let sse = 0;
    for (const m of mau) {
      const pQuen = 0.5 + (m.p - 0.5) * 2 ** (-m.cach / h);
      const duDoan = pQuen * (1 - layNguong(bo, 'NG03', m.nc)) + (1 - pQuen) * layNguong(bo, 'NG04', m.nc);
      sse += (duDoan - (m.dung ? 1 : 0)) ** 2;
    }
    const rmse = Math.sqrt(sse / mau.length);
    duong.push({ h, rmse: +rmse.toFixed(5) });
    if (!tot || rmse < tot.rmse) tot = { h, rmse };
  }
  return { ...tot, coMau: mau.length, duong };
}

/* ════════════════════════ NG07 · QUÉT LƯỚI ════════════════════════ */

/**
 * Quét lưới cho θ — chạy lại nhật ký với từng giá trị trong khoảng hợp lệ.
 *
 * Mục 3.8.3: «chọn giá trị cân bằng tốt nhất giữa hai loại sai: công nhận tinh thông
 * quá sớm và bắt luyện quá nhiều». Pelánek & Řihák (2017) gọi đó là đồ thị công sức
 * – kết quả.
 *
 * ── ⚠ PHÉP CÂN BẰNG LÀ MỘT LỰA CHỌN, KHÔNG PHẢI MỘT SỰ THẬT ──
 * «Cân bằng tốt nhất» đòi nói rõ một câu lớn bằng mấy câu nhỏ, mà không dữ liệu nào
 * trả lời được câu ấy — nó là câu hỏi SƯ PHẠM. Nên hàm này:
 *   · trả về CẢ ĐƯỜNG CONG, để chuyên gia nhìn được đánh đổi và chọn khác;
 *   · dùng một hàm chi phí nói thẳng ra, với `lamda` ghi vào đề xuất.
 * Giấu phép cân bằng đi và chỉ đưa một con số là đưa một quyết định sư phạm dưới
 * dạng một kết quả tính toán.
 */
export const LAMDA_MAC_DINH = 1;

export function quetLuoiTheta(nhom, bo, { luoi = null, lamda = LAMDA_MAC_DINH } = {}) {
  const [lo, hi] = KHOANG.NG07;
  const ds = luoi || Array.from({ length: Math.round((hi - lo) / 0.01) + 1 },
    (_, i) => +(lo + i * 0.01).toFixed(2));

  const duong = [];
  for (const theta of ds) {
    const thu = { ...bo, theoPhamVi: { ...(bo.theoPhamVi || {}), toanHe: { ...(bo.theoPhamVi?.toanHe || {}), NG07: theta } } };
    const r = chiSoNG07(nhom, thu);
    if (r.coMauCongNhanSom < 1 || r.coMauToiThao < 1) continue;
    duong.push({
      theta,
      congNhanSom: r.tiLeCongNhanSom,
      soCau: r.soCauTrungBinhToiThao,
      coMauSom: r.coMauCongNhanSom,
      coMauThao: r.coMauToiThao,
    });
  }
  if (!duong.length) return null;

  /* Chuẩn hoá công sức về [0,1] trên chính đường cong này — nếu không thì `lamda`
     mang đơn vị "số câu" và không so được với một tỉ lệ. */
  const maxCau = Math.max(...duong.map((x) => x.soCau));
  const minCau = Math.min(...duong.map((x) => x.soCau));
  const giai = maxCau - minCau || 1;
  for (const x of duong) x.chiPhi = x.congNhanSom + lamda * ((x.soCau - minCau) / giai);

  const tot = duong.reduce((a, b) => (b.chiPhi < a.chiPhi ? b : a));
  return { theta: tot.theta, chiPhi: tot.chiPhi, lamda, duong };
}

/* ════════════════════════ NG16 · PHÂN VỊ ════════════════════════ */

/** Phân vị của một mảng số. Nội suy tuyến tính, đúng lối `numpy.percentile`. */
export function phanVi(ds, q) {
  const a = [...ds].filter(Number.isFinite).sort((x, y) => x - y);
  if (!a.length) return null;
  const i = (a.length - 1) * q;
  const lo = Math.floor(i);
  const hi = Math.ceil(i);
  return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo);
}

/**
 * Ngưỡng "bế tắc" theo phân vị thời gian trả lời (Wise, 2017).
 *
 * ⚠ GOM THEO CẶP (dạng câu, bậc), đúng Bảng 3.22 — và đúng chỗ mục 3.6.8 đã báo
 * nhầm mệt mỏi vì gom thiếu một chiều.
 */
export function hocNguongHanhVi(luots, { q = 0.95, toiThieu = 30 } = {}) {
  const nhom = new Map();
  for (const a of luots) {
    if (!Number.isFinite(a?.ms)) continue;
    const k = `${a.mode ?? '—'}·${a.bac ?? '—'}`;
    if (!nhom.has(k)) nhom.set(k, []);
    nhom.get(k).push(a.ms / 1000);
  }
  const ra = {};
  for (const [k, ds] of nhom) {
    if (ds.length < toiThieu) continue;     // dưới mẫu tối thiểu thì KHÔNG kết luận
    ra[k] = { giay: +phanVi(ds, q).toFixed(1), coMau: ds.length };
  }
  return Object.keys(ra).length ? { q, theoNhom: ra } : null;
}

/* ════════════════════════ KHOẢNG TIN CẬY ════════════════════════ */

/**
 * Khoảng Wilson cho một tỉ lệ — KHÔNG dùng khoảng chuẩn (Wald).
 *
 * Wald vỡ ở đúng chỗ ta hay gặp: tỉ lệ gần 0 hoặc gần 1, và cỡ mẫu nhỏ. Nó cho ra
 * cận dưới âm hoặc cận trên quá 1, tức một khoảng tin cậy nói điều không thể xảy ra.
 */
export function khoangWilson(dung, tong, z = 1.96) {
  if (!tong) return null;
  const p = dung / tong;
  const d = 1 + (z * z) / tong;
  const tam = p + (z * z) / (2 * tong);
  const nua = z * Math.sqrt((p * (1 - p) + (z * z) / (4 * tong)) / tong);
  return [Math.max(0, (tam - nua) / d), Math.min(1, (tam + nua) / d)];
}

/* ════════════════════════ DỰNG ĐỀ XUẤT ════════════════════════ */

/** Nhóm lượt theo (bé, nút) — cùng phép nhóm mà `thongke.js` dùng. */
function theoChuoi(luots) {
  const nhom = new Map();
  for (const a of luots) {
    if (!a?.learnerId || !a?.bktUnit) continue;
    const k = `${a.learnerId}::${a.bktUnit}`;
    if (!nhom.has(k)) nhom.set(k, []);
    nhom.get(k).push(a);
  }
  for (const ds of nhom.values()) ds.sort((x, y) => (x.ts ?? 0) - (y.ts ?? 0));
  return nhom;
}

/** Nhóm chuỗi theo NGƯỜI HỌC — cho phép kiểm tra chéo chia đúng cách. */
function theoBe(luots) {
  const be = new Map();
  for (const [k, ds] of theoChuoi(luots)) {
    const b = k.split('::')[0];
    if (!be.has(b)) be.set(b, []);
    be.get(b).push(ds);
  }
  return be;
}

/**
 * Một đề xuất đổi ngưỡng.
 *
 * ⚠ MỖI ĐỀ XUẤT PHẢI TỰ BẢO VỆ ĐƯỢC. Mục 3.8.3 đòi lưu kèm cỡ mẫu, khoảng tin cậy,
 * phương pháp, VÀ chỉ số tính trên nhật ký với giá trị cũ và giá trị mới. Thiếu phần
 * cuối thì chuyên gia duyệt một con số trần — và «duyệt» khi ấy chỉ là bấm nút.
 */
function deXuat({ ma, phamVi, khoa, cu, moi, phuongPhap, coMau, khoangTinCay = null,
                  chiSoTruoc = null, chiSoSau = null, canCu = null, bayGio, toiThieu = 0 }) {
  const [lo, hi] = KHOANG[ma] || [];
  /* ── ⚠ CỠ MẪU XÉT THEO TỪNG NGƯỠNG, KHÔNG THEO TỔNG PHẠM VI ──
     Mục 3.8.3: «với MỖI NGƯỠNG và mỗi phạm vi, hàm chỉ chạy khi số lượt dữ liệu đạt
     cỡ mẫu tối thiểu NG21». Bản đầu tôi chốt ở tổng phạm vi, và nó cho ra đề xuất
     đổi θ với cỡ mẫu 46 trong khi phạm vi có 3.213 lượt — vì chỉ 46 lượt trong số
     ấy thực sự nói được gì về θ. Một đề xuất như thế trông đủ chuẩn (phạm vi đã qua
     NG21) nhưng đứng trên gần như không có gì. */
  const thieuMau = coMau < toiThieu;
  /* ⚠ NGOÀI KHOẢNG HỢP LỆ THÌ KHÔNG ĐỀ XUẤT, và nói rõ vì sao. Kẹp im lặng về biên
     là biến một dấu hiệu «mô hình đang nói điều vô lý» thành một con số trông hợp lệ.
     Bảng 3.19 gọi khoảng này là giới hạn CỨNG: thuật toán cũng không được vượt. */
  const ngoai = typeof moi === 'number' && lo != null && (moi < lo || moi > hi);
  return {
    ma,
    phamVi,
    khoa: khoa ?? null,
    giaTriHienTai: cu,
    giaTriDeXuat: (ngoai || thieuMau) ? null : moi,
    ngoaiKhoang: ngoai ? { giaTriTho: moi, khoang: [lo, hi] } : null,
    thieuMau: thieuMau ? { coMau, can: toiThieu } : null,
    phuongPhap,
    coMau,
    khoangTinCay,
    chiSoTruoc,
    chiSoSau,
    /* ⚠ LÝ DO TỪ CHỐI PHẢI THAY LỜI GIẢI THÍCH, KHÔNG ĐỨNG CẠNH NÓ.
       Bản đầu chỉ viết lại `canCu` cho trường hợp thiếu mẫu. Sinh bộ đề xuất đầu
       tiên trên dữ liệu thật thì dòng `NG16 dangCau=so` hiện ra KHÔNG có giá trị đề
       xuất mà căn cứ lại đọc y như một đề xuất bình thường — chuyên gia nhìn vào
       không hiểu vì sao không có con số nào. */
    canCu: thieuMau
      ? `KHÔNG đề xuất: chỉ ${coMau} lượt nói được về ngưỡng này, cần ${toiThieu} (NG21). `
        + `Giá trị tính thô là ${JSON.stringify(moi)} — ghi lại để thấy dữ liệu đang nghiêng về đâu, `
        + 'nhưng chưa đủ để đứng thành một đề xuất.'
      : (ngoai
        ? `KHÔNG đề xuất: máy tính ra ${JSON.stringify(moi)}, NGOÀI khoảng hợp lệ [${lo} – ${hi}] của `
          + 'Bảng 3.19 — và khoảng ấy là giới hạn cứng, thuật toán cũng không được vượt. '
          + `Đây là một DẤU HIỆU đáng xem: hoặc cận trên đang quá chặt, hoặc dữ liệu vào có chỗ bất thường. ${canCu}`
        : canCu),
    giaTriTho: (thieuMau || ngoai) ? moi : null,
    trangThai: 'cho',
    tinhLuc: bayGio,
  };
}

/**
 * Dựng mọi đề xuất cho MỘT phạm vi.
 *
 * ── ⚠ CHỐT CỠ MẪU ĐỨNG Ở ĐÂY, KHÔNG ĐỨNG Ở PHÉP THỐNG KÊ ──
 * Mục 3.8.3: «hàm chỉ chạy khi số lượt dữ liệu đạt cỡ mẫu tối thiểu NG21; nếu chưa
 * đủ, hàm học ở phạm vi rộng hơn». Thống kê thì cứ tính và cứ ghi kèm cỡ mẫu — giấu
 * số liệu vì chưa đủ mẫu thì không ai biết dữ liệu đang tới đâu. Nhưng biến thống kê
 * thành ĐỀ XUẤT thì phải đủ mẫu, vì đề xuất là thứ đi tới quyết định.
 */
export function dungDeXuat(luots, bo, { phamVi = 'toanHe', khoa = null, bayGio = Date.now() } = {}) {
  const ds = (luots || []).filter((a) => a?.learnerId && a?.bktUnit);
  const toiThieu = layNguong(bo, 'NG21');
  if (ds.length < toiThieu) {
    return { phamVi, khoa, coMau: ds.length, duMau: false, deXuat: [], viSao: `cần ${toiThieu} lượt, mới có ${ds.length}` };
  }

  const nhom = theoChuoi(ds);
  const be = theoBe(ds);
  const ra = [];
  const nc = phamVi === 'toanHe' ? {} : { [phamVi]: String(khoa) };
  const tt = toiThieu;   // cỡ mẫu tối thiểu, xét lại cho TỪNG ngưỡng

  /* ── NG01–NG05 · EM, có kiểm tra chéo ─────────────────────────────────── */
  const em = hocBKT([...nhom.values()].map((c) => c.map((x) => !!x.correct)));
  if (em) {
    /* ⚠ KIỂM TRA CHÉO TRƯỚC KHI ĐƯA THÀNH ĐỀ XUẤT (mục 3.8.3). Bộ tham số khớp dữ
       liệu đã thấy mà kém hơn bộ đang hành trên dữ liệu GIỮ LẠI thì nó đang học
       thuộc, không phải học. */
    const cheo = kiemTraCheo(be);
    const buocCu = [];
    for (const c of nhom.values()) buocCu.push(...chayLaiChuoi(c, bo));
    const truoc = chatLuongMoHinh(buocCu);

    /* ⚠ ĐÒI CẢI THIỆN HƠN NHIỄU, không chỉ hơn một hạt bụi.
       Bản đầu tôi viết `cheo.aucTrungBinh > truoc.auc`. Chạy thử thấy nó nhận một
       đề xuất đổi cả bốn tham số BKT vì AUC hơn đúng 0,0005 — trong khi năm phần
       chia lệch nhau tới 0,04. Một cải thiện nhỏ hơn mức nhiễu của chính phép đo
       thì không phải bằng chứng, và đổi bốn tham số theo nó là đổi mô hình người
       học của mọi đứa trẻ vì một con số ngẫu nhiên. */
    const bienAn = cheo ? cheo.saiSoChuan : 0;
    const dat = cheo && truoc.auc != null && cheo.aucTrungBinh > truoc.auc + bienAn;
    for (const [ma, khoaEm] of [['NG01', 'L0'], ['NG02', 'T'], ['NG03', 'slip'], ['NG04', 'guess']]) {
      ra.push(deXuat({
        ma, phamVi, khoa, bayGio, toiThieu: tt,
        cu: layNguong(bo, ma, nc),
        moi: dat ? +em[khoaEm].toFixed(4) : null,
        phuongPhap: 'EM trên chuỗi trả lời, kiểm tra chéo 5 phần CHIA THEO NGƯỜI HỌC',
        coMau: em.soLuot,
        chiSoTruoc: { auc: truoc.auc, rmse: truoc.rmse },
        chiSoSau: cheo ? { auc: cheo.aucTrungBinh, soPhan: cheo.soPhan, tungPhan: cheo.tungPhan } : null,
        canCu: dat
          ? `AUC trên dữ liệu giữ lại ${cheo.aucTrungBinh.toFixed(4)} > ${truoc.auc.toFixed(4)} của bộ đang hành, `
            + `và hơn nhiều hơn sai số chuẩn giữa các phần chia (${bienAn.toFixed(4)})`
          : (cheo
            ? `KHÔNG đề xuất: AUC giữ lại ${cheo.aucTrungBinh.toFixed(4)} không hơn `
              + `${truoc.auc?.toFixed(4)} của bộ đang hành quá sai số chuẩn ${bienAn.toFixed(4)}`
            : 'KHÔNG đề xuất: chưa đủ người học để chia 5 phần'),
      }));
    }
  }

  /* ── NG06 · hồi quy bán rã ────────────────────────────────────────────── */
  const h = hocNuaDoi(nhom, bo);
  if (h) {
    const cu = layNguong(bo, 'NG06', nc);
    const rmseCu = h.duong.find((x) => x.h === cu)?.rmse ?? null;
    ra.push(deXuat({
      ma: 'NG06', phamVi, khoa, bayGio, toiThieu: tt,
      cu, moi: h.h,
      phuongPhap: 'hồi quy chu kỳ bán rã trên lượt ĐẦU sau khoảng nghỉ ≥ 1 ngày (Settles & Meeder, 2016)',
      coMau: h.coMau,
      chiSoTruoc: rmseCu == null ? null : { rmse: rmseCu },
      chiSoSau: { rmse: h.rmse },
      canCu: rmseCu == null
        ? `RMSE nhỏ nhất tại h = ${h.h}`
        : `RMSE ${h.rmse.toFixed(5)} tại h = ${h.h}, so với ${rmseCu.toFixed(5)} của h = ${cu} đang hành`,
    }));
  }

  /* ── NG07 · quét lưới ─────────────────────────────────────────────────── */
  const q = quetLuoiTheta(nhom, bo);
  if (q) {
    const cu = layNguong(bo, 'NG07', nc);
    const diemCu = q.duong.find((x) => Math.abs(x.theta - cu) < 1e-9) || null;
    const diemMoi = q.duong.find((x) => x.theta === q.theta);
    ra.push(deXuat({
      ma: 'NG07', phamVi, khoa, bayGio, toiThieu: tt,
      cu, moi: q.theta,
      phuongPhap: `quét lưới trên nhật ký, cân bằng công nhận sớm với công sức (λ = ${q.lamda})`,
      coMau: diemMoi.coMauThao,
      khoangTinCay: khoangWilson(
        Math.round(diemMoi.congNhanSom * diemMoi.coMauSom), diemMoi.coMauSom),
      chiSoTruoc: diemCu && { congNhanSom: diemCu.congNhanSom, soCau: diemCu.soCau },
      chiSoSau: { congNhanSom: diemMoi.congNhanSom, soCau: diemMoi.soCau },
      canCu: 'kèm CẢ ĐƯỜNG CONG công sức–kết quả để chuyên gia chọn khác được; '
        + 'phép cân bằng là một lựa chọn sư phạm, không phải kết quả của dữ liệu',
    }));
    ra[ra.length - 1].duongCong = q.duong.map((x) => ({
      theta: x.theta, congNhanSom: +x.congNhanSom.toFixed(4), soCau: +x.soCau.toFixed(2),
    }));
  }

  /* ── NG16 · phân vị, ĐỀ XUẤT THEO TỪNG DẠNG CÂU ───────────────────────
     ⚠ KHÔNG đề xuất một con số chung. Đo trên dữ liệu thật thấy chênh lệch GẤP CHÍN
     LẦN giữa các dạng câu: `chon` 30,5 giây · `dungsai` 50,6 · `chondapan` 73,2 ·
     `so` 167,4 · `bieuthuc` 269,6. Lấy trung bình của chúng (118,3) ra một con số
     không mô tả dạng nào: nó quá lỏng với câu trắc nghiệm và quá chặt với câu biểu
     thức, tức gắn nhãn "bế tắc" sai ở cả hai đầu.

     Thang phạm vi đã có sẵn nấc `dangCau` cho đúng việc này, nên mỗi dạng câu là một
     đề xuất riêng. Bảng 3.22 đòi gom theo CẶP (dạng câu, bậc), nhưng bảng ngưỡng chỉ
     có nấc `dangCau` và nấc `bac` RỜI nhau chứ không có nấc cặp — nên phần chia theo
     bậc nằm ở `chiSoSau` làm bằng chứng, còn đề xuất đi theo dạng câu. */
  if (phamVi === 'toanHe') {
    const theoDang = new Map();
    for (const a of ds) {
      if (!Number.isFinite(a?.ms) || !a.mode) continue;
      const k = String(a.mode);
      if (!theoDang.has(k)) theoDang.set(k, []);
      theoDang.get(k).push(a);
    }
    for (const [dang, luotDs] of theoDang) {
      const hv = hocNguongHanhVi(luotDs);
      if (!hv) continue;
      const giay = Object.values(hv.theoNhom).map((x) => x.giay);
      ra.push(deXuat({
        ma: 'NG16', phamVi: 'dangCau', khoa: dang, bayGio, toiThieu: tt,
        cu: layNguong(bo, 'NG16', { dangCau: dang }),
        moi: +(giay.reduce((x, y) => x + y, 0) / giay.length).toFixed(1),
        phuongPhap: `phân vị ${hv.q} của thời gian trả lời trong CHÍNH dạng câu này — Wise (2017)`,
        coMau: luotDs.length,
        chiSoSau: hv.theoNhom,
        canCu: `phân vị ${hv.q} của riêng dạng "${dang}"; chia nhỏ theo bậc còn ở \`chiSoSau\` `
          + '— bảng ngưỡng không có nấc (dạng, bậc) ghép đôi nên đề xuất đi theo dạng câu',
      }));
    }
  }

  return { phamVi, khoa, coMau: ds.length, duMau: true, deXuat: ra };
}

/**
 * Học ở mọi phạm vi, và LÙI VỀ PHẠM VI RỘNG khi hẹp chưa đủ mẫu (mục 3.8.3).
 *
 * `lop` là danh sách phạm vi xếp từ HẸP tới RỘNG. Phạm vi nào không đủ `NG21` lượt
 * thì không sinh đề xuất — và vì phạm vi rộng hơn vẫn chạy, ngưỡng ở đó vẫn được
 * học. Đó chính là nghĩa của câu «nếu chưa đủ, hàm học ở phạm vi rộng hơn».
 */
export function hocMoiPhamVi(luots, bo, { bayGio = Date.now() } = {}) {
  const ra = [dungDeXuat(luots, bo, { phamVi: 'toanHe', khoa: null, bayGio })];
  for (const truong of ['mon', 'khoiLop', 'bac', 'dangCau']) {
    const m = new Map();
    for (const a of luots) {
      const k = a?.[truong];
      if (k == null || k === '') continue;
      if (!m.has(k)) m.set(k, []);
      m.get(k).push(a);
    }
    for (const [k, ds] of m) ra.push(dungDeXuat(ds, bo, { phamVi: truong, khoa: String(k), bayGio }));
  }
  return ra;
}
