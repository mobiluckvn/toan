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
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}

SO_DONG_TOI_DA = 6      # bác chốt: đoạn 4–6 câu
# Bài theo CHƯƠNG gom bốn unit, mà một lượt đối đáp ăn HAI dòng — sáu dòng chỉ đủ
# ba lượt, tức là chưa đi hết chương đã hết chỗ. Tám dòng là bốn lượt, vừa đủ để
# câu hỏi "bài đọc nói về chuyện gì" có nghĩa là ý chính của cả chương.
SO_DONG_TOI_DA_CHUONG = 8
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


def _hai_ban(bais: list[dict], kho: set[str], ten_sach: list[str]) -> tuple[str, str]:
    """Chọn TÊN cho hai bạn nói chuyện.

    Ưu tiên tên chính unit ấy dùng: bạn ĐÁP là người tự xưng tên trong câu ví dụ,
    bạn HỎI là người được gọi tên. Unit nào không có câu xưng tên thì mượn tên
    trong `them.ten` của bản chuẩn — chúng nằm trong vốn từ đã học, nên không phải
    tên lạ, và cũng không phải tên tôi bịa ra.
    """
    xung, goi = [], []
    for b in bais:
        for c in (b["knowledgeCore"].get("canonicalExamples") or []):
            if not all(w in kho for w in chu_trong(c)):
                continue
            xung += TU_XUNG.findall(c)
            goi += GOI_TEN.findall(c)
    du = [x for x in dict.fromkeys(xung + goi + ten_sach) if x]
    tu_xung = list(dict.fromkeys(xung))
    b_ = (tu_xung[0] if tu_xung else (du[0] if du else "Lucy"))
    # ⚠ Bạn HỎI cũng nên là một người CÓ CÂU TỰ XƯNG trong sách. Lúc đổi vai, chính
    # bạn ấy phải đáp "My name's …" — mà câu ấy chỉ tồn tại cho những cái tên sách
    # đã viết. Bản đầu ưu tiên tên được GỌI ("Hello, Minh.") nên Minh không có câu
    # nào để tự xưng, `_hop_vai` gạt sạch, và unit 2 · 5 tụt xuống hai dòng rồi bị
    # bỏ hẳn. Tên tự xưng trước, rồi mới tới tên được gọi.
    a_ = next((x for x in tu_xung[1:] + list(dict.fromkeys(goi)) + du if x != b_),
              None) or "Ben"
    return a_, b_


def _hoi_thoai(bais: list[dict], kho: set[str], ten_sach: list[str],
               toi_da: int) -> list[dict]:
    """ĐOẠN HỘI THOẠI giữa hai bạn — trả `[{"cau", "ai"}]`.

    ══ VÌ SAO ĐỔI HẲN CÁCH DỰNG ══ (bác chốt 18-08-2026)

    Bác đọc thử rồi bảo: "Bài đọc phải là một đoạn văn hoặc đoạn hội thoại có ý
    nghĩa chứ không phải mấy câu rời rạc chẳng liên quan gì đến nhau."

    Bản cũ xếp bốn tới sáu câu SẴN CÓ của sách cạnh nhau theo thứ tự unit và tin
    rằng thế là thành một mẩu hội thoại. Không thành. Nó ra những đoạn thế này:

        What's this?              ← hỏi cái gì? ai hỏi?
        It's a nose.
        What's your hobby?        ← nhảy sang chuyện khác, không ai dẫn
        It's cooking.
        Is this our classroom?
        Yes, it is.

    Ba câu hỏi của ba người vô hình, ba câu đáp của ba người khác. Bé đọc xong
    không biết ai nói với ai — mà câu hỏi "bài đọc nói về chuyện gì" thì lại đòi
    bé tóm được một ý chung.

    ── NAY: HAI BẠN, VÀ CÂU CHUYỆN PHẢI NHẤT QUÁN ──

    Mẫu câu của sách vốn ĐÃ LÀ lượt đối đáp — `"What's your hobby? - It's cooking."`
    là HAI lượt nói, không phải một câu. Trước nay chỗ ấy bị cắt đôi rồi rải ra như
    hai câu rời. Nay giữ nguyên cặp và GẮN VAI: bạn A hỏi, bạn B đáp.

    Ba luật giữ cho đoạn không tự mâu thuẫn:

      1. hai bạn có TÊN, lấy từ chính câu ví dụ của unit (`_hai_ban`);
      2. câu tự xưng tên phải đúng tên người nói, câu gọi tên phải gọi bạn kia
         (`_hop_vai`);
      3. một câu hỏi chỉ được đáp MỘT LẦN. Sách có bốn ví dụ chung một câu hỏi
         ("What's your name? - My name's Mary/Bill/Linh…") — nhét cả bốn vào thì
         một người đổi tên bốn lần. Gặp lại đúng câu hỏi ấy thì ĐỔI VAI: lần này
         B hỏi, A đáp. Đúng cách hai người thật nói chuyện, và vẫn chỉ dùng câu
         có sẵn của sách.

    Mẫu KHÔNG có vế hỏi (cả lớp 1 là thế) thì một bạn nói liền mạch, ra đoạn kể về
    chính mình: "Hi, I'm Bill. This is my bag. This is my hat."

    ⚠ VẪN KHÔNG BỊA CÂU TIẾNG ANH. Mọi dòng vẫn là câu sẵn của sách, cắt ở " - "
    đúng như cũ. Cái đổi là THỨ TỰ và VAI — hai thứ không phải chữ nghĩa.
    """
    a_, b_ = _hai_ban(bais, kho, ten_sach)
    dong: list[dict] = []
    da_hoi: dict[str, int] = {}          # câu hỏi → đã dùng mấy lần

    def them_duoc(cau: str) -> bool:
        """Còn chỗ, chưa có, và chưa quá hai dòng cùng khuôn."""
        if len(dong) >= toi_da or any(d["cau"] == cau for d in dong):
            return False
        return sum(1 for d in dong if _dang(d["cau"]) == _dang(cau)) < CUNG_KHUON_TOI_DA

    # ── LỜI CHÀO ĐỨNG ĐẦU ──
    # Giữ đúng thứ tự sách thì ra đoạn thế này, và đọc lên thấy sai ngay:
    #     Minh: What number is it?
    #     Ben:  It's five.
    #     Ben:  Hello. I'm Ben.      ← chào giữa chừng, sau khi đã nói chuyện xong
    # Xếp lại là việc của THỨ TỰ, không phải của chữ nghĩa — vẫn không bịa câu nào.
    def uu_tien(c: str) -> int:
        return 0 if re.match(r"^(Hello|Hi)\b", c) else 1

    ung_vien = [c for b in bais
                for c in (b["knowledgeCore"].get("canonicalExamples") or [])]
    for c in sorted(ung_vien, key=uu_tien):
        if len(dong) >= toi_da:
            break
        if not all(w in kho for w in chu_trong(c)):
            continue
        phan = _tach_doi(c)
        if len(phan) == 2:
            hoi, dap = phan
            lan = da_hoi.get(hoi, 0)
            if lan >= 2:
                continue      # hỏi đi hỏi lại ba lần thì không còn là câu chuyện
            # Lượt đầu A hỏi B đáp; gặp lại đúng câu hỏi ấy thì ĐỔI VAI.
            ai_hoi, ai_dap = (a_, b_) if lan == 0 else (b_, a_)
            if not (_hop_vai(hoi, ai_hoi, ai_dap) and _hop_vai(dap, ai_dap, ai_hoi)):
                continue
            # Lấy TRỌN cặp hoặc không lấy. Cắt giữa cặp thì đoạn kết thúc bằng
            # một câu hỏi bỏ lửng, và bé ngồi tìm câu đáp không có ở đâu cả.
            # ── ĐỔI VAI THÌ ĐƯỢC HỎI LẠI ĐÚNG CÂU ẤY ──
            # Sách cho bốn ví dụ chung một câu hỏi ("What's your name? - My name's
            # Mary/Bill/Linh/Nam"). Chặn câu hỏi trùng thì unit ấy chỉ còn HAI dòng
            # và mất hẳn bài đọc — bốn unit lớp 3 đã rớt đúng thế. Mà trong một
            # cuộc trò chuyện thật, hỏi lại là chuyện thường nhất:
            #     Ben: What's your name?   Mai: My name's Mai.
            #     Mai: What's your name?   Ben: My name's Ben.
            # Nên vế HỎI của lượt đổi vai được phép trùng; vế ĐÁP thì không, vì hai
            # người không thể cùng mang một cái tên.
            if len(dong) + 2 > toi_da:
                continue
            if lan == 0 and not them_duoc(hoi):
                continue
            if any(d["cau"] == dap for d in dong):
                continue
            dong.append({"cau": hoi, "ai": ai_hoi})
            dong.append({"cau": dap, "ai": ai_dap})
            da_hoi[hoi] = lan + 1
        elif phan:
            # ── CÂU ĐƠN: ĐỔI LƯỢT, đừng dồn hết cho một bạn ──
            # Dồn hết cho bạn ĐÁP thì ra "Bill: Touch your face! / Bill: Touch
            # your hair!" — Bill ra lệnh hai lần liền còn Mai đứng im. Ưu tiên
            # người CHƯA nói ở dòng trên; `_hop_vai` vẫn gác, nên câu tự xưng
            # tên không bao giờ rơi vào miệng người khác.
            x = phan[0]
            vua_noi = dong[-1]["ai"] if dong else None
            for ai in ([a_, b_] if vua_noi == b_ else [b_, a_]):
                if _hop_vai(x, ai, a_ if ai == b_ else b_) and them_duoc(x):
                    dong.append({"cau": x, "ai": ai})
                    break
    return dong


def _ten_unit(b: dict) -> str:
    """`"Unit 5 · Sở thích của mình · My hobbies"` → `"Sở thích của mình"`.

    Lấy mẩu TIẾNG VIỆT ở giữa: mẩu đầu là số hiệu, mẩu cuối là tên tiếng Anh của
    sách. Câu hỏi ý chính hỏi bằng tiếng Việt nên đáp án cũng phải tiếng Việt."""
    phan = [x.strip() for x in str(b.get("title") or "").split("·")]
    return phan[1] if len(phan) > 2 else (phan[-1] if phan else "?")


def _cung_khuon(bais: list[dict], cau: str, tru: set[str]) -> list[str]:
    """Câu CÙNG KHUÔN với `cau` mà KHÔNG nằm trong đoạn — dùng làm mồi nhử.

    Cùng khuôn = cùng CHỮ ĐẦU và cùng SỐ CHỮ. Thô, nhưng đúng việc: mọi câu của
    một mẫu đều sinh ra từ một công thức, nên chúng chỉ khác nhau ở chỗ điền vào ô
    trống — tức là khác nhau ĐÚNG CHI TIẾT mà câu hỏi đang hỏi. Mồi khác khuôn thì
    bé loại được bằng hình dạng câu, không cần đọc đoạn văn lấy một chữ.

    ⚠ So bằng BA CHỮ ĐẦU thì hỏng: chỗ điền của quá nửa mẫu câu lớp 3 nằm ở vế
    ĐÁP (`It's five.` ↔ `It's one.`), mà hai câu ấy chỉ chung đúng một chữ đầu.
    """
    khoa = (cau.split()[0].lower(), len(cau.split()))
    ra = []
    for b in bais:
        for c in b["knowledgeCore"].get("canonicalExamples") or []:
            for x in _tach_doi(c):
                if x in tru or x in ra:
                    continue
                if (x.split()[0].lower(), len(x.split())) == khoa:
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
        doan = _hoi_thoai([b], kho, ten_sach, SO_DONG_TOI_DA)
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
        doan = _hoi_thoai(ds, kho, ten_sach, SO_DONG_TOI_DA_CHUONG)
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
