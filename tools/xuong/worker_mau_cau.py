"""WORKER · MẪU CÂU cho một unit (việc V12).

Mẫu câu là thứ bé NHẠI, nên nó phải là câu người ta nói thật. Và nó phải có CÔNG
THỨC với ô trống đúng khuôn `[Tên]`, vì bộ sinh tra ô theo đúng hình dạng ấy —
một ô viết `(Country)` thì bộ sinh không thấy, rồi câu đi ra còn nguyên dấu ngoặc.
"""
from __future__ import annotations

import nen_worker

LOAI = "mau_cau"


def loi_dan(*, lop: int, chu_de: str, bang: str, mau_da_co: list[str], so_mau: int) -> str:
    return "\n".join([
        f"Bạn soạn MẪU CÂU cho một unit tiếng Anh lớp {lop} của học sinh Việt Nam.",
        "",
        f"CHỦ ĐỀ UNIT: {chu_de}",
        "",
        "TOÀN BỘ TIẾNG ANH BÉ ĐƯỢC DÙNG — không một chữ nào ngoài bảng này:",
        bang,
        "",
        *(["MẪU CÂU UNIT ĐÃ CÓ (đừng lặp lại):", *(f"- {x}" for x in mau_da_co), ""]
          if mau_da_co else []),
        f"VIỆC: soạn ĐÚNG {so_mau} mẫu câu cho unit này.",
        "",
        "LUẬT — theo đủ, không bỏ điều nào:",
        "1. MỌI chữ tiếng Anh CHỈ được lấy từ bảng trên. Tuyệt đối không từ mới.",
        "2. Mỗi mẫu gồm ba thứ:",
        '   - "vi_du": một câu HOÀN CHỈNH, đã điền, người ta nói thật;',
        '   - "cong_thuc": cùng câu ấy nhưng chỗ thay được viết thành [Tên];',
        '   - "dung_de": một câu tiếng Việt nói mẫu ấy DÙNG KHI NÀO.',
        "3. Ô trống viết đúng khuôn [Noun] · [Country] · [Number] · [Verb-ing] —",
        "   dấu ngoặc VUÔNG, chữ đầu hoa. Không dùng ngoặc tròn.",
        "4. Mỗi mẫu NHIỀU NHẤT MỘT ô trống. Hai ô thì phép soi câu của app không",
        "   điền nổi, và mẫu ấy mất phần luyện thay từ.",
        "5. Câu hỏi thì kèm câu đáp, ngăn bằng \" - \" (như: \"How are you? - I'm fine.\").",
        '6. "dung_de" là tiếng Việt, KHÔNG có chữ số.',
        "",
        "TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:",
        '{"muc": [{"vi_du": "…", "cong_thuc": "…", "dung_de": "…", "o_thay": []}]}',
    ])


def soan(*, lop: int, chu_de: str, tui: set, tu_moi: list[dict] | None = None,
         mau_da_co: list[str] | None = None, so_mau: int = 3,
         khoa_api: str | None = None) -> dict:
    dan = loi_dan(lop=lop, chu_de=chu_de,
                  bang=nen_worker.bang_tu(tui, tu_moi),
                  mau_da_co=mau_da_co or [], so_mau=so_mau)
    return nen_worker.chay(LOAI, dan, tui=tui, nhiet=0.3, khoa_api=khoa_api)
