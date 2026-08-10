# Khảo sát — Toán lớp 4 (Bước 0)

Nguồn: `docs/KSN4_SACH_HOAN_CHINH_Ky_Su_Nhi_Lop4.docx` · 6,8 MB · 3 253 khối
(2 784 đoạn văn · 469 bảng · 100 chỗ neo ảnh).

> **Kết luận một dòng:** đây là quyển ĐỀU NHẤT trong bốn quyển. Mọi con số đếm được
> đều tròn trịa: 44 bài × (9 luyện tập + 5 quiz), 44 × 4 bước, 616 đáp án khớp 1:1.
> Chỗ đáng sợ không nằm ở bóc tách mà ở **BẢNG TỰ SOI** và **HẠT MẦM NĂM NGOÁI**.

---

## 1 · Đếm được bao nhiêu

| | |
|---|---|
| chương | **11** |
| bài | **44** |
| ôn tập | **11** (mỗi chương một cái; **không có ải** như lớp 3) |
| câu luyện tập | **396** = 44 × 9 |
| câu quiz | **220** = 44 × 5 |
| **tổng câu trong bài** | **616** |
| đáp án bài | **616** — khớp 1:1, không thiếu một câu |
| câu ôn tập (đề chính) | **124** |
| câu đề B | **112** |
| đáp án ôn tập | 124 + 112, khớp 1:1 |
| chỗ neo ảnh | **100** |
| tệp ảnh | **57** |

## 2 · Khuôn một bài — mười mục CỐ ĐỊNH ①…⑩

Kiểm bằng máy: **44/44 bài có đúng ①…⑩, mỗi mục đúng một lần, đúng thứ tự.**
Không bài nào lệch. Tiêu đề mục cũng chỉ có **một biến thể** cho cả 9 mục
(riêng ② có 44 biến thể vì đuôi là tên câu chuyện — đó là chủ ý của sách).

| mục | tên | dạng khối | dùng làm gì |
|---|---|---|---|
| ① | MỤC TIÊU BÀI HỌC — Sau bài này con sẽ: | bảng | `objective` |
| ② | CHUYỆN MỞ BÀI — Đơn hàng số N: … | đoạn + **ảnh** | màn `hook` |
| ③ | PHÂN TÍCH & DỰNG MÔ HÌNH — bàn vẽ của kỹ sư | `▸ NHỊP 1 · DỊCH` + bảng CHO GÌ / HỎI GÌ / ĐẠI LƯỢNG | màn `explain` đầu |
| ④ | KHÁM PHÁ CÙNG SU KEM | `▸ NHỊP 2 · GIẢI` + **Bước 1-4** + bảng MẸO THÁM TỬ | `statements` · `lecture.screens` |
| ⑤ | LẮP VỀ CUỘC SỐNG & SOI | `▸ NHỊP 3 · LẮP + NHỊP 4 · SOI` + bảng | màn `explain` cuối |
| ⑥ | LỜI GIẢI MẪU TRÌNH BÀY VỞ | `Đề bài:` + bảng 2 cột | `workedExample` |
| ⑦ | TRÍ LONG ƠI, NHẦM RỒI! | bảng | màn `trap` · `misconceptions` |
| ⑧ | LUYỆN TẬP 3 MỨC SAO | `★ MỨC 1` / `★★ MỨC 2` / `★★★ MỨC 3` + `Câu N.` | `practice.pools` |
| ⑨ | QUIZ — CON HIỂU BÀI CHƯA? | bảng + **ảnh nhiệt kế** | `assessment.items` |
| ⑩ | GÓC BỐ MẸ | bảng | `parentNote` |

**Bước trong ④: đúng `Bước N —`, 176 lần = 44 × 4.** Không có bài nào đặt tên khác.
Đây là khác biệt lớn nhất so với lớp 3 (12 tên bước, 26 bước bốc hơi khi dùng mẫu lớp 2).
`R_BUOC` của `khuon_chung.py` đã biết `Bước` từ lớp 2 nên **không phải thêm tên nào**.

**Ba mức luyện tập chia 9 câu:** ★ MỨC 1 (câu 1-3) · ★★ MỨC 2 (câu 4-7) · ★★★ MỨC 3
(câu 8-9) — ánh xạ thẳng sang `warmup` / `standard` / `challenge`.

**Quiz: 44/44 bài đúng 2 Đúng/Sai + 3 trắc nghiệm ba phương án A/B/C.**
Dạng: `Câu N (Đúng/Sai?): …` và `Câu N: … A. …  B. …  C. …`.
→ cả 220 câu quiz đều chấm máy được, y như lớp 3.

## 3 · Đáp án nằm ở CUỐI CHƯƠNG — bẫy 5 và 6 tái xuất

Thứ tự trong một chương: `bài … bài · ÔN TẬP · ĐÁP ÁN CHI TIẾT — GIỌNG SU KEM ·
lời chốt chương · trang mở chương sau`.

Cắt bài "tới tiêu đề bài kế tiếp" là nuốt trọn **cả bộ đáp án của chương** vào mục ⑩
của bài cuối — đúng cái bẫy đã làm lộ đáp án cho bố mẹ ở lớp 2.

**Mã đáp án có tiền tố dấu trang** (bẫy 44):

```
B1   ĐÁP ÁN BÀI 1 — Những con số khổng lồ quanh nhà
Ô1   ĐÁP ÁN ÔN TẬP 1 — Khai trương xưởng (Đề chính)
Ô1B  ĐÁP ÁN ĐỀ B
```

Mỗi câu **một đoạn văn riêng** — dạng dễ bóc nhất trong bốn quyển:
`C1: …` (luyện tập) · `Quiz C1: …` (quiz) · `B1: …` (đề B).

⚠ **Khối đáp án phải đóng khi gặp BẢNG, không chỉ khi gặp đoạn văn.** Bộ đếm thử đầu
tiên của tôi đọc ra 22 đáp án cho đề B (thật ra 10): nó chạy xuyên bảng mở chương sau
rồi ăn luôn `B1.` `B2.` của phần luyện tập bài kế. Cùng họ với bẫy 5.

## 4 · Ôn tập — ba phần ngăn bởi mốc `✦`

Y hệt cấu trúc lớp 3, và **đều hơn**:

```
tiêu đề (Đạt a/b câu) · Luật chơi · ảnh
★ / ★★ / ★★★ CHẶNG … — Câu a-b        ← tên chặng đổi theo chủ đề, KHÔNG dùng để cắt
Câu 1. … Câu N.                        ← LUÔN là "Câu", không có Vụ/Phòng/Đảo như lớp 3
✦  BẢNG TỰ SOI — TRƯỢT … NÀO, ÔN BÀI ĐÓ
✦  ĐỀ B — <tên đổi theo chủ đề>        ← B1. … B10. mỗi câu MỘT đoạn
✦  SỔ ĐƠN HÀNG — BÀI CỦA RIÊNG CON     ← đề mở, không chấm
```

- **Ngưỡng đạt**: `Đạt a/b` đều đặn cả 11 ôn tập (8/10 hoặc 10/12) — vẫn nhận theo
  **hình dạng `a/b`**, đừng liệt kê động từ (bài học lớp 3).
- **Đề B luôn 10 câu**, trừ ôn tập 2 có 12.
- Tên chặng (`★★ QUẦY BÁNH`, `★★ TỦ SÁCH CŨ`) đổi mỗi ôn tập và **có khi hai chặng
  cùng hai sao** — đừng dùng số sao làm khoá.

### BẢNG TỰ SOI — chỗ nguy nhất cả quyển

Cả bảng nằm gọn trong **một ô bảng**, các mối nối viết nối đuôi nhau. Năm dạng, mẫu
chỉ biết dạng đầu là mất mối nối lặng lẽ:

| dạng | ví dụ thật |
|---|---|
| chuẩn | `Câu 1, 2, 3 → thuộc Bài 1 (…)` |
| có `và` | `Câu 1, 2, 3 và Câu 12 → thuộc Bài 5 (…)` |
| **không có chữ "thuộc"** | `Câu 12 → Bài 19 mức ★★★ (…)` |
| **hai bài** | `Câu 10 → ghép Bài 9 + Bài 10` |
| **không bài nào** | `Câu 10 → tổng hợp cả chương (…)` |

→ `veCau` phải là **danh sách** mã bài (lớp 3 đã học bài này). Dạng "tổng hợp cả chương"
ghi `canCu: 'chuong'` và trỏ về đủ các bài của chương — có thật, không phải lỗi.
Chốt bắt buộc: **mọi câu 1..N đều phải có mối nối**, thiếu một câu là kêu.

## 5 · HẠT MẦM NĂM NGOÁI — đường lùi về lớp 3, và cái bẫy của nó

44/44 bài có dòng `HẠT MẦM NĂM NGOÁI:` trong bảng tiêu đề bài. Nhưng:

> ⚠ **`Bài N` trần KHÔNG phải bài lớp 3 — nó là bài LỚP 4 ở trước.**
> *"Bài 19 êm đẹp vì đề khai sẵn cả tổng lẫn hiệu"* (bài 20) nói về bài 19 **lớp 4**.
> *"y như định luật bất biến con vừa học ở Bài 36"* (bài 37) — lớp 3 **không có** bài 36.

Chỉ đếm `Bài N` nằm trong câu có nêu **"Lớp 3"**:

| căn cứ | số bài | ghi chú |
|---|---|---|
| `sach` — nêu đích danh *"Lớp 3, ở Bài N"* | **14** | 1,2,4,5,6,7,8,9,11,13,14,15,16,19 |
| còn lại — chỉ nhắc chủ đề hoặc nhắc bài lớp 4 | **30** | phải soát tay, ghép theo tên bài |

Mẫu naive (bắt mọi `Bài N`) cho ra 32/44 "đích danh" — **trong đó 18 cái là trỏ nhầm
sang chính lớp 4**, và một cái trỏ ra ngoài phạm vi (lớp 3 chỉ có 34 bài).
Đúng loại "trỏ sai còn tệ hơn không trỏ" mà chuẩn mục 4 cảnh báo.

Dải cũng phải nở: `Lớp 3, ở Bài 4 và Bài 10-11` → 4, 10, 11.

## 6 · Hình — 57 tệp, 100 chỗ neo

Đếm theo **chỗ neo**, không đếm theo tệp (bẫy 42). Kiểm kín:

| nhóm | chỗ neo | tệp |
|---|---|---|
| ② CHUYỆN MỞ BÀI — mỗi bài một hình toán | 44 | 44 |
| ⑨ QUIZ — **nhiệt kế, một tệp dùng 44 lần** | 44 | 1 |
| ôn tập — hình "Luật chơi" | 11 | 11 |
| bìa / hướng dẫn dùng sách | 1 | 1 |
| **tổng** | **100** | **57** |

**Ảnh gốc lớp 4 là HÌNH TOÁN THẬT, không phải trang trí** — khác hẳn lớp 3. Hình mở
bài 1 vẽ đúng bảng hàng - lớp với 5 ô chữ số và hai nhãn lớp. Nhưng:

- phải **vẽ lại bằng `figforge`** theo bảng màu thương hiệu, không chép màu sách;
- hình mở của sách **chứa sẵn đáp án** (*"đọc theo lớp: hai mươi bốn nghìn | ba trăm
  năm mươi tám"*) → bản màn mở phải là **bản ĐỀ**, bỏ hết dấu vết đáp án (chuẩn mục 6 luật 3);
- **nhiệt kế làm THÀNH PHẦN GIAO DIỆN**, không phải PNG — y như `image3.png` của lớp 3;
- ảnh gốc **không phủ** hình giảng (mục ④) và hình bài tập (mục ⑧) — hai loại ấy phải
  tự dò và tự vẽ (bẫy 43: lớp 3 vẽ nhiều hơn lớp 2 dù ảnh gốc ít hơn).

## 7 · Sách viết mấy kiểu cho cùng một thứ (bẫy 7)

Ít bất ngờ thay — **gần như không có**:

| thứ | số cách viết |
|---|---|
| tên mục | 1 (trừ ② là tên chuyện) |
| tên bước | 1 — `Bước N —` |
| tên nhịp | 3 cố định — DỊCH · GIẢI · LẮP+SOI |
| tên mức | 3 cố định — `★ MỨC 1` … |
| tên câu | 1 — `Câu N.` |
| ngưỡng đạt | 1 — `Đạt a/b` |
| **tên chặng ôn tập** | **41 biến thể** — đổi theo chủ đề, KHÔNG dùng làm mốc cắt |
| **tên ĐỀ B** | **11 biến thể** (`— LÔ ĐƠN HÀNG THỨ HAI`, `— PHIÊN PHÚC THẨM`…) → neo vào `✦  ĐỀ B` |

## 8 · Việc phải làm, suy từ khảo sát

1. Bộ trích cắt theo **bảng tiêu đề bài**, đóng khối tại `ĐÁP ÁN CHI TIẾT` — không cắt
   theo "tiêu đề bài kế tiếp".
2. Đáp án bóc riêng, khoá `<mã bài>#C<n>` và `<mã bài>#Quiz<n>` để ôn tập không đè bài.
3. BẢNG TỰ SOI: đọc theo cấu trúc, `veCau` là danh sách, chốt phủ đủ 1..N.
4. Đường lùi lớp 3: 14 dòng `sach` lấy máy, **30 dòng soát tay**, khai cả dòng `khong`.
5. Hình: 44 màn mở (bản ĐỀ) + hình giảng theo bước + hình bài tập — dò như lớp 3.
6. Nhiệt kế và thẻ "Luật chơi" làm giao diện, không làm ảnh.
7. Ô nhập: quyển đọc chậm → **chỉ ô SỐ hoặc BẤM CHỌN**, chấm máy ≥ 85%.
