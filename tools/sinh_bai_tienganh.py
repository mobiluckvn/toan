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
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3", 4: "ta4", 5: "ta5"}
TIEN_TO = {1: "DL:TA1.", 2: "DL:TA2.", 3: "DL:TA3.", 4: "DL:TA4.", 5: "DL:TA5."}

# Gõ được thì gõ; dài hơn ngần này thì bậc 4 chuyển sang GHÉP THẺ CHỮ CÁI.
# Bé 6 tuổi gõ ~10 ký tự/phút — từ 10 ký tự là bỏ cuộc chứ không phải làm sai.
GO_TOI_DA = 5
# Ô gõ CẢ CÂU. Trùng ngưỡng của `tienganh_bai.test.mjs` — hai bên lệch nhau thì bộ
# sinh đẻ ra thứ cổng không nhận, mà không ai biết cho tới lúc chạy cổng.
GO_CAU_TOI_DA = 46
DAN_DIEN = "Nhìn hình rồi chọn từ điền vào chỗ trống."
# Ô trống là TÊN NGƯỜI (`Hi, I'm + [Name].`) thì không có hình nào vẽ được, mà câu
# vẫn dùng tốt — manh mối nằm ở chính câu. Bảo bé "nhìn hình" khi không có hình là
# nói dối bé, và bé sáu tuổi sẽ ngồi tìm cái không có. 15 câu từng như thế.
DAN_DIEN_KHONG_HINH = "Chọn từ điền vào chỗ trống."
THE_TOI_DA = 5          # trùng THE_TOI_DA của mon/tienganh/lib/cham.js


def canh_doc(u: dict) -> str:
    """Phần TIẾNG VIỆT của tên cảnh — dùng cho lời đọc và mọi câu tiếng Việt.

    Tên cảnh từ lớp 2 là song ngữ, ngăn bằng " · ". Tên để nhìn thì cần cả hai;
    giọng đọc tiếng Việt thì chỉ đọc được vế đầu.
    """
    return (u.get("canh") or "").split(" · ")[0].strip()


def am_id(loai: str, khoa: str) -> str:
    """Mã clip âm. Dùng chung giữa các bài: từ `dog` chỉ sinh MỘT lần cho cả quyển."""
    sach = "".join(c if c.isalnum() else "_" for c in khoa.lower()).strip("_")
    return f"{loai}_{sach}"[:60]


def tu_ipa(t: dict) -> str:
    """“hello /həˈləʊ/”, hoặc chỉ “Lucy” khi từ không có phiên âm.

    ⚠ Ghép thẳng bằng f-string là chỗ đã lọt lỗi thật: 8 tên riêng của lớp 3 (`Ben` ·
    `Lucy` · `Ms Hoa`…) không có IPA — mà tên riêng thì đúng là không cần — nên lời
    giải hiện lên màn hình thành “Ben None — bạn Ben”. Bốn chỗ cùng ghép một kiểu,
    nên gom về một hàm; chỗ nào tự ghép lại là chỗ ấy sẽ hiện `None` lần nữa.
    """
    return " ".join(str(x) for x in (t.get("tu"), t.get("ipa")) if x)


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
    # ⚠ VIẾT HOA LÀ CHUYỆN CỦA VỊ TRÍ, VÀ CỦA TỪNG LẦN XUẤT HIỆN.
    #
    # Bản cũ giữ MỘT cờ hoa cho mỗi ô, bật theo mặt chữ của từ neo trong câu SGK.
    # Hai chỗ sai cùng lúc:
    #   · "Snow White" viết hoa vì là TÊN RIÊNG, không phải vì đứng đầu câu — cờ
    #     ấy áp cho mọi từ điền sau và ra "They're The ant and the grasshopper.";
    #   · lớp 2 U5 có ô [Pronoun] xuất hiện HAI lần, một lần giữa câu một lần đầu
    #     câu ("What's [Pronoun] doing? - [Pronoun] is doing a quiz.") — một cờ
    #     thì hoặc hỏng chỗ này hoặc hỏng chỗ kia.
    #
    # Nên quyết ngay tại chỗ điền: ô nào NẰM ĐẦU MỘT CÂU thì viết hoa, còn lại
    # giữ nguyên mặt chữ của từ (tên riêng tự giữ chữ hoa của chính nó).
    for o, w in gan.items():
        dat = f"[{o}]"
        while dat in s:
            i = s.index(dat)
            truoc = s[:i].rstrip()
            dau_cau = (not truoc) or truoc[-1] in ".?!-:"
            x = (w[:1].upper() + w[1:]) if (dau_cau and w) else w
            s = s[:i] + x + s[i + len(dat):]
    return _chon_mao_tu(s)


def _chon_mao_tu(cau: str) -> str:
    """`a/an elephant` → `an elephant`; `a/an book` → `a book`.

    Bản đồ lớp 3 viết `a/an` ở BẢY công thức, để người soạn tự chọn. Máy điền thẳng
    thì ra "I can see a/an elephant." — bé đọc lên không biết đọc thế nào, và dấu
    gạch chéo giữa câu là thứ không ai nói ra miệng.
    Chọn được bằng MÁY vì luật rõ: chữ cái đầu của từ ngay sau là nguyên âm thì "an".
    Lớp 1·2 không có ca này nên bản cũ chưa cần.
    """
    def thay(m):
        sau = m.group(1)
        return ("an " if sau[:1].lower() in "aeiou" else "a ") + sau
    return re.sub(r"\ba/an\s+(\S+)", thay, cau)


def dang_can(o_ten: str, t: dict) -> str | None:
    """Ô đòi DẠNG nào của từ — suy từ chính tên ô trong công thức.

    Bản đồ cho từ ở dạng GỐC (`run`, `window`) còn câu cần dạng biến đổi
    (`running`, `windows`). Ghép thẳng thì ra "She's run." — xem lop1_bu.json.

    ⚠ SO TÊN Ô KHÔNG PHÂN BIỆT HOA THƯỜNG. Lớp 1 viết `[Noun-plural]`, lớp 2 viết
    `[Plural Noun]` — cùng một ý, khác cách gọi. Bản đầu so `"plural" in o_ten` nên
    lớp 2 trượt hết: `grape` điền nguyên dạng gốc vào ô số nhiều, ra
    "The grape are on the table." Cùng dòng họ với bảng khuôn lệch §0 của sổ dây
    chuyền — ba lớp không ai gọi giống ai.
    """
    ten = (o_ten or "").lower()
    if "verb-ing" in ten or "verb ing" in ten:
        return t.get("dang_ing")
    # ⚠ QUÁ KHỨ — lớp 5 mới có. Bốn mẫu viết ô là `[past verb]`. Không bắt ở đây
    # thì rơi xuống `return t["tu"]` cuối hàm, và bộ sinh lặng lẽ đẻ ra
    # "We visit the old buildings last summer." Trả None khi thiếu dạng: bên gọi
    # LOẠI TỪ ẤY KHỎI KHO chứ không điền bừa — xem [[bo-sinh-lui-ve-mac-dinh]].
    if "past" in ten:
        return t.get("dang_qk")
    if "plural" in ten:
        return t.get("so_nhieu") or (t["tu"] if "sonhieu" in (t.get("vai") or []) else None)
    return t["tu"]


# Những chữ được hiểu là VAI chứ không phải là một từ tiếng Anh. Khai ở `sua_slot`
# mà không nằm trong danh sách này thì hiểu là TÊN TỪ đích danh.
#
# ⚠ SUY TỪ CHÍNH DỮ LIỆU, ĐỪNG GHIM CỨNG. Bản đầu liệt kê 13 vai của lớp 1·2. Lớp 3
# khai thêm 13 vai mới (convat · soluong · dodac · tinhtu · noichon · nghe · sothich
# …), và vì chúng không có tên trong danh sách nên `sua_slot` của lớp 3 bị hiểu nhầm
# là DANH SÁCH TỪ: kho ứng viên rỗng, `sinh_cau` bỏ qua cả mẫu, im lặng. U16 mất
# sạch bậc 3 vì đúng chuyện này.
VAI_GOC = {"dt", "dongtu", "mau", "bophan", "thucan", "sonhieu", "khongdem",
           "so", "ten", "daitu", "giadinh", "vitri", "cumdongtu"}


def vai_biet(tu: list, them: dict) -> set:
    """Mọi tên vai CÓ THẬT trong quyển này — gom từ chính `vai` của từng từ."""
    ra = set(VAI_GOC)
    for t in tu:
        ra.update(t.get("vai") or [])
    for nhom, goi in (them or {}).items():
        if nhom.startswith("_") or not isinstance(goi, dict):
            continue
        for x in (goi.get("muc") or []):
            if isinstance(x, dict):
                ra.update(x.get("vai") or [])
    return ra


def ung_vien_tat(tu: list, them: dict) -> list[dict]:
    """Mọi ứng viên có thể, không lọc vai — để lọc lại bằng danh sách từ đích danh."""
    return ung_vien(sorted(vai_biet(tu, them)), tu, them)


def ung_vien(vai_can: list, tu: list, them: dict) -> list[dict]:
    """Những từ được phép điền vào một ô, theo VAI đã khai ở `lopN_bu.json`.

    ⚠ Bản đầu ghim cứng ba nhóm `so_dem` · `mau` · `ten` — đúng ba nhóm lớp 1 có.
    Lớp 2 khai thêm `dai_tu` · `dong_tu_phu` · `cum_dong_tu` cho sáu mẫu câu có ô
    [Pronoun] · [Verb] · [Verb-ing] · [Verb phrase], và cả sáu **rơi im lặng**: kho
    ứng viên rỗng → `sinh_cau` bỏ qua cả mẫu, không báo gì, cổng vẫn xanh.

    Nay duyệt MỌI nhóm trong `them`. Thêm nhóm mới ở phần bù là chạy được ngay,
    không phải nhớ sửa thêm một danh sách ở đây — đúng luật "thêm quyển mới không
    phải sửa bộ sinh" của §5 sổ dây chuyền.
    """
    kho = list(tu)
    for nhom, goi in them.items():
        if nhom.startswith("_") or not isinstance(goi, dict):
            continue
        for m in (goi.get("muc") or []):
            kho.append({"tu": m["word"] if isinstance(m, dict) else m,
                        "nghia": m.get("nghia", "") if isinstance(m, dict) else "",
                        "ipa": m.get("ipa", "") if isinstance(m, dict) else "",
                        "vai": m.get("vai", ["ten"]) if isinstance(m, dict) else ["ten"],
                        "ma": f"them_{nhom}_{m if isinstance(m, str) else m['word']}",
                        # Mang theo DẠNG BIẾN ĐỔI. Thiếu hai dòng này thì động từ phụ
                        # vào ô [Verb-ing] ở dạng gốc: "Is he fly a kite?" — đã thấy thật.
                        "dang_ing": m.get("dang_ing") if isinstance(m, dict) else None,
                        "so_nhieu": m.get("so_nhieu") if isinstance(m, dict) else None,
                        "go_duoc": True})
    return [t for t in kho if set(t.get("vai") or []) & set(vai_can)]


def cum_khai(khai: list, da_co: list, ma_mau: str, o: str) -> list[dict]:
    """Mục khai trong `sua_slot` là một CỤM, không phải một từ trong bảng từ vựng.

    ══ VÌ SAO CẦN ══ (bác chốt 19-08-2026)

    Bản đồ khai ô `[Activity]` của lớp 3 unit 10 bằng đúng tên mấy môn thể thao:

        o_thay: chat · badminton · basketball · chess · football · …

    Sách hiểu ngầm là "play + môn", nhưng bản đồ không ghi chữ "play" ở đâu cả. Nên
    bộ sinh điền thẳng và đẻ ra:

        ✗  I badminton at break time.
        ✗  What do you do at break time? - I basketball.

    Câu không có động từ. Không cổng nào bắt được: mọi CHỮ đều là từ đã học, khuôn
    thì khớp công thức, và máy thì không biết "badminton" là danh từ.

    Ô kiểu ấy cần một CỤM ("play badminton"), mà cụm thì không phải một mục trong
    bảng từ vựng — nên nhánh "danh sách từ đích danh" ở trên tra không ra và bỏ hết.

    ⚠ CHỈ NHẬN MỤC NHIỀU CHỮ. Mục một chữ mà tra không ra thì đó là GÕ NHẦM tên từ,
    không phải cụm — và gõ nhầm phải kêu lên chứ không được lặng lẽ thành một chuỗi
    tự do. Đây là chỗ dễ nuốt lỗi nhất của cả tệp này.

    Mọi chữ trong cụm vẫn phải là từ ĐÃ HỌC — cổng `tienganh_bai` phép 2 soi lại
    trên tệp đã ghi, nên khai bừa một chữ lạ thì đỏ ngay.
    """
    co = {t["tu"] for t in da_co}
    ra = []
    for x in khai:
        # ⚠ MỤC CỤM CÓ THỂ KHAI KÈM DẠNG. Lớp 5 U17 cần đúng chuyện này: câu hỏi
        # dùng động từ TRẦN ("How did she cook?") còn câu đáp dùng CỤM QUÁ KHỨ
        # ("She cooked very well."). Hai ô ấy phải là MỘT mục (để `cung_tu` nối
        # được), nhưng hiện ra hai mặt chữ khác nhau — nên mục khai được là
        # {"tu": "cook", "dang_qk": "cooked well"}.
        dang = {}
        if isinstance(x, dict):
            dang = {k: v for k, v in x.items() if k != "tu"}
            x = x["tu"]
        if x in co:
            continue
        if " " not in x and not dang:
            print(f"  ⚠ {ma_mau}/[{o}]: khai “{x}” mà bài không dạy từ ấy — gõ nhầm?")
            continue
        # Dựng đủ mọi khoá một mục từ vẫn có, để `sinh_cau` khỏi phải biết mục này
        # là cụm hay là từ. Thiếu `ma` thì phép neo vào câu SGK nổ KeyError.
        ra.append({"ma": f"cum_{re.sub(r'[^a-z0-9]+', '_', x.lower())}",
                   "tu": x, "nghia": None, "ipa": None, "vai": [], "am_o": "dau",
                   "so_it": None, "so_nhieu": None, "dang_ing": None,
                   "dang_qk": None,
                   "go_duoc": True, "nhom_nghia": None, "ten_rieng": None,
                   "hinh": None, "khong_ve": None, "hinh_ve": None,
                   "hinh_no": None, **dang})
    return ra


def sinh_cau(u: dict, tu: list, them: dict, sua_slot: dict, toi_da: int = 4) -> list[dict]:
    """Câu của một unit: câu SGK đứng đầu, rồi các câu thay MỘT ô mỗi lần.

    Chỉ đổi một ô mỗi câu — đó đúng là cách một bảng thay thế dạy: giữ nguyên khung,
    đổi một chỗ, để bé thấy chỗ nào là chỗ thay được. Đổi hai ô cùng lúc thì bé
    không biết cái gì vừa đổi.
    """
    VAI = vai_biet(tu, them)
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
                # Khai bằng DANH SÁCH TỪ đích danh, hay bằng VAI?
                #
                # Vai là luật rộng, và rộng quá thì đẻ ra câu vô nghĩa: ô [Verb] của
                # U8 nhận mọi `dongtu` nên ra "Can you do a van?", ô [Verb-ing] của
                # U2 ra "Is she doing a kite?". Câu đúng ngữ pháp, sai hẳn nghĩa —
                # và không cổng nào bắt được, vì máy không hiểu "doing a kite" là gì.
                #
                # Nên cho phép khai thẳng những từ HỢP NGHĨA với chính mẫu câu ấy.
                # Vai vẫn dùng được cho ô nào rộng thật (ô [Number], ô [Family member]).
                # Luật dứt khoát: MỌI mục đều là tên vai → hiểu là vai. Có bất kỳ
                # mục nào không phải tên vai → hiểu là danh sách TỪ đích danh. Không
                # trộn lẫn hai lối trong cùng một ô.
                if all(isinstance(x, str) and x in VAI for x in khai[o]):
                    kho[o] = ung_vien(khai[o], tu, them)
                else:
                    kho[o] = [t for t in ung_vien_tat(tu, them)
                              if t["tu"] in [x for x in khai[o] if isinstance(x, str)]]
                    kho[o] += cum_khai(khai[o], kho[o], mc["ma"], o)
            else:
                kho[o] = [t for t in tu if t["tu"] in mc["o_thay"]]
            # ── Ô ĐÒI MỘT DẠNG THÌ TỪ PHẢI CÓ DẠNG ẤY ──
            #
            # `chu()` ở dưới viết `dang_can(o, t) or t["tu"]`: ô đòi số nhiều mà từ
            # không khai `so_nhieu` thì nó lẳng lặng điền dạng GỐC. Câu vẫn ra, cổng
            # vẫn xanh, và bé đọc "Where are the lamp?" — sai đúng cái mà chính công
            # thức đang dạy ("nhiều vật nên dùng are").
            #
            # Nên lọc ngay từ kho: từ nào không có dạng ô cần thì không phải ứng viên
            # của ô ấy. Kho rỗng thì mẫu bị bỏ — và bỏ CÓ TIẾNG, vì `_thieu` của bản
            # chuẩn kêu lên là từ chưa khai `so_nhieu`.
            kho[o] = [t for t in kho[o] if dang_can(o, t)]
            if not kho[o]:
                break
        # ⚠ So với số ô KHÁC TÊN NHAU, không phải số lần ô xuất hiện.
        #
        # `kho` khoá bằng TÊN ô, nên công thức nhắc lại một tên thì `kho` chỉ có một
        # khoá cho tên ấy. Lớp 1 không mẫu nào nhắc lại tên ô nên `len(kho) == len(os)`
        # luôn đúng. Lớp 2 thì có: U2 nhắc [Pronoun] BA lần ("Is she flying a kite? -
        # Yes, she is. / No, she isn't."), U5 hai lần. Phép so cũ thấy 3 ≠ 5 rồi bỏ
        # qua CẢ MẪU — im lặng, không báo gì, và mất luôn hai unit khỏi vốn câu.
        if any(not v for v in kho.values()) or len(kho) != len(set(os)):
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
                        # ⚠ VIẾT HOA LÀ CHUYỆN CỦA VỊ TRÍ, không phải của từ neo.
                        # Bản cũ bật cờ hoa khi CHỮ NEO viết hoa — mà "Snow White"
                        # viết hoa vì nó là TÊN RIÊNG, không phải vì nó đứng đầu
                        # câu. Cờ ấy rồi áp cho mọi từ điền sau, và ra
                        #   ✗ "They're The ant and the grasshopper."
                        # Nay chỉ bật khi chỗ ấy THẬT SỰ mở đầu một câu; tên riêng
                        # tự giữ chữ hoa của chính nó.
                        i = goc.lower().index(d.lower())
                        truoc = goc[:i].rstrip()
                        found = t
                        hoa[o] = (not truoc) or truoc[-1] in ".?!-"
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
            # Trả về ĐÚNG mặt chữ của từ; việc viết hoa đầu câu do `dien()` lo —
            # nó biết ô đang đứng ở đâu trong công thức, còn ở đây thì không.
            return dang_can(o, t) or t["tu"]

        def _chu_cu(o, t):
            d = dang_can(o, t) or t["tu"]
            # ⚠ KHÔNG dùng `str.capitalize()` — nó HẠ chữ hoa ở phần sau:
            #     "Ms Hoa".capitalize()  →  "Ms hoa"
            # Lớp 1·2 không lộ vì mọi từ đều một chữ, toàn chữ thường. Lớp 3 có
            # "Ms Hoa" · "Mr Long" · "TV", và câu sinh ra thành "This is Ms hoa."
            return (d[:1].upper() + d[1:]) if hoa.get(o) else d

        # câu SGK trước — đó là câu đã có người soạn sách duyệt
        # `dang` = HÌNH DẠNG THẬT đã điền vào câu, không phải từ gốc. Hai thứ này
        # khác nhau thường xuyên hơn tưởng: "run" điền vào thành "running",
        # "window" thành "windows", "two" đầu câu thành "Two". Bước khoét chỗ
        # trống ở dưới cần đúng hình dạng ấy — xem chỗ dùng nó.
        # TỪ TRỌNG TÂM của câu SGK: ưu tiên ô nào neo được vào một TỪ MỚI CÓ HÌNH.
        # Bản cũ lấy cứng `os[-1]`. Với U16 (`How many + [Noun-plural] + can you
        # see? - I can see + [Number].`) ô cuối là con số — thứ duy nhất không vẽ
        # được — nên câu duy nhất của bài rơi vào tay số đếm, và sau khi chặn số
        # làm đáp án thì U16 còn ĐÚNG 0 câu luyện. Ô `[Noun-plural]` ngay bên cạnh
        # thì neo vào "windows", có hình, và cho ra đúng câu đáng luyện:
        #     "How many ___ can you see? - I can see six."
        # Nền của các ô cùng nhóm phải là MỘT từ — nếu không, câu SGK dựng ra đã
        # sai ngay từ dòng đầu.
        for g in [list(x) for x in ((sua_slot.get(mc["ma"]) or {}).get("cung_tu") or [])]:
            co = [o for o in g if o in kho]
            if len(co) < 2:
                continue
            chung = [t for t in kho[co[0]]
                     if all(any(y["ma"] == t["ma"] for y in kho[x]) for x in co[1:])]
            if not chung:
                continue
            dau = next((t for t in chung if any(nen[o]["ma"] == t["ma"] for o in co)),
                       chung[0])
            for o in co:
                nen[o] = dau

        def dung_duoc(o):
            t = nen[o]
            return (neo_duoc[o] and not str(t.get("ma") or "").startswith("them_")
                    and (t.get("hinh") or t.get("hinh_ve")))
        o_cuoi = next((o for o in reversed(os) if dung_duoc(o)), os[-1])
        ra.append({"cau": goc or dien(ct, {o: chu(o, nen[o]) for o in os}),
                   "tu": nen[o_cuoi], "dang": chu(o_cuoi, nen[o_cuoi]),
                   "neo": neo_duoc[o_cuoi], "mc": mc})

        # Đổi LUÂN PHIÊN từng ô, mỗi vòng một ô. Bản đầu vét cạn ô thứ nhất rồi mới
        # sang ô sau, nên U6 ("It's a + [Colour] + [Noun].") có 6 màu là đủ chạm
        # trần 4 câu — bé thấy bốn câu đổi màu mà KHÔNG BAO GIỜ thấy danh từ đổi,
        # tức là học một nửa mẫu câu.
        # ── HAI Ô KHÔNG ĐƯỢC TRÙNG TỪ ── (bắt được ở lớp 4, 20-08-2026)
        #
        # `kho` khoá bằng TÊN ô, nên hai ô CÙNG TÊN luôn nhận cùng một từ. Với
        # `[Routine]…[Routine]` (hỏi gì đáp nấy) thì đó là ĐÚNG. Nhưng lớp 4 unit 9
        # là `Is your sports day in [Month]? … It's in [Month].` — đoán một tháng
        # rồi SỬA LẠI, nên hai tháng phải KHÁC. Máy điền giống nhau và ra:
        #
        #     ✗  Is your sports day in June? - No, it isn't. It's in June.
        #
        # Ô khác tên cũng đụng: unit 18 khai `[shop]` và `[moc tham chieu]` cùng vai
        # `noichon`, nên bốc trúng nhau thì ra "The bookshop is near the bookshop."
        #
        # Không cổng nào bắt được — mọi chữ đều đã học, khuôn khớp công thức, câu
        # đúng ngữ pháp. Chỉ đọc lên mới thấy vô nghĩa. Nên khai `khac_nhau` trong
        # `sua_slot`, và MÁY canh, chứ `_ghi` thì chỉ người đọc được.
        khac = bool((sua_slot.get(mc["ma"]) or {}).get("khac_nhau"))

        # ── HAI Ô PHẢI LÀ CÙNG MỘT TỪ, Ở HAI DẠNG ── (lớp 5, 21-08-2026)
        #
        # `khac_nhau` lo chiều ngược: hai ô không được trùng. Lớp 5 cần chiều này.
        #
        #     Did you + [Verb]? - Yes, I did. I + [past verb].
        #
        # Hai ô KHÁC TÊN nên `sinh_cau` bốc độc lập, và ra:
        #
        #     ✗  Did you buy souvenirs? - Yes, I did. I swam.
        #
        # Hỏi một đằng đáp một nẻo. Không đổi tên ô cho giống nhau được: TÊN Ô
        # chính là thứ quyết định DẠNG (`dang_can`), nên hai ô cùng tên `[Verb]`
        # sẽ ra "Did you swam?".
        #
        # Nên khai `cung_tu` ở `sua_slot`: các nhóm ô phải lấy CÙNG MỘT TỪ, mỗi ô
        # tự chia dạng của mình. Không cổng nào bắt được lỗi này — mọi chữ đều đã
        # học, khuôn khớp công thức, câu đúng ngữ pháp; chỉ đọc lên mới thấy.
        nhom_cung = [list(g) for g in
                     ((sua_slot.get(mc["ma"]) or {}).get("cung_tu") or [])]
        cung_cua = {o: g for g in nhom_cung for o in g}

        def dong_bo(gan: dict, o: str, t: dict) -> dict:
            """Đổi một ô thì đổi cả nhóm của nó sang cùng từ ấy."""
            for x in cung_cua.get(o, [o]):
                if any(y["ma"] == t["ma"] for y in kho.get(x, [])):
                    gan[x] = chu(x, t)
            return gan

        def hop_le(gan: dict) -> bool:
            if not khac:
                return True
            # ⚠ So sau khi BỎ MẠO TỪ. Bản đầu so chuỗi trần, nên "bookshop" và
            # "the bookshop" là hai chuỗi khác nhau và lọt lưới:
            #     ✗  Where's the bookshop? - It's opposite the bookshop.
            def goc_tu(x):
                return re.sub(r"^(the|a|an)\s+", "", str(x).strip().lower())
            dung = [goc_tu(v) for v in gan.values() if v]
            return len(dung) == len(set(dung))

        hang = {o: [t for t in kho[o] if not (neo_duoc[o] and t["ma"] == nen[o]["ma"])]
                for o in os}
        while sum(1 for x in ra if x["mc"] is mc) < toi_da and any(hang.values()):
            for o in os:
                if not hang[o]:
                    continue
                t = hang[o].pop(0)
                gan = {x: chu(x, nen[x]) for x in os}
                gan = dong_bo(gan, o, t)
                if not hop_le(gan):
                    continue
                c = dien(ct, gan)
                if c != goc:
                    ra.append({"cau": c, "tu": t, "dang": gan[o], "neo": True, "mc": mc})
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
        chon_ds = tron(t["tu"], moi_nhu(t, tu))
        hinh_nut = {x: (next((y.get("hinh") for y in tu if y["tu"] == x), None))
                    for x in chon_ds}
        ve_nut = {x: (next((y.get("hinh_ve") for y in tu if y["tu"] == x), None))
                  for x in chon_ds}
        # ⚠ ĐỦ HÌNH CẢ BỐN NÚT thì mới bày hình.
        #
        # Lớp 1·2 từ nào cũng có hình nên câu này luôn đúng. Lớp 3 thì 51/204 từ
        # không có hình — và ba unit ĐẦU (`hello · hi · fine · how · I · you`)
        # KHÔNG CÓ TỪ NÀO có hình. Bày hình cho những câu ấy thì bốn nút ra bốn dấu
        # ❔ y hệt nhau: câu hỏi không trả lời được, chỉ đoán 1/4. Mà đề vẫn bảo
        # "bấm vào HÌNH đúng" — nói dối bé đúng cái kiểu 15 câu của lớp 1 từng làm.
        #
        # Lẫn lộn còn tệ hơn cả trống: ba nút có hình một nút ❔ thì cái ❔ lộ ngay
        # ra là khác biệt, và bé chọn theo hình dạng chứ không theo tiếng nghe được.
        #
        # Không có hình thì bấm vào CHỮ — bé lớp 3 đọc được, và đó cũng là việc lớp
        # 3 đang tập. Chữ hiện lên, không dối bé câu nào.
        du_hinh = all(hinh_nut.get(x) or ve_nut.get(x) for x in chon_ds)
        warmup.append({
            "id": f"C{i}",
            "bac": 1,
            "text": "Nghe rồi bấm vào hình đúng." if du_hinh
                    else "Nghe rồi bấm vào từ đúng.",
            "am": am_id("tu", t["tu"]),
            "anhChon": du_hinh,
            "format": "chon",
            "choices": chon_ds,
            # Nút của bậc 1 hiện HÌNH chứ không hiện chữ — bé chưa đọc được chữ
            # tiếng Anh thì bấm vào chữ là đoán mò. Chữ vẫn là giá trị đáp án để
            # bộ chấm so, nhưng cái bé NHÌN là emoji.
            "hinhNut": hinh_nut,
            "veNut": ve_nut,
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
            "solutionNarrative": f"{tu_ipa(t)} — {t['nghia']}",
            "hints": ["Nghe lại từ rồi nghĩ xem con nhìn thấy nó ở đâu."],
        })
    n = len(warmup)
    for i, t in enumerate(tu, 1):
        warmup.append({
            "id": f"C{n + i}",
            "bac": 2,
            "text": f"“{t['nghia']}” tiếng Anh là gì?",
            # Clip NGHĨA (tiếng Việt) — bé nghe nghĩa rồi chọn từ. KHÔNG dùng clip
            # tiếng Anh ở đây: phát từ lên là cho không đáp án.
            "am": am_id("nghia", t["nghia"]),
            "format": "chon",
            "choices": tron(t["tu"], moi_nhu(t, tu)),
            "answerKey": {"choice": t["tu"]},
            "solutionNarrative": f"{t['nghia']} — {tu_ipa(t)}",
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
    for c in cau:
        t = c["tu"]
        dang = c.get("dang") or t["tu"]
        # ── BA CỬA, VÀ MỘT CHỖ NÓI THẬT ──
        # Bác bắt 14-08; rà ra 18 câu hỏng. Câu hỏng tệ hơn câu thiếu: bé sáu tuổi
        # gặp một câu KHÔNG THỂ làm đúng thì học được đúng một điều — rằng mình kém.
        # Nhưng bỏ câu cũng phải có chừng: bản chặn đầu tiên của chính đợt sửa này
        # xoá sạch bài luyện của Unit 16 (còn 0 câu), tức là chữa lỗi bằng cách tạo
        # một lỗ hổng. Nên ba cửa dưới đây chỉ chặn cái KHÔNG cứu được, còn lại thì
        # sửa cho đúng chứ không vứt đi.
        #
        # 1. SỐ ĐẾM và MÀU không được làm đáp án. Chúng nằm ở `them` để ĐIỀN VÀO
        #    KHUNG cho có câu mà luyện, không phải từ mới của bài. Bản cũ lấy luôn
        #    chúng làm đáp án, nên Unit 6 có câu đáp án là "blue" — một từ CẢ QUYỂN
        #    không bài nào dạy (đã dò đủ 16 bài).
        #    TÊN NGƯỜI thì KHÁC: `Hi, I'm + [Name].` có ô tên là chính chỗ bài đang
        #    dạy, và "Bill" nằm trong câu ví dụ của sách. Chặn cả tên là mất 8 câu
        #    của Unit 1 mà chẳng vì lý do gì.
        ma = str(t.get("ma") or "")
        if ma.startswith("them_so_dem") or ma.startswith("them_mau"):
            continue
        # 2. NEO HỤT — chỗ này thì đúng là không cứu được. Câu SGK của U15 là
        #    "Point to your hand." trong khi `hand` là từ của U8, nên từ nền rơi về
        #    `face`. `replace` không tìm thấy gì, chỗ trống không được tạo, và đề
        #    hiện nguyên câu về BÀN TAY với đáp án là KHUÔN MẶT.
        if not c.get("neo", True) or dang not in c["cau"]:
            continue
        # 3. DẠNG ĐÃ ĐIỀN mới là thứ phải khoét, không phải từ gốc. Câu chứa
        #    "running" mà khoét theo "run" thì ra `"She's ___ning."` — chỗ trống cắt
        #    vào giữa chữ, điền đáp án vào lại thành "She's runing.". Đã sinh ra thật
        #    ở U11. Nay khoét TRỌN "running" và đáp án cũng là "running": đó chính
        #    là dạng bé phải học, chứ không phải từ gốc trong từ điển.
        #    Cùng chỗ này lo luôn "windows" của U16 — nếu không thì U16 mất trắng.
        dap = dang
        # 4. KHÔNG CÓ HÌNH thì đừng BẢO bé nhìn hình. 15 câu từng nói dối như thế.
        #    Nhưng câu vẫn dùng được — chỉ là manh mối nằm ở CÂU chứ không ở hình,
        #    nên đổi lời dẫn cho đúng sự thật thay vì vứt câu đi.
        anh, anhVe = t.get("hinh"), t.get("hinh_ve")
        coHinh = bool(anh or anhVe)
        n += 1
        standard.append({
            "id": f"S{n}",
            "bac": 3,
            "text": ("Nhìn hình rồi chọn từ điền vào chỗ trống:  " if coHinh
                     else "Chọn từ điền vào chỗ trống:  ")
                    + c["cau"].replace(dang, "___", 1),
            # Lời dẫn TIẾNG VIỆT dùng chung cho mọi câu điền — bé chưa đọc được
            # thì không có tiếng là không biết phải làm gì. Vẫn KHÔNG đọc câu
            # tiếng Anh: manh mối phải là HÌNH, đọc lên là thành bài nghe.
            "am": am_id("loi", DAN_DIEN if coHinh else DAN_DIEN_KHONG_HINH),
            # CỐ Ý KHÔNG có `am` cả câu. Phát cả câu lên thì bé chỉ việc nghe rồi
            # bấm — thành bài NGHE lặp lại của bậc 1, không còn kiểm cấu trúc nữa.
            # Manh mối ở đây là HÌNH; chỗ trống là chỗ bé phải tự nối hình với từ.
            "anh": anh,
            "anhVe": anhVe,
            "format": "chon",
            "choices": tron(dap, moi_nhu(t, tu)),
            "answerKey": {"choice": dap},
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
                "solutionNarrative": f"{tu_ipa(t)} — {t['nghia']}",
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
                "solutionNarrative": f"{tu_ipa(t)} — {t['nghia']}",
                "hints": [f"Từ này dài {len(t['tu'])} chữ cái."],
            })
    n = len(challenge)
    # Gõ VẾ ĐẦU thôi, và chỉ những câu gõ nổi.
    #
    # Lớp 1 mẫu câu nào cũng là một câu trần thuật ngắn ("It's a pen."). Lớp 2 quá
    # nửa là HỎI - ĐÁP có cả hai phương án:
    #     "Is she flying a kite? - Yes, she is. / No, she isn't."   53 ký tự
    # Bắt bé bảy tuổi gõ ngần ấy, kèm dấu gạch chéo, là bỏ cuộc chứ không phải làm
    # sai — bé gõ chừng mười ký tự một phút. Cổng `tienganh_bai` bắt đúng 12 chỗ.
    #
    # Vế trước " - " chính là câu bé cần nói ra; vế sau là lời đáp mẫu. Cắt xong mà
    # vẫn quá dài thì BỎ câu ấy khỏi bậc gõ, đừng cắt cụt giữa chừng.
    dem = 0
    for c in cau:
        if dem >= 2:                        # chỉ 2 câu — gõ cả câu là việc nặng nhất
            break
        go = c["cau"].split(" - ")[0].strip()
        if len(go) > GO_CAU_TOI_DA or not re.fullmatch(r"[A-Za-z0-9 '\-.,?!]+", go):
            continue
        dem += 1
        challenge.append({
            "id": f"T{n + dem}",
            "bac": 4,
            "text": "Nghe rồi gõ lại cả câu.",
            "am": am_id("cau", go),
            "answerKey": {"value": go},
            "solutionNarrative": go,
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
            # CÂU ĐÚNG hiện DẠNG ĐẦY ĐỦ, không hiện dạng rút.
            #
            # Hai lý do, và cả hai đều quan trọng hơn việc chép y câu SGK:
            #  · Dạy rõ hơn — bé thấy tận mắt "'re" thay cho chữ gì.
            #  · Neo được chữ đang giảng. Cổng `tienganh_bai` đòi mọi từ tiếng Anh
            #    đặt trong ngoặc kép phải có mặt trong câu đúng hoặc câu sai; viết
            #    "They're" thì chữ “are” không nằm ở đâu cả và bị báo là từ lạ.
            #    Lớp 1 thoát vì "is"/"am" chỉ hai chữ cái, dưới ngưỡng cổng soi.
            day_du = d.replace(rut, f" {day} ", 1).replace("  ", " ")
            return {
                "wrong": thieu, "right": day_du,
                "why": f"Câu này bắt buộc phải có “{day}”, nói nhanh thì rút lại "
                       f"thành {rut.strip()} như trong bài. "
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

def sat_hach(u: dict, cau: list, hinh_cua: dict) -> list:
    """Năm câu ĐÚNG/SAI — nghe và nhìn, KHÔNG cần đọc.

    ── VÌ SAO DỰNG LẠI ──
    Bản trước ra câu chữ: “ball” nghĩa là “quả bóng”. Bé lớp 1 chưa đọc sõi tiếng
    Việt nên 80 câu sát hạch của cả quyển đều là câu bé KHÔNG LÀM ĐƯỢC — nó chỉ
    đoán, và đúng/sai thì đoán trúng 50%. Con số trong sổ bố mẹ thành con số rỗng.

    Nay mỗi câu là: NGHE một từ tiếng Anh, NHÌN một hình, rồi bảo hình ấy có đúng
    là từ vừa nghe không. Không một chữ nào phải đọc, mà vẫn kiểm đúng thứ cần
    kiểm — bé có nối được ÂM với NGHĨA hay không.

    Dùng lại clip và hình đã có, không sinh thêm gì.

    ── ĐÁP ÁN VẪN XEN KẼ ──
    Ba câu đúng liền nhau là bé qua bằng cách đoán theo nhịp.

    ── ⚠ TỪ KHÔNG CÓ HÌNH THÌ KHÔNG DỰNG ĐƯỢC CÂU NÀY ──
    Cả khuôn trên đứng trên một điều: có một BỨC HÌNH để mà nhìn. Lớp 3 có 51/204
    từ không vẽ được, và ba unit đầu thì KHÔNG TỪ NÀO có hình — nên bản trước đẻ ra
    16 câu `anh: null`: bé nghe một từ, nhìn vào chỗ trống, rồi bấm Đúng hoặc Sai.
    Đúng 15 câu sát hạch của ba bài đầu là câu KHÔNG THỂ TRẢ LỜI, mà điểm vẫn ghi
    vào học bạ và bố mẹ vẫn đọc được con số ấy.

    Nên câu đúng/sai chỉ dựng từ từ CÓ HÌNH. Chỗ còn thiếu bù bằng câu NGHE → CHỌN
    NGHĨA: bé lớp 3 đọc được tiếng Việt, và câu ấy vẫn kiểm đúng một việc — nối ÂM
    với NGHĨA. Thà đổi dạng câu còn hơn giữ đúng dạng mà hỏi vào chỗ trống.
    """
    tu = [t for t in u["tu"] if t.get("nghia")]
    if len(tu) < 2:
        return []
    anh = lambda t: (hinh_cua.get(t["tu"]) or {})
    co_hinh = [t for t in tu if anh(t).get("hinh") or anh(t).get("ve")]

    dung, sai = [], []
    for i, t in enumerate(co_hinh):
        h = anh(t)
        dung.append(({"am": am_id("tu", t["tu"]), "anh": h.get("hinh"),
                      "anhVe": h.get("ve"), "text": ""},
                     True, f"ĐÚNG — {t['tu']} là {t['nghia']}."))
        khac = co_hinh[(i + 1) % len(co_hinh)]
        if khac["tu"] == t["tu"]:
            continue            # unit chỉ có MỘT từ có hình → không ghép lệch được
        hk = anh(khac)
        sai.append(({"am": am_id("tu", t["tu"]), "anh": hk.get("hinh"),
                     "anhVe": hk.get("ve"), "text": ""},
                    False, f"SAI — đó là {khac['tu']}. {t['tu']} là {t['nghia']}."))

    # Câu cuối dùng CẢ CÂU, nếu bài có: kiểm bé nghe được nguyên câu chứ không chỉ từ.
    if cau:
        c = cau[0]
        h = anh(c["tu"])
        if h.get("hinh") or h.get("ve"):
            dung.append(({"am": am_id("cau", c["cau"]), "anh": h.get("hinh"),
                          "anhVe": h.get("ve"), "text": ""},
                         True, f"ĐÚNG — {c['cau']}"))

    # ⚠ KHÔNG CÓ CÂU SAI THÌ CHỈ ĐƯỢC MỘT CÂU ĐÚNG/SAI.
    #
    # Câu SAI dựng bằng cách ghép tiếng đọc của từ này với HÌNH của từ khác — bài
    # nào chỉ có MỘT từ vẽ được thì không ghép lệch được, `sai` rỗng, và cả kỳ ra
    # toàn đáp án "đúng". Bé bấm "đúng" hết là trọn điểm mà không nghe câu nào.
    # Lớp 5 có bốn bài như thế (từ vựng phần lớn là CỤM VIỆC, không vẽ được).
    #
    # Thà ít câu đúng/sai còn hơn một dãy đoán được: phần thiếu đã có câu NGHE →
    # CHỌN NGHĨA bù ngay dưới, mà dạng ấy bốn lựa chọn nên không có nhịp để đoán.
    if not sai:
        dung = dung[:1]

    ra, k = [], 0
    while len(ra) < 5 and (dung or sai):
        kho, gt = (dung, True) if k % 2 == 0 else (sai, False)
        if not kho:
            kho, gt = (sai, False) if gt else (dung, True)
        if not kho:
            break
        than, _, loi = kho.pop(0)
        ra.append({"id": f"Q{len(ra) + 1}", **than, "format": "tf",
                   "nhinNghe": True, "answerKey": {"value": gt},
                   "solutionNarrative": loi})
        k += 1

    # ── bù cho đủ 5 câu bằng NGHE → CHỌN NGHĨA ──
    # Cùng khuôn bậc 2 của phần luyện tập, nên không có gì mới phải học lúc đi thi.
    for t in tu:
        if len(ra) >= 5:
            break
        moi = moi_nhu(t, tu, khoa="nghia")
        if len(moi) < 2:
            break
        ra.append({
            "id": f"Q{len(ra) + 1}",
            "text": f"“{t['tu']}” nghĩa là gì?",
            "am": am_id("tu", t["tu"]),
            "format": "chon",
            "choices": tron(t["nghia"], moi),
            "answerKey": {"choice": t["nghia"]},
            "solutionNarrative": f"{tu_ipa(t)} — {t['nghia']}",
        })
    return ra

# ── VIDEO TỪ MỚI TÁCH THEO NHÓM NGHĨA ──
#
# Đo thật trên 34 video đã dựng: độ dài ≈ 15 giây khung + 4 giây mỗi từ.
#     3 từ → 27,1s      5 từ → 37,1s      8 từ → 47,0s
# Lớp 1·2 mỗi unit 3,5 từ nên một video là đủ. Lớp 3 là 9,7 từ, nhiều nhất 15 —
# giữ khuôn cũ thì ra 54 tới 75 giây, mà bé lớp ba ngồi không nổi thì nó bấm bỏ
# qua và cả bài giảng thành công cốc.
#
# ⚠ KHÔNG PHẢI TỪ NÀO CŨNG DÀI BẰNG NHAU.
#
# Từ CÓ HÌNH mất ~4 giây: đọc từ, đọc nghĩa, xong. Từ KHÔNG vẽ được thì dạy bằng
# CÂU (xem `_canh_mot_tu` của kich_ban.py) — thêm một lời dẫn tiếng Việt và một câu
# tiếng Anh nữa, thành ~7 giây. Đếm đầu từ thì `Lời chào` của U1 (6 từ, cả sáu đều
# trừu tượng) ra 56 giây trong khi phép đếm bảo nó chỉ bằng 6 từ thường (39 giây).
#
# Nên đo bằng GIÂY, không bằng số từ. Ba con số dưới đây đều suy từ phép đo thật
# trên 74 video đã dựng, đừng chỉnh bừa:
GIAY_TU_CO_HINH = 4     # 3 từ → 27,1s · 5 từ → 37,1s · 8 từ → 47,0s
GIAY_TU_KHONG_HINH = 7  # cảnh "dùng trong câu" dài gần gấp đôi
GIAY_KHUNG = 15         # bìa + cảnh chữ cái của nhóm ĐẦU (nhóm sau chỉ ~4 giây)
TRAN_GIAY = 50          # trần một video từ mới — trùng cổng `tienganh_video`
NHOM_TOI_DA = TRAN_GIAY - GIAY_KHUNG        # 35 giây "ruột" một nhóm
# Dưới 20 giây ruột (≈24s cả khung) thì gộp vào nhóm cạnh. Ngưỡng này KHÔNG chỉ để
# tránh video quá ngắn — nó để tránh VỠ VỤN: U3 toàn từ trừu tượng, mỗi vai đúng
# một hai từ, và ngưỡng 12 giây đẻ ra NĂM tệp cho một unit. Năm ô video trên thanh
# việc, mỗi ô mười tám giây, thì bé bấm cả buổi không hết.
NHOM_TOI_THIEU = 5 * GIAY_TU_CO_HINH
NUA_TOI_THIEU = 3 * GIAY_TU_CO_HINH   # cắt đôi thì mỗi nửa vẫn phải đủ dài


def _dai(tu: dict) -> int:
    """Từ này ngốn mấy giây trong video."""
    return (GIAY_TU_CO_HINH if (tu.get("hinh") or tu.get("hinh_ve"))
            else GIAY_TU_KHONG_HINH)


def _cat_doi(g: list[str], dai: dict) -> list[list[str]]:
    """Cắt một nhóm làm đôi, cân theo GIÂY chứ không theo đầu từ."""
    nua, chay = sum(dai[x] for x in g) / 2, 0
    for i, x in enumerate(g[:-1]):
        chay += dai[x]
        if chay >= nua:
            return [g[:i + 1], g[i + 1:]]
    return [g[:1], g[1:]]


def _gom_nhom_nghia(tu: list[dict], vai_ten: dict) -> list[dict]:
    """Gom từ của một unit thành các NHÓM NGHĨA, mỗi nhóm một video.

    Nhóm KHÔNG phải soạn thêm: `vai` đã chia sẵn từ phần bù. U13 gom theo `vai` là
    ra ngay *nơi chốn* / *đồ đạc* / *chỗ đứng* — đúng ba nhóm người soạn sẽ chia.

    Ba bước, theo đúng thứ tự:
      1. gom theo `vai` (thứ tự xuất hiện, không phải a·b·c — bé học theo thứ tự sách)
      2. CẮT nhóm quá `NHOM_TOI_DA`, chia đều
      3. rồi mới GỘP nhóm lẻ dưới `NHOM_TOI_THIEU` vào nhóm cạnh nó nhỏ nhất

    Cắt trước gộp sau, và thứ tự ấy đổi hẳn kết quả. U4 có *bộ phận cơ thể* 7 từ và
    *động từ* 2 từ:
        gộp trước → 9 từ rồi cắt đôi → hai tệp đều mang tên "Bộ phận cơ thể · Hành
                    động", hai tay chân nằm lẫn trong cả hai
        cắt trước → 4 + 3, rồi hai động từ nhập vào nửa nhỏ → "Bộ phận cơ thể" (4) và
                    "Bộ phận cơ thể · Hành động" (5) — một tệp SẠCH tên, tệp kia nói
                    đúng cái nó chứa
    """
    dai = {t["tu"]: _dai(t) for t in tu}
    tong = sum(dai.values())
    if tong <= NHOM_TOI_DA:
        # Unit gọn thì một video, tên tệp `_tu.mp4` như hai quyển trước. Tách một
        # unit 4 từ ra hai tệp 20 giây là đổi tên tệp của 34 video đang chạy thật để
        # đổi lấy một cái không ai xin.
        return [{"ma": "tu", "ten": "Từ mới", "vai": [], "tu": [t["tu"] for t in tu]}]

    vai_cua = {t["tu"]: (t.get("vai") or ["dt"])[0] for t in tu}
    nhom: list[list[str]] = []
    cho: dict[str, int] = {}
    for t in tu:
        v = vai_cua[t["tu"]]
        if v not in cho:
            cho[v] = len(nhom)
            nhom.append([])
        nhom[cho[v]].append(t["tu"])

    def do(g):
        return sum(dai[x] for x in g)

    # ── cắt nhóm quá dài, chia ĐỀU ──
    # Chia đều chứ không cắt 7+3: hai tệp cân nhau, còn một tệp sát trần một tệp hụt
    # thì bé xem cái sau thấy cụt.
    def cat_deu(g):
        so_phan = max(1, -(-do(g) // NHOM_TOI_DA))
        if so_phan == 1:
            return [g]
        moi, ra, phan = do(g) / so_phan, [], []
        for x in g:
            phan.append(x)
            if do(phan) >= moi and len(ra) < so_phan - 1:
                ra.append(phan)
                phan = []
        return ra + ([phan] if phan else [])

    cat: list[list[str]] = []
    for g in nhom:
        cat += cat_deu(g)

    # ── gộp nhóm lẻ vào nhóm cạnh nó NHỎ NHẤT ──
    #
    # Chỉ gộp khi gộp xong vẫn dưới trần: gộp bừa thì `bộ phận cơ thể` 28 giây nuốt
    # hai động từ thành 36 — 51 giây cả khung, đúng cái vừa đi tránh. Nhóm cạnh đã
    # kín chỗ mà đủ dài để CẮT ĐÔI thì cắt rồi hãy gộp: U4 có `bộ phận cơ thể` 28
    # giây + `động từ` 8, cắt đôi rồi nhập vào nửa nhỏ là ra hai tệp cân nhau.
    #
    # ⚠ CHỖ NÀY TỪNG QUAY VÒNG KHÔNG DỪNG. Nhóm MỘT TỪ thì gộp bằng mọi giá (một
    # video tám giây không phải bài giảng), gộp xong quá trần thì lại cắt, cắt xong
    # hai nửa lại dưới ngưỡng nên lại đòi gộp — đúng hai nhóm ấy, mãi mãi. Nên nhóm
    # nào đã bị CẮT BẮT BUỘC thì ĐÓNG (`khoa`): nó không đi tìm chỗ gộp nữa, nhưng
    # vẫn NHẬN được nhóm khác nhập vào nếu vẫn dưới trần. Mỗi vòng lặp hoặc bớt một
    # nhóm, hoặc đóng thêm một nhóm — nên chắc chắn dừng.
    ds = [{"tu": g, "khoa": False} for g in cat]
    while len(ds) > 1:
        i = next((k for k, g in enumerate(ds)
                  if do(g["tu"]) < NHOM_TOI_THIEU and not g["khoa"]), None)
        if i is None:
            break
        canh = [k for k in (i - 1, i + 1) if 0 <= k < len(ds)]
        vua = [k for k in canh if do(ds[k]["tu"]) + do(ds[i]["tu"]) <= NHOM_TOI_DA]
        if not vua:
            j = min(canh, key=lambda k: (do(ds[k]["tu"]), k))
            # Cắt đôi nhóm cạnh chỉ đáng làm khi HAI NỬA đều còn đủ dài để đứng
            # thành video (≥ 3 từ có hình). Cắt một nhóm 20 giây làm đôi thì được
            # hai tệp mười giây — chữa một video ngắn bằng cách đẻ ra hai cái ngắn hơn.
            if (not ds[j]["khoa"] and len(ds[j]["tu"]) > 1
                    and do(ds[j]["tu"]) >= 2 * NUA_TOI_THIEU):
                ds[j:j + 1] = [{"tu": x, "khoa": True} for x in _cat_doi(ds[j]["tu"], dai)]
                continue
            if len(ds[i]["tu"]) > 1:
                ds[i]["khoa"] = True     # hai từ đứng riêng còn hơn một tệp 51 giây
                continue
        j = min(vua or canh, key=lambda k: (do(ds[k]["tu"]), k))
        a, b = (min(i, j), max(i, j))
        moi = ds[a]["tu"] + ds[b]["tu"]
        khoa = ds[a]["khoa"] or ds[b]["khoa"]
        ds[a:b + 1] = ([{"tu": moi, "khoa": khoa}] if do(moi) <= NHOM_TOI_DA
                       else [{"tu": x, "khoa": True} for x in _cat_doi(moi, dai)])
    cat = [g["tu"] for g in ds]

    # ── đặt tên SAU CÙNG, theo vai ĐÔNG NHẤT trong nhóm ──
    # Đếm lại từ danh sách đã chốt, đừng mang con số lúc cắt đi theo: gộp có thể nuốt
    # mất một mảnh, và "phần 1" đứng một mình là hỏi bé phần 2 đâu. Và vai đông nhất
    # mới được đặt tên tệp — nhóm 4 màu cộng một chữ `colour` mà gọi là `tu_dt` thì
    # người đi tìm tệp phải mở ra mới biết trong đó có gì.
    chinh = [max(dict.fromkeys(vai_cua[t] for t in g),
                 key=lambda v: (sum(1 for t in g if vai_cua[t] == v), -g.index(
                     next(t for t in g if vai_cua[t] == v))))
             for g in cat]
    dem = {v: chinh.count(v) for v in chinh}
    thu: dict[str, int] = {}
    ra = []
    for g, v in zip(cat, chinh):
        thu[v] = thu.get(v, 0) + 1
        phan = thu[v] if dem[v] > 1 else 0
        vai = [v] + [x for x in dict.fromkeys(vai_cua[t] for t in g) if x != v]
        ra.append({"ma": f"tu_{v}{phan}" if phan else f"tu_{v}", "phan": phan,
                   "vai": vai, "tu": g, "ten": _ten_nhom(vai, vai_ten, phan)})
    return ra


def _ten_nhom(vai: list[str], vai_ten: dict, phan: int) -> str:
    """Tên NÓI ĐƯỢC VỚI BÉ, hiện trên bìa video và trên thanh việc.

    Nhóm gộp thì ghép tên hai vai — thà dài một chút còn hơn gọi cả nhóm là "Số
    đếm" trong khi trong đó có `the alphabet`. Nhóm bị cắt thì đánh số phần, vì
    hai ô cùng tên trên thanh việc thì bé không biết mình còn thiếu cái nào.
    """
    ten = " · ".join(vai_ten.get(v, v) for v in vai[:2])
    if len(vai) > 2:
        ten += " · …"
    return f"{ten} · phần {phan}" if phan else ten


def _ten_video(u: dict, ma_bai: str, vai_ten: dict, tu: list[dict]) -> dict:
    """Tên tệp video, suy theo ĐÚNG luật `dung_video.py` đặt tên."""
    tep = ma_bai.replace("DL:", "DL_").replace(".", "_")
    ds = [x for m in u["mau_cau"] for x in _tach_mau(m)]
    vais = [x.get("vai", "cau") for x in ds]
    ra, dem = [], {}
    for x, v in zip(ds, vais):
        dem[v] = dem.get(v, 0) + 1
        ten = v if vais.count(v) == 1 else f"{v}{dem[v]}"
        ra.append({"vai": v, "cau": x["cau"], "tep": f"{tep}_{ten}.mp4"})
    # `tu` là DANH SÁCH, kể cả khi chỉ có một nhóm. Một trường hai hình dạng (khi
    # thì chuỗi khi thì mảng) là chỗ mọi bên đọc phải tự đoán, và sớm muộn có bên
    # đoán sai — xem `dsVideoTu()` ở `lib/noiDung.js`, nay chỉ còn MỘT hình dạng.
    # Gom trên ĐÚNG danh sách từ mà bài đem dạy (`vocabulary`), không phải trên
    # `u["tu"]` thô. Hai danh sách chỉ lệch khi có từ chưa có nghĩa — nhưng lệch là
    # nhóm khai một đằng, video dạy một nẻo, và không cổng nào hỏi được câu ấy.
    nhom = _gom_nhom_nghia(tu, vai_ten)
    return {"tu": [{"ma": g["ma"], "ten": g["ten"], "tu": g["tu"],
                    "tep": f"{tep}_{g['ma']}.mp4" if g["ma"] != "tu"
                           else f"{tep}_tu.mp4"} for g in nhom],
            "cau": ra}


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


# ══════════════════════════════════════════════════════════════════════════════
# LỜI MỞ "BA TỪ CÙNG ÂM" — ĐÃ BỎ HẲN 18-08-2026. ĐỪNG DỰNG LẠI.
# ══════════════════════════════════════════════════════════════════════════════
#
# Trước đây K2 nói: "Nghe ba từ này: X · Y · Z. Con có nghe thấy chúng bắt đầu
# giống nhau không? Đó chính là âm … của chữ …", với X·Y·Z là BA TỪ ĐẦU TIÊN của
# unit — lấy bừa, không hỏi lại lấy một lần.
#
# Bác bắt: "từ lớp 2 đến lớp 3 là nhiều từ mới không có trong nhóm âm. Nhưng video
# dạy từ mới bạn vẫn mô típ là hãy nghe 03 từ thấy giống nhau gì không? Giống nhau
# âm ... Hoàn toàn sai."
#
# Soi cả ba quyển: lớp 3 sai 21/21, lớp 2 sai 8/16, lớp 1 sai 6/16.
#
#     box · fox · ox                 "x" nằm CUỐI từ, không phải đầu
#     bird · cat · dog               chẳng có âm nào chung
#     cooking · dancing · drawing    bài khai chữ "p"
#     apple · bag · can              "a" là nguyên âm, bag/can không mở đầu bằng nó
#
# Tiền đề "mỗi unit có một chữ cái, và từ vựng minh hoạ chữ ấy" chỉ đúng với lớp 1,
# quyển xếp bài THEO CHỮ CÁI. Từ lớp 2 sách xếp theo CHỦ ĐỀ nên nó sụp hẳn.
#
# Bản đầu 18-08 chữa bằng cách chỉ sinh K2 khi ba từ THẬT SỰ cùng âm đầu (còn 18
# bài). Bác xem rồi chốt: "Bỏ sạch luôn đi." Đúng — giữ lại 18 bài thì cùng một
# quyển có hai kiểu mở màn, bé lớp 1 xem bài 3 thấy khác bài 4 mà không hiểu vì
# sao; mà cái được thì nhỏ, còn cái mất là một luật đơn giản.
#
# ⚠ ĐỪNG CHÈN LẠI. `chu` và `am` (`u["phonics"]`) VẪN CÒN trong bản đồ và vẫn nằm
# ngay đây — nên viết lại mấy dòng ấy rất dễ. Có cổng canh:
# `tienganh_bai.test.mjs` §4D đỏ nếu bài nào lại khai K2 hoặc nhắc chuyện âm đầu,
# và `tienganh_video.test.mjs` đỏ nếu kịch bản nào có lại cảnh `chu_cai`.
#
# Nay lời mở là K1: "Hôm nay chúng mình học 8 từ mới — Sở thích của mình." Đúng
# với mọi quyển, và nói ra thứ bé sắp học thật.


def dung_bai(u: dict, lop: int, truoc: str | None, sau: str | None,
              them: dict, sua_slot: dict, chuong: dict, vai_ten: dict) -> dict:
    ph = u.get("phonics") or {}
    hinh_cua = {t["tu"]: {"hinh": t.get("hinh"), "ve": t.get("hinh_ve")} for t in u["tu"]}
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
    canh_vi = str(u.get("canh") or "").split("·")[0].strip()
    K = [
        {"id": "K1",
         "text": f"Hôm nay chúng mình học {len(tu)} từ mới — {canh_vi}.",
         "doanAm": [(f"Hôm nay chúng mình học {len(tu)} từ mới — {canh_vi}.", "vi")]},
        {"id": "K3",
         "text": "Từ mới của bài: "
                 + " · ".join(f"{tu_ipa(t)} = {t['nghia']}" for t in tu),
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
            # ⚠ LỜI ĐỌC CHỈ LẤY PHẦN TIẾNG VIỆT.
            #
            # Từ lớp 2, tên cảnh để SONG NGỮ "Ở tiệc sinh nhật · At my birthday party"
            # (bác chốt 17-08). Nhưng đó là tên để NHÌN. Đưa nguyên cả cụm vào dòng
            # khai `vi` thì giọng đọc tiếng Việt đọc luôn phần tiếng Anh — nghe sai
            # hẳn, và cổng `tienganh_am` bắt đúng 17 dòng như thế.
            "narration": f"Cảnh hôm nay: {canh_doc(u)}.",
            "doanAm": [(f"Cảnh hôm nay: {canh_doc(u)}.", "vi")]}]
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
            # ⚠ MANG THEO DẠNG BIẾN ĐỔI. Bài học là NGUỒN mà `sinh_kichban_noi`
            # và các cổng dựng túi từ từ đó; thiếu `dang_qk` thì phòng nói gọi
            # "I bought souvenirs." là chữ lạ rồi BỎ câu ấy — câu đúng hẳn, chỉ
            # vì cái dạng quá khứ không đi cùng từ gốc sang tới đây.
            "vocabulary": [{"tu": t["tu"], "ipa": t["ipa"], "nghia": t["nghia"],
                            "so_nhieu": t.get("so_nhieu"),
                            "dang_ing": t.get("dang_ing"),
                            "dang_qk": t.get("dang_qk"),
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
            # Hội thoại: việc CUỐI của chuỗi nghe → hiểu → ráp câu → gõ → nói.
            # Bé phải nghe người kia nói gì rồi mới biết mình đáp gì.
            "hoiThoai": u.get("kich_ban_noi"),
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
        "assessment": {"passRule": "≥ 4/5", "items": sat_hach(u, cau, hinh_cua)},
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
        # Video của bài — app hỏi chỗ này chứ KHÔNG tự đoán tên tệp. Đoán tên là
        # chỗ lệch câm: bài hai mẫu câu ra `_cau1/_cau2`, bài hỏi–đáp ra `_hoi/_dap`,
        # bài một mẫu ra `_cau`. Bộ sinh biết chắc, giao diện thì không.
        "video": _ten_video(u, ma_bai, vai_ten, tu),
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

    # ── LỜI DẪN CỦA CÂU HỎI cũng phải có tiếng ──
    # Bản cũ không gom mấy dòng này: clip lời dẫn có mặt trên đĩa là do sinh tay từ
    # một đợt trước. Nên thêm MỘT lời dẫn mới là nó lặng lẽ không có clip — bé bấm
    # vào câu, không nghe thấy gì, mà bé sáu tuổi chưa đọc được chữ thì đứng luôn.
    # Đã suýt dính đúng thế khi tách "Chọn từ điền vào chỗ trống." ra khỏi
    # "Nhìn hình rồi chọn từ điền vào chỗ trống." trong đợt sửa hình 14-08.
    #
    # Gom theo `am` đã khai trong chính câu hỏi, không gõ lại danh sách ở đây: gõ
    # lại là hai bảng, mà hai bảng thì sớm muộn lệch.
    DAN = {am_id("loi", DAN_DIEN): DAN_DIEN,
           am_id("loi", DAN_DIEN_KHONG_HINH): DAN_DIEN_KHONG_HINH}
    for pool in bai["practice"]["pools"].values():
        for x in pool:
            if x.get("am") in DAN:
                them("loi", DAN[x["am"]], "vi")
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=1, choices=[1, 2, 3, 4, 5])
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
                       chuan.get("sua_slot") or {}, chuan.get("chuong") or {},
                       chuan.get("vai_ten") or {})
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
