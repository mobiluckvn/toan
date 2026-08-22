#!/usr/bin/env python3
"""THỐNG NHẤT NGHĨA TIẾNG VIỆT — một từ, một cách chú, trong cả năm quyển.

    tools/tts/.venv/bin/python tools/thong_nhat_nghia.py          # chỉ BÁO CÁO
    tools/tts/.venv/bin/python tools/thong_nhat_nghia.py --ghi    # ghi vào lopN_bu.json

Bộ soi `soat_vontu.py` tìm ra 31 từ mà sách chú hai kiểu: `bakery` là "hiệu bánh
mì" ở màn này, "tiệm bánh" ở màn kia. Không sai nghĩa, nhưng bé gặp HAI MẶT CHỮ
cho MỘT thứ và khó nhận ra đó là một.

── ⚠ BA TỪ KHÔNG ĐƯỢC THỐNG NHẤT ──

Không phải cứ hai nghĩa là lệch. Ba từ dưới đây có hai nghĩa THẬT, gộp lại là
làm hỏng một nghĩa đúng:

    can    "cái lon" (danh từ, lớp 1 bài đồ uống)
           "có thể, biết (làm gì)" (động từ, lớp 4)
    cook   "đầu bếp" (nghề, lớp 3)
           "nấu ăn"  (động từ, lớp 4)
    in     "ở trong" (trong hộp)
           "trong, ở (tên đường/phố)" — lớp 4 dùng cho "in Tran Hung Dao Street",
           gộp về "ở trong" là chú SAI hẳn.

── LUẬT CHỌN: GIỮ BẢN CỦA QUYỂN DẠY TRƯỚC ──

Một luật, áp đều, không chọn từng từ theo cảm tính. Lý do: bản ấy là bản bé gặp
ĐẦU TIÊN; quyển sau chỉ là gặp lại. Đổi cái bé đã thuộc để lấy một cách chú
"đẹp hơn" là bắt bé học lại từ đã biết.

Luật này cũng giữ được lớp phân loại tiếng Việt mà quyển sau hay rụng mất —
"cái diều" · "con gấu bông" · "quả bóng đá" — vốn tự nhiên hơn với bé nhỏ.

── SỬA Ở ĐÂU ──

KHÔNG sửa `web/public/content/**` (bản dựng, mất trắng lần sau) và KHÔNG sửa
`data/ban_do_tieng_anh.json` (quy ước cấm). Đường vá chính thức là
`data/tienganh/lopN_bu.json` → `tu[<mã nút>].nghia`, vì `chuan_tienganh.py` đọc
`nghia = b.get("nghia") or n.get("meaning_vi")`. Lối này đã dùng sẵn: "hiệu bánh
mì" hiện nay chính là một mục bù của lớp 4.

Sau khi ghi phải dựng lại, ĐÚNG THỨ TỰ — xem `docs/day_chuyen_du_lieu_tienganh.md`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

# Hai nghĩa THẬT — xem chú thích đầu tệp. Đây là danh sách KHAI TAY vì máy không
# phân biệt được từ đồng âm với chú lệch.
DE_NGUYEN = {"can", "cook", "in"}


def gom() -> dict[str, list[tuple[int, int, str, str]]]:
    """từ → [(lớp, unit, mã nút, nghĩa)] trên cả năm quyển."""
    ra: dict[str, list[tuple[int, int, str, str]]] = {}
    for lop in range(1, 6):
        tep = GOC / f"data/tienganh/chuan_lop{lop}.json"
        if not tep.exists():
            continue
        for u in json.loads(tep.read_text("utf8"))["unit"]:
            for t in u["tu"]:
                if t.get("nghia"):
                    ra.setdefault(t["tu"], []).append(
                        (lop, u["so"], t["ma"], t["nghia"]))
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true", help="ghi vào lopN_bu.json")
    a = p.parse_args()

    lech, giu, sua = [], [], {}
    for tu, ds in sorted(gom().items(), key=lambda x: x[0].lower()):
        nghia_ds = {n for *_, n in ds}
        if len(nghia_ds) < 2:
            continue
        if tu.lower() in DE_NGUYEN:
            giu.append((tu, sorted(nghia_ds)))
            continue
        dich = min(ds, key=lambda x: (x[0], x[1]))[3]
        doi = [(l, ma, n) for l, _, ma, n in ds if n != dich]
        lech.append((tu, dich, sorted(nghia_ds - {dich}), len(doi)))
        for l, ma, _ in doi:
            sua.setdefault(l, {})[ma] = dich

    print(f"── {len(giu)} từ ĐỂ NGUYÊN (hai nghĩa thật):")
    for tu, ns in giu:
        print(f"   {tu:14s} {' / '.join(ns)}")

    print(f"\n── {len(lech)} từ chú lệch → thống nhất về bản quyển DẠY TRƯỚC:")
    for tu, dich, bo, n in lech:
        print(f"   {tu:14s} giữ “{dich}”   (bỏ: {', '.join(bo)})   {n} mã nút")

    tong = sum(len(v) for v in sua.values())
    print(f"\n── {tong} mã nút phải bù, chia theo quyển: "
          + " · ".join(f"lớp {l}: {len(v)}" for l, v in sorted(sua.items())))

    if not a.ghi:
        print("\nChạy lại với  --ghi  để ghi vào lopN_bu.json.")
        return 0

    for lop, muc in sorted(sua.items()):
        tep = GOC / f"data/tienganh/lop{lop}_bu.json"
        d = json.loads(tep.read_text("utf8")) if tep.exists() else {}
        tu_bu = d.setdefault("tu", {})
        for ma, nghia in muc.items():
            # GIỮ NGUYÊN mọi trường khác của mục bù (`vai`, `ipa`, `hinh`…) —
            # thay cả mục là xoá mất công của người soạn trước.
            cu = tu_bu.get(ma)
            if not isinstance(cu, dict):
                cu = {} if cu is None else {"nghia": cu}
            cu["nghia"] = nghia
            tu_bu[ma] = cu
        tep.write_text(json.dumps(d, ensure_ascii=False, indent=1), "utf8")
        print(f"→ {tep.relative_to(GOC)}  ({len(muc)} mã nút)")

    print("\n⚠ Còn phải DỰNG LẠI, đúng thứ tự — xem docs/day_chuyen_du_lieu_tienganh.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
