"""XƯỞNG SINH NỘI DUNG — phần dùng chung (việc V12).

── XƯỞNG NÀY LÀ GÌ, VÀ VÌ SAO NÓ Ở NGOÀI APP ──
Bốn worker soạn nháp nội dung cho một unit, ba giám khảo bỏ phiếu, phiếu 2–1 thì
tranh luận, rồi mọi thứ nằm trong một danh sách CHỜ NGƯỜI DUYỆT. Không dòng nào
của app gọi tới đây, và không lúc nào bé học mà xưởng chạy.

Đây là chỗ DUY NHẤT trong kho mà Python gọi mô hình ngôn ngữ. Nó ở ngoài app vì
ba lẽ, và lẽ thứ ba mới là lẽ chính:

  1. Nội dung là file tĩnh — trụ số 1 của kiến trúc. Sinh lúc chạy là phá trụ ấy.
  2. Mô hình chậm và tốn; một unit mất vài phút, bé thì chờ vài giây là bỏ đi.
  3. VÀ NÓ PHẢI QUA NGƯỜI. Câu sai ở phòng nói thì bé nghe một lần rồi thôi; câu
     sai lọt vào `public/content/` thì mọi bé học nó, mọi lần, cho tới khi có ai
     mở ra đọc. Nên xưởng KHÔNG có đường nào ghi thẳng vào nội dung — nó chỉ đẻ ra
     một bản nháp và một danh sách để bác đọc.

── GIỚI HẠN ĐÃ ĐO, GHI RA ĐÂY ĐỂ KHÔNG AI TƯỞNG ĐÃ LÀM ──
Bản thiết kế (§7 hàng V12) đòi `tranh_luan.py` dùng **2 model khác nhau**. Hỏi API
thì khoá này thấy 12 model, nhưng mọi model văn bản ngoài `openai/gpt-oss-120b` đều
trả về:

    The model `qwen/qwen3.8-27b` is blocked at the organization level.
    The model `openai/gpt-oss-20b` is blocked at the organization level.

Nên vòng tranh luận hiện chạy MỘT model, hai nhiệt, hai phía lập luận. Nó yếu hơn
bản thiết kế muốn — hai lượt cùng một model thì sai cũng sai giống nhau. `MO_HINH_PHU`
để sẵn và đọc từ biến môi trường `GROQ_MODEL_PHU`: ngày nào tổ chức mở một model
nữa thì đặt biến ấy, không phải sửa mã.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent.parent

# ── MÔ HÌNH ──
MO_HINH = "openai/gpt-oss-120b"
#: Model thứ hai cho vòng tranh luận. Xem khối chú thích đầu tệp: mọi model khác
#: đang bị chặn ở cấp tổ chức, nên mặc định nó TRÙNG model chính — và `tranh_luan`
#: nói thẳng điều đó ra trong báo cáo thay vì im lặng.
MO_HINH_PHU = os.environ.get("GROQ_MODEL_PHU", "").strip() or MO_HINH

NGHI_NGAN = "low"

#: Trần token từng việc. Rời nhau vì bốn worker dài ngắn khác nhau hẳn, và một
#: trần chung thì chỗ nào cũng phải lấy theo chỗ dài nhất.
#:
#: ⚠ KHOÁ PHẢI TRÙNG `khuon.LOAI`. Bản đầu viết `"tu_moi"` ở đây mà `khuon.LOAI`
#: dùng `"tu"`, nên lượt gọi đầu tiên vỡ với `KeyError: 'tu'` — hai danh sách tên
#: nằm hai tệp thì sớm muộn lệch. `test_schema.py` có phép kiểm canh chúng khớp,
#: vì cái lệch ấy chỉ lộ ra lúc gọi mạng thật.
TOKEN = {
    "tu": 1600,
    "mau_cau": 1400,
    "kich_ban": 2000,
    "doc_hieu": 2000,
    "giam_khao": 700,
    "tranh_luan": 900,
}

#: Đếm để còn lần ra. Xưởng KHÔNG ghi gì ngoài thư mục đầu ra của chính nó.
DEM = {"goi": 0, "hong": 0, "token_ra": 0, "boc_truot": 0}


class LoiXuong(Exception):
    """Lỗi của xưởng. Tách khỏi lỗi mạng để `dieu_phoi` biết nên dừng hay thử lại."""


# ─────────────────────────── ĐƯỜNG RA, VÀ CHỐT CỦA NÓ ───────────────────────────

#: Thư mục DUY NHẤT xưởng được ghi vào.
RA_CHO_PHEP = GOC / "data/tienganh/xuong"

#: Thư mục xưởng TUYỆT ĐỐI không được ghi vào, kể cả khi người gọi đưa đường dẫn.
CAM_GHI = (GOC / "web/public/content", GOC / "web/dist", GOC / "web/src")


def soi_duong_ra(p: str | Path) -> Path:
    """Đường ra có nằm trong chỗ cho phép không.

    ⚠ CHỐT NÀY LÀ CHỐT CỦA CẢ VIỆC V12, không phải một phép kiểm lịch sự. Ràng buộc
    của bản thiết kế: "KHÔNG ghi thẳng vào `public/content/`". Một bản nháp do mô
    hình soạn mà lọt vào đó thì mọi bé học nó, mọi lần, cho tới khi có người mở ra
    đọc — và `--ra` là một tham số dòng lệnh, tức một chỗ gõ sai được.

    Soi bằng đường dẫn ĐÃ GIẢI (`resolve`), không soi chuỗi: `data/tienganh/xuong/
    ../../../web/public/content/x.json` là một chuỗi trông rất hợp lệ.
    """
    q = Path(p)
    if not q.is_absolute():
        q = GOC / q
    q = q.resolve()
    for x in CAM_GHI:
        try:
            q.relative_to(x.resolve())
        except ValueError:
            continue
        raise LoiXuong(f"KHÔNG được ghi vào {x.relative_to(GOC)} — xưởng chỉ ghi "
                       f"vào {RA_CHO_PHEP.relative_to(GOC)}")
    try:
        q.relative_to(RA_CHO_PHEP.resolve())
    except ValueError:
        raise LoiXuong(f"đường ra phải nằm trong {RA_CHO_PHEP.relative_to(GOC)} — "
                       f"nhận được: {q}") from None
    return q


# ─────────────────────────── KHOÁ VÀ LỜI GỌI ───────────────────────────

def khoa() -> str:
    """Khoá Groq. Đọc biến môi trường trước, rồi tới tệp bí mật của functions.

    ⚠ KHÔNG in khoá ra, và không đưa nó vào bất cứ thông báo lỗi nào — thông báo
    lỗi của công cụ hay bị dán nguyên văn vào chỗ khác.
    """
    k = os.environ.get("GROQ_API_KEY", "").strip()
    if k:
        return k
    tep = GOC / "web/functions/.secret.local"
    if tep.exists():
        m = re.search(r'GROQ_API_KEY\s*=\s*"?([^"\n]+)', tep.read_text("utf8"))
        if m:
            return m.group(1).strip()
    raise LoiXuong("Chưa có khoá Groq. Đặt GROQ_API_KEY, hay ghi vào "
                   "web/functions/.secret.local")


def goi(dan: str, *, token: int, nhiet: float = 0.3, mo_hinh: str | None = None,
        khoa_api: str | None = None) -> dict:
    """Một lời gọi, trả về KHỐI JSON đã bóc. Ném `LoiXuong` nếu không bóc được.

    ⚠ `response_format` NGHIÊM NGẶT, và `reasoning_effort` thấp. Hai nút vặn này
    không phải tuỳ chọn: `gpt-oss-120b` tiêu token cho phần NGHĨ trước khi viết, và
    lời dặn của xưởng dài hơn lời dặn phòng nói nhiều. Bỏ `reasoning_effort` thì nó
    nghĩ hết token rồi trả rỗng, và Groq đem chuỗi rỗng đi soi JSON rồi trả 400 —
    đúng chỗ hỏng đã ghi ở `functions/src/luyennoi.js`.

    Dùng `urllib` chứ không thêm `requests` vào phụ thuộc: kho này không có tệp
    requirements cho `tools/`, và một công cụ offline thì không đáng đổi lấy một gói
    nữa phải cài.
    """
    goi_den = "https://api.groq.com/openai/v1/chat/completions"
    than = json.dumps({
        "model": mo_hinh or MO_HINH,
        "messages": [{"role": "system", "content": dan}],
        "temperature": nhiet,
        "max_tokens": token,
        "reasoning_effort": NGHI_NGAN,
        "response_format": {"type": "json_object"},
    }).encode("utf8")
    yeu_cau = urllib.request.Request(goi_den, data=than, headers={
        "Authorization": f"Bearer {khoa_api or khoa()}",
        "Content-Type": "application/json",
        # ⚠ PHẢI CÓ `User-Agent`, VÀ ĐÂY LÀ MỘT CHỖ HỎNG CÓ THẬT.
        # Groq nằm sau Cloudflare, và Cloudflare chặn `User-Agent` mặc định của
        # `urllib` (`Python-urllib/3.x`). Không đặt thì MỌI lượt gọi trả:
        #     403  error code: 1010
        # Không có thân lỗi, không có lời giải thích — nên nó trông y như khoá sai.
        # Mất một lúc mới lần ra, vì cùng khoá ấy `curl` chạy ngon và SDK JavaScript
        # bên `functions/` cũng chạy ngon (SDK tự đặt UA của nó). Đây là cái giá của
        # việc dùng `urllib` thay cho một thư viện HTTP, và nó đáng ghi lại hơn là
        # đáng đổi sang `requests`.
        "User-Agent": "web5-xuong-tienganh/1.0",
    })
    DEM["goi"] += 1
    try:
        with urllib.request.urlopen(yeu_cau, timeout=180) as tra:
            d = json.loads(tra.read().decode("utf8"))
    except urllib.error.HTTPError as e:
        DEM["hong"] += 1
        # Đọc thân lỗi: Groq nói rõ vì sao (khoá sai · model bị chặn · khuôn JSON),
        # và ba cái ấy ba cách chữa khác nhau. "Lỗi HTTP 400" thì không chữa được gì.
        try:
            chi_tiet = json.loads(e.read().decode("utf8")).get("error", {}).get("message", "")
        except Exception:
            chi_tiet = ""
        raise LoiXuong(f"Groq trả {e.code}: {chi_tiet or e.reason}") from None
    except Exception as e:
        DEM["hong"] += 1
        raise LoiXuong(f"Không gọi được Groq: {e}") from None

    chon = (d.get("choices") or [{}])[0]
    chu = (chon.get("message") or {}).get("content") or ""
    DEM["token_ra"] += (d.get("usage") or {}).get("completion_tokens") or 0
    if not chu.strip():
        DEM["hong"] += 1
        raise LoiXuong("mô hình trả rỗng "
                       f"(finish_reason: {chon.get('finish_reason') or 'không rõ'})")
    return boc_json(chu)


def boc_json(chu: str) -> dict:
    """Bóc khối JSON. Mô hình được dặn trả đúng một khối, nhưng ĐỪNG TIN là nó luôn
    làm đúng — kèm lời dẫn quanh khối là chuyện thường."""
    m = re.search(r"\{[\s\S]*\}", chu or "")
    if not m:
        DEM["boc_truot"] += 1
        raise LoiXuong("không thấy khối JSON nào trong câu trả lời")
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        DEM["boc_truot"] += 1
        raise LoiXuong(f"khối JSON vỡ: {e}") from None


def in_dem(dau: str = "") -> None:
    print(f"  {dau}lượt gọi {DEM['goi']} · hỏng {DEM['hong']} · "
          f"bóc trượt {DEM['boc_truot']} · token ra {DEM['token_ra']}", file=sys.stderr)
