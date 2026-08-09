/**
 * HÌNH PHẢI ĐẾM ĐƯỢC — soi hình lớp 2.
 * chạy: node test/hinhdem.test.mjs
 *
 * Bài đếm hình có một đòi hỏi mà nhìn lướt không thấy thiếu: bé phải ĐẾM ĐƯỢC
 * TRÊN HÌNH. Vẽ mỗi loại một cái rồi ghi số bên dưới thì đáp án nằm sẵn, bé chẳng
 * đếm gì — mà hình vẫn "có hình, có số, có lời chú", nên qua mắt rất dễ.
 *
 * Bảy hình đã dính: ba tam giác RỜI NHAU cho câu "2 đơn + 1 ghép = 3"; hai chữ
 * nhật cho câu "ô cửa 2 × 2 có mấy hình vuông"; hai khối rời ghi sẵn "4 khối" cho
 * bài đếm khối bị che; 15 viên kẹo cho đề "17 viên".
 *
 * CỐ Ý KHÔNG soi "nói còn thừa N thì phải vẽ N". Đã thử: lời chú "7 thừa 1 nên 7
 * là số LẺ" nói về TÍNH CHẤT của số 7, mà viên lẻ ấy đã vẽ ngay trong nhóm rồi —
 * máy vẫn kêu. Phân biệt hai nghĩa ấy bằng mẫu chữ là đoán mò.
 *
 * CỐ Ý KHÔNG soi phép tính ghi trên hình. Đã thử: "41 − 34 = 49 − 42 = 7" (đẳng
 * thức nối), "(8 + 6) × 2 × 4 = 112" (ngoặc), "24 − 8 = 1 phần" (số đếm phần chứ
 * không phải kết quả), "6 giờ 50 + 15" (giờ) — máy đều kêu oan. Đã quét tay một
 * lượt 205 biểu thức của cả ba quyển: không phép nào sai. Bài kiểm hay kêu oan
 * thì người sau sẽ tắt nó đi, lúc ấy mất luôn cả những phép kiểm đúng.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const hinh = JSON.parse(readFileSync(join(G, 'data/lop2_hinh.json'), 'utf8'));

/* ── 1. Nhãn nói "N cái" mà nguyên mẫu chỉ vẽ MỘT ────────────────────────────
   `hinh_phang` và `khoi_hop` vẽ đúng một hình cho mỗi mục khai báo, nên nhãn ghi
   "4 khối" nghĩa là một khối đang đeo biển "4 khối". Trừ mục có `luoi` (ô kẻ vạch)
   hoặc `chia` (hình tròn chia phần): những phần ấy đã vẽ ra thật, đếm được. */
const MOT_MOT = { hinh_phang: 'hinh', khoi_hop: 'khoi' };
const DEM_SO = /(\d+)\s*(khối|ô|hình|cái|mảnh|tam giác|phần)/g;
const lac = [];
for (const x of hinh) {
  const key = MOT_MOT[x.arch];
  if (!key) continue;
  for (const m of x.params?.[key] || []) {
    if (m.luoi || m.chia) continue;
    const nhan = [m.ten, ...(m.canh || [])].filter(Boolean).join(' ');
    for (const [, n, dv] of nhan.matchAll(DEM_SO)) {
      if (Number(n) >= 2) lac.push(`${x.id} (${x.bai}) — nhãn "${n} ${dv}" mà chỉ vẽ một`);
    }
  }
}
t(`không hình nào đeo biển số thay cho vẽ thật (soi ${hinh.length} hình)`, lac.length === 0);
in5(lac);

/* ── 2. Mọi hình đều gọi được một nguyên mẫu có thật ──────────────────────────
   Thiếu nguyên mẫu thì `tools/ve_hinh_lop2.py` dừng hẳn, nhưng chỉ khi có người
   nhớ chạy nó. Soi ở đây để lỡ quên vẽ lại vẫn biết. */
const src = readFileSync(join(G, 'figforge/arch_l2.py'), 'utf8');
const thieu = [...new Set(hinh.map((x) => x.arch))].filter((a) => !src.includes(`def ${a}(`));
t(`nguyên mẫu nào cũng có thật (${new Set(hinh.map((x) => x.arch)).size} nguyên mẫu)`,
  thieu.length === 0);
in5(thieu);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
