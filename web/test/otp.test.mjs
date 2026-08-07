/** Kiểm đăng nhập bằng OTP — chạy: node test/otp.test.mjs */
import {
  makeCode, hashCode, safeEqual, canSend, nextRecord, verify, otpEmail,
  CODE_DIGITS, TTL_MS, MAX_WRONG, RESEND_COOLDOWN_MS, MAX_PER_HOUR,
} from '../functions/src/otp.js';
import { normalizeEmail, buildUserDoc, ROLES } from '../functions/src/user.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const NOW = 1_700_000_000_000;
const MAIL = 'bome@example.com';
const PEP = 'bí-mật-máy-chủ';

/* ── 1 · sinh mã ── */
t('mã đúng 6 chữ số', /^\d{6}$/.test(makeCode()));
t('mã nhỏ vẫn đủ 6 chữ số, không mất số 0 đầu', makeCode(() => 7) === '000007');
const codes = new Set(Array.from({ length: 300 }, () => makeCode()));
t('300 mã sinh ra đủ tản mát', codes.size > 280);

/* ── 2 · băm: không bao giờ lưu mã trần ── */
const h = hashCode(MAIL, '123456', PEP);
t('bản băm không chứa mã', !h.includes('123456'));
t('cùng đầu vào cho cùng bản băm', h === hashCode(MAIL, '123456', PEP));
t('email khác thì băm khác — mã người này không dùng cho người kia',
  h !== hashCode('khac@example.com', '123456', PEP));
t('thiếu chuỗi bí mật máy chủ thì băm khác', h !== hashCode(MAIL, '123456', ''));
t('so chuỗi an toàn: giống nhau thì đúng', safeEqual(h, h));
t('so chuỗi an toàn: khác nhau thì sai', !safeEqual(h, hashCode(MAIL, '000000', PEP)));
t('so chuỗi an toàn: khác độ dài không vỡ', !safeEqual('abc', 'abcd'));

/* ── 3 · chặn spam gửi mã ── */
t('lần đầu luôn cho gửi', canSend(null, NOW).ok);
const justSent = { sentAt: NOW, sentTimes: [NOW] };
t('bấm gửi lại ngay lập tức thì chặn', !canSend(justSent, NOW + 1000).ok);
t('chặn vì quá nhanh và có nói còn phải chờ bao lâu',
  canSend(justSent, NOW + 1000).reason === 'quá nhanh' && canSend(justSent, NOW + 1000).retryAfterMs > 0);
t('qua 60 giây thì cho gửi lại', canSend(justSent, NOW + RESEND_COOLDOWN_MS + 1).ok);

const many = { sentAt: NOW - 120_000, sentTimes: Array.from({ length: MAX_PER_HOUR }, (_, i) => NOW - i * 120_000) };
t('quá 5 mã một giờ thì chặn', !canSend(many, NOW).ok && canSend(many, NOW).reason === 'quá nhiều');
t('sang giờ sau thì mở lại', canSend(many, NOW + 3600_001).ok);

/* ── 4 · vòng đời một mã ── */
const rec = nextRecord(null, { email: MAIL, code: '246810', pepper: PEP, now: NOW });
t('bản ghi KHÔNG chứa mã trần', !JSON.stringify(rec).includes('246810'));
t('mã sống đúng 10 phút', rec.expiresAt === NOW + TTL_MS);
t('mã mới chưa có lần nhập sai nào', rec.wrong === 0);

t('nhập đúng thì vào được', verify(rec, { email: MAIL, code: '246810', pepper: PEP, now: NOW }).ok);
t('nhập đúng xong thì huỷ mã — mỗi mã chỉ vào được MỘT lần',
  verify(rec, { email: MAIL, code: '246810', pepper: PEP, now: NOW }).burn === true);
t('có khoảng trắng thừa vẫn nhận', verify(rec, { email: MAIL, code: ' 246810 ', pepper: PEP, now: NOW }).ok);
t('nhập sai thì từ chối', !verify(rec, { email: MAIL, code: '111111', pepper: PEP, now: NOW }).ok);
t('sai một lần thì đếm lên một', verify(rec, { email: MAIL, code: '111111', pepper: PEP, now: NOW }).wrong === 1);

t('quá 10 phút là hết hạn',
  !verify(rec, { email: MAIL, code: '246810', pepper: PEP, now: NOW + TTL_MS + 1 }).ok);
t('hết hạn thì huỷ bản ghi',
  verify(rec, { email: MAIL, code: '246810', pepper: PEP, now: NOW + TTL_MS + 1 }).burn === true);

const almost = { ...rec, wrong: MAX_WRONG - 1 };
const last = verify(almost, { email: MAIL, code: '999999', pepper: PEP, now: NOW });
t('sai đến lần thứ 5 thì huỷ mã, bắt xin mã mới', last.burn === true && last.reason.includes('quá nhiều'));
t('đã hết lượt thì mã ĐÚNG cũng không vào được',
  !verify({ ...rec, wrong: MAX_WRONG }, { email: MAIL, code: '246810', pepper: PEP, now: NOW }).ok);

t('mã của email khác không dùng chéo được',
  !verify(rec, { email: 'khac@example.com', code: '246810', pepper: PEP, now: NOW }).ok);
t('chưa xin mã mà đi kiểm thì từ chối', !verify(null, { email: MAIL, code: '246810', now: NOW }).ok);

/* ── 5 · gửi lại thì mã CŨ phải chết ── */
const again = nextRecord(rec, { email: MAIL, code: '135791', pepper: PEP, now: NOW + 61_000 });
t('mã cũ hết tác dụng sau khi xin mã mới',
  !verify(again, { email: MAIL, code: '246810', pepper: PEP, now: NOW + 61_000 }).ok);
t('mã mới thì vào được', verify(again, { email: MAIL, code: '135791', pepper: PEP, now: NOW + 61_000 }).ok);
t('vẫn nhớ lịch sử gửi để chặn spam', again.sentTimes.length === 2);

/* ── 6 · nội dung email ── */
const mail = otpEmail('246810');
t('mã hiện ngay ở tiêu đề để đọc từ thông báo', mail.subject.startsWith('246810'));
t('thư nói rõ mã sống bao lâu', mail.text.includes('10 phút'));
t('thư dặn không đọc mã cho người khác', mail.text.includes('Đừng đọc mã này'));
t('thư KHÔNG chứa liên kết bấm — khỏi tập thói bấm bừa', !/https?:\/\//.test(mail.text));

/* ── 7 · email và hồ sơ người dùng ── */
t('chuẩn hoá email về chữ thường', normalizeEmail('  Bo.Me@Gmail.COM ') === 'bo.me@gmail.com');
t('email sai định dạng bị loại', normalizeEmail('sai@@x') === null && normalizeEmail('') === null);
t('email không có tên miền cấp cao bị loại', normalizeEmail('a@b') === null);

const U = buildUserDoc({ uid: 'u1', email: 'An.Nguyen@Mail.vn', now: () => NOW });
t('tài khoản mới mặc định là học sinh', U.role === 'learner');
t('chưa đặt tên thì lấy tạm phần trước @', U.displayName === 'an.nguyen');
t('tài khoản mới CHƯA coi là đã lập hồ sơ',
  U.profileComplete === false);
t('có tên thật rồi thì đánh dấu đã lập hồ sơ',
  buildUserDoc({ uid: 'u1', email: 'a@b.vn', displayName: 'Minh An' }).profileComplete === true);
t('email lưu dạng đã chuẩn hoá', U.email === 'an.nguyen@mail.vn');
t('vai trò lạ thì từ chối',
  (() => { try { buildUserDoc({ uid: 'u1', email: 'a@b.vn', role: 'sếp' }); return false; } catch { return true; } })());
t('chỉ có đúng ba vai trò', ROLES.join() === 'learner,teacher,admin');

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
