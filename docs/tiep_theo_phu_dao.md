# Điểm dừng — BÀI PHỤ ĐẠO VÀ HAI BỘ ĐO KB2 · KB3 · 26-08-2026

Ghi ngày 26-08-2026. **Đọc trang này trước khi động vào tầng hậu kiểm
(`lib/phongnoi.js`), vào luồng phụ đạo, hoặc trước khi dẫn số liệu KB2 · KB3 vào
luận văn.** Bản bàn giao trước, về Chương 2 và Chương 3, ở
`docs/tiep_theo_luan_van.md` (25-08) — vẫn đúng, trừ bốn số liệu đã sửa (mục 4).

Hôm nay bắt đầu bằng một việc đọc: rà toàn bộ Chương 2 và Chương 3 rồi đối chiếu
xuống mã. Việc đọc ấy đẻ ra một phát hiện không lường trước — **bốn hạng mục mà
luận văn mô tả như đang chạy thì thật ra chỉ có cổng kiểm gọi**, trong đó có
nhánh mà chính mục 2.5.1 gọi là "cốt lõi của tính thích ứng". Phần còn lại của
ngày là đi vá chỗ ấy.

---

## 1 · Trạng thái kho — ⚠ ĐỌC TRƯỚC

- Nhánh **`phu-dao-va-bo-do-kb2-kb3`**, 3 commit, **CHƯA PUSH**, cây sạch.
- `main` vẫn đứng ở `555201f3`, không bị động tới.
- 18 tệp, +1 930 dòng. `npm test` xanh (92/92 tệp cổng), `npm run build` xanh,
  `npm run test:luat` trên bộ giả lập **37 PASS · 0 FAIL**.

| Commit | Nội dung |
|---|---|
| `cc3a41c9` | Bộ đo KB3 · tách `soiCau` · vá hai lỗ hổng hậu kiểm |
| `ba8abfac` | Nối bài phụ đạo vào chặng luyện tập · luật `phudao` |
| `b6520941` | Công cụ KB2 · sửa 4 số liệu luận văn · bảng đối chiếu |

> ### ⚠ VIỆC PHẢI LÀM TRƯỚC KHI ĐƯA BẢN MỚI LÊN
>
> ```
> firebase deploy --only firestore:rules
> ```
>
> Commit `ba8abfac` thêm loại học bạ `phudao` vào `firestore.rules`. **Chưa
> deploy mà đẩy bản mới lên thì mọi bản ghi khung A-R-A bị Firestore từ chối
> TRONG IM LẶNG** — lệnh ghi không chờ kết quả, bé học xong, màn hình báo xong,
> máy chủ không có gì. Đúng cái bẫy mà chú thích trong `firestore.rules` đã
> cảnh báo là "không cổng nào canh được".

---

## 2 · Bốn hạng mục "có mã, không ai gọi" — tìm ra khi rà

Cả bốn đều đã đặc tả đầy đủ ở Chương 3, đều có cổng kiểm, và đều **chỉ được gọi
từ `web/test/`**. Soi bằng `grep` trên toàn bộ `web/src` và `web/functions`.

| Thuật toán | Hàm | Nay ra sao |
|---|---|---|
| 3.10 · dựng bài phụ đạo | `dungPhuDao` | ✅ **đã nối** — mục 3 |
| 3.9 · hàm chính sách π | `viecTiepCuaNut` | ✅ **đã nối** ở cấp NÚT; cấp BÀI (`viecTiepCuaBai` · `duocVuotAi`) vẫn chưa |
| 3.7 · cộng hưởng xuôi | `congHuong` | ❌ vẫn chưa ai gọi |
| 3.14 · cặp A-R-A | `capHopLe` · `deltaC` | ⚠ khung đã được GHI, nhưng chưa có bộ nối tính ΔC |

Bài học phương pháp, đáng ghi: **cổng kiểm xanh không chứng minh tính năng có
chạy.** Một hàm thuần viết đúng, có cổng đủ, vẫn có thể chưa từng chạm tới một
đứa trẻ nào. Muốn biết thì phải hỏi "ai GỌI nó lúc chạy", và câu ấy chỉ trả lời
được bằng cách grep toàn kho — không cổng nào tự nói ra.

---

## 3 · Bài phụ đạo nay CHẠY THẬT

`web/src/mon/tienganh/components/PhuDao.jsx` (mới) + nối ở
`BaiHoc.jsx` → `LuyenTap`. Bốn quyết định thiết kế, mỗi cái một lý do:

- **Đếm chuỗi sai TẠI MÁY** (`demSai`, `BaiHoc.jsx:839`), không đọc
  `mastery.saiLienTiep`. Hàm nền chạy sau khi bản ghi lên tới máy chủ — mục 3.1.3
  nói thẳng là có độ trễ — nên lúc bé sai câu thứ ba thì con số trên máy chủ còn
  là 0 hoặc 1. Và đếm theo **LƯỢT** chứ không theo câu, đúng định nghĩa `S_c` ở
  Bảng 3.12: đếm theo câu thì một câu sai bốn lần rồi đúng chỉ tính là một.
- **Hỏi chính `viecTiepCuaNut`** (`BaiHoc.jsx:869`), không so tay với hằng số.
  Gõ lại luật ở màn hình là dựng bản thứ hai của cùng một chính sách. Đi qua hàm
  thì bắt được cả nhánh `p < θ_yếu` mà một phép so `n >= 3` bỏ sót.
- **Mời, không cắt ngang**, và **tối đa MỘT lần mỗi lần mở bài**
  (`PHU_DAO_MOI_BAI`, `BaiHoc.jsx:767`). Mời lúc câu hiện tại đã xong chứ không
  lúc vừa chạm ngưỡng — chạm ngưỡng là lúc màn hình đang bày đáp án, đổi màn ngay
  là giật mất câu đang dở khỏi tay bé. Trần một lần vì `viecTiepCuaNut` trả PHỤ
  ĐẠO ở cả điều kiện `p < θ_yếu`, đúng ngay từ câu sai đầu tiên, nên một bài mười
  nút có thể mời tới mười lần.
- **Ghi KHUNG A-R-A, KHÔNG ghi mức tinh thông** (`ManTiengAnh.jsx:204`
  `xongPhuDao`). Máy con chỉ có bản `mastery` nạp lúc mở bài; ghi con số cũ vào
  thì ΔC sai theo hướng không ai lần ra. Chỉ giữ khung — nút mắc · nút gốc rễ ·
  câu đã hỏi trước · câu của bài phụ đạo · hai mốc thời gian — còn hai lần đo thì
  dựng lại được từ nhật ký `attempts`. Ghi **cả lần bé bấm "Để sau"**, nếu không
  thì tỷ lệ nhận lời mời không đo được và mọi ΔC đo trên phần còn lại là mẫu tự
  chọn.

### Đo trên toàn bộ dữ liệu

- **92/92 bài** dựng được bài phụ đạo.
- Nhóm nút CÓ cạnh tiên quyết: **129 ca** gốc rễ khác nút mắc → **105 ca** ra
  được bài · **67 ca** gốc nằm ở BÀI khác · **2 ca** ở QUYỂN khác.
- 24 ca còn lại không ra bài, chia hai loại: **19 ca** nút gốc rễ không có bài
  nào dạy (trường `b` rỗng — `sp_g4_self_intro` · `sp_g4_favourite` ·
  `sp_g4_countries`…), **5 ca** hậu kiểm bác hết vì vốn từ phiên hẹp hơn.

### ⚠ `goiLLM` CÒN ĐỂ TRỐNG — và đó là chủ ý

Bảng 3.23 khai bài phụ đạo là một trong ba vị trí gọi mô hình. Luồng nay đã
chạy, nhưng tham số gọi mô hình để `null`: bài phụ đạo lấy câu từ kho tĩnh.

Lý do (ghi đủ ở cuối `PhuDao.jsx`): hai vị trí kia chỉ cần mô hình sinh **một câu
tiếng Anh** hoặc một đoạn nhận xét, và `soiCau` soi được trọn vẹn. Một **CÂU
HỎI** thì phải thoả bảy luật ở mục 3.5.2 — phương án nhiễu cùng trường nghĩa,
không hai phương án cùng nghĩa, đúng một cách điền hợp lệ, gợi ý đi từ xa tới
gần — mà hậu kiểm theo vốn từ **không bắt được** những lỗi ấy. Bật lời gọi ở đây
mà chưa có tầng hậu kiểm cho bảy luật là mở đúng cửa mà cả tầng chống ảo giác
sinh ra để đóng.

---

## 4 · Hai lỗ hổng THẬT của tầng hậu kiểm — bộ đo KB3 tìm ra

Cả hai lộ ra ở **lượt chạy đầu tiên** của `tools/do_an_toan_noi_dung.mjs`.

### 4.1 · Ô trống chưa điền LỌT QUA

Bốn bài có công thức **hai ô** (`Is your sports day in + [Month A]? - … It's in +
[Month B].`). Phép điền — cả trong `soiCau` lẫn ở chỗ mô hình bắt chước — chỉ
thay ô **đầu**, nên ô sau còn nguyên. Mà `gonCau` bóc sạch dấu ngoặc trước khi
so, nên chuỗi khớp với chính nó và **được nhận**: cô giáo máy có thể đọc cho bé
nghe *"It's in month B."*

Vá ở `phongnoi.js:724` — bác thẳng mọi câu còn dấu ngoặc vuông, đặt **TRƯỚC** năm
đường công nhận vì cả `nuaMauCau` lẫn `congThuc` đều mù với dấu ngoặc. Lý do bác
riêng (`oTrong`), không gộp vào `ngoaiVon`: hai lý do khác loại nhau, gộp lại là
mất đúng thông tin cần để lần ra chỗ hỏng.

### 4.2 · Bác oan dạng biến đổi của từ đã học

Đường `congThuc` nhận `so_nhieu · so_it · dang_ing · dang_qk` từ lâu, **đường
`tu` thì không** — nên `"playing the violin"` bị bác trong khi lớp 5 unit 4 dạy
hẳn mục từ `play the violin` với `dang_ing` đúng bằng chuỗi ấy. Hai đường của
cùng một hàng rào lệch luật là chỗ không ai nghĩ để mà đi tìm.

Vá ở `phongnoi.js:740`. **Không phải nới rào** — dạng biến đổi lấy từ chính mục
từ vựng bé đã học; từ nào bài không dạy thì vẫn không có đường vào. Đo: over-
rejection **12 → 5** ca, phủ phụ đạo **98 → 105/129**, và bộ chứng KB3 vẫn
100%/100% với OOV = 0, tức nới đúng chỗ chứ không mở lỗ nào.

### 4.3 · Một chỗ nối hỏng

Chú thích cũ của `dungPhuDao` bảo "chỗ gọi thật PHẢI truyền `cauHopLe`", nhưng
`cauHopLe(en, opt)` nhận **CHUỖI** còn `soiCau` trong hàm ấy được gọi với **ĐỐI
TƯỢNG câu hỏi**. Làm đúng theo chú thích là bác sạch mọi câu — mà "rỗng" thì
trông y hệt "kho tĩnh không có gì". Thêm `enCuaCau()` (`phudao.js:71`) và
`cauHoiHopLe()` (`:102`) làm vỏ nối đúng kiểu.

Chính cổng vừa cắm cho vỏ ấy bắt tiếp một lỗi nữa của nó: thẻ chữ cái
`['b','a','l','l']` bị ghép thành `"b a l l"`. Phải phân biệt thẻ chữ cái với thẻ
từ theo **ĐỘ DÀI thẻ**, không theo "có thẻ khoảng trắng không".

---

## 5 · Hai bộ đo mới

### `tools/do_an_toan_noi_dung.mjs` — KB3, nhóm độ đo C

```
node tools/do_an_toan_noi_dung.mjs do            # không cần mạng
node tools/do_an_toan_noi_dung.mjs thu           # cần GROQ_API_KEY
node tools/do_an_toan_noi_dung.mjs do --vao docs/kb3_dau_ra_tho.json
```

Lệnh `do` dựng **BỘ CHỨNG** từ dữ liệu 30 bài: chứng dương nhắm đúng một đường
công nhận mỗi câu, chứng âm gồm từ vượt cấp · ô sai loại · ô chưa điền · câu lặp
· câu rỗng. Kèm **phép thử ĐẢO CHIỀU** — tắt từng đường rồi xem tỷ lệ bác có tăng
đúng ở nhóm tương ứng không. Kết quả hiện tại: 289 câu chứng, **149/149** chứng
dương, **140/140** chứng âm, **OOV sau hậu kiểm = 0**, cả năm đường đều chứng
minh được tác dụng.

> ⚠ **KHÔNG được đọc kết quả lệnh `do` thành kết quả về MÔ HÌNH.** Bộ chứng nói
> "hàng rào đóng đúng chỗ nó phải đóng"; nó **không** nói "mô hình hay sinh từ lạ
> tới mức nào". Con số **OOV thô** chỉ có nghĩa khi đã chạy `thu` — và chưa chạy
> thì đừng dẫn con số ấy vào luận văn.

### `tools/danh_gia_mo_hinh.mjs` — KB2 (và KB1), nhóm độ đo A

```
node tools/danh_gia_mo_hinh.mjs --tu-kiem        # 13/13
node tools/danh_gia_mo_hinh.mjs --mo-phong 1000  # không cần dữ liệu thật
node tools/danh_gia_mo_hinh.mjs --tu-may-chu     # cần khoá quản trị
```

Bốn biến thể M0–M3, đủ bốn độ đo Bảng 3.27, kiểm chéo **chia theo NGƯỜI HỌC**,
phân tầng đúng hai giả thuyết H1 và H2.

Hai chỗ dễ sai đã xử, ghi lại để đừng ai "đơn giản hoá" chúng đi:

- **AUC phải xử lý ĐỒNG HẠNG** bằng hạng trung bình. Lượt đầu của mọi nút đều cho
  ra cùng một giá trị dự đoán (đều xuất phát từ `P(L₀)`), nên công thức không xử
  lý đồng hạng sẽ thổi con số lên một cách có hệ thống. `--tu-kiem` có bốn ca
  đồng hạng canh chuyện này.
- **Bộ mô phỏng phải dùng MÃ NÚT THẬT** và phải có **đợt ôn lại sau quãng nghỉ**.
  Bản đầu bịa mã nút và không có đợt ôn: 100% số lượt rơi vào nhóm "cách dưới 7
  ngày" nên M1 và M2 trùng khít, và nhóm "có tiên quyết" rỗng nên M3 trùng M2.
  Con số đẹp mà cả hai giả thuyết đều không kiểm được.

> ⚠ `--mo-phong` là **dữ liệu MÔ PHỎNG**, không phải kết quả thật. Kết quả một
> lượt chạy 300 người học **cố ý KHÔNG commit** (`docs/kb2_ket_qua.json` đã xoá)
> — để một tệp tên "kết quả KB2" nằm trong kho thì sớm muộn có người trích vào
> Chương 4. `docs/kb3_ket_qua.json` thì CÓ commit, vì nó đo một tính chất thật
> của mã đang chạy.

---

## 6 · Bốn số liệu luận văn đã sửa

| Chỗ | Cũ | Mới |
|---|---|---|
| C2 · 2.2.1.b | "17 loại" đỉnh | **27 loại có khai** + 79 đỉnh bỏ trống trường loại |
| C2 · 2.4.1 | "chỉ được gọi ở ba vị trí" | "chỉ được **phép** gọi" — câu cũ đọc thành lời khai hiện trạng, mà hiện trạng là hai |
| C3 · Bảng 3.25 | 33 phép kiểm luật | **37**, và nói rõ bộ này cần bộ giả lập nên TÁCH khỏi 92 tệp kiểm ngoại tuyến |
| C3 · Bảng 3.23 · 3.5.1 · 3.5.3 · Bảng 3.29 | — | Nêu rõ bài phụ đạo đã nối vào luồng nhưng lấy câu từ kho tĩnh; "tỷ lệ dùng dự phòng" hiện **luôn bằng 0**, nghĩa là *chưa đo được* chứ không phải *tầng dự phòng tốt* |

Bảng đối chiếu đầy đủ ở **`docs/Doi_chieu_C2_C3_ma_nguon.xlsx`**, 9 sheet. Sheet 7
là khoảng trống của đợt rà; sheet 8 là những gì đợt này đã triển khai.

**Mọi con số quy mô đều tái lập được và ĐÚNG:** 4.226 câu (2.220+626+910+470) ·
94 bài (16·16·21·21·20) · 1.194 đỉnh · 253 cạnh (195+5+53) · phân bố 9 loại đỉnh
của Bảng 3.4 khớp từng dòng · 187/871/4 nút của Bảng 3.20 · 150 đỉnh có tiên
quyết đi vào · 38 cạnh xuyên lớp · 583 REQUIRES · 3.336 CONTAINS · 3.989/7.602
bản đầy đủ · 92 tệp cổng.

---

## 7 · VIỆC KẾ TIẾP, theo thứ tự

1. **Deploy luật** (mục 1) — chặn mọi việc khác nếu định đưa bản mới lên.
2. **Đi thử một buổi TRỌN VẸN trên bản chạy.** Luồng phụ đạo mới chỉ qua cổng và
   qua phép chạy thử headless; **chưa ai bấm bằng tay lần nào.** Kho này đã hai
   lần trả giá cho việc tin cổng xanh — xem `[[kiem-bang-mat-truoc-khi-deploy]]`.
   Cần thấy tận mắt: lời mời hiện đúng lúc, "Để sau" trả bé về đúng chỗ, làm hết
   4 câu thì quay lại đúng câu đang dở, và mục `phudao` có lên máy chủ thật.
3. **Chạy `thu`** với `GROQ_API_KEY` để có con số OOV thô — nửa còn thiếu của KB3.
4. **19 nút gốc rễ không có bài nào dạy.** Hoặc soạn học liệu cho chúng, hoặc cho
   phép lùi thêm một bước trên đồ thị khi nút gốc rễ không có bài. Phải báo con
   số này khi viết KB8 — nó thuộc đúng nhóm rủi ro mà mục 3.7.2.h đã lường trước.
5. **Bộ nối ΔC**: đọc mục học bạ `phudao`, dựng lại `p` tại hai mốc bằng phép chạy
   lại của `danh_gia_mo_hinh.mjs`, rồi đưa vào `capHopLe` · `gomTheoMau`. Xong cái
   này thì KB4 hết bị chặn.
6. **Cắm mô hình vào phụ đạo** + tầng hậu kiểm cho bảy luật của mục 3.5.2. Xong
   thì cập nhật lại Bảng 3.23 và mục 3.5.3.
7. `congHuong` (Thuật toán 3.7) vẫn chưa ai gọi — hoặc nối, hoặc phát biểu lại.
8. Còn nợ từ các bản trước: Chương 1 và Chương 4 · gửi Thầy Chương 3 · ba chú
   thích "không màn nào đọc `reviewQueue`" nay sai với Tiếng Anh · cài ESLint ·
   `sessionId` của Toán nên mang cả `learnerId`.

---

## 8 · Những cái bẫy đã trả giá để biết — ĐỪNG DẪM LẠI

- **Cổng xanh không chứng minh tính năng có chạy.** Bốn thuật toán có cổng đủ mà
  không ai gọi. Muốn biết thì grep `web/src` và `web/functions` xem ai GỌI.
- **Sửa hàng rào thì phải đo lại hàng rào.** Cả hai lần nới `soiCau` hôm nay đều
  chạy lại bộ chứng KB3 ngay sau đó, để chắc là nới đúng chỗ chứ không mở lỗ. Nếu
  không có bộ chứng thì hai lần nới ấy là hai lần đoán.
- **Bộ đo cũng sai được, và sai trước cả mã.** Lượt chạy đầu của KB3 báo 5 "chứng
  dương bị bác oan" và 1 "chứng âm lọt qua" — **cả sáu đều là lỗi của bộ đo**,
  không phải của hàng rào: cắt nửa câu máy móc ở `" - "`, và dựng chứng âm
  `"This is Bill."` mà quên rằng bài ấy dạy hẳn mẫu `This is + [Name].` Đọc vội
  là đi sửa nhầm `soiCau`.
- **`viecTiepCuaNut` trả PHỤ ĐẠO ở HAI điều kiện**, không phải một. Điều kiện
  `p < θ_yếu` đúng ngay từ câu sai đầu tiên — ai bỏ `PHU_DAO_MOI_BAI` đi thì một
  bài mười nút sẽ mời mười lần.
- **`enCuaCau` không được lấy `solutionNarrative`.** Chuỗi ấy trộn tiếng Anh với
  nghĩa tiếng Việt trong một dòng; soi nó bằng vốn từ tiếng Anh thì bác nhầm gần
  hết.
- **`npm test` chạy vòng lặp shell, không phải `node --test`.** Gõ `node --test
  test/` thì hỏng — xem khoá `"//test"` trong `web/package.json`. Bộ kiểm luật
  thì gọi riêng bằng `npm run test:luat` **sau khi** `npm run gia-lap` đã chạy.
