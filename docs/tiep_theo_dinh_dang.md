# Điểm dừng — ĐỊNH DẠNG NỘI DUNG (markdown + LaTeX)

Cập nhật 2026-08-11 (lượt hai). Đọc tệp này TRƯỚC khi động vào lời văn hay cách trình bày bài.

> **ĐANG CHẠY trên ky-su-nhi.web.app.** Cổng: 29 tệp kiểm · 836 PASS · 0 FAIL.
> Ba việc tồn của đợt trước ĐÃ XONG (2026-08-11). Việc còn lại nay khác — xem cuối tệp.

---

## MAI VÀO VIỆC TỪ ĐÂU

Làm theo đúng thứ tự này, vì việc trước có thể lộ thêm việc cho việc sau:

1. **Viết gợi ý RIÊNG cho từng câu** — hiện mọi câu trong một bài dùng chung hai
   gợi ý; cổng canh sẵn rồi.
2. **Nới luật cho công thức có chữ cái** — đếm chỗ bọc nhầm trước khi nới.
3. **Rút gọn 109 tên bài lớp 5.**

---

## Dây chuyền — THỨ TỰ LÀ BẮT BUỘC

```
① dựng      python3 tools/dung_khuon_chung.py        (lớp 2)
            python3 tools/dung_khuon_chung_lop3.py
            python3 tools/dung_khuon_chung_lop4.py
② gắn hình  python3 tools/gan_hinh_lop2.py           (rồi dựng lại lớp 2)
③ định dạng python3 tools/dinh_dang.py               → markdown + LaTeX
④ bài mẫu   python3 tools/bai_mau.py                 → cắt phần Tóm tắt/Giải/Đáp số
⑤ gợi ý     python3 tools/goi_y.py                   → hai tầng gợi ý cho lớp 2·3·4
⑥ cổng      cd web && npm test && npm run build
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

### ✔ (2026-08-11) Ba việc của đợt trước ĐÃ XONG

**① Soát định dạng toàn bộ** — soi bằng máy cả năm quyển, tìm ra bốn chỗ hổng:
Mùa giải chưa hề được định dạng (tệp mang tiền tố `DR_`, bộ chuyển chỉ lọc `DL_`);
chuỗi đã có `$` thì bị bỏ qua CẢ chuỗi nên nửa còn lại mắc kẹt; luật phân số chặn
nhầm dấu phẩy và chữ đứng sau; thiếu 11 trường chữ. Nay chạy tới khi ĐỨNG YÊN.

**② Vẽ lại hình** — hoá ra chỉ **9 hình**, không phải 368 (sổ cũ đếm nhầm tổng số
hình). Matplotlib vẽ mathtext sẵn. Phải sửa thêm `fit_fs` (đếm nguyên văn nên nhãn
có công thức bị thu bé tí) và nhãn dưới hình bánh (bộ vẽ tự ghép `{tu}/{mau}`).

**③ 984 gợi ý** — gắn được 955/984 câu, suy từ lời GIẢNG của chính bài. Cổng mới
rồi bắt ngược lại **21 gợi ý của lớp 5 do người soạn viết nói thẳng đáp án**, đã
viết lại cả 21.

Hai cổng mới: `goi_y.test.mjs` và `chu_vao_man.test.mjs` (đọc MÃ NGUỒN tìm chỗ in
thẳng trường có LaTeX — nó bắt ngay 13 chỗ bỏ sót, gồm lời chào màn mở bài và cả
màn Mùa giải chưa từng nối).

---

## Việc còn lại

### 1 · GỢI Ý MỚI THEO BÀI, CHƯA THEO CÂU

Mọi câu trong cùng một bài đang dùng chung hai gợi ý (lấy từ câu chốt và bước
giảng đầu). Lớp 5 thì mỗi câu một gợi ý riêng do người soạn viết — đó là bậc trên.
Viết riêng cho 984 câu vẫn là việc còn để lại; cổng `goi_y.test.mjs` đã sẵn sàng
canh cho việc ấy (không được nói ra đáp án · không quá 160 chữ · không cắt giữa
công thức).

29 câu hiện KHÔNG có gợi ý nào, vì cả hai tầng đều chứa nguyên văn đáp án của
chính câu ấy nên bị bỏ.

### 2 · CÔNG THỨC CÓ CHỮ CÁI

`1/(a × b) = 1/a - 1/b` chưa được bọc, vì luật đòi hai đầu là SỐ. Nới được, nhưng
phải đếm lại chỗ bọc nhầm trước — "km/h", "N/A", "và/hoặc" đều có dạng `chữ/chữ`.

### 3 · TÊN BÀI LỚP 5

109/168 tên dài quá 60 chữ và bản thân cái tên đã là cách làm ("Vòng bốn 2·3·7·8:
chia số thừa số cho 4 — đọc dư như máy định vị"). Đổi thì đổi cả danh sách chương,
màn chủ đề và sổ phụ huynh.

---

Xem thêm `docs/tiep_theo_chu_de.md` (học theo chủ đề), `docs/tiep_theo_lop4.md`
(đường lùi từng bài) và `docs/CHUAN_DUA_SACH_VAO_APP.md` (44 cái bẫy).
