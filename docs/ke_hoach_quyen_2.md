# Kế hoạch đưa QUYỂN 2 lên phần mềm

**Nguồn:** `docs/KSN5_Q2_TRON_QUYEN_Mua_Giai_Vo_Dich.docx` (2,8 MB · 4 597 đoạn · 119 532 chữ · 48 ảnh)
**Ngày lập:** 08/08/2026 · dựa trên số liệu đếm được từ chính tệp gốc, không ước lượng.

---

## 1 · Quyển 2 có gì — số liệu đã đếm

| Khối | Số lượng | Ghi chú |
|---|---|---|
| Bài kỹ năng phòng thi | **5** (T1–T5) + 1 sát hạch trại | không có câu hỏi đánh số, dạy quy trình |
| Vòng đấu | **14** × 15 câu = **210 câu** | mỗi vòng 45 phút · thang 15 điểm |
| Đề trộn | **4** × 10 câu = **40 câu** | 30 phút · **chấm kép** toán + định dạng |
| Kỳ thi thử | **3** (20 + 20 + 24) = **64 câu** | vòng loại · bán kết · chung kết |
| **Tổng câu hỏi** | **314** | |
| Hồ sơ bẫy Cáo Đề | **168** | mã · tầng · dấu hiệu · đòn gỡ · thần chú |
| Thẻ chiến thuật | **14** | một thẻ mỗi chương |
| Màn (giai đoạn) | **81** | mỗi vòng 4 màn |
| Chỗ chèn sơ đồ | **71** | nhưng chỉ có **48 ảnh** → thiếu 23 |

### Phát hiện quan trọng nhất

**168 mã bẫy `CĐ-x.y` ghép 1–1 tuyệt đối với 168 micro của Quyển 1** — đã kiểm:
khớp 168/168, không thừa, không thiếu (`CĐ-4.2` ↔ `DL:KSN5Q1.B4.M2`).

Đây là trục nối hai quyển. Nhờ nó, không phải bịa thêm gì mà vẫn làm được:

- con sập bẫy `CĐ-4.2` → mở thẳng micro `B4.M2` của Quyển 1 để ôn
- mức thạo BKT tích được ở Quyển 1 dùng ngay để đoán vòng đấu nào con sẽ yếu
- cô giáo nhìn một bảng thấy cả hai quyển, không phải hai hệ thống rời

---

## 2 · Điểm khác biệt cốt lõi — và vì sao không bê nguyên khuôn Quyển 1

| | Quyển 1 | Quyển 2 |
|---|---|---|
| Mục đích | HIỂU và LÀM ĐƯỢC | biến nội công thành **ĐIỂM SỐ phòng thi** |
| Chấm | **máy chấm 1141/1141 câu** | **barem 4 mốc**, con tự chấm |
| Thời gian | không đồng hồ | **có đồng hồ**, 45 / 30 phút |
| Cổng | `mustPass` — sai câu bẫy là chặn | đạt 12/15 → mở vòng sau |
| Giá trị thật | ở chỗ làm đúng | ở **màn 2 và màn 3**, không ở điểm |

Sách nói thẳng: *"Điểm của màn 1 chỉ là số liệu; giá trị thật của vòng đấu nằm ở
màn 2 và màn 3."* Ép Quyển 2 vào khuôn máy-chấm của Quyển 1 là **phá đúng cái nó
định dạy** — trình bày ăn điểm, tự soi bài, nhận diện bẫy.

Nhưng để nguyên tự chấm hết thì cô giáo không có số liệu tin được, và không gating
được. **Đề xuất: chấm ba tầng.**

| Tầng | Ai chấm | Dùng để |
|---|---|---|
| **Đáp số** | máy (292/314 câu có đáp số gọn) | số liệu khách quan · mở khoá vòng sau · BKT |
| **Barem trình bày** | con tự tick 4 mốc | dạy cách ăn trọn điểm — nội dung chính của T2 |
| **Phiên tòa bẫy** | con tick SẬP / THOÁT từng bẫy | chẩn đoán, nối về micro Quyển 1 |

Chỉ **22/314 câu** (7%) bắt buộc giải thích bằng lời — số này để tự luận thuần,
đúng như kiểu `tuluan` đã có sẵn.

---

## 3 · Bài học Quyển 1 — áp dụng ngay từ đầu, không sửa sau

Đây là những thứ đã phải trả giá. Ghi ra để không lặp lại.

| Đã vấp ở Quyển 1 | Giá phải trả | Làm khác ở Quyển 2 |
|---|---|---|
| 513 câu **không có mã** | phải chạy migration đặt mã sau | bộ trích xuất **sinh mã ngay**, có phép kiểm chống trùng |
| `answerFields` trả rỗng cho tf/mcq | **90 câu không bấm được**, 68 câu tự động đúng | chạy bộ rà "con có làm được không" **trước khi** soạn dữ liệu |
| Màu **ghi thẳng trong dữ liệu** (771 chỗ) | đổi bảng màu phải làm hai lượt | dữ liệu Q2 **cấm chứa mã màu**, chỉ tham chiếu tên |
| Dữ liệu nằm 3 nơi, đồng bộ tay | lệch âm thầm | một nguồn + script đồng bộ + phép kiểm |
| Chỉ gửi kết quả ở màn kết bài | mất trung bình 7 câu/bài | đã sửa — Q2 dùng lại `pushAttempts` |
| Nhật ký bất biến + `ms` sai | không xoá được, phải đánh dấu phiên bản | Q2 ghi `v: 2` ngay từ bản ghi đầu |
| Đề viết tắt kiểu điện tín | 34 câu phải viết lại | phép kiểm chặn ngay khi nhập |
| Bảng cô chỉ dựng mỗi đêm | tưởng hệ thống hỏng | đã có nút cập nhật ngay |

**Nguyên tắc xuyên suốt:** viết bộ RÀ SOÁT trước, soạn dữ liệu sau. Ở Quyển 1 mọi
lỗi nặng đều do làm ngược thứ tự này.

---

## 4 · Sáu bước, mỗi bước có cổng nghiệm thu

Không sang bước sau khi cổng chưa xanh.

### Bước 1 · Trích xuất trung thực (không diễn giải)
Bộ trích `tools/rut_quyen2.py` đọc `.docx` → JSON thô, **giữ nguyên chữ**, chỉ gắn
cấu trúc: vòng → màn → câu / bẫy / thẻ.

> **Cổng:** đếm lại từ JSON phải khớp: 314 câu · 168 bẫy · 14 thẻ · 5 bài kỹ năng.
> Cộng thêm phép kiểm "không mất chữ": tổng ký tự JSON ≥ 98% tổng ký tự nguồn.

### Bước 2 · Bộ rà soát (viết TRƯỚC khi soạn)
Chuyển thẳng các phép kiểm của Quyển 1 sang: mọi câu có mã · mã không trùng · có
cách trả lời · làm đúng được công nhận · đề không viết tắt · không chứa mã màu.

> **Cổng:** chạy bộ rà trên dữ liệu Bước 1 → phải BÁO LỖI (vì chưa có đáp án).
> Bộ rà không báo gì là bộ rà hỏng, không phải dữ liệu tốt.

### Bước 3 · Chuẩn hoá đáp án và mã bẫy
Tách đáp án từ màn 2 (đã có sẵn "Câu n: …"), gắn `answerKey`, gắn `mustPass` cho
câu bẫy, nối mã `CĐ-x.y` → `DL:KSN5Q1.Bx.My`.

> **Cổng:** 292 câu máy chấm được, mỗi câu tự trả lời đúng thì được công nhận;
> 168 mã bẫy đều trỏ tới micro có thật.

### Bước 4 · Năng lực mới của phần mềm
Bốn thứ Quyển 1 chưa có:
1. **Đồng hồ đếm ngược** + ba lượt + luật 3 phút
2. **Barem 4 mốc** — con tự tick sau khi xem đáp án
3. **Phiên tòa bẫy** — 12 ô SẬP/THOÁT mỗi vòng
4. **Chấm kép** cho đề trộn (điểm toán · điểm định dạng, hai cột riêng)

> **Cổng:** mỗi thứ có phép kiểm riêng + thử phá. Đồng hồ phải đúng cả khi con
> khoá máy giữa chừng (thử thật, không tin lý thuyết).

### Bước 5 · Hình
71 chỗ cần sơ đồ, có 48 ảnh. Hai lựa chọn ở mục 6.

> **Cổng:** không hình nào lệch bảng màu; mã kiểm khớp PNG thật.

### Bước 6 · Nối vào phần mềm
Quyển 2 mở khi Quyển 1 đạt ngưỡng. Hồ sơ bẫy tra được. Sổ cô và sổ bố mẹ gộp số
liệu hai quyển.

> **Cổng:** đóng vai học sinh đi hết 14 vòng + 4 đề trộn + 3 kỳ thi, không sót.

---

## 5 · Ước lượng khối lượng

Quyển 1 có 1 141 câu và mất phần lớn dự án. Quyển 2 có **314 câu** — bằng khoảng
**27%** — nhưng **đáp án và lời chữa đã có sẵn trong sách**, không phải soạn mới.
Đổi lại phải làm **4 năng lực mới** mà Quyển 1 không có.

Ước lượng thô: phần dữ liệu nhẹ hơn Quyển 1 đáng kể; phần phần mềm nặng hơn.

---

## 6 · Ba việc đã chốt (08/08/2026)

| Việc | Đã chốt |
|---|---|
| Nguồn hình | **Vẽ lại toàn bộ 71 sơ đồ bằng FigForge** — một nguồn hình duy nhất, đồng bộ bảng màu icon, sửa/vẽ lại được như 672 hình Quyển 1 |
| Cách chấm | **Ba tầng** — máy chấm đáp số · con tự chấm barem · con tự soi bẫy |
| Điều kiện mở | **Theo chương tương ứng** — xong chương 1 Quyển 1 thì mở Vòng 1, học xen kẽ được |

### Tiến độ

- [x] **Bước 1 · Trích xuất trung thực** — cổng 29/29 xanh
- [x] **Bước 2 · Bộ rà soát** — 26 phép kiểm, bắt được cả lỗi của chính nó
- [x] **Bước 3 · Chuẩn hoá đáp án** — 102 câu máy chấm · 212 câu tự luận
- [x] **Bước 4 · Năng lực mới** — đồng hồ · barem 4 mốc · phiên tòa · chấm kép (44 phép kiểm)
- [x] **Bước 5 · sơ đồ** — 53 sơ đồ vẽ bằng FigForge, gắn vào 21 khối
- [x] **Bước 6 · Nối vào phần mềm** — đã kiểm end-to-end trên trình duyệt

### Kết quả đo được (khác kế hoạch ban đầu, ghi đúng số thật)

| | Kế hoạch ước | Thực tế |
|---|---|---|
| Câu máy chấm | 292 | **102** |
| Câu tự luận | 22 | **212** |

Vì sao lệch: kế hoạch đếm "câu có đáp số gọn" theo ĐỀ BÀI, nhưng cái quyết định là
có rút được đáp số CHẮC CHẮN từ lời chữa văn xuôi hay không. Soi mắt 20 mẫu mới lộ
ra câu đòi hai giá trị ("Tổng 84, hiệu 16 — tìm hai số") bị rút thành một số, con
viết đủ "34 và 50" sẽ bị chấm sai. Đã loại hẳn dạng ấy. Thà ít mà đúng.

---

## 8 · Bước 5 — sơ đồ (đã xong)

Hoá ra nhẹ hơn dự tính rất nhiều. Sợ phải "mô tả tay 71 sơ đồ", nhưng khi mở cấu
trúc `.docx` ra thì **tất cả đều cùng một hình dạng**: một bảng hai cột, ô đầu ghi
"TÌNH HUỐNG", ô bên cạnh là tiêu đề, các hàng sau là cặp (nhãn · lời giải thích).

Nên chỉ cần **một nguyên mẫu** `arch_q2.bang_chien_thuat`, không phải 71 mô tả tay.
Khác hẳn Quyển 1 vốn cần 25 nguyên mẫu vì mỗi hình toán một kiểu.

| | |
|---|---|
| Mốc "TÌNH HUỐNG" trong sách | 67 |
| Trừ bảng phiên tòa (đã dựng thành giao diện bấm được) | −14 |
| **Sơ đồ đã vẽ** | **53** |
| Gắn vào 21 khối · trại huấn luyện | 48 · 5 |

Chiều cao tính theo SỐ DÒNG THẬT sau khi ngắt chữ: bảng 4 hàng và bảng 12 hàng mà
cùng chiều cao thì một cái rỗng toác, một cái chữ đè nhau.

---

## 6b · Ba việc đã hỏi (giữ lại để tra sau)

### (a) Hình minh hoạ — 71 chỗ, có 48 ảnh
| | Ưu | Nhược |
|---|---|---|
| **Dùng lại 48 ảnh trong sách** | nhanh, đúng ý tác giả | lệch bảng màu mới; thiếu 23 chỗ; không vẽ lại được |
| **Vẽ lại bằng FigForge** | đồng bộ màu, sửa được, đủ 71 | tốn công, phải mô tả lại từng sơ đồ |
| **Lai: dùng ảnh có sẵn, đổi màu; vẽ mới 23 chỗ thiếu** | cân bằng | hai nguồn hình, khó nhất quán |

### (b) Cách chấm
Tôi đề xuất **chấm ba tầng** (mục 2). Cần bác xác nhận, vì nó quyết định cả cách
gating lẫn số liệu cô giáo nhìn thấy.

### (c) Điều kiện mở Quyển 2
| Lựa chọn | Ý nghĩa |
|---|---|
| Học hết 168 micro Quyển 1 | đúng tinh thần sách, nhưng chặn lâu |
| Xong chương tương ứng | vòng 1 mở khi xong chương 1 — học xen kẽ được |
| Mở tự do | ai cũng vào luyện thi được |

---

## 7 · Việc KHÔNG làm ở giai đoạn này

- Không sửa nội dung toán của sách. Nếu rà thấy lỗi, **báo cáo** chứ không tự đổi.
- Không gộp Quyển 2 vào tiến độ Quyển 1 — hai sổ riêng, một bảng tổng.
- Không bỏ phần tự chấm để lấy số liệu đẹp. Tự chấm chính là bài học của Quyển 2.
