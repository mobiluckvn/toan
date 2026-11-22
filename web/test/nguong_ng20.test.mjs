/**
 * CỔNG · NG20 — "số câu hỏi tối thiểu mỗi nút" (Bảng 4.7, điểm 6).
 *
 * Trước 22-11 NG20 có trong bảng ngưỡng, có ô trên màn chuyên gia, mà KHÔNG CHỖ NÀO
 * ĐỌC. Cổng này vừa là chỗ đọc thứ nhất (soát kho nội dung thật, in danh sách nút
 * thiếu câu), vừa canh chỗ đọc thứ hai (bài phụ đạo mang cờ `thieuCau`).
 *
 * ⚠ CỔNG NÀY CẢNH BÁO, KHÔNG CHẶN. Kho hiện có nút dưới NG20 — đó là sự thật về học
 *   liệu (bảng đối chiếu v4 đếm được 32), không phải lỗi mã. Chặn ở đây là bắt người
 *   sửa mã phải đi soạn câu mới được cho cổng xanh. Nên cổng in danh sách ra, và chỉ
 *   ĐỎ khi chính phép đếm sai (lệch với phép đếm độc lập ngay dưới) hoặc khi NG20
 *   thôi không được đọc.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

import * as con from '../src/chung/lib/nguong.js';
import { nutThieuCau, demCauTheoNut, canhBaoThieuCau } from '../src/mon/tienganh/lib/soatCau.js';
import { dungPhuDao } from '../src/mon/tienganh/lib/phudao.js';

const GOC = new URL('../public/content', import.meta.url).pathname;
const DT = JSON.parse(readFileSync(join(GOC, 'tienganh/do_thi.json'), 'utf8'));
const TEP = [];
for (const t of readdirSync(GOC)) {
  const d = join(GOC, t);
  if (!statSync(d).isDirectory() || !/^ta\d$/.test(t)) continue;
  for (const f of readdirSync(d)) {
    if (!f.endsWith('.json')) continue;
    try { TEP.push(JSON.parse(readFileSync(join(d, f), 'utf8'))); } catch { /* tệp hỏng: cổng khác lo */ }
  }
}

/** Phép đếm ĐỘC LẬP — chép đúng luật của `tools/doi_chieu_v4.py`, để soi `soatCau.js`. */
function demDocLap(nguong) {
  const theo = {};
  const hang = [...TEP];
  while (hang.length) {
    const y = hang.pop();
    if (Array.isArray(y)) { hang.push(...y); continue; }
    if (!y || typeof y !== 'object') continue;
    if (y.id && (y.format || y.answerKey)) {
      for (const m of (y.maNutDs?.length ? y.maNutDs : (y.maNut ? [y.maNut] : []))) theo[m] = (theo[m] || 0) + 1;
    }
    for (const v of Object.values(y)) if (v && typeof v === 'object') hang.push(v);
  }
  return Object.entries(theo).filter(([m, n]) => DT.nut[m] && !m.startsWith('ph_') && n < nguong).length;
}

test('kho nội dung có mặt để soát', () => {
  assert.ok(TEP.length > 50, `chỉ thấy ${TEP.length} tệp bài`);
  assert.ok(demCauTheoNut(TEP).size > 500);
});

test('soát kho: danh sách nút dưới NG20 khớp phép đếm độc lập — và IN RA', () => {
  const ng20 = con.layNguong(con.boNguong(), 'NG20');
  const ds = nutThieuCau(DT, TEP);
  assert.equal(ds.length, demDocLap(ng20), 'soatCau.js đếm lệch luật của bảng đối chiếu');
  for (const x of ds) assert.ok(x.co < x.can && x.can === ng20);
  /* CẢNH BÁO — không chặn. Xem đầu tệp. */
  console.log(`   ⚠ NG20 = ${ng20}: ${ds.length} nút có ít hơn ${ng20} câu`
    + `${ds.length ? ` — ${ds.slice(0, 8).map((x) => `${x.ma} (${x.co})`).join(', ')}${ds.length > 8 ? ', …' : ''}` : ''}`);
});

test('NG20 thật sự ĐƯỢC ĐỌC: đổi bộ ngưỡng là đổi danh sách', () => {
  const mac = nutThieuCau(DT, TEP).length;
  con.datBoNguong({ macDinh: { ...con.MAC_DINH, NG20: 10 } });
  let cao;
  try { cao = nutThieuCau(DT, TEP).length; } finally { con.datBoNguong(con.BO_MAC_DINH); }
  con.datBoNguong({ macDinh: { ...con.MAC_DINH, NG20: 3 } });
  let thap;
  try { thap = nutThieuCau(DT, TEP).length; } finally { con.datBoNguong(con.BO_MAC_DINH); }
  assert.ok(cao > mac, `NG20 = 10 phải ra nhiều nút thiếu hơn NG20 = 4 (${cao} ≤ ${mac})`);
  assert.ok(thap <= mac);
  assert.equal(cao, demDocLap(10));
});

test('NG20 theo NÚT: chuyên gia khai riêng cho một nút thì chỉ nút ấy đổi', () => {
  const ds = nutThieuCau(DT, TEP);
  assert.ok(ds.length, 'cần ít nhất một nút thiếu câu để thử');
  const x = ds[0];
  /* Hạ NG20 của RIÊNG nút ấy xuống đúng số câu nó có → nó thôi bị cảnh báo. */
  con.datBoNguong({ macDinh: con.MAC_DINH, theoPhamVi: { nut: { [x.ma]: { NG20: x.co } } } });
  try {
    const sau = nutThieuCau(DT, TEP);
    assert.equal(sau.some((y) => y.ma === x.ma), false);
    assert.equal(sau.length, ds.length - 1, 'các nút khác giữ nguyên NG20 toàn hệ');
  } finally { con.datBoNguong(con.BO_MAC_DINH); }
});

test('bài phụ đạo dựng trên kho dưới NG20 thì mang cờ `thieuCau`', async () => {
  const bai = (n) => ({ id: 'b', practice: { pools: { warmup: Array.from({ length: n }, (_, i) => ({ id: `c${i}`, maNut: 'a', format: 'chon' })) } } });
  const dt = { nut: { a: { t: 'vocabulary' } }, canh: [] };
  const mong = await dungPhuDao({ dt, mucThao: {}, maNutMac: 'a', baiDs: [bai(2)] });
  assert.deepEqual(mong.thieuCau, { ma: 'a', co: 2, can: 4 });
  const day = await dungPhuDao({ dt, mucThao: {}, maNutMac: 'a', baiDs: [bai(6)] });
  assert.equal(day.thieuCau, null);
  assert.equal(canhBaoThieuCau([bai(4)], 'a'), null, 'đủ đúng NG20 thì không cảnh báo');
});

test('danh mục ngưỡng không còn ghi NG20 là "chưa có trong mã"', () => {
  const goc = JSON.parse(readFileSync(new URL('../../data/nguong.json', import.meta.url), 'utf8'));
  const x = goc.nguong.find((y) => y.ma === 'NG20');
  assert.doesNotMatch(x.oDau, /CHƯA CÓ TRONG MÃ/);
  assert.match(x.oDau, /soatCau\.js/);
});
