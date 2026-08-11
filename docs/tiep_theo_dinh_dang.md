# Điểm dừng — ĐỊNH DẠNG NỘI DUNG (markdown + LaTeX)

Cập nhật 2026-08-11 (lượt ba). Đọc tệp này TRƯỚC khi động vào lời văn hay cách trình bày bài.

> **ĐANG CHẠY trên https://ky-su-nhi.web.app** — deploy 2026-08-11, bản `aa441d6`.
> Cổng: **30 tệp kiểm · 861 PASS · 0 FAIL**. Ba việc tồn của lượt hai ĐÃ XONG.
> Đã đi thật cả trên bản dựng lẫn bản đã lên mạng — và bắt được một lỗi chỉ lộ khi
> mở mắt xem (xem cuối tệp).
>
> ⚠ **Chỉ đẩy `hosting`.** `functions` và `firestore rules` cả phiên không đụng tới nên
> KHÔNG đẩy. Luật Firestore dùng `hasAll` nên trường mới `dangBai` lọt được mà không
> phải sửa rules — nhưng muốn đẩy chúng thì vẫn phải soát trước.

---

## MAI VÀO VIỆC TỪ ĐÂU

**Không còn việc tồn nào chắn đường.** Đã soát lại toàn kho, còn năm hướng —
xếp theo giá trị. Hai việc đầu **chờ bác quyết**, cháu không tự làm.

| # | việc | trạng thái |
|---|---|---|
| 1 | **Bỏ chip mã `K1 · K2 · K3`** ở màn nguyên tắc | ⏸ CHỜ BÁC QUYẾT — sửa là đụng cả bốn quyển đang chạy thật |
| 2 | **Deploy `functions` + `firestore rules`** | ⏸ CHỜ BÁC QUYẾT — cả phiên không đụng tới chúng, muốn đẩy phải soát trước |
| 3 | **Gợi ý cho Mùa giải** — 0/314 câu | quyển đấu chưa có dòng gợi ý nào. Nhưng hỏi trước: đây là quyển THI, bấm đồng hồ và không cho xem đáp — gợi ý có đúng chỗ không, hay chỉ nên có ở màn CHỮA ĐỀ? |
| 4 | **21 dạng bài chỉ có MỘT bậc** | luyện kém là chạm sàn ngay ở lớp 5, không lùi được. Phần lớn là dạng riêng lớp 5 (pha chế, hạt tươi - hạt khô, kim đồng hồ) nên có thể đúng là không có gốc lớp dưới — phải soi từng dạng mới biết |
| 5 | **6 micro đang nằm ở HAI dạng** | tác dụng phụ của `chu_de_tay.json`: luật ở đó chỉ THÊM, không XOÁ. Muốn dứt điểm phải sửa `skills.primary` ở nguồn — mà đổi là `bktUnit` đổi theo, mọi bản ghi nhật ký cũ mồ côi. Cân nhắc kỹ |

Sáu micro ở mục 5, để khỏi phải dò lại:

```
B52.M2  IV.5.2 + IV.5.3      B56.M1  V.4.1 + V.5.1
B53.M3  V.1.1  + V.1.2       B56.M2  V.4.1 + V.5.2
B55.M1  V.3.1  + V.3.2       B56.M3  V.3.2 + V.4.1
```

---

## Dây chuyền — THỨ TỰ LÀ BẮT BUỘC

```
① dựng      python3 tools/dung_khuon_chung.py        (lớp 2 — NẠP data/loi_chao.json)
            python3 tools/dung_khuon_chung_lop3.py
            python3 tools/dung_khuon_chung_lop4.py
② hình lớp2 python3 tools/ve_hinh_lop2.py            → vẽ PNG
            python3 tools/gan_hinh_lop2.py           → gắn vào bài (rồi dựng lại lớp 2)
③ mở bài L5 python3 tools/mo_bai_lop5.py             → nêu đề bài, bỏ đoạn thoại nói hai lần
④ tên bài   python3 tools/ten_bai_lop5.py            → tên ngắn, tên gốc dời sang titleDay
⑤ định dạng python3 tools/dinh_dang.py               → markdown + LaTeX
⑥ bài mẫu   python3 tools/bai_mau.py                 → cắt phần Tóm tắt/Giải/Đáp số
⑦ gợi ý     python3 tools/goi_y.py                   → nạp data/goi_y_tay.json
⑧ chủ đề    python3 tools/dung_chu_de.py             → bản đồ (chép TÊN BÀI, nên chạy SAU ④)
⑨ cổng      cd web && npm test && npm run build
```

⚠ **⑤ và ⑥ sửa thẳng bản DỰNG** (`web/public/content`), mà bộ dựng ① thì ghi đè
trọn tệp từ bản gốc. **Chạy ① sau ⑤⑥ là mất sạch định dạng — dữ liệu vẫn hợp lệ và
KHÔNG CÓ GÌ BÁO.**

③ và ④ KHÔNG dính bẫy ấy: lớp 5 không có bộ dựng khuôn chung, và cả hai đều ghi
**cả bản gốc lẫn bản dựng**.

---

## Lượt ba đã làm gì

### 1 · GỢI Ý RIÊNG CHO TỪNG CÂU — 984/984 câu, VIẾT TAY

Nguồn gốc: **`data/goi_y_tay.json`**. Sửa ở đó rồi chạy `tools/goi_y.py`.

Trước: mọi câu trong một bài dùng chung hai dòng suy từ câu chốt và bước giảng đầu.
Nay mỗi câu một cặp riêng, theo đúng chuẩn gợi ý người soạn đã viết cho lớp 5:

```
tầng 1  GỌI TÊN CẤU TRÚC        "Ba phòng, đọc từ trái sang: trăm — chục — đơn vị."
tầng 2  NƯỚC ĐI ĐẦU, dừng trước kết quả   "Chữ số đứng đầu đang ở phòng nào?"
```

**MÁY KHÔNG SUY ĐƯỢC THỨ NÀY — đã cân nhắc rồi bỏ.** Định cắt tầng 2 từ
`solutionNarrative` của từng câu, nhưng **274/984 câu có lời giải KHÔNG chứa dấu `=`
nào**, vì lời giải của chúng CHÍNH LÀ đáp án (`"814"` · `"362; 509; 740"` ·
`"gấp 10 lần"`). Cắt máy kiểu gì cũng ra đáp án hoặc ra một mẩu vô nghĩa.

Cổng bắt ba chỗ lộ đáp lúc viết (`"11"`, `"có"`, `"không"`) và **sáu chỗ hai câu
cùng bài dùng chung một dòng** — phép kiểm mới `gợi ý tầng 1 riêng theo từng câu`
dựng riêng để canh việc tụt về bậc cũ.

### 2 · NỚI LUẬT ĐỊNH DẠNG CHO CÔNG THỨC CÓ CHỮ CÁI — 114 chỗ

`1/(a × b) = 1/a − 1/b` nay được bọc. **Đếm trước khi nới** đúng như sổ dặn: cả năm
quyển có **991 cụm `X/Y` mang chữ**, mà đứng đầu bảng là

```
Đúng/Sai 230 · km/h 224 · m/s 115 · thêm/bớt 15 · phần/giờ 15
vòng/giờ 15 · m/giây 14 · 1/năm 5 · 2/g 2 (gam) · Sxq/Stp 2
```

Nên luật chỉ nhận **mười chữ cái THƯỜNG, ĐƠN LẺ**: `a b c d k m n p q t` — đúng tập
sách thật sự dùng làm ẩn. Ba chữ bị gạt có chủ ý: `s` và `h` là ĐƠN VỊ (m/s, km/h),
`x` sách dùng làm DẤU NHÂN (`1/(1x2)`), `g` là gam. Chữ HOA cũng gạt (`N/A`,
`TỔNG/HIỆU`, `Sxq/Stp`).

In ra soi bằng mắt cả 114 chỗ trước khi ghi: **0 chỗ bọc nhầm.** Mấy dạng ngờ ngợ
(`(n−1)/n`, `(n+1)/2`, `1/(n(n+1))` nhân ngầm) cố tình bỏ sót — thà bỏ sót còn hơn.

Cổng mới `dinh_dang.test.mjs` canh **chiều ngược**: không cụm lời văn nào bị bọc
thành phân số. Nó cũng canh lệnh LaTeX dán liền chữ sau (`\timesb` → bộ vẽ in
nguyên văn ra màn) — cái bẫy suýt dính khi nới luật.

### 3 · TÊN BÀI LỚP 5 — 109 tên, dài nhất 105 → 60 chữ

Nguồn gốc: **`data/ten_bai_lop5.json`** → `tools/ten_bai_lop5.py`.

Cái dở nặng hơn độ dài là **tên đã đọc trước cách làm** — "Vòng bốn 2·3·7·8: chia
số thừa số cho 4 — đọc dư như máy định vị". Bé chưa mở bài đã biết nước đi, đúng
bệnh của màn mở bài đã chữa một lần.

**Không vứt chữ nào**: tên gốc dời sang `titleDay`, hiện ở ô GỬI BỐ MẸ của màn kết —
bố mẹ đọc sau khi con đã tự làm xong.

Tên nằm **BA nơi** (`data/lessons`, bản dựng, `index_micro.json`); sót một nơi là hai
màn hiện hai tên khác nhau cho cùng một bài. Cổng `ten_bai.test.mjs` canh cả ba, và
canh cả việc chạy lại công cụ chồng tên ngắn lên chính nó làm mất tên gốc.

⚠ Cổng phải **trải phẳng LaTeX trước khi đo**: bản dựng đã qua `dinh_dang.py` nên
tên ở đó là `$\frac{1}{n}$` — đếm chuỗi thô thì một cái tên 47 chữ hoá ra "84 chữ".

### 4 · MÙA GIẢI VÀO MÀN CHỦ ĐỀ — TRỤC RIÊNG, KHÔNG VÀO THANG

14 khối đấu mời được ở 74/82 dạng bài (`dang[].muaGiai` trong `chu_de.json`).

Sổ cũ ghi lý do bỏ ra là "nối qua HAI chặng". Đúng, nhưng lý do **thật sự** phải giữ
nó ngoài `thang` nặng hơn: **`thang[].bai` phải là bài HỌC ĐƯỢC.** Vòng luyện chủ đề
gọi `loadLesson` rồi rút câu từ `practice.pools`; tệp Mùa giải mang tiền tố `DR_`, có
`man`/`cau` chứ không có `practice.pools`, và chạy bằng bộ chơi khác hẳn.

Nhét khối đấu vào thang là vòng luyện nạp về mảng câu RỖNG — **dữ liệu vẫn hợp lệ,
cổng vẫn xanh, mà bé bấm vào thì gặp màn trắng.** Cổng `chu_de.test.mjs` nay canh
đích danh: không mã `DR:` nào được lọt vào thang.

### 5 · BẢNG CÔ GIÁO LỌC THEO DẠNG BÀI

`chu_de.json` mang thêm bảng tra ngược **`baiDang`** (277 bài → mã dạng). Mỗi lượt trả
lời gửi lên máy chủ nay đóng thêm dấu **`dangBai`** bên cạnh `bktUnit`.

Hai trục trả lời hai câu khác nhau: `bktUnit` nói *con mắc ở micro nào*; `dangBai` nói
*cả lớp đang yếu MẢNG kiến thức nào* — nhìn theo bài thì không bao giờ thấy. Nhìn theo
bài, cô thấy "em sai bài 9, bài 23, bài 31"; nhìn theo dạng, cô thấy cả ba đều là
"dấu hiệu chia hết".

Ô lọc chỉ liệt những dạng THẬT SỰ có trong sổ của em ấy, và dòng cũ chưa có dấu vẫn
lọc được (suy từ `microId` qua bản đồ) — không phải chờ con học lại mới có dữ liệu.
Luật Firestore dùng `hasAll` nên trường mới lọt được, **không phải đẩy rules**.

---

## HAI CHỖ SỔ CŨ GHI SAI — đã soát lại và sửa

### (a) "Nhiệt kế lớp 3 vẫn là ảnh" — KHÔNG CÓ NỢ NÀY

`docs/tiep_theo_lop4.md` mục 2 ghi lớp 3 còn `image3.png` dùng 34 lần. Soát:
`image3.png` **không hề còn** trong `web/public/content` lẫn `web/dist`, không tệp
hình nào tên như thế, và không hình nào của lớp 3 gắn vào màn sát hạch. Lớp 3 đã dùng
`NhietKeHieuBai.jsx` như lớp 2·4 ngay từ đợt bóc tách — chính
`docs/phan_loai_hinh_lop3.md` dòng 12 ghi rõ "→ thành phần giao diện, không vẽ".

### (b) "Năm dạng bài chưa quyển nào dạy" — SÁCH CÓ DẠY ĐỦ CẢ NĂM

Sổ cũ kết luận là lỗ hổng chương trình, cần soạn nội dung mới. **Sai.** Đọc mục tiêu
và câu chốt của từng micro thì khớp từng chữ với lời tả dạng bài trong ma trận:

```
IV.5.3 Bể nước                ← B52.M2 "BỂ LÀ CÁI VỎ — NƯỚC MỚI LÀ HIỆN TRẠNG"
V.1.2  Vận tốc trung bình     ← B53.M3 "Vtb = tổng S : tổng T, KHÔNG phải 45"
V.3.2  Đường vòng khép kín    ← B55.M1 "khoảng cách cần gặm là cả MỘT VÒNG"
                              ← B56.M3 "hai kim đồng hồ là bài ĐUỔI KỊP trên đường vòng"
V.5.1  Tàu qua vật đứng yên   ← B56.M1 "qua mốc là ĐIỂM — quãng = đúng THÂN TÀU"
V.5.2  Tàu và vật chuyển động ← B56.M2 "MỐC BIẾT CHẠY — ngược chiều chia TỔNG"
```

**Gốc rễ:** chương 55 và 56 khai `skills.primary` theo số hiệu CHƯƠNG chứ không theo
số hiệu DẠNG — cả sáu micro đánh `CASE:V.3.1#1..3` và `CASE:V.4.1#1..3`, tức lấy dạng
đầu tiên của chương rồi đánh số thứ tự micro phía sau. Cả mảng V lệch một nấc.

**Vì sao không sửa thẳng `skills.primary`:** trường ấy đẻ ra luôn `bktUnit`, mà
`bktUnit` đã nằm trong nhật ký đã gửi lên máy chủ và trong sổ mức thạo. Đổi nó là mọi
bản ghi cũ mồ côi — mất lịch sử học của con để đổi lấy một nhãn phân loại. Vá bằng
`data/chu_de_tay.json` (`themBac`), đúng chỗ tệp ấy dựng ra để xử.

Bản đồ nay **0 dạng thủng**, 321 mối nối bài (trước 315).

---

## LỖI CHỈ LỘ KHI MỞ MẮT XEM — lại một lần nữa

Cổng 861 PASS, build sạch. Đi thật một vòng thì: **bấm khối đấu từ màn chủ đề là bé
bị ném về kệ sách**, không một tiếng báo.

Vì trong `App.jsx`, nhánh `if (!chuongTrinh) return <KeSach/>` nằm **CHẮN GIỮA** màn
chủ đề và màn đấu. Vào từ chủ đề thì không có quyển nào đang mở, nên kệ sách nuốt mất
`view.page === 'dau'` trước khi tới nơi.

**Đúng cái bẫy đã dính một lần rồi** — vụ mở bài lớp 3 từ màn chủ đề (khối `baiDocCham`
nằm sau `!chuongTrinh`). Cùng một hình dạng, cùng một triệu chứng. Nay nhánh `dau` đã
dời lên TRƯỚC kệ sách, kèm lời ghi tại chỗ.

**Bài học giữ lại: mọi màn vào được từ MÀN CHỦ ĐỀ đều phải đứng trước `!chuongTrinh`.**
Màn chủ đề không thuộc quyển nào — đó là cả điểm mạnh lẫn cái bẫy của nó.

Đã đi thật, gồm cả một lượt cố tình làm sai:
1. kệ sách → chủ đề → mảng V → dạng 5.1 (từng là "chưa có bài", nay có bậc lớp 5);
2. bấm "đấu thử ở Mùa giải" → mở đúng vòng đấu V14, luật 15 câu · 12 bẫy;
3. bấm Thoát → về **đúng** màn chủ đề 5.1, không rơi vào kệ Mùa giải;
4. lớp 2 bài 1 → luyện tập → sai lần 1 hiện gợi ý tầng 1, sai lần 2 hiện thêm tầng 2;
5. sang câu kế → gợi ý **khác hẳn** ("Mở từng cửa phòng rồi cộng lại");
6. lớp 3 bài 9 màn giảng → `1/k` vẽ thành phân số xếp dọc, không lộ mã LaTeX.

---

## Hai việc CHỜ BÁC QUYẾT

| # | việc | vì sao phải hỏi |
|---|---|---|
| 1 | Bỏ chip mã `K1 · K2 · K3` ở màn nguyên tắc | sửa là đụng cả bốn quyển đang chạy thật |
| 2 | Deploy `functions` và `firestore rules` | mấy phiên nay không đụng tới chúng nên chưa đẩy; muốn đẩy phải soát trước |

Hosting đã đẩy: `cd web && npx firebase deploy --only hosting` (1469 tệp, 230 tệp mới).

---

Xem thêm `docs/tiep_theo_chu_de.md` (học theo chủ đề), `docs/tiep_theo_lop4.md`
(đường lùi từng bài) và `docs/CHUAN_DUA_SACH_VAO_APP.md` (44 cái bẫy).
