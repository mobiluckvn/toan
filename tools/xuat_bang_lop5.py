#!/usr/bin/env python3
"""BẢNG SOÁT 20 BÀI TIẾNG ANH LỚP 5 → docs/bang_soat_lop5.xlsx

    tools/tts/.venv/bin/python tools/xuat_bang_lop5.py

Bác duyệt TRƯỚC khi tôi đổ công vào tranh, tiếng và video — vì sửa nội dung lúc
này là sửa một tệp, còn sửa sau khi đã dựng 45 video và 925 clip thì phải dựng
lại tất.

── BẢNG NÀY SOI CÁI GÌ ──
Chỗ rủi ro nhất của một quyển tiếng Anh không phải bảng từ vựng — bảng ấy lấy
thẳng từ sách. Rủi ro nằm ở NHỮNG CÂU MÁY SINH RA: chúng đúng công thức, mọi
chữ đều đã học, cổng xanh — mà đọc lên vẫn có thể vô nghĩa. Lớp 3 từng có
"I badminton at break time.", lớp 4 có "Where's the bookshop? - It's opposite
the bookshop.", lớp 5 suýt có "We visit the old buildings last summer."

Nên sheet chính là TỪNG CÂU MỘT, và bảng tự đánh dấu những chỗ đáng ngờ theo
bốn phép máy soi được:

    ① đáp án LẺ LOI về dáng câu giữa các lựa chọn → bé chọn bằng mắt
    ② câu còn sót dấu công thức (`...` · `/` · ` + `)
    ③ câu có chữ chưa dạy tới bài ấy
    ④ hai lựa chọn TRÙNG nhau

Bốn phép ấy KHÔNG thay được mắt bác: chúng không hiểu nghĩa. Cột cuối để trống
cho bác.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/bang_soat_lop5.xlsx"
LOP = 5


def tui_tu(den_unit: int) -> set[str]:
    """Mọi chữ bé đã gặp tính tới unit này — cộng dồn từ lớp 1."""
    kho: set[str] = set()

    def nap(s):
        kho.update(re.findall(r"[a-z']+", str(s or "").lower()))

    for l in range(1, LOP + 1):
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{l}.json").read_text("utf8"))
        for u in cn["unit"]:
            if l == LOP and u["so"] > den_unit:
                continue
            for t in u["tu"]:
                for k in ("tu", "so_it", "so_nhieu", "dang_ing", "dang_qk"):
                    nap(t.get(k))
            for m in u["mau_cau"]:
                nap(re.sub(r"\[[^\]]*\]", " ", str(m.get("cong_thuc") or "")))
                nap(m.get("vi_du"))
        for goi in (cn.get("them") or {}).values():
            if isinstance(goi, dict):
                for m in goi.get("muc") or []:
                    nap(m if isinstance(m, str) else m.get("word"))
    return kho


def dang(x: str) -> str:
    """Dáng câu — chữ đầu cộng số chữ. Cùng dáng thì bé phải ĐỌC mới phân biệt."""
    p = str(x or "").split()
    return f"{(p[0] if p else '').lower()}|{len(p)}"


def soi(muc: dict, kho: set[str]) -> list[str]:
    """Bốn phép máy soi được. Trả về danh sách chỗ đáng ngờ."""
    ra = []
    ch = [c for c in (muc.get("choices") or [])
          if re.match(r"^[A-Za-z]", str(c)) and not re.search(r"[^\x20-\x7E'’]", str(c))]
    dap = (muc.get("answerKey") or {}).get("choice")
    # ⚠ CHỈ ÁP CHO LỰA CHỌN LÀ CÂU. Với câu hỏi từ vựng thì bốn lựa chọn là bốn
    # TỪ RỜI (`class` · `dolphin` · `city`), mà "dáng" tính bằng chữ-đầu + số-chữ
    # nên MỖI TỪ một dáng riêng — đáp án lúc nào cũng "lẻ loi". Bản đầu của phép
    # này bắn 500 phát, và 500 phát ấy che mất mấy chỗ đáng ngờ thật.
    # ⚠ VÀ CHỈ KHI BÉ PHẢI ĐỌC. Câu "Nghe rồi bấm vào từ đúng." thì manh mối là
    # TIẾNG ĐỌC — bốn lựa chọn dài ngắn thế nào cũng không giúp bé đoán được. Bản
    # đầu soi cả chúng và bắn thêm 30 phát nữa, toàn phát hụt.
    doc_duoc = "___" in str(muc.get("text") or "")
    la_cau = len(ch) > 2 and all(len(str(c).split()) >= 3 for c in ch)
    if dap and la_cau and doc_duoc:
        if sum(1 for c in ch if dang(c) == dang(dap)) == 1:
            ra.append("đáp án LẺ LOI về dáng câu — bé chọn bằng mắt, không cần đọc")
    if len(ch) != len(set(ch)):
        ra.append("hai lựa chọn TRÙNG chữ")
    for chuoi in [muc.get("text")] + list(muc.get("choices") or []):
        s = str(chuoi or "")
        if "..." in s or "…" in s:
            ra.append(f"còn dấu ba chấm của công thức: “{s[:44]}”")
        # `this/that` là cách SÁCH viết, để yên. Chỉ bắt dấu gạch chéo CÓ KHOẢNG
        # TRẮNG hai bên — đó mới là dấu ngăn hai nhánh của công thức lọt ra.
        # ⚠ KHÔNG PHẢI LỖI, NHƯNG ĐÁNG HỎI. " / " ở đây là cách SÁCH viết hai
        # nhánh trả lời ("Yes, I do. / No, I don't."), và bốn quyển trước cũng
        # bày y như thế. Vẫn nêu ra để bác quyết có cắt bớt một nhánh không —
        # nêu thì bác chọn được, im thì coi như tôi đã chọn thay bác.
        if re.search(r"\s/\s", s):
            ra.append("bày CẢ HAI nhánh trả lời “Yes… / No…” — cách sách viết, "
                      "bốn quyển trước cũng thế; bác muốn cắt còn một nhánh không?")
        if " + " in s:
            ra.append(f"còn dấu cộng của công thức: “{s[:44]}”")
        if "  " in s.strip():
            ra.append(f"hai dấu cách liền: “{s[:44]}”")
    return ra


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

    cn = json.loads((GOC / f"data/tienganh/chuan_lop{LOP}.json").read_text("utf8"))
    bu = json.loads((GOC / f"data/tienganh/lop{LOP}_bu.json").read_text("utf8"))
    bais = {}
    for f in sorted((GOC / "web/public/content/ta5").glob("DL_TA5_B*.json")):
        b = json.loads(f.read_text("utf8"))
        bais[b["so"]] = b
    noi = {int(k["bai"].split(".B")[1]): k for k in json.loads(
        (GOC / "web/public/content/ta5/kichban_noi.json").read_text("utf8"))}
    chuong_cua = {u: int(c) for c, m in cn["chuong"].items() for u in m["unit"]}

    wb = Workbook()
    vien = Border(*[Side(style="thin", color="C8D4E2")] * 4)
    vang = PatternFill("solid", fgColor="FFF3D6")
    do = PatternFill("solid", fgColor="FBE0DC")

    def dau_bang(ws, cot):
        ws.append(cot)
        for i, _ in enumerate(cot, 1):
            o = ws.cell(row=1, column=i)
            o.font = Font(bold=True, color="FFFFFF", size=11)
            o.fill = PatternFill("solid", fgColor="0B4EA8")
            o.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 40

    # ══════════════ SHEET 1 · 20 BÀI ══════════════
    ws = wb.active
    ws.title = "20 bài"
    dau_bang(ws, ["Bài", "Chương", "Tên bài (Việt · Anh)", "Từ mới",
                  "MẪU CÂU sách dạy (+ câu ví dụ)",
                  "CÂU MÁY SINH — bé sẽ đọc những câu này",
                  "Luyện tập", "Sát hạch", "Phòng nói",
                  "Chỗ tôi sửa so với sách", "Bác duyệt"])
    SUA = {}
    for ma, m in (bu.get("mau_cau") or {}).items():
        if m.get("_ghi"):
            u = int(re.search(r"_u(\d+)_", ma).group(1))
            SUA.setdefault(u, []).append(f"[{ma}] {m['_ghi']}")
    for ma, m in (bu.get("sua_slot") or {}).items():
        if ma.startswith("_") or not m.get("_ghi"):
            continue
        u = int(re.search(r"_u(\d+)_", ma).group(1))
        SUA.setdefault(u, []).append(f"[{ma}] {m['_ghi']}")

    d = 1
    for u in cn["unit"]:
        so = u["so"]
        b = bais.get(so)
        if not b:
            continue
        d += 1
        mau = "\n\n".join(f"▸ {m.get('cong_thuc')}\n   sách: {m.get('vi_du')}"
                          for m in u["mau_cau"])
        cau = "\n".join(f"· {c}" for c in b["knowledgeCore"]["canonicalExamples"])
        pools = b["practice"]["pools"]
        kb = noi.get(so, {})
        ws.append([f"U{so:02d}", chuong_cua.get(so, ""), u["canh"],
                   " · ".join(t["tu"] for t in u["tu"]),
                   mau, cau,
                   f"★ {len(pools.get('warmup', []))}\n"
                   f"★★ {len(pools.get('standard', []))}\n"
                   f"★★★ {len(pools.get('challenge', []))}",
                   f"{len(b['assessment']['items'])} câu",
                   f"{len(kb.get('buoc') or [])} bước",
                   "\n\n".join(SUA.get(so, [])) or "— không sửa gì —", ""])
        if SUA.get(so):
            ws.cell(row=d, column=10).fill = vang
        ws.row_dimensions[d].height = 150
    for c, w in {"A": 6, "B": 7, "C": 30, "D": 40, "E": 56, "F": 60,
                 "G": 9, "H": 9, "I": 9, "J": 52, "K": 11}.items():
        ws.column_dimensions[c].width = w
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    ws.freeze_panes = "C2"

    # ══════════════ SHEET 2 · TỪNG CÂU MỘT ══════════════
    w2 = wb.create_sheet("Từng câu bé gặp")
    dau_bang(w2, ["Bài", "Bậc", "Dạng", "ĐỀ BÀI bé nhìn thấy",
                  "Các lựa chọn", "Đáp án", "MÁY SOI THẤY GÌ", "Bác duyệt"])
    d = 1
    ngo = 0
    for so in sorted(bais):
        b = bais[so]
        kho = tui_tu(so)
        muc = []
        for ten, ds in b["practice"]["pools"].items():
            muc += [(ten, x) for x in ds]
        muc += [("sát hạch", x) for x in b["assessment"]["items"]]
        for ten, x in muc:
            v = soi(x, kho)
            # chữ chưa dạy — soi riêng, vì cần túi từ của đúng unit ấy
            for s in [x.get("text")] + list(x.get("choices") or []):
                s = str(s or "")
                if not re.search(r"[A-Za-z]", s) or re.search(r"[^\x20-\x7E'’]", s):
                    continue
                la = [w for w in re.findall(r"[a-z']+", s.lower())
                      if w not in kho and not (w.endswith("'s") and w[:-2] in kho)]
                if la:
                    v.append(f"chữ chưa dạy tới bài này: {' · '.join(sorted(set(la)))}")
            d += 1
            ngo += 1 if v else 0
            w2.append([f"U{so:02d}", ten, x.get("format"),
                       str(x.get("text") or "").strip() or "(câu NHÌN–NGHE: đề là "
                       "bức hình cộng tiếng đọc, không có chữ)",
                       "\n".join(f"· {c}" for c in (x.get("choices") or [])),
                       str((x.get("answerKey") or {}).get("choice")
                           if (x.get("answerKey") or {}).get("choice") is not None
                           else (x.get("answerKey") or {}).get("value", "")),
                       "\n".join(f"⚠ {y}" for y in v), ""])
            if v:
                w2.cell(row=d, column=7).fill = do
    for c, w in {"A": 6, "B": 11, "C": 8, "D": 62, "E": 44, "F": 24,
                 "G": 60, "H": 11}.items():
        w2.column_dimensions[c].width = w
    for r in w2.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    w2.freeze_panes = "B2"
    w2.auto_filter.ref = f"A1:H{d}"

    # ══════════════ SHEET 3 · 187 TỪ ══════════════
    w3 = wb.create_sheet("187 từ")
    dau_bang(w3, ["Bài", "Từ", "Nghĩa", "Phiên âm", "Vai", "Số nhiều",
                  "Quá khứ", "Hình", "Vì sao không có hình", "Bác duyệt"])
    kv = (bu.get("hinh") or {}).get("_khong_ve") or {}
    vt = (bu.get("hinh") or {}).get("_ve_tay") or {}
    ten_vai = bu.get("vai_ten") or {}
    d = 1
    for u in cn["unit"]:
        for t in u["tu"]:
            d += 1
            h = t.get("hinh") or ""
            if t.get("hinh_ve"):
                h = f"{h}  → VẼ TAY “{t['hinh_ve']}”"
            w3.append([f"U{u['so']:02d}", t["tu"], t.get("nghia"), t.get("ipa"),
                       " · ".join(ten_vai.get(v, v) for v in (t.get("vai") or [])),
                       t.get("so_nhieu") or "", t.get("dang_qk") or "",
                       h or "—",
                       kv.get(t["tu"]) or (vt.get(t["tu"], {}).get("sai_o_dau")
                                           if t["tu"] in vt else ""), ""])
            if t["tu"] in vt:
                w3.cell(row=d, column=9).fill = vang
    for c, w in {"A": 6, "B": 30, "C": 30, "D": 26, "E": 22, "F": 18,
                 "G": 26, "H": 22, "I": 60, "J": 11}.items():
        w3.column_dimensions[c].width = w
    for r in w3.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    w3.freeze_panes = "C2"
    w3.auto_filter.ref = f"A1:J{d}"

    # ══════════════ SHEET 4 · LỜI DẪN ══════════════
    w4 = wb.create_sheet("Đọc trước")
    for r in [
        ["TIẾNG ANH LỚP 5 — BẢNG SOÁT 20 BÀI HỌC", ""],
        ["", ""],
        ["Soát cái gì",
         "Bảng từ vựng lấy thẳng từ sách nên ít rủi ro. Chỗ đáng soi là NHỮNG "
         "CÂU MÁY SINH RA: đúng công thức, mọi chữ đã học, cổng xanh — mà đọc "
         "lên vẫn có thể vô nghĩa. Sheet “Từng câu bé gặp” là chỗ ấy."],
        ["Máy đã soi giúp bốn phép",
         "① đáp án lẻ loi về dáng câu (bé chọn bằng mắt) · ② câu còn sót dấu "
         "công thức · ③ chữ chưa dạy tới bài ấy · ④ hai lựa chọn trùng nhau. "
         "Bốn phép ấy KHÔNG hiểu nghĩa — nên cột “Bác duyệt” vẫn là chỗ quyết."],
        ["", ""],
        ["LỚP 5 KHÁC BỐN QUYỂN TRƯỚC", ""],
        ["Thì QUÁ KHỨ",
         "Quyển đầu tiên cần. Bộ sinh chỉ biết dạng `-ing` và số nhiều; gặp ô "
         "[past verb] nó trả DẠNG GỐC và im lặng — suýt ra “We visit the old "
         "buildings last summer.” Nay khai `dang_qk` cho 27 cụm việc, và từ nào "
         "thiếu dạng thì bị LOẠI khỏi kho chứ không điền bừa."],
        ["Hai ô cùng một từ",
         "“Did you [Verb]? - Yes, I did. I [past verb].” Hai ô khác tên nên máy "
         "bốc độc lập: “Did you buy souvenirs? - Yes, I did. I swam.” Nay có cờ "
         "`cung_tu` buộc chúng là một việc, khác dạng."],
        ["21/40 mẫu nhiều ô",
         "Nhiều nhất trong năm quyển. Mẫu nhiều ô mà không khai ô thì bộ sinh bỏ "
         "CẢ MẪU, im lặng — U08 và U19 từng mất trắng bậc 2 vì thế."],
        ["", ""],
        ["CHƯA LÀM — chờ bác duyệt bảng này", ""],
        ["15 hình vẽ tay",
         "`crow` và `firefighter` là chuỗi ZWJ (vẽ ra chim + ô vuông đen, và mặt "
         "trơn + xe cứu hoả). `glue stick` ra băng dán, `pencil sharpener` ra "
         "cây bút chì, `jumper` ra cuộn len, `trousers` TRÙNG HỆT `jeans`, "
         "`cool` ra mặt đeo kính râm. Xem sheet “187 từ”, cột tô vàng."],
        ["20 cảnh tả tranh", "Theo đúng bốn luật bác chốt cho lớp 3·4."],
        ["925 clip tiếng · 45 video", "Dựng sau khi bác chốt nội dung."],
    ]:
        w4.append(r)
    w4.column_dimensions["A"].width = 26
    w4.column_dimensions["B"].width = 104
    for row in w4.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    for r in (1, 6, 11):
        w4.cell(row=r, column=1).font = Font(bold=True, size=13)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   20 bài · {d - 1} từ · {ngo} câu máy thấy đáng ngờ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
