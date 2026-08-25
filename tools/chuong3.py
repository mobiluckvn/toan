#!/usr/bin/env python3
"""
CHƯƠNG 3 LUẬN VĂN — sinh `docs/Chuong3_Luan_van.docx`.

Viết theo đúng khung Thầy chốt trong review:
  · xác định thực thể, thuộc tính của bài toán học tiếng Anh (biểu diễn bài toán)
  · phương pháp nhận biết hành vi   — đầu vào · đầu ra · thủ tục/thuật toán
  · phương pháp chẩn đoán lỗ hổng   — thông tin · thủ tục/thuật toán · công nghệ
  · phương pháp sinh bài, kiểm tra  — bài toán · thủ tục · công nghệ · độ đo
  · đề xuất kịch bản thực nghiệm và đánh giá

Nội dung tách ra bốn tệp `chuong3_p1.py` … `chuong3_p4.py`; hàm vẽ ở
`chuong3_khung.py`. Chạy lại là dựng lại — ĐỪNG sửa tay tệp .docx.

⚠ Mọi con số trong chương đều đối chiếu được với mã nguồn hoặc tệp dữ liệu đang
chạy ngày 25-08-2026. Chỗ nào là con số CHỌN chứ không phải con số ĐO đều được
nói ra tại chỗ — xem `docs/xac_nhan_chuong2.docx` để biết vì sao điều này quan
trọng.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx import Document                                    # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH                # noqa: E402
from docx.shared import Pt                                   # noqa: E402

import chuong3_p1, chuong3_p2, chuong3_p3, chuong3_p4        # noqa: E402
from chuong3_khung import do, doan, cham                     # noqa: E402

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs" / "Chuong3_Luan_van.docx"


TLTK = [
    "Baker, R. S. J. d., Corbett, A. T., & Aleven, V. (2008). More accurate "
    "student modeling through contextual estimation of slip and guess "
    "probabilities in Bayesian Knowledge Tracing. In Intelligent Tutoring "
    "Systems (pp. 406–415). Springer.",

    "Bloom, B. S. (1984). The 2 Sigma Problem: The search for methods of group "
    "instruction as effective as one-to-one tutoring. Educational Researcher, "
    "13(6), 4–16.",

    "Bộ Giáo dục và Đào tạo (2018). Chương trình giáo dục phổ thông môn Tiếng "
    "Anh (ban hành kèm Thông tư số 32/2018/TT-BGDĐT ngày 26-12-2018).",

    "Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the "
    "acquisition of procedural knowledge. User Modeling and User-Adapted "
    "Interaction, 4(4), 253–278.",

    "Council of Europe (2020). Common European Framework of Reference for "
    "Languages: Learning, teaching, assessment — Companion volume. Council of "
    "Europe Publishing.",

    "Ebbinghaus, H. (1885/1913). Memory: A Contribution to Experimental "
    "Psychology. Teachers College, Columbia University.",

    "Käser, T., Klingler, S., Schwing, A. G., & Gross, M. (2017). Dynamic "
    "Bayesian networks for student modeling. IEEE Transactions on Learning "
    "Technologies, 10(4), 450–462.",

    "Kasneci, E., et al. (2023). ChatGPT for good? On opportunities and "
    "challenges of large language models for education. Learning and Individual "
    "Differences, 103, 102274.",

    "Keller, J. M. (1987). Development and use of the ARCS model of "
    "instructional design. Journal of Instructional Development, 10(3), 2–10.",

    "Leitner, S. (1972). So lernt man lernen. Herder.",

    "Lewis, P., et al. (2020). Retrieval-augmented generation for "
    "knowledge-intensive NLP tasks. Advances in Neural Information Processing "
    "Systems, 33, 9459–9474.",

    "Nedungadi, P., & Remya, M. S. (2014). Incorporating forgetting in the "
    "Bayesian Knowledge Tracing model. 2014 IEEE International Conference on "
    "Advanced Communications, Control and Computing Technologies, 1686–1689.",

    "Pashler, H., McDaniel, M., Rohrer, D., & Bjork, R. (2008). Learning "
    "styles: Concepts and evidence. Psychological Science in the Public "
    "Interest, 9(3), 105–119.",

    "Pelánek, R. (2015). Bayesian knowledge tracing, logistic models, and "
    "beyond: An overview of learner modeling techniques. User Modeling and "
    "User-Adapted Interaction, 25(4), 313–350.",

    "Settles, B., & Meeder, B. (2016). A trainable spaced repetition model for "
    "language learning. Proceedings of the 54th Annual Meeting of the "
    "Association for Computational Linguistics (Volume 1: Long Papers), "
    "1848–1858.",

    "Sweller, J. (1988). Cognitive load during problem solving: Effects on "
    "learning. Cognitive Science, 12(2), 257–285.",

    "Vygotsky, L. S. (1978). Mind in Society: The Development of Higher "
    "Psychological Processes. Harvard University Press.",

    "Walkington, C. A. (2013). Using adaptive learning technologies to "
    "personalize instruction to student interests. Journal of Educational "
    "Psychology, 105(4), 932–945.",
]


def _bia(d):
    t = d.add_heading("CHƯƠNG 3", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t2 = d.add_heading(
        "THIẾT KẾ HỆ THỐNG HỌC THÍCH ỨNG CHO MÔN TIẾNG ANH TIỂU HỌC", level=0)
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    do(p, "Hệ thống đối chiếu: Kỹ Sư Nhí — ky-su-nhi.web.app, môn Tiếng Anh "
          "lớp 1–5", nghieng=True)

    d.add_paragraph()
    doan(d,
        "Chương 2 đã trình bày cơ sở lý thuyết và công nghệ liên quan. Chương "
        "này trình bày thiết kế cụ thể của hệ thống: cách bài toán học tiếng Anh "
        "ở bậc tiểu học được biểu diễn thành các thực thể và quan hệ máy tính xử "
        "lý được; ba phương pháp cốt lõi — nhận biết hành vi người học, chẩn "
        "đoán lỗ hổng kiến thức, sinh bài tập và kiểm tra — mỗi phương pháp kèm "
        "đầu vào, đầu ra, thủ tục và công nghệ sử dụng; hệ thống độ đo đánh giá; "
        "và các kịch bản thực nghiệm đề xuất.")

    doan(d,
        "Mọi thực thể, thuật toán, tham số và số liệu trình bày trong chương đều "
        "lấy từ hệ thống đã hiện thực và đang vận hành, đối chiếu tại thời điểm "
        "25-08-2026. Ở những chỗ một tham số là giá trị CHỌN chứ không phải giá "
        "trị hiệu chỉnh từ dữ liệu, điều đó được nêu ngay tại chỗ, và việc hiệu "
        "chỉnh nó trở thành một nội dung của các kịch bản thực nghiệm ở mục 3.7.")

    d.add_paragraph()
    p = d.add_paragraph()
    do(p, "Cấu trúc chương:", dam=True)
    cham(d, [
        ("3.1 · ", "Phát biểu bài toán, sáu ràng buộc thiết kế đặc thù lứa tuổi "
         "tiểu học, và kiến trúc bốn tầng."),
        ("3.2 · ", "Biểu diễn bài toán: ba miền thực thể, đồ thị tri thức có "
         "nhãn, lược đồ đầy đủ của sáu thực thể miền người học, vector trạng "
         "thái bốn chiều, và bốn bất biến của kho lưu vết."),
        ("3.3 · ", "Phương pháp nhận biết hành vi: bảy loại hành vi và bốn thuật "
         "toán, kèm cỡ mẫu tối thiểu và giới hạn của từng phép suy luận."),
        ("3.4 · ", "Phương pháp chẩn đoán lỗ hổng: mô hình Bayes có cơ chế quên, "
         "lan truyền chẩn đoán hai chiều trên đồ thị, ma trận trạng thái, hàm "
         "chính sách, và quy đổi mức phủ vốn sang thang năng lực."),
        ("3.5 · ", "Phương pháp sinh bài tập và kiểm tra: hai chế độ sinh và "
         "tiêu chí phân định, đường ống sinh nội dung tĩnh, kiến trúc tạo sinh "
         "tăng cường truy xuất bốn bước, bốn cấp kiểm tra, và công nghệ sử dụng."),
        ("3.6 · ", "Hệ thống độ đo bốn nhóm: mô hình · sư phạm · an toàn nội "
         "dung · hệ thống và vận hành."),
        ("3.7 · ", "Tám kịch bản thực nghiệm, ma trận kịch bản × độ đo, và các "
         "đe doạ tính hiệu lực."),
        ("3.8 · ", "Kết luận chương."),
    ])
    d.add_page_break()


def _tltk(d):
    d.add_heading("Tài liệu tham khảo của Chương 3", level=1)
    doan(d,
        "Danh mục dưới đây gồm các tài liệu được viện dẫn trong Chương 2 và "
        "Chương 3. Bảy tài liệu là bổ sung mới so với danh mục của Chương 2 "
        "phiên bản trước: Vygotsky và Bloom (đã được trích dẫn trong thân bài "
        "Chương 2 nhưng thiếu mục tương ứng), Council of Europe và Chương trình "
        "giáo dục phổ thông 2018 (căn cứ của phép quy đổi thang năng lực ở mục "
        "3.4.8), Leitner (lịch lặp lại ngắt quãng ở mục 3.2.4), Baker và cộng sự "
        "(tham số theo ngữ cảnh câu hỏi ở mục 3.4.3), và Ebbinghaus (đường cong "
        "quên ở mục 3.4.3).")
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
    chuong3_p1.viet(d)
    chuong3_p2.viet(d)
    chuong3_p3.viet(d)
    chuong3_p4.viet(d)
    d.add_page_break()
    _tltk(d)

    RA.parent.mkdir(parents=True, exist_ok=True)
    d.save(RA)
    print(f"đã ghi {RA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
