# Gói dữ liệu cho luận văn: hệ thống Kỹ Sư Nhí, dữ liệu mô phỏng

Đọc tệp này trước khi dùng các tệp khác trong gói.

## 1. Đây là gì

Gói gồm số liệu và ảnh màn hình từ hệ thống học thích ứng Kỹ Sư Nhí (https://ky-su-nhi.web.app). Dùng cho Chương 4 (thực nghiệm) và các hình minh chứng của luận văn thạc sĩ "Ứng dụng phương pháp học thích ứng hỗ trợ cá nhân hóa trong đào tạo tiếng Anh" (Vũ Trí Công, SoICT, bảo vệ 12/2026).

- **Người học:** 30 người học mô phỏng, lớp 1–5, sinh bằng script `tools/mo_phong/hoc_sinh_ao.mjs`.
- **Thời gian:** các em vào học ngẫu nhiên trong tháng 7/2026 và học tới 21/11/2026.
- **Lịch học:** học mỗi tối, khung 19:00–21:45. Lớp 1 chỉ học Tiếng Anh; lớp 2–5 học cả Toán và Tiếng Anh.
- **Cách tính:** mọi con số được tính bằng chính mã của hệ thống, gồm `functions/src/bieuDo.js` và hàm BKT `applyAttempt` trong `functions/src/bkt.js`. Đầu vào là nhật ký lượt trả lời trên máy chủ. Màn hình của cô giáo cũng hiện đúng những con số này.

## 2. ⚠ Quy tắc bắt buộc khi viết vào luận văn

1. **Đây là DỮ LIỆU MÔ PHỎNG, không phải học sinh thật.**
   - Mọi bảng, hình và chú thích phải ghi "dữ liệu mô phỏng".
   - Không được viết "học sinh đã học", "kết quả thực nghiệm trên học sinh" hay "nhật ký thật".
2. **"Học hết chương trình trong khoảng 3 tháng" là KỊCH BẢN đặt vào mô phỏng, không phải kết quả đo.**
   - Câu nên viết: "Mô phỏng kịch bản học đều hằng ngày cho thấy hệ thống hỗ trợ được nhịp học đi hết chương trình một năm trong khoảng 13 tuần."
   - Câu cấm viết: "học nhanh gấp 3 lần".
3. **Không suy ra hiệu quả dạy học.** Luận văn chưa có nhóm đối chứng (mục 5.2, hướng phát triển).
4. **Mô tả đúng hình dạng thật của số liệu, kể cả khi nó không đẹp.**
   - Đường cong học tập lên xuống, không giảm đều về 0.
   - Tỉ lệ đúng giảm ở các tuần cuối, vì các em đã học xong và chỉ ôn thưa.
   - Không làm tròn hay chọn điểm để đường trông đẹp hơn.

## 3. Ngưỡng đang dùng (`du_lieu/nguong_dang_dung.json`)

| Mã | Ý nghĩa | Giá trị |
|---|---|---|
| NG07 θ | Ngưỡng "đã nắm vững" | 0,85 |
| NG08 θ_yếu | Ngưỡng "yếu hẳn" | 0,30 |
| NG09 | Số lần sai liên tiếp thì thành "đang mắc" | 3 |
| NG13 | Số ngày chưa gặp lại thì bật cờ "có nguy cơ quên" | 14 |
| NG06 | Chu kỳ bán rã của hàm quên (ngày) | 14 |
| NG25 | Điểm P(L) mà hàm quên kéo về | 0,5 |

## 4. Các tệp số liệu

Thư mục `du_lieu/csv/` chứa các tệp CSV (UTF-8 có BOM, mở được bằng Excel). Mọi tệp đều có 3 cột đầu là `ma_em`, `ten`, `lop`.

| Tệp | Mỗi dòng là | Các cột còn lại | Dùng cho hình nào |
|---|---|---|---|
| `00_tom_tat_tung_em.csv` | một em | từ ngày, đến ngày, số lượt, số tuần | Bảng tổng quan mô phỏng |
| `01_theo_tuan.csv` | một em × một tuần × một môn | `tuan_bat_dau` (thứ Hai); `luot`; `dung_lan_dau_pct` (% câu đúng ngay lần thử đầu, câu làm lại sau gợi ý không tính); `bai_da_hoc_cong_don` (bài đã làm ít nhất 1 câu, chưa chắc đạt); `phut_ca_tuan`, `buoi_ca_tuan` (của cả hai môn); `giay_moi_cau_trung_vi` | Biểu đồ 1–3 |
| `02_gio_bat_dau_buoi.csv` | một em × một khung 30 phút | `khung_gio` (giờ VN), `so_buoi` | Biểu đồ 4 |
| `03_duong_cong_hoc_tap.csv` | một em × một môn × lần luyện thứ k | `so_luot`; `ti_le_loi_pct` (để trống khi dưới 10 lượt, theo mục 2.5) | Biểu đồ 5: đường cong học tập (mục 2.5, 3.9) |
| `04_nut_dat_theta_theo_tuan.csv` | một em × một tuần | `so_nut_da_gap`; `dat_theta_da_luu` (P(L) ≥ θ ở lần gặp gần nhất); `dat_theta_sau_tinh_quen` (sau khi tính quên tới cuối tuần) | Biểu đồ 6 (Hình 3.9, 3.13) |
| `05_sau_tinh_trang_nut.csv` | một em, tại 22/11/2026 | `dang_mac`, `yeu_han`, `vung_phat_trien_gan`, `da_nam_vung` (4 cột này cộng lại bằng `tong_nut`); `co_nguy_co_quen` (là cờ, đếm riêng) | Biểu đồ 7 (Bảng 3.9, Hình 3.10) |
| `06_ho_so_truoc_sau_tinh_quen.csv` | một em × một dải P(L) | `so_nut_da_luu`, `so_nut_sau_tinh_quen` (tính quên tới 22/11/2026) | Biểu đồ 8 (Hình 3.13) |
| `07_dien_bien_tai_nut.csv` | một lượt tại một nút | `nut`, `mon`, `tung_dang_mac`, `luot_thu`, `ngay`, `dung`, `PL_truoc_da_tinh_quen`, `PL_sau`, `sai_lien_tiep`. Mỗi em có tối đa 8 nút, mỗi nút tối đa 40 lượt gần nhất | Biểu đồ 9 (Hình 3.14, 3.16) |

**Định nghĩa "nút":**
- Tiếng Anh: một nút là một từ (mã `v_…`) hoặc một mẫu câu (mã `sp_…`).
- Toán: nút BKT là cả một chương (mã `CHUONG:n@Gk`). Vì vậy đường cong học tập của Toán đếm lần luyện theo **bài**.

**Các tệp khác trong `du_lieu/`:**
- `json/<ma_em>.json`: toàn bộ số liệu của một em, đúng dữ liệu mà màn hình dùng để vẽ.
- `tom_tat_mo_phong_ca_30_em.json`: tóm tắt do script mô phỏng ghi ra, gồm số tuần để xong chương trình theo lớp, đường học theo tháng, theo tuần học và theo lần gặp.

## 5. Ảnh màn hình (`anh_man_hinh/`)

Chụp trên bản thật ngày 22/11/2026. Bảng ánh xạ từng ảnh với nhận định trong luận văn nằm ở `BANG_MINH_CHUNG.md`.

**Ảnh chụp các màn khác:**

| Ảnh | Màn hình |
|---|---|
| `01_…` | Kệ sách của học sinh |
| `23_…` | Sổ bố mẹ |
| `24_…` | Bảng theo dõi của cô giáo |
| `24b`, `24d`, `24g` | Tab Tổng quan của Minh An (lớp 1), Diệu Linh (lớp 2), Phúc Lâm (lớp 5) |
| `26_…`, `26b_…` | Bảng xếp hạng Toán và Tiếng Anh |

**Ảnh chụp tab Biểu đồ của Diệu Linh (lớp 2):**

| Ảnh | Biểu đồ |
|---|---|
| `25_bieudo_dieulinh_1_2` | 1 và 2 |
| `25_bieudo_dieulinh_3_4` | 3 và 4 |
| `25_bieudo_dieulinh_5_6_duongcong_nutvung` | 5 và 6 |
| `25_bieudo_dieulinh_7_8_tinhtrang_quen` | 7 và 8 |
| `25_bieudo_dieulinh_9_dienbien_nut` | 9 |

## 6. Gợi ý việc cần làm với gói này

- Viết một mục mới trong Chương 4, "Thực nghiệm trên người học mô phỏng". Mục này gồm:
  - mô tả kịch bản (đọc `KE_HOACH_MO_PHONG.md`);
  - bảng tổng hợp theo lớp, gồm số em, số lượt, số tuần để xong chương trình (trung vị) và phút học trung bình;
  - các hình 5–9 vẽ lại từ CSV cho một em tiêu biểu, chú thích ghi "dữ liệu mô phỏng".
- Thay các câu "nhật ký thật" trong v10 (mục 4.5, Bảng 4.5–4.6, Tóm tắt, mục 4.7, 5.1) bằng câu nói rõ dữ liệu là mô phỏng.
- Khi trích một con số, ghi tệp và dòng lấy ra để người đọc kiểm lại được.
