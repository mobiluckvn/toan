/**
 * CỔNG · SỞ THÍCH NHỚ ĐƯỢC KHÔNG ĐƯỢC CHỌC THỦNG HÀNG RÀO VỐN TỪ.
 *
 * ── VIỆC NÀY LÀM GÌ ──
 * Phòng nói xưa nay hỏi bé "Con thích cái nào nhất?" rồi đưa câu trả lời vào lời
 * dặn LLM. Nhưng câu trả lời chỉ sống trong `useState` một phiên. Nay ghi xuống sổ
 * (`soThich`) để cô giáo máy còn nhớ ở buổi sau — mục 2.1.2 chiều Động lực.
 *
 * ── CÁI DỄ HỎNG, VÀ VÌ SAO CẦN CỔNG ──
 * Sổ sống lâu hơn nội dung. Bé đổi quyển, sách dồn unit, hay sổ cũ còn trên máy
 * sau một lần dựng lại — thì từ nhớ được có thể nằm NGOÀI vốn từ hiện tại. Mà
 * `dongHoSo()` nhét thẳng từ ấy vào lời dặn LLM.
 *
 * Hỏng ở đây KHÔNG giống mọi lỗi từ vựng khác. Hàng rào chống ảo giác có hai tầng:
 * lời dặn giới hạn vốn, rồi `cauHopLe()` soi lại đầu ra. Nhưng nếu chính LỜI DẶN
 * mời mô hình dùng một chữ ngoài vốn, thì mô hình nghe lời mà nói ra, rồi tầng soi
 * phía sau bác đúng câu ấy — cô giáo cứ nói, cứ bị bác, buổi học đứng im. Tầng hai
 * không cứu được cái hỏng do tầng một tự chuốc lấy.
 *
 * ── ĐẢO CHIỀU THỬ ──
 * Cổng nào cũng phải thử được cả hai chiều, nếu không xanh mà chẳng canh ai. Nên
 * mỗi phép dưới đây đều có một ca ĐÁNG LẼ PHẢI ĐỎ đi kèm.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  soRong, ghiSoThich, khoaSoThich, gopTienDo,
} from '../src/mon/tienganh/lib/progress.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');

test('ghi rồi đọc lại ra đúng từ, khoá theo QUYỂN', () => {
  const p = ghiSoThich(soRong(), 'ta5', 'dolphin', 3);
  const k = khoaSoThich('ta5');
  assert.equal(p.soThich[k].tu, 'dolphin');
  assert.equal(p.soThich[k].unit, 3);
  assert.ok(p.soThich[k].at, 'thiếu mốc thời gian thì phép gộp không so được bản nào mới');

  /* Khoá theo QUYỂN: chọn lại ở unit khác thì ĐÈ LÊN, không đẻ mục thứ hai. Mỗi
     unit một mục thì lại thành hỏi lại mỗi bài — đúng cái việc này đi sửa. */
  const q = ghiSoThich(p, 'ta5', 'football', 12);
  assert.equal(Object.keys(q.soThich).length, 1, 'mỗi quyển chỉ được MỘT mục sở thích');
  assert.equal(q.soThich[k].tu, 'football');

  /* Nhưng quyển KHÁC thì phải là mục khác — không thì học lớp 5 làm mất sở thích
     lớp 4, mà hai quyển hai vốn từ khác nhau. */
  const r = ghiSoThich(q, 'ta4', 'kite', 1);
  assert.equal(Object.keys(r.soThich).length, 2);
  assert.equal(r.soThich[khoaSoThich('ta4')].tu, 'kite');
  assert.equal(r.soThich[k].tu, 'football', 'ghi quyển khác mà đè mất quyển này');
});

test('gộp sổ máy với sổ máy chủ: bản MỚI HƠN thắng', () => {
  const k = khoaSoThich('ta5');
  const may = { ...soRong(), soThich: { [k]: { tu: 'cu', at: '2026-08-01T00:00:00Z' } } };
  const chu = { ...soRong(), soThich: { [k]: { tu: 'moi', at: '2026-08-20T00:00:00Z' } } };
  assert.equal(gopTienDo(may, chu).soThich[k].tu, 'moi');
  /* Đảo chiều: máy chủ CŨ hơn thì đừng đè bản mới ở máy — bé vừa chọn xong, đồng
     bộ về là mất ngay trước mắt. */
  assert.equal(gopTienDo(chu, may).soThich[k].tu, 'moi');
});

test('gộp không làm rơi sở thích khi một bên rỗng', () => {
  const k = khoaSoThich('ta5');
  const co = { ...soRong(), soThich: { [k]: { tu: 'dolphin', at: '2026-08-20T00:00:00Z' } } };
  assert.equal(gopTienDo(co, soRong()).soThich[k].tu, 'dolphin');
  assert.equal(gopTienDo(soRong(), co).soThich[k].tu, 'dolphin');
  /* Sổ cũ trên máy KHÔNG có trường `soThich` — `napTienDo` trải `soRong()` trước
     nên có sẵn `{}`, nhưng bản gộp cũng không được ném lỗi khi thiếu hẳn. */
  assert.doesNotThrow(() => gopTienDo({ micros: {}, chapters: {} }, co));
});

test('PhongNoi SOI LẠI từ nhớ được có còn trong vốn không', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/PhongNoi.jsx'));

  /* Phải có phép soi, và phép soi phải dựa trên CHÍNH `von` — chứ không phải tin
     thẳng `soThich.tu`. Bắt bằng hình dạng: có `von.loi.tu` trong cùng khối tính
     `thichNho`, và `hoSo` gửi đi là `thichDung` chứ không phải `soThich.tu`. */
  const i = ma.indexOf('thichNho');
  assert.notEqual(i, -1, 'PhongNoi không còn phép soi sở thích nhớ được');
  const khoi = ma.slice(i, i + 500);
  assert.match(khoi, /von\.loi\.tu/,
    'phép soi không đối chiếu với vốn từ — từ ngoài vốn sẽ chui thẳng vào lời dặn LLM');

  assert.match(ma, /hoSo:\s*\{\s*thich:\s*thichDung\s*\}/,
    'lời dặn LLM đang nhận `thich` thô, không qua phép soi');
  assert.doesNotMatch(ma, /hoSo:\s*\{\s*thich:\s*soThich/,
    'gửi thẳng từ trong sổ vào lời dặn là bỏ qua phép soi');

  /* Nhớ được rồi thì ĐỪNG HỎI LẠI — không thì phần nhớ thành vô nghĩa. */
  assert.match(ma, /!laTranh\s*&&\s*!thichDung\s*&&\s*hoiThich/,
    'thẻ hỏi sở thích vẫn hiện dù đã nhớ được từ buổi trước');

  /* Bài tả tranh KHÔNG hỏi sở thích — bác chốt 19-08-2026. Giữ nguyên nhánh ấy. */
  assert.match(ma, /!laTranh/, 'mất nhánh chặn thẻ sở thích ở bài tả tranh');
});

test('chỗ GHI nằm ở ManTiengAnh, không nằm rải rác', () => {
  /* Không phải chuyện gu kiến trúc: cổng `hocba_khop_luat.test.mjs` chỉ soi
     `luuMucHocBa` trong CHÍNH tệp ManTiengAnh. Gọi ở chỗ khác thì hình dạng gói
     không ai canh, mà sai hình dạng gói thì máy chủ từ chối trong im lặng. */
  const man = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(man, /luuMucHocBa\(learnerId,\s*'soThich'/,
    'ManTiengAnh không đẩy sở thích lên máy chủ');
  const phong = chiMa(doc('../src/mon/tienganh/components/PhongNoi.jsx'));
  assert.doesNotMatch(phong, /luuMucHocBa/,
    'PhongNoi gọi thẳng luuMucHocBa — cổng khớp-luật không soi tệp này');
});

test('luật Firestore đã mở cho soThich, và bên đọc đã nhặt', () => {
  /* Bốn chỗ phải khớp nhau. Ba chỗ soi được ở đây; bước deploy rules thì không
     cổng nào canh được — ghi trong chú thích của `firestore.rules`. */
  const luat = chiMa(doc('../firestore.rules'));
  const i = luat.indexOf('match /hocBaTA/{userId}/muc/{mucId}');
  assert.notEqual(i, -1);
  const khoi = luat.slice(i, luat.indexOf('}', luat.indexOf('allow write', i)));
  assert.match(khoi, /'soThich'/, 'luật chưa cho ghi soThich — máy chủ sẽ từ chối, im lặng');

  const du = chiMa(doc('../src/mon/tienganh/lib/duLieu.js'));
  assert.match(du, /v\.loai === 'soThich'/, 'bên đọc không nhặt soThich — ghi lên rồi bỏ đó');
  assert.match(du, /soThich: hb\.soThich/, '`tienDoTuMay` không trả soThich ra ngoài');
});
