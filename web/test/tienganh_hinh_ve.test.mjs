/**
 * CỔNG · BẢY HÌNH VẼ TAY, MỘT NGUỒN DUY NHẤT.
 *
 * Món nợ cũ: video hiện thẻ chữ thay cho hình, vì Pillow không dựng nổi SVG.
 * Cách chữa dễ nhất — vẽ lại 7 hình bằng Pillow cho video — cũng là cách sai
 * nhất: thành HAI bản vẽ của cùng một cái cổng, và hai bản thì sớm muộn cũng
 * lệch. Lệch kiểu ấy không có gì bắt được: bản dựng xanh, video chạy trơn, chỉ
 * có bé là thấy cái cổng trên màn hình khác cái cổng trong video.
 *
 * Nên cổng này canh đúng MỘT điều: hai bên vẫn đang đọc chung một tệp.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const NGUON = '../src/mon/tienganh/lib/hinh_ve.json';
const KHO = JSON.parse(doc(NGUON));
const COI = Object.keys(KHO.hinh);

test('mỗi hình vẽ tay có tên và có nét vẽ', () => {
  /* Bản đầu ghim cứng `COI.length === 7` và liệt kê đủ bảy tên. Ghim thế thì mỗi
     lần thêm một hình là cổng đỏ vì lý do KHÔNG PHẢI lỗi — và người sửa dễ nới
     bừa con số cho xanh, tức là cổng mất hẳn ý nghĩa. Đợt soát hình 14-08 thêm
     bốn hình (desk · mop · ball · garden) và đỏ đúng ở đây.
     Nay không đếm nữa: danh sách ĐÚNG là danh sách các bài đang dùng — phép kiểm
     thứ tư ở dưới so hai chiều, vừa chặn hình thiếu vừa chặn hình chết. */
  assert.ok(COI.length >= 7, 'bộ hình không được rỗng');
  for (const [k, v] of Object.entries(KHO.hinh)) {
    assert.ok(v.ten, `${k} thiếu tên đọc lên cho máy đọc màn hình`);
    assert.ok(v.than?.includes('<'), `${k} không có nét vẽ nào`);
    /* Nét vẽ phải là SVG THUẦN, không lẫn cú pháp JSX: `{...net}` hay `fill={M.go}`
       thì trình duyệt vẽ được (React tự dịch) nhưng cairosvg thì không — video sẽ
       ra ô trống mà không báo lỗi gì. */
    assert.doesNotMatch(v.than, /\{|\}/, `${k} còn lẫn cú pháp JSX, cairosvg không đọc được`);
  }
  assert.equal(KHO._khungNhin, '0 0 64 64');
});

test('màn hình ĐỌC tệp chung, không vẽ bản riêng', () => {
  const jsx = doc('../src/mon/tienganh/components/HinhVe.jsx');
  assert.match(jsx, /from '\.\.\/lib\/hinh_ve\.json'/);
  /* Không còn nét vẽ nào viết thẳng trong JSX — đó chính là bản thứ hai. */
  assert.doesNotMatch(jsx, /<path\s+d=/, 'còn nét vẽ nội tuyến trong JSX');
  assert.doesNotMatch(jsx, /<ellipse|<rect\s/, 'còn hình khối nội tuyến trong JSX');
});

test('video ĐỌC ĐÚNG tệp ấy, không phải bản chép', () => {
  const py = doc('../../tools/video/hinh_ve.py');
  assert.match(py, /'web' \/ 'src' \/ 'mon' \/ 'tienganh' \/ 'lib' \/ 'hinh_ve\.json'/,
    'bên Python phải trỏ vào chính tệp màn hình đang đọc');
  const dung = doc('../../tools/video/dung_video.py');
  assert.match(dung, /hinh_ve\.dan\(/, 'khung dựng phải dán hình vẽ tay');
  assert.doesNotMatch(dung, /chỗ giữ, không vẽ emoji sai[\s\S]{0,40}ve=/,
    'không được quay lại thẻ chữ khi đã có hình');

  const kb = doc('../../tools/video/kich_ban.py');
  assert.match(kb, /_hinh_cua_tu/, 'kịch bản phải mang theo khoá hình vẽ tay');
});

test('mọi khoá `ve` trong bài đều có hình thật', () => {
  /* Đây là chỗ hỏng câm điển hình: khai `ve: "gate"` trong dữ liệu bài mà bộ hình
     không có khoá ấy thì màn hình lặng lẽ rơi về emoji, video rơi về thẻ chữ, và
     không ai biết cho tới khi nhìn tận mắt. */
  /* ⚠ QUÉT MỌI QUYỂN TIẾNG ANH, đừng ghim một cái.
     Bản đầu chỉ đọc `ta1/`. Thêm quyển lớp 2 là năm hình vẽ tay của nó bị báo
     "không bài nào dùng" — cổng đỏ vì một lý do KHÔNG PHẢI lỗi, và người sửa dễ
     nới bừa cho xanh. Đúng cái bẫy 5 ghi ở §3 sổ dây chuyền. */
  const GOC = new URL('../public/content/', import.meta.url);
  const QUYEN = readdirSync(GOC, { withFileTypes: true })
    .filter((d) => d.isDirectory() && /^ta\d+$/.test(d.name))
    .map((d) => d.name);
  assert.ok(QUYEN.length, 'không thấy quyển Tiếng Anh nào — glob rỗng thì mọi phép đếm xanh trơn');
  const dung = new Set();
  let soBai = 0;
  for (const q of QUYEN) {
    const T = new URL(`${q}/`, GOC);
    for (const f of readdirSync(T).filter((x) => /^DL_TA\d+_B.*\.json$/.test(x))) {
      const b = JSON.parse(readFileSync(new URL(f, T)));
      soBai += 1;
      for (const h of b.hinhTu || []) if (h.ve) dung.add(h.ve);
    }
  }
  assert.ok(soBai >= 16, `chỉ thấy ${soBai} bài — chạy nhầm thư mục thì phép đếm vô nghĩa`);
  for (const v of dung) assert.ok(COI.includes(v), `bài khai hình "${v}" mà bộ hình không có`);
  /* Hai chiều: bài khai hình nào thì bộ hình phải có (trên), và bộ hình có gì thì
     phải có bài dùng (dưới). Hình chết không ai thấy, nên không ai sửa khi nó hỏng. */
  for (const k of COI) assert.ok(dung.has(k), `bộ hình có "${k}" mà không bài nào dùng`);
  assert.equal(dung.size, COI.length, 'số hình dùng phải bằng số hình có');
});
