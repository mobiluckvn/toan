#!/usr/bin/env python3
"""BÚT VẼ CẢNH — nét, người, đồ đạc, phông nền cho bài tả tranh.

Bác bác bỏ toàn bộ 42 bức cũ vì chúng là DÃY KỆ ĐỰNG ĐỒ RỜI: ba thanh gỗ ngang,
emoji đặt lên trên. Bức "Hello Again" có con diều, con mèo, cái mũ — mà không ai
chào ai. Tệp này là bút vẽ để dựng CẢNH thay cho kệ: có tường, có sàn, có trời,
có người đứng đúng chỗ.

── VÌ SAO NGƯỜI PHẢI VẼ TAY ──
Emoji ghép ZWJ (🧑‍🏫 👨‍⚕️) vẽ ra MỘT KHUÔN MẶT TRƠN: bộ vẽ tách chuỗi rồi vẽ từng
mảnh, mà dấu ⚕️ không có trong phông nên rơi mất trong im lặng. Đọc tên Unicode
KHÔNG đủ — phải rasterize rồi nhìn. Xem [[hinh-trong-video-phai-khop-loi-doc]].

Và emoji người chỉ có một tư thế đứng yên. Cảnh cần bé ĐANG VẪY, ĐANG CHỈ, ĐANG
NGỒI, ĐANG CHẠY — nên `nguoi()` dựng theo tham số: dáng · tóc · màu áo · hướng.

── KHÔNG PHẢI BỘ NHÂN BẢN ──
Tệp này chỉ biết VẼ. Nó không quyết cảnh nào có gì — bố cục từng bức khai tay
trong `data/tienganh/canh_lopN.json`. Đó là luật 4 bác chốt: 42 cảnh viết tay.
"""
from __future__ import annotations

import math
from PIL import Image, ImageDraw

W, H = 1280, 720
INK = "#15263A"          # màu nét, cùng màu với hinh_ve.json
TRAN = 96                # mép dưới của dải tiêu đề; cảnh bắt đầu từ đây

DA = "#F2C79A"           # màu da mặc định, lấy đúng của hinh_ve.json
TOC = "#3A2A20"


# ══════════════════════════════ NÉT CƠ BẢN ══════════════════════════════
def net(d: ImageDraw.ImageDraw, diem, mau=INK, day=6):
    """Đường gấp khúc có ĐẦU TRÒN. Pillow không có stroke-linecap nên phải tự
    chấm một hình tròn ở mỗi khớp — thiếu nó thì tay chân người cụt vuông."""
    diem = [(int(x), int(y)) for x, y in diem]
    if len(diem) > 1:
        d.line(diem, fill=mau, width=int(day), joint="curve")
    r = day / 2
    for x, y in diem:
        d.ellipse([x - r, y - r, x + r, y + r], fill=mau)


def khoi(d, x, y, w, h, nen="#FFFFFF", vien=INK, day=4, bo=0):
    """Hộp chữ nhật có viền. Đơn vị dựng nên cả bộ đồ đạc."""
    hop = [int(x), int(y), int(x + w), int(y + h)]
    if bo:
        d.rounded_rectangle(hop, radius=int(bo), fill=nen,
                            outline=vien, width=int(day))
    else:
        d.rectangle(hop, fill=nen, outline=vien, width=int(day))


def tron(d, cx, cy, r, nen="#FFFFFF", vien=INK, day=4):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nen,
              outline=vien, width=int(day))


def _nhat(mau: str, phan: float) -> str:
    """Trộn màu về phía trắng — dùng cho HẬU CẢNH. Vật ở xa mà đậm bằng vật ở
    gần thì bức tranh bẹt, bé không đọc được đâu là tiền cảnh."""
    r, g, b = (int(mau[i:i + 2], 16) for i in (1, 3, 5))
    f = lambda c: int(c + (255 - c) * phan)  # noqa: E731
    return f"#{f(r):02X}{f(g):02X}{f(b):02X}"


# ══════════════════════════════ NGƯỜI ══════════════════════════════
#
# Toạ độ vào là BÀN CHÂN (x, y) — vì trong cảnh người đứng trên sàn, và khai
# theo chân thì không bao giờ có người lơ lửng. Bức cũ khai theo tâm và đã ra
# một con mèo bay dưới gầm bàn.
#
DANG = ("dung", "vay", "chi", "ngoi", "chay", "nhay", "cui", "gio")


def nguoi(d, x, y, cao=200, *, ao="#3D8BD4", quan="#2F4A6B", vay_ao=None,
          da=DA, toc=TOC, toc_dai=False, tet=False, dang="dung", huong=1,
          xa=0.0):
    """Một người. `cao` là chiều cao cả người tính từ gót lên đỉnh đầu.

    `huong` = 1 quay sang phải, -1 sang trái. `xa` là độ lùi hậu cảnh
    (0 = tiền cảnh, 0.35 = nhạt dần về phía trời).

    ⚠ TAY VẼ BẰNG MÀU DA, không phải màu áo. Bản đầu tôi tô tay bằng `ao` và
    một cô giáo áo TRẮNG ra hai cánh tay tàng hình trên nền tường kem — cùng
    họ với lỗi tô chữ tiếng Anh bằng màu kẻ viền. Tay áo là một khúc ngắn ở
    vai, phần còn lại là da.
    """
    if dang not in DANG:
        raise SystemExit(f"✗ dáng người lạ: {dang!r} — có {DANG}")
    if xa:
        ao, quan, da, toc = (_nhat(c, xa) for c in (ao, quan, da, toc))
        vay_ao = _nhat(vay_ao, xa) if vay_ao else None
    muc = _nhat(INK, xa) if xa else INK

    # Tỉ lệ TRẺ CON: đầu to, chân ngắn. Bản đầu để chân dài 58% chiều cao nên
    # ra dáng người lớn — bức tranh vẽ lớp tiểu học mà toàn người mẫu.
    r = cao * 0.135                        # bán kính đầu
    rong = cao * 0.16                      # nửa bề ngang thân
    than = cao * 0.30                      # vai → hông, GIỮ NGUYÊN mọi dáng
    hong_y = y - cao * (0.30 if dang == "ngoi" else 0.44)
    vai_y = hong_y - than
    dau_y = vai_y - r * 0.95
    day = max(3, cao * 0.030)              # bề dày tay chân

    def giay(px, py, h=1):
        """Bàn chân. Thiếu nó thì hai ống quần cụt ngang sàn và người trông như
        đứng hụt xuống dưới mặt đất."""
        w = rong * 0.62
        d.ellipse([px - w * (0.35 if h > 0 else 0.85), py - day * 0.55,
                   px + w * (0.85 if h > 0 else 0.35), py + day * 0.55],
                  fill=muc, outline=muc)

    def chi_tay(diem):
        """Một cánh tay: khúc da, rồi tay áo đè lên phần sát vai, rồi bàn tay."""
        net(d, diem, da, day)
        net(d, [diem[0], (diem[0][0] + (diem[1][0] - diem[0][0]) * 0.42,
                          diem[0][1] + (diem[1][1] - diem[0][1]) * 0.42)],
            ao, day * 1.25)
        tron(d, diem[-1][0], diem[-1][1], day * 0.62, da, muc, day * 0.34)

    # ── CHÂN ──
    if dang == "chay":
        # Chạy thì THÂN NGẢ VỀ TRƯỚC và chân trước co lên — không phải đứng
        # dạng chân. Bản đầu để thân thẳng và ra dáng đứng nghỉ.
        net(d, [(x, hong_y), (x - rong * 1.5 * huong, y - cao * 0.10),
                (x - rong * 0.7 * huong, y - cao * 0.02)], quan, day * 1.5)
        net(d, [(x, hong_y), (x + rong * 1.7 * huong, y)], quan, day * 1.5)
        giay(x - rong * 0.7 * huong, y - cao * 0.02, huong)
        giay(x + rong * 1.7 * huong, y, huong)
    elif dang == "nhay":
        for s in (-1, 1):
            net(d, [(x, hong_y), (x + rong * 1.5 * s, y)], quan, day * 1.5)
            giay(x + rong * 1.5 * s, y, s)
    elif dang == "ngoi":
        # Đùi đưa NGANG ra trước tới đầu gối, rồi cẳng chân thả THẲNG xuống sàn.
        for k in (0.95, 1.45):
            net(d, [(x, hong_y), (x + rong * 1.5 * k * huong, hong_y),
                    (x + rong * 1.5 * k * huong, y)], quan, day * 1.5)
            giay(x + rong * 1.5 * k * huong, y, huong)
    elif dang == "cui":
        net(d, [(x, hong_y), (x - rong * 0.7, y)], quan, day * 1.5)
        net(d, [(x, hong_y), (x + rong * 1.5 * huong, hong_y + cao * 0.14),
                (x + rong * 2.1 * huong, y)], quan, day * 1.5)
        giay(x - rong * 0.7, y, -huong)
        giay(x + rong * 2.1 * huong, y, huong)
    else:
        for s in (-1, 1):
            net(d, [(x + rong * 0.42 * s, hong_y), (x + rong * 0.55 * s, y)],
                quan, day * 1.5)
            giay(x + rong * 0.55 * s, y, s)

    # ── THÂN ── váy là hình thang loe, áo là hộp bo góc
    if vay_ao:
        d.polygon([(x - rong, hong_y - than * 0.35), (x + rong, hong_y - than * 0.35),
                   (x + rong * 1.85, hong_y + cao * 0.09),
                   (x - rong * 1.85, hong_y + cao * 0.09)],
                  fill=vay_ao, outline=muc)
        khoi(d, x - rong, vai_y, rong * 2, than * 0.72, ao, muc, day * 0.55,
             bo=rong * 0.42)
    else:
        khoi(d, x - rong, vai_y, rong * 2, than + cao * 0.05, ao, muc,
             day * 0.55, bo=rong * 0.45)

    # ── TAY ──
    t_y = vai_y + cao * 0.035
    if dang == "vay":                      # một tay giơ cao vẫy, một tay buông
        chi_tay([(x - rong, t_y), (x - rong * 1.55, hong_y - cao * 0.01)])
        chi_tay([(x + rong, t_y), (x + rong * 1.85, t_y - cao * 0.12),
                 (x + rong * 1.65, t_y - cao * 0.25)])
    elif dang == "chi":                    # một tay chỉ NGANG, đúng hướng
        chi_tay([(x - rong * huong, t_y), (x - rong * 1.5 * huong, hong_y)])
        chi_tay([(x + rong * huong, t_y), (x + rong * 2.5 * huong, t_y + cao * 0.02)])
    elif dang in ("nhay", "gio"):          # hai tay giơ lên
        for s in (-1, 1):
            chi_tay([(x + rong * s, t_y), (x + rong * 1.95 * s, t_y - cao * 0.19)])
    elif dang == "chay":
        chi_tay([(x - rong, t_y), (x - rong * 2.0, t_y - cao * 0.07)])
        chi_tay([(x + rong, t_y), (x + rong * 1.9, t_y + cao * 0.09)])
    elif dang == "cui":                    # hai tay chụm về trước, thấp
        for k in (0.55, 1.0):
            chi_tay([(x + rong * 0.5 * huong, t_y),
                     (x + rong * (1.5 + k * 0.4) * huong, hong_y + cao * 0.05)])
    else:                                  # đứng · ngồi
        for s in (-1, 1):
            chi_tay([(x + rong * s, t_y), (x + rong * 1.3 * s, hong_y - cao * 0.01)])

    # ── ĐẦU ── cổ, rồi tóc sau, rồi mặt, rồi vành tóc trước trán
    net(d, [(x, vai_y), (x, dau_y + r * 0.6)], da, day * 1.1)
    if toc_dai:
        # ⚠ Tóc xoã phải DỪNG Ở VAI. Bản đầu cho dài xuống 2.4r và nó phủ kín cả
        # thân áo — cô giáo ra một khối tóc, không nhìn ra người mặc áo màu gì.
        d.polygon([(x - r * 1.02, dau_y - r * 0.1), (x + r * 1.02, dau_y - r * 0.1),
                   (x + r * 1.12, vai_y + r * 0.1), (x - r * 1.12, vai_y + r * 0.1)],
                  fill=toc)
    tron(d, x, dau_y, r, da, muc, day * 0.55)
    # Vành tóc trước trán: chỏm MỎNG ôm nửa trên của đầu. Bản đầu vẽ nửa hình
    # tròn nên nó trùm tới ngang mắt — cái mặt thành cái mũ.
    d.pieslice([x - r, dau_y - r, x + r, dau_y + r * 0.58], 178, 362, fill=toc)
    if tet:
        for s in (-1, 1):
            net(d, [(x + r * 0.9 * s, dau_y + r * 0.05),
                    (x + r * 1.4 * s, dau_y + r * 1.1)], toc, day * 1.2)
            tron(d, x + r * 1.45 * s, dau_y + r * 1.25, r * 0.24, "#E4574C", muc,
                 day * 0.3)
    # Mặt luôn quay ra NGƯỜI XEM kể cả khi thân quay ngang: bé phải nhìn thấy
    # nét mặt thì mới tả được "bạn ấy đang cười".
    for s in (-1, 1):
        tron(d, x + r * 0.36 * s, dau_y + r * 0.28, r * 0.16, muc, muc, 1)
    d.arc([x - r * 0.4, dau_y + r * 0.36, x + r * 0.4, dau_y + r * 0.84],
          15, 165, fill=muc, width=max(2, int(day * 0.5)))


# ══════════════════════════════ ĐỒ ĐẠC ══════════════════════════════
def cay(d, x, y, cao=220, xa=0.0):
    """Cái cây — thân nâu, tán ba cụm tròn."""
    la, than = _nhat("#4E9A4E", xa), _nhat("#7A4F33", xa)
    muc = _nhat(INK, xa)
    khoi(d, x - cao * 0.05, y - cao * 0.45, cao * 0.10, cao * 0.45, than, muc, 4)
    for dx, dy, rr in ((-0.20, -0.52, 0.22), (0.20, -0.52, 0.22), (0, -0.70, 0.26)):
        tron(d, x + cao * dx, y + cao * dy, cao * rr, la, muc, 4)


def may(d, x, y, rong=180, xa=0.25):
    n = _nhat("#FFFFFF", 0)
    muc = _nhat(INK, 0.45 + xa)
    for dx, dy, rr in ((-0.28, 0.05, 0.24), (0.28, 0.05, 0.22), (0, -0.08, 0.32)):
        tron(d, x + rong * dx, y + rong * dy, rong * rr, n, muc, 3)


def mat_troi(d, x, y, r=58):
    for i in range(12):
        a = math.radians(i * 30)
        net(d, [(x + math.cos(a) * r * 1.25, y + math.sin(a) * r * 1.25),
                (x + math.cos(a) * r * 1.65, y + math.sin(a) * r * 1.65)],
            "#F9B233", 8)
    tron(d, x, y, r, "#FFD84D", "#E09B18", 5)


def bang_den(d, x, y, w, h):
    """Bảng treo tường. MẶT BẢNG ĐỂ TRỐNG — bé đang tập đọc, chữ in sẵn trên
    tranh là cho sẵn đáp án, đó là luật bác chốt cho cả 42 bức."""
    khoi(d, x, y, w, h, "#8A6B45", INK, 5, bo=6)
    khoi(d, x + 12, y + 12, w - 24, h - 24, "#2E4A3A", INK, 4)
    khoi(d, x + w * 0.25, y + h, w * 0.5, 14, "#A9714B", INK, 4, bo=4)   # máng phấn


def cua_so(d, x, y, w, h, ngoai="#BFE3F7"):
    """Cửa sổ nhìn ra ngoài — có tán cây xanh cho biết ngoài kia là sân."""
    khoi(d, x, y, w, h, ngoai, INK, 5, bo=4)
    d.rectangle([x + 6, y + h * 0.62, x + w - 6, y + h - 6], fill="#8CC96B")
    tron(d, x + w * 0.30, y + h * 0.55, min(w, h) * 0.22, "#4E9A4E", INK, 3)
    net(d, [(x + w / 2, y), (x + w / 2, y + h)], INK, 5)
    net(d, [(x, y + h / 2), (x + w, y + h / 2)], INK, 5)


def cua(d, x, y, w, h, mo=False):
    khoi(d, x, y, w, h, "#A9714B", INK, 5, bo=4)
    if mo:
        khoi(d, x + w * 0.12, y + h * 0.06, w * 0.76, h * 0.88, "#6E4B33", INK, 4)
    tron(d, x + w * 0.80, y + h * 0.52, w * 0.06, "#F9B233", INK, 3)


def ban(d, x, y, w=190, cao=110, mau="#C8A87C"):
    """Bàn học/bàn ăn — mặt bàn rộng, hai chân. (x, y) là mép dưới giữa."""
    khoi(d, x - w / 2, y - cao, w, cao * 0.16, mau, INK, 4, bo=4)
    for s in (-1, 1):
        khoi(d, x + s * w * 0.40 - w * 0.04, y - cao * 0.86, w * 0.08,
             cao * 0.86, "#8A6B45", INK, 4)


def ghe(d, x, y, cao=120, huong=1, mau="#C8A87C"):
    r = cao * 0.42
    khoi(d, x - r, y - cao * 0.52, r * 2, cao * 0.14, mau, INK, 4, bo=3)   # mặt
    khoi(d, x - r * huong - r * 0.12 * huong, y - cao, r * 0.16, cao * 0.50,
         mau, INK, 4, bo=3)                                                # lưng
    for s in (-1, 1):
        khoi(d, x + s * r * 0.78 - r * 0.07, y - cao * 0.40, r * 0.14,
             cao * 0.40, "#8A6B45", INK, 4)


def gia_sach(d, x, y, w=180, cao=190):
    khoi(d, x - w / 2, y - cao, w, cao, "#A9714B", INK, 5, bo=3)
    for i in (1, 2):
        yy = y - cao + cao * i / 3
        net(d, [(x - w / 2, yy), (x + w / 2, yy)], INK, 4)
    mau = ["#C0392B", "#0B4EA8", "#1FCBAB", "#F9B233", "#7E57C2"]
    for i in range(2):
        for j in range(5):
            khoi(d, x - w / 2 + 14 + j * (w - 34) / 5, y - cao + cao * i / 3 + 12,
                 (w - 40) / 5 - 4, cao / 3 - 24, mau[(i * 5 + j) % 5], INK, 2)


def giuong(d, x, y, w=260, cao=130):
    khoi(d, x - w / 2, y - cao * 0.72, w, cao * 0.42, "#9FC6E8", INK, 4, bo=8)  # chăn
    khoi(d, x - w / 2 + 8, y - cao * 0.80, w * 0.26, cao * 0.20, "#FFFFFF", INK, 4, bo=8)
    khoi(d, x - w / 2, y - cao * 0.32, w, cao * 0.12, "#A9714B", INK, 4)
    khoi(d, x + w / 2 - w * 0.05, y - cao, w * 0.05, cao, "#8A6B45", INK, 4)
    for s in (-1, 1):
        khoi(d, x + s * (w / 2 - 14), y - cao * 0.22, 12, cao * 0.22, "#8A6B45", INK, 3)


def sofa(d, x, y, w=280, cao=150):
    khoi(d, x - w / 2, y - cao, w, cao * 0.70, "#8FA3B8", INK, 5, bo=14)
    khoi(d, x - w / 2, y - cao * 0.48, w, cao * 0.34, "#A8BACD", INK, 4, bo=10)
    for s in (-1, 1):
        khoi(d, x + s * w * 0.44 - w * 0.06, y - cao * 0.62, w * 0.12,
             cao * 0.50, "#8FA3B8", INK, 4, bo=8)


def khung_anh(d, x, y, w=200, h=150, trong=None):
    """Khung ảnh treo tường. `trong` là hàm vẽ phần bên trong."""
    khoi(d, x - w / 2, y, w, h, "#8A6B45", INK, 5, bo=4)
    khoi(d, x - w / 2 + 12, y + 12, w - 24, h - 24, "#FFF9EC", INK, 3)
    if trong:
        trong(d, x, y + 12, w - 24, h - 24)


def bang_ghim(d, x, y, w=340, h=230, o=3):
    """Bảng ghim treo tường — các ô ĐỂ TRỐNG."""
    khoi(d, x - w / 2, y, w, h, "#D9BE94", INK, 5, bo=4)
    bo = w / (o + 1)
    for i in range(o):
        xx = x - w / 2 + bo * 0.35 + i * (w - bo * 0.7) / o
        khoi(d, xx, y + h * 0.18, (w - bo * 0.7) / o - 12, h * 0.64,
             "#FFFFFF", INK, 3)
        tron(d, xx + ((w - bo * 0.7) / o - 12) / 2, y + h * 0.18, 7,
             ["#C0392B", "#0B4EA8", "#F9B233"][i % 3], INK, 2)


def bang_luoi(d, x, y, w=380, h=220, cot=7, hang=1, to=None):
    """Tấm lịch / thời khoá biểu — kẻ ô, các ô ĐỂ TRỐNG, `to` là ô tô màu."""
    khoi(d, x - w / 2, y, w, h, "#FFFFFF", INK, 5, bo=4)
    for i in range(1, cot):
        net(d, [(x - w / 2 + w * i / cot, y), (x - w / 2 + w * i / cot, y + h)], INK, 3)
    for j in range(1, hang):
        net(d, [(x - w / 2, y + h * j / hang), (x + w / 2, y + h * j / hang)], INK, 3)
    if to is not None:
        i, j = (to, 0) if isinstance(to, int) else to
        d.rectangle([x - w / 2 + w * i / cot + 3, y + h * j / hang + 3,
                     x - w / 2 + w * (i + 1) / cot - 3, y + h * (j + 1) / hang - 3],
                    fill="#F9B233")
        d.ellipse([x - w / 2 + w * i / cot + 8, y + h * j / hang + 8,
                   x - w / 2 + w * (i + 1) / cot - 8, y + h * (j + 1) / hang - 8],
                  outline="#C0392B", width=5)


def dong_ho(d, x, y, r=52, gio=6, phut=0):
    tron(d, x, y, r, "#FFFFFF", "#C0392B", 7)
    for i in range(12):
        a = math.radians(i * 30 - 90)
        net(d, [(x + math.cos(a) * r * 0.80, y + math.sin(a) * r * 0.80),
                (x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92)], INK, 3)
    ag = math.radians((gio % 12) * 30 + phut * 0.5 - 90)
    ap = math.radians(phut * 6 - 90)
    net(d, [(x, y), (x + math.cos(ag) * r * 0.48, y + math.sin(ag) * r * 0.48)], INK, 7)
    net(d, [(x, y), (x + math.cos(ap) * r * 0.76, y + math.sin(ap) * r * 0.76)], INK, 5)
    tron(d, x, y, r * 0.09, INK, INK, 1)


def gia_ve(d, x, y, cao=250):
    """Giá vẽ ba chân + tờ giấy trắng."""
    net(d, [(x, y - cao * 0.30), (x - cao * 0.30, y)], "#A9714B", 10)
    net(d, [(x, y - cao * 0.30), (x + cao * 0.30, y)], "#A9714B", 10)
    net(d, [(x, y - cao * 0.30), (x + cao * 0.06, y)], "#8A6B45", 9)
    khoi(d, x - cao * 0.30, y - cao, cao * 0.60, cao * 0.62, "#FFFFFF", INK, 5)
    net(d, [(x - cao * 0.34, y - cao * 0.38), (x + cao * 0.34, y - cao * 0.38)],
        "#8A6B45", 9)


def lua_trai(d, x, y, cao=130):
    for s, m in ((-1, "#8A6B45"), (1, "#A9714B")):
        net(d, [(x - cao * 0.42 * s, y), (x + cao * 0.38 * s, y - cao * 0.14)], m, 14)
    d.polygon([(x, y - cao), (x + cao * 0.30, y - cao * 0.30),
               (x - cao * 0.30, y - cao * 0.30)], fill="#F9B233", outline=INK)
    d.polygon([(x, y - cao * 0.72), (x + cao * 0.17, y - cao * 0.26),
               (x - cao * 0.17, y - cao * 0.26)], fill="#E4574C")


def leu(d, x, y, rong=230, cao=180):
    d.polygon([(x, y - cao), (x + rong / 2, y), (x - rong / 2, y)],
              fill="#E8833A", outline=INK, width=5)
    d.polygon([(x, y - cao * 0.92), (x + rong * 0.16, y), (x - rong * 0.16, y)],
              fill="#2E4A3A", outline=INK, width=4)


def hang_rao(d, x1, x2, y, cao=90, buoc=64):
    net(d, [(x1, y - cao * 0.72), (x2, y - cao * 0.72)], "#A9714B", 10)
    net(d, [(x1, y - cao * 0.36), (x2, y - cao * 0.36)], "#A9714B", 10)
    xx = x1
    while xx <= x2:
        khoi(d, xx - 9, y - cao, 18, cao, "#C8A87C", INK, 4, bo=3)
        xx += buoc


def song_sat(d, x, y, w, h, buoc=46):
    """Song sắt chuồng thú — vẽ ĐÈ LÊN con vật, nên gọi sau khi vẽ con vật."""
    khoi(d, x, y, w, 14, "#8FA3B8", INK, 4)
    khoi(d, x, y + h - 14, w, 14, "#8FA3B8", INK, 4)
    xx = x + buoc
    while xx < x + w:
        khoi(d, xx - 5, y, 10, h, "#8FA3B8", INK, 3)
        xx += buoc


def nha(d, x, y, rong=260, cao=250, tang=2, mau="#F3D89B", xa=0.0):
    """Dãy nhà học / nhà phố — thân + mái + các ô cửa sổ sáng."""
    t, m, muc = _nhat(mau, xa), _nhat("#C0392B", xa), _nhat(INK, xa)
    khoi(d, x - rong / 2, y - cao, rong, cao, t, muc, 5)
    d.polygon([(x - rong / 2 - 18, y - cao), (x + rong / 2 + 18, y - cao),
               (x, y - cao - cao * 0.24)], fill=m, outline=muc, width=5)
    for i in range(tang):
        for j in range(3):
            khoi(d, x - rong * 0.34 + j * rong * 0.29,
                 y - cao + cao * 0.14 + i * cao * 0.42,
                 rong * 0.18, cao * 0.24, _nhat("#BFE3F7", xa), muc, 4)


def oto(d, x, y, dai=190, mau="#C0392B", xa=0.0):
    t, muc = _nhat(mau, xa), _nhat(INK, xa)
    cao = dai * 0.34
    khoi(d, x - dai / 2, y - cao, dai, cao, t, muc, 4, bo=cao * 0.35)
    d.polygon([(x - dai * 0.26, y - cao), (x + dai * 0.22, y - cao),
               (x + dai * 0.12, y - cao * 1.62), (x - dai * 0.16, y - cao * 1.62)],
              fill=t, outline=muc, width=4)
    khoi(d, x - dai * 0.20, y - cao * 1.54, dai * 0.15, cao * 0.46,
         _nhat("#BFE3F7", xa), muc, 3, bo=3)
    khoi(d, x + dai * 0.00, y - cao * 1.54, dai * 0.15, cao * 0.46,
         _nhat("#BFE3F7", xa), muc, 3, bo=3)
    for s in (-1, 1):
        tron(d, x + s * dai * 0.30, y, dai * 0.11, _nhat("#2C2C2C", xa), muc, 4)
        tron(d, x + s * dai * 0.30, y, dai * 0.05, _nhat("#8FA3B8", xa), muc, 2)


def tu_kinh(d, x, y, w=280, cao=240, bay=None, mau="#F3D89B"):
    """Gian hàng có tủ kính — `bay` vẽ thứ bày trong tủ."""
    khoi(d, x - w / 2, y - cao, w, cao, mau, INK, 5)
    khoi(d, x - w / 2 + 16, y - cao * 0.78, w - 32, cao * 0.60, "#EAF2FB", INK, 4)
    d.polygon([(x - w / 2 - 14, y - cao), (x + w / 2 + 14, y - cao),
               (x + w / 2 + 14, y - cao - 34), (x - w / 2 - 14, y - cao - 34)],
              fill="#1FCBAB", outline=INK, width=4)
    if bay:
        bay(d, x, y - cao * 0.78, w - 32, cao * 0.60)


def bien_bao(d, x, y, cao=210):
    """Biển báo bát giác ĐỎ — không viết chữ."""
    net(d, [(x, y), (x, y - cao * 0.62)], "#8FA3B8", 12)
    r = cao * 0.30
    d.polygon([(x + math.cos(math.radians(i * 45 + 22.5)) * r,
                y - cao * 0.62 - r + math.sin(math.radians(i * 45 + 22.5)) * r)
               for i in range(8)], fill="#C0392B", outline=INK, width=5)


def ban_do(d, x, y, w=620, h=330):
    """Bản đồ thế giới treo tường: biển xanh, các mảng lục địa xanh lá.

    KHÔNG viết chữ, không vẽ đường biên giới — bé chỉ cần đọc ra "đây là bản đồ".
    """
    khoi(d, x - w / 2, y, w, h, "#7FC4E8", INK, 5, bo=4)
    lg = [[(0.06, 0.18), (0.24, 0.10), (0.30, 0.30), (0.20, 0.46), (0.08, 0.40)],
          [(0.14, 0.56), (0.26, 0.52), (0.28, 0.76), (0.18, 0.92), (0.12, 0.72)],
          [(0.40, 0.14), (0.62, 0.10), (0.66, 0.28), (0.46, 0.34)],
          [(0.44, 0.40), (0.58, 0.38), (0.60, 0.72), (0.48, 0.80), (0.42, 0.58)],
          [(0.68, 0.20), (0.92, 0.16), (0.94, 0.44), (0.72, 0.48)],
          [(0.78, 0.62), (0.92, 0.60), (0.93, 0.80), (0.80, 0.82)]]
    for m in lg:
        d.polygon([(x - w / 2 + a * w, y + b * h) for a, b in m],
                  fill="#79B85C", outline=INK)


def anh_nho(d, x, y, w=180, h=130, canh="nha"):
    """Một tấm ảnh / bức tranh nhỏ trong khung, có NỘI DUNG thật bên trong.

    ⚠ Bản đầu tôi vẽ mấy khung này thành Ô TRẮNG TRƠN, trong khi mô tả bác đã
    duyệt hứa hẳn "ảnh chụp bãi biển · cánh đồng · thành phố". Ô trắng vừa vô
    nghĩa với bé (không tả được gì) vừa làm TRANH LỆCH MÔ TẢ — mà mô tả chính là
    thứ sinh ra câu hỏi và bài nói. Xem [[hinh-trong-video-phai-khop-loi-doc]].
    """
    khoi(d, x - w / 2, y, w, h, "#FFF9EC", INK, 4, bo=3)
    l, t = x - w / 2, y
    def o(a, b): return (l + a * w, t + b * h)
    if canh == "bien":                                  # bãi biển: trời, biển, ô dù
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.52)], fill="#BFE3F7")
        d.rectangle([*o(0.03, 0.52), *o(0.97, 0.74)], fill="#4E8FC4")
        d.rectangle([*o(0.03, 0.74), *o(0.97, 0.94)], fill="#EBD9A8")
        d.pieslice([*o(0.52, 0.36), *o(0.88, 0.72)], 180, 360, fill="#E4574C",
                   outline=INK, width=2)
        net(d, [o(0.70, 0.54), o(0.70, 0.86)], INK, 3)
        tron(d, *o(0.18, 0.20), w * 0.07, "#FFD84D", "#E09B18", 2)
    elif canh == "que":                                 # đồng quê: trời, ruộng lúa
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.44)], fill="#BFE3F7")
        d.rectangle([*o(0.03, 0.44), *o(0.97, 0.94)], fill="#C9C24E")
        for i in range(5):
            net(d, [o(0.10 + i * 0.19, 0.52), o(0.10 + i * 0.19, 0.88)], "#9E9A32", 4)
        tron(d, *o(0.82, 0.20), w * 0.07, "#FFD84D", "#E09B18", 2)
    elif canh == "pho":                                 # thành phố: nhà cao tầng
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.94)], fill="#CFE6F5")
        for a, hh, m in ((0.10, 0.46, "#8FA3B8"), (0.34, 0.66, "#6E88A3"),
                         (0.58, 0.54, "#A8BACD"), (0.78, 0.72, "#7A93AE")):
            d.rectangle([*o(a, 0.94 - hh), *o(a + 0.16, 0.94)], fill=m, outline=INK)
    elif canh == "nha":                                 # tranh vẽ ngôi nhà
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.94)], fill="#EAF6FF")
        d.rectangle([*o(0.26, 0.48), *o(0.74, 0.90)], fill="#F3D89B", outline=INK, width=3)
        d.polygon([o(0.20, 0.48), o(0.80, 0.48), o(0.50, 0.18)], fill="#C0392B",
                  outline=INK)
        d.rectangle([*o(0.44, 0.66), *o(0.58, 0.90)], fill="#A9714B", outline=INK, width=2)
    elif canh == "cau":                                 # ảnh chụp cây cầu
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.58)], fill="#BFE3F7")
        d.rectangle([*o(0.03, 0.58), *o(0.97, 0.94)], fill="#4E8FC4")
        d.rectangle([*o(0.03, 0.52), *o(0.97, 0.60)], fill="#C0392B")
        for a in (0.18, 0.5, 0.82):
            d.pieslice([*o(a - 0.16, 0.30), *o(a + 0.16, 0.74)], 180, 360,
                       outline="#C0392B", width=4)
            net(d, [o(a, 0.30), o(a, 0.52)], "#C0392B", 3)
        tron(d, *o(0.84, 0.18), w * 0.06, "#FFD84D", "#E09B18", 2)
    elif canh == "ho":                                  # ảnh chụp mặt hồ
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.46)], fill="#BFE3F7")
        d.rectangle([*o(0.03, 0.46), *o(0.97, 0.94)], fill="#4E8FC4")
        for i in range(3):
            net(d, [o(0.14, 0.60 + i * 0.11), o(0.44, 0.60 + i * 0.11)], "#7FB0D8", 3)
        for a in (0.12, 0.30, 0.72, 0.90):
            d.rectangle([*o(a - 0.02, 0.34), *o(a + 0.02, 0.46)], fill="#7A4F33")
            tron(d, *o(a, 0.30), w * 0.06, "#4E9A4E", INK, 2)
    elif canh == "cay":                                 # tranh vẽ cái cây
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.94)], fill="#EAF6FF")
        d.rectangle([*o(0.45, 0.60), *o(0.55, 0.92)], fill="#7A4F33", outline=INK, width=2)
        tron(d, *o(0.50, 0.42), w * 0.22, "#4E9A4E", INK, 3)
    elif canh == "troi":                                # tranh vẽ mặt trời
        d.rectangle([*o(0.03, 0.06), *o(0.97, 0.94)], fill="#EAF6FF")
        for i in range(8):
            a = math.radians(i * 45)
            net(d, [(x + math.cos(a) * w * 0.16, y + h * 0.5 + math.sin(a) * w * 0.16),
                    (x + math.cos(a) * w * 0.26, y + h * 0.5 + math.sin(a) * w * 0.26)],
                "#F9B233", 4)
        tron(d, x, y + h * 0.5, w * 0.15, "#FFD84D", "#E09B18", 3)
    else:
        raise SystemExit(f"✗ không có cảnh nhỏ “{canh}”")


def mat_trang(d, x, y, r=62):
    """Mặt trăng tròn. Cảnh Trung thu dùng `mat_troi` thì ra ban ngày — lệch hẳn
    mô tả “trời tím sẫm có mặt trăng tròn vàng lớn”."""
    tron(d, x, y, r, "#FFF3C4", "#E0C86A", 4)
    for dx, dy, rr in ((-0.30, -0.20, 0.16), (0.24, 0.10, 0.20), (-0.05, 0.36, 0.12)):
        tron(d, x + r * dx, y + r * dy, r * rr, "#EFE0A8", "#E0C86A", 2)


def bang_thoi_tiet(d, x, y, w=420, h=200, khoanh=0):
    """Bảng thời tiết bốn ô: nắng · nhiều mây · mưa · TUYẾT. `khoanh` là ô được
    khoanh tròn đỏ — trạng thái của hôm nay.

    ⚠ Ô thứ tư đổi từ GIÓ sang TUYẾT khi làm lớp 5: cảnh “ngày mùa đông” mô tả
    ngoài cửa sổ đang rơi tuyết và ô tuyết được khoanh đỏ — mà bảng lại không có
    ô nào là tuyết. Tranh lệch mô tả thì bé đối chiếu không ra.

    ⚠ Tính từ thời tiết KHÔNG vẽ thành vật rời được: `sunny` không phải một đồ
    vật đặt trên bàn. Nên unit thời tiết phải có bảng này, và bản đầu tôi dựng
    nó bằng `bangLuoi` — ra BỐN Ô TRẮNG TRƠN, đúng thứ mô tả không hứa.
    """
    khoi(d, x - w / 2, y, w, h, "#FFFFFF", INK, 5, bo=6)
    o = w / 4
    for i in range(1, 4):
        net(d, [(x - w / 2 + o * i, y), (x - w / 2 + o * i, y + h)], INK, 3)
    for i in range(4):
        cx, cy = x - w / 2 + o * (i + 0.5), y + h * 0.5
        r = min(o, h) * 0.26
        if i == 0:                                   # nắng
            for k in range(8):
                a = math.radians(k * 45)
                net(d, [(cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r * 1.3),
                        (cx + math.cos(a) * r * 1.8, cy + math.sin(a) * r * 1.8)],
                    "#F9B233", 4)
            tron(d, cx, cy, r, "#FFD84D", "#E09B18", 4)
        else:                                        # ba ô kia đều có đám mây
            for dx, dy, rr in ((-0.5, 0.1, 0.6), (0.5, 0.1, 0.55), (0, -0.2, 0.8)):
                tron(d, cx + r * dx, cy + r * dy - h * 0.06, r * rr, "#FFFFFF", INK, 3)
            if i == 2:                               # mưa: ba giọt rơi
                for k in (-1, 0, 1):
                    net(d, [(cx + r * k * 0.7, cy + h * 0.10),
                            (cx + r * k * 0.7 - 4, cy + h * 0.22)], "#4E8FC4", 5)
            if i == 3:                               # tuyết: ba bông sáu cánh
                for k in (-1, 0, 1):
                    bx, by = cx + r * k * 0.8, cy + h * 0.13 + abs(k) * 8
                    for a in range(3):
                        g = math.radians(a * 60)
                        net(d, [(bx - math.cos(g) * 6, by - math.sin(g) * 6),
                                (bx + math.cos(g) * 6, by + math.sin(g) * 6)],
                            "#6C90BA", 3)
    d.ellipse([x - w / 2 + o * khoanh + 8, y + 8,
               x - w / 2 + o * (khoanh + 1) - 8, y + h - 8],
              outline="#C0392B", width=6)


def bang_mau(d, x, y, r=64):
    """Bảng màu tròn chia sáu ô — chỗ để hỏi "What colour is it?"."""
    for i, m in enumerate(("#C0392B", "#F9B233", "#4E9A4E", "#0B4EA8",
                           "#7E57C2", "#1FCBAB")):
        d.pieslice([x - r, y - r, x + r, y + r], i * 60, (i + 1) * 60,
                   fill=m, outline=INK, width=3)
    tron(d, x, y, r * 0.24, "#FFFFFF", INK, 3)


def huy_chuong(d, x, y, r=30):
    """Tấm huy chương vàng có dải ruy băng đỏ."""
    d.polygon([(x - r * 0.7, y - r * 2.1), (x, y - r * 0.6), (x + r * 0.7, y - r * 2.1)],
              fill="#C0392B", outline=INK, width=3)
    tron(d, x, y, r, "#FFD84D", "#E09B18", 4)
    tron(d, x, y, r * 0.52, "#F9B233", "#E09B18", 3)


def long_chim(d, x, y, cao=210):
    """Lồng chim treo trên giá. (x, y) là chân giá.

    ⚠ Có prop này vì bản đầu tôi thả con chim lơ lửng giữa trời cho khớp mô tả
    "lồng chim treo trên giá" — mà mô tả ấy bác đã duyệt, nên phải vẽ ĐÚNG cái
    lồng chứ không được hạ con chim xuống hàng rào rồi coi như xong. Tranh lệch
    mô tả là mở ra hai bản sự thật; xem [[hinh-trong-video-phai-khop-loi-doc]].
    """
    net(d, [(x, y), (x, y - cao)], "#8A6B45", 11)
    net(d, [(x, y - cao), (x + cao * 0.30, y - cao)], "#8A6B45", 9)
    r = cao * 0.24
    cx, cy = x + cao * 0.30, y - cao + r * 1.15
    khoi(d, cx - r, cy - r * 0.15, r * 2, r * 1.9, "#EAF2FB", INK, 4, bo=r * 0.3)
    d.pieslice([cx - r, cy - r * 1.1, cx + r, cy + r * 0.9], 180, 360,
               fill="#EAF2FB", outline=INK, width=4)
    for i in range(1, 5):
        net(d, [(cx - r + r * 2 * i / 5, cy - r * 0.9),
                (cx - r + r * 2 * i / 5, cy + r * 1.7)], INK, 3)
    khoi(d, cx - r * 1.05, cy + r * 1.6, r * 2.1, r * 0.3, "#8A6B45", INK, 4, bo=3)


def guong(d, x, y, w=210, h=270):
    khoi(d, x - w / 2, y, w, h, "#8A6B45", INK, 6, bo=8)
    khoi(d, x - w / 2 + 14, y + 14, w - 28, h - 28, "#DCEAF6", INK, 4, bo=4)


# ══════════════════════════════ PHÔNG NỀN ══════════════════════════════
def _dai(d, y1, y2, mau):
    d.rectangle([0, int(y1), W, int(y2)], fill=mau)


def nen_lop(d, o):
    """Trong lớp: tường kem, sàn gỗ, chân tường."""
    san = o.get("san", 560)
    _dai(d, TRAN, san, "#F6EEDC")
    _dai(d, san - 12, san + 6, "#C8A87C")
    _dai(d, san + 6, H, "#D9BE94")
    for i in range(1, 7):                       # ván sàn
        net(d, [(W * i / 7 - 60, san + 6), (W * i / 7 - 150, H)], "#C8A87C", 3)


def nen_phong(d, o):
    """Trong nhà: tường ấm hơn lớp học, sàn gỗ sẫm."""
    san = o.get("san", 560)
    _dai(d, TRAN, san, "#F1E4D3")
    _dai(d, san - 12, san + 6, "#B08D63")
    _dai(d, san + 6, H, "#C9A575")
    for i in range(1, 7):
        net(d, [(W * i / 7 - 60, san + 6), (W * i / 7 - 150, H)], "#B08D63", 3)


def nen_san(d, o):
    """Sân trường: trời, dãy nhà ở xa, sân gạch đỏ."""
    dat = o.get("san", 540)
    _dai(d, TRAN, dat, "#BFE3F7")
    _dai(d, dat, H, "#C9714E")
    for i in range(1, 6):
        net(d, [(0, dat + (H - dat) * i / 5), (W, dat + (H - dat) * i / 5)],
            "#B05F41", 3)


def nen_co(d, o):
    """Ngoài trời: trời và bãi cỏ."""
    dat = o.get("san", 520)
    _dai(d, TRAN, dat, "#BFE3F7")
    _dai(d, dat, H, "#8CC96B")
    _dai(d, dat, dat + 10, "#6FAE53")


def nen_pho(d, o):
    """Phố: trời, dãy nhà, vỉa hè, lòng đường."""
    he = o.get("he", 520)
    duong = o.get("duong", 610)
    _dai(d, TRAN, he, "#BFE3F7")
    _dai(d, he, duong, "#D8D2C6")
    _dai(d, duong, H, "#6E6E6E")
    _dai(d, duong, duong + 8, "#4F4F4F")
    x = 60                                       # vạch kẻ giữa đường
    while x < W:
        d.rectangle([x, (duong + H) / 2 - 6, x + 78, (duong + H) / 2 + 6],
                    fill="#F5F5F5")
        x += 150


def nen_toi(d, o):
    """Chạng vạng bên hồ: trời tím, mặt hồ, bờ cỏ sẫm."""
    dat = o.get("san", 470)
    _dai(d, TRAN, dat - 90, "#5B4C86")
    _dai(d, dat - 90, dat, "#8E7BB5")
    _dai(d, dat, dat + 80, "#3F5E86")            # mặt hồ
    _dai(d, dat + 80, H, "#3E6B45")
    for i in range(6):
        net(d, [(120 + i * 190, dat + 26 + (i % 3) * 16),
                (250 + i * 190, dat + 26 + (i % 3) * 16)], "#6C90BA", 4)


NEN = {"lop": nen_lop, "phong": nen_phong, "san": nen_san,
       "co": nen_co, "pho": nen_pho, "toi": nen_toi}

# Bảng tra cho bản khai: tên trong JSON → hàm vẽ.
VE = {"nguoi": nguoi, "cay": cay, "may": may, "matTroi": mat_troi,
      "bang": bang_den, "cuaSo": cua_so, "cua": cua, "ban": ban, "ghe": ghe,
      "giaSach": gia_sach, "giuong": giuong, "sofa": sofa,
      "khungAnh": khung_anh, "bangGhim": bang_ghim, "bangLuoi": bang_luoi,
      "dongHo": dong_ho, "giaVe": gia_ve, "luaTrai": lua_trai, "leu": leu,
      "hangRao": hang_rao, "songSat": song_sat, "nha": nha, "oto": oto,
      "tuKinh": tu_kinh, "longChim": long_chim, "banDo": ban_do,
      "anhNho": anh_nho, "bangMau": bang_mau, "bangThoiTiet": bang_thoi_tiet, "matTrang": mat_trang, "huyChuong": huy_chuong, "bienBao": bien_bao, "guong": guong}
