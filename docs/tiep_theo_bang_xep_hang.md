# Điểm dừng — BẢNG XẾP HẠNG

Cập nhật 2026-08-11 (lượt sáu). Đọc tệp này TRƯỚC khi động vào bảng xếp hạng hay bất
cứ thứ gì đăng dữ liệu của bé này cho bé khác đọc.

> ✅ **ĐÃ DEPLOY ĐỦ BA PHẦN**: `functions` (hàm `refreshBangXepHang` tạo mới, 8 hàm cũ
> cập nhật) + `firestore rules` + `hosting`.
> Cổng: **34 tệp kiểm · 1071 PASS · 0 FAIL**.

---

## ĐÂY LÀ TÀI LIỆU DUY NHẤT MỘT BÉ ĐỌC ĐƯỢC VỀ BÉ KHÁC

Cả bộ luật Firestore dựng trên một nguyên tắc: *mỗi bé chỉ đọc dữ liệu của mình*.
`bangXepHang/global` phá nguyên tắc ấy **có chủ ý**. Vì thế nó là chỗ cẩn thận nhất kho:

```
đăng lên:  biệt danh · lớp · sao · chuỗi ngày · số bài đạt · huy hiệu · vòng đấu
KHÔNG:     email · số bài sai · bài đang tắc · bất cứ gì khác
rules:     allow read if signedIn()   ·   allow write if false
```

`allow write: if false` là chốt: máy con **không bao giờ** ghi được vào bảng, nên không
ai tự đặt điểm cho mình hay sửa tên bạn khác. Chỉ Cloud Function (Admin SDK) ghi.

⚠ **Bẫy tên**: `buildUserDoc` điền sẵn `displayName` = phần trước @ của email khi bé
chưa khai tên. Đưa thẳng trường ấy lên bảng là **lộ một mẩu email người lớn cho cả
trường đọc**. `tenHien()` vì thế lùi về `"Bạn nhỏ lớp 3"`, KHÔNG lùi về `displayName`
khi `profileComplete` còn false. Nửa đầu `test/xephang.test.mjs` chỉ để canh điều này.

---

## VÌ SAO BA BẢNG CHỨ KHÔNG MỘT

Lớp 5 có 168 bài, lớp 2 có 33. Xếp theo "tổng bài đã đạt" thì **Trí Long (lớp 2) và
Su Kem (lớp 3) nằm đáy vĩnh viễn** — đúng hai bé cần động lực nhất. Và bé vào sau
không bao giờ đuổi kịp bé vào trước: bảng cộng dồn mãi mãi chỉ thưởng người đến sớm.

| bảng | đo gì | ai có cửa |
|---|---|---|
| 🔥 Tuần này | sao trong 7 ngày, **đặt lại mỗi tuần** | mọi bé, kể cả mới vào |
| 📅 Chuỗi ngày | ngày học liên tiếp | bé chăm, không cần giỏi |
| 👑 Tổng sao | cả chặng đường | bé đi đường dài |

```
+1  mỗi câu trả lời đúng      trần 60 sao/ngày ← chặn ngồi bấm lại một bài 500 lượt
+10 mỗi bài học đạt
+30 mỗi huy hiệu chương
+50 mỗi vòng đấu Mùa giải đạt
```

Ba nguồn sau **một-lần-một-mã** nên không cày được; chỉ câu trả lời cần trần. Trần tính
**theo NGÀY**, không theo tổng — học đều ba ngày phải được sao của cả ba ngày.

**Tổng sao KHÔNG cộng câu trả lời đúng**: nhật ký chỉ giữ theo cửa sổ ngày, cộng vào là
con số tụt dần theo thời gian — một bảng "tổng" mà đi lùi thì bé không hiểu nổi.

---

## THỨ THÚC BÉ KHÔNG PHẢI HẠNG 1

Là câu **"còn 12 sao nữa là con vượt Su Kem"**. Nên:

* **luôn ghim dòng của con**, kể cả hạng 87 — sau dấu `⋯`, cuối Top 20;
* khoảng cách tính tới người **NGAY TRÊN THEO ĐIỂM**, không phải người đứng trên một
  dòng: ba bạn cùng 120 sao thì người cần vượt là bạn 130, không thì câu "còn 0 sao
  nữa là vượt" thành vô nghĩa;
* **đuổi kịp một bạn** — bấm 🎯 ở dòng bất kỳ, thanh so kè hai người. Tính trên TOÀN
  TRƯỜNG, không theo bộ lọc lớp đang xem, để lọc về "Lớp 3" không làm bạn ấy biến mất.

**Cố ý không làm**: không hiện hạng bét, không hiện "con đứng trên bao nhiêu bạn".
Bé cuối bảng không cần bị dí mũi vào chỗ đó — bảng này để thúc, không phải để xếp loại.

---

## MỘT LẦN ĐỌC, HAI BẢNG

`docDuLieuChung()` đọc roster + nhật ký + tiến độ + học bạ **một lần**, rồi
`dungBangGiaoVien` và `dungBangXepHang` cùng dùng. Hai bảng dựng cách nhau vài giây
trong cùng lần chạy đêm 21h15 — đọc hai lần là nhân đôi hoá đơn Firestore.

Nút "Cập nhật ngay" của bé gọi `refreshBangXepHang`, **chặn dội 120 giây**: không có
chốt ấy thì cả lớp cùng bấm là mỗi lượt quét toàn bộ nhật ký của cả trường.

`dungBangXepHang` ghi **ĐÈ** chứ không merge — `rows` là mảng, merge sẽ giữ mãi những
khoá cũ đã bỏ, và một em đã xoá tài khoản mà tên vẫn treo trên bảng là chuyện không
được phép xảy ra.

---

## CHƯA KIỂM ĐƯỢC — VIỆC CỦA BÁC

Cháu **không đăng nhập được** (nhập mật khẩu/mã đăng nhập là việc cháu không làm), nên
mới xác nhận được ba thứ từ bên ngoài:

* cửa vào bảng có trên kệ sách và trên trang mỗi quyển ✓
* chưa đăng nhập thì màn báo đúng "Con cần đăng nhập…" ✓
* luật chặn thật: đọc `bangXepHang/global` không token → `PERMISSION_DENIED` ✓
* hàm `refreshBangXepHang` sống, gọi không token → `UNAUTHENTICATED` ✓

**Bác đăng nhập rồi bấm 🏆 Xếp hạng → "↻ Cập nhật ngay"** là bảng dựng lần đầu. Nếu
không bấm thì 21h15 tối nay lịch chạy đêm tự dựng.

⚠ Lúc này hệ thống mới có tài khoản của bác nên bảng sẽ chỉ có **một dòng**. Bảng chỉ
thành thứ thú vị khi đã có vài bé thật cùng học.

---

## MAI VÀO VIỆC TỪ ĐÂU

1. **Chưa có khái niệm LỚP HỌC / TRƯỜNG** trong dữ liệu — chỉ có `grade` (2-5). Nhiều
   trường dùng chung một app thì bảng "Cả nhà" sẽ loãng, và bé sẽ so mình với người lạ.
   Cần thêm `lopHoc` vào hồ sơ trước khi mở cho trường thứ hai.
2. **Ba việc bác chưa chọn** ở lượt này, làm được ngay khi cần: bảng vinh danh trên
   trang chính · dòng thời gian "bạn cùng lớp vừa làm gì" · huy hiệu khoe được.
3. Ba hướng cũ trong `docs/tiep_theo_dinh_dang.md` vẫn còn.

---

Xem thêm `docs/tiep_theo_quyen2_dapan.md` và `docs/tiep_theo_man_nha.md`.
