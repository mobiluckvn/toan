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

/* Cổng mạng của bộ giả lập. 8080 là cổng quen của rất nhiều thứ khác, nên cho phép
   đổi bằng biến môi trường thay vì ghim cứng:
       FS_EMU=127.0.0.1:8099 node test/luat_firestore.test.mjs
   `npm run gia-lap` bật bộ giả lập ở đúng cổng ấy. */
const HOST = process.env.FS_EMU || '127.0.0.1:8080';
const envTep = new URL('../.env.local', import.meta.url).pathname;
const DU_AN = process.env.DU_AN
  || (existsSync(envTep)
    ? (readFileSync(envTep, 'utf8').match(/VITE_FB_PROJECT_ID=(.+)/) || [])[1]?.trim()
    : null)
  || 'demo-test';
const goc = `http://${HOST}/v1/projects/${DU_AN}/databases/(default)/documents`;

/* ⚠ "Có ai trả lời ở cổng 8080" KHÔNG CÓ NGHĨA là bộ giả lập Firestore.
   Cổng 8080 là cổng quen của nhiều thứ khác — 18-08 nó bị một tiến trình node khác
   chiếm, trả 200 cho `/` nhưng 404 cho mọi đường Firestore, và cổng này đỏ 24 phép
   vì một lý do KHÔNG PHẢI lỗi. Nhận diện đúng thì phải hỏi CHÍNH đường mà phép thử
   sẽ dùng: đọc một tài liệu bất kỳ. Bộ giả lập trả 200 (có) hoặc 404 kèm thân JSON
   có `error.status` — thứ khác thì trả 404 trần hoặc HTML. */
const song = await fetch(`${goc}/__song__/__song__`, { signal: AbortSignal.timeout(1500) })
  .then(async (r) => {
    if (r.status === 200) return true;
    const t = await r.text().catch(() => '');
    try { return !!JSON.parse(t)?.error?.status; } catch { return false; }
  })
  .catch(() => false);
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
  /* Học bạ bọc số liệu trong một trường con `giaTri` — REST của Firestore đòi khai
     lồng đúng hình dạng này, không nhận object thường. */
  m: (o) => ({ mapValue: { fields: o } }),
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
/* ⚠ Gói này phải là gói MÀN HÌNH THẬT GỬI, không phải gói cổng tự nghĩ ra.
   Bản cũ tự viết `loai:'chuong'` trong khi `ManTiengAnh.jsx` gửi `'ontap'` — cổng
   thử đúng cái luật cho phép, chứ không phải cái app gửi đi, nên nó xanh suốt
   trong lúc mọi kỳ ôn tập Tiếng Anh bị máy chủ từ chối trong im lặng.
   Nay hình dạng dưới đây khớp `luuMucHocBa(learnerId, 'chuong', k, {giaTri})`, và
   `hocba_khop_luat.test.mjs` canh cho hai bên không lệch lại. */
const mucHopLe = {
  loai: V.s('chuong'), khoa: V.s('ta1:C1'), at: V.s('2026-08-12'),
  giaTri: V.m({ dat: V.b(true), best: V.n(9), tong: V.n(10), at: V.s('2026-08-12') }),
};
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/chuong__ta1_C1`, mucHopLe);
t('chính chủ ghi được mục học bạ', m === 200, `HTTP ${m}`);
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/loai_la`, { loai: V.s('dau'), khoa: V.s('x') });
t('loại ngoài danh sách thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, `hocBaTA/${BE_B}/muc/chuong__ta1_C1`, mucHopLe, BE_A);
t('bé A KHÔNG ghi được học bạ bé B', m === 403, `HTTP ${m}`);

/* ── VÒNG KHỨ HỒI: ghi lên rồi ĐỌC LẠI ──
   Ghi được 200 chưa chứng minh gì cả — bản cũ cũng "ghi được" một hình dạng mà
   `docHocBa` không nhặt nổi, nên máy chủ có tài liệu mà bé vẫn mất huy hiệu. Đọc
   lại và soi đúng cái thẻ huy hiệu cần (`best`, `tong`) mới là bằng chứng. */
{
  const r = await fetch(`${goc}/hocBaTA/${BE_A}/muc/chuong__ta1_C1`, {
    headers: { Authorization: `Bearer ${token(BE_A)}` },
  });
  const d = r.ok ? await r.json() : null;
  const gt = d?.fields?.giaTri?.mapValue?.fields;
  t('đọc lại thấy đúng loai mà bên đọc lọc', d?.fields?.loai?.stringValue === 'chuong');
  t('đọc lại thấy giaTri có best — thẻ huy hiệu dùng đúng trường này',
    gt?.best?.integerValue === '9', JSON.stringify(gt || null));
}

console.log('\n── hocBa (Toán) · SỔ GIỜ HỌC ──');
/* Thêm 17-08-2026 cùng lúc với `loai='gio'`.
   ⚠ Gói dưới đây phải khớp cái `congGioTrongNgay()` trong `mon/toan/lib/duLieu.js`
   THẬT SỰ gửi, không phải gói cổng tự nghĩ ra — đó đúng bài học đã ghi ở khối
   `hocBaTA` ngay trên: cổng thử đúng cái luật cho phép chứ không phải cái app gửi
   đi thì nó xanh suốt trong lúc máy chủ từ chối trong im lặng. */
const gioHopLe = {
  loai: V.s('gio'), ngay: V.s('2026-08-17'),
  giay: V.n(900), giayXem: V.n(300), giayLam: V.n(600),
  soLuot: V.n(1), baiCuoi: V.s('DL:KSN5Q1.B1.M1'), at: V.n(1755400000000),
};
m = await ghi(BE_A, `hocBa/${BE_A}/muc/gio_2026_08_17`, gioHopLe);
t('chính chủ ghi được sổ giờ học (loai=gio)', m === 200, `HTTP ${m}`);
m = await ghi(BE_A, `hocBa/${BE_A}/muc/gio_la`, { loai: V.s('gio_gi_do'), giay: V.n(1) });
t('loại ngoài danh sách vẫn BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, `hocBa/${BE_B}/muc/gio_2026_08_17`, gioHopLe, BE_A);
t('bé A KHÔNG ghi được sổ giờ của bé B', m === 403, `HTTP ${m}`);
m = await doc(`hocBa/${BE_B}/muc/gio_2026_08_17`, BE_A);
t('bé A KHÔNG đọc được sổ giờ của bé B', m === 403, `HTTP ${m}`);

/* VÒNG KHỨ HỒI — ghi 200 chưa chứng minh gì. Sổ bố mẹ và bảng cô giáo đọc đúng ba
   trường `giay`·`giayXem`·`giayLam`; thiếu một là số phút hiện ra sai mà không kêu. */
{
  const r = await fetch(`${goc}/hocBa/${BE_A}/muc/gio_2026_08_17`, {
    headers: { Authorization: `Bearer ${token(BE_A)}` },
  });
  const d = r.ok ? await r.json() : null;
  const f = d?.fields;
  t('đọc lại đủ ba con số giây mà sổ và bảng cô giáo cần',
    f?.giay?.integerValue === '900' && f?.giayXem?.integerValue === '300'
      && f?.giayLam?.integerValue === '600', JSON.stringify(f || null));
}

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
