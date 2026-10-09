/**
 * VÂN TAY PROMPT — đủ để so hai mẫu lời dặn, KHÔNG lưu một chữ nào của bé.
 *
 * ── VÌ SAO KHÔNG LƯU NGUYÊN VĂN ──
 * Giao ước của kho này là "Máy chủ KHÔNG lưu gì" (bác chốt, ghi ở
 * `goiPhongNoi.js:7` và `goiChamViet.js:9`). Nhưng mục 2.5.2 và 2.5.3 của luận
 * văn cần biết LƯỢT NÀY DÙNG MẪU PROMPT NÀO thì mới trả lời được câu "mẫu nào dạy
 * hiệu quả hơn" — đó chính là phép tối ưu prompt theo ΔC.
 *
 * Hai đòi hỏi ấy nhìn thì chọi nhau. Chúng chỉ chọi nếu ta tưởng phải lưu CẢ
 * PROMPT. Thật ra để so hai mẫu thì chỉ cần biết hai lượt có dùng CÙNG mẫu hay
 * không — mà điều đó một mã băm nói được, còn nội dung thì không cần.
 *
 * Bác chốt đường này 21-08-2026.
 *
 * ── ⚠ VÂN TAY LÀ MỘT CHIỀU, NHƯNG KHÔNG PHẢI LÀ VÔ DANH ──
 * Băm không lộ nội dung, nhưng nếu băm CẢ prompt thì mỗi lượt ra một vân tay
 * riêng (prompt có tên bé, có vốn từ của unit, có lịch sử hội thoại) — vừa vô
 * dụng cho việc so mẫu, vừa thành một mã theo dõi được từng lượt của từng bé.
 *
 * Nên băm ĐÚNG PHẦN KHUNG: cái phần giống nhau ở mọi lượt dùng cùng một mẫu. Phần
 * thay đổi theo bé (tên · vốn từ · hội thoại · bài viết) bị BỎ RA trước khi băm.
 * Nhờ thế hai bé khác nhau học cùng unit cho ra CÙNG một vân tay — đó vừa là điều
 * làm phép so có nghĩa, vừa là điều làm nó không lần ra ai.
 */
import { createHash } from 'node:crypto';

/**
 * PHIÊN BẢN MẪU LỜI DẶN — tăng tay mỗi khi sửa lời dặn theo cách đáng kể.
 *
 * Vì sao cần khi đã có mã băm: băm đổi khi MỘT ký tự đổi, kể cả sửa lỗi chính tả.
 * Số phiên bản nói ra chủ ý của người sửa — "đây là lần đổi đáng kể" — nên bảng
 * so ΔC gom theo số này, còn mã băm dùng để phát hiện lệch ngoài ý muốn (ai đó
 * sửa lời dặn mà quên tăng số).
 */
export const PHIEN_BAN_MAU = {
  /* 2 từ 09-10-2026 (việc V2): luật 7 · 8 · 8b rời khối chung sang `loidan_nhan.js`
     thành chín nhánh theo nhãn, luật 8c giữ lại và mang số 7, hai luật cuối lùi số.
     Đổi đáng kể, nên bảng so ΔC không được gom chung với lượt của mẫu 1. */
  luyennoi: 2,
  /* 2 từ 09-10-2026 (việc V4): một lời dặn tách thành CHUỖI BA mắt xích (tìm lỗi ·
     sửa · lời cho bố mẹ), và khung vân tay nay là ba khung ghép lại. Đổi đáng kể. */
  chamviet: 2,
};

/** Băm ngắn — 12 ký tự hex là đủ tách vài chục mẫu, và ngắn thì đọc log dễ. */
const bam = (s) => createHash('sha256').update(s, 'utf8').digest('hex').slice(0, 12);

/**
 * Vân tay của một lượt gọi.
 *
 * @param mau    tên mẫu: 'luyennoi' | 'chamviet'
 * @param khung  PHẦN KHUNG của lời dặn — chuỗi giống nhau ở mọi lượt cùng mẫu.
 *               ⚠ KHÔNG truyền phần có tên bé, vốn từ, hội thoại hay bài viết.
 * @param them   những mẩu khác cũng thuộc khung và cũng cần vào vân tay
 *               (mô hình, nhiệt độ…) — thứ đổi thì kết quả đổi, nên phải tính.
 */
export function vanTay(mau, khung, them = {}) {
  const phan = [
    `mau=${mau}`,
    `v=${PHIEN_BAN_MAU[mau] ?? 0}`,
    ...Object.keys(them).sort().map((k) => `${k}=${them[k]}`),
    `khung=${String(khung || '')}`,
  ].join('\n');
  return {
    mauPrompt: mau,
    phienBanMau: PHIEN_BAN_MAU[mau] ?? 0,
    vanTayPrompt: bam(phan),
  };
}

/**
 * Bỏ phần RIÊNG của bé ra khỏi một lời dặn, giữ lại khung.
 *
 * Dùng khi lời dặn dựng thành một chuỗi liền và không tách sẵn khung ra được.
 * Cắt theo DÒNG: dòng nào chứa dữ liệu của bé thì bỏ cả dòng.
 *
 * ⚠ Đây là lưới đỡ, KHÔNG phải cách làm chính. Cách đúng là chỗ gọi tự truyền
 * phần khung — vì chỉ chỗ ấy biết chắc mẩu nào là của bé. Hàm này lọc theo dấu
 * hiệu, mà lọc theo dấu hiệu thì sót được: thêm một dòng mới mang tên bé mà quên
 * khai vào đây là nó lọt vào vân tay, và không có gì báo.
 */
export const DAU_RIENG = [
  /vốn từ/i, /bảng từ/i, /mẫu câu bé/i, /bé viết/i, /bé nói/i,
  /the child/i, /tên bé/i, /^-\s/,
  /* ── DÒNG MANG CHỮ BÉ VỪA NÓI, từ việc V2 ──
     `loidan_nhan.js` mở đầu MỌI dòng mang dữ liệu của bé bằng đúng chữ `CHILD:`
     (hằng `DAU_DONG_RIENG` bên ấy). Một dấu hiệu khai sẵn và duy nhất thì chắc hơn
     đi đoán theo lời văn: thêm một nhãn mới mà quên khai cụm từ của nó vào đây là
     chữ của bé lọt vào vân tay, và không có gì báo — chính chỗ sót mà `luyennoi.js`
     đã nói trước là sẽ sót.
     Ba mẫu dưới là lưới đỡ thứ hai, cho trường hợp ai đó viết dòng riêng mà quên
     tiền tố. Cổng `tienganh_nhanluot.test.mjs` soi TÍNH CHẤT (đem từng giá trị của
     `chiTiet` đi tìm trong phần khung còn lại), không soi chính tả mấy mẫu này. */
  /^\s*CHILD:/i, /she said/i, /she asked/i, /left out:/i,
];

/**
 * ⚠ KHỐI BỌC DẤU — chắc hơn lọc theo dòng, và là cách nên dùng cho khối mới.
 *
 * Lọc theo dòng thì mỗi dòng mới phải khai một mẫu vào `DAU_RIENG`, và quên khai là
 * chữ của bé lọt vào vân tay mà không gì báo. Khối thì khai MỘT lần: mọi thứ giữa
 * hai dấu bị bỏ, kể cả dòng thêm vào sau này.
 *
 * Giao ước với `DAU_KHOI_RIENG` · `CUOI_KHOI_RIENG` ở
 * `web/src/mon/tienganh/lib/bangtrangthai.js` (từ V6; trước đó ở `phongnoi.js`, nay
 * tệp ấy chỉ tái xuất) — đổi một bên là phải đổi bên kia. Máy chủ và máy con không
 * import chéo được (cổng `ranh_gioi.test.mjs` chặn), nên hai hằng này là CHÉP, và
 * cổng `tienganh_bangtrangthai.test.mjs` so hai bản — đúng lối `lib/onlai.js` ↔
 * `functions/src/schedule.js`.
 */
export const KHOI_RIENG = { mo: '<<RIENG', dong: 'RIENG>>' };

export function locKhung(loiDan) {
  const ds = String(loiDan || '').split('\n');
  const giu = [];
  let trongKhoi = false;
  for (const d of ds) {
    if (d.includes(KHOI_RIENG.mo)) { trongKhoi = true; continue; }
    if (d.includes(KHOI_RIENG.dong)) { trongKhoi = false; continue; }
    if (trongKhoi) continue;
    if (!d.trim()) continue;
    if (DAU_RIENG.some((r) => r.test(d))) continue;
    giu.push(d);
  }
  return giu.join('\n');
}
