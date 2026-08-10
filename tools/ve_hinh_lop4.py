# -*- coding: utf-8 -*-
"""
Vẽ hình lớp 3 từ bản mô tả data/lop4_hinh.json.

    python3 tools/ve_hinh_lop4.py             # vẽ tất cả
    python3 tools/ve_hinh_lop4.py L4H_B01_MO  # vẽ riêng vài hình, để dò nhanh

CHỈ vẽ ra PNG và ghi sổ tay hình. KHÔNG gắn vào bài học ở đây — việc gắn phải nằm ở
BƯỚC CUỐI, vì chạy lại `chuan_lop4.py` sẽ ghi đè sạch phần hình vừa gắn mà không báo
gì (bẫy đã dính ở Quyển 2 lớp 5, rồi lớp 2 dính lại).
"""
import hashlib, json, os, sys
from collections import Counter

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'figforge'))
import arch_l4                                              # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop4_hinh.json')
RA_HINH = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop4_hinh_manifest.json')

# Tiêu đề hình không quá 120 chữ (chuẩn mục 5). Trên ngưỡng ấy nó là một đoạn văn
# đè lên đầu hình — 122 hình lớp 5 đã dính, mà phần hình bên dưới vẫn vẽ đẹp nên
# nhìn lướt không thấy sai.
DAI_TIEU_DE = 120


def main(loc=None):
    tat_ca = json.load(open(NGUON, encoding='utf-8'))
    trung = [k for k, v in Counter(m['id'] for m in tat_ca).items() if v > 1]
    if trung:
        # Trùng mã thì hình sau ĐÈ hình trước, và cái mất đi không kêu ca gì —
        # tôi đã dính đúng chỗ này khi đặt L3H_BT01 cho hai hình khác nhau.
        sys.exit(f'DỪNG: trùng mã hình {", ".join(trung)} — mỗi hình một mã riêng')

    mo_ta = tat_ca
    if loc:
        mo_ta = [m for m in tat_ca if m['id'] in loc]
        if not mo_ta:
            sys.exit(f'không có hình nào tên {", ".join(loc)}')
    os.makedirs(RA_HINH, exist_ok=True)

    so_tay = {}
    if os.path.exists(SO_TAY):
        so_tay = json.load(open(SO_TAY, encoding='utf-8'))

    # Sổ tay CHỈ THÊM thì mã đã bỏ hoặc đã đổi tên vẫn nằm lại, trỏ vào ảnh không
    # còn — bước gắn hình đọc sổ tay nên nó sẽ đòi một tệp đã xoá. Lượt chạy đầy đủ
    # phải dọn, và NÓI RA đã dọn cái gì.
    if not loc:
        con = {m['id'] for m in tat_ca}
        bo = sorted(k for k in so_tay if k not in con)
        for k in bo:
            so_tay.pop(k)
            png = os.path.join(RA_HINH, f'{k}.png')
            if os.path.exists(png):
                os.remove(png)
            print(f'  ␡ bỏ {k} — không còn trong bản mô tả')

    loi = []
    for m in mo_ta:
        ve = getattr(arch_l4, m['arch'], None)
        if ve is None:
            sys.exit(f"{m['id']}: chưa có nguyên mẫu '{m['arch']}' trong figforge/arch_l4.py")
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
