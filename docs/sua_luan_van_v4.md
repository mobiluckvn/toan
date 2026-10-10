# Những chỗ cần sửa trong `Luan_van_Chuong2_Chuong3_v4.docx`

Soạn 10-10-2026, đối chiếu với hệ thống đang chạy trên `ky-su-nhi.web.app`.
Mỗi mục ghi **nguyên văn đang có → nên sửa thành**, kèm cách tự kiểm chứng lại.

Dựng bảng đối chiếu đầy đủ: `docs/Doi_chieu_he_thong_v4.xlsx` (9 trang).

---

## ⚠ Đọc trước: hai chỗ luận văn đang TỰ ĐÁNH GIÁ THẤP HƠN THỰC TẾ

Phần lớn danh sách này không phải sửa lỗi. Nó là cập nhật những chỗ hệ thống đã
tiến xa hơn lúc viết — và hai trong số đó làm luận văn tự nhận là chưa làm được
thứ nó đã làm được.

---

## 1 · Bảng 3.2, ràng buộc R3 — số phép kiểm tra

| | |
|---|---|
| Đang có | «4.226 câu hỏi sinh sẵn, qua **92 phép kiểm tra**» |
| Nên sửa | «4.226 câu hỏi sinh sẵn, qua **112 phép kiểm tra**» |
| Kiểm chứng | `ls web/test/*.test.mjs \| wc -l` |

Con số 4.226 vẫn đúng — đếm lại khớp.

---

## 2 · Bảng 3.25, giới hạn «chưa đủ dữ liệu học tập thật»

| | |
|---|---|
| Đang có | «Chưa có đủ dữ liệu học tập thật; ví dụ chạy trên người học mô phỏng» |
| Nên sửa | Giữ vế sau, bỏ vế đầu. Nhật ký đã có **3.227 lượt** của **10 tài khoản**, toàn bộ nằm trong 90 ngày gần nhất. |
| Kiểm chứng | `tools/soi_ban_ghi_tienganh.mjs` với khoá quản trị |

⚠ Nhưng câu kết luận **vẫn đúng và nên giữ**: «đến lúc đó mọi nhận định về hiệu quả
dạy học vẫn là giả thuyết». Có nhật ký không phải có KB6 — chưa có nhóm đối chứng,
chưa có bài kiểm tra giấy đầu và cuối.

---

## 3 · Bảng 3.25, giới hạn «chưa đủ dữ liệu để đạt NG21»

| | |
|---|---|
| Đang có | «Bộ ngưỡng đang dùng là bộ mặc định v1; chưa đủ dữ liệu thật để hàm học ngưỡng (mục 3.8.3) đưa ra đề xuất có cỡ mẫu đạt NG21» |
| Nên sửa | «Bộ ngưỡng đang dùng là bộ mặc định v1. Hàm học ngưỡng đã chạy trên 3.213 lượt thật và đưa ra hai đề xuất đạt cỡ mẫu NG21 (ngưỡng bế tắc NG16 cho hai dạng câu). Các ngưỡng còn lại chưa đủ: NG06 và NG07 mới có 46 lượt nói được về chúng, và bốn tham số BKT bị chính phép kiểm tra chéo bác — xem mục 5 dưới đây.» |
| Kiểm chứng | bảng `nguong_de_xuat` trên Firestore, hoặc màn Duyệt đề xuất của vai trò `chuyengia` |

---

## 4 · Mục 3.2 và Bảng 3.4 — ba con số của đồ thị

Ngày 10-10-2026 đồ thị thêm **một** nút và **một** cạnh:

| Chỗ | Đang có | Nên sửa |
|---|---|---|
| mục 3.10, Hình 3.3 | 1.194 đỉnh | **1.195** đỉnh |
| mục 3.10 | 1.062 đỉnh học được | **1.063** đỉnh học được |
| Bảng 3.4 | «Ba loại cạnh của đồ thị lúc chạy (253 cạnh)» | **254** cạnh |

**Vì sao đổi.** Bài `DL:TA3.B00` dạy thật mẫu câu *«What number is it? - It's +
[Number].»* và khai nó ngay trong bài, nhưng bản đồ tri thức chưa bao giờ có nút ấy.
Sáu câu mồ côi: BKT vẫn theo dõi được, còn phép chẩn đoán trên đồ thị không đặt
được nút ấy vào đâu — không có nút trước, không thành ứng viên gốc rễ.

Đáng nói hơn: bản đồ có sẵn nút cầu `sp_g3_numbers` mà **ba mẫu câu lớp 4 khai là
«cần»**, nhưng nó không có bài nào dạy — đúng một trong «19 nút gốc rễ không có bài
dạy (các nút nối giữa hai khối lớp)» mà Bảng 3.25 tự khai. Khai nút thật rồi nối nút
cầu xuống nó thì **danh sách ấy bớt một**.

→ Nếu bản v5 giữ con số 19, nên đổi thành **18** và nói rõ chỗ bớt.

| | |
|---|---|
| Kiểm chứng | `~/.venv/bin/python3 tools/xuat_do_thi_con.py` — in ra «1195 nút · 254 cạnh» |
| Công cụ | `tools/va_nut_mo_coi.py` |

---

## 5 · Mục 3.8.3 — bổ sung một kết quả thực nghiệm đáng kể

Luận văn mô tả cách học ngưỡng nhưng chưa có kết quả. Nay có, và nó **ủng hộ lựa
chọn tham số của chính luận văn**:

> Chạy hàm học ngưỡng trên 3.213 lượt thật, ước lượng EM cho bốn tham số BKT
> (NG01–NG04) **không được đưa thành đề xuất**: kiểm tra chéo 5 phần chia theo
> người học cho AUC **0,682** trên dữ liệu giữ lại, thấp hơn **0,735** của bộ tham
> số đang hành. Nói cách khác, bộ tham số hiệu chỉnh bằng thực nghiệm ở Bảng 3.8
> vẫn dự đoán tốt hơn bộ máy học được từ nhật ký hiện có.

Đây là một kết quả có lợi cho luận văn: nó bảo vệ Bảng 3.8 bằng dữ liệu chứ không
chỉ bằng lập luận. Và nó cho thấy chốt «học để đề xuất, không tự áp dụng» của mục
3.8.3 không phải thủ tục — lần chạy đầu tiên đã dùng tới nó.

---

## 6 · Bảng 3.5 — lược đồ bản ghi lượt trả lời thiếu sáu trường

Bản ghi nay là **v6**. Sáu trường thêm sau khi viết bảng:

| Trường | Từ | Vì sao có |
|---|---|---|
| `nguongVer` | v3 | phiên bản bộ ngưỡng đã dùng — mục 3.8.2 đòi, để tính lại được |
| `khoiLop` | v4 | nấc `khoiLop` của thang phạm vi (mục 3.8.1) |
| `mon` | v5 | nấc `mon`; trước đó bản ghi Toán **không khai môn**, nên 3.075/3.212 dòng rơi ngoài mọi phép gom theo môn |
| `bac` | v6 | nấc `bac`; Bảng 3.22 đòi gom theo cặp (dạng câu, bậc) |
| `sauPhuDao` | v6 | tách lượt tự gỡ khỏi lượt sau can thiệp — xem mục 8 |
| `mauPrompt` · `phienBanMau` · `vanTayPrompt` | — | vân tay lời dặn, mục 2.5.2 |

---

## 7 · Bảng 3.6 — lược đồ hồ sơ nút tri thức thiếu sáu trường

`pTruoc` (mức thạo trước lượt, để tính ΔC của mục 2.5.2) · `msTong` · `msDem` ·
`msTrungBinh` (RT_avg của mục 2.3.1) · `goiTong` · `goiTrungBinh` (H_req) ·
`nguongVer`.

---

## 8 · Bảng 3.22 — một chỗ cách đọc NG09 không dùng được

Bảng 3.22 đọc NG09 bằng câu: *«nếu sau k lần sai trẻ vẫn thường tự làm đúng thì nên
tăng»*. Đo lần đầu trên dữ liệu thật ra một dãy **bật ngược**:

| k | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| P(đúng ở lượt kế) | 47,0% | 20,8% | **67,5%** | 17,6% |
| cỡ mẫu | 394 | 207 | 160 | 51 |

Chỗ vọt lên nằm **đúng tại k = 3 = NG09 đang hành**, tức đúng chỗ hệ thống bật phụ
đạo. Lượt kế tiếp ở đó không còn là «bé tự gỡ» mà là lượt **sau can thiệp** — thường
là câu dễ hơn do bài phụ đạo đưa ra.

Nên cách đọc ấy **mất hiệu lực tại đúng k = ngưỡng đang hành**: đọc nguyên văn thì
chuyên gia nâng NG09 vì chính tác dụng của can thiệp mà NG09 gây ra, rồi vòng sau
lại thấy k = 4 vọt lên. Một vòng tự khẳng định.

→ Đề nghị thêm một dòng vào cách đọc của NG09: *«con số tại k ≥ ngưỡng đang hành
đo tác dụng của can thiệp, không đo khả năng tự gỡ; chỉ các mốc k nhỏ hơn ngưỡng
mới đọc được theo cách này.»*

Hệ thống đã khai `sauPhuDao` trên bản ghi v6 để tách hai thứ ấy, nhưng phải chờ
nhật ký tích đủ dòng v6.

---

## 9 · Mục 3.8.1 — «năm nhóm» cần Thầy chốt

Mục 3.8.1 nói danh mục ngưỡng chia **năm nhóm**, nhưng Bảng 3.19 không có cột nhóm.
Tên nhóm trong `data/nguong.json` hiện là **đặt tạm**, và màn hình chuyên gia đang
gom theo đó:

1. Tham số mô hình người học và trí nhớ — NG01…NG06
2. Ngưỡng quyết định tinh thông và can thiệp — NG07, NG08, NG09
3. Tham số chẩn đoán nguyên nhân — NG10…NG13
4. Lưới an toàn và dẫn dắt — NG14, NG15
5. Ngưỡng hành vi và đo lường — NG16…NG21

→ Cần Thầy xác nhận năm nhóm này đúng ý, hoặc cho tên khác. Nếu đúng thì nên **thêm
một cột «Nhóm» vào Bảng 3.19** để mục 3.8.1 và bảng khớp nhau.

---

## 10 · Bảng 3.24 — mức sẵn sàng của KB4 không còn đúng

| | |
|---|---|
| Đang có | KB4 · mức sẵn sàng: «đang bị chặn (mục 3.5.3)» |
| Nên sửa | «cần cờ chia nhóm» — giống KB5 |

**Vì sao.** Đường mô hình của bài phụ đạo **đã nối đủ**: `PhuDao.jsx` truyền
`goiLLM`, có hai tầng hậu kiểm, câu sinh ra đi vào hàng đợi duyệt `choDuyetTA`.
Nhưng `phudao.js` chỉ gọi tới đường ấy khi kho **tĩnh** không đủ câu:

```js
if (tinhCaVong.length >= soCau || !goiLLM) { /* dùng kho tĩnh */ }
```

Kho tĩnh xưa nay luôn đủ, nên nhánh mô hình **chưa bao giờ tới lượt chạy** — hàng
đợi duyệt rỗng là *hệ quả*, không phải nguyên nhân. 32 nút dưới 4 câu chính là chỗ
nó sẽ chạy. Muốn chạy KB4 thì cần một **cờ chia nhóm cố ý**, đúng thứ KB5 cần.

Cờ ấy đã dựng (`web/src/chung/lib/chiaNhom.js`) nhưng **để tắt**: bật
`kb4_phudao_llm` là nới ràng buộc R3 — câu do mô hình soạn tới tay bé trước khi
người lớn duyệt. Đó là một quyết định về việc dạy trẻ.

---

## Những chỗ KHÔNG cần sửa — đã đếm lại và khớp

| Con số | Luận văn | Đếm lại |
|---|---|---|
| Câu hỏi sinh sẵn | 4.226 | 4.226 ✓ |
| Nút có ít hơn bốn câu (NG20) | 32 | 32 ✓ |
| Đồ thị tải về máy (R4) | 127 KB | 127,4 KB ✓ |
| Số ngưỡng (Bảng 3.19) | 21 | 21 ✓ |
| Nhịp tinh thông (Bảng 3.21) | 3 · 4 · 4 · 5 câu | 3 · 4 · 4 · 5 ✓ |
| Mức tinh thông khi vừa đạt θ = 0,85 | 0,944 | 0,944 ✓ |

Bảy ràng buộc R1–R7 đều giữ được; 19 trong 25 bảng của Chương 3 có hiện thực đầy đủ
trong hệ thống đang chạy.
