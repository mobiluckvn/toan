# Toán Tư Duy lớp 5 · Quyển 1 — Trang học tập thích ứng

**MOBILUCK / code247.ai** · Kỹ Sư Nhí lớp 5 · 168 micro · 672 hình · 1.141 câu hỏi · 14 kỳ sát hạch

Trang web cho học sinh lớp 5 tự học trọn Quý 1: **giảng nguyên tắc → xem bài mẫu → tự luyện → sát hạch lấy huy hiệu**,
có mức thạo BKT, ôn tập ngắt quãng và sổ theo dõi cho bố mẹ.

---

## Chạy trong 3 phút

```bash
cd web
npm install
npm run dev      # http://localhost:5173  — học được ngay, chưa cần Firebase
npm test         # 339 phép kiểm chạy trên dữ liệu thật của 168 micro
```

Chưa cấu hình Firebase thì app **vẫn học bình thường**: tiến độ lưu tại máy, dữ liệu nằm trong hàng đợi
chờ đồng bộ. Nối Firebase sau (xem `docs/DEPLOY.md`) là toàn bộ lịch sử được đẩy lên, không mất gì.

---

## Cây thư mục

```
web/                  Ứng dụng học (React + Vite + Tailwind)
  src/lib/            LÕI có test: flow · progress · sync · adaptive · content · firebase
  src/components/     16 component: phòng học · đăng nhập OTP · sổ học · bảng giáo viên
  public/content/     168 bài học · 672 hình · 14 kỳ sát hạch · chỉ mục  (deploy thẳng lên CDN)
  functions/          Cloud Functions: đăng nhập OTP · BKT · ôn tập · sổ học & bảng cô đêm
  test/               339 phép kiểm (node thuần, không cần trình duyệt)
  firestore.rules     luật bảo mật — nhật ký học BẤT BIẾN

figforge/             Bộ sinh hình: 25 nguyên mẫu + 672 figureSpec
data/                 km_v1_38 (đồ thị tri thức) · 168 DL json · 14 DCR · manifest hình
docs/                 Sổ tay thực thi · kế hoạch thi công · thiết kế VideoForge · bộ luật CodeGen
```

---

## Kiến trúc — ba điều đáng chú ý

**1 · Nội dung là file tĩnh, không có API model lúc chạy.**
Bài học (JSON) và hình (PNG) sinh sẵn từ trước, đẩy lên Hosting/CDN. App chỉ `fetch`.
→ không phí API, mở offline được sau lần tải đầu, không rủi ro model đổi hành vi giữa chừng.

**2 · Lõi tách khỏi giao diện để kiểm định được.**
Toàn bộ luật (dựng dòng chảy bài học, chấm bài, mở khoá, BKT, lịch ôn, sổ phụ huynh) nằm trong
module JS thuần, chạy test bằng `node` trên **dữ liệu thật của cả 168 micro** — kể cả mô phỏng
học trọn bài và mô phỏng đứt mạng giữa chừng.

**3 · Cổng `mustPass` là trục sư phạm.**
Sai câu bẫy thì **không mở bài sau**, dù đúng 2/3 câu còn lại. Bẫy mới là thứ mỗi bài dạy,
nên nó được ưu tiên hơn điểm số ở mọi tầng: luật đạt, luật mở khoá, và cả trọng số BKT.

---

## Tình trạng hoàn thành

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

## Tài liệu

* `docs/DEPLOY.md` — dựng Firebase và đưa lên mạng, từng bước
* `docs/CHECKLIST.md` — checklist nghiệm thu trước khi cho con dùng thật
* `docs/so_tay_thuc_thi.md` — sổ tay thực thi toàn dự án
* `web/README.md` — chi tiết kỹ thuật ứng dụng

---
*Triết lý xuyên suốt: "Thực hành sinh hiểu biết, hiểu biết sinh lý luận, lý luận soi sáng thực hành."*
