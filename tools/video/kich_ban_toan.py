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
THU_TU = NGUON / 'thu_tu.json'


def so_bai(b: dict) -> str:
    """Chữ "Bài n" hiện trên bìa video — ĐẾM TỪ VỊ TRÍ trong `thu_tu.json`.

    Bản đầu gõ cứng "Bài 13" vào kịch bản. Rồi chương 3 chèn thêm chín bài, B13 lùi
    xuống đứng thứ mười tám, và tám video vẫn đọc số cũ — bé xem "Bài 13" trong khi
    màn hình bên ngoài ghi "Bài 18". Video vẫn dựng ra bình thường, không cổng nào
    kêu, vì chuỗi chữ nào cũng hợp lệ. Đúng dòng họ lỗi ở chỗ nối.

    Nay số ấy đếm ra từ đúng cái lời khai mà màn hình đang dùng, nên hai bên không
    bao giờ lệch được nữa.
    """
    tt = json.loads(THU_TU.read_text('utf8'))['thuTu']
    try:
        return f'Bài {tt.index(b["id"]) + 1}'
    except ValueError:
        raise SystemExit(f'{b["id"]} không có trong thu_tu.json — chưa khai thứ tự?')

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
    # ⚠ DẤU NHÂN CHỈ Ở GIỮA HAI SỐ. Bản đầu đổi MỌI chữ `x` thành "nhân", nên nó
    # ăn luôn vào chữ tiếng Việt: "đếm mà xem" đọc thành "đếm mà nhân em", "chỗ xa"
    # thành "chỗ nhân a". Năm dòng hỏng như thế đã lên video thật, và bé nghe ra
    # một câu vô nghĩa. Ký hiệu `×` thì an toàn ở đâu cũng được — nó không phải
    # chữ cái tiếng Việt.
    s = re.sub(r'\s*×\s*', ' nhân ', s)
    s = re.sub(r'(?<=\d)\s*x\s*(?=\d)', ' nhân ', s)
    s = re.sub(r'\s*÷\s*', ' chia ', s)
    s = re.sub(r'(\d)\s*:\s*(\d)', r'\1 chia \2', s)
    # Chữ `n` trong "số hạng thứ n" là KÝ HIỆU, không phải chữ tiếng Việt. Để
    # nguyên thì Kokoro đọc theo tiếng Anh. Đọc tên chữ cái theo tiếng Việt.
    s = re.sub(r'(?<![\w])n(?![\w])', 'en-nờ', s)
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
        _c('bia', 'Dãy số là gì', so_bai(b), loi=['Hôm nay mình học về dãy số.']),
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
        _c('cong_thuc', 'Cách tìm khoảng cách',
           congThuc='khoảng cách = số sau − số trước',
           thay='10 − 5 = 5',
           loi=['Khoảng cách bằng số sau trừ số trước.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='khoảng cách = số sau − số trước',
           loi=['Con nhớ lại một lần nữa. Khoảng cách bằng số sau trừ số trước.',
                'Và thứ tự là chỗ đứng, còn giá trị là con số ở chỗ đó.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b14(b):
    return [
        _c('bia', 'Số hạng thứ n', so_bai(b), loi=['Hôm nay mình tìm số hạng ở chỗ xa.']),
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
        _c('cong_thuc', 'Cách tìm số hạng ở chỗ bất kỳ',
           congThuc='số hạng thứ n = số đầu + khoảng cách × (n − 1)',
           thay='số hạng thứ 4 = 5 + 5 × 3 = 20',
           loi=['Số hạng ở một chỗ bất kỳ bằng số đầu, cộng khoảng cách nhân với '
                'số lần cộng thêm.',
                'Thử với chỗ thứ tư. Năm cộng năm nhân ba bằng hai mươi.']),
        _c('y_toan', 'Khớp với dãy', 'Số hạng thứ tư đúng là 20.', buoc=4, soBuoc=4,
           loi=['Nhìn lại dãy mà xem, số hạng thứ tư đúng là hai mươi.']),
        _c('cong_thuc', 'Con nhớ kỹ công thức này nhé',
           congThuc='số hạng thứ n = số đầu + khoảng cách × (n − 1)',
           loi=['Con nhớ lại một lần nữa. Số hạng ở chỗ bất kỳ bằng số đầu, cộng '
                'khoảng cách nhân với số lần cộng thêm.',
                'Số lần cộng thêm luôn ít hơn số chỗ đúng một.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b15(b):
    return [
        _c('bia', 'Dãy có bao nhiêu số hạng', so_bai(b),
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
        _c('cong_thuc', 'Cách đếm số số hạng',
           congThuc='số số hạng = (số cuối − số đầu) : khoảng cách + 1',
           thay='(25 − 5) : 5 + 1 = 5',
           loi=['Số số hạng bằng số cuối trừ số đầu, chia cho khoảng cách, rồi cộng một.']),
        _c('cong_thuc', 'Con nhớ kỹ công thức này nhé',
           congThuc='số số hạng = (số cuối − số đầu) : khoảng cách + 1',
           loi=['Con nhớ lại một lần nữa. Số cuối trừ số đầu, chia cho khoảng cách, '
                'rồi cộng một.',
                'Cộng một vì số chỗ luôn nhiều hơn số lần cộng đúng một.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b16(b):
    return [
        _c('bia', 'Tổng dãy cách đều', so_bai(b),
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
        _c('cong_thuc', 'Cách tính tổng',
           congThuc='tổng = (số đầu + số cuối) × số số hạng : 2',
           thay='(5 + 25) × 5 : 2 = 75',
           loi=['Lấy số đầu cộng số cuối, nhân với số số hạng, rồi chia đôi.',
                'Ba mươi nhân năm chia hai bằng bảy mươi lăm.']),
        _c('cong_thuc', 'Con nhớ kỹ công thức này nhé',
           congThuc='tổng = (số đầu + số cuối) × số số hạng : 2',
           loi=['Con nhớ lại một lần nữa. Số đầu cộng số cuối, nhân với số số hạng, '
                'rồi chia đôi.',
                'Chia đôi vì khi ghép cặp mình đã cộng mỗi số hai lần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b17(b):
    return [
        _c('bia', 'Số này có thuộc dãy không', so_bai(b),
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
        _c('cong_thuc', 'Cách soi một số',
           congThuc='(số cần soi − số đầu) : khoảng cách',
           thay='(30 − 5) : 5 = 5  →  chỗ đứng = 5 + 1 = 6',
           loi=['Lấy số cần soi trừ số đầu, rồi chia cho khoảng cách.',
                'Chia hết thì thuộc dãy, và chỗ đứng bằng kết quả cộng một.']),
        _c('cong_thuc', 'Con nhớ kỹ công thức này nhé',
           congThuc='(số cần soi − số đầu) : khoảng cách',
           loi=['Con nhớ lại một lần nữa. Trừ số đầu trước đã, rồi mới chia cho '
                'khoảng cách.',
                'Chia hết thì thuộc dãy. Còn dư thì không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]



def kb_b18(b):
    """B18 · dùng CẢ BỐN công thức trên một bài — bài chốt của chương.

    Không dạy công thức mới. Việc của nó là cho bé thấy bốn công thức vừa học
    ĐỨNG CẠNH NHAU trên cùng một bài toán, và biết chọn cái nào."""
    return [
        _c('bia', 'Dùng cả bốn công thức', so_bai(b),
           loi=['Hôm nay mình dùng cả bốn công thức đã học vào một bài.']),
        _c('de_toan', 'Rạp phim mỗi hàng 8 ghế, đánh số liền từ 1. '
                      'Ghế đầu các hàng là 1, 9, 17, 25.',
           'Con nghe kỹ đề nhé.',
           loi=['Rạp phim mỗi hàng tám ghế, đánh số liền từ một.',
                'Ghế đầu các hàng là một, chín, mười bảy, hai mươi lăm.']),
        _c('day_so', 'Ghế đầu các hàng', so=[1, 9, 17, 25], hienThuTu=True,
           phu='Khoảng cách là 8.',
           loi=['Đây là một dãy cách đều, khoảng cách tám.']),
        _c('cong_thuc', 'Hỏi 1 — ghế đầu hàng 15 là số mấy',
           congThuc='số hạng thứ n = số đầu + khoảng cách × (n − 1)',
           thay='1 + 8 × 14 = 113',
           loi=['Câu hỏi thứ nhất dùng công thức số hạng ở chỗ bất kỳ.',
                'Một cộng tám nhân mười bốn bằng một trăm mười ba.']),
        _c('cong_thuc', 'Hỏi 2 — rạp 18 hàng thì mấy hàng ghế đầu',
           congThuc='số số hạng = (số cuối − số đầu) : khoảng cách + 1',
           thay='có 18 hàng nên có 18 số hạng',
           loi=['Câu hỏi thứ hai dùng công thức đếm số số hạng.']),
        _c('cong_thuc', 'Hỏi 3 — cộng tất cả ghế đầu hàng',
           congThuc='tổng = (số đầu + số cuối) × số số hạng : 2',
           thay='(1 + 137) × 18 : 2 = 1242',
           loi=['Câu hỏi thứ ba dùng công thức tính tổng.']),
        _c('cong_thuc', 'Hỏi 4 — vé số 113 có phải ghế đầu hàng không',
           congThuc='(số cần soi − số đầu) : khoảng cách',
           thay='(113 − 1) : 8 = 14  →  chỗ đứng = 15',
           loi=['Câu hỏi thứ tư dùng cách soi một số.',
                'Chia hết nên vé một trăm mười ba đúng là ghế đầu, của hàng mười lăm.']),
        _c('y_toan', 'Cách chọn công thức', 'Đọc kỹ câu hỏi rồi mới chọn.',
           buoc=1, soBuoc=1,
           loi=['Bốn công thức, mỗi công thức trả lời một loại câu hỏi.',
                'Con đọc kỹ câu hỏi rồi mới chọn, đừng vội tính.']),
        _c('cong_thuc', 'Con nhớ kỹ bốn công thức này nhé',
           congThuc='thứ n · số số hạng · tổng · soi một số',
           loi=['Con nhớ lại bốn công thức. Tìm số hạng ở chỗ bất kỳ, đếm số số hạng, '
                'tính tổng, và soi xem một số có thuộc dãy không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b19(b):
    """B19 · dãy KHÔNG cách đều: hai tầng và dãy nhân."""
    return [
        _c('bia', 'Dãy không cách đều', so_bai(b),
           loi=['Hôm nay mình gặp dãy không cách đều.']),
        _c('day_so', 'Dãy này có cách đều không', so=[1, 3, 6, 10, 15],
           loi=['Nhìn dãy một, ba, sáu, mười, mười lăm.',
                'Lấy số sau trừ số trước xem có bằng nhau không.']),
        _c('y_toan', 'Các hiệu KHÔNG bằng nhau', '2, 3, 4, 5 — mỗi lần một khác.',
           buoc=1, soBuoc=4,
           loi=['Các hiệu là hai, ba, bốn, năm. Không bằng nhau, nên dãy này không cách đều.']),
        _c('day_so', 'Nhưng chính các hiệu lại cách đều', so=[2, 3, 4, 5],
           phu='Đây gọi là dãy hai tầng.',
           loi=['Nhưng chính các hiệu ấy lại là một dãy cách đều.',
                'Dãy như thế gọi là dãy hai tầng.']),
        _c('y_toan', 'Viết tiếp thế nào', 'Hiệu tiếp theo là 6, rồi 7.',
           buoc=2, soBuoc=4,
           loi=['Muốn viết tiếp, con tìm hiệu tiếp theo trước.',
                'Hiệu tiếp là sáu, nên số tiếp là mười lăm cộng sáu bằng hai mươi mốt.']),
        _c('day_so', 'Còn dãy này thì sao', so=[3, 6, 12, 24],
           loi=['Còn dãy ba, sáu, mười hai, hai mươi tư thì sao.',
                'Trừ nhau không ra dãy đẹp. Con thử chia xem.']),
        _c('y_toan', 'Chia thì ra số không đổi', '6 : 3 = 2,  12 : 6 = 2,  24 : 12 = 2',
           buoc=3, soBuoc=4,
           loi=['Lấy số sau chia số trước, lần nào cũng bằng hai.',
                'Dãy như thế gọi là dãy nhân.']),
        _c('cong_thuc', 'Gặp dãy lạ thì soi hai việc',
           congThuc='trừ nhau → dãy hai tầng     chia nhau → dãy nhân',
           thay='1, 3, 6, 10 trừ nhau ra 2, 3, 4',
           loi=['Gặp dãy lạ, con làm hai việc.',
                'Trừ nhau mà ra dãy đẹp thì là dãy hai tầng. Chia nhau mà ra số không '
                'đổi thì là dãy nhân.']),
        _c('cong_thuc', 'Con nhớ kỹ hai phép thử này nhé',
           congThuc='trừ nhau → dãy hai tầng     chia nhau → dãy nhân',
           loi=['Con nhớ lại hai phép thử. Trừ nhau trước, không ra thì chia nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_b20(b):
    """B20 · trồng cây: cây và khoảng, ba thế trận."""
    return [
        _c('bia', 'Trồng cây', so_bai(b),
           loi=['Hôm nay mình đếm cây và đếm khoảng.']),
        _c('de_toan', 'Đoạn đường dài 40 mét, cứ 5 mét trồng một cây, '
                      'trồng cả hai đầu. Cần bao nhiêu cây?',
           'Con nghe kỹ đề nhé.',
           loi=['Đoạn đường dài bốn mươi mét, cứ năm mét trồng một cây, trồng cả hai đầu.',
                'Cần bao nhiêu cây.']),
        _c('y_toan', 'Chia ra được số KHOẢNG', '40 : 5 = 8 khoảng.', buoc=1, soBuoc=3,
           loi=['Bốn mươi chia năm bằng tám. Tám là số khoảng, chưa phải số cây.']),
        _c('day_so', 'Đếm thử trên đoạn ngắn', so=[0, 5, 10, 15],
           phu='4 cây nhưng chỉ 3 khoảng.',
           loi=['Đếm thử trên đoạn ngắn. Bốn cây nhưng chỉ ba khoảng.',
                'Số cây luôn nhiều hơn số khoảng đúng một.']),
        _c('cong_thuc', 'Trồng cả hai đầu',
           congThuc='số cây = số khoảng + 1',
           thay='8 + 1 = 9 cây',
           loi=['Trồng cả hai đầu thì số cây bằng số khoảng cộng một.',
                'Tám cộng một bằng chín cây.']),
        _c('y_toan', 'Nhưng có hai thế trận khác',
           'Trồng một đầu, hoặc trồng vòng kín.', buoc=2, soBuoc=3,
           loi=['Nhưng còn hai thế trận khác. Trồng một đầu thôi, hoặc trồng thành vòng kín.']),
        _c('cong_thuc', 'Một đầu, hoặc vòng kín',
           congThuc='số cây = số khoảng',
           thay='vòng kín 100 mét, mỗi 5 mét: 20 cây',
           loi=['Cả hai thế trận ấy thì số cây bằng đúng số khoảng.',
                'Vòng kín thì cây cuối đứng sát cây đầu, nên không cộng thêm.']),
        _c('y_toan', 'Câu hỏi phải trả lời trước tiên',
           'Hai đầu có cây không, hay nối thành vòng?', buoc=3, soBuoc=3,
           loi=['Trước khi tính, con trả lời một câu.',
                'Hai đầu có cây không, hay nối thành vòng.']),
        _c('cong_thuc', 'Con nhớ kỹ hai công thức này nhé',
           # Ngăn bằng dấu phẩy chứ không khoảng trắng: `giua()` xuống dòng theo BỀ
           # RỘNG, nên hai công thức cách nhau bằng khoảng trắng sẽ dính thành
           # một dòng liền không đọc nổi.
           congThuc='hai đầu: cây = khoảng + 1,  một đầu hoặc vòng: cây = khoảng',
           loi=['Con nhớ lại. Trồng cả hai đầu thì cây bằng khoảng cộng một.',
                'Trồng một đầu hoặc vòng kín thì cây bằng khoảng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 3 · CHÍN KỊCH BẢN — DẤU HIỆU CHIA HẾT
# ═══════════════════════════════════════════════════════════════════════════
# Ba luật bác ra ở đợt 2 nằm cả ở đây:
#   · mỗi video đúng MỘT vấn đề (bốn bài cũ gộp đôi ba việc, nay tách ra chín);
#   · chỗ khó hiểu thì VẼ RA (cảnh `nhom_deu` cho chia hết, `tach_so` cho dấu hiệu);
#   · mọi công thức phải GỌI TÊN TỪNG THÀNH PHẦN và nói VÌ SAO suy ra được.
#
# Luật thứ ba là chỗ chương này vốn hổng nặng nhất: bốn dấu hiệu chia hết trước nay
# chỉ được nêu ra như quy tắc phải nhớ. Nay bài nào cũng có phần chứng minh, và cả
# bốn dùng CHUNG MỘT LỐI NGHĨ — tách số ra phần chắc chắn chia hết và phần còn lại,
# rồi chỉ xét phần còn lại. Lặp đúng lối ấy bốn lần là bé nhận ra nó.
#
# Số neo 270 chạy suốt bảy bài đầu: một mình nó thoả cả bốn dấu hiệu.
KEO = 12                      # số kẹo của bài khái niệm


def kb_chia_het(b):
    """① Chia hết là gì — bài KHÁI NIỆM, không một dấu hiệu nào."""
    return [
        _c('bia', 'Chia hết là gì', so_bai(b),
           loi=['Hôm nay mình học xem chia hết nghĩa là gì.']),
        _c('nhom_deu', 'Có 12 viên kẹo, chia cho 3 bạn', tong=KEO, moiNhom=3,
           chuCuoi='Không thừa viên nào.',
           loi=['Có mười hai viên kẹo. Chia cho ba bạn.',
                'Xếp thành từng nhóm ba viên, được bốn nhóm, không thừa viên nào.']),
        _c('y_toan', 'Chia hết là chia xong không thừa gì',
           'Nên 12 chia hết cho 3.', buoc=1, soBuoc=5,
           loi=['Chia xong mà không thừa gì thì gọi là chia hết.',
                'Vậy mười hai chia hết cho ba.']),
        _c('nhom_deu', 'Bây giờ chia 13 viên cho 3 bạn', tong=13, moiNhom=3,
           chuCuoi='Còn thừa 1 viên.',
           loi=['Bây giờ có mười ba viên. Vẫn chia cho ba bạn.',
                'Được bốn nhóm, nhưng còn thừa một viên.']),
        _c('y_toan', 'Phần thừa lại gọi là số dư',
           'Ở đây số dư bằng 1.', buoc=2, soBuoc=5,
           loi=['Phần thừa lại gọi là số dư. Ở đây số dư bằng một.']),
        _c('y_toan', 'Gọi tên bốn thứ trong phép chia',
           '13 : 3 = 4 (dư 1)', buoc=3, soBuoc=5,
           loi=['Mười ba là số bị chia. Ba là số chia.',
                'Bốn là thương. Một là số dư.']),
        _c('nhom_deu', 'Vẫn 12 viên, nhưng chia cho 5 bạn', tong=KEO, moiNhom=5,
           chuCuoi='Thừa 2 viên, nên 12 không chia hết cho 5.',
           loi=['Vẫn mười hai viên, nhưng chia cho năm bạn.',
                'Được hai nhóm và thừa hai viên. Vậy mười hai không chia hết cho năm.']),
        _c('y_toan', 'Cùng một số, chia số này thì hết, chia số kia thì không',
           '12 chia hết cho 3, nhưng không chia hết cho 5.', buoc=4, soBuoc=5,
           loi=['Cùng một số mười hai. Chia cho ba thì hết, chia cho năm thì không.',
                'Nên lúc nào cũng phải hỏi rõ là chia hết cho số nào.']),
        _c('y_toan', 'Vậy nhìn vào đâu để biết',
           'Nhìn số dư. Số dư bằng 0 thì chia hết.', buoc=5, soBuoc=5,
           loi=['Muốn biết có chia hết không thì nhìn số dư.']),
        _c('cong_thuc', 'Điều cần nhớ',
           congThuc='chia hết  ⟶  số dư = 0',
           thay='12 : 3 = 4, dư 0',
           loi=['Chia hết nghĩa là số dư bằng không.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia hết  ⟶  số dư = 0',
           loi=['Con nhớ lại một lần nữa. Chia hết là số dư bằng không.',
                'Còn thừa dù chỉ một viên thì chưa gọi là chia hết.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chia_2(b):
    """② Dấu hiệu chia hết cho 2 — và VÌ SAO chỉ nhìn chữ số cuối."""
    return [
        _c('bia', 'Dấu hiệu chia hết cho 2', so_bai(b),
           loi=['Hôm nay mình học cách nhìn một cái là biết số đó chia hết cho hai.']),
        _c('tach_so', 'Xét số 24', so=24, sang=[2],
           chuPhu='Chỉ cần nhìn chữ số cuối.',
           loi=['Xét số hai mươi tư. Ta chỉ cần nhìn chữ số cuối cùng.']),
        _c('y_toan', 'Vì sao lại thế', 'Mình tách số ra hai phần.',
           buoc=1, soBuoc=5,
           loi=['Vì sao lại chỉ nhìn một chữ số. Mình tách số ra hai phần thì rõ.']),
        _c('tach_so', 'Tách 24 thành hai phần', so=24, sang=[1],
           phep='24 = 20 + 4',
           loi=['Hai mươi tư bằng hai mươi cộng bốn.']),
        _c('y_toan', 'Phần tròn chục luôn chia hết cho 2',
           '20 = 2 × 10, mà 10 = 2 × 5', buoc=2, soBuoc=5,
           loi=['Hai mươi bằng hai nhân mười, mà mười bằng hai nhân năm.',
                'Nên phần tròn chục lúc nào cũng chia hết cho hai.']),
        _c('y_toan', 'Nên phần ấy không bao giờ làm thừa',
           'Chỉ còn chữ số cuối quyết định.', buoc=3, soBuoc=5,
           loi=['Phần tròn chục không bao giờ làm thừa.',
                'Nên chỉ còn chữ số cuối quyết định.']),
        _c('tach_so', 'Chữ số cuối của 24 là 4', so=24, sang=[2],
           chuPhu='4 chia hết cho 2, nên 24 chia hết cho 2.',
           loi=['Chữ số cuối là bốn. Bốn chia hết cho hai.',
                'Vậy hai mươi tư chia hết cho hai.']),
        _c('tach_so', 'Còn số 25 thì sao', so=25, sang=[2],
           chuPhu='5 không chia hết cho 2, nên 25 không chia hết cho 2.',
           loi=['Còn hai mươi lăm. Chữ số cuối là năm, không chia hết cho hai.',
                'Vậy hai mươi lăm không chia hết cho hai.']),
        _c('y_toan', 'Năm chữ số cuối được phép', '0, 2, 4, 6 và 8',
           buoc=4, soBuoc=5,
           loi=['Có năm chữ số cuối được phép, là không, hai, bốn, sáu và tám.']),
        _c('tach_so', 'Thử với số 270', so=270, sang=[3],
           chuPhu='Chữ số cuối là 0, nên 270 chia hết cho 2.',
           loi=['Thử với hai trăm bảy mươi. Chữ số cuối là không.',
                'Vậy hai trăm bảy mươi chia hết cho hai.']),
        _c('y_toan', 'Số chia hết cho 2 còn gọi là số chẵn', '', buoc=5, soBuoc=5,
           loi=['Số chia hết cho hai còn được gọi là số chẵn.']),
        _c('cong_thuc', 'Dấu hiệu chia hết cho 2',
           congThuc='chữ số tận cùng là 0, 2, 4, 6 hoặc 8',
           thay='270 tận cùng 0  ⟶  chia hết',
           loi=['Số chia hết cho hai là số có chữ số tận cùng là không, hai, bốn, '
                'sáu hoặc tám.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chữ số tận cùng là 0, 2, 4, 6 hoặc 8',
           loi=['Con nhớ lại một lần nữa. Chỉ nhìn chữ số cuối cùng.',
                'Vì phần tròn chục đã chia hết cho hai sẵn rồi, không làm thừa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chia_5(b):
    """③ Dấu hiệu chia hết cho 5 — cùng lối nghĩ, cố ý lặp lại."""
    return [
        _c('bia', 'Dấu hiệu chia hết cho 5', so_bai(b),
           loi=['Hôm nay mình dùng lại đúng cách nghĩ hôm qua, nhưng với số năm.']),
        _c('tach_so', 'Xét số 35', so=35, sang=[2],
           chuPhu='Lại chỉ nhìn chữ số cuối.',
           loi=['Xét số ba mươi lăm. Ta lại chỉ nhìn chữ số cuối.']),
        _c('tach_so', 'Tách 35 thành hai phần', so=35, sang=[1],
           phep='35 = 30 + 5',
           loi=['Ba mươi lăm bằng ba mươi cộng năm.']),
        _c('y_toan', 'Phần tròn chục cũng chia hết cho 5',
           '30 = 3 × 10, mà 10 = 5 × 2', buoc=1, soBuoc=4,
           loi=['Ba mươi bằng ba nhân mười, mà mười bằng năm nhân hai.',
                'Nên phần tròn chục cũng chia hết cho năm.']),
        _c('y_toan', 'Nên lại chỉ còn chữ số cuối quyết định',
           'Đúng cách nghĩ của bài hôm qua.', buoc=2, soBuoc=4,
           loi=['Nên lại chỉ còn chữ số cuối quyết định.',
                'Đây đúng là cách nghĩ của bài hôm qua, dùng lại được.']),
        _c('tach_so', 'Chữ số cuối của 35 là 5', so=35, sang=[2],
           chuPhu='5 chia hết cho 5, nên 35 chia hết cho 5.',
           loi=['Chữ số cuối là năm, mà năm chia hết cho năm.',
                'Vậy ba mươi lăm chia hết cho năm.']),
        _c('y_toan', 'Chỉ có hai chữ số cuối được phép', '0 và 5',
           buoc=3, soBuoc=4,
           loi=['Chỉ có hai chữ số cuối được phép, là không và năm.']),
        _c('tach_so', 'Cẩn thận với số 52', so=52, sang=[2],
           chuPhu='Có chữ số 5 nhưng không đứng cuối, nên 52 không chia hết cho 5.',
           loi=['Cẩn thận với năm mươi hai. Trong số này có chữ số năm.',
                'Nhưng nó không đứng cuối, nên năm mươi hai không chia hết cho năm.']),
        _c('tach_so', 'Thử với số 270', so=270, sang=[3],
           chuPhu='Chữ số cuối là 0, nên 270 chia hết cho 5.',
           loi=['Thử với hai trăm bảy mươi. Chữ số cuối là không.',
                'Vậy hai trăm bảy mươi cũng chia hết cho năm.']),
        _c('y_toan', 'Số 270 chia hết cho cả hai số đã học',
           'Chia hết cho 2, và chia hết cho 5.', buoc=4, soBuoc=4,
           loi=['Hai trăm bảy mươi chia hết cho cả hai và cả năm.',
                'Bài sau mình sẽ xem vì sao lại có số làm được cả hai.']),
        _c('cong_thuc', 'Dấu hiệu chia hết cho 5',
           congThuc='chữ số tận cùng là 0 hoặc 5',
           thay='270 tận cùng 0  ⟶  chia hết',
           loi=['Số chia hết cho năm là số có chữ số tận cùng là không hoặc năm.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chữ số tận cùng là 0 hoặc 5',
           loi=['Con nhớ lại một lần nữa. Chỉ hai chữ số cuối được phép.',
                'Có chữ số năm ở giữa số thì không tính đâu nhé.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chia_2_5(b):
    """④ Chia hết cho CẢ 2 và 5 — dạy cách nghĩ phần chung."""
    return [
        _c('bia', 'Chia hết cho cả 2 và cho 5', so_bai(b),
           loi=['Hôm nay mình hỏi một câu mới. Số nào chia hết cho cả hai và cả năm.']),
        _c('y_toan', 'Con đã có hai danh sách',
           'Cho 2 thì tận cùng 0, 2, 4, 6, 8', buoc=1, soBuoc=4,
           loi=['Con đã có hai danh sách rồi.',
                'Chia hết cho hai thì tận cùng là không, hai, bốn, sáu hoặc tám.']),
        _c('y_toan', 'Và danh sách thứ hai',
           'Cho 5 thì tận cùng 0 hoặc 5', buoc=2, soBuoc=4,
           loi=['Chia hết cho năm thì tận cùng là không hoặc năm.']),
        _c('y_toan', 'Muốn thoả cả hai thì tìm phần chung',
           'Chữ số nào có mặt ở CẢ HAI danh sách?', buoc=3, soBuoc=4,
           loi=['Muốn thoả cả hai cùng lúc thì tìm chữ số có mặt ở cả hai danh sách.']),
        _c('tach_so', 'Chỉ có đúng một chữ số', so=0, sang=[1],
           chuPhu='Chỉ số 0 có mặt ở cả hai danh sách.',
           loi=['Chỉ có đúng một chữ số, là số không.']),
        _c('y_toan', 'Nên tận cùng phải bằng 0',
           'Không còn chữ số nào khác làm được.', buoc=4, soBuoc=4,
           loi=['Nên số chia hết cho cả hai và cả năm phải có tận cùng bằng không.']),
        _c('tach_so', 'Xét số 270', so=270, sang=[3],
           chuPhu='Tận cùng 0, nên chia hết cho cả 2 và 5.',
           loi=['Xét hai trăm bảy mươi. Tận cùng là không.',
                'Vậy nó chia hết cho cả hai và cả năm.']),
        _c('tach_so', 'Xét số 275', so=275, sang=[3],
           chuPhu='Tận cùng 5, chỉ chia hết cho 5.',
           loi=['Xét hai trăm bảy mươi lăm. Tận cùng là năm.',
                'Số năm là số lẻ, nên nó chỉ chia hết cho năm thôi.']),
        _c('tach_so', 'Xét số 264', so=264, sang=[3],
           chuPhu='Tận cùng 4, chỉ chia hết cho 2.',
           loi=['Xét hai trăm sáu mươi tư. Tận cùng là bốn.',
                'Nên nó chỉ chia hết cho hai thôi.']),
        _c('cong_thuc', 'Chia hết cho cả 2 và cho 5',
           congThuc='chữ số tận cùng = 0',
           thay='270 tận cùng 0  ⟶  cả hai',
           loi=['Số chia hết cho cả hai và cả năm là số có tận cùng bằng không.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chữ số tận cùng = 0',
           loi=['Con nhớ lại một lần nữa. Phải thoả đủ cả hai điều kiện.',
                'Thoả một cái thôi thì chưa được, và chỉ số không làm được cả hai.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chia_9(b):
    """⑤ Dấu hiệu chia hết cho 9 — bài KHÓ NHẤT chương, và phần vì sao là chính."""
    return [
        _c('bia', 'Dấu hiệu chia hết cho 9', so_bai(b),
           loi=['Hôm nay mình học một dấu hiệu khác hẳn ba bài trước.']),
        _c('tach_so', 'Với số 9 thì KHÔNG nhìn chữ số cuối', so=270, sang=[1, 2, 3],
           chuPhu='Phải cộng TẤT CẢ các chữ số lại.',
           loi=['Với số chín thì không nhìn chữ số cuối nữa.',
                'Mà phải cộng tất cả các chữ số lại.']),
        _c('y_toan', 'Nghe rất lạ', 'Nên mình xem vì sao lại thế.',
           buoc=1, soBuoc=5,
           loi=['Nghe rất lạ. Nên mình xem vì sao lại thế.']),
        _c('tach_so', 'Viết 270 ra theo hàng', so=270, sang=[],
           phep='270 = 2 × 100 + 7 × 10',
           loi=['Hai trăm bảy mươi bằng hai nhân một trăm, cộng bảy nhân mười.']),
        _c('y_toan', 'Bây giờ tách 100 và 10 ra',
           '100 = 99 + 1   và   10 = 9 + 1', buoc=2, soBuoc=5,
           loi=['Bây giờ tách ra. Một trăm bằng chín mươi chín cộng một.',
                'Và mười bằng chín cộng một.']),
        _c('y_toan', 'Thay vào thì được',
           '270 = (2 × 99 + 7 × 9) + (2 + 7 + 0)', buoc=3, soBuoc=5,
           loi=['Thay vào thì hai trăm bảy mươi tách được thành hai phần.']),
        _c('y_toan', 'Phần đầu luôn chia hết cho 9',
           'Vì 9 và 99 đều chia hết cho 9.', buoc=4, soBuoc=5,
           loi=['Phần đầu luôn chia hết cho chín, vì chín và chín mươi chín đều chia '
                'hết cho chín.']),
        _c('y_toan', 'Nên chỉ phần sau quyết định',
           'Phần sau đúng bằng TỔNG CÁC CHỮ SỐ.', buoc=5, soBuoc=5,
           loi=['Nên chỉ phần sau quyết định. Mà phần sau đúng bằng tổng các chữ số.',
                'Đó là lý do ta đi cộng các chữ số lại.']),
        _c('tach_so', 'Cộng các chữ số của 270', so=270, sang=[1, 2, 3],
           phep='2 + 7 + 0 = 9',
           chuPhu='9 chia hết cho 9, nên 270 chia hết cho 9.',
           loi=['Cộng lại được chín. Chín chia hết cho chín.',
                'Vậy hai trăm bảy mươi chia hết cho chín.']),
        _c('tach_so', 'Thử thêm số 72', so=72, sang=[1, 2],
           phep='7 + 2 = 9',
           chuPhu='Cũng chia hết cho 9.',
           loi=['Thử thêm bảy mươi hai. Bảy cộng hai bằng chín.',
                'Vậy bảy mươi hai cũng chia hết cho chín.']),
        _c('cong_thuc', 'Dấu hiệu chia hết cho 9',
           congThuc='tổng các chữ số chia hết cho 9',
           thay='2 + 7 + 0 = 9  ⟶  chia hết',
           loi=['Số chia hết cho chín là số có tổng các chữ số chia hết cho chín.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tổng các chữ số chia hết cho 9',
           loi=['Con nhớ lại một lần nữa. Cộng hết các chữ số lại rồi mới xét.',
                'Ta cộng được vì mười hơn chín đúng một đơn vị, nên mỗi chục để lại '
                'đúng một.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chia_3(b):
    """⑥ Dấu hiệu chia hết cho 3 — và quan hệ MỘT CHIỀU với 9."""
    return [
        _c('bia', 'Dấu hiệu chia hết cho 3', so_bai(b),
           loi=['Hôm nay mình dùng lại cách nghĩ của bài chín, nhưng với số ba.']),
        _c('tach_so', 'Cộng các chữ số của 270', so=270, sang=[1, 2, 3],
           phep='2 + 7 + 0 = 9',
           chuPhu='9 chia hết cho 3, nên 270 chia hết cho 3.',
           loi=['Cộng các chữ số của hai trăm bảy mươi được chín.',
                'Chín chia hết cho ba, nên hai trăm bảy mươi chia hết cho ba.']),
        _c('y_toan', 'Vì sao lại cộng được như với số 9',
           'Vì 9 và 99 cũng chia hết cho 3.', buoc=1, soBuoc=4,
           loi=['Vì sao lại cộng được giống hệt bài trước.',
                'Vì chín và chín mươi chín cũng chia hết cho ba.']),
        _c('y_toan', 'Nên phần đầu vẫn không làm thừa',
           'Chỉ tổng các chữ số quyết định.', buoc=2, soBuoc=4,
           loi=['Nên phần đầu vẫn không làm thừa, và chỉ tổng các chữ số quyết định.']),
        _c('tach_so', 'Bây giờ xét số 12', so=12, sang=[1, 2],
           phep='1 + 2 = 3',
           chuPhu='3 chia hết cho 3, nên 12 chia hết cho 3.',
           loi=['Bây giờ xét mười hai. Một cộng hai bằng ba.',
                'Ba chia hết cho ba, nên mười hai chia hết cho ba.']),
        _c('y_toan', 'Nhưng 12 có chia hết cho 9 không',
           'Tổng là 3, mà 3 KHÔNG chia hết cho 9.', buoc=3, soBuoc=4,
           loi=['Nhưng mười hai có chia hết cho chín không.',
                'Tổng là ba, mà ba không chia hết cho chín. Vậy là không.']),
        _c('y_toan', 'Hai dấu hiệu không thay được cho nhau',
           'Chia hết cho 9 thì chắc chắn chia hết cho 3.', buoc=4, soBuoc=4,
           loi=['Hai dấu hiệu này không thay được cho nhau.',
                'Chia hết cho chín thì chắc chắn chia hết cho ba, vì chín bằng ba '
                'nhân ba.']),
        _c('y_toan', 'Nhưng chiều ngược lại thì KHÔNG',
           'Số 12 chia hết cho 3 mà không chia hết cho 9.', buoc=4, soBuoc=4,
           loi=['Nhưng chiều ngược lại thì không đúng.',
                'Mười hai chia hết cho ba mà không chia hết cho chín.']),
        _c('cong_thuc', 'Dấu hiệu chia hết cho 3',
           congThuc='tổng các chữ số chia hết cho 3',
           thay='1 + 2 = 3  ⟶  12 chia hết cho 3',
           loi=['Số chia hết cho ba là số có tổng các chữ số chia hết cho ba.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia hết cho 9  ⟶  chia hết cho 3',
           loi=['Con nhớ lại một lần nữa. Chia hết cho chín thì chắc chắn chia hết '
                'cho ba.',
                'Nhưng chia hết cho ba thì chưa chắc chia hết cho chín.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chia_du(b):
    """⑦ Phép chia có dư — công thức, và vì sao dư luôn nhỏ hơn số chia."""
    return [
        _c('bia', 'Phép chia có dư', so_bai(b),
           loi=['Hôm nay mình viết cả phép chia thành một công thức.']),
        _c('nhom_deu', 'Có 14 cái bánh, mỗi hộp 4 cái', tong=14, moiNhom=4,
           chuCuoi='Được 3 hộp, thừa 2 cái.',
           loi=['Có mười bốn cái bánh, xếp mỗi hộp bốn cái.',
                'Được ba hộp và còn thừa hai cái.']),
        _c('y_toan', 'Viết thành phép chia', '14 : 4 = 3 (dư 2)',
           buoc=1, soBuoc=4,
           loi=['Viết thành phép chia. Mười bốn chia bốn bằng ba, dư hai.']),
        _c('y_toan', 'Gọi tên từng số',
           '14 số bị chia · 4 số chia · 3 thương · 2 số dư', buoc=2, soBuoc=4,
           loi=['Mười bốn là số bị chia. Bốn là số chia.',
                'Ba là thương. Hai là số dư.']),
        _c('y_toan', 'Ghép ngược lại thì được số ban đầu',
           '4 × 3 + 2 = 14', buoc=3, soBuoc=4,
           loi=['Ghép ngược lại. Bốn nhân ba cộng hai bằng mười bốn.',
                'Đúng bằng số ban đầu, nên phép chia không sai.']),
        _c('nhom_deu', 'Vì sao số dư phải nhỏ hơn số chia', tong=14, moiNhom=4,
           chuCuoi='Thừa 2 mà mỗi hộp cần 4 — không đủ thêm hộp nào.',
           loi=['Vì sao số dư phải nhỏ hơn số chia.',
                'Thừa hai cái, mà mỗi hộp cần bốn, nên không đủ xếp thêm hộp nào.']),
        _c('y_toan', 'Nếu phần thừa đủ một nhóm nữa',
           'Thì mình đã xếp thêm được rồi.', buoc=4, soBuoc=4,
           loi=['Nếu phần thừa mà đủ một nhóm nữa thì mình đã xếp thêm được rồi.',
                'Nên chỗ thừa lại luôn ít hơn số chia.']),
        _c('nhom_deu', 'Xếp sai thì trông thế này', tong=14, moiNhom=4,
           chuPhu='Viết 14 : 4 = 2 (dư 6) là sai',
           chuCuoi='Thừa 6 thì còn xếp thêm được một hộp nữa.',
           loi=['Có bạn viết mười bốn chia bốn bằng hai, dư sáu.',
                'Thừa sáu thì còn xếp thêm được một hộp nữa, nên viết thế là sai.']),
        _c('cong_thuc', 'Công thức phép chia có dư',
           congThuc='số bị chia = số chia × thương + số dư',
           thay='4 × 3 + 2 = 14',
           loi=['Số bị chia bằng số chia nhân thương, rồi cộng số dư.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số dư < số chia',
           loi=['Con nhớ lại một lần nữa. Số dư luôn nhỏ hơn số chia.',
                'Vì đủ một nhóm nữa thì phải xếp vào nhóm, không được để thừa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_thua_thieu(b):
    """⑧ Bài toán thừa - thiếu — đọc số dư cho đúng câu hỏi."""
    return [
        _c('bia', 'Bài toán thừa và thiếu', so_bai(b),
           loi=['Hôm nay mình học cách đọc số dư cho đúng với câu hỏi của đề.']),
        _c('de_toan', 'Lớp có 25 bạn đi tham quan. Mỗi xe chở được 6 bạn.',
           'Cần ít nhất bao nhiêu xe để chở hết cả lớp?',
           loi=['Lớp có hai mươi lăm bạn đi tham quan. Mỗi xe chở được sáu bạn.',
                'Hỏi cần ít nhất bao nhiêu xe để chở hết cả lớp.']),
        _c('nhom_deu', 'Xếp thử 25 bạn vào các xe 6 chỗ', tong=25, moiNhom=6,
           chuCuoi='Đầy 4 xe, còn thừa 1 bạn.',
           loi=['Xếp thử. Được bốn xe đầy và còn thừa một bạn.']),
        _c('y_toan', 'Phép chia', '25 : 6 = 4 (dư 1)', buoc=1, soBuoc=4,
           loi=['Hai mươi lăm chia sáu bằng bốn, dư một.']),
        _c('y_toan', 'Bây giờ đọc lại câu hỏi',
           'Đề hỏi chở HẾT cả lớp.', buoc=2, soBuoc=4,
           loi=['Bây giờ đọc lại câu hỏi. Đề hỏi chở hết cả lớp.']),
        _c('y_toan', 'Bạn thừa ra vẫn phải đi',
           'Nên phải thêm một xe nữa.', buoc=3, soBuoc=4,
           loi=['Bạn thừa ra vẫn phải đi, nên phải thêm một xe nữa.']),
        _c('y_toan', 'Đáp số', '4 + 1 = 5 xe', buoc=4, soBuoc=4,
           loi=['Vậy cần năm xe.']),
        _c('y_toan', 'Nhưng nếu đề hỏi khác thì đáp số khác',
           'Hỏi mấy xe chở ĐẦY 6 bạn thì đáp số là 4.', buoc=4, soBuoc=4,
           loi=['Nhưng nếu đề hỏi có mấy xe chở đầy sáu bạn thì đáp số chỉ là bốn.',
                'Cùng một phép chia, hỏi khác nhau thì đáp số khác nhau.']),
        _c('cong_thuc', 'Hai cách đọc số dư',
           congThuc='chở HẾT  ⟶  thương + 1',
           thay='4 + 1 = 5 xe',
           loi=['Nếu phần thừa vẫn cần một chỗ thì lấy thương cộng một.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia xong  ⟶  đọc lại câu hỏi',
           loi=['Con nhớ lại một lần nữa. Chia xong thì đọc lại câu hỏi rồi mới viết '
                'đáp số.',
                'Tính đúng mà đọc nhầm câu hỏi thì vẫn sai.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tan_cung(b):
    """⑨ Chữ số tận cùng của một tích — lối nghĩ tách phần không ảnh hưởng, lần bốn."""
    return [
        _c('bia', 'Chữ số tận cùng của một tích', so_bai(b),
           loi=['Hôm nay mình tìm chữ số cuối của một phép nhân mà không nhân hết.']),
        _c('de_toan', 'Tích 23 × 17 có chữ số tận cùng là mấy?',
           'Tìm mà không nhân hết cả phép.',
           loi=['Tích hai mươi ba nhân mười bảy có chữ số tận cùng là mấy.',
                'Mình tìm mà không nhân hết cả phép.']),
        _c('y_toan', 'Tách hai thừa số ra', '23 = 20 + 3   và   17 = 10 + 7',
           buoc=1, soBuoc=4,
           loi=['Tách hai thừa số ra. Hai mươi ba bằng hai mươi cộng ba.',
                'Mười bảy bằng mười cộng bảy.']),
        _c('y_toan', 'Nhân ra thì được bốn phần',
           '20 × 10 + 20 × 7 + 3 × 10 + 3 × 7', buoc=2, soBuoc=4,
           loi=['Nhân ra thì được bốn phần.']),
        _c('y_toan', 'Ba phần đầu đều là số tròn chục',
           'Chữ số cuối của chúng đều bằng 0.', buoc=3, soBuoc=4,
           loi=['Ba phần đầu đều có thừa số tròn chục, nên đều là số tròn chục.',
                'Chữ số cuối của chúng đều bằng không.']),
        _c('y_toan', 'Nên chúng không chạm tới chữ số cuối',
           'Chỉ phần cuối cùng quyết định.', buoc=4, soBuoc=4,
           loi=['Nên chúng không chạm tới chữ số cuối của tích.',
                'Chỉ phần cuối cùng quyết định.']),
        _c('tach_so', 'Nhân hai chữ số cuối với nhau', so=21, sang=[2],
           phep='3 × 7 = 21',
           chuPhu='Chữ số tận cùng của tích là 1.',
           loi=['Ba nhân bảy bằng hai mươi mốt. Chữ số cuối là một.',
                'Vậy tích tận cùng bằng một.']),
        _c('tach_so', 'Kiểm lại bằng phép nhân đầy đủ', so=391, sang=[3],
           chuPhu='23 × 17 = 391 — đúng là tận cùng bằng 1.',
           loi=['Kiểm lại. Hai mươi ba nhân mười bảy bằng ba trăm chín mươi mốt.',
                'Đúng là tận cùng bằng một.']),
        _c('y_toan', 'Cách này dùng để soi bài rất nhanh',
           'Nhân xong nhìn chữ số cuối, lệch là biết sai.', buoc=4, soBuoc=4,
           loi=['Cách này dùng để soi lại bài rất nhanh.',
                'Nhân xong nhìn chữ số cuối, lệch là biết mình sai ngay.']),
        _c('cong_thuc', 'Chữ số tận cùng của một tích',
           congThuc='lấy chữ số cuối nhân chữ số cuối',
           thay='3 × 7 = 21  ⟶  tận cùng 1',
           loi=['Lấy chữ số cuối của hai thừa số nhân với nhau, rồi lấy chữ số cuối '
                'của kết quả.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='lấy chữ số cuối nhân chữ số cuối',
           loi=['Con nhớ lại một lần nữa. Chỉ hai chữ số cuối quyết định.',
                'Vì phần tròn chục nhân ra lúc nào cũng tận cùng bằng không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# Khoá theo MÃ BÀI, không theo số bài. Từ 14-08 (lối C) số bài đếm từ vị trí trong
# `thu_tu.json`, nên nó đổi mỗi khi chèn bài mới — khoá theo nó thì chèn chín bài
# vào chương 3 là tám kịch bản này nhảy sang nhầm bài, mà vẫn dựng ra video hợp lệ.
BO = {
    'DL:KSN4.B13': kb_b13, 'DL:KSN4.B14': kb_b14, 'DL:KSN4.B15': kb_b15,
    'DL:KSN4.B16': kb_b16, 'DL:KSN4.B17': kb_b17, 'DL:KSN4.B18': kb_b18,
    'DL:KSN4.B19': kb_b19, 'DL:KSN4.B20': kb_b20,
    # ── chương 3 · chín bài dấu hiệu chia hết ──
    'DL:KSN4.B50': kb_chia_het, 'DL:KSN4.B09': kb_chia_2,
    'DL:KSN4.B51': kb_chia_5, 'DL:KSN4.B52': kb_chia_2_5,
    'DL:KSN4.B10': kb_chia_9, 'DL:KSN4.B53': kb_chia_3,
    'DL:KSN4.B11': kb_chia_du, 'DL:KSN4.B54': kb_thua_thieu,
    'DL:KSN4.B12': kb_tan_cung,
}


def soi(ds: list[dict], bai_id: str) -> list[str]:
    loi = []
    # Bác chốt 14-08: công thức phải HIỆN LÊN, và phải NHẮC LẠI trước khi kết.
    ct = [c for c in ds if c['loai'] == 'cong_thuc']
    if not ct:
        loi.append(f'{bai_id}: không có màn CÔNG THỨC nào')
    elif ds[-2]['loai'] != 'cong_thuc':
        loi.append(f'{bai_id}: màn ngay trước lúc kết phải là NHẮC LẠI công thức, '
                   f'đang là "{ds[-2]["loai"]}"')
    for c in ct:
        if not c.get('congThuc'):
            loi.append(f'{bai_id}: màn công thức thiếu chữ để hiện lên')
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
    lam = BO.get(bai['id'])
    if not lam:
        raise SystemExit(f'{bai["id"]}: chưa viết kịch bản video cho bài này')
    ds = lam(bai)
    xau = soi(ds, bai['id'])
    if xau:
        raise SystemExit('\n'.join('  ✗ ' + x for x in xau))
    return {'bai': bai['id'], 'tep': f'{ma}_giang.mp4', 'canh': ds}
