#!/usr/bin/env python3
"""
CHƯƠNG 3 (bản viết lại) — phần A: mục 3.1 đến 3.5.

    3.1  bài toán, ràng buộc, kiến trúc                       (rút gọn từ bản v2)
    3.2  đồ thị tri thức: thành hình · biểu diễn · CÀI ĐẶT     (viết mới)
    3.3  phiên của một cá nhân: lưu gì, lưu thế nào            (viết mới)
    3.4  TIÊU CHÍ phát hiện lỗ hổng và thủ tục chẩn đoán       (viết mới phần tiêu chí)
    3.5  phương pháp gợi ý can thiệp                           (rút gọn)
"""
from __future__ import annotations

from chuong3_v3_khung import (
    SO, bang, canh_bao, cham, cong_thuc, do, doan, hinh, json_khoi, ma_lenh,
    sn, sv, thuat_toan,
)

H = SO["hangSo"]
DT = SO["doThi"]
KC = SO["khoCau"]


def viet(d):
    _m31(d)
    _m32(d)
    _m33(d)
    _m34(d)
    _m35(d)


# ═══════════════════════════════════════════════════════════ 3.1 ═══════════
def _m31(d):
    d.add_heading("3.1. Phát biểu bài toán, ràng buộc và kiến trúc", level=1)

    d.add_heading("3.1.1. Phát biểu bài toán", level=2)
    doan(d,
         "Cho một miền tri thức môn Tiếng Anh được biểu diễn bằng đồ thị có "
         "hướng, có nhãn; một kho học liệu mà mỗi câu hỏi đã được gắn với một "
         "nút của đồ thị; và chuỗi tương tác quan sát được của một người học cụ "
         "thể. Yêu cầu là xác định, tại mỗi thời điểm, ba đại lượng:")
    cham(d, [
        ("Trạng thái tri thức — ", "xác suất người học đã nắm vững từng nút, có "
         "tính đến suy giảm theo thời gian và đến quan hệ tiên quyết."),
        ("Vị trí lỗ hổng — ", "khi người học thất bại lặp lại, xác định nút nào "
         "là nguyên nhân, phân biệt với nút nơi lỗi biểu hiện. Hai nút này "
         "thường không trùng nhau, và đó chính là chỗ một hệ thống thích ứng "
         "khác một hệ thống chỉ thống kê tỷ lệ đúng — sai."),
        ("Can thiệp tiếp theo — ", "chọn nội dung, độ khó, định dạng và ngữ cảnh "
         "cho bước học kế tiếp, sao cho vừa nằm trong vùng phát triển gần, vừa "
         "không vi phạm ràng buộc vốn từ của khối lớp."),
    ])
    doan(d,
         "Điều làm bài toán này khác bài toán học tập thích ứng tổng quát nằm ở "
         "đối tượng người dùng: người học từ sáu đến mười một tuổi, một tỷ lệ "
         "đáng kể chưa đọc thông tiếng Việt và hầu như không đọc được một câu "
         "hướng dẫn bằng tiếng Anh. Ràng buộc ấy loại bỏ nhiều giải pháp vốn "
         "hiển nhiên với người học trưởng thành — không thể yêu cầu tự đánh giá "
         "năng lực, không thể giải thích bằng một đoạn văn bản, không thể để "
         "người học tự chọn lộ trình — đồng thời làm tăng đáng kể cái giá của "
         "một nội dung sai: với người lớn, một câu tiếng Anh sai ngữ pháp là "
         "một bất tiện; với trẻ đang trong giai đoạn bắt chước ngôn ngữ, đó là "
         "một nội dung dạy sai và sẽ được ghi nhớ.")

    d.add_heading("3.1.2. Sáu ràng buộc thiết kế", level=2)
    bang(d, ["Mã", "Phát biểu ràng buộc", "Hệ quả thiết kế"], [
        ["R1", "Người học không phải đọc chữ để biết cần làm gì",
         "Mọi điều kiện đi tiếp biểu diễn bằng biểu tượng; thanh nhiệm vụ gồm "
         "các ô có ba trạng thái phân biệt được bằng thị giác"],
        ["R2", "Không người học nào bị kẹt vĩnh viễn",
         "Luật đi tiếp tách khỏi hàm chính sách: đã đạt, hoặc đã thử thật ít "
         "nhất hai lần (mục 3.5.1)"],
        ["R3", "Nội dung phải kiểm duyệt được trước khi đến tay người học",
         f"{sn(KC['tong'])} câu hỏi của phần học chính được sinh sẵn và đi qua "
         "92 phép kiểm tự động; mô hình ngôn ngữ chỉ được gọi ở ba vị trí, và "
         "tại đó vẫn bắt buộc qua hậu kiểm (mục 3.5.3)"],
        ["R4", "Hệ thống hoạt động được khi mất kết nối",
         f"Đồ thị phục vụ chẩn đoán rút gọn còn 127 KB và nạp về máy người học; "
         "nhật ký ghi vào bộ nhớ cục bộ rồi đẩy theo lô, mã bản ghi có tính lũy "
         "đẳng (mục 3.3.1)"],
        ["R5", "Máy chủ không lưu nội dung riêng tư của trẻ",
         "Bài viết, câu nói và lịch sử hội thoại không lưu ở tầng dịch vụ dùng "
         "chung; so sánh mẫu lời nhắc chỉ dựa trên vân tay của phần khung"],
        ["R6", "Mọi con số hiển thị cho người lớn phải mang nhãn nguồn",
         "Điểm do máy chấm, thời lượng suy ra và thời lượng đo trực tiếp là ba "
         "đại lượng khác nhau về bản chất; trường nguồn đi kèm mọi con số"],
    ], ten="Bảng 3.1: Sáu ràng buộc thiết kế và hệ quả")
    doan(d,
         "R2 và R3 có xu hướng đối lập với nguyên tắc “cá nhân hoá tối đa” "
         "thường gặp trong tài liệu về học tập thích ứng. Nghiên cứu này không "
         "xem đó là nhược điểm mà là một đánh đổi có chủ đích; tiêu chí phân "
         "định cho đánh đổi ấy được nêu ở mục 3.5.3.")

    d.add_heading("3.1.3. Kiến trúc và vòng lặp thích ứng", level=2)
    doan(d,
         "Hệ thống được tổ chức thành bốn tầng. Ranh giới giữa chúng đặt theo "
         "một nguyên tắc duy nhất: tầng nào thực thi được mà không cần kết nối "
         "thì đặt tại máy người học; tầng nào cần dữ liệu của nhiều phiên hoặc "
         "nhiều người học thì đặt tại máy chủ, dưới dạng hàm nền — đoạn mã được "
         "kích hoạt mỗi khi có một bản ghi mới, chứ không phải một tiến trình "
         "chạy thường trực. Toàn bộ phép chẩn đoán vì vậy nằm ở phía máy người "
         "học, và đó là lý do đồ thị phải được rút gọn (mục 3.2.5).")
    hinh(d, "h1_kien_truc",
         "Hình 3.1: Kiến trúc bốn tầng và vòng lặp thích ứng bảy bước")
    canh_bao(d,
             "Bước 3 và bước 4 nối với nhau qua máy chủ chứ không qua bộ nhớ "
             "cục bộ, nên giữa hai bước tồn tại một độ trễ. Thiết kế chấp nhận "
             "độ trễ ấy: hàm chính sách đọc hồ sơ nút của lần nạp gần nhất, còn "
             "tín hiệu tức thời trong phiên — chuỗi trả lời sai liên tiếp — "
             "được đếm tại máy người học và được xét TRƯỚC mức tinh thông "
             "(mục 3.5.1).")


# ═══════════════════════════════════════════════════════════ 3.2 ═══════════
def _m32(d):
    d.add_heading("3.2. Đồ thị tri thức: thành hình, biểu diễn và cài đặt", level=1)
    doan(d,
         "Mục này trả lời bốn câu hỏi tách bạch nhau mà một người đọc phản biện "
         "sẽ đặt ra theo đúng thứ tự: đồ thị được làm ra bằng cách nào; nó được "
         "định nghĩa hình thức ra sao và có quy mô bao nhiêu so với các hệ thống "
         "đã công bố; mỗi đỉnh và mỗi cạnh mang những thuộc tính gì; và trên "
         "máy, tập đỉnh cùng tập cạnh nằm ở bảng nào, được đọc bằng mệnh đề điều "
         "kiện nào.")

    # ── 3.2.1 ─────────────────────────────────────────────────────────────
    d.add_heading("3.2.1. Quy trình thành hình", level=2)
    doan(d,
         "Đồ thị không được sinh tự động từ văn bản và cũng không được vẽ tay "
         "trên một công cụ đồ hoạ. Nó được khai báo dưới dạng dữ liệu, qua sáu "
         "bước, mỗi bước để lại một con số kiểm chứng được:")
    hinh(d, "h2_thanh_hinh",
         "Hình 3.2: Sáu bước thành hình của đồ thị tri thức")
    cham(d, [
        ("① Số hoá — ", "đối chiếu sách giáo khoa của bộ sách đang dùng với yêu "
         "cầu cần đạt của Chương trình giáo dục phổ thông môn Tiếng Anh ban "
         "hành theo Thông tư 32/2018/TT-BGDĐT, tách mỗi mục từ vựng và mỗi mẫu "
         "câu thành một dòng dữ liệu."),
        ("② Khai đỉnh — ", "740 mục từ vựng và 164 mẫu câu của năm khối lớp "
         "tiểu học được khai trong năm tệp bảng chuẩn (mục 3.2.4), mỗi mục mang "
         "một mã định danh duy nhất theo khuôn "
         "«loại _ khối lớp _ bài _ tên»."),
        ("③ Khai cạnh — ", "215 mối tiên quyết được khai bằng tay trong trường "
         "thang[] của chính các tệp ấy, mỗi mối là một bộ ba (nút cần có trước, "
         "nút học sau, loại quan hệ). Việc khai bằng tay là có chủ đích: một "
         "quan hệ tiên quyết là một phán đoán sư phạm, không phải một tương "
         "quan thống kê."),
        ("④ Hợp nhất — ", f"các khối lớp được hợp nhất với phần đã số hoá của "
         "bậc trung học thành một đồ thị liên thông lớp 1–12 gồm "
         "3.989 đỉnh và 7.602 cạnh. Phạm vi rộng hơn phạm vi sử dụng là có lý "
         "do: chỉ khi giữ cả bậc trên thì các cạnh tiên quyết xuyên cấp mới tồn "
         "tại thật trong dữ liệu thay vì bị cắt cụt ở ranh giới lớp 5."),
        ("⑤ Kiểm — ", "đồ thị hợp nhất được soi bằng ba phép kiểm tự động: "
         "không cạnh treo (mọi cạnh có cả hai đầu tồn tại), không chu trình "
         "trên quan hệ tiên quyết, không cạnh trùng. Cả ba đại lượng ấy hiện "
         "đều bằng 0."),
        ("⑥ Rút gọn — ", f"bản lúc chạy được cắt xuống còn {sn(DT['nut'])} đỉnh "
         f"và {sn(DT['canh'])} cạnh, 127 KB trên đĩa và khoảng 21 KB khi truyền, "
         "đủ nhỏ để nạp về máy người học và duyệt ngoại tuyến."),
    ])
    canh_bao(d,
             "Bước ⑤ không phải thủ tục hình thức. Một chu trình trong quan hệ "
             "tiên quyết làm phép duyệt chẩn đoán ở mục 3.4.3 không bao giờ "
             "dừng — tức máy của người học treo giữa buổi học; một cạnh treo "
             "làm phép duyệt dừng sớm mà không phát ra dấu hiệu nào.")

    # ── 3.2.2 ─────────────────────────────────────────────────────────────
    d.add_heading("3.2.2. Định nghĩa hình thức và quy mô", level=2)
    doan(d, "Miền tri thức được biểu diễn bằng bộ bốn:")
    cong_thuc(d, "G = (V, E, τ, λ)",
              "V tập đỉnh · E ⊆ V × V tập cạnh có hướng · "
              "τ : V → T gán loại cho đỉnh · λ : E → R gán loại quan hệ cho cạnh")
    doan(d,
         "Cách biểu diễn này kế thừa lý thuyết không gian tri thức (Doignon và "
         "Falmagne, 1985): một trạng thái tri thức là một tập con "
         "của V đóng theo quan hệ tiên quyết, và chính tính đóng ấy cho phép "
         "suy ra điều chưa quan sát được từ điều đã quan sát. Phần nhãn trên "
         "đỉnh và trên cạnh theo quy ước đồ thị tri thức hiện đại (Hogan và "
         "cộng sự, 2021), còn việc dựng đồ thị từ chương trình và sách giáo "
         "khoa theo lối khai báo có kiểm chứng đi theo hướng của KnowEdu (Chen "
         "và cộng sự, 2018).")
    doan(d,
         "Trên bản đầy đủ, τ gán 27 loại đỉnh có khai và λ gán 29 loại quan hệ. "
         f"Trên bản lúc chạy, τ gán {len(DT['loaiNut']) - 1} loại đỉnh có khai "
         "(cùng một nhóm đỉnh bỏ trống trường loại, xem Bảng 3.4) và λ gán "
         f"{len(DT['loaiCanh'])} loại cạnh. Bảng 3.2 nêu hai bản; Bảng 3.3 đặt "
         "quy mô của đồ thị bên cạnh quy mô của những tập dữ liệu và hệ thống "
         "thường được dẫn trong tài liệu về theo dõi tri thức, để trả lời câu "
         "hỏi “bao nhiêu đỉnh thì đủ”.")
    bang(d, ["Tiêu chí", "Bản đầy đủ", "Bản lúc chạy"], [
        ["Khâu sử dụng", "dựng học liệu, chạy ngoại tuyến",
         "chẩn đoán tại máy người học"],
        ["Số đỉnh", "3.989", sn(DT["nut"])],
        ["Số cạnh", "7.602", sn(DT["canh"])],
        ["Phạm vi khối lớp", "lớp 1 – lớp 12", "lớp 1 – lớp 6"],
        ["Nội dung đỉnh", "đầy đủ nhãn, nghĩa, ví dụ, siêu dữ liệu",
         "mã loại, khối lớp, nhãn ngắn, bài dạy nút ấy"],
        ["Kích thước", "3,4 MB", "127 KB trên đĩa · ≈ 21 KB khi truyền"],
        ["Lý do tồn tại", "giữ cho cạnh tiên quyết xuyên cấp tồn tại thật",
         "đủ nhỏ để chẩn đoán chạy được ngoại tuyến (R4)"],
    ], ten="Bảng 3.2: Hai bản của đồ thị tri thức")

    bang(d, ["Hệ thống / tập dữ liệu", "Số đơn vị tri thức", "Nguồn"], [
        ["Tập ASSISTments 2009–2010 (skill builder)",
         "110 – 124 đơn vị kỹ năng (tuỳ bản đã lọc trùng)",
         "Liu và cộng sự (2021)"],
        ["Mô hình theo dõi tri thức của Corbett và Anderson",
         "vài chục quy tắc cho một chương của một môn",
         "Corbett và Anderson (1995)"],
        ["Không gian tri thức theo lý thuyết Doignon–Falmagne",
         "tập đỉnh cùng quan hệ tiên quyết, quy mô tuỳ miền",
         "Doignon và Falmagne (1985)"],
        ["Đồ thị tri thức giáo dục dựng bằng KnowEdu",
         "hàng trăm đến hàng nghìn khái niệm cho một môn",
         "Chen và cộng sự (2018)"],
        ["Đồ thị của nghiên cứu này — bản đầy đủ",
         "3.989 đỉnh, 12 khối lớp", "tự dựng, mục 3.2.1"],
        ["Đồ thị của nghiên cứu này — bản lúc chạy",
         f"{sn(DT['nut'])} đỉnh, trong đó {sn(DT['hocDuoc'])} đỉnh HỌC ĐƯỢC "
         "(sáu khối lớp)", "tự dựng, mục 3.2.1"],
    ], ten="Bảng 3.3: Quy mô đồ thị của nghiên cứu này đặt bên cạnh tài liệu đã công bố")
    doan(d,
         f"Con số {sn(DT['hocDuoc'])} đỉnh học được lớn hơn một bậc so với quy "
         "mô thường gặp trong tài liệu về theo dõi tri thức, và lý do nằm ở đơn "
         "vị phân rã chứ không ở tham vọng: các tập dữ liệu nêu trên lấy đơn vị "
         "là “kỹ năng” của môn Toán — một kỹ năng bao trùm nhiều bài tập cùng "
         "dạng — còn ở đây đơn vị là MỘT MỤC TỪ VỰNG hoặc MỘT MẪU CÂU, tức mức "
         "phân rã mịn nhất mà một câu hỏi tiếng Anh tiểu học có thể đánh giá. "
         "Phân rã mịn là điều kiện để chẩn đoán trỏ được vào một chỗ dạy lại "
         "được; cái giá phải trả là mỗi đỉnh có ít quan sát hơn, và đó chính là "
         "lý do mô hình cần cơ chế lan truyền trên đồ thị (mục 3.4.3) thay vì "
         "chỉ đếm riêng từng đỉnh.")

    # ── 3.2.3 ─────────────────────────────────────────────────────────────
    d.add_heading("3.2.3. Thuộc tính của đỉnh và của cạnh", level=2)
    doan(d,
         "Bảng 3.4 nêu phân bố loại đỉnh của bản lúc chạy. Tám loại đầu là đỉnh "
         f"HỌC ĐƯỢC — {sn(DT['hocDuoc'])} đỉnh, tức mẫu số của mọi phép đo mức "
         "phủ vốn; bốn loại ở dòng cuối là đỉnh TỔ CHỨC, dùng để gom nhóm chứ "
         "không phải thứ người học nắm hay không nắm, nên bị loại khỏi mẫu số.")
    bang(d, ["Loại đỉnh", "Số lượng", "Vai trò"], [
        ["vocabulary_item", sn(DT["loaiNut"].get("vocabulary_item", 0)),
         "mục từ vựng cụ thể — đơn vị đánh giá nhỏ nhất"],
        ["vocabulary", sn(DT["loaiNut"].get("vocabulary", 0)),
         "nhóm từ vựng theo chủ đề"],
        ["grammar", sn(DT["loaiNut"].get("grammar", 0)),
         "mẫu câu và cấu trúc ngữ pháp"],
        ["pronunciation", sn(DT["loaiNut"].get("pronunciation", 0)),
         "trọng âm và âm cần luyện"],
        ["unit", sn(DT["loaiNut"].get("unit", 0)), "đỉnh chứa, không đánh giá"],
        ["(bỏ trống trường loại)", sn(DT["loaiNut"].get("?", 0)),
         "mẫu câu lớp 1 — vẫn là đơn vị kiến thức thật"],
        ["prior_knowledge", sn(DT["loaiNut"].get("prior_knowledge", 0)),
         "kiến thức giả định người học đã có"],
        ["letter_sound", sn(DT["loaiNut"].get("letter_sound", 0)),
         "chữ cái và âm tương ứng"],
        ["review · fun_time · theme · course",
         sn(sum(DT["loaiNut"].get(k, 0)
                for k in ("review", "fun_time", "theme", "course"))),
         "đỉnh tổ chức, không dùng để đánh giá"],
    ], ten=f"Bảng 3.4: Phân bố loại đỉnh của đồ thị lúc chạy ({sn(DT['nut'])} đỉnh)")
    canh_bao(d,
             f"{sn(DT['loaiNut'].get('?', 0))} đỉnh mẫu câu lớp 1 bị bỏ trống "
             "trường loại trong dữ liệu gốc. Chúng vẫn được tính vào tập đỉnh "
             "học được chứ không bị loại ra: đây là kiến thức thật, và nếu loại "
             "ra thì mẫu số của khối lớp 1 hụt gần một nửa, khiến tỷ lệ phủ vốn "
             "tri thức tăng lên một cách giả tạo (mục 3.6.8).")

    doan(d,
         "Siêu dữ liệu trên đỉnh khác nhau theo loại. Bảng 3.5 nêu đầy đủ các "
         "trường của hai loại đỉnh được dùng nhiều nhất, kèm mục đích sử dụng "
         "của từng trường — một trường không có nơi tiêu thụ là một trường sẽ "
         "lệch với thực tế mà không ai phát hiện.")
    bang(d, ["Loại đỉnh", "Trường", "Ý nghĩa", "Nơi tiêu thụ"], [
        ["Mục từ vựng", "ma", "mã định danh duy nhất, ví dụ v_g3_u13_chair",
         "khoá liên kết với câu hỏi và với hồ sơ người học"],
        ["", "tu · ipa · nghia", "mặt chữ, phiên âm, nghĩa tiếng Việt",
         "hiển thị; ràng buộc vốn từ cho tầng sinh nội dung"],
        ["", "so_it · so_nhieu · dang_ing · dang_qk · dang_ngoi3",
         "các dạng biến đổi của từ",
         "hậu kiểm câu do mô hình sinh (Thuật toán 3.5)"],
        ["", "vai", "vai trò của từ trong câu hỏi (nói, chọn, gõ…)",
         "lựa chọn định dạng câu hỏi phù hợp"],
        ["", "hinh · hinh_ve", "biểu tượng hoặc hình minh hoạ",
         "câu hỏi không cần đọc chữ (R1)"],
        ["", "am_o · go_duoc", "vị trí trọng âm; từ này có gõ lại được không",
         "chấm phát âm; sinh câu bậc gõ chữ"],
        ["Mẫu câu", "ma", "mã định danh, ví dụ sp_g3_u13_2",
         "khoá liên kết như trên"],
        ["", "vi_du", "câu đầy đủ", "câu mẫu để người học lặp lại"],
        ["", "cong_thuc", "khuôn có ô trống, ví dụ «Where's the + [Room]?»",
         "hậu kiểm: dựng mọi cách điền hợp lệ rồi đối chiếu"],
        ["", "o_thay", "danh sách giá trị hợp lệ của ô trống",
         "sinh câu; kiểm tính duy nhất của đáp án"],
        ["", "thi · kieu_cau", "thì ngữ pháp và loại câu",
         "ràng buộc cho tầng sinh; phân loại chẩn đoán"],
        ["", "dung_de · tinh_huong", "chức năng giao tiếp và tình huống dùng",
         "phân công nhiệm vụ từng lượt ở phòng luyện nói"],
        ["", "phan", "phân tích câu thành các mảnh kèm vai trò",
         "giảng giải và dựng câu hỏi xếp thẻ"],
    ], ten="Bảng 3.5: Thuộc tính của đỉnh từ vựng và đỉnh mẫu câu")

    doan(d,
         "Cạnh mang ba thuộc tính: hai đầu và một nhãn loại. Nhãn loại là thuộc "
         "tính quan trọng nhất của cả đồ thị, vì nó quyết định cạnh nào được "
         "phép tham gia phép chẩn đoán.")
    bang(d, ["Loại cạnh", "Số lượng", "Ý nghĩa", "Dùng để chẩn đoán"], [
        ["ban_do", sn(DT["loaiCanh"].get("ban_do", 0)),
         "quan hệ tiên quyết của bản đồ gốc", "Có"],
        ["noi_bai", sn(DT["loaiCanh"].get("noi_bai", 0)),
         "bắc cầu giữa hai bài thuộc một nhóm từ có thứ tự", "Có"],
        ["trong_bai", sn(DT["loaiCanh"].get("trong_bai", 0)),
         "thứ tự đọc của hai từ liền nhau trong cùng một bài", "KHÔNG"],
    ], ten=f"Bảng 3.6: Phân bố loại cạnh của đồ thị lúc chạy ({sn(DT['canh'])} cạnh)")
    doan(d,
         "Loại trong_bai biểu diễn thứ tự đọc của hai từ liền nhau trong cùng "
         "một bài — ví dụ eighteen đứng trước nineteen. Đây không phải ràng "
         "buộc tiên quyết: sách giáo khoa dạy cả khối từ trong một buổi, nên "
         "lấy loại cạnh này đi khoá bài là chặn người học ngay giữa bài đang "
         "học. Vì vậy mọi phép duyệt chẩn đoán đều chạy trên tập cạnh đã lọc:")
    cong_thuc(d, "E_prereq = { e ∈ E : λ(e) ∈ {ban_do, noi_bai} }",
              f"|E_prereq| = {sn(DT['canhTienQuyet'])} cạnh, trong đó "
              f"{sn(DT['xuyenLop'])} cạnh xuyên khối lớp")
    doan(d,
         f"Một tính chất của đồ thị chi phối toàn bộ thiết kế phía sau: trong "
         f"{sn(DT['nut'])} đỉnh, chỉ {sn(DT['nutCoTienQuyet'])} đỉnh có ít nhất "
         "một cạnh tiên quyết đi vào. Điều này hợp lý về mặt ngôn ngữ học — học "
         "từ “book” không đòi hỏi biết “pen” trước — nhưng có hai hệ quả: phép "
         "định vị nguyên nhân chỉ chạy được trên phần đỉnh ấy (mục 3.4.3), và "
         "bản thân đồ thị không đủ để làm bộ truy xuất vốn từ, nên phải hợp "
         "nhất với một nguồn thứ hai (mục 3.5.3).")

    # ── 3.2.4 ─────────────────────────────────────────────────────────────
    d.add_heading("3.2.4. Cài đặt: tập đỉnh và tập cạnh nằm ở bảng nào", level=2)
    doan(d,
         "Đồ thị tồn tại trên máy dưới ba dạng, ở ba chặng khác nhau của quy "
         "trình. Bảng 3.7 nêu rõ dạng nào nằm ở tệp nào, ai ghi, ai đọc và ở "
         "chặng nào — đây là câu trả lời cho câu hỏi “cài đặt thì biểu diễn "
         "trên máy như thế nào”.")
    bang(d, ["Dạng", "Nơi lưu", "Cấu trúc", "Ai ghi", "Ai đọc"], [
        ["Bảng khai đỉnh và cạnh",
         "data/tienganh/chuan_lop1..5.json (5 tệp)",
         "unit[].tu[] — mỗi phần tử là một đỉnh từ vựng (18 trường); "
         "unit[].mau_cau[] — mỗi phần tử là một đỉnh mẫu câu (9–10 trường); "
         "thang[] — mỗi phần tử là một cạnh {can, truoc_khi, loai}",
         "người soạn học liệu, sửa tay",
         "bộ sinh học liệu và bộ xuất đồ thị, chạy ngoại tuyến"],
        ["Đồ thị đầy đủ",
         "data/ban_do_tieng_anh.json",
         "graph.nodes[] — mảng đỉnh, mỗi đỉnh có id, node_kind, grade và các "
         "trường riêng của loại; graph.edges[] — mảng cạnh {source, target, "
         "relation, properties, cross_grade}",
         "bộ hợp nhất, chạy một lần mỗi năm học",
         "bộ xuất đồ thị con; không nạp lúc chạy"],
        ["Đồ thị lúc chạy",
         "web/public/content/tienganh/do_thi.json",
         "nut — TỪ ĐIỂN khoá theo mã đỉnh, giá trị {t, b, n, g, u}; "
         "canh — DANH SÁCH CẠNH {can, truoc_khi, loai, xuyen_lop}",
         "tools/xuat_do_thi_con.py, sinh lại mỗi đợt dựng học liệu",
         "máy người học, nạp một lần cho cả phiên"],
    ], ten="Bảng 3.7: Ba dạng cài đặt của đồ thị tri thức")

    doan(d,
         "Bản lúc chạy dùng hai cấu trúc dữ liệu khác nhau cho hai tập, và sự "
         "khác nhau ấy xuất phát từ phép truy cập mà mỗi tập phải phục vụ. Tập "
         "đỉnh được lưu dưới dạng từ điển vì phép truy cập chủ yếu là tra một "
         "đỉnh theo mã — thời gian hằng số. Tập cạnh được lưu dưới dạng danh "
         f"sách vì phép truy cập chủ yếu là lọc theo một đầu; với "
         f"{sn(DT['canh'])} cạnh, một phép quét tuyến tính mất chưa tới một "
         "phần nghìn giây, nên việc dựng thêm danh sách kề bị loại bỏ có chủ "
         "đích: nó làm tệp to thêm mà không đổi được trải nghiệm.")
    doan(d,
         "Hai phép truy vấn cơ bản trên tập cạnh được định nghĩa bằng đúng hai "
         "mệnh đề điều kiện dưới đây; mọi thuật toán chẩn đoán ở mục 3.4 đều chỉ "
         "gọi hai phép này chứ không đọc thẳng tập cạnh:")
    ma_lenh(d, [
        "truoc(G, v)  =  { c.can       : c ∈ E,  c.truoc_khi = v  ∧  λ(c) ∈ {ban_do, noi_bai} }",
        "sau(G, v)    =  { c.truoc_khi : c ∈ E,  c.can       = v  ∧  λ(c) ∈ {ban_do, noi_bai} }",
    ], ten="Hai phép truy vấn cơ bản trên tập cạnh")
    canh_bao(d,
             "Mệnh đề λ(c) ∈ {ban_do, noi_bai} là MẶC ĐỊNH, và muốn lấy cả cạnh "
             "trong_bai thì bên gọi phải yêu cầu tường minh. Đặt mặc định ở "
             "phía an toàn là có chủ đích: quên lọc thì phép duyệt đi qua quan "
             "hệ thứ tự đọc và cho ra kết luận vô nghĩa về mặt sư phạm, mà kết "
             "luận ấy nghe vẫn có lý nên không ai cãi.")
    doan(d,
         "Hướng của cạnh được quy ước một lần cho toàn hệ thống: bộ ba "
         "{can: A, truoc_khi: B} đọc là “phải có A trước khi học B”. Hệ quả: "
         "truoc(B) trả về A và sau(A) trả về B. Đảo nhầm hai đầu thì phép lan "
         "truyền chẩn đoán chạy đúng chiều ngược lại — người học sai một từ ở "
         "bài 1 mà hệ thống đi tìm nguyên nhân ở bài 20.")

    # ── 3.2.5 ─────────────────────────────────────────────────────────────
    d.add_heading("3.2.5. Một mảnh đồ thị thật", level=2)
    doan(d,
         "Hình 3.3 trích một mảnh đồ thị bằng chính phép duyệt của hệ thống, "
         "xuất phát từ mẫu câu mà người học trong ví dụ ở mục 3.6 đang mắc. Tám "
         "đỉnh, bảy cạnh loại ban_do; mọi giá trị P(L) trên hình do hàm nền "
         "tính ra từ chuỗi trả lời ở Bảng 3.19, không phải giá trị gán tay.")
    hinh(d, "h3_manh_do_thi",
         "Hình 3.3: Mảnh đồ thị quanh mẫu câu sp_g3_u13_2, trích bằng phép "
         "duyệt ngược trần độ sâu 4")


# ═══════════════════════════════════════════════════════════ 3.3 ═══════════
def _m33(d):
    d.add_heading("3.3. Phiên làm việc của một cá nhân: lưu gì và lưu thế nào", level=1)

    d.add_heading("3.3.1. Định nghĩa phiên và bốn kho ghi", level=2)
    doan(d,
         "Một phiên được định nghĩa hẹp và thao tác được: MỘT LẦN MỞ BÀI LÀ MỘT "
         "PHIÊN. Khi màn bài học được dựng, hệ thống sinh một mã phiên gồm chữ "
         "p, mốc thời gian mã hoá cơ số 36 và năm ký tự ngẫu nhiên; mọi lượt "
         "trả lời trong lần mở bài ấy mang chung mã này. Định nghĩa hẹp như vậy "
         "để một phiên luôn có đúng một chủ sở hữu, đúng một bài học và một "
         "khoảng thời gian liền mạch — ba điều kiện để bất biến B1 ở mục 3.3.5 "
         "kiểm được.")
    hinh(d, "h4_luu_phien",
         "Hình 3.4: Bốn kho mà một phiên ghi vào, kèm chủ thể ghi của từng kho")
    doan(d,
         "Bốn kho khác nhau ở nhịp ghi và ở chủ thể ghi, và sự khác nhau ấy là "
         "thiết kế chứ không phải tình cờ: nhật ký lượt trả lời ghi sau mỗi "
         "lượt và bất biến, nên nó là nguồn gốc; ba kho còn lại đều suy ra được "
         "từ nó, nên chúng kiểm chứng được.")

    d.add_heading("3.3.2. Bản ghi lượt trả lời", level=2)
    doan(d,
         "Đây là đơn vị dữ liệu quan trọng nhất của toàn hệ thống. Bảng 3.8 nêu "
         "đầy đủ các trường, nhóm theo bốn nhóm ý nghĩa.")
    bang(d, ["Nhóm", "Trường", "Kiểu", "Ý nghĩa"], [
        ["Định danh và thời gian", "id", "chuỗi",
         "mã ghép: người học · phiên · bài · câu · số thứ tự lượt trong phiên"],
        ["", "learnerId · sessionId · microId · quyen · mon", "chuỗi",
         "người học, phiên, bài học, quyển học liệu, môn"],
        ["", "ts", "số", "mốc thời gian (mili-giây) theo đồng hồ máy người học"],
        ["", "serverTs", "dấu thời gian", "mốc do máy chủ đóng khi nhận"],
        ["", "v", "số", "phiên bản luật ghi (hiện là 2)"],
        ["Nhận thức", "bktUnit", "chuỗi",
         "MỘT nút được đánh giá — nút duy nhất được cập nhật mức tinh thông"],
        ["", "maNutDs", "mảng",
         "mọi nút câu hỏi chạm tới; ghi kèm cho lan truyền, KHÔNG dùng cộng điểm"],
        ["", "itemId", "chuỗi", "mã câu hỏi"],
        ["", "phase", "chuỗi",
         "practice · assess · check · worked được tính; intro · sample · teach không"],
        ["", "correct", "luận lý", "kết quả đúng hay sai"],
        ["", "answer · expected", "chuỗi", "câu trả lời thô và đáp án, cắt ở 120 ký tự"],
        ["Hành vi", "ms", "số", "thời gian phản hồi RIÊNG của lượt trả lời ấy"],
        ["", "tries", "số", "lượt thử thứ mấy của cùng một câu hỏi"],
        ["", "hintsUsed", "số", "số gợi ý đã hiển thị (hiện tự động sau hai lần sai)"],
        ["", "mode", "chuỗi", "định dạng câu hỏi"],
        ["Bối cảnh hệ thống", "mauPrompt · phienBanMau · vanTayPrompt",
         "chuỗi / số / chuỗi",
         "tên mẫu lời nhắc, số phiên bản, mã băm 12 ký tự của phần khung — chỉ "
         "có ở lượt có mô hình tham gia"],
    ], ten="Bảng 3.8: Lược đồ bản ghi lượt trả lời (kho attempts)")
    doan(d,
         "Dưới đây là một bản ghi thật, do chính hàm dựng bản ghi của hệ thống "
         "sinh ra cho lượt thứ 11 của phiên ví dụ ở mục 3.6 — lượt trả lời sai "
         "thứ ba liên tiếp:")
    json_khoi(d, SO["banGhiMau"], ten="Một bản ghi lượt trả lời, nguyên văn")
    canh_bao(d,
             "Trường bktUnit mang ĐÚNG MỘT nút, không phải cả maNutDs. Nếu một "
             "lượt trả lời đúng được tính công cho cả danh sách nút thì mức "
             "tinh thông tăng ảo và mô hình trở nên lạc quan quá mức — tức cho "
             "người học đi tiếp khi chưa thực sự vững. Ràng buộc “một lượt trả "
             "lời, một nút được cập nhật” vì vậy là điều kiện để mô hình không "
             "tự làm sai lệch chính mình.")
    doan(d,
         "Mã bản ghi nhúng đủ năm thành phần để dựng lại lần nữa cũng ra đúng "
         "mã cũ. Nhờ thế, việc đẩy lại hàng đợi nhiều lần không sinh bản ghi "
         "trùng — đó là điều kiện để hệ thống hoạt động được khi mất kết nối "
         "(R4). Mười một bản ghi của phiên ví dụ mang các mã:")
    ma_lenh(d, SO["maBanGhi"])
    canh_bao(d,
             "Số thứ tự ở cuối mã là thành phần không thể lược bỏ. Nếu đẩy từng "
             "lượt riêng lẻ thì số thứ tự luôn bằng 0, mọi lượt của cùng một "
             "câu hỏi ghi đè lên nhau, và hệ thống mất đúng thông tin mà nhật "
             "ký được sinh ra để lưu giữ: rằng người học đã sai ba lần rồi mới "
             "trả lời đúng.")

    d.add_heading("3.3.3. Hồ sơ nút tri thức", level=2)
    doan(d,
         "Hồ sơ nút là hiện thực cụ thể của mô hình che phủ: mỗi nút mà người "
         "học đã chạm tới có đúng một tài liệu, khoá theo mã nút. Bảng 3.9 nêu "
         "các trường kèm ánh xạ sang ký hiệu toán học của Chương 2.")
    bang(d, ["Trường", "Ký hiệu", "Ý nghĩa", "Cách tính"], [
        ["p", "P(Lₙ)", "mức tinh thông sau lượt gần nhất",
         "cập nhật Bayes có suy giảm (Thuật toán 3.1)"],
        ["pTruoc", "P(Lₙ₋₁)", "mức tinh thông trước lượt ấy",
         "giá trị p sau khi áp phép quên, trước khi cập nhật"],
        ["mastered", "P(L) ≥ θ", "đã đạt ngưỡng tinh thông chưa",
         f"so p với θ = {sv(H['theta'], 2)}"],
        ["nAttempts · nCorrect", "n", "tổng số lượt và số lượt đúng", "cộng dồn"],
        ["saiLienTiep", "S_c", "số lần sai liên tiếp tại nút này",
         "trả lời đúng một lần thì đặt lại về 0"],
        ["msTong · msDem", "—", "tổng và mẫu số của thời gian phản hồi",
         "cộng dồn bằng TỔNG, không nhân trung bình cũ"],
        ["msTrungBinh", "RT_avg", "thời gian phản hồi trung bình",
         "msTong / msDem; rỗng khi chưa đo được lượt nào"],
        ["goiTong · goiTrungBinh", "H_req", "số gợi ý đã hiển thị", "cộng dồn"],
        ["lastSeen", "T_last", "mốc tương tác gần nhất",
         "đầu vào bắt buộc của phép quên"],
        ["lastMicroId", "—", "bài học gần nhất chạm tới nút này", "ghi đè"],
        ["unit · learnerId · mon · maNutDs", "—", "định danh và phân loại",
         "sao chép từ bản ghi lượt trả lời"],
    ], ten="Bảng 3.9: Lược đồ hồ sơ nút tri thức (kho mastery)")
    doan(d,
         "Dưới đây là hồ sơ thật của nút mà người học trong ví dụ đang mắc, "
         "sau lượt thứ 11 của phiên:")
    json_khoi(d, SO["hoSoNutMau"], ten="Một hồ sơ nút tri thức, nguyên văn")
    canh_bao(d,
             "Trường msTrungBinh nhận giá trị rỗng khi chưa có lượt nào đo được "
             "thời gian, chứ KHÔNG nhận giá trị 0. Coi giá trị thiếu là 0 sẽ "
             "kéo trung bình xuống và biến kết luận “người học trả lời nhanh "
             "dần” thành một kết luận do lỗi ghi nhận sinh ra.")

    d.add_heading("3.3.4. Mệnh đề điều kiện của phép ghi và phép đọc", level=2)
    doan(d,
         "Quyền ghi và quyền đọc không nằm trong mã ứng dụng mà được khai ở "
         "tầng cơ sở dữ liệu, dưới dạng mệnh đề điều kiện do máy chủ kiểm trước "
         "khi chấp nhận mỗi lệnh. Đặt ở đó chứ không đặt trong mã ứng dụng là có "
         "lý do: mã ứng dụng chạy trên máy của người dùng nên sửa được, còn "
         "mệnh đề này thì không.")
    ma_lenh(d, [
        "match /attempts/{attemptId} {",
        "  allow read:   canRead(resource.data.learnerId)",
        "  allow create: isMine(request.resource.data.learnerId)",
        "             ∧  có đủ ['learnerId','microId','itemId','phase','correct','ts']",
        "             ∧  correct là luận lý",
        "             ∧  phase ∈ ['practice','assess','check','worked']",
        "             ∧  (không khai serverTs  ∨  serverTs = request.time)",
        "  allow update, delete:  SAI  ← không ai sửa được điểm đã ghi",
        "}",
        "",
        "match /mastery/{userId}/units/{unitId} {",
        "  allow read:   canRead(userId)",
        "  allow write:  SAI          ← chỉ hàm nền (quyền quản trị) được ghi",
        "}",
    ], ten="Mệnh đề điều kiện của hai kho quan trọng nhất")
    doan(d,
         "Ba mệnh đề đáng chú ý. Thứ nhất, allow update, delete: SAI làm cho "
         "nhật ký trở thành bất biến theo đúng nghĩa kỹ thuật, không phải theo "
         "quy ước — đây là điều kiện để bất biến B3 ở mục sau có nghĩa. Thứ "
         "hai, mệnh đề đòi đủ sáu trường bắt buộc chặn ngay tại máy chủ những "
         "bản ghi thiếu trường; thiếu một trường thì lệnh bị từ chối, nên hệ "
         "thống phải đếm và báo số bản ghi bị từ chối chứ không được bỏ qua "
         "trong im lặng. Thứ ba, mastery cấm mọi lệnh ghi từ phía người dùng: "
         "mô hình người học chỉ được sửa bởi hàm nền, nên nó luôn là hàm của "
         "nhật ký.")

    d.add_heading("3.3.5. Bốn bất biến của kho lưu vết", level=2)
    doan(d,
         "Tính toàn vẹn của kho sự kiện được phát biểu thành bốn bất biến kiểm "
         "được bằng chương trình, thay vì được giả định. Cả bốn đều rút ra từ "
         "những lỗi đã thực sự xảy ra trong quá trình phát triển.")
    bang(d, ["Mã", "Phát biểu bất biến", "Phép kiểm", "Lỗi phát hiện được"], [
        ["B1", "mỗi mã phiên chỉ sinh ra tại một lần mở bài của một người học",
         "nhóm theo sessionId, đếm số learnerId phân biệt; phải bằng 1",
         "bản ghi bị gán nhầm sang người học khác"],
        ["B2", "dãy số thứ tự lượt trong phiên phải liền mạch",
         "nhóm theo bộ ba (người học, phiên, bài), kiểm dãy không thủng",
         "mất bản ghi giữa chừng"],
        ["B3", "mô hình người học phải suy ra được từ nhật ký",
         "so nAttempts với số bản ghi của nút; dựng lại hồ sơ từ nhật ký gốc "
         "rồi đối chiếu", "hàm nền bỏ sót lượt, hoặc có can thiệp thủ công"],
        ["B4", "không nút nào có lượt trả lời mà thiếu hồ sơ",
         "tập nút có trong nhật ký trừ tập nút có hồ sơ; phải rỗng",
         "hàm nền không xử lý một loại sự kiện nào đó"],
    ], ten="Bảng 3.10: Bốn bất biến của kho lưu vết và phép kiểm tương ứng")
    canh_bao(d,
             "Bốn phép kiểm trên KHÔNG phát hiện được trường hợp mất phần đuôi "
             "của một phiên: nếu những lượt cuối không bao giờ được đẩy lên máy "
             "chủ thì dãy số thứ tự vẫn liền mạch, chỉ ngắn hơn thực tế. Không "
             "được đọc kết quả “không có lỗ hổng trong dãy” thành “không mất dữ "
             "liệu”. Muốn phát hiện, phải đối chiếu với một nguồn độc lập hoặc "
             "đếm thủ công trong một buổi kiểm chứng.")


# ═══════════════════════════════════════════════════════════ 3.4 ═══════════
def _m34(d):
    d.add_heading("3.4. Tiêu chí phát hiện lỗ hổng và thủ tục chẩn đoán", level=1)

    d.add_heading("3.4.1. Định nghĩa lỗ hổng và bốn tiêu chí phát hiện", level=2)
    doan(d,
         "Chẩn đoán trong nghiên cứu này được hiểu theo nghĩa hẹp: phân biệt "
         "NƠI LỖI BIỂU HIỆN với NƠI LỖ HỔNG THỰC SỰ NẰM. Một lỗ hổng được định "
         "nghĩa như sau.")
    canh_bao(d,
             "Nút g là lỗ hổng gốc rễ của thất bại tại nút v khi và chỉ khi: "
             "(i) tồn tại một đường đi từ g tới v trên tập cạnh tiên quyết "
             "E_prereq, dài không quá d bước; (ii) mức tinh thông tại g chưa "
             "đạt ngưỡng; và (iii) trong số mọi nút thoả (i) và (ii), g có độ "
             "ngờ lớn nhất.")
    doan(d,
         "Định nghĩa ấy chỉ dùng được khi đã có một tiêu chí trả lời câu hỏi "
         "trước đó: khi nào thì hệ thống bắt đầu đi tìm lỗ hổng. Bốn tiêu chí "
         "dưới đây là toàn bộ điều kiện kích hoạt; hệ thống không đi tìm lỗ "
         "hổng ở bất kỳ tình huống nào khác.")
    bang(d, ["Mã", "Tiêu chí", "Điều kiện hình thức", "Căn cứ"], [
        ["TC1", "thất bại lặp lại tại một nút",
         f"S_c ≥ {H['saiLienTiepMac']} (số lần sai LIÊN TIẾP tại chính nút ấy)",
         "sai hai lần liền là chuyện thường của việc học; ba lần liền thì người "
         "học không tự thoát ra được bằng cách thử lại. Đây là tín hiệu TỨC "
         "THỜI, được xét TRƯỚC mọi đại lượng có quán tính"],
        ["TC2", "mức tinh thông tụt dưới ngưỡng yếu",
         f"P(L) < θ_yếu = {sv(H['thetaYeu'], 2)}",
         "dưới mức này thì luyện thêm cùng kiểu câu hỏi không khắc phục được — "
         "cần một bài vá nhắm vào nơi khác"],
        ["TC3", "nút có tiên quyết chưa vững",
         "∃ g : g →* v trên E_prereq, khoảng cách ≤ d = 4, và P(L_g) < θ",
         "điều kiện để việc định vị có nghĩa; nếu mọi tiên quyết đều đã vững "
         "thì lỗ hổng nằm ngay tại v"],
        ["TC4", "cả bài học có ít nhất một nút mắc",
         "∃ v ∈ N_bài : π(v) = PHỤ_ĐẠO",
         "ở cấp bài học, nhánh phụ đạo THẮNG nhánh vượt ải: một bài có mười nút "
         "mà chín nút vững và một nút mắc thì việc cần làm là gỡ nút ấy, không "
         "phải cho đi nhanh qua cả bài"],
    ], ten="Bảng 3.11: Bốn tiêu chí phát hiện lỗ hổng")
    doan(d,
         "TC1 và TC2 là hai tiêu chí độc lập, và việc giữ cả hai là cần thiết: "
         "một người học có thể có mức tinh thông tàm tạm mà vẫn vừa sai ba câu "
         "liền — lúc ấy con số trung bình không phải thứ đáng nghe; ngược lại, "
         "một người học có mức tinh thông rất thấp nhưng chưa sai đủ ba lần "
         "liên tiếp trong phiên này vẫn cần được vá. TC3 quyết định phép định "
         "vị có cho ra đích hay không; khi TC3 không thoả, hệ thống vá ngay tại "
         "nút đang mắc chứ không báo lỗi — nhiều nút vốn không có tiên quyết "
         "nào, và chính nó là gốc.")

    d.add_heading("3.4.2. Ước lượng trạng thái: mô hình Bayes có cơ chế quên", level=2)
    doan(d,
         "Mỗi lượt trả lời chạy qua một quy trình ba bước: suy giảm theo thời "
         "gian, cập nhật Bayes, rồi cơ hội học tập. Bước suy giảm dùng hàm mũ "
         "với nửa đời h:")
    cong_thuc(d, "P′(L) = 0,5 + ( P(L) − 0,5 ) · 2^( −Δt / h )",
              f"Δt là số ngày kể từ lần tương tác gần nhất; h = "
              f"{H['nuaDoiNgay']} ngày")
    doan(d,
         "Hàm kéo về 0,5 chứ không về 0: người học quên thì trở thành “không "
         "chắc”, chứ không thành “chưa từng biết”. Hệ quả cần nêu vì nó phản "
         "trực giác — một nút mà người học từng làm sai nhiều (P(L) thấp) sẽ "
         "NHÍCH LÊN theo thời gian. Điều đó đúng: lâu không kiểm thì hiểu biết "
         "hiện tại của hệ thống về người học nhạt đi theo cả hai chiều, chứ "
         "không phải người học giỏi lên.")
    thuat_toan(
        d, "3.1", "Cập nhật hồ sơ nút tri thức từ một lượt trả lời",
        "hồ sơ nút hiện có D (có thể rỗng); một lượt trả lời a gồm kết quả "
        "đúng/sai, thời gian phản hồi, số gợi ý, cờ câu bắt buộc đúng; mốc thời "
        "gian hiện tại t.",
        "hồ sơ nút mới, gồm mức tinh thông trước và sau, các biến đếm và các đại "
        "lượng hành vi cộng dồn.",
        [
            "1  Δt ← (t − D.lastSeen) / 86 400 000        // số ngày; thiếu ⇒ 0",
            f"2  p₀ ← D.p nếu có, ngược lại P(L₀) = {sv(H['L0'], 2)}",
            "3  p₀ ← 0,5 + (p₀ − 0,5) · 2^(−Δt / 14)      // BƯỚC QUÊN DẦN",
            "4",
            "5  (S, G) ← (0,06 , 0,15) nếu a.mustPass     // câu bẫy: tin cậy hơn",
            f"          ngược lại ({sv(H['slip'], 2)} , {sv(H['guess'], 2)})",
            "6  if a.correct:",
            "7      p₁ ← p₀(1 − S) / [ p₀(1 − S) + (1 − p₀)·G ]",
            "8  else:",
            "9      p₁ ← p₀·S / [ p₀·S + (1 − p₀)(1 − G) ]",
            f"10  p  ← p₁ + (1 − p₁)·T          với T = {sv(H['T'], 2)}   // CƠ HỘI HỌC TẬP",
            "11  p  ← kẹp(p, 0,001 , 0,999)",
            "12",
            "13  D′.pTruoc     ← p₀             // để tính ΔC ở mục 3.6.7",
            "14  D′.p          ← p",
            f"15  D′.mastered   ← (p ≥ θ)        với θ = {sv(H['theta'], 2)}",
            "16  D′.nAttempts  ← D.nAttempts + 1",
            "17  D′.nCorrect   ← D.nCorrect + [a.correct]",
            "18  D′.saiLienTiep← 0 nếu a.correct, ngược lại D.saiLienTiep + 1",
            "19  if a.ms hợp lệ:                            // THIẾU thì BỎ QUA,",
            "20      D′.msTong ← D.msTong + a.ms            //   không coi là 0",
            "21      D′.msDem  ← D.msDem + 1",
            "22  D′.msTrungBinh ← D′.msTong / D′.msDem nếu msDem > 0, ngược lại rỗng",
            "23  D′.goiTong     ← D.goiTong + a.hintsUsed",
            "24  D′.lastSeen    ← t",
            "25  return D′",
        ],
        ghi_chu=[
            "Dòng 5 là một dạng cá thể hoá tham số theo ĐƠN VỊ CÂU HỎI chứ "
            "không theo người học (Baker và cộng sự, 2008): chi phí ước lượng "
            "thấp hơn nhiều so với ước lượng riêng cho từng người học mà vẫn "
            "nắm được phần lớn khác biệt giữa các câu hỏi.",
            "Dòng 19–22: thời gian phản hồi thiếu thì không tính vào mẫu số. "
            "Việc cộng dồn thực hiện bằng TỔNG chứ không bằng cách nhân trung "
            "bình cũ với n − 1 — cách sau tích luỹ sai số dấu phẩy động sau vài "
            "trăm lượt, trong khi tài liệu này tồn tại suốt quá trình học.",
            "Phạm vi áp dụng: chỉ bốn pha mà người học TỰ đưa ra câu trả lời — "
            "luyện tập, sát hạch, câu chốt sau đoạn đọc hiểu, câu xen giữa ví "
            "dụ mẫu. Ba pha giới thiệu, làm mẫu, giảng bài bị loại trừ vì ở đó "
            "máy đang làm mẫu, tính vào mức tinh thông là ghi công cho người "
            "khác.",
        ])
    bang(d, ["Tham số", "Giá trị", "Căn cứ lựa chọn"], [
        ["P(L₀)", sv(H["L0"], 2),
         "bộ tham số phổ biến 0,25 kết hợp P(G) = 0,20 công nhận tinh thông chỉ "
         "sau hai câu đúng — quá dễ dãi với học sinh tiểu học"],
        ["P(T)", sv(H["T"], 2),
         "đặt để đạt nhịp bốn câu trả lời đúng liên tiếp mới công nhận tinh thông"],
        ["P(S)", f"{sv(H['slip'], 2)} (câu bẫy: 0,06)",
         "sơ suất ở lứa tuổi tiểu học không hiếm"],
        ["P(G)", f"{sv(H['guess'], 2)} (câu bẫy: 0,15)",
         "phần lớn câu hỏi là trắc nghiệm bốn lựa chọn"],
        ["θ — ngưỡng tinh thông", sv(H["theta"], 2),
         "với bộ tham số trên, tương ứng khoảng bốn câu đúng liên tiếp; và một "
         "câu sai sau đó kéo tụt xuống dưới ngưỡng"],
        ["θ_yếu", sv(H["thetaYeu"], 2),
         "dưới mức này thì luyện thêm cùng kiểu câu hỏi không khắc phục được"],
        ["h — nửa đời trí nhớ", f"{H['nuaDoiNgay']} ngày",
         "giá trị CHỌN theo lịch ôn sẵn có (+1 · +3 · +7 ngày); chưa hiệu chỉnh "
         "từ dữ liệu học thật — việc hiệu chỉnh là nội dung của kịch bản KB1"],
        ["α — hệ số lan truyền ngược", sv(H["alpha"], 1),
         "mỗi bước lùi về gốc thì độ ngờ còn lại 60 %; giá trị CHỌN, quét lưới ở KB1"],
        ["β — hệ số cộng hưởng xuôi", sv(H["beta"], 2),
         "mức cộng thêm cho nút dựng trên một nút đã vững; giá trị CHỌN"],
    ], ten="Bảng 3.12: Bộ tham số của mô hình và căn cứ lựa chọn")

    d.add_heading("3.4.3. Định vị nguyên nhân bằng lan truyền ngược", level=2)
    doan(d,
         "Khi một trong bốn tiêu chí ở Bảng 3.11 được kích hoạt, thuật toán "
         "duyệt ngược theo cạnh tiên quyết để xếp hạng các nút nền tảng theo "
         "mức độ khả nghi. Độ ngờ của một nút cách nút thất bại k bước:")
    cong_thuc(d, "doNgo(v) = α^k · ( 1 − P(L_v) ),   với α = 0,6",
              "α^k — càng xa chỗ sai thì càng khó gọi là nguyên nhân;  "
              "1 − P(L) — nút đã vững thì không phải thủ phạm, dù nó là tiên quyết")
    thuat_toan(
        d, "3.2", "Định vị nút gốc rễ",
        "đồ thị G; hồ sơ mức tinh thông M; nút thất bại v₀; trần độ sâu d = 4; "
        "số nút trả về tối đa m = 3.",
        "danh sách nút khả nghi, sắp giảm dần theo độ ngờ, mỗi nút kèm số bước "
        "và mức tinh thông hiện tại.",
        [
            "1  E′ ← { e ∈ E : λ(e) ∈ {ban_do, noi_bai} }   // LỌC THEO NHÃN CẠNH",
            "2  thăm ← {v₀};  KQ ← ∅;  biên ← [v₀]",
            "3  for k = 1 .. d:",
            "4      biên_mới ← []",
            "5      for u ∈ biên:",
            "6          for v ∈ truoc(G, u):",
            "7              if v ∈ thăm: continue",
            "8              thăm ← thăm ∪ {v};  KQ ← KQ ∪ {(v, k)}",
            "9              biên_mới ← biên_mới + [v]",
            "10      biên ← biên_mới",
            "11",
            "12  for (v, k) ∈ KQ:",
            "13      p ← M[v].p nếu có, ngược lại 0,10      // chưa học ⇒ đáng ngờ",
            "14      doNgo(v) ← 0,6^k · (1 − p)",
            "15  KQ ← { (v,k) ∈ KQ : p_v < θ }              // LOẠI nút ĐÃ TINH THÔNG",
            "16  return m phần tử đầu của KQ sắp giảm dần theo doNgo",
        ],
        ghi_chu=[
            "Dòng 1 là điều kiện ĐÚNG ĐẮN chứ không phải một tối ưu hoá hiệu "
            "năng: duyệt trên toàn bộ tập cạnh sẽ đi qua quan hệ cấu thành và "
            "quan hệ thứ tự đọc, cho ra kết luận vô nghĩa về mặt sư phạm.",
            "Dòng 3 — trần độ sâu tồn tại trước hết vì ý nghĩa sư phạm: một "
            "nguyên nhân cách vị trí lỗi bảy bước thì không còn can thiệp được. "
            "Đồng thời nó bảo đảm phép duyệt luôn dừng, kể cả khi đồ thị chứa "
            "chu trình.",
            "Dòng 13 và 15 hiện thực hai quy tắc đối xứng: nút CHƯA CÓ SỐ LIỆU "
            "được gán P(L₀) = 0,10 — rất đáng ngờ nhưng không phải 0, vì “chưa "
            "có tin” khác “đã đo và thấy hổng”; nút ĐÃ TINH THÔNG bị loại hẳn "
            "chứ không xếp hạng thấp, vì giữ lại thì màn hình có thể bày ra một "
            "“lỗ hổng gốc rễ” trỏ vào thứ người học làm đúng mãi.",
        ])
    doan(d,
         "Chiều ngược lại — cộng hưởng xuôi — cộng thêm β/k · P(L_g) cho các nút "
         "dựng trên một nút đã vững, với ba chốt: chỉ lan từ nút THẬT SỰ đã "
         "thạo, mức cộng nhỏ dần theo bước, và kết quả bị kẹp dưới một trần "
         f"cứng bằng θ − 0,05 = {sv(SO['congHuong']['tran'], 2)}. Trần cứng là "
         "chốt quan trọng nhất: để cộng hưởng đẩy một nút lên thẳng “đã thạo” "
         "khi người học chưa làm câu nào của nút ấy là tuyên thạo khống, và hệ "
         "thống sẽ bỏ qua bài người học chưa từng học, trong im lặng.")
    canh_bao(d,
             "Hiện trạng hiện thực: hàm cộng hưởng xuôi đã được viết đầy đủ và "
             "có cổng kiểm tự động, nhưng CHƯA được nối vào tầng thích ứng lúc "
             "chạy. Điều này không ảnh hưởng tới việc so sánh biến thể mô hình ở "
             "kịch bản KB2 — đó là phép chạy lại ngoại tuyến — nhưng lợi ích "
             "“vượt ải bài dễ ở chủ đề mới” hiện chưa tồn tại cho người học.")

    d.add_heading("3.4.4. Đánh giá tình trạng: sáu trạng thái và luật nhận dạng", level=2)
    doan(d,
         "Kết quả của hai mục trên được quy về một trong sáu tình trạng. Đây là "
         "toàn bộ không gian trạng thái mà tầng thích ứng phân biệt được; mọi "
         "quyết định ở mục 3.5 đều là hàm của tình trạng này chứ không đọc "
         "thẳng con số.")
    bang(d, ["Tình trạng", "Luật nhận dạng", "Ý nghĩa sư phạm", "Việc hệ thống làm"], [
        ["Chưa có số liệu", "không có hồ sơ nút, hoặc p rỗng",
         "người học chưa từng chạm nút này",
         "cho đi tiếp; xếp câu của nút này lên nhóm ưu tiên thứ hai"],
        ["Đang bế tắc", f"S_c ≥ {H['saiLienTiepMac']} (xét TRƯỚC mọi tiêu chí khác)",
         "sai liên tiếp, không tự thoát ra được bằng cách thử lại",
         "kích hoạt phụ đạo, mời chứ không cắt ngang"],
        ["Yếu hẳn", f"p < θ_yếu = {sv(H['thetaYeu'], 2)}",
         "luyện thêm cùng kiểu câu hỏi không gỡ được",
         "kích hoạt phụ đạo; xếp câu của nút này xuống nhóm thứ ba"],
        ["Trong vùng phát triển gần",
         f"{sv(H['thetaYeu'], 2)} ≤ p < {sv(H['theta'], 2)}",
         "đã biết đôi chút nhưng chưa chắc — luyện ở đây đổi được nhiều nhất",
         "cho đi tiếp; xếp câu của nút này LÊN ĐẦU"],
        ["Đã tinh thông", f"p ≥ θ = {sv(H['theta'], 2)}",
         "vững hẳn phần này", "đề xuất vượt ải; xếp câu của nút này xuống cuối"],
        ["Có nguy cơ quên", "lastSeen cách hiện tại ≥ 14 ngày",
         "mức tinh thông đang suy giảm dù chưa đo lại",
         "đưa vào lịch ôn; nêu ở chiều T của vectơ trạng thái"],
    ], ten="Bảng 3.13: Sáu tình trạng của một nút và luật nhận dạng")
    doan(d,
         "Bốn chiều của mô hình thích ứng đa chiều được tổng hợp thành một vectơ "
         "trạng thái S_u(t) = [C, T, P, M] ở cấp BÀI HỌC: C là mức nắm các nút "
         "của bài (trung bình p, trả về nhãn vững / đang học / yếu / chưa có số "
         "liệu); T là cờ nguy cơ quên; P là định dạng người học làm tốt nhất "
         f"(yêu cầu tối thiểu {SO['hanhVi']['toiThieuMau']} lượt mỗi định dạng, "
         "dưới ngưỡng trả về rỗng); M là sở thích do người học tự chọn.")
    canh_bao(d,
             "Vectơ trạng thái trả về NHÃN chứ không trả về số thô, và đây là "
             "ràng buộc bắt buộc chứ không phải lựa chọn trình bày. Nơi tiêu "
             "thụ vectơ là lời nhắc gửi cho mô hình ngôn ngữ; mô hình không sử "
             "dụng hiệu quả số thô, và nghiêm trọng hơn, nó có thể nhắc lại "
             "nguyên văn con số ấy trước mặt trẻ.")

    d.add_heading("3.4.5. Bảy tín hiệu hành vi đầu vào", level=2)
    doan(d,
         "Tầng chẩn đoán đứng trên bảy tín hiệu hành vi. Chỉ một trong bảy là "
         "quan sát trực tiếp được; sáu tín hiệu còn lại đều là kết quả suy "
         "luận, và mỗi suy luận có một cơ chế sai lệch riêng, nên Bảng 3.14 nêu "
         "cả ngưỡng cỡ mẫu lẫn giới hạn đã biết.")
    bang(d, ["Mã", "Hành vi", "Tín hiệu", "Ngưỡng và cỡ mẫu", "Giới hạn đã biết"], [
        ["H1", "trả lời đúng / sai", "kết quả chấm", "—",
         "chỉ bốn pha người học tự trả lời được tính"],
        ["H2", "đoán ngẫu nhiên", "tham số P(G) của mô hình",
         f"P(G) = {sv(H['guess'], 2)}; câu bẫy 0,15",
         "xử lý ở tầng mô hình, không phân biệt được từng lượt cụ thể"],
        ["H3", "bế tắc", "thời gian phản hồi cao mà vẫn sai",
         "ms ≥ 45 giây và trả lời sai", "bản ghi đời cũ không có ms đáng tin"],
        ["H4", "cần trợ giúp", "số gợi ý đã hiển thị",
         "gợi ý hiện tự động sau 2 lần sai",
         "là “đã hiển thị”, KHÔNG phải “đã yêu cầu”"],
        ["H5", "bỏ dở buổi học", "bản ghi rời màn hình khi chưa hoàn thành",
         "mỗi lần một bản ghi riêng",
         "là CẬN DƯỚI: đóng thẳng cửa sổ trình duyệt thì không ghi được"],
        ["H6", "mệt mỏi nhận thức", "thời gian phản hồi chậm dần trong phiên",
         f"≥ {SO['hanhVi']['toiThieuMoiNua']} lượt mỗi nửa; chênh ≥ "
         f"{int(SO['hanhVi']['nguongChamDan'] * 100)} %",
         "phải tách theo định dạng, nếu không sẽ luôn dương tính — xem mục 3.6.9"],
        ["H7", "khuynh hướng ưa một định dạng", "tỷ lệ đúng theo từng định dạng",
         f"≥ {SO['hanhVi']['toiThieuMau']} lượt mỗi định dạng",
         "dưới cỡ mẫu trả về “chưa đủ dữ liệu”, không trả về “kém”"],
    ], ten="Bảng 3.14: Bảy tín hiệu hành vi, ngưỡng và giới hạn")
    canh_bao(d,
             "Nguyên tắc xuyên suốt của cả bảng: CHƯA ĐỦ MẪU THÌ TRẢ VỀ “CHƯA "
             "BIẾT”, KHÔNG TRẢ VỀ “KÉM”. Ví dụ cụ thể của vòng lặp tự củng cố "
             "mà nguyên tắc ấy ngăn chặn: người học làm hai câu gõ chữ và sai "
             "cả hai, hệ thống kết luận yếu định dạng gõ chữ với tỷ lệ 0 %, "
             "giảm số câu gõ chữ, cỡ mẫu không bao giờ tăng thêm, và cái nhãn "
             "sai tự nuôi chính nó.")
    doan(d,
         "Bốn trong bảy tín hiệu hiện chỉ được đo và báo cáo cho người lớn, "
         "chưa được dùng để tự động điều chỉnh buổi học. Đây là lựa chọn có chủ "
         "đích: các ngưỡng ở cột thứ tư chưa được hiệu chỉnh trên dữ liệu học "
         "tập thực tế đủ lớn, và để một ngưỡng chưa hiệu chỉnh tự động can "
         "thiệp vào buổi học của một đứa trẻ là rủi ro lớn hơn giá trị thu "
         "được. Việc hiệu chỉnh là nội dung của kịch bản KB1 ở mục 3.8.")


# ═══════════════════════════════════════════════════════════ 3.5 ═══════════
def _m35(d):
    d.add_heading("3.5. Phương pháp gợi ý can thiệp", level=1)
    doan(d,
         "Hệ thống gợi ý ba loại can thiệp, xếp theo mức độ can thiệp tăng dần: "
         "đổi THỨ TỰ câu hỏi của chặng đang học; cho VƯỢT ẢI phần đã vững; và "
         "dựng một bài PHỤ ĐẠO nhắm vào nút gốc rễ. Mục này trình bày hàm chọn "
         "giữa ba loại ấy, rồi trình bày từng loại.")

    d.add_heading("3.5.1. Hàm chính sách và ranh giới quyền quyết định", level=2)
    thuat_toan(
        d, "3.3", "Hàm chính sách π ở cấp nút và cấp bài học",
        "hồ sơ nút D gồm mức tinh thông p và số lần sai liên tiếp S_c; hoặc "
        "danh sách nút của một bài học.",
        "một trong ba hành động — tịnh tiến, vượt ải, phụ đạo — kèm lý do diễn "
        "đạt bằng ngôn ngữ tự nhiên.",
        [
            "CHO MỘT NÚT π(D):",
            f"1  if S_c ≥ {H['saiLienTiepMac']}: return (PHỤ_ĐẠO, «sai S_c lần liên tiếp»)   // TC1, XÉT TRƯỚC",
            "2  if p không tồn tại: return (TIẾP, «chưa có số liệu»)",
            "3  if p ≥ θ:        return (VƯỢT_ẢI, «đã nắm vững»)",
            "4  if p < θ_yếu:    return (PHỤ_ĐẠO, «còn yếu»)          // TC2",
            "5  return (TIẾP, «đang trong vùng phát triển gần»)",
            "",
            "CHO MỘT BÀI HỌC π_bài(M, danh sách nút N):",
            "6  if N rỗng: return (TIẾP, «bài chưa gắn nút tri thức nào»)",
            "7  T ← [ π(M[v]) : v ∈ N ];   Mắc ← { t ∈ T : t = PHỤ_ĐẠO }",
            "8  if Mắc ≠ ∅:                                 // TC4 — PHỤ ĐẠO ƯU TIÊN",
            "9      sắp Mắc tăng dần theo p; nút yếu nhất là đích phụ đạo",
            "10      return (PHỤ_ĐẠO, nút_mắc = Mắc[0])",
            "11  if mọi t ∈ T đều là VƯỢT_ẢI: return (VƯỢT_ẢI)",
            "12  return (TIẾP)",
            "",
            "ĐIỀU KIỆN ĐƯỢC BỎ QUA BÀI HỌC:",
            "13  return đã_đạt_bài  AND  |N| ≥ 3  AND  π_bài(M, N) = VƯỢT_ẢI",
        ],
        ghi_chu=[
            "Dòng 1 hiện thực nguyên tắc “tín hiệu tức thời trước đại lượng có "
            "quán tính”. Một chi tiết hiện thực có hệ quả: chuỗi sai liên tiếp "
            "phải được đếm TẠI MÁY NGƯỜI HỌC theo từng lượt, vì hàm nền cập "
            "nhật hồ sơ nút sau một quãng trễ — lúc người học sai câu thứ ba "
            "thì con số trên máy chủ còn là 0 hoặc 1.",
            "Dòng 13 đặt cửa hẹp có chủ đích, đòi đủ ba điều kiện đồng thời. "
            "Thà để người học làm lại một bài đã nắm vững và mất vài phút, còn "
            "hơn bỏ qua một bài chưa vững, vì bài ấy còn là nền tảng cho những "
            "bài sau.",
        ])
    doan(d,
         "Hàm chính sách KHÔNG quyết định việc người học có được chuyển sang "
         "bài kế tiếp hay không. Quyền ấy thuộc về một bộ luật điều hướng riêng "
         "với đúng một điều kiện:")
    cong_thuc(d, "ĐI TIẾP ĐƯỢC  ⟺  đã ĐẠT  ∨  đã THỬ THẬT ≥ 2 lần")
    doan(d,
         "Vế thứ hai là lưới an toàn, và là hiện thực trực tiếp của ràng buộc "
         "R2. Lý do sống còn: mô hình có thể chấm sai, và một người học bị đánh "
         "giá nhầm không được phép bị kẹt vĩnh viễn — trẻ không có cách nào tự "
         "thoát, và cũng không biết để kêu. Cùng một luật được áp dụng nguyên "
         "vẹn ở ba cấp — mở bài học kế tiếp, mở chặng kế tiếp trong bài, và cho "
         "phép để lại một câu hỏi làm sau — để người học chỉ phải hiểu luật ấy "
         "một lần. Bài học đi tiếp theo lưới an toàn KHÔNG được ghi nhận là đã "
         "đạt: nó nằm trong danh sách còn nợ và phải hoàn thành mới mở được kỳ "
         "ôn tập chương.")

    d.add_heading("3.5.2. Gợi ý thứ tự: xếp câu theo vùng phát triển gần", level=2)
    doan(d,
         "Khi hàm chính sách trả về hành động tịnh tiến, tầng thích ứng xếp lại "
         "thứ tự câu hỏi trong kho của BẬC ĐỘ KHÓ HIỆN TẠI theo bốn nhóm, với "
         "hồ sơ định dạng làm khoá phụ.")
    bang(d, ["Thứ tự", "Nhóm", "Khoảng P(L)", "Căn cứ xếp ở vị trí này"], [
        ["1", "đang trong vùng phát triển gần",
         f"{sv(H['thetaYeu'], 2)} ≤ p < {sv(H['theta'], 2)}",
         "vùng luyện tập tạo ra thay đổi trạng thái lớn nhất; đưa lên đầu vì "
         "đầu buổi người học còn tỉnh táo nhất"],
        ["2", "chưa có số liệu", "—", "nút chưa từng tiếp cận; cần được học, và học sớm"],
        ["3", "yếu hẳn", f"p < {sv(H['thetaYeu'], 2)}",
         "xếp SAU chứ không phải trước: luyện thêm cùng kiểu câu hỏi ở nơi đang "
         "sai nhiều là dẫn tới sai tiếp, và mở đầu buổi học bằng ba câu sai "
         "liên tiếp làm người học mất động lực. Vị trí này cần bài phụ đạo"],
        ["4", "đã tinh thông", f"p ≥ {sv(H['theta'], 2)}",
         "vẫn cho làm nhưng xếp cuối; việc loại bỏ hẳn thuộc thẩm quyền của "
         "nhánh vượt ải"],
    ], ten="Bảng 3.15: Bốn nhóm sắp xếp thứ tự câu hỏi theo vùng phát triển gần")
    canh_bao(d,
             "Phép sắp xếp CHỈ đổi thứ tự, KHÔNG loại bỏ câu hỏi nào, và chỉ "
             "thực hiện trong phạm vi kho câu của một bậc độ khó. Loại bớt câu "
             "hỏi thì sổ tiến độ, thanh đếm câu và phép chấm đều sai lệch; trộn "
             "giữa các bậc thì thang độ khó do người soạn học liệu thiết lập bị "
             "phá vỡ.")

    d.add_heading("3.5.3. Gợi ý nội dung: bài phụ đạo bốn bước", level=2)
    doan(d,
         "Khi hàm chính sách trả về hành động phụ đạo, hệ thống dựng một bài vá "
         f"{H['soCauPhuDao']} câu nhắm vào nút gốc rễ. Bài này là chỗ duy nhất "
         "trong toàn hệ thống mà câu hỏi có thể không do bộ sinh tĩnh dựng sẵn, "
         "nên nó cũng là chỗ duy nhất cần một hàng rào hậu kiểm riêng.")
    thuat_toan(
        d, "3.4", "Dựng một bài phụ đạo",
        "đồ thị G; hồ sơ mức tinh thông M; nút đang mắc v_mắc; các bài đã tải "
        "sẵn B gồm bài hiện tại và các bài tiên quyết; vốn từ hợp lệ W; hàm gọi "
        f"mô hình (không bắt buộc); hàm hậu kiểm; số câu cần sinh n = "
        f"{H['soCauPhuDao']}.",
        "một bài phụ đạo gồm nút gốc rễ, danh sách câu hỏi, nguồn gốc của câu "
        "hỏi (tĩnh, mô hình, hoặc trộn), và cờ đã phải dùng phương án dự phòng.",
        [
            "1  // BƯỚC 1 — TRUY XUẤT: định vị đích",
            "2  g ← ĐỊNH_VỊ_GỐC_RỄ(G, M, v_mắc, m = 1)     // Thuật toán 3.2",
            "3  if g không tồn tại: g ← v_mắc              // nút không có tiên quyết",
            "4",
            "5  // BƯỚC 2 — TĨNH TRƯỚC: gom câu có sẵn quanh nút gốc rễ",
            "6  T ← ∅",
            "7  for bậc in [khởi_động, ráp_câu, thử_thách]:   // BẬC THẤP TRƯỚC",
            "8      for b ∈ B, for c ∈ b.kho[bậc]:",
            "9          if g ∉ ({c.maNut} ∪ c.maNutDs): continue",
            "10          T ← T + [c];  if |T| ≥ n: break",
            "11  T ← [ c ∈ T : HẬU_KIỂM(c) ]                // soi CẢ câu tĩnh",
            "12  if |T| ≥ n hoặc không có hàm gọi mô hình:",
            "13      return (g, T[0..n−1], nguồn = 'tĩnh', dự_phòng = false)",
            "14",
            "15  // BƯỚC 3 — SINH: chỉ bù phần còn thiếu",
            "16  try:  S ← GỌI_MÔ_HÌNH(nút = g, vốn = W, số_câu = n − |T|)",
            "17  except:  S ← ∅;  dự_phòng ← true           // KHÔNG ném lỗi ra ngoài",
            "18",
            "19  // BƯỚC 4 — HẬU KIỂM: hàng rào duy nhất còn lại",
            "20  S′ ← [ c ∈ S : c hợp khuôn ∧ HẬU_KIỂM(c) ]",
            "21  if |S′| < |S|: dự_phòng ← true             // có câu bị bác bỏ",
            "22  return (g, (T + S′)[0..n−1], nguồn, dự_phòng)",
        ],
        ghi_chu=[
            "Thứ tự ở Bước 2 NGƯỢC với trực giác, và đó là chủ ý. Tại thời điểm "
            "ấy người học đang học dở, vừa trả lời sai ba câu liên tiếp, và "
            "giao diện vừa thông báo sẽ hỗ trợ. Nếu lời gọi mạng thất bại mà "
            "người học nhận màn hình trống thì đó là sự cố nghiêm trọng hơn cả "
            "việc không có bài phụ đạo: vừa mất mạch học, vừa mất niềm tin vào "
            "chức năng vừa sử dụng.",
            "Dòng 11: hậu kiểm chạy CẢ trên câu tĩnh, dù câu tĩnh đã qua 92 "
            "phép kiểm khi dựng học liệu — vì hàm hậu kiểm ràng buộc theo vốn "
            "từ của PHIÊN HỌC HIỆN TẠI, hẹp hơn vốn từ lúc dựng.",
        ])
    doan(d,
         "Tiêu chí phân định giữa nội dung sinh sẵn và nội dung sinh lúc chạy "
         "được phát biểu như sau: một nội dung được phép sinh lúc chạy KHI VÀ "
         "CHỈ KHI thoả đồng thời ba điều kiện — (a) nội dung tĩnh không phục vụ "
         "được nhu cầu ấy; (b) tồn tại một phép hậu kiểm TẤT ĐỊNH có khả năng "
         "bác bỏ kết quả sai; và (c) có phương án dự phòng khi lời gọi thất "
         "bại. Ba vị trí trong hệ thống thoả cả ba điều kiện: bài phụ đạo, "
         "phòng luyện nói và chấm bài viết ngắn.")
    canh_bao(d,
             "Hiện trạng hiện thực: phòng luyện nói và chấm bài viết đang gọi "
             "mô hình thật. Bài phụ đạo đã được nối vào chặng luyện tập và chạy "
             "thật với toàn bộ 94 bài, nhưng hàm gọi mô hình để TRỐNG có chủ "
             "đích — sinh một câu hỏi khác hẳn sinh một câu nói: câu hỏi có "
             "phương án nhiễu, đáp án đúng duy nhất, gợi ý đi từ xa tới gần, mà "
             "hậu kiểm theo vốn từ (Thuật toán 3.5) không bắt được những lỗi "
             "ấy. Tiêu chí (b) vì vậy chưa thoả cho vị trí này, và theo đúng "
             "tiêu chí phân định vừa nêu, mô hình chưa được gọi cho tới khi có "
             "một tầng hậu kiểm riêng.")

    d.add_heading("3.5.4. Hậu kiểm tất định", level=2)
    doan(d,
         "Hậu kiểm là một hàm quyết định: cho một câu tiếng Anh do mô hình sinh "
         "ra, xác định câu ấy có được phép đưa cho người học hay không. Hàm có "
         "tính tất định, thực thi tại máy người học, không gọi mạng. Nó trả về "
         "kèm TÊN ĐƯỜNG công nhận, để bộ đo thống kê được theo từng đường.")
    thuat_toan(
        d, "3.5", "Hậu kiểm một câu tiếng Anh",
        "câu cần kiểm s; vốn từ hợp lệ W gồm từ vựng, mẫu câu và câu có sẵn "
        "trong sách; tên riêng của người học; câu của lượt trước.",
        "kết luận hợp lệ hoặc không, kèm tên đường công nhận hoặc lý do bác bỏ.",
        [
            "1  if s còn dấu ngoặc vuông: return (false, 'oTrong')   // CHỐT ĐẶT TRƯỚC",
            "2  c ← CHUẨN_HOÁ(s)       // thường hoá, bỏ dấu câu, gộp khoảng trắng",
            "3  if c rỗng: return (false, 'rong')",
            "4  if c = CHUẨN_HOÁ(câu_trước): return (false, 'lap')   // CHỐNG LẶP",
            "5",
            "6  // Năm đường công nhận",
            "7  if ∃ t ∈ W.từ, ∃ d ∈ DẠNG(t) : CHUẨN_HOÁ(d) = c: return (true, 'tu')",
            "8  if c ∈ CHUẨN_HOÁ(14 câu nghi thức lớp học):         return (true, 'nghiThuc')",
            "9  if ∃ m ∈ W.mẫu_câu : c ∈ NỬA_CỦA(m):                return (true, 'mauCau')",
            "10  if ∃ x ∈ W.câu_sách : CHUẨN_HOÁ(x) = c:            return (true, 'cauSach')",
            "11  for m ∈ W.mẫu_câu có công thức:",
            "12      for khung ∈ { m.công_thức } ∪ TÁCH_ĐÔI(m.công_thức):",
            "13          D ← tập giá trị hợp lệ của ô trống theo LOẠI_Ô_TRỐNG(khung)",
            "14          for d ∈ D:",
            "15              if CHUẨN_HOÁ(ĐIỀN(khung, d)) = c:      return (true, 'congThuc')",
            "16  return (false, 'ngoaiVon')",
        ],
        ghi_chu=[
            "Dòng 1 được bổ sung sau khi bộ đo của kịch bản KB3 phát hiện một "
            "lỗ hổng thật: bốn bài có công thức hai ô trống, phép điền chỉ thay "
            "ô đầu, ô sau còn nguyên “[Month B]”; mà hàm chuẩn hoá bóc sạch dấu "
            "ngoặc trước khi so, nên chuỗi khớp với chính nó và được nhận. Đây "
            "là ví dụ trực tiếp cho lập luận rằng hậu kiểm phải tất định và đo "
            "được, vì lỗi này không lời nhắc nào chặn được.",
            "Thuật toán DỰNG HẾT mọi khả năng rồi so sánh, thay vì đối sánh "
            "bằng biểu thức chính quy. Số cách điền rất nhỏ (bằng số mẫu câu "
            "nhân số từ vựng), nên phương pháp dựng hết vừa rẻ về chi phí tính "
            "toán, vừa không tạo chỗ cho một biểu thức chính quy viết sai lọt qua.",
        ])
