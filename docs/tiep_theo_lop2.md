# Điểm dừng — 2026-08-08

**Mọi thứ đã deploy và đang chạy.** Cây làm việc sạch tại `68a61d7`, `main` khớp
`origin/main`, 604 phép kiểm xanh (17/17 tệp).

## Đã xong

| | |
|---|---|
| 33 bài lớp 2 | 281 câu luyện tập · 165 câu tự kiểm **chấm máy** |
| 70 hình | 64 trong bài · 6 trong kỳ sát hạch · **33/33 bài có hình** |
| 8 ôn tập + 3 ải | 114 câu, đủ đáp án, Bảng tự soi trỏ đúng bài cần ôn |
| Mã nguồn | lớp 2 và lớp 5 **dùng chung**; khác biệt khai ở `data/chuong_trinh.json` |
| Gói JS | tách 3 phần — sửa nội dung chỉ tải lại 127 KB thay vì 828 KB |
| firebase-functions | 5.1.1 → **7.3.2**, đã chạy thật trên máy chủ |

---

## Việc tiếp theo, xếp theo GIÁ TRỊ THẬT

### 1 · Đề B chưa dùng được  ← đáng làm nhất

Sách hứa với bé: *"Chưa đạt thì ôn theo bảng trên rồi làm ĐỀ B"*. Nhưng app **chưa
làm được lời hứa đó** — bé trượt xong chỉ có nút "Làm lại" đúng đề cũ.

Trạng thái: `deB` đang là **dòng thô**, mỗi dòng gói nhiều câu
(`"B1. Tách số 692… B2. Viết thêm số 0…"`). Riêng **đáp án B thì đã tách xong** —
12 câu, nằm ở `dapAnB`. Nên việc còn lại chỉ là tách phần đề và cho ExamPlayer một
lối vào đề B.

Ước lượng: tách đề (`rut_ontap_lop2.py`) + nút "Làm đề B" ở màn kết quả. Nhỏ, gọn.

### 2 · Bảng cô giáo chưa thấy lớp 2

`TeacherBoard.jsx:7` còn cắt cứng tiền tố lớp 5:
```js
const short = (id) => String(id || '').replace('DL:KSN5Q1.', '');
```
Mã bài lớp 2 hiện nguyên `DL:KSN2.B01` nên cô đọc rối. Sổ phụ huynh đã lọc theo
chương trình rồi, chỉ còn màn này. Sửa nhỏ, cùng kiểu đã làm ở `ExamPlayer`.

### 3 · Nạp Firebase muộn — 130 KB gzip khỏi lần tải đầu

Firebase SDK là **554 KB / 130 KB gzip**, chiếm 2/3 gói. Tách gói đã giúp lần tải
SAU; muốn giảm cả lần ĐẦU thì phải `import()` động.

**Chặn ở đâu:** `src/lib/firebase.js` (215 dòng, 21 hàm xuất) **không có phép kiểm
nào**. Sửa luồng đăng nhập mà không có lưới an toàn là liều. Thứ tự đúng: viết phép
kiểm cho firebase.js trước, rồi mới đổi sang import động.

Lưu ý khi làm: `watchAuth` hiện trả hàm huỷ đăng ký **đồng bộ** — nạp muộn thì phải
giữ nguyên giao kèo ấy (trả hàm huỷ, huỷ luôn cả khi SDK chưa nạp xong).

### 4 · Lời văn của ĐỀ BÀI còn dài

7,6% câu vượt 20 chữ (163/2135). Con số này **tăng từ 5,7%** khi tôi cho phép đo
tính cả đề bài — nghĩa là đề bài dài dòng hơn phần giảng. Phần giảng đã được viết
lại kỹ, đề bài thì chưa. Dùng đúng cơ chế `VIET_LAI` trong `de_hieu_lop2.py`.

### 5 · Những việc nhỏ, làm khi tiện

- 1 câu ôn tập (Ô3 câu 10 — mật thư) chưa có trong Bảng tự soi vì sách viết
  *"dãy C của mật thư"* chứ không viết số. Đang tạm trỏ về bài đầu chương.
- `firebase-admin` 12 → 14 (v7 nhận cả hai, không gấp).
- `nodemailer ^9.0.5` — số hiệu lạ, nên soi lại xem có đúng gói mình nghĩ không.

---

## KHÔNG nên làm — đã cân nhắc và loại

**Chấm máy 281 câu luyện tập.** Nghe hợp lý nhưng đã đo: chỉ **11/281 câu (3%)** có
đáp án là số thuần hoặc dãy số. 97% còn lại là câu chữ (*"3 trăm, 6 chục, 8 đơn
vị"*, *"lớn hơn vì 9 chục > 2 chục"*). Ép chấm máy là **chấm oan bé viết đúng** —
đúng bài học đã trả giá ở Quyển 2 lớp 5. Giữ tự chấm.

**Gộp `Home.jsx` và `HomeLop2.jsx` thành một component.** Hai trang khác nhau mười
điểm chính sách (khoá bài · chế độ học · thẻ hôm nay · thẻ ôn · bảng sao · chương
gập mở · luật mở kỳ thi · ba ải · Mùa giải · màu đầu trang). Một component mười cờ
khó đọc hơn hai tệp rõ việc. Phần lặp thật — dòng danh sách — **đã gom** vào
`DongDanhSach.jsx`, dùng chung cả hai lớp.

---

## Dây chuyền

```bash
python3 tools/lam_lop2.py     # 6 bước, PHẢI chạy liền nhau
cd web && npm test && npm run build
```

Vẽ lại hình thì chạy riêng `python3 tools/ve_hinh_lop2.py` (chậm, mà bản mô tả hình
gần như không đổi theo lời văn).

## Bốn cái bẫy đã dính — đừng dính lại

- **Gắn hình phải ở BƯỚC CUỐI.** Bước dựng dữ liệu ghi đè trọn tệp bài học; gắn hình
  trước nó là mất sạch hình mà dữ liệu vẫn hợp lệ và bài vẫn chạy — không có gì báo.
- **Đừng neo hình theo nguyên văn dòng.** Lời văn đã được viết lại ở bước 2. Neo theo
  THỨ TỰ BƯỚC (`neoBuoc`) hoặc MÃ CÂU (`neoCau`).
- **`npm test` nối bằng `&&`.** Một tệp vỡ là dừng cả chuỗi mà tổng PASS trông vẫn
  đẹp. Luôn soi **mã thoát** và **số tệp chạy xong (17)**.
- **Trước khi deploy functions**, chạy `firebase emulators:start --only functions`:
  nó nạp hàm đúng như deploy, bắt được API đã bị bỏ mà không đụng backend thật.

## Hai thư mục lớp 2, hai vai — cố ý KHÁC nhau

| | |
|---|---|
| `data/lop2/` | bản GỐC giữ 8 mục ①…⑧ của sách, để đối chiếu sách giấy |
| `web/public/content/lop2/` | bản KHUÔN CHUNG với lớp 5, app đọc bản này — **sửa tay ở đây là mất** |

---

## Đợt 1 chuyển video · chương 1 · Vương quốc Số

Năm bài chữ thành **mười bài video**. Quyển lớp 2 nay **38 bài**.

| bài | mã | một việc duy nhất |
|---|---|---|
| 1 | B01 | ba phòng của một số |
| 2 | B34 *(mới)* | mỗi chữ số đáng bao nhiêu · tách thành tổng |
| 3 | B35 *(mới)* | so hai số — so phòng bên trái trước |
| 4 | B02 | thêm số 0 vào bên phải — to gấp mười |
| 5 | B36 *(mới)* | xoá số 0 tận cùng — nhỏ đi mười lần |
| 6 | B03 | đổi chỗ hai chữ số — số nào lớn hơn |
| 7 | B37 *(mới)* | hiệu hai số đổi chỗ — toàn số bảng nhân 9 |
| 8 | B04 | xếp thẻ: số lớn nhất và bé nhất |
| 9 | B38 *(mới)* | khi có thẻ số 0 |
| 10 | B05 | tìm đủ mọi số — đi tuần tra có thứ tự |

### Bác chốt: video KHÔNG nhân vật, giống lớp 4

Quyển lớp 2 lấy nhân vật làm khung (phụ đề kệ sách, tên chương), nhưng video đi
thẳng vào toán. Nên bốn mục còn chữ của bài cũng bỏ tên nhân vật luôn — để bé xem
video xong đọc tiếp không thấy đổi giọng. Có phép soi canh: bài nào còn chữ
"Trí Long" hay "Su Kem" là bộ soạn dừng ngay.

### Ba chỗ lớp 2 khác lớp 4 — phải theo, đừng bê nguyên khuôn lớp 4

1. **Tám mục**, không phải mười (không có dựng mô hình và lắp - soi);
2. **Số câu luyện tập không cố định** — 18 bài có 8 câu, 13 bài có 9, 2 bài có 10.
   Ép về một con số là phải bịa thêm câu hoặc cắt mất câu của sách;
3. **LUẬT Ô NHẬP SỐ 1** — quyển đọc chậm KHÔNG được có ô gõ chữ. Đáp không phải con
   số thì bắt buộc cho bấm nút. `khuon_bai_lop2.soi_bai` canh, và đã phá thử.

### Hạ tầng phải làm trước

* **lối C** — `data/lop2/thu_tu.json`. Nửa phía màn hình hoá ra đã có sẵn:
  `noiDung.js` vốn đếm số bài từ vị trí cho mọi quyển;
* **trường `video`** trong `dung_khuon_chung.py`;
* **`them_goi_y.py` và bộ dựng video** mở cho nhiều quyển (`--quyen lop2`).

### Vẫn đúng lớp lỗi cũ

**14 hình mồ côi** neo vào mục nay đã rỗng — lần thứ tư liên tiếp, luôn cùng một chỗ.

**Kỳ sát hạch trỏ sai bài.** Lớp 2 khai mối nối bằng `diagnosesMicro`, và bộ dựng
suy mã bài từ SỐ BÀI CỦA SÁCH. Sau khi tách, câu "điền dấu lớn bé" vẫn trỏ về B01 —
mà B01 nay chỉ dạy ba phòng. Đã khai đích danh sáu mối nối ở `KHAI_TAY_L2`, và viết
lại câu 6 (hỏi trùng ý câu 2) cho phủ bài xoá số 0.

Cổng `on_tap_noi_bai.test.mjs` nay soi **cả hai quyển** — nó đọc được cả `veBai` của
lớp 4 lẫn `diagnosesMicro` của lớp 2. Đã phá thử ba kiểu trên lớp 2, cả ba đều kêu.

### Còn lại của quyển

Bảy chương, **28 bài chữ**: bé là vua đếm (3) · dãy số kỳ diệu (3) · siêu nhân tính
nhanh (4) · chuyện toán lời văn (6) · thám tử tí hon (4) · vương quốc hình học (5) ·
toán trong cuộc sống (3).

---

## Đợt 2 · chương 2 · Bé là vua đếm

Ba bài chữ thành **sáu bài video**. Quyển lớp 2 nay **41 bài**.

| bài | mã | một việc duy nhất |
|---|---|---|
| 11 | B06 | đếm từ đâu đến đâu — trừ rồi thêm một |
| 12 | B39 *(mới)* | đếm nhảy cóc — cách 2 và cách 5 |
| 13 | B07 | truy tìm chữ số — chia hai cánh quân |
| 14 | B40 *(mới)* | số đứng ở cả hai cánh — chỉ bắt một lần |
| 15 | B08 | trang khác chữ số — chia hai đoàn tàu |
| 16 | B41 *(mới)* | đếm chữ số cả cuốn — cộng hai đoàn tàu |

### Vì sao tách đúng ba chỗ ấy

**B06** gộp "đếm từ a đến b" với "đếm nhảy cóc" — hai nghề khác nhau. Cái đầu là hiểu
vì sao phải THÊM MỘT; cái sau là nhận ra quãng nhảy đều.

**B07** gộp "chia hai cánh quân" với "bớt số đếm hai lần". Cái sau là mầm non của
phép đếm phần bù ở lớp 4 — đáng đứng riêng một bài.

**B08** gộp "trang khác chữ số" với "cộng hai đoàn tàu". Bé hay tắc ở bước cộng cuối,
nên tách ra cho bước ấy có chỗ riêng.

### Số neo

    từ nhà 3 đến nhà 7   → 5 nhà, mà phép trừ chỉ ra 4
    2, 4, 6, 8, 10       → nhảy cóc cách hai
    chữ số 5 từ 1 tới 99 → 10 + 10 − 1 = 19
    cuốn 25 trang        → 9 + 32 = 41 chữ số

### Cổng bắt được

Ẩn dụ **"bước chân"** lọt vào lời đọc của bài nhảy cóc — `video_toan.test.mjs` kêu
ngay. Và **10 hình mồ côi** neo vào mục nay đã rỗng (lần thứ năm).

Kỳ sát hạch: khai thêm **năm mối nối** ở `KHAI_TAY_L2`. Ba bài mới vốn không câu nào
hỏi tới — phép ④ của cổng `on_tap_noi_bai` tìm ra đúng ba chỗ trống ấy. Lần này
không phải viết lại câu nào: mười câu của sách chia vừa đủ cho sáu bài.

---

## Đợt 3 · chương 3 · Dãy số kỳ diệu

Ba bài chữ thành **chín bài video** — chương gộp nặng nhất từ trước tới nay. Quyển
lớp 2 nay **47 bài · 25 video · 22.3 phút**.

| bài | mã | một việc duy nhất |
|---|---|---|
| 17 | B09 | bắt nhịp — trừ để tìm nhịp, cộng để đi tiếp |
| 18 | B42 *(mới)* | toa mờ ở giữa — bắt nhịp ở hai số còn rõ rồi lần ngược |
| 19 | B43 *(mới)* | số này có trong dãy không — nhảy cóc thử |
| 20 | B10 | dãy gấp đôi — mỗi số bằng số trước cộng chính nó |
| 21 | B44 *(mới)* | dãy bậc thang — bước nhảy dài thêm một |
| 22 | B45 *(mới)* | quy luật phải đúng với MỌI số đã cho |
| 23 | B11 | chẵn hay lẻ nhìn ở đuôi — chữ số tận cùng |
| 24 | B46 *(mới)* | bảng nhân 2 toàn chẵn, bảng nhân 5 đuôi 0 hoặc 5 |
| 25 | B47 *(mới)* | cộng chẵn lẻ — chưa tính đã biết tổng |

### Vì sao tách thành ba chứ không phải hai

**B09** ôm ba động tác khác hẳn nhau: ĐI XUÔI (tìm nhịp rồi cộng tiếp), LẦN NGƯỢC
(điền số mờ ở giữa), KIỂM TRA (số này có thuộc dãy không). Bé tắc ở động tác nào
thì phải xem lại đúng động tác ấy — gộp một bài thì không chỉ được chỗ nào.

**B10** ôm dãy gấp đôi, dãy bậc thang, và *"quy luật phải đúng với tất cả các số"*.
Cái thứ ba mới là bài học thật của cả chương, mà nó nằm lọt thỏm ở bước 4 của sách.

**B11** ôm nhìn đuôi đoán chẵn lẻ, bí mật hai bảng nhân, và cộng chẵn lẻ.

### Số neo

    4, 8, 12, 16       → nhịp 4, tiếp là 20 và 24
    5, ?, 15, 20       → số mờ là 10
    3, 6, 9, ...       → không dừng ở 20, nhảy thẳng 18 sang 21
    1, 2, 4, 8         → gấp đôi, tiếp là 16
    2, 3, 5, 8, 12     → bậc thang, tiếp là 17
    134 chẵn · 275 lẻ  → nhìn chữ số tận cùng
    26 + 13            → chẵn cộng lẻ ra lẻ

### Cổng bắt được — và hai chỗ cổng KHÔNG bắt được

Cổng bắt: **sáu bài mới không câu ôn tập nào hỏi tới** (phép ④ của
`on_tap_noi_bai`), **bốn gợi ý lộ đáp án**, **sáu bài thiếu lời chào**.

Hai chỗ chỉ lộ khi **mở mắt xem bản chạy thật**:

1. **Lời chào của B10 nói về dãy của bài khác.** B10 nay dạy dãy gấp đôi 1, 2, 4, 8,
   mà lời chào vẫn mời bé đoán tiếp dãy 2, 3, 5, 8, 12 — dãy ấy nay là của B44.
2. **Lời chào của B11 hỏi đúng câu của B47**, lại còn nhắc tên nhân vật.

Cả hai đều qua được cổng `loi_chao.test.mjs` cũ, vì cổng ấy soi HÌNH DẠNG (có hay
không, dài bao nhiêu, mấy câu) chứ không soi NỘI DUNG. Đã dựng
`web/test/loi_chao_dung_bai.test.mjs`: mọi số và mọi dãy số nêu trong lời chào phải
có mặt trong chính bài ấy, và lời chào bài video không được nhắc tên nhân vật. Đo
trên cả 120 bài video của ba quyển thì 0 chỗ lệch — nên đòi 0. Đã phá thử bốn kiểu,
kêu cả bốn.

### Một câu ôn tập viết lại

Câu 5 hỏi *"đoàn tàu 3, 6, 9, ..., 27 có mấy toa"* — đúng ý câu C8 luyện tập của bài
NHẢY CÓC THỬ, mà câu 9 đã phủ bài ấy rồi; trong khi bài BẢNG NHÂN GIẤU GÌ không câu
nào hỏi tới. Viết lại câu 5 thành *"số 37 có nằm trong bảng nhân 5 không"*. Nghề đếm
toa vẫn còn nguyên ở phần luyện tập nên sách không mất gì.

`KHAI_TAY_L2` nay nhận thêm trường `khoa` để khai đè ô nhập — vá vào
`lop2_ontap_o.json` thì lần chạy `tach_ontap.py` sau sẽ dựng lại tệp ấy và xoá mất.

### Còn lại của quyển

Năm chương, **22 bài chữ**: siêu nhân tính nhanh (4) · chuyện toán lời văn (6) ·
thám tử tí hon (4) · vương quốc hình học (5) · toán trong cuộc sống (3).

---

## Đợt 4 · chương 4 · Siêu nhân tính nhanh

Bốn bài chữ thành **mười bài video**. Quyển lớp 2 nay **53 bài · 35 video · 31.8
phút · 429 câu luyện tập** (405 chấm máy).

| bài | mã | một việc duy nhất |
|---|---|---|
| 26 | B12 | ghép đôi tròn chục — dòm đuôi tìm đôi bạn |
| 27 | B48 *(mới)* | ghép hai khay kẹo — cùng số hàng thì gộp làm một |
| 28 | B13 | ghép cặp đầu với cuối — mọi cặp bằng nhau |
| 29 | B49 *(mới)* | dãy lẻ số thì có một bạn đứng giữa |
| 30 | B14 | cho kết quả chạy ngược — cộng và trừ |
| 31 | B50 *(mới)* | máy nhân và máy chia ngược nhau |
| 32 | B51 *(mới)* | khi số cần tìm bị lấy đi — 14 trừ ô trống bằng 6 |
| 33 | B15 | chia theo vòng — mỗi bạn mấy viên, thừa mấy |
| 34 | B52 *(mới)* | luật vàng — số thừa phải bé hơn số bạn |
| 35 | B53 *(mới)* | chia hết hay còn thừa — bảng nhân là danh sách chia đẹp |

### Chữ "X" của sách phải bỏ

Sách đặt tên bài là *"ĐI TÌM SỐ BÍ MẬT X"*. Máy đọc chữ X thành tiếng Anh — lớp 4
đã dính đúng mười lăm chỗ như thế. Cả bốn bài tìm ô trống ở đây gọi thẳng là
**"ô trống"**, và `tools/tinh_nhanh_lop2.py` có phép soi chặn cả `X` lẫn `▢`.

### LỖI CHỈ LỘ KHI MỞ MẮT XEM — lần này ở HÌNH VẼ TRONG VIDEO

Bài 27 mượn cảnh `nhom_deu` để vẽ khay kẹo. Lời đọc bảo *"ba hàng, mỗi hàng bốn
viên"*, mà `nhom_deu` xếp tối đa ba viên một dòng nên vẽ ra **ba NHÓM bốn viên, mỗi
nhóm gấp thành hai dòng**. Bé nghe "hàng" mà nhìn thấy "nhóm" — trong khi cả bài
dạy phép nhân đứng trên đúng chữ "hàng" ấy.

Không cổng nào bắt được: cảnh hợp lệ, video dựng ra bình thường, lời đọc sạch. Chỉ
lệch giữa LỜI và HÌNH.

Đã thêm cảnh **`luoi_cham`** vào `tools/video/dung_video.py`: vẽ đúng một lưới
`hang` dòng × `cot` viên, và `cot2` vẽ phần nối dài bên phải bằng màu khác — đúng
lúc hai khay đẩy sát vào nhau.

Soát lại **toàn bộ 17 cảnh `nhom_deu`** của cả bốn quyển thì thấy thêm **bốn chỗ
cùng lỗi ở chương 3**: lời bảo *"8 viên chia đôi, mỗi bên 4 viên"* mà hình vẽ bốn
CẶP. Sửa cả bốn: muốn vẽ hai nửa thì `moiNhom` phải là số viên MỖI NỬA, không phải
số nửa.

### Còn lại của quyển

Bốn chương, **18 bài chữ**: chuyện toán lời văn (6) · thám tử tí hon (4) · vương
quốc hình học (5) · toán trong cuộc sống (3).

---

## Đợt 5 · chương 5 · Chuyện toán lời văn

Chương dài nhất của quyển. Sáu bài chữ thành **mười hai bài video** — bài nào cũng
gộp đúng HAI nghề ngược chiều nhau, nên đợt này tách đôi đều tăm tắp. Quyển lớp 2
nay **59 bài · 47 video · 42.8 phút · 476 câu luyện tập** (456 chấm máy).

| bài | mã | một việc duy nhất |
|---|---|---|
| 36 | B16 | chia đều — phép chia và khuôn ba dòng |
| 37 | B54 *(mới)* | bài ngược — biết mỗi phần, tìm tất cả |
| 38 | B17 | sơ đồ hai đoạn thẳng — ai dài, ai ngắn |
| 39 | B55 *(mới)* | bẫy câu chữ đảo — "An ít hơn Bình" thì ai nhiều hơn |
| 40 | B18 | liệt kê có thứ tự mọi cách tách tổng |
| 41 | B56 *(mới)* | dò cột hơn nhau — thử lại đủ hai điều kiện |
| 42 | B19 | vẽ theo phần — gấp mấy lần là mấy khối |
| 43 | B57 *(mới)* | chia tổng cho số phần rồi trả về từng người |
| 44 | B20 | tuổi sau mấy năm — ai cũng thêm bằng nhau |
| 45 | B58 *(mới)* | phần hơn tuổi không bao giờ đổi |
| 46 | B21 | biết mỗi giờ, hỏi tất cả — phép nhân |
| 47 | B59 *(mới)* | biết tất cả, hỏi mỗi giờ — phép chia |

### Dùng lại sơ đồ đoạn thẳng của lớp 4

Bốn bài dùng cảnh `so_do_doan` — vốn dựng cho chương tổng-hiệu lớp 4, nay chạy cho
hai dạng của lớp 2 mà không phải sửa gì:

- **hơn kém** → hai đoạn lệch nhau, khúc dôi ra tô vàng là phần hơn;
- **chia phần** → `phanBe`/`phanLon` chia đoạn thành các khối bằng nhau.

Đã rút khung hình ra nhìn cả ba loại — theo đúng bài học của đợt trước
([[hinh-trong-video-phai-khop-loi-doc]]) — cả ba đều vẽ đúng thứ lời đọc đang nói.

### Cổng bắt được ngay lúc viết

Ẩn dụ **"thần chú"** trong tên một cảnh — `dung_video_toan.py --loi` kêu trước cả
khi sinh âm, nên không tốn một clip nào. Còn 96 gợi ý thì qua sạch ngay lượt đầu.

### Một tên kỳ sát hạch thành mồ côi

Kỳ ôn tập 5 tên là *"TUYỂN TẬP CHUYỆN TOÁN CỦA TRÍ LONG"*. Chương này nay không còn
bài chữ nào, nên nhân vật ấy không xuất hiện ở đâu trong chương nữa — bé đọc thấy
một cái tên chưa gặp bao giờ. Đã đổi thành *"TUYỂN TẬP CHUYỆN TOÁN LỜI VĂN"* qua
bảng `DOI_TEN_KY_L2`. Kỳ ôn tập 8 vẫn giữ tên có nhân vật, vì chương 8 còn bài chữ.

### Một câu ôn tập đảo chiều

Câu 6 cũ hỏi lại đúng ý câu 2 — đều là tìm người ÍT hơn, phép trừ thẳng — trong khi
bài BẪY CÂU CHỮ ĐẢO không câu nào hỏi tới. Đã đảo chiều câu 6 cho người phải tìm
thành người NHIỀU hơn, đúng cái bẫy mà bài ấy dạy.

### Còn lại của quyển

Ba chương, **12 bài chữ**: thám tử tí hon (4) · vương quốc hình học (5) · toán
trong cuộc sống (3).

---

## Đợt 6 · chương 6 · Thám tử tí hon

Bốn bài chữ thành **tám bài video**. Nghề thứ hai của mỗi bài luôn là CHỖ SÁCH TỰ
NÊU RA LÀ HAY SAI NHẤT — đúng thứ đáng đứng riêng. Quyển lớp 2 nay **63 bài · 55
video · 50.7 phút · 506 câu luyện tập** (490 chấm máy).

| bài | mã | một việc duy nhất |
|---|---|---|
| 48 | B22 | đi lùi qua hai máy — đảo phép từng máy |
| 49 | B60 *(mới)* | máy làm sau cùng thì lùi qua trước |
| 50 | B23 | đếm chân — gắn tạm hai chân cho tất cả |
| 51 | B61 *(mới)* | chân thừa chia thành từng cặp |
| 52 | B24 | cây và khoảng — luật bàn tay |
| 53 | B62 *(mới)* | biết chiều dài, tìm số cây |
| 54 | B25 | vẽ thang xếp thứ tự |
| 55 | B63 *(mới)* | bảng loại trừ — đánh dấu rồi gạch |

### Cảnh mới: `bang_loai_tru`

Cả bài 55 đứng trên một cái bảng ba hàng ba cột. Nói bằng lời thì rối; vẽ ra thì bé
thấy ngay hàng nào chỉ còn một ô trống. Cảnh nhận `hang`, `cot` và `o` — mỗi ô là
`""` (chưa biết), `"v"` (đúng, tô teal) hoặc `"x"` (đã loại, tô đỏ). Video đi qua
năm trạng thái của cùng cái bảng ấy, từ trống trơn tới kín dấu.

### Hai chữ cấm của chính tên chương

`TU_CAM` có sẵn **"thám tử"** và **"vũ khí"** — chúng là vỏ nhân vật của sách, mà
tên chương lại đúng là *"Thám tử tí hon"*. Tên chương giữ nguyên trong dữ liệu, còn
lời đọc và chữ trên màn thì tránh; `tools/suy_luan_lop2.py` có phép soi riêng, chỉ
soi phần THÂN bài chứ không soi `tenChuong`.

### Lại hai câu ôn tập mồ côi tên nhân vật

Quét toàn bộ kỳ sát hạch lớp 2 thì thấy **hai câu ở chương ĐÃ chuyển hết sang
video** vẫn nhắc tên nhân vật: chương 6 câu 4 và chương 2 câu 10. Đã viết lại cả
hai thành "một bạn". Chương 8 và ải 3 giữ nguyên, vì chương 8 còn bài chữ nên nhân
vật vẫn có mặt thật.

### Còn lại của quyển

Hai chương, **8 bài chữ**: vương quốc hình học (5) · toán trong cuộc sống (3).
