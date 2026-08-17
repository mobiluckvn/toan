/* ═══════════ LUẬT FIRESTORE — CHẠY THẬT TRÊN MÁY GIẢ LẬP ═══════════
 *
 * chạy: npm run test:luat        (tự bật máy giả lập rồi tắt)
 *
 * ── VÌ SAO CÓ TỆP NÀY, VÀ VÌ SAO NÓ RA ĐỜI MUỘN ──
 *
 * Kho có gần sáu mươi cổng, và KHÔNG cổng nào canh `firestore.rules`. Đó lại đúng
 * tệp có kiểu hỏng tệ nhất trong cả kho: **từ chối trong im lặng**. `loai` không nằm
 * trong danh sách cho phép thì Firestore vứt lượt ghi đi mà không báo gì; sổ tại máy
 * con vẫn đúng, màn hình vẫn bình thường, nên không ai thấy — cho tới lúc bố mẹ mở
 * sổ ở máy khác và thấy trống.
 *
 * Chuyện ấy đã xảy ra thật một lần (11-08-2026, ba loại `chuong`·`chuDe`·`dau` mới
 * thêm). Ngày 17-08 thêm `loai='gio'` cho sổ giờ học là đúng ca ấy lần thứ hai.
 *
 * ── PHÉP NÀY LÀM GÌ ──
 *
 * Không đọc tệp luật bằng mắt, mà DỰNG MÁY GIẢ LẬP rồi thử ghi thật: ghi được thì
 * xanh, bị từ chối thì đỏ. Và quan trọng ngang thế — thử cả chiều NGƯỢC: ghi thứ
 * đáng lẽ phải bị chặn, mà chặn không nổi thì cũng đỏ. Một danh sách cho phép chỉ
 * có nghĩa khi nó THẬT SỰ từ chối thứ ngoài danh sách.
 */
import { readFileSync } from 'node:fs';
import {
  initializeTestEnvironment, assertSucceeds, assertFails,
} from '@firebase/rules-unit-testing';
/* Nhập từ '@firebase/firestore' chứ KHÔNG từ 'firebase/firestore': bộ thử luật trả
   về thể hiện của gói @firebase/firestore, mà hai gói là hai bản sao khác nhau —
   trộn vào là "Expected first argument to collection() to be a CollectionReference". */
import { doc, setDoc, getDoc } from 'firebase/firestore';

let pass = 0, fail = 0;
const t = async (n, p) => {
  try { await p; pass++; } catch (e) { fail++; console.log('  ✗', n, '—', e.message); }
};

const env = await initializeTestEnvironment({
  projectId: 'ky-su-nhi-thu-luat',
  firestore: { rules: readFileSync('firestore.rules', 'utf8'), host: '127.0.0.1', port: 8099 },
});
await env.clearFirestore();

const be = env.authenticatedContext('be1').firestore();
const beKhac = env.authenticatedContext('be2').firestore();
const co = env.authenticatedContext('co1', { role: 'teacher' }).firestore();
const la = env.unauthenticatedContext().firestore();

const muc = (db, uid, id) => doc(db, `hocBa/${uid}/muc/${id}`);

/* ── SỔ GIỜ HỌC: cái vừa thêm ── */
await t('bé ghi được sổ giờ của chính mình (loai=gio)',
  assertSucceeds(setDoc(muc(be, 'be1', 'gio_2026_08_17'),
    { loai: 'gio', ngay: '2026-08-17', giay: 900, giayXem: 300, giayLam: 600 })));

await t('ba loại cũ vẫn ghi được — không làm hỏng cái đang chạy',
  Promise.all([
    assertSucceeds(setDoc(muc(be, 'be1', 'chuong_c1'), { loai: 'chuong', giaTri: {} })),
    assertSucceeds(setDoc(muc(be, 'be1', 'chuDe_PT_I_1_1'), { loai: 'chuDe', giaTri: {} })),
    assertSucceeds(setDoc(muc(be, 'be1', 'dau_V01'), { loai: 'dau', giaTri: {} })),
  ]));

/* ── ĐẢO CHIỀU: danh sách cho phép chỉ có nghĩa khi nó TỪ CHỐI được ──
   Không có ba phép dưới đây thì "ghi được" ở trên chẳng chứng minh gì: một luật
   `allow write: if true` cũng cho ra đúng kết quả ấy. */
await t('loai LẠ bị chặn (nếu không, danh sách cho phép là vô nghĩa)',
  assertFails(setDoc(muc(be, 'be1', 'gio_x'), { loai: 'linh_tinh', giay: 1 })));

await t('thiếu hẳn trường loai cũng bị chặn',
  assertFails(setDoc(muc(be, 'be1', 'khong_loai'), { giay: 1 })));

await t('bé KHÔNG ghi được vào sổ của bé khác',
  assertFails(setDoc(muc(beKhac, 'be1', 'gio_2026_08_17'), { loai: 'gio', giay: 1 })));

await t('người chưa đăng nhập không ghi được',
  assertFails(setDoc(muc(la, 'be1', 'gio_2026_08_17'), { loai: 'gio', giay: 1 })));

/* ── ĐỌC: cô giáo xem được, bé khác thì không ── */
await t('cô giáo đọc được sổ giờ của bé',
  assertSucceeds(getDoc(muc(co, 'be1', 'gio_2026_08_17'))));
await t('bé đọc được sổ của chính mình',
  assertSucceeds(getDoc(muc(be, 'be1', 'gio_2026_08_17'))));
await t('bé KHÔNG đọc được sổ của bé khác',
  assertFails(getDoc(muc(beKhac, 'be1', 'gio_2026_08_17'))));

/* ── Số liệu ghi vào có còn nguyên không ── */
await env.withSecurityRulesDisabled(async (ctx) => {
  const d = await getDoc(doc(ctx.firestore(), 'hocBa/be1/muc/gio_2026_08_17'));
  const ok = d.exists() && d.data().giay === 900 && d.data().giayXem === 300;
  await t('sổ giờ ghi lên rồi đọc lại vẫn đủ ba con số', ok ? Promise.resolve() : Promise.reject(new Error('số liệu không khớp')));
});

await env.cleanup();
console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
