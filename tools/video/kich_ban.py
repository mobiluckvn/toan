#!/usr/bin/env python3
"""KỊCH BẢN VIDEO cho một bài Tiếng Anh lớp 1.

Đọc tệp bài (`web/public/content/ta1/DL_TA1_*.json`) và sổ âm, đẻ ra danh sách CẢNH.
Mỗi cảnh là một khung hình cộng một chuỗi clip tiếng. `dung_video.py` lo phần vẽ và
ghép; tệp này chỉ lo NÓI CÁI GÌ, THEO THỨ TỰ NÀO.

── VÌ SAO PHẢI CÓ VIDEO, KHÔNG PHẢI CHỈ MÀN HÌNH ──
Bé lớp 1 CHƯA ĐỌC SÕI TIẾNG VIỆT. Mọi lời giải thích bằng chữ trên màn hình — kể cả
phần "câu này dùng để làm gì" vừa thêm — thực chất là chữ cho NGƯỜI LỚN đọc. Bé chỉ
nhận được nội dung qua TAI và MẮT: tiếng nói cộng hình.

── MỘT VIDEO CHO TỪ, RỒI MỖI MẪU CÂU MỘT VIDEO ──
Bản đầu dựng một video 87 giây cho cả bài. Với bé 6 tuổi thì dài, và HỌC TỪ với RÁP
CÂU vốn là hai việc khác nhau. Tách rồi lại thấy tiếp: bài có HAI mẫu câu mà gộp
chung một video thì bé xem xong không biết mình vừa học một cấu trúc hay hai.

    <bài>_tu.mp4     chữ cái · từ mới
    <bài>_hoi.mp4    câu HỎI      — nếu mẫu câu là cặp hỏi–đáp
    <bài>_dap.mp4    câu TRẢ LỜI
    <bài>_cau1.mp4   mẫu câu thường, đánh số khi bài có nhiều mẫu

CẶP HỎI–ĐÁP phải tách, và đây là chỗ bản trước sai nặng nhất: "How many windows can
you see? - I can see six." trông như MỘT mẫu câu vì bản đồ khai chung một dòng, kỳ
thực là HAI cấu trúc dán bằng dấu gạch. Bản trước bắt bé lớp 1 nhắc lại cả cụm 46 ký
tự ba lần. Bé chưa biết gì về tiếng Anh thì phải học CÂU HỎI, tập cho thuộc, rồi mới
sang CÂU TRẢ LỜI.

Ba bài có hai mẫu câu: U1 (Hi / Bye), U11 (She's / He's), U13 (She's having /
He's having). Đúng ba chỗ mà cái đáng học nằm ở CHỖ KHÁC NHAU giữa hai mẫu — nên
mỗi mẫu phải có đất riêng, rồi mới so được.

── TẬP NÓI THEO: BA LẦN, CHẬM DẦN LÊN BÌNH THƯỜNG ──
Mỗi video mẫu câu kết bằng phần bé nhắc theo:

    lần 1  ×0,6  thật chậm — bé nghe rõ từng phụ âm
    lần 2  ×0,8  chậm vừa
    lần 3  ×1,0  như người lớn nói

Sau mỗi lần có KHOẢNG LẶNG dài bằng chính câu ấy, để bé kịp nói. Không có khoảng
lặng thì "nói theo" chỉ là nghe ba lần.

Đọc chậm là do MÔ HÌNH đọc chậm, không phải kéo giãn tệp: kéo giãn giữ được cao độ
nhưng làm nhoè phụ âm — mà phụ âm mới là chỗ bé cần nghe rõ.

── LUẬT DỰNG KỊCH BẢN ──

1. GIẢI THÍCH bằng tiếng VIỆT, MẪU bằng tiếng ANH — và tách hẳn hai đoạn.
   Không bao giờ trộn hai thứ tiếng trong một clip: hai model khác nhau, model nào
   đọc lẫn cũng sai (xem tools/tts/README.md).

2. Nghe tiếng Anh thì trên màn hình phải có ĐÚNG thứ đang được nói tới — chữ tiếng
   Anh to, kèm hình. Bé chưa đọc được thì hình là chỗ dựa duy nhất.

3. CÂU MẪU đọc HAI LẦN, có khoảng lặng ở giữa để bé nhắc theo. Đây là phần "nói"
   mà Đợt 1 chưa chấm được — nhưng không chấm không có nghĩa là không tập.

4. Hình chỉ hiện khi hình ấy ĐÚNG. Bảy từ đang dùng emoji gần đúng (gate 🚧 là biển
   công trường, top 🪀 là yo-yo) thì video hiện THẺ CHỮ, không hiện hình sai — trên
   màn hình bé còn có chữ và tiếng để bù, trong video thì hình sai là dạy sai.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent.parent


def ma_am(loai: str, chu: str) -> str:
    """Cùng luật đặt mã với `tools/tts/sinh_am.py`. Lệch một ký tự là cảnh câm."""
    sach = "".join(c if c.isalnum() else "_" for c in str(chu).lower()).strip("_")
    return f"{loai}_{sach}"[:60]


DAN_MAU = "Mẩu này là"

# Lời dẫn và lời kết RIÊNG cho từng video. Dùng chung cho cả 16 bài nên chỉ tốn
# bốn clip, mà nhờ đó không video nào bắt đầu hay kết thúc cụt lủn.
DAN_TU = "Phần một: từ mới của bài."
DAN_CAU = "Phần hai: mẫu câu của bài."
KET_TU = "Con đã học xong từ mới rồi. Giỏi lắm!"
KET_CAU = "Con đã nói được cả câu rồi. Giỏi lắm!"
DAN_NOI = "Giờ con nói theo cô nhé. Ba lần, chậm rồi nhanh dần."

# Ba tốc độ của phần tập nói. Hậu tố mã clip lấy từ tốc độ, nên đổi bảng này là
# phải sinh lại clip — cổng `tienganh_am` bắt được vì mã không tra ra.
TOC_DO = (0.6, 0.8, 1.0)
NHAN_TOC = {0.6: "Thật chậm", 0.8: "Chậm vừa", 1.0: "Như bình thường"}


def ma_cham(cau: str, td: float) -> str:
    """Mã clip đọc chậm. ×1.0 dùng lại clip thường, khỏi sinh trùng."""
    return ma_am("cau", cau) if td == 1.0 else f"{ma_am('cau', cau)}_x{int(td * 100)}"


def lam_sach(s: str) -> str:
    """Bỏ dấu nháy cong và gạch dài trước khi đem đọc.

    Kokoro-VI đọc “ ” và — thành khoảng lặng dài, nghe như máy vấp. Chữ HIỆN LÊN
    thì giữ nguyên dấu nháy cho đẹp; chữ ĐEM ĐỌC thì bỏ."""
    for a, b in (("“", ""), ("”", ""), ("—", ","), ("’", "'"), ("  ", " ")):
        s = s.replace(a, b)
    return s.strip()


def loi_phan(ph: dict) -> str:
    """Lời đọc cho một mẩu — TIẾNG VIỆT thuần, vì mẩu tiếng Anh đã đọc riêng."""
    return lam_sach(f"nghĩa là {ph['lam_gi']}")


def _canh(loai, chu_chinh="", chu_phu="", hinh=None, loi=None, **k):
    """`loi` là danh sách (chữ, tiếng[, tốc độ]) — MÃ clip suy ra từ đó, không gõ tay.

    Bản trước khai `am` bằng mã, còn danh sách chữ đem đi sinh tiếng thì gom ở một
    script khác. Hai chỗ tính cùng một thứ nên sớm muộn cũng lệch — và đã lệch thật:
    đổi câu sai của "chỗ dễ nhầm" là bộ dựng báo cảnh câm, vì script gom clip không
    biết câu ấy đã đổi. Nay chỉ còn MỘT chỗ khai, mã và chữ đi liền nhau.
    """
    loi = [tuple(x) for x in (loi or [])]
    them = k.pop("am2", [])
    am = [ma_cham(c, x[2]) if len(x) > 2 and x[2] != 1.0
          else (ma_am("loi", c) if x[1] == "vi" else ma_am("cau", c))
          for x in loi for c in [x[0]]]
    return {"loai": loai, "chuChinh": chu_chinh, "chuPhu": chu_phu,
            "hinh": hinh, "am": am + them, "loiAm": [list(x) for x in loi], **k}


def _hinh_cua_tu(h: dict):
    """
    Hai đường ra hình, theo đúng thứ tự ưu tiên của màn hình (`HinhVe.jsx`):
    có `ve` thì dùng HÌNH VẼ TAY, không thì dùng emoji.

    Trước đây hàm này trả None cho mọi từ có `ve`, vì Pillow không dựng nổi SVG —
    nên bảy từ ấy trong video hiện một thẻ chữ thay cho hình, đúng cái mà cả bộ
    hình vẽ tay sinh ra để tránh. Nay `hinh_ve.py` rasterize được, nên trả thẳng
    khoá vẽ và khung dựng lo phần còn lại.
    """
    return {"ve": h.get("ve")} if h.get("ve") else {"hinh": h.get("hinh")}


def _phan(bai: dict) -> dict:
    kc = bai["knowledgeCore"]
    tu = kc["vocabulary"]
    hinh_cua = {h["tu"]: h for h in (bai.get("hinhTu") or [])}
    mc = kc.get("mauCau") or {}
    ds = []

    def anh(t):
        """Hình của một từ: emoji, hoặc khoá hình vẽ tay. Xem `_hinh_cua_tu`."""
        return _hinh_cua_tu(hinh_cua.get(t["tu"]) or {})

    # ══ VIDEO 1 · TỪ ══
    # ── 1 · BÌA ──────────────────────────────────────────────────────────
    hook = next((m for m in bai["lecture"]["screens"] if m["kind"] == "hook"), None)
    ds.append(_canh("bia", bai["title"], "Từ mới",
                    loi=[(c, "vi") for c, t in (hook.get("doanAm") or []) if t == "vi"]
                        + [(DAN_TU, "vi")]))

    # ── 2 · CHỮ CÁI, DẠY QUA TỪ ─────────────────────────────────────────
    # Bác chốt bỏ phần âm rời: /d/ tách khỏi từ không tồn tại trong lời nói tự
    # nhiên. Nên dạy âm bằng cách cho nghe LIỀN ba từ cùng chữ đầu.
    chu = (bai.get("dangGoc") or "?").split()[0]
    K = {s["id"]: s for s in kc["statements"]}
    if "K2" in K:
        ds.append(_canh("chu_cai", chu, "",
                        loi=[(c, t) for c, t in (K["K2"].get("doanAm") or [])]))

    # ── 3 · TỪ MỚI — mỗi từ MỘT cảnh ────────────────────────────────────
    for t in tu:
        ds.append(_canh("tu", t["tu"], f"{t['nghia']}  {t['ipa']}", **anh(t),
                        # tiếng Anh trước (bé nghe từ), rồi tiếng Việt (bé hiểu nghĩa)
                        loi=[], am2=[ma_am("tu", t["tu"]), ma_am("nghia", t["nghia"])]))

    ds.append(_canh("ket", "Giỏi lắm!", f"Con đã biết {len(tu)} từ mới của bài.",
                    loi=[(KET_TU, "vi")]))
    tu_ds, ds = ds, []

    # ══ VIDEO 2..n · MỖI MẪU CÂU MỘT VIDEO ══
    cau_ds = []
    for mc in (kc.get("mauCauDs") or ([mc0] if (mc0 := kc.get("mauCau")) else [])):
        cau_ds.append(_mot_mau_cau(bai, mc, tu, anh))
    return {"tu": tu_ds, "cau": cau_ds}


def _mot_mau_cau(bai, mc, tu, anh) -> list[dict]:
    """Trọn một video cho MỘT mẫu câu: dẫn → dùng để làm gì → tách mẩu →
    nghe cả câu → TẬP NÓI ba lần → chỗ dễ nhầm → kết."""
    kc = bai["knowledgeCore"]
    NHAN = {"hoi": "Câu hỏi", "dap": "Câu trả lời", "cau": "Mẫu câu"}
    ds = [_canh("bia", bai["title"], f"{NHAN[mc.get('vai', 'cau')]} · {mc['cau']}",
                vaiKhoi=mc.get("vai", "cau"), loi=[(DAN_CAU, "vi")])]

    if mc.get("dungDe"):
        loi = f"Câu hôm nay dùng để {mc['dungDe'].lower()} {mc.get('tinhHuong', '')}".strip()
        ds.append(_canh("dung_de", mc["dungDe"], mc.get("tinhHuong", ""),
                        loi=[(loi, "vi")]))

    for i, ph in enumerate(mc.get("phan") or []):
        ds.append(_canh("tach_cau", mc["cau"], ph["lam_gi"],
                        soPhan=i + 1, phan=mc["phan"],
                        loi=[(DAN_MAU, "vi"), (ph["chu"], "en"), (loi_phan(ph), "vi")]))

    # Câu sinh từ CHÍNH nửa này. Với cặp hỏi–đáp thì canonicalExamples chứa cả cụm
    # "hỏi - đáp", nên phải CẮT lấy đúng nửa mình đang dạy — không thì video câu hỏi
    # lại đọc cả câu trả lời, đúng cái vừa sửa.
    def nua(c: str) -> str:
        if mc.get("vai") == "hoi" and " - " in c:
            return c.split(" - ")[0]
        if mc.get("vai") == "dap" and " - " in c:
            return c.split(" - ", 1)[1]
        return c
    khung = (mc.get("congThuc") or "").replace(" + ", " ").split("[")[0].strip()
    cung_khung = list(dict.fromkeys(
        nua(c) for c in (kc.get("canonicalExamples") or [])
        if khung and c.startswith(khung))) or [mc["cau"]]
    # Cảnh này cũng bảo bé "nghe rồi NHẮC LẠI", nên cùng luật với `nhac_theo`:
    # chỉ vế nói ra miệng được. Giữ nguyên cả cặp hỏi - đáp thì bé phải nhắc lại
    # "… / No, she isn't." — dấu gạch chéo không đọc được, và nói cả hai câu đáp
    # ngược nhau là vô nghĩa.
    for c in cung_khung[:3]:
        cn = cau_noi_duoc(c)
        ds.append(_canh("ca_cau", cn, "Con nghe rồi nhắc lại nhé",
                        **next((anh(t) for t in tu if t["tu"] in cn), {}),
                        loi=[(cn, "en")], lapLai=2))

    # ── TẬP NÓI: ba lần, chậm dần lên bình thường, có lặng để bé nói ──
    ds.append(_canh("dan_noi", "Nói theo cô nhé", "Ba lần — chậm rồi nhanh dần",
                    loi=[(DAN_NOI, "vi")]))
    # ⚠ TẬP NÓI thì chỉ nói VẾ ĐẦU, không nói cả cặp hỏi - đáp.
    #
    # Mẫu câu lớp 1 đều là câu trần thuật ngắn nên `mc["cau"]` nói ra miệng được.
    # Quá nửa mẫu câu lớp 2 là hỏi - đáp kèm CẢ HAI phương án:
    #     "Is she flying a kite? - Yes, she is. / No, she isn't."
    # Bắt bé nhắc lại nguyên cụm ấy ba lần là bắt bé đọc một thứ không ai nói ra
    # miệng bao giờ — dấu gạch chéo không đọc được, và hai câu đáp ngược nhau thì
    # nói cả hai là vô nghĩa. Video B02 vì thế dài 124 giây, trong khi trần của
    # lớp 1 là 90.
    #
    # Vế trước " - " chính là câu bé cần nói. Cùng một luật với ô gõ ở
    # `sinh_bai_tienganh.py` — hai chỗ phải nghĩ giống nhau về "câu nói được".
    cau_noi = cau_noi_duoc(mc["cau"])
    for k, td in enumerate(TOC_DO, 1):
        ds.append(_canh("nhac_theo", cau_noi, NHAN_TOC[td],
                        lan=k, soLan=len(TOC_DO), tocDo=td,
                        loi=[(cau_noi, "en", td)], choNoi=True))

    nham = (kc.get("misconceptions") or [None])[0]
    trap = next((m for m in bai["lecture"]["screens"] if m["kind"] == "trap"), None)
    if nham and trap and nham["right"] == mc["cau"]:
        ds.append(_canh("de_nham", nham["wrong"], nham["right"], why=nham["why"],
                        loi=[(c, t) for c, t in (trap.get("doanAm") or [])]
                            + [(lam_sach(nham["why"]), "vi")]))

    ds.append(_canh("ket", "Giỏi lắm!", f"Con nói được câu “{mc['cau']}” rồi.",
                    loi=[(KET_CAU, "vi")]))
    return ds


def cac_phan(bai: dict) -> dict:
    """{"tu": [cảnh…], "cau": [[cảnh…] cho mỗi mẫu câu]}"""
    return _phan(bai)


def kich_ban(bai: dict) -> list[dict]:
    d = _phan(bai)
    return d["tu"] + [c for kh in d["cau"] for c in kh]


def loi_can_sinh(ds: list[dict], so_am: dict) -> list[dict]:
    """Những dòng kịch bản cần mà sổ âm chưa có. Đọc thẳng từ `loiAm` của cảnh, nên
    đổi bất cứ chữ nào trong kịch bản là danh sách này tự đúng theo."""
    co = {c["id"] for c in so_am.get("clip", [])}
    ra = {}
    for c in ds:
        for x in c.get("loiAm") or []:
            chu, tieng = x[0], x[1]
            td = x[2] if len(x) > 2 else 1.0
            i = ma_cham(chu, td) if td != 1.0 else (
                ma_am("loi", chu) if tieng == "vi" else ma_am("cau", chu))
            if i not in co and i not in ra:
                ra[i] = {"id": i, "chu": chu, "tieng": tieng,
                         **({"tocDo": td} if td != 1.0 else {})}
    return list(ra.values())


def soat(ds: list[dict], so_am: dict) -> list[str]:
    """Cảnh nào gọi clip không có thì nói ra — cảnh câm là cảnh hỏng."""
    co = {c["id"] for c in so_am.get("clip", [])}
    return [f"cảnh {i} ({c['loai']}): thiếu clip {m}"
            for i, c in enumerate(ds) for m in c["am"] if m not in co]


def cau_noi_duoc(cau: str) -> str:
    """Vế bé NÓI RA MIỆNG được: phần trước dấu " - " của cặp hỏi - đáp."""
    return (cau or "").split(" - ")[0].strip()


def lop_cua(ma: str) -> int:
    """`DL_TA2_B04` → 2. Mã bài đã mang số lớp, đừng bắt người gọi khai lại."""
    m = re.match(r"DL_TA(\d+)_", ma or "")
    if not m:
        raise SystemExit(f"mã bài không đọc ra lớp: {ma!r} (phải dạng DL_TA2_B04)")
    return int(m.group(1))


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--bai", required=True, help="vd DL_TA1_B04")
    p.add_argument("--ra")
    a = p.parse_args()

    # Thư mục và sổ âm SUY TỪ CHÍNH MÃ BÀI, không ghim 'ta1'.
    # `DL_TA2_B04` đã mang sẵn số lớp; bắt người gọi khai thêm `--lop` là mở đường
    # cho hai thứ lệch nhau — đọc bài lớp 2 mà tra sổ âm lớp 1 thì mọi clip đều
    # "chưa có" và video ra câm, không lỗi nào hiện.
    lop = lop_cua(a.bai)
    bai = json.loads((GOC / f"web/public/content/ta{lop}/{a.bai}.json").read_text("utf8"))
    so = json.loads((GOC / f"web/public/content/tienganh/lop{lop}_am.json").read_text("utf8"))
    hp = cac_phan(bai)
    ds = hp["tu"] + [c for kh in hp["cau"] for c in kh]
    loi = soat(ds, so)
    print(f"{a.bai}: từ {len(hp['tu'])} cảnh · "
          + " · ".join(f"mẫu {i+1}: {len(kh)} cảnh" for i, kh in enumerate(hp["cau"]))
          + f" · {sum(len(c['am']) for c in ds)} clip")
    for x in loi[:8]:
        print("  ⚠", x)
    if a.ra:
        Path(a.ra).write_text(json.dumps(ds, ensure_ascii=False, indent=1), "utf8")
        print("→", a.ra)
    return 1 if loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
