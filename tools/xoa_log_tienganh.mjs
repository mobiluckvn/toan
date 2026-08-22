/**
 * ĐẾM · XOÁ dữ liệu học môn TIẾNG ANH trên máy chủ.
 *
 *     export GOOGLE_APPLICATION_CREDENTIALS=/đường/dẫn/khoa-quan-tri.json
 *     node tools/xoa_log_tienganh.mjs            # CHỈ ĐẾM, không đụng gì
 *     node tools/xoa_log_tienganh.mjs --xoa      # xoá thật, KHÔNG LÙI ĐƯỢC
 *
 * ── VÌ SAO KHÔNG DÙNG `firebase firestore:delete` ──
 *
 * Hai lý do, lý do thứ hai mới là lý do thật:
 *
 * 1. Ba kho DÙNG CHUNG với môn Toán — `attempts`, `mastery/…/units`,
 *    `reviewQueue/…/cards`. CLI xoá được cả kho hoặc cả cây, không lọc được
 *    theo trường. Xoá cả kho là xoá luôn tiến độ Toán của bé.
 *
 * 2. ⚠ CLI KHÔNG NÓI GÌ CẢ. Chạy `firestore:delete progressTA -r --force` xong
 *    thì không in một dòng nào và trả mã thoát 0. Tôi đã thử ĐỐI CHỨNG bằng một
 *    kho chắc chắn không tồn tại (`zzz_khong_he_ton_tai`) — kết quả y hệt: im
 *    lặng, mã thoát 0. Nghĩa là mã thoát 0 KHÔNG chứng minh có gì bị xoá, cũng
 *    không chứng minh kho ấy từng có dữ liệu. Báo "đã xoá xong" dựa trên nó là
 *    nói quá, cùng họ [[nguong-phan-tram-che-lo-thung]].
 *
 * Nên tệp này ĐẾM TRƯỚC, in ra từng kho bao nhiêu bản ghi, rồi mới xoá, rồi đếm
 * LẠI. Ba con số ấy mới là bằng chứng.
 *
 * ── RANH GIỚI: cái gì là "của Tiếng Anh" ──
 *
 *   attempts            trường `mon == 'tienganh'` — do `suKien.js` ghi kèm mỗi
 *                       lượt. Trước Đợt 1 môn Tiếng Anh KHÔNG ghi vào `attempts`
 *                       lần nào, nên không có bản ghi cũ nào thiếu nhãn.
 *   mastery/…/units     trường `mon` — `onAttempt` ghi `a.mon || 'toan'`, tức
 *                       bản ghi Toán mặc định 'toan'. Đếm THÊM một lần theo hình
 *                       dạng mã nút (`v_*` · `sp_*`) và ĐỐI CHIẾU hai con số:
 *                       lệch nhau là có bản ghi khai sai môn, phải xem bằng mắt
 *                       trước khi xoá.
 *   reviewQueue/…/cards `microId` bắt đầu bằng `DL:TA` (mã bài Tiếng Anh).
 *   progressTA · hocBaTA · phongNoiTA    thuần Tiếng Anh, xoá cả cây.
 *
 * ── BA THỨ KHÔNG XOÁ, NHƯNG SẼ CŨ ĐI ──
 * `report/{uid}` · `teacherBoard/global` · `bangXepHang/global` là bản TỔNG HỢP
 * dựng từ dữ liệu trên. Xoá nguồn thì chúng còn giữ số cũ cho tới lần dựng lại
 * kế tiếp. Tệp này chỉ ĐẾM và báo, không tự sửa — sửa chúng là việc khác.
 */
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';

/* `firebase-admin` chỉ nằm trong `web/functions/node_modules`. Mượn từ đó thay vì
   cài thêm một bản thứ hai ở gốc kho — hai bản thì sớm muộn lệch phiên bản, mà
   lệch phiên bản của thư viện quản trị là thứ chỉ lộ ra lúc đang xoá dữ liệu. */
const doi = createRequire(new URL('../web/functions/package.json', import.meta.url));
const { initializeApp, cert, applicationDefault } = doi('firebase-admin/app');
const { getFirestore } = doi('firebase-admin/firestore');

const XOA = process.argv.includes('--xoa');
const KHOA = process.env.GOOGLE_APPLICATION_CREDENTIALS;

if (!KHOA) {
  console.error(
    '✗ chưa có khoá quản trị.\n'
    + '  Firebase Console → Project settings → Service accounts → Generate new\n'
    + '  private key, rồi:\n'
    + '      export GOOGLE_APPLICATION_CREDENTIALS=/đường/dẫn/khoa.json',
  );
  process.exit(1);
}

initializeApp({
  credential: (() => {
    try { return cert(JSON.parse(readFileSync(KHOA, 'utf8'))); }
    catch { return applicationDefault(); }
  })(),
});
const db = getFirestore();

/** Xoá theo lô — Firestore chặn ở 500 thao tác một lô. */
async function xoaLo(refs) {
  for (let i = 0; i < refs.length; i += 400) {
    const lo = db.batch();
    refs.slice(i, i + 400).forEach((r) => lo.delete(r));
    await lo.commit();
  }
}

/** Cả một cây con: `progressTA/{uid}/micros/*` và cả tài liệu cha. */
async function quetCay(ten) {
  const cha = await db.collection(ten).listDocuments();
  const refs = [];
  for (const d of cha) {
    for (const con of await d.listCollections()) {
      (await con.listDocuments()).forEach((x) => refs.push(x));
    }
    refs.push(d);
  }
  return refs;
}

const bang = [];
const ghi = (kho, refs, chu = '') => { bang.push({ kho, refs, chu }); };

/* ── ĐẾM ─────────────────────────────────────────────────────────────────── */

const att = await db.collection('attempts').where('mon', '==', 'tienganh').get();
ghi('attempts (mon=tienganh)', att.docs.map((d) => d.ref));

const units = await db.collectionGroup('units').get();
const theoMon = units.docs.filter((d) => d.get('mon') === 'tienganh');
const theoMa = units.docs.filter((d) => /^(v|sp)_/.test(d.id));
ghi('mastery/*/units (mon=tienganh)', theoMon.map((d) => d.ref),
  theoMon.length === theoMa.length ? 'khớp với phép đếm theo mã nút'
    : `⚠ LỆCH: đếm theo mã nút ra ${theoMa.length} — xem bằng mắt TRƯỚC khi xoá`);

const cards = await db.collectionGroup('cards').get();
const theTA = cards.docs.filter((d) => String(d.get('microId') || '').startsWith('DL:TA'));
ghi('reviewQueue/*/cards (bài DL:TA*)', theTA.map((d) => d.ref));

for (const k of ['progressTA', 'hocBaTA', 'phongNoiTA']) ghi(k, await quetCay(k));

const tong = bang.reduce((s, x) => s + x.refs.length, 0);
console.log(XOA ? '── ĐẾM TRƯỚC KHI XOÁ' : '── CHỈ ĐẾM (chưa đụng gì)');
for (const x of bang) {
  console.log(`   ${String(x.refs.length).padStart(6)}  ${x.kho}${x.chu ? `   ${x.chu}` : ''}`);
}
console.log(`   ${String(tong).padStart(6)}  TỔNG`);

/* ── KHÔNG XOÁ, CHỈ BÁO LÀ SẼ CŨ ĐI ──────────────────────────────────────── */
const bt = await db.collection('report').listDocuments();
console.log(`\n── bản tổng hợp sẽ CŨ ĐI (không xoá): report/* (${bt.length} bé) `
  + '· teacherBoard/global · bangXepHang/global');

if (!XOA) {
  console.log('\nChạy lại với  --xoa  để xoá thật. Không lùi lại được.');
  process.exit(0);
}

/* ── XOÁ, RỒI ĐẾM LẠI ────────────────────────────────────────────────────── */
const lech = bang.find((x) => x.chu.startsWith('⚠'));
if (lech) {
  console.error(`\n✗ DỪNG: ${lech.chu}\n  Hai phép đếm không khớp thì chưa biết đang xoá cái gì.`);
  process.exit(1);
}

console.log('\n── XOÁ');
for (const x of bang) {
  await xoaLo(x.refs);
  console.log(`   ✓ ${x.kho}`);
}

console.log('\n── ĐẾM LẠI (phải về 0 hết)');
const con = {
  'attempts (mon=tienganh)': (await db.collection('attempts').where('mon', '==', 'tienganh').get()).size,
  'mastery/*/units (mon=tienganh)': (await db.collectionGroup('units').get())
    .docs.filter((d) => d.get('mon') === 'tienganh').length,
  'reviewQueue/*/cards (bài DL:TA*)': (await db.collectionGroup('cards').get())
    .docs.filter((d) => String(d.get('microId') || '').startsWith('DL:TA')).length,
};
for (const k of ['progressTA', 'hocBaTA', 'phongNoiTA']) con[k] = (await quetCay(k)).length;

let sot = 0;
for (const [k, v] of Object.entries(con)) {
  if (v) sot += v;
  console.log(`   ${String(v).padStart(6)}  ${k}${v ? '   ⚠ CÒN SÓT' : ''}`);
}
process.exit(sot ? 1 : 0);
