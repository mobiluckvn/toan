# Điểm dừng — LUẬN VĂN, CHƯƠNG 2 VÀ CHƯƠNG 3 · 25-08-2026

Ghi tối 25-08-2026. **Đọc trang này trước khi động vào bất kỳ tệp `.docx` nào
trong `docs/`, hoặc trước khi sửa số liệu của luận văn.**

Ngày hôm nay làm đúng hai việc Thầy giao trong review: xác nhận Chương 2 theo
khung Thầy chốt, và viết Chương 3. Việc thứ nhất đẻ ra một chuyện không lường
trước — chín chỗ Chương 2 sai mà bản rà ngày 23-08 chưa bắt được, trong đó ba
chỗ là **mã nút minh hoạ không tồn tại trong đồ thị đang chạy**.

---

## 1 · Đã xong và ĐÃ COMMIT

Commit `c8faeb47`, đã push lên `origin/main`. 13 tệp, +5 160 dòng.

### Ba tài liệu mới

| Tệp | Bộ sinh | Quy mô |
|---|---|---|
| `docs/xac_nhan_chuong2.docx` | `tools/xac_nhan_chuong2.py` | ~25 trang · 22 mục sửa · 3 việc cấu trúc · 7 TLTK thiếu |
| `docs/Chuong3_Luan_van.docx` | `tools/chuong3.py` + `chuong3_khung.py` + `chuong3_p1..p4.py` | ~62 trang · 32 bảng · 14 thuật toán · 8 kịch bản |
| `docs/Chuong2_Luan_van_Thac_sy_1_v4.docx` | `tools/ap_dung_sua_ch2.py` | v3 + **44 lần sửa cho 22 mục** · 214 → 269 đoạn |

> ⚠ **CHẠY LẠI LÀ DỰNG LẠI.** Đừng sửa tay ba tệp `.docx` này. Muốn đổi chữ thì
> sửa script rồi chạy lại. `v3` KHÔNG bị động tới và phải giữ nguyên — nó là
> đầu vào của `ap_dung_sua_ch2.py`.

### Chín chỗ Chương 2 sai, tìm được hôm nay

Bản `sua_chuong2.docx` (23-08) không có mục nào trong số này.

| Mã | Chỗ | Sai gì |
|---|---|---|
| A-5 | 2.2.1.b · 2.2.2.b | Luận văn viết "lớp 1–5" và "E là ràng buộc tiên quyết". Thật ra lớp 1–12, và REQUIRES chỉ là tập con 583/7602. Nay khai `G = (V, E, τ, λ)` |
| **A-6** | 2.2.2.c · 2.3.3.c | **BA MÃ NÚT MINH HOẠ SAI** — xem mục 4 dưới |
| A-7 | Bảng 2.1 | Khai `p_learned` · `struggle_count` · `last_interacted` — không trường nào tồn tại. Mã mẫu `SV_20242344M` là mã học viên cao học |
| B-4 | 2.4.1 | Hệ thống là LAI, không thuần tạo sinh — cần khai thành lựa chọn có lý do |
| B-6 | 2.5.1 | π KHUYẾN NGHỊ, không GÁC ĐƯỜNG; quyền đi tiếp thuộc `dandat.js` |
| C-5 | 2.1.2.c | "liên tục thử nghiệm định dạng" nói quá — thật ra chỉ đổi THỨ TỰ |
| C-6 | 2.3.2.c | Cơ chế quên: chưa cho dạng hàm, chưa khai `h = 14` là số CHỌN |
| C-7 | 2.3.2.b | Câu bắt buộc đúng dùng bộ tham số riêng |
| C-8 | 2.5.2 | Bốn bất biến của kho lưu vết |

### Ba con số đo lại thấy LỆCH tài liệu cũ

- `do_thi.json` là **127 KB** trên đĩa và **≈21 KB** khi truyền (gzip) —
  KHÔNG phải "80 KB" như `sua_chuong2.docx` và chú thích mã ghi.
- Bản đồ đầy đủ **3,4 MB**, không phải 3,1 MB.
- Chuỗi BKT đạt ngưỡng ở **lượt 7** (0,904). Bản cũ ghi "lượt thứ 8 đạt 0,903"
  mà **không nêu chuỗi quan sát** nên không tái lập được. Bản mới nêu rõ chuỗi:
  `sai · đúng · đúng · đúng · sai · đúng · đúng` →
  `0,094 · 0,299 · 0,597 · 0,831 · 0,459 · 0,741 · 0,904`.

### Danh mục tham khảo 11 → 18

Thêm nhóm V. Bảy tài liệu: Baker 2008 · Vygotsky 1978 · Leitner 1972 ·
Ebbinghaus 1885 · Bloom 1984 · Council of Europe 2020 · Bộ GD-ĐT 2018.

⚠ **Vygotsky và Bloom vốn đang bị TRÍCH DẪN TREO** — thân bài nhắc tên mà danh
mục không có mục. Nhân đó sửa luôn cách phát biểu Bài toán 2 Sigma ở 2.4.1:
"cao hơn 98%" là sai, đúng là *vượt khoảng 98% học sinh lớp thường*, tức ~2 độ
lệch chuẩn.

### Đã rà ảnh kiểm chứng — SẠCH

Bảy ảnh `docs/anh_kiem_chung/*.jpg`: không tên bé · không uid/email/điện thoại ·
không thanh địa chỉ (nên không lộ token phiên) · không DevTools · **cả 7 tệp
không có khối EXIF/XMP nào**. Đều chụp từ tài khoản đi thử, mọi màn ở trạng thái
trắng. Dùng được cả khi kho chuyển công khai, và trích thẳng vào phụ lục cũng
được.

---

## 2 · ⚠ VIỆC PHẢI LÀM ĐẦU TIÊN NGÀY MAI

**Lấy lại số liệu sau mốc dựng lại 21 giờ — việc này ĐÃ TREO TỪ 24-08.**

Bản bàn giao 23-08 đặt đây là việc đầu tiên của ngày 24-08. Soi git thì **không
có commit nào ngày 24-08**, nên việc này chưa ai làm.

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
node tools/kiem_kho_du_lieu.mjs        # bốn phép bất biến
node tools/soi_ban_ghi_sai_chu.mjs     # phải ra 0/268
node tools/soi_ban_ghi_tienganh.mjs
```

`report/{uid}` · `teacherBoard/global` · `bangXepHang/global` là bản **tổng
hợp**, dựng từ dữ liệu đã bị dọn tối 23-08. Nếu chúng vẫn lệch với `attempts`
thì việc dựng lại hằng đêm có vấn đề riêng — soi `nightlyTeacherBoard`.

---

## 3 · Còn nợ, theo thứ tự đáng làm

1. **Gửi Thầy hai tệp `xac_nhan_chuong2.docx` và `Chuong3_Luan_van.docx`.**
   Chương 3 chưa qua mắt Thầy lần nào; duyệt xong mới biết phải chỉnh gì.
2. **Chưa có Chương 1 và Chương 4.** Chương 4 (thực nghiệm) đứng trên tám kịch
   bản ở mục 3.7 — ba kịch bản KB1 · KB3 · KB5 **chạy được ngay, không cần
   người học thật**, nên làm trước để Chương 4 có số liệu thật.
3. **Sửa chú thích sai trong mã:** `web/src/mon/tienganh/lib/doThi.js` dòng 10
   và 35 vẫn ghi "80 KB". Con số đúng là 127 KB / ≈21 KB.
4. **Ba chú thích nói "không màn nào đọc `reviewQueue`" nay ĐÃ SAI với Tiếng
   Anh** — xem mục 5.
5. **Đi thử một buổi TRỌN VẸN trên bản chạy.** Vẫn chưa buổi nào đi hết
   Sát hạch → xong bài → sinh thẻ ôn → màn ôn lại. Nợ từ 23-08.
6. **Cài ESLint.** Vẫn chưa có `web/.eslintrc*` lẫn `web/eslint.config.*`, và
   `package.json` không nhắc eslint. Lỗi hook làm trắng màn hôm 23-08 ESLint
   bắt được ngay (`react-hooks/rules-of-hooks`). Nợ từ 23-08.
7. **`sessionId` của Toán nên mang cả `learnerId`.** Nợ từ 23-08.
8. **Hỏi bác: hai tệp sao lưu có chuyển ra ngoài kho không?**
   `sao_luu_don_ban_ghi.json` và `sao_luu_don_ban_ghi_2.json` vẫn nằm trong thư
   mục kho (đã gitignore, đã kiểm là KHÔNG lọt vào 14 commit vừa push). Chúng
   chứa dữ liệu học thật của các bé. Đã hỏi tối 23-08, chưa có trả lời.
9. **Hai tài liệu cũ nay đã lạc hậu một phần:** `docs/sua_chuong2.docx` liệt kê
   13 chỗ cần sửa mà **cả 13 nay đã áp vào v4**, và nó còn ghi "80 KB".
   `docs/benchmark_chuong2.xlsx` cũng vậy. Chưa dựng lại — quyết định xem có
   dựng lại hay để nguyên làm dấu vết lịch sử.

---

## 4 · Ba mã nút minh hoạ SAI — loại lỗi phản biện tra ra trong ba phút

Đây là phát hiện đáng giá nhất trong ngày, và đáng ghi lại vì nó chỉ ra một họ
lỗi chứ không phải ba lỗi lẻ.

| Chương 2 (v3) viết | Đồ thị đang chạy thật ra là |
|---|---|
| `v_g1_u9_numbers` — "numbers 1 to 10" ở Lớp 1 | **KHÔNG TỒN TẠI** ở cả đồ thị đầy đủ lẫn đồ thị lúc chạy. Lớp 1 không có nút số đếm nào |
| `v_g2_u14_nineteen` ← `v_g2_u13_eleven` | Không có cạnh nối. Cạnh thật là `v_g2_u14_eighteen` → `v_g2_u14_nineteen`, và nó mang nhãn `trong_bai` — **đúng loại cạnh hệ thống CỐ Ý loại khỏi chẩn đoán** |
| `sp_g3_u11_2` phụ thuộc nút từ vựng `v_g2_u13_eleven` | Tiên quyết thật là `sp_g3_u2_2`. Chuỗi đúng: `sp_g3_u11_2 → sp_g3_u2_2 → sp_g3_u1_1 → sp_g2_greeting` |

**Họ lỗi:** luận văn viết TRƯỚC, hệ thống dựng SAU, và khi hệ thống dựng xong
thì không ai quay lại soi câu chữ. Ba ví dụ thay thế trong v4 đều đã đối chiếu
bằng chính phép duyệt của hệ thống (`duyetNguoc` với `CANH_THAT`).

**Cách soi lại nếu sửa thêm ví dụ nào:**

```python
import json, collections
g = json.load(open('web/public/content/tienganh/do_thi.json'))
back = collections.defaultdict(list)
for c in g['canh']:
    if c.get('loai', 'ban_do') in {'ban_do', 'noi_bai'}:   # ⚠ BỎ trong_bai
        back[c['truoc_khi']].append(c['can'])
# nút có tồn tại không:  ma in g['nut']
# tiên quyết trực tiếp:  back[ma]
```

---

## 5 · Những cái bẫy đã trả giá để biết — ĐỪNG DẪM LẠI

- **Khối JSON của Bảng 2.1 KHÔNG nằm ở thân tài liệu** mà trong một **ô bảng
  1×1**, nên `doc.paragraphs` của python-docx không thấy. Mất một lần chạy vì
  chỗ này. Phải qua `d.tables[0].rows[0].cells[0].paragraphs`. Và **đừng xoá
  hết đoạn trong ô** — ô bảng rỗng thì Word báo hỏng tệp; phải giữ lại đoạn đầu
  làm neo.
- **Đừng gán `runs[0].text = ...` để sửa một đoạn.** Đoạn nào có run đầu in đậm
  (kiểu `- Nguyên lý: `) thì cả đoạn sẽ thành in đậm. Phải dựng lại run từ khuôn
  `rPr` — xem `dat_chu()` trong `ap_dung_sua_ch2.py`.
- **`grep ... | head && echo "có lỗi"` LUÔN chạy nhánh `&&`**, vì mã thoát của
  đường ống là của `head` chứ không phải `grep`. Phép soi bí mật đầu tiên của
  tôi báo động giả vì đúng lỗi này. Soi bằng Python cho chắc.
- **Ba chú thích trong mã nay đã SAI với môn Tiếng Anh** — chúng nói "không màn
  nào đọc `reviewQueue`, kể cả bên Toán":
  `web/functions/index.js:92` · `mon/tienganh/components/OnLai.jsx:11` ·
  `mon/tienganh/lib/onlai.js:6`.
  Thực tế đã kiểm hôm nay: **Tiếng Anh ĐÃ nối trọn** (`duLieu.js:40 theOn` →
  `ManTiengAnh.jsx:81 docTheOn` → `:305 theDenHan` → `OnLai`). **Toán thì vẫn
  chỉ GHI, không đọc.** Chú thích đúng phải phân biệt hai môn.
- **Đếm ★ cho cẩn thận.** Tôi báo với bác "6 chỗ mới" trong khi thật ra là 9 —
  đếm nhầm ở phần tóm tắt, tài liệu thì vẫn đúng 9.

---

## 6 · Trạng thái kho

- Nhánh `main`, khớp `origin/main` tại `c8faeb47`. **0 commit chưa đẩy.**
- Cây làm việc sạch.
- `.gitignore` nay chặn thêm `~$*` — Word đẻ tệp khoá tạm khi đang mở `.docx`.
- Kho là **riêng tư** (GitHub API trả 404).
- Đã quét 7 936 dòng thêm mới của 14 commit vừa push: không có khoá Google API,
  PEM, `private_key`, khoá Groq, khoá OpenAI, `client_secret`, hay mã tài khoản
  thật nào bị nhúng.
