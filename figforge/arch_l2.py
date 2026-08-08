# -*- coding: utf-8 -*-
"""
Nguyên mẫu riêng cho LỚP 2.

Khác Quyển 2 lớp 5: ở đó 53 sơ đồ đều CÙNG một khuôn (bảng chữ hai cột) nên một
nguyên mẫu là đủ. Hình lớp 2 là hình toán thật, 75 hình chia thành 15 nhóm — xem
docs/phan_loai_hinh_lop2.md. Tệp này dựng dần từng nhóm.

Đã có:
  may_bien_doi  — nhóm "Máy biến đổi" (4 hình: image2, image8, image32, image51)
"""
from core import (canvas, card, save, txt_fit, arrow, _txt,
                  NAVY, TEAL, GOLD, RED, DARKTEAL, DARKGOLD, PALERED, PALETEAL, FS)

# Ba vai màu của một ô: (viền, nền, chữ)
MAU = {
    'teal': (TEAL, PALETEAL, DARKTEAL),
    'gold': (GOLD, '#FFF4DF', DARKGOLD),
    'do':   (RED, PALERED, RED),
}

W_O, W_MAY = 1.0, 2.35      # bề ngang tương đối: máy rộng hơn ô số
KHE = 9.5                   # khoảng hở giữa hai ô — chỗ để vẽ mũi tên
LE_T, LE_P = 6.0, 94.0


def _do_hang(o):
    """Tính (x, bề ngang) cho từng ô trong một hàng."""
    trong = [W_MAY if c.get('may') else W_O for c in o]
    con_lai = (LE_P - LE_T) - KHE * (len(o) - 1)
    donvi = con_lai / sum(trong)
    ra, x = [], LE_T
    for t in trong:
        w = donvi * t
        ra.append((x, w))
        x += w + KHE
    return ra


def may_bien_doi(p, out):
    """
    params:
      title  tiêu đề trên cùng
      rows   [{'mau': 'teal'|'do', 'nguoc': bool, 'o': [ô, …]}, …]
             ô = {'may': 'MÁY × 3'}            → hộp máy (nền trắng, viền theo màu hàng)
                 {'t': '15', 'mau': 'gold'}    → ô số (mặc định 'gold')
      giua   dòng chữ chen giữa hai hàng (tuỳ chọn)
      note   dòng chốt dưới cùng (tuỳ chọn)

    Hàng 'nguoc' vẽ mũi tên chỉ sang TRÁI — đó là ý chính của cả nhóm hình này:
    máy chạy ngược thì vừa đổi chiều vừa đảo phép tính.
    """
    rows = p.get('rows') or []
    if not rows:
        raise ValueError('may_bien_doi cần ít nhất một hàng')

    CAO_O = 13.0
    khe_hang = 15.0 if p.get('giua') else 8.0
    tren = 11.0 if p.get('title') else 4.0
    duoi = 8.0 if p.get('note') else 4.0
    can = tren + CAO_O * len(rows) + khe_hang * (len(rows) - 1) + duoi

    fig, ax, H = canvas(7.6, max(2.6, can * 7.6 / 100))

    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren - CAO_O
    day = y                     # đáy của hàng cuối — mốc đặt dòng chốt
    for i, hang in enumerate(rows):
        mau_hang = hang.get('mau', 'teal')
        vien_hang = MAU[mau_hang][0]
        nguoc = bool(hang.get('nguoc'))
        o = hang['o']
        vitri = _do_hang(o)

        for (x, w), c in zip(vitri, o):
            if c.get('may'):
                # hộp máy: nền trắng cho nổi trên nền giấy, viền + chữ theo màu hàng
                card(ax, x, y, w, CAO_O, fc='white', ec=vien_hang, lw=2.2, r=1.8)
                txt_fit(ax, x + w / 2, y + CAO_O / 2, c['may'], w - 4,
                        FS['mid'], MAU[mau_hang][2], z=5)
            else:
                vien, nen, chu = MAU[c.get('mau', 'gold')]
                card(ax, x, y, w, CAO_O, fc=nen, ec=vien, lw=2.2, r=1.8)
                txt_fit(ax, x + w / 2, y + CAO_O / 2, str(c.get('t', '')), w - 3,
                        FS['big'], chu, z=5)

        # mũi tên nối các ô; hàng ngược thì đầu nhọn quay sang trái
        for j in range(len(vitri) - 1):
            (x1, w1), (x2, _) = vitri[j], vitri[j + 1]
            trai, phai = x1 + w1 + 1.0, x2 - 1.0
            p1, p2 = ((phai, y + CAO_O / 2), (trai, y + CAO_O / 2)) if nguoc \
                else ((trai, y + CAO_O / 2), (phai, y + CAO_O / 2))
            arrow(ax, p1, p2, c=vien_hang, lw=3.2, ms=18, z=4)

        if i == 0 and p.get('giua'):
            txt_fit(ax, 50, y - khe_hang / 2, p['giua'], 92, FS['body'], RED, z=6)
        day = y
        y -= CAO_O + khe_hang

    # tính từ ĐÁY HÀNG CUỐI, không phải từ y — y đã bị trừ thêm một lần ở vòng cuối,
    # ra toạ độ âm thì bbox_inches='tight' nới khung và chừa một khoảng trống to
    if p.get('note'):
        txt_fit(ax, 50, day - 4.6, p['note'], 92, FS['body'], DARKTEAL, z=5)

    save(fig, out)
