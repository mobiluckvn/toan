# Kế hoạch sản xuất video cho toàn bộ Toán lớp 4

**Viết 14-08-2026, sau khi bác duyệt cụm dãy số (B13–B17).**

Khuôn đã chốt và đã chạy thật trên `ky-su-nhi.web.app`. Tài liệu này ghi lại **đúng
cách làm ấy**, kèm số đo thật từ năm bài đầu, để nhân ra 44 bài còn lại mà không
phải mò lại.

---

## 1 · Khuôn đã chốt — một bài trông thế nào

```
MỞ BÀI        video 45–70 giây          ← thay CẢ mở bài lẫn bài giảng
BÀI MẪU       một bài giải từng bước    ← cùng ví dụ với video
LUYỆN TẬP     9 câu, mức ★ ★★ ★★★       ← bám từng nấc video
SÁT HẠCH      5 câu
```

Bài không còn chữ giảng nào. `chuyenMoBai` · `dichMoHinh` · `khamPha` · `lapSoi`
đều RỖNG; `mantra` rỗng nên màn "NGUYÊN TẮC CẦN NHỚ" cũng biến mất. Thanh chặng còn
bốn nhãn.

### Video gồm những cảnh nào

| cảnh | việc |
|---|---|
| `bia` | tên bài, một câu mời |
| `day_so` | vẽ dữ liệu ra thành ô, ô đang nói tới thì sáng |
| `y_toan` | một ý một màn, có chấm tiến độ |
| **`cong_thuc`** | **công thức đóng khung + một dòng thay số** |
| **`cong_thuc`** | **nhắc lại công thức, ngay trước lúc kết** |
| `ket` | chốt, mời làm bài |

---

## 2 · Mười luật, mỗi luật là một lỗi đã xảy ra

**1 · KHÔNG chuyện dẫn.** Bản đầu đọc trọn "chuyện mở bài" của giáo án — 300 chữ về
bạn Mai và cậu giao báo, trước khi tới được chữ "dãy số". Bác xem xong bảo *"mở bài
quá nhiều"*. Video mở ra là vào ngay ví dụ.

**2 · KHÔNG ẩn dụ, KHÔNG nhân vật.** Không "kỹ sư", "thám tử", "tuyệt kỹ"; không Su
Kem, Trí Long; và không cả những ví von dễ thương như "bước chân", "dấu vân tay của
dãy". Mỗi ẩn dụ là một lớp bé phải bóc trước khi tới được cái cần học. Cổng
`TU_CAM` chặn lúc dựng, `video_toan.test.mjs` chặn cái đã dựng ra.

**3 · Một ví dụ chạy suốt cả cụm.** Năm bài dãy số đều dùng `5, 10, 15, 20, 25`. Bé
không phải làm quen dữ liệu mới ở mỗi bài, và nhận ra ngay khi nó xuất hiện lại
trong bài tập.

**4 · KÝ HIỆU Ở MÀN, CHỮ Ở LỜI.** Luật gốc của cả chuyện. Màn hình đọc bằng MẮT nên
ký hiệu là cách gọn nhất; máy đọc bằng TIẾNG nên ký hiệu là cách sai nhất. Mỗi cảnh
khai hai thứ tách nhau: `chuChinh`/`congThuc` để hiện, `loi` để đọc.

Lời đọc phải sạch: không ký tự đặc biệt, **không chữ số** (đọc thành chữ), **không
chữ cái đứng lẻ** (`n` đọc theo tiếng Anh), câu không quá 130 chữ.

**5 · CÔNG THỨC PHẢI HIỆN LÊN.** Nghe một câu dài rồi trôi qua thì bé không giữ được
gì. Công thức đóng khung, bên dưới một dòng thay số.

**6 · NHẮC LẠI TRƯỚC KHI KẾT.** Một màn "Con nhớ kỹ công thức này nhé", đọc lại kèm
câu VÌ SAO — *"cộng một vì số chỗ luôn nhiều hơn số lần cộng đúng một"*.

**7 · BÀI TẬP BÁM TỪNG NẤC VIDEO.** Ba câu đầu dùng chính ví dụ trong video. Gợi ý
nói cùng thứ tiếng với clip — không thì bé nghe một đằng đọc một nẻo.

### Ba luật bác ra thêm ở đợt 2 (14-08)

**8 · MỘT VIDEO — MỘT VẤN ĐỀ.** Tách bài nhỏ hơn nữa. Bài nào còn ôm hai việc thì
cắt đôi, và bài tập ăn theo đúng một việc ấy. Đây là lý do chương 3 tách **4 bài
thành 9**: bốn dấu hiệu chia hết đang nhồi chung, mà khái niệm gốc "chia hết là gì"
thì chưa bài nào định nghĩa — đúng lỗi của cụm dãy số trước khi sửa.

**9 · HÌNH MINH HOẠ CHO CHỖ KHÓ HIỂU.** Chỗ nào nói bằng lời mà bé phải tưởng tượng
thì vẽ ra. Dựng qua `hinh_ve.json` để màn hình và video cùng một nguồn — đừng vẽ
riêng cho video, sẽ lệch.

**10 · CÔNG THỨC PHẢI GIẢI THÍCH TỪNG THÀNH PHẦN, VÀ VÌ SAO SUY RA ĐƯỢC.** Luật 5
mới bắt công thức HIỆN LÊN; luật này bắt nó phải HIỂU ĐƯỢC. Mỗi chữ trong công thức
là một khái niệm phải gọi tên trước. Rồi phải nói vì sao công thức ấy đúng — không
phải "con nhớ nhé". Ví dụ đã làm: *"cộng một vì số chỗ luôn nhiều hơn số lần cộng
đúng một"*. Bài "vì sao các dấu hiệu chia hết lại đúng" tách hẳn ra một bài riêng
cũng vì luật này.

---

## 3 · Số đo thật, từ năm bài đầu

| | mỗi bài | 44 bài còn lại |
|---|---|---|
| kịch bản video viết tay | ~36 dòng | ~1 600 dòng |
| nội dung bài viết tay | ~163 dòng | ~7 200 dòng |
| clip tiếng | 13 clip | **572 clip** |
| video | 55 giây · 0,9 MB | **~40 phút · 40 MB** |
| câu hỏi | 14 (9 luyện + 5 quiz) | **616 câu** |

**Phần nào máy làm, phần nào người làm:**

| việc | ai làm | ghi chú |
|---|---|---|
| kịch bản video | **NGƯỜI** | chỗ tốn nhất, và không rút ngắn được — xem §5 |
| dựng cảnh → mp4 | máy | `dung_video_toan.py`, vài giây một bài |
| sinh tiếng | máy | Kokoro, ~1 phút cho 13 clip |
| bài tập + gợi ý + lời chào | **NGƯỜI** | |
| ô nhập chấm máy | **NGƯỜI** khai, máy soi | cổng đối chiếu với lời chữa |
| dựng bài, gắn hình, gắn gợi ý | máy | đúng thứ tự ở §6 |
| dọn phần giảng cũ | máy | mục để rỗng, bộ dựng tự hiểu |

---

## 4 · Thứ tự làm — theo CHƯƠNG, không theo số bài

44 bài còn lại, 11 chương. Làm trọn từng chương rồi bác duyệt, vì bài trong một
chương dùng chung ví dụ và chung cách nói.

| đợt | chương | bài | vì sao xếp trước |
|---|---|---|---|
| 1 | 4 · Dãy số | B18 · B19 · B20 | **nối tiếp cụm vừa xong**, dùng lại đúng ví dụ 5·10·15·20·25 |
| ~~2~~ | ~~3 · Dấu hiệu chia hết~~ | **XONG 14-08** | 4 bài → **9 bài**, xem §12 |
| ~~3~~ | ~~5 · Trung bình cộng~~ | **XONG 14-08** | 3 bài → **6 bài**, xem §13 |
| ~~4~~ | ~~6 · Tổng - hiệu~~ | **XONG 14-08** | 4 bài → **7 bài**, xem §14 |
| ~~5~~ | ~~7 · Tổng - tỉ, Hiệu - tỉ~~ | **XONG 14-08** | 4 bài → **7 bài**, xem §15 |
| 6 | 1 · Số đến lớp triệu | B01–B04 | bài đầu quyển, bé mới vào |
| 7 | 2 · Bốn phép tính | B05–B08 | |
| 8 | 9 · Phân số | B38–B42 | cần kiểu cảnh vẽ phân số |
| 9 | 10 · Hình học | B43–B46 | cần kiểu cảnh hình — nặng nhất |
| 10 | 11 · Quãng đường | B47–B49 | |
| 11 | 8 · Bài toán lời văn | B32–B37 | **để cuối**: sáu bài, mỗi bài một phương pháp riêng, khó ra khuôn chung |

**Đợt 1 nên làm ngay**: ba bài ấy đang nằm ngay sau cụm vừa duyệt, và bé học tới đó
sẽ thấy hụt — bốn bài đầu chương có video, ba bài sau lại là tường chữ.

---

## 5 · Vì sao kịch bản KHÔNG sinh tự động được

Đã thử và đã hỏng. Bản đầu lấy thẳng chữ trong giáo án làm lời đọc. Sai từ gốc:
giáo án viết cho MẮT người lớn — có chuyện dẫn, câu dài, ngoặc và mũi tên. Cắt gọt
bao nhiêu cũng không thành lời giảng cho bé nghe.

Cái máy làm được là **dựng**: có kịch bản rồi thì mp4 ra trong vài giây. Cái người
phải làm là **quyết dạy gì trước, dạy gì sau, và nói bằng câu nào**.

Nhưng có ba thứ rút ngắn được thật:

1. **Kiểu cảnh dùng lại.** `day_so` · `y_toan` · `cong_thuc` phủ được phần lớn bài
   số học. Chương hình học và phân số cần thêm kiểu mới — làm một lần, dùng cho cả
   chương.
2. **Khuôn kịch bản cố định.** Bài nào cũng đi: *ví dụ cụ thể → đặt vấn đề → từng
   bước → công thức → thay số → nhắc lại → chốt.*
3. **Bài tập suy từ kịch bản.** Bảy nấc video thành bảy câu đầu; hai câu ★★★ là gộp
   và mở rộng.

---

## 6 · Chạy lại — ĐÚNG THỨ TỰ, sai là mất dữ liệu

```bash
python3 tools/day_so_lop4.py                    # nội dung bài (viết tay)
python3 tools/dung_khuon_chung_lop4.py --khai   # dựng bản cho app
python3 tools/gan_hinh_lop4.py                  # ⚠ SAU khi dựng
python3 tools/goi_y.py                          # ⚠ SAU khi dựng
tools/tts/.venv/bin/python tools/video/dung_video_toan.py --loi
tools/tts/.venv/bin/python tools/tts/sinh_am.py --vao data/lop4_loi_video.json \
    --ra web/public/content/toan/audio --so web/public/content/toan/lop4_am.json
#   ↑ nay BỎ QUA clip đã đúng — chỉ sinh câu mới. Đổi model hay giọng thì thêm
#     `--lam-lai` để sinh lại tất.
tools/tts/.venv/bin/python tools/video/dung_video_toan.py
cd web && npm test && npm run build
```

⚠ **Bẫy đã sập hai lần:** chạy lại bộ dựng là **mất** phần hình và gợi ý đã gắn —
`gan_hinh_lop4.py` và `goi_y.py` là bước SAU. Cổng bắt được (92 hình rơi, 441 câu
mất gợi ý), nhưng chỉ khi có ai chạy `npm test`.

---

## 7 · Cổng canh — 14 phép ở `video_toan.test.mjs`

Bài khai video mà thiếu tệp · video dựng rồi mà không bài nào dùng · clip tiếng
thiếu tệp · **ẩn dụ trong lời đọc** · **chữ số trong lời đọc** · **chữ cái đứng lẻ**
· **dấu nhân ăn vào chữ Việt** · câu quá 130 chữ · video quá hai phút · **có màn
công thức** · **có nhắc lại trước lúc kết** · màn mở bài có gọi Video · Video là
component chung.

Cộng hai cổng đã nới **có điều kiện**: bài được rỗng nguyên tắc và rỗng hình màn mở
CHỈ KHI có `video.giang` thật. Đây là chỗ dễ nới bừa nhất — xoá nhầm phần giảng rồi
nới cổng cho xanh thì bài ấy thành trống trơn mà không ai biết.

---

## 8 · Ba việc phải quyết trước khi bắt đầu đợt lớn

**1 · Sơ đồ đoạn thẳng. → ĐÃ LÀM 14-08.** Cảnh `so_do_doan` — xem §14. Bác dặn
riêng: **vẽ kiểu đoạn thẳng**, nên nó là đoạn thẳng nằm ngang có ngoặc hai đầu, đúng
cách sách giáo khoa vẽ, không phải cột hay ô vuông. Chương 7 dùng lại được ngay.

**2 · Bài cũ có nên giữ chữ giảng không.** Năm bài vừa làm xoá sạch. Nhưng 44 bài cũ
đã có phần giảng viết kỹ, có hình, có bẫy Trí Long. Xoá hết là mất một khối lượng
lớn nội dung đã soạn. Ba lối:
   - xoá hết như B13–B17 (nhất quán nhất, nhưng mất nhiều nhất);
   - giữ chữ giảng làm phần ĐỌC THÊM, gấp lại dưới video;
   - chỉ xoá ở bài mà video thật sự nói đủ.

**3 · Nhân vật Trí Long. → ĐÃ QUYẾT 14-08: BỎ.** Bác chốt bỏ nhân vật, làm đồng bộ
với khuôn đã duyệt. Đã bỏ xong. Chú ý chỗ nhân vật chui ngược vào: `khuon_chung.py`
suy dòng "dấu hiệu" từ **TÊN MỤC** `suKemNham`, nên đổi nội dung mà quên đổi tên mục
là nhân vật hiện lại. Tên mục nay là `CHỖ HAY NHẦM`, và `video_toan.test.mjs` có hai
phép canh (không nhân vật trong bài có video · không nhân vật trong lời đọc).

---

## 10 · Chèn bài mới — LỐI C, không còn dồn số

**Bác chốt 14-08.** Trước đây mã bài mang sẵn con số (`DL:KSN4.B14` = bài 14), nên
chèn một bài vào giữa là phải đổi mã của mọi bài phía sau, rồi **dời tiến độ đã lưu
trong máy từng bé** cho khớp. Đợt đầu đo thật: 353 tệp, 4 566 chỗ đổi mã, 99 tệp đổi
tên. Tách nhỏ cả quyển thì còn **chín đợt như thế nữa** — chín lần đụng vào dữ liệu
thật của trẻ con, mỗi lần sai một nấc là huy hiệu trỏ nhầm bài mà chẳng có gì báo.

Lối C cắt sợi dây: **mã bài từ nay chỉ là CÁI TÊN**, không bao giờ đổi. Số hiển thị
đếm từ **vị trí trong mảng**, và thứ tự mảng khai thẳng ở `data/lop4/thu_tu.json`.

### Thêm một bài — ba bước, hết

```
1. tools/day_so_lop4.py   →  data/lop4/DL_KSN4_B50.json   (mã TRỐNG kế tiếp)
2. data/lop4/thu_tu.json  →  đặt "DL:KSN4.B50" vào ĐÚNG CHỖ trong mảng
3. python3 tools/dung_khuon_chung_lop4.py --khai   (rồi gan_hinh · goi_y — §6)
```

Không đổi tên tệp nào. Không đổi mã bài nào. **Không dời tiến độ của bé.** Bài mới
nằm giữa chương thì mọi bài sau nó tự lùi một số trên màn hình, còn dưới sổ thì mã
vẫn nguyên nên tiến độ vẫn trỏ đúng bài cũ.

### Hai luật phải nhớ

**Mã đã dùng thì không cấp lại.** Xoá một bài thì bỏ mã khỏi `thu_tu.json`, nhưng
đừng đưa mã ấy cho bài khác — bé đã học bài cũ vẫn đang giữ tiến độ mang đúng mã đó,
cấp lại là bé bỗng "đã xong" một bài chưa từng thấy. Luôn lấy mã trống KẾ TIẾP.

**Không thêm đợt dồn nào nữa.** `donSoLop4.js` vẫn phải sống, vì bé chưa mở app từ
trước đợt 1 thì sổ trong máy vẫn mang mã cũ. Nhưng nó **đông cứng ở một đợt**, và
`don_so_lop4.test.mjs` đỏ nếu ai thêm dòng thứ hai. Công cụ `tools/don_so_lop4.py` đã
**bỏ hẳn** — để nó nằm đó là người sau sẽ chạy.

### Cổng canh — `thu_tu_bai.test.mjs`, 16 phép

Lời khai ⟷ tệp nguồn trùng khít · bản dựng giữ đúng thứ tự lời khai · trường `so` cũ
khớp vị trí · không mã trùng · **không cấp lại mã đã xoá** · màn hình đếm chứ không
đọc `so` · **không còn công cụ dồn số**. Bộ dựng cũng tự chặn, in ra thiếu bên nào.

Đã thử ngược cả bảy: phá từng thứ một, cả bảy đều đỏ.

**Bằng chứng đổi mà không hỏng:** dựng lại sau khi sửa, bản cho app ra **byte y hệt**
bản cũ — 49 bài, không một chữ đổi.

---

## 11 · Lịch sử — vì sao có lối C

### Câu hỏi đã trả lời: bác chọn lối C

Tách nhỏ bài thì số bài đổi, nên mã bài đổi, nên **tiến độ đã lưu của các bé phải
dời theo**. Đợt 1 đã dồn một lần: 353 tệp, 4 566 chỗ đổi mã, 99 tệp đổi tên. Nếu mọi
chương đều tách như bác muốn thì **còn 9 đợt dồn nữa** — chín lần dời tiến độ thật.

| lối | làm gì | giá |
|---|---|---|
| A | dồn số sau mỗi đợt | 9 lần dời tiến độ thật của bé |
| B | gom lại, dồn một lần ở cuối | số bài lộn xộn suốt lúc làm |
| **C · cháu khuyên** | **mã bài đứng yên mãi, số hiển thị suy từ vị trí trong mảng** | sửa một lần, hết hẳn chuyện dồn |

**Bác chọn lối C, và đã làm xong — xem §10.**

### Chỗ đang đứng

- Hạ tầng dồn số đã sửa để **chịu được nhiều đợt**: `donSoLop4.js` đổi từ cờ đúng/sai
  sang **đếm số đợt** (`DOT`), vì bé đã chạy đợt 1 mang cờ `true` thì đợt 2 sẽ không
  bao giờ chạy cho bé ấy — *tiến độ đứng yên trong khi bài đã dời*. 11 phép canh, có
  phép **hội tụ**: bé chưa dồn · bé mang cờ cũ · bé lưu số đợt — cả ba phải về cùng
  một chỗ.
- **Không dồn số đợt 2 nữa** — lối C bỏ hẳn việc ấy. **Còn lại: viết 9 bài chương 3.**

### ⚠ Quả mìn đã gỡ — đừng đặt lại

Có lúc `DOT` đã khai **hai** đợt trong khi nội dung mới dồn **một**. Dựng và deploy
lúc ấy là tiến độ mọi bé nhảy **+10** trong khi bài chỉ dời **+5** — mọi huy hiệu
trỏ vượt 5 bài, và **không cổng nào bắt được**, vì cả hai bên đều hợp lệ khi xét
riêng. Đúng dòng họ "lỗi ở chỗ nối". May là chưa deploy.

**Luật:** thêm dòng vào `DOT` **đúng lúc** chạy `don_so_lop4.py --that`, không sớm
hơn một phút nào. Hai chỗ ấy phải đổi cùng một commit; cổng thứ 11 của
`don_so_lop4.test.mjs` so dải bên JS với dải bên Python và đỏ nếu lệch.

### 9 bài của chương 3 — bản đề xuất

Tách theo luật 8, mỗi bài đúng một việc:

| bài | việc duy nhất |
|---|---|
| 1 | **chia hết là gì** — khái niệm gốc, chưa bài nào định nghĩa |
| 2 | dấu hiệu chia hết cho 2 |
| 3 | dấu hiệu chia hết cho 5 |
| 4 | chia hết cho cả 2 và 5 |
| 5 | dấu hiệu chia hết cho 9 |
| 6 | dấu hiệu chia hết cho 3 |
| 7 | phân biệt chia hết cho 3 và cho 9 |
| 8 | **vì sao các dấu hiệu ấy đúng** — luật 10 |
| 9 | bài kết hợp |

---

## 9 · Sau lớp 4

Khuôn này không riêng gì lớp 4. `dung_video_toan.py` đọc `data/lop{N}/`, và ba kiểu
cảnh đều không biết mình đang dựng cho lớp nào. Lớp 2 và lớp 3 — 67 bài, cũng
**100% không định nghĩa khái niệm nào** — dùng lại được nguyên.

Nhưng đừng bắt đầu trước khi lớp 4 xong: mỗi lần đổi khuôn là phải dựng lại toàn bộ
video của những lớp đã làm.

---

## 12 · Đợt 2 đã làm — chương 3 tách 4 bài thành 9

Bốn bài cũ đang gộp đôi ba việc vào một chỗ, và **không bài nào định nghĩa "chia hết
là gì"** — đúng lỗi của cụm dãy số trước khi sửa.

| bài | mã | một việc duy nhất |
|---|---|---|
| 9 | B50 *(mới)* | **chia hết là gì** · số dư · gọi tên bốn thành phần |
| 10 | B09 | dấu hiệu chia hết cho 2 — **và vì sao chỉ nhìn chữ số cuối** |
| 11 | B51 *(mới)* | dấu hiệu chia hết cho 5 — cùng lối chứng minh, cố ý lặp |
| 12 | B52 *(mới)* | chia hết cho cả 2 và 5 — dạy cách nghĩ **phần chung** |
| 13 | B10 | dấu hiệu chia hết cho 9 — **vì sao lại cộng các chữ số** |
| 14 | B53 *(mới)* | dấu hiệu chia hết cho 3 — và quan hệ **một chiều** với 9 |
| 15 | B11 | phép chia có dư — **vì sao số dư luôn nhỏ hơn số chia** |
| 16 | B54 *(mới)* | bài toán thừa - thiếu — khi nào cộng thêm một |
| 17 | B12 | chữ số tận cùng của một tích |

**Một lối nghĩ chạy suốt bốn bài dấu hiệu:** *tách số ra phần chắc chắn chia hết và
phần còn lại, rồi chỉ xét phần còn lại.* Lặp đúng lối ấy bốn lần thì bé nhận ra nó là
một cách nghĩ, không phải bốn mẹo rời rạc. Bài cuối dùng lại nó lần thứ tư cho phép
nhân.

**Số neo `270`** chạy suốt bảy bài đầu — một mình nó thoả cả bốn dấu hiệu (tận cùng 0;
tổng chữ số bằng 9).

### Hai kiểu cảnh mới — luật 9

| cảnh | việc | dùng ở |
|---|---|---|
| `nhom_deu` | xếp N vật thành nhóm k, **phần thừa tô đỏ** | chia hết · số dư · thừa-thiếu |
| `tach_so` | một số tách ra từng chữ số, **tô sáng phần đang xét** | bốn dấu hiệu · tận cùng tích |

`nhom_deu` là cảnh đáng giá nhất chương: nó trả lời "vì sao số dư luôn nhỏ hơn số
chia" trong một giây — phần thừa nhìn thấy được là **không đủ xếp thêm một nhóm**.

### Số đo

9 video · 10,4 phút · 155 clip tiếng mới · 126 câu hỏi · quyển từ **49 lên 54 bài**.

### Ba lỗi ở CHỖ NỐI mà đợt này làm lộ ra

Cả ba đều là **một bên đúng, một bên đúng, chỗ nối sai** — và không bên nào tự biết.

**1 · Video đọc sai số bài.** Kịch bản gõ cứng `'Bài 13'`. Chèn chín bài xong thì B13
đứng thứ mười tám, video vẫn đọc số cũ. Video dựng ra bình thường, không cổng nào kêu
vì chuỗi chữ nào cũng hợp lệ. Nay số ấy **đếm từ `thu_tu.json`**, cùng nguồn với màn
hình, nên hai bên không lệch được nữa.

**2 · `BO` khoá theo SỐ bài.** Chín kịch bản mới mang mã ngoài dải `range(13, 21)`,
nên `--tat-ca` im lặng bỏ qua đúng chín bài vừa viết. Nay khoá theo **mã bài** và danh
sách mặc định **suy từ `BO`**.

**3 · Cổng ghép bài nguồn với bản dựng bằng SỐ bài.** Từ lối C hai bên cố ý khác số,
nên nó ghép trượt toàn bộ và báo thiếu hình màn mở ở những bài vốn có video. Nay ghép
bằng **mã bài**.

### Và một bẫy cũ sập lại

Chạy `day_so_lop4.py` lần hai **xoá sạch hình đã gắn ngay trong bản gốc** —
`gan_hinh_lop4.py` ghi hình vào chính tệp nguồn. `chia_het_lop4.py` nay **giữ lại
`hinh` đã có** trước khi ghi đè. Sáu hình cũ neo vào mở bài và bài giảng của B09–B12
đã gỡ hẳn (cả `lop4_hinh.json`, `lop4_hinh_manifest.json` lẫn tệp ảnh) vì hai mục ấy
nay rỗng — giữ lại là hình không bao giờ hiện.

### Dấu niêm phong bộ chấm

`cham_tienganh.test.mjs` niêm phong lại **2228 → 2273**. Đã soát trước khi sửa: `git
diff` trên `src/mon/toan/lib/` trống trơn; `dungKhiSaiDap` và `tuDoiChieu` vẫn đứng yên
ở 1 và 1 (hai con số này đếm câu chấm **bất thường**, nên đổi cách chấm là chúng động
đậy ngay cả khi tổng khớp); 11 kỳ sát hạch vẫn 124 câu. Lệch đúng bằng 9×9 − 4×9 = 45.

### Đề ôn tập cũng phải theo — bốn sổ, không phải một

Tách bài xong mà quên đề ôn thì **57 tệp cổng vẫn xanh**, chỉ mở bản chạy thật mới
thấy: đề đã là câu mới ("18 quả cam") mà ô nhập vẫn là ô cũ ("xếp hàng 2 vừa khít
không"). Đề một đằng, ô một nẻo — xét riêng thì bên nào cũng hợp lệ.

Một kỳ ôn tập nằm rải ở **bốn sổ**, sửa thiếu một là hỏng câm:

| sổ | giữ gì |
|---|---|
| `data/lop4_ontap.json` | đề bài, đáp án chữ, và `veCau` — **mũi tên gửi bé về bài cần ôn** |
| `data/lop4_ontap_o.json` | ô nhập chấm máy, khoá `OT<ch>#C<n>` và `OT<ch>#B<n>` |
| `data/lop4_hinh.json` + manifest | hình của kỳ |
| `khuon_chung.py` · `TEN_KY` | tên kỳ hiện trên màn (đè tên trong `lop4_ontap.json`) |

**`veCau` là chỗ âm thầm nhất.** Đợt 1 tách cụm dãy số thành năm bài nhưng mười câu
của kỳ ôn 4 vẫn trỏ về ba bài cũ — câu "tính tổng" gửi bé về bài dùng-cả-bốn-công-thức
thay vì bài tổng-dãy-cách-đều. Bé làm sai được đưa nhầm bài để ôn lại, suốt từ đợt 1
tới nay. Đã nắn cả mười.

Ba phép canh mới ở `thu_tu_bai.test.mjs`: mọi bài đều có ít nhất một câu ôn kiểm tới ·
câu ôn chỉ trỏ về bài **cùng chương** · câu ôn nào cũng có ô nhập chấm máy.

---

## 13 · Đợt 3 · chương 5 — trung bình cộng, 3 bài thành 6

Cùng lỗ thủng với hai chương trước: **không bài nào nói trung bình cộng LÀ GÌ**. Bài
đầu vào thẳng "san bằng" rồi quay sang bài toán ngược ngay trong cùng một bài.

| bài | mã | một việc duy nhất |
|---|---|---|
| 26 | B55 *(mới)* | **trung bình cộng là gì** — san bằng, và chỗ công thức sinh ra |
| 27 | B21 | tìm trung bình cộng — **đếm đúng có mấy số** |
| 28 | B56 *(mới)* | biết trung bình cộng tìm tổng — **đọc ngược phép chia** |
| 29 | B57 *(mới)* | tìm số còn thiếu — hai bước, không công thức mới |
| 30 | B22 | hơn kém mức trung bình — **phần nhô lên bằng phần hụt xuống** |
| 31 | B23 | thêm một số vào nhóm — **nhớ đổi cả số lượng** |

**Bộ neo `4 ; 6 ; 8`** chạy suốt sáu bài, chọn để mọi thứ của chương NHÌN THẤY được
trên đúng bộ ba ấy: tổng 18 chia 3 ra chẵn 6; số giữa đúng bằng trung bình nên san
bằng chỉ là cột 8 nhường 2 cho cột 4; và phần nhô lên (2) đúng bằng phần hụt xuống
(2) — đó là trọn bài "hơn kém mức trung bình", khỏi phải chứng minh.

### Kiểu cảnh mới — `san_bang`

Vẽ mấy cột cao thấp, kẻ vạch mức trung bình, và vẽ được cả trạng thái **đã san**.
Nó làm cho "trung bình cộng" thôi là một phép chia khô khốc: bé thấy cột cao nhường
cho cột thấp, cuối cùng ai cũng như ai. Bài "hơn kém mức trung bình" thì chỉ cần kẻ
vạch là xong phần chứng minh.

### Danh sách việc cho MỘT chương — chép ra mà làm

Đợt 2 sót đề ôn tập vì không có danh sách. Nay có:

```
1. tools/<ten>_lop4.py        6 bài · giữ `hinh` cũ trước khi ghi đè
2. data/lop4/thu_tu.json      chèn mã mới vào ĐÚNG CHỖ (tool tự làm)
3. kich_ban_toan.py           kịch bản video, khoá theo MÃ BÀI
4. data/loi_chao.json         lời chào — mỗi bài một câu, tối đa hai câu
5. data/lop4_gan_lop3.json    đường lùi về lớp 3
6. data/lop4_ontap.json       đề ôn 10+10 câu, và `veCau` trỏ ĐÚNG bài
7. data/lop4_ontap_o.json     20 ô nhập, khoá OT<ch>#C<n> và OT<ch>#B<n>
8. lop4_hinh.json + manifest  GỠ hình neo vào mục nay đã rỗng, xoá cả tệp .png
9. --loi → sinh_am → dựng video
10. dung_khuon_chung → gan_hinh → goi_y      ⚠ ĐÚNG THỨ TỰ
11. cổng: SO_BAI · số video · dấu niêm phong MOC
12. npm test → build → NHÌN BẢN CHẠY THẬT → commit → deploy
```

**Bước 12 không bỏ được.** Đợt 2 xanh cả 57 tệp mà đề ôn vẫn hỏng — chỉ mở ra nhìn
mới thấy.

### Số đo

6 video · 5,0 phút · 73 clip tiếng mới · 84 câu hỏi · quyển từ **54 lên 57 bài**.
Niêm phong bộ chấm 2275 → 2303, lệch đúng bằng 54 − 26 = 28 câu luyện tập chấm máy
được của chương (ba bài cũ có 26 vì một câu vốn để bé tự chấm).

---

## 14 · Đợt 4 · chương 6 — tổng - hiệu, 4 bài thành 7

Chương này gói chặt nhất từ trước tới nay: **B24 dạy CẢ HAI công thức** cùng lúc lại
kèm việc vẽ sơ đồ; **B27 gộp bài toán tuổi với bài ba số** — hai dạng chẳng liên quan.
Và vẫn thiếu bài gốc: **không bài nào dạy sơ đồ đoạn thẳng là gì**, nó được dùng ngay
từ bài đầu như thể bé đã biết.

| bài | mã | một việc duy nhất |
|---|---|---|
| 32 | B58 *(mới)* | **sơ đồ đoạn thẳng là gì** — đọc và vẽ, KHÔNG công thức |
| 33 | B24 | số lớn = (tổng + hiệu) : 2 — **thêm hiệu cho hai đoạn bằng nhau** |
| 34 | B59 *(mới)* | số bé = (tổng − hiệu) : 2 — **cắt bớt cho hai đoạn bằng nhau** |
| 35 | B25 | tổng bị giấu — lôi tổng ra trước |
| 36 | B26 | hiệu bị giấu — dịch câu chữ thành con số |
| 37 | B27 | cùng thêm vào cả hai — **hiệu đứng yên** |
| 38 | B60 *(mới)* | ba số — quy về đoạn ngắn nhất, chia BA |

### Vì sao hai công thức phải tách thành hai bài

Đây là quyết định quan trọng nhất của chương. Dạy chung một bài thì bé nhận hai câu
gần giống hệt nhau, khác đúng một dấu, và lẫn ngay. Tách ra thì mỗi bài **suy công
thức từ hình**, và bé thấy chúng không phải hai điều phải nhớ mà là **một cách nghĩ
soi từ hai phía**:

```
thêm HIỆU vào đoạn ngắn  →  hai đoạn bằng nhau  →  2 lần số lớn = tổng + hiệu
cắt HIỆU khỏi đoạn dài   →  hai đoạn bằng nhau  →  2 lần số bé  = tổng − hiệu
```

Câu chốt bé mang theo: **tìm số to thì cộng, tìm số nhỏ thì trừ** — và bé biết vì sao.

### Kiểu cảnh mới — `so_do_doan`

Bác dặn riêng nên nó vẽ **đúng bằng đoạn thẳng**: hai vạch nằm ngang có ngoặc hai đầu,
khúc dôi ra tô vàng, ngoặc bên phải ôm cả hai đoạn ghi tổng. Ba cờ để dựng cảnh chứng
minh: `themVaoBe` (nối thêm nét đứt vàng), `botOLon` (khúc cắt tô đỏ), `chuTong`.

Bộ neo **tổng 70 · hiệu 10** (số lớn 40, số bé 30) chạy suốt bảy bài — cả hai công
thức đều ra số chẵn, và trung bình cộng của chúng là 35 nên bài "tổng bị giấu" nối
được với chương 5 vừa học.

### Số đo

7 video · 88 clip tiếng mới · 98 câu hỏi · quyển từ **57 lên 60 bài**. Gỡ 7 hình cũ
neo vào mở bài và bài giảng — chính video nay đã có sơ đồ, giữ lại là hình chết.

---

## 15 · Đợt 5 · chương 7 — tổng-tỉ và hiệu-tỉ, 4 bài thành 7

Bốn bài cũ gói đôi hết: B29 gộp "tỉ số bị giấu" **với** "tổng bị giấu"; B30 gộp công
thức **với** hiệu ẩn; B31 gộp bài ba số **với** bài nối hai tỉ số. Và vẫn thiếu bài
gốc — **không bài nào nói tỉ số là gì**.

| bài | mã | một việc duy nhất |
|---|---|---|
| 39 | B61 *(mới)* | **tỉ số là gì** — mọi phần đều bằng nhau, KHÔNG công thức |
| 40 | B28 | tổng - tỉ — chia tổng cho **tổng số phần** |
| 41 | B30 | hiệu - tỉ — chia hiệu cho **số phần chênh** |
| 42 | B62 *(mới)* | đề giấu tỉ số — dịch "gấp rưỡi" thành hai con số |
| 43 | B29 | đề giấu tổng hoặc hiệu — dùng lại kỹ năng chương 6 |
| 44 | B31 | ba số theo tỉ |
| 45 | B63 *(mới)* | nối hai tỉ số — quy về cùng một loại phần |

### Bộ neo chọn được rất khéo — hai số 20 và 50

```
tổng 70   ← ĐÚNG tổng của chương 6, bé vừa quen
hiệu 30
tỉ số 2 : 5  →  tổng gồm 7 phần · hiệu gồm 3 phần · mỗi phần 10
```

Nhờ thế **bài tổng-tỉ và bài hiệu-tỉ dùng CHUNG MỘT BỨC TRANH**, chỉ khác chỗ nhìn:
một bên nhìn cả bảy phần, một bên nhìn ba phần chênh. Hai bài đặt liền nhau, đúng cách
chương 6 ghép số lớn với số bé — và bé rút ra một câu duy nhất: *có tổng thì chia tổng
số phần, có hiệu thì chia số phần chênh.*

### Cảnh cũ mở rộng, không dựng cảnh mới

`so_do_doan` của chương 6 thêm hai tham số `phanBe`/`phanLon` — vạch đứng chia đoạn
thành các phần bằng nhau. Không phải dựng cảnh thứ hai, và quan trọng hơn: bé thấy
**cùng một loại hình** với chương trước, chỉ có thêm vạch chia.

### Một miễn trừ được KHAI RA, không bỏ lặng

Bài cuối (nối hai tỉ số) không dùng bộ neo, vì nối tỉ số cần **ba** đại lượng mà bộ
neo là một cặp hai số. `soi()` khai miễn trừ ấy kèm lý do, thay vì lặng lẽ bỏ phép
kiểm — bỏ lặng thì lần sau ai quên bộ neo ở bài khác cũng không ai hay.

### Số đo

7 video · 76 clip tiếng mới · 98 câu hỏi · quyển từ **60 lên 63 bài**. Gỡ 6 hình cũ.
Niêm phong 2332 → 2361 (+27 luyện tập, +2 câu ôn trước chưa có ô nhập).

---

## 16 · Sinh tiếng nay dùng lại clip đã đúng

Suốt bốn đợt, mỗi lần thêm một chương là `sinh_am.py` **sinh lại từ đầu toàn bộ**.
Tới chương 7 thì 500 clip mất **hai mươi phút**, trong đó hơn bốn trăm clip không đổi
một chữ.

Gốc rễ: sổ tra vẫn ghi `van_tay` của từng câu, và chú thích đầu sổ vẫn nói *"sửa chữ
thì vân tay đổi, phải sinh lại clip ấy"* — nhưng **không ai đọc lại nó**. Vòng lặp gọi
`ghi_mp3` cho mọi dòng. Chú thích mô tả một hành vi chưa bao giờ tồn tại.

Đây đúng loại hỏng **không ai kêu**: clip vẫn đúng, video vẫn dựng, chỉ là phí hai
mươi phút mỗi đợt.

**Đo sau khi sửa:** 500 clip, không đổi gì → **0,17 giây**, và không nạp model.

Bỏ qua CHỈ KHI mọi thứ ảnh hưởng tới tiếng đều trùng khít — chữ (qua vân tay), tiếng,
giọng, tốc độ, model — **và** tệp mp3 còn nằm đó thật. Model chỉ nạp khi thật sự phải
sinh, nên lần chạy không có gì mới thì không đụng tới một GB nào.

Đã thử ngược năm ca: bỏ hẳn phép dùng lại · quên xét giọng · quên xét tốc độ · quên
kiểm tệp còn không · bỏ cờ `--lam-lai`. Cả năm đều đỏ. Cổng ở `video_toan.test.mjs`.

**Cửa thoát:** `--lam-lai` sinh lại tất, dùng khi đổi model hay đổi giọng — lúc ấy chữ
không đổi nên vân tay không đổi, mà tiếng thì phải đổi.

---

## 17 · Đợt 6 · chương 8 — bài toán lời văn, NĂM BÀI ĐẦU

Bác muốn xem khuôn trước rồi mới làm nốt, nên đợt này làm 5 trên 10 bài dự kiến.

**Chương này khác hẳn năm chương trước, và phải nói rõ chỗ khác.** Chương 3 tới 7,
sáu bảy bài là các mặt của MỘT ý — nên mỗi chương có một bài khái niệm gốc và một bộ
neo chạy suốt. Chương 8 thì mỗi bài là **một phương pháp riêng**, không có khái niệm
gốc chung, và **không bộ neo nào chở nổi cả chương**. Ép một bộ neo vào đây là gượng.

Nên chương này **neo theo cặp**: hai bài tuổi dùng mẹ 30 con 6 (hiệu 24); hai bài làm
chung dùng anh 6 giờ em 12 giờ (việc chia 12 phần); bài tính ngược đứng riêng.

| bài | mã | một việc duy nhất |
|---|---|---|
| 46 | B32 | tuổi một mốc — **là bài cũ mặc áo mới**, che chữ "tuổi" đi thì thấy |
| 47 | B64 *(mới)* | tuổi hai mốc — **hiệu tuổi không bao giờ đổi** |
| 48 | B33 | làm chung — chia việc thành phần, KHÔNG dùng phân số |
| 49 | B65 *(mới)* | làm chung rồi một người nghỉ — đếm số phần còn lại |
| 50 | B34 | tính ngược — **đi lùi thì đổi phép** |

Bài 46 là bài đáng giá nhất: nó dạy rằng **không có phép nào mới**. Chương này vốn
làm bé sợ vì tưởng mỗi bài một phép thần; nói thẳng ra là bé nhẹ hẳn.

Lớp 4 chưa học phân số nên bài làm chung **không** dùng lối "mỗi giờ làm được một
phần mấy công việc". Lối của lớp 4 là chia việc thành số phần chia hết cho cả hai
thời gian — vừa đúng sức bé, vừa nhìn thấy được trên hình `nhom_deu`.

### Còn lại đợt hai

Giả thiết tạm · khử · thế · sơ đồ Ven · nguyên lý chuồng thỏ. B35 B36 B37 tạm giữ
nguyên bài chữ cũ, nên chương 8 hiện có 8 bài, sau sẽ thành 10.

### Số đo

5 video · **62 clip tiếng mới trong 2 phút 29** (trước khi sửa bộ sinh tiếng thì đợt
này sẽ mất hơn hai mươi phút) · 70 câu hỏi · quyển từ **63 lên 65 bài**.
