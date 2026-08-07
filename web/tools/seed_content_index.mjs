/**
 * Nạp chỉ mục micro lên Firestore (collection contentIndex) để Cloud Function biết
 * lịch ôn, tên bài và tên bẫy của từng micro mà không phải tải cả file bài học.
 *
 * Hai cách chạy — chọn cách nào cũng được:
 *
 *   1. Dùng phiên đăng nhập Firebase CLI (tiện nhất, không phải tải khoá về máy):
 *        firebase login                     # nếu chưa đăng nhập
 *        node tools/seed_content_index.mjs --project ky-su-nhi
 *
 *   2. Dùng khoá dịch vụ (khi chạy trong CI, không có người ngồi trước máy):
 *        export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
 *        node tools/seed_content_index.mjs --project ky-su-nhi --admin
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const args = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : fallback;
};
const useAdmin = args.includes('--admin');

const idx = JSON.parse(fs.readFileSync('public/content/index_micro.json', 'utf8'));
const entries = Object.entries(idx);

/* Mã dự án: lấy từ cờ dòng lệnh, hoặc .firebaserc, hoặc biến môi trường */
function detectProject() {
  const flag = arg('project');
  if (flag) return flag;
  try {
    const rc = JSON.parse(fs.readFileSync('.firebaserc', 'utf8'));
    if (rc.projects?.default) return rc.projects.default;
  } catch { /* không có .firebaserc */ }
  return process.env.GCLOUD_PROJECT || process.env.FIREBASE_PROJECT || null;
}

const project = detectProject();
if (!project) {
  console.error('Không biết nạp vào dự án nào. Thêm --project <mã>, hoặc chạy firebase use --add.');
  process.exit(1);
}

/* ─────────── Cách 2: Admin SDK ─────────── */
if (useAdmin) {
  const { initializeApp, applicationDefault } = await import('firebase-admin/app');
  const { getFirestore } = await import('firebase-admin/firestore');
  initializeApp({ credential: applicationDefault(), projectId: project });
  const db = getFirestore();
  let n = 0;
  for (const [key, val] of entries) {
    await db.doc(`contentIndex/${key}`).set(val, { merge: true });
    n++;
  }
  console.log(`đã nạp ${n} bản ghi vào contentIndex (dự án ${project})`);
  process.exit(0);
}

/* ─────────── Cách 1: mượn phiên đăng nhập của Firebase CLI ─────────── */
function cliToken() {
  const p = path.join(os.homedir(), '.config', 'configstore', 'firebase-tools.json');
  if (!fs.existsSync(p)) return null;
  const t = JSON.parse(fs.readFileSync(p, 'utf8')).tokens || {};
  // Token sống khoảng một giờ; hết hạn thì chạy bất kỳ lệnh firebase nào để làm mới.
  if (t.expires_at && Date.now() > t.expires_at) return null;
  return t.access_token || null;
}

const token = cliToken();
if (!token) {
  console.error('Chưa có phiên đăng nhập Firebase còn hiệu lực.');
  console.error('Chạy:  firebase login       rồi thử lại.');
  console.error('(hoặc dùng khoá dịch vụ với cờ --admin)');
  process.exit(1);
}

/** Bọc giá trị JS thành kiểu Firestore REST */
function toValue(v) {
  if (v === null || v === undefined) return { nullValue: null };
  if (typeof v === 'boolean') return { booleanValue: v };
  if (typeof v === 'number') return Number.isInteger(v)
    ? { integerValue: String(v) } : { doubleValue: v };
  if (Array.isArray(v)) return { arrayValue: { values: v.map(toValue) } };
  if (typeof v === 'object') return { mapValue: { fields: toFields(v) } };
  return { stringValue: String(v) };
}
const toFields = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, toValue(v)]));

/**
 * Hai chuỗi KHÁC NHAU, hay bị lẫn:
 *   · URL để gọi HTTP  — có https://firestore.googleapis.com/v1/
 *   · name của document — chỉ đường dẫn tài nguyên, BẮT ĐẦU bằng "projects/".
 * Đưa nhầm URL vào name thì Firestore báo: lacks "projects" at index 0.
 */
const DOCS = `projects/${project}/databases/(default)/documents`;
const BASE = `https://firestore.googleapis.com/v1/${DOCS}`;

/** Ghi theo lô — Firestore nhận tối đa 500 phép ghi mỗi lần commit */
async function commit(batch) {
  const res = await fetch(`${BASE}:commit`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      writes: batch.map(([key, val]) => ({
        update: { name: `${DOCS}/contentIndex/${key}`, fields: toFields(val) },
        // không có updateMask thì Firestore GHI ĐÈ cả document; ta muốn đúng như vậy
      })),
    }),
  });
  if (!res.ok) throw new Error(`${res.status} ${(await res.text()).slice(0, 300)}`);
}

let done = 0;
const SIZE = 200;
for (let i = 0; i < entries.length; i += SIZE) {
  const batch = entries.slice(i, i + SIZE);
  await commit(batch);
  done += batch.length;
  process.stdout.write(`\r  đã nạp ${done}/${entries.length}…`);
}
console.log(`\nđã nạp ${done} bản ghi vào contentIndex (dự án ${project})`);
