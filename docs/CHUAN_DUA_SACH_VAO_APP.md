# Chuẩn đưa một quyển sách vào phần mềm

Viết sau khi làm xong **Toán lớp 2** (33 bài · 70 hình · 8 ôn tập · 3 ải) và
**Quyển 2 lớp 5** (21 khối · 53 sơ đồ). Mọi luật ở đây đều đổi bằng một lần vấp
thật — phần *"Mười tám cái bẫy"* là chỗ đáng đọc nhất, đọc trước khi gõ dòng nào.

> **Nguyên tắc bao trùm:** thà thiếu còn hơn sai. Một câu chấm sai làm bé mất tin
> vào cả phần mềm; một hình vẽ sai dạy bé điều ngược lại. Không chắc thì để tự chấm,
> để trống, và **nói ra** — đừng đoán.

---

## 1 · Ba tầng dữ liệu — đừng trộn

| Tầng | Ở đâu | Vai | Ai sửa |
|---|---|---|---|
| **THÔ** | `data/<quyen>_tho.json` | đúng nguyên văn sách, mốc bất biến để đối chiếu | máy ghi, người KHÔNG sửa |
| **GỐC** | `data/<quyen>/*.json` | giữ cấu trúc mục của sách, lời văn đã viết lại | máy ghi, người đọc để đối chiếu sách giấy |
| **KHUÔN CHUNG** | `web/public/content/<thuMuc>/*.json` | app đọc bản này | **máy ghi — sửa tay là mất** |

Ba tầng **cố ý khác nhau**. Đây là chỗ dễ nhầm nhất với người quen nếp cũ
(lớp 5 Quyển 1 thì `data/lessons` và `public/content/lessons` phải giống hệt nhau).

Sửa nội dung thì sửa ở **bản mô tả** (`data/<quyen>_hinh.json`,
`data/<quyen>_dapan_tay.json`, bảng `VIET_LAI`) rồi chạy lại dây chuyền.

---

## 2 · Khuôn chung — mọi quyển đều về hình dạng này

Một bài học là một tệp JSON. App có **một bộ mã duy nhất** đọc khuôn này cho mọi
lớp, mọi môn.

```jsonc
{
  "id": "DL:KSN2.B01",          // duy nhất toàn hệ thống; TIỀN TỐ quyết định quyển
  "grade": 2, "quyen": "lop2",
  "title": "Bài 1 · NGÔI NHÀ TRĂM - CHỤC - ĐƠN VỊ",
  "so": 1, "chuong": 1, "tenChuong": "Vương quốc Số",
  "durationMinutes": 10,

  "skills":  { "bktUnit": "CHUONG:1@G2" },     // đơn vị theo dõi cho cô giáo
  "series":  { "order": 1, "prev": null, "next": "DL:KSN2.B02" },

  "objective": {
    "kidText": "…",      // CON đọc — ngắn, lời thường
    "text":    "…",      // bản đầy đủ cho bố mẹ
    "passRule": "đúng ≥ 4/5 câu tự kiểm"
  },

  "knowledgeCore": {
    "statements":     [{ "id": "K1", "text": "…" }],   // nguyên tắc, mỗi cái một ý
    "mantra":         "câu chốt của bài",
    "misconceptions": [{ "wrong": "…", "signal": "…", "fix": "…" }]
  },

  "lecture": {
    "screens": [
      { "id": "S1", "kind": "hook",    "narration": "…" },
      { "id": "S2", "kind": "explain", "narration": "", "teaches": ["K1"] },
      { "id": "S9", "kind": "trap",    "narration": "…" }
    ]
  },

  "workedExample": { "title": "Bài mẫu", "problem": "…", "steps": [{ "show": "…" }] },

  "practice":   { "pools": { "warmup": [], "standard": [], "challenge": [] } },
  "assessment": { "passRule": "≥ 4/5", "items": [] },

  "parentNote": { "onComplete": "…", "homeActivity": "…", "watchFor": "…" },

  "figureSpec": [{
    "id": "L2H_CTS01", "usedIn": ["screen:S2"], "file": "figures/L2H_CTS01.png",
    "caption": "…", "sha256_16": "22baa5536b2ec0f0"
  }]
}
```

### Một câu hỏi

```jsonc
{
  "id": "C1", "text": "đề bài",
  "format": "tf" | "mcq" | undefined,
  "choices": ["A. 38", "B. 308"],        // chỉ với mcq
  "answerKey": { … },                     // xem mục 6
  "solutionNarrative": "lời giải mẫu để bé tự so"
}
```

### `usedIn` — hình đứng ở đâu

| Giá trị | Nghĩa |
|---|---|
| `hook` · `trap` · `mantra` | gắn vào màn tương ứng |
| `screen:S3` | gắn ĐÍCH DANH màn giảng S3 |
| `item:C8` | gắn vào **câu hỏi C8** — dùng khi đề nằm trong hình |

`screen:` và `item:` là mở rộng bắt buộc phải có. Lớp 5 nguyên bản chỉ đặt được
**hai** hình trong phần giảng; sách nào nhiều hình hơn là đặt sai chỗ.

### Kỳ sát hạch (ôn tập · thi cuối)

```jsonc
{
  "id": "DCR:KSN2.C1", "chapter": 1, "loai": "ontap" | "ai",
  "name": "ÔN TẬP 1 · VƯỢT CỔNG VƯƠNG QUỐC SỐ",
  "need": 8,                                  // ngưỡng đạt LẤY TỪ SÁCH, không ghim cứng
  "examA": [{
    "qno": 1, "text": "…", "answer": "…",
    "diagnosesMicro": "DL:KSN2.B01",           // ← BẢNG TỰ SOI của sách
    "trapName": "Bài 1 · NGÔI NHÀ TRĂM…"       // tên bài viết đủ chữ cho bé đọc
  }],
  "deB": [], "dapAnB": {}, "hinh": []
}
```

`diagnosesMicro` là thứ đáng giá nhất của phần ôn tập: bé sai câu nào, bấm một nút
là mở đúng bài cần ôn. Sách nào có "Bảng tự soi" thì **phải** trích được vào đây.

---

## 3 · Dây chuyền — bảy bước, chạy liền nhau

```bash
python3 tools/lam_<quyen>.py     # cả bảy bước
cd web && npm test && npm run build
```

| # | Bước | Ra | Ghi chú |
|---|---|---|---|
| 1 | trích thô từ `.docx` | `data/<q>_tho.json` | GIỮ NGUYÊN CHỮ. Phần nằm giữa hai bài cất riêng vào `sauBai` |
| 2 | làm lời văn dễ hiểu | `data/<q>_dehieu.json` | bảng `VIET_LAI` khớp nguyên văn; giữ bản gốc ở `muc[*].goc` |
| 3 | dựng dữ liệu bài học | `data/<q>/*.json` | **ghi đè trọn tệp** |
| 4 | gắn hình vào bài | sửa `data/<q>/` | **PHẢI sau bước 3** |
| 5 | trích ôn tập + đề thi | `data/<q>_ontap.json` | nguồn là `sauBai` của bước 1 |
| 6 | tách câu thành ô điền | `data/<q>_dapan.json` | hợp nhất với bản viết tay |
| 7 | dựng bản khuôn chung | `web/public/content/…` | app đọc bản này |

Vẽ hình tách riêng (`ve_hinh_<quyen>.py`) — chạy khi sửa hình, vì vẽ chậm mà bản
mô tả hình gần như không đổi theo lời văn.

---

## 4 · Chuẩn hình vẽ

**Bé nhìn vô phải hiểu ngay. Không ẩn dụ, không từ lạ.**

- Bỏ tên gọi lạ của sách: *"DÃY THỎ FIBONACCI"* → **"Mỗi số = hai số liền trước cộng lại"**
- Nhãn ghi **phép tính thật** (`+1, +2, +4, +8`) thay vì `+ chính nó`
- Vẽ đúng thứ bé phải làm: chân con vật phải **đếm được**, chấm tròn phải **đếm được từng cái**
- Một hình một dòng chốt, viết bằng lời thường, nói đúng cách làm
- Ô mờ (không đếm) và ô đỏ (phải điền) là **hai màu khác nhau** vì là hai việc khác nhau

**Kỹ thuật**

- Nguyên mẫu ở `figforge/arch_<quyen>.py`, dùng `figforge/core.py` — **bảng màu đóng**,
  phải khớp `web/tailwind.config.js`. Đổi màu là phải vẽ lại toàn bộ hình.
- Dùng màu thương hiệu, **không** bắt chước màu sách.
- Mỗi hình một `sha256_16`; app dùng nó làm dấu phiên bản nên sửa một hình chỉ tải lại hình ấy.
- **Đúng toán trước, đẹp sau**: tia số phải đặt mốc theo GIÁ TRỊ, cung nhảy chỉ nối
  các mốc THUỘC dãy.

**Neo hình** — theo thứ tự bước (`neoBuoc: 2`) hoặc mã câu (`neoCau: "C8"`).
Không bao giờ neo theo nguyên văn dòng.

Hình chưa có chỗ đặt thì đánh dấu `hoan` và **in ra mỗi lần chạy** — im lặng bỏ qua
là lần sau tưởng đã gắn rồi.

---

## 5 · Chuẩn lời văn — bé đọc phải hiểu ngay

Sách gốc viết cho người lớn đọc và cho người soạn dùng. Ba thứ luôn lọt ra màn hình:

**1. Ký hiệu vượt cấp.** Lớp 5 chưa học tập hợp, chia hết bằng ký hiệu, `≤ ≥`, suy ra.
Viết bằng lời: `108 ⋮ 9` → **"108 chia hết cho 9"**; `d ∈ {2;3;7;8}` → **"d là 2, 3, 7
hoặc 8"**; `0 ≤ số dư < số chia` → **"số dư bé hơn số chia"**.
GIỮ những dấu đã học: `< > = ≠` và dấu phép tính.

**2. Mã nội bộ của người soạn.** `K3 — hỏi ngược:` · `Ca chuẩn K1+K2` · `Đ5.1` đứng
ngay đầu câu. Bé đọc không hiểu gì mà lại là chữ đầu tiên nhìn thấy.

**3. Ví von bọc ngoài câu toán.** `Thần chú tiệm bánh: chia càng nhiều phần — lát càng
mỏng!` Phần sau dấu hai chấm đã là toán nói thẳng; chỉ cái vỏ là ví von — **bỏ vỏ, giữ
ruột**: `Câu cần nhớ: chia càng nhiều phần — lát càng mỏng!`
Giữ nhân vật và mô hình đếm được (đóng kẹo vào túi); bỏ thứ chỉ để cho kêu.

**Tiêu đề hình không quá 120 chữ.** Trên ngưỡng ấy nó là một đoạn văn đè lên đầu hình,
không ai đọc — dù phần hình bên dưới vẽ rất rõ. Mượn `title` của bài làm tiêu đề.

### Cách làm — và ba cái chốt bắt buộc

| việc | công cụ |
|---|---|
| sửa lời văn theo luật | `tools/de_hieu_lop5.py` |
| rút gọn tiêu đề hình | `tools/tieu_de_hinh_lop5.py` |
| vẽ lại hình có chữ vừa đổi | `tools/ve_lai_lop5.py` |
| chỗ ví von phải viết tay | `data/lop5_loi_van_tay.json` |
| giữ không cho mọc lại | `web/test/lop5.test.mjs` |

**Chốt 1 — chỉ sửa TRƯỜNG BÉ ĐỌC.** Chốt danh sách bằng cách ĐỌC MÃ GIAO DIỆN, đừng
đoán: `mechanism`, `skills`, `videoSpec`, `numberRange`, `display.lines` không hiện lên
màn hình. Sửa cả những chỗ ấy là đụng dữ liệu người soạn dùng mà chẳng lợi gì.

**Chốt 2 — soát mất số trước khi ghi.** So *đa tập* chữ số trước và sau. Luật dịch sai
thường nuốt mất một con số mà câu vẫn đọc trôi. Chỉ ba nguồn mất số là hợp lệ: chữ số
trong mã `K1`/`Đ5.1`, và số `0`/`1` của vế `0 ≤ x <`.

**Chốt 3 — bảng viết tay phải khớp.** Mục nào không khớp chỗ nào **và** bản thay cũng
không có mặt trong sách thì báo ngay: bảng đang nói một đằng, sách một nẻo. Đừng báo khi
chỉ thiếu vế đầu — công cụ chạy được nhiều lần, lần thứ hai thì chữ đã đổi xong.

**Luật hẹp trước, luật rộng sau.** Luật rộng chạy trước sẽ nuốt mất ngữ cảnh mà luật hẹp
cần. Và **đừng viết luật xoá mã giữa câu** — xem bẫy 16.

---

## 6 · Chuẩn đáp án — chấm máy đúng chỗ chấm được

### Các dạng khoá (bộ chấm `web/src/lib/flow.js` hiểu sẵn)

```jsonc
{ "value": 72 }                                     // một đáp số
{ "values": [12, 30, 68], "ordered": false }        // dãy số
{ "accept": ["4 - 4", "4-4", "4 và 4"] }            // nhiều cách viết đều đúng
{ "parts": [                                        // NHIỀU Ô CÓ NHÃN — dùng nhiều nhất
    { "label": "trăm", "value": 3 },
    { "label": "134", "value": "chẵn", "options": ["chẵn", "lẻ"] }  // có options → nút bấm
]}
{ "value": true }        // format: "tf"
{ "choice": "B. 308" }   // format: "mcq", kèm choices[]
```

### Luật viết đáp án

1. **KHÔNG BAO GIỜ tự nghĩ ra đáp án.** Mọi giá trị rút từ lời giải của sách.
2. **Nhãn ô lấy từ ĐỀ BÀI, không lấy từ lời giải.** Nhãn `[40 gồm 4 chục]` là cho
   không bé đáp án.
3. **Đề hỏi mấy thứ thì mấy ô.** Hỏi "mấy con gà, mấy con chó" mà chỉ một ô là sai.
4. **Không tách ô cho bước trung gian** sách không giao — đó là đổi đề.
5. Không chắc → để tự chấm, có `solutionNarrative` để bé đối chiếu.
6. Việc làm bằng tay, câu "vì sao", đề mở → **cố ý** giữ tự chấm, đánh dấu `thucHanh`.

### Suy máy được tới đâu

Suy đáp án từ lời văn **chỉ dùng được cho khuôn cố định**. Số liệu thật của lớp 2:

| | |
|---|---|
| máy suy ra (8 luật hẹp, đã soát tay từng câu) | 88 / 281 |
| viết tay | 154 / 281 |
| cố ý để tự chấm | 39 / 281 |

Đã thử 3 luật "thông minh" hơn, **phải bỏ 2** vì suy sai. Đừng thử lại — mã và lý do
còn trong `tools/tach_cau_lop2.py`.

**Tự soát bài của mình:** mọi con số viết tay phải **xuất hiện trong lời giải của
sách**. Chốt này bắt được lỗi thật (sách viết *"một phần tư"* bằng chữ, tôi ghi `4`).

---

## 7 · Cổng nghiệm thu — phải có những phép kiểm nào

Mỗi quyển một tệp `web/test/<quyen>.test.mjs`. **Soi loại lỗi HỎNG MÀ KHÔNG BÁO** —
lỗi làm app vỡ thì tự thấy, không cần kiểm.

- [ ] đủ số bài · đủ mục · số câu khớp
- [ ] chữ nghĩa **không mất**: đếm dòng từng mục so với sách
- [ ] lời văn viết lại **không khó hơn** bản gốc; giữ ≥ 90% lượng chữ
- [ ] không lẫn phần khác (ôn tập · đáp án · tiêu đề chương) vào bài
- [ ] **hình đã vẽ = đã gắn + trong kỳ thi + hoãn** ← bắt được hình rơi mất **2 lần**
- [ ] hình neo vào chỗ **có thật**; sha khớp ảnh thật
- [ ] mỗi màn giảng chỉ dạy một nguyên tắc; mọi nguyên tắc đều có màn nhận
- [ ] `prev`/`next` khớp thứ tự
- [ ] đáp án đúng hình dạng bộ chấm hiểu
- [ ] ô bấm chọn: **đáp án nằm trong danh sách phương án**
- [ ] Bảng tự soi trỏ vào bài **có thật**
- [ ] tiền tố mã bài không trùng / không là tiền tố của nhau

**Chạy cổng đúng cách:**

```bash
cd web && npm test
```
Các tệp nối bằng `&&` — một tệp vỡ là **dừng cả chuỗi** mà tổng PASS trông vẫn đẹp.
Luôn soi **mã thoát** và **số tệp chạy xong**.

**Đừng để phép kiểm sai.** Tôi viết hai phép kiểm "nhãn có lộ đáp án không", cả hai
báo động giả (6 chỗ và 8 chỗ) rồi phải bỏ. Việc ấy phải soát bằng mắt. **Một phép
kiểm sai tệ hơn không có** — nó cho cảm giác an toàn giả.

---

## 8 · Hai mươi lăm cái bẫy đã dính

Mỗi cái đều thuộc loại **hỏng mà không có gì báo**.

### Dây chuyền

1. **Gắn hình trước bước dựng dữ liệu** → mất sạch hình, dữ liệu vẫn hợp lệ, bài vẫn chạy.
2. **Neo hình theo nguyên văn dòng** → bước 2 viết lại lời văn là trượt hết.
3. **Chạy lẻ bước 3 mà quên bước 2** → app hiện lại lời văn khó của sách gốc.
4. **`dist/` không tự đồng bộ** → phải `npm run build`.

### Bóc tách

5. **Cắt bài tới tiêu đề bài kế tiếp** → ôn tập, đáp án cả chương, tiêu đề chương sau
   rơi hết vào mục CUỐI của bài (639 dòng rác, lộ luôn đáp án cho bố mẹ).
6. **Đáp án ôn tập đè đáp án bài** — cùng đánh `C1, C2…`. 60 lời giải gắn sai câu.
7. **Sách không nhất quán, chỗ nào cũng có thể lệch:**
   `Bước 1.` / `Nhịp 1 —` / `Vũ khí 2 —` · `C4 (tổng 3):` / `C10 — MẬT THƯ:` ·
   `Vụ 1:` / `VB1:` · `Đạt 8/12 câu` / `Phá được 6/8 vụ` ·
   `Câu 6, 7 và dãy C của mật thư → thuộc Bài 10`
8. **Mẫu tách câu đòi dấu chấm** → 165 câu quiz ghi `Câu 1 (Đúng/Sai?):` không hề
   được tách ra, nằm lẫn trong phần chữ.

### Đáp án

9. **Số cuối một vế thường là số trong lời GIẢI THÍCH**, không phải đáp án:
   `"75 − 57 = 18 — nằm trong bảng nhân 9"` → lấy nhầm **9**.
10. **Nhãn dựng từ lời giải lộ đáp án.**
11. **Đề hỏi hai thứ mà chỉ lấy một đáp** (`viết HAI số tiếp theo`; `mấy con gà, mấy con chó`).
12. **Đáp án viết bằng chữ**: sách ghi *"một phần tư"*, bé gõ `tư` bị chấm oan.

### Hình

13. **Tia số đặt mốc cách đều** → `18 → 20 → 21` trông như ba khoảng bằng nhau. Sai tỉ lệ còn tệ hơn không có.
14. **Cung nhảy nối vào ga tàu ĐI QUA** → dạy ngược điều bài đang dạy.
15. **Nhãn hàng đè ô đầu · cỡ chữ mỗi ô tính riêng** (`2` to hơn `10` trong cùng hàng).

### Lời văn

16. **Luật xoá mã nội bộ GIỮA CÂU.** Mẫu `K<số>` + khoảng trắng + chữ thường biến
    *"Ca chuẩn K1+K2 từ sách"* thành *"Ca chuẩn K1+từ sách"* — hỏng câu mà vẫn đọc
    trôi nên rất dễ lọt. Mã giữa câu phải xử bằng luật RIÊNG cho từng cụm.
17. **Dọn khoảng trắng đụng dấu `:`** → `47 : 5` thành `47: 5`, hỏng mọi phép chia của
    cả quyển. Trong toán Việt `:` là PHÉP CHIA, không phải dấu câu. `= ?` cũng phải
    giữ nguyên dấu cách.
18. **Bỏ mã nội bộ xong còn trơ dấu chấm** → màn bài mẫu hiện đúng một dấu `.` dưới
    biểu tượng 📌. Kết quả chỉ còn dấu câu thì trả về RỖNG.
19. **Tiêu đề hình chép nguyên `objective.text`** → 397 chữ đè kín đầu hình. 122 hình
    dính, mà phần hình bên dưới vẫn vẽ đẹp nên nhìn lướt không thấy sai.

### Hình và sổ

20. **Sửa `figureSpec.params` mà không vẽ lại** → dữ liệu nói một đằng, ảnh hiện một
    nẻo. Bé vẫn nhìn thấy ký hiệu cũ trên hình. Không có gì báo, vì cả hai đều hợp lệ.
21. **Quên cập nhật `data/figure_manifest.json`** — nơi THỨ BA chép lại mã kiểm và lời
    chú. Bài học đúng, sổ sai. Khoá sổ là `<mã bài>#<mã hình>`, không phải `<mã hình>`.

### Mã nguồn

22. **Biến trong vòng lặp đè tham số của hàm** → `series.prev` ra danh sách chỉ số dòng.
23. **Phép kiểm so trên số ĐÃ LÀM TRÒN** → 7,6% bị làm tròn thành 8 rồi trượt oan.
24. **Component đọc dữ liệu bất đồng bộ MỘT LẦN lúc dựng** → sổ đăng ký về sau thì
    màn hình thiếu hẳn một mảng.
25. **Danh sách tệp kiểm gõ tay trong `package.json`** → thêm tệp kiểm mà quên đăng ký
    thì nó nằm im, tưởng có kiểm mà không có. Quét cả thư mục: `for f in test/*.test.mjs`.

---

## 9 · Quy trình khi thêm một quyển mới

### Bước 0 · Khảo sát trước khi gõ dòng nào

```python
# đếm bài, mục, câu, hình; liệt kê MỌI tiêu đề để thấy chỗ sách không nhất quán
import zipfile, re
z = zipfile.ZipFile('docs/<sach>.docx')
# word/document.xml → đoạn văn;  word/_rels/… → ảnh
```

Phải trả lời được **trước khi viết bộ trích**:

- [ ] Bao nhiêu bài? Mỗi bài có những mục nào? Mục có đánh dấu cố định không (`①…⑧`)?
- [ ] Đáp án nằm ở đâu — cuối bài hay cuối chương? Đánh mã thế nào?
- [ ] Có ôn tập / đề thi không? Có **Bảng tự soi** không?
- [ ] Bao nhiêu hình? **Mỗi hình thuộc bài nào, mục nào, sau bước nào?**
- [ ] Hình nào là **hình toán** (thiếu là không làm được bài), hình nào chỉ trang trí,
      hình nào nên làm thành **thành phần giao diện** thay vì ảnh tĩnh?
- [ ] Sách dùng những cách viết nào cho cùng một thứ? (liệt kê hết — xem bẫy số 7)

Ghi kết quả vào `docs/khao_sat_<quyen>.md`. **Khảo sát sai thì mọi bước sau đều sai.**

### Bước 1 · Phân loại hình

Gom 100% hình thành nhóm, đếm mỗi nhóm, **kiểm kín** (tổng nhóm = tổng hình). Ghi ra
`docs/phan_loai_hinh_<quyen>.md`. Đây là thứ quyết định cần mấy nguyên mẫu.

> Lớp 2: 75 hình → 15 nhóm → 17 nguyên mẫu. Bản khảo sát đầu đoán "5–8 nguyên mẫu là
> phủ hết" — **thiếu hơn hai lần**.

### Bước 2 · Dựng dây chuyền

Chép `tools/rut_lop2.py` · `chuan_lop2.py` · `khuon_chung.py` làm mẫu. Phần khác nhau
giữa các sách nằm gần hết ở **bộ trích** (bước 1) và **bảng khớp mục** (`khuon_chung`).

### Bước 3 · Vẽ hình

Nhóm lớn trước. Mỗi nhóm: viết nguyên mẫu → vẽ vài hình → **đặt cạnh bản sách để
so** → sửa → vẽ cả nhóm.

Đừng vẽ hết rồi mới xem. Bốn lỗi trình bày của nhóm đầu tiên (dòng chốt rơi tận đáy,
nhãn đè ô, hàng cách quá xa, cỡ chữ lẫn lộn) nếu phát hiện muộn thì phải sửa 70 hình.

### Bước 4 · Đáp án

Viết luật hẹp → **in ra soát tay TỪNG CÂU** → cái nào sai thì bỏ luật, viết tay.
Đừng tin luật chưa soát.

### Bước 5 · Cổng nghiệm thu

Viết theo danh sách mục 7. Mỗi lần bắt được lỗi thật thì **thêm một phép kiểm cho
lỗi ấy**.

### Bước 6 · Khai vào sổ đăng ký

`data/chuong_trinh.json` — thêm một mục là kệ sách tự hiện, **không sửa giao diện**:

```jsonc
"lop3": {
  "ma": "lop3", "mon": "toan", "lop": 3, "loai": "hoc",
  "ten": "Toán Tư Duy lớp 3",
  "tienTo": "DL:KSN3.",         // KHÔNG được trùng / là tiền tố của quyển khác
  "thuMuc": "lop3",
  "soBai": 40,
  "doc": { "chuTo": true }      // nhịp đọc theo lứa tuổi
}
```

Rồi xoá mục tương ứng khỏi `sapCo`.

### Bước 7 · Kiểm bằng mắt rồi mới deploy

```bash
cd web && npm test && npm run build && npx vite preview
```
Đi trọn **một bài thật**: mở bài → xem hình đúng chỗ → làm câu luyện tập sai rồi
đúng → làm sát hạch → xem Bảng tự soi trỏ đúng bài.

Deploy xong **gọi thẳng vào bản chạy thật** để kiểm, đừng tin dòng "Deploy complete":

```bash
curl -s https://ky-su-nhi.web.app/content/<thuMuc>/index.json | head
curl -s https://ky-su-nhi.web.app/content/figures/<HINH>.png | shasum -a 256 | cut -c1-16
```

---

## 10 · Ước lượng công sức — số liệu thật của lớp 2

| Việc | Khối lượng |
|---|---|
| Khảo sát + phân loại hình | 75 hình → 15 nhóm |
| Dây chuyền bóc tách | 7 bước, ~900 dòng Python |
| Vẽ hình | 70 hình · 17 nguyên mẫu · ~800 dòng |
| Đáp án | 88 suy máy + 154 viết tay |
| Cổng nghiệm thu | 68 phép kiểm riêng cho quyển |

Phần **tốn công nhất** là hình (17 nguyên mẫu) và đáp án viết tay (154 câu). Phần
**dễ sai nhất** là bóc tách — vì sách không nhất quán, mà sai thì im lặng.

---

## 11 · Tài liệu để lại cho mỗi quyển

| Tệp | Nội dung |
|---|---|
| `docs/khao_sat_<quyen>.md` | kết quả bước 0 |
| `docs/phan_loai_hinh_<quyen>.md` | nhóm hình, kiểm kín |
| `docs/soat_<quyen>_<ngày>.md` | bản soát đối chiếu sách |
| `docs/tiep_theo_<quyen>.md` | điểm dừng · việc còn lại · **việc đã cân nhắc và LOẠI** |

Mục *"đã cân nhắc và loại"* quan trọng ngang phần việc còn lại: nó ngăn phiên sau
đề xuất lại một ý đã đo và bác bỏ.
