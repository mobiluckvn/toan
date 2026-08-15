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
