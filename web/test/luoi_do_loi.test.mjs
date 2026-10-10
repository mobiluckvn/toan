import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

/**
 * CỔNG CHO LƯỚI ĐỠ KHI MÀN VỠ.
 *
 * ── ⚠ CỔNG NÀY ĐỌC MÃ NGUỒN, KHÔNG DỰNG MÀN — VÀ ĐÓ LÀ MỘT HẠN CHẾ THẬT ──
 * Kho này chạy cổng bằng `node` trần: không có bộ dịch JSX, không có DOM giả. Nên
 * một cổng dựng thật `LuoiDoLoi` rồi cho một component con ném lỗi thì chạy không
 * được ở đây — đúng cái lỗ hổng đã để HAI lỗi `ReferenceError` lên tới bản thật.
 *
 * Phần dựng thật tôi đã đo bằng tay (`react-dom/server`, màn đỡ đặt sẵn trạng thái
 * "đã vỡ"): màn đỡ tự dựng được · có câu cho bé · có nút bấm được · không lộ vết
 * lỗi · `getDerivedStateFromError` trả `{vo:true}` · có `componentDidCatch`.
 *
 * Còn cổng này giữ những điều KHÔNG được phép trôi mất giữa hai lần sửa:
 * lưới đỡ có được NỐI không, nối ở ĐÚNG CHỖ không, và nó có nuốt lỗi không. Ba điều
 * ấy đọc từ mã nguồn là đủ chắc, và chúng mới là chỗ người ta hay lỡ tay.
 */

const doc = (d) => readFileSync(new URL(d, import.meta.url), 'utf8');
const main = doc('../src/main.jsx');
const luoi = doc('../src/chung/components/LuoiDoLoi.jsx');

test('lưới đỡ được nối ở NGOÀI CÙNG, bọc cả App', () => {
  /* Bọc bên trong App thì một lỗi ở tầng trên lưới vẫn cho ra trang trắng. Thứ tự
     này là cả tác dụng của lưới. */
  assert.match(main, /<LuoiDoLoi>\s*<App\s*\/>\s*<\/LuoiDoLoi>/,
    'main.jsx phải dựng <LuoiDoLoi><App /></LuoiDoLoi>');
  assert.match(main, /import LuoiDoLoi from/);
});

test('lưới đỡ KHÔNG nạp động, không nằm sau một `await` nào có thể hỏng', () => {
  /* `napNguong()` đứng trước phần dựng. Nếu lưới đỡ cũng nạp động sau đó thì một
     lỗi trong chính bước nạp lại cho ra trang trắng — tức lưới không đỡ được đúng
     lúc cần nhất. Nên nó phải là `import` tĩnh ở đầu tệp. */
  const dauTep = main.slice(0, main.indexOf('const batDau'));
  assert.match(dauTep, /^import LuoiDoLoi from/m, 'phải import TĨNH ở đầu tệp');
  assert.ok(!/await import\([^)]*LuoiDoLoi/.test(main), 'không được nạp động');
});

test('bắt lỗi bằng CẢ HAI móc của React', () => {
  /* `getDerivedStateFromError` đổi trạng thái để vẽ màn đỡ; `componentDidCatch` là
     chỗ duy nhất còn nhìn thấy vết gọi hàm. Thiếu cái đầu thì không có màn đỡ;
     thiếu cái sau thì có màn đỡ mà không ai lần ra được lỗi. */
  assert.match(luoi, /static getDerivedStateFromError\s*\(/);
  assert.match(luoi, /componentDidCatch\s*\(/);
});

test('KHÔNG nuốt lỗi — vẫn in ra console', () => {
  /* Lưới đỡ im lặng thì nó che mất chính thứ nó đang đỡ: màn vẫn hỏng, chỉ là hỏng
     đẹp hơn, và không ai biết để đi sửa. */
  assert.match(luoi, /console\.error\(\s*'\[màn vỡ\]'/);
  assert.match(luoi, /componentStack/, 'phải giữ vết cây component — thứ duy nhất chỉ ra chỗ hỏng');
});

test('KHÔNG hiện chi tiết lỗi cho bé', () => {
  /* Vết gọi hàm là chữ của người lớn và có thể lộ đường dẫn nội bộ. Phần vẽ ra màn
     (sau `render()`) không được chạm tới đối tượng lỗi. */
  const ve = luoi.slice(luoi.indexOf('render()'));
  assert.ok(!/\{\s*(this\.state\.loi|loi\.message|loi\.stack|componentStack)/.test(ve),
    'không được đổ nội dung lỗi vào phần hiển thị');
});

test('có ĐƯỜNG RA bé tự đi được, không chỉ có "tải lại"', () => {
  /* Tải lại mà lỗi nằm ở màn đầu thì bé quay về đúng chỗ vỡ, lặp vô tận. Nút thứ
     hai dựng lại cây từ đầu (`key` đổi) và dọn chỗ đứng. */
  assert.match(luoi, /Về kệ sách, học tiếp/);
  assert.match(luoi, /sessionStorage\.clear/);
  assert.match(luoi, /key=\{this\.state\.khoa\}/,
    'phải đổi `key` — không thì cây cũ giữ nguyên state hỏng và vỡ lại ngay');
});

test('dọn chỗ đứng nhưng KHÔNG đụng tới bài bé đã học', () => {
  /* `localStorage` giữ sổ tại máy — thứ duy nhất còn công học của bé khi chưa đăng
     nhập. Xoá nó để "cho sạch" là lấy mất bài của trẻ vì một lỗi của người lớn. */
  assert.ok(!/localStorage\.clear/.test(luoi), 'KHÔNG được xoá sổ tại máy');
});

test('lưới đỡ không phụ thuộc gì ngoài React', () => {
  /* Nó là thứ chạy KHI mọi thứ khác đã hỏng. Kéo thêm một module vào là thêm một
     đường cho chính nó vỡ theo. */
  const nhap = [...luoi.matchAll(/^import .* from '([^']+)'/gm)].map((m) => m[1]);
  assert.deepEqual(nhap, ['react'], `lưới đỡ chỉ được import 'react', đang có: ${nhap.join(', ')}`);
});
