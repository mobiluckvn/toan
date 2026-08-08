# -*- coding: utf-8 -*-
"""Nguyên mẫu 9-12: sơ đồ đoạn thẳng · cân · lưới ô · phân số."""
from core import *
from core import _txt, txt_fit, fit_fs, CHAR_W
from matplotlib.patches import Polygon, Circle

# ═══ 9 · bar_diagram — sơ đồ đoạn thẳng / băng (tổng-hiệu, tỉ số) ═══
def bar_diagram(p, out):
    """params: title, bars[{name, units(int), color, label}], brace{text}, note"""
    bs = p['bars']; n = len(bs)
    BH, GAP = 8.5, 5.0
    need = (11 if p.get('title') else 4) + n*(BH+GAP) + (11 if p.get('brace') else 0) \
           + (7 if p.get('note') else 3)
    fig, ax, H = canvas(7.2, need*7.2/100)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    maxu = max(b['units'] for b in bs)
    X0, W = 20, 62
    unit = W/maxu
    y = H - (11 if p.get('title') else 4)
    cols = [TEAL, NAVY2, GOLD, RED]
    for i, b in enumerate(bs):
        col = b.get('color') or cols[i % 4]
        for u in range(b['units']):
            card(ax, X0 + u*unit + 0.6, y-BH, unit-1.2, BH, fc=col, ec='none', r=1.1)
        _txt(ax, X0-2.5, y-BH/2, b['name'], FS['body'], INK, 'bold', ha='right', z=5)
        if b.get('label'):
            chip(ax, X0 + b['units']*unit + 8, y-BH/2, b['label'], GOLD, DARKGOLD, FS['small'])
        y -= BH + GAP
    if p.get('brace'):
        card(ax, 6, y-6, 88, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, y-1.8, p['brace']['text'], 84, FS['body'], NAVY, z=5)
    if p.get('note'):
        caption(ax, p['note'], 2.6)
    save(fig, out)

# ═══ 10 · balance_scale — cân / tỉ lệ ═══
def balance_scale(p, out):
    """params: title, left{text, weight}, right{text, weight}, verdict, note
       Bên NẶNG hạ xuống (đúng vật lý)."""
    L, R = p['left'], p['right']
    fig, ax, H = canvas(7.2, 3.9)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    cx = 50
    beam_y = H - 17           # cao độ trục
    ARM = 29
    d = 0 if L['weight'] == R['weight'] else (-4.5 if L['weight'] > R['weight'] else 4.5)
    yL, yR = beam_y + d, beam_y - d          # nặng hơn → thấp hơn
    # trụ + chân đế
    ax.plot([cx, cx], [beam_y, beam_y-13], color=NAVY, lw=4.5, zorder=3)
    ax.add_patch(Polygon([(cx-7, beam_y-13), (cx+7, beam_y-13), (cx, beam_y-5)],
                 fc=NAVY, ec='none', zorder=3))
    ax.plot([cx-11, cx+11], [beam_y-13.4, beam_y-13.4], color=NAVY, lw=4, solid_capstyle='round', zorder=3)
    # đòn cân
    ax.plot([cx-ARM, cx+ARM], [yL, yR], color=NAVY, lw=4.5, solid_capstyle='round', zorder=4)
    ax.add_patch(Circle((cx, beam_y), 2.2, fc=GOLD, ec=NAVY, lw=1.6, zorder=6))
    for X, y_end, D, col in ((cx-ARM, yL, L, TEAL), (cx+ARM, yR, R, GOLD)):
        ax.plot([X, X], [y_end, y_end-5], color=NAVY, lw=2, zorder=4)
        tc = DARKTEAL if col == TEAL else DARKGOLD
        card(ax, X-19, y_end-14, 38, 9, fc=col, ec='none', r=1.5)
        txt_fit(ax, X, y_end-9.5, D['text'], 35, FS['body'], tc, z=6)
    if p.get('verdict'):
        card(ax, 12, 7.5, 76, 8.5, fc=GOLD, ec='none', r=1.5)
        txt_fit(ax, 50, 11.7, p['verdict'], 72, FS['body'], DARKGOLD, z=6)
    if p.get('note'):
        caption(ax, p['note'], 2.6)
    save(fig, out)

# ═══ 11 · grid_count — lưới ô vuông / đếm ô ═══
def grid_count(p, out):
    """params: title, cols, rows, fill[[c,r],...], fill_color, note, memo"""
    C, R = p['cols'], p['rows']
    fig, ax, H = canvas(7.2, 4.0)
    if p.get('title'):
        txt_fit(ax, 50, H-4.5, p['title'], 92, FS['title'], NAVY, z=6)
    cell = min(52/C, (H-26)/R)
    X0, Y0 = 10, 12
    fills = {tuple(f) for f in p.get('fill', [])}
    fc_on = p.get('fill_color', TEAL)
    for r in range(R):
        for c in range(C):
            on = (c, r) in fills
            ax.add_patch(Rectangle((X0+c*cell, Y0+r*cell), cell, cell,
                         fc=fc_on if on else 'white', ec=NAVY if on else LINE,
                         lw=1.8 if on else 1.1, zorder=3))
    if p.get('show_dims', True):
        chip(ax, X0+C*cell/2, Y0-5.5, f'{C} ô ngang', GOLD, DARKGOLD, FS['small'])
        chip(ax, X0-7, Y0+R*cell/2, f'{R} ô dọc', TEAL, DARKTEAL, FS['small'])
    for lb in (p.get('row_labels') or []):
        _txt(ax, X0-3, Y0+(lb['row']+0.5)*cell, lb['text'], FS['tiny'], INK, 'bold', z=5, ha='right')
    if p.get('memo'):
        CX = X0+C*cell+10
        card(ax, CX, Y0+2, 96-CX-2, R*cell-4)
        for i, m in enumerate(p['memo'][:3]):
            txt_fit(ax, CX+(96-CX-2)/2, Y0+R*cell-8-i*8, m, 96-CX-8, FS['mid'],
                    [NAVY, TEAL, GOLD][i], z=4)
    if p.get('note'): caption(ax, p['note'], 2.6)
    save(fig, out)

# ═══ 12 · fraction_split — phân số / chia phần ═══
def fraction_split(p, out):
    """params: title, shapes[{parts, shaded, label, kind: bar|circle}], note"""
    sh = p['shapes']; n = len(sh)
    fig, ax, H = canvas(7.2, 3.8)
    if p.get('title'):
        txt_fit(ax, 50, H-4.5, p['title'], 92, FS['title'], NAVY, z=6)
    span = 96/n
    for i, s in enumerate(sh):
        cx = 2 + span*(i+0.5)
        cy = H/2 + 1
        if s.get('kind', 'bar') == 'circle':
            from matplotlib.patches import Wedge
            R = min(12.5, span/2 - 5)
            for k in range(s['parts']):
                a0, a1 = 90 - (k+1)*360/s['parts'], 90 - k*360/s['parts']
                ax.add_patch(Wedge((cx, cy), R, a0, a1, fc=TEAL if k < s['shaded'] else 'white',
                             ec=NAVY, lw=1.8, zorder=3))
        else:
            W = span - 10; hh = 11
            cw = W/s['parts']
            for k in range(s['parts']):
                ax.add_patch(Rectangle((cx-W/2+k*cw, cy-hh/2), cw, hh,
                             fc=TEAL if k < s['shaded'] else 'white', ec=NAVY, lw=1.8, zorder=3))
        chip(ax, cx, cy-16.5, s.get('label') or f"{s['shaded']}/{s['parts']}", GOLD, DARKGOLD, FS['body'])
    if p.get('note'): caption(ax, p['note'], 2.6)
    save(fig, out)

# ═══ 13 · place_value_chart — bảng hàng của chữ số (C1–C4) ═══
def place_value_chart(p, out):
    """params: title, headers[], rows[{label, cells[], color}], comma_after(int),
               shift{steps, dir:'>'|'<', label}, note"""
    hd = p['headers']; rows = p['rows']; n = len(hd)
    need = (11 if p.get('title') else 4) + 9 + len(rows)*11 + (9 if p.get('shift') else 0) \
           + (7 if p.get('note') else 3)
    fig, ax, H = canvas(7.6, need*7.6/100)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, W = 14, 78
    cw = W/n
    ca = p.get('comma_after')
    y = H - (11 if p.get('title') else 4)
    # tiêu đề cột
    for i, h in enumerate(hd):
        isdec = ca is not None and i > ca
        card(ax, X0+i*cw+0.5, y-8, cw-1, 8, fc=TEAL if isdec else NAVY, ec='none', r=1.1)
        txt_fit(ax, X0+i*cw+cw/2, y-4, h, cw-3, FS['tiny'],
                DARKTEAL if isdec else 'white', z=5)
    y -= 10
    # các dòng số
    for r in rows:
        col = r.get('color') or 'white'
        hi = set(r.get('highlight') or [])
        for i, c in enumerate(r['cells']):
            fcc = GOLD if i in hi else col
            card(ax, X0+i*cw+0.5, y-9, cw-1, 9, fc=fcc,
                 ec=DARKGOLD if i in hi else LINE, lw=2.0 if i in hi else 1.3, r=1.1)
            if c not in (None, ''):
                txt_fit(ax, X0+i*cw+cw/2, y-4.5, str(c), cw-3, FS['big'], NAVY, z=5)
        if r.get('label'):
            txt_fit(ax, X0-2, y-4.5, r['label'], 13, FS['small'], INK, z=5, ha='right')
        has_dec = any(str(x).strip() for x in r['cells'][ca+1:]) if ca is not None else False
        if ca is not None and has_dec:
            xx = X0+(ca+1)*cw
            ax.plot([xx, xx], [y-9, y], color=RED, lw=2.2, ls=(0, (4, 3)), zorder=6)
            ax.text(xx, y-4.5, ',', ha='center', va='center', fontsize=FS['big']+8,
                    color=RED, fontweight='bold', zorder=7,
                    bbox=dict(boxstyle='circle,pad=0.18', fc='white', ec=RED, lw=1.4))
        y -= 11
    if p.get('shift'):
        s = p['shift']
        d = 1 if s.get('dir', '>') == '>' else -1
        x1 = X0 + W*0.30; x2 = x1 + d*cw*s.get('steps', 1)*1.0
        arrow(ax, (x1, y-2), (x2, y-2), c=GOLD, lw=3.2, ms=16)
        chip(ax, (x1+x2)/2, y-7.5, s.get('label', ''), GOLD, DARKGOLD, FS['small'])
        y -= 9
    if p.get('note'):
        caption(ax, p['note'], 2.6)
    save(fig, out)

# ═══ 14 · fence_posts — hàng rào cọc & khoảng (dãy cách đều) ═══
def fence_posts(p, out):
    """params: title, first, last, step, show, labels, gap_at, highlight[], show_step,
       gap_note, formula, note"""
    fig, ax, H = canvas(7.6, 3.9)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    n = p.get('show', 6)
    X0, X1 = 12, 88
    y = H/2 + 3
    gap = (X1-X0)/(n-1)
    ax.plot([X0, X1], [y, y], color=LINE, lw=2.5, zorder=2)
    labels = p.get('labels') or ([str(p['first'] + i*p['step']) for i in range(n-1)] + [str(p['last'])])
    for i in range(n):
        x = X0 + i*gap
        last = (i == n-1)
        ax.plot([x, x], [y-4.5, y+4.5], color=NAVY, lw=3.4, solid_capstyle='round', zorder=4)
        hl = i in set(p.get('highlight') or [])
        ax.add_patch(Circle((x, y+4.5), 2.2 if hl else 1.5,
                     fc=GOLD if hl else 'white', ec=NAVY, lw=2.0 if hl else 1.2, zorder=5))
        lab = '…' if (p.get('gap_at') == i) else labels[i] if i < len(labels) else ''
        if i in set(p.get('highlight') or []):
            chip(ax, x, y-8.5, lab, GOLD, DARKGOLD, FS['tiny'])
        else:
            txt_fit(ax, x, y-8, lab, gap*0.95, FS['small'], NAVY, z=5)
    for i in range(n-1):
        x = X0 + i*gap
        if p.get('show_step', True):
            _txt(ax, x+gap/2, y+3, str(p['step']), FS['tiny'], TEAL, 'bold', z=5)
        ax.plot([x+1.6, x+gap-1.6], [y, y], color=TEAL, lw=2.2, zorder=3)
    if p.get('gap_note'):
        chip(ax, 50, y-13.5, p['gap_note'], TEAL, DARKTEAL, FS['small'])
    if p.get('formula'):
        card(ax, 8, 6.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 10.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'): caption(ax, p['note'], 2.4)
    save(fig, out)

# ═══ 15 · venn_two — hai vòng giao nhau (đếm "hoặc") ═══
def venn_two(p, out):
    """params: title, left{label,count}, right{label,count}, both{label,count}, result, note"""
    L, R, B = p['left'], p['right'], p['both']
    fig, ax, H = canvas(7.6, 4.3)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    cy, r = 32, 12
    xl, xr = 41, 59
    ax.add_patch(Circle((xl, cy), r, fc=TEAL, ec='none', alpha=.55, zorder=2))
    ax.add_patch(Circle((xr, cy), r, fc=GOLD, ec='none', alpha=.6, zorder=2))
    ax.add_patch(Circle((xl, cy), r, fc='none', ec=NAVY, lw=2.2, zorder=4))
    ax.add_patch(Circle((xr, cy), r, fc='none', ec=NAVY, lw=2.2, zorder=4))
    _txt(ax, xl-5, cy, str(L['count']), FS['big'], NAVY, 'bold', z=5)
    _txt(ax, xr+5, cy, str(R['count']), FS['big'], NAVY, 'bold', z=5)
    _txt(ax, 50, cy, str(B['count']), FS['big'], RED, 'bold', z=5)
    txt_fit(ax, xl-6, cy+r+4, L['label'], 32, FS['small'], DARKTEAL, z=5)
    txt_fit(ax, xr+6, cy+r+4, R['label'], 32, FS['small'], DARKGOLD, z=5)
    ax.plot([50, 50], [cy-r+1, cy-r-3.5], color=RED, lw=1.6, zorder=5)
    chip(ax, 50, cy-r-6.5, B['label'], PALERED, RED, FS['tiny'])
    if p.get('result'):
        card(ax, 8, 5.5, 84, 8.5, fc=NAVY, ec='none', r=1.4)
        txt_fit(ax, 50, 9.7, p['result'], 80, FS['body'], 'white', z=5)
    if p.get('note'):
        caption(ax, p['note'], 2.0)
    save(fig, out)


# ═══ 16 · cycle_ring — vòng quay chu kỳ (tận cùng, dãy lặp) ═══
def cycle_ring(p, out):
    """params: title, items[str], start_note, pointer(int|None), pointer_label, note"""
    import numpy as np
    it = p['items']; n = len(it)
    fig, ax, H = canvas(7.6, 3.9)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    cx, cy, R = 33, H/2 - 2, 13
    pts = []
    for i in range(n):
        a = np.pi/2 - i*2*np.pi/n
        x, y = cx + np.cos(a)*R, cy + np.sin(a)*R
        pts.append((x, y))
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i+1) % n]
        arrow(ax, (x1 + (x2-x1)*0.28, y1 + (y2-y1)*0.28),
                  (x1 + (x2-x1)*0.72, y1 + (y2-y1)*0.72), c=MUTE, lw=2, ms=13, rad=-0.25)
    for i, (x, y) in enumerate(pts):
        on = (p.get('pointer') == i+1)
        col = GOLD if on else (NAVY if i % 2 == 0 else NAVY2)
        tc = DARKGOLD if on else 'white'
        ax.add_patch(Circle((x, y), 5.4, fc=col, ec=NAVY if on else 'none', lw=2.4, zorder=5))
        _txt(ax, x, y, str(it[i]), FS['mid'], tc, 'bold', z=6)
        _txt(ax, cx + (x-cx)*1.42, cy + (y-cy)*1.42, f'#{i+1}', FS['tiny'], MUTE, 'bold', z=6)
    _txt(ax, cx, cy, f'chu kỳ {n}', FS['small'], NAVY, 'bold', z=6)
    if p.get('rule'):
        card(ax, 55, cy-13, 41, 26)
        lines = p['rule'] if isinstance(p['rule'], list) else [p['rule']]
        for i, l in enumerate(lines[:3]):
            txt_fit(ax, 75.5, cy+7-i*8, l, 37, FS['body'], [NAVY, TEAL, DARKGOLD][i], z=4)
    if p.get('note'): caption(ax, p['note'], 2.4)
    save(fig, out)

# ═══ 17 · pair_sum — ghép cặp Gauss (tổng dãy cách đều) ═══
def pair_sum(p, out):
    """params: title, seq[str] (dùng '…' ở giữa), pair_sum_label, formula, note"""
    seq = p['seq']; n = len(seq)
    fig, ax, H = canvas(7.6, 4.2)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, X1 = 9, 91
    y = H/2 + 4
    gap = (X1-X0)/(n-1)
    xs = [X0 + i*gap for i in range(n)]
    for i, s in enumerate(seq):
        if s == '…':
            _txt(ax, xs[i], y, '…', FS['big'], MUTE, 'bold', z=5)
        else:
            card(ax, xs[i]-4.6, y-4.2, 9.2, 8.4, fc=NAVY, ec='none', r=1.3)
            txt_fit(ax, xs[i], y, s, 8, FS['body'], 'white', z=5)
    k = n // 2
    for j in range(min(k, 3)):
        a, b = xs[j], xs[n-1-j]
        rad = 0.20 + j*0.09
        ax.add_patch(FancyArrowPatch((a, y+4.6), (b, y+4.6), arrowstyle='<|-|>',
                     mutation_scale=12, color=GOLD, lw=2.2,
                     connectionstyle=f'arc3,rad=-{rad}', zorder=4))
    if p.get('pair_label'):
        chip(ax, 50, y-11, p['pair_label'], GOLD, DARKGOLD, FS['small'])
    if p.get('formula'):
        card(ax, 8, 5.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 9.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'): caption(ax, p['note'], 2.2)
    save(fig, out)

# ═══ 18 · area_split — mô hình diện tích cho luật phân phối a×(b+c) ═══
def area_split(p, out):
    """params: title, height{label,val}, parts[{label,val,color}], formula, note"""
    hgt = p['height']; parts = p['parts']
    fig, ax, H = canvas(7.6, 4.3)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, W = 20, 68
    y0, hh = 25, 19
    def _vn(v):
        s = f'{v:g}'.replace('.', ',')
        return s
    tot = sum(abs(x['val']) for x in parts)
    x = X0
    cols = [TEAL, GOLD, NAVY2]
    for i, pt in enumerate(parts):
        w = W*abs(pt['val'])/tot
        col = pt.get('color') or cols[i % 3]
        tc = DARKTEAL if col == TEAL else (DARKGOLD if col == GOLD else 'white')
        ax.add_patch(Rectangle((x, y0), w, hh, fc=col, ec=NAVY, lw=2, zorder=3))
        txt_fit(ax, x+w/2, y0+hh/2, pt['label'], w-3, FS['mid'], tc, z=5)
        x += w
    chip(ax, X0+W/2, y0-5.5,
         ' + '.join(_vn(x['val']) for x in parts) + '  =  ' + _vn(round(sum(x['val'] for x in parts), 6)),
         GOLD, DARKGOLD, FS['small'])
    ax.add_patch(FancyArrowPatch((X0-5, y0), (X0-5, y0+hh), arrowstyle='<|-|>', mutation_scale=14,
                 color=TEAL, lw=2.6, zorder=4))
    chip(ax, X0-12, y0+hh/2, hgt['label'], TEAL, DARKTEAL, FS['small'])
    if p.get('formula'):
        card(ax, 8, 5.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 9.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'): caption(ax, p['note'], 2.2)
    save(fig, out)

# ═══ 19 · chain_cancel — dây chuyền triệt tiêu (domino · rút chéo) ═══
def chain_cancel(p, out):
    """params: title, terms[str], cancel[idx bị gạch], survive[idx sống sót], result, note"""
    ts = p['terms']; n = len(ts)
    fig, ax, H = canvas(7.6, 4.0)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, X1 = 6, 94
    y = H/2 + 3
    cw = (X1-X0)/n
    can = set(p.get('cancel') or []); sur = set(p.get('survive') or [])
    for i, t in enumerate(ts):
        x = X0 + i*cw
        if i in sur:
            card(ax, x+0.6, y-6, cw-1.2, 12, fc=TEAL, ec=DARKTEAL, lw=2, r=1.2)
            tc = DARKTEAL
        else:
            card(ax, x+0.6, y-6, cw-1.2, 12, fc='white', ec=LINE, lw=1.3, r=1.2)
            tc = MUTE if i in can else NAVY
        txt_fit(ax, x+cw/2, y, t, cw-3, FS['mid'], tc, z=5)
        if i in can:
            ax.plot([x+2, x+cw-2], [y+3.4, y-3.4], color=RED, lw=2.4, zorder=6)
    chip(ax, 50, y-10.5, p.get('cancel_note', 'các phần giữa gặp nhau và triệt tiêu'),
         PALERED, RED, FS['small'])
    if p.get('result'):
        card(ax, 10, 5, 80, 8.5, fc=NAVY, ec='none', r=1.4)
        txt_fit(ax, 50, 9.2, p['result'], 76, FS['body'], 'white', z=5)
    if p.get('note'): caption(ax, p['note'], 1.9)
    save(fig, out)

# ═══ 20 · level_bars — cột số liệu + đường ĐIỂM CÂN, hiện phần thừa/thiếu ═══
def level_bars(p, out):
    """params: title, values[num], labels[str], mean(num), mean_label, show_dev(bool),
               unit, note, verdict"""
    vs = p['values']; n = len(vs)
    mean = p.get('mean') if p.get('mean') is not None else sum(vs)/n
    fig, ax, H = canvas(7.6, 4.2)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, W = 12, 76
    base, top = 21, H - 14
    lo = min(min(vs), mean); hi = max(max(vs), mean)
    span = max(hi - lo, 1)
    pad = span * 0.35
    def Y(v):  # quy đổi giá trị → toạ độ
        return base + (v - (lo - pad)) / (span + 2*pad) * (top - base)
    bw = W / n * 0.6
    for i, v in enumerate(vs):
        x = X0 + (i + 0.5) * W/n
        y = Y(v)
        over = v > mean
        ax.add_patch(Rectangle((x - bw/2, base), bw, y - base,
                     fc=TEAL if over else NAVY2, ec='none', zorder=3))
        ax.text(x, y + 2.8, str(v), ha='center', va='center', fontsize=FS['small'],
                color=NAVY, fontweight='bold', zorder=7,
                bbox=dict(boxstyle='round,pad=0.22', fc=BG, ec='none'))
        if p.get('labels') and i < len(p['labels']):
            _txt(ax, x, base - 4.5, p['labels'][i], FS['tiny'], MUTE, 'bold', z=5)
        if p.get('show_dev', True) and abs(v - mean) > 1e-9:
            d = v - mean
            ax.add_patch(Rectangle((x - bw/2, Y(mean)), bw, y - Y(mean),
                         fc='none', ec=GOLD, lw=2, ls=(0, (3, 2)), zorder=4))
            _txt(ax, x + bw*0.75, (y + Y(mean))/2,
                 ('+' if d > 0 else '−') + f'{abs(d):g}'.replace('.', ','),
                 FS['tiny'], DARKGOLD if d > 0 else RED, 'bold', z=6)
    ym = Y(mean)
    ax.plot([X0 - 2, X0 + W + 2], [ym, ym], color=RED, lw=2.6, zorder=6)
    chip(ax, X0 + W + 6, ym, p.get('mean_label', f'TBC {mean:g}'.replace('.', ',')),
         RED, 'white', FS['tiny'])
    ax.plot([X0 - 2, X0 + W + 2], [base, base], color=NAVY, lw=2, zorder=3)
    if p.get('verdict'):
        card(ax, 8, 4.5, 84, 8, fc=NAVY, ec='none', r=1.4)
        txt_fit(ax, 50, 8.4, p['verdict'], 80, FS['body'], 'white', z=5)
    if p.get('note'): caption(ax, p['note'], 1.6)
    save(fig, out)

# ═══ 21 · sum_diff_bars — sơ đồ đoạn thẳng TỔNG – HIỆU ═══
def sum_diff_bars(p, out):
    """params: title, small{label,val}, big{label,val}, diff_label, total_label,
               formula, note  — vẽ theo TỈ LỆ THẬT, đoạn dôi ra là HIỆU"""
    S, B = p['small'], p['big']
    fig, ax, H = canvas(7.6, 3.9)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, W = 8, 60
    sc = W / max(B['val'], 1e-9)
    ws, wb = S['val']*sc, B['val']*sc
    yb, ys, bh = H-21, H-32, 8.5
    # đoạn LỚN: phần bằng bé (navy) + phần hiệu (đỏ)
    def _fits(text, avail):
        """Có vừa không NGAY CẢ Ở CỠ CHỮ SÀN?"""
        longest = max((len(l) for l in str(text).split('\n')), default=0)
        return longest * CHAR_W * FS['tiny'] <= avail - 2.5
    def _label(x_center, y_center, text, avail, tc_in, fc_out, tc_out, x_chip, y_chip):
        if _fits(text, avail):
            txt_fit(ax, x_center, y_center, text, avail - 2, FS['body'], tc_in, z=5)
        else:
            chip(ax, x_chip, y_chip, text, fc_out, tc_out, FS['tiny'])
    card(ax, X0, yb, ws, bh, fc=NAVY, ec='none', r=1.2)
    card(ax, X0+ws, yb, wb-ws, bh, fc=RED, ec='none', r=1.2)
    _label(X0+ws/2, yb+bh/2, B['label'], ws, 'white', NAVY, 'white', X0+wb/2, yb+bh+4.2)
    _label(X0+ws+(wb-ws)/2, yb+bh/2, p.get('diff_label', 'hiệu'), wb-ws,
           'white', RED, 'white', X0+wb+18, yb+bh/2)
    # đoạn BÉ
    card(ax, X0, ys, ws, bh, fc=TEAL, ec='none', r=1.2)
    _label(X0+ws/2, ys+bh/2, S['label'], ws, DARKTEAL, TEAL, DARKTEAL, X0+ws/2, ys-4.2)
    # ngoặc TỔNG: ôm dọc CẢ HAI đoạn (tổng = bé + lớn), đặt bên phải
    xbr = X0 + wb + 4
    ax.plot([xbr-2, xbr, xbr, xbr-2], [yb+bh, yb+bh, ys, ys], color=GOLD, lw=2.6, zorder=4)
    chip(ax, xbr + 7, (yb+bh+ys)/2, p.get('total_label', 'tổng'), GOLD, DARKGOLD, FS['small'])
    if p.get('formula'):
        card(ax, 8, 5.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 9.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'): caption(ax, p['note'], 2.2)
    save(fig, out)

# ═══ 22 · before_after_parts — hai sơ đồ TRƯỚC / SAU theo khúc, hiện phần NHÍCH ═══
def before_after_parts(p, out):
    """params: title, before{tag,a,b,a_label,b_label}, after{tag,a,b,a_label,b_label},
               delta{label}, formula, note  (a, b = số khúc)"""
    BF, AF = p['before'], p['after']
    mx = max(BF['a'] + BF['b'], AF['a'] + AF['b'], 1)
    BH, G_IN, G_MID = 7.5, 2.6, 8.0
    block = BH*2 + G_IN                      # một nhóm 2 thanh
    need = 12 + block + G_MID + block + 7 + 11 + 6
    fig, ax, H = canvas(7.6, need*7.6/100)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, W = 20, 62
    cw = W / mx
    ytop = H - 12
    y = ytop
    rows = []                                # lưu (y_dưới, y_trên) của thanh A từng nhóm
    for gi, grp in enumerate((BF, AF)):
        _txt(ax, X0-3, y-BH/2, grp.get('tag', ''), FS['small'], NAVY, 'bold', ha='right', z=5)
        for i2 in range(grp['a']):
            card(ax, X0+i2*cw+0.5, y-BH, cw-1, BH, fc=TEAL, ec='none', r=1.1)
        if grp.get('a_label'):
            chip(ax, X0+max(grp['a'], grp['b'])*cw+11, y-BH/2, grp['a_label'], TEAL, DARKTEAL, FS['tiny'])
        rows.append((y-BH, y))
        y -= BH + G_IN
        for i2 in range(grp['b']):
            card(ax, X0+i2*cw+0.5, y-BH, cw-1, BH, fc=NAVY, ec='none', r=1.1)
        if grp.get('b_label'):
            chip(ax, X0+max(grp['a'], grp['b'])*cw+11, y-BH/2, grp['b_label'], NAVY, 'white', FS['tiny'])
        y -= BH + (G_MID if gi == 0 else 0)
    # khung đánh dấu khúc NHÍCH của A (từ thanh A nhóm trên xuống thanh A nhóm dưới)
    if AF['a'] != BF['a']:
        lo, hi = sorted((BF['a'], AF['a']))
        x1, x2 = X0 + lo*cw, X0 + hi*cw
        ytopr, ybotr = rows[0][1], rows[1][0]
        ax.add_patch(Rectangle((x1, ybotr), x2-x1, ytopr-ybotr, fc='none', ec=GOLD, lw=2.4,
                     ls=(0, (4, 2)), zorder=6))
        if p.get('delta'):
            # đặt vào KHOẢNG TRỐNG giữa hai nhóm, không đè thanh nào
            chip(ax, (x1+x2)/2, rows[1][1] + 4.4, p['delta']['label'], GOLD, DARKGOLD, FS['tiny'])
    if p.get('formula'):
        card(ax, 8, 5.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 9.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'):
        caption(ax, p['note'], 2.2)
    save(fig, out)

# ═══ 23 · stack_compare — hai cột chồng (nước / chất khô) vẽ đúng tỉ lệ, tô neo bất biến ═══
def stack_compare(p, out):
    """params: title, cols[{tag,total,total_label,parts[{label,val,color}]}],
               anchor_label, formula, note  — color: 'anchor' | 'water' | khác"""
    cs = p['cols']
    mx = max(c['total'] for c in cs)
    fig, ax, H = canvas(7.6, 5.2)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    base, top = 36, H - 16
    hmax = top - base
    n = len(cs)
    bw = 17
    xs = [24 + i*(52/max(n-1, 1)) - bw/2 for i in range(n)] if n > 1 else [50 - bw/2]
    for i, c in enumerate(cs):
        x = xs[i]; y = base
        legend = []
        for pt in c['parts']:
            h = hmax * pt['val'] / mx
            anc = pt.get('color') == 'anchor'
            fc = GOLD if anc else (TEAL if pt.get('color') == 'water' else NAVY2)
            tc = DARKGOLD if anc else 'white'
            ax.add_patch(Rectangle((x, y), bw, h, fc=fc,
                         ec=DARKGOLD if anc else 'none', lw=2.2 if anc else 0, zorder=3))
            if h >= 6 and len(str(pt['label']))*CHAR_W*FS['tiny'] <= bw-2:
                txt_fit(ax, x+bw/2, y+h/2, pt['label'], bw-2, FS['tiny'], tc, z=5)
            else:
                legend.append((pt['label'], fc))       # đoạn mỏng → xuống chú thích
            y += h
        _txt(ax, x+bw/2, base-5, c['tag'], FS['small'], NAVY, 'bold', z=5)
        for k, (lb, col) in enumerate(legend):
            ax.plot([x+bw/2-11.5], [base-9.8-k*4.6], marker='s', ms=5, color=col, zorder=5)
            txt_fit(ax, x+bw/2+1.5, base-9.8-k*4.6, lb, 22, FS['tiny'], INK, w='normal', z=5)
        if c.get('total_label'):
            chip(ax, x+bw/2, y+4.2, c['total_label'], NAVY, 'white', FS['tiny'])
        if i < n-1:
            arrow(ax, (x+bw+2, top+2), (xs[i+1]-2, top+2), c=MUTE, lw=2.2, ms=14)
    if p.get('anchor_label'):
        chip(ax, 50, 19, p['anchor_label'], GOLD, DARKGOLD, FS['small'])
    if p.get('formula'):
        card(ax, 8, 5.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 9.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'):
        caption(ax, p['note'], 1.8)
    save(fig, out)

def _fits_seg(text, w):
    return len(str(text)) * CHAR_W * FS['tiny'] <= w - 2

# ═══ 24 · venn_three — ba vòng giao nhau (trừ giao đôi, cộng trả giao ba) ═══
def venn_three(p, out):
    """params: title, sets[{label,count}×3], pairs{ab,ac,bc}, triple, outside{label,count},
               result, note"""
    S = p['sets']; PR = p['pairs']
    fig, ax, H = canvas(7.6, 5.8)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    cx, cy, r = 50, 34, 15
    import math
    cs = [(cx, cy + 8.5), (cx - 9.5, cy - 5.5), (cx + 9.5, cy - 5.5)]
    cols = [TEAL, GOLD, NAVY2]
    for (x, y), col in zip(cs, cols):
        ax.add_patch(Circle((x, y), r, fc=col, ec='none', alpha=.42, zorder=2))
    for (x, y) in cs:
        ax.add_patch(Circle((x, y), r, fc='none', ec=NAVY, lw=2, zorder=5))
    # số chỉ-riêng của từng vòng
    only = [S[0]['count'] - PR['ab'] - PR['ac'] + p['triple'],
            S[1]['count'] - PR['ab'] - PR['bc'] + p['triple'],
            S[2]['count'] - PR['ac'] - PR['bc'] + p['triple']]
    pos_only = [(cx, cy + 18), (cx - 18, cy - 12), (cx + 18, cy - 12)]
    for (x, y), v in zip(pos_only, only):
        _txt(ax, x, y, str(v), FS['mid'], NAVY, 'bold', z=6)
    # giao đôi
    _txt(ax, cx - 10.5, cy + 6.5, str(PR['ab'] - p['triple']), FS['small'], RED, 'bold', z=6)
    _txt(ax, cx + 10.5, cy + 6.5, str(PR['ac'] - p['triple']), FS['small'], RED, 'bold', z=6)
    _txt(ax, cx, cy - 10.5, str(PR['bc'] - p['triple']), FS['small'], RED, 'bold', z=6)
    _txt(ax, cx, cy + 0.5, str(p['triple']), FS['mid'], DARKGOLD, 'bold', z=7)
    # chú giải hàng ngang dưới tiêu đề — không đè hình
    lx = 16
    for s, col in zip(S, cols):
        ax.plot([lx], [64], marker='s', ms=7, color=col, zorder=6)
        txt_fit(ax, lx + 12, 64, f"{s['label']} ({s['count']})", 20, FS['small'], NAVY, z=6)
        lx += 25
    if p.get('outside'):
        chip(ax, 50, 56.5, f"{p['outside']['label']}: {p['outside']['count']}", '#EAF2FB', NAVY, FS['tiny'])
    if p.get('result'):
        card(ax, 8, 4.2, 84, 8.5, fc=NAVY, ec='none', r=1.4)
        txt_fit(ax, 50, 8.4, p['result'], 80, FS['body'], 'white', z=5)
    if p.get('note'): caption(ax, p['note'], 1.2)
    save(fig, out)

# ═══ 25 · geo_shape — hình đa giác tổng quát: vùng tô · điểm · đường phụ · nhãn cạnh ═══
_GEO_FC = dict(teal=(TEAL, DARKTEAL), gold=(GOLD, DARKGOLD), navy=(NAVY, 'white'),
               pale=(SOFT, NAVY), red=(PALERED, RED), none=('none', NAVY), white=('white', NAVY))

def geo_shape(p, out):
    """params: title, points{P:[x,y]}, shapes[{pts[],fill,label,alpha}],
               segments[{from,to,dashed,color,label}], labels[{at,text,dx,dy}],
               edge_labels[{from,to,text,offset}], right_angles[{at,a,b}], formula, note"""
    P = {k: (float(v[0]), float(v[1])) for k, v in p['points'].items()}
    xs = [v[0] for v in P.values()]; ys = [v[1] for v in P.values()]
    # tính cả bán kính hình tròn vào khung bao — nếu không, vòng tròn sẽ tràn mép
    for _sh in p.get('shapes', []):
        _c = _sh.get('circle')
        if _c:
            _x, _y = P[_c['at']]; _r = float(_c['r'])
            xs += [_x - _r, _x + _r]; ys += [_y - _r, _y + _r]
    fig, ax, H = canvas(7.6, 4.6)
    if p.get('title'):
        txt_fit(ax, 50, H-4.8, p['title'], 92, FS['title'], NAVY, z=6)
    X0, X1 = 16, 84
    Y0, Y1 = (23 if p.get('formula') else 10), H - 14
    sx = (X1-X0)/max(max(xs)-min(xs), 1e-9); sy = (Y1-Y0)/max(max(ys)-min(ys), 1e-9)
    s = min(sx, sy)
    ox = (X0+X1)/2 - s*(max(xs)+min(xs))/2
    oy = (Y0+Y1)/2 - s*(max(ys)+min(ys))/2
    T = lambda k: (ox + s*P[k][0], oy + s*P[k][1])
    from matplotlib.patches import Wedge as _Wedge
    for sh in p.get('shapes', []):
        fc, tc = _GEO_FC.get(sh.get('fill', 'pale'), _GEO_FC['pale'])
        if sh.get('circle'):                      # hình tròn / cung tròn
            cc = sh['circle']; ctr = T(cc['at']); rr = s*cc['r']
            if cc.get('a0') is not None:
                ax.add_patch(_Wedge(ctr, rr, cc['a0'], cc['a1'], fc=fc, ec=NAVY, lw=2.2, zorder=3))
            else:
                ax.add_patch(Circle(ctr, rr, fc=fc, ec=NAVY, lw=2.4, zorder=sh.get('z', 3)))
            if sh.get('label'):
                ax.text(ctr[0] + cc.get('dx', 0), ctr[1] + cc.get('dy', 0), sh['label'],
                        ha='center', va='center', fontsize=FS['small'], fontweight='bold',
                        color=tc, zorder=7,
                        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=.8))
            continue
        poly = [T(k) for k in sh['pts']]
        ax.add_patch(Polygon(poly, fc=fc, ec=NAVY, lw=2.2, zorder=3,
                     alpha=sh.get('alpha', 1.0) if fc != 'none' else 1.0))
        if sh.get('label'):
            cxp = sum(q[0] for q in poly)/len(poly); cyp = sum(q[1] for q in poly)/len(poly)
            ax.text(cxp, cyp, sh['label'], ha='center', va='center', fontsize=FS['small'],
                    fontweight='bold', color=tc if fc != 'none' else NAVY, zorder=6,
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=.75))
    for sg in p.get('segments', []):
        a, b = T(sg['from']), T(sg['to'])
        ax.plot([a[0], b[0]], [a[1], b[1]], color=sg.get('color') or NAVY,
                lw=2.6, ls=(0, (5, 3)) if sg.get('dashed') else '-', zorder=5)
        if sg.get('label'):
            chip(ax, (a[0]+b[0])/2 + sg.get('dx', 0), (a[1]+b[1])/2 + sg.get('dy', 0),
                 sg['label'], 'white', NAVY, FS['tiny'])
    for k in p.get('show_points', list(P.keys())):
        x, y = T(k)
        ax.plot([x], [y], marker='o', ms=6, color=NAVY, zorder=7)
        d = next((l for l in p.get('labels', []) if l['at'] == k), {})
        _txt(ax, x + d.get('dx', 0) or (3.2 if x >= 50 else -3.2),
             y + (d.get('dy', 0) or (3.2 if y >= (Y0+Y1)/2 else -3.2)),
             d.get('text', k), FS['small'], NAVY, 'bold', z=7)
    for el in p.get('edge_labels', []):
        a, b = T(el['from']), T(el['to'])
        mx_, my_ = (a[0]+b[0])/2, (a[1]+b[1])/2
        chip(ax, mx_ + el.get('dx', 0), my_ + el.get('dy', 0), el['text'], GOLD, DARKGOLD, FS['tiny'])
    if p.get('formula'):
        card(ax, 8, 5.5, 84, 8.5, fc='white', ec=NAVY, lw=1.6, r=1.4)
        txt_fit(ax, 50, 9.7, p['formula'], 80, FS['body'], NAVY, z=5)
    if p.get('note'): caption(ax, p['note'], 2.0)
    save(fig, out)
