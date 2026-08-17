/* ═══════════ HÌNH KHAI RA THÌ PHẢI CÓ MÀN NÀO VẼ ═══════════
 * chạy: node test/hinh_co_ai_ve.test.mjs
 *
 * ── VÌ SAO TÁM LƯỢT DỌN HÌNH MỒ CÔI VẪN ĐỂ LỌT ──
 *
 * Lượt dọn hình mồ côi hỏi: "tệp bài đã dựng có nhắc mã hình này không?" — grep
 * chuỗi. Phép ấy LUÔN trả lời CÓ, vì chính khối `figureSpec` trong tệp bài chứa mã
 * hình. Phép dọn tự chứng minh với chính nó.
 *
 * Hậu quả thật: `DL:KSN2.B23` sau khi thành bài video có `buildTeachSteps` trả về
 * KHÔNG MÀN GIẢNG NÀO, mà hai hình của nó khai `usedIn: ['teach_core']` và
 * `['trap']` — hai màn đã biến mất. Hai tệp PNG nằm trong bản dựng, tải về máy bé,
 * và không bao giờ hiện lên.
 *
 * ── PHÉP DƯỚI ĐÂY LÀM KHÁC ──
 *
 * Chạy CHÍNH `buildFlow` — đúng hàm mà màn hình gọi — rồi đếm hình nó thật sự lấy
 * ra. Hình nào khai trong `figureSpec` mà không màn nào lấy là hình chết.
 *
 * `figFor` trong `flow.js` quyết định hình nào rơi vào màn nào:
 *     teach_domain  → màn giảng thứ nhất
 *     teach_core    → màn giảng thứ hai
 *     trap          → màn giảng CUỐI
 *     screen:S3     → đích danh một màn
 *     item:C8       → gắn vào câu hỏi
 *     hook          → màn mở bài, và chỉ khi bài KHÔNG có lời chào
 * Bài dùng video không còn màn giảng nào, nên mọi hình `teach_*` và `trap` của nó
 * đều chết — đúng chỗ vừa lọt.
 *
 * ── HAI MÓN NỢ CŨ PHÉP NÀY VỪA TÌM RA (15-08-2026) ──
 *
 * Lớp 2 và lớp 3 nay sạch. Hai quyển kia còn nợ, và cả hai đều CÙNG MỘT DÒNG HỌ với
 * lỗi vừa sửa — hình gắn vào màn không còn tồn tại:
 *
 *   · lớp 4 · 29 hình. 28 hình khai `hook`: `figFor(lesson,'hook')` chỉ được gọi ở
 *     nhánh `if (coLoiChao && hook)`, mà 28 bài ấy có lời chào NHƯNG không còn màn
 *     `hook` nào (đã chuyển sang video), nên nhánh ấy không chạy. Thêm 1 hình
 *     `teach_core` ở B13, cùng ca với B23 của lớp 2.
 *   · lớp 5 Quyển 1 · 168 hình khai `mantra`. Bước `mantra` trong `buildFlow` KHÔNG
 *     mang khoá hình nào cả, và `StepView` case 'mantra' cũng không vẽ hình. Tức là
 *     168 hình ấy chưa từng hiện lên kể từ ngày dựng.
 *
 * NGƯỠNG ĐẶT Ở ĐÚNG CHỖ DỮ LIỆU ĐANG ĐỨNG: 0 cho hai quyển đã dọn, và niêm phong
 * đúng con số đang có cho hai quyển còn nợ — chỉ được giảm, không được tăng. Đòi 0
 * ngay cho cả bốn thì cổng đỏ liên miên và người ta sẽ tắt nó đi.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { buildFlow } from '../src/mon/toan/lib/flow.js';

const G = new URL('../../', import.meta.url).pathname;
const ND = join(G, 'web/public/content');

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (ds) => ds.slice(0, 5).forEach((x) => console.log('     ', x));

/* Quyển nào có thư mục bài thì soi quyển ấy — thêm quyển mới không phải sửa tệp này. */
const QUYEN = ['lop2', 'lop3', 'lop4', 'lessons']
  .filter((q) => existsSync(join(ND, q)));

/* Mọi khoá mà một bước có thể mang hình. Đọc thẳng từ `StepView.jsx` để hai nơi
   không lệch: thêm khoá mới bên ấy mà quên ở đây thì cổng báo chết oan. */
const KHOA_HINH = ['figure', 'figureBay', 'figureGiai'];
const sv = readFileSync(
  new URL('../src/mon/toan/components/StepView.jsx', import.meta.url), 'utf8');
const khoaSV = [...new Set((sv.match(/\bstep\.figure[A-Za-z]*/g) || [])
  .map((x) => x.replace('step.', '')))].sort();
t(`danh sách khoá hình khớp StepView (${khoaSV.join(', ')})`,
  JSON.stringify(khoaSV) === JSON.stringify([...KHOA_HINH].sort()));

let tongKhai = 0, tongVe = 0, tongBai = 0;
for (const q of QUYEN) {
  const tep = readdirSync(join(ND, q)).filter((f) => /^DL_.*\.json$/.test(f));
  if (!tep.length) continue;

  const chet = [];
  let khai = 0, ve = 0;
  for (const f of tep) {
    const b = JSON.parse(readFileSync(join(ND, q, f), 'utf8'));
    const spec = (b.figureSpec || []).map((h) => h.id);
    if (!spec.length) continue;
    khai += spec.length;
    tongBai += 1;

    /* Chạy đúng hàm mà màn hình gọi. Bài nào dựng lỗi thì coi như KHÔNG vẽ được
       hình nào — chứ đừng nuốt lỗi rồi báo xanh. */
    let dung = new Set();
    try {
      for (const s of buildFlow(b)) {
        /* BA khoá, không phải hai. Bản đầu chỉ đếm `figure` và `figureBay`, nên
           `figureGiai` — hình LỜI GIẢI hiện sau khi bé làm xong — bị báo chết oan
           ở 20 chỗ. Danh sách này phải khớp `StepView.jsx`; có phép kiểm bên dưới
           canh đúng chuyện ấy. */
        for (const k of KHOA_HINH) if (s[k]?.id) dung.add(s[k].id);
      }
    } catch (e) {
      chet.push(`${b.id}: buildFlow ném lỗi — ${e.message}`);
      continue;
    }
    ve += dung.size;
    for (const id of spec) {
      if (!dung.has(id)) {
        const h = b.figureSpec.find((x) => x.id === id);
        chet.push(`${b.id} · ${id} · usedIn ${JSON.stringify(h.usedIn)}`);
      }
    }
  }
  tongKhai += khai; tongVe += ve;
  /* ── NGƯỠNG: 0 CHO QUYỂN ĐÃ DỌN, NIÊM PHONG CHO QUYỂN CÒN NỢ ──
     Phép này ra đời hôm nay và tìm ra nợ cũ ở hai quyển. Đòi 0 ngay cho cả bốn thì
     cổng đỏ liên miên và người ta sẽ tắt nó đi — nên ghi đúng con số đang có, và
     CHỈ CHO PHÉP GIẢM. Sửa được chỗ nào thì hạ số ấy xuống; nó nhích lên là có hình
     chết mới. */
  /* `lessons` tụt dần theo từng đợt lớp 5 chuyển sang video: mỗi micro có video là
     bỏ luôn hình `mantra` chết của nó. Hạ con số này mỗi đợt — cổng tự in ra nhắc. */
  const NO = { lop2: 0, lop3: 0, lop4: 29, lessons: 39 };
  const muc = NO[q] ?? 0;
  t(`${q} · hình chết không được nhiều hơn ${muc} (đang ${chet.length})`,
    chet.length <= muc);
  if (chet.length < muc) {
    console.log(`     ↓ ${q} đã dọn bớt: ${chet.length}/${muc} — hạ con số trong `
      + '`NO` xuống để chốt lại.');
  }
  in5(chet);
}

/* Đảo chiều: phép trên chỉ có nghĩa khi nó THẬT SỰ chạy được buildFlow và lấy ra
   được hình. Không có hình nào lấy ra được thì "0 hình chết" là câu nói suông. */
t(`buildFlow có lấy ra hình thật (${tongVe} hình được màn nào đó vẽ)`, tongVe > 0);
t(`và có bài để mà soi (${tongBai} bài có figureSpec)`, tongBai > 0);

console.log(`\n   ${QUYEN.length} quyển · ${tongBai} bài có khai hình · `
  + `${tongKhai} hình khai · ${tongVe} hình được vẽ\n`);
console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
