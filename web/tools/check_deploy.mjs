/**
 * KIỂM SAU TRIỂN KHAI — chạy: node tools/check_deploy.mjs
 *
 * Soi những thứ dễ quên nhất khi đưa lên mạng, mỗi cái một dòng rõ đạt hay không.
 * Chạy được cả trước lẫn sau khi deploy; cái nào cần mạng thì tự bỏ qua nếu chưa đăng nhập.
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

let ok = 0, bad = 0;
const t = (name, pass, hint = '') => {
  if (pass) { ok++; console.log(`  ✓ ${name}`); }
  else { bad++; console.log(`  ✗ ${name}${hint ? `\n      → ${hint}` : ''}`); }
};
const head = (s) => console.log(`\n── ${s} ──`);
const sh = (cmd, args) => {
  try { return execFileSync(cmd, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); }
  catch { return null; }
};

/* ── 1 · tệp cấu hình ── */
head('Cấu hình');
const fb = JSON.parse(readFileSync('firebase.json', 'utf8'));
t('firebase.json đọc được', !!fb.hosting && !!fb.firestore);
t('đã gắn dự án (.firebaserc)', existsSync('.firebaserc'),
  'chạy: firebase use --add');
t('có .env.local cho web', existsSync('.env.local'),
  'sao chép .env.example rồi điền 6 giá trị từ Console');
if (existsSync('.env.local')) {
  const env = readFileSync('.env.local', 'utf8');
  const keys = ['VITE_FB_API_KEY', 'VITE_FB_AUTH_DOMAIN', 'VITE_FB_PROJECT_ID',
                'VITE_FB_STORAGE_BUCKET', 'VITE_FB_SENDER_ID', 'VITE_FB_APP_ID'];
  const missing = keys.filter((k) => !new RegExp(`^${k}=.+`, 'm').test(env));
  t('đủ 6 khoá cấu hình web', missing.length === 0, `thiếu: ${missing.join(', ')}`);
  t('không còn giá trị mẫu', !/your-project|demo-xem-giao-dien/.test(env),
    '.env.local vẫn đang chứa giá trị ví dụ');
}
t('.env.local nằm trong .gitignore',
  readFileSync('../.gitignore', 'utf8').includes('.env.local'));

/* ── 2 · luật bảo mật ── */
head('Luật bảo mật');
const rules = readFileSync('firestore.rules', 'utf8');
t('nhật ký attempts BẤT BIẾN',
  /match \/attempts[\s\S]*?allow update, delete: if false/.test(rules),
  'thiếu dòng này là điểm đã ghi sửa được — mất tính bằng chứng');
t('không ai tự phong vai trò được',
  /request\.resource\.data\.role == resource\.data\.role/.test(rules),
  'thiếu là ai cũng đặt role=teacher rồi đọc kết quả cả trường');
t('vai trò đọc từ token, không từ Firestore',
  /request\.auth\.token\.role/.test(rules));
t('otpCodes cấm mọi người', /match \/otpCodes[\s\S]*?allow read, write: if false/.test(rules));
t('có luật chặn mặc định ở cuối',
  /match \/\{document=\*\*\}\s*\{\s*allow read, write: if false/.test(rules));

const st = readFileSync('storage.rules', 'utf8');
t('ảnh đại diện kiểm chủ sở hữu',
  /userId == request\.auth\.uid/.test(st),
  'thiếu là ai cũng ghi đè ảnh của mọi trẻ khác');

/* ── 3 · chỉ mục ── */
head('Chỉ mục truy vấn');
const idx = JSON.parse(readFileSync('firestore.indexes.json', 'utf8'));
const has = (fields) => idx.indexes.some((i) =>
  JSON.stringify(i.fields.map((f) => f.fieldPath)) === JSON.stringify(fields));
t('lịch sử của một người theo thời gian', has(['learnerId', 'ts']));
t('bảng giáo viên quét theo mốc máy chủ', has(['mustPass', 'correct', 'serverTs'])
  || idx.indexes.some((i) => i.fields.some((f) => f.fieldPath === 'serverTs')));
t('danh sách học sinh theo vai trò', has(['role', 'displayName']));

/* ── 4 · Functions ── */
head('Cloud Functions');
t('đã cài phụ thuộc', existsSync('functions/node_modules'), 'cd functions && npm install');
const fnSrc = readFileSync('functions/index.js', 'utf8');
t('runtime còn hạn (Node 20 ngừng hẳn 30/10/2026)',
  JSON.parse(readFileSync('firebase.json', 'utf8')).functions?.runtime !== 'nodejs20',
  'đổi firebase.json → functions.runtime sang nodejs22');
t('defineSecret lấy đúng chỗ',
  /from 'firebase-functions\/params'/.test(fnSrc),
  "lấy từ 'firebase-functions/v2' là deploy vỡ ngay bước phân tích");
/* Firebase coi MỌI export là một Cloud Function. Chốt danh sách theo TÊN chứ không
   theo số lượng: đếm số thì thêm một hàm mới lại đỏ, mà đổi tên hàm cũ lại vẫn xanh. */
const HAM_MONG_DOI = ['onAttempt', 'onMicroDone', 'nightlyReport', 'nightlyTeacherBoard',
                      'refreshTeacherBoard', 'requestOtp', 'verifyOtp'];
const exported = [...fnSrc.matchAll(/^export const (\w+)/gm)].map((m) => m[1]);
const thieu = HAM_MONG_DOI.filter((h) => !exported.includes(h));
const thua = exported.filter((h) => !HAM_MONG_DOI.includes(h));
t(`xuất đúng ${HAM_MONG_DOI.length} hàm (thiếu: ${thieu.join(',') || 'không'} · thừa: ${thua.join(',') || 'không'})`,
  thieu.length === 0 && thua.length === 0);
t('không lẫn hàm thường vào danh sách xuất',
  !exported.includes('masteryOf'),
  'Firebase coi mọi export là Cloud Function — hàm thường lọt ra là sinh hàm rác');

/* ── 5 · nội dung ── */
head('Nội dung');
t('bản build có sẵn', existsSync('dist/index.html'), 'chạy: npm run build');
if (existsSync('dist/content/lessons')) {
  t('bản build có đủ 168 bài', readdirSync('dist/content/lessons').length === 168);
  t('bản build có đủ 672 hình', readdirSync('dist/content/figures').length === 672);
}
const micro = JSON.parse(readFileSync('public/content/index_micro.json', 'utf8'));
t('chỉ mục có tên bài và mục tiêu cho con',
  Object.values(micro).every((m) => m.title && m.objectiveKid));

/* ── 6 · phần cần mạng ── */
head('Trên máy chủ (bỏ qua nếu chưa đăng nhập)');
const who = sh('firebase', ['login:list']);
if (!who || /No authorized/.test(who)) {
  console.log('  · chưa đăng nhập firebase — bỏ qua các mục cần mạng');
} else {
  const secrets = sh('firebase', ['functions:secrets:access', 'OTP_PEPPER']) ? true : false;
  t('đã đặt bí mật OTP_PEPPER', secrets, 'firebase functions:secrets:set OTP_PEPPER');
  for (const [name, why] of [
    ['SMTP_USER', 'địa chỉ Gmail dùng để gửi mã'],
    ['SMTP_PASS', 'mật khẩu ỨNG DỤNG 16 ký tự — CHƯA ĐẶT thì mã chỉ in ra log, không ai đăng nhập được'],
    ['SMTP_HOST', 'máy chủ SMTP, thường là smtp.gmail.com'],
  ]) {
    t(`đã đặt bí mật ${name}`, !!sh('firebase', ['functions:secrets:access', name]), why);
  }
  const list = sh('firebase', ['functions:list']);
  if (list) {
    for (const f of ['requestOtp', 'verifyOtp', 'onAttempt', 'onMicroDone',
                     'nightlyReport', 'nightlyTeacherBoard']) {
      t(`hàm ${f} đã lên`, list.includes(f));
    }
  }
}

console.log(`\n${ok} ĐẠT · ${bad} CHƯA ĐẠT`);
process.exit(bad ? 1 : 0);
