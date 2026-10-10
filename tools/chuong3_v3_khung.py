#!/usr/bin/env python3
"""
KHUNG DỰNG CHƯƠNG 3 (bản viết lại) — hàm vẽ và số liệu dùng chung.

Dùng lại toàn bộ hàm vẽ của `chuong3_khung.py` (bảng, giả mã, cảnh báo, công
thức), thêm ba thứ mà bản viết lại cần:

  · `hinh()`   chèn ảnh PNG do `chuong3_v3_hinh.py` dựng, kèm dòng "Hình 3.x";
  · `sv()` `sn()` viết số theo lối Việt Nam — 0,375 và 1.194;
  · `SO`       toàn bộ số liệu do `chuong3_v3_so.mjs` sinh ra bằng cách gọi
               CHÍNH mã đang chạy thật.

⚠ ĐỪNG GÕ TAY MỘT CON SỐ NÀO CÓ TRONG `SO`. Gõ tay thì hai nơi hai số, và khi
mã đổi thì luận văn sai mà không ai biết — đúng cái bẫy mà mục 3.3.5 của chính
chương này nêu ra cho phần mềm.
"""
from __future__ import annotations

import json
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from chuong3_khung import (                                   # noqa: F401
    DO, XAM, XANH, bang, canh_bao, cham, cong_thuc, do, doan, hinh_chu,
    ma_lenh, thuat_toan,
)

GOC = Path(__file__).resolve().parent.parent
HINH = GOC / "docs" / "hinh_c3v3"
SO = json.loads((GOC / "docs" / "chuong3_v3_so.json").read_text("utf8"))


def sv(x, n: int = 3) -> str:
    """Số thập phân kiểu Việt: 0,375. `None` → dấu gạch."""
    if x is None:
        return "—"
    return f"{x:.{n}f}".replace(".", ",")


def sn(x) -> str:
    """Số nguyên có dấu phân nhóm kiểu Việt: 1.194."""
    return f"{int(x):,}".replace(",", ".")


def hinh(d, ten: str, chu_thich: str, rong: float = 6.3):
    """Chèn một hình PNG, căn giữa, kèm dòng chú thích in đậm ở dưới."""
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(HINH / f"{ten}.png"), width=Inches(rong))
    q = d.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    do(q, chu_thich, dam=True)
    q.paragraph_format.space_after = Pt(10)


def json_khoi(d, obj, ten: str | None = None, rut: int = 0):
    """In một tài liệu JSON nguyên văn — dùng cho bản ghi thật."""
    if ten:
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        do(p, ten, dam=True)
    txt = json.dumps(obj, ensure_ascii=False, indent=1)
    for dong in txt.split("\n"):
        if rut and len(dong) > rut:
            dong = f"{dong[:rut - 1]}…"
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Pt(18)
        r = p.add_run(dong if dong else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(9.0)
    d.add_paragraph()
