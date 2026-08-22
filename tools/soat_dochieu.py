#!/usr/bin/env python3
"""RÀ SOÁT BÀI ĐỌC HIỂU → docs/soat_dochieu.xlsx

    tools/tts/.venv/bin/python tools/soat_dochieu.py

── VÌ SAO CÓ TỆP NÀY ──
Bác bắt được 22-08-2026: bài đọc lớp 5 unit 1 kể chuyện tự giới thiệu trong lớp
("This is my class. This is Mary. Mary is my friend. She's friendly.") rồi dán
thêm "I can see a dolphin.", và câu hỏi là "What's your favourite animal?" với
đáp án "It's a dolphin." — CẢ ĐOẠN KHÔNG HỀ NÓI AI THÍCH CON GÌ.

Bộ này soi ĐÚNG một câu hỏi cho mỗi câu hỏi: **đoạn văn NÓI Ở CHỖ NÀO?**

── ⚠ PHÉP SOI PHẢI CHỈ RA ĐƯỢC CÂU NGUỒN ──
Không đủ khi chỉ kiểm "từ trong đáp án có xuất hiện trong đoạn": `dolphin` CÓ xuất
hiện, mà câu hỏi vẫn sai. Nên mỗi câu hỏi phải tìm được một CÂU CỤ THỂ trong đoạn
mang đúng MỆNH ĐỀ mà câu hỏi đòi — thấy thì ghi ra câu ấy, không thấy thì báo lỗi.

── BA MỨC, KHÔNG PHẢI HAI ──
  ĐẠT       đoạn nói thẳng ra, chỉ được đúng câu nguồn.
  SUY ĐƯỢC  đoạn không nói thẳng nhưng bé nhìn TRANH là trả lời được, và mệnh đề
            cùng loại (ví dụ đoạn "There's a desk." → hỏi "What's this?").
  LỖI       đoạn không nói, tranh cũng không cứu được — câu hỏi bịa ra một mệnh
            đề mới. Đây là loại bác bắt được.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/soat_dochieu.xlsx"

DAT, SUY, LOI = "ĐẠT", "SUY ĐƯỢC TỪ TRANH", "LỖI"
MAT = "CẦN MẮT NGƯỜI"


def gon(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()


def tu(s: str) -> set[str]:
    return set(gon(s).split())


# ── MỆNH ĐỀ MÀ MỖI DẠNG CÂU HỎI ĐÒI ─────────────────────────────────────────
#
# Khoá là dấu hiệu trong câu hỏi; giá trị là các khuôn câu ĐOẠN phải có thì câu
# hỏi mới trả lời được. `None` nghĩa là dạng ấy không đòi mệnh đề riêng.
#
# ⚠ Bảng này CỐ Ý HẸP. Dạng nào chưa khai thì rơi vào "chưa phân loại" và hiện ra
# ở cột riêng — thà nói "tôi chưa soi được cái này" còn hơn cho qua im lặng rồi
# báo cáo một con số đẹp hơn sự thật.
#
# ── ⚠ CỘT THỨ TƯ: TRANH CÓ CỨU ĐƯỢC KHÔNG ──
# Đây là chỗ bản đầu của bộ soi sai, và sai theo hướng DỄ DÃI. Nó cho mọi câu hỏi
# "cứu" được bằng tranh, nên ca bác bắt (favourite animal → dolphin) bị xếp thành
# "suy được từ tranh" — trong khi tranh cho thấy CON CÁ HEO, chứ không bao giờ cho
# thấy bé THÍCH con gì.
#
# Tranh chỉ cứu được mệnh đề QUAN SÁT ĐƯỢC: cái này là gì · thấy gì · mấy cái ·
# màu gì · đang làm gì · ở đâu. Còn TRONG ĐẦU BÉ — thích gì, muốn gì, nghĩ gì,
# thường mặc gì — thì đoạn văn PHẢI NÓI RA. Không nói mà vẫn hỏi là bịa ra một
# mệnh đề về chính đứa trẻ.
DOI = [
    ("favourite", [r"\bfavourite\b", r"\bi like\b", r"\blikes\b"],
     "đoạn phải NÓI RA sở thích: “My favourite … is …” hoặc “I like …”",
     False),
    ("what can you see", [r"\bi can see\b", r"\bwe can see\b"],
     "đoạn phải có câu “I can see …”",
     True),
    ("how many", [r"\bi can see \w+\b", r"\bthere are\b", r"\bthere's\b"],
     "đoạn phải nói SỐ LƯỢNG",
     True),
    ("what colour", [r"\bis (red|blue|green|yellow|black|white|pink|orange|brown|purple)\b"],
     "đoạn phải nói MÀU của chính vật ấy",
     True),
    ("doing", [r"\b(is|are|'s|'re) \w+ing\b"],
     "đoạn phải có câu đang-làm-gì (V-ing)",
     True),
    ("how old", [r"\b(is|'s) \w*\s*\d", r"\byears old\b", r"\b(is|'s) (one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"],
     "đoạn phải nói TUỔI",
     True),
    ("where", [r"\b(from|in|at|on|near|behind|under|next to)\b"],
     "đoạn phải nói NƠI CHỐN",
     True),
    ("what do you have", [r"\bi have\b", r"\bi've got\b"],
     "đoạn phải có câu “I have …”",
     False),
    ("what did", [r"\b(was|were|went|had|did|played|visited|watched|saw)\b"],
     "đoạn phải có câu ở THÌ QUÁ KHỨ",
     True),
    ("what will", [r"\b(will|'ll|going to)\b"],
     "đoạn phải có câu ở THÌ TƯƠNG LAI",
     True),
    ("what's this", [r"\bthis is\b", r"\bthat's\b", r"\bthere's\b", r"\bit's\b", r"\bi can see\b"],
     "đoạn phải trỏ vào vật ấy",
     True),
    ("who's this", [r"\bthis is\b", r"\bthat's\b"],
     "đoạn phải giới thiệu người ấy",
     True),
    ("what do you do", [r"\bi \w+\b"],
     "đoạn phải nói bé LÀM GÌ",
     False),
    ("what day", [r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|today is)\b"],
     "đoạn phải nói THỨ",
     True),
    ("when", [r"\b(on |in |at |monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|may|june|july|august|september|october|november|december)\b"],
     "đoạn phải nói THỜI ĐIỂM",
     True),
    ("what subjects", [r"\b(maths|english|music|art|science|it|vietnamese)\b"],
     "đoạn phải kể MÔN HỌC",
     True),
    ("like?", [r"\bis \w+\b", r"\bit's \w+\b"],
     "đoạn phải TẢ tính chất của vật ấy",
     True),
    ("does he do", [r"\bhe \w+s\b", r"\bhe's \w+ing\b"],
     "đoạn phải nói anh ấy LÀM GÌ",
     True),
    ("weather", [r"\b(sunny|rainy|windy|cloudy|hot|cold|cool|warm|weather)\b"],
     "đoạn phải nói THỜI TIẾT",
     True),
    ("activity", [r"\b(likes?|loves?|enjoys?)\b"],
     "đoạn phải nói bạn ấy THÍCH hoạt động nào",
     False),
    ("how does he", [r"\bhe \w+s\b", r"\bhe's \w+ing\b"],
     "đoạn phải nói anh ấy làm việc đó BẰNG CÁCH NÀO",
     False),
    ("job", [r"\b(teacher|nurse|doctor|farmer|worker|driver|pilot|singer|writer|reporter)\b"],
     "đoạn phải nói NGHỀ",
     True),
    ("wear", [r"\b(wear|wears|wearing)\b"],
     "đoạn phải nói bé MẶC gì",
     False),
    ("main characters", [r"\b(tortoise|hare|ant|grasshopper|fox|crow|dwarf|snow white)\b"],
     "đoạn phải NHẮC TÊN các nhân vật",
     True),
    ("how can i get", [r"\b(by bus|by bike|by car|on foot|walk|take the)\b"],
     "đoạn phải nói ĐI BẰNG GÌ",
     True),
    ("what do you think", [r"\b(i think|it's \w+|beautiful|nice|great|interesting)\b"],
     "đoạn phải nói Ý KIẾN về vật ấy",
     False),
]


def soi_mot(hoi: str, dap: str, doan: list[str], co_tranh: bool):
    """Trả (mức, câu nguồn, cách sửa)."""
    kho = [c for c in doan]
    gon_doan = {gon(c) for c in kho}
    h_raw = hoi or ""

    # ── BA DẠNG CÂU HỎI TIẾNG VIỆT — hai trong ba KIỂM MÁY ĐƯỢC ──
    #
    # Bản đầu tôi gộp cả ba vào "câu hỏi tiếng Việt, không soi" rồi báo một con số
    # đẹp. Sai: hai dạng dưới đây kiểm được, và kiểm được thì phải kiểm.
    # ⚠ CHỈ NHÁY CONG mới là dấu bao. Bản đầu tôi cho cả nháy đơn `'` vào lớp ký
    # tự, nên `Câu “What's this?” …` bị cắt ngay ở dấu lược của "What's" — phép
    # bắt hỏng, câu rơi xuống bảng DOI và bị báo LỖI OAN. Sáu câu như thế.
    m = re.search(r"Câu\s*[“\"]([^”\"]+)[”\"]\s*có trong bài đọc không", h_raw)
    if m:
        co = gon(m.group(1)) in gon_doan
        dung = ("Có" if co else "Không")
        if gon(dap) != gon(dung):
            return LOI, "", (f"đáp án đang là “{dap}” mà câu ấy "
                             f"{'CÓ' if co else 'KHÔNG'} trong đoạn → phải là “{dung}”")
        return DAT, (m.group(1) if co else "(đúng: câu ấy không có trong đoạn)"), ""

    if "Câu nào CÓ trong bài đọc" in h_raw:
        if gon(dap) in gon_doan:
            return DAT, next(c for c in kho if gon(c) == gon(dap)), ""
        return LOI, "", "đáp án phải là một câu CÓ THẬT, nguyên văn, trong đoạn"

    if "nói về chuyện gì" in h_raw:
        return MAT, "", ("hỏi CHỦ ĐỀ — máy không kiểm được đáp án có đúng với đoạn "
                         "không, cần đọc bằng mắt")

    if not re.match(r"^[A-Za-z]", h_raw):
        return MAT, "", "dạng câu hỏi tiếng Việt chưa khai — cần đọc bằng mắt"

    # 1 · đáp án là MỘT CÂU CÓ THẬT trong đoạn → chắc chắn đạt
    if gon(dap) in gon_doan:
        nguon = next(c for c in kho if gon(c) == gon(dap))
        return DAT, nguon, ""

    h = (hoi or "").lower()
    BO = tu("i a an the is it s can see this that my you re are we do does")
    for ten, khuon, sua, tranhCuu in DOI:
        if ten not in h:
            continue
        noi = tu(dap) - BO
        cungKhuon = [c for c in kho if any(re.search(k, c.lower()) for k in khuon)]

        # ⚠ TÌM CÂU CHỨA ĐÚNG VẬT TRƯỚC, rồi mới nói tới câu cùng khuôn.
        #
        # Bản đầu lấy câu ĐẦU TIÊN cùng khuôn rồi ghi vào cột "đoạn nói ở câu nào".
        # Thành ra hỏi "What's this? → It's a desk" mà cột ấy chỉ vào "This is my
        # teacher." — trong khi đoạn CÓ câu "There's a desk." Cột ấy chính là thứ
        # bác đọc để duyệt, nên chỉ sai chỗ là bảng mất giá trị.
        if noi:
            khop = [c for c in kho if noi & tu(c)]
            trung = [c for c in khop if c in cungKhuon]
            if trung:
                return DAT, trung[0], ""
            if khop:
                # Đoạn CÓ nhắc vật ấy, nhưng bằng một mệnh đề KHÁC LOẠI.
                # Tranh chỉ cứu được khi mệnh đề ấy QUAN SÁT ĐƯỢC.
                if co_tranh and tranhCuu:
                    return SUY, khop[0], ""
                return LOI, khop[0], sua
        if cungKhuon and not noi:
            return DAT, cungKhuon[0], ""
        return LOI, "", sua
    return "chưa phân loại", "", "dạng câu hỏi chưa khai trong bảng DOI"


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

    hang = []
    for f in sorted((GOC / "web/public/content").glob("ta*/dochieu.json")):
        quyen = f.parent.name
        for b in json.loads(f.read_text("utf8")):
            doan = [x["cau"] for x in (b.get("doan") or [])]
            co_tranh = bool(b.get("tranh"))
            for c in (b.get("cau") or []):
                hoi = (c.get("text") or "").strip()
                dap = ((c.get("answerKey") or {}).get("choice") or "").strip()
                muc, nguon, sua = soi_mot(hoi, dap, doan, co_tranh)
                hang.append({
                    "quyen": quyen, "bai": b.get("name", ""), "id": c.get("id", ""),
                    "doan": " ".join(doan), "hoi": hoi, "phu": c.get("phu", ""),
                    "dap": dap, "muc": muc, "nguon": nguon, "sua": sua,
                })

    # câu MỒ CÔI trong đoạn — lỗi ở tầng đoạn văn, không phải tầng câu hỏi
    mocoi = []
    for f in sorted((GOC / "web/public/content").glob("ta*/dochieu.json")):
        quyen = f.parent.name
        for b in json.loads(f.read_text("utf8")):
            doan = [x["cau"] for x in (b.get("doan") or [])]
            if len(doan) < 2:
                continue
            bo = tu("this is my a an the i you it s and can see are that there")
            for i, c in enumerate(doan):
                khac = set().union(*[tu(x) for j, x in enumerate(doan) if j != i])
                rieng = tu(c) - bo
                if rieng and not (rieng & (khac - bo)):
                    mocoi.append({"quyen": quyen, "bai": b.get("name", ""),
                                  "doan": " ".join(doan), "cau": c})

    wb = Workbook()
    vien = Border(*[Side(style="thin", color="C8D4E2")] * 4)
    MAU = {DAT: "D6F0DC", SUY: "FFF3D6", LOI: "FBE0DC", MAT: "EDF1F5",
           "chưa phân loại": "E2DDF0"}

    def dau(ws, cot, rong):
        ws.append(cot)
        for i, _ in enumerate(cot, 1):
            o = ws.cell(row=1, column=i)
            o.font = Font(bold=True, color="FFFFFF", size=11)
            o.fill = PatternFill("solid", fgColor="0B4EA8")
            o.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 40
        for c, w in rong.items():
            ws.column_dimensions[c].width = w

    ws = wb.active
    ws.title = "Câu hỏi"
    dau(ws, ["Quyển", "Bài", "Câu", "ĐOẠN VĂN", "CÂU HỎI", "Lời Việt", "ĐÁP ÁN",
             "Mức", "Đoạn nói ở câu nào", "CÁCH SỬA"],
        {"A": 7, "B": 40, "C": 6, "D": 60, "E": 30, "F": 26, "G": 24, "H": 18,
         "I": 34, "J": 46})
    for i, h in enumerate(hang, start=2):
        ws.append([h["quyen"], h["bai"], h["id"], h["doan"], h["hoi"], h["phu"],
                   h["dap"], h["muc"], h["nguon"], h["sua"]])
        ws.cell(row=i, column=8).fill = PatternFill("solid", fgColor=MAU.get(h["muc"], "FFFFFF"))
        ws.cell(row=i, column=8).font = Font(bold=True, size=10)
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:J{len(hang) + 1}"

    w2 = wb.create_sheet("Câu mồ côi")
    dau(w2, ["Quyển", "Bài", "ĐOẠN VĂN", "CÂU BỊ DÁN VÀO"],
        {"A": 7, "B": 44, "C": 70, "D": 34})
    for m in mocoi:
        w2.append([m["quyen"], m["bai"], m["doan"], m["cau"]])
    for r in w2.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    w2.auto_filter.ref = f"A1:D{len(mocoi) + 1}"

    import collections
    dem = collections.Counter(h["muc"] for h in hang)
    w3 = wb.create_sheet("Tổng hợp")
    dau(w3, ["Mức", "Số câu", "Tỉ lệ", "Nghĩa là gì"], {"A": 20, "B": 9, "C": 9, "D": 86})
    ngh = {
        DAT: "Đoạn NÓI THẲNG, và cột “đoạn nói ở câu nào” chỉ ra được câu ấy.",
        SUY: "Đoạn không nói thẳng nhưng bé NHÌN TRANH là trả lời được, và mệnh đề "
             "cùng loại. Chấp nhận được với bài có tranh — nhưng nên rà mắt.",
        LOI: "Đoạn KHÔNG nói, tranh cũng không cứu được. Câu hỏi bịa ra một mệnh "
             "đề mới — đây là loại bác bắt được ở bài lớp 5 unit 1.",
        MAT: "Máy không kiểm được — hỏi CHỦ ĐỀ bài đọc. Phải đọc bằng mắt.",
        "chưa phân loại": "Dạng câu hỏi chưa khai trong bảng DOI của bộ soi. "
                          "KHÔNG phải là đạt — là chỗ bộ soi chưa với tới.",
    }
    for k in [LOI, SUY, DAT, MAT, "chưa phân loại"]:
        if not dem.get(k):
            continue
        w3.append([k, dem[k], f"{dem[k] / len(hang) * 100:.0f}%", ngh[k]])
        w3.cell(row=w3.max_row, column=1).fill = PatternFill("solid", fgColor=MAU[k])
    w3.append(["TỔNG", len(hang), "100%", f"{len(mocoi)} câu mồ côi ở sheet riêng"])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True)
    for r in w3.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(hang)} câu hỏi · {len(mocoi)} câu mồ côi)")
    for k in [LOI, SUY, DAT, MAT, "chưa phân loại"]:
        if dem.get(k):
            print(f"   {k:22s} {dem[k]:4d}  ({dem[k] / len(hang) * 100:3.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
