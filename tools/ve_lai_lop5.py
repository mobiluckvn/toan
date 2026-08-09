# -*- coding: utf-8 -*-
"""
LỚP 5 — vẽ lại những hình có chữ vừa bị sửa.

    python3 tools/ve_lai_lop5.py --soat    # chỉ liệt kê hình cần vẽ lại
    python3 tools/ve_lai_lop5.py           # vẽ lại + cập nhật sha trong bài học

VÌ SAO PHẢI CÓ BƯỚC NÀY: `figureSpec[].params` là BẢN MÔ TẢ, còn PNG là bản đã vẽ.
Sửa chữ trong params mà không vẽ lại thì dữ liệu nói một đằng, ảnh hiện một nẻo —
bé vẫn nhìn thấy "∈ {0; 2; 4}" trên hình dù trong dữ liệu đã đổi thành "là 0, 2
hoặc 4". Không có gì báo, vì cả hai đều hợp lệ.

Chỉ vẽ lại hình có params ĐỔI THẬT (so sha của chính bản mô tả), không vẽ lại cả
672 hình — vẽ lại toàn bộ vừa chậm vừa làm 600 hình đổi mã kiểm vô cớ, khiến máy
của bé phải tải lại hết.
"""
import hashlib, json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'figforge'))
from render import RENDERERS, fname                          # noqa: E402

DATA = os.path.join(GOC_KHO, 'data', 'lessons')
PUBLIC = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lessons')
HINH = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')
MANIFEST = os.path.join(GOC_KHO, 'data', 'figure_manifest.json')


def ma_mo_ta(f):
    """Mã của BẢN MÔ TẢ — đổi chữ trong params là mã đổi theo."""
    goi = json.dumps({'a': f.get('archetype'), 'p': f.get('params')},
                     ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(goi.encode('utf-8')).hexdigest()[:16]


def main(chi_soat=False):
    can_ve, thieu_ve, loi = [], [], []
    for ten in sorted(os.listdir(DATA)):
        if not ten.startswith('DL_KSN5Q1_'):
            continue
        d = json.load(open(os.path.join(DATA, ten), encoding='utf-8'))
        for f in d.get('figureSpec') or []:
            png = os.path.join(HINH, os.path.basename(f['file']))
            if not os.path.exists(png):
                thieu_ve.append((d['id'], f['id']))
                continue
            # Vẽ thử vào tệp tạm rồi so mã kiểm: khác nghĩa là chữ trên hình đã đổi.
            can_ve.append((ten, d['id'], f, png))

    ve, giu = 0, 0
    for ten, mid, f, png in can_ve:
        arch = RENDERERS.get(f.get('archetype'))
        if arch is None:
            loi.append((mid, f['id'], f.get('archetype'), 'không có nguyên mẫu'))
            continue
        # đuôi phải là .png — matplotlib chọn định dạng theo ĐUÔI TỆP
        tam = png[:-4] + '.thu.png'
        try:
            arch(f['params'], tam)
        except Exception as e:
            loi.append((mid, f['id'], f.get('archetype'), repr(e)[:90]))
            if os.path.exists(tam):
                os.remove(tam)
            continue
        moi = hashlib.sha256(open(tam, 'rb').read()).hexdigest()[:16]
        cu = hashlib.sha256(open(png, 'rb').read()).hexdigest()[:16]
        if moi == cu:
            giu += 1
            os.remove(tam)
            continue
        ve += 1
        if chi_soat:
            os.remove(tam)
            print(f'  cần vẽ lại  {mid}#{f["id"]}  {f.get("archetype")}')
        else:
            os.replace(tam, png)
            f['sha256_16'] = moi

    if not chi_soat:
        so_hinh = json.load(open(MANIFEST, encoding='utf-8'))
        # ghi lại bài học có sha mới, đủ CẢ HAI nơi
        for ten in sorted(os.listdir(DATA)):
            if not ten.startswith('DL_KSN5Q1_'):
                continue
            d = json.load(open(os.path.join(DATA, ten), encoding='utf-8'))
            for f in d.get('figureSpec') or []:
                png = os.path.join(HINH, os.path.basename(f['file']))
                if os.path.exists(png):
                    f['sha256_16'] = hashlib.sha256(open(png, 'rb').read()).hexdigest()[:16]
            for thu_muc in (DATA, PUBLIC):
                with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as fh:
                    json.dump(d, fh, ensure_ascii=False, indent=1)
            # SỔ HÌNH là nơi thứ ba chép lại mã kiểm và lời chú. Quên nó thì bài học
            # nói một đằng, sổ nói một nẻo — bài kiểm "mã kiểm hình khớp PNG thật"
            # bắt được, nhưng chỉ khi mình nhớ chạy. Cập nhật ngay tại đây.
            for f in d.get('figureSpec') or []:
                # khoá sổ là "DL:KSN5Q1.B10.M1#F1", còn f['id'] chỉ là "F1"
                muc = so_hinh.get(f"{d['id']}#{f['id']}")
                if muc is None:
                    continue
                muc['sha256_16'] = f['sha256_16']
                if f.get('caption'):
                    muc['caption'] = f['caption']

        with open(MANIFEST, 'w', encoding='utf-8') as fh:
            json.dump(so_hinh, fh, ensure_ascii=False, indent=1)

    print(f'{ve} hình vẽ lại · {giu} hình giữ nguyên'
          + (' (CHƯA ghi)' if chi_soat else ''))
    if thieu_ve:
        print(f'  ⚠ {len(thieu_ve)} hình khai trong bài mà không có tệp PNG')
    for m, i, a, e in loi[:10]:
        print(f'  ✗ {m}#{i} [{a}] {e}')
    if loi:
        print(f'  ✗ tổng {len(loi)} hình không vẽ được')
    return ve, loi


if __name__ == '__main__':
    main('--soat' in sys.argv)
