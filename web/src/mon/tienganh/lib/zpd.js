import { layNguong, BO_MAC_DINH } from '../../../chung/lib/nguong.js';
/**
 * VÙNG PHÁT TRIỂN GẦN (ZPD) — xếp câu theo chỗ bé đang chông chênh.
 *
 * ── ĐỢT 1 MỚI GHI ĐƯỢC P(L), ĐÂY LÀ PHẦN ĐỌC ──
 * Sau Đợt 1, mỗi lượt trả lời cập nhật `mastery/{uid}/units/{maNut}` với xác suất
 * bé đã nắm nút ấy. Nhưng ghi mà không ai đọc thì bé vẫn học y hệt như trước —
 * con số nằm trong Firestore không đổi được một buổi học nào. Tệp này là chỗ đọc
 * nó ra và dùng vào một việc cụ thể: quyết định câu nào đưa cho bé TRƯỚC.
 *
 * ── BỐN NHÓM, VÀ VÌ SAO XẾP THEO THỨ TỰ NÀY ──
 *   1. ĐANG CHÔNG CHÊNH (0.3 ≤ p < 0.85) — chính là ZPD. Bé đã biết đôi chút
 *      nhưng chưa chắc: luyện ở đây đổi được nhiều nhất. Đưa lên đầu vì đầu buổi
 *      bé còn tỉnh táo nhất.
 *   2. CHƯA CÓ SỐ — nút bé chưa từng chạm. Phải học, và học sớm.
 *   3. YẾU HẲN (p < 0.3) — bé đang sai nhiều. Xếp SAU chứ không phải trước:
 *      luyện thêm cùng một kiểu câu ở chỗ bé đang sai nhiều là bắt bé sai tiếp,
 *      mà mở đầu buổi bằng ba câu sai liền thì bé nghỉ. Chỗ này cần bài PHỤ ĐẠO
 *      (Đợt 4), không phải thêm lượt luyện.
 *   4. ĐÃ THẠO (p ≥ 0.85) — vẫn cho làm, nhưng để cuối. Bỏ hẳn là việc của
 *      "Mastery Skip" ở Đợt 4, và bỏ thì phải có ngưỡng riêng cao hơn.
 *
 * ── ⚠ HAI ĐIỀU KHÔNG ĐƯỢC LÀM ──
 * KHÔNG BỎ CÂU NÀO. Chỉ đổi thứ tự. Bé vẫn gặp đủ mọi câu của mức ấy — sổ tiến
 * độ, thanh đếm câu và phép chấm đều dựa trên số câu, bỏ bớt là lệch hết.
 *
 * KHÔNG TRỘN GIỮA CÁC MỨC. Hàm này chỉ được gọi trên pool của MỘT mức (khởi động
 * · ráp câu · thử thách). Ba mức là một thang độ khó do người soạn dựng; trộn
 * chúng theo P(L) là ném thang ấy đi.
 */

import { tiLeDung, xepDinhDang } from './hoso.js';

/** Ngưỡng thạo — giữ đúng con số của `functions/src/bkt.js` (bác chốt 0,85). */
export const NGUONG_THAO = layNguong(BO_MAC_DINH, 'NG07');

/** Dưới mức này thì luyện thêm cùng kiểu câu không giúp gì — cần phụ đạo. */
export const NGUONG_YEU = layNguong(BO_MAC_DINH, 'NG08');

export const NHOM = {
  chongChenh: 0,
  chuaBiet: 1,
  yeu: 2,
  daThao: 3,
};

/**
 * Một nút thuộc nhóm nào.
 *
 * ⚠ `p` KHÔNG PHẢI SỐ thì coi như CHƯA BIẾT, không coi là 0. Tài liệu hỏng, hàm
 * nền chưa chạy xong, hay trường thiếu — cả ba đều là "chưa có tin", mà coi
 * "chưa có tin" thành "bé rất yếu" là xếp nhầm cả nhóm xuống cuối buổi.
 */
export function nhomCua(p) {
  if (!Number.isFinite(p)) return NHOM.chuaBiet;
  if (p >= NGUONG_THAO) return NHOM.daThao;
  if (p < NGUONG_YEU) return NHOM.yeu;
  return NHOM.chongChenh;
}

/**
 * Đọc mức thạo của một nút từ sổ `mastery`.
 *
 * Khoá tài liệu là `encodeURIComponent(bktUnit)` (hàm nền đặt thế), nhưng mã nút
 * của Tiếng Anh (`v_g5_u1_city`) không có ký tự nào cần mã hoá — nên hai dạng
 * khoá trùng nhau. Vẫn thử cả hai: đổi cách đặt mã ở đâu đó mà quên chỗ này thì
 * hỏng lặng lẽ, chỉ là bảng xếp câu về y như cũ và không ai thấy gì.
 */
export const mucThaoCua = (mucThao, maNut) => {
  if (!maNut) return null;
  const d = mucThao?.[maNut] ?? mucThao?.[encodeURIComponent(maNut)];
  return Number.isFinite(d?.p) ? d.p : null;
};

/**
 * CHIỀU SƯ PHẠM — khoá xếp PHỤ, dùng bảng "bé làm tốt dạng câu nào".
 *
 * Luật, và lý do của nó:
 *
 *   Ở chỗ bé CHÔNG CHÊNH hoặc YẾU → đưa định dạng bé MẠNH lên trước.
 *   Nội dung đã khó rồi; chồng thêm một dạng câu bé cũng vật vã là bắt bé đánh
 *   nhau với hai thứ cùng lúc, và khi sai thì không ai biết bé sai vì chưa hiểu
 *   bài hay vì chưa quen cách hỏi. Tách hai cái khó ra.
 *
 *   Ở chỗ bé ĐÃ THẠO → đưa định dạng bé YẾU lên trước.
 *   Nội dung an toàn nên đây là chỗ rẻ nhất để tập cách hỏi bé còn ngại. Sai ở
 *   đây không tốn gì, mà quen dần thì lần sau gặp dạng ấy ở bài mới bé đỡ khớp.
 *
 *   Ở chỗ CHƯA BIẾT → giữ nguyên thứ tự người soạn. Không có lý do để thích dạng
 *   nào hơn khi chính nội dung cũng mới tinh.
 *
 * ⚠ CHỈ LÀ KHOÁ PHỤ. Nhóm ZPD vẫn quyết trước — thứ bé đang chông chênh vẫn lên
 * đầu dù nó rơi vào dạng câu bé yếu. Cho định dạng thắng nhóm là đảo ngược cả
 * mục đích: buổi học sẽ mở bằng thứ bé đã thạo, chỉ vì nó hợp dạng câu.
 */
function hangDinhDang(format, hoSo, nhom) {
  const ti = hoSo ? tiLeDung(hoSo, format) : null;
  if (ti === null) return 0;               // chưa đủ mẫu → không xê dịch gì
  /* Nhóm đã thạo thì đảo chiều: yếu lên trước. */
  return nhom === NHOM.daThao ? ti : -ti;
}

/**
 * Xếp lại một pool câu theo ZPD. ỔN ĐỊNH trong từng nhóm — giữ nguyên thứ tự
 * người soạn đặt, chỉ đổi thứ tự giữa các nhóm (và trong nhóm thì theo định dạng,
 * nếu có hồ sơ đủ mẫu).
 *
 * Không có số liệu (chưa đăng nhập, mất mạng, hàm nền chưa chạy) thì trả về ĐÚNG
 * mảng cũ, không phải bản sao đã xáo — bé học y như trước, không có gì lạ xảy ra.
 */
export function xepTheoZPD(cauDs, mucThao, hoSo = null) {
  const ds = Array.isArray(cauDs) ? cauDs : [];
  if (ds.length < 2) return ds;

  const coThao = !!mucThao && Object.keys(mucThao).length
    && ds.some((c) => mucThaoCua(mucThao, c?.maNut) !== null);
  /* Hồ sơ định dạng chỉ đáng dùng khi có ÍT NHẤT HAI dạng đủ mẫu — một dạng thì
     mọi câu cùng hạng, xếp lại chẳng đổi gì mà vẫn tốn một lần sắp. */
  const coDang = !!hoSo && xepDinhDang(hoSo).length >= 2
    && ds.some((c) => c?.format);
  if (!coThao && !coDang) return ds;

  return ds
    .map((c, i) => {
      const n = coThao ? nhomCua(mucThaoCua(mucThao, c?.maNut)) : NHOM.chuaBiet;
      return { c, i, n, d: coDang ? hangDinhDang(c?.format, hoSo, n) : 0 };
    })
    .sort((a, b) => (a.n - b.n) || (a.d - b.d) || (a.i - b.i))
    .map((x) => x.c);
}

/**
 * Những nút bé đang chông chênh nhất — để màn hình nói được bé đang học gì.
 * Sắp xếp theo P(L) tăng dần: chỗ chênh vênh nhất đứng trước.
 */
export function nutChongChenh(mucThao, { toiDa = 5 } = {}) {
  return Object.entries(mucThao || {})
    .map(([ma, d]) => ({ ma, p: Number.isFinite(d?.p) ? d.p : null }))
    .filter((x) => x.p !== null && nhomCua(x.p) === NHOM.chongChenh)
    .sort((a, b) => a.p - b.p)
    .slice(0, toiDa);
}
