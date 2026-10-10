import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

/**
 * MỌI MÃ NÚT TRONG BÀI PHẢI LÀ MỘT ĐỈNH CỦA ĐỒ THỊ TRI THỨC.
 *
 * ── VÌ SAO CÓ CỔNG NÀY ──
 * Phát hiện khi dựng bảng đối chiếu luận văn v4: phép đếm «nút dưới 4 câu» ra 73
 * thay vì 32, và chênh lệch là 46 mã bài học dùng mà đồ thị không có.
 *
 * Hậu quả khác nhau theo chỗ mã ấy nằm:
 *   · là `maNut` CHÍNH  → lượt trả lời mang `bktUnit` ấy, BKT vẫn theo dõi được,
 *     nhưng phép chẩn đoán trên đồ thị KHÔNG đặt nút ấy vào đâu: không có nút
 *     trước, không thành ứng viên gốc rễ, lan truyền ngược dừng ngay tại đó.
 *   · ở `maNutDs`       → mọi chỗ đọc nó coi từng mục là một nút (`vectorS` gộp mức
 *     thạo, `baiTienQuyet` tra nút trước, `viecTiepCuaBai` hỏi hàm chính sách). Mã
 *     ngoài đồ thị KHÔNG BAO GIỜ có mức thạo, nên bài chứa nó không bao giờ ra
 *     `vuotAi` — thẻ ôn không bao giờ được hoãn dù bé đã vững hẳn.
 *
 * Cả hai hỏng LẶNG LẼ: không màn nào đổi màu, không cổng nào đỏ, chỉ mấy phép suy
 * luận trên đồ thị âm thầm kém đi.
 *
 * ⚠ CỔNG NÀY SO VỚI ĐỒ THỊ, KHÔNG SO VỚI DANH SÁCH TIỀN TỐ. Lọc theo `cum_`/`them_`
 * là ghim chính tả — thêm một tiền tố mới là cổng lặng lẽ bỏ sót.
 */

const GOC = new URL('../public/content', import.meta.url).pathname;
const DT = JSON.parse(readFileSync(join(GOC, 'tienganh/do_thi.json'), 'utf8'));

function tepTiengAnh() {
  const ra = [];
  for (const t of readdirSync(GOC)) {
    const d = join(GOC, t);
    if (!statSync(d).isDirectory() || !/^ta\d$/.test(t)) continue;
    for (const f of readdirSync(d)) if (f.endsWith('.json')) ra.push(join(d, f));
  }
  return ra;
}

function* moiCau(x) {
  const hang = [x];
  while (hang.length) {
    const y = hang.pop();
    if (Array.isArray(y)) { hang.push(...y); continue; }
    if (!y || typeof y !== 'object') continue;
    if (y.id && (y.format || y.answerKey)) yield y;
    for (const v of Object.values(y)) if (v && typeof v === 'object') hang.push(v);
  }
}

const tep = tepTiengAnh();

test('đồ thị và nội dung đều có mặt để soi', () => {
  assert.ok(Object.keys(DT.nut).length > 1000, 'đồ thị rỗng — cổng đang soi nhầm chỗ');
  assert.ok(tep.length > 50, `chỉ thấy ${tep.length} tệp bài`);
});

test('mọi `maNut` CHÍNH là một đỉnh của đồ thị', () => {
  const xau = [];
  for (const t of tep) {
    let d; try { d = JSON.parse(readFileSync(t, 'utf8')); } catch { continue; }
    for (const c of moiCau(d)) {
      if (c.maNut && !DT.nut[c.maNut]) xau.push(`${t.split('/').pop()} ${c.id}: ${c.maNut}`);
    }
  }
  assert.deepEqual(xau, [],
    `${xau.length} câu có nút chính ngoài đồ thị — phép chẩn đoán không đặt được chúng vào đâu:\n  `
    + xau.slice(0, 15).join('\n  '));
});

test('mọi mã trong `maNutDs` là một đỉnh của đồ thị', () => {
  const xau = [];
  for (const t of tep) {
    let d; try { d = JSON.parse(readFileSync(t, 'utf8')); } catch { continue; }
    for (const c of moiCau(d)) {
      for (const m of (c.maNutDs || [])) {
        if (!DT.nut[m]) xau.push(`${t.split('/').pop()} ${c.id}: ${m}`);
      }
    }
  }
  assert.deepEqual(xau, [],
    `${xau.length} mã trong maNutDs ngoài đồ thị — bài chứa chúng không bao giờ ra \`vuotAi\`:\n  `
    + xau.slice(0, 15).join('\n  '));
});

test('`maNut` chính luôn nằm trong `maNutDs`', () => {
  /* `maNutDs` là «mọi nút câu này chạm tới», nên nó phải chứa cả nút chính. Thiếu
     thì `viecTiepCuaBai` xét một tập nút KHÁC với tập mà BKT đang theo dõi. */
  const xau = [];
  for (const t of tep) {
    let d; try { d = JSON.parse(readFileSync(t, 'utf8')); } catch { continue; }
    for (const c of moiCau(d)) {
      if (c.maNut && Array.isArray(c.maNutDs) && !c.maNutDs.includes(c.maNut)) {
        xau.push(`${t.split('/').pop()} ${c.id}`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu có nút chính không nằm trong maNutDs`);
});

test('đồ thị KHÔNG có đỉnh mồ côi do chính phép vá sinh ra', () => {
  /* `tools/va_nut_mo_coi.py` thêm `sp_g3_starter_1` và một cạnh từ nút cầu
     `sp_g3_numbers`. Nếu phép vá chạy nửa chừng — thêm nút mà hụt cạnh — thì nút
     mới nằm trơ, và nút cầu vẫn không có bài dạy. */
  const n = DT.nut.sp_g3_starter_1;
  assert.ok(n, 'thiếu sp_g3_starter_1 — 6 câu của DL:TA3.B00 sẽ mồ côi trở lại');
  assert.equal(n.b, 'DL:TA3.B00', 'nút phải biết mình được dạy ở bài nào');
  const canh = DT.canh.filter((c) => c.can === 'sp_g3_starter_1');
  assert.equal(canh.length, 1, 'phải có đúng một cạnh nối lên nút cầu');
  assert.equal(canh[0].truoc_khi, 'sp_g3_numbers',
    'nút cầu giữa hai khối lớp phải nối xuống mẫu câu thật dạy nó');
});
