# -*- coding: utf-8 -*-
"""
Nguyên mẫu riêng cho QUYỂN 2 — bảng chiến thuật phòng thi.

Sách Quyển 2 chèn sơ đồ ở 67 chỗ, và chúng đều cùng MỘT hình dạng: một tiêu đề rồi
các cặp (nhãn ngắn · lời giải thích). Nên chỉ cần một nguyên mẫu, không phải mô tả
tay từng cái — khác hẳn 25 nguyên mẫu của Quyển 1 vốn là hình toán mỗi cái một kiểu.

Dùng chung bảng màu ở core.py (đã rút từ icon thương hiệu), nên đổi màu một lần là
cả Quyển 1 lẫn Quyển 2 đổi theo.
"""
from core import (canvas, card, save, txt_fit, wrap_fit, _txt,
                  NAVY, TEAL, GOLD, DARKTEAL, DARKGOLD, INK, MUTE, LINE, SOFT, FS)

# Màu luân phiên cho từng hàng — đọc bảng dài đỡ lạc dòng
VIEN = [TEAL, GOLD, NAVY]
NEN = ['#E6FAF5', '#FFF4DF', '#EAF2FB']
CHU_NHAN = [DARKTEAL, DARKGOLD, NAVY]


def bang_chien_thuat(p, out):
    """
    params:
      title  tiêu đề bảng
      rows   [[nhãn, mô tả], …]
      note   dòng ghi chú dưới cùng (tuỳ chọn)

    Cột trái hẹp (nhãn), cột phải rộng (lời giải thích) — đúng tỉ lệ của sách.
    Chiều cao tính theo SỐ DÒNG THẬT sau khi ngắt chữ, không cố định: bảng 4 hàng
    và bảng 12 hàng mà cùng chiều cao thì một cái rỗng toác, một cái chữ đè nhau.
    """
    rows = [r for r in (p.get('rows') or []) if any(str(x).strip() for x in r)]
    if not rows:
        rows = [['', '']]

    W_NHAN, W_MO = 27.0, 60.0
    X_NHAN, X_MO = 5.0, 35.0

    # đo trước: mỗi hàng cao bao nhiêu
    # wrap_fit trả về (chữ đã ngắt dòng, cỡ chữ, SỐ DÒNG) — ba giá trị, không phải hai
    dong = []
    for nhan, mo in rows:
        s_nhan, fs_nhan, _ = wrap_fit(str(nhan), W_NHAN - 3, FS['body'], max_lines=3)
        s_mo, fs_mo, _ = wrap_fit(str(mo), W_MO - 3, FS['small'], max_lines=6)
        d_nhan, d_mo = s_nhan.split('\n'), s_mo.split('\n')
        n = max(len(d_nhan), len(d_mo))
        dong.append(((d_nhan, fs_nhan), (d_mo, fs_mo), max(7.0, 3.4 * n + 3.2)))

    cao_bang = sum(d[2] + 1.4 for d in dong)
    tren = 11.0 if p.get('title') else 4.0
    duoi = 7.0 if p.get('note') else 3.0
    can = tren + cao_bang + duoi

    fig, ax, H = canvas(7.6, max(2.6, can * 7.6 / 100))

    if p.get('title'):
        txt_fit(ax, 50, H - 5.2, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren
    for i, ((d_nhan, fs_nhan), (d_mo, fs_mo), cao) in enumerate(dong):
        vien, nen, cn = VIEN[i % 3], NEN[i % 3], CHU_NHAN[i % 3]
        # ô nhãn
        card(ax, X_NHAN, y - cao, W_NHAN, cao, fc=nen, ec=vien, lw=1.6, r=1.4)
        for k, dg in enumerate(d_nhan):
            _txt(ax, X_NHAN + W_NHAN / 2, y - cao / 2 + (len(d_nhan) - 1 - 2 * k) * 1.7,
                 dg, fs=fs_nhan, c=cn, w='bold', z=5)
        # ô mô tả
        card(ax, X_MO, y - cao, W_MO, cao, fc='white', ec=LINE, lw=1.2, r=1.4)
        for k, dg in enumerate(d_mo):
            _txt(ax, X_MO + 1.6, y - cao / 2 + (len(d_mo) - 1 - 2 * k) * 1.7,
                 dg, fs=fs_mo, c=INK, ha='left', z=5)
        y -= cao + 1.4

    if p.get('note'):
        txt_fit(ax, 50, y - 2.2, p['note'], 92, FS['small'], MUTE, z=5)

    save(fig, out)
