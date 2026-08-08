# -*- coding: utf-8 -*-
"""FigForge · lõi style dùng chung cho 12 nguyên mẫu hình — MOBILUCK brand."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch, Polygon, Wedge
import textwrap

plt.rcParams['font.family'] = 'DejaVu Sans'

# ── bảng màu đóng (Đ5.1) ──
# Bảng màu rút từ icon thương hiệu (icon/icon.jpg) — PHẢI khớp web/tailwind.config.js,
# lệch một bên là hình và giao diện đá màu nhau.
NAVY, NAVY2, TEAL, TEAL2, GOLD, RED = '#0B4EA8', '#1268D6', '#1FCBAB', '#12A98F', '#F9B233', '#C0392B'
INK, MUTE, BG, SOFT, LINE = '#15263A', '#5B6E85', '#F8FBFD', '#E8F1FA', '#D4E1EE'
DARKTEAL, DARKGOLD, PALERED, PALETEAL = '#04382C', '#5A3A00', '#FDECE9', '#E6FAF5'

FS = dict(title=12.5, big=17, mid=13.5, body=11, small=10, tiny=9.5)   # thang cỡ chữ

def canvas(w=7.2, h=4.0):
    """Khung vẽ chuẩn: hệ toạ độ 0-100 theo chiều ngang."""
    fig, ax = plt.subplots(figsize=(w, h), dpi=170)
    H = 100 * h / w
    ax.set_xlim(0, 100); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor(BG)
    return fig, ax, H

def card(ax, x, y, w, h, fc='white', ec=LINE, lw=1.6, r=2, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.6,rounding_size={r}',
                                fc=fc, ec=ec, lw=lw, zorder=z))

def chip(ax, x, y, text, fc=GOLD, tc=DARKGOLD, fs=FS['body'], z=7):
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, zorder=z,
            bbox=dict(boxstyle='round,pad=0.45', fc=fc, ec='none'))

def arrow(ax, p1, p2, c=INK, lw=3.0, style='-|>', rad=0.0, z=4, ms=16):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=c, lw=lw,
                                 connectionstyle=f'arc3,rad={rad}', zorder=z))

def wrap(s, n=28):
    return '\n'.join(textwrap.wrap(str(s), n)) if s else ''

def caption(ax, text, y=3.2):
    ax.text(50, y, text, ha='center', fontsize=FS['small'], color=MUTE)

def save(fig, path):
    plt.tight_layout(pad=0.2)
    fig.savefig(path, facecolor=BG, bbox_inches='tight')
    plt.close(fig)

def _txt(ax, x, y, s, fs=FS['body'], c=INK, w='normal', ha='center', va='center', z=5, style=None):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=c, fontweight=w, zorder=z, style=style,
            linespacing=1.35)


# ── FIT-CHECK (Đ3.4): tự thu cỡ chữ cho vừa bề ngang cho phép ──
CHAR_W = 0.128          # bề ngang trung bình 1 ký tự / 1 pt cỡ chữ (đo thực nghiệm, có biên an toàn)

def fit_fs(text, max_w, fs=FS['mid'], floor=FS['tiny']):
    """Trả cỡ chữ lớn nhất (<= fs) để text vừa max_w đơn vị canvas."""
    longest = max((len(l) for l in str(text).split('\n')), default=0)
    while fs > floor and longest * CHAR_W * fs > max_w:
        fs -= 0.5
    return fs

def wrap_fit(s, max_w, fs=FS['mid'], max_lines=4, floor=FS['tiny']):
    """Ngắt dòng + thu cỡ chữ cho vừa bề ngang max_w.

    Khác txt_fit ở chỗ KHÔNG cắt cụt chữ: cỡ nhỏ đi thì mỗi dòng chứa được nhiều
    ký tự hơn nên số dòng giảm. Trả (chữ đã ngắt dòng, cỡ chữ, số dòng).
    """
    s = ' '.join(str(s or '').split())
    if not s:
        return '', fs, 1
    while True:
        per = max(8, int(max_w / (CHAR_W * fs)))
        lines = textwrap.wrap(s, per) or ['']
        if len(lines) <= max_lines or fs <= floor:
            return '\n'.join(lines), fs, len(lines)
        fs -= 0.5


def txt_wrap(ax, x, y, s, max_w, fs=FS['mid'], c=INK, w='bold', z=5, max_lines=4):
    """Vẽ chữ đã ngắt dòng, canh giữa theo chiều dọc quanh y."""
    text, size, n = wrap_fit(s, max_w, fs, max_lines)
    ax.text(x, y, text, ha='center', va='center', fontsize=size, color=c,
            fontweight=w, zorder=z, linespacing=1.3)
    return n


def txt_fit(ax, x, y, s, max_w, fs=FS['mid'], c=INK, w='bold', z=5, ha='center'):
    """Vẽ chữ đã thu cỡ cho vừa khung — không bao giờ tràn."""
    f = fit_fs(s, max_w, fs)
    ax.text(x, y, s, ha=ha, va='center', fontsize=f, color=c, fontweight=w, zorder=z, linespacing=1.35)
    return f

def bbox_of(x, y, w, h):
    return (x, y, x + w, y + h)

def overlap(a, b, gap=0.0):
    """True nếu hai bbox giao nhau (Đ2.2)."""
    return not (a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])
