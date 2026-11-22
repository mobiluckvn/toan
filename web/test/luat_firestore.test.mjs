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
/* ⚠ ĐỌC CỔNG TỪ CHÍNH `firebase.gialap.json`, ĐỪNG GHIM SỐ.
   Bản cũ ghim 8080 trong khi `npm run gia-lap` bật bộ giả lập ở 8099 — nên cổng
   này TỰ BỎ QUA kể cả khi bộ giả lập đang chạy ngon lành, và đã bỏ qua như thế
   suốt. Đúng cái điều tệp này tự cảnh báo ở đầu: cổng im lặng là cổng không ai
   biết đã ngừng canh. Nay hỏi đúng tệp cấu hình mà lệnh bật dùng. */
const cauHinh = (() => {
  const d = new URL('../firebase.gialap.json', import.meta.url).pathname;
  try { return JSON.parse(readFileSync(d, 'utf8'))?.emulators?.firestore?.port; }
  catch { return null; }
})();
const HOST = process.env.FS_EMU || `127.0.0.1:${cauHinh || 8080}`;
const envTep = new URL('../.env.local', import.meta.url).pathname;
/* Mã dự án cũng phải khớp lệnh bật (`--project ky-su-nhi-thu-luat`): bộ giả lập
   chạy `--single_project_mode`, hỏi sai mã dự án là 404 mọi đường. */
const DU_AN = process.env.DU_AN
  || (cauHinh ? 'ky-su-nhi-thu-luat' : null)
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

/* ══ BỐ MẸ XÁC NHẬN ĐIỂM MÁY CHẤM — CHỈ BA TRƯỜNG (việc V5) ══
   Điểm bài viết do mô hình chấm nên nó là điểm TẠM. Bố mẹ đồng ý hoặc sửa, và đó
   là lệnh UPDATE. Chốt thật nằm ở `affectedKeys().hasOnly`, không ở lời dặn: không
   có nó thì một lệnh "xác nhận điểm" sửa được luôn `cham` và `viet` — tức sửa được
   LỜI CHẤM và BÀI BÉ VIẾT, hai thứ là bằng chứng để biết máy chấm đúng hay sai.
   Và máy chủ không tin máy con ở chỗ này: mã máy con thì ai cũng sửa được. */
const mucViet = (them = {}) => ({
  loai: V.s('viet'), khoa: V.s('ta3:VU1'), at: V.s('2026-10-09'),
  giaTri: V.m({
    viet: V.s('My school is big.'), diem: V.n(8), best: V.n(8),
    khen: V.s('Con dùng đúng từ school.'), soLoi: V.n(1),
    choBoMe: V.s('Con làm tốt.'), nguon: V.s('ai'),
    trangThai: V.s('tam'), at: V.s('2026-10-09'), ...them,
  }),
});
const DUONG_VIET = `hocBaTA/${BE_A}/muc/viet__ta3_VU1`;

m = await ghi(BE_A, DUONG_VIET, mucViet());
t('ghi mới mục bài viết (trangThai tam)', m === 200, `HTTP ${m}`);

/* Đồng ý: đổi đúng ba trường. */
m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.s(''), xacNhanLuc: V.s('2026-10-09T10:00:00Z'),
}));
t('bố mẹ XÁC NHẬN được — chỉ ba trường đổi', m === 200, `HTTP ${m}`);

/* Sửa điểm: vẫn đúng ba trường ấy. */
m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.n(7), xacNhanLuc: V.s('2026-10-09T10:01:00Z'),
}));
t('bố mẹ SỬA ĐIỂM được', m === 200, `HTTP ${m}`);

/* ⚠ Và đây là phép canh đáng giá nhất của cả khối: sửa LỜI CHẤM thì bị từ chối. */
m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.n(7), xacNhanLuc: V.s('2026-10-09T10:02:00Z'),
  khen: V.s('Lời khen bị sửa tay.'),
}));
t('sửa LỜI CHẤM thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.n(7), xacNhanLuc: V.s('2026-10-09T10:03:00Z'),
  viet: V.s('Bai cua be bi sua tay.'),
}));
t('sửa BÀI BÉ VIẾT thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

/* `diem` — điểm máy chấm — cũng là bằng chứng, không được đè. */
m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.n(7), xacNhanLuc: V.s('2026-10-09T10:04:00Z'),
  diem: V.n(10),
}));
t('đè ĐIỂM MÁY CHẤM thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

/* Trạng thái lạ thì từ chối — hai giá trị, không có giá trị thứ ba. */
m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('coGiaoDaXem'), diemNguoi: V.s(''), xacNhanLuc: V.s('2026-10-09T10:05:00Z'),
}));
t('trạng thái ngoài hai giá trị thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

/* ══ GHI LẠI MỘT MỤC ĐÃ CÓ — chỗ luật V5 vừa làm vỡ một lần ══
   `luuMucHocBa` dùng `setDoc(merge:true)`, nên ghi lần hai là lệnh UPDATE. Bé làm
   lại kỳ ôn tập, bỏ dở lần thứ hai, viết lại bài — tất cả đều ghi lại.
   ⚠ Phép canh này phải chạy SAU một lệnh ghi cùng đường dẫn, nếu không nó chỉ thử
   `create` và xanh vô nghĩa — đúng cách luật V5 đã lọt lần đầu. */
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/chuong__ta1_C1`, mucHopLe);
t('GHI LẠI mục đã có (loai chuong) vẫn được', m === 200, `HTTP ${m}`);
m = await ghi(BE_A, DUONG_VIET, mucViet({ diem: V.n(9), khen: V.s('Lời chấm MỚI.') }));
t('bé viết LẠI thì ghi đè cả lời chấm được (trangThai về tam)', m === 200, `HTTP ${m}`);
/* Nhưng không được VỪA xác nhận VỪA sửa lời chấm — đó mới là chốt của V5. */
m = await ghi(BE_A, DUONG_VIET, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.n(7), xacNhanLuc: V.s('2026-10-09T11:00:00Z'),
  khen: V.s('Vừa xác nhận vừa sửa lời chấm.'),
}));
t('vừa xác nhận vừa sửa lời chấm thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
/* Và không đổi được `loai` của một mục đã có. */
m = await ghi(BE_A, DUONG_VIET, { loai: V.s('chuong'), khoa: V.s('ta3:VU1'),
  at: V.s('2026-10-09'), giaTri: V.m({ dat: V.b(true) }) });
t('đổi `loai` của mục đã có thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

/* ⚠ MỤC `viet` CŨ (ghi trước V5) KHÔNG CÓ `trangThai` — và bé viết lại một bài cũ
   là ghi lại đúng mục ấy. Đòi trường luôn có thì mọi bài viết cũ hoá thành không
   ghi lại được, im lặng. */
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/viet__ta3_VU9`, {
  loai: V.s('viet'), khoa: V.s('ta3:VU9'), at: V.s('2026-09-01'),
  giaTri: V.m({ viet: V.s('Old essay.'), diem: V.n(7), nguon: V.s('ai') }),
});
t('mục bài viết CŨ (chưa có trangThai) vẫn ghi được', m === 200, `HTTP ${m}`);
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/viet__ta3_VU9`, {
  loai: V.s('viet'), khoa: V.s('ta3:VU9'), at: V.s('2026-10-09'),
  giaTri: V.m({ viet: V.s('Old essay, written again.'), diem: V.n(8), nguon: V.s('ai') }),
});
t('và GHI LẠI mục cũ ấy cũng được', m === 200, `HTTP ${m}`);

/* Và bé B vẫn không chạm được vào học bạ bé A. */
m = await ghi(BE_A, `hocBaTA/${BE_B}/muc/viet__ta3_VU1`, mucViet({
  trangThai: V.s('xacNhan'), diemNguoi: V.n(10), xacNhanLuc: V.s('2026-10-09T10:06:00Z'),
}), BE_A);
t('bé A KHÔNG xác nhận được điểm của bé B', m === 403, `HTTP ${m}`);

/* ── BẢN GHI BỎ DỞ (`loai: 'phien'`, vá 23-08-2026) ───────────────────────────
   `phien` là loại MỚI. Luật Firestore từ chối `loai` lạ TRONG IM LẶNG — máy con
   không thấy lỗi, bé không thấy gì, dữ liệu chỉ đơn giản là không có. Buổi đi thử
   bản chạy chỉ chứng minh được điều phủ định (console không có `permission-denied`),
   mà "không bị từ chối" khác hẳn "ghi được đúng nội dung".

   Gói dưới đây khớp ĐÚNG cái `roiManGiuaChung` trong `ManTiengAnh.jsx` gửi:
       luuMucHocBa(learnerId, 'phien', `${ct.ma}:${e.maPhien}`,
                   { giaTri: { microId, chang, soLuot, giay } })
   Chép sai một trường là cổng lại thử cái luật cho phép chứ không phải cái app
   gửi — đúng vết xe của `loai:'ontap'` ghi ở đầu khối này. */
const mucPhien = {
  loai: V.s('phien'), khoa: V.s('ta3:p-abc123'), at: V.s('2026-08-23'),
  giaTri: V.m({
    microId: V.s('DL:TA3.B00'), chang: V.s('tu'),
    soLuot: V.n(4), giay: V.n(37),
  }),
};
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/phien__ta3_p-abc123`, mucPhien);
t('chính chủ ghi được bản ghi BỎ DỞ (loai `phien`)', m === 200,
  `HTTP ${m} — 403 nghĩa là luật chưa cho \`phien\`, và bản ghi bỏ dở đang RƠI IM LẶNG`);

m = await ghi(BE_A, `hocBaTA/${BE_B}/muc/phien__ta3_p-abc123`, mucPhien, BE_A);
t('bé A KHÔNG ghi được bản ghi bỏ dở vào sổ bé B', m === 403, `HTTP ${m}`);

/* Hai lần bỏ dở CÙNG một bài phải nằm ở hai tài liệu — khoá mang mã phiên nên
   không đè nhau. Đây là điều kiện để đếm được "bỏ dở bài này mấy lần". */
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/phien__ta3_p-def456`, {
  ...mucPhien, khoa: V.s('ta3:p-def456'),
});
t('lần bỏ dở thứ hai cùng bài ghi được vào tài liệu RIÊNG', m === 200, `HTTP ${m}`);

/* Vòng khứ hồi: đọc lại và soi đúng bốn trường mà phép đo mệt mỏi cần. Ghi 200
   chưa chứng minh gì — bản cũ của `hocBaTA` cũng từng "ghi được" một hình dạng mà
   bên đọc không nhặt nổi. */
{
  const r = await fetch(`${goc}/hocBaTA/${BE_A}/muc/phien__ta3_p-abc123`, {
    headers: { Authorization: `Bearer ${token(BE_A)}` },
  });
  const d = r.ok ? await r.json() : null;
  const gt = d?.fields?.giaTri?.mapValue?.fields;
  t('đọc lại thấy loai `phien`', d?.fields?.loai?.stringValue === 'phien');
  t('đọc lại thấy microId — biết bỏ dở BÀI NÀO', gt?.microId?.stringValue === 'DL:TA3.B00');
  t('đọc lại thấy chang — biết bỏ dở Ở ĐÂU trong bài', gt?.chang?.stringValue === 'tu');
  t('đọc lại thấy soLuot', Number(gt?.soLuot?.integerValue ?? gt?.soLuot?.doubleValue) === 4);
  t('đọc lại thấy giay — chiều Thời gian cần đúng con số này',
    Number(gt?.giay?.integerValue ?? gt?.giay?.doubleValue) === 37);
}

/* ── KHUNG A-R-A: một lần can thiệp PHỤ ĐẠO (loai `phudao`, thêm 26-08) ──
   Gói dưới đây khớp ĐÚNG cái `xongPhuDao` trong `ManTiengAnh.jsx` gửi. Cùng lý do
   với khối `phien` ngay trên: cổng phải thử cái APP GỬI, không phải cái luật cho.

   ⚠ Khoá nhúng MỐC THỜI GIAN chứ không phải mã bài, vì một bài có thể kích hoạt
   phụ đạo nhiều lần ở những nút khác nhau — khoá theo bài thì lần sau đè lần
   trước, mất đúng thứ giao thức A-R-A cần đếm. */
const mucPhuDao = {
  loai: V.s('phudao'), khoa: V.s('ta5:DL:TA5.B08:1756000000000'), at: V.s('2026-08-26'),
  giaTri: V.m({
    microId: V.s('DL:TA5.B08'), maNutMac: V.s('sp_g5_u8_1'),
    nutGoc: V.s('sp_g5_u6_1'), lam: V.b(true), soCau: V.n(4), dung: V.n(3),
  }),
};
m = await ghi(BE_A, `hocBaTA/${BE_A}/muc/phudao__ta5_b08_1756000000000`, mucPhuDao);
t('chính chủ ghi được KHUNG A-R-A (loai `phudao`)', m === 200,
  `HTTP ${m} — 403 nghĩa là chưa deploy luật mới, và mỗi lần phụ đạo đang RƠI IM LẶNG`);

m = await ghi(BE_A, `hocBaTA/${BE_B}/muc/phudao__ta5_b08_1756000000000`, mucPhuDao, BE_A);
t('bé A KHÔNG ghi được khung A-R-A vào sổ bé B', m === 403, `HTTP ${m}`);

{
  const r = await fetch(`${goc}/hocBaTA/${BE_A}/muc/phudao__ta5_b08_1756000000000`, {
    headers: { Authorization: `Bearer ${token(BE_A)}` },
  });
  const d = r.ok ? await r.json() : null;
  const gt = d?.fields?.giaTri?.mapValue?.fields;
  /* Hai mã nút này là CẢ GIÁ TRỊ của bản ghi: `maNutMac` là chỗ lỗi lộ ra,
     `nutGoc` là chỗ lan truyền ngược chỉ ra. Thiếu một trong hai thì không đối
     chiếu được với chẩn đoán của giáo viên ở kịch bản KB8. */
  t('đọc lại thấy maNutMac — chỗ lỗi LỘ RA', gt?.maNutMac?.stringValue === 'sp_g5_u8_1');
  t('đọc lại thấy nutGoc — chỗ lan truyền ngược chỉ ra', gt?.nutGoc?.stringValue === 'sp_g5_u6_1');
}

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

console.log('\n── hàng đợi DUYỆT câu do mô hình soạn (việc V9) ──');
{
  /* Luật thứ bảy của một câu hỏi — "phương án nhiễu có thật là cái sai trẻ hay mắc
     hay chỉ là một chữ bừa" — KHÔNG kiểm được bằng code. Nên câu phải chờ người
     lớn, và luật phải cho bé GHI mà không cho bé ĐỌC: để bé đọc thì đây thành một
     kho câu chưa ai kiểm mà bé lấy ra làm được. */
  const mucCho = (them = {}) => ({
    learnerId: V.s(BE_A), maNut: V.s('v_g1_u10_mango'), nguon: V.s('ai'),
    trangThai: V.s('cho'), at: V.s('2026-10-09'),
    cau: V.m({ id: V.s('pd_ai_1'), text: V.s('Chọn từ đúng') }), ...them,
  });
  /* ⚠ MÃ TÀI LIỆU MỚI MỖI LẦN CHẠY. Bộ giả lập giữ dữ liệu giữa hai lần `npm run
     test:luat`, nên một mã cố định mang theo TRẠNG THÁI của lần trước: lần đầu cô
     giáo duyệt nó, lần sau bé không ghi lại được nữa — và phép canh đỏ vì rác cũ,
     không vì luật sai. Tự mình dính đúng chỗ ấy một lần.
     Chuỗi create → update(cho) → cô duyệt → bé bị chặn nằm TRỌN trong một lần
     chạy, nên nó vẫn soi được cả `create` lẫn `update` mà không cần kho bẩn. */
  const D = `choDuyetTA/BE_A__pd_ai_${Date.now()}`;

  let m2 = await ghi(BE_A, D, mucCho());
  t('bé GHI được câu chờ duyệt', m2 === 200, `HTTP ${m2}`);
  m2 = await doc(D, BE_A);
  t('nhưng bé KHÔNG ĐỌC được hàng đợi duyệt', m2 === 403, `HTTP ${m2}`);
  m2 = await doc(D, BE_B, 'teacher');
  t('cô giáo đọc được', m2 === 200, `HTTP ${m2}`);

  m2 = await ghi(BE_A, 'choDuyetTA/gia_tinh', mucCho({ nguon: V.s('tinh') }));
  t('câu KHÔNG phải của mô hình thì BỊ TỪ CHỐI', m2 === 403, `HTTP ${m2}`);
  m2 = await ghi(BE_A, 'choDuyetTA/gia_duyet', mucCho({ trangThai: V.s('duyet') }));
  t('bé tự đánh dấu ĐÃ DUYỆT thì BỊ TỪ CHỐI', m2 === 403, `HTTP ${m2}`);
  m2 = await ghi(BE_A, 'choDuyetTA/gia_be_khac', mucCho({ learnerId: V.s(BE_B) }));
  t('bé A không ghi được câu đứng tên bé B', m2 === 403, `HTTP ${m2}`);

  /* ⚠ GHI LẠI KHI CHƯA AI DUYỆT. Mã tài liệu tiền định, nên bé làm lại phụ đạo ở
     CÙNG nút là một lệnh UPDATE. Phép canh này phải chạy SAU một lệnh ghi cùng
     đường dẫn, nếu không nó chỉ thử `create` và xanh vô nghĩa. */
  m2 = await ghi(BE_A, D, mucCho({ cau: V.m({ id: V.s('pd_ai_1'), text: V.s('Câu MỚI của buổi sau') }) }));
  t('bé GHI LẠI được khi câu còn chờ duyệt', m2 === 200, `HTTP ${m2}`);

  /* Cô giáo duyệt — đổi trạng thái. Bé thì không. */
  m2 = await ghi(BE_B, D, mucCho({ trangThai: V.s('duyet') }), BE_B, 'teacher');
  t('cô giáo DUYỆT được', m2 === 200, `HTTP ${m2}`);
  m2 = await ghi(BE_A, D, mucCho({ trangThai: V.s('duyet') }));
  t('bé KHÔNG duyệt được câu của chính mình', m2 === 403, `HTTP ${m2}`);
  /* ⚠ Và ĐÃ DUYỆT RỒI thì bé cũng không ghi đè được — không thì bé ghi đè một câu
     cô vừa bỏ, rồi nó quay lại hàng đợi như mới. */
  m2 = await ghi(BE_A, D, mucCho());
  t('câu ĐÃ DUYỆT thì bé không ghi đè được', m2 === 403, `HTTP ${m2}`);
}

console.log('\n── chốt chặn chung ──');
m = await ghi(BE_A, `linhTinhTA/${BE_A}/x/y`, { a: V.s('b') });
t('collection chưa khai luật thì BỊ CHẶN', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, 'bangXepHang/global', { diem: V.n(99) });
t('máy con KHÔNG ghi được vào bảng xếp hạng', m === 403, `HTTP ${m}`);
m = await doc('bangXepHang/global', BE_A);
t('bé đăng nhập ĐỌC ĐƯỢC bảng xếp hạng', m === 200 || m === 404, `HTTP ${m}`);

/* ══════════════════════════════════════════════════════════════════════
   BỐN BẢNG QUẢN LÝ NGƯỠNG — R7, Bảng 3.20.

   Đây là chỗ nguyên tắc "giá trị máy học ra chỉ là ĐỀ XUẤT, chỉ chuyên gia phát
   hành được" thành hàng rào máy gác chứ không phải một dòng trong tài liệu. Soi
   bằng mắt không đủ: một luật viết đúng mà đặt sai thứ tự `allow` là mở toang.
   ══════════════════════════════════════════════════════════════════════ */
console.log('\n── bốn bảng quản lý ngưỡng (R7) ──');

const CG = 'chuyen_gia_uid';
const nguongHopLe = (gt = 0.85, phienBan = 2, phamVi = null) => ({
  ma: V.s('NG07'), giaTri: { doubleValue: gt },
  canDuoi: { doubleValue: 0.70 }, canTren: { doubleValue: 0.98 },
  phienBan: V.n(phienBan), nguon: V.s('chuyenGia'),
  ...(phamVi ? { phamVi: V.m({ loai: V.s(phamVi.loai), ...(phamVi.khoa != null ? { khoa: V.s(phamVi.khoa) } : {}) }) } : {}),
});

/* ── GHI NHIỀU TÀI LIỆU TRONG MỘT LẦN CAM KẾT ──
   Từ 22-11 (Bảng 4.7, điểm 3) mỗi dòng `nguong`/`nguong_lich_su` phải đi CÙNG lần tăng
   bộ đếm `nguong_phien_ban/hienHanh` — luật đọc `getAfter` của bộ đếm. Ghi lẻ từng
   tài liệu bằng PATCH thì luật thấy bộ đếm chưa đổi và từ chối, đúng như phải thế;
   nên phép thử chiều CHO phải cam kết cả lô bằng `:commit`, y như giao dịch thật. */
const tenDayDu = (duong) => `projects/${DU_AN}/databases/(default)/documents/${duong}`;
async function camKet(nhuAi, role, ds) {
  const r = await fetch(`${goc}:commit`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token(nhuAi, role)}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ writes: ds.map(([duong, fields]) => ({ update: { name: tenDayDu(duong), fields } })) }),
  });
  return r.status;
}
/* Số hiện tại của bộ đếm (0 khi chưa có). Bộ giả lập giữ dữ liệu giữa các lần chạy
   trong cùng một phiên bật, nên phải hỏi chứ không đoán. */
async function soDem() {
  const r = await fetch(`${goc}/nguong_phien_ban/hienHanh`, {
    headers: { Authorization: `Bearer ${token(CG, 'chuyengia')}` },
  });
  if (r.status !== 200) return 0;
  return Number((await r.json())?.fields?.so?.integerValue) || 0;
}
const dem = (so) => ['nguong_phien_ban/hienHanh', { so: V.n(so) }];

m = await doc('nguong/NG07', BE_A);
t('bé ĐỌC được bảng ngưỡng — máy con phải đọc mới chạy được',
  m === 200 || m === 404, `HTTP ${m}`);
let so = await soDem();
m = await camKet(CG, 'chuyengia', [dem(so + 1), ['nguong/NG07', nguongHopLe(0.85, so + 1)]]);
t('chuyên gia GHI được ngưỡng trong khoảng hợp lệ (kèm tăng bộ đếm)', m === 200, `HTTP ${m}`);
so = await soDem();
m = await ghi(CG, 'nguong/NG07', nguongHopLe(0.86, so), CG, 'chuyengia');
t('ghi ngưỡng mà KHÔNG tăng bộ đếm thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 2), ['nguong/NG07', nguongHopLe(0.86, so + 2)]]);
t('bộ đếm chỉ được tăng ĐÚNG MỘT — nhảy số thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1), ['nguong/NG07', nguongHopLe(0.86, so)]]);
t('dòng ngưỡng mang số KHÁC bộ đếm thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, 'nguong/NG07', nguongHopLe(0.9, so + 1));
t('bé KHÔNG ghi được ngưỡng', m === 403, `HTTP ${m}`);
m = await ghi(BE_A, 'nguong_phien_ban/hienHanh', { so: V.n(so + 1) });
t('bé KHÔNG tăng được bộ đếm', m === 403, `HTTP ${m}`);
m = await camKet('ad_uid', 'admin', [dem(so + 1), ['nguong/NG07', nguongHopLe(0.9, so + 1)]]);
t('ADMIN cũng KHÔNG ghi được — vai trò tách hẳn', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1), ['nguong/NG07', nguongHopLe(0.99, so + 1)]]);
t('giá trị NGOÀI khoảng hợp lệ thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1), ['nguong/NG07', nguongHopLe(0.50, so + 1)]]);
t('dưới cận dưới cũng BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1), ['nguong/NG99', { ma: V.s('NG99'), giaTri: { doubleValue: 1 } }]]);
t('thiếu canDuoi/canTren/phienBan thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);

/* ── PHẠM VI HẸP (Bảng 4.7, điểm 2) ── */
m = await camKet(CG, 'chuyengia', [dem(so + 1),
  ['nguong/NG07__khoiLop__3', nguongHopLe(0.80, so + 1, { loai: 'khoiLop', khoa: '3' })]]);
t('chuyên gia ghi được ngưỡng cho MỘT khối lớp', m === 200, `HTTP ${m}`);
so = await soDem();
m = await camKet(CG, 'chuyengia', [dem(so + 1),
  ['nguong/NG07__khoiLop__4', nguongHopLe(0.80, so + 1, { loai: 'khoiLop', khoa: '3' })]]);
t('mã tài liệu LỆCH phạm vi khai bên trong thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1),
  ['nguong/NG07__lop__3', nguongHopLe(0.80, so + 1, { loai: 'lop', khoa: '3' })]]);
t('nấc phạm vi KHÔNG có trên thang thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1),
  ['nguong/NG07', nguongHopLe(0.80, so + 1, { loai: 'khoiLop', khoa: '3' })]]);
t('dòng phạm vi hẹp KHÔNG được nằm ở mã tài liệu toàn hệ', m === 403, `HTTP ${m}`);

/* ⚠ MÃ TÀI LIỆU PHẢI KHÁC NHAU MỖI LẦN CHẠY. `nguong_lich_su` là bảng CHỈ-THÊM, nên
   một mã ghim cứng làm lần chạy thứ hai trên cùng bộ giả lập tự đỏ: phép "chuyên gia
   THÊM được dòng lịch sử" biến thành phép "sửa lại dòng cũ", và luật từ chối — đúng
   như luật phải làm. Cổng đỏ vì chính thứ nó đang canh hoạt động đúng là một cổng
   dẫn người sửa đi sai hướng, nên mỗi lần chạy dùng một hậu tố riêng. */
const LAN = `${Date.now()}_${Math.floor(Math.random() * 1e6)}`;

const lichSuHopLe = (nguoi = CG, lyDo = 'tỷ lệ công nhận sớm 18%', phienBan = 2) => ({
  ma: V.s('NG07'), giaTriMoi: { doubleValue: 0.88 }, phienBan: V.n(phienBan),
  nguoiSua: V.s(nguoi), thoiDiem: V.s('2026-10-10T00:00:00Z'), lyDo: V.s(lyDo),
});

so = await soDem();
m = await camKet(CG, 'chuyengia', [dem(so + 1), [`nguong_lich_su/ls1_${LAN}`, lichSuHopLe(CG, undefined, so + 1)]]);
t('chuyên gia THÊM được dòng lịch sử (cùng lần tăng bộ đếm)', m === 200, `HTTP ${m}`);
so = await soDem();
m = await camKet(CG, 'chuyengia', [dem(so + 1), [`nguong_lich_su/ls1_${LAN}`, lichSuHopLe(CG, 'sửa lại', so + 1)]]);
t('nhưng SỬA lại dòng ấy thì BỊ TỪ CHỐI — lịch sử chỉ thêm', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1), [`nguong_lich_su/ls2_${LAN}`, lichSuHopLe(CG, '', so + 1)]]);
t('thiếu LÝ DO thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await camKet(CG, 'chuyengia', [dem(so + 1), [`nguong_lich_su/ls3_${LAN}`, lichSuHopLe(BE_A, undefined, so + 1)]]);
t('khai nguoiSua là người KHÁC thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await ghi(CG, `nguong_lich_su/ls4_${LAN}`, lichSuHopLe(CG, undefined, so), CG, 'chuyengia');
t('dòng lịch sử KHÔNG đi cùng một lần phát hành thì BỊ TỪ CHỐI', m === 403, `HTTP ${m}`);
m = await doc(`nguong_lich_su/ls1_${LAN}`, BE_A);
t('bé KHÔNG đọc được lịch sử ngưỡng', m === 403, `HTTP ${m}`);

m = await ghi(CG, `nguong_de_xuat/dx1_${LAN}`,
              { ma: V.s('NG07'), giaTriDeXuat: { doubleValue: 0.88 }, trangThai: V.s('cho') },
              CG, 'chuyengia');
t('KHÔNG AI tạo được đề xuất từ máy con — chỉ hàm nền', m === 403, `HTTP ${m}`);
m = await doc('thong_ke_nguong/tk1', CG, 'chuyengia');
t('chuyên gia đọc được thống kê', m === 200 || m === 404, `HTTP ${m}`);
m = await ghi(CG, 'thong_ke_nguong/tk1', { ma: V.s('NG07') }, CG, 'chuyengia');
t('nhưng KHÔNG ghi được thống kê — chỉ hàm nền', m === 403, `HTTP ${m}`);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
