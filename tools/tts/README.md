# Dây chuyền âm thanh môn Tiếng Anh

Hai model, cùng họ Kokoro, cùng giấy phép Apache-2.0, cùng đầu ra 24 kHz.

| | model | giọng mặc định | dùng cho |
|---|---|---|---|
| tiếng Anh | `hexgrad/Kokoro-82M` · `lang_code='b'` | `bf_emma` | 60 từ · 55 câu |
| tiếng Việt | [`iamdinhthuan/Kokoro-Vietnamese`](https://github.com/iamdinhthuan/Kokoro-Vietnamese) · G2P `vig2p` | `diem_trinh` | lệnh bài · nghĩa từ · lời giảng |

## Cài

```bash
brew install python@3.12 espeak-ng
bash tools/tts/cai_dat.sh
```

Gần **1 GB**, để trong `tools/tts/.venv/` — **không commit** (xem `.gitignore`).
Máy mới thì chạy lại `cai_dat.sh`.

Môi trường này **tách hẳn** với Python 3.9 hệ thống mà `figforge/` và `tools/*.py`
đang dùng. Cài đè lên python hệ thống là bốn quyển Toán mất đường dựng lại hình.

## Sinh âm

```bash
# 10 clip mẫu để nghe trước
tools/tts/.venv/bin/python tools/tts/sinh_am.py --nghe-thu

# sinh thật
tools/tts/.venv/bin/python tools/tts/sinh_am.py \
    --vao data/tienganh/lop1_loi.json \
    --ra  web/public/content/tienganh/audio \
    --so  web/public/content/tienganh/lop1_am.json
```

Đầu vào là danh sách `{ id, chu, tieng }` với `tieng` là `"en"` hoặc `"vi"`.

## Ba điều dễ vấp

### 1 · Mỗi dòng chỉ MỘT thứ tiếng

Kokoro-VI chỉ đọc tiếng Việt, Kokoro-82M chỉ đọc tiếng Anh. Dòng lẫn hai thứ tiếng
thì model nào đọc cũng sai:

```
✗  "Con bấm vào hình con dog nhé."   → Kokoro-VI đọc "dog" theo vần Việt: /dóc/
✓  "Con bấm vào hình"  [vi]  +  "dog"  [en]  +  "nhé"  [vi]   → nối bằng ffmpeg
```

`sinh_am.py` **từ chối** dòng lẫn tiếng chứ không đọc bừa, và cổng
`web/test/tienganh_am.test.mjs` soát danh sách trước khi sinh. Đọc bừa thì ra 520
clip hỏng mà không ai biết cho tới lúc bé nghe.

Ngoài lề: hai giọng khác nhau lại **hoá hay** — bé nghe là biết ngay đâu là tiếng
Việt, đâu là tiếng Anh. Đừng cố tìm một giọng đọc cả hai.

### 2 · Giọng tiếng Anh phải là ANH-ANH

Bản đồ tri thức khai IPA chuẩn Anh-Anh: `/ɒ/` (dog) · `/ɑː/` (car) · `/eə/` (hair).
Đọc bằng giọng Anh-Mỹ thì bé nghe `/dɔːɡ/`, `/kɑːr/` — **lệch với phiên âm đang hiện
ngay trên màn hình**. Nên `lang_code='b'` và giọng `bf_*`/`bm_*`, không phải `'a'`.

### 3 · Ghim `numpy<2`

torch bản CPU cho Python 3.12 hiện là 2.2.2, biên dịch với NumPy 1.x. Để pip tự kéo
NumPy 2 thì mỗi lần `import torch` nhả ra một trang cảnh báo `_ARRAY_API not found`
rồi **vẫn chạy tiếp** — kiểu hỏng khó chịu nhất vì nó không dừng, chỉ làm mọi đầu ra
lẫn cảnh báo. `cai_dat.sh` đã ghim sẵn.

## Sổ tra

`sinh_am.py --so` ghi lại mỗi clip do **model nào** sinh, **giọng nào**, và **vân tay
sha256 của chữ**. Sửa một câu thì vân tay đổi → biết đúng clip nào phải sinh lại.
Không có sổ thì sáu tháng nữa phải đoán, hoặc sinh lại cả 520 clip.

## Kích thước thật

Đo trên 10 clip mẫu: trung bình **~20 KB/clip** (mp3 64 kbps mono, 24 kHz).
Cả quyển lớp 1 ~520 clip ≈ **10 MB**.
