#!/usr/bin/env python3
"""SOÁT BẢNG TỪ MÀN VIẾT — mỗi ô chữ có nghĩa nhờ LUẬT NÀO.

    tools/tts/.venv/bin/python tools/soat_vontu.py     → docs/soat_vontu.xlsx

── BẢN NÀY KHÁC BẢN ĐẦU Ở CHỖ NÀO ──

Bản đầu (22-08-2026) liệt kê 105 ô chữ KHÔNG có nghĩa tiếng Việt, để bác duyệt
xem chú nghĩa cho từng chữ thế nào. Sửa xong thì con số ấy về 0 — và một bảng
rỗng thì bác không soi lại được gì.

Nên bảng nay lật ngược câu hỏi: **mỗi ô chữ đang có nghĩa nhờ luật nào**, và
luật nào là MÁY suy, luật nào là TÔI VIẾT TAY. Chỗ tôi viết tay mới là chỗ đáng
bác đọc lại — máy suy sai thì cổng bắt được, còn tôi viết sai nghĩa thì không
gì bắt được.

── SÁU LUẬT, XẾP THEO MỨC ĐÁNG NGỜ ──

    từ vựng · tra thẳng     nghĩa lấy nguyên từ `knowledgeCore.vocabulary`.
                            Không phải việc của tôi, không cần soi.
    cụm giữ nguyên          "break time" · "table tennis" giữ NGUYÊN CỤM, lấy
                            nghĩa của cụm. Đây là luật gỡ được 48/105 ô.
    cụm · khớp thể chia     sách dạy "collect seashells", đoạn kể "We collected
                            seashells." — cùng một mục từ vựng.
    suy số nhiều            `books` ← `book`. CHỈ danh từ: tiếng Việt không đánh
                            dấu số nhiều nên nghĩa không đổi.
    ⚠ nghĩa tôi viết tay    không có nguồn nào ngoài tôi. CHỖ CẦN BÁC ĐỌC.
    chữ nối · không chú     `KHONG_CHU` — chú nghĩa từ điển cho chúng là dạy sai
                            (`can` trong "I can see" không phải "cái lon").

── ⚠ HAI LỖI NẶNG HƠN CHUYỆN THIẾU NGHĨA — cả hai ĐÃ SỬA ──

1. NGHĨA CHỈ NẰM Ở `title=`. `VietBai.jsx` từng bày nghĩa bằng thuộc tính `title`
   của thẻ nút, tức TOOLTIP, chỉ hiện khi rê chuột. Trên máy tính bảng và điện
   thoại — thứ bé thật sự dùng — KHÔNG BAO GIỜ hiện. Nên 2075 ô ĐÃ CÓ nghĩa cũng
   vô hình y như 606 ô không có. Nay vẽ thành chữ nhỏ ngay dưới từ.

2. GẠCH NỐI BỊ CẮT. Bộ tách chữ từng dùng `[A-Za-z][A-Za-z']*`, nên `T-shirt` đẻ
   thêm hai ô rác (ta4 U18 có ĐỦ CẢ BA ô), `Mid-Autumn Festival` thành ba ô rời
   mà không có ô gạch nối nào để bé ghép lại, `twenty-nine` rụng mất nửa sau.

Cổng canh cả hai: `web/test/tienganh_bangtu_viet.test.mjs`.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "tools"))
from sinh_bai_tranh import (KHONG_CHU, NGHIA_LE, QUYEN,  # noqa: E402
                            cum_tu_vung, khuon_cum, nghia_goc)

RA = GOC / "docs/soat_vontu.xlsx"

TRA, TRA_KHAC, CUM, CHIA, SO_NHIEU, TAY, NOI, LA = (
    "từ vựng · tra thẳng", "từ vựng · bài khác chú khác", "cụm giữ nguyên",
    "cụm · khớp thể chia", "suy số nhiều", "⚠ nghĩa tôi viết tay",
    "chữ nối · cố ý không chú", "⚠ CHƯA RÕ TỪ ĐÂU RA",
)
# Xếp theo mức đáng bác đọc lại, không xếp theo abc.
THU_TU = [TAY, TRA_KHAC, CHIA, CUM, SO_NHIEU, TRA, NOI, LA]


def kho_tu(lop: int) -> dict[str, str]:
    """Bảng nghĩa dựng ĐÚNG như `sinh_bai_tranh.tu_trong_tranh` dựng."""
    ng: dict[str, str] = {}
    for l in range(1, lop + 1):
        tm = GOC / f"web/public/content/{QUYEN[l]}"
        for f in sorted(tm.glob(f"DL_{QUYEN[l].upper()}_B*.json")):
            b = json.loads(f.read_text("utf8"))
            for v in b["knowledgeCore"]["vocabulary"]:
                ng.setdefault(v["tu"], v.get("nghia") or "")
    return ng


def moi_nghia_cua_tu() -> dict[str, dict[str, list[str]]]:
    """Mọi nghĩa mà SÁCH từng chú cho một từ, kèm bài nào chú thế.

    Bài phạm vi CHƯƠNG do `sinh_vietbai_tienganh.py` sinh, và nó lấy `nghia` ngay
    ở BÀI CHỨA TỪ chứ không tích luỹ. Nên nghĩa hợp lệ mà bảng tích luỹ tra không
    ra — phải hỏi "sách có chú thế ở đâu đó không", chứ không hỏi "bảng của tôi
    có khớp không".
    """
    ra: dict[str, dict[str, list[str]]] = {}
    for lop, q in QUYEN.items():
        for f in sorted((GOC / f"web/public/content/{q}").glob(
                f"DL_{q.upper()}_B*.json")):
            b = json.loads(f.read_text("utf8"))
            for v in b["knowledgeCore"]["vocabulary"]:
                if v.get("nghia"):
                    ra.setdefault(v["tu"], {}).setdefault(
                        v["nghia"], []).append(b.get("id", f.stem))
    return ra


def xet(tu: str, nghia: str, kho: dict, cum: list,
        sach: dict | None = None) -> tuple[str, str]:
    """Ô này có nghĩa nhờ luật nào. Trả (luật, nguồn).

    ⚠ `kho` phải là bảng nghĩa TÍCH LUỸ TỚI ĐÚNG LỚP của bài ấy, không phải bảng
    của lớp 5. Bảng dựng bằng `setdefault` nên mục nào gặp TRƯỚC thì thắng: soi
    bài lớp 3 bằng bảng lớp 5 thì `table tennis` ra "bóng bàn" trong khi bài thật
    ghi "môn bóng bàn", và 30 ô lành bị báo là không truy được nguồn.
    """
    if tu.lower() in KHONG_CHU:
        return NOI, ""
    if not nghia:
        return LA, "ô TRỐNG NGHĨA"
    if kho.get(tu) == nghia:
        return ((CUM if re.search(r"[ \-]", tu) else TRA),
                f"mục từ vựng “{tu}”")
    # Cụm chia thể: mục từ vựng nào có đúng nghĩa ấy và khớp được chữ này.
    for goc, g in cum:
        if g == nghia and khuon_cum(goc).fullmatch(tu):
            return (CUM if goc.lower() == tu.lower() else CHIA), f"cụm “{goc}”"
    if NGHIA_LE.get(tu.lower()) == nghia:
        return TAY, "khai trong NGHIA_LE"
    if nghia_goc(tu, kho) == nghia:
        return SO_NHIEU, f"số ít “{tu[:-1]}”"
    o_sach = (sach or {}).get(tu, {})
    if nghia in o_sach:
        return TRA_KHAC, f"bài {o_sach[nghia][0]} chú thế"
    return LA, "không truy được nguồn"


def main() -> int:
    # ── mỗi CHỮ một dòng; gom các bài dùng nó, và NHỚ LỚP để soi cho đúng bảng ──
    o_cua: dict[tuple[str, str], set[str]] = {}
    lop_cua_o: dict[tuple[str, str], int] = {}
    tong_o = 0
    for lop, q in QUYEN.items():
        tep = GOC / f"web/public/content/{q}/vietbai.json"
        if not tep.exists():
            continue
        for b in json.loads(tep.read_text("utf8")):
            for o in b["vonTu"]:
                tong_o += 1
                k = (o["tu"], o["nghia"])
                o_cua.setdefault(k, set()).add(b["id"])
                # Lớp NHỎ NHẤT dùng ô này — chính là bảng nghĩa đã sinh ra nó.
                lop_cua_o[k] = min(lop_cua_o.get(k, lop), lop)

    kho_moi_lop = {l: kho_tu(l) for l in QUYEN}
    cum_moi_lop = {l: cum_tu_vung(kho_moi_lop[l]) for l in QUYEN}

    sach = moi_nghia_cua_tu()

    dong = []
    for (tu, ng), bai in o_cua.items():
        l = lop_cua_o[(tu, ng)]
        luat, nguon = xet(tu, ng, kho_moi_lop[l], cum_moi_lop[l], sach)
        dong.append((tu, ng, luat, nguon, sorted(bai)))
    dong.sort(key=lambda x: (THU_TU.index(x[2]), x[0].lower()))

    dem: dict[str, int] = {}
    for _, _, luat, _, _ in dong:
        dem[luat] = dem.get(luat, 0) + 1

    # ══ Excel ══
    wb = Workbook()
    dam = Font(bold=True, color="FFFFFF")
    nen = PatternFill("solid", fgColor="2F4A6B")
    vang = PatternFill("solid", fgColor="FFF3CD")
    do = PatternFill("solid", fgColor="F8D7DA")
    tren = Alignment(vertical="top", wrap_text=True)

    def dung_bang(ws, dau, rong):
        ws.append(dau)
        for c in ws[1]:
            c.font, c.fill = dam, nen
        for c, r in zip("ABCDEFG", rong):
            ws.column_dimensions[c].width = r

    def don(ws):
        for r in ws.iter_rows(min_row=1):
            for c in r:
                c.alignment = tren
        ws.freeze_panes = "A2"

    ws = wb.active
    ws.title = "Mỗi ô nhờ luật nào"
    dung_bang(ws, ["Chữ trên ô", "Nghĩa bé đọc được", "Luật", "Nguồn",
                   "Bài dùng"], (28, 34, 24, 30, 46))
    for tu, ng, luat, nguon, bai in dong:
        ws.append([tu, ng, luat, nguon, " · ".join(bai)])
        if luat == TAY:
            for c in ws[ws.max_row]:
                c.fill = vang
        elif luat == LA:
            for c in ws[ws.max_row]:
                c.fill = do
    don(ws)

    w2 = wb.create_sheet("Nghĩa tôi viết tay")
    dung_bang(w2, ["Chữ", "Nghĩa tôi viết", "Bài dùng"], (24, 40, 60))
    for tu, ng, luat, _, bai in dong:
        if luat == TAY:
            w2.append([tu, ng, " · ".join(bai)])
    don(w2)

    # ── PHÁT HIỆN KÈM: cùng một từ, sách chú hai nghĩa khác nhau ở hai bài ──
    #
    # Không phải lỗi của bộ sinh, mà là chuyện trong chính dữ liệu sách. Bé gặp
    # `bakery` ở màn này là "hiệu bánh mì", màn kia là "tiệm bánh". Không sai
    # nghĩa, nhưng hai mặt chữ cho một từ thì bé khó nhận ra là MỘT thứ.
    dang_dung = {tu for tu, _, _, _, _ in dong}
    hai_nghia = {tu: ng for tu, ng in sach.items()
                 if len(ng) > 1 and tu in dang_dung}
    w5 = wb.create_sheet("Một từ hai nghĩa")
    dung_bang(w5, ["Chữ", "Mấy kiểu", "Các nghĩa · và bài chú thế",
                   "Bác chốt dùng nghĩa nào"], (22, 10, 78, 26))
    # ⚠ KHÔNG PHẢI DÒNG NÀO CŨNG LÀ LỖI, và bộ soi không tự phân biệt được:
    #   · `can` = "cái lon" / "có thể" và `cook` = "đầu bếp" / "nấu ăn" là TỪ
    #     ĐỒNG ÂM THẬT — hai nghĩa đều đúng, sách chú đúng chỗ;
    #   · `bakery` = "hiệu bánh mì" / "tiệm bánh" và `chips` = "khoai tây chiên"
    #     / "khoai tây rán" mới là CHÚ LỆCH — một thứ, hai mặt chữ.
    # Phân biệt hai loại ấy cần người đọc, nên bảng để trống một cột cho bác.
    w5.append(["⚠ Không phải dòng nào cũng là lỗi", "",
               "`can` = cái lon / có thể là TỪ ĐỒNG ÂM THẬT — hai nghĩa đều "
               "đúng. Còn `bakery` = hiệu bánh mì / tiệm bánh là CHÚ LỆCH: một "
               "thứ mà bé gặp hai mặt chữ ở hai màn. Máy không phân biệt được "
               "hai loại này.", ""])
    for c in w5[2]:
        c.fill = vang
    for tu in sorted(hai_nghia, key=str.lower):
        ng = hai_nghia[tu]
        w5.append([tu, len(ng),
                   "   |   ".join(f"“{k}” ({', '.join(v[:2])})"
                                  for k, v in ng.items()), ""])
    don(w5)

    w3 = wb.create_sheet("Hai lỗi đã sửa")
    dung_bang(w3, ["Lỗi", "Ở đâu", "Bé chịu hậu quả gì", "Nay thế nào"],
              (32, 46, 54, 50))
    w3.append([
        "Nghĩa tiếng Việt chỉ là tooltip",
        "web/src/mon/tienganh/components/VietBai.jsx — title={v.nghia}",
        "Trên máy tính bảng và điện thoại tooltip KHÔNG BAO GIỜ hiện, nên bé "
        "không đọc được nghĩa của BẤT KỲ ô nào — kể cả 2075 ô đã có nghĩa.",
        "Vẽ thành chữ nhỏ ngay dưới từ. Đã mở bản chạy thật xem tận mắt. "
        "Cổng `tienganh_bangtu_viet` canh, đảo chiều thử rồi.",
    ])
    w3.append([
        "Gạch nối bị cắt thành ô rời",
        "tools/sinh_bai_tranh.py — bộ tách chữ [A-Za-z][A-Za-z']*",
        "Bé không ghép lại được vì không có ô gạch nối nào. Bài ta4 U18 hiện "
        "ĐỦ CẢ BA ô “T-shirt” · “T” · “shirt”.",
        "Bộ tách chữ giữ gạch nối. `Mid-Autumn Festival` nay là MỘT ô.",
    ])
    w3.append([
        "Cụm bị xé thành chữ lẻ",
        "tools/sinh_bai_tranh.py — bảng nghĩa tra bằng NGUYÊN VĂN khoá",
        "48/105 ô trống nghĩa. Và nặng hơn: chữ lẻ ĐỔI NGHĨA khi rời cụm — "
        "“table tennis” là bóng bàn còn `tennis` một mình là quần vợt, "
        "“first floor” kiểu Anh là TẦNG HAI, “set square” là cái ê-ke.",
        "Giữ nguyên cụm, khớp cả khi động từ đầu cụm chia thể. Nhờ thế KHÔNG "
        "phải chọn nghĩa cho chữ lẻ — 6 chỗ định hỏi bác chốt tự tan.",
    ])
    don(w3)

    w4 = wb.create_sheet("Tổng hợp")
    dung_bang(w4, ["Luật", "Số chữ", "Ai chịu trách nhiệm"], (26, 10, 62))
    ai = {
        TAY: "TÔI — không có nguồn nào khác. Sai thì không cổng nào bắt được.",
        TRA_KHAC: "sách · nhưng là mục từ vựng ở BÀI KHÁC, chú khác đi một chút "
                  "— xem trang “Một từ hai nghĩa”",
        CHIA: "máy · suy từ mục từ vựng của sách",
        CUM: "sách · nghĩa của chính cụm sách dạy",
        SO_NHIEU: "máy · chỉ danh từ số nhiều",
        TRA: "sách · tra thẳng knowledgeCore.vocabulary",
        NOI: "cố ý bỏ trống — chú nghĩa cho chữ nối là dạy sai",
        LA: "⚠ KHÔNG TRUY ĐƯỢC — phải xem bằng mắt",
    }
    for k in THU_TU:
        if dem.get(k):
            w4.append([k, dem[k], ai[k]])
    w4.append(["TỔNG chữ khác nhau", len(dong), f"{tong_o} ô trên toàn bộ bài"])
    don(w4)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)

    print(f"→ {RA.relative_to(GOC)}  ({len(dong)} chữ khác nhau · {tong_o} ô)")
    for k in THU_TU:
        if dem.get(k):
            print(f"   {dem[k]:5}  {k}")
    if dem.get(LA):
        print("   ✗ có ô không truy được nguồn nghĩa — xem trang đầu, dòng tô đỏ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
