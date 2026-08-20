# Dây chuyền dữ liệu Tiếng Anh — từ bản đồ tri thức tới bài chạy được

**Viết 14-08-2026, sau khi lớp 1 chạy xong end-to-end.** Đây là bản ghi lại *đã làm
thế nào*, để lớp 2 không phải mò lại — và để biết chỗ nào từng hỏng.

Lớp 1: **1 bản đồ → 8 loại dữ liệu → 16 bài · 469 câu hỏi · 553 clip tiếng · 37 video.**

---

## 0 · Bức tranh một trang

```
data/ban_do_tieng_anh.json          ① BẢN ĐỒ GỐC — bác cấp, KHÔNG SỬA
        3 989 node · 7 602 cạnh · cả 12 lớp                        (3.5 MB)
   │
   ├──── data/tienganh/lop1_bu.json ② PHẦN BÙ — soạn tay              (46 KB)
   │        nghĩa Việt · IPA · vai từ · hình · dạng số nhiều · ing
   ↓     tools/chuan_tienganh.py --lop 1
data/tienganh/chuan_lop1.json       ③ BẢN CHUẨN — một hình dạng cho mọi lớp
        16 unit · 60 từ · 19 mẫu câu · 10 mối tiên quyết           (59 KB)
   ↓     tools/sinh_bai_tienganh.py --lop 1 --tat-ca
web/public/content/ta1/DL_TA1_B*.json   ④ 16 BÀI HỌC             (340 KB)
data/tienganh/lop1_loi.json             ⑤ SỔ LỜI CẦN ĐỌC — 357 dòng
   │
   ├─ tools/sinh_ontap_tienganh.py   → ⑥ ontap.json · 4 kỳ · 40 câu
   ├─ tools/sinh_kichban_noi.py      → ⑦ kichban_noi.json · 16 kịch bản · 153 bước
   │  tools/kichban_tay_ta1.py          (ba bài viết tay: U6 · U9 · U16)
   ↓
tools/tts/sinh_am.py                → ⑧ audio/*.mp3 · lop1_am.json
        553 clip · 8.8 MB · hai model Kokoro
   ↓     tools/video/kich_ban.py + dung_video.py
web/public/content/tienganh/video/  → ⑨ 37 mp4 · 28.4 MB

web/src/mon/tienganh/lib/hinh_ve.json  ⑩ 11 HÌNH VẼ TAY — dùng chung
        màn hình đọc trực tiếp · video rasterize bằng cairosvg
```

**Luật xuyên suốt:** mỗi tầng chỉ đọc tầng trên nó. Không tầng nào ghi ngược lên. Sửa
tay ở tầng dưới là mất trắng ở lần dựng sau — đã dính thật, xem §3.

---

## 1 · Chạy lại toàn bộ

```bash
python3 tools/chuan_tienganh.py --lop 1
python3 tools/sinh_bai_tienganh.py --lop 1 --tat-ca
python3 tools/sinh_ontap_tienganh.py
python3 tools/sinh_kichban_noi.py
python3 tools/kichban_tay_ta1.py                 # ba kịch bản viết tay
# sinh clip cho những dòng lop1_loi.json khai mà audio/ chưa có:
tools/tts/.venv/bin/python tools/tts/sinh_am.py --vao <thiếu.json> --ra <ra> --so <sổ>
tools/tts/.venv/bin/python tools/video/dung_video.py --tat-ca
python3 tools/soat_hinh_tienganh.py --lech       # từ nào chưa ai nhìn hình
cd web && npm test
```

⚠ **Sai thứ tự là mất dữ liệu.** `sinh_bai` ghi đè 16 bài; `sinh_ontap` và
`sinh_kichban_noi` đọc từ 16 bài ấy. Chạy `sinh_ontap` trước là dựng đề từ bài cũ —
xem §3, lỗi đã lọt thật.

---

## 2 · Từng loại dữ liệu: là gì · dựng thế nào · luật gì · dùng vào việc gì

### ① Bản đồ gốc — `data/ban_do_tieng_anh.json`

| | |
|---|---|
| **là gì** | Đồ thị tri thức cả 12 lớp bác cấp. 3 989 node, 7 602 cạnh. |
| **dựng** | Không dựng. Nguyên liệu bên ngoài. |
| **dùng** | Nguồn DUY NHẤT của: unit · từ vựng · mẫu câu · phonics · thứ tự học. |

Node dùng tới ở lớp 1: `unit` · `vocabulary` · `sentence_pattern` · `letter_sound`.
Cạnh dùng tới: `HAS_UNIT` · `HAS_VOCABULARY` · `HAS_SLOT` (ô trống của mẫu câu) ·
`REQUIRES` (mối tiên quyết) · `CONTAINS`.

**LUẬT SỐ MỘT: KHÔNG BAO GIỜ SỬA TỆP NÀY.** Thiếu gì thì đắp ở ②. Sửa vào đây là lần
sau bác cấp bản mới thì mọi sửa đổi biến mất, không ai biết đã mất gì.

⚠ **Ba lớp KHÔNG cùng khuôn**, dù nằm chung một tệp — đây là phát hiện đắt nhất của cả
đợt, và là lý do phải có tầng ③:

| trường | lớp 1 | lớp 2 | lớp 3 |
|---|---|---|---|
| số hiệu unit | `unit_no` | `unit_number` | `unit_number` |
| unit → từ | mảng `vocabulary` | **không có**, chỉ cạnh | **không có**, chỉ cạnh |
| từ → phonics | `target_phonics` | `phonics_focus` | *(không có)* |
| nghĩa Việt | **0/60** | 56/56 | 185/204 |
| IPA | **0/60** | 56/56 | 184/204 |

Viết bộ sinh bài thẳng trên khuôn lớp 1 thì tới lớp 2 là vỡ — vỡ vào lúc đã có 16 bài
chạy thật, tức lúc đắt nhất để sửa.

> **Cho lớp 2:** đọc lại bảng này TRƯỚC khi viết dòng nào. Lớp 2 có sẵn nghĩa và IPA
> nên phần bù nhẹ hơn nhiều, nhưng unit→từ phải đi qua cạnh chứ không có mảng sẵn.

---

### ② Phần bù soạn tay — `data/tienganh/lop1_bu.json`

| | |
|---|---|
| **là gì** | Mọi thứ bản đồ thiếu mà bài học cần. 46 KB, soạn tay. |
| **dựng** | Người viết. Không sinh được — đây là chỗ cần người. |
| **dùng** | `chuan_tienganh.py` đắp lên bản đồ khi dựng ③. |

Gồm bảy nhóm:

| khoá | nội dung | vì sao cần |
|---|---|---|
| `tu` | nghĩa Việt · IPA · **vai** (dt/đt/màu/số) · `so_nhieu` · `dang_ing` · `go_duoc` | bản đồ lớp 1 không có nghĩa lẫn IPA |
| `hinh` | 60 emoji + `_ve_tay` khai 11 từ cần hình vẽ | bé chưa đọc chữ — hình là nghĩa |
| `mau_cau` | tình huống dùng · phân tích từng phần câu | bản đồ chỉ có công thức trần |
| `sua_slot` | **ô nào nhận gì** khi công thức nhiều ô | không khai thì thay bừa ra `"It's a pen bell."` |
| `them` | số đếm · màu · tên người | ba nhóm mẫu câu ĐÒI mà bản đồ không có node nào |
| `kich_ban_noi` | hội thoại mẫu từng unit | phần luyện nói |
| `chuong` | gộp 16 unit thành 4 chương | bản đồ không chia chương |

**LUẬT `vai`** — đây là trục xoay của cả bộ sinh câu. Mỗi từ khai vai (`dt` danh từ ·
`dongtu` động từ · `mau` màu · `so` số · `sonhieu` số nhiều · `ten` tên riêng). `sua_slot`
khai mỗi ô nhận vai nào. Thiếu một trong hai là câu sai ngữ pháp, và không cổng nào bắt
được vì câu vẫn "hợp lệ" về mặt chuỗi.

**LUẬT `them` — TỪ PHỤ KHÔNG PHẢI TỪ VỰNG.** Số đếm và màu ở đây sinh ra để *điền vào
khung cho có câu mà luyện*, không phải để bé học thuộc. Chúng **không được làm đáp án**
của bất kỳ câu hỏi nào. Vi phạm luật này đã đẻ ra câu đáp án là `blue` — một từ cả quyển
không bài nào dạy. Tên người thì KHÁC: `Hi, I'm + [Name].` có ô tên là chính chỗ bài
đang dạy, nên tên được làm đáp án.

---

### ③ Bản chuẩn — `data/tienganh/chuan_lop1.json`

| | |
|---|---|
| **là gì** | Một hình dạng duy nhất, mọi lớp giống nhau. 16 unit · 60 từ · 19 mẫu câu. |
| **dựng** | `tools/chuan_tienganh.py --lop N` — bản đồ ① + phần bù ② |
| **dùng** | Đầu vào DUY NHẤT của bộ sinh bài ④. |

Hình dạng:

```
{ lop, cefr,
  unit: [{ ma, so, canh, chu_de, nang_luc, phonics, tu[], mau_cau[] }],
  thang:  [{ can, truoc_khi }]      ← mối tiên quyết, suy từ cạnh REQUIRES
  chuong: { "1": { ten, unit: [1,2,3,4] } },
  them, sua_slot,
  _thieu: []                        ← từ nào còn thiếu nghĩa/IPA/hình
}
```

**LUẬT: `_thieu` phải RỖNG trước khi sinh bài.** Nó là bản kê những chỗ phần bù chưa
đắp kín. Không rỗng mà cứ sinh thì bài ra có ô trống, và không ai thấy cho tới khi bé
mở màn hình.

**⚠ ĐÂY LÀ BẢN DỰNG, KHÔNG PHẢI BẢN GỐC.** Sửa tay vào đây thì lần chạy
`chuan_tienganh.py` sau là mất sạch. Đã dính thật trong đợt soát hình 14-08: cháu sửa
`hinh_ve` cho bốn từ vào thẳng tệp này, cổng `tienganh_lop1_bu` bắt được, phải khai lại
vào ②.

---

### ④ 16 bài học — `web/public/content/ta1/DL_TA1_B*.json`

| | |
|---|---|
| **là gì** | Bài chạy được, đúng khuôn `digital-lesson/v2-micro` — **cùng khuôn bốn quyển Toán**. |
| **dựng** | `tools/sinh_bai_tienganh.py --lop 1 --tat-ca` |
| **dùng** | `LessonPlayer` dựng thẳng, không sửa một dòng nào của phần chung. |

Mỗi bài gồm: `lecture.screens` (hook · explain · trap) · `knowledgeCore` (từ · mẫu câu ·
`canonicalExamples` · `misconceptions` · `hoiThoai`) · `practice.pools` ba bậc ·
`assessment` · `hinhTu` · `video`.

Số thật của lớp 1: **warmup 180 · standard 117 · challenge 92 · sát hạch 80 = 469 câu.**

#### Bốn bậc câu hỏi

| bậc | pool | dạng | manh mối |
|---|---|---|---|
| ★ 1 | warmup | nghe → bấm hình | tiếng |
| ★ 2 | warmup | nghe → chọn nghĩa | tiếng |
| ★★ 3 | standard | xếp thẻ thành câu · điền chỗ trống | **hình** |
| ★★★ 4 | challenge | gõ lại từ · ghép chữ cái | trí nhớ |

#### Bảy luật khi sinh câu — mỗi luật là một lỗi đã xảy ra

1. **Câu chỉ lấy từ bảng thay thế** (`o_thay`, tức cạnh `HAS_SLOT`). Máy không tự ghép
   câu mới — ghép thì sớm muộn ra câu sai ngữ pháp mà không ai soát nổi 16 bài.

2. **Điền vào CÔNG THỨC, không thay chuỗi trong câu ví dụ.** Bản đầu `replace` từ cũ
   bằng từ mới; vỡ ở U15 vì câu mẫu `"Point to your hand."` mà `hand` là từ của U8 —
   phép tìm trả chuỗi rỗng và dán từ mới vào đầu câu: `"facePoint to your hand."`

3. **Mồi nhử lấy từ CÙNG UNIT.** Cả unit cùng chữ cái đầu, nên bé chọn sai là vì chưa
   phân biệt được nguyên âm giữa — đúng cái bài đang dạy. Mồi từ unit khác thì bé đoán
   trúng bằng chữ cái đầu và không học được gì.

4. **KHÔNG dùng random.** Chạy hai lần phải ra hai tệp giống hệt. Có random thì
   `git diff` đầy nhiễu và không ai soát nổi.

5. **Khoét chỗ trống theo DẠNG THẬT đã điền**, không theo từ gốc. `run` điền vào thành
   `running`, `window` thành `windows`, `two` đầu câu thành `Two`. Khoét theo từ gốc ra
   `"She's ___ning."` — chỗ trống cắt vào giữa chữ.

6. **Neo hụt thì bỏ câu.** Từ trọng tâm không nằm trong câu thì không khoét được chỗ
   trống, và đề hiện nguyên câu kèm đáp án của một câu khác.

7. **Không có hình thì đừng bảo "Nhìn hình".** 15 câu từng nói dối bé như thế. Nặng nhất
   là 4 câu U16: đếm cửa sổ trong một bức hình không tồn tại. Nay đổi lời dẫn thành
   `"Chọn từ điền vào chỗ trống"` chứ không vứt câu đi.

⚠ **Bỏ câu hỏng cũng phải có chừng.** Bản chặn đầu tiên của đợt sửa 14-08 xoá sạch bài
luyện của U16 (còn 0 câu) — chữa lỗi bằng cách tạo một lỗ hổng. Nên câu SGK chọn ô
trọng tâm là **ô neo được vào từ CÓ HÌNH**, không lấy cứng ô cuối.

#### Câu đúng/sai: ghép lệch là CỐ Ý

Khuôn sát hạch: Q1·Q3·Q5 ghép **đúng** (đáp án `true`), Q2·Q4 ghép **lệch** có chủ ý
(đáp án `false`, lời giải gọi tên vật đang hiện: *"SAI — đó là dog"*). Ai soát mà không
biết luật này sẽ báo nhầm 32 lỗi — cháu đã báo nhầm đúng như thế trong lần đo đầu.

---

### ⑤ Sổ lời cần đọc — `data/tienganh/lop1_loi.json`

| | |
|---|---|
| **là gì** | 357 dòng chữ cần có clip tiếng, kèm thứ tiếng. |
| **dựng** | `sinh_bai_tienganh.py` gom trong lúc dựng bài (`loi_can_doc`). |
| **dùng** | Đầu vào của `sinh_am.py`. |

**LUẬT: MỖI DÒNG MỘT THỨ TIẾNG.** Đọc từ `doanAm` chứ không từ `narration` —
`narration` là chữ hiện lên màn hình và được phép lẫn tiếng Anh, `doanAm` mới là thứ
đem đi đọc. Lẫn hai thứ là ra clip đọc `"In the bedroom"` bằng giọng Việt.

⚠ **Phải gom CẢ lời dẫn của câu hỏi.** Bản cũ không gom, nên thêm một lời dẫn mới là nó
lặng lẽ không có clip — bé bấm vào câu, không nghe thấy gì, mà bé sáu tuổi chưa đọc được
chữ thì đứng luôn. Đã suýt dính khi tách `"Chọn từ điền vào chỗ trống."` ra khỏi
`"Nhìn hình rồi chọn từ điền vào chỗ trống."`

---

### ⑥ Đề ôn tập chương — `web/public/content/ta1/ontap.json`

| | |
|---|---|
| **là gì** | 4 kỳ × 10 câu, mỗi kỳ chốt một chương (4 unit). |
| **dựng** | `tools/sinh_ontap_tienganh.py` — lấy câu ĐÃ SINH của 4 unit trong chương. |
| **dùng** | Màn kỳ ôn tập; qua được thì ghi huy hiệu chương vào học bạ. |

**LUẬT: KHÔNG sinh câu mới.** Kỳ ôn tập theo đúng nghĩa của nó hỏi lại đúng những thứ
bốn unit vừa dạy — âm có sẵn, hình có sẵn. Sinh câu mới là phải chạy lại cả dây chuyền
TTS.

**LUẬT: chỉ hai dạng, cả hai KHÔNG BẮT ĐỌC** — nghe→bấm hình, và nghe→nhìn hình→đúng/sai.

⚠ **Tệp này KHÔNG tự dựng lại khi bài đổi.** Đã lọt thật: sửa xong bốn hình, chạy lại
bộ sinh bài, mở app thấy đúng — mà đề ôn tập vẫn giữ ⚽ cho `ball` và 🪑 cho `desk`. Bé
học "cái bàn" rồi đi thi lại gặp cái ghế: **tệ hơn cả lúc chưa sửa**, vì hai chỗ trong
cùng một quyển dạy hai nghĩa khác nhau. Nay có cổng canh (§4, phép 7).

---

### ⑦ Kịch bản phòng luyện nói — `ta1/kichban_noi.json`

| | |
|---|---|
| **là gì** | 16 kịch bản · 153 bước. Mỗi bước: câu tiếng Anh + chỗ khó bằng tiếng Việt. |
| **dựng** | `tools/sinh_kichban_noi.py` · ba bài viết tay: `tools/kichban_tay_ta1.py` |
| **dùng** | Phòng luyện nói — câu tiếng Anh lấy thẳng từ đây, mô hình chỉ viết lời Việt. |

**Vì sao có:** dặn dò là thứ mô hình *có thể* theo; kịch bản viết sẵn là thứ nó *không
cần* theo. Rút đúng cái quyền hay hỏng ra khỏi tay nó. Mô hình đã hai lần không theo lời
dặn dù dặn rất rõ: sinh `"Bye, bike."` (nhét đồ vật vào ô tên người) và nói y một câu
hai lượt liền ngay sau khi được dặn "đừng lặp".

**LUẬT: không bịa câu.** Mọi câu tiếng Anh phải là câu **sẵn có của sách** —
`mauCauDs` hoặc `canonicalExamples`, **đã lọc theo từ**. U6 có `"It's a blue pen."` mà
cả 16 bài không dạy `blue`, nên câu ấy bị loại. Số đếm là ngoại lệ có khai: không bài
nào dạy số, nhưng hai bài có ô `[Number]` — sách coi số là vốn nền bé có sẵn từ giờ Toán.

**LUẬT: ba bài viết tay** (U6 · U9 · U16) vì công thức HAI ô trống, máy không đoán được
ô nào nhận màu ô nào nhận danh từ. Đặt cờ `tay: true` để lần sinh sau không đè lên.

---

### ⑧ Clip tiếng — `content/tienganh/audio/*.mp3` + `lop1_am.json`

| | |
|---|---|
| **là gì** | 553 clip · 8.8 MB. Sổ tra `lop1_am.json` khớp id → tệp + vân tay. |
| **dựng** | `tools/tts/sinh_am.py` — hai model Kokoro, Apache-2.0, cùng 24 kHz. |
| **dùng** | Mọi chỗ có tiếng: bài học · câu hỏi · ôn tập · video. |

| | model | giọng |
|---|---|---|
| tiếng Anh | `hexgrad/Kokoro-82M` `lang_code='b'` | `bf_emma` (en-GB) |
| tiếng Việt | `iamdinhthuan/Kokoro-Vietnamese` | `diem_trinh` |

**LUẬT: `en-GB` xuyên suốt** — giọng mẫu, bộ chấm nói (`TIENG = 'en-GB'`), và Web Speech
trong phòng luyện nói. Để `en-US` thì bé nghe mẫu Anh ở bài rồi giọng Mỹ ở phòng nói, mà
hai chuẩn khác nhau ở đúng những âm lớp 1 đang học.

**LUẬT: `van_tay` trong sổ tra.** Sửa chữ thì vân tay đổi → phải sinh lại clip ấy. Không
có vân tay thì chữ đổi mà clip cũ vẫn nằm đó, bé nghe một đằng đọc một nẻo.

Môi trường **tách hẳn** (`tools/tts/.venv`, ~1 GB, không commit) khỏi Python hệ thống mà
`figforge/` và `tools/*.py` đang dùng. Cài đè là bốn quyển Toán mất đường dựng lại hình.

---

### ⑨ Video — `content/tienganh/video/*.mp4`

| | |
|---|---|
| **là gì** | 37 tệp · 28.4 MB. Mỗi bài: 1 video từ mới + 1–2 video mẫu câu. |
| **dựng** | `tools/video/kich_ban.py` (dựng cảnh) → `dung_video.py` (Pillow + ffmpeg) |
| **dùng** | Dẫn đường đầu mỗi chặng — chữ trên màn từ 2 029 xuống 310 ký tự. |

**LUẬT: video đọc CÙNG nguồn hình với màn hình.** `hinhTu` của bài, và hình vẽ tay thì
rasterize từ chính `lib/hinh_ve.json` bằng cairosvg. Vẽ lại một bản riêng cho video là
thành hai bản của cùng một vật, và hai bản thì sớm muộn lệch — sửa cái cổng trên màn
hình mà quên cái cổng trong video, không cổng nào bắt được, chỉ có bé là thấy hai cái
cổng khác nhau.

⚠ **Video là tệp đã render.** Đổi hình hoặc đổi chữ thì phải dựng lại đúng những bài ấy
— `--bai DL_TA1_B04`. Không có gì tự nhắc.

---

### ⑩ Hình vẽ tay — `web/src/mon/tienganh/lib/hinh_ve.json`

| | |
|---|---|
| **là gì** | 46 hình SVG, khung nhìn `0 0 64 64`, nét dày, màu phẳng. Hình nào vẽ MỘT NGƯỜI đang làm việc gì đó thì mang cờ `nguoi: true` — bài tả tranh đọc cờ ấy để biết hoạt động nào vẽ ra tranh được (xem `docs/lam_bai_tranh.md` luật 7). |
| **dựng** | Viết tay. Render ra PNG **nhìn tận mắt** trước khi chốt. |
| **dùng** | Màn hình đọc trực tiếp; video rasterize bằng cairosvg. Một tệp, hai bên. |

**LUẬT: SVG THUẦN, không lẫn cú pháp JSX.** `{...net}` hay `fill={M.go}` thì trình duyệt
vẽ được (React tự dịch) nhưng cairosvg thì không — video ra ô trống mà không báo lỗi gì.

**Khi nào cần vẽ tay:** khi Unicode không có emoji đúng. 49/60 từ dùng emoji; 11 từ còn
lại emoji chỉ *gần* đúng hoặc *sai hẳn*:

| sai hẳn (sửa 14-08) | gần đúng (từ trước) |
|---|---|
| `desk` 🪑 CHAIR — cái ghế | `gate` 🚧 biển công trường |
| `mops` 🧹 BROOM — cái chổi | `head` 👤 bóng người |
| `ball` ⚽ — trùng hệt `football` | `hair` 💇 đang cắt tóc |
| `garden` 🌷 — một bông hoa lẻ | `top` 🪀 yo-yo · `lake` 🏞️ · `run` · `wash` |

---

## 3 · Năm cái bẫy đã sập thật

**1 · Sửa bản dựng thay vì bản gốc.** `chuan_lop1.json` do máy sinh; sửa tay vào đó là
mất ở lần chạy sau. Nguồn thật là `lop1_bu.json`.

**2 · Tệp sinh ra không tự dựng lại.** `ontap.json` giữ hình cũ sau khi bài đã đổi. Bất
kỳ tệp nào đọc từ 16 bài đều phải chạy lại SAU `sinh_bai`.

**3 · Cổng đếm được nhưng không hiểu nghĩa.** Mọi cổng cũ hỏi "có hình không", không
cổng nào hỏi "hình này vẽ cái gì". Bốn hình sai và 18 câu hỏng nằm đó từ đầu mà cổng vẫn
xanh. Cách chữa: đọc **tên Unicode chính thức** của emoji đặt cạnh nghĩa — `🪑` tên là
`CHAIR`, đọc ra là thấy. Phần máy không làm được thì chốt bằng bảng người soát
(`docs/hinh_da_soat.md`).

**4 · Glob rỗng báo "0 lỗi".** Chạy nhầm thư mục thì mọi vòng lặp chạy 0 lần và phép đếm
xanh trơn. Mọi cổng quét tệp phải **chốt số tệp tìm thấy** trước khi soi.

**5 · Cổng ghim cứng con số.** `assert COI.length === 7` thì mỗi lần thêm một hình là đỏ
vì lý do KHÔNG PHẢI lỗi — và người sửa dễ nới bừa con số cho xanh, tức là cổng mất hẳn ý
nghĩa. Nên so **hai chiều** với thứ đang dùng thật, đừng đếm.

---

## 4 · Cổng canh — chạy được bằng `node`, không cần mạng

| tệp | canh gì |
|---|---|
| `tienganh_lop1_bu` | phần bù đắp kín · 60 từ có nghĩa/IPA/hình · không hình vẽ nào thừa |
| `tienganh_bai` | 16 bài đúng khuôn · mã câu không trùng · mối tiên quyết khép kín |
| `tienganh_am` | mọi `am` đều có clip · mỗi dòng một thứ tiếng |
| `tienganh_hinh_ve` | SVG thuần · khoá `ve` khớp hai chiều với bài |
| **`tienganh_hinh_dung_tu`** | **8 phép — xem dưới** |
| `tienganh_ontap` | 4 kỳ có câu thật · màn hình gọi tới chỗ ghi học bạ |
| `tienganh_phongnoi` | vốn từ · kịch bản · lời Việt · xưng hô (98 phép) |

`tienganh_hinh_dung_tu.test.mjs` là cổng dựng ra sau đợt bác bắt:

1. mỗi từ mới đều CÓ hình
2. hai từ khác nhau KHÔNG dùng chung một hình
3. câu bảo "nhìn hình" thì phải CÓ hình
4. câu bảo "điền chỗ trống" thì phải CÓ `___`
5. đáp án phải là từ bé ĐÃ ĐƯỢC DẠY (chấp dạng biến đổi: `run`→`running`)
6. câu đúng/sai: đúng thì hình khớp, sai thì hình lệch, lời giải gọi đúng tên vật
7. **đề ôn tập dùng đúng hình của bài**
8. **MỌI từ phải có tên trong `docs/hinh_da_soat.md`** — bảng người đã nhìn tận mắt

Phép 8 quan trọng nhất: máy không nhìn được tranh, nên phải có chỗ ghi lại *ai đã nhìn
cái gì*. Thêm từ mới mà quên nhìn hình là đỏ ngay.

---

## 5 · Làm lớp 2: đi theo thứ tự này

1. **Đọc §0 bảng khuôn lệch.** Lớp 2 có sẵn nghĩa + IPA (56/56) nên phần bù nhẹ hơn
   nhiều — nhưng `unit → từ` phải đi qua **cạnh**, không có mảng sẵn như lớp 1.
2. **Soạn `lop2_bu.json`** — chủ yếu là `vai` · `hinh` · `sua_slot` · `them`. Đây là
   phần tốn người nhất, và không rút ngắn được.
3. `chuan_tienganh.py --lop 2` → **đòi `_thieu` rỗng** rồi mới đi tiếp.
4. `sinh_bai_tienganh.py --lop 2 --tat-ca` — bộ sinh **không phải sửa** nếu ③ đúng khuôn.
   Nếu phải sửa, sửa ở `chuan_tienganh.py` chứ đừng thêm nhánh `if lop == 2` vào bộ sinh.
5. `soat_hinh_tienganh.py --lech` → **nhìn từng hình**, ghi vào `hinh_da_soat.md`.
6. Ôn tập → kịch bản nói → âm → video, đúng thứ tự §1.
7. `npm test`, rồi **mở app nhìn tận mắt**. Cổng xanh không chứng minh được gì: bốn hình
   sai của lớp 1 đi qua mọi cổng suốt hai ngày.

**Việc chưa làm, để lại cho lớp 2 cân nhắc:** 5 từ số nhiều mà hình vẽ một vật (riêng U9
dạy đếm) · 4 hình "gần đúng" (`cup` ☕ · `bag` 👜 · `hat` 🎩 · `mother`/`father`) · và
chuyện emoji mặt (🐱🐴) lẫn với emoji cả con (🐕🦆). Cả ba đều ghi ở `docs/hinh_da_soat.md`.

---

## 6 · LỚP 3 — quyển đầu tiên khuôn cũ KHÔNG chịu nổi

Ghi 18-08-2026, sau khi dựng xong nền lớp 3.

| | lớp 1 | lớp 2 | **lớp 3** |
|---|---|---|---|
| Unit | 16 | 16 | **21** |
| Từ | 60 | 56 | **204** |
| Từ / unit | 3,8 | 3,5 | **9,7** (nhiều nhất 15) |
| Mẫu câu | 19 | 18 | **43** |

### Năm khác biệt về CHẤT

**1 · 39/204 từ KHÔNG vẽ được.** `hello · fine · my · this · yes · please · many ·
here`… Cả hai quyển trước dựng trên một câu: *"bé chưa đọc được chữ nên HÌNH CHÍNH
LÀ NGHĨA"*. Câu ấy đúng khi quyển chỉ dạy vật cụ thể; lớp 3 thì gãy, và gãy đúng các
unit mở đầu (U1 có 9/13 từ trừu tượng).

→ Khai `hinh._khong_ve` **kèm lý do**. `chuan_tienganh.py` không tính là thiếu và gắn
cờ `khong_ve`. **Đừng cố tìm emoji** — đó chính là cách đẻ ra `desk` → 🪑 (tên Unicode
thật: CHAIR) của lớp 1.

**2 · 26/42 công thức có dấu `/`** — bản đồ để người soạn tự chọn. Ba cách xử:

| loại | xử |
|---|---|
| `a/an` | MÁY chọn (`_chon_mao_tu`): chữ sau bắt đầu bằng nguyên âm thì `an` |
| `/` ở ĐẦU câu (`Hello / Hi` · `he / she` · `Touch / Open`) | NGƯỜI chọn — đè `cong_thuc` VÀ `vi_du` ở phần bù |
| `/` ở lời ĐÁP (`Yes, I do. / No, I don't.`) | GIỮ — cặp đáp mẫu hợp lệ |

**3 · 9,7 từ/unit.** Giữ khuôn video cũ (~8 giây một từ) thì video từ mới dài **73
giây**, unit nặng nhất **112** — lớp 1·2 chỉ 30. **Phải tách video theo NHÓM NGHĨA**,
mỗi nhóm một tệp ~30 giây, và từ trừu tượng cần một loại cảnh khác (dạy bằng CÂU,
không dạy bằng tranh).

**4 · 8 từ dạy lại ở nhiều unit · 24 mục là CỤM nhiều chữ.** Lớp 1·2 mỗi từ chỉ thuộc
một unit — bộ sinh mồi nhử dựa vào giả định ấy.

**5 · U0 "Starter" số hiệu là CHỮ và không có mẫu câu nào.**

### Bốn lỗi câm của bộ sinh, chỉ lộ khi có quyển thứ BA

- **`VAI_BIET` ghim cứng** 13 vai của lớp 1·2. Lớp 3 khai thêm 13 vai mới → `sua_slot`
  bị hiểu nhầm là danh sách TỪ, kho rỗng, bỏ qua cả mẫu, im lặng. Nay **suy từ chính
  dữ liệu** (`vai_biet()`).
- **`str.capitalize()` hạ chữ hoa phía sau**: `"Ms Hoa"` → `"Ms hoa"`.
- **`a/an` không ai giải** → `"I can see a/an elephant."`
- **`cau_hoi` bỏ từ KHÔNG có nghĩa tiếng Việt**, mà tên riêng thì không cần dịch →
  U1 mất sạch ứng viên cho ô `[Name]`, mất luôn bậc 3. Cho tên một nghĩa ngắn
  ("bạn Ben") là chữa được và cũng đúng hơn.

### Một cửa mới ở tầng chuẩn hoá

Phần bù nay **THÊM được mẫu câu**, không chỉ đắp phần dạy: khai `_unit` trong
`mau_cau`. Dùng cho Starter — sách không khai mẫu nào nên bài mất bậc 3.
⚠ Dùng dè: mỗi mẫu thêm là một câu KHÔNG có trong sách, phải nằm trọn trong năng lực
unit đã khai và ghi rõ lý do ở `_them_moi`.

### Còn lại cho lớp 3 — ĐÃ LÀM XONG 18-08, xem §7

---

## 7 · BA TẦNG MỚI (18-08-2026) — video nhóm nghĩa · đọc hiểu · bài viết

Dây chuyền nay **13 tầng**. Ba tầng thêm đều đọc từ ④ (16/21 bài đã sinh), nên
**phải chạy SAU `sinh_bai`** — cùng luật với `ontap.json` ở §3 bẫy 2.

```
④ bài học ─┬─ tools/sinh_dochieu_tienganh.py  → ⑪ ta3/dochieu.json   5 bài · 30 dòng
           ├─ tools/sinh_vietbai_tienganh.py  → ⑫ ta3/vietbai.json   5 đề
           └─ (video.tu là DANH SÁCH nhóm)    → ⑬ 43 video từ mới thay vì 21
```

### ⑪ Bài đọc hiểu — `sinh_dochieu_tienganh.py`

Đoạn 4–6 câu, mỗi dòng là một câu **SẴN CÓ** của chính bốn bài trong chương, cắt đôi
ở cặp hỏi–đáp. Không bịa câu tiếng Anh — luật xuyên suốt cả môn.

Bốn câu hỏi: 1 ý chính (đáp án là TÊN CHƯƠNG, mồi là tên chương khác) · 2 chi tiết
"câu nào CÓ trong bài" (mồi CÙNG KHUÔN khác từ) · 1 có/không.

⚠ Câu "câu nào CÓ trong bài" **không được có nút nghe** — `am` của nó là clip đáp án.

### ⑫ Đề bài viết — `sinh_vietbai_tienganh.py`

Đề bằng TIẾNG VIỆT (viết tiếng Anh, đọc đề tiếng Việt — một việc một lúc), kèm mẫu
câu của chương và **vốn từ DỒN** từ chương 1 tới đó. `vonTu` đi thẳng vào lời dặn
máy chấm và vào phép soi chữ lạ, nên nó không phải chỗ trang trí.

### ⑬ Video từ mới, mỗi NHÓM NGHĨA một tệp

`video.tu` của bài nay là DANH SÁCH `{ma, ten, tu[], tep}`; `kich_ban.py` đọc thẳng
danh sách ấy chứ KHÔNG chia lại. Hai chỗ cùng chia một thứ thì sớm muộn lệch, mà
lệch ở đây nghĩa là app hỏi một tệp không tồn tại.

⚠ **Chia theo GIÂY, không theo số từ** (`GIAY_TU_CO_HINH` = 4 · `GIAY_TU_KHONG_HINH`
= 7). Từ không vẽ được thì dạy bằng CÂU nên tốn gần gấp đôi; đếm đầu từ thì nhóm
*Lời chào* của U1 ra 56 giây trong khi phép đếm bảo nó bằng 6 từ thường.

### Cổng mới

| tệp | canh gì |
|---|---|
| `tienganh_video` | bài khai tệp nào thì có tệp ấy · không mp4 mồ côi · nhóm khớp hai chiều với `vocabulary` · độ dài 12–50s (từ mới) |
| `tienganh_dochieu` | mọi chữ trong đoạn ĐÃ HỌC tới chương ấy · đáp án có thật trong đoạn, mồi thì không |
| `tienganh_chamviet` | chốt cửa máy chủ · lời dặn đòi đủ bốn điều bác chốt · soi chữ lạ hai chiều · điểm đeo nhãn "máy chấm" |

---

## §8 · BÀI TẢ TRANH — tầng thứ 14 (19-08-2026)

Bác chốt: một BỨC TRANH làm nền cho cả ba màn — đọc · viết · nói. Toàn bộ quy trình,
sáu luật dựng tranh, và những chỗ đã dính nằm ở **`docs/lam_bai_tranh.md`**; đọc tệp
ấy TRƯỚC khi làm bài tranh cho một quyển mới.

Bốn tệp mới trong dây chuyền:

| Tệp | Việc |
|---|---|
| `data/tienganh/tranh_lopN.json` | bản khai từng bức: vật · đoạn mô tả · câu hỏi |
| `tools/soan_tranh_lop3.py` | soạn bản khai từ chính vốn của unit |
| `tools/tranh_tienganh.py` | vẽ PNG, ghép từ bộ hình màn hình và video đang dùng |
| `tools/sinh_bai_tranh.py` | sinh ba màn quanh bức tranh |

⚠ **Thứ tự**: `sinh_bai_tranh.py` chạy SAU `sinh_dochieu` và `sinh_vietbai` — nó
CHÈN ĐÈ mục của unit có tranh. Chạy trước thì bị ghi đè lại, im lặng.
