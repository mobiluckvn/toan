#!/usr/bin/env python3
"""SINH BA MÀN CHO MỘT BỨC TRANH — đọc · viết · nói.

    python3 tools/sinh_bai_tranh.py --lop 3

Bác chốt 19-08-2026: một bức tranh làm nền cho cả ba màn. Đọc thì có tranh kèm đoạn
mô tả; viết thì CHỈ có tranh; nói thì bé nhìn tranh còn cô giáo máy cầm bản mô tả
bằng chữ.

Tệp này đọc `data/tienganh/tranh_lopN.json` rồi CHÈN THÊM mục vào ba tệp đã có:

    web/public/content/taN/dochieu.json        mục đọc, có `tranh`
    web/public/content/taN/vietbai.json        mục viết, có `tranh`
    web/public/content/taN/kichban_noi.json    kịch bản nói quanh tranh

── VÌ SAO CHÈN THÊM CHỨ KHÔNG THAY ──
Hai bộ sinh cũ (`sinh_dochieu_tienganh.py` · `sinh_vietbai_tienganh.py`) vẫn chạy
và vẫn đúng cho những unit chưa có tranh. Chạy tệp này SAU chúng thì unit nào có
tranh sẽ được thay bằng bản tranh, unit nào chưa có thì giữ nguyên. Nhờ thế bác thử
được một bài mà không phải chờ vẽ đủ 21 bức.

⚠ THỨ TỰ CHẠY: dochieu → vietbai → kichban_noi → **tệp này**. Chạy trước thì bản
tranh bị bộ sinh cũ ghi đè, và không có gì báo — cùng họ với
[[ban-dung-lai-de-mat-ban-sua-tay]].

── CÂU HỎI HỎI VỀ TRANH, KHÔNG PHẢI DÒ CHỮ ──
Đây là chỗ được nhất của lối tranh. Bài đọc cũ chỉ hỏi được "câu nào CÓ trong đoạn"
— bé dò chữ là xong, không cần hiểu. Có tranh thì hỏi được "trong tranh có mấy quả
bóng" và "câu nào ĐÚNG với bức tranh": bé phải đối chiếu chữ với hình, tức là phải
HIỂU câu ấy nói gì.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}
DUONG_TRANH = "tienganh/tranh"


def ma_am(loai: str, chu: str) -> str:
    """Cùng luật đặt mã với `tools/tts/sinh_am.py`. Lệch một ký tự là nút nghe câm."""
    import unicodedata
    s = unicodedata.normalize("NFKD", str(chu or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return f"{loai}_{s}"


def _tach_doi(s: str) -> list[str]:
    return [x.strip() for x in str(s or "").split(" - ") if x.strip()]


def _tron(dung: str, moi: list[str]) -> list[str]:
    """Xếp đáp án vào giữa đám mồi. KHÔNG random — chạy hai lần phải ra một tệp."""
    ds = list(moi)
    ds.insert(min(len(ds), (len(dung) + len(ds)) % (len(ds) + 1)), dung)
    return ds


def _dang(cau: str) -> tuple:
    return (cau.split()[0].lower(), len(cau.split())) if cau.split() else ("", 0)


def cau_hoi_tranh(k: dict, canh_khac: list[str]) -> list[dict]:
    """Bốn câu hỏi VỀ BỨC TRANH."""
    ra = []

    # ① Ở ĐÂU — thay cho câu "ý chính" cũ. Bé nhìn tranh là trả lời được, không
    #    phải đọc lấy một chữ tiếng Anh nào. Câu mở đầu nên dễ.
    ra.append({
        "id": "T1", "loai": "yChinh",
        "text": "Bức tranh này vẽ ở đâu?",
        "format": "chon",
        "choices": _tron(k["ten"], canh_khac[:3]),
        "answerKey": {"choice": k["ten"]},
        "solutionNarrative": f"Đây là cảnh {k['ten'].lower()}.",
    })

    # ② ĐẾM — con số lấy thẳng từ bản khai tranh, nên không thể lệch với hình.
    #    Mồi là những số GẦN, để bé phải đếm thật chứ không loại bằng cảm giác.
    for h in (k.get("hoiDem") or [])[:2]:
        so = h["so"]
        moi = [str(x) for x in (so - 1, so + 1, so + 2) if 1 <= x <= 10][:3]
        ra.append({
            "id": f"T{len(ra) + 1}", "loai": "chiTiet",
            "text": f"Trong tranh có mấy {h['viet']}?",
            "format": "chon",
            "choices": _tron(str(so), moi),
            "answerKey": {"choice": str(so)},
            "solutionNarrative": f"Con đếm lại nhé — có {so} {h['viet']}.",
        })

    # ③ CÂU NÀO ĐÚNG VỚI TRANH — chỗ bé phải đối chiếu chữ với hình.
    #    Đáp án lấy câu ĐƠN trong `moTa` (không phải nửa của cặp hỏi–đáp), mồi lấy
    #    từ `sai` — những câu người soạn khai là CHẮC CHẮN sai với tranh này.
    don = [c for c in k["moTa"] if " - " not in c]
    if don and k.get("sai"):
        dung = don[0]
        # Mồi khác khuôn nhau, đúng luật bác chốt 19-08: ba mồi giống hệt nhau thì
        # bé chọn đúng bằng HÌNH DẠNG mà không cần đọc.
        moi, khuon = [], {_dang(dung)}
        for x in k["sai"]:
            if _dang(x) in khuon:
                continue
            khuon.add(_dang(x))
            moi.append(x)
        if len(moi) >= 2:
            ra.append({
                "id": f"T{len(ra) + 1}", "loai": "chiTiet",
                "text": "Câu nào ĐÚNG với bức tranh?",
                "format": "chon",
                "choices": _tron(dung, moi[:3]),
                "answerKey": {"choice": dung},
                "solutionNarrative": f"“{dung}” — con nhìn lại tranh xem nhé.",
            })

    # ④ ĐÁP LẠI MỘT CÂU HỎI — dùng đúng cặp hỏi–đáp trong đoạn mô tả.
    cap = [c for c in k["moTa"] if " - " in c]
    if cap:
        hoi, dap = _tach_doi(cap[0])[:2]
        khac = [_tach_doi(c)[1] for c in cap[1:]] + [c for c in don if c != dap]
        moi, khuon = [], {_dang(dap)}
        for x in khac:
            if _dang(x) in khuon:
                continue
            khuon.add(_dang(x))
            moi.append(x)
        if len(moi) >= 2:
            ra.append({
                "id": f"T{len(ra) + 1}", "loai": "chiTiet",
                "text": f"Có người hỏi “{hoi}” — con đáp thế nào?",
                "format": "chon",
                "choices": _tron(dap, moi[:3]),
                "answerKey": {"choice": dap},
                "solutionNarrative": f"“{dap}”.",
            })
    return ra


def muc_doc(k: dict, lop: int, canh_khac: list[str]) -> tuple[dict, list[dict]]:
    """Mục đọc hiểu + những dòng cần clip tiếng."""
    dong = [x for c in k["moTa"] for x in _tach_doi(c)]
    cau = cau_hoi_tranh(k, canh_khac)
    muc = {
        "id": f"DOC:TA{lop}.U{k['unit']:02d}",
        "unit": k["unit"], "chapter": k.get("chuong", 1),
        "phamVi": "unit", "loai": "dochieu", "dang": "tranh",
        "name": f"ĐỌC HIỂU · UNIT {k['unit']} · {k['ten'].upper()}",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "tranhTen": k["ten"],
        # Đoạn mô tả giữ nguyên CẶP hỏi–đáp thành hai dòng, đúng cách đoạn hội thoại
        # đang làm — nút nghe của từng dòng mới khớp một clip.
        "doan": [{"cau": x, "am": ma_am("cau", x)} for x in dong],
        "cau": cau,
        "soCau": len(cau),
        "need": min(len(cau), max(2, len(cau) - 1)),
    }
    return muc, [{"id": ma_am("cau", x), "chu": x, "tieng": "en"} for x in dong]


def muc_viet(k: dict, lop: int, von: list[dict]) -> dict:
    """Mục bài viết — CHỈ có tranh, không có đoạn mô tả."""
    goi = []
    dem = [c for c in k["moTa"] if c.startswith("How many")]
    nhin = [c for c in k["moTa"] if c.startswith("I can see")]
    mau = [c for c in k["moTa"] if c.startswith("It's a") and " - " not in c]
    so = [c for c in k["moTa"] if c.startswith("What number")]
    if dem:
        goi.append({"nhan": "Đếm xem có mấy cái",
                    "cum": list(dict.fromkeys([x for c in dem for x in _tach_doi(c)]))})
    if nhin:
        goi.append({"nhan": "Nói con nhìn thấy gì", "cum": list(dict.fromkeys(nhin))})
    if mau:
        goi.append({"nhan": "Nói màu", "cum": list(dict.fromkeys(mau))})
    if so:
        goi.append({"nhan": "Đọc con số",
                    "cum": list(dict.fromkeys([x for c in so for x in _tach_doi(c)]))})
    return {
        "id": f"VIET:TA{lop}.U{k['unit']:02d}",
        "unit": k["unit"], "chapter": k.get("chuong", 1),
        "phamVi": "unit", "loai": "vietbai", "dang": "tranh",
        "name": f"BÀI VIẾT · UNIT {k['unit']} · {k['ten'].upper()}",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "tranhTen": k["ten"],
        "de": "Con nhìn bức tranh rồi viết 2–3 câu tả bức tranh nhé.",
        "toiThieu": 2,
        "mauCau": list(k["moTa"]),
        "goiY": goi,
        "vonTu": von,
        # Máy chấm đối chiếu với đây: bé viết được ý nào CÓ THẬT trong tranh thì
        # tính ý ấy. Không có nó thì máy chỉ chấm được ngữ pháp, và một câu đúng
        # ngữ pháp nhưng tả sai tranh vẫn qua.
        "yTrongTranh": list(k["moTa"]),
    }


def kich_ban_noi(k: dict) -> dict:
    """Kịch bản phòng nói quanh bức tranh.

    Cô giáo máy CÓ bản mô tả bằng chữ, bé thì chỉ nhìn tranh — bác chốt đúng thế.
    Nhờ vậy cô sửa được cả Ý chứ không chỉ sửa tiếng: bé nói "I can see two balls."
    thì cô biết là sai SỐ, vì bản mô tả ghi ba.
    """
    buoc = [{"loai": "chao", "en": "Hello!",
             "vi": "Chào con! Hôm nay cô con mình cùng tả một bức tranh nhé."}]
    # ĐƯỜNG LUI: tên từng vật trong tranh. Bé đuối thì `haDoKho` lùi về đây — chỉ
    # cần chỉ vào tranh và gọi tên một thứ, không phải nói cả câu.
    for n in k["nhom"]:
        buoc.append({"loai": "tu", "en": n["tu"], "tu": n["tu"],
                     "vi": f"Con tìm “{n['tu']}” trong tranh rồi nói tên nó nhé."})
    # CÔ LÀM MẪU TRƯỚC. Bé chưa bao giờ tả tranh bằng tiếng Anh; không có mẫu thì
    # lượt đầu tiên bé ngồi im. `buocTiepTheo` cũng đòi bước luyện đầu là `mau`.
    buoc.append({"loai": "mau", "en": k["moTa"][0], "mauCau": k["moTa"][0],
                 "vi": "Cô tả trước một câu, con nghe rồi nhìn vào tranh nhé."})
    for c in k["moTa"]:
        phan = _tach_doi(c)
        if len(phan) == 2:
            hoi, dap = phan
            buoc.append({"loai": "hoiBe", "en": hoi, "mauCau": c, "dapMau": dap,
                         "vi": f"Con nhìn tranh rồi đáp nhé. Con đáp theo khuôn: {dap}"})
        else:
            buoc.append({"loai": "noiCa", "en": phan[0], "mauCau": phan[0],
                         "vi": "Con nói lại cả câu này, rồi tìm nó trong tranh nhé."})
    buoc.append({"loai": "ket"})
    return {
        "bai": f"DL:TA3.B{k['unit']:02d}",
        "ten": f"Tả tranh · {k['ten']}",
        "muc_tieu": f"Tả được bức tranh “{k['ten']}” bằng câu đã học",
        "tinh_huong": f"Con và cô cùng nhìn một bức tranh: {k['ten'].lower()}.",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "moTaTranh": list(k["moTa"]),
        "dang": "tranh",
        "tu": [n["tu"] for n in k["nhom"]],
        "buoc": buoc,
        "tay": True,      # đừng để `sinh_kichban_noi.py` ghi đè
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3)
    p.add_argument("--thieu", help="ghi ra tệp những dòng chưa có clip")
    a = p.parse_args()
    q = QUYEN[a.lop]
    tm = GOC / f"web/public/content/{q}"

    kho = json.loads((GOC / f"data/tienganh/tranh_lop{a.lop}.json").read_text("utf8"))
    canh = [k["ten"] for k in kho]
    # Chưa đủ tranh để lấy mồi "ở đâu" từ chính chúng, nên mượn tên CẢNH của các
    # unit khác — đều là nơi bé đã gặp, nên mồi vẫn có nghĩa.
    #
    # ⚠ LẤY `canh` CỦA BẢN CHUẨN, KHÔNG LẤY TÊN UNIT. Bản đầu lấy tên unit và ra
    # bốn lựa chọn: "Trong cửa hàng đồ chơi · Khởi động · Chào hỏi · Tên của chúng
    # mình" — ba mồi không phải NƠI CHỐN nào cả, nên bé loại được mà không cần nhìn
    # tranh. Câu hỏi vẫn "chạy đúng", chỉ là không hỏi gì.
    ten_unit = []
    for l in range(1, a.lop + 1):
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{l}.json").read_text("utf8"))
        for u in cn["unit"]:
            c = str(u.get("canh") or "").split("·")[0].strip()
            # Chỉ nhận cái NÓI RA MỘT NƠI: "Ở chợ" · "Trong phòng ngủ" · "Bên hồ".
            if c and re.match(r"^(Ở|Trong|Bên|Tại)\b", c):
                ten_unit.append(c)
    ten_unit = list(dict.fromkeys(ten_unit))

    docs = json.loads((tm / "dochieu.json").read_text("utf8"))
    viets = json.loads((tm / "vietbai.json").read_text("utf8"))
    kbs = json.loads((tm / "kichban_noi.json").read_text("utf8"))
    loi = []

    for k in kho:
        khac = [t for t in ten_unit if t != k["ten"]][:3] or ["Ở vườn thú", "Trong bếp"]
        muc, am = muc_doc(k, a.lop, khac)
        loi += am
        docs = [x for x in docs if x["id"] != muc["id"]] + [muc]

        # Vốn từ cho bài viết: lấy lại của mục cũ nếu có, không thì gom từ tranh.
        cu = next((x for x in viets if x.get("unit") == k["unit"]
                   and x.get("phamVi") == "unit"), None)
        von = (cu or {}).get("vonTu") or [{"tu": n["tu"], "nghia": ""} for n in k["nhom"]]
        mv = muc_viet(k, a.lop, von)
        viets = [x for x in viets if x["id"] != mv["id"]] + [mv]

        kb = kich_ban_noi(k)
        kbs = [x for x in kbs if x["bai"] != kb["bai"]] + [kb]
        print(f"  unit {k['unit']}: {len(muc['doan'])} dòng · {len(muc['cau'])} câu hỏi "
              f"· {len(mv['goiY'])} nhóm gợi ý · {len(kb['buoc'])} bước nói")

    docs.sort(key=lambda x: (x.get("chapter", 0), x.get("phamVi") != "unit",
                             x.get("unit", 99)))
    viets.sort(key=lambda x: (x.get("chapter", 0), x.get("phamVi") != "unit",
                              x.get("unit", 99)))
    kbs.sort(key=lambda x: x["bai"])
    (tm / "dochieu.json").write_text(json.dumps(docs, ensure_ascii=False, indent=1), "utf8")
    (tm / "vietbai.json").write_text(json.dumps(viets, ensure_ascii=False, indent=1), "utf8")
    (tm / "kichban_noi.json").write_text(
        json.dumps(kbs, ensure_ascii=False, indent=1) + "\n", "utf8")
    (GOC / f"data/tienganh/kichban_noi_lop{a.lop}.json").write_text(
        json.dumps(kbs, ensure_ascii=False, indent=1) + "\n", "utf8")
    print(f"→ {tm.relative_to(GOC)}/  (dochieu · vietbai · kichban_noi)")

    if a.thieu:
        so = json.loads((GOC / f"web/public/content/tienganh/lop{a.lop}_am.json")
                        .read_text("utf8"))
        co = {c["id"] for c in so.get("clip", [])}
        con = [m for m in {x["id"]: x for x in loi}.values() if m["id"] not in co]
        Path(a.thieu).write_text(json.dumps(con, ensure_ascii=False, indent=1), "utf8")
        print(f"{len(con)} dòng chưa có clip → {a.thieu}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
