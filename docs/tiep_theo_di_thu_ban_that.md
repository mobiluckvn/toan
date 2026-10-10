# Điểm dừng — ĐI THỬ BẢN THẬT MỘT BUỔI TRỌN VẸN, VÀ BA LỖI CHẶN · 10-10-2026

Ghi ngày 10-10-2026. **Đọc trang này trước khi động vào phòng luyện nói, phần chấm
viết, hay trước khi tin rằng một màn nào đó "đã chạy vì cổng xanh".**

Bản bàn giao trước ở `docs/tiep_theo_xuong_va_deploy.md` (09-10) — vẫn đúng về xưởng
nội dung và mười hai việc V1→V12. **Mục 1 "VIỆC KẾ TIẾP" của nó — đi thử bằng tay
một buổi trọn vẹn trên bản thật — nay đã làm**, và đó là nội dung trang này.

Buổi đi thử tìm ra **ba lỗi CHẶN NGƯỜI DÙNG** đang sống trên bản thật. Cả ba đều
có cổng xanh, build xanh và deploy xanh phía trên. Đó mới là phần đáng đọc.

---

## 1 · Trạng thái kho — ⚠ ĐỌC TRƯỚC

- Nhánh **`phu-dao-va-bo-do-kb2-kb3`**, HEAD `59b45b1a`, **đã push**, cây sạch.
- Hai commit mới: `31e45799` (lỗi ① và ②) · `59b45b1a` (lỗi ③).
- `main` **vẫn đứng ở `555201f3`** — chưa merge, và bản thật vẫn chạy mã của NHÁNH.
- `npm run build` xanh · **103 tệp cổng · 0 tệp đỏ** (+8 phép kiểm mới).
- **Đã deploy hai lượt:** `hosting + functions:chamViet`, rồi `hosting`.

> ⚠ Vẫn giữ nguyên hai cảnh báo của bản trước: chạy `npm run build` TRƯỚC `npm test`,
> và soi cổng bằng **mã thoát TỪNG TỆP** chứ đừng cộng mấy dòng `N PASS`.

---

## 2 · BA LỖI CHẶN, VÀ VÌ SAO KHÔNG CÁI NÀO BỊ BẮT

### ① Phòng luyện nói VỠ TRẮNG MÀN HÌNH — cả năm quyển Tiếng Anh

Bấm tab **Phòng luyện nói** là trang trắng trơn, không một chữ. Console:

```
ReferenceError: Cannot access 'ae' before initialization
```

`PhongNoi.jsx` dòng 219 dùng `keHoach`, mà `useState` khai nó mãi dòng 283 — `const`
nằm trong vùng chết cho tới dòng khai báo, nên **mọi** lần dựng màn đều ném, React
gỡ cây, cả app trắng. Do chính commit V7 `23614a98` (09-10) đưa vào rồi deploy ngay
hôm ấy.

**Kéo theo:** việc **V3** (trí nhớ của cô giáo máy) và **V10** (phân xử lượt nói mơ
hồ) **chưa từng chạy được một lần nào trên bản thật** — chúng chỉ sống trong màn này.

**Vá:** dời khối `tinhBuoi`/`loiKet` xuống sau chỗ khai `keHoach`.

### ② Lời chấm bài viết KHÔNG BAO GIỜ BÁO LỖI CHO BÉ

Hai bài thử, hai lần y nhau:

| Bé viết | Máy trả |
|---|---|
| *I can see two friend… The girl have a red bag.* | **6/10** · "Cô không tìm thấy lỗi nào trong bài của con." |
| *This is Mary. She eight years old.* | **8/10** · "Cô không tìm thấy lỗi nào trong bài của con." |

Điểm dưới 10 mà bảo không có lỗi — hai vế tự chọi nhau, và bé đọc được cả hai.

**Gốc KHÔNG ở mô hình.** Dựng lại trọn chuỗi bằng Groq thật với đúng gói máy con
gửi: mắt xích 1 **tìm ra** lỗi, mắt xích 2 **viết được** câu sửa đúng. Nhưng hàng rào
vốn từ bác câu sửa vì một chữ ngoài bảng:

```
VIET:TA3.U02 | She is eight years old.                  → chữ lạ: ["she"]   (bảng chỉ khai "She's")
VIET:TA3.U01 | I can see two friends at the school gate. → chữ lạ: ["friends","at","the","school","gate"]
VIET:TA3.U01 | The girl has a red bag.                   → chữ lạ: ["the","girl","has","a","red"]
```

Ở Unit 1 nó bác cả `the · at · school · gate` — **bốn chữ chính bé vừa gõ ra**. Vòng
xin lại ép mô hình bỏ trống câu sửa, rồi máy con lọc mục rỗng ấy đi **trong im lặng**
(không đếm vào `boQua`, nên màn hình cũng không nói là có giấu).

**Vá bốn chỗ:**

| Chỗ | Sửa gì |
|---|---|
| `chuLa` (cả hai bản chép) | nhận thêm `beViet` — chữ bé vừa viết thì không phải chữ bé chưa học |
| `gocBienHinh` (mới) | đuôi đều `-s -es -ed -ing -'s`, **chỉ tha khi GỐC có trong vốn** — `has` không lọt nhờ `ha` |
| `soiLoiCham` | `sua` rỗng nay đếm vào `boQua` — giấu thì phải nói là có giấu |
| `loiDanSua` luật 3 | nói ra ba thứ chữ được phép, nếu không mô hình tự kiểm duyệt rồi trả `loi: []` |

> ⚠ **BẢN VÁ ĐẦU CỦA TÔI LÀM HỎNG THÊM MỘT CHỖ.** Viết luật 3 thành **bảy dòng** thì
> mắt xích 2 **cạn token** ngay lượt gọi đầu — Groq trả `400 json_validate_failed`,
> và bé sẽ thấy "chưa chấm được". Lời dặn dài thì `gpt-oss-120b` nghĩ lâu hơn, mà
> phần nghĩ ăn chung trần với phần viết — đúng cái bẫy chú thích ở `goiMot` đã cảnh
> báo. Chữa: rút còn **ba dòng** + `TOKEN_SUA` 700 → 900 (tổng trần 1700 → 1800, cổng
> ghi lý do). **Nới luật thì nới bằng chữ ngắn.**

### ③ Mỗi lượt nói ném `ReferenceError` — cô không có tiếng, buổi không được lưu

Lỗi này **nấp sau lỗi ①**: phải vá xong màn trắng mới thấy nó.

Triệu chứng: lượt gọi `luyenNoi` trả **HTTP 200**, câu của cô hiện ra đủ, mà ngay
dưới là dòng vàng *"Cô giáo máy chưa trả lời được. Con thử lại nhé."*

Gốc: khối ghi lượt nói vào engine BKT (thêm 23-08, `17a9d1b7`) đặt trong `guiLuot`,
nơi **không có `r` lẫn `kq`** — hai biến ấy sinh ra trong `noi`. Biến chưa khai, ở
module (strict mode) là `ReferenceError` mỗi lượt.

**Ba dòng nằm SAU chỗ ném, nên cả ba chưa từng chạy:**

| Dòng | Hậu quả thật |
|---|---|
| `docLen(tra.en)` · `docDoan(tra.vi)` | **cô KHÔNG đọc thành tiếng câu nào** — cả phòng luyện nói mà không có tiếng |
| `luuBuoi(uid, …)` | buổi nói **không lên `phongNoiTA`** |
| `onLuot?.(…)` | kỹ năng NÓI vẫn **ngoài BKT** — đúng lỗ thủng mà việc 23-08 định vá |

**Vá:** đưa khối về `noi`; vân tay lời dặn nay đi theo **lượt của cô** (`luotCoCuoi`),
vì tới lúc bé đáp thì `tra` đã ngoài tầm với.

### ⚠ VÌ SAO KHÔNG CỔNG NÀO BẮT ĐƯỢC — và cách soi nhanh họ lỗi này

Cả ① và ③ là **mã tham chiếu một biến không có trong phạm vi**. 103 tệp cổng đều là
**logic thuần** chạy bằng `node`; không tệp nào `render()` một component. `npm run
build` thì không soi thứ tự dùng biến trong thân hàm. Và `web/` **không có ESLint**
(không `.eslintrc*` lẫn `eslint.config.*`), nên `no-use-before-define` không ai gác.

**Cách soi nhanh cả kho:** minifier **KHÔNG đổi tên biến tự do**, nên biến chưa khai
nằm **nguyên văn** trong bundle đã deploy:

```bash
grep -o "kq&&kq\.diem[^;]\{0,60\}" web/dist/assets/index-*.js   # bắt được đúng lỗi ③
```

Và một phép soi "dùng trước dòng khai" trong CÙNG một component (đã chạy một lượt
10-10, chỉ `PhongNoi` dính) nằm ở mục 6 dưới.

---

## 3 · ĐÃ SOI TẬN MẮT SAU KHI DEPLOY — không chỉ tin lệnh deploy

Cả ba bản vá đều kiểm lại **trên `ky-su-nhi.web.app`**, không phải trên `dist` tại máy:

| Kiểm gì | Bằng chứng |
|---|---|
| Phòng nói dựng ra | tranh · câu của cô · thẻ từ · nút micro; console sạch |
| Dòng lỗi giả | biến mất |
| Cô đọc thành tiếng, lượt chào **tự động** | móc `speechSynthesis.speak` bắt được: `What can you see?` (en-GB · 0.9) rồi `Con nhìn bức tranh rồi tả…` (vi-VN) |
| Buổi lên máy chủ | `firestore…/Write/channel` → 200 |
| Lượt nói vào BKT | sổ tại máy có `phongNoi: {dung: 4, tong: 5}` |
| **V3 · trí nhớ của cô** | Góc bố mẹ hiện "CÔ GIÁO MÁY ĐANG NHỚ GÌ VỀ CON" + 3 câu + nút xoá |
| **V10 · phân xử** | log `phanxunoi` 02:53:36 · `auth: VALID` |
| **Chấm viết sau vá** | `I have two friend.` → `I have two friends.` · "Sau "two" phải dùng danh từ số nhiều" |

Buổi nói đi trọn **5 bước kịch bản** tới màn kết *"Con nói được rồi! · Con nói đúng 3
câu liền."*

---

## 4 · CÁCH BƠM CHỮ VÀO BỘ NHẬN DẠNG GIỌNG NÓI — để đi thử mà không cần nói

Phòng nói và phần luyện từ đòi **giọng thật**, nên trước nay không tự động đi thử
được. Cách này cho app đi **đúng đường của nó**, chỉ bước "nghe tiếng" là giả.

```js
// Dán vào console TRÊN TRANG ĐANG MỞ (đừng tải lại sau khi dán).
// `nghenoi.js` giữ `const SR = window.webkitSpeechRecognition` từ lúc nạp module,
// nên KHÔNG thay được `window.webkitSpeechRecognition` — phải vá PROTOTYPE, vì
// `new SR()` vẫn lấy prototype ấy.
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const batGoc = SR.prototype.start;
SR.prototype.start = function () {
  const chu = window.__beNoi;
  if (!chu) return batGoc.call(this);          // không bơm thì nghe thật như cũ
  const pa = Array.isArray(chu) ? chu : [chu];
  setTimeout(() => {
    const mot = { isFinal: true, length: pa.length };
    pa.forEach((t, i) => { mot[i] = { transcript: t, confidence: 0.92 }; });
    this.onresult && this.onresult({ resultIndex: 0, results: { length: 1, 0: mot } });
    this.onend && this.onend();
  }, 400);
};
SR.prototype.stop = SR.prototype.abort = function () {};

window.__beNoi = 'I can see two bikes';   // rồi bấm nút micro
```

⚠ **Nó KHÔNG thử bước Chrome đổi tiếng thành chữ** — chỉ thử mọi thứ phía sau. Xong
thì `delete window.__beNoi` và **tải lại trang** (hai hàm `stop`/`abort` đã bị thay).

**Mẹo tìm ca rơi đúng vùng mơ hồ [5,7] để kích V10:** đừng đoán, chạy chính bộ chấm —
`chamTot(chamTu, dich, [nghe], { doiThu })` rồi lọc bằng `moHoCanBoPhieu`. Đo ra ba ca
cho ta3 B01: `hi`←"yi" (5, đối thủ `i`), **`how`←"yow" (7, đối thủ `you`)**, `Ben`←"Be"
(7, đối thủ `bye`).

---

## 5 · LỖI NỘI DUNG MỚI: 43% BƯỚC HỎI BÀI TẢ TRANH KHÔNG TRẢ LỜI ĐÚNG ĐƯỢC

Chưa vá — để bác chốt hướng.

Bé đáp **đúng** *"They are at the school gate"* cho câu *"Where are they?"* thì
**không được điểm nào**, rồi cô "sửa" bằng *"This is Ben."* kèm lời dặn *"Cô đang hỏi
câu hỏi về vị trí. Con trả lời lại cho đúng nhé."* — câu sửa ấy không phải câu trả lời
vị trí. Ngược lại, nói *"This is Ben"* (chẳng liên quan câu hỏi) lại được **⭐⭐⭐**.

Gốc ở `lib/phongnoi.js:720`:

```js
if (buoc.loai === 'goiY') return buoc.dapMau ? [buoc.dapMau] : [...moTa];
```

Thiếu `dapMau` thì "câu được tính là đúng" rơi về **cả năm câu mô tả tranh**, không
câu nào trả lời câu hỏi. Đếm thật:

```
bước goiY của bài TẢ TRANH: 127 · thiếu dapMau: 55  (43%)
   ta3 · B00 "Where are you?"      ta3 · B04 "Touch your face!"
   ta3 · B01 "Where are they?"     ta3 · B05 "What's your hobby?"
   ta3 · B02 "What's this?"        ta3 · B08 "What do you have?"   …
```

Nặng hơn: vốn từ unit B01 **không có** `they · are · school · gate`, nên **không câu
nào** vừa trả lời đúng vừa nằm trong vốn. Cùng họ với
`[[cau-hoi-va-doan-van-lay-tu-hai-mau-cau]]`.

**Hai đường chữa, chọn một:**
1. Bổ sung `dapMau` cho 55 bước — việc nội dung, bước cuối là mắt người.
2. Sửa mã: bước thiếu `dapMau` thì **không chấm** lượt ấy, thay vì chấm theo mấy câu
   chẳng liên quan — một chỗ sửa, nhưng mất phần chấm của 43% số bước.

---

## 6 · MẤY CHỖ NHỎ HƠN, CŨNG CHỈ LỘ KHI MỞ MẮT RA NHÌN

| | Chỗ hỏng | Ghi chú |
|---|---|---|
| 1 | **Thi thử ăn gian được**: sai 3 lần thì màn **hiện "Đáp án: four"** mà vẫn để "Thử lại" và tính là đúng | Lấy được huy hiệu **8/10** dù không nghe được clip nào. Đúng lỗi thứ bảy của `[[kiem-bang-mat-truoc-khi-deploy]]`, nay sang Tiếng Anh |
| 2 | Cùng một kỳ thi trộn **hai luật**: câu đúng/sai một phát ăn ngay và không báo đúng sai; câu trắc nghiệm thử vô hạn | Điểm phụ thuộc câu rơi vào dạng nào |
| 3 | **Sổ bố mẹ tự mâu thuẫn**: "Con chưa học bài nào — chưa có gì để tổng kết" + "0 BÀI ĐÃ ĐẠT" nằm ngay trên "Tiếng Anh lớp 3 · master 1/5 chương · Cần cố gắng: Bài 0 · Bài 1" | |
| 4 | Dòng cuối sổ bố mẹ khuyên "Đăng nhập rồi thì sổ có thêm…" **trong khi đang đăng nhập** | |
| 5 | "DẠNG CÂU CON LÀM TỐT NHẤT: chọn đáp án — **đúng 14%**" | Gọi 14% là "làm tốt nhất" vì nó là dạng DUY NHẤT đủ mẫu |
| 6 | Xác nhận điểm xong thì mục biến mất, **không chỗ nào thấy lại** "đã xác nhận 9/10" | |
| 7 | **Không có error boundary** — một lỗi là trắng cả app, bé không thấy chữ nào | Chính nó làm lỗi ① thành màn trắng thay vì một dòng báo |
| 8 | Lời gợi ý của máy chấm xưng **"bạn"** ("Tiếp tục luyện tập, bạn sẽ viết tốt hơn!") trong khi cả app xưng "con" | Lời dặn chấm viết chưa có `XUNG_HO_CAM` như phòng nói |

**Phép soi "dùng biến trước dòng khai" trong cùng một component** (đã chạy 10-10, chỉ
`PhongNoi` dính thật):

```bash
# cắt file theo ranh giới `function Ten(`, trong mỗi khối đối chiếu dòng khai
# useState/useRef/useMemo với các câu lệnh thân hàm (thụt đúng 2 dấu cách) ở TRÊN nó
```

---

## 6b · V9 ĐÃ THỬ XONG — 10-10-2026, bổ sung sau

Làm ngay trong phiên ấy, bằng cách bơm chữ ở mục 4 để qua cửa "nói đủ 13 từ".

**Đường đi:** Từ mới (13 từ, mỗi từ nghe + nói) → Mẫu câu (4 mẫu, mỗi mẫu xem video +
nói) → **Luyện tập mở**. Chặng Mẫu câu **bắt buộc xem hết video** (`mo: xemDu &&
(noiDu || micHong)`, không có đường "nghe đủ" như chặng Từ mới); tua bằng
`v.currentTime = v.duration - 0.25; v.play()` rồi đợi sự kiện `ended`.

**Kích phụ đạo:** sai **3 lần liên tiếp** trên cùng một nút (`SAI_LIEN_TIEP_MAC = 3`).
⚠ Lời mời **không hiện ngay lúc sai** — `choPhuDao` chỉ được bày ra khi bé **LÀM XONG
câu ấy** (trả lời đúng, hoặc "Để câu này lại sau"). Cứ bấm sai mãi thì không bao giờ
thấy; tôi mất mấy lượt mới nhận ra.

**Kết quả — chạy đúng, trọn vòng:**

| Chặng | Màn hình |
|---|---|
| Mời | 🔎 "Mình gỡ chỗ này cùng nhau nhé · Cô thấy con chưa chắc phần **how — như thế nào**. Làm 3 câu ngắn…" — chẩn đoán **đúng** nút tôi cố tình làm hỏng |
| Làm | "rối · câu 1/3 · how — như thế nào", ba câu, có cả dạng gõ lại |
| Xong | 👍 "Xong rồi, mình quay lại bài nhé · Con làm đúng 3/3 câu" → quay về Luyện tập |

**`sinhCauPhuDao` đã được gọi LẦN ĐẦU trên bản thật** — log `sinhcauphudao`
03:26:26 · `auth: VALID`. Tức hai vòng kho tĩnh không đủ câu cho nút ấy và đường mô
hình đã cắm đúng.

**Còn một mắt chưa nhìn tận nơi: `choDuyetTA` có bao nhiêu dòng.** Luật cho bé GHI mà
không cho ĐỌC, nên cả máy con lẫn tôi đều không soi được — phải `soi_ban_ghi_tienganh.mjs`.

**Đo riêng bộ sinh bằng mô hình thật** (hai nút, mỗi nút 3 câu) để biết hàng đợi sẽ
nhận được gì:

- Lượt 1: **3/3 bị `soiCauAI` bác** — "gợi ý lộ thẳng đáp án" (gợi ý liệt kê đúng mấy
  chữ của đáp án: *"Câu hỏi dùng từ how, you, fine"* ↔ đáp án *"how you fine"*).
- Lượt 2: **6/6 ĐẠT** — tức tỷ lệ qua cửa dao động mạnh giữa các lượt.
- ⚠ **Mấy câu ĐẠT lại đúng loại cần người đọc:** *"Nói lời chào"* → đáp án `hello`
  trong khi `hi` cũng là lời chào; *"Chào một bạn"* → `hello Ben` trong khi
  `hello Lucy` đúng y hệt. **Hai đáp án đúng** — luật thứ bảy mà code không kiểm được.
- Và vài câu là tiếng Anh vỡ: *"how you fine"*, *"how Ben you fine"* — đúng điều V12
  đã thấy: túi vốn một unit không có từ chức năng thì mô hình xếp chữ thành câu không
  ai nói.

**Rút ra:** đường mô hình **chạy**, tầng hậu kiểm bằng code **có tác dụng thật**, và
hàng đợi duyệt **là chỗ đúng** cho phần còn lại — nhưng chừng nào `tools/nhap_cau_duyet.py`
chưa có thì hàng đợi chỉ đầy lên, và **không câu nào do máy soạn được vào kho tĩnh**.
Đó là việc kế tiếp số 2 dưới đây.

**Một quan sát nhỏ:** lúc 92 lượt trong hàng đợi gửi dồn một lúc, console có ba dòng
`WebChannelConnection RPC 'Write' stream transport errored`. SDK tự thử lại, hàng đợi
rút về 0, các lượt sau không lặp lại. Ghi ra đây để lần sau thấy thì biết là cái gì.

## 7 · VIỆC KẾ TIẾP, theo thứ tự

1. ~~Thử V9~~ — **XONG, xem mục 6b.** Phụ đạo chạy trọn vòng, `sinhCauPhuDao` đã
   gọi được lần đầu. Còn lại: mở `choDuyetTA` ra đếm (cần khoá quản trị).
2. **Chốt hướng cho 55 bước thiếu `dapMau`** (mục 5).
3. **Merge nhánh về `main`** — `main` vẫn ở `555201f3`, không còn là thứ đang chạy.
4. **Bật ESLint với `no-use-before-define`, hoặc một cổng dựng mỗi màn đúng một lần.**
   Hai lỗi `ReferenceError` lên tới bản thật chỉ vì chỗ này trống.
5. Mở tài liệu Firestore ra nhìn: `GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
   node tools/soi_ban_ghi_tienganh.mjs`. Buổi đi thử chỉ chứng minh được điều PHỦ ĐỊNH
   (không bị từ chối), chưa chứng minh **ghi đúng nội dung gì** — đúng cái bẫy tệp ấy
   tự cảnh báo ở đầu trang.
6. Mấy chỗ nhỏ ở mục 6, theo thứ tự bác thấy cần.
7. Nợ cũ từ bản 09-10 — ⚠ `tools/nhap_cau_duyet.py` nay **gấp hơn**: mục 6b cho thấy
   hàng đợi đã thật sự có đường vào, mà vẫn chưa có đường ra ·
   xưởng chưa qua đợt dùng thật · `GROQ_MODEL_PHU` · `congHuong` chưa ai gọi · 19 nút
   gốc rễ không có bài nào dạy · bộ nối ΔC · Chương 1 và Chương 4 luận văn.

Xem thêm `[[cong-khong-dung-man-nao]]`, `[[kiem-bang-mat-truoc-khi-deploy]]`,
`[[di-thu-ban-chay-bat-duoc-cai-cong-khong-bat]]`, `[[loi-dan-tu-choi-nhau]]`,
`[[0-fail-tren-dia-khong-phai-tren-cay-da-push]]`.
