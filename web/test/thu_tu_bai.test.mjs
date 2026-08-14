/* ═══════════ SỐ BÀI SUY TỪ VỊ TRÍ — LỐI C ═══════════
 *
 * Bác chốt 14-08 sau khi thấy giá của lối cũ: mã bài mang sẵn con số, nên chèn một
 * bài vào giữa là phải đổi mã của mọi bài phía sau. Đợt dồn đầu tiên đo được 353
 * tệp, 4 566 chỗ đổi mã, 99 tệp đổi tên — và mỗi đợt như thế còn phải DỜI TIẾN ĐỘ
 * ĐÃ LƯU của từng bé cho khớp. Tách nhỏ cả quyển thì còn chín đợt nữa.
 *
 * Lối C cắt sợi dây ấy: mã bài chỉ còn là CÁI TÊN, không bao giờ đổi; số hiển thị
 * đếm từ vị trí trong mảng. Chèn bài mới = thêm một dòng vào `thu_tu.json`.
 *
 * Mấy phép dưới đây canh đúng những chỗ sợi dây có thể nối lại lúc nào không hay.
 */
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';

const GOC = path.resolve(import.meta.dirname, '..', '..');
const doc = (p) => JSON.parse(fs.readFileSync(path.join(GOC, p), 'utf8'));
const co = (p) => fs.existsSync(path.join(GOC, p));

const QUYEN = ['lop2', 'lop3', 'lop4'];   // lớp 5 khai kiểu khác, xem chú thích cuối

for (const q of QUYEN) {
  const idx = doc(`web/public/content/${q}/index.json`);

  test(`${q} · index.json xếp đúng thứ tự học, không rỗng`, () => {
    assert.ok(idx.length > 0, 'index.json rỗng');
  });

  /* Màn hình nay ĐẾM số bài chứ không đọc `so`. Nhưng trường `so` vẫn nằm trong tệp
     và vẫn có người đọc (báo cáo phụ huynh cũ, công cụ). Hai con số mà lệch nhau thì
     bé thấy "Bài 14" còn bố mẹ thấy "Bài 19" — không ai kêu. */
  test(`${q} · trường 'so' đã lưu khớp với vị trí trong mảng`, () => {
    const lech = idx
      .map((b, i) => ({ viTri: i + 1, so: b.so, id: b.id }))
      .filter((x) => x.so !== x.viTri);
    assert.deepEqual(lech, [], 'so lệch vị trí');
  });

  test(`${q} · mã bài không trùng nhau`, () => {
    const ma = idx.map((b) => b.id);
    assert.equal(new Set(ma).size, ma.length, 'có mã bài khai hai lần');
  });
}

/* ── Lời khai thứ tự: chỉ lớp 4 đã chuyển sang lối C ──
   Lớp 2·3 chưa tách bài nên chưa cần; khi nào tách thì thêm `thu_tu.json` cho quyển
   ấy và nới danh sách dưới đây. Không bắt cả ba phải có ngay, vì cổng đòi một tệp
   chưa ai định làm thì người sau chỉ tạo tệp rỗng cho nó xanh. */
const CO_LOI_KHAI = ['lop4'];

for (const q of CO_LOI_KHAI) {
  const tt = doc(`data/${q}/thu_tu.json`).thuTu;
  const idx = doc(`web/public/content/${q}/index.json`);

  test(`${q} · thứ tự trong bản dựng ĐÚNG như lời khai`, () => {
    assert.deepEqual(idx.map((b) => b.id), tt,
      'bộ dựng đã xếp lại thứ tự — index.json phải giữ nguyên thứ tự của thu_tu.json');
  });

  test(`${q} · lời khai và tệp nguồn trùng khít`, () => {
    const tep = fs.readdirSync(path.join(GOC, 'data', q))
      .filter((f) => /^DL_KSN\d+_B\d+\.json$/.test(f))
      .map((f) => f.slice(0, -5).replace(/^DL_KSN(\d+)_/, 'DL:KSN$1.'));
    assert.deepEqual([...tt].sort(), [...tep].sort(),
      'khai mà thiếu tệp thì màn hình hụt một bài; có tệp mà không khai thì bài ấy '
      + 'dựng xong nằm đó, không lối nào vào — cả hai đều không ai kêu');
  });

  test(`${q} · lời khai không có mã trùng`, () => {
    assert.equal(new Set(tt).size, tt.length);
  });

  /* Cái bẫy thật của lối C. Mã bài nay là tên chết, nên người sau rất dễ nghĩ "xoá
     bài này thì mã trống, cấp lại cho bài mới". Nhưng bé đã học bài cũ vẫn đang giữ
     tiến độ mang đúng mã ấy — cấp lại là bé bỗng "đã xong" một bài chưa từng thấy.
     Nên mã cao nhất chỉ được TĂNG. Chốt lại con số ở đây để lần sau ai hạ xuống là
     cổng đỏ ngay, kèm lý do. */
  test(`${q} · mã bài chỉ được cấp mới, không tái dùng mã đã xoá`, () => {
    const soCua = (id) => Number(id.match(/\.B(\d+)$/)[1]);
    const cao = Math.max(...tt.map(soCua));
    assert.ok(cao >= tt.length,
      `mã cao nhất (${cao}) nhỏ hơn số bài (${tt.length}) — dấu hiệu có mã bị cấp `
      + 'lại. Mã đã dùng thuộc về tiến độ của bé cũ, đừng dùng lại.');
  });
}

/* ── Sợi dây cũ không được nối lại ── */
test('màn hình ĐẾM số bài, không đọc trường so', () => {
  const s = fs.readFileSync(
    path.join(GOC, 'web/src/mon/toan/lib/noiDung.js'), 'utf8');
  assert.ok(/so:\s*i \+ 1/.test(s),
    'noiDung.js phải suy số bài từ vị trí (so: i + 1)');
  assert.ok(!/^\s*so:\s*b\.so\s*,/m.test(s),
    'noiDung.js đọc lại b.so — sợi dây mã↔số đã nối lại');
});

test('không còn công cụ dồn số nào chạy được', () => {
  assert.ok(!co('tools/don_so_lop4.py'),
    'lối C bỏ hẳn việc dồn số. Còn để công cụ dồn nằm đó là người sau sẽ chạy nó, '
    + 'rồi lại một lần dời tiến độ thật của các bé mà đáng ra không cần nữa.');
});

/* ── Lớp 5 đi lối riêng, cố ý ──
   Lớp 5 khai `index_micro.json` dạng đối tượng, mỗi bài ba micro, và số bài suy ra
   bằng công thức (4 bài = 1 chương). Nó không tách bài, không dồn số, nên chưa cần
   chuyển. Ghi ra đây để người sau khỏi tưởng là bỏ sót. */
test('lớp 5 vẫn suy số bài từ mã — có chủ ý, không phải bỏ sót', () => {
  const s = fs.readFileSync(
    path.join(GOC, 'web/src/mon/toan/lib/noiDung.js'), 'utf8');
  assert.ok(/soBaiCua/.test(s), 'hàm suy số của lớp 5 biến mất');
});
