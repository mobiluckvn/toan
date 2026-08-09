# -*- coding: utf-8 -*-
"""
LỚP 5 — cắt tiêu đề hình dài thành tiêu đề đọc được.

    python3 tools/tieu_de_hinh_lop5.py --soat    # chỉ liệt kê, KHÔNG ghi
    python3 tools/tieu_de_hinh_lop5.py           # ghi vào data/ và web/public/

VẤN ĐỀ: 122 hình lấy nguyên `objective.text` (dài tới 397 chữ) làm tiêu đề hình.
Vẽ ra là bảy dòng chữ đặc kín đè lên đầu hình — không ai đọc, nhất là bé lớp 5;
mà phần hình bên dưới thì lại vẽ rõ ràng, coi như hỏng oan.

CÁCH SỬA: thay bằng `title` của bài. Tên bài vốn đã là câu tóm tắt gọn (trung
bình 50 chữ) và nói đúng điều hình đang vẽ, nên hình tự đứng một mình vẫn hiểu.

NGƯỠNG 120 CHỮ: đo thật trên bản vẽ — dưới ngưỡng này tiêu đề gói trong hai dòng,
vẫn là tiêu đề; trên ngưỡng là một đoạn văn.

Chạy xong PHẢI chạy `tools/ve_lai_lop5.py` để vẽ lại — sửa params mà không vẽ lại
thì dữ liệu nói một đằng, ảnh hiện một nẻo.
"""
import json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(GOC_KHO, 'data', 'lessons')
PUBLIC = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lessons')
NGUONG = 120


def main(chi_soat=False):
    n, khong_co = 0, []
    for ten in sorted(os.listdir(DATA)):
        if not ten.startswith('DL_KSN5Q1_'):
            continue
        d = json.load(open(os.path.join(DATA, ten), encoding='utf-8'))
        doi = False
        for f in d.get('figureSpec') or []:
            ti = (f.get('params') or {}).get('title', '')
            if len(ti) <= NGUONG:
                continue
            gon = (d.get('title') or '').strip()
            if not gon:
                # Không có tên bài để mượn thì ĐỪNG tự cắt ngang câu — cắt giữa
                # chừng còn khó hiểu hơn để nguyên. Báo ra để sửa tay.
                khong_co.append((d['id'], f['id']))
                continue
            n += 1
            if chi_soat:
                print(f'  {d["id"]}#{f["id"]}  {len(ti)} → {len(gon)} chữ\n'
                      f'      {gon}')
            else:
                f['params']['title'] = gon
                doi = True
        if doi and not chi_soat:
            for thu_muc in (DATA, PUBLIC):
                with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as fh:
                    json.dump(d, fh, ensure_ascii=False, indent=1)

    print(f'{n} tiêu đề hình rút gọn' + (' (CHƯA ghi)' if chi_soat else ''))
    for i, fi in khong_co:
        print(f'  ⚠ {i}#{fi} tiêu đề dài mà bài không có tên — sửa tay')
    return n


if __name__ == '__main__':
    main('--soat' in sys.argv)
