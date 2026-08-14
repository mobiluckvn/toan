/**
 * CỔNG · VIDEO MỞ BÀI + BÀI GIẢNG CỦA TOÁN.
 *
 * Bác chốt 14-08: *"phần Mở bài và bài giảng xây thành video và KHÔNG DÙNG ẨN DỤ,
 * để học sinh lần đầu xem video sẽ hiểu. Dùng cách tạo video như Tiếng Anh lớp 1."*
 *
 * Ba thứ có thể hỏng mà không kêu, nên phải canh:
 *   1. bài KHAI có video mà tệp không tồn tại → bé thấy một ô đen;
 *   2. video dựng rồi mà bài KHÔNG khai → nằm đó không ai xem;
 *   3. ẩn dụ mọc lại vào lời đọc — mà lời đọc thì không ai đọc lại bao giờ.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';

const APP = new URL('../public/content/lop4/', import.meta.url);
const VIDEO = new URL('../public/content/toan/video/', import.meta.url);
const AUDIO = new URL('../public/content/toan/audio/', import.meta.url);

const tep = readdirSync(APP).filter((f) => /^DL_KSN4_B\d+\.json$/.test(f)).sort();
assert.equal(tep.length, 49, `phải thấy 49 bài, đang thấy ${tep.length}`);
const BAI = tep.map((f) => JSON.parse(readFileSync(new URL(f, APP), 'utf8')));
const coVideo = BAI.filter((b) => b.video?.giang);

test('năm bài dãy số đều có video, và tệp CÓ THẬT', () => {
  const can = ['DL:KSN4.B13', 'DL:KSN4.B14', 'DL:KSN4.B15', 'DL:KSN4.B16', 'DL:KSN4.B17'];
  for (const id of can) {
    const b = BAI.find((x) => x.id === id);
    assert.ok(b?.video?.giang, `${id} chưa khai video`);
    const p = new URL(b.video.giang, VIDEO);
    assert.ok(existsSync(p), `${id}: khai "${b.video.giang}" mà không có tệp`);
    assert.ok(statSync(p).size > 200_000, `${id}: tệp video bé bất thường`);
  }
});

test('KHÔNG bài nào khai video mà thiếu tệp', () => {
  /* Khai thừa thì màn mở bài hiện một ô đen — `onLoi` có kêu, nhưng bé thì ngồi
     nhìn ô đen và tưởng máy hỏng. */
  const xau = coVideo.filter((b) => !existsSync(new URL(b.video.giang, VIDEO)));
  assert.deepEqual(xau.map((b) => b.id), []);
});

test('KHÔNG video nào dựng rồi mà không bài nào dùng', () => {
  /* Chiều ngược lại: dựng xong quên khai thì video nằm đó, tốn dung lượng, và bé
     không bao giờ được xem. Cùng luật hai chiều đã dùng cho hình vẽ tay. */
  const dung = new Set(coVideo.map((b) => b.video.giang));
  const co = readdirSync(VIDEO).filter((f) => f.endsWith('.mp4'));
  assert.deepEqual(co.filter((f) => !dung.has(f)), []);
});

test('mọi clip tiếng của video đều có tệp — không cảnh nào CÂM', () => {
  const so = JSON.parse(readFileSync(new URL('../public/content/toan/lop4_am.json', import.meta.url), 'utf8'));
  const xau = so.clip.filter((c) => !existsSync(new URL(c.tep, AUDIO)));
  assert.deepEqual(xau.map((c) => c.id), []);
  assert.ok(so.clip.length >= 30, `sổ tra âm chỉ có ${so.clip.length} clip`);
});

test('KHÔNG ẩn dụ trong lời đọc — luật bác dặn', () => {
  /* Danh sách này trùng `TU_CAM` của `tools/video/kich_ban_toan.py`. Hai nơi cùng
     canh một luật là cố ý: bên Python chặn lúc DỰNG, bên này chặn cái đã dựng ra
     — sửa tay tệp sổ tra âm cũng không lọt. */
  const CAM = /(kỹ sư|xưởng|thám tử|tuyệt kỹ|vũ khí|bí kíp|thần chú|mật mã|mật thư|hoa tiêu|quan tòa|cao thủ|đơn hàng|Su Kem|Trí Long|bước chân|dấu vân tay|người giải|chìa khoá|không gian toán)/i;
  const so = JSON.parse(readFileSync(new URL('../public/content/toan/lop4_am.json', import.meta.url), 'utf8'));
  const xau = so.clip.filter((c) => CAM.test(c.chu || ''))
    .map((c) => `${c.id}: "${CAM.exec(c.chu)[0]}"`);
  assert.deepEqual(xau, [], `${xau.length} câu đọc còn ẩn dụ`);
});

test('lời đọc KHÔNG còn CHỮ SỐ — mọi con số đọc thành chữ', () => {
  /* Bác dặn 14-08: "các thông tin cần chuyển thành chữ hết". Số viết có dấu cách
     phân nhóm là chỗ hỏng rõ nhất: "1 275" đọc thành "một, hai trăm bảy mươi lăm".
     Chữ HIỆN LÊN màn hình vẫn là số — bé nhìn số dễ hơn nhìn chữ — nhưng chữ ĐEM
     ĐỌC thì phải thành lời. */
  const so = JSON.parse(readFileSync(new URL('../public/content/toan/lop4_am.json', import.meta.url), 'utf8'));
  const xau = so.clip.filter((c) => /\d/.test(c.chu || ''))
    .map((c) => `${c.id}: "${c.chu.slice(0, 50)}"`);
  assert.deepEqual(xau, [], `${xau.length} câu đọc còn chữ số`);
});

test('câu đọc NGẮN — không câu nào quá một hơi', () => {
  /* Bản đầu có câu 300 chữ (đọc trọn chuyện mở bài của giáo án). Bác xem xong bảo
     "mở bài quá nhiều". Nay trần 130 chữ, và bỏ hẳn phần chuyện dẫn. */
  const so = JSON.parse(readFileSync(new URL('../public/content/toan/lop4_am.json', import.meta.url), 'utf8'));
  const dai = so.clip.filter((c) => (c.chu || '').length > 130)
    .map((c) => `${c.id}: ${c.chu.length} chữ`);
  assert.deepEqual(dai, []);
});

test('video NGẮN — mỗi bài dưới hai phút', () => {
  /* Video dài thì bé xem một lần rồi thôi, mà bài này cần xem lại. */
  const co = readdirSync(VIDEO).filter((f) => f.endsWith('.mp4'));
  const to = co.filter((f) => statSync(new URL(f, VIDEO)).size > 1_500_000);
  assert.deepEqual(to, [], 'video quá lớn — nhiều khả năng dài quá hai phút');
});

test('lời đọc KHÔNG mang ký hiệu chỉ có nghĩa với mắt', () => {
  /* Dấu `;` ngăn số hạng đọc lên thành "chấm phẩy"; `×` `−` `=` phải thành lời.
     Bỏ bước này thì clip nghe như máy đánh vần ký hiệu. */
  const so = JSON.parse(readFileSync(new URL('../public/content/toan/lop4_am.json', import.meta.url), 'utf8'));
  const KY_HIEU = /[;×÷−=“”"]|\.\.\./;
  const xau = so.clip.filter((c) => KY_HIEU.test(c.chu || ''))
    .map((c) => `${c.id}: "${KY_HIEU.exec(c.chu)[0]}"`);
  assert.deepEqual(xau, []);
});

test('màn MỞ BÀI có gọi Video, và trỏ đúng thư mục của Toán', () => {
  /* Dựng video xong mà quên gắn vào màn hình thì mọi phép trên vẫn xanh, còn bé
     thì không thấy video nào. Soi thẳng chỗ nối. */
  const sv = readFileSync(new URL('../src/mon/toan/components/StepView.jsx', import.meta.url), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '').replace(/\{\/\*[\s\S]*?\*\/\}/g, '');
  assert.match(sv, /import Video from '\.\.\/\.\.\/\.\.\/chung\/components\/Video\.jsx'/);
  assert.match(sv, /lesson\.video\?\.giang/, 'phải hỏi bài có video không');
  assert.match(sv, /thuMuc="toan"/, 'phải trỏ thư mục toan, không dùng mặc định tienganh');
});

test('Video là component CHUNG — không chép bản thứ hai', () => {
  /* Chép một bản riêng cho Toán thì hai bản sớm muộn lệch, mà chỗ lệch là mấy luật
     đã tính riêng cho bé: không tự chạy, không cho tua, xem xong mới mở nút. */
  const chung = new URL('../src/chung/components/Video.jsx', import.meta.url);
  assert.ok(existsSync(chung), 'Video.jsx phải nằm ở vùng chung');
  assert.ok(!existsSync(new URL('../src/mon/tienganh/components/Video.jsx', import.meta.url)),
    'bản cũ trong mon/tienganh phải được dọn đi');
  const s = readFileSync(chung, 'utf8');
  assert.match(s, /thuMuc = 'tienganh'/, 'phải nhận thư mục qua tham số');
  assert.doesNotMatch(s.replace(/\/\*[\s\S]*?\*\//g, ''), /content\}\/tienganh\/video/,
    'không được ghim cứng thư mục tienganh trong đường dẫn');
});
