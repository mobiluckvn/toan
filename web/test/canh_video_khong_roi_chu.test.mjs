/* ═══════════ KHAI GÌ TRONG KỊCH BẢN THÌ BỘ VẼ PHẢI DÙNG TỚI ═══════════
 * chạy: node test/canh_video_khong_roi_chu.test.mjs
 *
 * ── LỖI ĐÃ XẢY RA THẬT (16-08-2026) ──
 *
 * Kịch bản viết:
 *
 *     _c('de_toan', 'Đề bài', de='Chia 17 viên bi vào các hộp, mỗi hộp 3 viên')
 *
 * mà `dung_video.khung()` ở nhánh `de_toan` chỉ đọc `chuChinh`, KHÔNG hề đọc `de`.
 * Kết quả: khung trắng trơn mang đúng hai chữ "Đề bài", trong khi tiếng vẫn đọc
 * trọn đề bài. Bé nghe một đằng, nhìn một nẻo, và không có gì để đọc lại.
 *
 * 27 VIDEO LỚP 2 ĐÃ LÊN BẢN THẬT như thế. Không cổng nào kêu, vì:
 *   · kịch bản hợp lệ — `soi()` chỉ soi lời đọc và công thức;
 *   · mp4 dựng ra bình thường, đủ cảnh, đủ tiếng, đủ dung lượng;
 *   · `video_toan.test.mjs` chỉ hỏi "có tệp không", không hỏi "trong tệp có gì".
 * Chỉ lộ ra khi rút khung hình ra nhìn bằng mắt.
 *
 * ── PHÉP DƯỚI ĐÂY SOI GÌ ──
 *
 * Với MỖI loại cảnh: gom mọi khoá mà kịch bản thật sự truyền vào, rồi đối chiếu
 * với thân hàm vẽ của loại ấy. Khoá nào kịch bản khai mà bộ vẽ không nhắc tới là
 * chữ rơi mất — hoặc kịch bản gõ nhầm tên khoá, hoặc bộ vẽ quên đọc.
 *
 * Đây là phép hai chiều, cùng dòng họ với `hinh_co_ai_ve` (hình khai mà không màn
 * nào vẽ) và `video_toan` (video dựng mà không bài nào dùng).
 */
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* Gọi thẳng python để lấy MỌI cảnh của MỌI kịch bản đã viết — đừng chép lại danh
   sách bài ở đây, thêm bài mới là lệch ngay. */
const ra = execFileSync('python3', ['-c', `
import sys, json; sys.path.insert(0, 'tools/video')
import kich_ban_toan as K
out = []
for ma in sorted(K.BO):
    m = ma.replace('DL:', 'DL_').replace('.', '_')
    try: kb = K.kich_ban(m)
    except SystemExit: continue
    for c in kb['canh']:
        out.append({'bai': ma, 'loai': c['loai'],
                    'khoa': [k for k, v in c.items()
                             if k not in ('loai', 'loiAm', 'am')
                             and v not in (None, '', [], {})]})
print(json.dumps(out, ensure_ascii=False))
`], { cwd: G, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
const canh = JSON.parse(ra);
t(`đọc được kịch bản (${canh.length} cảnh)`, canh.length > 500);

/* Cắt thân hàm vẽ của từng loại cảnh ra khỏi `khung()`. Các nhánh viết theo đúng
   một khuôn `elif L == "<tên>":` nên cắt được bằng chính khuôn ấy. */
const dv = readFileSync(new URL('../../tools/video/dung_video.py', import.meta.url), 'utf8');
const moc = [...dv.matchAll(/^ {4}(?:el)?if L == "([a-z_0-9]+)":/gm)];
t(`tìm thấy các nhánh vẽ trong dung_video.py (${moc.length} loại)`, moc.length > 20);

const than = {};
moc.forEach((m, i) => {
  const dau = m.index;
  const cuoi = i + 1 < moc.length ? moc[i + 1].index : dv.indexOf('\n    return im', dau);
  than[m[1]] = dv.slice(dau, cuoi);
});

/* `chuChinh` và `chuPhu` đi qua `_c()` cho MỌI loại cảnh, kể cả loại không vẽ chúng
   (ví dụ `bia` vẽ bằng đường khác). Chỉ soi các khoá RIÊNG của từng cảnh — đó đúng
   là chỗ gõ nhầm tên hoặc quên đọc. */
const BO_QUA = new Set(['chuChinh', 'chuPhu']);

const roi = new Map();
for (const c of canh) {
  const t2 = than[c.loai];
  if (!t2) { roi.set(`${c.loai}: KHÔNG có nhánh vẽ nào`, c.bai); continue; }
  for (const k of c.khoa) {
    if (BO_QUA.has(k)) continue;
    if (t2.includes(`"${k}"`) || t2.includes(`'${k}'`)) continue;
    const khoaLoi = `${c.loai}.${k}`;
    if (!roi.has(khoaLoi)) roi.set(khoaLoi, c.bai);
  }
}
t(`không khoá nào rơi mất (${roi.size} khoá)`, roi.size === 0);
[...roi].slice(0, 8).forEach(([k, b]) => console.log(`      ${k} — kịch bản khai ở ${b}, bộ vẽ không đọc`));

/* Đảo chiều: phép trên chỉ có nghĩa khi nó THẬT SỰ soi được vào thân hàm. Nếu cắt
   thân sai thì mọi khoá đều "không thấy" và phép sẽ đỏ — nhưng nếu cắt ra chuỗi
   rỗng mà `includes` vẫn trả true thì nó xanh oan. Nên đòi một khoá CÓ THẬT và một
   khoá CHẮC CHẮN KHÔNG CÓ. */
t('(đối chứng) nhánh de_toan có đọc khoá `de`',
  /\bde\b/.test(than.de_toan || '') && (than.de_toan || '').includes('"de"'));
t('(đối chứng) và không đọc một khoá bịa ra',
  !(than.de_toan || '').includes('"khoa_bia_ra"'));

console.log(`\n   ${canh.length} cảnh · ${moc.length} loại cảnh · `
  + `${new Set(canh.map((c) => c.bai)).size} bài\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
