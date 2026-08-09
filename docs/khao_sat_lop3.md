# Khảo sát — Toán Tư Duy lớp 3 · Cuộc phiêu lưu mới của Su Kem

Nguồn: `docs/Toan_Tu_Duy_Lop3_Cuoc.docx` · 2,1 MB · 2 446 đoạn có chữ · 47 ảnh nhúng
(80 chỗ neo ảnh trong `document.xml`, tức là **có ảnh dùng lại ở nhiều chỗ**).

Đây là **Bước 0** của `CHUAN_DUA_SACH_VAO_APP.md` mục 10. Khảo sát sai thì mọi bước
sau đều sai, nên trả lời hết bảng dưới trước khi gõ dòng bộ trích nào.

---

## 1 · Khối lượng

| | lớp 3 | lớp 2 (để so) |
|---|---|---|
| chương | 8 | 8 |
| bài học | **34** | 33 |
| ôn tập | 8 | 8 |
| ải cuối sách | 3 | 3 |
| mục mỗi bài | 8 (①…⑧) | 8 (①…⑧) |
| mức sao luyện tập | ★ 34 · ★★ 34 · ★★★ 34 | như vậy |
| ảnh nhúng | 47 | 75 |
| sticker danh hiệu | 12 | — |

**Kết luận: khuôn giống lớp 2 gần như hoàn toàn.** Dây chuyền `rut_lop2.py` →
`chuan_lop2.py` → `khuon_chung.py` dùng lại được, chỉ đổi bộ trích và bảng khớp mục.

## 2 · Tám mục cố định của mỗi bài

```
①  MỤC TIÊU BÀI HỌC — Sau bài này con sẽ:
②  CHUYỆN MỞ BÀI — <tên tình huống>
③  KHÁM PHÁ CÙNG SU KEM — <tên>
④  VÍ DỤ MẪU — Trình bày vào vở thế nào?
⑤  TRÍ LONG ƠI, NHẦM RỒI!
⑥  LUYỆN TẬP 3 MỨC SAO
⑦  QUIZ — CON HIỂU BÀI CHƯA?
⑧  GÓC BỐ MẸ
```

Khớp mục sang khuôn chung **y như lớp 2** (`NOI_DUNG_HINH` trong `khuon_chung.py`):
① → `objective`/`mantra` · ② → màn `hook` · ③ → `knowledgeCore` + màn `explain` ·
④ → `workedExample` · ⑤ → `misconceptions` + màn `trap` · ⑥ → `practice.pools` ·
⑦ → `assessment.items` · ⑧ → `parentNote`.

**Hai mục lớp 2 KHÔNG có:**

- `Dạng gốc: …` (34 dòng) — ngay dưới tiêu đề bài, cho biết dạng toán chuẩn. Lớp 2
  cũng có, đổ vào `dangGoc`.
- `HẠT MẦM NĂM NGOÁI: …` (35 dòng) — nối ngược về bài lớp 2 tương ứng. **Mới.**
  Đây là thứ đáng giữ: nó là đường dẫn giữa hai quyển, nên cần một trường riêng
  (`hatMam`) chứ đừng nhét vào lời giảng.

## 3 · Đáp án nằm ở đâu

Một khối riêng cuối sách: `ĐÁP ÁN CHI TIẾT — GIỌNG SU KEM`, bên trong:

- `B1  ĐÁP ÁN BÀI 1 — Tòa tháp Nghìn` … 34 mục
- `ĐÁP ÁN ÔN TẬP …` × 8
- `Đáp án ba ải — giọng Su Kem`

⚠ **Đúng bẫy số 6 của chuẩn**: đáp án ôn tập cũng đánh `C1, C2…` nên nếu bộ trích
không đóng bài đang mở khi gặp tiêu đề đáp án ôn tập thì **đáp án ôn tập đè đáp án
bài**. Lớp 2 đã mất 60 lời giải vì lỗi này. Cách rào đã có sẵn trong `rut_lop2.py`.

⚠ Tiêu đề đáp án có **tiền tố dấu trang** (`B1  `, `B10  `) — mẫu neo `^ĐÁP ÁN BÀI`
trượt hết. Phải cho phép tiền tố.

## 4 · Sách không nhất quán ở đâu (bẫy số 7)

| thứ | các cách viết gặp trong sách |
|---|---|
| câu hỏi | `Câu 1.` (413) · `Câu 1 (Đúng/Sai?):` (70) · `Câu 1:` (102) |
| bước trong mục ③ | `Bước 1` (101) · `Nhịp 1` (4) |
| tiêu đề bài | mục lục: `Bài 6 · Phép chia có dư chính danh27` (chữ thường + **số trang dính liền**) · thật: `Bài 6 · PHÉP CHIA CÓ DƯ CHÍNH DANH` (in hoa) |

Mẫu tách câu phải nhận **cả ba** dấu ngăn `.` `:` `(`. Lớp 2 từng bỏ sót 165 câu quiz
vì mẫu chỉ đòi dấu chấm.

⚠ **Bẫy chữ Việt mới, chưa có trong chuẩn:** dải `à-ỹ` (U+00E0–U+1EF9) **chứa cả
`Đ` `Ơ` `Ư` VIẾT HOA** (U+0110, U+01A0, U+01AF). Nên phép thử "dòng này in hoa" viết
kiểu `[^a-zà-ỹ]+$` **trượt mọi tiêu đề có Đ/Ơ/Ư** — mà tiếng Việt thì tiêu đề nào
chẳng có. Phải so bằng `s == s.upper()` hoặc liệt kê dải chữ thường cho đúng.

## 5 · Kỳ sát hạch

- Ôn tập 1…8, mỗi bài 10 câu, đạt 8/10 nhận sticker danh hiệu.
- Ba ải cuối sách, có khối đáp án riêng.
- **KHÔNG có Bảng tự soi.** Lớp 2 có, và `chuan_lop2.py` dùng nó để trỏ câu ôn tập
  sai về đúng bài cần học lại. Lớp 3 phải **suy ra mối nối ôn tập → bài** bằng cách
  khác: ôn tập nằm cuối chương nên mặc định trỏ về các bài trong chương ấy, rồi soát
  tay từng câu. Đây là việc phát sinh so với lớp 2 — đừng bỏ qua, thiếu nó thì bé làm
  sai không biết học lại bài nào.

## 6 · Hình — phải phân loại trước khi vẽ (Bước 1)

47 ảnh, 80 chỗ neo. Chưa phân loại. Theo chuẩn mục 10 · Bước 3, phải tính **cả ba
loại hình ngay từ đầu**, đừng lặp lại lượt lớp 2 (45 trên 120 hình phải làm lượt hai):

1. **hình giảng** — neo theo bước trong mục ③
2. **hình màn mở** — bài hình học bắt buộc có; là bản ĐỀ, bỏ hết đáp án
3. **hình bài tập** — cặp `item:CX` + `item:CX:giai` cho mọi câu mà đề MÔ TẢ một hình

Cách dò loại 3 bằng máy đã ghi ở chuẩn mục 10 · Bước 3.

## 7 · Việc còn phải làm trước khi gõ bộ trích

- [ ] Đối chiếu 47 ảnh với 80 chỗ neo → mỗi ảnh thuộc bài nào, mục nào, sau bước nào
- [ ] Phân 47 ảnh thành nhóm nguyên mẫu (lớp 2 ra 17 nhóm cho 75 hình)
- [ ] Quyết mối nối ôn tập → bài, thay cho Bảng tự soi mà lớp 3 không có
- [ ] Chốt tiền tố mã bài: `DL:KSN3.` — kiểm không trùng và không là tiền tố của mã khác
