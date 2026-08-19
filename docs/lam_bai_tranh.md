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
lớp 1·2, và xoay theo số unit để hai bức liền nhau không trùng.

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
   Hai bảng cần xem lại theo sách của quyển ấy: `VAI_VAT` / `VAI_BO` (vai nào đặt
   được sau "a") và `KHONG_DEM`.
2. `tranh_tienganh.py` · `sinh_bai_tranh.py` · `kho_cau_tienganh.py` đã nhận
   `--lop`, không phải sửa.
3. Cổng đã soi theo `dang: 'tranh'` nên tự áp cho quyển mới; riêng
   `tienganh_chamviet` đang đọc `tranh_lop3.json` — thêm quyển thì mở rộng chỗ ấy.
4. Bức nào soạn ra còn kỳ thì **sửa tay** trong `tranh_lopN.json` rồi đặt cờ
   `tay: true` — lần soạn sau không đè lên.

## CÒN THÔ, CHƯA SỬA TAY

Máy soạn được khung đúng luật, nhưng vài bức đọc lên vẫn khô. Ghi ra để còn sửa:

* **U04 Cơ thể** — tả từng bộ phận như vật rời: *"This is a face. That's an ear."*
  Đúng vốn, nhưng người ta không tả mặt kiểu ấy.
* **U07 Lời dặn trong lớp** và **U10 Giờ ra chơi** — từ của hai unit này
  (`come in` · `badminton` · `chess`) không đặt được sau "a", nên tranh phải mượn
  vật của unit khác, và lạc chủ đề.
* **U09 Màu sắc** — tranh có đồ vật nhưng đoạn chưa nói MÀU; cần khuôn hai ô
  `It's a + [Colour] + [Noun].`
* **U15 Ở bàn ăn** — món ăn phần lớn không đếm được (`rice` · `bread` · `meat`) nên
  bị loại khỏi vật; tranh còn `bean` và `egg`.
