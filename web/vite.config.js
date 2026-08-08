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
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0,
    /**
     * TÁCH GÓI THEO NHỊP THAY ĐỔI, không phải theo kích thước.
     *
     * Trước đây tất cả nằm trong MỘT tệp 828 KB có mã băm theo nội dung: sửa một
     * dòng bài học là mã băm đổi, máy của con phải tải lại trọn 828 KB — kể cả
     * phần Firebase và React vốn hàng tháng không đổi.
     *
     * Chia làm ba:
     *   firebase  554 KB — đổi khi nâng SDK, tức là hiếm
     *   react     138 KB — đổi khi nâng React, còn hiếm hơn
     *   index     127 KB — mã của mình, đổi mỗi lần sửa bài
     * Nay deploy nội dung thì con chỉ tải lại 127 KB, hai gói kia nằm yên trong
     * bộ nhớ đệm. Lần tải ĐẦU vẫn bằng cũ — muốn giảm cả lần đầu thì phải nạp
     * Firebase muộn (import động), việc ấy đụng luồng đăng nhập nên để riêng.
     */
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined;
          if (id.includes('/firebase/') || id.includes('@firebase/')) return 'firebase';
          if (id.includes('/react')) return 'react';
          return 'vendor';
        },
      },
    },
    /* Firebase SDK 554 KB là một khối liền, không tách nhỏ hơn được. Đặt ngưỡng
       trên nó để cảnh báo im — cảnh báo kêu mãi vì một chuyện đã biết và đã xử
       thì đến lúc kêu vì chuyện thật cũng không ai nhìn. */
    chunkSizeWarningLimit: 600,
  },
  define: { __NOI_DUNG_V__: JSON.stringify(bamNoiDung()) },
});
