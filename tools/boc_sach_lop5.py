#!/usr/bin/env python3
"""BÓC SÁCH TIẾNG ANH LỚP 5 → bộ khung `data/tienganh/lop5_bu.json`.

    python3 tools/boc_sach_lop5.py            # in ra để xem
    python3 tools/boc_sach_lop5.py --ghi      # ghi tệp (KHÔNG đè phần đã sửa tay)

⚠ KHÔNG SỬA `data/ban_do_tieng_anh.json`. Nó là bản gốc. Tệp này chỉ ĐỌC.

── LỚP 5 KHÁC BỐN QUYỂN TRƯỚC Ở ĐÂU ──

1. **Nghĩa tiếng Việt ĐÃ CÓ DẤU.** 186/187 chữ; chữ còn lại là `far → xa`, vốn
   không có dấu thật. Lớp 4 phải gõ tay 233 nghĩa vì bản đồ khai không dấu —
   lớp 5 không cần, và tôi đã kiểm chứ không suy từ lớp 4.

2. **KHÔNG có bài Review.** 20 unit đều là bài học, đánh số 1…20 theo
   `unit_number` (bản đồ để `order` rỗng ở cả 20 nút).

3. **THÌ QUÁ KHỨ — thứ bốn quyển trước chưa từng có.** Bốn mẫu câu đòi ô
   `[past verb]`, mà `sinh_bai_tienganh.dang_can()` chỉ biết `dang_ing` và
   `so_nhieu`; gặp ô lạ nó trả về DẠNG GỐC. Không sửa thì bộ sinh lặng lẽ đẻ ra
   *"We visit the old buildings last summer."* — đúng họ
   [[bo-sinh-lui-ve-mac-dinh]]. Nên `dang_qk` khai ở đây, và `dang_can` phải
   biết đọc nó.

4. **21/40 mẫu câu có NHIỀU Ô** (lớp 4 có 15). Mẫu nhiều ô mà không khai
   `sua_slot` thì `sinh_cau` bỏ qua CẢ MẪU, im lặng.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BAN_DO = GOC / "data/ban_do_tieng_anh.json"
RA = GOC / "data/tienganh/lop5_bu.json"

# ── VAI: suy từ `semantic_field` của bản đồ ───────────────────────────────────
# Vai quyết định từ ấy ĐẶT ĐƯỢC vào ô nào, và cổng soi tranh có coi nó là VẬT
# VẼ ĐƯỢC hay không. Khai sai vai thì bộ sinh đẻ ra câu vô nghĩa mà không có gì
# báo — lớp 3 từng có "I badminton at break time." vì `badminton` khai nhầm vai.
#
# Vai MỚI của lớp 5 (bốn quyển trước chưa có) đánh dấu ★.
VAI_THEO_FIELD = {
    # nơi chốn — gom hết về `noichon`, kể cả địa danh có thật
    "places":                ["noichon"],
    "places_vietnam":        ["noichon"],
    "landmarks":             ["noichon"],
    "holiday_places":        ["noichon"],
    "outdoor_places":        ["noichon"],
    "tet_places":            ["noichon"],
    "school_places":         ["noichon"],
    "school":                ["noichon"],
    "homes":                 ["noichon"],
    # việc làm được / đang làm
    "free_time":             ["viec"],
    "job_actions":           ["viec"],
    "school_activities":     ["viec"],
    "outdoor_activities":    ["viec"],
    "trip_activities":       ["viec"],
    "holiday_activities":    ["viec"],
    "summer_activities":     ["viec"],
    "tet_activities":        ["viec"],
    "healthy_habits":        ["viec"],
    "health_advice":         ["viec"],
    "adverbs":               ["viec"],      # `cook well` là CỤM việc + cách làm
    "directions":            ["dongtu"],
    # người và nghề
    "jobs":                  ["nghe"],
    "story_characters":      ["dt"],
    # tính chất
    "opinion_adjectives":    ["tinhtu"],
    "personality":           ["tinhtu"],
    "weather":               ["thoitiet"],
    # đồ và ăn uống
    "classroom_objects":     ["dodung"],
    "clothes":               ["quanao"],
    "food":                  ["thucan"],
    "food_drinks":           ["thucan"],
    "animals":               ["convat"],
    "sports":                ["sothich"],
    "colours":               ["mau"],
    # thời gian và số
    "seasons":               ["mua"],
    "months":                ["thang"],
    "numbers":               ["so"],
    "distance":              ["so"],
    "adverbs_of_frequency":  ["tanso"],     # ★ always · often · never
    "frequency":             ["tanso"],     # ★ every day · twice a week
    "special_days":          ["sukien"],
    "tet_events":            ["sukien"],
    # còn lại
    "prepositions_of_place": ["vitri"],
    "nationalities":         ["quoctich"],  # ★ American · Japanese
    "transport":             ["phuongtien"],# ★ by bus · on foot
    "health_problems":       ["benh"],      # ★ headache · toothache
}

# ── VAI THEO TỪNG TỪ — chỗ `semantic_field` gom quá thô ──────────────────────
#
# ⚠ ĐỌC ĐOẠN NÀY TRƯỚC KHI TIN BẢNG TRÊN. Ở lớp 4 bảng field báo "233/233 suy
# được vai, 0 chỗ chịu" — con số ấy CHE MẤT khoảng hai chục chỗ gán sai, chỉ lộ
# khi in danh sách ra đọc. Lớp 5 cũng thế, sáu nhóm gom lẫn:
#
#   · `healthy_habits` gom cả VIỆC (do yoga) lẫn TÍNH TỪ (strong) lẫn NGƯỜI
#     (swimmer);
#   · `health_problems` gom cả BỆNH (headache) lẫn chữ `matter` trong câu hỏi
#     "What's the matter?" — đó là danh từ trần;
#   · `food_drinks` đổ chung ĐỒ ĂN và ĐỒ UỐNG;
#   · `story_characters` gom cả CON VẬT (ant · hare · tortoise) lẫn NGƯỜI
#     (Snow White · dwarf);
#   · `distance` gom ĐƠN VỊ ĐO (kilometre) với TÍNH TỪ (far);
#   · `holiday_activities` có `swim` là động từ trần, không phải cụm việc.
VAI_THEO_TU = {
    # healthy_habits — tách tính từ và người ra khỏi việc
    "strong": ["tinhtu"], "swimmer": ["nghe"],
    # health_problems — `matter` là danh từ trong "What's the matter?"
    "matter": ["dt"],
    # food_drinks — uống thì là `douong`
    "apple juice": ["douong"], "milk tea": ["douong"],
    # story_characters — con vật vẽ khác người
    "ant": ["convat"], "crow": ["convat"], "fox": ["convat"],
    "grasshopper": ["convat"], "hare": ["convat"], "tortoise": ["convat"],
    "dwarf": ["dt"], "Snow White": ["dt", "ten_rieng"],
    # distance
    "kilometre": ["dodac"], "far": ["tinhtu"],
    # holiday_activities
    "swim": ["viec"],
    # numbers — `hundred` đứng một mình không đếm được vật nào
    "hundred": ["so"],
}

# Tên tiếng Việt của vai MỚI. Vai cũ đã có tên ở `lop3_bu.json`/`lop4_bu.json`.
VAI_TEN_MOI = {
    "tanso":      "Mấy lần, bao lâu một lần",
    "quoctich":   "Người nước nào",
    "phuongtien": "Đi bằng gì",
    "benh":       "Chỗ nào đau",
    # `Snow White` mang HAI vai: `dt` (một nhân vật) và `ten_rieng`. Vai thứ hai
    # ba quyển trước chưa từng đặt tên vì chưa quyển nào khai nó thành vai.
    "ten_rieng":  "Tên riêng",
}

# ── DẠNG QUÁ KHỨ ────────────────────────────────────────────────────────────
#
# Bốn mẫu câu lớp 5 đòi ô `[past verb]`. Bản đồ KHÔNG khai dạng quá khứ, và
# `dang_can()` gặp ô lạ thì trả về dạng gốc — im lặng. Khai ở đây, và
# `sinh_bai_tienganh.dang_can()` đã được dạy đọc khoá `dang_qk`.
#
# ⚠ Chỉ khai những chữ THẬT SỰ rơi vào ô quá khứ. Khai thừa thì không sao, khai
# thiếu thì bộ sinh lùi về dạng gốc — nên bên `chuan_tienganh` có phép đếm, và
# từ nào thiếu dạng thì bị LOẠI KHỎI KHO chứ không điền bừa.
# ── SỐ NHIỀU ─────────────────────────────────────────────────────────────────
# Ô `[plural nouns]` của U08 đòi dạng số nhiều. `dang_can()` trả None khi thiếu,
# và cả mẫu câu bị bỏ IM LẶNG — U08 mất trắng bậc 2 vì đúng chuyện này.
SO_NHIEU = {
    "crayon": "crayons", "glue stick": "glue sticks",
    "pencil sharpener": "pencil sharpeners", "set square": "set squares",
    "blouse": "blouses", "coat": "coats", "jumper": "jumpers",
    "dolphin": "dolphins", "ant": "ants", "crow": "crows",
    "hare": "hares", "tortoise": "tortoises", "grasshopper": "grasshoppers",
}

DANG_QK = {
    "plant trees": "planted trees",
    "play games": "played games",
    "visit the old buildings": "visited the old buildings",
    "walk around the lake": "walked around the lake",
    "buy souvenirs": "bought souvenirs",
    "collect seashells": "collected seashells",
    "eat seafood": "ate seafood",
    "see some interesting places": "saw some interesting places",
    "take a boat trip around the bay": "took a boat trip around the bay",
    "walk on the beach": "walked on the beach",
    "swim": "swam",
    "take photos": "took photos",
    "go camping": "went camping",
    "join a music club": "joined a music club",
    "practise swimming": "practised swimming",
    "visit an eco-farm": "visited an eco-farm",
    "cook well": "cooked well",
    "run fast": "ran fast",
    "sing beautifully": "sang beautifully",
    "work hard": "worked hard",
    "do projects": "did projects",
    "read books": "read books",
    "solve maths problems": "solved maths problems",
    "listen to music": "listened to music",
    "play chess": "played chess",
    "watch the fish": "watched the fish",
    "dance around the campfire": "danced around the campfire",
}


# ══════════════════════════════ HÌNH ══════════════════════════════
#
# Ba bảng, ba việc khác nhau. Chỗ này quyết định bé NHÌN THẤY GÌ, nên mỗi mục
# đều đã đọc TÊN UNICODE CHÍNH THỨC rồi mới nhận — không tin cảm nhận. Cách ấy
# bắt được chín hình sai và hai chuỗi ZWJ ngay trong lượt đề xuất đầu tiên.

# ① EMOJI ĐÚNG NGHĨA — đã soi tên, nhận.
HINH = {
    "dolphin": "🐬", "ant": "🐜", "hare": "🐇", "tortoise": "🐢",
    "grasshopper": "🦗",          # CRICKET — cùng họ côn trùng nhảy, chấp nhận
    "sandwich": "🥪", "burger": "🍔", "apple juice": "🧃", "milk tea": "🧋",
    "crayon": "🖍️", "set square": "📐",
    "blouse": "👚", "coat": "🧥", "jeans": "👖",
    "funfair": "🎡", "theatre": "🎭", "tower": "🗼",
    "spring": "🌸", "autumn": "🍂", "winter": "❄️",
    "cold": "🥶", "hot": "🥵", "warm": "🌤️",
    "swimmer": "🏊", "headache": "🤕", "toothache": "🦷",
    "by bicycle": "🚲", "by bus": "🚌", "by taxi": "🚕", "on foot": "🚶",
    "fireworks show": "🎆", "flower festival": "🌷", "New Year party": "🎉",
    "Mid-Autumn Festival": "🥮", "Children's Day": "🎈", "Sports Day": "🏅",
    "Teachers' Day": "🌹", "Snow White": "👸",
    "aquarium": "🐠",             # ⚠ TROPICAL FISH — xem VE_TAY, đây chỉ là bản lùi
}

# ② PHẢI VẼ TAY — emoji sai nghĩa, trùng nghĩa với từ khác, hoặc là chuỗi ZWJ.
#
# ⚠ HAI CHUỖI ZWJ. `crow` 🐦‍⬛ là BIRD + ZWJ + BLACK LARGE SQUARE và
# `firefighter` 🧑‍🚒 là ADULT + ZWJ + FIRE ENGINE. Bộ dựng tách chuỗi rồi vẽ từng
# mảnh, nên ra "con chim đứng cạnh ô vuông đen" và "mặt trơn cạnh xe cứu hoả" —
# đúng cái đã dính ở `doctor` · `nurse` · `farmer` · `pet shop`.
VE_TAY = {
    "crow":             ("crow", "🐦\u200d⬛", "chuỗi ZWJ — vẽ ra chim + ô vuông đen"),
    "firefighter":      ("firefighter", "🧑\u200d🚒", "chuỗi ZWJ — mặt trơn + xe cứu hoả"),
    "glue stick":       ("glue_stick", "🩹", "ADHESIVE BANDAGE — cái băng dán, không phải hồ dán"),
    "pencil sharpener": ("pencil_sharpener", "✏️", "PENCIL — chính là cây bút chì, không phải cái gọt"),
    "jumper":           ("jumper", "🧶", "BALL OF YARN — cuộn len, không phải cái áo len"),
    "trousers":         ("trousers", "👖", "JEANS — TRÙNG HỆT hình của `jeans`; hai từ khác nhau phải hai hình"),
    "flat":             ("flat", "🏢", "OFFICE BUILDING — trùng hệt `building`"),
    "aquarium":         ("aquarium", "🐠", "TROPICAL FISH — con cá, không phải bể cá"),
    "cool":             ("cool", "😎", "SMILING FACE WITH SUNGLASSES — “ngầu”, không phải MÁT TRỜI"),
    "sore throat":      ("sore_throat", "😷", "FACE WITH MEDICAL MASK — cái khẩu trang, không phải đau họng"),
    "stomach ache":     ("stomach_ache", "🤢", "NAUSEATED FACE — buồn nôn, không hẳn là đau bụng"),
    "dwarf":            ("dwarf", "🧙", "MAGE — ông phù thuỷ, không phải chú lùn"),
    "writer":           ("writer", "✍️", "WRITING HAND — bàn tay, mà NGHỀ phải vẽ chân dung người"),
    "reporter":         ("reporter", "🎤", "MICROPHONE — cái micro, mà NGHỀ phải vẽ chân dung người"),
    "pink":             ("pink", "🩷", "U+1FA77 quá mới, nhiều phông chưa có — ô vuông màu vẽ tay cho chắc"),
}

# ③ CỐ Ý KHÔNG CÓ HÌNH — kèm LÝ DO.
#
# Lớp 1·2 dựng trên một câu: "bé chưa đọc được chữ nên HÌNH CHÍNH LÀ NGHĨA".
# Câu ấy đúng khi cả quyển chỉ dạy vật cụ thể. Lớp 5 thì quá nửa là TÍNH TỪ,
# TẦN SUẤT, VIỆC LÀM và ĐỊA DANH — cố tìm một emoji cho chúng chính là cách đẻ
# ra hình sai. Thà khai thẳng "không vẽ được, vì …".
KHONG_VE = {
    # tính từ và tính cách — không có hình dạng
    **{w: "tính từ — không vẽ thành một vật được" for w in (
        "active clever friendly helpful difficult easy fun useful interesting "
        "beautiful exciting fantastic peaceful strong far".split())},
    "good for group work": "cụm tính từ — không vẽ thành một vật được",
    # tần suất
    **{w: "tần suất — vẽ thành hình thì ra cái đồng hồ, không ra nghĩa" for w in (
        "always often sometimes usually rarely never".split())},
    **{w: "tần suất — xem trên" for w in (
        "every day", "once a week", "twice a week", "three times a week")},
    # số đếm
    **{w: "con số — bé ĐỌC chữ số, không nhìn hình" for w in (
        "twenty-three thirty-eight ninety-three forty hundred twenty-nine".split())},
    "one hundred and sixteen": "con số — xem trên",
    "one hundred and twenty-nine": "con số — xem trên",
    "kilometre": "đơn vị đo — 📏 là cái thước kẻ, không phải một ki-lô-mét",
    # quốc tịch
    **{w: "quốc tịch — cờ nước vẽ ra RỖNG HẲN (phông không có), đã dính ở lớp 4"
       for w in "American Australian Japanese Malaysian".split()},
    # tháng
    "November": "tháng — lớp 4 cũng để trống, bé đọc chữ",
    "December": "tháng — 🎄 là cây thông Nô-en, lệch hẳn với tháng Chạp ta",
    # vị trí và hướng
    **{w: "giới từ chỉ chỗ — vẽ riêng thì vô nghĩa, phải có vật mới thấy"
       for w in ("above", "beside", "in front of", "under")},
    **{w: "lời chỉ đường — là VIỆC PHẢI LÀM, không phải một vật"
       for w in ("go along", "go downstairs", "go past", "go upstairs")},
    # tầng nhà
    **{w: "tầng nhà — vẽ riêng một tầng thì không ai nhận ra"
       for w in ("first floor", "ground floor", "second floor", "third floor")},
    # danh từ trừu tượng
    "class": "lớp 5C — là TẬP THỂ, không phải cái phòng; 🏫 là ngôi trường",
    "matter": "trong câu “What's the matter?” — không phải một vật",
    # địa danh có thật: vẽ emoji thì ra một cái chung chung, không ra CHỖ ẤY
    **{w: "địa danh có thật — emoji chỉ ra chỗ chung chung, không ra đúng nơi này"
       for w in ("Ba Na Hills", "Bai Dinh Pagoda", "Hoan Kiem Lake",
                 "Suoi Tien Theme Park", "Dam Sen Aquarium", "Huong River",
                 "Phong Nha Cave", "Phu Quoc Island", "Dragon Bridge",
                 "Ha Noi Opera House", "Ho Chi Minh City Museum",
                 "Ngo Mon Square", "grandparents' house")},
}


def _vai_ten_cu() -> dict:
    """Tên ngắn của các vai mà ba quyển trước đã đặt."""
    ra = {}
    for l in (1, 2, 3, 4):
        f = GOC / f"data/tienganh/lop{l}_bu.json"
        if f.exists():
            ra.update(json.loads(f.read_text("utf8")).get("vai_ten") or {})
    return ra


def _ke_thua() -> tuple[dict, dict, dict]:
    """Từ nào bốn quyển trước ĐÃ KHAI hình thì lấy lại đúng khai báo ấy.

    Mỗi quyển phải tự khai hình cho MỌI từ của mình, kể cả từ quyển trước đã
    dạy — `chuan_tienganh` chỉ đọc bảng `hinh` của chính quyển ấy. Lớp 4 gõ lại
    15 mục như thế bằng tay.

    Gõ lại là mở ra hai bản sự thật rồi lệch nhau lúc nào không biết: sửa hình
    `farmer` ở lớp 3 mà quên lớp 4 thì cùng một chữ ra hai mặt, và bé không nhận
    ra đó là một thứ. Nên đọc thẳng từ bốn tệp cũ.
    """
    em, ve, kv = {}, {}, {}
    for l in (1, 2, 3, 4):
        f = GOC / f"data/tienganh/lop{l}_bu.json"
        if not f.exists():
            continue
        h = json.loads(f.read_text("utf8")).get("hinh") or {}
        for k, v in h.items():
            if k.startswith("_"):
                continue
            if isinstance(v, str):
                em[k] = v
        for k, v in (h.get("_ve_tay") or {}).items():
            if not k.startswith("_"):
                ve[k] = v
        for k, v in (h.get("_khong_ve") or {}).items():
            if not k.startswith("_"):
                kv[k] = v
    return em, ve, kv


def _viec_khong_ve(tu_theo_vai: dict) -> dict:
    """Mọi CỤM VIỆC đều không vẽ thành một vật được: `take a boat trip around the
    bay` là cả một câu chuyện, không phải cái thuyền. Khai từng chữ một thì sót,
    nên suy thẳng từ VAI — chỗ nào vai là `viec` mà chưa có hình thì khai luôn."""
    return {w: "cụm việc — cả một hành động, không vẽ thành một vật được"
            for w, vai in tu_theo_vai.items()
            if "viec" in vai and w not in HINH and w not in VE_TAY}


def nap_ban_do() -> list[dict]:
    d = json.loads(BAN_DO.read_text("utf8"))
    return [x for x in d["graph"]["nodes"] if x.get("grade") == 5]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true")
    a = p.parse_args()

    nut = nap_ban_do()
    # ⚠ XẾP THEO `unit_number`, KHÔNG theo `order`: cả 20 nút lớp 5 đều để
    # `order` rỗng. Bản lớp 4 xếp theo `order` — bê nguyên sang đây thì
    # `sorted(key=...)` vỡ vì None, hoặc tệ hơn là xếp bừa mà vẫn chạy trọn.
    hoc = sorted([x for x in nut if x["type"] == "unit"],
                 key=lambda y: y["unit_number"])
    if any("Review" in str(u.get("topic")) for u in hoc):
        raise SystemExit("✗ lớp 5 có bài Review — phải khai `bo_unit` như lớp 4")

    tv = sorted([x for x in nut if x["type"] == "vocabulary_item"],
                key=lambda y: y["id"])
    tu, theo_tu = {}, 0
    for v in tv:
        vai = VAI_THEO_TU.get(v["word"])
        if vai:
            theo_tu += 1
        else:
            vai = VAI_THEO_FIELD.get(v.get("semantic_field"))
        muc = {"vai": vai} if vai else {"vai": None, "_field": v.get("semantic_field")}
        if v["word"] in DANG_QK:
            muc["dang_qk"] = DANG_QK[v["word"]]
        if v["word"] in SO_NHIEU:
            muc["sonhieu"] = SO_NHIEU[v["word"]]
        tu[v["id"]] = muc

    chua = [k for k, m in tu.items() if not m.get("vai")]
    tu_lop5 = {v["word"] for v in tv}

    mau_cau = {}
    for g in sorted([x for x in nut if x["type"] == "grammar"], key=lambda y: y["id"]):
        mau_cau[g["id"]] = {
            "cong_thuc": g.get("grammar_form") or g.get("label_en"),
            "vi_du": g.get("example"),
            "dung_de": None,      # ← người điền
            "tinh_huong": None,   # ← người điền
        }

    khung = {
        "_doc": [
            "PHẦN BÙ SOẠN TAY — TIẾNG ANH LỚP 5.",
            "",
            f"{len(hoc)} bài học (không có Review) · {len(tu)} từ · "
            f"{len(mau_cau)} mẫu câu.",
            "",
            "Bộ khung do `tools/boc_sach_lop5.py` sinh ra từ bản đồ gốc; phần",
            "`canh` · `dung_de` · `tinh_huong` · `sua_slot` · `hinh` thì SOẠN TAY.",
            "Chạy lại bộ bóc KHÔNG đè phần đã sửa tay.",
            "",
            "⚠ Nghĩa tiếng Việt lấy thẳng bản đồ — lớp 5 khai CÓ DẤU, khác lớp 4.",
            "⚠ `dang_qk` là dạng QUÁ KHỨ, thứ bốn quyển trước không cần.",
        ],
        "_nguon": "data/ban_do_tieng_anh.json — graph.nodes, grade == 5",
        "_ngay": "21-08-2026",
        # Tên ngắn của VAI — video "nhóm nghĩa" đọc bảng này. Vai cũ lấy lại
        # đúng tên ba quyển trước đã đặt: đặt lại tên khác thì cùng một nhóm ra
        # hai cái tên ở hai quyển, và bé thấy nó là hai thứ.
        "vai_ten": {**_vai_ten_cu(), **VAI_TEN_MOI},
        "tu": tu,
        # ⚠ `chuan_tienganh` đọc bảng này bằng `isinstance(v, str)` — mục nào
        # không phải CHUỖI TRẦN thì nó bỏ qua IM LẶNG. Bản đầu tôi khai
        # `{"emoji": "🐬"}` cho gọn và cả 39 emoji rơi sạch: bộ chuẩn hoá vẫn
        # chạy trọn, vẫn ghi tệp, chỉ lặng lẽ báo "thiếu hình" cho đúng những
        # chữ tôi vừa khai.
        "hinh": {
            **{w: e for w, e in _ke_thua()[0].items() if w in tu_lop5},
            **HINH,
            "_ve_tay": {**{w: v for w, v in _ke_thua()[1].items() if w in tu_lop5},
                        **{w: {"ve": k, "tam": t, "sai_o_dau": v}
                           for w, (k, t, v) in VE_TAY.items()}},
            "_khong_ve": {**{w: v for w, v in _ke_thua()[2].items() if w in tu_lop5},
                          **KHONG_VE,
                          **_viec_khong_ve(
                              {v["word"]: (tu[v["id"]].get("vai") or []) for v in tv})},
        },
        # ⚠ KHOÁ THEO MÃ UNIT, không theo số thứ tự — `chuan_tienganh` tra bằng
        # `bu["unit"][u["id"]]`. Khoá số thì nó không tìm thấy gì, mà cũng không
        # báo: chỉ lặng lẽ để tên cảnh bằng tiếng Anh.
        "unit": {u["id"]: {"_topic": u["topic"], "_theme": u["theme"],
                           "_trang": u.get("page"), "canh": None}
                 for u in hoc},
        "mau_cau": mau_cau,
        "sua_slot": {},
        "them": {},
        "chuong": {},
        "kich_ban_noi": {},
    }

    print(f"  {len(hoc)} bài học · không có bài Review")
    print(f"  {len(tu)} từ  ({theo_tu} khai TAY đích danh, "
          f"{len(tu) - theo_tu} suy từ semantic_field, {len(chua)} chưa có vai)")
    print(f"  {len(DANG_QK)} dạng quá khứ khai tay")
    kv = {**KHONG_VE, **_viec_khong_ve(
        {v["word"]: (tu[v["id"]].get("vai") or []) for v in tv})}
    e_cu, v_cu, k_cu = _ke_thua()
    lai = [w for w in tu_lop5 if w in e_cu or w in v_cu or w in k_cu]
    print(f"  hình: {len(HINH)} emoji mới · {len(VE_TAY)} phải VẼ TAY · "
          f"{len(kv)} cố ý không có hình · {len(lai)} kế thừa từ quyển trước")
    print(f"  {len(mau_cau)} mẫu câu (dung_de · tinh_huong còn trống)")
    for k in chua[:10]:
        print(f"     ⚠ {k}  field={tu[k].get('_field')}")

    dem = {}
    for v in tv:
        dem.setdefault(v["word"], []).append(v["id"])
    trung = {w: i for w, i in dem.items() if len(i) > 1}
    if trung:
        print(f"  {len(trung)} chữ có NHIỀU NÚT (sách dạy lại ở unit sau):")
        for w, ids in sorted(trung.items()):
            print(f"     · {w:34s} {' '.join(ids)}")

    if a.ghi:
        if RA.exists():
            cu = json.loads(RA.read_text("utf8"))
            # Giữ TẤT CẢ khoá cũ; chỉ ba khoá bộ bóc làm chủ mới hợp nhất từng mục.
            # Xem [[ban-dung-lai-de-mat-ban-sua-tay]].
            LAM_CHU = ("tu", "mau_cau", "unit")
            for k, v in cu.items():
                if k in LAM_CHU and isinstance(v, dict):
                    moi = khung[k]
                    for k2, v2 in v.items():
                        if k2 in moi and isinstance(v2, dict):
                            moi[k2] = {**moi[k2],
                                       **{a2: b for a2, b in v2.items() if b is not None}}
                        elif k2 not in moi:
                            moi[k2] = v2
                elif k in ("_doc", "_nguon", "_ngay"):
                    khung[k] = v
                elif isinstance(v, dict) and isinstance(khung.get(k), dict):
                    # ⚠ NẮN LẠI KHUÔN CŨ. Phép "giữ tất cả khoá cũ" chữa được
                    # chuyện MẤT bản sửa tay, nhưng nó cũng giữ luôn bản GHI
                    # HỎNG: tôi từng khai `{"emoji": "🐬"}` thay vì chuỗi trần,
                    # sửa bộ bóc rồi chạy lại — và mục hỏng vẫn nằm đó đè lên
                    # mục đúng. Chạy lại không chữa được, phải xoá tay.
                    if k == "hinh":
                        v = {k2: (v2.get("emoji") if isinstance(v2, dict)
                                  and set(v2) == {"emoji"} else v2)
                             for k2, v2 in v.items()}
                    khung[k] = {**khung[k], **v}
                else:
                    khung[k] = v
        # ── DỌN MÃ MỒ CÔI ── "giữ tất cả" chữa được chuyện MẤT nhưng đẻ ra
        # chuyện TÍCH RÁC: mã đoán sai nằm lại cạnh mã đúng, mỗi mục nhìn riêng
        # đều hợp lệ nên không gì đỏ.
        hop_le = {u["id"] for u in hoc}
        moi_coi = [k for k in (khung.get("unit") or {})
                   if not k.startswith("_") and k not in hop_le]
        for k in moi_coi:
            khung["unit"].pop(k)
        if moi_coi:
            print(f"  ⚠ dọn {len(moi_coi)} mã unit mồ côi: {' '.join(sorted(moi_coi))}")
        tu_ok = {v["id"] for v in tv}
        moi_coi = [k for k in (khung.get("tu") or {}) if k not in tu_ok]
        for k in moi_coi:
            khung["tu"].pop(k)
        if moi_coi:
            print(f"  ⚠ dọn {len(moi_coi)} mã từ mồ côi: {' '.join(sorted(moi_coi))}")

        RA.write_text(json.dumps(khung, ensure_ascii=False, indent=1) + "\n", "utf8")
        print(f"→ {RA.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
