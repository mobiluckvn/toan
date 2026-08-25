#!/usr/bin/env python3
"""
XÁC NHẬN VÀ CHỈNH SỬA CHƯƠNG 2 — theo review của Thầy (25-08-2026).

Sinh `docs/xac_nhan_chuong2.docx`.

Khác `tools/sua_chuong2.py` ở chỗ nào: bản kia liệt kê 12 chỗ lệch giữa luận văn
và hệ thống. Bản này trả lời ĐÚNG CÂU HỎI CỦA THẦY — "xác nhận nội dung Chương 2
theo bốn phần: tổng quan · biểu diễn vấn đề · xử lý với một cá thể · các phương
pháp" — nên nó vừa soi CẤU TRÚC (thiếu mục nào so với khung Thầy nêu) vừa gộp lại
mọi chỗ phải sửa về nội dung, kể cả sáu chỗ MỚI tìm được ngày 25-08.

⚠ Sáu chỗ mới đều thuộc loại người phản biện đối chiếu được: ba mã nút minh hoạ
trong luận văn KHÔNG có thật trong đồ thị đang chạy, hoặc có thật nhưng nối bằng
loại cạnh mà chính hệ thống loại ra khỏi phép chẩn đoán.

Chạy lại là dựng lại — ĐỪNG sửa tay tệp .docx.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs" / "xac_nhan_chuong2.docx"


# ── khung Thầy yêu cầu, đối chiếu với mục đang có ────────────────────────────
KHUNG = [
    ("1. Tổng quan về học thích ứng",
     "2.1.1 Khái niệm và ba thế hệ · 2.1.2 Mô hình thích ứng đa chiều",
     "ĐỦ",
     "Giữ nguyên bố cục. Chỉ sửa số liệu ở 2.1.2 (xem C-4, C-5, C-7)."),

    ("2. Biểu diễn vấn đề (đồ thị tri thức)",
     "2.2.1 Đồ thị tri thức · 2.2.2 Ràng buộc tiên quyết",
     "ĐỦ NHƯNG SAI SỐ LIỆU",
     "Ba ví dụ mã nút đang sai (A-5, A-6). Phải nói rõ đồ thị có HAI bản: bản "
     "dựng và bản lúc chạy (B-1)."),

    ("3.a Xử lý với một cá thể — người học",
     "2.3.1 Bản sao số người học (Digital Twin)",
     "ĐỦ",
     "Bảng 2.1 đang bịa tên trường; phải khớp lược đồ thật hoặc khai rõ là mô "
     "hình khái niệm (A-7)."),

    ("3.b Xử lý với một cá thể — nhận biết hành vi",
     "Nằm rải ở 2.3.1c (nhóm T) và 2.5.2 (bốn nhóm dữ liệu lưu vết)",
     "THIẾU MỘT MỤC RIÊNG",
     "★ Thầy nêu đây là MỘT việc riêng. Đề nghị tách thành mục 2.3.4 — xem §2.1."),

    ("3.c Xử lý với một cá thể — chẩn đoán lỗ hổng",
     "2.3.2 BKT · 2.3.3 Lan truyền chẩn đoán trên đồ thị",
     "ĐỦ",
     "Sửa ngưỡng θ và các khoảng giá trị (A-1); công bố α, β (C-2)."),

    ("4.a Các phương pháp — tạo sinh",
     "2.4.1 LLM như gia sư · 2.4.2 Ảo giác từ vựng · 2.4.3 RAG",
     "ĐỦ NHƯNG MÔ TẢ SAI CƠ CHẾ",
     "Bước 3 của RAG không đảm bảo được bằng lời nhắc; cái làm nên con số ấy là "
     "tầng HẬU KIỂM (A-8). Và hệ thống là LAI, không thuần tạo sinh (B-4)."),

    ("4.b Các phương pháp — độ đo hiệu năng",
     "2.5.3 Giao thức A-R-A · ΔC · Đường cong học tập",
     "MỎNG",
     "★ Chỉ có hai độ đo, đều là độ đo SƯ PHẠM. Thiếu hẳn độ đo mô hình "
     "(AUC/RMSE), độ đo an toàn nội dung, độ đo hệ thống — xem §2.3."),

    ("4.c Các phương pháp — công nghệ sử dụng",
     "Không có mục nào",
     "THIẾU HẲN",
     "★ Cả Chương 2 không nhắc một tên công nghệ nào ngoài 'LLM'. Đề nghị thêm "
     "mục 2.6 — xem §2.2."),
]


# ── ba việc về cấu trúc ──────────────────────────────────────────────────────
CAU_TRUC = [
    ("2.1", "Tách “Nhận biết hành vi người học” thành mục riêng 2.3.4",
     [("VÌ SAO",
       "Thầy liệt kê ba việc song song khi “xử lý với một cá thể”: người học · "
       "nhận biết hành vi · chẩn đoán lỗ hổng. Chương 2 hiện có mục riêng cho "
       "việc thứ nhất (2.3.1) và việc thứ ba (2.3.2, 2.3.3), nhưng việc thứ hai "
       "thì nằm rải làm hai mảnh ở hai mục cách xa nhau: nhóm thuộc tính T trong "
       "2.3.1c, và bốn nhóm dữ liệu lưu vết trong 2.5.2. Người đọc không ghép "
       "lại được thành một phương pháp."),
      ("ĐỀ NGHỊ VIẾT GÌ",
       "Thêm mục 2.3.4 “Nhận biết hành vi người học”, gồm bốn tiểu mục: "
       "(a) phân loại hành vi quan sát được — trả lời, đoán lụi, bế tắc, nhận "
       "trợ giúp, bỏ dở, mệt mỏi, ưa định dạng; (b) tín hiệu đo được cho từng "
       "hành vi; (c) ngưỡng và cỡ mẫu tối thiểu; (d) giới hạn của từng phép suy "
       "luận. Phần thuật toán chi tiết để dành cho Chương 3 (mục 3.3)."),
      ("HỆ THỐNG ĐÃ CÓ GÌ ĐỂ VIẾT",
       "Đủ cả bảy hành vi. `CauHoi.jsx` đo `ms` từng lượt và đếm `hintsUsed`; "
       "`report.js::metMoi()` so nửa đầu với nửa cuối phiên TÁCH THEO ĐỊNH DẠNG; "
       "`report.js::stuckItems()` bắt câu làm ≥ 45 giây mà vẫn sai; "
       "`hoso.js` cộng bảng định dạng với chốt cỡ mẫu 8 lượt; `BaiHoc.jsx` ghi "
       "bản ghi `loai='phien'` mỗi lần bé rời màn giữa chừng.")]),

    ("2.2", "Bổ sung mục 2.6 “Công nghệ nền tảng sử dụng”",
     [("VÌ SAO",
       "Thầy nêu “công nghệ sử dụng” hai lần trong review — một lần ở phần chẩn "
       "đoán, một lần ở phần sinh bài. Chương 2 hiện không nêu tên một công nghệ "
       "cụ thể nào: không có cơ sở dữ liệu, không có mô hình ngôn ngữ cụ thể, "
       "không có bộ nhận dạng giọng nói, không có nền chạy hàm. Người phản biện "
       "sẽ hỏi “hệ thống này chạy trên cái gì” và luận văn chưa trả lời được."),
      ("ĐỀ NGHỊ VIẾT GÌ",
       "Mục 2.6 gồm bốn nhóm, mỗi nhóm nêu LỰA CHỌN và LÝ DO chọn: "
       "(a) tầng giao diện — React 18 + Vite 5, chạy được ngoại tuyến vì đồ thị "
       "rút gọn và học liệu đều nằm ở máy con; "
       "(b) tầng lưu trữ và xác thực — Firebase Authentication, Cloud Firestore "
       "với luật bảo mật khai theo trường, Firebase Hosting; "
       "(c) tầng tính toán phía máy chủ — Cloud Functions for Firebase trên "
       "Node.js 22, ba loại kích hoạt: theo tài liệu mới (`onDocumentCreated`), "
       "theo lịch (`onSchedule`) và theo lời gọi (`onCall`); "
       "(d) tầng trí tuệ nhân tạo — mô hình `openai/gpt-oss-120b` qua Groq cho "
       "sinh và chấm, Web Speech API của trình duyệt cho nhận dạng phát âm, "
       "Kokoro TTS cho giọng đọc dựng sẵn."),
      ("⚠ MỘT ĐIỀU PHẢI NÓI THẲNG",
       "Mỗi lựa chọn phải kèm GIỚI HẠN, vì mỗi lựa chọn đều có cái giá: "
       "Firestore không cho truy vấn theo đồ thị nên phép duyệt tiên quyết phải "
       "chạy ở máy con; Web Speech API phụ thuộc micro và mức ồn nên điểm phát "
       "âm của cùng một bé trên hai thiết bị có thể khác nhau; mô hình chạy qua "
       "dịch vụ ngoài nên không có gì bảo đảm phiên bản trọng số không đổi giữa "
       "hai lần đo — đó là lý do mỗi lượt phải mang vân tay lời nhắc.")]),

    ("2.3", "Mở rộng 2.5.3 thành hệ thống độ đo bốn nhóm",
     [("VÌ SAO",
       "Mục 2.5.3 hiện có đúng hai độ đo — ΔC và đường cong học tập — và cả hai "
       "đều đo TIẾN BỘ SƯ PHẠM. Không có độ đo nào trả lời được ba câu hỏi mà "
       "hội đồng chắc chắn hỏi: (1) mô hình BKT dự đoán có đúng không; (2) tầng "
       "chống ảo giác từ vựng chặn được bao nhiêu phần trăm; (3) hệ thống chạy "
       "có kịp không."),
      ("ĐỀ NGHỊ VIẾT GÌ",
       "Chia 2.5.3 thành bốn nhóm: "
       "(a) độ đo MÔ HÌNH — AUC, RMSE và độ chính xác trên bài toán dự đoán lượt "
       "kế tiếp, đo bằng cách chạy lại nhật ký; "
       "(b) độ đo SƯ PHẠM — ΔC của giao thức A-R-A, độ dốc đường cong học tập, "
       "số lượt trung bình tới ngưỡng thạo, tỉ lệ nút thạo trên mỗi khối lớp; "
       "(c) độ đo AN TOÀN NỘI DUNG — tỉ lệ câu sinh chứa từ ngoài vốn (OOV), tỉ "
       "lệ bị hậu kiểm bác, tỉ lệ phải lùi về câu dựng sẵn; "
       "(d) độ đo HỆ THỐNG — độ trễ đầu-cuối một lượt sinh, tỉ lệ lượt ghi được "
       "lên máy chủ, số bản ghi kẹt trong hàng đợi tại máy. "
       "Chi tiết công thức và cách đo để ở Chương 3 mục 3.6."),
      ("MỘT LƯU Ý VỀ THỨ TỰ",
       "Nhóm (d) sinh ra từ một bài học đắt: ngày 23-08-2026 phát hiện mỗi phiên "
       "học chỉ có bản ghi ĐẦU TIÊN lên được máy chủ. Mọi độ đo của ba nhóm trên "
       "đều đứng trên giả định “nhật ký đầy đủ”, mà giả định ấy đã sai suốt một "
       "thời gian dài và không có độ đo nào phát hiện ra. Nhóm (d) là chỗ luận "
       "văn tự bảo vệ mình.")]),
]


# ── các mục phải sửa ─────────────────────────────────────────────────────────
def M(ma, muc, tieu_de, dang, sua, bang_chung):
    return dict(ma=ma, muc=muc, tieu_de=tieu_de, dang=dang, sua=sua, bc=bang_chung)


NHOM_A = [
    M("A-1", "2.3.2 · 2.3.3 · 2.5.1",
      "Ngưỡng tinh thông θ và cả ba khoảng giá trị đi kèm",
      "Luận văn đặt θ = 0,95, vùng tịnh tiến 0,6 ≤ P(L) < 0,95, ngưỡng cảnh báo "
      "lan truyền ngược P(L) < 0,6. Cả ba con số đều không khớp hệ thống đang chạy.",
      "“Ngưỡng tinh thông đặt θ = 0,85, hiệu chỉnh bằng thực nghiệm trên chính "
      "bộ tham số BKT của hệ thống. Với P(L₀) = 0,10 · P(T) = 0,08 · P(S) = 0,10 "
      "· P(G) = 0,30, ngưỡng 0,85 tương ứng với khoảng bốn câu đúng liên tiếp mới "
      "công nhận là thạo, và một câu sai sau đó kéo mức thạo tụt xuống dưới "
      "ngưỡng. Không gian trạng thái chia làm bốn vùng theo hai ngưỡng: "
      "vùng YẾU P(L) < 0,30 — luyện thêm cùng kiểu câu không gỡ được, cần phụ "
      "đạo; vùng PHÁT TRIỂN GẦN 0,30 ≤ P(L) < 0,85 — chỗ luyện tập đổi được "
      "nhiều nhất; vùng THẠO P(L) ≥ 0,85; và vùng CHƯA CÓ SỐ LIỆU, cố ý tách "
      "riêng chứ không quy về 0. Bộ tham số cũ theo tài liệu (P(L₀) = 0,25 · "
      "P(G) = 0,20) tuyên bố thạo chỉ sau hai câu đúng — quá dễ dãi với học sinh "
      "tiểu học.”",
      "`web/functions/src/bkt.js:13–14` — `DEFAULT_PARAMS` và "
      "`MASTERY_THRESHOLD = 0.85`. `web/src/mon/tienganh/lib/zpd.js:34,37` — "
      "`NGUONG_THAO = 0.85`, `NGUONG_YEU = 0.3`. Ngưỡng lấy từ MỘT chỗ rồi "
      "chuyền đi, không gõ lại số ở nơi thứ hai. Chuỗi chạy thật, xuất phát từ "
      "P(L₀) = 0,10 với quan sát sai · đúng · đúng · đúng · sai · đúng · đúng: "
      "0,094 → 0,299 → 0,597 → 0,831 (ba đúng liền VẪN chưa đạt θ) → 0,459 (MỘT "
      "câu sai kéo tụt sâu) → 0,741 → 0,904 (đạt θ ở lượt thứ bảy). "
      "⚠ Bản `sua_chuong2.docx` ngày 23-08 ghi “tới lượt thứ tám mới đạt 0,903” "
      "— con số ấy ứng với một chuỗi quan sát khác và không nêu chuỗi, nên "
      "không tái lập được; bản này nêu rõ chuỗi. "
      "⚠ Giữ θ = 0,95 trong luận văn thì mọi con số của chương thực nghiệm sẽ "
      "không khớp với hệ thống đang chạy."),

    M("A-2", "2.5.2 (và phần mô tả dữ liệu của chương thực nghiệm)",
      "Dữ liệu thu được trước 23-08-2026 không dùng để phân tích được",
      "Luận văn mô tả một đường ống ghi nhận đầy đủ: mỗi lượt trả lời một bản ghi "
      "bất biến, mô hình người học dựng trên chuỗi bản ghi ấy.",
      "Thêm một đoạn vào phần mô tả dữ liệu: “Trong giai đoạn thử nghiệm, đường "
      "ống ghi nhận có hai khiếm khuyết đã được phát hiện và khắc phục ngày "
      "23-08-2026. Thứ nhất, do tương tác giữa quy tắc bất biến của kho sự kiện "
      "và cơ chế gửi theo lô, mỗi phiên học chỉ có bản ghi ĐẦU TIÊN lên được máy "
      "chủ. Thứ hai, cơ chế nhận lại dữ liệu học thử khi đăng nhập đã gán nhầm "
      "bản ghi của người học này sang người học khác. Toàn bộ dữ liệu đã được rà "
      "và làm sạch: 130 bản ghi sai chủ được gỡ bỏ, mô hình người học được dựng "
      "lại từ nguồn gốc bằng chính hàm cập nhật của hệ thống. Vì vậy số liệu "
      "dùng cho phân tích chỉ lấy từ sau mốc này.”",
      "Đo bằng khoá quản trị 23-08-2026. Kho `attempts` chỉ có 2 bản ghi môn "
      "Tiếng Anh cho hai buổi học khoảng mười lượt mỗi buổi. Nguyên nhân: "
      "`attempts` khai `allow update, delete: if false`, mà máy con mỗi lượt lại "
      "gửi lại cả phiên, còn `writeBatch` thì nguyên khối nên một bản ghi trùng "
      "làm rơi cả lô. Vá xong đo lại cùng một thao tác: 2 → 18. Bảy mã phiên bị "
      "hai người học cùng mang — chuyện không thể tự nhiên. Sau khi dọn: "
      "`attempts` 398 → 268, `mastery` 32 mục khớp tuyệt đối 32/32. "
      "⚠ NÓI RA LÀ ĐIỂM CỘNG, IM LÀ ĐIỂM TRỪ: người phản biện đối chiếu số liệu "
      "hai thời điểm sẽ thấy chênh; nói trước thì đó là bằng chứng của một quy "
      "trình kiểm soát dữ liệu có thật."),

    M("A-3", "2.3.2",
      "Phải nói rõ pha nào được tính vào BKT, pha nào không",
      "Luận văn viết BKT cập nhật mức tinh thông sau mỗi lượt trả lời của người "
      "học — đọc như thể mọi tương tác đều vào mô hình.",
      "“Mức tinh thông chỉ cập nhật từ những lượt người học TỰ trả lời: luyện "
      "tập (`practice`), sát hạch (`assess`), câu chốt nhanh sau một đoạn đọc "
      "(`check`) và câu xen giữa ví dụ mẫu (`worked`). Các bước hệ thống đang "
      "trình bày lời giải — giới thiệu, làm mẫu, giảng — không được tính, vì ở "
      "đó người học chưa đưa ra câu trả lời nào của mình; tính vào là ghi công "
      "cho người khác.”",
      "`web/functions/index.js` — danh sách trắng bốn pha trong `onAttempt`. "
      "Trước 23-08-2026 hàm nền chỉ nhận `practice` và `assess`, nên bỏ trắng "
      "513/1654 câu, tức 31% số câu người học thực làm. ⚠ Một chú thích trong mã "
      "từng khẳng định hai pha kia “chỉ môn Tiếng Anh phát” — sai, đo trên máy "
      "chủ có 49 lượt môn Toán mang chúng. Cổng `pha_vao_bkt.test.mjs` nay đọc "
      "thẳng từ mã nguồn xem mỗi môn phát ra pha nào."),

    M("A-4", "2.3.1",
      "“CEFR hiện tại của người học” đo PHỦ VỐN, không đo năng lực",
      "Luận văn xếp “Mức độ CEFR hiện tại” vào nhóm thuộc tính M của hồ sơ, đặt "
      "cạnh `p_learned` và `RT_avg` — tức đọc như một đại lượng đo được từ hành vi.",
      "“Mức CEFR của người học được suy ra từ mô hình năng lực theo một quy ước "
      "bắc cầu hai nhịp. Nhịp thứ nhất do hệ thống đo: với mỗi khối lớp, tính tỉ "
      "lệ số nút tri thức mà người học đã đạt P(L) ≥ 0,85 trên TỔNG số nút học "
      "được của khối. Nhịp thứ hai lấy nguyên mục tiêu đã ấn định trong Chương "
      "trình giáo dục phổ thông 2018 môn Tiếng Anh: khối lớp 1–2 là chương trình "
      "làm quen (dưới Bậc 1), khối lớp 3–5 nhắm Bậc 1 tương đương A1. Hệ thống "
      "công nhận một bậc khi tỉ lệ phủ của khối đạt 60% và khối ấy có tối thiểu "
      "30 nút; chưa đạt thì hệ thống báo đúng tỉ lệ phủ hiện có chứ không quy ra "
      "bậc. ⚠ Đây KHÔNG phải phép đo theo chuẩn CEFR: CEFR định nghĩa bậc bằng "
      "mô tả năng lực làm được (can-do descriptors), không định nghĩa bằng số "
      "đơn vị kiến thức đã nắm. Nhịp thứ hai là quy ước của chương trình quốc "
      "gia, không phải kết quả đo của hệ thống.”",
      "`web/src/mon/tienganh/lib/cefr.js` — `KHOI`, `TOI_THIEU_NUT = 30`, "
      "`PHU_DAT = 0.6`. Mẫu số lấy 1 062 nút học được trên tổng 1 194 nút của đồ "
      "thị lúc chạy; 132 nút chứa (course · theme · unit · review · fun_time) bị "
      "loại vì chúng là ngăn xếp tổ chức. Ba lựa chọn phải bảo vệ được khi phản "
      "biện: ngưỡng phủ 60%, ngưỡng đáng tin 30 nút, và việc lấy mẫu số là TOÀN "
      "khối chứ không phải số nút đã chạm — lấy “đã chạm” thì một người học đúng "
      "5 nút và nắm cả 5 sẽ ra 100%, tức phép đo thưởng cho việc học ít. "
      "Cổng `cefr_quy_doi.test.mjs` (19 phép) khoá bốn chỗ này."),

    M("A-5", "2.2.1 · 2.2.2",
      "★ MỚI — Quy mô đồ thị và bản chất tập cạnh E đang khai sai",
      "Mục 2.2.1b viết: “cấu trúc chương trình Tiếng Anh tiểu học (từ lớp 1 đến "
      "lớp 5) được biểu diễn thành một Đồ thị tri thức G = (V, E)”. Mục 2.2.2b "
      "viết: “Tập hợp các Cạnh E đại diện cho các Ràng buộc tiên quyết”.",
      "Sửa hai chỗ. Thứ nhất về QUY MÔ: “Đồ thị tri thức được số hoá cho toàn bộ "
      "chương trình phổ thông từ lớp 1 đến lớp 12, gồm 3 989 nút và 7 602 cạnh; "
      "phần thuộc cấp tiểu học (lớp 1–5) là 1 189 nút. Việc số hoá vượt quá phạm "
      "vi tiểu học là có chủ ý — nó cho phép các cạnh tiên quyết xuyên cấp tồn "
      "tại thật thay vì bị cắt cụt ở ranh giới lớp 5.” Thứ hai về TẬP CẠNH: "
      "“Đồ thị là đồ thị CÓ NHÃN, G = (V, E, τ, λ) trong đó τ gán mỗi nút một "
      "trong 17 loại và λ gán mỗi cạnh một trong 29 loại quan hệ. Ràng buộc tiên "
      "quyết là một tập con: REQUIRES ⊂ E, gồm 583 cạnh trên tổng 7 602. Việc "
      "phân biệt này không phải chi tiết kỹ thuật mà là điều kiện đúng đắn của "
      "phép chẩn đoán — duyệt ngược trên toàn bộ E sẽ đi qua cả cạnh CONTAINS "
      "(3 336 cạnh, quan hệ cấu thành) và cho ra kết luận vô nghĩa kiểu ‘nguyên "
      "nhân em sai là vì em chưa nắm cả Unit 3’.”",
      "Đếm trực tiếp `data/ban_do_tieng_anh.json`, khối `statistics`: "
      "`total_nodes` 3 989 · `total_edges` 7 602 · `nodes_by_grade` trải từ lớp 1 "
      "tới lớp 12 · `edges_by_relation` có 29 loại, `REQUIRES` 583, `CONTAINS` "
      "3 336, `HAS_VOCABULARY` 849, `HAS_SLOT` 827. Trong mã, chính hệ thống đã "
      "làm đúng việc phân loại này: `doThi.js:33` khai "
      "`CANH_THAT = new Set(['ban_do','noi_bai'])` và mọi phép duyệt mặc định "
      "BỎ loại cạnh `trong_bai`."),

    M("A-6", "2.2.2c · 2.3.3c",
      "★ MỚI — Ba ví dụ minh hoạ mã nút không đúng với đồ thị đang chạy",
      "Mục 2.2.2c và 2.3.3c dùng bốn ví dụ cụ thể có mã nút. Đối chiếu với đồ "
      "thị thật thì: (1) nút `v_g1_u9_numbers` (“numbers 1 to 10” lớp 1) KHÔNG "
      "TỒN TẠI — cả đồ thị đầy đủ lẫn đồ thị lúc chạy đều không có nút số đếm "
      "nào ở lớp 1; (2) cặp `v_g2_u14_nineteen` ← `v_g2_u13_eleven` không có "
      "cạnh nối; cạnh thật là `v_g2_u14_eighteen` → `v_g2_u14_nineteen` và nó "
      "mang nhãn `trong_bai` — đúng loại cạnh mà hệ thống CỐ Ý loại khỏi phép "
      "chẩn đoán; (3) ví dụ ở 2.3.3c nói sai mẫu câu hỏi tuổi `sp_g3_u11_2` thì "
      "hệ thống lần ra nút số đếm lớp 2 `v_g2_u13_eleven` — thật ra tiên quyết "
      "của nút ấy là `sp_g3_u2_2`, không phải nút từ vựng nào.",
      "Thay bằng ba ví dụ ĐÃ ĐỐI CHIẾU, chép thẳng được: "
      "(a) Trục ngữ pháp xuyên lớp — “Để nắm mẫu hỏi–đáp về hoạt động đang diễn "
      "ra ở Lớp 2 (nút `sp_g2_u5_1`), người học bị ràng buộc bởi thể khẳng định "
      "của thì hiện tại tiếp diễn đã học ở Lớp 1 (nút `sp_g1_u11_1`). Đây là một "
      "trong 38 cạnh tiên quyết xuyên lớp của đồ thị lúc chạy, mang cờ "
      "`xuyen_lop: true`.” "
      "(b) Chuỗi chẩn đoán bốn bước — “Từ mẫu câu `sp_g3_u18_2`, phép duyệt "
      "ngược đi qua `sp_g3_u18_1` (bước 1) → `sp_g3_u5_1` (bước 2) → "
      "`sp_g3_u4_1` (bước 3) → `sp_g3_u3_2` (bước 4), tức chạm trần độ sâu "
      "sauToiDa = 4.” "
      "(c) Chuỗi chẩn đoán vượt lớp — “Người học sai mẫu hỏi tuổi ở Lớp 3 "
      "(`sp_g3_u11_2`), hệ thống lần ngược qua `sp_g3_u2_2` rồi `sp_g3_u1_1`, "
      "và tới bước thứ ba thì chạm nút chào hỏi của Lớp 2 (`sp_g2_greeting`) — "
      "vùng khủng hoảng kiến thức nằm ở lớp dưới đúng như giả thuyết của cơ chế "
      "lan truyền ngược.”",
      "Đối chiếu bằng cách nạp `web/public/content/tienganh/do_thi.json` rồi "
      "chạy đúng phép duyệt của hệ thống (`duyetNguoc` với `CANH_THAT`). "
      "⚠ Đây là loại lỗi người phản biện đối chiếu ĐƯỢC và bắt trong ba phút, vì "
      "mã nút là thứ tra cứu được. Sửa xong thì ngược lại: nó thành bằng chứng "
      "rằng luận văn viết từ hệ thống thật."),

    M("A-7", "2.3.1 · Bảng 2.1",
      "★ MỚI — Bảng 2.1 khai tên trường không có trong hệ thống",
      "Bảng 2.1 trình bày lược đồ JSON của Bản sao số với các trường "
      "`learner_id`, `knowledge_overlay`, `p_learned`, `struggle_count`, "
      "`last_interacted`. Không trường nào trong số này tồn tại trong hệ thống; "
      "và mã học sinh mẫu `SV_20242344M` có dạng mã học viên cao học, không phải "
      "mã người học tiểu học.",
      "Hai lối, chọn một. Lối GỌN: giữ Bảng 2.1 nhưng ghi rõ dưới bảng “Bảng "
      "trình bày lược đồ khái niệm; tên trường trong hiện thực và ánh xạ tương "
      "ứng xem Chương 3, mục 3.2.4”, rồi Chương 3 đưa lược đồ thật. Lối MẠNH "
      "HƠN: thay thẳng Bảng 2.1 bằng lược đồ thật của tài liệu "
      "`mastery/{uid}/units/{maNut}` — `p` (mức thạo sau lượt gần nhất), "
      "`pTruoc` (mức thạo trước lượt ấy, để tính ΔC), `mastered`, `nAttempts`, "
      "`nCorrect`, `saiLienTiep`, `msTrungBinh` (RT_avg), `goiTrungBinh` "
      "(H_req), `lastSeen`, `lastMicroId`, `unit`, `mon`, `maNutDs` — kèm một "
      "cột “ứng với ký hiệu nào trong mô hình toán học”. Tôi nghiêng về lối thứ "
      "hai: một bảng lược đồ thật, có ánh xạ sang ký hiệu, mạnh hơn hẳn một bảng "
      "minh hoạ.",
      "`web/functions/src/bkt.js::applyAttempt()` — vật trả về chính là hình "
      "dạng tài liệu được ghi. `web/functions/index.js::onAttempt` bổ sung thêm "
      "bốn trường `unit` · `learnerId` · `mon` · `maNutDs` khi ghi."),

    M("A-8", "2.4.3 bước 3",
      "“Đảm bảo 100% không chứa từ vựng lạ” — đúng kết quả, sai cơ chế",
      "Luận văn viết: “Nhờ có các giới hạn từ Bước 2, kết quả tạo sinh đảm bảo "
      "100% không chứa từ vựng lạ vượt cấp.” Tức là gán cho LỜI NHẮC cái công "
      "mà lời nhắc không làm được.",
      "“Kiến trúc bảo đảm ràng buộc từ vựng bằng HAI tầng chứ không bằng một. "
      "Tầng thứ nhất là lời nhắc có ràng buộc, đóng vai trò định hướng. Tầng thứ "
      "hai là HẬU KIỂM tất định chạy tại máy người học: mỗi câu do mô hình sinh "
      "ra được đối chiếu lại với vốn từ hợp lệ, và chỉ được nhận nếu thuộc một "
      "trong năm lớp — một từ trong vốn, một câu nghi thức lớp học thuộc danh "
      "sách cố định, một câu ví dụ của bài, một câu sẵn của sách giáo khoa, hoặc "
      "một công thức đã điền đúng LOẠI ô trống. Câu không qua được bị thay bằng "
      "câu do chính máy con dựng từ dữ liệu bài. Việc tách hai tầng là bắt buộc: "
      "lời nhắc là thứ mô hình CÓ THỂ theo, không phải thứ mô hình BUỘC phải "
      "theo, nên chỉ tầng thứ hai mới cho ra một bảo đảm phát biểu được.”",
      "`web/src/mon/tienganh/lib/phongnoi.js:679 cauHopLe()` và `:741 "
      "cauThayThe()`; `goiPhongNoi.js:97,124` gọi hậu kiểm ở cả hai nhánh; "
      "`phudao.js:97` hậu kiểm từng câu một, kể cả câu tĩnh. Hai lần đã trả giá "
      "cho việc tin lời nhắc: mô hình sinh “Bye, bike.” sau khi được dặn rõ ô ấy "
      "là chỗ của TÊN NGƯỜI, và nói lặp y một câu ngay sau khi được dặn “đừng "
      "lặp”. ⚠ Mô tả đúng thì luận văn MẠNH HƠN — vì hai tầng là một đóng góp "
      "thiết kế, còn “prompt đảm bảo 100%” là một câu không ai tin."),
]


NHOM_B = [
    M("B-1", "2.2.1d",
      "Đồ thị làm bộ truy xuất — phải phân biệt bản DỰNG và bản LÚC CHẠY",
      "Luận văn mô tả đồ thị đóng vai trò bộ truy xuất (Retriever) cho RAG, với "
      "quy mô toàn bộ chương trình.",
      "“Đồ thị tồn tại ở hai bản phục vụ hai khâu khác nhau. Bản ĐẦY ĐỦ (3 989 "
      "nút · 7 602 cạnh) dùng ở khâu dựng học liệu, chạy ngoại tuyến. Bản LÚC "
      "CHẠY (1 194 nút · 253 cạnh, 127 KB trên đĩa và khoảng 21 KB khi truyền) được cắt ra và nạp về máy người "
      "học; nó CHỈ giữ QUAN HỆ, không giữ nhãn, nghĩa hay ví dụ — vì học liệu đã "
      "mang sẵn phần chữ nghĩa, chép lại là nhân đôi dữ liệu và sớm muộn hai bản "
      "lệch nhau. 253 cạnh gồm 195 cạnh tiên quyết của bản đồ gốc, 5 cạnh bắc "
      "cầu giữa hai bài của cùng một nhóm từ vựng có thứ tự, và 53 cạnh thứ tự "
      "đọc trong cùng một bài; nhóm thứ ba KHÔNG phải ràng buộc tiên quyết và bị "
      "loại khỏi mọi phép duyệt chẩn đoán. Kích thước nhỏ là điều kiện để phép "
      "chẩn đoán chạy được ngay trên máy, không cần gọi máy chủ — tính chất này "
      "quan trọng với người dùng là học sinh tiểu học, nơi đường truyền không "
      "phải lúc nào cũng có.”",
      "Đếm trực tiếp hai tệp; bộ cắt là `tools/xuat_do_thi_con.py`. Phân bố loại "
      "cạnh của bản lúc chạy: `ban_do` 195 · `trong_bai` 53 · `noi_bai` 5. "
      "⚠ SỬA LẠI SO VỚI BẢN 23-08: con số “80 KB” trong `sua_chuong2.docx` và "
      "trong chú thích ở `lib/doThi.js` là SAI. Đo lại ngày 25-08: tệp "
      "`do_thi.json` nặng 127 KB trên đĩa (nén gọn cũng 127 KB vì nó đã không có "
      "khoảng trắng thừa), và khoảng 21 KB khi truyền qua mạng nhờ nén gzip. "
      "Luận văn nên dùng cặp số 127 KB / 21 KB, vì cả hai đều đo được và mỗi số "
      "trả lời một câu hỏi khác nhau: 127 KB là thứ chiếm bộ nhớ khi duyệt, "
      "21 KB là thứ người dùng phải tải. Đồ thị đầy đủ là 3,4 MB, không phải "
      "3,1 MB."),

    M("B-2", "2.2.1d · 2.4.3 bước 1",
      "Bộ truy xuất GỘP hai nguồn, không chỉ tra đồ thị — và đây là kết quả đo",
      "Luận văn mô tả bộ truy xuất trích một đồ thị con chứa đúng chủ đề, từ "
      "vựng và cấu trúc câu của bài hiện tại.",
      "“Bộ truy xuất hợp nhất hai nguồn trả lời hai câu hỏi khác nhau: cửa sổ "
      "tuần tự (tối đa ba bài liền trước mà người học ĐÃ ĐẠT) trả lời “người học "
      "vừa học gì”, còn phép duyệt ngược theo cạnh tiên quyết trả lời “bài này "
      "dựng trên gì”. Việc hợp nhất — thay vì thay thế — là kết quả của một phép "
      "đo trên toàn bộ 94 bài: cửa sổ tuần tự BỎ SÓT tiên quyết ở 40 bài, trong "
      "đó 2 bài có tiên quyết nằm ở quyển khác mà cửa sổ không bao giờ với tới; "
      "nhưng nếu THAY hẳn bằng đồ thị thì 87/94 bài có vốn từ hẹp đi và nhiều "
      "bài về rỗng, vì phần lớn nút từ vựng không có cạnh tiên quyết nào — trong "
      "đồ thị lúc chạy chỉ 150/1 194 nút có ít nhất một tiên quyết. Cả hai nguồn "
      "đều lọc qua điều kiện người học ĐÃ ĐẠT bài chứa nút ấy: bài chưa đạt thì "
      "vốn từ của nó không được vào, kể cả khi đồ thị nói bài hiện tại cần nó.”",
      "`web/src/mon/tienganh/lib/phongnoi.js:169 vonTu()` và "
      "`doThi.js:162 baiTienQuyet()`. Con số 150/1 194 đếm trực tiếp trên tập "
      "cạnh `ban_do` + `noi_bai` của đồ thị lúc chạy. ⚠ Đây là chỗ ĐO TRƯỚC KHI "
      "LÀM đã lật ngược thiết kế ban đầu — đáng viết vào luận văn như một kết "
      "quả, không phải giấu đi như một lần đổi ý."),

    M("B-3", "2.5.2 nhóm Bối cảnh hệ thống",
      "“Mã prompt để kiểm toán” — băm KHUNG, không lưu nội dung",
      "Luận văn liệt kê “mã ID của câu lệnh Prompt” trong nhóm Bối cảnh hệ thống, "
      "đọc như thể mỗi bản ghi mang mã của lời nhắc đã sinh ra nó.",
      "“Bản ghi sự kiện mang vân tay của KHUNG lời nhắc — gồm mã mẫu, số phiên "
      "bản do người sửa khai tay, và mã băm 12 ký tự của phần khung — chứ không "
      "lưu nội dung lời nhắc đã sinh. Phần thay đổi theo từng người học (tên, "
      "vốn từ của bài, lịch sử hội thoại, bài viết) bị loại ra TRƯỚC khi băm. "
      "Nhờ thế hai người học khác nhau cùng học một bài cho ra CÙNG một vân tay "
      "— đó vừa là điều làm phép so sánh giữa các mẫu lời nhắc có nghĩa, vừa là "
      "điều làm vân tay không lần ra được cá nhân nào. Việc gom dữ liệu để so "
      "hiệu quả thì theo SỐ PHIÊN BẢN chứ không theo mã băm, vì băm đổi cả khi "
      "sửa một lỗi chính tả; mã băm dùng để phát hiện lệch ngoài ý muốn.”",
      "`web/functions/src/vantay.js` — `vanTay()`, `PHIEN_BAN_MAU`, `locKhung()`; "
      "`chamviet.js:127 khungCham()` dựng khung bằng chính hàm dựng lời nhắc với "
      "dữ liệu rỗng. Ba trường `mauPrompt` · `phienBanMau` · `vanTayPrompt` vào "
      "bản ghi tại `suKien.js:182–184`. ✅ Đã soi thấy trên máy chủ 23-08-2026: "
      "một lượt bài viết mang `mauPrompt=chamviet` · `phienBanMau=1` · "
      "`vanTayPrompt=1c85246bffac`."),

    M("B-4", "2.4.1 · 2.1.1 (thế hệ thứ ba)",
      "★ MỚI — Hệ thống là LAI, và cần khai là lai chứ không phải thuần tạo sinh",
      "Mục 2.1.1 mô tả thế hệ thứ ba là chuyển từ “lựa chọn” bài tập có sẵn sang "
      "“tạo sinh” nội dung mới theo thời gian thực; mục 2.4.1 nói LLM tạo sinh "
      "nội dung cá nhân hoá trên quy mô lớn. Hệ thống đang chạy KHÔNG làm như "
      "vậy, và không làm như vậy là có lý do.",
      "Thêm một đoạn định vị vào cuối 2.4.1: “Hệ thống đề xuất chọn một vị trí "
      "LAI trên trục lựa chọn–tạo sinh, và việc chọn vị trí ấy là một quyết định "
      "thiết kế có căn cứ. Toàn bộ 4 226 câu hỏi của phần học chính (3 756 câu "
      "luyện tập ở bốn bậc độ khó và 470 câu sát hạch) được sinh TRƯỚC bằng bộ "
      "sinh tất định rồi đi qua 92 phép kiểm tự động trước khi tới tay người "
      "học. Mô hình ngôn ngữ lớn chỉ được gọi ở ba chỗ mà nội dung tĩnh không "
      "phục vụ được: bài phụ đạo sinh lúc chạy khi kho tĩnh không đủ câu cho nút "
      "gốc rễ, phòng luyện nói đối thoại, và chấm bài viết ngắn kèm giải thích "
      "lỗi. Lý do của ranh giới này thuộc về đối tượng người dùng: với học sinh "
      "6–11 tuổi, một câu hỏi sai hoặc một từ vượt cấp không phải phiền toái mà "
      "là dạy sai, và trẻ sẽ nhớ cái sai ấy. Nội dung tĩnh cho phép kiểm duyệt "
      "TRƯỚC, nội dung sinh lúc chạy thì chỉ kiểm được SAU. Do đó hệ thống đặt "
      "nội dung sinh lúc chạy ở đúng những chỗ mà giá trị cá nhân hoá vượt được "
      "rủi ro, và ở những chỗ ấy vẫn buộc mọi kết quả đi qua tầng hậu kiểm.”",
      "Đếm trực tiếp trên 94 tệp bài của năm quyển `ta1`–`ta5`: pools warmup "
      "2 220 · standard 626 · challenge 910 = 3 756 câu luyện; assessment 470 "
      "câu. Số cổng: 92 tệp `.mjs` trong `web/test/`. LLM được gọi ở "
      "`functions/index.js::chamViet` · `::luyenNoi`, và ở "
      "`lib/phudao.js::dungPhuDao` qua tham số `goiLLM`."),

    M("B-5", "2.5.1",
      "Hàm chính sách π — thứ tự xét, và điều kiện vượt ải",
      "Luận văn mô tả ba nhánh theo khoảng giá trị của P(L), tức đọc như thể P(L) "
      "là biến quyết định duy nhất.",
      "“Hàm chính sách xét ĐANG MẮC TRƯỚC mức thạo: nếu người học sai từ ba lần "
      "liên tiếp trở lên tại một nút thì chuyển sang can thiệp phụ đạo, bất kể "
      "P(L) đang là bao nhiêu. Lý do: P(L) là một trung bình có quán tính, còn "
      "chuỗi sai liên tiếp là tín hiệu tức thời và đáng tin hơn về trạng thái "
      "hiện tại — một người học có P(L) = 0,96 mà vừa sai ba câu liền thì con số "
      "trung bình không phải thứ đáng nghe. Ngưỡng ba (chứ không phải hai) cũng "
      "có lý do: sai hai lần liền là chuyện thường của việc học, cắt ngang ở đó "
      "thì mạch học bị ngắt liên tục. Nhánh Vượt ải xét ở mức BÀI chứ không mức "
      "nút, và đòi đủ ba điều kiện: người học đã đạt bài ấy, bài có ít nhất ba "
      "nút, và MỌI nút của bài đều đạt ngưỡng. Trong phép gộp ở mức bài, PHỤ ĐẠO "
      "THẮNG VƯỢT ẢI: một bài mười nút với chín nút vững và một nút đang mắc thì "
      "việc cần làm là gỡ nút ấy, không phải cho bay qua cả bài.”",
      "`web/src/mon/tienganh/lib/chinhsach.js` — `SAI_LIEN_TIEP_MAC = 3`, "
      "`viecTiepCuaNut()` xét `sai >= 3` trước khi xét `p`, `viecTiepCuaBai()` "
      "cho phụ đạo thắng, `duocVuotAi(..., {toiThieuNut: 3})`. Chạy thật: cùng "
      "p = 0,96 nhưng vừa sai ba lần thì kết quả là `phuDao`, không phải "
      "`vuotAi`."),

    M("B-6", "2.5.1",
      "★ MỚI — π KHUYẾN NGHỊ, không GÁC ĐƯỜNG: tách hai vai trò và nói rõ vì sao",
      "Mục 2.5.1 mô tả hàm chính sách như “bộ não điều phối, quyết định hành "
      "động tiếp theo của hệ thống”. Đọc thế thì π quyết cả việc người học có "
      "được đi tiếp hay không. Hệ thống KHÔNG làm vậy, và đây là chỗ đáng viết "
      "thành một đóng góp chứ không phải một chỗ lệch.",
      "“Hệ thống tách hai quyền quyết định vốn hay bị gộp làm một. Hàm chính "
      "sách π trả lời câu hỏi NÊN LÀM GÌ TIẾP — tịnh tiến, vượt ải hay phụ đạo — "
      "và kết quả của nó điều khiển việc chọn câu, chọn nút mục tiêu và việc gọi "
      "sinh bài phụ đạo. Nhưng câu hỏi CÓ ĐƯỢC ĐI TIẾP KHÔNG thì thuộc về một bộ "
      "luật riêng, và bộ luật ấy chỉ có một điều: người học đi tiếp được khi ĐÃ "
      "ĐẠT, HOẶC đã thử thật ít nhất hai lần. Vế thứ hai là lưới đỡ, và nó tồn "
      "tại vì một lý do sư phạm không thương lượng được: mô hình BKT có thể chấm "
      "sai, mà nếu quyền mở đường nằm trong tay mô hình thì một người học bị "
      "đánh giá nhầm sẽ kẹt vĩnh viễn ở một bài — không có cách nào tự thoát, và "
      "với trẻ nhỏ thì cái học được không phải môn học mà là ‘mình học kém’. "
      "Cùng một luật ‘đạt hoặc thử đủ hai lần’ được dùng lại nguyên vẹn ở ba "
      "tầng: mở bài kế tiếp, mở chặng kế tiếp, và cho phép để lại một câu làm "
      "sau. Bài đi vòng KHÔNG được ghi là đạt; nó nằm trong danh sách còn nợ, có "
      "nhãn riêng, và phải làm xong mới mở được kỳ ôn tập chương.”",
      "`web/src/mon/tienganh/lib/dandat.js` — `THU_TOI_THIEU = 2`, "
      "`moBai()`, `duocBoQua()`, `moKyOnTap()`; chú thích đầu tệp "
      "`chinhsach.js:15–23` nói rõ tệp này KHÔNG thay `dandat.js`. ⚠ Không viết "
      "ra thì người phản biện đọc 2.5.1 sẽ hỏi đúng câu “nếu mô hình chấm sai "
      "thì đứa trẻ làm gì” — và luận văn đã có câu trả lời, chỉ là chưa nói."),
]


NHOM_C = [
    M("C-1", "2.5.2",
      "Nhịp ghi sự kiện — nói rõ là GOM LÔ theo phiên, và mã bản ghi lũy đẳng",
      "Luận văn mô tả “chuỗi sự kiện bất biến nối tiếp nhau trên trục thời gian”, "
      "không nói về nhịp ghi.",
      "“Sự kiện được ghi vào bộ nhớ tại máy ngay khi người học trả lời, nhưng "
      "chỉ được đẩy lên máy chủ theo LÔ. Mã định danh của mỗi bản ghi nhúng đủ "
      "năm thành phần — mã người học, mã phiên, mã bài, mã câu và SỐ THỨ TỰ của "
      "lượt trong phiên — nhờ đó việc dựng lại và gửi lại là thao tác lũy đẳng: "
      "một lượt cũ luôn ra đúng mã cũ, không sinh bản ghi trùng. Số thứ tự là "
      "thành phần không bỏ được: nếu đẩy từng lượt một thì số thứ tự luôn bằng 0 "
      "và mọi lượt của cùng một câu sẽ đè lên nhau, làm mất đúng thông tin mà "
      "nhật ký sinh ra để giữ — rằng người học sai hai lần rồi mới đúng.”",
      "`web/src/mon/tienganh/lib/suKien.js:123 maSuKien()` và "
      "`:145 dungSuKien()`."),

    M("C-2", "2.3.3",
      "Công bố hai hệ số α, β và công thức độ ngờ",
      "Luận văn nêu lan truyền ngược có hệ số suy giảm α và lan truyền xuôi có hệ "
      "số cộng hưởng β, nhưng không cho giá trị cũng không cho dạng công thức.",
      "“Hệ số suy giảm α = 0,6. Độ ngờ của một nút tiên quyết cách chỗ sai k "
      "bước được tính bằng doNgo = α^k × (1 − P(L)); cần cả hai thành phần — "
      "α^k vì càng xa chỗ sai thì càng khó gọi là nguyên nhân theo nghĩa dạy "
      "được, và (1 − P(L)) vì một nút người học đã vững thì không phải thủ phạm "
      "dù nó là tiên quyết. Nút chưa có số liệu được gán P(L) = P(L₀) = 0,10, "
      "tức rất đáng ngờ — một tiên quyết chưa từng chạm chính là lý do hay gặp "
      "nhất — nhưng không gán 0, vì ‘chưa có tin’ vẫn khác ‘đã đo và thấy hổng’. "
      "Phép duyệt có trần độ sâu bốn bước và loại bỏ những nút đã đạt ngưỡng "
      "thạo. Hệ số cộng hưởng β = 0,08: khi một nút đã đạt ngưỡng thạo, các nút "
      "dựng trên nó được cộng thêm (β / số bước) × P(L của nút nguồn), nhưng kết "
      "quả bị kẹp dưới NGƯỠNG_TRẦN = θ − 0,05 — tức cộng hưởng không bao giờ tự "
      "nó tuyên bố một nút là đã thạo. Ba chốt chống tuyên thạo khống: chỉ lan "
      "từ nút thật sự đã thạo, mức cộng nhỏ dần theo bước, và kết quả bị kẹp "
      "dưới trần.”",
      "`web/src/mon/tienganh/lib/lantruyen.js` — `ALPHA = 0.6`, `BETA = 0.08`, "
      "`NGUONG_TRAN = NGUONG_THAO - 0.05`, `P_MAC_DINH = 0.1`, `sauToiDa = 4`. "
      "Ví dụ chạy thật: nút p = 0,55 có nút trên đã thạo thì được nâng lên 0,63."),

    M("C-3", "2.1.2 chiều Thời gian",
      "Mệt mỏi nhận thức đo bằng HAI tín hiệu độc lập — nêu rõ giới hạn từng cái",
      "Luận văn nêu chiều Thời gian bao gồm đo mệt mỏi nhận thức, nhưng không nói "
      "đo bằng cách nào. Người phản biện sẽ hỏi ngay: mệt mỏi là trạng thái bên "
      "trong, phần mềm suy ra từ dấu hiệu quan sát được nào?",
      "“Chiều Thời gian được hiện thực bằng bốn thành phần: đường cong quên "
      "(hàm mũ, nửa đời 14 ngày), lịch lặp lại ngắt quãng theo hộp Leitner, và "
      "HAI tín hiệu độc lập cho mệt mỏi nhận thức. Tín hiệu thứ nhất — CHẬM DẦN "
      "TRONG PHIÊN: hệ thống so thời gian phản hồi trung bình nửa đầu với nửa "
      "cuối của cùng một phiên học, TÁCH RIÊNG THEO TỪNG ĐỊNH DẠNG câu hỏi, và "
      "chỉ kết luận khi mỗi nửa có tối thiểu ba lượt; chậm hơn 25% thì báo là có "
      "dấu hiệu mệt. Việc tách theo định dạng là bắt buộc chứ không phải tinh "
      "chỉnh: bài học đi theo thang độ khó tăng dần nên câu cuối phiên vốn đã "
      "khó hơn câu đầu, so thẳng thì phiên nào cũng ra ‘mệt’ và điều đó phản ánh "
      "thiết kế bài học chứ không phản ánh người học. Tín hiệu thứ hai — BỎ DỞ: "
      "mỗi lần người học rời màn bài học khi chưa hoàn thành, hệ thống ghi một "
      "bản ghi gồm mã bài, chặng đang dở, số lượt đã làm và số giây đã ở trong "
      "bài; mỗi lần một bản ghi chứ không gộp, vì chính SỐ LẦN bỏ dở cùng một "
      "bài mới là tín hiệu. ⚠ Tín hiệu thứ hai có giới hạn phải nêu: chỉ ghi "
      "được khi người học rời màn qua thao tác trong ứng dụng; đóng thẳng trình "
      "duyệt thì không ghi được. Con số thu được là CẬN DƯỚI của số lần bỏ dở "
      "thật, dùng làm chỉ báo xu hướng chứ không phải phép đếm đầy đủ. Cả hai "
      "tín hiệu hiện được ĐO và báo cho phụ huynh, chưa dùng để tự động rút ngắn "
      "buổi học.”",
      "`web/functions/src/report.js` — `metMoi()`, `TOI_THIEU_MOI_NUA = 3`, "
      "`NGUONG_CHAM = 0.25`, gom theo `a.mode` trong từng phiên; "
      "`BaiHoc.jsx` ghi mục học bạ `loai='phien'` với bốn trường "
      "`microId` · `chang` · `soLuot` · `giay`. ✅ Đã soi thấy trên máy chủ "
      "23-08-2026: 5 bản ghi loại `phien`, cùng một bài bị bỏ dở 5 lần được đếm "
      "riêng từng lần (169 giây · 31 · 21 · 5 …) — đúng thiết kế."),

    M("C-4", "2.1.2 chiều Nhận thức",
      "Giới hạn của phép đo PHÁT ÂM",
      "Luận văn xếp năng lực nói vào chiều Nhận thức cùng các kỹ năng khác, không "
      "phân biệt nguồn của phép đo.",
      "“Điểm phát âm được chấm bằng bộ nhận dạng giọng nói sẵn có của trình duyệt "
      "(Web Speech API). Vì vậy con số này phụ thuộc chất lượng micro và mức ồn "
      "của môi trường: cùng một người học, hai thiết bị khác nhau có thể cho kết "
      "quả khác nhau. Hệ thống vẫn đưa điểm này vào mô hình người học, nhưng gắn "
      "nhãn riêng cho ba dạng lượt nói (`noiTu` · `noiCau` · `phongNoi`) để có "
      "thể tách ra khi cần một phép đo thuần nhất. Ràng buộc này cũng chi phối "
      "thiết kế điều hướng: không nút nào bị KHOÁ theo điểm phát âm — điều kiện "
      "là ‘đạt ngưỡng HOẶC đã thử thật hai lần’, vì trẻ nói ngọng, trẻ nói giọng "
      "địa phương và trẻ dùng micro rẻ đều có thể không bao giờ chạm ngưỡng.”",
      "`web/src/mon/tienganh/lib/nghenoi.js:23` dùng "
      "`window.SpeechRecognition || window.webkitSpeechRecognition`; "
      "`dandat.js:203 noiDuoc()` cho ba trạng thái `dat` · `thu` · `chua`, và "
      "`micHong` mở đường ngay khi thiết bị hỏng. ⚠ Nêu giới hạn này là điểm "
      "cộng về tính trung thực khoa học, không phải điểm trừ."),

    M("C-5", "2.1.2 chiều Sư phạm",
      "★ MỚI — “Liên tục thử nghiệm các định dạng” nói quá mức hệ thống làm",
      "Mục 2.1.2c viết hệ thống “liên tục thử nghiệm các định dạng khác nhau để "
      "tìm ra phương pháp truyền đạt tối ưu nhất tại từng thời điểm”. Câu ấy gợi "
      "một cơ chế thăm dò kiểu bandit. Hệ thống làm việc khiêm tốn hơn nhiều, và "
      "chỗ khiêm tốn ấy là có lý do.",
      "“Chiều Sư phạm được hiện thực bằng một hồ sơ định dạng: sáu định dạng câu "
      "hỏi (chọn đáp án · xếp thẻ thành câu · gõ lại chữ · đúng-sai · nghe rồi "
      "nhìn hình · nói theo), mỗi định dạng giữ một cặp (số câu đúng, tổng số "
      "câu) và chỉ những lượt trả lời ĐẦU của mỗi câu mới được tính — tính cả "
      "lượt thử lại thì định dạng nào cho phép thử nhiều lần sẽ có tỉ lệ đúng "
      "thấp hơn, mà đó là tính chất của định dạng chứ không phải của người học. "
      "Hồ sơ này được dùng làm KHOÁ XẾP PHỤ, không phải cơ chế chọn: nhóm vùng "
      "phát triển gần vẫn quyết định trước, chỉ trong cùng một nhóm mới xếp theo "
      "định dạng. Luật xếp đảo chiều theo vùng: ở chỗ người học đang chông chênh "
      "hoặc còn yếu thì đưa định dạng MẠNH lên trước, để nội dung khó không "
      "chồng thêm một cách hỏi cũng khó; ở chỗ đã thạo thì đưa định dạng YẾU lên "
      "trước, vì đó là chỗ rẻ nhất để tập một cách hỏi còn ngại. Hệ thống KHÔNG "
      "đổi tỉ lệ các định dạng trong một bài và KHÔNG bỏ câu nào — chỉ đổi thứ "
      "tự — vì số câu là cơ sở của phép chấm và sổ tiến độ. Mọi kết luận về định "
      "dạng đều đòi tối thiểu 8 lượt; dưới ngưỡng ấy hệ thống trả về ‘chưa biết’ "
      "chứ không trả về ‘kém’, vì một nhãn ‘kém’ dựng trên hai lượt sẽ dẫn tới "
      "việc cho ít câu dạng ấy đi, nên mẫu không bao giờ lớn thêm và cái nhãn "
      "sai tự nuôi chính nó.”",
      "`web/src/mon/tienganh/lib/hoso.js` — `TOI_THIEU_MAU = 8`, "
      "`TEN_DINH_DANG` sáu mục, `tiLeDung()` trả `null` dưới ngưỡng, "
      "`yeuNhat()` đòi ít nhất hai định dạng đủ mẫu; "
      "`zpd.js:95 hangDinhDang()` là chỗ đảo chiều theo vùng; "
      "`ManTiengAnh.jsx:266` chỉ đếm lượt `lan === 1`."),

    M("C-6", "2.3.2 · 2.1.2 chiều Thời gian",
      "★ MỚI — Cơ chế quên: cho dạng công thức, và nói rõ nó kéo về đâu",
      "Luận văn trích Nedungadi & Remya (2014) cho cơ chế quên nhưng không cho "
      "dạng hàm, không cho tham số, và không nói mức thạo tụt về đâu.",
      "“Trước khi cập nhật Bayes, mức thạo cũ được điều chỉnh theo số ngày kể từ "
      "lần chạm gần nhất: P′(L) = 0,5 + (P(L) − 0,5) · 2^(−Δt / h), với h là nửa "
      "đời trí nhớ, đặt h = 14 ngày. Điểm cần nhấn: hàm kéo mức thạo về 0,5 chứ "
      "KHÔNG về 0. Đây là lựa chọn có hệ quả hai chiều và cả hai đều đúng theo "
      "nghĩa mô hình. Chiều thứ nhất: người học quên thì trạng thái trở thành "
      "‘không chắc’, chứ không thành ‘chưa từng biết’ — kéo về 0 là bắt học lại "
      "từ đầu một thứ đã từng thạo, và với trẻ nhỏ thì đó là hình phạt cho việc "
      "nghỉ vài hôm. Chiều thứ hai, nghe ngược đời nhưng là hệ quả đúng: một nút "
      "từng sai nhiều (P(L) thấp) sẽ NHÍCH LÊN theo thời gian, vì cái phân rã ở "
      "đây là ĐỘ TIN CẬY của hệ thống vào hiểu biết hiện có về người học, chứ "
      "không phải năng lực của người học. Bản ghi đời cũ không có dấu thời gian "
      "thì không phân rã — thà không phân rã còn hơn phân rã theo một mốc bịa "
      "ra. ⚠ Con số h = 14 ngày là con số CHỌN theo lịch ôn sẵn có (+1 · +3 · +7 "
      "ngày) chứ không phải con số hiệu chỉnh từ dữ liệu; luận văn phải khai như "
      "vậy, và việc hiệu chỉnh h là một trong các kịch bản thực nghiệm đề xuất "
      "ở Chương 3.”",
      "`web/functions/src/bkt.js:56 NUA_DOI_NGAY = 14` và `:69 quenDan()`; "
      "chú thích tại chỗ đã ghi rõ đây là con số chọn, chưa hiệu chỉnh."),

    M("C-7", "2.3.2",
      "★ MỚI — Câu BẮT BUỘC ĐÚNG dùng bộ tham số BKT riêng",
      "Luận văn trình bày bốn tham số BKT như một bộ duy nhất cho mọi câu hỏi.",
      "“Bốn tham số không đồng nhất trên mọi câu hỏi. Những câu được người soạn "
      "đánh dấu BẮT BUỘC ĐÚNG — các câu bẫy đặt đúng vào chỗ hiểu sai phổ biến — "
      "dùng bộ tham số riêng với P(G) = 0,15 và P(S) = 0,06 thay cho 0,30 và "
      "0,10. Căn cứ: trả lời đúng một câu bẫy nhờ đoán thì khó hơn hẳn, nên tín "
      "hiệu quan sát được ở đó đáng tin hơn; đối xứng lại, sai một câu bẫy kéo "
      "mức thạo xuống mạnh hơn sai một câu thường. Đây là một dạng cá thể hoá "
      "tham số theo ITEM chứ không theo người học, rẻ hơn nhiều so với việc ước "
      "lượng tham số riêng cho từng người mà vẫn nắm được phần lớn khác biệt "
      "giữa các câu hỏi.”",
      "`web/functions/src/bkt.js:41 paramsFor()`. Trường `mustPass` trên câu "
      "hỏi, và `report.js::topTraps()` dùng chính trường ấy để chỉ ra ‘bẫy hay "
      "sập nhất’ cho phụ huynh."),

    M("C-8", "2.5.2",
      "★ MỚI — Bốn bất biến mà một kho lưu vết học tập phải giữ",
      "Mục 2.5.2 mô tả kiến trúc lưu vết hướng sự kiện ở mức nguyên lý (bất biến, "
      "chuỗi thời gian, bốn nhóm dữ liệu) nhưng không nêu điều kiện đúng đắn nào "
      "kiểm tra được. Đây chính là chỗ hệ thống đã hỏng nặng nhất mà mọi phép "
      "kiểm khác đều báo xanh.",
      "Thêm một tiểu mục: “Kiến trúc lưu vết hướng sự kiện chỉ có giá trị nếu "
      "kho sự kiện giữ được bốn bất biến, và bốn bất biến này phải kiểm tra được "
      "bằng phép chạy tự động chứ không bằng niềm tin vào mã nguồn: "
      "(1) MỖI PHIÊN MỘT CHỦ — một mã phiên chỉ sinh ở một lần mở bài của một "
      "người học, nên hai người học cùng mang một mã phiên là dấu hiệu dữ liệu "
      "đã bị gán nhầm chủ; "
      "(2) DÃY SỐ THỨ TỰ LIỀN — mã bản ghi nhúng số thứ tự của lượt trong phiên "
      "nên dãy phải liền; thủng là mất bản ghi giữa chừng. Phép kiểm phải nhóm "
      "theo bộ ba (người học · phiên · bài), không theo riêng mã phiên; "
      "(3) MÔ HÌNH SUY ĐƯỢC TỪ NHẬT KÝ — tổng số lượt ghi trong hồ sơ mỗi nút "
      "phải bằng đúng số bản ghi còn lại của nút ấy, và dựng lại hồ sơ từ nhật "
      "ký phải ra đúng hồ sơ đang có; "
      "(4) KHÔNG NÚT NÀO CÓ LƯỢT MÀ THIẾU HỒ SƠ — chiều ngược của (3), bắt được "
      "cảnh hàm nền bỏ sót một loại lượt. "
      "⚠ Bốn phép này không bắt được việc mất phần ĐUÔI: nếu mấy lượt cuối của "
      "một phiên không bao giờ lên máy chủ thì dãy số thứ tự vẫn liền, chỉ ngắn "
      "hơn thực tế. Muốn biết thì phải so với một nguồn độc lập hoặc đếm tay khi "
      "đi thử.”",
      "`tools/kiem_kho_du_lieu.mjs` hiện thực đủ bốn phép, chỉ đọc, không ghi. "
      "Mỗi phép bắt một họ lỗi ĐÃ XẢY RA THẬT ngày 23-08-2026. ⚠ Đây là chỗ luận "
      "văn có thể đóng góp một điều mà phần lớn tài liệu về event sourcing trong "
      "giáo dục không nói: bất biến phải kèm phép kiểm, vì kho sự kiện hỏng "
      "trong im lặng."),
]


TLTK_THIEU = [
    ("Vygotsky, L. S. (1978). Mind in Society: The Development of Higher "
     "Psychological Processes. Harvard University Press.",
     "Mục 2.1.2a dùng khái niệm Vùng phát triển gần (ZPD) làm căn cứ cho toàn bộ "
     "chiều Nhận thức, nhưng danh mục 11 tài liệu không có nguồn gốc của khái "
     "niệm này. Đây là chỗ hội đồng bắt trong một phút."),

    ("Bloom, B. S. (1984). The 2 Sigma Problem: The search for methods of group "
     "instruction as effective as one-to-one tutoring. Educational Researcher, "
     "13(6), 4–16.",
     "Mục 2.4.1 mở đầu bằng “Bài toán 2 Sigma” và nêu con số 98%, nhưng không có "
     "tài liệu tham chiếu. Cần bổ sung, và nhân tiện kiểm lại cách phát biểu: "
     "kết quả gốc là học sinh được kèm 1-1 đạt trên mức trung bình của lớp "
     "thường khoảng hai độ lệch chuẩn, tương ứng vượt khoảng 98% học sinh lớp "
     "thường — không phải “cao hơn 98%”."),

    ("Council of Europe (2020). Common European Framework of Reference for "
     "Languages: Learning, teaching, assessment — Companion volume. Council of "
     "Europe Publishing.",
     "Cả Chương 2 dùng thang CEFR làm ràng buộc cho tầng sinh nội dung và làm "
     "thuộc tính hồ sơ, nhưng không dẫn nguồn định nghĩa thang. Bắt buộc phải "
     "có, nhất là khi mục A-4 nói rõ phép quy đổi của hệ thống KHÔNG phải phép "
     "đo theo chuẩn CEFR — muốn nói được điều đó thì phải dẫn được chuẩn."),

    ("Bộ Giáo dục và Đào tạo (2018). Chương trình giáo dục phổ thông môn Tiếng "
     "Anh (ban hành kèm Thông tư số 32/2018/TT-BGDĐT).",
     "Nhịp thứ hai của phép quy đổi CEFR lấy nguyên mục tiêu khối lớp từ văn bản "
     "này. Không dẫn thì con số bậc năng lực không có căn cứ pháp lý nào."),

    ("Leitner, S. (1972). So lernt man lernen. Herder.",
     "Lịch lặp lại ngắt quãng của hệ thống dùng hộp Leitner với năm khoảng "
     "1 · 3 · 7 · 14 · 30 ngày. Settles & Meeder (2016) đã có trong danh mục "
     "nhưng đó là mô hình học được, không phải hộp cố định đang dùng."),

    ("Baker, R. S. J. d., Corbett, A. T., & Aleven, V. (2008). More accurate "
     "student modeling through contextual estimation of slip and guess "
     "probabilities in Bayesian Knowledge Tracing. In Intelligent Tutoring "
     "Systems (pp. 406–415). Springer.",
     "Cần cho mục C-7 (tham số P(S), P(G) thay đổi theo ngữ cảnh câu hỏi) và cho "
     "phần bàn về hiện tượng suy biến tham số khi hiệu chỉnh BKT — thứ mà kịch "
     "bản thực nghiệm hiệu chỉnh tham số ở Chương 3 phải phòng."),

    ("Ebbinghaus, H. (1885/1913). Memory: A Contribution to Experimental "
     "Psychology. Teachers College, Columbia University.",
     "Nguồn của đường cong quên. Mục 2.1.2b nói “hàm phân rã thời gian” mà không "
     "dẫn nguồn nào cho dạng hàm."),
]


UU_TIEN = [
    ("A-1", "Ngưỡng θ và ba khoảng giá trị", "2.3.2 · 2.3.3 · 2.5.1",
     "BẮT BUỘC", "Người phản biện đối chiếu mã là thấy ngay"),
    ("A-2", "Dữ liệu trước 23-08 không dùng được", "2.5.2 + chương thực nghiệm",
     "BẮT BUỘC", "Ảnh hưởng thẳng tới mọi con số của chương sau"),
    ("A-5", "Quy mô đồ thị và bản chất tập cạnh E", "2.2.1 · 2.2.2",
     "BẮT BUỘC", "Đếm được từ tệp dữ liệu"),
    ("A-6", "Ba ví dụ mã nút sai", "2.2.2c · 2.3.3c",
     "BẮT BUỘC", "Tra cứu được trong ba phút; đã có câu thay thế đối chiếu xong"),
    ("A-8", "RAG bước 3 — đúng kết quả, sai cơ chế", "2.4.3",
     "BẮT BUỘC", "Sửa xong thì mạnh hơn, vì hai tầng là một đóng góp"),
    ("A-3", "Pha nào vào BKT", "2.3.2", "CAO", "Liên quan 31% dữ liệu"),
    ("A-4", "CEFR là quy ước bắc cầu", "2.3.1", "CAO", "Tránh một câu hỏi khó"),
    ("A-7", "Bảng 2.1 khai tên trường không có", "2.3.1",
     "CAO", "Nên thay bằng lược đồ thật"),
    ("B-4", "Hệ thống là LAI, không thuần tạo sinh", "2.4.1 · 2.1.1",
     "CAO", "Định vị đóng góp; im thì thành chỗ yếu"),
    ("B-6", "π khuyến nghị, không gác đường", "2.5.1",
     "CAO", "Trả lời trước câu ‘nếu mô hình chấm sai thì sao’"),
    ("§2.2", "Thêm mục 2.6 Công nghệ sử dụng", "chương 2 (mục mới)",
     "CAO", "Thầy nêu đích danh, hiện thiếu hẳn"),
    ("§2.3", "Mở rộng 2.5.3 thành bốn nhóm độ đo", "2.5.3",
     "CAO", "Thầy nêu đích danh; hiện chỉ có độ đo sư phạm"),
    ("§2.1", "Tách mục 2.3.4 Nhận biết hành vi", "chương 2 (mục mới)",
     "TRUNG BÌNH", "Thầy nêu là việc riêng; nội dung đã có, chỉ gom lại"),
    ("B-1 · B-2 · B-3 · B-5", "Bốn chỗ hệ thống làm khác và làm tốt hơn", "2.2.1 · 2.4.3 · 2.5.1 · 2.5.2",
     "TRUNG BÌNH", "Sửa cho khớp thì luận văn mạnh lên"),
    ("C-1 … C-8", "Tám chỗ nói chung chung, cần con số cụ thể", "rải khắp chương",
     "TRUNG BÌNH", "Điều kiện để phần trình bày TÁI LẬP được"),
    ("TLTK", "Bảy tài liệu tham khảo còn thiếu", "danh mục cuối chương",
     "CAO", "Hai trong số đó (Vygotsky, Bloom) đang được TRÍCH mà không có mục"),
]


# ── dựng tài liệu ────────────────────────────────────────────────────────────
def do(p, chu, dam=False, mau=None, nghieng=False):
    r = p.add_run(chu)
    r.bold = dam
    r.italic = nghieng
    if mau:
        r.font.color.rgb = mau
    return r


def khoi(d, nhan, chu, mau_nhan=None):
    p = d.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    do(p, f"{nhan}: ", dam=True, mau=mau_nhan)
    do(p, chu)
    return p


def bang(d, dau_cot, hang, rong=None):
    t = d.add_table(rows=1, cols=len(dau_cot))
    t.style = "Light Grid Accent 1"
    for i, x in enumerate(dau_cot):
        o = t.rows[0].cells[i]
        o.text = ""
        do(o.paragraphs[0], x, dam=True)
    for h in hang:
        c = t.add_row().cells
        for i, x in enumerate(h):
            c[i].text = ""
            do(c[i].paragraphs[0], str(x))
    for r in t.rows:
        for o in r.cells:
            for p in o.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
    d.add_paragraph()
    return t


DO = RGBColor(0xB0, 0x22, 0x22)
XANH = RGBColor(0x1F, 0x5C, 0x2E)


def main() -> int:
    d = Document()
    d.styles["Normal"].font.name = "Times New Roman"
    d.styles["Normal"].font.size = Pt(12)

    t = d.add_heading("XÁC NHẬN VÀ CHỈNH SỬA CHƯƠNG 2", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s = d.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    do(s, "Đối chiếu khung Thầy yêu cầu với nội dung Chương 2 và hệ thống đang chạy",
       nghieng=True)

    p = d.add_paragraph()
    do(p, "Hệ thống đối chiếu: ", dam=True)
    do(p, "Kỹ Sư Nhí — ky-su-nhi.web.app, môn Tiếng Anh lớp 1–5\n")
    do(p, "Ngày lập: ", dam=True)
    do(p, "25-08-2026\n")
    do(p, "Căn cứ: ", dam=True)
    do(p, "bản Chương 2 `docs/Chuong2_Luan_van_Thac_sy_1_v3.docx`; bảng đối chiếu "
          "54 tiêu chí `docs/benchmark_chuong2.xlsx`; và một lượt rà lại mã nguồn "
          "cùng dữ liệu đang chạy ngày 25-08-2026.\n")
    do(p, "Quan hệ với tài liệu cũ: ", dam=True)
    do(p, "bản `docs/sua_chuong2.docx` (23-08) liệt kê 12 chỗ lệch. Tài liệu này "
          "gộp lại toàn bộ 12 chỗ ấy, sắp lại theo đúng bốn phần Thầy nêu, và bổ "
          "sung ")
    do(p, "sáu chỗ MỚI", dam=True, mau=DO)
    do(p, " tìm được ngày 25-08 — trong đó có ba mã nút minh hoạ không đúng với "
          "đồ thị đang chạy, là loại lỗi người phản biện tra cứu được.")

    d.add_heading("§1 · Đối chiếu khung Thầy yêu cầu với cấu trúc hiện có", level=1)
    d.add_paragraph(
        "Thầy chốt Chương 2 gồm bốn phần: tổng quan · biểu diễn vấn đề (đồ thị "
        "tri thức) · xử lý với một cá thể (người học, nhận biết hành vi, chẩn "
        "đoán lỗ hổng) · các phương pháp (tạo sinh, độ đo hiệu năng, công nghệ "
        "sử dụng). Bảng dưới đối chiếu từng phần với mục đang có.")
    bang(d, ["Thầy yêu cầu", "Mục hiện có", "Tình trạng", "Việc phải làm"], KHUNG)
    p = d.add_paragraph()
    do(p, "Kết luận §1: ", dam=True, mau=XANH)
    do(p, "khung Chương 2 hiện tại ĐÃ khớp với khung Thầy nêu ở sáu trên tám "
          "điểm, không phải viết lại bố cục. Hai điểm thiếu — “nhận biết hành "
          "vi” chưa có mục riêng và “công nghệ sử dụng” thiếu hẳn — cùng một "
          "điểm mỏng là phần độ đo hiệu năng. Ba việc ấy trình bày ở §2; phần "
          "còn lại là sửa nội dung, trình bày ở §3–§5.")

    d.add_heading("§2 · Ba việc về CẤU TRÚC", level=1)
    for so, ten, muc in CAU_TRUC:
        d.add_heading(f"{so}. {ten}", level=2)
        for nhan, chu in muc:
            khoi(d, nhan, chu, mau_nhan=DO if nhan.startswith("⚠") or nhan.startswith("★") else None)

    d.add_heading("§3 · NHÓM A — sai sự thật hoặc sai số liệu, buộc phải sửa", level=1)
    d.add_paragraph(
        "Mỗi mục gồm bốn phần: SỬA Ở ĐÂU · ĐANG VIẾT GÌ · SỬA THÀNH GÌ (câu thay "
        "thế đã viết sẵn, chép thẳng vào được) · VÌ SAO VÀ BẰNG CHỨNG (số đo lấy "
        "từ mã hoặc dữ liệu, kèm đường dẫn tệp). Dấu ★ đánh dấu mục MỚI tìm được "
        "ngày 25-08-2026.")
    for m in NHOM_A:
        d.add_heading(f"{m['ma']}. [Mục {m['muc']}] {m['tieu_de']}", level=2)
        khoi(d, "ĐANG VIẾT GÌ", m["dang"])
        khoi(d, "SỬA THÀNH GÌ", m["sua"], mau_nhan=XANH)
        khoi(d, "VÌ SAO — VÀ BẰNG CHỨNG", m["bc"])

    d.add_heading("§4 · NHÓM B — hệ thống làm khác, và làm tốt hơn mô tả", level=1)
    d.add_paragraph(
        "Những chỗ này không phải lỗi của hệ thống mà là chỗ luận văn mô tả một "
        "cách còn hệ thống làm một cách khác có căn cứ hơn. Sửa cho khớp thì "
        "luận văn mạnh lên, vì mỗi chỗ là một quyết định thiết kế bảo vệ được.")
    for m in NHOM_B:
        d.add_heading(f"{m['ma']}. [Mục {m['muc']}] {m['tieu_de']}", level=2)
        khoi(d, "ĐANG VIẾT GÌ", m["dang"])
        khoi(d, "SỬA THÀNH GÌ", m["sua"], mau_nhan=XANH)
        khoi(d, "VÌ SAO — VÀ BẰNG CHỨNG", m["bc"])

    d.add_heading("§5 · NHÓM C — nói chung chung, cần con số cụ thể", level=1)
    d.add_paragraph(
        "Tiêu chí của nhóm này là TÍNH TÁI LẬP: một người đọc luận văn có dựng "
        "lại được cơ chế ấy không. Chỗ nào chỉ nêu tên cơ chế mà không cho tham "
        "số, dạng hàm, ngưỡng hay cỡ mẫu tối thiểu thì xếp vào đây.")
    for m in NHOM_C:
        d.add_heading(f"{m['ma']}. [Mục {m['muc']}] {m['tieu_de']}", level=2)
        khoi(d, "ĐANG VIẾT GÌ", m["dang"])
        khoi(d, "SỬA THÀNH GÌ", m["sua"], mau_nhan=XANH)
        khoi(d, "VÌ SAO — VÀ BẰNG CHỨNG", m["bc"])

    d.add_heading("§6 · Tài liệu tham khảo còn thiếu", level=1)
    d.add_paragraph(
        "Danh mục hiện có 11 tài liệu. Bảy tài liệu dưới đây cần bổ sung; hai "
        "trong số đó (Vygotsky và Bloom) đang được TRÍCH DẪN trong thân bài mà "
        "không có mục tương ứng ở danh mục — đó là lỗi hình thức nặng hơn lỗi "
        "thiếu nguồn.")
    for tl, vs in TLTK_THIEU:
        p = d.add_paragraph(style="List Number")
        do(p, tl, dam=True)
        q = d.add_paragraph()
        q.paragraph_format.left_indent = Pt(24)
        do(q, "Vì sao cần: ", nghieng=True)
        do(q, vs)

    d.add_heading("§7 · Bảng tóm tắt và thứ tự làm", level=1)
    d.add_paragraph(
        "Sắp theo mức ưu tiên. “BẮT BUỘC” là những chỗ người phản biện đối chiếu "
        "được bằng cách mở mã nguồn hoặc tệp dữ liệu ra tra cứu.")
    bang(d, ["Mã", "Việc", "Mục luận văn", "Ưu tiên", "Vì sao ở mức ấy"], UU_TIEN)

    d.add_heading("§8 · Một điều nên nói thẳng trong luận văn", level=1)
    for x in [
        "Bốn trong sáu chỗ mới tìm được ngày 25-08 đều thuộc cùng một họ: luận "
        "văn viết TRƯỚC, hệ thống dựng SAU, và khi hệ thống dựng xong thì không "
        "ai quay lại soi câu chữ. Đó là một quy trình có thể mô tả được, và mô "
        "tả được thì nên mô tả — phần bàn luận của luận văn có chỗ để nói rằng "
        "việc đối chiếu ngược từ hệ thống về tài liệu thiết kế đã bắt được bao "
        "nhiêu chỗ lệch, và đó chính là một kết quả.",

        "Chỗ hệ thống CỐ Ý khác luận văn — giữ 3 756 câu luyện tập sinh sẵn thay "
        "vì chuyển hết sang sinh lúc chạy — nên được viết như một LỰA CHỌN CÓ "
        "LÝ DO chứ không phải một phần chưa làm kịp. Nội dung tĩnh có 92 phép "
        "kiểm soi trước khi tới tay trẻ; nội dung sinh lúc chạy chỉ có hậu kiểm. "
        "Với người dùng 6–11 tuổi, khác biệt ấy không nhỏ.",

        "Việc dọn 130 bản ghi sai chủ và dựng lại mô hình người học từ nguồn gốc "
        "nên nằm trong luận văn, không nên giấu. Người phản biện đối chiếu số "
        "liệu hai thời điểm sẽ thấy chênh; nói trước thì đó là bằng chứng của "
        "một quy trình kiểm soát dữ liệu có thật, và bốn bất biến ở mục C-8 là "
        "phần đóng góp rút ra được từ chuyện ấy.",
    ]:
        d.add_paragraph(x, style="List Bullet")

    RA.parent.mkdir(parents=True, exist_ok=True)
    d.save(RA)
    print(f"đã ghi {RA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
