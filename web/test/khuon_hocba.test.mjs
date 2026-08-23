/**
 * CỔNG: mọi môn phải nộp `canCoGang` đúng khuôn mà màn dùng chung đọc.
 *
 * ── VÌ SAO CÓ CỔNG NÀY ──
 * Đi thử bản chạy 23-08-2026 thấy Sổ bố mẹ hiện thẳng câu "Cần cố gắng: Bài
 * undefined" cho bố mẹ đọc. Nguyên nhân: khuôn `HocBaMon` ở `soMon.js` có ghi
 * `canCoGang: [...]` nhưng KHÔNG ghi bên trong mỗi phần tử có gì. Toán nộp
 * `{id, so, ten, micro, chuong, lan, dung, tong}`, Tiếng Anh đoán thành
 * `{ma, best, tong}`, còn `ParentReport.jsx` ghép `Bài ${b.so}` — ra `undefined`.
 *
 * ⚠ ĐÂY LÀ HỌ LỖI "CHỖ NỐI", HỌ HAY GẶP NHẤT TRONG REPO NÀY: mỗi tệp đọc riêng
 * đều đúng, cái sai nằm ở CHỖ GIÁP giữa chúng, và không cổng nào nhận là của
 * mình. Phép dưới đây cố ý đứng đúng ở chỗ giáp: nó lấy TÊN TRƯỜNG mà màn dùng
 * chung thật sự đọc, rồi đòi mọi môn nộp đủ chừng ấy.
 */

import { readFileSync } from 'node:fs';

const doc = (d) => readFileSync(new URL(d, import.meta.url), 'utf8');
const chiMa = (s) => s
  .replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '))
  .replace(/^([ \t]*)\/\/.*$/gm, '$1');

let pass = 0; let fail = 0;
const ok = (dieu, ten, them = '') => {
  if (dieu) { pass += 1; } else { fail += 1; console.log(`  ✗ ${ten}${them ? ` — ${them}` : ''}`); }
};

/* ── 1. Trường nào màn dùng chung THẬT SỰ đọc ─────────────────────────────── */
const bao = chiMa(doc('../src/chung/components/ParentReport.jsx'));
/* Bắt mọi `b.<tên>` trong khối vẽ `canCoGang`. Đọc từ chính màn chứ không chép
   tay danh sách: chép tay thì thêm một trường mới là cổng lạc hậu ngay. */
const truongDoc = new Set([...bao.matchAll(/\bb\.(\w+)/g)].map((m) => m[1]));
ok(truongDoc.has('so'), 'màn tổng có đọc `b.so` (tiền đề của cả cổng này)');
ok(truongDoc.size >= 4, 'đọc được danh sách trường từ màn tổng', `chỉ thấy ${[...truongDoc]}`);

/* ── 2. Mỗi môn nộp đủ trường ấy — KIỂM BẰNG CÁCH CHẠY, KHÔNG PHẢI ĐỌC CHỮ ──
 *
 * ⚠ Bản đầu của phép này grep tên trường trong mã nguồn, và nó ĐỎ OAN môn Toán:
 * Toán lấy `so`·`ten` qua `{...b}` từ sổ đăng ký nên hai chữ ấy không xuất hiện ở
 * đâu cả, dù kết quả hoàn toàn đúng. Cổng ghim chính tả kiểu ấy ép người ta viết
 * mã xấu đi cho cổng xanh — đã dính nhiều lần. Nay GỌI HÀM rồi soi vật trả về.
 */
{
  const { baiCanCoGang } = await import('../src/mon/toan/lib/hocba.js');
  const { hocBaQuyen } = await import('../src/mon/tienganh/lib/hocba.js');

  const raToan = baiCanCoGang(
    { bai: [{ id: 'b1', so: 7, ten: 'Phép cộng', micro: 1, chuong: 2 }] },
    { micros: { b1: { pass: false, attempts: 3, best: 2, total: 5 } } },
  );
  const raTA = hocBaQuyen(
    { micros: { 'DL:TA3.B07': { pass: false, attempts: 2, score: 4, total: 9 } } },
    { ma: 'ta3', ten: 'Tiếng Anh lớp 3', bai: ['DL:TA3.B07'], soChuong: 5 },
  ).canCoGang;

  for (const [mon, ds] of [['toan', raToan], ['tienganh', raTA]]) {
    ok(ds.length === 1, `môn ${mon} trả đúng 1 bài cần cố gắng`, `trả ${ds.length}`);
    const b = ds[0] || {};
    /* `so` là trường DUY NHẤT màn tổng ghép thẳng vào câu tiếng Việt — thiếu nó
       là chữ "undefined" ra tới mắt bố mẹ, nên đòi gắt nhất ở đây. */
    ok(Number.isFinite(b.so), `môn ${mon}: \`so\` là số hữu hạn`,
      `ra ${JSON.stringify(b.so)} → màn tổng ghép thành "Bài undefined"`);
    for (const t of ['lan', 'dung', 'tong']) {
      ok(Number.isFinite(b[t]), `môn ${mon}: \`${t}\` là số`, `ra ${JSON.stringify(b[t])}`);
    }
    ok('ten' in b, `môn ${mon} có nộp \`ten\``);
  }
  /* Và số phải lấy ĐÚNG bài, không phải vị trí trong danh sách. */
  ok(raTA[0].so === 7, 'Tiếng Anh: DL:TA3.B07 ra số 7, không phải 0 (vị trí đầu mảng)',
    `ra ${raTA[0].so}`);
}

/* ── 3. Và màn tổng phải TỰ CHỐT, không tin môn nộp đủ ────────────────────── */
ok(/Number\.isFinite\(b\.so\)/.test(bao),
  'màn tổng lọc bài không có `so` trước khi ghép chuỗi',
  'môn thứ ba khai lệch là chữ `undefined` lại ra tới mắt bố mẹ');

/* ── 4. Số bài suy từ MÃ, không phải từ vị trí trong sổ đăng ký ───────────── */
{
  const { soBaiTuMa } = await import('../src/mon/tienganh/lib/hocba.js');
  ok(soBaiTuMa('DL:TA3.B00') === 0, 'B00 ra số 0, không phải null (bài Unit 0 có thật)');
  ok(soBaiTuMa('DL:TA3.B07') === 7, 'B07 ra số 7');
  ok(soBaiTuMa('hỏng') === null, 'mã sai khuôn trả null chứ không trả 0',
    'trả 0 thì mọi bài hỏng mã đều hiện thành "Bài 0"');
  ok(soBaiTuMa(null) === null, 'null vào thì null ra');
}

console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
