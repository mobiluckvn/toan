/**
 * ĐÁNH GIÁ MÔ HÌNH NGƯỜI HỌC — kịch bản KB2 (mục 3.7.2.b), độ đo nhóm A (Bảng 3.27).
 *
 *     node tools/danh_gia_mo_hinh.mjs --mo-phong 1000      # không cần dữ liệu thật
 *     node tools/danh_gia_mo_hinh.mjs --vao docs/attempts.json
 *     node tools/danh_gia_mo_hinh.mjs --tu-may-chu          # cần khoá quản trị
 *
 * ── BÀI TOÁN ĐƯỢC ĐẶT Ở DẠNG DỰ ĐOÁN ──
 * Tại mỗi lượt thứ n của một người học ở một nút, dùng trạng thái mô hình SAU lượt
 * n−1 để dự đoán xác suất trả lời đúng ở lượt n, rồi đối chiếu với kết quả thật:
 *
 *     P(đúng ở lượt n) = P(Lₙ₋₁)·(1 − P(S)) + (1 − P(Lₙ₋₁))·P(G)
 *
 * `P(Lₙ₋₁)` ở đây là mức tinh thông SAU phép quên và TRƯỚC cập nhật Bayes — đúng
 * bằng trường `pTruoc` mà `applyAttempt` ghi ra. Lấy `p` (sau cập nhật) là nhìn
 * trộm đáp án: nó đã được sửa bằng chính kết quả cần dự đoán.
 *
 * ── BỐN BIẾN THỂ, ĐÚNG NHƯ MỤC 3.7.2.b ──
 *   M0  tỷ lệ đúng cơ bản — mốc so sánh, không có mô hình nào cả
 *   M1  BKT chuẩn (KHÔNG có cơ chế quên)
 *   M2  BKT có cơ chế quên  ← đây là mô hình đang chạy thật
 *   M3  M2 cộng lan truyền xuôi trên đồ thị
 *
 * ── ⚠ CHIA TẬP THEO NGƯỜI HỌC, KHÔNG THEO LƯỢT ──
 * Chia theo lượt thì các lượt của cùng một người học nằm ở cả hai bên, và mô hình
 * được hưởng lợi từ chính chuỗi mà nó phải dự đoán (mục 3.6.2).
 *
 * ⚠ MỘT ĐIỀU PHẢI NÓI RÕ KHI BÁO CÁO: bộ tham số BKT là hằng số khai trước, không
 *   ước lượng từ dữ liệu. Nên phép kiểm chéo ở đây KHÔNG chống quá khớp tham số —
 *   không có tham số nào được khớp cả. Nó chỉ làm cho khoảng biến thiên giữa các
 *   phần trở thành một ước lượng trung thực về độ ổn định của con số. Đọc thành
 *   "đã kiểm chéo nên không quá khớp" là đọc sai.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import {
  applyAttempt, bktUpdate, quenDan, paramsFor, DEFAULT_PARAMS, MASTERY_THRESHOLD,
} from '../web/functions/src/bkt.js';
import { datDoThi, duyetXuoi } from '../web/src/mon/tienganh/lib/doThi.js';
import { congHuong, BETA, NGUONG_TRAN } from '../web/src/mon/tienganh/lib/lantruyen.js';

const GOC = join(dirname(fileURLToPath(import.meta.url)), '..');
const NGAY = 86400000;

/* Đúng bốn pha mà hàm nền tính vào mô hình — ĐỌC TỪ MÃ NỀN để không lệch, cùng
   cách `tools/kiem_kho_du_lieu.mjs` làm. Gõ lại tay thì hai nơi trôi xa nhau và
   phép đánh giá đo một hệ thống khác với hệ thống đang chạy. */
function phaTinhVaoBKT() {
  const nen = readFileSync(join(GOC, 'web/functions/index.js'), 'utf8');
  const m = nen.match(/if \(!\[([^\]]+)\]\.includes\(a\.phase\)\) return;/);
  return (m?.[1].match(/'([a-z]+)'/g) || []).map((x) => x.slice(1, -1));
}

/* ═══════════════════════ NGUỒN DỮ LIỆU ═══════════════════════ */

async function napTuMayChu() {
  const khoa = process.env.GOOGLE_APPLICATION_CREDENTIALS;
  if (!khoa || !existsSync(khoa)) {
    console.error('✗ thiếu khoá quản trị.\n'
      + '  export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json\n'
      + '  ⚠ Khoá để NGOÀI thư mục kho — nó mở được toàn bộ dữ liệu dự án.');
    process.exit(1);
  }
  const { createRequire } = await import('node:module');
  const doi = createRequire(new URL('../web/functions/package.json', import.meta.url));
  const { initializeApp, cert } = doi('firebase-admin/app');
  const { getFirestore } = doi('firebase-admin/firestore');
  initializeApp({ credential: cert(JSON.parse(readFileSync(khoa, 'utf8'))) });
  const q = await getFirestore().collection('attempts').get();
  return q.docs.map((d) => d.data());
}

/**
 * MỐC LÀM SẠCH DỮ LIỆU — mục 3.7.1 đặt điều kiện tiền đề: chỉ dùng dữ liệu sau
 * ngày 23-8-2026. Trước mốc ấy đường ống ghi nhận có hai khiếm khuyết đã xác định.
 * Cắm thẳng vào công cụ chứ không để người chạy tự nhớ — quên một lần là cả bảng
 * số liệu sai mà không có gì báo.
 */
const MOC_SACH = Date.parse('2026-08-23T00:00:00Z');

/* ═══════════════════════ NGƯỜI HỌC MÔ PHỎNG (KB1) ═══════════════════════ */

/**
 * Sinh người học mô phỏng để KIỂM CHỨNG CHÍNH CÁC PHÉP ĐO này, và để chạy KB1.
 *
 * ⚠ RỦI RO PHẢI NÊU (mục 3.7.2.a): người học mô phỏng tuân theo đúng dạng mô hình
 *   đang được đánh giá, nên kết quả LẠC QUAN hơn thực tế. Giảm thiểu bằng cách cho
 *   tham số THẬT của người học mô phỏng KHÁC tham số mà mô hình sử dụng.
 *
 * Bộ sinh tất định (không dùng Math.random) để hai lần chạy cho cùng kết quả —
 * điều kiện để so hai đợt đo với nhau.
 */
function moPhong(soNguoi, dt) {
  /* Bộ sinh số giả ngẫu nhiên tất định — mulberry32. */
  let h = 0x9e3779b9;
  const rnd = () => {
    h = (h + 0x6d2b79f5) | 0;
    let t = Math.imul(h ^ (h >>> 15), 1 | h);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  /**
   * ⚠ DÙNG MÃ NÚT THẬT CỦA ĐỒ THỊ, không bịa `mp_nut_1`.
   *
   * Bản đầu bịa mã nút, và hậu quả là HAI giả thuyết của KB2 không kiểm được:
   * phân tầng "có / không có cạnh tiên quyết đi vào" cho ra một nhóm rỗng, và M3
   * không có cạnh nào để lan truyền nên trùng khít M2. Con số đẹp mà vô nghĩa.
   *
   * Lấy đủ cả hai loại nút — có tiên quyết đi vào (150 nút) và không — theo đúng
   * tỷ lệ của đồ thị, để hai nhóm phân tầng đều có mẫu.
   */
  const HOC_DUOC_LOAI = new Set(['vocabulary', 'vocabulary_item', 'grammar',
    'pronunciation', 'letter_sound', 'prior_knowledge', '?']);
  const coVao = new Set();
  for (const c of (dt?.canh || [])) {
    if ((c.loai || 'ban_do') !== 'trong_bai') coVao.add(c.truoc_khi);
  }
  const moiNut = Object.keys(dt?.nut || {})
    .filter((m) => HOC_DUOC_LOAI.has(dt.nut[m]?.t ?? '?'))
    .sort();
  const nutCoTQ = moiNut.filter((m) => coVao.has(m));
  const nutKhongTQ = moiNut.filter((m) => !coVao.has(m));
  if (!moiNut.length) throw new Error('cần đồ thị để mô phỏng trên mã nút thật');

  /* Tham số THẬT của người học — cố ý LỆCH khỏi tham số mô hình dùng, đúng biện
     pháp giảm thiểu rủi ro mà mục 3.7.2.a nêu. */
  const SLIP_THAT = 0.14; const GUESS_THAT = 0.22; const HOC_DUOC = 0.11;
  /* Xác suất quên THẬT mỗi ngày không gặp lại — mô hình KHÔNG biết con số này,
     nó chỉ có hàm mũ nửa đời 14 ngày. Lệch nhau là có chủ ý. */
  const QUEN_MOI_NGAY = 0.035;

  const ra = [];
  const soNut = 30;
  for (let u = 0; u < soNguoi; u += 1) {
    const nangLuc = 0.2 + 0.6 * rnd();
    let t = Date.parse('2026-08-24T08:00:00Z');
    const daHoc = [];

    const motLoat = (nut, trangThai) => {
      let biet = trangThai;
      const soLuot = 3 + Math.floor(rnd() * 5);
      for (let i = 0; i < soLuot; i += 1) {
        const dung = biet ? rnd() > SLIP_THAT : rnd() < GUESS_THAT;
        ra.push({
          learnerId: `mp_${u}`, bktUnit: nut, correct: dung, phase: 'practice',
          ts: t, ms: 4000 + Math.floor(rnd() * 12000), hintsUsed: 0,
          mustPass: false, mon: 'tienganh',
        });
        if (!biet && rnd() < HOC_DUOC + nangLuc * 0.1) biet = true;
        t += 45000 + Math.floor(rnd() * 120000);
      }
      return biet;
    };

    /* Đợt học: mỗi buổi vài nút, cách nhau một hai ngày. */
    for (let k = 0; k < soNut; k += 1) {
      /* Trộn hai loại nút theo tỷ lệ của đồ thị để cả hai nhóm phân tầng có mẫu. */
      const dungCoTQ = rnd() < 0.35 && nutCoTQ.length;
      const kho = dungCoTQ ? nutCoTQ : nutKhongTQ;
      const nut = kho[Math.floor(rnd() * kho.length)];
      if (daHoc.some((x) => x.nut === nut)) { k -= 1; continue; }
      const biet = motLoat(nut, rnd() < nangLuc * 0.3);
      daHoc.push({ nut, biet, luc: t });
      t += (1 + Math.floor(rnd() * 2)) * NGAY;
    }

    /**
     * ĐỢT ÔN LẠI SAU MỘT QUÃNG NGHỈ — thiếu đợt này thì cơ chế quên KHÔNG BAO GIỜ
     * được kích hoạt trong mô phỏng, vì mọi lượt của một nút nằm liền nhau trong
     * cùng một buổi. Bản đầu thiếu đúng chỗ này: 100% số lượt rơi vào nhóm "cách
     * dưới 7 ngày", nên M1 và M2 trùng khít và giả thuyết H1 không kiểm được.
     */
    for (const x of daHoc) {
      if (rnd() > 0.5) continue;
      const nghi = 7 + Math.floor(rnd() * 25);              // 7–31 ngày
      t = Math.max(t, x.luc + nghi * NGAY);
      /* Quên thật theo thời gian — người học mô phỏng quên theo dạng hàm KHÁC với
         hàm mũ nửa đời mà mô hình dùng. */
      const quen = x.biet && rnd() < 1 - (1 - QUEN_MOI_NGAY) ** nghi;
      motLoat(x.nut, x.biet && !quen);
      t += (1 + Math.floor(rnd() * 3)) * NGAY;
    }
  }
  return ra.sort((a, b) => a.ts - b.ts);
}

/* ═══════════════════════ CHẠY LẠI NHẬT KÝ ═══════════════════════ */

/** Xác suất trả lời đúng ở lượt tới, từ mức tinh thông TRƯỚC lượt ấy. */
const duDoan = (pTruoc, tham) => pTruoc * (1 - tham.slip) + (1 - pTruoc) * tham.guess;

/**
 * Chạy lại toàn bộ nhật ký của MỘT người học theo một biến thể mô hình.
 * Trả về `[{ duDoan, that, coTienQuyet, cachNgay, nut }]`.
 */
function chayLai(ds, bienThe, { dt = null } = {}) {
  const ho = new Map();          // nút → hồ sơ
  const ra = [];
  let phaiTinhLai = true;
  let mapCongHuong = {};

  for (const a of ds) {
    const nut = a.bktUnit;
    const cu = ho.get(nut);
    const tham = paramsFor(a);

    /* Mức tinh thông TRƯỚC lượt này. */
    let p0 = cu?.p ?? DEFAULT_PARAMS.L0;
    let cach = 0;
    if (Number.isFinite(cu?.lastSeen)) cach = Math.max(0, (a.ts - cu.lastSeen) / NGAY);

    if (bienThe !== 'M1') p0 = quenDan(p0, cach);      // M0/M2/M3 có cơ chế quên

    if (bienThe === 'M3' && dt) {
      /* Cộng hưởng xuôi: chỉ tính lại khi TẬP NGUỒN đổi (một nút vừa vượt ngưỡng).
         Tính lại mỗi lượt thì đúng nhưng chậm, mà kết quả y hệt — tập nguồn không
         đổi thì ánh xạ cộng hưởng cũng không đổi. */
      if (phaiTinhLai) {
        const m = {};
        for (const [k, v] of ho) m[k] = v;
        mapCongHuong = congHuong(dt, m);
        phaiTinhLai = false;
      }
      /* Chỉ NÂNG, không hạ — và không bao giờ vượt trần (chốt 3 của Thuật toán 3.7). */
      const nang = mapCongHuong[nut];
      if (Number.isFinite(nang) && nang > p0) p0 = Math.min(NGUONG_TRAN, nang);
    }

    ra.push({
      duDoan: bienThe === 'M0' ? null : duDoan(p0, tham),
      that: a.correct ? 1 : 0,
      nut,
      cachNgay: cach,
      lanThu: (cu?.nAttempts ?? 0) + 1,
    });

    /* Cập nhật hồ sơ. M1 bỏ phép quên nên phải tự cập nhật chứ không gọi
       `applyAttempt` (hàm ấy LUÔN áp phép quên — đó là mô hình đang chạy). */
    const p = bktUpdate(p0, !!a.correct, tham);
    const truocDat = (cu?.p ?? 0) >= MASTERY_THRESHOLD;
    ho.set(nut, {
      p, lastSeen: a.ts, nAttempts: (cu?.nAttempts ?? 0) + 1,
    });
    if (bienThe === 'M3' && (p >= MASTERY_THRESHOLD) !== truocDat) phaiTinhLai = true;
  }
  return ra;
}

/* ═══════════════════════ ĐỘ ĐO NHÓM A ═══════════════════════ */

/**
 * AUC theo lối hạng (Mann–Whitney), có XỬ LÝ ĐỒNG HẠNG bằng hạng trung bình.
 *
 * ⚠ Đồng hạng không phải chuyện hiếm ở đây mà là chuyện THƯỜNG: lượt đầu tiên của
 * mọi nút đều cho ra đúng một giá trị dự đoán (vì đều xuất phát từ P(L₀)). Dùng
 * công thức không xử lý đồng hạng thì AUC bị thổi lên một cách có hệ thống.
 */
function auc(diem) {
  const duong = diem.filter((d) => d.that === 1).length;
  const am = diem.length - duong;
  if (!duong || !am) return null;
  const sap = [...diem].sort((a, b) => a.duDoan - b.duDoan);
  const hang = new Array(sap.length);
  for (let i = 0; i < sap.length;) {
    let j = i;
    while (j + 1 < sap.length && sap[j + 1].duDoan === sap[i].duDoan) j += 1;
    const tb = (i + j + 2) / 2;          // hạng 1-based, trung bình cho cả cụm
    for (let k = i; k <= j; k += 1) hang[k] = tb;
    i = j + 1;
  }
  let tongHangDuong = 0;
  sap.forEach((d, i) => { if (d.that === 1) tongHangDuong += hang[i]; });
  return (tongHangDuong - (duong * (duong + 1)) / 2) / (duong * am);
}

const rmse = (diem) =>
  Math.sqrt(diem.reduce((s, d) => s + (d.duDoan - d.that) ** 2, 0) / diem.length);

const doChinhXac = (diem) =>
  diem.filter((d) => (d.duDoan >= 0.5 ? 1 : 0) === d.that).length / diem.length;

const lopDaSo = (diem) => {
  const d1 = diem.filter((d) => d.that === 1).length;
  return Math.max(d1, diem.length - d1) / diem.length;
};

/**
 * SAI LỆCH HIỆU CHUẨN — Bảng 3.27 gọi đây là độ đo QUAN TRỌNG NHẤT với hệ thống
 * này, và lý do rất cụ thể: ngưỡng θ = 0,85 chỉ có nghĩa nếu phát biểu "mô hình dự
 * đoán 85%" thực sự tương ứng với "trả lời đúng khoảng 85% số lần". Mô hình xếp
 * hạng giỏi (AUC cao) mà hiệu chuẩn lệch thì ngưỡng ấy đặt ở đâu cũng sai.
 *
 * Trả về 10 nhóm kèm cỡ mẫu, và ECE — trung bình có trọng số của |dự đoán − thật|.
 */
function hieuChuan(diem, soNhom = 10) {
  const nhom = Array.from({ length: soNhom }, () => ({ n: 0, tongDuDoan: 0, tongThat: 0 }));
  for (const d of diem) {
    const i = Math.min(soNhom - 1, Math.floor(d.duDoan * soNhom));
    nhom[i].n += 1; nhom[i].tongDuDoan += d.duDoan; nhom[i].tongThat += d.that;
  }
  let ece = 0;
  const bang = nhom.map((b, i) => {
    const tbDuDoan = b.n ? b.tongDuDoan / b.n : null;
    const tiLeThat = b.n ? b.tongThat / b.n : null;
    if (b.n) ece += (b.n / diem.length) * Math.abs(tbDuDoan - tiLeThat);
    return {
      khoang: `${(i / soNhom).toFixed(1)}–${((i + 1) / soNhom).toFixed(1)}`,
      n: b.n, tbDuDoan, tiLeThat,
    };
  });
  return { bang, ece };
}

function doTatCa(diem) {
  if (!diem.length) return null;
  return {
    n: diem.length,
    auc: auc(diem),
    rmse: rmse(diem),
    doChinhXac: doChinhXac(diem),
    lopDaSo: lopDaSo(diem),
    ...hieuChuan(diem),
  };
}

/* ═══════════════════════ KIỂM CHÉO THEO NGƯỜI HỌC ═══════════════════════ */

function chiaPhan(dsNguoi, soPhan) {
  /* Chia tất định theo thứ tự mã người học đã sắp — không ngẫu nhiên, để hai lần
     chạy cho cùng kết quả. */
  const ten = [...dsNguoi.keys()].sort();
  const phan = Array.from({ length: soPhan }, () => []);
  ten.forEach((t, i) => phan[i % soPhan].push(t));
  return phan;
}

/* ═══════════════════════ CHẠY ═══════════════════════ */

function chay({ ban, dt, soPhan }) {
  const PHA = phaTinhVaoBKT();
  const truoc = ban.length;
  let ban2 = ban.filter((a) => a?.learnerId && a?.bktUnit && PHA.includes(a.phase || 'practice'));
  const boPha = truoc - ban2.length;

  /* Mốc làm sạch — chỉ áp cho dữ liệu THẬT, dữ liệu mô phỏng sinh sau mốc rồi. */
  const truocMoc = ban2.filter((a) => Number.isFinite(a.ts) && a.ts < MOC_SACH).length;
  ban2 = ban2.filter((a) => !Number.isFinite(a.ts) || a.ts >= MOC_SACH);

  const theoNguoi = new Map();
  for (const a of ban2) {
    if (!theoNguoi.has(a.learnerId)) theoNguoi.set(a.learnerId, []);
    theoNguoi.get(a.learnerId).push(a);
  }
  for (const ds of theoNguoi.values()) ds.sort((x, y) => (x.ts ?? 0) - (y.ts ?? 0));

  const coTienQuyet = new Set();
  if (dt) {
    for (const c of (dt.canh || [])) {
      if ((c.loai || 'ban_do') !== 'trong_bai') coTienQuyet.add(c.truoc_khi);
    }
  }

  const BIEN_THE = ['M0', 'M1', 'M2', 'M3'];
  const phan = chiaPhan(theoNguoi, soPhan);
  const kq = {};

  for (const bt of BIEN_THE) {
    const tatCa = [];
    const theoPhan = [];
    for (const ten of phan) {
      const diemPhan = [];
      for (const t of ten) {
        const d = chayLai(theoNguoi.get(t), bt, { dt });
        diemPhan.push(...d);
      }
      theoPhan.push(diemPhan);
      tatCa.push(...diemPhan);
    }
    /* M0 không có mô hình: dự đoán bằng tỷ lệ đúng của CHÍNH TẬP HUẤN LUYỆN
       (các phần khác), không phải của cả tập — lấy cả tập là nhìn trộm đáp án. */
    if (bt === 'M0') {
      for (let i = 0; i < theoPhan.length; i += 1) {
        const khac = theoPhan.filter((_, j) => j !== i).flat();
        const tiLe = khac.length ? khac.filter((d) => d.that === 1).length / khac.length : 0.5;
        theoPhan[i].forEach((d) => { d.duDoan = tiLe; });
      }
    }
    const gop = theoPhan.flat();
    kq[bt] = {
      chung: doTatCa(gop),
      theoPhan: theoPhan.map((p) => {
        const m = doTatCa(p);
        return m ? { n: m.n, auc: m.auc, rmse: m.rmse } : null;
      }),
      phanTang: {
        coTienQuyet: doTatCa(gop.filter((d) => coTienQuyet.has(d.nut))),
        khongTienQuyet: doTatCa(gop.filter((d) => !coTienQuyet.has(d.nut))),
        cachDuoi7Ngay: doTatCa(gop.filter((d) => d.cachNgay < 7)),
        cachTu7Ngay: doTatCa(gop.filter((d) => d.cachNgay >= 7)),
      },
    };
  }
  return { kq, thongKe: { tongBanGhi: truoc, boPha, truocMoc, dung: ban2.length, soNguoi: theoNguoi.size, soPhan } };
}

/* ═══════════════════════ BẢN IN ═══════════════════════ */

const s4 = (x) => (x === null || x === undefined ? '   —  ' : x.toFixed(4));
const s1 = (x) => (x === null || x === undefined ? '  — ' : `${(x * 100).toFixed(1)}%`);

function inRa(r, nguon) {
  const { kq, thongKe: t } = r;
  console.log(`\n══════ KB2 · ĐÁNH GIÁ MÔ HÌNH NGƯỜI HỌC ══════`);
  console.log(`  nguồn: ${nguon}`);
  console.log(`  ${t.tongBanGhi} bản ghi → dùng ${t.dung}`
    + `  (bỏ ${t.boPha} vì sai pha, ${t.truocMoc} vì trước mốc 23-8-2026)`);
  console.log(`  ${t.soNguoi} người học · kiểm chéo ${t.soPhan} phần, CHIA THEO NGƯỜI HỌC`);

  if (!kq.M2?.chung) { console.log('\n  ✗ không đủ dữ liệu để đo.\n'); return; }

  console.log(`\n── BỐN BIẾN THỂ ──`);
  console.log(`  ${'mô hình'.padEnd(34)}${'AUC'.padStart(8)}${'RMSE'.padStart(9)}`
    + `${'ch.xác'.padStart(9)}${'lớp đa số'.padStart(11)}${'ECE'.padStart(9)}`);
  const TEN = {
    M0: 'M0 · tỷ lệ đúng cơ bản',
    M1: 'M1 · BKT chuẩn',
    M2: 'M2 · BKT + cơ chế quên  ← đang chạy',
    M3: 'M3 · M2 + lan truyền xuôi',
  };
  for (const bt of ['M0', 'M1', 'M2', 'M3']) {
    const c = kq[bt]?.chung;
    if (!c) continue;
    console.log(`  ${TEN[bt].padEnd(34)}${s4(c.auc).padStart(8)}${s4(c.rmse).padStart(9)}`
      + `${s1(c.doChinhXac).padStart(9)}${s1(c.lopDaSo).padStart(11)}${s4(c.ece).padStart(9)}`);
  }
  console.log(`\n  ⚠ Độ chính xác phải đọc KÈM cột "lớp đa số": dữ liệu học tập lệch về phía`);
  console.log(`    trả lời đúng, nên một mô hình đoán bừa "luôn đúng" cũng đạt đúng cột ấy.`);
  console.log(`  ⚠ RMSE chỉ có nghĩa khi SO GIỮA các biến thể, không so với ngưỡng tuyệt đối.`);

  console.log(`\n── ĐỘ ỔN ĐỊNH GIỮA CÁC PHẦN KIỂM CHÉO (AUC) ──`);
  for (const bt of ['M1', 'M2', 'M3']) {
    const ds = (kq[bt]?.theoPhan || []).filter(Boolean).map((p) => p.auc).filter((x) => x !== null);
    if (!ds.length) continue;
    const tb = ds.reduce((a, b) => a + b, 0) / ds.length;
    const sd = Math.sqrt(ds.reduce((s, x) => s + (x - tb) ** 2, 0) / ds.length);
    console.log(`  ${bt}: ${ds.map((x) => x.toFixed(3)).join(' · ')}`
      + `   → trung bình ${tb.toFixed(4)} ± ${sd.toFixed(4)}`);
  }

  console.log(`\n── PHÂN TẦNG (giả thuyết H1 và H2 của KB2) ──`);
  console.log(`  H1 — cơ chế quên giúp nhiều hơn ở lượt cách lần trước ≥ 7 ngày:`);
  for (const nhom of ['cachDuoi7Ngay', 'cachTu7Ngay']) {
    const a = kq.M1?.phanTang[nhom]; const b = kq.M2?.phanTang[nhom];
    if (!a || !b) continue;
    const ten = nhom === 'cachDuoi7Ngay' ? 'cách < 7 ngày ' : 'cách ≥ 7 ngày ';
    console.log(`     ${ten} n=${String(b.n).padStart(6)}   M1 AUC ${s4(a.auc)}`
      + `  →  M2 AUC ${s4(b.auc)}   (chênh ${((b.auc - a.auc) >= 0 ? '+' : '')}${(b.auc - a.auc).toFixed(4)})`);
  }
  console.log(`  H2 — lan truyền chỉ cải thiện ở nút CÓ cạnh tiên quyết đi vào:`);
  for (const nhom of ['coTienQuyet', 'khongTienQuyet']) {
    const a = kq.M2?.phanTang[nhom]; const b = kq.M3?.phanTang[nhom];
    if (!a || !b) continue;
    const ten = nhom === 'coTienQuyet' ? 'có tiên quyết ' : 'không tiên quyết';
    console.log(`     ${ten} n=${String(b.n).padStart(6)}   M2 AUC ${s4(a.auc)}`
      + `  →  M3 AUC ${s4(b.auc)}   (chênh ${((b.auc - a.auc) >= 0 ? '+' : '')}${(b.auc - a.auc).toFixed(4)})`);
  }

  console.log(`\n── HIỆU CHUẨN CỦA M2 (mô hình đang chạy) ──`);
  console.log(`  ${'khoảng dự đoán'.padEnd(16)}${'n'.padStart(8)}${'dự đoán TB'.padStart(13)}${'đúng THẬT'.padStart(12)}   lệch`);
  for (const b of kq.M2.chung.bang) {
    if (!b.n) continue;
    const lech = b.tbDuDoan - b.tiLeThat;
    const dau = Math.abs(lech) >= 0.10 ? '  ⚠' : '';
    console.log(`  ${b.khoang.padEnd(16)}${String(b.n).padStart(8)}${s1(b.tbDuDoan).padStart(13)}`
      + `${s1(b.tiLeThat).padStart(12)}   ${(lech >= 0 ? '+' : '')}${(lech * 100).toFixed(1)} điểm${dau}`);
  }
  console.log(`\n  ECE = ${kq.M2.chung.ece.toFixed(4)}`);
  console.log(`  ⚠ Ngưỡng θ = ${MASTERY_THRESHOLD} chỉ có nghĩa nếu dòng "0.8–0.9" cho thấy dự đoán`);
  console.log(`    và tỷ lệ đúng thật xấp xỉ nhau. Lệch lớn ở dòng ấy thì phải hiệu chỉnh θ,`);
  console.log(`    chứ không phải giữ nguyên rồi giải thích bằng lời.`);
  console.log('');
}

/* ═══════════════════════ TỰ KIỂM ═══════════════════════ */

/**
 * Kiểm chính ba hàm độ đo bằng những trường hợp tính được BẰNG TAY.
 *
 * Không đưa vào `web/test/` vì đây là mã của `tools/`, không phải mã chạy trong
 * ứng dụng — và vì con số "92 tệp cổng" là một con số luận văn dẫn ra, thêm tệp
 * vào đó là phải sửa cả Bảng 3.25 lẫn mục 3.5.2 cho một thứ không thuộc bản chạy.
 *
 * Trường hợp ĐỒNG HẠNG là trường hợp quan trọng nhất: lượt đầu của mọi nút đều cho
 * ra cùng một giá trị dự đoán (đều xuất phát từ P(L₀)), nên công thức AUC không xử
 * lý đồng hạng sẽ thổi con số lên một cách có hệ thống.
 */
function tuKiem() {
  const loi = [];
  const gan = (a, b, ten, sai = 1e-9) => {
    /* `null` là một KẾT QUẢ hợp lệ (AUC không định nghĩa được khi chỉ có một lớp),
       nên phải so bằng nhau chứ không coi mọi null là hỏng. */
    const hong = b === null ? a !== null : (a === null || Math.abs(a - b) > sai);
    if (hong) loi.push(`${ten}: được ${a}, đợi ${b}`);
  };
  const d = (duDoan, that) => ({ duDoan, that });

  /* AUC tách bạch hoàn toàn → 1; ngược hoàn toàn → 0. */
  gan(auc([d(0.9, 1), d(0.8, 1), d(0.2, 0), d(0.1, 0)]), 1, 'AUC tách bạch');
  gan(auc([d(0.1, 1), d(0.2, 1), d(0.8, 0), d(0.9, 0)]), 0, 'AUC ngược');
  /* ĐỒNG HẠNG hoàn toàn → đúng 0,5. Không xử lý đồng hạng thì ra 0 hoặc 1. */
  gan(auc([d(0.5, 1), d(0.5, 0), d(0.5, 1), d(0.5, 0)]), 0.5, 'AUC đồng hạng');
  /* Đồng hạng một phần: 2 dương (0,9 · 0,5) · 2 âm (0,5 · 0,1).
     Cặp (0,9;0,5)=1 · (0,9;0,1)=1 · (0,5;0,5)=0,5 · (0,5;0,1)=1 → 3,5/4. */
  gan(auc([d(0.9, 1), d(0.5, 1), d(0.5, 0), d(0.1, 0)]), 3.5 / 4, 'AUC đồng hạng một phần');
  /* Một lớp rỗng thì AUC không định nghĩa được — phải trả null, không trả 0,5. */
  gan(auc([d(0.9, 1), d(0.8, 1)]), null, 'AUC một lớp');

  gan(rmse([d(1, 1), d(0, 0)]), 0, 'RMSE khớp hoàn toàn');
  gan(rmse([d(0.5, 1), d(0.5, 0)]), 0.5, 'RMSE nửa vời');
  gan(doChinhXac([d(0.9, 1), d(0.1, 0), d(0.9, 0)]), 2 / 3, 'độ chính xác');
  gan(lopDaSo([d(0.9, 1), d(0.9, 1), d(0.1, 0)]), 2 / 3, 'lớp đa số');

  /* Hiệu chuẩn: hai nhóm, mỗi nhóm lệch 0,3 → ECE = 0,3. */
  const hc = hieuChuan([d(0.05, 1), d(0.05, 0), d(0.95, 1), d(0.95, 0)], 10);
  gan(hc.ece, 0.45, 'ECE');            // |0,05−0,5|=0,45 và |0,95−0,5|=0,45

  /* Xác suất dự đoán: p=1 thì đúng bằng 1−slip; p=0 thì đúng bằng guess. */
  gan(duDoan(1, DEFAULT_PARAMS), 1 - DEFAULT_PARAMS.slip, 'dự đoán khi đã thạo');
  gan(duDoan(0, DEFAULT_PARAMS), DEFAULT_PARAMS.guess, 'dự đoán khi chưa thạo');

  if (loi.length) {
    console.error(`\n✗ TỰ KIỂM HỎNG (${loi.length}):`);
    loi.forEach((x) => console.error(`   ${x}`));
    return 1;
  }
  console.log('\n✓ tự kiểm: 13/13 phép đo đúng (kể cả bốn trường hợp ĐỒNG HẠNG của AUC)\n');
  return 0;
}

/* ═══════════════════════ CỬA VÀO ═══════════════════════ */

const cd = process.argv.slice(2);
const co = (t) => cd.includes(t);
const lay = (t, mac) => { const i = cd.indexOf(t); return i >= 0 ? cd[i + 1] : mac; };

/* Nạp đồ thị TRƯỚC, vì bộ mô phỏng cần mã nút thật của nó. */
let dt = null;
const fDoThi = join(GOC, 'web/public/content/tienganh/do_thi.json');
if (existsSync(fDoThi)) { dt = JSON.parse(readFileSync(fDoThi, 'utf8')); datDoThi(dt); }

if (co('--tu-kiem')) process.exit(tuKiem());

let ban; let nguon;
if (co('--mo-phong')) {
  const n = Number(lay('--mo-phong', 1000)) || 1000;
  ban = moPhong(n, dt);
  nguon = `${n} người học MÔ PHỎNG (tất định, trên mã nút THẬT của đồ thị)`
    + ` — ⚠ không phải dữ liệu thật, xem chú thích moPhong()`;
} else if (co('--vao')) {
  const f = join(GOC, lay('--vao'));
  const d = JSON.parse(readFileSync(f, 'utf8'));
  ban = Array.isArray(d) ? d : (d.ban || d.attempts || []);
  nguon = f;
} else if (co('--tu-may-chu')) {
  ban = await napTuMayChu();
  nguon = 'Firestore · collection attempts';
} else {
  console.error('Dùng một trong:\n'
    + '  --mo-phong 1000        người học mô phỏng, không cần dữ liệu thật\n'
    + '  --vao <tệp.json>       nhật ký đã kết xuất\n'
    + '  --tu-may-chu           đọc thẳng Firestore (cần khoá quản trị)');
  process.exit(1);
}

const r = chay({ ban, dt, soPhan: Number(lay('--phan', 5)) || 5 });
inRa(r, nguon);
const ra = join(GOC, 'docs/kb2_ket_qua.json');
writeFileSync(ra, JSON.stringify(r, null, 2));
console.log(`  → đã ghi ${ra}\n`);
