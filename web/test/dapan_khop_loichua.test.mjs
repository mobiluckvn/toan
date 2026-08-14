/**
 * CỔNG · ĐÁP ÁN CHẤM MÁY PHẢI KHỚP LỜI CHỮA.
 *
 * `luat_o_nhap` canh HÌNH DẠNG ô nhập (có nhãn chưa, mồi nhử có sai thật không,
 * quyển đọc chậm có ô gõ chữ không). Nó KHÔNG canh được điều quan trọng nhất: con
 * số trong đáp án có ĐÚNG không.
 *
 * Máy không giải hộ được bài toán. Nhưng có một thứ máy so được: mỗi câu đều có
 * `loiChua` — lời giải viết tay — và đáp án chấm máy phải nằm trong đó. Hai chỗ
 * viết cùng một con số thì lệch nhau là có một chỗ sai, và cổng chỉ ra ngay.
 *
 * Đây là loại lỗi tệ nhất của phần luyện tập: bé làm ĐÚNG mà máy báo sai, rồi bé
 * tin máy chứ không tin mình.
 *
 * Áp cho cụm dãy số lớp 4 (B13–B17) — cụm vừa viết tay 14-08. Nới ra cả quyển thì
 * phải soát 44 bài cũ trước, vì lời chữa của chúng viết theo lối khác.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const G = new URL('../../', import.meta.url).pathname;
const O = JSON.parse(readFileSync(`${G}data/lop4_dapan_o.json`, 'utf8'));

const BAI = [13, 14, 15, 16, 17].map((n) => JSON.parse(
  readFileSync(`${G}data/lop4/DL_KSN4_B${n}.json`, 'utf8')));

/** Mọi con số trong một chuỗi, bỏ dấu cách phân nhóm ("1 275" là một số). */
const soTrong = (s) => (String(s).replace(/(?<=\d) (?=\d{3}\b)/g, '')
  .match(/\d+/g) || []).map(Number);

test('mọi câu luyện tập của cụm dãy số đều chấm được bằng máy', () => {
  const thieu = [];
  for (const b of BAI) {
    for (const c of b.cau.filter((x) => x.phan === 'luyenTap')) {
      if (!O[`${b.id}#${c.id}`]) thieu.push(`${b.id}#${c.id}`);
    }
  }
  assert.deepEqual(thieu, [], `${thieu.length} câu không ai chấm được`);
});

test('con số trong đáp án PHẢI có trong lời chữa', () => {
  /* Lệch nhau nghĩa là một trong hai chỗ sai — và cả hai đều do người gõ. */
  const xau = [];
  for (const b of BAI) {
    for (const c of b.cau.filter((x) => x.phan === 'luyenTap')) {
      const o = O[`${b.id}#${c.id}`];
      if (!o) continue;
      const co = new Set(soTrong(c.loiChua));
      const phan = o.parts || [o];
      for (const p of phan) {
        if (typeof p.value !== 'number') continue;
        if (!co.has(p.value)) {
          xau.push(`${b.id}#${c.id} · ô "${p.label || 'đáp số'}" = ${p.value} `
            + `mà lời chữa không có số ấy: "${String(c.loiChua).slice(0, 60)}"`);
        }
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} chỗ đáp án lệch lời chữa`);
});

test('đáp án BẤM CHỌN phải nằm trong danh sách nút', () => {
  const xau = [];
  for (const [k, o] of Object.entries(O)) {
    for (const p of (o.parts || [])) {
      if (!p.options) continue;
      if (!p.options.includes(p.value)) xau.push(`${k}: "${p.value}" không có trong nút`);
    }
  }
  assert.deepEqual(xau, []);
});

test('câu QUIZ: đáp án phải nằm trong danh sách chọn', () => {
  const xau = [];
  for (const b of BAI) {
    for (const c of b.cau.filter((x) => x.phan === 'quiz')) {
      if (c.format !== 'mcq') continue;
      if (!c.choices.includes(c.answerKey.choice)) {
        xau.push(`${b.id}#${c.id}: "${c.answerKey.choice}" không có trong ${c.choices}`);
      }
    }
  }
  assert.deepEqual(xau, []);
});

test('BÀI 13 đi đúng đường video đã dạy', () => {
  /* Bác duyệt video rồi bảo viết bài tập theo video. Ba câu đầu phải bám đúng dãy
     trong video (5, 10, 15, 20, 25) — bé vừa xem xong, gặp lại dãy quen thì câu
     đầu không phải một cửa ải. Và phải hỏi ĐỦ HAI CHIỀU: thứ tự → giá trị, rồi
     giá trị → thứ tự. Thiếu một chiều là bé chỉ học được một nửa. */
  const b13 = BAI.find((b) => b.so === 13);
  const lt = b13.cau.filter((c) => c.phan === 'luyenTap');
  const daySo = /5\s*;\s*10\s*;\s*15\s*;\s*20\s*;\s*25/;
  assert.ok(lt.slice(0, 3).every((c) => daySo.test(c.text)),
    'ba câu đầu phải dùng đúng dãy trong video');
  assert.ok(lt.some((c) => /số hạng thứ hai/i.test(c.text)),
    'phải có câu hỏi thứ tự → giá trị');
  assert.ok(lt.some((c) => /đứng ở thứ tự thứ mấy|đứng thứ mấy/i.test(c.text)),
    'phải có câu hỏi ngược: giá trị → thứ tự');
  assert.ok(lt.some((c) => /lấy số sau trừ số trước/i.test(c.text)),
    'phải có câu dùng đúng cách nói của video');
});
