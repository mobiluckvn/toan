"""TRANH LUẬN — chỉ cho phiếu 2–1, hai vòng (việc V12 · mẫu #10).

── VÌ SAO CHỈ 2–1 ──
Ba giám khảo bác hết hai thì mục ấy loại, xong. Ba thuận thì nó qua phần sàng. Chỗ
duy nhất tranh luận đổi được điều gì là 2–1: hai người thấy ổn, MỘT người thấy hỏng.

Và đó đúng là chỗ đáng tốn thêm lượt gọi, vì cả hai phía đều có thể đúng. Người bác
có thể vừa bắt được một lỗi hai người kia bỏ qua — hoặc vừa bác oan vì đọc nhầm một
chữ. Một con số "2 thuận 1 bác" không phân biệt được hai chuyện ấy; một đoạn LẬP
LUẬN thì phân biệt được, và đoạn ấy là thứ bác đọc trong `duyet.md`.

── HAI VÒNG, VÀ VÌ SAO ĐÚNG HAI ──
Vòng 1: phía bác nói rõ chỗ hỏng; phía thuận đáp lại.
Vòng 2: phía bác được đọc câu đáp rồi nói nó có giữ ý kiến không.

Vòng ba không thêm gì: đo trên mọi vòng gọi lại của kho này (V1 `SUA_CO_TOI_DA=2`,
V4 `SUA_LAI_TOI_DA=2`, V9 `VONG_TOI_DA=2`) thì vòng thứ ba chỉ nhắc lại vòng hai.
Và quan trọng hơn: tranh luận KHÔNG quyết định gì — nó chỉ viết lập luận cho người
đọc. Thêm vòng là thêm chữ bác phải đọc.

── ⚠ NÓ KHÔNG QUYẾT ĐỊNH, VÀ ĐÓ LÀ CHỐT ──
Hàm này KHÔNG trả về "qua" hay "loại". Nó trả về hai đoạn lập luận và một dòng tóm
ý. Cho nó quyết thì ta có một mô hình tự chấm điểm mình — mà toàn bộ việc V12 dựng ra
để tránh đúng chuyện ấy.

── GIỚI HẠN ĐÃ ĐO ──
Bản thiết kế đòi hai VÒNG dùng hai MODEL khác nhau, để hai bên không sai giống nhau.
Khoá này chỉ dùng được `openai/gpt-oss-120b`:

    The model `qwen/qwen3.8-27b` is blocked at the organization level.
    The model `openai/gpt-oss-20b` is blocked at the organization level.

Nên hiện hai phía khác nhau bằng NHIỆT và bằng PHÍA ĐƯỢC GIAO, không bằng model. Hàm
trả về `mot_model: True` để `duyet.md` nói thẳng điều ấy ra — bác đọc một đoạn tranh
luận mà không biết hai phía cùng một mô hình thì dễ tin nó hơn nó đáng được tin.
Đặt `GROQ_MODEL_PHU` là có hai model thật, không phải sửa mã.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chung  # noqa: E402

SO_VONG = 2
NHIET_BAC = 0.2
NHIET_THUAN = 0.4

DEM = {"goi": 0, "hong": 0, "giu_y": 0, "doi_y": 0}


def _dan_chung(lop: int, chu_de: str, loai: str, muc: dict) -> list[str]:
    return [
        f"Một mục nội dung tiếng Anh soạn cho bé lớp {lop} đang có hai ý kiến trái nhau.",
        "",
        f"CHỦ ĐỀ UNIT: {chu_de}",
        f"LOẠI MỤC: {loai}",
        "",
        "MỤC:",
        json.dumps(muc, ensure_ascii=False, indent=1),
    ]


def _goi(dan: str, nhiet: float, mo_hinh: str, khoa_api: str) -> dict:
    DEM["goi"] += 1
    try:
        return chung.goi(dan, token=chung.TOKEN["tranh_luan"], nhiet=nhiet,
                         mo_hinh=mo_hinh, khoa_api=khoa_api)
    except chung.LoiXuong as e:
        DEM["hong"] += 1
        return {"_loi": str(e)}


def tranh_luan(muc: dict, *, loai: str, lop: int, chu_de: str, ly_do_bac: str,
               khoa_api: str | None = None) -> dict:
    """Hai vòng. Trả `{vong: [...], giu_y, mot_model, loi}` — KHÔNG trả quyết định."""
    k = khoa_api or chung.khoa()
    dau = _dan_chung(lop, chu_de, loai, muc)
    vong = []

    # ── VÒNG 1 · phía THUẬN đáp lại lời bác ──
    d1 = _goi("\n".join([
        *dau,
        "",
        "MỘT NGƯỜI SOÁT ĐÃ BÁC MỤC NÀY, lý do:",
        f"    {ly_do_bac or '(không ghi lý do)'}",
        "",
        "Hai người soát khác cho qua.",
        "",
        "VIỆC CỦA BẠN: đọc lời bác trên rồi trả lời — lời bác ấy ĐÚNG hay KHÔNG,",
        "và vì sao. Trả lời bằng chứng cứ lấy từ chính mục ở trên, đừng nói chung chung.",
        "Nếu lời bác đúng thì NÓI LÀ ĐÚNG — bạn không phải bên bào chữa.",
        "",
        'TRẢ LỜI ĐÚNG MỘT KHỐI JSON: {"dap": "…"}',
        '- "dap": tiếng Việt, nhiều nhất 60 chữ.',
    ]), NHIET_THUAN, chung.MO_HINH, k)
    dap = str(d1.get("dap") or d1.get("_loi") or "").strip()
    vong.append({"phia": "thuan", "chu": dap, "loi": d1.get("_loi")})

    # ── VÒNG 2 · phía BÁC đọc câu đáp rồi nói còn giữ ý không ──
    d2 = _goi("\n".join([
        *dau,
        "",
        "BẠN LÀ NGƯỜI ĐÃ BÁC MỤC NÀY, lý do của bạn:",
        f"    {ly_do_bac or '(không ghi lý do)'}",
        "",
        "Người khác đáp lại:",
        f"    {dap or '(không đáp được)'}",
        "",
        "VIỆC CỦA BẠN: đọc câu đáp rồi nói bạn CÒN GIỮ ý kiến bác hay KHÔNG.",
        "Đổi ý là chuyện bình thường và đáng làm nếu câu đáp đúng.",
        "",
        'TRẢ LỜI ĐÚNG MỘT KHỐI JSON: {"giu_y": true, "chu": "…"}',
        '- "giu_y": true là vẫn bác, false là bỏ lời bác.',
        '- "chu": tiếng Việt, nhiều nhất 60 chữ, nói vì sao.',
    ]), NHIET_BAC, chung.MO_HINH_PHU, k)
    giu = bool(d2.get("giu_y", True)) if "_loi" not in d2 else True
    vong.append({"phia": "bac", "chu": str(d2.get("chu") or d2.get("_loi") or "").strip(),
                 "giu_y": giu, "loi": d2.get("_loi")})
    DEM["giu_y" if giu else "doi_y"] += 1

    return {
        "vong": vong,
        "giu_y": giu,
        #: True nghĩa là hai phía CÙNG một model — lập luận kém độc lập hơn bản
        #: thiết kế muốn. `duyet.md` in thẳng điều này ra cho người đọc.
        "mot_model": chung.MO_HINH_PHU == chung.MO_HINH,
        "so_vong": SO_VONG,
    }
