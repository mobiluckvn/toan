# LỚP 5 QUYỂN 1 — CHUYỂN SANG VIDEO GIẢNG

**Đọc trang này trước khi gõ dòng nào.**

## Đang ở đâu

| | |
|---|---|
| Tổng | 56 bài lớn × 3 micro = **168 micro**, 14 chương (4 bài lớn / chương) |
| Đã xong | **48/168** — bài 1 tới 16, hết chương 4 |
| Còn lại | 120 micro · 40 bài lớn · chương 5 tới 14 |
| Deploy | đã lên `ky-su-nhi.web.app` tới bài 16 |

Bốn quyển kia đã xong trọn: lớp 2 (71), lớp 3 (34), lớp 4 (95) — không còn bài chữ.

## ⚠ HAI MÓN NỢ ĐANG TREO

**1. `khoaBai` của lớp 5 đang TẠM MỞ.** Bác nhờ mở hết để đi thử trọn quyển
(16-08-2026). Cờ ở `chuong_trinh.json`, khối `"ma": "lop5"`, hiện là `false`.
Thử xong phải bật lại `true` — sửa ở **cả hai nơi**: `data/chuong_trinh.json` và
`web/public/content/chuong_trinh.json`. Lý do bật lại đã ghi ngay cạnh cờ.

**2. `NO.lessons` trong `web/test/hinh_co_ai_ve.test.mjs`** phải **hạ 3 sau mỗi bài
lớn** — mỗi micro có video là bỏ một hình `mantra` chưa từng hiện lên. Đang là
**120**. Cổng tự in dòng nhắc `↓ lessons đã dọn bớt: … — hạ con số trong NO xuống`.

## Nhịp làm một bài lớn (đã chạy 16 lần)

```bash
# ① đọc nội dung ba micro
python3 - <<'PY'
import json
for m in ('M1','M2','M3'):
    d=json.load(open(f'web/public/content/lessons/DL_KSN5Q1_B<N>_{m}.json',encoding='utf-8'))
    print(d['id'], d['title'])
    for x in d['knowledgeCore']['statements']: print('  ', x['text'][:120])
    for s in d['videoSpec']['scenes']: print('  [', s.get('templateHint'), ']', (s.get('voiceover') or '')[:145])
PY

# ② viết ba hàm kb5_* trong tools/video/kich_ban_toan.py, khai vào BO theo MÃ bài
# ③ cổng kịch bản (bắt khoá rơi mất, từ cấm, câu dài, thứ tự màn kết)
cd web && node test/canh_video_khong_roi_chu.test.mjs

# ④ sinh âm rồi dựng video
tools/tts/.venv/bin/python tools/video/dung_video_toan.py --quyen lop5 --loi
tools/tts/.venv/bin/python tools/tts/sinh_am.py --vao data/lop5_loi_video.json \
    --ra web/public/content/toan/audio --so web/public/content/toan/lop5_am.json
for m in DL_KSN5Q1_B<N>_M1 DL_KSN5Q1_B<N>_M2 DL_KSN5Q1_B<N>_M3; do
  tools/tts/.venv/bin/python tools/video/dung_video_toan.py --quyen lop5 --bai $m </dev/null
done

# ⑤ RÚT KHUNG HÌNH RA NHÌN — bước không được bỏ
ffmpeg -ss <giây> -i <video>.mp4 -frames:v 1 khung.png -y

# ⑥ nối vào bài · THỨ TỰ NÀY KHÔNG ĐƯỢC ĐẢO
python3 tools/video_lop5.py
python3 tools/dinh_dang.py && python3 tools/bai_mau.py && python3 tools/goi_y.py
python3 tools/video_lop5.py     # chạy lại: phải báo "0 bài vừa thu gọn"

# ⑦ hạ NO.lessons đi 3, rồi
cd web && npm run build && npm test
```

Xong thì đi thử trên bản chạy, commit, deploy.

## Bốn chỗ vấp lặp đi lặp lại

1. **`buoc`/`soBuoc` chỉ dùng được ở cảnh `y_toan`.** Khai ở `tach_so`, `day_so`,
   `so_do_ven`, `khoi`, `bang_hang`… là rơi im lặng. Đợt nào cổng cũng bắt vài chỗ.
2. **Màn ngay trước `ket` bắt buộc là `cong_thuc`** — luật `soi()` trong
   `kich_ban_toan.py`, bác chốt 14-08.
3. **`khuyet` của cảnh `khoi` là DANH SÁCH theo từng tầng**, không phải một số.
4. **Sách lớp 5 đầy chữ trong `TU_CAM`**: mật thư · thám tử · tuyệt kỹ · Gauss ·
   thần chú. Gọi thẳng bằng chữ toán — đó chính là điều bác chốt khi bỏ nhân vật:
   giữ Ý của sách, bỏ VỎ của sách.

## Về `videoSpec`

Mỗi micro có sẵn khối `videoSpec` viết tay trong sách: 840 cảnh, trung bình 87
giây, đủ lời đọc · chữ trên màn · mô tả hình · thời lượng từng cảnh.

**Rất tốt để lấy Ý và SỐ LIỆU. Không dùng thẳng được**, vì nó viết cho video dọc
9:16 có hoạt hình, và so với luật của mình thì: 363/840 cảnh dính `TU_CAM`, 191
cảnh gọi tên nhân vật, 532/840 câu dài quá 130 chữ, thời lượng vượt mốc 45–70 giây.

Đã cân nhắc viết bộ **dịch máy** từ `videoSpec` sang kịch bản. Bác chốt **làm bằng
tay như lớp 3** (16-08). Lý do vẫn đúng: chỗ hỏng thật của cả bảy chương lớp 3 và
mười sáu bài lớp 5 đều nằm ở **hình có phục vụ được lời không** — thứ máy dịch
không tự lo được.

## Bốn khác biệt của lớp 5 so với ba quyển kia

| | |
|---|---|
| Đơn vị | **một video một MICRO**, không gộp về bài lớn |
| Nguồn | mỗi micro có sẵn `videoSpec` (xem trên) |
| Chặng giảng | có thêm bước **`check`** — câu hỏi tương tác, **phải giữ** |
| Bộ nối | không có bước dựng khuôn → `tools/video_lop5.py` riêng, **idempotent** |

`video_lop5.py` thu bài về đúng hình dạng lớp 4: `statements` rỗng · `mantra` rỗng
· `vocabulary` rỗng · `lecture.screens` chỉ giữ màn có `item` · `figureSpec` chỉ
giữ hình `item:`. Bỏ `vocabulary` là bắt buộc — `flow.js` dựng bước câu chốt nếu
CÓ MỘT TRONG HAI, và mục đầu của danh sách từ là "nhân vật: Su Kem, Trí Long…".
