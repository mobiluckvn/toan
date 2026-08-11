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
① dựng      python3 tools/dung_khuon_chung.py        (lớp 2 — NẠP data/loi_chao.json)
            python3 tools/dung_khuon_chung_lop3.py
            python3 tools/dung_khuon_chung_lop4.py
② hình lớp2 python3 tools/ve_hinh_lop2.py            → vẽ PNG
            python3 tools/gan_hinh_lop2.py           → gắn vào bài (rồi dựng lại lớp 2)
③ mở bài L5 python3 tools/mo_bai_lop5.py             → nêu đề bài, bỏ đoạn thoại nói hai lần
④ định dạng python3 tools/dinh_dang.py               → markdown + LaTeX
⑤ bài mẫu   python3 tools/bai_mau.py                 → cắt phần Tóm tắt/Giải/Đáp số
⑥ gợi ý     python3 tools/goi_y.py                   → hai tầng gợi ý cho lớp 2·3·4
⑦ cổng      cd web && npm test && npm run build
```

⚠ **④ và ⑤ sửa thẳng bản DỰNG** (`web/public/content`), mà bộ dựng ① thì ghi đè
trọn tệp từ bản gốc. **Chạy ① sau ④⑤ là mất sạch định dạng — dữ liệu vẫn hợp lệ và
KHÔNG CÓ GÌ BÁO.** Đúng cái bẫy đã dính với việc gắn hình ở Quyển 2.

③ thì KHÔNG dính bẫy ấy: lớp 5 không có bộ dựng khuôn chung, và `mo_bai_lop5.py`
ghi **cả `data/lessons/` lẫn `web/public/content/lessons/`** — chạy lại lúc nào
cũng được.

---

## Đã làm ở đợt này

### 1 · MÀN MỞ BÀI — nêu vấn đề, KHÔNG nói trước cách làm

Chỗ này chưa sổ nào ghi, mà nó là **cơ chế**, không phải một lần sửa nội dung.

**Lớp 2·3·4 — `data/loi_chao.json`, 111 lời chào viết tay** (33 + 34 + 44 = đủ mọi
bài). Bộ dựng `khuon_chung.py` nạp tệp này lúc nạp mô-đun và đặt vào
`objective.kidText`, kèm cờ **`objective.laLoiChao`**. Bài nào thiếu thì rơi về
mục tiêu giáo án và cổng `web/test/loi_chao.test.mjs` bắt ngay.

Tệp giữ luôn ba khoá tài liệu `_doc` · `_luat` · `_vi_sao` — **đọc `_luat` trước
khi viết thêm lời chào cho quyển mới.** Tóm tắt: một tình huống, tối đa hai câu,
không nói cách làm, không chữ nghề, kết bằng câu hỏi hoặc lời rủ.

Vì sao phải làm: mở bài trước đây in nguyên mục tiêu giáo án — **30/33 bài lớp 2,
32/34 lớp 3 và 44/44 lớp 4 dài quá 170 chữ**, lại nói sẵn cách làm. `kidText` chỉ
là bản sao y của `text` chứ chưa từng có bản viết cho trẻ.

**Cờ `laLoiChao` điều khiển `flow.js:663`** — quyển CÓ lời chào thì màn mở là lời
chào, còn `hook` đẩy sang màn sau; quyển KHÔNG có (lớp 5, Mùa giải) thì màn mở
vẫn là `hook` như cũ. Bản đầu tôi gộp intro+hook cho **mọi** quyển, thành ra lớp 4
nêu cùng một đề bài hai lần liền.

**Lớp 5 — `tools/mo_bai_lop5.py`.** Bệnh khác hẳn: màn mở nói **cùng một đoạn
thoại hai lần** — một lần bằng lời (trung bình 208 chữ), một lần nữa bằng hình
`character_speech` chép lại đúng hai câu ấy (155 chữ). Bé đọc 363 chữ mà vẫn chưa
thấy đề bài. Nay lời mở là **một câu nêu bài toán** lấy từ
`knowledgeCore.canonicalExamples[0].problem`; hình mở chỉ giữ **câu SAI** (cái bẫy),
bỏ câu phản bác vì nó thuộc màn giảng ngay sau. Bài hình học thì màn mở phải là
**hình vẽ thật**, và chính hình ấy đi tiếp vào phần giải (`usedIn` mang cả hai
chặng) để bé nhìn một hình từ đầu đến cuối.

Cũng ở đợt này: bỏ ô "NGUYÊN TẮC CẦN NHỚ" khỏi màn mở — bác nói đúng, *mở bài mà
đã có kiến thức cần nhớ thì còn gì để đọc*. Câu chốt nay có màn riêng đặt SAU khi
giảng xong. Chỗ ẩn: `figFor(lesson,'mantra')` có đường lui kéo đúng tấm thẻ ấy trở
lại màn vừa dọn — đã bỏ đường lui đó.

### 2 · Bộ hiển thị markdown + LaTeX

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

### 3 · Bộ chuyển `tools/dinh_dang.py` — 7123 chỗ

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

### 4 · Bài mẫu trình bày như vào vở — `tools/bai_mau.py`

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

### 5 · Nối `<Chu>` vào mọi màn

Đề bài · lời giảng · nguyên tắc · bài mẫu · câu luyện tập · lời giải · gợi ý ·
dòng "Đáp án:" · kỳ sát hạch · vòng luyện chủ đề.

Một chỗ trượt và **chỉ lộ khi mở mắt xem**: màn giảng dùng `step.screen.narration`
(không có `?.`) nên phép thay hàng loạt trượt, và bé thấy nguyên văn
`$\frac{1}{1 \times 2}$` trên màn hình.

Phần PHÂN TÍCH (CHO GÌ · HỎI GÌ · ĐẠI LƯỢNG · QUAN HỆ · CHỌN CÔNG CỤ · ƯỚC LƯỢNG)
trước in thành một khối chữ sáu dòng dính nhau; nay mỗi mục một khung có nhãn.

---

## Ba việc tồn của đợt trước — ĐÃ XONG (2026-08-11)

### ① Soát định dạng toàn bộ — soi bằng máy cả năm quyển, tìm ra bốn chỗ hổng:
Mùa giải chưa hề được định dạng (tệp mang tiền tố `DR_`, bộ chuyển chỉ lọc `DL_`);
chuỗi đã có `$` thì bị bỏ qua CẢ chuỗi nên nửa còn lại mắc kẹt; luật phân số chặn
nhầm dấu phẩy và chữ đứng sau; thiếu 11 trường chữ. Nay chạy tới khi ĐỨNG YÊN.

### ② Vẽ lại hình — hoá ra chỉ **9 hình**, không phải 368 (sổ cũ đếm nhầm tổng số
hình). Matplotlib vẽ mathtext sẵn. Phải sửa thêm `fit_fs` (đếm nguyên văn nên nhãn
có công thức bị thu bé tí) và nhãn dưới hình bánh (bộ vẽ tự ghép `{tu}/{mau}`).

### ③ 984 gợi ý — gắn được 955/984 câu, suy từ lời GIẢNG của chính bài. Cổng mới
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
