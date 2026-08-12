/**
 * CỔNG BẢNG XẾP HẠNG — chạy: node test/xephang.test.mjs
 *
 * Bảng này là TÀI LIỆU DUY NHẤT một bé đọc được về bé khác, nên phép kiểm chia hai
 * phần và phần đầu quan trọng hơn hẳn:
 *
 *   A · KHÔNG RÒ RỈ  — tài liệu đăng lên không được mang email, không mang số bài
 *      sai, không mang bất cứ thứ gì ngoài biệt danh · lớp · sao. Và tên hiện phải
 *      lùi về "Bạn nhỏ lớp N" khi bé chưa khai tên, vì lúc ấy `displayName` chính là
 *      phần trước @ của email bố mẹ (xem buildUserDoc).
 *
 *   B · CÔNG BẰNG VÀ THÚC ĐƯỢC — bé lớp 2 phải có cửa thắng bé lớp 5; cày điểm phải
 *      bị chặn; bé ngoài Top 20 vẫn phải thấy mình và thấy khoảng cách tới người trên.
 */
import { readFileSync } from 'node:fs';
import {
  SAO, TRAN_SAO_NGAY, ngayVN, saoTrongKhoang, chuoiNgay, tenHien, xepHang, buildBangXepHang,
} from '../functions/src/bangxephang.js';
import {
  xepLai, danhSachHien, khoangCachTren, soKe, loiSoKe, locLop, dsLop, BANG, huyChuong,
} from '../src/chung/lib/xephang.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const NOW = Date.parse('2026-08-11T14:00:00Z');       // 21:00 giờ VN
const NGAY = 86400000;
const att = (uid, ts, ok = true) => ({ learnerId: uid, correct: ok, ts });
const em = (uid, o = {}) => ({ uid, grade: 3, displayName: '', profileComplete: false, ...o });

/* ═══════════ A · KHÔNG RÒ RỈ ═══════════ */

t('chưa khai tên → KHÔNG lấy tên tạm từ email',
  tenHien({ displayName: 'congvt', profileComplete: false, grade: 3 }) === 'Bạn nhỏ lớp 3');
t('đã khai tên → hiện đúng tên con',
  tenHien({ displayName: 'Su Kem', profileComplete: true, grade: 3 }) === 'Su Kem');
t('có biệt danh → biệt danh thắng tất cả',
  tenHien({ displayName: 'Su Kem', profileComplete: true, bietDanh: 'Trí Long' }) === 'Trí Long');
t('biệt danh dài bị cắt, không phá bố cục bảng',
  tenHien({ bietDanh: 'x'.repeat(90) }).length === 24);

{
  const bang = buildBangXepHang({
    roster: [em('u1', { displayName: 'An', profileComplete: true, email: 'bome@gmail.com' })],
    attempts: [att('u1', NOW - NGAY)],
    progress: { u1: { m1: { pass: true, at: NOW - NGAY }, m2: { pass: false, at: NOW } } },
    hocBa: {}, now: NOW,
  });
  const chuoiJson = JSON.stringify(bang);
  t('tài liệu đăng lên KHÔNG chứa email', !chuoiJson.includes('bome@gmail.com') && !chuoiJson.includes('@'));
  const CHO_PHEP = ['ma', 'ten', 'lop', 'saoTuan', 'saoTong', 'chuoi',
                    'baiTuan', 'cauTuan', 'baiDat', 'huyHieu', 'vongDau',
                    'hangTuan', 'hangChuoi', 'hangTong'];
  const thua = Object.keys(bang.rows[0]).filter((k) => !CHO_PHEP.includes(k));
  t(`dòng chỉ mang đúng những trường đã duyệt (thừa: ${thua.join()})`, thua.length === 0);
  t('không đăng số bài SAI hay bài đang tắc',
    !chuoiJson.includes('tried') && !chuoiJson.includes('stuck') && !chuoiJson.includes('m2'));
  t('công thức sao đăng kèm để bé đọc được', bang.cong.cauDung === SAO.cauDung);
}

/* ═══════════ B · SAO: THƯỞNG NỖ LỰC, CHẶN CÀY ═══════════ */

t('mỗi câu đúng một sao',
  saoTrongKhoang({ attempts: [att('u', NOW), att('u', NOW)] }) === 2 * SAO.cauDung);
t('câu SAI không được sao',
  saoTrongKhoang({ attempts: [att('u', NOW, false), att('u', NOW, false)] }) === 0);
t('bài · huy hiệu · vòng đấu cộng đúng thang',
  saoTrongKhoang({ baiDat: [1, 2], huyHieu: [1], vongDau: [1] })
  === 2 * SAO.baiDat + SAO.huyHieu + SAO.vongDau);
t('thang sao xếp đúng thứ tự giá trị',
  SAO.cauDung < SAO.baiDat && SAO.baiDat < SAO.huyHieu && SAO.huyHieu < SAO.vongDau);

/* CÀY ĐIỂM: ngồi bấm lại một bài 500 lượt trong một ngày. */
{
  const cay = Array.from({ length: 500 }, () => att('u', NOW));
  t(`làm 500 câu trong MỘT ngày cũng chỉ được ${TRAN_SAO_NGAY} sao`,
    saoTrongKhoang({ attempts: cay }) === TRAN_SAO_NGAY);
  /* Nhưng học ĐỀU ba ngày thì phải được đủ ba ngày — trần theo NGÀY, không theo tổng. */
  const deu = [...Array(40).fill(0).map(() => att('u', NOW)),
               ...Array(40).fill(0).map(() => att('u', NOW - NGAY)),
               ...Array(40).fill(0).map(() => att('u', NOW - 2 * NGAY))];
  t('học đều ba ngày thì được sao của cả ba ngày', saoTrongKhoang({ attempts: deu }) === 120);
}

/* BÉ LỚP 2 PHẢI CÓ CỬA THẮNG BÉ LỚP 5 — cả điểm của bảng "tuần này". */
{
  const bang = buildBangXepHang({
    roster: [em('long', { grade: 2, bietDanh: 'Trí Long' }), em('kem', { grade: 3, bietDanh: 'Su Kem' })],
    attempts: [
      // Trí Long lớp 2: học chăm cả tuần
      ...Array(30).fill(0).map(() => att('long', NOW - NGAY)),
      ...Array(30).fill(0).map(() => att('long', NOW - 2 * NGAY)),
      // Su Kem lớp 3: đã đạt nhiều bài từ TRƯỚC, tuần này học ít
      ...Array(5).fill(0).map(() => att('kem', NOW - NGAY)),
    ],
    progress: {
      long: { a: { pass: true, at: NOW - NGAY } },
      kem: Object.fromEntries(Array.from({ length: 40 }, (_, i) =>
        [`m${i}`, { pass: true, at: NOW - 90 * NGAY }])),      // học từ ba tháng trước
    },
    hocBa: {}, now: NOW,
  });
  const long = bang.rows.find((r) => r.ma === 'long');
  const kem = bang.rows.find((r) => r.ma === 'kem');
  t('bảng TUẦN NÀY: bé chăm tuần này thắng bé đã học nhiều từ trước',
    long.hangTuan === 1 && kem.hangTuan === 2);
  t('bảng TỔNG SAO: bé đi đường dài vẫn được ghi nhận',
    kem.hangTong === 1 && long.hangTong === 2);
  t('thành tích CŨ không rơi vào sao tuần này', kem.saoTuan < long.saoTuan);
  t('tổng sao KHÔNG cộng câu trả lời đúng (nhật ký chỉ giữ theo cửa sổ)',
    kem.saoTong === 40 * SAO.baiDat);
}

/* ═══════════ C · CHUỖI NGÀY ═══════════ */
t('học hôm nay và hôm qua → chuỗi 2',
  chuoiNgay([att('u', NOW), att('u', NOW - NGAY)], NOW) === 2);
t('nghỉ hôm nay nhưng tối qua có học → chuỗi CÒN SỐNG',
  chuoiNgay([att('u', NOW - NGAY), att('u', NOW - 2 * NGAY)], NOW) === 2);
t('nghỉ hai ngày → chuỗi đứt',
  chuoiNgay([att('u', NOW - 2 * NGAY), att('u', NOW - 3 * NGAY)], NOW) === 0);
t('chưa học buổi nào → chuỗi 0', chuoiNgay([], NOW) === 0);
t('học nhiều lượt cùng một ngày vẫn chỉ tính một ngày',
  chuoiNgay([att('u', NOW), att('u', NOW - 1000), att('u', NOW - 2000)], NOW) === 1);
/* Ranh giới ngày theo giờ VN: 21h30 tối VN và 6h sáng hôm sau là HAI ngày, dù cùng
   một ngày UTC. Tính theo UTC thì chuỗi đứng im dù bé học đều. */
t('ranh giới ngày tính theo giờ Việt Nam',
  ngayVN(Date.parse('2026-08-11T14:30:00Z')) + 1 === ngayVN(Date.parse('2026-08-11T23:00:00Z')));

/* ═══════════ D · XẾP HẠNG ═══════════ */
{
  const ds = [{ ma: 'a', ten: 'A', d: 10 }, { ma: 'b', ten: 'B', d: 10 },
              { ma: 'c', ten: 'C', d: 5 }];
  const x = xepHang(ds, (r) => r.d);
  t('cùng điểm thì cùng hạng', x[0].hang === 1 && x[1].hang === 1);
  t('hạng sau nhảy đúng số người đứng trên', x[2].hang === 3);
}

/* ═══════════ E · BÉ NGOÀI TOP VẪN PHẢI THẤY MÌNH ═══════════ */
{
  const rows = Array.from({ length: 40 }, (_, i) =>
    ({ ma: `u${i}`, ten: `Bạn ${i}`, lop: 3, saoTuan: 100 - i, chuoi: 1 }));
  const ds = danhSachHien(rows, 'saoTuan', 'u30');
  t('cắt đúng Top 20', ds.tren.length === 20);
  t('bé hạng 31 vẫn thấy dòng của mình', ds.ngoaiTop === true && ds.con.hang === 31);
  const trongTop = danhSachHien(rows, 'saoTuan', 'u5');
  t('bé trong Top thì không vẽ dòng thừa', trongTop.ngoaiTop === false);
  const laMat = danhSachHien(rows, 'saoTuan', 'chua-co');
  t('bé chưa có trên bảng thì không vẽ dòng trống lửng lơ',
    laMat.con === null && laMat.ngoaiTop === false);

  const kc = khoangCachTren(rows, 'saoTuan', 'u30');
  t('khoảng cách tới người ngay trên đúng', kc.thieu === 1 && kc.ban.ma === 'u29');
  t('bé đang dẫn đầu thì không có ai để đuổi',
    khoangCachTren(rows, 'saoTuan', 'u0') === null);
  /* Ba bạn cùng điểm: người con cần vượt là người ĐIỂM CAO HƠN, không phải bạn cùng
     điểm đứng trên một dòng — nếu không, "còn 0 sao nữa là vượt" là câu vô nghĩa. */
  const hoa = [{ ma: 'x', ten: 'X', saoTuan: 50 }, { ma: 'y', ten: 'Y', saoTuan: 30 },
               { ma: 'z', ten: 'Z', saoTuan: 30 }];
  const kh = khoangCachTren(hoa, 'saoTuan', 'z');
  t('bạn cùng điểm không bị tính là người phải vượt', kh.ban.ma === 'x' && kh.thieu === 20);
}

/* ═══════════ F · ĐUỔI KỊP MỘT BẠN ═══════════ */
{
  const rows = [{ ma: 'long', ten: 'Trí Long', lop: 2, saoTuan: 80 },
                { ma: 'kem', ten: 'Su Kem', lop: 3, saoTuan: 100 }];
  const sk = soKe(rows, 'saoTuan', 'long', 'kem');
  t('so kè: nhận ra ai đang dẫn', sk.dan === 'ban' && sk.cach === 20);
  t('lời nhắn nói bằng VIỆC LÀM ĐƯỢC, có tên bạn',
    loiSoKe(sk, 'sao tuần này').includes('20') && loiSoKe(sk, 'sao').includes('Su Kem'));
  t('con dẫn thì lời nhắn đổi giọng',
    loiSoKe(soKe(rows, 'saoTuan', 'kem', 'long'), 'sao').includes('dẫn'));
  t('hoà nhau thì nói hoà',
    soKe([{ ma: 'a', ten: 'A', saoTuan: 5 }, { ma: 'b', ten: 'B', saoTuan: 5 }],
         'saoTuan', 'a', 'b').dan === 'hoa');
  /* Ba ngả bìa nơi gọi rất dễ quên — quên thì vẽ ra thanh so kè con với chính con. */
  t('chưa chọn ai để đuổi → không vẽ thanh', soKe(rows, 'saoTuan', 'long', null) === null);
  t('tự đuổi chính mình → không vẽ thanh', soKe(rows, 'saoTuan', 'long', 'long') === null);
  t('bạn đã rời bảng → không vẽ thanh', soKe(rows, 'saoTuan', 'long', 'da-xoa') === null);
  t('cả hai cùng 0 sao thì thanh chia đôi, không chia cho 0',
    soKe([{ ma: 'a', ten: 'A', saoTuan: 0 }, { ma: 'b', ten: 'B', saoTuan: 0 }],
         'saoTuan', 'a', 'b').phanTramCon === 50);
}

/* ═══════════ G · LỌC THEO LỚP, VÀ XẾP LẠI TỪ 1 ═══════════ */
{
  const rows = [{ ma: 'a', ten: 'A', lop: 5, saoTuan: 90 },
                { ma: 'b', ten: 'B', lop: 3, saoTuan: 50 },
                { ma: 'c', ten: 'C', lop: 3, saoTuan: 20 }];
  t('lọc lớp 3 lấy đúng hai bạn', locLop(rows, 3).length === 2);
  t('"Cả nhà" giữ nguyên mọi bạn', locLop(rows, 0).length === 3);
  const l3 = xepLai(locLop(rows, 3), 'saoTuan');
  t('bảng của một lớp đánh số lại TỪ 1, không giữ hạng toàn trường',
    l3[0].hang === 1 && l3[0].ma === 'b');

  /* Bộ lọc suy TỪ DỮ LIỆU, không ghim 2·3·4·5: hồ sơ nay cho khai lớp 2 → 12, nên
     ghim cứng là anh lớp 8 có mặt trên bảng mà không ô lọc nào chứa mình. */
  t('bộ lọc chỉ hiện lớp CÓ NGƯỜI, xếp tăng dần',
    dsLop(rows).map((l) => l.ma).join() === '0,3,5');
  t('lớp trên tiểu học cũng có ô lọc của mình',
    dsLop([...rows, { ma: 'x', ten: 'X', lop: 8, saoTuan: 1 }]).some((l) => l.ma === 8));
  /* Một lớp thì nút "Cả nhà" chẳng lọc gì — đừng vẽ ra chiếm chỗ. */
  t('chỉ một lớp thì không vẽ bộ lọc',
    dsLop([{ ma: 'a', ten: 'A', lop: 3 }, { ma: 'b', ten: 'B', lop: 3 }]).length === 0);
  t('bảng rỗng thì không vẽ bộ lọc', dsLop([]).length === 0);
}

/* ═══════════ K · LỚP CON KHAI ĐƯỢC ═══════════
   Bản đầu của màn hồ sơ chỉ cho chọn 4·5·6, nên anh chị lớp 7-12 phải khai sai ngay
   ở màn đầu tiên — mà con số ấy đi thẳng vào bảng xếp hạng lẫn vào bậc xuất phát của
   vòng luyện chủ đề.

   Phép kiểm này TỪNG so với đúng chuỗi '2,3,...,12', và thế là thêm Tiếng Anh lớp 1
   — mở danh sách xuống lớp 1 cho bé 6 tuổi khai đúng lớp mình — là cổng đỏ dù việc
   làm hoàn toàn đúng. Cùng loại "ghim cứng theo hiện trạng" với chuỗi thứ tự kệ
   sách. Nên soi LUẬT chứ không soi danh sách: liền mạch, không trùng, tới hết 12,
   và phủ mọi lớp đang có sách. */
{
  const { LOP_HOC, LOP_MAC_DINH, lopHopLe } = await import('../src/mon/toan/lib/noiDung.js');
  t(`lớp khai được liền mạch tới 12 (${LOP_HOC[0]} → ${LOP_HOC[LOP_HOC.length - 1]})`,
    LOP_HOC.every((g, i) => i === 0 || g === LOP_HOC[i - 1] + 1)
    && LOP_HOC[LOP_HOC.length - 1] === 12);
  {
    const dkFile = new URL('../public/content/chuong_trinh.json', import.meta.url).pathname;
    const lopCoSach = [...new Set(Object.values(
      JSON.parse(readFileSync(dkFile, 'utf8')).chuongTrinh || {},
    ).map((c) => c.lop).filter(Number.isFinite))];
    const thieu = lopCoSach.filter((g) => !LOP_HOC.includes(g));
    t(`phủ mọi lớp đang có sách (${lopCoSach.sort((a, b) => a - b).join('·')})`,
      thieu.length === 0);
  }
  t('lớp mặc định nằm trong danh sách', LOP_HOC.includes(LOP_MAC_DINH));
  t('lớp lạ bị chặn, lùi về mặc định',
    lopHopLe(99) === LOP_MAC_DINH && lopHopLe(0) === LOP_MAC_DINH
    && lopHopLe(null) === LOP_MAC_DINH && lopHopLe('bậy') === LOP_MAC_DINH);
  t('lớp hợp lệ giữ nguyên, nhận cả chuỗi số', lopHopLe(8) === 8 && lopHopLe('11') === 11);

  /* Bậc xuất phát của vòng luyện chủ đề: anh lớp 9 phải vào bậc CAO NHẤT đang có
     (lớp 5), không rơi về bậc thấp hay ra null. */
  const { bacBatDau } = await import('../src/mon/toan/lib/progress.js');
  const thang = [{ lop: 2 }, { lop: 3 }, { lop: 4 }, { lop: 5 }];
  t('lớp trên tiểu học vào bậc cao nhất đang có', bacBatDau(thang, 9) === 5);
  t('lớp 3 vào đúng bậc lớp 3', bacBatDau(thang, 3) === 3);
}

/* ═══════════ H · BA BẢNG, VÀ HUY CHƯƠNG ═══════════ */
t('có đúng ba bảng', BANG.length === 3 && BANG.map((b) => b.ma).join() === 'tuan,chuoi,tong');
t('bảng nào cũng có lời giải thích cho bé đọc', BANG.every((b) => b.mo.length > 20));
t('ba hạng đầu có huy chương, hạng 4 hiện số',
  huyChuong(1) === '🥇' && huyChuong(3) === '🥉' && huyChuong(4) === null);

/* ═══════════ I · NGẢ BÌA ═══════════ */
{
  const rong = buildBangXepHang({ roster: [], attempts: [], now: NOW });
  t('chưa có em nào: không vỡ', rong.rows.length === 0 && rong.soEm === 0);
  const chuaHoc = buildBangXepHang({ roster: [em('u1')], attempts: [], now: NOW });
  t('em chưa học buổi nào vẫn có dòng, 0 sao',
    chuaHoc.rows[0].saoTuan === 0 && chuaHoc.rows[0].chuoi === 0);
  t('đếm đúng số em có học tuần này', chuaHoc.soEmCoHoc === 0);
  t('lượt của tài khoản đã xoá không dựng dòng ma',
    buildBangXepHang({ roster: [em('u1')], attempts: [att('ma-la', NOW)], now: NOW })
      .rows.every((r) => r.cauTuan === 0));
  t('bảng là dữ liệu thuần, đem lưu Firestore được',
    typeof JSON.parse(JSON.stringify(chuaHoc)).generatedAt === 'number');

  /* ── ĐẾM CẢ HAI MÔN ──
     Sao của bài Tiếng Anh phải tính y như sao của bài Toán: `saoTong` cộng theo
     số bài ĐẠT, không hỏi bài ấy thuộc môn nào. Chỗ từng hỏng không nằm ở đây mà
     ở chỗ ĐỌC — `docDuLieuChung` chỉ đọc collection của Toán, nên môn kia có học
     bao nhiêu bảng cũng báo 0. Nên kiểm cả hai: phép cộng, và chỗ đọc. */
  const caHai = buildBangXepHang({
    roster: [em('u1')], now: NOW,
    progress: { u1: { 'DL:KSN2.B01': { pass: true }, 'DL:TA1.B01': { pass: true } } },
  });
  t('bài Tiếng Anh cũng ra sao như bài Toán',
    caHai.rows[0].saoTong === 2 * SAO.baiDat);

  const nen = readFileSync(new URL('../functions/index.js', import.meta.url), 'utf8');
  t('chỗ đọc dữ liệu có lấy sổ tiến độ Tiếng Anh', nen.includes('progressTA/${r.uid}/micros'));
  t('chỗ đọc dữ liệu có lấy học bạ Tiếng Anh', nen.includes('hocBaTA/${r.uid}/muc'));
}

console.log(`\n   ${BANG.length} bảng · sao: câu ${SAO.cauDung} · bài ${SAO.baiDat}`
  + ` · huy hiệu ${SAO.huyHieu} · vòng đấu ${SAO.vongDau} · trần ${TRAN_SAO_NGAY}/ngày`);
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
