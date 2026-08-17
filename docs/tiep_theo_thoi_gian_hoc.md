# Điểm dừng — ĐO THỜI GIAN HỌC · BẢNG CÔ GIÁO · BẢNG XẾP HẠNG

Ghi 17-08-2026. Đọc trang này trước khi động vào phần ghi giờ hoặc hai cái bảng.

## Đã xong và ĐÃ LÊN BẢN THẬT

| | |
|---|---|
| Đo giờ | `src/mon/toan/lib/dongHo.js` — đo theo **BƯỚC**, nên bước xem video có số |
| Từng bài nhỏ | `progress/{uid}/micros` thêm `giay` · `giayXem` · `giayLam` |
| Theo ngày | `hocBa/{uid}/muc` `loai='gio'`, cộng dồn bằng `increment` |
| Sổ bố mẹ | lấy số đo thật; không có thì lùi về ước lượng và **nói rõ là ước lượng** |
| Bảng cô giáo | mục **EM CẦN GIÚP TRƯỚC**, xếp theo EM, kèm lý do yếu |
| Bé | "⏱ hôm nay N phút" trên trang chính, lấy sổ tại máy nên hiện ngay |
| Luật | `firestore.rules` nhận `loai='gio'` — **đã deploy** |
| Hàm máy chủ | `nightlyReport` · `nightlyTeacherBoard` — **đã deploy** |

Cổng: `dong_ho_hoc.test.mjs` (23) · `luat_firestore.test.mjs` (25) · toàn bộ 59 tệp,
0 FAIL. Cả hai đều đã **thử ngược** và đỏ đúng chỗ.

## ⚠ MẮT XÍCH CUỐI CÙNG CHƯA CÓ BẰNG CHỨNG

**Chưa buổi học thật nào chạy qua đường mới.** Mọi thứ trên đây đúng ở tầng hàm và
tầng luật, nhưng chưa ai xác nhận một lượt học thật sinh ra tài liệu
`hocBa/{uid}/muc/gio_YYYY_MM_DD`.

Cách kiểm, KHÔNG cần đụng bản thật (xem `docs/di_thu_gia_lap.md`):

```bash
cd web && PATH="/usr/local/Cellar/openjdk/26.0.2/bin:$PATH" \
  npx firebase emulators:start --only auth,firestore,functions
cd web && VITE_FB_EMULATOR=1 npx vite --port 5174
```

Mã OTP in ra log cửa sổ 1, không gửi mail. Đăng nhập → học **một micro** → rồi soi
ba thứ: tài liệu `gio_…` có sinh ra không · ba con số giây có đúng không ·
`progress` của micro ấy có `giay`/`giayXem` không.

⚠ **Đừng đăng nhập tài khoản thử vào BẢN THẬT.** Nó lọt vào `bangXepHang/global` —
tài liệu duy nhất trẻ con đọc được về nhau — và bảng cô giáo đếm nó như học sinh
thật. Xem `bang-xep-hang-lo-du-lieu-be` trong sổ nhớ.

## Hai việc còn để ngỏ, bác chưa chốt

**1 · Adaptive đọc tín hiệu thời gian.** `lib/adaptive.js` và `functions/src/bkt.js`
hiện chỉ đọc đúng/sai. Nay đã có `giay` mỗi bài thì phân biệt được "đúng vì hiểu" với
"đúng vì đoán trúng". Chưa làm vì nó đổi cách chọn bài kế cho bé — cần bàn ngưỡng.

**2 · Cột thời gian trên bảng xếp hạng.** Cháu khuyên **KHÔNG**: bảng thưởng "học
lâu" là dạy bé mở app rồi để đấy. Ba cột hiện nay đều thưởng **việc làm được**. Nếu
bác vẫn muốn thì đăng **"số ngày có học"** thay vì "số phút" — vẫn khuyến khích đều
đặn mà không tạo động cơ ngồi lì. ⚠ Thêm trường vào bảng ấy phải sửa danh sách
`CHO_PHEP` trong `test/xephang.test.mjs`; cổng chặn mọi trường chưa được duyệt, và đó
chính là điểm của nó.

## Số liệu cũ sẽ mang nhãn ƯỚC

Buổi học TRƯỚC 17-08 không có giờ đo thật vì lúc ấy chưa có đồng hồ. Sổ hiện nhãn
**PHÚT (ƯỚC)** cho khoảng đó — cố ý, để bố mẹ biết con số ấy thiếu phần xem giảng.
Phải mất vài ngày cửa sổ 7 ngày mới toàn số thật.

## Ba chỗ vấp của MÁY NÀY

| | |
|---|---|
| `gcloud` | **không có trên máy** — đã tìm cả PATH, `zsh -lc`, `find`, tắt sandbox |
| Java | keg-only, đường thật `/usr/local/Cellar/openjdk/26.0.2/bin` (sổ cũ ghi `/usr/local/opt/openjdk/bin`) |
| cổng 8080 | thường đã có bộ giả lập chạy sẵn — cứ chạy thẳng cổng luật, không cần bật thêm |

## Bài học đắt nhất của đợt

**Cổng luật Firestore ĐÃ CÓ SẴN** từ 12-08 (`test/luat_firestore.test.mjs`, ghi trong
`docs/di_thu_gia_lap.md`), và tôi ghi đè mất nó sau khi tuyên bố "không cổng nào
canh". Trước khi dựng MỚI bất cứ cổng hay dây chuyền nào: `ls docs/` và
`ls web/test/` đọc hết TÊN một lượt, rồi grep theo **việc nó làm** chứ không theo tên
tệp mình đang định đặt.

Và: `npm test | grep | head -20` **giấu mất cổng đỏ nằm sau dòng 20**. Đếm số tệp,
đọc dòng tổng kết.
