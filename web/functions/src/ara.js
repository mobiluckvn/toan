import { layNguong, BO_MAC_DINH } from './nguong.js';
/**
 * A-R-A và ΔC — bài phụ đạo có thật sự giúp được không (mục 2.5.3).
 *
 * Assess → Remediate → Assess. Đo mức nắm TRƯỚC khi vá, vá, rồi đo LẠI. Hiệu số
 * là ΔC (Knowledge Gain). Không có phép này thì "hệ thống có phụ đạo" chỉ là một
 * câu trong tài liệu: chẳng ai biết bài vá có đổi được gì không.
 *
 * ── ⚠ LẦN ĐO SAU PHẢI DÙNG CÂU KHÁC LẦN ĐO TRƯỚC ──
 * Hỏi lại đúng mấy câu vừa chữa thì bé trả lời đúng vì vừa NHÌN THẤY đáp án —
 * đó là đo trí nhớ ngắn hạn, không phải đo hiểu bài. Và nó sai theo hướng ĐẸP
 * LÊN: mọi bài phụ đạo đều trông như hiệu quả, kể cả bài vô dụng. `capHopLe()`
 * dưới đây bác một cặp A-R-A nếu hai lần đo trùng câu.
 *
 * ── GOM THEO PHIÊN BẢN MẪU, KHÔNG GOM THEO MÃ BĂM ──
 * Mã băm đổi cả khi sửa một lỗi chính tả trong lời dặn, nên gom theo băm là chẻ
 * dữ liệu ra vụn, mỗi nhóm vài mẫu, và chẳng so được gì. `phienBanMau` do người
 * sửa khai tay, nên nó nói đúng cái cần: "đây là lần đổi ĐÁNG KỂ". Mã băm để
 * phát hiện lệch ngoài ý muốn — ai đó sửa lời dặn mà quên tăng số.
 */

/** Cỡ mẫu tối thiểu để nói một mẫu prompt tốt hơn mẫu khác. */
export const TOI_THIEU_CAP = layNguong(BO_MAC_DINH, 'NG19');

/**
 * Một cặp A-R-A hợp lệ chưa?
 *
 * `cap` = { truoc: {p, itemIds}, sau: {p, itemIds}, mauPrompt, phienBanMau }
 */
export function capHopLe(cap) {
  if (!cap) return { ok: false, vi: 'không có gì' };
  const a = cap.truoc; const b = cap.sau;
  if (!Number.isFinite(a?.p) || !Number.isFinite(b?.p)) {
    return { ok: false, vi: 'thiếu mức nắm ở một trong hai lần đo' };
  }
  const ta = new Set(a.itemIds || []);
  const tb = new Set(b.itemIds || []);
  if (!ta.size || !tb.size) return { ok: false, vi: 'thiếu danh sách câu đã hỏi' };
  const trung = [...tb].filter((x) => ta.has(x));
  if (trung.length) {
    return {
      ok: false,
      vi: `lần đo sau dùng lại ${trung.length} câu của lần trước — đo trí nhớ ngắn `
        + 'hạn chứ không đo hiểu bài, và sai theo hướng đẹp lên',
    };
  }
  return { ok: true, vi: '' };
}

/** ΔC của một cặp — dương là bé khá lên. */
export const deltaC = (cap) => (capHopLe(cap).ok ? cap.sau.p - cap.truoc.p : null);

/**
 * Gom ΔC theo mẫu prompt.
 *
 * Trả `[{ mau, phienBan, soCap, deltaTB, hopLe, boQua }]`, hiệu quả cao đứng
 * trước. `boQua` đếm số cặp bị loại — hiện ra chứ không giấu: một mẫu có 40 cặp
 * mà 35 bị loại thì con số trung bình của 5 cặp còn lại không đáng tin, và người
 * đọc phải thấy điều đó.
 */
export function gomTheoMau(dsCap, { toiThieu = TOI_THIEU_CAP } = {}) {
  const nhom = new Map();
  for (const c of (dsCap || [])) {
    const k = `${c?.mauPrompt || '?'}@${c?.phienBanMau ?? 0}`;
    if (!nhom.has(k)) {
      nhom.set(k, {
        mau: c?.mauPrompt || '?', phienBan: c?.phienBanMau ?? 0,
        tong: 0, soCap: 0, boQua: 0,
      });
    }
    const n = nhom.get(k);
    const d = deltaC(c);
    if (d === null) { n.boQua += 1; continue; }
    n.tong += d;
    n.soCap += 1;
  }
  return [...nhom.values()]
    .map((n) => ({
      mau: n.mau,
      phienBan: n.phienBan,
      soCap: n.soCap,
      boQua: n.boQua,
      /* Dưới cỡ mẫu thì KHÔNG đưa ra con số. Một mẫu prompt bị chê hay được khen
         dựa trên 2 cặp là kết luận tự nuôi chính nó — cùng cái bẫy với bảng định
         dạng ở Đợt 2. */
      deltaTB: n.soCap >= toiThieu ? +(n.tong / n.soCap).toFixed(4) : null,
      duMau: n.soCap >= toiThieu,
    }))
    .sort((a, b) => (b.deltaTB ?? -Infinity) - (a.deltaTB ?? -Infinity));
}

/**
 * Mẫu nào đang dạy hiệu quả hơn — câu trả lời cho mục 2.5.3 "tối ưu hoá prompt".
 *
 * ⚠ CHỈ NÓI KHI CÓ ÍT NHẤT HAI MẪU ĐỦ MẪU. Một mẫu đủ dữ liệu thì nó vừa tốt nhất
 * vừa tệ nhất — câu ấy không có nghĩa gì, đúng như `yeuNhat` bên hồ sơ định dạng.
 */
export function mauTotNhat(dsCap, opt) {
  const ds = gomTheoMau(dsCap, opt).filter((x) => x.duMau);
  if (ds.length < 2) return null;
  return { tot: ds[0], kem: ds[ds.length - 1], soMau: ds.length };
}
