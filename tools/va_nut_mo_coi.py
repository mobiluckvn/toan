#!/usr/bin/env python3
"""VÁ MÃ NÚT MỒ CÔI — mã bài học dùng mà đồ thị tri thức không có.

Phát hiện khi dựng bảng đối chiếu v4: phép đếm «nút dưới 4 câu» ra 73 thay vì 32
của luận văn, và chênh lệch chính là 46 mã không phải đỉnh của `do_thi.json`.

── BA HỌ, BA NGUYÊN NHÂN KHÁC NHAU ──

1 · `sp_g3_starter_1` — MỘT mã, 6 câu, và là `maNut` CHÍNH.
    Bài `DL:TA3.B00` dạy thật mẫu câu «What number is it? - It's + [Number].» và
    khai nó ngay trong bài, nhưng bản đồ tri thức chưa bao giờ có nút ấy. Lượt trả
    lời 6 câu đó mang `bktUnit: sp_g3_starter_1`, nên BKT vẫn theo dõi được, còn
    phép chẩn đoán trên đồ thị KHÔNG đặt nút ấy vào đâu — nó không có nút trước,
    không thành ứng viên gốc rễ, và lan truyền ngược dừng ngay tại đó.

    ⚠ Bản đồ đã có `sp_g3_numbers`, nhưng đó là nút CẦU (`prior_knowledge`) giữa hai
    khối lớp: ba mẫu câu lớp 4 khai «cần» nó, mà bản thân nó không có bài nào dạy.
    Đó đúng là giới hạn Bảng 3.25 tự khai — «19 nút gốc rễ không có bài dạy (các nút
    nối giữa hai khối lớp)». Nên lời giải đúng không phải trỏ 6 câu sang nút cầu, mà
    là KHAI NÚT THẬT rồi nối nút cầu xuống nó. Làm thế thì cầu có bài dạy, và danh
    sách 19 nút kia bớt một.

2 · `cum_*` (30 mã) và `them_*` (15 mã) — chỉ nằm ở `maNutDs`, không bao giờ là
    `maNut` chính. Đây là MẨU ĐIỀN Ô do bộ sinh đặt tên: `them_ten_Bill` (tên Bill),
    `them_mau_blue` (màu xanh), `cum_a_burger` (cụm «a burger»). Chúng không phải
    tri thức — bé không «thạo tên Bill».

    `maNutDs` nghĩa là «mọi nút tri thức câu này chạm tới», và mọi chỗ đọc nó đều
    coi từng mục là một nút: `vectorS` gộp mức thạo, `baiTienQuyet` tra nút trước,
    `viecTiepCuaBai` hỏi hàm chính sách. Mã không có trong đồ thị thì không bao giờ
    có mức thạo, nên:
      · `viecTiepCuaBai` của 9 bài ấy KHÔNG BAO GIỜ ra `vuotAi` — tức thẻ ôn của
        chúng không bao giờ được hoãn, dù bé đã vững hẳn;
      · `baiTienQuyet` tra vào hư không.
    Cả hai hỏng LẶNG LẼ: không màn nào đổi, không cổng nào đỏ.

    Không mã nào trong `src/` hay `functions/` đọc tiền tố `cum_`/`them_`, nên bỏ
    chúng khỏi `maNutDs` là không mất gì. Đáp án vẫn nằm nguyên ở `answerKey`.

chạy:  ~/.venv/bin/python3 tools/va_nut_mo_coi.py --xem
       ~/.venv/bin/python3 tools/va_nut_mo_coi.py --ghi
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BAN_DO = GOC / "data/ban_do_tieng_anh.json"
DO_THI = GOC / "web/public/content/tienganh/do_thi.json"

NUT_MOI = {
    "id": "sp_g3_starter_1",
    "example": "What number is it? - It's five.",
    "grammar_form": "What number is it? - It's + [Number].",
    "target_vocab_slots": ["number"],
    "grammar_metadata": {
        "tense": "present_simple",
        "sentence_type": "question",
        "formula": "What number is it? - It's {number}.",
    },
    "label": "SentencePattern",
    "type": "grammar",
    "node_kind": "sentence_pattern",
    "grade": 3,
    "source_graph": "g3",
    "unit": "u_g3_starter",
    "label_en": "What number is it? - It's five.",
    "bkt_params": {"p_l0": 0.25, "p_transit": 0.15, "p_guess": 0.2, "p_slip": 0.1},
    "cefr_level": "Pre-A1",
}

CANH_MOI = {
    "source": "sp_g3_numbers",
    "target": "sp_g3_starter_1",
    "relation": "REQUIRES",
    "properties": {
        "type": "grammar",
        "reason": "Nut cau 'biet dem so o Lop 3' duoc day bang mau cau Starter nay",
    },
    "source_graph": "g3",
}


def _la_cau(y) -> bool:
    return bool(y.get("id")) and bool(y.get("format") or y.get("answerKey"))


def _duyet(x):
    hang = [x]
    while hang:
        y = hang.pop()
        if isinstance(y, list):
            hang.extend(y)
            continue
        if not isinstance(y, dict):
            continue
        yield y
        hang.extend(v for v in y.values() if isinstance(v, (dict, list)))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true", help="ghi thật; mặc định chỉ xem")
    a = p.parse_args()

    ban_do = json.loads(BAN_DO.read_text("utf8"))
    co_nut = {n["id"] for n in ban_do["graph"]["nodes"]}

    # ── 1 · khai nút thật vào bản đồ ──────────────────────────────────────────
    them_nut = NUT_MOI["id"] not in co_nut
    co_canh = any(e["source"] == CANH_MOI["source"] and e["target"] == CANH_MOI["target"]
                  and e["relation"] == "REQUIRES" for e in ban_do["graph"]["edges"])
    print(f"① nút {NUT_MOI['id']}: {'THÊM' if them_nut else 'đã có'}"
          f" · cạnh từ {CANH_MOI['source']}: {'THÊM' if not co_canh else 'đã có'}")
    if a.ghi:
        if them_nut:
            ban_do["graph"]["nodes"].append(NUT_MOI)
        if not co_canh:
            ban_do["graph"]["edges"].append(CANH_MOI)
        if them_nut or not co_canh:
            st = ban_do.get("statistics") or {}
            st["total_nodes"] = len(ban_do["graph"]["nodes"])
            st["total_edges"] = len(ban_do["graph"]["edges"])
            ban_do["statistics"] = st
            BAN_DO.write_text(json.dumps(ban_do, ensure_ascii=False, indent=2) + "\n", "utf8")

    # ── 2 · bỏ mẩu điền ô khỏi `maNutDs` ──────────────────────────────────────
    # ⚠ So với ĐỒ THỊ ĐANG CHẠY, không so với danh sách tiền tố. Lọc theo `cum_`/
    #   `them_` là ghim chính tả: bộ sinh đặt thêm một tiền tố mới là phép vá này
    #   lặng lẽ bỏ sót, mà không gì báo.
    dt = json.loads(DO_THI.read_text("utf8"))["nut"]
    doi = []
    for f in sorted((GOC / "web/public/content").glob("ta*/*.json")):
        try:
            d = json.loads(f.read_text("utf8"))
        except json.JSONDecodeError:
            continue
        sua = 0
        for y in _duyet(d):
            if not _la_cau(y) or not isinstance(y.get("maNutDs"), list):
                continue
            chinh = y.get("maNut")
            sach = [m for m in y["maNutDs"] if m in dt or m == chinh]
            if sach != y["maNutDs"]:
                bo = [m for m in y["maNutDs"] if m not in sach]
                doi.append((f.name, y.get("id"), bo))
                sua += 1
                if a.ghi:
                    y["maNutDs"] = sach
        if sua and a.ghi:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", "utf8")

    print(f"② bỏ mẩu điền ô khỏi maNutDs: {len(doi)} câu")
    for t, i, bo in doi[:6]:
        print(f"     {t} {i}: bỏ {bo}")
    if len(doi) > 6:
        print(f"     … và {len(doi) - 6} câu nữa")

    if not a.ghi:
        print("\n(chưa ghi — thêm --ghi; nhớ chạy lại tools/xuat_do_thi_con.py sau khi ghi)")
    else:
        print("\nĐÃ GHI. Chạy tiếp: ~/.venv/bin/python3 tools/xuat_do_thi_con.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
