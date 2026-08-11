/**
 * CỔNG MÀN CÔ GIÁO — bốn tab của một em có dựng nổi không.
 * chạy: node test/man_co_giao.test.mjs
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Soát end-to-end 11-08-2026: đăng nhập bằng tài khoản giáo viên rồi bấm vào một em,
 * **ba trên bốn tab vỡ trắng ngay lập tức**. Không phải sai số liệu — màn hình trắng
 * bong, React tháo cả cây.
 *
 *   · tab "Theo lớp"      → `h.chiMuc.bai` — học bạ CHƯA BAO GIỜ nộp `chiMuc`;
 *   · tab "Theo lớp"      → `trangThaiBai(...)` — hàm của Toán, tầng chung không
 *                            import được (luật ranh giới) nên chưa hề import;
 *   · tab "Theo chủ đề"   → `banDo` — một cái tên không khai ở đâu cả.
 *
 * Cả ba là mã CHẾT CHƯA TỪNG CHẠY. 1 096 phép kiểm cũ đi qua sạch, vì không phép nào
 * dựng thử màn này; mà ở `npm run dev` thì màn đăng nhập bị tắt hẳn, nên cửa vào màn
 * cô giáo cũng không mở ra bao giờ.
 *
 * ── PHÉP KIỂM NÀY GÁC GÌ ──
 * Học bạ phải nộp ĐỦ mọi thứ bảng cô giáo đọc, và nộp bằng chính hình dạng ấy. Tầng
 * chung không được với sang ruột môn để tự tính bù.
 *
 * ⚠ Còn một lớp lỗi tệp này KHÔNG bắt được: tên chưa khai (`banDo`, `trangThaiBai`).
 * Đó là việc của ESLint `no-undef` — kho chưa cài. Xem `docs/soat_toan_end_to_end.md`.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { emptyProgress, recordMicro, saveSpot } from '../src/mon/toan/lib/progress.js';
import { hocBaQuyen, hocBaChuDe } from '../src/mon/toan/lib/hocba.js';
import { ghiNhoChuong, datSoDangKy } from '../src/mon/toan/lib/noiDung.js';
import { NHAN_TRANG_THAI_BAI, NHAN_MUC_CHUONG, NHAN_TINH_TRANG }
  from '../src/chung/lib/nhanHocBa.js';

const D = new URL('../public/content/', import.meta.url).pathname;
const SRC = new URL('../src/', import.meta.url).pathname;
const doc = (p) => JSON.parse(readFileSync(D + p, 'utf8'));
datSoDangKy(doc('chuong_trinh.json'));

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* Dựng chỉ mục THẬT của một quyển, đúng cách `napChiMuc` gom chương từ bài thật. */
function chiMucCua(thuMuc, ma) {
  const ds = doc(`${thuMuc}/index.json`);
  ghiNhoChuong(ds);
  const bai = ds.map((b) => ({
    id: b.id, so: b.so, micro: 1, ten: b.ten || b.title || b.id, chuong: b.chuong,
  }));
  const theo = new Map();
  for (const b of bai) {
    if (!theo.has(b.chuong)) theo.set(b.chuong, { so: b.chuong, ten: `Chương ${b.chuong}`, bai: [] });
    theo.get(b.chuong).bai.push(b);
  }
  return { ma, ten: ma, bai, chuong: [...theo.values()].sort((x, y) => x.so - y.so) };
}

const cm = chiMucCua('lop2', 'lop2');
let P = emptyProgress();
P = recordMicro(P, cm.bai[0].id, { pass: true, mustOK: true, right: 9, total: 9 });
P = recordMicro(P, cm.bai[1].id, { pass: false, mustOK: false, right: 4, total: 9 });
P = saveSpot(P, cm.bai[2].id, 7, 24);
const hb = hocBaQuyen(cm, P, { khoaBai: cm.khoaBai });

/* ── 1 · Từng ô bài mà cô nhìn vào ── */
t('học bạ nộp danh sách chương', Array.isArray(hb.chuong) && hb.chuong.length > 0);
t('chương nào cũng nộp danh sách bài', hb.chuong.every((c) => Array.isArray(c.bai)));

const moiBai = hb.chuong.flatMap((c) => c.bai);
t('bài nào cũng được MÔN chấm sẵn trạng thái — tầng chung không tự tính',
  moiBai.every((b) => typeof b.trangThai === 'string'));
t('trạng thái nào cũng có chữ để in ra',
  moiBai.every((b) => NHAN_TRANG_THAI_BAI[b.trangThai]));

const tt = (id) => moiBai.find((b) => b.id === id)?.trangThai;
t('bài đã đạt chấm là "dat"', tt(cm.bai[0].id) === 'dat');
t('bài học hết mà chưa qua bẫy chấm là "chuaDat"', tt(cm.bai[1].id) === 'chuaDat');
t('bài đang dở chấm là "dangDo"', tt(cm.bai[2].id) === 'dangDo');
t('bài chưa đụng tới chấm là "mo"', tt(cm.bai[3].id) === 'mo');

/* ── 2 · Mức của chương cũng phải có chữ ── */
t('mức chương nào cũng có chữ để in ra',
  hb.chuong.every((c) => NHAN_MUC_CHUONG[c.muc]));

/* ── 3 · Tab "Theo chủ đề" ── */
const banDo = doc('chu_de.json');
const cd = hocBaChuDe(banDo, P);
t('học bạ chủ đề có đủ bốn ô đếm',
  ['vung', 'dangHoc', 'canCoGang', 'chuaHoc'].every((k) => typeof cd.dem[k] === 'number'));
t('mảng nào cũng có chủ đề và dạng bài',
  cd.mang.every((m) => Array.isArray(m.chuDe)));
const moiDang = cd.mang.flatMap((m) => m.chuDe.flatMap((c) => c.dang));
t('dạng bài nào cũng có tình trạng in được',
  moiDang.every((d) => NHAN_TINH_TRANG[d.tinhTrang]));

/* ── 4 · Tầng chung KHÔNG được tự tính lấy phần của môn ──
   Ba lỗi hôm nay đều bắt đầu từ một chỗ: màn chung với tay sang ruột Toán. Luật này
   đã có `ranh_gioi.test.mjs` gác đường `import`, nhưng gọi một cái tên KHÔNG import
   thì cổng ấy không thấy — nên chốt thêm ở đây bằng tên hàm cụ thể. */
const CAM = ['trangThaiBai', 'baiDeXuatChuong', 'thongKeChuong', 'hocBaQuyen', 'hocBaChuDe'];
const tepChung = readdirSync(`${SRC}chung/components`).filter((f) => /\.jsx?$/.test(f));
for (const f of tepChung) {
  const s = readFileSync(`${SRC}chung/components/${f}`, 'utf8');
  const dung = CAM.filter((h) => new RegExp(`\\b${h}\\s*\\(`).test(s));
  t(`chung/components/${f} không tự gọi hàm của môn (${dung.join() || 'sạch'})`,
    dung.length === 0);
}

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
