# Điểm dừng — Toán lớp 3

Cập nhật 2026-08-09. Đọc tệp này TRƯỚC, rồi mới đọc `CHUAN_DUA_SACH_VAO_APP.md`.

**ĐÃ DEPLOY** — https://ky-su-nhi.web.app · `npx firebase deploy --only hosting` từ
thư mục `web/`. Chỉ đẩy hosting: functions và rules không đụng tới trong đợt này nên
không đẩy theo, tránh mang lên thứ chưa kiểm.

Nguồn: `docs/Toan_Tu_Duy_Lop3_Cuoc.docx` · 34 bài · 8 chương · 8 ôn tập · 3 ải.

---

## MAI VÀO VIỆC TỪ ĐÂU

**Lớp 3 XONG TRỌN, không còn việc tồn.** 23/23 tệp kiểm xanh, cây làm việc sạch, đã
deploy. Ba hướng đi tiếp, xếp theo giá trị:

| # | việc | trạng thái |
|---|---|---|
| 1 | **Đưa quyển LỚP 4 vào app** | chưa có bản `.docx` nguồn. Dây chuyền và phép kiểm đã sẵn — xem "Sẵn sàng cho quyển sau" bên dưới |
| 2 | Bỏ chip mã `K1 · K2 · K3` ở màn nguyên tắc | **chờ bác quyết** — sửa là đụng cả lớp 2 và lớp 5 đang chạy |
| 3 | Deploy `functions` và `firestore rules` | cả phiên chưa đụng tới chúng nên KHÔNG đẩy. Muốn đẩy thì soát trước |

### Sẵn sàng cho quyển sau — chép được ngay

| dùng lại | cách |
|---|---|
| `figforge/arch_l3.py` | 29 nguyên mẫu hình (22 của lớp 2 + 7 mới). Quyển sau `import` chứ đừng chép |
| `khuon_chung.py` | tự đọc `quyen` từ bản gốc, biết 12 cách sách đặt tên bước |
| 6 bộ công cụ `*_lop3.py` | chép làm mẫu: `rut · dapan · ontap · chuan · ve_hinh · gan_hinh · tach_cau · dung_khuon_chung` |
| `web/test/luat_o_nhap.test.mjs` | **KHÔNG cần chép** — nó tự đọc sổ đăng ký, quyển mới khai vào là bị soi ngay |
| giao diện | đã lái hết theo cờ trong sổ; khai `doc.moiManMotMuc` là xong, không sửa component nào |

**Bắt đầu quyển mới thì đọc `CHUAN_DUA_SACH_VAO_APP.md` trước** — 44 cái bẫy, và mục 7
nay có thêm năm luật ô nhập.

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
| 3b | vẽ & gắn hình | `figforge/arch_l3.py` · `tools/ve_hinh_lop3.py` · `tools/gan_hinh_lop3.py` — **122 hình · 21 nguyên mẫu · đủ 34/34 bài, đã soát hết ba loại** |
| 4 | ô nhập chấm máy | `tools/tach_cau_lop3.py` + `data/lop3_dapan_tay.json` → `data/lop3_dapan_o.json` — **298/307 câu luyện tập chấm máy (97%) · 468 ô nhập · 62 ô bấm chọn · 0 ô gõ chữ** |
| 5 | khuôn chung + sổ đăng ký | `tools/dung_khuon_chung_lop3.py` → `web/public/content/lop3/` · `reviews/DCR_KSN3_C*` — **34 bài · 11 kỳ sát hạch · LỚP 3 ĐÃ HIỆN TRONG APP** |
| — | đường lùi về lớp 2 | `data/lop3_gan_lop2.json` — 34 bài (21 `sach` · 11 `chuDe` · 2 `khong`), nút đã nối tới `FinaleCard` |

Phép kiểm: `web/test/lop3.test.mjs` (58 phép). Chạy `cd web && npm test`.

**Thứ tự chạy dây chuyền** — đảo là mất hình mà không có gì báo:

```
rut_lop3.py → dapan_lop3.py → ontap_lop3.py → chuan_lop3.py → ve_hinh_lop3.py
  → gan_hinh_lop3.py → dung_khuon_chung_lop3.py
```

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

## VIỆC 2 — `tools/chuan_lop3.py` dựng dữ liệu bài học  ✔ XONG

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

### Nút "Học lại bài lớp 2" — đã nối, đã kiểm bằng mắt

`FinaleCard.jsx` hiện **Hạt mầm năm ngoái** và hộp đường lùi. Chưa đạt thì hộp ấy
viền vàng nổi hẳn lên: đó là lối ra đỡ hụt hẫng nhất, về luyện lại gốc chứ không phải
làm lại bài khó thêm một lượt. `onMoBai` đi xuyên `App → LessonPlayer → StepView →
FinaleCard`.

Nhớ mục 6 của chuẩn khi dựng màn mở: lời mở là MỘT CÂU nêu bài toán, lấy từ dòng
`Đề bài` của mục ④, và câu dẫn chỉ giữ khi không chứa con số.

---

## VIỆC 3 — Bước 3 · vẽ hình  ✔ XONG BA LOẠI

### Đã xong — chạy được, có phép kiểm giữ

| việc | kết quả |
|---|---|
| đếm khối lượng trước khi vẽ | `tools/khao_sat_hinh_lop3.py` |
| **7 nguyên mẫu** | `figforge/arch_l3.py` — nhập lại 22 nguyên mẫu lớp 2, viết mới 7 |
| bộ vẽ | `tools/ve_hinh_lop3.py` → `web/public/content/figures/` + sổ tay |
| bộ gắn | `tools/gan_hinh_lop3.py` — chạy **sau** `chuan_lop3.py`, là bước CUỐI |
| hình đã vẽ | **122 hình · đủ 34/34 bài, ba loại đều đã soát hết** (`data/lop3_hinh.json`) |

Bảy nguyên mẫu mới: `hinh_tron` · `luoi_dien_tich` · `ven_hai_vong` · `lich_thang` ·
`can_ong_dong` · `tien_viet` · `bieu_thuc_ngoac`. Bước 1 đoán "khoảng 5" — hoá ra 7,
vì hình tròn và lưới diện tích không nguyên mẫu lớp 2 nào đỡ được.

`arch_l3.py` **nhập** nguyên mẫu lớp 2 chứ không chép: sửa một nguyên mẫu lớp 2 thì
hình lớp 3 được sửa theo. Bản chép tay không làm được thế.

### Khối lượng còn lại — máy đếm ra, đừng đoán

Chạy `python3 tools/khao_sat_hinh_lop3.py --chi-tiet`:

| loại | cần | đã vẽ |
|---|---|---|
| ① hình giảng (neo theo bước) | 131 bước ở 34 bài | **39 — đủ 34/34 bài** |
| ② hình màn mở (bản ĐỀ, bỏ hết đáp án) | 34 bài | **34 — đủ** |
| ③ hình bài tập (`item:CX` + `:giai`) | 14 câu chắc + 134 câu cần soát tay | **46 hình / 25 câu — ĐÃ SOÁT HẾT** |

**Không vẽ đủ 131 hình giảng, và đó là cố ý.** Chuẩn dặn "không phải mọi bước đều
đáng vẽ" — vẽ đúng bước mang cái CỐT của bài, còn bước chỉ diễn giải bằng lời thì
thêm hình là thêm thứ để bé phải đọc. 39 hình phủ đủ 34 bài; bài nào dày ý thì hai
hình (bài 1, 6).

### 134 câu "có thể cần hình" — đã soát tay xong

**10 câu thật sự cần**, đã vẽ đủ cặp đề + lời giải. **124 câu KHÔNG cần**, cùng một
lý do: đề đã tả trọn bằng lời và việc của bé là TÍNH chứ không phải NHÌN. "Tính chu
vi hình chữ nhật dài 7 cm rộng 3 cm" mà vẽ cái hình chữ nhật ra thì chẳng thêm thông
tin nào — chỉ thêm một thứ để bé phải đọc.

Hình chỉ đáng vẽ khi bé **phải nhìn mới làm được**: đếm cây trên vòng tròn (B24C3),
đếm vạch cưa (B24C6), thấy hai quả cân giống nhau ở hai đĩa (B33C5), thấy khối nấp
hàng sau (B31C8), thấy các ngày cùng cột lịch (B32C6)…

Kết luận này ghi trong hằng `CAN_HINH` và `DA_SOAT_KHONG_CAN` của
`tools/khao_sat_hinh_lop3.py`, kèm lý do từng câu — không ghi thì phiên sau lại quét
ra đúng 134 dòng ấy và lại ngồi soát từ đầu.

Nguyên mẫu `hinh_tron` được thêm tham số `quanhVong` cho bài trồng cây quanh hồ:
vẽ ra thì bé đếm được cả cây lẫn khoảng và tự thấy hai số bằng nhau — đúng chỗ bé
hay đếm thừa một.

Lưới quét lượt đầu của tôi ra 306/477 câu "có thể cần" — đó là nhiễu chứ không phải
sàng lọc, và một danh sách 306 dòng thì không ai soát tay nổi. Bản hiện tại đòi câu
phải nhắc tới một VẬT THỂ nhìn được, nên còn 135 — đúng cỡ soát được.

### Bốn lỗi trình bày đã bắt ở nhóm đầu (chuẩn dặn phải bắt sớm, không thì sửa cả trăm hình)

1. **Tên hình thu nhỏ mãi vẫn tràn** → dùng `txt_wrap` ngắt dòng, đừng dùng `txt_fit`
2. **Nhãn đè lên nét vẽ** → mọi nhãn của `hinh_tron` đặt NGOÀI mép
3. **Ô 1 cm² vẽ hai cỡ trong cùng một bức** → cạnh ô tính MỘT LẦN cho cả hình.
   Đây là bẫy 26 tái xuất, và nó nguy vì cả bài đang dạy SO hai diện tích
4. **Hình "RÀO" vẽ y hệt hình "THẢM"**, chỉ khác cái tên bên dưới → hình phản lại
   chính bài. Nay `do: 'rao'` bỏ ô lòng, chỉ còn viền dày kèm vạch chia từng cm

### Ba lỗi nữa bắt được ở lượt vẽ 34 màn mở

5. **`cau_truc_so` tràn khung với 4 tháp.** Nguyên mẫu lớp 2 đóng cứng bề ngang 26,
   vừa khít ba tháp Trăm - Chục - Đơn vị; lớp 3 xây thêm tháp NGHÌN thành 104 > 88,
   mái nhà cụt hai đầu. Đã sửa ở `arch_l2.py` bằng `min(26, 88/số phòng)` — **hình
   lớp 2 giữ nguyên từng bit**, đã đối chiếu mã băm để chắc.
6. **Ống đong vẽ mọi ống cùng cỡ** → chai 1000 ml cao bằng cốc 350 ml. Cùng kiểu nói
   dối như ô 1 cm² lệch cỡ. Nay chiều cao tỉ lệ với dung tích.
7. **Trùng mã hình.** Tôi đặt `L3H_BT01` cho hai hình khác nhau; hình sau đè hình
   trước và **không kêu ca gì** — chỉ lộ ra vì bộ đếm báo "73 hình · sổ tay 71 mục".
   Nay bộ vẽ dừng hẳn khi thấy trùng mã, và **sổ tay biết dọn** mã đã bỏ (trước đó
   nó chỉ thêm, nên mã cũ nằm lại trỏ vào ảnh đã xoá).

### Bẫy 26 lần thứ ba — lần này nằm trong nguyên mẫu DÙNG CHUNG

`cham_tron` tính cỡ chấm RIÊNG cho từng nhóm, nên trong cùng một bức, rương "3 viên
xếp một hàng dọc" ra chấm bán kính 2,6 còn phần dư "2 viên một hàng ngang" chỉ 1,3 —
đúng một nửa. Cùng một viên ngọc mà vẽ hai cỡ: bé đếm vẫn ra số đúng, nhưng nhìn ra
hai thứ khác nhau, mà bài chia có dư thì phần dư PHẢI trông y hệt phần đã chia.

Lời chú cũ nói *"cỡ chấm dùng chung cho cả nhóm"* — đúng chữ, nhưng **cả nhóm chưa
phải cả bức**. Nay tính một lần cho cả bức.

⚠ **Sửa cái này làm đổi 3 hình của LỚP 2** (`L2H_CHAM01 · 02 · 04`) — chúng dính cùng
lỗi từ trước. 117/120 hình lớp 2 còn lại giữ nguyên từng byte, đã đối chiếu mã băm.
Đã chạy lại trọn đuôi dây chuyền lớp 2: `ve_hinh_lop2 → gan_hinh_lop2 →
dung_khuon_chung`.

### Hai lỗi DỮ LIỆU, không phải lỗi mã — cả hai đều câm

- **Lịch tháng nói dối**: tôi nhập `batDau` sai nên 6·13·20·27 rơi cột thứ Hai trong
  khi nhãn cột và lời chú đều nói Chủ nhật. Sách nói ngày 6 là **Chủ nhật**. Hình vẽ
  đẹp, dữ liệu hợp lệ, chỉ có sự thật là sai. Nay có phép kiểm soi đúng chỗ này.
- **Sách lớp 3 đặt tên bước MƯỜI KIỂU**, lớp 2 chỉ có bốn. Bài 29 đặt cả ba bước
  giảng là "Nhân vật 1/2/3", bài 23 dùng "Nhịp", bài 26 dùng "Phép thử". Mẫu lớp 2
  bỏ sót 26 bước, mà bỏ sót thì im lặng: bài vẫn dựng, chỉ là chặng giảng trống trơn.
  `gan_hinh_lop3.py` liệt kê đủ 12 tên VÀ canh — bài nào không nhận ra bước nào thì kêu.
  ⚠ **`khuon_chung.py` vẫn dùng `R_BUOC` bốn tên** — phải sửa ở VIỆC 4, không thì
  `statements` và `lecture.screens` của mấy bài ấy rỗng.

### Còn lại

- `image3.png` (nhiệt kế, dùng 34 lần) làm **component**, không phải PNG
- thẻ "Luật chơi" của 8 ôn tập cũng là khung chữ → làm giao diện
- vẽ **cả ba loại hình**, đừng vẽ xong loại ① rồi tưởng xong (lớp 2 trả giá hai lượt:
  45 trên 120 hình là làm ở lượt thứ hai)

---

## VIỆC 4 — bước 5 · qua khuôn chung, khai sổ  ✔ XONG

`tools/dung_khuon_chung_lop3.py` → `web/public/content/lop3/` (34 bài) +
`reviews/DCR_KSN3_C*.json` (11 kỳ sát hạch) + khai `lop3` vào sổ đăng ký.
**Lớp 3 đã hiện trong app**, đã kiểm bằng mắt: kệ sách → trang chính → bài → màn mở
có hình → ôn tập → màn kết → nút "Học lại bài lớp 2".

Dùng CHUNG `khuon_chung.sang_khuon_chung` với lớp 2, không chép bản thứ hai. Hàm ấy
tự đọc `quyen` từ bản gốc nên **không có tham số nào để gọi nhầm**.

### `khuon_chung.py` — mẫu tên bước, chỗ suýt hỏng câm nhất cả quyển

`R_BUOC` cũ biết bốn tên của lớp 2 (`Bước · Nhịp · Vũ khí · Chặng`). Sách lớp 3 dùng
**mười hai**: thêm `Phép thử · Chiêu · Đường · Tuyệt kỹ · Kho báu · Thế trận ·
Nhân vật · Câu hỏi`. Giữ mẫu cũ thì **7 bài không có nguyên tắc nào** (bài 7, 12, 16,
19, 20, 24, 29) và **26 bước bốc hơi** — bài vẫn dựng ra, phòng học vẫn mở, chỉ là
không dạy gì và không một dòng cảnh báo.

Đã đối chiếu: thêm tám tên **không làm lệch một dòng nào của lớp 2**, và bản dựng
lớp 2 sau khi sửa giống bản cũ **từng byte**.

### Ba chỗ giao diện gõ cứng `'lop2'` — đã lái theo sổ đăng ký

`content.js` vốn dặn "đừng rải điều kiện *nếu là lớp 2 thì…* ra khắp component", mà
chính `App.jsx` lại làm thế. Thêm lớp 3 là ba chỗ hỏng cùng lúc:

| chỗ | hỏng gì nếu không sửa |
|---|---|
| `App.jsx` so `chuongTrinh === 'lop2'` | bé lớp 3 rơi vào phòng học lớp 5: chữ nhỏ, dồn nhiều khối một màn |
| `HomeLop2.jsx` gõ cứng `content/lop2/` và tên quyển | mở lớp 3 ra thấy đúng 33 bài của lớp 2 dưới cái tên lớp 2 |
| `ExamPlayer.jsx` bảng `lop2 ? KSN2 : KSN5Q1` | mọi kỳ sát hạch lớp 3 nạp nhầm tệp của lớp 5 |

Nay cả ba hỏi **cờ trong sổ**: `nhipDocCham()` (từ `doc.moiManMotMuc`), `thuMuc`,
`maKy()` (suy từ `tienTo`). Thêm quyển thứ tư không phải sửa gì.

### Hai lỗi câm nữa

- **`onTap` vs `ontap`**: bản gốc lớp 3 ghi hoa chữ T, lớp 2 ghi thường, mà giao diện
  lọc theo `'ontap'` → **cả 8 ôn tập lớp 3 biến mất khỏi màn hình**, dữ liệu vẫn đủ,
  tệp vẫn đúng, chỉ là không ai thấy. Chuẩn hoá ở bộ dựng, và có phép kiểm so thẳng
  bộ từ vựng hai quyển.
- **`LessonPlayer` thiếu `key`**: bấm "Học lại bài lớp 2" từ màn kết bài lớp 3 thì
  React giữ nguyên component cũ, số thứ tự màn KHÔNG reset → rơi thẳng vào màn kết
  bài lớp 2 (24/24, điểm 0/0), coi như chưa học đã xong. `resumeAt` chỉ là giá trị
  khởi tạo nên không cứu được. Nay có `key={view.baiId}` và đi lùi thì `fromStart`.

### Đáp án ôn tập — bước 2c bổ sung

Kỳ sát hạch cần đáp án, mà bản đầu của `ontap_lop3.py` ĐÓNG khối ngay khi gặp chữ
`ĐÁP ÁN` nên tám bộ đáp án ôn tập rơi hết ra ngoài. Nay bóc đủ **114 đáp án đề chính
+ 84 đề B**. Ba dạng phải đọc mới biết:
- ải đánh tiêu đề bằng tiền tố `Ả1`, không phải `★ ĐÁP ÁN ẢI`
- ôn tập 6 đặt tên câu là "Vụ" nên đáp án ghi `V1:` chứ không phải `C1:`
- ôn tập 3 chèn nhãn giữa mã và dấu hai chấm: `C10 — MẬT THƯ: (A) …`

---

## VIỆC 6 — ô nhập cho câu luyện tập  ✔ XONG

**Triệu chứng bác nêu:** cả 307 câu luyện tập đều là "con làm rồi bấm xem lời giải".
Bé bấm một nút là xong, không ai biết bé có làm hay không — sổ phụ huynh và bảng cô
giáo trống, tức là KHÔNG đánh giá được việc học.

| | |
|---|---|
| suy máy (5 luật hẹp, đã soát tay từng câu) | 88 / 307 |
| viết tay (`data/lop3_dapan_tay.json`) | 210 / 307 |
| **chấm máy được** | **298 / 307 (97%) · 468 ô nhập** |
| CỐ Ý để tự chấm, đã khai lý do từng câu | 9 |
| chưa xét | **0** |

### Không ô nào bắt bé GÕ CHỮ

| loại ô | số ô |
|---|---|
| điền số | 406 |
| **bấm chọn** (nút) | **62** |
| gõ chữ hay biểu thức | **0** |

Luật cứng: **mỗi ô chỉ được là điền SỐ hoặc BẤM CHỌN.** Sáu ô biểu thức cuối cùng
(`2 000 + 400 + 30 + 5` · `6 ▢ 5` · đặt ngoặc) cũng đã thành nút — gõ biểu thức thì
thừa thiếu một dấu cách là mất điểm oan, y như gõ chữ.

Bé lớp 3 gõ chậm và sai chính tả một chữ là mất điểm oan, mà bài thì đang kiểm TOÁN
chứ không kiểm kỹ năng gõ. Nên mọi đáp án là CHỮ đều thành nút bấm: chia có dư
(`3 dư 1`) · tên bốn thành phần phép chia · đọc giờ · giờ "kém" · thứ trong tuần ·
chẵn/lẻ · thuộc/không · hợp lệ/phạm luật · đơn vị đo.

Mồi nhử của ô chia có dư dựng theo đúng ba lỗi sách nêu — sai thương, sai số dư, và
số dư ≥ số chia — và mỗi mồi được kiểm bằng chính phép chia để chắc chắn nó SAI.

Với câu **đặt ngoặc** thì hai lựa chọn chính là HAI CÁCH ĐẶT DUY NHẤT có thể
(`(3 + 5) × 2` và `3 + (5 × 2)`) — không phải bịa mồi, chỉ liệt kê hết khả năng.

Phép kiểm `không mồi nhử nào vô tình cũng đúng` tự tính giá trị mọi lựa chọn là
biểu thức số rồi so — mồi mà cũng ra đáp án đúng thì bé chọn nó bị chấm sai oan,
tệ hơn cả việc không có trắc nghiệm.

Phép kiểm `không ô nào bắt bé gõ chữ` canh chỗ này.

Dạng khoá đã dùng: `parts` (nhiều ô có nhãn) · `value` (một số) · `values` (dãy số,
giữ thứ tự) · `divmod` cho chia có dư (`"3 dư 1"` — giữ CẢ thương LẪN số dư, vì đề
"viết chính danh" hỏi cả hai).

### Bốn lỗi bắt được khi soát tay chính luật của mình

1. **Cắt ở dấu `=` ĐẦU TIÊN** → ô nhận đáp án `"30 + 6 = 36"`, bé gõ đúng `36` vẫn
   bị chấm sai. Phải lấy vế CUỐI.
2. **Bỏ ngoặc làm mất số dư**: `13 : 4 = 3 (dư 1)` thành `3`. Đề hỏi cả thương lẫn
   dư — chấm mỗi thương là ĐỔI ĐỀ.
3. **Đề hỏi hai phép mà chỉ ra một ô** (`18 : 3` bị bỏ vì sách chèn chữ "chia hết"
   giữa thương và ngoặc). Nay đếm số phép trong ĐỀ và bắt khớp.
4. **Lời giải nêu MỘT trong nhiều đáp án đúng** ("ví dụ 6 × 6 + 1 = 37") — chấm đúng
   mỗi 37 là chấm oan mọi số hợp lệ khác. Nay thấy "ví dụ/chẳng hạn" là để tự chấm.

### ⚠ Một lỗi của BỘ CHẤM, không phải của dữ liệu

Gõ `2000 + 400 + 30 + 5` mà sách ghi `2 000 + 400 + 30 + 5` thì **bị báo sai** — bé
làm ĐÚNG vẫn trượt, ở mọi câu tách số theo hàng. Khoảng trắng giữa hai chữ số là dấu
phân nghìn kiểu Việt, không mang nghĩa. Đã nới trong `web/src/lib/flow.js` (hàm
`boPhanNghin`), chỉ bỏ khi khoảng trắng kẹp GIỮA hai chữ số nên không gộp nhầm hai
số. Nới này **có lợi cho cả lớp 2 và lớp 5**.

### 9 câu tự chấm — CỐ Ý, đã khai lý do

Không còn câu nào "chưa xét". Phần lớn câu "vì sao" hoá ra vẫn đo được: đề hỏi MỘT
con số kèm MỘT lời giải thích, nên tách con số ra thành ô là đo được ngay, còn lời
giải thích để bé đối chiếu với `solutionNarrative`. 28 câu chuyển được nhờ cách ấy.

Bốn nhóm còn giữ tự chấm:
- **đề mở · việc làm bằng tay** (6) — chuẩn mục 7 luật 6
- **nhiều đáp án đều đúng** (2) — sách ghi "ví dụ 6 × 6 + 1 = 37" thì 43, 49… cũng đúng
- **đọc số thành CHỮ** (1) — "năm mươi tư" và "năm mươi bốn" đều đúng
- **chỉ yêu cầu gạch chân, đáp là câu văn** (1) — mỗi bé diễn đạt một kiểu

Hai câu cuối khai đích danh trong hằng `CO_Y` của `tach_cau_lop3.py`, để lần sau
không ai tưởng là bỏ sót.

### Ô BẤM CHỌN — trả lời phần "phần nào chọn trắc nghiệm"

Dùng `options` trong `parts` để ra nút bấm thay vì ô gõ: chẵn/lẻ · thuộc/không ·
hợp lệ/phạm luật · cửa trái/cửa phải · g-kg-ml-l · đoạn/phần · nhịp đều/phép thử sâu
hơn. Chữ trên nút LẤY TỪ SÁCH — chốt tự soát nay soi cả đề lẫn lời giải, vì tên loại
của nút thường do chính ĐỀ nêu ra.

---

## Luật đã rút ra — QUYỂN SAU ĐƯỢC RÀ TỰ ĐỘNG

`web/test/luat_o_nhap.test.mjs` đọc danh sách quyển từ `content/chuong_trinh.json`,
nên **lớp 4 vừa khai vào sổ là bị soi ngay** — không ai phải nhớ chép lại luật, và
không ai chép thiếu. Năm luật: cấm ô gõ chữ (quyển đọc chậm) · mồi nhử phải thật sự
sai · đáp án bấm chọn nằm trong nút · ô nào cũng có nhãn và nhãn không lộ đáp án ·
chấm máy ≥ 85%.

Luật 1 lái theo cờ `doc.moiManMotMuc` trong sổ, không theo tên quyển — lớp 4 chỉ cần
khai cờ ấy. Lớp 5 không bật cờ nên 209 ô gõ chữ của nó là CHỦ Ý, không phải nợ.

Toàn văn năm luật + ba lần phép kiểm đỏ oan: `CHUAN_DUA_SACH_VAO_APP.md` mục 7.

---

## Việc đã cân nhắc và LOẠI

- **Vẽ đủ 131 hình giảng, mỗi bước một hình.** Loại: chuẩn dặn "không phải mọi bước
  đều đáng vẽ". Bước nào chỉ diễn giải bằng lời mà thêm hình là thêm thứ để bé phải
  đọc. 39 hình phủ đủ 34 bài đã đúng liều.
- **Tách riêng `cham_tron` cho lớp 3 để khỏi đụng hình lớp 2.** Loại: như thế lớp 2 ở
  lại với lỗi lệch cỡ chấm. Sửa ở gốc, rồi đối chiếu mã băm để biết đúng 3/120 hình
  lớp 2 đổi.
- **Dựng lại hai luật `r_nhieu_ve` và `r_hai_ben` của lớp 2.** Loại: lớp 2 đã thử
  và phải GỠ cả hai — chúng suy đáp án từ LỜI VĂN của lời giải và sai hàng loạt. Mã
  cũ còn trong `tools/tach_cau_lop2.py` kèm lý do.
- **`npm run deploy` (build + firebase deploy đầy đủ).** Loại: lệnh ấy đẩy cả
  functions và firestore rules — đợt này không đụng tới chúng, đẩy theo là mang lên
  trạng thái cục bộ chưa ai kiểm. Dùng `--only hosting`.

## Chưa làm — cân nhắc riêng

Màn NGUYÊN TẮC in mã `K1 · K2 · K3` thành chip xanh trước mỗi nguyên tắc (`StepView.jsx`
dòng 86). Với bé 8-9 tuổi thì "K2" không mang nghĩa gì — đúng loại "mã nội bộ của
người soạn" mà chuẩn mục 5 bảo phải bỏ. **Nhưng nó có sẵn từ trước và dùng chung cả
ba quyển**, nên sửa là đụng cả lớp 2 lẫn lớp 5. Chưa sửa, để bác quyết.

## Đừng quên

- ~~Tiền tố mã bài `DL:KSN3.` chưa kiểm trùng~~ — **đã kiểm, không trùng**: 235 mã bài
  hiện có chia làm `DL:KSN5Q1` (168) · `DL:KSN3` (34) · `DL:KSN2` (33), cộng
  `DR:KSN5Q2` (42) · `DCR:*` (25) ở nội dung đã dựng. Không mã nào đụng mã nào.
- Khai sổ đăng ký (`data/chuong_trinh.json`): nhớ `loai: 'hoc'` và `donVi`
- 44 cái bẫy trong chuẩn — sách lớp 3 đã dính lại bẫy 5, 6, 7 y như lớp 2
