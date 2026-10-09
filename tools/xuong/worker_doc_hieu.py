"""WORKER · BÀI ĐỌC HIỂU cho một unit (việc V12).

⚠ CHỖ HỎNG NẶNG NHẤT CỦA PHẦN NÀY ĐÃ BẮT ĐƯỢC THẬT: 47 câu hỏi ở hai đợt bài đọc có
nhiều hơn một đáp án đúng, hoặc có câu hỏi mà đoạn văn không trả lời được. Xem
`mot-cau-hoi-mot-dap-an-dung` và `cau-hoi-va-doan-van-lay-tu-hai-mau-cau`.

Nên lời dặn dưới đây chặt hơn ba worker kia ở hai chỗ, và cả hai đều là chỗ đã hỏng:
câu hỏi phải trả lời được TỪ ĐOẠN VĂN, và chỉ một phương án đúng.
"""
from __future__ import annotations

import nen_worker

LOAI = "doc_hieu"


def loi_dan(*, lop: int, chu_de: str, bang: str, so_cau_doan: int,
            so_cau_hoi: int) -> str:
    return "\n".join([
        f"Bạn soạn BÀI ĐỌC HIỂU tiếng Anh cho bé lớp {lop} người Việt.",
        "",
        f"CHỦ ĐỀ UNIT: {chu_de}",
        "",
        "TOÀN BỘ TIẾNG ANH BÉ ĐƯỢC DÙNG — không một chữ nào ngoài bảng này:",
        bang,
        "",
        f"VIỆC: soạn ĐÚNG MỘT bài đọc gồm {so_cau_doan} câu, và {so_cau_hoi} câu hỏi.",
        "",
        '⚠ MẢNG "muc" CÓ ĐÚNG MỘT PHẦN TỬ. Các câu của đoạn nằm trong "doan", các câu',
        'hỏi nằm trong "cau" của CÙNG phần tử ấy.',
        "",
        "LUẬT — theo đủ, không bỏ điều nào:",
        "1. MỌI chữ tiếng Anh CHỈ lấy từ bảng trên. Tuyệt đối không từ mới.",
        "2. Đoạn văn phải KỂ MỘT CHUYỆN, các câu nối nhau — không phải mấy câu rời.",
        "3. MỖI câu hỏi phải trả lời được CHỈ BẰNG ĐOẠN VĂN TRÊN. Không câu nào",
        "   đòi bé biết thêm thứ gì ngoài đoạn. Đọc lại đoạn rồi tự trả lời từng",
        "   câu trước khi ghi ra.",
        "4. ĐÚNG MỘT phương án đúng. Ba phương án nhiễu phải SAI RÕ RÀNG theo đoạn",
        "   văn — không được \"cũng có thể đúng\".",
        "5. Phương án không được trùng nhau, kể cả trùng về nghĩa.",
        '6. "hoi" là tiếng Việt (lời dẫn cho bé), "chon" và "dung" là tiếng Anh.',
        '7. "dung" phải là một trong "chon", nguyên văn.',
        "",
        "TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:",
        '{"muc": [{"doan": [{"cau": "…"}],',
        '          "cau": [{"hoi": "…", "chon": ["…","…","…","…"], "dung": "…"}]}]}',
    ])


def soan(*, lop: int, chu_de: str, tui: set, tu_moi: list[dict] | None = None,
         so_cau_doan: int = 6, so_cau_hoi: int = 4,
         khoa_api: str | None = None) -> dict:
    dan = loi_dan(lop=lop, chu_de=chu_de,
                  bang=nen_worker.bang_tu(tui, tu_moi),
                  so_cau_doan=so_cau_doan, so_cau_hoi=so_cau_hoi)
    return nen_worker.chay(LOAI, dan, tui=tui, nhiet=0.3, khoa_api=khoa_api)
