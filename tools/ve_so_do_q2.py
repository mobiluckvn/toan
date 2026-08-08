# -*- coding: utf-8 -*-
"""
BƯỚC 5b — vẽ sơ đồ Quyển 2 và gắn vào dữ liệu bài học.

    python3 tools/ve_so_do_q2.py

Bỏ qua BIÊN BẢN PHIÊN TÒA: 14 bảng ấy đã dựng thành giao diện bấm được ở màn 3
(con tick SẬP/THOÁT từng bẫy), vẽ thêm ảnh tĩnh là thừa và dễ lệch nhau.
"""
import hashlib, json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'figforge'))
from arch_q2 import bang_chien_thuat                       # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'quyen2_sodo.json')
RA_HINH = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')
KHOI_DIR = os.path.join(GOC_KHO, 'web', 'public', 'content', 'quyen2')
DATA_DIR = os.path.join(GOC_KHO, 'data', 'quyen2')
BO_QUA = 'BIÊN BẢN PHIÊN TÒA'


def main():
    so_do = json.load(open(NGUON, encoding='utf-8'))
    ve = [s for s in so_do if BO_QUA not in s['tieuDe']]
    os.makedirs(RA_HINH, exist_ok=True)

    theo_khoi, n = {}, 0
    for i, s in enumerate(ve, 1):
        ten = f'KSN5Q2_SD{i:02d}.png'
        duong = os.path.join(RA_HINH, ten)
        bang_chien_thuat({'title': s['tieuDe'], 'rows': s['hang']}, duong)
        sha = hashlib.sha256(open(duong, 'rb').read()).hexdigest()[:16]
        n += 1
        theo_khoi.setdefault(s['khoi'], []).append({
            'id': f'SD{i:02d}', 'file': f'figures/{ten}',
            'caption': s['tieuDe'], 'man': s['man'], 'sha256_16': sha,
        })

    # gắn vào từng khối
    gan = 0
    for tep in sorted(os.listdir(KHOI_DIR)):
        if not tep.startswith('DR_'):
            continue
        d = json.load(open(os.path.join(KHOI_DIR, tep), encoding='utf-8'))
        hinh = theo_khoi.get(d['id'], [])
        d['soDo'] = hinh
        gan += len(hinh)
        for thu_muc in (KHOI_DIR, DATA_DIR):
            with open(os.path.join(thu_muc, tep), 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)

    # sơ đồ của Khối 1 (trại huấn luyện) chưa có khối chứa → để riêng một tệp
    chung = theo_khoi.get(None, [])
    for thu_muc in (KHOI_DIR, DATA_DIR):
        with open(os.path.join(thu_muc, 'so_do_trai.json'), 'w', encoding='utf-8') as f:
            json.dump(chung, f, ensure_ascii=False, indent=1)

    print(f'vẽ {n} sơ đồ · gắn vào khối {gan} · trại huấn luyện {len(chung)}'
          f' · bỏ qua {len(so_do) - len(ve)} bảng phiên tòa')


if __name__ == '__main__':
    main()
