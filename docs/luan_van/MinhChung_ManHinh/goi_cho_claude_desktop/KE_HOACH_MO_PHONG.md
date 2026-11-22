# Kế hoạch dữ liệu mô phỏng: 30 học sinh, lớp 1–5 (bản chờ duyệt)

> 22/11/2026. Chưa đẩy lên máy chủ khi bạn chưa duyệt.

## 1. Phân bổ cố định ngay từ đầu

Mỗi tài khoản gắn **một lớp duy nhất** và học đúng chương trình của lớp đó suốt các tháng.

| Lớp | Số em | Toán (bài) | Tiếng Anh (unit) | Tổng bài phải học | Nhịp cần để xong trong ~13 tuần |
|---|---|---|---|---|---|
| 1 | 4 | chưa có | 16 | 16 | khoảng 1 unit / 5–6 ngày, xen ôn tập |
| 2 | 7 | 71 | 16 | 87 | khoảng 1 bài / ngày |
| 3 | 8 | 34 | 21 | 55 | khoảng 4 bài / tuần |
| 4 | 6 | 95 | 21 | 116 | khoảng 1,3 bài / ngày |
| 5 | 5 | 168 (bài ngắn ~7 phút) | 20 | 188 | khoảng 2 bài / ngày |

Mã em đánh theo thứ tự vào học. Tên hiển thị "HS mô phỏng NN", email đuôi `.test`, cờ `moPhong` (giữ nguyên như hiện tại).

## 2. Lịch vào học

- **Đề xuất:** cả 30 em vào học rải rác trong **tháng 7** (01/07–31/07), lệch nhau vài ngày, để đến 31/10 mỗi em đã học khoảng 3 tháng.
- **Phương án khác:** một phần em vào tháng 8–9 và tới 31/10 mới đi được 1–2 tháng ("đang đúng tiến độ"). Muốn vậy, bạn nói rõ tỉ lệ.

## 3. Nhịp học hằng ngày

- **Số buổi:**
  - Học **mỗi ngày**, khoảng 85–95% số ngày. Thỉnh thoảng nghỉ 1–2 hôm (ốm, có việc).
  - Có ngày học **2 buổi**, tần suất mỗi em một khác (khoảng 15–35% số ngày).
- **Giờ học:** chỉ trong **19:00–22:00**, phút bắt đầu ngẫu nhiên mỗi buổi. Hai buổi cùng ngày cách nhau ít nhất 45 phút.
- **Một buổi gồm:** ôn bài cũ đến hạn, rồi 1–3 bài mới.
- **Số bài mới mỗi buổi** do một bộ điều nhịp tính: số bài còn lại chia số ngày còn lại tới mốc 3 tháng, nhân với hệ số riêng của em.

## 4. Mỗi em một tốc độ riêng

- Mỗi em có năng lực nền và tốc độ tiếp thu riêng.
- Bài nào trượt sát hạch thì buổi sau làm lại, nên em yếu sẽ chậm hơn một cách tự nhiên.
- Kết quả dự kiến khi tới mốc 3 tháng:

| Nhóm | Tỉ lệ em | Thời điểm xong chương trình |
|---|---|---|
| Nhanh | khoảng 20% | xong sớm, ở tuần 9–11, rồi chuyển sang ôn |
| Phần đông | khoảng 65% | xong ở tuần 12–13 |
| Chậm | khoảng 15% | tuần 14, hoặc tới 31/10 mới đạt 85–95% chương trình |

Không em nào giống em nào, và không phải 100% em đều xong đúng hạn. Kết quả đều tuyệt đối trông giả và hội đồng sẽ nghi.

## 5. Những gì sẽ đo và đưa vào luận văn

- Đường học: tỉ lệ đúng theo tuần học và theo số lần gặp cùng một nút kiến thức.
- Thời gian trả lời giảm dần.
- Số nút kiến thức đạt mức thạo, do thuật toán BKT của app tính.
- Số tuần để xong chương trình của từng em và theo từng lớp.

## 6. ⚠ Cách trình bày với hội đồng (bắt buộc)

Mốc "xong chương trình trong khoảng 3 tháng" là **kịch bản đặt vào mô phỏng**: giả định em học đều mỗi ngày với nhịp ở mục 1. Đây **không phải kết quả đo** và **không chứng minh** phương pháp làm trẻ học nhanh gấp 3 lần.

**Câu nên viết:**
> "Mô phỏng kịch bản học đều hằng ngày 30–60 phút (19h–22h) cho thấy hệ thống hỗ trợ được nhịp học đi hết chương trình một năm trong khoảng 13 tuần: mô hình người học cập nhật mức thạo đúng, lịch ôn và phụ đạo vận hành, và đường học đi lên."

**Câu không được viết:**
> "Học sinh dùng hệ thống học nhanh gấp 3 lần."

Muốn khẳng định câu này cần thực nghiệm thật có nhóm đối chứng.

## 7. Các bước sau khi bạn duyệt

1. Sửa script theo các mục 1–4, chạy thử ở máy và gửi bạn bảng kết quả **trước khi đẩy**.
2. Bạn đồng ý thì gỡ bộ đang có trên máy chủ và đẩy bộ mới.
3. Kiểm tra trên máy chủ: số tài khoản, số lượt, dữ liệu thật vẫn nguyên.
4. Gắn email đăng nhập (bạn cung cấp) cho 3–4 em, vào Chrome chụp ảnh theo `BANG_MINH_CHUNG.md`.

## 8. Kết quả chạy thử tại máy (22/11/2026, chưa đẩy lên máy chủ)

Đã chốt thêm: mọi em vào học ngẫu nhiên trong tháng 7; em chậm được học kéo sang tháng 11, chậm nhất tới 14/11.

| Lớp | Số em | Toán: tuần xong (trung vị) | Tiếng Anh: tuần xong (trung vị) | Phút học TB / em |
|---|---|---|---|---|
| 1 | 4 | — | 12,4 | 673 |
| 2 | 7 | 12,1 | 11,4 | 916 |
| 3 | 8 | 12,8 | 12,7 | 761 |
| 4 | 6 | 12,3 | 12,1 | 1.263 |
| 5 | 5 | 12,7 | 12,6 | 1.787 |

- **Thời gian xong chương trình:**
  - Nhanh nhất 10 tuần, chậm nhất 16,1 tuần, trung vị 12,6 tuần.
  - Có 6 em còn học trong tháng 11.
- **Giờ mở buổi học** rải từ 19:00 đến 21:45, khoảng 480–580 buổi cho mỗi nửa giờ. Riêng khung 21:30 có ít buổi hơn.
- **Tiến bộ:**
  - Tỉ lệ đúng lần đầu tăng từ 74,3% (tuần 1) lên khoảng 80–82%.
  - Thời gian mỗi câu giảm từ 25,2 giây xuống khoảng 17 giây.
  - Theo lần gặp cùng một nút, tỉ lệ đúng tăng từ 64% lên 86%.
- **Quy mô:** 69.275 lượt. Chi tiết ở `mo_phong/tom_tat_ban_chay_thu.json`.
