# -*- coding: utf-8 -*-
"""KHUÔN CHUNG ĐỂ VIẾT MỘT BÀI LỚP 4 — dùng cho MỌI chương.

Tách ra từ `day_so_lop4.py` khi bắt đầu chương 3. Hai chương cùng một khuôn bài,
nên nếu mỗi chương giữ một bản sao thì sớm muộn hai bản lệch nhau: sửa tên mục ở
bên này, bên kia vẫn tên cũ — và **không cổng nào bắt được**, vì cả hai đều dựng ra
bài hợp lệ. Đúng bài học của `hinh_ve.json`: một nguồn cho hai nơi vẽ.

Ở đây CHỈ có khuôn rỗng. Nội dung bài nằm ở tệp của từng chương.
"""
from __future__ import annotations


def muc(ten, dong, nhip='', hinh=None):
    return {'ten': ten, 'dong': list(dong), 'hinh': list(hinh or []), 'nhip': nhip}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, chuong, ten_chuong):
    """Một bài hoàn chỉnh.

    ⚠ `so` ở đây chỉ là SỐ TẠM lúc viết. Từ 14-08 (lối C) số bài hiển thị do
    `data/lop4/thu_tu.json` quyết định, và bộ dựng ĐÈ lại trường này theo vị trí
    trong lời khai. Đừng dựa vào nó để suy ra bài đứng thứ mấy.

    `ten` là tên TRẦN, không có tiền tố "Bài n ·" — `khuon_chung` tự ghép khi dựng.
    Ghép sẵn ở đây thì bản dựng ra "Bài 13 · Bài 13 · DÃY SỐ…".
    """
    return {
        'id': f'DL:KSN4.B{so:02d}', 'quyen': 'KSN4', 'so': so,
        'ten': ten, 'chuong': chuong, 'tenChuong': ten_chuong,
        'dangGoc': dang_goc, 'hatMam': hat_mam, 'ganDuoi': gan_duoi,
        'muc': m, 'cau': cau,
    }


def lt(so, mucsao, text, loi_chua, ghi_chu=''):
    """Một câu luyện tập. `tuLuan: True` nghĩa là có lời giải chữ; ô nhập chấm máy
    khai riêng ở `lop4_dapan_o.json`."""
    return {'id': f'C{so}', 'maSach': f'C{so}', 'so': so, 'muc': mucsao,
            'phan': 'luyenTap', 'ghiChu': ghi_chu, 'text': text,
            'loiChua': loi_chua, 'tuLuan': True}


def q_tf(so, text, dung, loi_chua, ke=''):
    return {'id': f'Q{so}', 'maSach': f'C{so}', 'so': so, 'muc': 1, 'phan': 'quiz',
            'ghiChu': 'Đúng/Sai?', 'text': text, 'format': 'tf', 'tuLuan': False,
            'answerKey': {'value': dung}, 'loiChua': loi_chua,
            'solutionNarrative': ke or loi_chua}


def q_mcq(so, text, chon, dung, loi_chua, ke=''):
    return {'id': f'Q{so}', 'maSach': f'C{so}', 'so': so, 'muc': 1, 'phan': 'quiz',
            'ghiChu': '', 'text': text, 'choices': chon, 'format': 'mcq',
            'tuLuan': False, 'answerKey': {'choice': dung}, 'loiChua': loi_chua,
            'solutionNarrative': ke or loi_chua}


TEN_MUC = {
    'mucTieu': 'MỤC TIÊU BÀI HỌC — Sau bài này con sẽ:',
    'dichMoHinh': 'PHÂN TÍCH & DỰNG MÔ HÌNH — bàn vẽ của kỹ sư',
    'khamPha': 'KHÁM PHÁ CÙNG SU KEM — vào không gian toán',
    'lapSoi': 'LẮP VỀ CUỘC SỐNG & SOI',
    'viDuMau': 'LỜI GIẢI MẪU TRÌNH BÀY VỞ',
    # Không tên ai — bác chốt bỏ nhân vật 14-08. `khuon_chung` suy dòng dấu hiệu
    # từ chính tiêu đề này, nên đổi ở đây là dòng ấy tự trống theo.
    'suKemNham': 'CHỖ HAY NHẦM',
    'luyenTap': 'LUYỆN TẬP 3 MỨC SAO',
    'quiz': 'QUIZ — CON HIỂU BÀI CHƯA?',
    'gocBoMe': 'GÓC BỐ MẸ',
}


def dung_muc(mo_bai_ten, mo_bai, muc_tieu, dich, kham, lap, vidu, nham, bome):
    """Mười mục của một bài.

    Bài dùng VIDEO thay mở bài và bài giảng thì bốn mục ②③④⑤ để RỖNG — bộ dựng
    thấy rỗng thì không sinh màn nào, bé đi thẳng từ video sang bài mẫu. Đây là chủ
    ý (bác chốt 14-08), và `video_toan.test.mjs` canh đúng điều đó.
    """
    return {
        'mucTieu': muc(TEN_MUC['mucTieu'], muc_tieu),
        'chuyenMoBai': muc(f'CHUYỆN MỞ BÀI — {mo_bai_ten}', mo_bai),
        'dichMoHinh': muc(TEN_MUC['dichMoHinh'], dich, 'NHỊP 1, DỊCH'),
        'khamPha': muc(TEN_MUC['khamPha'], kham, 'NHỊP 2, GIẢI'),
        'lapSoi': muc(TEN_MUC['lapSoi'], lap, 'NHỊP 3, LẮP + NHỊP 4, SOI'),
        'viDuMau': muc(TEN_MUC['viDuMau'], vidu),
        'suKemNham': muc(TEN_MUC['suKemNham'], nham),
        'luyenTap': muc(TEN_MUC['luyenTap'], []),
        'quiz': muc(TEN_MUC['quiz'], ['Khoanh vào đáp án đúng (mỗi câu 1 sao ★)']),
        'gocBoMe': muc(TEN_MUC['gocBoMe'], bome),
    }


MUC_BAT_BUOC = ('mucTieu', 'chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi',
                'viDuMau', 'suKemNham', 'luyenTap', 'quiz', 'gocBoMe')

# Nấc sao của chín câu luyện tập. Cố định cho mọi bài để bé đi quen một nhịp.
NAC_SAO = [1, 1, 1, 2, 2, 2, 2, 3, 3]


def soi_bai(ds, o_nhap):
    """Soi chung cho mọi chương — mấy luật này đều đã có cổng canh bên `web/test`.
    Soi ở đây để hỏng thì chưa ghi gì cả, thay vì ghi ra rồi mới đỏ."""
    loi = []
    for b in ds:
        n = b['so']
        lt_ = [c for c in b['cau'] if c['phan'] == 'luyenTap']
        qz = [c for c in b['cau'] if c['phan'] == 'quiz']
        if len(lt_) != 9:
            loi.append(f'B{n}: {len(lt_)} câu luyện tập, phải đúng 9')
        if len(qz) != 5:
            loi.append(f'B{n}: {len(qz)} câu quiz, phải đúng 5')
        if [c['muc'] for c in lt_] != NAC_SAO:
            loi.append(f'B{n}: mức sao luyện tập không đúng 1,1,1,2,2,2,2,3,3')
        for m in MUC_BAT_BUOC:
            if m not in b['muc']:
                loi.append(f'B{n}: thiếu mục {m}')
        for c in lt_:
            if f'{b["id"]}#{c["id"]}' not in o_nhap:
                loi.append(f'B{n}: câu {c["id"]} chưa có ô nhập chấm máy')
        # Đáp án bấm chọn phải nằm trong danh sách nút (luật 3 của luật ô nhập)
        for c in qz:
            if c.get('format') == 'mcq' and c['answerKey']['choice'] not in c['choices']:
                loi.append(f'B{n}: quiz {c["id"]} đáp án không có trong danh sách nút')
    return loi
