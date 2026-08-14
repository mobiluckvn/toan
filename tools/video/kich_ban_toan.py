# -*- coding: utf-8 -*-
"""KỊCH BẢN VIDEO MÔN TOÁN — viết tay, ngắn, đi thẳng vào một dãy số cụ thể.

Bác xem bản đầu rồi bảo **rất không ổn**, và chỉ đúng ba chỗ:

  1. MỞ BÀI QUÁ NHIỀU. Bản đầu đọc trọn phần "chuyện mở bài" của giáo án — một câu
     chuyện về bạn Mai và cậu giao báo, dài 300 chữ, trước khi tới được khái niệm.
     Nay BỎ HẲN chuyện dẫn: video mở ra là vào ngay dãy số.
  2. PHẢI ĐƠN GIẢN TỚI MỨC LỚP 3 CŨNG HIỂU. Nói thẳng: dãy số là gì, thứ tự là gì,
     giá trị là gì — và bám vào MỘT dãy cụ thể suốt cả video.
  3. LỜI ĐỌC CÒN KÝ TỰ ĐẶC BIỆT. Đo lại bản đầu: 40 dấu hai chấm, 11 mũi tên `→`,
     42 dấu ngoặc, thêm `…` `?` `!` `✓`. Máy đọc chúng thành khoảng lặng hoặc đọc
     sai. Nay MỌI THỨ chuyển thành chữ, kể cả CON SỐ.

── VÌ SAO KHÔNG SINH TỰ ĐỘNG TỪ BÀI HỌC NỮA ──
Bản đầu lấy thẳng chữ trong giáo án làm lời đọc. Sai từ gốc: giáo án viết cho MẮT
người lớn đọc — có chuyện dẫn, có câu dài, có ngoặc và mũi tên. Cắt gọt bao nhiêu
cũng không thành lời giảng cho bé nghe.

Nên kịch bản video nay VIẾT TAY, mỗi bài một bản, mỗi câu một ý, không câu nào dài
quá một hơi đọc. Có cổng đếm.

── CON SỐ ĐỌC THÀNH CHỮ ──
Bác dặn "các thông tin cần chuyển thành chữ hết". Chữ HIỆN LÊN màn hình vẫn là số
(bé nhìn số dễ hơn nhìn chữ), nhưng chữ ĐEM ĐỌC thì "15" thành "mười lăm". Không
làm thế thì đọc số có dấu cách kiểu "1 275" ra thành "một, hai trăm bảy mươi lăm".
"""
from __future__ import annotations

import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent.parent
NGUON = GOC / 'data' / 'lop4'

# Vỏ nhân vật của quyển, cộng mấy ví von chính cháu từng viết. Cấm tuyệt đối.
TU_CAM = re.compile(
    r'\b(kỹ sư|xưởng|thám tử|tuyệt kỹ|vũ khí|bí kíp|thần chú|mật mã|mật thư|hoa tiêu|'
    r'quan tòa|cao thủ|đơn hàng|Su Kem|Trí Long|bước chân|dấu vân tay|'
    r'người giải|chìa khoá|không gian toán|Gauss)\b', re.I)

# Câu đọc dài hơn ngần này là bé mất mạch trước khi nghe hết.
DAI_TOI_DA = 130

DON_VI = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']


def so_chu(n: int) -> str:
    """Số thành chữ tiếng Việt, tới hàng nghìn — đủ cho cả quyển lớp 4.

    Viết tay chứ không gọi thư viện: tiếng Việt có ba chỗ bất quy tắc mà thư viện
    hay làm sai — "mười lăm" (không phải "mười năm"), "hai mươi mốt" (không phải
    "hai mươi một"), và "một trăm linh năm" (không phải "một trăm không năm").
    """
    if n < 0:
        return 'âm ' + so_chu(-n)
    if n < 10:
        return DON_VI[n]
    if n < 20:
        le = n - 10
        if le == 0:
            return 'mười'
        return 'mười ' + ('lăm' if le == 5 else DON_VI[le])
    if n < 100:
        chuc, le = divmod(n, 10)
        s = f'{DON_VI[chuc]} mươi'
        if le == 1:
            return s + ' mốt'
        if le == 4:
            return s + ' tư'
        if le == 5:
            return s + ' lăm'
        return s if le == 0 else f'{s} {DON_VI[le]}'
    if n < 1000:
        tram, du = divmod(n, 100)
        s = f'{DON_VI[tram]} trăm'
        if du == 0:
            return s
        if du < 10:
            return f'{s} linh {DON_VI[du]}'
        return f'{s} {so_chu(du)}'
    nghin, du = divmod(n, 1000)
    s = f'{so_chu(nghin)} nghìn'
    if du == 0:
        return s
    if du < 100:
        return f'{s} không trăm {so_chu(du)}' if du >= 10 else f'{s} không trăm linh {DON_VI[du]}'
    return f'{s} {so_chu(du)}'


def doc_duoc(s: str) -> str:
    """Chữ đem ĐỌC. Chỉ còn chữ cái, dấu chấm và dấu phẩy — không gì khác.

    Đây là chỗ bản đầu hỏng: nó chỉ thay vài ký hiệu rồi thôi, nên 40 dấu hai chấm
    và 11 mũi tên vẫn lọt xuống Kokoro. Nay làm ngược lại: dịch hết những gì dịch
    được, rồi XOÁ SẠCH phần còn lại — và có cổng soi lại sau cùng.
    """
    s = str(s or '')
    s = re.sub(r'\s*[×x]\s*', ' nhân ', s)
    s = re.sub(r'\s*÷\s*', ' chia ', s)
    s = re.sub(r'(\d)\s*:\s*(\d)', r'\1 chia \2', s)
    s = s.replace('−', ' trừ ').replace(' - ', ' trừ ')
    s = re.sub(r'\s*\+\s*', ' cộng ', s)
    s = re.sub(r'\s*=\s*', ' bằng ', s)
    s = re.sub(r'\s*→\s*', ' nên ', s)
    s = re.sub(r'\.\.\.|…', ' và cứ thế ', s)
    # số có dấu cách phân nhóm: "1 275" là MỘT số, đừng đọc thành hai
    s = re.sub(r'(?<=\d) (?=\d{3}\b)', '', s)
    s = re.sub(r'\d+', lambda m: ' ' + so_chu(int(m.group(0))) + ' ', s)
    s = re.sub(r'[^\w\s.,]', ' ', s, flags=re.UNICODE)
    s = re.sub(r'_', ' ', s)
    s = re.sub(r'\s+([,.])', r'\1', s)
    s = re.sub(r'([,.])(?=\S)', r'\1 ', s)
    return re.sub(r'\s+', ' ', s).strip()


def ma_am(chu: str) -> str:
    sach = ''.join(c if c.isalnum() else '_' for c in chu.lower()).strip('_')
    return f'loi_{sach}'[:60]


def _c(loai, chu='', phu='', loi=None, **k):
    loi = [doc_duoc(x) for x in (loi or []) if str(x).strip()]
    return {'loai': loai, 'chuChinh': chu, 'chuPhu': phu,
            'loiAm': [[x, 'vi'] for x in loi], 'am': [ma_am(x) for x in loi], **k}


# ═══════════════════════════════════════════════════════════════════════════
# NĂM KỊCH BẢN — viết tay. Cả năm bám vào CÙNG MỘT dãy ví dụ 5, 10, 15, 20, 25
# để bé không phải làm quen dãy mới ở mỗi bài.
# ═══════════════════════════════════════════════════════════════════════════
DAY = [5, 10, 15, 20, 25]


def kb_b13(b):
    return [
        _c('bia', 'Dãy số là gì', 'Bài 13', loi=['Hôm nay mình học về dãy số.']),
        _c('day_so', 'Đây là một dãy số', so=DAY,
           loi=['Đây là một dãy số. Năm, mười, mười lăm, hai mươi, hai mươi lăm.']),
        _c('y_toan', 'Dãy số là gì', 'Là nhiều số viết nối nhau theo một thứ tự.',
           buoc=1, soBuoc=5,
           loi=['Dãy số là nhiều số viết nối nhau theo một thứ tự.']),
        _c('day_so', 'Mỗi số gọi là một số hạng', so=DAY,
           phu='Dãy này có 5 số hạng.',
           loi=['Mỗi số trong dãy gọi là một số hạng.',
                'Dãy này có năm số hạng.']),
        _c('day_so', 'Thứ tự là chỗ đứng', so=DAY, hienThuTu=True, chiSo=1,
           phu='Số 5 đứng thứ nhất.',
           loi=['Mỗi số hạng đứng ở một chỗ. Chỗ đó gọi là thứ tự.',
                'Số năm đứng thứ nhất.']),
        _c('day_so', 'Thứ tự là chỗ đứng', so=DAY, hienThuTu=True, chiSo=3,
           phu='Số 15 đứng thứ ba.',
           loi=['Số mười đứng thứ hai. Số mười lăm đứng thứ ba.']),
        _c('day_so', 'Giá trị là con số ở chỗ đó', so=DAY, hienThuTu=True, chiSo=3,
           phu='Số hạng thứ ba có giá trị 15.',
           loi=['Con số viết ở mỗi chỗ gọi là giá trị.',
                'Số hạng thứ ba có giá trị là mười lăm.']),
        _c('y_toan', 'Thứ tự khác giá trị', 'Thứ tự là 3. Giá trị là 15.',
           buoc=2, soBuoc=5,
           loi=['Thứ tự là ba. Giá trị là mười lăm.',
                'Hai con số này khác nhau. Con nhớ kỹ chỗ này nhé.']),
        _c('y_toan', 'Bây giờ lấy số sau trừ số trước',
           '10 − 5 = 5,  15 − 10 = 5,  20 − 15 = 5', buoc=3, soBuoc=5,
           loi=['Bây giờ lấy số sau trừ số trước.',
                'Mười trừ năm bằng năm. Mười lăm trừ mười bằng năm.']),
        _c('y_toan', 'Các hiệu đều bằng nhau', 'Dãy như thế gọi là dãy cách đều.',
           buoc=4, soBuoc=5,
           loi=['Các hiệu đều bằng năm. Dãy như thế gọi là dãy cách đều.']),
        _c('y_toan', 'Khoảng cách', 'Số 5 đó gọi là khoảng cách của dãy.',
           buoc=5, soBuoc=5,
           loi=['Số năm đó gọi là khoảng cách của dãy.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b14(b):
    return [
        _c('bia', 'Số hạng thứ n', 'Bài 14', loi=['Hôm nay mình tìm số hạng ở chỗ xa.']),
        _c('day_so', 'Vẫn dãy này', so=DAY, hienThuTu=True,
           loi=['Vẫn dãy số cũ. Năm, mười, mười lăm, hai mươi, hai mươi lăm.']),
        _c('y_toan', 'Muốn tìm số hạng thứ 100 thì sao',
           'Viết cả dãy ra thì rất lâu.', buoc=1, soBuoc=4,
           loi=['Muốn tìm số hạng thứ một trăm thì sao.',
                'Viết cả dãy ra thì rất lâu. Mình cần cách nhanh hơn.']),
        _c('day_so', 'Đếm số lần cộng thêm', so=DAY, hienThuTu=True, chiSo=4,
           phu='Từ chỗ 1 đến chỗ 4 cộng thêm 3 lần.',
           loi=['Từ chỗ thứ nhất đến chỗ thứ tư, mình cộng thêm mấy lần.',
                'Đếm mà xem. Ba lần, không phải bốn lần.']),
        _c('y_toan', 'Vì sao ít hơn một',
           'Chỗ thứ nhất đã có sẵn, không phải cộng lần nào.', buoc=2, soBuoc=4,
           loi=['Vì chỗ thứ nhất đã có sẵn rồi, không phải cộng lần nào.']),
        _c('y_toan', 'Cách tìm số hạng thứ n',
           'Số đầu cộng khoảng cách nhân với n trừ 1.', buoc=3, soBuoc=4,
           loi=['Vậy số hạng thứ n bằng số đầu, cộng khoảng cách nhân với n trừ một.']),
        _c('y_toan', 'Thử với chỗ thứ tư', '5 + 5 × 3 = 20', buoc=4, soBuoc=4,
           loi=['Thử với chỗ thứ tư. Năm cộng năm nhân ba bằng hai mươi.',
                'Nhìn lại dãy mà xem, số hạng thứ tư đúng là hai mươi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b15(b):
    return [
        _c('bia', 'Dãy có bao nhiêu số hạng', 'Bài 15',
           loi=['Hôm nay mình đếm xem một dãy có bao nhiêu số hạng.']),
        _c('day_so', 'Dãy ngắn thì đếm tay được', so=DAY, hienThuTu=True,
           phu='Dãy này có 5 số hạng.',
           loi=['Dãy ngắn thì đếm tay được. Dãy này có năm số hạng.']),
        _c('y_toan', 'Dãy dài thì sao', 'Từ 5 đến 100 thì đếm tay rất lâu.',
           buoc=1, soBuoc=4,
           loi=['Nhưng dãy từ năm đến một trăm thì đếm tay rất lâu.']),
        _c('y_toan', 'Lấy số cuối trừ số đầu', '25 − 5 = 20', buoc=2, soBuoc=4,
           loi=['Mình lấy số cuối trừ số đầu. Hai mươi lăm trừ năm bằng hai mươi.']),
        _c('y_toan', 'Chia cho khoảng cách', '20 : 5 = 4', buoc=3, soBuoc=4,
           loi=['Rồi chia cho khoảng cách. Hai mươi chia năm bằng bốn.',
                'Bốn là số lần cộng thêm, chưa phải số số hạng.']),
        _c('day_so', 'Cộng thêm 1 cho chỗ đầu tiên', so=DAY, hienThuTu=True, chiSo=1,
           phu='4 + 1 = 5 số hạng.',
           loi=['Cộng thêm một cho chỗ đầu tiên. Bốn cộng một bằng năm số hạng.']),
        _c('y_toan', 'Nhớ câu này', 'Số chỗ nhiều hơn số lần cộng đúng 1.',
           buoc=4, soBuoc=4,
           loi=['Con nhớ câu này. Số chỗ luôn nhiều hơn số lần cộng đúng một.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b16(b):
    return [
        _c('bia', 'Tổng dãy cách đều', 'Bài 16',
           loi=['Hôm nay mình cộng tất cả các số trong một dãy.']),
        _c('day_so', 'Cộng cả dãy này', so=DAY,
           loi=['Cộng cả dãy này. Năm cộng mười cộng mười lăm cộng hai mươi cộng hai mươi lăm.']),
        _c('y_toan', 'Có cách nhanh hơn cộng lần lượt',
           'Ghép số đầu với số cuối.', buoc=1, soBuoc=4,
           loi=['Có cách nhanh hơn là cộng lần lượt. Mình ghép số đầu với số cuối.']),
        _c('y_toan', 'Ghép từng cặp', '5 + 25 = 30,  10 + 20 = 30',
           buoc=2, soBuoc=4,
           loi=['Năm cộng hai mươi lăm bằng ba mươi.',
                'Mười cộng hai mươi cũng bằng ba mươi. Cặp nào cũng bằng nhau.']),
        _c('y_toan', 'Vì sao cặp nào cũng bằng nhau',
           'Một bên tăng bao nhiêu, bên kia giảm bấy nhiêu.', buoc=3, soBuoc=4,
           loi=['Vì một bên tăng bao nhiêu thì bên kia giảm đúng bấy nhiêu.']),
        _c('y_toan', 'Cách tính tổng',
           'Số đầu cộng số cuối, nhân số số hạng, rồi chia đôi.', buoc=4, soBuoc=4,
           loi=['Lấy số đầu cộng số cuối, nhân với số số hạng, rồi chia đôi.',
                'Chia đôi vì mình đã ghép mỗi số hai lần.']),
        _c('y_toan', 'Thử với dãy trên', '30 × 5 : 2 = 75', buoc=4, soBuoc=4,
           loi=['Thử với dãy trên. Ba mươi nhân năm chia hai bằng bảy mươi lăm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b17(b):
    return [
        _c('bia', 'Số này có thuộc dãy không', 'Bài 17',
           loi=['Hôm nay mình xem một số có nằm trong dãy hay không.']),
        _c('day_so', 'Vẫn dãy này', so=DAY,
           phu='Số 30 có thuộc dãy này không?',
           loi=['Vẫn dãy số cũ. Số ba mươi có nằm trong dãy này không.']),
        _c('y_toan', 'Trừ số đầu trước đã', '30 − 5 = 25', buoc=1, soBuoc=4,
           loi=['Việc đầu tiên là lấy số đó trừ số đầu.',
                'Ba mươi trừ năm bằng hai mươi lăm.']),
        _c('y_toan', 'Rồi chia cho khoảng cách', '25 : 5 = 5', buoc=2, soBuoc=4,
           loi=['Rồi chia cho khoảng cách. Hai mươi lăm chia năm bằng năm.']),
        _c('y_toan', 'Chia hết thì thuộc dãy',
           'Còn dư thì không thuộc dãy.', buoc=3, soBuoc=4,
           loi=['Chia hết thì số đó thuộc dãy. Còn dư thì không thuộc dãy.']),
        _c('y_toan', 'Nó đứng thứ mấy', '5 + 1 = 6', buoc=4, soBuoc=4,
           loi=['Phép chia cho ra năm, là số lần cộng thêm.',
                'Cộng một thì ra chỗ đứng. Số ba mươi đứng thứ sáu.']),
        _c('y_toan', 'Một chốt nữa dễ quên',
           'Số đó còn phải nằm trong dãy, không vượt số cuối.', buoc=4, soBuoc=4,
           loi=['Còn một điều dễ quên. Số đó phải nằm trong dãy, không được vượt quá số cuối.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


BO = {13: kb_b13, 14: kb_b14, 15: kb_b15, 16: kb_b16, 17: kb_b17}


def soi(ds: list[dict], bai_id: str) -> list[str]:
    loi = []
    for c in ds:
        for chu, _ in c['loiAm']:
            if TU_CAM.search(chu):
                loi.append(f'{bai_id} · {c["loai"]}: lời đọc có ẩn dụ')
            if len(chu) > DAI_TOI_DA:
                loi.append(f'{bai_id} · {c["loai"]}: câu đọc dài {len(chu)} chữ '
                           f'(trần {DAI_TOI_DA}) — "{chu[:60]}…"')
            la = re.sub(r'[\w\s.,]', '', chu, flags=re.UNICODE)
            if la:
                loi.append(f'{bai_id} · {c["loai"]}: lời đọc còn ký tự lạ {la!r}')
            if re.search(r'\d', chu):
                loi.append(f'{bai_id} · {c["loai"]}: lời đọc còn CHỮ SỐ, phải đọc thành chữ')
        if TU_CAM.search(c['chuChinh'] + ' ' + c['chuPhu']):
            loi.append(f'{bai_id} · {c["loai"]}: chữ trên màn có ẩn dụ')
    return loi


def kich_ban(ma: str) -> dict:
    bai = json.loads((NGUON / f'{ma}.json').read_text('utf8'))
    lam = BO.get(bai['so'])
    if not lam:
        raise SystemExit(f'{bai["id"]}: chưa viết kịch bản video cho bài này')
    ds = lam(bai)
    xau = soi(ds, bai['id'])
    if xau:
        raise SystemExit('\n'.join('  ✗ ' + x for x in xau))
    return {'bai': bai['id'], 'tep': f'{ma}_giang.mp4', 'canh': ds}
