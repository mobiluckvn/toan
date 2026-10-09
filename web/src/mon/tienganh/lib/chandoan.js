/**
 * CHẨN ĐOÁN BẰNG LỜI — nói cho bé (và bố mẹ) biết VÌ SAO lại ôn lại chỗ này.
 *
 * ── VÌ SAO CẦN ──
 * Phụ đạo đã chạy từ 26-08: bé sai một câu, hệ thống lần ngược đồ thị tìm nút gốc
 * rễ, rồi mời bé làm bốn câu ở nút ấy. Nhưng lời mời chỉ là "Mình ôn lại một chút
 * nhé" — bé không biết ôn cái gì, bố mẹ không biết vì sao con đang làm một bài
 * trông chẳng liên quan tới bài đang học.
 *
 * Mà hệ thống BIẾT lý do: nó vừa tính ra nút nào bé mắc và nút nào là gốc. Không
 * nói ra thì cả tầng lan truyền ngược — thứ đắt nhất của môn này — nhìn từ phía bé
 * chỉ là một bài tập ngẫu nhiên.
 *
 * ── MỘT CÂU, ĐỌC TO ĐƯỢC, KHÔNG SỐ ──
 * Giữ đúng quy ước của `dongHoSo` và `dongHoSoAI`: câu nào ở đây cũng phải KHÔNG
 * SAO nếu đọc to lên trước mặt bé. "Nút sp_g1_u12_1 có P(L)=0,23" thì không phải
 * câu như thế — và nó cũng chẳng nói gì với một đứa trẻ sáu tuổi.
 *
 * ── THUẦN, KHÔNG GỌI MẠNG ──
 * Chẩn đoán suy được hết từ đồ thị và cái nhãn lượt (V2). Không có lý gì tốn một
 * lời gọi cho một câu mà code viết được.
 */
import { nhanNut, baiCuaNut } from './doThi.js';

/** Trần ký tự câu chẩn đoán. Nó được ĐỌC TO cho bé nghe, nên phải ngắn. */
export const CHAN_DOAN_TOI_DA_CHU = 120;

/**
 * Nhãn nút → mẩu chữ đọc được cho bé.
 *
 * ⚠ NHÃN NÚT MẪU CÂU LÀ MỘT CÔNG THỨC: `She's + [Verb-ing].` Đọc nguyên văn thì
 * bé nghe cả dấu ngoặc vuông và dấu cộng. Bóc chúng ra, giữ lại phần đọc được.
 */
export function chuDeNut(dt, ma) {
  const n = nhanNut(dt, ma);
  if (!n) return '';
  return String(n)
    /* Ô trống thành dấu lửng: `She's + [Verb-ing].` → `She's …` Đọc nguyên văn thì
       bé nghe cả dấu ngoặc vuông và dấu cộng. */
    .replace(/\s*\+\s*/g, ' ')
    .replace(/\[([^\]]+)\]/g, '…')
    /* `….` đọc ra một dấu chấm lửng rồi một dấu chấm — gộp lại. */
    .replace(/…\s*[.!?]+/g, '…')
    /* ⚠ NHÃN NÚT TỪ VỰNG LÀ `mango — quả xoài`: chữ Anh KÈM nghĩa Việt. Giữ CẢ HAI
       và để `tachTheoTieng` tách lúc đọc (`PhuDao.jsx` làm thế) — bỏ phần tiếng Anh
       thì bé không biết đang ôn CHỮ NÀO, mà bỏ phần nghĩa thì bé sáu tuổi không
       hiểu chữ ấy là gì. Chỉ đổi gạch ngang dài sang dấu phẩy cho câu đọc trôi. */
    .replace(/\s*—\s*/g, ', ')
    .replace(/\s+/g, ' ')
    .trim();
}

/* Mỗi nhãn lượt (V2) một cách nói "con vừa vướng ở đâu" — tiếng Việt, cho bé. */
const VI_NHAN = {
  thieuTu: 'con bỏ sót một chữ',
  saiThuTu: 'con nói đúng chữ nhưng chưa đúng thứ tự',
  nhamTu: 'con lẫn hai chữ với nhau',
  lacDe: 'câu con nói chưa đúng việc',
  imLang: 'câu này còn khó với con',
  tiengViet: 'câu này còn khó với con',
  hoiLai: 'con còn đang hỏi về chỗ này',
  dung: '',
  moDau: '',
};

/**
 * CÂU CHẨN ĐOÁN.
 *
 * @param nutSai    nút bé vừa mắc
 * @param nutGocRe  nút GỐC RỄ lần ngược ra được — có thể trùng `nutSai`
 * @param nhan      nhãn lượt của V2 (không bắt buộc)
 *
 * ⚠ GỐC RỄ TRÙNG NÚT SAI LÀ CHUYỆN THƯỜNG, KHÔNG PHẢI LỖI. Nhiều nút không có
 * tiên quyết nào, và chính nó là gốc. Lúc ấy câu phải nói khác đi — "mình ôn lại
 * chính chỗ ấy" — chứ không được nói "ôn cái trước nó" về một cái không tồn tại.
 */
export function cauChanDoan({ dt = null, nutSai = null, nutGocRe = null, nhan = null } = {}) {
  const goc = nutGocRe || nutSai;
  const chuGoc = chuDeNut(dt, goc);
  const vi = VI_NHAN[nhan] || '';
  const cungNut = !goc || !nutSai || goc === nutSai;

  const phan = [];
  if (vi) phan.push(`Vừa rồi ${vi}`);
  if (cungNut) {
    phan.push(chuGoc ? `mình ôn lại “${chuGoc}” một chút nhé` : 'mình ôn lại chỗ này một chút nhé');
  } else {
    phan.push(chuGoc
      ? `mà chỗ này dựng trên “${chuGoc}” — mình ôn cái đó trước nhé`
      : 'mà chỗ này dựng trên một bài cũ — mình ôn bài đó trước nhé');
  }
  const s = `${phan.join(', ').replace(/^./, (c) => c.toUpperCase())}.`;
  return s.length > CHAN_DOAN_TOI_DA_CHU
    ? `${s.slice(0, CHAN_DOAN_TOI_DA_CHU - 2).trim()}…` : s;
}

/**
 * GRADER CHO CÂU TĨNH — câu này có thật là của ĐÚNG nút ấy không.
 *
 * ── VÌ SAO CẦN, KHI `cauTinhCuaNut` ĐÃ LỌC THEO NÚT ──
 * `cauTinhCuaNut` nhận câu khi `c.maNut === maNut` HOẶC `maNut` nằm trong
 * `c.maNutDs`. Mà `maNutDs` là danh sách MỌI nút câu ấy chạm tới — một câu ôn tập
 * cuối chương chạm năm nút, nên nó "thuộc" cả năm. Lấy nó đi phụ đạo cho một nút
 * cụ thể thì bé làm một câu rộng hơn hẳn chỗ nó đang mắc, mà hệ thống vẫn ghi là
 * "đã phụ đạo nút ấy" — ΔC đo ra một con số về một việc không xảy ra.
 *
 * Nên chấm: 1 khi nút ấy là nút CHÍNH của câu (hoặc câu chỉ chạm ít nút), 0 khi
 * câu là câu rộng. Thuần code, 0 chi phí — §7 bước 1 nói rõ chỉ cân nhắc grader
 * bằng mô hình nếu đo thấy câu tĩnh lệch nút nhiều.
 */
export const NUT_TOI_DA_MOT_CAU = 2;

export function chamCauTinh(cau, { maNut, doThi = null } = {}) {
  if (!cau || !maNut) return 0;
  if (cau.maNut === maNut) return 1;
  const ds = Array.isArray(cau.maNutDs) ? cau.maNutDs.filter(Boolean) : [];
  if (!ds.includes(maNut)) return 0;
  /* Câu chạm quá nhiều nút là câu ÔN TẬP, không phải câu của một nút. */
  if (ds.length > NUT_TOI_DA_MOT_CAU) return 0;
  /* Và nút ấy phải dạy ở một bài THẬT — nút không có bài thì không có gì để ôn. */
  return doThi && !baiCuaNut(doThi, maNut) ? 0 : 1;
}
