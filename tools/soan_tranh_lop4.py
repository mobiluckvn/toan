#!/usr/bin/env python3
"""SOẠN BẢN KHAI TRANH cho cả quyển lớp 4 — mỗi unit một bức.

    python3 tools/soan_tranh_lop4.py            # in ra để xem
    python3 tools/soan_tranh_lop4.py --ghi      # ghi vào data/tienganh/tranh_lop4.json

Bác chốt 19-08-2026: "Bạn apply cách làm này cho tất cả các bài nhé."

── VÌ SAO SINH CHỨ KHÔNG GÕ TAY 20 BỨC ──
Mỗi bức cần: vật vẽ được · đoạn mô tả · câu hỏi tiếng Anh · mồi nhử · câu hỏi gợi ý
cho phòng nói. Gõ tay 20 bức là gõ 20 lần cùng một luật, và sớm muộn lệch — quên
một chữ trong bảng từ, hay dùng một khuôn unit ấy chưa học, thì không có gì báo
ngoài cổng.

Sinh ra từ chính vốn của unit thì cả năm thứ ấy cùng một nguồn, và cổng soi lại
được. Bức nào ra kỳ thì SỬA TAY trong `tranh_lop4.json` rồi đặt cờ `tay: true` —
lần soạn sau không đè lên.

── LUẬT SOẠN ──
1. VẬT là từ MỚI của unit, có hình, và ĐẶT ĐƯỢC SAU "a": loại từ không đếm được,
   loại hoạt động, loại nơi chốn. Thiếu thì mượn thêm của unit trước.
2. ĐOẠN: mỗi vật một câu, xoay vòng bốn khuôn KỂ của sách —
   `This is a X.` · `I can see a X.` · `That's a X.` · `There's a X.`
   Unit dạy HOẠT ĐỘNG thì dùng `She's Xing.` / `He's Xing.` (khuôn lớp 1 unit 11).
3. CÂU HỎI bằng tiếng Anh, chỉ dùng khuôn ĐÃ HỌC tới unit ấy.
4. MỒI là câu của kho mà KHÔNG tả bức tranh này.

⚠ MẠO TỪ. Khuôn của sách ghi "a", nhưng "a elephant" là sai. Đổi sang "an" trước
nguyên âm — đó là sửa ngữ pháp bắt buộc, không phải bịa câu; `sinh_bai_tienganh.py`
cũng làm đúng thế ở `_chon_mao_tu`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "tools"))
from kho_cau_tienganh import kho_chu, chu_trong  # noqa: E402
from kho_cau_tienganh import hinh_cua_tu  # noqa: E402

# Vai ĐẶT ĐƯỢC sau "a" và vẽ ra hình được.
VAI_VAT = {"convat", "dochoi", "dodac", "dodung", "bophan", "giadinh", "nghe",
           "dt", "thucan", "noichon"}
# Vai KHÔNG đặt sau "a": nơi chốn (a school nghe được nhưng tranh vẽ cả cảnh),
# màu, số, hoạt động, đồ uống (không đếm được).
# ⚠ `trochoi` (badminton · chess · football) KHÔNG đặt được sau "a": "a badminton"
# sai hẳn. Unit 10 vì thế phải mượn vật của unit khác cùng chương.
VAI_BO = {"mau", "so", "sothich", "viec", "viecthu", "douong", "trochoi",
          "chao", "hoi", "daitu", "ten", "sohuu", "tinhtu", "chidinh", "xungho",
          "dongtu", "soluong", "vitri", "nghe_",
          # ⚠ VAI MỚI CỦA LỚP 4 — bản chép từ lớp 3 không biết chúng, nên
          # `sunny` · `maths` · `today` · `left` lọt qua phép "đặt được sau a"
          # và đẻ ra "This is a sunny."
          "thoitiet", "monhoc", "thang", "thu", "thoigian", "mua",
          "huong", "quocgia", "tien", "sukien"}
# Hoạt động — dùng khuôn "She's …ing."
VAI_VIEC = {"sothich", "viec", "viecthu"}

KHUON_KE = ["This is {a}.", "I can see {a}.", "That's {a}.", "There's {a}."]
# ⚠ NGƯỜI THÂN ĐI VỚI "my", KHÔNG ĐI VỚI "a". "This is a father." sai hẳn — tiếng
# Anh nói "This is my father." Khuôn `This is my + [Noun].` là của lớp 1 unit 3.
KHUON_NHA = ["This is my {t}.", "That's my {t}.", "This is my {t}.", "That's my {t}."]
VAI_NHA = {"giadinh"}
# ⚠ LỚP 4 CÓ BỐN KHUÔN, KHÔNG PHẢI HAI.
# Lớp 3 chỉ có `She's …` / `He's …`, nên quá bốn hoạt động là ba dòng cùng một
# khuôn và cổng "không quá 2 dòng cùng khuôn" đỏ ngay — đó là lý do `BOT_VIEC = 4`
# ở lớp 3, KHÔNG phải vì bốn là con số đẹp.
#
# Bác chốt 20-08: đọc · nói · viết lớp 4 phải DÀI HƠN. Muốn nhiều hoạt động hơn
# thì phải THÊM KHUÔN, không phải nới số. Lớp 4 dạy sẵn hai khuôn nữa:
#     They're …ing.   (Starter · U20 — "What are they doing?")
# Ba khuôn × 2 dòng = tối đa 6 hoạt động mà vẫn qua cổng.
#
# ⚠ KHÔNG thêm khuôn `I can + [Ability]` dù lớp 4 có dạy: nó đòi ĐỘNG TỪ NGUYÊN
# THỂ (`I can swim.`) mà kho tranh chỉ giữ dạng `-ing`. Suy ngược `swimming` →
# `swim` bằng cách cắt đuôi là chỗ đẻ ra `dancing` → `danc`.
KHUON_VIEC = ["She's {ing}.", "He's {ing}.", "They're {ing}."]
# Nhiều nhất BỐN hoạt động trong một bức. Không phải con số cho đẹp: `KHUON_VIEC`
# chỉ có hai khuôn, xoay vòng She's/He's, nên năm hoạt động là ba dòng cùng một
# khuôn — và cổng "không quá 2 dòng cùng khuôn" đỏ ngay. Bốn thì vừa đúng hai/hai.
BOT_VIEC = 6

# Không đếm được — "a rice" sai. Sách không khai cờ này nên liệt kê ở đây, và
# `chuan_tienganh.py` cũng chưa có chỗ nào khai nó.
# ── DÀI HƠN LỚP 3 ── (bác chốt 20-08-2026)
# Lớp 3: tối đa 5 vật, 2 kệ, đoạn 4–5 câu.
# Lớp 4: 7 vật, 3 kệ, đoạn 6–7 câu (bức dạy màu thì 14 câu).
# Ba con số này đi VỚI NHAU: nới số vật mà không thêm kệ thì vật rơi ra ngoài, và
# `assert` ở cuối `soan()` bắt ngay.
TOI_DA_VAT = 7
SO_KE = 3

KHONG_DEM = {"rice", "bread", "meat", "milk", "water", "juice", "chicken", "fish",
             "popcorn", "pasta", "sand", "water", "hair", "homework"}


# ══════════════════════════════════════════════════════════════════════════════
# VẬT ƯU TIÊN — chỗ khai TAY cái mà máy không suy được: bức này nên vẽ những gì.
#
# Máy chọn vật theo luật (từ của unit → cùng chương → lớp 1·2) và luật ấy hợp lệ
# nhưng VÔ VỊ ở sáu bức: unit 7 "Lời dặn trong lớp" toàn động từ nên máy mượn của
# unit liền trước, ra "school · library · playground · classroom · gym" — năm chỗ
# khác nhau trong một bức tên là "trong lớp".
#
# Nên: người khai vật, MÁY VẪN SOI LUẬT — vật phải đã học tới unit ấy, phải có
# hình, phải đặt được sau "a". Khai một từ chưa học thì nó bị loại và bức tự bù,
# không có chuyện lọt ra bản chạy.
#
#   vat   danh sách vật, theo thứ tự muốn vẽ
#   chinh vật CHỦ THỂ của bức — vẽ to, đứng một mình kệ trên, và câu đầu tả nó;
#         mấy vật còn lại là bộ phận/đồ đi kèm nên đều dùng "I can see …"
#   mau   bức dạy MÀU: mỗi vật kèm một câu "It's + [Colour]." ngay sau
UU_TIEN = {
    # ⚠ KHOÁ LÀ SỐ BÀI (0–20) SAU KHI ĐÃ BỎ BỐN BÀI ÔN TẬP, không phải mã unit của
    # bản đồ. Chép nguyên bảng của lớp 3 sang thì cảnh lớp 3 rơi vào unit lớp 4 —
    # bức "Tiệc sinh nhật" hiện ra mắt mũi mồm. Đã dính, nên xoá sạch rồi soạn lại.
    #
    # Bác chốt 20-08: lớp 4 phải DÀI HƠN lớp 3 → mỗi cảnh nhắm 6–7 vật, không phải 5.
    0:  {"vat": ["friend", "girl", "ball", "kite", "bike", "hat", "cat"]},
    1:  {"vat": ["friend", "girl", "brother", "sister", "mother", "father", "cake"]},
    2:  {"vat": ["bed", "cup", "egg", "bag", "school", "door", "window"]},
    3:  {"vat": ["school", "library", "playground", "gym", "bike", "ball", "book"]},
    # `grapes` là số nhiều nên phép soi loại — "a grapes" sai. Thay bằng apple.
    4:  {"vat": ["cake", "apple", "cup", "box", "table", "kite", "ball"],
        "chinh": "cake"},
    6:  {"vat": ["school", "playground", "garden", "building", "gym", "library",
                 "classroom"]},
    7:  {"vat": ["book", "pen", "pencil", "notebook", "eraser", "desk", "bag"]},
    8:  {"vat": ["book", "ruler", "pencil", "notebook", "eraser", "quiz", "bell"]},
    9:  {"vat": ["ball", "basketball", "volleyball", "football", "kite", "bike",
                 "box"]},
    10: {"vat": ["beach", "campsite", "zoo", "tent", "kite", "bike", "box"]},
    11: {"vat": ["house", "door", "window", "table", "chair", "bed", "lamp"]},
    # doctor · nurse · gardener nay có hình VẼ TAY (chân dung nửa người mặc
    # đồng phục) nên đưa lại vào bức. Trước đó chúng ra khuôn mặt trơn.
    12: {"vat": ["farmer", "doctor", "nurse", "teacher", "policeman", "worker", "gardener"]},
    13: {"vat": ["face", "eye", "nose", "hand", "ear", "mouth", "head"],
        "chinh": "face"},
    14: {"vat": ["bed", "teapot", "cup", "blanket", "lamp", "chair", "window"]},
    15: {"vat": ["cinema", "gym", "table", "book", "ball", "cake", "cup"]},
    # ⚠ KHÔNG vẽ tính từ thời tiết (sunny · rainy · windy · cloudy): chúng không
    # đặt được sau "a", và một bức không thể vừa nắng vừa mưa vừa gió. Unit vẫn
    # dạy thời tiết qua CÂU; tranh vẽ cảnh ngoài trời để tả.
    16: {"vat": ["kite", "tent", "table", "ball", "bike", "box", "car"]},
    17: {"vat": ["road", "bookshop", "bakery", "supermarket", "car", "bus",
                 "bike"]},
    18: {"vat": ["bookshop", "bakery", "skirt", "pen", "bag", "cake", "cup"]},
    19: {"vat": ["crocodile", "giraffe", "hippo", "lion", "peacock", "bird",
                 "elephant"]},
    20: {"vat": ["tent", "campsite", "lake", "river", "beach", "sail", "bird"]},
}

# Màu của vật — CHỈ những emoji một màu, gọi tên không cãi được. Đừng thêm bừa:
# "cake 🍰" trắng hay hồng hay nâu, ba người nhìn ra ba màu.
MAU_CUA = {"apple": "red", "leaf": "green", "box": "brown", "square": "blue",
           "sun": "yellow"}


def mao_tu(tu: str) -> str:
    return ("an " if tu[:1].lower() in "aeiou" else "a ") + tu


def bai_lop4() -> list[dict]:
    tm = GOC / "web/public/content/ta4"
    return [json.loads(p.read_text("utf8")) for p in sorted(tm.glob("DL_TA4_B*.json"))]


def bai_lop123() -> list[dict]:
    """Bài lớp 1·2 — chỗ mượn vật khi unit lớp 4 không có gì vẽ được.

    Chương 1 của lớp 4 dạy chào hỏi · tên · bạn bè: bốn unit liền không có lấy một
    danh từ vẽ ra tranh được. Không mượn thì bốn bức ấy trống trơn.
    """
    ra = []
    for q in ("ta1", "ta2", "ta3"):
        tm = GOC / f"web/public/content/{q}"
        ra += [json.loads(p.read_text("utf8"))
               for p in sorted(tm.glob(f"DL_{q.upper()}_B*.json"))]
    return ra


def vat_cua(b: dict, chuan_tu: dict, truoc: list[dict],
            chuan_tu12: dict | None = None, du_phong: list[dict] | None = None) -> list[dict]:
    """Vật cho bức tranh: từ MỚI của unit, có hình, đặt được sau "a"."""
    hinh = {h["tu"]: h for h in (b.get("hinhTu") or [])}

    def duoc(t: str) -> bool:
        c = chuan_tu.get(t) or {}
        vai = set(c.get("vai") or [])
        if not (hinh.get(t, {}).get("hinh") or hinh.get(t, {}).get("ve")):
            return False
        if t.lower() in KHONG_DEM or " " in t and not c.get("dang_ing"):
            return False
        return bool(vai & VAI_VAT) and not (vai & VAI_BO)

    ra = [t["tu"] for t in b["knowledgeCore"]["vocabulary"] if duoc(t["tu"])][:5]
    # Thiếu thì mượn của unit trước — bức tranh vẫn phải đủ vật để tả.
    if len(ra) < 3:
        # ⚠ CHỈ MƯỢN CỦA UNIT CÙNG CHƯƠNG. Mượn bừa thì ra "bean · bed · egg · desk"
        # — cái giường lạc vào bàn ăn. Cùng chương là cùng chủ đề sách đã gom sẵn.
        for x in reversed([y for y in truoc if y["chuong"] == b["chuong"]] or truoc):
            hx = {h["tu"]: h for h in (x.get("hinhTu") or [])}
            for t in x["knowledgeCore"]["vocabulary"]:
                if len(ra) >= 4:
                    break
                tu = t["tu"]
                c = chuan_tu.get(tu) or {}
                vai = set(c.get("vai") or [])
                if (tu not in ra and (hx.get(tu, {}).get("hinh") or hx.get(tu, {}).get("ve"))
                        and tu.lower() not in KHONG_DEM and " " not in tu
                        and vai & VAI_VAT and not (vai & VAI_BO)):
                    ra.append(tu)
            if len(ra) >= 4:
                break
    # Vẫn thiếu thì mượn lớp 1·2 — bé học rồi, và bức tranh phải có gì để tả.
    if len(ra) < 3 and du_phong:
        ct = {**(chuan_tu12 or {}), **chuan_tu}
        # XOAY theo số unit: không xoay thì unit 1 và unit 2 mượn đúng bốn vật đầu
        # danh sách và ra HAI BỨC GIỐNG HỆT NHAU.
        n = b["so"] % max(1, len(du_phong))
        du_phong = du_phong[n:] + du_phong[:n]
        for x in du_phong:
            hx = {h["tu"]: h for h in (x.get("hinhTu") or [])}
            for t in x["knowledgeCore"]["vocabulary"]:
                if len(ra) >= 4:
                    break
                tu = t["tu"]
                vai = set((ct.get(tu) or {}).get("vai") or [])
                if (tu not in ra and (hx.get(tu, {}).get("hinh") or hx.get(tu, {}).get("ve"))
                        and tu.lower() not in KHONG_DEM and " " not in tu
                        and vai & VAI_VAT and not (vai & VAI_BO)):
                    ra.append(tu)
            if len(ra) >= 4:
                break
    return ra


# Emoji NÀO là "một người đang làm gì đó". Chỉ những mã này mới được vào tranh
# dưới khuôn "She's …ing." — xem `la_nguoi` ngay dưới để biết vì sao.
NGUOI_MA = [
    (0x1F466, 0x1F469),   # boy · girl · man · woman
    (0x1F46B, 0x1F478),   # cặp đôi · người đi bộ · cảnh sát · cô dâu…
    (0x1F481, 0x1F483),   # chỉ đường · gội đầu · nhảy 💃
    (0x1F486, 0x1F487),   # massage · cắt tóc
    (0x1F574, 0x1F575),   # người mặc vest · thám tử
    (0x1F57A, 0x1F57A),   # nam nhảy
    (0x1F645, 0x1F64F),   # khoanh tay · cúi chào · giơ tay…
    (0x1F3C3, 0x1F3CC),   # chạy 🏃 · lướt · bơi · nâng tạ · chơi gôn
    (0x1F6B4, 0x1F6B6),   # đạp xe 🚴 · xe đạp địa hình · đi bộ
    (0x1F6CC, 0x1F6CC),   # nằm
    (0x1F930, 0x1F939),   # bế bé · nhún vai · làm xiếc…
    (0x1F93C, 0x1F93E),   # vật · bóng nước · bóng ném
    (0x1F9CD, 0x1F9CF),   # đứng · quỳ · người khiếm thính
    (0x1F9D1, 0x1F9DF),   # người 🧑 (kể cả 🧑‍🍳) · trẻ · leo núi 🧗 · ngồi thiền
]


HINH_VE = json.loads(
    (GOC / "web/src/mon/tienganh/lib/hinh_ve.json").read_text("utf8"))["hinh"]


def la_nguoi(h: dict | None) -> bool:
    """Hình của từ này có VẼ MỘT NGƯỜI không?

    ⚠ Đây là chỗ đã lên bản thật rồi mới lộ. Bức "Ở vườn thú" viết *"He's
    counting."* mà trên tranh là cái bàn phím số 🔢; unit 18 viết *"She's
    reading."* mà tranh là quyển sách 📖 — bé nhìn quyển sách thì bé nói "a book",
    không ai nói được "She's reading" từ một quyển sách nằm trên kệ.

    Phép kiểm cũ chỉ hỏi "từ này CÓ hình không". Có hình, nhưng hình là ĐỒ VẬT.
    Nay hỏi thêm: hình ấy có người không. Không có người thì hoạt động ấy ở lại
    thẻ từ và video, không vào tranh.

    Cố tình để danh sách HẸP: đoán sai theo hướng hẹp thì mất một hoạt động (tranh
    tự bù bằng đồ vật), đoán sai theo hướng rộng thì bé lại đứng nhìn quyển sách.

    HÌNH VẼ TAY thì không đoán được bằng mã — hỏi thẳng cờ `nguoi` khai trong
    `hinh_ve.json`. Một nguồn cho cả ba bên (bộ soạn · màn hình · cổng).
    """
    if (h or {}).get("ve"):
        return bool(HINH_VE.get(h["ve"], {}).get("nguoi"))
    for ch in (h or {}).get("hinh") or "":
        m = ord(ch)
        if any(a <= m <= b for a, b in NGUOI_MA):
            return True
    return False


def viec_cua(b: dict, chuan_tu: dict) -> list[str]:
    """Hoạt động của unit — từ có `dang_ing`, để dùng khuôn "She's …ing.".

    ⚠ PHẢI CÓ HÌNH. Bỏ sót phép kiểm này thì bộ dựng tranh dừng hẳn giữa chừng ở
    "không có hình cho swinging" — và nó dừng ĐÚNG, vì vẽ một ô trống rồi bảo bé tả
    thì bé không có gì để tả.

    ⚠ VÀ HÌNH ẤY PHẢI CÓ NGƯỜI — xem `la_nguoi`.
    """
    hinh = {h["tu"]: h for h in (b.get("hinhTu") or [])}
    ra = []
    for t in b["knowledgeCore"]["vocabulary"]:
        c = chuan_tu.get(t["tu"]) or {}
        vai = set(c.get("vai") or [])
        if vai & VAI_VIEC:
            ing = c.get("dang_ing") or (t["tu"] if t["tu"].endswith("ing") else None)
            h = hinh.get(ing) or hinh.get(t["tu"]) or {}
            if ing and " " not in ing and la_nguoi(h):
                ra.append(ing)
    return ra[:4]



def so_nhieu_cua(tu: str, chuan_tu: dict, ct12: dict, kho: set | None = None) -> str | None:
    """Dạng số nhiều của từ — CHỈ khi bé đã học tới đây.

    ⚠ `chuan_lop4.json` khai `cat → cats` ở unit 16. Tra thẳng vào đó khi soạn tranh
    cho unit 1 thì ra câu hỏi "How many cats can you see?" — mà "cats" là chữ bé
    chưa gặp. Cổng bắt được: "đề hỏi … chữ lạ cats".
    """
    sn = ((chuan_tu.get(tu) or ct12.get(tu) or {}) or {}).get("so_nhieu")
    if sn and kho is not None and sn.lower() not in kho:
        return None
    return sn


def hoi_doc(doan: list[str], nhom: list[dict], chuan_tu: dict, ct12: dict,
            unit: int, kho: set) -> list[dict]:
    """Câu hỏi sau khi đọc — BẰNG TIẾNG ANH, chỉ dùng khuôn đã học tới unit này.

    Ba khuôn hỏi, xếp theo lúc sách dạy chúng:
        What can you see?              lớp 2 unit 4  — dùng được từ đầu quyển
        How many … can you see?        lớp 1 unit 16 — cần từ có dạng số nhiều
        What's she doing?              lớp 2 unit 5  — cho unit dạy hoạt động
        What's this?                   lớp 4 unit 4  — chỉ từ unit 4 trở đi

    Cổng `tienganh_dochieu` soi lại từng chữ của ĐỀ theo túi từ đã học, nên khuôn
    nào lỡ dùng sớm là đỏ ngay.
    """
    ra = []
    nhin = next((c for c in doan if c.startswith("I can see")), None)
    lam = next((c for c in doan if c.startswith(("She's", "He's"))), None)

    co = {n["tu"] for n in nhom}
    # ⚠ MỒI PHẢI CÙNG KHUÔN VỚI ĐÁP ÁN, chỉ khác TÊN VẬT.
    # Mồi khác khuôn thì đáp án thành lựa chọn DUY NHẤT mang khuôn của nó — bé chọn
    # đúng bằng mắt, không cần đọc. Cổng bắt được 33 chỗ đúng kiểu ấy.
    ngoai = [t for t in ("dog", "cat", "duck", "goat", "car", "bag", "hat", "cup")
             if t not in co and t in kho]

    if nhin:
        ra.append({"loai": "yChinh", "en": "What can you see?",
                   "vi": "Con nhìn thấy gì trong tranh?", "dap": nhin,
                   "moi": [f"I can see {mao_tu(t)}." for t in ngoai[:3]]})
    elif lam:
        khac = [x for x in ("running", "walking", "swimming") if x in kho]
        ra.append({"loai": "yChinh", "en": "What's she doing?",
                   "vi": "Bạn ấy đang làm gì?", "dap": lam,
                   "moi": [f"She's {x}." for x in khac[:3]]})

    # ĐẾM — chỉ khi từ ấy có dạng số nhiều đã khai, nếu không thì "How many kites"
    # thành một chữ bé chưa gặp.
    for n in nhom:
        sn = so_nhieu_cua(n["tu"], chuan_tu, ct12, kho)
        if sn and len(ra) < 3 and not any("How many" in x["en"] for x in ra):
            ra.append({"loai": "chiTiet",
                       "en": f"How many {sn} can you see?",
                       # Dòng phụ là chỗ bám TIẾNG VIỆT — chép nguyên chữ tiếng Anh
                       # vào ("Con thấy mấy box?") thì nó chẳng bám hộ được gì.
                       "vi": f"Con thấy mấy {(chuan_tu.get(n['tu']) or ct12.get(n['tu']) or {}).get('nghia') or n['tu']}?",
                       "dap": "I can see one."})
            break

    # MÀU — bức dạy màu thì hỏi bằng đúng khuôn của nó: "What colour is it?"
    # Mồi là màu KHÁC, cùng khuôn "It's + [Colour]." — bé phải đọc mới chọn được.
    #
    # ⚠ "What colour is it?" KHÔNG NÓI RÕ HỎI VẬT NÀO — mà đoạn có bốn vật bốn màu,
    # nên bốn lựa chọn đều đúng với một vật nào đó. Đúng cái bác bắt: "nhiều câu
    # trả lời ý same same nhau rất khó cho con chọn". Sửa được bằng ĐỀ TIẾNG ANH
    # thì phải viết "What colour is the apple?" — sách chưa dạy khuôn ấy. Nên chốt
    # vật ở DÒNG PHỤ tiếng Việt: dòng phụ vốn sinh ra để làm chỗ bám, đây đúng chỗ
    # dùng nó, mà câu tiếng Anh vẫn nguyên si câu của sách.
    mau = next(((i, c) for i, c in enumerate(doan)
                if re.fullmatch(r"It's (\w+)\.", c)
                and c[5:-1].strip() in MAU_CUA.values()), None)
    if mau and len(ra) < 3:
        i, cau = mau
        cua = next((n["tu"] for n in nhom if n["tu"] in (doan[i - 1] if i else "")), None)
        nghia = ((chuan_tu.get(cua) or ct12.get(cua) or {}).get("nghia") or cua or "vật")
        khac = [m for m in ("black", "blue", "green", "red", "white", "yellow")
                if m in kho and f"It's {m}." != cau]
        ra.append({"loai": "chiTiet", "en": "What colour is it?",
                   "vi": f"{nghia} ({cua}) màu gì?", "dap": cau,
                   "moi": [f"It's {m}." for m in khac[:3]]})

    # ĐANG LÀM GÌ — cho unit dạy hoạt động, hoặc "What's this?" cho unit từ 4 trở đi.
    if lam and len(ra) < 3 and not any(x["en"].startswith("What's she") for x in ra) and False:
        ra.append({"loai": "chiTiet", "en": "What's she doing?",
                   "vi": "Bạn ấy đang làm gì?", "dap": lam})
    elif unit >= 4 and len(ra) < 3:
        vat = next((c for c in doan if c.startswith(("This is", "That's"))), None)
        # ⚠ NGƯỜI thì hỏi "Who's this?" — "What's this?" về bố mẹ là hỏi bố mẹ là
        # CÁI GÌ. Khuôn "Who's this? - It's my sister." là của chính unit 11.
        nguoi = bool(vat and " my " in vat)
        if nguoi and unit < 11:
            vat = None
        if vat:
            ra.append({"loai": "chiTiet",
                       "en": "Who's this?" if nguoi else "What's this?",
                       "vi": "Đây là ai?" if nguoi else "Đây là cái gì?",
                       "moi": [f"It's {mao_tu(t)}." for t in ngoai[:3]],
                       "dap": "It's " + vat.split(" is ", 1)[-1].replace("That's ", "")
                              if " is " in vat else "It's " + vat[len("That's "):]})
    return ra


def moi_sai(nhom: list[dict], chuan_tu: dict, ct12: dict, kho: set) -> list[str]:
    """Mồi nhử — câu ĐÃ HỌC nhưng KHÔNG tả bức tranh này, và khác khuôn nhau.

    Không suy được bằng máy rằng một câu "sai với tranh": "There's a cat." có thể
    đúng dù không nằm trong đoạn. Nên chỉ lấy vật KHÔNG có trong tranh — chắc chắn
    sai, vì tranh chỉ vẽ đúng những vật đã khai.
    """
    co = {n["tu"] for n in nhom}
    ung = [t for t in ("dog", "cat", "ball", "car", "duck", "goat", "garden", "bag")
           if t not in co and t in kho]
    khuon = ["I can see {a}.", "There's {a}.", "This is {a}."]
    ra = []
    for i, t in enumerate(ung[:3]):
        ra.append(khuon[i % len(khuon)].format(a=mao_tu(t)))
    # Một câu hoạt động cho khác hẳn hình dạng — "She's running." của lớp 1 unit 11.
    if "running" in kho:
        ra.append("She's running.")
    return ra


# Đạo cụ trung tính — đứng được trong bất kỳ cảnh nào, và đếm được. Dùng ở hai
# chỗ: độn cho unit dạy hoạt động, và bảo đảm bức nào cũng hỏi được câu "How many".
PHU = ["kite", "bike", "cake", "table", "box", "tent", "van", "car"]


def soan(b, chuan_tu, truoc, canh, canh_en, chuan_tu12=None, du_phong=None) -> dict:
    viec = viec_cua(b, chuan_tu)
    vat = vat_cua(b, chuan_tu, truoc, chuan_tu12, du_phong)
    kho = kho_chu(4, b["so"])

    nhom, doan = [], []
    # ⚠ UNIT DẠY HOẠT ĐỘNG THÌ KHÔNG ĐỘN VẬT CỦA UNIT KHÁC vào — ra tranh
    # "cooking · drawing · face · dancing", cái mặt lạc giữa mấy người đang làm việc.
    #
    # NHƯNG unit dạy CẢ HAI thì phải có cả hai: unit 20 dạy con vật (elephant ·
    # tiger · monkey) LẪN việc chúng đang làm (climbing · swinging). Bỏ hết vật thì
    # bức "Ở vườn thú" không có lấy một con thú. Vật của CHÍNH unit ấy thì giữ.
    #
    # ⚠ NHƯNG "không độn" mà thành TRANH TRỐNG thì còn tệ hơn lạc chủ đề. Từ khi
    # `viec_cua` đòi hình phải có NGƯỜI, unit 18 chỉ còn `dancing` + `table` — hai
    # vật, đoạn hai câu, ở gần cuối quyển. Nên: ưu tiên vật của chính unit, còn
    # THIẾU thì mượn tiếp cho đủ bốn.
    # Mượn thì mượn ĐỒ ĐẠO CỤ, không mượn từ đầu danh sách: `PHU` là mấy thứ đứng
    # được trong bất kỳ cảnh nào. Mượn bừa thì U05 "Sở thích" ra "cooking · running
    # · dancing · face" — đúng cái lạc chủ đề đoạn trên vừa chép ra làm ví dụ.
    tu_minh = {t["tu"] for t in b["knowledgeCore"]["vocabulary"]}
    uu = UU_TIEN.get(b["so"]) or {}
    if uu:
        # Người đã khai vật cho bức này. MÁY VẪN SOI: chưa học tới thì loại, không
        # có hình thì loại — khai sai không lọt ra bản chạy được, chỉ mất chỗ ấy.
        hinh_da = hinh_cua_tu(4, b["so"])
        # ⚠ PHÉP SOI CỦA `UU_TIEN` PHẢI CHẶT BẰNG LUẬT CHUNG, không lỏng hơn.
        # Bản đầu chỉ hỏi "đã học chưa · có hình chưa · đếm được không", KHÔNG hỏi
        # "đặt được sau chữ a không". Nên khai tay là lọt thẳng, và ra:
        #     ✗ This is a sunny.   (tính từ)
        #     ✗ I can see an eyes. (danh từ số nhiều)
        # Cả hai đều đúng khuôn, đúng túi từ, không cổng nào bắt — chỉ đọc mới thấy.
        # ⚠ NGOẠI LỆ CÓ TÊN, không phải nới luật.
        # `basketball` · `volleyball` · `football` mang vai `trochoi`, và `trochoi`
        # bị chặn vì "a badminton" sai hẳn. Nhưng BA QUẢ BÓNG thì đếm được và vẽ
        # được — lớp 3 đã chốt đúng thế. Ghi tên từng từ ở đây; nới cả vai thì
        # `badminton` · `chess` lọt theo.
        NGOAI_LE = {"basketball", "volleyball", "football"}

        def dat_duoc_sau_a(t: str) -> bool:
            if t in NGOAI_LE:
                return True
            vai = set((chuan_tu.get(t) or (chuan_tu12 or {}).get(t) or {}).get("vai") or [])
            if vai & VAI_BO:
                return False
            # số nhiều: `eyes` · `shoes` · `chips`. Danh sách ngoại lệ vì tiếng Anh
            # có `glass` · `bus` · `dress` tận cùng bằng s mà vẫn là số ít.
            if t.endswith("s") and not t.endswith(("ss", "us")) and t[:-1] in kho:
                return False
            return True

        vat = [t for t in uu["vat"]
               if t in kho and " " not in t and t.lower() not in KHONG_DEM
               and (hinh_da.get(t, {}).get("hinh") or hinh_da.get(t, {}).get("ve"))
               and dat_duoc_sau_a(t)]
        thieu = [t for t in uu["vat"] if t not in vat]
        if thieu:
            print(f"   ⚠ U{b['so']:02d} khai vật chưa dùng được: {' '.join(thieu)}")
    elif viec:
        viec = viec[:BOT_VIEC]
        rieng = [t for t in vat if t in tu_minh]
        khac = [t for t in PHU if t in kho and t not in rieng]
        khac += [t for t in vat if t not in tu_minh and t not in khac]
        vat = rieng[:2]
        while len(viec) + len(vat) < TOI_DA_VAT - 1 and khac:
            vat.append(khac.pop(0))
    if viec:
        # Unit dạy HOẠT ĐỘNG: tranh vẽ người đang làm, câu dùng khuôn "She's …ing."
        for i, v in enumerate(viec):
            nhom.append({"tu": v, "so": 1, "ke": i % SO_KE, "co": 110})
            doan.append(KHUON_VIEC[i % len(KHUON_VIEC)].format(ing=v))
    # Vật CHỦ THỂ đứng trước, vẽ to, một mình kệ trên: bức "Cơ thể chúng mình" là
    # tả MỘT khuôn mặt, mắt mũi mồm là bộ phận của nó — không phải năm vật rời.
    # ⚠ CẮT Ở ĐÂY, TRƯỚC KHI SINH CÂU. Kệ dưới chỉ chứa ba vật, nên bức có chủ thể
    # tối đa 1 + 3. Cắt sau khi đã sinh câu thì ra bốn vật đi với năm câu — bé đọc
    # một câu tả thứ không có trên tranh, đúng cái bẫy "cắt cả hai cùng một chỗ".
    chinh = uu.get("chinh")
    if chinh and chinh in vat:
        vat = [chinh] + [t for t in vat if t != chinh][:(SO_KE - 1) * 3]
    for i, t in enumerate(vat):
        if len(doan) >= TOI_DA_VAT and not uu.get("mau"):
            break
        la_chinh = bool(chinh) and t == chinh
        nhom.append({"tu": t, "so": 1,
                     "ke": 0 if la_chinh else (1 + (len(nhom) - 1) % (SO_KE - 1) if chinh
                                       else len(nhom) % SO_KE),
                     # ⚠ 190 là cỡ của bố cục HAI kệ. Với ba kệ thì kệ trên cùng thấp hơn,
                     # vật to đè lên dòng tựa đề tiếng Anh — che mất chữ.
                     "co": 150 if la_chinh else 110})
        # ⚠ Tra CẢ hai kho. `chuan_tu` chỉ có từ lớp 4; `mother` · `brother` ·
        # `sister` · `father` là từ lớp 1–3 nên tra hụt → vai rỗng → rơi vào khuôn
        # "This is a …" và ra "That's a brother." Người nhà phải đi với "my".
        vai = set(((chuan_tu.get(t) or (chuan_tu12 or {}).get(t)) or {}).get("vai") or [])
        if la_chinh:
            doan.append(f"This is {mao_tu(t)}.")
        elif chinh:
            # Bộ phận của chủ thể: BỎ khuôn "That's …" — "That's an ear." nghe như
            # chỉ sang tai người khác, mà đây là mắt mũi mồm của CHÍNH khuôn mặt ấy.
            # Vẫn phải xoay hai khuôn, vì ba dòng liền cùng khuôn là đoạn văn lặp và
            # cổng "không quá 2 dòng cùng khuôn" bắt đúng.
            doan.append(["I can see {a}.", "There's {a}."][(i - 1) % 2].format(a=mao_tu(t)))
        elif vai & VAI_NHA:
            doan.append(KHUON_NHA[i % len(KHUON_NHA)].format(t=t))
        else:
            doan.append(KHUON_KE[i % len(KHUON_KE)].format(a=mao_tu(t)))
        # BỨC DẠY MÀU: nói tên vật rồi nói màu nó, đúng khuôn của chính unit 9
        # ("What colour is it? - It's + [Colour]."). Không có câu màu thì bức "Màu
        # sắc" chẳng nhắc tới màu nào — bé đọc xong không biết bài dạy gì.
        if uu.get("mau") and MAU_CUA.get(t) in kho:
            doan.append(f"It's {MAU_CUA[t]}.")

    # ── RẢI KHUÔN: không quá HAI dòng cùng hình dạng ──
    # Cổng đo hình dạng bằng (chữ đầu | số chữ). Với 7 vật mà chỉ 4 khuôn kể thì
    # một khuôn phải dùng ba lần → đỏ. Tệ hơn: `KHUON_NHA` ("This is my X.") ĐỤNG
    # hình dạng với `KHUON_KE` ("This is a X.") — cùng "this|4" — nên bức có người
    # nhà chạm trần mà nhìn thì tưởng đã xoay đủ.
    def dang(c):
        w = c.split()
        return f"{w[0].lower()}|{len(w)}" if w else ""

    def la_nha(i):
        if i >= len(nhom):
            return True
        t = nhom[i]["tu"]
        vai = set(((chuan_tu.get(t) or (chuan_tu12 or {}).get(t)) or {}).get("vai") or [])
        return bool(vai & VAI_NHA)

    dem = {}
    for i, c in enumerate(doan):
        d = dang(c)
        dem[d] = dem.get(d, 0) + 1
        if dem[d] <= 2:
            continue
        # ⚠ KHÔNG đổi khuôn của NGƯỜI NHÀ — họ chỉ có hai khuôn, và cả hai đều
        # phải giữ chữ "my". Bản đầu đổi bừa và ra "I can see a mother."
        # Đổi một dòng KHÁC cùng hình dạng, dòng nào không phải người nhà.
        thay_o = i if not la_nha(i) else next(
            (j for j in range(len(doan))
             if j != i and dang(doan[j]) == d and not la_nha(j)), None)
        if thay_o is None:
            continue
        tu = nhom[thay_o]["tu"]
        for kh in KHUON_KE:
            thu = kh.format(a=mao_tu(tu))
            if dang(thu) != d and dem.get(dang(thu), 0) < 2:
                dem[d] -= 1
                dem[dang(thu)] = dem.get(dang(thu), 0) + 1
                doan[thay_o] = thu
                break

    # ── LUÔN CÓ MỘT VẬT ĐẾM ĐƯỢC ──
    # Không có thì bức tranh chỉ hỏi được MỘT câu, mà cổng đòi đủ cả tổng quan lẫn
    # chi tiết. Unit dạy hoạt động (U05 · U18 · U19 · U20) và unit dạy người nhà
    # (U11) đều rơi vào đó: đoạn toàn "She's dancing." hoặc "This is my father.",
    # không câu nào đếm được và cũng không câu nào mở đầu bằng "I can see".
    # Thêm một vật phụ vừa chữa được cả hai, vừa làm tranh đỡ trống.
    #
    # ⚠ KHÔNG ĐỘN VÀO BỨC ĐÃ KHAI TAY. Bức "Cơ thể chúng mình" mà độn thêm cái diều
    # cho đủ câu hỏi đếm thì lại hỏng đúng chỗ vừa chữa. Bức khai tay hỏi được
    # "What's this?" (khuôn của chính unit 4) nên vẫn đủ hai câu.
    co_dem = any(so_nhieu_cua(n["tu"], chuan_tu, chuan_tu12 or {}, kho) for n in nhom)
    co_nhin = any(c.startswith("I can see") for c in doan)
    if not uu and (not co_dem or not co_nhin) and len(nhom) < 6:
        for t in PHU[b["so"] % len(PHU):] + PHU[:b["so"] % len(PHU)]:
            if t in {n["tu"] for n in nhom} or t not in kho:
                continue
            if not so_nhieu_cua(t, chuan_tu, chuan_tu12 or {}, kho):
                continue
            nhom.append({"tu": t, "so": 1, "ke": len(nhom) % SO_KE, "co": 100})
            doan.append(f"I can see {mao_tu(t)}.")
            break

    # ⚠ MỖI VẬT ĐÚNG MỘT CÂU, KHÔNG THỪA KHÔNG THIẾU.
    # Đoạn bị cắt ở năm câu (`doan[:5]`) trong khi `nhom` giữ cả sáu vật, nên tranh
    # vẽ một vật không ai tả — đúng cái bác bắt ở unit 0 ("nội dung phải đồng bộ với
    # tranh"), chỉ ngược chiều. Cắt CẢ HAI cùng một chỗ.
    #
    # Bức dạy MÀU có HAI câu cho một vật ("This is an apple." + "It's red.") nên cắt
    # theo số VẬT, không theo số câu.
    if uu.get("mau"):
        nhom = nhom[:TOI_DA_VAT]
        doan = doan[:len(nhom) * 2]
    else:
        nhom, doan = nhom[:TOI_DA_VAT], doan[:TOI_DA_VAT]

    # Xếp chỗ: mỗi kệ nhiều nhất ba vật, cách đều. Vật chủ thể vẽ to thì đứng giữa
    # kệ trên một mình.
    #
    # ⚠ CẮT Ở ĐÂY LÀ CẮT VẬT MÀ KHÔNG CẮT CÂU — đúng cái bẫy đã dính một lần. Kệ
    # dưới chỉ chứa được ba, nên bức có chủ thể tối đa là 1 + 3 vật; cắt `doan`
    # theo đó luôn, đừng để bốn vật đi với năm câu.
    ke_ds = [[n for n in nhom if n["ke"] == k][:3] for k in range(SO_KE)]
    assert sum(len(x) for x in ke_ds) == len(nhom), "kệ không chứa hết vật — cắt sớm hơn"
    nhom = []
    for ke, ds in enumerate(ke_ds):
        for i, n in enumerate(ds):
            n["ke"] = ke
            n["x"] = 640 if len(ds) == 1 else 250 + i * 300
            nhom.append(n)

    return {
        "id": f"TRANH:TA4.U{b['so']:02d}",
        "unit": b["so"], "chuong": b["chuong"],
        "ten": canh, "ten_en": canh_en,
        # ⚠ Kệ dưới cùng ở y=700 thì thanh kệ chạm mép ảnh (cao 720) và bị cắt.
        "ke": [300, 480, 660],
        "nhom": nhom,
        # ⚠ KHÔNG cắt lại ở đây. Cắt đã làm xong ở trên, theo số VẬT; cắt lần nữa
        # theo số CÂU thì bức dạy màu (hai câu một vật) mất sạch mấy câu màu — và
        # đó chính là thứ unit ấy dạy.
        "doan": doan,
        "hoiDoc": hoi_doc(doan, nhom, chuan_tu, chuan_tu12 or {}, b["so"], kho),
        "sai": moi_sai(nhom, chuan_tu, chuan_tu12 or {}, kho),
        "hoiGoiY": [{"hoi": "What can you see?", "y": "bé kể một vật trong tranh"}],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true")
    a = p.parse_args()

    chuan = json.loads((GOC / "data/tienganh/chuan_lop4.json").read_text("utf8"))
    chuan_tu = {t["tu"]: t for u in chuan["unit"] for t in u["tu"]}
    canh_cua = {u["so"]: str(u.get("canh") or "").split("·") for u in chuan["unit"]}

    # ⚠ LỚP 4 GỘP BA QUYỂN, không phải hai. Tên biến `ct12` là di sản của lớp 3;
    # để nguyên (1, 2) thì từ của lớp 3 tra hụt — `mother` · `father` rơi vào khuôn
    # "This is a mother." thay vì "This is my mother."
    ct12 = {}
    # ⚠ GHI ĐÈ, KHÔNG `setdefault`. Sách dạy lại một từ ở lớp sau thì bản sau
    # thường KHAI ĐÚNG HƠN: `mother` ở lớp 1 khai vai `dt`, lớp 3 khai `giadinh`.
    # Giữ bản đầu tiên là giữ bản thô nhất, và ra "This is a mother."
    for l in (1, 2, 3):
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{l}.json").read_text("utf8"))
        for u in cn["unit"]:
            for t in u["tu"]:
                ct12[t["tu"]] = t
    du_phong = bai_lop123()
    bais = bai_lop4()
    ra = []
    for i, b in enumerate(bais):
        # ⚠ Lớp 3 BỎ QUA unit 0 vì bức ấy khai tay. Lớp 4 KHÔNG có bản khai tay
        # nào, nên bỏ qua là mất trắng bức Starter — 20 bức thay vì 21, và không
        # có gì báo. Cứ soạn; muốn sửa tay thì đặt cờ `tay: true` như mọi bức khác.
        c = canh_cua.get(b["so"]) or [""]
        k = soan(b, chuan_tu, bais[:i], c[0].strip(),
                 (c[1].strip() if len(c) > 1 else ''), ct12, du_phong)
        k.pop("_kho", None)
        ra.append(k)
        print(f"U{b['so']:02d} {k['ten'][:26]:28s} {len(k['nhom'])} vật · "
              f"{len(k['doan'])} câu · {' '.join(n['tu'] for n in k['nhom'])}")

    if a.ghi:
        p2 = GOC / "data/tienganh/tranh_lop4.json"
        cu = json.loads(p2.read_text("utf8"))
        # ⚠ Bộ lớp 3 GIỮ RIÊNG unit 0 vì bức ấy khai tay và không nằm trong `ra`.
        # Lớp 4 tự soạn cả U0, nên giữ riêng là ĐẾM HAI LẦN — ra 22 bức cho 21 unit.
        # Chỉ giữ bức nào mang cờ `tay`.
        giu = {k["unit"]: k for k in cu if k.get("tay")}
        moi = [giu.get(k["unit"], k) for k in ra]
        p2.write_text(json.dumps(moi, ensure_ascii=False, indent=1) + "\n", "utf8")
        print(f"→ {p2.relative_to(GOC)}  ({len(moi)} bức)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
