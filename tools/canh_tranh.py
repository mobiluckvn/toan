#!/usr/bin/env python3
"""DỰNG BỨC TRANH TẢ CẢNH cho một unit — nền chung của ĐỌC · VIẾT · NÓI.

    tools/tts/.venv/bin/python tools/canh_tranh.py --lop 3 --tat-ca

Thay hẳn `tools/tranh_tienganh.py`, vốn chỉ biết vẽ ba thanh gỗ ngang rồi đặt
emoji lên. Bác bác bỏ toàn bộ 42 bức ấy:

    "Chủ đề bài là Hello Again thì bạn nên vẽ một bối cảnh có người chào nhau.
     Trong bức tranh có thể có các con vật, có xe đạp, có mèo, có mũ… chứ không
     ai đi vẽ như bạn đang vẽ."

── BẢN KHAI LÀ DỮ LIỆU, TỆP NÀY CHỈ LÀ BÚT ──
`data/tienganh/canh_lopN.json` khai từng bức: nền gì, vật nào, đặt ở đâu. Tệp
này không quyết cảnh nào có gì. Đó là luật 4 bác chốt — 42 cảnh VIẾT TAY, không
có bước nhân bản nào. Bộ sinh chỉ soi, không sáng tác.

── THỨ TỰ VẼ QUYẾT ĐỊNH CHIỀU SÂU ──
Vẽ theo đúng thứ tự khai trong `vat`: khai trước nằm dưới. Nên hậu cảnh khai
trước, tiền cảnh khai sau. Vật ở xa truyền `xa` để nhạt bớt — không có nó thì
cái cây cuối sân đậm ngang bạn nhỏ đứng ngay trước mặt, và bức tranh bẹt ra.

── CHỮ TRONG TRANH ──
Chỉ có TÊN CẢNH song ngữ trên dải tiêu đề. Mọi mặt chữ BÊN TRONG cảnh — bảng
đen, biển tên phố, tấm lịch, thời khoá biểu, bảng tên — đều ĐỂ TRỐNG. Bé đang
tập đọc tiếng Anh: chữ in sẵn trong tranh là cho sẵn đáp án của chính bài viết
và bài nói.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "tools" / "video"))
sys.path.insert(0, str(GOC / "tools"))

from PIL import Image, ImageDraw  # noqa: E402
import hinh_ve  # noqa: E402
from dung_video import NEN as MAU_NEN, INK, MUTE, phong, giua, ve_emoji  # noqa: E402
from kho_cau_tienganh import hinh_cua_tu  # noqa: E402
import canh_ve  # noqa: E402
from canh_ve import W, H, NEN, VE  # noqa: E402

# ⚠ KHOÁ KHAI — mô tả thứ nét vẽ ĐÃ VẼ, không sai khiến nét vẽ làm gì thêm.
#
# `ao_la` là một ví dụ: bút `nguoi` vẽ một cái áo, nhưng nó chỉ biết MÀU, không
# biết đó là áo len hay áo sơ mi. Cổng `tienganh_dochieu` vì thế báo đỏ khi đoạn
# văn nói "jumper" — tranh CÓ vẽ, chỉ là không có gì trong bản khai nói tên nó.
#
# Khai ở đây thay vì nới cổng: cổng vẫn đỏ với mọi món quần áo CHƯA khai, nên
# một đoạn nói "coat" mà tranh vẽ áo len thì vẫn bị bắt. Nới cổng thì mất hẳn
# phép canh ấy — đúng cái bẫy [[cong-ghim-chinh-ta-thay-vi-tinh-chat]].
#
# Khoá khai KHÔNG được truyền xuống bút vẽ, nếu không `nguoi()` ném TypeError.
KHAI = {"ao_la"}


def ve_vat(im, d, k: dict, hinh: dict):
    """Một mục trong `vat`. Hai lối khai:

        {"ve": "nguoi", "x": 330, "y": 560, ...}   vẽ tay, tra ở canh_ve.VE
        {"tu": "ball",  "x": 700, "y": 540, "co": 90}   hình của TỪ VỰNG

    Lối thứ hai đi qua đúng bộ hình mà `HinhVe.jsx` (màn hình) và
    `dung_video.py` (video) đang dùng — hình vẽ tay trước, emoji sau. Ba nơi vẽ
    khác thứ tự thì cùng một từ ra ba mặt khác nhau và bé không nhận ra đó là
    một thứ. Xem [[mot-nguon-cho-hai-ben-ve]].
    """
    if "ve" in k:
        ten = k["ve"]
        if ten not in VE:
            raise SystemExit(f"✗ không có bút vẽ “{ten}” — có {sorted(VE)}")
        tham = {a: b for a, b in k.items() if a != "ve" and a not in KHAI}
        VE[ten](d, **tham)
        return

    tu, co = k["tu"], k.get("co", 100)
    h = hinh.get(tu) or {}
    if hinh_ve.dan(im, h.get("ve"), k["x"], k["y"], co):
        return
    if h.get("hinh"):
        ve_emoji(im, h["hinh"], k["x"], k["y"], co)
        return
    # Không vẽ được thì kêu NGAY. Để trống một ô trên tranh thì bé nhìn vào chỗ
    # ấy và không hiểu phải tả gì — mà không có gì báo cho tôi biết.
    raise SystemExit(f"✗ không có hình cho từ “{tu}”")


def dung(khai: dict, hinh: dict) -> Image.Image:
    im = Image.new("RGB", (W, H), MAU_NEN)
    d = ImageDraw.Draw(im)

    n = khai["nen"]
    kieu = n["kieu"] if isinstance(n, dict) else n
    if kieu not in NEN:
        raise SystemExit(f"✗ không có phông nền “{kieu}” — có {sorted(NEN)}")
    NEN[kieu](d, n if isinstance(n, dict) else {})

    for k in khai["vat"]:
        ve_vat(im, d, k, hinh)

    # TÊN CẢNH SONG NGỮ — bác chốt 19-08: "Trên hình có text cũng nên song ngữ."
    # ⚠ Phân cấp bằng CỠ CHỮ, không bằng độ nhạt. Bản đầu tôi tô dòng tiếng Anh
    # bằng LINE (#D4E1EE) — đó là màu KẺ VIỀN, đặt trên nền sáng thì gần như vô
    # hình, và chỉ lộ ra khi mở bản chạy thật. Xem [[kiem-bang-mat-truoc-khi-deploy]].
    d.rectangle([0, 0, W, canh_ve.TRAN], fill=MAU_NEN)
    giua(d, 12, khai["ten"], phong(32), INK)
    if khai.get("ten_en"):
        giua(d, 52, khai["ten_en"], phong(26), MUTE)
    return im


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3)
    p.add_argument("--unit", type=int)
    p.add_argument("--tat-ca", action="store_true")
    p.add_argument("--ra", default="web/public/content/tienganh/tranh")
    a = p.parse_args()

    kho = json.loads((GOC / f"data/tienganh/canh_lop{a.lop}.json").read_text("utf8"))
    ds = kho if a.tat_ca else [k for k in kho if k["unit"] == a.unit]
    if not ds:
        return print(f"✗ chưa khai cảnh cho unit {a.unit}") or 1

    ra = GOC / a.ra
    ra.mkdir(parents=True, exist_ok=True)
    for khai in ds:
        im = dung(khai, hinh_cua_tu(a.lop, khai["unit"]))
        tep = ra / f"{khai['id'].replace(':', '_').replace('.', '_')}.png"
        im.save(tep)
        print(f"  ✓ U{khai['unit']:02d} {tep.name:22s} {khai['ten']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
