#!/usr/bin/env node
/**
 * KB1 — HIỆU CHỈNH NGƯỠNG TRÊN NGƯỜI HỌC MÔ PHỎNG (Bảng 3.24).
 *
 *     node tools/kb1_quet_luoi.mjs            1.000 bé, bộ ngưỡng mặc định
 *     node tools/kb1_quet_luoi.mjs --be 200   ít bé hơn cho nhanh
 *     node tools/kb1_quet_luoi.mjs --ghi      ghi đề xuất ra tệp JSON
 *
 * ── ⚠ KHÔNG GHI FIRESTORE, VÀ ĐÓ LÀ CHỦ Ý ──
 * Lượt mô phỏng mà trôi vào `attempts` thì mọi chỉ số của Bảng 3.22 nói về một đám
 * trẻ không tồn tại, hàm học ngưỡng đề xuất theo chúng, và không có đường lùi vì
 * nhật ký là BẤT BIẾN. Công cụ này chỉ in ra màn hình và (với `--ghi`) ra một tệp
 * JSON trong `docs/`.
 *
 * ── ⚠ KB1 TRẢ LỜI ĐƯỢC CÂU GÌ, VÀ KHÔNG TRẢ LỜI ĐƯỢC CÂU GÌ ──
 * Trẻ mô phỏng học đúng theo BKT vì ta bảo nó thế. Nên kết quả ở đây KHÔNG nói
 * «ngưỡng nào dạy trẻ tốt hơn» — nói thế là lấy giả thiết làm kết luận.
 *
 * Nó nói được: «nếu thế giới đúng như bộ tham số ta tin, thì mỗi θ dẫn tới NHỊP DẠY
 * nào» — mấy câu tới khi công nhận, bao nhiêu phần trăm công nhận sớm, bao nhiêu
 * nút được công nhận. Ba con số ấy chuyên gia đọc được và BÁC được, còn bản thân θ
 * thì không.
 */
import { argv } from 'node:process';
import { writeFileSync } from 'node:fs';

const G = new URL('../web/functions/src/', import.meta.url);
const { sinhNhatKy, nhipDay, MAC_DINH } = await import(new URL('moPhongHoc.js', G));
const { BO_MAC_DINH, KHOANG, layNguong } = await import(new URL('nguong.js', G));
const { hocMoiPhamVi } = await import(new URL('hocNguong.js', G));

const co = (ten, mac) => {
  const i = argv.indexOf(ten);
  return i > 0 && argv[i + 1] ? Number(argv[i + 1]) : mac;
};
const soBe = co('--be', MAC_DINH.soBe);
const ghi = argv.includes('--ghi');

console.log(`KB1 · ${soBe} người học mô phỏng · bộ ngưỡng v${BO_MAC_DINH.phienBan}\n`);
const t0 = Date.now();
const luots = sinhNhatKy(BO_MAC_DINH, { soBe });
console.log(`sinh ${luots.length.toLocaleString('vi-VN')} lượt trong ${((Date.now() - t0) / 1000).toFixed(1)} giây`);

/* ── 1 · NHỊP DẠY THEO θ — bảng chuyên gia đọc được ───────────────────────── */
const [lo, hi] = KHOANG.NG07;
const theta = [];
for (let x = lo; x <= hi + 1e-9; x += 0.05) theta.push(+x.toFixed(2));

console.log('\n══ NHỊP DẠY THEO θ ══');
console.log('  θ      số câu tới khi    nút được      công nhận');
console.log('         được công nhận    công nhận     sớm');
const bang = [];
for (const th of theta) {
  const r = nhipDay(luots, BO_MAC_DINH, th);
  bang.push(r);
  const pt = (x) => (x == null ? '    —' : `${(x * 100).toFixed(1).padStart(5)}%`);
  console.log(`  ${String(th).padEnd(6)} ${String(r.soCauToiThao ?? '—').padStart(10)}      `
    + `${pt(r.tiLeDuocCongNhan)}       ${pt(r.tiLeCongNhanSom)}   (mẫu ${r.coMauSom})`);
}

/* ⚠ ĐỌC BẢNG NÀY THEO SỐ CÂU, KHÔNG THEO XÁC SUẤT — đúng lời Bảng 3.21: đổi θ từ
   0,85 lên 0,90 có thể chẳng đổi gì trong cách hệ thống đối xử với trẻ. */
const nhom = new Map();
for (const r of bang) {
  if (r.soCauToiThao == null) continue;
  const k = Math.round(r.soCauToiThao);
  if (!nhom.has(k)) nhom.set(k, []);
  nhom.get(k).push(r.theta);
}
console.log('\n  Gom theo SỐ CÂU (đây mới là thứ bé cảm thấy):');
for (const [k, ds] of [...nhom].sort((a, b) => a[0] - b[0])) {
  console.log(`    ~${k} câu: θ = ${ds.join(' · ')}`);
}

/* ── 2 · ĐỀ XUẤT từ chính hàm học ngưỡng ──────────────────────────────────── */
console.log('\n══ ĐỀ XUẤT (chạy hàm học ngưỡng thật trên nhật ký mô phỏng) ══');
const ra = hocMoiPhamVi(luots, BO_MAC_DINH, { bayGio: Date.UTC(2026, 2, 1) });
const ds = ra.flatMap((x) => x.deXuat);
for (const d of ds) {
  const moi = d.giaTriDeXuat === null
    ? (d.thieuMau ? `— thiếu mẫu ${d.thieuMau.coMau}/${d.thieuMau.can}`
      : (d.ngoaiKhoang ? `— ngoài khoảng (${d.ngoaiKhoang.giaTriTho})` : '— không đề xuất'))
    : JSON.stringify(d.giaTriDeXuat);
  console.log(`  ${d.ma} ${(d.phamVi + (d.khoa ? `=${d.khoa}` : '')).padEnd(20)} `
    + `${JSON.stringify(d.giaTriHienTai)} → ${moi}`);
}

console.log('\n⚠ Đây là nhịp dạy TRONG MỘT THẾ GIỚI MÔ PHỎNG đúng theo BKT. Nó cho biết');
console.log('  một bộ ngưỡng dẫn tới nhịp nào, KHÔNG cho biết ngưỡng nào dạy trẻ tốt hơn.');
console.log('  Câu sau chỉ KB6 (học sinh thật, 4 tuần) mới trả lời được.');

if (ghi) {
  const tep = new URL('../docs/kb1_ket_qua.json', import.meta.url);
  writeFileSync(tep, `${JSON.stringify({
    chay: new Date().toISOString(),
    soBe,
    soLuot: luots.length,
    nguongVer: BO_MAC_DINH.phienBan,
    thetaDangHanh: layNguong(BO_MAC_DINH, 'NG07'),
    nhipDay: bang,
    deXuat: ds,
    luuY: 'Nhật ký MÔ PHỎNG, không phải dữ liệu học thật. Xem đầu tools/kb1_quet_luoi.mjs.',
  }, null, 2)}\n`, 'utf8');
  console.log(`\nđã ghi ${tep.pathname.split('/').slice(-2).join('/')}`);
}
