# -*- coding: utf-8 -*-
"""
TÊN BÀI LỚP 5 — thay tên dài bằng tên ngắn, KHÔNG mất chữ nào.

    python3 tools/ten_bai_lop5.py --soat      # in thử, KHÔNG ghi
    python3 tools/ten_bai_lop5.py             # ghi

── VẤN ĐỀ ──

109/168 micro lớp 5 có tên dài quá 60 chữ, dài nhất 105 chữ. Trên kệ sách, thẻ hôm
nay, thang chủ đề và sổ phụ huynh nó bị cắt cụt hoặc xuống ba dòng. Nhưng cái dở
nặng hơn không phải độ dài — mà là **tên đã đọc trước cách làm**:

    "Vòng bốn 2·3·7·8: chia số thừa số cho 4 — đọc dư như máy định vị"

Bé chưa mở bài đã biết nước đi. Đúng cái bệnh của màn mở bài trước đây, và đã chữa
một lần rồi (xem `data/loi_chao.json`).

── KHÔNG VỨT CHỮ NÀO ĐI ──

Tên gốc KHÔNG phải viết ẩu — nó là một dòng tóm tắt cách làm rất chặt, quý cho
người lớn. Nên nó không bị xoá mà dời sang trường `titleDay`: bé thấy tên ngắn,
còn sổ phụ huynh và bảng cô giáo vẫn đọc được dòng đầy đủ.

Chạy lại bao nhiêu lần cũng được: đã có `titleDay` thì giữ nguyên, không chồng
tên ngắn lên chính nó.

── BA NƠI PHẢI SỬA CÙNG LÚC ──

    data/lessons/*.json                    bản gốc
    web/public/content/lessons/*.json      bản dựng (app đọc)
    web/public/content/index_micro.json    danh mục — kệ sách & thẻ hôm nay đọc

Sót một nơi là hai màn hiện hai cái tên khác nhau cho cùng một bài. Sửa xong nhớ
dựng lại bản đồ chủ đề (`tools/dung_chu_de.py`) vì `thang[].ten` chép từ tên bài.
"""
import json, os, sys, glob

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEP_TAY = os.path.join(GOC_KHO, 'data', 'ten_bai_lop5.json')
DAI_NHAT = 60


def nap_ten():
    b = json.load(open(TEP_TAY, encoding='utf-8'))
    return b.get('ten') or {}


def _doi(o, ten):
    """Đổi `title` của một bản ghi, dời tên gốc sang `titleDay`. Trả True nếu có đổi."""
    moi = ten.get(o.get('id') or o.get('microId'))
    if not moi or o.get('title') == moi:
        return False
    # Chỉ dời MỘT lần: chạy lại thì `titleDay` đã là tên gốc thật, đừng ghi đè
    # bằng tên ngắn của lượt trước.
    o.setdefault('titleDay', o.get('title') or '')
    o['title'] = moi
    return True


def main(chi_soat=False):
    ten = nap_ten()
    dem = {'khai': len(ten), 'gốc': 0, 'dựng': 0, 'danh mục': 0, 'khai thừa': 0}

    thay = set()
    for nhan, mau in (('gốc', os.path.join(GOC_KHO, 'data', 'lessons', '*.json')),
                      ('dựng', os.path.join(GOC_KHO, 'web', 'public', 'content',
                                            'lessons', 'DL_*.json'))):
        for f in sorted(glob.glob(mau)):
            b = json.load(open(f, encoding='utf-8'))
            if _doi(b, ten):
                dem[nhan] += 1
                thay.add(b['id'])
                if not chi_soat:
                    with open(f, 'w', encoding='utf-8') as g:
                        json.dump(b, g, ensure_ascii=False, indent=1)

    dm = os.path.join(GOC_KHO, 'web', 'public', 'content', 'index_micro.json')
    b = json.load(open(dm, encoding='utf-8'))
    for o in b.values():
        if _doi(o, ten):
            dem['danh mục'] += 1
    if not chi_soat:
        with open(dm, 'w', encoding='utf-8') as g:
            json.dump(b, g, ensure_ascii=False, indent=1)

    dem['khai thừa'] = len(set(ten) - thay) if thay else 0

    for k, v in dem.items():
        print(f'{v:>5}  {k}')

    # Soát lại: còn tên nào dài quá không, và tên ngắn có trùng nhau không.
    con_dai, moi = [], {}
    for f in sorted(glob.glob(os.path.join(GOC_KHO, 'data', 'lessons', '*.json'))):
        x = json.load(open(f, encoding='utf-8'))
        t = x.get('title') or ''
        if len(t) > DAI_NHAT:
            con_dai.append((x['id'], len(t)))
        moi.setdefault(t, []).append(x['id'])
    trung = {k: v for k, v in moi.items() if len(v) > 1}
    print(f'\ncòn {len(con_dai)} tên dài quá {DAI_NHAT} chữ · {len(trung)} tên trùng nhau')
    for i, n in con_dai[:8]:
        print(f'   [{n}] {i}')
    for k, v in list(trung.items())[:5]:
        print(f'   trùng "{k}" ← {", ".join(v)}')
    return dem


if __name__ == '__main__':
    main('--soat' in sys.argv)
