/**
 * CỔNG GÁC DANH SÁCH ÂM — luật "MỖI DÒNG MỘT THỨ TIẾNG".
 * chạy: node test/tienganh_am.test.mjs
 *
 * ── VÌ SAO ──
 * Dây chuyền âm dùng HAI model: Kokoro-82M chỉ đọc tiếng Anh, Kokoro-Vietnamese chỉ
 * đọc tiếng Việt. Một dòng lẫn hai thứ tiếng thì model nào đọc cũng sai:
 *
 *     "Con bấm vào hình con dog nhé."  →  Kokoro-VI đọc "dog" theo vần Việt: /dóc/
 *
 * Cái hỏng ở đây KHÔNG dừng chương trình. Model vẫn ra tiếng, tệp mp3 vẫn đúng định
 * dạng, sổ tra vẫn đầy đủ. Chỉ đến lúc bé đeo tai nghe mới lộ — mà lúc ấy đã 520
 * clip rồi. Nên phải chặn ở DANH SÁCH, trước khi sinh.
 *
 * `tools/tts/sinh_am.py` cũng soát đúng luật này trước khi nạp model. Hai chỗ soát
 * là cố ý: cổng bắt lúc sửa dữ liệu, script bắt lúc chạy tay với tệp chưa qua cổng.
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const R = new URL('../../', import.meta.url).pathname;
const TA = join(R, 'data/tienganh');
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

/** Chữ Việt CÓ DẤU — dấu hiệu chắc chắn nhất của một dòng tiếng Việt. */
const CO_DAU = /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i;

/**
 * Chữ Việt KHÔNG dấu hay lọt vào câu tiếng Anh mà mắt thường bỏ qua.
 * Cố ý KHÔNG có "can" — đó là từ tiếng Anh thật của Unit 3 (cái lon).
 */
/* Chữ Việt không dấu KHÁC, gặp trong nghĩa của từ vựng. Danh sách này chỉ để phép
   đoán ngôn ngữ bớt báo oan — thêm chữ vào đây không nới lỏng gì về nội dung. */
const VIET_KHAC = new Set([
  'anh', 'em', 'trai', 'chi', 'ba', 'ma', 'bo', 'me', 'ong', 'ban',
  'cam', 'canh', 'xanh', 'do', 'den', 'hoa', 'qua', 'cai', 'chim', 'ca',
  'xem', 'ti', 'vi', 'tivi', 'nam', 'lam', 'tay', 'chan', 'sao', 'hai',
]);

const VIET_KHONG_DAU = new Set([
  'con', 'cua', 'cho', 'va', 'la', 'co', 'khong', 'nhe', 'hay', 'bam',
  'nghe', 'nhin', 'chon', 'dung', 'sai', 'roi', 'moi', 'hinh', 'tu', 'cau',
]);

/**
 * Từ CHỨC NĂNG tiếng Anh — thứ không bao giờ đứng lẻ trong một câu tiếng Việt.
 * Cố ý chỉ lấy từ chức năng, không lấy danh từ: "dog" có thể xuất hiện hợp lệ
 * trong một câu Việt đang NHẮC TỚI từ ấy, còn "in the" thì không.
 */
const EN_CHUC_NANG = new Set([
  'the', 'a', 'an', 'is', 'are', 'am', 'this', 'that', 'these', 'those',
  'in', 'on', 'at', 'to', 'of', 'my', 'your', 'his', 'her', 'its',
  'i', 'you', 'he', 'she', 'it', 'we', 'they', "i'm", "he's", "she's", "it's",
  'can', 'have', 'has', 'do', 'does', 'and', 'or', 'how', 'many', 'what',
  'there', 'look', 'point', 'touch', 'like', 'see', 'hello', 'hi', 'bye',
]);

/** @returns lời báo lỗi, hoặc null nếu dòng dùng được. Cùng luật với sinh_am.py. */
function soatDong(m) {
  const chu = String(m?.chu ?? '').trim();
  if (!chu) return 'chữ rỗng';
  if (m.tieng !== 'en' && m.tieng !== 'vi') return `tiếng phải là 'en' hoặc 'vi', đang là ${JSON.stringify(m.tieng)}`;

  if (m.tieng === 'en') {
    if (CO_DAU.test(chu)) return `khai 'en' mà có chữ Việt CÓ DẤU: "${chu}"`;
    const lot = [...new Set((chu.toLowerCase().match(/[a-z]+/g) || []))]
      .filter((w) => VIET_KHONG_DAU.has(w));
    /* Một từ trùng nhau là chuyện thường ("top" vừa là tiếng Anh vừa gần giống chữ
       Việt); HAI từ trở lên thì đúng là câu tiếng Việt khai nhầm. */
    if (lot.length >= 2) return `khai 'en' mà nhiều chữ Việt không dấu (${lot.join(', ')}): "${chu}"`;
  } else {
    /* ⚠ "Không chữ nào có dấu" KHÔNG đủ để kết luận là tiếng Anh. Tiếng Việt có
       hẳn một lớp từ không dấu, và nghĩa của `brother` là "anh, em trai" — ba từ,
       không từ nào có dấu, mà vẫn là tiếng Việt trăm phần trăm. Lớp 2 báo đỏ đúng
       hai dòng như thế.

       Nên đòi thêm một dấu hiệu ĐỘC LẬP: có chữ nào KHÔNG PHẢI tiếng Việt không?
       Chuỗi mà mọi chữ đều đọc được bằng vần Việt thì Kokoro-VI đọc ra vẫn đúng —
       đó mới là điều phép kiểm này thật sự lo. */
    const chuCai = (chu.toLowerCase().match(/[a-z]+/g) || []);
    const laVietDuoc = (w) => VIET_KHONG_DAU.has(w) || VIET_KHAC.has(w);
    if (!CO_DAU.test(chu) && chuCai.length >= 3 && !chuCai.every(laVietDuoc)) {
      return `khai 'vi' mà không chữ nào có dấu: "${chu}"`;
    }
    /* Chỗ này bản đầu để lọt, và lọt đúng một dòng do chính bộ sinh đẻ ra:
           "Cảnh hôm nay: In the bedroom."
       Câu có dấu tiếng Việt nên qua được phép kiểm trên, mà bên trong vẫn là một
       mẩu tiếng Anh — Kokoro-VI sẽ đọc "In the bedroom" theo vần Việt.
       Bắt bằng CỤM: hai từ chức năng tiếng Anh đứng gần nhau thì đó là tiếng Anh,
       chứ một từ trùng nhau ("in", "an") thì còn có thể là tình cờ. */
    /* Tách từ theo CHỮ CÁI UNICODE, rồi mới lọc lấy từ thuần ASCII.
       Bản đầu tách bằng /[a-z']+/ nên "cái cửa" vỡ thành c·i·c·a, và "i" với "a"
       bị chấm là tiếng Anh — báo oan đúng một nghĩa từ hợp lệ. Phép kiểm báo oan
       thì nguy hơn phép kiểm bỏ sót, vì lần sau người ta tắt nó đi. */
    const en = [...new Set(chu.toLowerCase().match(/[\p{L}']+/gu) || [])]
      .filter((w) => /^[a-z']+$/.test(w) && EN_CHUC_NANG.has(w));
    if (en.length >= 2) return `khai 'vi' mà có cụm tiếng Anh (${en.join(' ')}): "${chu}"`;
  }
  return null;
}

/* ══ 1 · LUẬT SOÁT PHẢI THẬT SỰ BẮT ĐƯỢC ══
   Phép kiểm cho chính phép kiểm. Một cổng không ai thử thì rất dễ là cổng luôn xanh. */
const PHAI_BAT = [
  { chu: 'Con bấm vào hình con dog nhé.', tieng: 'en' },
  { chu: 'This is a dog.', tieng: 'vi' },
  { chu: 'con nghe roi bam vao hinh', tieng: 'en' },
  { chu: '', tieng: 'en' },
  { chu: 'dog', tieng: 'eng' },
  /* Dòng này bản đầu của cổng ĐỂ LỌT, và nó do chính bộ sinh đẻ ra. Giữ lại đây
     làm phép kiểm vĩnh viễn — lỗi đã lọt một lần thì phải có chỗ canh mãi. */
  { chu: 'Cảnh hôm nay: In the bedroom.', tieng: 'vi' },
  { chu: 'Mẫu câu: This is a + [Noun].', tieng: 'vi' },
];
const PHAI_THA = [
  { chu: 'dog', tieng: 'en' },
  { chu: 'teddy bear', tieng: 'en' },
  { chu: 'How many windows can you see? - I can see six.', tieng: 'en' },
  { chu: 'This is my bag.', tieng: 'en' },
  { chu: 'con chó', tieng: 'vi' },
  { chu: 'Con nghe rồi bấm vào hình đúng nhé.', tieng: 'vi' },
  { chu: 'Giỏi lắm! Con được ba ngôi sao.', tieng: 'vi' },
];
const lotLuoi = PHAI_BAT.filter((m) => !soatDong(m)).map((m) => JSON.stringify(m));
t(`7 dòng hỏng đều bị bắt (${lotLuoi.length} lọt lưới)`, lotLuoi.length === 0);
in5(lotLuoi);
const baoOan = PHAI_THA.map((m) => [m, soatDong(m)]).filter(([, s]) => s)
  .map(([m, s]) => `"${m.chu}" → ${s}`);
t(`7 dòng đúng không bị báo oan (${baoOan.length} oan)`, baoOan.length === 0);
in5(baoOan);

/* ══ 2 · SOÁT MỌI DANH SÁCH ÂM CÓ THẬT ══
   Quét cả thư mục, không gõ tay tên tệp: thêm lớp 2 là bị soi ngay, không ai phải
   nhớ đăng ký. Chưa có tệp nào thì cổng nói ra chứ không lặng lẽ xanh. */
const dsAm = existsSync(TA)
  ? readdirSync(TA).filter((f) => /^lop\d+_loi\.json$/.test(f))
  : [];
if (!dsAm.length) {
  console.log('   ⏸ chưa có data/tienganh/lopN_loi.json nào — chưa tới bước sinh âm');
} else {
  for (const f of dsAm) {
    const dong = JSON.parse(readFileSync(join(TA, f), 'utf8'));
    const loi = dong.map((m, i) => [m.id || `#${i}`, soatDong(m)])
      .filter(([, s]) => s).map(([i, s]) => `${i}: ${s}`);
    t(`${f} · mỗi dòng một thứ tiếng (${dong.length} dòng, ${loi.length} hỏng)`, loi.length === 0);
    in5(loi);

    /* id trùng nhau thì clip sau ĐÈ clip trước — mất tiếng một câu, không ai báo. */
    const dem = {};
    for (const m of dong) dem[m.id] = (dem[m.id] || 0) + 1;
    const trung = Object.entries(dem).filter(([, n]) => n > 1).map(([i, n]) => `${i} ×${n}`);
    t(`${f} · không id nào trùng (${trung.length})`, trung.length === 0);
    in5(trung);
  }
}

/* ══ 2B · HAI HÀM ĐẶT MÃ PHẢI RA CÙNG MỘT CHUỖI ══
   `tools/tts/sinh_am.py` đặt tên clip, còn `NutNghe.jsx` tra lại clip ấy. Hai bên
   viết bằng hai ngôn ngữ, và lệch MỘT ký tự là nút nghe biến mất — màn hình vẫn đủ
   chữ, chỉ là câm, nên không ai biết cho tới lúc bé bấm.

   Đã lệch thật: Python đổi MỖI ký tự lạ thành MỘT gạch, còn bản JS đầu tiên gộp
   chuỗi gạch liền nhau. ": " ra "__" bên này và "_" bên kia, thế là mọi lời giảng
   mất tiếng. Nên soi bằng cách tính lại mã từ CHỮ rồi so với mã trong danh sách. */
const maJS = (chu, tieng) => {
  const sach = [...String(chu).toLowerCase()]
    .map((c) => (/[\p{L}\p{N}]/u.test(c) ? c : '_')).join('').replace(/^_+|_+$/g, '');
  return `${tieng === 'vi' ? 'loi' : 'cau'}_${sach}`.slice(0, 60);
};
for (const f of dsAm) {
  const dong = JSON.parse(readFileSync(join(TA, f), 'utf8'));
  /* Chỉ soi dòng do `doanAm` sinh ra (tiền tố loi_ và cau_) — từ vựng và nghĩa
     dùng tiền tố khác (tu_, nghia_) và được tra bằng mã ghi sẵn trong bài. */
  const soi = dong.filter((m) => /^(loi|cau)_/.test(m.id));
  const lech = soi.filter((m) => maJS(m.chu, m.tieng) !== m.id)
    .map((m) => `${m.id} ≠ ${maJS(m.chu, m.tieng)} ("${m.chu.slice(0, 40)}")`);
  t(`${f} · mã clip của JS khớp mã của Python (${soi.length} dòng, ${lech.length} lệch)`,
    lech.length === 0);
  in5(lech);
}

/* ══ 3 · SỔ TRA PHẢI NẰM ĐÚNG NƠI SỔ ĐĂNG KÝ CHỈ TỚI, VÀ KHỚP DANH SÁCH ══

   Chỗ này đã hỏng thật, và hỏng theo kiểu khó thấy nhất. Sổ âm nằm ở
   `data/tienganh/lop1_am.json`, còn app đọc theo đường khai trong sổ đăng ký —
   tức là dưới `web/public/content/`. Tệp không có ở đó, máy chủ dev trả về
   `index.html` thay thế, và `fetch` báo **200**. Nên:

     · curl thấy 200 → tưởng có tệp;
     · `r.ok` là true → mã nguồn đi tiếp;
     · `r.json()` mới vỡ, mà chỗ ấy lại có `catch` → nuốt lỗi, trả sổ rỗng;
     · mọi nút nghe tra ra null rồi TỰ ẨN — cả quyển câm, màn hình vẫn đủ chữ.

   Nên phép kiểm phải hỏi ĐÚNG câu app hỏi: theo đường trong sổ đăng ký, có tệp
   thật không — và mỗi clip nó khai có tệp mp3 thật không. */
const DK = JSON.parse(readFileSync(join(R, 'web/public/content/chuong_trinh.json'), 'utf8'));
const CT_AM = Object.values(DK.chuongTrinh || {}).filter((c) => c.am?.so);
for (const c of CT_AM) {
  const soTep = join(R, 'web/public/content', c.am.so);
  t(`${c.ma}: sổ âm có thật ở đúng đường sổ đăng ký khai (${c.am.so})`, existsSync(soTep));
  if (!existsSync(soTep)) continue;
  const so = JSON.parse(readFileSync(soTep, 'utf8'));
  const thieuTep = (so.clip || [])
    .filter((x) => !existsSync(join(R, 'web/public/content', c.am.thuMuc, x.tep)))
    .map((x) => x.tep);
  t(`${c.ma}: ${so.clip?.length || 0} clip đều có tệp mp3 (${thieuTep.length} thiếu)`,
    thieuTep.length === 0);
  in5(thieuTep);
}

/* Sửa chữ mà quên sinh lại clip thì bé nghe một đằng, đọc một nẻo. Vân tay bắt được. */
for (const f of dsAm) {
  const ct = CT_AM.find((c) => c.am.so.includes(f.replace('_loi.json', '_am.json')));
  const soTep = ct ? join(R, 'web/public/content', ct.am.so) : '';
  if (!soTep || !existsSync(soTep)) {
    console.log(`   ⏸ ${f}: chưa sinh âm`);
    continue;
  }
  const dong = JSON.parse(readFileSync(join(TA, f), 'utf8'));
  const so = JSON.parse(readFileSync(soTep, 'utf8'));
  const theoId = Object.fromEntries((so.clip || []).map((c) => [c.id, c]));
  const lech = [];
  for (const m of dong) {
    const c = theoId[m.id];
    if (!c) { lech.push(`${m.id}: chưa có clip`); continue; }
    if (c.tieng !== m.tieng) lech.push(`${m.id}: sổ ghi tiếng "${c.tieng}" ≠ "${m.tieng}"`);
    if (c.chu !== m.chu) lech.push(`${m.id}: chữ đã sửa mà chưa sinh lại clip`);
  }
  t(`${f} · sổ âm khớp danh sách (${lech.length} lệch)`, lech.length === 0);
  in5(lech);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
