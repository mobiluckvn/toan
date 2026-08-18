# TIẾNG ANH — điểm dừng chung ba quyển

Ghi 18-08-2026. **Đọc trang này trước khi làm tiếp môn Tiếng Anh.**
Đọc kèm `docs/day_chuyen_du_lieu_tienganh.md` — dây chuyền 10 tầng, và §6 là bản rà
soát lớp 3.

## Đang ở đâu

| | lớp 1 | lớp 2 | lớp 3 |
|---|---|---|---|
| Unit | 16 | 16 | **21** |
| Từ | 60 | 56 | **204** |
| Mẫu câu | 19 | 18 | **43** |
| Câu luyện tập | 469 | 287 | **998** |
| Câu sát hạch | 80 | 80 | **105** |
| Kỳ ôn tập | 4 | 4 | **5** |
| Kịch bản nói | 16 · 153 bước | 16 · 130 | **21 · 346** |
| Clip tiếng | 558 | 507 | **1011** |
| **Video** | 37 | 34 | **CHƯA CÓ** |
| Deploy | ✅ | ✅ | **chưa** |

Kệ sách: `ta1 → lop2 → ta2 → lop3 → ta3 → lop4 → lop5 → lop5q2`
Cổng: **59 tệp kiểm · 0 FAIL**.

---

## VIỆC KẾ TIẾP — theo đúng thứ tự

### 1 · Video lớp 3, CẤU TRÚC MỚI (bác chốt 18-08)

⚠ **KHÔNG dùng lại khuôn lớp 1·2.** Lý do đo được:

| | lớp 1 | lớp 2 | lớp 3 |
|---|---|---|---|
| từ / unit | 3,8 | 3,5 | **9,7** (nhiều nhất 15) |
| video từ mới nếu giữ khuôn | 30s | 30s | **~73s, unit nặng nhất ~112s** |

Hai việc phải làm:

**(a) Tách video từ mới theo NHÓM NGHĨA** — mỗi unit 2–3 tệp ~30 giây thay vì một
tệp dài. Ví dụ U13: *phòng ốc* / *đồ đạc* / *chỗ đứng*. Tên tệp nói ra nhóm nào.

**(b) Thêm loại cảnh cho 39 TỪ TRỪU TƯỢNG.** Chúng đã khai `hinh._khong_ve` kèm lý
do, và bản chuẩn gắn cờ `khong_ve`. Không vẽ `hello` được, nhưng DIỄN được: cảnh
**dùng trong câu** — hai người chào nhau, chữ `hello` sáng lên trong câu.

Chỗ sửa: `tools/video/kich_ban.py` (dựng cảnh) và `tools/video/dung_video.py` (vẽ).
Cả hai nay đã **suy lớp từ mã bài** (`DL_TA3_B04` → `ta3`), không phải sửa đường dẫn.

⚠ Nhớ ba bài học của video lớp 2:
- lời NHẮC LẠI chỉ lấy vế trước `" - "` (đã có `cau_noi_duoc()`)
- sổ âm mỗi quyển phải TỰ ĐỦ — clip dùng chung với quyển khác vẫn phải có tên trong
  sổ quyển này, không thì video ra câm
- rút khung hình NHÌN TẬN MẮT, nhất là hình vẽ tay qua cairosvg

### 2 · Bài đọc hiểu ngắn (bác chốt 18-08)

Mỗi chương một bài đọc 4–6 câu, **dựng CHỈ từ vốn từ đã học** của lớp 1+2+3 tính tới
chương ấy. Gồm: đoạn đọc → trắc nghiệm **ý chính** → trắc nghiệm **chi tiết**.

Hạ tầng **không cần bộ chơi mới**: `chon` (trắc nghiệm) và `tf` (đúng/sai) đã chạy
sẵn ở cả ba quyển; chỉ cần một màn hiện đoạn văn phía trên.

⚠ Phải có phép kiểm chặn **chữ lạ** — đúng khuôn cổng `mọi chữ trong câu sinh ra đều
có gốc` đang canh.

### 3 · Bài viết ngắn, chấm bằng AI (bác chốt 18-08)

Bốn điều bác chốt:
1. **Sửa lỗi và khen CỤ THỂ** — chỉ ra câu sai ở đâu, sửa lại cho đúng.
2. **Có điểm để vào sổ** — và phải nói rõ là AI chấm.
3. **Chỉ gợi ý bằng vốn từ đã học**, không dạy từ mới.
4. **Bố mẹ đọc được bài viết và lời chấm.**

Hạ tầng đã có: `web/functions/src/luyennoi.js` chạy Groq `openai/gpt-oss-120b`, khoá
ở Secret Manager. Dựng `chamViet` theo đúng khuôn ấy.
⚠ Thêm `loai` mới vào `hocBaTA` thì phải sửa `firestore.rules` VÀ deploy rules —
xem `docs/DEPLOY.md`.

### 4 · Deploy lớp 3

Chưa deploy vì còn thiếu video. Deploy phải kèm rules nếu đụng `firestore.rules`.

---

## Món nợ cũ còn treo

- **Lớp 1**: huy hiệu chương chưa đi hết một kỳ ôn tập trên bản THẬT · chưa thử phần
  NÓI bằng micro thật · 19 mẫu câu chưa soát xong theo tiêu chuẩn "một video một
  việc" · ba nhóm hình "gần đúng" ở `docs/hinh_da_soat.md`.
- **Lớp 2**: hai video mẫu câu dài 100s và 94s · chưa mở app nhìn tận mắt một vòng.
- **Lớp 3**: chưa nhìn tận mắt bài nào.

---

## Ba cái bẫy đã dính TRONG ĐỢT NÀY — đừng dẫm lại

**1 · Quên khai sổ đăng ký, HAI LẦN LIỀN.** Lớp 2 và lớp 3 đều dựng xong hết rồi mới
phát hiện `chuong_trinh.json` chưa có tên quyển → kệ sách không hiện, mọi thứ chỉ là
tệp trên đĩa. Nay đã có cổng hỏi ngược trong `kesach.test.mjs`.
⚠ `thuTu` phải KHÔNG TRÙNG trên cả kệ VÀ xếp theo LỚP tăng dần.

**2 · Bộ dựng ghim cứng tên quyển.** `sinh_ontap` · `sinh_kichban_noi` · `kich_ban` ·
`dung_video` đều từng ghim `ta1`. Nặng nhất: `sinh_kichban_noi` ghi thẳng
`data/tienganh/kichban_noi.json` cho MỌI quyển — chạy lớp 2 là đè mất kịch bản lớp 1,
mà lớp 1 có ba bài viết tay máy không sinh lại được.

**3 · Danh sách ghim cứng theo lớp 1·2 trong bộ sinh.** `VAI_BIET` liệt kê 13 vai;
lớp 3 khai thêm 13 vai mới → `sua_slot` bị hiểu nhầm là danh sách TỪ, kho rỗng, bỏ
qua cả mẫu, IM LẶNG. Nay suy từ chính dữ liệu (`vai_biet()`).
Cùng họ: `str.capitalize()` hạ chữ hoa phía sau (`"Ms Hoa"` → `"Ms hoa"`), `a/an`
không ai giải, `cau_hoi` bỏ từ không có nghĩa tiếng Việt nên tên riêng rơi mất.

---

## Chạy lại lớp 3 từ đầu

```bash
python3 tools/chuan_tienganh.py --lop 3          # đòi _thieu RỖNG
python3 tools/sinh_bai_tienganh.py --lop 3 --tat-ca
python3 tools/sinh_ontap_tienganh.py --lop 3     # danh mục khung phải có trước
python3 tools/sinh_kichban_noi.py --lop 3
tools/tts/.venv/bin/python tools/tts/sinh_am.py \
    --vao data/tienganh/lop3_loi.json \
    --ra web/public/content/tienganh/audio \
    --so web/public/content/tienganh/lop3_am.json
cd web && npm test
```

⚠ `sinh_am.py --so` nay GỘP vào sổ cũ, không ghi đè (đã vá 17-08 sau khi nó xoá mất
553 clip lớp 1). Chỉ `--lam-lai` mới quét sạch.
