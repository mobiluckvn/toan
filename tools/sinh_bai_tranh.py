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
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "tools"))
from nut_tri_thuc import (kho_nut, nut_cua_bai_viet,  # noqa: E402
                          nut_cua_cau)

# Kho nút của quyển đang dựng — nạp một lần ở `main`.
KHO_NUT = [{}]
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3", 4: "ta4", 5: "ta5"}
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
def cau_hoi_sau_doc(k: dict) -> list[dict]:
    """CÂU HỎI SAU KHI ĐỌC — hỏi BẰNG TIẾNG ANH.

    ══ BÁC CHỐT 19-08-2026 ══
        "phần câu hỏi và câu trả lời của bài đọc hãy dùng tiếng anh bạn ơi."

    Trước đó câu hỏi và cả bốn lựa chọn đều bằng tiếng Việt — bé đọc xong đoạn tiếng
    Anh rồi trả lời tiếng Việt, tức là phần luyện ĐỌC dừng lại ngay khi hết đoạn.

    ⚠ NHƯNG CHỈ ĐƯỢC HỎI BẰNG KHUÔN ĐÃ HỌC. Câu hỏi khai tay ở `hoiDoc` của bản
    khai tranh, và cổng soi lại từng chữ theo túi từ tích luỹ — hỏi bằng một khuôn
    bé chưa gặp thì bài đọc hiểu hoá ra bài đoán đề.

    Lời Việt vẫn còn ở `phu`, nhưng là dòng NHỎ dưới câu tiếng Anh: bé đọc được thì
    đọc tiếng Anh, chưa được thì có chỗ bám. Lựa chọn thì THUẦN tiếng Anh — đó mới
    là chỗ bé luyện đọc thật.
    """
    ra = []
    for h in k.get("hoi") or []:
        moi = list(h.get("moi") or [])
        if len(moi) < 2:
            # Mồi nhử KHAI TAY ở bản khai, vì mồi phải SAI VỚI BỨC TRANH NÀY mà
            # máy không biết bức tranh có gì. Bản trước để máy suy và đẻ ra câu
            # hỏi hai đáp án đúng — thà kêu còn hơn im lặng bỏ câu.
            raise SystemExit(f"✗ U{k['unit']:02d} “{h['hoi']}”: mồi nhử chỉ có "
                             f"{len(moi)} — cần ít nhất 2")
        if h["dap"] in moi:
            raise SystemExit(f"✗ U{k['unit']:02d} “{h['hoi']}”: mồi nhử TRÙNG đáp án")
        ra.append({
            "id": f"T{len(ra) + 1}",
            "loai": "yChinh" if len(ra) == 0 else "chiTiet",
            "text": h["hoi"],
            "phu": h["vi"],
            "format": "chon",
            "choices": _tron(h["dap"], moi[:3]),
            "answerKey": {"choice": h["dap"]},
            "solutionNarrative": f"Nhìn trong tranh: “{h['dap']}”.",
            # MÃ NÚT — thiếu nó thì lượt trả lời không vào engine được. Luật gán
            # dùng chung ở `tools/nut_tri_thuc.py`.
            **nut_cua_cau(h["dap"], h["hoi"], " ".join(k.get("doan") or []),
                          KHO_NUT[0]),
        })
    return ra


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
        # SONG NGỮ — bác chốt 19-08: "Tiêu đề của bài đọc thì cũng cần là song ngữ."
        # Tên tiếng Anh nằm sẵn ở `ten_en` của bản khai; thiếu thì chỉ có tiếng Việt,
        # chứ không tự dịch — dịch bừa là đẻ ra một cái tên không có trong sách.
        "name": (f"ĐỌC · UNIT {k['unit']} · {k['ten'].upper()}"
                 + (f" · {k['ten_en'].upper()}" if k.get('ten_en') else '')),
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "tranhTen": k["ten"] + (f" · {k['ten_en']}" if k.get("ten_en") else ""),
        "doan": [{"cau": x, "am": ma_am("cau", x)} for x in k["doan"]],
        "cau": cau_hoi_sau_doc(k),
    }
    muc["soCau"] = len(muc["cau"])
    muc["need"] = min(muc["soCau"], max(2, muc["soCau"] - 1))
    return muc, [{"id": ma_am("cau", x), "chu": x, "tieng": "en"} for x in k["doan"]]


# Những chữ mà NGHĨA TỪ ĐIỂN sẽ đánh lừa bé khi chúng đứng làm chữ nối.
# ⚠ "can" trong "I can see a board." từng được chú là "cái lon" — đúng nghĩa từ
# vựng của `can` ở bài đồ uống, nhưng sai hẳn với chỗ nó đang đứng. Bảng từ màn
# viết là thứ bé đọc để ghép câu, nên một nghĩa sai ở đây là dạy sai.
KHONG_CHU = {"can", "see", "do", "does", "did", "have", "has", "is", "are",
             "was", "were", "am", "be", "will", "would", "like", "there",
             "that", "that's", "there's", "this", "it", "it's", "a", "an",
             "the", "and", "to", "of", "s", "left", "right", "watch", "play",
             # Chữ RÚT GỌN — cùng loại với `it's` · `that's` · `there's` đã có ở
             # trên, chỉ là sót. Chú nghĩa cho chúng còn tệ hơn để trống: `He's`
             # là "bạn ấy LÀ" trong "He's my friend" nhưng là "bạn ấy ĐANG" trong
             # "He's reading books" — một dòng nghĩa không nói được cả hai.
             "he's", "she's", "they're", "i'm", "i'd", "i'll", "we'll"}

# ⚠ TÁCH CHỮ PHẢI GIỮ GẠCH NỐI.
#
# Bản cũ dùng `[A-Za-z][A-Za-z']*`, không biết gạch nối. Hậu quả bé gánh:
#   · `T-shirt` đẻ thêm hai ô rác — bài ta4 U18 hiện ĐỦ CẢ BA ô T-shirt · T · shirt;
#   · `Mid-Autumn Festival` thành ba ô rời, mà KHÔNG có ô gạch nối nào để ghép lại,
#     nên bé không có cách nào viết đúng tên ngày hội ấy;
#   · `twenty-nine` rụng mất nửa sau.
# Đây là lỗi làm bé viết SAI, nặng hơn hẳn việc thiếu một dòng nghĩa.
TACH_CHU = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def tach_chu(s: str) -> list[str]:
    return [w for w in (x.strip("-") for x in TACH_CHU.findall(s)) if w]


# Nghĩa cho những chữ ĐỨNG MỘT MÌNH thật, không phải mảnh vỡ của cụm nào.
#
# ⚠ BẢNG NÀY PHẢI NHỎ, VÀ NHỎ LÀ DẤU HIỆU TỐT. Bản đầu tôi khai 59 mục — chú
# nghĩa cho từng mảnh vỡ của cụm. Khi bước ①b biết giữ nguyên cụm thì 35 mục
# thành thừa: `collected` · `watering` · `break` · `tennis` … không còn đứng một
# mình ở đâu nữa. Đã xoá hết 35 mục ấy.
#
# Xoá chứ không giữ "phòng khi cần": mục không ai dùng thì không ai kiểm, mà một
# nghĩa SAI nằm đây thì không cổng nào bắt được — nó chỉ chờ một quyển sau vô
# tình sinh ra đúng chữ ấy. Thiếu thì cổng `tienganh_bangtu_viet` đỏ ngay, và
# đỏ ồn ào tốt hơn sai lặng lẽ.
#
# Đây cũng là chỗ DUY NHẤT nghĩa do tôi viết chứ không phải sách chú — nên là
# chỗ bác đọc lại. Xem trang "Nghĩa tôi viết tay" trong `docs/soat_vontu.xlsx`.
NGHIA_LE = {
    # đại từ — `I` và `my` sách đã chú, bốn chữ này thì sót
    "he": "bạn ấy (nam)", "she": "bạn ấy (nữ)", "we": "chúng mình",
    "you": "bạn, con",
    # chữ sách dùng trong MẪU CÂU nhưng không khai thành mục từ vựng
    "animal": "con vật", "subject": "môn học", "wear": "mặc",
    "want": "muốn", "think": "nghĩ", "should": "nên", "from": "từ",
    "at": "ở, tại", "by": "bằng, bởi",
    # dạng chia đứng lẻ, gốc lại không có mục riêng
    "goes": "đi", "likes": "thích", "works": "làm việc", "years": "năm",
    # danh từ lẻ mà kho chỉ dạy trong cụm ("water park" · "take photos" …)
    "flower": "bông hoa", "home": "nhà", "park": "công viên",
    "photo": "tấm ảnh", "picture": "bức tranh", "tv": "ti vi",
    # tên riêng tiếng Việt viết không dấu trong bài đọc — chú ở đây chính là cho
    # bé thấy MẶT CHỮ CÓ DẤU của cái tên em ấy vẫn đọc hằng ngày
    "tran hung dao": "Trần Hưng Đạo (tên phố)",
}

# Dạng SỐ NHIỀU suy được bằng máy: tiếng Việt không đánh dấu số nhiều nên nghĩa
# của `books` đúng bằng nghĩa của `book`.
# ⚠ CHỈ danh từ số nhiều. KHÔNG suy cho `-ing` · `-ed` · động từ chia `-s`: ở đó
# nghĩa CHUYỂN, và gốc có khi lại là danh từ — `water` là "nước", suy ra thì
# `watering` thành "nước" thay vì "tưới". Những dạng ấy khai tay ở `NGHIA_LE`.
KHONG_SUY_SO_NHIEU = {"likes", "plays", "goes", "works", "does", "has", "is",
                      "was", "years", "sports"}


# Dạng chia của ĐỘNG TỪ ĐỨNG ĐẦU CỤM.
#
# Sách dạy cụm ở thể gốc — "collect seashells" · "take photos" · "go camping".
# Đoạn văn thì kể chuyện đã xảy ra: "We collected seashells." Hai bên không nhận
# ra nhau thì cụm bị xé, và đó đúng là 8 trong 9 ô còn sót sau bước ①b.
BAT_QUY_DONG_TU = {
    "go": ["goes", "going", "went", "gone"],
    "take": ["takes", "taking", "took", "taken"],
    "do": ["does", "doing", "did", "done"],
    "run": ["runs", "running", "ran"],
    "buy": ["buys", "buying", "bought"],
    "eat": ["eats", "eating", "ate", "eaten"],
    "see": ["sees", "seeing", "saw", "seen"],
    "swim": ["swims", "swimming", "swam"],
    "have": ["has", "having", "had"],
}


def dang_chia(w: str) -> list[str]:
    """Mọi dạng chia có thể của một động từ. Dạng nào không có thật thì cũng
    chỉ là một nhánh regex không bao giờ khớp — không hại gì."""
    ds = {w, w + "s", w + "ing", w + "ed"}
    if w.endswith("e"):
        ds |= {w[:-1] + "ing", w + "d"}
    if w.endswith("y"):
        ds |= {w[:-1] + "ies", w[:-1] + "ied"}
    ds |= set(BAT_QUY_DONG_TU.get(w, ()))
    return sorted(ds, key=len, reverse=True)


def khuon_cum(t: str) -> re.Pattern:
    """Khuôn bắt một cụm, cho phép chữ ĐẦU chia thể."""
    dau, *con = t.split(" ")
    dau_alt = "|".join(re.escape(x) for x in dang_chia(dau))
    duoi = (r"\s+" + r"\s+".join(re.escape(x) for x in con)) if con else ""
    return re.compile(rf"(?<![A-Za-z])({dau_alt}){duoi}(?![A-Za-z])", re.I)


def cum_tu_vung(nghia: dict) -> list[tuple[str, str]]:
    """Mọi CỤM tra được, dài trước ngắn sau — dùng chung với `tools/soat_vontu.py`.

    Tách ra thành hàm riêng vì bộ soi cũng cần đúng danh sách này. Để mỗi bên tự
    dựng lấy thì sớm muộn hai bên lệch nhau, và bộ soi báo "không truy được nguồn"
    cho những ô hoàn toàn lành — đã xảy ra đúng một lần, 30 ô.
    """
    ra = []
    for t, g in nghia.items():
        if not g or not re.search(r"[ \-]", t):
            continue
        # "get (to)" — phần trong NGOẶC là tuỳ chọn: sách gộp "get to school" và
        # "get there" vào một mục. Sinh cả hai khuôn, để cái nào khớp thì khớp.
        bien = ({re.sub(r"\s*\([^)]*\)", "", t).strip(),
                 t.replace("(", "").replace(")", "").strip()}
                if "(" in t else {t})
        ra += [(b, g) for b in bien if b]
    ra.sort(key=lambda x: len(x[0]), reverse=True)
    return ra


def nghia_goc(t: str, nghia: dict) -> str:
    """Nghĩa suy từ dạng SỐ ÍT, nếu có. Không có thì trả chuỗi rỗng."""
    w = t.lower()
    if w in KHONG_SUY_SO_NHIEU or not w.endswith("s"):
        return ""
    for goc in (t[:-1], t[:-2] if w.endswith("es") else None):
        if goc and nghia.get(goc):
            return nghia[goc]
        if goc and nghia.get(goc.lower()):
            return nghia[goc.lower()]
    return ""


def tu_trong_tranh(k: dict, lop: int) -> list[dict]:
    """Bảng từ cho màn viết — ĐỦ ĐỂ VIẾT LẠI CẢ ĐOẠN MÔ TẢ.

    ══ BÁC CHỐT 19-08-2026 ══
        "Phần từ trong tranh cần đầy đủ hơn như nội dung của phần đọc (ít nhất là
         thế)."

    Bản trước gom tên VẬT rồi thêm tay bảy chữ nối đoán chừng — và đoán thiếu:
    "That's" của câu "That's a yo-yo." không có trong bảng, nên bé bấm hết bảng vẫn
    không viết nổi đoạn mà chính bài đọc vừa cho đọc.

    Nay suy THẲNG từ đoạn mô tả: mọi chữ trong đoạn đều phải có mặt. Đoán thì còn
    thiếu, chứ suy từ đoạn thì không thể thiếu.

    Ba nhóm, xếp theo việc:
      · VẬT trong tranh — kèm nghĩa, đây là thứ bé chọn để nói về;
      · CHỮ NỐI lấy từ chính đoạn (This · I · can · see · That's · There's…);
      · SỐ trên tấm biển, cộng "It's" để nói về nó — tranh có mà đoạn không nhắc,
        bé muốn viết thêm thì phải có chữ.
    """
    nghia = {}
    for l in range(1, lop + 1):
        tm = GOC / f"web/public/content/{QUYEN[l]}"
        for f in sorted(tm.glob(f"DL_{QUYEN[l].upper()}_B*.json")):
            b = json.loads(f.read_text("utf8"))
            for v in b["knowledgeCore"]["vocabulary"]:
                nghia.setdefault(v["tu"], v.get("nghia") or "")

    ra, da = [], set()

    def them(t, ng=""):
        if t and t.lower() not in da:
            da.add(t.lower())
            g = "" if t.lower() in KHONG_CHU else (
                ng or nghia.get(t) or NGHIA_LE.get(t.lower()) or nghia_goc(t, nghia))
            ra.append({"tu": t, "nghia": g})

    cau_ds = list(k["doan"]) + [h["dap"] for h in (k.get("hoi") or [])]

    # ① vật trong tranh — nay lấy từ `vat`, mục nào khai `tu` là một từ vựng thật
    for n in k["vat"]:
        if n.get("tu"):
            them(n["tu"])

    # ①b CỤM TỪ VỰNG NHIỀU CHỮ — thêm NGUYÊN CỤM, không để bị xé ra.
    #
    # ⚠ Đây là chỗ đẻ ra 48 trong 105 ô "không có nghĩa". Kho từ vựng dạy rất
    # nhiều CỤM ("break time" · "table tennis" · "set square" · "collect
    # seashells"), mà bảng nghĩa tra bằng NGUYÊN VĂN khoá. Xé cụm ra thì chữ lẻ
    # không khớp khoá nào → ô trống nghĩa.
    #
    # Và tệ hơn hẳn chuyện trống nghĩa: chữ lẻ ĐỔI NGHĨA khi rời cụm. "table
    # tennis" là BÓNG BÀN, `tennis` một mình là quần vợt; "set square" là cái
    # ê-ke, `set` một mình thì không; "first floor" kiểu Anh là TẦNG HAI. Có lúc
    # tôi định chú nghĩa cho từng chữ lẻ — làm thế là dạy sai. Giữ nguyên cụm thì
    # không phải chọn nghĩa nào cả, và bé bấm một cái được đúng thứ sách dạy.
    #
    # Dài trước ngắn sau, để "table tennis" ăn trước "table".
    cum = cum_tu_vung(nghia)

    for c in cau_ds:
        con = c
        for t, g in cum:
            kh = khuon_cum(t)
            m = kh.search(con)
            if not m:
                continue
            # Ô mang ĐÚNG chữ trong đoạn ("collected seashells"), nhưng nghĩa lấy
            # của cụm gốc — tiếng Việt không đổi dạng theo thì, nên nghĩa vẫn
            # đúng, mà bé bấm một cái là ra đúng chữ bài đọc vừa cho đọc.
            them(m.group(0), g)
            # ⚠ XOÁ KHỎI CÂU rồi mới xét cụm ngắn hơn. Không xoá thì "get up" và
            # "get" cùng khớp một chỗ và đẻ ra hai ô cho một chữ.
            con = kh.sub(" ", con)

    # ② mọi chữ của đoạn mô tả, giữ nguyên dạng viết trong đoạn ("That's", "This")
    # ③ và mọi chữ trong ĐÁP ÁN câu hỏi — bé muốn viết thêm ý ấy thì phải có chữ.
    #    Suy từ đáp án chứ không đoán: đoán là chỗ bản trước thiếu mất "That's".
    for c in cau_ds:
        # Bỏ những chữ đã nằm trong một CỤM đã thêm ("teddy bear" → bỏ teddy, bear).
        con = c
        for t in sorted(da, key=len, reverse=True):
            con = re.sub(rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])", " ", con,
                         flags=re.I)

        # ②b TÊN RIÊNG NHIỀU CHỮ — dãy chữ hoa liền nhau, KHÔNG tính chữ mở câu.
        #
        # "I live in Tran Hung Dao Street." từng thành bốn ô rời `Tran` · `Hung`
        # · `Dao` · `Street`, và ba ô đầu là ba ô cuối cùng còn trống nghĩa trong
        # cả năm quyển. Chúng không phải tên ba người — chúng là một cái tên phố
        # bị xé làm ba. Kho từ vựng không dạy tên phố nên khớp-cụm không với tới.
        #
        # ⚠ Phải bỏ chữ MỞ CÂU: "Mary is my friend." thì `Mary` viết hoa chỉ vì
        # đứng đầu câu. Nên chỉ nhận dãy từ hai chữ hoa trở lên và không bắt đầu
        # ở vị trí 0.
        for m in re.finditer(r"[A-Z][A-Za-z'\-]*(?:\s+[A-Z][A-Za-z'\-]*)+", con):
            if m.start() == 0:
                continue
            them(m.group(0))
            con = con[:m.start()] + " " * len(m.group(0)) + con[m.end():]

        for w in tach_chu(con):
            them(w)
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
        "name": (f"VIẾT · UNIT {k['unit']} · {k['ten'].upper()}"
                 + (f" · {k['ten_en'].upper()}" if k.get('ten_en') else '')),
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "tranhTen": k["ten"] + (f" · {k['ten_en']}" if k.get("ten_en") else ""),
        "de": "Con nhìn bức tranh rồi viết một đoạn tả bức tranh nhé.",
        "toiThieu": 2,
        "mauCau": [],
        "goiY": [],
        "vonTu": von,
        # MÃ NÚT cho bài viết — bé viết được đoạn tả tranh là chạm tới cả vốn từ
        # của bức tranh ấy. Nút chính là ô chữ ĐẦU TIÊN tra ra được.
        **nut_cua_bai_viet(von, KHO_NUT[0]),
        # Máy chấm đối chiếu với đây — bé viết được ý nào CÓ THẬT trong tranh thì
        # tính ý ấy. Không bày ra màn hình.
        "yTrongTranh": list(k["doan"]),
    }


def kich_ban_noi(k: dict, lop: int) -> dict:
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
    # Câu CÔ HỎI khi bé bí. Câu nào trùng với câu hỏi sau bài đọc thì mang theo
    # ĐÁP MẪU; câu nào không thì để trống — phòng nói tự nhận mọi câu trong đoạn
    # làm đáp đúng (`phongnoi.js`: `buoc.dapMau ? [buoc.dapMau] : [...moTa]`).
    dap_cua = {h["hoi"]: h["dap"] for h in k.get("hoi") or []}
    for g in k.get("goiY") or []:
        if g["hoi"] == "What can you see?":
            continue          # đã là bước `taTranh` mở đầu
        b = {"loai": "goiY", "en": g["hoi"],
             "vi": f"Con nhìn tranh rồi đáp nhé — {g['vi']}"}
        if g["hoi"] in dap_cua:
            b["dapMau"] = dap_cua[g["hoi"]]
        buoc.append(b)
    # XÂU CHUỖI: cả đoạn thành MỘT lượt nói. Đây là đích của cả buổi.
    buoc.append({
        "loai": "caDoan",
        "en": " ".join(k["doan"]),
        "vi": "Giỏi lắm! Giờ con nói cả đoạn cho cô nghe nhé.",
    })
    buoc.append({"loai": "ket"})
    return {
        # ⚠ GHIM CỨNG "TA3" Ở ĐÂY LÀ HỎNG CÂM. Kịch bản tranh của lớp 4 mang
        # mã lớp 3 nên phép thay `x["bai"] != kb["bai"]` không khớp bài nào —
        # nó NỐI THÊM thay vì THAY THẾ, và `kichban_noi.json` có 42 mục cho 21
        # bài. Không cổng nào bắt, chỉ đếm mới thấy.
        "bai": f"DL:{QUYEN[lop].upper()}.B{k['unit']:02d}",
        "ten": f"Tả tranh · {k['ten']}",
        "muc_tieu": f"Tả được bức tranh “{k['ten']}” thành một đoạn",
        "tinh_huong": f"Con và cô cùng nhìn một bức tranh: {k['ten'].lower()}.",
        "tranh": f"{DUONG_TRANH}/{k['id'].replace(':', '_').replace('.', '_')}.png",
        "moTaTranh": list(k["doan"]),
        "dang": "tranh",
        "tu": [x["tu"] for x in tu_trong_tranh(k, lop)
               if x["nghia"] and x["tu"].lower() not in KHONG_CHU][:10],
        "buoc": buoc,
        "tay": True,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3)
    p.add_argument("--thieu", help="ghi ra tệp những dòng chưa có clip")
    a = p.parse_args()
    KHO_NUT[0] = kho_nut(a.lop)
    q = QUYEN[a.lop]
    tm = GOC / f"web/public/content/{q}"

    # ⚠ NGUỒN ĐỔI 20-08-2026: `canh_lopN.json` thay `tranh_lopN.json`. Bản cũ khai
    # theo KỆ (`nhom` · `ke` · `bienSo`) nên đoạn văn buộc thành bảng liệt kê —
    # bác bác bỏ cả 42 bài. Bản mới khai theo CẢNH và mang sẵn `moTa` · `hoi` ·
    # `goiY` viết tay. Xem [[bai-ta-tranh-khong-hoi-thoai]].
    kho = json.loads((GOC / f"data/tienganh/canh_lop{a.lop}.json").read_text("utf8"))
    # Tên CẢNH của các unit — mồi cho câu hỏi "bức tranh này vẽ ở đâu".
    # ⚠ Lấy `canh` của bản chuẩn, KHÔNG lấy tên unit: tên unit là "Khởi động" ·
    # "Chào hỏi" — không phải NƠI CHỐN nào cả, nên bé loại được mà chẳng cần nhìn
    # tranh. Câu hỏi vẫn "chạy đúng", chỉ là không hỏi gì.
    ten_canh = []
    for l in range(1, a.lop + 1):
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{l}.json").read_text("utf8"))
        for u in cn["unit"]:
            c = str(u.get("canh") or "").split("·")[0].strip()
            if c and re.match(r"^(Ở|Trong|Bên|Tại)\b", c):
                ten_canh.append(c)
    ten_canh = list(dict.fromkeys(ten_canh))
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

        kb = kich_ban_noi(k, a.lop)
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
