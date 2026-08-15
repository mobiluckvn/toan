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
# ⚠ ĐỪNG GHIM MỘT QUYỂN. Bản đầu ghim `lop4`; mở sang lớp 2 thì mọi câu đều báo
# "không có bài này trong bản dựng" — đúng thật, vì nó đang tìm trong thư mục lớp 4.
QUYEN_CUA = {'KSN2': 'lop2', 'KSN3': 'lop3', 'KSN4': 'lop4', 'KSN5Q1': 'lessons'}


def _app(ma: str) -> Path:
    for k, v in QUYEN_CUA.items():
        if k in ma:
            return GOC / 'web' / 'public' / 'content' / v
    raise SystemExit(f'{ma}: không nhận ra quyển nào')

DAI_NHAT = 160


def _phang(s: str) -> str:
    return re.sub(r'\s+', '', str(s)).lower()


def co_roi(chuoi: str, tu: str) -> bool:
    """Chữ `tu` có đứng RỜI trong `chuoi` không — cùng luật với `goi_y.test.mjs`.

    ⚠ CHỖ NÀY TỪNG LỆCH VỚI CỔNG VÀ CHO LỌT BỐN GỢI Ý. Bản đầu soi bằng phép "chuỗi
    con" thô: nếu đáp án nằm đâu đó trong ĐỀ thì bỏ qua luôn, không soi gợi ý nữa.
    Mà đáp "có" thì đề nào chẳng có — "Số 10 có trong dãy không?" — nên mọi gợi ý
    của cả cụm câu ấy được tha bổng.

    Cổng thì soi bằng luật ĐỨNG RỜI: chữ phải có ranh giới hai bên. Trong đề trên,
    "có" dính ngay sau chữ số 10 nên cổng KHÔNG coi là đã có trong đề, và bắt được
    gợi ý "xem dãy có đặt chân vào số ấy không".

    Hai nơi soi khác luật thì bộ soi tại chỗ thành vô dụng — nó chỉ nói "qua rồi"
    để mình yên tâm. Nay chép đúng luật của cổng sang đây.
    """
    return bool(re.search(rf'(^|[^\d,.]){re.escape(tu)}([^\d,.]|$)', _phang(chuoi)))


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
        tep = _app(ma) / f"{ma.replace('DL:', 'DL_').replace('.', '_')}.json"
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
                    # Đáp một chữ thì câu nào chẳng dính — cổng cũng bỏ qua chúng.
                    if len(_phang(a)) < 2:
                        continue
                    if co_roi(de, a):
                        continue          # đáp đã nằm sẵn trong đề, không phải lộ
                    if co_roi(h, a):
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
