# Tách hai môn — TOÁN và TIẾNG ANH không đụng vào nhau

Ghi 2026-08-11. Đọc tệp này TRƯỚC khi thêm môn mới hay động vào `chung/`.

> **Đợt 1 XONG**: frontend đã tách, cổng `ranh_gioi.test.mjs` gác ranh giới.
> Cổng: **35 tệp · 1096 PASS · 0 FAIL**. Hành vi môn Toán KHÔNG đổi.
> **Đợt 2 CHƯA LÀM**: tách backend thành ba codebase và tách collection dữ liệu.

---

## CÂY THƯ MỤC — ba vùng, một chiều

```
src/
  App.jsx · main.jsx · soMon.js     VỎ — đăng nhập, kệ sách, giao màn cho môn
  chung/                            DÙNG CHUNG — mù hẳn về môn
    lib/     nenTang · taiKhoan · soQuyen · xephang · chuviet · nhanHocBa
    components/  KeSach · BangXepHang · ParentReport · TeacherBoard ·
                 HocSinhChiTiet · LoginScreen · ProfileSetup · ThanhTren …
  mon/toan/                         MÔN TOÁN — khép kín
    index.js     CỬA DUY NHẤT vỏ được nhìn vào
    lib/         flow · progress · hocba · adaptive · dau · noiDung · duLieu · sync
    components/  ManToan · HomeQuyen · LessonPlayer · ChuDe · MuaGiai …
  mon/tienganh/                     MÔN TIẾNG ANH — khung rỗng, dangCo: false
```

**Chiều phụ thuộc, và chỉ một chiều:**

```
vỏ  →  chung          ✓
vỏ  →  mon/<x>/index.js  ✓   (CHỈ cửa index.js, không vào ruột)
mon →  chung          ✓
chung → mon           ✗ CẤM
mon/toan ↔ mon/tienganh  ✗ CẤM
```

## VÌ SAO `chung/` PHẢI MÙ VỀ MÔN

Bốn màn nhìn nhiều môn một lượt — kệ sách · bảng xếp hạng · sổ bố mẹ · bảng cô giáo —
đều nằm ở `chung/`. Chỉ cần MỘT trong bốn màn ấy gọi thẳng vào Toán là chúng vĩnh
viễn không dựng nổi môn thứ hai, và mỗi lần thêm môn lại phải sửa cả bốn.

Nên `src/soMon.js` (nơi duy nhất gọi tên từng môn) đặt ở tầng **vỏ**, không ở `chung/`.
Đặt nhầm chỗ là luật ấy mất hiệu lực ngay.

## GIAO ƯỚC MỘT MÔN PHẢI NỘP

Khai đủ ở `mon/<môn>/index.js`; xem lời ghi trong `src/soMon.js`.

```
ma · ten · bieuTuong · dangCo · Man
cuaPhu[]                     lối vào không qua quyển nào (vd "Học theo chủ đề")
napTienDo · luuTienDo · gopTienDo · napTuMay
dsQuyen · tienDoQuyen        cho kệ sách
hocBa · hocBaCuaEm           cho sổ bố mẹ và bảng cô giáo — KHUÔN CỐ ĐỊNH
bangXepHang · lamMoiBangXepHang
bangCoGiao · lamMoiBangCoGiao · nhatKyCuaEm · napBanDoDang · tenDang · dangCuaBai
soMayChu · lamMoiSoMayChu
```

`tienDo` do **vỏ giữ** (để kệ sách và sổ bố mẹ cùng vẽ lại khi con học xong một bài)
nhưng vỏ **không bao giờ soi vào bên trong** — với vỏ nó là một khối đục.

## HAI LỖI ĐỢT NÀY DÍNH THẬT

**(a) `mon/*/lib/…` trong lời ghi đóng luôn khối chú thích.** Chuỗi `*/` nằm giữa
`/* … */` cắt khối ngay tại đó, phần còn lại của lời ghi thành mã. Viết
`mon/<môn>/lib/…`.

**(b) TÊN TREO sau khi xẻ tệp.** `loadLesson` gọi `THU_MUC_CUA` vốn ở lại nửa kia;
`export … from` chỉ chuyển tiếp ra ngoài chứ KHÔNG đưa tên vào phạm vi tệp. Cổng xanh
1 095 phép mà mở app ra là cả bốn quyển câm.

Cổng `ranh_gioi.test.mjs` nay **gọi thử từng hàm xuất ra** của mọi lõi và soi
`ReferenceError`. Nạp module thôi không bắt được — thân hàm chưa chạy. Và hàm `async`
không ném ra ngoài mà trả promise bị từ chối, nên phải bắt cả nhánh ấy (bản đầu của
chính cổng này nuốt mất, nên nó xanh trong khi `loadLesson` đang vỡ thật).

## ĐỢT 2 — CHƯA LÀM

1. **Ba codebase functions**: `functions/` (chung: OTP, hồ sơ) · `functions-toan/` ·
   `functions-ta/`. `deploy --only functions:ta` không đụng một hàm nào của Toán.
2. **Collection riêng** cho Tiếng Anh: `attemptsTA` · `progressTA` · `hocBaTA` ·
   `reportTA` · `bangXepHangTA` · `teacherBoardTA`, kèm khối luật Firestore riêng.
3. **Sửa `luat_o_nhap` cho hỏi MÔN** — làm TRƯỚC khi khai quyển Tiếng Anh vào sổ.
4. **Bộ chấm riêng** `mon/tienganh/lib/cham.js`, kèm cổng canh "Toán không đổi".
5. Cân nhắc thêm **ESLint `no-undef`** — nó chặn hẳn loại lỗi (b) ở mọi tệp, không
   chỉ ở lõi có hàm gọi khống được.

---

Xem thêm `docs/khao_sat_ban_do_tieng_anh.md` và `docs/khao_sat_tieng_anh.md`.
