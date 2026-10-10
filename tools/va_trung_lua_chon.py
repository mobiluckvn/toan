#!/usr/bin/env python3
"""VÁ CÂU TRẮC NGHIỆM CÓ Ô TRÙNG NHAU.

── VÌ SAO CẦN TỆP NÀY ──
`sinh_bai_tienganh.py` lọc mồi nhử theo MÃ TỪ, mà mã thì bao giờ cũng khác nhau.
Cái bé nhìn thấy lại là `nghia`, và một unit có thể có hai từ cùng nghĩa: TA3 U1 có
`hello`/`hi` đều là "xin chào". Thành ra câu “hello” nghĩa là gì? lên bản thật với
HAI ô cùng ghi "xin chào" — bé bấm ô nào cũng thấy mình vừa chọn giữa hai thứ y hệt.

Bộ sinh đã vá. Nhưng nội dung ĐÃ DỰNG thì không tự sửa, và chạy lại cả dây chuyền
sinh bài thì đụng vào 16 bài đang chạy ngon lành (`--lop N --unit M` còn có lỗi cắt
cụt `lopN_loi.json` chưa sửa). Nên tệp này vá ĐÚNG những câu hỏng, tại chỗ.

── ⚠ MỒI BÙ LẤY TRONG CÙNG BÀI ──
Luật 2 của bộ sinh: mồi nhử lấy từ CÙNG UNIT, vì cả unit cùng chữ cái đầu nên bé
chọn sai là vì chưa phân biệt được âm giữa — đúng cái bài đang dạy. Mồi lấy từ unit
khác thì bé đoán trúng bằng chữ cái đầu và không học được gì. Nên bù cũng chỉ bù từ
chính các ô đã xuất hiện trong bài ấy.

── ⚠ KHÔNG ĐỤNG TỚI ĐÁP ÁN ──
Chỉ bỏ ô THỪA và thêm ô mồi. `answerKey` giữ nguyên, và tệp này từ chối ghi nếu đáp
án không còn nằm trong danh sách ô — thà dừng lại còn hơn sửa một câu thành câu
không có đáp án đúng.

chạy:  python3 tools/va_trung_lua_chon.py --xem      (chỉ xem, không ghi)
       python3 tools/va_trung_lua_chon.py --ghi
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
VUNG = [GOC / "web" / "public" / "content", GOC / "data"]
TEN_O = ("choices", "options", "luaChon")
SO_O_MONG_MUON = 4


def _cau_trong(x):
    """Mọi dict có danh sách ô, đi sâu vào mọi ngóc ngách của tệp."""
    hang = [x]
    while hang:
        y = hang.pop()
        if isinstance(y, list):
            hang.extend(y)
            continue
        if not isinstance(y, dict):
            continue
        for ten in TEN_O:
            o = y.get(ten)
            if isinstance(o, list) and len(o) > 1 and all(not isinstance(v, (dict, list)) for v in o):
                yield y, ten, o
        hang.extend(v for v in y.values() if isinstance(v, (dict, list)))


def _dap_cua(c):
    """Đáp án của một câu, bất kể nó khai kiểu nào."""
    k = c.get("answerKey")
    if isinstance(k, dict):
        for t in ("choice", "value", "text"):
            if k.get(t) is not None:
                return str(k[t])
    if isinstance(k, str):
        return k
    if c.get("answer") is not None:
        return str(c["answer"])
    return None


def _khuon(c) -> str:
    """Khuôn câu hỏi: lời dẫn sau khi bỏ phần trong ngoặc kép.

    “hello” nghĩa là gì?  →  “…” nghĩa là gì?

    ⚠ ĐÂY LÀ CHỖ QUYẾT ĐỊNH MỒI BÙ LẤY TỪ ĐÂU, và bản đầu tôi làm sai: gom MỌI ô
    trong bài thành một kho chung, nên câu “fine” nghĩa là gì? được bù thêm ô
    `hello` — một từ TIẾNG ANH chen vào giữa bốn nghĩa tiếng Việt. Bé không cần biết
    nghĩa cũng loại được nó, tức mồi ấy không mồi gì cả; tệ hơn, nó dạy bé mẹo chọn
    theo mặt chữ thay vì theo nghĩa. Ô bù phải CÙNG LOẠI với ô đang có, và khuôn câu
    hỏi là thứ nói lên loại ấy.
    """
    t = str(c.get("text") or "")
    t = re.sub(r"[“\"'‘][^”\"'’]*[”\"'’]", "“…”", t)
    return f'{c.get("format") or "?"}|{t}'


def _kho_mo_cua_bai(d):
    """Mồi bù, gom theo KHUÔN câu hỏi — cùng bài (luật 2) và cùng loại ô."""
    kho: dict[str, list[str]] = {}
    thay: dict[str, set] = {}
    for c, _, o in _cau_trong(d):
        k = _khuon(c)
        kho.setdefault(k, [])
        thay.setdefault(k, set())
        for v in o:
            s = str(v).strip()
            if s and s.casefold() not in thay[k]:
                thay[k].add(s.casefold())
                kho[k].append(s)
    return kho


def va_mot_tep(duong: Path, ghi: bool):
    d = json.loads(duong.read_text(encoding="utf8"))
    kho = _kho_mo_cua_bai(d)
    doi = []

    for c, ten, o in _cau_trong(d):
        chu = [str(v).strip() for v in o]
        if len(set(x.casefold() for x in chu)) == len(chu):
            continue

        dap = _dap_cua(c)
        # Bỏ ô trùng, GIỮ NGUYÊN THỨ TỰ — đổi thứ tự là đổi cả bài với bé đã làm rồi.
        sach, thay = [], set()
        for v in chu:
            if v.casefold() in thay:
                continue
            thay.add(v.casefold())
            sach.append(v)

        # Bù cho đủ số ô, lấy từ chính kho của bài này.
        for v in kho.get(_khuon(c), []):
            if len(sach) >= min(SO_O_MONG_MUON, len(chu)):
                break
            if v.casefold() not in thay:
                thay.add(v.casefold())
                sach.append(v)

        if dap is not None and dap.strip().casefold() not in {x.casefold() for x in sach}:
            raise SystemExit(
                f"DỪNG: {duong.name} câu {c.get('id')} — vá xong đáp án {dap!r} không còn trong ô. "
                "Không ghi gì cả.")

        doi.append((c.get("id") or "?", chu, sach))
        if ghi:
            c[ten] = sach

    if doi and ghi:
        duong.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    return doi


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true", help="ghi thật; mặc định chỉ xem")
    a = p.parse_args()

    tong = 0
    tep_doi = 0
    for vung in VUNG:
        if not vung.exists():
            continue
        for t in sorted(vung.rglob("*.json")):
            try:
                doi = va_mot_tep(t, a.ghi)
            except json.JSONDecodeError:
                continue
            if not doi:
                continue
            tep_doi += 1
            print(f"\n{t.relative_to(GOC)}")
            for ma, truoc, sau in doi:
                tong += 1
                bo = Counter(x.casefold() for x in truoc)
                trung = [k for k, v in bo.items() if v > 1]
                print(f"  {ma}: trùng {trung}")
                print(f"     trước: {truoc}")
                print(f"     sau  : {sau}")

    print(f"\n{tong} câu trong {tep_doi} tệp." + ("" if a.ghi else "  (chưa ghi — thêm --ghi)"))


if __name__ == "__main__":
    main()
