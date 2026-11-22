"""HÀNG RÀO VỐN TỪ BẰNG PYTHON — chạy TRƯỚC giám khảo LLM (việc V12).

── THỨ TỰ NÀY LÀ CHỐT, KHÔNG PHẢI SỞ THÍCH ──
Bản thiết kế: *"Mọi câu qua `soiCau`-tương-đương bằng Python TRƯỚC giám khảo LLM."*

Vì sao thứ tự ấy quan trọng: giám khảo là mô hình, và mô hình thì tốn tiền, chậm, và
**bỏ phiếu theo cảm giác**. Đem một câu dùng chữ ngoài vốn ra hỏi ba giám khảo thì
có khi cả ba khen nó hay — vì nó hay thật, chỉ là bé chưa học chữ ấy. Phép soi vốn
từ trả lời được câu "bé đã học chữ này chưa" một cách TUYỆT ĐỐI, nên nó phải đi
trước; để nó sau thì ba lượt gọi mạng tiêu vào một câu đã chết sẵn.

── ⚠ §7 CHỈ SAI CHỖ ──
Bản thiết kế ghi phép soi ấy "đã có trong `chuan_tienganh.py`". Không có: tệp ấy
dựng bản chuẩn chương trình, không soi câu nào. Phép soi THẬT nằm ở
`tools/sinh_kichban_noi.py` — `chu_biet()` dựng túi chữ bé được coi là đã biết,
`chu_trong()` tách chữ, `cau_lanh_lan()` soi câu sạch.

── VÀ VÌ SAO NHẬP LẠI CHỨ KHÔNG CHÉP ──
Kho này có một tiền lệ chép luật sang hai bản: `functions/src/chula.js` là bản sao
của `chuLa` bên máy con, và nó có cổng `chula_hai_ban.test.mjs` so hai bản với nhau.
Chép được vì hai bên hai ngôn ngữ (JS máy con, JS máy chủ) mà `ranh_gioi` cấm nhập
chéo.

Ở đây KHÔNG có lý do ấy: cả hai đều là Python, cùng thư mục `tools/`. Chép thành bản
thứ ba là tự nhận thêm một chỗ lệch mà không đổi lấy gì. Nên nhập lại.

⚠ `chu_biet()` đọc một BIẾN MODULE (`LOP`) để tìm `data/tienganh/chuan_lop{N}.json`.
Đặt biến của module khác từ bên ngoài là việc đáng ngại, nên nó gói kín trong đúng
một hàm dưới đây, có chú thích, và có phép kiểm trong `test_schema.py`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(GOC / "tools"))

import sinh_kichban_noi as _kb  # noqa: E402  (phải sau khi nối đường dẫn)

chu_trong = _kb.chu_trong
cau_lanh_lan = _kb.cau_lanh_lan


def tui_chu(bai: dict, lop: int) -> set[str]:
    """Túi chữ bé được coi là đã biết ở bài này.

    ⚠ ĐẶT `_kb.LOP` RỒI TRẢ LẠI. `chu_biet()` đọc biến module ấy để nạp nhóm `them`
    của bản chuẩn (tên phố, tên lớp, chỗ để đồ). Không đặt thì nó nạp nhóm của lớp 1
    cho mọi lớp, và "Class 5A" thành chữ lạ `a` — hỏng theo kiểu không ai thấy, vì
    câu vẫn gần đúng.

    Trả lại giá trị cũ ở `finally`: xưởng chạy nhiều lớp trong một tiến trình, và một
    biến module để lại giá trị của lần trước là đúng cái bẫy "sổ cũ còn trên máy".
    """
    cu = _kb.LOP
    try:
        _kb.LOP = lop
        return set(_kb.chu_biet(bai))
    finally:
        _kb.LOP = cu


def chu_la(cau: str, tui: set[str]) -> list[str]:
    """Những chữ trong câu KHÔNG nằm trong túi. Rỗng nghĩa là câu qua hàng rào."""
    return [c for c in chu_trong(cau) if c not in tui]


def soi_cau(cau: str, tui: set[str]) -> list[str]:
    """Soi MỘT câu tiếng Anh. Trả danh sách lý do bác; rỗng là qua.

    Hai tầng, và tầng thứ hai hay bị quên: chữ phải nằm trong vốn, VÀ câu phải sạch
    (`cau_lanh_lan` bác câu còn ô trống, viết hoa giữa câu, thiếu dấu cách sau dấu
    phẩy — mấy thứ bộ sinh của sách đã đẻ ra thật).
    """
    cau = str(cau or "").strip()
    if not cau:
        return ["câu rỗng"]
    ly_do = []
    if not cau_lanh_lan(cau):
        ly_do.append("câu không lành lặn (ô trống · viết hoa giữa câu · thiếu dấu cách)")
    # `chu_trong` chỉ nhặt CHỮ, nên chữ số và emoji lọt qua mà không ai soi. Bé đọc
    # "7" thì máy đọc mẫu thành "seven" — một chữ có thể ngoài vốn; emoji thì máy
    # đọc thành tên của nó, hoặc đọc im.
    if re.search(r"\d", cau):
        ly_do.append("có chữ số — viết bằng chữ để soi được vốn từ")
    if re.search(r"[^\x00-\x7F‘’“”…–—]", cau):
        ly_do.append("có ký tự lạ (emoji · ký hiệu ngoài bảng chữ)")
    la = chu_la(cau, tui)
    if la:
        ly_do.append("chữ ngoài vốn: " + ", ".join(sorted(set(la))))
    return ly_do


def soi_bo(cau_ds: list[str], tui: set[str]) -> dict:
    """Soi CẢ BỘ câu. Trả `{qua: [...], bac: [{cau, ly_do}]}`.

    ⚠ VÀ SOI TRÙNG LẶP Ở MỨC BỘ. Từng câu một thì bốn câu y hệt nhau đều hợp lệ; cả
    bộ thì là một câu hỏi lặp bốn lần. Chỗ hỏng ấy đã bắt được thật ở việc V9 (bốn
    câu phụ đạo giống nhau), nên nó phải có chốt ở đây trước khi giám khảo xem.
    """
    qua, bac = [], []
    da_co: dict[str, str] = {}
    for c in cau_ds:
        ly_do = soi_cau(c, tui)
        khoa = re.sub(r"[^a-z0-9 ]", " ", str(c or "").lower())
        khoa = re.sub(r"\s+", " ", khoa).strip()
        if khoa and khoa in da_co:
            ly_do.append(f'trùng câu đã có: "{da_co[khoa]}"')
        if ly_do:
            bac.append({"cau": c, "ly_do": ly_do})
        else:
            da_co[khoa] = c
            qua.append(c)
    return {"qua": qua, "bac": bac}
