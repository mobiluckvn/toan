#!/usr/bin/env python3
"""DỰNG TÀI LIỆU: NHỮNG CHỖ CẦN SỬA Ở CHƯƠNG 2 LUẬN VĂN → docs/sua_chuong2.docx

    tools/tts/.venv/bin/python tools/sua_chuong2.py

Bác nhờ 23-08-2026: viết một tài liệu .docx liệt kê các vấn đề cần chỉnh sửa lại
Chương 2, càng chi tiết càng tốt, để bác tự sửa.

── ⚠ NGUYÊN TẮC VIẾT TÀI LIỆU NÀY ──
Mỗi mục phải trả lời đủ BỐN câu, thiếu câu nào thì bác không sửa được:
    1. SỬA Ở ĐÂU   — mục nào, câu nào của luận văn;
    2. ĐANG VIẾT GÌ — nguyên văn chỗ sai (hoặc ý của nó);
    3. SỬA THÀNH GÌ — câu thay thế, viết sẵn để bác chép;
    4. VÌ SAO + BẰNG CHỨNG — số đo lấy từ mã/dữ liệu đang chạy, có đường dẫn tệp.

Và một luật nữa: KHÔNG mục nào được viết "hệ thống làm sai so với luận văn" khi
sự thật là "luận văn mô tả một cách, hệ thống làm cách khác TỐT HƠN". Bốn mục ở
nhóm B thuộc loại ấy — sửa luận văn cho khớp thì luận văn MẠNH lên, không yếu đi.
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/sua_chuong2.docx"

# (mục, tiêu đề, đang viết gì, sửa thành gì, vì sao + bằng chứng)
MUC = [
    # ══ NHÓM A · SỐ LIỆU SAI, PHẢI SỬA ══
    ("A", "2.3.2", "Ngưỡng tinh thông θ = 0,95 → phải sửa thành 0,85",
     "Luận văn đặt ngưỡng coi là đã tinh thông θ = 0,95.",
     "“Ngưỡng tinh thông được đặt θ = 0,85, hiệu chỉnh bằng thực nghiệm trên chính "
     "bộ tham số BKT của hệ thống. Với bộ tham số P(L₀)=0,10 · P(T)=0,08 · "
     "P(S)=0,10 · P(G)=0,30, ngưỡng 0,85 tương ứng với khoảng bốn câu đúng liên "
     "tiếp mới công nhận là thạo, và một câu sai sau đó kéo mức thạo tụt xuống "
     "dưới ngưỡng. Bộ tham số cũ (P(L₀)=0,25 · P(G)=0,20) tuyên bố thạo chỉ sau "
     "hai câu — quá dễ dãi với học sinh tiểu học.”",
     "Đo trên chính mã đang chạy (`web/functions/src/bkt.js` dòng 13–14). Chuỗi "
     "mười lượt chạy thật cho: sai → 0,094; ba câu đúng liền → 0,830; MỘT câu sai "
     "kéo tụt còn 0,458; tới lượt thứ 8 mới đạt 0,903 và được công nhận thạo. "
     "Xem `docs/ma_tran_du_lieu.xlsx`, trang “Engine chạy thật”, cảnh 1. "
     "⚠ Nếu giữ θ=0,95 trong luận văn thì con số ấy KHÔNG khớp với hệ thống đang "
     "chạy, và người phản biện đối chiếu mã sẽ thấy ngay."),

    ("A", "2.5.2", "⚠ DỮ LIỆU THU ĐƯỢC TRƯỚC 23-08-2026 KHÔNG DÙNG ĐỂ PHÂN TÍCH ĐƯỢC",
     "Luận văn mô tả một đường ống ghi nhận đầy đủ: mỗi lượt trả lời một bản ghi "
     "bất biến, và mô hình người học dựng trên chuỗi bản ghi ấy. Nếu chương thực "
     "nghiệm có trích số liệu đã thu, thì con số ấy cần được xem lại.",
     "Thêm một đoạn vào phần mô tả dữ liệu, đại ý:\n"
     "  “Trong giai đoạn thử nghiệm, đường ống ghi nhận có hai khiếm khuyết đã "
     "được phát hiện và khắc phục ngày 23-08-2026. Thứ nhất, do tương tác giữa "
     "quy tắc bất biến của kho sự kiện và cơ chế gửi theo lô, mỗi phiên học chỉ "
     "có bản ghi ĐẦU TIÊN lên được máy chủ. Thứ hai, cơ chế nhận lại dữ liệu học "
     "thử khi đăng nhập đã gán nhầm bản ghi của người học này sang người học "
     "khác. Toàn bộ dữ liệu đã được rà và làm sạch: 130 bản ghi sai chủ được gỡ "
     "bỏ, mô hình người học được dựng lại từ nguồn gốc. Vì vậy số liệu dùng cho "
     "phân tích được lấy từ sau mốc này.”",
     "Đo bằng khoá quản trị 23-08-2026. (a) Kho `attempts` chỉ có 2 bản ghi môn "
     "Tiếng Anh cho hai buổi học khoảng mười lượt mỗi buổi — vì `attempts` khai "
     "`allow update, delete: if false` mà máy con mỗi lượt lại gửi lại cả phiên, "
     "còn `writeBatch` thì nguyên khối nên một bản ghi trùng làm rơi cả lô. Vá "
     "xong đo lại cùng một thao tác: 2 → 18. (b) 7 mã phiên bị hai người học "
     "cùng mang — chuyện không thể tự nhiên, vì mã phiên chỉ sinh ở một lần mở "
     "bài của một người. 130/398 bản ghi nằm sai học bạ. Đã xoá và dựng lại: "
     "`attempts` 398 → 268, `mastery` 32 mục, khớp tuyệt đối với nguồn (32/32).\n"
     "  ⚠ ĐÂY LÀ ĐIỂM CỘNG NẾU VIẾT RA, VÀ LÀ ĐIỂM TRỪ NẾU IM. Người phản biện "
     "đối chiếu số liệu hai thời điểm sẽ thấy chênh; nói trước thì đó là bằng "
     "chứng của một quy trình kiểm soát dữ liệu có thật."),

    ("A", "2.3.2", "BKT bỏ trắng 31% số câu người học thực làm",
     "Luận văn mô tả BKT cập nhật mức tinh thông sau mỗi lượt trả lời của người "
     "học.",
     "Nêu rõ những pha nào được tính và những pha nào bị loại, kèm lý do:\n"
     "  “Mức tinh thông chỉ cập nhật từ những lượt người học TỰ trả lời: luyện "
     "tập, sát hạch, câu chốt nhanh và câu xen giữa ví dụ mẫu. Các bước hệ thống "
     "đang trình bày lời giải (giới thiệu, làm mẫu, giảng) không được tính, vì ở "
     "đó người học chưa đưa ra câu trả lời nào của mình.”",
     "Trước 23-08-2026, hàm nền chỉ nhận hai pha `practice` và `assess`, nên "
     "`check` (câu chốt nhanh) và `worked` (câu xen giữa ví dụ) bị bỏ trắng — "
     "theo ghi chú trong `LessonPlayer.jsx` là 513/1654 câu, tức 31% số câu "
     "người học thực làm. Đã nới danh sách và dựng lại mô hình trên toàn bộ dữ "
     "liệu còn lại.\n"
     "  ⚠ Một chú thích trong mã từng khẳng định hai pha ấy “chỉ môn Tiếng Anh "
     "phát”. Sai — đo trên máy chủ có 49 lượt môn Toán mang chúng. Cổng "
     "`pha_vao_bkt.test.mjs` nay đọc thẳng từ mã nguồn xem mỗi môn phát ra pha "
     "nào, để không ai thu hẹp lại vì tin một lời ghi sai."),

    ("A", "2.3.1", "Hồ sơ bé — “CEFR hiện tại” đo PHỦ VỐN, không phải đo năng lực",
     "Luận văn xếp “CEFR hiện tại của người học” vào nhóm thuộc tính hồ sơ được "
     "hệ thống theo dõi, đặt cạnh `p_learned`, `RT_avg` — tức đọc như một đại "
     "lượng đo được từ hành vi. Trước 23-08-2026 điều này KHÔNG đúng: mức CEFR "
     "chỉ là nhãn gắn sẵn cho từng quyển học liệu.",
     "“Mức CEFR của người học được suy ra từ mô hình năng lực theo một quy ước "
     "bắc cầu hai nhịp. Nhịp thứ nhất do hệ thống đo: với mỗi khối lớp, tính tỉ "
     "lệ số nút tri thức mà người học đã đạt P(L) ≥ 0,85 trên tổng số nút của "
     "khối. Nhịp thứ hai lấy nguyên mục tiêu đã ấn định trong Chương trình GDPT "
     "2018 môn Tiếng Anh: khối lớp 1–2 là chương trình làm quen (dưới Bậc 1), "
     "khối lớp 3–5 nhắm Bậc 1 tương đương A1. Hệ thống công nhận một bậc khi tỉ "
     "lệ phủ của khối tương ứng đạt 60% và khối ấy có tối thiểu 30 nút; chưa đạt "
     "thì hệ thống báo đúng tỉ lệ phủ hiện có chứ không quy ra bậc.\n"
     "  ⚠ Cần nêu rõ trong luận văn: đây KHÔNG phải phép đo theo chuẩn CEFR. "
     "CEFR định nghĩa bậc bằng mô tả năng lực làm được (can-do descriptors), "
     "không định nghĩa bằng số đơn vị kiến thức đã nắm. Nhịp thứ hai là quy ước "
     "của chương trình quốc gia, không phải kết quả đo của hệ thống.”",
     "ĐÃ HIỆN THỰC 23-08-2026: `web/src/mon/tienganh/lib/cefr.js`. Mẫu số lấy "
     "1 062 nút học được trên tổng 1 194 nút của đồ thị lúc chạy — 132 nút chứa "
     "(course · theme · unit · review · fun_time) bị loại vì chúng là ngăn xếp tổ "
     "chức, không phải thứ người học nắm hay không nắm. Phân bố: khối lớp 1–2 có "
     "187 nút, khối lớp 3–5 có 871 nút, khối bắc cầu lớp 6 chỉ 4 nút nên luôn "
     "mang cờ “không đáng tin” và không bao giờ được lấy làm kết luận. Ba lựa "
     "chọn có thể tranh luận và cần bảo vệ được khi phản biện: ngưỡng phủ 60%, "
     "ngưỡng đáng tin 30 nút, và việc lấy mẫu số là TOÀN khối chứ không phải số "
     "nút người học đã chạm — lấy mẫu số là “đã chạm” thì một người học đúng 5 "
     "nút và nắm cả 5 sẽ ra 100%, tức phép đo thưởng cho việc học ít. Cổng "
     "`web/test/cefr_quy_doi.test.mjs` (19 phép) khoá đúng bốn chỗ này và đã "
     "được thử ngược: phá từng hàng rào thì cổng đỏ đúng chỗ."),

    ("B", "2.5.2", "“Mã prompt để kiểm toán” — nay đã lưu cùng lượt, giữ nguyên mô tả",
     "Luận văn liệt kê “mã prompt” trong nhóm Bối cảnh hệ thống của bản ghi sự "
     "kiện, đọc như thể mỗi bản ghi đều mang mã prompt đã sinh ra nó. Trước "
     "23-08-2026 mô tả này đi trước hiện trạng: vân tay có sinh ra nhưng chỉ "
     "nằm trong phản hồi trả về máy con, không vào bản ghi.",
     "GIỮ NGUYÊN mô tả trong luận văn, và nói thêm cho chính xác: “Bản ghi sự "
     "kiện mang vân tay của KHUNG lời nhắc — gồm mã mẫu, số phiên bản và mã băm "
     "của khung — chứ không lưu nội dung lời nhắc đã sinh. Chủ ý này để truy vết "
     "được “câu chấm này do mẫu nhắc nào sinh ra” mà không lưu dữ liệu riêng tư "
     "của người học vào bản ghi dùng chung.”",
     "ĐÃ HIỆN THỰC 23-08-2026. Ba trường `mauPrompt` · `phienBanMau` · "
     "`vanTayPrompt` đi từ `web/functions/src/vantay.js` qua phản hồi của "
     "`chamViet`/`luyenNoi`, được `goiChamViet.js` giữ lại (trước đây bị rơi ở "
     "đúng chỗ này), rồi vào bản ghi tại `web/src/mon/tienganh/lib/suKien.js`.\n"
     "  ✅ ĐÃ SOI THẤY TRÊN MÁY CHỦ 23-08-2026 bằng khoá quản trị: lượt bài viết "
     "mang `mauPrompt=chamviet` · `phienBanMau=1` · `vanTayPrompt=1c85246bffac`. "
     "Nay trả lời được câu “câu này do prompt nào sinh ra” bằng dữ liệu, không "
     "phải bằng mã nguồn."),

    ("B", "2.2.1", "Đồ thị làm bộ truy xuất — cần phân biệt bản ĐẦY ĐỦ và bản LÚC CHẠY",
     "Luận văn mô tả đồ thị tri thức đóng vai trò bộ truy xuất (Retriever) cho "
     "RAG, với quy mô toàn bộ chương trình lớp 1–5.",
     "“Đồ thị đầy đủ gồm 3 989 nút và 7 602 cạnh, dùng ở khâu DỰNG học liệu. Khi "
     "chạy, ứng dụng trên máy người học nạp một đồ thị rút gọn gồm 1 194 nút và "
     "253 cạnh (195 cạnh REQUIRES, 5 cạnh nối bài, 53 cạnh thứ tự trong bài), chỉ "
     "giữ QUAN HỆ mà không giữ nhãn hay ví dụ — vì học liệu đã mang sẵn phần chữ "
     "nghĩa. Bản rút gọn nặng khoảng 80 KB, đủ để duyệt chẩn đoán ngay trên máy "
     "mà không cần gọi máy chủ.”",
     "Đếm trực tiếp: `data/ban_do_tieng_anh.json` = 3 989 nút / 7 602 cạnh; "
     "`web/public/content/tienganh/do_thi.json` = 1 194 nút / 253 cạnh. Bộ cắt: "
     "`tools/xuat_do_thi_con.py`. Nói rõ hai bản thì phần kiến trúc của luận văn "
     "chính xác hơn hẳn, và giải thích được vì sao chẩn đoán chạy được offline."),

    ("B", "2.3.1", "H_req — “số lần dùng trợ giúp” cần định nghĩa lại cho đúng",
     "Luận văn định nghĩa H_req là số lần người học YÊU CẦU trợ giúp.",
     "“H_req trong hệ thống là số gợi ý người học ĐÃ ĐƯỢC THẤY tại một câu, không "
     "phải số lần chủ động yêu cầu: gợi ý hiện tự động sau một số lần trả lời sai. "
     "Hai đại lượng gần nhau nhưng không đồng nhất — H_req ở đây phản ánh mức khó "
     "mà người học gặp phải, chứ không phản ánh hành vi tìm kiếm trợ giúp.”",
     "`web/src/mon/tienganh/components/CauHoi.jsx` — số gợi ý tính từ `lan` (số "
     "lượt đã trả lời) so với hằng số `HIEN_GOI_Y`, không có nút “xin gợi ý”. Chú "
     "thích trong `web/src/mon/tienganh/lib/suKien.js` đã ghi rõ khác biệt này. "
     "Nếu luận văn diễn giải H_req như hành vi tìm trợ giúp thì kết luận rút ra "
     "sẽ sai về chất."),

    # ══ NHÓM C · LUẬN VĂN NÓI CHUNG CHUNG, NÊN NÓI RÕ THÊM ══
    ("C", "2.5.2", "Nhịp ghi sự kiện — nên nói rõ là GOM LÔ theo phiên",
     "Luận văn mô tả “lưu vết hướng sự kiện — chuỗi sự kiện bất biến”, không nói "
     "về nhịp ghi.",
     "“Sự kiện được ghi vào bộ nhớ ngay khi người học trả lời, nhưng chỉ được đẩy "
     "lên máy chủ theo LÔ ở cuối mỗi phiên. Mã định danh của mỗi bản ghi nhúng số "
     "thứ tự của lượt trong phiên, nhờ đó việc gửi lại toàn phiên là thao tác "
     "lũy đẳng: các lượt cũ ghi đè lên chính chúng, không sinh bản ghi trùng. "
     "Thiết kế này cần thiết vì nếu đẩy từng lượt một, số thứ tự luôn bằng 0 và "
     "mọi lượt của cùng một câu sẽ đè lên nhau — mất đúng thông tin mà nhật ký "
     "sinh ra để giữ (người học sai hai lần rồi mới đúng).”",
     "`web/src/mon/tienganh/lib/suKien.js` — hàm `maSuKien(learnerId, maPhien, "
     "microId, itemId, i)`. Ghi rõ điều này giúp luận văn giải thích được vì sao "
     "vẫn giữ được tính bất biến của chuỗi sự kiện khi mạng chập chờn."),

    ("C", "2.3.3", "Lan truyền — nên công bố hai hệ số α và β",
     "Luận văn nêu lan truyền ngược có hệ số suy giảm α và lan truyền xuôi có hệ "
     "số cộng hưởng β, nhưng không cho giá trị.",
     "“Hệ số suy giảm α = 0,6: mỗi bước lùi về phía nút gốc, độ nghi ngờ nhân với "
     "α. Hệ số cộng hưởng β = 0,08: khi một nút phía trên đã đạt ngưỡng thạo, các "
     "nút dựng trên nó được cộng thêm β vào mức thạo ước lượng, nhưng không vượt "
     "quá NGƯỠNG_TRẦN = θ − 0,05 — tức cộng hưởng không bao giờ tự nó tuyên bố "
     "một nút là đã thạo.”",
     "`web/src/mon/tienganh/lib/lantruyen.js` — `ALPHA = 0.6`, `BETA = 0.08`, "
     "`NGUONG_TRAN = NGUONG_THAO - 0.05`. Ví dụ chạy thật: nút p = 0,55 có nút "
     "trên đã thạo thì được nâng lên 0,63. Công bố số cụ thể làm phần này tái lập "
     "được."),

    ("C", "2.5.1", "Hàm chính sách π — nên nói rõ THỨ TỰ XÉT và điều kiện vượt ải",
     "Luận văn mô tả ba nhánh (Tịnh tiến · Vượt ải · Can thiệp phụ đạo) theo "
     "khoảng giá trị của P(L).",
     "“Hàm chính sách xét ĐANG MẮC TRƯỚC mức thạo: nếu người học sai từ 3 lần "
     "liên tiếp trở lên tại một nút thì chuyển sang can thiệp phụ đạo, bất kể "
     "P(L) đang là bao nhiêu. Lý do: P(L) là một trung bình có quán tính, còn "
     "chuỗi sai liên tiếp là tín hiệu tức thời và đáng tin hơn về trạng thái hiện "
     "tại. Nhánh Vượt ải xét ở mức BÀI chứ không mức nút, và đòi đủ ba điều kiện: "
     "đã đạt bài, bài có ít nhất 3 nút, và MỌI nút của bài đều đạt ngưỡng.”",
     "`web/src/mon/tienganh/lib/chinhsach.js` — `viecTiepCuaNut` xét "
     "`saiLienTiep >= 3` trước khi xét `p`; `duocVuotAi(mucThao, maNutDs, daDat, "
     "{toiThieuNut: 3})`. Chạy thật: cùng p = 0,96 nhưng vừa sai 3 lần thì kết "
     "quả là `phuDao`, không phải `vuotAi`. Xem `docs/ma_tran_du_lieu.xlsx` cảnh "
     "4 và 4b."),

    ("C", "2.1.2", "Chiều Thời gian — mệt mỏi đo bằng HAI tín hiệu, nêu rõ giới hạn từng cái",
     "Luận văn nêu chiều Thời gian bao gồm đo mệt mỏi nhận thức, nhưng không nói "
     "đo bằng cách nào. Người phản biện sẽ hỏi ngay: mệt mỏi là trạng thái bên "
     "trong, phần mềm suy ra từ dấu hiệu quan sát được nào?",
     "“Chiều Thời gian được hiện thực bằng bốn thành phần: đường cong quên (hàm "
     "mũ, nửa đời 14 ngày), lịch lặp lại ngắt quãng, và HAI tín hiệu độc lập cho "
     "mệt mỏi nhận thức.\n"
     "  Tín hiệu thứ nhất — CHẬM DẦN TRONG PHIÊN: hệ thống so thời gian phản hồi "
     "trung bình nửa đầu với nửa cuối của cùng một phiên học, tách riêng theo "
     "từng định dạng câu hỏi, và chỉ kết luận khi mỗi nửa có tối thiểu 3 lượt. "
     "Chậm hơn 25% thì báo là có dấu hiệu mệt.\n"
     "  Tín hiệu thứ hai — BỎ DỞ: mỗi lần người học rời màn bài học khi chưa hoàn "
     "thành, hệ thống ghi một bản ghi gồm mã bài, chặng đang dở, số lượt đã làm "
     "và số giây đã ở trong bài; mỗi lần một bản ghi chứ không gộp, vì chính số "
     "LẦN bỏ dở cùng một bài mới là tín hiệu.\n"
     "  Hai tín hiệu hiện được ĐO và báo cho phụ huynh, chưa dùng để tự động rút "
     "ngắn buổi học.”",
     "Tín hiệu 1: `web/functions/src/report.js` — hàm `metMoi()`, hằng số "
     "`TOI_THIEU_MOI_NUA = 3` và `NGUONG_CHAM = 0,25`; hiện ở `ParentReport.jsx`. "
     "Việc tách theo ĐỊNH DẠNG là chi tiết đáng viết vào luận văn: không tách thì "
     "phiên nào cũng ra 'mệt', vì các màn cuối buổi vốn có dạng câu tốn thời gian "
     "hơn — chậm hơn vì ĐỔI VIỆC chứ không phải vì mệt. Tín hiệu 2 vá 23-08-2026 "
     "(`BaiHoc.jsx` → học bạ loại `phien`).\n"
     "  ✅ ĐÃ SOI THẤY TRÊN MÁY CHỦ 23-08-2026: 5 bản ghi loại `phien`, đủ bốn "
     "trường `microId`·`chang`·`soLuot`·`giay`, và CÙNG MỘT BÀI bị bỏ dở 5 lần "
     "được đếm riêng từng lần (169 giây · 31 giây · 21 giây · 5 giây …) — đúng "
     "thiết kế, vì chính số LẦN mới là tín hiệu. Luật Firestore cũng đã thử "
     "thật trên bộ giả lập: 9 phép, kể cả chiều bị từ chối.\n"
     "  ⚠ PHẢI NÊU GIỚI HẠN CỦA TÍN HIỆU 2: chỉ ghi được khi người học rời màn qua "
     "thao tác trong ứng dụng; đóng thẳng trình duyệt thì không ghi được. Con số "
     "thu được là CẬN DƯỚI của số lần bỏ dở thật — dùng làm chỉ báo xu hướng, "
     "không phải phép đếm đầy đủ. Nêu ra là điểm cộng về tính trung thực, và "
     "tránh câu phản biện “sao số lần bỏ dở lại thấp bất thường”."),

    ("C", "2.1.2", "Chiều Nhận thức — nên nói rõ giới hạn của điểm PHÁT ÂM",
     "Luận văn xếp năng lực nói vào chiều Nhận thức cùng các kỹ năng khác, không "
     "phân biệt nguồn của phép đo.",
     "“Điểm phát âm được chấm bằng bộ nhận dạng giọng nói sẵn có của trình duyệt "
     "(Web Speech API). Vì vậy con số này phụ thuộc chất lượng micro và mức ồn "
     "của môi trường: cùng một người học, hai thiết bị khác nhau có thể cho kết "
     "quả khác nhau. Hệ thống vẫn đưa điểm này vào mô hình người học, nhưng gắn "
     "nhãn riêng cho ba dạng lượt nói để có thể tách ra khi cần một phép đo "
     "thuần nhất.”",
     "`web/src/mon/tienganh/lib/nghenoi.js` dòng 23 dùng "
     "`window.SpeechRecognition || window.webkitSpeechRecognition`. Ba nhãn: "
     "`mode` = `noiTu` · `noiCau` · `phongNoi` (bổ sung 23-08-2026). Nêu giới hạn "
     "này là điểm cộng về tính trung thực khoa học, không phải điểm trừ."),
]

# Việc phần mềm còn nợ — để bác biết mục nào KHÔNG phải sửa luận văn
CON_NO = [
    ("Nối vân tay prompt vào `attempts`", "ĐÃ XONG 23-08-2026",
     "Ba trường `mauPrompt` · `phienBanMau` · `vanTayPrompt` nay đi vào mỗi bản "
     "ghi sự kiện. Mục 2.5.2 đáp ứng đúng như luận văn mô tả — không phải sửa "
     "chữ, chỉ nói thêm rằng vân tay băm KHUNG chứ không lưu nội dung nhắc."),
    ("Ghi sự kiện rời màn / bỏ dở", "ĐÃ XONG 23-08-2026",
     "Mục học bạ loại `phien` (mã bài · chặng · số lượt · số giây), mỗi lần bỏ dở "
     "một bản ghi. Đây là tín hiệu THỨ HAI cho mệt mỏi nhận thức — tín hiệu thứ "
     "nhất (`metMoi()` so thời gian phản hồi nửa đầu với nửa cuối phiên) đã có "
     "sẵn từ trước. Nêu rõ giới hạn cận dưới: đóng thẳng trình duyệt thì không "
     "ghi được."),
    ("Báo cáo riêng của bé đọc thêm `progressTA` và `hocBaTA`", "ĐÃ XONG 23-08-2026",
     "`dungSoHoc` nay gộp số bài xong và số phút học của cả hai môn. Trước đó hai "
     "cột ấy bỏ sót toàn bộ môn Tiếng Anh."),
    ("Quy đổi P(L) sang thang CEFR", "ĐÃ XONG 23-08-2026",
     "`lib/cefr.js` + thẻ “con đang ở đâu trên thang năng lực” ở Góc bố mẹ. "
     "⚠ Đây là quy ước bắc cầu, KHÔNG phải phép đo theo chuẩn CEFR — mục A-2.3.1 "
     "đã viết sẵn câu phải đưa vào luận văn để nói đúng điều đó. "
     "⚠ Hàm cũ `cefrCuaBe()` (suy bậc từ quyển đã học xong) KHÔNG màn nào gọi — "
     "mã chết từ lúc viết — nên đã XOÁ ngày 23-08 theo ý bác; lý do và hai cái "
     "bẫy của nó ghi lại trong chú thích tại `lib/hoso.js`."),
]


def main() -> int:
    d = Document()
    d.styles["Normal"].font.name = "Times New Roman"
    d.styles["Normal"].font.size = Pt(12)

    t = d.add_heading("NHỮNG CHỖ CẦN CHỈNH SỬA — CHƯƠNG 2 LUẬN VĂN", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = d.add_paragraph()
    p.add_run("Hệ thống đối chiếu: ").bold = True
    p.add_run("Kỹ Sư Nhí — ky-su-nhi.web.app (môn Tiếng Anh, lớp 1–5)\n")
    p.add_run("Ngày lập: ").bold = True
    p.add_run("23-08-2026\n")
    p.add_run("Căn cứ: ").bold = True
    p.add_run("đối chiếu 54 tiêu chí của Chương 2 với mã nguồn và dữ liệu đang "
              "chạy, cộng một buổi đăng nhập kiểm chứng trên bản chạy thật.\n")
    p.add_run("Sửa lần 2 — 23-08-2026 (chiều): ").bold = True
    p.add_run("bốn việc phần mềm ở phụ lục đã làm xong và deploy, nên ba mục "
              "A-2.3.1, B-2.5.2 và C-2.1.2 được viết lại. Rà lại còn phát hiện "
              "HAI chỗ bảng đối chiếu bản 22-08 ghi ĐẠT mà thực ra chưa: hàm "
              "`cefrCuaBe()` không màn nào gọi, và vân tay prompt bị rơi ở "
              "`goiChamViet.js`. Cả hai nay đã vá; bảng "
              "`docs/benchmark_chuong2.xlsx` đã ghi rõ chỗ sửa lại.\n")
    p.add_run("Sửa lần 3 — 23-08-2026 (tối): ").bold = True
    p.add_run("soi Firestore bằng khoá quản trị và phát hiện hai lỗi ĐƯỜNG ỐNG "
              "DỮ LIỆU, nặng hơn mọi mục trước: mỗi phiên học chỉ có bản ghi đầu "
              "tiên lên được máy chủ, và 130/398 bản ghi nằm sai học bạ. Cả hai "
              "đã vá, dữ liệu đã dọn và mô hình người học đã dựng lại. Xem hai "
              "mục MỚI ở đầu nhóm A — chúng ảnh hưởng thẳng tới phần số liệu của "
              "luận văn, không chỉ tới câu chữ.")

    d.add_heading("Cách đọc tài liệu này", level=1)
    for x in [
        "Mỗi mục gồm bốn phần: (1) SỬA Ở ĐÂU — mục nào của luận văn; (2) ĐANG VIẾT "
        "GÌ; (3) SỬA THÀNH GÌ — câu thay thế đã viết sẵn để chép thẳng vào; (4) VÌ "
        "SAO và BẰNG CHỨNG — số đo lấy từ mã hoặc dữ liệu, kèm đường dẫn tệp.",
        "Các mục được xếp thành ba nhóm: NHÓM A là số liệu sai, buộc phải sửa. "
        "NHÓM B là chỗ luận văn mô tả một cách còn hệ thống làm cách khác TỐT HƠN "
        "— sửa cho khớp thì luận văn mạnh lên. NHÓM C là chỗ luận văn nói chung "
        "chung, nên nói rõ thêm để phần trình bày tái lập được.",
        "Phần cuối liệt kê những việc thuộc về PHẦN MỀM chứ không phải luận văn — "
        "để bác biết mục nào không cần sửa chữ, chỉ cần bổ sung mã.",
    ]:
        d.add_paragraph(x, style="List Bullet")

    ten_nhom = {
        "A": "NHÓM A — SỐ LIỆU SAI, BUỘC PHẢI SỬA",
        "B": "NHÓM B — LUẬN VĂN MÔ TẢ MỘT CÁCH, HỆ THỐNG LÀM CÁCH KHÁC TỐT HƠN",
        "C": "NHÓM C — NÓI CHUNG CHUNG, NÊN NÓI RÕ THÊM",
    }
    nhom_hien = None
    stt = 0
    for nhom, muc, tieu_de, dang, sua, vi_sao in MUC:
        if nhom != nhom_hien:
            nhom_hien = nhom
            d.add_page_break()
            d.add_heading(ten_nhom[nhom], level=1)
        stt += 1
        d.add_heading(f"{stt}. [Mục {muc}] {tieu_de}", level=2)

        for nhan, noi_dung in [
            ("ĐANG VIẾT GÌ", dang),
            ("SỬA THÀNH", sua),
            ("VÌ SAO — VÀ BẰNG CHỨNG", vi_sao),
        ]:
            q = d.add_paragraph()
            r = q.add_run(nhan + ": ")
            r.bold = True
            r.font.color.rgb = RGBColor(0x2F, 0x4A, 0x6B)
            for i, doan in enumerate(str(noi_dung).split("\n")):
                if i:
                    q = d.add_paragraph()
                    q.paragraph_format.left_indent = Pt(18)
                q.add_run(doan)

    d.add_page_break()
    d.add_heading("PHỤ LỤC — VIỆC CỦA PHẦN MỀM (ĐÃ XONG 23-08-2026)", level=1)
    d.add_paragraph(
        "Bốn việc dưới đây ĐÃ LÀM XONG ngày 23-08-2026 và đã lên bản chạy thật "
        "(luật Firestore → hàm nền → giao diện, đúng thứ tự). Mục tương ứng của "
        "luận văn nay đáp ứng đúng như đang mô tả — nhưng ba trong bốn mục vẫn "
        "cần NÓI RÕ GIỚI HẠN, xem lại các mục A-2.3.1, B-2.5.2 và C-2.1.2 ở "
        "trên. Làm xong phần mềm không có nghĩa là câu chữ trong luận văn tự "
        "đúng theo.")
    b = d.add_table(rows=1, cols=3)
    b.style = "Light Grid Accent 1"
    for i, h in enumerate(["Việc", "Tình trạng", "Xong rồi thì được gì"]):
        b.rows[0].cells[i].text = h
        b.rows[0].cells[i].paragraphs[0].runs[0].bold = True
    for viec, cong, duoc in CON_NO:
        o = b.add_row().cells
        o[0].text, o[1].text, o[2].text = viec, cong, duoc

    d.add_page_break()
    d.add_heading("PHỤ LỤC — TÀI LIỆU ĐỐI CHIẾU KÈM THEO", level=1)
    for ten, mo in [
        ("docs/benchmark_chuong2.xlsx", "Đối chiếu đủ 54 tiêu chí của Chương 2 với "
         "hệ thống: đáp ứng / một phần / không thể, kèm lộ trình."),
        ("docs/ma_tran_du_lieu.xlsx", "Ma trận 36 trường dữ liệu (ghi gì · ở đâu · "
         "tần suất · ai đọc), và trang “Engine chạy thật” — đầu ra của chính mã "
         "engine, không phải sơ đồ."),
        ("docs/soat_giam_sat.xlsx", "16 hành động của người học, hành động nào có "
         "dữ liệu giám sát, hành động nào chưa."),
        ("docs/kiem_chung_ban_chay.xlsx", "Biên bản buổi đăng nhập kiểm chứng trên "
         "bản chạy thật (07h32 ngày 23-08-2026), kèm ảnh chụp màn hình. ⚠ Phần "
         "quan sát GIỮ NGUYÊN, không sửa cho khớp hiện trạng — sửa thì nó thôi "
         "không còn là biên bản. Những gì vá SAU buổi ấy ghi riêng ở trang “Sau "
         "buổi thử”, và trang ấy nói rõ phần nào VẪN CHƯA đi thử lại."),
    ]:
        q = d.add_paragraph(style="List Bullet")
        q.add_run(ten).bold = True
        q.add_run(" — " + mo)

    RA.parent.mkdir(parents=True, exist_ok=True)
    d.save(RA)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   {len(MUC)} mục cần sửa · {len(CON_NO)} việc thuộc phần mềm")
    for k, v in {"A": 0, "B": 0, "C": 0}.items():
        n = sum(1 for m in MUC if m[0] == k)
        print(f"   nhóm {k}: {n} mục")
    return 0


if __name__ == "__main__":
    sys.exit(main())
