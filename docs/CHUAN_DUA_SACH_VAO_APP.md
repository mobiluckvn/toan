# Chuẩn đưa một quyển sách vào phần mềm

Viết sau khi làm xong **Toán lớp 2** (33 bài · 120 hình · 8 ôn tập · 3 ải) và
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
  "answerKey": { … },                     // xem mục 7
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

**Hình ĐẾM thì phải ĐẾM ĐƯỢC.** Bài "đếm hình / đếm khối / chia có dư" chỉ đạt khi bé
đếm được ngay trên hình:

- Vẽ **đủ số vật**, đừng vẽ một cái rồi ghi "3 cái" bên dưới — đáp án nằm sẵn thì bé
  không đếm gì, mà hình vẫn "có hình, có số, có lời chú" nên nhìn lướt không thấy sai.
- Hình ghép phải là **một hình liền** bị vạch chia, không phải mấy hình rời xếp cạnh
  nhau. Vẽ rời thì cái hình TO đang ẩn — thứ cả bài đang dạy — biến mất.
- Bản tô đậm hình ghép phải **bỏ vạch chia bên trong**, không thì bé vẫn thấy hai mảnh
  chứ không thấy một hình.
- Đếm khối thì xếp **tháp thật**, có khối nấp hàng sau; kèm bản trải phẳng từng tầng.
- Chia có dư thì **vẽ cả phần dư**.
- Hình trộn nhiều loại thì **xếp xen kẽ**; gom theo loại là nhìn một cái ra số, khỏi đếm.
- Nguyên mẫu vẽ đúng **một hình cho mỗi mục khai báo**: nhãn ghi "4 khối" trên một mục
  nghĩa là một khối đang đeo biển "4 khối". `web/test/hinhdem.test.mjs` soi đúng chỗ này.

### Hình cho BÀI TẬP — đề và lời giải là HAI hình

Bài tập cần hình thì cần **hai** hình, không phải một:

| chặng | `usedIn` | hiện khi nào | được chứa gì |
|---|---|---|---|
| đề | `item:C8` | ngay cùng câu hỏi | hình + số đo cho sẵn. **Không** đáp án |
| lời giải | `item:C8:giai` | sau khi bé làm xong | chỉ ra TỪNG hình tìm được, hoặc trải phẳng từng tầng |

Gộp làm một là lộ đáp án lúc bé chưa làm. Bỏ hình lời giải thì bài đếm hình chỉ còn
một câu chữ — bé vẫn không biết mình **sót cái nào**.

Trường `vaiTro: 'giai'` phải đi qua **đủ bốn chặng**, rơi ở chặng nào cũng im lặng:
`data/<quyen>_hinh.json` → sổ tay hình → bước gắn hình → `khuon_chung.py`.
Sổ tay ghi theo danh sách khoá CỐ ĐỊNH nên thêm trường mới là phải sửa cả chỗ ghi sổ.

Chưa có nguyên mẫu vẽ được thứ đề bài mô tả thì **viết nguyên mẫu mới**, đừng ghi số đo
thành một dòng chữ dưới hình: `"2 cm · 3 cm · 4 cm"` không cho bé biết số nào của cạnh
nào, mà bài chu vi thì phải cộng đúng từng cạnh.

### Đường LÙI về quyển dưới

Quyển nào nối tiếp một quyển đã có thì **phải khai đường lùi**: bài lớp 3 trỏ về bài
lớp 2 cùng chủ đề, để bé học đuối thì quay lại luyện gốc chứ không bỏ dở.

Bảng ở `data/<quyen>_gan_<quyenduoi>.json`, mỗi dòng ghi cả **CĂN CỨ**:

| căn cứ | nghĩa |
|---|---|
| `sach` | sách CHỈ ĐÍCH DANH "Bài n lớp 2" — chắc chắn |
| `chuDe` | sách chỉ nhắc chủ đề, không nêu số bài; ghép theo tên bài — **cần soát tay** |
| `khong` | quyển dưới không có bài cùng chủ đề — cố ghép là chỉ đường sai |

Phải có **đủ mọi bài**, kể cả dòng `khong`. Bỏ trống thì không phân biệt được "chưa
làm" với "đã xét và kết luận là không có". Trỏ sai còn tệ hơn không trỏ: bé bấm vào
rồi lạc sang bài chẳng liên quan, mất niềm tin vào chính cái nút ấy.

Sách lớp 3 để sẵn mối nối này ở mục `HẠT MẦM NĂM NGOÁI` — 21/34 bài nêu đích danh số
bài lớp 2, 11 bài chỉ nhắc chủ đề, 2 bài lớp 2 không có gì tương ứng.

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

## 6 · Chuẩn màn mở bài — ngắn, nêu thẳng bài toán

Màn mở là chỗ phình to nhanh nhất, mà phình theo kiểu rất khó thấy: **lời dẫn và hình
nói cùng một nội dung**. Đo thật trước khi sửa:

| | lời dẫn | chữ trên hình mở | tổng |
|---|---|---|---|
| lớp 5 (168 bài) | 208 chữ | 155 chữ (hình chép lại đúng hai câu ấy) | **363** |
| lớp 2 (33 bài) | 297 chữ | — | **297** |

Bé đọc hết ngần ấy vẫn **chưa biết bài hỏi gì**, vì đề bài không nằm ở đó.

### Bốn luật

**1 · Lời mở là MỘT CÂU NÊU BÀI TOÁN.** Không kể chuyện dài. Sau khi sửa: lớp 5 còn
80 chữ, lớp 2 còn 0 chữ. Câu đề lấy từ trường đã soạn sẵn, đừng viết mới:

| quyển | nguồn câu đề |
|---|---|
| có `knowledgeCore` | `canonicalExamples[0].problem` → `workedExample.problem` → `objective.kidText` |
| lớp 2 (mục sách) | dòng mở đầu bằng `Đề bài` trong mục `viDuMau` |

**2 · Lời và hình KHÔNG được nói cùng một nội dung.** Lời nêu đề, hình nêu **cái bẫy**.
Hình lời thoại giữ **đúng MỘT bong bóng** — câu sai mà bé hay mắc. Câu gỡ chuyển sang
phần giảng ở màn ngay sau; để ở màn mở là nói trước mất.

**3 · BÀI HÌNH HỌC bắt buộc mở bằng HÌNH VẼ THẬT**, không phải bong bóng chữ. Và đó
phải là **bản ĐỀ của chính hình giải** — cùng điểm, cùng số đo cho sẵn — để phần giải
đi tiếp trên đúng hình ấy, bé nhìn một hình từ đầu đến cuối.

Bản đề = bản giải **bỏ hết dấu vết đáp án**:

```
bỏ  formula · note · verdict · result
bỏ  mọi nhãn có dấu '='   (nhãn kết quả: "S = 30 cm²")
giữ nhãn số đo cho sẵn    ("đáy 12", "cao 5") — không có dấu '='
bỏ  cả TIÊU ĐỀ hình
```

Bỏ tiêu đề vì lời dẫn ngay trên đã nêu đề, ô "Câu hỏi" ngay dưới đã nêu bẫy — ghi thêm
lên hình là lặp lần thứ ba, đúng thứ cần tránh.

**4 · Câu dẫn chỉ giữ khi KHÔNG chứa con số.** Chuyện mở bài hay kể một bộ số khác với
bộ số của đề — *"ba tấm thẻ 2, 5, 8"* rồi đề lại cho *4, 0, 9*. Ghép vào nhau thành hai
đề đá nhau ngay dòng đầu tiên bé đọc.

### Sửa ở BỘ DỰNG, không sửa tệp đã dựng

Quyển nào dựng qua `tools/khuon_chung.py` thì sửa ở đó. Sửa thẳng `web/public/content/`
là lần chạy dây chuyền sau ghi đè sạch — mà chẳng có gì báo.

| việc | công cụ |
|---|---|
| lớp 5 (tệp bài học rời) | `tools/mo_bai_lop5.py` |
| lớp 2 (dựng từ mục sách) | `tools/khuon_chung.py`, hàm dựng `screens` |

Nhãn của màn là **"BÀI TOÁN"** (`StepView.jsx`, nhánh `hook`), không phải "TÌNH HUỐNG"
— bé đọc nhãn là biết phải làm gì.

---

## 7 · Chuẩn đáp án — chấm máy đúng chỗ chấm được

### Các dạng khoá (bộ chấm `web/src/mon/toan/lib/flow.js` hiểu sẵn)

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

### Ô NHẬP — năm luật, có phép kiểm TỰ ĐỘNG áp cho mọi quyển

`web/test/luat_o_nhap.test.mjs` đọc danh sách quyển từ `content/chuong_trinh.json`,
nên **quyển mới vừa khai vào sổ là bị soi ngay** — không ai phải nhớ chép lại luật,
và không ai chép thiếu. Năm luật, mỗi luật rút từ một lỗi ĐÃ XẢY RA THẬT:

| # | luật | vì sao |
|---|---|---|
| 1 | **Quyển ĐỌC CHẬM: mọi ô là điền SỐ hoặc BẤM CHỌN** | bé 7-9 tuổi gõ chậm; sai chính tả một chữ, hay thừa một dấu cách trong biểu thức, là mất điểm oan — bài đang kiểm TOÁN chứ không kiểm kỹ năng gõ |
| 2 | **Mồi nhử phải THẬT SỰ SAI** | mồi vô tình cũng đúng thì bé chọn nó bị chấm sai oan, tệ hơn cả không có trắc nghiệm |
| 3 | **Đáp án bấm chọn nằm trong danh sách nút** | lệch một chữ là bé bấm đúng mà máy báo sai — bé thì tin máy chứ không tin mình |
| 4 | **Ô nào cũng có nhãn, nhãn không đưa sẵn đáp án** | nhiều ô không nhãn thì bé không biết ô nào hỏi gì; nhãn dựng từ lời giải là cho không đáp số |
| 5 | **Chấm máy ≥ 85% câu luyện tập** (quyển đọc chậm) | dưới ngưỡng ấy bé làm xong không ai biết đúng sai — sổ phụ huynh và bảng cô giáo trống |

**Luật 1 chỉ áp cho quyển đọc chậm**, nhận theo cờ `doc.moiManMotMuc` trong sổ đăng
ký chứ không theo tên quyển. Lớp 5 là bạn 10-11 tuổi, gõ biểu thức được — 209 ô gõ
chữ của nó là CHỦ Ý, không phải nợ bỏ quên. Thêm lớp 4 chỉ cần khai cờ, khỏi sửa
phép kiểm.

**Ba lần phép kiểm này đỏ OAN, và cả ba đều dạy một điều: phép kiểm chặt hơn bộ chấm
là sai, không phải nghiêm.**

1. So chuỗi thô nên đỏ 5 câu lớp 5 — quyển ấy cố ý để lý do trong ngoặc ở `value`
   (`"cặp vàng (1,25 × 8)"`) còn nút chỉ in phần cốt lõi, mà bộ chấm tha đúng chỗ đó.
   → dùng chung `splitAside` / `answerCore` với bộ chấm.
2. Quy gạch ngang ngắn `–` (U+2013) thành phép trừ, nên nhãn `mắt 3–4` (một KHOẢNG)
   bị tính ra −1. → chỉ tính khi có dấu phép tính không nhập nhằng.
3. So mồi nhử bằng GIÁ TRỊ ở câu hỏi về DẠNG VIẾT: lớp 5 hỏi "viết 2,73 thành tổng
   giá trị các hàng", mồi `2 + 0,73` cộng lại cũng ra 2,73 nhưng không phải tách theo
   hàng — đó là mồi TỐT, đúng lỗi bài muốn bẫy. → luật 2 chỉ áp khi đáp án là một
   CON SỐ TRẦN.

### Cách hạ số câu tự chấm

Câu "vì sao" thường hỏi **một con số kèm một lời giải thích**. Tách con số ra thành ô
là đo được ngay, lời giải thích để bé đối chiếu với `solutionNarrative`. Lớp 3 chuyển
được 28 câu nhờ cách ấy, kéo tự chấm từ 37 xuống 9.

Còn giữ tự chấm là CỐ Ý cho: đề mở (bé tự sáng tác đề) · việc làm bằng tay (dùng
compa vẽ) · đọc số thành chữ (*"năm mươi tư"* và *"năm mươi bốn"* đều đúng) · sách chỉ
nêu MỘT trong nhiều đáp án đúng (*"ví dụ 6 × 6 + 1 = 37"*). Khai đích danh từng câu
kèm lý do, để lần sau không ai tưởng là bỏ sót.

### Suy máy được tới đâu

Suy đáp án từ lời văn **chỉ dùng được cho khuôn cố định**. Số liệu thật của lớp 2:

| | |
|---|---|
| máy suy ra (8 luật hẹp, đã soát tay từng câu) | 0 / 568 |
| viết tay | 568 / 568 |
| cố ý để tự chấm | 0 / 568 |

Đã thử 3 luật "thông minh" hơn, **phải bỏ 2** vì suy sai. Đừng thử lại — mã và lý do
còn trong `tools/tach_cau_lop2.py`.

**Tự soát bài của mình:** mọi con số viết tay phải **xuất hiện trong lời giải của
sách**. Chốt này bắt được lỗi thật (sách viết *"một phần tư"* bằng chữ, tôi ghi `4`).

---

## 8 · Cổng nghiệm thu — phải có những phép kiểm nào

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
- [ ] **màn mở**: lời dẫn ≤ ~150 chữ và KHÔNG trùng chữ với hình mở
- [ ] **bài hình học** đều có hình vẽ ở màn mở, và hình ấy KHÔNG chứa đáp án
- [ ] **bài tập cần hình** có đủ cặp `item:CX` + `item:CX:giai`
- [ ] hình đếm **đếm được**: không nhãn nào ghi "N cái" mà chỉ vẽ một
- [ ] không ký hiệu vượt cấp · không mã nội bộ · không ví von (mục 5)

**Chạy cổng đúng cách:**

```bash
cd web && npm test
```
`package.json` quét cả thư mục `test/` nên tệp kiểm mới tự được chạy — đừng quay lại
kiểu gõ tay từng tệp nối bằng `&&`: quên đăng ký một tệp là nó nằm im, mà tổng PASS
trông vẫn đẹp. Dù vậy vẫn luôn soi **mã thoát** VÀ **số tệp chạy xong**: một tệp lỗi cú
pháp thì nó không nạp được, tổng phép kiểm tụt hàng trăm mà chỉ hiện đúng một dòng ✗.

**Đừng để phép kiểm sai.** Tôi viết hai phép kiểm "nhãn có lộ đáp án không", cả hai
báo động giả (6 chỗ và 8 chỗ) rồi phải bỏ. Việc ấy phải soát bằng mắt. **Một phép
kiểm sai tệ hơn không có** — nó cho cảm giác an toàn giả.

---

## 9 · Bốn mươi bốn cái bẫy đã dính

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

### Hình đếm

22. **Vẽ mỗi loại một cái rồi ghi sẵn số** → bé không đếm được gì. 4 hình lớp 2 dính.
23. **Hình ghép vẽ thành mấy hình RỜI** → mất hẳn cái hình to đang ẩn, tức là mất bài.
24. **Chia có dư mà không vẽ phần dư** → đề nói 17 viên, bé đếm trên hình ra 15.
25. **Nguyên mẫu vẽ `vuong` thành chữ nhật** (2r × 1,6r) trong khi bài dạy phân biệt
    vuông với chữ nhật. Lỗi ở NGUYÊN MẪU nên lan ra mọi hình dùng nó.
26. **Cỡ chấm tính theo từng hàng** → hàng 2 chấm to hơn hàng 3 chấm, cùng một rổ kẹo
    mà viên to viên nhỏ.

### Mã nguồn

27. **Biến trong vòng lặp đè tham số của hàm** → `series.prev` ra danh sách chỉ số dòng.
28. **Phép kiểm so trên số ĐÃ LÀM TRÒN** → 7,6% bị làm tròn thành 8 rồi trượt oan.
29. **Component đọc dữ liệu bất đồng bộ MỘT LẦN lúc dựng** → sổ đăng ký về sau thì
    màn hình thiếu hẳn một mảng.
30. **Danh sách tệp kiểm gõ tay trong `package.json`** → thêm tệp kiểm mà quên đăng ký
    thì nó nằm im, tưởng có kiểm mà không có. Quét cả thư mục: `for f in test/*.test.mjs`.
31. **`git checkout` để xoá lỗi gieo thử** cuốn theo cả phần sửa CHƯA COMMIT trong cùng
    tệp. Sao lưu trước khi gieo, hoặc commit xong mới thử.

### Màn mở bài

32. **Câu dẫn và đề bài kể HAI BỘ SỐ khác nhau** → hai đề đá nhau ngay dòng đầu.
33. **Luật lọc so `len(giữ) != len(gốc)`** — 16 bài có CẢ HAI lời cùng loại nên hai vế
    bằng nhau, luật không chạy mà bảng tổng kết vẫn báo đã sửa. So theo SỐ CÒN LẠI.
34. **Lời thoại bỏ lửng "…" hợp lệ nhờ đối chiếu với lời dẫn** → đổi lời dẫn là mất chỗ
    dựa, phép kiểm đỏ oan. Viết lại thành khẳng định trọn vẹn thì vừa đúng vừa hết lệ thuộc.
35. **Gỡ 'hook' khỏi hình cũ TRƯỚC khi dựng hình mới** → có lúc bài không còn hình mở
    nào, mà công cụ lại đòi phải có sẵn hình mở mới chịu chạy nên bỏ qua luôn cả bài.

### Mã nguồn (tiếp)

36. **Bản vá chú thích nuốt mất dấu đóng `*/`** → 5 tệp kiểm KHÔNG NẠP ĐƯỢC. Tổng phép
    kiểm tụt từ 647 xuống 432 mà chỉ hiện đúng một dòng ✗. Đếm SỐ TỆP thực chạy mới thấy.
37. **Chốt đặt nhầm hàm** vì hai hàm dùng tên biến khác nhau (`loai` với `p.get('loai')`)
    — bản vá "áp dụng thành công" mà chốt nằm ở chỗ không bao giờ chạy tới.
38. **Bố cục tính bề ngang theo SỐ MỤC** → 8 mục thì mỗi mục còn 11 đơn vị, hình vuông
    bị ép thành cột dọc và nhãn chồng lên nhau. Xuống hàng, và lấy cạnh theo cả hai chiều.
39. **Callback dùng state khai SAU nó** → mảng phụ thuộc chạy ngay lúc render nên là
    ReferenceError, không phải `undefined`. Đặt hàm ngay sau chỗ khai.
40. **Đơn vị đếm mặc định "bài"** → kệ sách ghi "26 bài" cho mùa giải, thứ không có bài
    nào. Khai `donVi` ở sổ đăng ký.

### Chữ Việt

41. **Dải `à-ỹ` (U+00E0–U+1EF9) CHỨA CẢ `Đ` `Ơ` `Ư` VIẾT HOA** (U+0110, U+01A0, U+01AF).
    Phép thử "dòng này in hoa" viết kiểu `[^a-zà-ỹ]+$` trượt mọi tiêu đề có Đ/Ơ/Ư — mà
    tiếng Việt thì tiêu đề nào chẳng có. So bằng `s == s.upper()`.
42. **Đếm số ẢNH mà tưởng là đếm số HÌNH** → một ảnh dùng lại nhiều chỗ. Sách lớp 3
    có 80 chỗ neo trên 47 tệp, mà riêng cái nhiệt kế đã chiếm 34 chỗ. Đếm theo TỆP
    thì hụt, đếm theo CHỖ NEO thì thừa — phải tách ảnh lặp ra trước.
43. **Nhìn số ảnh gốc mà ước lượng công vẽ** → lớp 3 có 46 hình toán nhưng gần hết
    nằm ở màn mở; mục giảng chỉ 6 hình cho 34 bài, bài tập KHÔNG có hình nào. Việc
    vẽ nhiều hơn lớp 2 chứ không ít, dù ảnh gốc ít hơn.
44. **Tiêu đề trong sách có tiền tố dấu trang** (`B1  ĐÁP ÁN BÀI 1`) và **mục lục dán
    số trang vào cuối tiêu đề** (`…chính danh27`). Mẫu neo `^ĐÁP ÁN BÀI` hay `…$` đều
    trượt. Cho phép tiền tố, và cắt đuôi số trang trước khi so.

---

## 10 · Quy trình khi thêm một quyển mới

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
nhãn đè ô, hàng cách quá xa, cỡ chữ lẫn lộn) nếu phát hiện muộn thì phải sửa cả 120 hình.

**Ba loại hình, đừng bỏ sót loại nào** (lượt lớp 2 đầu tiên chỉ vẽ loại thứ nhất, phải
quay lại làm hai loại kia):

1. **hình giảng** — neo theo bước (`neoBuoc`)
2. **hình màn mở** — bài hình học bắt buộc có; là bản ĐỀ, bỏ hết đáp án (mục 6)
3. **hình bài tập** — cặp `item:CX` + `item:CX:giai` cho mọi câu mà đề MÔ TẢ một hình
   ("vẽ hình vuông rồi kẻ đường chéo", "tầng dưới 2 hàng × 2 khối")

Dò loại 3 bằng máy: quét lời câu hỏi tìm từ chỉ hình (`vẽ`, `hình vuông`, `khối`,
`đếm hình`, `cạnh`…) rồi đối chiếu với `usedIn` đã có. Lượt lớp 2 quét ra **46 câu nói
tới hình mà 0 câu có hình**.

### Bước 4 · Đáp án

Viết luật hẹp → **in ra soát tay TỪNG CÂU** → cái nào sai thì bỏ luật, viết tay.
Đừng tin luật chưa soát.

### Bước 5 · Cổng nghiệm thu

Viết theo danh sách mục 8. Mỗi lần bắt được lỗi thật thì **thêm một phép kiểm cho
lỗi ấy**.

### Bước 6 · Khai vào sổ đăng ký

Ngoài `ma · mon · lop · ten · tienTo · thuMuc · soBai`, để ý hai trường hay quên:

- **`loai`** — `'hoc'` là chuỗi bài học tuần tự (mở màn Home của lớp); `'giai'` là mùa
  giải, App mở thẳng bảng đấu chứ không đi qua Home.
- **`doc.moiManMotMuc`** — cờ NHỊP ĐỌC CHẬM. Nó quyết ba thứ cùng lúc: phòng học nào
  mở ra, chữ to hay nhỏ, và **có bị áp luật "cấm ô gõ chữ" hay không**. Quyển cho bé
  tiểu học nhỏ (lớp 2, 3, 4) phải bật; bật xong là `luat_o_nhap.test.mjs` soi ngay.
- **`donVi`** — đơn vị đếm hiện trên kệ sách, mặc định `'bài'`. Mùa giải đếm bằng vòng
  đấu nên phải khai riêng.

Khai đủ thì **kệ sách tự hiện, không phải sửa giao diện** — đó là điều sổ đăng ký sinh ra để làm.

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

## 11 · Ước lượng công sức — số liệu thật của lớp 2

Con số đáng nhớ nhất: **45 trên 120 hình là làm ở lượt thứ hai**. Lượt đầu vẽ đủ hình
cho phần giảng rồi tưởng xong, mãi tới khi có người đọc kỹ mới lộ ra màn mở không có
hình và 46 câu bài tập nói tới hình mà không câu nào có hình. Quyển lớp 3 nên tính cả
ba loại hình ngay từ Bước 1 (mục 10) thay vì trả giá hai lượt.

| Việc | Khối lượng |
|---|---|
| Khảo sát + phân loại hình | 75 hình → 15 nhóm |
| Dây chuyền bóc tách | 7 bước, ~900 dòng Python |
| Vẽ hình giảng | 75 hình · 17 nguyên mẫu · ~800 dòng |
| Vẽ hình màn mở + hình bài tập | +45 hình · +5 nguyên mẫu — làm ở lượt SAU, vì lượt đầu chỉ nghĩ tới hình giảng |
| Vá nốt hình màn mở | +16 hình — lượt trên vẫn để 16/33 bài mở ra KHÔNG có hình nào, chỉ lộ khi đếm |
| Dọn hình mồ côi | −130 hình — mười sáu bài chữ tách thành bài video, hình của chúng không ai dùng nữa mà vẫn nằm trong sổ. Ba dòng trên là số hình ĐÃ TỪNG vẽ, cộng lại ra 136. Trong lượt dọn ấy đã xoá NHẦM một hình: `L2H_CANH07` neo ở bài B08 mà thật ra thuộc kỳ ôn tập chương 2 — xem `web/test/hinh_ky_sat_hach.test.mjs` |
| **Tổng hình còn dùng** | **tổng 6 hình · 22 nguyên mẫu** |
| Đáp án | 0 suy máy + 568 viết tay |
| Cổng nghiệm thu | 68 phép kiểm riêng cho quyển |

Phần **tốn công nhất** là hình (22 nguyên mẫu) và đáp án viết tay (568 câu). Phần
**dễ sai nhất** là bóc tách — vì sách không nhất quán, mà sai thì im lặng.

---

## 12 · Tài liệu để lại cho mỗi quyển

| Tệp | Nội dung |
|---|---|
| `docs/khao_sat_<quyen>.md` | kết quả bước 0 |
| `docs/phan_loai_hinh_<quyen>.md` | nhóm hình, kiểm kín |
| `docs/soat_<quyen>_<ngày>.md` | bản soát đối chiếu sách |
| `docs/tiep_theo_<quyen>.md` | điểm dừng · việc còn lại · **việc đã cân nhắc và LOẠI** |

Mục *"đã cân nhắc và loại"* quan trọng ngang phần việc còn lại: nó ngăn phiên sau
đề xuất lại một ý đã đo và bác bỏ.
