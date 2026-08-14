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
        giua(d, 56, "Bài toán hôm nay", phong(32), MUTE)
        the(d, 80, 130, W - 160, 330, nen="#FFFFFF", vien=NAVY, day=4)
        giua(d, 175, c["chuChinh"], phong(40), INK, rong=W - 240)
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
            giua(d, 385, "Thay số vào thử", phong(30), MUTE)
            the(d, 110, 430, W - 220, 120, nen="#FFFFFF", vien=TEAL, day=4)
            giua(d, 462, c["thay"], phong(42), TEAL_DARK, rong=W - 260)

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
        if c.get("hienThuTu"):
            d.text((x0 - 130, y_tt + 22), "đứng thứ", font=phong(30), fill=MUTE)
        d.text((x0 - 130, y_gt + 26), "số", font=phong(30), fill=MUTE)
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
        don_vi = rong_toi_da / max(lon, be, 1)
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
            f = phong(30)
            d.text((xb + 16, (y_be + y_lon) / 2 - 16), c["chuTong"], font=f, fill=NAVY)

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
        giua(d, 50, c.get("chuChinh", ""), phong(38), NAVY, rong=W - 140)
        chu_so = [x for x in str(c.get("so", ""))]
        sang = set(c.get("sang", []))           # chỉ số 1-based của chữ số tô sáng
        rong_o, cach = 108, 18
        tong_w = len(chu_so) * rong_o + (len(chu_so) - 1) * cach
        # Cân giữa như `nhom_deu`; chừa chỗ dưới cho dòng phép và dòng phụ.
        cao_chu = 168 + (82 if c.get('phep') and c.get('chuPhu') else 0)
        x0, y = (W - tong_w) // 2, max(150, (H - 118 - cao_chu) // 2)
        for i, ch in enumerate(chu_so):
            x = x0 + i * (rong_o + cach)
            hi = (i + 1) in sang
            the(d, x, y, rong_o, 118, nen=GOLD_PALE if hi else "#FFFFFF",
                vien=GOLD if hi else LINE, day=6 if hi else 3, bo=18)
            f = phong(66)
            d.text((x + (rong_o - d.textlength(ch, font=f)) / 2, y + 20), ch,
                   font=f, fill=GOLD_DARK if hi else NAVY)
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
