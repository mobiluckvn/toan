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

def muc_doc(k: dict, lop: int) -> tuple[dict, list[dict]]:
    """Mục ĐỌC — một ĐOẠN mô tả tranh, KHÔNG câu hỏi.

    ══ BÁC BẮT LÀM LẠI 19-08-2026 ══

        "phần đọc sẽ là các câu mô tả tranh, viết thành một đoạn không viết rời rạc
         như bạn đang làm. […] Rõ ràng mô tả tranh thì làm gì có câu hỏi mà nhét câu
         hỏi vô làm gì. Câu hỏi dùng cho cô giáo gợi ý học sinh để tả thôi."

    Bản trước tôi làm sai hai chỗ cùng lúc: đoạn là mấy cặp HỎI–ĐÁP xếp cạnh nhau
    (không phải văn mô tả), và nhét thêm năm câu trắc nghiệm. Cả hai đều là thói
    quen của bài đọc hiểu cũ, mang nguyên sang chỗ không hợp.

    Nay: đúng một đoạn văn kể, đọc xong là xong. Không có gì để bấm ngoài nút nghe
    và nút "con đọc xong rồi".
    """
    muc = {
        "id": f"DOC:TA{lop}.U{k['unit']:02d}",
        "unit": k["unit"], "chapter": k.get("chuong", 1),
        "phamVi": "unit", "loai": "dochieu", "dang": "tranh",
        "name": f"ĐỌC · UNIT {k['unit']} · {k['ten'].upper()}",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "tranhTen": k["ten"],
        "doan": [{"cau": x, "am": ma_am("cau", x)} for x in k["doan"]],
        "cau": [],
    }
    return muc, [{"id": ma_am("cau", x), "chu": x, "tieng": "en"} for x in k["doan"]]


def tu_trong_tranh(k: dict, lop: int) -> list[dict]:
    """Bảng từ cho màn viết: đúng những VẬT CÓ TRONG TRANH, kèm nghĩa của sách.

    ⚠ Bản đầu lấy `vonTu` của mục viết cũ — tức là vốn từ của chính unit 0, tức là
    mười con số. Bé nhìn tranh thấy diều và mèo con, mở bảng từ ra thấy one · two ·
    three: không gõ nổi một câu nào. Từ phải là từ CỦA BỨC TRANH, mà tranh thì cố ý
    lấy vật từ lớp 1·2.
    """
    nghia = {}
    for l in range(1, lop + 1):
        tm = GOC / f"web/public/content/{QUYEN[l]}"
        for f in sorted(tm.glob(f"DL_{QUYEN[l].upper()}_B*.json")):
            b = json.loads(f.read_text("utf8"))
            for v in b["knowledgeCore"]["vocabulary"]:
                nghia.setdefault(v["tu"], v.get("nghia") or "")
    ra = [{"tu": n["tu"], "nghia": nghia.get(n["tu"], "")} for n in k["nhom"]]
    # Thêm mấy chữ NỀN của khuôn mô tả — không có chúng thì bấm được vật mà không
    # ghép được câu.
    for t in ("I", "can", "see", "this", "is", "there's", "a"):
        ra.append({"tu": t, "nghia": ""})
    return ra


def muc_viet(k: dict, lop: int, von: list[dict]) -> dict:
    """Mục VIẾT — tranh và một cái ô trống. Không câu hỏi, không mẫu câu.

    Bác chốt: "Về phần viết cũng vậy." Bày mẫu câu ra thì bé chép lại, mà bản mẫu
    câu của bài tả tranh CHÍNH LÀ đoạn mô tả — tức là cho sẵn đáp án.

    Bảng từ thì giữ: bé lớp 3 gõ tiếng Anh còn chậm, và bấm một TỪ không phải là
    được cho một CÂU.
    """
    return {
        "id": f"VIET:TA{lop}.U{k['unit']:02d}",
        "unit": k["unit"], "chapter": k.get("chuong", 1),
        "phamVi": "unit", "loai": "vietbai", "dang": "tranh",
        "name": f"VIẾT · UNIT {k['unit']} · {k['ten'].upper()}",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "tranhTen": k["ten"],
        "de": "Con nhìn bức tranh rồi viết một đoạn tả bức tranh nhé.",
        "toiThieu": 2,
        "mauCau": [],
        "goiY": [],
        "vonTu": von,
        # Máy chấm đối chiếu với đây — bé viết được ý nào CÓ THẬT trong tranh thì
        # tính ý ấy. Không bày ra màn hình.
        "yTrongTranh": list(k["doan"]),
    }


def kich_ban_noi(k: dict) -> dict:
    """Kịch bản NÓI — chỉ một việc: tả bức tranh.

    ══ BÁC TẢ ĐÚNG NHỊP CẦN CÓ, 19-08-2026 ══

        "Phần Nói bạn hãy xoá tất cả các thứ đi. Chỉ để một bức tranh sau đó yêu cầu
         học sinh mô tả bức tranh. Khi học sinh nói thì căn cứ theo mô tả tranh bạn
         có bạn sẽ hướng dẫn học sinh mô tả được tranh. […] Ví dụ học sinh không
         biết tả thì cô hỏi how many kite in the picture. Nếu học sinh trả lời đúng
         thì okay sau vài câu trả lời thì cô xâu chuỗi lại thành 01 đoạn nói cho học
         sinh nói cả đoạn đó."

    Ba nhịp, đúng thế:

        taTranh   cô mời bé tả — "What can you see?" (câu của sách, L2 U04)
        goiY      bé bí thì cô HỎI từng chi tiết một
        caDoan    tả được rồi thì cô xâu chuỗi, bé nói cả đoạn

    KHÔNG có bước chào, không có bước từ mới, không có bước mẫu câu. Bác bảo xoá
    tất cả các thứ khác đi thì xoá thật — để lại là bé lại đi nhại từ như cũ.

    `goiY` cũng chính là ĐƯỜNG LUI khi bé đuối (`haDoKho`): bí thì được hỏi, đúng
    như bác tả. Nên kịch bản này không cần bước `tu` nào.
    """
    buoc = [{
        "loai": "taTranh",
        "en": "What can you see?",
        "vi": "Con nhìn bức tranh rồi tả cho cô nghe nhé. Con thấy gì trong tranh?",
    }]
    for h in k.get("hoiGoiY") or []:
        if not h.get("dap"):
            continue          # câu mời chung đã là bước `taTranh` ở trên
        buoc.append({
            "loai": "goiY", "en": h["hoi"], "dapMau": h["dap"],
            "vi": f"Con nhìn tranh rồi đáp nhé — {h.get('y') or 'con xem kỹ trong tranh'}.",
        })
    # XÂU CHUỖI: cả đoạn thành MỘT lượt nói. Đây là đích của cả buổi.
    buoc.append({
        "loai": "caDoan",
        "en": " ".join(k["doan"]),
        "vi": "Giỏi lắm! Giờ con nói cả đoạn cho cô nghe nhé.",
    })
    buoc.append({"loai": "ket"})
    return {
        "bai": f"DL:TA3.B{k['unit']:02d}",
        "ten": f"Tả tranh · {k['ten']}",
        "muc_tieu": f"Tả được bức tranh “{k['ten']}” thành một đoạn",
        "tinh_huong": f"Con và cô cùng nhìn một bức tranh: {k['ten'].lower()}.",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "moTaTranh": list(k["doan"]),
        "dang": "tranh",
        "tu": [n["tu"] for n in k["nhom"]],
        "buoc": buoc,
        "tay": True,
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
    docs = json.loads((tm / "dochieu.json").read_text("utf8"))
    viets = json.loads((tm / "vietbai.json").read_text("utf8"))
    kbs = json.loads((tm / "kichban_noi.json").read_text("utf8"))
    loi = []

    for k in kho:
        muc, am = muc_doc(k, a.lop)
        loi += am
        docs = [x for x in docs if x["id"] != muc["id"]] + [muc]

        mv = muc_viet(k, a.lop, tu_trong_tranh(k, a.lop))
        viets = [x for x in viets if x["id"] != mv["id"]] + [mv]

        kb = kich_ban_noi(k)
        kbs = [x for x in kbs if x["bai"] != kb["bai"]] + [kb]
        print(f"  unit {k['unit']}: đoạn {len(muc['doan'])} câu "
              f"· {len(kb['buoc'])} bước nói")

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
