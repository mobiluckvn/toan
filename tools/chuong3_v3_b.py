#!/usr/bin/env python3
"""
CHƯƠNG 3 (bản viết lại) — phần B: mục 3.6 đến 3.10.

    3.6  VÍ DỤ MINH HOẠ ĐẦY ĐỦ — một phiên của một người học   (viết mới, trọng tâm)
    3.7  câu hỏi phản biện và chỗ trả lời                       (viết mới)
    3.8  hệ thống độ đo                                         (rút gọn mạnh)
    3.9  kịch bản thực nghiệm                                   (rút gọn mạnh)
    3.10 kết luận và giới hạn đã biết
"""
from __future__ import annotations

from chuong3_v3_khung import (
    SO, bang, canh_bao, cham, cong_thuc, do, doan, hinh, json_khoi, ma_lenh,
    sn, sv, thuat_toan,
)

H = SO["hangSo"]
KC = SO["khoCau"]
PD = SO["phuDao"]

# Mã máy → chữ đọc được. Bày mã máy ra cho người đọc luận văn là đúng lỗi mà
# chính mục 3.4.3 của chương này nêu ra cho giao diện.
VIEC = {"tiep": "tịnh tiến", "vuotAi": "vượt ải", "phuDao": "PHỤ ĐẠO"}
NAM = {"vung": "vững", "dangHoc": "đang học", "yeu": "yếu"}
DANG = {"chon": "chọn đáp án", "the": "xếp thẻ thành câu", "go": "gõ lại chữ",
        "tf": "đúng / sai", "nghenhin": "nghe rồi nhìn hình", "noi": "nói theo"}
NGUON = {"tinh": "tĩnh", "llm": "mô hình", "tron": "trộn"}


def _dap(chuoi):
    """{"choice":"colour"} → colour — bày đáp án chứ không bày cấu trúc dữ liệu."""
    import json as _j
    try:
        v = _j.loads(chuoi)
    except Exception:
        return chuoi
    if isinstance(v, dict):
        x = v.get("choice", v.get("value", v.get("the")))
        if isinstance(x, list):
            return " ".join(str(i) for i in x)
        return str(x)
    return str(v)


def viet(d):
    _m36(d)
    _m37(d)
    _m38(d)
    _m39(d)
    _m310(d)


# ═══════════════════════════════════════════════════════════ 3.6 ═══════════
def _m36(d):
    d.add_page_break()
    d.add_heading("3.6. Ví dụ minh hoạ: một phiên của một người học cụ thể", level=1)
    doan(d,
         "Năm mục trên trình bày thiết kế theo lối đặc tả. Mục này chạy toàn bộ "
         "thiết kế ấy trên MỘT phiên của MỘT người học, theo dõi từ trạng thái "
         "trước phiên tới bài phụ đạo được dựng ra và tới con số hiệu quả đo "
         "được, rồi nêu những gì phiên ấy đã ghi vào kho dữ liệu. Mục đích là "
         "làm cho mọi khái niệm ở trên trở thành một thứ kiểm chứng được từng "
         "bước.")
    canh_bao(d,
             "Phạm vi của bằng chứng, nêu trước để không bị đọc quá: NGƯỜI HỌC "
             "trong ví dụ là người học mô phỏng, và CHUỖI trả lời do tác giả "
             "đặt để minh hoạ đúng tình huống cần minh hoạ. Mọi thứ còn lại đều "
             "thật: đồ thị tri thức, kho câu hỏi, công thức, ngưỡng, lược đồ "
             "bản ghi, và toàn bộ con số mà hệ thống tính ra từ chuỗi ấy. Các "
             "bảng dưới đây do một chương trình sinh ra bằng cách gọi trực tiếp "
             "chính các mô-đun đang vận hành — hàm cập nhật Bayes của hàm nền, "
             "hàm định vị nút gốc rễ, hàm chính sách, hàm xếp câu theo vùng "
             "phát triển gần, hàm dựng bài phụ đạo và hàm dựng bản ghi — nên "
             "nếu công thức trong mã sai thì số trong luận văn sai theo.")

    # ── 3.6.1 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.1. Bối cảnh", level=2)
    bang(d, ["Hạng mục", "Giá trị"], [
        ["Người học", "M., lớp 3, đã học bốn bài trước đó trong ba tuần"],
        ["Bài học của phiên", "DL:TA3.B13 — Unit 13 · Ngôi nhà của mình · My house"],
        ["Số nút tri thức bài này chạm tới", f"{len(SO['nutCuaBai'])} nút "
         "(12 mục từ vựng và 2 mẫu câu)"],
        ["Kho câu hỏi của bài",
         "36 câu bậc khởi động · 7 câu bậc ráp câu · 14 câu bậc thử thách · "
         "5 câu sát hạch"],
        ["Mã phiên", SO["banGhiMau"]["sessionId"]],
        ["Số lượt trả lời trong phiên", f"{len(SO['luot'])} lượt"],
        ["Kết cục", "hệ thống phát hiện lỗ hổng ở lượt thứ 11 và dựng một bài "
         f"phụ đạo {len(PD['cau'])} câu nhắm vào một bài học khác"],
    ], ten="Bảng 3.16: Bối cảnh của phiên được minh hoạ")

    # ── 3.6.2 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.2. Trạng thái trước phiên", level=2)
    doan(d,
         "Trước khi mở bài, hồ sơ nút của người học này gồm sáu mẫu câu đã gặp "
         "ở bốn bài trước. Cột cuối cho thấy tác dụng của cơ chế quên: mọi giá "
         "trị đều bị kéo về phía 0,5 theo số ngày chưa gặp lại, và cả ba nút "
         "từng đạt ngưỡng tinh thông nay đều đã tụt xuống dưới ngưỡng.")
    bang(d, ["Nút", "Nhãn", "Bài dạy", "n / đúng", "P(L) lần gần nhất",
             "Số ngày cách", "P(L) sau phép quên"],
         [[x["ma"], x["nhan"], x["bai"], f"{x['n']} / {x['dung']}",
           sv(x["p"]) + (" ✔" if x["thao"] else ""), str(x["ngayCach"]),
           sv(x["pSauQuen"])] for x in SO["truocPhien"]],
         ten="Bảng 3.17: Hồ sơ nút tri thức của người học trước phiên "
             "(dấu ✔ = đã đạt ngưỡng θ = 0,85)")
    v = SO["vectorS"]
    bang(d, ["Chiều", "Nguồn dữ liệu", "Giá trị đầu phiên"], [
        ["C — Nhận thức", "trung bình P(L) của các nút trong bài, chỉ tính nút "
                          "đã có số liệu",
         f"«{NAM.get(v['mucNam'], '—')}»"],
        ["T — Thời gian", "lastSeen xa nhất trong các nút của bài",
         f"«{'có nguy cơ quên' if v['hayQuen'] else 'chưa tới ngưỡng quên'}»"],
        ["P — Sư phạm", f"hồ sơ định dạng, tối thiểu "
                        f"{SO['hanhVi']['toiThieuMau']} lượt mỗi định dạng",
         f"«{DANG.get(v['dangManh'], '—')}»"],
        ["M — Động lực", "chủ đề người học tự chọn, lưu ở học bạ",
         f"«{v['thich']}»"],
    ], ten="Bảng 3.18: Vectơ trạng thái S = [C, T, P, M] của người học lúc mở bài")
    doan(d,
         "Đúng bốn NHÃN này, không kèm số thô, là thứ được đóng gói vào lời "
         "nhắc gửi cho mô hình ngôn ngữ — theo ràng buộc đã nêu ở mục 3.4.4.")

    # ── 3.6.3 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.3. Diễn biến mười một lượt", level=2)
    doan(d,
         "Mỗi dòng của Bảng 3.19 là MỘT bản ghi trong kho nhật ký và đồng thời "
         "là MỘT lần hàm nền chạy cập nhật Bayes. Cột «π» là hành động mà hàm "
         "chính sách trả về ngay sau lượt ấy.")
    bang(d, ["Lượt", "Câu", "Nút được cập nhật", "Kết quả", "ms", "Gợi ý",
             "P(L) trước", "P(L) sau", "Δ", "S_c", "π"],
         [[str(i + 1), x["item"], x["nut"], "đúng" if x["dung"] else "SAI",
           sn(x["ms"]), str(x["goi"]), sv(x["pTruoc"]), sv(x["p"]),
           ("+" if x["delta"] >= 0 else "") + sv(x["delta"]),
           str(x["saiLienTiep"]), VIEC[x["viec"]]]
          for i, x in enumerate(SO["luot"])],
         ten="Bảng 3.19: Mười một lượt của phiên, chạy trên chính mã hàm nền",
         co_chu=8.5)
    hinh(d, "h5_pl_phien",
         "Hình 3.5: Diễn biến mức tinh thông qua mười một lượt; mỗi mũi tên là "
         "một lần cập nhật Bayes")
    doan(d,
         "Ba điều đáng đọc trong bảng. Thứ nhất, tám lượt đầu đều đúng nhưng "
         "không lượt nào đưa nút tương ứng lên ngưỡng tinh thông: một câu đúng "
         "từ trạng thái ban đầu chỉ nâng P(L) từ 0,100 lên 0,310, và mẫu câu "
         "sp_g3_u13_1 sau hai câu đúng mới đạt 0,608. Đó đúng là nhịp mà bộ "
         "tham số ở Bảng 3.12 được chọn để tạo ra — cần khoảng bốn câu đúng "
         "liên tiếp. Thứ hai, ba lượt sai ở cuối gần như không làm P(L) giảm "
         "thêm (0,100 → 0,094 → 0,093 → 0,093), vì giá trị đã sát sàn; điều "
         "này cho thấy vì sao mức tinh thông MỘT MÌNH không đủ để phát hiện "
         "tình trạng bế tắc, và vì sao cần tiêu chí TC1 đếm số lần sai liên "
         "tiếp. Thứ ba, cột π cho thấy hàm chính sách đã trả về PHỤ_ĐẠO ngay từ "
         "lượt thứ 9 theo tiêu chí TC2 (P(L) < θ_yếu), nhưng lý do đổi ở lượt "
         "thứ 11 sang «sai 3 lần liên tiếp» — tức TC1 kích hoạt, và TC1 mới là "
         "tiêu chí làm giao diện mời người học vào bài phụ đạo.")

    # ── 3.6.4 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.4. Phát hiện lỗ hổng: đối chiếu bốn tiêu chí", level=2)
    ho = SO["hoSoNutMau"]
    bang(d, ["Tiêu chí", "Điều kiện", "Giá trị đo được tại lượt 11", "Kết luận"], [
        ["TC1", f"S_c ≥ {H['saiLienTiepMac']}",
         f"S_c = {ho['saiLienTiep']}", "THOẢ — kích hoạt"],
        ["TC2", f"P(L) < {sv(H['thetaYeu'], 2)}",
         f"P(L) = {sv(ho['p'])}", "THOẢ"],
        ["TC3", "tồn tại tiên quyết chưa vững trong 4 bước",
         f"{len(SO['ungVien'])} ứng viên, trong đó "
         f"{len([x for x in SO['ungVien'] if x['loai'] != 'loai'])} nút chưa đạt ngưỡng",
         "THOẢ — phép định vị cho ra đích"],
        ["TC4", "bài học có ít nhất một nút mắc",
         f"π_bài trả về «{VIEC[SO['chinhSachBai']['viec']]}» — "
         f"{SO['chinhSachBai']['vi_sao']}", "THOẢ"],
    ], ten="Bảng 3.20: Bốn tiêu chí phát hiện lỗ hổng, đối chiếu trên phiên ví dụ")
    doan(d,
         "Cả bốn tiêu chí cùng thoả trong ví dụ này, nhưng chúng không phải một "
         "tiêu chí nói bốn lần. TC2 thoả từ lượt thứ 9 còn TC1 chỉ thoả ở lượt "
         "thứ 11 — nếu chỉ giữ TC1 thì hệ thống bỏ sót người học có mức tinh "
         "thông rất thấp mà chưa sai đủ ba lần liên tiếp trong phiên này; nếu "
         "chỉ giữ TC2 thì bỏ sót người học có mức tinh thông tàm tạm mà đang bế "
         "tắc thật. TC3 là điều kiện để phép định vị có nghĩa, và TC4 là điều "
         "kiện ở cấp bài học — nó quyết định khi cả bài chỉ có một nút mắc thì "
         "hệ thống gỡ nút ấy chứ không cho đi nhanh qua cả bài.")

    # ── 3.6.5 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.5. Định vị nguyên nhân", level=2)
    doan(d,
         "Phép duyệt ngược xuất phát từ mẫu câu sp_g3_u13_2 — «Where are the + "
         "[Furniture-plural]? - They're + [Preposition] + the room.» — trên tập "
         "cạnh tiên quyết, trần độ sâu 4, cho ra bảy ứng viên. Bảng 3.21 liệt "
         "kê TOÀN BỘ ứng viên trước khi lọc, để thấy phép xếp hạng hoạt động ra "
         "sao chứ không chỉ thấy kết quả.")
    bang(d, ["Nút", "Nhãn", "Bước", "P(L)", "doNgo = α^bước · (1 − P(L))",
             "Bài dạy nút", "Xử lý"],
         [[x["ma"], x["nhan"], str(x["buoc"]),
           sv(x["p"]) if x["p"] is not None else "chưa có số → 0,10",
           sv(x["doNgo"]), x["bai"] or "—", x["ghi_chu"]]
          for x in SO["ungVien"]],
         ten="Bảng 3.21: Bảy ứng viên nút gốc rễ và độ ngờ của từng ứng viên",
         co_chu=8.5)
    hinh(d, "h6_lan_truyen",
         "Hình 3.6: Độ ngờ của bảy ứng viên; ba nút đã đạt ngưỡng tinh thông bị "
         "loại khỏi danh sách")
    goc = SO["nutGocRe"][0]
    doan(d,
         f"Kết quả: nút gốc rễ là {goc['ma']} — «{goc['nhan']}» — dạy ở bài "
         f"{goc['bai']}, cách nút đang mắc {goc['buoc']} bước, với P(L) = "
         f"{sv(goc['p'])} và độ ngờ {sv(goc['doNgo'])}. Diễn giải sư phạm: "
         "người học không làm được câu hỏi «Where are the chairs? – They're in "
         "the room» KHÔNG phải vì chưa thuộc từ chỉ đồ vật (ba mục từ ấy đều "
         "vừa được nâng lên 0,310 trong chính phiên này), mà vì chưa vững mẫu "
         "câu SỐ NHIỀU «… are they? – They're …» học ở Unit 9. Luyện thêm câu "
         "của Unit 13 sẽ không gỡ được chỗ đó.")
    doan(d,
         "Hai chi tiết của phép xếp hạng đáng nêu vì chúng là chỗ một người đọc "
         "phản biện sẽ dừng lại. Thứ nhất, hai ứng viên sp_g3_u9_2 và "
         "sp_g3_u13_1 CÙNG cách nút mắc một bước, nên hệ số α^k bằng nhau và "
         "thứ hạng hoàn toàn do mức tinh thông quyết định: 0,374 so với 0,608, "
         "cho ra độ ngờ 0,375 so với 0,235. Thứ hai, ba nút sp_g3_u9_1, "
         "sp_g3_u8_1 và sp_g3_u3_1 bị LOẠI HẲN chứ không xếp hạng thấp, dù "
         "chúng nằm trên đường đi tới nút mắc — vì P(L) của chúng vượt ngưỡng "
         "tinh thông, và một nút người học làm đúng mãi thì không thể là thủ "
         "phạm.")

    # ── 3.6.6 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.6. Gợi ý can thiệp: bài phụ đạo được dựng ra", level=2)
    doan(d,
         f"Hệ thống gom câu có sẵn quanh nút gốc rễ, ưu tiên bậc độ khó thấp, "
         f"và tìm đủ {len(PD['cau'])} câu trong kho tĩnh của bài {PD['baiGoc']} "
         f"— nên nguồn là «{NGUON.get(PD['nguon'], PD['nguon'])}» và không phải "
         f"gọi mô hình ngôn ngữ, "
         f"cờ dự phòng bằng {'đúng' if PD['luiVe'] else 'sai'}. Bốn câu ấy là:")
    bang(d, ["Mã câu", "Bậc", "Nút đánh giá", "Đề bài", "Đáp án"],
         [[c["id"], str(c["bac"]), c["nut"], c["text"], _dap(c["dap"])]
          for c in PD["cau"]],
         ten=f"Bảng 3.22: Bốn câu của bài phụ đạo, lấy từ kho tĩnh của bài "
             f"{PD['baiGoc']}", co_chu=8.5)
    canh_bao(d,
             "Bốn câu này thuộc một BÀI HỌC KHÁC với bài người học đang mở. Đó "
             "chính là điểm phân biệt: một hệ thống chỉ thống kê tỷ lệ đúng — "
             "sai sẽ đưa thêm câu của Unit 13, còn hệ thống này lùi về Unit 9 "
             "vì đồ thị nói rằng chỗ hổng nằm ở đó.")
    doan(d,
         "Người học làm bài phụ đạo và đúng "
         f"{len([x for x in SO['dienBienPhuDao'] if x['dung']])} trên "
         f"{len(SO['dienBienPhuDao'])} câu. Diễn biến mức tinh thông tại nút gốc "
         "rễ:")
    bang(d, ["Câu phụ đạo", "Kết quả", "P(L) tại nút gốc rễ sau lượt"],
         [[x["item"], "đúng" if x["dung"] else "SAI", sv(x["p"])]
          for x in SO["dienBienPhuDao"]],
         ten="Bảng 3.23: Diễn biến mức tinh thông tại nút gốc rễ trong bài phụ đạo")
    dc = SO["deltaCGoc"]
    doan(d,
         f"Biến thiên tri thức tại nút gốc rễ: {sv(dc['truoc'])} → "
         f"{sv(dc['sau'])}, tức ΔC = +{sv(dc['delta'])}. Nút gốc rễ vượt ngưỡng "
         "tinh thông ngay trong lần can thiệp này. Một hệ quả trực tiếp đáng "
         "nêu: nếu chạy lại phép định vị ngay sau đó, nút gốc rễ của cùng một "
         "thất bại sẽ KHÁC — vì sp_g3_u9_2 nay đã vượt ngưỡng nên bị loại khỏi "
         "danh sách, và đích chuyển sang ứng viên xếp sau. Chẩn đoán vì vậy là "
         "một hàm của trạng thái hiện tại chứ không phải một nhãn dán vĩnh viễn.")

    # ── 3.6.7 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.7. Đo hiệu quả: ΔC và điều kiện hợp lệ của phép đo", level=2)
    doan(d,
         "ΔC ở mục trên đo tại nút GỐC RỄ. Muốn kết luận bài phụ đạo có giúp "
         "người học gỡ được chỗ đang mắc hay không thì phải đo lại tại nút MẮC, "
         "theo giao thức Đánh giá → Can thiệp → Đánh giá lại. Phép đo ấy chỉ có "
         "nghĩa khi lần đo sau dùng những câu hỏi KHÁC lần đo trước; hỏi lại "
         "đúng mấy câu vừa chữa là đo trí nhớ ngắn hạn chứ không đo hiểu bài, "
         "và sai theo hướng ĐẸP LÊN — mọi bài phụ đạo đều trông như hiệu quả, "
         "kể cả bài vô dụng.")
    thuat_toan(
        d, "3.6", "Kiểm tra tính hợp lệ của một cặp đo trước — sau",
        "một cặp gồm hai lần đo, mỗi lần có mức tinh thông và danh sách mã câu "
        "đã hỏi; tên mẫu lời nhắc và số phiên bản.",
        "kết luận hợp lệ hay không, kèm lý do khi không hợp lệ.",
        [
            "1  if thiếu mức tinh thông ở một trong hai lần đo:",
            "2      return (false, «thiếu mức nắm»)",
            "3  if một trong hai danh sách câu rỗng:",
            "4      return (false, «thiếu danh sách câu đã hỏi»)",
            "5  trùng ← câu_sau ∩ câu_trước",
            "6  if trùng ≠ ∅:                      // ĐIỀU KIỆN QUYẾT ĐỊNH",
            "7      return (false, «lần đo sau dùng lại câu của lần trước»)",
            "8  return (true, «»)",
        ])
    bang(d, ["Cặp đo", "Câu lần trước", "Câu lần sau", "Kết luận của Thuật toán 3.6",
             "ΔC"], [
        ["Cặp A — dùng lại câu cũ", "S5 · S6 · S7", "S5 · S7",
         SO["ara"]["capTrung"]["vi"], "không tính"],
        ["Cặp B — câu hoàn toàn mới", "S5 · S6 · S7", "G1 · G2",
         "hợp lệ", "+" + sv(SO["ara"]["capSach"]["deltaC"])],
    ], ten="Bảng 3.24: Hai cặp đo trước — sau và kết luận của phép kiểm hợp lệ")
    canh_bao(d,
             "Ví dụ này phơi ra một ràng buộc thật của kho học liệu: nút đang "
             f"mắc chỉ có đúng {SO['ara']['soCauCuaNutMac']} câu hỏi trong toàn "
             "bộ bài học, và cả ba đã bị dùng ở lần đo trước. Với riêng nút "
             "này, một cặp đo hợp lệ KHÔNG dựng được từ kho tĩnh — phải có câu "
             "sinh thêm. Đây chính là một trong ba vị trí mà mô hình ngôn ngữ "
             "được phép tham gia theo tiêu chí ở mục 3.5.3, và cũng là lý do "
             "phải có tầng hậu kiểm riêng cho câu hỏi trước khi bật vị trí ấy.")
    doan(d,
         f"Trên toàn bộ kho — {sn(KC['tong'])} câu hỏi gắn với "
         f"{sn(KC['nutCoCau'])} nút — có {sn(KC['nutDuoi4Cau'])} nút mang dưới "
         "bốn câu hỏi, tức khoảng "
         f"{sv(KC['nutDuoi4Cau'] / KC['nutCoCau'] * 100, 1)} %. Với "
         f"{sn(KC['nutCoCau'] - KC['nutDuoi4Cau'])} nút còn lại, một cặp đo hợp "
         "lệ dựng được ngay từ kho tĩnh. Con số này phải được công bố kèm mọi "
         "kết quả ΔC, vì nó quyết định phép đo áp dụng được cho phần nào của "
         "kho học liệu.")

    # ── 3.6.8 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.8. Hai con số trình bày cho người lớn", level=2)
    doan(d,
         "Kết quả của phiên được chuyển thành hai thứ người lớn đọc được. Thứ "
         "nhất là ma trận trạng thái đồ thị: mỗi dòng là một nút người học đang "
         "gặp khó khăn, kèm nút gốc rễ tương ứng — nghĩa là không phải “em này "
         "sai 3 câu” mà “em này mắc ở mẫu câu Unit 13, mà gốc là mẫu câu số "
         "nhiều Unit 9”.")
    bang(d, ["Nút đang gặp khó khăn", "P(L)", "Nút gốc rễ", "Khoảng cách"],
         [[r["nhan"], sv(r["p"]),
           (r["goc"]["nhan"] if r.get("goc") else "— không có tiên quyết nào"),
           (f"{r['goc']['buoc']} bước · P(L) = {sv(r['goc']['p'])}"
            if r.get("goc") else "—")]
          for r in SO["maTran"]],
         ten="Bảng 3.25: Ma trận trạng thái đồ thị sau phiên, năm dòng đầu")
    doan(d,
         "Thứ hai là mức phủ vốn tri thức, quy đổi bắc cầu hai nhịp: từ P(L) "
         "của từng nút sang phần trăm phủ vốn của một khối lớp (nhịp hệ thống "
         "ĐO ĐƯỢC), rồi từ khối lớp sang bậc năng lực (nhịp là QUY ƯỚC do "
         "Chương trình giáo dục phổ thông 2018 ấn định, không phải phép đo của "
         "phần mềm).")
    cong_thuc(d,
              "phủ(b) = | { v ∈ V_học_được : khối(v) = b ∧ P(L_v) ≥ θ } |  /  "
              "| { v ∈ V_học_được : khối(v) = b } |")
    bang(d, ["Khối", "Lớp", "Nút đã vững / tổng nút học được", "% phủ",
             "Đủ tin cậy", "Công nhận bậc"],
         [[b["ma"], b["moTa"], f"{b['vung']} / {sn(b['tong'])}",
           sv(b["phu"] * 100, 1) + " %",
           "Có" if b["dangTin"] else f"Không — dưới {SO['phuVon']['toiThieuNut']} nút",
           "Có" if b["dat"] else "Chưa"]
          for b in SO["phuVon"]["banDo"]],
         ten="Bảng 3.26: Mức phủ vốn tri thức theo khối lớp sau phiên")
    doan(d,
         f"Câu mà giao diện hiển thị: «{SO['phuVon']['cau']}» — con số 0 % "
         "trong câu ấy là do giao diện làm tròn tới phần trăm nguyên, giá trị "
         f"thật là {sv(SO['phuVon']['banDo'][1]['phu'] * 100, 1)} %; đây là một "
         "chỗ cần sửa ở tầng hiển thị, đã ghi vào Bảng 3.32. Ba lựa chọn trong "
         "phép quy đổi này cần được bảo vệ khi phản biện, nên nêu tường minh: "
         f"ngưỡng phủ {sv(SO['phuVon']['phuDat'], 2)} để công nhận một bậc là "
         "một LỰA CHỌN — đòi 100 % thì không người học nào đạt, vì đồ thị chứa "
         "cả nút chưa có bài dạy, còn hạ xuống dưới 0,50 thì “đạt” được công "
         f"nhận trong khi quá nửa vốn chưa nắm; ngưỡng tin cậy "
         f"{SO['phuVon']['toiThieuNut']} nút chặn con số vô nghĩa ở khối lớp 6 "
         "vốn chỉ có bốn nút bắc cầu; và mẫu số là TOÀN BỘ vốn của khối chứ "
         "không phải số nút đã tiếp cận — lấy mẫu số là số nút đã tiếp cận thì "
         "một người học mới học năm nút và nắm cả năm sẽ ra 100 %, tức phép đo "
         "thưởng cho việc học ít. Hệ quả phải chấp nhận là trong những tuần đầu "
         "con số rất nhỏ. Đó là con số đúng, và giao diện phải trình bày đúng "
         "như vậy.")

    # ── 3.6.9 ────────────────────────────────────────────────────────────
    d.add_heading("3.6.9. Phiên kế tiếp: thứ tự câu hỏi đã đổi", level=2)
    doan(d,
         "Buổi học sau, người học mở lại bài. Lúc này sáu mục từ vựng đã có số "
         "liệu còn bốn mục chưa, nên phép xếp theo vùng phát triển gần đổi thứ "
         "tự mười câu đầu của chặng bậc một:")
    z = SO["xepZPD"]
    doan(d, "Thứ tự người soạn đặt: " + " → ".join(z["goc"])
            + ".   Thứ tự sau khi xếp lại: " + " → ".join(z["sau"]) + ".")
    bang(d, ["Thứ tự mới", "Câu", "Nút", "P(L)", "Nhóm"],
         [[str(r["thuTu"]), r["item"], r["nut"],
           sv(r["p"]) if r["p"] is not None else "—", r["nhom"]]
          for r in z["dong"]],
         ten="Bảng 3.27: Thứ tự câu hỏi sau khi xếp lại theo vùng phát triển gần")
    doan(d,
         "Bốn câu thuộc nhóm chưa có số liệu bị đẩy xuống sau sáu câu thuộc "
         "nhóm đang chông chênh, đúng theo Bảng 3.15. Không câu nào bị loại bỏ "
         "và không câu nào của bậc khác bị trộn vào — tổng số câu giữ nguyên, "
         "nên sổ tiến độ, thanh đếm câu và phép chấm không bị lệch.")

    # ── 3.6.10 ───────────────────────────────────────────────────────────
    d.add_heading("3.6.10. Phiên này đã ghi lại những gì", level=2)
    bang(d, ["Kho", "Số bản ghi của phiên", "Nội dung"], [
        ["attempts", f"{len(SO['luot'])} bản ghi (bất biến)",
         "mỗi lượt trả lời một dòng, mã nhúng phiên và số thứ tự"],
        ["mastery", f"{len(set(x['nut'] for x in SO['luot']))} tài liệu được ghi "
                    "đè trong giao dịch",
         "P(L) mới, pTruoc, các biến đếm, thời gian phản hồi trung bình, "
         "số gợi ý, mốc tương tác gần nhất"],
        ["progressTA", "1 tài liệu",
         "kết quả cuối bài — phiên này chưa tới chặng sát hạch nên bài ở trạng "
         "thái đang dở"],
        ["hocBaTA", "1 mục loại «phudao»",
         "khung đo trước — sau: nút mắc, nút gốc rễ, danh sách câu đã hỏi "
         "trước, danh sách câu phụ đạo, hai mốc thời gian"],
    ], ten="Bảng 3.28: Bốn kho và số bản ghi mà phiên ví dụ sinh ra")
    doan(d, "Mục học bạ loại «phudao» của phiên này, nguyên văn:")
    json_khoi(d, SO["khungARA"])
    canh_bao(d,
             "Khung này CỐ Ý không chứa mức tinh thông trước và sau. Máy người "
             "học chỉ có bản hồ sơ nút nạp lúc mở bài, mà hàm nền cập nhật sau "
             "một quãng trễ — ghi con số cũ vào thì ΔC sai theo hướng không ai "
             "lần ra. Hai lần đo được dựng lại ngoại tuyến bằng phép chạy lại "
             "nhật ký, đúng nguyên tắc “mô hình người học phải suy ra được từ "
             "nhật ký” của bất biến B3.")

    # ── 3.6.11 ───────────────────────────────────────────────────────────
    d.add_heading("3.6.11. Bốn điều ví dụ này phơi ra", level=2)
    doan(d,
         "Một ví dụ chạy trên hệ thống thật có giá trị riêng: nó phơi ra những "
         "chỗ mà đặc tả không nói. Bốn điều dưới đây được phát hiện khi dựng "
         "chính ví dụ này, và cả bốn đều được nêu lại ở mục 3.10.")
    hv = SO["hanhVi"]["metMoi"]
    cham(d, [
        ("Kho câu hỏi mỏng ở một số nút. ",
         f"{sn(KC['nutDuoi4Cau'])} trên {sn(KC['nutCoCau'])} nút có dưới bốn "
         "câu hỏi, nên với những nút ấy giao thức đo trước — sau không dựng "
         "được cặp hợp lệ từ kho tĩnh (mục 3.6.7)."),
        ("Nút gốc rễ đổi sau can thiệp. ",
         "Sau khi bài phụ đạo đưa nút gốc rễ vượt ngưỡng, phép định vị cùng "
         "một thất bại sẽ trả về một đích khác. Đây là hành vi ĐÚNG, nhưng nó "
         "có nghĩa là báo cáo cho phụ huynh phải kèm mốc thời gian, và hai báo "
         "cáo ở hai thời điểm khác nhau có thể trỏ vào hai nút khác nhau mà "
         "không mâu thuẫn."),
        ("Phép nhận biết mệt mỏi dương tính giả trên chính phiên này. ",
         f"Chạy phép đo trên nhật ký của phiên: thời gian phản hồi trung bình "
         f"nửa đầu {sn(hv['msDau'])} ms, nửa cuối {sn(hv['msCuoi'])} ms, chênh "
         f"{int(hv['chamHon'] * 100)} % — vượt ngưỡng 25 % nên cờ mệt mỏi bật. "
         "Nhưng phần chênh ấy KHÔNG thuộc về người học: phép đo gom theo ĐỊNH "
         "DẠNG để loại trừ ảnh hưởng của độ khó, mà ở đây cả mười một lượt đều "
         "cùng một định dạng «chọn đáp án» trong khi bậc độ khó thì tăng từ "
         "khởi động lên ráp câu. Phép gom theo định dạng chưa đủ khi một định "
         "dạng trải qua nhiều bậc; phải gom theo BỘ ĐÔI (định dạng, bậc). Đây "
         "là một sửa đổi cụ thể mà ví dụ này chỉ ra và mục 3.10 ghi nhận."),
        ("Nút gốc rễ có thể không có bài dạy. ",
         "Khi chạy phép định vị trên toàn bộ nhóm nút có cạnh tiên quyết đi "
         "vào, có 19 trường hợp nút gốc rễ không được bài học nào dạy — đó là "
         "các nút bắc cầu xuyên khối lớp, tồn tại để cạnh tiên quyết có chỗ neo "
         "chứ không có học liệu tương ứng. Hệ thống xử lý đúng ở tầng giao diện "
         "— không dựng được bài phụ đạo thì mời người học đi tiếp, không có màn "
         "trắng — nhưng con số này phải được nêu riêng khi báo cáo kết quả chẩn "
         "đoán."),
    ])


# ═══════════════════════════════════════════════════════════ 3.7 ═══════════
def _m37(d):
    d.add_heading("3.7. Những câu hỏi phản biện và chỗ trả lời", level=1)
    doan(d,
         "Thiết kế ở các mục trên có một số chỗ mà người đọc phản biện sẽ dừng "
         "lại. Bảng 3.29 tập hợp những câu hỏi ấy cùng câu trả lời ngắn và chỗ "
         "dẫn chứng, để việc bảo vệ không phải dựng lại lập luận từ đầu.")
    bang(d, ["Câu hỏi", "Trả lời ngắn", "Dẫn chứng"], [
        ["Đồ thị tri thức được làm ra bằng cách nào — tự động sinh hay khai tay?",
         "Khai tay theo sách giáo khoa và Chương trình 2018, qua sáu bước, mỗi "
         "bước để lại một con số kiểm chứng được. Quan hệ tiên quyết là phán "
         "đoán sư phạm nên được khai tay có chủ đích.", "Mục 3.2.1, Hình 3.2"],
        ["Bao nhiêu nút thì đủ, và con số ấy so với tài liệu ra sao?",
         f"{sn(SO['doThi']['nut'])} đỉnh lúc chạy, trong đó "
         f"{sn(SO['doThi']['hocDuoc'])} đỉnh học được. Lớn hơn các tập dữ liệu "
         "theo dõi tri thức thường dẫn vì đơn vị phân rã là một mục từ vựng "
         "hoặc một mẫu câu, không phải một “kỹ năng”.", "Bảng 3.3 và diễn giải"],
        ["Mỗi đỉnh mang những thuộc tính gì?",
         "18 trường cho đỉnh từ vựng và 9–10 trường cho đỉnh mẫu câu, mỗi "
         "trường có một nơi tiêu thụ xác định.", "Bảng 3.5"],
        ["Trên máy, tập đỉnh và tập cạnh nằm ở bảng nào?",
         "Ba dạng ở ba chặng: bảng khai (5 tệp chuẩn), đồ thị đầy đủ, đồ thị "
         "lúc chạy. Đỉnh lưu dạng từ điển, cạnh lưu dạng danh sách.",
         "Bảng 3.7"],
        ["Mệnh đề điều kiện nào quyết định cạnh nào được dùng để chẩn đoán?",
         "E_prereq = { e : λ(e) ∈ {ban_do, noi_bai} }, đặt làm MẶC ĐỊNH; muốn "
         "lấy cạnh thứ tự đọc phải yêu cầu tường minh.",
         "Mục 3.2.4 và Thuật toán 3.2 dòng 1"],
        ["Một phiên của một cá nhân lưu những thông tin gì, và lưu thế nào?",
         "Bốn kho, khác nhau ở nhịp ghi và chủ thể ghi; nhật ký lượt trả lời "
         "bất biến là nguồn gốc, ba kho còn lại suy ra được từ nó.",
         "Hình 3.4, Bảng 3.8, Bảng 3.9, Bảng 3.28"],
        ["Căn cứ nào để nói dữ liệu ấy đáng tin?",
         "Bốn bất biến kiểm được bằng chương trình, chạy trước và sau mỗi đợt "
         "thu dữ liệu; kèm phát biểu rõ về điều mà chúng KHÔNG phát hiện được.",
         "Bảng 3.10 và cảnh báo kèm theo"],
        ["Tiêu chí nào để nói có một lỗ hổng?",
         "Bốn tiêu chí TC1–TC4, kèm định nghĩa hình thức của “lỗ hổng gốc rễ”. "
         "TC1 và TC2 độc lập với nhau và cần cả hai.",
         "Bảng 3.11, đối chiếu ở Bảng 3.20"],
        ["Vì sao tin rằng nút được chỉ ra đúng là nguyên nhân?",
         "Không tin tuyệt đối — đó là một GIẢ THUYẾT được xếp hạng, và giao "
         "thức đo trước — sau tồn tại để kiểm chứng giả thuyết ấy bằng số.",
         "Mục 3.6.5 và 3.6.7"],
        ["Nếu mô hình chấm sai thì người học có bị kẹt không?",
         "Không. Hàm chính sách chỉ khuyến nghị; quyền mở đường học thuộc một "
         "bộ luật riêng với lưới an toàn “đã đạt hoặc đã thử thật hai lần”.",
         "Mục 3.5.1"],
        ["Con số phủ vốn có phải là điểm CEFR không?",
         "Không. Nhịp thứ hai của phép quy đổi là quy ước của Chương trình "
         "2018, không phải phép đo của phần mềm; giao diện phải nói đúng như vậy.",
         "Mục 3.6.8"],
        ["Mô hình ngôn ngữ có thể dạy sai không?",
         "Có, nên nó chỉ được gọi ở ba vị trí thoả đồng thời ba điều kiện, và "
         "mọi câu sinh ra đều phải qua một hàm hậu kiểm tất định chạy tại máy "
         "người học.", "Mục 3.5.3 và Thuật toán 3.5"],
        ["Kết quả trong luận văn có tái lập được không?",
         "Mọi số liệu ở mục 3.6 do một chương trình sinh ra bằng cách gọi chính "
         "các mô-đun đang vận hành; chạy lại chương trình ấy cho ra đúng các "
         "bảng trong chương.", "Cảnh báo đầu mục 3.6"],
    ], ten="Bảng 3.29: Mười ba câu hỏi phản biện điển hình và chỗ trả lời",
        co_chu=8.5)


# ═══════════════════════════════════════════════════════════ 3.8 ═══════════
def _m38(d):
    d.add_heading("3.8. Hệ thống độ đo đánh giá", level=1)
    doan(d,
         "Một hệ thống học tập thích ứng sử dụng trí tuệ nhân tạo tạo sinh phải "
         "trả lời bốn câu hỏi độc lập, và mỗi câu hỏi đòi một nhóm độ đo riêng. "
         "Việc gộp chúng vào một chỉ số tổng hợp sẽ che mất chính những điểm "
         "cần quan sát.")
    bang(d, ["Nhóm", "Câu hỏi cần trả lời", "Độ đo chính", "Phương pháp đo"], [
        ["A — mô hình người học",
         "mô hình dự đoán hành vi người học có chính xác không?",
         "AUC, RMSE, độ chính xác, sai lệch hiệu chuẩn theo 10 nhóm",
         "chạy lại nhật ký, dùng trạng thái sau lượt n−1 dự đoán lượt n"],
        ["B — tiến bộ và hiệu quả can thiệp",
         "người học có tiến bộ không, và can thiệp có hiệu quả không?",
         "độ dốc đường cong học tập, ΔC theo mẫu lời nhắc, số lượt tới tinh "
         "thông, mức phủ vốn",
         "phân tích nhật ký và hồ sơ nút; giao thức đo trước — sau"],
        ["C — an toàn nội dung",
         "tầng chống ảo giác từ vựng ngăn chặn được bao nhiêu?",
         "tỷ lệ từ ngoài vốn trước và sau hậu kiểm, tỷ lệ bị bác bỏ theo từng "
         "đường công nhận, tỷ lệ dùng phương án dự phòng, tỷ lệ lặp câu",
         "bộ chứng dựng sẵn, đối chiếu tự động, phép thử đảo chiều"],
        ["D — hệ thống và vận hành",
         "hệ thống vận hành có đúng và kịp thời không?",
         "tỷ lệ lượt ghi thành công, số bản ghi tồn đọng, độ trễ đầu — cuối, "
         "bốn bất biến",
         "đo trên bản chạy thật và rà soát kho dữ liệu"],
    ], ten="Bảng 3.30: Bốn nhóm độ đo")
    doan(d,
         "Ba độ đo có định nghĩa riêng cần nêu vì chúng quyết định giá trị của "
         "cả hệ thống đánh giá.")
    cham(d, [
        ("Sai lệch hiệu chuẩn (nhóm A) — ", "chia các lượt thành mười nhóm theo "
         "xác suất dự đoán, trong mỗi nhóm so xác suất trung bình với tỷ lệ "
         f"đúng thực tế. Đây là độ đo quan trọng nhất với hệ thống này: ngưỡng "
         f"θ = {sv(H['theta'], 2)} chỉ có nghĩa nếu phát biểu “mô hình dự đoán "
         "85 %” thực sự tương ứng với “trả lời đúng khoảng 85 % số lần”."),
        ("ΔC theo mẫu lời nhắc (nhóm B) — ", "trung bình biến thiên tri thức "
         f"của các cặp đo hợp lệ; cần tối thiểu {H['toiThieuCapARA']} cặp mới "
         "công bố một con số, và PHẢI công bố kèm số cặp bị loại. Một mẫu có 40 "
         "cặp mà 35 cặp bị loại thì trung bình của 5 cặp còn lại không đáng "
         "tin, và người đọc cần biết điều đó."),
        ("Tỷ lệ từ ngoài vốn sau hậu kiểm (nhóm C) — ", "phải bằng 0 theo thiết "
         "kế. Đây là một phát biểu KIỂM CHỨNG ĐƯỢC, khác hẳn phát biểu “lời "
         "nhắc bảo đảm 100 % không có từ lạ” vốn không kiểm chứng được. Nếu một "
         "phép đo cho ra giá trị khác 0 thì đó là lỗi của hàm hậu kiểm và định "
         "vị được ngay ở một trong năm đường công nhận của Thuật toán 3.5."),
    ])
    doan(d,
         "Nhóm D thường bị bỏ qua trong tài liệu về học tập thích ứng, nhưng ở "
         "đây được đặt ngang hàng với ba nhóm còn lại, vì mọi kết luận của ba "
         "nhóm kia đều đứng trên một giả định: nhật ký đầy đủ và đúng chủ sở "
         "hữu. Giả định ấy có thể sai mà không phát ra dấu hiệu nào — trong quá "
         "trình phát triển đã có giai đoạn tỷ lệ lượt ghi thành công chỉ đạt "
         "khoảng một phần mười mà không phép kiểm nào phát hiện.")


# ═══════════════════════════════════════════════════════════ 3.9 ═══════════
def _m39(d):
    d.add_heading("3.9. Kịch bản thực nghiệm đề xuất", level=1)
    doan(d,
         "Sáu kịch bản dưới đây xếp theo chi phí tăng dần và mức độ phụ thuộc "
         "vào người học thật tăng dần. Thứ tự có chủ đích: kết quả của kịch bản "
         "trước dùng để hiệu chỉnh tham số cho kịch bản sau, và đưa một hệ "
         "thống chưa hiệu chỉnh vào lớp học thật thì vừa tốn kém vừa khó lý "
         "giải kết quả.")
    bang(d, ["Mã", "Mục tiêu", "Giả thuyết chính", "Thiết kế", "Nhóm độ đo",
             "Mức sẵn sàng"], [
        ["KB1", "hiệu chỉnh bộ tham số và nửa đời trí nhớ bằng mô phỏng",
         "tồn tại bộ tham số sao cho θ tương ứng khoảng bốn câu đúng liên tiếp "
         "và một câu sai kéo tụt xuống dưới ngưỡng; kết quả hàm chính sách nhạy "
         "với θ hơn với α và β",
         "1.000 người học mô phỏng, quét lưới θ × α × β × h; tham số thật của "
         "người học mô phỏng khác tham số của mô hình",
         "A, B", "Cao — mọi thuật toán ở mục 3.4 là hàm thuần, chạy được không "
                 "cần mạng và không cần cơ sở dữ liệu"],
        ["KB2", "so sánh bốn biến thể mô hình trên nhật ký thật",
         "mô hình có cơ chế quên dự đoán tốt hơn mô hình chuẩn, và chênh lệch "
         "lớn hơn ở những lượt cách lần trước từ 7 ngày; lan truyền trên đồ thị "
         "cải thiện dự đoán ở nhóm nút có tiên quyết",
         "kiểm chéo năm phần chia theo NGƯỜI HỌC; phân tầng theo nhóm nút và "
         "theo khoảng cách thời gian; kiểm định DeLong cho AUC",
         "A, B, D", "Công cụ đã viết và tự kiểm; chờ đủ dữ liệu thật"],
        ["KB3", "định lượng đóng góp của tầng hậu kiểm, tách khỏi đóng góp của "
                "lời nhắc",
         "lời nhắc đứng một mình không bảo đảm được việc không có từ ngoài vốn; "
         "sau hậu kiểm tỷ lệ vi phạm bằng 0",
         "30 bài trải đều năm quyển × 20 lượt gọi × 3 vị trí; ghi lại đầu ra "
         "thô và kết quả sau hậu kiểm; PHÉP THỬ ĐẢO CHIỀU tắt lần lượt từng "
         "đường công nhận",
         "C, D", "Bộ đo đã viết; chế độ đo đã chạy; chế độ gọi mô hình thật cần "
                 "khoá dịch vụ"],
        ["KB4", "so sánh hiệu quả các mẫu lời nhắc bằng ΔC",
         "các mẫu khác nhau cho ΔC trung bình khác nhau có ý nghĩa thống kê",
         "phân bổ ngẫu nhiên mẫu ở mỗi lần kích hoạt phụ đạo; lọc cặp hợp lệ "
         "bằng Thuật toán 3.6; kiểm định t hai mẫu hoặc Mann-Whitney",
         "B, C", "Bị chặn — vị trí gọi mô hình cho bài phụ đạo còn trống "
                 "(mục 3.5.3)"],
        ["KB5", "kiểm chứng hiệu quả của cơ chế xếp câu theo vùng phát triển gần",
         "nhóm có xếp lại đạt mức tinh thông trung bình cao hơn sau cùng một số "
         "lượt, và có tỷ lệ bỏ dở thấp hơn",
         "thử nghiệm đối chứng ngẫu nhiên trong hệ thống, phân tầng theo khối "
         "lớp và mức phủ vốn ban đầu, tối thiểu bốn tuần; hồi quy đa mức",
         "B, D", "Sẵn sàng về mã; cần thêm một cờ phân nhóm ngẫu nhiên"],
        ["KB6", "đánh giá hệ thống trong điều kiện sử dụng thực tế",
         "người học có tiến bộ đo được; hệ thống ghi nhận đầy đủ hành vi, tức "
         "bốn bất biến được giữ và tỷ lệ ghi thành công gần 100 %",
         "5–10 học sinh ở hai khối lớp, bốn tuần, ít nhất ba phiên mỗi tuần; "
         "ĐO ĐẦU VÀ CUỐI bằng bài kiểm tra trên giấy do giáo viên soạn, không "
         "dùng câu hỏi của hệ thống",
         "A, B, C, D", "Sẵn sàng về kỹ thuật; phần khó là tổ chức"],
    ], ten="Bảng 3.31: Sáu kịch bản thực nghiệm", co_chu=8.0)
    doan(d,
         "Ba điều kiện tiền đề phải thoả trước khi tiến hành bất kỳ kịch bản "
         "nào. Thứ nhất, mốc dữ liệu: chỉ sử dụng dữ liệu thu được sau ngày "
         "đường ống ghi nhận được khắc phục, vì trước mốc ấy mỗi phiên học chỉ "
         "có bản ghi đầu tiên lên được máy chủ. Thứ hai, bốn bất biến ở Bảng "
         "3.10 phải được chạy trước và sau mỗi đợt thu dữ liệu; một đợt vi phạm "
         "bất kỳ bất biến nào đều bị loại khỏi phân tích cho tới khi xác định "
         "được nguyên nhân. Thứ ba, đạo đức nghiên cứu: người tham gia là trẻ "
         "em nên cần sự đồng ý của phụ huynh; dữ liệu báo cáo phải được ẩn "
         "danh; bảng xếp hạng hiển thị cho trẻ chỉ chứa biệt danh, khối lớp và "
         "số điểm thưởng.")
    doan(d,
         "Thứ tự triển khai đề xuất gồm ba đợt. Đợt một chạy KB1 và KB3 — cả "
         "hai không cần người học thật, cho kết quả nhanh, và kết quả của chúng "
         "là điều kiện để các đợt sau có nghĩa. Đợt hai chạy KB6 với người học "
         "thật, KB5 và KB4 lồng bên trong dưới dạng phân bổ ngẫu nhiên. Đợt ba "
         "chạy KB2 trên dữ liệu mà KB6 đã tích luỹ được.")


# ══════════════════════════════════════════════════════════ 3.10 ═══════════
def _m310(d):
    d.add_heading("3.10. Kết luận chương và giới hạn đã biết", level=1)
    doan(d,
         "Chương này đã chuyển cơ sở lý thuyết của Chương 2 thành một thiết kế "
         "cụ thể, với bốn nhóm kết quả.")
    cham(d, [
        ("Biểu diễn tri thức (mục 3.2). ",
         "Đồ thị tri thức được đặc tả đầy đủ trên ba mặt mà một thiết kế phải "
         "nêu: quy trình thành hình sáu bước kèm số liệu từng bước; định nghĩa "
         "hình thức G = (V, E, τ, λ) cùng quy mô đặt bên cạnh tài liệu đã công "
         "bố; và cài đặt trên máy — tập đỉnh lưu dạng từ điển, tập cạnh lưu "
         "dạng danh sách, hai phép truy vấn cơ bản kèm mệnh đề điều kiện lọc "
         "theo nhãn cạnh. Nhãn cạnh được lập luận là điều kiện ĐÚNG ĐẮN chứ "
         "không phải chi tiết kỹ thuật."),
        ("Biểu diễn phiên của một cá nhân (mục 3.3). ",
         "Một phiên được định nghĩa thao tác được — một lần mở bài — và ghi vào "
         "bốn kho khác nhau ở nhịp ghi và chủ thể ghi, với lược đồ đầy đủ của "
         "hai kho quan trọng nhất kèm bản ghi thật nguyên văn. Quyền ghi và "
         "quyền đọc được khai bằng mệnh đề điều kiện ở tầng cơ sở dữ liệu, và "
         "tính toàn vẹn được phát biểu thành bốn bất biến kiểm được bằng chương "
         "trình."),
        ("Chẩn đoán và gợi ý (mục 3.4 và 3.5). ",
         "Bốn tiêu chí phát hiện lỗ hổng được phát biểu tường minh cùng định "
         "nghĩa hình thức của “lỗ hổng gốc rễ”; sáu tình trạng và luật nhận "
         "dạng của chúng tạo thành toàn bộ không gian trạng thái mà tầng thích "
         "ứng phân biệt được; sáu thuật toán đặc tả đầy đủ đầu vào, đầu ra và "
         "thủ tục. Hai đóng góp thiết kế đáng nêu riêng: ranh giới quyền quyết "
         "định — hàm chính sách khuyến nghị, nhưng quyền mở đường học thuộc một "
         "bộ luật riêng có lưới an toàn; và bảo đảm hai tầng cho ràng buộc vốn "
         "từ — lời nhắc định hướng, còn hậu kiểm tất định mới tạo ra một phát "
         "biểu kiểm chứng được."),
        ("Minh chứng vận hành (mục 3.6). ",
         "Toàn bộ thiết kế được chạy trên một phiên cụ thể, từ trạng thái trước "
         "phiên tới bài phụ đạo và con số hiệu quả, với mọi bảng do chương "
         "trình sinh ra bằng cách gọi chính các mô-đun đang vận hành. Ví dụ ấy "
         "vừa minh hoạ cơ chế, vừa phơi ra bốn hạn chế mà đặc tả không nói."),
    ])
    doan(d,
         "Bảng 3.32 tập hợp những giới hạn đã biết của thiết kế ở thời điểm "
         "viết, kèm hướng xử lý. Nêu chúng ở đây là có chủ đích: một luận văn "
         "chỉ nêu phần chạy được thì không cho người đọc cách kiểm chứng phần "
         "còn lại.")
    bang(d, ["Giới hạn", "Ảnh hưởng", "Hướng xử lý"], [
        ["Lan truyền xuôi đã viết nhưng chưa nối vào tầng thích ứng lúc chạy",
         "lợi ích “vượt ải bài dễ ở chủ đề mới” chưa tồn tại cho người học; "
         "không ảnh hưởng tới KB2 vì đó là phép chạy lại ngoại tuyến",
         "nối tại chỗ tính vectơ trạng thái, dùng mức tinh thông đã cộng hưởng "
         "mà không ghi đè hồ sơ"],
        ["Vị trí gọi mô hình cho bài phụ đạo còn trống",
         "bài phụ đạo hiện chỉ lấy câu từ kho tĩnh; KB4 bị chặn",
         "dựng một tầng hậu kiểm riêng cho CÂU HỎI (bảy luật của bộ sinh tĩnh) "
         "trước khi bật vị trí này — đúng theo tiêu chí (b) ở mục 3.5.3"],
        [f"{sn(SO['khoCau']['nutDuoi4Cau'])} nút có dưới bốn câu hỏi",
         "không dựng được cặp đo trước — sau hợp lệ từ kho tĩnh cho những nút ấy",
         "soạn bổ sung câu cho các nút ấy, hoặc dùng câu sinh lúc chạy sau khi "
         "đã có tầng hậu kiểm riêng"],
        ["Phép nhận biết mệt mỏi gom theo định dạng, chưa gom theo bậc độ khó",
         "dương tính giả khi một định dạng trải qua nhiều bậc — chứng minh "
         "bằng chính phiên ví dụ ở mục 3.6.11",
         "đổi khoá gom thành bộ đôi (định dạng, bậc); ngưỡng cỡ mẫu giữ nguyên"],
        ["19 nút gốc rễ không được bài học nào dạy",
         "phép định vị trỏ vào một nút không dựng được bài phụ đạo",
         "soạn học liệu cho các nút ấy, hoặc lùi thêm một bước trên đồ thị khi "
         "nút gốc rễ không có bài"],
        ["Ma trận trạng thái chưa có ở màn dành cho giáo viên",
         "giáo viên chưa xem được chẩn đoán gốc rễ của cả lớp",
         "đưa phép tính ma trận ra một mô-đun trung tính với môn học"],
        ["Bốn trong bảy tín hiệu hành vi chưa được dùng để điều chỉnh buổi học",
         "hệ thống đo và báo cáo, nhưng chưa can thiệp",
         "chỉ bật sau khi ngưỡng được hiệu chỉnh ở KB1 — để một ngưỡng chưa "
         "hiệu chỉnh tự động can thiệp là rủi ro lớn hơn giá trị thu được"],
        ["Giao diện làm tròn mức phủ vốn tới phần trăm nguyên",
         "giá trị nhỏ hiển thị thành 0 % trong khi giá trị thật khác 0 — đúng "
         "chỗ dễ làm phụ huynh hiểu nhầm nhất, vì tuần đầu con số vốn đã nhỏ",
         "hiển thị một chữ số thập phân, và luôn kèm phân số thật "
         "(số nút đã vững trên tổng số nút của khối)"],
        ["Chưa có dữ liệu học tập thật đủ lớn",
         "mọi con số ở mục 3.6 chạy trên người học mô phỏng",
         "KB6 — và cho tới khi có kết quả KB6, mọi phát biểu về hiệu quả sư "
         "phạm phải được nêu như giả thuyết"],
    ], ten="Bảng 3.32: Giới hạn đã biết của thiết kế và hướng xử lý")
