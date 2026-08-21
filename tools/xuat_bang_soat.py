#!/usr/bin/env python3
"""BẢNG SOÁT 42 BÀI TẢ TRANH → docs/bang_soat_ta_tranh.xlsx

    tools/tts/.venv/bin/python tools/xuat_bang_soat.py

Khác `tools/canh_de_xuat.py` ở đúng một điều, và điều ấy là cả vấn đề:

    canh_de_xuat.py  đọc BẢN NHÁP trong chính nó   → bảng để BÀN
    xuat_bang_soat.py đọc NỘI DUNG ĐANG CHẠY       → bảng để SOÁT

Bảng nháp đã hết việc: bác duyệt xong, tôi đem đi làm, và trong lúc làm thì 35
bài phải sửa — vì cổng chỉ ra tôi dùng những chữ bé CHƯA HỌC TỚI (`classroom`
mãi U06 mới dạy, `desk` U14, `who` U11; `tree` · `board` · `family` · `people`
sách không có). Nếu nay lại xuất từ bản nháp thì bác soát một đằng, bé học một
nẻo — đúng cái bẫy [[ban-dung-lai-de-mat-ban-sua-tay]].

Nên tệp này đọc thẳng những gì đã deploy:

    data/tienganh/canh_lopN.json          mô tả tranh · đoạn · câu hỏi · gợi ý
    web/public/content/taN/vietbai.json   bảng từ màn VIẾT (máy sinh ra thật)
    web/public/content/taN/kichban_noi.json   các bước phòng nói
    web/public/content/tienganh/tranh/*.png   chính bức bé nhìn thấy

và DÁN LUÔN BỨC TRANH vào từng dòng — soát chữ mà không thấy hình thì không
soát được cái đáng soát nhất: chữ có khớp hình không.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/bang_soat_ta_tranh.xlsx"
QUYEN = {3: "ta3", 4: "ta4", 5: "ta5"}
TRANH = GOC / "web/public/content/tienganh/tranh"

# ══════════════════════════════════════════════════════════════════════════
# ĐỔI GÌ SO VỚI BẢNG BÁC ĐÃ DUYỆT
#
# Khai TAY, vì lý do đổi nằm ở chỗ máy không đọc ra được: "chữ này bé chưa học
# tới bài này". Bác duyệt bản nào thì bản ấy là mốc; mọi chỗ tôi tự đổi sau đó
# phải nói ra, không được lặng lẽ trôi đi.
# ══════════════════════════════════════════════════════════════════════════
DOI = {
 (3, 0): "Bỏ `classroom` (mãi U06 mới dạy), `desks` (U14), `board` (sách không có). "
         "Đoạn nay tả cô giáo · bạn · cái bàn · quyển sách · cái cặp đỏ.",
 (3, 1): "`bags` chưa khai số nhiều và `Who is this?` mãi U11 mới dạy → đổi sang "
         "đếm XE ĐẠP, và vẽ thêm hai chiếc xe đạp ở cổng trường cho khớp.",
 (3, 2): "Bỏ câu hỏi `Who is this?` (chưa dạy tới), thay bằng `What can you see?`.",
 (3, 3): "Bỏ `Mr Long` · `tree` · `school` · `who` (đều chưa có tới bài này). "
         "Đoạn nay tả cô Hoa · bạn Minh · khu vườn · cái cặp.",
 (3, 4): "Năm dòng đều `This is my …` — cổng chặn quá 2 dòng cùng khuôn. Đổi ba "
         "dòng sang `That's` · `I can see` · `My hair is black.`",
 (3, 5): "Thêm câu mở `This is my school.` — bảng từ màn VIẾT chỉ còn 9 chữ, "
         "dưới ngưỡng 10.",
 (3, 6): "Ba dòng cùng khuôn; và cả đoạn chỉ trỏ vào đồ vật → thêm `I like my school.`",
 (3, 7): "Bỏ `desks`; cả đoạn chỉ trỏ đồ vật → thêm `I like my teacher.`",
 (3, 8): "Ba dòng `I have …` → đổi sang `There's` · `I can see` · `That's`.",
 (3, 9): "Ba dòng `This is my …` và ba dòng `My … is …` → xoay sang bốn khuôn.",
 (3, 10): "`plays` (ngôi thứ ba) chưa dạy. Đoạn nay tả sân chơi · bóng đá · bạn.",
 (3, 11): "Bốn dòng cùng khuôn; `family` và `people` sách không dạy.",
 (3, 12): "`people` chưa dạy; và sách chỉ dạy `What's her job?`, KHÔNG dạy `his` → "
          "câu hỏi 2 đổi sang `What can you see?`",
 (3, 13): "Ba dòng cùng khuôn. Đáp án `They're in the living room.` lẻ loi về dáng "
          "câu (5 chữ, ba mồi 4 chữ) → hỏi `Where's the bed?` thay.",
 (3, 14): "Ba dòng `There's a … in the room.` cùng khuôn.",
 (3, 15): "`family` và `cups` chưa dạy.",
 (3, 17): "`toy box` — cả `toy` lẫn `box` đều không có trên tranh; `What does she "
          "have?` dùng `does` chưa dạy ở lớp 3.",
 (3, 19): "`tree` sách không có → đổi sang `There's a garden.`",
 (3, 20): "`tree` sách không có; ba dòng cùng khuôn.",
 (4, 0): "`bags` chưa khai số nhiều, `Who is this?` dùng dạng chưa dạy → đếm XE ĐẠP, "
         "và vẽ thêm hai chiếc xe đạp vào sân trường.",
 (4, 1): "`map` sách không có → bỏ khỏi đoạn (bức tranh vẫn có tấm bản đồ làm bối "
         "cảnh). Đáp án `I'm from Viet Nam.` lẻ loi về dáng câu → hỏi `Where's she "
         "from?` thay.",
 (4, 2): "Ba dòng cùng khuôn.",
 (4, 3): "Mồi nhử `I watch TV.` dùng chữ mãi U14 mới dạy → `I stay at home.`",
 (4, 4): "Mồi nhử `It's in June.` (U09) đứng ở bài chương 1 → `It's in February.`; "
         "và ba dòng cùng khuôn.",
 (4, 5): "Đáp án `He can ride a bike.` (5 chữ) lẻ loi giữa ba mồi 3 chữ.",
 (4, 7): "Ba dòng cùng khuôn.",
 (4, 8): "`pictures` chưa khai số nhiều.",
 (4, 9): "Ba dòng cùng khuôn; `friends` chưa khai số nhiều.",
 (4, 10): "`photo` mãi U20 mới dạy → dùng `picture`; ba dòng cùng khuôn.",
 (4, 11): "Tên phố trong mồi nhử (`Le Loi` · `Hai Ba Trung`) dùng chữ chưa dạy.",
 (4, 15): "Mồi `He watches films.` · `He cooks meals.` dùng ngôi thứ ba chưa dạy. "
          "Thêm chiếc xe đạp vào tranh cho khớp câu `I can see a bike.`",
 (4, 17): "Bỏ câu hỏi `What does the sign say?` — biển báo theo luật là ĐỂ TRỐNG "
          "nên bé không đáp được.",
 (4, 18): "Ba dòng cùng khuôn.",
 (4, 19): "`tree` sách không có; `lions` · `monkeys` chưa khai số nhiều; ba dòng "
          "cùng khuôn.",
 (4, 20): "`summer camp` — `camp` chưa dạy, dùng `campsite`. Đáp án `They're singing "
          "songs.` lẻ loi về dáng câu, không mẫu nào cùng dáng → hỏi `What can you "
          "see?` thay.",
}

LUAT = [
    ["BỐN LUẬT — bác chốt 20-08-2026, đã cài xong và deploy 21-08", ""],
    ["", ""],
    ["1 · KHÔNG HỘI THOẠI",
     "Đoạn đọc là VĂN MÔ TẢ, chỉ có câu kể. Mẫu câu HỎI của unit vẫn dùng — nhưng "
     "ở CÂU HỎI SAU BÀI và ở phòng nói, không nhét vào đoạn văn."],
    ["2 · VỐN TÍCH LUỸ TỪ LỚP 1",
     "Chữ và câu lấy từ lớp 1 cộng dồn tới ĐÚNG CHƯƠNG của bài ấy. Đây là chỗ tôi "
     "sai nhiều nhất khi làm: viết theo trí nhớ về chủ đề chứ không theo vốn từ "
     "thật, nên 20 chỗ dùng chữ bé chưa học tới. Nay có cổng soi từng chữ."],
    ["3 · MỘT NƠI, MỘT LÚC",
     "Trả lời được “đây là chỗ nào” bằng một câu. Nhiều nhất 2–3 người. Đồ vật "
     "phải THUỘC VỀ chỗ ấy."],
    ["4 · KHÔNG NHÂN BẢN",
     "42 cảnh viết tay ở tools/soan_canh.py. Bộ vẽ (tools/canh_ve.py) chỉ biết VẼ, "
     "không quyết cảnh nào có gì."],
    ["", ""],
    ["LUẬT ĐẺ RA CÁI KỆ — ĐÃ BỎ", ""],
    ["Cổng cũ đòi",
     "“mỗi vật ĐÚNG MỘT câu tả nó, và ngược lại”. Nghe rất hợp lý, và chính nó ép "
     "đoạn văn thành bảng liệt kê: thêm một câu nói về người là cổng kêu “thừa "
     "câu”. Bức bác chê ra đời từ đó."],
    ["Nay thay bằng",
     "① vật đoạn nhắc tới phải CÓ trên tranh · ② số đếm phải khớp · ③ câu “…ing” "
     "phải có người trên tranh · ④ cả đoạn KHÔNG được toàn câu trỏ-vật."],
    ["", ""],
    ["PHÒNG NÓI — BA NHỊP", ""],
    ["Bé thấy gì", "CHỈ bức tranh. Không thấy đoạn văn."],
    ["Nhịp 1 · MỜI TẢ", "Cô: “Con nhìn bức tranh rồi tả cho cô nghe nhé.”"],
    ["Nhịp 2 · GỢI Ý",
     "Bé bí thì cô HỎI — cột “④ NÓI” là các câu ấy. Câu nào trùng câu hỏi sau bài "
     "đọc thì mang theo ĐÁP MẪU; câu nào không thì phòng nói nhận mọi câu trong "
     "đoạn làm đáp đúng."],
    ["Nhịp 3 · CẢ ĐOẠN", "Cô xâu chuỗi rồi mời bé nói LIỀN cả đoạn. Đó là đích."],
    ["", ""],
    ["⚠ VÌ SAO KHÔNG CÓ CHỮ TRONG TRANH",
     "Biển tên phố, tấm lịch, thời khoá biểu, bảng tên, mặt bảng đen — đều ĐỂ "
     "TRỐNG. Bé đang tập đọc tiếng Anh; chữ in sẵn trên tranh là cho sẵn đáp án "
     "của chính bài viết và bài nói."],
]


def anh_nho(tep: Path, ra: Path, rong: int = 380) -> Path:
    """Thu nhỏ bức tranh để nhúng — 42 ảnh 1280×720 nhúng nguyên là tệp 30 MB."""
    from PIL import Image
    im = Image.open(tep)
    im = im.resize((rong, round(rong * im.height / im.width)), Image.LANCZOS)
    im.save(ra)
    return ra


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.drawing.image import Image as XLImage

    tam = Path(tempfile.mkdtemp(prefix="bangsoat_"))
    wb = Workbook()
    ws = wb.active
    ws.title = "42 bài tả tranh"

    dau = ["Quyển", "Bài", "Chủ đề unit", "Bối cảnh", "BỨC TRANH BÉ NHÌN THẤY",
           "① MÔ TẢ TRANH (lời cho AI vẽ)",
           "② ĐOẠN ĐỌC — không hội thoại",
           "③ CÂU HỎI sau khi đọc  (✓ = đáp án)",
           "④ NÓI · câu cô hỏi khi bé bí",
           "④ VIẾT · bảng từ máy đang bày",
           "ĐỔI GÌ so với bảng bác đã duyệt", "Bác duyệt"]
    ws.append(dau)
    for i, _ in enumerate(dau, 1):
        o = ws.cell(row=1, column=i)
        o.font = Font(bold=True, color="FFFFFF", size=11)
        o.fill = PatternFill("solid", fgColor="0B4EA8")
        o.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 46

    vien = Border(*[Side(style="thin", color="C8D4E2")] * 4)
    dong = 1
    for lop in (3, 4, 5):
        canh = json.loads((GOC / f"data/tienganh/canh_lop{lop}.json").read_text("utf8"))
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{lop}.json").read_text("utf8"))
        ten_unit = {u["so"]: u["canh"] for u in cn["unit"]}
        viet = {v["unit"]: v for v in json.loads(
            (GOC / f"web/public/content/{QUYEN[lop]}/vietbai.json").read_text("utf8"))
            if v.get("dang") == "tranh"}
        noi = {int(k["bai"].split(".B")[1]): k for k in json.loads(
            (GOC / f"web/public/content/{QUYEN[lop]}/kichban_noi.json").read_text("utf8"))
            if k.get("dang") == "tranh"}

        for k in canh:
            u = k["unit"]
            dong += 1

            # ③ câu hỏi: đáp án đánh dấu ✓, mồi nhử liệt kê sau
            hoi = "\n\n".join(
                f"{i}. {h['hoi']}\n   ({h['vi']})\n   ✓ {h['dap']}\n"
                + "\n".join(f"   ✗ {m}" for m in h["moi"])
                for i, h in enumerate(k["hoi"], 1))

            # ④ nói: lấy TỪ KỊCH BẢN ĐANG CHẠY, không suy lại
            b = noi.get(u, {})
            noi_txt = "\n".join(
                f"· {s['en']}" + (f"   → đáp mẫu: {s['dapMau']}" if s.get("dapMau")
                                  else "   (nhận mọi câu trong đoạn)")
                for s in b.get("buoc", []) if s["loai"] == "goiY")

            v = viet.get(u, {})
            tu_txt = " · ".join(x["tu"] for x in v.get("vonTu", []))

            ws.append([f"lớp {lop}", f"U{u:02d}", ten_unit.get(u, ""), k["ten"],
                       "", k["moTa"], " ".join(k["doan"]), hoi, noi_txt, tu_txt,
                       DOI.get((lop, u),
                               "— viết mới cho lớp 5, bác chưa duyệt bản nháp nào —"
                               if lop == 5 else "— giữ nguyên như bảng đã duyệt —"),
                       ""])

            tep = TRANH / f"{k['id'].replace(':', '_').replace('.', '_')}.png"
            if tep.exists():
                nho = anh_nho(tep, tam / f"{lop}_{u:02d}.png")
                img = XLImage(str(nho))
                ws.add_image(img, f"E{dong}")
            ws.row_dimensions[dong].height = 172

    for cot, w in {"A": 8, "B": 6, "C": 24, "D": 26, "E": 55, "F": 62, "G": 46,
                   "H": 44, "I": 40, "J": 40, "K": 46, "L": 11}.items():
        ws.column_dimensions[cot].width = w
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    # Cột "đổi gì" tô nhạt cho dễ lướt — nhưng chỉ những dòng CÓ đổi.
    vang = PatternFill("solid", fgColor="FFF3D6")
    for r in range(2, dong + 1):
        if not str(ws.cell(row=r, column=11).value or "").startswith("—"):
            ws.cell(row=r, column=11).fill = vang
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:L{dong}"

    w2 = wb.create_sheet("Luật · Phòng nói")
    for r in LUAT:
        w2.append(r)
    w2.column_dimensions["A"].width = 34
    w2.column_dimensions["B"].width = 96
    for row in w2.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    for d in (1, 8, 13):
        w2.cell(row=d, column=1).font = Font(bold=True, size=13)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    n_doi = sum(1 for r in range(2, dong + 1)
                if not str(ws.cell(row=r, column=11).value or "").startswith("—"))
    print(f"→ {RA.relative_to(GOC)}  ({dong - 1} bài · {n_doi} bài có sửa khi làm)")
    print("   lớp 3: 21 · lớp 4: 21 · lớp 5: 20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
