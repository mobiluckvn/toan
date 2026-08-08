# -*- coding: utf-8 -*-
"""
Vẽ hình lớp 2 từ bản mô tả data/lop2_hinh.json.

    python3 tools/ve_hinh_lop2.py            # vẽ tất cả
    python3 tools/ve_hinh_lop2.py L2H_MAY03  # vẽ riêng vài hình, để dò nhanh

CHỈ vẽ ra PNG và ghi sổ tay hình. KHÔNG gắn vào bài học ở đây — việc gắn phải
nằm ở BƯỚC CUỐI của tools/lam_lop2.py, vì chạy lại bộ dựng dữ liệu sẽ ghi đè
sạch phần hình vừa gắn mà không báo gì (đã dính đúng lỗi này ở Quyển 2 lớp 5).
"""
import hashlib, json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'figforge'))
import arch_l2                                              # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop2_hinh.json')
RA_HINH = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop2_hinh_manifest.json')


def main(loc=None):
    mo_ta = json.load(open(NGUON, encoding='utf-8'))
    if loc:
        mo_ta = [m for m in mo_ta if m['id'] in loc]
        if not mo_ta:
            sys.exit(f'không có hình nào tên {", ".join(loc)}')
    os.makedirs(RA_HINH, exist_ok=True)

    so_tay = {}
    if os.path.exists(SO_TAY):
        so_tay = json.load(open(SO_TAY, encoding='utf-8'))

    for m in mo_ta:
        ve = getattr(arch_l2, m['arch'], None)
        if ve is None:
            sys.exit(f"{m['id']}: chưa có nguyên mẫu '{m['arch']}' trong figforge/arch_l2.py")
        ten = f"{m['id']}.png"
        duong = os.path.join(RA_HINH, ten)
        ve(m['params'], duong)
        sha = hashlib.sha256(open(duong, 'rb').read()).hexdigest()[:16]
        so_tay[m['id']] = {
            'file': f'figures/{ten}', 'caption': m['caption'], 'bai': m['bai'],
            'muc': m['muc'], 'neoBuoc': m.get('neoBuoc', 0), 'neoCau': m.get('neoCau'),
            'hoan': m.get('hoan'),
            'goc': m['goc'], 'sha256_16': sha,
        }
        print(f"  {m['id']}  {m['goc']:>13s} → {ten}  {sha}")

    with open(SO_TAY, 'w', encoding='utf-8') as f:
        json.dump(so_tay, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f'\nvẽ {len(mo_ta)} hình · sổ tay có {len(so_tay)} mục → {os.path.relpath(SO_TAY, GOC_KHO)}')


if __name__ == '__main__':
    main(sys.argv[1:] or None)
