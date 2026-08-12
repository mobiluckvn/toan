/**
 * SOÁT PHẦN BÙ DỮ LIỆU TIẾNG ANH LỚP 1.
 * chạy: node test/tienganh_lop1_bu.test.mjs
 *
 * `data/tienganh/lop1_bu.json` là lớp đắp lên bản đồ tri thức — nó khớp với bản đồ
 * bằng ID NODE. Khớp bằng id thì gõ sai một ký tự là mục ấy nằm im: bản đồ vẫn có
 * từ, phần bù vẫn có nghĩa, mà hai bên không gặp nhau. Bé mở bài ra thấy từ tiếng
 * Anh không có nghĩa — hỏng kiểu câm, không ai báo.
 *
 * Tệp này bắt đúng chỗ ấy: mọi id phải TRỎ VÀO ĐÚNG NODE CÓ THẬT, và mọi node phải
 * ĐƯỢC BÙ ĐỦ. Thiếu một trong hai chiều là đỏ.
 *
 * Nó cũng canh những gì phần bù hứa sẽ chặn: 5 unit nguyên âm phải được sửa
 * `position`, mọi mẫu câu nhiều ô phải khai vai cho từng ô, mọi từ phải gõ được.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const R = new URL('../../', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const bando = JSON.parse(readFileSync(`${R}data/ban_do_tieng_anh.json`, 'utf8'));
const bu = JSON.parse(readFileSync(`${R}data/tienganh/lop1_bu.json`, 'utf8'));

const N = Object.fromEntries(bando.graph.nodes.map((n) => [n.id, n]));
const g1 = bando.graph.nodes.filter((n) => String(n.grade) === '1');
const tuBanDo = g1.filter((n) => n.node_kind === 'vocabulary');
const phBanDo = g1.filter((n) => n.node_kind === 'phonics');
const spBanDo = g1.filter((n) => n.node_kind === 'sentence_pattern');

/* ══ 1 · ĐỦ CẢ HAI CHIỀU ══ */
const idBu = Object.keys(bu.tu);
const thieu = tuBanDo.filter((n) => !bu.tu[n.id]).map((n) => `${n.id} (${n.word})`);
const thua = idBu.filter((id) => !N[id]);
t(`bù đủ ${tuBanDo.length} từ của bản đồ (thiếu ${thieu.length})`, thieu.length === 0);
in5(thieu);
t(`không id nào trỏ vào hư không (thừa ${thua.length})`, thua.length === 0);
in5(thua);

/* Chữ `word` trong phần bù phải KHỚP bản đồ — nếu không thì đang bù nhầm node.
   Đây là phép kiểm bắt được lỗi mà "id có tồn tại" bỏ lọt. */
const lechChu = idBu.filter((id) => N[id] && N[id].word !== bu.tu[id].word)
  .map((id) => `${id}: bản đồ "${N[id].word}" ≠ phần bù "${bu.tu[id].word}"`);
t(`chữ trong phần bù khớp bản đồ (${lechChu.length} lệch)`, lechChu.length === 0);
in5(lechChu);

/* ══ 2 · MỌI TỪ ĐỀU CÓ ĐỦ BA THỨ ══ */
const VAI_HOP_LE = ['dt', 'dongtu', 'mau', 'bophan', 'thucan', 'sonhieu', 'khongdem', 'so', 'ten'];
const khuyet = [];
for (const [id, x] of Object.entries(bu.tu)) {
  if (!x.nghia || !x.nghia.trim()) khuyet.push(`${id}: thiếu nghĩa`);
  if (!x.ipa || !/^\/.+\/$/.test(x.ipa)) khuyet.push(`${id}: IPA thiếu hoặc không có hai dấu /`);
  if (!Array.isArray(x.vai) || !x.vai.length) khuyet.push(`${id}: thiếu vai từ loại`);
  else for (const v of x.vai) if (!VAI_HOP_LE.includes(v)) khuyet.push(`${id}: vai lạ "${v}"`);
}
t(`60 từ đều có nghĩa · IPA · vai (${khuyet.length} chỗ khuyết)`, khuyet.length === 0);
in5(khuyet);

/* Nghĩa tiếng Việt phải CÓ DẤU. Đây đúng là lỗi đang làm hỏng lớp 4 (233/233 từ
   nghĩa không dấu) — chặn ngay ở lớp 1 để nó không lặp lại. */
const CO_DAU = /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i;
const khongDau = Object.entries(bu.tu).filter(([, x]) => !CO_DAU.test(x.nghia))
  .map(([id, x]) => `${id}: "${x.nghia}"`);
/* Vài nghĩa vốn không có chữ nào mang dấu ("mẹ" có, "cá" có, nhưng "bố" có…).
   Ngưỡng: quá 1/4 số từ không dấu là dấu hiệu ai đó dán nguyên bản không dấu vào. */
t(`nghĩa tiếng Việt CÓ DẤU (${khongDau.length}/${idBu.length} không dấu)`,
  khongDau.length <= idBu.length / 4);
in5(khongDau);

/* ══ 3 · BẪY position — VỊ TRÍ ÂM LÀ CHUYỆN CỦA TỪNG TỪ ══
   Bản đầu của phần bù sửa `position` theo UNIT, và cổng này bắt được là vẫn sai:
   U3 có `apple` (âm ở đầu) lẫn `bag·can·hat` (âm ở giữa), U13 có `noodles·nuts`
   (đầu) lẫn `bananas` (giữa). Nên bây giờ soát TỪNG TỪ, và soát bằng cách TỰ SUY
   RA sự thật từ chữ chứ không tin lời khai. */
t('bản đồ vẫn khai cả 16 phonics là "initial" (bản đồ mà sửa rồi thì bỏ phần bù đi)',
  phBanDo.every((p) => p.position === 'initial'));

/** Chữ cái mà unit chứa từ này đang dạy — suy từ bản đồ, không gõ tay. */
function chuCuaTu(idTu) {
  const u = g1.find((n) => n.node_kind === 'unit' && (n.vocabulary || []).includes(idTu));
  return u?.pronunciation_focus?.phonics?.[0]?.toLowerCase() || null;
}

const lechAm = [], thieuAm = [];
for (const [id, x] of Object.entries(bu.tu)) {
  const chu = chuCuaTu(id);
  if (!chu) continue;
  const suyRa = x.word.toLowerCase().startsWith(chu) ? 'dau' : 'giua';
  if (suyRa === 'giua' && !x.am_o) {
    thieuAm.push(`${id} "${x.word}": âm /${chu}/ KHÔNG ở đầu mà chưa khai am_o`);
  } else if (x.am_o && x.am_o !== suyRa) {
    lechAm.push(`${id} "${x.word}": khai "${x.am_o}" mà chữ nói là "${suyRa}"`);
  }
}
t(`mọi từ có âm KHÔNG ở đầu đều khai am_o (${thieuAm.length} thiếu)`, thieuAm.length === 0);
in5(thieuAm);
t(`am_o khai đúng với chữ của từ (${lechAm.length} lệch)`, lechAm.length === 0);
in5(lechAm);

/* Unit nào TRỘN hai vị trí thì `sua_phonics` phải ghi "mixed" — để người sau đọc
   khối ấy không tưởng cả unit cùng một vị trí rồi ra đề sai cả loạt. */
const saiTomTat = [];
for (const p of phBanDo) {
  const u = g1.find((n) => n.node_kind === 'unit' && (n.phonics || []).includes(p.id));
  const vt = new Set((u?.vocabulary || []).map((v) => bu.tu[v]?.am_o || 'dau'));
  const that = vt.size > 1 ? 'mixed' : (vt.has('giua') ? 'medial' : 'initial');
  const khai = bu.sua_phonics[p.id]?.position || 'initial';
  if (khai !== that) saiTomTat.push(`${p.id}: khai "${khai}" mà thật ra là "${that}"`);
}
t(`tóm tắt vị trí âm của 16 unit đúng (${saiTomTat.length} sai)`, saiTomTat.length === 0);
in5(saiTomTat);

const suaBay = Object.keys(bu.sua_phonics).filter((k) => !k.startsWith('_'))
  .filter((id) => !N[id]);
t(`sua_phonics không trỏ vào node không có (${suaBay.length})`, suaBay.length === 0);
in5(suaBay);

/* ══ 4 · MẪU CÂU NHIỀU Ô PHẢI KHAI VAI TỪNG Ô ══
   Đây là chỗ chặn "It's a pen bell." */
const loiSlot = [];
for (const [id, s] of Object.entries(bu.sua_slot)) {
  if (id.startsWith('_')) continue;
  if (!N[id]) { loiSlot.push(`${id}: không có mẫu câu này trong bản đồ`); continue; }
  const form = N[id].grammar_form || '';
  const oTrongForm = [...form.matchAll(/\[([^\]]+)\]/g)].map((m) => m[1]);
  for (const o of oTrongForm) {
    if (!s.o?.[o]) loiSlot.push(`${id}: công thức có ô [${o}] mà chưa khai vai`);
  }
  for (const o of Object.keys(s.o || {})) {
    if (!oTrongForm.includes(o)) loiSlot.push(`${id}: khai vai cho ô [${o}] mà công thức không có`);
  }
}
t(`mọi ô trong công thức đều được khai vai (${loiSlot.length} chỗ)`, loiSlot.length === 0);
in5(loiSlot);

/* Mẫu câu có TỪ 2 Ô TRỞ LÊN thì BẮT BUỘC phải nằm trong sua_slot — không khai là
   bộ sinh thay bừa. Đây là luật, không phải gợi ý. */
const nhieuOChuaKhai = spBanDo
  .filter((sp) => ([...(sp.grammar_form || '').matchAll(/\[[^\]]+\]/g)].length >= 2))
  .filter((sp) => !bu.sua_slot[sp.id])
  .map((sp) => `${sp.id}: "${sp.grammar_form}"`);
t(`mẫu câu nhiều ô đều đã khai vai (${nhieuOChuaKhai.length} chưa)`, nhieuOChuaKhai.length === 0);
in5(nhieuOChuaKhai);

/* ══ 5 · DẠNG BIẾN ĐỔI PHẢI CÓ THẬT ══
   "She's + [Verb-ing]" mà từ trong slot là "run" — không có dạng `ing` thì bộ sinh
   ghép thẳng ra "She's run." */
const thieuDang = [];
for (const [id, s] of Object.entries(bu.sua_slot)) {
  if (id.startsWith('_') || !s.dung_dang) continue;
  const co = Object.values(bu.tu).some((x) => x[s.dung_dang]);
  if (!co) thieuDang.push(`${id}: đòi dạng "${s.dung_dang}" mà không từ nào khai`);
}
t(`mọi dạng biến đổi được đòi đều có từ khai (${thieuDang.length})`, thieuDang.length === 0);
in5(thieuDang);

/* ══ 6 · GÕ ĐƯỢC BẰNG BÀN PHÍM THƯỜNG ══ */
const khongGoDuoc = Object.entries(bu.tu)
  .filter(([, x]) => !/^[a-z ]+$/.test(x.word))
  .map(([id, x]) => `${id}: "${x.word}"`);
t(`mọi từ chỉ gồm chữ thường và dấu cách (${khongGoDuoc.length})`, khongGoDuoc.length === 0);
in5(khongGoDuoc);

/* Từ dài phải nằm trong danh sách MIỄN GÕ — nếu không bé bậc 4 phải gõ 10 ký tự. */
const NGUONG = 7;
const daiMaBatGo = Object.values(bu.tu)
  .filter((x) => x.word.length > NGUONG && !bu.khong_bat_go.tu.includes(x.word))
  .map((x) => `${x.word} (${x.word.length} ký tự)`);
t(`từ trên ${NGUONG} ký tự đều được miễn gõ (${daiMaBatGo.length} chưa miễn)`, daiMaBatGo.length === 0);
in5(daiMaBatGo);

/* ══ 7 · PHẦN THÊM ══ */
t('có đủ 10 số đếm one…ten', bu.them.so_dem.muc.length === 10);
t('có ít nhất 4 màu cho ô [Colour]', bu.them.mau.muc.length >= 4);
t('có tên dự phòng cho ô [Name]', bu.them.ten.muc.length >= 2);
const themKhuyet = [...bu.them.so_dem.muc, ...bu.them.mau.muc]
  .filter((x) => !x.nghia || !/^\/.+\/$/.test(x.ipa || ''))
  .map((x) => x.word);
t(`số đếm và màu đều có nghĩa + IPA (${themKhuyet.length} khuyết)`, themKhuyet.length === 0);
in5(themKhuyet);

/* ══ 7B · MỌI TỪ PHẢI CÓ HÌNH, VÀ BẢY TỪ NỢ PHẢI CÓ HÌNH VẼ TAY ══
   Bậc 1 (nghe → bấm hình) và bài điền chỗ trống của bậc 3 đều dựa vào HÌNH. Từ nào
   thiếu hình thì hai chỗ ấy hiện dấu hỏi — bé không làm được, mà dữ liệu vẫn hợp lệ.

   Bảy từ dùng emoji GẦN ĐÚNG (gate 🚧 là biển công trường, top 🪀 là yo-yo…) đã được
   vẽ tay bằng SVG. Phép kiểm này canh hai chiều: mọi khoá `ve` phải có hình thật
   trong `HinhVe.jsx`, và mọi hình trong `HinhVe.jsx` phải có từ dùng tới — hình
   thừa nằm im là dấu hiệu ai đó đổi tên từ mà quên. */
const veTay = bu.hinh._ve_tay;
const nguonHinhVe = readFileSync(join(R, 'web/src/mon/tienganh/components/HinhVe.jsx'), 'utf8');
const coTrongBo = (k) => new RegExp(`\\b${k}:\\s*\\w+`).test(
  nguonHinhVe.slice(nguonHinhVe.indexOf('const BO = {')));

const thieuHinh = Object.values(bu.tu)
  .filter((x) => !bu.hinh[x.word] && !veTay[x.word])
  .map((x) => x.word);
t(`60 từ đều có hình (${thieuHinh.length} thiếu)`, thieuHinh.length === 0);
in5(thieuHinh);

const veHong = Object.entries(veTay).filter(([k]) => !k.startsWith('_'))
  .filter(([, v]) => !v.ve || !coTrongBo(v.ve))
  .map(([k, v]) => `${k}: khoá "${v.ve}" không có trong HinhVe.jsx`);
t(`bảy từ nợ đều đã có hình vẽ tay (${veHong.length} chưa)`, veHong.length === 0);
in5(veHong);

const dungVe = new Set(Object.values(veTay).map((v) => v.ve).filter(Boolean));
const boHinh = (nguonHinhVe.match(/const BO = \{([^}]*)\}/) || [, ''])[1]
  .split(',').map((x) => x.split(':')[0].trim()).filter(Boolean);
const veThua = boHinh.filter((k) => !dungVe.has(k));
t(`không hình vẽ nào nằm im không ai dùng (${veThua.length} thừa)`, veThua.length === 0);
in5(veThua);

/* ══ 8 · KHÔNG NHÂN VẬT CỦA SÁCH TOÁN ══
   Bác chốt 12-08-2026: quyển Tiếng Anh dựng cho MỌI học sinh, không đòi bé phải
   biết trước thế giới của bốn quyển Toán. Bé học Tiếng Anh lớp 1 chưa chắc đã học
   Toán lớp 2.

   Đây là loại quyết định rất dễ trôi: sáu tháng nữa ai đó viết lời giảng, thấy hai
   nhân vật có sẵn giọng văn hay, tiện tay mượn một câu — và không cổng nào biết.
   Nên biến nó thành hàng rào máy gác, quét CẢ THƯ MỤC chứ không gõ tay tên tệp. */
const NHAN_VAT = ['Trí Long', 'Tri Long', 'Su Kem', 'SuKem', 'Su Bống', 'Su Bong'];
const quetTep = (d) => (existsSync(d) ? readdirSync(d, { withFileTypes: true })
  .flatMap((x) => (x.isDirectory() ? quetTep(join(d, x.name))
    : /\.json$/.test(x.name) ? [join(d, x.name)] : [])) : []);

const dinhNhanVat = [];
for (const p of quetTep(join(R, 'data/tienganh'))) {
  const s = readFileSync(p, 'utf8');
  for (const nv of NHAN_VAT) {
    /* Bỏ qua chính dòng ghi chú đang DẶN đừng dùng — nếu không thì lời dặn tự làm
       cổng đỏ, và người sau sẽ xoá lời dặn thay vì xoá nhân vật. */
    const dong = s.split('\n').filter((l) => l.includes(nv) && !/KHÔNG dùng|đừng dùng|không dính/i.test(l));
    if (dong.length) dinhNhanVat.push(`${p.split('/data/')[1]}: "${nv}" ×${dong.length}`);
  }
}
t(`không tệp nào của Tiếng Anh nhắc nhân vật sách Toán (${dinhNhanVat.length})`,
  dinhNhanVat.length === 0);
in5(dinhNhanVat);

/* Danh sách tên dự phòng phải LẤY TỪ SÁCH, không bịa và không mượn của Toán.
   Mọi tên phải xuất hiện thật trong bản đồ, hoặc trong câu mẫu của chính lớp 1. */
const chuTrongBanDo = new Set(bando.graph.nodes.flatMap(
  (n) => [n.word, n.example].filter(Boolean).flatMap((s) => String(s).split(/[^A-Za-zÀ-ỹ]+/)),
));
const tenLa = bu.them.ten.muc.filter((x) => !x.split(' ').every((w) => chuTrongBanDo.has(w)));
t(`tên dự phòng đều có gốc trong bản đồ (${tenLa.length} tên lạ)`, tenLa.length === 0);
in5(tenLa);

/* ══ 9 · TỔNG KẾT ══ */
const soVai = {};
for (const x of Object.values(bu.tu)) for (const v of x.vai) soVai[v] = (soVai[v] || 0) + 1;
console.log(`\n   ${idBu.length} từ đã bù · vai: `
  + Object.entries(soVai).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(' · '));
const soAmGiua = Object.values(bu.tu).filter((x) => x.am_o === 'giua').length;
console.log(`   thêm: ${bu.them.so_dem.muc.length} số · ${bu.them.mau.muc.length} màu`
  + ` · ${bu.them.ten.muc.length} tên · ${soAmGiua} từ có âm ở GIỮA (bản đồ khai nhầm là đầu)`
  + ` · khai vai cho ${Object.keys(bu.sua_slot).filter((k) => !k.startsWith('_')).length} mẫu câu`);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
