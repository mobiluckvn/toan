#!/usr/bin/env python3
"""CHƯƠNG 3 — phần 1: mục 3.1 (phát biểu bài toán) và 3.2 (biểu diễn bài toán)."""
from __future__ import annotations

from chuong3_khung import (
    bang, canh_bao, cham, cong_thuc, do, doan, hinh_chu, ma_lenh,
)


def viet(d):
    _m31(d)
    _m32(d)


# ═══════════════════════════════════════════════════════════════════════════
# 3.1 · PHÁT BIỂU BÀI TOÁN VÀ KIẾN TRÚC HỆ THỐNG
# ═══════════════════════════════════════════════════════════════════════════
def _m31(d):
    d.add_heading("3.1. Phát biểu bài toán và kiến trúc hệ thống", level=1)
    doan(d,
        "Chương 2 đã trình bày cơ sở lý thuyết của học tập thích ứng: đồ thị tri "
        "thức làm phương tiện biểu diễn miền học, thuật toán theo dõi tri thức "
        "Bayes làm phương tiện lượng hoá trạng thái nhận thức, kiến trúc tạo "
        "sinh tăng cường truy xuất làm phương tiện kiểm soát nội dung do mô hình "
        "ngôn ngữ lớn sinh ra. Chương này chuyển các cơ sở ấy thành một thiết kế "
        "cụ thể cho một bài toán cụ thể: dạy tiếng Anh cho học sinh tiểu học "
        "Việt Nam, từ lớp 1 đến lớp 5. Mọi thực thể, thuộc tính, thuật toán và "
        "tham số trình bày dưới đây đều đã được hiện thực và đang vận hành; "
        "phần cuối chương đề xuất các kịch bản thực nghiệm để kiểm chứng chúng.")

    # ── 3.1.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.1.1. Phát biểu bài toán", level=2)
    doan(d,
        "Bài toán được phát biểu như sau. Cho một miền tri thức môn Tiếng Anh "
        "được biểu diễn dưới dạng đồ thị có hướng, có nhãn; cho một kho học "
        "liệu gồm các bài học và câu hỏi đã được gắn với các nút của đồ thị; và "
        "cho một chuỗi tương tác quan sát được của một người học cụ thể. Hãy xác "
        "định, tại mỗi thời điểm, ba đại lượng:")
    cham(d, [
        ("Trạng thái tri thức — ", "ước lượng xác suất người học đã nắm vững "
         "từng nút tri thức, có tính tới sự suy giảm theo thời gian và tính tới "
         "quan hệ tiên quyết giữa các nút."),
        ("Vị trí lỗ hổng — ", "khi người học thất bại lặp lại, xác định nút tri "
         "thức nào là NGUYÊN NHÂN, phân biệt với nút nơi lỗi LỘ RA. Hai nút này "
         "thường không trùng nhau, và đây là chỗ một hệ thống thích ứng khác một "
         "hệ thống chỉ đếm đúng–sai."),
        ("Can thiệp sư phạm tiếp theo — ", "chọn nội dung, độ khó, định dạng và "
         "ngữ cảnh cho bước học kế tiếp, sao cho vừa nằm trong vùng phát triển "
         "gần của người học vừa không vi phạm ràng buộc vốn từ của khối lớp."),
    ])

    doan(d,
        "Ba đại lượng trên tương ứng với ba phương pháp mà chương này trình bày: "
        "nhận biết hành vi (mục 3.3) cung cấp tín hiệu đầu vào; chẩn đoán lỗ "
        "hổng (mục 3.4) biến tín hiệu thành trạng thái và định vị nguyên nhân; "
        "sinh bài tập và kiểm tra (mục 3.5) biến trạng thái thành hành động.")

    doan(d,
        "Điều làm bài toán này khác với bài toán học thích ứng tổng quát nằm ở "
        "đối tượng người dùng. Người học ở đây từ sáu đến mười một tuổi; nhiều "
        "em chưa đọc thông tiếng Việt, và gần như không em nào đọc được một câu "
        "hướng dẫn bằng tiếng Anh. Điều đó loại bỏ nhiều giải pháp vốn hiển "
        "nhiên với người học trưởng thành: không thể hỏi người học tự đánh giá, "
        "không thể giải thích bằng một đoạn văn, không thể để người học tự chọn "
        "lộ trình. Nó cũng nâng cái giá của một nội dung sai: với người lớn, một "
        "câu tiếng Anh sai ngữ pháp là một phiền toái; với trẻ đang tập nhại, đó "
        "là dạy sai, và trẻ sẽ nhớ.")

    # ── 3.1.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.1.2. Sáu ràng buộc thiết kế", level=2)
    doan(d,
        "Từ đặc thù người dùng, sáu ràng buộc dưới đây được đặt ra trước khi "
        "thiết kế. Chúng chi phối hầu hết các quyết định trình bày ở phần sau, "
        "nên được nêu tập trung ở đây thay vì nhắc lại rải rác.")

    bang(d,
        ["Ràng buộc", "Phát biểu", "Hệ quả thiết kế"],
        [
            ["R1 — Không bắt trẻ đọc chữ để biết phải làm gì",
             "Mọi điều kiện đi tiếp phải hiện được bằng hình, không bằng một câu "
             "hướng dẫn.",
             "Thanh “việc của con” gồm các ô có biểu tượng, ba trạng thái nhìn "
             "thấy được. Bỏ hẳn lối báo điều kiện bằng một dòng chữ."],

            ["R2 — Không người học nào được kẹt vĩnh viễn",
             "Mô hình đánh giá có thể sai; nếu quyền mở đường nằm trong tay mô "
             "hình thì một người học bị chấm nhầm không có cách nào tự thoát.",
             "Luật đi tiếp tách khỏi hàm chính sách: “đã ĐẠT, HOẶC đã thử thật "
             "ít nhất hai lần”. Dùng lại nguyên vẹn ở ba tầng (mở bài · mở chặng "
             "· để lại một câu). Xem mục 3.4.7."],

            ["R3 — Nội dung phải kiểm được TRƯỚC khi tới tay trẻ",
             "Nội dung sinh lúc chạy chỉ kiểm được SAU. Chỗ nào kiểm trước được "
             "thì phải kiểm trước.",
             "4 226 câu của phần học chính sinh sẵn và đi qua 92 phép kiểm tự "
             "động. Mô hình ngôn ngữ chỉ được gọi ở ba chỗ nội dung tĩnh không "
             "phục vụ được, và ở đó vẫn buộc qua hậu kiểm. Xem mục 3.5.1."],

            ["R4 — Chạy được khi mất mạng",
             "Đường truyền ở gia đình học sinh không phải lúc nào cũng có; mất "
             "mạng không được làm mất công học.",
             "Đồ thị chẩn đoán rút gọn còn 127 KB (≈ 21 KB khi truyền) nạp về máy con; nhật ký ghi vào "
             "bộ nhớ tại máy rồi đẩy theo lô, mã bản ghi lũy đẳng nên gửi lại "
             "bao nhiêu lần cũng không sinh dòng trùng. Xem mục 3.3.2."],

            ["R5 — Máy chủ không lưu nội dung riêng tư của trẻ",
             "Bài viết, câu nói và lịch sử hội thoại của trẻ không được lưu ở "
             "tầng dịch vụ dùng chung.",
             "Lời nhắc gửi đi rồi bỏ; muốn so hiệu quả giữa các mẫu lời nhắc thì "
             "chỉ lưu VÂN TAY của phần khung. Xem mục 3.5.7."],

            ["R6 — Mọi con số hiện cho người lớn phải mang nhãn nguồn",
             "Điểm do máy chấm, số phút suy ra và số phút đo thật là ba đại "
             "lượng khác nhau về bản chất.",
             "Trường `nguon` đi kèm mọi con số; màn hình nói rõ “máy chấm”, và "
             "phân biệt số phút ĐO ĐƯỢC với số phút SUY RA. Xem mục 3.6.5."],
        ],
        ten="Bảng 3.1: Sáu ràng buộc thiết kế và hệ quả",
    )

    canh_bao(d,
        "Ràng buộc R2 và R3 kéo ngược chiều nhau với ràng buộc “cá nhân hoá tối "
        "đa” thường thấy trong tài liệu. Chương này không coi đó là nhược điểm "
        "của thiết kế mà là một sự đánh đổi có ý thức, và mục 3.5.1 trình bày "
        "tiêu chí phân định cụ thể.")

    # ── 3.1.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.1.3. Kiến trúc bốn tầng và vòng lặp thích ứng", level=2)
    doan(d,
        "Hệ thống được tổ chức thành bốn tầng. Ranh giới giữa các tầng đặt theo "
        "nguyên tắc: tầng nào có thể chạy mà không cần mạng thì đặt ở máy người "
        "học, tầng nào cần dữ liệu của nhiều phiên hoặc nhiều người học thì đặt "
        "ở máy chủ.")

    hinh_chu(d, [
        "┌───────────────────────────────────────────────────────────────────┐",
        "│  TẦNG 4 · TRÌNH DIỄN            (máy người học — React 18/Vite)    │",
        "│  màn bài học · phòng luyện nói · màn ôn lại · góc bố mẹ           │",
        "└───────────────┬───────────────────────────────────┬───────────────┘",
        "                │ tín hiệu hành vi                  │ nội dung",
        "┌───────────────▼───────────────┐   ┌───────────────▼───────────────┐",
        "│  TẦNG 3 · THÍCH ỨNG           │   │  TẦNG 2 · TRI THỨC & HỌC LIỆU │",
        "│  (máy người học, chạy offline)│◄──┤  (tệp tĩnh, tải một lần)      │",
        "│  · xếp câu theo ZPD           │   │  · đồ thị rút gọn 127 KB      │",
        "│  · lan truyền chẩn đoán       │   │    1 194 nút · 253 cạnh       │",
        "│  · hàm chính sách π           │   │  · 94 bài · 4 226 câu         │",
        "│  · hồ sơ định dạng · vector S │   │  · âm · video · hình · kịch bản│",
        "└───────────────┬───────────────┘   └───────────────────────────────┘",
        "                │ nhật ký sự kiện (theo lô, lũy đẳng)",
        "┌───────────────▼───────────────────────────────────────────────────┐",
        "│  TẦNG 1 · DỮ LIỆU & TÍNH TOÁN NỀN      (Firestore + Cloud Funcs)  │",
        "│  · attempts/  nhật ký bất biến   · mastery/  mô hình người học    │",
        "│  · reviewQueue/  thẻ ôn Leitner  · report/ · teacherBoard/        │",
        "│  · onAttempt (BKT) · nightlyReport · chamViet · luyenNoi          │",
        "└───────────────────────────────────────────────────────────────────┘",
    ], ten="Hình 3.1: Kiến trúc bốn tầng")

    doan(d,
        "Vòng lặp thích ứng khép kín qua bảy bước, lặp lại ở mỗi lượt trả lời "
        "của người học:")
    cham(d, [
        "Người học trả lời một câu hỏi. Tầng trình diễn đo thời gian phản hồi "
        "riêng cho lượt ấy và đếm số gợi ý đã hiện.",
        "Tầng trình diễn dựng một bản ghi sự kiện bất biến, xếp vào hàng đợi tại "
        "máy và đẩy lên máy chủ không chờ kết quả.",
        "Hàm nền `onAttempt` kích hoạt theo tài liệu mới, chạy cập nhật Bayes có "
        "tính suy giảm theo thời gian, ghi lại hồ sơ nút trong một giao dịch.",
        "Máy người học nạp lại hồ sơ nút; tầng thích ứng tính vector trạng thái "
        "bốn chiều và chạy hàm chính sách.",
        "Nếu chính sách trả về “tịnh tiến”, tầng thích ứng xếp lại thứ tự câu "
        "theo vùng phát triển gần và theo hồ sơ định dạng.",
        "Nếu chính sách trả về “phụ đạo”, tầng thích ứng duyệt ngược đồ thị tìm "
        "nút gốc rễ, gom câu tĩnh quanh nút ấy, và chỉ gọi mô hình ngôn ngữ khi "
        "kho tĩnh không đủ — mọi câu đều qua hậu kiểm.",
        "Khi người học đạt một bài, hàm nền sinh thẻ ôn theo lịch ngắt quãng; "
        "thẻ đến hạn được màn ôn lại đọc ra ở buổi học sau.",
    ], danh_so=True)

    canh_bao(d,
        "Bước 3 và bước 4 nối với nhau qua máy chủ chứ không qua bộ nhớ, nên "
        "giữa hai bước có một độ trễ. Thiết kế chấp nhận độ trễ này: hàm chính "
        "sách đọc hồ sơ nút của lần nạp gần nhất, còn tín hiệu tức thời trong "
        "phiên — chuỗi sai liên tiếp — được giữ ở máy con và xét TRƯỚC mức thạo. "
        "Xem mục 3.4.7.")


# ═══════════════════════════════════════════════════════════════════════════
# 3.2 · BIỂU DIỄN BÀI TOÁN
# ═══════════════════════════════════════════════════════════════════════════
def _m32(d):
    d.add_heading("3.2. Biểu diễn bài toán: thực thể, thuộc tính và quan hệ", level=1)

    # ── 3.2.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.2.1. Ba miền thực thể", level=2)
    doan(d,
        "Toàn bộ dữ liệu của hệ thống được tổ chức thành ba miền tách bạch. Việc "
        "tách bạch không chỉ để trình bày cho gọn: mỗi miền có một chủ sở hữu "
        "khác nhau, một nhịp thay đổi khác nhau và một chế độ ghi khác nhau.")

    bang(d,
        ["Miền", "Nội dung", "Ai sinh ra", "Nhịp đổi", "Chế độ ghi"],
        [
            ["MIỀN TRI THỨC", "Đồ thị các đơn vị kiến thức và quan hệ giữa chúng",
             "Số hoá từ chương trình và sách giáo khoa", "Rất chậm — theo năm học",
             "Chỉ đọc lúc chạy"],
            ["MIỀN HỌC LIỆU", "Bài học, câu hỏi, âm, video, hình, kịch bản nói",
             "Bộ sinh tất định, chạy ngoại tuyến", "Chậm — theo đợt dựng",
             "Chỉ đọc lúc chạy"],
            ["MIỀN NGƯỜI HỌC", "Nhật ký sự kiện, mô hình tri thức, hồ sơ, thẻ ôn",
             "Sinh ra từ chính tương tác của người học", "Từng lượt trả lời",
             "Ghi liên tục; nhật ký BẤT BIẾN"],
        ],
        ten="Bảng 3.2: Ba miền thực thể",
    )

    doan(d,
        "Quan hệ giữa ba miền là quan hệ CHE PHỦ theo nghĩa của mô hình overlay "
        "đã trình bày ở mục 2.3.1: miền học liệu ánh xạ vào miền tri thức qua "
        "trường mã nút trên từng câu hỏi; miền người học phủ một lớp trạng thái "
        "lên chính các nút ấy. Không miền nào sao chép dữ liệu của miền kia — "
        "chúng chỉ tham chiếu qua mã nút.")

    canh_bao(d,
        "Nguyên tắc không sao chép có một hệ quả cụ thể đáng nêu: đồ thị rút gọn "
        "nạp về máy người học CHỈ giữ quan hệ, không giữ nhãn tiếng Anh, nghĩa "
        "tiếng Việt hay ví dụ, vì học liệu đã mang đủ phần chữ nghĩa. Chép lại "
        "là nhân đôi dữ liệu, mà nhân đôi thì sớm muộn hai bản lệch nhau và "
        "không ai biết bản nào đúng.")

    # ── 3.2.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.2.2. Miền tri thức: đồ thị tri thức có nhãn", level=2)
    doan(d,
        "Miền tri thức được biểu diễn bằng một đồ thị có hướng, có nhãn trên cả "
        "đỉnh lẫn cạnh:")
    cong_thuc(d, "G = (V, E, τ, λ)",
              "V — tập đỉnh · E ⊆ V × V — tập cạnh có hướng · "
              "τ : V → T — hàm gán loại đỉnh · λ : E → R — hàm gán loại quan hệ")

    doan(d,
        "Việc đưa hai hàm nhãn vào định nghĩa không phải chi tiết hình thức mà "
        "là điều kiện đúng đắn của phép chẩn đoán. Tập cạnh E chứa 29 loại quan "
        "hệ khác nhau, trong đó quan hệ tiên quyết chỉ là một tập con. Nếu duyệt "
        "ngược trên toàn bộ E để tìm nguyên nhân, phép duyệt sẽ đi qua cả quan "
        "hệ cấu thành và cho ra kết luận vô nghĩa kiểu “nguyên nhân em sai là vì "
        "em chưa nắm cả Unit 3”. Do đó mọi phép duyệt chẩn đoán đều ràng buộc "
        "trên tập cạnh đã lọc theo nhãn:")
    cong_thuc(d, "E_prereq = { e ∈ E : λ(e) ∈ {REQUIRES, NOI_BAI} }")

    doan(d,
        "Đồ thị tồn tại ở hai bản phục vụ hai khâu khác nhau. Bảng 3.3 nêu quy "
        "mô và vai trò của từng bản.")

    bang(d,
        ["", "Bản ĐẦY ĐỦ", "Bản LÚC CHẠY"],
        [
            ["Dùng ở khâu", "Dựng học liệu (ngoại tuyến)",
             "Chẩn đoán tại máy người học"],
            ["Số đỉnh", "3 989", "1 194"],
            ["Số cạnh", "7 602", "253"],
            ["Phạm vi lớp", "Lớp 1 – lớp 12", "Lớp 1 – lớp 6"],
            ["Nội dung đỉnh", "Đủ nhãn, nghĩa, ví dụ, siêu dữ liệu",
             "Chỉ mã loại, khối lớp, nhãn ngắn, bài dạy nút ấy"],
            ["Kích thước", "3,4 MB", "127 KB trên đĩa · ≈ 21 KB khi truyền (nén gzip)"],
            ["Vì sao cần bản này", "Cạnh tiên quyết xuyên cấp tồn tại thật thay "
             "vì bị cắt cụt ở ranh giới lớp 5",
             "Đủ nhỏ để chẩn đoán chạy được ngoại tuyến (ràng buộc R4)"],
        ],
        ten="Bảng 3.3: Hai bản của đồ thị tri thức",
    )

    doan(d, "Phân bố loại đỉnh và loại cạnh của bản lúc chạy như sau.")
    bang(d,
        ["Loại đỉnh", "Số lượng", "Vai trò"],
        [
            ["vocabulary_item", "420", "Mục từ vựng cụ thể (đơn vị đánh giá nhỏ nhất)"],
            ["vocabulary", "260", "Nhóm từ vựng theo chủ đề"],
            ["grammar", "152", "Mẫu câu / cấu trúc ngữ pháp"],
            ["pronunciation", "116", "Trọng âm, âm cần luyện"],
            ["unit", "98", "Đơn vị bài học (đỉnh chứa)"],
            ["(không khai loại)", "79", "Mẫu câu lớp 1 — vẫn là kiến thức thật"],
            ["prior_knowledge", "19", "Kiến thức giả định đã có"],
            ["letter_sound", "16", "Chữ cái và âm tương ứng"],
            ["review · fun_time · theme · course", "34", "Đỉnh tổ chức, không đánh giá"],
        ],
        ten="Bảng 3.4: Phân bố loại đỉnh — đồ thị lúc chạy (1 194 đỉnh)",
    )

    canh_bao(d,
        "79 đỉnh mẫu câu lớp 1 bị bỏ trống trường loại trong dữ liệu gốc. Chúng "
        "được TÍNH vào tập đỉnh học được, không loại ra: chúng là kiến thức thật "
        "(ví dụ “That's a + [Noun].”), và loại ra thì mẫu số của khối lớp 1 hụt "
        "gần một nửa, làm tỉ lệ phủ vốn vọt lên giả tạo. Xem mục 3.4.8.")

    bang(d,
        ["Loại cạnh", "Số lượng", "Có dùng để chẩn đoán không?"],
        [
            ["ban_do — quan hệ tiên quyết của bản đồ gốc", "195", "CÓ"],
            ["noi_bai — bắc cầu giữa hai bài của một nhóm từ có thứ tự", "5", "CÓ"],
            ["trong_bai — thứ tự ĐỌC của hai từ liền nhau trong cùng một bài",
             "53", "KHÔNG — xem cảnh báo dưới"],
        ],
        ten="Bảng 3.5: Phân bố loại cạnh — đồ thị lúc chạy (253 cạnh)",
    )

    canh_bao(d,
        "Loại cạnh `trong_bai` KHÔNG phải ràng buộc tiên quyết. Sách dạy cả khối "
        "từ trong một buổi, nên lấy loại cạnh này đi khoá đường học là chặn "
        "người học ngay giữa chính bài đang mở. Đây cũng là chỗ một ví dụ minh "
        "hoạ ở Chương 2 cần sửa: cặp “eleven → nineteen” nối bằng cạnh "
        "`trong_bai`, không phải cạnh tiên quyết.")

    doan(d,
        "Một tính chất của đồ thị có ảnh hưởng lớn tới thiết kế bộ truy xuất: "
        "trong 1 194 đỉnh của bản lúc chạy, chỉ 150 đỉnh có ít nhất một cạnh "
        "tiên quyết đi vào. Điều này hợp lý về mặt ngôn ngữ — từ “book” không "
        "đòi phải biết “pen” trước — nhưng nó có nghĩa là đồ thị MỘT MÌNH không "
        "đủ làm bộ truy xuất vốn từ. Mục 3.5.4 trình bày cách hợp nhất hai nguồn.")

    doan(d,
        "Số cạnh tiên quyết xuyên lớp trong bản lúc chạy là 38. Đây là loại cạnh "
        "quan trọng nhất với cơ chế chẩn đoán, vì nó cho phép hệ thống đưa ra "
        "giả thuyết “lỗ hổng nằm ở lớp dưới”. Hai chuỗi dưới đây lấy trực tiếp "
        "từ đồ thị đang chạy bằng chính phép duyệt của hệ thống:")
    ma_lenh(d, [
        "(a) Ràng buộc xuyên lớp trực tiếp",
        "    sp_g1_u11_1   ──REQUIRES──►  sp_g2_u5_1",
        "    (lớp 1: thể khẳng định           (lớp 2: mẫu hỏi–đáp về",
        "     thì hiện tại tiếp diễn)          hoạt động đang diễn ra)",
        "",
        "(b) Chuỗi chẩn đoán ngược vượt lớp — điểm xuất phát là nút người học sai",
        "    sp_g3_u11_2  →  sp_g3_u2_2  →  sp_g3_u1_1  →  sp_g2_greeting",
        "    (lớp 3, bước 0)   (bước 1)      (bước 2)       (lớp 2, bước 3)",
        "",
        "(c) Chuỗi chạm trần độ sâu — dừng ở bước 4 theo thiết kế",
        "    sp_g3_u18_2 → sp_g3_u18_1 → sp_g3_u5_1 → sp_g3_u4_1 → sp_g3_u3_2",
    ])

    doan(d,
        "Siêu dữ liệu trên đỉnh khác nhau theo loại đỉnh. Bảng 3.6 nêu các "
        "trường của hai loại đỉnh được dùng nhiều nhất.")
    bang(d,
        ["Loại đỉnh", "Trường", "Ý nghĩa", "Dùng vào việc gì"],
        [
            ["Từ vựng", "ma", "Mã định danh duy nhất, ví dụ `v_g3_u1_hello`",
             "Khoá liên kết với câu hỏi và với hồ sơ người học"],
            ["", "tu · ipa · nghia", "Mặt chữ, phiên âm, nghĩa tiếng Việt",
             "Hiển thị; ràng buộc vốn từ cho tầng sinh"],
            ["", "so_nhieu · so_it · dang_ing · dang_qk", "Các dạng biến đổi",
             "Hậu kiểm câu sinh: cho phép dạng biến đổi của từ ĐÃ HỌC"],
            ["", "lexical_type", "Từ đơn hay cụm từ",
             "Chọn định dạng câu hỏi phù hợp"],
            ["", "am · amO", "Mã clip tiếng và vị trí trọng âm",
             "Phát âm mẫu; chấm phát âm"],
            ["Mẫu câu", "cau", "Câu đầy đủ, ví dụ “What's your name?”",
             "Câu mẫu để nhại"],
            ["", "congThuc", "Khuôn có ô trống, ví dụ “Hi, I'm + [Name].”",
             "Hậu kiểm: dựng mọi cách điền hợp lệ rồi đối chiếu"],
            ["", "thi · kieu_cau", "Thì ngữ pháp và loại câu",
             "Ràng buộc cho tầng sinh; phân loại chẩn đoán"],
            ["", "dungDe", "Chức năng giao tiếp của mẫu",
             "Chọn việc cho từng lượt ở phòng luyện nói"],
        ],
        ten="Bảng 3.6: Siêu dữ liệu trên đỉnh từ vựng và đỉnh mẫu câu",
    )

    # ── 3.2.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.2.3. Miền học liệu: quyển, bài, chặng, câu", level=2)
    doan(d,
        "Học liệu được tổ chức theo bốn cấp lồng nhau. Cấp thấp nhất — CÂU — là "
        "nơi miền học liệu chạm vào miền tri thức, qua hai trường mã nút.")

    hinh_chu(d, [
        "QUYỂN (5)  ─ ma · ten · lop · cefr · danh sách bài · cờ khoá bài",
        "   └─ BÀI (94)  ─ id · tenBai · chuong · knowledgeCore · practice ·",
        "        │              assessment · video · hinhTu · parentNote",
        "        ├─ CHẶNG (5–6)  ─ tu · cau · luyen · [noi] · sat · phong",
        "        └─ CÂU (4 226)  ─ id · maNut · maNutDs · bac · format ·",
        "                          text · answerKey · hints · solutionNarrative",
    ], ten="Hình 3.2: Bốn cấp của miền học liệu")

    bang(d,
        ["Quyển", "Tên", "Khối lớp", "Bậc CEFR (nhãn học liệu)", "Số bài"],
        [
            ["ta1", "Tiếng Anh lớp 1", "1", "Pre-A1", "16"],
            ["ta2", "Tiếng Anh lớp 2", "2", "Pre-A1", "16"],
            ["ta3", "Tiếng Anh lớp 3", "3", "Pre-A1", "21"],
            ["ta4", "Tiếng Anh lớp 4", "4", "A1", "21"],
            ["ta5", "Tiếng Anh lớp 5", "5", "A1", "20"],
            ["", "Tổng", "", "", "94"],
        ],
        ten="Bảng 3.7: Năm quyển học liệu",
    )

    canh_bao(d,
        "Bậc CEFR ở bảng trên là NHÃN CỦA HỌC LIỆU — mức mà quyển ấy nhắm tới — "
        "chứ không phải mức năng lực của người học. Hai đại lượng này khác nhau "
        "và từng bị nhầm trong một phiên bản trước. Cách hệ thống ước lượng bậc "
        "của người học trình bày ở mục 3.4.8.")

    doan(d,
        "Câu hỏi được phân thành bốn bậc độ khó và sáu định dạng. Bậc do người "
        "soạn đặt và phản ánh thang sư phạm; định dạng phản ánh cách hỏi. Hai "
        "chiều này độc lập với nhau, và điều đó quan trọng: mục 3.3.4 dùng chiều "
        "định dạng để nhận biết cách hỏi nào người học hợp hơn, mà không được "
        "phép làm xáo trộn thang độ khó.")

    bang(d,
        ["Bậc", "Tên", "Số câu", "Vai trò"],
        [
            ["1", "Khởi động (warmup)", "2 220",
             "Nhận mặt từ, nghe rồi chọn — đo mức nhận biết"],
            ["2", "Ráp câu (standard)", "626",
             "Dùng từ trong một cấu trúc — đo mức vận dụng"],
            ["3", "Thử thách (challenge)", "910",
             "Ghép nhiều đơn vị kiến thức — đo mức tổng hợp"],
            ["4", "Sát hạch (assessment)", "470",
             "Kiểm tra cuối bài, có luật đạt riêng"],
            ["", "Tổng", "4 226", ""],
        ],
        ten="Bảng 3.8: Bốn bậc câu hỏi",
    )

    bang(d,
        ["Mã định dạng", "Tên hiển thị", "Cách trả lời", "Đo được gì"],
        [
            ["chon", "Chọn đáp án", "Bấm một trong bốn lựa chọn",
             "Nhận biết; có xác suất đoán trúng cao"],
            ["the", "Xếp thẻ thành câu", "Kéo các thẻ chữ vào đúng thứ tự",
             "Trật tự từ; không đoán được"],
            ["go", "Gõ lại chữ", "Gõ từ đã nghe",
             "Chính tả và mặt chữ"],
            ["tf", "Đúng / sai", "Bấm một trong hai",
             "Phân biệt nghĩa; xác suất đoán trúng rất cao"],
            ["nghenhin", "Nghe rồi nhìn hình", "Bấm hình đúng với tiếng đọc",
             "Nghe hiểu, không cần đọc chữ (ràng buộc R1)"],
            ["noi", "Nói theo", "Nói vào micro",
             "Phát âm — xem giới hạn ở mục 3.6.5"],
        ],
        ten="Bảng 3.9: Sáu định dạng câu hỏi",
    )

    doan(d,
        "Mỗi câu hỏi mang hai trường liên kết với đồ thị, và sự phân biệt giữa "
        "chúng là một quyết định thiết kế có hệ quả:")
    cham(d, [
        ("maNut — ", "MỘT nút duy nhất, là nút mà câu này ĐÁNH GIÁ. Đây là nút "
         "được ghi vào bản ghi sự kiện và là nút duy nhất được cập nhật mức "
         "thạo."),
        ("maNutDs — ", "danh sách mọi nút mà câu này CHẠM TỚI. Trường này được "
         "ghi kèm để phép lan truyền chẩn đoán sau này dùng, nhưng KHÔNG chỗ nào "
         "được lấy nó ra cộng điểm."),
    ])
    canh_bao(d,
        "Nếu một lượt trả lời đúng được tính công cho cả danh sách nút, mức thạo "
        "sẽ phồng lên và hệ thống trở nên LẠC QUAN về người học — tức là cho đi "
        "tiếp khi người học chưa vững. Ràng buộc “một lượt, một nút” vì thế "
        "không phải quy ước tuỳ tiện mà là điều kiện để mô hình không tự lừa "
        "mình.")

    # ── 3.2.4 ──────────────────────────────────────────────────────────────
    d.add_heading("3.2.4. Miền người học: sáu thực thể", level=2)
    doan(d,
        "Miền người học gồm sáu thực thể. Thực thể thứ nhất là nhật ký bất biến; "
        "năm thực thể còn lại đều SUY RA được từ nó, và tính chất suy ra được ấy "
        "chính là điều kiện kiểm tra tính toàn vẹn trình bày ở mục 3.2.6.")

    bang(d,
        ["Thực thể", "Đường dẫn lưu trữ", "Khoá", "Chế độ ghi", "Suy ra từ đâu"],
        [
            ["Lượt trả lời", "attempts/{id}",
             "mã ghép năm thành phần", "CHỈ THÊM — cấm sửa, cấm xoá", "gốc"],
            ["Hồ sơ nút tri thức", "mastery/{uid}/units/{maNut}",
             "mã nút", "Ghi đè trong giao dịch", "attempts"],
            ["Tiến độ bài", "progressTA/{uid}/micros/{maBai}",
             "mã bài", "Gộp", "kết quả cuối bài"],
            ["Thẻ ôn", "reviewQueue/{uid}/cards/{id}",
             "mã bài + số mốc", "Gộp", "sự kiện đạt bài"],
            ["Mục học bạ", "hocBaTA/{uid}/muc/{khoa}",
             "loại + khoá", "Gộp", "sự kiện màn hình"],
            ["Sổ tổng hợp", "report/{uid} · teacherBoard · bangXepHang",
             "mã người học", "Dựng lại theo lịch", "attempts + mastery + progress"],
        ],
        ten="Bảng 3.10: Sáu thực thể của miền người học",
    )

    doan(d,
        "Thực thể LƯỢT TRẢ LỜI là đơn vị dữ liệu quan trọng nhất của cả hệ "
        "thống. Bảng 3.11 nêu đầy đủ các trường, nhóm theo bốn nhóm dữ liệu đã "
        "định nghĩa ở mục 2.5.2.")

    bang(d,
        ["Nhóm", "Trường", "Kiểu", "Ý nghĩa"],
        [
            ["Định danh & thời gian", "id", "chuỗi",
             "Mã ghép: người học · phiên · bài · câu · SỐ THỨ TỰ lượt trong phiên"],
            ["", "learnerId", "chuỗi", "Mã người học"],
            ["", "sessionId", "chuỗi", "Mã phiên — một lần mở bài là một phiên"],
            ["", "ts", "số", "Mốc mili-giây theo đồng hồ máy người học"],
            ["", "serverTs", "dấu thời gian", "Mốc do máy chủ đóng lúc nhận"],
            ["", "v", "số", "Phiên bản luật ghi (hiện là 2)"],
            ["Nhận thức", "bktUnit", "chuỗi", "MỘT nút được đánh giá — vào BKT"],
            ["", "maNutDs", "mảng", "Mọi nút câu này chạm — KHÔNG cộng điểm"],
            ["", "microId · quyen · mon", "chuỗi", "Bài, quyển, môn"],
            ["", "itemId", "chuỗi", "Mã câu hỏi"],
            ["", "phase", "chuỗi",
             "practice · assess · check · worked (được tính); intro · sample · "
             "teach (không tính)"],
            ["", "correct", "luận lý", "Đúng hay sai"],
            ["", "answer · expected", "chuỗi", "Câu trả lời thô và đáp án, cắt 120 ký tự"],
            ["Hành vi", "ms", "số", "Thời gian phản hồi RIÊNG lượt ấy"],
            ["", "tries", "số", "Lượt thứ mấy của cùng một câu"],
            ["", "hintsUsed", "số", "Số gợi ý ĐÃ HIỆN — xem cảnh báo dưới"],
            ["", "mode", "chuỗi", "Định dạng câu hỏi"],
            ["Bối cảnh hệ thống", "mauPrompt", "chuỗi",
             "Tên mẫu lời nhắc, chỉ có ở lượt do mô hình tham gia"],
            ["", "phienBanMau", "số", "Số phiên bản mẫu, do người sửa khai tay"],
            ["", "vanTayPrompt", "chuỗi", "Băm 12 ký tự của phần KHUNG lời nhắc"],
        ],
        ten="Bảng 3.11: Lược đồ bản ghi lượt trả lời (attempts)",
    )

    canh_bao(d,
        "Trường `hintsUsed` là số gợi ý người học ĐÃ ĐƯỢC THẤY, không phải số "
        "lần chủ động yêu cầu: trong hệ thống này gợi ý hiện tự động sau hai lần "
        "trả lời sai, không có nút xin gợi ý. Hai đại lượng gần nhau nhưng không "
        "đồng nhất — đại lượng ở đây phản ánh MỨC KHÓ người học gặp phải, không "
        "phản ánh hành vi tìm kiếm trợ giúp. Diễn giải nhầm thì kết luận rút ra "
        "sẽ sai về chất.")

    doan(d,
        "Thực thể HỒ SƠ NÚT TRI THỨC là hiện thực cụ thể của mô hình che phủ. "
        "Bảng 3.12 nêu đầy đủ các trường, kèm ánh xạ sang ký hiệu toán học đã "
        "dùng ở Chương 2.")

    bang(d,
        ["Trường", "Ký hiệu (Chương 2)", "Ý nghĩa", "Cách tính"],
        [
            ["p", "P(Lₙ)", "Mức thạo sau lượt gần nhất",
             "Cập nhật Bayes có suy giảm — Thuật toán 3.5"],
            ["pTruoc", "P(Lₙ₋₁)", "Mức thạo TRƯỚC lượt ấy",
             "Giá trị p sau khi áp phép quên, trước khi cập nhật"],
            ["mastered", "P(L) ≥ θ", "Đã đạt ngưỡng thạo chưa", "So p với θ = 0,85"],
            ["nAttempts", "n", "Tổng số lượt tại nút này", "Cộng dồn"],
            ["nCorrect", "—", "Số lượt đúng", "Cộng dồn"],
            ["saiLienTiep", "S_c", "Số lần sai LIÊN TIẾP",
             "Đúng một lần là về 0 — xem cảnh báo"],
            ["msTong · msDem", "—", "Tổng và mẫu số của thời gian phản hồi",
             "Cộng dồn bằng TỔNG, không nhân trung bình cũ"],
            ["msTrungBinh", "RT_avg", "Thời gian phản hồi trung bình",
             "msTong / msDem; `null` khi chưa có lượt nào đo được"],
            ["goiTong · goiTrungBinh", "H_req", "Số gợi ý đã thấy, tổng và trung bình",
             "Cộng dồn"],
            ["lastSeen", "T_last", "Mốc lần chạm gần nhất",
             "Đầu vào bắt buộc của phép quên"],
            ["lastMicroId", "—", "Bài gần nhất chạm nút này", "Ghi đè"],
            ["unit · learnerId · mon · maNutDs", "—", "Trường định danh và phân loại",
             "Chép từ bản ghi lượt"],
        ],
        ten="Bảng 3.12: Lược đồ hồ sơ nút tri thức (mastery)",
    )

    canh_bao(d,
        "Trường `saiLienTiep` khác hẳn `nAttempts` và khác hẳn số lần làm cả "
        "bài. Cái cần đo là “ĐANG bí”, không phải “TỪNG bí”: một người học sai "
        "ba lần rồi đúng mười lần thì tỉ lệ đúng trông vẫn đẹp, trong khi ba lần "
        "sai liên tiếp lúc ấy là tín hiệu cần can thiệp. Vì vậy đúng một lần là "
        "biến đếm về 0.")

    canh_bao(d,
        "Trường `msTrungBinh` trả `null` khi chưa có lượt nào đo được thời gian, "
        "chứ không trả 0. Với dữ liệu đời cũ hoặc màn hình chưa bấm giờ, coi giá "
        "trị thiếu là 0 sẽ kéo trung bình xuống và biến “người học trả lời nhanh "
        "dần” thành một kết luận do lỗi ghi sinh ra.")

    doan(d,
        "Thực thể THẺ ÔN hiện thực lịch lặp lại ngắt quãng theo hộp Leitner. Mỗi "
        "thẻ mang mã bài, loại thẻ (thẻ từ vựng hay thẻ câu), số hộp hiện tại và "
        "mốc đến hạn. Năm khoảng cách của các hộp là 1 · 3 · 7 · 14 · 30 ngày. "
        "Sau một lượt ôn, thẻ đúng thì lên một hộp, thẻ sai thì VỀ HỘP 0 chứ "
        "không lùi một nấc — thẻ vừa quên phải gặp lại ngày mai, trong khi lùi "
        "từ hộp 4 xuống hộp 3 vẫn còn tận bảy ngày nữa.")

    # ── 3.2.5 ──────────────────────────────────────────────────────────────
    d.add_heading("3.2.5. Vector trạng thái người học", level=2)
    doan(d,
        "Bốn chiều của mô hình thích ứng đa chiều (mục 2.1.2) được gom thành một "
        "vector trạng thái tại thời điểm t:")
    cong_thuc(d, "S_u(t) = [ C(t), T(t), P(t), M ]")

    bang(d,
        ["Chiều", "Thành phần", "Nguồn dữ liệu", "Dạng trả về"],
        [
            ["C — Nhận thức", "Mức nắm các nút của bài hiện tại",
             "Trung bình p của các nút trong bài, lấy từ `mastery`",
             "Nhãn: vững · đang học · yếu · chưa có số liệu"],
            ["T — Thời gian", "Có lâu không gặp lại",
             "`lastSeen` xa nhất trong các nút của bài",
             "Nhãn luận lý: hay quên (≥ 14 ngày)"],
            ["P — Sư phạm", "Định dạng người học làm tốt nhất",
             "Hồ sơ định dạng, đòi tối thiểu 8 lượt mỗi định dạng",
             "Mã định dạng, hoặc `null` khi chưa đủ mẫu"],
            ["M — Động lực", "Sở thích cá nhân",
             "Người học tự chọn, lưu ở học bạ để sống qua nhiều buổi",
             "Chuỗi chủ đề"],
        ],
        ten="Bảng 3.13: Bốn chiều của vector trạng thái",
    )

    canh_bao(d,
        "Vector trả về NHÃN chứ không trả về SỐ THÔ, và đây là một ràng buộc bắt "
        "buộc chứ không phải lựa chọn trình bày. Nơi tiêu thụ vector là lời nhắc "
        "cho mô hình ngôn ngữ; số thô thì mô hình không biết dùng, và tệ hơn, nó "
        "có thể nhại lại nguyên văn con số ấy trước mặt trẻ. Nhãn thì dịch được "
        "thành câu người, và câu người thì đọc to lên cũng không sao.")

    # ── 3.2.6 ──────────────────────────────────────────────────────────────
    d.add_heading("3.2.6. Bốn bất biến của kho lưu vết", level=2)
    doan(d,
        "Kiến trúc lưu vết hướng sự kiện chỉ có giá trị nếu kho sự kiện giữ được "
        "một số bất biến, và các bất biến ấy phải kiểm tra được bằng phép chạy "
        "tự động chứ không bằng niềm tin vào mã nguồn. Bốn bất biến dưới đây "
        "được rút ra từ những lỗi đã xảy ra thật trong quá trình phát triển; mỗi "
        "bất biến kèm một phép kiểm chạy trực tiếp trên kho dữ liệu.")

    bang(d,
        ["Bất biến", "Phát biểu", "Phép kiểm", "Bắt được lỗi gì"],
        [
            ["B1 — Mỗi phiên một chủ",
             "Một mã phiên chỉ sinh ở một lần mở bài của một người học",
             "Nhóm theo `sessionId`, đếm số `learnerId` phân biệt; phải bằng 1",
             "Cơ chế nhận lại dữ liệu học thử gán nhầm bản ghi sang người học khác"],

            ["B2 — Dãy số thứ tự liền",
             "Mã bản ghi nhúng số thứ tự lượt trong phiên nên dãy phải liền",
             "Nhóm theo bộ ba (người học · phiên · bài), kiểm dãy không thủng",
             "Mất bản ghi giữa chừng"],

            ["B3 — Mô hình suy được từ nhật ký",
             "Tổng số lượt trong hồ sơ mỗi nút bằng đúng số bản ghi của nút ấy",
             "So `nAttempts` với số bản ghi; và dựng lại hồ sơ từ nhật ký rồi đối chiếu",
             "Hàm nền bỏ sót lượt, hoặc có ai ghi tay vào mô hình"],

            ["B4 — Không nút nào có lượt mà thiếu hồ sơ",
             "Chiều ngược của B3",
             "Lấy tập nút có trong nhật ký trừ tập nút có hồ sơ; phải rỗng",
             "Hàm nền không chạy cho một loại lượt nào đó"],
        ],
        ten="Bảng 3.14: Bốn bất biến và phép kiểm tương ứng",
    )

    canh_bao(d,
        "Bốn phép kiểm trên KHÔNG bắt được việc mất phần đuôi: nếu những lượt "
        "cuối của một phiên không bao giờ lên máy chủ thì dãy số thứ tự vẫn "
        "liền, chỉ ngắn hơn thực tế. Muốn phát hiện thì phải so với một nguồn "
        "độc lập, hoặc đếm tay trong một buổi đi thử có kiểm chứng. Không được "
        "đọc kết quả “không lỗ” thành “không mất gì”.")

    doan(d,
        "Việc nêu bốn bất biến này ở tầng thiết kế, thay vì coi chúng là chi "
        "tiết vận hành, xuất phát từ một quan sát: kho sự kiện hỏng TRONG IM "
        "LẶNG. Mọi độ đo về mô hình người học, về tiến bộ và về hiệu quả can "
        "thiệp đều đứng trên giả định “nhật ký đầy đủ và đúng chủ”. Nếu giả định "
        "ấy sai mà không có phép kiểm nào phát hiện, toàn bộ kết quả thực nghiệm "
        "sẽ sai theo một cách không nhìn thấy được từ chính các kết quả ấy.")
