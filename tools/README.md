# Công cụ

* `../web/tools/seed_content_index.mjs` — nạp chỉ mục 168 micro lên Firestore
* `../figforge/render.py` — render hình từ figureSpec
* `../figforge/gen_figurespec.py` — sinh figureSpec khái niệm bằng luật suy dẫn

## Render lại toàn bộ hình
```bash
cd figforge && python3 render.py --specs figspecs_all.json --out ../web/public/content/figures
```

## Xưởng sinh nội dung Tiếng Anh — `xuong/` (việc V12)

Bốn worker soạn nháp cho **một unit**, ba giám khảo bỏ phiếu, phiếu 2–1 thì tranh
luận, rồi mọi thứ nằm trong một danh sách **chờ người duyệt**.

```bash
python3 tools/xuong/dieu_phoi.py --lop 4 --unit 3           # cần khoá Groq
python3 tools/xuong/dieu_phoi.py --lop 4 --unit 3 --kho     # in kế hoạch, không gọi mạng
python3 tools/xuong/test_schema.py                          # 66 phép kiểm, không cần mạng
```

Khoá đọc từ `GROQ_API_KEY`, hoặc từ `web/functions/.secret.local`.

### Ba chốt không được phá

| Chốt | Ở đâu |
|---|---|
| Chỉ ghi vào `data/tienganh/xuong/` — kể cả khi gõ `../../../web/public/content` | `chung.soi_duong_ra` |
| Không tệp nào trong `web/` nhập xưởng (nên nó không bao giờ chạy lúc bé học) | `test_schema.py` khối D |
| Mọi câu qua khuôn + hàng rào vốn từ **bằng code** TRƯỚC khi tới giám khảo | `nen_worker.chay` |

Hàng rào vốn từ **nhập lại** `chu_biet` · `chu_trong` · `cau_lanh_lan` của
`sinh_kichban_noi.py` — không chép bản thứ hai, và `test_schema.py` khẳng định chúng
là **chính** hàm ấy (`is`), không phải bản sao.

### Đo thật, lớp 4 unit 3 (16 giây, 49 lượt gọi)

| | |
|---|---|
| ba giám khảo đều thuận | 5/13 |
| còn bàn (phiếu 2–1) | 3/13 |
| bị loại (≥2 bác) | 5/13 |

Năm mục bị loại **đều bị loại đúng**, và lý do thì chính xác: *"i is at home today —
nhiều câu sai ngữ pháp, từ viết thường"* · *"I read music at park không tự nhiên"* ·
*"thiếu mạo từ a trong play a game"* · *"homework không thuộc chủ đề Me and My
Friends"*.

Đó là bằng chứng cho tầng giám khảo: hàng rào bằng code trả lời được "chữ này bé học
chưa" một cách tuyệt đối, nhưng **không** trả lời được "đây có phải tiếng Anh không".
Túi vốn một unit chỉ 45 chữ và không có từ chức năng, nên mô hình xếp chữ thành câu
không ai nói mà vẫn qua hàng rào. Chỉ giám khảo bắt được loại ấy.

### ⚠ Hai giới hạn, đo ra chứ không đoán

**1 · Tranh luận chạy MỘT model, không phải hai.** Bản thiết kế đòi hai. Khoá này
thấy 12 model nhưng mọi model văn bản khác đều `blocked at the organization level`.
Đặt `GROQ_MODEL_PHU` là có hai model thật; `duyet.md` in thẳng ra khi nó đang chạy
một model, để người đọc không tin đoạn tranh luận hơn nó đáng được tin.

**2 · Một TỪ MỚI kéo theo bốn dây chuyền nữa.** Đo thật: đắp 4 từ vào một unit rồi
chạy cổng thì **sáu tệp cổng đỏ**, và cả sáu đỏ đúng chỗ phải đỏ — thiếu clip đọc
(`tienganh_am`), thiếu nút trong đồ thị (`tienganh_dothi` · `tienganh_manut`), thiếu
hình **và chưa ai soát tận mắt** (`tienganh_hinh_dung_tu`), thiếu video
(`tienganh_video`). Nên "qua 83 cổng" **không** có nghĩa "chạy bộ sinh là xong": một
mục `mau_cau` thì nhẹ, một từ mới là năm bước và bước cuối là mắt người.

### Rót vào nội dung thật

```bash
# 1 · tự gõ tệp chọn: {"tu": [...], "mau_cau": [...]} — chính việc gõ LÀ duyệt
# 2 · đắp rồi dựng (KHÔNG sửa chuan_lopN.json trên đĩa)
python3 tools/sinh_bai_tienganh.py --lop 4 --unit 3 --xuong <tệp chọn>
# 3 · chạy bốn dây chuyền kia nếu có từ mới — xem bảng trên
# 4 · cd web && npm run build && npm test
```
