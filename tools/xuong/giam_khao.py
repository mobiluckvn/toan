"""BA GIÁM KHẢO, CHẠY SONG SONG (việc V12 · mẫu #3 Parallelization + #17).

── BA CHIỀU, VÀ VÌ SAO PHẢI TÁCH RA BA LƯỢT GỌI ──
    vốn/mẫu    — câu này có đúng là thứ unit NÀY dạy, hay nó lạc sang unit khác?
    tự nhiên   — người ta có nói câu này không? hay nó đúng ngữ pháp mà không ai nói?
    hợp tuổi   — bé tuổi này hiểu được không? nội dung có phù hợp không?

Gộp ba chiều vào một lời dặn thì nhận về một con điểm, và con điểm ấy che hết: một
câu rất tự nhiên nhưng lạc unit sẽ được khen, vì mô hình thấy hai trên ba chiều tốt
rồi nó cho qua. Tách ra thì mỗi lượt chỉ có một việc, và PHIẾU BÁC nói rõ bác vì
chiều nào — mà biết chiều nào mới sửa được.

Và vì ba chiều KHÔNG phụ thuộc nhau, chúng chạy cùng lúc: cả bộ tốn đúng quãng chờ
của lượt chậm nhất.

── LUẬT ĐẾM PHIẾU ──
    ≥2 bác       → LOẠI, ghi lý do
    2–1          → `tranh_luan.py`, 2 vòng, rồi vào `duyet.md` CHO NGƯỜI quyết
    3 thuận      → qua, nhưng VẪN vào `duyet.md`

⚠ KỂ CẢ 3 THUẬN VẪN PHẢI QUA NGƯỜI. Ba giám khảo là ba lượt gọi cùng một mô hình với
ba lời dặn; chúng không độc lập theo nghĩa thống kê, và "ba thuận" không phải một
bằng chứng. Nó chỉ là một phép SÀNG để bác đọc ít hơn — không phải một phép duyệt.

── VÀ MỘT GIỚI HẠN ĐO ĐƯỢC, GHI RA ĐÂY ──
Bản thiết kế muốn vòng tranh luận dùng 2 model khác nhau. Khoá này chỉ dùng được
`openai/gpt-oss-120b`; mọi model văn bản khác bị chặn ở cấp tổ chức. Xem `chung.py`.
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chung  # noqa: E402

#: Ba chiều. Khoá là mã chiều; `TEN` là lời người đọc.
CHIEU = ("von_mau", "tu_nhien", "hop_tuoi")
TEN = {
    "von_mau": "vốn từ và mẫu câu của unit",
    "tu_nhien": "tiếng Anh có tự nhiên không",
    "hop_tuoi": "có hợp tuổi bé không",
}

#: Bác từ bao nhiêu phiếu thì LOẠI. Hằng, vì nó quyết định cái gì tới tay bác đọc.
BAC_DE_LOAI = 2

#: Nhiệt từng chiều. Chiều "vốn/mẫu" là việc đối chiếu máy móc nhất nên nhiệt thấp
#: nhất; "hợp tuổi" cần một chút cảm nhận nên cao hơn.
NHIET = {"von_mau": 0.1, "tu_nhien": 0.2, "hop_tuoi": 0.3}

DEM = {"xet": 0, "loai": 0, "tranh_luan": 0, "ba_thuan": 0, "hong": 0}


def _loi_dan(chieu: str, *, lop: int, chu_de: str, bang: str, loai: str,
             muc: dict) -> str:
    chung_dau = [
        f"Bạn là người soát nội dung tiếng Anh tiểu học, soát một mục soạn cho bé lớp {lop}.",
        "",
        f"CHỦ ĐỀ UNIT: {chu_de}",
        f"LOẠI MỤC: {loai}",
    ]
    if chieu == "von_mau":
        than = [
            "TOÀN BỘ TIẾNG ANH BÉ ĐƯỢC DÙNG:",
            bang,
            "",
            "VIỆC CỦA BẠN — CHỈ xét MỘT điều: mục này có đúng là thứ unit NÀY dạy không?",
            "Bác nếu: dùng chữ ngoài bảng · lạc sang chủ đề khác · dạy một cấu trúc",
            "unit này không dạy.",
            "KHÔNG xét câu có hay không, không xét có hợp tuổi không — hai chiều ấy",
            "có người khác soát.",
        ]
    elif chieu == "tu_nhien":
        than = [
            "VIỆC CỦA BẠN — CHỈ xét MỘT điều: người nói tiếng Anh có nói câu này không?",
            "Bác nếu: đúng ngữ pháp mà không ai nói thế · dịch word-by-word từ tiếng Việt ·",
            "cụm từ gượng · câu hỏi mà câu đáp không khớp.",
            "KHÔNG xét vốn từ, KHÔNG xét tuổi — hai chiều ấy có người khác soát.",
        ]
    else:
        than = [
            f"VIỆC CỦA BẠN — CHỈ xét MỘT điều: bé lớp {lop} (khoảng {lop + 5} tuổi) có",
            "hiểu và dùng được mục này không?",
            "Bác nếu: khái niệm quá trừu tượng · câu quá dài · nội dung không phù hợp",
            "với trẻ con · đòi kiến thức bé chưa có.",
            "KHÔNG xét vốn từ, KHÔNG xét tiếng Anh tự nhiên — hai chiều ấy có người khác soát.",
        ]
    return "\n".join([
        *chung_dau,
        "",
        *than,
        "",
        "MỤC CẦN SOÁT:",
        json.dumps(muc, ensure_ascii=False, indent=1),
        "",
        'TRẢ LỜI ĐÚNG MỘT KHỐI JSON: {"thuan": true, "ly_do": "…"}',
        '- "thuan": true là cho qua, false là bác.',
        '- "ly_do": tiếng Việt, nhiều nhất 30 chữ, nói CHỖ hỏng. Thuận thì ghi "".',
        "- Không chắc thì THUẬN: người lớn còn đọc lại sau bạn, và bác oan một mục",
        "  tốt thì không ai biết để lấy lại.",
    ])


def _mot_phieu(chieu: str, *, lop: int, chu_de: str, bang: str, loai: str,
               muc: dict, khoa_api: str) -> dict:
    dan = _loi_dan(chieu, lop=lop, chu_de=chu_de, bang=bang, loai=loai, muc=muc)
    try:
        d = chung.goi(dan, token=chung.TOKEN["giam_khao"], nhiet=NHIET[chieu],
                      khoa_api=khoa_api)
    except chung.LoiXuong as e:
        DEM["hong"] += 1
        # ⚠ LƯỢT HỎNG = KHÔNG CÓ PHIẾU (`None`) — không thuận, cũng không bác.
        # Bản cũ coi lượt hỏng là THUẬN: một lúc nhà cung cấp trả 429 là cả lô được
        # "3/3 thuận" mà `duyet.md` không ghi gì. Coi là bác thì lại xoá oan đầu ra.
        # Nên mục thiếu phiếu đi vào nhóm riêng `thieu_phieu`, và bác đọc nó.
        return {"chieu": chieu, "thuan": None, "ly_do": "", "loi": str(e)}
    thuan = doc_thuan(d.get("thuan"))
    return {
        "chieu": chieu,
        "thuan": thuan,
        "ly_do": str(d.get("ly_do") or "").strip(),
        "loi": None if thuan is not None else f"phiếu không đọc được: {d.get('thuan')!r}",
    }


def doc_thuan(v) -> bool | None:
    """Đọc phiếu NGHIÊM. `bool("false")` là True — bản cũ để chuỗi "false" thành
    thuận, và thiếu khoá cũng thành thuận. Chỉ nhận true/false thật hoặc chuỗi
    "true"/"false"; còn lại là KHÔNG CÓ PHIẾU."""
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.strip().lower() in ("true", "false"):
        return v.strip().lower() == "true"
    return None


def xet(muc: dict, *, loai: str, lop: int, chu_de: str, bang: str,
        khoa_api: str | None = None) -> dict:
    """Ba phiếu SONG SONG cho một mục. Trả `{phieu, so_bac, ket}`.

    `ket` là một trong: `loai` · `tranh_luan` · `qua`.
    """
    k = khoa_api or chung.khoa()
    DEM["xet"] += 1
    with ThreadPoolExecutor(max_workers=len(CHIEU)) as bom:
        phieu = list(bom.map(
            lambda c: _mot_phieu(c, lop=lop, chu_de=chu_de, bang=bang, loai=loai,
                                 muc=muc, khoa_api=k),
            CHIEU))
    so_bac = sum(1 for p in phieu if p["thuan"] is False)
    thieu = sum(1 for p in phieu if p["thuan"] is None)
    if so_bac >= BAC_DE_LOAI:
        DEM["loai"] += 1
        ket = "loai"
    elif thieu:
        # Thiếu phiếu thì KHÔNG được ra "qua": "qua" phải là ba phiếu thuận thật.
        DEM["thieu_phieu"] = DEM.get("thieu_phieu", 0) + 1
        ket = "thieu_phieu"
    elif so_bac == 1:
        DEM["tranh_luan"] += 1
        ket = "tranh_luan"
    else:
        DEM["ba_thuan"] += 1
        ket = "qua"
    return {"phieu": phieu, "so_bac": so_bac, "ket": ket}
