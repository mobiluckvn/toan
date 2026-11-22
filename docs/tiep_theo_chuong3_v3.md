# Chương 3 viết lại — bản v3

Tệp sinh ra: `docs/Chuong3_Luan_van_v3.docx` (32 bảng · 6 hình · 6 thuật toán,
≈ 20.400 từ — bản trong `Luan_van_Chuong2_Chuong3_v2.docx` là ≈ 29.800 từ).

## Dựng lại

Ba bước, theo đúng thứ tự — bước sau đọc kết quả của bước trước:

```bash
node tools/chuong3_v3_so.mjs                          # → docs/chuong3_v3_so.json
tools/tts/.venv/bin/python tools/chuong3_v3_hinh.py   # → docs/hinh_c3v3/*.png
tools/tts/.venv/bin/python tools/chuong3_v3.py        # → docs/Chuong3_Luan_van_v3.docx
```

⚠ ĐỪNG SỬA TAY TỆP `.docx`. Chạy lại là dựng lại.

`chuong3_v3_so.mjs` là chỗ đáng chú ý nhất: nó `import` thẳng các mô-đun đang
chạy thật — `functions/src/bkt.js`, `functions/src/ara.js`,
`functions/src/report.js`, `lib/doThi.js`, `lib/lantruyen.js`,
`lib/chinhsach.js`, `lib/zpd.js`, `lib/phudao.js`, `lib/suKien.js`,
`lib/cefr.js` — rồi cho một bé giả đi qua một phiên và ghi mọi con số ra JSON.
Sai công thức trong mã thì số trong luận văn sai theo, nên mục 3.6 là bằng
chứng chứ không phải lời kể.

## Chín nhận xét của Thầy → chỗ trả lời

| Nhận xét | Mục |
| --- | --- |
| Làm 01 phiên 01 cá nhân cụ thể sẽ như thế nào (một ví dụ minh hoạ) | 3.6 (11 bảng, 2 hình) |
| Tiêu chí để phát hiện lỗ hổng | 3.4.1 — Bảng 3.11, đối chiếu ở Bảng 3.20 |
| Người phản biện sẽ hỏi những gì, ví dụ minh hoạ | 3.7 — Bảng 3.29, 13 câu |
| Đồ thị tri thức biểu diễn như thế nào | 3.2.2 — G = (V, E, τ, λ) |
| Một đồ thị tri thức có bao nhiêu nút, tham khảo tài liệu nào | Bảng 3.3 — đặt cạnh ASSISTments, Doignon–Falmagne, KnowEdu |
| Cài đặt thì biểu diễn trên máy thế nào; tập nút ở bảng nào; mệnh đề điều kiện | 3.2.4 — Bảng 3.7 + hai phép truy vấn + `E_prereq` |
| Đồ thị thành hình ra sao; các thuộc tính nào | 3.2.1 (Hình 3.2, sáu bước) và Bảng 3.5 (18 + 10 trường) |
| Phiên của một cá nhân lưu thông tin gì và lưu thế nào | 3.3 — Hình 3.4, Bảng 3.8, 3.9, 3.28 + hai bản ghi nguyên văn |
| Xử lý tình huống: đánh giá được các tình trạng như thế nào | 3.4.4 — Bảng 3.13, sáu tình trạng và luật nhận dạng |
| Đề xuất phương pháp gợi ý, ví dụ rất cụ thể | 3.5 (ba loại can thiệp) và 3.6.6 (bài phụ đạo thật, bốn câu thật) |

## Cắt những gì để ngắn hơn

- Mục 3.3 bản cũ (nhận biết hành vi, 7 tiểu mục + 4 thuật toán) → gộp còn
  **một bảng** (Bảng 3.14) ở mục 3.4.5. Bốn thuật toán ấy vẫn nằm trong mã và
  có cổng kiểm; luận văn chỉ nêu tín hiệu, ngưỡng và giới hạn.
- 14 thuật toán → **6**. Sáu thuật toán còn giữ là những thuật toán mà không
  đọc thủ tục thì không hiểu được cơ chế. Số còn lại được nhắc tên tại chỗ.
- Bỏ hẳn mục "công nghệ sử dụng theo tầng" (Bảng 3.21 và 3.25 bản cũ) — nó
  thuộc phụ lục chứ không thuộc lập luận thiết kế.
- Mục 3.7 bản cũ (6 kịch bản × 7 tiểu mục) → **một bảng** (Bảng 3.31).
- Phần "quyết định thiết kế" sau mỗi thuật toán: giữ tối đa 2–3 mục thay vì 5.

## Ví dụ ở mục 3.6 — tóm tắt để đọc nhanh

Bé M. lớp 3 mở bài `DL:TA3.B13` (Unit 13 — My house), 11 lượt. Tám lượt đầu
đúng, ba lượt cuối sai liên tiếp tại mẫu câu `sp_g3_u13_2`
(*Where are the [Furniture-plural]? – They're [Preposition] the room*).

- Bốn tiêu chí TC1–TC4 đều thoả; `S_c = 3` là tiêu chí làm giao diện mời bé.
- Duyệt ngược trên `E_prereq` cho **7 ứng viên**; 3 bị loại vì đã đạt ngưỡng.
- Nút gốc rễ: `sp_g3_u9_2` (*What colour are they? – They're [Colour].*),
  **dạy ở bài khác** — `DL:TA3.B09` — cách 1 bước, P(L) = 0,374, độ ngờ 0,375.
- Bài phụ đạo lấy **4 câu thật** từ kho tĩnh của B09; ΔC tại nút gốc rễ
  0,374 → 0,839.

## Bốn chỗ ví dụ này phơi ra (đều đã vào Bảng 3.32)

1. **32/894 nút có dưới 4 câu hỏi** → với những nút ấy không dựng được cặp
   A-R-A hợp lệ từ kho tĩnh. Nút trong ví dụ có đúng 3 câu, và cả 3 đã dùng ở
   lần đo trước.
2. **Nút gốc rễ đổi sau can thiệp** — đúng về cơ chế, nhưng báo cáo cho phụ
   huynh phải kèm mốc thời gian.
3. **`metMoi()` dương tính giả** trên chính phiên này: nửa đầu 5.780 ms, nửa
   cuối 10.820 ms, chênh 87 %. Nguyên nhân: hàm gom theo ĐỊNH DẠNG để loại trừ
   độ khó, nhưng ở đây cả 11 lượt cùng định dạng `chon` trong khi bậc tăng từ
   khởi động lên ráp câu. **Phải đổi khoá gom thành bộ đôi (định dạng, bậc)** —
   `functions/src/report.js`, hàm `metMoi`.
4. **`cauMoTa()` làm tròn phủ vốn tới phần trăm nguyên** → 0,3 % hiển thị thành
   0 %. `lib/cefr.js`.

## Việc còn lại khi ghép vào luận văn đầy đủ

- Bảng 0.4 "Mã hiệu dùng trong Chương 3" ở phần đầu tài liệu cần cập nhật:
  thêm **TC1–TC4**; sửa "Thuật toán 3.1 … 3.14" thành **3.1 … 3.6**; bỏ
  **M0–M3** và **GT1/GT2** (bản mới không đánh số giả thuyết riêng, chúng nằm
  trong cột "Giả thuyết chính" của Bảng 3.31).
- Danh mục hình và danh mục bảng phải dựng lại (32 bảng, 6 hình).
- Năm tài liệu tham khảo mới: Doignon & Falmagne (1985), Hogan và cộng sự
  (2021), Chen và cộng sự (2018), Liu và cộng sự (2021), Piech và cộng sự
  (2015).
