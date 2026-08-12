#!/usr/bin/env python3
"""DỰNG VIDEO MP4 cho một bài Tiếng Anh lớp 1.

    tools/tts/.venv/bin/python tools/video/dung_video.py --bai DL_TA1_B04
    tools/tts/.venv/bin/python tools/video/dung_video.py --tat-ca

Đọc kịch bản (`kich_ban.py`) → vẽ từng cảnh ra PNG bằng Pillow → ghép hình với
tiếng bằng ffmpeg → một tệp mp4.

── VÌ SAO KHÔNG DÙNG figforge ──
`figforge` dựng sơ đồ toán bằng matplotlib, không vẽ được thẻ từ vựng có emoji màu.
Ở đây cần ba thứ nó không có: emoji màu, chữ Việt cỡ lớn, và bố cục theo cảnh.

── HAI CHỖ CỦA macOS PHẢI BIẾT TRƯỚC ──

1. `Apple Color Emoji.ttc` là phông sbix — Pillow CHỈ mở được ở đúng vài cỡ có sẵn
   (20·32·40·48·64·96·160). Xin cỡ khác là `invalid pixel size`. Nên vẽ ở 160 rồi
   thu nhỏ, không xin thẳng cỡ mình muốn.

2. Phông hệ thống mặc định KHÔNG đủ dấu tiếng Việt ở mọi cỡ. `Arial Unicode.ttf`
   có đủ — đã thử "Ở khu vườn, quả chuối" hiện đúng dấu.

── NHỊP HÌNH ──
Mỗi cảnh dài đúng bằng tiếng của nó cộng một khoảng lặng. Cảnh không có tiếng
(tách câu) dùng nhịp cố định. Không cắt hình giữa lúc đang nói.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kich_ban import cac_phan, soat  # noqa: E402
import hinh_ve  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

GOC = Path(__file__).resolve().parent.parent.parent
AUDIO = GOC / "web/public/content/tienganh/audio"
W, H = 1280, 720

# Bảng màu MOBILUCK — trùng tailwind.config.js và figforge/core.py.
NAVY, TEAL, GOLD, INK, MUTE = "#0B4EA8", "#1FCBAB", "#F9B233", "#15263A", "#5B6E85"
NEN, SOFT, LINE, ALERT = "#EEF4FA", "#EAF2FB", "#D4E1EE", "#C0392B"
TEAL_DARK, GOLD_DARK, TEAL_PALE, GOLD_PALE = "#04382C", "#5A3A00", "#E6FAF5", "#FFF4DF"

PHONG_VIET = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
PHONG_EMOJI = "/System/Library/Fonts/Apple Color Emoji.ttc"
EMOJI_CO = 160          # cỡ sbix DUY NHẤT dùng — xem chú thích đầu tệp

NGHI = 0.45             # khoảng lặng cuối mỗi cảnh, giây
NHIP_TINH = 2.6         # cảnh không tiếng (tách câu) dài bao lâu


def phong(co: int, dam=False):
    return ImageFont.truetype(PHONG_VIET, co)


def ve_emoji(im: Image.Image, ch: str, tam_x: int, tam_y: int, co: int):
    """Vẽ emoji ở cỡ 160 lên ảnh phụ rồi THU NHỎ — xem lý do ở đầu tệp."""
    if not ch:
        return
    o = Image.new("RGBA", (EMOJI_CO * 2, EMOJI_CO * 2), (0, 0, 0, 0))
    ImageDraw.Draw(o).text((0, 0), ch, font=ImageFont.truetype(PHONG_EMOJI, EMOJI_CO),
                           embedded_color=True)
    o = o.crop(o.getbbox() or (0, 0, 1, 1))
    ti = co / max(o.size)
    o = o.resize((max(1, int(o.width * ti)), max(1, int(o.height * ti))), Image.LANCZOS)
    im.paste(o, (tam_x - o.width // 2, tam_y - o.height // 2), o)


def giua(d: ImageDraw.ImageDraw, y: int, chu: str, f, mau=INK, rong=W - 160):
    """Viết một dòng CĂN GIỮA, tự xuống dòng khi quá rộng. Trả về y sau cùng."""
    if not chu:
        return y
    tu, dong, hien = chu.split(), [], ""
    for t in tu:
        thu = f"{hien} {t}".strip()
        if d.textlength(thu, font=f) <= rong:
            hien = thu
        else:
            dong.append(hien)
            hien = t
    dong.append(hien)
    cao = (f.size * 1.32)
    for i, x in enumerate(dong):
        d.text(((W - d.textlength(x, font=f)) / 2, y + i * cao), x, font=f, fill=mau)
    return int(y + len(dong) * cao)


def the(d, x, y, w, h, nen="#FFFFFF", vien=LINE, day=3, bo=26):
    d.rounded_rectangle([x, y, x + w, y + h], radius=bo, fill=nen, outline=vien, width=day)


# ─────────────────────────── vẽ từng loại cảnh ───────────────────────────

def khung(c: dict) -> Image.Image:
    im = Image.new("RGB", (W, H), NEN)
    d = ImageDraw.Draw(im)
    L = c["loai"]

    if L == "bia":
        the(d, 90, 170, W - 180, 380, nen=NAVY, vien=NAVY)
        giua(d, 250, c["chuChinh"], phong(64), "#FFFFFF")
        giua(d, 380, c["chuPhu"], phong(38), "#BFD8F5")

    elif L == "chu_cai":
        giua(d, 70, "Chữ hôm nay", phong(34), MUTE)
        the(d, W // 2 - 150, 150, 300, 300, nen=GOLD_PALE, vien=GOLD, day=5)
        giua(d, 210, c["chuChinh"], phong(180), NAVY)
        giua(d, 510, "Nghe ba từ này — chúng bắt đầu giống nhau", phong(40), INK)

    elif L == "tu":
        # Hai đường ra hình, cùng thứ tự ưu tiên với màn hình (`HinhVe.jsx`):
        # hình vẽ tay trước, rồi mới tới emoji. Bản trước không có nhánh đầu nên
        # bảy từ hiện một thẻ chữ trống — đúng cái mà bộ hình vẽ tay sinh ra để
        # tránh. Nét vẽ đọc từ CHÍNH tệp màn hình đang đọc, xem `hinh_ve.py`.
        if hinh_ve.dan(im, c.get("ve"), W // 2, 250, 280):
            y = 440
        elif c.get("hinh"):
            ve_emoji(im, c["hinh"], W // 2, 250, 260)
            y = 430
        else:
            the(d, W // 2 - 260, 140, 520, 210, nen=SOFT, vien=LINE)
            giua(d, 200, "🔤", phong(1))     # chỗ giữ, không vẽ emoji sai
            y = 400
        giua(d, y, c["chuChinh"], phong(96), NAVY)
        giua(d, y + 130, c["chuPhu"], phong(42), INK)

    elif L == "dung_de":
        giua(d, 60, "Câu hôm nay dùng để làm gì", phong(34), MUTE)
        y = giua(d, 130, c["chuChinh"], phong(58), NAVY)
        the(d, 110, y + 40, W - 220, 190, nen=SOFT, vien=LINE)
        giua(d, y + 80, c["chuPhu"], phong(40), INK, rong=W - 280)

    elif L == "tach_cau":
        giua(d, 60, "Câu này gồm những mẩu nào", phong(34), MUTE)
        phan, n = c["phan"], c["soPhan"]
        y = 170
        for i, ph in enumerate(phan):
            hien = i < n
            nen = (GOLD if ph.get("thay") else SOFT) if hien else "#F5F8FC"
            chu_mau = (GOLD_DARK if ph.get("thay") else NAVY) if hien else "#C9D6E4"
            the(d, 120, y, 300, 74, nen=nen, vien=LINE if not hien else nen, bo=16)
            f = phong(40)
            d.text((120 + (300 - d.textlength(ph["chu"], font=f)) / 2, y + 14),
                   ph["chu"], font=f, fill=chu_mau)
            if hien:
                d.text((460, y + 20), ph["lam_gi"], font=phong(32), fill=INK if i == n - 1 else MUTE)
            y += 92

    elif L == "ca_cau":
        if not hinh_ve.dan(im, c.get("ve"), W // 2, 220, 230) and c.get("hinh"):
            ve_emoji(im, c["hinh"], W // 2, 220, 210)
        the(d, 90, 370, W - 180, 150, nen="#FFFFFF", vien=NAVY, day=4)
        giua(d, 405, c["chuChinh"], phong(62), NAVY)
        giua(d, 560, c["chuPhu"], phong(38), MUTE)

    elif L == "de_nham":
        giua(d, 60, "Chỗ dễ nhầm", phong(34), GOLD_DARK)
        the(d, 110, 130, W - 220, 120, nen=GOLD_PALE, vien=GOLD)
        giua(d, 165, c["chuChinh"], phong(54), ALERT)
        f = phong(54)
        w = d.textlength(c["chuChinh"], font=f)
        d.line([(W - w) / 2, 192, (W + w) / 2, 192], fill=ALERT, width=4)
        the(d, 110, 290, W - 220, 120, nen=TEAL_PALE, vien=TEAL)
        giua(d, 325, c["chuPhu"], phong(54), TEAL_DARK)
        giua(d, 450, c.get("why", ""), phong(32), INK, rong=W - 260)

    elif L == "dan_noi":
        ve_emoji(im, "🗣️", W // 2, 230, 180)
        giua(d, 390, c["chuChinh"], phong(66), NAVY)
        giua(d, 490, c["chuPhu"], phong(38), MUTE)

    elif L == "nhac_theo":
        # Ba lần, chậm dần lên bình thường. Chấm tròn cho bé biết đang lần mấy —
        # bé chưa đọc được chữ "2/3", nhưng ba chấm thì nhìn là hiểu.
        giua(d, 56, "Nói theo cô", phong(32), MUTE)
        the(d, 90, 190, W - 180, 170, nen="#FFFFFF", vien=TEAL, day=5)
        giua(d, 235, c["chuChinh"], phong(64), NAVY)
        n, tong = c.get("lan", 1), c.get("soLan", 3)
        r, cach = 26, 90
        x0 = W // 2 - cach * (tong - 1) // 2
        for i in range(tong):
            xong = i < n
            d.ellipse([x0 + i * cach - r, 430 - r, x0 + i * cach + r, 430 + r],
                      fill=TEAL if xong else "#FFFFFF", outline=TEAL, width=4)
        giua(d, 500, c["chuPhu"], phong(44), TEAL_DARK)
        giua(d, 580, "🐢 → 🐇", phong(1))
        ve_emoji(im, "🐢" if c.get("tocDo", 1) < 0.75 else ("🐇" if c.get("tocDo", 1) >= 1 else "🚶"),
                 W // 2, 615, 74)

    elif L == "ket":
        giua(d, 190, "🎉", phong(1))
        ve_emoji(im, "🎉", W // 2, 240, 190)
        giua(d, 400, c["chuChinh"], phong(72), TEAL_DARK)
        giua(d, 505, c["chuPhu"], phong(34), MUTE)

    return im


# ─────────────────────────── ghép ───────────────────────────

def dai(tep: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(tep)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def dung(bai_ma: str, ra: Path, ds: list[dict], so: dict) -> dict:
    """Dựng MỘT video từ một danh sách cảnh."""
    thieu = soat(ds, so)
    if thieu:
        raise SystemExit(f"✗ {ra.name}: {len(thieu)} cảnh câm — {thieu[0]}")
    tep_cua = {c["id"]: AUDIO / c["tep"] for c in so["clip"]}

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        anh_ds, am_ds, tong = [], [], 0.0
        for i, c in enumerate(ds):
            p = tmp / f"c{i:03d}.png"
            khung(c).save(p)
            clip = [tep_cua[m] for m in c["am"]] * c.get("lapLai", 1)
            d = sum(dai(x) for x in clip) + NGHI * max(1, len(clip))
            if c.get("choNoi"):
                # CHỪA CHỖ CHO BÉ NÓI — dài bằng chính câu ấy, cộng chút đà.
                # Không chừa thì "nói theo" chỉ là nghe ba lần.
                d += sum(dai(x) for x in clip) + 0.7
            if not clip:
                d = NHIP_TINH
            anh_ds.append((p, d))
            am_ds.append(clip)
            tong += d

        # ── dải tiếng: nối các clip, chèn khoảng lặng đúng chỗ ──
        loc, dau_vao = [], []
        n = 0
        moc = 0.0
        for (p, d), clip in zip(anh_ds, am_ds):
            t = moc
            for x in clip:
                dau_vao += ["-i", str(x)]
                loc.append(f"[{n}:a]adelay={int(t * 1000)}|{int(t * 1000)}[a{n}]")
                t += dai(x) + NGHI
                n += 1
            moc += d
        wav = tmp / "tieng.wav"
        if n:
            tron = "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0[out]"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *dau_vao,
                            "-filter_complex", ";".join(loc) + ";" + tron,
                            "-map", "[out]", "-t", f"{tong:.3f}", str(wav)], check=True)

        # ── dải hình: danh sách concat ──
        ds_tep = tmp / "hinh.txt"
        ds_tep.write_text("".join(
            f"file '{p}'\nduration {d:.3f}\n" for p, d in anh_ds)
            + f"file '{anh_ds[-1][0]}'\n", "utf8")

        ra.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(ds_tep),
            *(["-i", str(wav)] if n else []),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "24",
            *(["-c:a", "aac", "-b:a", "96k", "-shortest"] if n else []),
            str(ra)], check=True)

    return {"canh": len(ds), "giay": round(tong, 1), "mb": round(ra.stat().st_size / 1e6, 2)}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--bai")
    p.add_argument("--tat-ca", action="store_true")
    p.add_argument("--ra", default="web/public/content/tienganh/video")
    a = p.parse_args()

    dsm = ([f"DL_TA1_B{i:02d}" for i in range(1, 17)] if a.tat_ca
           else [a.bai] if a.bai else None)
    if not dsm:
        p.error("cần --bai DL_TA1_B04 hoặc --tat-ca")
    so = json.loads((GOC / "web/public/content/tienganh/lop1_am.json").read_text("utf8"))
    tong = 0.0
    for m in dsm:
        bai = json.loads((GOC / f"web/public/content/ta1/{m}.json").read_text("utf8"))
        hp = cac_phan(bai)
        # Một tệp cho TỪ, rồi MỖI MẪU CÂU một tệp. Bài hai mẫu câu (U1 · U11 · U13)
        # mà gộp chung thì bé xem xong không biết vừa học một cấu trúc hay hai.
        # Tên tệp nói ra VAI của video: `_hoi` / `_dap` cho cặp hỏi–đáp, `_cauN`
        # cho mẫu câu thường. Nhìn tên là biết mở cái nào, không phải đoán số.
        phan = [("tu", hp["tu"])]
        vais = [kh[0].get("vaiKhoi", "cau") for kh in hp["cau"]]
        dem = {}
        for kh, v in zip(hp["cau"], vais):
            dem[v] = dem.get(v, 0) + 1
            ten = v if vais.count(v) == 1 else f"{v}{dem[v]}"
            phan.append((ten, kh))
        for ten, canh in phan:
            kq = dung(m, GOC / a.ra / f"{m}_{ten}.mp4", canh, so)
            tong += kq["giay"]
            print(f"  ✓ {m}_{ten}.mp4  {kq['canh']:2d} cảnh · "
                  f"{kq['giay']:5.1f}s · {kq['mb']} MB")
    print(f"\n{len(dsm) * 2} video · tổng {tong / 60:.1f} phút")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
