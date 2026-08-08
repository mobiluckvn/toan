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
