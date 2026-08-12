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

test('bảy hình, mỗi hình có tên và nét vẽ', () => {
  assert.equal(COI.length, 7);
  assert.deepEqual(COI.sort(), ['gate', 'hair', 'head', 'lake', 'run', 'top', 'wash']);
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
  const TA1 = new URL('../public/content/ta1/', import.meta.url);
  const dung = new Set();
  for (const f of readdirSync(TA1).filter((x) => x.startsWith('DL_TA1_B'))) {
    const b = JSON.parse(readFileSync(new URL(f, TA1)));
    for (const h of b.hinhTu || []) if (h.ve) dung.add(h.ve);
  }
  for (const v of dung) assert.ok(COI.includes(v), `bài khai hình "${v}" mà bộ hình không có`);
  assert.equal(dung.size, 7, 'cả bảy hình đều phải được dùng — hình thừa là hình chết');
});
