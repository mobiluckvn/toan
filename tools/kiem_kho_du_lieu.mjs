/**
 * ĐỐI CHIẾU KHO DỮ LIỆU HỌC — bốn phép, chạy sau mỗi lần dọn hoặc mỗi khi nghi.
 *
 *     export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
 *     node tools/kiem_kho_du_lieu.mjs
 *
 * ⚠ CHỈ ĐỌC. Không ghi, không xoá.
 *
 * ── BỐN PHÉP, VÀ VÌ SAO ĐÚNG BỐN PHÉP NÀY ──
 * Mỗi phép bắt một họ lỗi ĐÃ XẢY RA THẬT ngày 23-08-2026, không phải một danh
 * sách nghĩ ra cho đẹp:
 *
 *   ① PHIÊN HAI CHỦ — một `sessionId` chỉ sinh ở MỘT lần mở bài của MỘT bé, nên
 *      hai bé cùng mang một mã phiên là chuyện không thể tự nhiên. Bắt được lỗi
 *      hàm nhận lại hàng đợi sang tên nhầm (130/398 bản ghi nằm sai học bạ).
 *
 *   ② LỖ TRONG DÃY SỐ THỨ TỰ — mã bản ghi nhúng số thứ tự của lượt trong phiên,
 *      nên dãy phải liền. Thủng là mất bản ghi giữa chừng.
 *      ⚠ PHẢI nhóm theo (bé · phiên · bài), không theo mình `sessionId`: một
 *      phiên đi qua hai micro thì số thứ tự lặp lại hợp lệ, gộp chung sẽ báo lỗ
 *      oan. Bản đầu của phép này đã báo oan đúng như thế.
 *
 *   ③ mastery KHỚP attempts — `mastery` suy hoàn toàn từ `attempts`, nên
 *      `nAttempts` của mỗi nút phải bằng đúng số lượt còn lại của nút ấy. Lệch
 *      nghĩa là hàm nền bỏ sót lượt, hoặc có ai ghi tay vào `mastery`.
 *
 *   ④ NÚT CÓ LƯỢT MÀ THIẾU mastery — chiều ngược của ③. Bắt được cảnh hàm nền
 *      không chạy cho một số bản ghi (đã xảy ra với pha `check`/`worked` trước
 *      khi nới danh sách trắng).
 *
 * ⚠ BỐN PHÉP NÀY KHÔNG BẮT ĐƯỢC MẤT PHẦN ĐUÔI. Nếu mấy lượt CUỐI của một phiên
 *    không bao giờ lên máy chủ thì dãy số thứ tự vẫn liền, chỉ ngắn hơn thực tế.
 *    Muốn biết thì phải so với một nguồn độc lập (sổ tiến độ), hoặc đi thử rồi
 *    đếm tay. Đừng đọc "0 lỗ" thành "không mất gì".
 */
import { createRequire } from 'node:module';
import { readFileSync, existsSync } from 'node:fs';

const doi = createRequire(new URL('../web/functions/package.json', import.meta.url));
const { initializeApp, cert } = doi('firebase-admin/app');
const { getFirestore } = doi('firebase-admin/firestore');

const KHOA = process.env.GOOGLE_APPLICATION_CREDENTIALS;
if (!KHOA || !existsSync(KHOA)) {
  console.error('✗ thiếu khoá quản trị.\n'
    + '  export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json\n'
    + '  ⚠ Khoá để NGOÀI thư mục kho — nó mở được toàn bộ dữ liệu dự án.');
  process.exit(1);
}
initializeApp({ credential: cert(JSON.parse(readFileSync(KHOA, 'utf8'))) });
const db = getFirestore();

/* Đúng bốn pha mà `onAttempt` tính vào BKT — đọc từ mã nền để không lệch. */
const nen = readFileSync(new URL('../web/functions/index.js', import.meta.url), 'utf8');
const PHA = (nen.match(/if \(!\[([^\]]+)\]\.includes\(a\.phase\)\) return;/)?.[1] || '')
  .match(/'([a-z]+)'/g)?.map((x) => x.slice(1, -1)) || [];

const q = await db.collection('attempts').get();
console.log(`\n  attempts: ${q.size} bản ghi · pha tính vào BKT: ${PHA.join(' · ')}\n`);
let hong = 0;

/* ── ① phiên hai chủ ─────────────────────────────────────────────────────── */
{
  const m = new Map();
  q.forEach((d) => {
    const s = d.get('sessionId');
    if (!m.has(s)) m.set(s, new Set());
    m.get(s).add(d.get('learnerId'));
  });
  const xau = [...m].filter(([, v]) => v.size > 1);
  console.log(`  ① phiên bị hai bé cùng mang: ${xau.length}`);
  xau.slice(0, 10).forEach(([s, v]) => console.log(`     ✗ ${s} → ${v.size} bé`));
  hong += xau.length;
}

/* ── ② lỗ trong dãy số thứ tự ────────────────────────────────────────────── */
{
  const m = new Map();
  q.forEach((d) => {
    const k = `${d.get('learnerId')}|${d.get('sessionId')}|${d.get('microId')}`;
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(Number(String(d.id).split('_').pop()));
  });
  const xau = [];
  for (const [k, seq] of m) {
    const s = [...new Set(seq)].sort((a, b) => a - b);
    if (s.length !== s[s.length - 1] - s[0] + 1) xau.push(`${k} → ${s.join(',')}`);
  }
  console.log(`  ② nhóm (bé·phiên·bài) có lỗ trong dãy số thứ tự: ${xau.length}/${m.size}`);
  xau.slice(0, 10).forEach((x) => console.log(`     ✗ ${x}`));
  hong += xau.length;
}

/* ── ③ + ④ mastery so với attempts ───────────────────────────────────────── */
{
  const dem = new Map();
  q.forEach((d) => {
    const a = d.data();
    if (!a.bktUnit || !PHA.includes(a.phase)) return;
    const k = `${a.learnerId}/${encodeURIComponent(a.bktUnit)}`;
    dem.set(k, (dem.get(k) || 0) + 1);
  });
  const co = new Set();
  let khop = 0; const lech = [];
  for (const cha of await db.collection('mastery').listDocuments()) {
    for (const u of (await cha.collection('units').get()).docs) {
      const k = `${cha.id}/${u.id}`;
      co.add(k);
      if (dem.get(k) === u.get('nAttempts')) khop += 1;
      else lech.push(`${k}: mastery=${u.get('nAttempts')} · attempts=${dem.get(k) ?? 0}`);
    }
  }
  console.log(`  ③ mục mastery khớp số lượt: ${khop}/${khop + lech.length}`);
  lech.slice(0, 10).forEach((x) => console.log(`     ✗ ${x}`));
  const thieu = [...dem.keys()].filter((k) => !co.has(k));
  console.log(`  ④ nút có lượt mà THIẾU mastery: ${thieu.length}`);
  thieu.slice(0, 10).forEach((x) => console.log(`     ✗ ${x}`));
  hong += lech.length + thieu.length;
}

console.log(hong
  ? `\n  ✗ ${hong} chỗ không khớp — xem từng dòng ở trên.\n`
  : '\n  ✓ Bốn phép đều sạch.'
    + '\n  ⚠ Nhắc lại: bốn phép này KHÔNG bắt được mất phần đuôi của một phiên.\n');
process.exit(hong ? 1 : 0);
