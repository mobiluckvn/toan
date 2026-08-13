/**
 * LUẬT FIRESTORE — thử THẬT trên bộ giả lập, cả chiều CHO lẫn chiều TỪ CHỐI.
 * chạy:  (cửa sổ 1)  PATH="/usr/local/opt/openjdk/bin:$PATH" npx firebase emulators:start
 *        (cửa sổ 2)  node test/luat_firestore.test.mjs
 *
 * ── VÌ SAO PHẢI CHẠY THẬT ──
 * `tienganh_may_chu.test.mjs` chỉ ĐỌC tệp luật bằng regex: nó bắt được "quên viết
 * luật", nhưng không bắt được "luật viết rồi mà sai". Chỉ máy chủ mới biên dịch và
 * thi hành được bộ luật, nên phần này phải chạy trên bộ giả lập.
 *
 * Và quan trọng hơn: nó thử được chiều BỊ TỪ CHỐI — bé A ghi vào sổ bé B, thiếu
 * trường, sai kiểu, collection chưa khai luật. Đó là những chỗ mà cổng đọc-tệp và
 * cả việc bấm tay qua giao diện đều không với tới, vì giao diện chỉ đi đường đúng.
 *
 * ── KHÔNG CÓ BỘ GIẢ LẬP THÌ BỎ QUA ÊM ──
 * `npm test` phải chạy được trên máy không có Java. Nhưng bỏ qua thì NÓI RA, chứ
 * không lặng lẽ xanh — cổng im lặng là cổng không ai biết đã ngừng canh.
 *
 * Bộ giả lập nhận JWT KHÔNG KÝ (`alg: none`), nhờ vậy giả được `uid` và `role` tuỳ
 * ý mà không cần đăng nhập thật.
 */
import { readFileSync, existsSync } from 'node:fs';

const HOST = '127.0.0.1:8080';
const envTep = new URL('../.env.local', import.meta.url).pathname;
const DU_AN = process.env.DU_AN
  || (existsSync(envTep)
    ? (readFileSync(envTep, 'utf8').match(/VITE_FB_PROJECT_ID=(.+)/) || [])[1]?.trim()
    : null)
  || 'demo-test';
const goc = `http://${HOST}/v1/projects/${DU_AN}/databases/(default)/documents`;

const song = await fetch(`http://${HOST}/`, { signal: AbortSignal.timeout(1500) })
  .then(() => true).catch(() => false);
if (!song) {
  console.log('   ⏸ BỘ GIẢ LẬP KHÔNG CHẠY — bỏ qua phần thử luật thật.');
  console.log('      Bật bằng: PATH="/usr/local/opt/openjdk/bin:$PATH" \\');
  console.log('                npx firebase emulators:start --only auth,firestore,functions');
  console.log('\n0 PASS · 0 FAIL');
  process.exit(0);
}

const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
const token = (uid, role) => [
  b64({ alg: 'none', typ: 'JWT' }),
  b64({
    iss: `https://securetoken.google.com/${DU_AN}`, aud: DU_AN, sub: uid, user_id: uid,
    iat: 1, exp: 9999999999, auth_time: 1, email_verified: true,
    firebase: { identities: {}, sign_in_provider: 'custom' },
    ...(role ? { role } : {}),
  }),
  '',
].join('.');

const V = {
  s: (v) => ({ stringValue: String(v) }),
  b: (v) => ({ booleanValue: !!v }),
  n: (v) => ({ integerValue: String(v) }),
};

async function ghi(uid, duong, fields, nhuAi = uid, role) {
  const r = await fetch(`${goc}/${duong}`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token(nhuAi, role)}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ fields }),
  });
  return r.status;
}
async function doc(duong, nhuAi, role) {
  const r = await fetch(`${goc}/${duong}`, {
    headers: { Authorization: `Bearer ${token(nhuAi, role)}` },
  });
  return r.status;
}

let pass = 0, fail = 0;
const t = (ten, dieu, them = '') => {
  if (dieu) { pass += 1; console.log(`  ✓ ${ten}`); }
  else { fail += 1; console.log(`  ✗ ${ten}${them ? ` — ${them}` : ''}`); }
};

const BE_A = 'be_a_uid', BE_B = 'be_b_uid';
const baiHopLe = {
  microId: V.s('DL:TA1.B04'), pass: V.b(true), score: V.n(5), total: V.n(5),
  bac: V.n(4), attempts: V.n(1), at: V.s('2026-08-12T05:00:00Z'),
};

console.log('\n── progressTA ──');
let m = await ghi(BE_A, `progressTA/${BE_A}/micros/DL_TA1_B04`, baiHopLe);
t('chính chủ GHI ĐƯỢC bài của mình', m === 200, `HTTP ${m}`);

m = await ghi(BE_A, `progressTA/${BE_B}/micros/DL_TA1_B04`, baiHopLe, BE_A);
t('bé A KHÔNG ghi được vào sổ bé B', m === 403, `HTTP ${m}`);

m = await ghi(BE_A, `progressTA/${BE_A}/micros/thieu_truong`,
  { microId: V.s('DL:TA1.B05'), pass: V.b(true) });          // thiếu `score`
t('thiếu trường luật đòi thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

m = await ghi(BE_A, `progressTA/${BE_A}/micros/sai_kieu`,
  { microId: V.s('DL:TA1.B06'), pass: V.s('true'), score: V.n(3) });  // pass là chuỗi
t('sai kiểu dữ liệu thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

m = await doc(`progressTA/${BE_A}/micros/DL_TA1_B04`, BE_A);
t('chính chủ ĐỌC ĐƯỢC sổ của mình', m === 200, `HTTP ${m}`);
m = await doc(`progressTA/${BE_A}/micros/DL_TA1_B04`, BE_B);
t('bé B KHÔNG đọc được sổ bé A', m === 403, `HTTP ${m}`);
m = await doc(`progressTA/${BE_A}/micros/DL_TA1_B04`, 'co_giao', 'teacher');
t('cô giáo ĐỌC ĐƯỢC sổ của học sinh', m === 200, `HTTP ${m}`);

console.log('\n── hocBaTA ──');
const mucHopLe = { loai: V.s('chuong'), khoa: V.s('ta1:C1'), at: V.s('2026-08-12') };
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/chuong__ta1_C1`, mucHopLe);
t('chính chủ ghi được mục học bạ', m === 200, `HTTP ${m}`);
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/loai_la`, { loai: V.s('dau'), khoa: V.s('x') });
t('loại ngoài danh sách thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, `hocBaTA/${BE_B}/muc/chuong__ta1_C1`, mucHopLe, BE_A);
t('bé A KHÔNG ghi được học bạ bé B', m === 403, `HTTP ${m}`);

console.log('\n── bằng chứng học tập không xoá được ──');
{
  const r = await fetch(`${goc}/progressTA/${BE_A}/micros/DL_TA1_B04`, {
    method: 'DELETE', headers: { Authorization: `Bearer ${token(BE_A)}` },
  });
  /* Chính chủ cũng KHÔNG xoá được bài đã học. Ban đầu là ngẫu nhiên (lệnh xoá không
     mang `request.resource.data` nên hai điều kiện kiểu dữ liệu tự sai), nay ghi
     thành chủ ý — xem chú thích trong firestore.rules. Có phép kiểm ở đây thì ai
     nới luật sau này sẽ thấy mình đang đổi một quyết định, không phải sửa lỗi. */
  t('chính chủ KHÔNG xoá được bài đã học', r.status === 403, `HTTP ${r.status}`);
}

console.log('\n── phòng luyện nói ──');
{
  /* Đây là TIẾNG NÓI của trẻ con — thứ riêng tư nhất trong cả kho. Máy chủ không
     lưu gì (bác chốt), nên chính máy con đẩy buổi lên đây; luật phải cho chính chủ
     GHI, mà chỉ chính chủ thôi. Cô giáo KHÔNG đọc được: `canRead` cho cô đọc kết
     quả học là đúng, nhưng một buổi trò chuyện thì khác hẳn. */
  const buoi = { soLuot: V.n(2), luot: { arrayValue: { values: [] } } };
  m = await ghi(BE_A, `phongNoiTA/${BE_A}/buoi/b1`, buoi);
  t('chính chủ ghi được buổi luyện nói', m === 200, `HTTP ${m}`);
  m = await ghi(BE_A, `phongNoiTA/${BE_B}/buoi/b1`, buoi, BE_A);
  t('bé A KHÔNG ghi được vào phòng nói của bé B', m === 403, `HTTP ${m}`);
  m = await doc(`phongNoiTA/${BE_B}/buoi/b1`, BE_A);
  t('bé A KHÔNG đọc được buổi nói chuyện của bé B', m === 403, `HTTP ${m}`);
  m = await ghi(BE_A, `phongNoiTA/${BE_A}/buoi/sai`, {
    soLuot: V.s('nhieu'), luot: { arrayValue: { values: [] } },
  });
  t('sai kiểu dữ liệu thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
}

console.log('\n── chốt chặn chung ──');
m = await ghi(BE_A, `linhTinhTA/${BE_A}/x/y`, { a: V.s('b') });
t('collection chưa khai luật thì BỊ CHẶN', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, 'bangXepHang/global', { diem: V.n(99) });
t('máy con KHÔNG ghi được vào bảng xếp hạng', m === 403, `HTTP ${m}`);
m = await doc('bangXepHang/global', BE_A);
t('bé đăng nhập ĐỌC ĐƯỢC bảng xếp hạng', m === 200 || m === 404, `HTTP ${m}`);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
