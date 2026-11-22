/**
 * BỘ NGƯỠNG — bản MÁY CHỦ. Ràng buộc R7 của luận văn (mục 3.8).
 *
 * ⚠ ĐÂY LÀ BẢN CHÉP của `src/chung/lib/nguong.js`. Phần dưới khối chú thích này
 * phải GIỐNG HỆT bản kia, từng ký tự — cổng `nguong_hai_ban.test.mjs` so đúng như
 * thế, và so cả với `data/nguong.json`.
 *
 * ── VÌ SAO CHÉP, KHÔNG IMPORT ──
 * `functions/` lên Cloud Functions với `package.json` riêng và chỉ mang theo thư
 * mục của nó; `src/` thì đi qua Vite. Một import chéo là bản deploy vỡ, mà vỡ lúc
 * deploy thì không cổng nào bắt trước. Cùng lẽ với `chula.js` ↔ `lib/chamviet.js`.
 *
 * ⚠ SỬA MỘT BÊN LÀ PHẢI SỬA BÊN KIA, VÀ SỬA CẢ `data/nguong.json`. Lệch ở đây hỏng
 *   theo kiểu khó thấy nhất: BKT chấm bằng θ này, màn hình quyết định bằng θ kia,
 *   và không gì báo.
 *
 * ── TỚI ĐÂU RỒI (22-11-2026, Bảng 4.7) ──
 * Máy chủ đọc bảng `nguong` qua `napNguong.js` (có nhớ tạm). Phép đổi dòng bảng →
 * bộ (`boTuBang`) nằm trong phần thân dùng chung, nên hai phía dựng bộ cùng một luật.
 */

/** Thang phạm vi, HẸP TRƯỚC RỘNG SAU. `layNguong` duyệt đúng thứ tự này. */
export const THANG_PHAM_VI = ['nut', 'dangCau', 'bac', 'loaiNut', 'khoiLop', 'mon', 'toanHe'];

/** Phiên bản bộ ngưỡng mặc định. Bản ghi lượt mang số này ở `nguongVer`. */
export const PHIEN_BAN = 1;

/**
 * GIÁ TRỊ MẶC ĐỊNH — đúng bằng con số đang chạy trước khi có R7.
 *
 * ⚠ Đưa ngưỡng ra dữ liệu KHÔNG ĐƯỢC ĐỔI HÀNH VI. Mọi giá trị ở đây phải bằng
 * đúng hằng số cũ; 103 cổng hiện có chính là phép kiểm cho điều đó.
 */
export const MAC_DINH = {
  NG01: 0.10,
  NG02: 0.08,
  NG03: 0.10,
  NG04: 0.30,
  NG05: { slip: 0.06, guess: 0.15 },
  NG06: 14,
  NG07: 0.85,
  NG08: 0.30,
  NG09: 3,
  NG10: 4,
  NG11: 3,
  NG12: 0.6,
  NG13: 14,
  NG14: 2,
  NG15: 3,
  NG16: 45,
  NG17: { ti: 0.25, toiThieuMoiNua: 3 },
  NG18: 8,
  NG19: 5,
  NG20: 4,
  NG21: 200,
  /* ── NG22–NG30: hằng số TRƯỚC ĐÂY GÕ CỨNG TRONG MÃ (Bảng 4.7, điểm 5) ──
     Nguyên tắc "mọi tham số nằm trong cấu hình" của mục 3.8. Mỗi giá trị dưới đây
     ĐÚNG BẰNG con số đã gõ cứng ở chỗ cũ (`oDau` trong `data/nguong.json` chỉ chỗ),
     nên đưa chúng ra bảng không đổi hành vi — 103 cổng cũ vẫn là phép kiểm. */
  NG22: 0.08,
  NG23: 0.05,
  NG24: 2,
  NG25: 0.5,
  NG26: 0.1,
  NG27: 4,
  NG28: { m1: 1, m2: 3, m3: 7 },
  NG29: 0.6,
  NG30: 30,
};

/** Khoảng hợp lệ — GIỚI HẠN CỨNG, chuyên gia lẫn máy đều không ra ngoài được. */
export const KHOANG = {
  NG01: [0.01, 0.50], NG02: [0.01, 0.40], NG03: [0.01, 0.49], NG04: [0.05, 0.49],
  NG05: [0.01, 0.30], NG06: [3, 60], NG07: [0.70, 0.98], NG08: [0.10, 0.78],
  NG09: [2, 6], NG10: [1, 6], NG11: [1, 5], NG12: [0.3, 0.9], NG13: [3, 60],
  NG14: [1, 5], NG15: [2, 10], NG16: [15, 120], NG17: [0.10, 0.60], NG18: [5, 30],
  NG19: [3, 50], NG20: [3, 10], NG21: [50, 5000],
  NG22: [0.01, 0.30], NG23: [0.01, 0.30], NG24: [1, 6], NG25: [0.2, 0.6],
  NG26: [0.01, 0.50], NG27: [2, 6], NG28: [1, 60], NG29: [0.5, 0.95], NG30: [10, 200],
};

/**
 * LẤY MỘT NGƯỠNG — hàm THUẦN, không đọc mạng, không đọc giờ.
 *
 * Thuần là điều kiện tiên quyết của "quét lưới" ở mục 3.8.3: chạy lại cả nhật ký
 * với một dãy giá trị chỉ làm được khi hàm quyết định không giấu trạng thái nào.
 *
 * @param bo       bộ ngưỡng: { macDinh: {ma: giaTri}, theoPhamVi?: {loai: {khoa: {ma: giaTri}}} }
 * @param ma       mã ngưỡng, 'NG01'…'NG30'
 * @param nguCanh  { nut, dangCau, bac, loaiNut, khoiLop, mon } — thiếu khoá nào thì bỏ qua nấc ấy
 */
export function layNguong(bo, ma, nguCanhRieng = {}) {
  /* Ngữ cảnh phiên làm NỀN, cái truyền vào ĐÈ lên. Nhờ vậy một chỗ gọi chỉ biết mã
     nút vẫn lấy đúng giá trị của môn và khối lớp bé đang học, mà không phải mang
     theo hai thứ ấy qua năm tầng hàm. */
  return layNguongThuan(bo, ma, { ..._nguCanh, ...(nguCanhRieng || {}) });
}

/**
 * CÙNG PHÉP TRA, NHƯNG KHÔNG ĐỌC NGỮ CẢNH PHIÊN — chỉ đúng `nguCanh` truyền vào.
 *
 * Màn chuyên gia soi "bộ hiệu lực của phạm vi khối lớp 3" thì phải ra đúng bộ ấy,
 * dù máy đang mở dở một quyển nào đó: để ngữ cảnh phiên lọt vào phép soi là soi
 * nhầm phạm vi mà không gì báo. Nên `soiNguong`/`nhipTinhThong` dùng hàm này.
 */
export function layNguongThuan(bo, ma, nguCanh = {}) {
  const theo = bo?.theoPhamVi || {};
  for (const loai of THANG_PHAM_VI) {
    if (loai === 'toanHe') break;
    const khoa = nguCanh?.[loai];
    if (khoa == null) continue;
    const v = theo?.[loai]?.[khoa]?.[ma];
    if (v !== undefined) return v;
  }
  const chung = theo?.toanHe?.[ma];
  if (chung !== undefined) return chung;
  const mac = (bo?.macDinh ?? MAC_DINH)[ma];
  if (mac === undefined) throw new Error(`layNguong: không có ngưỡng ${ma}`);
  return mac;
}

/** Một phạm vi `{ loai, khoa }` → ngữ cảnh tra cứu tương ứng. `toanHe` là ngữ cảnh rỗng. */
export function nguCanhCuaPhamVi(phamVi) {
  const loai = phamVi?.loai;
  if (!loai || loai === 'toanHe' || phamVi?.khoa == null || phamVi.khoa === '') return {};
  return { [loai]: String(phamVi.khoa) };
}

/**
 * CÁC DÒNG CỦA BẢNG `nguong` → MỘT BỘ NGƯỠNG. Bản DUY NHẤT của phép đổi này.
 *
 * ── VÌ SAO NẰM Ở TỆP DÙNG CHUNG ──
 * Máy chủ (`functions/src/napNguong.js`) và máy con (`src/chung/lib/napNguong.js`)
 * cùng đọc bảng `nguong`. Mỗi bên tự đổi theo kiểu của mình thì sớm muộn một bên
 * hiểu `phamVi` khác bên kia — BKT chấm theo θ của khối lớp 3, màn hình bé quyết
 * định theo θ toàn hệ. Đặt ở đây thì cổng `nguong_hai_ban` canh luôn phép đổi.
 *
 * Dòng thiếu `phamVi`, hoặc `loai: 'toanHe'`, hoặc thiếu `khoa` → giá trị toàn hệ.
 * Dòng có `phamVi: { loai, khoa }` hợp lệ → `theoPhamVi[loai][khoa][ma]`.
 * Dòng mang `loai` lạ (không có trên thang) thì BỎ, không đoán: một dòng `loai: 'lop'`
 * gõ nhầm mà được coi là toàn hệ thì nó đè lên cả hệ thống.
 *
 * @returns bộ ngưỡng, hoặc `null` khi bảng không có dòng dùng được — để bên gọi tự
 *          lùi về nguồn kế tiếp, chứ không lặng lẽ thành bộ rỗng.
 */
export function boTuBang(dsDong) {
  const macDinh = {};
  const theoPhamVi = {};
  let phienBan = PHIEN_BAN;
  let co = false;
  for (const x of (dsDong || [])) {
    if (!x || !x.ma || x.giaTri === undefined) continue;
    const pv = x.phamVi;
    const hep = pv && pv.loai && pv.loai !== 'toanHe' && pv.khoa != null && pv.khoa !== '';
    if (hep && !THANG_PHAM_VI.includes(pv.loai)) continue;
    if (Number.isFinite(x.phienBan)) phienBan = Math.max(phienBan, x.phienBan);
    co = true;
    if (!hep) { macDinh[x.ma] = x.giaTri; continue; }
    const k = String(pv.khoa);
    theoPhamVi[pv.loai] = theoPhamVi[pv.loai] || {};
    theoPhamVi[pv.loai][k] = theoPhamVi[pv.loai][k] || {};
    theoPhamVi[pv.loai][k][x.ma] = x.giaTri;
  }
  return co ? { phienBan, macDinh, theoPhamVi } : null;
}

/** Bộ ngưỡng chỉ gồm giá trị mặc định — dùng khi chưa tải được bộ của chuyên gia. */
export const BO_MAC_DINH = { phienBan: PHIEN_BAN, macDinh: MAC_DINH, theoPhamVi: {} };

/**
 * BỘ ĐANG HÀNH — một ô nhớ, đặt MỘT LẦN lúc mở phiên rồi thôi.
 *
 * ── VÌ SAO LÀ BIẾN, TRONG KHI `layNguong` PHẢI THUẦN ──
 * `layNguong` vẫn thuần: nó nhận bộ ngưỡng làm tham số. Ô nhớ này chỉ là chỗ CẤT bộ
 * đã tải, tách hẳn khỏi phép tính. Nhờ vậy quét lưới (mục 3.8.3) vẫn chạy lại được
 * cả nhật ký với một dãy giá trị mà không phải đụng vào ô này.
 *
 * ── VÌ SAO ĐẶT MỘT LẦN, KHÔNG ĐỔI GIỮA CHỪNG ──
 * Mục 3.8.2: "Máy người học tải tệp này cùng với `do_thi.json` khi mở bài và dùng nó
 * cho cả phiên", và 3.8.4: "Phiên bản mới chỉ có hiệu lực từ phiên tiếp theo; phiên
 * đang chạy giữ nguyên bộ ngưỡng đã tải." Đổi ngưỡng giữa buổi thì nửa đầu buổi và
 * nửa sau chấm theo hai luật, mà bản ghi chỉ mang được một số `nguongVer`.
 *
 * ⚠ Từ 22-11 (Bảng 4.7, điểm 4) mọi QUYẾT ĐỊNH trong `mon/**` đọc ô này LÚC DÙNG,
 * kèm ngữ cảnh. Các hằng viết hoa cũ (`SAI_LIEN_TIEP_MAC`, `ALPHA`…) vẫn còn — chụp
 * bộ của phiên lúc nạp module, chỉ để cổng và chỗ HIỂN THỊ con số chung dùng. Dù
 * vậy `main.jsx` vẫn phải `await napNguong()` TRƯỚC khi import `App.jsx`: mấy hằng
 * ấy phải chụp đúng bộ của phiên, và ô này phải có bộ trước lượt chấm đầu tiên.
 * Cổng `nguong_phien.test.mjs` canh.
 */
let _bo = BO_MAC_DINH;

/** Bộ ngưỡng đang dùng cho phiên này. */
export const boNguong = () => _bo;

/**
 * NGỮ CẢNH CỦA PHIÊN — `mon` và `khoiLop`, đặt khi bé mở một quyển.
 *
 * ── VÌ SAO HAI NẤC NÀY LÀ CHUYỆN CỦA PHIÊN, KHÔNG PHẢI CỦA TỪNG LỜI GỌI ──
 * Thang phạm vi có sáu nấc, nhưng chúng không cùng một hạng. `nut` · `dangCau` ·
 * `bac` đổi theo TỪNG LƯỢT, nên chỗ nào cần thì phải tự truyền vào. Còn `mon` và
 * `khoiLop` thì cả buổi học chỉ có một giá trị: bé đang mở quyển Tiếng Anh lớp 3 thì
 * mọi lời gọi trong buổi ấy đều thuộc môn ấy, lớp ấy.
 *
 * Giữ hai nấc ấy ở đây thì hàng chục chỗ gọi `layNguong` không phải mọc thêm tham
 * số, mà vẫn lấy đúng giá trị của quyển bé đang học. Chỗ nào cần nấc hẹp hơn thì
 * truyền thêm, và nó ĐÈ LÊN ngữ cảnh phiên — hẹp luôn thắng rộng, đúng mục 3.8.1.
 */
let _nguCanh = {};

/** Ngữ cảnh phiên hiện tại. */
export const nguCanhPhien = () => _nguCanh;

/** Đặt ngữ cảnh phiên. Gọi khi bé mở một quyển; gọi lại khi đổi quyển. */
export function datNguCanh(nc) {
  _nguCanh = {};
  for (const k of ['mon', 'khoiLop']) {
    if (nc?.[k] != null && nc[k] !== '') _nguCanh[k] = String(nc[k]);
  }
  return _nguCanh;
}

/**
 * CHUẨN HOÁ MỘT BỘ — lấp mã thiếu bằng mặc định. THUẦN: không đụng bộ đang hành.
 *
 * Màn chuyên gia đọc bảng tươi rồi cần đúng hình dạng này để soi, mà KHÔNG được đặt
 * nó làm bộ của phiên (mục 3.8.4: phiên đang chạy giữ bộ đã tải). Nên tách khỏi
 * `datBoNguong`.
 */
export function chuanHoaBo(bo) {
  const sach = bo && typeof bo === 'object' && bo.macDinh ? bo : BO_MAC_DINH;
  return { phienBan: sach.phienBan ?? PHIEN_BAN,
           macDinh: { ...MAC_DINH, ...(sach.macDinh || {}) },
           theoPhamVi: sach.theoPhamVi || {} };
}

/** Đặt bộ cho cả phiên. Trả về chính bộ đã đặt, để chỗ gọi ghi `nguongVer`. */
export function datBoNguong(bo) {
  _bo = chuanHoaBo(bo);
  return _bo;
}

/**
 * BỘ ỨNG VIÊN — bộ `bo` sau khi đặt `giaTri[ma]` (với mọi `ma` trong `doi`) vào ĐÚNG
 * phạm vi `phamVi`. THUẦN, trả bản sao. Đây là thứ màn chuyên gia soi TRƯỚC khi phát
 * hành, và cũng là thứ hàm phát hành soi lại lần cuối.
 */
export function apDungThayDoi(bo, phamVi, giaTri, doi) {
  const goc = chuanHoaBo(bo);
  const macDinh = { ...goc.macDinh };
  const theoPhamVi = {};
  for (const [loai, theoKhoa] of Object.entries(goc.theoPhamVi || {})) {
    theoPhamVi[loai] = {};
    for (const [khoa, v] of Object.entries(theoKhoa || {})) theoPhamVi[loai][khoa] = { ...v };
  }
  const nc = nguCanhCuaPhamVi(phamVi);
  const [loai] = Object.keys(nc);
  for (const ma of (doi || [])) {
    if (!loai) { macDinh[ma] = giaTri[ma]; continue; }
    theoPhamVi[loai] = theoPhamVi[loai] || {};
    theoPhamVi[loai][nc[loai]] = theoPhamVi[loai][nc[loai]] || {};
    theoPhamVi[loai][nc[loai]][ma] = giaTri[ma];
  }
  return { phienBan: goc.phienBan, macDinh, theoPhamVi };
}

/* Mấy ngưỡng mang HAI con số thì soi theo trường nào. */
const TRUONG_SO = { NG05: ['slip', 'guess'], NG17: ['ti'], NG28: ['m1', 'm2', 'm3'] };

const trongKhoang = (ma, v) => {
  const k = KHOANG[ma];
  if (!k) return false;
  const so = TRUONG_SO[ma] ? TRUONG_SO[ma].map((t) => v?.[t]) : [v];
  return so.every((x) => typeof x === 'number' && Number.isFinite(x)
                         && x >= k[0] && x <= k[1]);
};

/**
 * MỘT LƯỢT TRẢ LỜI → XÁC SUẤT THẠO MỚI. Thuật toán 3.1, và là bản DUY NHẤT.
 *
 * ── VÌ SAO CÔNG THỨC BKT LẠI NẰM Ở TỆP NGƯỠNG ──
 * Bảng 3.21 ("nhịp tinh thông") phải hiện ngay trên màn hình chuyên gia khi họ kéo
 * θ — tức máy CON cần tính được nó. Mà BKT vốn chỉ có ở máy chủ (`functions/src/
 * bkt.js`), và hai phía không import chéo được.
 *
 * Ba đường: chép công thức sang máy con (bản thứ ba, sẽ trôi) · gọi máy chủ mỗi lần
 * kéo thanh trượt (chậm, và chuyên gia mất cảm giác tức thì) · hoặc đặt công thức
 * vào đúng tệp vốn ĐÃ có hai bản chép và ĐÃ có cổng so. Chọn đường thứ ba:
 * `functions/src/bkt.js` nay gọi xuống đây, nên vẫn chỉ có MỘT bản công thức.
 */
export const KEP = (x, L0) => (Number.isFinite(x) ? Math.min(0.999, Math.max(0.001, x)) : L0);

export function capNhatBKT(p, dung, { T, slip, guess, L0 }) {
  const truoc = KEP(p, L0);
  const sau = dung
    ? (truoc * (1 - slip)) / (truoc * (1 - slip) + (1 - truoc) * guess)
    : (truoc * slip) / (truoc * slip + (1 - truoc) * (1 - guess));
  return KEP(sau + (1 - sau) * T, L0);
}

/** Bốn tham số BKT của một bộ ngưỡng, theo ngữ cảnh. */
export const thamSoBKT = (bo, nguCanh = {}) => ({
  L0: layNguong(bo, 'NG01', nguCanh),
  T: layNguong(bo, 'NG02', nguCanh),
  slip: layNguong(bo, 'NG03', nguCanh),
  guess: layNguong(bo, 'NG04', nguCanh),
});

/**
 * NHỊP TINH THÔNG — Bảng 3.21, phép kiểm thứ ba của mục 3.8.4.
 *
 * ── VÌ SAO CHUYÊN GIA CẦN BẢNG NÀY ──
 * Nhìn con số θ thì không thấy được điều quan trọng nhất. Với bộ tham số hiện tại,
 * đổi θ từ 0,85 lên 0,90 KHÔNG đổi gì trong cách hệ thống đối xử với trẻ — cả hai
 * đều cần bốn câu đúng liên tiếp. Hạ xuống 0,80 thì chỉ còn ba. Nên chuyên gia phải
 * sửa ngưỡng theo "số câu" và "sai một câu thì còn bao nhiêu", chứ không theo một
 * con số xác suất.
 *
 * @returns { soCau, mucKhiDat, sauKhiSai } — `soCau: null` nghĩa là trong `tran`
 *          lượt vẫn chưa đạt, tức θ quá cao so với bộ tham số.
 */
export function nhipTinhThong(bo, nguCanh = {}, tran = 30) {
  /* Tra THUẦN — không trộn ngữ cảnh phiên. Bảng này trả lời cho ĐÚNG phạm vi chuyên
     gia đang xem, không cho quyển mà máy tình cờ đang mở. */
  const lay = (ma) => layNguongThuan(bo, ma, nguCanh);
  const ts = { L0: lay('NG01'), T: lay('NG02'), slip: lay('NG03'), guess: lay('NG04') };
  const theta = lay('NG07');
  let p = ts.L0;
  for (let i = 1; i <= tran; i += 1) {
    p = capNhatBKT(p, true, ts);
    if (p >= theta) {
      return { soCau: i, mucKhiDat: p, sauKhiSai: capNhatBKT(p, false, ts) };
    }
  }
  return { soCau: null, mucKhiDat: p, sauKhiSai: capNhatBKT(p, false, ts) };
}

/** Nhịp phải nằm trong khoảng này thì mới cho phát hành — mục 3.8.4. */
export const NHIP_CHO_PHEP = [3, 6];

/**
 * SOI MỘT BỘ NGƯỠNG — ba loại điều kiện của mục 3.8.4, trả về danh sách chỗ sai.
 *
 * ⚠ TRẢ VỀ DANH SÁCH, KHÔNG NÉM. Chuyên gia sửa một lần nhiều ngưỡng thì phải thấy
 * HẾT chỗ sai, chứ không phải sửa một chỗ rồi lại gặp chỗ sau — đúng lẽ `soiLoiCham`
 * đã dùng ở phần chấm viết.
 *
 * @param nguCanh  soi BỘ HIỆU LỰC của ngữ cảnh nào. Rỗng = toàn hệ. Chuyên gia sửa
 *                 θ cho khối lớp 3 thì phải soi bộ mà bé lớp 3 thật sự nhận — gồm
 *                 θ mới ấy GHÉP với θ_yếu, P(T)… thừa hưởng từ phạm vi rộng hơn —
 *                 chứ không soi bộ toàn hệ rồi tưởng là xong.
 */
export function soiNguong(bo, nguCanh = {}) {
  const loi = [];
  /* Tra THUẦN: ngữ cảnh phiên không được lọt vào phép soi (xem `layNguongThuan`). */
  const lay = (ma) => {
    try { return layNguongThuan(bo, ma, nguCanh); } catch { return undefined; }
  };
  for (const ma of Object.keys(KHOANG)) {
    const v = lay(ma);
    if (v === undefined) { loi.push({ ma, vi: 'không có giá trị' }); continue; }
    if (!trongKhoang(ma, v)) {
      loi.push({ ma, vi: `ngoài khoảng [${KHOANG[ma][0]}, ${KHOANG[ma][1]}]`, giaTri: v });
    }
  }
  /* Ràng buộc GIỮA các ngưỡng — mục 3.8.4. */
  const theta = lay('NG07');
  const yeu = lay('NG08');
  if (typeof theta === 'number' && typeof yeu === 'number' && yeu > theta - 0.20) {
    loi.push({ ma: 'NG08', vi: `θ_yếu phải ≤ θ − 0,20 (θ = ${theta})`, giaTri: yeu });
  }
  /* Hàm quên kéo P(L) về NG25 khi bé nghỉ lâu. Điểm tựa ấy mà sát θ thì nghỉ đủ lâu
     là bé TỰ THÀNH "đã thạo" một nút chưa từng vững — tuyên thạo khống bằng thời
     gian. Đòi cùng khoảng cách 0,20 như θ_yếu. (Có `1e-9` vì 0,70 − 0,20 trong số
     thực ra 0,4999…, và θ = 0,70 là giá trị hợp lệ — thiếu nó thì bộ mặc định của
     hàm quên tự đỏ ở đúng cận dưới của θ.) */
  const tua = lay('NG25');
  if (typeof theta === 'number' && typeof tua === 'number' && tua > theta - 0.20 + 1e-9) {
    loi.push({ ma: 'NG25', vi: `điểm tựa của hàm quên phải ≤ θ − 0,20 (θ = ${theta})`, giaTri: tua });
  }
  /* Lịch ôn phải GIÃN DẦN: +1 · +3 · +7. Hai mốc trùng nhau là hai thẻ ôn cùng
     ngày; mốc sau sớm hơn mốc trước thì "ôn ngắt quãng" chạy ngược. */
  const lich = lay('NG28');
  if (lich && typeof lich === 'object' && !(lich.m1 < lich.m2 && lich.m2 < lich.m3)) {
    loi.push({ ma: 'NG28', vi: 'ba mốc ôn phải tăng dần (mốc 1 < mốc 2 < mốc 3)', giaTri: lich });
  }
  for (const [ma, truong] of [['NG03', null], ['NG04', null],
                              ['NG05', 'slip'], ['NG05', 'guess']]) {
    const v = truong ? lay(ma)?.[truong] : lay(ma);
    if (typeof v === 'number' && v >= 0.5) {
      loi.push({ ma, vi: `${truong || ma} phải < 0,5 để mô hình không suy biến`, giaTri: v });
    }
  }
  /* Phép kiểm THỨ BA của mục 3.8.4 — nhịp tinh thông. Đây là chỗ bắt được thứ mà
     hai phép trên không thấy: từng ngưỡng đều trong khoảng, mà GHÉP LẠI thì ra một
     nhịp dạy vô lý (đạt sau một câu, hoặc không bao giờ đạt). */
  if (!loi.length) {
    const { soCau } = nhipTinhThong(bo, nguCanh);
    const [it, nhieu] = NHIP_CHO_PHEP;
    if (soCau === null) {
      loi.push({ ma: 'NG07', vi: `θ quá cao: luyện ${30} câu đúng liên tiếp vẫn chưa đạt` });
    } else if (soCau < it || soCau > nhieu) {
      loi.push({ ma: 'NG07',
                 vi: `nhịp tinh thông ${soCau} câu, phải trong khoảng ${it}–${nhieu}`,
                 giaTri: soCau });
    }
  }
  return loi;
}

/**
 * BỘ HIỆU LỰC CỦA MỘT PHẠM VI — giá trị bé ở phạm vi ấy thật sự nhận, từng mã.
 *
 * Màn chuyên gia bày bộ này khi chọn một phạm vi hẹp: ô nào phạm vi ấy chưa khai thì
 * hiện giá trị THỪA HƯỞNG từ nấc rộng hơn, để chuyên gia thấy đúng điểm xuất phát.
 */
export function giaTriHieuLuc(bo, phamVi = null) {
  const nc = nguCanhCuaPhamVi(phamVi);
  const ra = {};
  for (const ma of Object.keys(KHOANG)) ra[ma] = layNguongThuan(bo, ma, nc);
  return ra;
}

/**
 * SOI MỘT PHẠM VI — và mọi chỗ nó GIAO với phạm vi khác đã khai.
 *
 * ── VÌ SAO KHÔNG CHỈ SOI ĐÚNG MỘT NGỮ CẢNH ──
 * Đặt θ = 0,75 cho khối lớp 3 thì bộ `{ khoiLop: 3 }` có thể sạch, nhưng một bé lớp
 * 3 học Tiếng Anh nhận ngữ cảnh `{ mon: tienganh, khoiLop: 3 }` — mà nếu môn Tiếng
 * Anh đã khai θ_yếu = 0,60 thì GHÉP lại ra θ_yếu > θ − 0,20. Từng phạm vi đều hợp
 * lệ, chỗ giao thì không; và đó đúng là chỗ một đứa trẻ thật sẽ đứng.
 *
 * Nên soi: ngữ cảnh của chính phạm vi, rồi từng cặp (phạm vi ấy × mỗi khoá đã khai
 * ở một nấc KHÁC). Cặp là đủ cho trường hợp hay gặp (môn × khối lớp, khối lớp × dạng
 * câu); bộ ba trở lên thì số tổ hợp nổ theo số nút, nên không soi ở đây.
 *
 * @returns danh sách lỗi như `soiNguong`, mỗi lỗi kèm `nguCanh` nơi nó xảy ra.
 */
export function soiPhamVi(bo, phamVi = null) {
  const goc = nguCanhCuaPhamVi(phamVi);
  const loaiGoc = Object.keys(goc)[0] || null;
  const dsNguCanh = [goc];
  const theo = bo?.theoPhamVi || {};
  for (const loai of THANG_PHAM_VI) {
    if (loai === 'toanHe' || loai === loaiGoc) continue;
    for (const khoa of Object.keys(theo[loai] || {})) dsNguCanh.push({ ...goc, [loai]: khoa });
  }
  const ra = [];
  const daCo = new Set();
  for (const nc of dsNguCanh) {
    for (const l of soiNguong(bo, nc)) {
      const k = `${l.ma}|${l.vi}`;
      if (daCo.has(k)) continue;
      daCo.add(k);
      ra.push({ ...l, nguCanh: nc });
    }
  }
  return ra;
}
