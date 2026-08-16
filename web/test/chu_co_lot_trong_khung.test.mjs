/* ═══════════ CHỮ VIẾT TRONG KHUNG THÌ PHẢI LỌT TRONG KHUNG ═══════════
 * chạy: node test/chu_co_lot_trong_khung.test.mjs
 *
 * ── LỖI ĐÃ XẢY RA THẬT (16-08-2026) ──
 *
 * Nhánh `cong_thuc` của `dung_video.py` vẽ ô "Thay số vào thử" cao ĐÓNG CỨNG 120px
 * — vừa đúng MỘT dòng chữ cỡ 42. Câu nào dài hơn một dòng thì `giua()` xuống dòng
 * bình thường, và dòng thứ hai rơi xuống DƯỚI đáy khung: chữ đen nằm trần trên nền,
 * nửa trong nửa ngoài cái viền xanh.
 *
 * 72 TRONG 419 MÀN CÔNG THỨC của cả bốn quyển đã lên bản thật như thế. Không cổng
 * nào kêu, vì:
 *   · `soi()` chỉ soi lời đọc, từ cấm và thứ tự màn — không soi bề rộng chữ;
 *   · `canh_video_khong_roi_chu` hỏi "khoá có ai đọc không", mà khoá `thay` thì CÓ
 *     người đọc — nó chỉ vẽ ra ngoài khung;
 *   · mp4 dựng ra bình thường, đủ cảnh, đủ tiếng, đủ dung lượng.
 * Chỉ lộ ra khi rút khung hình ra nhìn bằng mắt (lớp 5 bài 17).
 *
 * ── PHÉP DƯỚI ĐÂY SOI GÌ ──
 *
 * Đo chữ bằng CHÍNH bộ chữ và CHÍNH phép ngắt dòng mà bộ vẽ dùng (`ngat_dong`),
 * rồi hỏi: khối chữ ấy có nằm lọt trong cái khung vẽ quanh nó không. Đo bằng số ký
 * tự là vô nghĩa — chữ tiếng Việt có dấu rộng hẹp khác nhau, và đó đúng là chỗ 72
 * màn kia lọt lưới.
 */
import { execFileSync } from 'node:child_process';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const ra = execFileSync('tools/tts/.venv/bin/python', ['-c', `
import sys, json; sys.path.insert(0, 'tools/video')
import dung_video as D, kich_ban_toan as K
from PIL import Image, ImageDraw
d = ImageDraw.Draw(Image.new('RGB', (D.W, D.H)))

# Mỗi mục: (tên chỗ, cỡ chữ, bề rộng cho phép, đỉnh khung, đáy khung, y chữ bắt đầu)
# — chép đúng theo nhánh 'cong_thuc' trong dung_video.py.
def do(chu, co, rong):
    f = D.phong(co)
    n = len(D.ngat_dong(d, chu, f, rong))
    return n, int(f.size * 1.32) * n

out = []
for ma in sorted(K.BO):
    m = ma.replace('DL:', 'DL_').replace('.', '_')
    try: kb = K.kich_ban(m)
    except SystemExit: continue
    for c in kb['canh']:
        if c['loai'] != 'cong_thuc': continue
        n, cao = do(c['congThuc'], 46, D.W - 190)
        # khung công thức: the(60, 120, W-120, 210) → 120..330, chữ từ y=175
        out.append({'bai': ma, 'cho': 'congThuc', 'day': 175 + cao, 'khung': 330})
        if c.get('thay'):
            f = D.phong(42); b = int(f.size * 1.32)
            n2 = len(D.ngat_dong(d, c['thay'], f, D.W - 260))
            cao_khung = max(120, b * n2 + 64)
            y = 430 + (cao_khung - b * n2) // 2
            out.append({'bai': ma, 'cho': 'thay',
                        'day': y + b * n2, 'khung': 430 + cao_khung})
print(json.dumps(out, ensure_ascii=False))
`], { cwd: G, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });

const o = JSON.parse(ra);
t(`đọc được các màn công thức (${o.length} khối chữ)`, o.length > 400);

const tran = o.filter((x) => x.day > x.khung);
t(`không khối chữ nào tràn khỏi khung (${tran.length} khối tràn)`, tran.length === 0);
tran.slice(0, 8).forEach((x) => console.log(
  `      ${x.bai} · ${x.cho} — chữ chạm ${x.day}px, khung hết ở ${x.khung}px`));

/* Đảo chiều: phép trên chỉ có nghĩa nếu nó BẮT ĐƯỢC một khối cố tình tràn. Không
   có bước này thì một hôm `ngat_dong` trả về mảng rỗng là mọi thứ xanh oan. */
const thu = execFileSync('tools/tts/.venv/bin/python', ['-c', `
import sys; sys.path.insert(0, 'tools/video')
import dung_video as D
from PIL import Image, ImageDraw
d = ImageDraw.Draw(Image.new('RGB', (D.W, D.H)))
f = D.phong(42)
dai = ' '.join(['chữ'] * 40)
print(len(D.ngat_dong(d, dai, f, D.W - 260)), len(D.ngat_dong(d, 'ngắn', f, D.W - 260)))
`], { cwd: G, encoding: 'utf8' }).trim().split(' ').map(Number);
t('(đối chứng) câu dài ngắt ra nhiều dòng, câu ngắn đúng một dòng',
  thu[0] > 2 && thu[1] === 1);

console.log(`\n   ${new Set(o.map((x) => x.bai)).size} bài · ${o.length} khối chữ đã đo\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
