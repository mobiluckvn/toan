import React from 'react';
import { createRoot } from 'react-dom/client';
import { napNguong } from './chung/lib/napNguong.js';
import './index.css';

/**
 * ⚠ TẢI BỘ NGƯỠNG TRƯỚC, RỒI MỚI IMPORT `App.jsx`. Đây không phải chuyện thứ tự cho
 * đẹp — nó là điều kiện để R7 có tác dụng.
 *
 * Mọi hằng ngưỡng trong `mon/**` (`NGUONG_THAO`, `SAI_LIEN_TIEP_MAC`, `ALPHA`…) gọi
 * `layNguong(boNguong(), …)` ngay LÚC NẠP MODULE. `import` tĩnh ở đầu tệp chạy trước
 * mọi dòng lệnh, nên `import App from './App.jsx'` kiểu thường sẽ nạp cả cây module
 * TRƯỚC khi `napNguong()` kịp đặt bộ — mấy hằng ấy chụp đúng bộ mặc định, tệp tải về
 * chẳng tác dụng gì, và không có gì báo. Nên phải là `await import(...)` động.
 *
 * Mất mạng thì `napNguong()` tự lùi về bộ mặc định (R4), không ném — bé vẫn học được.
 */
const batDau = async () => {
  await napNguong();
  const { default: App } = await import('./App.jsx');
  createRoot(document.getElementById('root')).render(
    <React.StrictMode><App /></React.StrictMode>,
  );
};
batDau();
