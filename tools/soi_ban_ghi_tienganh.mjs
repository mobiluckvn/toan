/**
 * SOI bằng khoá quản trị hai thứ mà buổi đi thử 23-08-2026 KHÔNG tự xác nhận được.
 *
 *     export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
 *     node tools/soi_ban_ghi_tienganh.mjs             # soi bé mới nhất
 *     node tools/soi_ban_ghi_tienganh.mjs <uid>       # soi đúng một bé
 *
 * ── HAI CÂU HỎI, VÀ VÌ SAO MÁY CON KHÔNG TRẢ LỜI ĐƯỢC ──
 *
 *   ① `hocBaTA/{uid}/muc` loại `phien` — bản ghi BỎ DỞ.
 *      Buổi đi thử chỉ chứng minh được điều PHỦ ĐỊNH: console không có
 *      `permission-denied`, tức luật KHÔNG từ chối. Nhưng "không bị từ chối"
 *      không phải "đã ghi đúng nội dung" — cùng họ với cái bẫy `firestore:delete`
 *      trả mã thoát 0 cho cả kho không tồn tại. Phải mở tài liệu ra nhìn.
 *
 *   ② `attempts` — ba trường vân tay prompt.
 *      Việc ① của phụ lục Chương 2. Máy con CÓ gửi, nhưng kênh ghi của Firestore
 *      là luồng nhị phân, đọc mạng chỉ thấy 200 chứ không thấy đã ghi trường gì.
 *
 * ⚠ TỆP NÀY CHỈ ĐỌC. Không ghi, không xoá, không sửa — muốn xoá thì dùng
 *    `tools/xoa_log_tienganh.mjs`, tệp ấy có đếm trước/đếm sau tử tế.
 *
 * ⚠ VÀ NÓ IN RA DỮ LIỆU HỌC CỦA MỘT BÉ CÓ THẬT. Chạy trên máy bác thì được;
 *    đừng dán nguyên đầu ra vào tài liệu nộp — cắt lấy phần cần rồi bỏ `uid`.
 */
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';

/* Mượn `firebase-admin` của `web/functions` — cùng lý do đã ghi ở
   `xoa_log_tienganh.mjs`: hai bản thì sớm muộn lệch phiên bản. */
const doi = createRequire(new URL('../web/functions/package.json', import.meta.url));
const { initializeApp, cert, applicationDefault } = doi('firebase-admin/app');
const { getFirestore } = doi('firebase-admin/firestore');

const KHOA = process.env.GOOGLE_APPLICATION_CREDENTIALS;
if (!KHOA) {
  console.error(
    '✗ chưa có khoá quản trị.\n'
    + '  Firebase Console → Project settings → Service accounts →\n'
    + '  "Generate new private key", lưu thành ~/khoa-dich-vu.json rồi:\n'
    + '      export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json',
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

const uidChon = process.argv.find((x) => !x.startsWith('-') && x.length > 20
  && !x.includes('/'));

/** Bé nào mới học Tiếng Anh gần đây nhất — để khỏi phải gõ uid bằng tay. */
async function beMoiNhat() {
  const cha = await db.collection('hocBaTA').listDocuments();
  let tot = null;
  for (const d of cha) {
    const q = await d.collection('muc').orderBy('at', 'desc').limit(1).get();
    if (q.empty) continue;
    const at = q.docs[0].get('at');
    const t = typeof at === 'string' ? Date.parse(at) : (at?.toMillis?.() ?? 0);
    if (!tot || t > tot.t) tot = { uid: d.id, t };
  }
  return tot?.uid || null;
}

const uid = uidChon || await beMoiNhat();
if (!uid) { console.error('✗ không thấy bé nào có học bạ Tiếng Anh.'); process.exit(1); }
console.log(`\n══ Bé: ${uid}${uidChon ? '' : '  (bé có mục học bạ mới nhất)'}\n`);

/* ═══ ① BẢN GHI BỎ DỞ ══════════════════════════════════════════════════════ */
{
  const q = await db.collection(`hocBaTA/${uid}/muc`).get();
  const theoLoai = new Map();
  q.forEach((d) => {
    const l = d.get('loai') || '(không khai)';
    theoLoai.set(l, (theoLoai.get(l) || 0) + 1);
  });
  console.log('── ① hocBaTA · số mục theo loại');
  console.table([...theoLoai].map(([loai, so]) => ({ loai, so })));

  const phien = q.docs.filter((d) => d.get('loai') === 'phien');
  if (!phien.length) {
    console.log('⚠ KHÔNG có mục nào loại `phien`.\n'
      + '  Nghĩa là sự kiện BỎ DỞ chưa ghi được — hoặc luật chặn trong im lặng,\n'
      + '  hoặc hàm gỡ màn không chạy. ĐỪNG báo là đã có.\n');
  } else {
    console.log(`✓ có ${phien.length} bản ghi bỏ dở. Nội dung:`);
    console.table(phien.map((d) => {
      const g = d.get('giaTri') || {};
      return {
        khoa: d.id,
        bai: g.microId ?? '—',
        chang: g.chang ?? '—',
        soLuot: g.soLuot ?? '—',
        giay: g.giay ?? '—',
        luc: String(d.get('at') || '').slice(0, 19),
      };
    }));
    /* Mỗi lần bỏ dở PHẢI là một bản ghi riêng — gộp theo bài là mất chính con số
       đáng giá nhất (bỏ dở CÙNG một bài mấy lần). */
    const theoBai = new Map();
    phien.forEach((d) => {
      const b = d.get('giaTri')?.microId || '?';
      theoBai.set(b, (theoBai.get(b) || 0) + 1);
    });
    const lap = [...theoBai].filter(([, n]) => n > 1);
    console.log(lap.length
      ? `✓ có bài bị bỏ dở nhiều lần và ĐẾM RIÊNG từng lần: ${lap.map(([b, n]) => `${b}×${n}`).join(' · ')}`
      : 'ℹ mỗi bài mới bỏ dở 1 lần — chưa kiểm được việc KHÔNG gộp; bỏ dở cùng một bài lần nữa rồi soi lại.');
    const thieu = phien.filter((d) => {
      const g = d.get('giaTri') || {};
      return !g.microId || g.chang == null || !Number.isFinite(g.soLuot) || !Number.isFinite(g.giay);
    });
    console.log(thieu.length
      ? `⚠ ${thieu.length} bản ghi THIẾU trường: ${thieu.map((d) => d.id).join(', ')}`
      : '✓ mọi bản ghi đủ bốn trường microId · chang · soLuot · giay');
  }
}

/* ═══ ② VÂN TAY PROMPT TRONG `attempts` ════════════════════════════════════ */
{
  console.log('\n── ② attempts · vân tay prompt');
  const q = await db.collection('attempts')
    .where('learnerId', '==', uid).where('mon', '==', 'tienganh').get();
  if (q.empty) {
    console.log('⚠ bé này chưa có bản ghi `attempts` nào của Tiếng Anh.\n');
  } else {
    const coAI = q.docs.filter((d) => ['viet', 'phongNoi'].includes(d.get('cau')?.format)
      || d.get('mode') === 'phongNoi' || d.get('phase') === 'worked');
    console.log(`  tổng lượt Tiếng Anh: ${q.size} · trong đó lượt CÓ AI CHẤM: ${coAI.length}`);
    if (!coAI.length) {
      console.log('ℹ chưa có lượt nào do AI chấm → chưa kiểm được vân tay.\n'
        + '  Làm một bài VIẾT hoặc vào PHÒNG NÓI rồi soi lại.');
    } else {
      console.table(coAI.slice(0, 8).map((d) => ({
        id: d.id.slice(-28),
        dinhDang: d.get('cau')?.format ?? d.get('mode') ?? '—',
        mauPrompt: d.get('mauPrompt') ?? '(THIẾU)',
        phienBanMau: d.get('phienBanMau') ?? '(THIẾU)',
        vanTay: String(d.get('vanTayPrompt') ?? '(THIẾU)').slice(0, 16),
      })));
      const thieu = coAI.filter((d) => !d.get('mauPrompt') || !d.get('vanTayPrompt'));
      console.log(thieu.length
        ? `⚠ ${thieu.length}/${coAI.length} lượt AI chấm THIẾU vân tay — mục 2.5.2 chưa đạt trọn.`
        : `✓ cả ${coAI.length} lượt AI chấm đều mang đủ vân tay (mauPrompt · phienBanMau · vanTayPrompt).`);
      /* Vân tay băm KHUNG, không băm cả prompt — nên hai lượt cùng mẫu phải RA
         CÙNG một băm dù nội dung bé viết khác hẳn. Đây là chỗ dễ hỏng nhất. */
      const nhom = new Map();
      coAI.forEach((d) => {
        const k = `${d.get('mauPrompt')}@${d.get('phienBanMau')}`;
        if (!nhom.has(k)) nhom.set(k, new Set());
        nhom.get(k).add(d.get('vanTayPrompt'));
      });
      for (const [k, v] of nhom) {
        if (v.size > 1) {
          console.log(`⚠ mẫu ${k} ra ${v.size} vân tay KHÁC NHAU — nghĩa là đang băm cả `
            + 'nội dung riêng của bé chứ không chỉ băm khung. Xem `functions/src/vantay.js`.');
        }
      }
    }
  }
}

/* ═══ ③ ĐỐI CHIẾU: mastery có khớp số lượt không ═══════════════════════════ */
{
  console.log('\n── ③ mastery · P(L) engine đã tính');
  const q = await db.collection(`mastery/${uid}/units`).get();
  if (q.empty) {
    console.log('⚠ chưa có nút nào — hàm nền `onAttempt` chưa chạy hoặc chạy hỏng.\n');
  } else {
    console.table(q.docs.slice(0, 10).map((d) => ({
      nut: decodeURIComponent(d.id),
      p: Number(d.get('p') ?? 0).toFixed(3),
      pTruoc: d.get('pTruoc') == null ? '—' : Number(d.get('pTruoc')).toFixed(3),
      saiLienTiep: d.get('saiLienTiep') ?? '—',
      soLuot: d.get('nAttempts') ?? '—',
      mon: d.get('mon') ?? '(không khai)',
    })));
    console.log(`  tổng nút có P(L): ${q.size}`);
  }
}

console.log('');
