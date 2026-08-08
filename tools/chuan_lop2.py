# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 3 — dựng dữ liệu bài học cho phần mềm.

    python3 tools/chuan_lop2.py

Đáp án nằm ở mục "ĐÁP ÁN CHI TIẾT — GIỌNG TRÍ LONG" cuối mỗi chương, viết liền
kiểu "C1: … C2: … C3: …". Gắn lời chữa vào đúng câu, để con làm xong thì tự so —
đúng như sách dặn: "Con hãy tự làm hết sức trước rồi mới mở trang này nhé!"

Không cố máy chấm: đáp án lớp 2 phần lớn là câu chữ ("3 trăm, 6 chục, 8 đơn vị"),
ép thành ô nhập số là chấm oan con viết đúng. Bài học từ Quyển 2 lớp 5.
"""
import json, os, re, zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON_DOCX = os.path.join(GOC_KHO, 'docs', 'Toan_Tu_Duy_Lop2_Ban_hoan_chinh.docx')
NGUON = os.path.join(GOC_KHO, 'data', 'lop2_dehieu.json')
RA_DIR = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop2')
RA_DATA = os.path.join(GOC_KHO, 'data', 'lop2')

R_DAP_BAI = re.compile(r'^B(\d+)\s+ĐÁP ÁN BÀI (\d+)')
R_CAU = re.compile(r'\b(C\d+)\s*:\s*')

TEN_CHUONG = {
    1: 'Vương quốc Số', 2: 'Bé là vua đếm', 3: 'Dãy số kỳ diệu',
    4: 'Siêu nhân tính nhanh', 5: 'Chuyện toán lời văn', 6: 'Thám tử tí hon',
    7: 'Vương quốc hình học', 8: 'Toán trong cuộc sống',
}


def doan_van():
    z = zipfile.ZipFile(NGUON_DOCX)
    root = ET.fromstring(z.read('word/document.xml'))
    ra = []
    for p in root.iter(W + 'p'):
        t = ' '.join(''.join(n.text or '' for n in p.iter(W + 't')).split())
        if t:
            ra.append(t)
    return ra


def rut_dap_an(ps):
    """{số bài: {mã câu: lời chữa}} — gộp mọi dòng đáp án của bài rồi tách theo Cn."""
    theo_bai, hien = {}, None
    for t in ps:
        m = R_DAP_BAI.match(t)
        if m:
            hien = int(m.group(2)); theo_bai.setdefault(hien, [])
            continue
        if hien is None:
            continue
        if t.startswith(('ĐÁP ÁN', 'Con hãy tự làm', 'TOÁN TƯ DUY', 'CHƯƠNG')):
            hien = None if t.startswith(('TOÁN TƯ DUY', 'CHƯƠNG')) else hien
            continue
        if R_CAU.search(t):
            theo_bai[hien].append(t)

    ra = {}
    for so, dong in theo_bai.items():
        gop = ' '.join(dong)
        vt = [(m.group(1), m.start(), m.end()) for m in R_CAU.finditer(gop)]
        d = {}
        for i, (ma, _, het) in enumerate(vt):
            ket = vt[i + 1][1] if i + 1 < len(vt) else len(gop)
            loi = gop[het:ket].strip().rstrip('.;, ')
            if loi:
                d[ma] = loi
        if d:
            ra[so] = d
    return ra


def main():
    B = json.load(open(NGUON, encoding='utf-8'))
    dap = rut_dap_an(doan_van())
    os.makedirs(RA_DIR, exist_ok=True)
    os.makedirs(RA_DATA, exist_ok=True)

    idx, co_dap = [], 0
    for b in B['bai']:
        d = dap.get(b['so'], {})
        cau = []
        for c in b['cau']:
            loi = d.get(c['id'], '')
            if loi:
                co_dap += 1
            cau.append({**c, 'loiChua': loi, 'tuLuan': True})

        bai = {
            'id': f'DL:KSN2.B{b["so"]:02d}',
            'quyen': 'lop2',
            'so': b['so'],
            'ten': b['ten'],
            'chuong': b['chuong'],
            'tenChuong': TEN_CHUONG.get(b['chuong'], ''),
            'dangGoc': b['dangGoc'],
            'muc': b['muc'],
            'cau': cau,
        }
        ten = f'DL_KSN2_B{b["so"]:02d}.json'
        for thu_muc in (RA_DIR, RA_DATA):
            with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as f:
                json.dump(bai, f, ensure_ascii=False, indent=1)
        idx.append({'id': bai['id'], 'so': b['so'], 'ten': b['ten'],
                    'chuong': b['chuong'], 'tenChuong': bai['tenChuong'],
                    'soCau': len(cau)})

    for thu_muc in (RA_DIR, RA_DATA):
        with open(os.path.join(thu_muc, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump(idx, f, ensure_ascii=False, indent=1)

    tong = sum(len(b['cau']) for b in B['bai'])
    print(f'đã ghi {len(idx)} bài vào {RA_DIR}')
    print(f'  {tong} câu · có lời chữa {co_dap} ({co_dap * 100 // tong}%)')


if __name__ == '__main__':
    main()
