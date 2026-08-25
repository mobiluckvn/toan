#!/usr/bin/env python3
"""
ÁP CHÍN MỤC SỬA MỚI VÀO CHƯƠNG 2.

    docs/Chuong2_Luan_van_Thac_sy_1_v3.docx  →  docs/Chuong2_Luan_van_Thac_sy_1_v4.docx

Chín mục là những chỗ tìm được ngày 25-08-2026, đánh dấu ★ trong
`docs/xac_nhan_chuong2.docx`. Bản 23-08 (`sua_chuong2.docx`) chưa có mục nào
trong số này.

    A-5  quy mô đồ thị và bản chất tập cạnh E      → 2.2.1.b · 2.2.2.b
    A-6  ba ví dụ mã nút sai                       → 2.2.2.c · 2.3.3.c
    A-7  Bảng 2.1 khai tên trường không có         → 2.3.1
    B-4  hệ thống là LAI, không thuần tạo sinh     → 2.4.1
    B-6  π khuyến nghị, không gác đường            → 2.5.1
    C-5  "liên tục thử nghiệm định dạng" nói quá   → 2.1.2.c
    C-6  cơ chế quên — cho dạng công thức          → 2.3.2.c
    C-7  câu bắt buộc đúng dùng tham số riêng      → 2.3.2.b
    C-8  bốn bất biến của kho lưu vết              → 2.5.2

⚠ CHƯA ÁP mười ba mục còn lại của bản 23-08, trong đó có A-1 (ngưỡng θ = 0,95
  phải sửa thành 0,85). Bác muốn áp nốt thì bảo — chúng nằm sẵn trong
  `docs/xac_nhan_chuong2.docx`.

⚠ KHÔNG ĐỘNG VÀO BẢN v3. Chạy lại là dựng lại v4 từ v3, nên đừng sửa tay v4.
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

GOC = Path(__file__).resolve().parent.parent
VAO = GOC / "docs" / "Chuong2_Luan_van_Thac_sy_1_v3.docx"
RA = GOC / "docs" / "Chuong2_Luan_van_Thac_sy_1_v4.docx"


# ─────────────────────────────────────────────────────────────────────────────
# thao tác trên tài liệu — giữ nguyên định dạng của đoạn gốc
# ─────────────────────────────────────────────────────────────────────────────
def _rpr_mau(p):
    """Lấy một khối định dạng ký tự làm khuôn. Ưu tiên run KHÔNG in đậm."""
    for r in p.runs:
        if not r.bold:
            e = r._element.find(qn("w:rPr"))
            if e is not None:
                return copy.deepcopy(e)
    for r in p.runs:
        e = r._element.find(qn("w:rPr"))
        if e is not None:
            return copy.deepcopy(e)
    return None


def dat_chu(p, phan):
    """
    Ghi lại nội dung một đoạn. `phan` là chuỗi, hoặc danh sách (chữ, in_đậm).

    Xoá hết run cũ rồi dựng run mới từ khuôn định dạng — không dùng lối gán
    `runs[0].text` vì đoạn nào có run đầu in đậm (kiểu "- Nguyên lý: ") thì cả
    đoạn sẽ thành in đậm.
    """
    if isinstance(phan, str):
        phan = [phan]
    # phần tử là chuỗi thì coi như không in đậm; là cặp thì tôn trọng cờ đậm
    phan = [(x, False) if isinstance(x, str) else tuple(x) for x in phan]
    mau = _rpr_mau(p)
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    for chu, dam in phan:
        r = p.add_run()
        if mau is not None:
            r._element.insert(0, copy.deepcopy(mau))
        r.text = chu
        r.bold = dam


def chen_sau(p, ds, mau=None):
    """Chèn các đoạn mới NGAY SAU đoạn `p`, sao định dạng đoạn từ `mau`."""
    goc = mau if mau is not None else p
    truoc = p._p
    ra = []
    for phan in ds:
        el = copy.deepcopy(goc._p)
        moi = Paragraph(el, p._parent)
        dat_chu(moi, phan)
        truoc.addnext(el)
        truoc = el
        ra.append(moi)
    return ra


class Ch2:
    def __init__(self, d):
        self.d = d
        self.da_sua = []

    def tim(self, dau, mo_ta=""):
        """Đoạn ĐẦU TIÊN bắt đầu bằng `dau`. Không thấy thì dừng hẳn."""
        for p in self.d.paragraphs:
            if p.text.strip().startswith(dau):
                return p
        raise SystemExit(f"KHÔNG THẤY đoạn bắt đầu bằng: {dau[:60]!r} ({mo_ta})")

    def thay(self, ma, dau, phan):
        p = self.tim(dau, ma)
        dat_chu(p, phan)
        self.da_sua.append((ma, "thay", dau[:48]))
        return p

    def them(self, ma, sau_dau, ds, mau_dau=None):
        p = self.tim(sau_dau, ma)
        mau = self.tim(mau_dau, ma) if mau_dau else None
        chen_sau(p, ds, mau)
        self.da_sua.append((ma, f"thêm {len(ds)} đoạn", sau_dau[:48]))
        return p


B = True   # in đậm


# ═════════════════════════════════════════════════════════════════════════════
def main() -> int:
    if not VAO.exists():
        print(f"không có {VAO}", file=sys.stderr)
        return 1
    d = Document(str(VAO))
    c = Ch2(d)

    # ── C-5 · 2.1.2.c — "liên tục thử nghiệm các định dạng" nói quá ──────────
    c.thay("C-5",
        "- Nguyên lý: Hệ thống thu thập dữ liệu lưu vết để xác định mức độ ưu tiên",
        [("- Nguyên lý: ", B),
         "Hệ thống thu thập dữ liệu lưu vết để xác định mức độ ưu tiên định dạng "
         "(Format Preference) của từng học sinh (ví dụ: học sinh A phản hồi tốt "
         "với câu hỏi Trắc nghiệm hình ảnh, học sinh B làm tốt hơn ở dạng Xếp "
         "thẻ thành câu). Hệ thống hiện thực sáu định dạng câu hỏi và giữ cho "
         "mỗi định dạng một cặp (số câu trả lời đúng, tổng số câu), trong đó chỉ "
         "tính lượt trả lời ĐẦU của mỗi câu — tính cả lượt thử lại thì định dạng "
         "nào cho phép thử nhiều lần một cách tự nhiên sẽ có tỷ lệ đúng thấp "
         "hơn, mà đó là tính chất của định dạng chứ không phải của học sinh. Kết "
         "quả đo được dùng làm khóa sắp xếp PHỤ: nhóm theo Vùng phát triển gần "
         "vẫn quyết định trước, chiều Sư phạm chỉ sắp lại thứ tự trong cùng một "
         "nhóm, không thay đổi tỷ lệ các định dạng trong một bài và không loại "
         "bỏ câu hỏi nào. Luật sắp xếp đảo chiều theo vùng: ở nơi học sinh còn "
         "chông chênh thì đưa định dạng học sinh MẠNH lên trước, để độ khó của "
         "nội dung không chồng thêm độ khó của cách hỏi; ở nơi đã tinh thông thì "
         "đưa định dạng học sinh YẾU lên trước, vì đó là chỗ ít rủi ro nhất để "
         "làm quen một cách hỏi còn ngại."])

    c.them("C-5",
        "- Nguyên lý: Hệ thống thu thập dữ liệu lưu vết để xác định mức độ ưu tiên",
        [[("- Ràng buộc về cỡ mẫu: ", B),
          "Mọi kết luận về định dạng đều đòi hỏi tối thiểu tám lượt trả lời cho "
          "định dạng đó; dưới ngưỡng này hệ thống trả về trạng thái “chưa đủ dữ "
          "liệu” chứ không trả về “học sinh yếu định dạng này”. Ràng buộc này "
          "chặn một vòng lặp tự củng cố: nếu hệ thống kết luận sớm rằng học sinh "
          "yếu một định dạng, nó sẽ giảm số câu thuộc định dạng ấy, khiến cỡ mẫu "
          "không bao giờ tăng thêm và kết luận sai tự nuôi chính nó."]])

    # ── A-5a · 2.2.1.b — quy mô đồ thị và hai hàm nhãn ───────────────────────
    c.thay("A-5a",
        "Về mặt toán học, cấu trúc chương trình Tiếng Anh tiểu học",
        "Về mặt toán học, chương trình giáo dục Tiếng Anh được số hóa thành một "
        "Đồ thị tri thức có hướng, CÓ NHÃN trên cả đỉnh lẫn cạnh:")

    c.thay("A-5a", "G = (V, E)", "G = (V, E, τ, λ)")

    c.thay("A-5a", "Trong đó, bộ bản thể học (Ontology)",
        "trong đó τ : V → T là hàm gán loại cho đỉnh (17 loại) và λ : E → R là "
        "hàm gán loại quan hệ cho cạnh (29 loại). Đồ thị được số hóa cho toàn bộ "
        "chương trình phổ thông từ Lớp 1 đến Lớp 12, gồm 3 989 đỉnh và 7 602 "
        "cạnh; riêng phần thuộc cấp tiểu học (Lớp 1–5) là 1 189 đỉnh. Việc số "
        "hóa vượt quá phạm vi tiểu học là có chủ ý: nó cho phép các ràng buộc "
        "tiên quyết xuyên cấp tồn tại thật trong dữ liệu thay vì bị cắt cụt ở "
        "ranh giới Lớp 5. Trên nền đó, bộ bản thể học (Ontology) của hệ thống "
        "được định nghĩa chi tiết như sau:")

    # ── A-5b · 2.2.2.b — REQUIRES là TẬP CON của E ───────────────────────────
    c.thay("A-5b", "Về mặt toán học, chương trình giáo dục Tiếng Anh được biểu diễn",
        "Như đã định nghĩa ở mục 2.2.1, chương trình giáo dục Tiếng Anh được "
        "biểu diễn dưới dạng một Đồ thị có hướng, có nhãn G = (V, E, τ, λ), "
        "trong đó:")

    c.thay("A-5b", "- Tập hợp các Cạnh E đại diện cho các Ràng buộc tiên quyết",
        [("- Tập hợp các Cạnh E ", B),
         "chứa 29 loại quan hệ khác nhau. Ràng buộc tiên quyết chỉ là một TẬP "
         "CON của tập cạnh ấy: E_prereq = { e ∈ E : λ(e) = REQUIRES }, gồm 583 "
         "cạnh trên tổng số 7 602 cạnh của đồ thị."])

    c.them("A-5b", "- Tập hợp các Cạnh E ",
        ["Việc phân biệt tập con này không phải là chi tiết kỹ thuật mà là điều "
         "kiện đúng đắn của cơ chế chẩn đoán trình bày ở mục 2.3.3. Nếu phép "
         "duyệt ngược chạy trên toàn bộ tập cạnh E, nó sẽ đi qua cả các quan hệ "
         "cấu thành — riêng quan hệ CONTAINS đã có 3 336 cạnh — và cho ra kết "
         "luận vô nghĩa về mặt sư phạm, kiểu “nguyên nhân học sinh trả lời sai "
         "là vì chưa nắm được cả Unit 3”. Do đó mọi thuật toán chẩn đoán trong "
         "nghiên cứu này đều ràng buộc trên tập cạnh đã lọc theo nhãn, chứ không "
         "trên E."])

    # ── A-6a · 2.2.2.c — hai trục tịnh tiến ──────────────────────────────────
    c.thay("A-6a", "- Trục tịnh tiến Ngữ pháp (Grammar Progression)",
        [("- Trục tịnh tiến Ngữ pháp (Grammar Progression): ", B),
         "Cấu trúc câu phát triển từ dạng hạt nhân thành dạng phức hợp, và sự "
         "phát triển này vượt qua ranh giới khối lớp. Ví dụ minh họa dưới đây "
         "được đối chiếu trực tiếp trên đồ thị đang vận hành: để nắm được mẫu "
         "hỏi–đáp về hoạt động đang diễn ra ở Lớp 2 (Nút sp_g2_u5_1), người học "
         "bị ràng buộc bởi Thể khẳng định của Thì hiện tại tiếp diễn đã học ở "
         "Lớp 1 (Nút sp_g1_u11_1). Đây là một trong 38 cạnh tiên quyết xuyên lớp "
         "của đồ thị lúc chạy, được đánh dấu bằng thuộc tính cross_grade."])

    c.thay("A-6a", "- Trục tịnh tiến Từ vựng (Vocabulary Progression)",
        [("- Trục tịnh tiến Từ vựng (Vocabulary Progression): ", B),
         "Khái niệm từ vựng không đứng độc lập mà là thành phần bắt buộc để lấp "
         "đầy các khe (target_vocab_slots) trong cấu trúc câu. Tuy nhiên, cần "
         "phân biệt hai loại liên kết giữa các nút từ vựng, vì chúng có ý nghĩa "
         "sư phạm khác hẳn nhau. Loại thứ nhất là ràng buộc tiên quyết thật, "
         "biểu diễn bằng cạnh REQUIRES của bản đồ gốc hoặc bằng cạnh bắc cầu "
         "giữa hai bài thuộc cùng một thang từ vựng có thứ tự. Loại thứ hai chỉ "
         "là thứ tự ĐỌC của hai từ liền nhau trong CÙNG một bài — chẳng hạn cặp "
         "v_g2_u14_eighteen → v_g2_u14_nineteen thuộc loại này. Loại thứ hai "
         "KHÔNG phải là cửa ải sư phạm, bởi sách giáo khoa dạy cả khối từ trong "
         "một buổi; hệ thống vì vậy loại hẳn nó khỏi mọi phép duyệt chẩn đoán. "
         "Sự phân biệt này có hệ quả trực tiếp: coi thứ tự đọc là ràng buộc tiên "
         "quyết sẽ khóa người học ngay giữa chính bài đang mở."])

    # ── A-7 · 2.3.1 Bảng 2.1 — thay bằng lược đồ THẬT ────────────────────────
    _bang_21(c)

    # ── C-7 · 2.3.2.b — tham số riêng cho câu bắt buộc đúng ──────────────────
    c.them("C-7", "- P(S) - Xác suất sơ suất",
        ["Bốn tham số trên không đồng nhất trên mọi câu hỏi. Những câu được "
         "người soạn đánh dấu Bắt buộc đúng — các câu bẫy đặt vào đúng chỗ hiểu "
         "sai phổ biến — sử dụng bộ tham số riêng với P(G) = 0,15 và P(S) = 0,06 "
         "thay cho 0,30 và 0,10. Căn cứ của việc phân biệt: trả lời đúng một câu "
         "bẫy nhờ đoán mò khó hơn hẳn, nên tín hiệu quan sát được ở đó đáng tin "
         "cậy hơn; đối xứng lại, trả lời sai một câu bẫy kéo xác suất nắm vững "
         "xuống mạnh hơn so với trả lời sai một câu thường. Đây là một dạng cá "
         "thể hóa tham số theo ĐƠN VỊ CÂU HỎI thay vì theo người học, có chi phí "
         "ước lượng thấp hơn nhiều mà vẫn nắm bắt được phần lớn khác biệt giữa "
         "các câu hỏi (Baker et al., 2008)."])

    # ── C-6 · 2.3.2.c — cơ chế quên, đặt thành Bước 0 ────────────────────────
    c.them("C-6", "Mục tiêu của thuật toán BKT là liên tục tính toán",
        [[("Bước 0: Hiệu chỉnh theo thời gian (Cơ chế quên)", B)],

         "Do việc thụ đắc ngôn ngữ mang bản chất hao hụt theo thời gian, trước "
         "khi áp dụng Định lý Bayes, hệ thống hiệu chỉnh xác suất nắm vững theo "
         "khoảng thời gian Δt (tính bằng ngày) kể từ lần tương tác gần nhất với "
         "nút tri thức:",

         [("P′(Lₙ₋₁) = 0,5 + [ P(Lₙ₋₁) − 0,5 ] × 2^(−Δt / h)", B)],

         "trong đó h là nửa đời của trí nhớ, đặt h = 14 ngày. Điểm cần nhấn "
         "mạnh: hàm kéo xác suất về 0,5 chứ KHÔNG kéo về 0. Người học quên một "
         "kiến thức thì trạng thái trở thành “không chắc chắn”, chứ không trở "
         "thành “chưa từng biết”; kéo về 0 tương đương với việc bắt học lại từ "
         "đầu một nội dung đã từng tinh thông, và với học sinh tiểu học thì đó "
         "là hình phạt cho việc nghỉ vài ngày. Hệ quả thứ hai của lựa chọn này "
         "nghe có vẻ nghịch lý nhưng đúng về mặt mô hình: một nút mà người học "
         "từng trả lời sai nhiều (P(L) thấp) sẽ NHÍCH LÊN theo thời gian, bởi "
         "đại lượng bị phân rã ở đây là độ tin cậy của hệ thống vào hiểu biết "
         "hiện có về người học, không phải năng lực của bản thân người học. Bản "
         "ghi không có dấu thời gian thì không phân rã — thà không phân rã còn "
         "hơn phân rã theo một mốc suy đoán.",

         "Cần khai báo rõ: giá trị h = 14 ngày là giá trị được CHỌN theo lịch "
         "lặp lại ngắt quãng sẵn có (+1, +3, +7 ngày) chứ chưa phải giá trị hiệu "
         "chỉnh từ dữ liệu học thật. Người học theo đúng lịch ôn sẽ gặp lại nút "
         "tri thức trước khi xác suất rơi đáng kể; nghỉ hẳn hai tuần thì mới "
         "thấy tụt. Việc hiệu chỉnh h bằng thực nghiệm là một nội dung được đề "
         "xuất ở chương sau."])

    # ── A-6b · 2.3.3.c — chuỗi lan truyền ngược ──────────────────────────────
    c.thay("A-6b", "- Minh họa thực nghiệm: Khi học sinh Lớp 3 làm sai liên tục",
        [("- Minh họa thực nghiệm (đã đối chiếu trên đồ thị đang vận hành): ", B),
         "Khi học sinh Lớp 3 làm sai liên tục mẫu câu hỏi tuổi “How old is he?” "
         "(Nút sp_g3_u11_2), thuật toán BKT truyền thống chỉ ghi nhận rằng học "
         "sinh yếu mẫu câu này. Với BKT cải tiến, hệ thống duyệt ngược theo cạnh "
         "tiên quyết và thu được chuỗi ba bước: sp_g3_u11_2 → sp_g3_u2_2 (bước "
         "1) → sp_g3_u1_1 (bước 2) → sp_g2_greeting (bước 3). Nghĩa là hệ thống "
         "tự động đưa ra giả thuyết rằng vùng khủng hoảng kiến thức có thể nằm ở "
         "mẫu chào hỏi của Lớp 2, và lan truyền một lực trừ (penalty) làm giảm "
         "xác suất P(L) của các nút nền tảng ấy theo hệ số suy giảm α lũy thừa "
         "số bước. Độ ngờ của mỗi nút được tính bằng α^k × (1 − P(L)), cần cả "
         "hai thành phần: α^k vì nguyên nhân càng xa chỗ sai thì càng khó gọi là "
         "nguyên nhân theo nghĩa dạy được, và (1 − P(L)) vì một nút người học đã "
         "vững thì không phải thủ phạm, dù nó là tiên quyết."])

    # ── B-4 · 2.4.1 — định vị LAI trên trục lựa chọn – tạo sinh ──────────────
    c.them("B-4", "- Phản hồi có tính giải thích (Explainable Feedback)",
        [[("Định vị của hệ thống đề xuất trên trục lựa chọn – tạo sinh. ", B),
          "Cần nói rõ rằng hệ thống trong nghiên cứu này không chuyển hoàn toàn "
          "sang chế độ tạo sinh thời gian thực, mà chọn một vị trí LAI, và việc "
          "chọn vị trí lai là một quyết định thiết kế có căn cứ chứ không phải "
          "một phần chưa hoàn thiện. Toàn bộ 4 226 câu hỏi của phần học chính — "
          "gồm 3 756 câu luyện tập ở ba bậc độ khó và 470 câu sát hạch — được "
          "sinh TRƯỚC bằng bộ sinh tất định và đi qua 92 phép kiểm tự động trước "
          "khi tới tay người học. Mô hình Ngôn ngữ Lớn chỉ được gọi ở ba vị trí "
          "mà nội dung tĩnh không phục vụ được: sinh bài tập phụ đạo khi kho "
          "tĩnh không đủ câu cho nút gốc rễ, đối thoại trong phòng luyện nói, và "
          "chấm bài viết ngắn kèm giải thích lỗi."],

         "Lý do của ranh giới này thuộc về đặc thù đối tượng người dùng. Với học "
         "sinh từ 6 đến 11 tuổi, một câu hỏi sai ngữ pháp hoặc một từ vượt cấp "
         "không phải là phiền toái mà là dạy sai, và trẻ sẽ ghi nhớ nội dung sai "
         "đó. Nội dung tĩnh cho phép kiểm duyệt TRƯỚC khi phân phối; nội dung "
         "tạo sinh thời gian thực chỉ kiểm duyệt được SAU khi sinh. Do đó hệ "
         "thống đặt nội dung tạo sinh ở đúng những vị trí mà giá trị cá nhân hóa "
         "vượt được rủi ro, và ở những vị trí ấy vẫn buộc mọi kết quả đi qua "
         "tầng hậu kiểm trình bày ở mục 2.4.3."])

    # ── B-6 · 2.5.1 — ranh giới quyền quyết định của π ───────────────────────
    c.them("B-6", "- Can thiệp phụ đạo (Remediation Intervention)",
        [[("Ranh giới quyền quyết định của Hàm chính sách. ", B),
          "Một điểm thiết kế cần được nêu rõ để tránh hiểu nhầm: Hàm chính sách "
          "π trả lời câu hỏi NÊN LÀM GÌ TIẾP THEO, nhưng không trả lời câu hỏi "
          "NGƯỜI HỌC CÓ ĐƯỢC ĐI TIẾP HAY KHÔNG. Quyền thứ hai thuộc về một bộ "
          "quy tắc điều hướng riêng biệt, với đúng một điều kiện: người học được "
          "mở nội dung kế tiếp khi đã ĐẠT, HOẶC đã thử thật ít nhất hai lần."],

         "Vế thứ hai là lưới an toàn, và nó tồn tại vì một lý do sư phạm không "
         "thương lượng được: mọi mô hình đánh giá xác suất đều có thể sai, và "
         "nếu quyền mở đường học nằm hoàn toàn trong tay mô hình thì một học "
         "sinh bị đánh giá nhầm sẽ mắc kẹt vĩnh viễn tại một bài học — không có "
         "cách nào tự thoát ra, và cũng không có cách nào báo cho hệ thống biết. "
         "Với trẻ nhỏ, điều học được trong tình huống đó không phải là môn học "
         "mà là niềm tin rằng bản thân mình học kém. Cùng một quy tắc được áp "
         "dụng nguyên vẹn ở ba cấp — mở bài học kế tiếp, mở chặng kế tiếp trong "
         "bài, và cho phép để lại một câu hỏi làm sau — để người học chỉ phải "
         "hiểu luật ấy một lần rồi áp dụng ở mọi nơi. Bài học đi vòng theo lưới "
         "an toàn KHÔNG được ghi nhận là đã đạt: nó nằm trong danh sách còn nợ, "
         "mang nhãn riêng, và phải hoàn thành mới mở được kỳ ôn tập chương."])

    # ── C-8 · 2.5.2 — bốn bất biến của kho lưu vết ───────────────────────────
    c.them("C-8", "- Dữ liệu Bối cảnh Hệ thống (System Context)",
        [[("Bốn bất biến của kho lưu vết. ", B),
          "Kiến trúc lưu vết hướng sự kiện chỉ mang lại giá trị nếu kho sự kiện "
          "giữ được một số bất biến, và các bất biến này phải kiểm tra được bằng "
          "chương trình chạy tự động thay vì bằng niềm tin vào mã nguồn. Lý do: "
          "một kho sự kiện có thể hỏng trong im lặng. Mọi độ đo về mô hình người "
          "học và về tiến bộ học tập đều đứng trên giả định “nhật ký đầy đủ và "
          "đúng chủ sở hữu”, mà nếu giả định ấy sai thì bản thân các kết quả "
          "không hề bộc lộ điều đó. Nghiên cứu này đề xuất bốn bất biến sau:"],

         [("(1) Mỗi phiên một chủ sở hữu. ", B),
          "Một mã phiên chỉ sinh ra tại một lần mở bài của một người học, nên "
          "hai người học cùng mang một mã phiên là dấu hiệu dữ liệu đã bị gán "
          "nhầm chủ."],

         [("(2) Dãy số thứ tự liền mạch. ", B),
          "Mã định danh bản ghi nhúng số thứ tự của lượt trả lời trong phiên, "
          "nên dãy phải liền; chỗ thủng là dấu hiệu mất bản ghi giữa chừng. Phép "
          "kiểm phải nhóm theo bộ ba (người học, phiên, bài học) chứ không theo "
          "riêng mã phiên — một phiên đi qua hai bài thì số thứ tự lặp lại là "
          "hợp lệ."],

         [("(3) Mô hình suy được từ nhật ký. ", B),
          "Tổng số lượt ghi trong hồ sơ mỗi nút tri thức phải bằng đúng số bản "
          "ghi còn lại của nút ấy, và việc dựng lại toàn bộ hồ sơ từ nhật ký gốc "
          "phải cho ra kết quả trùng khớp."],

         [("(4) Không nút tri thức nào có lượt trả lời mà thiếu hồ sơ. ", B),
          "Đây là chiều ngược của bất biến (3), phát hiện trường hợp tầng tính "
          "toán nền không xử lý một loại sự kiện nào đó."],

         "Cần nêu kèm giới hạn của bốn phép kiểm này: chúng không phát hiện được "
         "việc mất phần đuôi của một phiên học. Nếu những lượt trả lời cuối cùng "
         "không bao giờ được đẩy lên máy chủ thì dãy số thứ tự vẫn liền mạch, "
         "chỉ ngắn hơn thực tế; muốn phát hiện phải đối chiếu với một nguồn dữ "
         "liệu độc lập hoặc đếm thủ công trong một buổi kiểm chứng."])

    # ── ĐỢT 2 · mười ba mục của bản 23-08 ───────────────────────────────────
    _dot2(c)

    # ── bổ sung bảy tài liệu tham khảo mà phần chữ mới trích tới ────────────
    _them_tltk(c)

    d.save(str(RA))

    print(f"đã ghi {RA}\n")
    print(f"{'MỤC':6s} {'VIỆC':14s} NEO")
    for ma, viec, neo in c.da_sua:
        print(f"{ma:6s} {viec:14s} {neo}…")
    print(f"\nTổng: {len(c.da_sua)} lần sửa cho 22 mục "
          "(9 mục đợt 25-08 + 13 mục đợt 23-08), cộng 7 tài liệu tham khảo.")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
def _bang_21(c):
    """
    A-7 · Thay khối JSON của Bảng 2.1 bằng LƯỢC ĐỒ THẬT của tài liệu `mastery`.

    Khối cũ khai `p_learned` · `struggle_count` · `last_interacted` — không
    trường nào tồn tại trong hệ thống — và mã học sinh mẫu `SV_20242344M` mang
    dạng mã học viên cao học chứ không phải mã người học tiểu học.
    """
    d = c.d
    p_cap = c.tim("Bảng 2.1:", "A-7")
    dat_chu(p_cap,
            "Bảng 2.1: Lược đồ dữ liệu thực tế của Bản sao số người học "
            "(Learner Digital Twin)")

    # ⚠ Khối JSON KHÔNG nằm ở thân tài liệu — nó nằm trong một ô bảng 1×1, nên
    #   `d.paragraphs` không thấy. Đã mất một lần chạy vì chỗ này.
    o = d.tables[0].rows[0].cells[0]
    khoi = list(o.paragraphs)
    if len(khoi) < 5 or khoi[0].text.strip() != "{":
        raise SystemExit("A-7: ô bảng không chứa khối JSON như mong đợi")

    mau = khoi[0]
    moi = [
        "hồ sơ người học      —  users/{learner_id}",
        "  learner_id   : \"u7Kd93RfQ2\"          // mã tài khoản",
        "  cefr         : suy ra từ mức phủ vốn tri thức, xem mục 2.3.1.c",
        "  preferences  : [\"animals\", \"sports\"]",
        "",
        "trạng thái che phủ   —  mastery/{learner_id}/units/{ma_nut}",
        "{",
        "  \"unit\"         : \"sp_g3_u2_2\",   // mã nút tri thức trên đồ thị G",
        "  \"p\"            : 0.45,           // P(Lₙ)   — mức thạo SAU lượt gần nhất",
        "  \"pTruoc\"       : 0.62,           // P(Lₙ₋₁) — mức thạo TRƯỚC lượt ấy",
        "  \"mastered\"     : false,          // p ≥ θ",
        "  \"nAttempts\"    : 7,              // tổng số lượt tại nút này",
        "  \"nCorrect\"     : 3,",
        "  \"saiLienTiep\"  : 3,              // S_c — số lần sai LIÊN TIẾP",
        "  \"msTrungBinh\"  : 12480,          // RT_avg (mili-giây); null khi chưa đo được",
        "  \"goiTrungBinh\" : 0.86,           // H_req — số gợi ý trung bình mỗi lượt",
        "  \"lastSeen\"     : 1755950400000,  // T_last — mốc chạm gần nhất",
        "  \"lastMicroId\"  : \"DL:TA3.B02\",",
        "  \"mon\"          : \"tienganh\"",
        "}",
    ]
    # Giữ lại đoạn ĐẦU làm neo (xoá hết thì ô bảng rỗng và Word báo hỏng tệp),
    # ghi đè nội dung nó, chèn phần còn lại phía sau, rồi mới xoá các đoạn cũ.
    dat_chu(khoi[0], moi[0])
    chen_sau(khoi[0], moi[1:], mau)
    for p in khoi[1:]:
        p._element.getparent().remove(p._element)

    p_nguon = next(p for p in c.d.paragraphs if p.text.strip().startswith("Nguồn:"))
    chen_sau(p_nguon, [
        "Lược đồ trên là hình dạng tài liệu thực tế mà tầng tính toán nền ghi ra "
        "sau mỗi lượt trả lời, không phải một minh họa khái niệm. Ánh xạ sang ký "
        "hiệu toán học đã dùng trong mục này: p ứng với P(Lₙ), pTruoc ứng với "
        "P(Lₙ₋₁), saiLienTiep ứng với S_c, msTrungBinh ứng với RT_avg, "
        "goiTrungBinh ứng với H_req, và lastSeen ứng với T_last. Hai trường "
        "pTruoc và p tồn tại song song vì hiệu số giữa chúng chính là chỉ số "
        "Biến thiên Tri thức ΔC dùng ở mục 2.5.3; nếu chỉ lưu giá trị sau thì "
        "phép đo hiệu quả can thiệp không thực hiện được. Trường msTrungBinh "
        "nhận giá trị null khi chưa có lượt nào đo được thời gian, chứ không "
        "nhận giá trị 0 — coi giá trị thiếu là 0 sẽ kéo trung bình xuống và biến "
        "“học sinh trả lời nhanh dần” thành một kết luận do lỗi ghi nhận sinh "
        "ra. Đặc tả đầy đủ của cả sáu thực thể thuộc miền người học được trình "
        "bày ở Chương 3, mục 3.2.4.",
    ])
    c.da_sua.append(("A-7", f"thay {len(khoi)} đoạn", "Bảng 2.1 — khối JSON"))


def _dot2(c):
    """
    Mười ba mục của bản `sua_chuong2.docx` ngày 23-08-2026.

        A-1  ngưỡng θ và ba khoảng giá trị        → 2.3.2.d · 2.3.3.c · 2.3.3.d · 2.5.1
        A-2  dữ liệu trước 23-08 không dùng được  → 2.5.2
        A-3  pha nào được tính vào BKT            → 2.3.2.c
        A-4  CEFR là quy ước bắc cầu              → 2.3.1.c
        A-8  RAG bước 3 — đúng kết quả, sai cơ chế→ 2.4.3
        B-1  hai bản của đồ thị                   → 2.2.1.d
        B-2  bộ truy xuất gộp hai nguồn           → 2.4.3 bước 1
        B-3  H_req là "đã thấy", không phải "đã xin" → 2.3.1.c
        B-5  thứ tự xét của hàm chính sách        → 2.5.1
        C-1  nhịp ghi gom lô, mã lũy đẳng         → 2.5.2
        C-2  công bố α và β                       → 2.3.3.c · 2.3.3.d
        C-3  mệt mỏi đo bằng hai tín hiệu         → 2.1.2.b
        C-4  giới hạn của phép đo phát âm         → 2.1.2.a
    """
    # ── C-4 · 2.1.2.a — giới hạn phép đo phát âm ────────────────────────────
    c.them("C-4", "- Cơ sở lý thuyết: Trạng thái nhận thức được lượng hóa",
        [[("- Giới hạn của phép đo kỹ năng nói: ", B),
          "Điểm phát âm được chấm bằng bộ nhận dạng giọng nói sẵn có của trình "
          "duyệt (Web Speech API). Con số này vì vậy phụ thuộc vào chất lượng "
          "micro và mức ồn của môi trường: cùng một người học, hai thiết bị khác "
          "nhau có thể cho kết quả khác nhau. Hệ thống vẫn đưa điểm này vào mô "
          "hình người học, nhưng gắn nhãn riêng cho ba dạng lượt nói để có thể "
          "tách ra khi cần một phép đo thuần nhất. Ràng buộc này cũng chi phối "
          "thiết kế điều hướng: không nội dung nào bị khóa theo điểm phát âm, "
          "bởi trẻ nói ngọng, trẻ nói giọng địa phương và trẻ dùng micro chất "
          "lượng thấp đều có thể không bao giờ chạm ngưỡng."]])

    # ── C-3 · 2.1.2.b — mệt mỏi đo bằng HAI tín hiệu ────────────────────────
    c.thay("C-3", "- Nguyên lý: Đối với việc thụ đắc ngôn ngữ",
        [("- Nguyên lý: ", B),
         "Đối với việc thụ đắc ngôn ngữ (Tiếng Anh), từ vựng và cấu trúc ngữ "
         "pháp sẽ dần bị lãng quên theo thời gian (Ebbinghaus, 1885). Do đó, hệ "
         "thống không chỉ đánh giá lúc học sinh vừa làm xong bài, mà còn tính "
         "toán sự hao hụt tri thức theo một hàm phân rã thời gian — dạng hàm cụ "
         "thể trình bày ở mục 2.3.2. Chiều thích ứng này được hiện thực bằng bốn "
         "thành phần: đường cong quên, lịch lặp lại ngắt quãng theo hộp Leitner "
         "với năm khoảng cách 1 · 3 · 7 · 14 · 30 ngày (Leitner, 1972), và HAI "
         "tín hiệu độc lập cho trạng thái mệt mỏi nhận thức."])

    c.them("C-3", "- Nguyên lý: Đối với việc thụ đắc ngôn ngữ",
        [[("Tín hiệu thứ nhất — CHẬM DẦN TRONG PHIÊN. ", B),
          "Hệ thống so sánh thời gian phản hồi trung bình của nửa đầu với nửa "
          "cuối trong cùng một phiên học, TÁCH RIÊNG THEO TỪNG ĐỊNH DẠNG câu "
          "hỏi, và chỉ kết luận khi mỗi nửa có tối thiểu ba lượt; chênh lệch từ "
          "25% trở lên thì báo là có dấu hiệu mệt mỏi. Việc tách theo định dạng "
          "là bắt buộc chứ không phải một tinh chỉnh: bài học đi theo thang độ "
          "khó tăng dần, nên câu cuối phiên vốn đã khó hơn và tốn thời gian hơn "
          "câu đầu; so sánh trực tiếp thì phiên học nào cũng cho ra kết quả “có "
          "dấu hiệu mệt”, và điều đó phản ánh thiết kế bài học chứ không phản "
          "ánh người học."],

         [("Tín hiệu thứ hai — BỎ DỞ. ", B),
          "Mỗi lần người học rời màn hình bài học khi chưa hoàn thành, hệ thống "
          "ghi một bản ghi gồm mã bài, chặng đang dở, số lượt đã làm và số giây "
          "đã ở trong bài; mỗi lần một bản ghi riêng chứ không gộp, bởi chính SỐ "
          "LẦN bỏ dở cùng một bài mới là tín hiệu. Tín hiệu này có một giới hạn "
          "phải nêu khi báo cáo: nó chỉ ghi được khi người học rời màn hình qua "
          "thao tác trong ứng dụng; đóng thẳng cửa sổ trình duyệt thì không ghi "
          "được. Con số thu được vì vậy là CẬN DƯỚI của số lần bỏ dở thật, dùng "
          "làm chỉ báo xu hướng chứ không phải phép đếm đầy đủ."],

         "Ở phiên bản hiện tại, cả hai tín hiệu được ĐO và báo cho phụ huynh, "
         "chưa được dùng để tự động rút ngắn buổi học. Đây là một lựa chọn có ý "
         "thức: các ngưỡng nêu trên chưa được hiệu chỉnh trên dữ liệu học thật "
         "đủ lớn, và để một ngưỡng chưa hiệu chỉnh tự động can thiệp vào buổi "
         "học của một đứa trẻ là rủi ro lớn hơn giá trị thu được."])

    # ── B-1 · 2.2.1.d — hai bản của đồ thị ──────────────────────────────────
    c.them("B-1", "- Xây dựng Kiến trúc RAG",
        ["Cần phân biệt hai bản của Đồ thị tri thức, vì chúng phục vụ hai khâu "
         "khác nhau. Bản ĐẦY ĐỦ (3 989 đỉnh · 7 602 cạnh, khoảng 3,4 MB) được "
         "dùng ở khâu dựng học liệu, chạy ngoại tuyến. Bản LÚC CHẠY được cắt ra "
         "và nạp về máy người học: 1 194 đỉnh · 253 cạnh, khoảng 127 KB trên đĩa "
         "và 21 KB khi truyền qua mạng. Bản lúc chạy CHỈ giữ QUAN HỆ — không giữ "
         "nhãn, nghĩa tiếng Việt hay ví dụ — bởi học liệu đã mang sẵn phần chữ "
         "nghĩa; sao chép lại là nhân đôi dữ liệu, và dữ liệu nhân đôi thì sớm "
         "muộn hai bản sẽ lệch nhau mà không có cách nào biết bản nào đúng.",

         "Kích thước nhỏ của bản lúc chạy là điều kiện để phép duyệt chẩn đoán "
         "thực hiện được ngay trên máy người học mà không cần gọi máy chủ — một "
         "yêu cầu thực tế với đối tượng người dùng là học sinh tiểu học, nơi "
         "đường truyền không phải lúc nào cũng sẵn có. Trong 253 cạnh của bản "
         "này, 195 cạnh là ràng buộc tiên quyết của bản đồ gốc, 5 cạnh bắc cầu "
         "giữa hai bài thuộc cùng một thang từ vựng có thứ tự, và 53 cạnh còn "
         "lại chỉ biểu diễn thứ tự đọc trong cùng một bài — nhóm thứ ba bị loại "
         "khỏi mọi phép duyệt chẩn đoán, như đã nêu ở mục 2.2.2."])

    # ── B-3 · 2.3.1.c — H_req ───────────────────────────────────────────────
    c.thay("B-3", "- H_req (Hint Requests)",
        [("- H_req: ", B),
         "Số gợi ý mà người học ĐÃ ĐƯỢC THẤY tại một Nút tri thức. Cần phân biệt "
         "đại lượng này với “số lần chủ động yêu cầu trợ giúp”: trong hệ thống, "
         "gợi ý hiện TỰ ĐỘNG sau một số lần trả lời sai, không có nút xin gợi ý. "
         "Hai đại lượng gần nhau nhưng không đồng nhất — đại lượng ở đây phản "
         "ánh MỨC KHÓ mà người học gặp phải, không phản ánh hành vi tìm kiếm trợ "
         "giúp. Diễn giải nhầm sẽ dẫn tới kết luận sai về chất."])

    # ── A-4 · 2.3.1.c — CEFR là quy ước bắc cầu ─────────────────────────────
    c.thay("A-4", "- Bao gồm các siêu dữ liệu (Metadata) về người học",
        [("- Bao gồm các siêu dữ liệu (Metadata) về người học như: ", B),
         "mức năng lực quy đổi theo thang tham chiếu, sở thích cá nhân (VD: Bóng "
         "đá, Công chúa, Thế giới tự nhiên), và định dạng bài tập mà người học "
         "làm tốt nhất (VD: Trắc nghiệm hình ảnh)."])

    c.them("A-4", "- Bao gồm các siêu dữ liệu (Metadata) về người học",
        ["Riêng mức năng lực cần được phát biểu chính xác, vì đây là chỗ dễ bị "
         "đọc thành một điều mà hệ thống không đo. Mức năng lực được suy ra theo "
         "một QUY ƯỚC BẮC CẦU hai nhịp. Nhịp thứ nhất do hệ thống đo: với mỗi "
         "khối lớp, tính tỷ lệ số Nút tri thức mà người học đã đạt P(L) ≥ θ trên "
         "TỔNG số Nút học được của khối ấy — gọi là mức phủ vốn tri thức. Nhịp "
         "thứ hai lấy nguyên mục tiêu đã ấn định trong Chương trình giáo dục phổ "
         "thông môn Tiếng Anh (Bộ Giáo dục và Đào tạo, 2018): khối Lớp 1–2 là "
         "chương trình làm quen, dưới Bậc 1; khối Lớp 3–5 nhắm Bậc 1, tương "
         "đương A1. Hệ thống công nhận một bậc khi mức phủ của khối đạt 60% và "
         "khối ấy có tối thiểu 30 Nút; chưa đạt thì hệ thống báo đúng tỷ lệ phủ "
         "hiện có chứ không quy ra bậc.",

         "Cần nhấn mạnh: đây KHÔNG phải là phép đo theo chuẩn CEFR. Khung tham "
         "chiếu chung châu Âu định nghĩa bậc năng lực bằng các mô tả làm được "
         "(can-do descriptors) — người học nói được gì, với ai, trong tình huống "
         "nào — chứ không định nghĩa bằng số đơn vị kiến thức đã nắm (Council of "
         "Europe, 2020). Nhịp thứ hai của phép quy đổi là quy ước của chương "
         "trình quốc gia, không phải kết quả đo của phần mềm. Câu phát biểu đúng "
         "là “người học đã vững 34% vốn kiến thức của khối lớp mà chương trình "
         "xếp ở bậc A1”, không phải “người học đạt A1”.",

         "Ba lựa chọn trong phép quy đổi cần được nêu tường minh để có thể tranh "
         "luận: ngưỡng phủ 60%, ngưỡng đáng tin cậy 30 Nút, và việc lấy mẫu số "
         "là TOÀN BỘ vốn của khối chứ không phải số Nút người học đã chạm tới. "
         "Lựa chọn thứ ba là quan trọng nhất: nếu lấy mẫu số là “đã chạm tới” "
         "thì một người học mới học đúng 5 Nút và nắm được cả 5 sẽ đạt 100%, tức "
         "là phép đo thưởng cho việc HỌC ÍT. Hệ quả phải chấp nhận của lựa chọn "
         "này là trong những tuần đầu con số sẽ rất nhỏ; đó là con số đúng, và "
         "giao diện phải trình bày đúng như vậy chứ không làm tròn cho đẹp."])

    # ── A-3 · 2.3.2.c — pha nào được tính vào BKT ───────────────────────────
    c.them("A-3", "Giá trị P(Lₙ) này sẽ được lưu vào Bản sao số",
        ["Cần nói rõ phạm vi áp dụng của phép cập nhật. Mức tinh thông chỉ được "
         "cập nhật từ những lượt mà người học TỰ đưa ra câu trả lời: luyện tập, "
         "sát hạch, câu chốt nhanh sau một đoạn đọc hiểu, và câu xen giữa ví dụ "
         "mẫu. Các bước mà hệ thống đang trình bày lời giải — giới thiệu, làm "
         "mẫu, giảng bài — không được tính, bởi ở đó người học chưa đưa ra câu "
         "trả lời nào của mình; tính vào là ghi công cho người khác. Ranh giới "
         "này cần được khai báo tường minh và kiểm tra tự động: ở một phiên bản "
         "trước, danh sách các pha được tính bị thu hẹp còn hai pha, khiến 31% "
         "số câu người học thực làm bị bỏ trắng khỏi mô hình mà không có dấu "
         "hiệu nào cảnh báo."])

    # ── A-1a · 2.3.2.d — ngưỡng tinh thông θ ────────────────────────────────
    c.thay("A-1a", "Cụ thể, hệ thống thiết lập một Ngưỡng tinh thông",
        "Cụ thể, hệ thống thiết lập một Ngưỡng tinh thông (Mastery Threshold) "
        "θ = 0,85. Giá trị này được hiệu chỉnh bằng thực nghiệm trên chính bộ "
        "tham số của hệ thống — P(L₀) = 0,10 · P(T) = 0,08 · P(S) = 0,10 · "
        "P(G) = 0,30 — sao cho ngưỡng tương ứng với khoảng bốn câu trả lời đúng "
        "liên tiếp mới công nhận là tinh thông, và một câu sai sau đó kéo xác "
        "suất tụt xuống dưới ngưỡng. Bộ tham số mặc định thường gặp trong tài "
        "liệu (P(L₀) = 0,25 · P(G) = 0,20) tuyên bố tinh thông chỉ sau hai câu "
        "đúng, quá dễ dãi với học sinh tiểu học. Khi P(Lₙ) ≥ θ, hệ thống đánh "
        "dấu Nút tri thức là “Mastered” và ngừng sinh thêm bài tập ở Nút này, "
        "giúp giảm tải nhận thức và tránh sự nhàm chán (Sweller, 1988). Ngược "
        "lại, nếu P(Lₙ) sụt giảm, hệ thống kích hoạt cờ để lùi xuống sinh bài "
        "tập phụ đạo ở các Nút tri thức tiên quyết.")

    c.them("A-1a", "Cụ thể, hệ thống thiết lập một Ngưỡng tinh thông",
        ["Không gian trạng thái của một Nút tri thức được chia thành bốn vùng "
         "theo hai ngưỡng, và bốn vùng này là cơ sở cho cả cơ chế sắp xếp bài "
         "tập lẫn Hàm chính sách ở mục 2.5.1:",

         [("- Vùng YẾU — P(L) < 0,30: ", B),
          "luyện thêm cùng một kiểu câu hỏi không gỡ được, cần bài tập phụ đạo ở "
          "Nút tiên quyết."],

         [("- Vùng PHÁT TRIỂN GẦN — 0,30 ≤ P(L) < 0,85: ", B),
          "đây chính là Vùng phát triển gần theo nghĩa của Vygotsky (1978), nơi "
          "việc luyện tập thay đổi trạng thái nhiều nhất."],

         [("- Vùng TINH THÔNG — P(L) ≥ 0,85: ", B),
          "ngừng sinh thêm bài tập thường ở Nút này."],

         [("- Vùng CHƯA CÓ SỐ LIỆU: ", B),
          "Nút mà người học chưa từng chạm tới. Vùng này được tách riêng chứ "
          "không quy về 0, bởi “chưa có thông tin” khác hẳn “đã đo và thấy "
          "hổng”; quy về 0 sẽ xếp nhầm toàn bộ nội dung mới xuống cuối buổi học."],

         "Chuỗi bảy lượt chạy trên chính bộ tham số của hệ thống minh họa nhịp "
         "mà ngưỡng θ = 0,85 tạo ra. Xuất phát từ P(L₀) = 0,10 với chuỗi quan "
         "sát sai · đúng · đúng · đúng · sai · đúng · đúng, xác suất nắm vững "
         "lần lượt là 0,094 → 0,299 → 0,597 → 0,831 → 0,459 → 0,741 → 0,904. Hai "
         "tính chất cần có đều xuất hiện: ba câu đúng liên tiếp từ trạng thái "
         "ban đầu vẫn chưa đủ để công nhận tinh thông (0,831 < 0,85), và một câu "
         "sai đơn lẻ kéo xác suất từ 0,831 xuống 0,459, tức tụt sâu dưới cả "
         "ngưỡng của Vùng phát triển gần, buộc người học phải chứng minh lại."])

    # ── A-1b + C-2a · 2.3.3.c — ngưỡng kích hoạt và hệ số α ─────────────────
    c.thay("A-1b/C-2a", "- Nguyên lý: Nếu xác suất P(L_target)",
        [("- Nguyên lý: ", B),
         "Cơ chế được kích hoạt khi số lần sai liên tiếp S_c tại một Nút đạt từ "
         "3 trở lên, HOẶC khi xác suất P(L_target) tụt xuống dưới ngưỡng của "
         "Vùng yếu (0,30). Khi đó thuật toán duyệt ngược đồ thị theo các cạnh "
         "tiên quyết, với trần độ sâu bốn bước, và xếp hạng các Nút nền tảng "
         "theo Độ ngờ được định nghĩa như sau:"])

    c.them("A-1b/C-2a", "- Nguyên lý: Cơ chế được kích hoạt khi số lần sai liên tiếp",
        [[("doNgo(v) = α^k × [ 1 − P(L_v) ]", B)],

         "trong đó α = 0,6 là Hệ số suy giảm (Decay Penalty Factor) và k là số "
         "bước từ Nút đích tới Nút v. Công thức đòi hỏi CẢ HAI thành phần. Thành "
         "phần α^k phản ánh rằng một nguyên nhân cách chỗ sai quá xa thì không "
         "còn là nguyên nhân theo nghĩa dạy được. Thành phần [1 − P(L_v)] phản "
         "ánh rằng một Nút người học đã vững thì không phải thủ phạm, dù nó là "
         "tiên quyết; các Nút đã đạt ngưỡng tinh thông bị loại hẳn khỏi danh "
         "sách thay vì xếp hạng thấp, bởi để lại chúng thì hệ thống có thể trình "
         "ra một “lỗ hổng gốc rễ” trỏ đúng vào phần mà người học luôn làm đúng, "
         "và niềm tin vào cả bảng chẩn đoán mất theo.",

         "Nút chưa có số liệu được gán P(L) = P(L₀) = 0,10, tức là rất đáng ngờ "
         "— một tiên quyết chưa từng được chạm tới chính là nguyên nhân thường "
         "gặp nhất — nhưng không gán bằng 0, bởi “chưa có thông tin” vẫn khác "
         "“đã đo và thấy hổng”. Trần độ sâu bốn bước vừa mang ý nghĩa sư phạm "
         "vừa bảo đảm phép duyệt luôn dừng kể cả khi đồ thị có chu trình."])

    # ── A-1c + C-2b · 2.3.3.d — hệ số cộng hưởng β ──────────────────────────
    c.thay("A-1c/C-2b", "- Nguyên lý: Nếu một loạt các Nút tiên quyết",
        [("- Nguyên lý: ", B),
         "Nếu một Nút tiên quyết đạt ngưỡng Tinh thông (P(L) ≥ 0,85), thuật toán "
         "áp dụng một Hệ số cộng hưởng (Boost Factor) β = 0,08 để nâng xác suất "
         "ước lượng của các Nút dựng trên nó. Mức nâng cho một Nút cách nguồn k "
         "bước là (β / k) × P(L của Nút nguồn), tức nhỏ dần theo khoảng cách."])

    c.them("A-1c/C-2b", "- Nguyên lý: Nếu một Nút tiên quyết đạt ngưỡng Tinh thông",
        ["Cơ chế này bị chặn bởi ba chốt, và cả ba cùng chống một lỗi duy nhất: "
         "tuyên bố tinh thông khống. Thứ nhất, chỉ lan truyền từ những Nút mà "
         "người học THẬT SỰ đã đạt ngưỡng. Thứ hai, mức cộng nhỏ dần theo số "
         "bước. Thứ ba, kết quả bị kẹp dưới một trần cứng bằng θ − 0,05 = 0,80, "
         "nghĩa là cộng hưởng không bao giờ TỰ NÓ đưa được một Nút tới ngưỡng "
         "tinh thông. Nếu thiếu chốt thứ ba, hệ thống có thể đánh dấu tinh thông "
         "cho một Nút mà người học chưa làm câu nào, rồi bỏ qua bài học tương "
         "ứng — và bỏ qua trong im lặng, vì mọi con số tổng hợp đều đẹp.",

         "Ngoài ra, kết quả cộng hưởng được trả về trong một ánh xạ RIÊNG chứ "
         "không ghi đè vào hồ sơ gốc của người học: trộn lẫn thì xác suất ĐO "
         "ĐƯỢC và xác suất SUY RA không còn phân biệt được, và lần cập nhật kế "
         "tiếp sẽ coi giá trị suy ra như một quan sát thật."])

    # ── A-8 + B-2 · 2.4.3 — bốn bước của RAG ────────────────────────────────
    c.them("B-2", "- Bước 1 - Truy xuất tri thức (Retrieval)",
        ["Bộ truy xuất hợp nhất HAI nguồn trả lời hai câu hỏi khác nhau: một cửa "
         "sổ tuần tự gồm tối đa ba bài liền trước mà người học ĐÃ ĐẠT, trả lời "
         "câu hỏi “người học vừa học gì”; và phép duyệt ngược theo cạnh tiên "
         "quyết trên đồ thị, trả lời câu hỏi “bài này dựng trên gì”. Việc hợp "
         "nhất — thay vì thay thế — là kết quả của một phép đo trên toàn bộ 94 "
         "bài học: cửa sổ tuần tự bỏ sót tiên quyết ở 40 bài, trong đó 2 bài có "
         "tiên quyết nằm ở quyển khác mà cửa sổ không bao giờ với tới được; "
         "nhưng nếu thay hẳn bằng đồ thị thì 87 trên 94 bài có vốn từ HẸP ĐI và "
         "nhiều bài về rỗng, bởi trong 1 194 đỉnh của đồ thị lúc chạy chỉ có 150 "
         "đỉnh mang cạnh tiên quyết đi vào — điều này hợp lý về mặt ngôn ngữ, vì "
         "từ “book” không đòi hỏi phải biết “pen” trước.",

         "Cả hai nguồn đều lọc qua điều kiện người học ĐÃ ĐẠT bài chứa Nút ấy: "
         "bài chưa đạt thì vốn từ của nó không được đưa vào, kể cả khi đồ thị "
         "chỉ ra rằng bài hiện tại cần nó. Bỏ chốt này đi tức là để mô hình nói "
         "bằng những từ người học chưa từng học, tức tự tay chọc thủng chính "
         "tầng chống ảo giác từ vựng."])

    c.thay("A-8", "- Bước 3 - Tạo sinh có kiểm soát",
        [("- Bước 3 - Tạo sinh có kiểm soát (Constrained Generation): ", B),
         "LLM tiếp nhận Prompt và tiến hành sinh ra các câu hỏi, các phương án "
         "nhiễu (distractors) và lời giải thích. Các ràng buộc từ Bước 2 đóng "
         "vai trò ĐỊNH HƯỚNG, làm giảm mạnh khả năng mô hình dùng từ vượt cấp — "
         "nhưng chúng không cấu thành một bảo đảm, bởi lời nhắc là thứ mô hình "
         "CÓ THỂ tuân theo chứ không phải thứ mô hình BUỘC phải tuân theo."])

    c.them("A-8", "- Bước 3 - Tạo sinh có kiểm soát",
        [[("- Bước 4 - Hậu kiểm tất định (Deterministic Post-validation): ", B),
          "Mỗi câu do mô hình sinh ra được đối chiếu lại với vốn từ hợp lệ bằng "
          "một hàm quyết định chạy tại máy người học, không gọi mạng. Câu chỉ "
          "được chấp nhận nếu thuộc một trong năm lớp: một từ nằm trong vốn từ; "
          "một câu nghi thức lớp học thuộc danh sách cố định đã khai báo; một "
          "câu ví dụ của bài; một câu có sẵn trong sách giáo khoa; hoặc một công "
          "thức đã được điền đúng LOẠI ô trống. Câu không qua được sẽ bị thay "
          "bằng một câu do chính máy người học dựng từ dữ liệu bài — luôn hợp "
          "lệ, vì nó ghép từ dữ liệu chứ không sinh mới."]])

    c.thay("A-8", "Nhờ kiến trúc RAG, hệ thống tận dụng được khả năng sáng tạo",
        "Việc tách bạch Bước 3 và Bước 4 là điểm cần nhấn mạnh so với mô tả "
        "thường gặp về kiến trúc RAG. Bảo đảm “nội dung sinh ra không chứa từ "
        "vựng vượt cấp” chỉ là một phát biểu KIỂM CHỨNG ĐƯỢC khi nó được thực "
        "thi bởi một tầng tất định: khi ấy có thể đo tỷ lệ vi phạm ở đầu ra thô "
        "của mô hình, đo lại sau hậu kiểm, và hiệu số giữa hai phép đo chính là "
        "đóng góp của tầng hậu kiểm. Nếu quy công cho lời nhắc, phát biểu ấy "
        "không có cách nào kiểm chứng. Thực tế triển khai đã hai lần cho thấy "
        "giới hạn của lời nhắc: mô hình sinh ra câu “Bye, bike.” sau khi được "
        "chỉ rõ ô trống ấy dành cho TÊN NGƯỜI, và lặp lại y nguyên một câu ngay "
        "sau khi được dặn không được lặp. Nhờ kiến trúc bốn bước, hệ thống tận "
        "dụng được khả năng sáng tạo câu chữ linh hoạt của LLM để cá nhân hóa "
        "ngữ cảnh, nhưng vẫn duy trì được sự kiểm soát sư phạm khắt khe của một "
        "chương trình học chuẩn mực thông qua Đồ thị tri thức.")

    # ── A-1d + B-5 · 2.5.1 — ba nhánh của hàm chính sách ────────────────────
    c.thay("A-1d/B-5", "- Tịnh tiến bình thường (Proceed)",
        [("- Tịnh tiến bình thường (Proceed): ", B),
         "Nếu xác suất nắm vững P(L) của Nút tri thức hiện tại nằm trong Vùng "
         "phát triển gần (0,30 ≤ P(L) < 0,85) và người học không đang trong "
         "chuỗi sai liên tiếp, Hàm chính sách ra lệnh tiếp tục luyện tập ở Nút "
         "này với độ khó tăng dần."])

    c.thay("A-1d/B-5", "- Vượt ải (Mastery Skip)",
        [("- Vượt ải (Mastery Skip): ", B),
         "Nếu P(L) ≥ 0,85, hệ thống đánh dấu Nút là Tinh thông. Cần lưu ý rằng "
         "nhánh này được xét ở cấp BÀI HỌC chứ không ở cấp Nút, và đòi hỏi đủ ba "
         "điều kiện: người học đã đạt bài học ấy, bài có ít nhất ba Nút tri "
         "thức, và MỌI Nút của bài đều đạt ngưỡng. Trong phép gộp ở cấp bài, "
         "nhánh Phụ đạo luôn thắng nhánh Vượt ải: một bài mười Nút với chín Nút "
         "đã vững và một Nút đang mắc thì việc cần làm là gỡ Nút ấy, không phải "
         "cho bỏ qua cả bài — cho vượt ải ở đây chính là bỏ lại đúng chỗ người "
         "học cần giúp nhất, và bỏ lại một cách lặng lẽ."])

    c.thay("A-1d/B-5", "- Can thiệp phụ đạo (Remediation Intervention)",
        [("- Can thiệp phụ đạo (Remediation Intervention): ", B),
         "Đây là cốt lõi của tính “thích ứng”. Điều kiện kích hoạt là số lần sai "
         "liên tiếp S_c tại một Nút đạt từ 3 trở lên, HOẶC P(L) tụt xuống dưới "
         "0,30. Hệ thống tự động truy vết ngược theo các cạnh tiên quyết trên Đồ "
         "thị tri thức để tìm ra Nút gốc rễ bị hổng, sau đó dựng một bài tập "
         "ngắn thuộc Nút gốc rễ này, được lồng trong Ngữ cảnh dựa trên Sở thích "
         "của người học để giảm thiểu rào cản tâm lý."])

    c.them("A-1d/B-5", "- Can thiệp phụ đạo (Remediation Intervention)",
        ["Thứ tự xét giữa ba nhánh là một chi tiết thiết kế có hệ quả: Hàm chính "
         "sách kiểm tra điều kiện ĐANG MẮC TRƯỚC khi kiểm tra mức tinh thông. Lý "
         "do nằm ở bản chất khác nhau của hai đại lượng — P(L) là một trung bình "
         "có quán tính, còn chuỗi sai liên tiếp là tín hiệu tức thời và đáng tin "
         "cậy hơn về trạng thái hiện tại. Một người học có P(L) = 0,96 nhưng vừa "
         "trả lời sai ba câu liền thì con số trung bình không phải là thứ đáng "
         "nghe. Ngưỡng ba (chứ không phải hai) cũng có căn cứ: sai hai lần liên "
         "tiếp là chuyện thường của việc học, cắt ngang ở đó khiến mạch học bị "
         "ngắt liên tục."])

    # ── C-1 · 2.5.2 — nhịp ghi theo lô, mã lũy đẳng ─────────────────────────
    c.them("C-1", "Theo kiến trúc này, quá trình học tập không phải là các bản ghi",
        ["Về nhịp ghi: sự kiện được ghi vào bộ nhớ tại máy người học ngay khi "
         "người học trả lời, nhưng chỉ được đẩy lên máy chủ theo LÔ. Mã định "
         "danh của mỗi bản ghi nhúng đủ năm thành phần — mã người học, mã phiên, "
         "mã bài học, mã câu hỏi và SỐ THỨ TỰ của lượt trả lời trong phiên — nhờ "
         "đó việc dựng lại và gửi lại là thao tác lũy đẳng: một lượt cũ luôn "
         "sinh ra đúng mã cũ, không tạo bản ghi trùng. Số thứ tự là thành phần "
         "không thể bỏ: nếu đẩy từng lượt riêng lẻ thì số thứ tự luôn bằng 0 và "
         "mọi lượt trả lời của cùng một câu sẽ ghi đè lên nhau, làm mất đúng "
         "thông tin mà nhật ký sinh ra để giữ — rằng người học đã sai hai lần "
         "rồi mới trả lời đúng. Thiết kế này đồng thời là điều kiện để hệ thống "
         "hoạt động khi mất kết nối: bản ghi nằm lại hàng đợi tại máy và được "
         "gửi lại ở phiên sau mà không sinh trùng lặp."])

    # ── A-2 · 2.5.2 — chất lượng dữ liệu thu được ───────────────────────────
    c.them("A-2", "Cần nêu kèm giới hạn của bốn phép kiểm này",
        ["Trong quá trình triển khai thử nghiệm, đường ống ghi nhận đã bộc lộ "
         "hai khiếm khuyết rơi đúng vào hai bất biến đầu tiên, và cả hai đã được "
         "khắc phục ngày 23-08-2026. Thứ nhất, do tương tác giữa quy tắc bất "
         "biến của kho sự kiện và cơ chế gửi theo lô — một bản ghi đã tồn tại "
         "làm lệnh ghi cả lô bị từ chối — mỗi phiên học chỉ có bản ghi ĐẦU TIÊN "
         "lên được máy chủ, phần còn lại nằm lại trong bộ nhớ tại máy. Thứ hai, "
         "cơ chế nhận lại dữ liệu học thử khi người dùng đăng nhập đã gán nhầm "
         "130 trên 398 bản ghi sang chủ sở hữu khác.",

         "Toàn bộ dữ liệu đã được rà soát và làm sạch, mô hình người học được "
         "dựng lại từ nhật ký gốc bằng chính hàm cập nhật của hệ thống, và bốn "
         "phép kiểm nêu trên cho kết quả trùng khớp tuyệt đối sau khi làm sạch. "
         "Do đó, số liệu dùng cho phân tích thực nghiệm chỉ được lấy từ sau mốc "
         "thời gian này. Việc công bố công khai giới hạn này là bắt buộc về mặt "
         "liêm chính khoa học; nó cũng cho thấy chính xác vì sao bốn bất biến "
         "phải được kiểm tra tự động thay vì được giả định — cả hai khiếm khuyết "
         "đều không làm chương trình dừng lại và không để lại dấu hiệu nào trên "
         "giao diện."])

    # ── Bloom: sửa cách phát biểu và gắn nguồn (kéo theo mục §6) ────────────
    p = c.tim("Trong giáo dục truyền thống, nhà nghiên cứu tâm lý học giáo dục",
              "Bloom")
    dat_chu(p,
        "Trong giáo dục truyền thống, nhà nghiên cứu tâm lý học giáo dục "
        "Benjamin Bloom đã chỉ ra “Bài toán 2 Sigma” (2 Sigma Problem): học sinh "
        "được kèm riêng theo hình thức 1-kèm-1 đạt kết quả cao hơn khoảng hai độ "
        "lệch chuẩn so với mức trung bình của lớp học truyền thống, tương ứng "
        "với việc vượt khoảng 98% học sinh trong lớp thường (Bloom, 1984). Tuy "
        "nhiên, việc cung cấp gia sư cá nhân cho mọi học sinh là điều không "
        "tưởng về mặt chi phí.")
    c.da_sua.append(("§6", "thay", "2.4.1 — phát biểu Bài toán 2 Sigma + nguồn"))


def _them_tltk(c):
    """
    Bổ sung BẢY tài liệu tham khảo mà phần chữ mới trích tới, rồi đánh số lại
    toàn bộ danh mục. Hai trong số đó — Vygotsky và Bloom — đã được nhắc tới
    trong thân bài bản gốc mà KHÔNG có mục tương ứng; trích dẫn treo là lỗi hình
    thức nặng hơn thiếu nguồn.

    ⚠ Đánh số lại an toàn vì thân bài trích theo kiểu TÁC GIẢ – NĂM chứ không
      theo số. Nếu sau này đổi sang trích theo số thì phải rà lại chỗ này.
    """
    them = [
        # (neo — mục đứng ngay TRƯỚC, nội dung)
        ("Käser",
         "Baker, R. S. J. d., Corbett, A. T., & Aleven, V. (2008). More accurate "
         "student modeling through contextual estimation of slip and guess "
         "probabilities in Bayesian Knowledge Tracing. In Intelligent Tutoring "
         "Systems (pp. 406–415). Springer. — Cơ sở cho việc ước lượng tham số "
         "P(S) và P(G) theo ngữ cảnh của từng câu hỏi thay vì dùng một bộ tham "
         "số chung; căn cứ của bộ tham số riêng dành cho câu Bắt buộc đúng. Được "
         "trích dẫn tại Mục 2.3.2."),

        ("Baker, R. S. J. d.",
         "Vygotsky, L. S. (1978). Mind in Society: The Development of Higher "
         "Psychological Processes. Harvard University Press. — Nguồn gốc khái "
         "niệm Vùng phát triển gần (Zone of Proximal Development), cơ sở của "
         "việc chia không gian trạng thái thành bốn vùng và của cơ chế sắp xếp "
         "bài tập theo mức chông chênh. Được trích dẫn tại Mục 2.1.2, 2.3.2."),

        ("Settles, B.",
         "Leitner, S. (1972). So lernt man lernen. Herder. — Hệ thống hộp lặp "
         "lại ngắt quãng; cơ sở của lịch ôn năm khoảng cách 1 · 3 · 7 · 14 · 30 "
         "ngày và của quy tắc đưa thẻ sai về hộp đầu tiên. Được trích dẫn tại "
         "Mục 2.1.2."),

        ("Leitner, S.",
         "Ebbinghaus, H. (1885/1913). Memory: A Contribution to Experimental "
         "Psychology. Teachers College, Columbia University. — Nguồn gốc đường "
         "cong quên; cơ sở cho dạng hàm phân rã theo thời gian dùng ở Bước 0 của "
         "thuật toán cập nhật. Được trích dẫn tại Mục 2.1.2, 2.3.2."),

        ("Kasneci, E.",
         "Bloom, B. S. (1984). The 2 Sigma Problem: The search for methods of "
         "group instruction as effective as one-to-one tutoring. Educational "
         "Researcher, 13(6), 4–16. — Bằng chứng thực nghiệm về khoảng cách hiệu "
         "quả giữa dạy kèm 1-kèm-1 và lớp học truyền thống; động cơ của việc "
         "dùng tác nhân trí tuệ nhân tạo để giải bài toán quy mô. Được trích dẫn "
         "tại Mục 2.4.1."),
    ]
    for neo, chu in them:
        p = next(x for x in c.d.paragraphs if neo in x.text and x.text.strip().startswith("["))
        chen_sau(p, [[("[0] ", False), chu]])

    # Nhóm V — hai nguồn về khung năng lực, đặt sau mục cuối của nhóm IV.
    p_cuoi = None
    for x in c.d.paragraphs:
        if x.text.strip().startswith("[") and "] " in x.text[:6]:
            p_cuoi = x
    p_nhom4 = next(x for x in c.d.paragraphs
                   if x.text.strip().startswith("IV. Kiến trúc LLM"))
    chen_sau(p_cuoi, ["V. Khung tham chiếu năng lực và Chương trình giáo dục"],
             mau=p_nhom4)
    p_h5 = next(x for x in c.d.paragraphs
                if x.text.strip().startswith("V. Khung tham chiếu"))
    chen_sau(p_h5, [
        [("[0] ", False),
         "Council of Europe (2020). Common European Framework of Reference for "
         "Languages: Learning, teaching, assessment — Companion volume. Council "
         "of Europe Publishing. — Định nghĩa bậc năng lực bằng mô tả làm được "
         "(can-do descriptors); căn cứ để khẳng định phép quy đổi mức phủ vốn "
         "của hệ thống KHÔNG phải phép đo theo chuẩn CEFR. Được trích dẫn tại "
         "Mục 2.3.1."],
        [("[0] ", False),
         "Bộ Giáo dục và Đào tạo (2018). Chương trình giáo dục phổ thông môn "
         "Tiếng Anh (ban hành kèm Thông tư số 32/2018/TT-BGDĐT ngày "
         "26-12-2018). — Mục tiêu bậc năng lực ấn định cho từng khối lớp; nhịp "
         "thứ hai của phép quy đổi bắc cầu. Được trích dẫn tại Mục 2.3.1."],
    ], mau=p_cuoi)

    # A-1 còn một chỗ cuối: ghi chú của Sweller trong danh mục vẫn ghi θ = 0,95.
    p_sw = next(x for x in c.d.paragraphs if "Sweller, J. (1988)" in x.text)
    for r in p_sw.runs:
        if "0,95" in r.text:
            r.text = r.text.replace("θ = 0,95", "θ = 0,85")
    if "0,95" in p_sw.text:
        dat_chu(p_sw, p_sw.text.replace("θ = 0,95", "θ = 0,85"))
    c.da_sua.append(("A-1e", "thay", "TLTK — ghi chú Sweller: θ 0,95 → 0,85"))

    # Đánh số lại toàn bộ danh mục theo thứ tự xuất hiện.
    mau_so = re.compile(r"\[\d+\]")
    stt = 0
    for p in c.d.paragraphs:
        t = p.text.strip()
        if not (t.startswith("[") and "] " in t[:6]):
            continue
        stt += 1
        xong = False
        for r in p.runs:
            if mau_so.search(r.text):
                r.text = mau_so.sub(f"[{stt}]", r.text, count=1)
                xong = True
                break
        if not xong:
            dat_chu(p, mau_so.sub(f"[{stt}]", p.text, count=1))
    c.da_sua.append(("§6", "thêm 7 mục", f"TLTK — đánh số lại [1]–[{stt}]"))


if __name__ == "__main__":
    raise SystemExit(main())
