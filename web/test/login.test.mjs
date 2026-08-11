/**
 * Kiểm bộ dịch lỗi của màn đăng nhập — chạy: node test/login.test.mjs
 *
 * Vì sao đáng một tệp test riêng: đây là chỗ DUY NHẤT bố mẹ nhìn thấy khi có trục trặc.
 * Lọt ra một chữ "internal" là họ đứng hình, không biết phải làm gì tiếp.
 */
import { readFileSync } from 'node:fs';

// LoginScreen.jsx là JSX nên node không nạp thẳng được — bóc riêng hàm niceError ra chạy.
const src = readFileSync(new URL('../src/chung/components/LoginScreen.jsx', import.meta.url), 'utf8');
const body = src.slice(src.indexOf('export function niceError'), src.indexOf('\n}\n', src.indexOf('export function niceError')) + 2);
const niceError = new Function(`${body.replace('export function', 'function')}; return niceError;`)();

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const VN = /[àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểàảãá]/i;
const noCode = (s) => !/(internal|unavailable|permission-denied|resource-exhausted|invalid-argument|functions\/|auth\/)/i.test(s);

/* ── 1 · không bao giờ lọt mã kỹ thuật ra màn hình ── */
const codes = [
  'internal', 'unavailable', 'deadline-exceeded', 'unauthenticated', 'functions/not-found',
  'auth/network-request-failed', 'FirebaseError: internal', '', null, undefined,
  'Firebase: Error (auth/invalid-credential).',
];
for (const c of codes) {
  const out = niceError(c);
  t(`"${String(c).slice(0, 28)}" → câu tiếng Việt`, VN.test(out) && noCode(out) && out.length > 10);
}

/* ── 2 · dịch đúng từng tình huống ── */
t('email sai định dạng', niceError('invalid-argument: bad').includes('Email chưa đúng'));
t('sai mật khẩu', niceError('auth/wrong-password').includes('mật khẩu chưa đúng'));
t('mất mạng', niceError('unavailable').includes('Mạng đang chập chờn'));
t('gọi không tới máy chủ thì gợi ý lối thoát',
  niceError('internal').includes('Để sau'));
t('thử quá nhiều lần', niceError('auth/too-many-requests').includes('quá nhiều lần'));

/* ── 3 · thông điệp tiếng Việt mình tự viết ở máy chủ thì GIỮ NGUYÊN ── */
t('giữ nguyên lời nhắc chờ bao lâu',
  niceError('resource-exhausted: Bạn vừa xin mã rồi. Thử lại sau 42 giây nhé.')
    === 'Bạn vừa xin mã rồi. Thử lại sau 42 giây nhé.');
t('giữ nguyên lời báo nhập sai',
  niceError('permission-denied: Mã không đúng.') === 'Mã không đúng.');
t('mã lỗi tiếng Anh kèm permission-denied thì KHÔNG hiện trần',
  noCode(niceError('permission-denied: forbidden')));

/* ── 4 · câu tiếng Việt bất kỳ thì hiện nguyên ── */
t('câu tiếng Việt tự viết được giữ',
  niceError(new Error('Chưa cấu hình máy chủ.')) === 'Chưa cấu hình máy chủ.');
t('đối tượng Error cũng đọc được',
  VN.test(niceError(new Error('unavailable'))));

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
