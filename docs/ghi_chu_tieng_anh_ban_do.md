# Ghi chú trước buổi bàn về TIẾNG ANH — soạn bài giảng & bài tập từ bản đồ tri thức

Lập 12-08-2026, chuẩn bị cho buổi bàn với bác.

Bác giao hướng mới: **làm bài giảng và bài tập DỰA TRÊN bản đồ tri thức**. Đây là chỗ
khác hẳn với kết luận cũ trong `docs/khao_sat_ban_do_tieng_anh.md` — bản khảo sát ấy
chốt là "vẫn phải đợi bộ sách `.docx` như bốn quyển Toán". Nay ta không đợi sách nữa
mà lấy chính bản đồ làm nguyên liệu.

Tệp này trả lời đúng một câu: **bản đồ nuôi được tới đâu, và chỗ nào phải bù.**

---

## 1 · Một node lớp 4-5 thực sự có gì

Đã mở `data/ban_do_tieng_anh.json` đọc tận nơi, không đoán.

**Từ vựng** (233 từ lớp 4 · 187 từ lớp 5):
```json
{ "word": "friend", "ipa": "/frend/", "meaning_vi": "ban be",
  "lexical_type": "word", "semantic_field": "people",
  "unit": "u_g4_starter", "cefr_level": "A1",
  "bkt_params": { "p_l0": 0.25, "p_transit": 0.15, "p_guess": 0.2, "p_slip": 0.1 } }
```

**Mẫu câu** (48 lớp 4 · 40 lớp 5):
```json
{ "example": "Hello. How are you? - I'm fine, thank you.",
  "grammar_metadata": { "tense": "present_simple", "sentence_type": "greeting",
                        "formula": "Hello. How are you? - I am fine, thank you." } }
```

**Phát âm** (40 lớp 4 · 20 lớp 5): `sound` · `example_words` · `note_vi`.

**Unit** (25 lớp 4 · 20 lớp 5): `topic` · `theme` · `page` · `order` · `competences`
(2-3 năng lực mỗi unit, viết bằng tiếng Anh).

**Mật độ mỗi unit:** trung bình **9,3 từ** · 1-4 mẫu câu · 0-2 phonics.

---

## 2 · Sinh được gì NGAY, không cần thêm dữ liệu

Bảng dưới là ý kiến của cháu, để bác gạch bỏ hoặc thêm.

| dạng bài | nguyên liệu có sẵn | ghi chú |
|---|---|---|
| Nghe/nhìn từ → chọn nghĩa Việt | `word` + `meaning_vi` | mồi nhử lấy từ **cùng `semantic_field`** — sai kiểu ấy mới dạy được điều gì |
| Nghĩa Việt → gõ từ tiếng Anh | như trên, đảo chiều | đúng "luật ô nhập" của app: máy chấm được |
| Ghép từ với IPA | `word` + `ipa` | lớp 4-5 đủ 100% IPA |
| Xếp lại câu đúng thứ tự | `formula` của mẫu câu | cắt công thức thành thẻ rồi trộn |
| Điền chỗ trống trong mẫu câu | `example` + `formula` | khoét đúng chỗ khác nhau giữa hai chuỗi |
| Nhận diện âm | `sound` + `example_words` | **mỏng**: phần lớn chỉ **một** từ ví dụ |
| Phân loại từ theo nhóm nghĩa | `semantic_field` | tự nhiên thành trò "xếp vào rổ" |

**Đủ để dựng khung một bài học** theo đúng năm chặng của phòng học đang có (mở bài →
giảng → bài mẫu → luyện tập → sát hạch): mỗi unit ≈ một bài, 9 từ + 1-4 mẫu câu là
vừa một lượt 10 phút.

---

## 3 · Sáu chỗ bản đồ KHÔNG có — phải quyết cách bù

### (a) ⚠ Lớp 4: **233/233 từ nghĩa Việt KHÔNG DẤU**

Đây là phát hiện đáng kể nhất, và nó **sửa lại lời khuyên cũ**. Khảo sát trước ghi
"lớp 4 và 5 đủ 100% nghĩa Việt" — đúng về số lượng, nhưng đọc tận nơi thì lớp 4 toàn
`"ban be"`, `"quyen sach"`, `"am /a/ trong America"`.

```
Lớp 4: 233 từ · có dấu 0   · không dấu 233
Lớp 5: 187 từ · có dấu 185 · không dấu 2
```

Không thể hiện thẳng cho bé tiểu học đang tập đọc. **Nên đổi thứ tự: làm LỚP 5 trước.**
Lớp 4 phải bù dấu cho 233 từ — máy thêm dấu được nhưng phải có người soát, vì `"ban"`
ra `bàn · bán · bạn · bản` tuỳ ngữ cảnh.

### (b) Không có một câu hỏi nào

Bản đồ nói *dạy cái gì*, không nói *hỏi thế nào*. Bài tập phải **sinh ra**. Hai đường:

* **Sinh theo khuôn** (như bảng mục 2) — chắc chắn, kiểm được, nhưng cả 420 từ chung
  một giọng, học 20 bài là bé nhận ra khuôn.
* **Nhờ mô hình ngôn ngữ soạn**, lấy bản đồ làm đề bài, rồi người soát.

Cháu nghiêng về **trộn**: khuôn lo phần luyện tập và sát hạch (cần chấm máy chắc tay),
mô hình lo lời giảng và câu chuyện dẫn dắt (cần giọng người). Nhưng đây là **việc bác
quyết**, vì nó định luôn chi phí và thời gian.

### (c) Không có lời giảng

Chỉ **1** node trong toàn bộ lớp 4-5 có trường `description`. Bốn quyển Toán có lời
giảng từng bước do người viết; ở đây chưa có gì.

### (d) Không có âm thanh — với môn ngoại ngữ thì đây là lỗ nặng nhất

Đã soát mọi tên trường của 3 989 node: không một trường âm thanh nào. Mà tiếng Anh
không có tiếng thì dạy được một nửa. **Phải quyết TRƯỚC khi bóc tách** vì nó đổi hình
dạng dữ liệu và đổi cả màn hình phòng học (chưa dòng nào trong `web/src` đụng tới audio).

Ba đường, chi phí rất khác nhau: giọng máy đọc ngay tại trình duyệt (rẻ, có sẵn, giọng
máy) · sinh sẵn tệp tiếng rồi đóng vào app (nghe tốt hơn, tốn dung lượng và công dựng) ·
thu tiếng người (tốt nhất, đắt nhất).

### (e) Không có hình

Bốn quyển Toán đều có hình dựng bằng `figforge`. Từ vựng tiểu học mà không có hình thì
bé lớp 4-5 học chay bằng chữ.

### (f) `competences` viết bằng tiếng Anh

`"Talking about outdoor activities"` — dùng làm mục tiêu bài học thì phải dịch, vì đây
là chữ cho **bố mẹ** đọc.

---

## 4 · Thang tiên quyết: có, nhưng mỏng ở hai lớp này

583 cạnh `REQUIRES` toàn bản đồ là thứ quý — bên Toán mình phải dựng tay
`chu_de_tay.json`. Nhưng riêng lớp 4-5:

```
Lớp 4: trong lớp 64 · xuyên lớp  8
Lớp 5: trong lớp 34 · xuyên lớp 19
```

Đủ để xếp thứ tự học trong một lớp, **chưa đủ** để dựng màn "Học theo chủ đề" xuyên
lớp như bên Toán. Cạnh xuyên lớp phần lớn lại nối ở mức *khoá học*
(`English Grade 5 ⇐ English Grade 4`), không nối tới từng điểm kiến thức.

Điểm sáng: **`bkt_params` đủ trên 3 373/3 373 node**, nên `functions/src/bkt.js` chạy
được ngay, không phải viết lại.

---

## 5 · Bốn chỗ của Toán sẽ chấm sai nếu bê nguyên

Nhắc lại từ `docs/khao_sat_tieng_anh.md`, vì đây là phần dễ quên nhất:

1. **`flow.js checkAnswer` là bộ chấm TOÁN.** Mọi phép nới trong đó (phân số ↔ thập
   phân, bỏ dấu phân nghìn, dãy số không kể thứ tự) vô nghĩa với tiếng Anh và có chỗ
   chấm **sai**. Phải tách `chamTiengAnh()` riêng, gọi theo môn.
2. **`luat_o_nhap.test.mjs` tự đọc sổ đăng ký** và áp cả năm luật cho mọi quyển. Khai
   quyển Tiếng Anh vào sổ là **cổng đỏ ngay**. Phải sửa luật cho hỏi MÔN **trước** khi
   khai quyển — làm ngược lại thì người sửa vội sẽ tắt luật cho cả bốn quyển Toán.
3. **`tools/dinh_dang.py` phải tắt** cho môn này: luật bọc phân số nhận chữ cái đơn lẻ
   `a b c d k m n p q t`, mà tiếng Anh đầy chữ đơn lẻ và đầy dấu `/` (`and/or`).
4. **`chu_de.json` + `bktUnit` là ma trận TOÁN.** Đừng trộn — sẽ thành màn chủ đề lẫn
   "Phân số" với "Present Simple".

Còn **dùng lại được nguyên**: kệ sách · HomeQuyen · `lib/hocba.js` · sổ bố mẹ · bảng cô
giáo · bảng xếp hạng · LessonPlayer · hàng đợi ôn tập +1/+3/+7 ngày · và nay cả phần
tài khoản nhiều bé một máy.

---

## 6 · Sáu câu cần bác quyết — xếp theo mức chặn đường

1. **Âm thanh**: giọng máy · tệp sinh sẵn · thu tiếng người? *(chặn nhiều thứ nhất —
   đổi cả hình dạng dữ liệu lẫn màn hình)*
2. **Bài tập soạn thế nào**: khuôn máy · mô hình soạn · trộn cả hai?
3. **Bắt đầu từ lớp 5 hay lớp 4?** Cháu đề nghị **lớp 5**, vì lớp 4 phải bù dấu cho
   233 từ trước.
4. **Hình minh hoạ**: có làm không, và làm bằng `figforge` như Toán?
5. **Nhận diện app**: hiện là "Toán Tư Duy", nhân vật Trí Long · Su Kem là của sách
   Toán. Tiếng Anh dùng chung hay có nhân vật riêng?
6. **Sao của bài Tiếng Anh có ngang giá sao của bài Toán** trên bảng xếp hạng không?

---

## 7 · Nếu bác chốt xong, đường đi ngắn nhất

Thứ tự này cố ý: mỗi bước đều **kiểm được** trước khi bước tiếp, và ba bước đầu không
đụng gì tới bốn quyển Toán đang chạy thật.

1. Sửa `luat_o_nhap` cho hỏi MÔN — **trước tiên**, nếu không khai quyển là cổng đỏ.
2. Tách `chamTiengAnh()` khỏi bộ chấm Toán, kèm phép kiểm riêng.
3. Dựng bộ sinh bài: bản đồ lớp 5 → 20 unit → khung bài + bài tập, ra đúng khuôn
   `data/` mà bốn quyển Toán đang dùng.
4. Người soát một unit mẫu **trước khi sinh cả 20** — đúng bài học của
   `docs/CHUAN_DUA_SACH_VAO_APP.md`.
5. Khai quyển vào `data/chuong_trinh.json`, dựng nội dung, đi thử end-to-end.
6. Âm thanh (theo đường bác chọn ở câu 1).

---

## Đọc kèm

* `docs/khao_sat_ban_do_tieng_anh.md` — khảo sát bản đồ (lưu ý: mục "nên bắt đầu từ
  lớp 4 và 5" nay cần đọc cùng phát hiện **(a)** ở trên)
* `docs/khao_sat_tieng_anh.md` — mã nguồn hiện có chịu được tới đâu
* `docs/CHUAN_DUA_SACH_VAO_APP.md` — 44 cái bẫy đã dính thật khi bóc tách sách
* `docs/tach_hai_mon.md` — kiến trúc ba vùng và Đợt 2
