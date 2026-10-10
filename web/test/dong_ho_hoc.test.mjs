/* ═══════════ ĐỒNG HỒ HỌC ĐO ĐÚNG CÁI CẦN ĐO ═══════════
 * chạy: node test/dong_ho_hoc.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 *
 * Phép đo cũ (`minutesStudied` trong functions/src/report.js) cộng KHOẢNG CÁCH giữa
 * hai lượt bấm "Kiểm tra". Nay cả bốn quyển đã chuyển sang video: 405 video, cộng
 * lại 390,7 phút giảng, và xem video thì con không bấm gì — nên không một giây nào
 * trong đó được đếm. Con xem trọn video sáu mươi lăm giây rồi trả lời đúng ngay câu
 * chốt thì sổ ghi "học 0 phút".
 *
 * `lib/dongHo.js` đo theo BƯỚC nên bước xem video có số như mọi bước khác. Nhưng đo
 * theo bước lại mở ra một loạt ngả sai mà phép cũ không có: con mở bài rồi đi ăn
 * cơm, con chuyển tab, con chỉnh lại đồng hồ máy. Tệp này canh đúng những ngả ấy.
 */
import { cong, tomTat, dongHo, maNgay, laBuocLam, TRAN_MOT_LAN }
  from '../src/mon/toan/lib/dongHo.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── Cộng một quãng ── */
t('cộng quãng thường', cong({}, 'practice', 3000).practice === 3000);
t('cộng dồn vào cùng một bước', cong(cong({}, 'intro', 1000), 'intro', 2000).intro === 3000);

/* Trần: con mở bài rồi bỏ đi hai tiếng. Không chặn thì một buổi ra 120 phút. */
t(`quãng dài hơn trần bị cắt về đúng trần (${TRAN_MOT_LAN / 60000} phút)`,
  cong({}, 'intro', 2 * 3600 * 1000).intro === TRAN_MOT_LAN);

/* Quãng ÂM: con chỉnh lại đồng hồ máy giữa buổi thì `now() - moc` ra số âm. Không
   chặn thì tổng bị TRỪ đi, và một buổi học tử tế ra số phút nhỏ hơn thực. */
t('quãng âm bị bỏ, không trừ vào tổng', cong({ intro: 5000 }, 'intro', -9999).intro === 5000);
t('quãng không phải số thì bỏ', cong({}, 'intro', undefined).intro === undefined);

/* ── Tách XEM với LÀM ── */
t('check · practice · assess là bước LÀM',
  ['check', 'practice', 'assess'].every(laBuocLam));
t('intro · sample · worked · finale là bước XEM',
  ['intro', 'sample', 'worked', 'finale'].every((b) => !laBuocLam(b)));
/* Bước lạ (thêm chặng mới mà quên khai) phải rơi vào XEM chứ không biến mất khỏi
   tổng — thà xếp nhầm cột còn hơn nuốt mất thời gian con đã bỏ ra. */
t('bước lạ vẫn được tính, xếp vào XEM', !laBuocLam('chang_moi_nao_do'));

const ts = tomTat({ intro: 60000, check: 30000, practice: 90000 });
t('tổng = xem + làm', ts.giay === 180 && ts.giayXem === 60 && ts.giayLam === 120);
t('sổ rỗng ra 0 chứ không ra NaN', tomTat({}).giay === 0);

/* ── Đồng hồ có trạng thái ── */
{
  let gio = 1000;
  const now = () => gio;
  const d = dongHo(now);
  d.doiBuoc('intro'); gio += 65000;          // xem trọn video 65 giây
  d.doiBuoc('check'); gio += 20000;          // trả lời câu chốt
  d.doiBuoc('practice'); gio += 40000;
  const r = d.chot();
  t('video 65 giây ĐƯỢC ĐẾM (đây là cả lý do của tệp này)', r.giayXem === 65);
  t('phần trả lời đếm riêng', r.giayLam === 60);
  t('tổng đúng', r.giay === 125);
}

/* Khuất màn hình thì dừng. Đây là ngả hay gặp nhất: trẻ con chuyển tab suốt, mà
   trần 5 phút vẫn cho không công mỗi lần chuyển. */
{
  let gio = 0;
  const d = dongHo(() => gio);
  d.doiBuoc('intro'); gio += 10000;
  d.roi();            gio += 200000;         // đi chỗ khác hơn ba phút
  d.vao();            gio += 5000;
  t('quãng khuất màn hình KHÔNG được tính', d.chot().giay === 15);
}
{
  let gio = 0;
  const d = dongHo(() => gio);
  d.doiBuoc('intro'); gio += 10000;
  d.roi(); d.roi(); d.roi();                 // gọi thừa
  t('gọi roi() nhiều lần không cộng thêm lần nào', d.chot().giay === 10);
}
{
  let gio = 0;
  const d = dongHo(() => gio);
  d.vao();                                   // vào khi chưa có bước nào
  gio += 10000;
  t('vao() lúc chưa có bước thì không dựng quãng ma', d.chot().giay === 0);
}

/* ── ĐẢO CHIỀU: phép trên chỉ có nghĩa nếu đồng hồ THẬT SỰ đếm ── */
{
  let gio = 0;
  const d = dongHo(() => gio);
  d.doiBuoc('intro'); gio += 7000;
  t('đồng hồ có đếm ra số thật (không phải luôn trả 0)', d.chot().giay === 7);
}

/* ── Mã ngày phải theo giờ Việt Nam ──
   `toISOString()` trả giờ UTC, nên con học 22h tối thứ Ba bị ghi sang thứ Tư — chuỗi
   ngày học đứt oan, mà 22h lại đúng giờ nhiều bé ngồi vào bàn. */
{
  /* 01:00 sáng ngày 18 giờ Việt Nam = 18:00 ngày 17 giờ UTC. Đây là ca bẫy thật:
     `toISOString()` ghi buổi học ấy sang NGÀY HÔM TRƯỚC. */
  const khuya = Date.parse('2026-08-17T18:00:00Z');
  const utc = new Date(khuya).toISOString().slice(0, 10);
  t('giờ VN đọc đúng ngày 18', maNgay(khuya) === '2026-08-18');
  t(`và lối UTC đọc SAI thành ${utc} — bẫy có thật, không phải lo hão`,
    utc === '2026-08-17' && utc !== maNgay(khuya));

  const toi = Date.parse('2026-08-17T15:30:00Z');   // 22:30 giờ VN, vẫn ngày 17
  t('22h30 giờ VN vẫn là ngày 17', maNgay(toi) === '2026-08-17');
  const sang = Date.parse('2026-08-17T01:00:00Z');  // 08:00 giờ VN
  t('sáng sớm giờ VN cũng đúng ngày', maNgay(sang) === '2026-08-17');
}

/* ── Tài liệu tiến độ mang được ba con số giây ── */
{
  const { buildProgressDoc } = await import('../src/mon/toan/lib/sync.js');
  const d = buildProgressDoc({
    microId: 'DL:KSN5Q1.B1.M1', grade: { pass: true, right: 3, total: 3 },
    events: [], sessionId: 's1', gio: { giay: 125, giayXem: 65, giayLam: 60 },
  });
  t('tiến độ mang giây của lượt học', d.giay === 125 && d.giayXem === 65 && d.giayLam === 60);
  const k = buildProgressDoc({
    microId: 'DL:KSN5Q1.B1.M1', grade: { pass: true }, events: [], sessionId: 's1',
  });
  /* null chứ KHÔNG phải 0: "chưa đo được" khác hẳn "học 0 giây", và sổ phải phân
     biệt được hai thứ ấy để không hiện một con số sai cho bố mẹ tin theo. */
  t('không có đồng hồ thì để null, không để 0', k.giay === null && k.giayXem === null);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
