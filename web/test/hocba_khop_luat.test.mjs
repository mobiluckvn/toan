/**
 * CỔNG · CHỖ GHI HỌC BẠ PHẢI KHỚP VỚI LUẬT FIRESTORE.
 *
 * ── VÌ SAO CẦN THÊM MỘT CỔNG NỮA ──
 * `luat_firestore.test.mjs` đã thử luật rồi, và thử rất kỹ. Nhưng nó tự dựng gói
 * mang đi thử:
 *
 *     const mucHopLe = { loai: V.s('chuong'), … };   ← cổng tự viết
 *
 * Còn màn hình thì gửi `loai: 'ontap'`. Cổng thử đúng cái luật CHO PHÉP, chứ không
 * phải cái app GỬI ĐI — nên nó xanh suốt trong khi trên bản thật mọi kỳ ôn tập
 * Tiếng Anh đều bị máy chủ từ chối, im lặng, hàng tháng trời.
 *
 * Đây là dạng lỗi ở CHỖ NỐI: hai bên đều đúng khi nhìn riêng, chỉ chỗ gặp nhau là
 * hỏng, mà chỗ gặp nhau thì không tệp nào sở hữu. Cùng họ với "vỏ app quên truyền
 * hồ sơ con xuống môn" — cũng không cổng nào bắt được vì lý do y hệt.
 *
 * Nên cổng này không thử luật, cũng không thử app. Nó đọc CẢ HAI BÊN rồi so:
 *
 *   1. mọi `loai` màn hình gửi phải nằm trong danh sách `firestore.rules` cho phép;
 *   2. mọi gói phải bọc trong `giaTri` — vì bên đọc chỉ nhặt `v.giaTri`;
 *   3. bên đọc phải lọc đúng những `loai` mà luật cho ghi, không thừa không thiếu.
 *
 * ⚠ Đọc MÃ, không đọc lời ghi chú. Đã dính hai lần: cổng đếm cả chữ trong comment
 * rồi báo xanh. Nên phải bóc chú thích trước khi soi.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');

/** Bóc chú thích khối và chú thích dòng — giữ nguyên độ dài không cần, chỉ cần MÃ. */
const chiMa = (s) => s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');

const LUAT = chiMa(doc('../firestore.rules'));

/**
 * Danh sách `loai` mà luật cho ghi vào một collection học bạ.
 * Đọc thẳng từ `firestore.rules` chứ không chép sang đây — chép là sớm muộn lệch,
 * mà lệch ở đúng chỗ này thì lại im lặng.
 */
function loaiChoPhep(ten) {
  const i = LUAT.indexOf(`match /${ten}/{userId}/muc/{mucId}`);
  assert.notEqual(i, -1, `firestore.rules không có khối cho ${ten}`);
  /* ⚠ Tên luật đổi được: khối Tiếng Anh từ V5 dùng `allow create, delete` (và một
     `allow update` riêng cho việc bố mẹ xác nhận điểm) thay vì một `allow write`
     gộp. Tìm theo tên luật cụ thể là cổng đỏ vì hình dạng rules đổi, dù tính chất
     — "rules CHỐT một danh sách loai, và màn hình với bên đọc phải khớp" — không
     đổi. Nên tìm chính DANH SÁCH, trong khối `match` ấy. */
  const het = LUAT.indexOf('match /', i + 10);
  const khoi = LUAT.slice(i, het === -1 ? undefined : het);
  const m = khoi.match(/data\.loai in \[([^\]]+)\]/);
  assert.ok(m, `khối ${ten} không chốt danh sách loai — ai cũng ghi được hình dạng lạ`);
  return m[1].split(',').map((s) => s.trim().replace(/^'|'$/g, ''));
}

/** Mọi lệnh gọi `luuMucHocBa(...)` trong một tệp, kèm `loai` và gói dữ liệu. */
function noiGhi(nguon) {
  const ma = chiMa(nguon);
  const ra = [];
  const re = /luuMucHocBa\(\s*[^,]+,\s*'([^']+)'\s*,/g;
  let m;
  while ((m = re.exec(ma)) !== null) {
    /* Lấy phần còn lại của lệnh gọi để soi gói — đủ dùng vì gói luôn nằm sau khoá. */
    ra.push({ loai: m[1], sau: ma.slice(m.index, m.index + 320) });
  }
  return ra;
}

const MAN = {
  tienganh: { man: '../src/mon/tienganh/components/ManTiengAnh.jsx', kho: 'hocBaTA' },
  toan: { man: '../src/mon/toan/components/ManToan.jsx', kho: 'hocBa' },
};

for (const [mon, { man, kho }] of Object.entries(MAN)) {
  test(`[${mon}] mọi loai màn hình GỬI đều nằm trong danh sách luật CHO`, () => {
    const cho = loaiChoPhep(kho);
    const goi = noiGhi(doc(man));
    assert.ok(goi.length > 0, `${man} không gọi luuMucHocBa — học bạ không bao giờ có gì`);
    for (const g of goi) {
      assert.ok(cho.includes(g.loai),
        `màn hình gửi loai '${g.loai}' mà ${kho} chỉ cho [${cho}] — máy chủ TỪ CHỐI, im lặng`);
    }
  });

  test(`[${mon}] gói học bạ phải bọc trong giaTri — bên đọc chỉ nhặt v.giaTri`, () => {
    for (const g of noiGhi(doc(man))) {
      assert.match(g.sau, /giaTri\s*:/,
        `gọi luuMucHocBa loai '${g.loai}' mà không bọc giaTri — ghi lên rồi đọc ra rỗng`);
    }
  });
}

test('bên ĐỌC lọc đúng những loai mà luật cho GHI', () => {
  /* Luật cho ghi một loại mà bên đọc không nhặt thì tài liệu nằm đó vĩnh viễn,
     không ai thấy — đúng cái đã xảy ra, chỉ khác chiều. */
  const cap = [
    ['hocBaTA', '../src/mon/tienganh/lib/duLieu.js'],
    ['hocBa', '../src/mon/toan/lib/duLieu.js'],
  ];
  for (const [kho, tep] of cap) {
    const ma = chiMa(doc(tep));
    for (const loai of loaiChoPhep(kho)) {
      assert.ok(ma.includes(`'${loai}'`),
        `${kho} cho ghi loai '${loai}' mà ${tep} không đọc — ghi lên rồi bỏ đó`);
    }
  }
});

test('bên đọc KHÔNG đỡ bằng cả tài liệu khi thiếu giaTri', () => {
  /* `v.giaTri || v` là cái đỡ đã CHE MẤT lỗi: bên ghi gửi sai hình dạng mà đọc ra
     vẫn có gì đó, chỉ thiếu `best` — thẻ huy hiệu hiện "undefined/undefined" và
     không ai nghĩ là lỗi ghi. Chỉ nhận đúng một hình dạng. */
  for (const tep of ['../src/mon/tienganh/lib/duLieu.js', '../src/mon/toan/lib/duLieu.js']) {
    assert.doesNotMatch(chiMa(doc(tep)), /v\.giaTri\s*\|\|\s*v\b/,
      `${tep}: đỡ bằng cả tài liệu thì hình dạng sai không bao giờ lộ`);
  }
});

test('chính cổng này soi MÃ, không soi lời ghi chú', () => {
  /* Bẫy đã sập hai lần trong kho này. Thử ngược: một tệp giả chỉ có chú thích. */
  const gia = "/* luuMucHocBa(uid, 'loai_bia', k, {}) */\n// luuMucHocBa(uid, 'nua', k, {})\n";
  assert.equal(noiGhi(gia).length, 0, 'cổng đang đếm cả chữ trong chú thích');
});
