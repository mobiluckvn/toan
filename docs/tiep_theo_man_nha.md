# Điểm dừng — MÀN NHÀ, HỌC BẠ, SỔ BỐ MẸ, BẢNG CÔ GIÁO

Cập nhật 2026-08-11 (lượt bốn). Đọc tệp này TRƯỚC khi động vào trang chính của quyển,
sổ bố mẹ, bảng cô giáo, hay bất cứ chỗ nào đếm "con học tới đâu".

> Cổng: **32 tệp kiểm · 1005 PASS · 0 FAIL** (trước đợt này: 30 tệp · 861 PASS).
> Đã đi thật trên bản dựng, 0 lỗi trong bảng điều khiển.
>
> ✅ **ĐÃ DEPLOY ĐỦ BA PHẦN** lúc 11-08-2026: `firestore rules` + `hosting` (1470 tệp)
> + `functions` (8 hàm cập nhật). Đây là lần đầu đẩy rules và functions sau nhiều đợt
> chỉ đẩy hosting — bắt buộc, vì thư mục `hocBa/{uid}/muc` là mới và luật mặc định là CẤM.
>
> Đã đi thật trên **https://ky-su-nhi.web.app** sau khi đẩy: kệ sách xếp đúng lớp 2→3→4→5
> →Mùa giải · trang lớp 4 chỉ đúng bài đang dở (Bài 22, bước 3) · sổ bố mẹ cả hai trục ·
> Mùa giải có hai lối ra · màn chủ đề tầng 2 có ⌂ Kệ sách.

---

## MỘT PHÉP ĐẾM CHO BỐN MÀN HÌNH — `web/src/lib/hocba.js`

Đây là thứ đáng giá nhất của đợt này. Trước đây bốn màn tự đếm lấy, mỗi màn một luật:

| màn | đếm kiểu cũ |
|---|---|
| trang chính lớp 5 | 14 chương gõ cứng, 12 bài mỗi chương gõ cứng |
| trang chính lớp 2·3·4 | danh sách phẳng, đúng **một** thẻ "bài tiếp theo" cho cả sách |
| sổ bố mẹ | `b.done / 12` — chia cứng cho 12 với mọi quyển |
| bảng cô giáo | chỉ có tổng số bài đạt, không tách theo quyển |

Bốn con số khác nhau về cùng một đứa trẻ, và không có cách nào biết cái nào đúng.

Nay `hocba.js` là **hàm thuần** (vào: chỉ mục đã nạp + sổ tiến độ; ra: số), nên phép
kiểm chạy được bằng node trên **dữ liệu thật của cả bốn quyển** — kể cả hai ngả bìa
hay rơi vào hư không: quyển chưa học bài nào, và quyển đã xong hết.

```
trangThaiBai      dat · dangDo · chuaDat · mo · khoa
baiDeXuatChuong   dở → chưa đạt & đã mở → null
thongKeChuong     master = xong hết bài VÀ qua kỳ sát hạch
hocBaQuyen        đếm quyển + việc tiếp theo + kỳ đang chờ
baiCanCoGang      đã thử mà chưa qua, nặng nhất lên đầu
hocBaChuDe        5 mảng → chủ đề → dạng: vững · đang học · cần cố gắng · chưa học
trinhDo           một dòng đọc trong ba giây
```

---

## BỐN QUYỂN, MỘT TRANG CHÍNH — `HomeQuyen.jsx`

`Home.jsx` (lớp 5) và `HomeLop2.jsx` (lớp 2·3·4) đã **gộp làm một**. Ghi chú cũ trong
`DongDanhSach.jsx` nói cố ý tách vì "mười điểm chính sách khác nhau" — đúng khi chỉ có
hai quyển. Với bốn quyển thì cái giá lộ ra: cùng là "trang chính của một quyển sách"
mà bé gặp hai app khác nhau.

Mười điểm khác biệt ấy nay **đọc từ `data/chuong_trinh.json`**, không từ tên quyển:

```
thuTu     thứ tự trên kệ sách        1 · 2 · 3 · 4 · 5
khoaBai   khoá bài tuần tự            chỉ lop5
quyen2    cửa sang quyển luyện thi    lop5 → lop5q2
chuong[]  tên 14 chương của lớp 5     (lớp 2·3·4 đã có trong index.json)
tepOnTap  danh mục kỳ ôn tập          lop5 → ontap_lop5.json
```

**Thứ bác dặn — mỗi chương có bài đề xuất riêng.** Chưa học chương nào thì nó chỉ vào
**bài ĐẦU chương ấy**; đang học dở thì chỉ vào chỗ dở; học rồi thì chỉ bài kế. Trước
đây lớp 2·3·4 chỉ có một thẻ cho cả 44 bài, nên mở chương 6 ra là không biết bắt đầu
từ đâu.

⚠ **`lessons/` chỉ được chứa BÀI HỌC.** Bốn phép kiểm quét thư mục ấy bằng `*.json` rồi
đọc thẳng `j.id`. Bản đầu của đợt này đặt `lessons/ontap.json` vào đó và làm vỡ cả bốn.
Nên lớp 5 khai đường dẫn riêng qua `tepOnTap`.

---

## ĐƯỜNG VỀ NHÀ — `ThanhTren.jsx`

Mọi màn không phải phòng học nay có **đúng hai lối, luôn ở đúng một chỗ**:
trái là lùi MỘT bước, phải là **⌂ Kệ sách**. Trước đây màn chủ đề đi sâu ba tầng thì
phải bấm "← Quay lại" ba lần; Mùa giải chỉ có một nút "⌂ Về trang chính" mà nó lại đưa
về trang lớp 5, không về kệ sách.

Cổng `mannha.test.mjs` canh việc này bằng cách đọc **mã nguồn**: màn gốc phải nhận cửa
về nhà, và `App.jsx` phải THẬT SỰ truyền nó xuống — nhận mà không ai truyền thì nút biến
mất trong im lặng.

---

## HAI LỖI CŨ, HỎNG CÂM, ĐÃ SỬA

### (a) Huy hiệu chương LÂY GIỮA CÁC QUYỂN

Sổ cũ khoá kỳ sát hạch bằng **số chương trần**: `chapters[3]`. Bốn quyển đều đánh chương
từ 1, nên con thi chương 3 của lớp 2 là **huy hiệu chương 3 của lớp 5 cũng sáng lên** —
và thi lại ở quyển kia thì đè mất kết quả cũ. Dữ liệu vẫn hợp lệ, cổng vẫn xanh.

Nay khoá là `lop3.5`. Bản ghi theo khoá cũ vẫn đọc được, **nhưng chỉ khi con mới học
đúng một quyển** — học từ hai quyển trở lên thì bỏ, thà thiếu còn hơn gắn nhầm.

### (b) "làm đúng **null** câu là qua"

Ba cửa ải của lớp 3 không đặt ngưỡng (`need: null`) vì sách chỉ bảo "làm hết 10 câu".
Màn cũ ghép chuỗi thẳng nên bé đọc được đúng chữ ấy trên màn hình. Chính cổng
`kesach.test.mjs` mới viết đã bắt ra.

Kèm hai chỗ cùng loại: `BangSuuTapSao` khen "Đủ **8** sao" cho cả lớp 4 (11 chương) và
lớp 5 (14 chương); chân trang khoe "Toán Tư Duy lớp 5 · 168 bài" ở cuối **mọi** màn.

---

## SỔ BỐ MẸ VÀ BẢNG CÔ GIÁO

**Sổ bố mẹ** (`ParentReport.jsx`) nay có hai trục, nhìn được cả bốn quyển:

* **theo lớp** — quyển → chương → bài, mỗi chương một nhãn `đã master` / `xong bài,
  chưa qua kỳ sát hạch` / `đang học` / `chưa học`, và bài chưa qua bấm được để mở lại;
* **theo chủ đề** — 5 mảng → chủ đề → 82 dạng bài, mỗi dạng `đã vững` / `đang học` /
  `cần cố gắng` / `chưa học`, kèm bậc lớp nào đã xong, bậc nào đã trượt.

**Bảng cô giáo** (`TeacherBoard.jsx` + `HocSinhChiTiet.jsx`) — bấm vào một em thì mới
tải học bạ của riêng em ấy, bốn tầng: tổng quan (trình độ · phút học · chỗ cần kèm) →
theo lớp/chương/bài → theo chủ đề/dạng → nhật ký từng câu (giữ nguyên bản cũ).

Dòng danh sách chung thêm **số phút học** và **trình độ** (quyển cao nhất em đã có bài
đạt) — "47 bài đạt" một mình không nói lên gì, 47 bài lớp 2 khác hẳn 47 bài lớp 5.

---

## LƯU DỮ LIỆU CHI TIẾT — thư mục `hocBa` mới

Sổ tiến độ có bốn phần, mà trước nay **chỉ một phần lên được mạng**:

```
micros    → progress/{uid}/micros    ✔ đã có
chapters  → hocBa/{uid}/muc  loai=chuong   ✘ chỉ nằm ở máy
chuDe     → hocBa/{uid}/muc  loai=chuDe    ✘ chỉ nằm ở máy
dau       → hocBa/{uid}/muc  loai=dau      ✘ chỉ nằm ở máy
```

Ba phần thiếu là ba phần bố mẹ hỏi nhiều nhất: con qua kỳ sát hạch nào, vững chủ đề
nào, đấu tới vòng mấy. Đổi máy là mất sạch, và cô giáo thì không bao giờ thấy.

Để **riêng** chứ không nhét vào `progress/{uid}/micros`: hàm nền `onMicroDone` chạy trên
mọi tài liệu của thư mục ấy và đọc thẳng `after.microId` — thả một hình dạng khác vào là
hàm đêm ném lỗi, còn `microsPassed` thì đếm phồng lên.

**Và app nay KÉO SỔ VỀ khi đăng nhập.** Trước đây chỉ đẩy lên, không bao giờ kéo về: con
học ở máy tính bảng rồi mở máy của bố mẹ là thấy quyển trắng tinh. `gopTienDo` gộp theo
mốc thời gian của **từng mục**, không lấy nguyên một bên — hai máy học dở hai bài khác
nhau thì cả hai đều phải còn.

---

## BA VIỆC ĐÃ ĐẨY — khác mọi lần trước

| # | việc | vì sao |
|---|---|---|
| 1 | `hosting` ✅ | như thường lệ |
| 2 | **`firestore rules`** ✅ | **BẮT BUỘC.** Thư mục `hocBa/{uid}/muc` là mới; luật mặc định là CẤM, nên không đẩy rules thì mọi lượt ghi kỳ sát hạch · bậc chủ đề · vòng đấu đều bị từ chối **trong im lặng** — sổ tại máy vẫn đúng nên không ai thấy gì |
| 3 | `functions` ✅ | `learnerRows` nay tính thêm `minutes` và `theoSach`. Không đẩy thì bảng cô giáo vẫn chạy, chỉ là cột "phút" và "trình độ" để trống — giao diện đã lo sẵn trường hợp thiếu, không hiện "0 phút" |

```
cd web && npx firebase deploy --only hosting,firestore:rules
cd web && npx firebase deploy --only functions      # nếu đẩy cả hàm nền
```

---

## MAI VÀO VIỆC TỪ ĐÂU

1. ~~Đẩy rules + hosting~~ — **XONG.** Cả ba phần đã lên mạng.
2. Ba hướng cũ vẫn còn nguyên trong `docs/tiep_theo_dinh_dang.md`: gợi ý cho Mùa giải
   (0/314 câu), 21 dạng chỉ một bậc, 6 micro nằm ở hai dạng.
3. `progress/{uid}/micros` không lưu `attempts`, nên bảng cô giáo đọc về luôn thấy
   "1 lần" cho mọi bài. Muốn đúng thì thêm trường ấy vào `buildProgressDoc`.

---

Xem thêm `docs/tiep_theo_dinh_dang.md` (định dạng nội dung · năm hướng đi tiếp),
`docs/tiep_theo_chu_de.md` (học theo chủ đề) và `docs/CHUAN_DUA_SACH_VAO_APP.md`.
