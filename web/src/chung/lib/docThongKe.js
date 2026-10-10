/**
 * ĐỌC CHỈ SỐ THEO DÕI NGƯỠNG — Bảng 3.22, phía máy con.
 *
 * Hàm nền ghi vào `thong_ke_nguong` mỗi tuần một dòng cho mỗi phạm vi; đây là chỗ
 * đọc chúng ra cho màn hình chuyên gia.
 *
 * ── ⚠ KHÔNG TÍNH LẠI Ở MÁY CON ──
 * Phép tính đòi đọc cả nhật ký (hàng trăm nghìn lượt) và chạy lại BKT trên từng
 * chuỗi. Làm ở máy con thì vừa chậm vừa đòi quyền đọc lượt của MỌI bé — tức mở một
 * cửa dữ liệu rộng hơn hẳn việc hiển thị vài con số. Nên máy con chỉ đọc kết quả
 * đã tính; `firestore.rules` cho chuyên gia ĐỌC `thong_ke_nguong` và cấm ghi.
 *
 * ── ⚠ KHÔNG CÓ SỐ LIỆU LÀ MỘT TRẠNG THÁI, KHÔNG PHẢI MỘT LỖI ──
 * Tuần đầu chưa có dòng nào, và hệ thống thật có thể chưa đủ lượt. Trả `[]` và để
 * màn hình nói thẳng "chưa có số liệu" — hiện số 0 thì chuyên gia tưởng đã đo và đo
 * ra 0, rồi sửa ngưỡng theo một con số không tồn tại.
 */
import { collection, getDocs, limit, orderBy, query } from 'firebase/firestore';
import { db, hasFirebase } from './nenTang.js';

/** Bao nhiêu dòng gần nhất thì đủ nhìn ra xu hướng mà không tải cả năm. */
export const SO_DONG = 60;

export async function docThongKeNguong() {
  if (!hasFirebase || !db) return { dong: [], loi: null };
  try {
    const q = query(collection(db, 'thong_ke_nguong'), orderBy('tinhLuc', 'desc'), limit(SO_DONG));
    const snap = await getDocs(q);
    return { dong: snap.docs.map((d) => ({ ma: d.id, ...d.data() })), loi: null };
  } catch (e) {
    /* Chuyên gia phải BIẾT là đọc hỏng, chứ không thấy một bảng rỗng rồi kết luận
       "chưa có dữ liệu". Hai chuyện ấy dẫn tới hai hành động khác nhau. */
    return { dong: [], loi: e?.message || 'không đọc được thống kê' };
  }
}

/** Gom theo phạm vi, mỗi phạm vi giữ các tuần theo thứ tự mới → cũ. */
export function gomTheoPhamVi(dong) {
  const m = new Map();
  for (const d of dong || []) {
    const k = `${d.phamVi || 'toanHe'}:${d.khoa ?? 'all'}`;
    if (!m.has(k)) m.set(k, { phamVi: d.phamVi || 'toanHe', khoa: d.khoa ?? null, tuan: [] });
    m.get(k).tuan.push(d);
  }
  for (const v of m.values()) v.tuan.sort((a, b) => (b.tinhLuc ?? 0) - (a.tinhLuc ?? 0));
  /* Toàn hệ trước, rồi tới các phạm vi hẹp — chuyên gia đọc từ rộng xuống hẹp. */
  return [...m.values()].sort((a, b) => {
    if (a.phamVi === b.phamVi) return String(a.khoa).localeCompare(String(b.khoa));
    return a.phamVi === 'toanHe' ? -1 : b.phamVi === 'toanHe' ? 1 : a.phamVi.localeCompare(b.phamVi);
  });
}

/**
 * Đọc một chỉ số thành CÂU, không thành con số trần.
 *
 * Bảng 3.22 không chỉ liệt kê chỉ số — nó có hẳn một cột "cách đọc", vì một con số
 * không kèm cách đọc thì chuyên gia phải tự đoán nên tăng hay giảm. Chỗ này là cột
 * ấy, và nó cố ý nói bằng tiếng người.
 *
 * ⚠ Mọi câu đều là GỢI Ý MỘT HƯỚNG, không phải một lệnh: chúng dựa trên dữ liệu
 *   quan sát được, mà dữ liệu quan sát được không biết vì sao bé sai.
 */
export function docHieu(tk) {
  if (!tk) return [];
  const ra = [];
  const pt = (x) => `${Math.round(x * 100)}%`;

  const som = tk.NG07?.tiLeCongNhanSom;
  const soCau = tk.NG07?.soCauTrungBinhToiThao;
  if (som != null && tk.NG07.coMauCongNhanSom >= 10) {
    if (som >= 0.2) {
      ra.push({ ma: 'NG07', muc: 'canXem', chu: `Cứ 5 nút được công nhận tinh thông thì khoảng 1 nút hôm sau bé làm sai câu đầu (${pt(som)}). Thường là dấu hiệu nên NÂNG θ.` });
    } else if (som <= 0.05 && soCau != null && soCau >= 6) {
      ra.push({ ma: 'NG07', muc: 'canXem', chu: `Công nhận sớm rất thấp (${pt(som)}) nhưng bé phải làm trung bình ${soCau.toFixed(1)} câu mới được công nhận — có thể đang luyện thừa, cân nhắc HẠ θ.` });
    } else {
      ra.push({ ma: 'NG07', muc: 'on', chu: `Công nhận sớm ${pt(som)}, trung bình ${soCau?.toFixed(1) ?? '—'} câu tới khi công nhận.` });
    }
  }

  const tuLen = tk.NG08?.tiLeTuLenLai;
  if (tuLen != null && tk.NG08.coMau >= 10) {
    ra.push({
      ma: 'NG08',
      muc: tuLen >= 0.5 ? 'canXem' : 'on',
      chu: `${pt(tuLen)} số nút rơi dưới θ_yếu rồi tự lên lại.`
        + (tuLen >= 0.5 ? ' Cao — ngưỡng có thể đang quá cao, bật phụ đạo cho những nút bé tự gỡ được.' : '')
        + (tk.NG08.chuaTruPhuDao ? ' ⚠ Con số này CHƯA trừ những lần bé lên lại nhờ phụ đạo, nên là cận trên.' : ''),
    });
  }

  const k = tk.NG09 || {};
  const coK = [1, 2, 3, 4].filter((i) => k[`k${i}`]?.coMau >= 10);
  if (coK.length) {
    /* ⚠ ĐÁNH DẤU NHỮNG k ĐÃ QUA CAN THIỆP, và nói hẳn ra vì sao. Đo lần đầu trên
       dữ liệu thật: 47% · 21% · 67,5% · 18% — con số vọt lên nằm đúng tại k = NG09
       đang hành, tức đúng chỗ hệ thống bật phụ đạo. Lượt kế tiếp ở đó không còn là
       "bé tự gỡ" mà là lượt SAU khi được giúp. Đọc nguyên văn Bảng 3.22 tại đó thì
       chuyên gia nâng NG09 vì chính tác dụng của can thiệp mà NG09 gây ra. */
    const coDauSao = coK.some((i) => k[`k${i}`].sauCanThiep);
    ra.push({
      ma: 'NG09',
      muc: 'on',
      chu: `Xác suất bé tự làm đúng ở lượt kế tiếp: ${coK.map((i) => `sau ${i} lần sai ${pt(k[`k${i}`].tiLeDung)}${k[`k${i}`].sauCanThiep ? '*' : ''}`).join(' · ')}.`
        + (coDauSao
          ? ' ⚠ Mốc có dấu * là mốc hệ thống ĐÃ bật phụ đạo, nên con số ở đó đo tác dụng'
            + ' của việc giúp chứ không đo khả năng tự gỡ — đừng nâng ngưỡng vì nó.'
            + ' Chỉ các mốc KHÔNG có dấu * mới đọc được theo cách thường.'
          : ' Nếu sau nhiều lần sai bé vẫn thường tự làm đúng thì ngưỡng đang bật phụ đạo sớm.'),
    });
  }

  const m = tk.NG01_NG05;
  if (m?.auc != null && m.coMau >= 50) {
    ra.push({
      ma: 'NG01–NG05',
      muc: m.auc < 0.6 ? 'canXem' : 'on',
      chu: `AUC ${m.auc.toFixed(3)} · RMSE ${m.rmse.toFixed(3)} · lệch hiệu chuẩn ${m.saiLechHieuChuan >= 0 ? '+' : ''}${m.saiLechHieuChuan.toFixed(3)}`
        + (m.auc < 0.6 ? ' — mô hình phân biệt kém ở phạm vi này, nên học tham số riêng cho nó.' : '')
        + (Math.abs(m.saiLechHieuChuan) > 0.1 ? ` Mô hình đang ${m.saiLechHieuChuan > 0 ? 'LẠC QUAN' : 'BI QUAN'} hơn thực tế.` : ''),
    });
  }

  const nghi = (tk.NG06 || []).filter((x) => x.coMau >= 20 && x.saiLechHieuChuan != null);
  if (nghi.length >= 2) {
    const xa = nghi[nghi.length - 1];
    if (xa.saiLechHieuChuan > 0.1) {
      ra.push({ ma: 'NG06', muc: 'canXem', chu: `Sau khoảng nghỉ ${xa.tu}${xa.den ? `–${xa.den}` : '+'} ngày, mô hình dự đoán LẠC QUAN hơn thực tế (+${xa.saiLechHieuChuan.toFixed(3)}) — nên GIẢM chu kỳ bán rã h.` });
    } else {
      ra.push({ ma: 'NG06', muc: 'on', chu: `Sai lệch sau nghỉ dài: ${xa.saiLechHieuChuan >= 0 ? '+' : ''}${xa.saiLechHieuChuan.toFixed(3)} (${xa.coMau} lượt).` });
    }
  }

  return ra;
}
