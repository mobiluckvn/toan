"""WORKER · KỊCH BẢN NÓI cho một unit (việc V12).

Kịch bản là thứ phòng luyện nói đi theo từng bước. Mỗi bước có câu tiếng Anh cô nói
và lời tiếng Việt cô giải thích — hai thứ, hai tiếng, và chúng phải nói về CÙNG một
việc. Chỗ hỏng đã thấy thật ở việc V7: bước kế hoạch và lời dặn nói hai từ khác nhau,
rồi mô hình chọn bừa.
"""
from __future__ import annotations

import nen_worker

LOAI = "kich_ban"


def loi_dan(*, lop: int, chu_de: str, canh: str, bang: str, mau: list[str],
            so_buoc: int) -> str:
    return "\n".join([
        f"Bạn soạn KỊCH BẢN một buổi luyện nói tiếng Anh cho bé lớp {lop} người Việt.",
        "",
        f"CHỦ ĐỀ UNIT: {chu_de}",
        *([f"BỐI CẢNH: {canh}"] if canh else []),
        "",
        "TOÀN BỘ TIẾNG ANH BÉ ĐƯỢC DÙNG — không một chữ nào ngoài bảng này:",
        bang,
        "",
        *(["MẪU CÂU CỦA UNIT:", *(f"- {x}" for x in mau), ""] if mau else []),
        f"VIỆC: soạn ĐÚNG MỘT kịch bản, và kịch bản ấy gồm {so_buoc} bước.",
        "",
        f'⚠ MẢNG "muc" CÓ ĐÚNG MỘT PHẦN TỬ. {so_buoc} bước nằm TRONG mảng "buoc" của',
        "phần tử ấy — KHÔNG phải mỗi bước một phần tử của \"muc\".",
        "",
        "LUẬT — theo đủ, không bỏ điều nào:",
        "1. MỌI chữ tiếng Anh CHỈ lấy từ bảng trên. Tuyệt đối không từ mới.",
        "2. Mỗi bước gồm:",
        '   - "cau": câu TIẾNG ANH cô nói ở bước ấy (một câu, đã điền đủ, không ô trống);',
        '   - "vi": lời TIẾNG VIỆT cô nói kèm — và nó phải nói về ĐÚNG câu ấy.',
        "3. Dễ trước, khó sau: bước đầu là bước bé làm được ngay.",
        "4. Bước cuối là bước bé tự nói một câu của mình, không nhại.",
        '5. "ten" · "muc_tieu" · "tinh_huong": tiếng Việt, KHÔNG có chữ số.',
        "6. Không câu nào còn dấu ngoặc vuông — kịch bản là câu đã điền.",
        "",
        "TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:",
        '{"muc": [{"ten": "…", "muc_tieu": "…", "tinh_huong": "…",',
        '          "buoc": [{"cau": "…", "vi": "…"}]}]}',
    ])


def soan(*, lop: int, chu_de: str, canh: str, tui: set,
         tu_moi: list[dict] | None = None, mau: list[str] | None = None,
         so_buoc: int = 6, khoa_api: str | None = None) -> dict:
    dan = loi_dan(lop=lop, chu_de=chu_de, canh=canh,
                  bang=nen_worker.bang_tu(tui, tu_moi),
                  mau=mau or [], so_buoc=so_buoc)
    return nen_worker.chay(LOAI, dan, tui=tui, nhiet=0.3, khoa_api=khoa_api)
