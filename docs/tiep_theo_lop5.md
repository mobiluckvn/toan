# LỚP 5 QUYỂN 1 — CHUYỂN SANG VIDEO GIẢNG

**Đọc trang này trước khi gõ dòng nào.**

## Đang ở đâu

| | |
|---|---|
| Tổng | 56 bài lớn × 3 micro = **168 micro**, 14 chương (4 bài lớn / chương) |
| Đã xong | **108/168** — bài 1 tới 36, **HẾT chương 9** |
| Còn lại | 60 micro · 20 bài lớn · chương 10 tới 14 |
| Deploy | đã lên `ky-su-nhi.web.app` tới bài 32; **bài 33 tới 36 chưa deploy** |

Bốn quyển kia đã xong trọn: lớp 2 (71), lớp 3 (34), lớp 4 (95) — không còn bài chữ.

## Mở đầu buổi sau: làm bài 37

Chương 9 đã trọn. Bài 37 mở chương 10 — phần trăm. Chạy đúng nhịp bảy bước ở dưới. Cây làm việc đang SẠCH,
tám chương đầu đã deploy và đã đi thử bằng mắt trên bản thật.

```bash
git -C /Users/v/Documents/Code/web5/repo log --oneline -3   # commit cuối: deploy chương 8
```

## ⚠ HAI MÓN NỢ ĐANG TREO

**1. `khoaBai` của lớp 5 đang TẠM MỞ.** Bác nhờ mở hết để đi thử trọn quyển
(16-08-2026). Cờ ở `chuong_trinh.json`, khối `"ma": "lop5"`, hiện là `false`.
Thử xong phải bật lại `true` — sửa ở **cả hai nơi**: `data/chuong_trinh.json` và
`web/public/content/chuong_trinh.json`. Lý do bật lại đã ghi ngay cạnh cờ.

**2. `NO.lessons` trong `web/test/hinh_co_ai_ve.test.mjs`** phải **hạ 3 sau mỗi bài
lớn** — mỗi micro có video là bỏ một hình `mantra` chưa từng hiện lên. Đang là
**60**. Cổng tự in dòng nhắc `↓ lessons đã dọn bớt: … — hạ con số trong NO xuống`.

## Nhịp làm một bài lớn (đã chạy 32 lần)

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
# đoán giây theo thứ tự cảnh hay trượt. Muốn tìm ĐÚNG màn có hình thì quét màu:
# rút một loạt khung rồi đếm điểm mang màu riêng của hình ấy — ví dụ vạch
# `mucTB` của `san_bang` là #F9B233, `phan_so` tô #E6FAF5.

# ⑥ nối vào bài · THỨ TỰ NÀY KHÔNG ĐƯỢC ĐẢO
python3 tools/video_lop5.py
python3 tools/dinh_dang.py && python3 tools/bai_mau.py && python3 tools/goi_y.py
python3 tools/video_lop5.py     # chạy lại: phải báo "0 bài vừa thu gọn"

# ⑦ hạ NO.lessons đi 3, rồi
cd web && npm run build && npm test
```

Xong thì đi thử trên bản chạy, commit, deploy.

## Video phải dài 45–70 GIÂY, và cổng đo thật

`video_dai_bao_lau.test.mjs` đo bằng `ffprobe`, không đoán bằng dung lượng. Nhịp
thật của cả bộ: trung bình 58 giây.

**Phép ước lượng: một câu đọc ≈ 4,3 giây.** Nhắm **13–14 câu** cho một micro.

| | |
|---|---|
| dưới 13 câu | ngó chừng trần DƯỚI (bài 25 M2 viết 12 câu ra 45,2 giây, suýt lọt) |
| 13–14 câu | chỗ nên nhắm — mười sáu bài liền không phải sửa gì |
| 15 câu | SÁT trần trên; có 2 cảnh hình là gần như chắc vượt (bài 27 M3, bài 32 M3) |

Cảnh có `so_do_doan` hay `san_bang` ngốn thêm giây, vì lời tả hình dài hơn lời tả
phép tính. Cứ 15 câu kèm hai cảnh hình thì rút trước một câu, khỏi dựng lại.

Đếm trước khi dựng, khỏi mất công sinh âm lại:

```bash
python3 -c "
import sys; sys.path.insert(0,'tools/video')
import kich_ban_toan as K
for m in ('DL_KSN5Q1_B<N>_M1','DL_KSN5Q1_B<N>_M2','DL_KSN5Q1_B<N>_M3'):
    n = sum(len(c['loiAm']) for c in K.kich_ban(m)['canh'])
    print(m, n, 'câu → ước', round(n*4.3), 'giây')
"
```

Rút bằng cách **gộp hai câu đọc thành một**, đừng bỏ ý. Mỗi câu bỏ đi bớt được
khoảng 4 giây. Cũng gộp được hai màn cùng một bảng tra thành một màn.

⚠ Cổng ấy CHỈ NIÊM PHONG món nợ cũ (`NO_DAI = 7` video lớp 2·4 đã deploy). Video
MỚI không được nợ — thêm một cái vượt 70 giây là cổng đỏ ngay.

## Ba chỗ nữa dễ lọt, chỉ lộ khi rút khung hình ra nhìn

1. **Chữ tràn ra ngoài khung.** Ô "Thay số vào thử" của màn `cong_thuc` từng đóng
   cứng cao 120px — vừa đúng MỘT dòng. Câu dài hơn thì dòng thứ hai rơi xuống dưới
   đáy khung. **72 trong 419 màn công thức của cả bốn quyển đã lên bản thật như
   thế.** Nay khung giãn theo số dòng, và có cổng `chu_co_lot_trong_khung.test.mjs`
   đo bằng chính bộ chữ của bộ vẽ.
2. **Chuỗi `y_toan` không khai `buoc` thì hiện "Bước 1 trên 1".** Đặt ngay sau màn
   "Bước 3 trên 3" là đọc ra như tụt về đầu. Khai đủ số bước cho cả chuỗi, hoặc xếp
   màn không đánh số lên TRƯỚC chuỗi.
3. **Hai băng `phan_so` LUÔN dài bằng nhau** — nên chúng chỉ dùng được khi hai phân
   số đo trên CÙNG một cái. Bài tỉ số ẩn (bài 20) so hai khay KHÁC cỡ, vẽ bằng
   `phan_so` là hình nói dối rằng A bằng B. Chỗ ấy dùng `so_do_doan`, có sẵn
   `phanBe` · `phanLon` để chia ô đều nhau, `hienHieu` tô chỗ nhô ra, `chuTong` vẽ
   ngoặc ôm cả hai.
4. **Chương tổng – hiệu thì dùng `so_do_doan`** — nó được viết riêng cho chương này.
   `hienHieu` tô khúc dôi ra màu vàng, `chuTong` vẽ ngoặc ôm cả hai đoạn,
   `themVaoBe` vẽ nét đứt bù cho bằng đoạn lớn (đúng đường "(tổng + hiệu) : 2"), và
   `botOLon` tô khúc hiệu màu đỏ cho đường bớt ra. Hai màn đặt cạnh nhau là kể trọn
   cả hai đường về một đáp.

   ⚠ **Đặt hai màn cạnh nhau thì PHẢI khai `thangDo`.** Mặc định mỗi màn tự chuẩn
   hoá theo đoạn dài nhất CỦA NÓ, nên khúc hiệu 24 ở màn "sau 5 năm" vẽ ngắn hơn ở
   màn "hôm nay" — hình nói ngược lại đúng điều lời đang dạy. Khai `thangDo` bằng giá
   trị lớn nhất của cả cụm thì mọi màn chung một thước. Lỗi thật, bắt được ở bài 28,
   và bài 32 M3 sống nhờ nó: hai hồi của câu chuyện phải vẽ hộp ĐỨNG IM dài y hệt
   nhau, không thì hình nói ngược lại đúng điều lời đang dạy.

   `phanBe` · `phanLon` chia đoạn thành ô đều nhau — đó là hình của chương 8 (tổng –
   tỉ): kẻ ô ra thì bé ĐẾM được tổng số phần, thứ mà cả chương đứng hay đổ ở đó.
   Nhưng `so_do_doan` chỉ vẽ được HAI đoạn — bài ba số thì dùng `day_so` (dãy phần,
   dãy đáp) hoặc `san_bang` (ba cột, thấy luôn tỉ lệ).
5. **Chương trung bình cộng thì dùng `san_bang`**, không phải `day_so`. Nó vẽ cột
   cao thấp kèm vạch `mucTB`, nên đặt hai màn cạnh nhau là bé THẤY vạch nhích lên
   (bài 22 M1: ba cột mốc 26, rồi bốn cột mốc 29) hoặc thấy vạch đứng im (M2: cột
   thứ tư chạm đúng vạch). `deu=True` vẽ trạng thái đã san. `so` phải là SỐ, không
   phải chuỗi — bộ vẽ có gọi `sum(so)`.
6. **`day_so` ghi nhãn hàng là "số"** — sai nghĩa khi hàng ấy không phải số của đề.
   Bài 21 vẽ dãy PHẦN LỆCH (−3 +3 +1 −1) mà nhãn vẫn ghi "số" thì bé đọc ra một dãy
   số không có trong đề nào cả. Nay khai `nhanHang` để đổi.
7. **`giua()` ngắt dòng theo DẤU CÁCH**, nên `7/8 = 0,875` bị xẻ đôi giữa hai dòng.
   Viết liền `7/8=0,875` thì mỗi phép là một cụm không tách được.

Và một việc dọn: **rút lời xong thì `sinh_am.py` để lại clip mồ côi** — nó chỉ sinh
thêm, không bao giờ xoá. Sau mỗi đợt, xoá đúng những clip đợt này sinh ra mà sổ tra
không còn nhắc tới (đối chiếu `git ls-files --others` với mọi `*_am.json`). Đừng đụng
95 clip mồ côi CŨ trong kho — chúng có từ các đợt trước, và chưa cổng nào canh.

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
