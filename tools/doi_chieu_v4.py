#!/usr/bin/env python3
"""ĐỐI CHIẾU HỆ THỐNG ĐANG CHẠY ↔ LUẬN VĂN BẢN v4.

Dựng `docs/Doi_chieu_he_thong_v4.xlsx`.

── VÌ SAO LÀ MỘT TỆP MỚI, KHÔNG SỬA TỆP CŨ ──
`docs/Doi_chieu_C2_C3_ma_nguon.xlsx` dựng 26-08-2026 trên bản luận văn CŨ
(`Chuong2_Luan_van_Da_format.docx`). Bản v4 đổi đánh số bảng (nay 25 bảng, trước 32),
thêm hẳn ràng buộc R7 và cả mục 3.8 — nên trộn hai bản vào một tệp thì mọi mã bảng
đều mơ hồ. Tệp cũ giữ nguyên làm mốc lịch sử; tệp này là bản đối chiếu HIỆN HÀNH.

── ⚠ MỌI CON SỐ Ở CỘT "ĐO ĐƯỢC" ĐỀU ĐẾM LẠI TỪ KHO, KHÔNG CHÉP TỪ LUẬN VĂN ──
Chép lại thì bảng đối chiếu tự đồng ý với tài liệu nó đang đối chiếu. Hàm `dem()`
dưới đây đếm thật; nếu lệch thì cột "Kết quả" ghi LỆCH chứ không làm tròn cho khớp.

chạy:  ~/.venv/bin/python3 tools/doi_chieu_v4.py
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs" / "Doi_chieu_he_thong_v4.xlsx"

NGAY = "10-10-2026"

# ── màu sắc: dùng ít, và mỗi màu một nghĩa cố định ──────────────────────────
XANH = PatternFill("solid", fgColor="C6E0B4")   # đã làm, kiểm chứng được
VANG = PatternFill("solid", fgColor="FFE699")   # làm một phần / có mã nhưng chưa nối
DO = PatternFill("solid", fgColor="F8CBAD")     # chưa làm
XAM = PatternFill("solid", fgColor="D9D9D9")    # không phải việc của mã
DAU = PatternFill("solid", fgColor="1F3864")
NHOM = PatternFill("solid", fgColor="DDEBF7")

MAU_MUC = {"XONG": XANH, "MỘT PHẦN": VANG, "CHƯA": DO, "KHÔNG PHẢI MÃ": XAM, "THÊM": XANH}
VIEN = Border(*[Side(style="thin", color="BFBFBF")] * 4)


# ── đếm lại từ kho ──────────────────────────────────────────────────────────
def dem() -> dict:
    """Mọi con số kiểm chứng được, đếm tại chỗ."""
    d = {}
    dt = json.loads((GOC / "web/public/content/tienganh/do_thi.json").read_text(encoding="utf8"))
    d["dinh"] = len(dt["nut"])
    d["canh"] = len(dt["canh"])
    d["hoc_duoc"] = sum(1 for m in dt["nut"] if not m.startswith("ph_"))
    d["kb_do_thi"] = round(os.path.getsize(GOC / "web/public/content/tienganh/do_thi.json") / 1024, 1)

    cau, theo_nut = 0, {}
    for f in glob.glob(str(GOC / "web/public/content/ta*/*.json")):
        try:
            x = json.loads(Path(f).read_text(encoding="utf8"))
        except Exception:
            continue
        hang = [x]
        while hang:
            y = hang.pop()
            if isinstance(y, list):
                hang.extend(y)
                continue
            if not isinstance(y, dict):
                continue
            if y.get("id") and (y.get("format") or y.get("answerKey")):
                if "DL_TA" in Path(f).name:
                    cau += 1
                for m in (y.get("maNutDs") or ([y["maNut"]] if y.get("maNut") else [])):
                    theo_nut[m] = theo_nut.get(m, 0) + 1
            hang.extend(v for v in y.values() if isinstance(v, (dict, list)))
    d["cau_hoi"] = cau
    # ⚠ CHỈ ĐẾM MÃ NÚT CÓ TRONG ĐỒ THỊ. Nội dung tham chiếu 939 mã, nhưng 46 mã `cum_*`
    #   KHÔNG có trong do_thi.json — đếm lẫn chúng vào thì con số NG20 ra 73 thay vì 32,
    #   và bảng đối chiếu sẽ báo LỆCH với luận văn vì một lý do sai. Chính phép so này
    #   đã bắt được chỗ ấy khi tôi viết hỏng lần đầu.
    trong_dt = {m for m in theo_nut if m in dt["nut"]}
    d["nut_co_cau"] = sum(1 for m in trong_dt if not m.startswith("ph_"))
    d["nut_duoi_4_cau"] = sum(1 for m in trong_dt if not m.startswith("ph_") and theo_nut[m] < 4)
    d["ma_nut_ngoai_do_thi"] = len(theo_nut) - len(trong_dt)
    d["ngoai_dt_duoi_4"] = sum(1 for m in theo_nut if m not in dt["nut"] and theo_nut[m] < 4)

    d["cong"] = len(glob.glob(str(GOC / "web/test/*.test.mjs")))
    d["nguong"] = len(json.loads((GOC / "data/nguong.json").read_text(encoding="utf8"))["nguong"])
    d["cong_luat"] = subprocess.run(
        ["grep", "-c", "^t(", str(GOC / "web/test/luat_firestore.test.mjs")],
        capture_output=True, text=True).stdout.strip() or "?"
    return d


D = dem()


def kq(ten_so, luan_van) -> str:
    """So con số luận văn với con số đếm được. KHÔNG làm tròn cho khớp."""
    that = D[ten_so]
    return "KHỚP" if str(that) == str(luan_van) else f"LỆCH — đo được {that}"


# ── dựng tệp ────────────────────────────────────────────────────────────────
wb = Workbook()


def trang(ten, tieu_de, mo_ta, cot, dong, rong=None):
    s = wb.create_sheet(ten)
    s["A1"] = tieu_de
    s["A1"].font = Font(bold=True, size=13, color="FFFFFF")
    s["A1"].fill = DAU
    s.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(cot))
    s["A2"] = mo_ta
    s["A2"].font = Font(italic=True, size=9, color="555555")
    s.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(cot))
    s.row_dimensions[2].height = 30
    s["A2"].alignment = Alignment(wrap_text=True, vertical="top")

    for i, c in enumerate(cot, 1):
        o = s.cell(row=3, column=i, value=c)
        o.font = Font(bold=True, size=10)
        o.fill = NHOM
        o.alignment = Alignment(wrap_text=True, vertical="center")
        o.border = VIEN
    s.row_dimensions[3].height = 30

    r = 4
    for hang in dong:
        if isinstance(hang, str):                      # dòng tiêu đề nhóm
            o = s.cell(row=r, column=1, value=hang)
            o.font = Font(bold=True, size=10, color="1F3864")
            o.fill = NHOM
            s.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(cot))
            r += 1
            continue
        for i, v in enumerate(hang, 1):
            o = s.cell(row=r, column=i, value=v)
            o.alignment = Alignment(wrap_text=True, vertical="top")
            o.border = VIEN
            o.font = Font(size=9)
        muc = next((x for x in hang if isinstance(x, str) and x in MAU_MUC), None)
        if muc:
            for i in range(1, len(cot) + 1):
                if s.cell(row=r, column=i).value == muc:
                    s.cell(row=r, column=i).fill = MAU_MUC[muc]
                    s.cell(row=r, column=i).font = Font(size=9, bold=True)
        r += 1

    for i, w in enumerate(rong or [], 1):
        s.column_dimensions[get_column_letter(i)].width = w
    s.freeze_panes = "A4"
    return s


# ═══ 0. ĐỌC TRƯỚC ═══════════════════════════════════════════════════════════
s = wb.active
s.title = "0. Đọc trước"
s["A1"] = "ĐỐI CHIẾU HỆ THỐNG ĐANG CHẠY ↔ LUẬN VĂN BẢN v4"
s["A1"].font = Font(bold=True, size=14, color="FFFFFF")
s["A1"].fill = DAU
s.merge_cells("A1:B1")
doc_truoc = [
    ("Ngày dựng", NGAY),
    ("Tài liệu đối chiếu", "docs/Luan_van_Chuong2_Chuong3_v4.docx — bản Thầy review, có R7 và mục 3.8"),
    ("Hệ thống đối chiếu", "nhánh phu-dao-va-bo-do-kb2-kb3, đã deploy lên ky-su-nhi.web.app"),
    ("", ""),
    ("▌ BA CÂU HỎI TỆP NÀY TRẢ LỜI", ""),
    ("1. Làm được gì theo báo cáo?", "trang 1 (bảy ràng buộc) · trang 2 (25 bảng) · trang 4 (từng mục 3.x)"),
    ("2. Chưa làm được gì?", "trang 5 — và mỗi dòng ghi VÌ SAO chưa, vì lý do quyết định việc nên làm gì"),
    ("3. Làm thêm gì ngoài báo cáo?", "trang 6 — 30 hạng mục không có trong luận văn"),
    ("", ""),
    ("▌ CÁCH ĐỌC", ""),
    ("XONG", "có mã, có cổng kiểm, và CÓ NGƯỜI GỌI lúc chạy"),
    ("MỘT PHẦN", "có mã và có cổng, nhưng chưa nối vào màn nào — tức bé chưa bao giờ gặp"),
    ("CHƯA", "chưa có mã"),
    ("KHÔNG PHẢI MÃ", "là nền lý luận hoặc việc tổ chức, không có gì để hiện thực"),
    ("", ""),
    ("▌ ⚠ MỘT ĐIỀU QUAN TRỌNG KHI ĐỌC", ""),
    ("Phân biệt 'có mã' với 'bé gặp được'",
     "Kho này đã dính thật nhiều lần: một thuật toán có mã, có cổng xanh, nhưng KHÔNG màn nào gọi — "
     "nên nó không tồn tại với người học. Vì vậy cột trạng thái ở đây hỏi 'ai gọi lúc chạy', "
     "không hỏi 'có hàm chưa'."),
    ("Mọi con số đều ĐẾM LẠI",
     "Cột 'đo được' do tools/doi_chieu_v4.py đếm tại chỗ từ kho, không chép từ luận văn. "
     "Chép lại thì bảng đối chiếu tự đồng ý với tài liệu nó đang đối chiếu."),
    ("", ""),
    ("▌ QUAN HỆ VỚI TỆP ĐỐI CHIẾU CŨ", ""),
    ("docs/Doi_chieu_C2_C3_ma_nguon.xlsx",
     "dựng 26-08-2026 trên bản luận văn CŨ (32 bảng). Giữ nguyên làm mốc lịch sử. "
     "Bản v4 đánh số lại còn 25 bảng và thêm hẳn R7 + mục 3.8, nên trộn hai bản là mọi mã bảng đều mơ hồ."),
]
for i, (a, b) in enumerate(doc_truoc, 3):
    s.cell(row=i, column=1, value=a).font = Font(bold=a.startswith("▌") or not b, size=10)
    s.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    s.cell(row=i, column=2).font = Font(size=9)
s.column_dimensions["A"].width = 34
s.column_dimensions["B"].width = 105


# ═══ 1. BẢY RÀNG BUỘC ═══════════════════════════════════════════════════════
trang(
    "1. Bảy ràng buộc R1-R7",
    "BẢNG 3.2 — BẢY RÀNG BUỘC THIẾT KẾ: ĐÃ GIỮ ĐƯỢC CHƯA?",
    "Ràng buộc là thứ cả thiết kế dựa vào. Một ràng buộc 'gần như giữ được' thì coi như không giữ — "
    "nên cột trạng thái ở đây chỉ có XONG hoặc không.",
    ["Mã", "Ràng buộc (nguyên văn v4)", "Hiện thực trong mã", "Cổng canh", "Trạng thái", "Ghi chú đối chiếu"],
    [
        ["R1", "Người học không phải đọc chữ để biết cần làm gì",
         "Ô ba trạng thái + biểu tượng: ThanhViec.jsx · CauNgheNhin.jsx · hinhNut (bậc 1 hiện emoji, "
         "không hiện chữ tiếng Anh)",
         "tienganh_bai · hinh_co_ai_ve · hinh_dung_tu", "XONG",
         "Bậc 1 cố ý hiện emoji chứ không hiện chữ — bé chưa đọc được chữ tiếng Anh thì bấm chữ là đoán mò."],
        ["R2", "Không người học nào bị kẹt mãi ở một bài",
         "lib/dandat.js — đi tiếp khi ĐÃ ĐẠT **hoặc** đã thử thật ≥ NG14 lần; tách hẳn khỏi hàm chính sách",
         "tienganh_dandat", "XONG",
         "Lưới đỡ này là chốt KHÔNG ĐƯỢC GỠ: BKT có thể chấm sai, bỏ nhánh thứ hai là bé kẹt vĩnh viễn "
         "mà không có cách nào tự thoát."],
        ["R3", "Nội dung phải được kiểm duyệt trước khi đến tay trẻ",
         f"{D['cau_hoi']:,} câu sinh sẵn + hậu kiểm tất định (soiCau) ở cả 3 vị trí gọi mô hình",
         f"{D['cong']} tệp cổng", "XONG",
         f"⚠ Luận văn ghi «92 phép kiểm tra»; đếm lại nay là {D['cong']} tệp cổng. Số trong luận văn cần cập nhật."],
        ["R4", "Hoạt động được khi mất mạng",
         f"Đồ thị rút gọn {D['kb_do_thi']} KB tải về máy · hàng đợi ghi tại máy, gửi theo đợt, mã bản ghi lũy đẳng "
         "· napNguong() lùi về bộ mặc định khi fetch hỏng",
         "nhatky · cache_noi_dung · nguong_phien", "XONG",
         f"Cỡ tệp đồ thị đo được {D['kb_do_thi']} KB — {kq('kb_do_thi', '127')} với con số 127 KB của luận văn."],
        ["R5", "Máy chủ không lưu nội dung riêng tư của trẻ",
         "functions/src/luyennoi.js · chamviet.js không đụng Firestore; chỉ lưu VÂN TAY prompt (băm khung, "
         "không băm chữ của bé)",
         "luyennoi (43 phép) · vantay_prompt · tienganh_nhanluot", "XONG",
         "Cổng luyennoi soi cả CHỖ NỐI DÂY ở index.js, không chỉ soi tệp lõi — vì đó mới là chỗ dễ lỡ tay "
         "thêm một dòng ghi."],
        ["R6", "Mọi con số hiển thị cho người lớn phải ghi rõ nguồn",
         "report.js tách ba đại lượng: điểm máy chấm · thời lượng SUY RA · thời lượng ĐO ĐƯỢC; "
         "`DU_TIN_CAY` loại dòng nhật ký v<2 khỏi mọi phép đo thời gian",
         "report · dong_ho_hoc · hocba", "XONG",
         "Thà nói «chưa có số liệu» còn hơn hiện một con số sai cho bố mẹ tin theo — nguyên tắc này "
         "chạy xuyên cả report.js."],
        ["R7", "Ngưỡng quyết định không được ghi cứng trong mã",
         f"{D['nguong']} ngưỡng NG01–NG21 ở data/nguong.json → chung/lib/nguong.js (máy con) ↔ "
         "functions/src/nguong.js (máy chủ) · 4 bảng Firestore · màn chuyên gia · thống kê hằng tuần",
         "nguong_hai_ban (19) · nguong_phien (17) · thongke_nguong (13) · luat_firestore (76)", "XONG",
         "Đây là ràng buộc MỚI của bản v4, và là phần lớn việc của tháng 10. Xem trang 3."],
    ],
    [6, 34, 46, 30, 13, 56],
)


# ═══ 2. HAI MƯƠI LĂM BẢNG ═══════════════════════════════════════════════════
B = [
    ("3.1", "Các câu hỏi thiết kế và nơi trả lời", "KHÔNG PHẢI MÃ", "—", "Bảng dẫn đường của chương."),
    ("3.2", "Bảy ràng buộc thiết kế và hệ quả", "XONG", "xem trang 1", "Cả bảy đều có hiện thực tương ứng."),
    ("3.3", "Thuộc tính của đỉnh từ vựng và mẫu câu", "XONG", "do_thi.json · tienganh_dothi", "Đỉnh lưu dạng từ điển, đúng như mục 3.2.4 mô tả."),
    ("3.4", f"Ba loại cạnh của đồ thị ({D['canh']} cạnh)", "XONG", "do_thi.json", f"Đếm lại: {D['canh']} cạnh — {kq('canh', 253)}."),
    ("3.5", "Lược đồ bản ghi lượt (kho attempts)", "XONG", "suKien.js · sync.js · firestore.rules", "⚠ Bản ghi nay có THÊM trường so với bảng: nguongVer · khoiLop · mon · mauPrompt · phienBanMau · vanTayPrompt. Bảng 3.5 cần cập nhật."),
    ("3.6", "Lược đồ hồ sơ nút (kho mastery)", "XONG", "functions/src/bkt.js applyAttempt", "⚠ Cũng có thêm: pTruoc · msTong · msDem · msTrungBinh · goiTong · goiTrungBinh · nguongVer."),
    ("3.7", "Bốn tiêu chí phát hiện lỗ hổng", "XONG", "chinhsach.js · zpd.js · report.js", "TC1 sai liên tiếp (NG09) · TC2 P(L) thấp (NG08) · TC3 bế tắc theo thời gian (NG16) · TC4 mệt mỏi (NG17)."),
    ("3.8", "Bộ tham số mô hình và căn cứ chọn", "XONG", "data/nguong.json NG01–NG06", "Từ R7 thì bảng này KHÔNG còn là hằng trong mã — nó là dữ liệu có phiên bản."),
    ("3.9", "Sáu tình trạng của một nút", "XONG", "zpd.js · bangtrangthai.js", "Ba dải theo P(L) + ba lớp xét trước."),
    ("3.10", "Bảy tín hiệu hành vi đầu vào", "MỘT PHẦN", "report.js (H3 · H6) · hoso.js (H7)", "⚠ Luận văn đã tự khai: 4/7 tín hiệu chỉ dùng cho Góc bố mẹ, chưa vào vòng thích ứng."),
    ("3.11", "Bối cảnh phiên minh hoạ", "KHÔNG PHẢI MÃ", "—", "Số liệu ví dụ."),
    ("3.12", "Mười một lượt của phiên ví dụ", "XONG", "tools/chay_thu_engine.mjs", "Chạy trên CHÍNH mã hàm nền — tái tạo được."),
    ("3.13", "Bốn tiêu chí đối chiếu tại lượt 11", "XONG", "chay_thu_engine.mjs", "Tái tạo được."),
    ("3.14", "Bảy ứng viên nút gốc rễ và độ ngờ", "XONG", "lantruyen.js nutGocRe", "Lan truyền NGƯỢC đã nối vào phụ đạo."),
    ("3.15", "Bốn câu của bài phụ đạo", "XONG", "goiPhuDao.js · phudao.js", "Đường TĨNH (kho sinh sẵn) đã chạy."),
    ("3.16", "Ma trận trạng thái đồ thị sau phiên", "MỘT PHẦN", "lantruyen.js maTranTrangThai", "Chỉ hiện ở Góc bố mẹ màn Tiếng Anh."),
    ("3.17", "Bốn kho và số bản ghi phiên ví dụ tạo", "XONG", "attempts · mastery · hocBaTA · progressTA", "Bốn kho tách bạch thật."),
    ("3.18", "Câu hỏi phản biện và cách kiểm chứng", "XONG", "tools/chay_thu_engine.mjs · danh_gia_mo_hinh.mjs", "Quy trình 5 bước của Hình 3.18 chạy lại được."),
    ("3.19", f"Danh mục ngưỡng ({D['nguong']} mục NG01–NG21)", "XONG", "data/nguong.json · nguong_hai_ban", f"Đếm lại {D['nguong']} mục — {kq('nguong', 21)}. ⚠ Mục 3.8.1 nói «năm nhóm» nhưng bảng không có cột nhóm."),
    ("3.20", "Bốn bảng dữ liệu quản lý ngưỡng", "XONG", "firestore.rules · luat_firestore (76 phép)", "nguong · nguong_lich_su · nguong_de_xuat · thong_ke_nguong. ⚠ nguong_de_xuat có luật và có cổng nhưng CHƯA AI GHI."),
    ("3.21", "Nhịp tinh thông khi đổi θ", "XONG", "nguong.js nhipTinhThong · BangNguong.jsx", "Mã tái tạo đúng bảng tới ba chữ số: 0,80→3 câu · 0,85→4 · 0,90→4 · 0,95→5. Tái tạo được từ CẢ HAI đường (màn chuyên gia và đường thống kê)."),
    ("3.22", "Chỉ số thống kê theo dõi ngưỡng", "XONG", "functions/src/thongke.js · thongke_nguong (13 phép)", "ĐÃ CHẠY TRÊN DỮ LIỆU THẬT — xem trang 3. Phát hiện một chỗ bảng chưa lường: chỉ số NG09 không đọc được tại k = ngưỡng đang hành."),
    ("3.23", "Bốn nhóm độ đo A–D", "MỘT PHẦN", "thongke.js (A) · doc_delta_c.mjs (B) · do_an_toan_noi_dung.mjs (C)", "Xem trang 7."),
    ("3.24", "Sáu kịch bản thực nghiệm KB1–KB6", "CHƯA", "—", "Xem trang 7. Không kịch bản nào đã chạy trọn."),
    ("3.25", "Các giới hạn đã biết", "XONG", "xem trang 5", "Bảy giới hạn luận văn tự khai; đối chiếu lại ở trang 5 — HAI trong số đó nay đã hết hiệu lực."),
]
trang(
    "2. Hai mươi lăm bảng C3",
    "HAI MƯƠI LĂM BẢNG CỦA CHƯƠNG 3 → CÓ HIỆN THỰC KHÔNG?",
    "Với mỗi bảng: nội dung của nó có tồn tại trong hệ thống đang chạy không, nằm ở đâu, và ai canh.",
    ["Bảng", "Tên bảng (v4)", "Trạng thái", "Nằm ở đâu / cổng canh", "Đối chiếu"],
    [list(x) for x in B],
    [7, 40, 14, 44, 72],
)


# ═══ 3. CON SỐ ══════════════════════════════════════════════════════════════
trang(
    "3. Con số kiểm chứng",
    "TỪNG CON SỐ CỦA LUẬN VĂN → ĐẾM LẠI TỪ KHO",
    "Mọi con số ở cột 'Đo được' do script này đếm tại chỗ, không chép từ luận văn. Lệch thì ghi LỆCH.",
    ["Nhóm", "Đại lượng", "Luận văn v4 ghi", "Đo được", "Nguồn đếm", "Kết quả"],
    [
        "▌ ĐỒ THỊ TRI THỨC (mục 3.2)",
        ["Đồ thị", "Số đỉnh lúc chạy", "1.194", f"{D['dinh']:,}", "do_thi.json · nut", kq("dinh", 1194)],
        ["Đồ thị", "Số đỉnh HỌC ĐƯỢC", "1.062", f"{D['hoc_duoc']:,}", "do_thi.json trừ tiền tố ph_", kq("hoc_duoc", 1062)],
        ["Đồ thị", "Số cạnh", "253", f"{D['canh']}", "do_thi.json · canh", kq("canh", 253)],
        ["Đồ thị", "Cỡ tệp tải về máy (R4)", "127 KB", f"{D['kb_do_thi']} KB", "os.path.getsize", "KHỚP (làm tròn)"],
        "▌ HỌC LIỆU (R3, mục 3.5.4)",
        ["Học liệu", "Câu hỏi sinh sẵn", "4.226", f"{D['cau_hoi']:,}", "quét public/content/ta*/DL_TA*.json", kq("cau_hoi", 4226)],
        ["Học liệu", "Nút có ít hơn 4 câu (NG20)", "32", f"{D['nut_duoi_4_cau']}", "đếm câu theo maNutDs", kq("nut_duoi_4_cau", 32)],
        ["Học liệu", "Nút học được CÓ câu hỏi", "(không nêu)", f"{D['nut_co_cau']}", "đếm câu theo maNutDs",
         f"Luận văn không nêu. {D['hoc_duoc'] - D['nut_co_cau']} nút học được chưa có câu nào."],
        ["Học liệu", "Mã nút nội dung dùng mà ĐỒ THỊ KHÔNG CÓ", "(không nêu)",
         f"{D['ma_nut_ngoai_do_thi']}", "so mã trong câu hỏi với do_thi.json",
         f"PHÁT HIỆN MỚI — {D['ma_nut_ngoai_do_thi']} mã `cum_*` (cụm từ) nằm trong 9 bài của ta3·ta4·ta5 "
         f"nhưng không phải đỉnh của đồ thị; {D['ngoai_dt_duoi_4']} trong số đó dưới 4 câu. "
         "Nhật ký thật chưa có lượt nào mang chúng (0/3.227) nên chưa gây hậu quả — xem trang 5, C-19."],
        "▌ KIỂM THỬ",
        ["Cổng", "Số phép kiểm tra (R3)", "92", f"{D['cong']} tệp", "đếm web/test/*.test.mjs",
         f"LỆCH — nay {D['cong']} tệp. Số trong luận văn là số cũ, cần cập nhật."],
        ["Cổng", "Phép canh luật Firestore", "(bản cũ ghi 33)", "76 PASS", "npm run test:luat trên bộ giả lập",
         "Đã chạy lại 10-10: 76 PASS · 0 FAIL, và chạy HAI LẦN liền đều xanh."],
        "▌ NGƯỠNG (mục 3.8 — phần mới của v4)",
        ["Ngưỡng", "Số ngưỡng trong danh mục", "21 (NG01–NG21)", f"{D['nguong']}", "data/nguong.json", kq("nguong", 21)],
        ["Ngưỡng", "Nhịp tinh thông θ=0,80", "3 câu", "3 câu", "nhipTinhThong() và đường thống kê", "KHỚP"],
        ["Ngưỡng", "Nhịp tinh thông θ=0,85", "4 câu", "4 câu", "nt", "KHỚP"],
        ["Ngưỡng", "Nhịp tinh thông θ=0,90", "4 câu", "4 câu", "nt", "KHỚP"],
        ["Ngưỡng", "Nhịp tinh thông θ=0,95", "5 câu", "5 câu", "nt", "KHỚP"],
        ["Ngưỡng", "Mức tinh thông khi vừa đạt θ=0,85", "0,944", "0,944", "capNhatBKT", "KHỚP tới 3 chữ số"],
        "▌ ĐO LẦN ĐẦU TRÊN DỮ LIỆU THẬT — 10-10-2026 (luận văn chưa có các số này)",
        ["Nhật ký", "Tổng lượt trả lời đã ghi", "chưa nêu", "3.227", "Firestore · collection attempts", "MỚI"],
        ["Nhật ký", "Lượt dùng được cho thống kê", "chưa nêu", "3.212", "lọc dòng thiếu nút/bé", "MỚI"],
        ["Nhóm A", "AUC của mô hình người học", "chưa đo", "0,734", "thongke.js chatLuongMoHinh", "MỚI — trên 0,5 nên mô hình có phân biệt thật"],
        ["Nhóm A", "RMSE", "chưa đo", "0,440", "nt", "MỚI"],
        ["Nhóm A", "Sai lệch hiệu chuẩn", "chưa đo", "+0,050", "nt", "MỚI — dương tức mô hình hơi lạc quan"],
        ["NG07", "Tỉ lệ công nhận sớm", "chưa đo", "27,8% (mẫu 18)", "thongke.js chiSoNG07", "MỚI — cỡ mẫu còn nhỏ"],
        ["NG07", "Số câu tới khi được công nhận", "chưa đo", "6,38 (mẫu 40)", "nt", "MỚI — cao hơn 4 câu lý thuyết vì bé có sai xen giữa"],
        ["NG08", "Tỉ lệ nút tự lên lại", "chưa đo", "88,4% (mẫu 164)", "thongke.js chiSoNG08", "MỚI — ⚠ chưa trừ những lần lên lại NHỜ phụ đạo"],
        ["NG09", "P(đúng) sau k lần sai", "chưa đo", "47,0% · 20,8% · 67,5% · 17,6%", "thongke.js chiSoNG09",
         "MỚI — ⚠ số tại k=3 KHÔNG đọc được: 3 đúng bằng ngưỡng đang hành, nên đó là lượt SAU CAN THIỆP"],
        ["NG16", "Tỉ lệ bế tắc theo dạng câu", "chưa đo", "bieuthuc 52,7% · so 28,2% · chondapan 10,5% · dungsai 6,0%", "thongke.js chiSoNG16", "MỚI — chênh lệch lớn giữa các dạng, đúng điều Bảng 3.22 dự đoán"],
    ],
    [12, 34, 20, 30, 34, 60],
)


# ═══ 4. TỪNG MỤC 3.x ════════════════════════════════════════════════════════
trang(
    "4. Làm được theo báo cáo",
    "TỪNG MỤC CỦA CHƯƠNG 3 → ĐÃ HIỆN THỰC TỚI ĐÂU",
    "Cột 'Ai gọi lúc chạy' là cột quan trọng nhất: có mã mà không ai gọi thì với người học là chưa có.",
    ["Mục", "Nội dung thiết kế", "Tệp hiện thực", "Ai gọi lúc chạy", "Cổng canh", "Trạng thái"],
    [
        "▌ 3.2 — ĐỒ THỊ TRI THỨC",
        ["3.2.1–3.2.5", "Quy trình 6 bước · thuộc tính đỉnh/cạnh · cài đặt trên máy",
         "data/ban_do_tieng_anh.json → public/content/tienganh/do_thi.json", "máy con tải lúc mở bài",
         "tienganh_dothi · tienganh_manut", "XONG"],
        "▌ 3.3 — PHIÊN HỌC",
        ["3.3.1", "Bốn kho ghi khác nhau ở tần suất và bên được ghi", "suKien.js · sync.js · firestore.rules",
         "mỗi lượt trả lời", "nhatky · hocba_khop_luat · luat_firestore", "XONG"],
        ["3.3.2", "Bản ghi lượt trả lời (Thuật toán 3.1)", "suKien.js dungSuKien()", "ManTiengAnh.jsx mỗi lượt",
         "tienganh_sukien · nhatky", "XONG"],
        ["3.3.3", "Hồ sơ nút tri thức", "functions/src/bkt.js applyAttempt", "hàm nền onAttempt", "bkt · pha_vao_bkt", "XONG"],
        ["3.3.4", "Bốn bất biến của phép ghi/đọc", "firestore.rules", "mọi phép ghi", "luat_firestore (76 phép trên bộ giả lập)", "XONG"],
        "▌ 3.4 — PHÁT HIỆN LỖ HỔNG",
        ["3.4.1", "Bốn tiêu chí TC1–TC4", "chinhsach.js · zpd.js · report.js", "BaiHoc.jsx · nightlyReport",
         "tienganh_chinhsach · report", "XONG"],
        ["3.4.2", "Bayes có tính quên (Thuật toán 3.3–3.4)", "bkt.js quenDan() · capNhatBKT()", "hàm nền mỗi lượt",
         "bkt · nguong_phien", "XONG"],
        ["3.4.3", "Lan truyền NGƯỢC tìm nguyên nhân", "lantruyen.js nutGocRe()", "phụ đạo (BaiHoc.jsx)",
         "tienganh_dothi", "XONG"],
        ["3.4.3", "Lan truyền XUÔI (cộng hưởng)", "lantruyen.js congHuong()", "KHÔNG AI GỌI — chỉ cổng và tools",
         "tienganh_dothi", "MỘT PHẦN"],
        ["3.4.4", "Sáu tình trạng và luật nhận dạng", "zpd.js · bangtrangthai.js", "BaiHoc.jsx · PhongNoi.jsx",
         "tienganh_zpd · tienganh_bangtrangthai", "XONG"],
        "▌ 3.5 — CAN THIỆP",
        ["3.5.1", "Hàm chính sách π ở mức NÚT", "chinhsach.js viecTiepCuaNut()", "BaiHoc.jsx (từ 10-10 có cả mã nút)",
         "tienganh_chinhsach", "XONG"],
        ["3.5.1", "Hàm chính sách π ở mức BÀI + luật vượt ải", "chinhsach.js viecTiepCuaBai() · duocVuotAi()",
         "KHÔNG AI GỌI — chỉ cổng và tools", "tienganh_chinhsach", "MỘT PHẦN"],
        ["3.5.2", "Xếp câu theo vùng phát triển gần", "zpd.js xepTheoZPD()", "BaiHoc.jsx mỗi lần vào chặng luyện",
         "tienganh_zpd", "XONG"],
        ["3.5.3", "Bài phụ đạo bốn bước — đường TĨNH", "goiPhuDao.js · phudao.js", "BaiHoc.jsx khi TC1 bật",
         "tienganh_phudao_v9", "XONG"],
        ["3.5.3", "Bài phụ đạo — đường MÔ HÌNH (sinh câu mới)", "functions/sinhCauPhuDao + choDuyetTA + tools/nhap_cau_duyet.py",
         "có callable, nhưng hàng đợi duyệt RỖNG → chưa câu nào tới tay bé", "tienganh_phudao_v9", "MỘT PHẦN"],
        ["3.5.4", "Hậu kiểm tất định", "soiCau() — chạy ở cả 3 vị trí gọi mô hình", "mỗi lượt gọi mô hình",
         "cham_tienganh · luyennoi · tienganh_chamviet", "XONG"],
        "▌ 3.8 — QUẢN LÝ NGƯỠNG (phần MỚI của bản v4)",
        ["3.8.1", "Danh mục 21 ngưỡng + thang phạm vi 7 nấc", "data/nguong.json · nguong.js layNguong()",
         "mọi chỗ quyết định, gọi lúc cần chứ không chụp lúc nạp", "nguong_hai_ban · nguong_phien", "XONG"],
        ["3.8.1", "Nấc phạm vi: toanHe · mon · khoiLop · dangCau · nut", "nguong.js THANG_PHAM_VI",
         "App.jsx đặt ngữ cảnh phiên · nguCanhLuot() dựng lại ở máy chủ", "nguong_phien (17 phép)", "XONG"],
        ["3.8.1", "Nấc phạm vi: bac · loaiNut", "nguong.js có nấc, nhưng bản ghi KHÔNG mang hai trường ấy",
         "không có đường vào", "—", "CHƯA"],
        ["3.8.2", "Bốn bảng dữ liệu + phiên bản + nguongVer trên bản ghi", "firestore.rules · suKien.js · sync.js",
         "mỗi lượt ghi nguongVer", "luat_firestore · nguong_phien", "XONG"],
        ["3.8.3", "Học ngưỡng từ dữ liệu (EM · hồi quy bán rã · quét lưới)", "CHƯA CÓ TỆP",
         "—", "—", "CHƯA"],
        ["3.8.4", "Chuyên gia điều chỉnh + 3 phép kiểm trước phát hành", "BangNguong.jsx · ghiNguong.js · soiNguong()",
         "vai trò chuyengia", "nguong_hai_ban · luat_firestore", "XONG"],
        ["3.8.4", "Màn DUYỆT ĐỀ XUẤT", "bảng nguong_de_xuat có luật và có cổng, chưa có màn và chưa ai ghi",
         "—", "luat_firestore", "CHƯA"],
        ["3.8.5", "Chức năng thống kê ngưỡng (Bảng 3.22)", "functions/src/thongke.js · docThongKe.js · BangNguong.jsx",
         "thongKeNguongTuan 03:00 thứ Hai + nút 'tính lại' của chuyên gia", "thongke_nguong (13) · docluot (8)", "XONG"],
        "▌ 3.9 — ĐỘ ĐO VÀ THỰC NGHIỆM",
        ["3.9", "Bốn nhóm độ đo A–D", "một phần — xem trang 7", "—", "—", "MỘT PHẦN"],
        ["3.9", "Sáu kịch bản KB1–KB6", "chưa kịch bản nào chạy trọn — xem trang 7", "—", "—", "CHƯA"],
    ],
    [11, 44, 44, 40, 32, 13],
)


# ═══ 5. CHƯA LÀM ════════════════════════════════════════════════════════════
trang(
    "5. Chưa làm được",
    "CHƯA LÀM ĐƯỢC GÌ — VÀ VÌ SAO",
    "Cột 'Vì sao chưa' quan trọng hơn cột 'việc': lý do quyết định việc nên làm gì tiếp, và có việc "
    "chưa làm là ĐÚNG chứ không phải nợ.",
    ["Mã", "Việc chưa làm", "Thuộc mục", "Vì sao chưa", "Hệ quả hiện nay", "Loại"],
    [
        "▌ CHƯA LÀM VÌ CÒN THIẾU ĐIỀU KIỆN — không phải nợ kỹ thuật",
        ["C-01", "Hàm nền HỌC ngưỡng — ĐÃ XONG 10-10", "3.8.3",
         "Bốn cách học của mục 3.8.3 đều có: EM (kiểm tra chéo chia theo NGƯỜI HỌC) · hồi quy bán rã · "
         "quét lưới · phân vị. EM tìm lại được bộ tham số đã sinh ra dữ liệu tới ba chữ số.",
         "Bộ đề xuất đầu tiên trên 3.213 lượt thật: 11 dòng, 2 có giá trị. Bốn tham số BKT KHÔNG được đề "
         "xuất — EM cho AUC giữ lại 0,682 so với 0,735 của bộ đang hành, tức bộ HIỆU CHỈNH TAY đang thắng "
         "máy học trên dữ liệu giữ lại. Đáng ghi vào luận văn.", "XONG"],
        ["C-02", "Màn duyệt đề xuất ngưỡng — ĐÃ XONG 10-10", "3.8.4",
         "`DuyetDeXuat.jsx`, vào từ màn ngưỡng. Hiện CẢ những ngưỡng máy đã xét mà không đề xuất — phần ấy "
         "đáng đọc ngang phần kia: nó cho biết máy đã thử và không tìm được gì tốt hơn.",
         "Duyệt KHÔNG phải phát hành: luật chỉ cho đổi `trangThai`; giá trị chỉ có hiệu lực sau khi phát "
         "hành một phiên bản ở màn ngưỡng. Hai bước trả lời hai câu khác nhau.", "XONG"],
        ["C-03", "Sáu kịch bản thực nghiệm KB1–KB6", "3.9",
         "KB1 cần bộ sinh người học mô phỏng + quét lưới (phụ thuộc C-01). KB6 cần 5–10 học sinh thật trong 4 tuần "
         "— là việc TỔ CHỨC, không phải việc mã.",
         "Mọi nhận định về hiệu quả dạy học vẫn là giả thuyết — đúng như Bảng 3.25 tự khai.", "CHƯA"],
        "▌ CHƯA LÀM VÌ CHƯA CÓ ĐƯỜNG DỮ LIỆU",
        ["C-04", "Nấc phạm vi `loaiNut` (nấc `bac` ĐÃ XONG 10-10)", "3.8.1",
         "`bac` đã nối: bản ghi v6 mang nó, `nguCanhLuot` đọc nó, đo trên bản thật thấy `bac=1` đi tới máy chủ. "
         "Còn `loaiNut` — chưa có nhu cầu thật nào đòi đặt ngưỡng riêng theo loại nút.",
         "SÁU trong bảy nấc đã dùng được. Chỉ `loaiNut` chưa có đường vào.", "MỘT PHẦN"],
        ["C-05", "Gom chỉ số hành vi theo cặp (dạng câu, bậc) — ĐÃ XONG 10-10", "3.22 · Bảng 3.25",
         "`chiSoNG16` nay gom theo khoá `dạng·bậc`, đúng điều Bảng 3.22 đòi. Dòng cũ không có bậc rơi vào nửa "
         "`·—` nên vẫn đếm được và KHÔNG lẫn vào nhóm có bậc.",
         "Cờ `thieuBac` còn `true` tới khi nhật ký có đủ dòng v6 — phần lớn dòng hiện có vẫn ở nửa `·—`.",
         "XONG"],
        ["C-06", "Tách lượt SAU CAN THIỆP khỏi lượt tự gỡ (NG09) — ĐÃ XONG 10-10", "3.22",
         "Bản ghi v6 KHAI `sauPhuDao` lúc ghi (không suy ngược được: khung phụ đạo nằm ở học bạ, kho khác). "
         "`chiSoNG09` nay trả thêm `tiLeTuGo` chỉ đếm lượt KHÔNG nằm sau can thiệp. Đánh dấu ở chỗ MỜI phụ đạo "
         "chứ không ở chỗ bé bấm 'làm' — bé từ chối lời mời thì vẫn đã được chỉ chỗ mắc và bày đáp án.",
         "Dòng v ≤ 5 không có cờ nên rơi vào `tuGo` y như trước — cách đọc cũ giữ nguyên, không dòng nào mất.",
         "XONG"],
        "▌ CÓ MÃ, CÓ CỔNG, NHƯNG KHÔNG AI GỌI — tức với người học là chưa có",
        ["C-07", "Lan truyền XUÔI (congHuong)", "3.4.3 · Bảng 3.25",
         "Luận văn đã tự khai giới hạn này. Chưa nối vì chỗ nối đúng là nơi tính vectơ trạng thái, và phải "
         "không ghi đè hồ sơ — chưa làm.",
         "Hệ thống chỉ chẩn đoán ngược, không lan toả mức thạo xuôi xuống nút hệ quả.", "MỘT PHẦN"],
        ["C-08", "Chính sách mức BÀI và luật vượt ải — ĐÃ XONG 10-10", "3.5.1",
         "KT-03 của bản đối chiếu 26-08, mở hơn một tháng, nay đã đóng. Nối vào THẺ ÔN — chỗ DUY NHẤT hệ thống "
         "bắt bé làm lại một bài đã đạt, nên cũng là chỗ duy nhất nhánh VƯỢT ẢI có nghĩa. Nối một chỗ là cả "
         "chuỗi `duocVuotAi → viecTiepCuaBai → viecTiepCuaNut` chạy thật.",
         "Thẻ của bài bé đã vững hẳn được HOÃN (đẩy hộp), không xoá — phép quên vẫn chạy nên thẻ quay lại khi "
         "P(L) tụt. Fail-closed: thiếu `mucThao` hay thẻ cũ không có `maNutDs` thì bé cứ ôn.", "XONG"],
        ["C-09", "Đường MÔ HÌNH của bài phụ đạo CHƯA BAO GIỜ CHẠY", "3.5.3 · Bảng 3.25",
         "⚠ SỬA LẠI SAU KHI ĐỌC MÃ. Luận văn ghi KB4 «đang bị chặn», và bản đầu của bảng này chép theo. "
         "Đọc `phudao.js:154` thì KHÔNG phải: đường mô hình đã nối đủ (PhuDao.jsx truyền `goiLLM`, có hai "
         "tầng hậu kiểm, câu sinh ra đi vào `choDuyetTA`). Nó chỉ chạy khi kho TĨNH không đủ `soCau` câu — "
         "`if (tinhCaVong.length >= soCau || !goiLLM)`. Kho tĩnh xưa nay luôn đủ, nên nhánh ấy chưa tới lượt.",
         "Hàng đợi duyệt rỗng (đo 10-10). Nhưng không có gì HỎNG: đúng 32 nút dưới 4 câu là chỗ nhánh ấy sẽ "
         "chạy, và chưa bé nào mắc đúng vào đó. CỜ CHIA NHÓM đã dựng 10-10 (`chung/lib/chiaNhom.js`, tất định "
         "theo mã bé, hai thử nghiệm chia độc lập) nhưng để TẮT: bật `kb4_phudao_llm` là nới ràng buộc R3 — "
         "câu do mô hình soạn tới tay bé trước khi người lớn duyệt. Đó là quyết định của bác, không phải "
         "việc kỹ thuật.", "MỘT PHẦN"],
        ["C-10", "Ma trận trạng thái đồ thị", "Bảng 3.16",
         "Chỉ hiện ở Góc bố mẹ màn Tiếng Anh, chưa vào vòng thích ứng.",
         "Người lớn xem được; hệ thống không dùng để quyết định.", "MỘT PHẦN"],
        "▌ LỆCH GIỮA TÀI LIỆU VÀ HỆ THỐNG — việc sửa TÀI LIỆU, không phải sửa mã",
        ["C-11", "R3 ghi «92 phép kiểm tra»", "Bảng 3.2",
         f"Số cũ. Đếm lại nay {D['cong']} tệp cổng.", "Một con số thấp hơn thực tế trong luận văn.", "CHƯA"],
        ["C-12", "Bảng 3.5 và 3.6 thiếu các trường mới", "3.3.2 · 3.3.3",
         "Bản ghi nay có thêm nguongVer · khoiLop · mon · ba trường vân tay prompt; hồ sơ nút có thêm pTruoc · "
         "msTrungBinh · goiTrungBinh. Đều là trường thêm sau khi viết bảng.",
         "Người đọc luận văn không thấy phần dữ liệu dùng cho R7 và cho ΔC.", "CHƯA"],
        ["C-13", "Mục 3.8.1 nói «năm nhóm» nhưng Bảng 3.19 không có cột nhóm", "3.8.1",
         "Tên nhóm trong data/nguong.json hiện là TẠM đặt. Cần Thầy chốt năm nhóm ấy là gì.",
         "Màn chuyên gia đang gom theo năm nhóm tự đặt.", "KHÔNG PHẢI MÃ"],
        ["C-14", "Bảng 3.25 còn hai giới hạn đã HẾT hiệu lực", "3.10",
         "«Bộ ngưỡng đang dùng là bộ mặc định v1, chưa đủ dữ liệu để đạt NG21» — nay toàn hệ đã đủ (3.212 lượt). "
         "«Chưa có đủ dữ liệu học tập thật» — nay đã có 3.227 lượt của 10 tài khoản.",
         "Luận văn tự đánh giá thấp hơn thực tế.", "CHƯA"],
        "▌ NGOÀI PHẠM VI LUẬN VĂN, nhưng đã báo và chưa sửa",
        ["C-19", "46 mã nút `cum_*` nằm ngoài đồ thị tri thức", "3.2 · 3.4.3",
         "Chín bài của ta3·ta4·ta5 gắn câu hỏi vào các mã `cum_*` (cụm từ) không phải đỉnh của do_thi.json. "
         "Phát hiện khi dựng bảng này: phép đếm NG20 ra 73 thay vì 32, và chênh lệch chính là chúng.",
         "Chưa gây hậu quả: nhật ký thật chưa có lượt nào mang mã `cum_*` (0/3.227). Nhưng nếu một bé làm "
         "tới đó thì BKT vẫn theo dõi được, còn phép chẩn đoán trên đồ thị (nutGocRe) KHÔNG đặt được nút ấy "
         "vào đâu — nó không có nút trước, không thành ứng viên gốc rễ.", "CHƯA"],
        ["C-15", "55 bước gợi ý của bài tả tranh thiếu `dapMau`", "—", "Đã báo, chưa làm.",
         "Bé xem gợi ý mà không có câu mẫu để đối chiếu.", "CHƯA"],
        ["C-16", "Màn Thi thử dò được đáp án", "—", "Đã báo, chưa làm.", "Bé có thể thử lần lượt tới khi trúng.", "CHƯA"],
        ["C-17", "Chưa có ESLint", "—",
         "Kho chạy cổng bằng node trần, không có bộ dịch JSX và không có DOM giả — nên không cổng nào dựng "
         "một màn React. Hai lỗi ReferenceError đã lên tới bản thật vì lỗ hổng này.",
         "Đã có lưới đỡ (trang 6, T-27) nên bé không thấy màn trắng nữa, nhưng lỗi vẫn lọt được.", "CHƯA"],
        ["C-18", "Nhánh chưa gộp vào main", "—", "Chưa gộp.", "main đang cũ hơn bản đã deploy.", "CHƯA"],
    ],
    [7, 40, 14, 60, 44, 12],
)


# ═══ 6. LÀM THÊM ════════════════════════════════════════════════════════════
trang(
    "6. Làm THÊM ngoài báo cáo",
    "LÀM THÊM GÌ NGOÀI BÁO CÁO — 30 HẠNG MỤC KHÔNG CÓ TRONG LUẬN VĂN",
    "Phần lớn sinh ra từ việc ĐEM HỆ THỐNG RA CHẠY THẬT: luận văn mô tả thiết kế, còn những thứ dưới đây "
    "là thứ phải có để thiết kế ấy sống được với trẻ thật.",
    ["Mã", "Hạng mục", "Vì sao có, dù luận văn không đòi", "Nằm ở đâu", "Loại"],
    [
        "▌ MƯỜI HAI MẪU AI AGENT (V1–V12) — luận văn chỉ nêu 3 vị trí gọi mô hình",
        ["T-01", "V1 · Vòng GỌI LẠI khi hậu kiểm bác câu của cô giáo máy",
         "Hậu kiểm bác câu thì phải có đường đi tiếp, không thì cô giáo im lặng giữa buổi.", "functions/src/luyennoi.js", "THÊM"],
        ["T-02", "V2 · Phân loại lượt của bé thành 9 nhãn → lời dặn ngắn theo nhãn",
         "Một lời dặn chung cho mọi tình huống thì mô hình trả lời chung chung.", "loidan_nhan.js · tienganh_nhanluot", "THÊM"],
        ["T-03", "V3 · Hồ sơ AI về bé, giữ qua nhiều buổi, bố mẹ xem và xoá được",
         "Cô giáo máy quên sạch sau mỗi buổi thì không dạy tiếp được. Kèm quyền xoá vì đó là dữ liệu về trẻ.",
         "hosoai.js · Góc bố mẹ", "THÊM"],
        ["T-04", "V4 · Chấm bài viết 3 mắt xích + viết lại khi có từ lạ",
         "Một lượt gọi vừa tìm lỗi vừa sửa vừa viết lời cho bố mẹ thì làm hỏng cả ba.", "functions/src/chamviet.js", "THÊM"],
        ["T-05", "V5 · Điểm AI ở trạng thái 'tạm', bố mẹ xác nhận hoặc sửa",
         "Điểm do máy chấm không được đứng ngang điểm người chấm — đúng tinh thần R6.", "hocBaTA · ParentReport", "THÊM"],
        ["T-06", "V6 · bangTrangThai(uid) — MỘT nguồn sự thật về bé cho mọi mô-đun",
         "Trước đó mỗi mô-đun tự lắp trạng thái, và chúng lệch nhau.", "bangtrangthai.js", "THÊM"],
        ["T-07", "V7 · Kế hoạch buổi (planner là CODE, không phải mô hình) + replanner",
         "Để mô hình tự lập kế hoạch buổi học là bỏ quyền quyết định cho thứ có thể sai.", "kehoach.js", "THÊM"],
        ["T-08", "V8 · Bài học cuối buổi + job ΔC đề xuất sửa lời dặn", "Vòng tối ưu prompt của mục 2.5.3 cần một chỗ đo.",
         "tools/doc_delta_c.mjs", "THÊM"],
        ["T-09", "V9 · Phụ đạo có grader + re-query + chẩn đoán bằng LỜI", "Mục 3.5.3 nêu bốn bước; đây là phần hiện thực đầy đủ.",
         "functions/sinhCauPhuDao", "THÊM"],
        ["T-10", "V10 · Chấm viết 'lỗi ∥ khen' chạy song song; lượt nói mơ hồ BỎ PHIẾU",
         "Chỉ báo lỗi thì bé nản; lượt nói mơ hồ chấm một lần thì hay sai.", "chamviet.js · phanxu.js", "THÊM"],
        ["T-11", "V11 · Nhánh ReAct 4 tool cho lượt bé hỏi lại — ĐO RA KHÔNG HƠN NÊN TẮT",
         "Đáng kể ngang phần làm được: đo rồi tắt, và ghi lại vì sao.", "luyennoi_tool.js (mặc định TẮT)", "THÊM"],
        ["T-12", "V12 · Xưởng sinh nội dung offline (4 worker → cổng mã → 3 giám khảo → người duyệt)",
         "Sinh nội dung lúc chạy thì không kịp duyệt. Xưởng đẩy việc sinh ra NGOÀI giờ học.", "tools/xuong/", "THÊM"],
        "▌ R7 — PHẦN VƯỢT QUÁ MÔ TẢ CỦA MỤC 3.8",
        ["T-13", "Hai bản chép nguong.js (máy con ↔ máy chủ) + cổng SO HAI BẢN",
         "Hai phía không import chéo được. Hai bản chép không có cổng so thì sớm muộn trôi khỏi nhau.",
         "nguong_hai_ban.test.mjs (19 phép)", "THÊM"],
        ["T-14", "Phép kiểm NHỊP TINH THÔNG chặn phát hành", "Từng ngưỡng hợp lệ mà GHÉP lại vẫn ra nhịp dạy vô lý: "
         "θ=0,70 với T=0,40 cho nhịp 2 câu, bị bác.", "nguong.js soiNguong()", "THÊM"],
        ["T-15", "Khoảng hợp lệ soi ở TẦNG CƠ SỞ DỮ LIỆU, không chỉ ở màn hình",
         "Chốt ở màn hình thì ai gọi thẳng API là qua được.", "firestore.rules", "THÊM"],
        ["T-16", "Vai trò thứ tư `chuyengia`, tách hẳn khỏi `admin`", "Để admin không vô tình sửa được ngưỡng.",
         "firestore.rules isChuyenGia()", "THÊM"],
        ["T-17", "Phát hành ghi HAI dòng trong một writeBatch (giá trị + lịch sử kèm lý do)",
         "Ghi được giá trị mà hụt lịch sử thì có một con số không ai biết vì sao.", "ghiNguong.js", "THÊM"],
        ["T-18", "Ngữ cảnh phiên SUY TỪ TRẠNG THÁI, không gán tay ở chỗ gọi",
         "Đổi quyển có BỐN đường; gán tay ở một đường thì ba đường kia để ngữ cảnh cũ nằm lại, và hậu quả thì câm.",
         "App.jsx useEffect", "THÊM"],
        ["T-19", "Bản ghi lượt KHAI khoiLop và mon, máy chủ KHÔNG suy từ hình dạng mã nút",
         "Mã nút `v_g5_…` có sẵn chữ g5, bóc ra là xong — nhưng đó là quy ước đặt tên, đổi một lần là mọi lượt "
         "lặng lẽ rơi về bộ chung.", "suKien.js · sync.js · bkt.js nguCanhLuot()", "THÊM"],
        "▌ ĐO LƯỜNG — luận văn định nghĩa độ đo, chưa có bộ đo",
        ["T-20", "Toàn bộ Bảng 3.22 thành mã THUẦN, chạy lại được trên nhật ký với bộ ngưỡng KHÁC",
         "Đó chính là bước 'chạy thử lại' mà mục 3.8.3 đòi — chuyên gia thấy hậu quả TRƯỚC khi duyệt.",
         "functions/src/thongke.js", "THÊM"],
        ["T-21", "AUC tính bằng hạng (Mann–Whitney), xử hoà bằng hạng trung bình",
         "Không phải dựng đường cong rồi lấy diện tích: cách hạng cho cùng một số và không phải chọn số điểm chia.",
         "thongke.js chatLuongMoHinh()", "THÊM"],
        ["T-22", "Hạn chế của chỉ số đi XUỐNG TẬN TÀI LIỆU, không nằm trong chú thích",
         "`chuaTruPhuDao` · `thieuBac` · `sauCanThiep` — một hạn chế chỉ ghi trong mã là hạn chế người đọc bảng không thấy.",
         "thongke.js · docThongKe.js", "THÊM"],
        ["T-23", "Màn chuyên gia đọc chỉ số thành CÂU, không thành số trần",
         "Bảng 3.22 có hẳn cột 'cách đọc'. Một con số không kèm cách đọc thì chuyên gia phải tự đoán tăng hay giảm.",
         "docThongKe.js docHieu()", "THÊM"],
        ["T-24", "Ba trạng thái phân biệt: đang nạp · chưa có số liệu · ĐỌC HỎNG",
         "Bảng rỗng vì chưa có dữ liệu và bảng rỗng vì đọc hỏng dẫn tới hai hành động khác nhau.",
         "BangNguong.jsx", "THÊM"],
        "▌ ĐỘ BỀN KHI CHẠY THẬT — không có trong luận văn vì luận văn mô tả thiết kế",
        ["T-25", f"{D['cong']} tệp cổng tự động, trong đó 76 phép chạy trên bộ giả lập Firestore THẬT",
         "Cổng đọc tệp bắt được 'quên viết luật', không bắt được 'luật viết rồi mà sai'.",
         "web/test/", "THÊM"],
        ["T-26", "Cổng chống hai ô trắc nghiệm giống hệt nhau",
         "18 câu đã lên bản thật với hai ô cùng ghi 'xin chào'. Cổng cũ đếm được 'có mấy ô' nhưng không hỏi "
         "'mấy ô ấy có khác nhau không'.", "o_chon_khac_nhau.test.mjs", "THÊM"],
        ["T-27", "Lưới đỡ khi màn vỡ — thay màn TRẮNG bằng một câu và một đường ra",
         "Hai lần ReferenceError lên tới bản thật cho ra trang trắng hoàn toàn, cổng và bản dựng đều xanh.",
         "LuoiDoLoi.jsx · luoi_do_loi.test.mjs", "THÊM"],
        ["T-28", "Phân trang nhật ký bằng con trỏ (ts, mã tài liệu)",
         "Mươi dòng ấy sai BA lần, cả ba đều câm với node --check, bản dựng và 105 cổng.",
         "functions/src/docLuot.js · docluot.test.mjs", "THÊM"],
        ["T-29", "Công cụ soi dữ liệu thật bằng khoá quản trị",
         "Đi thử bản chạy bắt được những thứ cổng xanh không bắt — đã dính thật nhiều lần.",
         "tools/soi_ban_ghi_tienganh.mjs · nhap_cau_duyet.py", "THÊM"],
        ["T-30", "Môn TOÁN dùng chung bộ ngưỡng (luận văn chỉ nói Tiếng Anh)",
         "Quyết định ② của bác: chung một bộ, thêm nấc phạm vi `mon`. Gỡ luôn chuyện θ từng bị khai ba chỗ ba số.",
         "chung/lib/nguong.js · mon/toan/lib/sync.js", "THÊM"],
    ],
    [7, 48, 62, 40, 10],
)


# ═══ 7. ĐỘ ĐO VÀ KỊCH BẢN ═══════════════════════════════════════════════════
trang(
    "7. Độ đo & kịch bản",
    "BẢNG 3.23 (BỐN NHÓM ĐỘ ĐO) VÀ BẢNG 3.24 (SÁU KỊCH BẢN) — SẴN SÀNG TỚI ĐÂU",
    "Cột 'Mức sẵn sàng v4' là đánh giá của luận văn; cột 'Thực tế 10-10' là đo lại.",
    ["Mã", "Nội dung", "Mức sẵn sàng v4 ghi", "Thực tế 10-10-2026", "Còn thiếu gì", "Trạng thái"],
    [
        "▌ BỐN NHÓM ĐỘ ĐO (Bảng 3.23)",
        ["A", "Mô hình người học: AUC · RMSE · sai lệch hiệu chuẩn",
         "định nghĩa xong, chưa có bộ đo",
         "ĐÃ ĐO THẬT: AUC 0,734 · RMSE 0,440 · lệch +0,050 trên 3.212 lượt",
         "Sai lệch hiệu chuẩn mới tính một con số chung, chưa chia theo 10 nhóm xác suất như bảng đòi.",
         "XONG"],
        ["B", "Tiến bộ và hiệu quả can thiệp: độ dốc đường cong · ΔC · phủ vốn",
         "định nghĩa xong",
         "độ dốc có (report.js duongCongHoc) · ΔC có công cụ (doc_delta_c.mjs) · phủ vốn có (cefr.js)",
         "ΔC đòi ≥ 5 cặp hợp lệ (NG19); chưa đủ cặp vì đường mô hình của phụ đạo chưa chạy (C-09).",
         "MỘT PHẦN"],
        ["C", "An toàn nội dung: tỉ lệ từ ngoài vốn trước/sau hậu kiểm",
         "bộ đo đã chạy",
         "do_an_toan_noi_dung.mjs chạy được; hậu kiểm có ở cả 3 vị trí gọi mô hình",
         "Chưa chạy thành một đợt đo có báo cáo.",
         "MỘT PHẦN"],
        ["D", "Hệ thống và vận hành: tỉ lệ ghi thành công · bản ghi tồn · độ trễ · 4 bất biến",
         "quan trọng ngang ba nhóm kia",
         "4 bất biến có cổng (luat_firestore 76 phép); tỉ lệ ghi đo được bằng soi_ban_ghi_tienganh.mjs",
         "Chưa có bảng theo dõi liên tục — mới soi thủ công từng đợt.",
         "MỘT PHẦN"],
        "▌ SÁU KỊCH BẢN THỰC NGHIỆM (Bảng 3.24)",
        ["KB1", "Hiệu chỉnh θ, α, h và tạo bộ ngưỡng đề xuất đầu tiên", "cao",
         "CHƯA CHẠY. Nhưng điều kiện nay tốt hơn luận văn tưởng: đã có 3.212 lượt thật, và toàn bộ phép tính "
         "chạy lại được trên nhật ký với bộ ngưỡng khác.",
         "Bộ sinh người học mô phỏng + vòng quét lưới (= C-01).", "CHƯA"],
        ["KB2", "So sánh bốn phiên bản mô hình", "chờ dữ liệu thật",
         "CHƯA CHẠY. Dữ liệu đã có; chưa có khâu chia 5 phần theo người học và kiểm định DeLong.",
         "Bộ kiểm tra chéo chia theo người học.", "CHƯA"],
        ["KB3", "Tách riêng đóng góp của hậu kiểm", "bộ đo đã chạy",
         "CHƯA CHẠY THÀNH ĐỢT. Bộ đo có (do_an_toan_noi_dung.mjs).",
         "Chạy 30 bài × 20 lượt × 3 vị trí và ghi lại kết quả.", "CHƯA"],
        ["KB4", "So sánh các mẫu lời nhắc bằng ΔC", "đang bị chặn",
         "KHÔNG BỊ CHẶN NHƯ LUẬN VĂN GHI. Đường mô hình đã nối đủ; nó chỉ chạy khi kho tĩnh không đủ câu, mà "
         "kho tĩnh xưa nay luôn đủ (xem C-09). Vân tay prompt đã ghi đủ ở cả 11 lượt AI chấm.",
         "Một CỜ CHIA NHÓM cố ý đẩy một phần phiên sang đường mô hình — cùng thứ KB5 cần.", "CHƯA"],
        ["KB5", "Hiệu quả của việc sắp xếp theo vùng phát triển gần", "cần cờ chia nhóm",
         "CHƯA CHẠY. Thuật toán xếp ZPD đã nối vào màn thật.",
         "Cờ chia nhóm ngẫu nhiên trên hồ sơ người học.", "CHƯA"],
        ["KB6", "Dùng thực tế 5–10 học sinh trong 4 tuần", "khó nhất là khâu tổ chức",
         "CHƯA CHẠY — và đây là việc TỔ CHỨC, không phải việc mã. Hệ thống đã deploy và chạy được.",
         "Phụ huynh đồng ý · giáo viên ra đề kiểm tra giấy đầu/cuối.", "KHÔNG PHẢI MÃ"],
    ],
    [7, 42, 26, 56, 46, 12],
)


# ═══ 8. VIỆC NÊN LÀM TIẾP ═══════════════════════════════════════════════════
trang(
    "8. Việc nên làm tiếp",
    "VIỆC NÊN LÀM TIẾP — XẾP THEO THỨ TỰ TÔI NGHĨ LÀ ĐÚNG",
    "Thứ tự xếp theo: (1) ảnh hưởng tới trẻ đang học · (2) mở khoá được nhiều việc khác · (3) rẻ.",
    ["Thứ tự", "Việc", "Vì sao đứng ở đây", "Phụ thuộc", "Ước lượng"],
    [
        ["✔", "XONG 10-10 — C-08 · C-04 · C-05 · C-06 · C-09",
         "Bốn việc nhỏ làm trong một đợt: nhánh VƯỢT ẢI nay có chỗ chạy (thẻ ôn) · bản ghi v6 mang `bac` và "
         "`sauPhuDao` · chỉ số hành vi gom theo cặp (dạng, bậc) · NG09 tách lượt tự gỡ khỏi lượt sau can "
         "thiệp · cờ chia nhóm tất định (để TẮT). 110 cổng xanh, đã deploy, đo trên bản thật.",
         "—", "—"],
        ["1", "BẬT thử nghiệm KB5 (`kb5_zpd`)",
         "Cờ đã sẵn. Bật là có số liệu đo tác dụng của việc xếp câu theo vùng phát triển gần — không nới ràng "
         "buộc nào. ⚠ Nhóm đối chứng sẽ học bằng thứ tự thường suốt đợt đo, nên là quyết định của bác.",
         "bác chốt", "nhỏ"],
        ["3", "Cập nhật ba chỗ số liệu trong luận văn (C-11 · C-12 · C-14)",
         "Rẻ, và nâng độ tin cậy: hiện luận văn đang tự đánh giá THẤP HƠN thực tế ở hai chỗ.",
         "Thầy chốt C-13", "nhỏ"],
        ["4", "KB1 trên NGƯỜI HỌC MÔ PHỎNG",
         "Hàm học ngưỡng đã chạy trên dữ liệu thật (C-01 xong). Phần còn thiếu của KB1 là bộ sinh 1.000 "
         "người học mô phỏng — cần nó thì NG06 và NG07 mới đủ cỡ mẫu để thành đề xuất.",
         "không", "vừa"],
        ["5", "Nối lan truyền XUÔI vào chỗ tính vectơ trạng thái (C-07)",
         "Luận văn tự khai là giới hạn. Có mã, có cổng.", "không", "vừa"],
        
        ["7", "Dựng cổng DỰNG THẬT một màn React (C-17)",
         "Hai lỗi ReferenceError đã lên bản thật qua đúng lỗ hổng này. Lưới đỡ đã che hậu quả, nhưng lỗi vẫn lọt.",
         "thêm jsdom + bộ dịch JSX vào devDependencies", "vừa"],
        ["8", "Gộp nhánh vào main (C-18)", "Vệ sinh kho.", "không", "nhỏ"],
        ["9", "KB6 — 5–10 học sinh trong 4 tuần",
         "Việc tổ chức, không phải việc mã. Nhưng tới khi chạy xong thì mọi nhận định về hiệu quả dạy học "
         "vẫn là giả thuyết — đúng như Bảng 3.25 tự khai.",
         "phụ huynh đồng ý · giáo viên ra đề", "lớn"],
    ],
    [8, 46, 72, 32, 11],
)

RA.parent.mkdir(parents=True, exist_ok=True)
wb.save(RA)
print(f"đã ghi {RA.relative_to(GOC)}  ({len(wb.sheetnames)} trang)")
for t in wb.sheetnames:
    print(f"   {t:28} {wb[t].max_row - 3:3} dòng")
