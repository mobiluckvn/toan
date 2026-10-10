# Điểm dừng — R7 TRỌN MỤC 3.8, VÀ BA KỊCH BẢN CÓ BỘ ĐO · 10-10-2026

Ghi ngày 10-10-2026 (tối). **Đọc trang này trước khi động vào bộ ngưỡng, hàm nền
thống kê/học ngưỡng, hay trước khi tin rằng một màn React nào đó "đã chạy vì cổng
xanh".**

Bản bàn giao trước ở `docs/tiep_theo_di_thu_ban_that.md` (10-10, sáng) — vẫn đúng về
ba lỗi chặn đã vá. Trang này kể phần việc sau đó: **toàn bộ ràng buộc R7 của bản
luận văn v4**, bảng đối chiếu hệ thống ↔ luận văn, và ba kịch bản thực nghiệm.

---

## 1 · Trạng thái kho — ⚠ ĐỌC TRƯỚC

- **`main` ĐÃ GỘP** ngày 10-10-2026 (tối): tua nhanh từ `555201f3` (25-08) lên
  `124a9a8a`, **55 commit**, không một xung đột nào — `main` là tổ tiên thẳng của
  nhánh, đi sau 55 và đi trước 0.
  ⚠ Việc này treo từ 25-08; nay `main` · `origin/main` · nhánh đều cùng một chỗ.
- Nhánh **`phu-dao-va-bo-do-kb2-kb3`** vẫn còn, trỏ cùng commit. Bản thật đang chạy
  đúng mã ấy, nên **không phải deploy lại** sau khi gộp.
- ⚠ Chạy trọn cổng TRÊN CHÍNH CÂY `main` sau khi gộp, không tin vào kết quả chạy ở
  nhánh — kho này từng push một nhánh ở trạng thái vỡ vì `git add` sót thư mục.
- **116 tệp cổng · 0 đỏ** (sáng nay 103) · **`npm run soi` 0 lỗi** (ESLint mới).
- Đã deploy trọn **rules + 18 functions + hosting**.

> ⚠ Giữ nguyên hai cảnh báo của các bản trước: chạy `npm run build` TRƯỚC `npm test`,
> và soi cổng bằng **mã thoát TỪNG TỆP** chứ đừng cộng mấy dòng `N PASS`.

> ⚠ **`npm run soi` chạy RIÊNG, cố ý không gắn vào `npm test`.** Cổng nói về HÀNH
> VI; ESLint nói về HÌNH DẠNG MÃ. Gộp một lệnh thì một lời than về biến thừa chặn
> mất một phép canh về việc dạy trẻ.

---

## 2 · ⚠ PHẦN ĐÁNG ĐỌC NHẤT: BỐN LẦN SUÝT/ĐÃ ĐƯA MÀN TRẮNG LÊN BẢN THẬT

Cùng **một lớp lỗi**, và cả bốn lần `npm run build` xanh, mọi cổng xanh:

| | chỗ | bắt được bằng |
|---|---|---|
| ① | hook sau `return` sớm (React 310) | **đã lên bản thật** — đi thử bằng tay |
| ② | biến dùng trước khi khai ở Phòng luyện nói | **đã lên bản thật** — đi thử bằng tay |
| ③ | `daPhuDao` đọc từ sai component | đọc lại khi viết |
| ④ | quên `import { duocVuotAi }` | đọc lại khi viết |

**Lý do bản dựng không bắt được:** Vite/esbuild **không phân giải tên biến**. Một
biến không tồn tại trong phạm vi vẫn dịch ra JavaScript hợp lệ và chỉ ném LÚC CHẠY.

Nay có **ba lớp đỡ**, và cần cả ba:

1. **`LuoiDoLoi.jsx`** bọc ngoài `<App/>` — thay màn trắng bằng một câu và một
   đường ra bé tự đi được. Không sửa lỗi, sửa HẬU QUẢ.
2. **`man_dung_duoc.test.mjs`** — tự gói bằng esbuild rồi **dựng thật** bốn màn.
   Đã thử ngược: gây lại đúng lỗi ③ → cổng ĐỎ; trả nguyên trạng → xanh.
   ⚠ Dựng ở MÁY CHỦ nên **không** bắt được React 310 (đòi lượt vẽ thứ hai) —
   giới hạn ấy ghi thẳng thành một phép kiểm trong tệp.
3. **ESLint** (`npm run soi`) — bắt lớp lỗi ấy ở dạng tĩnh, trên toàn bộ mã.

### Và ESLint tìm ra một nút ĐANG HỎNG ngay lần chạy đầu

`mocEn` khai trong `PhongNoi`, dùng trong `LuotCo` — **hai component khác nhau cùng
tệp**. Nút 🔈 «nghe lại lời tiếng Việt» ném `ReferenceError` **mỗi lần bé bấm**; lỗi
nằm trong hàm xử lý sự kiện nên không làm vỡ màn, chỉ khiến nút im lặng. Đã vá và
đo lại trên bản thật: bấm, **không một lỗi nào**.

Hai lỗi nữa cùng lớp: hàm `dongHoSo` chết từ đợt V6 mà gọi vào là vỡ, và một khoá
`micros` khai hai lần trong một object literal.

> ⚠ **`export { X } from '…'` là TÁI XUẤT — nó KHÔNG đưa tên vào phạm vi tệp.** Đây
> là nguyên nhân của lỗi ②-kiểu trong `phongnoi.js`, và nó rất dễ đọc nhầm.

---

## 3 · R7 — mục 3.8 của luận văn nay TRỌN

Bốn đợt, tất cả đã deploy. Kế hoạch và nhật ký chi tiết: `docs/ke_hoach_r7_bang_nguong.md`
(12 mục).

| đợt | việc | dấu hiệu xong |
|---|---|---|
| 1 | 21 ngưỡng NG01–NG21 ra `data/nguong.json` | **không đổi một ly hành vi** — 103 cổng xanh y nguyên |
| 2 | hai đường nạp + `nguongVer` trên bản ghi + cổng so hai bản | đổi một giá trị là thấy hành vi đổi ở cả hai phía |
| 3 | 4 bảng Firestore + vai trò `chuyengia` + màn ngưỡng | chuyên gia sửa θ mà không nhờ ai viết mã |
| 4 | thống kê (Bảng 3.22) · học ngưỡng (3.8.3) · màn duyệt | có đề xuất kèm cỡ mẫu và chỉ số trước/sau |

**Thang phạm vi đủ cả BẢY nấc** (`nut · dangCau · bac · loaiNut · khoiLop · mon ·
toanHe`), mỗi nấc có đường dữ liệu thật. Bản ghi lượt nay là **v7**.

### ⚠ Ba chốt KHÔNG ĐƯỢC GỠ

- **Máy chủ KHÔNG suy `khoiLop`/`loaiNut` từ hình dạng mã nút.** Mã `v_g5_u1_city`
  có sẵn chữ `g5`, bóc ra là xong — nhưng đó là quy ước đặt tên của bộ sinh nội
  dung, đổi một lần là mọi lượt lặng lẽ rơi về bộ `toanHe`. Bản ghi phải **KHAI**.
- **Ngữ cảnh phiên SUY TỪ TRẠNG THÁI, không gán tay ở chỗ gọi.** Đổi quyển có BỐN
  đường; gán tay ở một đường thì ba đường kia để ngữ cảnh quyển trước nằm lại, và
  bé lớp 3 được chấm bằng θ lớp 5 — câm hoàn toàn.
- **Máy học để ĐỀ XUẤT, không tự áp dụng.** `hocNguong.js` không ghi vào bảng
  `nguong`; `firestore.rules` chốt thêm một lần (chuyên gia chỉ đổi được `trangThai`).

---

## 4 · Số thật đầu tiên — và một kết quả đáng cho luận văn

Chạy trên **3.213 lượt** nhật ký thật (10 tài khoản, toàn bộ trong 90 ngày):

```
AUC 0,734 · RMSE 0,440 · lệch hiệu chuẩn +0,050
NG07  công nhận sớm 27,8% (mẫu 18) · 6,38 câu tới khi công nhận (mẫu 40)
NG08  tự lên lại 88,4% (mẫu 164) — ⚠ chưa trừ phụ đạo
NG16  bieuthuc 52,7% · so 28,2% · chondapan 10,5% · dungsai 6,0%
```

**Bộ tham số hiệu chỉnh tay THẮNG máy học.** EM cho AUC trên dữ liệu giữ lại
**0,682** so với **0,735** của bộ đang hành — nên hàm học ngưỡng **từ chối** đề xuất
đổi cả bốn tham số BKT. Đây là kết quả bảo vệ Bảng 3.8 bằng dữ liệu, không bằng lập
luận. Nên đưa vào mục 3.8.3.

### ⚠ Một chỗ cách đọc Bảng 3.22 KHÔNG dùng được

NG09 đo được `47,0% · 20,8% · 67,5% · 17,6%` cho k = 1…4. Chỗ vọt lên nằm **đúng
tại k = 3 = NG09 đang hành**, tức đúng chỗ hệ thống bật phụ đạo — lượt kế tiếp ở đó
là lượt **sau can thiệp**, không phải «bé tự gỡ». Đọc nguyên văn thì chuyên gia nâng
NG09 vì chính tác dụng của can thiệp mà NG09 gây ra. Bản ghi v6 đã khai `sauPhuDao`
để tách hai thứ; chờ nhật ký tích đủ dòng v6.

---

## 5 · Ba kịch bản thực nghiệm — bộ đo đã chạy

| | trạng thái | ⚠ điều phải biết khi đọc kết quả |
|---|---|---|
| **KB1** | `node tools/kb1_quet_luoi.mjs` — 1.000 bé mô phỏng, 84.000 lượt | **KHÔNG** trả lời được «ngưỡng nào dạy trẻ tốt hơn» — trẻ mô phỏng học theo BKT vì ta bảo nó thế |
| **KB2** | `chayKB2` — kiểm tra chéo 5 phần + DeLong | **TỪ CHỐI KẾT LUẬN** trên dữ liệu hiện có |
| **KB3** | `node tools/do_an_toan_noi_dung.mjs do` — 149/149 · 136/136 · OOV = 0 | phần ③ chưa chạy: cần `GROQ_API_KEY` và 600 lượt gọi mô hình |

### ⚠ Bản đầu của KB1 vô dụng, và chính kết quả nói ra

NG06 ra đúng **60** và NG07 ra đúng **0,70** — **cả hai đụng biên** khoảng hợp lệ.
Lý do: trẻ mô phỏng **không quên**. Hai con số đụng biên không phải kết quả hiệu
chỉnh; chúng là lời khai rằng mô phỏng không nói được gì về hai ngưỡng ấy.

Nay thế giới mô phỏng có chu kỳ bán rã **riêng** (`nuaDoiThat`) — **phải độc lập với
NG06**, nếu không là vòng tròn. Tính chất đã ghim thành cổng: thế giới quên nhanh
hơn thì `h` học ra nhỏ hơn (đo `4 · 9 · 15 · 19` cho `h` thật `3 · 7 · 14 · 30`).

### ⚠ KB2 từ chối kết luận, và đó là phần đáng kể nhất

DeLong cho p < 0,01 ở **cả sáu cặp** — nhìn qua thì mọi thứ «khác nhau thật». Nhưng
hai cách đọc cho hai thứ tự **ngược nhau** (gộp: `bktQuen` nhất 0,742; trung bình
từng phần: `bktQuen` bét 0,569) và một phần chia chỉ có **3 lượt**. `chayKB2` trả
`ketLuan: 'chuaKetLuanDuoc'` kèm lý do. Trao ra sáu con số p mà không nói điều đó là
mời người đọc kết luận sai bằng chính con số mình đưa cho họ.

---

## 6 · Bảng đối chiếu hệ thống ↔ luận văn v4

`docs/Doi_chieu_he_thong_v4.xlsx` — 9 trang, dựng lại bất cứ lúc nào bằng
`~/.venv/bin/python3 tools/doi_chieu_v4.py`.

- Bảy ràng buộc **R1–R7: 7/7**
- 25 bảng Chương 3: **19 xong** · 3 một phần · 1 chưa · 2 không phải việc mã
- **30 hạng mục làm THÊM** ngoài báo cáo
- Mọi con số ở cột «đo được» **đếm lại từ kho**, không chép từ luận văn

**`docs/sua_luan_van_v4.md`** — mười chỗ cần sửa, mỗi chỗ kèm nguyên văn, câu nên
sửa thành, và cách tự kiểm chứng. ⚠ **Hai chỗ luận văn đang tự đánh giá THẤP HƠN
thực tế** (Bảng 3.25 nói chưa đủ dữ liệu, mà đã có 3.227 lượt).

---

## 7 · VIỆC KẾ TIẾP

### Tôi làm được ngay, không cần gì từ bác
1. ~~Gộp nhánh vào `main`~~ — **XONG 10-10 tối**, xem mục 1.
2. Dọn 51 cảnh báo `exhaustive-deps` của ESLint (hiện để cảnh báo có chủ ý).
3. Không còn nấc phạm vi nào thiếu.

### Cần bác chốt trước
| | việc | vì sao cần chốt |
|---|---|---|
| ⚠ | **BẬT `kb4_phudao_llm`** | **NỚI RÀNG BUỘC R3** — câu do mô hình soạn tới tay bé trước khi người lớn duyệt |
| | BẬT `kb5_zpd` | không nới ràng buộc nào, nhưng nhóm đối chứng học bằng thứ tự kém hơn suốt đợt đo |
| | Thi thử dò được đáp án | sửa thế nào là quyết định sư phạm |
| | 55 bước gợi ý thiếu `dapMau` | bước cuối phải là mắt người |
| | cập nhật luận văn | theo `docs/sua_luan_van_v4.md` |

Cả hai cờ nằm ở `web/src/chung/lib/chiaNhom.js`, **đang để 0 (tắt)**.

### Cần Thầy
«Năm nhóm ngưỡng» của mục 3.8.1 là những nhóm nào — Bảng 3.19 không có cột nhóm, và
tên nhóm trong `data/nguong.json` hiện là **đặt tạm**.

### Không phải việc mã
**KB6** — 5–10 học sinh thật trong 4 tuần. Tới khi chạy xong thì mọi nhận định về
hiệu quả **dạy học** vẫn là giả thuyết, đúng như Bảng 3.25 tự khai. KB1 trên người
học mô phỏng **không thay được**.

---

## 8 · Công cụ mới trong đợt này

| lệnh | làm gì |
|---|---|
| `npm run soi` | ESLint, bộ luật hẹp — xem `web/eslint.config.js` |
| `node tools/kb1_quet_luoi.mjs [--be N] [--ghi]` | KB1 trên người học mô phỏng |
| `node tools/do_an_toan_noi_dung.mjs do` | KB3, không cần mạng |
| `~/.venv/bin/python3 tools/doi_chieu_v4.py` | dựng lại bảng đối chiếu |
| `~/.venv/bin/python3 tools/va_nut_mo_coi.py --ghi` | vá mã nút ngoài đồ thị |
| `python3 tools/va_trung_lua_chon.py --ghi` | vá câu có hai ô giống nhau |

⚠ Hai lệnh cần `GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json`:
`tools/soi_ban_ghi_tienganh.mjs` và `tools/nhap_cau_duyet.py --lay`.

---

## 9 · Dọn cảnh báo ESLint — và ba lỗi ghi sai lộ ra (10-10 đêm, `0704b336`)

`npm run soi` nay **0 lỗi · 0 cảnh báo**. Trước đó 51 cảnh báo, để nguyên có chủ ý
vì kho này có chỗ cố ý bỏ phụ thuộc. Dọn trọn thì bắt được ba lỗi thật.

### Ba lỗi, cùng một lớp: bao đóng giữ giá trị cũ

| Chỗ | Khai sai | Hậu quả |
|---|---|---|
| `BaiHoc.jsx` · `ghiNoi` chặng Mẫu câu | `}, []);` mà thân hàm đọc `ds[i]` | `i` đóng băng ở 0 → **mọi** lượt nói cả chặng ghi `maNut` của câu ĐẦU |
| `BaiHoc.jsx` · `ManTu` · `ghiNoi` | `[onNoi]` | đổi bài không dựng lại component → tra vốn từ bài TRƯỚC → `maNut` null |
| `PhongNoi.jsx` · `thuLai` | thiếu `ma` | buổi luyện nói lưu vào quyển bé đã rời khỏi |

Cả ba hỏng **lặng lẽ**. Hai cái đầu đưa mã nút sai vào nhật ký, mà nhật ký là BẤT
BIẾN — dữ liệu đã ghi trước `0704b336` không sửa lại được. Khi đọc lại Bảng 3.22
cần biết: **lượt `format: 'noiCau'` ghi trước 10-10-2026 có `bktUnit` không đáng
tin**; lượt `noiTu` thì tuỳ, chỉ sai khi bé đổi bài mà không rời màn.

### Luật xử cảnh báo phụ thuộc — hai lối, không có lối "để đấy"

**Thêm phụ thuộc** khi chứng minh được là tương đương hoặc đúng hơn:
- hàm trần chỉ đọc một giá trị → `useCallback` với đúng giá trị ấy (`dangCua`);
- giá trị đã là `useMemo` nên danh tính ổn định (`mocEn`, `canNoiGi`);
- mục của một hằng mức mô-đun (`ct?.bai` lấy từ `SO_DK`) — khai nó KHÔNG nạp vòng vòng;
- effect đã tự chốt "đúng một lần" bằng cờ (`daGhi`, `daDocKet`) → khai ĐỦ là vô
  hại, và con số ghi sổ thành con số của lượt vừa xong thay vì lúc dựng màn.

**`eslint-disable-next-line` kèm lý do** khi bỏ phụ thuộc là chủ ý — bốn chỗ, mỗi
chỗ ghi rõ hậu quả nếu thêm: `cau.id` (thêm `cau.the` là xoá chữ bé đang gõ) ·
`bai?.id` (thêm `pools` là nạp lại đồ thị + bài tiên quyết mỗi lần vẽ) · `khoaBac`
(`bac` do `.find()` trả nên là object mới mỗi lần vẽ → vòng lặp tải) · `id` của
`maPhien` (là thứ KÍCH HOẠT, không phải thứ đọc).

### Việc kế tiếp sau đợt này

Nhóm "tôi tự làm được" đã **hết việc**. Mọi mục còn lại ở mục 8 đều chờ bác chốt
(hai cờ thí nghiệm, Thi thử, 55 `dapMau`, sửa luận văn), chờ Thầy (tên năm nhóm
ngưỡng), hoặc không phải việc mã (KB6 — học sinh thật, 4 tuần).
