/**
 * SOÁT BÀI HỌC TIẾNG ANH ĐÃ SINH.
 * chạy: node test/tienganh_bai.test.mjs
 *
 * Bài do MÁY sinh, nên cái hỏng ở đây không phải lỗi gõ tay mà là lỗi HÀNG LOẠT:
 * sai một chỗ trong bộ sinh là 16 bài cùng sai một kiểu. Cổng này soi ba thứ mà
 * mắt người đọc 16 tệp JSON sẽ bỏ sót.
 *
 * ── LỖI ĐÃ XẢY RA THẬT, VÀ VÌ SAO CÓ MỤC 2 ──
 * Bản đầu của bộ sinh thay chuỗi trong CÂU VÍ DỤ thay vì điền vào CÔNG THỨC. Ở U15
 * câu mẫu là "Point to your hand." còn từ của unit là face·father·foot·football —
 * `hand` thuộc U8, không có trong câu. Phép tìm trả chuỗi RỖNG và
 * `"...".replace("", "face", 1)` dán "face" vào đầu:
 *
 *     ✗  "facePoint to your hand."
 *
 * JSON vẫn hợp lệ, cổng cũ vẫn xanh, LessonPlayer vẫn dựng ra màn hình. Chỉ có bé
 * là đọc một câu vô nghĩa. Mục 2 dưới đây bắt đúng loại ấy: mọi CHỮ trong câu sinh
 * ra phải có gốc — hoặc là từ của bản đồ, hoặc là chữ có sẵn trong công thức.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { chamTiengAnh, chuanTA } from '../src/mon/tienganh/lib/cham.js';

const R = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const quyens = ['ta1', 'ta2', 'ta3'].filter((q) => existsSync(join(R, 'web/public/content', q)));
if (!quyens.length) {
  console.log('   ⏸ chưa sinh bài tiếng Anh nào');
  console.log('\n0 PASS · 0 FAIL');
  process.exit(0);
}

for (const q of quyens) {
  const lop = Number(q.slice(2));
  const chuan = JSON.parse(readFileSync(join(R, `data/tienganh/chuan_lop${lop}.json`), 'utf8'));
  const bais = readdirSync(join(R, 'web/public/content', q)).filter((f) => /^DL_.*\.json$/.test(f))
    .sort().map((f) => JSON.parse(readFileSync(join(R, 'web/public/content', q, f), 'utf8')));
  t(`${q} · sinh đủ ${chuan.unit.length} bài`, bais.length === chuan.unit.length);

  /* ══ 1 · MỌI CÂU HỎI PHẢI CHẤM MÁY ĐƯỢC ══
     Đưa chính đáp án vào làm bài. Câu nào không tự chấm đúng nổi thì bé làm đúng
     cũng bị báo sai — và với bài máy sinh thì lỗi ấy nhân lên 16 lần. */
  const khongCham = [], khongDo = [];
  let soCau = 0;
  for (const b of bais) {
    const cau = [...Object.values(b.practice.pools).flat(), ...b.assessment.items];
    for (const c of cau) {
      soCau += 1;
      const k = c.answerKey;
      const dap = k.the ? k.the : (k.choice !== undefined ? k.choice : k.value);
      const r = chamTiengAnh(c, dap);
      if (!r.ok) khongCham.push(`${b.id}/${c.id}: đưa đáp án đúng mà chấm SAI`);
      if (r.mode !== 'auto') khongDo.push(`${b.id}/${c.id}: rơi vào tự-đối-chiếu`);
      /* Chiều ngược lại: có kiểu hỏng làm bộ chấm nhận bừa mọi thứ. */
      const bay = k.the ? k.the.map(() => 'zzz') : 'zzz-khong-bao-gio-dung';
      if (chamTiengAnh(c, bay).ok && c.format !== 'tf') {
        khongCham.push(`${b.id}/${c.id}: đáp án SAI vẫn được tính đúng`);
      }
    }
  }
  t(`${q} · ${soCau} câu đều chấm máy đúng (${khongCham.length} hỏng)`, khongCham.length === 0);
  in5(khongCham);
  t(`${q} · không câu nào rơi vào tự-đối-chiếu (${khongDo.length})`, khongDo.length === 0);
  in5(khongDo);

  /* ══ 2 · CÂU SINH RA PHẢI CÓ GỐC — chặn "facePoint to your hand." ══
     Kho chữ hợp lệ = mọi từ của bản đồ (kể cả dạng biến đổi) + mọi chữ có sẵn
     trong CÔNG THỨC của mẫu câu + tên riêng và số đếm đã khai. Một chữ ngoài kho
     ấy nghĩa là bộ sinh vừa đẻ ra thứ không ai duyệt. */
  const kho = new Set();
  const nap = (s) => String(s || '').toLowerCase().match(/[a-z']+/g)?.forEach((w) => kho.add(w));
  for (const u of chuan.unit) {
    for (const x of u.tu) [x.tu, x.so_it, x.so_nhieu, x.dang_ing].forEach(nap);
    for (const m of u.mau_cau) {
      nap(String(m.cong_thuc || '').replace(/\[[^\]]*\]/g, ' '));
      nap(m.vi_du);
    }
  }
  for (const nhom of ['so_dem', 'mau', 'ten']) {
    for (const m of (chuan.them?.[nhom]?.muc) || []) nap(typeof m === 'string' ? m : m.word);
  }

  const chuLa = [], sai_dang = [];
  for (const b of bais) {
    for (const c of b.knowledgeCore.canonicalExamples) {
      for (const w of c.toLowerCase().match(/[a-z']+/g) || []) {
        if (!kho.has(w)) chuLa.push(`${b.id}: "${c}" — chữ lạ “${w}”`);
      }
      /* Câu tiếng Anh phải mở đầu bằng chữ HOA và đóng bằng dấu câu. "facePoint…"
         lọt qua phép kiểm chữ-lạ nếu "face" hợp lệ, nhưng chết ở đây. */
      if (!/^[A-Z]/.test(c)) sai_dang.push(`${b.id}: "${c}" không mở đầu bằng chữ hoa`);
      if (!/[.?!]$/.test(c)) sai_dang.push(`${b.id}: "${c}" không có dấu câu cuối`);
      /* Hai chữ dính liền nhau không có dấu cách — dấu vết của replace hỏng. */
      if (/[a-z][A-Z]/.test(c)) sai_dang.push(`${b.id}: "${c}" có hai chữ dính nhau`);
      if (/\[|\]/.test(c)) sai_dang.push(`${b.id}: "${c}" còn sót ô chưa điền`);
    }
  }
  t(`${q} · mọi chữ trong câu sinh ra đều có gốc (${chuLa.length} chữ lạ)`, chuLa.length === 0);
  in5(chuLa);
  t(`${q} · câu sinh ra đúng dạng câu (${sai_dang.length} chỗ)`, sai_dang.length === 0);
  in5(sai_dang);

  /* ══ 3 · MỒI NHỬ, Ô GÕ, VÀ NHỊP ĐÁP ÁN ══ */
  const moiTrung = [], goDai = [], nhip = [];
  for (const b of bais) {
    for (const c of Object.values(b.practice.pools).flat()) {
      const k = c.answerKey;
      if (c.choices) {
        const d = chuanTA(k.choice);
        for (const x of c.choices) {
          if (x !== k.choice && chuanTA(x) === d) {
            moiTrung.push(`${b.id}/${c.id}: mồi “${x}” trùng đáp án`);
          }
        }
        if (!c.choices.includes(k.choice)) {
          moiTrung.push(`${b.id}/${c.id}: đáp án không có trong nút`);
        }
      }
      /* Ô gõ của bé 6 tuổi: chỉ chữ Latin thường và không quá dài. */
      if (k.value !== undefined && !c.choices) {
        const v = String(k.value);
        if (v.length > 46) goDai.push(`${b.id}/${c.id}: gõ ${v.length} ký tự`);
        if (!/^[A-Za-z0-9 '\-.,?!]+$/.test(v)) goDai.push(`${b.id}/${c.id}: “${v}” gõ không được`);
      }
    }
    /* Kỳ sát hạch KHÔNG được cùng một đáp án liên tiếp quá 2 lần — bé qua bằng
       cách đoán theo nhịp thì con số trong sổ bố mẹ là con số rỗng. */
    const gt = b.assessment.items.map((x) => x.answerKey.value);
    for (let i = 2; i < gt.length; i += 1) {
      if (gt[i] === gt[i - 1] && gt[i] === gt[i - 2]) {
        nhip.push(`${b.id}: ba câu liền cùng đáp án ${gt[i]}`);
      }
    }
    if (new Set(gt).size < 2 && gt.length > 1) nhip.push(`${b.id}: cả kỳ chỉ một đáp án`);
  }
  t(`${q} · không mồi nhử nào trùng đáp án (${moiTrung.length})`, moiTrung.length === 0);
  in5(moiTrung);
  t(`${q} · ô gõ vừa sức bé (${goDai.length} chỗ)`, goDai.length === 0);
  in5(goDai);
  t(`${q} · đáp án sát hạch không thành nhịp đoán được (${nhip.length})`, nhip.length === 0);
  in5(nhip);

  /* ══ 3B · CHỖ DỄ NHẦM PHẢI NÓI VỀ CHÍNH CÂU CỦA BÀI ẤY ══

     Đây là lỗi bác bắt được khi mở Unit 1: máy đọc “Hi, I'm Bill.” mà chữ bên dưới
     giải thích về “con chó”. Gốc là một dòng — `dung.replace(" a ", " ", 1)` — cộng
     một lời giải thích GHIM CỨNG ví dụ "This is a dog":

       · 10/16 bài không có chữ " a " nên phép cắt không làm gì → câu "sai" TRÙNG
         HỆT câu đúng. Bé được cho xem một câu hoàn toàn đúng rồi bảo là sai;
       · 16/16 bài dùng chung một lời giải thích, kể cả bài dạy "I have a car".

     Không cổng nào bắt được: JSON hợp lệ, màn hình vẽ đủ, clip vẫn đọc. Chỉ tai
     người mới nghe ra. Nên soi ba điều, và điều thứ ba mới là điều đắt nhất. */
  const nhamHong = [];
  for (const b of bais) {
    const m = (b.knowledgeCore.misconceptions || [])[0];
    if (!m) continue;                       // không dựng khối là hợp lệ — thà thiếu còn hơn sai
    if (m.wrong === m.right) {
      nhamHong.push(`${b.id}: câu "sai" TRÙNG HỆT câu đúng — "${m.wrong}"`);
    }
    /* Câu "sai" không được là một câu ĐÚNG của chính bài ấy. */
    if (b.knowledgeCore.canonicalExamples.includes(m.wrong)) {
      nhamHong.push(`${b.id}: câu "sai" lại là một câu đúng trong bài — "${m.wrong}"`);
    }
    /* Lời giải thích phải NHẮC TỚI câu của bài này. Ghim cứng ví dụ của bài khác
       là bé nghe một đằng đọc một nẻo — đúng chỗ đã hỏng. */
    /* "Nhắc tới bài này" tính cả từ đứng TRONG CÂU, không chỉ từ vựng — luật câu
       ra lệnh giải thích bằng chính động từ mở đầu ("Touch"), mà động từ ấy không
       nằm trong danh sách từ mới. Bản đầu của phép kiểm báo oan đúng ba bài ấy. */
    const chuTrongCau = new Set(
      [m.right, m.wrong].join(' ').toLowerCase().match(/[a-z']+/g) || [],
    );
    const nhacToi = [m.right, m.wrong].some((c) => m.why.includes(c))
      || (b.knowledgeCore.vocabulary || []).some((v) => m.why.includes(v.tu) || m.why.includes(v.nghia))
      || [...chuTrongCau].some((w) => w.length > 2 && m.why.toLowerCase().includes(w));
    if (!nhacToi) nhamHong.push(`${b.id}: lời giải thích không nhắc tới câu/từ nào của bài`);
    /* Và KHÔNG được nhắc tới từ tiếng Anh của bài KHÁC. Từ nằm trong câu đúng HOẶC
       câu sai đều hợp lệ — "You" là chữ bị thêm vào để tạo lỗi, nó chỉ có ở câu sai. */
    const tuBaiNay = new Set((b.knowledgeCore.vocabulary || []).map((v) => v.tu.toLowerCase()));
    const tuLa = [...new Set(m.why.toLowerCase().match(/“[^”]+”/g) || [])]
      .map((x) => x.replace(/[“”]/g, '').trim())
      .filter((w) => /^[a-z][a-z' ]*$/.test(w) && w.length > 2)
      .filter((w) => !tuBaiNay.has(w) && !chuTrongCau.has(w)
                     && !m.right.toLowerCase().includes(w) && !m.wrong.toLowerCase().includes(w));
    if (tuLa.length) nhamHong.push(`${b.id}: giải thích nhắc từ lạ (${tuLa.join(', ')})`);
  }
  t(`${q} · chỗ dễ nhầm khớp với câu của bài (${nhamHong.length} chỗ lệch)`, nhamHong.length === 0);
  in5(nhamHong);

  /* ══ 4 · MỖI BÀI PHẢI ĐỦ BỐN BẬC ══
     Bốn việc bác nêu: hiểu từ · hiểu cấu trúc · nói · gõ. Bài thiếu bậc 3 thì bé
     học xong không ráp được câu nào — mà điều đó KHÔNG lộ ra ở bất cứ con số nào. */
  const thieuBac = [];
  for (const b of bais) {
    const co = new Set(Object.values(b.practice.pools).flat().map((c) => c.bac));
    for (const bac of [1, 2, 3, 4]) {
      if (!co.has(bac)) thieuBac.push(`${b.id} (${b.title}): thiếu bậc ${bac}`);
    }
  }
  t(`${q} · bài nào cũng đủ bốn bậc (${thieuBac.length} chỗ thiếu)`, thieuBac.length === 0);
  in5(thieuBac);

  /* ══ 5 · KHOÁ BKT PHẢI KÈM MÃ QUYỂN ══
     Khoá số trần làm huy hiệu lây giữa các quyển — đã dính thật bên Toán. */
  const khoaTran = bais.filter((b) => !String(b.skills?.bktUnit || '').includes('@'))
    .map((b) => `${b.id}: bktUnit “${b.skills?.bktUnit}”`);
  t(`${q} · khoá BKT nào cũng kèm mã quyển (${khoaTran.length})`, khoaTran.length === 0);
  in5(khoaTran);

  const tong = bais.reduce((a, b) => a + Object.values(b.practice.pools).flat().length, 0);
  console.log(`   ${q}: ${bais.length} bài · ${tong} câu luyện tập · `
    + `${bais.reduce((a, b) => a + b.assessment.items.length, 0)} câu sát hạch`);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
