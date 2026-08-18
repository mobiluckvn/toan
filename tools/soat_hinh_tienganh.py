#!/usr/bin/env python3
"""SOÁT HÌNH ↔ TỪ — in bảng để NGƯỜI nhìn, kèm tên chuẩn Unicode.

    python3 tools/soat_hinh_tienganh.py --lop 1          # bảng 60 từ
    python3 tools/soat_hinh_tienganh.py --lop 3 --lech   # chỉ in chỗ chưa ai nhìn

── VÌ SAO CẦN CÔNG CỤ NÀY ──
Bác bắt 14-08: "hình là ghế nhưng từ lại là Desk … rất nghiêm trọng". Đúng, và
đây là loại lỗi cổng không tự bắt được: máy không nhìn được tranh. Nó biết `desk`
CÓ hình, biết hình ấy không trùng ai, nhưng không biết bức hình vẽ cái ghế.

Cái máy BIẾT là **tên Unicode chính thức** của emoji. `🪑` tên là `CHAIR`. Đọc tên
ra cạnh nghĩa "cái bàn học" thì lỗi lộ ngay, không phải cãi nhau bằng cảm nhận.
Đó chính là cách tìm ra bốn chỗ sai trong đợt soát này.

Tên Unicode KHÔNG thay được người nhìn — `🎩 TOP HAT` cho "cái mũ" thì tên vẫn có
chữ HAT, mà bé lại chẳng bao giờ đội cái mũ ấy. Nên công cụ này chỉ dọn bàn cho
người soát, không thay người soát. Kết quả soát ghi vào `docs/hinh_da_soat.md`, và
`web/test/tienganh_hinh_dung_tu.test.mjs` đòi mọi từ phải có tên trong tệp ấy.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
VE = GOC / 'web' / 'src' / 'mon' / 'tienganh' / 'lib' / 'hinh_ve.json'

# ⚠ MỘT SỔ SOÁT CHO MỖI QUYỂN, và công cụ nhận `--lop`.
#
# Bản đầu ghim cứng `ta1` và `docs/hinh_da_soat.md`, lại còn `sys.exit` nếu không
# thấy đúng 16 bài. Nên suốt hai quyển sau nó không chạy được lấy một lần — mà
# `tienganh_hinh_dung_tu.test.mjs` cũng ghim `ta1` y hệt, thành ra 204 từ lớp 3
# không ai nhìn hình mà mọi cổng vẫn xanh. Xem `docs/tiep_theo_tienganh.md`.
SO_SOAT = {1: GOC / 'docs' / 'hinh_da_soat.md',
           2: GOC / 'docs' / 'hinh_da_soat_lop2.md',
           3: GOC / 'docs' / 'hinh_da_soat_lop3.md'}


def ten_unicode(e: str) -> str:
    """Tên chính thức của từng ký tự trong emoji. Đây là BẰNG CHỨNG, không phải ý kiến."""
    ra = []
    for ch in e or '':
        if ch in ('️', '‍'):      # dấu biến thể và dấu nối — không có tên riêng
            continue
        try:
            ra.append(unicodedata.name(ch))
        except ValueError:
            ra.append('?')
    return ' + '.join(ra)


def doc_bang(lop: int) -> list[tuple]:
    thu_muc = GOC / 'web' / 'public' / 'content' / f'ta{lop}'
    tep = sorted(thu_muc.glob(f'DL_TA{lop}_B*.json'))
    # Chốt "có tệp để mà soi", KHÔNG chốt một con số: glob rỗng thì mọi vòng lặp
    # chạy 0 lần và bảng ra trắng tinh, nhìn như đã sạch.
    if not tep:
        sys.exit(f'không thấy bài nào ở {thu_muc} — sai thư mục?')
    ve = json.loads(VE.read_text('utf8'))['hinh']
    ra = []
    for f in tep:
        b = json.loads(f.read_text('utf8'))
        ng = {t['tu']: t['nghia'] for t in b['knowledgeCore'].get('vocabulary', [])}
        for h in b.get('hinhTu', []):
            if h.get('ve'):
                ra.append((b['id'][-3:], h['tu'], ng.get(h['tu'], '?'),
                           f'vẽ tay `{h["ve"]}`', ve[h['ve']]['ten']))
            elif h.get('hinh'):
                ra.append((b['id'][-3:], h['tu'], ng.get(h['tu'], '?'),
                           h['hinh'], ten_unicode(h['hinh'])))
            else:
                # Từ CỐ Ý không có hình (`hello` · `fine` · `my`) — vẫn phải soát,
                # nhưng soát câu hỏi khác: "không vẽ được" có đúng không.
                ra.append((b['id'][-3:], h['tu'], ng.get(h['tu'], '?'),
                           '(không vẽ)', '—'))
    return ra


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lop', type=int, default=1, choices=[1, 2, 3])
    p.add_argument('--lech', action='store_true',
                   help='chỉ in từ chưa có trong sổ soát của quyển ấy')
    a = p.parse_args()

    bang = doc_bang(a.lop)
    so = SO_SOAT[a.lop]
    da_soat = set(re.findall(r'^\|\s*`([^`]+)`\s*\|',
                             so.read_text('utf8') if so.exists() else '', re.M))

    if a.lech:
        thieu = [r for r in bang if r[1] not in da_soat]
        for r in thieu:
            print(f'CHƯA SOÁT · {r[0]} {r[1]:12} {r[2]:18} {r[3]:16} {r[4]}')
        print(f'\n{len(thieu)}/{len(bang)} từ chưa ai nhìn hình tận mắt')
        return

    print(f"{'bài':4} {'từ':12} {'nghĩa sách':18} {'hình':16} {'tên chuẩn Unicode':34} soát")
    print('─' * 104)
    for r in bang:
        print(f'{r[0]:4} {r[1]:12} {r[2]:18} {r[3]:16} {r[4]:34} '
              + ('✓' if r[1] in da_soat else 'CHƯA'))
    print(f'\n{len(bang)} từ · {sum(1 for r in bang if r[1] in da_soat)} đã soát')
    print(f'Kết quả soát: {so.relative_to(GOC)}')


if __name__ == '__main__':
    main()
