/**
 * CỔNG · KỲ ÔN TẬP CHƯƠNG.
 *
 * Món nợ này nằm im lâu nhất, và nó là kiểu nợ khó thấy nhất: mọi mảnh đều CÓ —
 * `ontap.json` khai 4 kỳ, `luuMucHocBa()` viết xong, luật Firestore mở sẵn
 * `hocBaTA` — chỉ là không mảnh nào gọi mảnh nào. Bản dựng xanh, không lỗi nào,
 * và bé học xong bốn unit thì không có gì xảy ra cả.
 *
 * Nên cổng này kiểm ĐỦ CHUỖI, không chỉ kiểm dữ liệu: đề có câu thật · câu dùng
 * được (có tiếng, có hình) · luật mở đúng · và màn hình có THẬT SỰ gọi tới chỗ
 * ghi học bạ.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { moKyOnTap, conThieuChoOnTap } from '../src/mon/tienganh/lib/dandat.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const TA1 = new URL('../public/content/ta1/', import.meta.url);
const KY = JSON.parse(readFileSync(new URL('ontap.json', TA1)));

const bais = readdirSync(TA1)
  .filter((f) => f.startsWith('DL_TA1_B') && f.endsWith('.json'))
  .map((f) => JSON.parse(readFileSync(new URL(f, TA1))));

test('bốn kỳ, mỗi kỳ có câu THẬT — không còn là danh mục rỗng', () => {
  assert.equal(KY.length, 4);
  for (const k of KY) {
    assert.ok(k.cau?.length > 0, `kỳ ${k.so} không có câu nào`);
    assert.equal(k.soCau, k.cau.length, `kỳ ${k.so}: soCau khai lệch với số câu thật`);
    assert.ok(k.need > 0 && k.need <= k.soCau,
      `kỳ ${k.so}: cần ${k.need}/${k.soCau} câu — ngưỡng vượt số câu thì không bao giờ qua được`);
  }
});

test('mã câu KHÔNG TRÙNG trong một kỳ', () => {
  /* Hai unit đều có câu "C1". Trùng mã thì React dùng chung `key`, giữ nguyên
     state khi sang câu mới, và chỗ chuyển dạng câu là trắng màn hình — đã vỡ thật
     một lần ở đúng kiểu này (chỗ nối ★ sang ★★). */
  for (const k of KY) {
    const ma = k.cau.map((c) => c.id);
    assert.equal(new Set(ma).size, ma.length, `kỳ ${k.so} có mã câu trùng`);
  }
});

test('mọi câu đều CÓ TIẾNG — bé lớp 1 không đọc được đề', () => {
  for (const k of KY) {
    for (const c of k.cau) {
      assert.ok(c.am, `kỳ ${k.so} câu ${c.id} không có clip`);
    }
  }
});

test('mọi câu đều dùng lại clip và hình ĐÃ CÓ, không đòi sinh mới', () => {
  /* Đây là điều kiện để kỳ ôn tập dựng được mà không phải chạy lại cả dây chuyền
     TTS. Câu nào lọt ra ngoài kho có sẵn thì im lặng thành câu câm. */
  const kho = new Set();
  for (const b of bais) {
    for (const c of [...Object.values(b.practice.pools).flat(), ...b.assessment.items]) {
      if (c.am) kho.add(c.am);
    }
  }
  for (const k of KY) {
    for (const c of k.cau) {
      assert.ok(kho.has(c.am), `kỳ ${k.so} câu ${c.id} dùng clip lạ: ${c.am}`);
    }
  }
});

test('đề TRỘN cả bốn unit của chương, không dồn vào một bài', () => {
  for (const k of KY) {
    const tuBai = new Set(k.cau.map((c) => c.tuBai));
    assert.equal(tuBai.size, 4,
      `kỳ ${k.so} chỉ lấy câu từ ${tuBai.size} unit — ôn tập chương thì phải hỏi cả chương`);
    /* Và phải đúng chương của nó: kỳ 2 mà lôi câu chương 1 vào là ôn nhầm chỗ. */
    for (const c of k.cau) {
      const b = bais.find((x) => x.id === c.tuBai);
      assert.equal(b?.chuong, k.chapter, `kỳ ${k.so} lấy câu của chương ${b?.chuong}`);
    }
  }
});

test('câu đúng/sai có cả ĐÚNG và SAI — bấm ✓ suốt không được 10/10', () => {
  for (const k of KY) {
    const tf = k.cau.filter((c) => !c.anhChon).map((c) => c.answerKey.value);
    assert.ok(tf.filter((v) => v === true).length > 0, `kỳ ${k.so} không có câu đáp ĐÚNG`);
    assert.ok(tf.filter((v) => v === false).length > 0, `kỳ ${k.so} không có câu đáp SAI`);
  }
});

test('kỳ ôn tập KHÔNG mở bằng cửa "thử 2 lần"', () => {
  const ds = ['B01', 'B02'];
  /* Đi vòng qua bài thì vẫn học tiếp được, nhưng huy hiệu chương thì không: cho
     lấy huy hiệu khi còn bài chưa đạt là huy hiệu ấy không nói lên điều gì. */
  const diVong = { micros: { B01: { done: true, pass: false, attempts: 5 }, B02: { pass: true } } };
  assert.equal(moKyOnTap(diVong, ds), false);
  assert.equal(conThieuChoOnTap(diVong, ds), 1);

  const dat = { micros: { B01: { pass: true }, B02: { pass: true } } };
  assert.equal(moKyOnTap(dat, ds), true);
  assert.equal(conThieuChoOnTap(dat, ds), 0);

  /* Chương rỗng KHÔNG được tính là "xong hết" — `[].every()` trả true, và đó là
     cách một chương chưa có bài nào lại mở toang kỳ thi của nó. */
  assert.equal(moKyOnTap(dat, []), false);
});

test('màn hình THẬT SỰ ghi vào học bạ — đây mới là chỗ nợ', () => {
  const man = doc('../src/mon/tienganh/components/ManTiengAnh.jsx');
  assert.match(man, /import OnTap from/, 'phải có màn kỳ ôn tập');
  assert.match(man, /luuMucHocBa\(/, 'xong kỳ ôn tập phải ghi lên hocBaTA');
  assert.match(man, /ghiChuong\(/, 'và ghi cả sổ tại máy, để huy hiệu hiện khi mất mạng');
  assert.match(man, /moKyOnTap\(/, 'thẻ kỳ ôn tập phải hỏi luật mở');
  assert.match(man, /page: 'ontap'/, 'phải có đường đi tới màn kỳ ôn tập');

  const on = doc('../src/mon/tienganh/components/OnTap.jsx');
  assert.match(on, /CauNgheNhin/, 'dùng chung component với sát hạch');
  assert.doesNotMatch(on, /Bỏ qua câu này|Để câu này lại sau/,
    'kỳ ôn tập là lúc ĐO, không có nút bỏ qua');

  const bh = doc('../src/mon/tienganh/components/BaiHoc.jsx');
  assert.match(bh, /import CauNgheNhin from/,
    'sát hạch và kỳ ôn tập phải dùng CHUNG một cách chấm, không chép hai bản');
});
