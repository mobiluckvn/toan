# TIẾNG ANH LỚP 1 — điểm dừng và việc tiếp theo

Ghi 12-08-2026. Đọc tệp này TRƯỚC khi làm tiếp môn Tiếng Anh.

Quyển đầu tiên của môn thứ hai đã **chạy được thật**: bé đăng nhập, học trọn một
bài, tiến độ lên máy chủ, xoá sổ tại máy rồi tải lại vẫn còn. Chưa deploy.

---

## 1 · ĐANG CÓ GÌ

```
16 unit · 4 chương · 395 câu luyện tập · 80 câu sát hạch
531 clip âm (Kokoro Anh-Anh + Kokoro-Vietnamese)
37 video mp4 · 34 phút
60 hình: 53 emoji + 7 vẽ tay SVG
45 tệp cổng · 0 FAIL
```

### Dây chuyền, theo thứ tự chạy

```
data/ban_do_tieng_anh.json          bản đồ gốc — KHÔNG SỬA
  + data/tienganh/lop1_bu.json      phần bù soạn tay (nghĩa · IPA · vai · hình · dạy)
  ↓  tools/chuan_tienganh.py        chuẩn hoá 3 khuôn lớp 1·2·3 về một
data/tienganh/chuan_lop1.json
  ↓  tools/sinh_bai_tienganh.py     sinh 16 bài
web/public/content/ta1/DL_TA1_B*.json
  ↓  tools/video/kich_ban.py        kịch bản cảnh
  ↓  tools/tts/sinh_am.py           sinh clip tiếng (2 model)
  ↓  tools/video/dung_video.py      Pillow + ffmpeg → mp4
web/public/content/tienganh/{audio,video}/
```

**Chạy lại toàn bộ:**

```bash
python3 tools/chuan_tienganh.py --lop 1
python3 tools/sinh_bai_tienganh.py --lop 1 --tat-ca
# gom lời còn thiếu → sinh âm → nhập vào sổ (xem tools/tts/README.md)
tools/tts/.venv/bin/python tools/video/dung_video.py --tat-ca
cd web && npm test
```

---

## 2 · VIỆC TIẾP THEO, THEO THỨ TỰ CHẶN ĐƯỜNG

### (a) ~~Nối video vào app~~ — XONG 12-08
Sáu chặng gộp còn năm, video dẫn đường. Chữ trên màn từ **2 029 xuống 310 ký tự**;
mọi giải thích lui vào **Góc bố mẹ**, gập sẵn. Sát hạch dựng lại thành nghe–nhìn,
không còn chữ nào phải đọc. Phần NÓI (từ · câu · hội thoại) đã có.

### (b) Deploy luật Firestore — bé chưa dùng thật được
```bash
firebase deploy --only firestore:rules
```
Chưa deploy thì `progressTA` và `hocBaTA` bị `match /{document=**}` chặn, và Firestore
**từ chối trong im lặng**. Luật đã thử trên bộ giả lập (14 phép kiểm, xem
`docs/di_thu_gia_lap.md`) nhưng máy chủ thật vẫn chạy bộ luật cũ.

### (c) Soát lại 19 mẫu câu theo tiêu chuẩn "một video một việc"
Bác đã bắt được hai chỗ gộp mà cháu không thấy: cặp hỏi–đáp của U9 và U16. Còn ngờ:
* **U6** `It's a red pen.` — dạy cùng lúc *nó là* + *màu* + *đồ vật*: ba việc
* **U16 `_dap`** `I can see six.` — dùng khung `I can see` mà U14 mới là bài dạy nó,
  hai bài không nối với nhau

### (d) Bảy hình còn nợ
`gate` · `head` · `hair` · `top` · `lake` · `run` · `wash` đang dùng SVG vẽ tay trên
màn hình, nhưng **video thì hiện thẻ chữ, không hiện hình** — vì Pillow không dựng
được SVG. Muốn video có hình thì phải vẽ lại bằng Pillow hoặc thêm bộ chuyển SVG.

### (e) Kỳ ôn tập chương — `hocBaTA` đang rỗng
`ta1/ontap.json` đã khai 4 kỳ, `luuMucHocBa()` đã có, **chưa ai gọi** vì màn kỳ ôn
tập chưa dựng.

### (f) Bảng xếp hạng · bảng cô giáo
Hàm nền chỉ đếm sao của Toán, nên môn này trả `null`. Muốn mở thì sửa
`functions/src/bangxephang.js` biết đếm cả Tiếng Anh.

### (g) ~~Phần NÓI có chấm~~ — XONG 12-08
`lib/chamnoi.js` (57 phép kiểm) + `lib/nghenoi.js` (Web Speech). Nói từ · nói câu ·
hội thoại 16 kịch bản. ⚠ Chrome gửi tiếng bé lên máy chủ Google — đổi sang Whisper
thì chỉ sửa `nghenoi.js`.

### (h) Chưa thử được bằng MICRO THẬT
Toàn bộ 57 phép kiểm chấm trên chữ giả lập những gì STT trả về. Đường
micro → Web Speech → bộ chấm chỉ người thật thử mới biết.

---

## 3 · MƯỜI CÁI BẪY ĐÃ DÍNH THẬT — đừng dẫm lại

Tất cả đều **cổng xanh mà vẫn sai**. Mỗi cái nay có phép kiểm canh.

| # | bẫy | dấu hiệu |
|---|---|---|
| 1 | `position: "initial"` khai cho cả 16 phonics | 20 từ có âm ở GIỮA; vị trí âm là chuyện của TỪNG TỪ, không phải của unit |
| 2 | slot phẳng, không phân vai | `"It's a pen bell."` |
| 3 | thay chuỗi trong câu ví dụ thay vì điền vào công thức | `"facePoint to your hand."` |
| 4 | giao ước `soMon.js` ghi sai kiểu tham số | kệ sách hiện "0 unit" cho quyển 16 bài |
| 5 | `napSoAm` nhớ cả lần hỏng | cả quyển câm, màn hình vẫn đủ chữ |
| 6 | sổ âm nằm ở `data/` mà app đọc `public/` | `curl` trả **200** vì máy chủ dev trả `index.html` thay thế |
| 7 | hai hàm đặt mã clip ở hai ngôn ngữ | lệch một gạch dưới → mọi nút nghe biến mất |
| 8 | `CauHoi` không có `key` | trắng màn hình giữa bài, chỗ nối ★ sang ★★ |
| 9 | lời giải thích "chỗ dễ nhầm" ghim cứng một ví dụ | 10/16 bài câu "sai" trùng hệt câu đúng |
| 10 | gom clip ở một script, kịch bản dùng ở chỗ khác | đổi câu là lệch; nay kịch bản tự khai chữ (`loiAm`) |

**Ba lần đọc nhầm dấu hiệu** (ghi ở `docs/di_thu_gia_lap.md`): `curl 200` không có
nghĩa là tệp có thật · đọc Firestore quên token bị từ chối rồi hiện thành "0 tài
liệu" · bộ đếm lỗi bằng 0 có thể là "chưa từng chạy" chứ không phải "chạy trót lọt".

---

## 4 · NHỮNG QUYẾT ĐỊNH ĐÃ CHỐT — đừng mở lại nếu không có lý do mới

* **Kokoro** sinh sẵn tệp; tiếng Việt dùng bản cộng đồng `Kokoro-Vietnamese`
* **Bỏ phần âm phonics rời** — dạy âm qua từ ví dụ
* **Không nhân vật** Trí Long · Su Kem: quyển dựng cho MỌI học sinh
* **Hình = emoji + 7 SVG vẽ tay**; `figforge` chỉ dựng sơ đồ toán, không vẽ được vật
* **Lớp 1 chưa dạy số ít / số nhiều** — để bài khác dạy
* **Mỗi dòng chỉ MỘT thứ tiếng** — hai model, trộn là đọc sai
* **Giọng Anh-Anh** (`bf_emma`), vì bản đồ khai IPA Anh-Anh
* **Bài đã học không xoá được** — bằng chứng học tập, luật Firestore chặn cả chính chủ

---

## Đọc kèm

* `docs/lop1_tieng_anh_khao_sat_va_thiet_ke.md` — khảo sát bản đồ và thiết kế bài
* `docs/di_thu_gia_lap.md` — bật bộ giả lập, thử luật thật
* `tools/tts/README.md` — dây chuyền âm, ba điều dễ vấp
* `docs/tach_hai_mon.md` — kiến trúc ba vùng
