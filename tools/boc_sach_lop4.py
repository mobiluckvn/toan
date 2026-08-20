#!/usr/bin/env python3
"""BÓC SÁCH TIẾNG ANH LỚP 4 → bộ khung `data/tienganh/lop4_bu.json`.

    python3 tools/boc_sach_lop4.py            # in ra để xem
    python3 tools/boc_sach_lop4.py --ghi      # ghi tệp (KHÔNG đè phần đã sửa tay)

── VÌ SAO SINH CHỨ KHÔNG GÕ TAY ──
Lớp 4 có 233 từ · 48 mẫu câu · 25 unit. Gõ tay là gõ 233 lần cùng một luật, và
sớm muộn lệch — sai một mã `v_g4_…` thì bản chuẩn lặng lẽ bỏ qua từ ấy.

Bản đồ gốc đã khai sẵn `semantic_field` cho từng từ, nên VAI suy được từ đó.
Việc của người là soát lại bảng `VAI_THEO_FIELD` và mấy chỗ máy chịu.

⚠ KHÔNG SỬA `data/ban_do_tieng_anh.json`. Nó là bản gốc. Tệp này chỉ ĐỌC.

⚠ `--ghi` GIỮ NGUYÊN mọi khoá đã có trong tệp cũ — chạy lại sau khi đã sửa tay
thì không mất gì. Đây là chỗ bộ dựng khác của kho này từng đè mất bản sửa tay;
xem [[ban-dung-lai-de-mat-ban-sua-tay]].
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BAN_DO = GOC / "data/ban_do_tieng_anh.json"
RA = GOC / "data/tienganh/lop4_bu.json"

# ── VAI: suy từ `semantic_field` của bản đồ ───────────────────────────────────
# Vai quyết định từ ấy ĐẶT ĐƯỢC vào ô nào của mẫu câu, và có vẽ ra tranh được
# không. Khai sai vai thì bộ sinh đẻ ra câu vô nghĩa mà không có gì báo — ví dụ
# lớp 3 từng có "I badminton at break time." vì `badminton` khai nhầm vai.
#
# Bên trái là `semantic_field` của bản đồ, bên phải là vai của kho này.
# Vai MỚI của lớp 4 (lớp 1·2·3 chưa có) đánh dấu ★.
VAI_THEO_FIELD = {
    "people":            ["dt"],
    "job":               ["nghe"],
    "workplace":         ["noichon"],
    "place":             ["noichon"],
    "city":              ["noichon"],
    "facility":          ["noichon"],
    "shop":              ["noichon"],
    "location":          ["vitri"],
    "direction":         ["vitri"],          # ★ turn left / go straight
    "direction_verb":    ["dongtu"],
    "preposition":       ["vitri"],
    "month":             ["thang"],          # ★
    "day_of_week":       ["thu"],            # ★
    "time_word":         ["thoigian"],       # ★
    "time":              ["thoigian"],       # ★
    "subject":           ["monhoc"],         # ★
    "country":           ["quocgia"],        # ★
    "weather":           ["thoitiet"],       # ★
    "weather_noun":      ["thoitiet"],       # ★
    "ability":           ["viec"],           # can + [Ability]
    "activity":          ["viec"],
    "camp_activity":     ["viec"],
    "outdoor":           ["viec"],
    "daily_routine":     ["viec"],
    "housework":         ["viec"],
    "action":            ["dongtu"],
    "verb":              ["dongtu"],
    "classroom_command": ["dongtu"],
    "appearance_adj":    ["tinhtu"],
    "description_adj":   ["tinhtu"],
    "adjective":         ["tinhtu"],
    "body_part":         ["bophan"],
    "animal":            ["convat"],
    "food":              ["thucan"],
    "drink":             ["douong"],
    "item":              ["dodac"],
    "noun":              ["dodac"],
    "money":             ["dodac"],
    "party":             ["dodac"],
    "event":             ["dt"],
    "modal":             ["dt"],
    "conjunction":       ["dt"],
    "connector":         ["dt"],
    "question_word":     ["hoi"],
}

# ── VAI THEO TỪNG TỪ — chỗ `semantic_field` gom quá thô ──────────────────────
#
# ⚠ ĐỌC KỸ ĐOẠN NÀY TRƯỚC KHI TIN BẢNG TRÊN. Bản đầu chỉ có `VAI_THEO_FIELD`, và
# nó báo "233/233 từ suy được vai — 0 chỗ chịu". Con số ấy CHE MẤT khoảng hai chục
# chỗ gán sai, chỉ lộ khi in danh sách từ ra đọc:
#
#   · field `direction` gom cả `left` (chỗ) lẫn `turn left` (việc phải làm);
#   · field `time_word` gom cả `o'clock` lẫn `fifteen`/`thirty` (là SỐ PHÚT)
#     lẫn `summer` (là MÙA) lẫn `at` (là giới từ);
#   · field `location` gọi `city` · `town` · `mountains` là "vị trí", nhưng đó là
#     NƠI CHỐN — `vitri` phải để dành cho `in` · `near` · `behind`;
#   · field `item`/`noun`/`money`/`party` đổ chung vào `dodac`, nên `birthday` ·
#     `thousand` · `dong` thành "đồ đạc trong nhà" — mà `a thousand` thì không
#     đặt lên kệ tranh được.
#
# Đây đúng cái bẫy [[nguong-phan-tram-che-lo-thung]]: cổng xanh ≠ có ai canh.
VAI_THEO_TU = {
    # direction — TÁCH đôi: chỗ nào là HƯỚNG, chỗ nào là VIỆC PHẢI LÀM
    "left": ["huong"], "right": ["huong"], "go straight": ["dongtu"],
    "stop": ["dongtu"], "turn": ["dongtu"], "turn left": ["dongtu"],
    "turn right": ["dongtu"], "turn round": ["dongtu"],
    # time_word — số phút là SỐ, mùa là MÙA, `at` là giới từ
    "fifteen": ["so"], "thirty": ["so"], "forty-five": ["so"],
    "summer": ["mua"], "at": ["vitri"],
    # location — nơi chốn, không phải vị trí
    "city": ["noichon"], "town": ["noichon"], "village": ["noichon"],
    "mountains": ["noichon"],
    # đồ đạc — tách sự kiện, tiền, quần áo
    "birthday": ["sukien"], "party": ["sukien"], "sports day": ["sukien"],
    "dong": ["tien"], "thousand": ["so"],
    "skirt": ["quanao"], "T-shirt": ["quanao"],
    # người
    "friend": ["dt"],
}

# Tên tiếng Việt của vai MỚI. Vai cũ đã có tên trong `lop3_bu.json`, chép sang.
VAI_TEN_MOI = {
    "thang":     "Tháng trong năm",
    "thu":       "Thứ trong tuần",
    "thoigian":  "Giờ giấc, lúc nào",
    "monhoc":    "Môn học",
    "quocgia":   "Nước nào",
    "thoitiet":  "Thời tiết",
    "huong":     "Bên trái, bên phải",
    "mua":       "Mùa trong năm",
    "sukien":    "Dịp, ngày hội",
    "tien":      "Tiền",
    "quanao":    "Quần áo",
}


# ── NGHĨA TIẾNG VIỆT CÓ DẤU ─────────────────────────────────────────────────
#
# ⚠ CHỖ NÀY KHÔNG BỎ ĐƯỢC. Bản đồ gốc khai nghĩa lớp 4 bằng tiếng Việt KHÔNG
# DẤU — cả 233/233 từ ("ban be" · "thang Tu" · "hieu banh mi"). Ba quyển trước
# không bị: lớp 1·2·3 nghĩa đều có dấu. Đây là thứ BÉ ĐỌC trên màn hình, nên
# phải bù, mà bù thì bù ở đây chứ KHÔNG sửa `ban_do_tieng_anh.json`.
#
# Không cổng nào bắt được chuyện này: chữ vẫn là chữ, chỉ là sai chính tả
# tiếng Việt. Chỉ đọc ra mới thấy.
NGHIA = {
    'America': 'nước Hoa Kì', 'April': 'tháng Tư',
    'August': 'tháng Tám', 'Australia': 'nước Ô-xtrây-li-a',
    'Bangkok': 'Băng Cốc', 'Britain': 'nước Anh',
    'December': 'tháng Mười Hai', 'English': 'môn Tiếng Anh',
    'English teacher': 'giáo viên Tiếng Anh', 'February': 'tháng Hai',
    'Friday': 'thứ Sáu', 'IT': 'môn Tin học',
    'January': 'tháng Giêng', 'Japan': 'nước Nhật',
    'July': 'tháng Bảy', 'June': 'tháng Sáu',
    'London': 'Luân Đôn', 'Malaysia': 'nước Ma-lay-xi-a',
    'March': 'tháng Ba', 'May': 'tháng Năm',
    'Monday': 'thứ Hai', 'November': 'tháng Mười Một',
    'October': 'tháng Mười', 'PE': 'môn Thể dục',
    'Saturday': 'thứ Bảy', 'September': 'tháng Chín',
    'Singapore': 'nước Xinh-ga-po', 'Sunday': 'Chủ Nhật',
    'Sydney': 'Xít-ni', 'T-shirt': 'áo thun',
    'Thailand': 'nước Thái Lan', 'Thursday': 'thứ Năm',
    'Tokyo': 'Tô-ki-ô', 'Tuesday': 'thứ Ba',
    'Viet Nam': 'nước Việt Nam', 'Vietnamese': 'môn Tiếng Việt',
    'Wednesday': 'thứ Tư', 'actor': 'diễn viên (nam)',
    'art': 'môn Mĩ thuật', 'at': 'vào lúc',
    'at noon': 'buổi trưa', 'bakery': 'hiệu bánh mì',
    'beach': 'bãi biển', 'because': 'bởi vì',
    'behind': 'đằng sau', 'between': 'ở giữa',
    'big': 'to, lớn', 'bird': 'con chim',
    'birthday': 'ngày sinh', 'bookshop': 'hiệu sách',
    'building': 'toà nhà', 'building a campfire': 'đốt lửa trại',
    'busy': 'bận rộn, nhộn nhịp', 'but': 'nhưng',
    'campsite': 'địa điểm cắm trại', 'can': 'có thể, biết (làm gì)',
    'chips': 'khoai tây rán', 'cinema': 'rạp chiếu phim',
    'city': 'thành phố', 'clean the floor': 'lau sàn nhà',
    'clothes shop': 'cửa hàng quần áo', 'cloudy': 'có mây, nhiều mây',
    'come in': 'vào', 'computer room': 'phòng máy tính',
    'cook': 'nấu ăn', 'cook meals': 'nấu các bữa ăn',
    'countryside': 'vùng quê', 'crocodile': 'cá sấu',
    'cycle': 'đạp xe', 'dance': 'nhảy múa',
    'dance beautifully': 'nhảy múa đẹp', 'dancing around the campfire': 'nhảy múa quanh lửa trại',
    'do housework': 'làm việc nhà', 'do the housework': 'làm việc nhà',
    'do yoga': 'tập yoga', 'doctor': 'bác sĩ',
    'dong': 'đồng (đơn vị tiền Việt Nam)', 'draw': 'vẽ',
    'email': 'gửi thư điện tử', 'eyes': 'đôi mắt',
    'face': 'khuôn mặt', 'factory': 'nhà máy',
    'farm': 'trang trại', 'farmer': 'nông dân',
    'favourite': 'yêu thích', 'fifteen': 'mười lăm',
    'food stall': 'quầy hàng thực phẩm', 'forty-five': 'bốn mươi lăm',
    'friend': 'bạn bè', 'garden': 'vườn',
    'gardener': 'người làm vườn', 'get (to)': 'đến (địa điểm)',
    'get up': 'thức dậy', 'gift shop': 'cửa hàng quà tặng',
    'giraffe': 'hươu cao cổ', 'go straight': 'đi thẳng',
    'go to bed': 'đi ngủ', 'go to school': 'đi học',
    'grapes': 'nho', 'gym': 'phòng tập thể dục',
    'hair': 'tóc', 'hand': 'bàn tay',
    'have breakfast': 'ăn sáng', 'help with the cooking': 'giúp việc nấu ăn',
    'hippo': 'hà mã', 'history and geography': 'môn Lịch sử và Địa lí',
    'hospital': 'bệnh viện', 'in': 'trong, ở (tên đường/phố)',
    'in the afternoon': 'buổi chiều', 'in the evening': 'buổi tối',
    'in the morning': 'buổi sáng', 'jam': 'mứt',
    'juice': 'nước ép', 'jump': 'nhảy',
    'kick': 'đá (bóng)', 'last': 'trước, lần trước',
    'left': 'bên trái', 'lemonade': 'nước chanh',
    'like': 'thích', 'lion': 'sư tử',
    'listen to music': 'nghe nhạc', 'live': 'sống, sinh sống',
    'long': 'dài', 'maths': 'môn Toán',
    'maths teacher': 'giáo viên Toán', 'mountains': 'vùng núi',
    'music': 'môn Âm nhạc', 'near': 'ở gần',
    'noisy': 'ồn ào', 'nose': 'mũi',
    'nurse': 'y tá, điều dưỡng viên', 'nursing home': 'viện điều dưỡng',
    "o'clock": 'giờ (giờ chẵn)', 'office worker': 'nhân viên văn phòng',
    'open your books': 'mở sách ra', 'opposite': 'đối diện',
    'painter': 'hoạ sĩ', 'party': 'buổi tiệc',
    'peacock': 'con công', 'pen': 'bút',
    'pet shop': 'cửa hàng thú cưng', 'play badminton': 'chơi cầu lông',
    'play football': 'chơi bóng đá', 'play tennis': 'chơi quần vợt',
    'play the guitar': 'chơi ghi ta', 'play the piano': 'chơi piano',
    'playground': 'sân chơi', 'playing card games': 'chơi bài',
    'playing tug of war': 'chơi kéo co', 'policeman': 'cảnh sát (nam)',
    'pupil': 'học sinh', 'putting up a tent': 'dựng lều',
    'quiet': 'yên tĩnh', 'rainy': 'có mưa',
    'read aloud': 'đọc to', 'read books': 'đọc sách',
    'ride a bike': 'đạp xe', 'ride a horse': 'cưỡi ngựa',
    'right': 'bên phải', 'road': 'con đường, đường phố',
    'road sign': 'biển chỉ đường', 'roar loudly': 'gầm vang',
    'roller skate': 'trượt pa-tanh', 'round': 'tròn',
    'run quickly': 'chạy nhanh', 'say goodbye': 'chào tạm biệt',
    'school': 'trường học', 'school bag': 'cặp sách',
    'school garden': 'vườn trường', 'science': 'môn Khoa học',
    'shopping centre': 'trung tâm mua sắm', 'short': 'thấp, ngắn',
    'sing': 'hát', 'sing merrily': 'hót vui vẻ',
    'singer': 'ca sĩ', 'singing songs': 'hát',
    'sit down': 'ngồi xuống', 'skip': 'nhảy dây',
    'skirt': 'váy', 'slim': 'mảnh mai',
    'sports centre': 'trung tâm thể thao', 'sports day': 'ngày hội thể thao',
    'sports shop': 'cửa hàng thể thao', 'stand up': 'đứng lên',
    'stay at home': 'ở nhà', 'stop': 'dừng lại',
    'street': 'phố, đường phố', 'study at school': 'học ở trường',
    'summer': 'mùa hè', 'sunny': 'có nắng',
    'supermarket': 'siêu thị', 'swim': 'bơi',
    'swimming pool': 'bể bơi', 'taking a photo': 'chụp ảnh',
    'tall': 'cao', 'teacher': 'giáo viên',
    'telling a story': 'kể chuyện', 'tent': 'lều (ở nơi cắm trại)',
    'thirty': 'ba mươi', 'thousand': 'nghìn',
    'today': 'hôm nay', 'town': 'thị trấn',
    'turn': 'rẽ', 'turn left': 'rẽ trái',
    'turn right': 'rẽ phải', 'turn round': 'quay lại, đổi hướng ngược lại',
    'village': 'ngôi làng', 'visit': 'thăm',
    'wash the clothes': 'giặt quần áo', 'wash the dishes': 'rửa bát đĩa',
    'watch TV': 'xem ti vi', 'watch films': 'xem phim',
    'watch television': 'xem truyền hình', 'water': 'nước',
    'water park': 'công viên nước', 'weather': 'thời tiết',
    'weekend': 'cuối tuần', 'why': 'tại sao',
    'windy': 'có gió', 'worker': 'công nhân',
    'write': 'viết', 'yesterday': 'hôm qua',
    'zoo': 'vườn thú',
}


def nap_ban_do() -> list[dict]:
    d = json.loads(BAN_DO.read_text("utf8"))
    return [x for x in d["graph"]["nodes"] if x.get("grade") == 4]


def so_unit(ma: str, thu_tu: dict) -> int | None:
    """`u_g4_starter` → 0 · `u_g4_1` → 1. Tra theo `order` của bản đồ, KHÔNG suy
    từ chữ số trong mã: bản đồ có cả unit Review, và số thứ tự của chúng chen vào
    giữa. Xem `_bo_review` dưới."""
    return thu_tu.get(ma)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true")
    a = p.parse_args()

    nut = nap_ban_do()
    units = sorted([x for x in nut if x["type"] == "unit"], key=lambda y: y["order"])

    # ── UNIT: bỏ 4 bài Review, đánh số lại 0…20 ──
    # Bản đồ khai 25 unit, trong đó 4 là "Review N & Extension" — đó là ÔN TẬP
    # CHƯƠNG, không phải bài học. Lớp 3 cũng thế: 21 bài học + ôn tập riêng.
    hoc = [u for u in units if "Review" not in u["topic"]]
    thu_tu = {u["id"]: i for i, u in enumerate(hoc)}
    review = [u for u in units if "Review" in u["topic"]]

    tu, theo_tu = {}, 0
    tv = sorted([x for x in nut if x["type"] == "vocabulary_item"], key=lambda y: y["id"])
    for v in tv:
        f = v.get("semantic_field")
        vai = VAI_THEO_TU.get(v["word"])
        if vai:
            theo_tu += 1
        else:
            vai = VAI_THEO_FIELD.get(f)
        muc = {"vai": vai} if vai else {"vai": None, "_field": f}
        if v["word"] in NGHIA:
            muc["nghia"] = NGHIA[v["word"]]
        tu[v["id"]] = muc

    chua = [k for k, v in tu.items() if not v.get("vai")]
    khong_nghia = [x["word"] for x in tv if x["word"] not in NGHIA]

    # ── TỪ TRÙNG: một chữ, nhiều nút ──
    # `campsite` có BA nút (unit 10 · 17 · 20), `big` có hai nút hai field khác
    # nhau. Không phải lỗi của bản đồ — sách dạy lại — nhưng bộ sinh phải biết,
    # nếu không cùng một chữ ra hai vai khác nhau tuỳ nút nào đọc trước.
    dem = {}
    for v in tv:
        dem.setdefault(v["word"], []).append(v["id"])
    trung = {w: ids for w, ids in dem.items() if len(ids) > 1}

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
            "PHẦN BÙ SOẠN TAY — TIẾNG ANH LỚP 4.",
            "",
            f"{len(hoc)} bài học + {len(review)} bài ôn tập · "
            f"{len(tu)} từ · {len(mau_cau)} mẫu câu.",
            "",
            "Bộ khung do `tools/boc_sach_lop4.py` sinh ra từ bản đồ gốc; phần",
            "`dung_de` · `tinh_huong` · `phan` · `hinh` · `canh` thì SOẠN TAY.",
            "Chạy lại bộ bóc KHÔNG đè phần đã sửa tay.",
        ],
        "_nguon": "data/ban_do_tieng_anh.json — graph.nodes, grade == 4",
        "_ngay": "20-08-2026",
        "vai_ten": VAI_TEN_MOI,
        "tu": tu,
        "hinh": {},
        # ⚠ KHOÁ THEO MÃ UNIT, không theo số thứ tự. `chuan_tienganh` tra phần bù
        # bằng `bu["unit"][u["id"]]`, nên khoá số thì nó KHÔNG TÌM THẤY GÌ — mà
        # cũng không báo, chỉ lặng lẽ để tên cảnh bằng tiếng Anh. Bản đầu tôi khai
        # số, và phép dọn mã mồ côi ở cuối tệp này xoá sạch chính thứ nó vừa sinh.
        "unit": {u["id"]: {"_topic": u["topic"], "_theme": u["theme"],
                           "_trang": u.get("page"), "canh": None}
                 for u in hoc},
        "mau_cau": mau_cau,
        "sua_slot": {},
        "them": {},
        "chuong": {},
        "kich_ban_noi": {},
    }

    print(f"  {len(hoc)} bài học · {len(review)} bài ôn tập")
    print(f"  {len(tu)} từ  ({theo_tu} từ khai TAY đích danh, "
          f"{len(tu) - theo_tu} suy từ semantic_field, {len(chua)} chưa có vai)")
    print(f"  {len(NGHIA)} nghĩa tiếng Việt CÓ DẤU bù vào "
          f"({len(set(khong_nghia))} chữ chưa có)")
    if khong_nghia:
        print(f"     ⚠ {' · '.join(sorted(set(khong_nghia)))}")
    print(f"  {len(mau_cau)} mẫu câu (dung_de · tinh_huong còn trống)")
    for k in chua[:10]:
        print(f"     ⚠ {k}  field={tu[k].get('_field')}")
    if trung:
        print(f"  {len(trung)} chữ có NHIỀU NÚT (sách dạy lại ở unit sau):")
        for w, ids in sorted(trung.items()):
            print(f"     · {w:12s} {' '.join(ids)}")

    if a.ghi:
        if RA.exists():
            cu = json.loads(RA.read_text("utf8"))
            # ── GIỮ NGUYÊN MỌI THỨ NGƯỜI ĐÃ SỬA ──
            #
            # ⚠ Bản đầu liệt kê ĐÍCH DANH mấy khoá cần giữ ("hinh", "sua_slot", …).
            # Danh sách ấy lỗi thời ngay lần sau: tôi thêm khoá `bo_unit` bằng tay,
            # chạy lại bộ bóc, và nó XOÁ MẤT — trong khi docstring của chính tệp
            # này vẫn hứa "không mất gì". Nay làm ngược lại: giữ TẤT CẢ khoá cũ,
            # chỉ những khoá bộ bóc thật sự làm chủ mới hợp nhất theo từng mục.
            LAM_CHU = ("tu", "mau_cau", "unit")
            for k, v in cu.items():
                if k in LAM_CHU and isinstance(v, dict):
                    moi = khung[k]
                    for k2, v2 in v.items():
                        if k2 in moi and isinstance(v2, dict):
                            # người ghi đè máy, nhưng `null` của người thì không
                            # xoá mất giá trị máy vừa suy ra
                            moi[k2] = {**moi[k2],
                                       **{a2: b for a2, b in v2.items() if b is not None}}
                        elif k2 not in moi:
                            moi[k2] = v2
                elif k in ("_doc", "_nguon", "_ngay"):
                    khung[k] = v          # người viết lại lời dẫn thì giữ
                elif isinstance(v, dict) and isinstance(khung.get(k), dict):
                    khung[k] = {**khung[k], **v}
                else:
                    khung[k] = v
        # ── DỌN MÃ MỒ CÔI ──
        # "Giữ tất cả" chữa được chuyện MẤT, nhưng đẻ ra chuyện TÍCH RÁC: tôi khai
        # 21 tên cảnh bằng mã ĐOÁN SAI, sửa lại bằng mã đúng, chạy lại bộ bóc — và
        # nó giữ cả hai, thành 42 mục, trong đó 21 mục gán tên cảnh cho nhầm unit.
        # Không có gì đỏ, vì mỗi mục nhìn riêng đều hợp lệ.
        hop_le = {u["id"] for u in units} | {u["id"] for u in review}
        for kho, ten in ((khung.get("unit") or {}), "unit"), \
                        ((khung.get("bo_unit") or {}), "bo_unit"):
            if ten == "bo_unit":
                continue
            moi_coi = [k for k in kho if not k.startswith("_") and k not in hop_le]
            for k in moi_coi:
                kho.pop(k)
            if moi_coi:
                print(f"  ⚠ dọn {len(moi_coi)} mã mồ côi trong `{ten}`: "
                      f"{' '.join(sorted(moi_coi))}")
        tu_hop_le = {v["id"] for v in tv}
        moi_coi = [k for k in (khung.get("tu") or {}) if k not in tu_hop_le]
        for k in moi_coi:
            khung["tu"].pop(k)
        if moi_coi:
            print(f"  ⚠ dọn {len(moi_coi)} mã từ mồ côi: {' '.join(sorted(moi_coi))}")

        RA.write_text(json.dumps(khung, ensure_ascii=False, indent=1) + "\n", "utf8")
        print(f"→ {RA.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
