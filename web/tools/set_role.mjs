/**
 * ĐẶT VAI TRÒ cho một tài khoản.
 *
 *   node tools/set_role.mjs <email> <learner|teacher|admin> [--project ky-su-nhi]
 *
 * Phải đặt ở HAI CHỖ và tệp này lo cả hai:
 *   1. users/{uid}.role          — để giao diện biết hiện màn nào
 *   2. custom claim trong token  — để LUẬT BẢO MẬT tin
 *
 * Thiếu chỗ 2 thì luật vẫn coi là học sinh thường: giao diện hiện bảng giáo viên
 * nhưng Firestore từ chối mọi lượt đọc, màn hình trống trơn mà không rõ vì sao.
 *
 * Người dùng phải ĐĂNG XUẤT rồi đăng nhập lại thì token mới mang vai trò mới.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const [email, role, ...rest] = process.argv.slice(2);
const ROLES = ['learner', 'teacher', 'admin'];
const flag = (n, d = null) => {
  const i = rest.indexOf(`--${n}`);
  return i >= 0 && rest[i + 1] ? rest[i + 1] : d;
};

if (!email || !ROLES.includes(role)) {
  console.error('Dùng: node tools/set_role.mjs <email> <learner|teacher|admin> [--project <mã>]');
  process.exit(1);
}

const project = flag('project')
  || (fs.existsSync('.firebaserc') && JSON.parse(fs.readFileSync('.firebaserc', 'utf8')).projects?.default);
if (!project) { console.error('Không biết dự án nào. Thêm --project.'); process.exit(1); }

const cfg = path.join(os.homedir(), '.config', 'configstore', 'firebase-tools.json');
const tok = fs.existsSync(cfg) ? (JSON.parse(fs.readFileSync(cfg, 'utf8')).tokens || {}).access_token : null;
if (!tok) { console.error('Chưa đăng nhập. Chạy: firebase login'); process.exit(1); }

const H = { Authorization: `Bearer ${tok}`, 'Content-Type': 'application/json' };
const api = async (url, body, method = 'POST') => {
  const r = await fetch(url, { method, headers: H, body: body === undefined ? undefined : JSON.stringify(body) });
  const t = await r.text();
  if (!r.ok) throw new Error(`${r.status} ${t.slice(0, 300)}`);
  return t ? JSON.parse(t) : {};
};

const IDT = `https://identitytoolkit.googleapis.com/v1/projects/${project}`;
const FS = `https://firestore.googleapis.com/v1/projects/${project}/databases/(default)/documents`;

/* 1 · tìm tài khoản theo email */
const found = await api(`${IDT}/accounts:lookup`, { email: [email.toLowerCase()] });
const user = (found.users || [])[0];
if (!user) {
  console.error(`Không thấy tài khoản ${email}.`);
  console.error('Người đó phải ĐĂNG NHẬP MỘT LẦN trước để hệ thống lập hồ sơ.');
  process.exit(1);
}
const uid = user.localId;

/* 2 · custom claim — chỗ luật bảo mật thật sự đọc */
await api(`${IDT}/accounts:update`, { localId: uid, customAttributes: JSON.stringify({ role }) });

/* 3 · users/{uid}.role — chỗ giao diện đọc */
await api(`${FS}/users/${uid}?updateMask.fieldPaths=role`,
  { fields: { role: { stringValue: role } } }, 'PATCH');

/* 4 · đọc lại để chắc */
const back = await api(`${IDT}/accounts:lookup`, { localId: [uid] });
const claim = JSON.parse(back.users[0].customAttributes || '{}');
const doc = await fetch(`${FS}/users/${uid}`, { headers: H }).then((r) => r.json());

console.log(`  ${email}  →  ${role}`);
console.log(`    custom claim  : ${claim.role === role ? '✓' : '✗'} ${claim.role}`);
console.log(`    users/{uid}   : ${doc.fields?.role?.stringValue === role ? '✓' : '✗'} ${doc.fields?.role?.stringValue}`);
console.log('\n  Người dùng phải ĐĂNG XUẤT rồi đăng nhập lại thì token mới mang vai trò mới.');
