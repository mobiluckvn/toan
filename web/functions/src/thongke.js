import { layNguong, capNhatBKT } from './nguong.js';
import { nguCanhLuot } from './bkt.js';

/**
 * CHỈ SỐ THEO DÕI NGƯỠNG — Bảng 3.22 của luận văn (mục 3.8.5).
 *
 * Mỗi chỉ số ở đây được chọn vì nó trả lời được MỘT câu: ngưỡng này đang quá cao
 * hay quá thấp. Một con số không trả lời được câu ấy thì không thuộc về đây, dù
 * nó đẹp — chuyên gia cần căn cứ để sửa, không cần bảng điều khiển.
 *
 * ── ⚠ TỆP NÀY THUẦN TOÁN, KHÔNG ĐỤNG FIRESTORE ──
 * Vào: một MẢNG lượt trả lời. Ra: một đối tượng chỉ số. Vì thuần nên cổng chạy lại
 * được trên nhật ký bịa, và — quan trọng hơn — chạy lại được trên nhật ký THẬT với
 * một bộ ngưỡng KHÁC. Đó chính là bước "chạy thử lại" mà mục 3.8.3 đòi: chuyên gia
 * thấy hậu quả của một thay đổi TRƯỚC khi duyệt.
 *
 * ── ⚠ DỰNG LẠI MỨC THẠO, KHÔNG ĐỌC `mastery` ──
 * Kho `mastery` chỉ giữ trạng thái HIỆN TẠI, tính bằng bộ ngưỡng ĐANG hành. Muốn
 * biết "với θ = 0,80 thì tỉ lệ công nhận sớm là bao nhiêu" thì phải chạy lại cả
 * chuỗi. Nên ở đây mọi mức thạo đều dựng lại từ đầu bằng `capNhatBKT` — cùng một
 * hàm mà hàm nền dùng thật, không phải một bản chép riêng cho thống kê.
 */

const NGAY = 86400000;

/** Nhóm lượt theo (bé, nút) và sắp theo thời gian trong từng nhóm. */
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

/** Bốn tham số BKT đang hành cho ngữ cảnh của một lượt. */
const thamSoCua = (bo, nc) => ({
  L0: layNguong(bo, 'NG01', nc),
  T: layNguong(bo, 'NG02', nc),
  slip: layNguong(bo, 'NG03', nc),
  guess: layNguong(bo, 'NG04', nc),
});

/**
 * Chạy lại một chuỗi và trả về từng bước: mức thạo TRƯỚC lượt, dự đoán, kết quả.
 *
 * `pDuDoan` là xác suất hệ thống NGHĨ bé sẽ trả lời đúng, trước khi biết kết quả:
 *   P(đúng) = P(L)·(1 − slip) + (1 − P(L))·guess
 * Đây là đại lượng duy nhất so được với sự thật (0 hoặc 1), nên mọi phép đo chất
 * lượng mô hình — AUC, RMSE, sai lệch hiệu chuẩn — đều dựng trên nó.
 *
 * ⚠ KHÔNG tính phép QUÊN ở đây. Quên là hàm của khoảng nghỉ, mà chính khoảng nghỉ
 * là thứ chỉ số NG06 đang đo — đưa phép quên vào phép đo của chính nó thì mô hình
 * tự chấm điểm cho mình.
 */
export function chayLaiChuoi(ds, bo) {
  const buoc = [];
  let p = null;
  for (const a of ds) {
    const nc = nguCanhLuot(a);
    const ts = thamSoCua(bo, nc);
    if (p === null) p = ts.L0;
    const pDuDoan = p * (1 - ts.slip) + (1 - p) * ts.guess;
    const dung = !!a.correct;
    const pSau = capNhatBKT(p, dung, ts);
    buoc.push({ a, pTruoc: p, pSau, pDuDoan, dung, nc });
    p = pSau;
  }
  return buoc;
}

/**
 * NG07 · θ — hai chỉ số, và chúng phải đọc CÙNG NHAU (Bảng 3.22).
 *
 *   (a) tỉ lệ "công nhận sớm": nút đã được công nhận tinh thông, nhưng câu ĐẦU
 *       TIÊN ở lần gặp sau — cách ít nhất một ngày — lại sai.
 *   (b) số câu trung bình tới khi được công nhận.
 *
 * (a) cao → nên tăng θ. (b) cao mà (a) thấp → bé đang phải luyện thừa, nên giảm θ.
 * Chỉ nhìn một trong hai là sửa sai hướng: hạ θ cho bé đỡ luyện thì công nhận sớm
 * tăng, mà con số ấy nằm ở chỉ số kia.
 *
 * ⚠ ĐÒI CÁCH ÍT NHẤT MỘT NGÀY, và đó là cả điểm của phép đo. Câu sai ngay sau đó
 * trong cùng một phiên chỉ là sẩy tay; cái đáng lo là bé "đã thạo" rồi hôm sau
 * không làm được.
 */
export function chiSoNG07(nhom, bo) {
  let soCongNhan = 0;
  let soSomSai = 0;
  let tongCauToiThao = 0;
  let soChuoiThao = 0;

  for (const ds of nhom.values()) {
    const buoc = chayLaiChuoi(ds, bo);
    for (let i = 0; i < buoc.length; i++) {
      const theta = layNguong(bo, 'NG07', buoc[i].nc);
      if (buoc[i].pSau < theta) continue;

      /* Lần ĐẦU chuỗi này chạm θ — chỉ đếm một lần cho mỗi (bé, nút). */
      soChuoiThao++;
      tongCauToiThao += i + 1;

      const mocThao = buoc[i].a.ts ?? 0;
      const sau = buoc.slice(i + 1).find((b) => (b.a.ts ?? 0) - mocThao >= NGAY);
      if (sau) {
        soCongNhan++;
        if (!sau.dung) soSomSai++;
      }
      break;
    }
  }

  return {
    /* `null` chứ không phải 0 khi chưa có mẫu nào — "chưa biết" không phải "tốt". */
    tiLeCongNhanSom: soCongNhan ? soSomSai / soCongNhan : null,
    coMauCongNhanSom: soCongNhan,
    soCauTrungBinhToiThao: soChuoiThao ? tongCauToiThao / soChuoiThao : null,
    coMauToiThao: soChuoiThao,
  };
}

/**
 * NG08 · θ_yếu — tỉ lệ nút rơi xuống dưới θ_yếu rồi TỰ lên lại mà không cần phụ đạo.
 *
 * Tỉ lệ cao → ngưỡng đang quá cao, hệ thống bật phụ đạo cho những nút bé tự gỡ được.
 *
 * ⚠ "KHÔNG CẦN PHỤ ĐẠO" Ở ĐÂY ĐO BẰNG NHẬT KÝ LƯỢT, mà nhật ký lượt không ghi một
 * bài phụ đạo đã chạy hay chưa (khung phụ đạo nằm ở học bạ, kho khác). Nên con số
 * này là CẬN TRÊN: nó đếm cả những lần bé lên lại NHỜ phụ đạo. Cờ `chuaTruPhuDao`
 * đi kèm xuống tận tài liệu thống kê, chứ không chỉ nằm trong lời chú thích này —
 * một hạn chế chỉ ghi trong mã là một hạn chế người đọc bảng không thấy.
 */
export function chiSoNG08(nhom, bo) {
  let soRoi = 0;
  let soTuLen = 0;
  for (const ds of nhom.values()) {
    const buoc = chayLaiChuoi(ds, bo);
    let duoi = false;
    for (const b of buoc) {
      const yeu = layNguong(bo, 'NG08', b.nc);
      if (!duoi && b.pSau < yeu) { duoi = true; soRoi++; } else if (duoi && b.pSau >= yeu) { duoi = false; soTuLen++; }
    }
  }
  return {
    tiLeTuLenLai: soRoi ? soTuLen / soRoi : null,
    coMau: soRoi,
    chuaTruPhuDao: true,
  };
}

/**
 * NG09 · xác suất trả lời ĐÚNG ở lượt kế tiếp sau k lần sai liên tiếp (k = 1…4).
 *
 * Beck & Gong (2013): nếu sau k lần sai bé vẫn thường tự làm đúng thì ngưỡng đang
 * quá thấp — hệ thống ngắt mạch bé không cần thiết. Ngược lại, nếu xác suất đã rất
 * thấp từ k nhỏ hơn thì nên giảm, kẻo bé loay hoay lâu.
 *
 * Trả từng k RIÊNG kèm cỡ mẫu, không gộp thành một con số: cả cách đọc nằm ở chỗ
 * con số ấy đổi thế nào theo k.
 *
 * ── ⚠ CON SỐ TẠI k = NG09 ĐANG HÀNH KHÔNG ĐỌC ĐƯỢC THEO BẢNG 3.22 ──
 * Đo lần đầu trên dữ liệu thật (3212 lượt) ra một dãy bật ngược:
 *
 *     k=1  47,0% (394)   k=2  20,8% (207)   k=3  67,5% (160)   k=4  17,6% (51)
 *
 * Tụt từ k=1 sang k=2 là hợp lẽ. Nhưng k=3 vọt lên 67,5% — và 3 đúng bằng NG09
 * đang hành, tức ĐÚNG CHỖ hệ thống bật phụ đạo. Lượt kế tiếp sau lần sai thứ ba
 * không còn là "bé tự gỡ" nữa: nó là lượt SAU CAN THIỆP, thường là câu dễ hơn do
 * bài phụ đạo đưa ra.
 *
 * Nên cách đọc của Bảng 3.22 ("sau k lần sai bé vẫn thường tự làm đúng thì nên
 * TĂNG ngưỡng") mất hiệu lực tại đúng k ấy — đọc nguyên văn thì chuyên gia sẽ nâng
 * NG09 vì chính tác dụng của can thiệp mà NG09 gây ra, rồi vòng sau lại thấy k=4
 * vọt lên. Một vòng tự khẳng định.
 *
 * Nên `tuCan` đánh dấu những k ≥ ngưỡng đang hành, và màn hình phải nói ra. Tách
 * hẳn lượt sau can thiệp ra khỏi lượt tự gỡ thì cần biết một bài phụ đạo đã chạy
 * hay chưa — điều nhật ký lượt không ghi (khung phụ đạo nằm ở học bạ, kho khác).
 * Ghi lại đây để người sau không đọc nhầm, và để biết phải thêm gì nếu muốn đo sạch.
 */
export function chiSoNG09(nhom, bo = null) {
  const theoK = {};
  for (const ds of nhom.values()) {
    let sai = 0;
    for (const a of ds) {
      if (sai >= 1 && sai <= 4) {
        const o = theoK[sai] || (theoK[sai] = { dung: 0, tong: 0 });
        o.tong++;
        if (a.correct) o.dung++;
      }
      sai = a.correct ? 0 : sai + 1;
    }
  }
  /* Ngưỡng đang hành — từ đó trở đi, lượt kế tiếp là lượt SAU CAN THIỆP. */
  let nguong = null;
  try { nguong = bo ? layNguong(bo, 'NG09') : null; } catch { nguong = null; }

  const ra = {};
  for (const k of [1, 2, 3, 4]) {
    const o = theoK[k];
    ra[`k${k}`] = {
      tiLeDung: o ? o.dung / o.tong : null,
      coMau: o ? o.tong : 0,
      /* `true` = con số này KHÔNG đọc được theo Bảng 3.22: tại đây hệ thống đã bật
         phụ đạo, nên nó đo tác dụng của can thiệp chứ không đo khả năng tự gỡ. */
      sauCanThiep: nguong != null && k >= nguong,
    };
  }
  return ra;
}

/**
 * NG01–NG05 · chất lượng mô hình: AUC · RMSE · sai lệch hiệu chuẩn (Nhóm A, Bảng 3.23).
 *
 * Chỉ số kém ở một phạm vi → nên học tham số riêng cho phạm vi đó. Đó là lý do
 * chúng được tính CẢ theo từng phạm vi chứ không chỉ một con số chung.
 *
 * AUC tính bằng thống kê Mann–Whitney (hạng), KHÔNG dựng đường cong rồi lấy diện
 * tích: cách hạng cho đúng cùng một số, chạy một lượt, và không phải chọn số điểm
 * chia — một tham số bịa thêm là một chỗ nữa để hai lần đo ra hai kết quả.
 */
export function chatLuongMoHinh(buocDs) {
  const n = buocDs.length;
  if (!n) return { auc: null, rmse: null, saiLechHieuChuan: null, coMau: 0 };

  let tongBinhPhuong = 0;
  let tongDuDoan = 0;
  let tongThat = 0;
  for (const b of buocDs) {
    const that = b.dung ? 1 : 0;
    tongBinhPhuong += (b.pDuDoan - that) ** 2;
    tongDuDoan += b.pDuDoan;
    tongThat += that;
  }

  /* AUC — xếp hạng, xử hoà bằng hạng trung bình (đúng định nghĩa Mann–Whitney). */
  const sapXep = [...buocDs].sort((x, y) => x.pDuDoan - y.pDuDoan);
  const hang = new Array(sapXep.length);
  for (let i = 0; i < sapXep.length;) {
    let j = i;
    while (j + 1 < sapXep.length && sapXep[j + 1].pDuDoan === sapXep[i].pDuDoan) j++;
    const tb = (i + j) / 2 + 1;
    for (let k = i; k <= j; k++) hang[k] = tb;
    i = j + 1;
  }
  let tongHangDung = 0;
  let soDung = 0;
  for (let i = 0; i < sapXep.length; i++) {
    if (sapXep[i].dung) { tongHangDung += hang[i]; soDung++; }
  }
  const soSai = n - soDung;

  return {
    /* Toàn đúng hoặc toàn sai thì AUC không có nghĩa — `null`, không phải 0,5. */
    auc: (soDung && soSai)
      ? (tongHangDung - (soDung * (soDung + 1)) / 2) / (soDung * soSai) : null,
    rmse: Math.sqrt(tongBinhPhuong / n),
    /* Dương = mô hình LẠC QUAN hơn sự thật. Dấu mang nghĩa, đừng lấy trị tuyệt đối. */
    saiLechHieuChuan: (tongDuDoan - tongThat) / n,
    coMau: n,
  };
}

/**
 * NG06 · h, NG13 — sai lệch hiệu chuẩn ở lượt ĐẦU sau một khoảng nghỉ, chia theo Δt.
 *
 * Dự đoán lạc quan sau khoảng nghỉ dài (sai lệch dương và lớn dần theo Δt) → chu kỳ
 * bán rã đang đặt quá dài, nên giảm h.
 */
export const NHOM_NGHI = [[1, 3], [3, 7], [7, 14], [14, 30], [30, Infinity]];

export function chiSoNG06(nhom, bo) {
  const o = NHOM_NGHI.map(([a, b]) => ({ tu: a, den: b === Infinity ? null : b, buoc: [] }));
  for (const ds of nhom.values()) {
    const buoc = chayLaiChuoi(ds, bo);
    for (let i = 1; i < buoc.length; i++) {
      const cach = ((buoc[i].a.ts ?? 0) - (buoc[i - 1].a.ts ?? 0)) / NGAY;
      const vi = NHOM_NGHI.findIndex(([a, b]) => cach >= a && cach < b);
      if (vi >= 0) o[vi].buoc.push(buoc[i]);
    }
  }
  return o.map((x) => ({ tu: x.tu, den: x.den, ...chatLuongMoHinh(x.buoc) }));
}

/**
 * NG16–NG18 · hành vi — tỉ lệ lượt bị gắn nhãn, theo từng dạng câu.
 *
 * Một nhóm có tỉ lệ bất thường → ngưỡng chưa hợp với nhóm ấy. Bảng 3.22 đòi gom
 * theo cặp (dạng câu, bậc); nhật ký lượt hiện KHÔNG mang bậc, nên ở đây mới gom
 * được theo dạng câu. Cờ `thieuBac` xuống tận tài liệu thay vì lặng lẽ gom thiếu
 * một chiều rồi để người đọc tưởng đã đủ.
 */
export function chiSoNG16(luots, bo) {
  const theoDang = new Map();
  for (const a of luots) {
    if (!Number.isFinite(a?.ms)) continue;
    const dang = a.mode ? String(a.mode) : '—';
    if (!theoDang.has(dang)) theoDang.set(dang, { tong: 0, beTac: 0 });
    const o = theoDang.get(dang);
    o.tong++;
    if (a.ms / 1000 >= layNguong(bo, 'NG16', nguCanhLuot(a))) o.beTac++;
  }
  return {
    thieuBac: true,
    theoDangCau: Object.fromEntries(
      [...theoDang.entries()].map(([k, v]) => [k, { tiLeBeTac: v.beTac / v.tong, coMau: v.tong }]),
    ),
  };
}

/**
 * Gom tất cả thành MỘT tài liệu thống kê cho một phạm vi.
 *
 * `phamVi` và `khoa` chỉ là NHÃN — việc lọc lượt nào thuộc phạm vi nào do bên gọi
 * làm, vì nó biết mình đang gom theo khối lớp hay theo môn. Hàm này không tự đoán.
 */
export function tinhThongKe(luots, bo, { phamVi = 'toanHe', khoa = null, bayGio = Date.now() } = {}) {
  const ds = [...(luots || [])].filter((a) => a && a.bktUnit && a.learnerId);
  const nhom = theoChuoi(ds);
  const buocTatCa = [];
  for (const chuoi of nhom.values()) buocTatCa.push(...chayLaiChuoi(chuoi, bo));

  return {
    phamVi,
    khoa,
    tinhLuc: bayGio,
    nguongVer: bo?.phienBan ?? null,
    coMau: ds.length,
    soChuoi: nhom.size,
    /* ⚠ CỠ MẪU TỐI THIỂU LÀ CỦA VIỆC HỌC NGƯỠNG, KHÔNG PHẢI CỦA VIỆC THỐNG KÊ.
       Thống kê cứ tính và cứ ghi kèm cỡ mẫu — giấu số liệu vì "chưa đủ mẫu" thì
       chuyên gia không bao giờ biết dữ liệu đang tới đâu, và cũng không biết còn
       thiếu bao nhiêu. Chốt NG21 đứng ở chỗ biến thống kê thành ĐỀ XUẤT. */
    duMauDeHoc: ds.length >= layNguong(bo, 'NG21'),
    NG07: chiSoNG07(nhom, bo),
    NG08: chiSoNG08(nhom, bo),
    NG09: chiSoNG09(nhom, bo),
    NG01_NG05: chatLuongMoHinh(buocTatCa),
    NG06: chiSoNG06(nhom, bo),
    NG16: chiSoNG16(ds, bo),
  };
}
