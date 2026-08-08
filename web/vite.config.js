import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { bamNoiDung } from './tools/noidung_version.mjs';

/**
 * DẤU PHIÊN BẢN NỘI DUNG.
 *
 * Bài học và hình được gắn `max-age=604800, immutable` (xem firebase.json) mà tên
 * tệp thì không đổi khi sửa nội dung. Máy nào đã mở trang rồi sẽ giữ bản cũ tới
 * BẢY NGÀY, không thèm hỏi lại máy chủ — sửa xong đẩy lên mà con vẫn học bài cũ.
 *
 * Băm toàn bộ JSON trong public/content thành một mã ngắn, dán vào mọi đường dẫn
 * nội dung dưới dạng `?v=…`. Nội dung đổi → mã đổi → trình duyệt coi là tệp mới.
 * Chỉ băm JSON là đủ cho cả hình: mỗi bài giữ `figureSpec[].sha256_16` của hình
 * mình dùng, nên hình đổi thì JSON cũng đổi theo.
 */
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, host: true },
  build: { outDir: 'dist', assetsInlineLimit: 0 },
  define: { __NOI_DUNG_V__: JSON.stringify(bamNoiDung()) },
});
