#!/usr/bin/env python3
"""XUẤT BẢNG BÀI ĐỌC ĐỂ BÁC REVIEW → docs/bang_bai_doc.xlsx

    python3 tools/xuat_bang_doc.py

Toàn bộ bài đọc của ba quyển ta3 · ta4 · ta5 — cả bài của TỪNG UNIT lẫn bài ÔN
TẬP CHƯƠNG — mỗi CÂU HỎI một dòng, để bác đọc và sửa thẳng trong Excel. Sửa
xong thì `python3 tools/nap_bang_doc.py` nạp ngược vào bảng nguồn.

── VÌ SAO XUẤT TỪ `data/tienganh/canh_lopN.json` ──
Đó là bản khai ĐÃ DỰNG, tức đúng thứ đang chạy trong app. `canh_de_xuat.py` là
bảng nguồn viết tay, nhưng nó gói câu hỏi trong MỘT ô chữ dài — đọc thì được,
soát từng câu thì không. Hai bên luôn khớp vì bản khai sinh ra từ chính nó.

── ĐƯỜNG ĐI HAI CHIỀU ──

    tools/canh_de_xuat.py  ──soan_canh.py──▶  data/tienganh/canh_lopN.json
            ▲                                          │
            │                                          │ tệp này
            └────────── tools/nap_bang_doc.py ◀──── docs/bang_bai_doc.xlsx
                                                    (bác sửa ở đây)

Nạp ngược ghi vào `canh_de_xuat.py` chứ KHÔNG ghi thẳng vào bản khai: bản khai
bị `soan_canh.py` dựng lại là mất. Một nguồn sự thật, không hai.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/bang_bai_doc.xlsx"
QUYEN = {3: "ta3", 4: "ta4", 5: "ta5"}

HUONG_DAN = [
    ("BẢNG BÀI ĐỌC — CÁCH DÙNG", ""),
    ("", ""),
    ("Sheet “CÂU HỎI”",
     "Mỗi dòng một câu hỏi. Bác sửa thẳng vào sáu cột màu vàng: CÂU HỎI (EN) · "
     "DÒNG PHỤ (VI) · ĐÁP ÁN ĐÚNG · MỒI 1 · MỒI 2 · MỒI 3. Cột cuối “BÁC GHI” "
     "để bác dặn thêm — nó KHÔNG vào phần mềm, chỉ để hai bác cháu trao đổi."),
    ("Sheet “ĐOẠN ĐỌC”",
     "Mỗi dòng một bài. Sửa được cột ĐOẠN ĐỌC. ⚠ Sửa đoạn thì phải dựng lại "
     "TIẾNG ĐỌC (Kokoro) cho câu mới — bộ nạp sẽ báo, cháu chạy thêm một bước."),
    ("KHÔNG được sửa", "Cột MÃ BÀI và cột CÂU (T1 · T2 …) — đó là khoá để nạp "
     "ngược. Cũng đừng thêm dòng, đừng xoá dòng, đừng đổi thứ tự dòng."),
    ("Số lựa chọn",
     "Câu thường có ĐÁP ÁN + 3 MỒI. Câu Có/Không (Yes, it is. / No, it isn't.) "
     "chỉ có ĐÁP ÁN + 1 MỒI — để trống MỒI 2 và MỒI 3, đừng bịa thêm."),
    ("", ""),
    ("LUẬT SỐ MỘT — MỖI CÂU ĐÚNG MỘT ĐÁP ÁN",
     "Mồi phải SAI với BỨC TRANH ĐANG CHẠY và SAI với ĐOẠN ĐỌC. Ba chỗ hay "
     "trượt: (a) mồi nêu một vật CÓ trên tranh; (b) mồi là câu đoạn đọc đã nói, "
     "cùng chủ ngữ; (c) mồi bao trùm đáp án — “playing games” bao cả “playing "
     "chess”."),
    ("CÂU HỎI PHẢI KHỚP ĐÁP ÁN",
     "Hỏi “he” thì đáp phải là “He …”; hỏi “in the morning” thì đáp phải là "
     "việc buổi sáng. Dòng phụ tiếng Việt chỉ THU HẸP câu hỏi (đang hỏi ai, "
     "cái nào) — nó không đổi được nghĩa câu tiếng Anh."),
    ("DÒNG PHỤ CHỐT BẰNG THỨ NHÌN THẤY ĐƯỢC",
     "Chỗ đứng (bên trái · bên phải) · màu áo · dáng (đang ngồi) · vai (mẹ · "
     "bố) · tên riêng. Đừng chốt bằng chính đáp án (“bạn đang múa làm gì?”), "
     "và đừng chốt bằng thứ nét vẽ không vẽ ra."),
    ("VỐN TỪ",
     "Chỉ dùng chữ đã học TỚI BÀI ẤY (tích luỹ từ lớp 1). Cổng "
     "`tienganh_dochieu` soi lại và báo đỏ nếu có chữ lạ — cháu sẽ chạy sau khi "
     "nạp, nếu vướng sẽ hỏi lại bác."),
]


def bai_ten(k: dict) -> str:
    return (f"ÔN TẬP {k['chuong']}" if k.get("phamVi") == "chuong"
            else f"U{k['unit']:02d}")


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "CÂU HỎI"

    DAU = ["MÃ BÀI", "Quyển", "Bài", "Tên bài", "Tệp tranh", "ĐOẠN ĐỌC",
           "CÂU", "CÂU HỎI (EN)", "DÒNG PHỤ (VI)", "ĐÁP ÁN ĐÚNG",
           "MỒI 1", "MỒI 2", "MỒI 3", "BÁC GHI"]
    SUA = set(range(8, 14))          # cột H..M — bác sửa được
    ws.append(DAU)

    dong_bai = []
    n_cau = 0
    for lop in (3, 4, 5):
        kho = json.loads((GOC / f"data/tienganh/canh_lop{lop}.json")
                         .read_text("utf8"))
        for k in kho:
            tranh = k["id"].replace(":", "_").replace(".", "_") + ".png"
            doan = " ".join(k["doan"])
            dong_bai.append([k["id"], f"lớp {lop}", bai_ten(k), k["ten"],
                             tranh, doan, k.get("moTa", ""), ""])
            for i, h in enumerate(k["hoi"], 1):
                moi = list(h.get("moi") or []) + ["", "", ""]
                ws.append([k["id"], f"lớp {lop}", bai_ten(k), k["ten"], tranh,
                           doan, f"T{i}", h["hoi"], h.get("vi", ""), h["dap"],
                           moi[0], moi[1], moi[2], ""])
                n_cau += 1

    w2 = wb.create_sheet("ĐOẠN ĐỌC")
    w2.append(["MÃ BÀI", "Quyển", "Bài", "Tên bài", "Tệp tranh", "ĐOẠN ĐỌC",
               "Mô tả bức tranh (để đối chiếu)", "BÁC GHI"])
    for d in dong_bai:
        w2.append(d)

    w3 = wb.create_sheet("HƯỚNG DẪN")
    for a, b in HUONG_DAN:
        w3.append([a, b])

    # ── mặt bảng ─────────────────────────────────────────────────────────
    vang = PatternFill("solid", fgColor="FFF3CD")
    xanh = PatternFill("solid", fgColor="0B4EA8")
    xam = PatternFill("solid", fgColor="EEF2F7")
    for sheet, sua in ((ws, SUA), (w2, {6})):
        for i in range(1, sheet.max_column + 1):
            o = sheet.cell(row=1, column=i)
            o.font = Font(bold=True, color="FFFFFF")
            o.fill = xanh
            o.alignment = Alignment(vertical="center", wrap_text=True)
        for row in sheet.iter_rows(min_row=2):
            for o in row:
                o.alignment = Alignment(vertical="top", wrap_text=True)
                if o.column in sua:
                    o.fill = vang
                elif o.column <= 7:
                    o.fill = xam
        sheet.freeze_panes = "H2" if sheet is ws else "F2"
        sheet.auto_filter.ref = sheet.dimensions

    for cot, w in {"A": 20, "B": 8, "C": 11, "D": 26, "E": 24, "F": 62,
                   "G": 6, "H": 40, "I": 40, "J": 30, "K": 30, "L": 30,
                   "M": 30, "N": 30}.items():
        ws.column_dimensions[cot].width = w
    for cot, w in {"A": 20, "B": 8, "C": 11, "D": 28, "E": 24, "F": 78,
                   "G": 90, "H": 30}.items():
        w2.column_dimensions[cot].width = w
    w3.column_dimensions["A"].width = 34
    w3.column_dimensions["B"].width = 96
    for row in w3.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    w3.cell(row=1, column=1).font = Font(bold=True, size=14)
    for r in (3, 4, 5, 6, 8, 9, 10, 11):
        w3.cell(row=r, column=1).font = Font(bold=True)
    for i in range(1, ws.max_column + 1):
        get_column_letter(i)          # giữ openpyxl tính lại bề rộng

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   {len(dong_bai)} bài đọc · {n_cau} câu hỏi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
