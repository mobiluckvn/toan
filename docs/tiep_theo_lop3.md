# Điểm dừng — Toán lớp 3

Cập nhật 2026-08-09. Đọc tệp này TRƯỚC, rồi mới đọc `CHUAN_DUA_SACH_VAO_APP.md`.

Nguồn: `docs/Toan_Tu_Duy_Lop3_Cuoc.docx` · 34 bài · 8 chương · 8 ôn tập · 3 ải.

---

## Đã xong — chạy được, có phép kiểm giữ

| bước | việc | kết quả |
|---|---|---|
| 0 | khảo sát | `docs/khao_sat_lop3.md` |
| 1 | phân loại hình | `docs/phan_loai_hinh_lop3.md` |
| 2a | bộ trích thô | `tools/rut_lop3.py` → `data/lop3_tho.json` — **34 bài · 477 câu** |
| 2b | bóc đáp án | `tools/dapan_lop3.py` → `data/lop3_dapan.json` — **477 đáp án, khớp 1:1** |
| — | đường lùi về lớp 2 | `data/lop3_gan_lop2.json` — 34 bài (21 `sach` · 11 `chuDe` · 2 `khong`) |

Phép kiểm: `web/test/lop3.test.mjs` (11 phép). Chạy `cd web && npm test`.

---

## VIỆC 1 — chữa bộ tách câu ôn tập  ⚠ ĐANG DỞ

`tools/ontap_lop3.py` → `data/lop3_ontap.json`. Bóc được 8 ôn tập · 3 ải · mối nối
từng câu về từng bài. **Nhưng 5/8 ôn tập tách THỪA 1–5 câu** so với số sách nêu:

```
Ôn tập 2: 13 câu, sách nói 12       Ôn tập 5: 13 câu, sách nói 12
Ôn tập 3: 12 câu, sách nói 10       Ôn tập 6: 13 câu, sách nói 8
Ôn tập 4: 14 câu, sách nói 10
```

Ôn tập 1, 7, 8 đã khớp. Công cụ IN CẢNH BÁO cho từng chỗ lệch, không im lặng ghi bừa.

**Hai giả thuyết chưa kiểm:**
1. lời chữa đề trong cùng khối cũng đánh số (`Câu 4, 5 → thuộc Bài 2` đã rào, nhưng
   có thể còn dạng khác)
2. vài ôn tập không có mốc `✦ ĐỀ B` rõ ràng nên câu Đề B vẫn gộp vào đề chính

**Cách làm đúng:** in nguyên văn thân từng khối ôn tập lệch rồi ĐỌC, đừng vá mẫu
regex theo cảm tính. Tôi đã vá ba lượt liên tiếp và mỗi lượt lộ thêm một dạng mới —
đó là dấu hiệu phải đọc chứ không phải đoán.

**Ba dạng đã biết, đã rào, đừng làm hỏng khi sửa:**
- tiêu đề ải có tiền tố `①②③` — mẫu `^ẢI` trượt hết
- mỗi ôn tập đặt tên câu theo CHỦ ĐỀ: `Câu` · `Vụ` · `Phòng` · `Đảo` · `Mã` · `Trạm` · `Cửa`
- số câu cần đạt KHÔNG cố định: `Đạt 8/10 câu` · `Phá 6/8 vụ án` — đọc từ chính dòng ấy

---

## VIỆC 2 — `tools/chuan_lop3.py` dựng dữ liệu bài học

Chép `tools/chuan_lop2.py`. Bảng khớp mục ①…⑧ **y hệt lớp 2** (xem `khuon_chung.py`,
hằng `NOI_DUNG_HINH`). Hai trường phải THÊM so với lớp 2:

| trường | nguồn | dùng làm gì |
|---|---|---|
| `hatMam` | đã có trong `lop3_tho.json` | lời nối ngược về lớp 2, hiện ở màn kết bài |
| `ganLop2` | `data/lop3_gan_lop2.json` | nút **"Học lại bài lớp 2"** — việc bác dặn |

Nút ấy chưa làm. Chỗ đặt: `FinaleCard.jsx` (trang kết bài) và màn khi bé không đạt
sát hạch. Lấy `ve[0]` làm đích; dòng `canCu: 'khong'` thì KHÔNG hiện nút.

Nhớ mục 6 của chuẩn khi dựng màn mở: lời mở là MỘT CÂU nêu bài toán, lấy từ dòng
`Đề bài` của mục ④, và câu dẫn chỉ giữ khi không chứa con số.

---

## Sau đó — Bước 3 · vẽ hình (phần nặng nhất)

Xem `docs/phan_loai_hinh_lop3.md`. Con số đáng nhớ: sách cho **46 hình toán** nhưng
gần hết nằm ở màn mở; **mục giảng chỉ 6 hình cho 34 bài**, bài tập KHÔNG có hình nào.
Việc vẽ nhiều hơn lớp 2 chứ không ít, dù ảnh gốc ít hơn (bẫy 43).

- 13 nhóm nguyên mẫu; **9 nhóm dùng lại được** nguyên mẫu lớp 2 đã có
- phải dựng mới ~5: Ven hai vòng · lịch tháng · cân & ống đong · tiền Việt · biểu thức có ngoặc
- `image3.png` (nhiệt kế, dùng 34 lần) làm **component**, không phải PNG
- vẽ **cả ba loại hình ngay từ đầu** — giảng · màn mở · bài tập (`item:CX` + `:giai`)

---

## Đừng quên

- Tiền tố mã bài: `DL:KSN3.` — chưa kiểm trùng với `DL:KSN2.` / `DL:KSN5Q1.` / `DR:KSN5Q2.`
- Khai sổ đăng ký (`data/chuong_trinh.json`): nhớ `loai: 'hoc'` và `donVi`
- 44 cái bẫy trong chuẩn — sách lớp 3 đã dính lại bẫy 5, 6, 7 y như lớp 2
