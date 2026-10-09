# Điểm dừng — MƯỜI HAI VIỆC AI AGENT, XƯỞNG NỘI DUNG, VÀ BẢN THẬT ĐÃ LÊN · 09-10-2026

Ghi ngày 09-10-2026. **Đọc trang này trước khi động vào phòng luyện nói, phần chấm
viết, xưởng nội dung (`tools/xuong/`), hay trước khi deploy lại.**

Bản bàn giao trước ở `docs/tiep_theo_phu_dao.md` (26-08) — vẫn đúng về luồng phụ đạo
và hai bộ đo KB2 · KB3, nhưng **mục "VIỆC KẾ TIẾP" của nó đã xong mục 1** (deploy
luật), và danh sách việc nay thay bằng mục 7 dưới đây.

Hôm nay làm trọn **mười hai việc V1→V12** của
`docs/REVIEW_18_MAU_AI_AGENT_TIENG_ANH.md`, rồi **deploy lên bản thật**. Hai việc có
kết cục khác "xong và bật", và đó là phần đáng đọc nhất của trang này.

---

## 1 · Trạng thái kho — ⚠ ĐỌC TRƯỚC

- Nhánh **`phu-dao-va-bo-do-kb2-kb3`**, HEAD `8fe6110d`, **đã push**, cây sạch.
- `main` vẫn đứng ở `555201f3` — **chưa merge**. Bản thật đang chạy mã của NHÁNH.
- 25 commit từ `main`: 172 tệp, +22 268 / −11 894 dòng.
- `npm run build` xanh · **103 tệp cổng · 2 874 phép kiểm · 0 tệp đỏ**
- `python3 tools/xuong/test_schema.py` → **66 PASS · 0 FAIL**
- `npm run test:luat` (bộ giả lập) — 61 phép canh luật.

> ⚠ **Chạy `npm run build` TRƯỚC `npm test`.** Một tệp cổng soi chính bản dựng (dấu
> phiên bản nội dung), nên sai thứ tự là nó đỏ mà chẳng có gì sai.

> ⚠ **Soi cổng trên CÂY ĐÃ PUSH, và soi bằng mã thoát TỪNG TỆP.** Bộ chạy không dừng
> ở tệp đầu hỏng, mà chỉ ~64/103 tệp in dòng `N PASS · 0 FAIL` — cộng mấy dòng ấy rồi
> thấy "0 FAIL" là đang đọc hai phần ba bộ cổng mà tưởng đã đọc hết. Xem
> `0-fail-tren-dia-khong-phai-tren-cay-da-push` trong sổ nhớ.

---

## 2 · ĐÃ DEPLOY LÊN BẢN THẬT — 09-10-2026

Dự án `ky-su-nhi` · **https://ky-su-nhi.web.app**

| Phần | Kết quả |
|---|---|
| `firestore:rules` | ✔ released — **mở ba tính năng đã bị từ chối trong im lặng** |
| `functions` | ✔ **3 tạo mới** + 12 cập nhật |
| `hosting` | ✔ release complete |

**Ba tính năng mà rules vừa mở** (chúng đã có mã từ V3 · V5 · V9 nhưng Firestore vẫn
từ chối, và từ chối KHÔNG báo gì): trí nhớ của cô giáo máy (`hoSoAI`), bố mẹ xác nhận
điểm bài viết (`allow update`), hàng đợi duyệt câu phụ đạo (`choDuyetTA`).

**Ba hàm tạo mới:** `phanXuNoi` (V10) · `luyenNoiTool` (V11, nhưng máy con đang TẮT
nhánh gọi nó) · `sinhCauPhuDao` — ⚠ tức callable của V9 **trước nay cũng chưa từng
lên**, dù mã đã có từ đợt trước.

**Đã soi bản chạy thật, không chỉ tin lệnh deploy:**

- `index-BBRdwOAQ.js` trên mạng **khớp** `dist` tại máy;
- `dochieu.json` của cả ta3 · ta4 · ta5 trên mạng khớp kho **từng byte**;
- ba callable mới trả `UNAUTHENTICATED` (401) khi gọi trần — tức chúng **tồn tại,
  tới được, và chốt cửa đăng nhập hoạt động**. Nếu là 404 thì mới là chưa lên.

> ⚠ **CHƯA đi thử bằng tay một buổi trọn vẹn trên bản thật.** Đây vẫn là mục 2 của
> bản bàn giao 26-08 và nó vẫn chưa làm. Kho này có hai bài học riêng về đúng chuyện
> ấy (`kiem-bang-mat-truoc-khi-deploy`, `di-thu-ban-chay-bat-duoc-cai-cong-khong-bat`):
> cổng xanh và deploy xanh **không** chứng minh bé bấm được.

---

## 3 · Mười hai việc — ba việc cuối làm hôm nay

### V10 · Chấm viết "lỗi ∥ khen", và lượt nói mơ hồ bỏ phiếu — `9e2f8edd`

**Chấm viết** tách mắt xích tìm lỗi thành HAI lượt song song. Trước đây lời khen do
mắt xích sửa viết — tức nó vừa đọc danh sách năm lỗi xong rồi mới điền vào trường
"khen". Nay lượt tìm khen là lượt riêng, không thấy danh sách lỗi.

`gopKhen` gộp hai danh sách **bằng mã**, bịt hai chỗ mà chạy song song mở ra: nó
**khen câu bé không hề viết** (bé viết *"I have two cat"*, nó khen *"I have two
cats"*), và **cùng một câu vừa khen vừa bị liệt lỗi** — chỗ sau thì lỗi thắng.

**Chấm nói** vùng 5–7 đem hỏi hai phiếu, khác nhau hai đường: nhiệt, và **thứ tự hai
chữ đảo ngược**. Lời dặn **không nói chữ nào là chữ đang hỏi** — hai chữ vào dưới tên
A và B.

⚠ **Làm theo §7 đúng nguyên văn thì phần này không bao giờ chạy.** §7 lấy từ cạnh
tranh ở `kq.nhamThanh`, mà `chamTu` chỉ đặt nó khi từ bên cạnh **thắng hẳn** — lúc ấy
điểm bị ép trần 3, ngoài vùng [5,7]. Nên thêm `doiThuGan`: báo ra từ cạnh tranh gần
nhất **kể cả khi nó không thắng**. Báo ra KHÔNG đổi điểm một ly (có cổng riêng canh,
vì 711 câu đã đo của bốn quyển phụ thuộc nó).

**Đo:** 0,6% lượt nói rơi vào vùng mơ hồ (15/2 348) → 11 cặp độc nhất. Đảo vai hai
lần chạy, 22 lượt: **lệch 0 lần**. `blothel` → `brother` cả hai lần, đúng ca bộ chấm
chuỗi **sai hẳn** (mother 0,71 > brother 0,57).

⚠ Ba điều chưa đạt / phải nói ra, chi tiết trong commit: tiêu chí §7 đòi 50 mẫu
**chấm tay** nên chưa đạt được bằng code; bộ đo bản đầu của tôi gán nhãn sai rồi cho
ra "sai 23%" (con số vô nghĩa, đã bỏ và ghi lý do trong `tools/do_phan_xu.mjs`); và
**cùng một lượt nói ra hai điểm khác nhau giữa hai lần chạy** (6/11 rồi 3/11 nhất
trí) — chưa chữa, giới hạn thiệt hại là ±1 trong [5,7].

### V11 · Nhánh ReAct cho lượt bé hỏi lại — `f22e1d0b` · **MẶC ĐỊNH TẮT**

Bốn tool thuần trên gói `kho` máy con gửi lên, trần 3 bước, bắt lặp, kết quả ≤300 ký
tự, 110 phép kiểm, có đường lùi. **Nhưng cờ `BAT_NHANH_TRA = false`.**

Đo bằng Groq thật, 25 lượt (`node tools/do_hoi_co.mjs`):

| Bé hỏi | đường cũ | nhánh tra |
|---|---|---|
| nghĩa chữ **trong** bài | 10/10 | 10/10 |
| một chữ **ngoài** bài (đúng = **không** dạy) | 10/10 | 10/10 |
| chữ ấy **đọc thế nào** — tiêu chí §7 | — | **0/5** |
| tool được gọi | — | **4/25** |

Ba điều rút ra:

1. **Giả thuyết dựng ra nhánh này sai.** Lý lẽ ban đầu: "từ lớp 3 bảng vốn dài hàng
   trăm chữ". Đếm ra: bảng một bài lớp 3–5 chỉ **7–13 chữ**.
2. **Hàng rào vốn từ đã giữ được mà không cần tool** — lời dặn nhãn `hoiLai` (§9 A7)
   một mình chặn đủ: 10/10 lượt cô hẹn "mình học sau nhé" và không dịch.
3. **Tool `nghe_lai` trùng với một kênh đã có.** `PhongNoi` vốn **đọc to `tra.en` ở
   mọi lượt**, nên "phát chữ cho bé nghe" là hành vi mặc định. Tiêu chí "kèm clip"
   của §7 thật ra **đã đạt** — bằng đường cũ.

Số phải xem trước khi bật: `LOI_HOI_CO.buoc / LOI_HOI_CO.goi`. Quanh 0 thì để tắt.

⚠ **Lỗi tôi tự chuốc, lần thứ ba cùng một họ.** Bản đầu chết **19/20** lượt với Groq
400 `attempted to call tool 'json' which was not in request.tools` — mô hình thấy lời
dặn đòi JSON **và** thấy có `tools`, nên trả lời qua kênh tool bằng một tool nó tự
đặt tên. Bản vá đầu của tôi (chèn một dòng "đừng trả JSON lượt này") **không ăn**, vì
dòng ấy nằm **dưới** khối `HARD RULES`. Chữa bằng cách khai đúng tool nó đang đòi
(`tra_loi_be`) — và bản vá ấy còn **rẻ hơn**: trả lời ngay ở lượt một.

### V12 · Xưởng sinh nội dung offline — `8d9f2f68`

`tools/xuong/`: bốn worker soạn nháp cho **một unit**, hai tầng soi bằng **code**, ba
giám khảo song song, phiếu 2–1 thì tranh luận hai vòng, rồi dừng ở `duyet.md`.

Chỗ **duy nhất** trong kho mà Python gọi mô hình. Ba chốt, cả ba có cổng:

| Chốt | Ở đâu |
|---|---|
| chỉ ghi vào `data/tienganh/xuong/` — soi đường dẫn **đã giải**, nên `../../../web/public/content` cũng bị bác | `chung.soi_duong_ra` |
| không tệp nào trong `web/` nhắc tới xưởng | `test_schema.py` khối D |
| khuôn + hàng rào vốn từ chạy **trước** giám khảo | `nen_worker.chay` |

Hàng rào **nhập lại** `chu_biet`/`chu_trong`/`cau_lanh_lan` của `sinh_kichban_noi.py`
và cổng khẳng định đó là **chính** hàm ấy (`is`) — không chép bản thứ hai.
⚠ §7 ghi phép soi ấy "đã có trong `chuan_tienganh.py`": **không có**, tệp ấy dựng bản
chuẩn chương trình chứ không soi câu nào.

**Đo thật, lớp 4 unit 3 · 16 giây · 49 lượt gọi:** 5/13 ba giám khảo đều thuận · 3/13
còn bàn · **5/13 bị loại**. Năm mục bị loại **đều đúng**: *"i is at home today — nhiều
câu sai ngữ pháp, từ viết thường"* · *"I read music at park không tự nhiên"* · *"thiếu
mạo từ a trong play a game"* · *"homework không thuộc chủ đề Me and My Friends"*.

**Và đó là bằng chứng CHO tầng giám khảo — ngược hẳn V11.** Code trả lời được "chữ này
bé học chưa" một cách tuyệt đối, nhưng **không** trả lời được "đây có phải tiếng Anh
không". Túi vốn một unit 45 chữ và không có từ chức năng, nên mô hình xếp chữ thành
câu không ai nói mà vẫn qua hàng rào sạch.

---

## 4 · Mấy chỗ hỏng hôm nay, và bốn là của tôi

| | Chỗ hỏng | Chỉ lộ ra khi |
|---|---|---|
| 1 | Cloudflare chặn `User-Agent` của `urllib` → **mọi** lượt gọi trả `403 error code: 1010`, không thân lỗi. Cùng khoá ấy `curl` và SDK JavaScript đều chạy ngon | gọi Groq từ Python |
| 2 | `chung.TOKEN` khoá `"tu_moi"` mà `khuon.LOAI` dùng `"tu"` → `KeyError: 'tu'` | lượt gọi đầu tiên |
| 3 | Phép rút câu gộp **ba** thứ khác loại vào một danh sách: công thức bị bác vì ô trống `[Noun]`; phương án trắc nghiệm trùng giữa hai câu hỏi bị đếm là "câu lặp" | đọc đầu ra thật |
| 4 | Lời dặn xin "một kịch bản 6 bước", mô hình đọc `muc` thành danh sách **bước** rồi trả **sáu** kịch bản một-bước. Trần 12 nhận hết | đọc đầu ra thật |
| 5 | `--xuong` vỡ `KeyError: 'go_duoc'` — mục `tu` thật có **19 trường**, nhiều trường do bản chuẩn **suy ra** từ bản đồ | chạy bộ sinh |

Và **hai cổng cũ** phải sửa, cả hai dính đúng cái bẫy chúng tự cảnh báo ba dòng trên:
`vantay_prompt` so **tổng độ dài** (chú thích ngay trên đó dặn "đừng soi độ dài");
`tienganh_chamviet` phát câu trả lời theo **số thứ tự lượt gọi**, mà nay hai lượt chạy
song song.

---

## 5 · Xưởng: cách rót vào nội dung thật

```bash
python3 tools/xuong/dieu_phoi.py --lop 4 --unit 3        # cần khoá Groq
python3 tools/xuong/dieu_phoi.py --lop 4 --unit 3 --kho  # in kế hoạch, không gọi mạng
python3 tools/xuong/test_schema.py                       # 66 phép kiểm, không cần mạng
```

1. Đọc `data/tienganh/xuong/duyet.md`.
2. **Tự gõ** một tệp `{"tu": [...], "mau_cau": [...]}` chỉ gồm mục muốn giữ — *chính
   việc gõ tệp ấy LÀ hành động duyệt.* Đừng đưa `lop{N}_u{NN}.json` vào bộ sinh: tệp
   ấy có cả phần còn bàn và phần bị loại.
3. `python3 tools/sinh_bai_tienganh.py --lop 4 --unit 3 --xuong <tệp chọn>`
   (`--xuong` **không** sửa `chuan_lop{N}.json` trên đĩa — đắp trong bộ nhớ rồi dựng).
4. ⚠ **MỘT TỪ MỚI KÉO THEO BỐN DÂY CHUYỀN NỮA.** Đo thật: đắp 4 từ vào một unit lớp
   4 rồi chạy cổng → **sáu tệp cổng đỏ**, cả sáu đỏ đúng chỗ phải đỏ:

| Cổng đỏ | Vì sao | Phải làm gì |
|---|---|---|
| `tienganh_am` · `tienganh_hai_loi_22_08` | từ mới chưa có clip đọc | dây chuyền âm |
| `tienganh_dothi` · `tienganh_manut` | nút tri thức mới chưa có trong đồ thị | cập nhật đồ thị |
| `tienganh_hinh_dung_tu` | chưa có hình, **và chưa ai soát tận mắt** | vẽ, rồi **người** soát |
| `tienganh_video` | video từ mới chưa render | dây chuyền video |

   Một mục `mau_cau` thì nhẹ; một **từ mới** là năm bước, bước cuối là mắt người.
5. `cd web && npm run build && npm test`

`data/tienganh/xuong/` nằm trong `.gitignore` — bản nháp trong git là bản nháp sớm
muộn có người tưởng là nội dung thật.

---

## 6 · Lời dẫn câu đọc hiểu — 19 câu · `8fe6110d`

Đợt **hai** của "mỗi câu hỏi một đáp án đúng" (bác chốt 29-08): rà trọn 176 câu / 75
bài lớp 3 · 4 · 5, lần này đọc đoạn, đọc câu hỏi **và mở từng tệp PNG**. Đợt trước chỉ
soi **mồi** nên mù hẳn với ba họ nằm ở phía **câu hỏi**: lệch đại từ (`How does HE…` →
`SHE does yoga.`), lệch mốc thời gian (`…in the MORNING?` → đoạn ghi *in the evening*),
và tranh hai người mà lời dẫn chỉ nói "bạn ấy".

Sửa ở **cả hai nơi** — `data/tienganh/canh_lop{N}.json` là bản gốc,
`web/public/content/ta{N}/dochieu.json` là bản dựng. Kèm `tools/soat_hoi_chot.py`
(cổng soi phía câu hỏi, cùng họ `soat_moi_nhu.py`); nay nó báo **0 chỗ** còn phải đọc
lại.

---

## 7 · VIỆC KẾ TIẾP, theo thứ tự

1. **Đi thử bằng tay MỘT BUỔI TRỌN VẸN trên bản thật.** Việc này đã nằm trong bản bàn
   giao 26-08 và vẫn chưa làm, mà nay còn gấp hơn: rules vừa mở ba tính năng chưa ai
   bấm thử trên bản chạy (trí nhớ của cô · bố mẹ xác nhận điểm · hàng đợi duyệt câu),
   và `sinhCauPhuDao` vừa lên lần đầu.
2. **Merge nhánh về `main`.** Bản thật đang chạy mã của nhánh, `main` còn ở `555201f3`
   — tức `main` không còn là thứ đang chạy, và đó là một chỗ dễ nhầm.
3. **Hàng đợi duyệt câu phụ đạo chưa có đường ra** (`choDuyetTA` chỉ đầy lên). Cần
   `tools/nhap_cau_duyet.py` ghép câu đã duyệt vào kho tĩnh.
4. **Xưởng chưa qua đợt dùng thật nào** — nên tiêu chí §7 *"bác duyệt dưới 10% bác
   bỏ"* chưa đo được. Chạy một unit rồi duyệt thật là đo được ngay.
5. **Vòng tranh luận của xưởng chạy một model.** Mọi model văn bản khác `blocked at
   the organization level`. Mở một model nữa rồi đặt `GROQ_MODEL_PHU`.
6. Nợ cũ còn nguyên, từ bản bàn giao 26-08: `congHuong` chưa ai gọi · 19 nút gốc rễ
   không có bài nào dạy · bộ nối ΔC (chặn KB4) · Chương 1 và Chương 4 luận văn.
7. Nợ mới, đã ghi trong README mục "Chưa làm": `nhamTu` chưa có nguồn ở **phòng nói**
   (phòng nói chấm cả CÂU bằng `chamCau`, nơi không có đối thủ nào) · lời dặn cho dùng
   chữ chức năng mà `chuLa` thì không (vá là **nới** hàng rào, nên để bác quyết) ·
   khung mẫu câu HAI Ô không ai soi nổi · đường đọc Firestore thật của
   `tools/doc_delta_c.mjs`.

Xem thêm `[[0-fail-tren-dia-khong-phai-tren-cay-da-push]]`,
`[[loi-dan-tu-choi-nhau]]`, `[[kiem-bang-mat-truoc-khi-deploy]]`,
`[[cong-ghim-chinh-ta-thay-vi-tinh-chat]]`.
