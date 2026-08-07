# CHECKLIST NGHIỆM THU

Ký vào từng dòng trước khi cho con dùng thật. Thứ tự có chủ ý: **con học được** trước,
**dữ liệu đúng** sau, **lên mạng** cuối cùng.

---

## A · Nội dung (làm trước, không cần lập trình)

- [ ] Mở `web/public/content/lessons/DL_KSN5Q1_B49_M1.json` — đọc thấy đủ 16 khối, không thiếu trường
- [ ] Mở 10 hình bất kỳ trong `web/public/content/figures/` — chữ không tràn, số khớp đề bài
- [ ] Soi 3 hình của chương con đang học kỹ hơn: **hình và phép tính có mâu thuẫn nhau không?**
- [ ] Đọc lướt 5 màn GIẢNG trên app — lời giảng có dễ hiểu với con anh không

> Đây là việc **không ai làm thay được**. Máy kiểm được bố cục, không kiểm được "con có hiểu không".

---

## B · Ứng dụng học

- [ ] `npm test` — 5 dòng, tất cả `0 FAIL`
- [ ] Học trọn một micro: mở bài → giảng → bài mẫu → luyện → sát hạch → huy hiệu
- [ ] Ở phần luyện: cố tình sai 3 lần → phải hiện gợi ý 1, gợi ý 2, rồi mở đáp án
- [ ] Ở phần sát hạch: **cố tình sai câu bẫy** nhưng đúng hai câu kia → phải **KHÔNG đạt**
- [ ] Về trang chính: bài kế tiếp phải còn **khoá 🔒**
- [ ] Làm lại và đúng câu bẫy → bài kế tiếp mở ra
- [ ] Bấm "Sổ học" → thấy tiến độ 14 chương và danh sách bài chưa qua câu bẫy
- [ ] Học hết một chương → nút kỳ sát hạch chương chuyển sang màu đỏ (mở)
- [ ] Trong kỳ sát hạch: tự chấm sai một câu → bảng tự soi hiện đúng micro cần ôn

---

## C · Trên điện thoại (nơi con thật sự học)

- [ ] Mở trên điện thoại của con — chữ đủ to, nút bấm không hụt tay
- [ ] Xoay ngang / dọc không vỡ bố cục
- [ ] Bàn phím số hiện ra khi bấm vào ô nhập đáp án
- [ ] Nhập `0,785` (dấu phẩy Việt Nam) — phải chấm đúng
- [ ] Ảnh tải nhanh trên 4G (lần đầu ~2 giây/bài)

---

## D · Dữ liệu và bảo mật (sau khi nối Firebase)

- [ ] Firestore Rules đã đẩy, `attempts` có `allow update, delete: if false`
- [ ] Học một micro → Firestore có ~10–15 document `attempts` với đủ `tries`, `ms`, `mustPass`
- [ ] `mastery/{learnerId}/units/...` có `p` tăng dần sau mỗi câu đúng
- [ ] Bật chế độ máy bay giữa bài → học nốt được → bật mạng lại → dữ liệu tự lên, **không mất bài**
- [ ] Tài khoản bố mẹ B **không đọc được** dữ liệu con của tài khoản A
- [ ] Chạy tay `nightlyParentReport` → `parentReport/{learnerId}` được tạo

---

## E · Một tuần thí điểm với con

- [ ] Con học đều 15 phút/ngày trong 7 ngày → có 7 phiên dữ liệu thật
- [ ] Mở `attempts`, tìm câu sai nhiều nhất → **bẫy nào cần giảng lại**
- [ ] So thời gian thật mỗi micro với `durationMinutes` khai trong dữ liệu
- [ ] Hỏi con đúng ba câu:
  - chỗ nào **chán**?
  - chỗ nào **khó hiểu**?
  - **hình nào con thích nhất**?

> Chỉ sau mốc này mới mở rộng sang Quý 2 hoặc lớp 4. Sửa theo phản hồi thật của con,
> đừng sửa theo phỏng đoán.

---

## Những chỗ đã biết là chưa xong

- [ ] Nút "Đề khác" **ẩn** ở hầu hết câu — metadata `generator` viết bằng văn xuôi,
      chỉ 1/181 câu máy dùng được. Nâng cấp metadata thì nút sẽ hiện.
- [ ] Các màn tương tác đặc thù (kéo thả, đếm ô) chưa làm — hiện là hình tĩnh + câu hỏi.
- [ ] Video chưa dựng. Với kiến trúc hiện tại nên **quay màn hình chính các component này**
      thay vì làm pipeline riêng.
- [ ] 36/1.141 câu là lời giải thích dài → để **con tự đối chiếu**, máy không chấm.
      Đây là lựa chọn có chủ ý, không phải thiếu sót.
