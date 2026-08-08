# -*- coding: utf-8 -*-
"""Nguyên mẫu 1-4: phủ 74% mô tả hình trong 168 micro."""
from core import *
from core import _txt, txt_fit, fit_fs

# ═══ 1 · formula_card — thẻ / hộp công thức (26%) ═══
def formula_card(p, out):
    """params: title, formulas[{text, tone: navy|teal|gold}], note, mantra

    Thẻ CAO THEO CHỮ: đo trước xem mỗi ô cần mấy dòng rồi mới dựng khung,
    nhờ vậy câu dài được ngắt dòng đủ ý thay vì bị cắt cụt bằng dấu '…'.
    """
    fs = p['formulas']
    # đo trước: mỗi ô cần mấy dòng cho phần nhãn và phần chữ chính
    plan = []
    for f in fs:
        _, _, nb = wrap_fit(f['text'], 78, FS['big'], max_lines=4)
        nl = 0
        if f.get('label'):
            _, _, nl = wrap_fit(f['label'], 78, FS['small'], max_lines=2)
        plan.append((nl, nb, 7.5 + 4.6 * nb + 4.0 * nl))

    body_h = sum(h for _, _, h in plan) + 3 * len(fs)
    mantra_n = wrap_fit(p['mantra'], 78, FS['mid'], max_lines=3)[2] if p.get('mantra') else 0
    mantra_h = (6 + 4.4 * mantra_n) if mantra_n else 0
    total = 11 + body_h + (mantra_h + 3 if mantra_h else 0) + (5 if p.get('note') else 2)
    fig, ax, H = canvas(7.2, max(1.6, total * 7.2 / 100))

    y = H - 8
    if p.get('title'):
        txt_fit(ax, 50, y, p['title'], 90, FS['title'], NAVY, z=5); y -= 8
    tones = dict(navy=(NAVY, 'white'), teal=(TEAL, DARKTEAL), gold=(GOLD, DARKGOLD),
                 white=('white', NAVY))
    for f, (nl, nb, h) in zip(fs, plan):
        fc, tc = tones.get(f.get('tone', 'navy'), tones['navy'])
        card(ax, 6, y - h, 88, h, fc=fc, ec=LINE if fc == 'white' else 'none')
        if nl:
            txt_wrap(ax, 50, y - 2.2 - 2.0 * nl, f['label'], 78, FS['small'], tc, z=5, max_lines=2)
            txt_wrap(ax, 50, y - 4.0 * nl - 3.4 - 2.3 * nb, f['text'], 78, FS['big'], tc, z=5)
        else:
            txt_wrap(ax, 50, y - h / 2, f['text'], 78, FS['big'], tc, z=5)
        y -= h + 3
    if mantra_h:
        card(ax, 6, y - mantra_h, 88, mantra_h, fc=GOLD, ec='none')
        txt_wrap(ax, 50, y - mantra_h / 2, p['mantra'], 78, FS['mid'], DARKGOLD, z=5, max_lines=3)
        y -= mantra_h + 3
    if p.get('note'):
        caption(ax, p['note'], max(y - 1, 2.0))
    save(fig, out)


# ═══ 2 · character_speech — nhân vật + lời thoại (23%) ═══
CHARS = {   # (màu áo, biểu tượng, vai)
 'Su Kem':      (TEAL,  '◕‿◕', 'cô giáo nhỏ'),
 'Trí Long':    (NAVY2, '◔_◔', 'bạn hay nhầm'),
 'Cáo Đề':      (RED,   '◣_◢', 'kẻ gài bẫy'),
 'Su Bống':     (GOLD,  '^‿^', 'bạn nhỏ'),
 'sư phụ Trí Dũng': (NAVY, '⌐■_■', 'sư phụ'),
}
def _avatar(ax, x, y, name, r=7.5):
    col, face, _ = CHARS.get(name, (NAVY, '•‿•', ''))
    ax.add_patch(Circle((x, y), r, fc=col, ec='white', lw=2.5, zorder=4))
    _txt(ax, x, y + 0.6, face, FS['mid'], 'white', 'bold', z=5)
    _txt(ax, x, y - r - 3.4, name, FS['tiny'], MUTE, 'bold', z=5)

def character_speech(p, out):
    """params: lines[{who, say, tone: normal|wrong|right}], title

    Bong bóng thoại CAO THEO LỜI: đo trước mỗi lời cần mấy dòng rồi mới dựng khung.
    Trước đây khung cứng 17 đơn vị nên lời dài phải cắt cụt bằng '…' ngay trong dữ
    liệu — con đọc tình huống mở bài mà không biết chuyện gì xảy ra tiếp.
    """
    # bong bóng không có lời thì bỏ hẳn — trước đây vẫn vẽ ra một khung trắng trơn
    # cạnh mặt nhân vật, con nhìn tưởng hình lỗi hoặc chữ chưa tải xong
    ls = [L for L in p['lines'] if str(L.get('say') or '').strip()]
    if not ls:
        ls = p['lines'][:1]
    # đo trước: mỗi bong bóng cần mấy dòng, và cần cao bao nhiêu
    plan = []
    for L in ls:
        text, size, n = wrap_fit(L['say'], 68, FS['body'], max_lines=8)
        plan.append((text, size, max(13.0, 4.0 + 4.3 * n)))

    total = 5 + sum(h + 5 for _, _, h in plan) + (7 if p.get('title') else 0)
    fig, ax, H = canvas(7.2, max(1.6, total * 7.2 / 100))
    y = H - 4
    if p.get('title'):
        txt_fit(ax, 50, y, p['title'], 90, FS['title'], NAVY, z=5); y -= 7
    for i, (L, (text, size, h)) in enumerate(zip(ls, plan)):
        left = i % 2 == 0
        bx = 20 if left else 6
        tone = L.get('tone', 'normal')
        fc = {'normal': 'white', 'wrong': PALERED, 'right': PALETEAL}[tone]
        ec = {'normal': LINE, 'wrong': RED, 'right': TEAL}[tone]
        card(ax, bx, y - h, 74, h, fc=fc, ec=ec, lw=1.8)
        ax.text(bx + 37, y - h/2, text, ha='center', va='center', fontsize=size,
                color=INK, zorder=5, linespacing=1.35)
        _avatar(ax, 10 if left else 90, y - h/2 + 2, L['who'])
        y -= h + 5
    save(fig, out)

# ═══ 3 · two_way_compare — bảng so sánh 2 ngả đúng/sai (14%) ═══
def two_way_compare(p, out):
    """params: title, wrong{head, steps[], result}, right{head, steps[], result}, verdict"""
    W, R = p['wrong'], p['right']
    # đếm cả số DÒNG sau khi ngắt chữ, không chỉ số bước (chống tràn xuống ô kết quả)
    def _lines(side):
        return sum(len(wrap(s, 26).split('\n')) for s in side['steps'])
    rows = max(_lines(W), _lines(R))
    fig, ax, H = canvas(7.2, 2.2 + 0.55*rows + (0.6 if p.get('verdict') else 0))
    y = H - 5
    if p.get('title'):
        txt_fit(ax, 50, y, p['title'], 90, FS['title'], NAVY, z=5); y -= 7
    top = y
    neutral = p.get('neutral')
    LCOL, LPALE, LMARK = (NAVY, '#EAF2FB', '①') if neutral else (RED, PALERED, '✗')
    RCOL, RMARK = (TEAL, '②') if neutral else (TEAL, '✓')
    for side, (X, Wd, col, pale, mark, head) in {
        'wrong': (4, 45, LCOL, LPALE, LMARK, W), 'right': (51, 45, RCOL, PALETEAL, RMARK, R)}.items():
        h = 9 + 6.2*rows + 9
        card(ax, X, top - h, Wd, h, fc=pale, ec=col, lw=2.2)
        card(ax, X + 2, top - 8, Wd - 4, 6.5, fc=col, ec='none', r=1.4)
        txt_fit(ax, X + Wd/2, top - 4.7, f"{mark}  {head['head']}", Wd-7, FS['body'], 'white', z=5)
        yy = top - 13
        for s in head['steps']:
            ws = wrap(s, 26); nl = len(ws.split('\n'))
            txt_fit(ax, X + Wd/2, yy - (nl-1)*1.6, ws, Wd-7, FS['small'], INK, w='normal', z=5)
            yy -= 6.2 * nl
        card(ax, X + 4, top - h + 2.5, Wd - 8, 7, fc='white', ec=col, lw=1.4, r=1.4)
        txt_fit(ax, X + Wd/2, top - h + 6, head['result'], Wd-11, FS['mid'], col, z=5)
    if p.get('verdict'):
        vfs = fit_fs(p['verdict'], 76, FS['body'])
        chip(ax, 50, top - h - 5.5, p['verdict'], GOLD, DARKGOLD, vfs)
    save(fig, out)

# ═══ 4 · motion_track — chuyển động: mũi tên, hành trình (11%) ═══
def motion_track(p, out):
    """params: title, length_label, movers[{name, from(0-1), dir: '>'|'<', speed, color}],
               meet{at(0-1), label}, notes[]"""
    fig, ax, H = canvas(7.2, 3.2)
    y0 = H - 6
    if p.get('title'):
        _txt(ax, 50, y0, p['title'], FS['title'], NAVY, 'bold')
    X0, X1, LY = 10, 90, H/2 - 2
    ax.plot([X0, X1], [LY, LY], color=NAVY, lw=4, solid_capstyle='round', zorder=3)
    for x, lab in ((X0, p.get('from_label', 'A')), (X1, p.get('to_label', 'B'))):
        ax.plot([x, x], [LY - 3.5, LY + 3.5], color=NAVY, lw=3, zorder=3)
        _txt(ax, x, LY - 7, lab, FS['body'], NAVY, 'bold', z=5)
    if p.get('length_label'):
        chip(ax, 50, LY + 8.5, p['length_label'], GOLD, DARKGOLD, FS['small'])
    cols = [TEAL, RED, NAVY2, GOLD]
    for i, m in enumerate(p['movers']):
        c = m.get('color') or cols[i % 4]
        x = X0 + (X1 - X0) * m['from']
        dx = 11 if m.get('dir', '>') == '>' else -11
        yy = LY + (4.5 if i % 2 == 0 else -4.5)
        arrow(ax, (x, yy), (x + dx, yy), c=c, lw=3.2, ms=15)
        _txt(ax, x + dx/2, yy + (3.6 if i % 2 == 0 else -3.6),
             f"{m['name']}  {m.get('speed','')}", FS['small'], c, 'bold', z=6)
    if p.get('meet'):
        mx = X0 + (X1 - X0) * p['meet']['at']
        ax.plot([mx], [LY], marker='*', ms=20, color=GOLD, mec=DARKGOLD, mew=1.2, zorder=7)
        chip(ax, mx, LY - 11, p['meet']['label'], GOLD, DARKGOLD, FS['small'])
    if p.get('notes'):
        caption(ax, '  ·  '.join(p['notes']), 3)
    save(fig, out)
