#!/usr/bin/env python3
"""NẠP NGƯỢC BẢNG BÁC ĐÃ SỬA → tools/canh_de_xuat.py

    python3 tools/nap_bang_doc.py --thu      # chỉ xem sẽ đổi gì, KHÔNG ghi
    python3 tools/nap_bang_doc.py            # ghi thật

Đọc `docs/bang_bai_doc.xlsx` (bác sửa trong Excel) rồi ghi vào **bảng nguồn**
`tools/canh_de_xuat.py`. Sau đó chạy tiếp:

    tools/tts/.venv/bin/python tools/soan_canh.py
    python3 tools/sinh_bai_tranh.py --lop 3   # và 4, 5
    python3 tools/soat_moi_nhu.py · python3 tools/soat_hoi_chot.py
    cd web && npm run build && for f in test/*.test.mjs; do node "$f"; done

── VÌ SAO GHI VÀO TỆP .py CHỨ KHÔNG GHI VÀO BẢN KHAI ──
`data/tienganh/canh_lopN.json` là bản DỰNG. Ghi vào đó thì lần sau ai chạy
`soan_canh.py` là mất trắng, không có gì báo — đúng cái bẫy
[[ban-dung-lai-de-mat-ban-sua-tay]]. Nên nguồn vẫn là một, và là tệp .py.

── GHI BẰNG `ast`, KHÔNG BẰNG PHÉP THAY CHUỖI ──
Mỗi bài là một lời gọi `C(noi, mo_ta, doan, hoi, goi_y, ghi)`. Bộ nạp tìm đúng
đối số thứ ba (`doan`) và thứ tư (`hoi`) của đúng lời gọi ấy bằng vị trí ký tự
mà `ast` cho, rồi thay đoạn văn bản. Phép thay chuỗi thì khớp nhầm — đã dính
một lần ở bước dựng màn hỏi, xem docs/lam_bai_tranh.md mục "VÌ SAO BƯỚC ⑦".
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BANG = GOC / "docs/bang_bai_doc.xlsx"
NGUON = GOC / "tools/canh_de_xuat.py"

# MÃ BÀI → (tên dict trong canh_de_xuat.py, khoá)
RE_ID = re.compile(r"^TRANH:TA(\d)\.(U(\d+)|C(\d+))$")


def dich_ma(ma: str) -> tuple[str, int]:
    m = RE_ID.match(str(ma).strip())
    if not m:
        raise SystemExit(f"✗ mã bài lạ: {ma!r} — cột MÃ BÀI không được sửa")
    lop, so_u, so_c = m.group(1), m.group(3), m.group(4)
    return (f"L{lop}", int(so_u)) if so_u else (f"L{lop}C", int(so_c))


def chuoi_hoi(cau: list[dict]) -> str:
    """Dựng lại cột câu hỏi theo đúng khuôn `_hoi()` của soan_canh.py đọc."""
    dong = []
    for i, c in enumerate(cau, 1):
        chot = f" | {c['vi']}" if c.get("vi") else ""
        moi = " · ".join(c["moi"])
        dong.append(f"{i}. {c['hoi']}{chot} → {c['dap']}  (mồi: {moi})")
    return "\n".join(dong)


def literal(s: str, thut: int) -> str:
    """Chuỗi Python nhiều dòng, mỗi dòng của bảng một dòng mã — để `git diff`
    chỉ ra đúng câu đã đổi thay vì một khối chữ dài."""
    dong = s.split("\n")
    ra = []
    for i, d in enumerate(dong):
        ra.append(json.dumps(d + ("\\n" if i < len(dong) - 1 else ""),
                             ensure_ascii=False).replace("\\\\n", "\\n"))
    noi = ("\n" + " " * thut).join(ra)
    return noi


def doc_bang() -> tuple[dict, dict]:
    from openpyxl import load_workbook
    if not BANG.exists():
        raise SystemExit(f"✗ chưa có {BANG.relative_to(GOC)} — chạy "
                         f"`python3 tools/xuat_bang_doc.py` trước")
    wb = load_workbook(BANG, data_only=True)
    ws = wb["CÂU HỎI"]
    hoi: dict[str, list[dict]] = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        ma, cau_id, q, vi, dap = r[0], r[6], r[7], r[8], r[9]
        moi = [str(x).strip() for x in r[10:13] if x and str(x).strip()]
        if not q or not dap:
            raise SystemExit(f"✗ {ma} {cau_id}: thiếu câu hỏi hoặc đáp án")
        if not moi:
            raise SystemExit(f"✗ {ma} {cau_id}: không còn mồi nào")
        hoi.setdefault(str(ma).strip(), []).append(
            {"hoi": str(q).strip(), "vi": str(vi or "").strip(),
             "dap": str(dap).strip(), "moi": moi})

    doan = {}
    if "ĐOẠN ĐỌC" in wb.sheetnames:
        for r in wb["ĐOẠN ĐỌC"].iter_rows(min_row=2, values_only=True):
            if r and r[0] and r[5]:
                doan[str(r[0]).strip()] = " ".join(str(r[5]).split())
    return hoi, doan


def vi_tri(src: bytes) -> dict[tuple[str, int], dict]:
    """(dict, khoá) → vị trí BYTE của đối số `doan` và `hoi` trong nguồn.

    ⚠ `col_offset` của `ast` đếm theo BYTE UTF-8, không theo ký tự. Cả tệp này
    là chữ tiếng Việt nên hai con số ấy lệch nhau hàng chục — cắt theo ký tự
    thì lát cắt rơi vào giữa câu và sinh ra một tệp .py không parse nổi. Nên
    mọi phép cắt dán ở đây làm trên BYTES, decode ở bước cuối.
    """
    cay = ast.parse(src)
    dau_dong = [0]
    for d in src.split(b"\n"):
        dau_dong.append(dau_dong[-1] + len(d) + 1)

    def khoang(n):
        return (dau_dong[n.lineno - 1] + n.col_offset,
                dau_dong[n.end_lineno - 1] + n.end_col_offset)

    ra = {}
    for nut in cay.body:
        if not (isinstance(nut, ast.Assign) and len(nut.targets) == 1
                and isinstance(nut.targets[0], ast.Name)
                and re.fullmatch(r"L[345]C?", nut.targets[0].id)
                and isinstance(nut.value, ast.Dict)):
            continue
        ten = nut.targets[0].id
        for k, v in zip(nut.value.keys, nut.value.values):
            if not (isinstance(k, ast.Constant) and isinstance(v, ast.Call)
                    and getattr(v.func, "id", "") == "C" and len(v.args) >= 4):
                continue
            ra[(ten, k.value)] = {
                "doan": khoang(v.args[2]), "hoi": khoang(v.args[3]),
                "thut": v.args[3].col_offset}
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--thu", action="store_true", help="chỉ xem, không ghi")
    a = p.parse_args()

    hoi_moi, doan_moi = doc_bang()
    src = NGUON.read_bytes()
    vt = vi_tri(src)

    # Bảng hiện đang chạy — để chỉ ra đúng chỗ nào bác đã đổi.
    cu = {}
    for lop in (3, 4, 5):
        for k in json.loads((GOC / f"data/tienganh/canh_lop{lop}.json")
                            .read_text("utf8")):
            cu[k["id"]] = k

    thay, doi_doan, doi_hoi = [], [], []
    for ma, cau in hoi_moi.items():
        khoa = dich_ma(ma)
        if khoa not in vt:
            raise SystemExit(f"✗ {ma}: không tìm thấy {khoa[0]}[{khoa[1]}] "
                             f"trong {NGUON.name}")
        k = cu.get(ma, {})

        s_moi = chuoi_hoi(cau)
        s_cu = chuoi_hoi([{"hoi": h["hoi"], "vi": h.get("vi", ""),
                           "dap": h["dap"], "moi": h["moi"]}
                          for h in k.get("hoi", [])])
        if s_moi != s_cu:
            doi_hoi.append(ma)
            for i, (m, c) in enumerate(zip(s_moi.split("\n"),
                                           s_cu.split("\n")), 1):
                if m != c:
                    print(f"  {ma} câu {i}")
                    print(f"    cũ : {c}")
                    print(f"    mới: {m}")
            thay.append((vt[khoa]["hoi"],
                         literal(s_moi, vt[khoa]["thut"]).encode("utf8")))

        d_moi = doan_moi.get(ma)
        if d_moi and d_moi != " ".join(k.get("doan", [])):
            doi_doan.append(ma)
            print(f"  {ma} ĐOẠN ĐỌC")
            print(f"    cũ : {' '.join(k.get('doan', []))}")
            print(f"    mới: {d_moi}")
            thay.append((vt[khoa]["doan"], literal(d_moi, 5).encode("utf8")))

    if not thay:
        print("Bảng không có gì khác bản đang chạy — không phải ghi gì.")
        return 0

    for (dau, cuoi), moi in sorted(thay, key=lambda x: -x[0][0]):
        src = src[:dau] + moi + src[cuoi:]

    print(f"\n{len(doi_hoi)} bài đổi CÂU HỎI · {len(doi_doan)} bài đổi ĐOẠN")
    if a.thu:
        print("(--thu: chưa ghi gì)")
        return 0

    ast.parse(src)                    # ghi ra một tệp .py hỏng thì thà đừng ghi
    NGUON.write_bytes(src)
    print(f"→ đã ghi {NGUON.relative_to(GOC)}")
    print("\nChạy tiếp:")
    print("  tools/tts/.venv/bin/python tools/soan_canh.py")
    print("  for L in 3 4 5; do python3 tools/sinh_bai_tranh.py --lop $L; done")
    print("  python3 tools/soat_moi_nhu.py && python3 tools/soat_hoi_chot.py")
    print("  cd web && npm run build && for f in test/*.test.mjs; do node $f; done")
    if doi_doan:
        print("\n⚠ ĐOẠN ĐỌC có đổi → PHẢI dựng tiếng cho câu mới:")
        print("  python3 tools/sinh_bai_tranh.py --lop N --thieu /tmp/loi.json")
        print("  tools/tts/.venv/bin/python tools/tts/sinh_am.py --vao /tmp/loi.json \\")
        print("      --ra web/public/content/tienganh/audio \\")
        print("      --so web/public/content/tienganh/lopN_am.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
