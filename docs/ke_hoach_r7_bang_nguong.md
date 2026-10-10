# Kế hoạch R7 — NGƯỠNG LÀ DỮ LIỆU, KHÔNG PHẢI HẰNG SỐ TRONG MÃ · 10-10-2026

Dựng từ **mục 3.8 của `docs/Luan_van_Chuong2_Chuong3_v4.docx`** (Thầy yêu cầu đưa
tham số ra bảng cấu hình để chuyên gia tự chỉnh). Trang này **chỉ là kế hoạch** —
chưa sửa một dòng mã nào.

> Đọc cùng: `docs/tiep_theo_di_thu_ban_that.md` (điểm dừng mã nguồn, 10-10).

---

## 1 · Luận văn đòi gì

Ràng buộc **R7: mọi ngưỡng là dữ liệu, không phải hằng số trong mã**, năm phần:

1. **Danh mục 21 ngưỡng** NG01–NG21 — mặc định, khoảng hợp lệ, **phạm vi áp dụng**,
   cách học từ dữ liệu (Bảng 3.19).
2. **Bốn bảng** `nguong` · `nguong_lich_su` · `nguong_de_xuat` · `thong_ke_nguong`
   (Bảng 3.20), mỗi bảng có luật ghi riêng.
3. **Hàm thuần** `layNguong(bộ, mã, ngữ cảnh)` — chọn giá trị ở phạm vi **hẹp nhất
   có khai báo**, theo thứ tự `nút → dạng câu hỏi → loại nút → khối lớp → toàn hệ thống`.
4. **`nguongVer`** trên mỗi bản ghi lượt, để kết quả cũ luôn tính lại được đúng với
   ngưỡng lúc đó.
5. **Quy trình chuyên gia**: hệ thống học ra ĐỀ XUẤT → người duyệt → phát hành phiên
   bản. Ba phép kiểm trước khi phát hành: khoảng hợp lệ · ràng buộc chéo
   (θ_yếu ≤ θ − 0,20; P(G) < 0,5; P(S) < 0,5) · **nhịp tinh thông** phải nằm trong
   3–6 câu đúng liên tiếp.

---

## 2 · 21 ngưỡng ấy HIỆN nằm ở đâu trong mã

| NG | Ngưỡng | Mặc định | Hiện ở | Kiểu lưu | Phía |
|---|---|---|---|---|---|
| NG01–04 | P(L₀)·P(T)·P(S)·P(G) | 0,10 / 0,08 / 0,10 / 0,30 | `functions/src/bkt.js:13` `DEFAULT_PARAMS` | hằng trong object | máy chủ |
| NG05 | S/G của câu bẫy | 0,06 / 0,15 | `functions/src/bkt.js:43` | ⚠ **object vô danh giữa thân hàm** | máy chủ |
| NG06 | h — bán rã trí nhớ | 14 ngày | `functions/src/bkt.js:56` `NUA_DOI_NGAY` | hằng xuất | máy chủ |
| **NG07** | **θ — ngưỡng tinh thông** | **0,85** | `functions/src/bkt.js:14` **+** `src/mon/tienganh/lib/zpd.js:34` **+** `src/mon/toan/lib/adaptive.js:13` | ⚠ **BA bản** | cả hai |
| NG08 | θ_yếu | 0,30 | `src/mon/tienganh/lib/zpd.js:37` `NGUONG_YEU` | hằng xuất | máy con |
| NG09 | sai liên tiếp để bật phụ đạo | 3 | `src/mon/tienganh/lib/chinhsach.js:42` `SAI_LIEN_TIEP_MAC` | hằng xuất | máy con |
| NG10 | d — độ sâu duyệt ngược | 4 | `src/mon/tienganh/lib/lantruyen.js:52` `sauToiDa = 4` | ⚠ tham số mặc định | máy con |
| NG11 | m — số nút gốc trả về | 3 | `lantruyen.js:52` `toiDa = 3` | ⚠ tham số mặc định | máy con |
| NG12 | α — giảm độ ngờ mỗi bước | 0,6 | `lantruyen.js:26` `ALPHA` | hằng xuất | máy con |
| NG13 | ngày coi là có nguy cơ quên | 14 | `chinhsach.js:149` `ngayCoiLaQuen = 14` | ⚠ tham số mặc định | máy con |
| NG14 | lần thử thật (lưới an toàn) | 2 | `src/mon/tienganh/lib/dandat.js:37` `THU_TOI_THIEU` | hằng xuất | máy con |
| NG15 | nút tối thiểu để bỏ qua cả bài | 3 | `chinhsach.js:126` `toiThieuNut = 3` | ⚠ tham số mặc định | máy con |
| NG16 | H3 — thời gian coi là bế tắc | 45 s | `functions/src/report.js:95` `msThreshold = 45000` | ⚠ tham số mặc định | máy chủ |
| NG17 | H6 — mức chậm dần coi là mệt | 25% / ≥3 lượt | `functions/src/report.js:249` `NGUONG_CHAM` + `:246` `TOI_THIEU_MOI_NUA` | hằng xuất | máy chủ |
| NG18 | H7 — cỡ mẫu tối thiểu cho dạng câu | 8 | `src/mon/tienganh/lib/hoso.js:23` `TOI_THIEU_MAU` | hằng xuất | máy con |
| NG19 | cặp ΔC hợp lệ tối thiểu | 5 | `functions/src/ara.js:22` `TOI_THIEU_CAP` | hằng xuất | máy chủ |
| NG20 | câu hỏi tối thiểu mỗi nút | 4 | **KHÔNG CÓ trong mã** | — | — |
| NG21 | cỡ mẫu tối thiểu để học một ngưỡng | 200 lượt | **KHÔNG CÓ trong mã** | — | — |

**Tổng:** 11 hằng có tên (dễ) · **5 tham số mặc định trong chữ ký hàm** · 1 object vô
danh · 1 nhân ba bản · **2 chưa tồn tại**.

---

## 3 · Năm chỗ khó, khó dần

### a. Ngưỡng nằm ở HAI PHÍA, mà hai phía bị CẤM import chéo

9 ngưỡng ở `web/functions/`, 10 ở `web/src/`. Cổng `ranh_gioi.test.mjs` chặn import
chéo, và chặn đúng: `functions/` lên Cloud Functions với `package.json` riêng, `src/`
đi qua Vite. Nên `nguong.json` phải tới được cả hai bằng **hai đường khác nhau**:

- máy con — `fetch(CONTENT + '/tienganh/nguong.json')`, có sẵn khuôn ở
  `src/mon/tienganh/lib/doThi.js:43` `napDoThi()`;
- máy chủ — đọc Firestore lúc chạy, hoặc gói kèm lúc deploy (xem câu hỏi ③).

> ⚠ **Rủi ro lớn nhất của cả việc này:** hai đường lệch nhau thì BKT chấm bằng θ
> này, màn hình quyết định bằng θ kia, và **không gì báo**. Cùng họ với
> `chula.js` ↔ `chamviet.js` — kho đã phải dựng một cổng so hai bản cho đúng
> chuyện ấy. Lần này cũng phải có cổng so hai phía ngay từ đợt đầu.

### b. θ hiện có BA bản, cổng chỉ canh HAI

`test/tienganh_chinhsach.test.mjs:40` khẳng định `NGUONG_THAO === MASTERY_THRESHOLD`.
Bản thứ ba — `src/mon/toan/lib/adaptive.js:13` của **môn Toán** — không ai canh.
Bảng 3.19 ghi phạm vi "khối lớp, loại nút", **chưa có cột môn** (câu hỏi ②).

### c. Năm ngưỡng là THAM SỐ MẶC ĐỊNH, nên chỗ gọi ghi đè được

`sauToiDa = 4` · `toiDa = 3` · `ngayCoiLaQuen = 14` · `toiThieuNut = 3` ·
`msThreshold = 45000`.

Khác hằng số ở chỗ **chỗ gọi truyền được giá trị khác**, và hiện có chỗ làm thế thật:
`lantruyen.js:123` gọi `nutGocRe(..., { toiDa: 1 })`. Chỉ thay giá trị mặc định bằng
`layNguong(...)` thì mấy chỗ ghi đè ấy vẫn lờ bộ ngưỡng đi — **phải rà từng CHỖ GỌI,
không chỉ từng chỗ khai báo.**

### d. "Phạm vi áp dụng" HIỆN KHÔNG TỒN TẠI ở đâu cả — đây là phần lớn nhất

Hôm nay mọi ngưỡng là **một con số toàn cục**. Bảng 3.19 đòi θ khác nhau giữa khối
1–2 và 3–5, giữa đỉnh từ vựng và đỉnh mẫu câu. Nhưng hàm quyết định **không nhận
ngữ cảnh ấy**:

```js
viecTiepCuaNut({ p, saiLienTiep })     // không biết nút nào, lớp nào, dạng câu gì
```

Muốn có phạm vi thì mọi hàm chính sách phải nhận thêm mã nút + khối lớp + dạng câu,
và mọi chỗ gọi phải chuyền xuống — sửa chữ ký xuyên suốt `chinhsach.js` ·
`lantruyen.js` · `zpd.js` · `dandat.js` và các màn gọi chúng.

**Đề xuất:** tách đôi. Đợt 1 chỉ phạm vi `toàn hệ thống` (giữ nguyên chữ ký, chỉ đổi
NGUỒN của giá trị); đợt sau mới mở phạm vi hẹp. Luận văn vẫn mô tả đủ thiết kế, phần
cài đặt ghi rõ đang ở mức nào — đúng lối chương 3 vẫn ghi "giá trị chọn theo lập luận,
chưa chỉnh theo dữ liệu".

### e. NG20 và NG21 chưa có gì

NG20 (4 câu/nút) — đã soi `test/tienganh_manut.test.mjs`, nó **không** đếm câu theo
nút. NG21 (200 lượt) phục vụ hàm học ngưỡng mà hàm ấy chưa tồn tại. Hai cái này là
**viết mới**, không phải chuyển chỗ.

---

## 4 · Những thứ ĐÃ CÓ, đừng dựng lại

| Cần gì | Đã có sẵn ở đâu |
|---|---|
| Nạp `nguong.json`, chạy được khi mất mạng (R4) | `doThi.js:43` `napDoThi()` — fetch + nhớ + `RONG` khi hỏng |
| `nguongVer` trên bản ghi lượt | `suKien.js` đã mang `phienBanMau` · `vanTayPrompt`; thêm trường thứ ba là cùng một lẽ |
| Luật ghi theo vai trò | `firestore.rules` có khuôn `isTeacher()` / `isAdmin()`; cổng `luat_firestore.test.mjs` đã có |
| Bảng chỉ-thêm-không-sửa | `attempts` đã làm đúng kiểu ấy |
| Chạy lại nhật ký với giá trị khác ("quét lưới", 3.8.3) | mọi thuật toán **đã là hàm thuần** — điều kiện tiên quyết, đã đạt sẵn |
| Tính nhịp tinh thông cho Bảng 3.21 | `functions/src/bkt.js` `applyAttempt` — chạy lại được |

⚠ Thiếu: **vai trò `chuyên gia`**. Rules mới có `student` / `teacher` / `admin`.

---

## 5 · CÁI BẪY với 103 cổng — đọc trước khi viết dòng đầu tiên

Nhiều cổng hiện khẳng định hành vi **dựa trên đúng con số hiện tại**:
`tienganh_phudao_v9` dựa vào `SAI_LIEN_TIEP_MAC = 3`, `tienganh_zpd` dựa vào θ = 0,85.

Khi ngưỡng thành dữ liệu có hai cách, chọn sai là **mất cổng mà vẫn thấy xanh**:

- ❌ **Cổng đọc bộ ngưỡng đang hành.** Chuyên gia đổi θ → cổng vẫn xanh trong khi
  hành vi đã khác. Cổng tự chạy theo cấu hình thì nó không canh gì nữa.
- ✅ **Cổng ghim một bộ cố định** (`nguong.mac_dinh.json`) và khẳng định hành vi theo
  bộ ấy; **thêm cổng riêng canh CƠ CHẾ**: `layNguong` chọn đúng phạm vi · khoảng hợp
  lệ chặn được giá trị ngoài biên · ràng buộc chéo θ_yếu ≤ θ − 0,20 · hai phía đọc
  ra cùng một giá trị.

---

## 6 · Bốn đợt

| Đợt | Việc | Dấu hiệu làm xong |
|---|---|---|
| **1** | Gom 19 ngưỡng đang có thành **một tệp mặc định + `layNguong` thuần**, phạm vi `toàn hệ thống`. Đổi 5 tham số mặc định và 1 object vô danh thành hằng có tên **trước** | **Không đổi hành vi** — 103 cổng xanh y nguyên, không sửa một phép kiểm nào |
| **2** | Hai đường nạp (máy con fetch · máy chủ đọc) + `nguongVer` trên bản ghi lượt + **cổng so hai phía** | Gỡ luôn chuyện θ nhân ba; đổi một giá trị trong tệp là thấy hành vi đổi ở cả hai phía |
| **3** | Bốn bảng Firestore + luật + vai trò chuyên gia + màn hình quản lý ngưỡng kèm bảng **nhịp tinh thông** (Bảng 3.21) | Chuyên gia sửa được θ mà không nhờ người viết mã |
| **4** | Hàm nền học ngưỡng + thống kê (Bảng 3.22) + NG20, NG21 | Có đề xuất kèm cỡ mẫu và chỉ số trước/sau |

**Đợt 1 + 2 là đủ cho R7 trong luận văn** — "tham số tách khỏi mã, chuyên gia sửa
được, kết quả cũ tính lại được". Đợt 3 + 4 là phần vận hành, và đợt 4 cần dữ liệu
thật mà hiện chưa đủ.

---

## 7 · BỐN CÂU ĐÃ CHỐT — 10-10-2026

| | Câu hỏi | Bác chốt | Hệ quả cho mã |
|---|---|---|---|
| ① | Đợt 1 có làm luôn "phạm vi áp dụng"? | **Toàn hệ thống trước** | Đợt 1 KHÔNG đụng chữ ký hàm. `layNguong` nhận `ngữ cảnh` ngay từ đầu nhưng mới dùng nấc `toanHe`; mở nấc hẹp ở đợt sau mà không phải sửa lại chỗ gọi |
| ② | Môn Toán dùng chung bộ ngưỡng? | **Chung, thêm phạm vi `mon`** | `layNguong` phải nằm ở `src/chung/lib/` — `ranh_gioi` luật 1 cấm Toán import của Tiếng Anh, luật 3 cho `mon/**` import `chung/**`. Thang phạm vi thành `nút → dạng câu → loại nút → khối lớp → môn → toàn hệ thống`. Gỡ luôn θ nhân ba |
| ③ | Máy chủ đọc ngưỡng kiểu gì? | **Đọc Firestore, có nhớ tạm** | Chuyên gia sửa là có hiệu lực ngay, không phải deploy — đúng tinh thần R7. Hàm nền giữ bộ ngưỡng trong bộ nhớ, hết hạn thì đọc lại |
| ④ | Vai trò chuyên gia? | **Thêm vai trò thứ tư** | `firestore.rules` thêm `isChuyenGia()`; `admin` không vô tình sửa được ngưỡng |

### Hệ quả về chỗ đặt tệp

Vì ② và vì `functions/` lên Cloud Functions với `package.json` riêng (không import
được `src/`), `layNguong` phải có **HAI BẢN CHÉP**, đúng lối `chula.js` ↔
`chamviet.js` đã dùng:

```
data/nguong.json                  ← bản gốc, 21 mục, người sửa đọc cái này
web/src/chung/lib/nguong.js       ← bản máy con (cả Toán lẫn Tiếng Anh import được)
web/functions/src/nguong.js       ← bản máy chủ
web/test/nguong_hai_ban.test.mjs  ← cổng SO HAI BẢN, bắt buộc
```


---

## 8 · ĐỢT 1 — ĐÃ LÀM XONG · 10-10-2026

**Nguyên tắc của đợt này: không đổi một ly hành vi.** 103 cổng cũ chính là phép kiểm
cho điều đó — không sửa một phép kiểm nào của chúng.

### Bước 1 · Đặt tên cho 6 chỗ chưa có tên

| NG | Trước | Sau |
|---|---|---|
| NG05 | object vô danh giữa `paramsFor()` | `BAY_PARAMS` |
| NG10 | `sauToiDa = 4` trong chữ ký | `SAU_TOI_DA` |
| NG11 | `toiDa = 3` trong chữ ký | `NUT_GOC_TOI_DA` |
| NG13 | `ngayCoiLaQuen = 14` trong chữ ký | `NGAY_COI_LA_QUEN` |
| NG15 | `toiThieuNut = 3` trong chữ ký | `NUT_TOI_THIEU_VUOT_AI` |
| NG16 | `msThreshold = 45000` trong chữ ký | `MS_BE_TAC` |

Giá trị mặc định của chữ ký nay trỏ vào hằng, nên **chỗ gọi ghi đè vẫn ghi đè được**
(`lantruyen.js` gọi `nutGocRe(..., { toiDa: 1 })` — cố ý, giữ nguyên).

### Bước 2 · `data/nguong.json` — bản gốc

21 mục, mỗi mục có `ma · ten · nhom · giaTri · donVi · canDuoi · canTren ·
phamViChoPhep · nguon · canCu · oDau`. Trường **`oDau`** là thứ giữ cho danh mục
không trôi khỏi mã — cổng bắt buộc mọi mục phải khai.

⚠ Hai mục `NG20` · `NG21` ghi `oDau: "CHƯA CÓ TRONG MÃ — đợt 4"`, đúng sự thật.

⚠ Tên năm nhóm là **tạm đặt**: mục 3.8.1 nói 21 ngưỡng "chia thành năm nhóm" mà
Bảng 3.19 không có cột nhóm nào. Cần khớp lại với bản in.

### Bước 3 · `layNguong` — hai bản chép

```
web/src/chung/lib/nguong.js       ← máy con, ở `chung/` để CẢ HAI MÔN import được
web/functions/src/nguong.js       ← máy chủ, thân giống hệt từng ký tự
```

Có: `THANG_PHAM_VI` (`nút → dạng câu → bậc → loại nút → khối lớp → môn → toàn hệ`) ·
`MAC_DINH` · `KHOANG` · `layNguong(bo, ma, nguCanh)` thuần · `soiNguong(bo)` trả
**danh sách** chỗ sai (không ném, để chuyên gia thấy hết một lượt) · `PHIEN_BAN`.

`layNguong` **đã nhận `nguCanh` ngay từ đợt 1** dù mới dùng nấc `toanHe` — mở nấc hẹp
ở đợt sau là thêm DỮ LIỆU, không phải sửa lại chỗ gọi.

### Bước 4 · Nối 19 hằng vào `layNguong`

11 chỗ ở máy con (gồm `mon/toan/lib/adaptive.js` — **θ nay dùng chung, hết nhân ba**),
8 chỗ ở máy chủ. Tên xuất giữ nguyên hết, nên không chỗ gọi nào phải sửa.

⚠ `NG16` trong danh mục đo bằng **giây**, mã đo bằng **mili-giây** — đổi đơn vị ngay
tại chỗ đọc (`MS_BE_TAC = layNguong(...) * 1000`), không để hai đơn vị cùng tên trôi
nổi hai nơi.

### Bước 5 · Cổng `nguong_hai_ban.test.mjs` — 12 phép kiểm

So **ba bản** (`data/nguong.json` ↔ máy con ↔ máy chủ) và canh **cơ chế**, không canh
con số: thang phạm vi lấy đúng nấc hẹp nhất · hỏi mã không có thì NÉM · bộ mặc định
phải sạch · khoảng hợp lệ bắt được · θ_yếu ≤ θ − 0,20 · P(S), P(G) < 0,5 kể cả câu bẫy
· `soiNguong` trả hết chỗ sai một lượt.

> ⚠ **Cổng KHÔNG đọc bộ ngưỡng đang hành.** Nếu đọc thì chuyên gia đổi θ là cổng vẫn
> xanh trong khi hành vi đã khác — xem mục 5.

### Hai chỗ tự vấp, ghi lại kẻo lặp

1. Sinh bản máy chủ bằng cách cắt chú thích rồi `lstrip` — **mất một ký tự xuống
   dòng**, hai thân lệch nhau đúng 1 byte. Cổng bắt được ngay. Cắt thì cắt bằng
   `slice(indexOf('…') + 2)`, đừng cắt thêm gì.
2. Viết dấu đóng khối chú thích **vào trong** một khối chú thích → nó tự đóng khối,
   tệp cổng lỗi cú pháp. Và phép so ban đầu dùng `split` theo dấu ấy nên chỉ so được
   một mẩu giữa hai dấu — cổng xanh mà chẳng so gì.

### Đợt 1 KHÔNG làm

Tải bộ ngưỡng từ Firestore · `nguongVer` trên bản ghi lượt · bốn bảng · vai trò
chuyên gia · màn hình quản lý · hàm học. Tất cả ở đợt 2–4.


---

## 9 · ĐỢT 2 — ĐÃ LÀM XONG · 10-10-2026

Ngưỡng nay đi từ **tệp/Firestore** vào mã, và mỗi bản ghi mang **phiên bản bộ ngưỡng
đã dùng**. Chưa có bảng Firestore thật (đợt 3) — đọc ra rỗng thì lùi về mặc định,
đúng như mong muốn, và khi bảng có thật thì tự dùng mà không phải sửa gì.

### Hai đường nạp, và vì sao phần TẢI nằm ngoài tệp dùng chung

`nguong.js` có hai bản chép giống hệt nhau từng ký tự. Nhưng hai phía TẢI theo hai
cách khác hẳn — máy con `fetch` tệp tĩnh, máy chủ đọc Firestore — nên nhét cả hai vào
tệp dùng chung là phá luôn phép so của cổng. Phần tải vì thế nằm riêng:

```
tools/xuat_nguong.py            data/nguong.json → web/public/content/nguong.json
src/chung/lib/napNguong.js      máy con: fetch, nhớ lại, hỏng thì lùi về mặc định
functions/src/napNguong.js      máy chủ: đọc bảng `nguong`, NHỚ TẠM 5 phút
```

`xuat_nguong.py` **fail-closed**: giá trị ngoài `[canDuoi, canTren]` hay vi phạm ràng
buộc chéo thì DỪNG, không xuất. Để lọt một giá trị xấu ra tệp chạy thì cả hàng rào
khoảng hợp lệ thành trang trí.

### Bộ đang hành, và cái bẫy thứ tự nạp module

`nguong.js` thêm một ô nhớ `boNguong()` / `datBoNguong()`, đặt **một lần** lúc mở
phiên — đúng mục 3.8.2 ("dùng nó cho cả phiên") và 3.8.4 ("phiên bản mới chỉ có hiệu
lực từ phiên tiếp theo"). `layNguong` vẫn **thuần**: ô nhớ chỉ là chỗ cất, tách hẳn
khỏi phép tính, nên quét lưới của mục 3.8.3 vẫn chạy lại được.

> ⚠ **CÁI BẪY LỚN NHẤT CỦA ĐỢT NÀY.** Mọi hằng ngưỡng trong `mon/**` gọi
> `layNguong(boNguong(), …)` **lúc nạp module**. Mà `import` tĩnh chạy trước mọi dòng
> lệnh — nên `import App from './App.jsx'` kiểu thường sẽ nạp cả cây module TRƯỚC khi
> `napNguong()` kịp đặt bộ. Mấy hằng ấy chụp đúng bộ mặc định, tệp tải về chẳng tác
> dụng gì, **màn hình vẫn chạy ngon và không lỗi nào**. Nên `main.jsx` phải:
>
> ```js
> await napNguong();
> const { default: App } = await import('./App.jsx');   // ĐỘNG, không tĩnh
> ```
>
> Cổng `nguong_phien` canh đúng ba điều này: có `await napNguong()`, có `await
> import('./App.jsx')`, và KHÔNG còn `import App from`.

### Máy chủ đọc lúc GỌI, không đọc bản chụp

Hàm nền sống rất lâu giữa hai lượt. Nếu phép chấm đọc hằng chụp-lúc-nạp thì chuyên
gia sửa ngưỡng xong phải chờ hàm nền khởi động lại mới ăn — **vẫn phải nhờ người viết
mã**, đúng thứ R7 muốn bỏ. Nên `bkt.js` có `thamSo()` đọc bộ đang hành mỗi lần gọi;
`DEFAULT_PARAMS` giữ lại làm mốc cho cổng.

`layBoNguong(db)` **nhớ tạm 5 phút**: đọc Firestore mỗi lượt là thêm một lượt đọc cho
mỗi câu trẻ làm, đổi lấy một thứ gần như không bao giờ đổi. Hỏng thì **lùi về mặc
định và ĐẾM** (`LOI_DOC.lui`), không ném — một sự cố đọc cấu hình không được phép
thành một sự cố mất điểm của trẻ.

### `nguongVer` — và nó kéo theo môn Toán

Bản ghi lượt của **cả hai môn** nay mang `nguongVer`, và tài liệu `mastery` cũng vậy.
Cùng một lẽ với `phienBanMau` đã có: không lưu nội dung, chỉ lưu đủ để **tính lại**.

Kéo theo hai việc: `PHIEN_BAN_BAN_GHI` lên **3 ở cả hai môn** (cổng
`tienganh_sukien` đòi hai môn khai cùng một số), và `mon/toan/lib/sync.js` phải import
`chung/lib/nguong.js`. Hợp lẽ — từ quyết định ②, Toán dùng chung bộ ngưỡng, nên bản
ghi của Toán cũng cần biết nó được tính bằng θ nào.

⚠ **Luật Firestore KHÔNG phải sửa**: `attempts` dùng `keys().hasAll([...])` (trường
bắt buộc) chứ không `hasOnly`, nên thêm trường là hợp lệ sẵn. Đã soi tận nơi.

### Cổng `nguong_phien.test.mjs` — 11 phép kiểm

Thứ tự nạp ở `main.jsx` · không còn chỗ nào đọc `BO_MAC_DINH` · BKT đổi kết quả ngay
khi đổi bộ · quên dần đi theo NG06 · đọc Firestore cả giá trị toàn hệ lẫn theo phạm vi
· hỏng thì lùi và ĐẾM · bảng rỗng cũng lùi · **nhớ tạm thật sự không đọc lại trong
hạn** · `nguongVer` ở cả hai môn · hàm nền nạp bộ TRƯỚC khi chấm · tệp chạy khớp bản gốc.

### Chỗ tự vấp — và cổng CŨ bắt được, không phải cổng mới

`napNguong` ban đầu gọi `fetch(`${CONTENT}/nguong.json`)` **không đóng dấu phiên
bản**. Cổng `cache_noi_dung` đỏ ngay: *"quên `dongDau`: src/chung/lib/napNguong.js:36"*.

Nội dung được phục vụ `public, max-age=604800, immutable` — không có dấu phiên bản
thì trình duyệt giữ bản cũ **một tuần**. Nghĩa là chuyên gia sửa ngưỡng xong, bé vẫn
học bằng bộ cũ bảy ngày, **và không gì báo**. Đúng thứ R7 định bỏ, lại tái sinh ở
tầng cache.

Đáng ghi vì hai lẽ: cổng mới `nguong_phien` của chính tôi KHÔNG bắt được chỗ này —
nó canh thứ tự nạp và đường đọc, không canh cache; và cổng cũ thì bắt ngay. Thêm một
đường nạp nội dung là phải nhớ `dongDau`, như 25 đường kia.

### Đợt 2 KHÔNG làm

Bốn bảng Firestore · vai trò chuyên gia · màn hình quản lý · hàm học ngưỡng · phạm vi
hẹp (mới có `toanHe`). Đợt 3–4.


---

## 10 · ĐỢT 3 — ĐÃ LÀM XONG · 10-10-2026

Từ đợt này, **chuyên gia sửa được ngưỡng mà không nhờ ai viết mã** — đúng điều R7
sinh ra để làm.

### Bốn bảng và vai trò thứ tư

`firestore.rules` thêm `isChuyenGia()` (vai trò `chuyengia`, **tách hẳn khỏi `admin`**
theo quyết định ④) và bốn khối luật:

| Bảng | Đọc | Ghi |
|---|---|---|
| `nguong` | mọi tài khoản đã đăng nhập — máy con PHẢI đọc để chạy | chỉ chuyên gia, **và giá trị phải trong `[canDuoi, canTren]`** |
| `nguong_lich_su` | chuyên gia · admin | **chỉ THÊM** — `allow update, delete: if false` |
| `nguong_de_xuat` | chuyên gia · admin | máy con **không tạo được**; chuyên gia chỉ đổi `trangThai` |
| `thong_ke_nguong` | chuyên gia · admin | `if false` — chỉ hàm nền |

Hai chốt đáng nói:

- **Khoảng hợp lệ soi ngay ở tầng cơ sở dữ liệu**, không chỉ ở màn hình. Chốt ở màn
  hình thì ai gọi thẳng API là qua được.
- **Chuyên gia không sửa được con số trong `nguong_de_xuat`**, chỉ duyệt hay từ chối.
  Sửa được thì "giá trị máy học ra" thành chỗ nhập tay, mà cỡ mẫu và khoảng tin cậy
  đi kèm lại đang nói về một giá trị khác.

### Công thức BKT nay chỉ còn MỘT bản

Bảng 3.21 phải hiện **ngay trên máy con** khi chuyên gia kéo θ — nhưng BKT vốn chỉ có
ở máy chủ, và hai phía không import chéo được. Ba đường: chép sang máy con (bản thứ
ba, sẽ trôi) · gọi máy chủ mỗi lần kéo (chậm, mất cảm giác tức thì) · hoặc đặt công
thức vào đúng tệp **vốn đã có hai bản chép và đã có cổng so**.

Chọn đường thứ ba: `capNhatBKT` nằm ở `nguong.js`, và `functions/src/bkt.js`
`bktUpdate` **gọi xuống đó**. Cổng khẳng định hai hàm cho cùng kết quả, và khẳng định
`bkt.js` không còn giữ công thức riêng.

### Phép kiểm THỨ BA: nhịp tinh thông

`soiNguong` nay có phép kiểm mà hai phép kia không thay được: từng ngưỡng đều trong
khoảng, mà **ghép lại** có thể ra một nhịp dạy vô lý. Đo thật: θ = 0,70 với T = 0,40
— cả hai đều hợp lệ — cho nhịp **2 câu**, bị bác.

**Mã tái tạo đúng Bảng 3.21 của luận văn**, tới ba chữ số thập phân:

```
θ      số câu   khi vừa đạt   sai một câu còn
0,80     3         0,837          0,470
0,85     4         0,944          0,730
0,90     4         0,944          0,730
0,95     5         0,982          0,896
```

Cổng ghim đúng bốn dòng ấy. Nếu một ngày tham số BKT đổi mà bảng trong luận văn không
đổi theo, cổng đỏ ngay — chứ không phải sáu tháng sau mới có người đọc ra.

### Màn hình quản lý ngưỡng

`src/chung/components/BangNguong.jsx`, vào bằng vai trò `chuyengia`. Ba điều bày ra,
mỗi điều một lý do:

1. **Khoảng hợp lệ nằm ngay cạnh ô nhập**, không giấu trong lời báo lỗi — giới hạn mà
   chỉ thấy sau khi gõ sai thì người ta gõ sai rồi mới biết.
2. **Nhịp tinh thông hiện LIỀN mỗi lần sửa, và đặt TRÊN danh sách** — vì đó mới là
   thứ chuyên gia cần nhìn. Màn nói thẳng: *"nên sửa theo con số này, đừng sửa theo
   giá trị xác suất"*.
3. **Lý do là bắt buộc** (luật Firestore cũng đòi `lyDo.size() > 0`) — `nguong_lich_su`
   chỉ đáng giá khi mỗi dòng trả lời được câu "vì sao".

`ghiNguong.js` ghi **hai dòng trong một `writeBatch`**: giá trị mới + dòng lịch sử.
Ghi được cái trước mà hụt cái sau thì có một con số không ai biết vì sao — đúng một
trong ba hạn chế R7 sinh ra để bỏ.

⚠ Phát hành **không đổi phiên đang chạy**; màn nói thẳng điều đó thay vì để chuyên gia
tưởng vừa đổi được cái gì ngay lập tức.

### Luật được MÁY kiểm, không chỉ soi bằng mắt

Bốn khối luật mới nay có **15 phép canh chạy trên bộ giả lập Firestore thật**, thêm
vào `test/luat_firestore.test.mjs` (**76 PASS · 0 FAIL**, trước là 61). Soi bằng mắt
không đủ: một luật viết đúng mà đặt sai thứ tự `allow` là mở toang.

```bash
npm run gia-lap     # cửa sổ 1 — firebase.gialap.json, cổng 8099, dự án ky-su-nhi-thu-luat
npm run test:luat   # cửa sổ 2
```

Mấy phép đáng kể: **admin cũng KHÔNG ghi được ngưỡng** (vai trò tách hẳn) · giá trị
ngoài khoảng bị từ chối ở cả hai đầu · **sửa lại một dòng lịch sử bị từ chối** · thiếu
lý do bị từ chối · khai `nguoiSua` là người khác bị từ chối · không ai tạo được đề
xuất từ máy con.

> ⚠ **Một chẩn đoán SAI của tôi, ghi lại kẻo người sau tin nhầm.** Lần đầu chạy,
> cổng báo *"BỘ GIẢ LẬP KHÔNG CHẠY — bỏ qua"*, và tôi kết luận `npm run test:luat`
> ghim sai cổng nên đã im lặng bỏ qua từ lâu. **Không phải.** Script ghim 8099 và
> `firebase.gialap.json` cũng 8099 — hai số trùng nhau, cổng vẫn chạy bình thường.
> Nó bỏ qua vì chính tôi bật bộ giả lập bằng `firebase.json` (cổng 8080, dự án
> `ky-su-nhi`) thay vì `npm run gia-lap`. Bài học: bật bằng ĐÚNG lệnh của kho trước
> khi kết luận cổng hỏng.
>
> Tôi vẫn bỏ `FS_EMU` ghim cứng khỏi `package.json` — không phải vì nó hỏng, mà vì
> chính tệp cổng dặn "ĐỪNG GHIM SỐ, đọc từ `firebase.gialap.json`", và một con số
> chép hai nơi thì sớm muộn lệch.

### Đợt 3 KHÔNG làm

Hàm nền học ngưỡng · thống kê (Bảng 3.22) · NG20, NG21 · phạm vi hẹp hơn `toanHe` ·
màn hình duyệt đề xuất (bảng `nguong_de_xuat` đã có luật **và đã có phép canh luật**,
nhưng chưa có ai ghi vào).

---

## 11 · PHẠM VI HẸP — ĐÃ LÀM XONG · 10-10-2026

Ba đợt trước mới chỉ dùng **một nấc** của thang phạm vi: `toanHe`. Đợt này mở bốn nấc
còn lại, tức phần còn thiếu của **quyết định ①** (đợt 1 đã hoãn lại: "toàn hệ thống
trước"). Từ đây **θ của lớp 3 khác θ của lớp 5 được**, và chuyên gia đặt điều đó
trong bảng chứ không nhờ ai sửa mã.

### Hai nửa, và chúng không giống nhau

| | Máy con | Hàm nền |
|---|---|---|
| Sống bao lâu | một phiên của **một** bé | dùng chung cho **mọi** bé, mọi môn |
| Lấy ngữ cảnh ở đâu | **phiên** — đặt lúc bé mở quyển | **từng bản ghi**, dựng lại mỗi lượt |
| Rò rỉ thì sao | không rò được: mỗi tab một bé | **chấm bé này bằng ngưỡng của bé kia** |

Nên hai nửa làm hai cách khác hẳn, và cổng canh riêng từng cách.

### Máy con: ngữ cảnh là HÀM của trạng thái, không gán tay

`datNguCanh` / `nguCanhPhien` đã có từ đợt 1; việc còn lại là đặt nó cho đúng.

Bản đầu tôi viết đặt thẳng trong `chonQuyen` — **và sai**. Đổi quyển có **bốn** đường,
không phải một: `chonQuyen` · `veKeSach` về kệ sách · `moCuaPhu` vào môn mà không qua
quyển nào (màn "Học theo chủ đề") · nhánh `loai: 'giai'` mở mùa giải. Ba đường kia sẽ
để ngữ cảnh của quyển TRƯỚC nằm lại, và hậu quả thì **câm hoàn toàn**: bé lớp 3 làm
bài vẫn được chấm bằng θ của lớp 5, không màn nào đổi màu, không cổng nào đỏ — chỉ
mức thạo trong học bạ sai.

Nên ngữ cảnh **suy từ trạng thái** bằng một `useEffect` theo `mon` · `quyen` · `dangKy`.
Thêm đường thứ năm sau này cũng không hỏng được, vì chẳng có chỗ gọi nào để quên.

`khoiLop` lấy từ **sổ đăng ký** (`ct.lop`), không bóc từ tên quyển — sổ đăng ký là nơi
duy nhất khai lớp.

Đo trên bản dựng thật, cả bốn đường:

```
mở Tiếng Anh lớp 5   → { mon: 'tienganh', khoiLop: '5' }
về kệ sách           → { }                       ← không bám lại quyển trước
mở Toán lớp 2        → { mon: 'toan', khoiLop: '2' }
Học theo chủ đề      → { mon: 'toan' }            ← xuyên lớp nên KHÔNG có khối lớp
```

### Mười lăm chỗ quyết định: từ hằng chụp sẵn sang hàm gọi lúc cần

`NGUONG_THAO` · `NGUONG_YEU` · `NGUONG_TRAN` vốn là hằng chụp lúc nạp module — một
con số cho cả hệ thống, đọc xong là đóng băng. Nay mỗi chỗ **quyết định** gọi
`nguongThao(nc)` · `nguongYeu(nc)` · `nguongTran(nc)`, 15 chỗ trong `zpd.js` ·
`chinhsach.js` · `lantruyen.js` · `hosoai.js` · `hoico.js` · `cefr.js`.

Ba hằng cũ **vẫn còn**, nay là ảnh chụp bản `toanHe`: cổng cần một con số cố định để
so, và một cổng đọc giá trị đang hành thì nó tự đồng ý với chính nó.

`viecTiepCuaNut(ho, nc = {})` nhận thêm ngữ cảnh hẹp hơn phiên; `BaiHoc.jsx` chuyền
`{ nut }` — **nấc hẹp nhất của thang**, để chuyên gia nới ngưỡng cho đúng một nút khó
mà không đụng cả khối lớp.

### Hàm nền: dựng lại ngữ cảnh từ bản ghi, và KHÔNG giữ lại

`nguCanhLuot(a)` trong `functions/src/bkt.js` đọc `mon` · `khoiLop` · `bktUnit` của
chính bản ghi, mỗi lượt một lần. `applyAttempt` dựng nó **một lần cho cả lượt** rồi
dùng chung cho `quenDan` (NG06), bốn tham số BKT (NG01–NG05) và `isMastered` (NG07) —
lấy hai lần ở hai chỗ là mở đường cho việc quên dần tính theo lớp 5 mà chấm thạo lại
theo `toanHe`.

⚠ **CHỈ ĐỌC TRƯỜNG BẢN GHI TỰ KHAI.** Mã nút `v_g5_u1_city` có sẵn chữ `g5`, bóc ra
là xong — nhưng đó là **quy ước đặt tên của bộ sinh nội dung, không phải một lời
khai**. Đổi quy ước một lần là mọi lượt lặng lẽ rơi về `toanHe`. `index.js` đã dặn
đúng điều này cho trường `mon` từ trước; đây là lần thứ hai nó đáng nhắc.

Nên **bản ghi phải khai `khoiLop`**: `suKien.js` (Tiếng Anh) và `sync.js` (Toán) cùng
lấy từ `nguCanhPhien()`, và `PHIEN_BAN_BAN_GHI` lên **4**. Nhật ký là bất biến nên
dòng `v ≤ 3` mãi mãi không có trường ấy — chúng trả `null`, `layNguong` bỏ qua nấc đó,
tức **giữ đúng hành vi trước R7**. Một bản ghi đời cũ phải chấm được, không được ném.

Luật Firestore dùng `hasAll` nên trường thêm không bị chặn — không phải deploy rules.

### Cổng

Bốn phép mới trong `test/nguong_phien.test.mjs` (**11 → 15 PASS**):

- ngữ cảnh lượt chỉ đọc trường tự khai — **ghim rằng `v_g5_…` KHÔNG suy ra `khoiLop`**
- cùng một mức thạo, ba phạm vi, ba kết luận "đã thạo" khác nhau (θ 0,85 · 0,60 · 0,99)
  — và nút hẹp hơn thì **thắng** khối lớp
- hai lượt liền của **hai bé khác nhau**: ngữ cảnh bé trước không được rò sang bé sau
- hai môn khai cùng `PHIEN_BAN_BAN_GHI`, và bản ghi thật mang `khoiLop`

**105 tệp cổng · 0 đỏ.** `npm run build` xanh.

### Đợt này KHÔNG làm

Hàm nền học ngưỡng · thống kê (Bảng 3.22) · NG20, NG21 — cả ba đợi **dữ liệu học
thật** (NG21 đòi 200 lượt mỗi phạm vi) · màn duyệt đề xuất · **deploy R7 lên bản thật**.

Và một việc nhỏ còn bỏ ngỏ: nấc `dangCau` của thang phạm vi **chưa có đường vào** —
bản ghi lượt không mang trường dạng câu, nên muốn dùng nấc ấy thì phải khai thêm, y
như vừa làm với `khoiLop`.

---

## 12 · DẠNG CÂU · THỐNG KÊ · ĐÃ LÊN BẢN THẬT — 10-10-2026

### R7 đã lên bản chạy

Ba đợt rưỡi trước mới nằm trên nhánh. Nay **đã deploy cả ba phần**: `firestore.rules`
(bốn bảng + vai trò chuyên gia) · functions · hosting. Đo trên `ky-su-nhi.web.app`:

```
bộ ngưỡng                 phienBan 1 · θ 0,85 · NG09 3
tệp ngưỡng                /content/nguong.json?v=6b3f7101585a   ← dấu phiên bản còn nguyên
mở Tiếng Anh lớp 3        { mon: 'tienganh', khoiLop: '3' }
console                   sạch, không lỗi
```

> Dấu `?v=` là thứ gánh cho `immutable, max-age=604800`. Thiếu nó thì một ngưỡng
> chuyên gia vừa sửa phải chờ 7 ngày mới tới được máy của trẻ.

### Nấc `dangCau` — không phải thêm trường nào

Nấc cuối còn thiếu của thang phạm vi. Hoá ra **đã nằm sẵn trong bản ghi**, ở trường
`mode` (Đợt 1 đã ghi nó để cộng hồ sơ định dạng). Nên lần này không đổi bản ghi,
không lên phiên bản, chỉ đọc đúng chỗ.

Đây là nấc đáng giá nhất cho **NG04 — xác suất đoán trúng**: câu bốn lựa chọn đoán
trúng ~0,25, câu gõ lại chữ thì gần 0. Một con số chung là sai cho cả hai.

⚠ **Hai môn dùng hai bộ từ khác nhau cho cùng trường ấy** — Tiếng Anh `chon · the ·
go · tf · nghenhin · noi`, Toán `so · bieuthuc · dungsai · chondapan · tuluan` —
nhưng `dangCau` là MỘT không gian khoá dùng chung. Chúng không trùng chữ nào, và đó
là **may, không phải thiết kế**: đổi tên `chondapan` thành `chon` là từ đó sửa ngưỡng
cho trắc nghiệm Tiếng Anh thì trắc nghiệm Toán đổi theo, câm. Cổng mới ghim điều đó.

> **Cổng ấy tôi viết hỏng hai lần trước khi đúng.** Bản đầu ghim regex đúng năm chữ
> của Toán — tức ghim CHÍNH TẢ, cái bẫy kho này đã dính bốn lần. Bản hai tự bịa vỏ
> câu để gọi `answerMode`, nhưng vỏ bịa sai hình dạng nên bốn trong năm nhánh rơi hết
> về `so` mà cổng vẫn xanh. Bản ba quét **nội dung thật** (10.103 câu) và lấy đúng
> những mã thực sự xuất hiện — thêm dạng câu mới vào sách là cổng thấy ngay.

### Chức năng thống kê ngưỡng (Bảng 3.22, mục 3.8.5)

`functions/src/thongke.js` — **thuần toán, không đụng Firestore**. Vào: mảng lượt.
Ra: chỉ số. Vì thuần nên chạy lại được trên nhật ký thật với một bộ ngưỡng KHÁC, và
đó đúng là bước "chạy thử lại" mà mục 3.8.3 đòi.

| Ngưỡng | Chỉ số | Đọc thế nào |
|---|---|---|
| NG07 θ | (a) tỉ lệ công nhận sớm · (b) số câu tới khi công nhận | (a) cao → tăng θ; (b) cao mà (a) thấp → đang luyện thừa, giảm θ |
| NG08 θ_yếu | tỉ lệ nút rơi xuống rồi TỰ lên lại | cao → bật phụ đạo không cần thiết |
| NG09 | P(đúng ở lượt kế) sau k = 1…4 lần sai | vẫn tự làm đúng → đang ngắt mạch bé quá sớm |
| NG01–NG05 | AUC · RMSE · sai lệch hiệu chuẩn, theo từng phạm vi | kém ở một phạm vi → học tham số riêng cho nó |
| NG06 h | sai lệch ở lượt đầu sau nghỉ, chia theo Δt | lạc quan sau nghỉ dài → giảm h |
| NG16–NG18 | tỉ lệ gắn nhãn theo dạng câu | một nhóm bất thường → ngưỡng chưa hợp nhóm ấy |

Ba chốt đáng nói:

- **Dựng lại mức thạo từ nhật ký, KHÔNG đọc `mastery`.** Kho ấy chỉ có trạng thái
  hiện tại theo bộ ngưỡng đang hành; muốn biết "với θ = 0,80 thì sao" thì phải chạy
  lại cả chuỗi. Cổng ghim rằng đổi θ thì chỉ số đổi theo (0,80→3 câu · 0,85→4 ·
  0,90→4 · 0,95→5 — đúng **Bảng 3.21**, nay tái tạo được từ cả hai đường).
- **Cỡ mẫu NG21 chặn ĐỀ XUẤT, không chặn THỐNG KÊ.** Giấu số vì "chưa đủ mẫu" thì
  chuyên gia không bao giờ biết dữ liệu đang tới đâu.
- **Hạn chế đi xuống tận tài liệu**, không nằm trong chú thích: `chuaTruPhuDao` (NG08
  đếm cả những lần bé lên lại NHỜ phụ đạo — nhật ký lượt không ghi điều đó) và
  `thieuBac` (Bảng 3.22 đòi gom theo (dạng câu, bậc), nhật ký chưa mang bậc).

### Phép đọc nhật ký — mươi dòng, sai ba lần

`functions/src/docLuot.js`. Tách khỏi `index.js` vì cả ba lần sai đều là loại mà
`node --check`, bản dựng và 105 cổng đều không thấy:

1. Dùng `eachDoc` (sắp theo `__name__`) với phép lọc `ts >= …`. Firestore đòi trường
   bất đẳng thức đứng ĐẦU thứ tự sắp → câu truy vấn ném **lúc chạy**, trong một hàm
   nền hằng tuần, tức nằm im trong nhật ký máy chủ.
2. Lọc trùng bằng `(bé, nút, ts)`. Cả loạt lượt gửi lên cùng lúc mang đúng một mốc →
   **nuốt lượt thật**, im lặng, chỉ làm các con số nhỏ đi.
3. Phân trang theo riêng `ts`, nhích mốc khi cả trang cùng một mốc. Quá 500 lượt
   chung một mốc là mất phần dư — **chính cổng mới viết bắt được**: 700 lượt chung
   một mốc thì đọc ra 500.

Nay phân trang bằng **con trỏ `(ts, mã tài liệu)`**, đúng cặp Firestore sắp theo khi
`orderBy('ts').orderBy('__name__')`. Cặp ấy duy nhất nên không còn trường hợp riêng
nào, và không cần lọc trùng. Đo trên bộ giả lập: 1200/1200 lượt, trong đó 700 chung
một mốc, kèm một tài liệu hỏng xen giữa.

### Hai cổng tự đỏ vì lý do không liên quan — đã sửa

- `luyennoi.test.mjs` cắt `index.js` từ `export const luyenNoi` tới **hết tệp**, tức
  ngầm giả định hàm ấy nằm cuối. Thêm bất kỳ hàm nền nào sau nó là cổng đỏ vì một lý
  do chẳng liên quan gì tới phòng luyện nói. Nay dừng ở `export` kế tiếp.
- `luat_firestore.test.mjs` ghim mã tài liệu `ls1`, mà `nguong_lich_su` là bảng
  **chỉ-thêm** — nên lần chạy THỨ HAI trên cùng bộ giả lập tự đỏ, và đỏ vì chính thứ
  nó đang canh hoạt động đúng. Nay mỗi lần chạy một hậu tố riêng; chạy hai lần liền
  đều 76 PASS.

### Màn hình

`BangNguong.jsx` thêm khối **"Dữ liệu tuần này nói gì về các ngưỡng"**, đặt TRƯỚC 21
ô nhập — cùng lẽ với bảng nhịp tinh thông: để dưới thì người ta sửa xong mới thấy căn
cứ. Mỗi chỉ số hiện thành **câu**, không thành số trần (Bảng 3.22 có hẳn cột "cách
đọc" — một con số không kèm cách đọc thì chuyên gia phải tự đoán nên tăng hay giảm).

Ba trạng thái phân biệt rõ, vì chúng dẫn tới ba hành động khác nhau: **đang nạp** ·
**đã nạp và chưa có số liệu** · **đọc hỏng**.

`docThongKe.js` chỉ ĐỌC kết quả đã tính. Tính lại ở máy con thì phải cho nó quyền đọc
lượt của mọi bé — một cửa dữ liệu rộng hơn hẳn việc hiện vài con số.

### Hàm nền

| | |
|---|---|
| `thongKeNguongTuan` | 03:00 thứ Hai, cửa sổ **90 ngày** |
| `tinhLaiThongKeNguong` | chuyên gia bấm "tính lại", không phải chờ tới thứ Hai |

Cửa sổ 90 ngày chứ không phải cả nhật ký: nhật ký bất biến nên chỉ dài ra mãi, đọc
hết thì một ngày hàm chạm trần 540 giây và từ đó **không có chỉ số nào nữa** — hỏng
đúng lúc dữ liệu nhiều nhất. Mã tài liệu mang **mốc tuần ISO** (đã thử 6 mốc, gồm hai
mốc bắc cầu năm) nên nhìn được theo thời gian, không đè lên một dòng duy nhất.

**107 tệp cổng · 0 đỏ** (thêm `thongke_nguong` 12 phép và `docluot` 8 phép).

### CHƯA làm, và vì sao

- **Hàm nền HỌC ngưỡng** (EM cho NG01–NG05 · hồi quy bán rã cho NG06 · quét lưới cho
  NG07–NG12) và **màn duyệt đề xuất**. Thống kê là phần ĐO; học ngưỡng là phần ĐỀ
  XUẤT, và nó chỉ có nghĩa khi `duMauDeHoc` thành `true` trên dữ liệu thật — hiện
  chưa ai học đủ 200 lượt mỗi phạm vi. Dựng bộ máy đề xuất bây giờ là dựng một cái
  máy chưa có gì để chạy, và không có cách nào biết nó chạy đúng hay sai.
- **Lần chạy thật đầu tiên của `thongKeNguongTuan`** là 03:00 thứ Hai tới. Phép đọc
  và phép tính đã thử trên bộ giả lập với 1200 lượt; phần chưa thử trên dữ liệu thật
  là lượt ghi xuống `thong_ke_nguong`.
- Nấc `bac` và `loaiNut` của thang phạm vi vẫn chưa có đường vào — bản ghi lượt không
  mang hai trường ấy.
