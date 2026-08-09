# Phân loại hình lớp 3

Khảo sát ngày 2026-08-09 từ `docs/Toan_Tu_Duy_Lop3_Cuoc.docx`, phần `word/media/`.
Đây là **Bước 1** của `CHUAN_DUA_SACH_VAO_APP.md` mục 10.

## Kết luận ngắn — và điều bất ngờ

| | |
|---|---|
| Chỗ neo ảnh trong sách | 80 |
| Tệp ảnh khác nhau | 47 |
| **Nhiệt kế** `image3.png` — dùng lại **34 lần** | → **thành phần giao diện**, không vẽ |
| Hình toán thật | **46** |

**Điều bất ngờ, quan trọng nhất của Bước 1:** hình của sách gần như toàn bộ nằm ở
**mục ② Chuyện mở bài** (31 hình), còn mục ③ Khám phá — nơi dạy nguyên tắc — chỉ có
**6 hình cho 34 bài**.

| mục | số hình | là gì |
|---|---|---|
| ② Chuyện mở bài | **31** | hình nêu ĐỀ, thường có ô trống để bé điền |
| ③ Khám phá | **6** | hình giảng — chỉ B1, B2, B3, B5, B6, B12 có |
| ⑧ Góc bố mẹ | 8 | thẻ "Luật chơi" mở đầu 8 bài ôn tập |
| — | 1 | `image18.png`, thẻ sticker/ôn tập chung |

Đối chiếu với chuẩn mục 10 · Bước 3 (**ba loại hình**):

| loại hình | sách cho sẵn | phải tự dựng |
|---|---|---|
| hình màn mở | 31 | 3 (B7, B10, B17 chưa có) |
| hình giảng | 6 | **~28 bài chưa có hình giảng nào** |
| hình bài tập (`item:CX` + `:giai`) | **0** | toàn bộ |

Lượt lớp 2 dựng 120 hình từ 75 ảnh gốc. Lớp 3 xuất phát từ 46 — **khối lượng vẽ sẽ
nhiều hơn lớp 2**, không ít hơn. Đừng nhìn con số 47 ảnh mà tưởng nhẹ.

## Ba việc rút ra ngay

1. **Nhiệt kế làm thành component**, không phải 34 tấm PNG. Nó là thanh 5 mức
   (1★ "Ôn lại cùng bố mẹ" → 5★ "Tuyệt vời! Sang bài mới") — đúng thứ nên bấm được,
   nối thẳng vào điểm quiz mà app đã có.
2. **Thẻ "Luật chơi" của 8 ôn tập** (mục ⑧) cũng là khung chữ, nên làm giao diện chứ
   không phải ảnh — giống cách Quyển 2 lớp 5 làm 53 sơ đồ chiến thuật.
3. Hình sách ở mục ② **đã đúng tinh thần màn mở của chuẩn**: nêu đề, có ô trống chưa
   điền (xem `image25.png` — bốn tòa tháp NGHÌN·TRĂM·CHỤC·ĐƠN VỊ, ô trống để bé viết
   2 4 3 5). Giữ ý tưởng, vẽ lại bằng FigForge cho đúng bảng màu và cỡ chữ.

## Nhóm nguyên mẫu — 46 hình toán

| # | Nhóm | Bài | Hình |
|---|---|---|---|
| 1 | Tháp giá trị chỗ (nghìn·trăm·chục·đơn vị) | B1 ②③, B2 ③ | 3 |
| 2 | Xếp thẻ số · chẵn lẻ theo đuôi | B3 ③ | 1 |
| 3 | Đếm số & đếm trang — ba đoàn tàu | B4 ② | 1 |
| 4 | Tách - gộp phép nhân (thùng cá) | B5 ③ | 1 |
| 5 | Chia có dư — rương ngọc, luật vàng | B6 ②③ (2 hình ②) | 3 |
| 6 | Gấp lên · giảm đi · một phần mấy | B8 ②, B9 ② | 3 |
| 7 | Đoàn tàu — dãy số nhịp đều, ga dừng | B9 ②, B11 ②, B12 ②③ | 4 |
| 8 | Biểu thức · ngoặc · tìm X · tính thuận tiện | B13 ②, B14 ②, B15 ②, B16 ② (2 hình) | 5 |
| 9 | Sơ đồ đoạn thẳng · sơ đồ phần | B18 ②, B19 ②, B20 ② | 3 |
| 10 | Máy biến đổi · đi lùi · thay thế | B21 ②, B22 ②, B26 ② | 3 |
| 11 | Gà - chó · trồng cây · sơ đồ Ven | B23 ②, B24 ②, B25 ② | 3 |
| 12 | Hình học phẳng · khối · tròn | B27 ②, B28 ②, B29 ②, B30 ②, B31 ② | 5 |
| 13 | Đo lường: giờ & lịch · cân đong · tiền | B32 ②, B33 ②, B34 ② | 3 |
| 14 | Thẻ "Luật chơi" ôn tập | ⑧ × 8 + `image18` | 9 → **giao diện** |

**Nguyên mẫu cần dựng: 13 nhóm.** Nhiều nhóm dùng lại được nguyên mẫu lớp 2 đã có:

| nhóm lớp 3 | nguyên mẫu lớp 2 dùng lại |
|---|---|
| 1 · tháp giá trị chỗ | `cau_truc_so` (mở rộng thêm tầng NGHÌN) |
| 5 · chia có dư | `cham_tron` (đã có tham số `du`) |
| 6 · gấp/giảm, một phần mấy | `hinh_phang` với `chia`, `cham_tron` |
| 7 · đoàn tàu, dãy số | `day_o`, `tia_so` |
| 9 · sơ đồ đoạn thẳng/phần | `doan_thang`, `hang_hop` |
| 10 · máy biến đổi | `may_bien_doi` |
| 11 · gà - chó, trồng cây | `con_vat`, `hang_cay` |
| 12 · hình học | `hinh_phang`, `hinh_ghep`, `thap_khoi`, `hinh_chu_vi`, `dong_xu_cham` |
| 13 · xem giờ | `dong_ho` |

**Phải dựng mới:** sơ đồ Ven hai vòng (B25), bảng lịch tháng (B32), cân & ống đong
(B33), tiền Việt (B34), biểu thức có ngoặc (B13-B14). Khoảng **5 nguyên mẫu mới**.

## Việc tiếp — Bước 2

- [ ] Viết `tools/rut_lop3.py` (chép `rut_lop2.py`, sửa mẫu neo theo mục 4 bản khảo sát)
- [ ] Bảng khớp mục sang khuôn chung — thêm trường `hatMam` và `ganLop2`
- [ ] Quyết mối nối ôn tập → bài (lớp 3 không có Bảng tự soi)
