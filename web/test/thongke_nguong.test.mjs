import test from 'node:test';
import assert from 'node:assert/strict';

import {
  tinhThongKe, chayLaiChuoi, chiSoNG07, chiSoNG09, chatLuongMoHinh, chiSoNG06,
} from '../functions/src/thongke.js';
import { BO_MAC_DINH, MAC_DINH, layNguong } from '../functions/src/nguong.js';

/**
 * CỔNG CHO CHỈ SỐ THEO DÕI NGƯỠNG — Bảng 3.22 (mục 3.8.5).
 *
 * Mấy chỉ số này sinh ra để chuyên gia SỬA NGƯỠNG theo. Một chỉ số tính sai thì
 * hậu quả không phải một màn hình xấu: nó là một lời khuyên sai về việc dạy trẻ,
 * mang dáng một con số đo được. Nên cổng ở đây ghim cách đọc, không chỉ ghim kiểu
 * dữ liệu.
 */

const NGAY = 86400000;
const T0 = Date.UTC(2026, 0, 1);

/** Một chuỗi lượt của MỘT bé tại MỘT nút. `kq` là chuỗi 'ddds' — đúng/sai. */
const chuoi = (kq, { be = 'b1', nut = 'v_x', tu = T0, cach = 60000, ...them } = {}) => [...kq].map((c, i) => ({
  learnerId: be, bktUnit: nut, correct: c === 'd', ts: tu + i * cach, mon: 'tienganh', ...them,
}));

const nhomCua = (luots) => {
  const m = new Map();
  for (const a of luots) {
    const k = `${a.learnerId}::${a.bktUnit}`;
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(a);
  }
  return m;
};

test('số câu tới khi công nhận tinh thông khớp Bảng 3.21', () => {
  /* Bảng 3.21 của luận văn: với bộ tham số mặc định, θ = 0,85 cần BỐN câu đúng
     liên tiếp. Cùng một con số phải ra từ đường thống kê — nếu hai đường cho hai
     số thì một trong hai đang mô tả một hệ thống không tồn tại. */
  const r = chiSoNG07(nhomCua(chuoi('dddddd')), BO_MAC_DINH);
  assert.equal(r.soCauTrungBinhToiThao, 4);
  assert.equal(r.coMauToiThao, 1);
});

test('"công nhận sớm" ĐÒI cách ít nhất một ngày', () => {
  /* Cả điểm của phép đo nằm ở chỗ này. Sai ngay sau đó trong cùng một phiên chỉ là
     sẩy tay; cái đáng lo là bé "đã thạo" rồi HÔM SAU không làm được. Bỏ điều kiện
     một ngày đi thì chỉ số này biến thành "tỉ lệ sẩy tay", vẫn ra số đẹp, và vẫn
     khiến chuyên gia tăng θ vì một lý do không có thật. */
  const cungPhien = chiSoNG07(nhomCua(chuoi('ddddds')), BO_MAC_DINH);
  assert.equal(cungPhien.coMauCongNhanSom, 0, 'sai trong cùng phiên không phải công nhận sớm');
  assert.equal(cungPhien.tiLeCongNhanSom, null, 'chưa có mẫu thì nói "chưa biết", đừng trả 0');

  const homSau = [...chuoi('ddddd'),
    { learnerId: 'b1', bktUnit: 'v_x', correct: false, ts: T0 + 2 * NGAY, mon: 'tienganh' }];
  const r = chiSoNG07(nhomCua(homSau), BO_MAC_DINH);
  assert.equal(r.coMauCongNhanSom, 1);
  assert.equal(r.tiLeCongNhanSom, 1);
});

test('mỗi (bé, nút) chỉ đếm MỘT lần chạm θ', () => {
  /* Bé thạo rồi sai rồi thạo lại thì vẫn là một lần "tới khi được công nhận". Đếm
     mỗi lần vượt θ thì bé học lâu (nhiều lần lên xuống) tự nhiên kéo trung bình
     xuống, tức chỉ số nói ngược lại sự thật. */
  const r = chiSoNG07(nhomCua(chuoi('ddddsdddd')), BO_MAC_DINH);
  assert.equal(r.coMauToiThao, 1);
  assert.equal(r.soCauTrungBinhToiThao, 4);
});

test('NG09: xác suất đúng ở lượt kế tiếp, tách theo từng k', () => {
  /* Cả cách đọc nằm ở chỗ con số đổi thế nào THEO k, nên không được gộp. */
  const r = chiSoNG09(nhomCua(chuoi('sdssdsssd')));
  // sau 1 lần sai: các lượt ở vị trí 1 (đúng), 3 (sai), 6 (sai) → 1/3
  assert.equal(r.k1.coMau, 3);
  assert.equal(r.k1.tiLeDung, 1 / 3);
  // sau 2 lần sai: vị trí 4 (đúng), 7 (sai) → 1/2
  assert.equal(r.k2.coMau, 2);
  assert.equal(r.k2.tiLeDung, 0.5);
  // sau 3 lần sai: vị trí 8 (đúng) → 1/1
  assert.equal(r.k3.coMau, 1);
  assert.equal(r.k3.tiLeDung, 1);
  assert.deepEqual(r.k4, { tiLeDung: null, coMau: 0 }, 'chưa có mẫu → null, không phải 0');
});

test('AUC tính bằng hạng, và `null` khi không có hai lớp', () => {
  /* Dựng tay bốn bước: hai đúng, hai sai, dự đoán biết trước — AUC tính được bằng
     giấy bút, nên cổng ghim đúng con số ấy chứ không ghim "là một số trong [0,1]". */
  const b = (pDuDoan, dung) => ({ pDuDoan, dung });
  // đúng ở 0,9 và 0,4; sai ở 0,6 và 0,2 → cặp xếp đúng: (0,9>0,6) (0,9>0,2) (0,4>0,2) = 3/4
  assert.equal(chatLuongMoHinh([b(0.9, true), b(0.4, true), b(0.6, false), b(0.2, false)]).auc, 0.75);

  /* Hoà phải tính nửa cặp — bỏ qua chỗ này thì AUC lệch đúng ở những mô hình dự
     đoán cùng một số cho mọi lượt, tức những mô hình tệ nhất. */
  assert.equal(chatLuongMoHinh([b(0.5, true), b(0.5, false)]).auc, 0.5);

  assert.equal(chatLuongMoHinh([b(0.9, true), b(0.8, true)]).auc, null,
    'toàn đúng thì AUC vô nghĩa — null, KHÔNG phải 0,5');
  assert.equal(chatLuongMoHinh([]).coMau, 0);
});

test('sai lệch hiệu chuẩn mang DẤU: dương là mô hình lạc quan', () => {
  /* Lấy trị tuyệt đối là mất đúng thông tin cần dùng. Bảng 3.22 đọc NG06 bằng câu
     "dự đoán lạc quan sau nghỉ dài → giảm h" — không có dấu thì câu ấy vô nghĩa. */
  const b = (pDuDoan, dung) => ({ pDuDoan, dung });
  assert.ok(chatLuongMoHinh([b(0.9, false), b(0.9, false)]).saiLechHieuChuan > 0);
  assert.ok(chatLuongMoHinh([b(0.1, true), b(0.1, true)]).saiLechHieuChuan < 0);
});

test('NG06: chia theo nhóm khoảng nghỉ, lượt trong cùng ngày không vào nhóm nào', () => {
  const ds = [
    { learnerId: 'b1', bktUnit: 'v_x', correct: true, ts: T0 },
    { learnerId: 'b1', bktUnit: 'v_x', correct: true, ts: T0 + 3600000 },      // cùng ngày
    { learnerId: 'b1', bktUnit: 'v_x', correct: false, ts: T0 + 2 * NGAY },    // nhóm 1–3
    { learnerId: 'b1', bktUnit: 'v_x', correct: false, ts: T0 + 12 * NGAY },   // nhóm 7–14
  ];
  const r = chiSoNG06(nhomCua(ds), BO_MAC_DINH);
  assert.equal(r.find((x) => x.tu === 1).coMau, 1);
  assert.equal(r.find((x) => x.tu === 7).coMau, 1);
  assert.equal(r.find((x) => x.tu === 3).coMau, 0);
  assert.equal(r.reduce((s, x) => s + x.coMau, 0), 2, 'lượt trong cùng ngày KHÔNG phải lượt sau nghỉ');
});

test('CHẠY THỬ LẠI: cùng nhật ký, đổi θ thì chỉ số đổi theo', () => {
  /* Đây là tính chất mà cả mục 3.8.3 dựa vào — "chuyên gia thấy hậu quả của một
     thay đổi TRƯỚC khi duyệt". Nó chỉ đúng khi thống kê dựng lại mức thạo từ nhật
     ký, chứ không đọc kho `mastery` (kho ấy chỉ có một bộ ngưỡng: bộ đang hành). */
  const luots = chuoi('dddddd');
  const voiTheta = (theta) => chiSoNG07(nhomCua(luots), {
    phienBan: 9, macDinh: { ...MAC_DINH }, theoPhamVi: { toanHe: { NG07: theta } },
  }).soCauTrungBinhToiThao;

  assert.equal(voiTheta(0.80), 3, 'Bảng 3.21: θ 0,80 cần 3 câu');
  assert.equal(voiTheta(0.85), 4);
  assert.equal(voiTheta(0.90), 4, 'Bảng 3.21: 0,85 và 0,90 cho CÙNG một nhịp');
  assert.equal(voiTheta(0.95), 5);
});

test('chuỗi chạy lại dùng ngưỡng theo PHẠM VI của từng lượt', () => {
  const bo = {
    phienBan: 9,
    macDinh: { ...MAC_DINH },
    theoPhamVi: { toanHe: { NG04: 0.30 }, dangCau: { go: { NG04: 0.02 } } },
  };
  const [chon] = chayLaiChuoi([{ learnerId: 'b', bktUnit: 'v', correct: true, ts: T0, mode: 'chon' }], bo);
  const [go] = chayLaiChuoi([{ learnerId: 'b', bktUnit: 'v', correct: true, ts: T0, mode: 'go' }], bo);
  assert.ok(chon.pDuDoan > go.pDuDoan,
    'câu trắc nghiệm phải có xác suất đoán trúng cao hơn câu gõ chữ');
});

test('cỡ mẫu tối thiểu chặn ĐỀ XUẤT, không chặn THỐNG KÊ', () => {
  /* Giấu số liệu vì "chưa đủ mẫu" thì chuyên gia không bao giờ biết dữ liệu đang
     tới đâu, cũng không biết còn thiếu bao nhiêu. Nên thống kê cứ tính và cứ ghi
     kèm cỡ mẫu; chốt NG21 đứng ở chỗ biến thống kê thành đề xuất. */
  const r = tinhThongKe(chuoi('dddd'), BO_MAC_DINH);
  assert.equal(r.coMau, 4);
  assert.equal(r.duMauDeHoc, false);
  assert.notEqual(r.NG07.soCauTrungBinhToiThao, null, 'vẫn phải TÍNH, chỉ là chưa đủ để học');
  assert.equal(r.nguongVer, BO_MAC_DINH.phienBan, 'chỉ số phải ghi bộ ngưỡng đã dùng');

  const nhieu = [];
  for (let i = 0; i < layNguong(BO_MAC_DINH, 'NG21'); i++) {
    nhieu.push(...chuoi('d', { be: `b${i}`, tu: T0 + i * 1000 }));
  }
  assert.equal(tinhThongKe(nhieu, BO_MAC_DINH).duMauDeHoc, true);
});

test('hạn chế của chỉ số đi XUỐNG tài liệu, không chỉ nằm trong chú thích', () => {
  /* Hai hạn chế đã biết: NG08 chưa trừ được những lần bé lên lại NHỜ phụ đạo (nhật
     ký lượt không ghi điều đó), và NG16 chưa gom được theo bậc (nhật ký không mang
     bậc). Người đọc bảng thống kê phải thấy hai điều ấy — một hạn chế chỉ ghi trong
     mã là một hạn chế không ai đọc. */
  const r = tinhThongKe(chuoi('dsdsd', { ms: 5000, mode: 'chon' }), BO_MAC_DINH);
  assert.equal(r.NG08.chuaTruPhuDao, true);
  assert.equal(r.NG16.thieuBac, true);
});

test('lượt thiếu nút hoặc thiếu bé bị loại, không làm vỡ phép tính', () => {
  const r = tinhThongKe([
    ...chuoi('dd'),
    { learnerId: 'b1', correct: true, ts: T0 },          // thiếu bktUnit
    { bktUnit: 'v_x', correct: true, ts: T0 },           // thiếu learnerId
    null,
  ], BO_MAC_DINH);
  assert.equal(r.coMau, 2);
  assert.equal(r.soChuoi, 1);
});
