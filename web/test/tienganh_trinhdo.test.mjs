/**
 * Khối "TRÌNH ĐỘ HIỆN TẠI" của Sổ bố mẹ, môn Tiếng Anh.
 * Trước 22-11-2026 `hocBaTu` trả `trinhDo: null` → em xong 16/16 unit vẫn bị báo
 * "Con chưa học bài nào". Cổng này giữ cho hai con số trên cùng màn khớp nhau.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { hocBaQuyen, trinhDoTu } from '../src/mon/tienganh/lib/hocba.js';

const ta1 = { ma: 'ta1', ten: 'Tiếng Anh lớp 1', soChuong: 4, bai: ['DL:TA1.B01', 'DL:TA1.B02', 'DL:TA1.B03'] };
const ta2 = { ma: 'ta2', ten: 'Tiếng Anh lớp 2', soChuong: 4, bai: ['DL:TA2.B01', 'DL:TA2.B02'] };
const hb = (micros) => [ta1, ta2].map((ct) => hocBaQuyen({ micros }, ct));

test('chưa học gì thì trình độ rỗng, không bịa quyển', () => {
  const td = trinhDoTu(hb({}));
  assert.equal(td.quyen, null);
  assert.equal(td.tongBaiDat, 0);
});

test('xong cả quyển thì khối đầu đếm đúng số bài đã đạt', () => {
  const micros = Object.fromEntries(ta1.bai.map((id, i) => [id, { pass: true, at: 1000 + i }]));
  const td = trinhDoTu(hb(micros));
  assert.equal(td.tongBaiDat, 3);
  assert.equal(td.quyen.ma, 'ta1');
  assert.equal(td.quyen.datBai, 3);
});

test('quyển đang học là quyển động vào GẦN NHẤT, nhận cả mốc chuỗi ISO', () => {
  const micros = {
    'DL:TA1.B01': { pass: true, at: '2026-08-01T12:00:00.000Z' },
    'DL:TA2.B01': { pass: false, at: '2026-10-01T12:00:00.000Z' },
  };
  assert.equal(trinhDoTu(hb(micros)).quyen.ma, 'ta2');
});

test('hocBaTu KHÔNG còn trả trinhDo: null', () => {
  const nguon = readFileSync(new URL('../src/mon/tienganh/lib/hocba.js', import.meta.url), 'utf8');
  assert.match(nguon, /trinhDo: trinhDoTu\(quyen\)/);
});
