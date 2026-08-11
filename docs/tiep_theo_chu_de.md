# Điểm dừng — HỌC THEO CHỦ ĐỀ

Cập nhật 2026-08-10. Đọc tệp này TRƯỚC khi động vào bản đồ chủ đề.

Nguồn ma trận: `docs/Ma_tran_kien_thuc_Toan5_HSG_Cap4.xlsx` — **đối chiếu ra thì nó
chính là `data/km_v1_38.json` đã có sẵn trong kho.**

> **XONG TRỌN.** Bản đồ chủ đề · màn xem theo chủ đề · vòng luyện tự lùi tự tiến ·
> Mùa giải · bảng cô giáo lọc theo dạng. Cổng: **30 tệp kiểm · 861 PASS · 0 FAIL**.
> Chưa deploy. Ba việc tồn của đợt đầu ĐÃ XONG (11-08-2026) — xem cuối tệp.

---

## MAI VÀO VIỆC TỪ ĐÂU

**Không còn việc tồn nào chắn đường** — ba hướng của đợt đầu đã làm xong cả ba
(11-08-2026). Đọc `docs/tiep_theo_dinh_dang.md` để biết hiện đang đứng ở đâu.

---

## Dây chuyền — chạy đúng thứ tự

| bước | lệnh | ra cái gì |
|---|---|---|
| 0 | `python3 tools/ten_bai_lop5.py` | tên bài lớp 5 — chạy TRƯỚC, vì bản đồ chép tên bài |
| 1 | `python3 tools/ma_tran.py` | bảng đối chiếu Excel ↔ bản đồ. Chỉ ĐỌC, không ghi |
| 2 | `python3 tools/dung_chu_de.py` | `data/chu_de.json` **và** `web/public/content/chu_de.json` |
| 3 | `node web/test/chu_de.test.mjs` | cổng riêng cho bản đồ (16 phép kiểm) |
| 4 | `cd web && npm test && npm run build` | cổng chung + bản dựng |

`tools/dung_chu_de.py --soat` chỉ in, không ghi. `--in` in TỪNG dạng bài kèm thang,
dùng để soi bằng mắt (82 dòng, đọc một lượt hết chừng năm phút).

Sửa tay thì sửa `data/chu_de_tay.json`, **không sửa `chu_de.json`** — tệp ấy dựng lại
là mất. Đợt đầu không có dòng sửa tay nào; đợt hai có **5 dòng**, xem cuối tệp.

---

## Ma trận bác gửi ĐÃ CÓ SẴN trong kho

| | Excel | km_v1_38.json | khớp |
|---|---|---|---|
| Trường hợp (cấp 4) | 264 | 264 `Case` | **264/264 trùng tên** |
| Mức độ CB/NC | 83 / 181 | 83 / 181 | **264/264 trùng** |
| Chủ đề (cấp 2) | 34 | 34 `Topic` | 34/34 ghép theo số hiệu |
| Dạng bài (cấp 3) | 82 | 82 `ProblemType` | 82/82 ghép theo số hiệu |
| Mảng (cấp 1) | 5 | 5 `KnowledgeArea` | 5/5 |

Ghép theo **SỐ HIỆU** (`1.1.`, `2.3.`) chứ không theo tên: hai bản viết tên khác nhau
ở 17 dạng và 6 chủ đề, ghép theo tên thì hụt 17/82. Excel viết đủ hơn nên **tên hiện
lên màn lấy từ Excel**, còn cấu trúc thì lấy từ bản đồ.

---

## Bản đồ ra: `web/public/content/chu_de.json` (105 KB)

```
5 mảng · 34 chủ đề · 82 dạng bài · 315 mối nối bài
  4 bậc: 21 dạng · 3 bậc: 16 · 2 bậc: 24 · 1 bậc: 16 · 0 bậc: 5
  → 61/82 dạng LÙI ĐƯỢC sang lớp dưới
bậc theo lớp: lớp 2: 33 · lớp 3: 30 · lớp 4: 64 · lớp 5: 69
```

Ba bảng phẳng `mang` → `chuDe` → `dang`; mỗi dạng có `ten` (từ Excel), `moTaLop`
(lời giới thiệu riêng cho từng lớp), `soTruongHop` (CB/NC), và `thang` xếp từ lớp
THẤP lên CAO.

---

## HAI LUẬT ĐÃ THỬ VÀ PHẢI BỎ

Ghi lại để đừng ai dựng lại — cả hai nghe đều rất xuôi tai.

### (a) Lấy `duongLui` của sách làm bậc thang

`duongLui` có `canCu:'sach'` là mối nối **chính sách chỉ đích danh** ("HẠT MẦM NĂM
NGOÁI: Lớp 3, Bài 16"), nên thoạt nghe đáng tin hơn ghép máy. Thử thì trong 78 bậc
nó thêm vào có **30 bậc rơi vào bài dạy chủ đề KHÁC**:

> "3.1. Lập số lớn nhất / nhỏ nhất" ← `DL:KSN3.B06`, mà bài ấy dạy **phép chia có dư**

Vì hai thứ trả lời hai câu hỏi khác nhau:

- `duongLui` nói **"bài này dựng trên bài kia"** — quan hệ BÀI NỀN
- thang chủ đề cần **"bài này dạy chủ đề ấy"** — quan hệ THÀNH VIÊN

Bài nền hoàn toàn có thể thuộc chủ đề khác, và thường là thế, vì học chủ đề mới bao
giờ cũng phải mượn kỹ năng của chủ đề cũ. **Hai lối lùi, hai việc khác nhau, không
cái nào thay được cái nào** — `duongLui` vẫn giữ nguyên chỗ cũ ở màn kết mỗi bài.

Nay bậc nào được sách xác nhận là bài nền thì gắn cờ `sachXacNhan` (28 bậc) để ghi
công, nhưng cờ ấy KHÔNG quyết định bậc có mặt hay không.

### (b) Lớp 5 lấy khai ở mức BÀI khi không micro nào khai

Bản đồ khai `LESSON:KSN5Q1.B11` dạy cả `PT:I.5.2` (dãy số) lẫn `PT:I.6.4` (chữ số
tận cùng), trong khi **cả ba micro của nó đều khai 6.4**. Lấy theo bài thì bé trượt
"dãy số không cách đều" bị đẩy sang ba bài chữ số tận cùng. Có **19 cặp (bài, dạng)**
như thế.

Nay lớp 5 **chỉ căn cứ `skills.primary` của từng MICRO** — micro mới là thứ bé thật
sự mở ra học. Vá hẹp cho 9 micro khai số hiệu không có trong ma trận (bài 19·20·24):
những micro ấy — và chỉ những micro ấy — mới lùi về lấy khai ở mức bài. Ba chỗ đó đã
đọc lại nhan đề micro để xác nhận.

---

## Kiểm chéo bằng ý kiến thứ hai

`dangGoc` là trường do NGƯỜI SOẠN ghi tay từng bài lớp 2·3·4 lúc bóc tách sách
("SỐ 1.1 — Phân tích cấu tạo số"). Nó độc lập hẳn với `adj.teaches` của bản đồ:

```
111 bài lớp 2-3-4 · cùng chỉ ≥1 dạng: 105 · LỆCH HẲN: 2 · chỉ bản đồ có: 4
```

Hai chỗ lệch là do `dangGoc` viện dẫn số hiệu **8.5 / 8.6** mà ma trận không có
(III.8 chỉ tới 8.4). Tức bản đồ đáng tin — và mấy thang trông "sai" khi đọc nhan đề
thì hoá ra đúng: `DL:KSN4.B09` tên là "DẤU HIỆU CHIA HẾT CHO 2 VÀ 5" nhưng `dangGoc`
ghi rõ nó dạy **cả** "6.1 dấu hiệu chia hết" **lẫn** "3.1 lập số chẵn - lẻ từ thẻ".

---

## Vòng luyện: máy trạng thái lùi / tiến

Ở `web/src/lib/progress.js`, viết thành hàm THUẦN (không nhét trong component) để
phép kiểm chạy được mọi ngả:

```
nguongDat(tong)                  đạt là 2/3 số câu — 6 câu thì cần 4
bacBatDau(thang, lopCon)         bậc cao nhất không vượt lớp con
buocSau(thang, lop, dat, tong)   → {hanh:'len'|'xuong'|'xong'|'san', lop?}
ghiLuyenChuDe(p, dang, lop, kq)  ghi sổ, giữ `best` của lần cao nhất
bacDaVung(p, dang)               bậc cao nhất đã đạt
```

**KÉM THÌ MỞ BÀI HỌC, KHÔNG PHẢI CHO LÀM THÊM BÀI TẬP.** Con sai ở bậc trên nghĩa là
hổng gốc; đưa thêm một xấp bài tập cùng kiểu ở lớp dưới chỉ để con sai thêm một lượt
nữa — thứ con thiếu là phần GIẢNG. Nên lùi một bậc là mở `LessonPlayer`, học xong thì
`veLai` đưa con về đúng vòng luyện của bậc ấy.

**CHẤM MỘT LẦN** (`chotMotLan`, dùng lại của kỳ sát hạch): vòng này quyết định lùi
hay tiến, mà sai rồi sửa lại được thì con số đo ra chẳng còn nghĩa gì.

Câu hỏi **không dựng thêm dữ liệu mới** — nạp bài của bậc bằng `loadLesson` rồi lọc
câu có `answerKey` trong `practice.pools`. Cả bốn quyển đã cùng một khuôn nên chỗ này
không phải phân nhánh theo lớp.

---

## Đường về (`veLai`)

`setView` vốn thay thẳng, mất chỗ cũ. Nay `view.veLai` nhớ đường về và mang theo cả
VỊ TRÍ đang đứng, nên:

- học xong bài mở từ màn chủ đề → về đúng cái thang vừa đứng, không phải bấm lại ba tầng;
- `finishMicro` tôn trọng `veLai` TRƯỚC khi tính bài kế trong quyển — nếu không, con
  vào bài từ mạch chủ đề mà học xong bị đẩy sang bài kế của quyển, đứt mạch;
- chuỗi lùi bao nhiêu nấc thì `veLai` vẫn được chuyền tiếp.

Màn chủ đề tự suy MẢNG từ mã dạng bài (`bd.dang[maDang].mang`), nên nơi gọi chỉ cần
nhớ mã dạng — một thứ, không phải hai.

**Gộp hai khối phòng học làm một.** Trước có hai khối `LessonPlayer` gần trùng nhau;
khối `baiDocCham` nằm trong nhánh `nhipDocCham(chuongTrinh)` đứng SAU `!chuongTrinh`,
nên mở bài lớp 3 từ màn chủ đề — nơi không có quyển nào đang mở — là rơi về kệ sách.

---

## Đã đi thật trên bản dựng (không chỉ chạy cổng)

Trọn vòng, gồm **một lượt cố tình làm sai**:

1. kệ sách → Học theo chủ đề → mảng I → thang 1.1 (đủ bốn bậc);
2. luyện bậc lớp 5, **sai cả 6 câu** → hiện đúng "lùi về bài lớp 4 cùng chủ đề";
3. mở bài lớp 4 → Thoát → vào thẳng **vòng luyện bậc lớp 4** (không rơi về kệ sách);
4. luyện đạt 5/6 → hiện "Lên bậc lớp 5" → bấm là sang bậc lớp 5;
5. mở lại app → sổ nhớ "Con đã vững tới bậc lớp 4";
6. luyện bậc **lớp 2** rồi sai hết → dừng tử tế: "chưa có bậc nào thấp hơn", mời bố
   mẹ cùng xem lại — **không lùi vào hư không**;
7. lối cũ theo quyển không đổi: mở bài từ trang chính lớp 3 rồi Thoát vẫn về đó.

---

## Việc còn lại

### 1 · ~~Năm dạng bài chưa quyển nào dạy~~ — SÁCH CÓ DẠY ĐỦ CẢ NĂM

**Kết luận cũ SAI, đã sửa 11-08-2026.** Đợt đầu ghi đây là lỗ hổng chương trình, cần
soạn nội dung mới. Đọc mục tiêu và câu chốt của từng micro thì nội dung khớp từng chữ
với lời tả dạng bài trong ma trận:

```
IV.5.3 Bể nước                ← B52.M2 "BỂ LÀ CÁI VỎ — NƯỚC MỚI LÀ HIỆN TRẠNG"
V.1.2  Vận tốc trung bình     ← B53.M3 "Vtb = tổng S : tổng T, KHÔNG phải 45"
V.3.2  Đường vòng khép kín    ← B55.M1 · B56.M3 (hai kim đồng hồ)
V.5.1  Tàu qua vật đứng yên   ← B56.M1 "qua mốc là ĐIỂM — quãng = đúng THÂN TÀU"
V.5.2  Tàu và vật chuyển động ← B56.M2 "MỐC BIẾT CHẠY — ngược chiều chia TỔNG"
```

**Gốc rễ:** chương 55 và 56 khai `skills.primary` theo số hiệu CHƯƠNG chứ không theo
số hiệu DẠNG — cả sáu micro đánh `CASE:V.3.1#1..3` và `CASE:V.4.1#1..3`, tức lấy dạng
đầu tiên của chương rồi đánh số thứ tự micro phía sau. Cả mảng V lệch một nấc.

Vá bằng `data/chu_de_tay.json` chứ không sửa `skills.primary`, vì trường ấy đẻ ra luôn
`bktUnit` — thứ đã nằm trong nhật ký đã gửi lên máy chủ. Lý do đầy đủ ghi trong chính
tệp ấy. Bản đồ nay **0 dạng thủng · 321 mối nối bài**.

**Bài học giữ lại: "ma trận có mà sách không có" gần như luôn là SAI KHAI, không phải
thủng chương trình. Đọc mục tiêu micro trước khi kết luận.**

### 2 · Mười sáu dạng chỉ có MỘT bậc

Phần lớn là dạng riêng lớp 5 (pha chế dung dịch, hạt tươi - hạt khô, kim đồng hồ).
Vẫn hiện trong danh sách, nhưng luyện kém thì chạm sàn ngay ở lớp 5.

### 3 · ~~Mùa giải chưa vào thang~~ — XONG, mà đi TRỤC RIÊNG

14 khối đấu mời được ở 74/82 dạng, qua `dang[].muaGiai` — **không** phải một bậc của
`thang`. Lý do nặng hơn chuyện "hai chặng": `thang[].bai` phải là bài HỌC ĐƯỢC, vì
vòng luyện gọi `loadLesson` rồi rút câu từ `practice.pools`; tệp Mùa giải là `DR_`,
có `man`/`cau` và chạy bằng `DauPlayer.jsx`. Nhét vào thang là vòng luyện nạp về mảng
câu RỖNG — cổng vẫn xanh mà bé bấm vào thì gặp màn trắng. Cổng nay canh đích danh.

⚠ Và đã dính thật một lỗi anh em của nó: nhánh `!chuongTrinh` trong `App.jsx` chắn
giữa màn chủ đề và màn đấu, nên bấm khối đấu từ chủ đề là rơi về kệ sách. **Mọi màn
vào được từ màn chủ đề đều phải đứng TRƯỚC `!chuongTrinh`.**

---

Xem thêm `docs/tiep_theo_lop4.md` (đường lùi từng bài ở màn kết) và
`docs/CHUAN_DUA_SACH_VAO_APP.md` (44 cái bẫy khi bóc tách sách).
