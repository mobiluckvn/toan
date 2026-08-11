# Điểm dừng — ĐÁP ÁN QUYỂN 2: 314/314 CÂU MÁY CHẤM ĐƯỢC

Cập nhật 2026-08-11 (lượt năm). Đọc tệp này TRƯỚC khi động vào đáp án Quyển 2 hay bộ
chấm `flow.js`.

> Cổng: **33 tệp kiểm · 1019 PASS · 0 FAIL**. Máy chấm **102 → 314/314 câu**.
> Đã đi thật một vòng đấu trên bản dựng: nhập số, bấm trắc nghiệm, câu ba ô, nộp bài,
> chữa đề, phiên tòa, nhật ký. 0 lỗi trong bảng điều khiển.

---

## VÌ SAO 212 CÂU BỊ BỎ LẠI

`tools/chuan_quyen2.py` rút đáp số bằng luật, và **cố ý rút rất dè** — lời chữa của
sách là văn xuôi, chứa cả số trung gian của phép tính ("10 × a − a = 9 × a = 27,9 →
a = 3,1"), nên đoán bừa "con số cuối cùng" là sẽ có câu con làm đúng mà máy báo sai.
Ở Quyển 1 đã dính đúng lỗi ấy 90 câu.

Sự dè dặt ấy đúng, nhưng cái giá lộ ra khi cần đo: **quyển luyện thi — quyển duy nhất
có đồng hồ và có barem — lại là quyển sổ phụ huynh và bảng cô giáo không đo được gì.**

## CÁCH LÀM: NGƯỜI KHAI, MÁY KIỂM

Đúng nếp Quyển 1 (`data/lop*_dapan_tay.json`): đọc tay từng lời chữa rồi khai đáp án
vào **`data/quyen2_dapan_tay.json`** (212 khoá, dạng `V01#C9`).

```
ĐÁP SỐ LÀ SỐ   → answerKey.value          242 câu · điền số
nhiều đáp số   → answerKey.parts           99 câu · mỗi ô một nhãn
dãy số         → answerKey.values           2 câu
ĐÁP SỐ LÀ CHỮ  → format mcq + choices      10 câu · con BẤM, không gõ
                 (và 41 ô bấm chọn nằm trong `parts`)
```

**Vì sao chữ thì chuyển trắc nghiệm:** bắt con gõ đúng từng chữ "KHÔNG chắc đúng" là
kiểm kỹ năng gõ chứ không kiểm toán. **Mồi nhử lấy từ chính sách** — mỗi lời chữa đều
có câu "Mất điểm nếu…", đó đúng là cái bẫy Cáo Đề gài; mồi bịa ra thì hoặc quá lộ,
hoặc vô tình cũng đúng.

Hai công cụ:
* `tools/dapan_quyen2.py` — **VÁ** `answerKey` vào cả `data/quyen2/` lẫn
  `web/public/content/quyen2/`. Vá chứ không dựng lại: bản dựng đã qua `dinh_dang.py`
  (markdown + LaTeX), chạy lại `chuan_quyen2.py` là mất sạch định dạng mà không báo gì.
* `tools/chuan_quyen2.py` — nay **đọc sổ tay trước luật máy**, để một ngày dựng lại
  từ bản thô vẫn ra 314/314.

---

## CỔNG `quyen2_dapan.test.mjs` — ĐO BỐN VIỆC, KHÔNG PHẢI MỘT

Viết tay 212 đáp án thì sai kiểu khác: gõ nhầm một chữ số, hay khai một con số sách
không hề nói tới. Sai kiểu ấy **tệ hơn cả tự chấm**. Nên cổng không đo "có đáp án
chưa", nó đo:

1. **máy chấm được** — không câu nào rơi về tự luận;
2. **chấm đúng** — nạp ngược chính đáp án vào bộ chấm, phải ra ĐÚNG;
3. **không chấm bừa** — nạp ô rỗng và chuỗi vô nghĩa, phải ra SAI;
4. **đáp án có trong sách** — mọi con số của đáp án phải có mặt trong lời chữa. Đây
   là chốt chặn duy nhất bắt được lỗi gõ nhầm và lỗi bịa, vì máy không tự giải bài
   để đối chiếu được.

Cộng thêm: mồi nhử đủ và khác nhau, đáp án nằm trong bộ nút, nhãn không cho không đáp
số, và **bản gốc khớp bản dựng**.

---

## BỐN LỖI CÂM CỔNG MỚI BẮT ĐƯỢC

### 1 · Chữ mờ trong ô nhập CHÍNH LÀ đáp án — `flow.js`

Ví dụ trong chữ mờ vốn cố định: `vd 3/4` · `vd 3 : 4` · `điền dạng: 2 giờ 24 phút`.
Bài nào có đáp số đúng bằng ví dụ ấy là con đọc được đáp án ngay trong ô còn trống.
Quyển 2 dính **ba câu**. Nay mỗi dạng có thêm một lời nhắc TRỐNG, dùng khi trùng.

### 2 · `"1 050"` bị đọc thành DÃY HAI SỐ — `flow.js`

`isNumberList` đếm số mà không bỏ dấu phân nghìn kiểu Việt, nên "1 050" ra hai số
(1 và 50) và đáp án bị coi là một dãy — câu "tính tổng… = 1 050" **nhận luôn cả
"50 và 1"**. Ảnh hưởng cả bốn quyển, không riêng Quyển 2.

### 3 · VÒNG ĐẤU 1 KHOÁ CỨNG dù đã học xong chương 1 — `dau.js`

`chuongDaXong` quét cả sổ `progress.micros` — mà đó là sổ CHUNG của bốn quyển.
`chapterOf` là hàm chia chương của Quyển 1, nên mã bài lớp 2·3·4 dồn hết về chương 1:
chỉ cần con học dở một bài lớp 3 là chương 1 của Quyển 1 bị coi là chưa xong. Và dòng
báo thì không kèm "còn N bài nữa", nên nhìn như app hỏng. `conThieu` trong `MuaGiai`
mắc đúng bẫy ấy.

### 4 · Lời chữa in ra nguyên văn `$4,5 \times 100 = 450$` — `DauPlayer.jsx`

`{q.loiChua}` không bọc `<Chu>`. Có sẵn từ đợt định dạng, nhưng nay 314/314 câu đều
máy chấm nên bé nào cũng đọc tới nó. Cùng lỗi ở `moTa` (luật vòng đấu), `thanChu` và
`ten` (phiên tòa · Mùa giải · trại huấn luyện). Cổng `chu_vao_man.test.mjs` nay canh
thêm ba trường ấy.

---

## MAI VÀO VIỆC TỪ ĐÂU

1. **Gợi ý cho Mùa giải — 0/314 câu.** Nay đã có đáp án cho mọi câu nên viết gợi ý
   đúng chuẩn hai tầng của Quyển 1 là làm được. Vẫn phải hỏi bác trước: quyển này
   bấm đồng hồ, gợi ý có đúng chỗ không hay chỉ nên ở màn CHỮA ĐỀ?
2. **Lời chữa của `V08#C13` tự cãi mình** — sách viết "…170 : 70 = 17/7 — chưa tròn,
   nên kiểm lại: Cẩn thận: A đầu = 120 + 30 = 150…". Đáp án cuối (3 lần) là đúng,
   nhưng bé đọc đoạn ấy sẽ rối. Đáng biên tập lại lời chữa.
3. Ba hướng cũ trong `docs/tiep_theo_dinh_dang.md` vẫn còn: 21 dạng chỉ một bậc,
   6 micro nằm ở hai dạng, chip mã `K1·K2·K3`.

---

Xem thêm `docs/tiep_theo_man_nha.md` (màn nhà · học bạ · sổ bố mẹ · bảng cô giáo) và
`docs/tiep_theo_dinh_dang.md`.
