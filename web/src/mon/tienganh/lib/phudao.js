/**
 * BÀI PHỤ ĐẠO — vá đúng chỗ bé đang mắc (mục 2.5.1 nhánh ba · 2.4.1).
 *
 * Bé sai ba lần liền ở một nút. Luyện thêm câu cùng loại thì bé sai tiếp — cái
 * hổng có thể nằm ở nút TIÊN QUYẾT chứ không ở đây (mục 2.3.3 đã tìm ra nó ở Đợt
 * 3). Bài phụ đạo nhắm vào nút gốc rễ ấy.
 *
 * ── BA BƯỚC, VÀ BƯỚC BA LÀ BƯỚC KHÔNG ĐƯỢC BỎ ──
 *   1. tìm nút gốc rễ                    (`nutGocRe`, Đợt 3)
 *   2. gom câu quanh nút ấy               — TĨNH trước, LLM sau
 *   3. SOI LẠI mọi câu bằng `cauHopLe()`  — kể cả câu tĩnh
 *
 * ── ⚠ ĐƯỜNG LÙI LÀ BẮT BUỘC, KHÔNG PHẢI TÍNH NĂNG PHỤ ──
 * Bé đang học dở, vừa sai ba câu liền, và màn hình hứa sẽ giúp. Nếu lúc ấy gọi
 * mạng hỏng mà bé nhận được màn trắng thì đó là hỏng NẶNG HƠN không có phụ đạo:
 * bé vừa mất mạch học, vừa mất niềm tin vào cái nút vừa bấm.
 *
 * Nên thứ tự là NGƯỢC với trực giác: lấy câu TĨNH của chính nút gốc rễ TRƯỚC, đủ
 * rồi thì thôi. LLM chỉ được gọi khi kho tĩnh không đủ — và gọi hỏng thì vẫn còn
 * phần tĩnh đã có trong tay.
 *
 * ── ⚠ CÂU LLM SINH RA CŨNG PHẢI QUA HẬU KIỂM ──
 * Đây là chỗ duy nhất trong cả app mà câu hỏi KHÔNG do bộ sinh dựng sẵn, tức là
 * không có 83 cổng nào soi trước khi tới tay bé. `cauHopLe()` là hàng rào duy
 * nhất còn lại. Bỏ nó đi để "cho nhanh" là mở đúng cái cửa mà cả tầng chống ảo
 * giác từ vựng sinh ra để đóng.
 */
import { nutGocRe } from './lantruyen.js';
import { baiCuaNut } from './doThi.js';

/** Bài phụ đạo dài bao nhiêu câu. Ngắn — đây là chỗ gỡ, không phải bài học mới. */
export const SO_CAU_PHU_DAO = 4;

/**
 * Gom câu TĨNH quanh một nút, từ những bài đã tải sẵn.
 *
 * @param baiDs  [bài] các bài đang có trong tay (bài hiện tại + bài tiên quyết)
 *
 * ⚠ Ưu tiên câu BẬC THẤP. Bé đang mắc thì đừng đưa câu khó nhất của nút ấy —
 * mục đích là gỡ, và gỡ thì bắt đầu từ chỗ bé làm được.
 */
export function cauTinhCuaNut(baiDs, maNut, { soCau = SO_CAU_PHU_DAO } = {}) {
  if (!maNut) return [];
  const uu = ['warmup', 'standard', 'challenge'];
  const ra = [];
  for (const khoa of uu) {
    for (const b of (baiDs || [])) {
      for (const c of (b?.practice?.pools?.[khoa] || [])) {
        if (!c?.id) continue;
        if (c.maNut !== maNut && !(c.maNutDs || []).includes(maNut)) continue;
        if (ra.some((x) => x.id === c.id)) continue;
        ra.push(c);
        if (ra.length >= soCau) return ra;
      }
    }
  }
  return ra;
}

/**
 * Dựng một bài phụ đạo.
 *
 * @param goiLLM  async ({maNut, von, soCau}) => [câu] — KHÔNG bắt buộc. Thiếu, hay
 *                ném lỗi, hay trả rỗng: phụ đạo vẫn ra bài bằng phần tĩnh.
 * @param soiCau  (câu) => bool — hậu kiểm. MẶC ĐỊNH LÀ NHẬN HẾT chỉ khi chỗ gọi
 *                cố tình không truyền; chỗ gọi thật PHẢI truyền `cauHopLe`.
 *
 * Trả `{ nutGoc, cau, nguon, luiVe }`:
 *   nguon  'tinh' | 'llm' | 'tron'
 *   luiVe  true khi đã phải lùi vì LLM hỏng — để màn hình và nhật ký biết.
 */
export async function dungPhuDao({
  dt, mucThao, maNutMac, baiDs = [], von = null,
  goiLLM = null, soiCau = () => true, soCau = SO_CAU_PHU_DAO,
}) {
  /* Nút gốc rễ — nếu không tìm được thì vá ngay tại chỗ bé mắc. Đó không phải
     thất bại: nhiều nút không có tiên quyết nào, và chính nó là gốc. */
  const goc = nutGocRe(dt, mucThao, maNutMac, { toiDa: 1 })[0]?.ma || maNutMac;

  const tinh = cauTinhCuaNut(baiDs, goc, { soCau }).filter((c) => soiCau(c));
  if (tinh.length >= soCau || !goiLLM) {
    return {
      nutGoc: goc, cau: tinh.slice(0, soCau), nguon: 'tinh', luiVe: false,
      baiGoc: baiCuaNut(dt, goc) || null,
    };
  }

  /* Kho tĩnh không đủ → nhờ LLM. Hỏng thì GIỮ phần tĩnh đã có, không ném lên. */
  let them = [];
  let luiVe = false;
  try {
    const r = await goiLLM({ maNut: goc, von, soCau: soCau - tinh.length });
    them = Array.isArray(r) ? r : [];
  } catch { luiVe = true; them = []; }
  if (!them.length) luiVe = true;

  /* ⚠ HẬU KIỂM TỪNG CÂU MỘT. Câu LLM sinh là câu DUY NHẤT trong app không đi qua
     bộ sinh và 83 cổng; `soiCau` là hàng rào cuối cùng. */
  const sach = them.filter((c) => c && c.id && soiCau(c));
  const cau = [...tinh, ...sach].slice(0, soCau);
  return {
    nutGoc: goc,
    cau,
    nguon: sach.length ? (tinh.length ? 'tron' : 'llm') : 'tinh',
    luiVe: luiVe || sach.length < them.length,
    baiGoc: baiCuaNut(dt, goc) || null,
  };
}
