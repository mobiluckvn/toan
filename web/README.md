# Trang học tập Toán Tư Duy lớp 5 · Quý 1

## Chạy thử
```bash
npm install
npm run dev          # http://localhost:5173
npm test             # kiểm lõi logic trên dữ liệu thật của 168 micro
```

## Cấu trúc
```
src/lib/flow.js       lõi: dựng dòng chảy 5 chặng · chấm bài · luật đạt   (JS thuần, có test)
src/lib/content.js    nạp DL json + ảnh từ thư mục tĩnh (không cần API)
src/components/
  LessonPlayer.jsx    khung + thanh chặng + tiến độ
  StepView.jsx        điều phối từng loại bước
  AnswerInput.jsx     ô trả lời dùng chung (số · nhiều phần · trắc nghiệm · tự đối chiếu)
  SampleCard.jsx      ca mẫu — con nghĩ trước, bấm mới mở lời giải
  WorkedExample.jsx   ví dụ dẫn dắt — đi từng nhịp, có câu hỏi xen giữa
  Figure.jsx          ảnh + chú thích
  PracticeItem.jsx    luyện tập: gợi ý 2 tầng, mở đáp án sau 3 lần
  AssessItem.jsx      sát hạch: một lần trả lời, có nhãn CÂU BẮT BUỘC ĐÚNG
  FinaleCard.jsx      huy hiệu · điểm · thẻ ôn · sổ phụ huynh
  Home.jsx            trang chính: 14 chương, tiến độ, nút "Học tiếp"
  ExamPlayer.jsx      kỳ sát hạch chương: 15 câu tự soi + bảng chẩn đoán micro
src/lib/progress.js   tiến độ · luật mở khoá · huy hiệu   (localStorage, có test)
src/lib/sync.js       dựng attempts · hàng đợi ngoại tuyến (JS thuần, có test)
src/lib/firebase.js   lớp bọc SDK: offline persistence · ghi attempts · đọc lịch sử
firestore.rules       luật bảo mật: nhật ký BẤT BIẾN, bố mẹ chỉ thấy con mình
firestore.indexes.json chỉ mục cho truy vấn lịch sử & bẫy hay sập
firebase.json         hosting + cache nội dung 7 ngày + emulators
functions/src/bkt.js       BKT thuần toán (có test)
functions/src/schedule.js  hàng đợi ôn tập Leitner (có test)
functions/index.js         onAttempt → cập nhật mức thạo · onMicroDone → sinh thẻ ôn
tools/seed_content_index.mjs  nạp chỉ mục 168 micro lên Firestore
src/lib/adaptive.js        chính sách phiên học (có test)
functions/src/report.js    dựng sổ phụ huynh (có test)
src/components/ParentReport.jsx  màn Sổ học của con
public/content/       168 bài học + 672 hình + 14 kỳ sát hạch  → deploy thẳng lên Hosting/CDN
test/                 102 tệp · 2 764 phép kiểm — lõi hai môn, soi 100% câu hỏi & mục tiêu, mở khoá & nhớ chỗ dở, offline & sang tên hàng đợi, BKT/ôn tập, sổ học, bảng giáo viên, đăng nhập OTP, và 35 tệp riêng cho Tiếng Anh (cô giáo máy, kế hoạch buổi, trí nhớ, phụ đạo, phân xử lượt nói mơ hồ, vốn từ, vân tay prompt, luật Firestore)
```

## Vì sao không cần backend
Toàn bộ nội dung là **file tĩnh**: bài học JSON + hình PNG sinh sẵn.
Không gọi API model nào lúc chạy → không phí, không phụ thuộc mạng, mở offline được sau lần tải đầu.
Firebase chỉ dùng ở **giai đoạn C** để lưu lịch sử học, không dùng cho nội dung.

## Trạng thái
- [x] B1 · khung dự án · lõi logic có test · thanh chặng · mở bài / tình huống / giảng / thần chú
- [x] B2 · chặng BÀI MẪU: ca mẫu nghĩ-trước-rồi-mở · ví dụ dẫn dắt đi từng nhịp có câu hỏi xen giữa · AnswerInput dùng chung
- [x] B3 · LUYỆN TẬP (gợi ý 2 tầng · sai 3 lần mở đáp án · lối quay lại nguyên tắc) · SÁT HẠCH (mustPass · luật ≥ n/m) · trang kết + sổ phụ huynh
- [x] B4 · trang chính 14 chương · luật mở khoá theo cổng mustPass · 14 kỳ sát hạch chương với bảng tự soi · huy hiệu · lưu tiến độ tại máy

## Ghi chú trung thực về "sinh đề biến thể"
Dữ liệu có 181 câu kèm `generator`, nhưng **ràng buộc và quy tắc đáp án viết bằng văn xuôi**
("số tự nhiên 4 chữ số, có đúng một chữ số 0"), nên máy chỉ dùng được **1/181**.
`makeVariant` trả `null` khi metadata không đủ và giao diện **ẩn nút "Đề khác"** — không sinh đề bừa.
Muốn dùng thật thì phải nâng cấp metadata generator (ràng buộc thành khoảng số, answerRule thành biểu thức).
Trước mắt 1.141 câu cố định đã đủ cho trọn Quý 1.

## Giai đoạn C1 — dữ liệu học trên Firebase

**Bốn quyết định đáng chú ý**

1. **Nhật ký bất biến.** Luật bảo mật cho phép `create` nhưng cấm `update`/`delete` với `attempts`.
   Bằng chứng học tập của con không ai sửa được, kể cả tài khoản bố mẹ.
2. **Ghi lượt thô, không chỉ ghi điểm.** Mỗi câu trả lời một dòng, kèm `tries`, `hintsUsed`, `ms`, `mustPass`.
   Nhờ vậy sau này trả lời được "bẫy nào hay sập nhất", "câu nào con làm 40 giây mà vẫn sai".
   Chi phí: một phiên 15 phút ≈ 30–40 lượt ghi.
3. **Offline là mặc định.** `persistentLocalCache` + hàng đợi cục bộ. Mất mạng giữa chừng thì
   phần chưa gửi được giữ nguyên, nối mạng lại gửi nốt — đã kiểm bằng test mô phỏng đứt mạng.
4. **BKT chỉ Cloud Function ghi.** `mastery/*` cấm ghi từ client, tránh sửa mức thạo từ trình duyệt.

**Chạy thử không cần dự án thật**
```bash
npm run emulators           # Auth + Firestore giả lập tại máy
```
Chưa cấu hình Firebase thì app **vẫn học được bình thường** — dữ liệu nằm trong hàng đợi cục bộ.

## Giai đoạn C2 — mức thạo (BKT) & hàng đợi ôn tập

**Hiệu chỉnh BKT bằng thực nghiệm, không lấy tham số sách vở.**
Bộ tham số đầu tiên (L0 .25 · guess .20) khiến **chỉ 2 câu đúng đã tuyên "thạo"** và một câu sai
vẫn không tụt dưới ngưỡng — quá dễ dãi với trẻ. Sau khi hiệu chỉnh (L0 .10 · T .08 · slip .10 · guess .30):

* cần **4 câu đúng liên tiếp** mới đạt ngưỡng thạo 0,85
* **một câu sai** sau đó kéo tụt xuống dưới ngưỡng
* làm đúng lại thì thạo trở lại sau 1 câu

**Câu bẫy có trọng số riêng** (`guess` .15 · `slip` .06): đúng câu bẫy tăng mạnh hơn câu thường,
sai câu bẫy tụt sâu hơn — vì bẫy mới là thứ bài học dạy.

**Hàng đợi ôn tập** đọc thẳng `spacedReview.schedule` của từng bài (mốc +1 / +3 / +7 ngày,
504 thẻ cho 168 micro), rồi chạy Leitner: ôn đúng lên hộp (1·3·7·14·30 ngày), ôn sai về hộp 0.

## Giai đoạn C3 — thích ứng & sổ phụ huynh

**Thứ tự ưu tiên trong một phiên** (`planSession`)
1. **Thẻ ôn đến hạn** (tối đa 3, quá hạn lâu nhất lên trước) — kiến thức cũ sắp quên
   quan trọng hơn kiến thức mới.
2. **Kỳ sát hạch chương đang chờ** — học hết chương thì thi lấy huy hiệu, không học lấn sang chương sau.
3. **Micro tiếp theo**: bài đầu tiên chưa thạo và đã mở khoá.
   Bài **đã đạt nhưng mức thạo tụt dưới 0,85** vẫn được gợi ý ôn lại (con quên thì học lại, không bỏ qua).
4. **Mức luyện vào bài** theo mức thạo: `< 0,4` khởi động · `0,4–0,7` cơ bản · `> 0,7` thử thách —
   không bắt bé đang giỏi làm lại câu khởi động.

**Sổ phụ huynh** do Cloud Function tổng hợp **21 giờ mỗi đêm** thành MỘT document
(bố mẹ đọc 1 lần thay vì quét hàng nghìn `attempts`): số phút học, số buổi, tỉ lệ đúng,
**bẫy hay sập nhất**, **câu làm lâu mà vẫn sai** (dấu hiệu bế tắc chứ không phải ẩu),
kèm gợi ý "chơi cùng con" lấy từ `parentNote` của đúng bài đang yếu.

Màn **Sổ học** chạy được cả khi **chưa nối Firebase** — khi ấy tính tại máy từ tiến độ cục bộ.
