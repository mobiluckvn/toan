"""WORKER · TỪ MỚI cho một unit (việc V12).

Worker này KHÔNG đi qua hàng rào vốn từ, và đó là đúng — việc của nó là đề xuất chữ
bé CHƯA học. Lý lẽ đầy đủ ở khối chú thích đầu `nen_worker.py`.

⚠ ĐỔI LẠI, NÓ LÀ WORKER DUY NHẤT MỞ RỘNG VỐN. Mọi câu của ba worker kia đều soi trên
túi ĐÃ NỚI bằng đầu ra của worker này, nên một từ rác ở đây mở cửa cho ba worker kia
dùng nó. Vì thế lời dặn dưới đây chặt ở ba chỗ: chủ đề unit, loại từ cụ thể, và
tuyệt đối không từ ghép dài.
"""
from __future__ import annotations

import nen_worker

LOAI = "tu"


def loi_dan(*, lop: int, chu_de: str, canh: str, da_co: list[str], so_tu: int) -> str:
    return "\n".join([
        f"Bạn soạn danh sách TỪ MỚI cho một unit tiếng Anh lớp {lop} của học sinh Việt Nam.",
        "",
        f"CHỦ ĐỀ UNIT: {chu_de}",
        *([f"BỐI CẢNH: {canh}"] if canh else []),
        "",
        "NHỮNG TỪ BÉ ĐÃ HỌC (đừng đề xuất lại):",
        " · ".join(da_co) or "(chưa có)",
        "",
        f"VIỆC: đề xuất ĐÚNG {so_tu} từ mới cho unit này.",
        "",
        "LUẬT — theo đủ, không bỏ điều nào:",
        "1. Từ phải thuộc CHỦ ĐỀ unit. Không nhặt từ hay mà lạc chủ đề.",
        "2. Một từ = một chữ, hoặc một cụm ngắn quen thuộc (tối đa ba chữ).",
        "   Không cụm dài, không thành ngữ, không từ chuyên môn.",
        f"3. Hợp tuổi lớp {lop}: thứ bé nhìn thấy, làm được, hay nói tới hằng ngày.",
        "4. \"nghia\" là tiếng Việt, ngắn, KHÔNG có chữ số, và là nghĩa bé hiểu được.",
        "5. \"vai\" là loại từ: dt (danh từ) · dongtu · tinhtu · mau · so · bophan ·",
        "   thucan · noi · hoatdong. Dùng đúng mã ấy, không tự đặt mã mới.",
        "6. Dạng biến đổi chỉ ghi khi CÓ THẬT và bé cần: so_nhieu · dang_ing · dang_qk.",
        "   Không có thì để null. ĐỪNG bịa dạng không tồn tại.",
        "7. KHÔNG ghi ipa nếu không chắc — để null. Một ký hiệu phiên âm sai thì",
        "   không ai trong nhà phát hiện được.",
        "",
        "TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:",
        '{"muc": [{"tu": "…", "nghia": "…", "ipa": null, "vai": ["dt"],',
        '          "so_nhieu": null, "dang_ing": null, "dang_qk": null}]}',
    ])


def soan(*, lop: int, chu_de: str, canh: str, tui: set, so_tu: int = 8,
         khoa_api: str | None = None) -> dict:
    dan = loi_dan(lop=lop, chu_de=chu_de, canh=canh,
                  da_co=sorted(tui), so_tu=so_tu)
    # `soi_hang_rao=False`: xem khối chú thích đầu tệp.
    return nen_worker.chay(LOAI, dan, tui=tui, nhiet=0.4, khoa_api=khoa_api,
                           soi_hang_rao=False)
