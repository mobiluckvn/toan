# -*- coding: utf-8 -*-
"""THÊM GỢI Ý VIẾT TAY — có soi tại chỗ.

Trả món nợ lộ ra ở chương 9: 24 bài dùng video ra đời với 216 câu không một gợi ý
riêng nào, vì bộ suy gợi ý lấy từ `mantra` và bước giảng đầu — hai chỗ mà bài video
cố ý để rỗng.

Viết tay 214 câu bằng tay trần thì chắc chắn lọt, nên tệp này soi NGAY LÚC THÊM,
đúng ba luật mà `web/test/goi_y.test.mjs` canh:

  1. KHÔNG nói ra đáp án — gợi ý chứa nguyên văn đáp án thì không còn là gợi ý.
     Soi kiểu bỏ hết dấu cách rồi tìm chuỗi con, y như cổng, để hai bên không lệch.
     Chỗ này đã cắn hai lần: đáp là "có" mà gợi ý viết "…có bằng nhau không?".
  2. Tầng 1 RIÊNG từng câu — hai câu cùng bài không được mang chung một dòng.
  3. Không quá 160 chữ.

    python3 tools/them_goi_y.py --soat     # chỉ soi, không ghi
    python3 tools/them_goi_y.py            # ghi vào data/goi_y_tay.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
TAY = GOC / 'data' / 'goi_y_tay.json'
APP = GOC / 'web' / 'public' / 'content' / 'lop4'

DAI_NHAT = 160


def _phang(s: str) -> str:
    return re.sub(r'\s+', '', str(s)).lower()


def dap_an(item) -> list[str]:
    """Mọi chuỗi coi là đáp án của một câu — lấy đúng cách cổng lấy."""
    k = item.get('answerKey') or {}
    ra = []
    if 'parts' in k:
        ra += [p.get('value') for p in k['parts']]
    for t in ('value', 'values', 'accept'):
        if t in k:
            v = k[t]
            ra += v if isinstance(v, list) else [v]
    return [str(x) for x in ra if x is not None and str(x) != '']


def soi(bo: dict) -> list[str]:
    """Soi trước khi ghi. Trả về danh sách chỗ chưa đạt."""
    loi = []
    for ma, cau in bo.items():
        tep = APP / f"{ma.replace('DL:', 'DL_').replace('.', '_')}.json"
        if not tep.exists():
            loi.append(f'{ma}: không có bài này trong bản dựng')
            continue
        d = json.loads(tep.read_text('utf8'))
        co = {c['id']: c for v in d['practice']['pools'].values() for c in v}
        tang1 = {}
        for cid, hs in cau.items():
            if cid not in co:
                loi.append(f'{ma} {cid}: bài không có câu này')
                continue
            if len(hs) != 2:
                loi.append(f'{ma} {cid}: phải đúng 2 tầng gợi ý')
                continue
            de = _phang(co[cid].get('text', ''))
            for h in hs:
                if len(str(h)) > DAI_NHAT:
                    loi.append(f'{ma} {cid}: gợi ý dài {len(str(h))} chữ')
                for a in dap_an(co[cid]):
                    if _phang(a) in de:
                        continue          # đáp đã nằm sẵn trong đề, không phải lộ
                    if _phang(a) in _phang(h):
                        loi.append(f'{ma} {cid}: gợi ý lộ đáp "{a}" → "{h[:44]}…"')
            if hs[0] in tang1:
                loi.append(f'{ma} {cid}: tầng 1 trùng với {tang1[hs[0]]}')
            tang1[hs[0]] = cid
    return loi


def them(bo: dict, chi_soat=False) -> int:
    loi = soi(bo)
    if loi:
        for x in loi:
            print('  ✗', x)
        print(f'\n{len(loi)} chỗ chưa đạt — CHƯA ghi gì cả')
        return 1
    n = sum(len(v) for v in bo.values())
    print(f'  ✓ {n} câu qua cả ba phép soi')
    if chi_soat:
        print('(--soat: chưa ghi)')
        return 0
    d = json.loads(TAY.read_text('utf8'))
    for ma, cau in bo.items():
        d.setdefault(ma, {}).update(cau)
    TAY.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'ghi {n} câu vào {TAY.relative_to(GOC)}')
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--soat', action='store_true')
    p.add_argument('--tep', type=Path, required=True,
                   help='tệp JSON chứa gợi ý cần thêm')
    a = p.parse_args()
    return them(json.loads(a.tep.read_text('utf8')), a.soat)


if __name__ == '__main__':
    sys.exit(main())
