# Kế hoạch hoàn thiện & bảo vệ Luận văn Thạc sĩ CNTT – đợt 12/2026 (SoICT – HUST)

> File bàn giao cho Claude (Desktop/Code) làm tiếp. Cập nhật lần cuối: 22/11/2026.
> Nguồn: https://soict.hust.edu.vn/ke-hoach-nop-ho-so-va-bao-ve-luan-van-cao-hoc-dot-thang-12-2026.html
> Đánh dấu `[x]` khi xong và ghi ngày bên cạnh.

## Thông tin cần bổ sung (chưa biết)
- [x] 22/11/2026 Cơ sở đào tạo của luận văn này: **Đại học Bách khoa Hà Nội** (tác giả học đồng thời ở Bách khoa và PTIT)
- [x] 22/11/2026 Nguyên tắc: **tất cả tham số nằm trong cấu hình** (bảng `nguong` + màn hình) — xem `YEU_CAU_CHO_CLAUDE_CODE.md`
- [ ] Họ tên, mã học viên (SHHV), khóa (2023B / 2024A / 2024B…), lớp, chuyên ngành
- [ ] Tên đề tài (VN/EN) và **số, ngày quyết định giao đề tài**
- [x] 22/11/2026 Tên GVHD: PGS. TS. Trần Đình Khang
- [ ] Tên đề tài hiện tại có **khớp quyết định** không? (nếu không → cần đơn điều chỉnh, mẫu 25)
- [ ] Chứng chỉ ngoại ngữ: loại gì, thi ở đâu? (VSTEP ngoài ĐHBK / CC quốc tế → phải **đăng ký hậu kiểm** và có kết quả trước khi duyệt hồ sơ)
- [ ] Đã đóng đủ học phí, đã hoàn thành chương trình đào tạo chưa?
- [x] 22/11/2026 Bản luận văn: Word, `Luan_van_Thac_si_VuTriCong_v5.docx`; nguồn dựng ở `_lam_viec/`

- [x] 22/11/2026 Phản biện thử bằng 3 vai → `DANH_SACH_VAN_DE_PHAN_BIEN.md` (52 mục); bản **v6** đã sửa các mục không phụ thuộc số liệu (xem mục G của tệp đó). Bản mới nhất: `Luan_van_Thac_si_VuTriCong_v6.docx`

- [x] 22/11/2026 Sinh **30 học sinh mô phỏng** (07–11/2026, 73.098 lượt) trên bản thật, có cờ `moPhong`; các em CÓ trong bảng xếp hạng và bảng giáo viên, chỉ bị loại khỏi thống kê và học ngưỡng. Lập bảng minh chứng ảnh chụp ở `MinhChung_ManHinh/BANG_MINH_CHUNG.md`; luận văn phải gọi phần này là "dữ liệu mô phỏng"
- [x] 22/11/2026 Màn giáo viên có tab **Biểu đồ** (9 biểu đồ, có tên trục và dòng "Cách đọc"; các hình 5–9 theo mục 2.5, Bảng 3.9, Hình 3.9/3.10/3.13/3.14/3.16) và bảng xếp hạng tách riêng Toán, Tiếng Anh. Gói số liệu và ảnh cho Claude Desktop: `MinhChung_ManHinh/goi_cho_claude_desktop.zip` (đọc `HUONG_DAN_CHO_CLAUDE.md` trước)
- [ ] Chụp nốt ảnh minh chứng theo `MinhChung_ManHinh/BANG_MINH_CHUNG.md` (đã xong các dòng 1, 23–26 và 25a–25e; còn màn bài học, Góc bố mẹ, phòng luyện nói, màn chuyên gia)
- [ ] Sửa luận văn: tên mô hình (gpt-oss-120b → Gemini 3.8 Flash), câu 5.1 về giáo viên, thêm mục thực nghiệm mô phỏng ở Chương 4

## Giai đoạn 1 – Đăng ký bảo vệ · HẠN: trước 30/11/2026 (còn ~8 ngày)
- [ ] Hoàn thiện nội dung luận văn và thống nhất với GVHD
- [x] 22/11/2026 Định dạng quyển theo mẫu ĐT.QT12.BM01 → `Luan_van_Thac_si_VuTriCong_v5.docx` (đủ 5 chương; còn phải điền các ô `[...]` ở bìa, kiểm số trang mục lục trong Word). Xem `BAO_CAO_RA_SOAT_LUAN_VAN.md`
- [x] 22/11/2026 Bỏ toàn bộ số liệu có lẫn môn Toán khỏi luận văn → bản **v7** (mục 4.5 chỉ còn cách đo, chờ số riêng môn Tiếng Anh).
- [x] 22/11/2026 Chuẩn hóa định dạng bảng, tiêu đề, chú thích, phương trình → bản **v8** (`QUY_TAC_DINH_DANG.md`).
- [x] 22/11/2026 Phạm vi giữ là bậc tiểu học (lớp 1–5) theo đúng mã nguồn → bản **v10** (bản v9 viết theo lớp 1–12 đã bỏ, nằm trong `_ban_cu_khong_dung/`).
- [x] 22/11/2026 Thêm mục 4.5 "Thực nghiệm trên người học mô phỏng" (Bảng 4.5, Hình 4.3–4.7, Phụ lục B ghi tệp và dòng của từng con số) → bản **v11**. Chỉ dùng số liệu môn Tiếng Anh.
- [ ] Giao `YEU_CAU_CHO_CLAUDE_CODE.md` cho Claude Code (sửa mã phần ngưỡng, đo số liệu mục 4.5 **chỉ cho môn Tiếng Anh**, chụp màn hình) rồi cập nhật Chương 4
- [ ] Điền **Mẫu đăng ký bảo vệ** `00_Mau_Dangkybaove_SoICT.doc` → GVHD ký → nộp **cô Nguyễn Thanh Nguyệt, P.505-B1** (nguyetnt@soict.hust.edu.vn)
- [ ] (Nếu đổi tên đề tài) Đơn điều chỉnh tên đề tài `BieuMau_BanDaoTao/25_…docx`, có ý kiến GVHD, trình ký **trước** khi nộp hồ sơ
- [ ] Ghi tên vào Google Sheet đăng ký BV: https://docs.google.com/spreadsheets/d/1omtVMZGRUyZd6y5BZc-yeM5VVP97kzfc/edit?gid=483340147
- [ ] Điền Lý lịch khoa học `BieuMau_BanDaoTao/11_Lý_lịch_khoa_học.docx`
- [ ] Chạy thử "Kiểm tra đạo văn" trên QLĐT (chỉ để xem trước, KHÔNG dùng báo cáo này đính vào quyển)
- [ ] Nộp hồ sơ BV + **bản mềm PDF** luận văn trên https://qldt.hust.edu.vn (video: https://www.youtube.com/watch?v=NAxO0Qi-Yh8)
  - Điền đúng tên đề tài; file luận văn là PDF
  - Mã nguồn ≤ 30MB, **không** kèm thư viện
  - Lấy **trang đầu báo cáo trùng lặp chính thức** (hệ thống sinh khi nộp) đính vào trang cuối quyển
- [ ] Nhắc GVHD duyệt trên hệ thống và **upload nhận xét** (mẫu 12) – hạn 30/11/2026

## Giai đoạn 2 – Xét duyệt (Khoa / Trường / Ban ĐT)
- 01–07/12/2026: Khoa đánh giá nội dung khoa học
- 08/12/2026: Khoa lập DS được bảo vệ, đề xuất phản biện & hội đồng
- Trước 10/12/2026: Trường CNTT&TT kiểm tra hồ sơ và điều kiện (CTĐT, học phí, **bản sao công chứng CC ngoại ngữ**)
- [ ] Theo dõi tiến trình phê duyệt trên QLĐT, sửa/bổ sung ngay khi có yêu cầu
- [ ] Khi được duyệt: nộp **hồ sơ bản giấy** cho cô Nguyệt (theo thông báo giáo vụ). Theo HD Ban ĐT 2020 gồm:
  - 05 quyển luận văn + 05 tóm tắt (xác nhận hoàn thành của GVHD) – *hỏi lại số lượng hiện hành*
  - Lý lịch khoa học; Nhận xét của GVHD; Đơn điều chỉnh tên đề tài (nếu có)
  - Bản sao công chứng CC ngoại ngữ; bài báo liên quan (nếu có)
  - Bản trích sao điểm toàn khóa (có xác nhận Ban ĐT)
- [ ] Nếu không kịp: đơn gia hạn `09_…docx`, nộp P.505-B1 ngày **07–14/12/2026** (hạn Ban ĐT 30/12/2026). Khóa 2023B **không được gia hạn**.

## Giai đoạn 3 – Bảo vệ · DỰ KIẾN: 26/12/2026 (hoặc tuần cuối tháng 12)
- 3 ngày trước BV: phản biện gửi nhận xét (mẫu 13)
- [ ] Chuẩn bị slide thuyết trình + demo
- [ ] Tập dượt, dự kiến câu hỏi phản biện
- [ ] In quyển đúng quy cách đóng (keo nhiệt, gáy: `Khóa - NGÀNH - HỌ TÊN - Mã HV`)

## Giai đoạn 4 – Sau bảo vệ · HẠN: 20 ngày sau BV (~15/01/2027 nếu BV 26/12)
- [ ] Sửa luận văn theo biên bản hội đồng
- [ ] Bản xác nhận chỉnh sửa `20_Xác_nhận_chỉnh_sửa_luận_văn.docx` (GVHD + Chủ tịch HĐ ký), đóng kèm quyển
- [ ] Nộp lưu chiểu 1 quyển cho TT Truyền thông & Tri thức số (TV Tạ Quang Bửu cũ), có chữ ký GVHD → lấy **Giấy biên nhận**
- [ ] Nộp Trường CNTT&TT 1 quyển (in 2 mặt, chữ nhỏ, bìa mềm) + Giấy biên nhận thư viện
- [ ] Cập nhật bản chỉnh sửa lên QLĐT
- [ ] (Tùy chọn) Xin chứng nhận hoàn thành CTĐT / bảng điểm (~2 tuần sau khi hoàn thiện hồ sơ)

## Tài liệu đã có trong thư mục này
- `README.md` – mốc thời gian, link, danh sách biểu mẫu
- `HUONG_DAN_DINH_DANG_LUAN_VAN.md` – thông số định dạng quyển (A4; lề 2/2/3,5/2,5 cm; TNR 13; giãn 1.1; IEEE)
- `00_Mau_Dangkybaove_SoICT.doc` – mẫu đăng ký bảo vệ của SoICT
- `BieuMau_BanDaoTao/` – 19 biểu mẫu Ban ĐT + PDF hướng dẫn thủ tục BV (2020)
  - Quan trọng: 10 (mẫu quyển + tóm tắt), 11 (lý lịch KH), 12 (nhận xét GVHD), 20 (xác nhận chỉnh sửa), 25 (điều chỉnh tên đề tài), 09 (gia hạn)

## Việc Claude có thể làm tiếp
1. Hỏi và điền phần "Thông tin cần bổ sung" ở trên.
2. Điền sẵn Mẫu đăng ký bảo vệ + Lý lịch khoa học từ thông tin của học viên.
3. Đối chiếu bản luận văn hiện có với `HUONG_DAN_DINH_DANG_LUAN_VAN.md`, chỉ ra và sửa lỗi định dạng.
4. Viết/biên tập Tóm tắt luận văn (≤ 500 chữ) và Lời cảm ơn (100–150 từ).
5. Kiểm tra danh mục tài liệu tham khảo theo chuẩn IEEE, thứ tự xuất hiện.
6. Soạn slide bảo vệ và bộ câu hỏi phản biện dự kiến.
