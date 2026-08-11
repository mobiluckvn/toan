/**
 * CỔNG HỌC BẠ — phép tính chung của bốn màn hình.
 * chạy: node test/hocba.test.mjs
 *
 * Trang chính của quyển, sổ bố mẹ và bảng cô giáo nay đếm bằng CÙNG một bộ hàm. Sai
 * ở đây là ba màn cùng nói dối một lượt, mà nói dối bằng con số trông rất thật.
 *
 * Chạy trên DỮ LIỆU THẬT của cả bốn quyển, không dựng chỉ mục giả: chỗ hay vỡ nhất
 * không phải công thức mà là hình dạng dữ liệu — lớp 4 có 11 chương, lớp 2·3 có 8 và
 * thêm ba cửa ải đánh số chương 9·10·11, lớp 5 thì ba micro mới thành một "bài".
 */
import { readFileSync } from 'node:fs';
import {
  emptyProgress, recordMicro, recordChapter, saveSpot, setMode, ghiLuyenChuDe,
  gopTienDo, ketQuaChuong,
} from '../src/mon/toan/lib/progress.js';
import {
  hocBaQuyen, baiDeXuatChuong, thongKeChuong, trangThaiBai, baiCanCoGang,
  hocBaChuDe, tinhTrangDang, trinhDo,
} from '../src/mon/toan/lib/hocba.js';
import { allMicroIds, ghiNhoChuong, datSoDangKy } from '../src/mon/toan/lib/noiDung.js';

const D = new URL('../public/content/', import.meta.url).pathname;
const doc = (p) => JSON.parse(readFileSync(D + p, 'utf8'));

/* Nạp sổ đăng ký THẬT. Bản mặc định trong content.js chỉ có lớp 2 và lớp 5, nên bài
   lớp 3·4 bị tính sang lớp 5 và mọi phép đếm theo quyển lệch trong im lặng. */
datSoDangKy(doc('chuong_trinh.json'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const PASS = { pass: true, mustOK: true, right: 3, total: 3 };
const TRUOT = { pass: false, mustOK: false, right: 1, total: 3 };

/* ── Dựng chỉ mục chuẩn hoá y như `napChiMuc`, nhưng đọc tệp thay vì fetch ── */
const dk = doc('chuong_trinh.json');

function chiMucCua(ma) {
  const ct = dk.chuongTrinh[ma];
  const onTapAll = (() => {
    try { return doc(ct.tepOnTap || `${ct.thuMuc}/ontap.json`); } catch { return []; }
  })();
  let bai;
  if (ma === 'lop5') {
    const idx = doc('index_micro.json');
    const tenCh = Object.fromEntries((ct.chuong || []).map((c) => [c.so, c.ten]));
    bai = allMicroIds('lop5').map((id) => {
      const m = idx[id.replace(/[:.]/g, '_')] || {};
      const b = Number(id.split('.B')[1].split('.M')[0]);
      const ch = Math.ceil(b / 4);
      return { id, so: b, micro: Number(id.split('.M')[1]), ten: m.title || id,
               chuong: ch, tenChuong: tenCh[ch], durationMinutes: m.durationMinutes };
    });
  } else {
    const ds = doc(`${ct.thuMuc}/index.json`);
    ghiNhoChuong(ds);
    bai = ds.map((b) => ({ id: b.id, so: b.so, micro: 1, ten: b.ten,
                           chuong: b.chuong, tenChuong: b.tenChuong, soCau: b.soCau }));
  }
  const m = new Map();
  for (const b of bai) {
    if (!m.has(b.chuong)) m.set(b.chuong, { so: b.chuong, ten: b.tenChuong, bai: [] });
    m.get(b.chuong).bai.push(b);
  }
  const chuong = [...m.values()].sort((x, y) => x.so - y.so);
  for (const c of chuong) c.onTap = onTapAll.filter((o) => o.loai !== 'ai' && o.chapter === c.so);
  return { ma, ten: ct.ten, bai, chuong,
           onTap: onTapAll.filter((o) => o.loai !== 'ai'),
           ai: onTapAll.filter((o) => o.loai === 'ai') };
}

const CM = Object.fromEntries(['lop2', 'lop3', 'lop4', 'lop5'].map((m) => [m, chiMucCua(m)]));

/* ══ 1 · CHỈ MỤC CHUẨN HOÁ — bốn quyển cùng một hình dạng ══ */
for (const [ma, cm] of Object.entries(CM)) {
  const khai = dk.chuongTrinh[ma];
  t(`${ma}: số bài khớp sổ đăng ký (${cm.bai.length})`, cm.bai.length === khai.soBai);
  t(`${ma}: số chương khớp sổ đăng ký (${cm.chuong.length})`,
    cm.chuong.length === khai.soChuong);
  t(`${ma}: chương nào cũng có tên`, cm.chuong.every((c) => c.ten && c.ten !== `Chương ${c.so}`));
  t(`${ma}: chương nào cũng có bài`, cm.chuong.every((c) => c.bai.length > 0));
  /* Ba cửa ải đánh số chương 9·10·11 — LỌT vào danh sách chương là màn hình vẽ ra ba
     chương rỗng, bấm vào không có gì mà cổng vẫn xanh. */
  t(`${ma}: cửa ải không lẫn vào danh sách chương`,
    cm.ai.every((o) => !cm.chuong.some((c) => c.so === o.chapter)));
  t(`${ma}: mọi chương đều có kỳ ôn tập`, cm.chuong.every((c) => c.onTap.length === 1));
}
t('lớp 2·3 có ba cửa ải', CM.lop2.ai.length === 3 && CM.lop3.ai.length === 3);
t('lớp 4·5 không có cửa ải', CM.lop4.ai.length === 0 && CM.lop5.ai.length === 0);

/* ══ 2 · CHƯA HỌC GÌ → MỖI CHƯƠNG ĐỀ XUẤT BÀI ĐẦU CỦA CHÍNH NÓ ══
   Đây là điều bác dặn: "mỗi bài đề xuất trong một chương là bài đầu tiên như lớp 5
   nếu chưa từng học". Trước đây lớp 2·3·4 chỉ có MỘT thẻ cho cả quyển. */
for (const ma of ['lop2', 'lop3', 'lop4']) {
  const hb = hocBaQuyen(CM[ma], emptyProgress(), { khoaBai: false });
  t(`${ma}: chưa học → mọi chương chỉ vào BÀI ĐẦU của chương ấy`,
    hb.chuong.every((c) => c.deXuat?.bai.id === c.bai[0].id && c.deXuat.viSao === 'moi'));
  t(`${ma}: việc tiếp theo của quyển = bài 1`, hb.deXuat?.bai.id === CM[ma].bai[0].id);
  t(`${ma}: chưa học thì chưa bắt đầu`, hb.daBatDau === false && hb.datBai === 0);
}

/* Lớp 5 KHOÁ BÀI: theo chương trình thì chỉ chương 1 mở; tự chọn thì bài đầu mọi
   chương đều mở. Hai chế độ ra hai kết quả khác nhau — đó là cả điểm của chúng. */
{
  const p0 = emptyProgress();
  const hbCT = hocBaQuyen(CM.lop5, p0, { khoaBai: true });
  t('lớp 5 · theo chương trình: chỉ chương 1 có đề xuất',
    hbCT.chuong.filter((c) => c.deXuat).length === 1 && hbCT.chuong[0].deXuat);
  const hbTC = hocBaQuyen(CM.lop5, setMode(p0, 'tuchon'), { khoaBai: true });
  t('lớp 5 · tự chọn: chương nào cũng chỉ vào bài đầu chương',
    hbTC.chuong.every((c) => c.deXuat?.bai.id === c.bai[0].id));
  t('lớp 5 · không khoá thì cũng vậy',
    hocBaQuyen(CM.lop5, p0, { khoaBai: false }).chuong.every((c) => c.deXuat?.bai.id === c.bai[0].id));
}

/* ══ 3 · ĐANG HỌC DỞ THÌ CHỈ VÀO ĐÚNG CHỖ DỞ ══ */
{
  const cm = CM.lop4;
  const c3 = cm.chuong[2];
  let P = emptyProgress();
  P = recordMicro(P, c3.bai[0].id, PASS);
  P = saveSpot(P, c3.bai[1].id, 4, 12);
  const hb = hocBaQuyen(cm, P, { khoaBai: false });
  const ch3 = hb.chuong.find((c) => c.so === c3.so);
  t('chương đang dở → chỉ vào bài dở, không phải bài kế',
    ch3.deXuat.bai.id === c3.bai[1].id && ch3.deXuat.viSao === 'dangDo');
  t('việc tiếp theo của quyển ưu tiên chỗ dở, không phải chương 1',
    hb.deXuat.bai.id === c3.bai[1].id);
  t('chương 1 chưa động vẫn chỉ vào bài đầu của nó',
    hb.chuong[0].deXuat.bai.id === cm.chuong[0].bai[0].id);
  t('trạng thái bài: dở · đạt · mở',
    trangThaiBai(P, c3.bai[1].id) === 'dangDo'
    && trangThaiBai(P, c3.bai[0].id) === 'dat'
    && trangThaiBai(P, c3.bai[2].id) === 'mo');
}

/* Học rồi mà TRƯỢT (chưa qua câu bẫy) thì chỉ lại chính bài ấy, không đi tiếp */
{
  const cm = CM.lop3;
  let P = recordMicro(emptyProgress(), cm.chuong[0].bai[0].id, TRUOT);
  const c1 = hocBaQuyen(cm, P, { khoaBai: false }).chuong[0];
  t('trượt câu bẫy → vẫn chỉ vào chính bài ấy',
    c1.deXuat.bai.id === cm.chuong[0].bai[0].id && c1.deXuat.viSao === 'chuaDat');
  t('bài trượt vào danh sách cần cố gắng',
    baiCanCoGang(cm, P)[0]?.id === cm.chuong[0].bai[0].id);
}

/* ══ 4 · XONG CHƯƠNG · MASTER CHƯƠNG · XONG QUYỂN ══ */
{
  const cm = CM.lop2;
  const c1 = cm.chuong[0];
  let P = emptyProgress();
  c1.bai.forEach((b) => { P = recordMicro(P, b.id, PASS); });
  let tk = thongKeChuong(P, c1, 'lop2');
  t('xong hết bài mà chưa thi → chưa master',
    tk.xongBai === true && tk.master === false && tk.coKy === true);
  t('kỳ sát hạch đang chờ được nêu đích danh',
    hocBaQuyen(cm, P, { khoaBai: false }).kyChoNo?.so === c1.so);
  t('chương xong hết bài thì hết đề xuất', baiDeXuatChuong(P, c1) === null);

  P = recordChapter(P, 'lop2', c1.so, { pass: true, right: 9, total: 10 });
  tk = thongKeChuong(P, c1, 'lop2');
  t('xong bài + qua kỳ → MASTER', tk.master === true && tk.kyDat === true);
  t('không còn kỳ nào chờ', hocBaQuyen(cm, P, { khoaBai: false }).kyChoNo === null);

  /* Khoá theo QUYỂN: huy hiệu chương 1 của lớp 2 không được lây sang lớp 3 */
  t('huy hiệu không lây sang quyển khác',
    ketQuaChuong(P, 'lop2', c1.so)?.pass === true
    && thongKeChuong(P, CM.lop3.chuong[0], 'lop3').kyDat === false);

  let Q = emptyProgress();
  cm.bai.forEach((b) => { Q = recordMicro(Q, b.id, PASS); });
  const hbQ = hocBaQuyen(cm, Q, { khoaBai: false });
  t('học hết quyển → xongQuyen, không còn đề xuất',
    hbQ.xongQuyen === true && hbQ.deXuat === null && hbQ.phanTram === 100);
}

/* Khoá cũ (chỉ số chương, không có mã quyển) — đọc được khi con mới học MỘT quyển,
   và bỏ qua khi con học nhiều quyển, thà thiếu còn hơn gắn nhầm huy hiệu. */
{
  let P = recordMicro(emptyProgress(), CM.lop3.bai[0].id, PASS);
  P = { ...P, chapters: { 1: { pass: true, best: 9, total: 10 } } };
  t('sổ cũ · học một quyển → nhận về đúng quyển ấy',
    ketQuaChuong(P, 'lop3', 1)?.pass === true && ketQuaChuong(P, 'lop5', 1) === null);
  const R = recordMicro(P, CM.lop5.bai[0].id, PASS);
  t('sổ cũ · học hai quyển → không đoán bừa',
    ketQuaChuong(R, 'lop3', 1) === null && ketQuaChuong(R, 'lop5', 1) === null);
}

/* ══ 5 · HỌC BẠ THEO CHỦ ĐỀ ══ */
{
  const bd = doc('chu_de.json');
  const rong = hocBaChuDe(bd, emptyProgress());
  t(`bản đồ chủ đề: ${rong.tong} dạng bài`, rong.tong === Object.keys(bd.dang).length);
  t('chưa học gì → mọi dạng đều "chưa học"',
    rong.dem.chuaHoc === rong.tong && rong.dem.vung === 0);
  t('năm mảng kiến thức', rong.mang.length === 5);
  t('đếm của mảng cộng lại bằng đếm tổng',
    rong.mang.reduce((s, m) => s + m.dem.chuaHoc, 0) === rong.dem.chuaHoc);

  /* Một dạng có thang: học hết bài của mọi bậc thì VỮNG. */
  const maCoThang = Object.keys(bd.dang).find((k) => (bd.dang[k].thang || []).length >= 2);
  const d = { ...bd.dang[maCoThang], __ma: maCoThang };
  const moiBai = d.thang.flatMap((b) => b.bai);
  let P = emptyProgress();
  t('chưa động → chuaHoc', tinhTrangDang(P, d).tinhTrang === 'chuaHoc');
  P = recordMicro(P, moiBai[0], TRUOT);
  t('đã thử mà trượt → cần cố gắng', tinhTrangDang(P, d).tinhTrang === 'canCoGang');
  P = recordMicro(P, moiBai[0], PASS);
  t('đạt vài bài, chưa hết → đang học', tinhTrangDang(P, d).tinhTrang === 'dangHoc');
  moiBai.forEach((id) => { P = recordMicro(P, id, PASS); });
  const tt = tinhTrangDang(P, d);
  t('đạt hết bài mọi bậc → vững',
    tt.tinhTrang === 'vung' && tt.baiDat === tt.soBai && tt.bacXong.length === d.thang.length);

  /* Luyện trượt một bậc thì phải hiện ra là chỗ cần cố gắng, kể cả khi đã vững bậc dưới */
  const bacThap = d.thang[0].lop, bacCao = d.thang[d.thang.length - 1].lop;
  let Q = ghiLuyenChuDe(emptyProgress(), maCoThang, bacThap, { dat: 6, tong: 6 });
  Q = ghiLuyenChuDe(Q, maCoThang, bacCao, { dat: 1, tong: 6 });
  const tq = tinhTrangDang(Q, { ...d, __ma: maCoThang });
  t('vững bậc dưới nhưng trượt bậc trên → cần cố gắng',
    tq.tinhTrang === 'canCoGang' && tq.vungToi === bacThap && tq.bacTruot.includes(bacCao));
}

/* ══ 6 · TRÌNH ĐỘ HIỆN TẠI ══ */
{
  let P = emptyProgress();
  CM.lop4.chuong[0].bai.forEach((b) => { P = recordMicro(P, b.id, PASS); });
  P = recordMicro(P, CM.lop2.bai[0].id, PASS);
  const ds = ['lop2', 'lop3', 'lop4', 'lop5'].map((m) => hocBaQuyen(CM[m], P, { khoaBai: m === 'lop5' }));
  const td = trinhDo(ds, P, { gioCua: (ma) => (ma === 'lop4' ? 2 : 1) });
  t('trình độ: quyển động vào gần nhất', td.quyen?.ma === 'lop4');
  t('trình độ: đếm đủ hai quyển đang học', td.soQuyenDangHoc === 2);
  t('trình độ: tổng bài đạt cộng cả hai quyển',
    td.tongBaiDat === CM.lop4.chuong[0].bai.length + 1);
  t('chưa học gì thì không bịa ra trình độ',
    trinhDo(['lop2'].map((m) => hocBaQuyen(CM[m], emptyProgress())), emptyProgress()).quyen === null);
}

/* ══ 7 · GỘP SỔ MÁY NÀY VỚI SỔ TRÊN MẠNG ══ */
{
  const A = CM.lop2.bai[0].id, B = CM.lop2.bai[1].id;
  const may1 = { micros: { [A]: { pass: true, at: '2026-08-01T00:00:00.000Z' } } };
  const may2 = { micros: { [B]: { pass: true, at: '2026-08-02T00:00:00.000Z' } } };
  const g = gopTienDo(may1, may2);
  t('gộp: giữ cả bài của hai máy', !!g.micros[A]?.pass && !!g.micros[B]?.pass);

  const cu = { micros: { [A]: { pass: false, best: 1, at: '2026-08-01T00:00:00.000Z' } } };
  const moi = { micros: { [A]: { pass: true, best: 3, at: '2026-08-05T00:00:00.000Z' } } };
  t('gộp: mốc mới đè mốc cũ', gopTienDo(cu, moi).micros[A].pass === true);
  t('gộp: mốc cũ KHÔNG đè mốc mới', gopTienDo(moi, cu).micros[A].pass === true);

  const c1 = ghiLuyenChuDe(emptyProgress(), 'CASE:I.1.1', 3, { dat: 6, tong: 6 });
  const c2 = ghiLuyenChuDe(emptyProgress(), 'CASE:I.1.1', 4, { dat: 2, tong: 6 });
  const gc = gopTienDo(c1, c2);
  t('gộp chủ đề: giữ cả hai bậc đã luyện',
    !!gc.chuDe['CASE:I.1.1'].bac['3'] && !!gc.chuDe['CASE:I.1.1'].bac['4']);
  t('gộp: sổ rỗng thì trả nguyên bên kia', gopTienDo(c1, {}).chuDe['CASE:I.1.1'] !== undefined);
}

console.log(`\n   ${Object.keys(CM).length} quyển · `
  + Object.entries(CM).map(([m, c]) => `${m} ${c.bai.length}b/${c.chuong.length}ch`).join(' · '));
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
