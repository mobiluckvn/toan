# TIẾNG ANH LỚP 1 — điểm dừng và việc tiếp theo

Ghi 12-08-2026. Đọc tệp này TRƯỚC khi làm tiếp môn Tiếng Anh.

Quyển đầu tiên của môn thứ hai đã **chạy được thật**: bé đăng nhập, học trọn một
bài, tiến độ lên máy chủ, xoá sổ tại máy rồi tải lại vẫn còn. Chưa deploy.

> ✅ **ĐÃ ĐI THỬ END-TO-END 13-08-2026.** Trọn 11 mục của bảng 2(i), trên bộ giả
> lập, tài khoản lập mới. **9 mục đạt · 2 mục hỏng** — cả hai đều là loại cổng
> xanh mà vẫn sai. Xem mục 0 ngay dưới.

---

## 0 · ĐI THỬ 13-08-2026 — hai chỗ hỏng

### (A) ✗ Học bạ Tiếng Anh KHÔNG ghi được lên máy chủ — ba chỗ khai ba kiểu

Bé làm trọn kỳ ôn tập, được 10/10, huy hiệu hiện lên, sổ tại máy ghi đủ. Máy chủ
**trống**. Console nói thẳng: `[tienganh] máy chủ từ chối ghi: permission-denied`.

Đây **không** phải chuyện "chưa deploy luật" như tệp này vẫn ghi ở mục 2(b). Bộ
giả lập chạy đúng `firestore.rules` của repo, và nó vẫn từ chối. Deploy cũng
không chữa được. Ba chỗ nói về cùng một thứ mà khai ba kiểu:

| chỗ | khai gì |
|---|---|
| `components/ManTiengAnh.jsx:79` — chỗ GHI | `loai: 'ontap'` |
| `firestore.rules:132` — chỗ GÁC | chỉ cho `loai in ['chuong']` → **từ chối** |
| `lib/duLieu.js:116` — chỗ ĐỌC LẠI | chỉ nhận `v.loai === 'chuong'` |

Hai trên ba đồng ý là `'chuong'`; chỉ chỗ ghi lệch. Nên **sửa ở chỗ ghi**, đừng
nới luật: nới luật thì tài liệu vào được máy chủ nhưng `docHocBa` vẫn không đọc
ra — hỏng câm thêm một tầng nữa.

**Vì sao cổng không bắt được:** `test/luat_firestore.test.mjs:111` tự tay dựng
`{ loai: 'chuong' }` rồi thử. Nó thử đúng cái mà app KHÔNG gửi. Phép kiểm luật mà
tự viết lấy payload thì nó chỉ chứng minh luật khớp với chính nó.

**Sửa cho trọn phải hai phần**, không phải đổi một chữ:

1. `ManTiengAnh.jsx:79` — `'ontap'` → `'chuong'`;
2. gửi đúng hình dạng mà `docHocBa` mong: bọc trong `{ giaTri: … }` như bên Toán
   (`ManToan.jsx:61`). Nay Tiếng Anh gửi phẳng `{quyen, chuong, ten, dat, dung,
   tong, can}`, mà `docHocBa` làm `chapters[v.khoa] = v.giaTri || v` — không có
   `giaTri` thì nó lấy NGUYÊN tài liệu. Sổ tại máy giữ `{dat, best, tong, at}`,
   nên `best` thành rỗng; rồi `gopTienDo` so `at` và cho bản máy chủ thắng — mất
   luôn số câu đúng đã có. Tức là chữa nửa vời sẽ đẻ ra lỗi thứ hai.

Nên thêm một phép kiểm đọc `loai` từ CHÍNH chỗ gọi rồi đối chiếu với danh sách
trong `firestore.rules`, chứ đừng chép tay lần nữa.

### (B) ✗ Thoát giữa chặng Luyện tập là mất sạch mức

`ghiChang` (progress.js:81) chỉ ghi **một** con số: chặng. Còn mức trong chặng —
`m`, `xaM`, `i`, `dem`, `no` ở `BaiHoc.jsx:400-406` — nằm nguyên trong `useState`,
không xuống sổ.

Đi thử thật: làm xong 9 câu mức ★, sang mức ★★, thoát ra, vào lại → về đúng chặng
Luyện tập ✔ nhưng **★★ khoá lại, ★ về "câu 1/9 · đúng 0/0"**. Bé phải làm lại cả
mức. Với bé lớp 1 thì bị mẹ gọi đi ăn cơm là mất một buổi học.

Chưa sửa — động vào chỗ lưu, **để bác quyết**. Cùng loại với món nợ "tiến độ HỌC
THỬ chưa đẩy lên máy chủ" bên Toán.

### (C) ✅ Thanh VIỆC CỦA CON — làm xong 13-08

Bác bắt tiếp: *"cần có một thanh trạng thái để các cháu biết đã học gì, chưa học
gì, cần phải học gì"*. Chỗ hỏng không phải cái luật — luật đúng — mà là **app nói
điều kiện đi tiếp bằng CHỮ**: `"Con xem hết video, hoặc bấm 🔈 nghe đủ 3 từ, rồi
đi tiếp nhé."` Bé lớp 1 chưa đọc được dòng ấy. Cả quyển dựng trên nguyên tắc
không bắt bé đọc chữ, mà đúng chỗ chỉ đường lại quay về chữ.

Nay mỗi việc là **một ô có hình**, ở đầu chặng Từ mới:

```
VIỆC CỦA CON     Còn 2 việc nữa.
 🎬    🍗✓    🍟    🐟    🥛
      🔈🎤   🔈🎤  🔈🎤  🔈🎤
```

* ba trạng thái, không phải hai — ô **nhúc nhích ngay lần bấm đầu**; nghe xong
  một từ mà ô vẫn trắng thì công vừa bỏ ra không để lại dấu, và đó đúng là lúc
  bé bỏ cuộc;
* hai chấm nhỏ `🔈`/`🎤` trong ô nói rõ còn thiếu **việc nào** — tách hẳn thành
  hai ô thì bài 4 từ thành 9 ô, màn nhỏ phải cuộn ngang;
* **bấm vào ô là cuộn thẳng tới chỗ phải làm** và nhấp nháy một nhịp. Biết mình
  thiếu gì mà không tới được chỗ ấy thì thanh mới đi nửa đường;
* màu KHÔNG phải thứ duy nhất mang tin: xong thì có ✓, chưa làm thì viền nét đứt.

**Luật đi tiếp đổi** (`lib/dandat.js` · `viecChangTu`), bác chốt 13-08:

```
(xem hết video HOẶC nghe đủ mọi từ)  VÀ  (nói đủ mọi từ HOẶC micro hỏng)
```

Trước đây nghe xong là đi được, nên phần NÓI thành thứ trang trí — bé không bao
giờ mở miệng, mà nói mới là chỗ khó nhất. Nay nói là việc phải làm.

⚠ **Hai chốt của vế "micro hỏng", đừng gỡ:**

1. micro hỏng **chỉ tha việc NÓI**, không tha việc nghe. Tha cả hai là mở toang
   chặng — đã có phép kiểm canh (`micro hỏng mà chưa nghe gì thì VẪN đóng`);
2. **im lặng không được tính là đã nói.** `NutNoi` chỉ báo `coTieng` khi máy nghe
   ra chữ; `no-speech` thì không gọi `onHong`. Lẫn hai thứ này là bé bấm ba cái
   trong im lặng rồi qua chặng. Đã đi thử tay: bấm nói mà không phát ra tiếng →
   *"Cô chưa nghe thấy gì"*, ô 🎤 vẫn xám, nút vẫn khoá. ✔

`NutNoi` nay có `onHong(mã)`: trước kia nó nuốt trọn mọi trục trặc micro vào
trong ô, màn hình cha không có cách nào biết — mà khi NÓI đã khoá đường đi thì
im lặng như thế là bé kẹt vĩnh viễn.

**Đã đi thử tay trên bộ giả lập**, không chỉ cổng: ô đổi màu đúng lúc bấm 🔈 ·
giả máy không micro (`getUserMedia` từ chối) → dòng vàng hiện, ô 🎤 gạch đi, nút
mở đúng khi nghe đủ · bấm ô `milk` trên thanh → cuộn thẳng tới thẻ ấy.

**Một cái bẫy đã dính khi dựng** (thêm vào bảng mục 3): thanh việc tự đọc
`v.ve`/`v.hinh` từ `vocabulary` — hình KHÔNG nằm ở đó mà ở `bai.hinhTu`. Cả bốn
ô vẽ ra dấu **❔** trong khi thẻ từ ngay dưới vẫn đủ 🍗🍟🐟🥛. Cổng xanh, bản dựng
xanh, chỉ mở ra nhìn mới thấy. Nay có `hinhCuaTu()` và **đúng một chỗ** trong tệp
được đụng `bai.hinhTu`, có cổng đếm.

Còn 12 unit nữa dùng cùng khuôn này — thanh tự dựng theo `vocabulary` nên không
phải sửa gì thêm. Chặng **Mẫu câu** vẫn đang nói bằng chữ (*"Còn 1 mẫu câu nữa
con chưa xem"*) — cùng loại lỗi, chưa làm.

### (D) ✅ Luyện từng từ: NÓI thành việc chính — làm xong 13-08

Bác chỉ tiếp: *"video đã dạy âm rồi; tới phần luyện từng từ phải làm nổi bật việc
các con phải học nói, để làm sao con nói được từ đó."*

Lưới bốn thẻ cũ hỏng ba chỗ cùng lúc:

* 🔈 và 🎤 là hai nút tròn **to bằng nhau** → trông như hai việc ngang hàng, trong
  khi video vừa dạy âm xong, tới đây nghe chỉ còn là lấy mẫu;
* bấm 🎤 thì ô chấm điểm bung ra **ở dưới cả lưới**, cách xa thẻ bé vừa bấm — bé
  6 tuổi không nối được hai thứ ấy với nhau;
* muốn nói một từ phải bấm **ba lần**: 🎤 → tìm ô ở dưới → "Bấm rồi nói".

Nay `LuyenTu` đi **một từ một lượt**: hình to, rồi `🔈 Nghe cô đọc`, rồi
`🎤 Đến lượt con` — nút to nhất màn, chấm điểm hiện ngay tại chỗ. Bé không phải
chọn gì. Phần nhìn bao quát đã có thanh VIỆC CỦA CON lo; bấm ô nào trên thanh là
nhảy tới đúng từ ấy, và ô đang đứng có viền đậm + `aria-current`.

**Ngưỡng "đã nói được"** (`lib/dandat.js` · `noiDuoc`), bác chốt 13-08 — lại đúng
một luật ấy, lần thứ tư:

```
ĐÃ NÓI ĐƯỢC KHI: đạt ≥ 6/10  HOẶC  đã THỬ THẬT 2 lần   (THU_TOI_THIEU)

  ⭐ dat   đạt ngưỡng
  ✓  thu   thử thật đủ lần, chưa đạt — vẫn đi tiếp được
  ○  chua
```

Hai chốt đi liền nhau, gỡ một cái là cái kia vô nghĩa: **không đòi phải đạt** (bé
ngọng, bé nói giọng miền, micro rẻ — cả ba có thể không bao giờ chạm ngưỡng), và
**không nhận "có mở miệng là xong"** (bé nhìn 🍟 đọc "chicken" mà được tính thì
dấu ✓ chỉ còn nghĩa là "con có phát ra tiếng"). `lan` chỉ cộng khi máy nghe ra
chữ.

`NutNoi` thêm `noiBat` (dáng to) và `onNghe`; `NutNghe` thêm `chuBen` để nút nghe
đứng một mình giữa màn có chữ — một vòng tròn trống trơn không nói được nó làm
gì, mà bố mẹ ngồi cạnh thì đọc được.

**Đã đi thử tay**, giả giọng bé bằng cách vá `SpeechRecognition.prototype`:
nói đúng → `10/10 ⭐ Con nói được rồi`, thanh hiện ⭐ · nói sai hai lần → `0/10`,
`✓ Con đã thử thật`, thanh cho qua · nói đủ bốn từ + xem hết video → nút mở, dòng
đầu thanh đổi thành *"Con đi tiếp được rồi."*

⚠ Một lần suýt báo nhầm: nhìn ảnh phóng to tưởng ô `chips` (mới `thu`) cũng đội
⭐ như ba ô kia. Hỏi thẳng DOM thì `chips` **không có huy hiệu nào** — đúng luật.
Ảnh nhỏ và mờ không phải bằng chứng; hỏi dữ liệu.

### (E) ✅ Bốn chặng còn lại theo cùng một cách — làm xong 13-08

Bác dặn làm nốt *"mẫu câu, luyện tập, luyện nói, sát hạch theo cách như thế này
cho con dễ học"*. Nay cả năm chặng cùng một ngôn ngữ hình.

**Hai khuôn, dùng chung cho mọi chặng:**

| khuôn | dùng ở đâu | vì sao |
|---|---|---|
| `ThanhViec` — ô có hình | Từ mới · Mẫu câu | 3–5 việc, mỗi việc có hình riêng |
| `ThanhCau` — dãy chấm | Luyện tập · Nói chuyện · Sát hạch | 5–16 câu, ô hình thì tràn màn |

`viecChangTu` và `viecChangCau` sinh ra **cùng một hình dạng ô** (`viecCon` là các
chấm nhỏ), nên `ThanhViec` chỉ vẽ chứ không biết đang ở chặng nào — có cổng so
hai bên, vì hai bên lệch hình dạng thì thanh phải mọc thêm nhánh `if`, và nhánh
ấy là chỗ lỗi câm sẽ nấp.

**Chặng Mẫu câu** — nay giống hệt Từ mới: mỗi mẫu một ô (🎬 xem · 🎤 nói), một
mẫu một lượt, nút nói dùng dáng `noiBat`. **Luật đổi**, bác chốt 13-08:

```
ĐI TIẾP KHI: xem đủ video  VÀ  (nói đủ câu HOẶC micro hỏng)
```

Bản trước chỉ đòi xem hết video, nên `NutNoi` ở đây là thứ trang trí y hệt chuyện
đã xảy ra ở chặng Từ mới. Nói được từng TỪ rời không phải là nói được tiếng Anh —
cả câu mới là chỗ bé phải ghép nhịp. Thay luôn dòng chữ *"Còn 1 mẫu câu nữa con
chưa xem"* bằng thanh ô.

**Luyện tập** — ba ô mức ★/★★/★★★ to (khoá thì 🔒, đã qua thì ✅, đang làm thì
viền đậm), dưới là dãy chấm cho từng câu của mức. Thay thanh mức chữ nhỏ và dòng
*"Câu 4/9 · đúng 2/3"*.

**Sát hạch** — dãy chấm thay dòng *"Câu 1/5"*. Bé sát hạch mà không biết còn mấy
câu thì mỗi câu đều có thể là câu cuối.

**Nói chuyện** — dãy chấm đếm **lượt CỦA BÉ** (lượt của máy bé không phải làm gì).

**Bốn dáng chấm khác nhau về HÌNH, không chỉ về màu:** ● đúng · ◍ để lại sau (có
lõi) · ○ chưa tới (nét đứt) · viền đậm = đang ở đây.

**Đã đi thử tay TRỌN cả năm chặng trên bộ giả lập**, Unit 5, giả giọng bé bằng
`SpeechRecognition.prototype`: Từ mới (4 từ ⭐) → Mẫu câu (**xem xong vẫn khoá,
phải nói mới mở** ✔) → Luyện tập 26 câu ba dạng, chấm đầy dần, cố tình bỏ qua một
câu thì hiện đúng *"Đúng 3/12 · 1 câu để lại sau"* → Nói chuyện → Sát hạch 5/5.

**Một chỗ sửa sau khi nhìn tận mắt:** Unit 5 chỉ có MỘT lượt hội thoại của bé,
nên dãy chấm ra đúng một chấm đơn độc nằm giữa một khung to — chiếm chỗ mà không
nói được gì. Nay `ThanhCau` tự ẩn khi `tong < 2`, và **cả cái khung bọc nó** cũng
phải ẩn theo (khung rỗng vẫn chiếm chỗ) — cổng canh cả hai nơi.

### 9 mục đạt

Khoá unit 2–16 (bấm vào không vào được) · thẻ *Học tiếp* chỉ đúng bài, đổi thành
*"CON ĐANG HỌC DỞ"* khi bỏ dở · nút Tiếp xám tới khi xem hết video **hoặc** nghe
đủ 3 từ, cả hai đường đều mở đúng · **bẫy #12 không tái phát** (clip chạy trọn
`0.31 → 0.70` rồi mới dừng) · giấu tệp mp4 đi thì hiện dòng vàng và nút Tiếp mở
ngay · chặng Mẫu câu đếm đúng `2 → "một" → mở` · quay về chặng 1 thì chặng 2·3
**vẫn mở**, có dòng *"→ Về chỗ con đang học"* · ba nấc sai chạy đúng và **gợi ý
không bao giờ hiện cùng nút bỏ qua**, cuối mức có màn 💪 *"Còn 1 câu con chưa làm
được"* · thẻ kỳ ôn tập khoá khi còn nợ, mở đúng khi đủ 4 bài.

**Chưa chứng minh được:** tiếng có kêu ra loa thật không — cháu đo bằng
`currentTime` nhích đều, không nghe tận tai. Vẫn cần người thử (cùng mục 2(h)).

### Ba lần suýt báo nhầm lỗi

Ghi lại vì cả ba đều là *dấu hiệu trông như lỗi mà không phải*:

1. Tài khoản "mới" hiện sẵn 2/16 unit — hoá ra cùng email thì cùng uid, tiến độ
   hôm trước là **thật**;
2. clip âm `stalled` ở `readyState 0` tưởng hỏng — chỉ là lần tải đầu chưa xong;
   cùng bấy nhiêu byte nạp qua Blob thì phát trọn;
3. `GET /emulator/v1/.../accounts` trả rỗng, tưởng bộ giả lập mất sạch tài khoản
   nên `permission-denied` chỉ là phiên mồ côi. Thật ra endpoint ấy **không nhận
   GET**. Phải dùng `POST .../accounts:query` — và tài khoản vẫn còn đủ. Suýt nữa
   thì bỏ qua lỗi (A).

---

## 1 · ĐANG CÓ GÌ

```
16 unit · 4 chương · 395 câu luyện tập · 80 câu sát hạch
4 kỳ ôn tập chương · 10 câu/kỳ, dựng từ chính câu của bốn unit
552 clip âm (Kokoro Anh-Anh + Kokoro-Vietnamese)
37 video mp4 · 34 phút
60 hình: 53 emoji + 7 vẽ tay SVG — nay hiện được CẢ trong video
49 tệp cổng · 0 FAIL
```

### Đi lần lượt — luật ở `lib/dandat.js`

Bác bắt được lỗ này 12-08: *"con có thể bỏ qua nhiều bài mà không làm ấy"*. Nó
không nằm ở một dòng nào — nó là chỗ KHÔNG CÓ luật nào. Nay một luật dùng cho cả
ba tầng:

```
ĐI TIẾP ĐƯỢC KHI: đã ĐẠT — hoặc đã THỬ THẬT ít nhất 2 lần.

tầng 1  bài trong quyển   khoaBai=true · bài trước đạt (hoặc thử 2 lần) thì mở
tầng 2  chặng trong bài   hai con số: `tai` đang ở đâu · `xa` đã đi xa nhất tới đâu
tầng 3  câu trong mức     sai 1 → thử lại · sai 2 → gợi ý · sai 3 → đáp án + để sau
```

Vế "thử 2 lần" mới là vế quan trọng: khoá cứng theo "phải đạt" thì bé tắc ở unit 7
là tắc vĩnh viễn. Nhưng đi vòng KHÔNG được ghi là đạt — bài ấy đội nhãn *"làm lại
nhé"*, và **kỳ ôn tập chương không mở bằng cửa ấy**: muốn huy hiệu thì phải quay
lại trả nợ.

### Dây chuyền, theo thứ tự chạy

```
data/ban_do_tieng_anh.json          bản đồ gốc — KHÔNG SỬA
  + data/tienganh/lop1_bu.json      phần bù soạn tay (nghĩa · IPA · vai · hình · dạy)
  ↓  tools/chuan_tienganh.py        chuẩn hoá 3 khuôn lớp 1·2·3 về một
data/tienganh/chuan_lop1.json
  ↓  tools/sinh_bai_tienganh.py     sinh 16 bài
web/public/content/ta1/DL_TA1_B*.json
  ↓  tools/video/kich_ban.py        kịch bản cảnh
  ↓  tools/tts/sinh_am.py           sinh clip tiếng (2 model)
  ↓  tools/video/dung_video.py      Pillow + ffmpeg → mp4
web/public/content/tienganh/{audio,video}/
```

**Chạy lại toàn bộ:**

```bash
python3 tools/chuan_tienganh.py --lop 1
python3 tools/sinh_bai_tienganh.py --lop 1 --tat-ca
python3 tools/sinh_ontap_tienganh.py          # 4 kỳ ôn tập, dựng từ câu của bài
# gom lời còn thiếu → sinh âm → nhập vào sổ (xem tools/tts/README.md)
tools/tts/.venv/bin/python tools/video/dung_video.py --tat-ca
cd web && npm test
```

---

## 2 · VIỆC TIẾP THEO, THEO THỨ TỰ CHẶN ĐƯỜNG

### (a) ~~Nối video vào app~~ — XONG 12-08
Sáu chặng gộp còn năm, video dẫn đường. Chữ trên màn từ **2 029 xuống 310 ký tự**;
mọi giải thích lui vào **Góc bố mẹ**, gập sẵn. Sát hạch dựng lại thành nghe–nhìn,
không còn chữ nào phải đọc. Phần NÓI (từ · câu · hội thoại) đã có.

### (b) Deploy luật Firestore — bé chưa dùng thật được
```bash
firebase deploy --only firestore:rules
```
Chưa deploy thì `progressTA` và `hocBaTA` bị `match /{document=**}` chặn, và Firestore
**từ chối trong im lặng**. Luật đã thử trên bộ giả lập (14 phép kiểm, xem
`docs/di_thu_gia_lap.md`) nhưng máy chủ thật vẫn chạy bộ luật cũ.

### (c) Soát lại 19 mẫu câu theo tiêu chuẩn "một video một việc"
Bác đã bắt được hai chỗ gộp mà cháu không thấy: cặp hỏi–đáp của U9 và U16. Còn ngờ:
* **U6** `It's a red pen.` — dạy cùng lúc *nó là* + *màu* + *đồ vật*: ba việc
* **U16 `_dap`** `I can see six.` — dùng khung `I can see` mà U14 mới là bài dạy nó,
  hai bài không nối với nhau

### (d) ~~Bảy hình còn nợ~~ — XONG 12-08
Nét vẽ dọn từ JSX sang **`lib/hinh_ve.json`**, màn hình và video cùng đọc MỘT tệp
ấy (`tools/video/hinh_ve.py` rasterize bằng `cairosvg`). Không vẽ lại bằng Pillow:
vẽ lại là thành hai bản của cùng cái cổng, và hai bản thì sớm muộn cũng lệch — mà
lệch kiểu ấy không cổng nào bắt được. 6 video đã dựng lại.

### (e) ~~Kỳ ôn tập chương~~ — XONG 12-08
`tools/sinh_ontap_tienganh.py` dựng 4 kỳ × 10 câu **từ chính câu của bốn unit**
trong chương — âm và hình đều có sẵn, không phải chạy lại TTS. Màn `OnTap.jsx`
gọi `ghiChuong` + `luuMucHocBa`.

⚠ **Đã hỏng suốt từ 12-08 tới 14-08, và hỏng trong im lặng.** Màn hình gửi
`loai:'ontap'` với các trường trải phẳng; `firestore.rules` chỉ cho `['chuong']` và
`docHocBa` chỉ nhặt `v.giaTri`. Ba hình dạng, không cái nào khớp cái nào. Lệnh ghi
không chờ kết quả nên máy chủ từ chối mà chẳng ai hay: bé thấy huy hiệu (sổ tại
máy), đổi máy là mất sạch, sổ bố mẹ không bao giờ thấy.

Cổng `luat_firestore` không bắt được vì nó **tự dựng gói** `{loai:'chuong'}` mang
đi thử — thử đúng cái luật CHO PHÉP, chứ không phải cái app GỬI ĐI. Nay:
`test/hocba_khop_luat.test.mjs` đọc chính dòng gọi trong `.jsx` rồi đối chiếu với
`firestore.rules` (cả hai môn), và `luat_firestore` ghi xong thì **đọc lại** để soi
đúng trường `giaTri.best` mà thẻ huy hiệu dùng.

### (f) ~~Bảng xếp hạng~~ — XONG 12-08
`docDuLieuChung` nay đọc cả `progressTA` và `hocBaTA`. Phép cộng sao vốn đã không
hỏi môn nào — chỗ hỏng nằm ở chỗ ĐỌC, không ở chỗ tính.

### (g) ~~Phần NÓI có chấm~~ — XONG 12-08
`lib/chamnoi.js` (57 phép kiểm) + `lib/nghenoi.js` (Web Speech). Nói từ · nói câu ·
hội thoại 16 kịch bản. ⚠ Chrome gửi tiếng bé lên máy chủ Google — đổi sang Whisper
thì chỉ sửa `nghenoi.js`.

### (h) Chưa thử được bằng MICRO THẬT
Toàn bộ 57 phép kiểm chấm trên chữ giả lập những gì STT trả về. Đường
micro → Web Speech → bộ chấm chỉ người thật thử mới biết.

### (i) ⚠ ĐỢT ĐI LẦN LƯỢT CHƯA ĐI THỬ — làm trước mọi việc khác

Cổng xanh và bản dựng xanh **không chứng minh được gì** về mấy thứ dưới đây; chúng
là thay đổi về ĐƯỜNG ĐI, mà đường đi thì phải đi mới biết:

| phải thử | dấu hiệu hỏng sẽ trông như thế nào |
|---|---|
| trang chính: unit 2–16 có khoá thật không | hiện 🔒 · bấm không vào · dòng "Chưa tới lượt bài này" |
| thẻ **Học tiếp** chỉ đúng bài | chỉ nhầm bài đã đạt, hoặc mất hẳn khi sổ trắng |
| chặng **Từ mới**: nút Tiếp có xám không | xám tới khi xem hết video **hoặc** bấm 🔈 đủ mọi từ |
| bấm 🔈 xong tiếng có bị TẮT NGAY không | `onPhat` đổi state cha → vẽ lại; đã kẹp bằng `ref`, nhưng phải nghe tận tai |
| video hỏng → nút Tiếp có mở ra không | tắt mạng rồi vào; phải hiện dòng vàng và cho đi tiếp |
| chặng **Mẫu câu**: bài 2 mẫu có đòi xem cả hai không | "Còn 1 mẫu câu nữa con chưa xem" |
| quay lại chặng 1 → chặng sau CÒN mở không | đây là chỗ bản cũ hỏng; phải thấy dòng "→ Về chỗ con đang học" |
| sai 3 lần → "Để câu này lại sau" → cuối mức có mời làm lại không | màn 💪 "Còn N câu con chưa làm được" |
| thẻ kỳ ôn tập: khoá khi còn nợ, mở khi đủ 4 bài | "Còn N bài nữa trong chương này là mở" |
| ~~làm xong kỳ ôn tập → `hocBaTA` có tài liệu chưa~~ | XONG 14-08 — xem (e); vòng khứ hồi có cổng canh, nhưng vẫn nên nhìn tận mắt một lần trên bản thật |
| vào lại bài đang dở có về đúng chặng cũ không | `ghiChang` chỉ ghi tại máy |

Bộ giả lập: xem `docs/di_thu_gia_lap.md`. **Nhớ ba chỗ đọc nhầm dấu hiệu** ghi ở
cuối tệp ấy — `curl 200` không có nghĩa là tệp có thật.

---

## 3 · MƯỜI CÁI BẪY ĐÃ DÍNH THẬT — đừng dẫm lại

Tất cả đều **cổng xanh mà vẫn sai**. Mỗi cái nay có phép kiểm canh.

| # | bẫy | dấu hiệu |
|---|---|---|
| 1 | `position: "initial"` khai cho cả 16 phonics | 20 từ có âm ở GIỮA; vị trí âm là chuyện của TỪNG TỪ, không phải của unit |
| 2 | slot phẳng, không phân vai | `"It's a pen bell."` |
| 3 | thay chuỗi trong câu ví dụ thay vì điền vào công thức | `"facePoint to your hand."` |
| 4 | giao ước `soMon.js` ghi sai kiểu tham số | kệ sách hiện "0 unit" cho quyển 16 bài |
| 5 | `napSoAm` nhớ cả lần hỏng | cả quyển câm, màn hình vẫn đủ chữ |
| 6 | sổ âm nằm ở `data/` mà app đọc `public/` | `curl` trả **200** vì máy chủ dev trả `index.html` thay thế |
| 7 | hai hàm đặt mã clip ở hai ngôn ngữ | lệch một gạch dưới → mọi nút nghe biến mất |
| 8 | `CauHoi` không có `key` | trắng màn hình giữa bài, chỗ nối ★ sang ★★ |
| 9 | lời giải thích "chỗ dễ nhầm" ghim cứng một ví dụ | 10/16 bài câu "sai" trùng hệt câu đúng |
| 10 | gom clip ở một script, kịch bản dùng ở chỗ khác | đổi câu là lệch; nay kịch bản tự khai chữ (`loiAm`) |
| 11 | cổng dò bộ hình bằng cách ĐỌC CHỮ trong `HinhVe.jsx` | dọn nét vẽ sang JSON là cổng kêu "7 từ chưa có hình" trong khi cả bảy vẫn nguyên — chỗ nào đọc được DỮ LIỆU thì đừng dò bằng biểu thức chính quy |
| 12 | đưa `onPhat` vào deps của `useCallback` trong `NutNghe` | mỗi lần vẽ lại là một hàm mới → `useEffect` chạy lại → phần dọn dẹp `pause()` ngay clip đang kêu. Bấm nghe ra một tiếng "tách" rồi im. Giữ trong `ref` |

**Ba lần đọc nhầm dấu hiệu** (ghi ở `docs/di_thu_gia_lap.md`): `curl 200` không có
nghĩa là tệp có thật · đọc Firestore quên token bị từ chối rồi hiện thành "0 tài
liệu" · bộ đếm lỗi bằng 0 có thể là "chưa từng chạy" chứ không phải "chạy trót lọt".

---

## 4 · NHỮNG QUYẾT ĐỊNH ĐÃ CHỐT — đừng mở lại nếu không có lý do mới

* **Kokoro** sinh sẵn tệp; tiếng Việt dùng bản cộng đồng `Kokoro-Vietnamese`
* **Bỏ phần âm phonics rời** — dạy âm qua từ ví dụ
* **Không nhân vật** Trí Long · Su Kem: quyển dựng cho MỌI học sinh
* **Hình = emoji + 7 SVG vẽ tay**; `figforge` chỉ dựng sơ đồ toán, không vẽ được vật
* **Lớp 1 chưa dạy số ít / số nhiều** — để bài khác dạy
* **Mỗi dòng chỉ MỘT thứ tiếng** — hai model, trộn là đọc sai
* **Giọng Anh-Anh** (`bf_emma`), vì bản đồ khai IPA Anh-Anh
* **Bài đã học không xoá được** — bằng chứng học tập, luật Firestore chặn cả chính chủ

---

## Đọc kèm

* `docs/lop1_tieng_anh_khao_sat_va_thiet_ke.md` — khảo sát bản đồ và thiết kế bài
* `docs/di_thu_gia_lap.md` — bật bộ giả lập, thử luật thật
* `tools/tts/README.md` — dây chuyền âm, ba điều dễ vấp
* `docs/tach_hai_mon.md` — kiến trúc ba vùng
* `web/src/mon/tienganh/lib/dandat.js` — luật đi lần lượt, đọc phần đầu tệp là đủ
