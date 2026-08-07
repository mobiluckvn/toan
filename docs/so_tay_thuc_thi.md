# SỔ TAY THỰC THI — TRANG HỌC TẬP THÍCH ỨNG TOÁN TƯ DUY LỚP 5
**MOBILUCK · code247.ai** · Từ dữ liệu km_v1_23 → sản phẩm con dùng được · Phiên bản 1.0 · 03/08/2026

> Cách đọc: mỗi bước có **① Mục tiêu · ② Việc làm · ③ Nghiệm thu (làm sao biết đã xong)**.
> Cột "Ai" ghi rõ việc nào anh làm, việc nào giao cho tôi (Claude) hoặc cho agent.
> Tổng thời gian ước tính: **4–6 tuần** làm buổi tối, hoặc **12–15 ngày** làm toàn thời gian.

---

## GIAI ĐOẠN 0 · CHUẨN BỊ NỀN (nửa ngày)

### Bước 0.1 — Quyết định 4 điểm trước khi gõ dòng code nào
| Quyết định | Gợi ý của tôi | Vì sao |
|---|---|---|
| Tên model Gemini | bản Flash mới nhất anh đang dùng | sinh figureSpec (JSON) — không cần model mạnh |
| Vùng Firebase | `asia-southeast1` (Singapore) | gần VN nhất, độ trễ ~30 ms |
| Cách đăng nhập của trẻ | **Bố mẹ có tài khoản → tạo nhiều hồ sơ con** (không cho trẻ tự đăng ký) | an toàn trẻ em, đúng luật, và bố mẹ xem được sổ học |
| Nền tảng web | React + TypeScript + Vite + Tailwind | bản mẫu HTML đã có sẵn, chuyển sang React nhanh |

**Nghiệm thu:** viết 4 dòng quyết định này vào `docs/DECISIONS.md` trong repo.

### Bước 0.2 — Dựng repo
```bash
mkdir toan-tu-duy && cd toan-tu-duy && git init
mkdir -p data/lessons data/figures figforge web functions tools docs
# chép dữ liệu đã bàn giao
cp .../DL_KSN5Q1_B*_M*.json      data/lessons/
cp .../km_v1_23.json             data/
cp .../MANIFEST_Q1.json          data/
unzip figforge_v1.zip -d figforge/
```
**Nghiệm thu:** `ls data/lessons | wc -l` → **168**.

### Bước 0.3 — Tạo dự án Firebase
1. console.firebase.google.com → **Add project** → tên `toan-tu-duy`
2. Bật: **Authentication** (Email/Password) · **Firestore** (chế độ *production*, vùng asia-southeast1) · **Storage** · **Hosting**
3. Máy local: `npm i -g firebase-tools && firebase login && firebase init`
   (chọn Firestore, Functions, Hosting, Storage — Functions dùng **TypeScript**)

**Nghiệm thu:** `firebase projects:list` thấy dự án; `firebase deploy --only hosting` đẩy được trang trắng.

---

## GIAI ĐOẠN 1 · SINH 500 HÌNH (3–5 ngày) — việc nặng nhất, làm trước

### Bước 1.1 — Thêm trường `figureSpec` vào schema micro *(Claude)*
Cập nhật `micro_lesson_schema.md` lên **v2.1**: mỗi micro có `payload.figureSpec[]` gồm `{id, archetype, params, caption, usedIn[]}` theo `figforge/schema.json`.
**Nghiệm thu:** schema có mục figureSpec + ví dụ đầy đủ của B49.M1.

### Bước 1.2 — Viết CLI render *(Claude)*
`figforge/render.py`:
```bash
python figforge/render.py --lesson data/lessons/DL_KSN5Q1_B49_M1.json --out data/figures/
# → data/figures/DL_KSN5Q1_B49_M1_F1.png ...
```
**Nghiệm thu:** chạy trên B49.M1 ra đúng số hình khai trong figureSpec, mở xem thấy đẹp.

### Bước 1.3 — Viết tool sinh figureSpec bằng Gemini *(Claude)*
`tools/gen_figurespec.py` — prompt gồm 3 phần: (a) `figforge/schema.json` nguyên văn, (b) `knowledgeCore` + `lecture.screens` của micro, (c) chỉ thị "chọn 2–4 hình, CHỈ trả JSON, chỉ dùng 12 archetype".
Bắt buộc `--dry-run` in JSON ra màn hình trước khi ghi đè.
**Nghiệm thu:** chạy cho 3 micro bất kỳ, JSON đều pass `validate_figurespec.py` (bước sau).

### Bước 1.4 — Viết validator + auto-QC *(Claude)*
`tools/validate_figurespec.py` kiểm: archetype nằm trong 12 · params đủ khoá bắt buộc · độ dài chuỗi ≤ ngưỡng (chống chữ tràn) · số hình 2–4 · `usedIn` trỏ tới block có thật.
`tools/qc_figures.py` kiểm ảnh đã render: đúng bảng màu · không có vùng trắng > 40% · kích thước đúng.
**Nghiệm thu:** cố tình sửa 1 spec sai → validator báo đúng lỗi, không cho render.

### Bước 1.5 — Chạy thử một chương rồi mới chạy đại trà *(anh duyệt)*
```bash
python tools/gen_figurespec.py --chapter 13        # 12 micro
python figforge/render.py --chapter 13 --out data/figures/
python tools/contact_sheet.py --chapter 13         # gộp ~36 hình thành 3 trang A4 để duyệt nhanh
```
Anh mở contact sheet, đánh dấu hình nào chưa đạt → tôi sửa **renderer** (không sửa từng hình).
**Nghiệm thu:** ≥ 80% hình của chương 13 đạt ngay lần đầu. Chưa đạt thì sửa renderer rồi render lại cả chương — đây chính là lúc đầu tư sửa có lãi nhất.

### Bước 1.6 — Chạy đại trà 168 micro
```bash
python tools/gen_figurespec.py --all && python figforge/render.py --all
python tools/contact_sheet.py --all      # ~14 trang duyệt
```
**Nghiệm thu:** `data/figures/` có ~500 PNG + `figure_manifest.json` (id → file + sha256). Anh duyệt xong toàn bộ.

> **Mẹo tiết kiệm:** duyệt bằng contact sheet nhanh hơn duyệt từng ảnh gấp 10 lần. Mỗi trang 12 hình, nhìn 30 giây là biết cái nào lệch.

---

## GIAI ĐOẠN 2 · TRANG HỌC TẬP (5–7 ngày)

### Bước 2.1 — Khởi tạo web *(anh chạy, Claude viết code)*
```bash
cd web && npm create vite@latest . -- --template react-ts
npm i firebase tailwindcss @tailwindcss/vite
```
Nạp brand vào `tailwind.config`: navy #0C3B70 · teal #1FC3A6 · gold #F8B942 · red #C0392B.

### Bước 2.2 — Chuyển bản mẫu HTML thành component React *(Claude)*
Dùng `hoc_thu_B49_M1.html` làm **đặc tả sống**. Tách thành:
```
LessonPlayer.tsx      dựng flow 5 chặng từ DL json
├─ IntroCard          mở bài + mục tiêu + thần chú
├─ TeachBlock         K-statement + hình + giảng giải   (chặng GIẢNG)
├─ CheckPoint         câu chốt nhanh
├─ SampleCard         ca mẫu: nghĩ trước → mở lời giải  (chặng BÀI MẪU)
├─ WorkedExample      từng bước có hỏi xen giữa
├─ PracticeItem       3 mức + hint 2 tầng + đáp án sau 3 lần
├─ AssessItem         mustPass + luật ≥2/3
└─ FinaleCard         huy hiệu + thẻ ôn + sổ phụ huynh
```
**Nghiệm thu:** mở B49.M1 trên web thấy **giống hệt** bản mẫu HTML; đổi sang B50.M2 vẫn chạy đúng mà không sửa code.

### Bước 2.3 — Đưa nội dung lên hosting
168 file DL json + 500 PNG đẩy lên **Hosting** (không phải Firestore — rẻ hơn nhiều và có CDN).
**Nghiệm thu:** mở bài trên 4G tải xong < 2 giây.

### Bước 2.4 — Chạy thử với cháu, KHÔNG có Firebase
Đây là mốc quan trọng: **con học được trọn một chương** trước khi mình động đến dữ liệu.
**Nghiệm thu:** cháu học 3 micro liên tiếp không cần anh giải thích gì thêm.

---

## GIAI ĐOẠN 3 · FIREBASE — LỊCH SỬ HỌC (3–5 ngày)

### Bước 3.1 — Cấu trúc Firestore
```
parents/{uid}                       email, tên, danh sách learners
learners/{learnerId}                tên con, lớp, parentUid, avatar
attempts/{attemptId}                learnerId, microId, itemId, phase,
                                    correct, tries, hintsUsed, ms, ts
mastery/{learnerId}/units/{bktUnit} p, nAttempts, lastSeen
progress/{learnerId}/micros/{microId}  state, score, mustPassOK, badge, doneAt
reviewQueue/{learnerId}/cards/{cardId} microId, dueAt, box
parentReport/{learnerId}            bản tổng hợp do Function ghi hằng đêm
```

### Bước 3.2 — Luật bảo mật (viết trước khi ghi dữ liệu thật)
```javascript
match /learners/{id} {
  allow read, write: if request.auth != null
    && resource.data.parentUid == request.auth.uid;
}
match /attempts/{id} {
  allow create: if request.auth != null
    && request.resource.data.learnerId in parentLearners();
  allow update, delete: if false;      // nhật ký bất biến
}
```
**Nghiệm thu:** `firebase emulators:start` + test: tài khoản A **không** đọc được dữ liệu con của tài khoản B.

### Bước 3.3 — Bật offline persistence *(bắt buộc, đừng bỏ qua)*
```typescript
initializeFirestore(app, { localCache: persistentLocalCache() });
```
**Nghiệm thu:** tắt wifi giữa bài → con vẫn học hết bài; bật lại wifi → dữ liệu tự lên.

### Bước 3.4 — Ghi attempts
Mỗi câu trả lời ghi 1 document. Ghi theo lô cuối mỗi chặng (dùng `writeBatch`) để tiết kiệm.
**Nghiệm thu:** học xong 1 micro → Firestore có ~10–15 attempts đúng nội dung.

### Bước 3.5 — Cloud Function cập nhật BKT
`functions/src/onAttempt.ts` — trigger `onDocumentCreated('attempts/{id}')`:
```
slip=0.10  guess=0.20  T=0.15   (ngưỡng thạo 0.85)
đúng: p' = p(1−slip) / [p(1−slip) + (1−p)·guess]
sai : p' = p·slip     / [p·slip   + (1−p)(1−guess)]
p_new = p' + (1−p')·T
```
**Nghiệm thu:** trả lời đúng 3 câu liên tiếp một unit → `mastery.p` vượt 0,85.

### Bước 3.6 — Hàng đợi ôn tập
Khi micro hoàn thành, đọc `spacedReview.schedule` (+1/+3/+7 ngày) → tạo card trong `reviewQueue`.
**Nghiệm thu:** sửa tay `dueAt` về hôm qua → mở app thấy thẻ ôn hiện đầu phiên.

### Bước 3.7 — Sổ phụ huynh
Function chạy 21h hằng đêm gộp attempts trong ngày → ghi `parentReport/{learnerId}`: số phút học, số micro xong, bẫy hay sập, gợi ý "chơi cùng con" lấy từ `parentNote.homeActivity`.
**Nghiệm thu:** bố mẹ mở tab Sổ học → **1 lần đọc Firestore** ra đủ báo cáo.

---

## GIAI ĐOẠN 4 · ADAPTIVE (2–3 ngày)

### Bước 4.1 — Chính sách chọn bài
`web/src/adaptive/policy.ts`:
1. Mở phiên: lấy 1–3 thẻ `reviewQueue` đến hạn
2. Chọn micro đầu tiên có `mastery.p < 0.85` **và** micro trước đã `mustPassOK`
3. Trong micro: `p < 0.4` → bắt đầu warmup · `0.4–0.7` → standard · `> 0.7` → challenge
4. Đúng 2 câu liên tiếp → lên mức (theo `adaptiveRules` có sẵn trong dữ liệu)

### Bước 4.2 — Sinh đề biến thể
Làm lại lần 2 → dùng `generator.template` + `answerRule` sinh số mới (181 câu đã có generator).
**Nghiệm thu:** làm lại B49.M1 hai lần thấy số khác nhau, đáp án vẫn chấm đúng.

### Bước 4.3 — Cổng mustPass
`mustPassOK = false` thì **khoá micro sau** dù `p` cao. Đây là điểm quan trọng nhất: bẫy mới là thứ bài dạy.
**Nghiệm thu:** cố tình sai câu bẫy nhưng đúng 2 câu kia → không mở được micro tiếp theo.

---

## GIAI ĐOẠN 5 · THÍ ĐIỂM & ĐO (1 tuần)

| Việc | Nghiệm thu |
|---|---|
| Cháu học đều 15 phút/ngày trong 1 tuần | 7 phiên có dữ liệu thật |
| Xem `attempts` tìm câu sai nhiều nhất | biết bẫy nào cần giảng lại |
| Đo thời gian trung bình mỗi micro | so với `durationMinutes` khai trong dữ liệu |
| Hỏi cháu 3 câu: chỗ nào chán · chỗ nào khó hiểu · hình nào thích | sửa đúng chỗ, không đoán |

**Chỉ sau mốc này mới mở rộng** sang Quý 2 / lớp 4 / video.

---

## THỨ TỰ ƯU TIÊN NẾU THIẾU THỜI GIAN

Nếu chỉ có 1 tuần, làm đúng 3 việc này là con đã học được thật:
1. **Giai đoạn 1** — sinh hình cho 1 chương (12 micro)
2. **Giai đoạn 2 bước 2.2** — LessonPlayer đọc DL json
3. **Giai đoạn 3 bước 3.3 + 3.4** — offline + ghi attempts

Bỏ tạm được: BKT (dùng luật đơn giản "chưa đạt thì học lại"), sổ phụ huynh, adaptive nâng cao.

---

## VIỆC ANH LÀM vs VIỆC TÔI LÀM

| Anh | Tôi (Claude) |
|---|---|
| 4 quyết định ở bước 0.1 | toàn bộ code: renderer, tools, React, Functions |
| Tạo dự án Firebase, chạy `firebase init` | schema Firestore, luật bảo mật, hàm BKT |
| **Duyệt contact sheet hình** (không ai thay được) | sinh figureSpec, render, auto-QC |
| Cho cháu học thử + kể lại phản ứng | sửa theo phản hồi thật |
| Quyết định khi hai phương án ngang nhau | trình bày rõ đánh đổi để anh quyết |

---
*Nguyên tắc xuyên suốt: mỗi giai đoạn phải kết thúc bằng thứ CON DÙNG ĐƯỢC, không phải bằng thứ chạy được trên máy.*
