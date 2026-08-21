#!/usr/bin/env python3
"""DỰNG BỨC TRANH CHO MỘT UNIT — nền chung cho ĐỌC · VIẾT · NÓI.

    tools/tts/.venv/bin/python tools/tranh_tienganh.py --lop 3 --unit 0

Bác chốt 19-08-2026:

    "Bài đọc sẽ là các dạng như một bức tranh: mô tả về bức tranh đó. Bài viết sẽ
     là cho học sinh một bức tranh và viết lại mô tả về bức tranh đó. Bài nói sẽ
     cho một bức tranh và cùng mô tả về bức tranh đó (AI sẽ có phần mô tả bức tranh
     bằng chữ còn học sinh thì chỉ được nhìn tranh thôi)."

Một bức tranh, ba màn dùng chung. Vẽ một lần, và bé gặp lại cùng một cảnh ba lần
với ba việc khác nhau — nhìn · viết · nói.

══ LUẬT SỐ MỘT: TRANH DỰNG NGƯỢC TỪ VỐN CÂU ══

Vẽ một thứ mà bé KHÔNG có câu nào nói về nó thì bé đứng nhìn. Nên mỗi vật trong
tranh phải kèm sẵn CÂU tả nó, và câu ấy phải là khuôn của sách. Ở đây khai vật rồi
sinh câu, chứ không vẽ trước rồi mới nghĩ xem tả kiểu gì.

Sáu khuôn mô tả bé đã có từ lớp 1·2 — đó là lý do lối này chạy được ngay từ unit 0
của lớp 3 chứ không phải chờ tới cuối quyển:

    There's a garden.                              L1 U07   có cái gì
    I can see a tiger.                             L1 U14   nhìn thấy gì
    How many windows can you see? - I can see six. L1 U16   đếm
    It's a red pen.                                L1 U06   màu
    The cake is on the table.                      L2 U12   nằm ở đâu
    What number is it? - It's five.                L3 U00   đọc số

══ VẼ BẰNG GÌ ══

Ghép từ BỘ HÌNH ĐÃ CÓ: 262/320 từ của ba quyển đã có emoji hoặc hình vẽ tay, và
`HinhVe.jsx` (màn hình) lẫn `dung_video.py` (video) đều đang đọc đúng bộ ấy. Vẽ
riêng một bộ nữa cho tranh là tạo thêm một nơi phải đồng bộ tay — cái bẫy quen của
kho này. Xem [[mot-nguon-cho-hai-ben-ve]].
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "tools" / "video"))

from PIL import Image, ImageDraw  # noqa: E402
import hinh_ve  # noqa: E402
from dung_video import W, H, NEN, INK, MUTE, NAVY, phong, giua, the, ve_emoji  # noqa: E402
sys.path.insert(0, str(GOC / "tools"))
# `hinh_cua_tu` ở `kho_cau_tienganh` — bộ soạn tranh cũng cần nó mà chạy bằng
# python hệ thống (không có cairosvg), nên nó phải nằm ở module KHÔNG kéo theo
# Pillow/cairo. Cùng một nguồn cho cả hai bên, không chép đôi.
from kho_cau_tienganh import hinh_cua_tu  # noqa: E402,F401

QUYEN = {1: "ta1", 2: "ta2", 3: "ta3", 4: "ta4", 5: "ta5"}


def ve_vat(im: Image.Image, tu: str, hinh: dict, x: int, y: int, co: int) -> bool:
    """Một vật lên tranh. Hình vẽ tay trước, rồi mới tới emoji — ĐÚNG thứ tự ưu tiên
    của `HinhVe.jsx` và của `dung_video.py`. Ba nơi khác thứ tự thì cùng một từ ra
    ba mặt khác nhau, và bé không nhận ra đó là một thứ."""
    h = hinh.get(tu) or {}
    if hinh_ve.dan(im, h.get("ve"), x, y, co):
        return True
    if h.get("hinh"):
        ve_emoji(im, h["hinh"], x, y, co)
        return True
    return False


def dung_tranh(khai: dict, hinh: dict) -> Image.Image:
    """Vẽ bức tranh từ bản khai.

    Bản khai là dữ liệu, không phải mã: `nhom` nào cũng chỉ nói "vật gì · mấy cái ·
    đặt ở đâu". Sửa tranh là sửa JSON, không phải sửa tệp này.
    """
    im = Image.new("RGB", (W, H), NEN)
    d = ImageDraw.Draw(im)

    # Nền cảnh: một cái bàn/kệ dài cho vật đứng lên, và tên cảnh bằng TIẾNG VIỆT ở
    # góc. Tên cảnh KHÔNG bằng tiếng Anh: bé đang phải tự tìm chữ để tả, mà đề bài
    # lại cho sẵn chữ thì hỏng cả bài viết lẫn bài nói.
    for y in khai.get("ke") or []:
        the(d, 60, y, W - 120, 22, nen="#C8A87C", vien="#8A6B45", day=3, bo=8)
    # TÊN CẢNH SONG NGỮ — bác chốt 19-08: "Trên hình có text cũng nên song ngữ."
    # Tiếng Việt trước (bé đọc được ngay), tiếng Anh dưới, nhỏ hơn một nấc: nó là
    # thứ bé đang tập đọc, không phải thứ dẫn bé vào bài.
    # ⚠ Phân cấp bằng CỠ CHỮ, không bằng độ nhạt. Bản đầu tôi tô dòng tiếng Anh
    # bằng LINE (#D4E1EE) — đó là màu kẻ viền, đặt trên nền NEN (#EEF4FA) thì gần
    # như vô hình. Mở bản chạy thật mới thấy: dòng "Our bodies" chìm hẳn vào nền.
    giua(d, 18, khai["ten"], phong(32), INK)
    if khai.get("ten_en"):
        giua(d, 58, khai["ten_en"], phong(26), MUTE)

    for n in khai["nhom"]:
        co = n.get("co", 110)
        # ĐỨNG TRÊN KỆ, không lơ lửng. Bản đầu khai thẳng tâm y, và ra bức tranh có
        # mèo bay dưới gầm bàn — vật thì đúng, cảnh thì vô lý, mà bé tả cảnh chứ
        # không tả danh sách vật. Nay khai `ke` (số thứ tự kệ) rồi tính tâm.
        y_ke = (khai.get("ke") or [H - 60])[n.get("ke", 0)]
        y = n.get("y") or (y_ke - co // 2 - 4)
        for i in range(n["so"]):
            x = n["x"] + i * n.get("cach", co + 20)
            if not ve_vat(im, n["tu"], hinh, x, y, co):
                # Không vẽ được thì nói ra ngay, đừng để một ô trống trên tranh —
                # bé nhìn vào chỗ trống ấy và không hiểu phải tả gì.
                raise SystemExit(f"✗ không có hình cho “{n['tu']}”")

    # Tấm biển số — chỗ để hỏi "What number is it?". Vẽ bằng CHỮ SỐ chứ không bằng
    # emoji: emoji số của một số máy hiện thành ô vuông, mà con số thì phải đọc được.
    if khai.get("bienSo"):
        bs = khai["bienSo"]
        the(d, bs["x"] - 55, bs["y"] - 55, 110, 110, nen="#FFFFFF", vien=NAVY, day=4)
        # ⚠ KHÔNG dùng `giua()` — nó căn giữa CẢ BỀ RỘNG MÀN, nên con số rơi vào
        # chính giữa tranh còn tấm biển thì rỗng ở góc. Đo chữ rồi đặt tay.
        f = phong(74)
        hop = d.textbbox((0, 0), str(bs["so"]), font=f)
        d.text((bs["x"] - (hop[2] - hop[0]) // 2 - hop[0],
                bs["y"] - (hop[3] - hop[1]) // 2 - hop[1]),
               str(bs["so"]), font=f, fill=NAVY)
    return im


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3)
    p.add_argument("--unit", type=int)
    p.add_argument("--tat-ca", action="store_true")
    p.add_argument("--ra", default="web/public/content/tienganh/tranh")
    a = p.parse_args()

    kho = json.loads((GOC / f"data/tienganh/tranh_lop{a.lop}.json").read_text("utf8"))
    ds = kho if a.tat_ca else [k for k in kho if k["unit"] == a.unit]
    if not ds:
        return print(f"✗ chưa khai tranh cho unit {a.unit}") or 1

    ra = GOC / a.ra
    ra.mkdir(parents=True, exist_ok=True)
    for khai in ds:
        hinh = hinh_cua_tu(a.lop, khai["unit"])
        im = dung_tranh(khai, hinh)
        tep = ra / f"{khai['id'].replace(':', '_').replace('.', '_')}.png"
        im.save(tep)
        print(f"  ✓ U{khai['unit']:02d} {tep.name:24s} "
              f"{', '.join(n['tu'] for n in khai['nhom'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
