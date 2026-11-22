import { layNguong, boNguong } from '../../../chung/lib/nguong.js';
/**
 * HÀM CHÍNH SÁCH π — từ trạng thái của bé sang việc nên làm tiếp (mục 2.5.1).
 *
 * Ba nhánh, đúng như luận văn khai:
 *   TIẾP     bé đang đi được, cứ đi tiếp theo nhịp thường.
 *   VƯỢT ẢI  bé đã vững hẳn phần này — cho đi nhanh hơn, đừng bắt luyện lại.
 *   PHỤ ĐẠO  bé đang mắc, và mắc theo kiểu luyện thêm cùng loại câu không gỡ được.
 *
 * ── ⚠ NGƯỠNG VƯỢT ẢI LẤY TỪ MỘT CHỖ DUY NHẤT ──
 * θ = 0,85, hiệu chỉnh bằng thực nghiệm (`bkt.js` ghi lý do: bộ tham số mặc định
 * theo tài liệu tuyên bé thạo chỉ sau 2 câu, quá dễ dãi với trẻ). Bác chốt con số
 * này 21-08; bản luận văn hiện hành ghi đúng 0,85 ở cả mục 2.3.2.d lẫn Bảng 3.18.
 * Lấy ngưỡng từ MỘT chỗ — `zpd.js` → `bkt.js` — chứ không gõ lại số ở đây: hai nơi
 * hai số là hai hệ thống khác nhau đội một tên.
 * (Bản nháp luận văn cũ từng ghi 0,95; chú thích cảnh báo chỗ lệch ấy gỡ 26-08.)
 *
 * ── ⚠ LƯỚI ĐỠ PHẢI CÒN NGUYÊN ──
 * `dandat.js` xưa nay cho bé đi tiếp khi đã ĐẠT *hoặc* đã THỬ THẬT ≥2 lần. Nhánh
 * thứ hai là lưới đỡ, và nó ở đó vì một lý do sống còn: BKT có thể chấm sai. Bỏ
 * nó đi để "chính sách theo P(L) cho thuần" là bé kẹt VĨNH VIỄN ở một bài khi mô
 * hình đánh giá nhầm — mà bé thì không có cách nào tự thoát, và cũng không biết
 * để kêu.
 *
 * Nên tệp này KHÔNG thay `dandat.js`. Nó chỉ trả lời câu "nên làm gì tiếp", còn
 * câu "có được đi tiếp không" vẫn thuộc `dandat.js` với lưới đỡ nguyên vẹn.
 */
import { nguongThao, nguongYeu, mucThaoCua } from './zpd.js';

export const VIEC = {
  tiep: 'tiep',
  vuotAi: 'vuotAi',
  phuDao: 'phuDao',
};

/**
 * Sai LIÊN TIẾP bao nhiêu lần thì gọi là "đang mắc".
 *
 * Ba, không phải hai: sai hai lần liền là chuyện thường của việc học, và gọi phụ
 * đạo ở đó thì bé bị ngắt mạch liên tục. Ba lần liền thì bé không tự thoát ra
 * được bằng cách thử lại nữa.
 */
export const saiLienTiepMac = (nc) => layNguong(boNguong(), 'NG09', nc);
/* Hằng chụp bộ của phiên — cho cổng và chỗ chỉ HIỂN THỊ. Quyết định dùng hàm trên. */
export const SAI_LIEN_TIEP_MAC = layNguong(boNguong(), 'NG09');

/**
 * Việc nên làm tiếp cho MỘT nút.
 *
 * @param ho  hồ sơ nút từ `mastery`: { p, saiLienTiep, nAttempts }
 *
 * Trả `{ viec, vi_sao, p }` — `vi_sao` để màn hình và cô giáo đọc được, chứ không
 * phải chỉ một mã lệnh. Quyết định về việc học của một đứa trẻ thì phải giải
 * thích được.
 */
export function viecTiepCuaNut(ho, nc = {}) {
  const p = Number.isFinite(ho?.p) ? ho.p : null;
  const sai = Number(ho?.saiLienTiep) || 0;
  /* `nc` — ngữ cảnh HẸP HƠN phiên (thường là `{ nut }`). Môn và khối lớp đã nằm
     trong ngữ cảnh phiên nên chỗ gọi không phải mang theo; xem `datNguCanh`. */

  /* ĐANG MẮC xét TRƯỚC mức thạo, và cố ý: bé có thể có P(L) tàm tạm mà vẫn vừa
     sai ba câu liền — lúc ấy con số trung bình không phải thứ đáng nghe. */
  if (sai >= saiLienTiepMac(nc)) {
    return { viec: VIEC.phuDao, p, vi_sao: `sai ${sai} lần liên tiếp` };
  }
  if (p === null) return { viec: VIEC.tiep, p, vi_sao: 'chưa có số liệu' };
  if (p >= nguongThao(nc)) {
    return { viec: VIEC.vuotAi, p, vi_sao: `đã vững (${Math.round(p * 100)}%)` };
  }
  if (p < nguongYeu(nc)) {
    return { viec: VIEC.phuDao, p, vi_sao: `còn yếu (${Math.round(p * 100)}%)` };
  }
  return { viec: VIEC.tiep, p, vi_sao: `đang học được (${Math.round(p * 100)}%)` };
}

/**
 * Việc nên làm cho cả một BÀI — gộp từ các nút của bài ấy.
 *
 * ⚠ PHỤ ĐẠO THẮNG VƯỢT ẢI. Một bài có 10 nút, 9 nút vững và 1 nút bé đang mắc thì
 * việc cần làm là gỡ nút ấy, không phải cho bé bay qua cả bài. Cho vượt ải ở đây
 * là bỏ lại đúng chỗ bé cần giúp nhất — và bỏ lại lặng lẽ, vì mọi con số tổng đều
 * đẹp.
 *
 * ⚠ VƯỢT ẢI ĐÒI **MỌI** NÚT ĐỀU VỮNG, và đòi có đủ số liệu. Một nút chưa có số là
 * một nút bé chưa từng làm — cho vượt là tuyên thạo khống, đúng thứ mà lan truyền
 * xuôi ở Đợt 3 đã phải dựng ba chốt để chặn.
 */
export function viecTiepCuaBai(mucThao, maNutDs = []) {
  const ds = [...new Set(maNutDs.filter(Boolean))];
  if (!ds.length) return { viec: VIEC.tiep, vi_sao: 'bài chưa gắn nút nào', nut: [] };

  const tung = ds.map((ma) => {
    const p = mucThaoCua(mucThao, ma);
    const ho = mucThao?.[ma] ?? mucThao?.[encodeURIComponent(ma)] ?? {};
    return { ma, ...viecTiepCuaNut({ ...ho, p }, { nut: ma }) };
  });

  const mac = tung.filter((x) => x.viec === VIEC.phuDao);
  if (mac.length) {
    /* Nút mắc nặng nhất đứng đầu — đó là chỗ bài phụ đạo nên nhắm vào. */
    mac.sort((a, b) => (a.p ?? 0) - (b.p ?? 0));
    return {
      viec: VIEC.phuDao,
      nutMac: mac[0].ma,
      vi_sao: `${mac.length} phần đang mắc, nặng nhất: ${mac[0].vi_sao}`,
      nut: tung,
    };
  }

  /* ⚠ KHÔNG cần thêm phép "mọi nút đều có số liệu" ở đây, và tôi đã suýt thêm.
     Đảo chiều thử mới thấy nó là MÃ CHẾT: `viecTiepCuaNut` trả `vuotAi` chỉ khi
     `p >= ngưỡng`, mà điều đó đòi `p` khác null — nút chưa có số luôn rơi vào
     nhánh `tiep`, nên `every(vuotAi)` đã hỏng sẵn. Một chốt an toàn không bao giờ
     chạy thì tệ hơn không có: người đọc sau tưởng chính nó đang bảo vệ, và không
     đi tìm chỗ bảo vệ thật. */
  if (tung.every((x) => x.viec === VIEC.vuotAi)) {
    return { viec: VIEC.vuotAi, vi_sao: 'mọi phần của bài đều đã vững', nut: tung };
  }
  return { viec: VIEC.tiep, vi_sao: 'đang đi được', nut: tung };
}

/**
 * ⚠ ĐƯỢC PHÉP BỎ QUA BÀI NÀY KHÔNG — cửa hẹp, và hẹp là chủ ý.
 *
 * Vượt ải chỉ được bỏ bài khi CẢ BA đúng: chính sách nói vượt ải, bé đã ĐẠT bài
 * ấy rồi, và bài có đủ nút để lời nói ấy có nghĩa. Thiếu điều nào cũng trả về
 * false — thà bé làm lại một bài đã vững (mất mấy phút) còn hơn bỏ qua một bài bé
 * chưa vững (mất cả một mắt xích, và mắt xích ấy đỡ cho những bài sau).
 */
/** NG15 · bài phải có ít nhất ngần này nút thì "vượt ải" mới có nghĩa. */
export const nutToiThieuVuotAi = (nc) => layNguong(boNguong(), 'NG15', nc);
export const NUT_TOI_THIEU_VUOT_AI = layNguong(boNguong(), 'NG15');

export function duocVuotAi(mucThao, maNutDs, daDat,
                           { toiThieuNut = nutToiThieuVuotAi() } = {}) {
  if (!daDat) return false;
  const ds = [...new Set((maNutDs || []).filter(Boolean))];
  if (ds.length < toiThieuNut) return false;
  return viecTiepCuaBai(mucThao, ds).viec === VIEC.vuotAi;
}

/**
 * VECTOR TRẠNG THÁI S = [C, T, P, M] — gom bốn chiều thành một khối cho lời dặn.
 *
 * Bốn chiều đã đo xong từ Đợt 1 tới Đợt 2, nhưng nằm rời nhau ở bốn chỗ. Đây là
 * chỗ gom, và là mảnh cuối của mục 2.1.2.
 *
 *   C  mức nắm bài này          ← `mastery` của các nút trong bài
 *   T  có lâu không gặp lại     ← `lastSeen` xa nhất trong các nút ấy
 *   P  dạng câu bé làm tốt nhất ← bảng định dạng (Đợt 2)
 *   M  sở thích                 ← đã có từ Đợt 0
 *
 * ⚠ TRẢ VỀ NHÃN, KHÔNG TRẢ VỀ SỐ. Chỗ nhận là lời dặn cho mô hình, và số thô thì
 * mô hình không biết làm gì — tệ hơn, nó có thể nhại lại nguyên văn trước mặt bé.
 * Nhãn thì dịch được thành câu người, và câu người thì đọc to lên cũng không sao.
 */
/** NG13 · nghỉ quá ngần này ngày thì coi là có nguy cơ quên. */
export const soNgayCoiLaQuen = (nc) => layNguong(boNguong(), 'NG13', nc);
export const NGAY_COI_LA_QUEN = layNguong(boNguong(), 'NG13');

export function vectorS({ mucThao, maNutDs = [], dinhDang = null, thich = null,
                          bayGio = Date.now(),
                          ngayCoiLaQuen = soNgayCoiLaQuen() } = {}) {
  const ds = [...new Set((maNutDs || []).filter(Boolean))];
  const ho = ds
    .map((ma) => mucThao?.[ma] ?? mucThao?.[encodeURIComponent(ma)])
    .filter(Boolean);

  let mucNam = null;
  if (ho.length) {
    const ps = ho.map((h) => (Number.isFinite(h.p) ? h.p : null)).filter((x) => x !== null);
    if (ps.length) {
      const tb = ps.reduce((a, b) => a + b, 0) / ps.length;
      mucNam = tb >= nguongThao() ? 'vung' : (tb < nguongYeu() ? 'yeu' : 'dangHoc');
    }
  }

  /* Lâu nhất trong các nút của bài — một nút bị bỏ quên là đủ để đáng nhắc lại. */
  const xa = ho.map((h) => h.lastSeen).filter(Number.isFinite);
  const hayQuen = xa.length
    ? (bayGio - Math.min(...xa)) / 86400000 >= ngayCoiLaQuen : false;

  return {
    mucNam,
    hayQuen,
    dangManh: dinhDang?.dangManh || null,
    deMet: !!dinhDang?.deMet,
    thich: thich || null,
  };
}
