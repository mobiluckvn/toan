#!/usr/bin/env python3
"""DỰNG BÀI ĐỌC HIỂU NGẮN — mỗi chương một bài.

    python3 tools/sinh_dochieu_tienganh.py --lop 3
    python3 tools/sinh_dochieu_tienganh.py --lop 3 --thieu /tmp/loi.json   # lời chưa có clip

Bác chốt 18-08-2026: mỗi chương một đoạn đọc 4–6 câu, dựng CHỈ từ vốn từ đã học
(lớp 1 + lớp 2 + lớp 3 tính tới chương ấy), rồi hỏi Ý CHÍNH và hỏi CHI TIẾT.

── LUẬT SỐ MỘT: KHÔNG BỊA CÂU TIẾNG ANH ──

Đoạn đọc KHÔNG phải văn mới. Mỗi dòng là một câu SẴN CÓ của chính bốn bài trong
chương (`canonicalExamples`), cắt đôi ở cặp hỏi–đáp. Đây là luật xuyên suốt cả môn,
và đã có hai lần trả giá: mô hình sinh `"Bye, bike."` (nhét đồ vật vào ô tên người),
và bộ sinh bài đầu tiên đẻ ra `"facePoint to your hand."` Câu có sẵn thì:

  · chắc chắn đúng ngữ pháp — người soạn sách đã duyệt;
  · chắc chắn nằm trong vốn từ đã học;
  · và CÓ SẴN CLIP TIẾNG, không phải chạy lại cả dây chuyền TTS cho một đoạn văn.

Xếp bốn tới sáu câu ấy cạnh nhau theo đúng thứ tự unit thì tự nó thành một mẩu hội
thoại đọc được:

    Hello. I'm Ben.
    Hello, Ben. I'm Lucy.
    How are you?
    Fine, thank you.

── BỐN CÂU HỎI, BA DẠNG, VÀ VÌ SAO ĐÚNG BA DẠNG ẤY ──

**Ý chính** — "Bài đọc này nói về chuyện gì?", bốn lựa chọn là TÊN CHƯƠNG (tiếng
Việt) của chương này và ba chương khác. Hỏi ý chính mà đáp án là một câu trong bài
thì đó không phải ý chính, đó là chi tiết. Tên chương chính là ý chính, và nó có
sẵn — không phải soạn thêm dòng nào.

**Chi tiết · câu nào CÓ trong bài** (hai câu) — ba tới bốn câu tiếng Anh, mồi là câu
CÙNG KHUÔN khác từ (`I have a pen.` ↔ `I have a book.`). Mồi cùng khuôn buộc bé phải
đọc lại đoạn để tìm đúng chi tiết; mồi khác khuôn thì bé loại được bằng hình dạng
câu, không cần đọc lấy một chữ.

**Chi tiết · có hay không** — một câu KHÔNG có trong đoạn, hỏi "câu này có trong bài
đọc không?", hai lựa chọn Có/Không. Đáp án cố ý là KHÔNG: ba câu trên đáp án đều là
"câu CÓ trong bài", nên câu cuối mà cũng "có" nốt thì bé qua được bằng cách bấm bừa
một dáng.

Cả bốn đều KHÔNG đòi bé dịch, vì cả quyển chưa dạy dịch câu bao giờ.

── CHỮ LẠ ──
`_kho_tu()` dựng túi từ ĐÃ HỌC TỚI CHƯƠNG ẤY. Câu nào có chữ ngoài túi thì bị loại
ngay tại đây, và `test/tienganh_dochieu.test.mjs` hỏi lại lần nữa trên tệp đã ghi —
bộ sinh tự kiểm lấy mình thì chẳng chứng minh được gì.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kho_cau_tienganh import cau_tich_luy  # noqa: E402

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}

# ── ĐOẠN NGẮN Ở ĐẦU QUYỂN, DÀI DẦN VỀ CUỐI ── (bác chốt 19-08-2026)
#
# "Mấy bài đầu bạn có thể viết một đoạn ngắn thôi rồi tăng dần độ dài về cuối."
#
# Đúng: unit 0 bé mới có mười một từ, mà bắt đọc bảy dòng thì bảy dòng ấy chỉ có thể
# là bảy biến thể của một câu. Cuối quyển bé đã có gần hai trăm từ, bốn dòng thì phí.
# Nên độ dài suy từ VỊ TRÍ của unit trong quyển, không phải một con số chung.
DONG_DAU_QUYEN = 4
DONG_CUOI_QUYEN = 8


def so_dong_cua(unit: int, unit_cuoi: int) -> int:
    """Đoạn của unit này nên dài mấy dòng."""
    if unit_cuoi <= 0:
        return DONG_DAU_QUYEN
    phan = max(0.0, min(1.0, unit / unit_cuoi))
    return round(DONG_DAU_QUYEN + (DONG_CUOI_QUYEN - DONG_DAU_QUYEN) * phan)


SO_DONG_TOI_DA = DONG_CUOI_QUYEN
# Bài theo CHƯƠNG gom bốn unit, mà một lượt đối đáp ăn HAI dòng — sáu dòng chỉ đủ
# ba lượt, tức là chưa đi hết chương đã hết chỗ. Tám dòng là bốn lượt, vừa đủ để
# câu hỏi "bài đọc nói về chuyện gì" có nghĩa là ý chính của cả chương.
# Bài chương gom bốn unit nên luôn dài hơn bài unit, và cũng dài dần theo chương.
DONG_DAU_CHUONG = 6
DONG_CUOI_CHUONG = 10


def so_dong_chuong(c: int, c_cuoi: int) -> int:
    if c_cuoi <= 1:
        return DONG_DAU_CHUONG
    phan = max(0.0, min(1.0, (c - 1) / (c_cuoi - 1)))
    return round(DONG_DAU_CHUONG + (DONG_CUOI_CHUONG - DONG_DAU_CHUONG) * phan)


SO_DONG_TOI_DA_CHUONG = DONG_CUOI_CHUONG
SO_DONG_TOI_THIEU = 4
# Bài theo UNIT chỉ có vốn câu của một unit, nên cho phép đoạn ngắn hơn một dòng.
# Ba câu vẫn là một đoạn đọc; đòi đủ bốn thì ba unit mất hẳn bài đọc.
SO_DONG_TOI_THIEU_UNIT = 3
SO_CAU_TOI_THIEU = 3    # dưới ngần này thì bỏ bài — một câu ý chính không thành bài đọc
# Qua bài khi sai NHIỀU NHẤT MỘT CÂU. Không đòi đúng hết: đây là bài đọc đầu tiên
# của cả môn, và sai một câu chi tiết rồi phải làm lại từ đầu thì bé bỏ.


def ma_am(loai: str, chu: str) -> str:
    """Cùng luật đặt mã với `tools/tts/sinh_am.py`. Lệch một ký tự là nút nghe câm."""
    sach = "".join(c if c.isalnum() else "_" for c in str(chu).lower()).strip("_")
    return f"{loai}_{sach}"[:60]


def chu_trong(s: str) -> list[str]:
    return re.findall(r"[a-z']+", str(s or "").lower())


def _kho_tu(chuans: list[dict], den_chuong: int | None, chuong_cua: dict) -> set[str]:
    """Túi từ bé ĐÃ HỌC — cùng phép dựng với `tienganh_bai.test.mjs`.

    Gồm: từ vựng (cả dạng số nhiều và -ing) · chữ trong CÔNG THỨC ngoài phần ô
    trống · và ba nhóm từ phụ (`số đếm · màu · tên`). Quyển lớp 1·2 vào trọn vẹn;
    quyển đang xét chỉ tính tới chương `den_chuong`.
    """
    kho: set[str] = set()

    def nap(s):
        kho.update(chu_trong(s))

    for i, chuan in enumerate(chuans):
        cuoi = (i == len(chuans) - 1)
        for u in chuan["unit"]:
            if cuoi and den_chuong is not None and chuong_cua.get(u["so"], 99) > den_chuong:
                continue
            for x in u["tu"]:
                for k in ("tu", "so_it", "so_nhieu", "dang_ing"):
                    nap(x.get(k))
            for m in u["mau_cau"]:
                nap(re.sub(r"\[[^\]]*\]", " ", str(m.get("cong_thuc") or "")))
                nap(m.get("vi_du"))
        for nhom in ("so_dem", "mau", "ten"):
            for m in ((chuan.get("them") or {}).get(nhom) or {}).get("muc") or []:
                nap(m if isinstance(m, str) else m.get("word"))
    return kho


def _tach_doi(c: str) -> list[str]:
    """`"How are you? - Fine, thank you."` → hai dòng. Cặp hỏi–đáp là HAI lượt nói.

    Vế đáp còn có thể là cặp phương án `"Yes, I do. / No, I don't."` — đoạn đọc thì
    phải chọn MỘT, vì không ai vừa đồng ý vừa từ chối trong một câu. Lấy vế đầu,
    cùng luật với `cau_noi_duoc()` của bộ dựng video.
    """
    ds = [x.strip() for x in str(c or "").split(" - ") if x.strip()]
    return [x.split(" / ")[0].strip() for x in ds]


def _dang(cau: str) -> tuple:
    """Khuôn của một câu: chữ đầu + số chữ. Cùng khuôn nghĩa là cùng công thức."""
    return (cau.split()[0].lower(), len(cau.split())) if cau.split() else ("", 0)


# Nhiều nhất hai dòng CÙNG KHUÔN trong một đoạn.
#
# U17 khai 4 ví dụ "She has a …" và đoạn ăn cả bốn, nên KHÔNG còn câu nào cùng khuôn
# để làm mồi, mà khoét chữ thì chỗ trống nào cũng có hai đáp án đúng. Kết quả: unit
# ấy chỉ dựng được câu ý chính, tức là mất bài đọc. Chừa lại hai câu là vừa đủ mồi,
# và đoạn cũng đỡ đọc như đọc bảng cửu chương.
CUNG_KHUON_TOI_DA = 2


# Ai xưng tên, ai được gọi tên — hai phép dò nhỏ, nhưng chúng là thứ giữ cho đoạn
# hội thoại không tự mâu thuẫn. Xem `_hop_vai`.
TU_XUNG = re.compile(r"\b(?:I'm|I am|My name's|My name is)\s+((?:Ms |Mr )?[A-Z][a-z]+)")
GOI_TEN = re.compile(r"\b(?:Hello|Hi|Bye|Goodbye),\s+((?:Ms |Mr )?[A-Z][a-z]+)")


def _hop_vai(cau: str, toi: str, ban: str) -> bool:
    """Câu này có hợp với MIỆNG người nói `toi` không (bạn kia là `ban`)?

    Hai luật, và cả hai đều là chỗ đoạn cũ đọc lên thấy vô lý ngay:

      · TỰ XƯNG phải đúng tên MÌNH. Đoạn cũ của lớp 3 unit 1 có bốn dòng, ba dòng
        là Lucy tự giới thiệu với ba người khác nhau:

            Hello. I'm Ben.
            Hello. I'm Lucy.
            Hello, Minh. I'm Lucy.      ← Lucy giới thiệu lần hai
            Hello, Ben. I'm Lucy.       ← lần ba

      · GỌI TÊN phải gọi người ĐANG NÓI CHUYỆN VỚI MÌNH. "Hello, Minh." trong khi
        Minh không có mặt trong đoạn thì bé đọc xong không biết Minh là ai.

    Cả hai lỗi ấy KHÔNG có chữ nào sai: từ nào cũng đã học, câu nào cũng của sách.
    Cổng cũ soi TỪNG DÒNG nên dòng nào cũng qua — chỉ đọc CẢ ĐOẠN mới thấy.
    """
    for m in TU_XUNG.findall(cau):
        if m != toi:
            return False
    for m in GOI_TEN.findall(cau):
        if m != ban:
            return False
    return True


def _hai_ban(nguon: list[dict], ten_sach: list[str], xoay: int = 0) -> tuple[str, str]:
    """Chọn TÊN cho hai bạn nói chuyện.

    Bạn ĐÁP là người tự xưng tên trong câu ví dụ; bạn HỎI cũng phải là một người có
    câu tự xưng, vì lúc đổi vai chính bạn ấy phải đáp "My name's …" — mà câu ấy chỉ
    tồn tại cho những cái tên sách đã viết. Hết mới mượn tên trong `them.ten`.
    """
    xung, goi = [], []
    for m in nguon:
        for c in m["vidu"] + [x for x in (m["hoi"], m["dap"]) if x]:
            xung += TU_XUNG.findall(c)
            goi += GOI_TEN.findall(c)
    du = [x for x in dict.fromkeys(xung + goi + list(ten_sach)) if x]
    tu_xung = list(dict.fromkeys(xung))
    # ⚠ XOAY VÒNG THEO UNIT. Bác bắt 19-08: "sao nhiều câu lặp lại quá đi kiểu như
    # Hello, I'm ben". Một phần là do nguồn câu hẹp (đã chữa), nhưng phần còn lại là
    # do CHỌN LUÔN TÊN ĐẦU DANH SÁCH: hai mươi bài đọc thì cả hai mươi đều mở bằng
    # "Hi, I'm Bill. / Hello. I'm Mai." Bé đọc bài thứ ba là thuộc lòng hai dòng ấy
    # và bỏ qua không đọc nữa.
    #
    # Xoay theo số unit chứ không random: chạy hai lần phải ra đúng một tệp, nếu
    # không thì mỗi lần dựng lại là 20 bài đọc đổi hết và clip tiếng phải sinh lại.
    if tu_xung:
        tu_xung = tu_xung[xoay % len(tu_xung):] + tu_xung[:xoay % len(tu_xung)]
    if du:
        du = du[xoay % len(du):] + du[:xoay % len(du)]
    b_ = (tu_xung[0] if tu_xung else (du[0] if du else "Lucy"))
    a_ = next((x for x in tu_xung[1:] + list(dict.fromkeys(goi)) + du if x != b_),
              None) or "Ben"
    return a_, b_


NAM = re.compile(r"\b(he|his|him|brother|father|grandfather|uncle|Mr [A-Z][a-z]+)\b", re.I)
NU = re.compile(r"\b(she|her|hers|sister|mother|grandmother|aunt|Ms [A-Z][a-z]+)\b", re.I)


def _gioi(cau: str) -> str | None:
    """Câu này nói về nam hay nữ? Không rõ thì `None`."""
    co_nam, co_nu = bool(NAM.search(cau)), bool(NU.search(cau))
    return "nam" if co_nam and not co_nu else ("nu" if co_nu and not co_nam else None)


def _hop_gioi(cau: str, dong: list[dict]) -> bool:
    """Câu này có mâu thuẫn giới tính với dòng ngay trước không?

    ⚠ LỖI THẬT, và nó chỉ lộ khi đọc HAI DÒNG LIỀN NHAU:

        Mai:  Who's this?
        Bill: It's my sister.
        Mai:  How old is he?        ← sister là "she"

    Từng dòng đều là câu đúng của sách, mọi chữ đều đã học, cổng soi từng dòng thì
    dòng nào cũng qua. Mở cả kho câu tích luỹ ra càng dễ dính, vì nay hai lượt cạnh
    nhau có thể đến từ hai unit khác nhau.

    Chỉ soi ngược MỘT dòng: xa hơn thì trong hội thoại thật người ta đổi chủ đề, và
    chặn quá tay là mất câu vô cớ.
    """
    g = _gioi(cau)
    if not g or not dong:
        return True
    truoc = _gioi(dong[-1]["cau"])
    return truoc is None or truoc == g


def _hoi_thoai(nguon: list[dict], ten_sach: list[str], toi_da: int,
               xoay: int = 0, chuong_dich: int | None = None) -> list[dict]:
    """ĐOẠN HỘI THOẠI giữa hai bạn — trả `[{"cau", "ai"}]`.

    ══ NGUỒN CÂU LÀ CẢ KHO TÍCH LUỸ ══ (bác chốt 19-08-2026)

    Bác đọc rồi bảo: "sao nhiều câu lặp lại quá đi kiểu như Hello, I'm ben .... Bài
    đọc bạn nên dùng vốn câu tích luỹ từ lớp 1 đến bài đó của lớp 3 chứ không nhất
    thiết là trong bài đó của lớp 3."

    Đúng, và con số nói thẳng: tính tới unit 5 lớp 3, bé đã học 52 MẪU CÂU (135 câu
    dùng được), mà bản trước chỉ lấy đúng 2 mẫu của chính unit ấy. Hai mẫu mà phải
    rải ra bốn tới sáu dòng thì không còn đường nào ngoài lặp — bốn ví dụ của unit 1
    chỉ khác nhau ở cái tên, nên đoạn nào cũng "Hello. I'm Ben. / Hello. I'm Lucy."

    Nay `kho_cau_tienganh.cau_tich_luy` đưa cả kho vào, và luật xếp đoạn đổi hẳn:
    MỖI MẪU CHỈ MỘT LƯỢT. Trước phải vét nhiều ví dụ của cùng một mẫu vì không có gì
    khác; nay dư mẫu nên không bao giờ phải lặp khuôn.

    ── ĐOẠN VẪN PHẢI LÀ CỦA UNIT NÀY ──

    Mở cả kho ra mà xếp bừa thì bài đọc của unit 5 lại toàn chuyện lớp 1. Nên thứ
    tự cố định:

        chào  →  mẫu của CHÍNH unit (`moi`)  →  mẫu cũ, gần nhất trước  →  tạm biệt

    Câu mới là trọng tâm, câu cũ là phần ôn, và hai đầu là chỗ mở/đóng cho đoạn
    thành một mẩu chuyện có đầu có cuối.

    ── HAI LUẬT GIỮ CHO ĐOẠN KHÔNG TỰ MÂU THUẪN ──
    Câu tự xưng phải đúng tên người nói, câu gọi tên phải gọi bạn kia (`_hop_vai`).
    Thiếu chúng thì ra đoạn cũ: Lucy tự giới thiệu ba lần với ba người khác nhau,
    và chào "Hello, Minh." trong khi Minh không hề có mặt.
    """
    a_, b_ = _hai_ban(nguon, ten_sach, xoay)
    dong: list[dict] = []

    def them_duoc(cau: str) -> bool:
        if len(dong) >= toi_da or any(d["cau"] == cau for d in dong):
            return False
        return sum(1 for d in dong if _dang(d["cau"]) == _dang(cau)) < CUNG_KHUON_TOI_DA

    # Phần giữa xếp MỚI trước, rồi cũ theo unit giảm dần — unit ngay trước thường
    # cùng chương, cùng chủ đề, nên đọc liền mạch hơn là lôi bài lớp 1 lên.
    # ⚠ XÃ GIAO KHÔNG VÀO BÀI ĐỌC. Bác chốt 19-08: "Cả một chương bạn toàn có nói về
    # mấy câu chào hỏi. […] Đọc nên là một bài đọc ngắn có thông tin." Đoạn chỉ dài
    # 4–8 dòng, mà chào mất hai dòng và tạm biệt mất một — nghĩa là gần một nửa bài
    # đọc không mang mẩu thông tin nào. Chào hỏi vẫn còn ở PHÒNG LUYỆN NÓI và ở
    # nhóm "Mở đầu" của BÀI VIẾT; đó mới là chỗ của nó.
    giua = [m for m in nguon if not m.get("xaGiao")]
    # ⚠ CÙNG CHƯƠNG TRƯỚC ĐÃ. Chỉ xếp theo unit giảm dần thì đoạn của unit 11 kết
    # bằng "I have a pen." của lớp 1 — câu đúng, đã học, nhưng chẳng liên quan gì
    # tới gia đình. Bác gọi đúng tên: "đoạn văn nó phải có ý nghĩa một chút".
    # Cùng chương nghĩa là cùng chủ đề sách đã gom sẵn, nên gần như miễn phí.
    giua.sort(key=lambda m: (not m["moi"],
                             m.get("chuong") != chuong_dich,
                             -m["lop"], -m["unit"]))

    def dat(m: dict, chi_mot: bool = False) -> None:
        """Đặt một mẫu thành một hoặc hai dòng. Mỗi mẫu dùng ĐÚNG MỘT LẦN."""
        hoi, dap = m["hoi"], m["dap"]
        # ── CÙNG MỘT CÂU HỎI, HAI MẪU ĐÁP ──
        # Unit 5 có hai mẫu chung câu hỏi "What's your hobby?" ("It's cooking." và
        # "I like singing."). Chặn câu hỏi trùng thì mẫu thứ hai không bao giờ được
        # dạy. Nên hỏi một lần, rồi vế đáp thứ hai thành một dòng NÓI THÊM của
        # chính bạn ấy — đúng cách người ta nói: "It's cooking. I like cooking."
        ai_ep = None
        if hoi and any(d["cau"] == hoi for d in dong):
            # Ai đã ĐÁP câu hỏi ấy thì chính người đó nói thêm. Để luân phiên như
            # câu đơn bình thường thì ra "Mai: I like singing." — Mai tự trả lời
            # câu Mai vừa hỏi, và Bill thì im. Đọc lên thấy sai ngay.
            i = next(k for k, d in enumerate(dong) if d["cau"] == hoi)
            ai_ep = dong[i + 1]["ai"] if i + 1 < len(dong) else None
            hoi = None
        if hoi and not chi_mot:
            if len(dong) + 2 > toi_da:
                return
            if not (_hop_vai(hoi, a_, b_) and _hop_vai(dap, b_, a_)):
                return
            if not _hop_gioi(hoi, dong):
                return
            if not them_duoc(hoi) or any(d["cau"] == dap for d in dong):
                return
            dong.append({"cau": hoi, "ai": a_})
            dong.append({"cau": dap, "ai": b_})
            return
        # Câu đơn: ưu tiên người CHƯA nói ở dòng trên, để hai bên thay phiên.
        vua = dong[-1]["ai"] if dong else None
        for c in ([dap] + [x for x in m["vidu"] if x != dap]):
            if not _hop_gioi(c, dong):
                continue
            thu = [ai_ep] if ai_ep else ([a_, b_] if vua == b_ else [b_, a_])
            for ai in thu:
                if _hop_vai(c, ai, a_ if ai == b_ else b_) and them_duoc(c):
                    dong.append({"cau": c, "ai": ai})
                    return

    # ── VÒNG 1: CHỈ CÂU CÙNG CHỦ ĐỀ ──
    # Đoạn NGẮN còn hơn đoạn LẠC. Lấp cho đủ số dòng bằng câu của chương khác thì ra
    # đoạn kết bằng "I have a pen." trong một bài về gia đình — đúng cái bác gọi là
    # "chào hỏi linh tinh", chỉ đổi chủ đề. Nên chỉ khi chưa đạt ngưỡng TỐI THIỂU
    # mới mở ra ngoài chương.
    cung_chu_de = [m for m in giua
                   if m["moi"] or (chuong_dich is not None
                                   and m.get("chuong") == chuong_dich
                                   and m["lop"] == max(x["lop"] for x in giua))]
    for m in cung_chu_de:
        if len(dong) >= toi_da:
            break
        dat(m)

    # ── VÒNG 2: nới ra, chỉ khi đoạn còn quá ngắn ──
    if len(dong) < SO_DONG_TOI_THIEU_UNIT:
        for m in giua:
            if len(dong) >= toi_da:
                break
            dat(m)

    # Hết mẫu mà đoạn vẫn ngắn thì vét thêm cách điền khác — chỉ khi thiếu, để
    #    đoạn bình thường không bị lắp thêm dòng cùng khuôn.
    if len(dong) < SO_DONG_TOI_THIEU_UNIT:
        for m in giua:
            for c in m["vidu"]:
                vua = dong[-1]["ai"] if dong else None
                for ai in ([a_, b_] if vua == b_ else [b_, a_]):
                    if _hop_vai(c, ai, a_ if ai == b_ else b_) and them_duoc(c):
                        dong.append({"cau": c, "ai": ai})
                        break
    return dong


def _ten_unit(b: dict) -> str:
    """`"Unit 5 · Sở thích của mình · My hobbies"` → `"Sở thích của mình"`.

    Lấy mẩu TIẾNG VIỆT ở giữa: mẩu đầu là số hiệu, mẩu cuối là tên tiếng Anh của
    sách. Câu hỏi ý chính hỏi bằng tiếng Việt nên đáp án cũng phải tiếng Việt."""
    phan = [x.strip() for x in str(b.get("title") or "").split("·")]
    return phan[1] if len(phan) > 2 else (phan[-1] if phan else "?")


def _cung_khuon(bais: list[dict], cau: str, tru: set[str]) -> list[str]:
    """Mồi nhử cho câu hỏi "câu nào CÓ trong bài đọc?".

    ══ ĐỔI HẲN CHIỀU 19-08-2026 ══

    Bác thử rồi bảo: "Câu hỏi phải đảm bảo con dễ dàng trả lời chứ nhiều câu trả lời
    ý same same nhau rất khó cho con chọn câu trả lời đúng."

    Bản cũ CỐ Ý lấy mồi CÙNG KHUÔN — `It's a nose.` ↔ `It's a hair.` — với lý do
    "mồi cùng khuôn buộc bé phải đọc lại đoạn để tìm đúng chi tiết". Lý do ấy đúng
    với một bài kiểm tra, sai với bé lớp 3 mới tập đọc: bốn lựa chọn chỉ khác nhau
    một chữ ở giữa thì việc bé làm không còn là ĐỌC HIỂU nữa mà là dò chính tả, và
    bé đọc hiểu đúng vẫn chọn sai.

    Nay mồi phải KHÁC RÕ: khác chữ mở đầu, hoặc lệch hẳn độ dài. Bé hiểu đoạn thì
    loại được ngay; bé không hiểu thì vẫn phải đọc, vì cả bốn đều là câu đã học và
    đều đúng ngữ pháp.

    Vẫn giữ tên hàm cũ để chỗ gọi khỏi đổi — cái đổi là LUẬT CHỌN, không phải chỗ
    dùng.
    """
    ra: list[str] = []
    da_dung_khuon = {_dang(cau)}          # kể cả khuôn của chính ĐÁP ÁN
    for b in bais:
        for c in b["knowledgeCore"].get("canonicalExamples") or []:
            for x in _tach_doi(c):
                if x in tru or x in ra or x == cau:
                    continue
                # ⚠ BA MỒI CŨNG PHẢI KHÁC NHAU, không chỉ khác đáp án.
                #
                # Bản đầu của phép sửa này mới chỉ đòi "mồi khác đáp án", và nó ra:
                #
                #     It's a face. · It's a hair. · It's a hand. · What's this? ✓
                #
                # Ba mồi giống hệt nhau, đáp án lẻ loi — bé chọn đúng bằng HÌNH DẠNG
                # mà không cần đọc lấy một chữ. Dễ, nhưng dễ vì đoán chứ không phải
                # vì hiểu. Mỗi lựa chọn một khuôn thì bé buộc phải nhớ đoạn vừa đọc,
                # mà vẫn không phải dò chính tả giữa hai câu khác nhau một chữ.
                if _dang(x) in da_dung_khuon:
                    continue
                da_dung_khuon.add(_dang(x))
                ra.append(x)
    return ra


def _khoet(cau: str, d: str) -> str:
    return re.sub(rf"\b{re.escape(d)}\b", "___", cau, count=1, flags=re.I)


def _mo_ho(cau: str, d: str, doan: list[str], tu: list[str]) -> bool:
    """Khoét chữ `d` khỏi `cau` xong, có DÒNG KHÁC trong đoạn cũng ra đúng chỗ trống ấy không?

    ⚠ Không hỏi câu này thì U0 ra hai câu y hệt nhau — "Trong bài có câu 'It's ___.'"
    — trong khi đoạn có cả "It's five." lẫn "It's one.". Hai đáp án cùng đúng, mà máy
    chỉ nhận một: bé đọc kỹ vẫn bị chấm sai.
    """
    k = _khoet(cau, d)
    for x in doan:
        if x == cau:
            continue
        for t in tu:
            if t.lower() == d.lower():
                continue
            if re.search(rf"\b{re.escape(t)}\b", x, re.I) and _khoet(x, t) == k:
                return True
    return False


def _cau_dien(doan: list[str], bais: list[dict], da_dung: set) -> dict | None:
    """Khoét một chữ khỏi MỘT DÒNG của đoạn rồi hỏi chữ ấy là gì.

    Vì sao cần dạng này: câu "câu nào CÓ trong bài" lấy mồi từ chính vốn câu của
    sách, mà một unit chỉ có 8 câu ví dụ — đoạn đọc ăn hết 4–6 câu thì không còn đủ
    ba mồi. Bảy unit vì thế chỉ dựng được đúng câu Ý CHÍNH, tức là không thành bài
    đọc. Dạng điền chữ lấy mồi từ VỐN TỪ (9–15 từ mỗi unit) nên lúc nào cũng có.

    KHÔNG gắn clip: nghe câu là nghe luôn chữ bị khoét — bé khỏi cần đọc.
    """
    tu = [t["tu"] for b in bais for t in b["knowledgeCore"]["vocabulary"]]
    for cau in doan:
        if cau in da_dung:          # mỗi dòng chỉ hỏi một lần, cho đỡ lặp
            continue
        # Khoét từ DÀI NHẤT khớp trước, để `pen` không cướp chỗ của `pencil`;
        # trong số ấy ưu tiên chữ CHƯA từng làm đáp án.
        hop = sorted((t for t in dict.fromkeys(tu)
                      if re.search(rf"\b{re.escape(t)}\b", cau, re.I)),
                     key=lambda t: (t.lower() in da_dung, -len(t)))
        d = next((t for t in hop if not _mo_ho(cau, t, doan, tu)), None)
        if not d:
            continue
        moi = [t for t in dict.fromkeys(tu) if t.lower() != d.lower()][:3]
        if len(moi) < 2:
            continue
        da_dung.add(cau)
        da_dung.add(d.lower())
        return {
            "id": "", "loai": "chiTiet",
            "text": f"Trong bài có câu “{_khoet(cau, d)}”. Chỗ trống là chữ nào?",
            "format": "chon",
            "choices": _tron(d, moi),
            "answerKey": {"choice": d},
            "solutionNarrative": f"“{cau}” — con đọc lại đoạn trên xem nhé.",
        }
    return None


def _cau_hoi(dung_ten: str, khac_ten: list[str], doan: list[str],
             bais: list[dict]) -> list[dict]:
    """`dung_ten` là chủ đề của chính bài đọc; `khac_ten` là ba chủ đề để làm mồi.

    Bài theo CHƯƠNG lấy tên chương, bài theo UNIT lấy tên unit — cùng một phép hỏi
    ý chính, chỉ khác cái tên đem so. Nhét riêng nhánh cho từng phạm vi thì hai
    nhánh sớm muộn lệch nhau."""
    ra: list[dict] = []

    # ── Q1 · Ý CHÍNH ──
    ra.append({
        "id": "D1", "loai": "yChinh",
        "text": "Bài đọc này nói về chuyện gì?",
        "format": "chon",
        "choices": _tron(dung_ten, khac_ten[:3]),
        "answerKey": {"choice": dung_ten},
        "solutionNarrative": f"Cả đoạn nói về {dung_ten.lower()}.",
    })

    # ── Q2·Q3 · CHI TIẾT · câu nào CÓ trong bài ──
    # Mồi đã dùng ở câu trước KHÔNG được dùng lại làm mồi câu sau: bé vừa thấy nó
    # bị loại thì lần thứ hai nó không còn nhử được ai.
    trong = set(doan)
    for x in doan:
        if len(ra) >= 3:
            break
        # Hai mồi cũng dựng được câu (ba lựa chọn). Đòi đủ ba mồi thì hai chương
        # cuối mất hẳn câu chi tiết thứ hai, chỉ vì mỗi bài chỉ khai 8 câu ví dụ và
        # số ấy chia cho hai mẫu câu.
        moi = _cung_khuon(bais, x, trong)
        if len(moi) < 2:
            continue
        ra.append({
            "id": f"D{len(ra) + 1}", "loai": "chiTiet",
            "text": "Câu nào CÓ trong bài đọc?",
            "format": "chon",
            "choices": _tron(x, moi[:3]),
            # ⚠ KHÔNG có nút nghe ở câu này. `am` của câu hỏi là clip của ĐÁP ÁN —
            # bé bấm nghe là được đọc thẳng câu đúng cho, và câu hỏi "đọc lại đoạn
            # để tìm" thành câu hỏi "nghe rồi bấm". Đúng cái màn này sinh ra để dạy
            # thì bị chính nút nghe ấy làm hỏng. Sáu dòng của đoạn văn ở trên vẫn có
            # nút nghe riêng — chỗ ấy nghe là để ĐỌC được, không phải để lấy đáp án.
            "answerKey": {"choice": x},
            "solutionNarrative": f"“{x}” — con đọc lại đoạn trên xem nhé.",
        })
        trong = trong | set(moi[:3])

    # ── Q4 · CHI TIẾT · đúng/sai ──
    # Đáp án SAI, cố ý: ba câu trên đáp án đều là "câu có trong bài", nên câu cuối
    # mà cũng đúng nốt thì bé qua được bằng cách bấm bừa một dáng.
    ngoai = next((c for x in doan
                  for c in _cung_khuon(bais, x, set(doan)) if c not in doan), None)
    if ngoai:
        # Hỏi bằng HAI LỰA CHỌN chứ không dùng `format: "tf"`. Bộ chơi `tf` của môn
        # này là `CauNgheNhin` — nghe một từ, NHÌN MỘT HÌNH, hình ấy có đúng không —
        # nó luôn vẽ một ô hình và luôn hỏi "Hình này có đúng không?". Đưa câu chữ
        # vào đó thì bé thấy một dấu ❔ to tướng và một câu hỏi không ăn nhập.
        # Còn `CauHoi` không có `choices` thì rơi vào Ô GÕ CHỮ. Nên: hai lựa chọn.
        ra.append({
            "id": f"D{len(ra) + 1}", "loai": "chiTiet",
            "text": f"Câu “{ngoai}” có trong bài đọc không?",
            "format": "chon",
            "choices": ["Có", "Không"],
            "am": ma_am("cau", ngoai), "amChu": ngoai,
            "answerKey": {"choice": "Không"},
            "solutionNarrative": f"KHÔNG — đoạn trên không có câu “{ngoai}”.",
        })

    # ── bù bằng câu ĐIỀN CHỮ cho đủ số câu tối thiểu ──
    da_dung: set = set()
    while len(ra) < SO_CAU_TOI_THIEU:
        c = _cau_dien(doan, bais, da_dung)
        if not c:
            break
        ra.append(c)
    for i, c in enumerate(ra, 1):
        c["id"] = f"D{i}"
    return ra


def _tron(dung: str, moi: list[str]) -> list[str]:
    """Xếp đáp án vào giữa đám mồi. KHÔNG random — chạy hai lần phải ra một tệp."""
    ds = list(moi)
    ds.insert(min(len(ds), (len(dung) + len(ds)) % (len(ds) + 1)), dung)
    return ds


def dung(lop: int) -> tuple[list[dict], list[dict]]:
    """Trả (danh mục bài đọc, danh sách lời cần có clip)."""
    tm = GOC / f"web/public/content/{QUYEN[lop]}"
    bais = [json.loads(p.read_text("utf8"))
            for p in sorted(tm.glob(f"DL_{QUYEN[lop].upper()}_B*.json"))]
    chuans = [json.loads((GOC / f"data/tienganh/chuan_lop{i}.json").read_text("utf8"))
              for i in range(1, lop + 1)]

    theo_chuong: dict[int, list[dict]] = {}
    for b in bais:
        theo_chuong.setdefault(b["chuong"], []).append(b)
    ten_chuong = {c: v[0]["tenChuong"] for c, v in theo_chuong.items()}
    # unit số → chương, để cắt túi từ đúng chỗ
    chuong_cua = {b["so"]: b["chuong"] for b in bais}

    ten_unit = {b["so"]: _ten_unit(b) for b in bais}

    # Tên người SÁCH dạy — để đặt vai cho hai bạn khi chính unit ấy không có câu
    # nào xưng tên. Lấy từ bản chuẩn chứ không gõ tay một danh sách: gõ tay thì
    # thêm quyển mới là lệch, mà lệch ở đây nghĩa là đoạn hội thoại gọi tên một
    # bạn chưa ai dạy.
    ten_sach = [x if isinstance(x, str) else x.get("word")
                for cn in chuans
                for x in (((cn.get("them") or {}).get("ten") or {}).get("muc") or [])]
    ten_sach = [x for x in dict.fromkeys(ten_sach) if x]

    ra, loi = [], {}

    def them(ky, doan, ds, dung_ten, khac_ten):
        # `doan` nay là `[{"cau", "ai"}]` — mỗi dòng có NGƯỜI NÓI. Câu hỏi thì vẫn
        # chỉ cần chữ, nên rút ra một danh sách chuỗi cho `_cau_hoi`.
        chu_doan = [d["cau"] for d in doan]
        ky["doan"] = [{"cau": d["cau"], "ai": d["ai"], "am": ma_am("cau", d["cau"])}
                      for d in doan]
        ky["cau"] = _cau_hoi(dung_ten, khac_ten, chu_doan, ds)
        ky["soCau"] = len(ky["cau"])
        if ky["soCau"] < SO_CAU_TOI_THIEU:
            print(f"  ⚠ {ky['id']}: chỉ dựng được {ky['soCau']} câu hỏi, bỏ qua")
            return
        # `need` KHÔNG được vượt số câu — từng ra "cần 2/1", tức là bài không bao
        # giờ qua được.
        ky["need"] = min(ky["soCau"], max(2, ky["soCau"] - 1))
        ra.append(ky)
        for x in chu_doan:
            loi[ma_am("cau", x)] = {"id": ma_am("cau", x), "chu": x, "tieng": "en"}
        for q in ky["cau"]:
            # `amChu` khai THẲNG câu mà clip đọc lên. Suy ngược từ `answerKey` là
            # chỗ vừa sai: câu Có/Không có đáp án là chữ "Không", và bộ sinh âm
            # ngoan ngoãn đem chữ Việt ấy đi đọc bằng giọng Anh.
            if q.get("am") and q.get("amChu"):
                loi[q["am"]] = {"id": q["am"], "chu": q["amChu"], "tieng": "en"}

    # ══ MỖI UNIT MỘT BÀI ĐỌC ══
    #
    # Bác chốt 18-08: bài theo chương là chỗ ÔN LẠI cả bốn unit, nhưng bé học xong
    # MỘT unit thì cần đọc ngay của unit ấy — không phải chờ hết chương. Đoạn đọc
    # chỉ lấy câu của chính unit, nên bé vừa học xong là đọc được luôn.
    for b in bais:
        kho = _kho_tu(chuans, b["chuong"], chuong_cua)
        # Nguồn câu là CẢ KHO TÍCH LUỸ tới unit này, không chỉ mấy ví dụ của
        # chính nó — bác chốt 19-08. Xem `kho_cau_tienganh`.
        nguon = cau_tich_luy(lop, b["so"], kho, {b["so"]})
        doan = _hoi_thoai(nguon, ten_sach,
                          so_dong_cua(b["so"], max(x["so"] for x in bais)),
                          b["so"], b["chuong"])
        if len(doan) < SO_DONG_TOI_THIEU_UNIT:
            print(f"  ⚠ unit {b['so']}: chỉ dựng được {len(doan)} dòng, bỏ qua")
            continue
        khac = [t for s2, t in sorted(ten_unit.items()) if s2 != b["so"]]
        # Mồi lấy unit GẦN NHẤT hai bên, không lấy đầu sổ: hai chủ đề cạnh nhau
        # mới thật sự dễ lẫn, chứ "Khởi động" thì bé loại ngay.
        gan = sorted(khac, key=lambda t: abs(list(ten_unit.values()).index(t) - b["so"]))
        them({"id": f"DOC:TA{lop}.U{b['so']:02d}", "unit": b["so"],
              "chapter": b["chuong"], "phamVi": "unit", "loai": "dochieu",
              "name": f"ĐỌC HIỂU · UNIT {b['so']} · {ten_unit[b['so']].upper()}"},
             doan, [b], ten_unit[b["so"]], gan)

    # ══ MỖI CHƯƠNG MỘT BÀI ĐỌC — ôn lại cả bốn unit ══
    for c, ds in sorted(theo_chuong.items()):
        kho = _kho_tu(chuans, c, chuong_cua)
        nguon = cau_tich_luy(lop, max(x["so"] for x in ds), kho,
                             {x["so"] for x in ds})
        doan = _hoi_thoai(nguon, ten_sach,
                          so_dong_chuong(c, max(theo_chuong)), c, c)
        if len(doan) < SO_DONG_TOI_THIEU:
            print(f"  ⚠ chương {c}: chỉ dựng được {len(doan)} dòng, bỏ qua")
            continue
        them({"id": f"DOC:TA{lop}.C{c}", "chapter": c, "phamVi": "chuong",
              "loai": "dochieu", "name": f"ĐỌC HIỂU CHƯƠNG {c} · {ten_chuong[c].upper()}"},
             doan, ds, ten_chuong[c],
             [t for s2, t in sorted(ten_chuong.items()) if s2 != c])
    return ra, list(loi.values())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3, choices=[1, 2, 3])
    p.add_argument("--thieu", help="ghi ra tệp những dòng chưa có clip")
    a = p.parse_args()

    ds, loi = dung(a.lop)
    ra = GOC / f"web/public/content/{QUYEN[a.lop]}/dochieu.json"
    ra.write_text(json.dumps(ds, ensure_ascii=False, indent=1), "utf8")
    for k in ds:
        cho = f"unit {k['unit']}" if k.get("phamVi") == "unit" else f"chương {k['chapter']}"
        print(f"  {cho:10s}: {len(k['doan'])} dòng · {len(k['cau'])} câu hỏi "
              f"· cần {k['need']}/{k['soCau']}")
    print(f"→ {ra}")

    if a.thieu:
        so = json.loads((GOC / f"web/public/content/tienganh/lop{a.lop}_am.json")
                        .read_text("utf8"))
        co = {c["id"] for c in so.get("clip", [])}
        con = [m for m in loi if m["id"] not in co]
        Path(a.thieu).write_text(json.dumps(con, ensure_ascii=False, indent=1), "utf8")
        print(f"{len(con)}/{len(loi)} dòng chưa có clip → {a.thieu}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
