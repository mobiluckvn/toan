#!/usr/bin/env python3
"""SOI MỒI NHỬ — câu hỏi nào có từ HAI đáp án đúng trở lên.

    python3 tools/soat_moi_nhu.py            # cả ba quyển
    python3 tools/soat_moi_nhu.py --lop 4

Bác bắt 29-08-2026: *"Yêu cầu câu trả lời trong các bài đọc phải đảm bảo chỉ có
01 đáp án đúng thôi nhé. Các câu nào 02 đáp án đúng thì cần viết lại cho nó sai
đi nhé."* Rà tay cả ba quyển ra 19 chỗ — không chỗ nào cổng bắt được, vì chỗ nào
cũng đúng chính tả, đúng túi từ, đúng khuôn. Chúng chỉ hỏng khi đọc ĐOẠN và nhìn
TRANH cùng lúc.

── VÌ SAO ĐÂY LÀ CÔNG CỤ, KHÔNG PHẢI CỔNG ──
Cả hai phép dưới đây đều báo cả những chỗ ĐÚNG:

    L3 U18  "What's she doing?" đáp "She's reading." · mồi "She's writing."
            → HỢP LỆ: đoạn nói HE's writing, chủ ngữ khác nên mồi sai thật.

Muốn không báo oan thì phải hiểu chủ ngữ trỏ vào ai trên bức tranh — máy không
làm được. Nên đây là công cụ để NGƯỜI đọc lại, không phải cổng để chặn. Dựng nó
thành cổng là ép người ta nới mã cho cổng xanh, đúng cái bẫy
[[cong-ghim-chinh-ta-thay-vi-tinh-chat]].

── HAI PHÉP ──
① MỒI TRÙNG VẬT TRÊN TRANH — mồi nêu một thứ bức tranh CÓ VẼ. Bắt được kiểu
  "What's this?" hỏi trống không giữa một bức có năm đồ vật.
② MỒI TRÙNG VỊ NGỮ CỦA ĐOẠN — bỏ chủ ngữ hai bên rồi so. Mạnh hơn hẳn phép ①:
  nó bắt được "He's short." (chữ `short` không có trên tranh nên phép ① mù) và
  "We collected seashells." (đoạn nói She, mà câu hỏi lại hỏi cả GIA ĐÌNH).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

# Bút vẽ cảnh nào VẼ RA thứ gì — CHÉP TỪ `web/test/tienganh_dochieu.test.mjs`.
# ⚠ Hai bản này phải khớp nhau. Lệch thì công cụ soi một bộ vật, cổng soi một bộ
# khác, và chỗ nào chỉ một bên biết thì chỗ ấy không ai canh.
TU_CUA_VE = {
    "nguoi": ["teacher", "friend", "girl", "boy", "mother", "father", "sister",
              "brother", "doctor", "nurse", "farmer", "people", "face", "nose",
              "eye", "mouth", "ear", "hair", "head", "hand", "name"],
    "ban": ["desk", "table"], "ghe": ["chair"], "bang": ["board"],
    "cuaSo": ["window"], "cua": ["door"], "giuong": ["bed"], "sofa": ["chair"],
    "giaSach": ["book", "library", "bookshop"], "cay": ["tree", "garden"],
    "may": ["cloud"], "matTroi": ["sun", "sunny"],
    "nha": ["school", "house", "building"],
    "oto": ["car"], "leu": ["tent"], "luaTrai": ["campfire"], "ho": ["lake"],
    "bienBao": ["sign", "road"],
    "tuKinh": ["bookshop", "bakery", "library", "shop"],
    "guong": ["mirror"], "dongHo": ["clock", "o'clock"],
    "giaVe": ["picture", "art"], "khungAnh": ["picture", "photo"],
    "bangGhim": ["picture", "photo", "board"],
    "bangLuoi": ["calendar", "timetable", "day", "Monday", "map"],
    "banDo": ["map"],
    "anhNho": ["picture", "photo", "beach", "countryside", "city", "lake",
               "bridge", "house", "tree", "sun"],
    "bangMau": ["colour"], "matTrang": ["moon"],
    "bangThoiTiet": ["weather", "sunny", "rainy", "windy", "cloudy", "sun"],
    "huyChuong": ["medal"], "longChim": ["bird"],
    "hangRao": ["garden"], "songSat": ["zoo"], "zoo": ["zoo"],
}
DO_CUA_NEN = {"toi": ["lake", "river"], "ho": ["lake", "river"], "co": ["garden"],
              "san": ["school", "playground"], "pho": ["street", "road", "city"],
              "lop": ["classroom"], "phong": ["house", "room"]}
DO_CUA_VIEC = {"cycling": ["bike"], "reading": ["book"], "writing": ["pen", "book"],
               "cooking": ["pot"], "skipping": ["rope"], "singing": ["song"]}

# Chủ ngữ mở đầu — cắt đi để còn lại VỊ NGỮ đem so.
CHU_NGU = re.compile(r"^(I|You|He|She|It|They|We)('s|'re|'m|'ve|'ll|'d)?\s+", re.I)


def chu(s: str) -> list[str]:
    return re.findall(r"[a-z']+", str(s or "").lower())


def trong_tranh(khai: dict) -> set[str]:
    """Bộ chữ mà BỨC TRANH vẽ ra — cùng luật với cổng, TRỪ bút `nguoi`.

    ⚠ BỎ `TU_CUA_VE["nguoi"]`. Bảng ấy là một bộ PHÂN LOẠI ("bút này vẽ ra một
    người, và người thì có mặt · mũi · mắt, có thể là mẹ hay bố hay cô giáo"),
    KHÔNG phải lời khẳng định rằng cả hai mươi mốt chữ ấy đều có trên tranh. Để
    nguyên thì mọi bức có một người bị báo là có đủ mẹ · bố · chị · em · bác sĩ
    · y tá — 40 trong 88 dòng của bản đầu là loại ấy, và chúng nhấn chìm mấy
    dòng thật.

    Đổi lại phép ① mù với người: bức vẽ HAI bạn gái, một nấu một múa, thì nó
    không kêu. Chỗ ấy phải nhìn bằng mắt — và đó đúng là lý do tệp này là công
    cụ chứ không phải cổng.
    """
    ra: set[str] = set()
    for v in khai.get("vat") or []:
        if v.get("tu"):
            ra.update(chu(v["tu"]))
            ra.update(DO_CUA_VIEC.get(v["tu"], []))
        if v.get("ao_la"):
            ra.update(chu(v["ao_la"]))
        if v.get("ve") and v["ve"] != "nguoi":
            ra.update(chu(" ".join(TU_CUA_VE.get(v["ve"], []))))
    nen = khai.get("nen")
    ra.update(DO_CUA_NEN.get(nen.get("kieu") if isinstance(nen, dict) else nen, []))
    return ra


def vi_ngu(cau: str) -> str | None:
    """Bỏ chủ ngữ, trả về phần còn lại. `None` nếu câu không mở bằng đại từ."""
    s = str(cau).strip().rstrip(".")
    m = CHU_NGU.match(s)
    return s[m.end():].strip().lower() if m else None


def soi(lop: int) -> int:
    tep = GOC / f"data/tienganh/canh_lop{lop}.json"
    if not tep.exists():
        return 0
    dem = 0
    for k in json.loads(tep.read_text("utf8")):
        tt = trong_tranh(k)
        vn = {v for v in (vi_ngu(c) for c in k["doan"]) if v}
        for h in k.get("hoi") or []:
            # Chữ CHUNG giữa đáp án và mồi không phải chỗ phân biệt hai câu.
            # "It's on the desk." ↔ "It's under the desk." khác nhau ở GIỚI TỪ,
            # mà `desk` thì cả hai đều có — báo nó lên là báo một chỗ không hỏng.
            chu_dap = set(chu(h["dap"]))
            for m in h.get("moi") or []:
                ly_do = []
                trung = [w for w in chu(m) if w in tt and w not in chu_dap]
                if trung:
                    ly_do.append(f"① tranh CÓ vẽ “{'·'.join(trung)}”")
                if (v := vi_ngu(m)) and v in vn:
                    ly_do.append("② đoạn đọc khẳng định vị ngữ ấy")
                if ly_do:
                    dem += 1
                    print(f"  {k['id']:18s} “{h['hoi']}”")
                    print(f"      đáp “{h['dap']}” · mồi “{m}”")
                    for x in ly_do:
                        print(f"        {x}")
    return dem


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, help="chỉ soi một quyển")
    a = p.parse_args()
    tong = 0
    for lop in ([a.lop] if a.lop else [3, 4, 5]):
        print(f"══ LỚP {lop} ══")
        tong += soi(lop)
    print(f"\n{tong} chỗ ĐÁNG ĐỌC LẠI — không phải chỗ nào cũng sai.")
    print("Mồi khác CHỦ NGỮ với câu trong đoạn thì hợp lệ; chốt bằng dòng phụ")
    print("tiếng Việt (dấu `|` trước mũi tên) cũng làm mồi sai đi. Xem")
    print("docs/lam_bai_tranh.md mục “MỘT CÂU HỎI, ĐÚNG MỘT ĐÁP ÁN ĐÚNG”.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
