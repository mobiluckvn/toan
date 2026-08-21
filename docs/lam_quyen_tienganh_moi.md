# LÀM MỘT QUYỂN TIẾNG ANH MỚI — sổ tay

*Viết khi làm lớp 4 (20-08-2026), bổ sung khi làm lớp 5 (21-08-2026).*

Bác chốt 20-08-2026: *"Hãy lưu lại hết các rule để chúng ta bắt đầu sang lớp 4."*

Tệp này là **danh sách việc**, không phải bài giảng. Mọi chỗ nêu đường dẫn đều đã
mở ra kiểm ngày 20-08-2026, không chép từ trí nhớ.

Năm quyển `ta1` … `ta5`. Mỗi quyển mới lại lộ ra một chỗ dây chuyền chưa biết
làm — mục 8 ghi lại những chỗ ấy.

---

## 0 · ĐỌC TRƯỚC, ĐỪNG DỰNG LẠI TỪ ĐẦU

| tệp | nói gì |
|---|---|
| `docs/day_chuyen_du_lieu_tienganh.md` | 14 tầng dữ liệu: tầng nào đẻ ra tầng nào |
| `docs/lam_bai_tranh.md` | bài tả tranh — 8 luật, mỗi luật đổi bằng một lỗi thật |
| `docs/CHUAN_DUA_SACH_VAO_APP.md` | 44 cái bẫy khi bóc tách một quyển sách mới |
| tệp này | chỗ nào phải sửa khi THÊM QUYỂN, và thứ tự chạy |

Bộ sinh đã nhận `--lop` gần như khắp nơi. Việc của lớp 4 **phần lớn là khai
thêm**, không phải viết mới.

---

## 1 · ĐÃ CÓ SẴN GÌ

**Bản đồ tri thức đã có lớp 4.** `data/ban_do_tieng_anh.json` → `graph.nodes`
đếm theo `grade`:

```
lớp 1: 120   lớp 2: 117   lớp 3: 321   lớp 4: 359   lớp 5: 272   …
```

⚠ **KHÔNG SỬA `ban_do_tieng_anh.json`.** Nó là bản gốc. Thiếu gì thì bù ở
`data/tienganh/lop4_bu.json` — xem tầng ② của dây chuyền.

---

## 2 · MƯỜI MỘT CHỖ PHẢI KHAI THÊM `ta4`

Khai sót một chỗ thì **không có gì đỏ** — bộ sinh lặng lẽ bỏ qua quyển mới, hoặc
giao diện lặng lẽ hiện quyển rỗng. Đây là danh sách đầy đủ, đã grep ra:

### a) Bảng `QUYEN` trong `tools/` — SÁU tệp

```
tools/kho_cau_tienganh.py:51        QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}
tools/sinh_bai_tienganh.py:45       (như trên)
tools/sinh_dochieu_tienganh.py:65   (như trên)
tools/sinh_vietbai_tienganh.py:46   (như trên)
tools/sinh_bai_tranh.py:40          (như trên)
tools/tranh_tienganh.py:58          (như trên)
```

Thêm `4: "ta4"` vào cả sáu. (`tools/dung_chu_de.py` cũng có một bảng `QUYEN`
nhưng đó là của môn TOÁN — đừng đụng.)

⚠ **CÒN HAI BẢNG NỮA, KHÔNG TÊN `QUYEN`** — danh sách này lúc đầu bỏ sót cả hai,
và cả hai đều làm bộ sinh vỡ giữa chừng khi làm lớp 4 thật:

```
tools/sinh_bai_tienganh.py   TIEN_TO = {1: "DL:TA1.", …}   ← KeyError: 4
tools/soat_hinh_tienganh.py  SO_SOAT = {1: …hinh_da_soat.md, …}
```

Cách tìm cho chắc, đừng tin danh sách này:

```
grep -rn "= {1:" tools --exclude-dir=tts --exclude-dir=__pycache__
grep -rn "choices=\[1, 2, 3" tools --exclude-dir=tts --exclude-dir=__pycache__
```

### b) `tools/soat_hinh_tienganh.py`

```
SO_SOAT = {1: …/hinh_da_soat.md, 2: …_lop2.md, 3: …_lop3.md}   ← thêm 4
p.add_argument('--lop', …, choices=[1, 2, 3])                   ← thêm 4
```

⚠ Chính tệp này từng ghim cứng `ta1`, nên **204 từ lớp 3 đi suốt hai quyển không
ai nhìn hình mà mọi cổng vẫn xanh**. Đừng để lặp lại.

### c) Cổng — NĂM tệp khai danh sách quyển

```
web/test/tienganh_bai.test.mjs:30
web/test/tienganh_dochieu.test.mjs:75
web/test/tienganh_hinh_dung_tu.test.mjs:43
web/test/tienganh_phongnoi.test.mjs:721
web/test/tienganh_video.test.mjs:36
```

đều là `['ta1', 'ta2', 'ta3']` → thêm `'ta4'`.

⚠ Mấy cổng này lọc `.filter(q => existsSync(...))`, nên **thêm tên quyển vào mà
chưa có tệp thì cổng im lặng bỏ qua** — glob rỗng báo 0 lỗi. Thêm tên NGAY khi
tạo thư mục, đừng để sau.

### d) Cổng ghim cứng `tranh_lop3.json` — HAI tệp

```
web/test/tienganh_dochieu.test.mjs:28
web/test/tienganh_chamviet.test.mjs:26
```

Cả hai đọc thẳng `data/tienganh/tranh_lop3.json`. Có `tranh_lop4.json` thì phải
nới ra đọc cả hai, nếu không bức tranh lớp 4 **không ai soi**.

### e) Sổ đăng ký quyển — `web/public/content/chuong_trinh.json`

Chép khối `"ta3"` (dòng ~515) thành `"ta4"`. Mấy khoá dễ sai:

| khoá | lưu ý |
|---|---|
| `thuTu` | **không trùng trên CẢ kệ sách**, không phải trong nhóm. Cổng canh đúng chuyện này. |
| `am.so` | `tienganh/lop4_am.json` — sổ tra RIÊNG từng quyển, nhưng `am.thuMuc` thì DÙNG CHUNG `tienganh/audio` |
| `bai` | liệt kê đủ `DL:TA4.B00…` — thiếu bài nào thì bài ấy không lên kệ |
| `soBai` · `soChuong` | phải khớp số tệp thật; có cổng đếm |
| `khoaBai` | lớp 1·2·3 để `false`. Đừng bật nếu bác chưa chốt. |

⚠ Xem `[[them-quyen-moi-vao-app]]`: **mọi chỗ giao diện so tên quyển đều hỏng
câm**. Đừng viết `if (ma === 'ta3')` ở bất kỳ đâu — hỏi CỜ trong sổ đăng ký.

### f) Bộ soạn tranh

Chép `tools/soan_tranh_lop3.py` → `soan_tranh_lop4.py`. Sửa:

* mọi `3` thành `4` (đường dẫn, `kho_chu(3, …)`, `hinh_cua_tu(3, …)`);
* `bai_lop12()` — hàm mượn vật; lớp 4 mượn được của **ta1 · ta2 · ta3**, sửa
  danh sách `("ta1", "ta2")` ở dòng ~134;
* bốn bảng phải xem lại theo sách của quyển ấy:
  `VAI_VAT` / `VAI_BO` · `KHONG_DEM` · `NGUOI_MA` · `UU_TIEN`.

---

## 3 · THỨ TỰ CHẠY — SAI THỨ TỰ LÀ MẤT SẠCH

```
② phần bù          soạn tay data/tienganh/lop4_bu.json   (từ bản đồ gốc)
③ bản chuẩn        python3 tools/chuan_tienganh.py --lop 4
④ bài học          python3 tools/sinh_bai_tienganh.py --lop 4 --tat-ca
⑥ đề ôn tập        python3 tools/sinh_ontap_tienganh.py --lop 4     ← QUÊN CỜ = đè lớp 1
⑦ kịch bản nói     python3 tools/sinh_kichban_noi.py --lop 4        ← QUÊN CỜ = đè lớp 1
⑪ đọc hiểu         python3 tools/sinh_dochieu_tienganh.py --lop 4 --thieu /tmp/loi_doc.json
⑫ bài viết         python3 tools/sinh_vietbai_tienganh.py --lop 4
⑭ BÀI TẢ TRANH     python3 tools/soan_tranh_lop4.py --ghi
                   tools/tts/.venv/bin/python tools/tranh_tienganh.py --lop 4 --tat-ca
                   python3 tools/sinh_bai_tranh.py --lop 4 --thieu /tmp/loi_tranh.json
⑧ clip tiếng       # BA nguồn dòng cần đọc, đừng bỏ sót nguồn nào:
                   #   data/tienganh/lop4_loi.json  ← ④ sinh_bai_tienganh tự ghi ra
                   #   /tmp/loi_doc.json            ← ⑪
                   #   /tmp/loi_tranh.json          ← ⑭
                   tools/tts/.venv/bin/python tools/tts/sinh_am.py \
                     --vao <mỗi tệp trên, chạy lần lượt> \
                     --ra web/public/content/tienganh/audio \
                     --so web/public/content/tienganh/lop4_am.json
⑨ video            tools/tts/.venv/bin/python tools/video/dung_video.py --lop 4 --tat-ca
   soát hình       python3 tools/soat_hinh_tienganh.py --lop 4 --lech
   dựng bản chạy   cd web && npm run build
   cổng            for f in test/*.test.mjs; do node "$f"; done
   KIỂM BẰNG MẮT   mở app — xem mục 5
```

⚠ **Tầng ⑭ phải chạy SAU ⑪ và ⑫.** Nó CHÈN mục tranh đè lên mục cũ của cùng
unit; chạy trước thì bị hai bộ kia ghi đè lại, và **không có gì báo**.

⚠ **Sinh âm SAU tầng tranh**, vì tranh đẻ ra câu mới. Và **sổ tra là một tệp
CỘNG DỒN**: `sinh_am.py` chạy nhiều lần vào cùng `--so` thì nó bù thêm, không ghi
đè. Chạy xong hết thì đối chiếu: mọi `clip[].tep` phải có mp3 thật trong thư mục.

⚠ **BA bộ mặc định LỚP 1 — quên cờ là ĐÈ MẤT BẢN ĐANG CHẠY của lớp 1**, im lặng
hoàn toàn:

| tệp | vì sao dễ quên |
|---|---|
| `sinh_ontap_tienganh.py` | đọc tay `sys.argv`, `--help` KHÔNG in ra `--lop` |
| `sinh_kichban_noi.py` | y hệt |
| `tools/video/dung_video.py` | có trong `--help`, nhưng `default=1` |

Với ba tệp này đừng tin `--help`; đọc thẳng dòng `LOP = 1` / `default=1` ở đầu.

✓ Ngược lại, `chuan_tienganh.py` đã khai sẵn `choices=[1,2,3,4,5]` và **bắt buộc**
`--lop` — không sửa gì, cũng không quên được.

⚠ `sinh_bai_tienganh --tat-ca` dựng lại toàn bộ tệp DL. Kiểm bằng **`git status`**,
đừng kiểm bằng bản chụp thư mục: `cp -r src dest` khi `dest` đã có thì nó **lồng
vào trong**, và tôi đã đối chiếu nhầm với một bản chụp cũ hai ngày.

---

## 3b · KHAI Ô CHO MẪU CÂU — chỗ đẻ ra câu vô nghĩa nhiều nhất

Mẫu NHIỀU Ô mà không khai `sua_slot` thì `sinh_cau` **bỏ qua CẢ MẪU, im lặng**.
Lớp 3 có 6 mẫu như thế, lớp 4 có **15**. Nhưng khai rồi vẫn chưa xong — bốn bệnh
đã gặp thật ở lớp 4, và **không cổng nào bắt được** vì mọi chữ đều đã học và khuôn
thì khớp công thức:

| bệnh | câu máy đẻ ra | chữa |
|---|---|---|
| hai ô CÙNG TÊN mà phải khác | *Is your sports day in June? … It's in June.* | đè `cong_thuc` trong bản bù, đổi thành `[Month A]`/`[Month B]` |
| hai ô KHÁC TÊN mà trùng từ | *Where's the bookshop? - It's opposite the bookshop.* | cờ `khac_nhau: true` |
| ô nuốt mất mạo từ | *It's near bookshop.* | khai ô bằng CỤM có sẵn `the` |
| ô bốc chữ rời | *I have breakfast at o'clock.* | khai ô bằng CỤM (`six o'clock`) |

⚠ **`_ghi` chỉ NGƯỜI đọc được.** Tôi viết "hai ô này phải khác nhau" vào `_ghi`
rồi tưởng xong — máy không đọc chú thích. Muốn máy canh thì phải có CỜ.

⚠ Ô cùng tên thì `sinh_cau` **luôn** điền giống nhau. Đó là ĐÚNG cho
`[Routine]…[Routine]` (hỏi gì đáp nấy) và SAI cho `[Month]…[Month]`. Đọc công
thức xem nó muốn gì, đừng suy từ hình dạng.

---

## 4 · LUẬT NỘI DUNG — mỗi luật đổi bằng một lỗi đã lên bản thật

### Không bịa câu tiếng Anh
Chỉ dùng câu và khuôn CỦA SÁCH. Chỗ duy nhất được sửa là **mạo từ**: khuôn ghi
`a` nhưng `a elephant` sai → đổi `an`. Đó là ngữ pháp bắt buộc, không phải bịa.

### Mọi `X or mặc_định` đều đáng ngờ
`dang_can(o, t) or t['tu']` đẻ ra *"Where are the lamp?"* — ô đòi số nhiều mà từ
chưa khai `so_nhieu` thì bộ sinh **lặng lẽ điền dạng gốc**. Thiếu dạng thì **loại
từ ấy khỏi kho**, đừng điền bừa.

### Chỉ dùng khuôn ĐÃ HỌC TỚI UNIT ẤY
Cắt theo **unit**, không theo chương. `chuan_lop3.json` khai `cat → cats` ở unit
16; tra thẳng vào đó khi soạn unit 1 thì ra *"How many cats"* — chữ bé chưa gặp.

### Hình phải ĐÚNG NGHĨA, và tên Unicode là bằng chứng
Đọc **tên chính thức** của emoji đặt cạnh nghĩa, đừng tin cảm nhận. Cách ấy bắt
được: `desk` → CHAIR · `mops` → BROOM · `table` → CHAIR · `blanket` → BED ·
`skipping` → **PERSON CARTWHEELING** (người lộn nhào!). Công cụ:
`tools/soat_hinh_tienganh.py --lop N`.

### Hai từ khác nhau thì hai hình khác nhau
`ball` ≠ `football` · `singing` ≠ `singer` · `cooking` ≠ `cook` · `run` = `running`
(một việc hai dạng → **dùng chung** một hình).
Nghề nghiệp vẽ **chân dung nửa người mặc đồng phục**; hoạt động vẽ **người đủ
thân đang làm động tác**.

### Bài tả tranh — BỐN LUẬT, bác chốt 20-08-2026
1. **KHÔNG HỘI THOẠI.** Đoạn đọc chỉ có câu kể. Mẫu câu hỏi vẫn dạy, nhưng ở
   CÂU HỎI SAU BÀI và ở phòng nói.
2. **VỐN TÍCH LUỸ TỪ LỚP 1** tới đúng CHƯƠNG của bài ấy.
3. **MỘT NƠI, MỘT LÚC** — nhiều nhất 2–3 người, đồ vật phải thuộc về chỗ ấy.
4. **KHÔNG NHÂN BẢN** — mỗi cảnh viết tay ở `tools/soan_canh.py`; bộ vẽ
   `tools/canh_ve.py` chỉ biết VẼ, không quyết cảnh nào có gì.

Thứ tự làm: ① mô tả tranh chi tiết → ② đoạn đọc → ③ câu hỏi → ④ nói · viết.
Đi từ bảng từ vựng ra tranh thì tranh thành cái kệ đựng từ.

⚠ **LUẬT ĐÃ BỎ:** "mỗi vật ĐÚNG MỘT câu tả nó, và ngược lại". Nghe rất hợp lý,
và chính nó ép đoạn văn thành bảng liệt kê — bác bác bỏ cả 42 bài vì hậu quả
ấy. Nếu thấy ai định dựng lại luật ấy thì đừng.

Hai luật vẫn giữ:
* hoạt động chỉ vào tranh được khi hình **có NGƯỜI** (cờ `nguoi: true`);
* mồi nhử phải **cùng dáng câu với đáp án** — khác dáng thì bé chọn bằng mắt.

⚠ **SOI TRƯỚC KHI DỰNG.** Làm lớp 3·4 tôi viết đoạn theo trí nhớ rồi phải sửa
20 chỗ SAU KHI đã có ảnh và tiếng. Lớp 5 dựng phép soi trước (vốn từ theo
chương · lặp khuôn · đáp án lẻ loi · hội thoại · đoạn chỉ-liệt-kê) và nó bắt 12
chỗ khi nội dung còn nằm trong một tệp.

### Phòng nói: bé ĐÁP, không nhại
Cả phòng nói từng dựng trên giả định "bé nhại lại câu cô vừa nói", nên cô hỏi
*"What can you see?"* mà bé nhại đúng câu hỏi ấy thì được **9/10**. Mỗi lượt của
cô phải mang theo `can` — danh sách câu được tính là đúng.

### Ngưỡng phần trăm che lỗ thủng
Cổng xanh ≠ có ai canh. **Đảo chiều thử mọi cổng mới**: cố tình nhét lỗi vào, xem
nó có đỏ đúng chỗ không. Cổng nào không đảo chiều thử thì coi như chưa có.

---

## 5 · KIỂM BẰNG MẮT — BƯỚC KHÔNG BỎ ĐƯỢC

Cổng soi **DỮ LIỆU**, không soi **MÀN HÌNH**. Riêng đợt lớp 3 vừa rồi, phần nhìn
bằng mắt bắt được bốn thứ mà 74 cổng xanh không thấy:

* màn ĐANG HỎI không có bức tranh nào, còn màn KẾT thì dựng tranh HAI LẦN;
* dòng chữ tiếng Anh trên tranh tô bằng màu KẺ VIỀN → chìm hẳn vào nền;
* cái bàn phím số 🔢 đứng cạnh câu *"He's counting."*;
* người đứng trên "tấm ván" — vạch đất vẽ trong hình, chồng lên kệ của bức tranh.

Việc phải làm sau mỗi lần deploy:

```
# 1. máy chủ có đúng bản vừa dựng không — so BĂM, đừng tin dấu ?v=
shasum -a 256 web/public/<tệp>
curl -s https://ky-su-nhi.web.app/<tệp> | shasum -a 256

# 2. mở app, vào từng loại màn một lần: bài học · đọc · viết · nói · ôn tập
```

⚠ `fetch` trần trong console **không phải bằng chứng** nội dung đã cũ — xem
`[[dau-phien-ban-ganh-cho-immutable]]`.

---

## 6 · DEPLOY

**Deploy TỪNG PHẦN MỘT.** Gộp `--only firestore:rules,functions,hosting` thì
hosting hỏng giữa chừng (mạng rớt lúc đẩy video) và kéo cả lệnh xuống — `functions`
KHÔNG chạy, mà `| tail` che mất mã thoát nên nhìn tưởng xong. Phải mở
`firebase functions:list` mới thấy hàm mới chưa hề có.

`firebase.json` nằm ở **`web/`**, không phải gốc kho.

---

## 7 · BẢNG ĐẾM LỚP 3 — để so khi làm lớp 4

| | lớp 1 | lớp 2 | lớp 3 |
|---|---|---|---|
| Unit · từ | 16 · 60 | 16 · 56 | **21 · 204** |
| Câu luyện tập | 469 | 287 | **1 056** |
| Câu sát hạch | — | — | **105** |
| Clip tiếng | 558 | 507 | **1 572** |
| Video | 37 | 34 | **87** |
| Bài tả tranh | — | — | **21 bức × 3 màn** |
| Đề ôn tập | — | — | **5** |

Cổng: **74 tệp · 0 FAIL**. Hình vẽ tay: **46 hình**, 10 mang cờ `nguoi`.


---

## 8 · LỚP 5 LỘ RA GÌ — đọc trước khi làm quyển thứ sáu

### Dạng từ: mỗi quyển lại thêm một dạng
`dang_can()` ban đầu chỉ biết `dang_ing` và `so_nhieu`. Lớp 5 cần thêm **ba**:

| dạng | ô | ví dụ |
|---|---|---|
| `dang_qk` | `[past verb]` | swim → swam · buy souvenirs → bought souvenirs |
| `dang_ngoi3` | `[Verb-s]` | do morning exercise → does morning exercise |
| `dang_ing` (đã có) | `[V-ing]` **và** `[Verb-ing]` | go for a walk → going for a walk |

⚠ **TÊN Ô MỖI QUYỂN VIẾT MỘT KIỂU.** Lớp 1 viết `[Verb-ing]`, lớp 5 viết
`[V-ing]`. Bản đầu so chuỗi nên lớp 5 trượt hết và đẻ ra *"I like go for a
walk."* Nay so bằng KHUÔN, và ô nào đòi một dạng chưa biết đọc thì **kêu lên**.

⚠ **CÓ QUYỂN KHAI SẴN DẠNG TRONG TỪ VỰNG.** Lớp 4 U20 dạy `building a campfire`
— đã là dạng -ing. Đòi bằng được `dang_ing` thì bài ấy MẤT MỘT BẬC. Luật: có
khai thì dùng, không thì nhận nếu chữ đầu đã đúng dạng.

### Thêm một dạng thì phải đi tìm MỌI túi từ
Trong một buổi tôi sửa **ba** cổng cùng một chỗ: `tienganh_bai` ·
`tienganh_dochieu` · `tienganh_hinh_dung_tu`, cộng bộ `sinh_kichban_noi`. Mỗi
nơi dựng túi từ riêng, và nơi nào thiếu dạng mới thì gọi câu đúng là "chữ lạ"
rồi **bỏ câu ấy đi**. Tìm bằng:

```
grep -rn "so_nhieu, x.dang_ing\|'so_nhieu'\|dang_ing" web/test tools --include=*.mjs --include=*.py
```

### Hai cơ chế mới ở `sua_slot`
* **`cung_tu`** — các ô phải lấy CÙNG MỘT TỪ, mỗi ô tự chia dạng. Chiều ngược
  của `khac_nhau`. Thiếu nó: *"Did you buy souvenirs? - Yes, I did. I swam."*
* **mục khai kèm dạng** — `{"tu": "cook", "dang_qk": "cooked very well"}`, để
  câu hỏi dùng động từ trần còn câu đáp dùng cụm quá khứ.

### Ô khai bằng VAI chỉ chạy khi CHÍNH UNIT ẤY dạy vai đó
`vai_biet()` dựng danh sách vai từ vốn từ của unit, không phải cả quyển. Khai
`noichon` cho ô `[place]` của một unit không dạy nơi chốn nào → rơi sang nhánh
"danh sách từ đích danh", kho rỗng, **cả mẫu bị bỏ im lặng**. U08 và U19 lớp 5
mất trắng bậc 2 vì thế. Chỗ nào cần từ của unit trước thì khai bằng CỤM
(`cum_khai` chỉ nhận mục NHIỀU CHỮ) hoặc qua nhóm `them` với vai riêng hẹp.

### Công thức của sách để lọt ba thứ vào câu bé đọc
`...` · `/` · `+`. Ba chỗ ở lớp 5. Và **phải sửa cả `vi_du`**, vì `sinh_cau`
đặt câu ví dụ của sách ĐỨNG ĐẦU.

### Mạo từ phải nằm trong mục khai
Công thức "I wear [clothes]." không có ô cho `a`. Khai trần `jumper` thì ra
*"I wear jumper."* Mà `jeans` số nhiều thì KHÔNG có `a`, đồ uống đi với `some`
— máy không phân biệt được, phải khai tay từng mục.

### Bảng nào TỆP LÀM CHỦ thì bản mới phải thắng
Phép "giữ tất cả khoá cũ" của bộ bóc chữa được chuyện mất bản sửa tay, nhưng nó
giữ luôn bản GHI HỎNG. Tôi thêm `swimmer` vào bảng vẽ tay, chạy lại, và mục ấy
không xuất hiện. Bảng `hinh` do chính bộ bóc khai nên phải cho bản mới thắng.

### Kỳ sát hạch của bài chỉ có MỘT từ vẽ được
Câu SAI dựng bằng cách ghép tiếng của từ này với HÌNH của từ khác. Bài nào chỉ
có một từ vẽ được thì không ghép lệch được → cả kỳ ra TOÀN đáp án "đúng", bé
bấm "đúng" hết là trọn điểm mà không nghe câu nào. Nay chặn ở bộ sinh.
