import { layNguong, BO_MAC_DINH, boNguong, capNhatBKT } from './nguong.js';
/**
 * BKT — Bayesian Knowledge Tracing (thuần toán, không phụ thuộc Firebase).
 *
 * Bốn tham số:
 *   L0    xác suất đã thạo từ trước khi học
 *   T     xác suất học được sau mỗi lần luyện (transit)
 *   slip  đã thạo nhưng vẫn trả lời sai (sẩy tay)
 *   guess chưa thạo nhưng đoán trúng
 */
/* Hiệu chỉnh bằng thực nghiệm (xem test/bkt.test.mjs):
   cần ~4 câu đúng liên tiếp mới đạt thạo, và MỘT câu sai sau đó kéo tụt dưới ngưỡng.
   Tham số cũ (L0 .25 · guess .20) tuyên thạo chỉ sau 2 câu — quá dễ dãi với trẻ. */
export const DEFAULT_PARAMS = {
  L0: layNguong(BO_MAC_DINH, 'NG01'),
  T: layNguong(BO_MAC_DINH, 'NG02'),
  slip: layNguong(BO_MAC_DINH, 'NG03'),
  guess: layNguong(BO_MAC_DINH, 'NG04'),
};

/**
 * THAM SỐ ĐANG HÀNH — đọc lúc GỌI, không lúc nạp module (việc R7 đợt 2).
 *
 * `DEFAULT_PARAMS` ở trên là bộ MẶC ĐỊNH, chụp lúc nạp; nó còn đó vì nhiều chỗ và
 * nhiều cổng dùng làm mốc. Nhưng hàm nền sống rất lâu giữa hai lượt gọi, nên nếu
 * phép chấm đọc hằng ấy thì chuyên gia sửa ngưỡng xong phải chờ hàm nền khởi động
 * lại mới ăn — tức vẫn phải nhờ người viết mã, đúng thứ R7 muốn bỏ.
 *
 * Vì vậy mọi phép tính dưới đây gọi `thamSo()`, và `index.js` nạp bộ ngưỡng
 * (`layBoNguong`) TRƯỚC khi gọi `applyAttempt`.
 */
const thamSo = (nc = {}) => ({
  L0: layNguong(boNguong(), 'NG01', nc),
  T: layNguong(boNguong(), 'NG02', nc),
  slip: layNguong(boNguong(), 'NG03', nc),
  guess: layNguong(boNguong(), 'NG04', nc),
});

/**
 * NGỮ CẢNH PHẠM VI CỦA MỘT LƯỢT (R7 · mục 3.8.1).
 *
 * Máy con có ngữ cảnh PHIÊN (`datNguCanh`, đặt lúc bé mở quyển); hàm nền thì không
 * — nó sống chung cho mọi bé, mọi môn, mọi khối lớp, và xử lượt của bé này ngay sau
 * lượt của bé khác. Nên ở đây ngữ cảnh phải dựng lại từ CHÍNH BẢN GHI, mỗi lượt một
 * lần, và không bao giờ được giữ lại giữa hai lượt.
 *
 * ⚠ CHỈ ĐỌC TRƯỜNG BẢN GHI TỰ KHAI. Không suy `khoiLop` từ hình dạng `v_g5_u1_city`:
 * đó là quy ước đặt tên của bộ sinh nội dung, không phải một lời khai: đổi nó một
 * lần là mọi lượt lặng lẽ rơi về bộ `toanHe`. Dòng nhật ký `v ≤ 3` không có
 * `khoiLop` — chúng trả `null`, và `layNguong` bỏ qua nấc ấy, tức giữ đúng hành vi
 * trước R7. Đó là chủ ý: một bản ghi đời cũ phải chấm được, chứ không được ném.
 */
export function nguCanhLuot(a = {}) {
  const nc = {};
  if (a.mon) nc.mon = String(a.mon);
  if (a.khoiLop != null && a.khoiLop !== '') nc.khoiLop = String(a.khoiLop);
  /* ── DẠNG CÂU — đã nằm sẵn trong bản ghi, ở trường `mode` ──
     Không phải thêm trường mới và không phải lên phiên bản bản ghi: `mode` đã mang
     đúng thứ này từ Đợt 1 (`hoso.js` cộng hồ sơ định dạng từ chính nó).

     Nấc này là nấc đáng giá nhất cho NG04 (xác suất ĐOÁN TRÚNG): câu bốn lựa chọn
     đoán trúng ~0,25, câu gõ lại chữ thì gần 0 — một con số chung cho cả hai là sai
     cho cả hai. Chuyên gia nay đặt được hai số khác nhau mà không nhờ ai viết mã.

     ⚠ HAI MÔN DÙNG HAI BỘ TỪ KHÁC NHAU cho cùng trường này: Tiếng Anh `chon · the ·
     go · tf · nghenhin · noi`, Toán `so · bieuthuc · dungsai · chondapan · tuluan`.
     Chúng không trùng chữ nào, nên một khoá `dangCau` hiện không thể mang hai nghĩa.
     Đó là may, không phải thiết kế — nên cổng `nguong_phien` ghim điều đó lại: đổi
     tên `chondapan` của Toán thành `chon` là hai môn dùng chung một ô ngưỡng, và
     chẳng gì kêu. */
  if (a.mode) nc.dangCau = String(a.mode);
  /* Bậc của câu — nấc `bac`. Nội dung khai sẵn ở 3.756/4.226 câu; bản ghi mang nó
     từ v6. Dòng cũ không có thì bỏ qua nấc này, tức giữ nguyên cách chấm cũ. */
  if (a.bac != null && a.bac !== '') nc.bac = String(a.bac);
  if (a.bktUnit) nc.nut = String(a.bktUnit);
  return nc;
}
export const MASTERY_THRESHOLD = layNguong(BO_MAC_DINH, 'NG07');

/** Một lần trả lời → cập nhật xác suất thạo */
export function bktUpdate(p, correct, params = null) {
  /* `params` thường tới từ `paramsFor`, đã mang đúng ngữ cảnh phạm vi của lượt.
     Gọi trần (không `params`) thì rơi về bộ `toanHe` — đúng cho cổng và cho chỗ
     nào chỉ cần một con số chung. */
  /* ⚠ GỌI XUỐNG `nguong.js`, KHÔNG giữ công thức riêng ở đây. Màn hình chuyên gia
     cần tính Bảng 3.21 ngay trên máy con, nên công thức phải có ở cả hai phía — và
     hai bản công thức thì sớm muộn trôi khỏi nhau. Chỗ duy nhất đã có hai bản chép
     KÈM cổng so là `nguong.js`, nên nó ở đó. */
  return capNhatBKT(p, correct, { ...thamSo(), ...(params || {}) });
}

const clamp = (x) => (Number.isFinite(x) ? Math.min(0.999, Math.max(0.001, x)) : thamSo().L0);

/** Chạy cả chuỗi trả lời */
export function bktSequence(answers, params = null, start = null) {
  let p = start ?? (params?.L0 ?? thamSo().L0);
  for (const ok of answers) p = bktUpdate(p, ok, params);
  return p;
}

export const isMastered = (p, th = MASTERY_THRESHOLD) => p >= th;

/**
 * Câu BẮT BUỘC ĐÚNG (bẫy) đáng tin hơn câu thường: trả lời đúng nhờ đoán khó hơn.
 * → giảm guess, tăng trọng số. Sai câu bẫy thì kéo mức thạo xuống mạnh hơn.
 */
/** NG05 · bộ tham số RIÊNG của câu bẫy — khó đoán hơn nên kết quả đáng tin hơn. */
export const BAY_PARAMS = layNguong(BO_MAC_DINH, 'NG05');

export function paramsFor(item = {}) {
  const nc = nguCanhLuot(item);
  return item.mustPass
    ? { ...thamSo(nc), ...layNguong(boNguong(), 'NG05', nc) }
    : thamSo(nc);
}

/**
 * NỬA ĐỜI CỦA TRÍ NHỚ — sau chừng này ngày không gặp lại, mức thạo rơi một nửa
 * quãng đường về phía "không chắc".
 *
 * 14 ngày là con số đặt theo lịch ôn sẵn có (+1 · +3 · +7 ngày): bé theo đúng
 * lịch thì gặp lại trước khi rơi đáng kể, bỏ hẳn hai tuần thì mới thấy tụt.
 * ⚠ Đây là con số CHỌN, không phải đo được — chưa có dữ liệu học thật để hiệu
 * chỉnh. Khi có rồi thì chỉnh ở đây, và ghi lại lý do như `DEFAULT_PARAMS`.
 */
export const NUA_DOI_NGAY = layNguong(BO_MAC_DINH, 'NG06');

/**
 * Mức thạo tụt dần khi lâu không gặp lại (chiều Thời gian, mục 2.1.2 luận văn).
 *
 * ⚠ KÉO VỀ 0.5, KHÔNG KÉO VỀ 0. Bé quên thì thành "không chắc", chứ không thành
 * "chưa từng biết" — kéo về 0 là bắt bé học lại từ đầu một thứ đã từng thạo, và
 * với trẻ con thì đó là hình phạt cho việc nghỉ vài hôm.
 *
 * Và vì kéo về 0.5, một nút bé từng làm SAI nhiều (p thấp) sẽ NHÍCH LÊN theo thời
 * gian. Nghe ngược đời nhưng đúng: lâu không kiểm thì hiểu biết hiện tại của hệ
 * thống về bé nhạt đi theo cả hai chiều, chứ không phải bé giỏi lên.
 */
export function quenDan(p, soNgay, nuaDoi = null, nc = {}) {
  const nua = nuaDoi ?? layNguong(boNguong(), 'NG06', nc);
  if (!Number.isFinite(p)) return thamSo().L0;
  if (!Number.isFinite(soNgay) || soNgay <= 0) return p;
  return clamp(0.5 + (p - 0.5) * 2 ** (-soNgay / nua));
}

/**
 * Cập nhật một bản ghi mastery từ một attempt.
 * doc: {p, nAttempts, nCorrect, lastSeen, saiLienTiep, pTruoc} | undefined
 *
 * ── `saiLienTiep` — SỐ LẦN SAI LIÊN TIẾP TẠI NÚT NÀY ──
 * Khác hẳn `nAttempts`, và khác hẳn `attempts` trong sổ tiến độ (đếm số lần làm
 * CẢ BÀI). Đây là `struggle_count` của mục 2.3.1 luận văn: bé sai mấy lần LIỀN
 * NHAU ở đúng nút này. Ba lần liền là dấu hiệu bé không tự thoát ra được — hai
 * đại lượng kia không nói ra điều đó, vì bé sai 3 lần rồi đúng 10 lần thì
 * `nCorrect/nAttempts` trông vẫn đẹp.
 *
 * Đúng MỘT lần là về 0. Cố ý: cái cần đo là "đang bí", không phải "từng bí".
 *
 * ── `pTruoc`/`p` — MỨC THẠO TRƯỚC VÀ SAU LƯỢT NÀY ──
 * Mục 2.5.2 đòi lưu P(L) trước và sau mỗi lượt để tính ΔC. Giá trị `pTruoc` đã
 * nằm sẵn trong tay ở dòng `cur` — trước nay chỉ là không ai ghi nó ra.
 *
 * ── QUÊN DẦN ──
 * Trước khi cập nhật, `p` cũ được kéo về phía 0.5 theo số ngày kể từ `lastSeen`
 * (xem `quenDan`). Đây là chiều Thời gian của mục 2.1.2, và cũng là thứ làm cho
 * "đã thạo" không phải một cái nhãn dán vĩnh viễn.
 *
 * ⚠ TỆP NÀY DÙNG CHUNG VỚI MÔN TOÁN ĐANG CHẠY THẬT. Các trường thêm vào đều MỚI,
 * và phép quên chỉ đổi `p` khi bé LÂU KHÔNG GẶP LẠI nút ấy — bé học đều thì
 * `lastSeen` luôn gần nên `cur` bằng đúng `p` cũ, không xê dịch gì. Tài liệu đời
 * cũ không có `lastSeen` thì KHÔNG phân rã. Cổng `bkt.test.mjs` canh cả ba điều.
 */
export function applyAttempt(doc, attempt, now = Date.now) {
  const bayGio = now();
  /* Bao lâu rồi bé không chạm nút này. `lastSeen` thiếu (tài liệu đời cũ) thì coi
     như VỪA gặp — thà không phân rã còn hơn phân rã theo một mốc bịa ra. */
  const cach = Number.isFinite(doc?.lastSeen)
    ? Math.max(0, (bayGio - doc.lastSeen) / 86400000) : 0;
  /* Dựng ngữ cảnh MỘT lần cho cả lượt: nửa đời trí nhớ, bốn tham số BKT và ngưỡng
     thạo phải cùng nhìn một phạm vi. Lấy hai lần ở hai chỗ là mở đường cho việc
     `quenDan` tính theo lớp 5 mà `isMastered` chấm theo `toanHe`. */
  const nc = nguCanhLuot(attempt);
  const cur = quenDan(doc?.p ?? thamSo(nc).L0, cach, null, nc);
  const dung = !!attempt.correct;
  const p = bktUpdate(cur, dung, paramsFor(attempt));
  const n = (doc?.nAttempts ?? 0) + 1;

  /* ── RT_avg và H_req — GỘP DẦN, không giữ cả dãy ──
     Mục 2.3.1 khai hai trường này ngay trong hồ sơ người học. Số thô từng lượt
     thì `attempts` đã có, nhưng bắt mọi chỗ đọc phải quét cả nghìn dòng rồi tự
     cộng là vừa chậm vừa dễ mỗi nơi cộng một kiểu.

     Cộng dồn bằng TỔNG chứ không nhân trung bình cũ với n: `(cũ*(n-1)+mới)/n`
     trôi số dần sau vài trăm lượt, mà tài liệu này sống suốt đời học của bé.

     ⚠ `ms` có thể thiếu (bản ghi đời cũ, hoặc màn chưa bấm giờ). Thiếu thì KHÔNG
     tính vào mẫu — chứ không coi là 0. Coi là 0 thì mỗi dòng thiếu kéo trung bình
     xuống, và "bé trả lời nhanh dần" thành một kết luận do lỗi ghi sinh ra. */
  const coMs = Number.isFinite(attempt.ms);
  const msTong = (doc?.msTong ?? 0) + (coMs ? attempt.ms : 0);
  const msDem = (doc?.msDem ?? 0) + (coMs ? 1 : 0);
  const goiTong = (doc?.goiTong ?? 0) + (Number(attempt.hintsUsed) || 0);

  return {
    p,
    /* Mức thạo TRƯỚC lượt này. Lần đầu chạm nút thì là L0 — vẫn ghi ra, để phép
       trừ `p - pTruoc` lúc nào cũng có nghĩa mà không phải xử lý trường hợp riêng. */
    pTruoc: cur,
    mastered: isMastered(p, layNguong(boNguong(), 'NG07', nc)),
    nAttempts: n,
    nCorrect: (doc?.nCorrect ?? 0) + (dung ? 1 : 0),
    saiLienTiep: dung ? 0 : (doc?.saiLienTiep ?? 0) + 1,
    msTong,
    msDem,
    /* RT_avg. `null` khi chưa có lượt nào đo được — thà nói "chưa có số liệu" còn
       hơn hiện một con số 0 cho bố mẹ tin theo. */
    msTrungBinh: msDem ? Math.round(msTong / msDem) : null,
    goiTong,
    /* H_req — số gợi ý trung bình mỗi lượt tại nút này. */
    goiTrungBinh: n ? +(goiTong / n).toFixed(2) : 0,
    lastMicroId: attempt.microId ?? doc?.lastMicroId ?? null,
    lastSeen: bayGio,
  };
}
