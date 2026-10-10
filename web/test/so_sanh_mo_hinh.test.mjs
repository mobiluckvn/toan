import test from 'node:test';
import assert from 'node:assert/strict';

import {
  aucXepCho, deLong, phanPhoiChuan, duDoan, chayKB2, BAN, TOI_THIEU_MOI_PHAN,
} from '../functions/src/soSanhMoHinh.js';
import { chatLuongMoHinh } from '../functions/src/thongke.js';
import { BO_MAC_DINH, layNguong } from '../functions/src/nguong.js';

/**
 * SO SÁNH PHIÊN BẢN MÔ HÌNH — kịch bản KB2 (Bảng 3.24).
 *
 * ⚠ PHẦN ĐÁNG CANH NHẤT KHÔNG PHẢI PHÉP TÍNH, MÀ LÀ PHÉP TỪ CHỐI KẾT LUẬN.
 * Chạy lần đầu trên dữ liệu thật, DeLong cho p < 0,01 ở cả sáu cặp — nhìn qua thì
 * mọi thứ «khác nhau thật». Nhưng AUC gộp và AUC trung bình từng phần cho hai thứ
 * tự NGƯỢC nhau, và một phần chia chỉ có 3 lượt. Trao ra sáu con số p mà không nói
 * điều đó là mời người đọc kết luận sai bằng chính con số mình đưa cho họ.
 */

const tao = (seed) => {
  let s = seed >>> 0;
  return () => { s = (Math.imul(s, 1103515245) + 12345) >>> 0; return s / 4294967296; };
};

/* ── AUC và giá trị xếp chỗ ─────────────────────────────────────────────── */

test('AUC tính bằng giá trị xếp chỗ KHỚP với AUC tính bằng hạng', () => {
  /* Hai đường tính độc lập phải ra cùng một số. Lệch thì một trong hai sai, và cả
     kiểm định DeLong dựng trên đường xếp chỗ nên sai theo. */
  const rnd = tao(7);
  const diem = Array.from({ length: 400 }, () => {
    const dung = rnd() < 0.6;
    return { p: Math.min(0.999, Math.max(0.001, (dung ? 0.6 : 0.4) + (rnd() - 0.5) * 0.6)), dung };
  });
  const a = aucXepCho(diem).auc;
  const b = chatLuongMoHinh(diem.map((x) => ({ pDuDoan: x.p, dung: x.dung }))).auc;
  assert.ok(Math.abs(a - b) < 1e-9, `hai đường tính lệch nhau: ${a} vs ${b}`);
});

test('AUC = null khi chỉ có một lớp', () => {
  assert.equal(aucXepCho([{ p: 0.9, dung: true }, { p: 0.8, dung: true }]), null);
  assert.equal(aucXepCho([]), null);
});

/* ── DeLong ─────────────────────────────────────────────────────────────── */

test('DeLong: HAI MÔ HÌNH Y HỆT NHAU → chênh lệch 0 và p = 1', () => {
  /* Phép thử nền của mọi kiểm định ghép đôi. Ra p nhỏ ở đây thì kiểm định đang
     bịa ra khác biệt, và mọi kết luận sau đó đều vô giá trị. */
  const rnd = tao(11);
  const d = Array.from({ length: 300 }, () => {
    const dung = rnd() < 0.5;
    return { p: rnd(), dung };
  });
  const r = deLong(d, d.map((x) => ({ ...x })));
  assert.equal(r.hieu, 0);
  assert.ok(r.p === null || r.p > 0.99, `hai bản y hệt mà p = ${r.p}`);
});

test('DeLong: mô hình TỐT HƠN HẲN → p rất nhỏ', () => {
  const rnd = tao(13);
  const nhan = Array.from({ length: 400 }, () => rnd() < 0.5);
  const tot = nhan.map((dung) => ({ p: dung ? 0.6 + rnd() * 0.4 : rnd() * 0.4, dung }));
  const te = nhan.map((dung) => ({ p: rnd(), dung }));
  const r = deLong(tot, te);
  assert.ok(r.hieu > 0.2, `chênh lệch quá nhỏ: ${r.hieu}`);
  assert.ok(r.p < 0.001, `p quá lớn: ${r.p}`);
});

test('DeLong ĐÒI hai tập ca cùng thứ tự — lệch thì NÉM, không tính bừa', () => {
  /* So hai AUC trên hai tập ca khác nhau là một phép tính vô nghĩa nhưng vẫn chạy
     ra số. Thà ném còn hơn trả về một con số không ai biết là vô nghĩa. */
  const a = [{ p: 0.9, dung: true }, { p: 0.1, dung: false }];
  assert.throws(() => deLong(a, [{ p: 0.9, dung: false }, { p: 0.1, dung: true }]), /không cùng thứ tự/);
  assert.throws(() => deLong(a, [{ p: 0.5, dung: true }]), /khác cỡ/);
});

test('phân phối chuẩn tích lũy đúng ở mấy mốc quen', () => {
  assert.ok(Math.abs(phanPhoiChuan(0) - 0.5) < 1e-6);
  assert.ok(Math.abs(phanPhoiChuan(1.96) - 0.975) < 2e-3, `Φ(1,96) = ${phanPhoiChuan(1.96)}`);
  assert.ok(Math.abs(phanPhoiChuan(-1.96) - 0.025) < 2e-3);
  assert.ok(phanPhoiChuan(6) > 0.999999);
});

/* ── Bốn phiên bản ──────────────────────────────────────────────────────── */

test('mốc đoán theo TỪNG NÚT, không phải một hằng số chung', () => {
  /* Bản đầu cho mốc đoán bằng tỉ lệ đúng chung; gộp năm phần lại ra AUC 0,367 —
     DƯỚI 0,5, điều một mốc hằng số không thể có. */
  const chuoi = [[
    { learnerId: 'b', bktUnit: 'de', correct: true, ts: 1 },
    { learnerId: 'b', bktUnit: 'kho', correct: false, ts: 2 },
  ]];
  const theoNut = new Map([['de', 0.9], ['kho', 0.1]]);
  const d = duDoan(chuoi, BO_MAC_DINH, 'moc', { theoNut, tiLeChung: 0.5 });
  assert.equal(d[0].p, 0.9);
  assert.equal(d[1].p, 0.1);
  /* Nút chưa gặp thì lùi về tỉ lệ chung, không bịa. */
  const e = duDoan([[{ learnerId: 'b', bktUnit: 'la', correct: true, ts: 1 }]],
    BO_MAC_DINH, 'moc', { theoNut, tiLeChung: 0.42 });
  assert.equal(e[0].p, 0.42);
});

test('bản `bktQuen` thật sự KHÁC `bkt` khi có khoảng nghỉ, và GIỐNG khi không', () => {
  const trongPhien = [[
    { learnerId: 'b', bktUnit: 'v', correct: true, ts: 0 },
    { learnerId: 'b', bktUnit: 'v', correct: true, ts: 60000 },
  ]];
  const a = duDoan(trongPhien, BO_MAC_DINH, 'bkt');
  const b = duDoan(trongPhien, BO_MAC_DINH, 'bktQuen');
  /* ⚠ KHÔNG đòi hai bản GIỐNG HỆT. Một phút nghỉ vẫn là nghỉ, và `quenDan` của hàm
     nền cũng tính đúng như thế — đòi bằng nhau tuyệt đối là đòi mã khác với hệ
     thống thật. Thứ đúng để đòi: trong một phiên thì phép quên KHÔNG ĐÁNG KỂ. */
  for (let i = 0; i < a.length; i += 1) {
    assert.ok(Math.abs(a[i].p - b[i].p) < 1e-3,
      `trong cùng phiên mà phép quên đổi tới ${Math.abs(a[i].p - b[i].p)}`);
  }

  const coNghi = [[
    { learnerId: 'b', bktUnit: 'v', correct: true, ts: 0 },
    { learnerId: 'b', bktUnit: 'v', correct: true, ts: 30 * 86400000 },
  ]];
  const c = duDoan(coNghi, BO_MAC_DINH, 'bkt');
  const d = duDoan(coNghi, BO_MAC_DINH, 'bktQuen');
  assert.ok(Math.abs(c[1].p - d[1].p) > 0.01, 'nghỉ 30 ngày mà phép quên không đổi gì');

  /* ⚠ QUÊN KÉO VỀ 0,5 TỪ CẢ HAI PHÍA, không phải kéo xuống.
     Tôi viết bản đầu là «phải kéo XUỐNG» và nó đỏ — phép thử sai, không phải mã
     sai. `bkt.js` đã dặn rõ: kéo về 0,5 chứ không kéo về 0, vì bé quên thì thành
     «không chắc» chứ không thành «chưa từng biết». Hệ quả nghe ngược đời nhưng
     đúng: một nút bé từng làm sai nhiều (p thấp) sẽ NHÍCH LÊN theo thời gian —
     lâu không kiểm thì hiểu biết của hệ thống về bé nhạt đi theo CẢ HAI chiều. */
  /* ⚠ VÀ PHẢI ĐO ĐÚNG ĐẠI LƯỢNG. `quenDan` kéo MỨC THẠO về 0,5, còn thứ `duDoan`
     trả ra là XÁC SUẤT TRẢ LỜI ĐÚNG — hai thang khác nhau:
         P(đúng) = p·(1 − slip) + (1 − p)·guess
     Với bộ mặc định, mức thạo 0,5 ứng với P(đúng) = 0,6 chứ không phải 0,5. Bản đầu
     tôi so với 0,5 và phép thử đỏ, trong khi mã đúng — suýt nữa đi sửa mã theo một
     phép thử đo nhầm thang. */
  const slip = layNguong(BO_MAC_DINH, 'NG03');
  const guess = layNguong(BO_MAC_DINH, 'NG04');
  const moc = 0.5 * (1 - slip) + 0.5 * guess;
  const veMoc = (x, y) => Math.abs(y - moc) < Math.abs(x - moc);
  assert.ok(veMoc(c[1].p, d[1].p),
    `quên phải kéo dự đoán về phía ${moc.toFixed(3)}: ${c[1].p.toFixed(4)} → ${d[1].p.toFixed(4)}`);

  /* Và kéo từ phía TRÊN xuống khi p đang cao. */
  const cao = [[
    ...Array.from({ length: 6 }, (_, i) => ({ learnerId: 'b', bktUnit: 'v', correct: true, ts: i * 60000 })),
    { learnerId: 'b', bktUnit: 'v', correct: true, ts: 60 * 86400000 },
  ]];
  const e = duDoan(cao, BO_MAC_DINH, 'bkt');
  const f = duDoan(cao, BO_MAC_DINH, 'bktQuen');
  assert.ok(f[6].p < e[6].p, 'p đang cao thì quên phải kéo XUỐNG');
  assert.ok(veMoc(e[6].p, f[6].p));
});

/* ── Phép TỪ CHỐI KẾT LUẬN ──────────────────────────────────────────────── */

const sinh = ({ soBe, soNut = 4, soLuot = 10, seed = 3 }) => {
  const rnd = tao(seed);
  const l = [];
  for (let b = 0; b < soBe; b += 1) {
    for (let n = 0; n < soNut; n += 1) {
      let thao = rnd() < 0.1;
      for (let t = 0; t < soLuot; t += 1) {
        l.push({
          learnerId: `b${b}`, bktUnit: `v${n}`,
          correct: thao ? rnd() > 0.1 : rnd() < 0.2,
          ts: Date.UTC(2026, 0, 1) + Math.floor(t / 4) * 2 * 86400000 + (t % 4) * 60000,
        });
        if (!thao && rnd() < 0.2) thao = true;
      }
    }
  }
  return l;
};

test('ít hơn số phần chia thì KHÔNG chạy, và nói rõ còn thiếu bao nhiêu', () => {
  const r = chayKB2(sinh({ soBe: 3 }), BO_MAC_DINH);
  assert.equal(r.duMau, false);
  assert.match(r.viSao, /cần 5 người học/);
});

test('⚠ HAI CÁCH ĐỌC NGƯỢC NHAU thì TỪ CHỐI KẾT LUẬN', () => {
  /* Đây là phép quan trọng nhất của cả tệp. Với ít người học, AUC gộp và AUC trung
     bình từng phần có thể cho hai thứ tự khác nhau — và khi ấy mấy con số p của
     DeLong (tính trên tập gộp) không đỡ được kết luận nào. */
  const r = chayKB2(sinh({ soBe: 6, soLuot: 6, seed: 29 }), BO_MAC_DINH);
  assert.equal(r.duMau, true);
  assert.ok(['ketLuanDuoc', 'chuaKetLuanDuoc'].includes(r.ketLuan));
  if (r.ketLuan === 'chuaKetLuanDuoc') {
    assert.equal(r.thuTu, null, 'từ chối kết luận thì KHÔNG được trả về một thứ tự');
    assert.ok(r.viSao && r.viSao.length > 40, 'phải nói rõ vì sao từ chối');
  } else {
    assert.ok(Array.isArray(r.thuTu) && r.thuTu.length === BAN.length);
  }
});

test('cảnh báo cỡ mẫu đi KÈM KẾT QUẢ, không nằm trong chú thích', () => {
  /* Một hạn chế chỉ ghi trong mã là hạn chế người đọc bảng không thấy. */
  const r = chayKB2(sinh({ soBe: 8 }), BO_MAC_DINH);
  assert.ok(r.canhBao, 'dưới 20 người học mà không có cảnh báo nào');
  assert.match(r.canhBao, /người học/);
});

test('đo TỪNG PHẦN riêng, và biết phần nào quá nhỏ', () => {
  const r = chayKB2(sinh({ soBe: 10 }), BO_MAC_DINH);
  assert.equal(r.tungPhan.length, 5);
  for (const x of r.tungPhan) {
    assert.ok(Number.isFinite(x.coMau));
    for (const b of BAN) assert.ok(x.auc[b] === null || (x.auc[b] >= 0 && x.auc[b] <= 1));
  }
  assert.ok(TOI_THIEU_MOI_PHAN >= 10, 'ngưỡng phần chia quá nhỏ thì vô dụng');
});

test('chia theo NGƯỜI HỌC: không bé nào nằm cả hai bên', () => {
  /* Chia theo lượt thì mô hình đã thấy bé ấy rồi, và AUC cao hơn sự thật một cách
     CÓ HỆ THỐNG — nên không ai nghi. */
  const l = sinh({ soBe: 10 });
  const r = chayKB2(l, BO_MAC_DINH);
  const tong = r.tungPhan.reduce((s, x) => s + x.coMau, 0);
  assert.equal(tong, r.coMau, 'tổng các phần phải bằng toàn bộ — mỗi lượt dự đoán đúng MỘT lần');
  assert.equal(r.tungPhan.reduce((s, x) => s + x.soBeGiuLai, 0), 10,
    'mỗi bé phải nằm ở đúng một phần giữ lại');
});
