import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { congHuong, hoSoCongHuong, nguongTran } from '../src/mon/tienganh/lib/lantruyen.js';
import { viecTiepCuaNut, VIEC } from '../src/mon/tienganh/lib/chinhsach.js';
import { duocHoan } from '../src/mon/tienganh/lib/onlai.js';
import { nguongThao } from '../src/mon/tienganh/lib/zpd.js';
import { dungBang } from '../src/mon/tienganh/lib/bangtrangthai.js';

/**
 * LAN TRUYỀN XUÔI — nối vào tầng thích ứng, 10-10-2026.
 *
 * Bảng 3.25 của luận văn khai đây là một giới hạn: «Lan truyền xuôi đã viết nhưng
 * chưa nối vào tầng thích ứng lúc chạy», và hướng xử lý nó tự đặt ra là «nối vào
 * chỗ tính vectơ trạng thái, KHÔNG ghi đè hồ sơ».
 *
 * ⚠ CẢ KHỐI CỔNG NÀY CANH VẾ SAU. Vế đầu chỉ là một lời gọi hàm; vế sau mới là chỗ
 * hỏng được, và hỏng thì hỏng theo kiểu tệ nhất: hồ sơ phồng lên vì một SUY LUẬN,
 * con số phồng ấy đi vào BKT ở lượt sau, rồi phồng tiếp. Tuyên thạo khống không ai
 * lần ra được.
 */

/* Đồ thị nhỏ: a → b → c (a là gốc, c dựng trên b, b dựng trên a). */
const DT = {
  nut: { a: { t: 'vocabulary' }, b: { t: 'grammar' }, c: { t: 'grammar' } },
  canh: [
    { can: 'a', truoc_khi: 'b', loai: 'ban_do' },
    { can: 'b', truoc_khi: 'c', loai: 'ban_do' },
  ],
};
const ho = (p) => Object.fromEntries(Object.entries(p).map(([k, v]) => [k, { p: v }]));

test('bé thạo nút gốc thì nút dựng trên nó NHÍCH lên', () => {
  const r = congHuong(DT, ho({ a: 0.95, b: 0.30, c: 0.20 }));
  assert.ok(r.b > 0.30, `b không nhích: ${r.b}`);
  assert.ok(r.c > 0.20, `c không nhích: ${r.c}`);
  assert.ok(r.b > r.c, 'nút gần nguồn phải nhích nhiều hơn nút xa');
});

test('KHÔNG lan từ nút bé CHƯA thạo', () => {
  /* Lan từ một nút bé mới làm được nửa vời là nhân cái nửa vời ấy ra cả nhánh. */
  assert.deepEqual(congHuong(DT, ho({ a: 0.50, b: 0.30 })), {});
});

test('⚠ CỘNG HƯỞNG KHÔNG BAO GIỜ CHẠM NGƯỠNG THẠO', () => {
  /* Đây là chốt chống tuyên thạo khống, và nó phải đúng kể cả khi nút đích đã sát
     ngưỡng sẵn. Vỡ chốt này thì một nút bé CHƯA TỪNG làm đúng có thể được công
     nhận tinh thông nhờ suy luận. */
  const sat = nguongThao() - 0.001;
  const r = congHuong(DT, ho({ a: 0.99, b: sat, c: sat }));
  for (const [ma, p] of Object.entries(r)) {
    assert.ok(p < nguongThao(), `${ma} chạm ngưỡng thạo: ${p}`);
    assert.ok(p <= nguongTran() + 1e-9, `${ma} vượt trần cộng hưởng: ${p}`);
  }
});

test('nút chỉ nhờ cộng hưởng KHÔNG thể ra `vuotAi`, và KHÔNG thể hoãn thẻ ôn', () => {
  /* Hai hậu quả cụ thể nếu chốt trần vỡ: hàm chính sách cho bé bay qua một nút bé
     chưa từng làm, và thẻ ôn của cả bài bị hoãn vì một suy luận. */
  const suyRa = hoSoCongHuong(DT, ho({ a: 0.99, b: 0.80, c: 0.80 }));
  for (const ma of ['b', 'c']) {
    assert.equal(viecTiepCuaNut({ p: suyRa[ma].p }).viec !== VIEC.vuotAi, true,
      `${ma} ra vuotAi chỉ nhờ cộng hưởng`);
  }
  assert.equal(duocHoan({ maNutDs: ['a', 'b', 'c'] }, suyRa), false,
    'thẻ ôn bị hoãn vì một suy luận chứ không phải vì bé đã vững');
});

test('hồ sơ GỐC không bị sửa, và con số suy ra được ĐÁNH DẤU', () => {
  const goc = ho({ a: 0.95, b: 0.30 });
  const truoc = JSON.stringify(goc);
  const suyRa = hoSoCongHuong(DT, goc);
  assert.equal(JSON.stringify(goc), truoc, 'hàm đã sửa hồ sơ gốc');
  assert.notEqual(suyRa, goc, 'phải là bản sao');
  assert.equal(suyRa.b.suyRa, true, 'con số suy ra phải tự khai là suy ra');
  assert.equal(suyRa.a.suyRa, undefined, 'con số ĐO ĐƯỢC không được gắn nhãn suy ra');
});

test('mọi trường khác của hồ sơ nút được giữ nguyên', () => {
  /* Mất `saiLienTiep` là mất tín hiệu bật phụ đạo; mất `lastSeen` là phép quên
     tính theo một mốc bịa ra. */
  const goc = { b: { p: 0.30, saiLienTiep: 2, lastSeen: 12345, nAttempts: 7 } };
  goc.a = { p: 0.95 };
  const suyRa = hoSoCongHuong(DT, goc);
  assert.equal(suyRa.b.saiLienTiep, 2);
  assert.equal(suyRa.b.lastSeen, 12345);
  assert.equal(suyRa.b.nAttempts, 7);
  assert.ok(suyRa.b.p > 0.30);
});

test('thiếu đồ thị hay thiếu hồ sơ thì trả nguyên — không ném, không bịa', () => {
  assert.equal(hoSoCongHuong(null, ho({ a: 0.9 })).a.p, 0.9);
  assert.equal(hoSoCongHuong(DT, null), null);
  const khongDoi = ho({ a: 0.2 });
  assert.equal(hoSoCongHuong(DT, khongDoi), khongDoi, 'không có gì đổi thì trả CHÍNH hồ sơ cũ');
});

test('⚠ BẢNG TRẠNG THÁI: `mucThao` TRẢ RA vẫn là con số ĐO ĐƯỢC', () => {
  /* Đây là chốt quan trọng nhất của cả khối. `dungBang` trả `mucThao` cho mọi chỗ
     dùng tiếp — nếu nó trả bản đã cộng hưởng thì con số suy ra đi thẳng vào chấm
     thạo, bật phụ đạo, hoãn thẻ ôn và học bạ. */
  const goc = ho({ a: 0.95, b: 0.30, c: 0.20 });
  const bang = dungBang({ mucThao: goc, doThi: DT, bai: null });
  assert.equal(bang.mucThao.b.p, 0.30, 'mucThao trả ra đã bị cộng hưởng đắp lên');
  assert.equal(bang.mucThao.b.suyRa, undefined);
});

test('lan truyền xuôi THỰC SỰ được nối — không chỉ có hàm và cổng', () => {
  /* Trước 10-10 `congHuong` chỉ có cổng và tools gọi, tức với người học là chưa tồn
     tại. Cổng này ghim chỗ nối, vì một hàm không ai gọi thì sớm muộn có người dọn
     đi mà tưởng là mã chết. */
  const src = readFileSync(new URL('../src/mon/tienganh/lib/bangtrangthai.js', import.meta.url), 'utf8');
  assert.match(src, /hoSoCongHuong\(/, 'bangtrangthai.js phải gọi hoSoCongHuong');
  assert.match(src, /vectorS\(\{\s*mucThao:\s*mucThaoSuyRa/,
    'vectơ trạng thái phải dùng bản ĐÃ cộng hưởng');
});
