/**
 * LỚP 3 — đường lùi về lớp 2 có trỏ đúng chỗ không.
 * chạy: node test/lop3.test.mjs
 *
 * Bảng `data/lop3_gan_lop2.json` là đường LÙI: học lớp 3 mà đuối thì quay về luyện
 * lại bài lớp 2 cùng chủ đề. Trỏ sai còn tệ hơn không trỏ — bé bấm vào rồi lạc sang
 * một bài chẳng liên quan, mất niềm tin vào chính cái nút ấy.
 *
 * Ba điều máy khẳng định được: bài lớp 2 được trỏ tới phải CÓ THẬT; mọi bài lớp 3
 * đều phải có một dòng trong bảng (kể cả dòng nói "không có bài tương ứng" — im lặng
 * bỏ trống thì không phân biệt được "chưa làm" với "đã xét và kết luận là không có");
 * và căn cứ phải là một trong ba giá trị đã khai.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const BANG = join(G, 'data/lop3_gan_lop2.json');
t('bảng đường lùi có thật', existsSync(BANG));
const b = JSON.parse(readFileSync(BANG, 'utf8'));
const gan = b.gan || {};

/* bài lớp 2 được trỏ tới phải có tệp thật */
const coL2 = new Set(readdirSync(join(G, 'data/lop2'))
  .filter((f) => f.startsWith('DL_KSN2_'))
  .map((f) => f.replace('.json', '').replace('DL_KSN2_', 'DL:KSN2.')));
const lac = [];
for (const [ma, v] of Object.entries(gan)) {
  for (const ve of v.ve || []) if (!coL2.has(ve)) lac.push(`${ma} → ${ve} (không có bài này)`);
}
t(`mọi đích đến đều là bài lớp 2 CÓ THẬT (${coL2.size} bài)`, lac.length === 0);
in5(lac);

/* đủ 34 bài lớp 3, không sót dòng nào */
const thieu = [];
for (let i = 1; i <= 34; i += 1) {
  const ma = `DL:KSN3.B${String(i).padStart(2, '0')}`;
  if (!gan[ma]) thieu.push(ma);
}
t(`đủ 34 bài lớp 3 trong bảng (${Object.keys(gan).length})`, thieu.length === 0);
in5(thieu);

/* căn cứ phải nằm trong ba giá trị đã khai ở `_canCu` */
const hopLe = new Set(Object.keys(b._canCu || {}));
const sai = Object.entries(gan).filter(([, v]) => !hopLe.has(v.canCu)).map(([k]) => k);
t(`căn cứ nào cũng được khai nghĩa (${[...hopLe].join(' · ')})`, sai.length === 0);
in5(sai);

/* dòng "khong" phải RỖNG đích đến — khai không có mà vẫn trỏ đi đâu đó là mâu thuẫn */
const mauThuan = Object.entries(gan)
  .filter(([, v]) => v.canCu === 'khong' && (v.ve || []).length > 0).map(([k]) => k);
t('dòng "không có bài tương ứng" thì không trỏ đi đâu cả', mauThuan.length === 0);
in5(mauThuan);

const theoCanCu = Object.values(gan).reduce((a, v) => {
  a[v.canCu] = (a[v.canCu] || 0) + 1; return a;
}, {});
console.log('   căn cứ:', Object.entries(theoCanCu).map(([k, v]) => `${k} ${v}`).join(' · '));

/* ── bản trích thô: mốc bất biến, mất chữ ở đây thì mọi bước sau đều thiếu ── */
const THO = join(G, 'data/lop3_tho.json');
let soTho = new Set();          /* mã 34 bài có thật — mọi đích đến đều phải nằm trong đây */
if (existsSync(THO)) {
  const d = JSON.parse(readFileSync(THO, 'utf8'));
  const bai = d.bai || [];
  t(`trích đủ 34 bài (${bai.length})`, bai.length === 34);
  const MUC = ['mucTieu', 'chuyenMoBai', 'khamPha', 'viDuMau',
               'suKemNham', 'luyenTap', 'quiz', 'gocBoMe'];
  const thieuMuc = bai.filter((b) => MUC.some((m) => !b.muc?.[m])).map((b) => b.so);
  t('bài nào cũng đủ 8 mục ①…⑧', thieuMuc.length === 0);
  in5(thieuMuc);
  /* Mỗi bài 5 câu quiz — sách nói vậy, và nhiệt kế cũng 5 mức. Lệch là mẫu tách
     câu bỏ sót: lớp 2 từng mất 165 câu quiz vì mẫu chỉ nhận dấu chấm. */
  const saiQuiz = bai.filter((b) => (b.cau || []).filter((c) => c.phan === 'quiz').length !== 5)
    .map((b) => `B${b.so}`);
  t('bài nào cũng đúng 5 câu quiz', saiQuiz.length === 0);
  in5(saiQuiz);
  /* `hatMam` là đường lùi về lớp 2 — thiếu là mất luôn lý do tồn tại của bảng gán */
  const khongHatMam = bai.filter((b) => !b.hatMam).map((b) => `B${b.so}`);
  t('bài nào cũng có HẠT MẦM NĂM NGOÁI', khongHatMam.length === 0);
  in5(khongHatMam);
  /* mã bài trong bảng đường lùi phải khớp số bài có thật trong bản trích */
  soTho = new Set(bai.map((b) => `DL:KSN3.B${String(b.so).padStart(2, '0')}`));
  const lechBang = Object.keys(gan).filter((k) => !soTho.has(k));
  t('bảng đường lùi không trỏ từ bài lớp 3 không có thật', lechBang.length === 0);
  in5(lechBang);
  console.log(`   ${bai.length} bài · ${bai.reduce((a, b) => a + (b.cau || []).length, 0)} câu`
    + ` · ${bai.reduce((a, b) => a + (b.sauBai || []).length, 0)} dòng ôn tập/ải/đáp án`);
}

/* ── đáp án: phải khớp 1:1 với câu hỏi ──
   Lớp 2 từng có 60 lời giải gắn SAI CÂU vì đáp án ôn tập cũng đánh C1, C2… và
   ghi đè lên đáp án bài (bẫy 6). Kiểu hỏng ấy không làm app vỡ, không làm số
   liệu lệch — chỉ làm bé đọc lời giải của một câu khác. Chỉ đếm khớp mới bắt được. */
const DA = join(G, 'data/lop3_dapan.json');
if (existsSync(THO) && existsSync(DA)) {
  const tho = JSON.parse(readFileSync(THO, 'utf8')).bai || [];
  const da = JSON.parse(readFileSync(DA, 'utf8'));
  const lech = [];
  for (const b of tho) {
    const ma = `DL:KSN3.B${String(b.so).padStart(2, '0')}`;
    for (const [phan, key] of [['luyenTap', 'luyenTap'], ['quiz', 'quiz']]) {
      const hoi = (b.cau || []).filter((c) => c.phan === phan).map((c) => c.maSach);
      const dap = Object.keys(da[ma]?.[key] || {});
      const thieuDap = hoi.filter((x) => !dap.includes(x));
      const thuaDap = dap.filter((x) => !hoi.includes(x));
      if (thieuDap.length) lech.push(`${ma} ${phan}: thiếu đáp án ${thieuDap.join(',')}`);
      if (thuaDap.length) lech.push(`${ma} ${phan}: thừa đáp án ${thuaDap.join(',')} (đè từ ôn tập?)`);
    }
  }
  t('mọi câu hỏi đều có đáp án, và không đáp án nào thừa', lech.length === 0);
  in5(lech);
  const n = Object.values(da).reduce((a, v) =>
    a + Object.keys(v.luyenTap || {}).length + Object.keys(v.quiz || {}).length, 0);
  console.log(`   ${Object.keys(da).length} bài · ${n} đáp án`);
}

/* ── ôn tập & ải: mối nối "sai câu nào, ôn bài đó" ──
   Bộ tách đầu tiên nhận nhầm dòng BẢNG TỰ SOI thành câu hỏi — 5/8 ôn tập thừa 1-5
   câu. Cái thừa thì bộ đếm kêu; cái THIẾU đi kèm mới nguy: mối nối trượt là câu ấy
   mất đường về bài, hoặc tệ hơn, cả ôn tập tụt xuống "suy theo chương" và trỏ mỗi
   câu về cả 5 bài. Bé bấm vào rồi phải tự đoán học lại bài nào — đúng cái việc mà
   nút này sinh ra để khỏi phải làm. */
const ON = join(G, 'data/lop3_ontap.json');
if (existsSync(ON)) {
  const o = JSON.parse(readFileSync(ON, 'utf8'));
  const khoi = Object.values(o.khoi || {});
  const on = khoi.filter((v) => v.loai === 'onTap');
  t(`đủ 8 ôn tập và 3 ải (${on.length} · ${khoi.length - on.length})`,
    on.length === 8 && khoi.length - on.length === 3);

  const ten = (v) => `${v.loai === 'onTap' ? 'Ôn tập' : 'Ải'} ${v.so}`;
  /* số câu tách được phải bằng con số chính sách nêu ("Đạt 8/10", "Phá 6/8 vụ án") */
  const lechSo = khoi.filter((v) => (v.cau || []).length !== v.tong)
    .map((v) => `${ten(v)}: tách ${v.cau.length}, sách nói ${v.tong}`);
  t('số câu mỗi khối khớp con số sách nêu', lechSo.length === 0);
  in5(lechSo);

  /* số câu liền mạch 1…n — thủng một số là mẫu bỏ sót đúng câu ấy */
  const thung = khoi.filter((v) => (v.cau || []).some((c, i) => c.so !== i + 1))
    .map((v) => ten(v));
  t('số câu chạy liền mạch 1…n', thung.length === 0);
  in5(thung);

  /* dòng bảng tự soi lọt vào làm câu hỏi — kiểu hỏng gốc. Dấu nhận biết KHÔNG phải
     mũi tên: sách dùng → ngay trong đề ("Bán kính 4 cm → đường kính?"). Chỉ mũi tên
     TRỎ TỚI MỘT SỐ BÀI mới là mối nối. */
  const lot = khoi.flatMap((v) => (v.cau || []).concat(v.cauDeB || [])
    .filter((c) => /→[^→]*Bài\s*\d/.test(c.text))
    .map((c) => `${ten(v)} ${c.id}: ${c.text.slice(0, 60)}`));
  t('không dòng bảng tự soi nào lọt vào làm câu hỏi', lot.length === 0);
  in5(lot);

  /* sách chỉ đích danh từng câu — phải đọc được, không được tụt xuống suy theo chương */
  const phaiSuy = on.filter((v) => v.canCu !== 'sach').map((v) => ten(v));
  t('mọi ôn tập đều đọc được mối nối SÁCH CHỈ ĐÍCH DANH', phaiSuy.length === 0);
  in5(phaiSuy);

  /* mọi câu có đường về, và đích đến phải là bài lớp 3 CÓ THẬT */
  const hong = [];
  for (const v of on) {
    for (const c of v.cau || []) {
      const ve = v.veCau?.[c.id] || [];
      if (!ve.length) hong.push(`${ten(v)} ${c.id}: không trỏ về bài nào`);
      for (const x of ve) if (!soTho.has(x)) hong.push(`${ten(v)} ${c.id} → ${x} (không có bài này)`);
    }
  }
  t('mọi câu ôn tập đều trỏ về một bài lớp 3 có thật', hong.length === 0);
  in5(hong);

  /* đề B là thứ bé làm khi chưa đạt — thiếu câu nào là chỗ ấy không luyện lại được */
  const lechB = on.filter((v) => (v.cauDeB || []).length !== v.tong)
    .map((v) => `${ten(v)}: đề B ${v.cauDeB.length} câu, đề chính ${v.tong}`);
  t('đề B đủ câu như đề chính', lechB.length === 0);
  in5(lechB);

  console.log(`   ${on.length} ôn tập · ${khoi.length - on.length} ải`
    + ` · ${khoi.reduce((a, v) => a + v.cau.length, 0)} câu`
    + ` · ${khoi.reduce((a, v) => a + v.cauDeB.length, 0)} câu đề B`);
}

/* ── bài đã dựng (data/lop3) — thứ phòng học sẽ đọc ── */
const BAI = join(G, 'data/lop3');
if (existsSync(BAI)) {
  const tep = readdirSync(BAI).filter((f) => f.startsWith('DL_KSN3_'));
  const bai = tep.map((f) => JSON.parse(readFileSync(join(BAI, f), 'utf8')));
  t(`dựng đủ 34 bài (${bai.length})`, bai.length === 34);

  /* mã bài phải khớp bản trích — lệch là phòng học mở ra bài không có thật */
  const laMa = bai.filter((b) => !soTho.has(b.id)).map((b) => b.id);
  t('mã bài nào cũng có trong bản trích', laMa.length === 0);
  in5(laMa);

  /* lời chữa: sách có đáp án cho cả 477 câu, mất câu nào là bé làm xong không so được */
  const khongLoi = bai.flatMap((b) => (b.cau || [])
    .filter((c) => !c.loiChua && !c.answerKey && !c.solutionNarrative)
    .map((c) => `${b.id} ${c.id}`));
  t('câu nào cũng có lời chữa hoặc đáp án', khongLoi.length === 0);
  in5(khongLoi);

  /* Chấm máy chỉ được phép khi CHẮC. Trắc nghiệm phải có đáp án nằm trong chính
     danh sách phương án của đề — lệch một chữ là bé chọn đúng mà máy báo sai, và
     bé thì tin máy chứ không tin mình. */
  const chamHong = bai.flatMap((b) => (b.cau || []).filter((c) => c.format === 'mcq')
    .filter((c) => !(c.choices || []).includes(c.answerKey?.choice))
    .map((c) => `${b.id} ${c.id}: đáp án ${JSON.stringify(c.answerKey)} không có trong ${JSON.stringify(c.choices)}`));
  t('đáp án trắc nghiệm nào cũng nằm trong phương án của đề', chamHong.length === 0);
  in5(chamHong);

  /* HẠT MẦM và đường LÙI — hai thứ lớp 2 không có, và là lý do quyển này nối được
     với quyển trước. Thiếu lặng lẽ thì app vẫn chạy, chỉ mất mối nối giữa hai năm. */
  const khongMam = bai.filter((b) => !b.hatMam).map((b) => b.id);
  t('bài nào cũng có HẠT MẦM NĂM NGOÁI', khongMam.length === 0);
  in5(khongMam);

  const luiHong = [];
  for (const b of bai) {
    const g = b.ganLop2 || {};
    if (!hopLe.has(g.canCu)) luiHong.push(`${b.id}: căn cứ lạ "${g.canCu}"`);
    /* khai "không có bài tương ứng" mà vẫn trỏ đi đâu đó là mâu thuẫn; ngược lại,
       khai có mà danh sách rỗng thì nút hiện ra rồi bấm chẳng tới đâu */
    if (g.canCu === 'khong' && (g.ve || []).length) luiHong.push(`${b.id}: khai "khong" mà vẫn trỏ`);
    if (g.canCu !== 'khong' && !(g.ve || []).length) luiHong.push(`${b.id}: khai có mà không trỏ đâu`);
    for (const x of g.ve || []) if (!coL2.has(x)) luiHong.push(`${b.id} → ${x} (không có bài lớp 2 này)`);
    if ((g.ve || []).length !== (g.ten || []).length) luiHong.push(`${b.id}: số đích và số tên lệch nhau`);
  }
  t('đường lùi về lớp 2 trỏ đúng và không tự mâu thuẫn', luiHong.length === 0);
  in5(luiHong);

  /* đường lùi phải chép ĐỦ đích, không cắt còn một. Bài 4, 16, 18 mỗi bài do sách
     chỉ đích danh HAI bài lớp 2 — lấy mỗi cái đầu là bỏ mất nửa đường về. */
  const hai = bai.filter((b) => (b.ganLop2?.ve || []).length > 1).length;
  t(`giữ đủ đích kép (${hai} bài trỏ về 2 bài lớp 2)`, hai === 3);

  const cham = bai.reduce((a, b) => a + b.cau.filter((c) => c.answerKey).length, 0);
  console.log(`   ${bai.length} bài · ${bai.reduce((a, b) => a + b.cau.length, 0)} câu`
    + ` · chấm máy ${cham} · có đường lùi ${bai.filter((b) => b.ganLop2?.ve?.length).length}`);
}

/* ── hình vẽ: bản mô tả, ảnh thật và sổ tay phải nói CÙNG một chuyện ──
   Kiểu hỏng đắt nhất ở đây không làm gì vỡ: sửa `params` mà quên vẽ lại thì dữ
   liệu nói một đằng ảnh hiện một nẻo, và cả hai đều hợp lệ (bẫy 20). Nên phép
   kiểm phải so bằng mã băm, không so bằng "có tệp hay không". */
const MOTA = join(G, 'data/lop3_hinh.json');
const SOTAY = join(G, 'data/lop3_hinh_manifest.json');
if (existsSync(MOTA) && existsSync(SOTAY)) {
  const mota = JSON.parse(readFileSync(MOTA, 'utf8'));
  const sotay = JSON.parse(readFileSync(SOTAY, 'utf8'));
  const FIG = join(G, 'web/public/content/figures');

  /* Trùng mã thì hình sau ĐÈ hình trước và cái mất đi không kêu ca gì — chỉ lộ ra
     nhờ bộ đếm lệch. Tôi đã dính đúng thế khi đặt L3H_BT01 cho hai hình khác nhau. */
  const dem = {};
  for (const m of mota) dem[m.id] = (dem[m.id] || 0) + 1;
  const trung = Object.entries(dem).filter(([, n]) => n > 1).map(([k]) => k);
  t('không hai hình nào trùng mã', trung.length === 0);
  in5(trung);

  /* Sổ tay chỉ THÊM nên mã đã bỏ vẫn nằm lại, trỏ vào ảnh không còn — bước gắn
     hình đọc sổ tay nên nó sẽ đòi một tệp đã xoá. So hai chiều mới bắt được. */
  const thieu = mota.filter((m) => !sotay[m.id]).map((m) => m.id);
  t(`mọi hình đã mô tả đều có trong sổ tay (${mota.length})`, thieu.length === 0);
  in5(thieu);
  const thua = Object.keys(sotay).filter((k) => !mota.some((m) => m.id === k));
  t('sổ tay không giữ lại mã đã bỏ', thua.length === 0);
  in5(thua);

  /* Mỗi bài một hình MÀN MỞ — chuẩn mục 10 bắt buộc, và lớp 2 trả giá cả một lượt
     vì lượt đầu chỉ nghĩ tới hình giảng. */
  const coMo = new Set(mota.filter((m) => m.muc === 'chuyenMoBai').map((m) => m.bai));
  const khongMo = [];
  for (let i = 1; i <= 34; i += 1) {
    const ma = `DL:KSN3.B${String(i).padStart(2, '0')}`;
    if (!coMo.has(ma)) khongMo.push(ma);
  }
  t(`bài nào cũng có hình màn mở (${coMo.size}/34)`, khongMo.length === 0);
  in5(khongMo);

  /* …và ít nhất một hình GIẢNG. Chặng giảng không hình thì lời văn treo lơ lửng ở
     dấu hai chấm — sách lớp 3 chỉ cho sẵn 6 hình giảng cho 34 bài, phần còn lại
     phải tự dựng, nên chỗ này rất dễ tưởng xong mà chưa xong. */
  const coGiang = new Set(mota.filter((m) => m.muc === 'khamPha').map((m) => m.bai));
  const khongGiang = [];
  for (let i = 1; i <= 34; i += 1) {
    const ma = `DL:KSN3.B${String(i).padStart(2, '0')}`;
    if (!coGiang.has(ma)) khongGiang.push(ma);
  }
  t(`bài nào cũng có hình giảng (${coGiang.size}/34)`, khongGiang.length === 0);
  in5(khongGiang);

  /* Hình giảng neo theo THỨ TỰ BƯỚC. Neo quá số bước thật thì bộ gắn dừng hẳn,
     nhưng bắt sớm ở đây thì biết ngay hình nào sai thay vì đọc log bộ gắn. */
  const buocQua = mota.filter((m) => m.muc === 'khamPha' && (m.neoBuoc || 0) > 6)
    .map((m) => `${m.id}: neoBuoc ${m.neoBuoc}`);
  t('không hình giảng nào neo vào bước quá xa', buocQua.length === 0);
  in5(buocQua);

  const lechSha = [];
  for (const [id, h] of Object.entries(sotay)) {
    const png = join(FIG, id + '.png');
    if (!existsSync(png)) { lechSha.push(`${id}: thiếu ảnh`); continue; }
    const sha = createHash('sha256').update(readFileSync(png)).digest('hex').slice(0, 16);
    if (sha !== h.sha256_16) lechSha.push(`${id}: ảnh lệch sổ tay — vẽ lại`);
  }
  t('ảnh thật khớp mã băm ghi trong sổ tay', lechSha.length === 0);
  in5(lechSha);

  /* Tiêu đề quá dài biến thành đoạn văn đè kín đầu hình — 122 hình lớp 5 từng
     dính, mà phần hình bên dưới vẫn vẽ đẹp nên nhìn lướt không thấy sai. */
  const daiQua = mota.filter((m) => (m.params?.title || '').length > 120
    || (m.params?.note || '').length > 120).map((m) => m.id);
  t('tiêu đề và dòng chốt đều dưới 120 chữ', daiQua.length === 0);
  in5(daiQua);

  /* Câu nào có hình ĐỀ thì BẮT BUỘC có hình lời giải. Bỏ hình lời giải thì bé
     làm xong vẫn không biết mình sót cái nào.

     Chiều ngược lại KHÔNG phải lỗi: câu "vẽ hai hình tròn cùng tâm O" chỉ có hình
     giải, vì vẽ sẵn ra là làm hộ bé đúng cái việc đề bảo bé làm. Luật đầu tôi viết
     đòi đủ cặp cả hai chiều nên đỏ oan đúng câu ấy — đề đã tả trọn bằng lời thì
     không cần hình đề. */
  const theoCau = {};
  for (const m of mota) {
    if (!m.neoCau) continue;
    const k = `${m.bai}#${m.neoCau}`;
    (theoCau[k] ||= []).push(m.vaiTro === 'giai' ? 'giai' : 'de');
  }
  const leCap = Object.entries(theoCau)
    .filter(([, v]) => v.includes('de') && !v.includes('giai'))
    .map(([k]) => `${k}: có hình đề mà không có hình lời giải`);
  t('câu nào có hình đề thì cũng có hình lời giải', leCap.length === 0);
  in5(leCap);

  /* Bản ĐỀ không được chứa đáp án. Với hình lưới diện tích, `hienTich` in sẵn
     "6 × 4 = 24 cm²" — để bật ở bản đề là bé khỏi phải đếm ô nào. */
  const loDap = mota.filter((m) => m.neoCau && m.vaiTro !== 'giai')
    .filter((m) => (m.params?.hinh || []).some((h) => h.hienTich))
    .map((m) => m.id);
  t('hình ĐỀ không in sẵn đáp án', loDap.length === 0);
  in5(loDap);

  /* Lịch tháng tự mâu thuẫn: cột được tô phải đúng là thứ của các ngày làm nổi.
     Bản đầu tôi nhập batDau sai nên 6·13·20·27 rơi cột thứ Hai trong khi nhãn
     cột và lời chú đều nói Chủ nhật — hình vẽ đẹp mà dạy sai một sự thật. */
  const THU = ['Hai', 'Ba', 'Tư', 'Năm', 'Sáu', 'Bảy', 'CN'];
  const lechLich = [];
  for (const m of mota.filter((x) => x.arch === 'lich_thang')) {
    const { batDau = 0, cot, toDam = [] } = m.params || {};
    if (cot === undefined) continue;
    for (const ngay of toDam) {
      const c = (batDau + ngay - 1) % 7;
      if (c !== cot) lechLich.push(`${m.id}: ngày ${ngay} là ${THU[c]}, không phải ${THU[cot]}`);
    }
  }
  t('lịch tháng: ngày làm nổi đúng cột đã tô', lechLich.length === 0);
  in5(lechLich);

  const capBaiTap = Object.keys(theoCau).length;
  console.log(`   ${mota.length} hình · ${new Set(mota.map((m) => m.arch)).size} nguyên mẫu`
    + ` · ${new Set(mota.map((m) => m.bai)).size} bài · ${capBaiTap} câu có hình đề+giải`);
}

/* ── bước 5 · bản cho app theo khuôn chung ──
   Đây là thứ phòng học ĐỌC THẬT. Bản gốc đúng mà bản này hỏng thì bé chịu, chứ
   không ai biết — hai thư mục cố tình khác nhau nên không so thẳng được. */
const APP = join(G, 'web/public/content/lop3');
if (existsSync(APP)) {
  const tep = readdirSync(APP).filter((f) => f.startsWith('DL_KSN3_B'));
  const app = tep.map((f) => JSON.parse(readFileSync(join(APP, f), 'utf8')));
  t(`dựng đủ 34 bài cho app (${app.length})`, app.length === 34);

  const saiLop = app.filter((b) => b.grade !== 3 || b.quyen !== 'lop3').map((b) => b.id);
  t('bài nào cũng khai đúng lớp 3', saiLop.length === 0);
  in5(saiLop);

  /* CHẶNG GIẢNG RỖNG LÀ HỎNG CÂM: bài vẫn dựng, phòng học vẫn mở, chỉ là không dạy
     gì. Sách lớp 3 đặt tên bước mười kiểu (Nhân vật · Phép thử · Thế trận · Kho
     báu…); mẫu bốn tên của lớp 2 làm 7 bài mất sạch nguyên tắc và 26 bước bốc hơi
     mà không một dòng cảnh báo. Phép kiểm này canh đúng chỗ ấy. */
  const rong = app.filter((b) => !(b.knowledgeCore?.statements || []).length)
    .map((b) => `${b.id} — mẫu tên bước bỏ sót cách sách đặt tên?`);
  t('bài nào cũng có ít nhất một nguyên tắc để dạy', rong.length === 0);
  in5(rong);

  const khongMan = app.filter((b) => !(b.lecture?.screens || []).length).map((b) => b.id);
  t('bài nào cũng có màn giảng', khongMan.length === 0);
  in5(khongMan);

  /* `duongLui` chỉ ghi khi thật sự có đích — trường rỗng thì giao diện phải đoán
     "chưa làm" hay "đã xét và không có". Và đích phải là bài lớp 2 CÓ THẬT. */
  const luiHong = [];
  for (const b of app) {
    const dl = b.duongLui;
    if (!dl) continue;
    if (!(dl.ve || []).length) luiHong.push(`${b.id}: có trường duongLui mà rỗng`);
    for (const x of dl.ve || []) if (!coL2.has(x)) luiHong.push(`${b.id} → ${x} không có thật`);
  }
  t(`đường lùi trong bản app trỏ đúng (${app.filter((b) => b.duongLui).length}/34 bài)`,
    luiHong.length === 0);
  in5(luiHong);

  /* HẠT MẦM phải theo sang bản app — nó là lời nối ngược về lớp 2 ở màn kết bài */
  const mam = app.filter((b) => b.hatMam).length;
  t(`hạt mầm theo sang bản app đủ 34 bài (${mam})`, mam === 34);
}

/* ── kỳ sát hạch (8 ôn tập + 3 ải) ── */
const REV = join(G, 'web/public/content/reviews');
if (existsSync(REV)) {
  const ky = readdirSync(REV).filter((f) => f.startsWith('DCR_KSN3_C'))
    .map((f) => JSON.parse(readFileSync(join(REV, f), 'utf8')));
  t(`đủ 11 kỳ sát hạch (${ky.length})`, ky.length === 11);

  /* Không đáp án thì bé làm xong chẳng có gì để so — mà kỳ thi vẫn chạy trơn tru */
  const khongDap = ky.flatMap((k) => (k.examA || []).filter((c) => !c.answer)
    .map((c) => `${k.id} ${c.id}`));
  t('câu sát hạch nào cũng có đáp án', khongDap.length === 0);
  in5(khongDap);

  /* Mối nối "sai câu nào, ôn bài đó" — thứ đáng giá nhất của phần ôn tập. Ải thì
     phủ cả sách nên không trỏ riêng bài nào, đó là cố ý. */
  const noiHong = [];
  for (const k of ky) {
    for (const c of k.examA || []) {
      if (k.loai === 'ai') continue;
      if (!c.diagnosesMicro) { noiHong.push(`${k.id} ${c.id}: không trỏ về bài nào`); continue; }
      if (!soTho.has(c.diagnosesMicro)) noiHong.push(`${k.id} ${c.id} → ${c.diagnosesMicro} không có thật`);
      for (const v of c.veBai || []) {
        if (!soTho.has(v.id)) noiHong.push(`${k.id} ${c.id} → ${v.id} không có thật`);
        if (!v.ten) noiHong.push(`${k.id} ${c.id} → ${v.id} thiếu tên bài để hiện cho bé`);
      }
    }
  }
  t('mọi câu ôn tập trỏ về một bài lớp 3 có thật, kèm tên', noiHong.length === 0);
  in5(noiHong);

  /* Một câu trỏ về HAI bài là chuyện thật (ôn tập 3 câu 10, ôn tập 4 câu 12).
     Khuôn lớp 5 chỉ có một ô `diagnosesMicro`, nên `veBai` phải giữ đủ danh sách —
     rơi mất đích thứ hai thì bé ôn nửa vời mà không ai biết. */
  const kep = ky.flatMap((k) => (k.examA || []).filter((c) => (c.veBai || []).length > 1)).length;
  t(`giữ đủ đích kép trong kỳ sát hạch (${kep} câu trỏ về 2 bài)`, kep === 2);

  /* HAI QUYỂN PHẢI DÙNG CHUNG MỘT CÁCH VIẾT. Bản gốc lớp 3 ghi `loai: 'onTap'`,
     lớp 2 ghi `'ontap'`, mà giao diện lọc theo `'ontap'` — lệch một chữ hoa là cả 8
     ôn tập lớp 3 biến mất khỏi màn hình: dữ liệu vẫn đủ, tệp vẫn đúng, chỉ là không
     ai thấy. So thẳng bộ từ vựng của hai quyển mới bắt được. */
  const tu2 = new Set(JSON.parse(readFileSync(join(G, 'web/public/content/lop2/ontap.json'), 'utf8'))
    .map((x) => x.loai));
  const tu3 = new Set(JSON.parse(readFileSync(join(G, 'web/public/content/lop3/ontap.json'), 'utf8'))
    .map((x) => x.loai));
  const la = [...tu3].filter((x) => !tu2.has(x));
  t(`lớp 3 dùng cùng bộ từ 'loai' với lớp 2 (${[...tu3].join(' · ')})`, la.length === 0);
  in5(la);

  const cauB = ky.reduce((a, k) => a + (k.deB || []).length, 0);
  console.log(`   ${ky.length} kỳ · ${ky.reduce((a, k) => a + k.examA.length, 0)} câu`
    + ` · ${cauB} câu đề B`);
}

/* ── sổ đăng ký: không khai thì lớp 3 không hiện trên kệ sách ── */
const DK = join(G, 'web/public/content/chuong_trinh.json');
if (existsSync(DK)) {
  const dk = JSON.parse(readFileSync(DK, 'utf8')).chuongTrinh || {};
  const l3 = dk.lop3;
  t('sổ đăng ký có khai lớp 3', !!l3);
  if (l3) {
    /* `loai` và `donVi` là hai trường hay quên nhất (chuẩn mục 10 · bước 6):
       thiếu `loai: hoc` thì App không mở Home của lớp mà nhảy thẳng bảng đấu. */
    t("lớp 3 khai loai: 'hoc' và donVi", l3.loai === 'hoc' && !!l3.donVi);
    t(`lớp 3 khai đủ 34 bài (${l3.soBai})`, l3.soBai === 34 && (l3.bai || []).length === 34);
    const laMa = (l3.bai || []).filter((x) => !soTho.has(x));
    t('mã bài trong sổ đăng ký đều có thật', laMa.length === 0);
    in5(laMa);
    t('lớp 2 và lớp 5 vẫn còn nguyên trong sổ',
      !!dk.lop2 && !!dk.lop5 && !!dk.lop5q2);
  }
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
