"""KHUÔN ĐẦU RA CỦA BỐN WORKER (việc V12).

── MỌI WORKER TRẢ JSON THEO KHUÔN CỐ ĐỊNH, KHÔNG VĂN TỰ DO ──
Bản thiết kế chốt thế, và lý do thì sâu hơn chuyện gọn gàng: đầu ra của xưởng phải
RÓT ĐƯỢC vào `data/tienganh/chuan_lop{N}.json` rồi đi qua bộ sinh và 83 cổng hiện
có. Một đoạn văn tự do thì phải có người đọc rồi gõ lại — mà lúc đã gõ lại thì xưởng
chẳng tiết kiệm được gì.

Nên khuôn ở đây KHÔNG phải khuôn tôi tự đặt: nó là hình dạng mà bốn bộ sinh hiện có
ĐANG đọc. Soi theo nó thì một bản nháp qua được `soi_khuon` là bản nháp bộ sinh nhận
được, không phải "bản nháp trông đúng".

── BỐN LOẠI, VÀ CHÚNG ĐI VÀO BỐN CHỖ KHÁC NHAU ──
    tu         → `unit[].tu`            (chuan_lop{N}.json, bộ sinh bài)
    mau_cau    → `unit[].mau_cau`       (chuan_lop{N}.json, bộ sinh bài)
    kich_ban   → kichban_noi.json       (bộ sinh kịch bản nói)
    doc_hieu   → dochieu.json           (bộ sinh đọc hiểu)

⚠ `test_schema.py` soi lại khuôn này BẰNG DỮ LIỆU THẬT: nó lấy một unit có sẵn của
lớp 4 rồi bắt `soi_khuon` phải nói "qua". Khuôn lệch khỏi hình dạng thật là cổng đỏ
ngay, chứ không chờ tới lúc rót vào mới biết.
"""
from __future__ import annotations

import re

LOAI = ("tu", "mau_cau", "kich_ban", "doc_hieu")

#: Trần số mục một worker được đẻ ra một lượt.
#:
#: ⚠ `kich_ban` và `doc_hieu` XIN ĐÚNG MỘT MỤC, nên trần 2 — không phải 12. Trần
#: rộng ở đó đã che một chỗ hỏng thật: lời dặn xin "một kịch bản gồm 6 bước", mô hình
#: đọc `muc` thành danh sách BƯỚC rồi trả về SÁU kịch bản một-bước. Trần 12 nhận hết
#: sáu cái ấy như sáu mục hợp lệ, và chúng đi tiếp tới giám khảo. Trần 2 thì nó kêu.
TRAN = {"tu": 16, "mau_cau": 6, "kich_ban": 2, "doc_hieu": 2}

#: Trần ký tự từng trường. Chỗ nào bé ĐỌC hay NGHE thì trần chặt hơn.
TRAN_CHU = {"tu": 40, "nghia": 80, "ipa": 40, "cau": 160, "cong_thuc": 200,
            "dung_de": 160, "vi": 160, "ten": 120, "muc_tieu": 200,
            "tinh_huong": 240, "hoi": 200}


def _chu(x) -> str:
    return str(x if x is not None else "").strip()


def _soi_chu(d: dict, khoa: str, ly_do: list, *, buoc: bool = True) -> str:
    v = _chu(d.get(khoa))
    if not v:
        if buoc:
            ly_do.append(f'thiếu "{khoa}"')
        return ""
    tran = TRAN_CHU.get(khoa)
    if tran and len(v) > tran:
        ly_do.append(f'"{khoa}" dài quá {tran} ký tự')
    return v


def _soi_tu(m: dict, ly_do: list) -> None:
    tu = _soi_chu(m, "tu", ly_do)
    _soi_chu(m, "nghia", ly_do)
    # IPA không bắt buộc: dây chuyền âm tự dựng được, và bắt mô hình bịa IPA thì nó
    # bịa — một ký hiệu phiên âm sai thì không ai trong nhà phát hiện được.
    _soi_chu(m, "ipa", ly_do, buoc=False)
    if tu and not re.fullmatch(r"[A-Za-z][A-Za-z' -]*", tu):
        ly_do.append(f'"tu" có ký tự lạ: {tu!r}')
    vai = m.get("vai")
    if not isinstance(vai, list) or not vai or not all(isinstance(x, str) and x for x in vai):
        ly_do.append('"vai" phải là mảng chuỗi, không rỗng')
    # ⚠ KHÔNG SỐ trong `nghia`. Lời nghĩa đi vào thẻ từ và vào video, và một con số
    # ở đó thì bộ đọc đọc ra "bốn" giữa một câu tiếng Việt — cùng lý lẽ với
    # `dongHoSoAI` bên app.
    if re.search(r"[0-9]", _chu(m.get("nghia"))):
        ly_do.append('"nghia" có chữ số')


def _soi_mau_cau(m: dict, ly_do: list) -> None:
    _soi_chu(m, "vi_du", ly_do) if "vi_du" in m else _soi_chu(m, "cau", ly_do)
    ct = _soi_chu(m, "cong_thuc", ly_do)
    _soi_chu(m, "dung_de", ly_do)
    # Ô trống phải viết đúng khuôn `[Tên]` — bộ sinh tra ô theo đúng hình dạng ấy,
    # và một ô viết `(Country)` thì nó không thấy, rồi câu đi ra còn nguyên dấu ngoặc.
    for o in re.findall(r"[\[\(]\s*([^\]\)]+)\s*[\]\)]", ct):
        if f"[{o}]" not in ct:
            ly_do.append(f'ô trống phải viết [{o}], không dùng ngoặc tròn')
    if "o_thay" in m and not isinstance(m.get("o_thay"), list):
        ly_do.append('"o_thay" phải là mảng')


def _soi_kich_ban(m: dict, ly_do: list) -> None:
    _soi_chu(m, "ten", ly_do)
    _soi_chu(m, "muc_tieu", ly_do)
    _soi_chu(m, "tinh_huong", ly_do)
    buoc = m.get("buoc")
    if not isinstance(buoc, list) or not buoc:
        ly_do.append('"buoc" phải là mảng, không rỗng')
        return
    for i, b in enumerate(buoc, 1):
        if not isinstance(b, dict):
            ly_do.append(f"bước {i} không phải object")
            continue
        phu = []
        _soi_chu(b, "cau", phu)
        _soi_chu(b, "vi", phu)
        ly_do.extend(f"bước {i}: {x}" for x in phu)


def _soi_doc_hieu(m: dict, ly_do: list) -> None:
    doan = m.get("doan")
    if not isinstance(doan, list) or not doan:
        ly_do.append('"doan" phải là mảng câu, không rỗng')
    else:
        for i, c in enumerate(doan, 1):
            cau = c.get("cau") if isinstance(c, dict) else c
            if not _chu(cau):
                ly_do.append(f"câu {i} của đoạn rỗng")
    cau_hoi = m.get("cau")
    if not isinstance(cau_hoi, list) or not cau_hoi:
        ly_do.append('"cau" (câu hỏi) phải là mảng, không rỗng')
        return
    for i, q in enumerate(cau_hoi, 1):
        phu = []
        if not isinstance(q, dict):
            ly_do.append(f"câu hỏi {i} không phải object")
            continue
        _soi_chu(q, "hoi", phu)
        chon = q.get("chon")
        dung = _chu(q.get("dung"))
        if not isinstance(chon, list) or len(chon) < 2:
            phu.append("phải có ít nhất 2 phương án")
        elif dung and dung not in [_chu(x) for x in chon]:
            phu.append('"dung" không nằm trong "chon"')
        if not dung:
            phu.append('thiếu "dung"')
        # ⚠ MỘT ĐÁP ÁN ĐÚNG, không hai. Chỗ hỏng này đã bắt được thật 47 câu ở hai
        # đợt bài đọc — xem `mot-cau-hoi-mot-dap-an-dung`.
        if isinstance(chon, list):
            dem = [_chu(x) for x in chon].count(dung)
            if dung and dem > 1:
                phu.append(f'đáp án "{dung}" xuất hiện {dem} lần trong "chon"')
        ly_do.extend(f"câu hỏi {i}: {x}" for x in phu)


_SOI = {"tu": _soi_tu, "mau_cau": _soi_mau_cau,
        "kich_ban": _soi_kich_ban, "doc_hieu": _soi_doc_hieu}


def soi_khuon(loai: str, muc_ds) -> dict:
    """Soi đầu ra một worker. Trả `{qua: [...], bac: [{muc, ly_do}]}`.

    KHÔNG ném: một mục vỡ thì bỏ đúng mục ấy, chứ đừng vứt cả lượt gọi. Mô hình trả
    về sáu mục mà một mục thiếu `nghia` thì năm mục kia vẫn dùng được.
    """
    if loai not in LOAI:
        raise ValueError(f"loại lạ: {loai}")
    if not isinstance(muc_ds, list):
        return {"qua": [], "bac": [{"muc": muc_ds, "ly_do": ["không phải mảng"]}]}
    qua, bac = [], []
    for m in muc_ds[:TRAN[loai]]:
        if not isinstance(m, dict):
            bac.append({"muc": m, "ly_do": ["không phải object"]})
            continue
        ly_do: list[str] = []
        _SOI[loai](m, ly_do)
        (bac if ly_do else qua).append({"muc": m, "ly_do": ly_do} if ly_do else m)
    if len(muc_ds) > TRAN[loai]:
        bac.append({"muc": None,
                    "ly_do": [f"trả về {len(muc_ds)} mục, quá trần {TRAN[loai]} — "
                              "đã bỏ phần thừa"]})
    return {"qua": qua, "bac": bac}


def cau_tieng_anh(loai: str, muc: dict) -> dict:
    """Rút MỌI tiếng Anh của một mục ra, TÁCH THÀNH BA LOẠI để hàng rào soi đúng cách.

    ── VÌ SAO PHẢI TÁCH, VÀ CHUYỆN ĐÃ HỎNG THẬT ──
    Bản đầu trả về MỘT danh sách phẳng. Chạy thật trên lớp 4 unit 3 thì nó bác sạch
    cả ba mẫu câu và cả bài đọc, vì hai lý do mà cả hai đều là lỗi của phép rút, không
    phải lỗi của mô hình:

      1. CÔNG THỨC CÓ Ô TRỐNG, VÀ ĐÓ LÀ ĐỊNH NGHĨA CỦA NÓ.
         `I play [Noun] on Saturdays.` bị bác với lý do "chữ ngoài vốn: noun" —
         `chu_trong` tách `[Noun]` ra thành chữ `noun`. Nhưng một công thức KHÔNG có
         ô trống thì không còn là công thức.

      2. PHƯƠNG ÁN TRẮC NGHIỆM ĐƯỢC PHÉP TRÙNG GIỮA CÁC CÂU HỎI.
         `monday` nằm trong phương án của câu 1 và câu 3, và phép soi trùng ở mức BỘ
         đếm nó là "câu lặp". Phép soi ấy sinh ra để bắt BỐN CÂU HỎI y hệt nhau
         (việc V9) — không phải để bắt hai câu hỏi dùng chung một phương án nhiễu.

    Nên ba loại, ba cách soi:
        cau        câu HOÀN CHỈNH — soi vốn · soi lành lặn · SOI TRÙNG
        tu_le      chữ lẻ và phương án — soi vốn, KHÔNG soi trùng, không soi lành lặn
        cong_thuc  công thức — soi vốn SAU KHI BỎ ô trống, không soi trùng
    """
    cau: list[str] = []
    tu_le: list[str] = []
    cong_thuc: list[str] = []

    if loai == "tu":
        # Một mục từ vựng là CHỮ LẺ, không phải câu: "dog" không lành lặn theo nghĩa
        # câu (không có dấu chấm, không có động từ) và nó không cần phải thế.
        tu_le += [_chu(muc.get("tu"))]
        tu_le += [_chu(muc.get(d)) for d in ("so_it", "so_nhieu", "dang_ing", "dang_qk")]
    elif loai == "mau_cau":
        cau.append(_chu(muc.get("vi_du") or muc.get("cau")))
        cong_thuc.append(_chu(muc.get("cong_thuc")))
    elif loai == "kich_ban":
        # Bước kịch bản PHẢI là câu đã điền — ô trống ở đây là lỗi thật, vì cô đọc
        # nguyên văn câu ấy cho bé nghe.
        cau += [_chu(b.get("cau")) for b in (muc.get("buoc") or []) if isinstance(b, dict)]
    elif loai == "doc_hieu":
        for c in muc.get("doan") or []:
            cau.append(_chu(c.get("cau") if isinstance(c, dict) else c))
        for q in muc.get("cau") or []:
            if not isinstance(q, dict):
                continue
            tu_le += [_chu(x) for x in (q.get("chon") or [])]
            tu_le.append(_chu(q.get("dung")))

    return {
        "cau": [x for x in cau if x],
        "tu_le": [x for x in tu_le if x],
        "cong_thuc": [x for x in cong_thuc if x],
    }


#: Ô trống của công thức: `[Noun]` · `[Country]` · `[Verb-ing]`…
import re as _re  # noqa: E402  (đặt cạnh chỗ dùng để người đọc thấy ngay)
O_TRONG = _re.compile(r"\[[^\]]*\]")


def bo_o_trong(s: str) -> str:
    """Bỏ ô trống khỏi công thức trước khi soi vốn từ. Xem `cau_tieng_anh`."""
    return O_TRONG.sub(" ", str(s or ""))
