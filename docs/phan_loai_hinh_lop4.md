# Phân loại hình — Toán lớp 4 (Bước 1)

Kiểm kín: mọi hình phải rơi vào đúng một nhóm, tổng các nhóm = tổng hình.

> **Bài học lớp 3 (bẫy 43) áp thẳng vào đây:** đừng nhìn số ảnh gốc mà ước lượng
> công vẽ. Sách lớp 4 có 56 ảnh toán, nhưng **gần hết nằm ở màn mở** — mục giảng
> và mục luyện tập KHÔNG có ảnh nào. Việc vẽ vì thế nhiều hơn số ảnh gốc, không ít hơn.

---

## 1 · Ảnh trong sách gốc — 57 tệp / 100 chỗ neo

| nhóm | chỗ neo | tệp | ta làm gì |
|---|---|---|---|
| ② hình mở bài — hình toán thật | 44 | 44 | **vẽ lại** bằng figforge, và phải là bản ĐỀ |
| ⑨ nhiệt kế tự đánh giá | 44 | 1 | **làm thành phần giao diện**, không phải ảnh |
| ôn tập — hình "Luật chơi" | 11 | 11 | thẻ chữ → làm giao diện |
| bìa · hướng dẫn dùng sách | 1 | 1 | bỏ |
| **tổng** | **100** | **57** | |

Ảnh gốc **không phủ** hai loại hình còn lại (hình giảng theo bước, hình bài tập) —
hai loại ấy phải tự dò và tự vẽ, y như lớp 2 và lớp 3.

## 2 · Ba loại hình phải vẽ

| loại | neo | số lượng | ghi chú |
|---|---|---|---|
| ① hình giảng | `screen:S<k>` theo `Bước n` | **48** | không phải bước nào cũng đáng vẽ |
| ② hình màn mở | `hook` | **44** | bản ĐỀ, bỏ hết dấu vết đáp án (chuẩn mục 6 luật 3) |
| ③ hình bài tập | `item:CX` + `item:CX:giai` | **28** (14 cặp) | chỉ khi bé PHẢI NHÌN mới làm được |
| **tổng** | | **120** | |

## 3 · Nhóm hình theo nguyên mẫu — kiểm kín 120/120

| # | nhóm | nguyên mẫu | hình | nguồn |
|---|---|---|---|---|
| 1 | bảng hàng - lớp, tách số theo tầng | `cau_truc_so` | 9 | lớp 2 |
| 2 | sơ đồ đoạn thẳng: tổng - hiệu, tổng - tỉ, hiệu - tỉ | `doan_thang` | 24 | lớp 2 |
| 3 | băng chuyền biến đổi, tìm X, tính ngược | `may_bien_doi` | 11 | lớp 2 |
| 4 | dãy số & tia số có bước nhảy | `tia_so` | 8 | lớp 2 |
| 5 | trồng cây - treo đèn ba thế trận | `hang_cay` | 4 | lớp 2 |
| 6 | chấm tròn, chia có dư, xếp hàng thừa - thiếu | `cham_tron` | 7 | lớp 2 |
| 7 | bảng liệt kê, bảng theo giờ (đuổi kịp - gặp nhau) | `bang_luoi` | 9 | lớp 2 |
| 8 | hộp có nhãn: CHO GÌ - HỎI GÌ, mẹo thám tử | `hang_hop` | 6 | lớp 2 |
| 9 | gà - chó, giả thiết tạm | `con_vat` | 3 | lớp 2 |
| 10 | cân bập bênh, khử - thế hai hoá đơn | `bap_benh` | 4 | lớp 2 |
| 11 | chu vi - diện tích có số đo từng cạnh | `hinh_chu_vi` | 6 | lớp 2 |
| 12 | lưới diện tích đếm được từng ô 1 m² | `luoi_dien_tich` | 6 | lớp 3 |
| 13 | hình tròn: tâm - bán kính - đường kính | `hinh_tron` | 4 | lớp 3 |
| 14 | sơ đồ Ven hai vòng, chuồng thỏ | `ven_hai_vong` | 3 | lớp 3 |
| 15 | tháp khối, đếm khối theo tầng | `thap_khoi` | 3 | lớp 2 |
| 16 | đồng hồ đọc giờ | `dong_ho` | 2 | lớp 2 |
| 17 | lời thoại Trí Long nói sai | `loi_thoai` | 1 | lớp 2 |
| **18** | **phân số: lát bánh, so sánh, rút gọn** | **`phan_so_lat`** ★ | **12** | **MỚI** |
| **19** | **san bằng trung bình cộng: cột cao - thấp** | **`cot_san_bang`** ★ | **6** | **MỚI** |
| **20** | **hộp giấy khai triển (hình trải phẳng)** | **`khai_trien_hop`** ★ | **2** | **MỚI** |
| **21** | **góc hai kim đồng hồ, đếm khấc** | **`goc_kim`** ★ | **3** | **MỚI** |
| | | | **120** | |

★ = phải dựng mới. Bốn nguyên mẫu, không phải bốn mươi: **17 trên 21 nhóm dùng lại
được** nguyên mẫu lớp 2 và lớp 3 — `arch_l4.py` **nhập** chúng chứ không chép, nên
sửa một nguyên mẫu lớp 2 thì hình lớp 4 được sửa theo.

### Vì sao đúng bốn cái mới

- **`phan_so_lat`** — cả chương 9 (5 bài, 12 hình) là phân số, mà không nguyên mẫu
  nào của hai quyển trước vẽ được phân số. `hinh_phang` có `chia`/`to_phan` nhưng
  chỉ cho MỘT hình; bài "lát nào to hơn" phải đặt **hai mẫu số khác nhau cạnh nhau,
  cùng một cái bánh** thì bé mới so được — vẽ hai bánh to nhỏ khác nhau là dạy ngược.
- **`cot_san_bang`** — trung bình cộng phải thấy CỘT CAO BỊ SAN XUỐNG CỘT THẤP thì
  "tổng phần vượt = tổng phần hụt" mới hiện ra. Vẽ bằng `hang_hop` thì chỉ còn mấy
  con số nằm cạnh nhau, mất đúng cái bài đang dạy.
- **`khai_trien_hop`** — `khoi_hop` vẽ khối nhìn nghiêng; bài 41 cần bản **trải
  phẳng** để bé đếm 6 mặt. Hai thứ khác hẳn nhau.
- **`goc_kim`** — `dong_ho` vẽ được kim nhưng không có cung góc và không đếm khấc.
  Bài 44 hỏi "mấy khấc", nên khấc phải **đếm được trên hình**.

## 4 · Hình ĐẾM ĐƯỢC — chỗ dễ dính lại bẫy 22-26

Bài lớp 4 có bốn chỗ phải đếm thật, và cả bốn đều đã dính ở quyển trước:

| bài | phải đếm | luật |
|---|---|---|
| B11 chia có dư | vẽ **cả phần dư**, cùng cỡ chấm với phần đã chia | bẫy 24 · 26 |
| B15 trồng cây | đếm được **cả cây lẫn khoảng** | — |
| B41 đếm khối | xếp **tháp thật**, có khối nấp hàng sau + bản trải phẳng từng tầng | bẫy 22 |
| B33 so phân số | các lát của **cùng một cái bánh** phải bằng nhau | bẫy 26 |

## 5 · Việc đã cân nhắc và LOẠI

- **Vẽ đủ 176 hình giảng (44 bài × 4 bước).** Loại: chuẩn dặn "không phải bước nào
  cũng đáng vẽ". Bước chỉ diễn giải bằng lời mà thêm hình là thêm thứ để bé phải đọc.
  48 hình phủ đủ 44 bài, bài nào dày ý thì hai hình.
- **Giữ ảnh gốc của sách làm hình mở.** Loại vì ba lẽ: màu không khớp bảng màu
  thương hiệu; ảnh **có sẵn đáp án** trong khi màn mở phải là bản ĐỀ; và ảnh raster
  không sửa lại được khi lời văn đổi.
- **Chép `arch_l3.py` thành `arch_l4.py`.** Loại: bản chép sẽ tụt hậu ngay lần sửa
  nguyên mẫu sau. Nhập vào, đúng như lớp 3 đã làm với lớp 2.
