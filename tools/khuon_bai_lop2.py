# -*- coding: utf-8 -*-
"""KHUÔN CHUNG ĐỂ VIẾT MỘT BÀI LỚP 2 — dùng cho mọi chương.

Anh em với `khuon_bai_lop4.py`, nhưng KHÔNG dùng lại được vì quyển lớp 2 khác ba chỗ:

  1. **Tám mục, không phải mười.** Lớp 2 không có "dựng mô hình" và "lắp - soi";
  2. **Số câu luyện tập không cố định.** Lớp 4 bài nào cũng đúng 9 câu; lớp 2 thì 18
     bài có 8 câu, 13 bài có 9, 2 bài có 10 — ép về một con số là phải viết thêm câu
     cho có, hoặc cắt mất câu của sách;
  3. **Luật ô nhập số 1.** Lớp 2 là quyển ĐỌC CHẬM: đáp án không phải con số thì
     BẮT BUỘC cho bấm nút (`options`), không được để bé gõ chữ. Bé 7 tuổi gõ chậm,
     sai chính tả một chữ là mất điểm oan — mà bài đang kiểm toán chứ không kiểm gõ.

Mã bài mang tiền tố `DL:KSN2.`, và `so` chỉ là số TẠM lúc viết — từ khi có lối C thì
`data/lop2/thu_tu.json` mới là chỗ quyết định bài đứng thứ mấy, và bộ dựng ĐÈ lại.
"""
from __future__ import annotations

import re as _re


def muc(ten, dong, nhip='', hinh=None):
    return {'ten': ten, 'dong': list(dong), 'hinh': list(hinh or []), 'nhip': nhip}


def bai(so, ten, dang_goc, m, cau, chuong, ten_chuong):
    return {
        'id': f'DL:KSN2.B{so:02d}', 'quyen': 'lop2', 'so': so,
        'ten': ten, 'chuong': chuong, 'tenChuong': ten_chuong,
        'dangGoc': dang_goc, 'muc': m, 'cau': cau,
    }


def lt(so, mucsao, text, loi_chua, ghi_chu=''):
    return {'id': f'C{so}', 'maSach': f'C{so}', 'so': so, 'muc': mucsao,
            'phan': 'luyenTap', 'ghiChu': ghi_chu, 'text': text,
            'loiChua': loi_chua, 'tuLuan': True}


def q_tf(so, text, dung, loi_chua):
    return {'id': f'Q{so}', 'maSach': f'C{so}', 'so': so, 'muc': 1, 'phan': 'quiz',
            'ghiChu': 'Đúng/Sai?', 'text': text, 'format': 'tf', 'tuLuan': False,
            'answerKey': {'value': dung}, 'loiChua': loi_chua,
            'solutionNarrative': loi_chua}


def q_mcq(so, text, chon, dung, loi_chua):
    return {'id': f'Q{so}', 'maSach': f'C{so}', 'so': so, 'muc': 1, 'phan': 'quiz',
            'ghiChu': '', 'text': text, 'choices': chon, 'format': 'mcq',
            'tuLuan': False, 'answerKey': {'choice': dung}, 'loiChua': loi_chua,
            'solutionNarrative': loi_chua}


TEN_MUC = {
    'mucTieu': 'MỤC TIÊU BÀI HỌC — Sau bài này con sẽ:',
    'khamPha': 'CÙNG KHÁM PHÁ',
    'viDuMau': 'LỜI GIẢI MẪU TRÌNH BÀY VỞ',
    'suKemNham': 'CHỖ HAY NHẦM',
    'luyenTap': 'LUYỆN TẬP 3 MỨC SAO',
    'quiz': 'QUIZ — CON HIỂU BÀI CHƯA?',
    'gocBoMe': 'GÓC BỐ MẸ',
}


def dung_muc(mo_bai_ten, mo_bai, muc_tieu, kham, vidu, nham, bome):
    """Tám mục của một bài lớp 2.

    Bài dùng VIDEO thì hai mục ② mở bài và ③ khám phá để RỖNG — video thay cả hai,
    bé đi thẳng từ video sang bài mẫu. Bác chốt 14-08, và video KHÔNG NHÂN VẬT.
    """
    return {
        'mucTieu': muc(TEN_MUC['mucTieu'], muc_tieu),
        'chuyenMoBai': muc(f'CHUYỆN MỞ BÀI — {mo_bai_ten}' if mo_bai_ten
                           else 'CHUYỆN MỞ BÀI', mo_bai),
        'khamPha': muc(TEN_MUC['khamPha'], kham),
        'viDuMau': muc(TEN_MUC['viDuMau'], vidu),
        'suKemNham': muc(TEN_MUC['suKemNham'], nham),
        'luyenTap': muc(TEN_MUC['luyenTap'], []),
        'quiz': muc(TEN_MUC['quiz'], ['Khoanh vào đáp án đúng (mỗi câu 1 sao ★)']),
        'gocBoMe': muc(TEN_MUC['gocBoMe'], bome),
    }


MUC_BAT_BUOC = ('mucTieu', 'chuyenMoBai', 'khamPha', 'viDuMau', 'suKemNham',
                'luyenTap', 'quiz', 'gocBoMe')

# Nấc sao theo SỐ CÂU của bài — lớp 2 không cố định 9 câu như lớp 4.
NAC_SAO = {
    8: [1, 1, 1, 2, 2, 2, 3, 3],
    9: [1, 1, 1, 2, 2, 2, 2, 3, 3],
    10: [1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
}


def soi_bai(ds, o_nhap):
    """Soi trước khi ghi — hỏng thì chưa ghi gì cả, thay vì ghi ra rồi mới đỏ."""
    loi = []
    for b in ds:
        n = b['id'][-3:]
        lt_ = [c for c in b['cau'] if c['phan'] == 'luyenTap']
        qz = [c for c in b['cau'] if c['phan'] == 'quiz']
        if not 8 <= len(lt_) <= 10:
            loi.append(f'{n}: {len(lt_)} câu luyện tập, phải trong khoảng 8 tới 10')
        elif [c['muc'] for c in lt_] != NAC_SAO[len(lt_)]:
            loi.append(f'{n}: mức sao không đúng nấc của bài {len(lt_)} câu')
        if len(qz) != 5:
            loi.append(f'{n}: {len(qz)} câu quiz, phải đúng 5')
        for m in MUC_BAT_BUOC:
            if m not in b['muc']:
                loi.append(f'{n}: thiếu mục {m}')
        for c in lt_:
            khoa = o_nhap.get(f'{b["id"]}#{c["id"]}')
            if not khoa:
                loi.append(f'{n}: câu {c["id"]} chưa có ô nhập chấm máy')
                continue
            # ⚠ LUẬT Ô NHẬP SỐ 1 — quyển đọc chậm KHÔNG được có ô gõ chữ.
            for p in (khoa.get('parts') or [khoa]):
                v = p.get('value')
                if isinstance(v, str) and not p.get('options'):
                    loi.append(f'{n}: câu {c["id"]} có ô gõ CHỮ "{v}" mà không cho '
                               f'bấm chọn — bé lớp 2 gõ chậm, sai chính tả là mất '
                               f'điểm oan')
        for c in qz:
            if c.get('format') == 'mcq' and c['answerKey']['choice'] not in c['choices']:
                loi.append(f'{n}: quiz {c["id"]} đáp án không có trong danh sách nút')
    loi += soi_so_hoc(ds)
    loi += soi_khoa_khop_loi(ds, o_nhap)
    return loi


# ═══════════════════════════════════════════════════════════════════════════
# SOI SỐ HỌC — mượn nguyên của lớp 4, xem chú thích dài ở `khuon_bai_lop4.py`
# ═══════════════════════════════════════════════════════════════════════════
_DAU = r'[+\-−×x:]'
_SO = r'\d+(?:\s\d{3})*'
_PHEP = _re.compile(
    rf'((?:{_SO}\s*{_DAU}\s*)+{_SO})\s*=\s*({_SO})(?!\s*{_DAU})(?!\s*\d)')
_TACH = _re.compile(rf'({_SO})|({_DAU})')


def _so(t: str) -> int:
    return int(t.replace(' ', ''))


def soi_so_hoc(ds) -> list[str]:
    loi = []
    for b in ds:
        van = []
        for c in b.get('cau', []):
            van += [c.get('loiChua', ''), c.get('solutionNarrative', '')]
        m = b.get('muc', {}).get('viDuMau')
        if isinstance(m, dict):
            van += m.get('dong', [])
        for t in van:
            for m2 in _PHEP.finditer(t or ''):
                if (t[:m2.start()]).rstrip()[-1:] in '+-−×x:':
                    continue
                ve, kq = m2.group(1), m2.group(2)
                so = [_so(x) for x, _ in _TACH.findall(ve) if x]
                dau = [d for _, d in _TACH.findall(ve) if d]
                if len(set(dau)) != 1:
                    continue
                d0, z = dau[0], _so(kq)
                if d0 == '+':
                    dung = sum(so) == z
                elif d0 in '-−':
                    x = so[0]
                    for y in so[1:]:
                        x -= y
                    dung = x == z
                elif d0 in '×x':
                    x = 1
                    for y in so:
                        x *= y
                    dung = x == z
                elif len(so) == 2:
                    md = _re.match(r'\s*\(?\s*dư\s+(\d+)', (t[m2.end():])[:14])
                    du = int(md.group(1)) if md else 0
                    dung = so[1] != 0 and so[0] == so[1] * z + du and du < so[1]
                else:
                    continue
                if not dung:
                    loi.append(f'{b["id"]}: phép sai — "{ve.strip()} = {kq.strip()}"')
    return loi


def soi_khoa_khop_loi(ds, o_nhap) -> list[str]:
    """Mọi giá trị SỐ của ô nhập phải nằm nguyên văn trong lời chữa.

    Phép này tìm ra 39 câu lệch ở kỳ sát hạch lớp 4 — chỗ mà đề đã viết lại còn lời
    giải thì quên. Nay soi ngay lúc viết bài, đừng để nó thành nợ.
    """
    loi = []
    for b in ds:
        for c in b.get('cau', []):
            if c['phan'] != 'luyenTap':
                continue
            k = o_nhap.get(f'{b["id"]}#{c["id"]}') or {}
            gt = ([p.get('value') for p in k['parts']] if 'parts' in k
                  else k.get('values') or [k.get('value')])
            van = (c.get('loiChua') or '').replace(' ', '')
            for v in gt:
                if isinstance(v, (int, float)) and not _re.search(
                        rf'(?<!\d){v}(?!\d)', van):
                    loi.append(f'{b["id"]} {c["id"]}: ô nhập có {v} mà lời chữa '
                               f'không nhắc tới')
    return loi
