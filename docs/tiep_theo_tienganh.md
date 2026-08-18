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
| Câu luyện tập | 469 | 287 | **1 058** |
| Câu sát hạch | 80 | 80 | **105** |
| Kỳ ôn tập | 4 | 4 | **5** |
| Kịch bản nói | 16 · 153 bước | 16 · 130 | **21 · 346** |
| Clip tiếng | 558 | 507 | **1 383** |
| **Video** | 37 | 34 | **86** (43 từ mới + 43 mẫu câu) |
| **Bài đọc hiểu** | — | — | **5** |
| **Bài viết chấm AI** | — | — | **5** |
| Deploy | ✅ | ✅ | **✅ 18-08** |

Kệ sách: `ta1 → lop2 → ta2 → lop3 → ta3 → lop4 → lop5 → lop5q2`
Cổng: **74 tệp kiểm · 0 FAIL**.

---

## Đợt 18-08 làm được những gì

### 1 · Video từ mới tách theo NHÓM NGHĨA ✅

21 unit → **43 tệp** thay vì 21. Nhóm không phải soạn thêm: `vai` đã chia sẵn, và
`_gom_nhom_nghia()` trong `sinh_bai_tienganh.py` gom theo đó.

⚠ **Chia theo GIÂY, không theo số từ.** Từ có hình mất ~4 giây; từ KHÔNG vẽ được thì
dạy bằng câu nên mất ~7. Đếm đầu từ thì nhóm *Lời chào* của U1 (6 từ, cả sáu đều trừu
tượng) ra 56 giây trong khi phép đếm bảo nó bằng 6 từ thường (39 giây). Ba con số ở
đầu phần ấy đều suy từ phép đo thật trên 75 video.

Kết quả đo lại: video từ mới **16–48 giây**, không cái nào vượt trần 50.

### 2 · Cảnh "dùng trong câu" cho từ trừu tượng ✅

41/51 từ không có hình nay hiện **câu chứa nó**, chữ ấy sáng lên trong ô vàng
(`loai: "tu_cau"`). 10 từ còn lại (`hi` · `bye` · `that` · `friend` · `no` · `sure` ·
`on` · `old` · `small` · `toy`) không câu nào của bài chứa → vẫn là thẻ chữ, vì
**không bịa câu tiếng Anh** là luật cứng của cả môn.

⚠ Câu ví dụ phải lấy **CẢ HAI VẾ** của cặp hỏi–đáp. `cau_noi_duoc()` chỉ giữ vế hỏi,
mà chỗ điền từ của quá nửa mẫu câu lớp 3 nằm ở vế đáp (`Where's your bedroom? - It's
here.`) — bỏ vế sau là bốn từ chỉ vị trí rơi hết về thẻ chữ trần.

### 3 · Bài đọc hiểu ngắn ✅ — `ta3/dochieu.json`

Mỗi chương một bài: đoạn 6 câu + 4 câu hỏi (1 ý chính · 2 chi tiết · 1 có/không).
Đoạn văn **ở lại trên màn suốt cả bài** — giấu đi rồi hỏi thì thành bài kiểm tra trí
nhớ. Mỗi dòng một nút nghe.

⚠ Câu "câu nào CÓ trong bài đọc?" **KHÔNG có nút nghe**: `am` của nó là clip của đáp
án, bấm nghe là được đọc thẳng câu đúng cho. Đã suýt lọt, chỉ lộ khi mở app nhìn.

Kết quả ghi ở **sổ tại máy** (`docHieu`), chưa lên máy chủ — xem `ghiDocHieu()`.

### 4 · Bài viết ngắn chấm bằng AI ✅ — `ta3/vietbai.json`

Bốn điều bác chốt đều có chỗ đứng, và cả bốn đều có phép kiểm
(`test/tienganh_chamviet.test.mjs`):

| | ở đâu |
|---|---|
| sửa lỗi và khen CỤ THỂ | `loiDanCham()` đòi `khen` và `loi[]` có câu sửa |
| có điểm, NÓI RÕ AI chấm | `nguon: 'ai'` trong sổ · dòng "Máy chấm (AI)" trên màn · "(máy chấm)" trên thẻ |
| chỉ gợi ý bằng từ đã học | bảng vốn đi kèm lời dặn, **và** `soiLoiCham()` bỏ câu có chữ lạ |
| bố mẹ đọc được | giữ CẢ bài viết trong sổ · Góc bố mẹ · `hocBaTA` loai `viet` |

⚠ `soiLoiCham` soi câu SỬA (tiếng Anh thuần) khác với lời GỢI Ý (tiếng Việt lẫn tiếng
Anh). Đem cả câu Việt đi so với vốn từ tiếng Anh thì mọi chữ Việt đều "lạ" và lời gợi
ý đúng bị bỏ — đã sập ngay lượt thử đầu.

### 5 · Ba lỗi CÂM của nội dung lớp 3, sửa nhân thể

Không nằm trong việc được giao, nhưng deploy kèm chúng thì bé lãnh đủ:

- **60 câu bậc 1 "bấm vào HÌNH đúng" mà không nút nào có hình** — bốn nút ra bốn dấu
  ❔ giống hệt nhau. Nay đủ hình cả bốn nút thì mới bày hình, không thì bấm vào CHỮ.
- **16 câu sát hạch "nhìn hình rồi đúng/sai" mà không có hình** — trọn 15 câu của ba
  bài đầu là câu không thể trả lời, mà điểm vẫn vào học bạ. Nay câu đúng/sai chỉ dựng
  từ từ CÓ hình, thiếu thì bù bằng câu nghe → chọn nghĩa.
- **`"Where are the lamp? - They're here the room."`** — ô đòi số nhiều mà từ chưa
  khai `so_nhieu` thì bộ sinh lẳng lặng điền dạng gốc; và `here`/`there` bị nhận là
  giới từ. Nay ô thiếu dạng thì **loại từ ấy khỏi kho**, không điền bừa.
- `"Ben None — bạn Ben"`: ghép `tu` với `ipa` bằng f-string, mà 8 tên riêng không có
  IPA. Nay dùng `tu_ipa()`.

---

## VIỆC KẾ TIẾP

### 1 · DEPLOY — ĐÃ CHẠY 18-08, cả ba phần

```bash
cd web && npm test && npm run build
firebase deploy --only firestore:rules      # ✅ loai 'viet' đã lên
firebase deploy --only functions            # ✅ chamViet: "Successful create operation"
firebase deploy --only hosting              # ✅ https://ky-su-nhi.web.app
```

⚠ **Deploy TỪNG PHẦN MỘT, đừng gộp.** Gộp `--only firestore:rules,functions,hosting`
thì hosting hỏng giữa chừng (mạng rớt lúc đẩy 65 MB video) và **kéo cả lệnh xuống**:
`functions` không chạy, mà `| tail` che mất mã thoát nên nhìn tưởng xong. Phải mở
`firebase functions:list` mới thấy `chamViet` chưa hề có. Hosting đẩy lại thì nó chỉ
bù phần còn thiếu — chạy hai ba lần là xong, không phải đẩy lại từ đầu.

### 2 · Chưa thử được, phải thử sau khi deploy

**Vòng chấm bài viết THẬT chưa chạy lần nào.** Khoá Groq nằm ở Secret Manager, máy
này không có, nên phần đã kiểm chỉ là: chốt cửa · lời dặn · bóc JSON · soi chữ lạ
(20 phép, chạy bằng `node`). Đường mạng thì mới chỉ thấy nhánh LỖI chạy đúng.

Sau khi deploy, mở một bài viết và chấm thử một bài **có lỗi cố ý** (`I Ben.`) rồi
soi ba thứ: điểm có ra không · câu sửa có đúng không · có từ nào ngoài bảng vốn không.

### 3 · Món nợ cũ còn treo

- **Video mẫu câu dài 70–100 giây** — 35 tệp, cả ba quyển. Khuôn mẫu câu (tách mẩu →
  ba câu cùng khuôn → tập nói ba tốc độ có khoảng lặng → chỗ dễ nhầm) chưa ai rút
  gọn. `tienganh_video.test.mjs` niêm phong con số 35, **chỉ được giảm**.
- **Lớp 1**: huy hiệu chương chưa đi hết một kỳ ôn tập trên bản THẬT · chưa thử phần
  NÓI bằng micro thật · 19 mẫu câu chưa soát xong theo "một video một việc" · ba nhóm
  hình "gần đúng" ở `docs/hinh_da_soat.md`.
- **Lớp 2**: chưa mở app nhìn tận mắt một vòng.
- **Lớp 2**: 11 chỗ `⚠️ gần đúng` và MỘT chỗ sai vật — `jam` 🍯 là hũ MẬT ONG.
  Chưa sửa vì sửa một hình là phải dựng lại video của bài ấy (quyển đã deploy).
  Xem `docs/hinh_da_soat_lop2.md`.
- **Lớp 3**: 20 chỗ `⚠️ gần đúng` còn để nguyên, nặng nhất là bốn phòng của U6
  (`library` 📚 · `art room` 🖼️ · `music room` 🎹 · `computer room` 💻) — cả bốn đều
  lấy một ĐỒ VẬT đứng thay cho CĂN PHÒNG. Xem `docs/hinh_da_soat_lop3.md`.
- Bài đọc hiểu chưa vào học bạ máy chủ (cố ý, xem `ghiDocHieu`).

---

## Ba cái bẫy đã dính TRONG ĐỢT NÀY — đừng dẫm lại

**1 · Cổng ghim cứng MỘT QUYỂN.** `tienganh_hinh_dung_tu.test.mjs` mở đúng thư mục
`ta1` và `assert.equal(tep.length, 16)`. Lớp 2 và lớp 3 chưa từng bị nó soi ngày nào —
và đúng những lỗi nó sinh ra để bắt ("câu bảo nhìn hình thì phải CÓ hình") lại nằm đầy
trong lớp 3. Cổng im lặng là cổng không ai biết đã ngừng canh.

→ **Đã chữa cuối ngày 18-08**: cổng nay suy danh sách quyển từ ĐĨA và soi cả ba (53
bài), mỗi quyển một sổ soát riêng. Bật lên là đỏ ngay năm chỗ — `table` · `desk` ·
`eraser` · `pencil case` · `swinging` đều vẽ nhầm vật, và tám chỗ hai từ một hình.

**2 · Bộ sinh LUI VỀ MẶC ĐỊNH thay vì kêu lên.** `dang_can(o, t) or t["tu"]`: ô đòi số
nhiều mà từ không có dạng ấy thì lấy dạng gốc. Câu vẫn ra, cổng vẫn xanh, bé đọc
"Where are the lamp?". Mọi chỗ viết `X or mặc_định` trong bộ sinh đều đáng ngờ như thế.

**3 · Nút nghe làm hỏng chính câu hỏi.** Câu đọc hiểu "câu nào CÓ trong bài" gắn `am`
là clip đáp án. Không cổng nào bắt được (clip có thật, mã đúng, tệp tồn tại) — chỉ mở
app bấm thử mới thấy. Cùng họ với "kiểm bằng mắt trước khi deploy".

---

## Chạy lại lớp 3 từ đầu

```bash
python3 tools/chuan_tienganh.py --lop 3          # đòi _thieu RỖNG
python3 tools/sinh_bai_tienganh.py --lop 3 --tat-ca
python3 tools/sinh_ontap_tienganh.py --lop 3     # PHẢI chạy sau sinh_bai
python3 tools/sinh_kichban_noi.py --lop 3
python3 tools/sinh_dochieu_tienganh.py --lop 3
python3 tools/sinh_vietbai_tienganh.py --lop 3
# lời còn thiếu clip — gom từ CẢ hai nguồn rồi sinh một lượt:
python3 tools/video/kich_ban.py --lop 3 --thieu /tmp/thieu_video.json
python3 tools/sinh_dochieu_tienganh.py --lop 3 --thieu /tmp/thieu_doc.json
tools/tts/.venv/bin/python tools/tts/sinh_am.py \
    --vao /tmp/thieu_video.json \
    --ra web/public/content/tienganh/audio \
    --so web/public/content/tienganh/lop3_am.json
tools/tts/.venv/bin/python tools/video/dung_video.py --tat-ca --lop 3
cd web && npm test
```

⚠ `sinh_am.py --so` GỘP vào sổ cũ, không ghi đè. Chỉ `--lam-lai` mới quét sạch.
⚠ Đổi nhóm nghĩa là **đổi tên tệp video**. Dựng lại xong phải xoá tệp mồ côi —
`tienganh_video.test.mjs` hỏi hai chiều nên nó bắt được, nhưng chỉ sau khi đã dựng.
