# Soát MÔN TOÁN end-to-end sau khi tách hai môn

Lập 2026-08-11, ngay sau `05f81e8` (tách frontend về ba vùng).

> **ĐÃ SOÁT XONG A–H 2026-08-11.** Kể cả mục H (đăng nhập · bảng xếp hạng · bảng cô
> giáo) — nay đi thử được nhờ **bộ giả lập**, xem "Cách đi thử phần đăng nhập" bên
> dưới. Bắt được **sáu lỗi câm**, đã sửa hết, đã có phép kiểm gác lại. Xem "Đã tìm
> thấy gì" ở cuối trang.

**Việc này chắn đường mọi việc khác.** Đợt tách vừa rồi động vào 55 tệp, xẻ đôi ba
tệp lõi và viết lại đường import của cả kho. Cổng 1 096 phép đã xanh và cháu đã đi
thử sáu màn — nhưng cổng KHÔNG bắt được loại lỗi chỉ lộ khi mở mắt xem, và đợt này
đã dính đúng một cái như thế (`THU_MUC_CUA is not defined`, cả bốn quyển câm).

Nên: **đi hết danh sách dưới đây trên `npm run dev` trước khi làm bất cứ gì tiếp theo.**

```bash
cd web && npm test && npm run dev     # http://localhost:5173
```

---

## A · Kệ sách

- [ ] Thứ tự đúng: lớp 2 → 3 → 4 → 5 → Mùa giải
- [ ] Thẻ **HỌC TIẾP** chỉ đúng quyển động vào gần nhất
- [ ] Vạch tiến độ từng quyển đúng số bài (kệ sách nay **hỏi môn**, không tự đếm — đây
      là chỗ mới thay, soi kỹ)
- [ ] Cửa phụ **🗺️ Học theo chủ đề** mở được (nay do môn tự khai, không phải kệ sách gọi)
- [ ] Cửa **🏆 Bảng xếp hạng** và **📖 Sổ bố mẹ**
- [ ] Mục "Sắp có" và "Ôn thi" vẫn hiện

## B · Trang chính của quyển — làm ĐỦ CẢ BỐN QUYỂN

- [ ] Lớp 2 · Lớp 3 · Lớp 4 · Lớp 5 — mở được, đúng tên, đúng số chương
- [ ] Thẻ **VIỆC CỦA CON**: chưa học → "Bắt đầu từ đây"; đang dở → "Học tiếp / Từ đầu"
- [ ] Mỗi chương có **dòng đề xuất riêng**; chương chưa học chỉ vào **bài đầu chương ấy**
- [ ] Bảng sưu tập sao đúng số chương (lớp 4 = 11, lớp 5 = 14)
- [ ] Kỳ ôn tập của từng chương; **ba cửa ải** ở lớp 2·3 (lớp 3 phải ghi "làm hết là qua")
- [ ] Lớp 5: chế độ học (theo chương trình / tự chọn) và lời giải thích "vì sao khoá"
- [ ] Lớp 5: cửa **🏆 Mùa giải** ở cuối trang
- [ ] Nút **⌂ Kệ sách** trên mọi trang

## C · Phòng học

- [ ] Mở một bài lớp 2 và một bài lớp 5 — hai nhịp đọc khác nhau (chữ to / dồn khối)
- [ ] Đủ năm chặng: mở bài → giảng → bài mẫu → luyện tập → sát hạch
- [ ] Sai lần 1 hiện gợi ý tầng 1, sai lần 2 hiện thêm tầng 2; **hai câu liền nhau gợi ý
      phải khác nhau**
- [ ] Công thức hiện thành phân số xếp dọc, **không lộ mã LaTeX**
- [ ] Thoát giữa chừng rồi vào lại → về **đúng chỗ dở**
- [ ] Màn kết: đường lùi về quyển dưới, ô GỬI BỐ MẸ

## D · Kỳ sát hạch

- [ ] Mở kỳ sát hạch chương 1 của lớp 5 và của lớp 2
- [ ] Máy chấm câu có đáp án; đề B sau khi trượt; bảng tự soi mở đúng bài
- [ ] Qua kỳ → huy hiệu sáng **đúng quyển ấy**, không lây sang quyển khác

## E · Học theo chủ đề

- [ ] Ba tầng: 5 mảng → chủ đề → thang của một dạng
- [ ] Nút **⌂ Kệ sách** có ở CẢ BA tầng
- [ ] Thang hiện đủ bậc lớp, tên quyển đúng ở từng bậc
- [ ] Luyện một chủ đề: đạt thì tiến bậc, kém thì lùi và **mở bài học** của bậc dưới
- [ ] "Đấu thử ở Mùa giải" → vào đúng vòng đấu, thoát ra về **đúng màn chủ đề**

## F · Mùa giải (Quyển 2)

- [ ] Vòng đấu mở theo chương đã xong của Quyển 1; dòng "còn N bài nữa" đúng số
- [ ] Bốn màn: làm đề (có đồng hồ) → chữa đề → phiên tòa → nhật ký
- [ ] **314/314 câu máy chấm**: ô số, trắc nghiệm, câu nhiều ô đều nhận
- [ ] Lời chữa hiện đúng, **không lộ mã LaTeX**
- [ ] Trại huấn luyện · Hồ sơ Cáo Đề · Thẻ chiến thuật
- [ ] Hai lối ra: "← Toán lớp 5" và "⌂ Kệ sách"

## G · Sổ bố mẹ

- [ ] Trình độ hiện tại đúng quyển, đúng số
- [ ] Tab **Xem theo lớp**: bốn quyển, từng chương có nhãn master / xong bài / đang học
- [ ] Tab **Xem theo chủ đề**: 5 mảng, đếm vững / đang học / cần cố gắng / chưa học
- [ ] ⚠ Nút bấm vào một bài để mở lại **đang tạm để trống** — đường vào phòng học chưa
      có trong giao ước, đã ghi vào Đợt 2. Xác nhận không có nút chết nào hiện ra.

## Cách đi thử phần ĐĂNG NHẬP — không cần hộp thư, không đụng dữ liệu thật

`.env.local` trỏ vào dự án THẬT, nên `npm run dev` xưa nay nói chuyện thẳng với
Firebase thật. Thêm nữa, `App.jsx` **tắt hẳn màn đăng nhập khi chạy local** — tiện,
nhưng chính vì thế bốn màn của mục H chưa bao giờ được ai đi thử.

Nay bật bộ giả lập là cả ba đường (đăng nhập · cơ sở dữ liệu · hàm máy chủ) quay về
máy mình, và màn đăng nhập hiện lại:

```bash
# cửa sổ 1 — cần Java (brew install openjdk)
cd web && PATH="/usr/local/opt/openjdk/bin:$PATH" \
  firebase emulators:start --only auth,firestore,functions

# cửa sổ 2
cd web && VITE_FB_EMULATOR=1 npm run dev
```

**Lấy mã OTP ở đâu:** không cần hộp thư. Chạy trên giả lập thì `sendMail` không gửi
mail mà in thẳng mã ra log của bộ giả lập:

```
[OTP] BỘ GIẢ LẬP — không gửi mail. Mã cho be.thu@example.test: 985834 là mã đăng nhập…
```

**Lập tài khoản giáo viên:** đăng nhập bằng một email bất kỳ (thành học sinh), sửa
`role` thành `teacher` trong Firestore giả lập (`http://127.0.0.1:4000/firestore`),
rồi đăng nhập lại — vai trò nằm trong token nên phải xin mã lần nữa.

⚠ Cờ `VITE_FB_EMULATOR` **buộc kèm** `import.meta.env.DEV`, nên không thể lọt vào bản
đưa lên mạng. `test/gia_lap.test.mjs` soi cả mã nguồn lẫn `dist/` để gác điều đó.

## H · Cần ĐĂNG NHẬP — nay đi thử được bằng bộ giả lập

- [ ] Đăng nhập bằng OTP; lần đầu hỏi tên + lớp (**2 → 12**)
- [ ] Học một bài rồi mở máy khác / xoá localStorage → đăng nhập lại → **kéo sổ về đủ**
- [ ] Bảng xếp hạng: bấm "↻ Cập nhật ngay", đổi biệt danh, chọn một bạn để đuổi
- [ ] Tài khoản giáo viên: bảng theo dõi, bấm vào một em → **bốn tab** (tổng quan · theo
      lớp · theo chủ đề · nhật ký)

---

## Nếu có chỗ nào vỡ

Ghi lại **màn nào · bấm gì · thấy gì**, rồi sửa TRƯỚC khi làm Đợt 2. Sửa xong nhớ hỏi:
*phép kiểm nào lẽ ra phải bắt được cái này?* — rồi viết nó, như đã làm với
`ranh_gioi.test.mjs`.

Xem thêm `docs/tach_hai_mon.md` (kiến trúc và Đợt 2).

---

# ĐÃ TÌM THẤY GÌ · 2026-08-11

Cả hai lỗi dưới đây **không làm màn hình vỡ**. Cổng 1 096 phép kiểm đi qua sạch,
sáu màn đi thử trước đó cũng không lộ gì. Đúng như sổ đã cảnh báo: loại lỗi này chỉ
ra mặt khi mở mắt xem — và một trong hai cái còn phải mở console mới thấy.

## Lỗi 1 · Vòng lặp không đáy trong phòng học ⚠ nặng nhất

**Màn nào · bấm gì · thấy gì:** Vào phòng học bất kỳ bài nào. Màn hình trông hoàn
toàn bình thường. Mở console: **3 180 dòng `Maximum update depth exceeded`** trong
bốn phút, đến từ `LessonPlayer.jsx:52`. Máy quay hết công suất, localStorage bị ghi
liên tục suốt thời gian con ngồi học.

**Vì sao:** `App.jsx` gộp sổ tiến độ bằng `{ ...t, [ma]: f(t[ma]) }` — dựng khối MỚI
kể cả khi môn báo "chẳng có gì đổi". React thấy sổ đổi → vẽ lại vỏ → hàm `datTienDo`
truyền xuống môn cũng mới → effect trong phòng học canh đúng hàm ấy chạy lại → lại
gọi vào vỏ → lại vẽ. `saveSpot` có chốt chặn reference đúng rồi, nhưng vỏ vứt nó đi.

**Sửa:** tách luật gộp ra `src/chung/lib/soTienDo.js` — `gopTienDoMon` trả về NGUYÊN
khối cũ khi môn không đổi gì.

## Lỗi 2 · Thẻ HỌC TIẾP chỉ sang quyển cũ

**Màn nào · bấm gì · thấy gì:** Học dở một bài lớp 2 rồi ra kệ sách. Thẻ HỌC TIẾP
vẫn chỉ tay sang **lớp 5** — quyển con học xong từ lâu, không phải quyển vừa động vào.

**Vì sao — hai tầng:**
1. `saveSpot` nhớ chỗ đang học dở nhưng **không đóng dấu `at`**, mà kệ sách và sổ bố
   mẹ đều xếp "quyển động vào gần nhất" theo đúng mốc ấy.
2. Núp dưới đó là `Date.parse(m.at || 0) || 0`. Bài chưa có dấu thì `0` bị ép thành
   chuỗi `"0"` và đọc ra **NĂM 2000** — một con số thật, khác 0, nên `|| 0` phía sau
   vô tác dụng. Người viết tưởng đó là đáy; nó không phải.

**Sửa:** `saveSpot` đóng dấu `at` ngay mỗi bước; `mocCua()` trong `mon/toan/index.js`
thay cho hai chỗ viết `Date.parse(m.at || 0)`.

## Lỗi 3 · Bài học thử KHÔNG BAO GIỜ lên được máy chủ ⚠ nặng

**Màn nào · bấm gì · thấy gì:** Đăng nhập rồi học vài bài. Máy chủ **trống trơn** —
không một dòng nhật ký. Màn hình không báo gì.

**Vì sao:** con học thử trước khi đăng nhập thì mọi bản ghi mang mã tạm `'local'`.
Đăng nhập xong phải SANG TÊN chúng — hàm `reassignQueue` đã có sẵn, có phép kiểm
xanh, chú thích mô tả đúng y vấn đề này… **nhưng chưa bao giờ được gọi ở đâu cả.**
Mà cả hàng đợi đi chung MỘT lô ghi, nên một bản ghi `'local'` kẹt lại là **cả lô bị
luật bảo mật từ chối, mãi mãi** — bài học SAU khi đăng nhập cũng không lên nổi.

Đúng lời hứa in trên màn đăng nhập bị vỡ: *"Đăng nhập lúc nào thì toàn bộ kết quả
được đẩy lên, không mất gì."*

**Sửa:** thêm mục giao ước `dangNhapXong(uid)` cho môn; `App.jsx` gọi nó ngay khi
đăng nhập, trước khi kéo sổ về. Sau khi sửa: 16 bản ghi kẹt thoát hết trong một lượt.

## Lỗi 4 · Ba trên bốn tab của bảng CÔ GIÁO vỡ trắng ⚠ nặng

**Màn nào · bấm gì · thấy gì:** đăng nhập tài khoản giáo viên → bấm vào một em →
bấm tab. **Màn hình trắng bong**, React tháo cả cây. Ba tab một lúc:

| tab | vì sao |
|---|---|
| Theo lớp | đọc `h.chiMuc.bai` — học bạ **chưa bao giờ** nộp `chiMuc` |
| Theo lớp | gọi `trangThaiBai(...)` — hàm của Toán, **chưa hề import** (mà cũng không được phép import: luật ranh giới) |
| Theo chủ đề | hỏi `banDo` — **một cái tên không khai ở đâu cả** |

Cả ba là mã CHẾT CHƯA TỪNG CHẠY: ở `npm run dev` màn đăng nhập bị tắt, nên cửa vào
bảng cô giáo chưa từng mở ra.

**Sửa:** môn chấm sẵn `trangThai` cho từng bài trong học bạ, tầng chung chỉ việc in;
`NHAN_TRANG_THAI_BAI` chuyển về `chung/lib/nhanHocBa.js` đúng chỗ của nhãn chung;
`banDo` thay bằng chính `cd` (học bạ chỉ nộp `chuDe` khi nạp được bản đồ).

## Lỗi 5 · Cô giáo mới không có cách nào dựng bảng lần đầu

Bảng chưa dựng lần nào thì màn hình bảo *"chạy tay hàm `nightlyTeacherBoard` trong
Firebase Console"* — mà cô giáo không có tài khoản Console. Nút "↻ Cập nhật ngay" thì
chỉ nằm trong nhánh bảng-ĐÃ-có. Vòng gà và trứng, đúng lúc cần nút nhất thì không có.

**Sửa:** đưa nút dựng vào cả màn bảng trống (hàm `refreshTeacherBoard` vốn đã sẵn).

## Lỗi 6 · Bộ giả lập vẫn GỬI MAIL THẬT

Chạy giả lập, bấm "Gửi mã cho tôi" → hàm mất 3,7 giây, không có dòng log mã nào: bộ
giả lập **với tay lên Secret Manager thật** lấy được `SMTP_USER`/`SMTP_PASS` (máy nào
đã `firebase login` là lấy được), nên mỗi lần đi thử là một lá thư thật rời hộp thư
mình. Đặt `functions/.secret.local` cũng không cứu được — nó vẫn hỏi Secret Manager
trước.

**Sửa:** `sendMail` chặn ngay đầu khi `process.env.FUNCTIONS_EMULATOR === 'true'`,
in mã ra log thay vì gửi. Biến ấy chỉ bộ giả lập đặt, chạy thật không bao giờ có.

## Phép kiểm đã viết

| tệp | gác gì | thử hoàn nguyên |
|---|---|---|
| `test/so_tien_do.test.mjs` | vòng lặp không đáy · dấu thời gian chỗ học dở · bẫy `Date.parse(0)` | bắt **6/6** |
| `test/man_co_giao.test.mjs` | học bạ nộp đủ thứ bảng cô giáo đọc · tầng chung không tự gọi hàm của môn | bắt **7/7** |
| `test/gia_lap.test.mjs` | cờ giả lập buộc kèm `DEV` · `dist/` không mang dấu vết giả lập | — |

Cổng nay **38 tệp**, xanh sạch. Bộ chạy tự gom `test/*.test.mjs`.

### ⚠ Một lớp lỗi cổng VẪN chưa bắt được

Hai trong ba lỗi của bảng cô giáo (`banDo`, `trangThaiBai`) là **tên chưa khai** —
đúng thứ ESLint `no-undef` bắt trong một giây, không cần chạy app. Kho **chưa cài
ESLint**. Ba lỗi hôm nay đều nằm trong mã chưa từng chạy, nên chỉ phép kiểm tĩnh mới
thấy. Đề nghị bác cho cài `eslint` với đúng một luật `no-undef` rồi thêm vào `npm test`.

## Không phải lỗi, nhưng bác nên biết

**353 trên 702 câu đề kỳ sát hạch chương không có `answerKey`** — máy không chấm
được, bé phải tự đối chiếu rồi bấm "Mình làm đúng / Mình làm sai". Phân bố rất lệch:

| quyển | câu thiếu đáp án |
|---|---|
| Lớp 2 · Lớp 4 | gần đủ (thiếu lẻ vài câu) |
| **Lớp 5 Quyển 1** | thiếu gần hết |

Đây là khoảng trống **nội dung có sẵn từ trước**, không phải hồi quy của đợt tách
môn — cùng một câu ("Viết số gồm: 3 chục, 5 đơn vị…") khi vào qua màn *luyện chủ đề*
thì có ô nhập và máy chấm bình thường, chỉ tệp `public/content/reviews/DCR_KSN5Q1_*`
là thiếu khoá đáp án. Muốn máy chấm cả kỳ sát hạch lớp 5 thì phải bổ khoá đáp án cho
các tệp ấy — làm như đã làm với `dapan_quyen2.py`.

## Mục H đã đi những gì

- ✅ đăng nhập bằng mã OTP; lần đầu hỏi tên + lớp, đủ **2 → 12**;
- ✅ xoá sạch máy (localStorage + IndexedDB) → đăng nhập lại → **kéo sổ về đủ**;
- ✅ bảng xếp hạng: "↻ Cập nhật ngay" · đổi biệt danh (lưu đúng, hiện sau khi dựng
  lại) · chỉ lộ **biệt danh · lớp · sao**, đúng luật;
- ✅ tài khoản giáo viên: bảng theo dõi dựng được, **bốn tab** đều sống.

## Còn nợ

- **Bảng xếp hạng · "chọn một bạn để đuổi"** — chưa thử được vì bảng giả lập mới có
  đúng một bé. Cần gieo thêm vài học sinh rồi xem lại.
- **Mục D · huy hiệu qua kỳ không lây sang quyển khác** — chưa đi tay hết 12 câu để
  lấy huy hiệu thật; đang dựa vào phép kiểm `test/hocba.test.mjs:168` (đang xanh).
- **Tiến độ HỌC THỬ không được đẩy lên máy chủ.** Bản sửa ở Lỗi 3 mới đưa được *nhật
  ký từng câu* lên. Còn "đã đạt bài nào" thì `submitSession` chỉ ghi khi con học XONG
  một bài **sau** khi đăng nhập — 18 bài học thử trước đó vẫn nằm lại ở máy, đổi máy
  là mất. Lời hứa "không mất gì" mới đúng một nửa. Chưa sửa: nó động vào luồng dữ
  liệu chính, nên để bác quyết.
