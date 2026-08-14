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
    # Tính lại mọi phép viết trong lời chữa — xem `soi_so_hoc` cuối tệp.
    loi += soi_so_hoc(ds)
    return loi


# ═══════════════════════════════════════════════════════════════════════════
# SOI SỐ HỌC TRONG LỜI CHỮA
# ═══════════════════════════════════════════════════════════════════════════
# Cháu đã viết hỏng hai câu ở chương 6 và chương 7 — cả hai là bài không có đáp số
# tự nhiên, và lời chữa thành một đoạn mò mẫm. Cổng không bắt được, vì với máy thì
# một chuỗi chữ nào cũng hợp lệ.
#
# Phép dưới đây không hiểu bài toán, nhưng nó TÍNH LẠI được mọi phép tính viết ra
# trong lời chữa. Người viết sai một phép cộng là đỏ ngay. Đó là phần lớn lỗi số học
# mà mắt người đọc lướt sẽ bỏ qua.
import re as _re

# ⚠ BẢN ĐẦU CỦA MẪU NÀY BÁO 130 LỖI GIẢ. Hai chỗ hỏng, và cả hai đều khiến nó đọc
# CỤT con số:
#   · `(?![\d,.])` ở cuối chối cả DẤU CHẤM CUỐI CÂU, nên "= 4 050." lùi thành "= 4";
#   · nó chấm cả mắt xích giữa một chuỗi dài, nên "7 × 64 = 7 × 60 + 7 × 4" bị đọc
#     thành "7 × 64 = 7".
# Suýt nữa cháu đi sửa 130 dòng nội dung ĐÚNG cho vừa lòng cái cổng sai. Nay mẫu chỉ
# bắt phép ĐỨNG MỘT MÌNH: hai bên không được dính thêm dấu phép nào.
# ⚠ BẢN ĐẦU CỦA MẪU NÀY BÁO 130 LỖI GIẢ, rồi bản thứ hai soi được ĐÚNG 0 PHÉP.
# Hai kiểu hỏng ngược nhau, và kiểu thứ hai nguy hiểm hơn nhiều: cổng xanh mà chẳng
# kiểm gì cả — nhìn từ ngoài giống hệt cổng đang canh tốt.
#
#   · bản 1: `(?![\d,.])` ở cuối chối cả DẤU CHẤM CUỐI CÂU, nên "= 4 050." lùi thành
#     "= 4"; và nó chấm cả mắt xích giữa chuỗi dài "7 × 64 = 7 × 60 + 7 × 4";
#   · bản 2: escape bị nhân đôi qua nhiều lớp nên `\d` thành dấu gạch chéo rồi chữ d.
#
# Bài học: sau khi sửa một cổng, phải ĐẾM xem nó soi được bao nhiêu, rồi PHÁ THỬ.
# "Không thấy lỗi" và "không tìm gì" trông y hệt nhau.
_DAU = r'[+\-−×x:]'
_SO = r'\d+(?:\s\d{3})*'          # "1 989" và "1989" là một số
# Bắt CẢ CHUỖI vế trái: "4 + 6 + 8 = 18" phải soi nguyên chuỗi, không soi mẩu cuối.
_PHEP = _re.compile(
    rf'((?:{_SO}\s*{_DAU}\s*)+{_SO})\s*=\s*({_SO})(?!\s*{_DAU})(?!\s*\d)')
_TACH = _re.compile(rf'({_SO})|({_DAU})')


def _so(t: str) -> int:
    """"1 989" và "1989" là một số. Dấu cách hàng nghìn là cách VIẾT, không phải phép."""
    return int(t.replace(' ', ''))


def soi_so_hoc(ds) -> list[str]:
    """Tính lại mọi phép `a ⊕ b = c` viết trong lời chữa và lời giải mẫu.

    ── BA LẦN VIẾT HỎNG, GHI LẠI ĐỂ NGƯỜI SAU KHỎI ĐI LẠI ──
    1. Bản đầu báo **130 lỗi giả**: `(?![\\d,.])` chối cả dấu chấm cuối câu nên
       "= 4 050." lùi thành "= 4". Suýt nữa đi sửa 130 dòng nội dung ĐÚNG.
    2. Bản hai soi được **đúng 0 phép** — escape bị nhân đôi nên `\\d` thành dấu gạch
       chéo rồi chữ d. Cổng xanh mà chẳng kiểm gì; nhìn từ ngoài giống hệt cổng tốt.
    3. Bản ba **bỏ qua quá tay**: nhảy cả chuỗi nhiều hạng, và nhảy luôn phép đứng
       sau dấu bằng ("Tổng = 25 × 4 = 100").

    Bài học: sửa cổng xong phải ĐẾM xem nó soi được bao nhiêu, rồi PHÁ THỬ từng loại.
    "Không thấy lỗi" và "không tìm gì" trông y hệt nhau.

    ── CHỖ CỐ Ý KHÔNG SOI ──
    Chuỗi TRỘN dấu ("2 + 3 × 4") bỏ qua, vì thứ tự phép dễ hiểu nhầm, mà soi nhầm
    còn tệ hơn không soi: người ta sẽ sửa nội dung đúng cho vừa lòng cái cổng.
    """
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
                # Nối tiếp một phép khác thì bỏ — nhưng đứng sau dấu BẰNG thì vẫn soi.
                truoc = (t[:m2.start()]).rstrip()
                if truoc[-1:] in '+-−×x:':
                    continue
                ve, kq = m2.group(1), m2.group(2)
                so = [_so(x) for x, _ in _TACH.findall(ve) if x]
                dau = [d for _, d in _TACH.findall(ve) if d]
                if len(set(dau)) != 1:
                    continue                       # chuỗi trộn dấu — cố ý bỏ qua
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
                    # `a : b = c` nghĩa là a = b × c. Chương 3 đầy phép chia CÓ DƯ
                    # viết "23 : 5 = 4 (dư 3)" — đọc luôn số dư, và tiện thể canh
                    # luật số dư phải nhỏ hơn số chia (chính là bài B11 dạy).
                    md = _re.match(r'\s*\(?\s*dư\s+(\d+)', (t[m2.end():])[:14])
                    du = int(md.group(1)) if md else 0
                    dung = so[1] != 0 and so[0] == so[1] * z + du and du < so[1]
                else:
                    continue                       # chia nhiều tầng — bỏ qua
                if not dung:
                    loi.append(f'{b["id"]}: phép sai — "{ve.strip()} = {kq.strip()}"')
    return loi
