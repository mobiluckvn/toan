# LỚP 5 QUYỂN 1 — CHUYỂN SANG VIDEO GIẢNG

**Đọc trang này trước khi gõ dòng nào.**

## Đang ở đâu

| | |
|---|---|
| Tổng | 56 bài lớn × 3 micro = **168 micro**, 14 chương (4 bài lớn / chương) |
| Đã xong | **165/168** — bài 1 tới 55 |
| Còn lại | **3 micro · bài 56** — làm xong là HẾT QUYỂN |
| Deploy | đã lên `ky-su-nhi.web.app` tới bài 32; **bài 33 tới 55 chưa deploy** |

Bốn quyển kia đã xong trọn: lớp 2 (71), lớp 3 (34), lớp 4 (95) — không còn bài chữ.

## Mở đầu buổi sau: làm bài 56 — bài CUỐI của quyển

Bài 56: M1 tàu dài qua mốc và qua cầu · M2 khi cái mốc cũng biết chạy · M3 hai kim
đồng hồ đuổi nhau. Làm xong là **hết quyển 168/168**. M1 dùng `so_do_doan` (cầu là
đoạn ngắn, quãng tàu đi là đoạn dài, phần dôi ra chính là thân tàu); M2 dùng
`duong_di`; M3 dùng `dong_ho` sẵn có.

Xong bài 56 thì còn HAI việc: bật lại `khoaBai`, và deploy trọn bài 33 tới 56.

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
**3**. Cổng tự in dòng nhắc `↓ lessons đã dọn bớt: … — hạ con số trong NO xuống`.

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
7. **`hinh_thang` là cảnh THÊM ngày 17-08** cho bài 48 — `dayLon` · `dayBe` · `cao` ·
   `duongCheo` (kẻ hai chéo và chấm giao điểm) · `nhanCao` (vẽ đường cao nét đứt kèm
   ô vuông góc). ⚠ Tỉ chỗ giao điểm rất dễ viết ngược: nó cách đáy BÉ một phần
   `dayBe`, cách đáy LỚN một phần `dayLon` — tức nằm GẦN đáy bé hơn.
8. **`tam_giac` cho `dinh` ra ngoài khoảng 0–1** thì chân đường cao rơi ngoài đáy và
   bộ vẽ tự kéo dài đáy bằng nét đứt — đúng ca tam giác tù, chỗ bé hay hoảng nhất.
9. **`duong_di` vẽ đoạn đường và hai mũi tên** (thêm 17-08 cho chương 14). Cùng
   hướng là đuổi (chia HIỆU), chụm đầu là gặp (chia TỔNG) — hai đề chỉ khác hai chữ
   cuối câu nên đọc lướt là chia nhầm, mà vẽ mũi tên ra thì không lẫn được.
   `toTu`/`toDen` tô khúc đi trước cho bài khác giờ; `sao` đánh dấu điểm gặp.
   ⚠ Đoạn vẽ ra là CÁI GÌ thì `nhanDai` phải nói đúng cái ấy: bản đầu của bài 54 M1
   đặt hai mũi tên ở 0,05 và 0,35 rồi vẫn kẻ ngoặc "cách nhau 5 km" ôm cả đoạn —
   hình bảo đoạn đường dài năm cây trong khi hai người cách nhau chưa tới một phần
   ba đoạn ấy. Đoạn phải CHÍNH LÀ khoảng cách, hai mũi tên đặt đúng hai đầu.
   ⚠ Tên đầu đoạn dài hơn một chữ cái thì lề hai bên không chứa nổi — bộ vẽ nay tự
   cho tên dài leo lên trên vạch, và kẹp mũi tên khỏi chạy quá mép.
10. **`tam_giac_ct` là tam giác CÔNG THỨC, không phải hình học** (thêm 17-08 cho bài
   53). Ô trên chia cho ô dưới, hai ô dưới nhân nhau, nên `che='tren' | 'trai' |
   'phai'` là lộ ngay phép tính cho ô ấy. Ba màn liên tiếp cùng một hình khác mỗi
   ô bị che thì cả chương chuyển động rút lại còn một hình.
11. **Hộp vẽ đặc thì có viên NẤP SAU LƯNG.** `khoi` lối `chong` vẽ hai nhân hai
   nhân hai ra bảy viên nhìn thấy được — viên thứ tám khuất. Lời đọc nói tám mà bé
   đếm ra bảy là hình nói ngược lời (bài 52 M1, bắt được khi rút khung hình). Bài
   nào cần bé ĐẾM ĐỦ thì vẽ lối `tang`; lối `chong` để dành cho bài cần thấy khối
   ĐẶC, ví dụ bài sơn mặt ngoài — ở đó lõi khuất mới đúng ý.
12. **`khoi` có `kieu='ao'` — bốn mặt bên trải thành MỘT hàng** (thêm 17-08 cho bài
   51). Nhánh `trai` bày sáu mặt theo hình chữ thập, đúng cái hộp nhưng KHÔNG kể
   được điều bài dạy: chiều dài tấm áo bằng chu vi đáy. `ao` xếp trước · hông · sau
   · hông liền nhau rồi kẻ ngoặc đo suốt. `hangNap` bày thêm nắp và đáy rời;
   `boMat=['nắp']` gạch chéo mặt không có, `loiBo` nói VÌ SAO bỏ. ⚠ Mặc định `loiBo`
   là "KHÔNG có" — hợp thùng không nắp, nhưng SÀN phòng thì vẫn có, chỉ không quét;
   để mặc định ở đấy là hình nói sai. Tên mặt bị gạch đặt DƯỚI ô, vì đặt vào giữa
   thì hai vạch chéo cắt nát chữ (bắt được khi rút khung hình bài 51 M2).
13. **`hinh_tron` khai `rTrong` (tỉ lệ 0–1) thì vẽ thêm vòng trong** — cảnh vành khăn
   của bài 50. Khai bằng TỈ chứ không phải bán kính thật, để hai vòng chung một
   thước; khai bán kính thật là hai vòng vẽ theo hai thang, hình nói dối.
14. **`so_do_ven` chỉ vẽ được HAI vòng** — bài Ven BA vòng (bài 44 M2) không có hình,
   phải diễn bằng công thức. Đừng bịa hình ba vòng.
15. **`giua()` ngắt dòng theo DẤU CÁCH**, nên `7/8 = 0,875` bị xẻ đôi giữa hai dòng.
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
