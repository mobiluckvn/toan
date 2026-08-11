# Khảo sát — BẢN ĐỒ TRI THỨC TIẾNG ANH LỚP 1-12 (v10)

Ghi 2026-08-11. Nguồn: `docs/ban_do_tri_thuc_tieng_anh_1_12_lien_thong_full_v10.json.zip`,
đã bung ra `data/ban_do_tieng_anh.json` (3,5 MB).

Bộ Global Success · NXB Giáo dục Việt Nam - Pearson · theo Thông tư 32/2018/TT-BGDĐT.

---

## 1 · ĐÂY LÀ BẢN ĐỒ, KHÔNG PHẢI SÁCH

Cần nói rõ ngay: tệp này **không có một câu hỏi nào, một bài tập nào, một lời giảng
nào**. Nó là đồ thị `G = (V, E)` mô tả *dạy CÁI GÌ và cái gì cần cái gì trước* — đúng
vai trò của `data/km_v1_38.json` bên Toán.

Muốn có bài để bé học thì vẫn cần **bộ sách**. Bản đồ này là thứ nói cho phần mềm biết
sắp xếp các bài ấy ra sao.

---

## 2 · CHẤT LƯỢNG CẤU TRÚC: RẤT TỐT

```
3 989 node · 7 602 cạnh · 12 lớp (1 → 12)
0 cạnh treo · 0 vòng lặp trong REQUIRES · 0 tự trỏ · 0 cạnh trùng · 0 mã trùng
```

Bốn con số 0 cuối là thứ hiếm. Bản đồ chủ đề Toán của mình phải soát tay mới ra
"0 dạng thủng"; bộ này tự khai và soát lại thì đúng.

**17 loại node** — `course · program · theme · unit · section · topic · skill ·
skill_category · function · project · review · reading_text · vocabulary_set ·
vocabulary · sentence_pattern · phonics · prior_knowledge`

```
vocabulary        2 683      sentence_pattern    439
phonics             251      unit                176
section             104      skill                96
vocabulary_set       52      review               40
theme                38      prior_knowledge      28
function             24      course/topic/project 12 mỗi loại
```

### Ba thứ đáng giá nhất

**(a) `REQUIRES` — đồ thị tiên quyết, 583 cạnh, 199 xuyên lớp.**
Đây chính là cơ chế "thang" của màn Học theo chủ đề bên Toán, nhưng **giàu hơn nhiều**:
bên Toán mình phải dựng tay `chu_de_tay.json`; ở đây sách đã khai sẵn.

```
Present continuous          ⇐ cần  Present simple
Wh-questions                ⇐ cần  Present simple · Present continuous
Quantifiers many/much…      ⇐ cần  Countable and uncountable nouns
```

**(b) `bkt_params` có trên 3 373/3 373 node nguyên tử** — `p_l0 · p_transit · p_guess ·
p_slip`, đúng bốn tham số mô hình BKT mà `functions/src/bkt.js` đang dùng cho Toán.
Nghĩa là **hàm `applyAttempt` chạy được ngay**, không phải viết lại.

**(c) CEFR trên mọi node**: Pre-A1 (lớp 1-3) → A1 (4-5) → A1-A2 (6) → A2 (7-9) → B1
(10-12). Đây là "thang lớp" có sẵn, dùng để xếp bậc luyện và để nói với bố mẹ con đang
ở đâu bằng một thước quốc tế.

---

## 3 · CHỖ CÒN THỦNG — phải bù trước khi dạy

| lớp | CEFR | unit | từ | nghĩa Việt | IPA | mẫu câu | phát âm |
|---|---|---|---|---|---|---|---|
| 1 | Pre-A1 | 16 | 60 | **0/60** | **0/60** | 19 | 16 |
| 2 | Pre-A1 | 16 | 56 | 56/56 | 56/56 | 18 | 16 |
| 3 | Pre-A1 | 21 | 204 | 185/204 | 184/204 | 42 | 40 |
| **4** | **A1** | 25 | 233 | **233/233** | **233/233** | 48 | 40 |
| **5** | **A1** | 20 | 187 | **187/187** | **187/187** | 40 | 20 |
| 6 | A1-A2 | 12 | 310 | 310/310 | 309/310 | 22 | 12 |
| 7 | A2 | 12 | 374 | **0/374** | **0/374** | 43 | 24 |
| 8 | A2 | 12 | 291 | **0/291** | **0/291** | 45 | 18 |
| 9 | A2 | 12 | 248 | 135/248 | 135/248 | 18 | 12 |
| 10 | B1 | 10 | 230 | 230/230 | **0/230** | 54 | 28 |
| 11 | B1 | 10 | 215 | 215/215 | **0/215** | 40 | 10 |
| 12 | B1 | 10 | 275 | 275/275 | **0/275** | 50 | 15 |

* **857/2 683 từ (32%) chưa có nghĩa tiếng Việt** — thủng trọn ở lớp 1, 7, 8.
* **1 579/2 683 từ (59%) chưa có phiên âm IPA** — thủng trọn ở lớp 1, 7, 8 và **cả ba
  lớp 10·11·12**.
* **72/439 mẫu câu thiếu công thức**, 33 thiếu ví dụ.
* **KHÔNG có một trường âm thanh nào** — đã soát mọi tên trường của 3 989 node. Đúng
  như dự đoán ở `docs/khao_sat_tieng_anh.md`.
* **Unit lớp 7-12 không có tên bài đọc được**: chỉ có `topic` (vd `"Hobbies"`), còn
  `label` là `"Unit"` — nhãn LOẠI, không phải tên. Lớp 1-6 thì có `label_vi`/`label_en`
  tử tế. Hiện thẳng lên màn là bé thấy 12 dòng "Unit" giống hệt nhau.
* **Mã node lớp 6 không có tiền tố lớp** (`u1`, `v_activity`, `g_present_simple`) trong
  khi lớp 7-12 thì có (`u_g7_1`, `sp_g7_u7_1`). Hiện chưa trùng nhau, nhưng đây là loại
  bất nhất mà thêm dữ liệu vào là vỡ.

---

## 4 · NÊN BẮT ĐẦU TỪ LỚP 4 VÀ LỚP 5

Ba lý do cùng chỉ về một chỗ:

1. **Dữ liệu đủ nhất**: 100% từ có nghĩa Việt và 100% có IPA — hai lớp duy nhất trọn
   vẹn cả hai, cùng lớp 2 (nhưng lớp 2 chỉ có 56 từ).
2. **Trùng đúng lứa đang có sách Toán** (lớp 2-5) — bé đang học Toán lớp 4-5 là người
   dùng sẵn có, không phải đi tìm người học mới.
3. **CEFR A1** là mức khởi đầu tự nhiên, có phonics đầy đủ (40 và 20 node).

Làm xong hai lớp ấy thì đường mở rộng rõ: xuống lớp 3 (đã gần đủ), rồi lên lớp 6.
Lớp 7·8 phải bù 665 nghĩa Việt + 665 IPA trước — việc của người soạn, không phải của
phần mềm.

---

## 5 · KHÔNG ĐƯỢC ẢNH HƯỞNG MÔN TOÁN — đây là phần quan trọng nhất

Bác dặn đúng chỗ cần dặn. Cháu soát cụ thể: có **bốn tệp dùng chung** mà Tiếng Anh
chạm vào là Toán chịu hậu quả, và **một tệp thêm vào thì an toàn**.

### An toàn — chỉ THÊM, không sửa
`data/chuong_trinh.json`: thêm một mục vào `chuongTrinh`. Kệ sách, HomeQuyen, sổ bố mẹ,
bảng cô giáo, bảng xếp hạng đều tự hiện. Cổng `kesach.test.mjs` canh sẵn mọi trường.
Thư mục `data/tienganh/` và `web/public/content/tienganh/` là mới hoàn toàn.

### ⚠ Bốn chỗ NGUY HIỂM

**(1) `web/src/lib/flow.js` — bộ chấm dùng chung cho 1 612 câu Toán.**
Sửa `checkAnswer` để nó hiểu tiếng Anh là đụng thẳng vào chỗ chấm bài của cả bốn quyển
Toán đang chạy thật. **Phải TÁCH `chamTiengAnh()` riêng**, `flow.js` chỉ rẽ nhánh theo
môn. Và phải có phép kiểm khẳng định *"kết quả chấm của Toán không đổi một câu nào"* —
không thì hỏng kiểu im lặng, cổng vẫn xanh.

**(2) `web/test/luat_o_nhap.test.mjs` — cổng này TỰ ĐỌC SỔ ĐĂNG KÝ.**
Cháu đọc kỹ: nó lặp qua **mọi** mục trong `chuongTrinh` có `thuMuc` tồn tại và chứa
`D[LR]_*.json`, rồi áp cả năm luật. Nghĩa là **khai quyển Tiếng Anh vào sổ là cổng đỏ
NGAY**, vì:

* luật 1 cấm ô gõ chữ ở quyển đọc chậm — mà tiếng Anh thì **gõ chữ chính là kỹ năng
  đang dạy**;
* luật 5 đòi máy chấm ≥ 85% câu luyện tập — kỹ năng nói và viết đoạn thì không đạt.

👉 **Sửa luật cho hỏi MÔN trước, rồi mới khai quyển.** Làm ngược lại thì người sửa vội
sẽ tắt luật cho cả bốn quyển Toán — mất luôn hàng rào đã cứu lớp 3 và lớp 4.

**(3) `tools/dinh_dang.py` — bọc LaTeX.**
Nó lấy danh sách quyển từ một mảng cứng trong chính tệp ấy, nên **chỉ cần KHÔNG thêm
Tiếng Anh vào mảng đó**. Thêm nhầm là nó bọc bậy hàng loạt (`and/or`, `he/she`,
`3/4 of the class`) mà dữ liệu vẫn hợp lệ nên cổng vẫn xanh.

**(4) `data/chu_de.json` + màn Học theo chủ đề.**
Đây là bản đồ 5 mảng → 82 dạng của **Toán**. Trộn bản đồ tiếng Anh vào là màn chủ đề
lẫn "Phân số" với "Present Simple". **Phải tách bản đồ theo MÔN** — và may là bản đồ
tiếng Anh đã có sẵn cấu trúc riêng, không cần ép vào khuôn Toán.

### Một chỗ nữa: bảng xếp hạng
Công thức sao hiện **không biết môn**. Hai môn chung một bảng thì một bài Toán và một
bài Tiếng Anh ngang giá nhau — bác có muốn thế không, hay tách hai bảng? Cần quyết
trước khi quyển Tiếng Anh đầu tiên lên kệ.

---

## 6 · VIỆC CẦN LÀM, THEO THỨ TỰ

1. **Bù dữ liệu thiếu cho lớp 4·5** — thật ra hai lớp này đã đủ, nên bước này bỏ qua
   được. Đó chính là lý do chọn chúng.
2. **Quyết âm thanh** (mp3 kèm nội dung / máy đọc / trộn) — đổi hình dạng dữ liệu nên
   phải quyết trước khi bóc tách.
3. **Sửa `luat_o_nhap` cho hỏi MÔN** — làm TRƯỚC khi khai quyển vào sổ.
4. **Tách bộ chấm tiếng Anh** khỏi `flow.js`, kèm cổng canh "Toán không đổi".
5. **Bác gửi bộ sách Tiếng Anh lớp 4 (hoặc 5)** — bản đồ nói dạy cái gì, sách mới cho
   bài để bé học.
6. Dựng thử **một unit** trước, đừng làm cả quyển.

---

Xem thêm `docs/khao_sat_tieng_anh.md` (khảo sát mã nguồn, viết trước khi có bản đồ)
và `docs/CHUAN_DUA_SACH_VAO_APP.md` (44 cái bẫy khi bóc tách sách).
