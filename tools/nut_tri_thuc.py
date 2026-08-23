#!/usr/bin/env python3
"""GÁN MÃ NÚT TRI THỨC CHO MỘT CÂU HỎI — dùng chung cho mọi bộ sinh.

Bác chốt 23-08-2026: bài ĐỌC và bài VIẾT phải vào engine. Muốn vào engine thì mỗi
câu phải mang `maNut` — hàm nền BKT đọc `bktUnit` từ đó rồi mới chấm được mức
NÚT. Trước bản này, 176/176 câu đọc hiểu không có mã nút nào, nên bé làm xong mà
không nút nào được ghi công.

── ⚠ VÌ SAO LÀ MỘT TỆP RIÊNG ──
Hai bộ sinh cần đúng luật này: `sinh_bai_tranh.py` (câu theo unit) và
`sinh_dochieu_tienganh.py` (câu theo chương). Để mỗi bên tự chép thì sớm muộn
lệch nhau — hôm nay tôi vừa dính đúng thế với danh sách cụm từ vựng, và bộ soi
báo oan 30 ô. Nên viết một lần, hai bên import.

── LUẬT GÁN, VÀ VÌ SAO THEO THỨ TỰ NÀY ──

    ① ĐÁP ÁN      thứ bé phải tự nghĩ ra. Sai ở đây là chưa vững chính từ ấy.
    ② CÂU HỎI     đáp án không có từ nào (kiểu "Có" · "Không") thì hỏi cái gì
                  chính là nút đang được kiểm.
    ③ ĐOẠN VĂN    lưới cuối. Kém chính xác nhất nhưng còn hơn không có nút, vì
                  không có nút thì lượt ấy biến mất khỏi engine.

Đo trên cả ba quyển: ① phủ 151/176, thêm ② và ③ thì phủ 176/176.

── ⚠ MỘT NÚT CHÍNH, GIỐNG `sinh_bai_tienganh.nut()` ──
Bản ghi `attempts` chỉ mang được MỘT `bktUnit`. Ghi hai nút cho một lượt là một
câu đúng được tính công hai lần, mức thạo phồng lên mà không ai lần ra được.
`maNutDs` giữ đủ để lan truyền chẩn đoán (mục 2.3.3) dùng sau, nhưng KHÔNG chỗ
nào được lấy nó ra cộng điểm.

Nút CHÍNH là từ DÀI NHẤT khớp được — "table tennis" thắng "table", vì cụm mới là
thứ sách dạy.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent


# ⚠ CHỮ KHÔNG ĐƯỢC LÀM NÚT — dù chúng CÓ trong bảng từ vựng.
#
# Bản đầu tôi tra thẳng mọi từ, và nút được gán nhiều nhất trên 176 câu là
# `v_g1_u3_can` (20 câu) — tức "CÁI LON", vì `can` trong "I can see a dog." bị
# nhận là danh từ đồ uống của lớp 1. Kế đó là `i` (13 câu), `what` (8), `have`,
# `how`. Hơn bốn mươi câu nhận một nút chẳng liên quan gì tới thứ câu ấy hỏi.
#
# Gán SAI nút còn tệ hơn KHÔNG gán: không gán thì engine không biết gì và ta
# thấy được chỗ trống; gán sai thì mức thạo "cái lon" của bé tăng lên mỗi lần bé
# đọc hiểu đúng, và không ai lần ra được con số ấy từ đâu.
#
# Danh sách này là hợp của hai danh sách đã có sẵn trong kho — `KHONG_CHU` của
# `sinh_bai_tranh.py` (chữ nối) và danh sách chữ TRÙNG MẶT của cổng
# `tienganh_dochieu.test.mjs` (`can` là cái lon mà cũng là "có thể") — cộng thêm
# đại từ và từ để hỏi. Chép danh sách là chuyện đáng ngại, nhưng ba nơi này ở ba
# thứ tiếng khác nhau (Python · Python · JS) nên không import chung được; cổng
# `tienganh_vao_engine` soi kết quả nên hai bên lệch là thấy ngay.
BO_QUA_NUT = {
    # chữ nối
    "can", "see", "do", "does", "did", "have", "has", "is", "are", "was", "were",
    "am", "be", "will", "would", "like", "there", "that", "that's", "there's",
    "this", "it", "it's", "a", "an", "the", "and", "to", "of", "s",
    # đại từ và sở hữu
    "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "our", "their", "its",
    # từ để hỏi
    "what", "where", "when", "who", "how", "why", "which", "whose",
    # trùng mặt chữ: vừa là vật vừa là chữ thường dùng
    "top", "play", "watch", "left", "right", "mop", "square", "want", "come in",
}


def kho_nut(lop: int) -> dict[str, str]:
    """từ (thường) → mã nút, TÍCH LUỸ từ lớp 1 tới `lop`.

    Tích luỹ chứ không riêng unit: đáp án bài đọc dùng cả vốn lớp dưới ("I can see
    a dog." ở lớp 5, mà `dog` học từ lớp 1). Bó trong unit thì chỉ gán được
    72/124 câu.
    """
    ra: dict[str, str] = {}
    for l in range(1, lop + 1):
        tep = GOC / f"data/tienganh/chuan_lop{l}.json"
        if not tep.exists():
            continue
        for u in json.loads(tep.read_text("utf8"))["unit"]:
            for t in u["tu"]:
                w = str(t.get("tu") or "").lower()
                if t.get("ma") and w and w not in BO_QUA_NUT:
                    ra.setdefault(w, t["ma"])
    return ra


def _tim(s, kho: dict[str, str], ds_tu: list[str]) -> list[str]:
    s = str(s or "").lower()
    ra = []
    for w in ds_tu:
        if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", s):
            ma = kho[w]
            if ma not in ra:
                ra.append(ma)
    return ra


def nut_cua_cau(dap, hoi, doan, kho: dict[str, str]) -> dict:
    """`{maNut, maNutDs}` cho một câu hỏi. Rỗng nếu không lần ra nút nào."""
    ds_tu = sorted(kho, key=len, reverse=True)
    for nguon in (dap, hoi, doan):
        ds = _tim(nguon, kho, ds_tu)
        if ds:
            return {"maNut": ds[0], "maNutDs": ds}
    return {}


def nut_cua_bai_viet(von_tu, kho: dict[str, str]) -> dict:
    """`{maNut, maNutDs}` cho một BÀI VIẾT.

    Bài viết không có "đáp án" — nó chạm cả vốn từ của bức tranh. Nên nút chính
    lấy từ ô chữ ĐẦU TIÊN tra ra được (ô xếp theo thứ tự vật trong tranh, tức thứ
    bé phải nói tới trước), còn `maNutDs` giữ tất cả.

    ⚠ Bài viết được chấm bằng AI, và điểm ấy KHÔNG phải một lượt đúng/sai sạch sẽ
    như câu trắc nghiệm. Bên gọi phải tự quyết ngưỡng nào là "đạt" rồi mới ghi —
    xem `VietBai.jsx`.
    """
    ds = []
    for o in (von_tu or []):
        ma = kho.get(str(o.get("tu", "")).lower())
        if ma and ma not in ds:
            ds.append(ma)
    return {"maNut": ds[0], "maNutDs": ds} if ds else {}
