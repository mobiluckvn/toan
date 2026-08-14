/**
 * LỚP 4 — cổng nghiệm thu riêng của quyển.
 * chạy: node test/lop4.test.mjs  (hoặc `npm test`, nó quét cả thư mục)
 *
 * Soi loại lỗi HỎNG MÀ KHÔNG BÁO — lỗi làm app vỡ thì tự thấy, không cần kiểm.
 * Danh sách theo chuẩn mục 8, cộng bốn phép riêng của quyển này:
 *
 *   · bẫy 5/6 — ôn tập và ĐÁP ÁN CHI TIẾT của cả chương rơi vào mục ⑩ của bài cuối.
 *     Đã dính thật trong đợt này: 11 bài, 121-155 dòng rác mỗi bài, lộ nguyên đáp án
 *     cho người lớn đọc, mà mọi phép ĐẾM CÂU vẫn đúng nên không có gì kêu.
 *   · đường lùi HAI TẦNG — lớp 4 → lớp 3 và lớp 5 → lớp 4. Trỏ sai còn tệ hơn không
 *     trỏ: bé bấm vào rồi lạc sang một bài chẳng liên quan.
 *   · `Bài n` TRẦN trong HẠT MẦM là bài LỚP 4, không phải lớp 3 — mẫu bắt mọi `Bài n`
 *     cho ra 18 dòng trỏ ngược vào chính lớp 4 và một dòng trỏ ra ngoài phạm vi.
 *   · hình màn mở phải là bản ĐỀ — không chứa dấu vết đáp án (chuẩn mục 6 luật 3).
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const G = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));
const doc = (p) => JSON.parse(readFileSync(p, 'utf8'));

const GOC = join(G, 'data/lop4');
const APP = join(G, 'web/public/content/lop4');
const teps = readdirSync(GOC).filter((f) => /^DL_KSN4_B\d+\.json$/.test(f));
const bais = teps.map((f) => doc(join(GOC, f))).sort((a, b) => a.so - b.so);

/* ══ 1 · đủ số bài · đủ mục · số câu khớp ══ */
/* ⚠ SỐ BÀI ĐỔI 44 → 49 NGÀY 14-08. Bác đọc Bài 13 cũ ("DÃY SỐ CÁCH ĐỀU") thấy khó
   hiểu; soi ra thì một bài nhồi BỐN công thức, và không bài nào của cả quyển định
   nghĩa một khái niệm nào (`vocabulary` rỗng ở 44/44). Cụm dãy số tách thành năm bài
   — khái niệm · thứ n · đếm · tổng · thuộc dãy — nên B13 cũ lùi thành B18, và 31 bài
   sau đó dồn theo. Xem `tools/day_so_lop4.py` và `tools/don_so_lop4.py`.

   Ba con số dưới đây là ĐẾM, không phải luật — nới chúng khi thêm bài là đúng. Nhưng
   phải nới CÙNG LÚC cả ba, và giữ nguyên phép "liền mạch": số bài rời rạc thì bé mở
   quyển thấy nhảy cóc Bài 12 sang Bài 18, mà không có gì báo. */
const SO_BAI = 60;
const SO_CAU = SO_BAI * 14;      // mỗi bài đúng 9 luyện tập + 5 quiz

t(`đủ ${SO_BAI} bài (${bais.length})`, bais.length === SO_BAI);
t(`số thứ tự bài liền mạch 1..${SO_BAI}`,
  bais.every((b, i) => b.so === i + 1));
t('đủ 11 chương', new Set(bais.map((b) => b.chuong)).size === 11);

const MUC = ['mucTieu', 'chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi',
  'viDuMau', 'suKemNham', 'luyenTap', 'quiz', 'gocBoMe'];
const thieuMuc = [];
for (const b of bais) {
  for (const m of MUC) if (!b.muc[m]) thieuMuc.push(`bài ${b.so} thiếu mục ${m}`);
}
t('bài nào cũng đủ 10 mục ①…⑩', thieuMuc.length === 0);
in5(thieuMuc);

const lechCau = bais.filter((b) => {
  const lt = b.cau.filter((c) => c.phan === 'luyenTap').length;
  const qz = b.cau.filter((c) => c.phan === 'quiz').length;
  return lt !== 9 || qz !== 5;
});
t('bài nào cũng đúng 9 luyện tập + 5 quiz', lechCau.length === 0);
in5(lechCau.map((b) => `bài ${b.so}`));

const tongCau = bais.reduce((s, b) => s + b.cau.length, 0);
t(`đủ ${SO_CAU} câu (${tongCau})`, tongCau === SO_CAU);

/* ══ 2 · KHÔNG lẫn phần khác vào bài — bẫy 5 và 6 ══ */
const RAC = /^(ĐÁP ÁN|ÔN TẬP \d+|✦\s+(BẢNG TỰ SOI|ĐỀ B)|B\d+\s+ĐÁP ÁN|Ô\d+B?\s+ĐÁP ÁN)/;
const ban = [];
for (const b of bais) {
  for (const [ten, m] of Object.entries(b.muc)) {
    for (const d of m.dong || []) {
      if (RAC.test(d)) ban.push(`bài ${b.so} · ${ten}: ${d.slice(0, 50)}`);
    }
  }
}
t('không mục nào lẫn ôn tập hay đáp án chi tiết', ban.length === 0);
in5(ban);

const gbmDai = bais.filter((b) => (b.muc.gocBoMe.dong || []).length > 8);
t('Góc bố mẹ không phình ra (≤ 8 dòng)', gbmDai.length === 0);
in5(gbmDai.map((b) => `bài ${b.so}: ${b.muc.gocBoMe.dong.length} dòng`));

/* ══ 3 · lời chữa và đáp án ══ */
const khongLoi = [];
for (const b of bais) {
  for (const c of b.cau) {
    if (!c.loiChua && !c.answerKey) khongLoi.push(`${b.id}#${c.id}`);
  }
}
t('mọi câu đều có lời chữa của sách', khongLoi.length === 0);
in5(khongLoi);

const quizChua = [];
for (const b of bais) {
  for (const c of b.cau.filter((x) => x.phan === 'quiz')) {
    if (!c.answerKey) quizChua.push(`${b.id}#${c.id}`);
  }
}
t('cả 220 câu quiz đều chấm máy được', quizChua.length === 0);
in5(quizChua);

/* trắc nghiệm: đáp án phải NẰM TRONG danh sách phương án — lệch một chữ là bé bấm
   đúng mà máy báo sai, và bé thì tin máy chứ không tin mình */
const lacChon = [];
for (const b of bais) {
  for (const c of b.cau) {
    const k = c.answerKey;
    if (k && k.choice && !(c.choices || []).includes(k.choice)) {
      lacChon.push(`${b.id}#${c.id}: "${k.choice}"`);
    }
  }
}
t('đáp án trắc nghiệm luôn nằm trong danh sách phương án', lacChon.length === 0);
in5(lacChon);

/* ══ 4 · hình ══ */
const soTay = doc(join(G, 'data/lop4_hinh_manifest.json'));
const HINH = join(G, 'web/public/content/figures');
const thieuAnh = [], lechSha = [];
for (const [id, h] of Object.entries(soTay)) {
  const p = join(HINH, `${id}.png`);
  if (!existsSync(p)) { thieuAnh.push(id); continue; }
  const sha = createHash('sha256').update(readFileSync(p)).digest('hex').slice(0, 16);
  // Sửa params mà quên vẽ lại thì dữ liệu nói một đằng, ảnh hiện một nẻo, và CẢ HAI
  // đều hợp lệ nên không có gì báo (bẫy 20).
  if (sha !== h.sha256_16) lechSha.push(`${id}: ${sha} ≠ ${h.sha256_16}`);
}
t(`mọi hình trong sổ tay đều có ảnh thật (${Object.keys(soTay).length})`,
  thieuAnh.length === 0);
in5(thieuAnh);
t('mã băm ảnh khớp sổ tay', lechSha.length === 0);
in5(lechSha);

/* hình đã vẽ = đã gắn — bắt được hình rơi mất HAI LẦN ở các quyển trước */
const daGan = new Set();
for (const b of bais) {
  for (const m of Object.values(b.muc)) {
    for (const h of m.hinh || []) daGan.add(h.id);
  }
}
const roi = Object.keys(soTay).filter((id) => !daGan.has(id) && !soTay[id].hoan);
t(`hình đã vẽ đều đã gắn vào bài (${daGan.size})`, roi.length === 0);
in5(roi);

/* mọi bài phải có hình MÀN MỞ — bài nào cũng mở bằng một tình huống có hình */
/* Bài nào VIDEO thay cả mở bài lẫn bài giảng thì không cần hình màn mở — chính
   video là màn mở. Giữ thêm một hình nữa là hình KHÔNG BAO GIỜ HIỆN, đúng nghĩa
   hình chết mà phép kiểm ngay trên vừa canh. Bác chốt 14-08. */
/* ⚠ GHÉP BẰNG MÃ BÀI, KHÔNG BẰNG SỐ BÀI. Từ 14-08 (lối C) `so` trong BẢN GỐC chỉ
   là số tạm lúc viết, còn `so` trong BẢN DỰNG đếm từ vị trí trong `thu_tu.json` —
   hai bên cố ý khác nhau. Bản đầu của phép kiểm này ghép bằng `so`, nên chèn chín
   bài vào chương 3 là nó ghép trượt toàn bộ và báo thiếu hình màn mở ở những bài
   vốn có video. Mã bài là thứ DUY NHẤT hai bên chắc chắn gọi giống nhau. */
const coVideo = new Set(readdirSync(APP)
  .filter((f) => /^DL_KSN4_B\d+\.json$/.test(f))
  .map((f) => doc(join(APP, f)))
  .filter((b) => b.video?.giang)
  .map((b) => b.id));
const khongMo = bais.filter((b) => !coVideo.has(b.id)
  && !(b.muc.chuyenMoBai.hinh || []).length);
t(`${SO_BAI}/${SO_BAI} bài có hình màn mở`, khongMo.length === 0);
in5(khongMo.map((b) => b.id));

/* hình màn mở là bản ĐỀ: không mang dấu vết đáp án (chuẩn mục 6 luật 3) */
const moTa = doc(join(G, 'data/lop4_hinh.json'));
const loMo = [];
for (const h of moTa.filter((x) => x.muc === 'chuyenMoBai')) {
  const p = h.params || {};
  if (p.note) loMo.push(`${h.id}: có dòng chốt "${String(p.note).slice(0, 40)}"`);
  if (p.hienTich) loMo.push(`${h.id}: hienTich bật`);
  if (p.tenGoc) loMo.push(`${h.id}: ghi sẵn tên góc "${p.tenGoc}"`);
  if (/=/.test(p.title || '')) loMo.push(`${h.id}: tiêu đề có dấu '='`);
}
t('hình màn mở KHÔNG chứa dấu vết đáp án', loMo.length === 0);
in5(loMo);

/* tiêu đề hình không quá 120 chữ — trên ngưỡng ấy nó là một đoạn văn đè lên đầu hình */
const tdDai = moTa.filter((h) => (h.params.title || '').length > 120);
t('tiêu đề hình ≤ 120 chữ', tdDai.length === 0);
in5(tdDai.map((h) => `${h.id}: ${h.params.title.length} chữ`));

/* ══ 5 · bản dựng cho app ══ */
if (existsSync(APP)) {
  const app = readdirSync(APP).filter((f) => /^DL_KSN4_B\d+\.json$/.test(f))
    .map((f) => doc(join(APP, f))).sort((a, b) => a.so - b.so);
  t(`bản cho app đủ ${SO_BAI} bài (${app.length})`, app.length === SO_BAI);

  /* prev/next khớp thứ tự */
  const lechNoi = [];
  app.forEach((d, i) => {
    const truoc = i ? app[i - 1].id : null;
    const sau = i + 1 < app.length ? app[i + 1].id : null;
    if (d.series.prev !== truoc || d.series.next !== sau) lechNoi.push(d.id);
  });
  t('prev/next khớp thứ tự bài', lechNoi.length === 0);
  in5(lechNoi);

  /* mỗi bài phải dạy ít nhất một nguyên tắc — chặng giảng rỗng là hỏng CÂM:
     bài vẫn dựng, phòng học vẫn mở, chỉ là không dạy gì.

     TRỪ bài mà VIDEO thay cả mở bài lẫn bài giảng (bác chốt 14-08). Ở đó rỗng là
     CHỦ Ý, và cái dạy nằm trong clip. Nhưng phải có video THẬT mới được rỗng —
     nếu không thì đúng là hỏng câm, và đây là chỗ dễ nới bừa nhất: ai đó xoá nhầm
     phần giảng rồi nới cổng cho xanh là bài ấy thành trống trơn. */
  const rong = app.filter((d) => !(d.knowledgeCore.statements || []).length
    && !d.video?.giang);
  t('bài nào cũng có nguyên tắc để dạy, HOẶC có video thay', rong.length === 0);
  in5(rong.map((d) => d.id));

  /* mọi nguyên tắc đều có màn nhận nó */
  const mocoi = [];
  for (const d of app) {
    const nhan = new Set((d.lecture.screens || []).flatMap((s) => s.teaches || []));
    for (const s of d.knowledgeCore.statements) {
      if (!nhan.has(s.id)) mocoi.push(`${d.id} · ${s.id}`);
    }
  }
  t('mọi nguyên tắc đều có màn giảng nhận', mocoi.length === 0);
  in5(mocoi);

  /* hình neo vào màn CÓ THẬT — 'screen:S9' trỏ vào màn không tồn tại thì hình biến
     mất lặng lẽ, mà bài vẫn chạy */
  const neoLac = [];
  for (const d of app) {
    const man = new Set((d.lecture.screens || []).map((s) => s.id));
    const cau = new Set([...Object.values(d.practice.pools).flat(),
      ...d.assessment.items].map((c) => c.id));
    for (const f of d.figureSpec || []) {
      for (const u of f.usedIn || []) {
        if (u.startsWith('screen:') && !man.has(u.slice(7))) {
          neoLac.push(`${d.id} · ${f.id} → ${u}`);
        }
        if (u.startsWith('item:') && !cau.has(u.slice(5).split(':')[0])) {
          neoLac.push(`${d.id} · ${f.id} → ${u}`);
        }
      }
    }
  }
  t('hình neo vào màn / câu CÓ THẬT', neoLac.length === 0);
  in5(neoLac);

  /* màn mở: lời dẫn ngắn, và KHÔNG kể một bộ số khác với đề (bẫy 32) */
  const moDai = app.filter((d) => {
    const h = (d.lecture.screens || []).find((s) => s.kind === 'hook');
    return h && (h.narration || '').length > 320;
  });
  t('lời dẫn màn mở không quá dài', moDai.length === 0);
  in5(moDai.map((d) => `${d.id}: ${d.lecture.screens[0].narration.length} chữ`));

  /* ── bẫy 32 · lời dẫn và hình màn mở phải kể CÙNG MỘT bài toán ──
     Đã dính thật: lời dẫn lấy đề của mục ⑥ (bài mẫu trình bày vở) còn hình vẽ theo
     mục ② (tình huống mở), nên màn mở hiện "tổng hai chữ số bằng 12" bên trên một
     cái bảng hàng - lớp ghi 24 358. Hai đề đá nhau ngay dòng đầu bé đọc, mà dữ liệu
     thì hợp lệ hoàn toàn — chỉ nhìn màn hình thật mới thấy.

     ── BẢN ĐẦU CANH BẰNG CON SỐ, VÀ ĐÃ PHẢI BỎ ──
     Bản đầu đòi "mọi số trong lời dẫn phải có mặt trong hình". Nó đúng ở thời lời
     dẫn chỉ mang mỗi câu HỎI GÌ (gần như không có số). Từ khi lời dẫn mang đủ đề
     bài thì mệnh đề ấy hỏng cả hai đầu:

       · bắt OAN — bài 4 có "tiền thiếu 45 nghìn" trong lời mà hình không vẽ, VÌ 45
         chính là ĐÁP ÁN. Đòi hình phải có nó là đòi hình lộ đáp;
       · bắt HỤT — thử tái tạo đúng bẫy 32 ở bài 1 thì nó KHÔNG bắt được, vì hình
         bài ấy chứa các chữ số rời (2·4·3·5·8) chứ không có chuỗi "24358".

     Nay canh bằng CHỮ: lời dẫn và tiêu đề hình phải chung ít nhất một từ có nghĩa.
     Hai bài toán khác nhau thì không chung từ nào — mệnh đề này bắt được bẫy 32 tái
     tạo, và bắt thêm ba bài còn sót thật (tuổi hai anh em / hình vẽ ba bạn với 100
     viên bi · phân số 3/4 - 5/8 / hình hỏi 7/8 - 9/10 · khung mái tam giác / hình
     cắt chữ nhật theo đường chéo). */
  const DUNG = new Set(['và', 'của', 'có', 'là', 'một', 'hai', 'ba', 'thì', 'cho',
    'với', 'các', 'những', 'này', 'ấy', 'bao', 'nhiêu', 'mấy', 'nào', 'thế', 'ra',
    'đi', 'được', 'bằng', 'trong', 'từ', 'đến', 'sau', 'trước', 'khi', 'mỗi', 'số',
    'hỏi', 'tìm', 'đúng', 'nếu', 'hơn', 'kém', 'còn', 'chỉ', 'đã', 'sẽ', 'vào',
    'trên', 'dưới', 'lại', 'như', 'mà', 'nó', 'gì', 'không']);
  const tuCua = (s) => new Set(
    (String(s).normalize('NFC').toLowerCase().match(/[0-9a-zà-ỹ]+/g) || [])
      .filter((w) => w.length > 1 && !DUNG.has(w)));
  const tdTheoBai = {};
  for (const m of moTa) {
    if (m.muc === 'chuyenMoBai') tdTheoBai[m.bai] = m.params?.title || '';
  }
  const daNhau = [];
  for (const d of app) {
    const h = (d.lecture.screens || []).find((s) => s.kind === 'hook');
    if (!h || !tdTheoBai[d.id]) continue;
    const tHinh = tuCua(tdTheoBai[d.id]);
    if (!tHinh.size) continue;
    const tLoi = tuCua(h.narration);
    if (![...tHinh].some((w) => tLoi.has(w))) {
      daNhau.push(`${d.id}: hình đề "${tdTheoBai[d.id].slice(0, 60)}" — lời dẫn `
        + `"${h.narration.slice(0, 60)}" không chung chữ nào`);
    }
  }
  t('lời dẫn màn mở và hình màn mở kể CÙNG một bài toán', daNhau.length === 0);
  in5(daNhau);

  /* nhãn đường lùi phải nói đúng LỚP đích */
  const nhanSai = app.filter((d) => d.duongLui
    && d.duongLui.nhan !== 'Học lại bài lớp 3');
  t('nút đường lùi mời đúng "Học lại bài lớp 3"', nhanSai.length === 0);
  in5(nhanSai.map((d) => `${d.id}: ${d.duongLui.nhan}`));
}

/* ══ 5b · LỜI VĂN NÓI THẲNG (bác yêu cầu) ══
   Sách bọc mọi thứ trong "Xưởng Mô Hình": bài toán là "đơn hàng", cách làm là
   "tuyệt kỹ", dấu hiệu chia hết là "mật mã", người giải là "kỹ sư"/"thám tử".
   Bé phải đọc qua lớp vỏ ấy mới tới được bài toán. `tools/de_hieu_lop4.py` bóc vỏ
   khi dựng; hai phép dưới canh không cho nó mọc lại. */
const BO_TRUONG = new Set(['id', 'file', 'sha256_16', 'usedIn', 'skills', 'series',
  '$schema', 'quyen', 'mucGoc', 'dangGoc']);
function* chuBeDoc(o, p = '') {
  if (typeof o === 'string') yield [p, o];
  else if (Array.isArray(o)) { for (const v of o) yield* chuBeDoc(v, p); }
  else if (o && typeof o === 'object') {
    for (const [k, v] of Object.entries(o)) {
      if (BO_TRUONG.has(k)) continue;
      yield* chuBeDoc(v, p ? `${p}.${k}` : k);
    }
  }
}
const VI_VON = /\b(kỹ sư|xưởng|thám tử|tuyệt kỹ|vũ khí|bí kíp|thần chú|mật mã|mật thư|hoa tiêu|quan tòa|cao thủ|đơn hàng|Anh Trí Dũng đố|TRÙM CUỐI|GÓC KHÁM PHÁ)\b/i;
const moiTep = [
  ...readdirSync(APP).filter((f) => /^DL_KSN4_B\d+\.json$/.test(f))
    .map((f) => join(APP, f)),
  ...readdirSync(join(G, 'web/public/content/reviews'))
    .filter((f) => /^DCR_KSN4_C\d+\.json$/.test(f))
    .map((f) => join(G, 'web/public/content/reviews', f)),
];
const conViVon = [], conCham = [];
for (const tep of moiTep) {
  for (const [p, s] of chuBeDoc(doc(tep))) {
    const m = s.match(VI_VON);
    if (m) conViVon.push(`${tep.split('/').pop()} · ${p}: "${m[1]}"`);
    /* Dấu · giữa câu — bé không biết nó nghĩa gì. Ở TIÊU ĐỀ thì giữ: chỗ ấy nó
       ngăn số bài với tên bài, cả bốn quyển đều dùng, bé không đọc nó thành lời. */
    const truong = p.split('.').pop();
    if (!/^(title|name|trapName|ten|tenChuong)$/i.test(truong) && s.includes(' · ')) {
      conCham.push(`${tep.split('/').pop()} · ${p}: ${s.slice(0, 50)}`);
    }
  }
}
t('không còn ví von / ẩn dụ trong chữ bé đọc', conViVon.length === 0);
in5(conViVon);
t('không còn dấu · làm dấu ngăn giữa câu', conCham.length === 0);
in5(conCham);

/* ══ 5c · KỲ SÁT HẠCH PHẢI CHẤM MÁY (bác yêu cầu) ══
   Trước đây ExamPlayer chỉ hỏi bé "Mình làm đúng / Mình làm sai" — 236 câu quan
   trọng nhất của quyển nằm ngoài mọi phép đo. */
const cauKy = readdirSync(join(G, 'web/public/content/reviews'))
  .filter((f) => /^DCR_KSN4_C\d+\.json$/.test(f))
  .flatMap((f) => {
    const d = doc(join(G, 'web/public/content/reviews', f));
    return [...(d.examA || []), ...(d.deB || [])];
  });
const kyCham = cauKy.filter((q) => q.answerKey);
t(`kỳ sát hạch chấm máy ≥ 95% (${kyCham.length}/${cauKy.length})`,
  kyCham.length >= cauKy.length * 0.95);

/* ══ 6 · kỳ sát hạch ══ */
const on = doc(join(G, 'data/lop4_ontap.json')).ky;
t(`đủ 11 kỳ ôn tập (${on.length})`, on.length === 11);
t('mọi kỳ có ngưỡng đạt lấy từ sách',
  on.every((k) => k.need >= 1 && k.tong === k.examA.length));

const maBai = new Set(bais.map((b) => b.id));
const soiLac = [], soiThieu = [];
for (const k of on) {
  for (const q of k.examA) {
    if (!(q.veCau || []).length) soiThieu.push(`${k.id} câu ${q.qno}`);
    for (const v of q.veCau || []) if (!maBai.has(v)) soiLac.push(`${k.id} → ${v}`);
  }
}
t('MỌI câu ôn tập đều có mối nối về bài', soiThieu.length === 0);
in5(soiThieu);
t('Bảng tự soi trỏ vào bài CÓ THẬT', soiLac.length === 0);
in5(soiLac);

const trongDap = [];
for (const k of on) {
  for (const q of [...k.examA, ...k.deB]) {
    if (!q.answer) trongDap.push(`${k.id} câu ${q.qno}`);
  }
}
t('mọi câu ôn tập và đề B đều có đáp án', trongDap.length === 0);
in5(trongDap);

/* ══ 7 · đường lùi lớp 4 → lớp 3 ══ */
const gan3 = doc(join(G, 'data/lop4_gan_lop3.json')).gan;
const coL3 = new Set(readdirSync(join(G, 'data/lop3'))
  .filter((f) => f.startsWith('DL_KSN3_B'))
  .map((f) => f.replace('.json', '').replace('DL_KSN3_', 'DL:KSN3.')));
t(`đủ ${SO_BAI} dòng đường lùi (${Object.keys(gan3).length})`,
  Object.keys(gan3).length === SO_BAI);

const lac3 = [];
for (const [ma, v] of Object.entries(gan3)) {
  for (const ve of v.ve || []) if (!coL3.has(ve)) lac3.push(`${ma} → ${ve}`);
}
t(`mọi đích đến là bài lớp 3 CÓ THẬT (${coL3.size} bài)`, lac3.length === 0);
in5(lac3);

const CAN_CU = new Set(['sach', 'sachSua', 'chuDe', 'khong']);
const canLa = Object.entries(gan3).filter(([, v]) => !CAN_CU.has(v.canCu));
t('căn cứ nằm trong bốn giá trị đã khai', canLa.length === 0);
in5(canLa.map(([m, v]) => `${m}: ${v.canCu}`));

/* dòng `khong` phải RỖNG đích, dòng khác phải CÓ đích — bỏ trống thì không phân
   biệt được "chưa xét" với "đã xét và kết luận là không có" */
const lechCan = Object.entries(gan3).filter(([, v]) =>
  (v.canCu === 'khong') !== ((v.ve || []).length === 0));
t('căn cứ khớp với danh sách đích', lechCan.length === 0);
in5(lechCan.map(([m]) => m));

/* mọi dòng phải ghi LÝ DO — bảng không có lý do thì phiên sau không soát lại được */
const khongViSao = Object.entries(gan3).filter(([, v]) => !v.viSao);
t('mọi dòng đường lùi đều ghi lý do', khongViSao.length === 0);
in5(khongViSao.map(([m]) => m));

/* ══ 8 · đường lùi lớp 5 → lớp 4 ══ */
const gan4 = doc(join(G, 'data/lop5_gan_lop4.json')).gan;
t(`đủ 168 micro lớp 5 có đường lùi (${Object.keys(gan4).length})`,
  Object.keys(gan4).length === 168);

const lac4 = [];
for (const [ma, v] of Object.entries(gan4)) {
  for (const ve of v.ve || []) if (!maBai.has(ve)) lac4.push(`${ma} → ${ve}`);
}
t('mọi đích đến là bài lớp 4 CÓ THẬT', lac4.length === 0);
in5(lac4);

/* trường `duongLui` phải NẰM TRONG tệp bài lớp 5, và ở CẢ HAI nơi — với Quyển 1
   lớp 5 thì data/lessons và public/content/lessons phải giống hệt nhau */
for (const noi of ['data/lessons', 'web/public/content/lessons']) {
  const d = doc(join(G, noi, 'DL_KSN5Q1_B41_M1.json'));
  t(`${noi} đã gắn đường lùi`,
    !!d.duongLui && d.duongLui.nhan === 'Học lại bài lớp 4');
}

/* ══ 9 · tiền tố mã bài không trùng, không là tiền tố của nhau ══ */
const TIEN_TO = ['DL:KSN2.', 'DL:KSN3.', 'DL:KSN4.', 'DL:KSN5Q1.', 'DR:KSN5Q2.'];
const dungNhau = [];
for (const a of TIEN_TO) {
  for (const b of TIEN_TO) {
    if (a !== b && b.startsWith(a)) dungNhau.push(`${a} là tiền tố của ${b}`);
  }
}
t('tiền tố mã bài không trùng / không lồng nhau', dungNhau.length === 0);
in5(dungNhau);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
