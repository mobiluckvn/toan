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
| 2 | 3 · Dấu hiệu chia hết | B09–B12 | B17 đã dùng phép chia hết, bé vừa gặp |
| 3 | 5 · Trung bình cộng | B21–B23 | ba bài, một công thức, dễ ra khuôn |
| 4 | 6 · Tổng - hiệu | B24–B27 | có sơ đồ đoạn thẳng — cần thêm một kiểu cảnh mới |
| 5 | 7 · Tổng - tỉ, Hiệu - tỉ | B28–B31 | dùng lại kiểu cảnh của đợt 4 |
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

**1 · Sơ đồ đoạn thẳng.** Chương 6 và 7 (8 bài) dạy bằng sơ đồ đoạn thẳng — kiểu
cảnh chưa có. Phải dựng trước, và nên dựng chung với `figforge` để màn hình và video
cùng một nguồn, đúng bài học của `hinh_ve.json`.

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

## 10 · ⚠ VIỆC CÒN TREO — ĐỌC TRƯỚC KHI LÀM ĐỢT 2

### Câu hỏi bác chưa trả lời: dồn số kiểu nào

Tách nhỏ bài thì số bài đổi, nên mã bài đổi, nên **tiến độ đã lưu của các bé phải
dời theo**. Đợt 1 đã dồn một lần: 353 tệp, 4 566 chỗ đổi mã, 99 tệp đổi tên. Nếu mọi
chương đều tách như bác muốn thì **còn 9 đợt dồn nữa** — chín lần dời tiến độ thật.

| lối | làm gì | giá |
|---|---|---|
| A | dồn số sau mỗi đợt | 9 lần dời tiến độ thật của bé |
| B | gom lại, dồn một lần ở cuối | số bài lộn xộn suốt lúc làm |
| **C · cháu khuyên** | **mã bài đứng yên mãi, số hiển thị suy từ vị trí trong mảng** | sửa một lần, hết hẳn chuyện dồn |

Lối C là chữa tận gốc: mã (`DL:KSN4.B14`) chỉ còn là cái tên, còn "Bài 19" là thứ
màn hình tự đếm ra. Không còn đợt dồn nào nữa. **Chưa làm gì cả — chờ bác chọn.**

### Chỗ đang đứng

- Hạ tầng dồn số đã sửa để **chịu được nhiều đợt**: `donSoLop4.js` đổi từ cờ đúng/sai
  sang **đếm số đợt** (`DOT`), vì bé đã chạy đợt 1 mang cờ `true` thì đợt 2 sẽ không
  bao giờ chạy cho bé ấy — *tiến độ đứng yên trong khi bài đã dời*. 11 phép canh, có
  phép **hội tụ**: bé chưa dồn · bé mang cờ cũ · bé lưu số đợt — cả ba phải về cùng
  một chỗ.
- **CHƯA dồn số đợt 2. CHƯA viết 9 bài chương 3.**

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
