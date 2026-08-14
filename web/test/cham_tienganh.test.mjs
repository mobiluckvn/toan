/**
 * BỘ CHẤM TIẾNG ANH — và CỔNG CANH "TOÁN KHÔNG ĐỔI".
 * chạy: node test/cham_tienganh.test.mjs
 *
 * Tệp này làm hai việc, và việc thứ hai mới là việc quan trọng.
 *
 * ── PHẦN A · chấm tiếng Anh có đúng không ──
 * Mỗi phép kiểm dưới đây gắn với một cái bẫy CỤ THỂ đã soi ra trong dữ liệu lớp 1,
 * không phải phép kiểm cho có.
 *
 * ── PHẦN B · Toán không đổi MỘT CÂU NÀO ──
 * Bác dặn: "có làm gì cũng không được ảnh hưởng đến môn Toán."
 *
 * `ranh_gioi.test.mjs` đã chặn hai môn import lẫn nhau. Nhưng nó chỉ soi ĐƯỜNG ĐI
 * của mã nguồn — nó không biết ai đó vào sửa thẳng `flow.js` cho "tiện tay hỗ trợ
 * tiếng Anh". Sửa một dòng trong `matchAtom` là 1 612 câu Toán đổi cách chấm, mà
 * không cổng nào đỏ.
 *
 * Nên phần B chấm THẬT lại toàn bộ câu Toán đang chạy và đối chiếu với con số đã
 * ghi. Đổi cách chấm — dù vô tình — là đỏ ngay, kèm con số lệch bao nhiêu.
 *
 * Ba con số ở `MOC` bên dưới là DẤU NIÊM PHONG. Sửa chúng chỉ khi bác CỐ Ý đổi bộ
 * chấm Toán và đã soát lại bằng mắt — đừng bao giờ sửa để "cho cổng xanh".
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { checkAnswer } from '../src/mon/toan/lib/flow.js';
import {
  chuanTA, chamO, chamNut, chamThe, chamTiengAnh, catThe, xepDuoc, THE_TOI_DA,
} from '../src/mon/tienganh/lib/cham.js';
/* Bộ chấm NÓI nằm ở tệp khác (`chamnoi.js`) — chấm tiếng thì khác chấm chữ. Nhưng
   soi chung một chỗ, vì với bé thì "chấm sai" là một chuyện, không phải hai. */
import { chamCau, chamTu, chuanHoa } from '../src/mon/tienganh/lib/chamnoi.js';

const G = new URL('../public/content/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ═════════ PHẦN A · BỘ CHẤM TIẾNG ANH ═════════ */

console.log('\n── A · bộ chấm tiếng Anh ──');

/* Bẫy 1: bàn phím iPad tự đổi ' thành ’. Bé gõ đúng y hệt mà bị chấm sai. */
t("dấu nháy cong ’ nhận như dấu thẳng '", chamO("She's running.", 'She’s running.'));
t("dấu nháy thẳng ' nhận như dấu cong ’", chamO('I’m Bill.', "I'm Bill."));

/* Bẫy 2: bé 6 tuổi chưa dùng phím Shift. */
t('hoa/thường không phân biệt', chamO('This is a dog.', 'this is a dog'));

/* Bẫy 3: dấu chấm cuối có gõ hay không cũng được — nhưng chỉ Ở CUỐI. */
t('thiếu dấu chấm cuối vẫn đúng', chamO('I have a car.', 'I have a car'));
t('thừa dấu chấm cuối vẫn đúng', chamO('milk', 'milk.'));
t('dấu hỏi cuối bỏ được', chamO('How many clocks?', 'how many clocks'));

/* Bẫy 4: khoảng trắng quanh dấu gạch ngăn hỏi/đáp. */
t('gạch ngăn hỏi/đáp: thừa thiếu khoảng trắng vẫn đúng',
  chamO('How many clocks? - Two.', 'How many clocks?-Two'));

/* SIẾT: sai chính tả là SAI. Bậc 4 đang kiểm đúng cái này. */
t('sai chính tả một chữ là SAI', !chamO('duck', 'dack'));
t('thiếu một chữ là SAI', !chamO('door', 'dor'));
t('thừa một chữ là SAI', !chamO('dog', 'dogg'));

/* SIẾT: thứ tự từ CHÍNH LÀ ngữ pháp — đây là chỗ bộ chấm Toán nới và sai. */
t('đảo thứ tự từ là SAI', !chamO('This is a dog.', 'a dog is this'));
t('xếp thẻ sai thứ tự là SAI', !chamThe(['This', 'is', 'a', 'dog.'], ['is', 'This', 'a', 'dog.']));
t('xếp thẻ đúng thứ tự là ĐÚNG', chamThe(['This', 'is', 'a', 'dog.'], ['This', 'is', 'a', 'dog.']));
t('xếp thẻ thiếu một thẻ là SAI', !chamThe(['This', 'is', 'a', 'dog.'], ['This', 'is', 'dog.']));

/* SIẾT: không quy về số. "Two" và "2" chỉ cùng đúng khi NGƯỜI SOẠN khai. */
t('"2" không tự động bằng "Two"', !chamO('Two', '2'));
t('khai nhanThem thì "2" mới bằng "Two"', chamO('Two', '2', ['2']));

/* Chưa trả lời phải là CHƯA ĐÚNG — bẫy mà bộ chấm Toán đã dính thật (68 câu). */
t('ô rỗng là CHƯA ĐÚNG', !chamO('dog', ''));
t('ô toàn khoảng trắng là CHƯA ĐÚNG', !chamO('dog', '   '));
t('chưa bấm gì ở câu đúng/sai là CHƯA ĐÚNG',
  !chamTiengAnh({ answerKey: { value: false } }, '').ok);

/* Bẫy 5 — cái quan trọng nhất. Câu dài nhất của lớp 1 là 46 ký tự; bộ chấm Toán
   bỏ chấm mọi đáp án dài quá 26 ký tự (`isSelfCheck`) nên bé MẤT Ô NHẬP. */
const CAU_DAI = 'How many windows can you see? - I can see six.';
t(`câu ${CAU_DAI.length} ký tự VẪN chấm máy (không rơi vào tự-đối-chiếu)`,
  chamTiengAnh({ answerKey: { value: CAU_DAI } }, CAU_DAI).mode === 'auto');
t('câu dài gõ đúng thì ĐÚNG',
  chamTiengAnh({ answerKey: { value: CAU_DAI } }, CAU_DAI.toLowerCase()).ok);
t('câu dài gõ sai một chữ thì SAI',
  !chamTiengAnh({ answerKey: { value: CAU_DAI } }, CAU_DAI.replace('six', 'sex')).ok);

/* Nút bấm */
t('bấm đúng nút', chamNut('a dog', 'A Dog'));
t('bấm nhầm nút', !chamNut('a dog', 'a duck'));
t('câu bấm chọn', chamTiengAnh({ format: 'chon', answerKey: { choice: 'ball' } }, 'Ball').ok);

/* Nhiều ô */
const nhieuO = { answerKey: { parts: [
  { label: 'từ', value: 'dog' },
  { label: 'nghĩa', value: 'con chó', options: ['con chó', 'con vịt'] },
] } };
t('nhiều ô: đúng cả hai', chamTiengAnh(nhieuO, ['dog', 'con chó']).ok);
t('nhiều ô: sai một ô là sai cả câu', !chamTiengAnh(nhieuO, ['dog', 'con vịt']).ok);

/* Cắt thẻ */
t('cắt thẻ: dấu câu dính vào từ trước',
  JSON.stringify(catThe('This is a dog.')) === JSON.stringify(['This', 'is', 'a', 'dog.']));
t('cắt thẻ: gạch ngăn hỏi/đáp thành thẻ riêng',
  JSON.stringify(catThe('How many clocks? - Two.'))
    === JSON.stringify(['How', 'many', 'clocks?', '-', 'Two.']));
t(`câu ≤ ${THE_TOI_DA} thẻ thì xếp được`, xepDuoc('This is a dog.'));
t('câu dài quá thì KHÔNG cho xếp cả câu', !xepDuoc(CAU_DAI));

/* chuanTA không được đụng vào GIỮA câu */
t('dấu phẩy giữa câu vẫn tính', chuanTA('Hi, I am Bill') !== chuanTA('Hi I am Bill'));

/* ═════════ PHẦN B · TOÁN KHÔNG ĐỔI MỘT CÂU NÀO ═════════ */

console.log('\n── B · cổng canh: bộ chấm Toán không xê dịch ──');

const dk = JSON.parse(readFileSync(join(G, 'chuong_trinh.json'), 'utf8')).chuongTrinh || {};
const maKyCua = (ct) => (ct.tienTo || 'DL:KSN5Q1.').replace(/^[A-Z]+:/, '').replace(/\.$/, '');

/** Mọi câu Toán đang chạy thật, gộp luyện tập và kỳ sát hạch. */
function cauToan() {
  const ra = [];
  for (const ct of Object.values(dk)) {
    if ((ct.mon || 'toan') !== 'toan') continue;
    const thuMuc = join(G, ct.thuMuc || '');
    if (!ct.thuMuc || !existsSync(thuMuc)) continue;
    for (const f of readdirSync(thuMuc).filter((x) => /^D[LR]_.*\.json$/.test(x))) {
      const b = JSON.parse(readFileSync(join(thuMuc, f), 'utf8'));
      ra.push(...Object.values(b.practice?.pools || {}).flat());
    }
    const tmKy = join(G, 'reviews');
    if (!existsSync(tmKy)) continue;
    for (const f of readdirSync(tmKy).filter((x) => x.startsWith(`DCR_${maKyCua(ct)}_`))) {
      const k = JSON.parse(readFileSync(join(tmKy, f), 'utf8'));
      ra.push(...(k.examA || []), ...(k.deB || []));
    }
  }
  return ra.filter((x) => x.answerKey);
}

/**
 * Đưa ĐÁP ÁN của chính câu ấy vào làm bài rồi chấm. Kết quả phải ổn định tuyệt đối:
 * đổi bất kỳ phép nới nào trong `flow.js` là mấy con số dưới đây xê dịch.
 *
 * Chấm cả bằng một câu trả lời CHẮC CHẮN SAI, để bắt cả chiều ngược lại — có kiểu
 * hỏng làm bộ chấm nhận bừa mọi thứ, mà chỉ thử đáp án đúng thì không lộ.
 */
function diemDanh() {
  const d = { tong: 0, dungKhiDungDap: 0, dungKhiSaiDap: 0, tuDoiChieu: 0 };
  for (const x of cauToan()) {
    const k = x.answerKey;
    d.tong += 1;
    let dap;
    if (x.format === 'tf') dap = k.value;
    else if (x.format === 'mcq') dap = k.choice;
    else if (k.values) dap = k.values.join('; ');
    else if (k.parts) dap = k.parts.map((p) => p.value);
    else if (k.accept) dap = [].concat(k.accept)[0];
    else dap = k.value;

    const r = checkAnswer(x, dap);
    if (r.ok) d.dungKhiDungDap += 1;
    if (r.mode === 'selfcheck') d.tuDoiChieu += 1;

    const bay = x.format === 'tf' ? !k.value : ' khong-bao-gio-dung ';
    if (checkAnswer(x, Array.isArray(dap) ? dap.map(() => bay) : bay).ok) d.dungKhiSaiDap += 1;
  }
  return d;
}

/**
 * ── DẤU NIÊM PHONG ──
 * Ghi 12-08-2026, ngay trước khi tách bộ chấm tiếng Anh. Đây là ảnh chụp cách
 * `flow.js` đang chấm bốn quyển Toán ĐANG CHẠY THẬT.
 *
 * Cổng đỏ ở đây nghĩa là: bộ chấm Toán vừa đổi. Đi tìm ai sửa `flow.js`, đừng sửa
 * con số. `tuDoiChieu` là số câu bộ chấm bỏ qua cho bé tự so — con số này TĂNG là
 * dấu hiệu bé vừa mất ô nhập ở đâu đó.
 */
/* ⚠ NIÊM PHONG LẠI 14-08 · 2183 → 2228. Đây KHÔNG phải đổi bộ chấm, mà là thêm câu:
   cụm dãy số lớp 4 tách thành năm bài mới, mỗi bài 9 câu luyện tập = 45 câu.

   Bằng chứng rằng bộ chấm không xê dịch, và đây mới là chỗ đáng đọc:
     · tong          2183 → 2228   lệch đúng +45
     · dungKhiDungDap 2181 → 2226   lệch đúng +45  (mọi câu MỚI đều chấm đúng, và
                                    không câu CŨ nào rơi khỏi diện chấm đúng)
     · dungKhiSaiDap     1 → 1      GIỮ NGUYÊN
     · tuDoiChieu        1 → 1      GIỮ NGUYÊN

   Hai con số cuối là thứ đáng canh nhất — chúng đếm những câu chấm BẤT THƯỜNG. Đổi
   bộ chấm thì chúng động đậy ngay cả khi tổng không đổi. Chúng đứng yên nghĩa là
   cách chấm y nguyên.

   Đừng bao giờ sửa bốn con số này chỉ để "cho cổng xanh". Sửa thì phải kèm một đoạn
   như đoạn này, nói rõ lệch bao nhiêu và VÌ SAO. */
/* ⚠ NIÊM PHONG LẠI 14-08 (lần hai) · 2228 → 2273. LẠI KHÔNG phải đổi bộ chấm.
   Chương 3 lớp 4 tách bốn bài thành chín. Cổng này chỉ đếm câu LUYỆN TẬP (`practice
   .pools`), không đếm quiz, nên số lệch tính ra đúng bằng:

       trước  4 bài × 9 câu = 36
       sau    9 bài × 9 câu = 81
       lệch                 = 45      ·   2228 + 45 = 2273  ✓

   Đã soát trước khi sửa con số:
     · `git diff` trên `src/mon/toan/lib/` và `src/chung/` — KHÔNG một dòng nào đổi;
     · `dungKhiSaiDap` và `tuDoiChieu` vẫn đứng yên ở 1 và 1. Đây mới là hai con số
       đáng tin: chúng đếm câu chấm BẤT THƯỜNG, nên đổi cách chấm là chúng động đậy
       ngay cả khi tổng vẫn khớp. Chúng đứng yên nghĩa là cách chấm y nguyên;
     · 11 kỳ sát hạch vẫn 124 câu và 112 câu đề B — phần sát hạch không xê dịch. */
/* ⚠ 2273 → 2275, cùng ngày. Hai câu ĐỌC SỐ của kỳ ôn 1 trước nay KHÔNG có ô nhập
   nên bé phải tự chấm, và cổng này cũng không đếm chúng. Nay cho bấm chọn (đáp án là
   lời đọc chứ không phải con số, nên theo luật ô nhập phải là nút bấm) — thêm đúng
   hai câu máy chấm được. `dungKhiDungDap` cũng +2, nghĩa là cả hai chấm đúng, và
   `dungKhiSaiDap`/`tuDoiChieu` vẫn đứng yên ở 1 và 1. */
/* ⚠ 2275 → 2303. Chương 5 tách ba bài thành sáu. Đo lại chính ba mã cũ:
       trước  26 câu luyện tập chấm máy được (một câu vốn để bé tự chấm)
       sau    54 câu  ·  lệch +28  ·  2275 + 28 = 2303  ✓
   Đã soát: `git diff` trên `src/mon/toan/lib/` và `src/chung/` trống trơn;
   `dungKhiSaiDap` và `tuDoiChieu` vẫn đứng yên ở 1 và 1. */
/* ⚠ 2303 → 2332. Chương 6 tách bốn bài thành bảy. Đo lại:
       luyện tập chương 6   36 → 63 câu chấm máy   (+27)
       kỳ ôn 6              22 → 24 câu chấm máy   (+2, hai câu cũ chưa có ô nhập)
                                          cộng  +29  ·  2303 + 29 = 2332  ✓
   Đã soát: `git diff` trên `src/mon/toan/lib/` và `src/chung/` trống trơn;
   `dungKhiSaiDap` và `tuDoiChieu` vẫn đứng yên ở 1 và 1. */
const MOC = { tong: 2332, dungKhiDungDap: 2330, dungKhiSaiDap: 1, tuDoiChieu: 1 };

const nay = diemDanh();
console.log(`   ${nay.tong} câu Toán · đưa đáp án đúng → ${nay.dungKhiDungDap} chấm đúng`
  + ` · đưa đáp án sai → ${nay.dungKhiSaiDap} vẫn được tính đúng`
  + ` · ${nay.tuDoiChieu} câu tự đối chiếu`);

if (MOC.tong === 0) {
  console.log('   ⚠ CHƯA NIÊM PHONG — chép con số trên vào `MOC` rồi chạy lại.');
} else {
  for (const k of Object.keys(MOC)) {
    t(`Toán không đổi · ${k} = ${MOC[k]} (đo được ${nay[k]})`, nay[k] === MOC[k]);
  }
}

console.log('\n── viết tắt KHÔNG có dấu nháy ──');
{
  /* Bác dặn 13-08: chấm phải bỏ khoảng trắng thừa và không phân biệt hoa thường
     thì độ chính xác mới đảm bảo. Đo lại thì ba việc ấy đã có sẵn — nhưng lộ ra
     một chỗ SAI THẬT: bộ nhận dạng hay trả về dạng viết tắt KHÔNG có dấu nháy.

         mẫu "Hi, I'm Bill."  ·  bé nói đúng y hệt  ·  máy nghe ra "hi im bill"
         → chỉ 7/10

     Bé nói đúng mà bị trừ điểm vì cái máy gõ thiếu một dấu nháy. Đó là chấm SAI,
     không phải chấm chặt. */
  const cap = [
    ["Hi, I'm Bill.", 'hi im bill'],
    ["Hi, I'm Bill.", 'HI   IM   BILL'],
    ["I don't like fish.", 'i dont like fish'],
    ["It's a cat.", 'its a cat'],
    ["Let's go.", 'lets go'],
  ];
  for (const [dich, nghe] of cap) {
    const d = chamCau(dich, nghe).diem;
    t(`"${dich}" vs "${nghe}" → ${d}/10`, d === 10);
  }
  /* Hoa thường và khoảng trắng thừa — bác nhắc riêng, nên soi riêng. */
  t('viết hoa không ảnh hưởng', chamTu('ball', '  BALL  ').diem === 10);
  t('dấu câu không ảnh hưởng', chamTu('chips', 'Chips!').diem === 10);
  t('khoảng trắng thừa không ảnh hưởng', chamCau('I like milk.', '  I   LIKE   MILK ').diem === 10);

  /* BỎ HẲN DẤU CÁCH khi so — bác dặn riêng, và đo ra lỗi thật: bộ nhận dạng tách
     chỗ cách theo ý nó chứ không theo sách. Bé nói đúng y hệt, chỉ khác chỗ cách,
     mà chỗ cách thì bé có nói ra đâu. */
  t('"teddy bear" vs "teddybear" → 10', chamTu('teddy bear', 'teddybear').diem === 10);
  t('"goodbye" vs "good bye" → 10', chamTu('goodbye', 'good bye').diem === 10);
  t('câu: "I like milk." vs "ilikemilk" → 10', chamCau('I like milk.', 'ilikemilk').diem === 10);
  /* Nhưng KHÔNG được nới thành "bỏ cách rồi đo độ giống": câu khác vẫn phải khác. */
  t('câu KHÁC vẫn bị trừ điểm', chamCau('I like milk.', 'I like fish.').diem < 8);

  /* KHÔNG được nhận nhầm: `were` là một từ thật, đừng bung thành "we are". */
  t('"were" giữ nguyên, không bung thành "we are"',
    chuanHoa('they were here') === 'they were here');
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
