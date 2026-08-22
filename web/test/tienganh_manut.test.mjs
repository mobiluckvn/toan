/**
 * CỔNG · MỖI CÂU LUYỆN PHẢI CHỈ ĐÚNG MỘT NÚT CỦA ĐỒ THỊ TRI THỨC.
 *
 * ── VÌ SAO CẦN ──
 * `maNut` là thứ biến sổ của bé từ "xong bài B04" thành "vững từ `dolphin`, còn
 * yếu mẫu `sp_g5_u1_1`". Hàm nền BKT ghi `mastery/{uid}/units/{bktUnit}` và
 * `bktUnit` lấy thẳng từ đây. Nên sai ở tầng này thì mọi con số phía sau đều sai,
 * mà sai một cách KHÔNG AI THẤY: mastery vẫn có tài liệu, vẫn có số, chỉ là số ấy
 * nói về một nút không tồn tại hoặc về nhầm nút.
 *
 * ── BA THỨ CỔNG NÀY CANH, VÀ VÌ SAO ĐỦ BA ──
 *  1. KHÔNG SÓT. Câu không có `maNut` là câu bé làm mà không ai ghi công — im
 *     lặng, vì màn hình vẫn chấm đúng/sai bình thường.
 *  2. NÚT CÓ THẬT. Mã nút bịa ra thì BKT chấm vào hư không: tài liệu mastery mọc
 *     lên, không nối vào đồ thị, không lan truyền được, và không gì báo.
 *  3. ĐÚNG MỘT NÚT CHÍNH. `attempts` chỉ mang được một `bktUnit`. Nếu bộ sinh
 *     ghi hai nút cho một câu thì một lượt trả lời đúng được tính công hai lần và
 *     mức thạo phồng lên — đây là lỗi tôi sợ nhất trong cả Đợt 1, vì nó làm hệ
 *     thống LẠC QUAN về bé, tức là cho bé đi tiếp khi bé chưa vững.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';

const doc = (p) => JSON.parse(readFileSync(new URL(p, import.meta.url), 'utf8'));
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];

const baiCua = (q) => readdirSync(new URL(`../public/content/${q}/`, import.meta.url))
  .filter((f) => /^DL_TA\d_B\d+\.json$/.test(f))
  .map((f) => doc(`../public/content/${q}/${f}`));

const cauCua = (b) => [
  ...Object.values(b.practice?.pools || {}).flat(),
  ...(b.assessment?.items || []),
];

/* Mã nút hợp lệ — đọc từ CHÍNH bản đồ, không chép danh sách sang đây. */
const banDo = doc('../../data/ban_do_tieng_anh.json');
const NUT_BAN_DO = new Set(banDo.graph.nodes.map((n) => n.id));

/**
 * Nút CHÍNH được phép nằm ngoài bản đồ đúng một trường hợp: mẫu câu SOẠN THÊM.
 *
 * `sp_g3_starter_1` là mẫu tôi thêm cho unit Starter lớp 3 — sách không khai mẫu
 * nào nên bài mất hẳn bậc ráp câu. Nó có thật với bé (có bài, có câu luyện, có
 * tiếng đọc) nhưng không có nút trong `ban_do_tieng_anh.json`, vì kho gốc cấm
 * sửa. Danh sách này phải HẸP và phải liệt kê từng cái: mở rộng nó bằng một luật
 * chung (kiểu "cho qua mọi mã bắt đầu bằng sp_") là mất luôn phép canh số 2.
 */
const NGOAI_LE = new Set(['sp_g3_starter_1']);

test('mọi câu luyện và câu sát hạch đều có maNut', () => {
  for (const q of QUYEN) {
    for (const b of baiCua(q)) {
      for (const c of cauCua(b)) {
        assert.ok(c.maNut, `${b.id} câu ${c.id}: thiếu maNut — bé làm mà không ai ghi công`);
      }
    }
  }
});

test('maNut CHÍNH phải là nút thật, và chỉ là từ vựng hoặc mẫu câu', () => {
  for (const q of QUYEN) {
    for (const b of baiCua(q)) {
      for (const c of cauCua(b)) {
        assert.match(c.maNut, /^(v|sp)_/,
          `${b.id} câu ${c.id}: nút chính '${c.maNut}' không phải từ vựng (v_) hay mẫu câu (sp_). `
          + 'Cụm ghép (cum_) và từ soạn thêm (them_) chỉ được làm nút PHỤ — chúng không có '
          + 'chỗ trong đồ thị nên không lan truyền chẩn đoán được.');
        assert.ok(NUT_BAN_DO.has(c.maNut) || NGOAI_LE.has(c.maNut),
          `${b.id} câu ${c.id}: nút '${c.maNut}' không có trong bản đồ — BKT sẽ chấm vào hư không`);
      }
    }
  }
});

test('maNut CHÍNH phải nằm trong maNutDs, và ds không được rỗng', () => {
  for (const q of QUYEN) {
    for (const b of baiCua(q)) {
      for (const c of cauCua(b)) {
        assert.ok(Array.isArray(c.maNutDs) && c.maNutDs.length,
          `${b.id} câu ${c.id}: maNutDs rỗng`);
        assert.ok(c.maNutDs.includes(c.maNut),
          `${b.id} câu ${c.id}: nút chính '${c.maNut}' không có trong maNutDs`);
        assert.equal(new Set(c.maNutDs).size, c.maNutDs.length,
          `${b.id} câu ${c.id}: maNutDs có mã trùng`);
      }
    }
  }
});

test('nút CHÍNH khớp với thứ câu ấy thật sự kiểm', () => {
  /* Câu bậc RÁP CÂU kiểm cấu trúc, nên nút chính phải là MẪU CÂU. Câu nghe-nhìn
     và câu từ↔nghĩa kiểm vốn từ, nên nút chính phải là TỪ.

     Đây là phép canh chống lẫn hai trục. Lẫn thì không có gì đỏ — sổ vẫn đầy số —
     nhưng bé sai ngữ pháp lại bị ghi là yếu từ vựng, và bài phụ đạo sau này sẽ
     dạy nhầm hẳn thứ bé cần. */
  /* ⚠ DẤU HIỆU LÀ `answerKey.the`, KHÔNG PHẢI `format`. Bản đầu tôi viết
     `c.format === 'the'` — không câu nào khớp, phép canh chạy qua 0 câu và vẫn
     xanh. Chính phép "rap > 0" ở cuối bắt được. Giữ nó lại: mọi phép canh lọc dữ
     liệu đều phải chứng minh nó lọc ra được cái gì đó.

     Và phải bó trong bậc STANDARD. Cùng dạng xếp thẻ ấy ở bậc THỬ THÁCH lại là
     ghép CHỮ CÁI thành một từ (445 câu) — kiểm chính tả của TỪ, nên nút chính là
     `v_` mới đúng. Cùng một hình dạng dữ liệu, hai việc khác hẳn nhau. */
  let rapCau = 0, ghepChu = 0;
  for (const q of QUYEN) {
    for (const b of baiCua(q)) {
      for (const c of (b.practice?.pools?.standard || [])) {
        if (!(c.answerKey || {}).the) continue;
        rapCau += 1;
        assert.match(c.maNut, /^sp_/,
          `${b.id} câu ${c.id}: câu RÁP THÀNH CÂU mà nút chính là '${c.maNut}' — `
          + 'phải là mẫu câu, không phải từ vựng');
      }
      for (const c of (b.practice?.pools?.challenge || [])) {
        if (!(c.answerKey || {}).the) continue;
        ghepChu += 1;
        assert.match(c.maNut, /^v_/,
          `${b.id} câu ${c.id}: câu GHÉP CHỮ mà nút chính là '${c.maNut}' — `
          + 'ghép chữ kiểm chính tả một TỪ, nút chính phải là từ vựng');
      }
      for (const c of (b.practice?.pools?.warmup || [])) {
        assert.match(c.maNut, /^v_/,
          `${b.id} câu ${c.id}: câu khởi động kiểm vốn TỪ mà nút chính là '${c.maNut}'`);
      }
    }
  }
  assert.ok(rapCau > 0, 'không lọc ra câu ráp nào — phép canh đang tự chứng minh với chính nó');
  assert.ok(ghepChu > 0, 'không lọc ra câu ghép chữ nào — như trên');
});

test('đảo chiều: phép canh nút-có-thật thật sự bắt được mã bịa', () => {
  /* Cổng xanh mà không canh ai thì vô dụng. Thử ngược bằng dữ liệu giả. */
  assert.ok(!NUT_BAN_DO.has('v_g9_u1_khongcothat'));
  assert.ok(!NGOAI_LE.has('v_g9_u1_khongcothat'));
  assert.ok(NUT_BAN_DO.has('sp_g5_u1_1'), 'nút thật mà bảo không có — phép canh hỏng ngược');
});
