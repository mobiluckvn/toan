# Khảo sát — ĐƯA MÔN TIẾNG ANH VÀO APP

Ghi 2026-08-11, TRƯỚC khi bắt tay. Đọc tệp này đầu tiên ở phiên làm Tiếng Anh.

> 📍 **ĐÃ CÓ BẢN ĐỒ TRI THỨC** (bác gửi 11-08-2026): `data/ban_do_tieng_anh.json` —
> 3 989 node · 7 602 cạnh · lớp 1-12 · bộ Global Success. Khảo sát riêng ở
> **`docs/khao_sat_ban_do_tieng_anh.md`**, đọc kèm tệp này. Bản đồ trả lời câu
> "dạy CÁI GÌ"; tệp này trả lời câu "mã nguồn hiện có chịu được tới đâu".

Mục đích: nói rõ **cái gì dùng lại được nguyên**, **cái gì tưởng dùng lại được mà sẽ
chấm sai**, và **cái gì chưa hề có**. Ba nhóm ấy quyết định khối lượng việc, chứ không
phải số bài trong sách.

---

## 1 · DÙNG LẠI ĐƯỢC NGUYÊN — không sửa dòng nào

Bốn đợt vừa rồi đã dọn đúng chỗ cần dọn: mọi thứ khác biệt giữa các quyển nay đọc từ
`data/chuong_trinh.json`, không gõ cứng trong giao diện.

| dùng lại | vì sao chạy được ngay |
|---|---|
| **Kệ sách** | đã nhóm theo `mon`; `tienganh` đã khai sẵn trong `mon` (🔤, màu teal) và đã có mục ở `sapCo`. Chuyển mục ấy sang `chuongTrinh` là quyển hiện lên |
| **HomeQuyen** | trang chính của quyển đọc `khoaBai · quyen2 · chuong[] · tepOnTap` từ sổ đăng ký |
| **lib/hocba.js** | đếm bài · chương · master · việc tiếp theo — thuần cấu trúc, không biết môn là gì |
| **Sổ bố mẹ · bảng cô giáo · bảng xếp hạng** | đều đọc `dsChuongTrinhSapXep()` rồi lọc `loai === 'hoc'` |
| **LessonPlayer + khung bài** | giảng → bài mẫu → luyện tập → sát hạch là khung SƯ PHẠM, không phải khung toán |
| **Hàng đợi ôn tập** (`functions/src/schedule.js`) | lịch +1/+3/+7 ngày — **đúng thứ từ vựng cần nhất**, dùng lại gần như miễn phí |
| **Nhật ký · học bạ · đồng bộ** | `attempts`, `progress`, `hocBa` không mang giả định môn nào |

**Việc cần làm ở nhóm này gần bằng không.** Đó là kết quả của bốn đợt dọn vừa rồi —
nếu làm Tiếng Anh trước chúng, khối lượng đã gấp mấy lần.

---

## 2 · TƯỞNG DÙNG LẠI ĐƯỢC MÀ SẼ CHẤM SAI — chỗ nguy hiểm nhất

### (a) `flow.js checkAnswer` là BỘ CHẤM TOÁN, không phải bộ chấm chung

871 dòng, và mọi phép nới trong đó đều là nới **toán học**:

```
phân số ↔ thập phân        "3/4" ↔ "0,75"
dấu − × ÷ gõ thành - x :
đơn vị đo bỏ hay không     "60 000 đồng" ↔ "60000"
bỏ dấu phân nghìn          "2 000" ↔ "2000"
dãy số không kể thứ tự     "29; 38" ↔ "38 và 29"
so sánh đảo chiều          "9/10 > 7/8" ↔ "7/8 < 9/10"
```

Với tiếng Anh, mấy phép này **vô nghĩa ở chỗ tốt nhất và CHẤM SAI ở chỗ tệ nhất**:
`toNumber` sẽ coi hai câu trả lời chữ khác nhau là bằng nhau nếu cùng chứa một con số;
`boPhanNghin` nối các chữ số dính nhau. Tiếng Anh cần một bộ nới **khác hẳn**, và đó
là quyết định SƯ PHẠM phải hỏi người soạn trước khi viết:

* hoa/thường có tính không? (`london` vs `London` — với bài dạy danh từ riêng thì CÓ)
* dấu câu cuối câu có bắt buộc? dấu nháy `'` cong hay thẳng?
* `I'm` ↔ `I am` — nhận cả hai hay bài đang dạy đúng dạng rút gọn?
* mạo từ `a/an/the` thiếu thì sai hẳn hay trừ một phần?
* sai chính tả một chữ cái — với bài NGHE thì tha, với bài CHÍNH TẢ thì không.

👉 **Đừng nhét vào `checkAnswer` hiện có.** Tách `chamTiengAnh()` riêng, `flow.js` gọi
theo môn. Trộn chung là một ngày nào đó phép nới của môn này chấm sai môn kia, và
kiểu hỏng ấy luôn im lặng.

### (b) Luật ô nhập số 1 MÂU THUẪN TRỰC DIỆN với Tiếng Anh

`test/luat_o_nhap.test.mjs` luật 1: **quyển đọc chậm KHÔNG được có ô gõ chữ** — đáp án
không phải số thì phải cho bấm nút. Với Toán lớp 2-4 đúng: bài đang kiểm toán, không
kiểm kỹ năng gõ.

Với Tiếng Anh thì **gõ chữ CHÍNH LÀ kỹ năng đang dạy**. Luật ấy hiện gắn với cờ
`doc.moiManMotMuc` (nhịp đọc). Phải đổi cho nó hỏi **MÔN**, không hỏi nhịp đọc —
nếu không, quyển Tiếng Anh lớp 2 vừa khai vào sổ là cổng đỏ ngay, và người sửa vội sẽ
tắt luật cho cả bốn quyển Toán.

### (c) `tools/dinh_dang.py` phải TẮT cho Tiếng Anh

Bộ định dạng bọc công thức thành LaTeX. Luật nới phân số của nó nhận **mười chữ cái
thường đơn lẻ `a b c d k m n p q t`** — tiếng Anh đầy chữ đơn lẻ và đầy dấu `/`
(`and/or`, `he/she`, `3/4 of the class`). Chạy nó lên nội dung tiếng Anh là bọc bậy
hàng loạt, mà **dữ liệu vẫn hợp lệ nên cổng vẫn xanh**.

### (d) Ma trận và mã kỹ năng là của TOÁN

`data/chu_de.json` (5 mảng → 34 chủ đề → 82 dạng) và `bktUnit` dạng `CASE:V.1.1#1@G5`
là khung kiến thức Toán. Màn **Học theo chủ đề** hiện vẽ thẳng từ đó.

Tiếng Anh cần khung riêng (CEFR pre-A1/A1/A2, hoặc khung của chính bộ sách). **Đừng
trộn vào `chu_de.json`** — sẽ thành một màn chủ đề lẫn lộn "Phân số" với "Present
Simple". Cần tách bản đồ chủ đề THEO MÔN trước khi dựng.

---

## 3 · CHƯA HỀ CÓ — phải làm mới

### ÂM THANH: không một dòng nào trong kho đụng tới

Đã soát cả `web/src`: không có `audio`, không có `SpeechSynthesis`. Mà Tiếng Anh thì
**nghe và phát âm là một nửa môn học**. Đây là khối việc lớn nhất, và cần quyết trước:

| cách | được | mất |
|---|---|---|
| tệp mp3 kèm nội dung (như `figures/`) | giọng thật, chuẩn, kiểm soát được | phải thu/mua; nặng; phải có mã kiểm như hình |
| Web Speech API của trình duyệt | miễn phí, không tệp nào | giọng máy, chất lượng khác nhau tuỳ máy/hệ điều hành, iOS hay câm |
| trộn: mp3 cho bài giảng, máy đọc cho từ lẻ | cân bằng | hai đường phải bảo trì |

Kèm theo: hình dạng dữ liệu phải có chỗ khai `audio` cho từng màn/từng từ, và
`figure_manifest.json` đã có sẵn nếp "mã kiểm sha256 cho từng tệp" — bê nguyên nếp ấy
sang cho âm thanh là hợp lý.

### Luyện phát âm (con NÓI, máy nghe)
Khác hẳn nghe. Cần quyết có làm không — nếu có thì phải khảo sát riêng, vì nó động tới
quyền dùng micro và tới việc chấm một thứ không có đáp án đúng/sai rạch ròi.

### Từ vựng là một loại nội dung MỚI
Toán không có khái niệm "thuộc lòng 500 từ". Cần một hình dạng dữ liệu riêng cho từ
vựng (từ · nghĩa · loại từ · phát âm · ví dụ · hình) và một màn luyện riêng. **Tin
vui**: hàng đợi ôn tập +1/+3/+7 ngày đã có sẵn và đúng là thứ từ vựng cần.

---

## 4 · THỨ TỰ ĐỀ NGHỊ

1. **Bác gửi bộ sách Tiếng Anh** (như bốn quyển Toán đã gửi dạng `.docx`).
2. Khảo sát sách → chốt **khung kiến thức** và **cách chấm** (mục 2a) — hai thứ này
   quyết định mọi thứ sau, sai là phải làm lại từ đầu.
3. Quyết **âm thanh** (mục 3) trước khi bóc tách, vì nó đổi hình dạng dữ liệu.
4. Đọc `docs/CHUAN_DUA_SACH_VAO_APP.md` — 44 cái bẫy đã dính thật. Nhưng đọc có phê
   phán: nó viết cho sách TOÁN, mục nào nói về công thức/đáp số thì không áp thẳng được.
5. Bóc tách một quyển nhỏ nhất trước để dò đường, đừng làm cả bộ.

---

## 5 · MỘT ĐIỀU NÊN NÓI THẲNG

App hiện là **Kỹ Sư Nhí · Toán Tư Duy**. Thêm Tiếng Anh là đổi bản chất sản phẩm từ
"một bộ sách Toán" thành "một nền tảng nhiều môn". Kệ sách và sổ đăng ký đã sẵn sàng
cho việc ấy, nhưng có ba chỗ ngoài mã nguồn cần bác quyết:

* **tên và nhận diện** — chân trang, thẻ tiêu đề, icon hiện đều nói "Toán Tư Duy";
* **nhân vật** — Trí Long · Su Kem · Su Bống · Cáo Đề là nhân vật của sách Toán. Tiếng
  Anh dùng chung dàn nhân vật hay có dàn riêng?
* **bảng xếp hạng** — sao của một bài Toán và sao của một bài Tiếng Anh có ngang giá
  không? Hiện công thức sao không biết môn; hai môn chung một bảng thì bé học Tiếng Anh
  và bé học Toán so nhau bằng cái gì.

---

Xem thêm `docs/CHUAN_DUA_SACH_VAO_APP.md`, `docs/tiep_theo_man_nha.md`
và `docs/tiep_theo_bang_xep_hang.md`.
