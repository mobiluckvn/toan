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
  luyennoi: 1,
  chamviet: 1,
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
];

export function locKhung(loiDan) {
  return String(loiDan || '')
    .split('\n')
    .filter((d) => d.trim() && !DAU_RIENG.some((r) => r.test(d)))
    .join('\n');
}
