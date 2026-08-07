# -*- coding: utf-8 -*-
"""Nguyên mẫu 5-8: hình học phẳng · khối 3D · đồng hồ · bậc thang."""
from core import *
from core import _txt, txt_fit, fit_fs, overlap, bbox_of
import numpy as np

# ═══ 5 · plane_geometry — hình tròn / tam giác / tứ giác (9%) ═══
def plane_geometry(p, out):
    """params: shape: circle|triangle|rect|trapezoid, dims{}, marks[], memo[], caption, title"""
    fig, ax, H = canvas(7.2, 4.0)
    if p.get('title'):
        _txt(ax, 50, H - 4, p['title'], FS['title'], NAVY, 'bold')
    cx, cy = 32, H/2 - 2
    sh = p['shape']; D = p.get('dims', {})
    if sh == 'circle':
        R = 21
        ax.add_patch(Circle((cx, cy), R, fc=SOFT, ec=NAVY, lw=3.2, zorder=2))
        ax.add_patch(Circle((cx, cy), 1.1, fc=NAVY, zorder=6))
        if D.get('d'):
            arrow(ax, (cx-R, cy), (cx+R, cy), c=GOLD, lw=3.4, style='<|-|>', ms=17)
            chip(ax, cx, cy-6.8, D['d'], GOLD, DARKGOLD, FS['body'])
        if D.get('r'):
            arrow(ax, (cx, cy), (cx, cy+R), c=TEAL, lw=3.4, ms=17)
            chip(ax, cx+8.5, cy+11, D['r'], TEAL, DARKTEAL, FS['small'])
    elif sh in ('rect', 'square'):
        w, h = (34, 24) if sh == 'rect' else (26, 26)
        ax.add_patch(Rectangle((cx-w/2, cy-h/2), w, h, fc=SOFT, ec=NAVY, lw=3, zorder=2))
        if D.get('w'): chip(ax, cx, cy-h/2-5, D['w'], GOLD, DARKGOLD, FS['small'])
        if D.get('h'): chip(ax, cx-w/2-8, cy, D['h'], TEAL, DARKTEAL, FS['small'])
    elif sh == 'triangle':
        pts = [(cx-20, cy-13), (cx+20, cy-13), (cx-2, cy+17)]
        ax.add_patch(Polygon(pts, fc=SOFT, ec=NAVY, lw=3, zorder=2))
        ax.plot([-2+cx, -2+cx], [cy-13, cy+17], color=TEAL, lw=2.6, ls=(0, (5, 4)), zorder=3)
        if D.get('base'): chip(ax, cx, cy-18, D['base'], GOLD, DARKGOLD, FS['small'])
        if D.get('height'): chip(ax, cx+10, cy+3, D['height'], TEAL, DARKTEAL, FS['small'])
    elif sh == 'trapezoid':
        pts = [(cx-21, cy-12), (cx+21, cy-12), (cx+12, cy+13), (cx-12, cy+13)]
        ax.add_patch(Polygon(pts, fc=SOFT, ec=NAVY, lw=3, zorder=2))
        if D.get('a'): chip(ax, cx, cy+17, D['a'], GOLD, DARKGOLD, FS['small'])
        if D.get('b'): chip(ax, cx, cy-17, D['b'], GOLD, DARKGOLD, FS['small'])
        if D.get('height'):
            ax.plot([cx, cx], [cy-12, cy+13], color=TEAL, lw=2.6, ls=(0, (5, 4)), zorder=3)
            chip(ax, cx+9, cy+1, D['height'], TEAL, DARKTEAL, FS['small'])
    if p.get('memo'):
        card(ax, 62, cy-16, 34, 32)
        _txt(ax, 79, cy+9, 'GHI NHỚ', FS['tiny'], MUTE, 'bold', z=3)
        for i, m in enumerate(p['memo'][:2]):
            _txt(ax, 79, cy+0.5-i*8, m, FS['big'], NAVY if i == 0 else TEAL, 'bold', z=3)
    if p.get('caption'): caption(ax, p['caption'])
    save(fig, out)

# ═══ 6 · solid_3d — hình hộp / lập phương (6%) ═══
def _box3d(ax, x, y, w, h, dp, fc=SOFT, ec=NAVY, lw=2.6):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=3))
    top = [(x, y+h), (x+dp, y+h+dp*0.7), (x+w+dp, y+h+dp*0.7), (x+w, y+h)]
    side = [(x+w, y), (x+w+dp, y+dp*0.7), (x+w+dp, y+h+dp*0.7), (x+w, y+h)]
    ax.add_patch(Polygon(top, fc='#DCE9F5', ec=ec, lw=lw, zorder=2))
    ax.add_patch(Polygon(side, fc='#CFE0F0', ec=ec, lw=lw, zorder=2))

def solid_3d(p, out):
    """params: title, kind: box|cube, dims{a,b,c}, layers(int|None), memo[], caption"""
    fig, ax, H = canvas(7.2, 4.0)
    if p.get('title'):
        _txt(ax, 50, H - 4, p['title'], FS['title'], NAVY, 'bold')
    x, y, w, h, dp = 10, H/2-15, 27, 21, 9
    _box3d(ax, x, y, w, h, dp)
    D = p.get('dims', {})
    if D.get('a'): chip(ax, x+w/2, y-5, D['a'], GOLD, DARKGOLD, FS['small'])
    if D.get('c'): chip(ax, x-7.5, y+h/2, D['c'], TEAL, DARKTEAL, FS['small'])
    if D.get('b'): chip(ax, x+w+dp*0.55, y+h+dp*0.7+4.5, D['b'], NAVY2, 'white', FS['small'])
    if p.get('layers'):
        for i in range(1, p['layers']):
            yy = y + h*i/p['layers']
            ax.plot([x, x+w], [yy, yy], color=NAVY, lw=1.2, ls=(0, (3, 3)), zorder=4)
    if p.get('memo'):
        CX, CW = 60, 36
        card(ax, CX, y-3, CW, h+14)
        _txt(ax, CX+CW/2, y+h+7, 'CÔNG THỨC', FS['tiny'], MUTE, 'bold', z=3)
        for i, m in enumerate(p['memo'][:3]):
            txt_fit(ax, CX+CW/2, y+h-1-i*8, m, CW-6, FS['mid'], [NAVY, TEAL, GOLD][i], z=3)
    if p.get('caption'): caption(ax, p['caption'])
    save(fig, out)

# ═══ 7 · clock_face — đồng hồ (5%) ═══
def clock_face(p, out):
    """params: title, clocks[{hour, minute, label}], note"""
    cs = p['clocks']; n = len(cs)
    fig, ax, H = canvas(7.2, 3.9)
    if p.get('title'):
        _txt(ax, 50, H - 4, p['title'], FS['title'], NAVY, 'bold')
    R = 13; span = 100/n
    for i, c in enumerate(cs):
        cx, cy = span*(i+0.5), H/2 + 1.5
        ax.add_patch(Circle((cx, cy), R, fc='white', ec=NAVY, lw=3, zorder=2))
        for t in range(12):
            a = np.pi/2 - t*np.pi/6
            ax.plot([cx+np.cos(a)*(R-2.2)], [cy+np.sin(a)*(R-2.2)], marker='o', ms=2.4,
                    color=NAVY if t % 3 == 0 else LINE, zorder=3)
        ah = np.pi/2 - (c['hour'] % 12 + c['minute']/60) * np.pi/6
        am = np.pi/2 - c['minute'] * np.pi/30
        ax.plot([cx, cx+np.cos(ah)*R*0.5], [cy, cy+np.sin(ah)*R*0.5], color=NAVY, lw=4,
                solid_capstyle='round', zorder=5)
        ax.plot([cx, cx+np.cos(am)*R*0.78], [cy, cy+np.sin(am)*R*0.78], color=TEAL, lw=3,
                solid_capstyle='round', zorder=5)
        ax.add_patch(Circle((cx, cy), 1.3, fc=GOLD, ec=NAVY, lw=1, zorder=6))
        if c.get('label'):
            chip(ax, cx, cy-R-5.5, c['label'], GOLD, DARKGOLD, FS['small'])
    # (nhãn nằm trên caption — kiểm khoảng thở ở dưới)
    if p.get('note'): caption(ax, p['note'], 2.6)
    save(fig, out)

# ═══ 8 · ladder_steps — bậc thang / tăng dần (2%) ═══
def ladder_steps(p, out):
    """params: title, steps[{text, sub}], note — bậc dưới trái leo lên bậc trên phải

    Bậc CAO THEO CHỮ: đo trước mỗi bậc cần mấy dòng rồi mới dựng khung, nhờ vậy
    câu dài được ngắt dòng đủ ý thay vì bị cắt cụt bằng dấu '…'.
    """
    st = p['steps']; n = len(st)
    bw = min(46, 92 - (n - 1) * 12)
    plan = []
    for s in st:
        _, _, nl = wrap_fit(s['text'], bw - 5, FS['mid'], max_lines=3)
        ns = 0
        if s.get('sub'):
            _, _, ns = wrap_fit(s['sub'], bw - 5, FS['tiny'], max_lines=2)
        plan.append((nl, ns, 5.5 + 4.2 * nl + 3.4 * ns))
    bh = max(h for _, _, h in plan)
    slot = bh + 4.0
    tn = wrap_fit(p['title'], 92, FS['title'], max_lines=2)[2] if p.get('title') else 0
    top = (4.0 + 4.6 * tn) if tn else 3.0
    bot = 8 if p.get('note') else 4
    need = top + slot * n + bot
    fig, ax, H = canvas(7.2, max(1.9, need * 7.2 / 100))

    if tn:
        txt_wrap(ax, 50, H - 2.4 - 2.3 * tn, p['title'], 92, FS['title'], NAVY, z=6, max_lines=2)
    for i, (s, (nl, ns, _)) in enumerate(zip(st, plan)):   # i = 0 là bậc dưới cùng
        x = 5 + i * ((92 - bw) / max(n - 1, 1))
        y = bot + i * slot
        col = [NAVY, NAVY2, TEAL, GOLD][i % 4]
        tc = 'white' if col in (NAVY, NAVY2) else (DARKTEAL if col == TEAL else DARKGOLD)
        card(ax, x, y, bw, bh, fc=col, ec='none', r=1.6)
        cy = y + bh / 2 + (1.8 * ns if ns else 0)
        txt_wrap(ax, x + bw / 2, cy, s['text'], bw - 5, FS['mid'], tc, z=5, max_lines=3)
        if ns:
            txt_wrap(ax, x + bw / 2, cy - 2.1 * nl - 1.9, s['sub'], bw - 5, FS['tiny'], tc,
                     z=5, max_lines=2)
        if i < n - 1:
            nx = 5 + (i + 1) * ((92 - bw) / max(n - 1, 1))
            arrow(ax, (x + bw * 0.72, y + bh + 0.4), (nx + bw * 0.28, y + slot - 0.4),
                  c=MUTE, lw=2, ms=13, rad=-0.25)
    if p.get('note'):
        caption(ax, p['note'], 2.6)
    save(fig, out)
