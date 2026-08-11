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
} from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { getFunctions } from 'firebase/functions';

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

let app = null, db = null, auth = null, fns = null;
if (hasFirebase) {
  app = initializeApp(cfg);
  db = initializeFirestore(app, {
    localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }),
  });
  auth = getAuth(app);
  fns = getFunctions(app, 'asia-southeast1');
}
export { db, auth, fns };
