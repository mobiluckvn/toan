#!/usr/bin/env python3
"""CHUẨN HOÁ BẢN ĐỒ TIẾNG ANH — ba khuôn lớp 1·2·3 về MỘT hình dạng.

    python3 tools/chuan_tienganh.py --lop 1
    python3 tools/chuan_tienganh.py --lop 1 --ra data/tienganh/chuan_lop1.json

── VÌ SAO PHẢI CÓ TỆP NÀY, VÀ PHẢI CÓ NGAY TỪ ĐẦU ──

Bác đi lớp 1 → 2 → 3. Ba lớp ấy KHÔNG cùng một khuôn dữ liệu, dù nằm chung một tệp:

    trường            lớp 1              lớp 2               lớp 3
    ───────────────────────────────────────────────────────────────────────
    số hiệu unit      unit_no            unit_number         unit_number
    unit → từ         mảng `vocabulary`  KHÔNG có, chỉ cạnh  KHÔNG có, chỉ cạnh
    từ → phonics      target_phonics     phonics_focus       (không có)
    từ → loại từ      (không có)         (không có)          pos
    phonics           letter·letter_name letter → focus      sound·example_word
                      target_sound·      phonics_type        target
                      position           example_words
    nghĩa Việt        0/60  ← phải bù    56/56               185/204
    IPA               0/60  ← phải bù    56/56               184/204

Viết bộ sinh bài thẳng trên khuôn lớp 1 thì tới lớp 2 là vỡ — và vỡ vào lúc đã có
16 bài chạy thật, tức là lúc đắt nhất để sửa. Nên chuẩn hoá TRƯỚC, một lần.

Đây cũng đúng bài học của bốn quyển Toán: `chuan_lop2.py` · `chuan_lop3.py` ·
`chuan_lop4.py` là ba tệp gần giống nhau, mỗi lần thêm quyển lại chép thêm một bản.

── KHÔNG SỬA BẢN ĐỒ GỐC ──
`data/ban_do_tieng_anh.json` là nguyên liệu bên ngoài cấp. Phần thiếu nằm ở
`data/tienganh/lopN_bu.json`, tệp này ĐẮP lên chứ không ghi ngược lại.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BAN_DO = GOC / "data/ban_do_tieng_anh.json"


# ───────────────────────── đọc bản đồ ─────────────────────────

def nap():
    d = json.loads(BAN_DO.read_text("utf8"))
    nut = {n["id"]: n for n in d["graph"]["nodes"]}
    canh = defaultdict(list)          # (quan hệ, nguồn) → [đích]
    nguoc = defaultdict(list)         # (quan hệ, đích)  → [nguồn]
    for e in d["graph"]["edges"]:
        canh[(e["relation"], e["source"])].append(e)
        nguoc[(e["relation"], e["target"])].append(e)
    return nut, canh, nguoc


# ─────────── ba chỗ khuôn lệch nhau: gói lại thành ba hàm ───────────

def so_unit(u: dict) -> int:
    """`unit_no` (lớp 1) hay `unit_number` (lớp 2-3) — hỏi ở đây, đừng hỏi khắp nơi.

    Lớp 3 khai `unit_number: "starter"` — CHỮ, không phải số. Bản đầu của hàm này
    gọi thẳng `int()` nên vỡ ngay ở lớp 3, đúng cái mà bộ chuẩn hoá sinh ra để
    tránh. Unit không đánh số thì xếp LÊN ĐẦU (số 0), vì "starter" theo nghĩa đen
    là bài mở đầu — và đối chiếu số trang thì đúng: nó ở trang nhỏ nhất.
    """
    for k in ("unit_no", "unit_number", "unit_index"):
        v = u.get(k)
        if v is None:
            continue
        try:
            return int(v)
        except (TypeError, ValueError):
            return 0
    return 0


def tu_cua_unit(u: dict, nut: dict, canh: dict) -> list[dict]:
    """Lớp 1 khai mảng `vocabulary` trong node; lớp 2-3 chỉ có cạnh CONTAINS.

    Đọc CẢ HAI rồi gộp — quyển nào khai kiểu gì cũng ra đúng, và quyển khai cả hai
    kiểu (nếu sau này có) cũng không bị đếm đôi.
    """
    ra = list(u.get("vocabulary") or [])
    for e in canh[("CONTAINS", u["id"])]:
        n = nut.get(e["target"])
        if n and n.get("node_kind") == "vocabulary" and n["id"] not in ra:
            ra.append(n["id"])
    # Lớp 2-3 còn gắn ngược bằng trường `unit` trên chính node từ.
    return [i for i in ra if i in nut]


def phonics_cua_unit(u: dict, nut: dict, canh: dict) -> dict | None:
    """Ba lớp khai phonics bằng ba bộ trường khác hẳn nhau. Gộp về một."""
    ids = list(u.get("phonics") or [])
    if u.get("phonics_node_id"):
        ids.append(u["phonics_node_id"])
    for e in canh[("CONTAINS", u["id"])]:
        n = nut.get(e["target"])
        if n and n.get("node_kind") == "phonics":
            ids.append(n["id"])
    ids = [i for i in dict.fromkeys(ids) if i in nut]
    if not ids:
        return None

    p = nut[ids[0]]
    pf = u.get("pronunciation_focus") or {}
    vd = p.get("example_words") or ([p["example_word"]] if p.get("example_word") else [])
    return {
        "ma": p["id"],
        # lớp 1: letter="Bb" · lớp 2: focus="p" · lớp 3: target="..."
        "chu": p.get("letter") or p.get("focus") or p.get("target") or pf.get("phonics"),
        "ten_chu": p.get("letter_name"),
        # lớp 1: target_sound="/b/" · lớp 3: sound
        "am": p.get("target_sound") or p.get("sound") or pf.get("target_sound"),
        "loai": p.get("phonics_type") or p.get("type"),
        "tu_vi_du": list(vd) or list(pf.get("example_words") or []),
        # `position` của lớp 1 SAI ở 6 unit — xem lop1_bu.json. Nên KHÔNG chép nó
        # ra đây; vị trí âm lấy từ trường `am_o` của từng TỪ.
    }


def mau_cau_cua_unit(u: dict, nut: dict, canh: dict, nguoc: dict,
                     day: dict | None = None) -> list[dict]:
    ids = list(u.get("sentence_patterns") or [])
    for e in canh[("CONTAINS", u["id"])]:
        n = nut.get(e["target"])
        if n and n.get("node_kind") == "sentence_pattern" and n["id"] not in ids:
            ids.append(n["id"])
    ra = []
    for i in ids:
        sp = nut.get(i)
        if not sp:
            continue
        gm = sp.get("grammar_metadata") or {}
        ra.append({
            "ma": i,
            "vi_du": sp.get("example"),
            "cong_thuc": sp.get("grammar_form") or gm.get("formula"),
            "thi": gm.get("tense"),
            "kieu_cau": gm.get("sentence_type"),
            # HAS_SLOT = bảng thay thế do người soạn sách duyệt. Đây là thứ quý nhất
            # trong cả bản đồ: sinh câu từ đây thì KHÔNG BAO GIỜ ra câu sai ngữ pháp.
            "o_thay": [nut[e["target"]]["word"]
                       for e in canh[("HAS_SLOT", i)] if e["target"] in nut],
            # Phần DẠY: câu này dùng để làm gì, từng mẩu làm việc gì, khác mẫu nào.
            # Bản đồ không có — soạn tay ở lopN_bu.json, xem mục `mau_cau`.
            **{k: v for k, v in ((day or {}).get(i) or {}).items() if not k.startswith("_")},
        })
    return ra


# ───────────────────────── chuẩn hoá một lớp ─────────────────────────

def chuan(lop: int, bu: dict) -> dict:
    nut, canh, nguoc = nap()
    trong_lop = [n for n in nut.values() if str(n.get("grade")) == str(lop)]
    units = sorted([n for n in trong_lop if n.get("node_kind") == "unit"], key=so_unit)

    tu_bu = bu.get("tu", {})
    day_mau_cau = {k: v for k, v in (bu.get("mau_cau") or {}).items()
                   if not k.startswith("_")}
    # Lớp hình: emoji cho 54 từ, cộng 6 từ dùng tạm và còn nợ hình vẽ tay.
    # Gộp hai nguồn ở ĐÂY, để chỗ dùng chỉ phải hỏi một câu "hình của từ này là gì".
    hinh = {k: {"emoji": v, "ve_tay": False}
            for k, v in (bu.get("hinh") or {}).items()
            if not k.startswith("_") and isinstance(v, str)}
    for k, v in ((bu.get("hinh") or {}).get("_ve_tay") or {}).items():
        if not k.startswith("_"):
            hinh[k] = {"emoji": v["tam"], "ve": v.get("ve"),
                       "ve_tay": True, "vi_sao": v["sai_o_dau"]}
    canh_am = {}
    for k, v in (bu.get("sua_phonics") or {}).items():
        if not k.startswith("_"):
            canh_am[k] = v

    ra_unit, thieu = [], []
    for u in units:
        ds = []
        for i in tu_cua_unit(u, nut, canh):
            n, b = nut[i], tu_bu.get(i, {})
            nghia = b.get("nghia") or n.get("meaning_vi")
            ipa = b.get("ipa") or n.get("ipa")

            # TÊN RIÊNG không có nghĩa tiếng Việt để mà thiếu — "Ben" dịch ra vẫn là
            # "Ben". Không tách ra thì báo cáo thiếu bị thổi phồng và người soạn đi
            # tìm nghĩa cho một cái tên. Lớp 3 khai 19 từ "thiếu nghĩa", nhưng 10
            # trong đó là Ben · Lucy · Mai · Minh · Ms Hoa · Mr Long… — thật sự
            # thiếu chỉ 9 từ, và đó là con số đáng để đi bù.
            ten_rieng = bool(b.get("ten_rieng")) or (
                n["word"][:1].isupper() and n.get("lexical_type") != "phrase"
            )
            if not nghia and not ten_rieng:
                thieu.append(f"{i} ({n['word']}): thiếu nghĩa")
            if not ipa and not ten_rieng:
                thieu.append(f"{i} ({n['word']}): thiếu IPA")
            h = hinh.get(n["word"])
            if not h and not ten_rieng:
                thieu.append(f"{i} ({n['word']}): thiếu hình")
            ds.append({
                "ma": i,
                "tu": n["word"],
                "nghia": nghia,
                "ipa": ipa,
                # `vai` chỉ lớp 1 có (do bù tay); lớp 3 có `pos` sẵn trong bản đồ.
                "vai": b.get("vai") or ([n["pos"]] if n.get("pos") else []),
                "am_o": b.get("am_o", "dau"),
                "so_it": b.get("soit"),
                "so_nhieu": b.get("sonhieu"),
                "dang_ing": b.get("ing"),
                "go_duoc": n["word"] not in (bu.get("khong_bat_go", {}).get("tu") or []),
                "nhom_nghia": n.get("semantic_field"),
                "ten_rieng": ten_rieng or None,
                "hinh": (h or {}).get("emoji"),
                # `ve` = khoá tra vào bộ hình vẽ tay (HinhVe.jsx); có thì ưu tiên
                # hơn emoji, vì emoji của bảy từ này chỉ GẦN đúng.
                "hinh_ve": (h or {}).get("ve"),
                "hinh_no": True if ((h or {}).get("ve_tay") and not (h or {}).get("ve")) else None,
            })

        pho = phonics_cua_unit(u, nut, canh)
        if pho and pho["ma"] in canh_am:
            pho["vi_tri"] = canh_am[pho["ma"]].get("position")

        # Tên cảnh và năng lực trong bản đồ đều bằng TIẾNG ANH, mà hai thứ ấy hiện
        # cho NGƯỜI VIỆT đọc. Bản dịch nằm ở phần bù; không có thì giữ nguyên tiếng
        # Anh và `_thieu` nói ra, chứ không lẳng lặng trộn hai thứ tiếng vào một dòng.
        ub = (bu.get("unit") or {}).get(u["id"], {})
        if not ub.get("canh"):
            thieu.append(f"{u['id']}: chưa dịch tên cảnh \"{u.get('topic')}\"")

        ra_unit.append({
            "ma": u["id"],
            "so": so_unit(u),
            "canh": ub.get("canh") or u.get("topic"),
            "canh_en": u.get("topic"),
            "chu_de": u.get("theme"),
            "trang": u.get("page"),
            "nang_luc": ub.get("nang_luc") or u.get("competences") or [],
            "nang_luc_en": u.get("competences") or [],
            # Kịch bản đối đáp — bản đồ không có, soạn tay ở lopN_bu.json.
            "kich_ban_noi": (bu.get("kich_ban_noi") or {}).get(u["id"]),
            "phonics": pho,
            "tu": ds,
            "mau_cau": mau_cau_cua_unit(u, nut, canh, nguoc, day_mau_cau),
        })

    # Thang tiên quyết TRONG lớp — dùng để xếp thứ tự học và dựng màn chủ đề.
    thang = []
    ids = {n["id"] for n in trong_lop}
    for (rel, src), es in canh.items():
        if rel != "REQUIRES":
            continue
        for e in es:
            if e["source"] in ids and e["target"] in ids:
                thang.append({"can": e["target"], "truoc_khi": e["source"]})

    return {
        "_doc": "Bản đồ tiếng Anh đã CHUẨN HOÁ — một hình dạng cho mọi lớp. "
                "Sinh ra từ tools/chuan_tienganh.py, ĐỪNG sửa tay.",
        "_nguon": ["data/ban_do_tieng_anh.json", f"data/tienganh/lop{lop}_bu.json"],
        "lop": lop,
        "cefr": next((n.get("cefr_level") for n in trong_lop if n.get("cefr_level")), None),
        "unit": ra_unit,
        "thang": thang,
        "chuong": {k: v for k, v in (bu.get("chuong") or {}).items()
                   if not k.startswith("_")},
        "them": bu.get("them", {}),
        "sua_slot": {k: v for k, v in (bu.get("sua_slot") or {}).items()
                     if not k.startswith("_")},
        "_thieu": thieu,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, required=True, choices=[1, 2, 3, 4, 5])
    p.add_argument("--ra", type=Path)
    a = p.parse_args()

    tep_bu = GOC / f"data/tienganh/lop{a.lop}_bu.json"
    bu = json.loads(tep_bu.read_text("utf8")) if tep_bu.exists() else {}
    if not tep_bu.exists():
        print(f"… không có {tep_bu.relative_to(GOC)} — chạy trên bản đồ trần")

    d = chuan(a.lop, bu)
    ra = a.ra or GOC / f"data/tienganh/chuan_lop{a.lop}.json"
    ra.parent.mkdir(parents=True, exist_ok=True)
    ra.write_text(json.dumps(d, ensure_ascii=False, indent=1), "utf8")

    n_tu = sum(len(u["tu"]) for u in d["unit"])
    n_cau = sum(len(u["mau_cau"]) for u in d["unit"])
    n_o = sum(len(m["o_thay"]) for u in d["unit"] for m in u["mau_cau"])
    print(f"lớp {a.lop} ({d['cefr']}): {len(d['unit'])} unit · {n_tu} từ · "
          f"{n_cau} mẫu câu · {n_o} câu sinh được · {len(d['thang'])} mối tiên quyết")
    if d["_thieu"]:
        print(f"⚠ {len(d['_thieu'])} chỗ còn thiếu:")
        for s in d["_thieu"][:8]:
            print("   ", s)
    try:
        print(f"→ {ra.relative_to(GOC)}")
    except ValueError:      # --ra trỏ ra ngoài kho (khi chạy thử)
        print(f"→ {ra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
