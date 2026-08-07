# HƯỚNG DẪN ĐƯA LÊN MẠNG

Mỗi bước có **lệnh chính xác** và **cách biết đã xong**. Làm tuần tự, đừng nhảy cóc.

---

## Bước 0 · Chuẩn bị máy (10 phút)

```bash
node -v          # cần ≥ 20
npm i -g firebase-tools
firebase login
```
**Xong khi:** `firebase projects:list` chạy được và hiện tài khoản của anh.

---

## Bước 1 · Chạy thử tại máy, CHƯA cần Firebase (15 phút)

```bash
cd web
npm install
npm test         # phải thấy 7 dòng "PASS · 0 FAIL"
npm run dev      # mở http://localhost:5173
```

**Xong khi:** cháu học được trọn một micro từ mở bài đến huy hiệu, và bấm "Sổ học" thấy tiến độ.

> Mốc này quan trọng hơn mọi bước sau. **Cho cháu học thử 3 bài trước khi dựng Firebase.**
> Nếu bài giảng chưa hấp dẫn thì sửa nội dung, đừng vội làm backend.

---

## Bước 2 · Tạo dự án Firebase (20 phút)

1. console.firebase.google.com → **Add project** → tên `toan-tu-duy`
2. Bật ba dịch vụ:
   - **Authentication** → Sign-in method → bật **Email/Password**
   - **Firestore Database** → Create database → **Production mode** → vùng **asia-southeast1**
   - **Hosting** → Get started
3. Project settings → General → mục "Your apps" → **Add app → Web** → sao chép cấu hình

```bash
cd web
cp .env.example .env.local     # rồi dán 6 giá trị vừa sao chép vào
firebase use --add             # chọn dự án vừa tạo
```

**Xong khi:** `cat .env.local` thấy đủ `VITE_FB_PROJECT_ID` và các khoá khác.

---

## Bước 3 · Đẩy luật bảo mật LÊN TRƯỚC KHI có dữ liệu thật (5 phút)

```bash
firebase deploy --only firestore:rules,firestore:indexes,storage
```

**Xong khi:** Firestore → Rules thấy đúng nội dung `firestore.rules`,
trong đó `attempts` có `allow update, delete: if false`.

> Đừng bao giờ để Firestore ở chế độ mở rồi tính sau. Dữ liệu học của trẻ là dữ liệu cá nhân.

---

## Bước 4 · Nạp chỉ mục nội dung (5 phút)

Cloud Function cần biết lịch ôn của từng bài mà không phải tải cả file bài học.

```bash
# tải khoá dịch vụ: Project settings → Service accounts → Generate new private key
export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
cd web && node tools/seed_content_index.mjs
```

**Xong khi:** in ra `đã nạp 168 bản ghi vào contentIndex`, và Firestore thấy collection `contentIndex`.

---

## Bước 5 · Triển khai Cloud Functions (10 phút)

```bash
cd web/functions && npm install && cd ..
firebase deploy --only functions
```

**Xong khi:** Console → Functions thấy đủ **năm** hàm (vùng asia-southeast1):

| Hàm | Khi nào chạy |
|---|---|
| `requestOtp` | người dùng bấm "Gửi mã cho tôi" |
| `verifyOtp` | người dùng nhập mã |
| `onAttempt` | mỗi lượt trả lời → cập nhật mức thạo |
| `onMicroDone` | học xong một bài → sinh thẻ ôn |
| `nightlyReport` | 21h00 — sổ học từng người |
| `nightlyTeacherBoard` | 21h15 — bảng toàn hệ thống cho giáo viên |

> Hai hàm OTP cần bốn bí mật `OTP_PEPPER`, `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` — đặt ở **bước 7a** trước khi triển khai,
> nếu không hàm sẽ triển khai được nhưng gửi mã thất bại.

---

## Bước 5b · Ba việc IAM mà `firebase deploy` KHÔNG tự làm

Tạo dự án bằng CLI thì ba thứ sau **không tự bật**, và mỗi thứ làm hỏng đăng nhập theo một
kiểu khác nhau. Triệu chứng ngoài màn hình đều giống hệt: *"Chưa gọi được máy chủ."*

**1 · Firebase Authentication chưa khởi tạo** → log báo `auth/configuration-not-found`

Bấm **Authentication → Get started** trong Console, hoặc chạy:

```bash
TOK=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.config/configstore/firebase-tools.json')))['tokens']['access_token'])")
curl -s -X POST -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  "https://identitytoolkit.googleapis.com/v2/projects/<DỰ_ÁN>/identityPlatform:initializeAuth" -d '{}'
curl -s -X PATCH -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  "https://identitytoolkit.googleapis.com/admin/v2/projects/<DỰ_ÁN>/config?updateMask=signIn.email.enabled,signIn.email.passwordRequired" \
  -d '{"signIn":{"email":{"enabled":true,"passwordRequired":true}}}'
```

**2 · Hàm không cho gọi khi chưa đăng nhập** → gọi thẳng trả về **403 Forbidden**

Hai hàm `requestOtp` và `verifyOtp` phải công khai — chính chúng là cửa đăng nhập, nên
không thể đòi đăng nhập trước. Bản thân hàm tự kiểm mã nên vẫn an toàn.

```bash
curl -s -X POST -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  "https://run.googleapis.com/v2/projects/<DỰ_ÁN>/locations/asia-southeast1/services/verifyotp:setIamPolicy" \
  -d '{"policy":{"bindings":[{"role":"roles/run.invoker","members":["allUsers"]}]}}'
```

> Tên dịch vụ Cloud Run viết **thường hết**: `verifyotp`, không phải `verifyOtp`.

**3 · Service account không tự ký được token** → log báo `iam.serviceAccounts.signBlob denied`

`createCustomToken` cần service account tự cấp quyền cho chính mình:

```bash
SA=<SỐ_DỰ_ÁN>-compute@developer.gserviceaccount.com
# lấy policy hiện tại, thêm binding rồi đặt lại (đừng ghi đè trắng)
curl -s -X POST -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  "https://iam.googleapis.com/v1/projects/<DỰ_ÁN>/serviceAccounts/$SA:setIamPolicy" \
  -d '{"policy":{"bindings":[{"role":"roles/iam.serviceAccountTokenCreator","members":["serviceAccount:'$SA'"]}]}}'
```

Quyền IAM cần khoảng **một phút** để lan truyền — thử ngay sau khi cấp vẫn có thể lỗi.

**Cách soi lỗi thật:** `firebase functions:log` CẮT MẤT nội dung lỗi. Lấy thẳng từ Cloud Logging:

```bash
curl -s -X POST -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  "https://logging.googleapis.com/v2/entries:list" -d '{
    "resourceNames":["projects/<DỰ_ÁN>"],
    "filter":"resource.labels.service_name=\"verifyotp\" AND severity>=ERROR",
    "orderBy":"timestamp desc","pageSize":3}'
```

---

## Bước 6 · Đưa trang web lên mạng (10 phút)

```bash
cd web
npm run build          # tạo thư mục dist/ (đã gồm 16 MB nội dung)
firebase deploy --only hosting
```

**Xong khi:** mở địa chỉ `https://<project>.web.app` học được trên điện thoại.

> Lần build đầu hơi lâu vì phải chép 672 ảnh. Cache đã đặt 7 ngày trong `firebase.json`
> nên lần thứ hai vào rất nhanh.

---

## Bước 7 · Tài khoản và vai trò (10 phút)

**Không có màn đăng ký.** Người dùng nhập email → hệ thống gửi mã 6 số vào hộp thư →
nhập mã là vào. Chưa có hồ sơ thì máy chủ lập luôn. Một tài khoản là một học sinh —
phụ huynh và con dùng chung.

**Ba vai trò**, đều nằm trong `users/{uid}.role` VÀ trong custom claim của token:

| Vai trò | Vào bằng | Thấy gì |
|---|---|---|
| `learner` | mã OTP qua email | dữ liệu của chính mình |
| `teacher` | mã OTP qua email | kết quả của **toàn bộ** học sinh |
| `admin` | email + mật khẩu | toàn quyền |

**7a · Đặt bốn bí mật máy chủ (bắt buộc)**

```bash
firebase functions:secrets:set OTP_PEPPER   # openssl rand -base64 32
firebase functions:secrets:set SMTP_HOST    # smtp.gmail.com
firebase functions:secrets:set SMTP_USER    # địa chỉ Gmail dùng để gửi
firebase functions:secrets:set SMTP_PASS    # mật khẩu ỨNG DỤNG 16 ký tự
```

> Lệnh này **cần bàn phím thật**. Chạy qua công cụ tự động hoặc script không tương tác thì
> nó nhận chuỗi rỗng và báo `Secret Payload cannot be empty`. Mở Terminal mà chạy.

**Vì sao để rời bốn mảnh chứ không gộp thành một URL**: tên đăng nhập là địa chỉ email, mà
email có dấu `@`. Nhét vào giữa URL kiểu `smtps://ten@mien.vn:matkhau@smtp.gmail.com:465`
thì bộ đọc URL cắt nhầm chỗ — gửi mail hỏng mà không báo lỗi rõ ràng. Muốn đúng phải nhớ
đổi `@` thành `%40`. Để rời thì dán sao dùng vậy.

`OTP_PEPPER` đổi lúc nào cũng được — **mọi mã đang chờ sẽ hết hiệu lực**, người dùng chỉ
cần xin mã mới.

Gmail phải dùng **mật khẩu ứng dụng** (`myaccount.google.com/apppasswords`, cần bật xác
minh 2 bước trước), không dùng mật khẩu thường. Mật khẩu ứng dụng hiện theo nhóm 4 ký tự
có dấu cách — dán cả dấu cách cũng được, hàm tự bỏ.

Chưa đặt `SMTP_USER`/`SMTP_PASS` thì hàm vẫn chạy nhưng **in mã ra log thay vì gửi mail** —
tiện lúc chạy thử, **tuyệt đối không để vậy khi chạy thật**.

**7b · Phong một tài khoản làm giáo viên**

Cô đăng nhập một lần bằng OTP để hệ thống lập hồ sơ. Rồi sửa `users/{uid}.role` thành
`teacher` trong Console, và đặt custom claim:

```bash
# chạy một lần bằng Admin SDK
node -e "require('firebase-admin').initializeApp(); \
  require('firebase-admin').auth().setCustomUserClaims('<uid>', {role:'teacher'})"
```

> Phải đặt **cả hai chỗ**. Luật bảo mật đọc vai trò từ **token**, không đọc từ Firestore —
> vì người dùng ghi được vào `users/{uid}` của mình, nên tin vào trường `role` ở đó thì
> ai cũng tự phong mình làm giáo viên rồi đọc kết quả cả trường. Sửa xong cô phải
> đăng xuất rồi đăng nhập lại thì token mới mang vai trò mới.

**7c · Tạo admin**

Authentication → Add user (email + mật khẩu) → đặt `users/{uid}.role = 'admin'` và custom
claim `role=admin` như trên. Admin **không đi đường OTP**, vào bằng mật khẩu.

**Xong khi:** nhập email ở màn đăng nhập, nhận được mã trong hộp thư, nhập mã vào được,
và Firestore hiện `users/{uid}` mới.

**Ai đọc được gì**

| | Chính chủ | Giáo viên | Admin | Người ngoài |
|---|---|---|---|---|
| `users/{uid}` | đọc, sửa tên | **đọc** | toàn quyền | cấm |
| `users/{uid}.role` | **cấm sửa** | cấm | sửa được | cấm |
| `attempts` nhật ký từng câu | đọc, **thêm** | **đọc** | đọc | cấm |
| `progress`, `mastery` | đọc, ghi | **đọc** | đọc | cấm |
| `report/{uid}` sổ học | đọc | **đọc** | đọc | cấm |
| `teacherBoard/global` | cấm | **đọc** | đọc | cấm |
| `reviewQueue` việc riêng | đọc, ghi | cấm | đọc | cấm |
| `otpCodes` | cấm | cấm | **cấm** | cấm |

Nhật ký `attempts` **bất biến với tất cả**: `allow update, delete: if false`. Không ai
sửa được điểm đã ghi — kể cả admin.

`otpCodes` cấm cả admin: mở quyền đọc là lộ bản băm, mở quyền ghi là tự đặt mã cho
tài khoản người khác. Chỉ Cloud Function qua Admin SDK mới đụng tới.

---

## Bước 8 · Kiểm thật ba tình huống (15 phút)

| Kiểm | Cách làm | Phải thấy |
|---|---|---|
| **Mất mạng** | Bật chế độ máy bay giữa bài, học nốt rồi bật mạng lại | Bài không mất; sau vài giây `attempts` xuất hiện đủ trên Firestore |
| **Riêng tư** | Đăng nhập bằng email thứ hai, thử đọc `attempts` của tài khoản đầu | Bị từ chối (permission denied) |
| **Không tự phong** | Đăng nhập thường, thử sửa `users/{uid}.role` thành `teacher` | Bị từ chối — đây là chốt chặn quan trọng nhất |
| **Mã OTP** | Nhập sai mã 5 lần liên tiếp | Lần thứ 5 báo "nhập sai quá nhiều lần", mã bị huỷ, phải xin mã mới |
| **Sổ đêm** | Console → Functions → `nightlyReport` → Run now | `report/{uid}` được tạo với số phút, tỉ lệ đúng, bẫy hay sập |
| **Bảng cô** | Console → Functions → `nightlyTeacherBoard` → Run now | `teacherBoard/global` có danh sách học sinh và bẫy nhiều em sập nhất |

---

## Chạy giả lập khi phát triển (không đụng dữ liệu thật)

```bash
cd web && npm run emulators        # Auth 9099 · Firestore 8080 · Functions 5001 · UI 4000
```

---

## Chi phí ước lượng

Một phiên học 15 phút ≈ **30–40 lượt ghi** + vài lượt đọc.
Một con học đều mỗi ngày ≈ **1.200 lượt ghi/tháng** — nằm gọn trong hạn mức miễn phí của Firebase.
Nội dung tĩnh nằm ở Hosting nên **không tính vào Firestore**.
