/** Kiểm BKT & hàng đợi ôn tập trên dữ liệu thật — node test/bkt.test.mjs */
import fs from 'fs';
import {
  bktUpdate, bktSequence, isMastered, applyAttempt, paramsFor, quenDan, NUA_DOI_NGAY,
  DEFAULT_PARAMS, MASTERY_THRESHOLD,
} from '../functions/src/bkt.js';
import {
  parseSchedule, scheduleOf, buildReviewCards, dueCards, reviewCard, overdueCount, BOX_DAYS,
} from '../functions/src/schedule.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const ids = []; for (let b = 1; b <= 56; b++) for (const k of [1, 2, 3]) ids.push(`DL_KSN5Q1_B${b}_M${k}.json`);
const lessons = ids.map((f) => JSON.parse(fs.readFileSync('public/content/lessons/' + f, 'utf8')));

/* ── BKT: hành vi cơ bản ── */
t('đúng thì mức thạo TĂNG', bktUpdate(0.3, true) > 0.3);
t('sai thì mức thạo GIẢM so với đúng', bktUpdate(0.3, false) < bktUpdate(0.3, true));
t('luôn nằm trong (0,1)', [0, 1, 0.5].every((p) => { const v = bktUpdate(p, true); return v > 0 && v < 1; }));
t('giá trị lạ → không vỡ', Number.isFinite(bktUpdate(NaN, true)));

/* ── đúng liên tiếp phải vượt ngưỡng thạo ── */
let need = 0, p = DEFAULT_PARAMS.L0;
while (p < MASTERY_THRESHOLD && need < 20) { p = bktUpdate(p, true); need++; }
t(`đúng liên tiếp ${need} lần thì vượt ngưỡng 0,85`, need >= 3 && need <= 6);
console.log(`   từ L0 = ${DEFAULT_PARAMS.L0} cần ${need} câu đúng liên tiếp để đạt thạo`);

t('sai một câu sau khi thạo → tụt xuống dưới ngưỡng',
  !isMastered(bktUpdate(bktSequence([true, true, true, true]), false)));
t('thạo rồi sai rồi đúng lại → thạo lại',
  isMastered(bktSequence([true, true, true, true, false, true, true])));

/* ── câu bẫy có trọng số riêng ── */
const pm = paramsFor({ mustPass: true });
t('câu bẫy: guess thấp hơn', pm.guess < DEFAULT_PARAMS.guess);
t('đúng câu bẫy tăng mạnh hơn câu thường',
  bktUpdate(0.4, true, pm) > bktUpdate(0.4, true, DEFAULT_PARAMS));
t('sai câu bẫy tụt sâu hơn câu thường',
  bktUpdate(0.7, false, pm) < bktUpdate(0.7, false, DEFAULT_PARAMS));

/* ── applyAttempt tích luỹ ── */
let doc;
for (const ok of [true, true, true]) doc = applyAttempt(doc, { correct: ok, microId: 'DL:KSN5Q1.B49.M1' }, () => 1);
t('đếm đủ số lượt và số đúng', doc.nAttempts === 3 && doc.nCorrect === 3);
t('ghi nhớ micro gần nhất', doc.lastMicroId === 'DL:KSN5Q1.B49.M1');
t('cờ mastered khớp ngưỡng', doc.mastered === isMastered(doc.p));

/* ── BỐN TRƯỜNG THÊM CHO MÔ HÌNH NGƯỜI HỌC (mục 2.3.1 · 2.5.2 luận văn) ──
   Thêm 22-08-2026. Tệp này DÙNG CHUNG với môn Toán đang chạy thật, nên phép canh
   đầu tiên phải là: bốn số cũ KHÔNG xê dịch. */
{
  const chuoi = [
    { correct: true,  ms: 1200, hintsUsed: 0 },
    { correct: false, ms: 3400, hintsUsed: 1 },
    { correct: false,           hintsUsed: 2 },   // thiếu ms: bản ghi đời cũ
    { correct: true,  ms: 800,  hintsUsed: 0 },
  ];
  let d;
  for (const a of chuoi) d = applyAttempt(d, { ...a, microId: 'm' }, () => 1);

  t('số cũ không đổi khi thêm trường mới', d.nAttempts === 4 && d.nCorrect === 2);

  /* struggle_count — sai LIÊN TIẾP, đúng một lần là về 0. Khác hẳn `nAttempts`:
     bé sai 3 lần rồi đúng 10 lần thì tỉ lệ đúng trông vẫn đẹp, mà lúc sai liền
     3 lần mới là lúc bé không tự thoát ra được. */
  t('saiLienTiep về 0 sau một câu đúng', d.saiLienTiep === 0);
  let e; for (const ok of [true, false, false]) e = applyAttempt(e, { correct: ok }, () => 1);
  t('saiLienTiep đếm được chuỗi sai', e.saiLienTiep === 2);

  /* P(L) trước/sau — để tính ΔC ở mục 2.5.3. */
  let f = applyAttempt(undefined, { correct: true }, () => 1);
  t('pTruoc lượt đầu là L0', Math.abs(f.pTruoc - DEFAULT_PARAMS.L0) < 1e-9);
  const g = applyAttempt(f, { correct: true }, () => 1);
  t('pTruoc lượt sau bằng p lượt trước', Math.abs(g.pTruoc - f.p) < 1e-9);

  /* ⚠ RT_avg: lượt THIẾU `ms` phải nằm NGOÀI mẫu, không được coi là 0. Coi là 0
     thì mỗi dòng thiếu kéo trung bình xuống, và "bé trả lời nhanh dần" thành một
     kết luận do lỗi ghi sinh ra. */
  t('RT_avg bỏ lượt thiếu ms ra khỏi mẫu',
    d.msDem === 3 && d.msTrungBinh === Math.round((1200 + 3400 + 800) / 3));
  t('RT_avg KHÔNG coi lượt thiếu ms là 0',
    d.msTrungBinh !== Math.round((1200 + 3400 + 0 + 800) / 4));
  t('chưa đo được lượt nào thì RT_avg là null, không phải 0',
    applyAttempt(undefined, { correct: true }, () => 1).msTrungBinh === null);

  /* H_req — số gợi ý trung bình mỗi lượt tại nút này. */
  t('H_req cộng dồn đúng', d.goiTong === 3 && d.goiTrungBinh === 0.75);

  /* Cộng bằng TỔNG chứ không nhân trung bình cũ với n — phép sau trôi số dần, mà
     tài liệu này sống suốt đời học của bé. Thử bằng một dãy dài. */
  let h; let tong = 0;
  for (let i = 0; i < 500; i += 1) { tong += 100 + i; h = applyAttempt(h, { correct: true, ms: 100 + i }, () => 1); }
  t('cộng dồn 500 lượt không trôi số', h.msTrungBinh === Math.round(tong / 500));
}

/* ── lịch ôn: đọc được từ dữ liệu thật ── */
t('đọc "+3 ngày: câu generator P1"', parseSchedule('+3 ngày: câu generator P1')?.days === 3);
t('dòng không hợp lệ → null', parseSchedule('ôn khi rảnh') === null);

let withSched = 0, totCards = 0, dayset = new Set();
for (const L of lessons) {
  const s = scheduleOf(L);
  if (s.length) withSched++;
  s.forEach((x) => dayset.add(x.days));
  totCards += buildReviewCards({ learnerId: 'L1', microId: L.id, lesson: L, at: 0 }).length;
}
t(`mọi micro có lịch ôn: ${withSched}/168`, withSched === 168);
t('tổng thẻ ôn sinh ra hợp lý', totCards === 168 * 3);
console.log(`   mốc ngày gặp trong dữ liệu: ${[...dayset].sort((a, b) => a - b).join(' · ')} · tổng ${totCards} thẻ`);

/* ── đến hạn & Leitner ── */
const DAY = 86400000;
const cards = buildReviewCards({ learnerId: 'L1', microId: 'DL:KSN5Q1.B49.M1', lesson: lessons[144], at: 0 });
t('mới học xong thì chưa có thẻ nào đến hạn', dueCards(cards, 0).length === 0);
t('sau 1 ngày có thẻ đến hạn', dueCards(cards, 1.1 * DAY).length >= 1);
t('sau 7 ngày cả ba thẻ đến hạn', dueCards(cards, 7.1 * DAY, 9).length === 3);
t('chỉ lấy tối đa n thẻ mỗi phiên', dueCards(cards, 30 * DAY, 2).length === 2);

const c0 = cards[0];
const up = reviewCard(c0, true, 0);
t('ôn đúng → lên hộp, giãn ra', up.box === 1 && up.dueAt === BOX_DAYS[1] * DAY);
const down = reviewCard(up, false, 0);
t('ôn sai → về hộp 0, ôn lại sớm', down.box === 0 && down.dueAt === BOX_DAYS[0] * DAY);
t('đếm thẻ quá hạn', overdueCount(cards, 4 * DAY) === 2);

/* ── bktUnit có mặt trong dữ liệu để gắn mastery ── */
const units = new Set(lessons.map((L) => L.skills?.bktUnit).filter(Boolean));
t(`mọi micro có bktUnit: ${lessons.filter((L) => L.skills?.bktUnit).length}/168`,
  lessons.every((L) => L.skills?.bktUnit));
console.log(`   số đơn vị kỹ năng khác nhau: ${units.size}`);

/* ── QUÊN DẦN (chiều Thời gian, mục 2.1.2) ─────────────────────────────────── */
{
  const NGAY = 86400000;

  t('vừa gặp thì không quên gì', quenDan(0.9, 0) === 0.9);
  t(`sau ${NUA_DOI_NGAY} ngày thì rơi NỬA quãng đường về 0.5`,
    Math.abs(quenDan(0.9, NUA_DOI_NGAY) - 0.7) < 0.005);

  /* ⚠ KÉO VỀ 0.5, KHÔNG VỀ 0. Kéo về 0 là bắt bé học lại từ đầu một thứ đã từng
     thạo — với trẻ con đó là hình phạt cho việc nghỉ vài hôm. */
  t('quên rất lâu vẫn không rơi về 0', quenDan(0.9, 3650) > 0.45);
  t('nút bé từng làm SAI thì NHÍCH LÊN phía 0.5, không tụt sâu thêm',
    quenDan(0.1, 56) > 0.1 && quenDan(0.1, 56) < 0.5);

  /* Điều tôi lo nhất: bé học ĐỀU mà điểm bị tụt oan. */
  let deu; let t0 = 0;
  for (let i = 0; i < 20; i += 1) { deu = applyAttempt(deu, { correct: true }, () => t0); t0 += NGAY; }
  let lien;
  for (let i = 0; i < 20; i += 1) lien = applyAttempt(lien, { correct: true }, () => 0);
  t('học đều mỗi ngày thì mức thạo không bị phạt đáng kể',
    Math.abs(deu.p - lien.p) < 0.02);
  t('học đều 20 hôm thì vẫn đạt thạo', deu.mastered === true);

  /* Nghỉ dài thì mới thấy tụt — và phải tụt THẬT, không thì phép quên vô nghĩa. */
  const nghi = applyAttempt({ p: 0.95, nAttempts: 9, nCorrect: 9, lastSeen: 0 },
    { correct: true }, () => 60 * NGAY);
  t('nghỉ 60 ngày thì mức thạo TRƯỚC lượt mới tụt rõ', nghi.pTruoc < 0.62);

  /* Tài liệu đời cũ không có `lastSeen` — KHÔNG phân rã theo một mốc bịa ra. */
  const cu = applyAttempt({ p: 0.9, nAttempts: 5 }, { correct: true }, () => 999 * NGAY);
  t('thiếu lastSeen thì không phân rã', Math.abs(cu.pTruoc - 0.9) < 1e-9);

  /* Mốc tương lai (đồng hồ máy con sai) không được làm p nhảy lung tung. */
  const tuongLai = applyAttempt({ p: 0.8, nAttempts: 3, lastSeen: 100 * NGAY },
    { correct: true }, () => 0);
  t('lastSeen ở tương lai thì coi như vừa gặp, không tính ngược',
    Math.abs(tuongLai.pTruoc - 0.8) < 1e-9);

  t('lastSeen được cập nhật thành mốc của lượt này', nghi.lastSeen === 60 * NGAY);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
