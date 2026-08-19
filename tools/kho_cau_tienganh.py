#!/usr/bin/env python3
"""KHO CÂU TÍCH LUỸ — mọi câu tiếng Anh bé ĐÃ HỌC, từ lớp 1 tới đúng bài đang xét.

    from kho_cau_tienganh import cau_tich_luy, tach_doi, khop_khung

══ VÌ SAO CÓ TỆP NÀY ══ (bác chốt 19-08-2026)

Bác đọc bài đọc hiểu và bài viết rồi bảo:

    "sao nhiều câu lặp lại quá đi kiểu như Hello, I'm ben .... Bài đọc bạn nên dùng
     vốn câu tích luỹ từ lớp 1 đến bài đó của lớp 3 chứ không nhất thiết là trong
     bài đó của lớp 3. Bài viết cũng vậy."

Đúng, và con số nói thẳng ra chỗ hỏng. Tính tới unit 5 của lớp 3:

    vốn câu bé ĐÃ HỌC        132 câu   (lớp 1: 64 · lớp 2: 32 · lớp 3 tới U5: 36)
    hai bộ sinh đang dùng      8 câu   (đúng `canonicalExamples` của mỗi unit)

Tám câu mà phải rải ra một đoạn đọc 4–6 dòng thì không còn đường nào khác ngoài
lặp — và đó chính là cái bác nhìn thấy. Bốn ví dụ của unit 1 chỉ khác nhau ở cái
tên, nên đoạn nào cũng "Hello. I'm Ben. / Hello. I'm Lucy."

Mở ra cả kho thì cùng lúc chữa được ba thứ: hết lặp, đoạn dài hơn mà vẫn tự nhiên,
và bé được ÔN lại câu cũ ngay trong lúc đọc bài mới.

══ VÌ SAO MỘT TỆP DÙNG CHUNG, KHÔNG CHÉP HAI BẢN ══

`sinh_dochieu_tienganh.py` và `sinh_vietbai_tienganh.py` cùng cần đúng một thứ:
"những câu bé đã học tính tới đây". Chép luật sang hai nơi thì sớm muộn lệch, mà
lệch ở đây nghĩa là bài đọc và bài viết của cùng một unit nói hai thứ tiếng khác
nhau — không cổng nào bắt được, vì mỗi bên tự nó vẫn đúng.

Cùng lý do `web/tools/noidung_version.mjs` là một tệp dùng chung cho vite và cổng.

══ TÍCH LUỸ TỚI ĐÂU ══

Tới ĐÚNG bài đang xét, không hơn:
  · trọn lớp 1 và lớp 2 (bé học xong mới lên lớp 3);
  · lớp 3 thì tới unit ấy, kể cả unit ấy.

Lấy quá thì bé gặp câu chưa ai dạy — đúng cái `_kho_tu` sinh ra để chặn. Nên mỗi
câu vẫn bị soi lại theo TÚI TỪ đã học trước khi được nhận.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}


def chu_trong(s: str) -> list[str]:
    return re.findall(r"[a-z']+", str(s or "").lower())


def tach_doi(s: str) -> tuple[str | None, str]:
    """`"What's your hobby? - It's cooking."` → `("What's your hobby?", "It's cooking.")`.

    Không phải cặp thì trả `(None, cả câu)`.

    ⚠ BỐN NƠI PHẢI CẮT GIỐNG NHAU: tệp này, `cauSachCuaBai` (phongnoi.js),
    `sinh_kichban_noi.py`, và cổng `tienganh_dochieu`. Lệch một chỗ thì câu ở bên
    này rơi ra ngoài túi hợp lệ của bên kia, và không gì kêu cả.
    """
    phan = [x.strip() for x in str(s or "").split(" - ")]
    if len(phan) == 2 and all(phan):
        return phan[0], phan[1]
    return None, str(s or "").strip()


def tach_lua_chon(s: str) -> list[str]:
    """`"Yes, it is. / No, it isn't."` → hai câu.

    Mẫu YES/NO viết cả hai lối đáp trong một chuỗi. Không tách thì bé đọc liền một
    hơi hai câu trái ngược nhau — "vâng đúng rồi không phải đâu".
    """
    if "/" not in str(s or ""):
        return [str(s or "").strip()]
    ra = [x.strip() for x in re.split(r"\s*/\s*", str(s))]
    if all(re.match(r"^[A-Z].*[.?!]$", x) for x in ra if x):
        return [x for x in ra if x]
    return [str(s).strip()]


def khop_khung(cong_thuc: str, cau: str) -> bool:
    """Câu này có phải một cách điền của công thức kia không."""
    if not cong_thuc:
        return False
    khung = re.sub(r"\s*\+\s*", " ", cong_thuc)
    mau = re.escape(khung).replace(r"\[", "[").replace(r"\]", "]")
    mau = re.sub(r"\[[^\]]+\]", "(.+?)", mau)
    return re.fullmatch(mau, str(cau or "").strip()) is not None


def sach_se(cau: str) -> bool:
    """Câu có sạch để đưa cho bé đọc hay chép không.

    Bản đồ lớp 2 khai `"Yes,[Pronoun] is."` — THIẾU dấu cách sau dấu phẩy
    (data/ban_do_tieng_anh.json). Bỏ qua chứ KHÔNG tự chèn: sửa hộ ở đây thì câu
    trong bài đọc khác câu trên màn bài học, mà chỗ sai thật vẫn nằm nguyên trong
    bản đồ.
    """
    return bool(cau) and not re.search(r"[,;](?=\S)", cau) and "/" not in cau


# ── CÂU XÃ GIAO ── (bác chốt 19-08-2026)
#
# "Cả một chương bạn toàn có nói về mấy câu chào hỏi. […] Căn bản đoạn văn nó phải
# có ý nghĩa một chút thay vì chỉ chào hỏi linh tinh. Phần chào hỏi, luyện tập nên
# để ở phần Luyện nói. Đọc nên là một bài đọc ngắn có thông tin."
#
# Đúng. Bài đọc mở đầu bằng hai dòng chào ở MỌI bài, mà đoạn chỉ dài 4–7 dòng —
# nghĩa là một phần ba tới một nửa bài đọc không mang một mẩu thông tin nào. Bé đọc
# xong không biết thêm điều gì về ai.
#
# Chào hỏi vẫn cần, nhưng đúng chỗ của nó: PHÒNG LUYỆN NÓI (bước `chao`) và BÀI
# VIẾT (nhóm "Mở đầu" — một đoạn văn tự giới thiệu thì phải có lời chào). Bài đọc
# thì bỏ hẳn.
XA_GIAO = re.compile(
    r"^(Hello|Hi|Bye|Goodbye|How are you|Fine, thank you|Nice to meet you)\b", re.I)


def la_xa_giao(m: dict) -> bool:
    """Mẫu câu này chỉ để chào hỏi, không mang thông tin gì."""
    return bool(XA_GIAO.match(m.get("hoi") or m.get("dap") or ""))


def bai_cua(lop: int) -> list[dict]:
    tm = GOC / f"web/public/content/{QUYEN[lop]}"
    return [json.loads(p.read_text("utf8"))
            for p in sorted(tm.glob(f"DL_{QUYEN[lop].upper()}_B*.json"))]


def cau_tich_luy(lop: int, den_unit: int, kho_tu: set[str],
                 unit_dich: set[int] | None = None) -> list[dict]:
    """Mọi MẪU CÂU bé đã học, từ lớp 1 tới `den_unit` của lớp `lop`.

    Trả danh sách mục, mỗi mục là MỘT mẫu câu:

        {"cau", "hoi", "dap", "khung", "dungDe", "vidu": [...],
         "lop", "unit", "moi"}

    `moi=True` nghĩa là mẫu ấy thuộc bài ĐANG HỌC (`unit_dich`) — bên gọi dùng nó
    để xếp câu mới lên trước, câu ôn lại xuống sau. Bài đọc mà toàn câu cũ thì nó
    không còn là bài đọc CỦA UNIT NÀY nữa.

    `vidu` là các cách điền khác của cùng mẫu, đã lọc theo túi từ — chỗ để bên gọi
    lấy thêm câu mà không phải lặp lại đúng một câu.

    Thứ tự: đúng thứ tự học (lớp 1 → lớp 3, unit nhỏ → lớn).
    """
    dich = unit_dich or set()
    ra: list[dict] = []
    for l in range(1, lop + 1):
        for b in bai_cua(l):
            if l == lop and b["so"] > den_unit:
                continue
            kc = b["knowledgeCore"]
            vi_du = [str(x) for x in (kc.get("canonicalExamples") or [])]
            mau = kc.get("mauCauDs") or ([kc["mauCau"]] if kc.get("mauCau") else [])
            for m in mau:
                hoi, dap = tach_doi(m.get("cau"))
                khung = tach_doi(m.get("congThuc") or "")[1]
                # Các cách điền khác của CHÍNH mẫu này, đã soi theo túi từ.
                cach = []
                for x in vi_du:
                    _, nua = tach_doi(x)
                    if khung and not khop_khung(khung, nua):
                        continue
                    for y in tach_lua_chon(nua):
                        if (y and sach_se(y) and y not in cach
                                and all(w in kho_tu for w in chu_trong(y))):
                            cach.append(y)
                dap_sach = [y for y in tach_lua_chon(dap)
                            if sach_se(y) and all(w in kho_tu for w in chu_trong(y))]
                if not dap_sach and not cach:
                    continue
                if hoi and not all(w in kho_tu for w in chu_trong(hoi)):
                    continue
                ra.append({
                    "cau": m.get("cau"),
                    "hoi": hoi,
                    "dap": dap_sach[0] if dap_sach else cach[0],
                    "khung": khung,
                    "dungDe": str(m.get("dungDe") or "").strip().rstrip("."),
                    "vidu": list(dict.fromkeys((dap_sach or []) + cach)),
                    "lop": l,
                    "unit": b["so"],
                    "chuong": b.get("chuong"),
                    "moi": (l == lop and b["so"] in dich),
                })
                ra[-1]["xaGiao"] = la_xa_giao(ra[-1])
    return ra


def hinh_cua_tu(lop: int, den_unit: int) -> dict:
    """Tra `tu → {hinh, ve}` trong mọi bài bé đã học tới đây.

    Đọc từ chính `bai.hinhTu` — cùng nguồn với thẻ từ, thanh việc và video. Chỗ nào
    tự dựng lại một bảng hình riêng là chỗ ấy sẽ lệch.

    ⚠ Ở ĐÂY chứ không ở `tranh_tienganh.py`: bộ soạn tranh cũng cần nó, mà bộ soạn
    chạy bằng python hệ thống — `tranh_tienganh` kéo theo Pillow và cairosvg, chỉ có
    trong venv. Hàm tra dữ liệu thì để ở module không phụ thuộc gì.
    """
    ra = {}
    for l in range(1, lop + 1):
        tm = GOC / f"web/public/content/{QUYEN[l]}"
        for p in sorted(tm.glob(f"DL_{QUYEN[l].upper()}_B*.json")):
            b = json.loads(p.read_text("utf8"))
            if l == lop and b["so"] > den_unit:
                continue
            for h in b.get("hinhTu") or []:
                if h.get("hinh") or h.get("ve"):
                    ra.setdefault(h["tu"], {"hinh": h.get("hinh"), "ve": h.get("ve")})
    return ra


def kho_chu(lop: int, den_unit: int) -> set[str]:
    """Túi TỪ bé đã học, từ lớp 1 tới `den_unit` của lớp `lop`.

    Cắt theo UNIT chứ không theo chương: chính xác hơn một nấc, và đó là nấc quyết
    định ở bài đọc theo unit — bé vừa học xong unit 5 thì chưa biết từ của unit 6
    dù hai unit cùng một chương.

    Gom cả `mau_cau` và mấy nhóm nền (`so_dem` · `mau` · `ten`), vì câu của sách
    dùng chúng mà bảng từ vựng thì không liệt kê.
    """
    kho: set[str] = set()

    def nap(s):
        kho.update(chu_trong(s))

    for l in range(1, lop + 1):
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{l}.json").read_text("utf8"))
        for u in cn["unit"]:
            if l == lop and u["so"] > den_unit:
                continue
            for x in u["tu"]:
                for k in ("tu", "so_it", "so_nhieu", "dang_ing"):
                    nap(x.get(k))
            for m in u["mau_cau"]:
                nap(re.sub(r"\[[^\]]*\]", " ", str(m.get("cong_thuc") or "")))
                nap(m.get("vi_du"))
        for nhom in ("so_dem", "mau", "ten"):
            for m in ((cn.get("them") or {}).get(nhom) or {}).get("muc") or []:
                nap(m if isinstance(m, str) else m.get("word"))
    return kho
