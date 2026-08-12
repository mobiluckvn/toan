# Đi thử trên BỘ GIẢ LẬP — không đụng dữ liệu thật

Ghi 12-08-2026, sau lần đi thử end-to-end đầu tiên của quyển Tiếng Anh lớp 1.

## Java đã có sẵn, chỉ là không nằm trên PATH

Bộ giả lập Firestore chạy bằng Java. `java -version` báo "Unable to locate a Java
Runtime" nên rất dễ tưởng là chưa cài — nhưng `openjdk` **đã cài qua brew**, chỉ là
brew để nó *keg-only* (không nối vào PATH, tránh đè bản Java của hệ thống).

```bash
/usr/local/opt/openjdk/bin/java -version      # có thật
```

## Chạy

```bash
# cửa sổ 1 — bộ giả lập
cd web
PATH="/usr/local/opt/openjdk/bin:$PATH" \
  npx firebase emulators:start --only auth,firestore,functions

# cửa sổ 2 — app nối vào bộ giả lập
cd web && VITE_FB_EMULATOR=1 npx vite --port 5174
```

`dungGiaLap` buộc kèm cờ `DEV`, nên bản `npm run build` để deploy KHÔNG mang khối
nối giả lập theo — không phải tin vào việc người dựng nhớ tắt cờ.

**Mã OTP in ra log của cửa sổ 1**, không gửi mail:

```
> [OTP] BỘ GIẢ LẬP — không gửi mail. Mã cho …@example.test: 738922
```

## Thử luật Firestore

```bash
node test/luat_firestore.test.mjs        # cần bộ giả lập đang chạy
```

14 phép kiểm, và **quá nửa là chiều BỊ TỪ CHỐI** — đó mới là phần đáng giá:

```
✓ chính chủ ghi được bài của mình      ✓ bé A KHÔNG ghi được vào sổ bé B
✓ thiếu trường luật đòi → từ chối       ✓ sai kiểu dữ liệu → từ chối
✓ cô giáo đọc được sổ học sinh          ✓ bé B KHÔNG đọc được sổ bé A
✓ loại học bạ lạ → từ chối              ✓ collection chưa khai luật → chặn
✓ chính chủ KHÔNG xoá được bài đã học   ✓ máy con KHÔNG ghi được bảng xếp hạng
```

Không có bộ giả lập thì tệp này **bỏ qua êm và NÓI RA** — cổng im lặng là cổng
không ai biết đã ngừng canh.

`tienganh_may_chu.test.mjs` (chạy được mọi lúc) chỉ đọc tệp luật bằng regex: nó bắt
"quên viết luật", không bắt được "luật viết rồi mà sai". Hai tệp bù nhau.

## Ba chỗ vấp khi đọc kết quả — đều là ĐỌC NHẦM DẤU HIỆU

Ghi lại vì cả ba đều làm mất thời gian, và cả ba đều là *tin vào một dấu hiệu không
có nghĩa như mình tưởng*.

**1 · `curl` trả 200 không có nghĩa là tệp có thật.** Máy chủ dev trả `index.html`
thay cho mọi đường không khớp. Sổ âm nằm sai thư mục mà `curl` vẫn 200; chỉ tới
`r.json()` mới vỡ, mà chỗ ấy lại có `catch` nuốt lỗi. Muốn biết có tệp thật thì
**đọc nội dung ra mà xem**, đừng nhìn mã trạng thái.

**2 · Đọc Firestore qua REST mà quên token thì bị luật từ chối** — và nếu chỗ bắt
lỗi trả về mảng rỗng thì nó hiện thành "0 tài liệu", trông y hệt "chưa ghi được gì".
Đã tưởng lệnh ghi hỏng trong khi dữ liệu nằm đúng chỗ. Phép đọc phải **in lỗi ra**,
đừng quy lỗi thành rỗng.

**3 · Ghi rồi mà `LOI_GHI.tuChoi` bằng 0** có thể nghĩa là "ghi trót lọt" HOẶC "lệnh
ghi chưa từng chạy". Hai chuyện khác hẳn nhau. Phân biệt bằng cách đọc ngược lại từ
máy chủ, không suy từ bộ đếm.

## Đi thử trọn một vòng

Đã chạy thật, không phải suy:

1. Đăng nhập bằng OTP → lập hồ sơ, **chọn được lớp 1** (trước bản này thấp nhất là lớp 2)
2. Học trọn Unit 1: 26 câu luyện tập bốn bậc + 5 câu sát hạch
3. `progressTA/{uid}/micros/DL_TA1_B01` xuất hiện trên máy chủ, đúng hình dạng
4. **Xoá sổ tại máy** rồi tải lại → tiến độ kéo về từ máy chủ

Bước 4 mới là bước chứng minh: ba bước đầu chỉ nói dữ liệu đi ra được.

## Còn nợ

`hocBaTA` hiện **0 tài liệu** — hàm `luuMucHocBa` đã có nhưng chưa ai gọi, vì màn kỳ
ôn tập chương của Tiếng Anh chưa dựng. Bốn kỳ đã khai ở `ta1/ontap.json`, chưa có
màn hình.
