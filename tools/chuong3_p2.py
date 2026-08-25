#!/usr/bin/env python3
"""CHƯƠNG 3 — phần 2: mục 3.3 (nhận biết hành vi) và 3.4 (chẩn đoán lỗ hổng)."""
from __future__ import annotations

from chuong3_khung import (
    bang, canh_bao, cham, cong_thuc, do, doan, hinh_chu, ma_lenh, thuat_toan,
)


def viet(d):
    _m33(d)
    _m34(d)


# ═══════════════════════════════════════════════════════════════════════════
# 3.3 · NHẬN BIẾT HÀNH VI NGƯỜI HỌC
# ═══════════════════════════════════════════════════════════════════════════
def _m33(d):
    d.add_heading("3.3. Phương pháp nhận biết hành vi người học", level=1)
    doan(d,
        "Mô hình tri thức của người học chỉ chính xác đến mức mà tín hiệu đầu "
        "vào của nó chính xác. Mục này trình bày cách hệ thống chuyển các thao "
        "tác quan sát được — một cú bấm, một quãng im lặng, một lần đóng màn — "
        "thành các đại lượng có thể đưa vào mô hình. Đây là tầng nằm giữa người "
        "học và thuật toán chẩn đoán, và cũng là tầng dễ hỏng trong im lặng "
        "nhất: một tín hiệu đo sai không làm chương trình dừng lại, nó chỉ làm "
        "mọi kết luận phía sau lệch đi.")

    # ── 3.3.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.1. Bài toán và bảy loại hành vi cần nhận biết", level=2)
    doan(d,
        "Bài toán nhận biết hành vi được phát biểu như sau: cho một chuỗi thao "
        "tác thô của người học trên giao diện, hãy suy ra các trạng thái và "
        "khuynh hướng không quan sát trực tiếp được, kèm theo một đánh giá về độ "
        "tin cậy của mỗi suy luận. Yêu cầu về độ tin cậy là phần bắt buộc: với "
        "cỡ mẫu nhỏ, một suy luận sai không chỉ vô dụng mà còn tự củng cố — "
        "mục 3.3.4 trình bày một ví dụ cụ thể của vòng lặp tự củng cố ấy.")

    bang(d,
        ["#", "Hành vi", "Quan sát trực tiếp được?", "Suy ra từ tín hiệu nào"],
        [
            ["H1", "Trả lời đúng / sai", "CÓ", "Kết quả chấm của câu hỏi"],
            ["H2", "Đoán lụi", "KHÔNG",
             "Thời gian phản hồi thấp bất thường kết hợp định dạng có xác suất "
             "đoán trúng cao"],
            ["H3", "Bế tắc", "KHÔNG",
             "Thời gian phản hồi ≥ 45 giây mà vẫn sai"],
            ["H4", "Gặp khó tới mức cần trợ giúp", "GIÁN TIẾP",
             "Số gợi ý đã hiện — gợi ý hiện tự động sau hai lần sai"],
            ["H5", "Bỏ dở buổi học", "MỘT PHẦN",
             "Bản ghi rời màn khi chưa hoàn thành; chỉ ghi được khi rời qua thao "
             "tác trong ứng dụng"],
            ["H6", "Mệt mỏi nhận thức", "KHÔNG",
             "Thời gian phản hồi chậm dần trong phiên, so trong cùng định dạng"],
            ["H7", "Ưa một định dạng câu hỏi", "KHÔNG",
             "Tỉ lệ đúng theo từng định dạng, chỉ tính lượt trả lời đầu"],
        ],
        ten="Bảng 3.15: Bảy loại hành vi và tín hiệu tương ứng",
    )

    doan(d,
        "Chỉ H1 là quan sát trực tiếp. Sáu hành vi còn lại đều là suy luận, và "
        "mỗi suy luận đều có một cách hỏng riêng. Các thuật toán dưới đây vì thế "
        "được trình bày kèm điều kiện áp dụng và giới hạn đã biết, không chỉ kèm "
        "thủ tục.")

    # ── 3.3.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.2. Thu nhận và ghi vết", level=2)
    doan(d,
        "Mọi tín hiệu đều bắt nguồn từ một bản ghi lượt trả lời. Thuật toán 3.1 "
        "mô tả cách bản ghi được dựng, xếp hàng và đẩy lên máy chủ. Thiết kế của "
        "nó bị chi phối bởi ràng buộc R4 (chạy được khi mất mạng) và bởi tính "
        "bất biến của kho sự kiện.")

    thuat_toan(d, "3.1", "Thu nhận và ghi vết một lượt trả lời",
        "mã người học u; mã phiên s; mã bài m; nhật ký phiên hiện tại W gồm các "
        "lượt đã ghi trong phiên; một lượt mới w = (mã câu, mã nút, đúng/sai, "
        "thời gian phản hồi, số gợi ý đã hiện, định dạng, mốc thời gian).",
        "hàng đợi tại máy được cập nhật; số bản ghi đã lên máy chủ; số bản ghi "
        "bị bỏ qua vì đã tồn tại.",
        [
            "1  W ← W ∪ {w}                              // nhật ký cả phiên",
            "2  R ← ∅",
            "3  for i, e in enumerate(W):",
            "4      id ← GHÉP(u, s, m, e.mã_câu, i)      // i là SỐ THỨ TỰ lượt",
            "5      R ← R ∪ { bản_ghi(id, u, s, m, e, v=2) }",
            "6  ",
            "7  D ← ĐỌC_SỔ_ĐÃ_GỬI()                     // tập mã đã lên máy chủ",
            "8  Q ← ĐỌC_HÀNG_ĐỢI()",
            "9  Q ← { r ∈ Q ∪ R : r.id ∉ D }             // trùng mã thì ghi đè",
            "10 GHI_HÀNG_ĐỢI(Q)",
            "11 if u là mã tạm hoặc không có mạng: return   // giữ lại, học tiếp",
            "12 ",
            "13 for mỗi lô L gồm tối đa 200 bản ghi của Q:",
            "14     try:",
            "15         GỬI(L);  D ← D ∪ mã(L)",
            "16     except:                               // lô hỏng → thử LẺ",
            "17         for r in L:",
            "18             try:",
            "19                 GỬI([r]);  D ← D ∪ {r.id}",
            "20             except e:",
            "21                 if e.mã == 'permission-denied':",
            "22                     D ← D ∪ {r.id}        // kho bất biến ⇒ đã có",
            "23                     bỏ_qua ← bỏ_qua + 1",
            "24                 else:",
            "25                     mất_mạng ← true; break   // GIỮ phần còn lại",
            "26 GHI_HÀNG_ĐỢI({ r ∈ Q : r.id ∉ D })",
        ],
        ghi_chu=[
            "Dòng 4 — số thứ tự i là thành phần không bỏ được của mã bản ghi. "
            "Nếu đẩy từng lượt một thì i luôn bằng 0, mọi lượt của cùng một câu "
            "sẽ đè lên nhau, và mất đúng thông tin mà nhật ký sinh ra để giữ: "
            "rằng người học sai hai lần rồi mới đúng.",

            "Dòng 9 và dòng 22 cùng chống một lỗi. Kho sự kiện cấm ghi đè, mà "
            "lệnh ghi theo lô của cơ sở dữ liệu là NGUYÊN KHỐI — một bản ghi đã "
            "tồn tại làm rơi cả lô. Hệ quả trước khi vá: mỗi phiên chỉ có bản "
            "ghi ĐẦU TIÊN lên được máy chủ, phần còn lại nằm chết trong bộ nhớ "
            "tại máy. Sổ “đã gửi” ở dòng 9 chặn từ nay; phép thử lẻ ở dòng 17–23 "
            "gỡ độc cho hàng đợi đã nhiễm từ trước. Thiếu một trong hai thì vá "
            "không có tác dụng.",

            "Dòng 21 — phải phân biệt bằng MÃ LỖI, không được “cứ hỏng là bỏ”. "
            "Mất mạng mà bỏ hết thì mất trắng công học của người học, đúng thứ "
            "cả cơ chế hàng đợi này sinh ra để tránh.",

            "Dòng 23 — số bản ghi bị bỏ phải được ĐẾM và trả về, không bỏ trong "
            "im lặng: nếu sau này có một lỗi khác cũng cho ra cùng mã lỗi thì dữ "
            "liệu sẽ bay mà không ai biết.",
        ])

    doan(d,
        "Về phép đo thời gian phản hồi, một chi tiết đáng nêu vì nó quyết định "
        "chất lượng của cả nhóm tín hiệu H2, H3 và H6: mốc bấm giờ được đặt lại "
        "MỖI LƯỢT, không phải mỗi câu. Người học sai lần một, đọc lời báo sai, "
        "rồi thử lại — nếu không đặt lại mốc thì thời gian của lượt hai gồm cả "
        "quãng ngồi đọc lời báo, và đại lượng thu được không còn là thời gian "
        "suy nghĩ nữa. Tương tự, mỗi lượt mang mốc thời gian RIÊNG chứ không "
        "dùng chung một mốc cho cả loạt; dùng chung thì mọi phép đo khoảng cách "
        "giữa các lượt đều ra 0.")

    # ── 3.3.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.3. Nhận biết mệt mỏi nhận thức", level=2)
    doan(d,
        "Mệt mỏi là trạng thái bên trong, không quan sát được. Hệ thống suy ra "
        "nó từ hai tín hiệu độc lập; mục này trình bày tín hiệu thứ nhất, mục "
        "3.3.5 trình bày tín hiệu thứ hai.")

    thuat_toan(d, "3.2", "Nhận biết chậm dần trong phiên",
        "tập bản ghi lượt A trong một khoảng thời gian; ngưỡng cỡ mẫu k = 3; "
        "ngưỡng chậm hơn δ = 0,25.",
        "cờ mệt mỏi; thời gian phản hồi trung bình nửa đầu và nửa cuối; mức chênh "
        "lệch tương đối; số phiên đã dùng được; cờ đủ dữ liệu.",
        [
            "1  A ← { a ∈ A : a.ms hợp lệ và a.ms > 0 và a.sessionId tồn tại }",
            "2  đầu_tổng ← 0; đầu_đếm ← 0; cuối_tổng ← 0; cuối_đếm ← 0",
            "3  ",
            "4  for mỗi phiên p trong A:",
            "5      sắp p theo mốc thời gian tăng dần",
            "6      G ← NHÓM_THEO_ĐỊNH_DẠNG(p)          // ⚠ then chốt",
            "7      for mỗi nhóm g ∈ G:",
            "8          if |g| < 2k: continue            // chưa đủ mẫu, bỏ nhóm",
            "9          h ← ⌊|g| / 2⌋",
            "10         đầu  ← g[0 .. h-1]              // h lượt ĐẦU",
            "11         cuối ← g[|g|-h .. |g|-1]        // h lượt CUỐI",
            "12         cộng dồn đầu, cuối vào bốn biến ở dòng 2",
            "13 ",
            "14 if đầu_đếm = 0 hoặc cuối_đếm = 0: return (đủ_dữ_liệu = false)",
            "15 msĐầu  ← đầu_tổng / đầu_đếm",
            "16 msCuối ← cuối_tổng / cuối_đếm",
            "17 chậmHơn ← (msCuối − msĐầu) / msĐầu",
            "18 return (mệt_mỏi = chậmHơn ≥ δ, msĐầu, msCuối, chậmHơn)",
        ],
        ghi_chu=[
            "Dòng 6 là chỗ quyết định tính đúng đắn của cả thuật toán. Cách hiển "
            "nhiên là so thẳng nửa đầu phiên với nửa cuối phiên. Cách ấy SAI, và "
            "sai một chiều: bài học đi theo thang độ khó tăng dần (khởi động → "
            "ráp câu → thử thách), nên câu cuối phiên VỐN ĐÃ khó hơn và tốn thời "
            "gian hơn câu đầu. So thẳng thì mọi buổi học đều cho ra “có dấu hiệu "
            "mệt”, và phụ huynh đọc thành “con tôi chóng mệt” trong khi thật ra "
            "hệ thống đang tăng độ khó đúng như thiết kế. Chỉ khi so TRONG CÙNG "
            "MỘT ĐỊNH DẠNG thì chênh lệch còn lại mới thuộc về người học.",

            "Dòng 8 — một định dạng phải có ít nhất 2k = 6 lượt trong phiên mới "
            "được dùng. Dưới ngưỡng đó, chênh lệch chỉ là một câu mà người học "
            "mải nhìn ra ngoài cửa sổ.",

            "Dòng 9–11 — với số lượt lẻ, lượt GIỮA bị bỏ hẳn chứ không dồn vào "
            "một bên. Dồn vào nửa sau là tự tay nghiêng kết quả về phía “mệt”.",
        ])

    # ── 3.3.4 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.4. Nhận biết khuynh hướng định dạng", level=2)
    doan(d,
        "Sáu định dạng câu hỏi được xoay vòng theo bậc độ khó, nhưng xoay theo "
        "luật chung chứ không theo người học. Một em nghe tốt mà gõ chữ kém vẫn "
        "nhận đúng chừng ấy câu gõ chữ như một em ngược lại. Đo được khuynh "
        "hướng ấy là điều kiện để nói tới thích ứng ở chiều sư phạm.")

    thuat_toan(d, "3.3", "Cập nhật và đọc hồ sơ định dạng",
        "hồ sơ hiện có H = { định dạng → (số đúng, tổng số) }; một lượt trả lời "
        "mới (định dạng f, đúng/sai c, lượt thứ mấy r); ngưỡng cỡ mẫu n₀ = 8.",
        "hồ sơ mới; và khi được hỏi, thứ hạng các định dạng đã đủ mẫu.",
        [
            "CẬP NHẬT(H, f, c, r):",
            "1  if r ≠ 1: return H              // ⚠ chỉ đếm lượt TRẢ LỜI ĐẦU",
            "2  H[f].tổng ← H[f].tổng + 1",
            "3  if c: H[f].đúng ← H[f].đúng + 1",
            "4  return H",
            "",
            "TỈ_LỆ_ĐÚNG(H, f):",
            "5  if H[f].tổng < n₀: return null   // “chưa biết”, KHÔNG phải “kém”",
            "6  return H[f].đúng / H[f].tổng",
            "",
            "XẾP_HẠNG(H):",
            "7  D ← { f : TỈ_LỆ_ĐÚNG(H, f) ≠ null }",
            "8  return sắp D giảm dần theo tỉ lệ đúng",
            "",
            "YẾU_NHẤT(H):",
            "9  D ← XẾP_HẠNG(H)",
            "10 if |D| < 2: return null          // một mình thì vừa mạnh vừa yếu",
            "11 return D[|D| − 1]",
        ],
        ghi_chu=[
            "Dòng 1 — chỉ lượt trả lời ĐẦU của mỗi câu được tính. Nếu tính cả "
            "lượt thử lại thì định dạng nào cho phép thử nhiều lần một cách tự "
            "nhiên sẽ có tỉ lệ đúng thấp hơn, mà đó là tính chất của định dạng "
            "chứ không phải của người học.",

            "Dòng 5 là chốt quan trọng nhất của thuật toán này, và lý do của nó "
            "là một vòng lặp tự củng cố: người học làm 2 câu gõ chữ, sai cả 2 → "
            "hệ thống kết luận “yếu định dạng gõ chữ, 0%” → cho ít câu gõ chữ đi "
            "→ cỡ mẫu không bao giờ lớn thêm → cái nhãn sai tự nuôi chính nó. Vì "
            "vậy dưới ngưỡng cỡ mẫu thì hệ thống trả về “chưa biết”, và mọi nơi "
            "tiêu thụ đều phải xử lý giá trị rỗng ấy chứ không được quy về 0.",

            "Dòng 10 — cần ít nhất hai định dạng đủ mẫu mới nói được “yếu nhất”. "
            "Một định dạng đứng một mình thì nó vừa mạnh nhất vừa yếu nhất, và "
            "câu ấy không mang thông tin nào.",
        ])

    doan(d,
        "Cách hồ sơ định dạng được TIÊU THỤ trình bày ở mục 3.4.7; điểm cần nhấn "
        "ở đây là nó chỉ đóng vai khoá xếp PHỤ. Hệ thống không đổi tỉ lệ các "
        "định dạng trong một bài và không bỏ câu nào — chỉ đổi thứ tự — vì số "
        "câu là cơ sở của phép chấm và của sổ tiến độ.")

    # ── 3.3.5 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.5. Nhận biết bỏ dở", level=2)
    doan(d,
        "Tín hiệu thứ hai của mệt mỏi, và cũng là tín hiệu về động lực: mỗi lần "
        "người học rời màn bài học khi chưa hoàn thành, hệ thống ghi một bản ghi "
        "gồm bốn trường — mã bài, chặng đang dở, số lượt đã làm, và số giây đã ở "
        "trong bài.")

    thuat_toan(d, "3.4", "Ghi nhận sự kiện rời màn giữa chừng",
        "mốc mở bài t₀; chặng hiện tại c; biến đếm số lượt đã làm trong bài; cờ "
        "đã hoàn thành bài.",
        "một mục học bạ loại `phien`, hoặc không ghi gì nếu bài đã hoàn thành.",
        [
            "1  khi thành phần màn bài học bị GỠ KHỎI CÂY GIAO DIỆN:",
            "2      if đã_hoàn_thành: return        // xong bài thì không phải bỏ dở",
            "3      GHI_HỌC_BẠ(loại = 'phien', {",
            "4          microId : mã bài,",
            "5          chang   : c,                // chặng đang dở lúc rời",
            "6          soLuot  : số lượt đã làm,",
            "7          giay    : ⌊(bây_giờ − t₀) / 1000⌋",
            "8      })                              // MỖI LẦN MỘT BẢN GHI",
        ],
        ghi_chu=[
            "Dòng 8 — mỗi lần bỏ dở là một bản ghi riêng, không gộp lại thành "
            "một biến đếm. Chính SỐ LẦN bỏ dở cùng một bài mới là tín hiệu: đo "
            "trên dữ liệu thật thấy một bài bị bỏ dở năm lần với thời lượng 169 "
            "· 31 · 21 · 5 giây — dãy giảm dần ấy nói lên nhiều hơn con số tổng.",

            "GIỚI HẠN PHẢI NÊU KHI BÁO CÁO: chỉ ghi được khi người học rời màn "
            "qua thao tác trong ứng dụng. Đóng thẳng cửa sổ trình duyệt thì "
            "không ghi được. Con số thu được vì vậy là CẬN DƯỚI của số lần bỏ dở "
            "thật, dùng làm chỉ báo xu hướng chứ không phải phép đếm đầy đủ. Nêu "
            "ra giới hạn này cũng là cách phòng trước câu hỏi “vì sao số lần bỏ "
            "dở lại thấp bất thường”.",
        ])

    # ── 3.3.6 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.6. Nhận biết đoán lụi và bế tắc", level=2)
    doan(d,
        "Hai hành vi này cùng dựa trên thời gian phản hồi nhưng nằm ở hai đầu "
        "của thang, và được xử lý ở hai chỗ khác nhau của hệ thống.")
    cham(d, [
        ("Bế tắc (H3) — ", "một lượt có thời gian phản hồi từ 45 giây trở lên mà "
         "vẫn sai. Đây là dấu hiệu người học đang bí chứ không phải làm ẩu, và "
         "nó khác hẳn một lượt sai trong ba giây. Hệ thống xếp hạng các lượt như "
         "vậy và đưa lên sổ phụ huynh, vì đó là chỗ người lớn can thiệp được."),
        ("Đoán lụi (H2) — ", "được xử lý ở tầng mô hình chứ không ở tầng nhận "
         "biết, thông qua tham số P(G) của thuật toán Bayes. Cách này tránh phải "
         "đặt một ngưỡng thời gian tuỳ tiện cho “nhanh bất thường”, vốn phụ "
         "thuộc mạnh vào độ tuổi và vào định dạng câu hỏi. Với những câu được "
         "người soạn đánh dấu BẮT BUỘC ĐÚNG, hệ thống hạ P(G) từ 0,30 xuống "
         "0,15 — trả lời đúng một câu bẫy nhờ đoán thì khó hơn hẳn, nên tín hiệu "
         "quan sát được ở đó đáng tin hơn. Chi tiết ở mục 3.4.3."),
    ])

    # ── 3.3.7 ──────────────────────────────────────────────────────────────
    d.add_heading("3.3.7. Tổng hợp: từ tín hiệu tới nơi tiêu thụ", level=2)
    bang(d,
        ["Hành vi", "Tín hiệu", "Ngưỡng / cỡ mẫu", "Nơi tiêu thụ", "Giới hạn đã biết"],
        [
            ["H1 Đúng/sai", "`correct`", "—",
             "Mô hình Bayes (3.4.3)", "Chỉ 4 pha tự trả lời mới được tính"],
            ["H2 Đoán lụi", "Tham số P(G)", "P(G)=0,30; câu bẫy 0,15",
             "Mô hình Bayes (3.4.3)", "Không phân biệt được từng lượt cụ thể"],
            ["H3 Bế tắc", "`ms` ≥ 45 000", "≥ 45 giây và sai",
             "Sổ phụ huynh", "Bản ghi đời cũ không có `ms` đáng tin"],
            ["H4 Cần trợ giúp", "`hintsUsed`", "Gợi ý hiện sau 2 lần sai",
             "Hồ sơ nút (H_req)", "Là “đã thấy”, không phải “đã xin”"],
            ["H5 Bỏ dở", "Mục học bạ `phien`", "Mỗi lần một bản ghi",
             "Sổ phụ huynh", "CẬN DƯỚI — đóng trình duyệt thì không ghi"],
            ["H6 Mệt mỏi", "Chậm dần trong phiên", "≥ 3 lượt mỗi nửa; chênh ≥ 25%",
             "Sổ phụ huynh", "Phải tách theo định dạng, nếu không thì luôn dương"],
            ["H7 Ưa định dạng", "Tỉ lệ đúng theo định dạng", "≥ 8 lượt mỗi định dạng",
             "Xếp thứ tự câu (3.4.7); vector S", "Dưới cỡ mẫu trả “chưa biết”"],
        ],
        ten="Bảng 3.16: Tổng hợp bảy tín hiệu hành vi",
    )

    canh_bao(d,
        "Bốn trên bảy hành vi hiện được ĐO và BÁO cho người lớn, chưa được dùng "
        "để tự động điều chỉnh buổi học. Đây là một lựa chọn có ý thức: các "
        "ngưỡng ở cột thứ ba chưa được hiệu chỉnh trên dữ liệu học thật đủ lớn, "
        "và để một ngưỡng chưa hiệu chỉnh tự động cắt ngắn buổi học của một đứa "
        "trẻ là rủi ro lớn hơn giá trị thu được. Việc hiệu chỉnh chúng là nội "
        "dung của kịch bản thực nghiệm KB1 ở mục 3.7.")


# ═══════════════════════════════════════════════════════════════════════════
# 3.4 · CHẨN ĐOÁN LỖ HỔNG KIẾN THỨC
# ═══════════════════════════════════════════════════════════════════════════
def _m34(d):
    d.add_heading("3.4. Phương pháp chẩn đoán lỗ hổng kiến thức", level=1)

    # ── 3.4.1 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.1. Bài toán chẩn đoán", level=2)
    doan(d,
        "Chẩn đoán ở đây được hiểu theo nghĩa hẹp và cụ thể: phân biệt NƠI LỖI "
        "LỘ RA với NƠI LỖ HỔNG NẰM. Một em học sinh lớp 3 sai câu “How many "
        "books are there?” ở bài 12. Nơi lộ ra là bài 12. Nhưng em có thể sai vì "
        "chưa vững số đếm học từ bài 2 — và nếu hệ thống chỉ cho luyện thêm mẫu "
        "câu bài 12 thì em vẫn sai, vì cái hổng nằm chỗ khác. Đây chính là chỗ "
        "một hệ thống thích ứng khác một hệ thống chỉ đếm đúng–sai.")

    doan(d,
        "Bài toán gồm ba bước nối tiếp, mỗi bước là một thuật toán riêng:")
    cham(d, [
        ("Ước lượng trạng thái — ", "từ chuỗi quan sát, tính xác suất người học "
         "nắm vững từng nút, có tính tới suy giảm theo thời gian (Thuật toán 3.5)."),
        ("Định vị nguyên nhân — ", "từ nút người học sai, duyệt ngược đồ thị "
         "theo cạnh tiên quyết để xếp hạng các nút khả nghi (Thuật toán 3.6)."),
        ("Chọn can thiệp — ", "từ trạng thái và vị trí nguyên nhân, quyết định "
         "hành động sư phạm tiếp theo (Thuật toán 3.9)."),
    ])

    # ── 3.4.2 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.2. Thông tin đầu vào", level=2)
    bang(d,
        ["Nguồn", "Nội dung", "Nơi lưu", "Nhịp cập nhật"],
        [
            ["Nhật ký lượt trả lời", "Chuỗi quan sát thô của người học",
             "attempts/ trên máy chủ", "Từng lượt, đẩy theo lô"],
            ["Hồ sơ nút tri thức", "P(L), số lần sai liên tiếp, mốc chạm gần nhất",
             "mastery/{uid}/units/", "Từng lượt, qua hàm nền"],
            ["Đồ thị rút gọn", "Quan hệ tiên quyết giữa các nút",
             "Tệp tĩnh 127 KB ở máy người học", "Theo đợt dựng học liệu"],
            ["Bộ tham số BKT", "P(L₀), P(T), P(S), P(G) và biến thể theo câu",
             "Hằng số trong mã", "Khi hiệu chỉnh lại"],
            ["Hồ sơ định dạng", "Tỉ lệ đúng theo từng định dạng",
             "Sổ tiến độ tại máy", "Từng lượt trả lời đầu"],
        ],
        ten="Bảng 3.17: Năm nguồn thông tin đầu vào của tầng chẩn đoán",
    )

    # ── 3.4.3 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.3. Ước lượng trạng thái: BKT có cơ chế quên", level=2)
    doan(d,
        "Thuật toán theo dõi tri thức Bayes chuẩn (mục 2.3.2) giả định tri thức "
        "chỉ đi lên. Với việc thụ đắc ngôn ngữ, giả định ấy không đúng: từ vựng "
        "và cấu trúc bị quên dần khi không gặp lại. Hệ thống bổ sung một bước "
        "suy giảm trước bước cập nhật Bayes.")

    doan(d, "Bước suy giảm dùng hàm mũ với nửa đời h:")
    cong_thuc(d, "P′(L) = 0,5 + ( P(L) − 0,5 ) · 2^( −Δt / h )",
              "Δt — số ngày kể từ lần chạm gần nhất; h = 14 ngày")

    canh_bao(d,
        "Hàm kéo mức thạo về 0,5 chứ KHÔNG về 0. Hệ quả có hai chiều và cả hai "
        "đều đúng theo nghĩa mô hình. Chiều thứ nhất: người học quên thì trạng "
        "thái trở thành “không chắc”, không thành “chưa từng biết” — kéo về 0 là "
        "bắt học lại từ đầu một thứ đã từng thạo, và với trẻ nhỏ thì đó là hình "
        "phạt cho việc nghỉ vài hôm. Chiều thứ hai, nghe ngược đời nhưng là hệ "
        "quả đúng: một nút từng sai nhiều (P(L) thấp) sẽ NHÍCH LÊN theo thời "
        "gian, vì cái phân rã ở đây là ĐỘ TIN CẬY của hệ thống vào hiểu biết "
        "hiện có, không phải năng lực của người học.")

    canh_bao(d,
        "h = 14 ngày là con số CHỌN theo lịch ôn sẵn có (+1 · +3 · +7 ngày), "
        "không phải con số hiệu chỉnh từ dữ liệu học thật. Người theo đúng lịch "
        "ôn thì gặp lại trước khi mức thạo rơi đáng kể; nghỉ hẳn hai tuần thì "
        "mới thấy tụt. Việc hiệu chỉnh h là nội dung của kịch bản KB1 (mục 3.7).")

    thuat_toan(d, "3.5", "Cập nhật hồ sơ nút từ một lượt trả lời",
        "hồ sơ nút hiện có D (có thể rỗng); một lượt trả lời a gồm đúng/sai, "
        "thời gian phản hồi, số gợi ý, cờ câu bắt buộc đúng; mốc hiện tại t.",
        "hồ sơ nút mới, gồm mức thạo trước và sau, các biến đếm và các đại lượng "
        "hành vi cộng dồn.",
        [
            "1  Δt ← (t − D.lastSeen) / 86 400 000          // số ngày; thiếu ⇒ 0",
            "2  p₀ ← D.p nếu có, ngược lại P(L₀) = 0,10",
            "3  p₀ ← 0,5 + (p₀ − 0,5) · 2^(−Δt / 14)        // QUÊN DẦN",
            "4  ",
            "5  (S, G) ← (0,06 , 0,15) nếu a.mustPass       // câu bẫy: tin hơn",
            "           ngược lại (0,10 , 0,30)",
            "6  if a.correct:",
            "7      p₁ ← p₀(1 − S) / [ p₀(1 − S) + (1 − p₀)·G ]",
            "8  else:",
            "9      p₁ ← p₀·S / [ p₀·S + (1 − p₀)(1 − G) ]",
            "10 p  ← p₁ + (1 − p₁)·T           với T = 0,08  // CƠ HỘI HỌC",
            "11 p  ← kẹp(p, 0,001 , 0,999)",
            "12 ",
            "13 D′.pTruoc     ← p₀              // để tính ΔC ở mục 3.6.3",
            "14 D′.p          ← p",
            "15 D′.mastered   ← (p ≥ θ)         với θ = 0,85",
            "16 D′.nAttempts  ← D.nAttempts + 1",
            "17 D′.nCorrect   ← D.nCorrect + [a.correct]",
            "18 D′.saiLienTiep← 0 nếu a.correct, ngược lại D.saiLienTiep + 1",
            "19 if a.ms hợp lệ:                              // ⚠ THIẾU thì BỎ,",
            "20     D′.msTong ← D.msTong + a.ms              //   không coi là 0",
            "21     D′.msDem  ← D.msDem + 1",
            "22 D′.msTrungBinh ← D′.msTong / D′.msDem  nếu msDem > 0, ngược lại null",
            "23 D′.goiTong     ← D.goiTong + a.hintsUsed",
            "24 D′.lastSeen    ← t",
            "25 return D′",
        ],
        ghi_chu=[
            "Dòng 3 — bản ghi đời cũ không có mốc chạm gần nhất thì KHÔNG phân "
            "rã, coi như vừa gặp. Thà không phân rã còn hơn phân rã theo một mốc "
            "bịa ra.",

            "Dòng 5 — đây là một dạng cá thể hoá tham số theo CÂU HỎI chứ không "
            "theo người học. Rẻ hơn nhiều so với ước lượng tham số riêng cho "
            "từng người mà vẫn nắm được phần lớn khác biệt giữa các câu hỏi: câu "
            "bẫy khó đoán trúng hơn, nên vừa hạ P(G) vừa hạ P(S), và hệ quả là "
            "sai một câu bẫy kéo mức thạo xuống mạnh hơn sai một câu thường.",

            "Dòng 13 — mức thạo TRƯỚC lượt này vẫn được ghi ra kể cả ở lần chạm "
            "đầu tiên (khi nó bằng P(L₀)), để phép trừ p − pTruoc lúc nào cũng "
            "có nghĩa mà không phải xử lý trường hợp riêng.",

            "Dòng 19–22 — thời gian phản hồi thiếu thì không tính vào MẪU SỐ, "
            "chứ không coi là 0. Coi là 0 thì mỗi dòng thiếu kéo trung bình "
            "xuống, và “người học trả lời nhanh dần” thành một kết luận do lỗi "
            "ghi sinh ra. Cộng dồn bằng TỔNG chứ không nhân trung bình cũ với "
            "n − 1: phép sau trôi số dần sau vài trăm lượt, mà tài liệu này sống "
            "suốt đời học của một đứa trẻ.",

            "Phạm vi áp dụng: thuật toán chỉ chạy cho bốn pha người học TỰ trả "
            "lời — luyện tập, sát hạch, câu chốt nhanh sau đoạn đọc, câu xen "
            "giữa ví dụ mẫu. Ba pha hệ thống đang trình bày lời giải bị loại. "
            "Trước khi mở rộng danh sách, hai pha sau bị bỏ trắng, tương ứng 31% "
            "số câu người học thực làm.",
        ])

    doan(d,
        "Bộ tham số được hiệu chỉnh bằng thực nghiệm trên chính chuỗi hành vi "
        "của hệ thống, không lấy nguyên giá trị mặc định trong tài liệu. Bảng "
        "3.18 nêu giá trị và căn cứ.")
    bang(d,
        ["Tham số", "Giá trị", "Căn cứ"],
        [
            ["P(L₀)", "0,10",
             "Bộ cũ 0,25 kết hợp P(G) = 0,20 tuyên bố thạo chỉ sau hai câu đúng "
             "— quá dễ dãi với học sinh tiểu học"],
            ["P(T)", "0,08", "Đặt để đạt nhịp bốn câu đúng liên tiếp mới công nhận thạo"],
            ["P(S)", "0,10 (câu bẫy: 0,06)", "Sơ suất ở lứa tuổi này không hiếm"],
            ["P(G)", "0,30 (câu bẫy: 0,15)",
             "Phần lớn câu là trắc nghiệm bốn lựa chọn; định dạng đúng–sai còn "
             "cao hơn nhưng dùng chung một giá trị để giữ mô hình đơn giản"],
            ["θ (ngưỡng thạo)", "0,85",
             "Với bộ tham số trên, tương ứng khoảng bốn câu đúng liên tiếp; và "
             "một câu sai sau đó kéo tụt xuống dưới ngưỡng"],
            ["θ_yếu", "0,30", "Dưới mức này thì luyện thêm cùng kiểu câu không gỡ được"],
            ["h (nửa đời trí nhớ)", "14 ngày", "Con số CHỌN theo lịch ôn; chưa hiệu chỉnh"],
        ],
        ten="Bảng 3.18: Bộ tham số của mô hình và căn cứ",
    )

    doan(d,
        "Chuỗi tám lượt dưới đây chạy trên chính mã của hệ thống, dùng để kiểm "
        "chứng bộ tham số cho ra nhịp mong muốn. Xuất phát từ P(L₀) = 0,10, "
        "chuỗi quan sát là: sai · đúng · đúng · đúng · sai · đúng · đúng · đúng.")
    ma_lenh(d, [
        "lượt  1  SAI    p = 0,094",
        "lượt  2  ĐÚNG   p = 0,299",
        "lượt  3  ĐÚNG   p = 0,597",
        "lượt  4  ĐÚNG   p = 0,831        ← ba câu đúng liền vẫn CHƯA đạt θ",
        "lượt  5  SAI    p = 0,459        ← MỘT câu sai kéo tụt sâu dưới ngưỡng",
        "lượt  6  ĐÚNG   p = 0,741",
        "lượt  7  ĐÚNG   p = 0,904        ← đạt θ = 0,85, công nhận thạo",
        "lượt  8  ĐÚNG   p = 0,968",
    ])
    doan(d,
        "Hai tính chất cần kiểm chứng đều xuất hiện. Thứ nhất, ba câu đúng liên "
        "tiếp từ trạng thái ban đầu vẫn chưa đủ để công nhận thạo (0,831 < "
        "0,85) — phải tới câu đúng thứ tư. Thứ hai, một câu sai đơn lẻ ở lượt 5 "
        "kéo mức thạo từ 0,831 xuống 0,459, tức tụt sâu dưới cả ngưỡng vùng phát "
        "triển gần, buộc người học phải chứng minh lại. Đây chính là nhịp mà "
        "ngưỡng θ = 0,85 được chọn để tạo ra, và là lý do bộ tham số cũ — với "
        "P(L₀) = 0,25 và P(G) = 0,20 — bị bác: bộ ấy công nhận thạo chỉ sau hai "
        "câu đúng.")

    # ── 3.4.4 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.4. Định vị nguyên nhân: lan truyền ngược", level=2)
    doan(d,
        "Khi người học thất bại lặp lại tại một nút, thuật toán duyệt ngược theo "
        "cạnh tiên quyết để xếp hạng các nút nền tảng theo mức khả nghi.")
    doan(d, "Độ ngờ của một nút cách nút thất bại k bước được định nghĩa:")
    cong_thuc(d, "doNgo(v) = α^k · ( 1 − P(L_v) )",
              "α = 0,6 — hệ số suy giảm theo bước")

    doan(d,
        "Công thức cần cả hai thành phần. Thành phần α^k phản ánh rằng nguyên "
        "nhân cách chỗ sai quá xa thì không còn là nguyên nhân theo nghĩa dạy "
        "được. Thành phần (1 − P(L)) phản ánh rằng một nút người học đã vững thì "
        "không phải thủ phạm, dù nó là tiên quyết.")

    thuat_toan(d, "3.6", "Định vị nút gốc rễ",
        "đồ thị G; hồ sơ mức thạo M; nút thất bại v₀; trần độ sâu d = 4; số nút "
        "trả về tối đa m = 3.",
        "danh sách nút khả nghi, sắp giảm dần theo độ ngờ, mỗi nút kèm số bước "
        "và mức thạo hiện tại.",
        [
            "1  E′ ← { e ∈ E : λ(e) ∈ {ban_do, noi_bai} }   // ⚠ LỌC THEO NHÃN",
            "2  thăm ← {v₀};  KQ ← ∅;  biên ← [v₀]",
            "3  for k = 1 .. d:",
            "4      biên_mới ← []",
            "5      for u ∈ biên:",
            "6          for v ∈ TIÊN_QUYẾT_CỦA(u, E′):",
            "7              if v ∈ thăm: continue",
            "8              thăm ← thăm ∪ {v}",
            "9              KQ ← KQ ∪ { (v, k) }",
            "10             biên_mới ← biên_mới + [v]",
            "11     biên ← biên_mới",
            "12 ",
            "13 for (v, k) ∈ KQ:",
            "14     p ← M[v].p nếu có, ngược lại 0,10       // ⚠ chưa học ⇒ đáng ngờ",
            "15     doNgo(v) ← 0,6^k · (1 − p)",
            "16 KQ ← { (v,k) ∈ KQ : p_v < θ }               // ⚠ loại nút ĐÃ THẠO",
            "17 return m phần tử đầu của KQ sắp giảm theo doNgo",
        ],
        ghi_chu=[
            "Dòng 1 — phép lọc theo nhãn cạnh là điều kiện đúng đắn, không phải "
            "tối ưu hoá. Duyệt trên toàn bộ tập cạnh sẽ đi qua quan hệ cấu thành "
            "và cho ra kết luận vô nghĩa. Loại cạnh “thứ tự đọc trong cùng một "
            "bài” cũng bị loại: sách dạy cả khối từ trong một buổi nên nó không "
            "phải cửa ải.",

            "Dòng 3 — trần độ sâu có mặt trước hết vì Ý NGHĨA: nguyên nhân cách "
            "chỗ sai bảy bước thì không còn dạy được. Nó đồng thời bảo đảm phép "
            "duyệt luôn dừng kể cả khi đồ thị có chu trình.",

            "Dòng 7 — tập đã thăm không phải để chống treo (trần độ sâu đã lo "
            "việc ấy) mà chống hai chuyện khác: cùng một nút bị trả về nhiều lần "
            "làm bảng chẩn đoán hiện một nút thành ba dòng, và số nhánh phình "
            "theo cấp số nhân khi có nhiều đường tới cùng một nút. Đã kiểm bằng "
            "cách gỡ ra: không treo, nhưng kết quả sai.",

            "Dòng 14 — nút chưa có số liệu được gán P(L₀) = 0,10, tức rất đáng "
            "ngờ, và đúng như vậy: một tiên quyết chưa từng chạm là lý do hay "
            "gặp nhất. Nhưng KHÔNG gán 0 tuyệt đối, vì “chưa có tin” vẫn khác "
            "“đã đo và thấy hổng”.",

            "Dòng 16 — nút đã thạo bị LOẠI HẲN chứ không xếp hạng thấp. Giữ lại "
            "thì màn hình có thể bày ra một “lỗ hổng gốc rễ” trỏ vào đúng thứ "
            "người học làm đúng mãi, và niềm tin vào cả bảng chẩn đoán mất theo.",
        ])

    doan(d,
        "Ví dụ chạy thật trên đồ thị đang vận hành, người học sai mẫu câu hỏi "
        "tuổi ở lớp 3:")
    ma_lenh(d, [
        "v₀ = sp_g3_u11_2   (lớp 3 — “How old is he?”)",
        "",
        "bước 1 : sp_g3_u2_2        p = 0,42   doNgo = 0,6¹ × 0,58 = 0,348",
        "bước 2 : sp_g3_u1_1        p = 0,71   doNgo = 0,6² × 0,29 = 0,104",
        "bước 2 : u_g3_starter      chưa có    doNgo = 0,6² × 0,90 = 0,324",
        "bước 3 : sp_g2_greeting    p = 0,55   doNgo = 0,6³ × 0,45 = 0,097",
        "",
        "→ nút gốc rễ = sp_g3_u2_2, và giả thuyết vượt lớp sp_g2_greeting vẫn",
        "  nằm trong danh sách để cô giáo xem được.",
    ])

    # ── 3.4.5 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.5. Lan truyền xuôi: cộng hưởng", level=2)
    doan(d,
        "Chiều ngược lại của lan truyền ngược: khi người học đã vững một nút nền "
        "tảng, các nút dựng trên nó đáng tin hơn đôi chút, và việc bắt làm lại "
        "từ đầu những bài dễ ở chủ đề mới là lãng phí thời gian.")

    thuat_toan(d, "3.7", "Cộng hưởng xuôi",
        "đồ thị G; hồ sơ mức thạo M; trần độ sâu d = 2; hệ số cộng hưởng "
        "β = 0,08.",
        "một ánh xạ { nút → mức thạo ước lượng mới }, CHỈ gồm những nút có thay "
        "đổi. Hàm không sửa hồ sơ gốc.",
        [
            "1  N ← { v : M[v].p ≥ θ }                    // ⚠ CHỐT 1",
            "2  R ← ∅",
            "3  for g ∈ N:",
            "4      for (v, k) ∈ DUYỆT_XUÔI(G, g, d):",
            "5          cũ ← R[v] nếu có, ngược lại M[v].p nếu có, ngược lại 0,10",
            "6          if cũ ≥ θ: continue               // đã thạo, không việc gì",
            "7          thêm ← (β / k) · M[g].p           // ⚠ CHỐT 2: nhỏ dần",
            "8          R[v] ← min( θ − 0,05 , cũ + thêm ) // ⚠ CHỐT 3: TRẦN",
            "9  return R",
        ],
        ghi_chu=[
            "Ba chốt cùng chống một lỗi duy nhất: TUYÊN THẠO KHỐNG. Nếu cộng "
            "hưởng đẩy được một nút lên thẳng “đã thạo” khi người học CHƯA LÀM "
            "câu nào của nút ấy, hệ thống sẽ bỏ qua một bài chưa từng học, và bỏ "
            "qua trong im lặng — mọi con số tổng đều đẹp. Chốt 1 giới hạn nguồn "
            "lan; chốt 2 làm mức cộng nhỏ dần theo bước; chốt 3 kẹp cứng kết quả "
            "dưới θ − 0,05, tức cộng hưởng không bao giờ TỰ NÓ đưa một nút tới "
            "ngưỡng thạo.",

            "Kết quả trả về là một ánh xạ RIÊNG, không trộn vào hồ sơ gốc. Trộn "
            "vào thì mức thạo ĐO ĐƯỢC và mức thạo SUY RA lẫn lộn, và lần cập "
            "nhật sau sẽ coi giá trị suy ra như một quan sát thật.",
        ])

    # ── 3.4.6 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.6. Ma trận trạng thái đồ thị", level=2)
    doan(d,
        "Kết quả cuối cùng của tầng chẩn đoán không phải một bảng điểm mà là một "
        "ma trận trạng thái: mỗi dòng là một nút người học đang chật vật, kèm "
        "nút gốc rễ tương ứng. Đây là dạng thông tin mà giáo viên và phụ huynh "
        "dùng được — không phải “em này sai 12 câu”, mà “em này sai ở mẫu câu "
        "bài 12, mà gốc là số đếm bài 2”.")

    thuat_toan(d, "3.8", "Dựng ma trận trạng thái",
        "đồ thị G; hồ sơ mức thạo M; ngưỡng chật vật 0,5; số dòng tối đa 10.",
        "danh sách dòng, mỗi dòng gồm mã nút, nhãn đọc được, mức thạo, và nút "
        "gốc rễ kèm nhãn.",
        [
            "1  K ← khoá của M",
            "2  K ← { GIẢI_MÃ(k) : k ∈ K }         // ⚠ khoá lưu ở dạng mã hoá URL",
            "3  K ← { v ∈ K : v ∈ V(G) }           // ⚠ lọc theo đồ thị MÔN NÀY",
            "4  L ← { (v, M[v].p, NHÃN(v)) : v ∈ K, M[v].p tồn tại và < 0,5 }",
            "5  sắp L tăng dần theo p; giữ 10 dòng đầu",
            "6  for (v, p, nhãn) ∈ L:",
            "7      gốc ← ĐỊNH_VỊ_GỐC_RỄ(G, M, v, m = 1)     // Thuật toán 3.6",
            "8      thêm (gốc, NHÃN(gốc)) vào dòng",
            "9  return L",
        ],
        ghi_chu=[
            "Dòng 2 — khoá tài liệu được mã hoá URL khi lưu. Bày thẳng khoá thô "
            "ra màn hình thì phụ huynh đọc một chuỗi kiểu `CHUONG%3A1%40G3`; "
            "chuyện này đã xảy ra thật.",

            "Dòng 3 — kho hồ sơ nút DÙNG CHUNG giữa hai môn (đó là chủ ý, vì hàm "
            "nền cập nhật mức thạo là hàm trung tính với môn). Không lọc theo đồ "
            "thị thì mã nút của môn kia lọt thẳng vào bảng của môn này.",

            "Dòng 4 — CHỈ nhận nút ĐÃ CÓ SỐ LIỆU. Nút người học chưa từng chạm "
            "không phải “đang chật vật”; gộp chúng vào thì bảng đầy những dòng "
            "nói “em chưa học phần này” — đúng nhưng vô dụng, và chúng dìm mất "
            "vài dòng thật sự đáng xem.",

            "Dòng 8 — nút gốc rễ phải kèm NHÃN ĐỌC ĐƯỢC. Không có nhãn thì bên "
            "gọi phải xử lý, không được bày mã máy ra cho người lớn đọc.",
        ])

    # ── 3.4.7 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.7. Hàm chính sách và ranh giới quyền quyết định", level=2)
    doan(d,
        "Hàm chính sách π ánh xạ trạng thái người học sang hành động sư phạm. Hệ "
        "thống hiện thực ba nhánh, nhưng điểm đáng nói nhất của mục này không "
        "phải ba nhánh ấy mà là RANH GIỚI QUYỀN: π trả lời câu hỏi “nên làm gì "
        "tiếp”, chứ không trả lời câu hỏi “có được đi tiếp không”.")

    thuat_toan(d, "3.9", "Hàm chính sách cho một nút và cho một bài",
        "hồ sơ nút D gồm mức thạo p và số lần sai liên tiếp S_c; hoặc danh sách "
        "nút của một bài.",
        "một trong ba hành động — TIẾP · VƯỢT ẢI · PHỤ ĐẠO — kèm lý do đọc được "
        "bằng tiếng Việt.",
        [
            "CHO MỘT NÚT π(D):",
            "1  if S_c ≥ 3: return (PHỤ_ĐẠO, «sai S_c lần liên tiếp»)  // ⚠ XÉT TRƯỚC",
            "2  if p không tồn tại: return (TIẾP, «chưa có số liệu»)",
            "3  if p ≥ θ:        return (VƯỢT_ẢI, «đã vững»)",
            "4  if p < θ_yếu:    return (PHỤ_ĐẠO, «còn yếu»)",
            "5  return (TIẾP, «đang học được»)",
            "",
            "CHO MỘT BÀI π_bài(M, danh sách nút N):",
            "6  if N rỗng: return (TIẾP, «bài chưa gắn nút nào»)",
            "7  T ← [ π(M[v]) : v ∈ N ]",
            "8  Mắc ← { t ∈ T : t = PHỤ_ĐẠO }",
            "9  if Mắc ≠ ∅:                              // ⚠ PHỤ ĐẠO THẮNG",
            "10     sắp Mắc tăng dần theo p; nút mắc nặng nhất là đích phụ đạo",
            "11     return (PHỤ_ĐẠO, nút_mắc = Mắc[0])",
            "12 if mọi t ∈ T đều là VƯỢT_ẢI: return (VƯỢT_ẢI)",
            "13 return (TIẾP)",
            "",
            "ĐƯỢC BỎ QUA BÀI NÀY KHÔNG:",
            "14 return đã_đạt_bài  AND  |N| ≥ 3  AND  π_bài(M, N) = VƯỢT_ẢI",
        ],
        ghi_chu=[
            "Dòng 1 — chuỗi sai liên tiếp được xét TRƯỚC mức thạo, và đây là "
            "quyết định thiết kế chứ không phải thứ tự tuỳ tiện. Mức thạo là một "
            "trung bình có quán tính; chuỗi sai liên tiếp là tín hiệu tức thời. "
            "Một người học có p = 0,96 mà vừa sai ba câu liền thì con số trung "
            "bình không phải thứ đáng nghe. Ngưỡng ba chứ không phải hai: sai "
            "hai lần liền là chuyện thường của việc học, cắt ngang ở đó thì mạch "
            "học bị ngắt liên tục.",

            "Dòng 9 — trong phép gộp ở mức bài, PHỤ ĐẠO THẮNG VƯỢT ẢI. Một bài "
            "mười nút với chín nút vững và một nút đang mắc thì việc cần làm là "
            "gỡ nút ấy, không phải cho bay qua cả bài. Cho vượt ải ở đây là bỏ "
            "lại đúng chỗ người học cần giúp nhất, và bỏ lại lặng lẽ.",

            "Dòng 14 — cửa bỏ qua bài cố ý HẸP, đòi đủ ba điều kiện. Thà để "
            "người học làm lại một bài đã vững, mất vài phút, còn hơn bỏ qua một "
            "bài chưa vững — vì bài ấy còn đỡ cho những bài sau.",
        ])

    doan(d,
        "Hàm chính sách KHÔNG quyết định việc người học có được sang bài kế tiếp "
        "hay không. Quyền ấy thuộc về một bộ luật riêng với đúng một điều:")
    cong_thuc(d, "ĐI TIẾP ĐƯỢC  ⟺  đã ĐẠT  ∨  đã THỬ THẬT ≥ 2 lần")

    doan(d,
        "Vế thứ hai là lưới đỡ, và nó tồn tại vì ràng buộc R2. Mô hình Bayes có "
        "thể chấm sai; nếu quyền mở đường nằm trong tay mô hình thì một người "
        "học bị đánh giá nhầm sẽ kẹt vĩnh viễn ở một bài — không có cách nào tự "
        "thoát, và cũng không biết để kêu. Với trẻ nhỏ, điều học được trong tình "
        "huống ấy không phải môn học mà là “mình học kém”. Cùng một luật được "
        "dùng lại nguyên vẹn ở ba tầng: mở bài kế tiếp, mở chặng kế tiếp, và cho "
        "phép để lại một câu làm sau. Ba chỗ cùng một luật thì người học học "
        "được luật ấy một lần rồi áp dụng ở mọi nơi.")

    canh_bao(d,
        "Bài đi vòng KHÔNG được ghi là đạt. Nó nằm trong danh sách còn nợ, mang "
        "nhãn riêng, và phải làm xong mới mở được kỳ ôn tập chương — đó là chỗ "
        "món nợ được đòi. Kỳ ôn tập chương không có cửa “thử hai lần”, vì nó là "
        "chỗ chốt một chương và ghi vào học bạ.")

    doan(d,
        "Kết quả của hàm chính sách được tiêu thụ ở hai chỗ. Khi trả về TIẾP, "
        "tầng thích ứng xếp lại thứ tự câu trong kho của bậc hiện tại theo bốn "
        "nhóm vùng phát triển gần, với hồ sơ định dạng làm khoá phụ. Khi trả về "
        "PHỤ ĐẠO, tầng thích ứng chuyển sang quy trình sinh bài vá ở mục 3.5.3.")

    bang(d,
        ["Thứ tự", "Nhóm", "Khoảng P(L)", "Vì sao xếp ở vị trí này"],
        [
            ["1", "Đang chông chênh", "0,30 ≤ p < 0,85",
             "Chính là vùng phát triển gần — luyện ở đây đổi được nhiều nhất; "
             "đưa lên đầu vì đầu buổi người học còn tỉnh táo nhất"],
            ["2", "Chưa có số liệu", "—",
             "Nút chưa từng chạm; phải học, và học sớm"],
            ["3", "Yếu hẳn", "p < 0,30",
             "Xếp SAU chứ không phải trước: luyện thêm cùng kiểu câu ở chỗ đang "
             "sai nhiều là bắt sai tiếp, mà mở đầu buổi bằng ba câu sai liền thì "
             "trẻ nghỉ. Chỗ này cần bài PHỤ ĐẠO, không phải thêm lượt luyện"],
            ["4", "Đã thạo", "p ≥ 0,85",
             "Vẫn cho làm nhưng để cuối; bỏ hẳn là việc của nhánh vượt ải"],
        ],
        ten="Bảng 3.19: Bốn nhóm xếp thứ tự câu theo vùng phát triển gần",
    )

    canh_bao(d,
        "Phép xếp này chỉ ĐỔI THỨ TỰ, không bỏ câu nào, và chỉ chạy trong kho "
        "của MỘT bậc độ khó. Bỏ bớt câu thì sổ tiến độ, thanh đếm câu và phép "
        "chấm đều lệch. Trộn giữa các bậc thì thang độ khó do người soạn dựng "
        "bị ném đi. Hồ sơ định dạng chỉ là khoá phụ: nhóm vùng phát triển gần "
        "vẫn quyết trước, vì cho định dạng thắng nhóm là mở đầu buổi học bằng "
        "thứ người học đã thạo, chỉ vì nó hợp cách hỏi.")

    # ── 3.4.8 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.8. Quy đổi mức phủ vốn sang thang năng lực", level=2)
    doan(d,
        "Phụ huynh và giáo viên cần một câu trả lời cho câu hỏi “con đang ở đâu”. "
        "Hệ thống cung cấp câu trả lời ấy bằng một phép quy đổi bắc cầu HAI "
        "NHỊP, và việc nói rõ hai nhịp là bắt buộc về mặt khoa học.")
    cong_thuc(d,
        "P(L) từng nút  →  % phủ vốn của một khối lớp  →  bậc CEFR của khối ấy",
        "nhịp 1: hệ thống ĐO ĐƯỢC · nhịp 2: quy ước do Chương trình GDPT 2018 ấn định")

    doan(d, "Mức phủ vốn của khối lớp b được định nghĩa:")
    cong_thuc(d,
        "phủ(b) = | { v ∈ V_học_được : khối(v) = b ∧ P(L_v) ≥ θ } |  /  "
        "| { v ∈ V_học_được : khối(v) = b } |")

    bang(d,
        ["Khối", "Lớp", "Bậc theo Chương trình GDPT 2018", "Số nút học được", "Đáng tin?"],
        [
            ["preA1", "1–2", "Chương trình làm quen (dưới Bậc 1)", "187", "CÓ"],
            ["A1", "3–5", "Bậc 1 — tương đương A1", "871", "CÓ"],
            ["A2", "6", "Bậc 2 — bắc cầu cấp hai", "4", "KHÔNG — dưới 30 nút"],
        ],
        ten="Bảng 3.20: Ba khối và mức tin cậy",
    )

    doan(d,
        "Hệ thống công nhận một bậc khi mức phủ đạt 0,60 VÀ khối ấy có tối thiểu "
        "30 nút. Chưa đạt thì hệ thống báo đúng tỉ lệ phủ hiện có chứ không quy "
        "ra bậc — câu đọc đúng là “con đã vững 34% vốn kiến thức của khối lớp mà "
        "chương trình xếp ở bậc A1”, câu đọc sai là “con đạt A1”.")

    canh_bao(d,
        "Đây KHÔNG phải phép đo theo chuẩn CEFR. CEFR định nghĩa bậc bằng mô tả "
        "năng lực làm được (can-do descriptors) — người học nói được gì, với ai, "
        "trong tình huống nào — chứ không định nghĩa bằng số đơn vị kiến thức đã "
        "nắm. Nhịp thứ hai là quy ước của chương trình quốc gia, không phải kết "
        "quả đo của hệ thống. Luận văn phải phát biểu đúng như vậy.")

    doan(d,
        "Ba lựa chọn trong phép quy đổi có thể tranh luận và cần bảo vệ được khi "
        "phản biện, nên được nêu tường minh:")
    cham(d, [
        ("Ngưỡng phủ 0,60 — ", "đòi 100% thì không ai đạt, vì đồ thị chứa cả nút "
         "chưa có bài dạy; dưới 0,50 thì “đạt” trong khi quá nửa vốn còn chưa "
         "nắm, nói ra không xuôi. Con số này đổi NGHĨA của chữ “đạt”, không đổi "
         "độ chính xác của phép đo."),
        ("Ngưỡng đáng tin 30 nút — ", "khối lớp 6 trong đồ thị chỉ có 4 nút bắc "
         "cầu; một người học nắm 1 nút sẽ ra “25% A2”, con số nói lên đúng là "
         "không có gì."),
        ("Mẫu số là TOÀN khối, không phải số nút đã chạm — ", "lấy mẫu số là “đã "
         "chạm” thì một người học đúng 5 nút và nắm cả 5 sẽ ra 100%, tức phép đo "
         "thưởng cho việc HỌC ÍT. Hệ quả phải chấp nhận: mấy tuần đầu con số rất "
         "nhỏ (1–3%). Đó là số ĐÚNG, và màn hình phải bày nó như vậy chứ không "
         "làm tròn cho đẹp."),
    ])

    # ── 3.4.9 ──────────────────────────────────────────────────────────────
    d.add_heading("3.4.9. Công nghệ sử dụng cho tầng chẩn đoán", level=2)
    bang(d,
        ["Thành phần", "Công nghệ", "Vì sao chọn", "Cái giá phải trả"],
        [
            ["Cập nhật mô hình", "Cloud Functions, kích hoạt theo tài liệu mới",
             "Chạy đúng một lần cho mỗi bản ghi; không phụ thuộc máy con còn mở "
             "hay không",
             "Có độ trễ giữa lúc trả lời và lúc mô hình cập nhật"],
            ["Nhất quán khi ghi", "Giao dịch của Firestore",
             "Hai lượt gần nhau cùng chạm một nút không làm mất cập nhật",
             "Chi phí ghi cao hơn ghi thường"],
            ["Duyệt đồ thị", "Chạy tại máy người học trên đồ thị rút gọn 127 KB",
             "Firestore không hỗ trợ truy vấn theo đồ thị; và ràng buộc R4 đòi "
             "chẩn đoán chạy được khi mất mạng",
             "Đồ thị phải đủ nhỏ, nên chỉ giữ quan hệ, không giữ chữ nghĩa"],
            ["Ngưỡng và tham số", "Hằng số khai ở MỘT tệp, các tệp khác nhập vào",
             "Hai nơi hai số là hai hệ thống khác nhau đội một tên",
             "Đổi tham số phải dựng lại và triển khai lại"],
            ["Kiểm chứng", "92 tệp kiểm chạy bằng node, không cần mạng",
             "Mọi thuật toán ở mục này là hàm thuần, kiểm được không cần cơ sở "
             "dữ liệu",
             "Hàm thuần đòi tách logic khỏi giao diện, tốn công thiết kế hơn"],
        ],
        ten="Bảng 3.21: Công nghệ của tầng chẩn đoán",
    )
