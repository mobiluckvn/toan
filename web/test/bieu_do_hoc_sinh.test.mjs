/**
 * CỔNG BIỂU ĐỒ MỘT EM — chạy: node test/bieu_do_hoc_sinh.test.mjs
 *
 * `functions/src/bieuDo.js` dựng năm chuỗi cho tab "Biểu đồ" của cô giáo. Cổng giữ
 * những chỗ dễ sai lặng lẽ: ranh giới tuần theo giờ VIỆT NAM, tuần nghỉ học vẫn có
 * điểm, chỉ tính lần thử ĐẦU, đếm lần gặp theo nút, và tách đúng hai môn.
 */
import { readFileSync } from 'node:fs';
import {
  buildBieuDo, buildMoHinh, dauTuan, monCua, LAN_GAP_TOI_DA, MAU_TOI_THIEU,
} from '../functions/src/bieuDo.js';
import { applyAttempt } from '../functions/src/bkt.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const VN = (s) => Date.parse(`${s}+07:00`);

t('Chủ nhật 23:30 giờ VN vẫn thuộc tuần cũ', dauTuan(VN('2026-07-12T23:30:00')) === '2026-07-06');
t('thứ Hai 00:10 giờ VN sang tuần mới (UTC vẫn là Chủ nhật)', dauTuan(VN('2026-07-13T00:10:00')) === '2026-07-13');
t('nhận môn theo mã bài', monCua({ microId: 'DL:TA3.B02' }) === 'tienganh' && monCua({ microId: 'DL:KSN2.B01' }) === 'toan');

const l = (ts, o = {}) => ({ ts, microId: 'DL:KSN2.B01', bktUnit: 'n1', correct: true, tries: 1, ms: 10000, sessionId: 's1', v: 7, ...o });
const bd = buildBieuDo([
  l(VN('2026-07-06T19:05:00'), { correct: false }),
  l(VN('2026-07-06T19:06:00'), { correct: true, tries: 2 }),          // lần thử 2: không tính
  l(VN('2026-07-06T19:07:00'), { microId: 'DL:TA1.B01', mon: 'tienganh', bktUnit: 't1' }),
  // tuần 13/7 nghỉ
  l(VN('2026-07-20T20:40:00'), { sessionId: 's2' }),
  l(VN('2026-07-20T20:41:00'), { sessionId: 's2', microId: 'DL:KSN2.B02', bktUnit: 'n2' }),
]);
t('đủ 3 tuần, kể cả tuần nghỉ', bd.tuan.map((x) => x.tuan).join() === '2026-07-06,2026-07-13,2026-07-20');
t('tuần nghỉ: 0 lượt, tỉ lệ để trống (không phải 0%)',
  bd.tuan[1].luot === 0 && bd.tuan[1].mon.toan.dungLanDau === null);
t('đúng lần đầu chỉ đếm lần thử 1 (Toán tuần 1: 0/1)', bd.tuan[0].mon.toan.dungLanDau === 0);
t('hai môn tách riêng', bd.mon.join() === 'tienganh,toan' && bd.tuan[0].mon.tienganh.dungLanDau === 100);
t('bài đã học cộng dồn, không tụt ở tuần nghỉ',
  bd.tuan.map((x) => x.mon.toan.baiDaHoc).join() === '1,1,2');
t('lần gặp đếm theo nút: n1 lần 1 sai, lần 2 đúng',
  bd.theoLanGap[0].tong === 3 && bd.theoLanGap[1].tong === 1 && bd.theoLanGap[1].dung === 100);
t('giờ bắt đầu buổi theo giờ VN, khung nửa tiếng',
  bd.gioHoc.map((g) => `${g.khung}:${g.buoi}`).join() === '19:00:1,20:30:1');
t('phút học tính từ khoảng cách câu (2 phút tuần đầu)', bd.tuan[0].phut === 2);
t('không lượt nào → không vỡ', buildBieuDo([]).soLuot === 0);

const nhieu = buildBieuDo(Array.from({ length: 20 }, (_, i) => l(VN('2026-07-06T19:00:00') + i * 60000)));
t(`lần gặp gộp đuôi ở ${LAN_GAP_TOI_DA}+`, nhieu.theoLanGap.length === LAN_GAP_TOI_DA
  && nhieu.theoLanGap[LAN_GAP_TOI_DA - 1].tong === 20 - LAN_GAP_TOI_DA + 1);

/* ═══ Phần B: các hình của luận văn, chạy lại BKT ═══ */
{
  const T0 = VN('2026-07-06T19:00:00');
  const ta = (i, nut, ok, ngay = 0) => ({ ts: T0 + ngay * 864e5 + i * 60000, microId: 'DL:TA1.B01',
    mon: 'tienganh', bktUnit: nut, correct: ok, tries: 1, sessionId: `s${ngay}`, v: 7 });
  /* nút a: sai 3 lần liền rồi đúng 6 lần; nút b: 12 lần đúng liền, rồi bỏ 30 ngày. */
  const luot = [
    ...[0, 1, 2].map((i) => ta(i, 'a', false)), ...[3, 4, 5, 6, 7, 8].map((i) => ta(i, 'a', true)),
    ...Array.from({ length: 12 }, (_, i) => ta(20 + i, 'b', true)),
  ];
  const now = T0 + 30 * 864e5;
  const m = buildMoHinh(luot, { now });
  /* P(L) phải TRÙNG với chạy tay applyAttempt — tức đúng mã của hàm nền. */
  let d; for (const a of luot.filter((x) => x.bktUnit === 'b')) d = applyAttempt(d, a, () => a.ts);
  const vb = m.dienBien.find((x) => x.nut === 'b');
  t('P(L) trong hình diễn biến trùng với applyAttempt', vb && vb.luot.at(-1).p === +d.p.toFixed(3));
  t('nút từng "đang mắc" xếp đầu hình diễn biến', m.dienBien[0].nut === 'a' && m.dienBien[0].tungMac);
  t('số lần sai liên tiếp đếm đúng (3 rồi về 0)',
    m.dienBien[0].luot.map((x) => x.sai).join() === '1,2,3,0,0,0,0,0,0');
  t('tình trạng hiện tại: a không còn mắc, tổng 2 nút', m.tinhTrang.tong === 2 && m.tinhTrang.dangMac === 0);
  t('30 ngày không gặp → cả hai nút có cờ nguy cơ quên', m.tinhTrang.nguyCoQuen === 2);
  t('tính quên tới hôm nay: nút b rời dải "đã vững"',
    m.hoSoQuen.truoc[2] >= 1 && m.hoSoQuen.sau[2] < m.hoSoQuen.truoc[2]);
  t(`đường cong học tập bỏ điểm dưới ${MAU_TOI_THIEU} lượt`,
    m.duongCong.tienganh.every((o) => o.tiLeLoi === null));
  t('ngưỡng trả kèm để màn vẽ vạch θ, θ_yếu', m.nguong.theta === 0.85 && m.nguong.thetaYeu === 0.3);
  t('nút đạt θ theo tuần: tuần đầu có nút đạt', m.nutVung[0].vungLuu >= 1);

  /* đủ mẫu: 10 nút, mỗi nút lần 1 sai, lần 2 đúng → lỗi 100% rồi 0% */
  const nhieu = [];
  for (let n = 0; n < MAU_TOI_THIEU; n++) { nhieu.push(ta(n * 2, `n${n}`, false), ta(n * 2 + 1, `n${n}`, true)); }
  const c = buildMoHinh(nhieu, { now }).duongCong.tienganh;
  t('đường cong học tập: tỉ lệ LỖI theo lần luyện', c[0].tiLeLoi === 100 && c[1].tiLeLoi === 0);
  const toan = buildMoHinh([0, 1, 2].map((i) => ({ ...ta(i, 'CHUONG:1@G2', true), mon: 'toan',
    microId: `DL:KSN2.B0${i}` })), { now }).duongCong.toan;
  t('Toán đếm lần luyện theo BÀI, không theo nút chương', toan[0].tong === 3 && toan[1].tong === 0);
}

const nen = readFileSync(new URL('../functions/index.js', import.meta.url), 'utf8');
const ham = nen.slice(nen.indexOf('export const bieuDoHocSinh'), nen.indexOf('export const bieuDoHocSinh') + 900);
t('hàm nền chỉ cho giáo viên và quản trị', /vai !== 'teacher' && vai !== 'admin'/.test(ham));
t('bảng cô giáo không còn lọc em mô phỏng ra',
  !/roster\.filter\(\(r\) => !r\.moPhong\)/.test(nen));

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
