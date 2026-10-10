#!/usr/bin/env python3
"""XUẤT BỘ NGƯỠNG CHO MÁY CON — `data/nguong.json` → `web/public/content/nguong.json`.

    python3 tools/xuat_nguong.py

── VÌ SAO PHẢI XUẤT, KHÔNG ĐỂ MÁY CON ĐỌC THẲNG `data/` ──
`data/` không nằm trong `web/`, nên Vite không phục vụ nó. Và tệp gốc có cả phần
dành cho NGƯỜI đọc (`_doc`, `canCu`, `oDau`) — thứ máy con không cần mà vẫn phải tải
về trên mạng di động của một đứa trẻ. Tệp chạy chỉ gồm `phienBan` và giá trị.

Mục 3.8.2 nói rõ: "Mỗi lần phát hành, toàn bộ bảng `nguong` được xuất thành một tệp
`nguong.json` có số phiên bản." Từ đợt 3, nguồn của lệnh xuất này sẽ là bảng `nguong`
trên Firestore thay vì tệp gốc; hình dạng tệp ra GIỮ NGUYÊN, nên máy con không phải
đổi gì.

⚠ FAIL-CLOSED. Giá trị ngoài [canDuoi, canTren] thì DỪNG, không xuất. Khoảng hợp lệ
  là giới hạn cứng (mục 3.8.1) — để lọt một giá trị ngoài khoảng ra tệp chạy thì cả
  hàng rào ấy thành trang trí.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NGUON = GOC / "data/nguong.json"
RA = GOC / "web/public/content/nguong.json"

# Mấy ngưỡng mang HAI con số thì soi theo trường nào — khớp `TRUONG_SO` của
# `src/chung/lib/nguong.js`. Lệch ở đây là tệp chạy soi lỏng hơn mã.
TRUONG_SO = {"NG05": ["slip", "guess"], "NG17": ["ti"]}


def soi(ds: list[dict]) -> list[str]:
    loi = []
    for x in ds:
        ma, v = x["ma"], x["giaTri"]
        so = [v.get(t) for t in TRUONG_SO[ma]] if ma in TRUONG_SO else [v]
        for s in so:
            if not isinstance(s, (int, float)):
                loi.append(f"{ma}: giá trị không phải số — {s!r}")
            elif not (x["canDuoi"] <= s <= x["canTren"]):
                loi.append(f"{ma}: {s} ngoài khoảng [{x['canDuoi']}, {x['canTren']}]")
    # Ràng buộc giữa các ngưỡng — mục 3.8.4, cùng luật với `soiNguong` bên JS.
    g = {x["ma"]: x["giaTri"] for x in ds}
    if g.get("NG08") is not None and g.get("NG07") is not None:
        if g["NG08"] > g["NG07"] - 0.20:
            loi.append(f"NG08: θ_yếu {g['NG08']} phải ≤ θ − 0,20 (θ = {g['NG07']})")
    for ma, truong in (("NG03", None), ("NG04", None), ("NG05", "slip"), ("NG05", "guess")):
        v = g.get(ma, {}).get(truong) if truong else g.get(ma)
        if isinstance(v, (int, float)) and v >= 0.5:
            loi.append(f"{ma}: {truong or ma} = {v} phải < 0,5 để mô hình không suy biến")
    return loi


def main() -> None:
    goc = json.loads(NGUON.read_text("utf8"))
    ds = goc["nguong"]
    loi = soi(ds)
    if loi:
        print("✗ KHÔNG xuất — bộ ngưỡng gốc có chỗ sai:", file=sys.stderr)
        for l in loi:
            print("   ·", l, file=sys.stderr)
        sys.exit(1)

    ra = {
        "_doc": "SINH RA bởi tools/xuat_nguong.py từ data/nguong.json — ĐỪNG sửa tay.",
        "phienBan": goc["phienBan"],
        "hieuLucTu": goc["hieuLucTu"],
        "macDinh": {x["ma"]: x["giaTri"] for x in ds},
        # Giá trị theo phạm vi hẹp — rỗng cho tới khi chuyên gia khai (đợt 3).
        "theoPhamVi": goc.get("theoPhamVi", {}),
    }
    RA.parent.mkdir(parents=True, exist_ok=True)
    RA.write_text(json.dumps(ra, ensure_ascii=False, indent=1), "utf8")
    print(f"  ✔ {len(ds)} ngưỡng · phiên bản {ra['phienBan']} → {RA.relative_to(GOC)}")


if __name__ == "__main__":
    main()
