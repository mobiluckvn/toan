# Kỹ Sư Nhí — Trang học tập thích ứng cho tiểu học

**MOBILUCK / code247.ai** · **hai môn · chín quyển · 462 bài · 713 video · 2 637 phép kiểm**

| Môn | Quyển | Bài | Lối học |
|---|---|---|---|
| Toán Tư Duy | lớp 2 · 3 · 4 · 5 (+ Mùa giải lớp 5) | 71 · 34 · 95 · 168 | giảng nguyên tắc → xem bài mẫu → tự luyện → sát hạch lấy huy hiệu |
| Tiếng Anh | lớp 1 · 2 · 3 · 4 · 5 | 16 · 16 · 21 · 21 · 20 | từ mới → mẫu câu → luyện nói với cô giáo máy → đọc hiểu → viết ngắn |

Có mức thạo BKT, ôn tập ngắt quãng, phụ đạo theo nút gốc rễ, và sổ theo dõi cho bố mẹ.

> Trang này mở đầu bằng phần **Toán lớp 5** vì đó là quyển dựng trước nhất và được ghi chép
> dày nhất. Phần **Tiếng Anh** — nơi có cô giáo máy và toàn bộ phần gọi mô hình ngôn ngữ —
> nằm ở mục [Tiếng Anh: cô giáo máy](#tiếng-anh-cô-giáo-máy-và-chín-lớp-chốt-chặn) phía dưới.

---

## Chạy trong 3 phút

```bash
cd web
npm install
npm run dev      # http://localhost:5173  — học được ngay, chưa cần Firebase
npm test         # 101 tệp · 2 637 phép kiểm, chạy trên dữ liệu thật của cả chín quyển
npm run test:luat   # luật Firestore — cần bộ giả lập, xem docs/DEPLOY.md
```

⚠ Chạy `npm run build` TRƯỚC `npm test`: một tệp cổng soi chính bản dựng (dấu phiên bản
nội dung), nên chạy sai thứ tự là nó đỏ mà chẳng có gì sai.

⚠ Phần Tiếng Anh gọi mô hình ngôn ngữ qua Cloud Functions. Không có khoá thì phòng luyện
nói và phần chấm bài viết báo lỗi tử tế; **mọi phần còn lại học bình thường**.

Chưa cấu hình Firebase thì app **vẫn học bình thường**: tiến độ lưu tại máy, dữ liệu nằm trong hàng đợi
chờ đồng bộ. Nối Firebase sau (xem `docs/DEPLOY.md`) là toàn bộ lịch sử được đẩy lên, không mất gì.

---

## Cây thư mục

```
web/                  Ứng dụng học (React + Vite + Tailwind)
  src/chung/          TẦNG VỎ — dùng chung cho MỌI môn, không môn nào được sửa
    lib/              nenTang (Firebase) · taiKhoan (đăng nhập, hồ sơ) · soQuyen (sổ đăng ký)
    components/       kệ sách · bảng xếp hạng · sổ bố mẹ · bảng cô giáo · đăng nhập
  src/mon/toan/       MÔN TOÁN — khép kín, không tệp nào của môn khác đụng vào
    lib/              flow · progress · hocba · adaptive · dau · noiDung · duLieu · sync
    components/       phòng học · màn chủ đề · Mùa giải · trang chính của quyển
  src/mon/tienganh/   MÔN TIẾNG ANH — khép kín, 5 quyển
    lib/              phongnoi · nhanluot · loidan_nhan · hosoai · bangtrangthai
                      kehoach · baihoc · chandoan · phudao · goiPhuDao
                      chamviet · chamnoi · dandat · zpd · lantruyen · onlai
    components/       phòng luyện nói · bài học · đọc hiểu · viết ngắn · ôn lại · phụ đạo
  public/content/     462 bài · 884 hình · 713 video · kỳ sát hạch · chỉ mục  (deploy lên CDN)
  functions/          Cloud Functions: đăng nhập OTP · BKT · ôn tập · sổ học & bảng cô đêm
                      luyennoi · chamviet · phudao · chula · vantay (phần gọi mô hình)
  test/               101 tệp · 2 637 phép kiểm (node thuần, không cần trình duyệt)
                      + 61 phép canh luật Firestore (cần bộ giả lập)
  firestore.rules     luật bảo mật — nhật ký học BẤT BIẾN

figforge/             Bộ sinh hình: 25 nguyên mẫu + 672 figureSpec
data/                 km_v1_38 (đồ thị tri thức) · 168 DL json · 14 DCR · manifest hình
docs/                 Sổ tay thực thi · kế hoạch thi công · thiết kế VideoForge · bộ luật CodeGen
```

---

## Kiến trúc — ba điều đáng chú ý

**1 · Nội dung là file tĩnh. Mô hình ngôn ngữ chỉ vào ĐÚNG ba chỗ.**
Bài học (JSON), hình (PNG) và video sinh sẵn từ trước, đẩy lên Hosting/CDN — app chỉ `fetch`.
→ không phí API, mở offline được sau lần tải đầu, không rủi ro model đổi hành vi giữa chừng.

Ba chỗ ngoại lệ, cả ba thuộc môn Tiếng Anh: **phòng luyện nói** (cô giáo máy đáp lời bé),
**chấm bài viết ngắn**, và **soạn câu phụ đạo** — hai cái đầu là *đối thoại*, thứ không sinh
sẵn được; cái thứ ba chỉ chạy khi kho 4.226 câu tĩnh không có đủ câu quanh nút bé đang mắc.

Mọi câu tiếng Anh mô hình sinh ra đều phải qua phép soi vốn từ trước khi tới bé, và **câu hỏi**
thì qua thêm hai tầng nữa (xem [Tiếng Anh: cô giáo máy](#tiếng-anh-cô-giáo-máy-và-chín-lớp-chốt-chặn)).
Không có khoá thì ba chỗ ấy báo lỗi tử tế — phụ đạo còn tự lùi về kho tĩnh — và mọi phần còn
lại học bình thường.

**2 · Lõi tách khỏi giao diện để kiểm định được.**
Toàn bộ luật (dựng dòng chảy bài học, chấm bài, mở khoá, BKT, lịch ôn, sổ phụ huynh, và cả luật
của cô giáo máy) nằm trong module JS thuần, chạy test bằng `node` trên **dữ liệu thật của cả
462 bài** — kể cả mô phỏng học trọn bài và mô phỏng đứt mạng giữa chừng.

Phần gọi mô hình cũng kiểm được bằng `node`: hàm mạng **tiêm qua tham số**, không mock module.
Nhờ thế cổng đếm được số lần gọi, soi được gói gửi lên, và thử được ca "mô hình trả lời sai hai
lần liền" — không cần khoá, không cần mạng.

**3 · Cổng `mustPass` là trục sư phạm.**
Sai câu bẫy thì **không mở bài sau**, dù đúng 2/3 câu còn lại. Bẫy mới là thứ mỗi bài dạy,
nên nó được ưu tiên hơn điểm số ở mọi tầng: luật đạt, luật mở khoá, và cả trọng số BKT.

---

## Tình trạng hoàn thành

### Chín quyển

| Quyển | Bài | Video | Ghi chú |
|---|---|---|---|
| Toán lớp 2 | 71 | 71 | xong trọn |
| Toán lớp 3 | 34 | 34 | xong trọn |
| Toán lớp 4 | 95 | 95 | xong trọn |
| Toán lớp 5 · Quyển 1 | 168 | 168 | xong trọn — quyển được ghi chép dày nhất, cả phần dưới nói về nó |
| Mùa giải lớp 5 | 26 | — | vòng đấu, không có bài giảng riêng |
| Tiếng Anh lớp 1 | 16 | 37 | xong trọn |
| Tiếng Anh lớp 2 | 16 | 34 | xong trọn |
| Tiếng Anh lớp 3 | 21 | 88 | xong trọn — thêm đọc hiểu · bài viết chấm AI |
| Tiếng Anh lớp 4 | 21 | 94 | xong trọn |
| Tiếng Anh lớp 5 | 20 | 92 | xong trọn — quyển đầu có THÌ QUÁ KHỨ |

### Bốn phần của quyển Toán lớp 5 (bản dựng gốc)

| Phần | Nội dung | Trạng thái |
|---|---|---|
| A | 672 hình cho 168 micro · 25 nguyên mẫu · km v1.38 | ✅ 14/14 chương |
| B | LessonPlayer 5 chặng · 168 micro · 14 kỳ sát hạch · huy hiệu | ✅ 4/4 lô |
| C | Firestore + luật bảo mật · offline · BKT · ôn tập · adaptive · sổ phụ huynh | ✅ 3/3 lô |
| D | Đóng gói · hướng dẫn deploy · checklist nghiệm thu | ✅ |

**Con có làm được bài không — soi 100% câu hỏi.**
Mỗi lần `npm test` là 1 654 câu (1 141 câu luyện tập + sát hạch, cộng câu chốt nhanh và câu xen giữa
bài mẫu) bị soi lại bằng chính lõi mà app dùng để dựng ô trả lời:

| Hàng rào | Hiện trạng |
|---|---|
| Mọi câu đều có cách trả lời (ô nhập hoặc nút chọn) | ✅ 1 654/1 654 · 6 câu tự luận có băng báo riêng |
| Mọi ô nhập đều có nhãn hiện thường trực | ✅ 1 292 ô · 309 bài nhiều ô đều có nhãn thật |
| Bài nhiều ô: nhãn không trùng nhau | ✅ 0 vi phạm |
| Không ô nào chỉ hiện dấu "?" | ✅ 0 vi phạm |
| Không đề bài / gợi ý / thẻ công thức nào bị cắt cụt | ✅ 0 vi phạm |
| **Đề hỏi mấy ý thì có đủ chừng ấy ô điền** | ✅ 0 vi phạm |
| **Không ô nào bắt con tự nghĩ ra chữ để gõ** | ✅ 0 vi phạm — đáp án bằng chữ đều thành nút bấm |
| **Câu tự luận vẫn có chỗ cho con viết** | ✅ 0 vi phạm |

**Ô nhập chỉ dành cho SỐ.** Mọi đáp án bằng chữ đã thành **nút bấm chọn** — con không phải
đoán xem nên gõ "bằng nhau" hay "như nhau". Cách làm: câu phân loại a/b/c thì bộ chọn chính
là tập đáp án của các ô anh em (không bịa gì cả); còn lại soạn tay 53 bộ, phương án nhiễu
lấy đúng cái sai trẻ hay mắc. Ký hiệu toán (`3/4`, `9 : 8`, `2 giờ 24 phút`, `9 dư 2`) vẫn
để con gõ, nhưng chữ mờ nói rõ dạng cần điền.

**Hai lối học.**
`Theo chương trình` — học lần lượt cả 168 bài, đúng thứ tự sư phạm.
`Con tự chọn chủ đề` — **bài đầu của mọi chương đều mở**, con thích chủ đề nào vào chủ đề đó;
nhưng TRONG một chương vẫn phải học lần lượt, vì các bài trong chương xây chồng lên nhau.
Đổi chế độ ở trang chính, app nhớ lựa chọn.

**Chạy local thì không hỏi đăng nhập** (`import.meta.env.DEV`) — cờ này do Vite đặt nên
không thể lọt sang bản đưa lên mạng, không phải nhớ tắt bằng tay.

Nhãn nằm **ngoài** ô chứ không phải chữ mờ trong ô — con gõ ký tự đầu tiên mà nhãn vẫn còn đó.
Bài nhiều ô được đánh số a/b/c/d, có chip đơn vị, và một dòng nói thẳng "bài này cần điền mấy ô".

**Mở app ra là biết phải làm gì.**
Thứ đầu tiên con thấy là thẻ *việc của con bây giờ*: **tên bài thật** (không phải mã `B1.M1`),
mất khoảng mấy phút, và một nút duy nhất để bấm. Lần đầu vào thì thẻ kể trước đường đi bốn nhịp
(cô giảng → xem mẫu → tự luyện → thi lấy huy hiệu) và nút ghi "Bắt đầu học", không phải "Học tiếp".

**Bỏ dở giữa chừng không mất bài.** App nhớ con đang ở bước nào của từng micro; mở lại là vào đúng
chỗ cũ ("Học tiếp — bước 12/23"), vẫn có nút *Từ đầu* nếu con muốn học lại. Dấu này KHÔNG tính là
đã làm bài và không mở khoá micro sau — có phép kiểm riêng canh đúng chỗ đó.

Danh sách bài chỉ hiện những bài **học được ngay**; phần chưa mở gộp thành một dòng, bấm vào thì
giải thích vì sao (phải đúng câu bẫy mới qua) thay vì im lặng như trước.

**Mục tiêu bài học viết cho con, không viết cho người lớn.**
Mỗi micro có hai bản mục tiêu: `objective.kidText` con đọc ở màn mở bài, và `objective.text`
bản gốc gấp lại phía dưới cho bố mẹ và thầy cô. Bản gốc trung vị **61 chữ**, có bài **9 cặp
ngoặc lồng nhau** — con lớp 5 mở ra là lướt qua. Bản viết lại cho con:

| | bản gốc | bản cho con |
|---|---|---|
| số chữ, trung vị | 61 | **26** |
| câu dài nhất | 101 chữ | **32 chữ** |
| bài dài trên 40 chữ | 154/168 | **0** |
| bài có ngoặc đơn | 153/168 | **0** |

Phép kiểm canh cả năm điều: bài nào cũng phải có bản cho con, bản gốc phải còn nguyên, bản cho
con không được là bản chép lại, không quá 35 chữ, không lồng nhiều ngoặc.

**Đăng nhập và theo dõi kết quả.**
Không có màn đăng ký: **nhập email → nhận mã 6 số → vào**. Chưa có tài khoản thì máy chủ
lập luôn, rồi hỏi đúng hai câu (tên con, đang học lớp mấy). Một tài khoản là một học sinh —
phụ huynh và con dùng chung.

| Vai trò | Vào bằng | Thấy gì |
|---|---|---|
| học sinh | mã OTP qua email | phòng học + sổ học của mình |
| giáo viên | mã OTP qua email | bảng toàn bộ học sinh, bấm vào một em xem nhật ký **từng câu** |
| quản trị | email + mật khẩu | toàn quyền |

Bảo mật mã OTP: **không lưu mã, chỉ lưu bản băm** (kèm email và một bí mật máy chủ);
sai 5 lần là huỷ mã; 60 giây mới cho gửi lại, tối đa 5 mã mỗi giờ; mã sống 10 phút và
**chỉ vào được một lần**. Trả lời giống hệt nhau dù email có trong hệ thống hay không —
không để lộ ai đang dùng app.

Chốt chặn quan trọng nhất: luật bảo mật đọc vai trò từ **custom claim trong token**, không
đọc từ Firestore. Người dùng ghi được vào `users/{uid}` của mình, nên tin vào trường `role`
ở đó thì ai cũng tự phong mình làm giáo viên rồi đọc kết quả cả trường.

**Học thử không cần đăng nhập.** Bài nằm ở máy, và trang chủ nói thẳng điều đó thay vì để
bố mẹ tưởng đã lưu lên mạng. Đăng nhập lúc nào thì toàn bộ hàng đợi được **sang tên** cho
tài khoản thật rồi đẩy lên — không sang tên thì luật bảo mật từ chối trong im lặng và công
học bay sạch, nên có phép kiểm riêng canh đúng chỗ đó.

### Hình mở bài: đối thoại, không phải lời kể

Mỗi micro mở màn bằng một hình `character_speech`: **Trí Long (hoặc Cáo Đề) nói cái sai mà
trẻ hay mắc — Su Kem hích nhẹ để con tự nhận ra**. Su Kem không đọc đáp án; phần giảng phía
sau mới làm việc đó.

Bộ sinh `figureSpec` ngày trước bắt lời thoại bằng regex tìm ngoặc kép. Regex ấy hỏng theo
bốn kiểu, cả bốn đều làm hình không đọc được, và đã sửa hết trên **28/168 hình**:

| Kiểu hỏng | Số hình | Ví dụ |
|---|---|---|
| bong bóng **rỗng** | 15 | Su Kem đứng im, chỉ có khung |
| bong bóng nuốt **cả lời dẫn** | 11 | Trí Long "nói" luôn đoạn kể về Su Kem, dài 243 ký tự |
| lời thoại **cắt cụt** ở dấu ngoặc | 7 | Su Kem: `100" cho số 3,5.` |
| **gán nhầm nhân vật / nhầm màu** | 3 | câu SAI của Trí Long gán cho Su Bống, lại tô xanh |

`test/hinhmobai.test.mjs` khoá cả bốn kiểu lại, cộng thêm hai luật màu: Su Kem không bao giờ
bị tô đỏ, và lời gỡ (xanh) phải đứng **sau** cái sai (đỏ) — đảo lại là tô xanh cho chính câu
sai. Riêng bài mở đầu B1.M1 cố ý để ngỏ ("cả lớp chia hai phe — con theo phe nào?") nên cả
hai bong bóng để **trắng**: tô màu là lộ đáp án trước khi con kịp nghĩ.

Phép kiểm còn đối chiếu `sha256_16` trong bài **và** trong manifest với PNG thật, vì sửa lời
thoại mà quên vẽ lại thì con vẫn xem hình cũ mà không ai biết.

### Năm kiểu trả lời — con nhìn là biết phải làm gì

`answerMode()` trong `flow.js` là nguồn sự thật duy nhất; mọi màn hình hỏi nó chứ
không tự đoán theo `format`. Mỗi kiểu kèm một câu chỉ thị hiện ngay dưới đề.

| Kiểu | Chỉ thị | Số câu |
|---|---|---|
| `so` | Con điền một con số vào ô. | 408 |
| `bieuthuc` | Con điền biểu thức toán vào ô (xem chữ mờ để biết dạng). | 55 |
| `dungsai` | Con bấm chọn ĐÚNG hoặc SAI. | 77 |
| `chondapan` | Con bấm chọn một đáp án. | 88 |
| `tuluan` | Con làm ra nháp, xong xem lời giải mẫu để tự so. | kỳ sát hạch chương |

Lỗi từng có: `inputCount` trả 0 cho Đúng/Sai và trắc nghiệm, nên **90 câu ở phòng
luyện không có nút nào để bấm** — 68 câu được chấm ĐÚNG dù con chưa trả lời (ô rỗng
đọc thành `false`, trùng đáp án), 22 câu chấm SAI rồi kẹt cứng. Nay tf/mcq cũng là
một ô trong `answerFields`, và **sai bao nhiêu lần cũng sửa lại được** — chỉ khoá ô
khi con đã đúng.

`test/hocsinh.test.mjs` đóng vai học sinh đi hết **168 bài · 2956 bước · 1309 câu**,
chỉ dùng thứ hiện trên màn hình chứ không đọc lén `answerKey`. Phép kiểm cốt lõi:
*con làm đúng thì có được công nhận không*. Chạy trên mã cũ nó báo đúng 542 câu
hỏng — nên kết quả sạch là đáng tin, không phải do phép rà dễ dãi.

### Bộ nhớ đệm: dấu phiên bản nội dung

Nội dung để `immutable` 7 ngày mà tên tệp không đổi khi sửa bài → máy đã mở trang
giữ bản cũ cả tuần. Ba tầng, mỗi tầng một cách:

| Thứ | Cache-Control | Đổi thì sao |
|---|---|---|
| `/`, `/hoc/**`, `index.html` | `no-cache` | deploy ăn ngay |
| `/content/**` (bài, hình) | 7 ngày `immutable` | đường dẫn mang `?v=…` → thành tệp mới |
| `/assets/*.js|css` | 1 năm `immutable` | Vite đã băm sẵn vào tên tệp |

Bài/chỉ mục dùng mã băm chung của cả `public/content`; **hình dùng `sha256_16` của
chính nó**, nên vẽ lại một hình chỉ tải lại đúng hình ấy, 671 hình kia nằm yên.
Hàm băm ở `tools/noidung_version.mjs`, `vite.config.js` và bộ kiểm dùng **chung** —
chép hai bản thì sửa một bên mà bên kia vẫn xanh, đúng cái bẫy đang muốn tránh.

Cạm bẫy đã vấp: header khớp theo **đường dẫn yêu cầu**, không phải đích rewrite —
đặt `source: "/index.html"` thì `/` vẫn rơi vào mặc định `max-age=3600`. Phải thêm
`**/!(*.*)` mới phủ hết các đường dẫn SPA.

### Nhật ký học: đúng · đủ · kịp thời

Mỗi lượt bấm "Kiểm tra" là MỘT dòng (không phải mỗi câu một dòng) — con sai hai lần
rồi mới đúng thì cô thấy đủ ba lượt, kèm `answer` (con gõ gì), `expected`, `ms` đo
riêng câu ấy, `hintsUsed`, `mode`, `revealed`.

| | Trước | Sau |
|---|---|---|
| **Đủ** — chặng được ghi | 2/4 (mất 513/1654 câu = 31%) | đủ 4: practice · assess · check · worked |
| **Đủ** — bỏ dở giữa bài | mất trắng, TB 7 câu/bài | đẩy dần sau mỗi lượt, giữ nguyên |
| **Đúng** — `ms` | tính từ lúc MỞ BÀI | thời gian riêng từng câu |
| **Đúng** — `ts` | cả loạt chung một mốc → "0 phút học" | mốc riêng từng lượt |
| **Kịp thời** | chỉ ở màn kết bài, bảng dựng 21:15 | gửi ngay + nút "↻ Cập nhật ngay" |

Ba cạm bẫy đã vấp, ghi lại kẻo quên:

- **513 câu chốt nhanh / xen ví dụ không có mã.** Ghi lên máy chủ mà không có mã thì
  cô cũng không biết là câu nào. Phải đặt mã ổn định trước (`C1…`, `W1…`).
- **Nhật ký BẤT BIẾN nên dữ liệu sai không xoá được.** Dòng ghi bằng luật cũ (`ms`
  tính từ lúc mở bài) nằm lẫn mãi mãi. Chữa bằng dấu phiên bản `v`: thống kê thời
  gian chỉ dùng dòng `v ≥ 2`, và sổ hiện "—" kèm lời giải thích thay vì "0 phút".
  Thà nói chưa đo được còn hơn đưa bố mẹ một con số sai.
- **Sổ học lọc theo `ts` (giờ máy của con).** Máy tính bảng đặt sai ngày là bản ghi
  rơi khỏi cửa sổ 7 ngày, sổ trống mà không ai hiểu vì sao. Đã đổi sang `serverTs`.

Đẩy dần dựng lại bản ghi từ TOÀN BỘ nhật ký phiên chứ không chỉ lượt mới: mã nhúng
số thứ tự nên dựng lại cho ra đúng mã cũ, hàng đợi ghi đè theo mã — gửi bao nhiêu
lần cũng không sinh dòng trùng.

**Chưa làm (đã ghi rõ, không giấu):**
- **Máy chủ gửi mail**: hàm OTP cần bốn bí mật `OTP_PEPPER`, `SMTP_HOST`, `SMTP_USER`,
  `SMTP_PASS` (xem `docs/DEPLOY.md` bước 7a). Chưa đặt SMTP thì mã **chỉ in ra log**, không
  gửi đi đâu — tiện lúc chạy thử, nhưng chạy thật mà quên là không ai đăng nhập được.
- Sinh đề biến thể: metadata `generator` trong dữ liệu viết bằng văn xuôi nên chỉ **1/181** câu
  dùng được. Giao diện **ẩn nút "Đề khác"** thay vì sinh đề bừa. Muốn dùng thật phải nâng cấp metadata.
- Hình miền cho từng micro hiện là **4 hình/micro**; các màn tương tác đặc thù (kéo thả, đếm ô)
  chưa làm — bản hiện tại là hình tĩnh + câu hỏi.
- Video: đã có thiết kế (`docs/thiet_ke_agent_videoforge.md`) nhưng chưa dựng. Với kiến trúc hiện tại,
  video nên sinh bằng cách **quay màn hình chính các component này**, không cần pipeline riêng.

---

## Tiếng Anh: cô giáo máy, và chín lớp chốt chặn

Năm quyển (lớp 1→5, 94 bài, 345 video). Khác Toán ở một điểm: **ba** chỗ gọi mô hình ngôn
ngữ lúc chạy (Groq · `openai/gpt-oss-120b`, qua Cloud Functions) — **luyện nói**, **chấm bài
viết**, và **soạn câu phụ đạo** khi kho tĩnh không đủ.

**Máy chủ KHÔNG lưu gì.** Mọi lời gọi đi qua callable có chốt cửa; ngữ cảnh do máy con giữ và
tự đẩy lên Firestore theo luật. Lý do thực tế: đây là tiếng nói của trẻ con — chỗ nào không
lưu thì chỗ ấy không bao giờ rò.

### Vì sao không thả cho mô hình nói

Bé sáu tuổi đang tập **nhại**, nên một câu sai là dạy sai. Đã sinh ra thật khi thả tự do:
`"Bye, bike."` — đúng ngữ pháp, nghe xuôi, vô nghĩa. Nên đảo từ TIN sang SOI: máy con tự soi
câu cô giáo nói, và mỗi tầng dưới đây là một lớp chốt.

| Lớp | Việc | Đo được |
|---|---|---|
| `soiCau` · 5 đường công nhận | câu cô nói phải nằm trong vốn từ của bài | tắt một đường thì nhóm câu tương ứng rơi — có phép thử đảo chiều |
| **xin lại khi bị bác** | nói cho mô hình biết sai CHỖ NÀO rồi gọi lại, trần 2 lần | phải lui về câu máy dựng: **20,4% → 3,7%** (54 lượt thật) |
| **một nhãn cho mỗi lượt của bé** | 9 nhãn thuần code → 9 lời dặn ngắn thay cho một lời dặn mười điều | 100% lượt có nhãn; bé sai → cô nhắc đúng câu ấy **0/9 → 5/7** |
| **trí nhớ qua nhiều buổi** | câu bé đã nói được · chữ hay sót · thứ bé thích; có HẠN, có trần, bố mẹ xoá được | buổi 2 mang theo mục của buổi 1 |
| **một bảng trạng thái** | sáu nguồn về bé gom một chỗ cho cả bốn màn | `vectorS(` chỉ còn được gọi ở một tệp |
| **chấm viết 3 mắt xích** | tìm lỗi (cấm sửa) → sửa → soi chữ lạ → xin lại → lời cho bố mẹ | mục bị bỏ vì chữ lạ: **7 → 0** (5 bài thật) |
| **kế hoạch buổi** | 5–7 việc lập đầu buổi bằng CODE, bày ra cho bé thấy và nghe | 50 buổi mô phỏng: **100%** xong kế hoạch; Groq thật: 5/5 việc, 2 buổi |
| **bài học cuối buổi** | một lượt gọi để cô ngẫm lại, rồi ghi vào trí nhớ | buổi 2 mang bài học của buổi 1; 0 bài bị soi bác |
| **phụ đạo: hai vòng tĩnh rồi mới tới mô hình** | nút gốc rễ #1 → #2 → (hết câu) mô hình, 1 lời gọi | 9/11 câu mô hình soạn qua cả hai tầng hậu kiểm |

⚠ **Cỡ mẫu của mấy con số ấy nhỏ, nói thẳng.** Chúng đo bằng mô hình THẬT, nhưng trên vài chục
lượt và vài bài — không phải vài trăm. Chúng đủ để nói "hướng này đúng", chưa đủ để nói "còn
đúng ở mọi quyển". Mỗi tầng đều có bộ đếm (`LOI_SUA_CO` · `LOI_CHU_LA` · `LOI_SUA_LAI` ·
`LOI_NOI_KHUON`) để đo lại trên bản chạy thật, và đó mới là con số đáng tin.

Một tầng CHƯA chứng minh được bằng lượt thật: đường **nới khuôn JSON** (khi Groq bác vì khuôn).
Lỗi ấy ngẫu nhiên, và lần đo lại 30 lượt thì nó không tái hiện — nên đường vá hiện chỉ có cổng
đơn vị chứng minh. Ghi ra đây để đừng ai tưởng nó đã được việc trên bản thật.

**Việc chỉ tiến khi bé nói đúng.** Kế hoạch buổi là một ĐÍCH, không phải một thanh
trang trí: bé sai thì bước giữ nguyên (hạ bậc `thay → mau → tu`), sai ba lần thì chèn
một bước phụ đạo ở nút gốc rễ. Và khi có kế hoạch thì "ba lượt đạt liền" **không kết
buổi nữa** — đo được là nếu để cả hai điều kiện thì 100% buổi "xong" mà trung bình chỉ
làm được 76% số bước, tức thanh bước nói dối với bé.

**Câu do mô hình soạn phải qua BA tầng, và tầng thứ ba là người.** Hậu kiểm vốn từ trả
lời "câu này dùng chữ bé đã học không"; nó không nói được câu ấy có hai đáp án đúng hay
gợi ý lộ đáp án. Nên: `soiCauAI` soi sáu luật của một câu hỏi, `soiBoCauAI` soi cả BỘ
(bốn câu y hệt nhau thì từng câu đều hợp lệ), rồi câu phải nằm trong hàng đợi
`choDuyetTA` chờ người lớn — **bé ghi được, bé không đọc được**. Luật thứ bảy —
"phương án nhiễu có thật là cái sai trẻ hay mắc hay chỉ là một chữ bừa" — không kiểm
được bằng code, và đó chính là lý do hàng đợi tồn tại.

**Điểm máy chấm là điểm TẠM.** Bố mẹ đồng ý hoặc sửa, một chạm, trong Góc bố mẹ — không có nút
nào cho bé tự xác nhận điểm của mình. Điểm máy chấm được giữ lại bên cạnh điểm bố mẹ sửa, nên
câu "máy chấm có hay sai không" luôn trả lời được. Luật Firestore chốt: khi đánh dấu *đã xác
nhận* thì **chỉ ba trường** được đổi — không sửa kèm lời chấm hay bài bé viết.

**Vân tay prompt, không lưu prompt.** Mục 2.5.2 của luận văn cần biết "lượt này dùng mẫu prompt
nào", mà giao ước là không lưu gì của bé. Hai điều ấy chỉ chọi nhau nếu tưởng phải lưu cả
prompt: để so hai mẫu thì chỉ cần một mã băm của **phần khung**. Phần riêng của bé nằm giữa hai
dấu `<<RIENG … RIENG>>` và bị bỏ sạch trước khi băm — hai bé khác nhau học cùng unit cho ra
**cùng một** vân tay, và đó vừa là điều làm phép so có nghĩa vừa là điều làm nó không lần ra ai.

### Bảy chỗ hỏng chỉ lộ ra khi gọi mô hình THẬT

101 tệp cổng xanh, build xanh, và cả bảy vẫn ở đó — vì chúng là lỗi **giữa các tầng** (không
tầng nào sai một mình) hoặc lỗi **chất lượng** (mỗi câu đều hợp lệ, cả bộ thì không).

- **Lời dặn tự chọi nhau.** Luật 4 nằm trong khối `HARD RULES` ("breaking any of these makes
  the lesson useless") và viết thẳng *"NEVER say the same English sentence — vary the word in
  the slot"*; dòng dặn riêng của lượt sửa thì đòi đọc lại NGUYÊN câu ấy. Mô hình chọn bên được
  **ta** gọi là hard rule — đúng theo lời ta dặn. Muốn một dòng ở dưới thắng một luật ở trên
  thì phải **nói thẳng ra** là nó thắng.
- **Chốt soi gạt chính câu đúng.** `soiCau` bác câu trùng lượt trước (`lap`), rồi vòng xin lại
  đọc lý do ấy và nhắc mô hình *"say a DIFFERENT sentence"* — tức **đẩy** nó đi sai. Ba tầng
  đều làm đúng phận mình và cộng lại thành hỏng. Dấu hiệu nhận ra: bộ đếm xin-lại cao bất
  thường (11 trên 27 lượt; vá xong còn 3).
- **Đường lui không bao giờ chạy.** `response_format: json_object` nghiêm ngặt làm Groq bác
  ngay trên máy chủ nó, nên `docTraLoi` — hàm viết RA để đỡ chữ trần, có chú thích tử tế —
  không bao giờ nhận được chữ ấy. Buổi dài tới lượt 6+ thì bé chỉ thấy dòng đỏ; một quyển chết
  liền **năm lượt**. Nay nới khuôn đúng một lần khi Groq bác *vì khuôn*.
- **Kế hoạch và lời dặn nói hai từ khác nhau.** `THIS STEP: practise the word "chicken"` ở
  dòng trên, `THIS TURN: say exactly this sentence: "I like milk."` ở dòng dưới — vì bước kế
  hoạch đưa mẫu câu TRẦN, mà lệnh "đọc nguyên văn" thì đọc câu ví dụ của sách. Mô hình đọc hai
  lệnh về hai từ thì chọn bừa, và bước kế hoạch coi như không có.
- **Ba bài học cho cùng MỘT lỗi.** Cô ngẫm lại buổi học rồi viết "thiếu *my* trước brother" ·
  "…trước mother" · "…trước father" — ba dòng chiếm chỗ trong lời dặn buổi sau mà chỉ nói một
  điều. Dấu hiệu trùng là **khuôn câu tiếng Việt**, không phải tập chữ trích: phép dọn đầu của
  tôi đòi cùng tập chữ nên không bắt được gì.
- **Lời dẫn chứa thẳng đáp án.** Câu phụ đạo có lời dẫn tiếng Việt `Bạn của tôi luôn nói: I
  like fish.` cho câu đáp án đúng `I like fish` — bé chỉ việc chép lại. Phép soi ban đầu chỉ
  ngó phần *gợi ý*, không ngó *lời dẫn*.
- **Bốn câu y hệt nhau.** Cùng bộ phương án, cùng đáp án, chỉ khác lời dẫn. **Từng câu** một
  thì cả bốn đều hợp lệ; cả bộ thì là một câu hỏi lặp bốn lần. Soi từng câu không bao giờ thấy
  được chuyện này — phải có một phép soi CẢ BỘ.

### Ô trống có KIỂU — và lỗi ấy nằm ở ba chỗ

`loaiOTrong` xưa chỉ biết hai loại (tên người · từ bất kỳ), nên mọi ô khác nhận MỌI từ của bài:
`"Do you live in this sixteen?"` · `"He's truck."` đi qua `soiCau` sạch. Nay khai thêm bốn loại,
và **chỉ khai loại nào dữ liệu tự nói được** (`so` suy từ lời chú có chữ số; `ing`·`qk`·`nhieu`
suy từ chính trường dẫn xuất của mục từ).

Đo trên toàn bộ dữ liệu thật: **câu sách bị gạt oan 0** · **câu sai nay bị chặn 293** (10,2%).

Cùng một lỗi, ba chỗ — sửa một chỗ là nó vẫn ra: `soiCau` · bộ sinh kịch bản Python (4 câu đã
lên dữ liệu phát hành) · `dienBuoc` (chỗ chỉ lộ ra lúc chạy, vì nó điền theo sở thích TỪNG BÉ).

**Chỗ chưa vá, nói thẳng:** `"It's my sure."` VẪN đi qua, vì bài có dạy từ `sure` và mục từ
vựng **không có trường từ loại** (740 mục). Đoán từ lời chú tiếng Việt là dựng một cổng ghim
vào chính tả — việc còn lại là việc của DỮ LIỆU. Có một cổng *đòi* câu ấy vẫn đi qua, và nó đỏ
lên ngày nào mục từ có trường từ loại, để nhắc quay lại.

### Chưa làm (ghi rõ, không giấu)

- **Chấm viết "lỗi ∥ khen" · chấm nói mơ hồ bỏ phiếu** — việc cuối của GĐ 2 trong
  `docs/REVIEW_18_MAU_AI_AGENT_TIENG_ANH.md`, chưa dựng.
- **Hàng đợi duyệt chỉ ĐẦY lên, chưa có đường ra.** Câu do mô hình soạn nằm chờ người lớn
  (`choDuyetTA`), nhưng script ghép câu đã duyệt vào kho tĩnh thì chưa dựng — đó là việc của
  dây chuyền nội dung.
- **Nhãn `nhamTu` chưa có nguồn trên bản chạy**: phòng nói chấm bằng `chamCau`, mà chỉ `chamTu`
  tính `nhamThanh`. Nhãn phân loại đúng khi nạp tay (đã thử thật), nhưng chưa ai nạp.
- **Lời dặn cho dùng chữ chức năng mà `chuLa` thì không** — luật 1 ghi *"plus the bare function
  words"*, còn chốt soi gạt `there` · `on` · `the`. Vá nó là **nới** hàng rào vốn từ, nên để
  quyết chứ không tự làm.
- **Khung MẪU CÂU HAI Ô không ai soi nổi.** `soiCau` chỉ điền được ô đầu, nên câu của chính
  sách như `He's eleven years old.` (mẫu `How old is she? - She's + [Number] + years old.`) bị
  bác. Ba bài có khung hai ô; chúng mất phần luyện "thay từ".
- **Đường đọc Firestore thật của `tools/doc_delta_c.mjs`** chưa thử được (cần khoá quản trị và
  dữ liệu thật). Chỉ đường `--tep` có bằng chứng.
- **Chưa deploy `firestore.rules`.** BA việc cần nó: trí nhớ của cô (`hoSoAI`), bố mẹ xác nhận
  điểm (`allow update`), và hàng đợi duyệt câu (`choDuyetTA`). Thiếu bước này thì Firestore từ
  chối **trong im lặng**: sổ tại máy vẫn đúng, bé đổi máy là mất, và không gì báo.

      cd web && firebase deploy --only firestore:rules

---

## Tài liệu

* `docs/DEPLOY.md` — dựng Firebase và đưa lên mạng, từng bước
* `docs/CHECKLIST.md` — checklist nghiệm thu trước khi cho con dùng thật
* `docs/so_tay_thuc_thi.md` — sổ tay thực thi toàn dự án
* `docs/REVIEW_18_MAU_AI_AGENT_TIENG_ANH.md` — rà 18 mẫu kiến trúc AI agent cho môn Tiếng
  Anh: chẩn đoán, 12 việc (V1–V12), ca kiểm, và bản nháp lời dặn
* `web/README.md` — chi tiết kỹ thuật ứng dụng

---
*Triết lý xuyên suốt: "Thực hành sinh hiểu biết, hiểu biết sinh lý luận, lý luận soi sáng thực hành."*
