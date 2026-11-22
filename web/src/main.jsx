import React from 'react';
import { createRoot } from 'react-dom/client';
import { napNguong } from './chung/lib/napNguong.js';
import LuoiDoLoi from './chung/components/LuoiDoLoi.jsx';
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
 * Từ 22-11 `napNguong()` đọc BẢNG `nguong` trên Firestore (nơi chuyên gia phát hành),
 * rồi lùi lần lượt: bản nhớ tại máy → tệp tĩnh → bộ mặc định. Có hạn chót ~3 giây, nên
 * mất mạng thì bé chỉ chờ chừng ấy rồi vẫn học được (R4) — không ném, không treo.
 */
const batDau = async () => {
  await napNguong();
  const { default: App } = await import('./App.jsx');
  /* ⚠ LƯỚI ĐỠ BỌC NGOÀI CÙNG. Một `ReferenceError` ở bất kỳ màn nào cũng làm React
     gỡ TOÀN BỘ cây — không bọc thì bé thấy trang trắng, không chữ nào, không nút
     nào. Đã xảy ra hai lần trên bản thật (hook sau `return` sớm; biến dùng trước khi
     khai ở Phòng luyện nói), cả hai lần cổng và bản dựng đều xanh. */
  createRoot(document.getElementById('root')).render(
    <React.StrictMode><LuoiDoLoi><App /></LuoiDoLoi></React.StrictMode>,
  );
};
batDau();
