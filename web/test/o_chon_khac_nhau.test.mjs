import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

/**
 * MỖI Ô TRẮC NGHIỆM PHẢI KHÁC NHAU, VÀ ĐÁP ÁN PHẢI CÓ MẶT.
 *
 * ── VÌ SAO CÓ CỔNG NÀY ──
 * 18 câu của `DL:TA3.B01` lên bản thật với hai ô giống hệt nhau. Câu
 * “hello” nghĩa là gì? có HAI ô cùng ghi "xin chào" — bé bấm ô nào cũng thấy mình
 * vừa chọn giữa hai thứ y hệt, và không hiểu nổi vì sao.
 *
 * Nguyên nhân: bộ sinh lọc mồi nhử theo MÃ TỪ, mà mã thì bao giờ cũng khác nhau.
 * Cái bé NHÌN THẤY lại là `nghia`, và TA3 U1 có `hello`/`hi` cùng nghĩa "xin chào",
 * `bye`/`goodbye` cùng nghĩa "chào tạm biệt".
 *
 * ⚠ Cổng cũ đếm được "câu có mấy ô" nhưng không hỏi "mấy ô ấy có khác nhau không" —
 * nên nó xanh suốt. Đó là lý do cổng này so theo đúng CHUỖI bé đọc được, không so
 * theo mã.
 */

const GOC = new URL('../public/content', import.meta.url).pathname;
const TEN_O = ['choices', 'options', 'luaChon'];

function moiTep(d) {
  const ra = [];
  const di = (duong) => {
    for (const t of readdirSync(duong)) {
      const q = join(duong, t);
      if (statSync(q).isDirectory()) di(q);
      else if (t.endsWith('.json')) ra.push(q);
    }
  };
  di(d);
  return ra;
}

function* moiCau(x) {
  const hang = [x];
  while (hang.length) {
    const y = hang.pop();
    if (Array.isArray(y)) { hang.push(...y); continue; }
    if (!y || typeof y !== 'object') continue;
    for (const ten of TEN_O) {
      const o = y[ten];
      if (Array.isArray(o) && o.length > 1 && o.every((v) => v === null || typeof v !== 'object')) {
        yield { cau: y, ten, o };
      }
    }
    for (const v of Object.values(y)) if (v && typeof v === 'object') hang.push(v);
  }
}

const dapCua = (c) => {
  const k = c.answerKey;
  if (k && typeof k === 'object') {
    for (const t of ['choice', 'value', 'text']) if (k[t] != null) return String(k[t]);
    return null;
  }
  if (typeof k === 'string') return k;
  return c.answer != null ? String(c.answer) : null;
};

const tep = moiTep(GOC);

test('nội dung đang chạy có đủ câu trắc nghiệm để soi', () => {
  /* Cổng quét thư mục; thư mục rỗng thì nó xanh mà chẳng canh gì. */
  let n = 0;
  for (const t of tep) {
    let d; try { d = JSON.parse(readFileSync(t, 'utf8')); } catch { continue; }
    for (const _ of moiCau(d)) n++;
  }
  assert.ok(n > 500, `chỉ thấy ${n} câu có ô chọn — cổng đang soi nhầm chỗ`);
});

test('KHÔNG câu nào có hai ô giống nhau', () => {
  const xau = [];
  for (const t of tep) {
    let d; try { d = JSON.parse(readFileSync(t, 'utf8')); } catch { continue; }
    for (const { cau, o } of moiCau(d)) {
      const chu = o.map((v) => String(v).trim());
      /* So theo chuỗi đã chuẩn hoá hoa/thường: với bé thì "Xin chào" và "xin chào"
         là một ô, dù máy thấy hai chuỗi khác nhau. */
      if (new Set(chu.map((x) => x.toLowerCase())).size !== chu.length) {
        xau.push(`${t.split('/').pop()} ${cau.id ?? '?'}: ${JSON.stringify(chu)}`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu có ô trùng:\n  ${xau.slice(0, 20).join('\n  ')}`);
});

test('đáp án luôn nằm trong danh sách ô', () => {
  /* Phép vá có thể bỏ nhầm chính ô đáp án. Khi ấy bé KHÔNG CÓ cách nào trả lời
     đúng — tệ hơn hẳn hai ô trùng nhau. */
  const xau = [];
  for (const t of tep) {
    let d; try { d = JSON.parse(readFileSync(t, 'utf8')); } catch { continue; }
    for (const { cau, o } of moiCau(d)) {
      const dap = dapCua(cau);
      if (dap == null) continue;
      const co = o.some((v) => String(v).trim().toLowerCase() === dap.trim().toLowerCase());
      if (!co) xau.push(`${t.split('/').pop()} ${cau.id ?? '?'}: đáp ${JSON.stringify(dap)} ∉ ${JSON.stringify(o)}`);
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu không có đáp án trong ô:\n  ${xau.slice(0, 20).join('\n  ')}`);
});

/* ── MỘT PHÉP TÔI ĐÃ BỎ, GHI LẠI KẺO NGƯỜI SAU LẠI THÊM VÀO ──
   Bản đầu tôi thêm phép "câu trắc nghiệm phải có ít nhất ba ô", với lý do nghe rất
   xuôi: hai ô là trò tung đồng xu, đoán bừa trúng một nửa. Chạy ra 399 câu đỏ — và
   gần như tất cả là câu NHỊ PHÂN THẬT: có/không (127 câu) · chẵn/lẻ (23) · đúng/sai
   (18) · lớn hơn/bé hơn · "Is this a tiger?" → Yes, it is. / No, it isn't.

   Câu nhị phân không phải câu hỏng; ép nó thành ba ô là phải bịa ra một ô thứ ba vô
   nghĩa. Luật ấy là luật tôi tự nghĩ ra, không phải tính chất của nội dung — nên nó
   đi. Thứ thật sự cần canh là hai ô ấy có KHÁC NHAU không, và phép trên đã canh.

   Nếu một ngày cần canh "câu bốn ô bị rụng xuống còn hai", thì phải so với số ô bộ
   sinh ĐỊNH tạo, chứ không phải với một con số tròn chọn sẵn. */
