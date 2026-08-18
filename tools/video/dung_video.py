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
import math
import re
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


def ngat_dong(d: ImageDraw.ImageDraw, chu: str, f, rong: int) -> list[str]:
    """Ngắt chữ thành các dòng vừa bề rộng — CÙNG phép ngắt mà `giua()` dùng.

    Tách riêng ra để chỗ nào cần BIẾT TRƯỚC số dòng (mà vẽ khung cho vừa) thì hỏi
    được, thay vì đoán bằng số ký tự. Đếm bằng ký tự là sai: chữ tiếng Việt có dấu
    rộng hẹp khác nhau, và đó đúng là cách 72 màn công thức lọt lưới.
    """
    if not chu:
        return []
    dong, hien = [], ""
    for t in chu.split():
        thu = f"{hien} {t}".strip()
        if d.textlength(thu, font=f) <= rong:
            hien = thu
        else:
            dong.append(hien)
            hien = t
    dong.append(hien)
    return dong


def giua(d: ImageDraw.ImageDraw, y: int, chu: str, f, mau=INK, rong=W - 160):
    """Viết một dòng CĂN GIỮA, tự xuống dòng khi quá rộng. Trả về y sau cùng."""
    if not chu:
        return y
    dong = ngat_dong(d, chu, f, rong)
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
        # Cỡ chữ theo ĐỘ DÀI tên bài, và dòng phụ đặt theo y THẬT mà tiêu đề kết
        # thúc. Bản cũ ghim cứng y = 380 cho dòng phụ: tên ngắn của Tiếng Anh thì
        # vừa, nhưng tên bài Toán dài xuống hai dòng là phủ đè lên nó.
        n = len(c["chuChinh"])
        co = 64 if n <= 26 else (52 if n <= 44 else 42)
        the(d, 90, 170, W - 180, 380, nen=NAVY, vien=NAVY)
        y = giua(d, 235 if n <= 26 else 205, c["chuChinh"], phong(co), "#FFFFFF",
                 rong=W - 260)
        giua(d, max(y + 34, 380), c["chuPhu"], phong(36), "#BFD8F5")

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

    # ══ BA CẢNH CỦA MÔN TOÁN ══
    # Bác chốt 14-08: mở bài và bài giảng của lớp 4 phải thành VIDEO, và KHÔNG DÙNG
    # ẨN DỤ — bé xem lần đầu là hiểu. Nên ba cảnh dưới đây cố ý rất trơ: một hình,
    # một câu, không nhân vật, không ví von. Chữ trên màn CHỈ để bám mắt; lời đọc
    # mới là kênh chính, giống hệt cách video Tiếng Anh đang làm.
    elif L == "de_toan":
        # ĐỀ BÀI — chỉ đọc đề, KHÔNG hé cách làm. Đây là bản đề, không phải bài giải.
        #
        # ⚠ NHẬN CẢ `de` LẪN `chuChinh`. Kịch bản viết theo hai lối, và lối phổ biến
        # hơn là `_c('de_toan', 'Đề bài', de='<đề thật>')`. Bản cũ chỉ đọc `chuChinh`
        # nên 27 video lớp 2 đã lên bản thật với cái khung TRẮNG TRƠN mang đúng hai
        # chữ "Đề bài", trong khi tiếng vẫn đọc trọn đề — bé nghe một đằng, nhìn một
        # nẻo, và không có gì để đọc lại. Không cổng nào kêu vì mp4 vẫn hợp lệ; chỉ
        # lộ ra khi rút khung hình ra nhìn.
        giua(d, 56, "Bài toán hôm nay", phong(32), MUTE)
        the(d, 80, 130, W - 160, 330, nen="#FFFFFF", vien=NAVY, day=4)
        giua(d, 175, c.get("de") or c["chuChinh"], phong(40), INK, rong=W - 240)
        if c.get("chuPhu"):
            giua(d, 500, c["chuPhu"], phong(36), GOLD_DARK, rong=W - 220)

    elif L == "hinh_toan":
        # MỘT HÌNH, MỘT DÒNG. Hình lớp 4 đã vẽ sẵn ở `figures/` — video dùng ĐÚNG
        # tệp màn hình đang dùng, không vẽ lại bản thứ hai (bài học của `hinh_ve`).
        tep = c.get("tepHinh")
        if tep and Path(tep).exists():
            h = Image.open(tep).convert("RGB")
            rong = W - 160
            cao = int(h.height * rong / h.width)
            cao_toi_da = 430
            if cao > cao_toi_da:
                rong = int(rong * cao_toi_da / cao); cao = cao_toi_da
            im.paste(h.resize((rong, cao)), ((W - rong) // 2, 120))
            y = 120 + cao + 30
        else:
            y = 300
        giua(d, min(y, H - 130), c["chuChinh"], phong(36), INK, rong=W - 200)

    elif L == "cong_thuc":
        # CÔNG THỨC PHẢI HIỆN LÊN, KHÔNG CHỈ ĐỌC. Bác chốt 14-08: "các công thức cần
        # phải show trên video thay vì chỉ đọc, không học sinh sẽ không nhớ được."
        # Nghe một câu dài rồi trôi qua thì bé không giữ lại được gì; nhìn thấy nó
        # đóng khung thì còn hình trong đầu.
        #
        # Ký hiệu (n, ×, −, :) CHỈ ở đây — trên màn hình. Lời đọc thì nói bằng chữ
        # thuần Việt, vì máy đọc ký hiệu là đọc sai.
        giua(d, 54, c.get("chuChinh", "Công thức cần nhớ"), phong(34), MUTE)
        the(d, 60, 120, W - 120, 210, nen=GOLD_PALE, vien=GOLD, day=6)
        giua(d, 175, c["congThuc"], phong(46), NAVY, rong=W - 190)
        if c.get("thay"):
            # ⚠ KHUNG PHẢI GIÃN THEO SỐ DÒNG. Bản cũ đóng cứng cao 120 — vừa đúng
            # MỘT dòng. Câu nào dài hơn thì dòng thứ hai rơi xuống DƯỚI đáy khung,
            # chữ đen nằm trần trên nền. 72 trong 419 màn công thức của cả bốn quyển
            # đã lên bản thật như thế (lộ ra ở lớp 5 bài 17, 16-08-2026).
            giua(d, 385, "Thay số vào thử", phong(30), MUTE)
            f = phong(42)
            n = len(ngat_dong(d, c["thay"], f, W - 260))
            b_dong = int(f.size * 1.32)
            cao_khung = max(120, b_dong * n + 64)
            the(d, 110, 430, W - 220, cao_khung, nen="#FFFFFF", vien=TEAL, day=4)
            giua(d, 430 + (cao_khung - b_dong * n) // 2, c["thay"], f, TEAL_DARK,
                 rong=W - 260)

    elif L == "day_so":
        # MỘT DÃY SỐ VẼ RA THÀNH Ô — đây là hình quan trọng nhất của cả cụm, vì nó
        # cho bé THẤY hai thứ khác nhau nằm chồng lên nhau: hàng trên là THỨ TỰ
        # (đứng thứ mấy), hàng dưới là GIÁ TRỊ (số nào). Bác dặn nói thẳng hai khái
        # niệm ấy, nên phải có chỗ chỉ tay vào được.
        giua(d, 56, c.get("chuChinh", ""), phong(40), NAVY, rong=W - 160)
        so = c.get("so", [])
        n = len(so)
        rong_o, cach = 118, 16
        tong = n * rong_o + (n - 1) * cach
        x0 = (W - tong) // 2
        chi = c.get("chiSo")            # ô đang được chỉ tay vào, 1-based
        y_tt, y_gt = 190, 300
        f_nh = phong(30)

        def nhan_hang(y, chu):
            """Nhãn bên trái hàng, CĂN PHẢI để nó dừng ngay trước ô đầu tiên.

            Bản đầu đặt cứng ở `x0 - 130`, hợp với nhãn ngắn như "số". Nhãn dài thì
            nó chạy đè lên ô đầu — lớp 5 bài 55 M3 có hai ô, nhãn "giờ · xuôi và
            ngược" nuốt mất luôn con số thứ nhất. Nhãn dài quá cả lề thì cho leo lên
            trên hàng, thà lệch chỗ còn hơn đè mất số.
            """
            w_ = d.textlength(chu, font=f_nh)
            if x0 - 20 - w_ >= 12:
                d.text((x0 - 20 - w_, y), chu, font=f_nh, fill=MUTE)
            else:
                d.text((max((W - w_) / 2, 12), y - 48), chu, font=f_nh, fill=MUTE)

        if c.get("hienThuTu"):
            nhan_hang(y_tt + 22, "đứng thứ")
        # Nhãn hàng giá trị. Mặc định là "số", nhưng khai `nhanHang` để đổi khi hàng
        # ấy KHÔNG phải là số của đề — lớp 5 bài 21 vẽ dãy PHẦN LỆCH (−3 +3 +1 −1),
        # để nguyên chữ "số" thì bé đọc ra một dãy số không có trong đề nào cả.
        nhan_hang(y_gt + 26, c.get("nhanHang", "số"))
        for i, v in enumerate(so):
            x = x0 + i * (rong_o + cach)
            sang = chi is not None and (i + 1) == chi
            if c.get("hienThuTu"):
                the(d, x, y_tt, rong_o, 76, nen=GOLD if sang else GOLD_PALE,
                    vien=GOLD, day=4 if sang else 3, bo=16)
                f = phong(40)
                t = str(i + 1)
                d.text((x + (rong_o - d.textlength(t, font=f)) / 2, y_tt + 16), t,
                       font=f, fill=GOLD_DARK)
            the(d, x, y_gt, rong_o, 86, nen=TEAL_PALE if sang else "#FFFFFF",
                vien=TEAL if sang else LINE, day=5 if sang else 3, bo=16)
            f = phong(46)
            t = str(v)
            d.text((x + (rong_o - d.textlength(t, font=f)) / 2, y_gt + 18), t,
                   font=f, fill=NAVY)
        if c.get("chuPhu"):
            giua(d, 440, c["chuPhu"], phong(38), INK, rong=W - 200)

    elif L == "nhom_deu":
        # ══ CHIA HẾT, NHÌN THẤY ĐƯỢC ══
        # Luật 9 bác ra ở đợt 2: chỗ nào khó hiểu thì vẽ ra. "Chia hết" là chỗ khó
        # nhất của cả chương, vì nói bằng lời thì nó chỉ là một câu trừu tượng —
        # còn xếp 12 viên kẹo thành 4 nhóm 3 viên, không thừa viên nào, thì bé THẤY.
        #
        # Cảnh này vẽ `tong` viên thành từng nhóm `moiNhom` viên. Viên nào không đủ
        # xếp thành nhóm thì đứng riêng, tô đỏ — đó chính là SỐ DƯ, và bé thấy ngay
        # vì sao dư luôn phải nhỏ hơn số chia: đủ một nhóm nữa thì nó đã vào nhóm rồi.
        giua(d, 50, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        tong, moi_nhom = c.get("tong", 0), c.get("moiNhom", 1)
        so_nhom, du = divmod(tong, moi_nhom)
        r, cach_v = 21, 52                      # bán kính viên, khoảng cách tâm
        cot = min(moi_nhom, 3)                  # mỗi nhóm xếp tối đa 3 viên một hàng
        hang = -(-moi_nhom // cot)
        w_nhom = cot * cach_v + 34
        h_nhom = hang * cach_v + 34
        khung = [(w_nhom, h_nhom, moi_nhom)] * so_nhom
        if du:
            khung.append((min(du, 3) * cach_v + 34, cach_v + 34, du))
        tong_w = sum(k[0] for k in khung) + 22 * (len(khung) - 1)
        x = (W - tong_w) // 2
        # Đặt khối ô CÂN GIỮA phần dưới tiêu đề, chừa chỗ cho hai dòng chữ.
        # Bản đầu ghim y0 = 190 nên khung cao 720 bỏ trống hẳn một phần ba dưới.
        y0 = max(150, (H - h_nhom - 150) // 2)
        for k, (wn, hn, sl) in enumerate(khung):
            le = du and k == len(khung) - 1     # ô cuối là phần thừa
            the(d, x, y0, wn, hn, nen="#FFF0EE" if le else TEAL_PALE,
                vien=ALERT if le else TEAL, day=4, bo=18)
            for i in range(sl):
                cx = x + 17 + (i % cot) * cach_v + r + 4
                cy = y0 + 17 + (i // cot) * cach_v + r + 4
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          fill=ALERT if le else TEAL_DARK,
                          outline=ALERT if le else TEAL_DARK)
            x += wn + 22
        nhan = c.get("chuPhu") or (
            f"{tong} chia {moi_nhom} được {so_nhom} nhóm, thừa {du}" if du
            else f"{tong} chia {moi_nhom} được {so_nhom} nhóm, không thừa")
        giua(d, y0 + h_nhom + 46, nhan, phong(38), ALERT if du else TEAL_DARK,
             rong=W - 160)
        if c.get("chuCuoi"):
            giua(d, y0 + h_nhom + 118, c["chuCuoi"], phong(34), INK, rong=W - 200)

    elif L == "luoi_cham":
        # ══ KHAY KẸO HÀNG × CỘT — VẼ ĐÚNG CÁI MÌNH ĐANG NÓI ══
        #
        # ⚠ CẢNH NÀY RA ĐỜI VÌ MỘT LỖI CHỈ LỘ KHI MỞ MẮT XEM. Bài "ghép hai khay kẹo"
        # ban đầu mượn cảnh `nhom_deu`, lời đọc bảo "ba hàng, mỗi hàng bốn viên", mà
        # `nhom_deu` xếp tối đa ba viên một dòng nên vẽ ra BA NHÓM bốn viên, mỗi nhóm
        # gấp thành hai dòng. Bé nghe "hàng" mà nhìn thấy "nhóm" — hai thứ khác nhau,
        # và cả bài dạy phép nhân đứng trên đúng chữ "hàng" ấy.
        #
        # Nên cảnh này vẽ ĐÚNG một lưới `hang` dòng, mỗi dòng `cot` viên. `cot2` vẽ
        # thêm phần nối dài bên phải bằng màu khác — đó chính là lúc hai khay đẩy sát
        # vào nhau: số hàng giữ nguyên, mỗi hàng dài thêm.
        giua(d, 46, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        hang = max(1, c.get("hang", 1))
        cot = max(1, c.get("cot", 1))
        cot2 = max(0, c.get("cot2", 0))
        tong_cot = cot + cot2
        # Viên to hết mức mà vẫn vừa bề ngang; lưới rộng thì viên nhỏ lại.
        cach = min(62, int((W - 260) / max(tong_cot, 1)), int(360 / hang))
        r = max(7, cach // 2 - 6)
        w_luoi = tong_cot * cach
        h_luoi = hang * cach
        x0 = (W - w_luoi) // 2
        y0 = max(150, (H - h_luoi - 190) // 2)
        # Khung ôm khay thứ nhất, và khay nối thêm nếu có.
        the(d, x0 - 20, y0 - 20, cot * cach + 40, h_luoi + 40,
            nen=TEAL_PALE, vien=TEAL, day=4, bo=18)
        if cot2:
            the(d, x0 + cot * cach - 20, y0 - 20, cot2 * cach + 40, h_luoi + 40,
                nen=GOLD_PALE, vien=GOLD, day=4, bo=18)
        for i in range(hang):
            for j in range(tong_cot):
                cx = x0 + j * cach + cach // 2
                cy = y0 + i * cach + cach // 2
                mau = GOLD_DARK if j >= cot else TEAL_DARK
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mau, outline=mau)
        nhan = c.get("chuPhu") or f"{hang} × {tong_cot} = {hang * tong_cot} viên"
        giua(d, y0 + h_luoi + 54, nhan, phong(38), TEAL_DARK, rong=W - 160)
        if c.get("chuCuoi"):
            giua(d, y0 + h_luoi + 124, c["chuCuoi"], phong(34), INK, rong=W - 200)

    elif L == "bang_loai_tru":
        # ══ BẢNG LOẠI TRỪ — CÁCH SUY LUẬN KHÔNG PHẢI ĐOÁN MÒ ══
        #
        # Cả bài "ai cầm cái gì" đứng trên một cái bảng: mỗi hàng một bạn, mỗi cột
        # một đồ vật, manh mối chắc chắn thì đánh dấu, rồi gạch hết ô cùng hàng cùng
        # cột. Nói bằng lời thì rối; vẽ ra thì bé thấy ngay hàng nào chỉ còn một ô
        # trống — và ô ấy chính là đáp án.
        #
        # `hang` và `cot` là nhãn. `o` là bảng ký hiệu, mỗi phần tử là "" (chưa
        # biết), "v" (đúng, tô teal) hoặc "x" (đã loại, tô đỏ nhạt).
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        hang = c.get("hang", [])
        cot = c.get("cot", [])
        o = c.get("o", [])
        n_h, n_c = len(hang), len(cot)
        if not n_h or not n_c:
            return im
        w_o, h_o = 150, 84
        w_nhan = 190
        tong_w = w_nhan + n_c * w_o
        x0 = (W - tong_w) // 2
        y0 = 190
        f_nhan, f_ky = phong(30), phong(52)
        # hàng tiêu đề cột
        for j, ten in enumerate(cot):
            x = x0 + w_nhan + j * w_o
            giua_x = x + w_o / 2
            d.text((giua_x - d.textlength(ten, font=f_nhan) / 2, y0 - 48), ten,
                   font=f_nhan, fill=NAVY)
        for i, ten in enumerate(hang):
            y = y0 + i * h_o
            d.text((x0 + w_nhan - 20 - d.textlength(ten, font=f_nhan), y + 24), ten,
                   font=f_nhan, fill=NAVY)
            for j in range(n_c):
                x = x0 + w_nhan + j * w_o
                ky = (o[i][j] if i < len(o) and j < len(o[i]) else "") or ""
                nen = TEAL_PALE if ky == "v" else ("#FFF0EE" if ky == "x" else "#FFFFFF")
                vien = TEAL if ky == "v" else (ALERT if ky == "x" else LINE)
                the(d, x + 6, y + 6, w_o - 12, h_o - 12, nen=nen, vien=vien,
                    day=5 if ky else 3, bo=14)
                if ky:
                    t = "✓" if ky == "v" else "✗"
                    mau = TEAL_DARK if ky == "v" else ALERT
                    d.text((x + w_o / 2 - d.textlength(t, font=f_ky) / 2, y + 12), t,
                           font=f_ky, fill=mau)
        if c.get("chuPhu"):
            giua(d, y0 + n_h * h_o + 40, c["chuPhu"], phong(36), INK, rong=W - 160)

    elif L == "dong_ho":
        # ══ MẶT ĐỒNG HỒ HAI KIM ══
        # Cả bài xem giờ đứng trên việc PHÂN BIỆT HAI KIM: kim giờ ngắn và mập, kim
        # phút dài và mảnh. Vẽ hai kim dài bằng nhau là bài học đổ ngay từ hình.
        #
        # `gio` và `phut` là số mà mỗi kim đang chỉ (phút tính theo MẶT SỐ, tức 12 là
        # đúng giờ và 6 là rưỡi). Kim giờ tự xê dịch theo phút, nên "3 giờ rưỡi" thì
        # kim giờ nằm đúng giữa 3 và 4 — chính là chỗ bé hay đọc nhầm thành 4 giờ.
        # ⚠ ĐỪNG `import math` ở đây. `math` đã nhập ở đầu tệp; nhập lại BÊN TRONG
        # hàm làm nó thành biến CỤC BỘ của cả hàm `khung()`, nên mọi nhánh khác gọi
        # `math` mà chạy TRƯỚC nhánh này đều vỡ với `UnboundLocalError`. Đã dính:
        # `hinh_tron` có `dayLech` gọi `math.sqrt`, và video `DL_KSN4_B80` không
        # dựng lại được nữa — tệp cũ vẫn nằm đó nên không ai hay, cho tới lần dựng
        # lại đầu tiên, mà lần ấy cách hàng tháng.
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        cx, cy, r = W // 2, 350, 190
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#FFFFFF", outline=NAVY,
                  width=8)
        gio = float(c.get("gio", 12))
        phut = float(c.get("phut", 12))
        # Kim giờ xê dịch theo kim phút: đi hết một vòng phút thì kim giờ tiến một số.
        gio_that = (gio % 12) + (phut % 12) / 12
        for nhan, val, dai, day, mau in (
                ('kim giờ', gio_that * 30, r - 96, 20, TEAL_DARK),
                ('kim phút', (phut % 12) * 30, r - 34, 12, GOLD_DARK)):
            goc = math.radians(val - 90)
            d.line([cx, cy, cx + dai * math.cos(goc), cy + dai * math.sin(goc)],
                   fill=mau, width=day)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=NAVY)
        # ⚠ VẼ SỐ SAU KIM. Bản đầu vẽ số trước nên kim phút chỉ số 6 đè lên đúng con
        # số 6 — chính con số mà cả bài đang bảo bé nhìn vào.
        f_so = phong(38)
        for k in range(1, 13):
            goc = math.radians(k * 30 - 90)
            x = cx + (r - 42) * math.cos(goc)
            y = cy + (r - 42) * math.sin(goc)
            t = str(k)
            w = d.textlength(t, font=f_so)
            # Nền trắng nhỏ dưới chữ, để kim có chạy qua thì số vẫn đọc được.
            d.ellipse([x - w / 2 - 10, y - 30, x + w / 2 + 10, y + 30],
                      fill="#FFFFFF")
            d.text((x - w / 2, y - 24), t, font=f_so,
                   fill=NAVY if k in (12, 6) else MUTE)
        # Chú thích hai kim, đặt hai bên để không đè lên mặt số.
        f_ch = phong(30)
        d.text((80, cy - 40), 'kim giờ: NGẮN và mập', font=f_ch, fill=TEAL_DARK)
        d.text((80, cy + 10), 'kim phút: DÀI', font=f_ch, fill=GOLD_DARK)
        if c.get("chuPhu"):
            giua(d, cy + r + 44, c["chuPhu"], phong(38), INK, rong=W - 160)

    elif L == "hinh_cn":
        # ══ HÌNH CHỮ NHẬT — VẼ ĐƯỢC CẢ CHU VI LẪN DIỆN TÍCH ══
        # Chỗ bé lẫn nhất cả chương là chu vi với diện tích. Nói bằng lời thì hai chữ
        # ấy nghe na ná nhau; vẽ ra thì một cái là ĐƯỜNG ĐI QUANH MÉP, một cái là
        # MẶT BỊ PHỦ KÍN — hai thứ chẳng giống nhau chút nào.
        #
        # `oVuong=True` phủ lưới ô đơn vị để đếm diện tích. `vienDam=True` tô đậm
        # đường quanh mép để chỉ chu vi. Bật cả hai thì thấy luôn hai thứ trên cùng
        # một hình, đúng chỗ cần so.
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        dai, rong = c.get("dai", 1), c.get("rong", 1)
        o = min(74, int(560 / max(dai, 1)), int(300 / max(rong, 1)))
        w, h = dai * o, rong * o
        x0, y0 = (W - w) // 2, 190
        if c.get("oVuong"):
            for i in range(dai):
                for j in range(rong):
                    the(d, x0 + i * o, y0 + j * o, o, o,
                        nen=TEAL_PALE, vien=TEAL, day=2, bo=0)
        else:
            the(d, x0, y0, w, h, nen="#FFFFFF", vien=LINE, day=3, bo=0)
        # `duongCheo` cắt hình thành hai tam giác BẰNG NHAU — hình của bài cắt ghép.
        # Tô hai nửa hai màu để bé thấy chúng đúng bằng nhau, không phải tin lời.
        if c.get("duongCheo"):
            # Tô nền hai nửa thì ĐÈ MẤT lưới ô — mà lưới ô mới là chỗ bé đếm ra 48.
            # Nên có lưới thì chỉ kẻ đường chéo, không tô.
            if not c.get("oVuong"):
                d.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h)], fill=TEAL_PALE)
                d.polygon([(x0, y0), (x0, y0 + h), (x0 + w, y0 + h)], fill=GOLD_PALE)
            d.line([x0, y0 + h, x0 + w, y0], fill=ALERT, width=7)
        if c.get("vienDam"):
            d.rectangle([x0, y0, x0 + w, y0 + h], outline=GOLD, width=9)
        else:
            d.rectangle([x0, y0, x0 + w, y0 + h], outline=TEAL_DARK, width=4)
        f = phong(32)
        if c.get("nhanDai"):
            giua(d, y0 - 44, c["nhanDai"], f, INK, rong=W - 200)
        if c.get("nhanRong"):
            t = c["nhanRong"]
            d.text((x0 - 22 - d.textlength(t, font=f), y0 + h // 2 - 18), t,
                   font=f, fill=INK)
        if c.get("chuPhu"):
            giua(d, y0 + h + 44, c["chuPhu"], phong(36), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y0 + h + 110, c["chuCuoi"], phong(32),
                 GOLD_DARK if c.get("vienDam") else TEAL_DARK, rong=W - 200)

    elif L == "bang_hang":
        # ══ BẢNG HÀNG VÀ LỚP ══
        # Cả chương một đứng ở một ý mà nói bằng lời thì rối: chữ số đứng ở đâu thì
        # nặng bấy nhiêu, và cứ BA HÀNG gom thành MỘT LỚP. Vẽ ra thì hai chuyện ấy
        # thành một cái nhìn: mỗi chữ số một ô, ba ô một khung, khung có tên.
        #
        # Ô đánh số TỪ PHẢI SANG — đúng chiều đọc giá trị, không phải chiều đọc chữ.
        # `toSang` khai theo chiều ấy: 0 là hàng đơn vị.
        giua(d, 40, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        chu_so = [k for k in str(c.get("so", "")) if k.isdigit()]
        n = len(chu_so)
        TEN_HANG = ["đơn vị", "chục", "trăm", "nghìn", "chục nghìn", "trăm nghìn",
                    "triệu", "chục triệu", "trăm triệu"]
        TEN_LOP = ["đơn vị", "nghìn", "triệu"]
        o = min(104, int((W - 200) / max(n, 1)))
        x0, y0 = (W - n * o) // 2, 210
        sang = set(c.get("toSang") or [])
        for i, k in enumerate(chu_so):
            bac = n - 1 - i                       # bậc tính từ PHẢI sang
            to = bac in sang
            the(d, x0 + i * o, y0, o, o, nen=GOLD_PALE if to else "#FFFFFF",
                vien=GOLD if to else LINE, day=4 if to else 3, bo=0)
            f = phong(int(o * 0.56))
            d.text((x0 + i * o + (o - d.textlength(k, font=f)) / 2, y0 + o * 0.18),
                   k, font=f, fill=GOLD_DARK if to else NAVY)
            g = phong(21)
            ten = TEN_HANG[bac] if bac < len(TEN_HANG) else ""
            for j, t in enumerate(ten.split()):
                d.text((x0 + i * o + (o - d.textlength(t, font=g)) / 2,
                        y0 + o + 8 + j * 24), t, font=g, fill=MUTE)
        # Khung lớp: ba hàng một khung, tên khung viết phía trên.
        if c.get("hienLop", True):
            for lop in range((n + 2) // 3):
                dau = n - (lop + 1) * 3
                rong_lop = 3 if dau >= 0 else 3 + dau
                dau = max(dau, 0)
                x = x0 + dau * o
                d.rounded_rectangle([x - 6, y0 - 44, x + rong_lop * o + 6, y0 + o + 6],
                                    radius=10, outline=TEAL, width=4)
                t = f"lớp {TEN_LOP[lop]}" if lop < len(TEN_LOP) else ""
                if t:
                    # ⚠ CO NHÃN CHO VỪA KHUNG. Số bốn chữ số thì lớp nghìn chỉ rộng
                    # MỘT ô, mà chữ "lớp nghìn" ở cỡ 24 rộng gấp rưỡi ô ấy — nhãn
                    # tràn ra ngoài và đè lên khung bên cạnh. Nhìn thì hai khung
                    # dính vào nhau thành một, tức là vẽ ngược hẳn điều đang dạy.
                    # Chỉ lộ khi rút khung hình ra nhìn; video vẫn dựng ra bình
                    # thường, không cổng nào kêu.
                    cho = rong_lop * o - 12
                    co = 24
                    while co > 13 and d.textlength(t, font=phong(co)) > cho:
                        co -= 1
                    g = phong(co)
                    d.text((x + (rong_lop * o - d.textlength(t, font=g)) / 2,
                            y0 - 40 + (24 - co) // 2), t, font=g, fill=TEAL_DARK)
        y = y0 + o + 76
        if c.get("chuPhu"):
            y = giua(d, y, c["chuPhu"], phong(36), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y + 16, c["chuCuoi"], phong(32), TEAL_DARK, rong=W - 200)

    elif L == "goc":
        # ══ GÓC — VẼ RA ĐỂ SO VỚI Ê KE, KHÔNG ĐỂ ĐOÁN BẰNG MẮT ══
        # Cả bài góc đứng ở một ý: MẮT THƯỜNG ĐOÁN SAI. Nên hình này luôn vẽ được
        # cái ê ke đè lên góc — bé thấy cạnh góc chui gọn trong ê ke, trùng khít với
        # ê ke, hay xoè rộng ra ngoài ê ke. Ba cái nhìn ấy chính là ba loại góc, và
        # không cần một con số đo độ nào.
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        do = float(c.get("do", 45))
        cx, cy, dai = W // 2, 470, 300
        if c.get("eKe"):
            # Ê ke vẽ TRƯỚC để nằm dưới hai cạnh góc — cạnh góc phải nhìn thấy rõ.
            e = 150
            d.polygon([(cx, cy), (cx + e, cy), (cx, cy - e)], fill=GOLD_PALE)
            d.line([(cx, cy), (cx + e, cy), (cx, cy - e), (cx, cy)], fill=GOLD, width=5)
            d.rectangle([cx, cy - 26, cx + 26, cy], outline=GOLD, width=4)
            d.text((cx + e + 16, cy - 34), "ê ke", font=phong(28), fill=GOLD_DARK)
        x2 = cx + dai * math.cos(math.radians(do))
        y2 = cy - dai * math.sin(math.radians(do))
        d.line([cx, cy, cx + dai, cy], fill=NAVY, width=8)
        d.line([cx, cy, x2, y2], fill=NAVY, width=8)
        r = 74
        d.arc([cx - r, cy - r, cx + r, cy + r], -do, 0, fill=ALERT, width=6)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=NAVY)
        if c.get("ten"):
            giua(d, cy + 46, c["ten"], phong(44), ALERT, rong=W - 200)
        if c.get("chuPhu"):
            giua(d, cy + (110 if c.get("ten") else 46), c["chuPhu"], phong(34), INK,
                 rong=W - 200)

    elif L == "tam_giac":
        # ══ TAM GIÁC VÀ ĐƯỜNG CAO ══
        # Đường cao không nói bằng lời được. Phải thấy nó ĐI TỪ ĐỈNH XUỐNG ĐÁY và
        # gặp đáy ở một góc vuông. `dinh` là chỗ đứng của đỉnh, tính theo chiều dài
        # đáy — cho `dinh` ra ngoài khoảng không tới một là được ca đường cao RƠI
        # NGOÀI ĐÁY, chỗ bé hay hoảng nhất. Khi ấy đáy phải kéo dài ra mà đón.
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        day, cao, dinh = c.get("day", 8), c.get("cao", 5), float(c.get("dinh", 0.5))
        o = min(64, int(520 / max(day, 1)), int(230 / max(cao, 1)))
        w = day * o
        x0, y_day = (W - w) // 2, 480
        xd, yd = x0 + dinh * w, y_day - cao * o
        d.polygon([(x0, y_day), (x0 + w, y_day), (xd, yd)], fill=TEAL_PALE)
        d.line([(x0, y_day), (x0 + w, y_day), (xd, yd), (x0, y_day)], fill=TEAL_DARK,
               width=6)
        if c.get("duongCao"):
            # Chân rơi NGOÀI đáy — kéo dài đáy ra mà đón. Chỉ vẽ nét đứt trên ĐÚNG
            # PHẦN DÔI RA, đừng phủ lên cạnh đáy thật: lời chú nói "nét đứt là phần
            # đáy kéo dài", mà phủ cả đáy thì hình nói khác lời (bắt ở lớp 5 bài 45).
            if xd > x0 + w:                     # đỉnh lệch sang phải
                t0, t1 = x0 + w, xd
            elif xd < x0:                       # đỉnh lệch sang trái
                t0, t1 = xd, x0
            else:
                t0 = t1 = None
            if t0 is not None:
                for t in range(int(t0), int(t1), 22):
                    d.line([t, y_day, min(t + 11, t1), y_day], fill=MUTE, width=4)
            d.line([xd, yd, xd, y_day], fill=ALERT, width=7)
            ke = 26 if xd <= x0 + w / 2 else -26
            d.rectangle([min(xd, xd + ke), y_day - 26, max(xd, xd + ke), y_day],
                        outline=ALERT, width=4)
            if c.get("nhanCao"):
                d.text((xd + (14 if ke > 0 else -14 - d.textlength(
                    c["nhanCao"], font=phong(32))), (yd + y_day) // 2 - 18),
                    c["nhanCao"], font=phong(32), fill=ALERT)
        if c.get("nhanDay"):
            giua(d, y_day + 20, c["nhanDay"], phong(32), INK, rong=W - 200)
        if c.get("chuPhu"):
            giua(d, y_day + (74 if c.get("nhanDay") else 24), c["chuPhu"], phong(36),
                 INK, rong=W - 180)

    elif L == "hinh_thang":
        # ══ HÌNH THANG, VÀ BỐN VÙNG CỦA HAI ĐƯỜNG CHÉO ══
        # Thêm ngày 17-08 cho lớp 5 bài 48. Cả bài "bốn vùng" gần như KHÔNG dạy được
        # bằng lời: phải thấy hai đường chéo cắt nhau chia hình thành bốn mảnh, và
        # thấy hai mảnh BÊN nằm đối xứng nhau. Không có hình thì bé chỉ còn cách học
        # thuộc bốn con số.
        #
        # `dayLon` nằm dưới, `dayBe` căn giữa ở trên — đúng cách sách giáo khoa vẽ.
        # `duongCheo=True` kẻ hai đường chéo và chấm giao điểm; `nhanCao` thì vẽ thêm
        # đường cao nét đứt kèm ô vuông góc.
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        d_lon, d_be = c.get("dayLon", 8), c.get("dayBe", 4)
        cao = c.get("cao", 5)
        o = min(64, int(560 / max(d_lon, 1)), int(210 / max(cao, 1)))
        y_duoi, h = 460, cao * o
        y_tren = y_duoi - h
        xl0 = (W - d_lon * o) // 2
        xl1 = xl0 + d_lon * o
        xb0 = (W - d_be * o) // 2
        xb1 = xb0 + d_be * o
        d.polygon([(xl0, y_duoi), (xl1, y_duoi), (xb1, y_tren), (xb0, y_tren)],
                  fill=TEAL_PALE)
        d.line([(xl0, y_duoi), (xl1, y_duoi), (xb1, y_tren), (xb0, y_tren),
                (xl0, y_duoi)], fill=TEAL_DARK, width=6)
        if c.get("duongCheo"):
            d.line([xl0, y_duoi, xb1, y_tren], fill=ALERT, width=5)
            d.line([xl1, y_duoi, xb0, y_tren], fill=ALERT, width=5)
            # Giao điểm hai đường chéo — chấm cho bé chỉ tay vào được.
            #
            # ⚠ Tỉ này rất dễ viết ngược, và viết ngược thì chấm rơi lệch hẳn khỏi chỗ
            # hai nét cắt nhau (đã dính khi mới viết nhánh này). Hai tam giác kề hai
            # đáy đồng dạng với tỉ dayBe : dayLon, nên giao điểm cách đáy BÉ một phần
            # dayBe và cách đáy LỚN một phần dayLon — tức nó nằm GẦN đáy bé hơn.
            gx = W / 2
            gy = y_duoi - h * d_lon / max(d_be + d_lon, 1)
            d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], fill=ALERT)
        if c.get("nhanCao"):
            xc = xb0 + 34
            for t in range(int(y_tren), int(y_duoi), 18):
                d.line([xc, t, xc, min(t + 9, y_duoi)], fill=MUTE, width=4)
            d.rectangle([xc, y_duoi - 24, xc + 24, y_duoi], outline=MUTE, width=4)
            f = phong(30)
            # Nhãn sát ngay đường cao — đặt xa ra là chạm cạnh xiên khi đáy bé ngắn.
            d.text((xc + 14, (y_tren + y_duoi) // 2 - 18), c["nhanCao"], font=f,
                   fill=MUTE)
        g = phong(30)
        if c.get("nhanDayBe"):
            giua(d, y_tren - 44, c["nhanDayBe"], g, TEAL_DARK, rong=W - 200)
        if c.get("nhanDayLon"):
            giua(d, y_duoi + 16, c["nhanDayLon"], g, TEAL_DARK, rong=W - 200)
        if c.get("chuPhu"):
            giua(d, y_duoi + 64, c["chuPhu"], phong(36), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y_duoi + 124, c["chuCuoi"], phong(32), TEAL_DARK, rong=W - 200)

    elif L == "hinh_tron":
        # ══ HÌNH TRÒN — BÁN KÍNH VÀ ĐƯỜNG KÍNH ══
        # `dayLech` vẽ thêm một dây KHÔNG qua tâm. Đó là cả chỗ hay nhầm của bài:
        # bé căng dây từ mép này sang mép kia rồi gọi luôn là đường kính. Vẽ hai dây
        # cạnh nhau thì thấy ngay dây lệch tâm NGẮN HƠN — khỏi phải cãi.
        giua(d, 44, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        cx, cy, r = W // 2, 400, 190
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL_DARK, width=6)
        if c.get("rTrong"):
            # ══ VÀNH KHĂN — vòng trong ĐỒNG TÂM ══
            # Thêm 17-08 cho lớp 5 bài 50. Cả bài đứng ở chỗ "vành khăn là hiệu HAI
            # diện tích", và bẫy của nó là công thức giả lấy hiệu hai bán kính rồi
            # bình phương. Vẽ hai vòng đồng tâm thì bé thấy ngay: trong hình chẳng có
            # đường tròn nào bán kính bằng hiệu ấy cả.
            #
            # Khai bằng TỈ LỆ so với vòng ngoài (0 tới 1), để hai vòng luôn chung một
            # thước — khai bằng số đo thật thì tỉ trên màn sai, vành rộng hẹp tuỳ ý.
            rt = r * float(c["rTrong"])
            d.ellipse([cx - rt, cy - rt, cx + rt, cy + rt], outline=GOLD, width=6)
        if c.get("dayLech"):
            dy = 116
            x = math.sqrt(r * r - dy * dy)
            d.line([cx - x, cy - dy, cx + x, cy - dy], fill=MUTE, width=6)
            d.text((cx + x + 14, cy - dy - 20), c.get("nhanLech", "dây lệch tâm"),
                   font=phong(28), fill=MUTE)
        if c.get("hienD"):
            d.line([cx - r, cy, cx + r, cy], fill=GOLD, width=8)
        if c.get("hienR"):
            d.line([cx, cy, cx + r, cy], fill=ALERT, width=8)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=NAVY)
        d.text((cx - 66, cy + 18), "tâm", font=phong(28), fill=NAVY)
        f = phong(32)
        if c.get("nhanR"):
            t = c["nhanR"]
            d.text((cx + r / 2 - d.textlength(t, font=f) / 2, cy - 46), t, font=f,
                   fill=ALERT)
        if c.get("nhanD"):
            t = c["nhanD"]
            d.text((cx - d.textlength(t, font=f) / 2, cy + r + 16), t, font=f,
                   fill=GOLD_DARK)
        if c.get("chuPhu"):
            giua(d, cy + r + 66, c["chuPhu"], phong(36), INK, rong=W - 180)

    elif L == "duong_di":
        # ══ ĐOẠN ĐƯỜNG VÀ HAI MŨI TÊN ══
        # Cả chương chuyển động đứng hay đổ ở MỘT câu hỏi: hai bên đi cùng chiều hay
        # đối đầu? Cùng chiều thì mỗi giờ khoảng cách co lại bằng HIỆU vận tốc, đối
        # đầu thì bằng TỔNG. Hai đề chỉ khác đúng hai chữ ở cuối câu, nên đọc lướt là
        # chia nhầm — mà chia nhầm thì không có gì kêu lên cả.
        #
        # Vẽ hai mũi tên ra thì bé KHÔNG CẦN đọc kỹ nữa: hai mũi cùng quay phải là
        # đuổi, chụm đầu vào nhau là gặp. `xe1Huong` · `xe2Huong` nhận 'phai' hoặc
        # 'trai'; `xe1Dau` · `xe2Dau` là chỗ xuất phát, tính theo TỈ LỆ trên đoạn.
        #
        # `toTu` · `toDen` tô một khúc — dùng cho bài xuất phát khác giờ, khúc tô là
        # đoạn người trước đã đi xong trước khi người sau lên đường. `sao` đánh dấu
        # điểm gặp.
        giua(d, 40, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        x0, x1, y = 150, 1130, 330
        span = x1 - x0

        def px(f):
            return x0 + span * float(f)

        if c.get("toDen") is not None:
            d.rectangle([px(c.get("toTu", 0)), y - 22, px(c["toDen"]), y + 22],
                        fill=GOLD_PALE)
            if c.get("nhanTo"):
                giua(d, y - 62, c["nhanTo"], phong(30), GOLD_DARK, rong=W - 200)
        d.line([x0, y, x1, y], fill=TEAL_DARK, width=8)
        f_d = phong(36, dam=True)
        for xx, ten, lech in ((x0, c.get("dauA", "A"), -1), (x1, c.get("dauB", "B"), 1)):
            d.line([xx, y - 34, xx, y + 34], fill=TEAL_DARK, width=8)
            t = str(ten)
            w_ = d.textlength(t, font=f_d)
            # Tên đầu đoạn không phải lúc nào cũng là MỘT CHỮ CÁI. "người sau" ·
            # "người trước" thì lề hai bên không chứa nổi: đặt theo lối cũ là chữ
            # tràn ra ngoài mép màn hình, kẹp lại thì nó đè lên chính vạch đường.
            # Nên tên dài thì cho leo LÊN TRÊN vạch đầu đoạn.
            le = (x0 if lech < 0 else W - x1) - 16
            if w_ + 26 <= le:
                d.text((xx - w_ / 2 + lech * (w_ / 2 + 26), y - 24), t, font=f_d,
                       fill=TEAL_DARK)
            else:
                d.text((min(max(xx - w_ / 2, 16), W - 16 - w_), y - 78), t,
                       font=f_d, fill=TEAL_DARK)
        if c.get("sao") is not None:
            xs = px(c["sao"])
            d.ellipse([xs - 16, y - 16, xs + 16, y + 16], fill=ALERT)
            if c.get("nhanSao"):
                t = c["nhanSao"]
                f_s = phong(30)
                w_ = d.textlength(t, font=f_s)
                d.text((min(max(xs - w_ / 2, 20), W - 20 - w_), y + 28), t,
                       font=f_s, fill=ALERT)

        def mui_ten(yy, dau, huong, nhan, mau):
            if dau is None:
                return
            xs, sang_phai = px(dau), huong != "trai"
            # Mũi tên của người xuất phát ngay ở đầu đoạn chạy quá mép màn hình —
            # kẹp lại, thà ngắn còn hơn cụt đầu.
            xe = min(xs + 170, W - 24) if sang_phai else max(xs - 170, 24)
            d.line([xs, yy, xe, yy], fill=mau, width=8)
            k = 20 if sang_phai else -20
            d.polygon([(xe, yy), (xe - k, yy - 14), (xe - k, yy + 14)], fill=mau)
            d.line([xs, yy - 18, xs, yy + 18], fill=mau, width=5)
            if nhan:
                f_n = phong(28)
                w_ = d.textlength(nhan, font=f_n)
                d.text((min(max(min(xs, xe), 20), W - 20 - w_), yy - 48), nhan,
                       font=f_n, fill=mau)

        mui_ten(y - 100, c.get("xe1Dau"), c.get("xe1Huong", "phai"),
                c.get("xe1Nhan"), NAVY)
        mui_ten(y + 118, c.get("xe2Dau"), c.get("xe2Huong", "trai"),
                c.get("xe2Nhan"), GOLD_DARK)

        y_cuoi = y + 170
        if c.get("nhanDai"):
            d.line([x0, y_cuoi, x1, y_cuoi], fill=MUTE, width=3)
            for xn in (x0, x1):
                d.line([xn, y_cuoi - 10, xn, y_cuoi + 10], fill=MUTE, width=3)
            y_cuoi = giua(d, y_cuoi + 10, c["nhanDai"], phong(32), MUTE,
                          rong=W - 200)
        if c.get("chuPhu"):
            y_cuoi = giua(d, y_cuoi + 14, c["chuPhu"], phong(36), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y_cuoi + 12, c["chuCuoi"], phong(30), TEAL_DARK, rong=W - 200)

    elif L == "tam_giac_ct":
        # ══ TAM GIÁC CÔNG THỨC — CHE Ô CẦN TÌM LÀ LỘ PHÉP TÍNH ══
        # Đây KHÔNG phải hình tam giác của hình học; nó là cách xếp ba đại lượng để
        # ba công thức rời thành một. Ô trên chia cho ô dưới, hai ô dưới nhân nhau —
        # nên che ô nào thì phần còn lại tự đọc ra phép tính cho ô ấy.
        #
        # Chương chuyển động đứng hay đổ ở chỗ này: nói bằng lời thì bé phải thuộc ba
        # công thức và rất hay nhân chỗ đáng chia. Vẽ ra thì chỉ còn một hình.
        # `che` nhận 'tren' · 'trai' · 'phai' — ô bị che tô vàng và hiện dấu hỏi.
        giua(d, 40, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        cx, y0, b, h = W // 2, 130, 210, 280
        ym = y0 + h * 0.45                       # vạch ngang chia tầng trên · dưới
        bm = b * 0.45                            # nửa bề ngang tại vạch ấy
        y1 = y0 + h
        vung = {
            "tren": ([(cx, y0), (cx - bm, ym), (cx + bm, ym)],
                     (cx, y0 + h * 0.26)),
            "trai": ([(cx - bm, ym), (cx, ym), (cx, y1), (cx - b, y1)],
                     (cx - b * 0.38, y0 + h * 0.76)),
            "phai": ([(cx, ym), (cx + bm, ym), (cx + b, y1), (cx, y1)],
                     (cx + b * 0.38, y0 + h * 0.76)),
        }
        che = c.get("che")
        if che in vung:
            d.polygon(vung[che][0], fill=GOLD)
        d.line([(cx, y0), (cx + b, y1), (cx - b, y1), (cx, y0)],
               fill=TEAL_DARK, width=6, joint="curve")
        d.line([cx - bm, ym, cx + bm, ym], fill=TEAL, width=5)
        d.line([cx, ym, cx, y1], fill=TEAL, width=5)
        fo = phong(52, dam=True)
        for ten, khoa in (("tren", "tren"), ("trai", "traiDuoi"),
                          ("phai", "phaiDuoi")):
            chu = "?" if ten == che else str(c.get(khoa, ""))
            if not chu:
                continue
            tx, ty = vung[ten][1]
            d.text((tx - d.textlength(chu, font=fo) / 2, ty - 34), chu,
                   font=fo, fill=GOLD_DARK if ten == che else NAVY)
        y_cuoi = y1 + 26
        if c.get("chuPhu"):
            y_cuoi = giua(d, y_cuoi, c["chuPhu"], phong(38), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y_cuoi + 18, c["chuCuoi"], phong(32), TEAL_DARK, rong=W - 200)

    elif L == "khoi":
        # ══ KHỐI HỘP — BA CÁCH NHÌN CÙNG MỘT CÁI HỘP ══
        # `trai` trải phẳng ra sáu mặt, TÔ MÀU THEO CẶP: hai mặt cùng màu là hai mặt
        #        đối diện, bằng nhau. Cả bài nằm trong cách tô ấy.
        # `ao`   bóc RIÊNG bốn mặt bên rồi trải thành MỘT HÀNG — xem chú thích ở
        #        nhánh ấy; đó là hình của bài diện tích xung quanh.
        # `chong` xếp các tầng chồng lên nhau — cho thấy hình khối trông thế nào.
        # `tang`  tách rời từng tầng ra cạnh nhau — cho thấy CÁCH ĐẾM.
        # Vẽ được `khuyet` là số khối bị nhấc đi ở mỗi tầng, cho ca khối bị khoét.
        giua(d, 40, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        dai, rong, cao = c.get("dai", 4), c.get("rong", 3), c.get("cao", 2)
        kieu = c.get("kieu", "chong")

        def luoi(x, y, cot, hang, o, nen, vien, bo_bot=0):
            """Một tầng: `cot` nhân `hang` ô, bỏ bớt `bo_bot` ô ở cuối."""
            n = cot * hang
            for i in range(n - bo_bot):
                the(d, x + (i % cot) * o, y + (i // cot) * o, o, o,
                    nen=nen, vien=vien, day=2, bo=0)

        if kieu == "ao":
            # ══ TẤM ÁO: BỐN MẶT BÊN TRẢI THÀNH MỘT HÀNG ══
            # Nhánh `trai` bày sáu mặt theo hình chữ thập — đúng cái hộp, nhưng bốn
            # mặt bên nằm rời ba chỗ, nên nó KHÔNG kể được điều bài này dạy: bóc bốn
            # mặt bên ra thì chúng nối thành MỘT tấm chữ nhật, chiều dài đúng bằng
            # chu vi đáy. Ở đây xếp chúng liền nhau theo đúng vòng quanh hộp —
            # trước · hông · sau · hông — rồi kẻ ngoặc đo suốt chiều dài. Bé ĐẾM
            # được bốn khúc cộng lại thành vòng eo, thay vì phải tin lời.
            #
            # `hangNap` bày thêm hai mặt nắp và đáy rời ra bên dưới — đó là chỗ khác
            # nhau giữa xung quanh và toàn phần. `boMat` là danh sách tên mặt KHÔNG
            # có thật (thùng không nắp, sàn không quét): mặt ấy vẫn vẽ nhưng gạch
            # chéo, vì bài đứng hay đổ ở chỗ ĐẾM MẶT CỦA VẬT THẬT.
            bo_mat = set(c.get("boMat") or [])
            g = phong(26)

            def mat_phang(x, y, w_, h_, ten, nen, vien):
                """Một mặt. Mặt bị bỏ thì trắng, viền xám và gạch chéo đỏ."""
                mat_bo = ten in bo_mat
                the(d, x, y, w_, h_, nen="#FFFFFF" if mat_bo else nen,
                    vien=MUTE if mat_bo else vien, day=4, bo=0)
                # Tên mặt bị bỏ phải nằm NGOÀI ô: đặt vào giữa như mặt còn lại thì
                # hai vạch chéo cắt ngang chữ, đọc không ra. Bắt được khi rút khung
                # hình bài 51 M2 — chữ "nắp" bị gạch nát.
                if mat_bo:
                    d.line([x, y, x + w_, y + h_], fill=ALERT, width=5)
                    d.line([x + w_, y, x, y + h_], fill=ALERT, width=5)
                    # `loiBo` nói mặt ấy bị bỏ VÌ SAO. Mặc định "KHÔNG có" hợp với
                    # thùng không nắp, nhưng sàn phòng thì VẪN CÓ, chỉ là không
                    # quét vôi — để mặc định ở đấy là hình nói sai.
                    ten = f"{ten} — {c.get('loiBo', 'KHÔNG có')}"
                d.text((x + (w_ - d.textlength(ten, font=g)) / 2,
                        y + h_ + 8 if mat_bo else y + h_ / 2 - 16),
                       ten, font=g, fill=MUTE if mat_bo else INK)

            chu_vi = 2 * (dai + rong)
            o = min(52, int(940 / max(chu_vi, 1)), int(170 / max(cao, 1)))
            w, h = chu_vi * o, cao * o
            x0, y0 = (W - w) // 2, 150
            x = x0
            for a, ten, nen, vien in ((dai, "trước", GOLD_PALE, GOLD),
                                      (rong, "hông", TEAL_PALE, TEAL),
                                      (dai, "sau", GOLD_PALE, GOLD),
                                      (rong, "hông", TEAL_PALE, TEAL)):
                mat_phang(x, y0, a * o, h, ten, nen, vien)
                x += a * o
            d.rectangle([x0, y0, x0 + w, y0 + h], outline=TEAL_DARK, width=5)

            yb = y0 + h + 26                      # ngoặc đo suốt tấm áo
            d.line([x0, yb, x0 + w, yb], fill=NAVY, width=4)
            for xn in (x0, x0 + w):
                d.line([xn, yb - 12, xn, yb + 12], fill=NAVY, width=4)
            y_cuoi = yb + 14
            if c.get("nhanDai"):
                y_cuoi = giua(d, yb + 14, c["nhanDai"], phong(32), NAVY, rong=W - 200)
            if c.get("nhanCao"):
                fc = phong(32)
                d.text((x0 - 22 - d.textlength(c["nhanCao"], font=fc),
                        y0 + h / 2 - 18), c["nhanCao"], font=fc, fill=INK)

            if c.get("hangNap"):
                o2 = min(o, int(110 / max(rong, 1)), int(300 / max(dai, 1)))
                wn, hn = dai * o2, rong * o2
                yn = y_cuoi + 22
                for i, ten in enumerate((c.get("nhanNap", "nắp"),
                                         c.get("nhanDay", "đáy"))):
                    mat_phang(W // 2 - wn - 30 + i * (wn + 60), yn, wn, hn,
                              ten, TEAL_PALE, TEAL)
                # Chừa chỗ cho dòng tên nằm dưới ô khi có mặt bị gạch.
                y_cuoi = yn + hn + (32 if bo_mat else 0)
            # `chuPhu` · `chuCuoi` do đuôi chung của nhánh `khoi` vẽ, không vẽ lại.

        elif kieu == "trai":
            o = min(58, int(620 / (dai + 2 * cao)), int(400 / (2 * rong + 2 * cao)))
            tw, th = (dai + 2 * cao) * o, (2 * rong + 2 * cao) * o
            x0, y0 = (W - tw) // 2, 122
            xd, yd = x0 + cao * o, y0 + (rong + cao) * o          # ô đáy nằm giữa
            mat = [(xd, y0, dai, rong, TEAL_PALE, TEAL, "nắp"),
                   (xd, y0 + rong * o, dai, cao, GOLD_PALE, GOLD, "sau"),
                   (xd, yd, dai, rong, TEAL_PALE, TEAL, "đáy"),
                   (xd, yd + rong * o, dai, cao, GOLD_PALE, GOLD, "trước"),
                   (x0, yd, cao, rong, "#FFFFFF", MUTE, "hông"),
                   (xd + dai * o, yd, cao, rong, "#FFFFFF", MUTE, "hông")]
            g = phong(26)
            for x, y, a, b, nen, vien, ten in mat:
                the(d, x, y, a * o, b * o, nen=nen, vien=vien, day=4, bo=0)
                d.text((x + (a * o - d.textlength(ten, font=g)) / 2,
                        y + b * o / 2 - 16), ten, font=g, fill=INK)
            y_cuoi = y0 + th
        else:
            o = min(46, int(200 / max(dai, 1)), int(150 / max(rong, 1)))
            kh = list(c.get("khuyet") or [0] * cao)
            if kieu == "tang":
                g = phong(30)
                cach = dai * o + 78
                x0 = (W - (cach * cao - 78)) // 2
                for j in range(cao):
                    x = x0 + j * cach
                    luoi(x, 250, dai, rong, o, TEAL_PALE, TEAL, kh[j])
                    d.text((x + (dai * o - d.textlength(f"Tầng {j + 1}", font=g)) / 2,
                            250 - 46), f"Tầng {j + 1}", font=g, fill=NAVY)
                    n = dai * rong - kh[j]
                    t = f"{n} khối"
                    d.text((x + (dai * o - d.textlength(t, font=g)) / 2,
                            250 + rong * o + 16), t, font=g, fill=TEAL_DARK)
                y_cuoi = 250 + rong * o + 70
            else:
                # ══ XẾP KHỐI THEO LỐI HÌNH HỘP ══
                # Bản đầu vẽ mấy tầng là mấy cái LƯỚI PHẲNG đè lệch nhau. Nhìn ra
                # đúng cái nó là: mấy tấm lưới chồng lên nhau, không ra hình khối —
                # mà bài này bé phải THẤY được khối đặc thì mới hiểu vì sao đếm theo
                # tầng. Nay mỗi khối nhỏ vẽ đủ ba mặt: mặt trên, mặt trái, mặt phải.
                #
                # Thứ tự vẽ là chỗ dễ hỏng nhất: vẽ sai thứ tự thì khối đằng sau đè
                # lên khối đằng trước, hình lộn ngược mà vẫn ra hình. Vẽ theo ĐỘ SÂU
                # i cộng j cộng k tăng dần — xa vẽ trước, gần vẽ sau, gần đè lên xa.
                a = min(42, int(560 / (dai + rong)), int(150 / max(cao, 1)))
                bb, hh = a * 0.58, a * 1.12
                ox = W // 2 + int((rong - dai) * a / 2)
                oy = 250
                khoi_ = [(i, j, k) for k in range(cao) for j in range(rong)
                         for i in range(dai)
                         if (j * dai + i) < dai * rong - kh[k]]
                for i, j, k in sorted(khoi_, key=lambda t: t[0] + t[1] + t[2]):
                    x = ox + (i - j) * a
                    y = oy + (i + j) * bb - k * hh
                    d.polygon([(x, y), (x + a, y + bb), (x, y + 2 * bb),
                               (x - a, y + bb)], fill=TEAL_PALE, outline=TEAL_DARK)
                    d.polygon([(x - a, y + bb), (x, y + 2 * bb),
                               (x, y + 2 * bb + hh), (x - a, y + bb + hh)],
                              fill="#FFFFFF", outline=TEAL_DARK)
                    d.polygon([(x, y + 2 * bb), (x + a, y + bb),
                               (x + a, y + bb + hh), (x, y + 2 * bb + hh)],
                              fill=SOFT, outline=TEAL_DARK)
                y_cuoi = int(oy + (dai + rong) * bb + hh + 20)
        if c.get("chuPhu"):
            y_cuoi = giua(d, y_cuoi + 20, c["chuPhu"], phong(36), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y_cuoi + 18, c["chuCuoi"], phong(32), TEAL_DARK, rong=W - 200)

    elif L == "phan_so":
        # ══ PHÂN SỐ VẼ RA THÀNH BĂNG CHIA PHẦN ══
        # Cả chương phân số đứng hay đổ ở chỗ này: bé phải THẤY mẫu số là "chia làm
        # mấy phần" và tử số là "lấy mấy phần". Nói bằng lời thì hai chữ tử với mẫu
        # chỉ là hai cái tên khó nhớ; vẽ ra thì chúng có nghĩa ngay.
        #
        # Vẽ được một băng hoặc hai băng chồng nhau — hai băng là để SO SÁNH, và khi
        # so sánh thì hai băng phải DÀI BẰNG NHAU, nếu không thì hình nói dối.
        giua(d, 46, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        cap = [(c.get("tu"), c.get("mau"), c.get("nhan", ""))]
        if c.get("mau2"):
            cap.append((c.get("tu2"), c.get("mau2"), c.get("nhan2", "")))
        rong_bang, x0 = 620, 340
        y = 190 if len(cap) > 1 else 250
        for tu, mau, nhan in cap:
            if not mau:
                continue
            cao, b = 86, rong_bang / mau
            for i in range(mau):
                to = i < (tu or 0)
                the(d, x0 + i * b, y, b, cao, nen=TEAL_PALE if to else "#FFFFFF",
                    vien=TEAL if to else LINE, day=4 if to else 3, bo=0)
            if nhan:
                f = phong(40)
                d.text((x0 - 26 - d.textlength(nhan, font=f), y + 20), nhan,
                       font=f, fill=TEAL_DARK)
            # phân số viết bên phải băng, dạng tử trên mẫu có gạch ngang
            g = phong(34)
            xc = x0 + rong_bang + 34
            for k, t in enumerate((str(tu), str(mau))):
                d.text((xc + (30 - d.textlength(t, font=g)) / 2, y + k * 44 + 2), t,
                       font=g, fill=NAVY)
            d.line([xc, y + 44, xc + 30, y + 44], fill=NAVY, width=4)
            y += 152
        if c.get("chuPhu"):
            giua(d, y + 22, c["chuPhu"], phong(36), INK, rong=W - 180)
        if c.get("chuCuoi"):
            giua(d, y + 92, c["chuCuoi"], phong(32), TEAL_DARK, rong=W - 200)

    elif L == "so_do_ven":
        # ══ SƠ ĐỒ VEN — HAI VÒNG GIAO NHAU ══
        # Bài này chỉ có một ý, và ý ấy KHÔNG nói bằng lời được: phần giao bị đếm HAI
        # LẦN nên phải trừ đi một lần. Vẽ hai vòng chồng nhau thì bé nhìn thấy ngay
        # cái phần bị đếm đúp ấy nằm ở đâu.
        giua(d, 46, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        r = 168
        cx1, cx2, cy = W // 2 - 112, W // 2 + 112, 300
        d.ellipse([cx1 - r, cy - r, cx1 + r, cy + r], outline=TEAL, width=6)
        d.ellipse([cx2 - r, cy - r, cx2 + r, cy + r], outline=GOLD, width=6)
        f = phong(34)
        for x, nhan, mau in ((cx1 - r + 10, c.get("tenA", ""), TEAL_DARK),
                             (cx2 + r - 10, c.get("tenB", ""), GOLD_DARK)):
            if nhan:
                w = d.textlength(nhan, font=f)
                d.text((x - (w if x > W // 2 else 0), cy - r - 46), nhan, font=f, fill=mau)
        # Ba con số: chỉ A, cả hai, chỉ B — đặt đúng ba vùng của hình.
        g = phong(46)
        for x, t, mau in ((cx1 - 96, c.get("chiA", ""), TEAL_DARK),
                          (W // 2, c.get("caHai", ""), ALERT),
                          (cx2 + 96, c.get("chiB", ""), GOLD_DARK)):
            if t:
                d.text((x - d.textlength(str(t), font=g) / 2, cy - 24), str(t),
                       font=g, fill=mau)
        if c.get("chuGiao"):
            giua(d, cy + r + 18, c["chuGiao"], phong(30), ALERT, rong=W - 200)
        if c.get("chuPhu"):
            giua(d, cy + r + (72 if c.get("chuGiao") else 24), c["chuPhu"], phong(36),
                 INK, rong=W - 180)

    elif L == "so_do_doan":
        # ══ SƠ ĐỒ ĐOẠN THẲNG ══
        # Bác dặn riêng: chương tổng - hiệu thì **vẽ kiểu đoạn thẳng**. Nên đây là
        # đoạn thẳng thật — hai vạch nằm ngang có ngoặc hai đầu, đúng cách sách giáo
        # khoa vẽ, chứ không phải cột hay ô vuông.
        #
        #   Số bé   ├──────────┤              ⎫
        #                                      ⎬ tổng
        #   Số lớn  ├──────────┼────┤         ⎭
        #                       hiệu
        #
        # Toàn bộ chương này chứng minh bằng hình: thêm HIỆU vào đoạn ngắn thì hai
        # đoạn bằng nhau, nên hai lần số lớn bằng tổng cộng hiệu. Bớt HIỆU khỏi đoạn
        # dài thì cũng thế, nên hai lần số bé bằng tổng trừ hiệu. Không có hình thì
        # hai công thức ấy chỉ còn là hai câu phải học thuộc.
        giua(d, 46, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        be, lon = c.get("be", 0), c.get("lon", 0)
        x0, rong_toi_da = 300, 640
        # ⚠ HAI MÀN ĐẶT CẠNH NHAU THÌ PHẢI CHUNG MỘT THANG ĐO.
        #
        # Mặc định mỗi màn tự chuẩn hoá theo đoạn dài nhất CỦA NÓ — hợp lý khi màn
        # đứng một mình. Nhưng cả chương này hay đặt hai màn cạnh nhau để nói "cái
        # này KHÔNG đổi": tuổi mẹ con hôm nay và sau 5 năm, hiệu vẫn 24. Nếu mỗi màn
        # một thang thì khúc hiệu 24 vẽ ở màn sau NGẮN HƠN màn trước — hình nói ngược
        # lại đúng cái điều lời đang dạy. Lỗi thật, bắt được ở lớp 5 bài 28.
        #
        # Khai `thangDo` bằng giá trị lớn nhất của CẢ CỤM màn thì mọi màn cùng thước.
        don_vi = rong_toi_da / max(c.get("thangDo") or 0, lon, be, 1)
        y_be, y_lon, day_net = 210, 340, 9

        def vach_phan(y, dai, so_phan, mau):
            """Chia một đoạn thành `so_phan` phần bằng nhau bằng vạch đứng.

            Đây là hình của chương tỉ số: nói "tỉ số hai trên năm" thì bé chưa hình
            dung được gì, nhưng thấy đoạn ngắn chia hai phần và đoạn dài chia năm
            phần — mà mọi phần đều bằng nhau — thì hiểu ngay. Và cũng nhìn ra luôn
            tổng gồm bảy phần, hiệu gồm ba phần.
            """
            if not so_phan or so_phan < 2:
                return
            b = dai / so_phan
            for i in range(1, so_phan):
                d.line([x0 + i * b, y - 13, x0 + i * b, y + 13], fill=mau, width=7)

        def doan(y, dai, mau, nhan_trai, net=day_net, dut=False):
            x1 = x0 + dai
            if dut:                                   # đoạn thêm vào: vẽ nét đứt
                for x in range(int(x0), int(x1), 20):
                    d.line([x, y, min(x + 11, x1), y], fill=mau, width=net)
            else:
                d.line([x0, y, x1, y], fill=mau, width=net)
            for x in (x0, x1):                        # ngoặc hai đầu
                d.line([x, y - 17, x, y + 17], fill=mau, width=5)
            if nhan_trai:
                f = phong(30)
                d.text((x0 - 22 - d.textlength(nhan_trai, font=f), y - 17),
                       nhan_trai, font=f, fill=MUTE)
            return x1

        # ── đoạn ngắn ──
        x_be = doan(y_be, be * don_vi, TEAL_DARK, c.get("nhanBe", "Số bé"))
        vach_phan(y_be, be * don_vi, c.get("phanBe"), "#FFFFFF")
        if c.get("themVaoBe"):
            # Thêm hiệu vào đoạn ngắn cho bằng đoạn dài — nét đứt vàng.
            x2 = x0 + lon * don_vi
            for x in range(int(x_be), int(x2), 20):
                d.line([x, y_be, min(x + 11, x2), y_be], fill=GOLD, width=day_net)
            d.line([x2, y_be - 17, x2, y_be + 17], fill=GOLD, width=5)
            # Nhãn đặt ngay TRÊN phần vừa thêm, không căn giữa cả màn — nó đang chỉ
            # vào đúng một đoạn, để giữa màn thì bé không biết nó nói về chỗ nào.
            f, nhan = phong(28), "thêm hiệu vào cho bằng"
            d.text((min(max((x_be + x2) / 2 - d.textlength(nhan, font=f) / 2, 20),
                        W - 20 - d.textlength(nhan, font=f)), y_be - 62),
                   nhan, font=f, fill=GOLD_DARK)

        # ── đoạn dài, phần dôi ra tô vàng ──
        x_lon = doan(y_lon, lon * don_vi, TEAL_DARK, c.get("nhanLon", "Số lớn"))
        vach_phan(y_lon, lon * don_vi, c.get("phanLon"), "#FFFFFF")
        if c.get("hienHieu") and lon > be:
            xa = x0 + be * don_vi
            mau_hieu = ALERT if c.get("botOLon") else GOLD
            d.line([xa, y_lon, x_lon, y_lon], fill=mau_hieu, width=day_net + 4)
            d.line([xa, y_lon - 17, xa, y_lon + 17], fill=mau_hieu, width=5)
            nhan = c.get("chuHieu", "hiệu")
            f = phong(28)
            giua_x = (xa + x_lon) / 2
            d.text((giua_x - d.textlength(nhan, font=f) / 2, y_lon + 26), nhan,
                   font=f, fill=ALERT if c.get("botOLon") else GOLD_DARK)

        # ── ngoặc tổng, ôm cả hai đoạn ──
        if c.get("chuTong"):
            xb = x0 + max(be, lon) * don_vi + 46
            d.line([xb, y_be, xb, y_lon], fill=NAVY, width=5)
            for y in (y_be, y_lon):
                d.line([xb - 16, y, xb, y], fill=NAVY, width=5)
            # Nhãn tổng nằm bên PHẢI ngoặc, mà lề bên ấy chỉ còn hơn hai trăm điểm.
            # Nhãn dài hơn thế thì chảy ra ngoài mép và bị xén — bắt được ở bài 55
            # M2 ("tổng 24 = 2 lần V thực" mất luôn chữ cuối). Nay ngắt dòng cho vừa
            # lề, rồi xếp cả cụm dòng ấy cân giữa ngoặc.
            f = phong(30)
            rong_le = W - 16 - (xb + 16)
            dong = ngat_dong(d, c["chuTong"], f, rong_le)
            b_dong = int(f.size * 1.3)
            y_bd = (y_be + y_lon) / 2 - b_dong * len(dong) / 2
            for i, dg in enumerate(dong):
                d.text((xb + 16, y_bd + i * b_dong), dg, font=f, fill=NAVY)

        if c.get("chuPhu"):
            giua(d, 470, c["chuPhu"], phong(36), INK, rong=W - 160)
        if c.get("chuCuoi"):
            giua(d, 546, c["chuCuoi"], phong(34), TEAL_DARK, rong=W - 200)

    elif L == "san_bang":
        # ══ TRUNG BÌNH CỘNG, NHÌN THẤY ĐƯỢC ══
        # Luật 9 của bác. "Trung bình cộng" nói bằng lời thì mãi vẫn là một phép chia
        # khô khốc. Vẽ ra thành mấy cột cao thấp rồi SAN CHO BẰNG NHAU thì bé thấy
        # ngay nó là cái gì: cột cao nhường cho cột thấp, cuối cùng ai cũng như ai.
        #
        # `so` là chiều cao từng cột. `deu=True` vẽ trạng thái ĐÃ SAN — tất cả bằng
        # trung bình. `mucTB=True` kẻ một vạch ngang ở mức trung bình, để bé thấy
        # phần nhô lên trên vạch đúng bằng phần hụt xuống dưới.
        giua(d, 50, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        so = c.get("so", [])
        n = len(so)
        tb = sum(so) / n if n else 0
        hien = [tb] * n if c.get("deu") else so
        day, cao_toi_da = 500, 250          # đáy cột và chiều cao tối đa
        don_vi = cao_toi_da / max(max(so), 1)
        rong_cot, cach = 96, 46
        tong = n * rong_cot + (n - 1) * cach
        x0 = (W - tong) // 2
        if c.get("mucTB"):
            y_tb = day - tb * don_vi
            # Nhãn nằm TRÊN vạch, ở đầu trái — bản đầu đặt nó ngay cuối vạch nên chữ
            # chồng lên mấy nét đứt cuối, đọc rối đúng chỗ cần nhìn rõ nhất.
            for x in range(x0 - 34, x0 + tong + 34, 18):   # vạch đứt
                d.line([x, y_tb, x + 10, y_tb], fill=GOLD, width=4)
            d.text((x0 - 34, y_tb - 40), "mức trung bình", font=phong(26),
                   fill=GOLD_DARK)
        for i, v in enumerate(hien):
            x = x0 + i * (rong_cot + cach)
            h = v * don_vi
            the(d, x, day - h, rong_cot, max(h, 6), nen=TEAL_PALE, vien=TEAL, day=4, bo=12)
            f, t = phong(38), str(int(v) if float(v).is_integer() else round(v, 1))
            d.text((x + (rong_cot - d.textlength(t, font=f)) / 2, day - h - 46), t,
                   font=f, fill=TEAL_DARK)
            if c.get("deu"):                # nhắc lại số gốc dưới chân cột
                g, t2 = phong(26), str(so[i])
                d.text((x + (rong_cot - d.textlength(t2, font=g)) / 2, day + 12), t2,
                       font=g, fill=MUTE)
        if c.get("chuPhu"):
            giua(d, day + (52 if c.get("deu") else 34), c["chuPhu"], phong(36), INK,
                 rong=W - 160)

    elif L == "tach_so":
        # ══ MỘT SỐ, TÁCH RA TỪNG CHỮ SỐ ══
        # Bốn dấu hiệu chia hết đều chỉ nhìn vào MỘT PHẦN của con số: cho 2 và cho 5
        # thì nhìn chữ số cuối, cho 3 và cho 9 thì cộng hết các chữ số lại. Bé phải
        # thấy được "phần đang nhìn" tách khỏi phần còn lại, nếu không thì bốn dấu
        # hiệu trộn vào nhau thành một mớ.
        # ── DẤU PHẨY LÀ CÁI CỔNG, KHÔNG PHẢI MỘT CHỮ SỐ ──
        # Lớp 5 mở đầu bằng số thập phân, mà bản đầu của cảnh này bỏ MỌI ký tự vào
        # một ô như nhau — nên dấu phẩy ngồi trong ô y hệt chữ số, đúng chỗ bài đang
        # dạy "dấu phẩy là cổng ngăn hai bên" thì hình lại nói ngược. Nay dấu phẩy
        # vẽ THẤP và HẸP ở giữa hai ô, không có khung.
        # `sang` vẫn đếm theo CHỮ SỐ, không đếm dấu phẩy — kịch bản khỏi phải nhớ
        # trong số có mấy dấu.
        giua(d, 50, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        ky_tu = [x for x in str(c.get("so", ""))]
        sang = set(c.get("sang", []))           # chỉ số 1-based của CHỮ SỐ tô sáng
        rong_o, cach, rong_phay = 108, 18, 34
        tong_w = sum((rong_phay if x in ',.' else rong_o) for x in ky_tu) \
            + (len(ky_tu) - 1) * cach
        # Cân giữa như `nhom_deu`; chừa chỗ dưới cho dòng phép và dòng phụ.
        cao_chu = 168 + (82 if c.get('phep') and c.get('chuPhu') else 0)
        x0, y = (W - tong_w) // 2, max(150, (H - 118 - cao_chu) // 2)
        x, k = x0, 0
        for ch in ky_tu:
            if ch in ',.':
                f = phong(66)
                d.text((x + (rong_phay - d.textlength(ch, font=f)) / 2, y + 34), ch,
                       font=f, fill=NAVY)
                x += rong_phay + cach
                continue
            k += 1
            hi = k in sang
            the(d, x, y, rong_o, 118, nen=GOLD_PALE if hi else "#FFFFFF",
                vien=GOLD if hi else LINE, day=6 if hi else 3, bo=18)
            f = phong(66)
            d.text((x + (rong_o - d.textlength(ch, font=f)) / 2, y + 20), ch,
                   font=f, fill=GOLD_DARK if hi else NAVY)
            x += rong_o + cach
        if c.get("phep"):
            giua(d, y + 168, c["phep"], phong(42), TEAL_DARK, rong=W - 180)
        if c.get("chuPhu"):
            giua(d, y + (250 if c.get("phep") else 172), c["chuPhu"], phong(36),
                 INK, rong=W - 200)

    elif L == "y_toan":
        # MỘT Ý MỘT MÀN. Số thứ tự để bé biết đang ở bước mấy trên mấy.
        n, tong = c.get("buoc", 1), c.get("soBuoc", 1)
        giua(d, 52, f"Bước {n} trên {tong}", phong(32), MUTE)
        the(d, 80, 120, W - 160, 400, nen=SOFT, vien=LINE)
        giua(d, 160, c["chuChinh"], phong(46), NAVY, rong=W - 240)
        if c.get("chuPhu"):
            giua(d, 350, c["chuPhu"], phong(38), INK, rong=W - 240)
        r, cach = 16, 54
        x0 = W // 2 - cach * (tong - 1) // 2
        for i in range(tong):
            d.ellipse([x0 + i * cach - r, 580 - r, x0 + i * cach + r, 580 + r],
                      fill=TEAL if i < n else "#FFFFFF", outline=TEAL, width=3)

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


def lop_cua(ma: str) -> int:
    """`DL_TA2_B04` → 2. Mã bài đã mang số lớp, đừng bắt người gọi khai lại."""
    m = re.match(r"DL_TA(\d+)_", ma or "")
    if not m:
        raise SystemExit(f"mã bài không đọc ra lớp: {ma!r} (phải dạng DL_TA2_B04)")
    return int(m.group(1))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--bai")
    p.add_argument("--tat-ca", action="store_true")
    p.add_argument("--lop", type=int, default=1, help="quyển nào khi dùng --tat-ca")
    p.add_argument("--ra", default="web/public/content/tienganh/video")
    a = p.parse_args()

    # `--tat-ca` phải biết QUYỂN NÀO. Mặc định lớp 1 để lệnh cũ trong sổ vẫn chạy.
    dsm = ([f"DL_TA{a.lop}_B{i:02d}" for i in range(1, 17)] if a.tat_ca
           else [a.bai] if a.bai else None)
    if not dsm:
        p.error("cần --bai DL_TA2_B04 hoặc --tat-ca [--lop N]")
    # Sổ âm SUY TỪ MÃ BÀI, không ghim 'lop1'. Đọc bài lớp 2 mà tra sổ lớp 1 thì mọi
    # clip đều "chưa có" và video ra CÂM — không lỗi nào hiện, chỉ bé là thấy.
    lop = lop_cua(dsm[0])
    if any(lop_cua(m) != lop for m in dsm):
        p.error("một lượt chạy chỉ dựng được MỘT quyển")
    so = json.loads((GOC / f"web/public/content/tienganh/lop{lop}_am.json").read_text("utf8"))
    tong = 0.0
    for m in dsm:
        bai = json.loads((GOC / f"web/public/content/ta{lop}/{m}.json").read_text("utf8"))
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
