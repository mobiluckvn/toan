#!/usr/bin/env python3
"""ĐỒ THỊ CON CHO MÁY CON → web/public/content/tienganh/do_thi.json

    tools/tts/.venv/bin/python tools/xuat_do_thi_con.py

── VÌ SAO CẦN ──
`data/ban_do_tieng_anh.json` nặng và chỉ dùng LÚC DỰNG; app đọc tệp bài phẳng đã
sinh sẵn. Nghĩa là lúc chạy, máy con không có đồ thị nào để duyệt — nên mục 2.2.1
(duyệt DFS/BFS để chẩn đoán) và 2.3.3 (lan truyền) của luận văn đều đứng im.

Đây là bản rút gọn đủ cho hai việc ấy, và CHỈ hai việc ấy.

── ⚠ CẮT HẾT CHỮ NGHĨA ──
Nhãn, ví dụ, IPA, nghĩa tiếng Việt — bài học đã mang đủ rồi. Chép lại vào đây là
nhân đôi dữ liệu, mà nhân đôi thì sớm muộn hai bản lệch nhau và không ai biết bản
nào đúng. Đồ thị này chỉ giữ QUAN HỆ: nút nào cần nút nào.

Giữ `type` và `grade` vì phép duyệt cần (lọc theo loại, và biết cạnh nào xuyên
lớp). Giữ `unit` cho nút ngữ pháp vì bộ chọn câu cần biết mẫu câu thuộc bài nào.

── ⚠ GIỮ CẢ NÚT NGOÀI LỚP 1–5 MÀ CẠNH CHẠM TỚI ──
5 nút như thế. Bỏ chúng đi thì cạnh trỏ vào hư không, và phép duyệt ngược dừng
giữa chừng mà không có gì báo — đúng kiểu hỏng lặng lẽ. Chúng được đánh dấu
`ngoai: true` để bên dùng biết đây là nút của lớp khác.
"""
from __future__ import annotations

import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BAN_DO = GOC / "data/ban_do_tieng_anh.json"
RA = GOC / "web/public/content/tienganh/do_thi.json"
LOP = (1, 2, 3, 4, 5)


def main() -> int:
    d = json.loads(BAN_DO.read_text("utf8"))
    nut = {n["id"]: n for n in d["graph"]["nodes"]}
    trong = {i for i, n in nut.items() if n.get("grade") in LOP}

    canh = [e for e in d["graph"]["edges"]
            if e["relation"] == "REQUIRES"
            and (e["source"] in trong or e["target"] in trong)]

    # Nút ngoài lớp 1–5 mà cạnh chạm tới — giữ, nếu không cạnh trỏ vào hư không.
    cham = {e["source"] for e in canh} | {e["target"] for e in canh}
    giu = trong | (cham & set(nut))

    # Nút nào được DẠY ở bài nào — suy từ chính tệp bài đã sinh, không khai tay.
    #
    # Máy con cần điều này để đi từ "nút tiên quyết" sang "bài nào dạy nút ấy" rồi
    # tải bài đó về lấy vốn từ. Không có nó thì đồ thị chỉ tra được quan hệ giữa
    # các mã, mà mã thì không dạy được cho bé.
    bai_cua = {}
    for f in sorted((GOC / "web/public/content").glob("ta*/DL_TA*_B*.json")):
        b = json.loads(f.read_text("utf8"))
        muc = [x for v in (b.get("practice", {}).get("pools") or {}).values() for x in v]
        muc += (b.get("assessment", {}).get("items") or [])
        for i in muc:
            for m in (i.get("maNutDs") or []):
                bai_cua.setdefault(m, b["id"])

    # ── NHÃN ĐỌC ĐƯỢC ──
    #
    # ⚠ Ngoại lệ CÓ CHỦ Ý của luật "cắt hết chữ nghĩa" ở đầu tệp. Luật ấy nhắm vào
    # việc chép lại NỘI DUNG BÀI (ví dụ, IPA, nghĩa dài) — chép là nhân đôi dữ
    # liệu rồi hai bản lệch nhau. Còn đây là một nhãn NGẮN để gọi tên cái nút.
    #
    # Không có nó thì màn hình bày ra `v_g5_u1_city` cho bố mẹ đọc — và đúng thế
    # đã xảy ra ngày 22-08: Góc bố mẹ hiện `CHUONG%3A1%40G3`. Một mã máy, lại còn
    # mã hoá URL. Nguồn nhãn là `chuan_lopN.json`, tức cùng một nguồn với mọi thứ
    # khác, nên không có bản thứ hai để mà lệch.
    nhan = {}
    for l in LOP:
        f = GOC / f"data/tienganh/chuan_lop{l}.json"
        if not f.exists():
            continue
        for u in json.loads(f.read_text("utf8"))["unit"]:
            for t in u["tu"]:
                if t.get("ma") and t.get("tu"):
                    nhan[t["ma"]] = (f'{t["tu"]} — {t["nghia"]}' if t.get("nghia")
                                     else t["tu"])
            for m in u["mau_cau"]:
                if m.get("ma") and m.get("cong_thuc"):
                    nhan[m["ma"]] = m["cong_thuc"]

    ra_nut = {}
    for i in sorted(giu):
        n = nut[i]
        m = {"t": n.get("type") or "?"}
        if bai_cua.get(i):
            m["b"] = bai_cua[i]
        if nhan.get(i):
            m["n"] = nhan[i]
        g = n.get("grade")
        if g is not None:
            m["g"] = g
        if n.get("unit") is not None:
            m["u"] = n["unit"]
        if i not in trong:
            m["ngoai"] = True
        ra_nut[i] = m

    # Cạnh: chỉ (từ, tới). `can` là nút PHẢI CÓ TRƯỚC.
    #
    # ⚠ HƯỚNG CỦA CẠNH. Bản đồ ghi `source REQUIRES target`, tức là source CẦN
    # target — nên `can` = target, `truoc_khi` = source. Đảo nhầm hai đầu thì phép
    # lan truyền ngược chạy đúng chiều ngược lại: bé sai một từ ở unit 1 và hệ
    # thống đi tìm nguyên nhân ở unit 20. Cùng lối khai với `thang` trong
    # `chuan_lopN.json` (xem `chuan_tienganh.py`), để hai nơi không lệch nhau.
    ra_canh = []
    da = set()
    for e in canh:
        k = (e["target"], e["source"])
        if k in da:
            continue
        da.add(k)
        c = {"can": e["target"], "truoc_khi": e["source"], "loai": "ban_do"}
        g1, g2 = nut[e["target"]].get("grade"), nut[e["source"]].get("grade")
        if g1 is not None and g2 is not None and g1 != g2:
            c["xuyen_lop"] = True
        ra_canh.append(c)

    # Thang tiên quyết TỪ VỰNG — sinh ở `chuan_tienganh.py` (Đợt 0), không có
    # trong bản đồ gốc. Gộp vào đây để máy con chỉ phải đọc MỘT tệp.
    for l in LOP:
        p = GOC / f"data/tienganh/chuan_lop{l}.json"
        if not p.exists():
            continue
        for t in json.loads(p.read_text("utf8")).get("thang", []):
            if t.get("loai") == "ban_do":
                continue          # đã có ở trên, đừng đếm hai lần
            ra_canh.append(t)

    ra = {
        "_doc": "Đồ thị con lớp 1–5 cho MÁY CON duyệt. Sinh bằng "
                "tools/xuat_do_thi_con.py, ĐỪNG sửa tay.",
        "_nguon": ["data/ban_do_tieng_anh.json", "data/tienganh/chuan_lop*.json"],
        "nut": ra_nut,
        "canh": ra_canh,
    }
    RA.parent.mkdir(parents=True, exist_ok=True)
    RA.write_text(json.dumps(ra, ensure_ascii=False, separators=(",", ":")) + "\n", "utf8")

    kb = RA.stat().st_size / 1024
    import collections
    lo = collections.Counter(c.get("loai") for c in ra_canh)
    print(f"→ {RA.relative_to(GOC)}  ({kb:.0f} KB)")
    print(f"   {len(ra_nut)} nút ({len(giu - trong)} ngoài lớp 1–5) · {len(ra_canh)} cạnh")
    print(f"   nút biết thuộc bài nào: {sum(1 for m in ra_nut.values() if m.get('b'))}")
    print(f"   nút có nhãn đọc được:   {sum(1 for m in ra_nut.values() if m.get('n'))}")
    print(f"   cạnh theo loại: {dict(lo)}")
    print(f"   xuyên lớp: {sum(1 for c in ra_canh if c.get('xuyen_lop'))}")
    if kb > 250:
        print("⚠ TỆP TO HƠN DỰ TÍNH — máy con tải mỗi lần mở quyển, xem lại đang giữ gì thừa.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
