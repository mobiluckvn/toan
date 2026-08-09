# -*- coding: utf-8 -*-
"""
Vẽ hình lớp 3 từ bản mô tả data/lop3_hinh.json.

    python3 tools/ve_hinh_lop3.py             # vẽ tất cả
    python3 tools/ve_hinh_lop3.py L3H_TRON01  # vẽ riêng vài hình, để dò nhanh

CHỈ vẽ ra PNG và ghi sổ tay hình. KHÔNG gắn vào bài học ở đây — việc gắn phải nằm ở
BƯỚC CUỐI, vì chạy lại `chuan_lop3.py` sẽ ghi đè sạch phần hình vừa gắn mà không báo
gì (bẫy đã dính ở Quyển 2 lớp 5, rồi lớp 2 dính lại).
"""
import hashlib, json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'figforge'))
import arch_l3                                              # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop3_hinh.json')
RA_HINH = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop3_hinh_manifest.json')

# Tiêu đề hình không quá 120 chữ (chuẩn mục 5). Trên ngưỡng ấy nó là một đoạn văn
# đè lên đầu hình — 122 hình lớp 5 đã dính, mà phần hình bên dưới vẫn vẽ đẹp nên
# nhìn lướt không thấy sai.
DAI_TIEU_DE = 120


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

    loi = []
    for m in mo_ta:
        ve = getattr(arch_l3, m['arch'], None)
        if ve is None:
            sys.exit(f"{m['id']}: chưa có nguyên mẫu '{m['arch']}' trong figforge/arch_l3.py")
        for truong in ('title', 'note'):
            s = (m['params'].get(truong) or '')
            if len(s) > DAI_TIEU_DE:
                loi.append(f"{m['id']}: {truong} dài {len(s)} chữ (tối đa {DAI_TIEU_DE})")
        ten = f"{m['id']}.png"
        duong = os.path.join(RA_HINH, ten)
        ve(m['params'], duong)
        sha = hashlib.sha256(open(duong, 'rb').read()).hexdigest()[:16]
        so_tay[m['id']] = {
            'file': f'figures/{ten}', 'caption': m['caption'], 'bai': m['bai'],
            'muc': m['muc'], 'neoBuoc': m.get('neoBuoc', 0), 'neoCau': m.get('neoCau'),
            # 'giai' = hình chỉ hiện sau khi bé làm xong. Sổ tay phải chép lại, vì
            # bước gắn hình đọc SỔ TAY chứ không đọc bản mô tả.
            'vaiTro': m.get('vaiTro'),
            'hoan': m.get('hoan'), 'onTap': m.get('onTap'),
            'goc': m.get('goc', ''), 'sha256_16': sha,
        }
        print(f"  {m['id']:<14} {m.get('goc', '—'):>13s} → {ten}  {sha}")

    with open(SO_TAY, 'w', encoding='utf-8') as f:
        json.dump(so_tay, f, ensure_ascii=False, indent=1, sort_keys=True)
    for x in loi:
        print(f'  ⚠ {x}')
    print(f'\nvẽ {len(mo_ta)} hình · sổ tay có {len(so_tay)} mục '
          f'→ {os.path.relpath(SO_TAY, GOC_KHO)}')
    return 1 if loi else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:] or None))
