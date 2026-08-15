/* ═══════════ HÌNH CỦA KỲ SÁT HẠCH KHÔNG ĐƯỢC BIẾN MẤT ═══════════
 * chạy: node test/hinh_ky_sat_hach.test.mjs
 *
 * ── LỖI ĐÃ XẢY RA THẬT ──
 *
 * Mỗi lần tách một bài chữ thành bài video, hình của bài cũ thành mồ côi và phải
 * dọn đi. Lượt dọn ấy soi bằng câu hỏi "bài nào còn dùng hình này?" — mà có một
 * loại hình KHÔNG THUỘC BÀI NÀO: hình của kỳ ôn tập, khai bằng trường `onTap`.
 *
 *     L2H_CANH07 "Công viên: cột đèn đếm cách 5, ghế đá đếm cách 2" neo ở bài B08.
 *     B08 tách thành bài video, hình hết chủ, lượt dọn xoá cả tệp PNG lẫn dòng sổ.
 *     Nhưng kỳ ôn tập chương 2 vẫn hỏi "hàng cột đèn đánh số 5, 10, 15… có mấy
 *     cột?" — bé mở ra thấy câu hỏi tả một bức tranh không còn ở đó.
 *
 * Không có gì kêu: bài học không thiếu hình nào, sổ hình vẫn khớp chính nó, kỳ sát
 * hạch vẫn đủ câu. Chỉ lệch ở CHỖ NỐI giữa sổ hình và kỳ — mà không tệp nào sở hữu
 * chỗ nối ấy.
 *
 * ── BA PHÉP DƯỚI ĐÂY KHÉP KÍN CẢ HAI CHIỀU ──
 *
 * ① sổ khai `onTap` → kỳ ấy phải thật sự mang hình ấy   (bắt lượt dọn xoá nhầm)
 * ② kỳ mang hình nào → tệp PNG phải nằm trên đĩa        (bắt xoá tệp mà quên sổ)
 * ③ mã kiểm sha phải khớp tệp thật                      (bắt vẽ lại hình khác)
 *
 * Chiều ② mới là chiều quan trọng: nó soi thứ BÉ THẬT SỰ MỞ RA, không soi sổ sách.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
const ND = join(G, 'web/public/content');
const RV = join(ND, 'reviews');

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* Quyển nào có sổ hình thì soi quyển ấy — thêm quyển mới không phải sửa tệp này. */
const QUYEN = readdirSync(join(G, 'data'))
  .filter((f) => /^lop\d+_hinh_manifest\.json$/.test(f))
  .map((f) => ({ ma: f.split('_')[0], so: JSON.parse(readFileSync(join(G, 'data', f), 'utf8')) }));

const kyCua = (ma) => {
  const tienTo = `DCR_KSN${ma.replace('lop', '')}_`;
  return readdirSync(RV).filter((f) => f.startsWith(tienTo))
    .map((f) => [f, JSON.parse(readFileSync(join(RV, f), 'utf8'))]);
};

let tongOnTap = 0, tongGan = 0;
for (const Q of QUYEN) {
  const ky = kyCua(Q.ma);
  const mangCua = new Map(ky.map(([f, k]) => [f.replace(/^DCR_KSN\d+_|\.json$/g, ''),
    { f, ids: (k.hinh || []).map((h) => h.id), hinh: k.hinh || [] }]));

  /* ① Chiều sổ → kỳ. */
  const khai = Object.entries(Q.so).filter(([, v]) => v.onTap);
  tongOnTap += khai.length;
  const hut = khai
    .filter(([id, v]) => !(mangCua.get(v.onTap)?.ids || []).includes(id))
    .map(([id, v]) => `${id} khai onTap ${v.onTap} mà kỳ ấy không mang`);
  t(`${Q.ma} · hình khai cho kỳ đều đã gắn vào kỳ (${khai.length})`, hut.length === 0);
  if (hut.length) console.log('     ', hut.join(' · '));

  /* ② Chiều kỳ → đĩa. Đây là chiều bé thật sự đi qua. */
  for (const [, m] of mangCua) {
    tongGan += m.hinh.length;
    for (const h of m.hinh) {
      const p = join(ND, h.file || '');
      t(`${Q.ma} · ${m.f}: tệp ${h.file} có trên đĩa`, !!h.file && existsSync(p));
      if (h.file && existsSync(p)) {
        /* ③ Và phải đúng bức hình ấy, không phải bức khác cùng tên. */
        const sha = createHash('sha256').update(readFileSync(p)).digest('hex').slice(0, 16);
        t(`${Q.ma} · ${m.f}: ${h.id} đúng mã kiểm`, sha === h.sha256_16);
      }
      /* Có hình mà không có lời tả thì trình đọc màn hình đọc ra khoảng lặng. */
      t(`${Q.ma} · ${m.f}: ${h.id} có lời tả`, String(h.caption || '').length > 5);
    }
  }
}

/* Đếm ra con số, để lần sau ai đó "sửa cho xanh" bằng cách xoá nốt dữ liệu thì lộ. */
t(`có hình kỳ sát hạch để mà soi (${tongGan})`, tongGan > 0);
t(`sổ và kỳ khai cùng một số (${tongOnTap} ↔ ${tongGan})`, tongOnTap === tongGan);

console.log(`\n   ${QUYEN.length} quyển · ${tongGan} hình gắn vào kỳ sát hạch\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
