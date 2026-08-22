/**
 * CỔNG · BẢNG TỪ MÀN VIẾT — ô chữ phải có nghĩa, VÀ nghĩa phải HIỆN RA.
 *
 * Bác bảo soi 105 ô chữ không có nghĩa tiếng Việt (22-08-2026). Soi xong thì thứ
 * đáng canh nhất hoá ra không phải con số ấy.
 *
 * ── LỖI 1 · nghĩa nằm trong tooltip, bé dùng máy tính bảng không bao giờ thấy ──
 * `VietBai.jsx` bày nghĩa bằng `title={v.nghia}`. Trên máy tính bảng và điện
 * thoại, tooltip không hiện. Nghĩa là **2167 ô ĐÃ CÓ nghĩa cũng vô hình y hệt**
 * ô không có — vá hết 105 chữ mà không sửa chỗ này thì bé không đọc thêm được
 * một chữ nghĩa nào.
 *
 * Cùng họ với 62 câu sát hạch hồi Đợt 1: dữ liệu ĐÚNG và đầy đủ, cổng nào cũng
 * xanh, chỗ hỏng nằm giữa dữ liệu và mắt đứa trẻ — không tệp nào sở hữu chỗ ấy.
 * Nên cổng này soi CẢ HAI đầu.
 *
 * ── LỖI 2 · cụm bị xé thành chữ lẻ ──
 * Kho từ vựng dạy nhiều CỤM ("break time" · "table tennis" · "set square"), mà
 * bảng nghĩa tra bằng nguyên văn khoá. Xé cụm ra thì chữ lẻ không khớp khoá nào →
 * ô trống nghĩa. Và tệ hơn: chữ lẻ ĐỔI NGHĨA khi rời cụm — "table tennis" là bóng
 * bàn, `tennis` một mình là quần vợt; "first floor" kiểu Anh là TẦNG HAI.
 *
 * Gạch nối cũng thế: `T-shirt` từng đẻ thêm hai ô rác (bài ta4 U18 hiện đủ cả ba
 * ô), `Mid-Autumn Festival` thành ba ô rời mà không có ô gạch nối nào để ghép.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];

const bang = (q) => {
  try { return JSON.parse(doc(`../public/content/${q}/vietbai.json`)); }
  catch { return []; }
};

/* Chữ nối — chép từ `KHONG_CHU` của `tools/sinh_bai_tranh.py`. Chú nghĩa từ điển
   cho chúng là dạy sai (`can` trong "I can see" không phải "cái lon"). */
const KHONG_CHU = new Set([
  'can', 'see', 'do', 'does', 'did', 'have', 'has', 'is', 'are', 'was', 'were',
  'am', 'be', 'will', 'would', 'like', 'there', 'that', "that's", "there's",
  'this', 'it', "it's", 'a', 'an', 'the', 'and', 'to', 'of', 's', 'left',
  'right', 'watch', 'play', "he's", "she's", "they're", "i'm", "i'd", "i'll",
  "we'll",
]);

/* Tên riêng thì KHÔNG cần nghĩa tiếng Việt. Khai đích danh, không đoán theo chữ
   hoa: "This"·"I" cũng viết hoa mà không phải tên ai. */
const TEN_RIENG = new Set(['Hoa', 'Dao', 'Hung', 'Tran', 'Viet', 'Mary', 'Nam']);

test('⚠ NGHĨA PHẢI HIỆN RA MÀN HÌNH, không trốn trong tooltip', () => {
  const ma = chiMa(doc('../src/mon/tienganh/components/VietBai.jsx'));
  assert.doesNotMatch(ma, /title=\{v\.nghia\}/,
    'nghĩa lại nằm trong `title` — máy tính bảng và điện thoại không hiện tooltip, '
    + 'bé mất sạch phần nghĩa dù dữ liệu vẫn đủ');
  /* Soi thứ VẼ RA, không soi sự có mặt của chữ `nghia`: `title={v.nghia}` cũng
     chứa chữ ấy. Phải là một nút văn bản thật trong cây JSX. */
  assert.match(ma, /\{v\.nghia\s*&&\s*\([\s\S]{0,200}\{v\.nghia\}<\/span>/,
    'không thấy chỗ nào VẼ `v.nghia` thành chữ trên màn hình');
});

test('mọi ô chữ đều có nghĩa, trừ chữ nối và tên riêng', () => {
  const xau = [];
  for (const q of QUYEN) {
    for (const b of bang(q)) {
      for (const o of b.vonTu || []) {
        if (o.nghia || KHONG_CHU.has(o.tu.toLowerCase()) || TEN_RIENG.has(o.tu)) continue;
        xau.push(`${b.id}: ô “${o.tu}” không có nghĩa`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} ô trống nghĩa:\n  ${xau.slice(0, 12).join('\n  ')}`);
});

test('⚠ CỤM DỄ ĐỔI NGHĨA KHÔNG ĐƯỢC XÉ', () => {
  /* ⚠ KHÔNG soi "mọi cụm đều không được có ô lẻ" — luật ấy SAI, và tôi đã viết
     nhầm nó một lần. Bài dạy "ride a bike" vẫn phải có ô `bike` riêng, vì bé còn
     cần viết "I can see a bike."; ô `a` và `the` thì bài nào cũng cần.

     Thứ đáng canh hẹp hơn nhiều: mấy cụm mà chữ lẻ ĐỔI NGHĨA khi rời cụm. Ở
     những bài ấy, bày ô lẻ ra là dạy sai — dù có chú nghĩa hay không.
         "table tennis" là BÓNG BÀN, `tennis` một mình là quần vợt;
         "set square"   là cái Ê-KE,  `set`    một mình là "bộ";
         "first floor"  kiểu Anh là TẦNG HAI;
         "break time"   là giờ ra chơi;
         "get up"       là thức dậy, khác hẳn `get` = đến (địa điểm). */
  const BAY = {
    'table tennis': 'tennis', 'set square': 'set', 'first floor': 'first',
    'break time': 'break', 'get up': 'get',
  };
  const xau = [];
  for (const q of QUYEN) {
    for (const b of bang(q)) {
      /* Bài phạm vi CHƯƠNG bày cả kho từ của chương: ở đó "hundred" và
         "one hundred and twenty-nine" đều là mục từ vựng THẬT, không phải mảnh
         vỡ. Chỉ soi bài tả tranh. */
      if (b.phamVi !== 'unit') continue;
      const o = new Set((b.vonTu || []).map((x) => x.tu.toLowerCase()));
      for (const [cum, manh] of Object.entries(BAY)) {
        if (o.has(cum) && o.has(manh)) {
          xau.push(`${b.id}: dạy cụm “${cum}” mà vẫn bày ô lẻ “${manh}”`);
        }
      }
    }
  }
  assert.deepEqual(xau, [], xau.join('\n  '));
});

test('⚠ GẠCH NỐI KHÔNG ĐƯỢC CẮT — bé không có ô gạch nối để ghép lại', () => {
  const ma = readFileSync(new URL('../../tools/sinh_bai_tranh.py', import.meta.url), 'utf8');
  assert.match(ma, /TACH_CHU = re\.compile\(r"\[A-Za-z\]\[A-Za-z'\\-\]\*"\)/,
    "bộ tách chữ lại bỏ gạch nối — `T-shirt` sẽ đẻ thêm hai ô rác `T` và `shirt`");

  const xau = [];
  for (const q of QUYEN) {
    for (const b of bang(q)) {
      if (b.phamVi !== 'unit') continue;
      const o = new Set((b.vonTu || []).map((x) => x.tu.toLowerCase()));
      for (const cum of (b.vonTu || []).map((x) => x.tu).filter((t) => t.includes('-'))) {
        for (const m of cum.toLowerCase().split('-')) {
          if (o.has(m)) xau.push(`${b.id}: “${cum}” còn ô rời “${m}”`);
        }
      }
    }
  }
  assert.deepEqual(xau, [], xau.join('\n  '));
});
