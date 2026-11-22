# Bảng minh chứng: khẳng định trong luận văn → ảnh chụp màn hình thực tế

> Lập 22/11/2026. Nguồn khẳng định: `Luan_van_Thac_si_VuTriCong_v6.docx`.
> Ảnh lưu ở `that/` (tài khoản thật hoặc chức năng không phụ thuộc dữ liệu) và `mo_phong/` (tài khoản **học sinh mô phỏng**).
> Ứng dụng: https://ky-su-nhi.web.app. App không có đường dẫn riêng cho từng màn hình; cột "Đường bấm" ghi cách đi tới màn hình đó.

## Quy ước bắt buộc khi đưa vào luận văn và slide

1. Ảnh trong `mo_phong/` phải có chú thích dạng *"Hình 4.x – … (tài khoản học sinh mô phỏng, dữ liệu mô phỏng 07–10/2026)"*.
2. Dữ liệu mô phỏng gồm **30 học sinh ảo lớp 1–5** (4/7/8/6/5 em) và 69.275 lượt. Các em vào học trong tháng 7/2026, theo kịch bản học đều hằng ngày từ 19h đến 22h (`tom_tat.json`, sinh bằng `web/tools/mo_phong/hoc_sinh_ao.mjs`, hạt giống 20260701). Không được gọi là "học sinh thật" hay "dùng thử".
3. Số liệu "nhật ký thật" đang có trong luận văn (3.213 lượt, 10 tài khoản, đo ngày 10/10/2026) là **dữ liệu thật**. Giữ nguyên và **không trộn** với số mô phỏng. Máy chủ đã loại học sinh mô phỏng khỏi các phép đo ấy (`functions/src/moPhong.js`).

## Bảng đối chiếu

Trạng thái: ⬜ chưa chụp · ✅ đã chụp · ⚠️ luận văn cần sửa câu chữ.

| STT | Mục luận văn | Khẳng định | Đường bấm / điều phải thấy | Loại TK | Tệp ảnh | TT |
|---|---|---|---|---|---|---|
| 1 | 4.1, Bảng 4.1 | Có màn bài học, luyện nói, ôn tập, phụ huynh, chuyên gia; chạy trên trình duyệt | Học sinh → "Kệ sách của con": các quyển, "📖 Sổ bố mẹ", "Bảng xếp hạng" | thật | mo_phong/01_ke_sach_minhan_lop1.jpg | ✅ |
| 2 | 3.2.2, 4.1 | 94 bài Tiếng Anh, 5 khối | Kệ sách → quyển Tiếng Anh lớp 3 → danh sách Unit | thật | that/02_ds_unit.png | ⬜ |
| 3 | 3.3.1 | Mỗi lần mở bài là một phiên, đi qua các chặng | TA3 → Unit 13: thanh chặng Từ mới · Mẫu câu · Luyện tập · Nói chuyện · Sát hạch · Phòng luyện nói | thật | that/03_chang_bai.png | ⬜ |
| 4 | 3.1.2 (R1) | Trẻ không cần đọc chữ: ô ba trạng thái | Trong bài: thanh "Việc của con" | thật | that/04_thanh_viec.png | ⬜ |
| 5 | 3.5.1 (R2) | Mở bài khi đã đạt hoặc đã thử ≥ 2 lần | Danh sách bài: một bài được mở dù bài trước "chưa đạt" | mô phỏng | mo_phong/05_mo_bai.png | ⬜ |
| 6 | 3.5.2, Hình 3.17 | Xếp lại câu theo vùng phát triển gần | Luyện tập cùng một bài, hai buổi khác nhau | mô phỏng | mo_phong/06_zpd_a.png, 06_zpd_b.png | ⬜ |
| 7 | 3.4.4 (H4) | Gợi ý tự hiện sau 2 lần sai | Một câu luyện tập sai 2 lần | thật | that/07_goi_y.png | ⬜ |
| 8 | 3.5.3, 3.6.4 | Sai 3 lần liền thì vào phụ đạo 4 câu, lấy từ nút nguyên nhân | Màn Phụ đạo: "Cô thấy con chưa chắc phần …" | mô phỏng | mo_phong/08_phu_dao.png | ⬜ |
| 9 | 3.5.3 | Không để màn trắng khi gọi mạng | "Đợi cô một chút nhé…" rồi có câu ngay | thật | that/09_cho_mang.png | ⬜ |
| 10 | 3.5.3, 4.1 | Phòng luyện nói có mô hình ngôn ngữ và nhận dạng giọng nói | Phòng luyện nói: "Cô đang nghĩ…" và câu trả lời | thật | that/10_phong_noi.png | ⬜ ⚠️ |
| 11 | 2.1.2.d | Trẻ tự chọn chủ đề yêu thích | "Con chọn một cái, rồi mình sẽ tập nói về nó." | thật | that/11_chon_chu_de.png | ⬜ |
| 12 | 4.1 | Máy nghe trẻ nói, đọc câu mẫu | Chặng Nói chuyện: "Đến lượt con nói", "Nghe lại" | thật | that/12_noi_chuyen.png | ⬜ |
| 13 | 3.5.3 (R6) | AI chấm bài viết, ghi rõ là máy chấm | Bài viết: "Điểm", "Ai chấm", "Cô khen", "Lời cho bố mẹ" | thật | that/13_cham_viet.png | ⬜ |
| 14 | R6 | Điểm máy chấm chờ bố mẹ xác nhận | Góc bố mẹ: "Điểm máy chấm chờ bố mẹ xem (n)" | thật | that/14_cho_duyet.png | ⬜ |
| 15 | R5, 2.3.1 | Không lưu lời nói; bố mẹ xoá được trí nhớ của cô | "Cô giáo máy đang nhớ gì về con", nút "Xoá trí nhớ của cô" | thật | that/15_tri_nho.png | ⬜ |
| 16 | 3.1.3, 3.4.4 | Thẻ ôn +1/+3/+7 ngày | Trang quyển: thẻ "Ôn lại" → màn Ôn lại | mô phỏng | mo_phong/16_on_lai.png | ⬜ |
| 17 | 4.1 | Có kỳ ôn tập và đọc hiểu | Ôn tập; Đọc hiểu: "Nghe câu này" | thật | that/17_on_tap_doc.png | ⬜ |
| 18 | 3.6.6, Bảng 3.16 | "Mắc ở Unit 13, nguyên nhân là Unit 9" | Góc bố mẹ · "con đang mắc ở đâu": "nắm x%", "Gốc đáng ngờ…" | mô phỏng | mo_phong/18_goc_ngo.png | ⬜ |
| 19 | 3.6.6 | Mức phủ theo khối, phân số thật | "Con đang ở đâu trên thang năng lực" | mô phỏng | mo_phong/19_thang_nang_luc.png | ⬜ |
| 20 | 3.4.4 (H7) | Dạng câu tốt nhất chỉ hiện khi ≥ 8 lượt | Góc bố mẹ · "hệ thống biết gì về cách con học" | mô phỏng | mo_phong/20_dang_cau.png | ⬜ |
| 21 | 3.4.4 (H6) | Tín hiệu mệt mỏi chỉ báo cho người lớn | Sổ bố mẹ: "Con có chậm dần trong buổi học không" | mô phỏng | mo_phong/21_met_moi.png | ⬜ |
| 22 | 2.4.5, Bảng 3.23 | Đường cong học tập | Sổ bố mẹ: "Càng luyện càng ít sai" | mô phỏng | mo_phong/22_duong_hoc.png | ⬜ |
| 23 | 5.1 | Sổ phụ huynh tổng hợp nhiều môn | Sổ bố mẹ: tab môn, BÀI ĐÃ ĐẠT / ĐÃ VỮNG / KỸ NĂNG CÒN YẾU | mô phỏng | mo_phong/23_so_bo_me_tieng_anh_minhan.jpg | ✅ |
| 24 | 5.1 | Giáo viên xem kết quả chẩn đoán | Bảng theo dõi: 28/45 em có học, "EM CẦN GIÚP TRƯỚC" | mô phỏng | mo_phong/24_gv_bang_theo_doi.jpg | ✅ |
| 25 | 5.1, 3.3 | Giáo viên xem chi tiết một em, có biểu đồ tiến bộ | Bảng theo dõi → bấm một em → tab Biểu đồ, phần A (1–4): tỉ lệ đúng lần đầu/tuần, bài đã học cộng dồn, phút/tuần, giờ học — mọi biểu đồ có tên trục và dòng "Cách đọc" | mô phỏng | mo_phong/24b, 24d, 24g (tổng quan); mo_phong/25_bieudo_dieulinh_1_2.jpg, 25_bieudo_dieulinh_3_4.jpg | ✅ |
| 25a | 2.5, 3.9 | Đường cong học tập: tỉ lệ lỗi theo lần luyện, bỏ điểm < 10 lượt | tab Biểu đồ → 5 | mô phỏng | mo_phong/25_bieudo_dieulinh_5_6_duongcong_nutvung.jpg | ✅ |
| 25b | 2.3.3, Hình 3.9, 3.13 | Số nút đạt θ theo tuần, trước và sau khi tính quên | tab Biểu đồ → 6 | mô phỏng | mo_phong/25_bieudo_dieulinh_5_6_duongcong_nutvung.jpg | ✅ |
| 25c | Bảng 3.9, Hình 3.10 | Sáu tình trạng của nút trên dữ liệu một em | tab Biểu đồ → 7 | mô phỏng | mo_phong/25_bieudo_dieulinh_7_8_tinhtrang_quen.jpg | ✅ |
| 25d | Hình 3.13 | Hồ sơ nút trước và sau khi tính quên (tới hôm nay) | tab Biểu đồ → 8 | mô phỏng | mo_phong/25_bieudo_dieulinh_7_8_tinhtrang_quen.jpg | ✅ |
| 25e | Hình 3.14, 3.16 | Diễn biến P(L) và số lần sai liên tiếp tại một nút, vạch θ, θ_yếu, NG09 | tab Biểu đồ → 9 (chọn nút) | mô phỏng | mo_phong/25_bieudo_dieulinh_9_dienbien_nut.jpg | ✅ |
| 26 | 3.9 | Bảng xếp hạng chỉ hiện biệt danh, mỗi môn một bảng | "Bảng xếp hạng", "← con đây", tab Toán / Tiếng Anh | mô phỏng | mo_phong/26_xep_hang_tuan_nay.jpg, mo_phong/26b_xep_hang_tieng_anh_minhan.jpg | ✅ |
| 27 | 1.4, 3.8.4, 4.2 | 21 ngưỡng, 5 nhóm | Chuyên gia → Bảng ngưỡng | thật | that/27_bang_nguong.png | ⬜ |
| 28 | 3.8.4, Bảng 3.21 | Sửa θ thì tính lại nhịp công nhận | Sửa NG07 0,85 → 0,80: "nói đúng mấy câu liền" 4 → 3 (**không phát hành**) | thật | that/28_sua_theta.png | ⬜ |
| 29 | 3.8.4 | Giá trị sai bị báo lỗi | Nhập NG08 = 0,8 → báo vi phạm (**không phát hành**) | thật | that/29_rang_buoc.png | ⬜ |
| 30 | 3.8.4, 4.2 | Phát hành phải có lý do, có lịch sử | Ô lý do và nút phát hành. **Chỉ chụp trên bộ giả lập**, vì 4.6 khẳng định chưa phát hành lần nào | thật | that/30_phat_hanh.png | ⬜ |
| 31 | 3.8.4, 4.5.3 | Duyệt đề xuất máy học | Bảng ngưỡng → "Đề xuất máy học được →" (2 đề xuất NG16) | thật | that/31_de_xuat.png | ⬜ |
| 32 | 3.8.5, 4.5.3 | Thống kê ngưỡng theo tuần | "Dữ liệu tuần này nói gì về các ngưỡng" | thật | that/32_thong_ke.png | ⬜ |
| 33 | 3.3.1–3.3.3 | Mỗi phiên ghi bốn kho | Firebase console: một tài liệu `attempts` và một `mastery` | mô phỏng | mo_phong/33_firestore.png | ⬜ |
| 34 | 3.6.8 | Học bạ có mục phụ đạo | Firestore → `hocBaTA` → mục phudao | thật | that/34_hocba_phudao.png | ⬜ |
| 35 | 3.3.4, 3.8.2 | Quyền ghi khai ở tầng cơ sở dữ liệu | Firebase console → Rules (đoạn `nguong`) | thật | that/35_rules.png | ⬜ |
| 36 | R4, 2.4.6 | Học được khi mất mạng | DevTools Offline, bài vẫn chạy | thật | that/36_offline.png | ⬜ |
| 37 | 4.3.1, Phụ lục A | Bộ kiểm thử tự động | Terminal `npm test` | thật | that/37_npm_test.png | ⬜ |
| 38 | 4.1 | Đăng nhập email + mã; chọn người học | Màn đăng nhập, "Ai đang học" | thật | that/38_dang_nhap.png | ⬜ |

## Những chỗ luận văn cần sửa (⚠️)

- **Dòng 10, mục 3.5.3 và 4.1:** luận văn ghi mô hình `gpt-oss-120b`. Từ 22/11/2026 hệ thống chạy **Gemini 3.8 Flash**. Cần sửa tên mô hình, hoặc ghi "giai đoạn đo dùng gpt-oss-120b, sau đó nâng lên Gemini 3.8 Flash".
- **Dòng 26 và mọi ảnh:** theo xác nhận của tác giả ngày 22/11/2026, **toàn bộ 46 tài khoản trên hệ thống đều là tài khoản do tác giả tạo**; không có người dùng thật. Giao diện không còn nhãn, nên **mọi chú thích hình phải ghi "dữ liệu mô phỏng"**, và các câu "nhật ký thật" trong luận văn phải sửa theo.
- **Dòng 24–25:** bảng giáo viên vẫn **chỉ có trẻ thật**. Chụp dòng này với dữ liệu thật hiện có.
- **Dòng 24, mục 5.1:** câu "trình bày kết quả chẩn đoán cho giáo viên" chưa khớp mã nguồn. Ma trận "gốc đáng ngờ" chỉ hiện ở Góc bố mẹ. Nên sửa câu, hoặc chỉ khẳng định "giáo viên thấy em đang tắc".
- **Chương 4 nên thêm một mục mới** "Thực nghiệm trên dữ liệu mô phỏng 30 học sinh (07–10/2026)", với các bảng sau, đều lấy từ `tom_tat.json`:
  - tỉ lệ đúng lần đầu theo tuần học: 70,5% → khoảng 80–84%;
  - thời gian mỗi câu: 27,6 giây → khoảng 17 giây;
  - đường học theo lần gặp nút: 54,6% → 87%.

  Phần này đặt **cạnh** mục 4.5 (nhật ký thật), không thay thế.

## Tài khoản học sinh mô phỏng dùng để chụp

| HS | Lớp | Vào học | Ghi chú |
|---|---|---|---|
| (điền sau khi gắn email đăng nhập) | | | |

## Việc còn lại

- [ ] Gắn email đăng nhập được cho 3–4 em mô phỏng (bạn cung cấp địa chỉ).
- [ ] Chụp lần lượt các dòng ⬜, rồi cập nhật cột TT.
