/**
 * CỔNG BẢN ĐỒ CHỦ ĐỀ — trục thứ hai của app: xem & luyện theo CHỦ ĐỀ xuyên các lớp.
 * chạy: node test/chu_de.test.mjs
 *
 * `chu_de.json` do tools/dung_chu_de.py suy ra từ data/km_v1_38.json. Suy ra nghĩa
 * là sai lặng lẽ: một mã bài dịch hụt thì bé bấm vào bậc thang mà không mở được gì,
 * mà giao diện vẫn vẽ đủ nút. Cổng này soi đúng mấy chỗ ấy.
 *
 * ĐƯỜNG LÙI THEO CHỦ ĐỀ khác đường lùi ở màn kết mỗi bài:
 *   · màn kết   — "bài này dựng trên bài kia" (quan hệ BÀI NỀN, sách chỉ đích danh)
 *   · thang này — "bài này dạy chủ đề ấy"     (quan hệ THÀNH VIÊN)
 * Trộn hai thứ lại thì bé trượt "lập số lớn nhất" bị đẩy sang bài chia có dư — đã
 * thử và phải bỏ, xem lời mở đầu tools/dung_chu_de.py.
 */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const D = new URL('../public/content/', import.meta.url).pathname;
const bd = JSON.parse(readFileSync(join(D, 'chu_de.json'), 'utf8'));
const dk = JSON.parse(readFileSync(join(D, 'chuong_trinh.json'), 'utf8'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const mang = bd.mang || {}, chuDe = bd.chuDe || {}, dang = bd.dang || {};
t(`có mảng kiến thức (${Object.keys(mang).length})`, Object.keys(mang).length === 5);
t(`có chủ đề (${Object.keys(chuDe).length})`, Object.keys(chuDe).length === 34);
t(`có dạng bài (${Object.keys(dang).length})`, Object.keys(dang).length === 82);

/* ── Cây phải KHÉP KÍN hai chiều. Nút mồ côi thì hoặc giao diện vẽ ra một mục bấm
      vào rỗng, hoặc một dạng bài biến mất khỏi danh sách mà không ai biết. */
t('mọi chủ đề nêu trong mảng đều có thật',
  Object.values(mang).every((m) => (m.chuDe || []).every((k) => chuDe[k])));
t('mọi dạng bài nêu trong chủ đề đều có thật',
  Object.values(chuDe).every((c) => (c.dang || []).every((k) => dang[k])));
t('chủ đề nào cũng được đúng mảng của nó nhận',
  Object.entries(chuDe).every(([k, c]) => (mang[`AREA:${c.mang}`]?.chuDe || []).includes(k)));
t('dạng bài nào cũng được đúng chủ đề của nó nhận',
  Object.entries(dang).every(([k, d]) => (chuDe[d.chuDe]?.dang || []).includes(k)));

/* ── Mã bài trong thang phải MỞ ĐƯỢC. Đây là phép kiểm quan trọng nhất: bản đồ gọi
      bài là 'LESSON:TTD2.B1', app gọi 'DL:KSN2.B01' — khác tiền tố VÀ khác cách đệm
      số 0. Dịch hụt một chỗ là bậc thang trỏ vào hư không. */
const co = new Set();
for (const ct of Object.values(dk.chuongTrinh || {})) {
  const idx = join(D, ct.thuMuc, 'index.json');
  if (existsSync(idx)) {
    for (const b of JSON.parse(readFileSync(idx, 'utf8'))) co.add(b.id);
  }
}
const idFile = (id) => id.replace(/^DL:/, 'DL_').replace(/\./g, '_') + '.json';
const moDuoc = (id) => co.has(id)
  || existsSync(join(D, 'lessons', idFile(id)));

const bacs = Object.values(dang).flatMap((d) => d.thang || []);
const baiHong = bacs.flatMap((b) => b.bai.filter((i) => !moDuoc(i)));
t(`mọi mã bài trong thang đều mở được (${bacs.reduce((s, b) => s + b.bai.length, 0)} mã)`,
  baiHong.length === 0);
if (baiHong.length) console.log('     ', baiHong.slice(0, 6).join(', '));

t('bậc nào cũng có tên bài khớp số lượng mã bài',
  bacs.every((b) => (b.ten || []).length === b.bai.length));
t('bậc xếp từ lớp THẤP lên CAO',
  Object.values(dang).every((d) =>
    (d.thang || []).every((b, k, a) => k === 0 || a[k - 1].lop < b.lop)));

/* ── Lớp 5 phải trỏ vào MICRO, không phải bài sách: bé mở micro, không mở bài. */
t('bậc lớp 5 trỏ vào micro (…B<n>.M<k>)',
  bacs.filter((b) => b.lop === 5).every((b) => b.bai.every((i) => /\.M\d+$/.test(i))));
t('bậc lớp 2·3·4 trỏ vào bài (…B<nn>)',
  bacs.filter((b) => b.lop < 5).every((b) => b.bai.every((i) => /\.B\d+$/.test(i))));

/* ── Lời giới thiệu theo lớp: có bậc ở lớp nào thì phải có lời cho lớp ấy, không thì
      màn thang hiện một dòng trống. */
t('dạng bài nào cũng có lời giới thiệu cho mọi lớp nó có bậc',
  Object.values(dang).every((d) =>
    (d.thang || []).every((b) => (d.moTaLop || {})[String(b.lop)])));

/* ── ĐƯỜNG LÙI: dạng nào có ≥2 bậc thì mới lùi được. Con số này tụt là bản đồ hỏng
      thầm — thang vẫn dựng ra, chỉ là không còn chỗ nào để lùi. */
const nhieuBac = Object.values(dang).filter((d) => (d.thang || []).length >= 2);
t(`≥ 60 dạng bài có từ 2 bậc trở lên (${nhieuBac.length})`, nhieuBac.length >= 60);

/* ── Tên đầy đủ lấy từ Excel: không dạng nào được để tên rỗng. */
t('dạng bài nào cũng có tên', Object.values(dang).every((d) => (d.ten || '').trim()));
t('chủ đề nào cũng có tên', Object.values(chuDe).every((c) => (c.ten || '').trim()));

/* ── MÙA GIẢI ĐI TRỤC RIÊNG, KHÔNG LẪN VÀO THANG ──
   `thang[].bai` phải là bài HỌC ĐƯỢC: vòng luyện gọi `loadLesson` rồi rút câu từ
   `practice.pools`. Tệp Mùa giải mang tiền tố `DR_`, có `man`/`cau` chứ không có
   `practice.pools`, và chạy bằng `DauPlayer.jsx`. Lọt một mã `DR:` vào thang là bé
   bấm vào gặp màn trắng — mà dữ liệu vẫn hợp lệ nên KHÔNG phép kiểm nào khác báo. */
const trongThang = bacs.flatMap((b) => b.bai).filter((x) => String(x).startsWith('DR:'));
t(`không mã Mùa giải nào lọt vào thang (${trongThang.length})`, trongThang.length === 0);

const mgs = Object.values(dang).flatMap((d) => d.muaGiai || []);
t('có trục Mùa giải', mgs.length > 0);
t('khối đấu nào cũng mang mã DR:', mgs.every((x) => String(x.khoi).startsWith('DR:')));
t('khối đấu nào cũng nói rõ mấy bẫy trúng chủ đề',
  mgs.every((x) => x.soBay >= 1 && x.soBay <= x.tongBay));
t('mỗi dạng không mời trùng một khối hai lần',
  Object.values(dang).every((d) => {
    const ds = (d.muaGiai || []).map((x) => x.khoi);
    return new Set(ds).size === ds.length;
  }));

/* ── BẢNG TRA NGƯỢC `baiDang` ──
   Sổ cô giáo đóng dấu dạng bài lên từng lượt trả lời bằng bảng này. Nó phải KHỚP
   HAI CHIỀU với bảng `dang`: thiếu một chiều là có bài lọt sổ mà không ai hay. */
const baiDang = bd.baiDang || {};
t('có bảng tra ngược baiDang', Object.keys(baiDang).length > 250);

const xuoi = new Map();                       // bài → dạng, dựng lại từ bảng `dang`
for (const [ma, d] of Object.entries(dang)) {
  for (const b of d.thang || []) for (const x of b.bai) {
    if (!xuoi.has(x)) xuoi.set(x, new Set());
    xuoi.get(x).add(ma);
  }
}
const lech = [];
for (const [b, ds] of xuoi) {
  const co = new Set(baiDang[b] || []);
  for (const m of ds) if (!co.has(m)) lech.push(`${b} thiếu ${m}`);
}
for (const [b, ds] of Object.entries(baiDang)) {
  for (const m of ds) if (!xuoi.get(b)?.has(m)) lech.push(`${b} thừa ${m}`);
}
t(`baiDang khớp hai chiều với bảng dạng (lệch: ${lech.length})`, lech.length === 0);
lech.slice(0, 5).forEach((x) => console.log('     ', x));
t('mã dạng trong baiDang đều có thật',
  Object.values(baiDang).every((ds) => ds.every((m) => dang[m])));

/* ── BẬC PHẢI RÚT RA ĐƯỢC CÂU, KHÔNG CHỈ MỞ ĐƯỢC TỆP ──
 *
 * Phép trên hỏi "mã bài này có tệp không". Đó là câu hỏi ĐÚNG nhưng CHƯA ĐỦ, và chỗ
 * hụt đúng bằng chỗ đã hụt với mã Mùa giải ở trên: `LuyenChuDe.jsx` nạp bài rồi rút
 * câu từ `practice.pools`, chỉ lấy câu CÓ `answerKey`. Tệp có thật mà hồ chứa rỗng
 * thì bé bấm vào bậc và gặp một vòng luyện không câu nào — dữ liệu hợp lệ, cổng
 * xanh, màn trắng.
 *
 * Đếm y hệt `cauCua` bên ấy: ba hồ warmup · standard · challenge, lọc `answerKey`.
 * Đổi cách rút câu bên kia mà quên chỗ này thì con số dưới đây lệch, và nó lệch to
 * chứ không lệch thầm.
 */
const HO = ['warmup', 'standard', 'challenge'];
const demCau = (b) => HO.reduce((n, h) =>
  n + ((b?.practice?.pools?.[h] || []).filter((c) => c.answerKey).length), 0);
const doc = (id) => {
  for (const ct of Object.values(dk.chuongTrinh || {})) {
    const f = join(D, ct.thuMuc, idFile(id));
    if (existsSync(f)) return JSON.parse(readFileSync(f, 'utf8'));
  }
  return null;
};
const cauCuaBac = (b) => b.bai.reduce((n, id) => n + demCau(doc(id)), 0);
const bacRong = bacs.filter((b) => cauCuaBac(b) === 0);
t(`bậc nào cũng rút ra được câu chấm máy (rỗng: ${bacRong.length})`, bacRong.length === 0);
bacRong.slice(0, 5).forEach((b) => console.log('     ', b.lop, b.bai.join(', ')));

/* Dưới SO_CAU thì vòng luyện vẫn chạy, chỉ là ngắn hơn thiết kế — `LuyenChuDe` tự
   hạ ngưỡng theo số câu thật, và dưới 3 câu thì nó mời học thẳng bài. Nên đây KHÔNG
   phải lỗi, mà là món nợ niêm phong: chỉ được giảm. Nhích lên là có bậc vừa mỏng đi. */
const SO_CAU = 6;
const NO_MONG = 17;
const bacMong = bacs.filter((b) => { const n = cauCuaBac(b); return n > 0 && n < SO_CAU; });
t(`bậc dưới ${SO_CAU} câu không được nhiều hơn ${NO_MONG} (đang ${bacMong.length})`,
  bacMong.length <= NO_MONG);
if (bacMong.length < NO_MONG) {
  console.log(`     ↓ đã dày thêm: ${bacMong.length}/${NO_MONG} — hạ NO_MONG xuống để chốt.`);
}

/* Đảo chiều: hai phép trên chỉ có nghĩa nếu bộ đếm THẬT SỰ đếm ra câu. Đếm ra 0 câu
   ở mọi bậc thì "không bậc nào rỗng" là câu nói suông. */
const tongCau = bacs.reduce((s, b) => s + cauCuaBac(b), 0);
t(`bộ đếm có đếm ra câu thật (${tongCau} câu chấm máy đi từ chủ đề tới được)`,
  tongCau > 1000);

const trong = Object.entries(dang).filter(([, d]) => !(d.thang || []).length);
const tongBai = bacs.reduce((s, b) => s + b.bai.length, 0);
const theoLop = {};
for (const b of bacs) theoLop[b.lop] = (theoLop[b.lop] || 0) + 1;

console.log(`\n   5 mảng · 34 chủ đề · 82 dạng bài · ${tongBai} mối nối bài`
  + ` · ${nhieuBac.length} dạng lùi được`);
console.log('   bậc theo lớp: '
  + Object.entries(theoLop).map(([l, n]) => `lớp ${l}: ${n}`).join(' · '));
if (trong.length) {
  console.log(`   ⏸ ${trong.length} dạng bài ma trận có mà chưa quyển nào dạy: `
    + trong.map(([k]) => k).join(', '));
}
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
