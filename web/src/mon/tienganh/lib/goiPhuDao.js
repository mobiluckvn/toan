/**
 * GỌI MÁY SOẠN CÂU PHỤ ĐẠO — chỗ DUY NHẤT của phần này biết tới mạng.
 *
 * Ba tầng, đúng khuôn phòng luyện nói và phần chấm viết:
 *     phudao.js      luật thuần (hai vòng tĩnh, hậu kiểm), chạy được bằng node
 *     goiPhuDao.js   gọi máy chủ, bóc JSON, dựng câu đúng hình dạng   ← tệp này
 *     PhuDao.jsx     vẽ
 *
 * ── ĐƯỜNG NÀY LUÔN CÓ ĐƯỜNG LÙI ──
 * `dungPhuDao` gọi tới đây CHỈ KHI hai vòng kho tĩnh không đủ câu, và nó bắt mọi
 * lỗi: mất mạng, chưa có khoá, mô hình trả rác — phụ đạo vẫn ra bài bằng phần tĩnh
 * đã có. Nên tệp này được phép ném, và `LOI_SINH` đếm để còn lần ra.
 */
import { httpsCallable } from 'firebase/functions';
import { fns, hasFirebase } from '../../../chung/lib/nenTang.js';
import { SO_CAU_PHU_DAO } from './phudao.js';

/** Đếm số lần nhờ máy soạn bài, và số lần hỏng. Không hiện ra cho bé. */
export const LOI_SINH = { goi: 0, hong: 0, cau: 0, ganNhat: null };

/* Hình dạng câu bấm chọn mà `BaiHoc.jsx` vẽ được. Dựng ở MỘT chỗ: câu do mô hình
   sinh phải giống câu của bộ sinh tới mức màn hình không phân biệt được, nếu không
   thì phụ đạo vẽ ra một câu vỡ giao diện. */
function dungCau(x, i, maNut) {
  const chon = (x?.choices || []).map((c) => String(c || '').trim()).filter(Boolean);
  const dap = String(x?.answer || '').trim();
  if (!x?.text || chon.length < 2 || !dap || !chon.includes(dap)) return null;
  return {
    id: `pd_ai_${maNut}_${i + 1}`,
    maNut,
    format: 'chondapan',
    text: String(x.text).trim(),
    choices: chon,
    answerKey: dap,
    hints: x.hint ? [String(x.hint).trim()] : [],
    /* ⚠ `nguon` đặt ở ĐÂY nữa, dù `dungPhuDao` cũng đặt: câu này có thể đi qua
       đường khác (hàng đợi duyệt) mà không qua `dungPhuDao`, và một câu do mô hình
       sinh KHÔNG được có đường nào vào kho mà không đeo nhãn. */
    nguon: 'ai',
  };
}

/**
 * Nhờ máy soạn câu ôn. Trả về MẢNG CÂU đã đúng hình dạng — chưa hậu kiểm vốn từ.
 *
 * ⚠ KHÔNG hậu kiểm ở đây: `dungPhuDao` làm việc ấy bằng `cauHoiHopLe` với vốn từ
 * ĐẦY ĐỦ của bài (gồm cả bài của nút gốc rễ, có thể ở quyển khác). Soi ở đây thì
 * phải chuyền vốn qua hai tầng, và chỗ nào soi bằng vốn thiếu là chỗ bác oan.
 */
export async function nhoSinh({ maNut, nhan, von, soCau = SO_CAU_PHU_DAO, lop = 1 }) {
  if (!hasFirebase || !fns) {
    const e = new Error('Máy chưa nối được lên mạng.');
    e.code = 'functions/unavailable';
    throw e;
  }
  LOI_SINH.goi += 1;
  try {
    const { data } = await httpsCallable(fns, 'sinhCauPhuDao')({
      nhan: nhan || maNut,
      lop,
      soCau,
      vonTu: [...(von?.loi?.tu || []), ...(von?.on || []).flatMap((x) => x.tu || [])]
        .map((t) => ({ tu: t.tu, nghia: t.nghia || '' })),
      mauCau: [...(von?.loi?.cau || []), ...(von?.on || []).flatMap((x) => x.cau || [])]
        .map((c) => c.congThuc || c.cau).filter(Boolean),
    });
    const m = String(data?.chu || '').match(/\{[\s\S]*\}/);
    if (!m) throw new Error('không đọc được JSON');
    const ds = JSON.parse(m[0])?.cau;
    const ra = (Array.isArray(ds) ? ds : [])
      .map((x, i) => dungCau(x, i, maNut)).filter(Boolean).slice(0, soCau)
      .map((c) => ({ ...c, mauPrompt: data?.mauPrompt || null,
        phienBanMau: data?.phienBanMau ?? null, vanTayPrompt: data?.vanTayPrompt || null }));
    LOI_SINH.cau += ra.length;
    if (!ra.length) { LOI_SINH.hong += 1; LOI_SINH.ganNhat = 'không câu nào đúng hình dạng'; }
    return ra;
  } catch (e) {
    LOI_SINH.hong += 1;
    LOI_SINH.ganNhat = String(e?.code || e?.message || e);
    throw e;
  }
}
