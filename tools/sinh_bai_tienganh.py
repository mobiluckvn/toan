#!/usr/bin/env python3
"""SINH BÀI HỌC TIẾNG ANH từ bản đồ đã chuẩn hoá.

    python3 tools/sinh_bai_tienganh.py --lop 1 --unit 4        # dựng thử một unit
    python3 tools/sinh_bai_tienganh.py --lop 1 --tat-ca        # cả quyển

Đọc `data/tienganh/chuan_lop{N}.json` (do `chuan_tienganh.py` sinh ra) và đẻ ra bài
học đúng khuôn `digital-lesson/v2-micro` — cùng khuôn bốn quyển Toán đang chạy, để
`LessonPlayer` dựng được mà không phải sửa một dòng nào.

── BỐN BẬC, BA MỨC SAO ──
Bốn việc bác nêu — hiểu từ · hiểu cấu trúc · nói · gõ — xếp vào ba pool có sẵn:

    warmup    ★      bậc 1 NGHE-NHÌN  + bậc 2 HIỂU NGHĨA
    standard  ★★     bậc 3 CẤU TRÚC   (xếp thẻ · điền chỗ trống)
    challenge ★★★    bậc 4 GÕ LẠI     (gõ từ → gõ câu)

Phần NÓI hoãn sang Đợt sau (bác chốt): Đợt 1 bé chỉ nghe và nhại, không chấm.

── HAI LUẬT KHI SINH ──

1. CÂU CHỈ LẤY TỪ BẢNG THAY THẾ (`o_thay`, tức cạnh HAS_SLOT của bản đồ).
   Đó là những câu người soạn sách đã duyệt. Máy KHÔNG tự ghép câu mới — ghép thì
   sớm muộn cũng ra câu sai ngữ pháp mà không ai soát nổi 16 bài.

2. MỒI NHỬ LẤY TỪ CÙNG UNIT.
   Cả unit cùng một chữ cái đầu, nên bé chọn sai là vì chưa phân biệt được nguyên
   âm ở giữa — đúng cái bài đang dạy. Mồi lấy từ unit khác thì bé đoán trúng bằng
   chữ cái đầu và không học được gì.

── KHÔNG NHÂN VẬT ──
Quyển này dựng cho MỌI học sinh. Không Trí Long, không Su Kem — bé học Tiếng Anh
lớp 1 chưa chắc đã học Toán lớp 2. Khuôn "nghe câu sai rồi tự nhận ra" vẫn giữ,
nhưng câu sai đứng một mình, không cần ai nói nó ra.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}
TIEN_TO = {1: "DL:TA1.", 2: "DL:TA2.", 3: "DL:TA3."}

# Gõ được thì gõ; dài hơn ngần này thì bậc 4 chuyển sang GHÉP THẺ CHỮ CÁI.
# Bé 6 tuổi gõ ~10 ký tự/phút — từ 10 ký tự là bỏ cuộc chứ không phải làm sai.
GO_TOI_DA = 5
THE_TOI_DA = 5          # trùng THE_TOI_DA của mon/tienganh/lib/cham.js


def am_id(loai: str, khoa: str) -> str:
    """Mã clip âm. Dùng chung giữa các bài: từ `dog` chỉ sinh MỘT lần cho cả quyển."""
    sach = "".join(c if c.isalnum() else "_" for c in khoa.lower()).strip("_")
    return f"{loai}_{sach}"[:60]


def moi_nhu(dung: dict, ho: list[dict], n: int = 3, khoa: str = "tu") -> list[str]:
    """n mồi nhử LẤY TỪ CÙNG UNIT — xem luật 2 ở đầu tệp."""
    ra = [x[khoa] for x in ho if x["ma"] != dung["ma"] and x.get(khoa)]
    return ra[:n]


def tron(dung: str, moi: list[str]) -> list[str]:
    """Xếp đáp án vào giữa đám mồi. KHÔNG dùng random: chạy hai lần phải ra hai tệp
    giống hệt nhau, nếu không thì `git diff` đầy nhiễu và không ai soát nổi."""
    ds = list(moi)
    ds.insert(min(len(ds), (len(dung) + len(ds)) % (len(ds) + 1)), dung)
    return ds


# ───────────────────────── dựng từng chặng ─────────────────────────

def dien(cong_thuc: str, gan: dict) -> str:
    """Điền các ô của CÔNG THỨC. `"This is a + [Noun]."` + {Noun: "dog"} → `"This is a dog."`

    ── VÌ SAO KHÔNG THAY CHUỖI TRONG CÂU VÍ DỤ ──
    Bản đầu lấy `vi_du` rồi `replace` từ cũ bằng từ mới. Vỡ ở U15: câu mẫu là
    "Point to your hand." còn từ của unit là face·father·foot·football — `hand`
    thuộc U8, KHÔNG có trong danh sách từ của U15. Phép tìm trả về chuỗi RỖNG, và
    `"...".replace("", "face", 1)` dán "face" vào đầu câu:

        ✗  "facePoint to your hand."

    U11 thoát nạn chỉ vì "run" tình cờ là chuỗi con của "running" — đúng vì một lý
    do sai, tức là sẽ vỡ ngay khi đổi dữ liệu. Điền vào CÔNG THỨC thì không có chỗ
    nào để đoán, và mẫu nhiều ô cũng chạy luôn.
    """
    s = cong_thuc.replace(" + ", " ")
    for o, w in gan.items():
        s = s.replace(f"[{o}]", w)
    return s


def dang_can(o_ten: str, t: dict) -> str | None:
    """Ô đòi DẠNG nào của từ — suy từ chính tên ô trong công thức.

    Bản đồ cho từ ở dạng GỐC (`run`, `window`) còn câu cần dạng biến đổi
    (`running`, `windows`). Ghép thẳng thì ra "She's run." — xem lop1_bu.json.
    """
    if "Verb-ing" in o_ten:
        return t.get("dang_ing")
    if "plural" in o_ten:
        return t.get("so_nhieu") or (t["tu"] if "sonhieu" in (t.get("vai") or []) else None)
    return t["tu"]


def ung_vien(vai_can: list, tu: list, them: dict) -> list[dict]:
    """Những từ được phép điền vào một ô, theo VAI đã khai ở lop1_bu.json."""
    kho = list(tu)
    for nhom in ("so_dem", "mau", "ten"):
        for m in (them.get(nhom) or {}).get("muc", []):
            kho.append({"tu": m["word"] if isinstance(m, dict) else m,
                        "nghia": m.get("nghia", "") if isinstance(m, dict) else "",
                        "ipa": m.get("ipa", "") if isinstance(m, dict) else "",
                        "vai": m.get("vai", ["ten"]) if isinstance(m, dict) else ["ten"],
                        "ma": f"them_{nhom}_{m if isinstance(m, str) else m['word']}",
                        "go_duoc": True})
    return [t for t in kho if set(t.get("vai") or []) & set(vai_can)]


def sinh_cau(u: dict, tu: list, them: dict, sua_slot: dict, toi_da: int = 4) -> list[dict]:
    """Câu của một unit: câu SGK đứng đầu, rồi các câu thay MỘT ô mỗi lần.

    Chỉ đổi một ô mỗi câu — đó đúng là cách một bảng thay thế dạy: giữ nguyên khung,
    đổi một chỗ, để bé thấy chỗ nào là chỗ thay được. Đổi hai ô cùng lúc thì bé
    không biết cái gì vừa đổi.
    """
    ra = []
    for mc in u["mau_cau"]:
        ct, goc = mc.get("cong_thuc") or "", mc.get("vi_du") or ""
        os = [m[1:-1] for m in re.findall(r"\[[^\]]+\]", ct)]
        if not os:
            continue
        khai = (sua_slot.get(mc["ma"]) or {}).get("o") or {}
        # Ô một mình thì suy vai từ chính danh sách o_thay; nhiều ô thì BẮT BUỘC
        # phải khai vai, không thì thay bừa ra "It's a pen bell."
        if len(os) > 1 and not khai:
            continue

        kho = {}
        for o in os:
            if khai.get(o):
                kho[o] = ung_vien(khai[o], tu, them)
            else:
                kho[o] = [t for t in tu if t["tu"] in mc["o_thay"]]
            if not kho[o]:
                break
        if any(not v for v in kho.values()) or len(kho) != len(os):
            continue

        # Neo vào CÂU SGK: tìm xem mỗi ô đang là từ nào trong câu ấy. Khớp từ dài
        # trước để "pen" không cướp chỗ của "pencil".
        nen, hoa, neo_duoc = {}, {}, {}
        for o in os:
            hop = sorted(kho[o], key=lambda t: -len(t["tu"]))
            found = None
            for t in hop:
                for d in filter(None, {dang_can(o, t), t["tu"]}):
                    if d.lower() in goc.lower():
                        found, hoa[o] = t, d[0].isupper() or d.capitalize() in goc
                        break
                if found:
                    break
            nen[o] = found or hop[0]
            # Neo HỤT nghĩa là từ trong câu SGK không nằm trong kho của ô này —
            # U15 "Point to your hand." mà `hand` lại là từ của U8. Khi ấy từ nền
            # chỉ là chỗ dựa tạm, nên nó VẪN phải được sinh thành câu riêng; bỏ nó
            # đi là mất trắng "Point to your face."
            neo_duoc[o] = found is not None
            hoa.setdefault(o, False)

        def chu(o, t):
            d = dang_can(o, t) or t["tu"]
            return d.capitalize() if hoa.get(o) else d

        # câu SGK trước — đó là câu đã có người soạn sách duyệt
        ra.append({"cau": goc or dien(ct, {o: chu(o, nen[o]) for o in os}),
                   "tu": nen[os[-1]], "mc": mc})

        # Đổi LUÂN PHIÊN từng ô, mỗi vòng một ô. Bản đầu vét cạn ô thứ nhất rồi mới
        # sang ô sau, nên U6 ("It's a + [Colour] + [Noun].") có 6 màu là đủ chạm
        # trần 4 câu — bé thấy bốn câu đổi màu mà KHÔNG BAO GIỜ thấy danh từ đổi,
        # tức là học một nửa mẫu câu.
        hang = {o: [t for t in kho[o] if not (neo_duoc[o] and t["ma"] == nen[o]["ma"])]
                for o in os}
        while sum(1 for x in ra if x["mc"] is mc) < toi_da and any(hang.values()):
            for o in os:
                if not hang[o]:
                    continue
                t = hang[o].pop(0)
                gan = {x: chu(x, nen[x]) for x in os}
                gan[o] = chu(o, t)
                c = dien(ct, gan)
                if c != goc:
                    ra.append({"cau": c, "tu": t, "mc": mc})
                if sum(1 for x in ra if x["mc"] is mc) >= toi_da:
                    break
    # bỏ câu trùng, giữ thứ tự
    thay, sach = set(), []
    for c in ra:
        if c["cau"] not in thay:
            thay.add(c["cau"])
            sach.append(c)
    return sach


def cau_hoi(u: dict, lop: int, them: dict, sua_slot: dict) -> tuple[list, list, list, list]:
    """Trả về (warmup, standard, challenge, câu)."""
    tu = [t for t in u["tu"] if t.get("nghia")]
    cau = sinh_cau(u, tu, them, sua_slot)

    warmup, standard, challenge = [], [], []

    # ── ★ bậc 1 · NGHE rồi bấm HÌNH ──
    for i, t in enumerate(tu, 1):
        warmup.append({
            "id": f"C{i}",
            "bac": 1,
            "text": "Nghe rồi bấm vào hình đúng.",
            "am": am_id("tu", t["tu"]),
            "anhChon": True,
            "format": "chon",
            "choices": tron(t["tu"], moi_nhu(t, tu)),
            # Nút của bậc 1 hiện HÌNH chứ không hiện chữ — bé chưa đọc được chữ
            # tiếng Anh thì bấm vào chữ là đoán mò. Chữ vẫn là giá trị đáp án để
            # bộ chấm so, nhưng cái bé NHÌN là emoji.
            "hinhNut": {x: (next((y.get("hinh") for y in tu if y["tu"] == x), None))
                        for x in tron(t["tu"], moi_nhu(t, tu))},
            "veNut": {x: (next((y.get("hinh_ve") for y in tu if y["tu"] == x), None))
                      for x in tron(t["tu"], moi_nhu(t, tu))},
            "answerKey": {"choice": t["tu"]},
            "solutionNarrative": f"{t['tu']} — {t['nghia']}",
            "hints": [f"Nghe lại xem từ này bắt đầu bằng âm nào.",
                      f"Từ này nghĩa là “{t['nghia']}”."],
        })

    # ── ★ bậc 2 · TỪ ↔ NGHĨA, cả hai chiều ──
    n = len(warmup)
    for i, t in enumerate(tu, 1):
        warmup.append({
            "id": f"C{n + i}",
            "bac": 2,
            "text": f"“{t['tu']}” nghĩa là gì?",
            "am": am_id("tu", t["tu"]),
            "format": "chon",
            "choices": tron(t["nghia"], moi_nhu(t, tu, khoa="nghia")),
            "answerKey": {"choice": t["nghia"]},
            "solutionNarrative": f"{t['tu']} {t['ipa']} — {t['nghia']}",
            "hints": ["Nghe lại từ rồi nghĩ xem con nhìn thấy nó ở đâu."],
        })
    n = len(warmup)
    for i, t in enumerate(tu, 1):
        warmup.append({
            "id": f"C{n + i}",
            "bac": 2,
            "text": f"“{t['nghia']}” tiếng Anh là gì?",
            "format": "chon",
            "choices": tron(t["tu"], moi_nhu(t, tu)),
            "answerKey": {"choice": t["tu"]},
            "solutionNarrative": f"{t['nghia']} — {t['tu']} {t['ipa']}",
            "hints": ["Cả bốn từ đều bắt đầu giống nhau — nghe kỹ phần GIỮA của từ."],
        })

    # ── ★★ bậc 3 · XẾP THẺ và ĐIỀN CHỖ TRỐNG ──
    for i, c in enumerate(cau, 1):
        the = c["cau"].split()
        if len(the) > THE_TOI_DA:
            continue
        standard.append({
            "id": f"S{i}",
            "bac": 3,
            "text": "Xếp các thẻ thành câu đúng.",
            "am": am_id("cau", c["cau"]),
            "the": the,
            "answerKey": {"the": the},
            "solutionNarrative": c["cau"],
            "hints": ["Câu tiếng Anh bắt đầu bằng chữ viết hoa.",
                      "Thẻ có dấu chấm là thẻ cuối cùng."],
        })
    n = len(standard)
    for i, c in enumerate(cau, 1):
        t = c["tu"]
        standard.append({
            "id": f"S{n + i}",
            "bac": 3,
            "text": "Nhìn hình rồi chọn từ điền vào chỗ trống:  "
                    + c["cau"].replace(t["tu"], "___", 1),
            # CỐ Ý KHÔNG có `am` cả câu. Phát cả câu lên thì bé chỉ việc nghe rồi
            # bấm — thành bài NGHE lặp lại của bậc 1, không còn kiểm cấu trúc nữa.
            # Manh mối ở đây là HÌNH; chỗ trống là chỗ bé phải tự nối hình với từ.
            "anh": t.get("hinh"),
            "anhVe": t.get("hinh_ve"),
            "format": "chon",
            "choices": tron(t["tu"], moi_nhu(t, tu)),
            "answerKey": {"choice": t["tu"]},
            "solutionNarrative": c["cau"],
            "hints": ["Nhìn hình xem đó là con gì, cái gì.",
                      "Rồi nhớ lại từ tiếng Anh của nó."],
        })

    # ── ★★★ bậc 4 · GÕ LẠI ──
    for i, t in enumerate(tu, 1):
        if t["go_duoc"] and len(t["tu"]) <= GO_TOI_DA:
            challenge.append({
                "id": f"T{i}",
                "bac": 4,
                "text": f"Nghe rồi gõ lại từ này. ({t['nghia']})",
                "am": am_id("tu", t["tu"]),
                "answerKey": {"value": t["tu"]},
                "solutionNarrative": f"{t['tu']} {t['ipa']} — {t['nghia']}",
                "hints": [f"Từ này có {len(t['tu'])} chữ cái.",
                          f"Bắt đầu bằng chữ “{t['tu'][0]}”."],
            })
        else:
            # Từ dài thì GHÉP THẺ CHỮ CÁI thay cho gõ — nấc 1 của bậc 4.
            challenge.append({
                "id": f"T{i}",
                "bac": 4,
                "text": f"Ghép các chữ cái thành từ. ({t['nghia']})",
                "am": am_id("tu", t["tu"]),
                "the": list(t["tu"]),
                "answerKey": {"the": list(t["tu"])},
                "solutionNarrative": f"{t['tu']} {t['ipa']} — {t['nghia']}",
                "hints": [f"Từ này dài {len(t['tu'])} chữ cái."],
            })
    n = len(challenge)
    for i, c in enumerate(cau[:2], 1):     # chỉ 2 câu — gõ cả câu là việc nặng nhất
        challenge.append({
            "id": f"T{n + i}",
            "bac": 4,
            "text": "Nghe rồi gõ lại cả câu.",
            "am": am_id("cau", c["cau"]),
            "answerKey": {"value": c["cau"]},
            "solutionNarrative": c["cau"],
            "hints": ["Nhớ viết hoa chữ đầu câu và chấm ở cuối.",
                      "Gõ thiếu chữ “a” là câu sai — tiếng Anh bắt buộc phải có."],
        })

    return warmup, standard, challenge, cau


# ───────────────────────── CHỖ DỄ NHẦM ─────────────────────────

"""BẢNG LỖI NGƯỜI VIỆT HỌC TIẾNG ANH HAY MẮC — mỗi mẫu câu một lỗi CỦA NÓ.

── VÌ SAO CÓ CẢ BẢNG NÀY, THAY VÌ MỘT CÂU ──
Bản đầu làm đúng một việc: cắt chữ " a " ra khỏi câu mẫu, và dán một lời giải thích
GHIM CỨNG về mạo từ. Hỏng hai đường, và hỏng nặng:

  · 10 trên 16 bài không có chữ " a " trong câu, nên phép cắt KHÔNG làm gì — câu
    "sai" trùng hệt câu đúng. Bé được cho xem một câu HOÀN TOÀN ĐÚNG rồi bảo là
    thiếu chữ. Dạy ngược.
  · cả 16 bài dùng chung lời giải thích lấy ví dụ "This is a dog", kể cả bài đang
    dạy "I have a car" hay "Hi, I'm Bill" — bé nghe một đằng, đọc một nẻo.

Không cổng nào bắt được: JSON hợp lệ, màn hình vẽ đủ, tiếng vẫn đọc. Bác nghe ra khi
mở Unit 1 và thấy máy đọc "Hi, I'm Bill." còn chữ bên dưới nói về "con chó".

── LUẬT CỦA BẢNG ──
Mỗi mục là (nhận ra được không, dựng câu sai, giải thích). Giải thích PHẢI dựng từ
CHÍNH câu ấy, không được có ví dụ nào khác. Không mục nào khớp thì TRẢ VỀ None —
thà bài không có khối "chỗ dễ nhầm" còn hơn có một khối dạy sai.
"""


def _co(cau, tu, vai):
    """Từ đầu tiên trong câu mang vai này — để lời giải thích gọi đúng tên nó."""
    for t in tu:
        if vai in (t.get("vai") or []) and t["tu"].lower() in cau.lower():
            return t
    return None


def cho_de_nham(cau: str, tu: list[dict]) -> dict | None:
    """Trả về {wrong, right, why} hoặc None. Xếp theo độ HẸP: luật hẹp chạy trước,
    vì luật rộng (mạo từ) khớp gần như mọi câu và sẽ cướp chỗ."""
    d = cau
    XAC_DINH = ("my ", "your ", "the ", "a ", "an ")     # đã có từ hạn định

    # 1 · TÍNH TỪ ĐỨNG SAU DANH TỪ — lỗi đặc trưng nhất, tiếng Việt xếp ngược.
    mau = _co(d, tu, "mau")
    if mau:
        dt = next((t for t in tu if "dt" in (t.get("vai") or [])
                   and t["tu"].lower() in d.lower() and t["tu"] != mau["tu"]), None)
        if dt and f"{mau['tu']} {dt['tu']}" in d:
            return {
                "wrong": d.replace(f"{mau['tu']} {dt['tu']}", f"{dt['tu']} {mau['tu']}"),
                "right": d,
                "why": f"Tiếng Việt nói “{dt['nghia']} {mau['nghia'].replace('màu ', '')}” — "
                       f"màu đứng SAU. Tiếng Anh thì ngược lại, màu đứng TRƯỚC: "
                       f"“{mau['tu']} {dt['tu']}”.",
            }

    # 2 · CÂU RA LỆNH BỊ THÊM CHỦ NGỮ — tiếng Việt hay giữ “con/bạn”.
    #     Phải đứng TRƯỚC luật danh từ không đếm được, nếu không "Touch your hair."
    #     bị luật ấy chèn mạo từ vào giữa và ra "Touch your a hair." — một câu
    #     không người học nào viết, tức là dạy một lỗi KHÔNG CÓ THẬT.
    for lenh in ("Touch ", "Point ", "Look "):
        if d.startswith(lenh):
            return {
                "wrong": "You " + d[0].lower() + d[1:], "right": d,
                "why": f"Câu ra lệnh trong tiếng Anh KHÔNG có chủ ngữ — bắt đầu thẳng "
                       f"bằng “{d.split()[0]}”. Thêm “You” vào là thành câu kể, "
                       f"không còn là lời bảo nữa.",
            }

    # 3 · THÊM MẠO TỪ VÀO DANH TỪ KHÔNG ĐẾM ĐƯỢC — lỗi ngược của lỗi mạo từ.
    #     CHỈ khi danh từ ấy đang đứng trần: có "my/your/the" đằng trước thì chèn
    #     "a" vào là ra câu vô nghĩa, không phải lỗi thật.
    kd = _co(d, tu, "khongdem")
    if kd:
        truoc = d[:d.lower().index(kd["tu"].lower())]
        tran = not any(truoc.rstrip().endswith(x.strip()) for x in XAC_DINH)
        if tran and f" {kd['tu']}" in d:
            return {
                "wrong": d.replace(f" {kd['tu']}", f" a {kd['tu']}", 1), "right": d,
                "why": f"“{kd['tu']}” là thứ KHÔNG đếm được — không ai nói “một "
                       f"{kd['nghia']}”. Nên trước nó không có “a”.",
            }

    # 4 · (ĐÃ BỎ) QUÊN “s” SỐ NHIỀU.
    #     Bác chốt: lớp 1 CHƯA dạy số ít / số nhiều, để bài khác dạy. Nhắc “s” ở
    #     đây chỉ thêm một thứ bé chưa cần mà lại rối. Luật cũ từng nhận U9, U13,
    #     U16 — nay U13 rơi sang luật “to be” (đúng thứ đang dạy), còn U9 và U16
    #     không luật nào khớp thì KHÔNG dựng khối, đúng nguyên tắc thà thiếu còn
    #     hơn dạy sai.

    # 5 · BỎ MẤT ĐỘNG TỪ “to be” — tiếng Việt lược “là/đang” ở chỗ tiếng Anh bắt buộc.
    #     Lời giải thích dựng TỪ CHÍNH CÂU ẤY: bản đầu ghim cứng ví dụ "Bạn ấy đang
    #     chạy" nên bài "There's a garden." cũng bị giải thích bằng câu chạy.
    for rut in ("'s ", "'re ", "'m "):
        if rut in d:
            day = {"'s ": "is", "'re ": "are", "'m ": "am"}[rut]
            thieu = d.replace(rut, " ", 1).replace("  ", " ")
            return {
                "wrong": thieu, "right": d,
                "why": f"Câu này bắt buộc phải có “{day}”, viết rút thành “{rut.strip()}”. "
                       f"Tiếng Việt bỏ được chỗ ấy, tiếng Anh thì không: "
                       f"“{thieu}” là câu chưa đủ.",
            }
    # 6 · BỎ MẤT MẠO TỪ “a/an” — hay gặp nhất, để CUỐI vì nó khớp rộng nhất.
    for mt in (" an ", " a "):
        if mt in d:
            dt = next((t for t in tu if t["tu"].lower() in d.lower()
                       and "dt" in (t.get("vai") or [])), None)
            ten = f"“{dt['nghia']}”" if dt else "vật ấy"
            return {
                "wrong": d.replace(mt, " ", 1), "right": d,
                "why": f"Tiếng Việt nói {ten} là xong — không có chữ nào như “a”. "
                       f"Tiếng Anh thì bắt buộc: “{d}”. Thiếu “a” là câu sai.",
            }

    # 7 · BỎ MẤT “is/are” VIẾT ĐẦY ĐỦ.
    #     Để SAU luật mạo từ: câu có cả " is " lẫn " a " (như "This is a dog.") thì
    #     mạo từ là bài đáng dạy hơn, vì chính mẫu câu của unit ấy dạy chữ "a".
    #     Lời giải thích dựng từ CHÍNH câu này — bản trước ghim ví dụ “cái túi” nên
    #     bài dạy con chó cũng bị giải thích bằng cái túi, đúng lỗi bác đã chỉ.
    for tb in (" is ", " are "):
        if tb in d:
            thieu = d.replace(tb, " ", 1)
            return {
                "wrong": thieu, "right": d,
                "why": f"Thiếu “{tb.strip()}”. Câu “{thieu}” nghe vẫn đoán ra nghĩa, "
                       f"nhưng tiếng Anh bắt buộc phải có “{tb.strip()}”: “{d}”.",
            }

    # Không luật nào khớp → KHÔNG dựng khối. Thà thiếu còn hơn dạy sai.
    return None

def sat_hach(u: dict, cau: list) -> list:
    """Năm câu đúng/sai.

    ĐÁP ÁN PHẢI XEN KẼ. Bản đầu xếp ba câu ĐÚNG rồi hai câu SAI, và thế là bé qua
    được kỳ sát hạch bằng cách đoán theo NHỊP chứ không cần biết nghĩa từ nào —
    kỳ sát hạch mà đoán được thì sổ bố mẹ và bảng cô giáo đang báo một con số rỗng.
    """
    tu = [t for t in u["tu"] if t.get("nghia")]
    if len(tu) < 2:
        return []
    dung, sai = [], []

    for t in tu[:3]:
        dung.append((f"“{t['tu']}” nghĩa là “{t['nghia']}”.", "Đáp án: ĐÚNG"))
    # Ghép chéo: từ thứ i với nghĩa của từ kế tiếp. Mồi sai kiểu này buộc bé phải
    # nhớ ĐÚNG cặp, không đoán được bằng "nghe quen quen".
    for i, t in enumerate(tu[:2]):
        khac = tu[(i + 1) % len(tu)]
        sai.append((f"“{t['tu']}” nghĩa là “{khac['nghia']}”.",
                    f"SAI — “{t['tu']}” nghĩa là “{t['nghia']}”."))
    if cau:
        c = cau[0]
        sai.append((f"Câu “{c['cau'].replace(' a ', ' ', 1)}” viết đúng chưa?",
                    f"SAI — thiếu chữ “a”. Phải là “{c['cau']}”."))
        dung.append((f"Câu “{c['cau']}” viết đúng chưa?", "Đáp án: ĐÚNG"))

    # xen kẽ Đ · S · Đ · S · Đ
    ra, i = [], 0
    while len(ra) < 5 and (dung or sai):
        kho, gt = (dung, True) if i % 2 == 0 else (sai, False)
        if not kho:
            kho, gt = (sai, False) if gt else (dung, True)
        if not kho:
            break
        text, loi = kho.pop(0)
        ra.append({"id": f"Q{len(ra) + 1}", "text": text, "format": "tf",
                   "answerKey": {"value": gt}, "solutionNarrative": loi})
        i += 1
    return ra


def _tach_mau(m: dict) -> list[dict]:
    """Một mẫu câu → một hoặc hai mục (hỏi / đáp)."""
    def goi(d, nhan, cau_goc):
        return {"cau": d["cau"], "congThuc": m.get("cong_thuc"),
                "dungDe": d.get("dung_de"), "tinhHuong": d.get("tinh_huong"),
                "phan": d.get("phan") or [], "khacVoi": d.get("khac_voi"),
                "vai": nhan, "capVoi": cau_goc}
    if m.get("hoi") and m.get("dap"):
        return [goi(m["hoi"], "hoi", m["dap"]["cau"]),
                goi(m["dap"], "dap", m["hoi"]["cau"])]
    if not m.get("dung_de"):
        return []
    return [{"cau": m.get("vi_du"), "congThuc": m.get("cong_thuc"),
             "dungDe": m.get("dung_de"), "tinhHuong": m.get("tinh_huong"),
             "phan": m.get("phan") or [], "khacVoi": m.get("khac_voi"),
             "vai": "cau", "capVoi": None}]


def dung_bai(u: dict, lop: int, truoc: str | None, sau: str | None,
              them: dict, sua_slot: dict, chuong: dict) -> dict:
    ph = u.get("phonics") or {}
    tu = [t for t in u["tu"] if t.get("nghia")]
    warmup, standard, challenge, cau = cau_hoi(u, lop, them, sua_slot)
    chu = (ph.get("chu") or "?")
    am = ph.get("am") or ""
    ma_bai = f"{TIEN_TO[lop]}B{u['so']:02d}"
    ch_so = next((int(k) for k, v in chuong.items() if u["so"] in (v.get("unit") or [])),
                 (u["so"] - 1) // 4 + 1)

    # ── LỜI GIẢNG ──
    # Mỗi khối có HAI thứ, cố ý tách đôi:
    #   `text`  — chữ HIỆN LÊN màn hình. Được phép lẫn tiếng Anh, vì bé NHÌN thấy
    #             chữ tiếng Anh là chuyện bình thường và cần thiết.
    #   `doanAm`— chữ ĐỌC LÊN, cắt thành đoạn, MỖI ĐOẠN MỘT THỨ TIẾNG.
    #
    # Không tách đôi thì ra đúng dòng "Cảnh hôm nay: In the bedroom." — Kokoro-VI
    # đọc "In the bedroom" theo vần Việt. Lỗi ấy đã xảy ra thật ở bản đầu của tệp
    # này, và cổng tienganh_am.test.mjs giữ nó lại làm phép kiểm vĩnh viễn.
    #
    # Chữ cái và IPA (Dd · /d/) KHÔNG đưa vào phần đọc: bác chốt bỏ phần âm phonics
    # rời. Âm ấy dạy QUA TỪ VÍ DỤ ở K2 — cũng là cách dạy phonics đúng hơn, vì âm
    # /d/ tách khỏi từ thì không tồn tại trong lời nói tự nhiên.
    ba = " · ".join(t["tu"] for t in tu[:3])
    K = [
        {"id": "K1",
         "text": f"Hôm nay chúng mình học chữ {chu}. Chữ {chu} đọc là {am}.",
         "doanAm": [("Hôm nay chúng mình học một chữ cái mới. Con nhìn lên bảng nhé.", "vi")]},
        {"id": "K2",
         "text": f"Nghe ba từ này: {ba}. Con có nghe thấy chúng bắt đầu giống nhau "
                 f"không? Đó chính là âm {am} của chữ {chu}.",
         "doanAm": [("Nghe ba từ này.", "vi")]
                   + [(t["tu"], "en") for t in tu[:3]]
                   + [("Con có nghe thấy ba từ này bắt đầu giống nhau không? "
                       "Đó chính là âm của chữ hôm nay.", "vi")]},
        {"id": "K3",
         "text": "Từ mới của bài: "
                 + " · ".join(f"{t['tu']} {t['ipa']} = {t['nghia']}" for t in tu),
         "doanAm": [("Từ mới của bài.", "vi")]
                   + [x for t in tu for x in ((t["tu"], "en"), (t["nghia"], "vi"))]},
    ]
    if u["mau_cau"]:
        mc = u["mau_cau"][0]
        # ── DẠY VIỆC TRƯỚC, DẠY CÂU SAU ──
        # Bản đầu chỉ hiện công thức và một ví dụ. Bé học thuộc "Bye, Mai." xong
        # không biết nói lúc nào — chỉ là một chuỗi âm phải nhớ. Nên K4 nay trả lời
        # đúng câu bé cần: NÓI CÂU NÀY ĐỂ LÀM GÌ, và trong cảnh nào.
        if mc.get("dung_de"):
            K.append({
                "id": "K4",
                "text": f"Câu hôm nay dùng để: {mc['dung_de']} "
                        f"Ví dụ: {mc['tinh_huong']}",
                "doanAm": [(f"Câu hôm nay dùng để {mc['dung_de'].lower()} "
                            f"{mc['tinh_huong']}", "vi")],
            })
        K.append({
            "id": "K5" if mc.get("dung_de") else "K4",
            "text": f"Mẫu câu: {mc['cong_thuc']} — ví dụ: {mc['vi_du']}",
            "doanAm": [("Con nghe mẫu câu rồi nhắc lại nhé.", "vi"),
                       (mc["vi_du"], "en")],
        })

    man = [{"id": "S1", "kind": "hook",
            "narration": f"Cảnh hôm nay: {u['canh']}.",
            "doanAm": [(f"Cảnh hôm nay: {u['canh']}.", "vi")]}]
    man += [{"id": f"S{i + 2}", "kind": "explain", "narration": "", "teaches": [k["id"]]}
            for i, k in enumerate(K)]

    # ── CHỖ DỄ NHẦM ──
    # Không nhân vật nào nói câu sai; câu sai đứng một mình và bé tự nhận ra.
    nham = cho_de_nham(cau[0]["cau"], tu) if cau else None
    if nham:
        man.append({
            "id": f"S{len(man) + 1}", "kind": "trap", "teaches": [],
            # Lời dẫn KHÔNG được nói "thiếu một chữ": có luật thêm chữ (mạo từ vào
            # danh từ không đếm được), có luật đảo chỗ (màu đứng sau danh từ). Nói
            # chung chung "có một chỗ chưa đúng" thì đúng với mọi luật.
            "narration": f"Nghe câu này: {nham['wrong']} — câu này có một chỗ chưa "
                         f"đúng. Con nghe lại rồi tìm xem sai ở đâu nhé.",
            "doanAm": [("Nghe câu này.", "vi"),
                       (nham["wrong"], "en"),
                       ("Câu vừa rồi có một chỗ chưa đúng. Con nghe lại câu đúng nhé.", "vi"),
                       (nham["right"], "en")],
        })

    return {
        "$schema": "digital-lesson/v2-micro",
        "id": ma_bai,
        "grade": lop,
        "quyen": QUYEN[lop],
        "mon": "tienganh",
        "title": f"Unit {u['so']} · {u['canh']}",
        "durationMinutes": 10,
        "so": u["so"],
        # Chương lấy TỪ SÁCH (4 chương × 4 unit), không phải "mỗi unit một chương".
        # Cổng kesach đòi mỗi chương một kỳ ôn tập; khai 16 chương là đòi 16 kỳ ôn.
        "chuong": ch_so,
        "tenChuong": (chuong.get(str(ch_so)) or {}).get("ten") or f"Chương {ch_so}",
        "dangGoc": f"{chu} {am} · {u['chu_de']}",
        # Khoá BKT phải kèm mã quyển, không thì huy hiệu lây sang quyển khác.
        "skills": {"bktUnit": f"UNIT:{u['so']}@{QUYEN[lop].upper()}", "primary": []},
        "series": {"order": u["so"], "prev": truoc, "next": sau},
        "objective": {
            "id": "O1",
            "text": " ".join(u["nang_luc"]) or f"Học chữ {chu} và {len(tu)} từ mới.",
            "kidText": f"Học chữ {chu}, {len(tu)} từ mới, và một mẫu câu. "
                       f"Xong bài con nghe hiểu, nói theo và gõ lại được.",
            "passRule": "đúng ≥ 4/5 câu sát hạch",
        },
        "knowledgeCore": {
            "statements": K,
            "mantra": f"Nghe — hiểu — xếp — gõ. Bốn bước, cùng {len(tu)} từ ấy thôi.",
            "vocabulary": [{"tu": t["tu"], "ipa": t["ipa"], "nghia": t["nghia"],
                            "am": am_id("tu", t["tu"]), "amO": t.get("am_o", "dau")}
                           for t in tu],
            "canonicalExamples": [c["cau"] for c in cau],
            # MỌI mẫu câu của bài, mỗi cái đủ phần dạy. Bản đầu chỉ mang mẫu ĐẦU
            # TIÊN, nên U1 (Hi/Bye), U11 (She's/He's) và U13 mất hẳn mẫu thứ hai —
            # mà chính hai mẫu ấy mới dạy được chỗ khác nhau.
            # Mẫu câu KIỂU HỎI–ĐÁP ("How many clocks? - Two.") tách thành HAI mục:
            # một câu hỏi, một câu trả lời. Đó là hai cấu trúc khác nhau dán bằng
            # dấu gạch, và bé lớp 1 phải học hỏi cho thuộc rồi mới sang đáp.
            "mauCauDs": [x for m in u["mau_cau"] for x in _tach_mau(m)],
            # Giữ `mauCau` trỏ vào mẫu ĐẦU cho màn hình hiện tại — đổi cả giao diện
            # cùng lúc là hai việc trộn vào nhau.
            "mauCau": ({
                "cau": u["mau_cau"][0].get("vi_du"),
                "congThuc": u["mau_cau"][0].get("cong_thuc"),
                "dungDe": u["mau_cau"][0].get("dung_de"),
                "tinhHuong": u["mau_cau"][0].get("tinh_huong"),
                "phan": u["mau_cau"][0].get("phan") or [],
                "khacVoi": u["mau_cau"][0].get("khac_voi"),
            } if u["mau_cau"] else None),
            "misconceptions": [nham] if nham else [],
        },
        "lecture": {"screens": man},
        "workedExample": {
            "title": "Bài mẫu",
            "problem": cau[0]["cau"] if cau else tu[0]["tu"],
            "steps": ([
                {"show": f"Nghe cả câu: {cau[0]['cau']}", "phan": "giai"},
                {"show": "Tách ra từng thẻ: " + " | ".join(cau[0]["cau"].split()),
                 "phan": "giai"},
                {"show": f"Chữ cuối là “{cau[0]['tu']['tu']}” — {cau[0]['tu']['nghia']}. "
                         f"Đổi chữ ấy là được câu mới.", "phan": "giai"},
            ] if cau else []),
        },
        "practice": {"pools": {"warmup": warmup, "standard": standard,
                               "challenge": challenge}},
        "assessment": {"passRule": "≥ 4/5", "items": sat_hach(u, cau)},
        "parentNote": {
            # CHỈ dùng mẫu câu bài này đã dạy. Bản đầu bảo bố mẹ hỏi "What's this?"
            # — mẫu câu ấy tận lớp 2 mới học, bé lớp 1 nghe xong đứng im, và bố mẹ
            # tưởng con chưa thuộc bài.
            "onComplete": (f"Chỉ vào đồ trong nhà rồi nói mẫu câu bài này: "
                           f"“{cau[0]['cau']}” — cho con nhắc lại. Đổi chữ cuối để "
                           f"thành đồ khác." if cau else
                           "Chỉ vào đồ trong nhà và cho con gọi tên bằng tiếng Anh."),
            "homeActivity": f"Tìm trong nhà những thứ bắt đầu bằng âm {am}. "
                            "Không cần đúng hết, quan trọng là con nghe ra âm ấy.",
            "watchFor": "NÊN: cho con NGHE trước rồi mới nhìn chữ. "
                        "KHÔNG NÊN: bắt con đánh vần theo kiểu tiếng Việt — "
                        "tiếng Anh viết một đằng đọc một nẻo, đánh vần sẽ hại.",
        },
        # Hình từ vựng KHÔNG dùng figureSpec/figforge như bốn quyển Toán: figforge
        # chỉ dựng sơ đồ toán, không vẽ được con vịt (xem lop1_bu.json mục `hinh`).
        # Đợt 1 hình là EMOJI, nên nó đi thẳng cùng từ chứ không phải một tệp PNG
        # rời — không có gì để render, không có manifest để lệch.
        "hinhTu": [{"tu": t["tu"], "hinh": t.get("hinh"), "ve": t.get("hinh_ve"),
                    "no": True if t.get("hinh_no") else None} for t in tu],
    }


def loi_can_doc(bai: dict) -> list[dict]:
    """Danh sách dòng cần sinh âm. MỖI DÒNG MỘT THỨ TIẾNG — xem tools/tts/README.md.

    Đọc từ `doanAm` chứ KHÔNG từ `narration`: `narration` là chữ hiện lên màn hình
    và được phép lẫn tiếng Anh, `doanAm` mới là thứ đem đi đọc. Lẫn hai thứ này là
    ra clip đọc "In the bedroom" bằng giọng Việt.
    """
    ra, thay = [], set()

    def them(loai, chu, tieng):
        i = am_id(loai, chu)
        if i not in thay:
            thay.add(i)
            ra.append({"id": i, "chu": chu, "tieng": tieng})

    for v in bai["knowledgeCore"]["vocabulary"]:
        them("tu", v["tu"], "en")
        them("nghia", v["nghia"], "vi")
    for c in bai["knowledgeCore"]["canonicalExamples"]:
        them("cau", c, "en")
    for khoi in list(bai["lecture"]["screens"]) + list(bai["knowledgeCore"]["statements"]):
        for chu, tieng in khoi.get("doanAm") or []:
            them("loi" if tieng == "vi" else "cau", chu, tieng)
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=1, choices=[1, 2, 3])
    p.add_argument("--unit", type=int)
    p.add_argument("--tat-ca", action="store_true")
    a = p.parse_args()

    chuan = json.loads((GOC / f"data/tienganh/chuan_lop{a.lop}.json").read_text("utf8"))
    units = chuan["unit"]
    if not a.tat_ca:
        if a.unit is None:
            p.error("cần --unit N hoặc --tat-ca")
        units = [u for u in units if u["so"] == a.unit]
        if not units:
            print(f"✗ lớp {a.lop} không có unit {a.unit}", file=sys.stderr)
            return 1

    # Ghi THẲNG ra bản dựng. Bốn quyển Toán có `data/lopN/` là bản gốc viết tay
    # rồi mới dựng sang `public/content/lopN/`; tiếng Anh KHÔNG có sách viết tay —
    # nguồn là bản đồ + `data/tienganh/lopN_bu.json` + chính tệp này. Đẻ thêm một
    # bản trung gian ở `data/ta1/` chỉ tạo ra một nơi nữa phải đồng bộ tay, mà
    # "ba nơi phải đồng bộ" đã là cái bẫy quen thuộc của kho này rồi.
    tm = GOC / f"web/public/content/{QUYEN[a.lop]}"
    tm.mkdir(parents=True, exist_ok=True)
    tat = chuan["unit"]
    moi_loi = []
    for u in units:
        i = tat.index(u)
        truoc = f"{TIEN_TO[a.lop]}B{tat[i - 1]['so']:02d}" if i > 0 else None
        sau = f"{TIEN_TO[a.lop]}B{tat[i + 1]['so']:02d}" if i + 1 < len(tat) else None
        bai = dung_bai(u, a.lop, truoc, sau, chuan.get("them") or {},
                       chuan.get("sua_slot") or {}, chuan.get("chuong") or {})
        ten = f"DL_{QUYEN[a.lop].upper()}_B{u['so']:02d}.json"
        (tm / ten).write_text(json.dumps(bai, ensure_ascii=False, indent=1), "utf8")
        moi_loi += loi_can_doc(bai)
        po = bai["practice"]["pools"]
        print(f"Unit {u['so']:2d} · {u['canh'][:34]:34s} → {ten}  "
              f"★{len(po['warmup']):2d} ★★{len(po['standard']):2d} "
              f"★★★{len(po['challenge']):2d} · sát hạch {len(bai['assessment']['items'])}")

    # gộp trùng: từ `dog` xuất hiện ở nhiều bài chỉ sinh MỘT clip
    theo_id = {}
    for m in moi_loi:
        theo_id.setdefault(m["id"], m)
    tep_loi = GOC / f"data/tienganh/lop{a.lop}_loi.json"
    tep_loi.write_text(json.dumps(list(theo_id.values()), ensure_ascii=False, indent=1), "utf8")
    print(f"\n{len(theo_id)} dòng cần sinh âm → {tep_loi.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
