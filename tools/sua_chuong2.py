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

    ("A", "2.3.1", "Hồ sơ bé — “CEFR hiện tại” không phải một phép ĐO",
     "Luận văn xếp “CEFR hiện tại của người học” vào nhóm thuộc tính hồ sơ được "
     "hệ thống theo dõi, đặt cạnh `p_learned`, `RT_avg` — tức đọc như một đại "
     "lượng đo được từ hành vi.",
     "“Mức CEFR trong hệ thống là NHÃN CỦA HỌC LIỆU, không phải kết quả đo năng "
     "lực người học: mỗi quyển được gắn sẵn một mức (Pre-A1 cho lớp 1–3, A1 cho "
     "lớp 4–5) và giao diện hiển thị mức của quyển bé đang học. Việc quy đổi năng "
     "lực đo được (P(L) trên đồ thị) sang thang CEFR chưa được thực hiện và nằm "
     "ngoài phạm vi luận văn.”",
     "`web/public/content/chuong_trinh.json`: ta1·ta2·ta3 = Pre-A1, ta4·ta5 = A1. "
     "Mã hiển thị: `ManTiengAnh.jsx` — `const cefr = ct?.cefr`, tức lấy thẳng "
     "thuộc tính của QUYỂN, không đụng tới dữ liệu của bé. Viết đúng như trên thì "
     "luận văn tránh được một câu hỏi phản biện rất dễ bị hỏi."),

    ("A", "2.2.2", "`prerequisite_links` có thật, nhưng THƯA — cần nói rõ tỉ lệ",
     "Luận văn mô tả `prerequisite_links` như một thuộc tính của nút, đọc như thể "
     "mọi nút đều mang nó.",
     "“Ràng buộc tiên quyết được biểu diễn bằng HAI cơ chế bổ sung nhau: (a) thuộc "
     "tính `prerequisite_links` trên nút — hiện có ở 231/3 989 nút (5,8%); và (b) "
     "cạnh có hướng REQUIRES trong đồ thị — 583 cạnh. Cơ chế (b) là nguồn chính "
     "khi hệ thống chạy; (a) đóng vai trò bổ trợ cho những nút đã được chú giải "
     "thủ công.”",
     "Đếm trực tiếp trên `data/ban_do_tieng_anh.json`: 3 989 nút · 7 602 cạnh, "
     "trong đó 583 cạnh REQUIRES; 231 nút có `prerequisite_links`. Nói rõ con số "
     "thì phần mô tả đồ thị của luận văn trở nên kiểm chứng được."),

    ("A", "2.5.3", "Lịch lặp lại ngắt quãng: +1/+3/+7 → thực tế có NĂM bậc",
     "Luận văn mô tả lịch ôn theo ba mốc +1 / +3 / +7 ngày.",
     "“Lịch ôn dùng mô hình hộp Leitner năm bậc với giãn cách 1 – 3 – 7 – 14 – 30 "
     "ngày. Trả lời đúng đẩy thẻ lên bậc kế tiếp; trả lời sai đưa thẻ về bậc đầu.”",
     "`web/src/mon/tienganh/lib/onlai.js` — `BOX_NGAY = [1, 3, 7, 14, 30]`. Chuỗi "
     "chạy thật: đúng·đúng·đúng → bậc 3 (hẹn 14 ngày); một câu SAI → về bậc 0 "
     "(hẹn 1 ngày). Xem `docs/ma_tran_du_lieu.xlsx`, cảnh 6."),

    # ══ NHÓM B · LUẬN VĂN MÔ TẢ MỘT CÁCH, HỆ THỐNG LÀM CÁCH KHÁC TỐT HƠN ══
    ("B", "2.4.3", "RAG bước 3 — “prompt đảm bảo 100% không dùng từ lạ”",
     "Luận văn viết rằng bước Tạo sinh có kiểm soát dùng nhắc lệnh (prompt) để "
     "“đảm bảo 100%” mô hình không dùng từ ngoài vốn đã học.",
     "“Bước Tạo sinh có kiểm soát gồm HAI TẦNG, và con số 100% đến từ tầng thứ "
     "hai chứ không từ nhắc lệnh:\n"
     "  • Tầng 1 — ràng buộc trong nhắc lệnh: liệt kê vốn từ được phép và cấm dùng "
     "từ ngoài danh sách. Tầng này làm giảm mạnh tỉ lệ vi phạm nhưng KHÔNG bảo "
     "đảm tuyệt đối, vì mô hình ngôn ngữ là hệ sinh xác suất.\n"
     "  • Tầng 2 — hậu kiểm bắt buộc: mọi câu mô hình sinh ra đều bị đối chiếu lại "
     "với túi từ của chính bài học; câu chứa từ ngoài túi bị LOẠI BỎ trước khi "
     "hiển thị. Chính tầng này bảo đảm người học không bao giờ nhìn thấy từ lạ.”",
     "⚠ ĐÂY LÀ MỤC QUAN TRỌNG NHẤT CỦA TÀI LIỆU. Viết như luận văn hiện tại là "
     "một khẳng định KHÔNG THỂ ĐÚNG về mặt kỹ thuật, và người phản biện biết về "
     "LLM sẽ hỏi ngay. Viết lại thành hai tầng thì luận văn MẠNH HƠN: nó cho thấy "
     "tác giả hiểu giới hạn của prompt và đã thiết kế hàng rào thứ hai.\n\n"
     "BẰNG CHỨNG CHẠY THẬT (đăng nhập production 23-08-2026, tài khoản thử): sau "
     "khi chấm một bài viết, màn hình hiện đúng dòng “Cô có 1 câu gợi ý dùng từ "
     "con chưa học, nên cô giấu đi rồi.” Tức mô hình ĐÃ sinh ra một câu vi phạm, "
     "và tầng hậu kiểm ĐÃ chặn nó lại. Ảnh chụp: "
     "`docs/anh_kiem_chung/01_ai_cham_bai_viet.jpg`. Mã: `loiVietHopLe()` và "
     "`cauHopLe()` trong `web/src/mon/tienganh/lib/phongnoi.js`."),

    ("B", "2.5.2", "“Mã prompt để kiểm toán” — có vân tay, nhưng KHÔNG lưu cùng lượt",
     "Luận văn liệt kê “mã prompt” trong nhóm Bối cảnh hệ thống của bản ghi sự "
     "kiện, đọc như thể mỗi bản ghi đều mang mã prompt đã sinh ra nó.",
     "Chọn MỘT trong hai hướng:\n"
     "  (i) Sửa mô tả cho khớp hiện trạng: “Hệ thống sinh vân tay của KHUNG nhắc "
     "lệnh (mẫu prompt + phiên bản + tham số) và trả kèm mỗi lời chấm của mô "
     "hình. Vân tay này hiện đi cùng kết quả trả về, chưa được ghi vào bản ghi sự "
     "kiện; việc nối vân tay vào từng lượt để truy vết đầy đủ là hướng phát triển "
     "tiếp theo.”\n"
     "  (ii) Hoặc giữ nguyên mô tả trong luận văn và yêu cầu bổ sung phần mềm — "
     "công việc nhỏ: thêm một trường `vanTay` vào bản ghi `attempts`.",
     "`web/functions/src/vantay.js` có hàm `vanTay(mau, khung, them)` băm KHUNG "
     "lời dặn (không băm cả prompt, để không lưu nội dung riêng tư). Hai chỗ gọi: "
     "`chamviet.js:157` và `luyennoi.js:163` — cả hai đều SPREAD kết quả vân tay "
     "vào phản hồi trả về máy con, không ghi vào `attempts`. Nên hiện chưa trả "
     "lời được câu “câu này do prompt nào sinh ra”."),

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

    ("C", "2.1.2", "Chiều Thời gian — “đo mệt mỏi nhận thức” chưa có dữ liệu nền",
     "Luận văn nêu chiều Thời gian bao gồm đo mệt mỏi nhận thức.",
     "“Chiều Thời gian hiện được hiện thực bằng hai thành phần: đường cong quên "
     "(hàm mũ, nửa đời 14 ngày) và lịch lặp lại ngắt quãng. Thành phần đo mệt mỏi "
     "nhận thức chưa được hiện thực: hệ thống hiện không ghi sự kiện rời màn hay "
     "bỏ dở, nên chưa có dữ liệu nền để suy ra trạng thái mệt. Đây là hướng phát "
     "triển tiếp theo.”",
     "Đã rà toàn bộ màn hình môn Tiếng Anh: không màn nào phát sự kiện thoát. Xem "
     "`docs/soat_giam_sat.xlsx`, trang “Hành động → dữ liệu”, dòng “Bỏ dở giữa "
     "chừng”. Nhận là chưa có thì đúng hơn nhiều so với để người đọc tưởng đã có."),

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
    ("Nối vân tay prompt vào `attempts`", "nhỏ",
     "Thêm một trường vào bản ghi sự kiện. Xong thì mục 2.5.2 đáp ứng đúng như "
     "luận văn mô tả, không phải sửa chữ."),
    ("Ghi sự kiện rời màn / bỏ dở", "vừa",
     "Cần thiết nếu muốn giữ phần “đo mệt mỏi nhận thức” trong luận văn."),
    ("Báo cáo riêng của bé đọc thêm `progressTA` và `hocBaTA`", "nhỏ",
     "Hiện `dungSoHoc` chỉ đọc dữ liệu môn Toán, nên hai cột “xong bao nhiêu bài” "
     "và “số phút học” bỏ sót toàn bộ môn Tiếng Anh."),
    ("Quy đổi P(L) sang thang CEFR", "lớn",
     "Nếu muốn giữ CEFR như một phép ĐO trong luận văn thì phải làm phần này; "
     "nếu không thì sửa chữ theo mục A-2.3.1."),
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
              "chạy, cộng một buổi đăng nhập kiểm chứng trên bản chạy thật.")

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
    d.add_heading("PHỤ LỤC — VIỆC CỦA PHẦN MỀM, KHÔNG PHẢI CỦA LUẬN VĂN", level=1)
    d.add_paragraph(
        "Bốn việc dưới đây nếu làm xong thì mục tương ứng của luận văn đáp ứng "
        "đúng như đang mô tả, không phải sửa chữ.")
    b = d.add_table(rows=1, cols=3)
    b.style = "Light Grid Accent 1"
    for i, h in enumerate(["Việc", "Công sức", "Sửa xong thì được gì"]):
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
        ("docs/ma_tran_du_lieu.xlsx", "Ma trận 34 trường dữ liệu (ghi gì · ở đâu · "
         "tần suất · ai đọc), và trang “Engine chạy thật” — đầu ra của chính mã "
         "engine, không phải sơ đồ."),
        ("docs/soat_giam_sat.xlsx", "16 hành động của người học, hành động nào có "
         "dữ liệu giám sát, hành động nào chưa."),
        ("docs/kiem_chung_ban_chay.xlsx", "Biên bản buổi đăng nhập kiểm chứng trên "
         "bản chạy thật, kèm ảnh chụp màn hình."),
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
