/**
 * SOI bản ghi `attempts` bị GÁN NHẦM CHỦ.
 *
 *     export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
 *     node tools/soi_ban_ghi_sai_chu.mjs
 *
 * ── DẤU HIỆU ──
 * Một mã phiên (`sessionId`) chỉ sinh ra ở MỘT lần mở bài của MỘT bé. Nên hai bé
 * khác nhau cùng mang một mã phiên là chuyện không thể xảy ra tự nhiên — trừ khi
 * bản ghi bị sang tên nhầm.
 *
 * Cảnh thật, đo được 23-08-2026: bé A học trên một chỗ, đúng 1 lượt lên được (lỗi
 * hàng đợi nghẽn), phần còn lại kẹt; ít ngày sau bé B đăng nhập vào chính chỗ ấy,
 * `reassignQueue`/`sangTenHangDoi` viết lại cả xấp của A thành của B. Kết quả:
 * 7 phiên, 130/398 bản ghi mang tên sai chủ.
 *
 * Cả hai lỗi đã vá cùng ngày. Tệp này để KIỂM LẠI, và để soi định kỳ.
 *
 * ⚠ CHỈ ĐỌC. Không sửa, không xoá — dữ liệu cũ đã sai thì sửa hay bỏ là quyết
 *    định của người chủ, không phải của một script.
 */
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const doi = createRequire('/Users/v/Documents/Code/web5/repo/web/functions/package.json');
const { initializeApp, cert } = doi('firebase-admin/app');
const { getFirestore } = doi('firebase-admin/firestore');
initializeApp({ credential: cert(JSON.parse(readFileSync(process.env.GOOGLE_APPLICATION_CREDENTIALS,'utf8'))) });
const db = getFirestore();
const q = await db.collection('attempts').get();
const m = new Map();
q.forEach(d => {
  const s = d.get('sessionId');
  if (!m.has(s)) m.set(s, new Map());
  const be = d.get('learnerId');
  if (!m.get(s).has(be)) m.get(s).set(be, []);
  m.get(s).get(be).push(d);
});
let songi = 0;
console.log('  Phiên bị HAI bé cùng mang mã — dấu hiệu bản ghi bị sang tên nhầm:\n');
for (const [s, beMap] of m) {
  if (beMap.size < 2) continue;
  const hang = [...beMap].map(([be, ds]) => ({
    be: be.slice(0,10),
    so: ds.length,
    seq: [...ds.map(d => Number(String(d.id).split('_').pop()))].sort((a,b)=>a-b).join(','),
    luc: ds[0].get('serverTs')?.toDate?.().toISOString().slice(0,10),
  })).sort((a,b) => a.luc.localeCompare(b.luc));
  const sau = hang[hang.length-1];
  songi += sau.so;
  console.log(`  ${s} · ${beMap.size} bé`);
  hang.forEach(h => console.log(`     bé ${h.be}… · ${String(h.so).padStart(2)} lượt · seq ${h.seq} · ${h.luc}`));
}
console.log(`\n  ⇒ tổng bản ghi ĐÁNG NGỜ bị gán nhầm chủ: ${songi} / ${q.size}`);
