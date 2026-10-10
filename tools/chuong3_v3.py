#!/usr/bin/env python3
"""
CHƯƠNG 3 — BẢN VIẾT LẠI → docs/Chuong3_Luan_van_v3.docx

    node tools/chuong3_v3_so.mjs                    # 1. số liệu, từ mã đang chạy
    tools/tts/.venv/bin/python tools/chuong3_v3_hinh.py   # 2. sáu hình
    tools/tts/.venv/bin/python tools/chuong3_v3.py        # 3. chương

── VÌ SAO VIẾT LẠI ──
Bản trong `Luan_van_Chuong2_Chuong3_v2.docx` đặc tả đầy đủ nhưng không có chỗ
nào cho người đọc thấy hệ thống CHẠY. Nhận xét của Thầy hỏi đúng chín điều mà
một bản đặc tả không trả lời được:

    1. một phiên của một cá nhân cụ thể thì diễn ra thế nào       → mục 3.6
    2. tiêu chí để phát hiện lỗ hổng là gì                        → mục 3.4.1
    3. người phản biện sẽ hỏi gì, ví dụ minh hoạ ở đâu            → mục 3.7
    4. đồ thị tri thức biểu diễn như thế nào                      → mục 3.2.2
    5. bao nhiêu nút, tham khảo tài liệu nào                      → Bảng 3.3
    6. cài đặt thì tập nút nằm ở bảng nào, mệnh đề điều kiện nào  → mục 3.2.4
    7. đồ thị THÀNH HÌNH ra sao, thuộc tính nào                   → mục 3.2.1, Bảng 3.5
    8. một phiên lưu thông tin gì và lưu thế nào                  → mục 3.3
    9. đánh giá được các tình trạng như thế nào                   → Bảng 3.13
   10. phương pháp gợi ý, ví dụ rất cụ thể                        → mục 3.5 và 3.6.6

Bản này NGẮN HƠN bản v2 (10 mục thay vì 8 mục dài, 32 bảng thay vì 31 bảng cộng
14 thuật toán) nhờ ba cắt bỏ: gộp phần nhận biết hành vi vào một bảng duy nhất;
giữ 6 thuật toán thay vì 14, những thuật toán còn lại chỉ được nhắc tên; và bỏ
phần liệt kê công nghệ theo tầng — nó thuộc về phụ lục chứ không thuộc về lập
luận thiết kế.

⚠ ĐỪNG SỬA TAY TỆP .docx. Chạy lại là dựng lại.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx import Document                                    # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH                # noqa: E402
from docx.shared import Pt                                   # noqa: E402

import chuong3_v3_a                                          # noqa: E402
import chuong3_v3_b                                          # noqa: E402
from chuong3_v3_khung import SO, cham, do, doan, sn          # noqa: E402

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs" / "Chuong3_Luan_van_v3.docx"

TLTK = [
    "Baker, R. S. J. d., Corbett, A. T., & Aleven, V. (2008). More accurate "
    "student modeling through contextual estimation of slip and guess "
    "probabilities in Bayesian Knowledge Tracing. In Intelligent Tutoring "
    "Systems (pp. 406–415). Springer.",

    "Bộ Giáo dục và Đào tạo (2018). Chương trình giáo dục phổ thông môn Tiếng "
    "Anh (ban hành kèm Thông tư số 32/2018/TT-BGDĐT ngày 26-12-2018).",

    "Chen, P., Lu, Y., Zheng, V. W., Chen, X., & Yang, B. (2018). KnowEdu: A "
    "system to construct knowledge graph for education. IEEE Access, 6, "
    "31553–31563.",

    "Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the "
    "acquisition of procedural knowledge. User Modeling and User-Adapted "
    "Interaction, 4(4), 253–278.",

    "Council of Europe (2020). Common European Framework of Reference for "
    "Languages: Learning, teaching, assessment — Companion volume. Council of "
    "Europe Publishing.",

    "Doignon, J.-P., & Falmagne, J.-C. (1985). Spaces for the assessment of "
    "knowledge. International Journal of Man-Machine Studies, 23(2), 175–196.",

    "Ebbinghaus, H. (1885/1913). Memory: A Contribution to Experimental "
    "Psychology. Teachers College, Columbia University.",

    "Hogan, A., Blomqvist, E., Cochez, M., d’Amato, C., de Melo, G., Gutierrez, "
    "C., … Zimmermann, A. (2021). Knowledge Graphs. ACM Computing Surveys, "
    "54(4), Article 71.",

    "Leitner, S. (1972). So lernt man lernen. Herder.",

    "Lewis, P., et al. (2020). Retrieval-augmented generation for "
    "knowledge-intensive NLP tasks. Advances in Neural Information Processing "
    "Systems, 33, 9459–9474.",

    "Liu, Q., Shen, S., Huang, Z., Chen, E., & Zheng, Y. (2021). A survey of "
    "knowledge tracing. arXiv:2105.15106.",

    "Nedungadi, P., & Remya, M. S. (2014). Incorporating forgetting in the "
    "Bayesian Knowledge Tracing model. 2014 IEEE International Conference on "
    "Advanced Communications, Control and Computing Technologies, 1686–1689.",

    "Pelánek, R. (2015). Bayesian knowledge tracing, logistic models, and "
    "beyond: An overview of learner modeling techniques. User Modeling and "
    "User-Adapted Interaction, 25(4), 313–350.",

    "Piech, C., Bassen, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & "
    "Sohl-Dickstein, J. (2015). Deep knowledge tracing. Advances in Neural "
    "Information Processing Systems, 28, 505–513.",

    "Settles, B., & Meeder, B. (2016). A trainable spaced repetition model for "
    "language learning. Proceedings of the 54th Annual Meeting of the "
    "Association for Computational Linguistics (Volume 1: Long Papers), "
    "1848–1858.",

    "Vygotsky, L. S. (1978). Mind in Society: The Development of Higher "
    "Psychological Processes. Harvard University Press.",
]


def _bia(d):
    t = d.add_heading("CHƯƠNG 3", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t2 = d.add_heading(
        "THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG HỌC TẬP THÍCH ỨNG CHO MÔN TIẾNG ANH",
        level=0)
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph()

    doan(d,
         "Chương 2 đã trình bày cơ sở lý thuyết và công nghệ liên quan. Chương "
         "này chuyển các cơ sở ấy thành một thiết kế cụ thể cho bài toán dạy "
         "tiếng Anh bậc tiểu học, và trình bày theo một trật tự khác với trật "
         "tự đặc tả thông thường: trước hết là cách BIỂU DIỄN — đồ thị tri thức "
         "thành hình ra sao, được cài đặt trên máy thế nào, một phiên làm việc "
         "của một cá nhân lưu những gì; sau đó là các PHƯƠNG PHÁP — tiêu chí "
         "phát hiện lỗ hổng, thủ tục chẩn đoán, phương pháp gợi ý can thiệp; và "
         "cuối cùng là một VÍ DỤ ĐẦY ĐỦ chạy toàn bộ thiết kế ấy trên một phiên "
         "của một người học, từ trạng thái trước phiên tới bài phụ đạo được "
         "dựng ra và con số hiệu quả đo được.")
    doan(d,
         "Trật tự ấy phục vụ một mục đích: mọi khái niệm trình bày ở nửa đầu "
         "chương đều xuất hiện trở lại ở mục 3.6 dưới dạng một con số cụ thể "
         "của một người học cụ thể, nên người đọc kiểm chứng được từng bước "
         "thay vì phải tin vào lời đặc tả.")

    p = d.add_paragraph()
    do(p, "Nguồn của số liệu trong chương. ", dam=True)
    do(p, "Toàn bộ thực thể, thuật toán, tham số và số liệu đều lấy từ hệ thống "
          "đã được hiện thực và đang vận hành. Riêng các bảng của mục 3.6 do "
          "một chương trình sinh ra bằng cách gọi trực tiếp chính các mô-đun "
          "đang chạy — hàm cập nhật Bayes của hàm nền, hàm định vị nút gốc rễ, "
          "hàm chính sách, hàm xếp câu theo vùng phát triển gần, hàm dựng bài "
          "phụ đạo và hàm dựng bản ghi — nên chạy lại chương trình ấy cho ra "
          "đúng các bảng trong chương. Ở những chỗ một tham số là giá trị được "
          "CHỌN theo lập luận sư phạm chứ chưa phải giá trị hiệu chỉnh từ dữ "
          "liệu thực nghiệm, điều đó được nêu tường minh ngay tại chỗ, và việc "
          "hiệu chỉnh tham số ấy trở thành một nội dung của các kịch bản thực "
          "nghiệm ở mục 3.9.")

    d.add_paragraph()
    p = d.add_paragraph()
    do(p, "Cấu trúc chương:", dam=True)
    cham(d, [
        ("3.1 · ", "phát biểu bài toán, sáu ràng buộc thiết kế đặc thù lứa tuổi "
         "tiểu học, kiến trúc bốn tầng và vòng lặp thích ứng."),
        ("3.2 · ", "đồ thị tri thức: quy trình thành hình sáu bước, định nghĩa "
         "hình thức và quy mô đặt bên cạnh tài liệu đã công bố, thuộc tính của "
         "đỉnh và của cạnh, và cài đặt trên máy — tập đỉnh cùng tập cạnh nằm ở "
         "bảng nào, đọc bằng mệnh đề điều kiện nào."),
        ("3.3 · ", "phiên làm việc của một cá nhân: định nghĩa phiên, bốn kho "
         "ghi, lược đồ đầy đủ của bản ghi lượt trả lời và của hồ sơ nút tri "
         "thức kèm bản ghi thật nguyên văn, mệnh đề điều kiện của phép ghi và "
         "phép đọc, bốn bất biến của kho lưu vết."),
        ("3.4 · ", "tiêu chí phát hiện lỗ hổng và thủ tục chẩn đoán: định nghĩa "
         "lỗ hổng gốc rễ, bốn tiêu chí phát hiện, mô hình Bayes có cơ chế quên, "
         "lan truyền ngược, sáu tình trạng và luật nhận dạng, bảy tín hiệu hành "
         "vi đầu vào."),
        ("3.5 · ", "phương pháp gợi ý can thiệp: hàm chính sách và ranh giới "
         "quyền quyết định, gợi ý thứ tự theo vùng phát triển gần, gợi ý nội "
         "dung bằng bài phụ đạo bốn bước, hậu kiểm tất định."),
        ("3.6 · ", "VÍ DỤ MINH HOẠ ĐẦY ĐỦ — một phiên của một người học cụ thể, "
         "mười ba bảng và hai hình, tất cả do chương trình sinh ra từ mã đang "
         "chạy."),
        ("3.7 · ", "mười ba câu hỏi phản biện điển hình và chỗ trả lời."),
        ("3.8 · ", "hệ thống độ đo bốn nhóm."),
        ("3.9 · ", "sáu kịch bản thực nghiệm và ba điều kiện tiền đề."),
        ("3.10 · ", "kết luận chương và chín giới hạn đã biết của thiết kế."),
    ])
    d.add_page_break()


def _tltk(d):
    d.add_heading("Tài liệu tham khảo bổ sung cho Chương 3", level=1)
    doan(d,
         "Danh mục dưới đây gồm các tài liệu được viện dẫn trong chương. Năm "
         "tài liệu là bổ sung so với danh mục của bản trước, và cả năm đều phục "
         "vụ phần biểu diễn tri thức ở mục 3.2: Doignon và Falmagne (nền tảng "
         "lý thuyết không gian tri thức), Hogan và cộng sự (quy ước đồ thị tri "
         "thức có nhãn), Chen và cộng sự (dựng đồ thị tri thức cho giáo dục), "
         "Liu và cộng sự cùng Piech và cộng sự (quy mô tập dữ liệu theo dõi tri "
         "thức, làm mốc so sánh ở Bảng 3.3).")
    for x in sorted(TLTK):
        p = d.add_paragraph(style="List Number")
        p.paragraph_format.space_after = Pt(4)
        do(p, x)


def main() -> int:
    d = Document()
    d.styles["Normal"].font.name = "Times New Roman"
    d.styles["Normal"].font.size = Pt(13)
    d.styles["Normal"].paragraph_format.space_after = Pt(6)

    _bia(d)
    chuong3_v3_a.viet(d)
    chuong3_v3_b.viet(d)
    d.add_page_break()
    _tltk(d)

    RA.parent.mkdir(parents=True, exist_ok=True)
    d.save(RA)
    print(f"đã ghi {RA.relative_to(GOC)}")
    print(f"   số liệu đối chiếu lúc {SO['docLuc']}")
    print(f"   đồ thị {sn(SO['doThi']['nut'])} nút · kho câu "
          f"{sn(SO['khoCau']['tong'])} câu")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
