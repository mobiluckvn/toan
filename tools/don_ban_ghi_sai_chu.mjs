/**
 * DỌN 130 bản ghi `attempts` bị gán nhầm chủ, rồi DỰNG LẠI `mastery`.
 *
 *     export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
 *     node tools/don_ban_ghi_sai_chu.mjs            # CHẠY KHÔ — chỉ xem, không đụng
 *     node tools/don_ban_ghi_sai_chu.mjs --that     # làm thật
 *
 * ⚠ XOÁ DỮ LIỆU HỌC THẬT CỦA TRẺ, KHÔNG LÙI ĐƯỢC bằng một lệnh. Nên tệp này:
 *   ① SAO LƯU ra tệp JSON trước khi xoá bất cứ thứ gì — cả bản ghi sắp xoá lẫn
 *      toàn bộ `mastery` hiện thời. Có bản sao thì dựng lại được, kể cả khi sau
 *      này bác đổi ý muốn TRẢ VỀ ĐÚNG CHỦ thay vì xoá;
 *   ② mặc định CHẠY KHÔ. Phải gõ `--that` mới đụng vào máy chủ.
 *
 * ── AI LÀ CHỦ THẬT, VÀ VÌ SAO CHẮC ──
 * Một `sessionId` chỉ sinh ra ở MỘT lần mở bài của MỘT bé, nên hai bé cùng mang
 * một mã phiên là chuyện không thể tự nhiên. Trong cả 7 phiên như thế, ba dấu
 * hiệu ĐỘC LẬP chỉ về cùng một phía:
 *
 *   bé CHỦ THẬT   1 lượt · `ts` ≈ `serverTs` (lên ngay) · CÓ sổ tiến độ bài ấy
 *   bé BỊ GÁN     16–30 lượt · lên máy chủ vài ngày sau · KHÔNG có sổ tiến độ
 *
 * Sổ tiến độ (`progress`/`progressTA`) đi đường ghi KHÁC hẳn hàng đợi `attempts`,
 * nên nó là nhân chứng độc lập: bé không có sổ tiến độ của bài ấy nghĩa là chưa
 * từng mở bài ấy.
 *
 * ⚠ KHÔNG dùng "độ trễ giữa `ts` và `serverTs`" làm tiêu chí — đã thử: trung vị
 *    của CẢ KHO là 25 giờ, vì lỗi hàng đợi nghẽn làm gần như bản ghi nào cũng
 *    từng nằm kẹt. Tiêu chí ấy không tách được gì.
 *
 * ── DỰNG LẠI `mastery` ──
 * Dựng cho MỌI bé, không riêng bé bị đụng: `mastery` là thứ suy ra hoàn toàn từ
 * `attempts`, dựng lại cả kho thì mọi bé cùng một luật, không bé nửa cũ nửa mới.
 *
 * ⚠ ĐỒNG HỒ DÙNG `ts` CHỨ KHÔNG PHẢI GIỜ CHẠY. `applyAttempt` phân rã trí nhớ
 *    theo khoảng cách tới `lastSeen`. Lần chạy gốc dùng giờ CỦA HÀM NỀN — mà vì
 *    lỗi hàng đợi, hàm nền chạy muộn hơn lúc bé làm bài có khi mấy ngày, nên mức
 *    thạo cũ đã bị phân rã oan. Dựng lại theo `ts` (lúc bé BẤM) là đúng ý mô
 *    hình. Hệ quả phải nói ra: con số mới sẽ KHÁC con số cũ ở cả những bé không
 *    mất bản ghi nào — khác vì nay đúng hơn, không phải vì xoá.
 */
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const doi = createRequire(new URL('../web/functions/package.json', import.meta.url));
const { initializeApp, cert } = doi('firebase-admin/app');
const { getFirestore } = doi('firebase-admin/firestore');
const { applyAttempt } = await import('../web/functions/src/bkt.js');

const THAT = process.argv.includes('--that');
const KHOA = process.env.GOOGLE_APPLICATION_CREDENTIALS;
if (!KHOA || !existsSync(KHOA)) {
  console.error('✗ thiếu khoá quản trị.\n  export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json\n  ⚠ Khoá để NGOÀI thư mục kho — nó mở được toàn bộ dữ liệu dự án.');
  process.exit(1);
}
initializeApp({ credential: cert(JSON.parse(readFileSync(KHOA, 'utf8'))) });
const db = getFirestore();

const iso = (t) => (t ? new Date(t).toISOString().slice(0, 16).replace('T', ' ') : '—');
const khoaTienDo = (mon) => (mon === 'toan' ? 'progress' : 'progressTA');

console.log(THAT ? '\n⚠ CHẾ ĐỘ LÀM THẬT\n' : '\n▸ CHẠY KHÔ — không đụng gì vào máy chủ. Thêm --that để làm thật.\n');

/* ═══ ① TÌM BẢN GHI SAI CHỦ ════════════════════════════════════════════════ */
const tatCa = await db.collection('attempts').get();
const theoPhien = new Map();
tatCa.forEach((d) => {
  const s = d.get('sessionId');
  if (!theoPhien.has(s)) theoPhien.set(s, []);
  theoPhien.get(s).push(d);
});

const xoa = [];
const bang = [];
for (const [s, ds] of theoPhien) {
  const be = [...new Set(ds.map((d) => d.get('learnerId')))];
  if (be.length < 2) continue;
  /* Với mỗi bé trong phiên: có sổ tiến độ của bài ấy không? */
  const soi = [];
  for (const b of be) {
    const r = ds.filter((d) => d.get('learnerId') === b);
    const micros = [...new Set(r.map((d) => d.get('microId')))];
    let coTienDo = false;
    for (const mi of micros) {
      const k = `${khoaTienDo(r[0].get('mon') || 'toan')}/${b}/micros/${mi.replace(/[^A-Za-z0-9]+/g, '_')}`;
      if ((await db.doc(k).get()).exists) { coTienDo = true; break; }
    }
    soi.push({ be: b, r, coTienDo });
  }
  /* ── NHÂN CHỨNG THỨ HAI: GIỜ BẤM SO VỚI GIỜ SINH MÃ PHIÊN ──
     Sổ tiến độ chỉ được ghi khi bé NỘP bài. Bé bỏ dở sau vài câu thì không có sổ
     tiến độ, và nhân chứng thứ nhất im lặng — đúng cảnh phiên `smslukqqe8m4a`.

     Nhưng còn một dấu vết nữa, và nó cứng hơn: mã phiên nhúng GIỜ SINH
     (`newSessionId` = 's' + Date.now().toString(36) + ngẫu nhiên), còn mỗi bản
     ghi mang `ts` là lúc bé BẤM. Bản ghi bị sang tên vẫn giữ nguyên `ts` gốc —
     tức giờ bấm của bé A. Nên bé nào có `serverTs` cách `ts` hàng ngày TRONG KHI
     bé kia lên ngay tức thì, thì bé lên muộn ấy đang giữ bản ghi làm ra ở phiên
     của người khác: không ai trả lời được câu hỏi trong một phiên mở trên máy
     người khác từ mấy ngày trước.

     ⚠ CHỈ dùng làm nhân chứng KHI phiên có đúng một bé "lên ngay". Độ trễ tự nó
     KHÔNG phải bằng chứng — trung vị cả kho là 25 giờ vì lỗi hàng đợi nghẽn. Cái
     nói lên chuyện là SỰ TƯƠNG PHẢN trong cùng một phiên. */
  const NGAY_TUC_THI = 0.5;   // giờ
  for (const x of soi) {
    const ts = x.r.map((d) => d.get('ts')).filter(Boolean);
    const sv = x.r.map((d) => d.get('serverTs')?.toMillis?.()).filter(Boolean);
    x.tre = (ts.length && sv.length) ? (Math.min(...sv) - Math.min(...ts)) / 3600000 : null;
  }
  const lenNgay = soi.filter((x) => x.tre != null && x.tre < NGAY_TUC_THI);
  const lenMuon = soi.filter((x) => x.tre != null && x.tre >= NGAY_TUC_THI);

  const chuThat = soi.filter((x) => x.coTienDo).length
    ? soi.filter((x) => x.coTienDo)
    : (lenNgay.length === 1 && lenMuon.length ? lenNgay : []);
  const khongChu = soi.filter((x) => x.coTienDo).length
    ? soi.filter((x) => !x.coTienDo)
    : (lenNgay.length === 1 && lenMuon.length ? lenMuon : []);
  /* ⚠ CHỈ XOÁ KHI HÌNH DẠNG ĐÚNG NHƯ ĐÃ MÔ TẢ: đúng một bé có sổ tiến độ, và
     (các) bé kia thì không. Lệch khuôn thì BỎ QUA và báo — thà sót còn hơn xoá
     nhầm bài của một bé có thật. */
  if (chuThat.length !== 1 || khongChu.length === 0) {
    bang.push({ phien: s.slice(0, 16), tinhTrang: '⚠ KHÔNG rõ chủ — BỎ QUA', chi: soi.map((x) => `${x.be.slice(0, 8)}:${x.r.length}${x.coTienDo ? '✓' : '✗'}`).join(' ') });
    continue;
  }
  for (const x of khongChu) x.r.forEach((d) => xoa.push(d));
  bang.push({
    phien: s.slice(0, 16),
    chuThat: `${chuThat[0].be.slice(0, 8)}… (${chuThat[0].r.length} lượt, ${chuThat[0].coTienDo ? 'có sổ tiến độ' : `lên ngay ${chuThat[0].tre?.toFixed(1)}h`})`,
    xoaCua: khongChu.map((x) => `${x.be.slice(0, 8)}… (${x.r.length} lượt${x.coTienDo ? '' : `, trễ ${x.tre?.toFixed(1)}h`})`).join(' · '),
    luc: iso(Math.min(...ds.map((d) => d.get('ts')).filter(Boolean))),
  });
}
console.log('── ① Phiên bị hai bé cùng mang');
console.table(bang);
console.log(`  ⇒ sẽ xoá ${xoa.length} bản ghi / tổng ${tatCa.size}\n`);

/* ═══ ② SAO LƯU ════════════════════════════════════════════════════════════ */
const masteryTruoc = [];
for (const cha of await db.collection('mastery').listDocuments()) {
  for (const u of (await cha.collection('units').get()).docs) {
    masteryTruoc.push({ uid: cha.id, unit: u.id, data: u.data() });
  }
}
const luu = {
  luc: new Date().toISOString(),
  banGhiXoa: xoa.map((d) => ({ id: d.id, data: d.data() })),
  masteryTruocKhiDung: masteryTruoc,
};
/* ⚠ KHÔNG BAO GIỜ ĐÈ BẢN SAO LƯU CŨ. Chạy lần hai mà ghi đè lên tệp lần một là
   mất luôn đường lùi của lần một — mà lần một mới là lần xoá nhiều. Thấy tệp đã
   có thì đánh số tiếp. */
const tepLuu = (() => {
  const goc = new URL('../sao_luu_don_ban_ghi', import.meta.url).pathname;
  if (!existsSync(`${goc}.json`)) return `${goc}.json`;
  for (let i = 2; i < 100; i += 1) if (!existsSync(`${goc}_${i}.json`)) return `${goc}_${i}.json`;
  throw new Error('quá nhiều bản sao lưu — dọn bớt đi đã');
})();
if (THAT) {
  writeFileSync(tepLuu, JSON.stringify(luu, (k, v) => (v?.toDate ? v.toDate().toISOString() : v), 1));
  console.log(`── ② Đã sao lưu ${xoa.length} bản ghi + ${masteryTruoc.length} mục mastery`);
  console.log(`   → ${tepLuu}`);
  console.log('   (tệp này nằm ngoài git — xem .gitignore)\n');
} else {
  console.log(`── ② Sẽ sao lưu ${xoa.length} bản ghi + ${masteryTruoc.length} mục mastery ra ${tepLuu}\n`);
}

/* ═══ ③ XOÁ ════════════════════════════════════════════════════════════════ */
if (THAT && xoa.length) {
  for (let i = 0; i < xoa.length; i += 400) {
    const lo = db.batch();
    xoa.slice(i, i + 400).forEach((d) => lo.delete(d.ref));
    await lo.commit();
  }
  const lai = await db.collection('attempts').get();
  console.log(`── ③ Đã xoá. attempts: ${tatCa.size} → ${lai.size} (giảm ${tatCa.size - lai.size})\n`);
} else {
  console.log(`── ③ Sẽ xoá ${xoa.length} bản ghi\n`);
}

/* ═══ ④ DỰNG LẠI mastery ═══════════════════════════════════════════════════ */
const conLai = THAT ? (await db.collection('attempts').get()).docs
  : tatCa.docs.filter((d) => !xoa.some((x) => x.id === d.id));

const PHA = ['practice', 'assess', 'check', 'worked'];
const theoBe = new Map();
for (const d of conLai) {
  const a = d.data();
  if (!a.learnerId || !a.bktUnit || !PHA.includes(a.phase)) continue;
  if (!theoBe.has(a.learnerId)) theoBe.set(a.learnerId, []);
  theoBe.get(a.learnerId).push(a);
}

const moi = [];
for (const [uid, ds] of theoBe) {
  /* Theo ĐÚNG thứ tự bé làm bài — `ts` là lúc bé bấm, không phải lúc lên máy chủ. */
  ds.sort((x, y) => (x.ts ?? 0) - (y.ts ?? 0));
  const nut = new Map();
  for (const a of ds) {
    const cu = nut.get(a.bktUnit);
    const sau = applyAttempt(cu, a, () => (a.ts ?? Date.now()));
    nut.set(a.bktUnit, {
      ...sau, unit: a.bktUnit, learnerId: uid, mon: a.mon || 'toan', maNutDs: a.maNutDs ?? null,
    });
  }
  for (const [u, v] of nut) moi.push({ uid, unit: encodeURIComponent(u), data: v });
}

console.log('── ④ Dựng lại mastery');
console.log(`   trước: ${masteryTruoc.length} mục · sau: ${moi.length} mục`);
const cuKey = new Set(masteryTruoc.map((x) => `${x.uid}/${x.unit}`));
const moiKey = new Set(moi.map((x) => `${x.uid}/${x.unit}`));
const thua = [...cuKey].filter((k) => !moiKey.has(k));
console.log(`   mục CŨ nay không còn căn cứ (sẽ xoá): ${thua.length}`);
if (thua.length) thua.slice(0, 10).forEach((k) => console.log(`      ${k}`));

if (THAT) {
  for (let i = 0; i < moi.length; i += 400) {
    const lo = db.batch();
    moi.slice(i, i + 400).forEach((x) => lo.set(db.doc(`mastery/${x.uid}/units/${x.unit}`), x.data));
    await lo.commit();
  }
  for (let i = 0; i < thua.length; i += 400) {
    const lo = db.batch();
    thua.slice(i, i + 400).forEach((k) => lo.delete(db.doc(`mastery/${k.split('/')[0]}/units/${k.split('/')[1]}`)));
    await lo.commit();
  }
  const dem = [];
  for (const cha of await db.collection('mastery').listDocuments()) {
    dem.push(...(await cha.collection('units').listDocuments()));
  }
  console.log(`   ✓ đã ghi. mastery nay có ${dem.length} mục\n`);
} else {
  console.log('   (chạy khô — chưa ghi gì)\n');
}
