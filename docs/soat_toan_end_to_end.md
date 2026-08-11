# Soát MÔN TOÁN end-to-end sau khi tách hai môn

Lập 2026-08-11, ngay sau `05f81e8` (tách frontend về ba vùng).

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

## H · Cần ĐĂNG NHẬP — bác làm, cháu không nhập được mã

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
