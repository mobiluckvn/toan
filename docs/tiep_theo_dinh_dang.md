# Điểm dừng — ĐỊNH DẠNG NỘI DUNG (markdown + LaTeX)

Cập nhật 2026-08-11. Đọc tệp này TRƯỚC khi động vào lời văn hay cách trình bày bài.

> **ĐANG CHẠY trên ky-su-nhi.web.app.** Cổng: 27 tệp kiểm · 830 PASS · 0 FAIL.
> **CÒN BA VIỆC CHƯA LÀM** — xem "Việc còn lại" ở cuối. Đó là lý do có tệp này.

---

## MAI VÀO VIỆC TỪ ĐÂU

Làm theo đúng thứ tự này, vì việc trước có thể lộ thêm việc cho việc sau:

1. **Test end-to-end trọn vòng cả bốn quyển** — rẻ nhất, và mỗi lần đi thật lại
   lòi ra lỗi mà cổng xanh không bắt được (đã đúng như thế bảy lần).
2. **Vẽ lại 368 hình lớp 2·3·4** — chữ trong hình vẫn kiểu cũ (`1/(1×2)`).
3. **Viết 984 gợi ý** cho câu luyện tập lớp 2·3·4.

---

## Dây chuyền — THỨ TỰ LÀ BẮT BUỘC

```
① dựng      python3 tools/dung_khuon_chung.py        (lớp 2)
            python3 tools/dung_khuon_chung_lop3.py
            python3 tools/dung_khuon_chung_lop4.py
② gắn hình  python3 tools/gan_hinh_lop2.py           (rồi dựng lại lớp 2)
③ định dạng python3 tools/dinh_dang.py               → markdown + LaTeX
④ bài mẫu   python3 tools/bai_mau.py                 → cắt phần Tóm tắt/Giải/Đáp số
⑤ cổng      cd web && npm test && npm run build
```

⚠ **③ và ④ sửa thẳng bản DỰNG** (`web/public/content`), mà bộ dựng ① thì ghi đè
trọn tệp từ bản gốc. **Chạy ① sau ③④ là mất sạch định dạng — dữ liệu vẫn hợp lệ và
KHÔNG CÓ GÌ BÁO.** Đúng cái bẫy đã dính với việc gắn hình ở Quyển 2.

---

## Đã làm ở đợt này

### 1 · Bộ hiển thị markdown + LaTeX

`web/src/lib/chuviet.js` (bộ đọc) + `web/src/components/Chu.jsx` (bộ vẽ).
Dùng `<Chu t="…" />` cho một đoạn, `<Chu t="…" khoi />` cho nhiều đoạn.

**Vì sao không dùng KaTeX.** Đã đếm cả bốn quyển trước khi chọn:

```
phân số a/b 5097 · tỉ số a : b 3193 · dấu × 5263 · phần trăm 1726
m² cm² 488 · phân số lồng 183 · lũy thừa 25 · hỗn số 17 · CĂN: 0
```

Toàn số học tiểu học. KaTeX nặng ~270 KB kèm bộ phông riêng — vô lý cho một app
trẻ con mở bằng điện thoại. **Dữ liệu vẫn là LaTeX chuẩn**, nên hôm nào cần công
thức nặng hơn thì thay bộ vẽ mà không phải sửa một chữ nội dung.

Nhận: `**đậm**` · `*nghiêng*` · `` `mã` `` · gạch đầu dòng · danh sách đánh số ·
`### tiêu đề`; LaTeX `\frac{}{}` `\times` `\div` `^{}` `_{}` `\%` `\text{}`.
Lệnh lạ thì **giữ nguyên văn**, không nuốt — thà bé thấy `\sqrt` còn hơn thấy
chỗ trống.

### 2 · Bộ chuyển `tools/dinh_dang.py` — 7123 chỗ

**Nguyên tắc: thà bỏ sót còn hơn bọc nhầm.** Bọc nhầm một mẩu lời văn vào `$…$`
là bé thấy một cục chữ đơn cách giữa câu — xấu hơn lúc chưa sửa.

Ba lỗi tự gây, bắt được bằng cách **đếm chỗ ngờ** (không phải bằng cổng):

| lỗi | biểu hiện |
|---|---|
| loại trừ dấu phẩy cuối biểu thức | `9 - 4 = 5,` lùi còn `$9 - 4$` rồi bỏ `= 5` nằm trần |
| `-` và `:` không phân biệt khoảng với phép tính | `lớp 4-5`, `trang 1 - 9`, `Chương 6 - 7` bị bọc thành phép trừ |
| **`re.X` bỏ hết dấu cách trong mẫu** | `(?<!trang )` lặng lẽ thành `(?<!trang)` — chặn hoá ra không chặn gì |

Luật hiện tại: `-` và `:` chỉ là phép tính khi **có dấu cách hai bên**; cụm một
dấu đứng sau chữ chỉ thứ tự (`lớp`, `trang`, `Bài`…) thì coi là **khoảng**.

### 3 · Bài mẫu trình bày như vào vở — `tools/bai_mau.py`

**Cắt khúc, không viết mới.** Sách vốn đã có đủ mục, chúng chỉ nằm lẫn trong một
dãy phẳng 1634 dòng. Chỉ gắn nhãn `phan` rồi để giao diện gom:

```
261 TÓM TẮT · 540 PHÂN TÍCH · 415 BÀI GIẢI · 102 THỬ LẠI · 109 ĐÁP SỐ · 57 NÓI THÊM
150 dòng chỉ-là-tiêu-đề đã bỏ    ·    279/279 bài chia được
```

Màu theo **vai trò**: chỗ NGHĨ nền xám, chỗ VIẾT nền xanh, chỗ CHỐT nền vàng.

**ĐÁP SỐ là MỘT dòng chốt.** Bản đầu để nó "dính" nên mọi dòng sau `Đáp số: 108
đơn vị.` đều rơi vào mục ấy — đáp số dài ba dòng kèm cả lời bàn. Nay dòng sau
đáp số vào mục NÓI THÊM.

### 4 · Nối `<Chu>` vào mọi màn

Đề bài · lời giảng · nguyên tắc · bài mẫu · câu luyện tập · lời giải · gợi ý ·
dòng "Đáp án:" · kỳ sát hạch · vòng luyện chủ đề.

Một chỗ trượt và **chỉ lộ khi mở mắt xem**: màn giảng dùng `step.screen.narration`
(không có `?.`) nên phép thay hàng loạt trượt, và bé thấy nguyên văn
`$\frac{1}{1 \times 2}$` trên màn hình.

Phần PHÂN TÍCH (CHO GÌ · HỎI GÌ · ĐẠI LƯỢNG · QUAN HỆ · CHỌN CÔNG CỤ · ƯỚC LƯỢNG)
trước in thành một khối chữ sáu dòng dính nhau; nay mỗi mục một khung có nhãn.

---

## Việc còn lại

### 1 · TEST END-TO-END TRỌN VÒNG — làm trước tiên

Bác đã dặn "test end to end lại tất cả các phần: Mở bài, bài giảng, bài mẫu,
luyện tập, bài cuối rồi đến các gợi ý". Đợt này mới đi được:

- lớp 3 bài 21: trọn vòng mở bài → giảng → bài mẫu → luyện tập ✔
- lớp 4 bài 35 và 42: mở bài + giảng ✔
- lớp 5 bài 1: mở bài + giảng + màn bẫy ✔
- **CHƯA đi**: lớp 2 trọn vòng · màn kết (finale) · kỳ sát hạch sau khi đổi định
  dạng · vòng luyện chủ đề · Mùa giải (Quyển 2 — **chưa hề được định dạng**).

Nhớ nếp đã học: đi thật phải có **một lượt cố tình làm sai và cố tình phá**, chứ
không chỉ lượt làm đúng.

### 2 · CHỮ TRONG HÌNH VẪN KIỂU CŨ

368 hình của lớp 2·3·4 vẽ bằng matplotlib, chữ nằm sẵn trong PNG:

```
hình bài 35 lớp 4 vẽ "1/(1×2)"   trong khi lời văn cạnh nó đã là phân số xếp dọc
```

Sửa được: `figforge/arch_l2.py` là nơi vẽ chữ, thêm một bộ đổi `a/b` → hai dòng
có gạch ngang rồi vẽ lại toàn bộ (`ve_hinh_lop2.py`, `ve_hinh_lop4.py`). Nhớ chạy
`gan_hinh_*` sau đó, và **dựng lại thì mất định dạng** (xem dây chuyền ở trên).

### 3 · 984 CÂU LUYỆN TẬP KHÔNG CÓ GỢI Ý NÀO

| quyển | câu luyện tập | có gợi ý |
|---|---|---|
| lớp 2 | 281 | **0** |
| lớp 3 | 307 | **0** |
| lớp 4 | 396 | **0** |
| lớp 5 | 628 | 628 |

Giao diện đã có sẵn cơ chế **hai tầng gợi ý** (`hintState` trong `flow.js`): sai
lần 1 hiện gợi ý 1, sai lần 2 hiện gợi ý 2, sai lần 3 mở đáp án. Chỉ là dữ liệu
trống, nên bé lớp 2·3·4 sai mấy lần cũng không được giúp gì.

Đây là thiếu **nội dung**, không phải thiếu định dạng — phải viết tay, và nên
viết theo nếp của lớp 5: gợi ý 1 nhắc **hướng đi**, gợi ý 2 chỉ **bước đầu tiên**,
không cái nào nói ra đáp số.

### 4 · Hai chỗ nhỏ chưa đụng

- Công thức có **chữ cái** (`1/(a × b) = 1/a - 1/b`) chưa được bọc, vì luật đòi
  hai đầu là số. Có thể nới, nhưng phải đếm lại chỗ bọc nhầm trước.
- **109/168 tên bài lớp 5 dài quá 60 chữ** và bản thân cái tên đã là cách làm
  ("Vòng bốn 2·3·7·8: chia số thừa số cho 4 — đọc dư như máy định vị"). Đổi thì
  đổi cả danh sách chương và sổ phụ huynh.

---

Xem thêm `docs/tiep_theo_chu_de.md` (học theo chủ đề), `docs/tiep_theo_lop4.md`
(đường lùi từng bài) và `docs/CHUAN_DUA_SACH_VAO_APP.md` (44 cái bẫy).
