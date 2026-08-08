# -*- coding: utf-8 -*-
"""
Nguyên mẫu riêng cho LỚP 2.

Khác Quyển 2 lớp 5: ở đó 53 sơ đồ đều CÙNG một khuôn (bảng chữ hai cột) nên một
nguyên mẫu là đủ. Hình lớp 2 là hình toán thật, 75 hình chia thành 15 nhóm — xem
docs/phan_loai_hinh_lop2.md. Tệp này dựng dần từng nhóm.

Đã có:
  may_bien_doi  — nhóm "Máy biến đổi" (4 hình: image2, image8, image32, image51)
"""
from core import (canvas, card, save, txt_fit, arrow, _txt, fit_fs,
                  NAVY, TEAL, GOLD, RED, DARKTEAL, DARKGOLD, PALERED, PALETEAL,
                  LINE, MUTE, FS)

# Ba vai màu của một ô: (viền, nền, chữ)
MAU = {
    'teal': (TEAL, PALETEAL, DARKTEAL),
    'gold': (GOLD, '#FFF4DF', DARKGOLD),
    'do':   (RED, PALERED, RED),
    'tim':  ('#7E57C2', '#EDE7F6', '#4527A0'),
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


def _o(ax, x, y, w, h, c, r=1.8, fs=None):
    """Một ô số. `c` là dict: t (chữ), mau, mo (làm mờ), danh (dấu ✓/✗ phía trên)."""
    mau = c.get('mau', 'teal')
    vien, nen, chu = MAU.get(mau, MAU['teal'])
    if c.get('mo'):                      # ô mờ = ô KHÔNG được đếm, không phải ô trống
        vien, nen, chu = LINE, '#F2F4F7', MUTE
    card(ax, x, y, w, h, fc=nen, ec=vien, lw=2.2, r=r)
    _txt(ax, x + w / 2, y + h / 2, str(c.get('t', '')), fs=fs or FS['big'], c=chu, w='bold', z=6)
    if c.get('duoi'):
        txt_fit(ax, x + w / 2, y - 3.0, str(c['duoi']), w + 3, FS['tiny'], MUTE, z=6, w='normal')
    if c.get('danh'):
        txt_fit(ax, x + w / 2, y + h + 3.0, str(c['danh']), w, FS['body'],
                TEAL if c['danh'] == '✓' else RED, z=6)


def _banh_xe(ax, x, w, y):
    """Hai bánh xe dưới một toa tàu — vẽ đúng cái bé nhìn thấy, không phải hình trang trí."""
    from matplotlib.patches import Circle
    for dx in (0.28, 0.72):
        ax.add_patch(Circle((x + w * dx, y - 1.6), 1.5, fc='#4A4A4A', ec='#333', lw=1, zorder=7))


def day_o(p, out):
    """
    Dãy ô số nằm ngang — nhóm hình nhiều nhất của lớp 2 (13 hình).

    params:
      title  tiêu đề
      hang   [{nhan, o:[ô…], cung:[{tu,den,nhan}], tau:bool}, …]
             ô = {t, mau: teal|gold|do|tim, mo, danh, duoi}
      note   dòng chốt

    `cung` vẽ mũi tên vòng từ ô `tu` sang ô `den` kèm nhãn (+3, ×2…) — đó là chỗ bé
    phải nhìn ra NHỊP của dãy. `tau` thì thêm đầu tàu và bánh xe.
    """
    hang = p.get('hang') or []
    co_cung = any(h.get('cung') for h in hang)
    co_banh = any(h.get('tau') or h.get('banh') for h in hang)
    co_duoi = any(c.get('duoi') for h in hang for c in h['o'])
    # Hàng nào cũng có nhãn thì phải CHỪA chỗ bên trái, nếu không nhãn đè lên ô đầu.
    co_nhan = any(h.get('nhan') for h in hang)
    LE_NHAN = 17.0 if co_nhan else 0.0
    KHE_O = 2.6
    # Ô rộng bao nhiêu thì cao bấy nhiêu (có trần), để hàng 10 ô không thành
    # những cột dọc lêu nghêu mà hàng 3 ô cũng không thành băng dẹt.
    nhieu_nhat = max((len(h['o']) for h in hang), default=1)
    _rong = (94.0 - 6.0 - KHE_O * (nhieu_nhat - 1)) / nhieu_nhat
    CAO = max(8.0, min(13.0, _rong * 1.15))
    # Khoảng cách hàng vừa đủ: có cung nhảy thì phải chừa chỗ cho cung và nhãn của nó,
    # không có thì để sát lại — hàng cách nhau quá xa là mắt bé không gom được thành dãy.
    KHE_H = 19.0 if co_cung else (10.5 if co_duoi else 7.0)
    tren = 11.0 if p.get('title') else 4.0
    tren += 9.0 if co_cung else 0.0
    duoi = 8.0 if p.get('note') else 6.0
    can = tren + CAO * len(hang) + KHE_H * (len(hang) - 1) + duoi
    fig, ax, H = canvas(7.6, max(2.4, can * 7.6 / 100))

    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren - CAO
    day = y
    for h in hang:
        o = h['o']
        x0 = 6.0 + LE_NHAN
        banh = h.get('tau') or h.get('banh')
        if h.get('tau'):
            x0 = max(x0, 20.0)
            card(ax, 5.0, y, 12.0, CAO, fc='#9FB6DE', ec=NAVY, lw=2.2, r=1.6)
            card(ax, 7.0, y + CAO * 0.45, 6.0, CAO * 0.42, fc='#DCE6F5', ec=NAVY, lw=1.4, r=0.8)
            _banh_xe(ax, 5.0, 12.0, y)
        rong = (94.0 - x0 - KHE_O * (len(o) - 1)) / len(o)
        vt = [x0 + i * (rong + KHE_O) for i in range(len(o))]
        if h.get('nhan'):
            txt_fit(ax, x0 - 2.5, y + CAO / 2, h['nhan'], LE_NHAN - 2, FS['body'],
                    NAVY, z=6, ha='right')
        # một cỡ chữ cho CẢ HÀNG: để "2" và "10" cùng cỡ, nhìn mới ra một dãy
        fs_hang = min(fit_fs(str(c.get('t', '')), rong - 3, FS['big']) for c in o)
        for x, c in zip(vt, o):
            _o(ax, x, y, rong, CAO, c, fs=fs_hang)
            if banh:
                _banh_xe(ax, x, rong, y)
        if banh:
            ax.plot([3, 97], [y - 3.6, y - 3.6], color='#C9CFD6', lw=2.5, zorder=1)
        for cg in h.get('cung') or []:
            a, b = vt[cg['tu']], vt[cg['den']]
            arrow(ax, (a + rong * 0.72, y + CAO + 0.8), (b + rong * 0.28, y + CAO + 0.8),
                  c=TEAL, lw=2.6, rad=-0.45, ms=14, z=5)
            txt_fit(ax, (a + b) / 2 + rong / 2, y + CAO + 7.2, cg.get('nhan', ''),
                    rong + KHE_O, FS['body'], DARKTEAL, z=6)
        day = y
        y -= CAO + KHE_H

    # tính từ ĐÁY HÀNG CUỐI (xem may_bien_doi): lấy `y` sau vòng lặp là thừa một
    # nhịp, dòng chốt rơi xuống tận đáy và hình hở một mảng trắng giữa chừng
    if p.get('note'):
        txt_fit(ax, 50, day - (7.0 if co_banh else (7.5 if co_duoi else 4.6)),
                p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)
