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
    o_ds = nhom + ([{'ten': du.get('ten', 'còn thừa'), 'so': du['so'],
                     'mau': 'do'}] if du else [])
    # CỠ CHẤM TÍNH MỘT LẦN CHO CẢ BỨC, theo hàng dài nhất ở BẤT KỲ nhóm nào.
    #
    # Bản trước tính riêng từng nhóm, nên nhóm nào xếp hàng ngắn thì chấm to hơn:
    # rương "3 viên xếp 1 hàng dọc" ra chấm bán kính 2,6 còn phần dư "2 viên một
    # hàng ngang" chỉ 1,3 — đúng một nửa. Cùng một viên ngọc mà vẽ hai cỡ trong
    # cùng một bức thì bé đếm vẫn ra số đúng, nhưng nhìn ra hai thứ khác nhau, và
    # bài chia có dư thì phần dư PHẢI trông y hệt phần đã chia.
    #
    # Đây là bẫy 26 của chuẩn, lần này nằm một tầng cao hơn: không phải giữa các
    # HÀNG trong một nhóm mà giữa các NHÓM trong một bức. Lời chú cũ nói "dùng
    # chung cho cả nhóm" — đúng chữ, nhưng cả nhóm chưa phải cả bức.
    rong_nhat = max([max(_chia_hang(g['so'], g.get('hang', 4))) for g in o_ds] or [1])
    bw = min(3.4, (W - 6) / rong_nhat / 2)
    for i, g in enumerate(o_ds):
        x = 4.0 + i * (W + 3.5)
        vien, nen, chu = MAU.get(g.get('mau', 'teal'), MAU['teal'])
        card(ax, x, y, W, CAO, fc='white', ec=vien, lw=2.0, r=1.8)
        hangs = _chia_hang(g['so'], g.get('hang', 4))
        for r, sl in enumerate(hangs):
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


def hinh_phang(p, out):
    """
    Hình học phẳng — 8 hình. Vẽ ĐÚNG hình, ghi số đo lên đúng cạnh.

    params: title · hinh[{loai, ten, canh[], chia, to_phan}] · note
      loai: tamgiac | vuong | chunhat | tron | tugiac
      chia: số phần chia đều (hình tròn) · to_phan: tô mấy phần
    """
    from matplotlib.patches import Circle, Polygon, Wedge, Rectangle
    hs = p.get('hinh') or []
    n = max(len(hs), 1)
    W = 88.0 / n
    tren = 11.0 if p.get('title') else 4.0
    CAO = min(30.0, W * 0.95)
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + CAO + 18.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - CAO / 2 - 2.0
    for i, h in enumerate(hs):
        cx = 6.0 + W * (i + 0.5)
        loai = h.get('loai', 'vuong')
        vien, nen, chu = MAU.get(h.get('mau', 'teal'), MAU['teal'])
        r = min(W * 0.36, CAO * 0.42)
        if loai == 'tron':
            ax.add_patch(Circle((cx, yc), r, fc=nen, ec=vien, lw=2.4, zorder=4))
            k = int(h.get('chia', 0) or 0)
            for j in range(k):
                import math
                a = 90 - j * 360 / k
                ax.plot([cx, cx + r * math.cos(math.radians(a))],
                        [yc, yc + r * math.sin(math.radians(a))], color=vien, lw=1.8, zorder=5)
            for j in range(int(h.get('to_phan', 0) or 0)):
                # tô ĐẬM: đây là phần bé phải nhìn ra, tô nhạt thì không phân biệt được
                ax.add_patch(Wedge((cx, yc), r, 90 - (j + 1) * 360 / k, 90 - j * 360 / k,
                                   fc='#F08A72', ec=vien, lw=2.0, zorder=5))
        elif loai == 'tamgiac':
            ax.add_patch(Polygon([(cx - r, yc - r * 0.8), (cx + r, yc - r * 0.8), (cx, yc + r)],
                                 fc=nen, ec=vien, lw=2.4, zorder=4))
        elif loai == 'tugiac':
            ax.add_patch(Polygon([(cx - r, yc - r * 0.7), (cx + r * 0.9, yc - r), 
                                  (cx + r * 0.7, yc + r * 0.85), (cx - r * 0.8, yc + r * 0.5)],
                                 fc=nen, ec=vien, lw=2.4, zorder=4))
        else:
            # HÌNH VUÔNG PHẢI VUÔNG. Cũ: rộng 2r × cao 1,6r — tức là chữ nhật, mà bài
            # lại đang dạy phân biệt vuông với chữ nhật. Nay lấy CẠNH BẰNG NHAU.
            cao = r * 1.6
            w2 = cao / 2 if loai == 'vuong' else r * 1.35
            ax.add_patch(Rectangle((cx - w2, yc - cao / 2), w2 * 2, cao,
                                   fc=nen, ec=vien, lw=2.4, zorder=4))
            # `luoi: [số hàng, số cột]` — kẻ vạch chia đều. Không có vạch thì bé
            # không thấy tờ giấy đã gấp làm mấy phần, chỉ đọc được con số ghi bên dưới.
            lh, lc = (h.get('luoi') or [1, 1])[:2]
            x0, y0 = cx - w2, yc - cao / 2
            for j in range(1, int(lc)):
                ax.plot([x0 + w2 * 2 * j / lc] * 2, [y0, y0 + cao],
                        color=vien, lw=1.8, zorder=5)
            for j in range(1, int(lh)):
                ax.plot([x0, x0 + w2 * 2], [y0 + cao * j / lh] * 2,
                        color=vien, lw=1.8, zorder=5)
        # Tên hình đọc TRƯỚC, dòng mô tả đọc sau — đúng thứ tự mắt bé đi xuống
        if h.get('ten'):
            _txt(ax, cx, yc - r - 4.2, h['ten'], fs=FS['body'], c=chu, w='bold', z=7)
        for k2, c in enumerate(h.get('canh') or []):
            _txt(ax, cx, yc - r - 9.0 - k2 * 4.0, c, fs=FS['small'], c=INK, w='normal', z=7)
    if p.get('note'):
        txt_fit(ax, 50, yc - CAO / 2 - 13.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def khoi_hop(p, out):
    """Khối hộp nhìn nghiêng — 3 hình. Vẽ mặt trước + mặt trên + mặt bên."""
    from matplotlib.patches import Polygon
    kh = p.get('khoi') or []
    n = max(len(kh), 1)
    W = 88.0 / n
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.2, (tren + 30.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - 12.0
    for i, k in enumerate(kh):
        cx = 6.0 + W * (i + 0.5)
        s = min(W * 0.30, 9.0) * k.get('to', 1.0)
        d = s * 0.42
        vien, nen, _ = MAU.get(k.get('mau', 'teal'), MAU['teal'])
        ax.add_patch(Polygon([(cx-s, yc-s), (cx+s, yc-s), (cx+s, yc+s), (cx-s, yc+s)],
                             fc=nen, ec=vien, lw=2.2, zorder=5))
        ax.add_patch(Polygon([(cx-s, yc+s), (cx-s+d, yc+s+d), (cx+s+d, yc+s+d), (cx+s, yc+s)],
                             fc='#FFF4DF', ec=vien, lw=2.2, zorder=4))
        ax.add_patch(Polygon([(cx+s, yc-s), (cx+s+d, yc-s+d), (cx+s+d, yc+s+d), (cx+s, yc+s)],
                             fc='#E8F1FA', ec=vien, lw=2.2, zorder=4))
        if k.get('ten'):
            for j, dg in enumerate(str(k['ten']).split('\n')):
                _txt(ax, cx, yc - s - 4.0 - j * 4.2, dg, fs=FS['small'], c=NAVY, w='bold', z=7)
    if p.get('note'):
        txt_fit(ax, 50, yc - 20.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def bang_luoi(p, out):
    """Bảng lưới — 3 hình. Ô tô màu là ô con phải chú ý."""
    cot = p.get('cot') or []
    hang = p.get('hang') or []
    to = {tuple(x) for x in (p.get('to') or [])}
    nc, nh = max(len(cot), 1), max(len(hang), 1)
    W = min(11.0, 86.0 / nc)
    CAO = min(7.0, W * 0.8)
    x0 = 50 - W * nc / 2
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.2, (tren + CAO * (nh + 1) + (9.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - CAO
    for j, c in enumerate(cot):
        _txt(ax, x0 + W * (j + 0.5), y + CAO / 2, str(c), fs=FS['small'], c=NAVY, w='bold', z=6)
    y -= CAO
    for i, h in enumerate(hang):
        for j, v in enumerate(h):
            sang = (i, j) in to
            card(ax, x0 + W * j, y, W, CAO, fc=MAU['gold'][1] if sang else 'white',
                 ec=MAU['gold'][0] if sang else LINE, lw=1.8 if sang else 1.0, r=0.6)
            _txt(ax, x0 + W * (j + 0.5), y + CAO / 2, str(v), fs=FS['small'],
                 c=DARKGOLD if sang else INK, w='bold' if sang else 'normal', z=6)
        y -= CAO
    if p.get('note'):
        txt_fit(ax, 50, y - 1.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def bap_benh(p, out):
    """Cân bập bênh — 2 hình. Bên nào nặng hơn thì bên ấy chúc xuống."""
    from matplotlib.patches import Polygon
    trai, phai = p.get('trai', {}), p.get('phai', {})
    nghieng = p.get('nghieng', 'phai')
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.0, (tren + 30.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - 14.0
    d = 5.0 if nghieng == 'phai' else -5.0
    ax.plot([18, 82], [yc + d, yc - d], color='#8D6E63', lw=4.0, zorder=4, solid_capstyle='round')
    ax.add_patch(Polygon([(50, yc - 8.5), (44, yc - 9.5), (56, yc - 9.5)],
                         fc='#B0BEC5', ec=MUTE, lw=1.8, zorder=3))
    for x, o, dy in ((22.0, trai, d), (78.0, phai, -d)):
        vien, nen, chu = MAU.get(o.get('mau', 'gold'), MAU['gold'])
        card(ax, x - 8.0, yc + dy + 1.5, 16.0, 11.0, fc=nen, ec=vien, lw=2.4, r=1.6)
        txt_fit(ax, x, yc + dy + 7.0, str(o.get('t', '')), 13, FS['big'], chu, z=6)
    if p.get('note'):
        txt_fit(ax, 50, yc - 14.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def noi_cap(p, out):
    """Cung nối cặp — 2 hình. Hai số nối với nhau là một cặp cộng lại tròn chục."""
    o = p.get('o') or []
    cap = p.get('cap') or []
    n = max(len(o), 1)
    W = min(9.0, 88.0 / n)
    x0 = 50 - W * n / 2
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.2, (tren + 34.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - 22.0
    vt = [x0 + W * (i + 0.5) for i in range(len(o))]
    for x, c in zip(vt, o):
        card(ax, x - W * 0.42, y, W * 0.84, 9.0, fc=MAU['teal'][1], ec=MAU['teal'][0], lw=2.2, r=1.4)
        _txt(ax, x, y + 4.5, str(c), fs=FS['mid'], c=DARKTEAL, w='bold', z=6)
    for k, cg in enumerate(cap):
        a, b = vt[cg['tu']], vt[cg['den']]
        cao = 5.0 + 3.2 * k
        arrow(ax, (a, y + 9.4), (b, y + 9.4), c=[TEAL, GOLD, '#7E57C2', RED][k % 4],
              lw=2.4, rad=-0.5 - 0.08 * k, ms=0, style='-', z=5)
        _txt(ax, (a + b) / 2, y + 9.4 + cao, cg.get('nhan', ''), fs=FS['small'],
             c=DARKTEAL, w='bold', z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 5.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def cau_truc_so(p, out):
    """
    Cấu trúc số — 4 hình: ngôi nhà trăm-chục-đơn vị, tách số, hạt→thanh, phố nhà.

    params: title · kieu (nha|tach|phonha) · … · note
    """
    from matplotlib.patches import Polygon, Rectangle, Circle
    kieu = p.get('kieu', 'nha')
    tren = 11.0 if p.get('title') else 4.0
    duoi = 8.0 if p.get('note') else 4.0

    if kieu == 'nha':
        phong = p.get('phong') or []
        # +12 để chừa chỗ cho MÁI NHÀ, nếu không mái đè lên tiêu đề
        fig, ax, H = canvas(7.6, max(2.6, (tren + 12.0 + 42.0 + duoi) * 7.6 / 100))
        if p.get('title'):
            txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
        # BỀ NGANG PHÒNG PHẢI CO THEO SỐ PHÒNG. Cũ đóng cứng 26: lớp 2 có ba tháp
        # (trăm - chục - đơn vị) nên vừa khít, nhưng lớp 3 xây thêm tháp NGHÌN thành
        # bốn phòng → 104 > 88, tràn hẳn ra ngoài khung, mái nhà bị cắt cụt hai đầu.
        # min() giữ nguyên 26 cho mọi hình ba phòng, nên hình lớp 2 không đổi một nét.
        y0, CAO = H - tren - 46.0, 30.0
        W = min(26.0, 88.0 / max(len(phong), 1))
        x0 = 50 - W * len(phong) / 2
        ax.add_patch(Polygon([(x0 - 3, y0 + CAO), (50, y0 + CAO + 10), (x0 + W * len(phong) + 3, y0 + CAO)],
                             fc='#F08A72', ec=RED, lw=2.2, zorder=3))
        for i, ph in enumerate(phong):
            x = x0 + W * i
            vien, nen, chu = MAU.get(ph.get('mau', 'teal'), MAU['teal'])
            ax.add_patch(Rectangle((x, y0), W, CAO, fc=nen, ec=NAVY, lw=2.2, zorder=4))
            _txt(ax, x + W / 2, y0 + CAO - 5.0, ph.get('ten', ''), fs=FS['body'], c=NAVY, w='bold', z=6)
            _txt(ax, x + W / 2, y0 + CAO - 13.0, str(ph.get('so', '')), fs=FS['big'] + 4, c=chu, w='bold', z=6)
            _txt(ax, x + W / 2, y0 + 4.0, ph.get('duoi', ''), fs=FS['tiny'], c=MUTE, w='normal', z=6)
        if p.get('note'):
            txt_fit(ax, 50, y0 - 5.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
        save(fig, out); return

    if kieu == 'tach':
        phan = p.get('phan') or []
        fig, ax, H = canvas(7.6, max(2.2, (tren + 32.0 + duoi) * 7.6 / 100))
        if p.get('title'):
            txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
        yt = H - tren - 11.0
        card(ax, 36.0, yt, 28.0, 11.0, fc='#E8F1FA', ec=NAVY, lw=2.6, r=1.8)
        txt_fit(ax, 50, yt + 5.5, str(p.get('so', '')), 24, FS['big'] + 5, NAVY, z=6)
        yb = yt - 20.0
        n = max(len(phan), 1)
        W = min(22.0, 88.0 / n)
        x0 = 50 - W * n / 2
        for i, v in enumerate(phan):
            x = x0 + W * i
            vien, nen, chu = MAU.get(['gold', 'teal', 'tim', 'do'][i % 4], MAU['gold'])
            card(ax, x + 1.5, yb, W - 3.0, 11.0, fc=nen, ec=vien, lw=2.4, r=1.6)
            txt_fit(ax, x + W / 2, yb + 5.5, str(v), W - 6, FS['big'], chu, z=6)
            arrow(ax, (50, yt - 0.5), (x + W / 2, yb + 12.0), c=TEAL, lw=2.2, ms=13, z=4)
            if i:
                _txt(ax, x - 0.2, yb + 5.5, '+', fs=FS['mid'], c=NAVY, w='bold', z=7)
        if p.get('note'):
            txt_fit(ax, 50, yb - 5.5, p['note'], 92, FS['body'], DARKTEAL, z=5)
        save(fig, out); return

    # phố nhà: hai hàng nhà, một bên lẻ một bên chẵn
    tren_ds, duoi_ds = p.get('tren') or [], p.get('duoi') or []
    n = max(len(tren_ds), len(duoi_ds), 1)
    W = min(15.0, 88.0 / n)
    fig, ax, H = canvas(7.6, max(2.4, (tren + 44.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    for hang, yy, mau in ((tren_ds, H - tren - 15.0, 'gold'), (duoi_ds, H - tren - 41.0, 'teal')):
        x0 = 50 - W * len(hang) / 2
        vien, nen, chu = MAU[mau]
        for i, v in enumerate(hang):
            x = x0 + W * i + W * 0.12
            w = W * 0.76
            ax.add_patch(Polygon([(x - 1, yy + 9.0), (x + w / 2, yy + 15.0), (x + w + 1, yy + 9.0)],
                                 fc='#F08A72', ec=RED, lw=1.8, zorder=4))
            ax.add_patch(Rectangle((x, yy), w, 9.0, fc=nen, ec=vien, lw=2.0, zorder=4))
            _txt(ax, x + w / 2, yy + 4.5, str(v), fs=FS['body'], c=chu, w='bold', z=6)
    ax.add_patch(Rectangle((6, H - tren - 25.0), 88, 7.0, fc='#DDE3EA', ec=LINE, lw=1.4, zorder=2))
    for k in range(9):
        ax.plot([10 + k * 10, 16 + k * 10], [H - tren - 21.5] * 2, color='white', lw=2.0, zorder=3)
    if p.get('note'):
        txt_fit(ax, 50, H - tren - 47.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def dong_ho(p, out):
    """Đồng hồ — kim ngắn chỉ GIỜ, kim dài chỉ PHÚT. Có vạch số để bé đọc được."""
    import math
    from matplotlib.patches import Circle
    ds = p.get('dongho') or []
    n = max(len(ds), 1)
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.6, (tren + 46.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - 20.0
    R = min(17.0, 84.0 / (n * 2.4))
    for i, d in enumerate(ds):
        cx = 6.0 + (88.0 / n) * (i + 0.5)
        ax.add_patch(Circle((cx, yc), R, fc='white', ec=NAVY, lw=2.8, zorder=4))
        for k in range(12):
            a = math.radians(90 - k * 30)
            _txt(ax, cx + R * 0.8 * math.cos(a), yc + R * 0.8 * math.sin(a),
                 str(12 if k == 0 else k), fs=FS['tiny'], c=NAVY, w='bold', z=6)
        gio, phut = d.get('gio', 12), d.get('phut', 0)
        ap = math.radians(90 - phut * 6)
        ag = math.radians(90 - (gio % 12) * 30 - phut * 0.5)
        ax.plot([cx, cx + R * 0.62 * math.cos(ag)], [yc, yc + R * 0.62 * math.sin(ag)],
                color=RED, lw=4.2, zorder=5, solid_capstyle='round')
        ax.plot([cx, cx + R * 0.86 * math.cos(ap)], [yc, yc + R * 0.86 * math.sin(ap)],
                color=TEAL, lw=3.0, zorder=5, solid_capstyle='round')
        ax.add_patch(Circle((cx, yc), R * 0.07, fc=NAVY, ec='none', zorder=6))
        for k, dg in enumerate(str(d.get('ten', '')).split('\n')):
            _txt(ax, cx, yc - R - 5.0 - k * 4.4, dg, fs=FS['small'], c=INK, w='bold', z=6)
    if p.get('note'):
        txt_fit(ax, 50, yc - R - 15.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def hang_cay(p, out):
    """Hàng cây — bé đếm CÂY và đếm KHOẢNG, thấy ngay khoảng ít hơn cây 1."""
    from matplotlib.patches import Circle, Rectangle
    n = int(p.get('so_cay', 5))
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + 40.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - 26.0
    xs = [10.0 + i * (80.0 / (n - 1)) for i in range(n)]
    ax.plot([6, 94], [y, y], color='#B0895F', lw=2.6, zorder=2)
    for i, x in enumerate(xs):
        ax.add_patch(Rectangle((x - 1.0, y), 2.0, 9.0, fc='#A9744F', ec='none', zorder=4))
        ax.add_patch(Circle((x, y + 13.0), 5.2, fc='#8CD98C', ec='#3E8E3E', lw=2.0, zorder=5))
        _txt(ax, x, y - 4.0, f'cây {i + 1}', fs=FS['tiny'], c=MUTE, w='normal', z=6)
    for i in range(n - 1):
        xm = (xs[i] + xs[i + 1]) / 2
        arrow(ax, (xs[i] + 1.6, y + 4.5), (xs[i + 1] - 1.6, y + 4.5), c=RED, lw=1.8,
              style='<|-|>', ms=9, z=6)
        _txt(ax, xm, y + 7.6, p.get('khoang', '2 m'), fs=FS['tiny'], c=RED, w='bold', z=7)
    if p.get('note'):
        txt_fit(ax, 50, y - 10.5, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def ban_tay(p, out):
    """Bàn tay: 5 ngón nhưng chỉ 4 kẽ — cùng một chuyện với hàng cây."""
    from matplotlib.patches import Rectangle
    tren = 11.0 if p.get('title') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + 38.0 + (8.0 if p.get('note') else 4.0)) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - 24.0
    card(ax, 26.0, y - 2.0, 48.0, 9.0, fc='#FBD9C0', ec='#D98F63', lw=2.2, r=1.4)
    cao = [12.0, 16.0, 18.0, 16.0, 12.0]
    xs = [30.0 + i * 10.0 for i in range(5)]
    for i, (x, c) in enumerate(zip(xs, cao)):
        ax.add_patch(Rectangle((x - 3.0, y + 6.0), 6.0, c, fc='#FBD9C0', ec='#D98F63', lw=2.2, zorder=4))
        _txt(ax, x, y + 6.0 + c + 3.0, str(i + 1), fs=FS['body'], c='#8C4A22', w='bold', z=6)
    for i in range(4):
        _txt(ax, (xs[i] + xs[i + 1]) / 2, y + 9.5, '↓', fs=FS['body'], c=RED, w='bold', z=7)
        _txt(ax, (xs[i] + xs[i + 1]) / 2, y + 4.5, str(i + 1), fs=FS['tiny'], c=RED, w='bold', z=7)
    _txt(ax, 50, y - 7.0, '5 ngón tay · 4 kẽ tay', fs=FS['mid'], c=NAVY, w='bold', z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 13.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def loi_thoai(p, out):
    """Lời nói của nhân vật — dùng cho chỗ Su Kem làm sai và cho bảng giá viết nhầm."""
    from matplotlib.patches import Circle
    tren = 11.0 if p.get('title') else 4.0
    dong = p.get('dong') or []
    CAO = 10.0 + 5.2 * len(dong)
    fig, ax, H = canvas(7.6, max(2.0, (tren + CAO + 12.0) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    y = H - tren - CAO
    sai = p.get('sai', True)
    vien, nen, chu = (RED, PALERED, RED) if sai else (TEAL, PALETEAL, DARKTEAL)
    ax.add_patch(Circle((14.0, y + CAO / 2), 8.0, fc='#FBD9C0', ec='#D98F63', lw=2.2, zorder=5))
    for dx in (-2.6, 2.6):
        ax.add_patch(Circle((14.0 + dx, y + CAO / 2 + 2.0), 0.9, fc=NAVY, ec='none', zorder=6))
    ax.plot([11.6, 14.0, 16.4],
            [y + CAO / 2 - (4.0 if sai else 2.4), y + CAO / 2 - (2.6 if sai else 4.0),
             y + CAO / 2 - (4.0 if sai else 2.4)], color=NAVY, lw=1.8, zorder=6,
            solid_capstyle='round')
    card(ax, 26.0, y, 68.0, CAO, fc=nen, ec=vien, lw=2.4, r=1.8)
    for k, d in enumerate(dong):
        txt_fit(ax, 60.0, y + CAO - 6.0 - k * 5.2, d, 62, FS['body'], chu, z=6)
    if p.get('ten'):
        _txt(ax, 14.0, y - 3.5, p['ten'], fs=FS['small'], c=NAVY, w='bold', z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 6.5, p['note'], 92, FS['body'], NAVY, z=5)
    save(fig, out)


# ── ba nguyên mẫu cho bài ĐẾM ────────────────────────────────────────────────
# Bài đếm hình có một đòi hỏi mà các nguyên mẫu cũ không đáp được: bé phải ĐẾM
# ĐƯỢC TRÊN HÌNH. Vẽ mỗi loại một cái rồi ghi số bên dưới thì đáp án nằm sẵn trên
# hình, bé chẳng đếm gì — mà nhìn lướt vẫn thấy "có hình, có số", nên lọt rất dễ.

def _manh_tamgiac(cx, yc, w, h, n):
    """Tam giác to bị n−1 vạch từ ĐỈNH xuống đáy cắt thành n mảnh."""
    dinh = (cx, yc + h / 2)
    day_y = yc - h / 2
    moc = [(cx - w / 2 + w * i / n, day_y) for i in range(n + 1)]
    return [[dinh, moc[i], moc[i + 1]] for i in range(n)], [dinh], moc


def _manh_luoi(cx, yc, w, h, nh, nc):
    """Hình chữ nhật / vuông chia thành lưới nh × nc. Mảnh đánh số từ TRÁI SANG,
    TRÊN XUỐNG — đúng thứ tự mắt bé đọc, để số trên hình khớp lời giải."""
    x0, y0 = cx - w / 2, yc - h / 2
    ra = []
    for i in range(nh):
        for j in range(nc):
            a, b = x0 + w * j / nc, y0 + h * (nh - 1 - i) / nh
            ra.append([(a, b), (a + w / nc, b), (a + w / nc, b + h / nh), (a, b + h / nh)])
    return ra


def _manh_cheo(cx, yc, w, h, n):
    """Hình vuông kẻ đường chéo: n=1 → 2 tam giác, n=2 → 4 tam giác.

    Bài B27 có hai câu bắt kẻ đường chéo mà lưới ô vuông không tả được — chéo cắt
    QUA ô chứ không dọc theo mép ô.
    """
    a, b = cx - w / 2, yc - h / 2
    c, d = cx + w / 2, yc + h / 2
    if n <= 1:
        return [[(a, b), (c, b), (c, d)], [(a, b), (c, d), (a, d)]]
    return [[(a, b), (c, b), (cx, yc)], [(c, b), (c, d), (cx, yc)],
            [(c, d), (a, d), (cx, yc)], [(a, d), (a, b), (cx, yc)]]


def _tam(poly):
    return (sum(x for x, _ in poly) / len(poly), sum(y for _, y in poly) / len(poly))


def _hop_manh(p, cx, yc, w, h, to):
    """Gộp các mảnh được tô thành MỘT đa giác, nếu chúng ghép ra hình liền khối.

    Không gộp thì bản "mảnh 1 + 2" vẫn còn vạch chia chạy giữa vùng tô — bé nhìn
    ra hai mảnh, chứ không nhìn ra MỘT tam giác to. Mà nhìn ra hình to mới đúng
    là điều bài đang dạy.
    """
    ds = sorted(to)
    if not ds or ds != list(range(ds[0], ds[-1] + 1)):
        return None                                   # rời rạc thì không gộp được
    if p.get('cheo'):
        # Mảnh chia theo ĐƯỜNG CHÉO không nằm trên lưới ô. Đi tiếp xuống nhánh lưới
        # bên dưới thì nó gộp ra một hình CHỮ NHẬT phủ lên nửa hình — bé nhìn thấy
        # cột màu chứ không thấy tam giác. Chéo thì tô từng mảnh, không gộp.
        return None
    if p.get('loai') == 'tamgiac':
        n = int(p.get('vach', 2))
        _, (dinh,), moc = _manh_tamgiac(cx, yc, w, h, n)
        return [dinh, moc[ds[0]], moc[ds[-1] + 1]]
    nh, nc = (p.get('luoi') or [1, int(p.get('vach', 2))])[:2]
    nh, nc = int(nh), int(nc)
    hang = {i // nc for i in ds}
    cot = {i % nc for i in ds}
    # chỉ gộp khi vùng tô là một khối chữ nhật ĐẶC, không thủng lỗ
    if len(ds) != len(hang) * len(cot):
        return None
    if sorted(hang) != list(range(min(hang), max(hang) + 1)):
        return None
    if sorted(cot) != list(range(min(cot), max(cot) + 1)):
        return None
    x0, y0 = cx - w / 2, yc - h / 2
    a = x0 + w * min(cot) / nc
    b = x0 + w * (max(cot) + 1) / nc
    t = y0 + h * (nh - 1 - max(hang)) / nh
    d = y0 + h * (nh - min(hang)) / nh
    return [(a, t), (b, t), (b, d), (a, d)]


def _ve_ghep(ax, p, cx, yc, w, h, to=(), so=True, lw=2.4):
    """Vẽ hình ghép một lần. `to` = chỉ số các mảnh cần tô đậm."""
    from matplotlib.patches import Polygon
    loai = p.get('loai', 'chunhat')
    if p.get('cheo'):
        manh = _manh_cheo(cx, yc, w, h, int(p['cheo']))
    elif loai == 'tamgiac':
        manh, _, _ = _manh_tamgiac(cx, yc, w, h, int(p.get('vach', 2)))
    else:
        nh, nc = (p.get('luoi') or [1, int(p.get('vach', 2))])[:2]
        manh = _manh_luoi(cx, yc, w, h, int(nh), int(nc))
    vien, nen, chu = MAU.get(p.get('mau', 'teal'), MAU['teal'])
    for i, m in enumerate(manh):
        ax.add_patch(Polygon(m, fc=nen, ec=vien, lw=lw, zorder=4))
        if so:
            mx, my = _tam(m)
            _txt(ax, mx, my, str(i + 1), fs=FS['body'], c=chu, w='bold', z=7)
    if to:
        gop = _hop_manh(p, cx, yc, w, h, to)
        for m in ([gop] if gop else [manh[i] for i in to]):
            ax.add_patch(Polygon(m, fc='#F08A72', ec=vien, lw=lw, zorder=6))
    return manh


def hinh_ghep(p, out):
    """
    ĐẾM HÌNH TRONG HÌNH GHÉP — một hình to bị vạch chia thành nhiều mảnh.

    params:
      title · loai: tamgiac|vuong|chunhat · vach: n  |  luoi: [hàng, cột]
      tim: [{ten, o: [chỉ số mảnh]}]   các hình tìm được, mỗi cái một bản nhỏ tô đậm
      note · mau

    VÌ SAO CẦN: bản cũ vẽ ba tam giác RỜI NHAU to bằng nhau cho câu "2 hình đơn +
    1 hình ghép = 3". Bé đếm trên hình ấy được 3 tam giác rời — không hề thấy tam
    giác to ÔM hai mảnh nhỏ, mà đó mới là điều cả bài đang dạy.
    """
    tim = p.get('tim') or []
    ti = 1.0 if p.get('loai') == 'vuong' else 1.15
    # Bản nhỏ xếp tối đa 5 cái một hàng, tràn thì xuống hàng. Nhồi cả 8 cái vào một
    # hàng thì mỗi cái chỉ còn 11 đơn vị bề ngang: hình vuông bị ép thành cột dọc,
    # nhãn chồng lên nhau, dòng chốt bị đè.
    MOI_HANG = 5
    n = min(len(tim), MOI_HANG) or 1
    so_hang = (len(tim) + MOI_HANG - 1) // MOI_HANG
    W = 88.0 / n
    tren = 11.0 if p.get('title') else 4.0
    CAO = 30.0
    # cạnh bản nhỏ lấy theo CẢ bề ngang lẫn bề cao — có thế mới giữ đúng tỉ lệ hình
    O = min(W * 0.72 / ti, 17.0) if tim else 0.0
    duoi = 8.0 if p.get('note') else 4.0
    cao_khung = tren + CAO + (so_hang * (O + 9.0) + 4.0 if tim else 6.0) + duoi
    fig, ax, H = canvas(7.6, max(3.0, cao_khung * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    yc = H - tren - CAO / 2 - 1.0
    _ve_ghep(ax, p, 50, yc, CAO * ti, CAO, so=True)

    # Hàng bản nhỏ: mỗi bản tô đậm ĐÚNG một hình tìm được. Đây là chỗ bé thấy hình
    # ghép hiện ra — không có nó thì "hình ghép" vẫn chỉ là chữ.
    ybot = yc - CAO / 2 - 8.0
    if tim:
        y = yc - CAO / 2 - 5.0 - O / 2
        for k, t in enumerate(tim):
            r_, c_ = divmod(k, MOI_HANG)
            trong = min(MOI_HANG, len(tim) - r_ * MOI_HANG)
            cx = 50 - (trong - 1) * W / 2 + c_ * W
            cy = y - r_ * (O + 9.0)
            _ve_ghep(ax, p, cx, cy, O * ti, O, to=set(t.get('o') or []), so=False, lw=1.8)
            _txt(ax, cx, cy - O / 2 - 4.0, t.get('ten', ''),
                 fs=FS['small'], c=INK, w='bold', z=7)
        ybot = y - (so_hang - 1) * (O + 9.0) - O / 2 - 9.5
    if p.get('note'):
        txt_fit(ax, 50, ybot, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def thap_khoi(p, out):
    """
    THÁP KHỐI THẬT — xếp từng khối lập phương theo tầng, khối hàng sau bị che một phần.

    params:
      title · tang: [{hang, cot, ten}]  (kể từ TẦNG DƯỚI lên) · note

    Bên phải vẽ lại từng tầng thành lưới phẳng — đúng cách bài dạy: "đếm theo
    tầng, đếm cả bạn nấp hàng sau". Bản cũ vẽ hai khối rời ghi sẵn "4 khối" và
    "1 khối": không có tháp, không có khối bị che, tức là mất cả bài học.
    """
    from matplotlib.patches import Polygon, Rectangle
    tang = p.get('tang') or []
    if not tang:
        raise ValueError('thap_khoi cần ít nhất một tầng')
    nh = max(int(t.get('hang', 1)) for t in tang)
    nc = max(int(t.get('cot', 1)) for t in tang)
    nt = len(tang)

    tren = 11.0 if p.get('title') else 4.0
    KHUNG_W, KHUNG_H = 46.0, 32.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.8, (tren + KHUNG_H + 14.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    # cạnh khối: vừa cả bề ngang lẫn bề cao của khung trái
    s = min(KHUNG_W / (nc + (nh - 1) * 0.45 + 0.45), KHUNG_H / (nt + (nh - 1) * 0.45 + 0.45))
    d = s * 0.45
    x0 = 5.0
    ytr = H - tren - KHUNG_H
    vien, nen, _ = MAU.get(p.get('mau', 'teal'), MAU['teal'])

    # HÀNG SAU VẼ TRƯỚC. Vẽ ngược lại thì khối trước bị khối sau đè lên, nhìn ra
    # một mớ đường kẻ chứ không ra cái tháp.
    o = []
    for L, t in enumerate(tang):
        for r in range(int(t.get('hang', 1))):
            for c in range(int(t.get('cot', 1))):
                o.append((r, L, c))
    for r, L, c in sorted(o, key=lambda k: (-k[0], k[1], k[2])):
        x = x0 + c * s + r * d
        y = ytr + L * s + r * d
        ax.add_patch(Rectangle((x, y), s, s, fc=nen, ec=vien, lw=1.9, zorder=10 - r))
        ax.add_patch(Polygon([(x, y + s), (x + d, y + s + d), (x + s + d, y + s + d),
                              (x + s, y + s)], fc='#FFF4DF', ec=vien, lw=1.9, zorder=10 - r))
        ax.add_patch(Polygon([(x + s, y), (x + s + d, y + d), (x + s + d, y + s + d),
                              (x + s, y + s)], fc='#E8F1FA', ec=vien, lw=1.9, zorder=10 - r))

    # Bên phải: từng tầng trải phẳng, mỗi ô là một khối — đếm được từng cái.
    # Đây CHÍNH LÀ lời giải, nên hình ĐỀ BÀI phải tắt đi (`chiTang: false`), không
    # thì bé chưa đếm đã thấy sẵn "2 × 2 = 4".
    if p.get('chiTang') is False:
        if p.get('note'):
            txt_fit(ax, 50, ytr - 7.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
        save(fig, out)
        return
    xr = 56.0
    o_s = min(6.0, (100.0 - xr - 4.0) / max(nc, 1) * 0.8)
    y = H - tren - 6.0
    for L in range(nt - 1, -1, -1):
        t = tang[L]
        hh, cc = int(t.get('hang', 1)), int(t.get('cot', 1))
        _txt(ax, xr, y, t.get('ten') or f'tầng {L + 1}', fs=FS['small'], c=NAVY,
             w='bold', ha='left', z=7)
        y -= 4.6
        for r in range(hh):
            for c in range(cc):
                ax.add_patch(Rectangle((xr + c * o_s, y - (r + 1) * o_s * 0.86),
                                       o_s * 0.9, o_s * 0.78, fc=nen, ec=vien, lw=1.5, zorder=6))
        _txt(ax, xr + cc * o_s + 2.0, y - hh * o_s * 0.86 / 2 - 1.0,
             f'{cc} × {hh} = {cc * hh}' if hh > 1 else f'{cc} khối',
             fs=FS['small'], c=INK, ha='left', z=7)
        y -= hh * o_s * 0.86 + 5.0

    if p.get('note'):
        txt_fit(ax, 50, ytr - 7.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def dong_hinh(p, out):
    """
    ĐỐNG HÌNH TRỘN LẪN — vẽ ĐỦ số hình mỗi loại, xếp xen kẽ để bé phải đếm thật.

    params: title · hinh: [{loai, mau, soLuong}] · note

    Xếp XEN KẼ chứ không gom theo loại: gom lại thì nhìn một cái là ra số, khỏi
    đếm. Thứ tự xen kẽ tính bằng chia lấy dư nên lần vẽ nào cũng y hệt — hình
    không được đổi mỗi lần chạy, đổi là mã kiểm đổi theo và máy bé tải lại.
    """
    from matplotlib.patches import Circle, Polygon, Rectangle
    hs = p.get('hinh') or []
    tui = []
    for i, h in enumerate(hs):
        tui += [h] * int(h.get('soLuong', 1))
    if not tui:
        raise ValueError('dong_hinh cần ít nhất một hình')
    # xen kẽ: rải vòng tròn theo loại
    xen, con = [], [[h] * int(h.get('soLuong', 1)) for h in hs]
    while any(con):
        for nhom in con:
            if nhom:
                xen.append(nhom.pop(0))
    n = len(xen)
    moi_hang = min(n, 5)
    so_hang = (n + moi_hang - 1) // moi_hang
    tren = 11.0 if p.get('title') else 4.0
    O = min(15.0, 84.0 / moi_hang)
    duoi = 9.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + O * so_hang + 10.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    for k, h in enumerate(xen):
        r_, c_ = divmod(k, moi_hang)
        trong_hang = min(moi_hang, n - r_ * moi_hang)
        cx = 50 - (trong_hang - 1) * O / 2 + c_ * O
        cy = H - tren - O / 2 - r_ * O
        rr = O * 0.34
        vien, nen, _ = MAU.get(h.get('mau', 'teal'), MAU['teal'])
        loai = h.get('loai', 'vuong')
        if loai == 'tron':
            ax.add_patch(Circle((cx, cy), rr, fc=nen, ec=vien, lw=2.2, zorder=4))
        elif loai == 'tamgiac':
            ax.add_patch(Polygon([(cx - rr, cy - rr * 0.8), (cx + rr, cy - rr * 0.8),
                                  (cx, cy + rr)], fc=nen, ec=vien, lw=2.2, zorder=4))
        else:
            w2 = rr if loai == 'vuong' else rr * 1.3
            ax.add_patch(Rectangle((cx - w2, cy - rr), w2 * 2, rr * 2,
                                   fc=nen, ec=vien, lw=2.2, zorder=4))
    if p.get('note'):
        txt_fit(ax, 50, H - tren - O * so_hang - 6.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def hinh_chu_vi(p, out):
    """
    HÌNH CÓ SỐ ĐO TRÊN TỪNG CẠNH — cho bài chu vi và bài đếm cạnh/đỉnh.

    params: title · hinh[{loai, canh[số], ten, mau, dinh}] · note
      loai: tamgiac | vuong | chunhat | tugiac
      canh: số đo ghi lên từng cạnh, theo thứ tự vẽ. Bỏ trống thì không ghi số.
      dinh: True → chấm đậm các đỉnh, cho bài "đếm cạnh, đếm đỉnh"

    `hinh_phang` ghi số đo thành một dòng chữ DƯỚI hình ("2 cm · 3 cm · 4 cm"), nên
    bé không biết số nào của cạnh nào — mà bài chu vi thì phải cộng đúng từng cạnh.
    """
    from matplotlib.patches import Circle, Polygon
    hs = p.get('hinh') or []
    n = max(len(hs), 1)
    W = 88.0 / n
    tren = 11.0 if p.get('title') else 4.0
    CAO = min(32.0, W * 0.92)
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.6, (tren + CAO + 16.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - CAO / 2 - 1.0

    for i, h in enumerate(hs):
        cx = 6.0 + W * (i + 0.5)
        vien, nen, chu = MAU.get(h.get('mau', 'teal'), MAU['teal'])
        r = min(W * 0.34, CAO * 0.40)
        loai = h.get('loai', 'vuong')
        if loai == 'tamgiac':
            pts = [(cx - r, yc - r * 0.75), (cx + r, yc - r * 0.75), (cx, yc + r * 0.85)]
        elif loai == 'chunhat':
            a, b = r * 1.25, r * 0.72
            pts = [(cx - a, yc - b), (cx + a, yc - b), (cx + a, yc + b), (cx - a, yc + b)]
        elif loai == 'tugiac':
            pts = [(cx - r, yc - r * 0.7), (cx + r * 0.95, yc - r), (cx + r * 0.7, yc + r * 0.9),
                   (cx - r * 0.85, yc + r * 0.5)]
        else:
            a = r * 0.9
            pts = [(cx - a, yc - a), (cx + a, yc - a), (cx + a, yc + a), (cx - a, yc + a)]
        ax.add_patch(Polygon(pts, fc=nen, ec=vien, lw=2.4, zorder=4))

        # số đo đặt ngoài cạnh, đẩy ra theo hướng từ TÂM ra giữa cạnh
        so = h.get('canh') or []
        for k in range(len(pts)):
            if k >= len(so) or so[k] in (None, ''):
                continue
            x1, y1 = pts[k]
            x2, y2 = pts[(k + 1) % len(pts)]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = mx - cx, my - yc
            d = max((dx * dx + dy * dy) ** 0.5, 0.001)
            _txt(ax, mx + dx / d * 3.6, my + dy / d * 3.6, str(so[k]),
                 fs=FS['small'], c=chu, w='bold', z=8)
        if h.get('dinh'):
            for x, y in pts:
                ax.add_patch(Circle((x, y), 0.9, fc=vien, ec=vien, zorder=9))
        if h.get('ten'):
            _txt(ax, cx, yc - CAO / 2 - 3.0, h['ten'], fs=FS['body'], c=chu, w='bold', z=7)
    if p.get('note'):
        txt_fit(ax, 50, yc - CAO / 2 - 10.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def dong_xu_cham(p, out):
    """
    MẤY ĐỒNG XU BẰNG NHAU ĐẶT CHẠM NHAU — tâm của chúng nối lại thành hình gì.

    params: title · so (mấy đồng, 3 hoặc 4) · noiTam (True → nối các tâm) · note

    Bài B28 C7 hỏi ba tâm tạo thành hình gì. Không vẽ thì bé phải tự tưởng tượng
    ba hình tròn chạm nhau — quá sức bé lớp 2.
    """
    import math
    from matplotlib.patches import Circle, Polygon
    n = int(p.get('so', 3))
    tren = 11.0 if p.get('title') else 4.0
    CAO = 34.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.6, (tren + CAO + 6.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - CAO / 2
    r = CAO * 0.26
    # tâm nằm trên một đường tròn sao cho hai đồng kề nhau CHẠM nhau: khoảng cách
    # hai tâm đúng bằng 2r, nên bán kính vòng đặt tâm = r / sin(pi/n)
    R = r / math.sin(math.pi / n)
    tam = [(50 + R * math.cos(math.pi / 2 + 2 * math.pi * k / n),
            yc + R * math.sin(math.pi / 2 + 2 * math.pi * k / n)) for k in range(n)]
    vien, nen, chu = MAU.get(p.get('mau', 'gold'), MAU['gold'])
    for x, y in tam:
        ax.add_patch(Circle((x, y), r, fc=nen, ec=vien, lw=2.4, zorder=4))
    if p.get('noiTam'):
        ax.add_patch(Polygon(tam, fc='none', ec='#7E57C2', lw=2.6, zorder=7))
    for x, y in tam:
        ax.add_patch(Circle((x, y), 1.0, fc='#7E57C2', ec='#7E57C2', zorder=8))
    if p.get('note'):
        txt_fit(ax, 50, yc - CAO / 2 - 3.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)
