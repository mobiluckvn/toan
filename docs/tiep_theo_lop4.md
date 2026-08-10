# Điểm dừng — Toán lớp 4

Cập nhật 2026-08-10. Đọc tệp này TRƯỚC, rồi mới đọc `CHUAN_DUA_SACH_VAO_APP.md`.

Nguồn: `docs/KSN4_SACH_HOAN_CHINH_Ky_Su_Nhi_Lop4.docx` · 44 bài · 11 chương · 11 ôn tập.

> **XONG TRỌN — lớp 4 đã hiện trên kệ sách.** 44 bài · 92 hình · 392/396 câu luyện
> tập chấm máy (98%) · đường lùi hai chiều đã nối. Cổng nghiệm thu: **24 tệp kiểm ·
> 775 PASS · 0 FAIL**. Chưa deploy — xem "Việc còn lại" ở cuối.

---

## MAI VÀO VIỆC TỪ ĐÂU

**Không còn việc tồn nào chắn đường.** Ba hướng đi tiếp, xếp theo giá trị:

| # | việc | trạng thái |
|---|---|---|
| 1 | **Deploy lớp 4** | `cd web && npx firebase deploy --only hosting`. Chỉ đẩy hosting — functions và rules cả phiên không đụng tới |
| 2 | Nhiệt kế cho LỚP 3 | `image3.png` của lớp 3 (dùng 34 lần) vẫn là PNG; thành phần `NhietKe.jsx` đã dùng chung được, chỉ cần bỏ ảnh cũ |
| 3 | Bỏ chip mã `K1 · K2 · K3` ở màn nguyên tắc | **chờ bác quyết** — sửa là đụng cả bốn quyển đang chạy |

Chạy lại trọn dây chuyền:

```bash
python3 tools/rut_lop4.py && python3 tools/dapan_lop4.py && python3 tools/ontap_lop4.py
python3 tools/gan_lop4_lop3.py && python3 tools/chuan_lop4.py
python3 tools/mota_hinh_lop4.py && python3 tools/ve_hinh_lop4.py && python3 tools/gan_hinh_lop4.py
python3 tools/tach_cau_lop4.py && python3 tools/dung_khuon_chung_lop4.py --khai
python3 tools/gan_lop5_lop4.py
cd web && npm test && npm run build
```

---

## Đã xong — chạy được, có phép kiểm giữ

| bước | việc | kết quả |
|---|---|---|
| 0 | khảo sát | `docs/khao_sat_lop4.md` |
| 1 | phân loại hình | `docs/phan_loai_hinh_lop4.md` — 21 nhóm, 17 nhóm dùng lại nguyên mẫu cũ |
| 2a | bộ trích thô | `tools/rut_lop4.py` → `data/lop4_tho.json` — **44 bài · 616 câu** |
| 2b | bóc đáp án | `tools/dapan_lop4.py` → `data/lop4_dapan.json` — **852 đáp án khớp 1:1** |
| 2c | ôn tập | `tools/ontap_lop4.py` → `data/lop4_ontap.json` — **11 kỳ · 124 + 112 câu · mối nối đủ 124/124** |
| 3 | dựng bài học | `tools/chuan_lop4.py` → `data/lop4/` — **616 câu · 100% có lời chữa · 220/220 quiz chấm máy** |
| 3b | vẽ & gắn hình | `tools/mota_hinh_lop4.py` · `ve_hinh_lop4.py` · `gan_hinh_lop4.py` — **92 hình · 4 nguyên mẫu mới · đủ ba loại: 44 màn mở · 32 hình giảng · 8 cặp hình bài tập** |
| 4 | ô nhập | `tools/tach_cau_lop4.py` + `data/lop4_dapan_tay.json` — **392/396 (98%) · 559 ô · 77 ô bấm chọn · 0 ô gõ chữ** |
| 5 | khuôn chung | `tools/dung_khuon_chung_lop4.py` → `web/public/content/lop4/` + 11 `DCR_KSN4_C*` |
| — | đường lùi 4→3 | `data/lop4_gan_lop3.json` — 44 dòng (13 `sach` · 1 `sachSua` · 29 `chuDe` · 1 `khong`) |
| — | đường lùi 5→4 | `data/lop5_gan_lop4.json` — 56 bài sách → **168 micro**, đã gắn vào cả hai nơi |

Phép kiểm: `web/test/lop4.test.mjs` (40 phép). Cả bộ: **24 tệp · 775 PASS · 0 FAIL**.

**Thứ tự chạy dây chuyền** — đảo là mất hình mà không có gì báo:

```
rut_lop4 → dapan_lop4 → ontap_lop4 → gan_lop4_lop3 → chuan_lop4
  → mota_hinh_lop4 → ve_hinh_lop4 → gan_hinh_lop4
  → tach_cau_lop4 → dung_khuon_chung_lop4
```

`gan_lop5_lop4.py` chạy độc lập, nhưng phải SAU `chuan_lop4` vì nó đọc
`data/lop4/index.json` để lấy tên bài.

---

## Sách lớp 4 đều hơn hẳn ba quyển trước

Đây là điều đáng nhớ nhất khi ước lượng công sức cho quyển sau: **bóc tách gần như
không tốn công**, còn ô nhập thì tốn y như cũ.

| | lớp 3 | lớp 4 |
|---|---|---|
| số cách sách đặt tên BƯỚC | **12** (26 bước bốc hơi khi dùng mẫu lớp 2) | **1** — `Bước n —`, đúng 176 lần |
| tên câu | `Câu · Vụ · Phòng · Đảo · Mã · Trạm · Cửa` | **1** — `Câu n.` |
| mục mỗi bài | 8, có bài lệch | **10, đủ 44/44 bài, đúng thứ tự** |
| số câu mỗi bài | thay đổi | **9 + 5, không một ngoại lệ** |

Nhờ thế `khuon_chung.py` **không phải thêm tên bước nào**, và mọi phép đếm đều chốt
được thành con số cứng trong bộ trích.

---

## Bốn cái bẫy đã dính THẬT trong đợt này

### 1 · Bẫy 5 và 6 tái xuất — quyển thứ tư vẫn dính

Mốc đóng bài neo vào **dòng đầu** của khối. Nhưng bảng tiêu đề ôn tập mở bằng
`CHƯƠNG 1 · ĐẠI CÔNG TRƯỜNG LỚP TRIỆU` rồi mới tới `ÔN TẬP 1 · …`, nên mẫu trượt
sạch: **11 bài cuối chương nuốt trọn ôn tập VÀ đáp án chi tiết của cả chương vào mục
⑩ Góc bố mẹ** — 121-155 dòng rác mỗi bài, lộ nguyên đáp án cho người lớn đọc.

Mọi phép đếm câu vẫn đúng (9 + 5) nên **không có gì kêu**. Nay soi ba dòng đầu mỗi
khối, và có hai chốt riêng: "không mục nào chứa `ĐÁP ÁN`/`ÔN TẬP`" và "Góc bố mẹ
≤ 8 dòng".

### 2 · `Bài n` TRẦN trong HẠT MẦM là bài LỚP 4, không phải lớp 3

*"Bài 19 êm đẹp vì đề khai sẵn cả tổng lẫn hiệu"* (bài 20) nói về bài 19 **lớp 4**.
Mẫu bắt mọi `Bài n` cho ra 32/44 dòng "đích danh" — **18 trong số đó trỏ ngược vào
chính lớp 4**, và bài 37 trỏ ra `Bài 36` trong khi lớp 3 chỉ có 34 bài.

Chỉ đếm `Bài n` nằm trong câu có nêu **"Lớp 3"** → còn 14 dòng. 30 dòng soát tay.

**Một chỗ sách trỏ SAI, đã sửa** (`canCu: sachSua`): bài 8 ghi *"Lớp 3, ở Bài 8, con
đếm số chứa một chữ số bằng liệt kê chăm chỉ"* — nhưng Bài 8 lớp 3 là "GẤP LÊN —
GIẢM ĐI NHIỀU LẦN", còn việc ấy nằm ở **Bài 4**. Theo MÔ TẢ, không theo con số.

### 3 · Trạng thái sống qua chương làm ĐỀ thay chỗ ĐÁP ÁN

Bộ bóc đáp án giữ `cho` qua từng đuôi chương, nên câu **HỎI** của đề B chương sau
(`B1. Đọc số: 68 205.`) rơi đúng vào mẫu đáp án đề B (`B1: …`) và **ghi đè lời giải
chương trước**. Tổng vẫn tăng (214 thay vì 112) nên nhìn bảng tổng kết thấy "nhiều
hơn" chứ không thấy sai. Nay reset theo từng chương, và chốt "mỗi ôn tập 10-12 đáp án".

### 4 · Hình màn mở của CHÍNH TÔI chứa đáp án

Cổng nghiệm thu bắt hai hình: `L4H_B09_MO` có dòng chốt *"Nhìn CHỮ SỐ TẬN CÙNG là
biết chia hết cho 2"* — đó là cả bài học, in sẵn ngay màn mở. `L4H_B15_MO` để số đo
sân ở dòng chốt thay vì tiêu đề. Nay phép kiểm soi mọi hình `chuyenMoBai`: cấm
`note`, cấm `hienTich`, cấm `tenGoc`, cấm dấu `=` trong tiêu đề.

---

## Đường lùi — nay có BA TẦNG: lớp 5 → lớp 4 → lớp 3

Bác dặn "lùi được về lớp 4 khi không giải được bài lớp 5, và tham chiếu lớp 3 khi
không giải được bài lớp 4". Đã nối cả hai chiều.

### Ba chỗ phải sửa để chiều lớp 5 → lớp 4 chạy được

1. **`khuon_chung.py` ghim cứng nhãn `'Học lại bài lớp 2'`.** Lớp 4 trỏ về lớp 3 mà
   nút vẫn mời "Học lại bài lớp 2" thì bé bấm vào một lớp chẳng liên quan. Nay nhãn
   suy từ `lopDuoi` của chính đích. Tên trường cũng đổi `ganLop2` → `ganDuoi` (vẫn
   nhận tên cũ, nên bản gốc lớp 3 đã ghi ra đĩa không phải dựng lại).
2. **Nhánh `page: 'lesson'` của `App.jsx` KHÔNG nhận `onMoBai`** — mà `FinaleCard`
   lại ẩn hộp đường lùi khi thiếu nó. Nghĩa là dù dữ liệu có khai `duongLui`, màn kết
   bài lớp 5 vẫn không hiện gì. Đã truyền vào, kèm `key={view.microId}` (thiếu `key`
   là bấm nút xong rơi thẳng vào màn kết của bài đích — lỗi lớp 3 đã dính).
3. **Lớp 5 không dựng qua `khuon_chung.py`**, tệp bài nằm sẵn trên đĩa. Nên
   `gan_lop5_lop4.py` ghi thẳng trường `duongLui` vào **cả hai nơi**
   (`data/lessons/` và `web/public/content/lessons/` — với Quyển 1 lớp 5 hai nơi ấy
   phải giống hệt nhau, khác với lớp 2/3/4 nơi bản gốc và bản dựng cố ý khác nhau).

### Sửa `khuon_chung.py` mà KHÔNG làm lệch quyển cũ

Đã đối chiếu từng tệp: **lop2 · lessons · quyen2 · reviews giống hệt từng byte**;
lớp 3 chỉ đổi đúng 32 tệp (những bài CÓ đường lùi) và chỉ thêm đúng một dòng
`"lopDuoi": 2`. Nhãn nút không đổi một chữ.

### Lớp 5 không có "HẠT MẦM NĂM NGOÁI"

Quyển 1 lớp 5 soạn trước lớp 4 nên không trỏ về đâu cả — máy không dò được dòng nào.
Cả 56 bài sách đều là `chuDe`, ghép tay theo tên bài, mỗi dòng ghi lý do ở `viSao`.
Không dòng nào `khong`: sách lớp 4 phủ đủ mọi chủ đề của Quyển 1 lớp 5, chỉ khác độ sâu.

Bảng khai theo **bài sách** rồi rải xuống cả **ba micro** của bài ấy — bé học và
trượt ở mức micro, nên trượt micro nào cũng phải thấy đúng lối về.

---

## Việc còn lại

### 1 · Chưa deploy

Dữ liệu, hình và cổng nghiệm thu đều xong; `npm run build` đã chạy nên `web/dist/`
khớp `web/public/`. Deploy bằng `npx firebase deploy --only hosting` từ `web/`, rồi
**gọi thẳng vào bản chạy thật** chứ đừng tin dòng "Deploy complete".

### 2 · Nhiệt kế của LỚP 3 vẫn là ảnh

`NhietKe.jsx` nhận `tong` nên dùng chung cho mọi quyển; lớp 4 đã bỏ hẳn ảnh gốc.
Lớp 3 vẫn còn `image3.png` (dùng 34 lần) — món nợ cũ, nay đã có sẵn thành phần thay.

### 3 · Bốn câu CỐ Ý để tự chấm

Khai đích danh trong hằng `CO_Y` của `tools/tach_cau_lop4.py`, mỗi câu một lý do:
đọc số thành CHỮ · nêu quy luật bằng MỘT CÂU VĂN · hỏi "từng số hạng gánh cho ai" ·
vẽ tam giác rồi hạ đường cao bằng ê ke. Cả bốn thuộc nhóm chuẩn mục 7 luật 6 —
**không phải bỏ sót.**

---

## Sáu lỗi chỉ lộ ra khi MỞ MẮT XEM BẢN CHẠY THẬT

Chuẩn mục 10 bước 7 dặn "đi trọn một bài thật rồi mới deploy". Sáu lỗi dưới đây
**không phép kiểm nào bắt được** vì dữ liệu của chúng hoàn toàn hợp lệ:

1. **Bẫy 32 sống dậy ở màn mở.** Lời dẫn lấy đề của mục ⑥ (*"tổng hai chữ số bằng
   12"*) trong khi hình vẽ theo mục ② (bảng hàng - lớp ghi 24 358) — hai bài toán
   khác nhau nằm chung một màn, ngay dòng đầu bé đọc. Nay lời dẫn lấy từ dòng
   `HỎI GÌ?` của mục ③, đúng câu hỏi của tình huống mở. **Đã thêm phép kiểm**: con
   số trong lời dẫn phải có mặt trong hình — nó bắt tiếp bốn bài nữa.
2. **Nhãn cột đè lên nhau.** `cau_truc_so` đóng cỡ chữ cố định; lớp 4 xây bảy phòng
   tới lớp TRIỆU nên "TRĂM NGHÌN" và "CHỤC NGHÌN" chồng thành một khối chữ. Nay nhãn
   co theo bề ngang phòng — **hình lớp 2 và lớp 3 không đổi một nét** (đã đối chiếu).
3. **Màn nhịp DỊCH là một bức tường chữ.** Sáu dòng có nhãn dồn thành một đoạn liền.
   Nay nối bằng xuống dòng và giao diện giữ dòng.
4. **Màn bẫy in câu SAI hai lần** — lời dẫn trùng nguyên văn ô "SAI" ngay dưới. Nhắc
   hai lần đúng thứ mình muốn bé quên.
5. **Gọi nhầm tên nhân vật.** Dòng dấu hiệu ghim cứng "Su Kem", trong khi sách lớp 3
   VÀ lớp 4 đều đặt mục ấy là "TRÍ LONG ƠI, NHẦM RỒI!". Nay lấy tên từ tiêu đề mục —
   **sửa luôn cho lớp 3 đang chạy**.
6. **Hai tiêu đề cột của bảng thành hai "bước giải".** Mục ⑥ dựng bằng bảng hai cột,
   nên "TRANG VỞ CỦA CON" và "VÌ SAO VIẾT DÒNG NÀY?" lọt vào màn Bài mẫu — bé bấm
   "Bước tiếp" hai lần chỉ để đọc hai cái nhãn cột.

Ngoài ra `--khai` chạy lần thứ hai **đẻ thêm một dòng "Lớp 1"** ở kệ "sắp có" — bộ
dựng phải chạy được nhiều lần cho cùng một kết quả. Nay lọc cả dòng mới trước khi chèn.

## Việc đã cân nhắc và LOẠI

- **Luật suy đáp án "chốt có đúng một số"** — đã đo: thêm 5 câu, **sai 2** (bài 14
  câu 1 lấy `2` từ *"nhân với 2"* trong khi đáp án là `48, 96`; bài 44 câu 7 lấy `12`
  trong khi đáp án là *"hai kim TRÙNG nhau"*). Suy máy dừng ở 12 luật hẹp (180 câu),
  212 câu còn lại viết tay — chậm nhưng đúng, y như lớp 3.
- **Sửa `_don` của `tach_cau_lop3.py` để biết thêm đơn vị (km, lít, số hạng…).**
  Loại: sửa ở đó là **298 đáp án lớp 3 đổi theo** mà chẳng ai yêu cầu. Viết `_don4`
  riêng cho lớp 4, dùng lại phần còn lại.
- **Chép `arch_l3.py` thành `arch_l4.py`.** Loại: bản chép tụt hậu ngay lần sửa
  nguyên mẫu sau. `arch_l4` **nhập** 29 nguyên mẫu cũ và chỉ viết thêm 4 cái mới.
- **Giữ ảnh gốc của sách làm hình mở.** Loại vì ba lẽ: màu không khớp bảng màu
  thương hiệu; ảnh **có sẵn đáp án** (hình bài 1 in luôn cách đọc số) trong khi màn
  mở phải là bản ĐỀ; và ảnh raster không sửa lại được khi lời văn đổi.
- **Vẽ đủ 176 hình giảng (44 bài × 4 bước).** Loại: chuẩn dặn "không phải bước nào
  cũng đáng vẽ". 32 hình phủ những bước mang cái CỐT của bài.
- **Khai lớp 4 vào sổ khi ô nhập chưa đạt ngưỡng.** Loại: khai là bật năm luật ô
  nhập, mà cổng đỏ tệ hơn kệ sách thiếu một quyển. Nên `--khai` là cờ riêng, và nó
  vẫn báo nếu tỉ lệ chấm máy dưới 85%.
- **Nới phép kiểm "lời dẫn và hình kể cùng bài toán" cho dễ qua.** Loại: nó đang so
  với `caption` nên đỏ oan năm bài — chữa bằng cách so với NỘI DUNG VẼ RA (`params`),
  chứ không phải bằng cách bỏ phép kiểm. Nhưng bốn bài đỏ thật thì sửa HÌNH, không
  sửa ngưỡng: hình màn mở phải mang đủ số đo cho sẵn của đề.

---

## Đừng quên

- Tiền tố `DL:KSN4.` **đã kiểm, không trùng và không lồng** với `DL:KSN2.` ·
  `DL:KSN3.` · `DL:KSN5Q1.` · `DR:KSN5Q2.` (có phép kiểm giữ).
- Sổ đăng ký: nhớ `loai: 'hoc'`, `donVi: 'bài'`, và **`doc.moiManMotMuc: true`** —
  cờ ấy quyết ba thứ cùng lúc: phòng học nào mở, chữ to hay nhỏ, và có bị áp luật
  "cấm ô gõ chữ" hay không.
- Khai xong thì **xoá mục `Lớp 1 · 3 · 4` khỏi `sapCo`** — `--khai` đã làm sẵn,
  nhưng kiểm lại bằng mắt.
- Deploy xong **gọi thẳng vào bản chạy thật**, đừng tin dòng "Deploy complete":
  `curl -s https://ky-su-nhi.web.app/content/lop4/index.json | head`
