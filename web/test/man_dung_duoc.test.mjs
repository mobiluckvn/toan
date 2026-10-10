import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { build } from 'esbuild';
import React from 'react';
import { renderToString } from 'react-dom/server';

/**
 * DỰNG THẬT MỘT MÀN REACT — lỗ hổng C-17, bịt ngày 10-10-2026.
 *
 * ── VÌ SAO CÓ CỔNG NÀY ──
 * Kho này có 113 cổng khác, và TẤT CẢ đều là logic thuần: không cổng nào dựng một
 * component. Hai lần một `ReferenceError` đi lọt qua cả hàng rào ấy và lên tới bản
 * thật, mỗi lần cho ra một trang TRẮNG HOÀN TOÀN:
 *   · hook đặt sau một `return` sớm (React lỗi 310);
 *   · biến dùng trước khi khai (TDZ) ở Phòng luyện nói.
 * Và chỉ trong hôm nay tôi suýt thêm hai lần nữa — một lần đọc `daPhuDao` từ sai
 * component, một lần quên `import { duocVuotAi }`. Cả bốn lần: `npm run build`
 * xanh, mọi cổng xanh, bé thấy màn trắng.
 *
 * Lý do bản dựng không bắt được: Vite/esbuild KHÔNG phân giải tên biến. `daPhuDao`
 * không tồn tại trong phạm vi vẫn dịch ra JavaScript hợp lệ, và chỉ ném lúc CHẠY.
 * Muốn bắt thì phải CHẠY — tức phải dựng component ra thật.
 *
 * ── CÁCH LÀM, VÀ VÌ SAO KHÔNG ĐỔI BỘ CHẠY CỔNG ──
 * `npm test` gọi `node <tệp>` trần: không bộ dịch JSX, không DOM giả. Nên cổng này
 * TỰ gói mấy màn cần dựng bằng `esbuild` ra một tệp tạm rồi nhập vào. Không thêm
 * bộ nạp, không sửa `npm test`, và mọi cổng khác không đụng gì.
 *
 * ── ⚠ DỰNG Ở MÁY CHỦ KHÔNG PHẢI DỰNG Ở TRÌNH DUYỆT ──
 * `renderToString` chạy đúng MỘT lượt vẽ đầu, và KHÔNG chạy `useEffect`. Nên cổng
 * này bắt được: lỗi phạm vi · hook sai thứ tự · biến dùng trước khi khai · hàm gọi
 * trên `undefined` lúc vẽ đầu. Nó KHÔNG bắt được lỗi chỉ xảy ra trong hiệu ứng hay
 * sau một cú bấm. Ghi rõ ở đây để không ai tưởng màn xanh ở đây là màn chạy được.
 */

/* Mấy màn đáng dựng nhất: vào được bằng một vai trò, hoặc là lối ra duy nhất khi
   mọi thứ khác đã hỏng. Màn của BÉ cần nhiều dữ liệu giả hơn — xem phần cuối. */
const MAN = [
  { ten: 'BangNguong', duong: 'src/chung/components/BangNguong.jsx', props: { onExit() {}, onXemDeXuat() {} } },
  { ten: 'DuyetDeXuat', duong: 'src/chung/components/DuyetDeXuat.jsx', props: { onExit() {} } },
  { ten: 'LuoiDoLoi', duong: 'src/chung/components/LuoiDoLoi.jsx', props: { children: null } },
  { ten: 'KeSach', duong: 'src/chung/components/KeSach.jsx', props: { onChon() {}, dangKy: null } },
];

let thuMuc;
let goi;

test('gói mấy màn bằng esbuild', async () => {
  /* ⚠ GÓI PHẢI NẰM TRONG KHO, không nằm ở `/tmp`. Node phân giải `react` theo cây
     thư mục từ chỗ tệp nằm; gói ở `/tmp` thì không thấy `web/node_modules` và cổng
     đỏ vì một lý do chẳng liên quan gì tới mấy màn. */
  const cache = new URL('../node_modules/.cache/', import.meta.url).pathname;
  mkdirSync(cache, { recursive: true });
  thuMuc = mkdtempSync(join(cache, 'man-'));
  const vao = join(thuMuc, 'vao.jsx');
  writeFileSync(vao, MAN.map(({ ten, duong }) => {
    const tuyet = new URL(`../${duong}`, import.meta.url).pathname;
    return `export { default as ${ten} } from ${JSON.stringify(tuyet)};`;
  }).join('\n'));

  const ra = join(thuMuc, 'goi.mjs');
  await build({
    entryPoints: [vao],
    outfile: ra,
    bundle: true,
    format: 'esm',
    platform: 'node',
    jsx: 'automatic',
    loader: { '.js': 'jsx', '.css': 'empty', '.png': 'empty', '.svg': 'empty', '.json': 'json' },
    /* React và react-dom để NGOÀI gói: cổng này phải dựng bằng ĐÚNG bản React mà
       nó nhập ở đầu tệp, nếu không hai bản React cùng chạy và hook nào cũng ném. */
    external: ['react', 'react-dom', 'react/jsx-runtime', 'firebase', 'firebase/*'],
    logLevel: 'silent',
  });
  goi = await import(pathToFileURL(ra).href);
  for (const { ten } of MAN) assert.equal(typeof goi[ten], 'function', `không gói được ${ten}`);
});

for (const { ten, props } of MAN) {
  test(`dựng được màn ${ten}`, () => {
    let html;
    const im = console.error;
    console.error = () => {};          // React cảnh báo nhiều thứ không liên quan
    try {
      html = renderToString(React.createElement(goi[ten], props));
    } finally {
      console.error = im;
    }
    assert.ok(typeof html === 'string', `${ten} không trả ra HTML`);
    assert.ok(!/undefinedundefined|\[object Object\]/.test(html),
      `${ten} in ra giá trị thô vào giao diện`);
  });
}

test('⚠ CỔNG NÀY BẮT ĐƯỢC ĐÚNG LỚP LỖI ĐÃ LỌT — thử ngược lại', () => {
  /* Đảo chiều thử: dựng một component mang đúng lỗi đã hai lần lên bản thật, và
     khẳng định cổng ĐỎ. Không có phép này thì cổng có thể đang xanh vì nó không
     canh gì cả — kho này đã dính chuyện ấy nhiều lần.
     ⚠ Phải lấy biến từ một phạm vi KHÁC, giống y ca thật (`daPhuDao` sống trong
     `LuyenTap` mà bị đọc từ `BaiHoc`). */
  const Vo = () => {
    // eslint-disable-next-line no-undef
    const x = bienKhongHeTonTai.current;
    return React.createElement('p', null, String(x));
  };
  const im = console.error;
  console.error = () => {};
  let nem = null;
  try { renderToString(React.createElement(Vo)); } catch (e) { nem = e; } finally { console.error = im; }
  assert.ok(nem instanceof ReferenceError,
    'cổng KHÔNG bắt được lỗi phạm vi — nó đang canh một thứ khác');
});

test('⚠ GIỚI HẠN ĐÃ BIẾT: dựng ở máy chủ KHÔNG bắt được hook sau `return` sớm', () => {
  /* Phép này khẳng định một điều KHÔNG LÀM ĐƯỢC, và nó ở đây vì điều ấy dễ bị đọc
     nhầm: thấy «cổng dựng màn» xanh là tưởng mọi lỗi React đã có người canh.

     React lỗi 310 (số hook đổi giữa hai lượt vẽ) chỉ lộ khi có LƯỢT VẼ THỨ HAI, mà
     `renderToString` chạy đúng một lượt và không chạy `useEffect`. Muốn bắt lớp lỗi
     ấy thì phải dựng ở trình duyệt hoặc thêm DOM giả — chưa làm.

     Nếu một ngày phép này ĐỎ thì nghĩa là React đã đổi hành vi: lúc ấy sửa chú
     thích và nâng cấp cổng, đừng sửa phép cho xanh. */
  const im = console.error;
  console.error = () => {};
  let nem = null;
  try {
    /* eslint-disable react-hooks/rules-of-hooks -- component này CỐ TÌNH sai,
       nó là vật chứng của phép thử. */
    const Sai = ({ som }) => {
      if (som) return null;                     // return sớm
      const [x] = React.useState(1);            // hook sau return → React 310 ở máy con
      return React.createElement('p', null, x);
    };
    renderToString(React.createElement(() => {
      const [n, dat] = React.useState(0);
      React.useEffect(() => dat(1), []);        // effect KHÔNG chạy khi dựng ở máy chủ
      return React.createElement(Sai, { som: n === 0 });
    }));
    /* eslint-enable react-hooks/rules-of-hooks */
  } catch (e) { nem = e; } finally { console.error = im; }
  assert.equal(nem, null,
    'React nay ném cả khi dựng ở máy chủ — nâng cấp cổng này thay vì sửa phép cho xanh');
});

test.after(() => { if (thuMuc) rmSync(thuMuc, { recursive: true, force: true }); });
