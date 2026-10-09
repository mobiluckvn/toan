#!/usr/bin/env python3
"""SOI CÂU HỎI — hỏi có ĐÚNG cái mà đáp án trả lời không, và có chốt ĐANG HỎI AI.

    python3 tools/soat_hoi_chot.py
    python3 tools/soat_hoi_chot.py --lop 5

Bác bắt lần hai, 29-08-2026: *"review bài luyện đọc ở tất cả lớp 3,4,5 đảm bảo
câu trả lời của các bài đọc ấy chỉ có 01 câu là đúng thôi."*

`soat_moi_nhu.py` soi MỒI — mồi nào cũng đúng nốt. Tệp này soi phía bên kia:
**câu hỏi**. Ba họ dưới đây đều làm câu hỏi có hai đáp án đúng (hoặc không có
đáp án đúng nào), và soat_moi_nhu mù với cả ba vì nó không đọc câu hỏi.

── HỌ ① CÂU HỎI LỆCH ĐẠI TỪ VỚI ĐÁP ÁN ──
    L5 C3  "How does HE stay healthy?" → "SHE does yoga."
Đọc câu tiếng Anh thì KHÔNG đáp án nào đúng. Chúng lọt vào vì bài ôn chương chép
đề bài của bài unit mà quên đổi đại từ, còn dòng phụ tiếng Việt thì đã chốt đúng
người nên đọc lướt bằng tiếng Việt thấy hợp lý hoàn toàn.

── HỌ ② CÂU HỎI LỆCH MỐC THỜI GIAN VỚI ĐÁP ÁN ──
    L4 C3  "What do you do in the MORNING?" → "I wash the dishes." (đoạn: in the
           EVENING) · L5 C4 "…wear in WINTER?" → "I wear a T-shirt."
Cùng một gốc, và từng được ghi lại như một CHỦ Ý: mượn đề bài của unit rồi để
dòng phụ tiếng Việt lái sang mốc khác. Nhưng bé đang học đọc TIẾNG ANH — dòng
phụ chốt được ĐANG HỎI AI, không chốt lại được NGHĨA của câu hỏi.

── HỌ ③ CÂU HỎI KHÔNG CHỐT ĐANG HỎI AI ──
    L5 U11 "Who's this?" giữa bức có mẹ NGỒI CẠNH một bạn nhỏ → `It's my sister.`
           cũng đúng.
Bức nào có từ hai nhân vật trở lên mà câu hỏi dùng `he/she/this` thì dòng phụ
phải chốt bằng thứ NHÌN THẤY ĐƯỢC. Phép soi tìm những dòng phụ không có chữ chốt
nào — nó báo cả chỗ đúng (bức chỉ có một người thật sự nổi), nên đọc từng dòng.

⚠ Cũng như `soat_moi_nhu.py`: đây là CÔNG CỤ CHO NGƯỜI ĐỌC, không phải cổng.
Dựng thành cổng là ép người ta nới mã cho cổng xanh.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

NAM = re.compile(r"\b(he|his|him)\b", re.I)
NU = re.compile(r"\b(she|her|hers)\b", re.I)

# Mốc thời gian: mỗi nhóm là một trục — hỏi ở một mốc thì đáp phải ở đúng mốc ấy.
MOC = [
    {"in the morning", "in the afternoon", "in the evening", "at night", "at noon"},
    {"in spring", "in summer", "in autumn", "in winter"},
    {"today", "yesterday", "tomorrow", "last weekend", "last summer"},
]

# Chữ CHỐT trong dòng phụ — chỉ ra một người/vật cụ thể trên tranh.
# Chốt được bằng bốn lối: VỊ TRÍ (bên trái · góc trên) · DÁNG VẺ (áo đỏ · tóc
# tết) · VAI (mẹ · bố · cô giáo) · TÊN RIÊNG (bạn Ben). Thiếu cả bốn thì dòng
# phụ chỉ nhắc lại câu hỏi bằng tiếng Việt, và bé vẫn không biết cô hỏi ai.
CHOT = re.compile(
    r"bên trái|bên phải|áo |váy |tết|tóc |ngồi|đứng|người lớn|duy nhất|đầu hàng|"
    r"gian |sofa|giường|bàn|cửa|góc|phía trước|phía sau|trên tường|đội|mặc|"
    r"kể chuyện|chỉ tay|khuôn mặt|màu |mẹ|bố |cô giáo|bạn [A-ZĐ]", re.I)
DAI_TU = re.compile(r"\b(he|she|his|her|this|they|them)\b", re.I)


def hinh_nguoi(k: dict) -> int:
    """Đếm NHÂN VẬT trên tranh — cả người vẽ tay lẫn hình từ vựng có người.

    Hình `reading` · `cycling` … cũng là một nhân vật: bút vẽ chúng thành bóng
    người, và bé không phân biệt được bóng nào là bạn trai bóng nào là bạn gái.
    Đó chính là chỗ L3 U18 · U19 hỏng.
    """
    CO_NGUOI = {"reading", "writing", "cycling", "skipping", "walking", "run",
                "running", "cooking", "singing", "dancing", "swimming", "doctor",
                "nurse", "farmer", "teacher", "firefighter", "writer", "gardener",
                "watch TV", "mops"}
    return sum(1 for v in k["vat"]
               if v.get("ve") == "nguoi" or v.get("tu") in CO_NGUOI)


def moc_cua(s: str) -> set[str]:
    s = " " + s.lower() + " "
    return {m for nhom in MOC for m in nhom if m in s}


def soi(lop: int) -> int:
    tep = GOC / f"data/tienganh/canh_lop{lop}.json"
    if not tep.exists():
        return 0
    dem = 0
    for k in json.loads(tep.read_text("utf8")):
        nv = hinh_nguoi(k)
        # Câu nào trong đoạn mang đúng vị ngữ của đáp án — dùng để soi họ ②:
        # mốc thời gian của đáp án nằm ở CÂU NGUỒN chứ không ở lựa chọn.
        doan = " ".join(k["doan"])
        for h in k.get("hoi") or []:
            hoi, dap, vi = h["hoi"], h["dap"], h.get("vi", "")
            ly_do = []

            if (NAM.search(hoi) and NU.search(dap)) or \
               (NU.search(hoi) and NAM.search(dap)):
                ly_do.append("① câu hỏi và đáp án LỆCH ĐẠI TỪ")

            mh = moc_cua(hoi)
            if mh:
                # mốc của đáp án: lấy ở chính đáp án, không có thì ở câu nguồn
                loi = dap if moc_cua(dap) else next(
                    (c for c in k["doan"]
                     if c.rstrip(".").lower().startswith(dap.rstrip(".").lower())
                     or dap.rstrip(".").lower() in c.lower()), "")
                md = moc_cua(loi)
                for nhom in MOC:
                    a, b = mh & nhom, md & nhom
                    if a and b and not (a & b):
                        ly_do.append(f"② câu hỏi hỏi “{'·'.join(a)}” mà đáp án là "
                                     f"“{'·'.join(b)}”")

            if nv >= 2 and DAI_TU.search(hoi) and not CHOT.search(vi):
                ly_do.append(f"③ bức có {nv} nhân vật mà dòng phụ không chốt ai")

            if ly_do:
                dem += 1
                print(f"  {k['id']:18s} “{hoi}”  | {vi}")
                print(f"      đáp “{dap}”")
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
    print(f"\n{tong} chỗ ĐÁNG ĐỌC LẠI.")
    print("Họ ① và ② là lỗi thật gần như chắc chắn — câu tiếng Anh không khớp đáp.")
    print("Họ ③ báo cả chỗ đúng: bức có hai người mà chỉ một người ĐANG LÀM việc")
    print("được hỏi thì không cần chốt. Xem docs/lam_bai_tranh.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
