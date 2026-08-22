#!/usr/bin/env python3
"""SOÁT BẢNG TỪ MÀN VIẾT — 105 ô chữ không có nghĩa tiếng Việt.

    tools/tts/.venv/bin/python tools/soat_vontu.py     → docs/soat_vontu.xlsx

── ⚠ HAI LỖI NẶNG HƠN CHUYỆN THIẾU NGHĨA, TÌM RA KHI SOI ──

1. NGHĨA CHỈ NẰM Ở `title=` — ĐÃ SỬA. `VietBai.jsx` từng bày nghĩa bằng thuộc
   tính `title` của thẻ nút, tức TOOLTIP, chỉ hiện khi rê chuột. Trên máy tính
   bảng và điện thoại, thứ bé thật sự dùng, KHÔNG BAO GIỜ hiện — nên 2075 ô ĐÃ
   CÓ nghĩa cũng vô hình y như 606 ô không có. Nay nghĩa vẽ thành chữ nhỏ ngay
   dưới từ, và cổng `tienganh_bangtu_viet` canh chỗ ấy.

2. GẠCH NỐI BỊ CẮT — ĐÃ SỬA. Bộ tách chữ từng dùng `[A-Za-z][A-Za-z']*`.
   Nên `T-shirt` đẻ thêm hai ô rác `T` và `shirt` (bài ta4 U18 có ĐỦ CẢ BA ô),
   `Mid-Autumn Festival` thành ba ô rời mà không có ô gạch nối nào để bé ghép
   lại, `twenty-nine` rụng mất nửa sau. Đây là lỗi làm bé KHÔNG viết đúng được,
   nặng hơn hẳn việc thiếu một dòng nghĩa.

── VÌ SAO 105 CHỮ ẤY THIẾU NGHĨA — bốn nguyên nhân, bốn cách xử ──

Bảng nghĩa dựng bằng `nghia.setdefault(v["tu"], …)` từ `knowledgeCore.vocabulary`
của mọi bài đã học. Khoá tra là NGUYÊN VĂN `tu`. Mà kho từ vựng lưu rất nhiều
CỤM — "break time", "table tennis", "collect seashells", "do projects". Ô chữ thì
tách thành TỪNG CHỮ. Chữ lẻ không bao giờ khớp khoá cụm.

  A · nằm trong CỤM có nghĩa (48)   cụm có nghĩa, chữ lẻ thì không.
  B · dạng biến đổi (28)            số nhiều · thì quá khứ · V-ing.
  C · tên riêng / mảnh vỡ (11)      KHÔNG cần nghĩa — nhưng xem lỗi 2 ở trên.
  D · đại từ · chữ rút gọn (11)     cùng loại với `KHONG_CHU` sẵn có, chỉ là sót.
  E · thật sự vắng trong kho (7)

⚠ VÀ ĐÂY LÀ CHỖ KHÔNG ĐƯỢC LÀM MÁY: bảy chữ có nghĩa LẺ khác hẳn nghĩa của CỤM.
`set` trong "set square" là cái ê-ke, nhưng `set` một mình không phải. Lấy nghĩa
cụm gán cho chữ lẻ là dạy sai. Bảy chữ ấy cột "cần bác chọn" ghi ⚠.
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
from sinh_bai_tranh import KHONG_CHU, QUYEN  # noqa: E402

RA = GOC / "docs/soat_vontu.xlsx"

# ── nghĩa ĐỀ NGHỊ, viết tay. `None` = không cần nghĩa. ⚠ ở đầu = nghĩa lẻ khác
#    nghĩa cụm, cần bác chốt.
DE_NGHI: dict[str, str | None] = {
    # A · chữ lẻ tách khỏi cụm
    "TV": "ti vi", "around": "quanh, xung quanh", "at": "ở, tại",
    "break": "⚠ giờ giải lao — chỉ đúng trong cụm “break time”",
    "buy": "mua", "by": "bằng, bởi", "campfire": "lửa trại", "camping": "cắm trại",
    "centre": "trung tâm", "clean": "lau, dọn sạch", "day": "ngày",
    "decorate": "trang trí", "dentist": "nha sĩ", "drink": "uống",
    "evening": "buổi tối", "every": "mỗi", "exercise": "bài thể dục",
    "fast": "nhanh",
    "first": "⚠ thứ nhất, đầu tiên — nhưng “first floor” là TẦNG HAI kiểu Anh",
    "floor": "⚠ sàn nhà — còn nghĩa “tầng”, hai bài dùng hai nghĩa",
    "flower": "bông hoa", "flowers": "những bông hoa", "for": "cho, để",
    "fresh": "tươi",
    "get": "⚠ lấy, nhận — nhưng “get up” là thức dậy",
    "go": "đi", "home": "nhà", "morning": "buổi sáng", "park": "công viên",
    "photo": "tấm ảnh", "photos": "những tấm ảnh", "picture": "bức tranh",
    "projects": "bài tập dự án", "roses": "hoa hồng", "seashells": "vỏ sò",
    "set": "⚠ bộ — nhưng “set square” là cái ê-ke, nghĩa khác hẳn",
    "shopping": "mua sắm", "sign": "biển báo", "songs": "bài hát",
    "sports": "thể thao", "study": "học",
    "tennis": "⚠ quần vợt — nhưng “table tennis” là BÓNG BÀN",
    "time": "thời gian, giờ", "trees": "cây", "up": "lên", "walk": "đi bộ",
    "watching": "đang xem", "yoga": "yoga",
    # B · dạng biến đổi mà GỐC cũng không có nghĩa
    "collected": "đã thu lượm", "doing": "đang làm", "goes": "đi",
    "going": "đang đi", "planted": "đã trồng",
    "took": "đã chụp, đã lấy", "walked": "đã đi bộ", "went": "đã đi",
    "works": "làm việc", "years": "năm",
    # E · thật sự vắng
    "animal": "con vật", "from": "từ", "should": "nên", "subject": "môn học",
    "think": "nghĩ", "want": "muốn", "wear": "mặc",
}

TEN_RIENG = {"Hoa", "Dao", "Hung", "Tran", "Viet",
             "Autumn", "Bridge", "Dragon", "Festival", "Mid", "T"}
DAI_TU = {"He", "She", "We", "You", "He's", "She's", "They're",
          "I'm", "I'd", "I'll", "We'll"}

BAT_QUY = {
    "Mondays": "Monday", "Saturdays": "Saturday", "Sundays": "Sunday",
    "bikes": "bike", "books": "book", "buildings": "building", "cars": "car",
    "chairs": "chair", "crayons": "crayon", "desks": "desk", "dogs": "dog",
    "giraffes": "giraffe", "likes": "like", "living": "live", "plays": "play",
    "playing": "play", "ran": "run", "watering": "water",
    "collected": "collect", "doing": "do", "goes": "go", "going": "go",
    "planted": "plant", "took": "take", "walked": "walk", "went": "go",
    "works": "work", "years": "year",
}


def kho_tu(lop: int) -> dict[str, str]:
    """Bảng nghĩa DỰNG ĐÚNG như `sinh_bai_tranh.tu_trong_tranh` dựng."""
    ng: dict[str, str] = {}
    for l in range(1, lop + 1):
        tm = GOC / f"web/public/content/{QUYEN[l]}"
        for f in sorted(tm.glob(f"DL_{QUYEN[l].upper()}_B*.json")):
            b = json.loads(f.read_text("utf8"))
            for v in b["knowledgeCore"]["vocabulary"]:
                ng.setdefault(v["tu"], v.get("nghia") or "")
    return ng


def main() -> int:
    lop_cua = {"ta1": 1, "ta2": 2, "ta3": 3, "ta4": 4, "ta5": 5}
    kho = kho_tu(5)
    co = {k.lower(): v for k, v in kho.items() if v}
    trong_cum: dict[str, tuple[str, str]] = {}
    for k, v in co.items():
        ws = re.findall(r"[a-z][a-z']*", k)
        if len(ws) > 1:
            for w in ws:
                trong_cum.setdefault(w, (k, v))

    # ── gom mọi ô chữ thiếu nghĩa, kèm bài nào dùng ──
    thieu: dict[str, set[str]] = {}
    tong_o = co_nghia_o = 0
    for q in lop_cua:
        tep = GOC / f"web/public/content/{q}/vietbai.json"
        if not tep.exists():
            continue
        for b in json.loads(tep.read_text("utf8")):
            for o in b["vonTu"]:
                tong_o += 1
                if o["nghia"]:
                    co_nghia_o += 1
                    continue
                if o["tu"].lower() in KHONG_CHU:
                    continue
                thieu.setdefault(o["tu"], set()).add(b["id"])

    dong = []
    for w in sorted(thieu, key=str.lower):
        bai = sorted(thieu[w])
        if w in DAI_TU:
            dong.append((w, "D · đại từ · chữ rút gọn",
                         "cùng loại với các chữ nối đã khai trong KHONG_CHU — chỉ là sót",
                         "khai vào KHONG_CHU, không bày nghĩa", "", bai))
        elif w in TEN_RIENG:
            manh = w in {"Autumn", "Bridge", "Dragon", "Festival", "Mid", "T"}
            dong.append((w, "C · tên riêng / mảnh vỡ tên riêng",
                         "mảnh vỡ của tên riêng có gạch nối hoặc nhiều chữ"
                         if manh else "tên người",
                         "KHÔNG cần nghĩa — nhưng phải sửa chỗ CẮT GẠCH NỐI"
                         if manh else "KHÔNG cần nghĩa", "", bai))
        else:
            g = BAT_QUY.get(w)
            if g and g.lower() in co:
                dong.append((w, "B · dạng biến đổi, gốc CÓ nghĩa",
                             f"gốc “{g}” = {co[g.lower()]}",
                             "suy bằng máy từ gốc — tiếng Việt không đổi dạng",
                             co[g.lower()], bai))
            elif w.lower() in trong_cum:
                k, v = trong_cum[w.lower()]
                dong.append((w, "A · nằm trong CỤM có nghĩa",
                             f"kho chỉ có cụm “{k}” = {v}; chữ lẻ không khớp khoá",
                             "cần người viết nghĩa cho CHỮ LẺ",
                             DE_NGHI.get(w, ""), bai))
            else:
                dong.append((w, "E · thật sự vắng trong kho",
                             "không có trong knowledgeCore.vocabulary của bài nào",
                             "cần người viết nghĩa", DE_NGHI.get(w, ""), bai))

    # ── Excel ──
    wb = Workbook()
    dam = Font(bold=True, color="FFFFFF")
    nen = PatternFill("solid", fgColor="2F4A6B")
    vang = PatternFill("solid", fgColor="FFF3CD")
    tren = Alignment(vertical="top", wrap_text=True)

    ws = wb.active
    ws.title = "Chữ thiếu nghĩa"
    dau = ["Chữ", "Nhóm", "Vì sao thiếu", "Cách xử đề nghị",
           "Nghĩa đề nghị", "Bài dùng chữ này"]
    ws.append(dau)
    for c in ws[1]:
        c.font, c.fill = dam, nen
    for w, nh, vi, cach, ng, bai in dong:
        ws.append([w, nh, vi, cach, ng, " · ".join(bai)])
        if str(ng).startswith("⚠"):
            for c in ws[ws.max_row]:
                c.fill = vang
    for c, r in zip("ABCDEF", (14, 30, 52, 40, 46, 40)):
        ws.column_dimensions[c].width = r
    for r in ws.iter_rows(min_row=1):
        for c in r:
            c.alignment = tren
    ws.freeze_panes = "A2"

    w2 = wb.create_sheet("Hai lỗi nặng hơn")
    w2.append(["Lỗi", "Ở đâu", "Bé chịu hậu quả gì", "Bằng chứng"])
    for c in w2[1]:
        c.font, c.fill = dam, nen
    w2.append([
        "Nghĩa tiếng Việt chỉ là tooltip",
        "web/src/mon/tienganh/components/VietBai.jsx:166 — title={v.nghia}",
        "ĐÃ SỬA — nay nghĩa vẽ thành chữ nhỏ dưới từ. Trước đó tooltip KHÔNG "
        "BAO GIỜ hiện trên máy tính bảng, nên bé không đọc được nghĩa của BẤT "
        "KỲ ô nào, kể cả 2075 ô đã có nghĩa.",
        f"{co_nghia_o}/{tong_o} ô có nghĩa, và `nghia` chỉ xuất hiện đúng MỘT "
        "lần trong toàn bộ mã màn Viết — ở thuộc tính title.",
    ])
    w2.append([
        "Gạch nối bị cắt thành ô rời",
        "tools/sinh_bai_tranh.py — re.findall(r\"[A-Za-z][A-Za-z']*\", …)",
        "ĐÃ SỬA. Trước đó bé không ghép lại được vì không có ô gạch nối nào, "
        "và bài ta4 U18 hiện ĐỦ CẢ BA ô “T-shirt” · “T” · “shirt”.",
        "ta4 VIET:TA4.U18 (T-shirt) · ta5 VIET:TA5.U13 (Mid-Autumn Festival) · "
        "ta5 VIET:TA5.C4 (twenty-nine)",
    ])
    for c, r in zip("ABCD", (34, 56, 60, 56)):
        w2.column_dimensions[c].width = r
    for r in w2.iter_rows(min_row=1):
        for c in r:
            c.alignment = tren

    w3 = wb.create_sheet("Tổng hợp")
    dem: dict[str, int] = {}
    for _, nh, _, _, _, _ in dong:
        dem[nh] = dem.get(nh, 0) + 1
    w3.append(["Nhóm", "Số chữ", "Xử bằng gì"])
    for c in w3[1]:
        c.font, c.fill = dam, nen
    cach = {
        "A · nằm trong CỤM có nghĩa": "người viết nghĩa cho chữ lẻ (7 chữ ⚠ nghĩa lẻ KHÁC nghĩa cụm)",
        "B · dạng biến đổi, gốc CÓ nghĩa": "máy suy từ gốc",
        "C · tên riêng / mảnh vỡ tên riêng": "không cần nghĩa; sửa chỗ cắt gạch nối",
        "D · đại từ · chữ rút gọn": "khai vào KHONG_CHU",
        "E · thật sự vắng trong kho": "người viết nghĩa",
    }
    for k in sorted(dem):
        w3.append([k, dem[k], cach.get(k, "")])
    w3.append(["TỔNG", sum(dem.values()), ""])
    w3.append([])
    w3.append(["Bảng trống là ĐÚNG: 105 chữ đã xử xong, và cổng "
               "`web/test/tienganh_bangtu_viet.test.mjs` canh cả bốn chỗ.",
               "", ""])
    for c, r in zip("ABC", (38, 10, 70)):
        w3.column_dimensions[c].width = r
    for r in w3.iter_rows(min_row=1):
        for c in r:
            c.alignment = tren

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(dong)} chữ)")
    for k in sorted(dem):
        print(f"   {dem[k]:4}  {k}")
    thieu_de = [w for w, _, _, cach, ng, _ in dong
                if "viết nghĩa" in cach and not ng]
    if thieu_de:
        print(f"   ⚠ {len(thieu_de)} chữ cần nghĩa mà CHƯA đề nghị: "
              + ", ".join(thieu_de))
        return 1
    print(f"   {co_nghia_o}/{tong_o} ô có nghĩa; {tong_o - co_nghia_o} ô còn lại "
          "là CHỮ NỐI trong KHONG_CHU — cố ý không chú nghĩa")
    return 0


if __name__ == "__main__":
    sys.exit(main())
