"""NỀN CHUNG CHO BỐN WORKER (việc V12).

Một worker = một lời dặn + một lượt gọi + ba tầng soi. Phần "+ ba tầng soi" giống
nhau ở cả bốn, nên nó nằm đây; bốn tệp worker chỉ còn giữ lời dặn, tức giữ đúng cái
phần khác nhau.

── BA TẦNG, THEO ĐÚNG THỨ TỰ NÀY ──
    1. KHUÔN      `khuon.soi_khuon` — mục có đủ trường, đúng kiểu, trong trần?
    2. HÀNG RÀO   `hang_rao.soi_bo` — mọi câu tiếng Anh nằm trong vốn bé đã học?
    3. (giám khảo LLM, ở `giam_khao.py` — KHÔNG gọi từ đây)

Tầng 1 và 2 đều là CODE, miễn phí, và tuyệt đối. Tầng 3 tốn ba lượt gọi mạng và bỏ
phiếu theo cảm giác. Nên hai tầng đầu phải chạy trước và phải cắt sạch: đem một mục
thiếu trường ra hỏi giám khảo là đốt ba lượt gọi vào một mục đã chết.

── ⚠ WORKER "TỪ MỚI" KHÔNG ĐI QUA HÀNG RÀO, VÀ ĐÓ LÀ ĐÚNG ──
Hàng rào hỏi "chữ này bé học chưa?". Với ba worker kia thì đó là câu hỏi đúng. Với
worker từ mới thì nó vô nghĩa: việc của worker ấy là ĐỀ XUẤT chữ bé CHƯA học. Soi nó
bằng hàng rào thì bác sạch, mọi lần, và xưởng không bao giờ đẻ ra được từ nào.

Nên thứ tự của `dieu_phoi` là: từ mới TRƯỚC → nới túi chữ bằng mấy từ vừa đề xuất →
rồi ba worker kia soi trên túi ĐÃ NỚI. Bốn worker không chạy song song cả bốn được,
và chỗ ấy là một phụ thuộc thật, không phải một chỗ tôi quên tối ưu.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chung  # noqa: E402
import hang_rao  # noqa: E402
import khuon  # noqa: E402


def bang_tu(tui: set[str], tu_moi: list[dict] | None = None) -> str:
    """Bảng vốn đưa vào lời dặn: chữ bé đã học, cộng mấy từ unit này vừa đề xuất."""
    ds = sorted(tui)
    if tu_moi:
        ds = sorted(set(ds) | {str(t.get("tu") or "").lower() for t in tu_moi if t.get("tu")})
    return " · ".join(x for x in ds if x)


def chay(loai: str, dan: str, *, tui: set[str], nhiet: float = 0.3,
         khoa_api: str | None = None, soi_hang_rao: bool = True) -> dict:
    """Chạy một worker. Trả `{qua, bac, tho}` — `tho` là nguyên văn mô hình trả về.

    KHÔNG ném khi mô hình trả rác: `dieu_phoi` cần biết worker nào trượt để ghi vào
    `duyet.md`, chứ dừng cả xưởng vì một worker là mất ba worker kia.
    """
    ra = {"loai": loai, "qua": [], "bac": [], "tho": None, "loi": None}
    try:
        tho = chung.goi(dan, token=chung.TOKEN[loai], nhiet=nhiet, khoa_api=khoa_api)
    except chung.LoiXuong as e:
        ra["loi"] = str(e)
        return ra
    ra["tho"] = tho

    # Mô hình được dặn trả `{"muc": [...]}`. Nhận cả vài tên khoá hay bị nhầm —
    # bác cả lượt vì một tên khoá là phí một lượt gọi, mà nội dung thì vẫn đúng.
    muc_ds = None
    for k in ("muc", loai, "ds", "items", "ket_qua"):
        if isinstance(tho.get(k), list):
            muc_ds = tho[k]
            break
    if muc_ds is None:
        ra["loi"] = f'không thấy mảng mục nào (khoá có: {", ".join(sorted(tho))})'
        return ra

    # ── TẦNG 1 · KHUÔN ──
    k = khuon.soi_khuon(loai, muc_ds)
    ra["bac"] += [{"muc": x["muc"], "ly_do": x["ly_do"], "tang": "khuon"} for x in k["bac"]]

    # ── TẦNG 2 · HÀNG RÀO VỐN TỪ ──
    if not soi_hang_rao:
        ra["qua"] = k["qua"]
        return ra
    for m in k["qua"]:
        phan = khuon.cau_tieng_anh(loai, m)
        bac: list[str] = []
        # CÂU HOÀN CHỈNH — soi đủ ba điều, gồm cả soi TRÙNG ở mức bộ.
        soi = hang_rao.soi_bo(phan["cau"], tui)
        bac += [f'"{x["cau"]}" — {"; ".join(x["ly_do"])}' for x in soi["bac"]]
        # CHỮ LẺ và PHƯƠNG ÁN — chỉ soi vốn. Không soi lành lặn (một chữ không phải
        # câu), và KHÔNG soi trùng (hai câu hỏi được phép dùng chung phương án nhiễu).
        for x in phan["tu_le"]:
            la = hang_rao.chu_la(x, tui)
            if la:
                bac.append(f'"{x}" — chữ ngoài vốn: {", ".join(sorted(set(la)))}')
        # CÔNG THỨC — soi vốn SAU KHI bỏ ô trống. Xem `khuon.cau_tieng_anh`.
        for x in phan["cong_thuc"]:
            la = hang_rao.chu_la(khuon.bo_o_trong(x), tui)
            if la:
                bac.append(f'"{x}" — chữ ngoài vốn: {", ".join(sorted(set(la)))}')
        if bac:
            ra["bac"].append({"muc": m, "tang": "hang_rao", "ly_do": bac})
        else:
            ra["qua"].append(m)
    return ra
