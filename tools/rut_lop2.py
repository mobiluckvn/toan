# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 1 — trích sách thành JSON thô, GIỮ NGUYÊN CHỮ.

    python3 tools/rut_lop2.py

Bản trích này là mốc bất biến. Sách lớp 2 sẽ được VIẾT LẠI cho dễ hiểu ở bước sau,
nên càng phải giữ bản gốc: mọi câu chữ đã đổi đều phải đối chiếu được với sách, và
nếu viết lại hỏng nghĩa thì còn đường lùi.

Mỗi bài có 8 mục cố định (①…⑧). Bốn mục đầu và ⑥⑦ là CON đọc; ⑧ Góc bố mẹ là người
lớn đọc — phân biệt được điều này mới biết chỗ nào cần viết lại cho dễ.
"""
import json, os, re, zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'docs', 'Toan_Tu_Duy_Lop2_Ban_hoan_chinh.docx')
RA = os.path.join(GOC_KHO, 'data', 'lop2_tho.json')

# Tiêu đề bài THẬT viết IN HOA; dòng mục lục liệt kê nhiều bài trên một dòng thì không.
R_BAI = re.compile(r'^Bài (\d+)\s*·\s*([A-ZÀ-Ỹ0-9][^a-zà-ỹ]*(?:[^·]|$).*)$')
R_CHUONG = re.compile(r'^CHƯƠNG (\d+)$')
R_MUC = re.compile(r'^([①②③④⑤⑥⑦⑧])\s*(.*)$')
R_MUC_SAO = re.compile(r'^(★+)\s*MỨC (\d)')
# Luyện tập ghi "Câu 1. …", quiz ghi "Câu 1 (Đúng/Sai?): …" hoặc "Câu 3: …".
# Mẫu cũ chỉ nhận dấu chấm nên 165 câu quiz của 33 bài không hề được tách ra —
# chúng nằm lẫn trong phần chữ, không chấm được, cũng không đếm được.
R_CAU = re.compile(r'^Câu (\d+)\s*(?:\(([^)]*)\))?\s*[.:]\s*(.+)$')
R_DANG = re.compile(r'^Dạng gốc:\s*(.+)$')

# Bài được cắt từ tiêu đề bài này tới tiêu đề bài KẾ TIẾP. Giữa hai bài ấy sách còn
# chèn ôn tập, đáp án cả chương, tiêu đề chương sau — chúng rơi hết vào mục đang mở,
# tức luôn là ⑧ Góc bố mẹ. Đây là mốc để DỪNG gom vào bài.
# Không vứt phần dừng ấy đi: nó chính là chữ của 8 bài ôn tập và 3 ải, cất vào `sauBai`.
R_KET = re.compile(r'^(?:CHƯƠNG \d+|ÔN TẬP \d+|ĐÁP ÁN|Ải \d+|BẢNG SƯU TẬP'
                   r'|TOÁN TƯ DUY LỚP 2|LỜI (?:NHẮN|KẾT))\b')

TEN_MUC = {
    '①': 'mucTieu', '②': 'chuyenMoBai', '③': 'khamPha', '④': 'viDuMau',
    '⑤': 'suKemNham', '⑥': 'luyenTap', '⑦': 'quiz', '⑧': 'gocBoMe',
}
# Mục nào CON đọc — chỉ những mục này mới cần viết lại cho dễ hiểu
CON_DOC = {'mucTieu', 'chuyenMoBai', 'khamPha', 'viDuMau', 'suKemNham', 'luyenTap', 'quiz'}


def doan_van(duong_dan):
    z = zipfile.ZipFile(duong_dan)
    root = ET.fromstring(z.read('word/document.xml'))
    ra = []
    for p in root.iter(W + 'p'):
        t = ' '.join(''.join(n.text or '' for n in p.iter(W + 't')).split())
        if t:
            ra.append(t)
    return ra


def la_tieu_de_bai(t):
    """Tiêu đề bài thật: 'Bài 7 · TRUY TÌM CHỮ SỐ 5 TRỐN Ở ĐÂU' — phần tên IN HOA.
    Dòng mục lục ('Bài 6 · Đếm số… Bài 7 · Truy tìm…') có chữ thường và nhiều 'Bài'."""
    m = re.match(r'^Bài (\d+)\s*·\s*(.+)$', t)
    if not m or t.count('Bài ') > 1:
        return None
    ten = m.group(2).strip()
    chu_cai = [c for c in ten if c.isalpha()]
    if not chu_cai or sum(1 for c in chu_cai if c.isupper()) / len(chu_cai) < 0.8:
        return None
    return int(m.group(1)), ten


def main():
    ps = doan_van(NGUON)

    moc = []
    for i, t in enumerate(ps):
        b = la_tieu_de_bai(t)
        if b:
            moc.append((i, b[0], b[1]))
    moc.append((len(ps), None, None))

    chuong_tai = {}
    ch = 0
    for i, t in enumerate(ps):
        m = R_CHUONG.match(t)
        if m:
            ch = int(m.group(1))
        chuong_tai[i] = ch

    bai = []
    for k in range(len(moc) - 1):
        i, so, ten = moc[k]
        j = moc[k + 1][0]
        khuc = ps[i + 1:j]

        muc, hien, dang, mucsao = {}, None, '', 1
        cau, sau_bai, het = [], [], False
        for t in khuc:
            # từ mốc kết thúc trở đi là phần KHÔNG thuộc bài này nữa
            if het or R_KET.match(t):
                het = True
                sau_bai.append(t)
                continue
            d = R_DANG.match(t)
            if d:
                dang = d.group(1); continue
            m = R_MUC.match(t)
            if m:
                hien = TEN_MUC.get(m.group(1))
                muc.setdefault(hien, {'ten': m.group(2).strip(), 'dong': []})
                continue
            s = R_MUC_SAO.match(t)
            if s:
                mucsao = int(s.group(2)); continue
            c = R_CAU.match(t)
            if c and hien in ('luyenTap', 'quiz'):
                # Sách đánh số lại từ đầu ở mỗi phần ("Luyện tập — C1: …" và
                # "Quiz: C1 ĐÚNG"), nên `maSach` giữ đúng mã ấy để tra đáp án.
                # Còn `id` phải DUY NHẤT trong một bài, vì phần mềm dùng nó làm khoá.
                stt = sum(1 for x in cau if x['phan'] == hien) + 1
                # Mức sao (★ MỨC 1/2/3) chỉ có ở phần luyện tập. Quiz đứng SAU nên
                # thừa hưởng nhầm "★★★ MỨC 3" của luyện tập, thành ra câu quiz nào
                # cũng hiện 3 sao như thể khó nhất bài.
                cau.append({'id': ('Q' if hien == 'quiz' else 'C') + str(stt),
                            'maSach': f'C{stt}', 'so': int(c.group(1)),
                            'muc': 1 if hien == 'quiz' else mucsao,
                            'phan': hien, 'ghiChu': (c.group(2) or '').strip(),
                            'text': c.group(3)})
                continue
            if hien:
                muc[hien]['dong'].append(t)

        bai.append({
            'so': so, 'ten': ten, 'chuong': chuong_tai.get(i, 0),
            'dangGoc': dang, 'muc': muc, 'cau': cau, 'sauBai': sau_bai,
        })

    ban = {'nguon': os.path.basename(NGUON), 'soDoan': len(ps),
           'conDoc': sorted(CON_DOC), 'bai': bai}
    os.makedirs(os.path.dirname(RA), exist_ok=True)
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(ban, f, ensure_ascii=False, indent=1)

    print(f'đã ghi {RA}')
    print(f'  {len(bai)} bài · {sum(len(b["cau"]) for b in bai)} câu hỏi'
          f' · {len({b["chuong"] for b in bai})} chương')


if __name__ == '__main__':
    main()
