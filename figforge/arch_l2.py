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
                  LINE, MUTE, INK, FS)

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


def hang_hop(p, out):
    """
    Hàng hộp có nhãn — 9 hình. Mỗi hộp: một tiêu đề ngắn + vài dòng bên trong.

    params:
      title · hop[{ten, dong[], mau}] · ket (hộp kết luận nằm dưới) · note
    """
    hop = p.get('hop') or []
    n = len(hop)
    W = (92.0 - 3.0 * (n - 1)) / n
    sd = max(len(h.get('dong') or []) for h in hop) if hop else 1
    CAO = 12.0 + 4.6 * sd
    tren = 11.0 if p.get('title') else 4.0
    cao_ket = 11.0 if p.get('ket') else 0.0
    duoi = 7.0 if p.get('note') else 4.0
    can = tren + CAO + cao_ket + duoi
    fig, ax, H = canvas(7.6, max(2.4, can * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren - CAO
    for i, h in enumerate(hop):
        x = 4.0 + i * (W + 3.0)
        vien, nen, chu = MAU.get(h.get('mau', ['teal', 'gold', 'do', 'tim'][i % 4]), MAU['teal'])
        card(ax, x, y, W, CAO, fc=nen, ec=vien, lw=2.2, r=1.8)
        txt_fit(ax, x + W / 2, y + CAO - 4.2, h.get('ten', ''), W - 3, FS['body'], chu, z=6)
        for k, d in enumerate(h.get('dong') or []):
            txt_fit(ax, x + W / 2, y + CAO - 9.6 - k * 4.6, str(d), W - 3,
                    FS['small'], INK, z=6, w='normal')
    y -= cao_ket
    if p.get('ket'):
        card(ax, 20.0, y - 1.0, 60.0, 9.0, fc=PALETEAL, ec=TEAL, lw=2.2, r=1.6)
        txt_fit(ax, 50, y + 3.5, p['ket'], 56, FS['mid'], DARKTEAL, z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 5.0, p['note'], 92, FS['body'], MUTE, z=5, w='normal')
    save(fig, out)


def cham_tron(p, out):
    """
    Chấm tròn & chia nhóm — 5 hình. Bé ĐẾM ĐƯỢC từng chấm, đó là điểm mấu chốt.

    params:
      title · nhom[{ten, so, mau, hang}] · du{so, ten} · note
    """
    from matplotlib.patches import Circle
    nhom = p.get('nhom') or []
    du = p.get('du')
    n = len(nhom) + (1 if du else 0)
    W = (92.0 - 3.5 * (n - 1)) / n
    hmax = max([len(_chia_hang(g['so'], g.get('hang', 4))) for g in nhom] or [1])
    CAO = 9.0 + 5.6 * hmax
    tren = 11.0 if p.get('title') else 4.0
    duoi = 7.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + CAO + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren - CAO
    for i, g in enumerate(nhom + ([{'ten': du.get('ten', 'còn thừa'), 'so': du['so'],
                                    'mau': 'do'}] if du else [])):
        x = 4.0 + i * (W + 3.5)
        vien, nen, chu = MAU.get(g.get('mau', 'teal'), MAU['teal'])
        card(ax, x, y, W, CAO, fc='white', ec=vien, lw=2.0, r=1.8)
        hangs = _chia_hang(g['so'], g.get('hang', 4))
        for r, sl in enumerate(hangs):
            bw = min(3.4, (W - 6) / max(sl, 1) / 2)
            x0 = x + W / 2 - (sl - 1) * bw
            for k in range(sl):
                ax.add_patch(Circle((x0 + k * 2 * bw, y + CAO - 8.0 - r * 5.6), bw * 0.82,
                                    fc=nen, ec=vien, lw=1.6, zorder=5))
        txt_fit(ax, x + W / 2, y + 2.6, g.get('ten', ''), W - 3, FS['small'], chu, z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 4.6, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def _chia_hang(so, moi_hang):
    return [min(moi_hang, so - i * moi_hang) for i in range((so + moi_hang - 1) // moi_hang)] or [0]


def _dau_nguoi(ax, x, y, r, chan, mau='gold', ten=''):
    """Một con vật: đầu tròn có mặt cười + số chân que. Bé ĐẾM chân được."""
    from matplotlib.patches import Circle
    vien, nen, chu = MAU.get(mau, MAU['gold'])
    for k in range(chan):
        dx = (k - (chan - 1) / 2) * (r * 0.46)
        # Chân phải DÀI và tách rời để bé đếm được — đây là việc chính của hình này,
        # chân ngắn thành mấy cái gạch dính vào nhau thì đếm kiểu gì.
        ax.plot([x + dx, x + dx], [y - r * 0.55, y - r * 1.95], color=vien, lw=3.0,
                zorder=4, solid_capstyle='round')
    ax.add_patch(Circle((x, y), r, fc=nen, ec=vien, lw=2.2, zorder=5))
    for dx in (-r * 0.34, r * 0.34):
        ax.add_patch(Circle((x + dx, y + r * 0.24), r * 0.1, fc=NAVY, ec='none', zorder=6))
    ax.plot([x - r * 0.3, x, x + r * 0.3], [y - r * 0.22, y - r * 0.36, y - r * 0.22],
            color=NAVY, lw=1.8, zorder=6, solid_capstyle='round')
    if ten:
        _txt(ax, x, y - r * 2.35, ten, fs=FS['small'], c=chu, w='bold', z=6)


def con_vat(p, out):
    """
    Hàng con vật có chân — 5 hình. Đếm ĐẦU ra số con, đếm CHÂN ra số chân.

    params: title · con[{chan, mau, ten}] · note
    """
    con = p.get('con') or []
    n = max(len(con), 1)
    R = min(6.6, 84.0 / (n * 2.6))
    CAO = R * 4.6
    tren = 11.0 if p.get('title') else 4.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + CAO + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - R * 1.3
    buoc = 92.0 / n
    for i, c in enumerate(con):
        _dau_nguoi(ax, 4.0 + buoc * (i + 0.5), y, R, c.get('chan', 2),
                   c.get('mau', 'gold'), c.get('ten', ''))
    if p.get('note'):
        txt_fit(ax, 50, y - R * 2.95, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def doan_thang(p, out):
    """
    Sơ đồ đoạn thẳng — 2 hình. Mỗi bạn một thanh; thanh dài hơn = nhiều hơn.

    params: title · thanh[{ten, phan[{dai, nhan, mau}]}] · note
    """
    th = p.get('thanh') or []
    CAO, KHE = 9.5, 6.0
    tren = 11.0 if p.get('title') else 4.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.2, (tren + (CAO + KHE) * len(th) + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    tong = max(sum(x['dai'] for x in t['phan']) for t in th) if th else 1
    y = H - tren - CAO
    for t in th:
        txt_fit(ax, 15.0, y + CAO / 2, t.get('ten', ''), 13, FS['body'], NAVY, z=6, ha='right')
        x = 18.0
        for ph in t['phan']:
            w = 74.0 * ph['dai'] / tong
            vien, nen, chu = MAU.get(ph.get('mau', 'teal'), MAU['teal'])
            card(ax, x, y, w, CAO, fc=nen, ec=vien, lw=2.2, r=1.2)
            txt_fit(ax, x + w / 2, y + CAO / 2, str(ph.get('nhan', '')), w - 2,
                    FS['body'], chu, z=6)
            x += w
        y -= CAO + KHE
    if p.get('note'):
        txt_fit(ax, 50, y + KHE - 3.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def tia_so(p, out):
    """
    Tia số có bước nhảy — 2 hình. Bé thấy con số NHẢY từng bước bằng nhau.

    params: title · moc[{so, danh}] · nhan (chữ trên mỗi cung) · note
    """
    moc = p.get('moc') or []
    n = max(len(moc), 2)
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.0, (tren + 26.0 + (7.0 if p.get('note') else 3.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - 12.0
    ax.plot([5, 95], [y, y], color=NAVY, lw=2.8, zorder=3)
    # Đặt mốc theo GIÁ TRỊ, không chia đều: 18 → 20 → 21 mà vẽ cách đều nhau là
    # nói dối bé rằng ba khoảng ấy bằng nhau. Tia số sai tỉ lệ còn tệ hơn không có.
    gt = [float(m.get('so', 0)) for m in moc]
    lo, hi = min(gt), max(gt)
    xs = [8.0 + (84.0 * (v - lo) / (hi - lo) if hi > lo else 0) for v in gt]
    for x, m in zip(xs, moc):
        do = m.get('danh')
        ax.plot([x, x], [y - 2.2, y + 2.2], color=RED if do else NAVY, lw=2.6, zorder=4)
        _txt(ax, x, y - 5.6, str(m.get('so', '')), fs=FS['body'],
             c=RED if do else NAVY, w='bold', z=6)
        if do:
            from matplotlib.patches import Circle
            ax.add_patch(Circle((x, y), 3.2, fc='none', ec=RED, lw=2.4, zorder=5))
    # Cung nhảy chỉ nối các mốc THUỘC dãy. Mốc `danh` là ga tàu ĐI QUA chứ không
    # dừng — nối cung vào nó là vẽ ngược hẳn điều bài đang dạy.
    trong_day = [i for i, m in enumerate(moc) if not m.get('danh')]
    for a, b in zip(trong_day, trong_day[1:]):
        arrow(ax, (xs[a], y + 2.6), (xs[b], y + 2.6), c=TEAL, lw=2.4, rad=-0.5, ms=13, z=5)
        if p.get('nhan'):
            _txt(ax, (xs[a] + xs[b]) / 2, y + 9.6, p['nhan'], fs=FS['small'],
                 c=DARKTEAL, w='bold', z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 11.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)
