#!/usr/bin/env python3
"""CHƯƠNG 3 — phần 4: mục 3.7 (kịch bản thực nghiệm) và 3.8 (kết luận chương)."""
from __future__ import annotations

from chuong3_khung import (
    bang, canh_bao, cham, cong_thuc, do, doan, hinh_chu, ma_lenh, thuat_toan,
)


def viet(d):
    _m37(d)
    _m38(d)


# ═══════════════════════════════════════════════════════════════════════════
# 3.7 · KỊCH BẢN THỰC NGHIỆM
# ═══════════════════════════════════════════════════════════════════════════
def _kb(d, ma, ten, muc):
    """Một kịch bản: bảy phần cố định."""
    d.add_heading(f"{ma}. {ten}", level=3)
    for nhan, chu in muc:
        p = d.add_paragraph()
        p.paragraph_format.space_after = 0
        do(p, f"{nhan}: ", dam=True)
        if isinstance(chu, list):
            for x in chu:
                q = d.add_paragraph(style="List Bullet")
                q.paragraph_format.space_after = 0
                if isinstance(x, tuple):
                    do(q, x[0], dam=True)
                    do(q, x[1])
                else:
                    do(q, x)
        else:
            do(p, chu)
    d.add_paragraph()


def _m37(d):
    d.add_heading("3.7. Kịch bản thực nghiệm và đánh giá", level=1)

    # ── 3.7.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.7.1. Nguyên tắc chung và điều kiện tiền đề", level=2)
    doan(d,
        "Tám kịch bản dưới đây được sắp theo thứ tự chi phí tăng dần và mức độ "
        "phụ thuộc vào người học thật tăng dần. Bốn kịch bản đầu chạy được trên "
        "dữ liệu đã có hoặc trên dữ liệu mô phỏng; bốn kịch bản sau cần người "
        "học thật. Thứ tự này có chủ ý: kết quả của các kịch bản trước dùng để "
        "hiệu chỉnh tham số cho các kịch bản sau, và việc đưa một hệ thống chưa "
        "hiệu chỉnh vào lớp học thật vừa tốn kém vừa khó lý giải kết quả.")

    doan(d, "Ba điều kiện tiền đề phải thoả trước khi bắt đầu bất kỳ kịch bản nào:")
    cham(d, [
        ("Mốc dữ liệu — ", "chỉ dùng dữ liệu thu được TỪ SAU ngày 23-08-2026. "
         "Trước mốc này, đường ống ghi nhận có hai khiếm khuyết đã được xác định "
         "và khắc phục: mỗi phiên học chỉ có bản ghi đầu tiên lên được máy chủ, "
         "và cơ chế nhận lại dữ liệu học thử đã gán nhầm 130 trên 398 bản ghi "
         "sang người học khác. Dữ liệu đã được rà, làm sạch và dựng lại mô hình "
         "từ nguồn gốc; nhưng dữ liệu trước mốc không dùng để phân tích được."),
        ("Bốn bất biến — ", "chạy phép kiểm bốn bất biến (mục 3.2.6) trước và "
         "sau mỗi đợt thu dữ liệu. Kết quả phải là không phiên hai chủ, không lỗ "
         "trong dãy số thứ tự, mô hình khớp tuyệt đối với nhật ký, và không nút "
         "nào có lượt mà thiếu hồ sơ. Nếu một bất biến bị vi phạm thì mọi phân "
         "tích trên đợt dữ liệu ấy phải dừng cho tới khi tìm ra nguyên nhân."),
        ("Đạo đức và quyền riêng tư — ", "người tham gia là trẻ em, nên cần sự "
         "đồng ý của phụ huynh và của nhà trường trước khi thu dữ liệu; dữ liệu "
         "báo cáo phải ẩn danh; bảng xếp hạng hiển thị cho trẻ chỉ chứa biệt "
         "danh, khối lớp và số sao, không chứa bất kỳ thông tin định danh nào "
         "khác. Máy chủ không lưu bài viết và câu nói của trẻ."),
    ])

    canh_bao(d,
        "Việc công bố công khai đợt làm sạch dữ liệu là bắt buộc về mặt liêm "
        "chính khoa học, và cũng là lợi thế: người phản biện đối chiếu số liệu ở "
        "hai thời điểm sẽ thấy chênh lệch, và nói trước thì chênh lệch ấy trở "
        "thành bằng chứng của một quy trình kiểm soát dữ liệu có thật.")

    # ── 3.7.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.7.2. Tám kịch bản thực nghiệm", level=2)

    _kb(d, "KB1", "Hiệu chỉnh tham số mô hình bằng mô phỏng", [
        ("Mục tiêu", "Xác định bộ tham số BKT và nửa đời trí nhớ h cho ra hành "
         "vi mô hình phù hợp với kỳ vọng sư phạm, trước khi đưa vào lớp học thật."),
        ("Giả thuyết", "H1 — tồn tại bộ tham số sao cho ngưỡng θ = 0,85 tương "
         "ứng với khoảng bốn câu đúng liên tiếp và một câu sai kéo tụt xuống "
         "dưới ngưỡng. H2 — kết quả của hàm chính sách nhạy với θ nhiều hơn nhạy "
         "với α và β."),
        ("Thiết kế", [
            ("Người học mô phỏng — ", "sinh N = 1 000 người học ảo với năng lực "
             "tiềm ẩn phân bố chuẩn; mỗi người trả lời theo mô hình xác suất có "
             "tham số slip và guess thật khác với tham số mô hình dùng."),
            ("Quét lưới — ", "θ ∈ {0,75; 0,80; 0,85; 0,90; 0,95}; α ∈ {0,4; 0,5; "
             "0,6; 0,7; 0,8}; β ∈ {0,04; 0,08; 0,12}; h ∈ {7; 14; 21; 30} ngày."),
            ("Kiểm chứng nhịp — ", "với mỗi bộ tham số, chạy chuỗi mười lượt "
             "chuẩn (bốn đúng liền, một sai, ba đúng) và ghi lại lượt thứ mấy "
             "đạt ngưỡng."),
        ]),
        ("Dữ liệu", "Không cần dữ liệu thật. Chạy trực tiếp trên mã của hệ thống "
         "bằng node, không cần mạng và không cần cơ sở dữ liệu — điều kiện này "
         "có được nhờ mọi thuật toán ở mục 3.4 đều là hàm thuần."),
        ("Độ đo", "Số lượt tới thạo; số lượt tụt khỏi ngưỡng sau một câu sai; tỉ "
         "lệ tuyên thạo khống (mô hình nói thạo trong khi năng lực tiềm ẩn thấp); "
         "tỉ lệ bỏ sót (năng lực tiềm ẩn cao mà mô hình không công nhận)."),
        ("Phép kiểm định", "So sánh các bộ tham số bằng phân tích độ nhạy; vẽ "
         "đường đánh đổi giữa tỉ lệ tuyên thạo khống và tỉ lệ bỏ sót theo θ."),
        ("Rủi ro", "Người học mô phỏng theo đúng dạng mô hình mà ta đang đánh "
         "giá, nên kết quả có thể lạc quan. Giảm thiểu bằng cách cho tham số "
         "thật của người học ảo khác tham số mô hình, và thêm một nhóm người học "
         "ảo có hành vi quên theo dạng hàm khác."),
    ])

    _kb(d, "KB2", "Đánh giá mô hình ngoại tuyến trên nhật ký", [
        ("Mục tiêu", "Xác định mô hình nào dự đoán hành vi người học tốt nhất "
         "trong bốn biến thể, và xác định mô hình có được hiệu chuẩn tốt không."),
        ("Giả thuyết", "H1 — BKT có cơ chế quên dự đoán tốt hơn BKT chuẩn, và "
         "chênh lệch lớn hơn ở những lượt cách lần chạm trước từ 7 ngày trở lên. "
         "H2 — bổ sung lan truyền trên đồ thị cải thiện dự đoán ở những nút CÓ "
         "cạnh tiên quyết (150 trên 1 194 nút), và không đổi ở phần còn lại."),
        ("Thiết kế", [
            ("Bốn biến thể — ", "M0 tỉ lệ đúng cơ bản (mốc so sánh); M1 BKT "
             "chuẩn; M2 BKT có quên; M3 BKT có quên và có lan truyền."),
            ("Chia tập theo NGƯỜI HỌC — ", "kiểm chéo năm phần, tách theo người "
             "học chứ không theo lượt."),
            ("Phân tầng khi báo cáo — ", "báo riêng cho nhóm nút có tiên quyết "
             "và nhóm không có; báo riêng theo khoảng cách thời gian kể từ lần "
             "chạm trước."),
        ]),
        ("Dữ liệu", "Toàn bộ nhật ký lượt trả lời từ sau 23-08-2026. Cần tối "
         "thiểu vài nghìn lượt để các nhóm phân tầng còn đủ mẫu; đây là kịch bản "
         "chờ dữ liệu tích luỹ."),
        ("Độ đo", "AUC · RMSE · độ chính xác · sai lệch hiệu chuẩn theo mười "
         "nhóm xác suất (nhóm A, mục 3.6.2)."),
        ("Phép kiểm định", "So AUC giữa các biến thể bằng kiểm định DeLong trên "
         "cùng tập; so RMSE bằng kiểm định t bắt cặp trên các phần của kiểm chéo."),
        ("Rủi ro", "Cỡ mẫu nhỏ ở giai đoạn đầu làm khoảng tin cậy rộng. Phải báo "
         "khoảng tin cậy chứ không chỉ báo giá trị điểm, và phải nêu số người "
         "học thật sự đóng góp vào mỗi con số."),
    ])

    _kb(d, "KB3", "Kiểm chứng tầng chống ảo giác từ vựng", [
        ("Mục tiêu", "Định lượng đóng góp của tầng hậu kiểm, tách khỏi đóng góp "
         "của lời nhắc có ràng buộc."),
        ("Giả thuyết", "H1 — lời nhắc một mình KHÔNG đảm bảo được không có từ "
         "ngoài vốn; tỉ lệ vi phạm ở đầu ra thô lớn hơn 0 một cách có ý nghĩa. "
         "H2 — sau hậu kiểm, tỉ lệ vi phạm bằng 0."),
        ("Thiết kế", [
            ("Bộ kiểm — ", "chọn 30 bài trải đều năm quyển; với mỗi bài, sinh "
             "20 lượt gọi mô hình ở mỗi trong ba chỗ gọi (phụ đạo · phòng luyện "
             "nói · chấm bài viết), tổng khoảng 1 800 lượt."),
            ("Đo hai điểm — ", "ghi lại đầu ra THÔ của mô hình và kết quả SAU "
             "hậu kiểm cho từng lượt."),
            ("Phân tích chỗ trượt — ", "với mỗi câu bị bác, ghi lại nó trượt ở "
             "đường công nhận nào trong năm đường của Thuật toán 3.12."),
            ("Đảo chiều thử — ", "cố tình tắt từng đường công nhận rồi kiểm rằng "
             "tỉ lệ bác tăng đúng ở nhóm câu tương ứng; đây là phép chứng minh "
             "rằng mỗi đường thật sự có tác dụng, không phải mã chết."),
        ]),
        ("Dữ liệu", "Không cần người học thật. Vốn từ lấy từ dữ liệu bài; hồ sơ "
         "người học dùng bộ giả lập."),
        ("Độ đo", "OOV thô · OOV sau hậu kiểm · tỉ lệ bị bác theo từng đường "
         "công nhận · tỉ lệ phải lùi · tỉ lệ lặp câu · tỉ lệ sai khuôn trả về "
         "(nhóm C, mục 3.6.4)."),
        ("Phép kiểm định", "Khoảng tin cậy nhị thức cho từng tỉ lệ; so tỉ lệ vi "
         "phạm trước và sau hậu kiểm bằng kiểm định McNemar trên cùng tập lượt."),
        ("Rủi ro", "Kết quả gắn với một phiên bản mô hình cụ thể. Phải ghi lại "
         "tên mô hình, nhiệt độ, giới hạn token và vân tay lời nhắc cho mọi lượt "
         "trong bộ kiểm, để lần đo sau còn so được."),
    ])

    _kb(d, "KB4", "So sánh hiệu quả các mẫu lời nhắc bằng ΔC", [
        ("Mục tiêu", "Xác định mẫu lời nhắc nào cho ra bài phụ đạo giúp người "
         "học tiến bộ hơn, và kiểm chứng rằng chỉ số ΔC phân biệt được chúng."),
        ("Giả thuyết", "H1 — các mẫu lời nhắc khác nhau cho ra ΔC trung bình "
         "khác nhau một cách có ý nghĩa. H2 — mẫu có lồng ngữ cảnh theo sở thích "
         "cá nhân cho ΔC cao hơn mẫu không lồng."),
        ("Thiết kế", [
            ("Phân bổ ngẫu nhiên — ", "mỗi lần kích hoạt phụ đạo, chọn ngẫu "
             "nhiên một trong hai mẫu đang so; ghi số phiên bản mẫu vào bản ghi."),
            ("Giao thức A-R-A — ", "đo mức thạo trước, chạy bài phụ đạo, rồi đo "
             "lại bằng những câu KHÁC ở nút mục tiêu."),
            ("Lọc cặp hợp lệ — ", "áp Thuật toán 3.14; loại mọi cặp mà lần đo "
             "sau dùng lại câu của lần đo trước."),
        ]),
        ("Dữ liệu", "Cần tối thiểu 5 cặp hợp lệ cho mỗi mẫu để đưa ra con số, và "
         "thực tế cần vài chục cặp để kiểm định có sức mạnh. Đây là kịch bản phụ "
         "thuộc mạnh vào số lần kích hoạt phụ đạo, nên nên chạy song song với KB7."),
        ("Độ đo", "ΔC trung bình theo từng mẫu; số cặp hợp lệ; SỐ CẶP BỊ LOẠI và "
         "lý do loại."),
        ("Phép kiểm định", "Kiểm định t hai mẫu độc lập trên ΔC, hoặc "
         "Mann-Whitney nếu phân bố lệch; báo kèm cỡ ảnh hưởng."),
        ("Rủi ro", [
            ("Số cặp bị loại cao — ", "nếu phần lớn cặp bị loại vì trùng câu thì "
             "kho câu của nút mục tiêu quá mỏng, và kết luận dựng trên phần còn "
             "lại không đại diện. Phải báo tỉ lệ loại."),
            ("Trôi mô hình — ", "nhà cung cấp đổi trọng số giữa hai đợt đo sẽ "
             "trộn vào kết quả. Vân tay lời nhắc kèm tên mô hình cho phép phát "
             "hiện, nhưng không cho phép sửa chữa hồi tố."),
        ]),
    ])

    _kb(d, "KB5", "Đánh giá chất lượng học liệu bởi chuyên gia", [
        ("Mục tiêu", "Kiểm chứng rằng nội dung do hệ thống sinh — cả tĩnh lẫn "
         "lúc chạy — đạt chuẩn sư phạm theo đánh giá của giáo viên tiếng Anh "
         "tiểu học."),
        ("Giả thuyết", "H1 — tỉ lệ nội dung được chuyên gia chấp nhận không thấp "
         "hơn ngưỡng đặt trước. H2 — chuyên gia không phân biệt được câu sinh "
         "lúc chạy đã qua hậu kiểm với câu tĩnh, ở mức tốt hơn ngẫu nhiên."),
        ("Thiết kế", [
            ("Hội đồng — ", "5–7 giáo viên tiếng Anh tiểu học, không tham gia "
             "phát triển hệ thống."),
            ("Mẫu đánh giá — ", "200 câu hỏi chọn ngẫu nhiên phân tầng theo "
             "quyển, bậc độ khó và định dạng; trộn lẫn câu tĩnh với câu sinh lúc "
             "chạy đã qua hậu kiểm, không cho biết nguồn."),
            ("Thang chấm — ", "năm tiêu chí, mỗi tiêu chí thang Likert 5 mức: "
             "đúng ngữ pháp · phù hợp vốn từ khối lớp · phương án nhiễu hợp lý · "
             "chỉ có một đáp án đúng · gợi ý không lộ đáp án."),
            ("Câu hỏi phân biệt nguồn — ", "với mỗi câu, chuyên gia đoán đây là "
             "câu soạn sẵn hay câu máy sinh."),
        ]),
        ("Dữ liệu", "Không cần người học. Chuẩn bị bộ mẫu và biểu chấm."),
        ("Độ đo", "Điểm trung bình từng tiêu chí; tỉ lệ câu đạt cả năm tiêu chí; "
         "độ đồng thuận giữa các chuyên gia; tỉ lệ đoán đúng nguồn."),
        ("Phép kiểm định", "Hệ số kappa của Cohen hoặc Fleiss cho độ đồng thuận; "
         "kiểm định nhị thức so tỉ lệ đoán đúng nguồn với mức ngẫu nhiên 0,5."),
        ("Rủi ro", "Chuyên gia có thể chấm khắt khe hơn với câu họ NGHI là máy "
         "sinh. Việc giấu nguồn và trộn mẫu là để giảm thiểu chính điều này; "
         "câu hỏi phân biệt nguồn đặt ở CUỐI mỗi phiếu, sau khi đã chấm."),
    ])

    _kb(d, "KB6", "Kiểm chứng hiệu quả của xếp thứ tự theo vùng phát triển gần", [
        ("Mục tiêu", "Xác định việc xếp lại thứ tự câu theo bốn nhóm vùng phát "
         "triển gần có cải thiện kết quả học so với thứ tự do người soạn đặt hay "
         "không."),
        ("Giả thuyết", "H1 — nhóm có xếp lại đạt mức thạo trung bình cao hơn sau "
         "cùng một số lượt. H2 — nhóm có xếp lại có tỉ lệ bỏ dở thấp hơn, do "
         "buổi học không mở đầu bằng những câu người học đang sai nhiều."),
        ("Thiết kế", [
            ("Đối chứng ngẫu nhiên trong hệ thống — ", "phân bổ ngẫu nhiên mỗi "
             "người học vào nhóm CÓ hoặc KHÔNG xếp lại, giữ cố định suốt đợt."),
            ("Cân bằng — ", "phân tầng theo khối lớp và theo mức phủ vốn ban đầu."),
            ("Thời lượng — ", "tối thiểu bốn tuần, để cơ chế quên và lịch ôn "
             "ngắt quãng kịp có tác dụng."),
        ]),
        ("Dữ liệu", "Cần người học thật; nên chạy lồng trong KB7."),
        ("Độ đo", "Mức thạo trung bình theo số lượt; độ dốc đường cong học tập; "
         "số lượt tới thạo; tỉ lệ bỏ dở; số phút học đo thật."),
        ("Phép kiểm định", "Mô hình hồi quy đa mức với người học là hiệu ứng ngẫu "
         "nhiên, để tính tới việc các lượt của cùng một người không độc lập."),
        ("Rủi ro", [
            ("Nhiễu từ lưới đỡ — ", "luật “đạt hoặc thử đủ hai lần” hoạt động ở "
             "cả hai nhóm và có thể át hiệu ứng của việc xếp lại. Phải phân tích "
             "riêng nhóm người học chưa bao giờ dùng tới lưới đỡ."),
            ("Cỡ ảnh hưởng nhỏ — ", "xếp lại chỉ đổi THỨ TỰ, không đổi tập câu, "
             "nên hiệu ứng kỳ vọng nhỏ. Cần tính cỡ mẫu trước khi chạy."),
        ]),
    ])

    _kb(d, "KB7", "Thử nghiệm tại lớp học", [
        ("Mục tiêu", "Đánh giá hệ thống trong điều kiện sử dụng thật: người học "
         "thật, thiết bị thật, đường truyền thật, và động lực thật."),
        ("Giả thuyết", "H1 — người học có tiến bộ đo được qua đường cong học tập "
         "và mức phủ vốn. H2 — hệ thống ghi nhận đầy đủ hành vi trong điều kiện "
         "thật, tức bốn bất biến giữ nguyên và tỉ lệ lượt ghi thành công gần 100%."),
        ("Thiết kế", [
            ("Quy mô — ", "hai đến bốn lớp, mỗi lớp 25–35 học sinh, ở hai khối "
             "lớp khác nhau để phủ cả hai bậc học liệu."),
            ("Thời lượng — ", "tám tuần, hai buổi mỗi tuần, mỗi buổi 20–25 phút."),
            ("Đo đầu và cuối — ", "một bài kiểm tra giấy do giáo viên soạn, "
             "KHÔNG dùng câu của hệ thống, làm phép đo độc lập với mô hình."),
            ("Nhật ký vận hành — ", "chạy phép kiểm bốn bất biến hằng tuần; ghi "
             "lại mọi sự cố thiết bị, mất mạng và micro hỏng."),
        ]),
        ("Dữ liệu", "Toàn bộ nhật ký của đợt; hồ sơ nút; sổ thời gian học đo "
         "thật; bản ghi bỏ dở; kết quả bài kiểm tra giấy đầu và cuối."),
        ("Độ đo", "Cả bốn nhóm. Đặc biệt: tương quan giữa mức phủ vốn do hệ "
         "thống ước lượng và điểm bài kiểm tra giấy — đây là phép kiểm chứng "
         "HIỆU LỰC HỘI TỤ của mô hình, mạnh hơn mọi độ đo nội bộ."),
        ("Phép kiểm định", "Kiểm định t bắt cặp trên điểm đầu–cuối; hệ số tương "
         "quan giữa ước lượng của mô hình và điểm giấy; mô hình hồi quy đa mức "
         "cho tiến bộ theo thời gian."),
        ("Rủi ro", [
            ("Không có nhóm đối chứng ngoài — ", "so với lớp không dùng hệ thống "
             "thì khác biệt có thể do thời lượng học thêm chứ không do thích "
             "ứng. Nếu điều kiện cho phép, nên có một lớp dùng phiên bản đã tắt "
             "tầng thích ứng, giữ nguyên học liệu."),
            ("Hiệu ứng mới lạ — ", "tuần đầu trẻ hào hứng vì công cụ mới. Phân "
             "tích riêng tuần 1–2 và tuần 5–8."),
            ("Đo phát âm không thuần nhất — ", "thiết bị mỗi lớp khác nhau. Ghi "
             "lại loại thiết bị và tách điểm phát âm khỏi các phép đo tổng hợp."),
            ("Thiên lệch do người dạy — ", "giáo viên biết mục tiêu nghiên cứu "
             "có thể can thiệp khác thường. Ghi lại thời lượng và hình thức can "
             "thiệp của giáo viên."),
        ]),
    ])

    _kb(d, "KB8", "Kiểm chứng cơ chế chẩn đoán bằng đối chiếu với giáo viên", [
        ("Mục tiêu", "Xác định nút gốc rễ do hệ thống chỉ ra có trùng với chẩn "
         "đoán của giáo viên hay không. Đây là phép kiểm chứng trực tiếp nhất "
         "cho đóng góp cốt lõi của luận văn."),
        ("Giả thuyết", "H1 — tỉ lệ trùng khớp giữa nút gốc rễ do hệ thống chỉ ra "
         "và chẩn đoán của giáo viên cao hơn mức trùng khớp ngẫu nhiên. H2 — "
         "lan truyền ngược trên đồ thị chỉ ra nguyên nhân đúng hơn so với cách "
         "chỉ nhìn vào nút nơi lỗi lộ ra."),
        ("Thiết kế", [
            ("Chọn ca — ", "lấy 40 trường hợp người học có chuỗi sai từ ba lần "
             "liên tiếp trở lên tại một nút, trải đều các khối lớp."),
            ("Chẩn đoán độc lập — ", "giáo viên xem lại chuỗi câu trả lời của "
             "người học (KHÔNG xem kết quả của hệ thống) rồi chỉ ra nguyên nhân "
             "họ cho là gốc rễ, chọn từ danh sách nút của đồ thị."),
            ("Ba mốc so sánh — ", "(a) nút nơi lỗi lộ ra; (b) nút gốc rễ do hệ "
             "thống chỉ; (c) một nút tiên quyết chọn ngẫu nhiên."),
        ]),
        ("Dữ liệu", "Cần các ca thật từ KB7. Với mỗi ca, lưu lại toàn bộ danh "
         "sách nút khả nghi kèm độ ngờ, không chỉ nút đứng đầu."),
        ("Độ đo", "Tỉ lệ trùng khớp ở vị trí đầu; tỉ lệ nút giáo viên chọn nằm "
         "trong ba nút đầu của hệ thống; độ đồng thuận giữa các giáo viên."),
        ("Phép kiểm định", "Kiểm định McNemar so tỉ lệ trùng khớp giữa mốc (a) "
         "và mốc (b) trên cùng tập ca; kappa cho độ đồng thuận giữa giáo viên."),
        ("Rủi ro", [
            ("Giáo viên cũng có thể sai — ", "chẩn đoán của giáo viên là mốc so "
             "sánh, không phải chân lý. Nên báo cả các ca mà hai giáo viên chẩn "
             "đoán khác nhau, và phân tích riêng."),
            ("Đồ thị thưa — ", "chỉ 150 trên 1 194 nút có cạnh tiên quyết đi "
             "vào; với các nút còn lại, hệ thống trả về chính nút đang mắc. Phải "
             "báo riêng hai nhóm, nếu không thì tỉ lệ trùng khớp bị thổi lên bởi "
             "những ca mà hệ thống không thật sự chẩn đoán gì."),
        ]),
    ])

    # ── 3.7.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.7.3. Ma trận kịch bản và độ đo", level=2)
    bang(d,
        ["Kịch bản", "Nhóm A\nmô hình", "Nhóm B\nsư phạm", "Nhóm C\nnội dung",
         "Nhóm D\nhệ thống", "Cần người học thật?", "Phụ thuộc"],
        [
            ["KB1 Hiệu chỉnh tham số", "✔", "✔", "", "", "KHÔNG", "—"],
            ["KB2 Đánh giá ngoại tuyến", "✔", "✔", "", "✔", "Dữ liệu đã có", "KB1"],
            ["KB3 Chống ảo giác từ vựng", "", "", "✔", "✔", "KHÔNG", "—"],
            ["KB4 So mẫu lời nhắc", "", "✔", "✔", "", "CÓ", "KB3 · KB7"],
            ["KB5 Chuyên gia chấm học liệu", "", "", "✔", "", "KHÔNG", "KB3"],
            ["KB6 Xếp thứ tự theo ZPD", "", "✔", "", "✔", "CÓ", "KB1 · KB7"],
            ["KB7 Thử nghiệm tại lớp", "✔", "✔", "✔", "✔", "CÓ", "KB1 · KB3"],
            ["KB8 Đối chiếu chẩn đoán", "", "✔", "", "", "CÓ", "KB7"],
        ],
        ten="Bảng 3.31: Ma trận kịch bản × nhóm độ đo", co_chu=9,
    )

    doan(d,
        "Thứ tự triển khai đề xuất gồm ba đợt. Đợt một chạy KB1, KB3 và KB5 — "
        "cả ba không cần người học thật, cho kết quả nhanh, và kết quả của chúng "
        "là điều kiện để đợt sau có nghĩa. Đợt hai chạy KB7 tại lớp học, với KB6 "
        "và KB4 lồng bên trong dưới dạng phân bổ ngẫu nhiên. Đợt ba chạy KB2 và "
        "KB8 trên dữ liệu mà KB7 tích luỹ được.")

    # ── 3.7.4 ──────────────────────────────────────────────────────────────
    d.add_heading("3.7.4. Các đe doạ tính hiệu lực và biện pháp giảm thiểu", level=2)
    bang(d,
        ["Loại", "Đe doạ", "Biện pháp giảm thiểu"],
        [
            ["Hiệu lực nội tại", "Dữ liệu trước 23-08-2026 không đầy đủ và có "
             "bản ghi sai chủ",
             "Chỉ dùng dữ liệu sau mốc; công bố đợt làm sạch; chạy bốn bất biến "
             "trước và sau mỗi đợt thu"],

            ["", "Hiệu ứng mới lạ ở tuần đầu",
             "Phân tích riêng tuần 1–2 và tuần 5–8; thời lượng thử nghiệm tối "
             "thiểu tám tuần"],

            ["", "Lưới đỡ “thử hai lần” át hiệu ứng của tầng thích ứng",
             "Phân tích riêng nhóm người học chưa bao giờ dùng tới lưới đỡ"],

            ["Hiệu lực cấu trúc", "Mức phủ vốn không phải phép đo năng lực theo "
             "chuẩn CEFR",
             "Phát biểu rõ đây là quy ước bắc cầu hai nhịp; kiểm chứng hiệu lực "
             "hội tụ bằng bài kiểm tra giấy độc lập ở KB7"],

            ["", "Điểm phát âm phụ thuộc thiết bị và môi trường",
             "Ghi lại loại thiết bị; gắn nhãn riêng ba dạng lượt nói; tách khỏi "
             "mọi phép đo tổng hợp"],

            ["", "Số lần bỏ dở là CẬN DƯỚI, không phải phép đếm đầy đủ",
             "Nêu giới hạn khi báo cáo; dùng làm chỉ báo xu hướng, không dùng "
             "làm con số tuyệt đối"],

            ["Hiệu lực kết luận", "Cỡ mẫu nhỏ ở giai đoạn đầu",
             "Báo khoảng tin cậy chứ không chỉ giá trị điểm; nêu số người học "
             "đóng góp vào mỗi con số; đặt cỡ mẫu tối thiểu cho từng độ đo"],

            ["", "Các lượt của cùng một người học không độc lập",
             "Dùng mô hình hồi quy đa mức; chia tập theo NGƯỜI HỌC khi kiểm chéo"],

            ["", "So sánh nhiều lần làm tăng xác suất dương tính giả",
             "Khai báo trước các giả thuyết chính; hiệu chỉnh mức ý nghĩa cho "
             "các so sánh phụ"],

            ["Hiệu lực ngoại tại", "Chỉ thử trên một bộ học liệu, một môn, một "
             "nhóm trường",
             "Nêu rõ phạm vi khái quát hoá; thiết kế hệ thống tách miền tri thức "
             "khỏi tầng thuật toán để việc nhân rộng sang môn khác kiểm chứng được"],

            ["", "Kết quả gắn với một phiên bản mô hình ngôn ngữ cụ thể",
             "Ghi vân tay lời nhắc kèm tên mô hình và tham số sinh cho mọi lượt; "
             "báo cáo nêu rõ phiên bản và thời điểm đo"],
        ],
        ten="Bảng 3.32: Đe doạ tính hiệu lực và biện pháp giảm thiểu",
    )


# ═══════════════════════════════════════════════════════════════════════════
# 3.8 · KẾT LUẬN CHƯƠNG
# ═══════════════════════════════════════════════════════════════════════════
def _m38(d):
    d.add_heading("3.8. Kết luận chương", level=1)
    doan(d,
        "Chương này đã chuyển các cơ sở lý thuyết của Chương 2 thành một thiết "
        "kế cụ thể cho bài toán dạy tiếng Anh ở bậc tiểu học, gồm bốn nhóm kết "
        "quả.")

    doan(d,
        "Thứ nhất, về BIỂU DIỄN BÀI TOÁN (mục 3.2): xác định ba miền thực thể "
        "với ranh giới rõ ràng; đặc tả đồ thị tri thức dưới dạng đồ thị có nhãn "
        "trên cả đỉnh lẫn cạnh, kèm lý do vì sao nhãn cạnh là điều kiện đúng đắn "
        "chứ không phải chi tiết kỹ thuật; đặc tả đầy đủ lược đồ của sáu thực "
        "thể miền người học kèm ánh xạ sang ký hiệu toán học; và nêu bốn bất "
        "biến mà một kho lưu vết học tập phải giữ, mỗi bất biến kèm một phép "
        "kiểm chạy được.")

    doan(d,
        "Thứ hai, về NHẬN BIẾT HÀNH VI (mục 3.3): phân loại bảy hành vi cần nhận "
        "biết và nêu rõ chỉ một trong bảy là quan sát trực tiếp; trình bày bốn "
        "thuật toán với đầu vào, đầu ra và thủ tục đầy đủ; và với mỗi thuật "
        "toán, nêu điều kiện cỡ mẫu tối thiểu cùng giới hạn đã biết. Điểm cần "
        "nhấn của mục này là nguyên tắc “chưa đủ mẫu thì trả về CHƯA BIẾT, không "
        "trả về KÉM” — nguyên tắc ấy chặn một vòng lặp tự củng cố mà nếu không "
        "chặn sẽ làm hệ thống ngày càng tự tin vào một kết luận sai.")

    doan(d,
        "Thứ ba, về CHẨN ĐOÁN VÀ SINH BÀI (mục 3.4 và 3.5): trình bày mười thuật "
        "toán từ cập nhật mô hình có cơ chế quên, lan truyền chẩn đoán hai "
        "chiều, hàm chính sách, tới kiến trúc tạo sinh tăng cường truy xuất bốn "
        "bước. Hai đóng góp thiết kế đáng nêu riêng. Một là RANH GIỚI QUYỀN "
        "QUYẾT ĐỊNH: hàm chính sách khuyến nghị việc nên làm, nhưng quyền mở "
        "đường học thuộc về một bộ luật riêng với lưới đỡ “đã đạt hoặc đã thử "
        "thật hai lần” — vì mô hình có thể chấm sai, và một đứa trẻ bị chấm nhầm "
        "không được phép kẹt vĩnh viễn. Hai là BẢO ĐẢM HAI TẦNG cho ràng buộc "
        "vốn từ: lời nhắc định hướng, còn hậu kiểm tất định mới là thứ cho ra "
        "một phát biểu kiểm chứng được.")

    doan(d,
        "Thứ tư, về ĐỘ ĐO VÀ THỰC NGHIỆM (mục 3.6 và 3.7): xây dựng hệ thống độ "
        "đo bốn nhóm trả lời bốn câu hỏi độc lập, và đề xuất tám kịch bản thực "
        "nghiệm sắp theo chi phí tăng dần, mỗi kịch bản có mục tiêu, giả thuyết, "
        "thiết kế, dữ liệu, độ đo, phép kiểm định thống kê và rủi ro. Nhóm độ đo "
        "thứ tư — độ đo hệ thống và vận hành — thường bị bỏ qua trong tài liệu "
        "về học thích ứng, nhưng ở đây nó được đặt ngang hàng ba nhóm kia, vì "
        "mọi kết luận của ba nhóm kia đều đứng trên giả định “nhật ký đầy đủ và "
        "đúng chủ”, và giả định ấy có thể sai trong im lặng.")

    doan(d,
        "Một nhận xét chung khép lại chương. Phần lớn các quyết định thiết kế "
        "trình bày ở đây không đến từ suy luận thuần tuý mà đến từ việc ĐO TRƯỚC "
        "KHI LÀM, và trong vài trường hợp số đo đã lật ngược thiết kế ban đầu. "
        "Kế hoạch ban đầu cho bộ truy xuất là thay hẳn cửa sổ tuần tự bằng phép "
        "duyệt đồ thị; số đo trên toàn bộ 94 bài cho thấy thay hẳn sẽ làm 87 bài "
        "có vốn từ hẹp đi để đổi lấy 40 bài đúng hơn, nên thiết kế cuối là hợp "
        "nhất hai nguồn. Tương tự, một phép đếm ở tầng dữ liệu từng báo “50 chỗ "
        "thủng” trong khi soi ngược từ hậu quả chỉ có 2 bài mỏng thật. Bài học "
        "phương pháp rút ra được — và cũng là điều các kịch bản thực nghiệm ở "
        "mục 3.7 được thiết kế để tôn trọng — là: đếm ở tầng dữ liệu cho ra "
        "những con số dễ tin mà sai; phải soi ngược từ HẬU QUẢ.")
