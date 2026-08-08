# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 3 — dựng dữ liệu bài học cho phần mềm.

    python3 tools/chuan_lop2.py

Đáp án nằm ở mục "ĐÁP ÁN CHI TIẾT — GIỌNG TRÍ LONG" cuối mỗi chương, viết liền
kiểu "C1: … C2: … C3: …". Gắn lời chữa vào đúng câu, để con làm xong thì tự so —
đúng như sách dặn: "Con hãy tự làm hết sức trước rồi mới mở trang này nhé!"

Chấm máy ĐÚNG CHỖ chấm được, không ép:
  · Quiz (165 câu) — sách ghi sẵn "Quiz: C1 ĐÚNG · C2 SAI · C3 B…", toàn Đúng/Sai và
    trắc nghiệm A·B·C nên chấm máy chắc chắn đúng. Câu nào sách không ghi đáp án thì
    để bé tự chấm, KHÔNG đoán bừa.
  · Luyện tập (281 câu) — đáp án phần lớn là câu chữ ("3 trăm, 6 chục, 8 đơn vị"),
    ép thành ô nhập số là chấm oan con viết đúng. Giữ tự chấm. Bài học từ Quyển 2 lớp 5.
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
# Sách đôi khi chú thêm trong ngoặc trước dấu hai chấm: "C4 (tổng 3): 12; 21; 30".
# Mẫu cũ đòi dấu hai chấm dính ngay sau mã nên bỏ sót, câu ấy mất trắng lời giải.
R_CAU = re.compile(r'\b(C\d+)\s*(?:\([^)]*\))?\s*:\s*')

# Đáp án quiz nằm gọn một dòng: "Quiz: C1 ĐÚNG · C2 SAI (507 = 500 + 7) · C3 B · C4 A · C5 A."
R_QUIZ_DONG = re.compile(r'^Quiz\s*:\s*(.+)$')
R_QUIZ_CAU = re.compile(r'\b(C\d+)\s+(ĐÚNG|SAI|[A-D])\b\s*(?:\(([^)]*)\))?')
# Phương án trắc nghiệm trong đề: "… là: A. 38 B. 308 C. 380"
R_PA = re.compile(r'(?<![A-Za-zÀ-ỹ])([A-D])\.\s*')

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


def tach_phuong_an(text):
    """Tách "… là: A. 38 B. 308 C. 380" → (phần đề, ["A. 38", "B. 308", "C. 380"]).

    Trả về (text, []) nếu không phải câu trắc nghiệm. Giữ nguyên chữ cái ở đầu mỗi
    phương án vì sách chấm theo chữ cái ("C3 B"), và bé cũng đối chiếu theo chữ cái.
    """
    vt = [m for m in R_PA.finditer(text)]
    # phải đủ A, B liền mạch mới coi là trắc nghiệm
    if len(vt) < 2 or [m.group(1) for m in vt] != list('ABCD')[:len(vt)]:
        return text, []
    de = text[:vt[0].start()].strip().rstrip('–—-')
    pa = []
    for i, m in enumerate(vt):
        het = vt[i + 1].start() if i + 1 < len(vt) else len(text)
        pa.append(f'{m.group(1)}. {text[m.end():het].strip().rstrip(".;, ")}')
    return de, pa


def rut_dap_an_quiz(ps):
    """{số bài: {mã câu: (đáp án, giải thích)}} — đọc dòng "Quiz: C1 ĐÚNG · C2 SAI…".

    Mỗi bài có đúng một dòng như vậy, nằm ngay sau khối đáp án luyện tập của bài đó.
    Trước đây không ai đọc dòng này nên 165 câu quiz của 33 bài không có đáp án.
    """
    ra, hien = {}, None
    for t in ps:
        m = R_DAP_BAI.match(t)
        if m:
            hien = int(m.group(2)); continue
        if 'ĐÁP ÁN' in t[:40] or t.startswith(('TOÁN TƯ DUY', 'CHƯƠNG')):
            hien = None
            continue
        q = R_QUIZ_DONG.match(t)
        if q and hien is not None:
            ra[hien] = {c: (d, (g or '').strip())
                        for c, d, g in R_QUIZ_CAU.findall(q.group(1))}
            hien = None
    return ra


def dung_cau_quiz(c, dap):
    """Một câu quiz thành câu CHẤM ĐƯỢC: Đúng/Sai hoặc trắc nghiệm A·B·C.

    Không có đáp án trong sách thì trả về câu tự chấm, KHÔNG đoán bừa — chấm sai
    một câu là bé mất tin vào cả phần mềm.
    """
    de, pa = tach_phuong_an(c['text'])
    if dap is None:
        return {**c, 'text': de, 'choices': pa, 'loiChua': '', 'tuLuan': True}
    kq, giai = dap

    # `solutionNarrative` là tên trường của bộ chấm dùng chung (lớp 5). Đặt luôn ở đây
    # để AnswerInput khoe được lời giải thích của sách khi bé chọn đúng, khỏi phải sửa
    # component đang dùng cho cả hai lớp.
    if kq in ('ĐÚNG', 'SAI'):
        return {**c, 'text': de, 'format': 'tf', 'tuLuan': False,
                'answerKey': {'value': kq == 'ĐÚNG'},
                'loiChua': giai or f'Đáp án: {kq}',
                'solutionNarrative': giai}

    # trắc nghiệm: đối chiếu chữ cái với phương án đã tách từ đề
    chon = next((p for p in pa if p.startswith(f'{kq}.')), None)
    if chon is None:                       # đề không liệt kê được phương án → tự chấm
        return {**c, 'text': de, 'choices': pa, 'tuLuan': True,
                'loiChua': f'Đáp án: {kq}' + (f' ({giai})' if giai else '')}
    return {**c, 'text': de, 'format': 'mcq', 'choices': pa, 'tuLuan': False,
            'answerKey': {'choice': chon},
            'loiChua': giai or f'Đáp án: {chon}',
            'solutionNarrative': giai}


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
        # Mọi tiêu đề đáp án KHÁC (Ô1 ĐÁP ÁN ÔN TẬP 1 · Ô1B ĐÁP ÁN ĐỀ B · ĐÁP ÁN BA ẢI ·
        # ★ ĐÁP ÁN ẢI 1) đều phải ĐÓNG bài đang mở. Trước đây chúng không khớp mẫu tiêu đề
        # bài và cũng không bị chặn, nên trôi vào bài cuối chương; mà ôn tập cũng đánh số
        # C1, C2… nên ĐÈ THẲNG lên đáp án thật của bài. Tám bài cuối chương đều sai.
        if 'ĐÁP ÁN' in t[:40]:
            hien = None
            continue
        if t.startswith(('Con hãy tự làm', 'TOÁN TƯ DUY', 'CHƯƠNG')):
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
    ps = doan_van()
    dap = rut_dap_an(ps)
    dap_quiz = rut_dap_an_quiz(ps)
    os.makedirs(RA_DIR, exist_ok=True)
    os.makedirs(RA_DATA, exist_ok=True)

    idx, co_dap, cham_may = [], 0, 0
    for b in B['bai']:
        d = dap.get(b['so'], {})
        dq = dap_quiz.get(b['so'], {})
        cau = []
        for c in b['cau']:
            if c['phan'] == 'quiz':
                cau.append(dung_cau_quiz(c, dq.get(c.get('maSach', c['id']))))
                if cau[-1].get('answerKey'):
                    cham_may += 1
                    co_dap += 1
                continue
            loi = d.get(c.get('maSach', c['id']), '')
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
        # Tách hai con số: trang chính ghi "n câu luyện tập" nên gộp cả quiz vào là
        # nói sai với bé — quiz là phần tự kiểm cuối bài, không phải bài tập.
        idx.append({'id': bai['id'], 'so': b['so'], 'ten': b['ten'],
                    'chuong': b['chuong'], 'tenChuong': bai['tenChuong'],
                    'soCau': sum(1 for c in cau if c['phan'] == 'luyenTap'),
                    'soQuiz': sum(1 for c in cau if c['phan'] == 'quiz')})

    for thu_muc in (RA_DIR, RA_DATA):
        with open(os.path.join(thu_muc, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump(idx, f, ensure_ascii=False, indent=1)

    tong = sum(len(b['cau']) for b in B['bai'])
    print(f'đã ghi {len(idx)} bài vào {RA_DIR}')
    print(f"  {tong} câu · có lời chữa {co_dap} ({co_dap * 100 // tong}%) · chấm máy {cham_may}")


if __name__ == '__main__':
    main()
