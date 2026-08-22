/**
 * CỔNG · HAI LỖI BÁC BẮT ĐƯỢC NGÀY 22-08-2026, TRÊN BẢN ĐANG CHẠY.
 *
 * Cả hai đều thuộc một họ: MÀN HÌNH VẪN ĐỦ CHỮ nên nhìn lướt không ra, và 84 cổng
 * lúc ấy đều xanh vì chúng soi dữ liệu, không soi thứ bé nhìn thấy.
 *
 *  1. Góc bố mẹ hiện `CHUONG%3A1%40G3` — một mã máy của MÔN TOÁN, lại còn mã hoá
 *     URL. Hai lỗi chồng nhau: `mastery/{uid}/units` dùng CHUNG với Toán mà ma
 *     trận không lọc theo môn, và khoá tài liệu là `encodeURIComponent(bktUnit)`
 *     mà không ai giải mã.
 *
 *  2. Mất nút "Nghe cô đọc" ở chặng Từ mới và Mẫu câu — tức mất phần NGHE TRƯỚC
 *     KHI NÓI, đúng thứ hai chặng ấy sinh ra để làm. Nguyên nhân: sổ âm nhớ vào
 *     MỘT biến chung cho mọi quyển, mà `BaiHoc` gọi `napSoAm()` không tham số
 *     (mặc định ta1). Hai lời gọi đua nhau, lời nào xong sau thì thắng.
 *     ⚠ Lỗi này có từ `0b65a94c`, không phải mới — nhưng là CUỘC ĐUA nên lúc lộ
 *     lúc không, tuỳ máy và tuỳ mạng. Đó là lý do 84 cổng không ai thấy.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { maTranTrangThai } from '../src/mon/tienganh/lib/lantruyen.js';
import { nhanNut } from '../src/mon/tienganh/lib/doThi.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
const DT = JSON.parse(doc('../public/content/tienganh/do_thi.json'));

/* ── LỖI 1 · mã môn Toán lọt vào Góc bố mẹ ────────────────────────────────── */

test('⚠ MÃ CỦA MÔN TOÁN KHÔNG ĐƯỢC LỌT VÀO MA TRẬN TIẾNG ANH', () => {
  /* `mastery/{uid}/units` dùng CHUNG với Toán — đó là chủ ý (xem `duLieu.js`),
     nên bên ĐỌC phải tự lọc. Không lọc thì `CHUONG:1@G3` hiện lên trong Góc bố mẹ
     của môn Tiếng Anh, đúng cái bác thấy. */
  const mucThao = {
    [encodeURIComponent('CHUONG:1@G3')]: { p: 0.2 },   // của Toán
    'UNIT:4@KSN2': { p: 0.1 },                          // cũng của Toán
    v_g5_u1_city: { p: 0.3 },                           // của Tiếng Anh
  };
  const r = maTranTrangThai(DT, mucThao);
  assert.deepEqual(r.map((x) => x.ma), ['v_g5_u1_city'],
    'mã của môn Toán lọt vào bảng của Tiếng Anh');
});

test('⚠ KHOÁ PHẢI ĐƯỢC GIẢI MÃ — không bày chuỗi %3A%40 cho bố mẹ đọc', () => {
  const ma = chiMa(doc('../src/mon/tienganh/lib/lantruyen.js'));
  assert.match(ma, /decodeURIComponent/,
    'tên tài liệu mastery là encodeURIComponent(bktUnit) — không giải mã thì bố mẹ '
    + 'đọc một chuỗi mã hoá URL');
});

test('⚠ BÀY NHÃN ĐỌC ĐƯỢC, KHÔNG BÀY MÃ MÁY', () => {
  /* `v_g5_u1_city` không nói gì với bố mẹ. Đồ thị nay mang theo một nhãn NGẮN. */
  assert.equal(nhanNut(DT, 'v_g5_u1_city'), 'city — thành phố');
  const co = Object.values(DT.nut).filter((n) => n.n).length;
  assert.ok(co > 800, `chỉ ${co} nút có nhãn — phần lớn bảng sẽ hiện mã máy`);

  const r = maTranTrangThai(DT, { v_g5_u1_city: { p: 0.3 } });
  assert.equal(r[0].nhan, 'city — thành phố', 'ma trận không trả nhãn ra');

  const man = chiMa(doc('../src/mon/tienganh/components/ManTiengAnh.jsx'));
  assert.match(man, /x\.nhan \|\| x\.ma/, 'màn hình vẫn bày mã máy làm chính');
});

/* ── LỖI 2 · mất nút nghe ở Từ mới và Mẫu câu ─────────────────────────────── */

test('⚠ SỔ ÂM PHẢI NHỚ THEO TỪNG QUYỂN', () => {
  /* Một biến chung cho mọi quyển thì bé học lớp 5 có thể nhận sổ âm lớp 1, và mọi
     mã clip tra ra null → `NutNghe` TỰ ẨN → mất phần nghe-trước-khi-nói. */
  const ma = chiMa(doc('../src/mon/tienganh/lib/noiDung.js'));
  assert.doesNotMatch(ma, /export async function napSoAm\(ma = 'ta1'\) \{\s*if \(soAm\) return soAm;/,
    'napSoAm vẫn nhớ vào MỘT biến chung — quyển nào nạp trước thì cả app dùng sổ ấy');
  assert.match(ma, /khoAm/, 'không có kho nhớ theo quyển');
  assert.match(ma, /dangNapAm/,
    'không chặn cuộc đua: hai lời gọi cùng lúc thì lời nào xong SAU sẽ thắng');
});

test('⚠ CHỖ GỌI PHẢI TRUYỀN QUYỂN, không gọi trần', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/BaiHoc.jsx'));
  assert.doesNotMatch(ma, /napSoAm\(\s*\)/,
    'gọi `napSoAm()` trần thì mặc định ta1 — bé lớp 3·4·5 mất hết nút nghe');
  assert.match(ma, /napSoAm\(quyenCua\(/, 'phải suy quyển từ mã bài');
});

test('nút NGHE TRƯỚC KHI NÓI vẫn còn ở cả hai chặng', () => {
  /* Đây là phép canh cho chính TÍNH NĂNG, không phải cho một dòng mã: chặng Từ
     mới và Mẫu câu phải còn ô nói, và ô nói phải còn nút nghe mẫu bên trong. */
  const bai = chiMa(doc('../src/mon/tienganh/components/BaiHoc.jsx'));
  const soNutNoi = (bai.match(/<NutNoi/g) || []).length;
  assert.ok(soNutNoi >= 2,
    `chỉ còn ${soNutNoi} ô nói — chặng Từ mới và Mẫu câu mỗi chặng phải có một`);

  const noi = chiMa(doc('../src/mon/tienganh/components/NutNoi.jsx'));
  assert.match(noi, /<NutNghe[^>]*ma=\{maAm\}/,
    'ô nói mất nút nghe mẫu — bé phải nói theo mà không được nghe trước');
});

test('mã clip của MỌI quyển đều có trong sổ âm của chính quyển ấy', async () => {
  /* Phép canh dữ liệu đi kèm: sổ đúng quyển rồi thì mã phải tra ra. */
  const { readdirSync } = await import('node:fs');
  const dk = JSON.parse(doc('../public/content/chuong_trinh.json'));
  for (const q of ['ta1', 'ta2', 'ta3', 'ta4', 'ta5']) {
    const so = JSON.parse(doc(`../public/content/${dk.chuongTrinh[q].am.so}`));
    const co = new Set((so.clip || []).map((c) => c.id));
    let thieu = 0;
    for (const f of readdirSync(new URL(`../public/content/${q}/`, import.meta.url))) {
      if (!/^DL_TA\d_B\d+\.json$/.test(f)) continue;
      const b = JSON.parse(doc(`../public/content/${q}/${f}`));
      for (const v of (b.knowledgeCore?.vocabulary || [])) {
        if (v.am && !co.has(v.am)) thieu += 1;
      }
    }
    assert.equal(thieu, 0, `${q}: ${thieu} từ có mã clip không nằm trong sổ âm`);
  }
});
