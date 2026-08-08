# Lớp 2 — việc còn lại (bàn giao cho phiên sau)

**Điểm dừng:** `d0fc917` · đã deploy · 556 phép kiểm xanh · 37/37 mục trước deploy.
**Đã xong:** 33 bài chính · lời văn đã làm dễ hiểu (câu dài 13% → 6%) · màn chọn
chương trình · phòng học lớp 2.

---

## Ba việc còn thiếu

### 1 · 75 hình trong sách  ⚠ QUAN TRỌNG NHẤT

Đã khảo sát: **hình lớp 2 KHÁC hẳn hình Quyển 2 lớp 5**.

| | Quyển 2 lớp 5 | Lớp 2 |
|---|---|---|
| Loại | sơ đồ chiến thuật (bảng chữ) | **hình toán thật sự** |
| Thiếu hình thì | vẫn làm bài được | **KHÔNG hiểu được đề** |
| Hình dạng | đều một khuôn (bảng 2 cột) | mỗi hình một kiểu |

Ví dụ `image1.png`: đoàn tàu 6 toa ghi `5 · 10 · ? · 20 · 25 · ?`, đề bảo tìm nhịp
tàu rồi điền. **Không có hình thì bé không biết điền vào đâu.**

→ Nên đây là việc phải làm TRƯỚC hai việc kia. Kích thước 1185px, cùng ngôn ngữ
thị giác với FigForge nhưng **không cùng một khuôn** như 53 sơ đồ Quyển 2 — nên
không dùng lại được `arch_q2.bang_chien_thuat`, phải khảo sát nhóm hình rồi dựng
vài nguyên mẫu (đoàn tàu, ngôi nhà trăm-chục-đơn vị, hình học…).

**Việc đầu tiên của phiên sau:** phân loại 75 hình thành mấy nhóm, đếm mỗi nhóm
bao nhiêu cái. Có thể chỉ cần 5–8 nguyên mẫu là phủ hết.

Ảnh đã trích sẵn để xem nhanh (thư mục tạm, không nằm trong kho):
`scratchpad/l2img/image1.png … image75.png` — hoặc trích lại bằng `zipfile` từ
`docs/Toan_Tu_Duy_Lop2_Ban_hoan_chinh.docx`, phần `word/media/`.

### 2 · 8 bài ôn tập chương
Sách có "Ôn tập N · …" cuối mỗi chương, kèm **Bảng tự soi** (sai câu nào ôn bài
đó) và **Đề B** để làm lại. Bộ trích hiện tại (`tools/rut_lop2.py`) chỉ bắt 33 bài
chính, chưa bắt ôn tập.

Bảng tự soi đáng giá: nó là bản đồ *câu sai → bài cần ôn*, giống trục
`CĐ-x.y ↔ Bx.My` đã dùng rất hiệu quả ở lớp 5.

### 3 · 3 ải cuối sách
"Ải 1 ★ Khởi động · Ải 2 ★★ Chiến binh · Ải 3 ★★★ Trùm cuối", có kèm đáp án.
Vai trò giống kỳ thi thử của lớp 5.

Tổng câu hỏi của mục 2 + 3: khoảng **106 câu** (387 dòng `Câu n.` trong sách trừ
281 câu đã lấy).

---

## Chạy lại dây chuyền

```bash
python3 tools/lam_lop2.py    # trích thô → làm dễ hiểu → dựng dữ liệu
cd web && npm test           # cổng nghiệm thu soi lại
```

Ba bước PHẢI chạy liền nhau. Chạy lẻ `chuan_lop2.py` mà quên `de_hieu_lop2.py` thì
app hiện lại lời văn khó của sách gốc **mà không có gì báo**.

## Nhắc lại hai bẫy đã dính, đừng dính lại

- **Ghi đè âm thầm:** ở Quyển 2 lớp 5, chạy lại bộ dựng dữ liệu đã xoá sạch phần
  `soDo` vừa gắn — dữ liệu vẫn hợp lệ, bài vẫn chạy, chỉ mất hết hình. Nếu gắn
  hình lớp 2 theo cách tương tự thì phải cho vào `tools/lam_lop2.py` ở **bước cuối**.
- **Bảng viết tay khớp nguyên văn:** `VIET_LAI` trong `de_hieu_lop2.py` khớp theo
  đúng từng chữ. Sách sửa một dấu phẩy là câu ấy im lặng giữ nguyên bản khó —
  đã có cảnh báo, đừng bỏ qua khi nó kêu.

## Còn treo ở lớp 5 (chưa gấp)

- 106 câu lớp 2 vẫn dài hơn 20 chữ — phần lớn là lời kể có hội thoại, tự nhiên dài.
- `firebase-functions` v5 → v7 (breaking changes).
- Firebase Storage chưa bật (chỉ dùng cho ảnh đại diện).
