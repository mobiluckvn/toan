# LÀM BÀI TẢ TRANH — quy trình, và những chỗ đã dính

Bác chốt 19-08-2026: *"Bạn apply cách làm này cho tất cả các bài nhé. Lưu ý là ghi
lại để triển khai cho các lớp sau nhé."*

Tệp này là bản ghi ấy. Đọc TRƯỚC khi làm bài tranh cho một quyển mới.

---

## MỘT BỨC TRANH, BA MÀN

| Màn | Bé thấy | Bé làm | Máy có |
|---|---|---|---|
| **Đọc** | tranh **+** đoạn mô tả | đọc, rồi trả lời câu hỏi | đoạn viết sẵn |
| **Viết** | **chỉ tranh** | tự viết đoạn tả | bản mô tả để chấm |
| **Nói** | **chỉ tranh** | tả bằng miệng | bản mô tả bằng chữ → hỏi và sửa |

Vẽ một lần, dùng ba chỗ. Bé gặp lại cùng một cảnh ba lần với ba việc khác nhau.

---

## DÂY CHUYỀN — CHẠY ĐÚNG THỨ TỰ NÀY

```
① soạn bản khai      python3 tools/soan_tranh_lop3.py --ghi
② vẽ tranh           tools/tts/.venv/bin/python tools/tranh_tienganh.py --lop 3 --tat-ca
③ sinh ba màn        python3 tools/sinh_bai_tranh.py --lop 3 --thieu /tmp/loi.json
④ sinh tiếng         tools/tts/.venv/bin/python tools/tts/sinh_am.py \
                       --vao /tmp/loi.json --ra web/public/content/tienganh/audio \
                       --so web/public/content/tienganh/lop3_am.json
⑤ dựng bản chạy      cd web && npm run build
⑥ cổng               for f in test/*.test.mjs; do node "$f"; done
⑦ KIỂM BẰNG MẮT      mở app, vào từng màn — xem mục "vì sao bước ⑦ không bỏ được"
```

⚠ **Bước ③ phải chạy SAU `sinh_dochieu_tienganh.py` và `sinh_vietbai_tienganh.py`.**
Nó CHÈN mục tranh đè lên mục cũ của cùng unit; chạy trước thì bị hai bộ sinh kia
ghi đè lại, và không có gì báo.

---

## LUẬT DỰNG TRANH — sáu điều, mỗi điều đổi bằng một lỗi thật

**1 · Tranh dựng NGƯỢC từ vốn câu.** Vẽ một thứ mà bé không có câu nào nói về nó
thì bé đứng nhìn. Khai vật rồi sinh câu, không vẽ trước rồi nghĩ sau.

**2 · Nội dung phải ĐỒNG BỘ với tranh.** Bản đầu vẽ 3 con diều mà đoạn viết *"I can
see a kite."* — một con. Không sửa được CÂU cho khớp tranh, vì tới unit 0 sách chưa
có khuôn nào nói "ba con diều" trong một câu kể. Nên sửa TRANH: mỗi vật đúng một
cái. Cổng nay soi cả hai chiều — vật `so > 1` mà đoạn không nói số nào thì đỏ, và
đoạn tả vật nào thì tranh phải có vật ấy.

**3 · Mỗi vật ĐÚNG một câu.** Đoạn bị cắt ở năm câu trong khi tranh giữ sáu vật →
bé nhìn thấy một thứ không ai tả. Cắt cả hai cùng một chỗ.

**4 · Chỉ dùng khuôn ĐÃ HỌC tới unit ấy.** Bốn khuôn kể: `This is a X.` ·
`I can see a X.` · `That's a X.` · `There's a X.`. Hoạt động: `She's Xing.` Người
nhà: `This is my X.` (*"This is a father."* sai hẳn). Câu hỏi cũng thế —
`What can you see?` (lớp 2 U4) · `How many … can you see?` (lớp 1 U16) ·
`What's she doing?` (lớp 2 U5) · `What's this?` (lớp 3 U4) · `Who's this?` (U11,
và người thì phải hỏi *Who*, không phải *What*).

**5 · Mạo từ và dạng số nhiều phải ĐÃ HỌC.** `a elephant` sai → đổi `an`. Và
`cat → cats` sách dạy ở unit 16, nên soạn tranh cho unit 1 mà hỏi *"How many cats"*
là hỏi bằng một chữ bé chưa gặp.

**6 · Không độn vật của unit khác chủ đề.** Mượn bừa thì ra *"bean · bed · egg ·
desk"* — cái giường lạc vào bàn ăn. Mượn theo thứ tự: cùng unit → cùng chương →
lớp 1·2, và xoay theo số unit để hai bức liền nhau không trùng. Riêng unit dạy
HOẠT ĐỘNG thì mượn `PHU` — mấy đạo cụ đứng được trong bất kỳ cảnh nào (`kite` ·
`bike` · `cake` · `table` · `box` · `tent` · `van` · `car`); mượn từ đầu danh sách
vốn thì bức "Sở thích của mình" ra *"cooking · running · dancing · face"*.

**7 · Câu "She's …ing." thì trên tranh phải CÓ NGƯỜI.** Phép kiểm cũ chỉ hỏi *từ
này có hình không*. Có — nhưng hình là ĐỒ VẬT: `counting` → 🔢, `reading` → 📖,
`singing` → 🎤, `painting` → 🎨, `drawing` → 🖌️. Bức "Ở vườn thú" viết *"He's
counting."* bên cạnh một cái bàn phím số. Bé nhìn quyển sách thì bé nói *"a
book"*, không ai nói được *"She's reading"* từ quyển sách nằm trên kệ. Nay
`la_nguoi()` soi mã emoji; hoạt động nào hình không có người thì ở lại thẻ từ và
video, không vào tranh. Danh sách mã cố tình để HẸP — đoán hụt thì mất một hoạt
động (tranh tự bù bằng đạo cụ), đoán rộng thì bé lại đứng nhìn quyển sách.

Cách chữa TẬN GỐC là **vẽ tay một người đang làm việc ấy** rồi đặt cờ `nguoi:
true` trong `hinh_ve.json` — `la_nguoi()` và cổng cùng đọc cờ đó, không đoán mã.
Đã vẽ ba (20-08-2026), cùng một họ nét với `run` có sẵn:

| | vẽ gì | emoji cũ sai ở đâu |
|---|---|---|
| `singing` | người đứng, miệng há, micro đưa lên tận miệng, hai nốt nhạc bay ra | 🎤 là CÁI MICRO |
| `reading` | người cầm quyển sách MỞ trước mặt, mắt nhìn xuống trang | 📖 là QUYỂN SÁCH — mà lớp 1 đã dạy chính từ `book` |
| `writing` | người cầm bút CHẤM XUỐNG tờ giấy có dòng kẻ | ✍️ tên thật WRITING HAND: chỉ có bàn tay, không có người |
| `dancing` | người hai tay giơ lên, chân bước rộng, váy xoè đỏ | 💃 **không sai nghĩa** — vẽ lại chỉ vì LỐI NÉT, xem ngay dưới |

**Lối nét cũng là một lý do vẽ lại.** Ba từ trên vẽ xong thì bức U18 có bốn bạn
đang làm việc, ba bạn là hình vẽ tay mảnh-phẳng còn 💃 là emoji đậm-có-khối —
đứng cạnh nhau nhìn lệch hẳn. Nên hễ một bức đã có hình vẽ tay thì **mấy hình
người còn lại trong CÙNG bức ấy nên vẽ nốt**. Phân biệt `dancing` với `run`:
thân ĐỨNG THẲNG (run nghiêng về trước), tay giơ LÊN (run đánh ra sau), vệt nhịp
CONG hai bên (run là ba gạch THẲNG sau lưng).

⚠ Vẽ xong thì phải chạy lại **cả dây chuyền từ tầng ②**: khai `_ve_tay` trong
`lopN_bu.json` → `chuan_tienganh.py` → `sinh_bai_tienganh.py` (để `hinhTu[].ve`
có tên hình) → tranh → **và dựng lại VIDEO của mọi unit dạy từ ấy**, vì thẻ từ
trong video cũng đọc cùng nguồn hình.

⚠ Đừng vẽ đè lên một từ khác: `singer` (U12, nghề nghiệp) dùng 🧑‍🎤. Phân biệt
bằng khung hình — nghề là chân dung nửa người mặc đồng phục, hoạt động là người
đủ thân đang làm động tác.

⚠ **`BOT_VIEC = 4`, đừng nới.** `KHUON_VIEC` chỉ có hai khuôn (`She's …` /
`He's …`) xoay vòng, nên năm hoạt động là ba dòng cùng một khuôn và cổng "không
quá 2 dòng cùng khuôn" đỏ ngay. Bốn thì vừa đúng hai/hai. Đã đảo chiều thử.

⚠ **Vẽ thêm người thì bỏ bớt đạo cụ.** U18 vốn mượn `book` và `pen` làm đạo cụ;
khi `reading`/`writing` thành người, đoạn có cả người-đang-đọc-sách LẪN câu "This
is a book." — bé không biết câu ấy tả cái nào. Sửa `UU_TIEN` cùng lúc.

**8 · Chữ trên tranh phân cấp bằng CỠ, không bằng ĐỘ NHẠT.** Dòng tên cảnh tiếng
Anh từng tô bằng `LINE` (#D4E1EE) cho "nhạt hơn một nấc" — nhưng `LINE` là màu kẻ
viền, đặt trên nền `NEN` (#EEF4FA) thì gần như vô hình. Việt `INK`, Anh `MUTE`,
khác nhau ở cỡ chữ 32/26.

---

## CÂU HỎI

* Hỏi **sau khi đọc**, không nhét vào giữa đoạn. Bác đã bắt cả hai chiều: lần đầu
  tôi nhét câu hỏi vào giữa đoạn mô tả (sai), lần sau bỏ sạch câu hỏi (cũng sai).
* Hỏi **bằng tiếng Anh**, lựa chọn **thuần tiếng Anh**; dòng phụ tiếng Việt để nhỏ
  bên dưới làm chỗ bám.
* Phải có **một câu tổng quan** và **ít nhất một câu chi tiết**.
* **Mồi phải cùng khuôn với đáp án**, chỉ khác tên vật hoặc con số. Mồi khác khuôn
  thì đáp án thành lựa chọn DUY NHẤT mang khuôn của nó — bé chọn đúng bằng mắt,
  không cần đọc. Cổng bắt được 33 chỗ đúng kiểu ấy trong một lượt.

---

## PHÒNG NÓI — ba nhịp, không hơn

```
taTranh   cô mời tả          "What can you see?"     bé tự nói
goiY      bé bí thì cô HỎI   "How many …?"           bé ĐÁP (không nhại câu hỏi)
caDoan    xâu chuỗi          cả đoạn                 bé nói hết
```

* **Không có** bước chào, bước từ mới, bước mẫu câu, thẻ "con thích cái nào nhất",
  bảng "con nói về". Bác bảo xoá thì xoá thật — để lại là bé quay về nhại từ.
* **Bé ĐÁP, không nhại.** Đây là chỗ hỏng nặng nhất từng gặp: cả phòng nói dựng
  trên giả định "bé nhại lại câu cô vừa nói", nên khi cô hỏi *"What can you see?"*
  mà bé nhại đúng câu hỏi ấy thì được **9/10**. Mỗi lượt của cô nay mang theo `can`
  — những câu được tính là đúng.
* **Lời dặn cho mô hình là bản RIÊNG** (`loiDanTranh`), không ghép thêm vào lời dặn
  cũ: lời dặn cũ dài mười điều và gần như điều nào cũng nói về dạy nhại câu.
* **Sửa theo đúng nội dung đang hỏi.** Bé đáp nhầm câu thì cô nhắc lại CÂU HỎI
  trước, rồi mới tới chỗ lệch — bảo "con thiếu chữ three" khi bé đáp nhầm câu là
  làm bé rối thêm.
* Buổi chỉ **xong khi bé nói được cả đoạn** — `DAT_LIEN_DE_XONG = 3` vốn cắt buổi
  ngay trước bước ấy.

---

## BÀI VIẾT

* Chỉ tranh + ô trống. **Không** bày mẫu câu — với bài tả tranh thì mẫu câu CHÍNH
  LÀ đoạn mô tả, bày ra là cho sẵn đáp án.
* **Bảng từ phải đủ viết lại cả đoạn.** Bản đầu đoán chừng bảy chữ nối và thiếu
  `That's` — bé bấm hết bảng vẫn không viết nổi câu *"That's a yo-yo."* Nay suy
  thẳng từ đoạn: đoán thì còn thiếu, suy từ đoạn thì không thể thiếu.

---

## VÌ SAO BƯỚC ⑦ KHÔNG BỎ ĐƯỢC

Đã dính một lần, và dính nặng: cổng xanh cả 74 tệp, dữ liệu đúng, máy chủ có bản
mới — mà màn ĐANG HỎI **không có bức tranh nào**, còn màn KẾT thì dựng tranh HAI
LẦN. Vì tôi vá bằng phép thay chuỗi, ngữ cảnh đã đổi nên hai phép thay khớp nhầm
nhánh; và cổng thì soi DỮ LIỆU, không soi màn hình.

Cách chữa cũng là một luật: **gom về một hàm dựng "tranh + đoạn"**, ba màn cùng
gọi. Rải ra từng nhánh là để ngỏ chỗ cho các nhánh lệch nhau.

---

## LÀM CHO LỚP KHÁC

1. Chép `tools/soan_tranh_lop3.py` → `soan_tranh_lopN.py`, đổi `3` thành `N`.
   Bốn bảng cần xem lại theo sách của quyển ấy: `VAI_VAT` / `VAI_BO` (vai nào đặt
   được sau "a"), `KHONG_DEM`, `NGUOI_MA` (thêm mã nếu quyển ấy dạy hoạt động mà
   emoji chưa nằm trong danh sách), và `UU_TIEN`.
   ⚠ **Chạy soạn một lượt rồi ĐỌC hết danh sách vật in ra trước khi vẽ.** `UU_TIEN`
   là thứ chỉ người mới thấy cần: bức nào đọc lên thấy lạc chủ đề thì khai vật cho
   nó, đừng đợi tới lúc mở bản chạy.
2. `tranh_tienganh.py` · `sinh_bai_tranh.py` · `kho_cau_tienganh.py` đã nhận
   `--lop`, không phải sửa.
3. Cổng đã soi theo `dang: 'tranh'` nên tự áp cho quyển mới; riêng
   `tienganh_chamviet` đang đọc `tranh_lop3.json` — thêm quyển thì mở rộng chỗ ấy.
4. Bức nào soạn ra còn kỳ thì **sửa tay** trong `tranh_lopN.json` rồi đặt cờ
   `tay: true` — lần soạn sau không đè lên.

---

## `UU_TIEN` — CHỖ KHAI TAY CÁI MÁY KHÔNG SUY ĐƯỢC

Luật chọn vật (từ của unit → cùng chương → lớp 1·2) **hợp lệ nhưng vô vị** ở sáu
bức, vì có unit không dạy lấy một danh từ vẽ được:

| | máy soạn ra | hỏng ở chỗ |
|---|---|---|
| U04 Cơ thể | *This is a face. That's an ear.* | không ai tả mặt kiểu liệt kê vật rời |
| U07 Lời dặn trong lớp | school · library · playground · classroom · gym | năm địa điểm trong bức tên là "trong lớp" |
| U09 Màu sắc | book · pen · table · notebook · pencil | bức dạy MÀU mà đoạn không nhắc màu nào |
| U10 Giờ ra chơi | book · pen · table · notebook · pencil | y hệt U09 — hai bức liền nhau trùng nhau |
| U15 Ở bàn ăn | bean · bed · egg · desk | cái giường giữa bàn ăn |
| U18 Chơi và làm | dancing · bike · table · kite · cake | chẳng dính gì tới "chơi và làm" |

Nên `UU_TIEN` trong `soan_tranh_lop3.py`: **người khai vật, máy vẫn soi luật.**
Vật khai ra vẫn phải đã học tới unit ấy, phải có hình, phải đặt được sau "a" —
khai nhầm thì nó bị loại và in cảnh báo, không lọt ra bản chạy. Ba khoá:

* `vat` — danh sách vật, theo thứ tự muốn vẽ.
* `chinh` — vật **chủ thể**: vẽ to, đứng một mình kệ trên, câu đầu tả nó, mấy vật
  còn lại là bộ phận nên dùng `I can see …` / `There's …` (bỏ `That's …` — nghe
  như chỉ sang người khác). U04 nay là **một khuôn mặt** với mắt · mũi · mồm của
  chính nó.
* `mau` — bức dạy màu, xem ngay dưới.

Nhờ `UU_TIEN`, unit 10 lấy lại được từ của CHÍNH nó: `basketball` · `volleyball` ·
`football` mang vai `trochoi` nên luật chung gạt đi (đúng, vì *"a badminton"* sai),
nhưng ba quả bóng thì đếm được và vẽ được.

## BỨC DẠY MÀU — HAI CÂU MỘT VẬT, VÀ BA PHÉP KIỂM PHẢI BIẾT ĐIỀU ĐÓ

```
This is an apple. It's red.   I can see a leaf.  It's green.
That's a box.     It's brown. There's a square.  It's blue.
```

`MAU_CUA` chỉ nhận emoji **một màu, gọi tên không cãi được** — `apple` đỏ, `leaf`
xanh lá, `box` nâu, `square` xanh dương. Đừng thêm `cake 🍰`: trắng hay hồng hay
nâu, ba người nhìn ra ba màu.

Kiểu này phá ba phép kiểm cũ, và phá **đúng** — cả ba đều ngầm cho rằng *mỗi câu
nêu một vật*. Nên cổng có thêm khái niệm **CÂU NỐI** (`laCauNoi`), định nghĩa hẹp
đúng một dạng: câu không nêu vật nào, mang đúng khuôn `It's + [một màu ĐÃ HỌC].`,
và câu ngay trước có nêu vật. Ba chỗ bỏ qua câu nối: đếm câu ↔ đếm vật · "đoạn tả
vật tranh không có" · "không quá 2 dòng cùng khuôn". Nới rộng hơn thế — ví dụ cho
mọi câu không nêu vật đi qua — là mở lại cửa cho đúng thứ ba phép kiểm ấy sinh ra
để bắt.

⚠ Câu hỏi màu phải **chốt được hỏi vật nào**. `What colour is it?` một mình thì cả
bốn lựa chọn đều đúng với một vật nào đó — đúng cái bác bắt: *"nhiều câu trả lời ý
same same nhau"*. Sách chưa dạy `What colour is the apple?`, nên chốt ở **dòng phụ
tiếng Việt** ("quả táo (apple) màu gì?"): dòng phụ vốn sinh ra để làm chỗ bám, còn
câu tiếng Anh vẫn nguyên si câu của sách.

## CÒN THÔ, CHƯA SỬA

* **Còn hai bức lẫn lối vẽ.** U18 nay đều tay cả bốn người. Nhưng:
  * **U05 Sở thích** — `dancing`/`singing` vẽ tay, còn `cooking` 🧑‍🍳 và
    `running` 🏃 vẫn là emoji;
  * **U20 Ở vườn thú** — `dancing` vẽ tay, `climbing` 🧗 vẫn là emoji.

  Vẽ nốt là hết: `cooking` · `running` · `climbing`, rồi tới `cycling` 🚴 ·
  `walking` 🚶 · `swimming` 🏊 · `skipping` cho U19. Không gấp — emoji người vẫn
  ĐÚNG nghĩa, chỉ khác lối vẽ. ⚠ Vẽ từ nào thì nhớ **dựng lại video mọi unit dạy
  từ ấy**; `dancing` một từ thôi đã kéo theo ba unit (U05 · U18 · U20).
* **`counting` 🔢 · `painting` 🎨 · `drawing` 🖌️** — vẫn là hình đồ vật nên chưa
  vào tranh được. Cùng cách chữa như trên, chưa unit nào cần tới.
