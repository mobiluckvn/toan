#!/usr/bin/env python3
"""SINH ÂM cho môn Tiếng Anh — Kokoro (Anh) + Kokoro-Vietnamese (Việt).

    python tools/tts/sinh_am.py --vao <danh_sach.json> --ra <thư_mục> --so <sổ_tra.json>
    python tools/tts/sinh_am.py --nghe-thu                # 10 clip mẫu để nghe trước

Đầu vào là một danh sách dòng chữ:

    [ { "id": "tu_dog", "chu": "dog",        "tieng": "en" },
      { "id": "lenh_01", "chu": "Con nghe rồi bấm vào hình đúng nhé.", "tieng": "vi" } ]

Đầu ra: mp3 trong thư mục `--ra`, cộng một SỔ TRA ghi mỗi clip do model nào sinh,
giọng nào, và sha256 của chữ. Sáu tháng nữa sửa một câu, sổ nói cho biết phải chạy
lại bằng gì — không có sổ thì phải đoán.

── HAI LUẬT CỨNG ──

1. MỖI DÒNG CHỈ MỘT THỨ TIẾNG.
   Kokoro-VI chỉ đọc tiếng Việt, Kokoro-82M chỉ đọc tiếng Anh. Dòng lẫn hai thứ
   tiếng thì model nào đọc cũng sai: "Con bấm vào hình con dog nhé" → Kokoro-VI
   đọc "dog" theo vần Việt thành /dóc/. Tệp này TỪ CHỐI dòng lẫn tiếng chứ không
   đọc bừa — vì đọc bừa thì ra 520 clip hỏng mà không ai biết cho tới lúc bé nghe.
   Dòng nào cần cả hai thì tách thành nhiều mục rồi nối bằng `noi_am.py`.

2. GIỌNG TIẾNG ANH PHẢI LÀ ANH-ANH.
   Bản đồ tri thức khai IPA theo chuẩn Anh-Anh: /ɒ/ (dog), /ɑː/ (car), /eə/ (hair).
   Đọc bằng giọng Anh-Mỹ thì bé nghe /dɔːɡ/, /kɑːr/ — LỆCH với phiên âm đang hiện
   ngay trên màn hình. Nên lang_code='b' và giọng bf_*/bm_*, không phải 'a'.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

O = Path(__file__).resolve().parent
MAU = 24000  # cả hai model đều ra 24 kHz — trùng nhau nên ghép không lệch

# Giọng mặc định. Đổi ở đây, đừng rải khắp nơi.
GIONG_EN = "bf_emma"      # nữ, Anh-Anh — xem luật 2 ở đầu tệp
GIONG_VI = "diem_trinh"   # nữ, một trong 13 giọng của bản cộng đồng

# ─────────────────────────── soát đầu vào ───────────────────────────

# Chữ Việt có dấu — dấu hiệu chắc chắn nhất của một dòng tiếng Việt.
CO_DAU = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
    r"ùúủũụưừứửữựỳýỷỹỵđ]", re.IGNORECASE)

# Những chữ Việt KHÔNG dấu hay lọt vào câu tiếng Anh mà mắt thường bỏ qua.
VIET_KHONG_DAU = {
    "con", "cua", "cho", "va", "la", "co", "khong", "nhe", "hay", "bam",
    "nghe", "nhin", "chon", "dung", "sai", "roi", "moi", "hinh", "tu", "cau",
}


def soat_dong(m: dict) -> str | None:
    """Trả về lời báo lỗi, hoặc None nếu dòng dùng được."""
    chu, tieng = str(m.get("chu", "")).strip(), m.get("tieng")
    if not chu:
        return "chữ rỗng"
    if tieng not in ("en", "vi"):
        return f"tiếng phải là 'en' hoặc 'vi', đang là {tieng!r}"

    if tieng == "en":
        if CO_DAU.search(chu):
            return f"dòng khai 'en' mà có chữ Việt CÓ DẤU: {chu!r}"
        tu = re.findall(r"[A-Za-z]+", chu.lower())
        lot = sorted(set(tu) & VIET_KHONG_DAU)
        # "can" là từ tiếng Anh thật (U3) — chỉ báo khi có TỪ HAI TỪ TRỞ LÊN lọt vào,
        # một từ trùng nhau là chuyện thường, hai từ thì đúng là câu tiếng Việt.
        if len(lot) >= 2:
            return f"dòng khai 'en' mà nhiều chữ Việt không dấu ({', '.join(lot)}): {chu!r}"
    else:
        # Tiếng Việt mà KHÔNG có dấu nào, lại toàn chữ ASCII → gần như chắc là
        # tiếng Anh khai nhầm. Câu Việt thật hiếm khi dài mà không có dấu nào.
        if not CO_DAU.search(chu) and len(chu.split()) >= 3:
            return f"dòng khai 'vi' mà không có chữ nào có dấu: {chu!r}"
    return None


# ─────────────────────────── hai bộ đọc ───────────────────────────

class DocAnh:
    """Kokoro-82M, lang_code='b' (Anh-Anh)."""

    def __init__(self, giong: str = GIONG_EN):
        from kokoro import KPipeline
        self.giong = giong
        self.pipe = KPipeline(lang_code="b")

    def __call__(self, chu: str, toc_do: float = 1.0):
        import numpy as np
        khuc = [a for _, _, a in self.pipe(chu, voice=self.giong, speed=toc_do)]
        if not khuc:
            raise RuntimeError(f"Kokoro không ra tiếng cho: {chu!r}")
        return np.concatenate(khuc) if len(khuc) > 1 else khuc[0]


class DocViet:
    """Kokoro-Vietnamese (bản cộng đồng), G2P bằng vig2p."""

    def __init__(self, giong: str = GIONG_VI):
        from kokoro_vietnamese import KokoroVietnamese
        self.giong = giong
        # device="cpu": cả hai model chỉ 82 M tham số, máy này không có GPU NVIDIA.
        self.tts = KokoroVietnamese(device="cpu", voice=giong)

    def __call__(self, chu: str, toc_do: float = 1.0):
        am, _ = self.tts.synthesize(chu, speed=toc_do)
        return am


# ─────────────────────────── ghi tệp ───────────────────────────

def ghi_mp3(am, dich: Path) -> None:
    """WAV tạm → mp3 64 kbps mono. ffmpeg đã có sẵn trên máy."""
    import soundfile as sf
    tam = dich.with_suffix(".wav")
    sf.write(tam, am, MAU)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(tam),
         "-ac", "1", "-b:a", "64k", str(dich)],
        check=True,
    )
    tam.unlink()


def bam(chu: str) -> str:
    """Vân tay của CHỮ — sửa chữ thì vân tay đổi, biết ngay clip nào phải sinh lại."""
    return hashlib.sha256(unicodedata.normalize("NFC", chu).encode()).hexdigest()[:16]


# ─────────────────────────── chạy ───────────────────────────

MAU_NGHE_THU = [
    {"id": "thu_en_1", "chu": "dog", "tieng": "en"},
    {"id": "thu_en_2", "chu": "teddy bear", "tieng": "en"},
    {"id": "thu_en_3", "chu": "This is a dog.", "tieng": "en"},
    {"id": "thu_en_4", "chu": "How many clocks? - Two.", "tieng": "en"},
    {"id": "thu_en_5", "chu": "How many windows can you see? - I can see six.", "tieng": "en"},
    {"id": "thu_vi_1", "chu": "Con nghe rồi bấm vào hình đúng nhé.", "tieng": "vi"},
    {"id": "thu_vi_2", "chu": "con chó", "tieng": "vi"},
    # Không nhắc tên nhân vật nào: quyển Tiếng Anh dựng cho MỌI học sinh, không đòi
    # bé phải biết trước thế giới của bốn quyển Toán.
    {"id": "thu_vi_3", "chu": "Hôm nay chúng mình học chữ Dê nhé!", "tieng": "vi"},
    {"id": "thu_vi_4", "chu": "Câu này có một chỗ đọc nhầm. Con nghe kỹ rồi sửa lại nhé.", "tieng": "vi"},
    {"id": "thu_vi_5", "chu": "Giỏi lắm! Con được ba ngôi sao.", "tieng": "vi"},
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--vao", type=Path, help="danh sách dòng chữ (JSON)")
    p.add_argument("--ra", type=Path, default=O / "ra", help="thư mục chứa mp3")
    p.add_argument("--so", type=Path, help="nơi ghi sổ tra")
    p.add_argument("--nghe-thu", action="store_true", help="sinh 10 clip mẫu")
    p.add_argument("--giong-en", default=GIONG_EN)
    p.add_argument("--giong-vi", default=GIONG_VI)
    a = p.parse_args()

    if a.nghe_thu:
        dong = MAU_NGHE_THU
        a.ra = a.ra or (O / "ra")
    elif a.vao:
        dong = json.loads(a.vao.read_text("utf8"))
    else:
        p.error("cần --vao hoặc --nghe-thu")

    # ── soát TRƯỚC khi nạp model: hỏng đầu vào thì báo ngay, đừng đợi tải 1 GB ──
    loi = [(m.get("id", f"#{i}"), s) for i, m in enumerate(dong) if (s := soat_dong(m))]
    if loi:
        print(f"✗ {len(loi)} dòng không dùng được:", file=sys.stderr)
        for i, s in loi[:10]:
            print(f"   {i}: {s}", file=sys.stderr)
        return 1

    a.ra.mkdir(parents=True, exist_ok=True)
    doc = {}
    so = []
    for m in dong:
        tieng = m["tieng"]
        if tieng not in doc:
            print(f"→ nạp model {'Anh' if tieng == 'en' else 'Việt'}…", flush=True)
            doc[tieng] = DocAnh(a.giong_en) if tieng == "en" else DocViet(a.giong_vi)
        giong = a.giong_en if tieng == "en" else a.giong_vi
        # TỐC ĐỘ: mô hình tự đọc chậm, KHÔNG kéo giãn tệp có sẵn. Kéo giãn bằng
        # `atempo` giữ được cao độ nhưng làm nhoè phụ âm — mà phụ âm mới là chỗ bé
        # cần nghe rõ khi tập nói theo.
        td = float(m.get("tocDo") or 1.0)
        ten = f"{m['id']}.mp3"
        ghi_mp3(doc[tieng](m["chu"], td), a.ra / ten)
        so.append({"id": m["id"], "chu": m["chu"], "tieng": tieng, "tocDo": td,
                   "tep": ten, "model": "kokoro-82m" if tieng == "en" else "kokoro-vi",
                   "giong": giong, "van_tay": bam(m["chu"])})
        print(f"   ✓ {ten}  [{tieng}/{giong}/×{td}]  {m['chu'][:46]}")

    if a.so:
        a.so.parent.mkdir(parents=True, exist_ok=True)
        a.so.write_text(json.dumps(
            {"_doc": "Sổ tra clip âm. Sửa chữ thì `van_tay` đổi → phải sinh lại clip ấy.",
             "mau_hz": MAU, "clip": so}, ensure_ascii=False, indent=1), "utf8")
        print(f"\n→ sổ tra: {a.so}")

    print(f"\nXong {len(so)} clip → {a.ra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
