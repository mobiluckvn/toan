import { capNhatBKT, layNguong } from './nguong.js';
import { nguCanhLuot } from './bkt.js';
import { hocBKT } from './hocNguong.js';

/**
 * SO SÁNH CÁC PHIÊN BẢN MÔ HÌNH NGƯỜI HỌC — kịch bản KB2 (Bảng 3.24).
 *
 * KB2: «so sánh bốn phiên bản mô hình — kiểm tra chéo 5 phần chia theo người học;
 * kiểm định DeLong cho AUC».
 *
 * ── ⚠ LUẬN VĂN KHÔNG NÓI BỐN PHIÊN BẢN ẤY LÀ GÌ ──
 * Bảng 3.24 chỉ ghi «bốn phiên bản mô hình». Nên bốn bản dưới đây là TÔI CHỌN, và
 * phải nói rõ thế — ai đọc kết quả cũng cần biết mình đang so cái gì với cái gì.
 * Chọn theo một thang có nghĩa: mỗi bản thêm đúng MỘT thứ so với bản trước, nên
 * chênh lệch giữa hai bản liền nhau quy được cho chính thứ vừa thêm.
 *
 *   1 · `moc`        không có mô hình NGƯỜI HỌC nào — chỉ biết NÚT nào khó. Mỗi lượt
 *                    đoán bằng tỉ lệ đúng của chính nút ấy trên tập học. Đây là mốc
 *                    đúng để so: một mô hình người học không hơn được nó thì nó chưa
 *                    biết gì về BÉ, chỉ đang biết về bài.
 *                    ⚠ Bản đầu tôi cho mốc đoán bằng tỉ lệ đúng CHUNG của tập học.
 *                    Chạy thật ra AUC 0,367 — DƯỚI 0,5, điều một mốc hằng số không
 *                    thể có. Lý do: mỗi phần chia một hằng số khác nhau, gộp bốn
 *                    phần lại thì chính chênh lệch giữa các hằng số ấy sinh ra một
 *                    thứ tự giả. Một con số vô lý mà đọc lướt thì vẫn trôi.
 *   2 · `bkt`        BKT với bộ tham số đang hành (Bảng 3.8), hiệu chỉnh bằng tay.
 *   3 · `bktEM`      BKT với tham số ước lượng bằng EM trên CHÍNH tập học của mỗi
 *                    phần chia. Thêm đúng một thứ so với bản 2: tham số học từ dữ
 *                    liệu thay vì đặt tay.
 *   4 · `bktQuen`    bản 2 cộng phép QUÊN giữa hai buổi. Đáng so vì hệ thống lúc
 *                    chạy CÓ quên (`applyAttempt` gọi `quenDan`) trong khi đường
 *                    thống kê thì cố ý KHÔNG — nên đây là câu hỏi thật: phép quên
 *                    làm dự đoán tốt lên hay xấu đi?
 *
 * ── ⚠ CHIA THEO NGƯỜI HỌC, KHÔNG CHIA THEO LƯỢT ──
 * Chia theo lượt thì lượt của cùng một bé nằm cả hai bên: mô hình đã thấy bé ấy
 * rồi, và AUC đo được cao hơn sự thật một cách CÓ HỆ THỐNG — nên không ai nghi.
 */

const NGAY = 86400000;

export const BAN = ['moc', 'bkt', 'bktEM', 'bktQuen'];

export const TEN_BAN = {
  moc: 'mốc — tỉ lệ đúng của TỪNG NÚT, không có mô hình người học',
  bkt: 'BKT, tham số đang hành (Bảng 3.8)',
  bktEM: 'BKT, tham số học bằng EM trên tập học',
  bktQuen: 'BKT đang hành + phép quên giữa hai buổi',
};

/** Nhóm lượt theo (bé, nút), sắp theo thời gian. */
function theoChuoi(luots) {
  const m = new Map();
  for (const a of luots) {
    if (!a?.learnerId || !a?.bktUnit) continue;
    const k = `${a.learnerId}::${a.bktUnit}`;
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(a);
  }
  for (const ds of m.values()) ds.sort((x, y) => (x.ts ?? 0) - (y.ts ?? 0));
  return m;
}

const theoBe = (luots) => {
  const m = new Map();
  for (const [k, ds] of theoChuoi(luots)) {
    const b = k.split('::')[0];
    if (!m.has(b)) m.set(b, []);
    m.get(b).push(ds);
  }
  return m;
};

/** Kéo `p` về 0,5 theo số ngày nghỉ — cùng công thức `quenDan` của hàm nền. */
const quen = (p, soNgay, nuaDoi) => (soNgay > 0 ? 0.5 + (p - 0.5) * 2 ** (-soNgay / nuaDoi) : p);

/**
 * Dự đoán của một phiên bản trên một tập chuỗi.
 *
 * Trả `[{ p, dung }]` — xác suất mô hình nghĩ bé trả lời đúng, và kết quả thật.
 * `thamSo` chỉ dùng cho `bktEM`; `tiLeChung` chỉ dùng cho `moc`.
 */
export function duDoan(chuoiDs, bo, ban, { thamSo = null, tiLeChung = 0.5, theoNut = null } = {}) {
  const ra = [];
  for (const ds of chuoiDs) {
    const nc = nguCanhLuot(ds[0] || {});
    const ts = thamSo || {
      L0: layNguong(bo, 'NG01', nc), T: layNguong(bo, 'NG02', nc),
      slip: layNguong(bo, 'NG03', nc), guess: layNguong(bo, 'NG04', nc),
    };
    const nuaDoi = layNguong(bo, 'NG06', nc);
    let p = ts.L0;
    for (let i = 0; i < ds.length; i += 1) {
      const a = ds[i];
      if (ban === 'bktQuen' && i > 0) {
        const cach = ((a.ts ?? 0) - (ds[i - 1].ts ?? 0)) / NGAY;
        p = quen(p, cach, nuaDoi);
      }
      const duDoanP = ban === 'moc'
        /* Nút chưa gặp trong tập học thì lùi về tỉ lệ chung — thà đoán bằng mức
           trung bình còn hơn bịa một con số cho một nút chưa ai làm. */
        ? (theoNut?.get(a.bktUnit) ?? tiLeChung)
        : p * (1 - ts.slip) + (1 - p) * ts.guess;
      ra.push({ p: duDoanP, dung: !!a.correct });
      p = capNhatBKT(p, !!a.correct, ts);
    }
  }
  return ra;
}

/* ════════════════════════ AUC VÀ KIỂM ĐỊNH DELONG ════════════════════════ */

const psi = (x, y) => (x > y ? 1 : (x === y ? 0.5 : 0));

/**
 * AUC kèm GIÁ TRỊ XẾP CHỖ (placement values) — nguyên liệu của kiểm định DeLong.
 *
 * `v10[i]` = tỉ lệ ca ÂM mà ca dương thứ i xếp trên; `v01[j]` ngược lại. Trung bình
 * của mỗi mảng đều bằng AUC — và phương sai của chúng mới là thứ cho biết chênh
 * lệch giữa hai AUC có hơn nhiễu hay không.
 */
export function aucXepCho(diem) {
  const duong = diem.filter((x) => x.dung).map((x) => x.p);
  const am = diem.filter((x) => !x.dung).map((x) => x.p);
  const m = duong.length;
  const n = am.length;
  if (!m || !n) return null;

  const v10 = new Array(m).fill(0);
  const v01 = new Array(n).fill(0);
  for (let i = 0; i < m; i += 1) {
    for (let j = 0; j < n; j += 1) {
      const t = psi(duong[i], am[j]);
      v10[i] += t;
      v01[j] += t;
    }
  }
  for (let i = 0; i < m; i += 1) v10[i] /= n;
  for (let j = 0; j < n; j += 1) v01[j] /= m;
  const auc = v10.reduce((s, x) => s + x, 0) / m;
  return { auc, v10, v01, m, n };
}

const hiepPhuongSai = (a, b) => {
  const n = a.length;
  if (n < 2) return 0;
  const ta = a.reduce((s, x) => s + x, 0) / n;
  const tb = b.reduce((s, x) => s + x, 0) / n;
  let s = 0;
  for (let i = 0; i < n; i += 1) s += (a[i] - ta) * (b[i] - tb);
  return s / (n - 1);
};

/** Hàm phân phối chuẩn tích lũy — xấp xỉ Abramowitz & Stegun 7.1.26. */
export function phanPhoiChuan(z) {
  const t = 1 / (1 + 0.3275911 * Math.abs(z) / Math.SQRT2);
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
    - 0.284496736) * t + 0.254829592) * t * Math.exp(-(z * z) / 2);
  return z >= 0 ? 0.5 * (1 + y) : 0.5 * (1 - y);
}

/**
 * KIỂM ĐỊNH DeLong cho HAI AUC trên CÙNG một tập ca.
 *
 * ⚠ VÌ SAO KHÔNG SO HAI AUC BẰNG MẮT: hai mô hình chấm cùng một đám lượt nên sai
 * số của chúng TƯƠNG QUAN. Bỏ qua tương quan ấy là tính phương sai quá lớn, và một
 * chênh lệch thật bị bỏ sót; tệ hơn, nếu tính quá nhỏ thì một chênh lệch do nhiễu
 * được công bố thành kết quả. DeLong (1988) tính đúng hiệp phương sai qua giá trị
 * xếp chỗ.
 *
 * ⚠ ĐÒI HAI MẢNG ĐIỂM CÙNG THỨ TỰ, CÙNG CA. Khác thứ tự là kiểm định vô nghĩa, nên
 * hàm này tự so nhãn và ném nếu lệch.
 */
export function deLong(diemA, diemB) {
  if (diemA.length !== diemB.length) throw new Error('DeLong: hai tập ca khác cỡ');
  for (let i = 0; i < diemA.length; i += 1) {
    if (diemA[i].dung !== diemB[i].dung) throw new Error('DeLong: hai tập ca không cùng thứ tự');
  }
  const A = aucXepCho(diemA);
  const B = aucXepCho(diemB);
  if (!A || !B) return null;

  const s10 = { aa: hiepPhuongSai(A.v10, A.v10), bb: hiepPhuongSai(B.v10, B.v10), ab: hiepPhuongSai(A.v10, B.v10) };
  const s01 = { aa: hiepPhuongSai(A.v01, A.v01), bb: hiepPhuongSai(B.v01, B.v01), ab: hiepPhuongSai(A.v01, B.v01) };
  const v = (k) => s10[k] / A.m + s01[k] / A.n;
  const phuongSai = v('aa') + v('bb') - 2 * v('ab');

  const hieu = A.auc - B.auc;
  if (!(phuongSai > 0)) {
    return { aucA: A.auc, aucB: B.auc, hieu, z: null, p: null, phuongSai, coMau: diemA.length };
  }
  const z = hieu / Math.sqrt(phuongSai);
  return {
    aucA: A.auc,
    aucB: B.auc,
    hieu,
    z,
    /* Hai phía: ta hỏi «hai mô hình có khác nhau không», không hỏi «A có hơn B
       không». Hỏi một phía sau khi đã nhìn số là tự cho mình một nửa mức ý nghĩa. */
    p: 2 * (1 - phanPhoiChuan(Math.abs(z))),
    phuongSai,
    coMau: diemA.length,
  };
}

/* ════════════════════════ KB2 ════════════════════════ */

/**
 * Chạy KB2: kiểm tra chéo 5 phần chia theo người học, bốn phiên bản, DeLong từng cặp.
 *
 * Dự đoán của cả bốn bản được gom từ MỌI phần chia rồi mới so — nên mỗi lượt được
 * dự đoán đúng một lần, bởi một mô hình chưa từng thấy bé ấy.
 */
/** Phần chia quá nhỏ hay chỉ có một lớp thì AUC của nó vô nghĩa. */
export const TOI_THIEU_MOI_PHAN = 30;

/**
 * KẾT LUẬN — và nhiệm vụ chính của nó là TỪ CHỐI KẾT LUẬN khi dữ liệu không đỡ nổi.
 *
 * ── ⚠ VÌ SAO HÀM NÀY TỒN TẠI ──
 * Chạy KB2 lần đầu trên 3.213 lượt của 10 người học, DeLong cho p < 0,01 ở cả sáu
 * cặp — nhìn qua thì mọi thứ «khác nhau thật». Nhưng hai cách đọc MÂU THUẪN nhau:
 *
 *     gộp cả năm phần : bktQuen 0,742 cao nhất
 *     trung bình từng phần : bktQuen 0,569 THẤP NHẤT
 *
 * Mâu thuẫn ấy có nguyên nhân: AUC gộp xếp hạng chung dự đoán của năm phần, mà mỗi
 * phần có một thang điểm riêng — chênh lệch GIỮA các thang tự sinh ra thứ tự. Thêm
 * nữa, một phần chỉ giữ lại vài lượt thì AUC của nó là 0 hay 1 tuỳ may rủi.
 *
 * Trao ra sáu con số p mà không nói điều này là mời người đọc kết luận sai bằng
 * chính con số mình đưa cho họ. Nên khi hai cách đọc không nhất quán, hàm trả
 * `ketLuan: 'chuaKetLuanDuoc'` và nói rõ vì sao.
 */
function ketLuan(gop, tb, tungPhan) {
  const xau = tungPhan.filter((x) => x.coMau < TOI_THIEU_MOI_PHAN
    || Object.values(x.auc).some((v) => v == null || v === 0 || v === 1));
  const xep = (o) => BAN.filter((b) => o[b] != null).sort((a, b) => o[b] - o[a]);
  const a = xep(gop);
  const b = xep(tb);
  const nhatQuan = a.length === b.length && a.every((x, i) => x === b[i]);

  if (nhatQuan && !xau.length) {
    return { ketLuan: 'ketLuanDuoc', thuTu: a, viSao: null };
  }
  const ly = [];
  if (!nhatQuan) {
    ly.push(`hai cách đọc cho hai thứ tự khác nhau — gộp: ${a.join(' > ')}; `
      + `trung bình từng phần: ${b.join(' > ')}`);
  }
  if (xau.length) {
    ly.push(`${xau.length}/${tungPhan.length} phần chia quá nhỏ hoặc AUC suy biến `
      + `(phần ${xau.map((x) => x.phan).join(', ')})`);
  }
  return {
    ketLuan: 'chuaKetLuanDuoc',
    thuTu: null,
    viSao: `${ly.join('; ')}. Mấy con số p của DeLong tính trên tập GỘP nên không `
      + 'đỡ được kết luận khi tập gộp đã trộn nhiều thang điểm. Cần thêm người học.',
  };
}

export function chayKB2(luots, bo, { soPhan = 5 } = {}) {
  const be = theoBe(luots);
  const ds = [...be.keys()].sort();
  if (ds.length < soPhan) {
    return { duMau: false, viSao: `cần ${soPhan} người học, mới có ${ds.length}` };
  }

  const gom = Object.fromEntries(BAN.map((b) => [b, []]));
  const tungPhan = [];
  for (let k = 0; k < soPhan; k += 1) {
    const giu = new Set(ds.filter((_, i) => i % soPhan === k));
    const hoc = [];
    const thu = [];
    for (const [b, chuoi] of be) (giu.has(b) ? thu : hoc).push(...chuoi);
    if (!hoc.length || !thu.length) continue;

    const em = hocBKT(hoc.map((c) => c.map((x) => !!x.correct)));
    const tong = hoc.reduce((s, c) => s + c.length, 0);
    const dung = hoc.reduce((s, c) => s + c.filter((x) => x.correct).length, 0);
    const tiLeChung = tong ? dung / tong : 0.5;

    /* Tỉ lệ đúng của TỪNG NÚT trên tập học — mốc «biết bài khó, không biết bé». */
    const demNut = new Map();
    for (const c of hoc) {
      for (const a of c) {
        const o = demNut.get(a.bktUnit) || { tong: 0, dung: 0 };
        o.tong += 1;
        if (a.correct) o.dung += 1;
        demNut.set(a.bktUnit, o);
      }
    }
    const theoNut = new Map();
    /* ⚠ LÀM MỊN LAPLACE. Một nút chỉ có 2 lượt trong tập học cho ra 0 hoặc 1 tuyệt
       đối, và mốc bỗng «chắc chắn» về một nút nó gần như không biết gì. */
    for (const [ma, o] of demNut) theoNut.set(ma, (o.dung + 1) / (o.tong + 2));

    const cuaPhan = {};
    for (const ban of BAN) {
      cuaPhan[ban] = duDoan(thu, bo, ban, {
        thamSo: ban === 'bktEM' && em
          ? { L0: em.L0, T: em.T, slip: em.slip, guess: em.guess } : null,
        tiLeChung,
        theoNut,
      });
      gom[ban].push(...cuaPhan[ban]);
    }
    /* ⚠ ĐO TỪNG PHẦN RIÊNG, KHÔNG CHỈ GỘP. Gộp dự đoán của năm phần rồi tính một
       AUC là trộn năm thang điểm khác nhau vào một bảng xếp hạng — với mốc theo nút
       thì mỗi phần một bộ ước lượng, và chênh lệch GIỮA các phần tự sinh ra thứ tự
       giả. Con số gộp vẫn cần (DeLong đòi các ca ghép đôi), nhưng phải đọc kèm độ
       tản giữa các phần, nhất là khi chỉ có 10 người học. */
    const aucPhan = {};
    for (const ban of BAN) {
      const r = aucXepCho(cuaPhan[ban]);
      aucPhan[ban] = r ? +r.auc.toFixed(4) : null;
    }
    tungPhan.push({ phan: k, soBeGiuLai: giu.size, coMau: cuaPhan[BAN[0]].length, auc: aucPhan });
  }

  const auc = {};
  for (const ban of BAN) {
    const r = aucXepCho(gom[ban]);
    auc[ban] = r ? r.auc : null;
  }

  const cap = [];
  for (let i = 0; i < BAN.length; i += 1) {
    for (let j = i + 1; j < BAN.length; j += 1) {
      const r = deLong(gom[BAN[i]], gom[BAN[j]]);
      if (r) cap.push({ a: BAN[i], b: BAN[j], ...r });
    }
  }

  /* Trung bình AUC của từng phần — con số này KHÔNG trộn thang điểm giữa các phần,
     nên nó đáng tin hơn `auc` gộp khi số người học ít. */
  const aucTrungBinhPhan = {};
  for (const ban of BAN) {
    const ds2 = tungPhan.map((x) => x.auc[ban]).filter((x) => x != null);
    aucTrungBinhPhan[ban] = ds2.length
      ? +(ds2.reduce((a, b) => a + b, 0) / ds2.length).toFixed(4) : null;
  }

  return {
    duMau: true,
    soNguoiHoc: ds.length,
    soPhan,
    coMau: gom[BAN[0]].length,
    auc,
    aucTrungBinhPhan,
    tungPhan,
    cap,
    ...ketLuan(auc, aucTrungBinhPhan, tungPhan),
    /* ⚠ Cảnh báo đi KÈM KẾT QUẢ, không nằm trong chú thích: dưới 20 người học thì
       mỗi phần chỉ học trên vài bé, và mốc theo nút gần như không ước lượng được. */
    canhBao: ds.length < 20
      ? `chỉ ${ds.length} người học — mỗi phần học trên ${ds.length - Math.ceil(ds.length / soPhan)} bé; `
        + 'mốc theo nút rất nhiễu, chênh lệch giữa các bản BKT thì vẫn đọc được'
      : null,
  };
}
