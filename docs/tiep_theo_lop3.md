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
| 2c | ôn tập & ải | `tools/ontap_lop3.py` → `data/lop3_ontap.json` — **8 ôn tập · 3 ải · 114 câu · 84 câu đề B · mối nối đủ 84/84 câu, cả 8 ôn tập đều `canCu: sach`** |
| 3 | dựng bài học | `tools/chuan_lop3.py` → `data/lop3/` — **34 bài · 477 câu · 100% có lời chữa · 170 câu chấm máy** |
| — | đường lùi về lớp 2 | `data/lop3_gan_lop2.json` — 34 bài (21 `sach` · 11 `chuDe` · 2 `khong`) |

Phép kiểm: `web/test/lop3.test.mjs` (25 phép). Chạy `cd web && npm test`.

---

## Bài học từ VIỆC 1 (đã xong) — đọc trước khi vá bất kỳ bộ tách nào

Triệu chứng cũ: 5/8 ôn tập tách THỪA 1–5 câu. Tôi đã đoán mẫu tách câu hỏng. **Sai.**
In nguyên văn thân khối ra đọc thì mọi câu thừa đều là một dòng **BẢNG TỰ SOI** bị
nhận nhầm: mẫu mối nối trượt → dòng rơi xuống mẫu câu hỏi ở dưới → `Câu 6 và câu 11
→ thuộc Bài 7` hoá ra câu hỏi số 6.

Cái THỪA thì bộ đếm kêu. Ba hỏng câm đi kèm mới đáng sợ, không phép đếm nào bắt:

- **ôn tập 6** trượt cả 5 dòng (sách viết `→ vũ khí ĐI LÙI (Bài 22)`, không có chữ
  "thuộc") → tụt xuống `canCu: chuong`, mỗi câu trỏ về **cả 5 bài** của chương
- **ôn tập 8** nhét cả 3 mối nối vào **một dòng**, mẫu cũ chỉ lấy cái đầu → 5/10 câu
  mất đường về
- **ôn tập 4** và **7**: `tong` không đọc được (`Nhập đúng 9/12 mã` · `Nghiệm thu
  8/10 phòng` — mẫu chỉ biết `Đạt|Phá|Vượt`) nên lấy mặc định 10; ôn tập 7 đúng nhờ
  ăn may, ôn tập 4 báo "sách nói 10" trong khi sách nói 12

**Cách chữa đã dùng — đọc CẤU TRÚC, đừng dò từng dòng.** Mỗi ôn tập luôn có ba phần
ngăn bởi hai mốc `✦`: `thân đề → ✦ BẢNG TỰ SOI → ✦ ĐỀ B`. Ở phần nào chỉ dùng mẫu của
phần ấy. Dòng mối nối hết cửa rơi xuống thành câu hỏi; mẫu trượt thì mất mối nối và
bộ đếm kêu, chứ không đẻ ra câu hỏi ma.

**Dạng đã rào, đừng làm hỏng khi sửa:**
- tiêu đề ải có tiền tố `①②③` — mẫu `^ẢI` trượt hết
- tên câu theo CHỦ ĐỀ: `Câu` · `Vụ` · `Phòng` · `Đảo` · `Mã` · `Trạm` · `Cửa`
- ôn tập 6 gọi đề B là `✦ TẬP HỒ SƠ B`, không phải `✦ ĐỀ B`
- ngưỡng đạt nhận theo **hình dạng `a/b`** trong phần mở đầu, không liệt kê động từ —
  liệt kê thì sót, và sót lặng lẽ
- đề B nhồi nhiều câu trên một dòng (`B1. … B2. … B3. …`), phải cắt theo `B<số>.`
- một câu trỏ về HAI bài là chuyện thật, không phải lỗi: ôn tập 3 câu 10 (mật thư
  A/B/C) → Bài 10 + 12; ôn tập 4 câu 12 (mã kép a/b) → Bài 14 + 16. Nên `veCau` là
  **danh sách** mã bài, không phải một mã

---

## VIỆC 2 — `tools/chuan_lop3.py` dựng dữ liệu bài học  ⚠ LÀM TIẾP TỪ ĐÂY

**Xong**: `tools/chuan_lop3.py` → `data/lop3/` — 34 bài + `index.json`. 477 câu, **100%
có lời chữa**, **170 câu chấm máy** (102 trắc nghiệm + 68 Đúng/Sai — cả 170 câu quiz
đều chấm được, không câu nào phải bỏ). Luyện tập (307 câu) giữ TỰ CHẤM như lớp 2:
đáp án phần lớn là câu chữ, ép thành ô nhập số là chấm oan con viết đúng.

Không chép `chuan_lop2.py` mà **dùng lại** `tach_phuong_an` và `dung_cau_quiz` của nó
— hai hàm ấy mang sẵn mấy bài học đắt, chép ra bản thứ hai là bản ấy tụt hậu ngay lần
sửa sau. Cũng không mở lại docx: đáp án đã bóc xong ở bước 2b.

Hai trường thêm so với lớp 2, cả hai đã có trong bài dựng ra:

| trường | nguồn | dùng làm gì |
|---|---|---|
| `hatMam` | `lop3_tho.json` | lời nối ngược về lớp 2, hiện ở màn kết bài — đủ 34/34 |
| `ganLop2` | `lop3_gan_lop2.json` | nút **"Học lại bài lớp 2"** — 32/34 bài có đích |

⚠ **Sổ này từng dặn sai: "lấy `ve[0]` làm đích".** Làm thế thì bài 4, 16, 18 mất đích
thứ hai, mà cả ba đều do SÁCH chỉ đích danh hai bài lớp 2 (bài 4 "đếm số & đếm trang"
gộp đúng hai bài riêng biệt). Nên `ganLop2.ve` là **danh sách**. Dòng `canCu: 'khong'`
có danh sách rỗng sẵn — chỗ hiện nút cứ theo danh sách rỗng mà ẩn, khỏi thêm luật.

### Còn lại của việc 2 — nút chưa làm

`FinaleCard.jsx` (trang kết bài) và màn khi bé không đạt sát hạch. Làm được **sau**
bước 5 (khuôn chung), vì trước đó lớp 3 chưa vào tới phòng học.

Nhớ mục 6 của chuẩn khi dựng màn mở: lời mở là MỘT CÂU nêu bài toán, lấy từ dòng
`Đề bài` của mục ④, và câu dẫn chỉ giữ khi không chứa con số.

---

## VIỆC 3 — Bước 3 · vẽ hình (phần nặng nhất)

Xem `docs/phan_loai_hinh_lop3.md`. Con số đáng nhớ: sách cho **46 hình toán** nhưng
gần hết nằm ở màn mở; **mục giảng chỉ 6 hình cho 34 bài**, bài tập KHÔNG có hình nào.
Việc vẽ nhiều hơn lớp 2 chứ không ít, dù ảnh gốc ít hơn (bẫy 43).

- 13 nhóm nguyên mẫu; **9 nhóm dùng lại được** nguyên mẫu lớp 2 đã có
- phải dựng mới ~5: Ven hai vòng · lịch tháng · cân & ống đong · tiền Việt · biểu thức có ngoặc
- `image3.png` (nhiệt kế, dùng 34 lần) làm **component**, không phải PNG
- vẽ **cả ba loại hình ngay từ đầu** — giảng · màn mở · bài tập (`item:CX` + `:giai`)

---

## VIỆC 4 — bước 5 · qua khuôn chung, rồi khai sổ

`tools/dung_khuon_chung.py` + `khuon_chung.py` đưa bài về khuôn lớp 5 để dùng chung
phòng học. Bảng khớp mục ①…⑧ **y hệt lớp 2** (hằng `NOI_DUNG_HINH`). Xong bước này
lớp 3 mới hiện trong app.

---

## Đừng quên

- ~~Tiền tố mã bài `DL:KSN3.` chưa kiểm trùng~~ — **đã kiểm, không trùng**: 235 mã bài
  hiện có chia làm `DL:KSN5Q1` (168) · `DL:KSN3` (34) · `DL:KSN2` (33), cộng
  `DR:KSN5Q2` (42) · `DCR:*` (25) ở nội dung đã dựng. Không mã nào đụng mã nào.
- Khai sổ đăng ký (`data/chuong_trinh.json`): nhớ `loai: 'hoc'` và `donVi`
- 44 cái bẫy trong chuẩn — sách lớp 3 đã dính lại bẫy 5, 6, 7 y như lớp 2
