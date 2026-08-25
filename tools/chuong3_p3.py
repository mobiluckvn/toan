#!/usr/bin/env python3
"""CHƯƠNG 3 — phần 3: mục 3.5 (sinh bài tập, kiểm tra) và 3.6 (độ đo)."""
from __future__ import annotations

from chuong3_khung import (
    bang, canh_bao, cham, cong_thuc, do, doan, hinh_chu, ma_lenh, thuat_toan,
)


def viet(d):
    _m35(d)
    _m36(d)


# ═══════════════════════════════════════════════════════════════════════════
# 3.5 · SINH BÀI TẬP VÀ KIỂM TRA
# ═══════════════════════════════════════════════════════════════════════════
def _m35(d):
    d.add_heading("3.5. Phương pháp sinh bài tập và kiểm tra", level=1)

    # ── 3.5.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.1. Hai chế độ sinh và tiêu chí phân định", level=2)
    doan(d,
        "Tài liệu về học thích ứng thế hệ thứ ba thường mô tả một bước chuyển "
        "dứt khoát: từ LỰA CHỌN bài tập có sẵn sang TẠO SINH nội dung mới theo "
        "thời gian thực. Hệ thống này chọn một vị trí lai trên trục ấy, và việc "
        "chọn vị trí lai là một quyết định thiết kế có căn cứ chứ không phải một "
        "phần chưa làm kịp.")

    bang(d,
        ["", "Sinh TRƯỚC (ngoại tuyến)", "Sinh LÚC CHẠY (RAG)"],
        [
            ["Quy mô", "4 226 câu của phần học chính", "Bài phụ đạo 4 câu · phòng "
             "luyện nói · lời chấm bài viết"],
            ["Ai sinh", "Bộ sinh tất định viết bằng Python", "Mô hình ngôn ngữ lớn"],
            ["Kiểm duyệt", "TRƯỚC khi tới tay người học — 92 phép kiểm tự động, "
             "cộng soát tay theo đợt",
             "SAU khi sinh — hậu kiểm tất định tại máy người học"],
            ["Cá nhân hoá", "Theo bậc độ khó và theo thứ tự (xếp lại theo ZPD)",
             "Theo nút gốc rễ, sở thích, tên riêng và vốn từ đã học"],
            ["Chi phí mỗi lượt", "Bằng 0 — tệp tĩnh", "Một lời gọi dịch vụ ngoài"],
            ["Chạy được khi mất mạng", "CÓ", "KHÔNG — nên phải có đường lùi"],
            ["Rủi ro chính", "Nội dung cứng, lặp lại giữa các người học",
             "Ảo giác từ vựng, câu sai ngữ pháp, lặp câu"],
        ],
        ten="Bảng 3.22: So sánh hai chế độ sinh",
    )

    doan(d,
        "Tiêu chí phân định được phát biểu như sau: một nội dung được phép sinh "
        "lúc chạy khi và chỉ khi (a) nội dung tĩnh không phục vụ được nhu cầu "
        "ấy, VÀ (b) tồn tại một phép hậu kiểm tất định có thể bác bỏ kết quả "
        "sai, VÀ (c) có đường lùi khi lời gọi hỏng. Ba chỗ hệ thống gọi mô hình "
        "ngôn ngữ đều thoả cả ba điều kiện:")

    bang(d,
        ["Chỗ gọi", "(a) Vì sao tĩnh không đủ", "(b) Hậu kiểm", "(c) Đường lùi"],
        [
            ["Bài phụ đạo", "Nút gốc rễ có thể nằm ở bất kỳ đâu trong 1 194 nút; "
             "không thể soạn sẵn bài vá cho mọi tổ hợp",
             "Đối chiếu từng câu với vốn từ hợp lệ",
             "Lấy câu TĨNH của chính nút gốc rễ TRƯỚC, mô hình chỉ bù phần thiếu"],
            ["Phòng luyện nói", "Đối thoại đòi phản ứng với chính câu người học "
             "vừa nói — không soạn sẵn được",
             "Câu tiếng Anh phải thuộc một trong năm lớp hợp lệ",
             "Câu dựng sẵn từ dữ liệu bài, luôn đúng"],
            ["Chấm bài viết", "Lỗi của người học là mới mỗi lần; lời chấm phải "
             "trỏ đúng câu sai",
             "Soi lời chấm để bắt chữ lạ ngoài vốn từ",
             "Báo lỗi và giữ bài, không chấm bừa"],
        ],
        ten="Bảng 3.23: Ba chỗ được phép sinh lúc chạy",
    )

    canh_bao(d,
        "Lý do của ranh giới này thuộc về đối tượng người dùng (ràng buộc R3). "
        "Với học sinh 6–11 tuổi, một câu hỏi sai hoặc một từ vượt cấp không phải "
        "phiền toái mà là dạy sai, và trẻ sẽ nhớ cái sai ấy. Nội dung tĩnh cho "
        "phép kiểm duyệt TRƯỚC; nội dung sinh lúc chạy chỉ kiểm được SAU. Hệ "
        "thống vì thế đặt nội dung sinh lúc chạy ở đúng những chỗ mà giá trị cá "
        "nhân hoá vượt được rủi ro.")

    # ── 3.5.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.2. Đường ống sinh nội dung tĩnh", level=2)
    doan(d,
        "Nội dung tĩnh được sinh bằng một đường ống mười bốn tầng, chạy ngoại "
        "tuyến. Đường ống là tất định: cùng dữ liệu vào thì cùng dữ liệu ra, "
        "không có yếu tố ngẫu nhiên — đó là điều kiện để các phép kiểm tự động "
        "có nghĩa.")

    hinh_chu(d, [
        "  ① bản đồ tri thức gốc  ─────►  ② phần bù soạn tay",
        "            │                            │",
        "            └──────────┬─────────────────┘",
        "                       ▼",
        "                 ③ BẢN CHUẨN  (một bài = một khối dữ liệu đã chuẩn hoá)",
        "                       │",
        "     ┌─────────┬───────┼────────┬─────────┬─────────┬─────────┐",
        "     ▼         ▼       ▼        ▼         ▼         ▼         ▼",
        "  ④ bài học ⑤ sổ lời ⑥ đề ôn ⑦ kịch bản ⑪ đọc   ⑫ đề bài  ⑭ bài",
        "   4 bậc câu   cần đọc  chương   nói       hiểu     viết     tả tranh",
        "     │         │                                              ",
        "     │         ▼                                              ",
        "     │      ⑧ clip tiếng (Kokoro TTS)                        ",
        "     │         │                                              ",
        "     │         ▼                                              ",
        "     │      ⑨ video giảng ─── ⑬ tách theo NHÓM NGHĨA          ",
        "     ▼                                                        ",
        "  ⑩ hình vẽ (một nguồn cho cả hai bên vẽ)                    ",
    ], ten="Hình 3.3: Đường ống sinh nội dung tĩnh")

    doan(d,
        "Tầng ④ — sinh câu hỏi — là tầng quyết định chất lượng học liệu. Bảy "
        "luật dưới đây ràng buộc bộ sinh; mỗi luật tương ứng với một lỗi đã xảy "
        "ra thật trong quá trình phát triển.")
    cham(d, [
        ("Không dùng từ ngoài vốn của bài và các bài trước — ", "ràng buộc gốc "
         "của cả môn; vi phạm là ảo giác từ vựng ngay ở tầng tĩnh."),
        ("Phương án nhiễu phải cùng trường nghĩa — ", "nhiễu lấy bừa thì câu hỏi "
         "trở thành câu đoán được mà không cần hiểu."),
        ("Không có hai phương án cùng nghĩa — ", "lỗi này từng lọt: một câu có "
         "bốn lựa chọn trong đó hai cặp trùng nghĩa, nên có hai đáp án đúng."),
        ("Câu điền khuyết phải điền được đúng MỘT cách — ", "nếu ô trống nhận "
         "nhiều từ hợp lệ thì đáp án không xác định."),
        ("Không lộ đáp án trong chính đề bài — ", "kể cả qua hình minh hoạ hay "
         "qua phần chữ mờ; đã có lỗi hình lộ đáp án."),
        ("Mỗi câu phải gắn đúng một nút đánh giá — ", "điều kiện để mô hình "
         "không tính công một lượt cho nhiều nút."),
        ("Gợi ý phải đi từ xa tới gần — ", "gợi ý đầu nói về đặc điểm hình thức, "
         "gợi ý sau mới nói về nghĩa; ngược lại thì gợi ý đầu đã là đáp án."),
    ], danh_so=True)

    doan(d,
        "Toàn bộ đường ống được canh bởi 92 tệp kiểm chạy bằng node, không cần "
        "mạng và không cần cơ sở dữ liệu. Các phép kiểm chia làm ba loại: kiểm "
        "TÍNH CHẤT của dữ liệu sinh ra (mọi câu có mã nút, mọi từ nằm trong vốn, "
        "mọi hình có nguồn), kiểm SỰ NHẤT QUÁN giữa hai bản chép của cùng một "
        "luật, và kiểm CHỖ NỐI giữa các tầng.")

    canh_bao(d,
        "Loại thứ ba sinh ra từ một bài học đắt. Có lần toàn bộ đường ghi nhận "
        "dữ liệu học nằm im suốt nhiều tuần vì một hàm không được truyền xuống "
        "thành phần con — mỗi tệp đứng riêng đều đúng, chỗ hỏng nằm ở CHỖ NỐI, "
        "và không phép kiểm nào của hai loại đầu bắt được. Từ đó, mỗi đường dữ "
        "liệu quan trọng đều có một phép kiểm soi chính chỗ nối.")

    # ── 3.5.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.3. Sinh bài phụ đạo: kiến trúc RAG bốn bước", level=2)
    doan(d,
        "Kiến trúc tạo sinh tăng cường truy xuất trình bày ở mục 2.4.3 gồm ba "
        "bước. Hiện thực trong hệ thống này có BỐN bước: bước thứ tư — hậu kiểm "
        "— là bước không được bỏ, và là bước làm nên bảo đảm về vốn từ.")

    thuat_toan(d, "3.10", "Dựng một bài phụ đạo",
        "đồ thị G; hồ sơ mức thạo M; nút người học đang mắc v_mắc; các bài đã "
        "tải sẵn B (bài hiện tại và các bài tiên quyết); vốn từ hợp lệ W; hàm "
        "gọi mô hình (không bắt buộc); hàm hậu kiểm; số câu cần n = 4.",
        "một bài phụ đạo gồm nút gốc rễ, danh sách câu, nguồn của câu (tĩnh · "
        "mô hình · trộn), và cờ đã phải lùi.",
        [
            "1  // BƯỚC 1 — TRUY XUẤT: định vị đích và lấy vốn hợp lệ",
            "2  g ← ĐỊNH_VỊ_GỐC_RỄ(G, M, v_mắc, m = 1)     // Thuật toán 3.6",
            "3  if g không tồn tại: g ← v_mắc              // nút không có tiên quyết",
            "4  ",
            "5  // BƯỚC 2 — TĨNH TRƯỚC: gom câu có sẵn quanh nút gốc rễ",
            "6  T ← ∅",
            "7  for bậc in [khởi_động, ráp_câu, thử_thách]:   // ⚠ BẬC THẤP TRƯỚC",
            "8      for b ∈ B, for c ∈ b.kho[bậc]:",
            "9          if g ∉ ({c.maNut} ∪ c.maNutDs): continue",
            "10         if c.id ∈ mã(T): continue",
            "11         T ← T + [c];  if |T| ≥ n: break",
            "12 T ← [ c ∈ T : HẬU_KIỂM(c) ]                 // ⚠ soi CẢ câu tĩnh",
            "13 if |T| ≥ n hoặc không có hàm gọi mô hình:",
            "14     return (g, T[0..n-1], nguồn = 'tĩnh', lùi = false)",
            "15 ",
            "16 // BƯỚC 3 — TĂNG CƯỜNG VÀ SINH: chỉ bù phần còn thiếu",
            "17 lùi ← false",
            "18 try:",
            "19     S ← GỌI_MÔ_HÌNH(nút = g, vốn = W, số_câu = n − |T|)",
            "20 except:",
            "21     S ← ∅;  lùi ← true                      // ⚠ KHÔNG ném ra ngoài",
            "22 if S = ∅: lùi ← true",
            "23 ",
            "24 // BƯỚC 4 — HẬU KIỂM: hàng rào duy nhất còn lại",
            "25 S′ ← [ c ∈ S : c hợp khuôn ∧ HẬU_KIỂM(c) ]",
            "26 if |S′| < |S|: lùi ← true                   // có câu bị bác",
            "27 C ← (T + S′)[0 .. n−1]",
            "28 return (g, C, nguồn = 'trộn' nếu T ≠ ∅ ngược lại 'llm', lùi)",
        ],
        ghi_chu=[
            "Thứ tự ở bước 2 NGƯỢC với trực giác, và cố ý. Trực giác nói “gọi mô "
            "hình để có bài cá nhân hoá nhất”. Nhưng người học lúc ấy đang học "
            "dở, vừa sai ba câu liền, và màn hình vừa hứa sẽ giúp. Nếu lời gọi "
            "mạng hỏng mà người học nhận được màn trắng thì đó là hỏng NẶNG HƠN "
            "không có phụ đạo: vừa mất mạch học, vừa mất niềm tin vào cái nút "
            "vừa bấm. Lấy câu tĩnh trước thì hỏng cách nào cũng còn bài để học.",

            "Dòng 7 — ưu tiên bậc thấp. Người học đang mắc thì đừng đưa câu khó "
            "nhất của nút ấy; mục đích là gỡ, và gỡ thì bắt đầu từ chỗ làm được.",

            "Dòng 12 — hậu kiểm chạy cả trên câu TĨNH, dù câu tĩnh đã qua 92 "
            "phép kiểm lúc dựng. Lý do: hàm hậu kiểm ràng buộc theo vốn từ của "
            "PHIÊN HIỆN TẠI, hẹp hơn vốn từ lúc dựng — một câu hợp lệ trong bài "
            "gốc có thể chứa từ mà người học này chưa học tới.",

            "Dòng 25 — đây là hàng rào DUY NHẤT còn lại cho câu do mô hình sinh. "
            "Bỏ nó đi để “cho nhanh” là mở đúng cái cửa mà cả tầng chống ảo giác "
            "từ vựng sinh ra để đóng.",

            "Dòng 26 — cờ lùi được bật cả khi mô hình trả về câu nhưng bị hậu "
            "kiểm bác. Cờ này đi vào nhật ký và là đầu vào của độ đo “tỉ lệ phải "
            "lùi” ở mục 3.6.4.",
        ])

    # ── 3.5.4 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.4. Bộ truy xuất vốn từ hợp lệ", level=2)
    doan(d,
        "Bộ truy xuất trả lời câu hỏi: với người học này, ở bài này, mô hình "
        "được phép dùng những từ nào và những mẫu câu nào. Đây là thành phần "
        "quyết định của tầng chống ảo giác từ vựng, vì mọi ràng buộc phía sau "
        "đều đối chiếu với kết quả của nó.")

    thuat_toan(d, "3.11", "Truy xuất vốn từ hợp lệ cho một buổi học",
        "bài hiện tại b; danh sách bài đứng trước theo thứ tự học B_trước; đồ "
        "thị G; hồ sơ tiến độ (đã đạt bài nào); số bài cũ tối đa được trộn "
        "u = 3.",
        "vốn lõi (của bài hiện tại) và vốn ôn (các bài được trộn thêm), mỗi phần "
        "gồm từ vựng, mẫu câu và câu sẵn của sách.",
        [
            "1  lõi ← VỐN_CỦA_BÀI(b)          // từ · mẫu câu · câu sẵn của sách",
            "2  if người học CHƯA ĐẠT bài b:",
            "3      return (lõi, ôn = ∅)      // chưa đạt thì không mở rộng",
            "4  ",
            "5  // NGUỒN 1 — cửa sổ tuần tự: “vừa học gì”",
            "6  gần ← u bài CUỐI trong { x ∈ B_trước : đã đạt x }",
            "7  ",
            "8  // NGUỒN 2 — đồ thị: “bài này dựng trên gì”",
            "9  TQ ← ∅",
            "10 for v ∈ nút_của(b):",
            "11     for (w, k) ∈ DUYỆT_NGƯỢC(G, v, độ_sâu = 2):",
            "12         x ← BÀI_DẠY_NÚT(w)",
            "13         if x tồn tại ∧ x ≠ b ∧ đã đạt x: TQ ← TQ ∪ {x}",
            "14 ",
            "15 ôn ← [ VỐN_CỦA_BÀI(x) : x ∈ gần ∪ (TQ \\ gần) ]   // GỘP, không thay",
            "16 return (lõi, ôn)",
        ],
        ghi_chu=[
            "Dòng 15 — việc HỢP NHẤT hai nguồn thay vì thay thế là kết quả của "
            "một phép đo, không phải một lựa chọn thẩm mỹ. Đo trên toàn bộ 94 "
            "bài: cửa sổ tuần tự BỎ SÓT tiên quyết ở 40 bài, trong đó 2 bài có "
            "tiên quyết nằm ở QUYỂN KHÁC mà cửa sổ không bao giờ với tới được, "
            "dù nới rộng bao nhiêu — vì nó nới trong cùng quyển. Nhưng nếu THAY "
            "hẳn bằng đồ thị thì 87/94 bài có vốn từ HẸP ĐI và nhiều bài về "
            "rỗng, vì trong 1 194 nút chỉ 150 nút có cạnh tiên quyết đi vào. "
            "Thay hẳn là đánh đổi 87 bài lấy 40 bài.",

            "Dòng 2–3 và dòng 13 — CẢ HAI nguồn đều lọc qua điều kiện ĐÃ ĐẠT. "
            "Bài chưa đạt thì vốn từ của nó không được vào, kể cả khi đồ thị bảo "
            "bài hiện tại cần nó. Bỏ chốt ấy là để mô hình nói bằng từ người học "
            "chưa từng học, tức tự tay chọc thủng tầng chống ảo giác.",
        ])

    doan(d,
        "Ngoài vốn từ của bài, mô hình được phép dùng thêm một danh sách CỐ ĐỊNH "
        "gồm 14 câu nghi thức lớp học — “Hello!”, “Your turn.”, “Good job!”, "
        "“Try again.” và tương tự. Khe hở này được mở sau một quan sát thực tế: "
        "ở một bài chỉ có ĐÚNG MỘT mẫu câu, mô hình bị bó tới mức khi người học "
        "chào thì nó đáp lại bằng chính mẫu câu của bài, cho ra một cuộc đối "
        "thoại vô nghĩa. Các câu nghi thức không phải từ người học phải học "
        "thuộc — chúng là lời của giáo viên, trẻ nghe mãi rồi hiểu qua ngữ cảnh, "
        "đúng như trong lớp thật. Danh sách được khai tường minh và được đếm bởi "
        "một phép kiểm, vì nới nó ra là quay lại đúng chỗ hỏng mà việc bó vốn từ "
        "sinh ra để tránh.")

    # ── 3.5.5 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.5. Hậu kiểm câu do mô hình sinh", level=2)
    doan(d,
        "Hậu kiểm là hàm quyết định: cho một câu tiếng Anh do mô hình sinh, câu "
        "ấy có được phép đưa cho người học không. Hàm là tất định, chạy tại máy "
        "người học, không gọi mạng.")

    thuat_toan(d, "3.12", "Hậu kiểm một câu tiếng Anh",
        "câu cần soi s; vốn từ hợp lệ W (từ, mẫu câu, câu sẵn của sách); tên "
        "riêng của người học; câu của lượt TRƯỚC.",
        "hợp lệ hay không hợp lệ.",
        [
            "1  c ← CHUẨN_HOÁ(s)      // thường hoá, bỏ dấu câu, gộp khoảng trắng",
            "2  if c rỗng: return false",
            "3  if c = CHUẨN_HOÁ(câu_trước): return false     // ⚠ CHỐNG LẶP",
            "4  ",
            "5  // Năm đường công nhận",
            "6  if ∃ t ∈ W.từ : CHUẨN_HOÁ(t) = c: return true        // một từ rời",
            "7  if c ∈ CHUẨN_HOÁ(14 câu nghi thức lớp học): return true",
            "8  if ∃ m ∈ W.mẫu_câu : c ∈ NỬA_CỦA(m): return true     // cả cặp / nửa",
            "9  if ∃ x ∈ W.câu_sách : CHUẨN_HOÁ(x) = c: return true",
            "10 for m ∈ W.mẫu_câu có công thức:",
            "11     for khung ∈ { m.công_thức } ∪ TÁCH_ĐÔI(m.công_thức):",
            "12         loại ← LOẠI_Ô_TRỐNG(khung)",
            "13         nếu loại = 'tên': D ← { tên riêng, 'Bill', 'Mai' }",
            "14         ngược lại:        D ← ⋃_{t ∈ W.từ} { t.gốc, t.số_nhiều,",
            "15                                 t.số_ít, t.dạng_ing, t.dạng_qk }",
            "16         for d ∈ D:",
            "17             if CHUẨN_HOÁ(ĐIỀN(khung, d)) = c: return true",
            "18 return false",
        ],
        ghi_chu=[
            "Dòng 3 — chống lặp là một điều kiện riêng, không suy ra được từ "
            "tính hợp lệ về ngôn ngữ. Đã quan sát thấy hai lượt liền cùng cho ra "
            "một câu đúng ngữ pháp; với người học thì đó là một cuộc đối thoại "
            "hỏng, dù từng câu đều đúng.",

            "Dòng 8 — phải nhận cả CẶP hỏi–đáp lẫn TỪNG NỬA của cặp. Phòng luyện "
            "nói dạy theo lối đối đáp: giáo viên hỏi nửa trước, người học đáp "
            "nửa sau. Bản đầu chỉ điền vào cả cặp nên mọi câu đáp lẻ đều bị bác "
            "oan, kể cả câu đúng khuôn sách.",

            "Dòng 14–15 — ô có kiểu thì DẠNG BIẾN ĐỔI cũng điền được. Đây không "
            "phải nới rào: các dạng biến đổi lấy từ CHÍNH mục từ vựng người học "
            "đã học, không phải chữ mới. Từ nào bài không dạy thì vẫn không có "
            "đường vào.",

            "Cách tiếp cận là DỰNG HẾT rồi so, không đoán bằng biểu thức chính "
            "quy. Số cách điền rất nhỏ (số mẫu câu nhân số từ), nên dựng hết vừa "
            "rẻ vừa không có chỗ cho một biểu thức chính quy viết sai lọt qua.",
        ])

    doan(d,
        "Khi hậu kiểm bác một câu, hệ thống KHÔNG báo lỗi cho người học mà thay "
        "bằng một câu dựng sẵn từ chính dữ liệu bài — luôn đúng, vì nó ghép từ "
        "dữ liệu chứ không sinh ra từ đâu cả. Hàm dựng câu thay thế xếp sẵn vài "
        "phương án rồi lấy phương án đầu tiên KHÁC câu lượt trước; bản đầu chỉ "
        "dựng đúng một câu, và nếu chính nó trùng câu trước thì luật chống lặp "
        "trở thành vô nghĩa — chặn lặp xong lại thay bằng đúng câu vừa chặn.")

    # ── 3.5.6 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.6. Phòng luyện nói: máy con quyết việc, mô hình lo diễn đạt", level=2)
    doan(d,
        "Phòng luyện nói là chỗ mô hình ngôn ngữ đóng vai gia sư đối thoại. "
        "Thiết kế ở đây đảo ngược phân công thường thấy, và việc đảo ngược xuất "
        "phát từ một quan sát cụ thể.")

    doan(d,
        "Bản đầu giao cho mô hình cả việc chọn nội dung lẫn việc diễn đạt, với "
        "lời nhắc “chỉ được dùng những mẫu câu sau”. Kết quả: ở bài chỉ có một "
        "mẫu câu, sáu lượt liền mô hình nói đúng một câu. Lỗi không nằm ở mô "
        "hình — nó đang tuân lệnh răm rắp — mà nằm ở chỗ giao việc. Thả cho mô "
        "hình “tự nói cho phong phú” cũng không xong: hoặc nó lặp, hoặc nó bịa "
        "ra từ ngoài vốn của người học.")

    doan(d,
        "Thiết kế hiện tại tách hai việc. MÁY CON chọn sẵn từ mục tiêu và kiểu "
        "việc cho từng lượt — bốn kiểu: nói một từ, nói cả câu theo mẫu, thay "
        "một từ khác vào công thức, hoặc khen rồi sang việc mới. MÔ HÌNH chỉ lo "
        "diễn đạt: hiểu người học vừa nói gì và viết một lời tiếng Việt tự "
        "nhiên. Cách này biến “cho phong phú” — thứ không kiểm được — thành một "
        "phép đếm chạy được bằng node và soi được bằng phép kiểm.")

    canh_bao(d,
        "Mỗi lượt mô hình chỉ được nói ĐÚNG MỘT câu tiếng Anh ngắn, kèm một lời "
        "tiếng Việt. Ràng buộc một câu là vì người học sáu tuổi không nhại lại "
        "được hai câu. Ràng buộc tách hai thứ tiếng thành hai trường riêng là vì "
        "bộ đọc phải đọc câu tiếng Anh bằng giọng en-GB và lời tiếng Việt bằng "
        "giọng vi-VN; trộn hai thứ tiếng vào một dòng thì bộ đọc sai giọng.")

    # ── 3.5.7 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.7. Chấm bài viết ngắn", level=2)
    doan(d,
        "Bài viết ngắn là dạng bài duy nhất mà đáp án không đóng. Hệ thống dùng "
        "mô hình ngôn ngữ để chấm, với bốn yêu cầu ràng buộc trong lời nhắc và "
        "một tầng soi lại ở máy người học.")
    cham(d, [
        ("Khen CỤ THỂ — ", "nói rõ người học làm được gì, câu nào đúng, dùng "
         "đúng từ nào; không khen chung chung."),
        ("Mỗi lỗi phải chỉ ra ba phần — ", "câu viết sai, câu sửa lại, và vì "
         "sao; giải thích bằng tiếng Việt thật ngắn."),
        ("Câu sửa và câu gợi ý CHỈ được dùng từ trong bảng vốn từ — ", "và tầng "
         "soi lại ở máy con bắt chữ lạ nếu mô hình vi phạm."),
        ("Một lời riêng cho phụ huynh — ", "tiếng Việt, cho người lớn đọc."),
    ])

    doan(d,
        "Điểm số do máy chấm vẫn được ghi vào học bạ, vì phụ huynh hỏi “con viết "
        "được chưa” thì cần một câu trả lời. Nhưng con số ấy mang NHÃN NGUỒN đi "
        "kèm mọi chỗ ghi, và màn hình nói thẳng “máy chấm” (ràng buộc R6). Một "
        "con số không nhãn là một con số sẽ bị đọc nhầm thành điểm của giáo viên.")

    doan(d,
        "Về quyền riêng tư: máy chủ KHÔNG lưu gì. Bài viết của người học được "
        "chuyển tiếp tới dịch vụ mô hình rồi bỏ; lời chấm trả về máy con và máy "
        "con tự ghi vào học bạ của chính người học ấy. Yêu cầu này thoạt nhìn "
        "chọi với nhu cầu so sánh hiệu quả giữa các mẫu lời nhắc (mục 3.6.3), "
        "nhưng chúng chỉ chọi nếu ta tưởng phải lưu cả lời nhắc. Để so hai mẫu "
        "thì chỉ cần biết hai lượt có dùng CÙNG mẫu hay không — điều đó một mã "
        "băm nói được, còn nội dung thì không cần.")

    thuat_toan(d, "3.13", "Vân tay lời nhắc",
        "tên mẫu; phần KHUNG của lời nhắc (chuỗi giống nhau ở mọi lượt cùng "
        "mẫu); các tham số cũng thuộc khung (tên mô hình, nhiệt độ, giới hạn "
        "token).",
        "ba trường: tên mẫu, số phiên bản mẫu, mã băm 12 ký tự của khung.",
        [
            "1  khung ← DỰNG_LỜI_NHẮC(dữ_liệu_riêng = rỗng)   // ⚠ gọi lại chính hàm",
            "2  phần ← [ 'mau='   + tên_mẫu,",
            "3           'v='     + PHIÊN_BẢN[tên_mẫu],",
            "4           các tham số khung, sắp theo khoá,",
            "5           'khung=' + khung ]",
            "6  return ( tên_mẫu, PHIÊN_BẢN[tên_mẫu], SHA256(nối(phần))[0..11] )",
        ],
        ghi_chu=[
            "Dòng 1 — khung được dựng bằng CHÍNH hàm dựng lời nhắc, với phần dữ "
            "liệu riêng để rỗng. Cách này không sót không thừa, và sửa lời nhắc "
            "thì khung tự đổi theo — không có bảng nào phải nhớ cập nhật. Lối "
            "lọc theo dấu hiệu (bỏ những dòng chứa tên người học, vốn từ…) chỉ "
            "là lưới đỡ cho trường hợp không sở hữu hàm dựng.",

            "Băm KHUNG chứ không băm cả lời nhắc. Băm cả lời nhắc thì mỗi lượt "
            "ra một vân tay riêng — vừa vô dụng cho việc so mẫu, vừa thành một "
            "mã theo dõi được từng lượt của từng người học. Băm khung thì hai "
            "người học khác nhau cùng học một bài cho ra CÙNG một vân tay: đó "
            "vừa là điều làm phép so có nghĩa, vừa là điều làm nó không lần ra "
            "được ai.",

            "Số phiên bản do người sửa khai TAY, còn mã băm sinh tự động. Hai "
            "đại lượng phục vụ hai việc: số phiên bản nói ra chủ ý “đây là lần "
            "đổi đáng kể” nên dùng để GOM dữ liệu khi so; mã băm đổi cả khi sửa "
            "một lỗi chính tả nên dùng để PHÁT HIỆN lệch ngoài ý muốn — ai đó "
            "sửa lời nhắc mà quên tăng số.",
        ])

    # ── 3.5.8 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.8. Kiểm tra và đánh giá người học", level=2)
    doan(d,
        "Hệ thống kiểm tra người học ở bốn cấp, mỗi cấp có một luật đạt riêng và "
        "một hệ quả riêng.")

    bang(d,
        ["Cấp", "Hình thức", "Luật đạt", "Hệ quả khi đạt", "Hệ quả khi chưa đạt"],
        [
            ["Câu", "Một câu hỏi trong chặng luyện tập",
             "Trả lời đúng",
             "Cập nhật mô hình; sang câu sau",
             "Sai lần 1 → thử lại; lần 2 → hiện gợi ý; lần 3 → hiện đáp án và "
             "cho để lại sau, câu ấy bị ĐẾM để cuối mức mời làm lại"],

            ["Bài", "Chặng sát hạch cuối bài",
             "Theo luật đạt khai trong chính bài",
             "Ghi đạt; sinh thẻ ôn theo lịch ngắt quãng",
             "Ghi “đã làm mà chưa đạt”; vẫn đi tiếp được nếu đã thử ≥ 2 lần, "
             "nhưng nằm trong danh sách còn nợ"],

            ["Chương", "Kỳ ôn tập chương",
             "MỌI bài của chương đều đã ĐẠT — không có cửa “thử hai lần”",
             "Ghi huy hiệu vào học bạ",
             "Hiện còn thiếu mấy bài nữa thì mở được"],

            ["Ôn ngắt quãng", "Thẻ ôn đến hạn, 3 câu mỗi thẻ",
             "ĐÚNG HẾT mới tính là qua",
             "Thẻ lên một hộp Leitner, giãn khoảng cách",
             "Thẻ VỀ HỘP 0 — gặp lại ngày mai"],
        ],
        ten="Bảng 3.24: Bốn cấp kiểm tra",
    )

    canh_bao(d,
        "Ba nấc ở cấp CÂU là cố ý. Nếu mở nút bỏ qua ngay ở nấc thứ hai thì gợi "
        "ý và đáp án hiện CÙNG LÚC — không ai đọc gợi ý khi đáp án nằm ngay bên "
        "cạnh, và nấc gợi ý coi như không tồn tại. Phải để người học có đúng một "
        "lượt được thử VỚI gợi ý trong tay.")

    canh_bao(d,
        "Luật “đúng hết mới qua” ở cấp ôn ngắt quãng nghiêm hơn ở cấp bài, và đó "
        "là chủ ý: cả giá trị của lặp lại ngắt quãng nằm ở chỗ thẻ nào chưa chắc "
        "thì quay lại SỚM. Cho qua khi mới đúng 2/3 là giãn khoảng cách cho một "
        "thứ người học chưa vững, tức làm hỏng đúng cơ chế vừa dựng.")

    doan(d,
        "Câu hỏi cho một lượt ôn được lấy từ CHÍNH bài của thẻ ấy, không sinh "
        "mới và không soạn thêm — ôn tập mà hỏi câu chưa từng gặp thì đó là bài "
        "mới đội lốt. Thẻ loại “thẻ từ vựng” lấy câu bậc khởi động; thẻ loại "
        "“thẻ câu” lấy câu bậc ráp câu và thử thách, vì các mốc +3 và +7 ngày là "
        "lúc kiểm xem người học còn DÙNG được chứ không chỉ còn NHỚ. Hai lượt ôn "
        "cùng một bài xoay vòng điểm bắt đầu theo số lần đã ôn, nên không ra y "
        "hệt một bộ câu; xoay theo biến đếm chứ không theo số ngẫu nhiên, để "
        "phép kiểm còn kiểm được.")

    # ── 3.5.9 ──────────────────────────────────────────────────────────────
    d.add_heading("3.5.9. Công nghệ sử dụng", level=2)
    bang(d,
        ["Tầng", "Công nghệ", "Phiên bản / cấu hình", "Vai trò trong hệ thống"],
        [
            ["Giao diện", "React", "18.3", "Màn học, phòng luyện nói, góc bố mẹ"],
            ["", "Vite", "5.3", "Dựng gói; đóng dấu phiên bản vào tên tệp"],
            ["Lưu trữ", "Cloud Firestore", "Luật bảo mật khai theo trường",
             "Nhật ký, mô hình người học, tiến độ, thẻ ôn"],
            ["", "Firebase Authentication", "Đăng nhập bằng mã một lần",
             "Định danh người học"],
            ["", "Firebase Hosting", "—", "Phân phối ứng dụng và học liệu tĩnh"],
            ["Tính toán nền", "Cloud Functions for Firebase", "Node.js 22",
             "Cập nhật mô hình, dựng sổ, sinh thẻ ôn, trung chuyển lời gọi mô hình"],
            ["Trí tuệ nhân tạo", "openai/gpt-oss-120b qua Groq",
             "nhiệt độ 0,2 khi chấm · 0,4 khi đối thoại; mức suy luận thấp; trả "
             "về JSON",
             "Sinh bài phụ đạo, đối thoại luyện nói, chấm bài viết"],
            ["", "Web Speech API của trình duyệt", "en-GB",
             "Nhận dạng phát âm — xem giới hạn ở mục 3.6.5"],
            ["Dựng học liệu", "Python 3", "—",
             "Mười bốn tầng của đường ống sinh nội dung tĩnh"],
            ["", "Kokoro TTS", "Hai mô hình giọng", "Sinh clip tiếng"],
            ["", "Pillow + ffmpeg", "—", "Sinh hình và ghép video giảng"],
            ["Kiểm chứng", "node:test", "92 tệp, chạy không cần mạng",
             "Canh tính chất dữ liệu, tính nhất quán, và các chỗ nối"],
            ["", "Bộ giả lập Firebase", "33 phép trên luật bảo mật",
             "Chứng minh luật cho phép và luật từ chối đúng như thiết kế"],
        ],
        ten="Bảng 3.25: Công nghệ sử dụng theo tầng",
    )

    canh_bao(d,
        "Việc mô hình ngôn ngữ chạy qua một dịch vụ ngoài có một hệ quả về "
        "phương pháp: không có gì bảo đảm trọng số mô hình không đổi giữa hai "
        "lần đo. Đó chính là lý do mỗi lượt phải mang vân tay lời nhắc kèm tên "
        "mô hình và các tham số sinh — không có vân tay thì một thay đổi phía "
        "nhà cung cấp sẽ trộn vào kết quả thực nghiệm mà không ai truy ra được.")


# ═══════════════════════════════════════════════════════════════════════════
# 3.6 · HỆ THỐNG ĐỘ ĐO
# ═══════════════════════════════════════════════════════════════════════════
def _m36(d):
    d.add_heading("3.6. Hệ thống độ đo đánh giá", level=1)

    # ── 3.6.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.6.1. Bốn nhóm độ đo", level=2)
    doan(d,
        "Một hệ thống học thích ứng dùng trí tuệ nhân tạo tạo sinh cần trả lời "
        "bốn câu hỏi độc lập, và mỗi câu hỏi đòi một nhóm độ đo riêng. Trộn "
        "chúng vào một chỉ số tổng hợp là che mất chính chỗ cần nhìn.")

    bang(d,
        ["Nhóm", "Câu hỏi cần trả lời", "Độ đo chính", "Đo bằng cách nào"],
        [
            ["A · MÔ HÌNH", "Mô hình dự đoán người học có đúng không?",
             "AUC · RMSE · độ chính xác · sai lệch hiệu chuẩn",
             "Chạy lại nhật ký, dự đoán lượt kế tiếp"],
            ["B · SƯ PHẠM", "Người học có tiến bộ không, và can thiệp có giúp không?",
             "Đường cong học tập · ΔC · số lượt tới thạo · mức phủ vốn",
             "Phân tích nhật ký và hồ sơ nút"],
            ["C · AN TOÀN NỘI DUNG", "Tầng chống ảo giác từ vựng chặn được bao nhiêu?",
             "Tỉ lệ từ ngoài vốn · tỉ lệ bị hậu kiểm bác · tỉ lệ phải lùi",
             "Bộ kiểm sinh nội dung, đối chiếu tự động"],
            ["D · HỆ THỐNG", "Hệ thống có chạy đúng và kịp không?",
             "Độ trễ · tỉ lệ ghi thành công · số bản ghi kẹt · bốn bất biến",
             "Đo trên bản chạy thật và soi kho dữ liệu"],
        ],
        ten="Bảng 3.26: Bốn nhóm độ đo",
    )

    # ── 3.6.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.6.2. Nhóm A — độ đo mô hình người học", level=2)
    doan(d,
        "Bài toán đánh giá được đặt ở dạng dự đoán: tại mỗi lượt thứ n của một "
        "người học tại một nút, dùng trạng thái mô hình SAU lượt n−1 để dự đoán "
        "xác suất trả lời đúng ở lượt n, rồi đối chiếu với kết quả thật. Xác "
        "suất dự đoán:")
    cong_thuc(d,
        "P(đúng ở lượt n) = P(Lₙ₋₁)·(1 − P(S)) + (1 − P(Lₙ₋₁))·P(G)")

    bang(d,
        ["Độ đo", "Công thức / định nghĩa", "Đọc con số thế nào"],
        [
            ["AUC", "Diện tích dưới đường ROC của bài toán phân loại nhị phân",
             "0,50 là đoán mò. Tài liệu về BKT thường báo 0,65–0,75 trên dữ liệu "
             "thật; dưới 0,60 là mô hình gần như không mang thông tin"],
            ["RMSE", "Căn bậc hai trung bình bình phương sai số giữa xác suất dự "
             "đoán và kết quả thật (0 hoặc 1)",
             "Càng nhỏ càng tốt; so sánh giữa các biến thể mô hình mới có nghĩa, "
             "so với một ngưỡng tuyệt đối thì không"],
            ["Độ chính xác", "Tỉ lệ dự đoán đúng khi cắt ngưỡng ở 0,5",
             "Phải báo kèm tỉ lệ lớp đa số; dữ liệu học thường lệch về phía đúng "
             "nên độ chính xác một mình dễ gây ảo tưởng"],
            ["Sai lệch hiệu chuẩn", "Chia các lượt thành 10 nhóm theo xác suất "
             "dự đoán; trong mỗi nhóm so xác suất trung bình với tỉ lệ đúng thật",
             "Đây là độ đo QUAN TRỌNG NHẤT với hệ thống này: ngưỡng θ = 0,85 chỉ "
             "có nghĩa nếu “mô hình nói 85%” thật sự tương ứng với “đúng khoảng "
             "85% số lần”"],
        ],
        ten="Bảng 3.27: Nhóm A — độ đo mô hình",
    )

    canh_bao(d,
        "Phép đánh giá phải TÁCH THEO NGƯỜI HỌC khi chia tập, không tách theo "
        "lượt. Chia theo lượt thì các lượt của cùng một người học nằm ở cả hai "
        "phía, và mô hình được lợi từ chính chuỗi mà nó phải dự đoán.")

    # ── 3.6.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.6.3. Nhóm B — độ đo tiến bộ và hiệu quả can thiệp", level=2)
    doan(d,
        "Đường cong học tập biểu diễn tỉ lệ lỗi theo SỐ LẦN ĐÃ LUYỆN. Đây là "
        "cách trực quan nhất để thấy việc học có đang diễn ra hay không: một con "
        "số “đúng 78%” không nói được điều đó, vì nó trộn lần đầu với lần thứ "
        "mười vào cùng một rổ.")

    canh_bao(d,
        "Cái bẫy của đường cong học tập nằm ở câu hỏi “lần thứ mấy tính từ đâu”. "
        "Nếu sổ chỉ lấy nhật ký bảy ngày gần nhất và đánh số thứ tự trong chừng "
        "ấy, thì lượt thứ 12 của một từ người học đã học từ tháng trước bị ghi "
        "thành “lần thứ 1” — và đường cong dựng trên đó nói dối theo hướng ĐẸP "
        "LÊN: điểm “lần 1” có tỉ lệ lỗi thấp bất thường vì lẫn vào đó toàn những "
        "nút đã thạo từ lâu. Lối thoát không phải kéo dài cửa sổ (tốn, và bao "
        "nhiêu ngày cũng vẫn hụt) mà là dùng chính trường tổng số lượt trong hồ "
        "sơ nút: chỉ những nút có tổng số lượt ĐÚNG BẰNG số lượt đếm được trong "
        "cửa sổ mới được vào đường cong. Đường cong khi ấy nói về “những nút "
        "người học BẮT ĐẦU học trong kỳ” — hẹp hơn, nhưng đúng — và phải báo kèm "
        "số nút đã bị loại.")

    canh_bao(d,
        "Điểm có ít mẫu thì KHÔNG vẽ. Đuôi đường cong luôn thưa vì ít nút nào bị "
        "luyện tới lần thứ tám; một điểm dựng trên 2 mẫu nhảy 0% hay 100% tuỳ "
        "một câu, mà mắt người nhìn biểu đồ thì tin ngay. Mỗi điểm mang theo cỡ "
        "mẫu, và điểm dưới ngưỡng bị bỏ HẲN chứ không trả về kèm cờ — trả về thì "
        "sớm muộn có chỗ vẽ nó lên.")

    doan(d,
        "Hiệu quả của một can thiệp phụ đạo được đo bằng giao thức A-R-A (Đánh "
        "giá → Can thiệp → Đánh giá lại), với chỉ số biến thiên tri thức:")
    cong_thuc(d, "ΔC = P(L) tại lần đo SAU − P(L) tại lần đo TRƯỚC")

    thuat_toan(d, "3.14", "Kiểm tính hợp lệ của một cặp A-R-A",
        "một cặp gồm hai lần đo, mỗi lần có mức thạo và danh sách mã câu đã hỏi; "
        "tên mẫu lời nhắc và số phiên bản.",
        "hợp lệ hay không, kèm lý do khi không hợp lệ.",
        [
            "1  if thiếu mức thạo ở một trong hai lần đo:",
            "2      return (false, «thiếu mức nắm»)",
            "3  if một trong hai danh sách câu rỗng:",
            "4      return (false, «thiếu danh sách câu đã hỏi»)",
            "5  trùng ← câu_sau ∩ câu_trước",
            "6  if trùng ≠ ∅:                             // ⚠ CHỐT QUAN TRỌNG NHẤT",
            "7      return (false, «lần đo sau dùng lại câu của lần trước»)",
            "8  return (true, «»)",
        ],
        ghi_chu=[
            "Dòng 6 — nếu lần đo sau hỏi lại đúng những câu vừa chữa thì người "
            "học trả lời đúng vì vừa NHÌN THẤY đáp án. Đó là đo trí nhớ ngắn hạn "
            "chứ không đo hiểu bài, và nó sai theo hướng ĐẸP LÊN: mọi bài phụ "
            "đạo đều trông như hiệu quả, kể cả bài vô dụng. Không có chốt này "
            "thì toàn bộ chỉ số ΔC mất giá trị.",
        ])

    doan(d,
        "Khi gom ΔC để so sánh giữa các mẫu lời nhắc, việc gom theo SỐ PHIÊN BẢN "
        "chứ không theo mã băm là bắt buộc: mã băm đổi cả khi sửa một lỗi chính "
        "tả, nên gom theo băm sẽ chẻ dữ liệu ra vụn, mỗi nhóm vài mẫu, và không "
        "so được gì. Ngoài ra, một mẫu chỉ được đưa ra con số trung bình khi có "
        "tối thiểu 5 cặp hợp lệ, và số cặp bị LOẠI phải hiện ra chứ không giấu — "
        "một mẫu có 40 cặp mà 35 bị loại thì con số trung bình của 5 cặp còn lại "
        "không đáng tin, và người đọc phải thấy điều đó.")

    bang(d,
        ["Độ đo", "Định nghĩa", "Ngưỡng / điều kiện dùng"],
        [
            ["Độ dốc đường cong học tập",
             "Hệ số góc của hồi quy log(tỉ lệ lỗi) theo log(số lần luyện)",
             "Mỗi điểm ≥ 3 mẫu; chỉ tính nút bắt đầu học trong kỳ"],
            ["ΔC trung bình theo mẫu lời nhắc",
             "Trung bình biến thiên tri thức của các cặp A-R-A hợp lệ",
             "≥ 5 cặp hợp lệ mới đưa ra số; báo kèm số cặp bị loại"],
            ["Số lượt tới thạo",
             "Số lượt trung bình từ lần chạm đầu tới khi P(L) ≥ θ",
             "Chỉ tính nút đã đạt θ; báo kèm số nút chưa đạt"],
            ["Mức phủ vốn theo khối",
             "Tỉ lệ nút đạt θ trên tổng nút học được của khối",
             "Khối ≥ 30 nút mới đáng tin"],
            ["Tỉ lệ bài đạt ngay lần đầu",
             "Số bài đạt ở lần sát hạch đầu / tổng số bài đã làm",
             "Phân biệt với bài đi vòng theo lưới đỡ"],
        ],
        ten="Bảng 3.28: Nhóm B — độ đo sư phạm",
    )

    # ── 3.6.4 ──────────────────────────────────────────────────────────────
    d.add_heading("3.6.4. Nhóm C — độ đo an toàn nội dung", level=2)
    doan(d,
        "Nhóm này đo hiệu lực của tầng chống ảo giác từ vựng. Điểm cần nhấn: "
        "phải đo ở HAI ĐIỂM — trước hậu kiểm và sau hậu kiểm — vì chỉ hiệu số "
        "giữa hai điểm mới nói lên tầng hậu kiểm đóng góp bao nhiêu.")

    bang(d,
        ["Độ đo", "Định nghĩa", "Đo ở đâu", "Giá trị mong đợi"],
        [
            ["OOV thô", "Tỉ lệ câu do mô hình sinh có ít nhất một từ ngoài vốn "
             "hợp lệ, đo TRƯỚC hậu kiểm",
             "Đầu ra thô của mô hình", "Càng thấp càng tốt, nhưng không kỳ vọng 0"],
            ["OOV sau hậu kiểm", "Cùng định nghĩa, đo SAU hậu kiểm",
             "Câu thực sự đưa cho người học", "Phải bằng 0 theo thiết kế"],
            ["Tỉ lệ bị bác", "Số câu bị hậu kiểm bác / tổng số câu mô hình sinh",
             "Hàm hậu kiểm", "Là ĐÓNG GÓP của tầng hậu kiểm; báo riêng theo "
             "từng đường công nhận bị trượt"],
            ["Tỉ lệ phải lùi", "Số lượt phải dùng câu dựng sẵn / tổng số lượt gọi",
             "Cờ lùi trong nhật ký", "Cao bất thường là dấu hiệu lời nhắc hỏng "
             "hoặc vốn từ quá hẹp"],
            ["Tỉ lệ lặp câu", "Số lượt câu sinh trùng câu lượt trước / tổng lượt",
             "Nhánh chống lặp của hậu kiểm", "Đo riêng vì đây là lỗi khác loại "
             "với ảo giác từ vựng"],
            ["Sai khuôn trả về", "Số lượt mô hình trả về không đúng khuôn JSON "
             "hoặc trả về rỗng",
             "Tầng bóc kết quả", "Liên quan tới giới hạn token và mức suy luận"],
        ],
        ten="Bảng 3.29: Nhóm C — độ đo an toàn nội dung",
    )

    canh_bao(d,
        "Độ đo “OOV sau hậu kiểm phải bằng 0” là một phát biểu KIỂM CHỨNG ĐƯỢC, "
        "khác hẳn phát biểu “lời nhắc đảm bảo 100% không từ lạ” vốn không kiểm "
        "được. Nếu một phép đo cho ra giá trị khác 0, đó là lỗi của hàm hậu "
        "kiểm và định vị được ngay ở một trong năm đường công nhận.")

    # ── 3.6.5 ──────────────────────────────────────────────────────────────
    d.add_heading("3.6.5. Nhóm D — độ đo hệ thống và vận hành", level=2)
    doan(d,
        "Nhóm này thường bị bỏ qua trong tài liệu về học thích ứng, nhưng nó là "
        "chỗ luận văn tự bảo vệ mình: mọi độ đo của ba nhóm trên đều đứng trên "
        "giả định “nhật ký đầy đủ và đúng chủ”.")

    bang(d,
        ["Độ đo", "Định nghĩa", "Vì sao cần"],
        [
            ["Tỉ lệ lượt ghi thành công",
             "Số bản ghi có mặt trên máy chủ / số lượt người học thực làm",
             "Đã từng bằng khoảng 10% mà không phép kiểm nào phát hiện; đây là "
             "độ đo lẽ ra đã bắt được"],
            ["Số bản ghi kẹt trong hàng đợi",
             "Kích thước hàng đợi tại máy sau mỗi lần đẩy",
             "Kẹt kéo dài nghĩa là hàng đợi nhiễm độc"],
            ["Số bản ghi bị bỏ qua",
             "Số bản ghi bị coi là đã tồn tại và gỡ khỏi hàng đợi",
             "Nếu tăng bất thường thì có một lỗi khác cũng cho ra cùng mã lỗi"],
            ["Bốn bất biến (mục 3.2.6)",
             "Chạy trực tiếp trên kho: phiên hai chủ · lỗ trong dãy · mô hình "
             "khớp nhật ký · nút thiếu hồ sơ",
             "Điều kiện tiên quyết để mọi số liệu thực nghiệm có nghĩa"],
            ["Độ trễ đầu-cuối một lượt sinh",
             "Từ lúc người học bấm tới lúc câu sinh hiện ra",
             "Trẻ nhỏ mất tập trung nhanh; độ trễ là một biến sư phạm"],
            ["Chênh lệch số phút ĐO ĐƯỢC và SUY RA",
             "So số phút máy con bấm giờ với số phút suy từ khoảng cách giữa các "
             "lượt trả lời",
             "Phép suy ra bỏ sót toàn bộ thời gian xem giảng — riêng bốn quyển "
             "Toán là 405 video, cộng lại khoảng 390 phút"],
        ],
        ten="Bảng 3.30: Nhóm D — độ đo hệ thống",
    )

    canh_bao(d,
        "Điểm phát âm KHÔNG được đưa vào bất kỳ độ đo tổng hợp nào của nhóm A "
        "và nhóm B mà không nêu giới hạn kèm theo. Bộ nhận dạng giọng nói của "
        "trình duyệt phụ thuộc chất lượng micro và mức ồn môi trường: cùng một "
        "người học, hai thiết bị khác nhau có thể cho kết quả khác nhau. Ba dạng "
        "lượt nói được gắn nhãn riêng để có thể tách ra khi cần một phép đo "
        "thuần nhất.")
