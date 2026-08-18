#!/usr/bin/env python3
"""DỰNG ĐỀ BÀI VIẾT NGẮN — mỗi chương một đề, chấm bằng AI.

    python3 tools/sinh_vietbai_tienganh.py --lop 3

Bác chốt 18-08-2026, bốn điều:
  1. sửa lỗi và khen CỤ THỂ — chỉ ra câu sai ở đâu, sửa lại cho đúng;
  2. có ĐIỂM để vào sổ, và phải nói rõ là AI chấm;
  3. chỉ gợi ý bằng VỐN TỪ ĐÃ HỌC, không dạy từ mới;
  4. bố mẹ đọc được bài viết và lời chấm.

Tệp này lo phần ĐỀ. Ba điều còn lại nằm ở `web/functions/src/chamviet.js` (lời dặn
cho mô hình), `web/src/mon/tienganh/lib/chamviet.js` (bóc và SOI lời chấm) và
`components/VietBai.jsx` (màn hình).

── ĐỀ GỒM NHỮNG GÌ, VÀ VÌ SAO ──

Bé lớp 3 chưa viết được tiếng Anh từ chỗ trống. Nên đề KHÔNG chỉ là một câu hỏi:
nó mang theo cả chỗ dựa.

    de       việc phải làm, bằng TIẾNG VIỆT — bé đọc được tiếng Việt
    mauCau   những mẫu câu của chương, để bé ghép theo
    vonTu    vốn từ đã học TỚI CHƯƠNG NÀY, hiện thành bảng từ bấm được
    toiThieu số câu tối thiểu

`vonTu` còn là thứ ĐEM ĐI CHẤM: máy chấm được dặn chỉ gợi ý bằng đúng bảng ấy, và
`lib/chamviet.js` soi lại lời chấm để bắt chữ lạ. Dặn dò là thứ mô hình *có thể*
theo; soi lại là thứ nó không cần theo. Cả môn này đã học bài ấy hai lần rồi.

── VÌ SAO ĐỀ KHÔNG PHẢI TIẾNG ANH ──
Đề bằng tiếng Anh thì bé phải đọc hiểu đề trước đã, và bài kiểm tra viết hoá ra
kiểm tra đọc. Đề tiếng Việt, viết tiếng Anh — đúng một việc một lúc.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}

# Bé lớp 3 viết 2–3 câu là một bài. Đòi nhiều hơn thì bé chép lại mẫu cho xong.
CAU_TOI_THIEU = 2

# Đề của từng chương — soạn TAY, vì "viết về cái gì" là việc của người.
# Khoá là số chương; thiếu chương nào thì bộ sinh nói ra chứ không bịa một đề chung.
DE = {
    1: ("Con viết 2–3 câu tự giới thiệu nhé: chào, tên con là gì, "
        "rồi chào tạm biệt."),
    2: ("Con viết 2–3 câu về cơ thể và sở thích của con: con thích làm gì, "
        "và chỉ một bộ phận trên mặt."),
    3: ("Con viết 2–3 câu về đồ dùng học tập của con: con có gì, màu gì."),
    4: ("Con viết 2–3 câu về nhà con: trong phòng có gì, và một người trong nhà "
        "làm nghề gì."),
    5: ("Con viết 2–3 câu về con vật hoặc đồ chơi con thích, và con đang làm gì."),
}


def chu_trong(s: str) -> list[str]:
    return re.findall(r"[a-z']+", str(s or "").lower())


def dung(lop: int) -> list[dict]:
    tm = GOC / f"web/public/content/{QUYEN[lop]}"
    bais = [json.loads(p.read_text("utf8"))
            for p in sorted(tm.glob(f"DL_{QUYEN[lop].upper()}_B*.json"))]
    theo_chuong: dict[int, list[dict]] = {}
    for b in bais:
        theo_chuong.setdefault(b["chuong"], []).append(b)

    ra = []
    von: list[dict] = []          # dồn dần: chương sau có cả vốn của chương trước
    da_co: set[str] = set()
    for c, ds in sorted(theo_chuong.items()):
        for b in ds:
            for v in b["knowledgeCore"]["vocabulary"]:
                if v["tu"] not in da_co:
                    da_co.add(v["tu"])
                    von.append({"tu": v["tu"], "nghia": v["nghia"]})
        if c not in DE:
            print(f"  ⚠ chương {c}: chưa soạn đề, bỏ qua")
            continue
        mau = [m["cau"] for b in ds for m in (b["knowledgeCore"].get("mauCauDs") or [])]
        ra.append({
            "id": f"VIET:TA{lop}.C{c}",
            "chapter": c,
            "loai": "vietbai",
            "name": f"BÀI VIẾT {c} · {ds[0]['tenChuong'].upper()}",
            "de": DE[c],
            "toiThieu": CAU_TOI_THIEU,
            # Mẫu câu của CHÍNH chương này — bé ghép theo, không phải nhớ suông.
            "mauCau": list(dict.fromkeys(mau)),
            # Vốn từ DỒN từ chương 1 tới đây: bé viết về mình thì vẫn cần "I'm" của
            # chương 1 ở bài chương 4. Cắt theo đúng chương là cắt mất cả câu chào.
            "vonTu": list(von),
        })
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3, choices=[1, 2, 3])
    a = p.parse_args()
    ds = dung(a.lop)
    ra = GOC / f"web/public/content/{QUYEN[a.lop]}/vietbai.json"
    ra.write_text(json.dumps(ds, ensure_ascii=False, indent=1), "utf8")
    for k in ds:
        print(f"  chương {k['chapter']}: {len(k['vonTu'])} từ · {len(k['mauCau'])} mẫu câu")
    print(f"→ {ra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
