# TIẾNG ANH LỚP 1 — khảo sát dữ liệu & đề nghị thiết kế bài

Lập 12-08-2026. Nguồn: `data/ban_do_tieng_anh.json` (đọc trực tiếp, không đoán).

Bác chốt hướng mới: **đi từ lớp 1 → 2 → 3**, và mỗi bài phải phủ bốn việc —
*hiểu từ · hiểu cấu trúc chứa từ ấy · nói được · gõ lại được*.

Hai bản khảo sát trước (`khao_sat_ban_do_tieng_anh.md`, `ghi_chu_tieng_anh_ban_do.md`)
đều khuyên **tránh** lớp 1 vì nó thiếu nhiều nhất. Tệp này không cãi lại con số ấy,
nhưng chỉ ra một điều hai bản kia bỏ sót: **lớp 1 thiếu thứ dễ bù nhất, và có sẵn
thứ khó dựng nhất.**

---

## 1 · LỚP 1 CÓ GÌ — con số thật

```
120 node · 245 cạnh
16 unit · 60 từ · 19 mẫu câu · 16 phonics · 4 Fun time · 4 Review · 1 course
```

Mật độ: **3,75 từ/unit** (thấp nhất trong 12 lớp) · 1-2 mẫu câu/unit · đúng 1 phonics/unit.
Ít, nhưng với bé 6 tuổi thì 3-4 từ một buổi là **vừa**, không phải là thiếu.

### 1.1 · Xương sống là PHONICS, không phải chủ đề

Đây là phát hiện quan trọng nhất, và nó đổi hẳn cách nên dạy.

Mỗi unit khoá vào **một chữ cái**, và từ vựng của unit được chọn để **luyện đúng âm ấy**:

```
U1  Bb /b/  → ball · bike · book
U2  Cc /k/  → cake · car · cat · cup
U4  Dd /d/  → desk · dog · door · duck
U7  Gg /g/  → garden · gate · girl · goat
```

16 unit = 16 chữ cái: **a b c d e f g h i l m n o t u w**.
Còn thiếu **j k p q r s v x y z** — và lớp 2 phủ đúng 10 chữ ấy, cộng thêm digraph
`er` · `sh`. Nghĩa là:

> **Bảng chữ cái chỉ khép kín khi học hết lớp 2.**

Đây là lý lẽ mạnh nhất cho việc bác chọn bắt đầu từ lớp 1: bỏ lớp 1 thì bé vào lớp 2
mà chưa có 16 âm nền. Hai bản khảo sát trước xếp lớp 4-5 lên đầu là xét theo *độ đầy
của dữ liệu*, không xét theo *thứ tự học*.

### 1.2 · Bảng thay thế đã có sẵn — 53 câu hợp lệ

Cạnh `HAS_SLOT` nối **mẫu câu → đúng những từ được phép điền vào**:

```
"This is my + [Noun]."   ← bag · apple · can · hat
"I have a + [Noun]."     ← car · cake · cat · cup
"I can see a + [Noun]."  ← tiger · turtle · top · teddy bear
```

53 cạnh như thế = **53 câu tiếng Anh đúng, do người soạn sách duyệt**, không phải máy
bịa. Với môn ngoại ngữ thì đây là thứ quý nhất trong cả bản đồ: sinh bài tập từ bảng
thay thế thì **không bao giờ ra câu sai ngữ pháp**.

Bên Toán mình phải dựng tay `chu_de_tay.json`; ở đây sách khai sẵn.

### 1.3 · Thang tiên quyết trong lớp — có thật, 13 cạnh

```
This is my bag.  →  This is a dog.  →  That's a monkey.
                                    →  It's a red pen.
                                    →  There's a garden.
Touch your hair. →  Point to your hand.
                 →  Look at the lemons.
How many clocks? →  How many windows can you see?
She's running.   →  She's having noodles.        →  (bắc sang LỚP 2: What's he doing?)
foot             →  football
```

Đủ để xếp thứ tự học và để dựng màn "Học theo chủ đề" **trong lớp 1**.
Có 2 cạnh bắc thẳng sang lớp 2 (`She's running` → `Is she flying a kite?` và
`What's he doing?`) — đường lên đã có sẵn.

### 1.4 · `bkt_params` đủ 95/95 node nguyên tử

`functions/src/bkt.js` chạy được ngay, không viết lại. Giống kết luận cũ.

---

## 2 · TÁM CHỖ THỦNG — và giá phải trả để bù

Xếp theo **công bù**, không theo mức nghiêm trọng.

| # | thủng | lượng | ai bù | ghi chú |
|---|---|---|---|---|
| 1 | **nghĩa tiếng Việt** | **0/60** | người | 60 từ, một buổi ngồi. Toàn từ cụ thể (`ball`, `cat`) — dễ hơn hẳn lớp 7-8 |
| 2 | **IPA** | **0/60** | người/máy + soát | 60 từ |
| 3 | `position` **sai** ở 5 unit nguyên âm | 20 từ | người | xem 2.1 — cái bẫy câm |
| 4 | không có **số đếm** | U9, U16 cần `[Number]` | người | phải thêm one…ten |
| 5 | chỉ có **một màu** (`red`) | U6 cần `[Colour]` | người | xem 2.2 |
| 6 | U1 **không có slot nào** | 2 mẫu câu | người | `[Name]` — dùng tên bé, xem 4.4 |
| 7 | **không có hình** | 60 từ | figforge | bé 6 tuổi học chay bằng chữ là hỏng |
| 8 | **không có âm thanh** | toàn bộ | phải quyết | nặng nhất — xem mục 5 |

Mục 1+2 là 60 dòng. Hai bản khảo sát trước loại lớp 1 vì hai con số `0/60` này —
nhưng 60 từ nhỏ hơn 233 từ lớp 4 (đã có nghĩa nhưng **không dấu**, phải soát từng chữ).
**Bù lớp 1 rẻ hơn sửa lớp 4.**

### 2.1 · Bẫy câm: `position: "initial"` cho cả 16 phonics

Cả 16 node phonics đều khai `position: "initial"`. Đúng với 11 unit phụ âm. **Sai với
5 unit nguyên âm**, vì từ của chúng để âm ở **giữa**:

```
U3  Aa /æ/  → bag · can · hat        (không phải apple ở đầu)
U6  Ee /e/  → bell · pen · pencil · red
U5  Ii /ɪ/  → chicken · chips · fish · milk
U9  Oo /ɒ/  → clocks · locks · mops · pots
U11 Uu /ʌ/  → bus · run · sun · truck
```

Bộ sinh bài đọc `position` để ra đề *"từ nào BẮT ĐẦU bằng âm /æ/?"* thì **20 từ ra đề
sai**, mà dữ liệu vẫn hợp lệ nên **cổng vẫn xanh**. Đúng dạng lỗi câm mà
`docs/CHUAN_DUA_SACH_VAO_APP.md` cảnh báo.

👉 Phải sửa `position` thành `medial` cho 5 unit ấy **trước khi** viết bộ sinh.

### 2.2 · Bẫy thứ hai: slot phẳng, không phân vai

`HAS_SLOT` chỉ nói *"từ này điền vào câu này được"*, **không nói điền vào ô nào**:

```
"It's a + [Colour] + [Noun]."  ← red · pen · pencil · bell
```

Máy thay bừa sẽ ra `It's a pen bell.` hoặc `It's a red red.`
Lớp 3 có trường `pos`; **lớp 1 không có**. Phải gắn tay vai cho 60 từ
(danh từ · động từ · màu · bộ phận cơ thể · thức ăn) — hoặc chỉ sinh bài cho những
mẫu câu **một slot** (17/19 mẫu) và làm tay 2 mẫu còn lại.

### 2.3 · Bẫy thứ ba: từ trong bản đồ ở dạng gốc, câu cần dạng biến đổi

```
slot = "run"     nhưng câu là  "She's running."
slot = "window"  nhưng câu là  "How many windows can you see?"
```

Còn U9 thì từ đã ở dạng số nhiều sẵn (`clocks`, `mops`) — **bất nhất giữa hai unit
cùng dạy một mẫu câu**. Bộ sinh phải có bảng biến đổi tay, đừng ghép chuỗi thẳng.

### 2.4 · Hai unit có đúng một slot

U11 (`She's + [V-ing]` ← chỉ `run`) và U16 (`How many … can you see?` ← chỉ `window`).
Sinh máy ra được **một** câu. Hai bài này phải bù từ tay, hoặc mượn động từ đã học.

---

## 3 · SCHEMA LỚP 1 · 2 · 3 KHÁC NHAU — viết bộ sinh một lần là vỡ ở lớp 2

Bác định đi 1 → 2 → 3. Ba lớp này **không cùng một khuôn dữ liệu**:

| trường | lớp 1 | lớp 2 | lớp 3 |
|---|---|---|---|
| số hiệu unit | `unit_no` | `unit_number` | `unit_number` |
| unit → từ | mảng `vocabulary` trong node | **không có** — chỉ qua cạnh | **không có** — chỉ qua cạnh |
| từ → phonics | `target_phonics` | `phonics_focus` | *(không)* |
| từ → loại từ | *(không)* | *(không)* | `pos` |
| phonics | `letter` · `letter_name` · `target_sound` · `position` | `focus` · `phonics_type` · `example_words` | `sound` · `example_word` · `target` |
| nghĩa Việt | **0/60** | 56/56 | 185/204 |
| IPA | **0/60** | 56/56 | 184/204 |

👉 Bộ sinh phải có **một lớp chuẩn hoá** đọc cả ba khuôn về một dạng, viết **ngay từ
đầu**. Viết riêng cho lớp 1 rồi "sau này sửa" là đúng vết xe của bốn quyển Toán.

---

## 4 · ĐỀ NGHỊ: MỘT BÀI LỚP 1 TRÔNG NHƯ THẾ NÀO

16 unit → **16 bài chính**. Cộng 4 Fun time + 4 Review (bản đồ chỉ có tên và số trang,
nội dung phải tự dựng) → **24 bài**, đúng cỡ một quyển.

Giữ nguyên năm chặng của phòng học đang chạy (`PHASES` trong `flow.js`):

```
MỞ BÀI → GIẢNG → BÀI MẪU → LUYỆN TẬP → SÁT HẠCH
```

### 4.1 · Bốn việc bác nêu, xếp vào bốn bậc — mỗi bậc chỉ thêm MỘT khó khăn

Nguyên tắc: bé 6 tuổi chưa đọc thạo tiếng Việt. **Không bậc nào bắt bé làm hai việc mới
cùng lúc.**

| bậc | việc | bé làm gì | máy chấm | nguyên liệu |
|---|---|---|---|---|
| **1 · NGHE–NHÌN** | hiểu từ | nghe từ, bấm vào **hình** đúng | có | `word` + hình (phải vẽ) |
| **2 · HIỂU** | hiểu từ | thấy từ, bấm nghĩa Việt (và ngược lại) | có | `word` + `meaning_vi` (phải bù) |
| **3 · CẤU TRÚC** | hiểu mẫu câu | xếp **thẻ chữ** thành câu; điền ô trống bằng nút | có | `grammar_form` + `HAS_SLOT` |
| **4 · GÕ** | viết lại | gõ từ / gõ câu | có | `word` + câu sinh từ slot |
| **(nói)** | nói | đọc theo, máy nghe | **CHƯA CÓ** | xem mục 5 |

Mỗi bài đi hết bốn bậc trên **cùng 3-4 từ của unit ấy** — bé gặp lại một từ bốn lần
theo bốn cách khác nhau. Đó là chỗ "dễ vào" mà bác muốn: không thêm từ, chỉ thêm cách.

### 4.2 · Mồi nhử lấy từ đâu — chỗ này quyết định bài có dạy được gì không

Với lớp 1, **mồi tốt nhất là từ CÙNG UNIT**, vì chúng cùng chữ cái đầu:

```
Nghe /kæt/ → chọn:  cat · cake · car · cup
```

Bé chọn sai không phải vì đoán bừa, mà vì **chưa phân biệt được nguyên âm giữa** —
đúng cái bài đang dạy. Mồi lấy từ unit khác (`cat · dog · ball`) thì bé đoán trúng bằng
chữ cái đầu, không học được gì.

Cùng lý lẽ với luật 2 của `luat_o_nhap`: mồi phải **thật sự sai**, và phải sai **có ích**.

### 4.3 · Bậc GÕ chia ba nấc — vì 6 tuổi

`teddy bear` (10 ký tự, có dấu cách) mà bắt gõ nguyên là bé bỏ cuộc.

```
60 từ lớp 1 · độ dài:  3 ký tự ×13 · 4 ×24 · 5 ×9 · 6 ×9 · 7+ ×5
                       └─── 37/60 từ ≤ 4 ký tự ───┘
```

* **Nấc 1 — ghép thẻ chữ cái**: hiện sẵn `c · a · t`, bé kéo đúng thứ tự. Không gõ.
* **Nấc 2 — gõ từ ngắn** (≤ 5 ký tự, 46/60 từ).
* **Nấc 3 — gõ cả câu** (`I have a cat.`) — chỉ ở bài ôn.

Chấm: **bỏ qua hoa/thường, bỏ qua dấu cách thừa, bỏ qua dấu chấm cuối**. Nhưng
**không** bỏ qua sai chính tả — vì chính tả chính là thứ đang kiểm.
Đây là lý do phải có `chamTiengAnh()` riêng: bộ chấm Toán nới đúng những chỗ tiếng Anh
phải siết, và siết đúng những chỗ tiếng Anh phải nới.

### 4.4 · Unit 1 — dùng chính tên bé

U1 dạy `Hi, I'm + [Name].` và `Bye, + [Name].`, bản đồ **không có node tên nào**.
App vừa làm xong phần "nhiều bé một máy", mỗi bé có **biệt danh**. Lấy luôn:

```
Hi, I'm Bo.        ← biệt danh của chính bé
Bye, Mai.          ← tên dự phòng, lấy TỪ SÁCH
```

Bài đầu tiên của cả quyển mà bé thấy tên mình trong câu tiếng Anh — đáng giá hơn mọi
danh sách tên mẫu.

Sáu tên dự phòng — **Bill · Mai · Nam · Linh · Ben · Lucy** — lấy từ chính bộ Global
Success: `Bill` là tên trong câu mẫu U1 của bản đồ, năm tên còn lại là nhân vật có
thật trong bản đồ lớp 3. Vừa trung tính, vừa có gốc trong sách, và **không dính nhân
vật của quyển Toán** (xem mục 7 · câu 5).

### 4.5 · Ba mức sao, ánh xạ thẳng vào bậc

Giữ đúng khuôn ba mức của bốn quyển Toán:

```
★     bậc 1-2  (nghe–nhìn, hiểu nghĩa)   — bấm chọn
★★    bậc 3    (cấu trúc)                — xếp thẻ, điền nút
★★★   bậc 4    (gõ)                      — ô nhập
```

Bé làm được một sao là đã học được cái gì đó. Đây cũng là câu trả lời cho luật 5
(`đo được việc học`): **100% câu bậc 1-3 chấm máy được**, bậc 4 cũng chấm máy được.
Chỉ phần **nói** là không — nên nói phải nằm ngoài thang sao, hoặc chờ mục 5.

---

## 5 · ÂM THANH — ĐÃ CHỐT: Kokoro sinh sẵn tệp

Bản đồ **không có một trường âm thanh nào** (đã soát 3 989 node). Bác chốt:

> **Dùng Kokoro (TTS mã nguồn mở, Apache-2.0) sinh sẵn tệp âm. Bỏ phần phonics.
> Phần bé NÓI hoãn sang Đợt sau.**

### 5.1 · Kho âm cần sinh cho lớp 1 — đếm chính xác

```
60 từ vựng
55 câu   (19 mẫu gốc + 53 câu sinh từ HAS_SLOT, gộp trùng)
───────
115 clip tiếng Anh
```

115 tệp × ~1,5 s. Ở 24 kHz mono, mp3 64 kbps ≈ **1,4 MB cho cả quyển** — không đáng kể
so với thư mục `figures/` hiện có.

### 5.2 · TIẾNG VIỆT — Kokoro-Vietnamese của cộng đồng *(bác chỉ, đã kiểm)*

Kokoro-82M **bản gốc** hỗ trợ đúng 9 thứ tiếng — `a` Anh-Mỹ · `b` Anh-Anh · `e` Tây Ban
Nha · `f` Pháp · `h` Hindi · `i` Ý · `j` Nhật · `p` Bồ · `z` Trung. **Không có tiếng
Việt**, và eSpeak NG tuy có `vi` nhưng mô hình gốc không sinh ra tiếng được.

Bác chỉ đúng chỗ: **cộng đồng Việt Nam đã fine-tune một bản riêng.**

```
mã nguồn : github.com/iamdinhthuan/Kokoro-Vietnamese
trọng số : huggingface.co/contextboxai/Kokoro-Vietnamese
giấy phép: Apache-2.0          (cùng giấy phép với Kokoro gốc — dùng được)
G2P      : vig2p               (bộ chuyển chữ→âm riêng cho tiếng Việt)
giọng    : 13 giọng            Diễm Trinh · Mai Linh · Ngọc Huyền · Đức An · …
đầu ra   : 24 kHz              — TRÙNG với Kokoro gốc, ghép hai nguồn không lệch
chạy     : PyTorch hoặc ONNX   — bản ONNX chạy CPU, không cần GPU
```

Điều này **gỡ nút thắt**: không phải thu tiếng người nữa, và quan trọng hơn — mở ra
một thứ trước đó không dám tính.

### 5.2b · Hệ quả lớn: ĐỌC ĐƯỢC CẢ BÀI, không chỉ lệnh bài

Chỗ khó nhất của lớp 1 là **bé 6 tuổi chưa đọc được**. Trước đó cháu chỉ dám tính 25
câu lệnh. Có TTS tiếng Việt rẻ thì **mọi dòng chữ trong bài đều đọc lên được**: chuyện
mở bài, lời giảng, chỗ dễ nhầm, lời chữa.

Kho âm tính lại:

| | lượng | model |
|---|---|---|
| từ vựng | 60 | Kokoro-82M `a` |
| câu tiếng Anh | 55 | Kokoro-82M `a` |
| lệnh bài (tập đóng, dùng lại khắp 16 bài) | ~25 | Kokoro-VI |
| nghĩa từ tiếng Việt | 60 | Kokoro-VI |
| lời giảng · chuyện mở bài · lời chữa (~20 dòng × 16 bài) | ~320 | Kokoro-VI |
| **tổng** | **~520 clip** | |

**Đo thật** trên 10 clip mẫu đã sinh: trung bình ~20 KB/clip (mp3 64 kbps mono,
24 kHz), dài 0,75 – 3,85 s. Cả quyển ~520 clip ≈ **10 MB**. Vẫn nhỏ hơn `figures/`.

Và nghĩa từ nay **có cả hình lẫn tiếng** — không phải chọn một.

### 5.2c · ⚠ HAI MODEL, KHÔNG ĐƯỢC TRỘN TRONG MỘT DÒNG

Đây là cái bẫy của phương án này, và nó lộ muộn nếu không chặn từ đầu.

Kokoro-VI **chỉ đọc tiếng Việt**; Kokoro-82M **chỉ đọc tiếng Anh**. Một dòng lẫn hai
thứ tiếng thì model nào đọc cũng sai:

```
✗  "Con bấm vào hình con dog nhé."
      → Kokoro-VI đọc "dog" theo vần Việt  → /dóc/
      → Kokoro-82M đọc "Con bấm vào hình"  → không ra tiếng Việt
```

👉 **Luật: mỗi dòng chỉ MỘT thứ tiếng.** Dòng nào cần cả hai thì tách thành nhiều
đoạn, sinh riêng, rồi nối bằng `ffmpeg`:

```
"Con bấm vào hình"  [VI]  +  "dog"  [EN]  +  "nhé"  [VI]
```

Phải có **phép kiểm chặn dòng lẫn tiếng** — nếu không thì lỗi này ra 520 clip mà cổng
vẫn xanh, chỉ đến lúc bé nghe mới biết.

Điểm sáng ngoài lề: hai giọng khác nhau lại **hoá hay** — bé nghe là biết ngay đâu là
tiếng Việt, đâu là tiếng Anh. Cứ để vậy, đừng cố tìm một giọng đọc cả hai.

### 5.2d · Nghe thử — ĐÃ SINH, chờ bác nghe

Đây là bản fine-tune của cộng đồng, chưa có số liệu về dữ liệu huấn luyện. Cháu
không nghe được nên không tự phán được chất lượng.

**Đã cài xong dây chuyền và sinh 10 clip mẫu** → `tools/tts/ra/` (5 Anh · 5 Việt).
Bác nghe rồi gật thì mới sinh 520 clip. Đúng bài học của
`CHUAN_DUA_SACH_VAO_APP.md`: soát một cái trước khi làm cả loạt.

Nếu giọng chưa vừa: đổi `GIONG_EN` / `GIONG_VI` ở đầu `tools/tts/sinh_am.py` rồi
chạy lại — Kokoro-VI có **13 giọng**, Kokoro-82M có nhiều giọng Anh-Anh khác
(`bf_isabella` · `bm_george` · `bm_lewis`).

### 5.3 · Bỏ phonics thì bài phonics còn lại gì

Bác bảo bỏ phonics khỏi phần âm thanh. Cháu hiểu là **bỏ việc thu/sinh 16 âm rời**
(`/b/`, `/æ/` đọc tách khỏi từ) — chứ **không bỏ 16 bài phonics**, vì chúng chính là
xương sống của lớp 1 (mục 1.1) và bỏ đi thì 16 unit mất trục.

Bù lại, dạy âm **qua từ ví dụ** — mà Kokoro đọc từ thì tốt:

```
Nghe: dog · door · duck   → ba từ này bắt đầu giống nhau, con nghe thấy chứ?  → Dd
```

Đây thật ra là cách dạy phonics chuẩn hơn: âm rời `/d/` không tồn tại trong lời nói
tự nhiên. **Không cần thêm tệp nào ngoài 60 clip từ đã có.**

*Nếu ý bác là bỏ hẳn 16 bài phonics thì báo cháu — thiết kế sẽ khác nhiều.*

### 5.4 · Dây chuyền cần dựng

```
Python 3.10-3.12          ⚠ máy đang có 3.9.6 → PHẢI THÊM (brew install python@3.12)
+ kokoro · misaki         Anh
+ kokoro-vietnamese·vig2p Việt
+ torch · soundfile
+ espeak-ng               ⚠ chưa có → brew install espeak-ng
+ ffmpeg                  ✓ đã có sẵn (/usr/local/bin/ffmpeg)
```

Hai model, tải một lần: Kokoro-82M ~330 MB + Kokoro-VI. Đều 82 M tham số nên **chạy
CPU được**, máy 16 GB thừa sức; không cần GPU dù ví dụ của họ viết `device="cuda"`.

Ra `data/tienganh/lop1_am.json` (sổ tra `dòng chữ → tệp · model · giọng`) +
`web/public/content/tienganh/audio/`.
**Nhớ luật ba nơi**: `data/` · `web/public/` · `web/dist/` phải đồng bộ tay.

Sổ âm phải ghi **model nào sinh ra clip nào** — không thì sáu tháng nữa sửa một câu,
không ai biết chạy lại bằng model gì.

---

## 6 · KHÔNG ĐƯỢC ĐỤNG BỐN QUYỂN TOÁN

Không đổi so với hai bản trước, chỉ nhắc lại thứ tự bắt buộc:

1. **Sửa `luat_o_nhap.test.mjs` cho hỏi MÔN — TRƯỚC KHI khai quyển vào sổ.**
   Luật 1 cấm ô gõ chữ ở quyển đọc chậm; lớp 1 thì **gõ chữ chính là bậc 4**.
   Khai quyển trước là cổng đỏ ngay, rồi người sửa vội sẽ tắt luật cho **cả bốn quyển
   Toán** — mất hàng rào đã cứu lớp 3 và lớp 4.
2. **Tách `chamTiengAnh()`** khỏi `flow.js`, kèm phép kiểm khẳng định *"1 612 câu Toán
   không đổi kết quả một câu nào"*.
3. **Không thêm Tiếng Anh vào mảng quyển của `tools/dinh_dang.py`** (bọc LaTeX sẽ bọc
   bậy `and/or`, `he/she`).
4. **Không trộn vào `data/chu_de.json`** — đó là ma trận Toán.

Dùng lại được nguyên: kệ sách · HomeQuyen · `lib/hocba.js` · sổ bố mẹ · bảng cô giáo ·
bảng xếp hạng · LessonPlayer · hàng đợi ôn tập +1/+3/+7 · phần tài khoản nhiều bé.

---

## 7 · QUYẾT ĐỊNH ĐÃ CHỐT — 12-08-2026

| # | câu hỏi | bác chốt |
|---|---|---|
| 1 | âm thanh | **Kokoro sinh sẵn tệp.** Bỏ phần âm phonics rời *(xem 5.3)* |
| 1b | tiếng Việt | **Kokoro-Vietnamese của cộng đồng** *(bác chỉ — xem 5.2)*. Nhờ đó đọc được CẢ BÀI, không chỉ lệnh bài |
| 2 | phần bé NÓI | **hoãn sang Đợt sau.** Đợt 1 chỉ nghe–nhại, không chấm |
| 3 | 60 hình từ vựng | **dựng bằng `figforge`** như bốn quyển Toán |
| 4 | ai bù dữ liệu | **cháu soạn, bác soát** — 60 nghĩa · 60 IPA · 60 vai từ loại |
| 5 | nhân vật | **KHÔNG dùng nhân vật nào** — bỏ hẳn Trí Long · Su Kem *(bác chốt lại 12-08)* |

**Về câu 5** — cháu đề nghị dùng chung hai nhân vật của sách Toán, **bác bác bỏ**:
quyển này dựng cho **mọi học sinh**, không đòi bé phải biết trước thế giới của bốn
quyển Toán. Bác đúng, và lý do bác đưa mạnh hơn ba lý do của cháu:

* Bé lớp 1 học Tiếng Anh **chưa chắc đã học Toán lớp 2**. Bắt bé làm quen hai nhân vật
  lạ ngay bài đầu là thêm một việc, mà việc ấy không dạy điều gì về tiếng Anh.
* Quyển không dính nhân vật thì **dùng được ở bất cứ đâu** — lớp học, nhà, trường khác.
* Ít một tầng hư cấu thì lời giảng ngắn lại, mà lớp 1 thì càng ngắn càng tốt.

**Cái cần giữ, và giữ được:** khuôn `suKemNham` của Toán — *nghe một câu SAI rồi tự
nhận ra* — là cách dạy tốt với ngoại ngữ. Nó **không cần nhân vật nào cả**. Ở đây gọi
là **"chỗ dễ nhầm"**, và câu sai đứng một mình:

```
✗  "Su Kem đọc: This is a duck. Bạn ấy nhầm rồi, con sửa giúp nhé."
✓  "Nghe câu này: This is a duck. Có đúng với bức tranh không?"
```

Bản thứ hai còn **gọn hơn và thẳng vào việc hơn** — bỏ nhân vật hoá ra lại được.

**Chỗ chờ bác gật, nay chỉ còn một:** nghe **10 clip mẫu** (5 Việt · 5 Anh) trước khi
sinh cả 520 clip — mục 5.2d.

---

## 8 · ĐƯỜNG ĐI — thứ tự bắt buộc

| | việc | chạm vào Toán? |
|---|---|---|
| 1 | Sửa `luat_o_nhap` cho hỏi MÔN *(trước khi khai quyển, nếu không là cổng đỏ)* | sửa cổng, **không** sửa dữ liệu |
| 2 | Tách `chamTiengAnh()` + cổng canh *"1 612 câu Toán không đổi một câu"* | rẽ nhánh, không sửa nhánh cũ |
| 3 | Bù dữ liệu lớp 1 → `data/tienganh/lop1_bu.json` *(**không** sửa bản đồ gốc)* | không |
| 4 | Bộ chuẩn hoá đọc được cả ba khuôn lớp 1·2·3 *(mục 3)* | không |
| 5 | Dựng **một unit** mẫu, người soát, rồi mới sinh 15 bài còn lại | không |
| 6 | Dây chuyền Kokoro → 115 clip *(mục 5.4)* | không |
| 7 | Khai quyển vào `chuong_trinh.json`, dựng nội dung, đi thử end-to-end | chỉ THÊM một mục |

**Unit mẫu — đề nghị U4 `In the bedroom`** (`Dd /d/` · desk·dog·door·duck ·
`This is a + [Noun]`): bốn từ đều 3-4 ký tự nên gõ được, đều phụ âm đầu nên tránh bẫy
`position` (mục 2.1), và mẫu câu của nó là **nút thang cao nhất** trong lớp 1 — ba mẫu
khác dựng trên nó.

### Bước 3 bù đúng những gì

```
60  nghĩa tiếng Việt (có dấu)
60  phiên âm IPA
60  vai từ loại              → chặn bẫy 2.2 "It's a pen bell."
 5  sửa position → medial    → chặn bẫy 2.1 (U3 U5 U6 U9 U11)
 3  bảng biến đổi            → run→running · window→windows (bẫy 2.3)
10  số đếm one…ten           → U9 và U16 cần [Number]
 ~6 màu                      → U6 cần [Colour]; bản đồ chỉ có "red"
 2  slot cho U1              → dùng biệt danh của bé (mục 4.4)
```

---

## Đọc kèm

* `docs/khao_sat_ban_do_tieng_anh.md` — khảo sát cả 12 lớp *(mục "nên bắt đầu từ lớp
  4-5" nay thay bằng tệp này: bác chọn thứ tự học, không chọn theo độ đầy dữ liệu)*
* `docs/ghi_chu_tieng_anh_ban_do.md` — bản đồ nuôi được tới đâu
* `docs/CHUAN_DUA_SACH_VAO_APP.md` — 44 cái bẫy khi bóc tách sách
* `docs/tach_hai_mon.md` — kiến trúc ba vùng
