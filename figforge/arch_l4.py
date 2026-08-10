# -*- coding: utf-8 -*-
"""
Nguyên mẫu riêng cho LỚP 4.

Mười bảy trên hai mươi mốt nhóm hình lớp 4 dùng lại được nguyên mẫu của lớp 2 và
lớp 3 (xem `docs/phan_loai_hinh_lop4.md`). Nên tệp này KHÔNG chép lại chúng — nó
nhập thẳng từ `arch_l3` (vốn đã nhập của `arch_l2`) rồi chỉ viết thêm phần lớp 4
mới có. Bộ vẽ tra nguyên mẫu bằng `getattr(arch_l4, tên)`, nên nhập vào đây là đủ
để dùng, và sửa một nguyên mẫu lớp 2 thì hình lớp 4 được sửa theo — thứ mà bản chép
tay không làm được.

Bốn nguyên mẫu lớp 4 phải dựng mới:
    phan_so_lat      chương 9 · so sánh phân số, phân số của một số, rút gọn
    cot_san_bang     chương 5 · trung bình cộng — cột cao bị san xuống cột thấp
    khai_trien_hop   bài 41  · hộp giấy trải phẳng, đếm đủ 6 mặt
    goc_kim          bài 44  · góc hai kim đồng hồ, ĐẾM ĐƯỢC từng khấc
"""
import math

from core import (canvas, save, txt_fit, txt_wrap, _txt, FS, card,
                  NAVY, TEAL, GOLD, RED, DARKTEAL, INK, MUTE, LINE, SOFT,
                  PALETEAL, PALERED, DARKGOLD, BG)
from matplotlib.patches import Wedge, Rectangle, FancyBboxPatch, Polygon, Circle
import arch_l3
from arch_l3 import (MAU,                                          # noqa: F401
                     hinh_tron, luoi_dien_tich, ven_hai_vong, lich_thang,
                     can_ong_dong, tien_viet, bieu_thuc_ngoac,
                     may_bien_doi, day_o, hang_hop, cham_tron, con_vat,
                     doan_thang, tia_so, hinh_phang, khoi_hop, bang_luoi,
                     bap_benh, noi_cap, cau_truc_so, dong_ho, hang_cay,
                     ban_tay, loi_thoai, hinh_ghep, thap_khoi, dong_hinh,
                     hinh_chu_vi, dong_xu_cham)

_MAU = {'teal': TEAL, 'gold': GOLD, 'navy': NAVY, 'do': RED}


def _m(ten, mac_dinh=TEAL):
    return _MAU.get(ten, mac_dinh)


def phan_so_lat(p, out):
    """
    PHÂN SỐ — cái bánh chia lát, tô mấy lát lấy đi.

    LUẬT CỐT TỬ: mọi cái bánh trong CÙNG một bức phải **to bằng nhau**. Bài "lát nào
    to hơn" chỉ có nghĩa khi hai phân số cùng đo trên một cái bánh như nhau — vẽ bánh
    1/2 to hơn bánh 1/3 là bé nhìn ra ngay "cái to hơn", đúng thứ bài đang bắt so.
    Đây là bẫy 26 (cỡ vẽ tính riêng từng nhóm) mặc áo phân số.

    params:
      title · note
      banh: [{tu, mau, ten, nhan, kieu}]
        tu       tử số — mấy lát được tô
        mau      chia mấy lát (mẫu số)
        ten      nhãn dưới hình, thường là phân số viết bằng chữ
        nhan     dòng nhỏ dưới nhãn (ví dụ "= 6 cái bánh")
        kieu     'tron' (mặc định) | 'thanh' — thanh cho bài "phân số của một số"
      so: True → ghi phân số to giữa hình
    """
    banh = p.get('banh') or []
    n = max(len(banh), 1)
    co_note = bool(p.get('note'))
    fig, ax, H = canvas(7.2, 4.2 if co_note else 3.6)
    txt_fit(ax, 50, H - 5, p.get('title', ''), 92, FS['title'], NAVY)

    # MỘT cỡ dùng chung cho cả bức, tính một lần — xem ghi chú ở đầu hàm
    o_rong = min(84 / n, 30)
    r = min(o_rong * 0.34, 11.5)
    # chừa chỗ cho hai dòng nhãn dưới hình VÀ cho dòng chốt, không thì chúng đè nhau
    yc = H / 2 + (1.6 if co_note else -1.0)
    x0 = 50 - (o_rong * n) / 2

    for i, b in enumerate(banh):
        cx = x0 + o_rong * (i + 0.5)
        mau_so = max(int(b.get('mau', 1)), 1)
        tu = max(int(b.get('tu', 0)), 0)
        c = _m(b.get('mauSac', 'teal'))
        if b.get('kieu') == 'thanh':
            w, h = o_rong * 0.78, r * 1.1
            xa, ya = cx - w / 2, yc - h / 2
            for k in range(mau_so):
                ax.add_patch(Rectangle((xa + w * k / mau_so, ya), w / mau_so, h,
                                       fc=c if k < tu else 'white',
                                       ec=NAVY, lw=1.6, zorder=4))
        else:
            # lát vẽ từ 12 giờ đi thuận kim đồng hồ — bé đọc như đọc đồng hồ
            for k in range(mau_so):
                a1 = 90 - 360 * (k + 1) / mau_so
                a2 = 90 - 360 * k / mau_so
                ax.add_patch(Wedge((cx, yc), r, a1, a2,
                                   fc=c if k < tu else 'white',
                                   ec=NAVY, lw=1.6, zorder=4))
        if p.get('so', True):
            _txt(ax, cx, yc - r - 4.6, f'{tu}/{mau_so}', fs=FS['big'], c=NAVY,
                 w='bold', z=6)
        if b.get('ten'):
            txt_fit(ax, cx, yc - r - 9.2, b['ten'], o_rong - 2, FS['small'],
                    DARKTEAL, z=6)
        if b.get('nhan'):
            txt_fit(ax, cx, yc + r + 4.2, b['nhan'], o_rong - 2, FS['small'],
                    MUTE, z=6)
    if p.get('note'):
        txt_fit(ax, 50, 3.4, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def cot_san_bang(p, out):
    """
    TRUNG BÌNH CỘNG — mấy cột cao thấp, và vạch mức san đều cắt ngang.

    Bé phải NHÌN RA phần vượt trên vạch bằng đúng phần hụt dưới vạch: đó là cả bài
    học của chương. Nên phần vượt tô vàng, phần hụt kẻ sọc, và hai con số ấy ghi
    thẳng lên hình — không bắt bé nhẩm.

    params:
      title · note
      cot: [{ten, cao}]        cao = giá trị thật của từng số
      muc: số                  mức trung bình cộng; bỏ trống thì tự tính
      nhanMuc: chữ ghi cạnh vạch mức (mặc định "trung bình cộng")
      hieuSo: True → ghi "+n" / "−n" lên phần vượt và phần hụt
    """
    cot = p.get('cot') or []
    n = max(len(cot), 1)
    gia = [float(c.get('cao', 0)) for c in cot]
    muc = float(p['muc']) if p.get('muc') is not None else (sum(gia) / n if n else 0)
    dinh = max(gia + [muc]) or 1

    fig, ax, H = canvas(7.2, 4.0)
    txt_fit(ax, 50, H - 5, p.get('title', ''), 92, FS['title'], NAVY)

    day, tran = 12.0, H - 12.0
    thang = (tran - day) / dinh
    o = min(76 / n, 17)
    x0 = 50 - (o * n) / 2
    ax.plot([x0 - 4, x0 + o * n + 4], [day, day], color=INK, lw=2.0, zorder=3)

    for i, c in enumerate(cot):
        cx = x0 + o * (i + 0.5)
        w = o * 0.62
        h = gia[i] * thang
        hm = muc * thang
        # phần nằm trong mức: thân cột; phần vượt: vàng; phần hụt: khung nét đứt
        ax.add_patch(Rectangle((cx - w / 2, day), w, min(h, hm), fc=TEAL,
                               ec=NAVY, lw=1.5, zorder=4))
        if h > hm:
            ax.add_patch(Rectangle((cx - w / 2, day + hm), w, h - hm, fc=GOLD,
                                   ec=NAVY, lw=1.5, zorder=5))
        elif h < hm:
            ax.add_patch(Rectangle((cx - w / 2, day + h), w, hm - h, fc='white',
                                   ec=RED, lw=1.5, ls=(0, (3, 2)), zorder=5))
        _txt(ax, cx, day + max(h, hm) + 3.2, f'{gia[i]:g}', fs=FS['mid'], c=NAVY,
             w='bold', z=7)
        txt_fit(ax, cx, day - 4.2, str(c.get('ten', '')), o - 1, FS['small'],
                DARKTEAL, z=6)
        if p.get('hieuSo') and abs(h - hm) > 0.1:
            d = gia[i] - muc
            _txt(ax, cx, day + (min(h, hm) + max(h, hm)) / 2,
                 f'{d:+g}', fs=FS['small'], c=DARKGOLD if d > 0 else RED,
                 w='bold', z=8)

    ym = day + muc * thang
    ax.plot([x0 - 4, x0 + o * n + 4], [ym, ym], color=RED, lw=2.2,
            ls=(0, (5, 3)), zorder=6)
    _txt(ax, x0 + o * n + 5.5, ym, f"{p.get('nhanMuc', 'trung bình cộng')} {muc:g}",
         fs=FS['small'], c=RED, w='bold', ha='left', z=7)
    if p.get('note'):
        txt_fit(ax, 50, 4.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def khai_trien_hop(p, out):
    """
    HỘP GIẤY TRẢI PHẲNG — hình chữ thập sáu mặt, đếm được từng mặt.

    Khác hẳn `khoi_hop` (vẽ khối nhìn nghiêng): ở đây bé phải thấy ĐỦ SÁU MẶT nằm
    rời trên mặt bàn, và thấy mặt nào đối diện mặt nào. Ghi số đo lên từng mặt, vì
    bài diện tích xung quanh - toàn phần phải cộng đúng từng mặt.

    params:
      title · note
      dai · rong · cao      ba kích thước (đơn vị tuỳ đề, chỉ dùng để ghi nhãn)
      donVi                 'cm' mặc định
      danhSo: True          → đánh số 1..6 lên các mặt cho bài đếm mặt
      to: ['tren','duoi',…] → tô đậm những mặt nào (đáy · nắp · xung quanh)
    """
    d = float(p.get('dai', 4)); r = float(p.get('rong', 3)); c = float(p.get('cao', 2))
    dv = p.get('donVi', 'cm')
    to = set(p.get('to') or [])

    fig, ax, H = canvas(7.2, 4.6)
    txt_fit(ax, 50, H - 5, p.get('title', ''), 92, FS['title'], NAVY)

    # Hình trải phải ĐÚNG TỈ LỆ với hộp thật, không thì bài diện tích xung quanh
    # dạy ngược: bé thấy bốn mặt bên bằng nhau trong khi hai cặp khác hẳn nhau.
    # Dải giữa là bốn mặt XUNG QUANH đi vòng quanh hộp, cao đúng bằng `cao`:
    #     trước(dài×cao) · phải(rộng×cao) · sau(dài×cao) · trái(rộng×cao)
    # Nắp và đáy (dài×rộng) gắn trên - dưới mặt TRƯỚC.
    ngang, doc = 2 * d + 2 * r, c + 2 * r
    k = min(74 / max(ngang, 1), (H - 22) / max(doc, 1))
    D, R, C = d * k, r * k, c * k
    x0 = 50 - ngang * k / 2
    y0 = 11 + R                                   # đáy của dải giữa

    mat, x = [], x0
    for ten, w, loai in (('trước', D, 'xq'), ('phải', R, 'xq'),
                         ('sau', D, 'xq'), ('trái', R, 'xq')):
        mat.append((x, y0, w, C, ten, loai))
        x += w
    mat.append((x0, y0 + C, D, R, 'nắp', 'tren'))
    mat.append((x0, y0 - R, D, R, 'đáy', 'duoi'))

    for i, (mx, my, mw, mh, ten, loai) in enumerate(mat, 1):
        sang = (loai in to) or (ten in to)
        ax.add_patch(Rectangle((mx, my), mw, mh,
                               fc=PALETEAL if sang else 'white',
                               ec=NAVY, lw=1.8, zorder=4))
        lab = f'{i}' if p.get('danhSo') else ten
        _txt(ax, mx + mw / 2, my + mh / 2, lab, fs=FS['small'],
             c=DARKTEAL if sang else MUTE, w='bold', z=6)

    # Số đo ghi lên ĐÚNG CẠNH nó đo. Gộp thành một dòng "5 cm · 3 cm · 2 cm" dưới
    # hình thì bé không biết số nào của cạnh nào — chuẩn mục 4 cấm đúng chỗ này.
    _txt(ax, x0 + D / 2, y0 - R - 3.4, f'dài {d:g} {dv}', fs=FS['small'],
         c=NAVY, w='bold', z=7)
    _txt(ax, x0 - 2.4, y0 - R / 2, f'rộng {r:g} {dv}', fs=FS['small'], c=NAVY,
         w='bold', ha='right', z=7)
    _txt(ax, x0 + ngang * k + 2.4, y0 + C / 2, f'cao {c:g} {dv}',
         fs=FS['small'], c=NAVY, w='bold', ha='left', z=7)
    if p.get('note'):
        txt_fit(ax, 50, 3.8, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def goc_kim(p, out):
    """
    GÓC HAI KIM ĐỒNG HỒ — 12 khấc đều, cung góc tô rõ, ĐẾM ĐƯỢC từng khấc.

    Bài 44 hỏi "hai kim cách nhau mấy khấc" nên khấc phải đếm được TRÊN HÌNH: vẽ đủ
    12 vạch, và tô cung đúng số khấc giữa hai kim. Ghi sẵn "3 khấc" mà chỉ vẽ một
    vạch là bé không đếm gì — bẫy 22.

    params:
      title · note
      gio · phut        vị trí hai kim (phút thường là 0)
      soKhac            số khấc muốn tô; bỏ trống thì tự tính theo phía NGẮN
      tenGoc            'GÓC VUÔNG' | 'GÓC NHỌN' | … — bỏ trống thì KHÔNG ghi
                        (bản ĐỀ của màn mở phải bỏ, vì đó chính là đáp án)
    """
    gio = float(p.get('gio', 3)) % 12
    phut = float(p.get('phut', 0)) % 60
    fig, ax, H = canvas(7.2, 4.2)
    txt_fit(ax, 50, H - 5, p.get('title', ''), 92, FS['title'], NAVY)

    cx, cy, R = 50, H / 2 - 2.5, min(H / 2 - 8, 15)
    ax.add_patch(Circle((cx, cy), R, fc='white', ec=NAVY, lw=2.4, zorder=3))

    # góc kim: 12 giờ ở đỉnh, đi thuận kim đồng hồ
    a_phut = 90 - 6 * phut
    a_gio = 90 - 30 * (gio + phut / 60)

    # cung góc — tô TRƯỚC để nằm dưới kim và dưới vạch
    d = (a_phut - a_gio) % 360
    ngan = min(d, 360 - d)
    khac = p.get('soKhac')
    khac = round(ngan / 30) if khac is None else khac
    a1, a2 = (a_gio, a_phut) if d <= 180 else (a_phut, a_gio)
    ax.add_patch(Wedge((cx, cy), R * 0.55, a1, a2, fc=GOLD, ec='none',
                       alpha=0.55, zorder=4))

    for k in range(12):
        a = math.radians(90 - 30 * k)
        x1, y1 = cx + R * 0.88 * math.cos(a), cy + R * 0.88 * math.sin(a)
        x2, y2 = cx + R * math.cos(a), cy + R * math.sin(a)
        ax.plot([x1, x2], [y1, y2], color=NAVY, lw=2.2, zorder=5)
        xt, yt = cx + R * 0.74 * math.cos(a), cy + R * 0.74 * math.sin(a)
        _txt(ax, xt, yt, str(12 if k == 0 else k), fs=FS['small'], c=MUTE, z=6)

    for a, ln, lw, c in ((a_gio, 0.46, 4.2, NAVY), (a_phut, 0.70, 3.0, TEAL)):
        ar = math.radians(a)
        ax.plot([cx, cx + R * ln * math.cos(ar)], [cy, cy + R * ln * math.sin(ar)],
                color=c, lw=lw, solid_capstyle='round', zorder=7)
    ax.add_patch(Circle((cx, cy), 1.0, fc=NAVY, ec='none', zorder=8))

    _txt(ax, cx, cy - R - 4.6, f'{khac} khấc', fs=FS['mid'], c=DARKGOLD,
         w='bold', z=7)
    if p.get('tenGoc'):
        _txt(ax, cx, cy - R - 9.0, p['tenGoc'], fs=FS['mid'], c=RED, w='bold', z=7)
    if p.get('note'):
        txt_fit(ax, 50, 3.6, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)
