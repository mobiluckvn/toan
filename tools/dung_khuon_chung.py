# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 5 — dựng bản cho app theo KHUÔN CHUNG với lớp 5.

    python3 tools/dung_khuon_chung.py

Hai thư mục, hai vai khác nhau — đừng sửa nhầm:
    data/lop2/                    BẢN GỐC: giữ nguyên 8 mục ①…⑧ của sách, để người
                                  đối chiếu với sách giấy. Các bước 1–4 ghi vào đây.
    web/public/content/lop2/      BẢN CHO APP: đúng khuôn lớp 5, sinh ra từ bản gốc.
                                  KHÔNG sửa tay ở đây, chạy lại bước này là mất.

Nhờ cùng khuôn mà lớp 2 dùng được nguyên bộ mã của lớp 5: nhật ký học, sổ phụ
huynh, bảng cô giáo, BKT, nhớ chỗ học dở, gợi ý theo số lần sai.
"""
import json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'tools'))
from khuon_chung import sang_khuon_chung                    # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop2')
RA = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop2')
SO_DK = os.path.join(GOC_KHO, 'data', 'chuong_trinh.json')
RA_DK = os.path.join(GOC_KHO, 'web', 'public', 'content', 'chuong_trinh.json')


def main():
    os.makedirs(RA, exist_ok=True)
    teps = sorted(f for f in os.listdir(NGUON) if f.startswith('DL_KSN2_B'))
    bais = [json.load(open(os.path.join(NGUON, t), encoding='utf-8')) for t in teps]
    bais.sort(key=lambda b: b['so'])
    ids = [b['id'] for b in bais]

    idx = []
    for k, b in enumerate(bais):
        d = sang_khuon_chung(b, truoc=ids[k - 1] if k else None,
                             sau=ids[k + 1] if k + 1 < len(ids) else None)
        ten = b['id'].replace('DL:', 'DL_').replace('.', '_') + '.json'
        with open(os.path.join(RA, ten), 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        idx.append({
            'id': d['id'], 'so': d['so'], 'ten': b['ten'], 'title': d['title'],
            'chuong': d['chuong'], 'tenChuong': d['tenChuong'],
            'bktUnit': d['skills']['bktUnit'], 'passRule': d['assessment']['passRule'],
            'objective': d['objective']['kidText'],
            'durationMinutes': d['durationMinutes'],
            'soCau': sum(len(v) for v in d['practice']['pools'].values()),
            'soQuiz': len(d['assessment']['items']),
            'soHinh': len(d['figureSpec']),
        })

    with open(os.path.join(RA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)

    # sổ đăng ký chương trình — nơi DUY NHẤT khai khác biệt giữa hai lớp
    dk = json.load(open(SO_DK, encoding='utf-8'))
    dk['lop2']['bai'] = ids
    for thu_muc, duong in ((None, SO_DK), (None, RA_DK)):
        with open(duong, 'w', encoding='utf-8') as f:
            json.dump(dk, f, ensure_ascii=False, indent=1)

    tong_hinh = sum(x['soHinh'] for x in idx)
    tong_cau = sum(x['soCau'] for x in idx)
    tong_quiz = sum(x['soQuiz'] for x in idx)
    print(f'dựng {len(idx)} bài theo khuôn chung → {os.path.relpath(RA, GOC_KHO)}')
    print(f'  {tong_cau} câu luyện tập · {tong_quiz} câu sát hạch · {tong_hinh} hình')


if __name__ == '__main__':
    main()
