# -*- coding: utf-8 -*-
"""
BƯỚC 5a — trích các BẢNG CHIẾN THUẬT của Quyển 2 thành figureSpec.

    python3 tools/rut_so_do_q2.py

Trong sách, mỗi chỗ cần sơ đồ là một mốc "TÌNH HUỐNG" rồi tới một BẢNG HAI CỘT:
tiêu đề, sau đó từng cặp (nhãn · mô tả). Cấu trúc rất đều nên vẽ lại được bằng máy,
không phải mô tả tay từng cái.

Vì sao vẽ lại chứ không dùng 48 ảnh có sẵn: ảnh bitmap lệch bảng màu vừa đồng bộ
theo icon, thiếu mất 49 chỗ, và sửa nội dung sau này thì không vẽ lại được. Đây
đúng bài học của Quyển 1 — 672 hình sinh bằng máy nên đổi bảng màu chỉ mất một lệnh.
"""
import json, os, re, zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'docs', 'KSN5_Q2_TRON_QUYEN_Mua_Giai_Vo_Dich.docx')
RA = os.path.join(GOC_KHO, 'data', 'quyen2_sodo.json')

MOC = 'TÌNH HUỐNG'


def chu(el):
    return ' '.join(''.join(t.text or '' for t in el.iter(W + 't')).split())


def main():
    """
    Mỗi sơ đồ là một BẢNG HAI CỘT mà ô đầu tiên ghi đúng chữ "TÌNH HUỐNG":

        | TÌNH HUỐNG        | BẢNG CHIẾN THUẬT — BỐN KIỂU ĐỀ THƯỜNG GẶP |
        | Đề một câu hỏi rõ | Gạch số + đơn vị, gọi tên dạng, xong…      |
        | …                 | …                                          |

    Lúc đầu tôi tưởng "TÌNH HUỐNG" là một đoạn văn đứng trước bảng nên đi tìm ở cấp
    thân tài liệu — ra 0 kết quả, vì nó nằm NGAY TRONG ô đầu của chính bảng ấy.
    """
    z = zipfile.ZipFile(NGUON)
    body = ET.fromstring(z.read('word/document.xml')).find(W + 'body')

    # Bảng LỒNG NHAU: tb.iter('tr') gom cả hàng của bảng con, nên hàng "TÌNH HUỐNG"
    # thường không phải rows[0] của bảng ngoài. Duyệt theo HÀNG rồi lấy các hàng
    # ANH EM ngay sau nó — cách này không phụ thuộc bảng lồng mấy tầng.
    cha = {}
    for p_ in body.iter():
        for c in p_:
            cha[c] = p_

    # Duyệt theo THỨ TỰ TÀI LIỆU để biết mỗi sơ đồ thuộc khối nào — không có thông
    # tin này thì 53 sơ đồ chỉ là một đống ảnh rời, không gắn được vào bài.
    import re as _re
    R_KHOI = _re.compile(r'^(VÒNG ĐẤU|ĐỀ TRỘN|KỲ THI THỬ) (\d+)$')
    R_MAN = _re.compile(r'^MÀN (\d)')
    MA = {'VÒNG ĐẤU': 'V', 'ĐỀ TRỘN': 'T', 'KỲ THI THỬ': 'K'}
    khoi_hien, man_hien = None, 0
    thu_tu = {}
    for el in body.iter():
        if el.tag == W + 'p':
            t = chu(el)
            m = R_KHOI.match(t)
            if m:
                khoi_hien = f'DR:KSN5Q2.{MA[m.group(1)]}{int(m.group(2)):02d}'
                man_hien = 0
            elif R_MAN.match(t):
                man_hien = int(R_MAN.match(t).group(1))
        elif el.tag == W + 'tr':
            thu_tu[id(el)] = (khoi_hien, man_hien)

    so_do = []
    for tr in body.iter(W + 'tr'):
        o = list(tr.findall(W + 'tc'))
        if len(o) != 2 or chu(o[0]) != MOC:
            continue
        bang = cha.get(tr)
        if bang is None:
            continue
        anh_em = list(bang.findall(W + 'tr'))
        if tr not in anh_em:
            continue

        tieu_de = chu(o[1]) or 'BẢNG CHIẾN THUẬT'
        hang = []
        for r in anh_em[anh_em.index(tr) + 1:]:
            c = list(r.findall(W + 'tc'))
            if len(c) < 2:
                break
            nhan, mo = chu(c[0]), chu(c[1])
            if nhan or mo:
                hang.append([nhan, mo])
        if hang:
            kh, mn = thu_tu.get(id(tr), (None, 0))
            so_do.append({'tieuDe': tieu_de, 'hang': hang, 'khoi': kh, 'man': mn})

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(so_do, f, ensure_ascii=False, indent=1)

    from collections import Counter
    print(f'đã ghi {len(so_do)} sơ đồ vào {RA}')
    print('  số hàng mỗi sơ đồ:', dict(sorted(Counter(len(s['hang']) for s in so_do).items())))
    print('  ví dụ:', so_do[0]['tieuDe'][:66] if so_do else '—')


if __name__ == '__main__':
    main()
