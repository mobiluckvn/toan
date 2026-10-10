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
