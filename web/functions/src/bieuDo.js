/**
 * BIỂU ĐỒ CỦA MỘT EM — cho màn chi tiết học sinh ở phía cô giáo.
 *
 * Bảng cô giáo chỉ nhìn 7 ngày; sổ bố mẹ cũng vậy. Cô cần thêm câu hỏi thứ ba:
 * "từ lúc vào học tới giờ em đi lên hay đi xuống". Câu ấy phải đọc TOÀN BỘ nhật ký
 * của em, nên dựng ở máy chủ (một em vài nghìn lượt) rồi trả về vài chục con số —
 * chứ không kéo nghìn dòng về máy cô.
 *
 * Hàm thuần: nhận lượt, trả số. Không đọc Firestore — cổng chạy được bằng `node`.
 *
 * ── NĂM CHUỖI ──
 *   tuan[]      mỗi tuần (thứ Hai đầu tuần, giờ Việt Nam): lượt, tỉ lệ đúng lần đầu
 *               theo môn, phút học, số buổi, giây trung vị mỗi câu
 *   tichLuy     số bài ĐÃ HỌC (chạm tới lần đầu) cộng dồn theo tuần, theo môn
 *   theoLanGap  tỉ lệ đúng lần đầu ở lần gặp thứ k cùng một nút kiến thức
 *   gioHoc      số buổi theo giờ bắt đầu, khung nửa giờ
 *
 * ⚠ "Bài đã học" chứ KHÔNG phải "bài đạt": nhật ký không ghi lúc bài được công nhận
 *   đạt (sổ tiến độ chỉ giữ mốc lần làm cuối). Gọi nó là "bài đạt" là nói quá.
 */
import { minutesStudied } from './report.js';
import { applyAttempt, quenDan } from './bkt.js';
import { layNguong, boNguong } from './nguong.js';

const NGAY = 86400000;
const LECH_VN = 7 * 3600000;
/** Lần gặp thứ mấy thì gộp đuôi — sau ngần ấy lần mỗi điểm chỉ còn vài lượt. */
export const LAN_GAP_TOI_DA = 8;

export const monCua = (a) => (a?.mon === 'tienganh' || /^DL:TA/.test(a?.microId || '')
  ? 'tienganh' : 'toan');

/** Thứ Hai đầu tuần (giờ VN) của một mốc, dạng 'YYYY-MM-DD'. */
export function dauTuan(ms) {
  const d = new Date(ms + LECH_VN);
  const lui = (d.getUTCDay() + 6) % 7;
  return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - lui))
    .toISOString().slice(0, 10);
}

const lanDau = (a) => (a.tries ?? 1) <= 1;
const tiLe = (dung, tong) => (tong ? Math.round((100 * dung) / tong) : null);
const trungVi = (xs) => {
  if (!xs.length) return null;
  const s = [...xs].sort((x, y) => x - y);
  const g = s.length >> 1;
  return s.length % 2 ? s[g] : (s[g - 1] + s[g]) / 2;
};

export function buildBieuDo(luot) {
  const ds = (luot || []).filter((a) => Number.isFinite(a?.ts)).sort((x, y) => x.ts - y.ts);
  if (!ds.length) return { soLuot: 0, tuan: [], theoLanGap: [], gioHoc: [], mon: [] };

  /* Đủ MỌI tuần từ tuần đầu tới tuần cuối — tuần nghỉ học là một điểm 0, không phải
     một khoảng trống bị nối tắt trên đường. */
  const dau = Date.parse(`${dauTuan(ds[0].ts)}T00:00:00Z`);
  const cuoi = Date.parse(`${dauTuan(ds[ds.length - 1].ts)}T00:00:00Z`);
  const tuan = new Map();
  for (let t = dau; t <= cuoi; t += 7 * NGAY) {
    tuan.set(new Date(t).toISOString().slice(0, 10), { luot: [], buoi: new Set() });
  }
  for (const a of ds) {
    const o = tuan.get(dauTuan(a.ts));
    o.luot.push(a);
    if (a.sessionId) o.buoi.add(a.sessionId);
  }

  const mon = [...new Set(ds.map(monCua))].sort();
  const daHoc = Object.fromEntries(mon.map((m) => [m, new Set()]));
  const dsTuan = [];
  for (const [ngay, o] of tuan) {
    const theoMon = {};
    for (const m of mon) {
      const cua = o.luot.filter((a) => monCua(a) === m);
      const dau1 = cua.filter(lanDau);
      for (const a of cua) if (a.microId) daHoc[m].add(a.microId);
      theoMon[m] = {
        luot: cua.length,
        dungLanDau: tiLe(dau1.filter((a) => a.correct).length, dau1.length),
        baiDaHoc: daHoc[m].size,
      };
    }
    dsTuan.push({
      tuan: ngay,
      luot: o.luot.length,
      buoi: o.buoi.size,
      phut: minutesStudied(o.luot),
      giayMoiCau: (() => {
        const g = trungVi(o.luot.filter((a) => a.ms > 0).map((a) => a.ms / 1000));
        return g === null ? null : Math.round(g * 10) / 10;
      })(),
      mon: theoMon,
    });
  }

  /* Lần gặp thứ k: đếm theo NÚT (bktUnit) — đó là đơn vị mô hình người học theo dõi. */
  const dem = new Map();
  const gap = Array.from({ length: LAN_GAP_TOI_DA }, () => ({ tong: 0, dung: 0 }));
  for (const a of ds) {
    if (!lanDau(a)) continue;
    const k = a.bktUnit || a.microId;
    if (!k) continue;
    const n = (dem.get(k) || 0) + 1;
    dem.set(k, n);
    const o = gap[Math.min(n, LAN_GAP_TOI_DA) - 1];
    o.tong += 1;
    if (a.correct) o.dung += 1;
  }
  const theoLanGap = gap.map((o, i) => ({ lan: i + 1, tong: o.tong, dung: tiLe(o.dung, o.tong) }))
    .filter((o) => o.tong > 0);

  /* Giờ bắt đầu buổi: lượt SỚM NHẤT của mỗi buổi, khung nửa giờ, giờ VN. */
  const batDau = new Map();
  for (const a of ds) if (a.sessionId && !batDau.has(a.sessionId)) batDau.set(a.sessionId, a.ts);
  const khung = new Map();
  for (const ts of batDau.values()) {
    const d = new Date(ts + LECH_VN);
    const k = d.getUTCHours() * 2 + (d.getUTCMinutes() >= 30 ? 1 : 0);
    khung.set(k, (khung.get(k) || 0) + 1);
  }
  const gioHoc = [...khung.entries()].sort((x, y) => x[0] - y[0]).map(([k, n]) => ({
    khung: `${String(k >> 1).padStart(2, '0')}:${k % 2 ? '30' : '00'}`, buoi: n,
  }));

  return {
    soLuot: ds.length,
    tuLuc: ds[0].ts,
    denLuc: ds[ds.length - 1].ts,
    mon,
    tuan: dsTuan,
    theoLanGap,
    gioHoc,
  };
}

/* ═══════════ CÁC HÌNH CỦA LUẬN VĂN, DỰNG TỪ NHẬT KÝ CỦA MỘT EM ═══════════
 *
 * Năm chuỗi trên là thống kê đếm. Phần dưới là MÔ HÌNH NGƯỜI HỌC: chạy lại đúng
 * `applyAttempt` (BKT có tính quên, `bkt.js`) trên từng lượt của em, theo thứ tự
 * thời gian, với đồng hồ là giờ của chính lượt ấy — y như hàm nền `onAttempt` đã
 * chạy khi em học. Nhờ vậy cô thấy được các hình của luận văn trên dữ liệu của
 * đúng em này:
 *
 *   duongCong     mục 2.5 · đường cong học tập: tỉ lệ LỖI theo lần luyện thứ k
 *                 tại cùng một nút, theo môn; bỏ điểm có ít hơn `MAU_TOI_THIEU` lượt
 *                 (đúng lời dặn của mục ấy: "không vẽ những điểm có quá ít dữ liệu")
 *   nutVung       số nút đạt θ theo tuần — theo P(L) đã lưu, và theo P(L) sau khi
 *                 tính quên tới cuối tuần (ý của Hình 3.13, trải theo thời gian)
 *   tinhTrang     Bảng 3.9 / Hình 3.10: đếm nút theo tình trạng ở thời điểm hiện tại
 *   hoSoQuen      Hình 3.13: phân bố nút theo dải P(L), trước và sau khi tính quên
 *   dienBien      Hình 3.14 / 3.16: P(L) và số lần sai liên tiếp qua từng lượt, cho
 *                 vài nút đáng xem nhất (luyện nhiều nhất, và nút từng "đang mắc")
 *
 * ⚠ Ngưỡng đọc từ bộ đang hành (`boNguong()`), nên hàm nền phải `layBoNguong(db)`
 *   trước khi gọi — như mọi chỗ khác dùng BKT.
 */

/** Điểm của đường cong học tập phải có ít nhất ngần này lượt mới vẽ. */
export const MAU_TOI_THIEU = 10;
/** Đường cong học tập xét tới lần luyện thứ mấy. */
export const LAN_LUYEN_TOI_DA = 12;
/** Số nút đưa vào hình diễn biến. */
export const SO_NUT_DIEN_BIEN = 8;

export function buildMoHinh(luot, { now = Date.now() } = {}) {
  const bo = boNguong();
  const theta = layNguong(bo, 'NG07');
  const thetaYeu = layNguong(bo, 'NG08');
  const nguongMac = layNguong(bo, 'NG09');
  const ngayQuen = layNguong(bo, 'NG13');
  const nuaDoi = layNguong(bo, 'NG06');
  const tua = layNguong(bo, 'NG25');
  const nguong = { theta, thetaYeu, nguongMac, ngayQuen, nuaDoi, tua };

  const ds = (luot || []).filter((a) => Number.isFinite(a?.ts) && (a.bktUnit || a.microId))
    .sort((x, y) => x.ts - y.ts);
  if (!ds.length) {
    return { nguong, duongCong: {}, nutVung: [], tinhTrang: null, hoSoQuen: null, dienBien: [] };
  }

  const hoSo = new Map();          // nút → tài liệu mastery sau lượt gần nhất
  const monNut = new Map();
  const vet = new Map();           // nút → [{k, ts, p, pTruoc, sai, dung}]
  const lanThu = new Map();        // nút → số lần luyện (lần thử đầu) đã gặp
  const loi = {};                  // mon → [{tong, sai}] theo lần luyện

  for (const a of ds) {
    const nut = a.bktUnit || a.microId;
    const mon = monCua(a);
    monNut.set(nut, mon);
    const sau = applyAttempt(hoSo.get(nut), a, () => a.ts);
    hoSo.set(nut, sau);
    if (!vet.has(nut)) vet.set(nut, []);
    vet.get(nut).push({ ts: a.ts, p: +sau.p.toFixed(3), pTruoc: +sau.pTruoc.toFixed(3),
      sai: sau.saiLienTiep, dung: !!a.correct });

    if ((a.tries ?? 1) <= 1) {
      /* Đơn vị "lần luyện thứ k": Tiếng Anh là NÚT (mỗi từ, mỗi mẫu câu); Toán thì nút
         BKT là cả CHƯƠNG — một lớp chỉ 8 nút, đường cong theo nút không đủ mẫu — nên
         Toán đếm theo BÀI. */
      const khoa = mon === 'toan' ? (a.microId || nut) : nut;
      const k = (lanThu.get(khoa) || 0) + 1;
      lanThu.set(khoa, k);
      if (k <= LAN_LUYEN_TOI_DA) {
        loi[mon] = loi[mon] || Array.from({ length: LAN_LUYEN_TOI_DA }, () => ({ tong: 0, sai: 0 }));
        loi[mon][k - 1].tong += 1;
        if (!a.correct) loi[mon][k - 1].sai += 1;
      }
    }

  }

  const duongCong = {};
  for (const [mon, mang] of Object.entries(loi)) {
    duongCong[mon] = mang.map((o, i) => ({
      lan: i + 1, tong: o.tong, tiLeLoi: o.tong >= MAU_TOI_THIEU ? Math.round((100 * o.sai) / o.tong) : null,
    }));
  }

  /* Số nút đạt θ ở cuối mỗi tuần — chạy lại lần hai, gọn: với mỗi tuần, lấy P(L)
     của mỗi nút ở lượt gần nhất trước mốc cuối tuần. */
  const tuanDs = [];
  const dau = Date.parse(`${dauTuan(ds[0].ts)}T00:00:00Z`);
  const cuoi = Date.parse(`${dauTuan(ds[ds.length - 1].ts)}T00:00:00Z`);
  for (let t = dau; t <= cuoi; t += 7 * NGAY) tuanDs.push(t);
  const nutVung = tuanDs.map((t) => {
    const moc = t - LECH_VN + 7 * NGAY;
    let luu = 0, quen = 0, daGap = 0;
    for (const [, v] of vet) {
      let cuoiCung = null;
      for (const x of v) { if (x.ts < moc) cuoiCung = x; else break; }
      if (!cuoiCung) continue;
      daGap += 1;
      if (cuoiCung.p >= theta) luu += 1;
      if (quenDan(cuoiCung.p, (moc - cuoiCung.ts) / NGAY) >= theta) quen += 1;
    }
    return { tuan: new Date(t).toISOString().slice(0, 10), daGap, vungLuu: luu, vungQuen: quen };
  });

  /* Bảng 3.9 tại thời điểm hiện tại. "Đang mắc" xét TRƯỚC (như bảng ghi), rồi tới ba
     dải theo P(L) đã lưu; "có nguy cơ quên" là CỜ, đếm riêng vì đi kèm tình trạng khác. */
  const tinhTrang = { dangMac: 0, yeu: 0, vungGan: 0, daVung: 0, nguyCoQuen: 0, tong: hoSo.size };
  const dai = (p) => (p < thetaYeu ? 0 : p < theta ? 1 : 2);
  const hoSoQuen = { truoc: [0, 0, 0], sau: [0, 0, 0] };
  for (const [, d] of hoSo) {
    if (d.saiLienTiep >= nguongMac) tinhTrang.dangMac += 1;
    else if (d.p < thetaYeu) tinhTrang.yeu += 1;
    else if (d.p < theta) tinhTrang.vungGan += 1;
    else tinhTrang.daVung += 1;
    const ngay = (now - d.lastSeen) / NGAY;
    if (ngay >= ngayQuen) tinhTrang.nguyCoQuen += 1;
    hoSoQuen.truoc[dai(d.p)] += 1;
    hoSoQuen.sau[dai(quenDan(d.p, ngay))] += 1;
  }

  /* Nút cho hình diễn biến: ưu tiên nút TỪNG đang mắc (đúng câu chuyện của Hình
     3.14 → 3.16), rồi tới nút luyện nhiều nhất. */
  const xep = [...vet.entries()].map(([nut, v]) => ({
    nut, mon: monNut.get(nut), v, tungMac: v.some((x) => x.sai >= nguongMac),
  /* Nút Tiếng Anh trước: luận văn minh hoạ trên nút từ · mẫu câu; nút chương của
     Toán gộp hàng trăm lượt nên một đường của nó không kể được chuyện gì. */
  })).sort((x, y) => (y.tungMac - x.tungMac)
    || ((x.mon === 'tienganh' ? 0 : 1) - (y.mon === 'tienganh' ? 0 : 1))
    || (y.v.length - x.v.length));
  const dienBien = xep.slice(0, SO_NUT_DIEN_BIEN).map(({ nut, mon, v, tungMac }) => ({
    nut, mon, tungMac, soLuot: v.length,
    luot: v.slice(-40).map((x) => ({ ts: x.ts, p: x.p, pTruoc: x.pTruoc, sai: x.sai, dung: x.dung })),
  }));

  return { nguong, duongCong, nutVung, tinhTrang, hoSoQuen, dienBien };
}
