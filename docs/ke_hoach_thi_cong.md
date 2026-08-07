# KẾ HOẠCH THI CÔNG — CLAUDE LÀM TRỌN GÓI
**Không dùng Gemini ở bất kỳ khâu nào** · Toán Tư Duy lớp 5 Quý 1 · lập ngày 03/08/2026

> Hệ quả kiến trúc của quyết định này: **runtime không cần API model nào**. Hình sinh sẵn lúc build,
> app chỉ đọc file tĩnh (JSON + PNG) → không phí API, không phụ thuộc mạng, không rủi ro model đổi hành vi.

---

## PHẦN A · HÌNH MIỀN CỤ THỂ — 14 lô, mỗi lô 1 chương (12 micro)

Hiện đã có 504 hình *khái niệm* (thẻ nguyên tắc · lời thoại · bậc thang · so sánh hai ngả).
Còn thiếu **hình miền có số liệu thật** — loại đắt nhất về mặt sư phạm vì con nhìn là hiểu ngay.

**Việc mỗi lô:** đọc `knowledgeCore` + `canonicalExamples` của 12 micro → chọn 1 nguyên mẫu miền phù hợp
(`plane_geometry` · `solid_3d` · `motion_track` · `clock_face` · `bar_diagram` · `balance_scale` · `grid_count` · `fraction_split`)
→ điền **số thật lấy từ ca mẫu** → render → soát contact sheet → sửa → ghi vào metadata.

| Lô | Chương | Bài | Nguyên mẫu miền dự kiến |
|---|---|---|---|
| A1 | C1 | B1–B4 | bar_diagram (sơ đồ đoạn thẳng), grid_count |
| A2 | C2 | B5–B8 | bar_diagram, fraction_split |
| A3 | C3 | B9–B12 | fraction_split, bar_diagram |
| A4 | C4 | B13–B16 | fraction_split, bar_diagram |
| A5 | C5 | B17–B20 | bar_diagram, balance_scale |
| A6 | C6 | B21–B24 | bar_diagram (tỉ số), grid_count |
| A7 | C7 | B25–B28 | bar_diagram, balance_scale |
| A8 | C8 | B29–B32 | bar_diagram, plane_geometry |
| A9 | C9 | B33–B36 | plane_geometry, grid_count |
| A10 | C10 | B37–B40 | balance_scale (%), bar_diagram |
| A11 | C11 | B41–B44 | plane_geometry (tam giác, thang) |
| A12 | C12 | B45–B48 | plane_geometry (tỉ số diện tích) |
| A13 | C13 | B49–B52 | plane_geometry (tròn), solid_3d (khối) |
| A14 | C14 | B53–B56 | motion_track, clock_face |

**Kết quả mỗi lô:** +12 đến +24 hình · cập nhật `figureSpec` trong DL json và km (append-only).
**Kết quả toàn phần A:** ~700 hình tổng, mỗi micro 4–5 hình, km lên v1.38.

---

## PHẦN B · LESSONPLAYER (React + TypeScript) — 4 lô

| Lô | Nội dung | Kết quả |
|---|---|---|
| B1 | Khung dự án Vite + Tailwind brand + `useLesson` đọc DL json + dựng flow 5 chặng | chạy được 1 micro |
| B2 | Component chặng GIẢNG + BÀI MẪU (TeachBlock, FigureView, SampleCard, WorkedExample) | học hết phần giảng |
| B3 | Component LUYỆN + SÁT HẠCH (hint 2 tầng, generator biến thể, mustPass, luật ≥2/3) | học trọn 1 micro |
| B4 | Điều hướng chuỗi 168 micro + 14 kỳ sát hạch chương + huy hiệu + sổ phụ huynh | học trọn 1 chương |

## PHẦN C · FIREBASE — 3 lô

| Lô | Nội dung |
|---|---|
| C1 | Firestore schema + luật bảo mật + offline persistence + ghi `attempts` |
| C2 | Cloud Function BKT (ngưỡng 0,85) + `reviewQueue` từ `spacedReview` |
| C3 | Chính sách adaptive + cổng `mustPass` + sổ phụ huynh tổng hợp đêm |

## PHẦN D · ĐÓNG GÓI — 1 lô
Repo hoàn chỉnh + `README` + lệnh deploy + checklist nghiệm thu.

---

## TỔNG: 22 lô — mỗi lần anh gõ "Tiếp" tôi làm một lô

**Quy tắc tôi tự đặt cho mình:**
1. Mỗi lô kết thúc bằng **file thật chạy được**, không phải mô tả.
2. Mỗi lô có **kiểm định tự động** + tôi **soát mắt** ảnh/giao diện, báo cáo trung thực lỗi tìm được.
3. Số liệu trong hình **luôn lấy từ ca mẫu trong sách** — không bịa số.
4. Lỗi phát hiện được sửa ở **renderer/luật chung**, không vá từng hình.
5. Cuối mỗi lô ghi metadata đồng bộ (DL json + km + manifest), đối soát 0 lỗi mới đóng lô.

**Giới hạn thật của tôi — nói trước để anh chủ động:**
- Tôi làm theo phiên, không chạy nền được. Việc phải chia lô và lưu ra file sau mỗi lô (đang làm đúng vậy).
- Với ~700 hình tôi soát mẫu ngẫu nhiên + contact sheet, không soi từng cái. Anh duyệt cuối vẫn là chốt chặn.
- Việc trên máy anh (tạo dự án Firebase, chạy `firebase deploy`) tôi không làm thay được — sẽ đưa lệnh chính xác.
