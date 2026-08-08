# Lớp 2 — trạng thái (cập nhật 2026-08-08)

**Đã xong toàn bộ nội dung của sách.** Không còn hạng mục nào treo.

| | |
|---|---|
| 33 bài học | đủ 8 mục, 281 câu luyện tập, 165 câu tự kiểm chấm máy |
| 70 hình | 64 trong bài · 6 trong kỳ sát hạch · **33/33 bài có hình** |
| 8 bài ôn tập + 3 ải | 114 câu, đủ đáp án, có Bảng tự soi và đề B |
| Mã nguồn | **dùng chung với lớp 5** — khác biệt khai ở `data/chuong_trinh.json` |

## Dây chuyền — sáu bước, phải chạy liền nhau

```bash
python3 tools/lam_lop2.py     # trích → dễ hiểu → dựng bài → gắn hình → ôn tập → khuôn chung
cd web && npm test && npm run build
```

Vẽ lại hình thì chạy riêng `python3 tools/ve_hinh_lop2.py` (chậm, mà bản mô tả hình
gần như không đổi theo lời văn).

## Ba cái bẫy đã dính, đừng dính lại

- **Gắn hình phải ở BƯỚC CUỐI.** Bước dựng dữ liệu ghi đè trọn tệp bài học, gắn hình
  trước nó là mất sạch hình mà dữ liệu vẫn hợp lệ và bài vẫn chạy — không có gì báo.
- **Đừng neo hình theo nguyên văn dòng.** Lời văn đã được viết lại cho dễ hiểu ở bước 2.
  Neo theo THỨ TỰ BƯỚC (`neoBuoc`) hoặc theo MÃ CÂU (`neoCau`).
- **`npm test` nối bằng `&&`.** Một tệp vỡ là dừng cả chuỗi, mà tổng số PASS trông vẫn
  đẹp. Luôn soi **mã thoát** và **số tệp chạy xong (17)**.

## Việc còn treo (không thuộc lớp 2)

- `firebase-functions` v5 → v7 (breaking changes).
- Gói JS 828 KB vượt ngưỡng cảnh báo của Vite — tách gói bằng `manualChunks`.
- `HomeLop2.jsx` vẫn riêng với `Home.jsx`: hai trang chính khác nhau về bản chất
  (lớp 2 không khoá bài, có bảng sao; lớp 5 khoá theo chương, có thẻ hôm nay).
  Mọi thứ khác đã dùng chung.
