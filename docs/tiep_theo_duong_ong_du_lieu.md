# Điểm dừng — ĐƯỜNG ỐNG DỮ LIỆU HỌC · 23-08-2026

Ghi tối 23-08-2026. **Đọc trang này trước khi động vào `attempts`, `mastery`, hàng
đợi tại máy, hay phần số liệu của luận văn.**

Ngày hôm nay bắt đầu bằng việc vá bốn mục nhỏ ở phụ lục Chương 2, và kết thúc
bằng việc phát hiện đường ống ghi nhận dữ liệu — thứ cả tầng thích ứng đứng lên
trên — đã hỏng suốt từ đầu. Trang này ghi lại đủ để mai làm tiếp mà không phải
dò lại.

---

## 1 · Đã xong và ĐÃ LÊN BẢN THẬT

### Bốn việc phụ lục Chương 2

| Việc | Chỗ nằm |
|---|---|
| Vân tay prompt vào `attempts` | `functions/src/vantay.js` → `goiChamViet.js` → `suKien.js` |
| Sự kiện bỏ dở | `BaiHoc.jsx` (gỡ màn) → `ManTiengAnh.jsx` → học bạ `loai='phien'` |
| Báo cáo riêng đọc cả hai môn | `dungSoHoc` gộp `progressTA` + `hocBaTA` |
| Quy đổi P(L) → CEFR | `mon/tienganh/lib/cefr.js` + thẻ ở Góc bố mẹ |

### Hai lỗi ĐƯỜNG ỐNG — nặng nhất trong ngày

**① Mỗi phiên chỉ MỘT lượt lên được máy chủ.**
`attempts` khai `allow update, delete: if false` (nhật ký bất biến), mà máy con
mỗi lượt lại dựng lại và gửi **cả phiên**; `writeBatch` thì nguyên khối, nên một
bản ghi đã có làm rơi **cả lô**. Hệ quả: lượt 1 lên, mọi lượt sau chết trong
localStorage. Cả dự án có **2** bản ghi Tiếng Anh cho hai buổi ~10 lượt.

Vá **hai tầng**, thiếu tầng nào cũng vô dụng:
- ① sổ `ttd5.daGuiTA.v1` / `ttd5.daGui.v1` — không xếp lại mã đã lên;
- ② lô hỏng thì **thử lại từng bản ghi**; lẻ mà `permission-denied` thì coi như
  đã có trên máy chủ và bỏ khỏi hàng đợi; lẻ hỏng vì mã lỗi **khác** thì giữ.

> ⚠ Tầng ① chỉ chặn từ nay. Máy đang mang hàng đợi nhiễm độc thì kẹt vĩnh viễn —
> deploy bản chỉ-có-① rồi đi thử lại ra **đúng 0** bản ghi mới. Phải có ② mới gỡ.

Đo lại cùng một thao tác sau khi vá: **2 → 18**.

**② 130/398 bản ghi nằm sai học bạ.**
`reassignQueue` (Toán) và `sangTenHangDoi` (Tiếng Anh) hỏi *"có phải của tôi
không"* rồi sang tên **mọi** thứ còn lại — kể cả bản ghi của một bé **có thật**
khác. Ghép với lỗi ①: bé A học, 1 lượt lên, phần còn lại kẹt; ít ngày sau bé B
đăng nhập vào **cùng một chỗ** → cả xấp của A thành của B.

Nay chỉ nhận bản ghi chưa có chủ (`local`); của bé thật khác thì bỏ ra và **đếm**
vào `boLai` chứ không bỏ im lặng.

### Ba lỗi buổi đi thử bản chạy bắt được

| | |
|---|---|
| Màn học **trắng bốc** | React #310 — hook `useRef` đặt sau `return` sớm, do chính bản vá sáng nay. Cổng `hook_truoc_return.test.mjs` soi 57 tệp `.jsx` |
| P2 vá **nửa vời** | lối lui "Con chưa nói được" chỉ có ở chặng Từ mới; chặng Mẫu câu cũng đòi nói. Cổng nay **ĐẾM** số ô nói và đòi đủ chừng ấy lối lui |
| "Cần cố gắng: **Bài undefined**" | khuôn phần tử `canCoGang` chưa bao giờ được ghi ra → hai môn nộp hai kiểu. Đã ghi khuôn vào `soMon.js` |

### Đã dọn kho

`attempts` **398 → 268** · `mastery` **32 mục**, dựng lại từ nguồn bằng chính
`applyAttempt` của hàm nền.

Đối chiếu sau khi dọn: 0 phiên hai chủ · 0 lỗ trong dãy số thứ tự (48/48 nhóm
bé·phiên·bài) · **32/32** mục `mastery` khớp đúng số lượt · 0 nút thiếu.

> Sao lưu: `sao_luu_don_ban_ghi.json` (125 bản) và `sao_luu_don_ban_ghi_2.json`
> (5 bản), kèm `mastery` trước khi dựng. **Nằm ngoài git.** Còn bản sao thì vẫn
> **trả về đúng chủ** được nếu đổi ý.

**Cổng: 92 tệp, 0 FAIL.** Năm cổng mới đều đã **thử ngược** và đỏ đúng chỗ:
`luot_khong_roi` (29 phép) · `hook_truoc_return` · `khuon_hocba` · `pha_vao_bkt` ·
`cefr_quy_doi`. Luật trên bộ giả lập 33/33.

Đã deploy đủ ba tầng (luật → hàm nền → giao diện), gói `index-CT1m3F04.js`.

---

## 2 · ⚠ VIỆC PHẢI LÀM ĐẦU TIÊN NGÀY MAI

**Lấy lại số liệu sau mốc dựng lại 21 giờ.**
`report/{uid}` · `teacherBoard/global` · `bangXepHang/global` là bản **tổng hợp**,
dựng từ dữ liệu vừa bị dọn. Tối 23-08 chúng còn giữ số **cũ**. Sáng 24-08 mở lại
Sổ bố mẹ và bảng cô giáo, đối chiếu với `attempts` hiện tại — nếu vẫn lệch thì
việc dựng lại hằng đêm có vấn đề riêng, phải soi `nightlyTeacherBoard`.

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json   # xem mục 4
node tools/soi_ban_ghi_sai_chu.mjs      # phải ra 0/268
node tools/soi_ban_ghi_tienganh.mjs     # phien · vân tay · mastery
```

---

## 3 · Còn nợ, theo thứ tự đáng làm

1. **Đi thử một buổi TRỌN VẸN trên bản chạy.** Hôm nay mới đi tới chặng Luyện
   tập. Chưa buổi nào đi hết Sát hạch → xong bài → sinh thẻ ôn → màn ôn lại.
   Đặc biệt: **chưa bản ghi `phien` nào sinh ra từ đường "đóng thẳng tab"** —
   và đó là giới hạn đã biết, không phải lỗi.
2. **`reviewQueue` sinh thẻ mà KHÔNG màn nào đọc.** Ghi trong `functions/index.js`
   từ 22-08, vẫn đúng tới hôm nay. Lịch lặp lại ngắt quãng mới xong nửa đường ống.
3. **Bốn mục Chương 2 không phải việc code** — xem `docs/sua_chuong2.docx`, phụ lục.
4. **Cài ESLint.** Bốn lần suýt dính `no-undef` trong hai ngày, và lỗi hook hôm
   nay ESLint bắt được ngay (`react-hooks/rules-of-hooks`).
5. **`sessionId` của Toán nên mang cả `learnerId`.** Hôm nay phải suy chủ thật
   bằng ba nhân chứng gián tiếp; nhúng thẳng mã bé vào là khỏi phải suy.

---

## 4 · Những cái bẫy đã trả giá để biết — ĐỪNG DẪM LẠI

- **Khoá quản trị** đang ở `repo/khoa-dich-vu.json`, đã chặn trong `.gitignore`.
  Kho này hay commit bằng `git add -A` nên chỗ chặn ấy là chỗ chặn **duy nhất**.
  Nên chuyển ra ngoài thư mục kho.
- **Đừng nới luật cho `attempts` ghi đè được** để "sửa" lỗi ①. Tính bất biến là
  thứ mục 2.5.2 luận văn dựa vào. Chỗ sai ở máy con gửi thừa, không ở luật.
- **Đừng dùng độ trễ `serverTs − ts` làm tiêu chí một mình.** Trung vị cả kho là
  25 giờ. Cái nói lên chuyện là **sự tương phản trong cùng một phiên**.
- **Cổng xanh + build xanh + deploy xong ≠ màn hình chạy được.** Ba lỗi hôm nay
  đều lộ khi MỞ ĐÚNG MÀN trên bản thật.
- **"Đã vá" ≠ "đã chạy".** Phải đo lại trên bản thật sau mỗi lần deploy — bản vá
  một tầng đã lừa được tôi một lần.
- **Cổng ghim chính tả** làm khổ hai lần hôm nay: một cổng đỏ oan môn Toán vì
  grep tên trường (Toán lấy qua `{...b}`), một cổng đỏ oan câu tiếng Việt trung
  thực vì regex bắt cả thể phủ định. Kiểm **tính chất**, và khi được thì **gọi
  hàm rồi soi vật trả về**.
- **Bộ dọn từng suýt đè mất bản sao lưu** của lần chạy trước. Nay đánh số tiếp.

---

## 5 · Ảnh hưởng tới luận văn — đọc kèm `docs/sua_chuong2.docx`

Hai mục **mới** ở nhóm A, và cả hai đụng vào phần **số liệu** chứ không chỉ câu chữ:

- **A-2.5.2** — dữ liệu trước 23-08 không dùng để phân tích được. Có sẵn đoạn
  viết để chép vào chương thực nghiệm.
- **A-2.3.2** — BKT từng bỏ trắng **31%** số câu bé thực làm (pha `check`,
  `worked`). Một chú thích trong mã từng khẳng định hai pha ấy "chỉ Tiếng Anh
  phát" — sai, Toán có 49 lượt. Cổng `pha_vao_bkt.test.mjs` nay canh chỗ đó.

> Nói ra chuyện dọn kho là **điểm cộng**; im là điểm trừ. Người phản biện đối
> chiếu số liệu hai thời điểm sẽ thấy chênh.

Năm tệp đã dựng lại và khớp hiện trạng: `sua_chuong2.docx` ·
`benchmark_chuong2.xlsx` (54 tiêu chí CT2 + 2 phát hiện ngoài chương, tách bạch
mẫu số) · `soat_giam_sat.xlsx` · `ma_tran_du_lieu.xlsx` (37 trường) ·
`kiem_chung_ban_chay.xlsx` (thêm trang "Buổi thử lần 2" và "Soi máy chủ").
