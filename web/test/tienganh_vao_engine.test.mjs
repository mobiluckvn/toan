/**
 * CỔNG · MỌI HOẠT ĐỘNG PHẢI VÀO ĐƯỢC ENGINE (lỗ thủng P1 · P2, 23-08-2026)
 *
 * Đi thử bản chạy thật bằng tài khoản OTP ngày 23-08 tìm ra hai lỗ:
 *
 *  P1 · BA TRONG BỐN HOẠT ĐỘNG KHÔNG VÀO BKT. Đọc hiểu · Viết · Ôn tập đều không
 *       phát `onLuot`, nên không sinh `attempts`, nên P(L) không đổi và Góc bố mẹ
 *       trống trơn dù bé vừa làm xong ba việc. Và 176/176 câu đọc hiểu KHÔNG mang
 *       `maNut` — có phát cũng không biết ghi công cho nút nào.
 *
 *  P2 · CHẶNG TỪ MỚI ĐÒI MICRO, KHÔNG CÓ ĐƯỜNG VÒNG. `micHong` chỉ bật khi micro
 *       hỏng THẬT, nên bé KHÔNG CÓ micro thì đứng luôn ở chặng 1, ba chặng sau
 *       khoá theo, và không bao giờ sinh nổi một bản ghi BKT nào.
 *
 * ── VÌ SAO CỔNG NÀY SOI CẢ HAI TẦNG ──
 * Dữ liệu đủ mà màn không phát thì vô ích; màn phát mà dữ liệu không có mã nút thì
 * cũng vô ích. Hai tầng phải cùng đúng mới có một lượt vào được engine — nên soi
 * một tầng là canh nửa vời. Cùng bài học với 62 câu sát hạch hồi Đợt 1.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];
const jsonCua = (p) => { try { return JSON.parse(doc(p)); } catch { return null; } };

/* ── TẦNG DỮ LIỆU ─────────────────────────────────────────────────────────── */

test('MỌI câu đọc hiểu đều mang mã nút tri thức', () => {
  const xau = [];
  let tong = 0;
  for (const q of QUYEN) {
    for (const b of jsonCua(`../public/content/${q}/dochieu.json`) || []) {
      for (const c of b.cau || []) {
        tong += 1;
        if (!c.maNut) xau.push(`${b.id}/${c.id}: “${String(c.text).slice(0, 40)}”`);
      }
    }
  }
  assert.ok(tong > 150, `chỉ đếm được ${tong} câu đọc hiểu — nạp hụt dữ liệu?`);
  assert.deepEqual(xau.slice(0, 8), [],
    `${xau.length}/${tong} câu đọc hiểu KHÔNG có maNut — bé làm xong mà không nút `
    + 'nào được ghi công');
});

test('MỌI bài viết đều mang mã nút tri thức', () => {
  const xau = [];
  let tong = 0;
  for (const q of QUYEN) {
    for (const b of jsonCua(`../public/content/${q}/vietbai.json`) || []) {
      tong += 1;
      if (!b.maNut) xau.push(b.id);
    }
  }
  assert.ok(tong > 60, `chỉ đếm được ${tong} bài viết`);
  assert.deepEqual(xau, [], `${xau.length}/${tong} bài viết không có maNut`);
});

test('mã nút của câu đọc hiểu là mã CÓ THẬT trong bản chuẩn', () => {
  /* Gán nhầm một chuỗi không có trong bản đồ thì hàm nền vẫn ghi, vẫn dựng ra một
     nút mới toanh trong `mastery/` — mức thạo của một nút không ai dạy. */
  const that = new Set();
  for (const l of [1, 2, 3, 4, 5]) {
    const cn = jsonCua(`../../data/tienganh/chuan_lop${l}.json`);
    for (const u of cn?.unit || []) for (const t of u.tu || []) if (t.ma) that.add(t.ma);
  }
  const xau = [];
  for (const q of QUYEN) {
    for (const b of jsonCua(`../public/content/${q}/dochieu.json`) || []) {
      for (const c of b.cau || []) {
        for (const m of c.maNutDs || (c.maNut ? [c.maNut] : [])) {
          if (!that.has(m)) xau.push(`${b.id}/${c.id}: ${m}`);
        }
      }
    }
  }
  assert.deepEqual(xau.slice(0, 6), [], `${xau.length} mã nút không có trong bản chuẩn`);
});

/* ── TẦNG MÀN HÌNH ────────────────────────────────────────────────────────── */

test('⚠ BỐN MÀN đều phát lượt lên engine', () => {
  for (const [tep, vi] of [
    ['DocHieu.jsx', 'bài đọc hiểu'],
    ['OnTap.jsx', 'kỳ ôn tập'],
    ['VietBai.jsx', 'bài viết'],
    ['CauNgheNhin.jsx', 'câu nghe-nhìn của kỳ sát hạch'],
  ]) {
    const ma = chiMa(doc(`../src/mon/tienganh/components/${tep}`));
    assert.match(ma, /onLuot/,
      `${tep} (${vi}) không phát \`onLuot\` — bé làm xong mà engine không biết gì`);
  }
});

test('⚠ CHỖ NỐI: ManTiengAnh phải truyền ghiLuot cho CẢ BỐN màn', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  for (const the of ['BaiHoc', 'DocHieu', 'VietBai', 'OnTap']) {
    const m = ma.match(new RegExp(`<${the}[\\s\\S]{0,1500}?/>`));
    assert.ok(m, `không tìm thấy chỗ dựng <${the}>`);
    assert.match(m[0], /onLuot=\{ghiLuot\}/,
      `<${the}> KHÔNG được truyền onLuot — màn có phát mà không ai nghe, đúng lỗ `
      + 'thủng P1');
  }
});

test('bài đọc hiểu ĐƯỢC ĐẨY LÊN MÁY CHỦ, không chỉ nằm ở máy', () => {
  /* Bác đổi chủ ý 23-08: phần đọc phải lên máy chủ như phần viết. */
  const ma = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  const m = ma.match(/const xongDocHieu[\s\S]{0,700}?\}, \[/);
  assert.ok(m, 'không tìm thấy xongDocHieu');
  assert.match(m[0], /luuMucHocBa\([^)]*'doc'/,
    'xongDocHieu không gọi luuMucHocBa với loai `doc` — kết quả đọc chỉ nằm ở máy');
  assert.match(doc('../firestore.rules'), /'doc'/,
    "firestore.rules chưa cho ghi loai 'doc' → Firestore từ chối TRONG IM LẶNG");
});

/* ── P2 · ĐƯỜNG LUI KHI KHÔNG CÓ MICRO ────────────────────────────────────── */

test('⚠ CHẶNG TỪ MỚI có đường lui TỰ KHAI, không bắt hỏng micro mới cho qua', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/BaiHoc.jsx'));
  /* Soi thứ VẼ RA: một nút bấm được, gọi thẳng `onMicHong`. Soi sự có mặt của chữ
     `micHong` thì vô nghĩa — chữ ấy vốn đã đầy trong tệp. */
  assert.match(ma, /onClick=\{onMicHong\}/,
    'không có nút nào để bé tự khai "chưa nói được" — bé không có micro thì đứng '
    + 'luôn ở chặng 1 và không bao giờ sinh được dữ liệu BKT (lỗ thủng P2)');
  /* Và nút ấy phải đứng SAU phần nghe: bỏ luôn cả nghe thì chặng này không dạy gì. */
  assert.match(ma, /daNgheTu && !micHong/,
    'đường lui phải chờ bé NGHE xong mới hiện — phần nghe là thứ chặng này dạy');
  /* ⚠ VÀ CHỖ GỌI PHẢI TRUYỀN CỜ ẤY XUỐNG.
     Bản đầu của cổng này chỉ soi bên trong `LuyenTu`, nên nó XANH trong khi chỗ
     dựng `<LuyenTu>` không truyền `daNgheTu` — cờ mặc định `false`, nút không bao
     giờ hiện, tính năng chết mà cổng vẫn xanh. Đúng họ lỗi CHỖ NỐI của P1: mỗi
     tệp một mình đều đúng. Bắt được khi đi thử bản chạy, không phải khi đọc mã. */
  const goi = ma.match(/<LuyenTu[\s\S]{0,600}?\/>/);
  assert.ok(goi, 'không tìm thấy chỗ dựng <LuyenTu>');
  assert.match(goi[0], /daNgheTu=\{/,
    'chỗ gọi <LuyenTu> không truyền `daNgheTu` — nút lui không bao giờ hiện');
});

test('micro hỏng thì ô việc vẫn tính là xong', async () => {
  /* Luật ở `dandat.js`, đã có từ trước — phép này giữ cho nó không bị gỡ, vì
     đường lui tự khai ở trên chỉ có nghĩa khi luật này còn. */
  const { viecChangTu } = await import('../src/mon/tienganh/lib/dandat.js');
  const dsTu = [{ tu: 'city' }, { tu: 'class' }];
  const chua = viecChangTu({ dsTu, daNghe: ['city', 'class'], micHong: false });
  const hong = viecChangTu({ dsTu, daNghe: ['city', 'class'], micHong: true });
  const xong = (r) => r.viec.filter((v) => v.loai === 'tu' && v.tt === 'xong').length;
  assert.equal(xong(chua), 0, 'chưa khai hỏng mà đã cho xong — mất phần nói');
  assert.equal(xong(hong), 2, 'khai micro hỏng rồi mà ô việc vẫn kẹt');
});

test('⚠ SỐ ĐO KHÔNG ĐƯỢC BỊA: bài viết để `ms` rỗng chứ không lấy giờ gọi máy chấm', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/VietBai.jsx'));
  const m = ma.match(/onLuot\?\.\(\{[\s\S]{0,400}?\}\);/);
  assert.ok(m, 'VietBai không phát onLuot');
  assert.match(m[0], /ms:\s*null/,
    'màn Viết không biết bé gõ bài trong bao lâu; điền một con số vào `ms` là bịa '
    + 'dữ liệu cho chiều Thời gian');
});
