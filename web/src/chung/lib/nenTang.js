/**
 * NỀN TẢNG FIREBASE — MỘT thể hiện duy nhất cho cả app.
 *
 * Chỉ nối dây, không mang logic của môn nào. Hai môn cùng dùng `db`/`auth`/`fns` vì
 * chúng cùng một dự án Firebase và cùng MỘT tài khoản đăng nhập — đó là thứ duy nhất
 * hai môn chia nhau. Dữ liệu học thì mỗi môn một bộ collection riêng, xem
 * `mon/<môn>/lib/duLieu.js`.
 *
 * QUAN TRỌNG: bật persistentLocalCache — trẻ học trên máy tính bảng, mạng chập chờn.
 * Thiếu dòng này là mất bài giữa chừng, và trẻ mất bài một lần là nản luôn.
 */
import { initializeApp } from 'firebase/app';
import {
  initializeFirestore, persistentLocalCache, persistentMultipleTabManager,
  connectFirestoreEmulator,
} from 'firebase/firestore';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions';

/** Điền từ Firebase Console → Project settings. Đặt trong .env.local, không commit. */
const cfg = {
  apiKey: import.meta.env?.VITE_FB_API_KEY,
  authDomain: import.meta.env?.VITE_FB_AUTH_DOMAIN,
  projectId: import.meta.env?.VITE_FB_PROJECT_ID,
  storageBucket: import.meta.env?.VITE_FB_STORAGE_BUCKET,
  messagingSenderId: import.meta.env?.VITE_FB_SENDER_ID,
  appId: import.meta.env?.VITE_FB_APP_ID,
};

export const hasFirebase = !!cfg.projectId;

/**
 * BỘ GIẢ LẬP — bật bằng `VITE_FB_EMULATOR=1`, mặc định TẮT.
 *
 * Vì sao phải có: `.env.local` trỏ vào dự án THẬT, nên `npm run dev` xưa nay nói
 * chuyện thẳng với Firebase thật. Đi thử màn đăng nhập là gửi mail thật, lập tài
 * khoản thật, ghi vào sổ học của con thật. Không ai muốn thử một nút bấm mà phải
 * cân nhắc chuyện đó, nên cuối cùng màn đăng nhập chẳng bao giờ được đi thử.
 *
 * Bật cờ thì cả ba đường (đăng nhập · cơ sở dữ liệu · hàm máy chủ) quay về máy mình.
 * Mã OTP không cần hộp thư: chưa đặt SMTP thì `functions/index.js` in thẳng mã ra
 * log của bộ giả lập.
 *
 *   cd web && firebase emulators:start --only auth,firestore,functions
 *   cd web && VITE_FB_EMULATOR=1 npm run dev
 *
 * Cờ chỉ đọc lúc dựng bản dev; bản `npm run build` để deploy không mang nó theo.
 */
/* Buộc kèm `DEV`: Vite thay `import.meta.env.DEV` bằng `false` lúc dựng bản thật, nên
   cả khối nối giả lập bị cắt khỏi bản đưa lên mạng — không phải tin vào việc người
   dựng nhớ tắt cờ. Dựng nhầm với cờ bật thì app thật sẽ đi tìm 127.0.0.1 và chết câm. */
export const dungGiaLap = !!import.meta.env?.DEV
  && import.meta.env?.VITE_FB_EMULATOR === '1';

let app = null, db = null, auth = null, fns = null;
if (hasFirebase) {
  app = initializeApp(cfg);
  db = initializeFirestore(app, {
    /* Bộ nhớ đệm bền ĐỤNG bộ giả lập: nó giữ lại dữ liệu của lần chạy trước trong
       IndexedDB, nên tắt giả lập đi rồi mở lại là thấy dữ liệu ma. Chạy giả lập thì
       dùng bộ nhớ tạm. */
    ...(dungGiaLap ? {} : {
      localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }),
    }),
  });
  auth = getAuth(app);
  fns = getFunctions(app, 'asia-southeast1');

  if (dungGiaLap) {
    /* Sửa một tệp lúc đang chạy thì Vite nạp lại module này, và nối lần thứ hai vào
       cùng một `auth` là Firebase ném `auth/emulator-config-failed`. Không hỏng gì —
       đường đã nối từ lần đầu — nhưng nó rải lỗi đỏ ra console, đúng chỗ mình đang
       cần console sạch để soi lỗi thật. */
    try {
      connectAuthEmulator(auth, 'http://127.0.0.1:9099', { disableWarnings: true });
      connectFirestoreEmulator(db, '127.0.0.1', 8080);
      connectFunctionsEmulator(fns, '127.0.0.1', 5001);
      console.info('[Kỹ Sư Nhí] Đang chạy trên BỘ GIẢ LẬP — không đụng dữ liệu thật.');
    } catch { /* đã nối rồi (nạp lại nóng) — bỏ qua */ }
  }
}
export { db, auth, fns };
