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
# ⚠ ĐỪNG GHIM MỘT QUYỂN VÀO ĐÂY. Bản đầu ghim `data/lop4`, nên lúc mở sang quyển
# lớp 2 thì mọi thứ vẫn chạy — chỉ có điều nó đọc nhầm tệp của lớp 4 và chết ở chỗ
# "không có bài này". Nay thư mục suy TỪ MÃ BÀI: `DL_KSN2_B01` → `data/lop2`.
QUYEN_CUA = {'KSN2': 'lop2', 'KSN3': 'lop3', 'KSN4': 'lop4'}


def _thu_muc(ma_hoac_id: str) -> Path:
    """`DL_KSN4_B13` hay `DL:KSN4.B13` → thư mục nguồn của quyển ấy."""
    for k, v in QUYEN_CUA.items():
        if k in ma_hoac_id:
            return GOC / 'data' / v
    raise SystemExit(f'{ma_hoac_id}: không nhận ra quyển nào')


def so_bai(b: dict) -> str:
    """Chữ "Bài n" hiện trên bìa video — ĐẾM TỪ VỊ TRÍ trong `thu_tu.json`.

    Bản đầu gõ cứng "Bài 13" vào kịch bản. Rồi chương 3 chèn thêm chín bài, B13 lùi
    xuống đứng thứ mười tám, và tám video vẫn đọc số cũ — bé xem "Bài 13" trong khi
    màn hình bên ngoài ghi "Bài 18". Video vẫn dựng ra bình thường, không cổng nào
    kêu, vì chuỗi chữ nào cũng hợp lệ. Đúng dòng họ lỗi ở chỗ nối.

    Nay số ấy đếm ra từ đúng cái lời khai mà màn hình đang dùng, nên hai bên không
    bao giờ lệch được nữa.
    """
    tt = json.loads((_thu_muc(b['id']) / 'thu_tu.json').read_text('utf8'))['thuTu']
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


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 5 · SÁU KỊCH BẢN — TRUNG BÌNH CỘNG
# ═══════════════════════════════════════════════════════════════════════════
# Bộ neo 4 · 6 · 8 chạy suốt sáu bài. Chọn nó vì mọi thứ của chương này nhìn thấy
# được trên đúng bộ ba ấy: tổng 18 chia 3 ra chẵn 6; số giữa đúng bằng trung bình nên
# san bằng chỉ là cột 8 nhường 2 cho cột 4; và phần nhô lên (2) đúng bằng phần hụt
# xuống (2) — đó là trọn bài "hơn kém mức trung bình", khỏi phải chứng minh.
TBC = [4, 6, 8]


def kb_tbc_la_gi(b):
    """① Trung bình cộng là gì — bài KHÁI NIỆM, và chỗ công thức sinh ra."""
    return [
        _c('bia', 'Trung bình cộng là gì', so_bai(b),
           loi=['Hôm nay mình học xem trung bình cộng là gì.']),
        _c('san_bang', 'Ba bạn có 4, 6 và 8 cái kẹo', so=TBC,
           chuPhu='Ba bạn không bằng nhau.',
           loi=['Ba bạn có bốn, sáu và tám cái kẹo. Ba bạn không bằng nhau.']),
        _c('y_toan', 'Chia lại cho ba bạn bằng nhau', 'Mỗi bạn được mấy cái?',
           buoc=1, soBuoc=4,
           loi=['Bây giờ chia lại cho ba bạn bằng nhau. Mỗi bạn được mấy cái.']),
        _c('san_bang', 'San cho bằng nhau', so=TBC, deu=True,
           chuPhu='Cả ba bạn đều được 6 cái.',
           loi=['San cho bằng nhau thì cả ba bạn đều được sáu cái.']),
        _c('y_toan', 'San bằng là chuyển qua lại',
           'Bạn có 8 nhường 2 cho bạn có 4. Bạn có 6 đứng yên.', buoc=2, soBuoc=4,
           loi=['Bạn có tám cái nhường hai cái cho bạn có bốn cái.',
                'Bạn có sáu cái đứng yên.']),
        _c('y_toan', 'Còn một cách nữa', '4 + 6 + 8 = 18,  rồi  18 : 3 = 6',
           buoc=3, soBuoc=4,
           loi=['Còn một cách nữa. Gộp hết lại được mười tám cái.',
                'Chia đều cho ba bạn được sáu cái.']),
        _c('y_toan', 'Hai cách cho cùng một kết quả',
           'Vì san bằng không làm đổi tổng.', buoc=4, soBuoc=4,
           loi=['Hai cách đều ra sáu.',
                'Vì san bằng chỉ là chuyển kẹo qua lại, tổng số kẹo không đổi.']),
        _c('cong_thuc', 'Cách tìm trung bình cộng',
           congThuc='trung bình cộng = tổng : số lượng',
           thay='18 : 3 = 6',
           loi=['Trung bình cộng bằng tổng chia cho số lượng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='trung bình cộng = tổng : số lượng',
           loi=['Con nhớ lại một lần nữa. Cộng hết lại rồi chia cho số phần.',
                'Cộng xong mà quên chia thì đó mới là tổng, chưa phải trung bình cộng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tim_tbc(b):
    """② Tìm trung bình cộng — một việc duy nhất: ĐẾM ĐÚNG có mấy số."""
    return [
        _c('bia', 'Tìm trung bình cộng', so_bai(b),
           loi=['Hôm nay mình dùng công thức cho thật thạo.']),
        _c('de_toan', 'Đội ghi bàn trong 4 trận: 2 ; 5 ; 2 ; 3 bàn.',
           'Trung bình mỗi trận đội ghi mấy bàn?',
           loi=['Đội ghi bàn trong bốn trận. Hai, năm, hai và ba bàn.',
                'Hỏi trung bình mỗi trận đội ghi mấy bàn.']),
        _c('y_toan', 'Cộng hết lại', '2 + 5 + 2 + 3 = 12', buoc=1, soBuoc=4,
           loi=['Cộng hết lại được mười hai bàn.']),
        _c('y_toan', 'Bây giờ đếm xem có mấy số',
           'Bốn trận thì có bốn số.', buoc=2, soBuoc=4,
           loi=['Bây giờ đếm xem có mấy số. Bốn trận thì có bốn số.',
                'Số hai xuất hiện hai lần thì vẫn đếm là hai số.']),
        _c('y_toan', 'Chia đều', '12 : 4 = 3', buoc=3, soBuoc=4,
           loi=['Chia đều được ba bàn.']),
        _c('san_bang', 'Vẽ ra thì thấy mức trung bình', so=[2, 5, 2, 3], mucTB=True,
           chuPhu='Mức trung bình là 3.',
           loi=['Vẽ ra thì thấy mức trung bình là ba.']),
        _c('y_toan', 'Soi lại cho chắc',
           'Kết quả phải nằm giữa số bé nhất và số lớn nhất.', buoc=4, soBuoc=4,
           loi=['Soi lại cho chắc. Số bé nhất là hai, số lớn nhất là năm.',
                'Kết quả ba nằm giữa hai số ấy nên hợp lý.']),
        _c('cong_thuc', 'Nhớ chia cho ĐÚNG số lượng',
           congThuc='trung bình cộng = tổng : số lượng',
           thay='12 : 4 = 3',
           loi=['Trung bình cộng bằng tổng chia cho số lượng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số lặp lại vẫn đếm đủ số lần',
           loi=['Con nhớ lại một lần nữa. Số lặp lại vẫn phải đếm đủ số lần.',
                'Và kết quả luôn nằm giữa số bé nhất với số lớn nhất.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tim_tong(b):
    """③ Biết trung bình cộng, tìm tổng — công thức ngược, và VÌ SAO nó đúng."""
    return [
        _c('bia', 'Biết trung bình cộng, tìm tổng', so_bai(b),
           loi=['Hôm nay mình đi chiều ngược lại.']),
        _c('de_toan', 'Trung bình cộng của 4 số là 25.',
           'Tổng của bốn số ấy bằng bao nhiêu?',
           loi=['Trung bình cộng của bốn số là hai mươi lăm.',
                'Hỏi tổng của bốn số ấy bằng bao nhiêu.']),
        _c('y_toan', 'Nhớ lại chiều thuận', 'Tổng chia cho 4 thì được 25.',
           buoc=1, soBuoc=3,
           loi=['Nhớ lại chiều thuận. Tổng chia cho bốn thì được hai mươi lăm.']),
        _c('y_toan', 'Đọc ngược phép chia',
           'Chia cho 4 được 25 thì số ban đầu là 25 nhân 4.', buoc=2, soBuoc=3,
           loi=['Đọc ngược lại. Chia cho bốn mà được hai mươi lăm.',
                'Thì số ban đầu phải là hai mươi lăm nhân bốn.']),
        _c('san_bang', 'Nghĩ theo cách san bằng cũng ra thế',
           so=[25, 25, 25, 25],
           chuPhu='Mỗi phần 25, có 4 phần, gộp lại là 100.',
           loi=['Nghĩ theo cách san bằng cũng ra thế.',
                'Mỗi phần có hai mươi lăm, có bốn phần, gộp lại là một trăm.']),
        _c('y_toan', 'Tính ra', '25 × 4 = 100', buoc=3, soBuoc=3,
           loi=['Hai mươi lăm nhân bốn bằng một trăm.']),
        _c('cong_thuc', 'Cách tìm tổng',
           congThuc='tổng = trung bình cộng × số lượng',
           thay='25 × 4 = 100',
           loi=['Tổng bằng trung bình cộng nhân với số lượng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tổng = trung bình cộng × số lượng',
           loi=['Con nhớ lại một lần nữa. Trung bình cộng là số của MỘT phần.',
                'Muốn ra số của tất cả các phần thì nhân với số lượng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_so_thieu(b):
    """④ Tìm số còn thiếu — không công thức mới, chỉ nối hai bước đã biết."""
    return [
        _c('bia', 'Tìm số còn thiếu', so_bai(b),
           loi=['Hôm nay mình tìm một con số bị giấu đi.']),
        _c('de_toan', 'Trung bình cộng của hai số là 36, một số bằng 40.',
           'Tìm số còn lại.',
           loi=['Trung bình cộng của hai số là ba mươi sáu. Một số bằng bốn mươi.',
                'Hỏi số còn lại bằng bao nhiêu.']),
        _c('y_toan', 'Bước 1 — tìm tổng', '36 × 2 = 72', buoc=1, soBuoc=3,
           loi=['Bước một. Trung bình cộng là ba mươi sáu, có hai số.',
                'Nên tổng là ba mươi sáu nhân hai, bằng bảy mươi hai.']),
        _c('y_toan', 'Bước 2 — trừ đi số đã biết', '72 − 40 = 32', buoc=2, soBuoc=3,
           loi=['Bước hai. Lấy bảy mươi hai trừ bốn mươi, được ba mươi hai.']),
        _c('san_bang', 'Hai số ấy san bằng thì đúng mức 36', so=[40, 32], mucTB=True,
           chuPhu='Một số hơn 4, một số kém 4.',
           loi=['Vẽ ra thì thấy một số hơn mức bốn, một số kém mức bốn.']),
        _c('y_toan', 'Bước 3 — thử lại', '(40 + 32) : 2 = 36', buoc=3, soBuoc=3,
           loi=['Bước ba, thử lại. Bốn mươi cộng ba mươi hai chia hai bằng ba mươi sáu.',
                'Đúng bằng đề cho, nên bài làm đúng.']),
        _c('cong_thuc', 'Hai bước, không có công thức mới',
           congThuc='số còn thiếu = tổng − các số đã biết',
           thay='72 − 40 = 32',
           loi=['Số còn thiếu bằng tổng trừ đi các số đã biết.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tìm TỔNG trước, rồi mới trừ',
           loi=['Con nhớ lại một lần nữa. Phải tìm tổng trước, rồi mới trừ.',
                'Trừ thẳng vào trung bình cộng là sai, vì nó mới là số của một phần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_hon_kem(b):
    """⑤ Hơn kém mức trung bình — phần nhô lên bằng đúng phần hụt xuống."""
    return [
        _c('bia', 'Hơn kém mức trung bình', so_bai(b),
           loi=['Hôm nay mình xem mỗi số cách mức trung bình bao xa.']),
        _c('san_bang', 'Ba số 4 ; 6 ; 8 có mức trung bình là 6', so=TBC, mucTB=True,
           chuPhu='Vạch ngang là mức trung bình.',
           loi=['Ba số bốn, sáu và tám có mức trung bình là sáu.',
                'Vạch ngang chính là mức ấy.']),
        _c('y_toan', 'Số 4 nằm dưới vạch', '6 − 4 = 2, nên số 4 kém mức 2 đơn vị',
           buoc=1, soBuoc=4,
           loi=['Số bốn nằm dưới vạch. Nó kém mức trung bình hai đơn vị.']),
        _c('y_toan', 'Số 8 nhô lên trên vạch', '8 − 6 = 2, nên số 8 hơn mức 2 đơn vị',
           buoc=2, soBuoc=4,
           loi=['Số tám nhô lên trên vạch. Nó hơn mức trung bình hai đơn vị.']),
        _c('y_toan', 'Số 6 đúng bằng mức',
           'Không hơn cũng không kém.', buoc=3, soBuoc=4,
           loi=['Số sáu đúng bằng mức, không hơn cũng không kém.']),
        _c('y_toan', 'Phần nhô lên bằng đúng phần hụt xuống',
           'Phần hơn là 2. Phần kém cũng là 2.', buoc=4, soBuoc=4,
           loi=['Phần nhô lên là hai. Phần hụt xuống cũng là hai. Hai bên bằng nhau.']),
        _c('san_bang', 'Vì san bằng là lấy phần nhô đắp vào chỗ hụt', so=TBC, deu=True,
           chuPhu='Đắp xong vừa khít, không thừa không thiếu.',
           loi=['Vì san bằng chính là lấy phần nhô đắp vào chỗ hụt.',
                'Đắp xong vừa khít, nên hai phần phải bằng nhau ngay từ đầu.']),
        _c('cong_thuc', 'Điều cần nhớ',
           congThuc='tổng phần hơn = tổng phần kém',
           thay='2 = 2',
           loi=['Tổng phần hơn luôn bằng tổng phần kém.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hơn kém bao nhiêu = số đó − mức trung bình',
           loi=['Con nhớ lại một lần nữa. Muốn biết hơn kém bao nhiêu thì lấy số đó '
                'trừ mức trung bình.',
                'Đừng lấy luôn con số ấy làm phần hơn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_them_so(b):
    """⑥ Thêm một số vào nhóm — chỗ quên nhiều nhất là SỐ LƯỢNG đã đổi."""
    return [
        _c('bia', 'Thêm một số vào nhóm', so_bai(b),
           loi=['Hôm nay mình thêm một bạn vào nhóm rồi tính lại.']),
        _c('san_bang', 'Ba bạn có trung bình 6 cái kẹo', so=[6, 6, 6],
           chuPhu='Đã san đều, mỗi bạn 6 cái.',
           loi=['Ba bạn có trung bình sáu cái kẹo. Đã san đều, mỗi bạn sáu cái.']),
        _c('y_toan', 'Bước 1 — lấy tổng cũ', '6 × 3 = 18', buoc=1, soBuoc=4,
           loi=['Bước một. Ba bạn, trung bình sáu, nên tổng cũ là mười tám cái.']),
        _c('san_bang', 'Thêm một bạn có 10 cái', so=[6, 6, 6, 10], mucTB=True,
           chuPhu='Bạn mới cao hơn mức cũ.',
           loi=['Thêm một bạn nữa có mười cái. Bạn mới cao hơn mức cũ.']),
        _c('y_toan', 'Bước 2 — cộng số mới', '18 + 10 = 28', buoc=2, soBuoc=4,
           loi=['Bước hai. Tổng mới là mười tám cộng mười, bằng hai mươi tám.']),
        _c('y_toan', 'Bước 3 — chia lại cho SỐ LƯỢNG MỚI', '28 : 4 = 7',
           buoc=3, soBuoc=4,
           loi=['Bước ba. Bây giờ có bốn bạn chứ không phải ba nữa.',
                'Hai mươi tám chia bốn bằng bảy.']),
        _c('y_toan', 'Đoán trước cho chắc',
           'Bạn mới nhiều hơn mức cũ nên trung bình phải TĂNG.', buoc=4, soBuoc=4,
           loi=['Đoán trước cho chắc. Bạn mới có nhiều hơn mức cũ.',
                'Nên trung bình phải tăng. Kết quả bảy lớn hơn sáu, đúng như đoán.']),
        _c('cong_thuc', 'Tính lại trung bình',
           congThuc='trung bình mới = tổng mới : số lượng MỚI',
           thay='28 : 4 = 7',
           loi=['Trung bình mới bằng tổng mới chia cho số lượng mới.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='thêm người thì SỐ CHIA cũng đổi',
           loi=['Con nhớ lại một lần nữa. Thêm người vào nhóm thì số để chia cũng đổi.',
                'Quên đổi số lượng là chỗ hay sai nhất của bài này.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 6 · BẢY KỊCH BẢN — TỔNG - HIỆU
# ═══════════════════════════════════════════════════════════════════════════
# Bác dặn riêng: chương này **vẽ kiểu đoạn thẳng**. Nên cảnh `so_do_doan` là đoạn
# thẳng thật, và cả chương chứng minh BẰNG HÌNH chứ không nêu công thức:
#
#     thêm HIỆU vào đoạn ngắn → hai đoạn bằng nhau → hai lần số lớn = tổng + hiệu
#     cắt HIỆU khỏi đoạn dài  → hai đoạn bằng nhau → hai lần số bé  = tổng − hiệu
#
# Đó là lý do hai công thức tách thành hai bài: chúng KHÔNG phải hai câu phải nhớ,
# mà là một cách nghĩ soi từ hai phía. Dạy chung một bài thì bé lẫn dấu ngay.
TONG, HIEU, LON, BE = 70, 10, 40, 30


def kb_so_do(b):
    """① Sơ đồ đoạn thẳng là gì — bài KHÁI NIỆM, không một công thức nào."""
    return [
        _c('bia', 'Sơ đồ đoạn thẳng', so_bai(b),
           loi=['Hôm nay mình học cách vẽ bài toán ra thành hai đoạn thẳng.']),
        _c('so_do_doan', 'Hai số có tổng 70 và hiệu 10', be=BE, lon=LON,
           chuPhu='Đoạn ngắn là số bé, đoạn dài là số lớn.',
           loi=['Hai số có tổng bảy mươi và hiệu mười.',
                'Vẽ một đoạn ngắn cho số bé, một đoạn dài hơn cho số lớn.']),
        _c('y_toan', 'Hai đoạn vẽ thẳng hàng', 'Đầu bên trái ngang nhau.',
           buoc=1, soBuoc=3,
           loi=['Hai đoạn vẽ thẳng hàng, đầu bên trái ngang nhau.',
                'Có thế mới so được đoạn nào dài hơn.']),
        _c('so_do_doan', 'Khúc dôi ra chính là HIỆU', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10',
           chuPhu='Đoạn dài dôi ra một khúc bằng 10.',
           loi=['Đoạn dài dôi ra một khúc so với đoạn ngắn.',
                'Khúc ấy chính là hiệu, ở đây bằng mười.']),
        _c('y_toan', 'Còn tổng thì ghi ở đâu', 'Tổng là của CẢ HAI đoạn cộng lại.',
           buoc=2, soBuoc=3,
           loi=['Còn tổng thì ghi ở đâu. Tổng là của cả hai đoạn cộng lại.']),
        _c('so_do_doan', 'Ngoặc ôm cả hai đoạn, ghi tổng ra ngoài', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10', chuTong='tổng 70',
           chuPhu='Ghi 70 lên một đoạn là sai.',
           loi=['Ta ngoặc cả hai đoạn lại rồi ghi bảy mươi ra ngoài.',
                'Ghi bảy mươi lên một đoạn là sai, vì nó không phải của riêng đoạn nào.']),
        _c('y_toan', 'Đọc lại sơ đồ', 'Nhìn hình là biết đủ bốn thứ.',
           buoc=3, soBuoc=3,
           loi=['Nhìn hình là biết đoạn nào ngắn, khúc dôi ra bao nhiêu, và tổng bao nhiêu.']),
        _c('cong_thuc', 'Bốn thứ trên một sơ đồ',
           congThuc='đoạn ngắn · đoạn dài · khúc dôi ra = hiệu · ngoặc ngoài = tổng',
           loi=['Một sơ đồ có bốn thứ. Đoạn ngắn, đoạn dài, khúc dôi ra, và ngoặc ngoài.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='khúc dôi ra = hiệu · ngoặc ngoài = tổng',
           loi=['Con nhớ lại một lần nữa. Khúc dôi ra là hiệu, ngoặc ngoài là tổng.',
                'Vẽ được sơ đồ là con đã làm xong nửa bài rồi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_so_lon(b):
    """② Số lớn — SUY RA từ hình bằng cách thêm hiệu vào đoạn ngắn."""
    return [
        _c('bia', 'Tìm số lớn', so_bai(b),
           loi=['Hôm nay mình tìm số lớn, và tự nhìn ra công thức trên hình.']),
        _c('so_do_doan', 'Tổng 70, hiệu 10 — tìm số lớn', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10', chuTong='tổng 70',
           loi=['Hai số có tổng bảy mươi và hiệu mười. Tìm số lớn.']),
        _c('so_do_doan', 'Thêm hiệu vào đoạn ngắn', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10', themVaoBe=True,
           chuPhu='Bây giờ hai đoạn bằng nhau.',
           loi=['Nối thêm một khúc mười vào đoạn ngắn.',
                'Bây giờ hai đoạn dài bằng nhau, và mỗi đoạn đúng bằng số lớn.']),
        _c('y_toan', 'Tổng đổi thế nào', '70 + 10 = 80', buoc=1, soBuoc=3,
           loi=['Ta vừa thêm mười nên tổng cũng tăng thêm mười, thành tám mươi.']),
        _c('y_toan', '80 là của MẤY đoạn', 'Của hai đoạn bằng nhau.',
           buoc=2, soBuoc=3,
           loi=['Tám mươi là của hai đoạn bằng nhau, không phải của một đoạn.']),
        _c('y_toan', 'Nên còn phải chia đôi', '80 : 2 = 40', buoc=3, soBuoc=3,
           loi=['Nên còn phải chia đôi. Tám mươi chia hai bằng bốn mươi.',
                'Quên chia đôi là ra số lớn gấp đôi số thật.']),
        _c('cong_thuc', 'Cách tìm số lớn',
           congThuc='số lớn = (tổng + hiệu) : 2',
           thay='(70 + 10) : 2 = 40',
           loi=['Số lớn bằng tổng cộng hiệu, rồi chia đôi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số lớn = (tổng + hiệu) : 2',
           loi=['Con nhớ lại một lần nữa. Cộng hiệu vào vì ta bù cho đoạn ngắn.',
                'Chia đôi vì sau khi bù thì có hai đoạn bằng nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_so_be(b):
    """③ Số bé — cùng cách nghĩ, soi từ phía kia: cắt bớt đoạn dài."""
    return [
        _c('bia', 'Tìm số bé', so_bai(b),
           loi=['Hôm nay mình làm ngược lại bài hôm qua.']),
        _c('so_do_doan', 'Vẫn tổng 70, hiệu 10 — lần này tìm số bé', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10', chuTong='tổng 70',
           loi=['Vẫn hai số có tổng bảy mươi và hiệu mười. Lần này tìm số bé.']),
        _c('so_do_doan', 'Cắt bỏ khúc hiệu khỏi đoạn dài', be=BE, lon=LON,
           hienHieu=True, botOLon=True, chuHieu='cắt bỏ khúc này',
           chuPhu='Bây giờ hai đoạn lại bằng nhau.',
           loi=['Cắt bỏ khúc mười khỏi đoạn dài.',
                'Bây giờ hai đoạn lại bằng nhau, và mỗi đoạn đúng bằng số bé.']),
        _c('y_toan', 'Tổng đổi thế nào', '70 − 10 = 60', buoc=1, soBuoc=3,
           loi=['Ta vừa cắt đi mười nên tổng cũng giảm mười, còn sáu mươi.']),
        _c('y_toan', '60 là của hai đoạn', 'Nên chia đôi.', buoc=2, soBuoc=3,
           loi=['Sáu mươi là của hai đoạn bằng nhau, nên còn phải chia đôi.']),
        _c('y_toan', 'Số bé', '60 : 2 = 30', buoc=3, soBuoc=3,
           loi=['Sáu mươi chia hai bằng ba mươi. Vậy số bé là ba mươi.']),
        _c('so_do_doan', 'Kiểm chéo với bài hôm qua', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10', chuTong='tổng 70',
           chuPhu='30 + 40 = 70 và 40 − 30 = 10.',
           loi=['Kiểm chéo. Ba mươi cộng bốn mươi bằng bảy mươi, đúng bằng tổng.',
                'Bốn mươi trừ ba mươi bằng mười, đúng bằng hiệu.']),
        _c('cong_thuc', 'Cách tìm số bé',
           congThuc='số bé = (tổng − hiệu) : 2',
           thay='(70 − 10) : 2 = 30',
           loi=['Số bé bằng tổng trừ hiệu, rồi chia đôi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tìm số to thì CỘNG · tìm số nhỏ thì TRỪ',
           loi=['Con nhớ lại một lần nữa. Tìm số to thì cộng, tìm số nhỏ thì trừ.',
                'Và tổng bao giờ cũng lớn hơn hiệu nên lúc nào cũng trừ được.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_giau_tong(b):
    """④ Tổng bị giấu — một việc: lôi tổng ra trước."""
    return [
        _c('bia', 'Khi đề không cho sẵn tổng', so_bai(b),
           loi=['Hôm nay đề giấu mất tổng đi, mình phải tìm nó ra trước.']),
        _c('de_toan', 'Trung bình cộng của hai số là 35, hiệu của chúng là 10.',
           'Tìm hai số.',
           loi=['Trung bình cộng của hai số là ba mươi lăm. Hiệu là mười.',
                'Hỏi hai số ấy là bao nhiêu.']),
        _c('y_toan', 'Đề cho gì và thiếu gì', 'Có hiệu rồi, nhưng chưa có tổng.',
           buoc=1, soBuoc=3,
           loi=['Đề cho hiệu rồi, nhưng chưa cho tổng. Mà công thức thì cần tổng.']),
        _c('y_toan', 'Lôi tổng ra', '35 × 2 = 70', buoc=2, soBuoc=3,
           loi=['Chương trước con đã học. Tổng bằng trung bình cộng nhân số lượng.',
                'Ở đây ba mươi lăm nhân hai bằng bảy mươi.']),
        _c('so_do_doan', 'Có tổng rồi thì làm như cũ', be=BE, lon=LON,
           hienHieu=True, chuHieu='hiệu 10', chuTong='tổng 70',
           chuPhu='Số lớn 40, số bé 30.',
           loi=['Có tổng rồi thì làm như cũ. Số lớn bốn mươi, số bé ba mươi.']),
        _c('y_toan', 'Một kiểu giấu khác', 'Chu vi 48 m thì tổng dài và rộng là 24 m.',
           buoc=3, soBuoc=3,
           loi=['Còn một kiểu giấu nữa. Nếu đề cho chu vi hình chữ nhật.',
                'Chu vi bằng hai lần tổng chiều dài với chiều rộng, nên chia đôi là ra.']),
        _c('cong_thuc', 'Việc đầu tiên luôn là tìm tổng',
           congThuc='tổng = trung bình cộng × 2   ·   tổng = chu vi : 2',
           thay='35 × 2 = 70',
           loi=['Việc đầu tiên luôn là tìm tổng ra đã.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chưa có tổng thì chưa dùng được công thức',
           loi=['Con nhớ lại một lần nữa. Chưa có tổng thì chưa dùng được công thức.',
                'Đừng lấy nhầm trung bình cộng làm tổng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_giau_hieu(b):
    """⑤ Hiệu bị giấu — nấp trong CÂU CHỮ, không nấp trong con số."""
    return [
        _c('bia', 'Khi đề không cho sẵn hiệu', so_bai(b),
           loi=['Hôm nay đề giấu mất hiệu, và nó nấp trong câu chữ.']),
        _c('de_toan', 'Hai số tự nhiên liên tiếp có tổng bằng 71.', 'Tìm hai số.',
           loi=['Hai số tự nhiên liên tiếp có tổng bằng bảy mươi mốt.',
                'Hỏi hai số ấy là bao nhiêu.']),
        _c('y_toan', 'Đề không nói hiệu bằng mấy',
           'Nó chỉ nói hai số LIÊN TIẾP.', buoc=1, soBuoc=3,
           loi=['Đề không nói hiệu bằng mấy. Nó chỉ nói hai số liên tiếp.']),
        _c('y_toan', 'Dịch câu ấy ra', 'Liên tiếp nghĩa là hơn kém nhau đúng 1.',
           buoc=2, soBuoc=3,
           loi=['Hai số tự nhiên liên tiếp thì hơn kém nhau đúng một đơn vị.',
                'Vậy hiệu bằng một.']),
        _c('y_toan', 'Có hiệu rồi thì làm như cũ',
           'Số lớn = (71 + 1) : 2 = 36,  số bé = 35', buoc=3, soBuoc=3,
           loi=['Có hiệu rồi thì làm như cũ. Số lớn là ba mươi sáu, số bé là ba mươi lăm.']),
        _c('so_do_doan', 'Mấy kiểu nấp khác', be=8, lon=10,
           hienHieu=True, chuHieu='hiệu 2',
           chuPhu='Hai số chẵn liên tiếp thì hiệu là 2.',
           chuCuoi='Bớt số lớn 8 thì bằng nhau, nghĩa là hiệu bằng 8.',
           loi=['Hai số chẵn liên tiếp thì hiệu là hai, ví dụ tám và mười.',
                'Còn nói bớt số lớn đi tám thì bằng nhau, nghĩa là hiệu bằng tám.']),
        _c('cong_thuc', 'Dịch câu chữ thành con số',
           congThuc='liên tiếp = 1 · chẵn hoặc lẻ liên tiếp = 2 · bớt k thì bằng = k',
           thay='liên tiếp  ⟶  hiệu 1',
           loi=['Việc đầu tiên là dịch câu chữ của đề thành con số.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chuyển k từ số này sang số kia  ⟶  hiệu = 2 lần k',
           loi=['Con nhớ thêm một câu khó. Chuyển từ số lớn sang số bé.',
                'Thì bên này bớt đi, bên kia được thêm, nên hiệu bằng hai lần chỗ chuyển.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_cung_them(b):
    """⑥ Cùng thêm vào cả hai — hiệu đứng yên, và nhìn hình là thấy."""
    return [
        _c('bia', 'Cùng thêm vào cả hai số', so_bai(b),
           loi=['Hôm nay mình xem điều gì xảy ra khi cả hai số cùng lớn lên.']),
        _c('de_toan', 'Tổng tuổi hai anh em là 20, anh hơn em 4 tuổi.',
           'Sau 3 năm nữa mỗi người bao nhiêu tuổi?',
           loi=['Tổng số tuổi hai anh em là hai mươi. Anh hơn em bốn tuổi.',
                'Hỏi sau ba năm nữa mỗi người bao nhiêu tuổi.']),
        _c('so_do_doan', 'Sơ đồ hiện nay', be=8, lon=12,
           hienHieu=True, chuHieu='hiệu 4', chuTong='tổng 20',
           loi=['Vẽ sơ đồ hiện nay. Khúc dôi ra là bốn, ngoặc ngoài là hai mươi.']),
        _c('so_do_doan', 'Sau 3 năm, CẢ HAI đoạn cùng dài thêm 3', be=11, lon=15,
           hienHieu=True, chuHieu='hiệu vẫn 4', chuTong='tổng 26',
           chuPhu='Khúc dôi ra y nguyên!',
           loi=['Sau ba năm, cả hai đoạn cùng dài thêm ba.',
                'Nhưng khúc dôi ra vẫn như cũ. Anh vẫn hơn em bốn tuổi.']),
        _c('y_toan', 'Hiệu không bao giờ đổi', 'Vì hai đoạn cùng dài thêm như nhau.',
           buoc=1, soBuoc=3,
           loi=['Hiệu tuổi không bao giờ đổi, vì hai đoạn cùng dài thêm như nhau.']),
        _c('y_toan', 'Nhưng tổng thì tăng gấp đôi phần thêm',
           'Mỗi người thêm 3, hai người nên tổng thêm 6.', buoc=2, soBuoc=3,
           loi=['Nhưng tổng thì tăng. Mỗi người thêm ba tuổi, hai người nên tổng thêm sáu.',
                'Tổng mới là hai mươi sáu.']),
        _c('y_toan', 'Bây giờ mới tính', 'Anh = (26 + 4) : 2 = 15,  em = 11',
           buoc=3, soBuoc=3,
           loi=['Bây giờ mới tính. Anh mười lăm tuổi, em mười một tuổi.']),
        _c('cong_thuc', 'Cùng thêm vào cả hai số',
           congThuc='hiệu KHÔNG đổi  ·  tổng tăng thêm 2 lần phần thêm',
           thay='20 + 3 × 2 = 26',
           loi=['Cùng thêm vào cả hai số thì hiệu không đổi, còn tổng tăng hai lần phần thêm.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hiệu tuổi KHÔNG bao giờ đổi',
           loi=['Con nhớ lại một lần nữa. Hiệu tuổi không bao giờ đổi.',
                'Bố hơn con bao nhiêu tuổi thì mãi mãi hơn bấy nhiêu.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_ba_so(b):
    """⑦ Ba số — vẫn cách nghĩ cũ, chỉ khác là chia BA."""
    return [
        _c('bia', 'Ba số biết tổng và hai hiệu', so_bai(b),
           loi=['Hôm nay có ba số chứ không phải hai.']),
        _c('de_toan', 'Ba số có tổng 90. Số hai hơn số một 5, số ba hơn số một 10.',
           'Tìm ba số.',
           loi=['Ba số có tổng chín mươi.',
                'Số thứ hai hơn số thứ nhất năm, số thứ ba hơn số thứ nhất mười.']),
        _c('y_toan', 'Vẽ ba đoạn', 'Đoạn thứ nhất ngắn nhất.', buoc=1, soBuoc=4,
           loi=['Vẽ ba đoạn. Đoạn thứ nhất ngắn nhất.',
                'Đoạn hai dôi ra năm, đoạn ba dôi ra mười.']),
        _c('so_do_doan', 'Đoạn hai dôi ra 5', be=25, lon=30,
           hienHieu=True, chuHieu='5', nhanBe='Số một', nhanLon='Số hai',
           loi=['Đoạn thứ hai dôi ra năm so với đoạn thứ nhất.']),
        _c('so_do_doan', 'Đoạn ba dôi ra 10', be=25, lon=35,
           hienHieu=True, chuHieu='10', nhanBe='Số một', nhanLon='Số ba',
           loi=['Đoạn thứ ba dôi ra mười so với đoạn thứ nhất.']),
        _c('y_toan', 'Cắt cho ba đoạn bằng nhau', 'Cắt đi 5 và 10, tất cả là 15.',
           buoc=2, soBuoc=4,
           loi=['Cắt bỏ khúc năm và khúc mười. Tất cả là mười lăm.',
                'Bây giờ ba đoạn bằng nhau, mỗi đoạn bằng số thứ nhất.']),
        _c('y_toan', 'Tổng còn lại', '90 − 15 = 75', buoc=3, soBuoc=4,
           loi=['Tổng còn bảy mươi lăm.']),
        _c('y_toan', 'Chia cho MẤY', 'Còn ba đoạn bằng nhau nên chia ba.',
           buoc=4, soBuoc=4,
           loi=['Còn ba đoạn bằng nhau nên chia ba, chứ không chia đôi như bài hai số.',
                'Bảy mươi lăm chia ba bằng hai mươi lăm.']),
        _c('cong_thuc', 'Cách làm bài ba số',
           congThuc='cắt hết khúc dôi ra  ⟶  chia cho SỐ ĐOẠN',
           thay='(90 − 15) : 3 = 25',
           loi=['Cắt hết khúc dôi ra rồi chia cho số đoạn.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='có mấy đoạn bằng nhau thì chia cho bấy nhiêu',
           loi=['Con nhớ lại một lần nữa. Có mấy đoạn bằng nhau thì chia cho bấy nhiêu.',
                'Rồi cộng khúc dôi ra để tìm lại hai số kia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 7 · BẢY KỊCH BẢN — TỔNG - TỈ, HIỆU - TỈ
# ═══════════════════════════════════════════════════════════════════════════
# Bộ neo: hai số 20 và 50. Tổng 70 (đúng tổng chương 6, bé vừa quen), hiệu 30, tỉ số
# 2 trên 5 — nên tổng gồm 7 phần, hiệu gồm 3 phần, mỗi phần 10.
#
# Nhờ thế bài tổng - tỉ và bài hiệu - tỉ dùng CHUNG MỘT BỨC TRANH, chỉ khác chỗ nhìn.
# Đó là lý do hai bài đặt liền nhau, đúng cách chương 6 ghép số lớn với số bé.
TI_BE, TI_LON = 2, 5
SO_BE, SO_LON = 20, 50


def kb_ti_la_gi(b):
    """① Tỉ số là gì — bài KHÁI NIỆM, không một phép tính nào."""
    return [
        _c('bia', 'Tỉ số là gì', so_bai(b),
           loi=['Hôm nay mình học cách đọc tỉ số trên sơ đồ.']),
        _c('so_do_doan', 'Tỉ số 2 trên 5', be=SO_BE, lon=SO_LON,
           phanBe=TI_BE, phanLon=TI_LON,
           chuPhu='Số bé 2 phần, số lớn 5 phần.',
           loi=['Tỉ số hai trên năm nghĩa là số bé gồm hai phần, số lớn gồm năm phần.']),
        _c('y_toan', 'Điều quan trọng nhất', 'MỌI phần đều bằng nhau.',
           buoc=1, soBuoc=3,
           loi=['Điều quan trọng nhất là mọi phần đều bằng nhau.',
                'Vẽ phần to phần nhỏ thì sơ đồ nói sai tỉ số.']),
        _c('so_do_doan', 'Gộp lại thì được mấy phần', be=SO_BE, lon=SO_LON,
           phanBe=TI_BE, phanLon=TI_LON, chuTong='cả thảy 7 phần',
           chuPhu='2 + 5 = 7 phần.',
           loi=['Gộp cả hai lại thì được bảy phần.']),
        _c('y_toan', 'Còn chênh nhau mấy phần', '5 − 2 = 3 phần', buoc=2, soBuoc=3,
           loi=['Còn đoạn dài hơn đoạn ngắn ba phần.']),
        _c('y_toan', 'Tỉ số nói SỐ PHẦN, không nói giá trị',
           'Mỗi phần bằng bao nhiêu cũng được.', buoc=3, soBuoc=3,
           loi=['Tỉ số chỉ nói số phần, chưa nói mỗi phần bằng bao nhiêu.',
                'Nếu mỗi phần bằng mười thì hai số là hai mươi và năm mươi.']),
        _c('cong_thuc', 'Đọc một tỉ số',
           congThuc='2 : 5  ⟶  số bé 2 phần · số lớn 5 phần · mọi phần bằng nhau',
           thay='gộp 7 phần · chênh 3 phần',
           loi=['Tỉ số hai trên năm cho ta ba điều. Số phần của mỗi số, và mọi phần bằng nhau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='MỌI phần đều bằng nhau',
           loi=['Con nhớ lại một lần nữa. Mọi phần trên sơ đồ đều phải bằng nhau.',
                'Vẽ đúng được sơ đồ là con đã làm xong nửa bài.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tong_ti(b):
    """② Tổng - tỉ — chia TỔNG cho TỔNG SỐ PHẦN."""
    return [
        _c('bia', 'Bài toán tổng - tỉ', so_bai(b),
           loi=['Hôm nay đề cho thêm tổng của hai số.']),
        _c('so_do_doan', 'Tổng 70, tỉ số 2 trên 5', be=SO_BE, lon=SO_LON,
           phanBe=TI_BE, phanLon=TI_LON, chuTong='tổng 70',
           loi=['Hai số có tổng bảy mươi và tỉ số hai trên năm. Tìm hai số.']),
        _c('y_toan', 'Đếm cả thảy mấy phần', '2 + 5 = 7 phần', buoc=1, soBuoc=3,
           loi=['Đếm cả thảy có bảy phần. Bảy phần ấy gộp lại đúng bằng bảy mươi.']),
        _c('y_toan', 'Tìm một phần', '70 : 7 = 10', buoc=2, soBuoc=3,
           loi=['Bảy phần là bảy mươi, nên một phần là mười.']),
        _c('so_do_doan', 'Mỗi phần bằng 10', be=SO_BE, lon=SO_LON,
           phanBe=TI_BE, phanLon=TI_LON,
           chuPhu='Số bé 2 phần là 20. Số lớn 5 phần là 50.',
           loi=['Số bé có hai phần nên bằng hai mươi. Số lớn có năm phần nên bằng năm mươi.']),
        _c('y_toan', 'Thử lại', '20 + 50 = 70', buoc=3, soBuoc=3,
           loi=['Thử lại. Hai mươi cộng năm mươi bằng bảy mươi, đúng bằng tổng.']),
        _c('cong_thuc', 'Bài toán tổng - tỉ',
           congThuc='một phần = tổng : TỔNG SỐ PHẦN',
           thay='70 : 7 = 10',
           loi=['Một phần bằng tổng chia cho tổng số phần.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia cho TỔNG SỐ PHẦN, không chia cho 2 hay 5',
           loi=['Con nhớ lại một lần nữa. Chia cho tổng số phần, không chia riêng cho '
                'số phần của một bên.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_hieu_ti(b):
    """③ Hiệu - tỉ — CÙNG bức tranh, chỉ khác chỗ nhìn."""
    return [
        _c('bia', 'Bài toán hiệu - tỉ', so_bai(b),
           loi=['Hôm nay đề không cho tổng nữa, mà cho hiệu.']),
        _c('so_do_doan', 'Vẫn tỉ số 2 trên 5, nhưng cho HIỆU là 30',
           be=SO_BE, lon=SO_LON, phanBe=TI_BE, phanLon=TI_LON,
           hienHieu=True, chuHieu='hiệu 30',
           loi=['Vẫn tỉ số hai trên năm. Nhưng lần này đề cho hiệu bằng ba mươi.']),
        _c('y_toan', 'Nhìn phần chênh', '5 − 2 = 3 phần', buoc=1, soBuoc=3,
           loi=['Đoạn dài hơn đoạn ngắn ba phần. Ba phần ấy chính là hiệu.']),
        _c('y_toan', 'Tìm một phần', '30 : 3 = 10', buoc=2, soBuoc=3,
           loi=['Ba phần là ba mươi, nên một phần là mười.']),
        _c('so_do_doan', 'Vẫn ra hai số ấy', be=SO_BE, lon=SO_LON,
           phanBe=TI_BE, phanLon=TI_LON, chuTong='tổng 70',
           chuPhu='Số bé 20, số lớn 50 — đúng như bài hôm qua.',
           loi=['Vẫn ra hai mươi và năm mươi, đúng như bài hôm qua.',
                'Vì đó cùng một bức tranh, chỉ khác chỗ mình nhìn vào.']),
        _c('y_toan', 'Có tổng thì khác, có hiệu thì khác',
           'Tổng ứng với 7 phần. Hiệu ứng với 3 phần.', buoc=3, soBuoc=3,
           loi=['Tổng ứng với cả bảy phần. Còn hiệu chỉ ứng với ba phần chênh nhau.']),
        _c('cong_thuc', 'Bài toán hiệu - tỉ',
           congThuc='một phần = hiệu : SỐ PHẦN CHÊNH',
           thay='30 : 3 = 10',
           loi=['Một phần bằng hiệu chia cho số phần chênh nhau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='có tổng → chia tổng số phần · có hiệu → chia số phần chênh',
           loi=['Con nhớ lại một lần nữa. Có tổng thì chia tổng số phần.',
                'Có hiệu thì chia số phần chênh nhau. Chỉ khác đúng chỗ ấy.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_giau_ti(b):
    """④ Tỉ số bị giấu — bài ĐỌC HIỂU."""
    return [
        _c('bia', 'Khi đề giấu tỉ số', so_bai(b),
           loi=['Hôm nay đề không cho tỉ số bằng số, mà nói bằng lời.']),
        _c('de_toan', 'Khay có 40 chiếc bánh, số bánh nướng gấp rưỡi số bánh dẻo.',
           'Tính số bánh mỗi loại.',
           loi=['Khay có bốn mươi chiếc bánh. Số bánh nướng gấp rưỡi số bánh dẻo.',
                'Hỏi mỗi loại bao nhiêu chiếc.']),
        _c('y_toan', 'Gấp rưỡi nghĩa là gì', 'Là gấp một lần rưỡi.',
           buoc=1, soBuoc=3,
           loi=['Gấp rưỡi nghĩa là gấp một lần rưỡi.',
                'Chữ rưỡi ở đây là một nửa, không phải số năm.']),
        _c('so_do_doan', 'Dịch ra thành hai phần trên ba phần', be=2, lon=3,
           phanBe=2, phanLon=3, chuTong='tổng 40',
           chuPhu='Bánh dẻo 2 phần, bánh nướng 3 phần.',
           loi=['Nếu bánh dẻo là hai phần thì bánh nướng là ba phần.']),
        _c('y_toan', 'Bây giờ làm như cũ', '40 : 5 = 8', buoc=2, soBuoc=3,
           loi=['Cả thảy năm phần. Một phần là tám chiếc.']),
        _c('y_toan', 'Suy ra hai số', 'Bánh dẻo 16, bánh nướng 24', buoc=3, soBuoc=3,
           loi=['Bánh dẻo mười sáu chiếc, bánh nướng hai mươi tư chiếc.']),
        _c('cong_thuc', 'Dịch câu chữ thành tỉ số',
           congThuc='gấp rưỡi = 2 : 3   ·   gấp 3 lần = 1 : 3   ·   bằng hai phần ba = 2 : 3',
           thay='gấp rưỡi  ⟶  2 : 3',
           loi=['Việc đầu tiên là dịch câu chữ của đề thành hai con số.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='rưỡi = một nửa',
           loi=['Con nhớ lại một lần nữa. Chữ rưỡi nghĩa là một nửa.',
                'Gấp rưỡi là gấp một lần rưỡi, tức tỉ số hai trên ba.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_giau_tong_ti(b):
    """⑤ Tổng hoặc hiệu bị giấu — dùng lại đúng kỹ năng chương 6."""
    return [
        _c('bia', 'Khi đề giấu tổng hoặc hiệu', so_bai(b),
           loi=['Hôm nay đề giấu mất tổng, giống chương trước.']),
        _c('de_toan', 'Trung bình cộng của hai số là 35, số bé bằng hai phần năm số lớn.',
           'Tìm hai số.',
           loi=['Trung bình cộng của hai số là ba mươi lăm.',
                'Số bé bằng hai phần năm số lớn. Tìm hai số.']),
        _c('y_toan', 'Đề cho gì và thiếu gì', 'Có tỉ số rồi, nhưng chưa có tổng.',
           buoc=1, soBuoc=3,
           loi=['Đề cho tỉ số rồi, nhưng chưa cho tổng.']),
        _c('y_toan', 'Lôi tổng ra', '35 × 2 = 70', buoc=2, soBuoc=3,
           loi=['Chương trước con đã học. Tổng bằng trung bình cộng nhân hai.',
                'Ở đây được bảy mươi.']),
        _c('so_do_doan', 'Có tổng rồi thì làm như cũ', be=SO_BE, lon=SO_LON,
           phanBe=TI_BE, phanLon=TI_LON, chuTong='tổng 70',
           chuPhu='Một phần 10, hai số là 20 và 50.',
           loi=['Có tổng rồi thì làm như cũ. Một phần bằng mười.',
                'Hai số là hai mươi và năm mươi.']),
        _c('y_toan', 'Hiệu cũng bị giấu như thế',
           '"Mẹ hơn con 30 tuổi" chính là hiệu.', buoc=3, soBuoc=3,
           loi=['Hiệu cũng bị giấu theo cách tương tự.',
                'Nói mẹ hơn con ba mươi tuổi thì đó chính là hiệu.']),
        _c('cong_thuc', 'Thiếu gì thì lôi cái ấy ra trước',
           congThuc='tổng = trung bình cộng × 2   ·   tổng = chu vi : 2',
           thay='35 × 2 = 70',
           loi=['Thiếu gì thì lôi cái ấy ra trước đã.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đừng lấy trung bình cộng thay cho tổng',
           loi=['Con nhớ lại một lần nữa. Đừng lấy trung bình cộng thay cho tổng.',
                'Nó mới là số của một phần thôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_ba_so_ti(b):
    """⑥ Ba số theo tỉ — vẫn chia cho TỔNG SỐ PHẦN, chỉ nhiều đoạn hơn."""
    return [
        _c('bia', 'Ba số theo tỉ', so_bai(b),
           loi=['Hôm nay có ba số chứ không phải hai.']),
        _c('de_toan', 'Chia 90 quyển vở cho ba lớp theo tỉ số 2 : 3 : 4.',
           'Mỗi lớp được bao nhiêu quyển?',
           loi=['Chia chín mươi quyển vở cho ba lớp theo tỉ số hai, ba, bốn.']),
        _c('so_do_doan', 'Hai đoạn đầu', be=20, lon=30, phanBe=2, phanLon=3,
           nhanBe='Lớp một', nhanLon='Lớp hai',
           loi=['Lớp một hai phần, lớp hai ba phần.']),
        _c('so_do_doan', 'Thêm đoạn thứ ba', be=20, lon=40, phanBe=2, phanLon=4,
           nhanBe='Lớp một', nhanLon='Lớp ba',
           loi=['Lớp ba bốn phần. Mọi phần đều bằng nhau.']),
        _c('y_toan', 'Đếm cả thảy mấy phần', '2 + 3 + 4 = 9 phần', buoc=1, soBuoc=3,
           loi=['Đếm cả thảy có chín phần, chứ không phải ba.']),
        _c('y_toan', 'Tìm một phần', '90 : 9 = 10 quyển', buoc=2, soBuoc=3,
           loi=['Chín phần là chín mươi, nên một phần là mười quyển.']),
        _c('y_toan', 'Suy ra ba số', '20 · 30 · 40 quyển', buoc=3, soBuoc=3,
           loi=['Ba lớp được hai mươi, ba mươi và bốn mươi quyển.',
                'Cộng lại đúng chín mươi.']),
        _c('cong_thuc', 'Bài ba số theo tỉ',
           congThuc='một phần = tổng : TỔNG SỐ PHẦN',
           thay='90 : 9 = 10',
           loi=['Vẫn là tổng chia cho tổng số phần, chỉ khác là nhiều đoạn hơn.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia cho SỐ PHẦN, không chia cho số lớp',
           loi=['Con nhớ lại một lần nữa. Chia cho số phần, không chia cho số lớp.',
                'Ba lớp nhưng chín phần, vì mỗi lớp nhận số phần khác nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_noi_ti(b):
    """⑦ Nối hai tỉ số — bài khó nhất chương, một ý duy nhất."""
    return [
        _c('bia', 'Nối hai tỉ số', so_bai(b),
           loi=['Hôm nay đề cho hai tỉ số, và mình phải nối chúng lại.']),
        _c('de_toan', 'Ba bạn có 90 viên bi. An so với Bình là 2 : 3, Bình so với Cường '
                      'là 6 : 5.', 'Tìm số bi mỗi bạn.',
           loi=['Ba bạn có chín mươi viên bi.',
                'An so với Bình là hai trên ba. Bình so với Cường là sáu trên năm.']),
        _c('y_toan', 'Tìm mắt xích chung', 'Bình có mặt ở CẢ HAI tỉ số.',
           buoc=1, soBuoc=4,
           loi=['Bình có mặt ở cả hai tỉ số. Bình là mắt xích chung.']),
        _c('so_do_doan', 'Nhưng hai tỉ số đếm Bình khác nhau', be=3, lon=6,
           phanBe=3, phanLon=6, nhanBe='Bình ở tỉ số đầu', nhanLon='Bình ở tỉ số sau',
           chuPhu='Cùng một bạn Bình mà một bên 3 phần, một bên 6 phần.',
           loi=['Nhưng tỉ số đầu đếm Bình là ba phần, tỉ số sau đếm Bình là sáu phần.',
                'Cùng một bạn mà hai con số khác nhau thì chưa ghép được.']),
        _c('y_toan', 'Quy về cùng một loại phần',
           'Nhân tỉ số đầu với 2: An trên Bình thành 4 : 6', buoc=2, soBuoc=4,
           loi=['Nhân cả tỉ số đầu với hai thì Bình thành sáu phần.',
                'An trên Bình thành bốn trên sáu.']),
        _c('y_toan', 'Bây giờ nối được', 'An 4 phần, Bình 6 phần, Cường 5 phần',
           buoc=3, soBuoc=4,
           loi=['Bây giờ nối được. An bốn phần, Bình sáu phần, Cường năm phần.']),
        _c('y_toan', 'Làm như bài trước', '90 : 15 = 6 viên', buoc=4, soBuoc=4,
           loi=['Cả thảy mười lăm phần. Một phần là sáu viên.',
                'An hai mươi tư viên, Bình ba mươi sáu viên, Cường ba mươi viên.']),
        _c('cong_thuc', 'Cách nối hai tỉ số',
           congThuc='quy đại lượng chung về CÙNG một số phần, rồi mới ghép',
           thay='2 : 3  nhân 2  ⟶  4 : 6',
           loi=['Quy đại lượng chung về cùng một số phần, rồi mới ghép.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='nhân thì nhân CẢ HAI vế của tỉ số',
           loi=['Con nhớ lại một lần nữa. Nhân thì phải nhân cả hai vế của tỉ số.',
                'Nhân một vế thôi là tỉ số đổi hẳn, sai bài.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 8 · BÀI TOÁN LỜI VĂN — ĐỢT MỘT, NĂM KỊCH BẢN
# ═══════════════════════════════════════════════════════════════════════════
# Chương này KHÔNG có một bộ neo chung, vì mỗi bài là một phương pháp riêng. Neo theo
# CẶP: hai bài tuổi dùng mẹ 30 con 6 (hiệu 24); hai bài làm chung dùng anh 6 giờ em
# 12 giờ (việc chia 12 phần); bài tính ngược đứng riêng với số 10.


def kb_tuoi_mot(b):
    """① Tuổi một mốc — ý duy nhất: đây là bài CŨ mặc áo mới."""
    return [
        _c('bia', 'Bài toán tuổi ở một thời điểm', so_bai(b),
           loi=['Hôm nay mình gặp bài toán tuổi, và có một tin vui.']),
        _c('de_toan', 'Tổng số tuổi hai mẹ con là 36. Mẹ hơn con 24 tuổi.',
           'Tính tuổi mỗi người.',
           loi=['Tổng số tuổi hai mẹ con là ba mươi sáu. Mẹ hơn con hai mươi bốn tuổi.']),
        _c('y_toan', 'Che chữ tuổi đi mà xem',
           'Tổng hai số là 36, số này hơn số kia 24.', buoc=1, soBuoc=3,
           loi=['Con thử che chữ tuổi đi rồi đọc lại.',
                'Tổng hai số là ba mươi sáu, số này hơn số kia hai mươi bốn.']),
        _c('y_toan', 'Đây là bài con đã giải rồi', 'Bài tổng - hiệu của chương trước.',
           buoc=2, soBuoc=3,
           loi=['Đây chính là bài tổng trừ hiệu con đã giải rất thạo ở chương trước.']),
        _c('so_do_doan', 'Vẫn sơ đồ ấy', be=6, lon=30,
           hienHieu=True, chuHieu='hiệu 24', chuTong='tổng 36',
           nhanBe='Tuổi con', nhanLon='Tuổi mẹ',
           loi=['Vẫn vẽ hai đoạn như cũ. Khúc dôi ra là hai mươi bốn, ngoặc ngoài là '
                'ba mươi sáu.']),
        _c('y_toan', 'Dùng công thức cũ', 'Mẹ = (36 + 24) : 2 = 30,  con = 6',
           buoc=3, soBuoc=3,
           loi=['Tuổi mẹ bằng ba mươi sáu cộng hai mươi bốn rồi chia đôi, được ba mươi.',
                'Tuổi con là sáu. Cộng lại đúng ba mươi sáu, trừ nhau đúng hai mươi bốn.']),
        _c('cong_thuc', 'Bài toán tuổi một mốc',
           congThuc='che chữ "tuổi" đi  ⟶  là bài tổng - hiệu hoặc tổng - tỉ',
           thay='(36 + 24) : 2 = 30',
           loi=['Bài toán tuổi ở một thời điểm chính là bài cũ mặc áo mới.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='không có phép nào mới cả',
           loi=['Con nhớ lại một lần nữa. Không có phép nào mới cả.',
                'Thấy chữ tuổi thì đừng hoảng, cứ che nó đi rồi đọc lại đề.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tuoi_hai(b):
    """② Tuổi hai mốc — chìa khoá: hiệu tuổi không đổi."""
    return [
        _c('bia', 'Bài toán tuổi ở hai thời điểm', so_bai(b),
           loi=['Hôm nay bài toán tuổi có hai thời điểm, và cần biết một điều.']),
        _c('de_toan', 'Hiện nay mẹ 30 tuổi, con 6 tuổi.',
           'Sau bao nhiêu năm nữa tuổi mẹ gấp 3 lần tuổi con?',
           loi=['Hiện nay mẹ ba mươi tuổi, con sáu tuổi.',
                'Hỏi sau bao nhiêu năm nữa thì tuổi mẹ gấp ba lần tuổi con.']),
        _c('y_toan', 'Tìm cái KHÔNG đổi', 'Hiệu tuổi: 30 − 6 = 24', buoc=1, soBuoc=4,
           loi=['Việc đầu tiên là tìm cái không đổi. Hiệu tuổi là hai mươi bốn.',
                'Mỗi năm cả hai cùng thêm một tuổi nên hiệu này đứng yên mãi.']),
        _c('so_do_doan', 'Lúc mẹ gấp 3 lần con', be=12, lon=36,
           phanBe=1, phanLon=3, hienHieu=True, chuHieu='vẫn là 24',
           nhanBe='Tuổi con', nhanLon='Tuổi mẹ',
           loi=['Lúc ấy tuổi mẹ gấp ba lần tuổi con, nhưng hiệu vẫn là hai mươi bốn.']),
        _c('y_toan', 'Đây là bài hiệu - tỉ', 'Phần chênh 2 phần, ứng với 24',
           buoc=2, soBuoc=4,
           loi=['Đây chính là bài hiệu trừ tỉ. Phần chênh là hai phần, ứng với hai '
                'mươi bốn.']),
        _c('y_toan', 'Tuổi lúc ấy', 'Một phần 12 · con 12 tuổi · mẹ 36 tuổi',
           buoc=3, soBuoc=4,
           loi=['Một phần là mười hai. Con mười hai tuổi, mẹ ba mươi sáu tuổi.']),
        _c('y_toan', 'Sau bao nhiêu năm', 'Con từ 6 lên 12, vậy sau 6 năm',
           buoc=4, soBuoc=4,
           loi=['Con từ sáu tuổi lên mười hai tuổi, vậy sau sáu năm nữa.']),
        _c('cong_thuc', 'Điều quan trọng nhất của bài toán tuổi',
           congThuc='hiệu tuổi KHÔNG đổi — nó nối hai thời điểm',
           thay='30 − 6 = 24, mãi mãi',
           loi=['Hiệu tuổi không bao giờ đổi, và chính vì thế nó nối được hai thời điểm.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tổng và tỉ số thì đổi · hiệu thì không',
           loi=['Con nhớ lại một lần nữa. Tổng tuổi đổi, tỉ số tuổi đổi.',
                'Chỉ hiệu tuổi là đứng yên. Gặp bài hai thời điểm thì tìm nó trước.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_lam_chung(b):
    """③ Làm chung — chia việc thành phần, KHÔNG dùng phân số."""
    return [
        _c('bia', 'Làm chung công việc', so_bai(b),
           loi=['Hôm nay hai người cùng làm một việc, xem mấy giờ thì xong.']),
        _c('de_toan', 'Anh làm một mình xong trong 6 giờ, em xong trong 12 giờ.',
           'Hai anh em làm chung thì mấy giờ xong?',
           loi=['Anh làm một mình xong việc trong sáu giờ.',
                'Em làm một mình xong việc ấy trong mười hai giờ.']),
        _c('y_toan', 'Chia công việc thành phần',
           'Chọn số chia hết cho cả 6 và 12 — lấy 12 phần.', buoc=1, soBuoc=4,
           loi=['Mình chia công việc thành những phần bằng nhau.',
                'Chọn số chia hết cho cả sáu và mười hai, gọn nhất là mười hai phần.']),
        _c('y_toan', 'Mỗi giờ mỗi người làm mấy phần',
           'Anh 12 : 6 = 2 phần · em 12 : 12 = 1 phần', buoc=2, soBuoc=4,
           loi=['Anh xong mười hai phần trong sáu giờ, nên mỗi giờ anh làm hai phần.',
                'Em xong mười hai phần trong mười hai giờ, nên mỗi giờ em làm một phần.']),
        _c('y_toan', 'Làm chung một giờ được mấy phần', '2 + 1 = 3 phần',
           buoc=3, soBuoc=4,
           loi=['Làm chung thì mỗi giờ được ba phần.']),
        _c('nhom_deu', 'Cả việc 12 phần, mỗi giờ 3 phần', tong=12, moiNhom=3,
           chuPhu='12 chia 3 được 4 nhóm — tức 4 giờ.',
           chuCuoi='Mỗi nhóm là một giờ làm chung.',
           loi=['Cả việc mười hai phần, mỗi giờ làm ba phần.',
                'Mười hai chia ba được bốn, vậy bốn giờ thì xong.']),
        _c('y_toan', 'Soi lại cho chắc', 'Làm chung phải NHANH HƠN người nhanh nhất.',
           buoc=4, soBuoc=4,
           loi=['Soi lại cho chắc. Anh một mình đã xong trong sáu giờ.',
                'Làm chung ra bốn giờ, nhanh hơn, nên hợp lý.']),
        _c('cong_thuc', 'Cách làm bài làm chung',
           congThuc='chia việc thành phần  ⟶  cộng số phần mỗi giờ',
           thay='12 : 3 = 4 giờ',
           loi=['Chia việc thành phần rồi cộng số phần mỗi giờ.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='KHÔNG cộng thời gian — chỉ cộng số phần',
           loi=['Con nhớ lại một lần nữa. Không cộng thời gian được.',
                'Chỉ cộng số phần làm được mỗi giờ. Và làm chung phải nhanh hơn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_mot_nguoi_nghi(b):
    """④ Làm chung rồi một người nghỉ — theo dõi số phần còn lại."""
    return [
        _c('bia', 'Làm chung rồi một người nghỉ', so_bai(b),
           loi=['Hôm nay hai người làm chung một lúc rồi một người phải nghỉ.']),
        _c('de_toan', 'Anh 6 giờ, em 12 giờ. Làm chung 2 giờ thì anh nghỉ.',
           'Em làm nốt mất mấy giờ?',
           loi=['Anh xong trong sáu giờ, em xong trong mười hai giờ.',
                'Hai anh em làm chung hai giờ thì anh phải nghỉ, em làm nốt.']),
        _c('y_toan', 'Vẫn chia việc thành 12 phần',
           'Anh 2 phần · em 1 phần · chung 3 phần mỗi giờ', buoc=1, soBuoc=4,
           loi=['Vẫn chia việc thành mười hai phần như bài trước.',
                'Làm chung mỗi giờ được ba phần.']),
        _c('nhom_deu', 'Hai giờ làm chung được 6 phần', tong=12, moiNhom=6,
           chuPhu='3 phần mỗi giờ, hai giờ là 6 phần.',
           chuCuoi='Nửa việc đã xong.',
           loi=['Ba phần mỗi giờ, hai giờ là sáu phần. Nửa việc đã xong.']),
        _c('y_toan', 'Còn lại mấy phần', '12 − 6 = 6 phần', buoc=2, soBuoc=4,
           loi=['Cả việc mười hai phần, đã làm sáu phần, còn sáu phần.']),
        _c('y_toan', 'Bây giờ còn mấy người làm', 'Chỉ còn em — 1 phần mỗi giờ.',
           buoc=3, soBuoc=4,
           loi=['Bây giờ anh đã nghỉ, chỉ còn em làm, mỗi giờ một phần.',
                'Đây là chỗ hay quên nhất.']),
        _c('y_toan', 'Em làm nốt mất mấy giờ', '6 : 1 = 6 giờ', buoc=4, soBuoc=4,
           loi=['Còn sáu phần, mỗi giờ một phần, nên em mất sáu giờ nữa.']),
        _c('cong_thuc', 'Cách làm bài một người nghỉ',
           congThuc='số phần đã làm  ⟶  số phần còn lại  ⟶  chia cho người CÒN LẠI',
           thay='(12 − 6) : 1 = 6 giờ',
           loi=['Đếm số phần đã làm, rồi số phần còn lại, rồi chia cho người còn lại.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='bớt một người thì SỐ PHẦN MỖI GIỜ cũng đổi',
           loi=['Con nhớ lại một lần nữa. Bớt một người thì số phần mỗi giờ cũng đổi.',
                'Dùng lại con số cũ là vẫn tính như còn cả hai người.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tinh_nguoc(b):
    """⑤ Tính ngược — một ý duy nhất: đi lùi thì ĐỔI PHÉP."""
    return [
        _c('bia', 'Tính ngược từ cuối', so_bai(b),
           loi=['Hôm nay đề chỉ cho biết kết quả cuối cùng, và hỏi số ban đầu.']),
        _c('de_toan', 'Nghĩ một số, nhân 2, cộng 10, trừ 4 thì được 26.',
           'Tìm số đã nghĩ.',
           loi=['Nghĩ một số, nhân với hai, rồi cộng mười, rồi trừ bốn thì được hai '
                'mươi sáu.']),
        _c('y_toan', 'Đi xuôi thì chịu', 'Vì chưa biết bắt đầu từ số nào.',
           buoc=1, soBuoc=4,
           loi=['Đi xuôi thì chịu, vì chưa biết bắt đầu từ số nào.']),
        _c('y_toan', 'Nên đi lùi từ số cuối', '26 + 4 = 30', buoc=2, soBuoc=4,
           loi=['Nên mình đi lùi từ số cuối. Bước cuối là trừ bốn.',
                'Đi lùi thì đổi thành cộng bốn, được ba mươi.']),
        _c('y_toan', 'Lùi tiếp', '30 − 10 = 20', buoc=3, soBuoc=4,
           loi=['Trước đó là cộng mười, đi lùi thì đổi thành trừ mười, được hai mươi.']),
        _c('y_toan', 'Lùi nốt bước đầu', '20 : 2 = 10', buoc=4, soBuoc=4,
           loi=['Đầu tiên là nhân hai, đi lùi thì đổi thành chia hai, được mười.']),
        _c('y_toan', 'Thử lại bằng cách đi xuôi', '10 × 2 = 20 · + 10 = 30 · − 4 = 26',
           buoc=4, soBuoc=4,
           loi=['Thử lại. Mười nhân hai bằng hai mươi, cộng mười bằng ba mươi, trừ bốn '
                'bằng hai mươi sáu. Đúng bằng đề cho.']),
        _c('cong_thuc', 'Đi lùi thì ĐỔI PHÉP',
           congThuc='cộng ⟷ trừ    ·    nhân ⟷ chia',
           thay='26 + 4 = 30',
           loi=['Đi lùi thì đổi phép. Cộng thành trừ, nhân thành chia.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đi lùi thì làm NGƯỢC, từ bước CUỐI về bước đầu',
           loi=['Con nhớ lại một lần nữa. Đi lùi thì làm từ bước cuối ngược về bước đầu.',
                'Giữ nguyên phép là đi sai hướng, càng đi càng xa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ── chương 8 · đợt hai, năm bài cuối ──


def kb_gia_thiet(b):
    """⑥ Giả thiết tạm — đoán bừa rồi sửa dần."""
    return [
        _c('bia', 'Giả thiết tạm', so_bai(b),
           loi=['Hôm nay mình học một cách rất lạ mà rất hiệu quả.']),
        _c('de_toan', 'Vừa gà vừa chó có 36 con, đếm được 100 cái chân.',
           'Tính số con mỗi loại.',
           loi=['Vừa gà vừa chó có ba mươi sáu con, đếm được một trăm cái chân.']),
        _c('y_toan', 'Đoán bừa cho dễ tính', 'Giả sử tất cả 36 con đều là gà.',
           buoc=1, soBuoc=4,
           loi=['Mình cứ đoán bừa. Giả sử tất cả ba mươi sáu con đều là gà.']),
        _c('y_toan', 'Đếm chân theo giả thiết ấy', '36 × 2 = 72 chân',
           buoc=2, soBuoc=4,
           loi=['Gà hai chân, nên ba mươi sáu con có bảy mươi hai chân.']),
        _c('y_toan', 'Xem lệch bao nhiêu', '100 − 72 = 28 chân còn thiếu',
           buoc=3, soBuoc=4,
           loi=['Đề nói một trăm chân, mà đoán ra bảy mươi hai. Thiếu hai mươi tám chân.']),
        _c('nhom_deu', 'Đổi một con gà thành chó thì thêm 2 chân', tong=28, moiNhom=2,
           chuPhu='28 chân thiếu, mỗi lần đổi thêm 2 chân.',
           chuCuoi='Vậy phải đổi 14 con.',
           loi=['Đổi một con gà thành chó thì thêm hai chân.',
                'Thiếu hai mươi tám chân nên phải đổi mười bốn con.']),
        _c('y_toan', 'Đáp số', '14 con chó và 22 con gà', buoc=4, soBuoc=4,
           loi=['Có mười bốn con chó và hai mươi hai con gà.',
                'Thử lại đúng một trăm chân.']),
        _c('cong_thuc', 'Cách làm giả thiết tạm',
           congThuc='số cần đổi = phần lệch : lệch mỗi lần đổi',
           thay='28 : 2 = 14 con',
           loi=['Số cần đổi bằng phần lệch chia cho phần lệch mỗi lần đổi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đừng quên CHIA cho phần lệch mỗi lần',
           loi=['Con nhớ lại một lần nữa. Đừng quên chia cho phần lệch mỗi lần đổi.',
                'Lấy thẳng hai mươi tám là tưởng mỗi lần đổi chỉ thêm một chân.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_khu(b):
    """⑦ Khử — trừ hai lần mua cho một thứ biến mất."""
    return [
        _c('bia', 'Phương pháp khử', so_bai(b),
           loi=['Hôm nay mình làm cho một thứ trong bài biến mất.']),
        _c('de_toan', 'Mua 3 bút và 2 vở hết 22 nghìn. Mua 3 bút và 5 vở hết 37 nghìn.',
           'Tính giá một bút và một vở.',
           loi=['Mua ba bút và hai vở hết hai mươi hai nghìn đồng.',
                'Mua ba bút và năm vở hết ba mươi bảy nghìn đồng.']),
        _c('y_toan', 'Tìm phần giống HỆT nhau', 'Cả hai lần đều mua đúng 3 bút.',
           buoc=1, soBuoc=4,
           loi=['Nhìn kỹ thì cả hai lần đều mua đúng ba bút. Phần ấy giống hệt nhau.']),
        _c('y_toan', 'Trừ hai dòng cho nhau', 'Ba bút biến mất.', buoc=2, soBuoc=4,
           loi=['Lấy dòng dưới trừ dòng trên thì ba bút biến mất.']),
        _c('y_toan', 'Còn lại gì', '5 − 2 = 3 vở  ·  37 − 22 = 15 nghìn',
           buoc=3, soBuoc=4,
           loi=['Còn lại ba vở, và tiền còn mười lăm nghìn.',
                'Nhớ trừ cả hai vế, không chỉ trừ số vở.']),
        _c('y_toan', 'Tìm giá một vở', '15 : 3 = 5 nghìn', buoc=4, soBuoc=4,
           loi=['Ba vở hết mười lăm nghìn nên một vở là năm nghìn đồng.']),
        _c('y_toan', 'Quay về tìm giá bút', '22 − 10 = 12,  rồi 12 : 3 = 4 nghìn',
           buoc=4, soBuoc=4,
           loi=['Hai vở hết mười nghìn, nên ba bút hết mười hai nghìn.',
                'Một bút là bốn nghìn đồng.']),
        _c('cong_thuc', 'Phương pháp khử',
           congThuc='hai lần mua có phần GIỐNG HỆT  ⟶  trừ hai dòng',
           thay='37 − 22 = 15 nghìn cho 3 vở',
           loi=['Hai lần mua có phần giống hệt thì trừ hai dòng cho nhau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='trừ thì trừ CẢ HAI VẾ',
           loi=['Con nhớ lại một lần nữa. Trừ thì trừ cả hai vế.',
                'Bớt vở thì tiền cũng bớt theo, không thì hai bên hết bằng nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_the(b):
    """⑧ Thế — đổi hết về một loại nhờ câu quy đổi."""
    return [
        _c('bia', 'Phương pháp thế', so_bai(b),
           loi=['Hôm nay mình đổi hết mọi thứ về cùng một loại.']),
        _c('de_toan', 'Biết 2 hộp sữa giá bằng 3 gói bánh. Mua 4 hộp sữa và 6 gói bánh '
                      'hết 72 nghìn.', 'Tính giá mỗi thứ.',
           loi=['Biết hai hộp sữa giá bằng ba gói bánh.',
                'Mua bốn hộp sữa và sáu gói bánh hết bảy mươi hai nghìn đồng.']),
        _c('y_toan', 'Đây là câu quy đổi', '2 hộp sữa = 3 gói bánh', buoc=1, soBuoc=4,
           loi=['Câu hai hộp sữa bằng ba gói bánh cho phép mình đổi qua đổi lại.']),
        _c('y_toan', 'Đổi 4 hộp sữa thành bánh', 'Gấp đôi bên này thì gấp đôi bên kia.',
           buoc=2, soBuoc=4,
           loi=['Bốn hộp sữa gấp đôi hai hộp sữa, nên bằng gấp đôi ba gói bánh.',
                'Tức là sáu gói bánh.']),
        _c('y_toan', 'Bây giờ tất cả là bánh', '6 + 6 = 12 gói bánh hết 72 nghìn',
           buoc=3, soBuoc=4,
           loi=['Cả lần mua thành mười hai gói bánh, hết bảy mươi hai nghìn.']),
        _c('y_toan', 'Tìm giá mỗi thứ', 'Bánh 6 nghìn · sữa 9 nghìn', buoc=4, soBuoc=4,
           loi=['Một gói bánh là sáu nghìn đồng.',
                'Hai hộp sữa bằng ba gói bánh, tức mười tám nghìn, nên một hộp sữa là '
                'chín nghìn đồng.']),
        _c('cong_thuc', 'Phương pháp thế',
           congThuc='có câu QUY ĐỔI  ⟶  đổi hết về một loại',
           thay='4 hộp sữa  ⟶  6 gói bánh',
           loi=['Có câu quy đổi thì đổi hết về một loại rồi hãy tính.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='gấp mấy bên này thì gấp bấy bên kia',
           loi=['Con nhớ lại một lần nữa. Gấp mấy lần bên này thì gấp bấy nhiêu bên kia.',
                'Khử cần hai thứ giống hệt, còn thế cần một câu quy đổi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_ven(b):
    """⑨ Sơ đồ Ven — phần chồng nhau bị đếm hai lần."""
    return [
        _c('bia', 'Sơ đồ Ven', so_bai(b),
           loi=['Hôm nay mình vẽ hai vòng tròn chồng lên nhau.']),
        _c('de_toan', 'Lớp 38 bạn: 25 thích bóng đá, 18 thích cờ vua, 8 thích cả hai.',
           'Hỏi bao nhiêu bạn không thích môn nào?',
           loi=['Lớp có ba mươi tám bạn. Hai mươi lăm bạn thích bóng đá.',
                'Mười tám bạn thích cờ vua, và tám bạn thích cả hai môn.']),
        _c('y_toan', 'Cộng thẳng thì sai', '25 + 18 = 43, mà lớp chỉ có 38 bạn.',
           buoc=1, soBuoc=3,
           loi=['Cộng thẳng được bốn mươi ba, mà lớp chỉ có ba mươi tám bạn.',
                'Số bạn không thể nhiều hơn cả lớp.']),
        _c('so_do_ven', 'Vẽ ra thì thấy ngay', tenA='Thích bóng đá', tenB='Thích cờ vua',
           chiA=17, caHai=8, chiB=10,
           chuGiao='8 bạn thích CẢ HAI nằm ở phần chồng nhau',
           chuPhu='Phần ấy bị đếm hai lần.',
           loi=['Vẽ hai vòng chồng nhau thì thấy ngay.',
                'Tám bạn thích cả hai nằm ở phần chồng, nên bị đếm hai lần.']),
        _c('y_toan', 'Trừ đi một lần', '25 + 18 − 8 = 35 bạn', buoc=2, soBuoc=3,
           loi=['Trừ đi một lần thì được ba mươi lăm bạn thích ít nhất một môn.']),
        _c('y_toan', 'Tìm số bạn không thích môn nào', '38 − 35 = 3 bạn',
           buoc=3, soBuoc=3,
           loi=['Cả lớp ba mươi tám bạn, nên có ba bạn không thích môn nào.']),
        _c('cong_thuc', 'Sơ đồ Ven hai vòng',
           congThuc='số thích ít nhất một môn = A + B − phần chung',
           thay='25 + 18 − 8 = 35',
           loi=['Số bạn thích ít nhất một môn bằng nhóm một cộng nhóm hai, trừ phần chung.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='phần chồng bị đếm HAI lần nên trừ đi MỘT lần',
           loi=['Con nhớ lại một lần nữa. Phần chồng bị đếm hai lần nên trừ đi một lần.',
                'Cộng thẳng mà ra nhiều hơn cả lớp là biết mình quên trừ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chuong_tho(b):
    """⑩ Nguyên lý chuồng thỏ — bài KẾT chương, không tính ra số nào cả."""
    return [
        _c('bia', 'Nguyên lý chuồng thỏ', so_bai(b),
           loi=['Hôm nay là bài lạ nhất, vì nó không bắt con tính ra số nào cả.']),
        _c('de_toan', 'Một nhóm có 13 bạn.',
           'Chứng tỏ chắc chắn có ít nhất 2 bạn sinh cùng một tháng.',
           loi=['Một nhóm có mười ba bạn.',
                'Hãy chứng tỏ chắc chắn có ít nhất hai bạn sinh cùng một tháng.']),
        _c('y_toan', 'Đếm số CHỖ', 'Một năm có 12 tháng, tức 12 chỗ.',
           buoc=1, soBuoc=4,
           loi=['Trước hết đếm số chỗ. Một năm có mười hai tháng, tức mười hai chỗ.']),
        _c('y_toan', 'Đếm số ĐỒ cần xếp', 'Có 13 bạn.', buoc=2, soBuoc=4,
           loi=['Rồi đếm số đồ cần xếp. Có mười ba bạn.']),
        _c('nhom_deu', 'Xếp mỗi tháng một bạn', tong=13, moiNhom=12,
           chuPhu='12 bạn vừa đủ 12 tháng, còn thừa 1 bạn.',
           chuCuoi='Bạn thừa ấy phải vào một tháng đã có người.',
           loi=['Xếp mười hai bạn vào mười hai tháng, mỗi tháng một bạn.',
                'Vẫn còn thừa một bạn, mà không còn tháng trống nào.']),
        _c('y_toan', 'Nên chắc chắn có tháng chứa 2 bạn',
           'Ta không biết là tháng nào, nhưng chắc chắn có.', buoc=3, soBuoc=4,
           loi=['Nên chắc chắn có một tháng chứa hai bạn.',
                'Mình không biết đó là tháng nào, nhưng chắc chắn có.']),
        _c('y_toan', 'Đó chính là điều bài toán hỏi',
           'Bài này chứng minh điều đó PHẢI xảy ra.', buoc=4, soBuoc=4,
           loi=['Đó chính là điều bài toán hỏi. Bài này chứng minh một điều phải xảy ra.']),
        _c('cong_thuc', 'Nguyên lý chuồng thỏ',
           congThuc='nhiều ĐỒ hơn số CHỖ  ⟶  có chỗ chứa từ 2 đồ trở lên',
           thay='13 bạn · 12 tháng  ⟶  có tháng 2 bạn',
           loi=['Nhiều đồ hơn số chỗ thì chắc chắn có chỗ chứa từ hai đồ trở lên.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tìm đâu là ĐỒ, đâu là CHỖ',
           loi=['Con nhớ lại một lần nữa. Gặp bài kiểu này thì tìm xem đâu là đồ, đâu '
                'là chỗ.',
                'Đồ nhiều hơn chỗ là kết luận được ngay.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 9 · MƯỜI MỘT KỊCH BẢN — PHÂN SỐ
# ═══════════════════════════════════════════════════════════════════════════
# Bộ neo: phân số ba phần tư. Mọi con số đã kiểm bằng máy trước khi viết — kể cả
# tổng tách hiệu, nó ra đúng ba phần tư nên nối liền với bộ neo.
#
# Chương này đứng hay đổ ở cảnh `phan_so`: bé phải THẤY mẫu số là "chia làm mấy phần"
# và tử số là "lấy mấy phần". Nói bằng lời thì tử với mẫu chỉ là hai cái tên khó nhớ.


def kb_ps_la_gi(b):
    """① Phân số là gì — bài KHÁI NIỆM."""
    return [
        _c('bia', 'Phân số là gì', so_bai(b),
           loi=['Hôm nay mình học xem phân số là gì.']),
        _c('phan_so', 'Chia băng giấy làm 4 phần bằng nhau', tu=0, mau=4,
           chuPhu='Bốn phần phải BẰNG NHAU.',
           loi=['Chia một băng giấy làm bốn phần bằng nhau.',
                'Phải bằng nhau thì mới đúng.']),
        _c('phan_so', 'Rồi tô 3 phần', tu=3, mau=4,
           chuPhu='Phần đã tô viết là ba phần tư.',
           loi=['Rồi tô ba phần. Phần đã tô viết thành phân số ba phần tư.']),
        _c('y_toan', 'Số viết DƯỚI gọi là mẫu số',
           'Nó cho biết chia làm mấy phần.', buoc=1, soBuoc=3,
           loi=['Số viết ở dưới gọi là mẫu số. Nó cho biết chia làm mấy phần.']),
        _c('y_toan', 'Số viết TRÊN gọi là tử số',
           'Nó cho biết lấy mấy phần.', buoc=2, soBuoc=3,
           loi=['Số viết ở trên gọi là tử số. Nó cho biết lấy mấy phần.']),
        _c('y_toan', 'Hai số nói HAI VIỆC khác nhau',
           'Đổi chỗ chúng là ra phân số khác hẳn.', buoc=3, soBuoc=3,
           loi=['Hai số nói hai việc khác nhau. Một số về việc chia, một số về việc lấy.',
                'Đổi chỗ chúng là ra phân số khác hẳn.']),
        _c('cong_thuc', 'Đọc một phân số',
           congThuc='mẫu số = chia mấy phần   ·   tử số = lấy mấy phần',
           thay='3 phần trong 4 phần',
           loi=['Mẫu số là chia mấy phần, tử số là lấy mấy phần.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='các phần phải BẰNG NHAU',
           loi=['Con nhớ lại một lần nữa. Các phần chia ra phải bằng nhau.',
                'Chia to nhỏ khác nhau thì phân số không còn nghĩa gì.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_so_de(b):
    """② So sánh cùng mẫu hoặc cùng tử — nhìn hình là thấy."""
    return [
        _c('bia', 'So sánh cùng mẫu hoặc cùng tử', so_bai(b),
           loi=['Hôm nay mình so hai phân số, nhưng chỉ hai trường hợp dễ nhất.']),
        _c('phan_so', 'Cùng mẫu số: ba phần tư và hai phần tư', tu=3, mau=4,
           tu2=2, mau2=4, chuPhu='Chia giống hệt nhau, chỉ khác số phần lấy.',
           loi=['Ba phần tư và hai phần tư đều chia băng làm bốn phần.',
                'Chia giống hệt nhau, chỉ khác số phần lấy.']),
        _c('y_toan', 'Cùng mẫu thì đếm số phần lấy',
           'Lấy nhiều hơn thì lớn hơn.', buoc=1, soBuoc=3,
           loi=['Cùng mẫu thì chỉ cần đếm số phần lấy. Lấy nhiều hơn thì lớn hơn.']),
        _c('phan_so', 'Cùng tử số: ba phần tư và ba phần năm', tu=3, mau=4,
           tu2=3, mau2=5, chuPhu='Cùng lấy 3 phần, nhưng phần bên nào to hơn?',
           loi=['Ba phần tư và ba phần năm đều lấy ba phần.',
                'Nhưng phần của bên nào to hơn.']),
        _c('y_toan', 'Chia ÍT thì mỗi phần TO',
           'Chia 4 phần thì mỗi phần to hơn chia 5 phần.', buoc=2, soBuoc=3,
           loi=['Chia làm bốn phần thì mỗi phần to hơn chia làm năm phần.',
                'Như chia bánh cho ít người thì miếng to hơn.']),
        _c('y_toan', 'Nên ba phần tư lớn hơn',
           'Cùng lấy 3 phần mà phần to hơn.', buoc=3, soBuoc=3,
           loi=['Nên ba phần tư lớn hơn ba phần năm.']),
        _c('cong_thuc', 'Hai trường hợp dễ',
           congThuc='cùng mẫu → tử lớn hơn thì lớn hơn   ·   cùng tử → mẫu bé hơn thì lớn hơn',
           thay='3/4 > 2/4   và   3/4 > 3/5',
           loi=['Cùng mẫu thì tử lớn hơn là lớn hơn. Cùng tử thì mẫu bé hơn là lớn hơn.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='mẫu càng LỚN thì mỗi phần càng NHỎ',
           loi=['Con nhớ lại một lần nữa. Mẫu số càng lớn thì mỗi phần càng nhỏ.',
                'Đừng tưởng mẫu lớn thì phân số lớn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_quy_dong(b):
    """③ Quy đồng — chia lại cho hai băng giống nhau."""
    return [
        _c('bia', 'Quy đồng mẫu số', so_bai(b),
           loi=['Hôm nay mình so hai phân số khác hẳn nhau.']),
        _c('phan_so', 'Ba phần tư và hai phần ba', tu=3, mau=4, tu2=2, mau2=3,
           chuPhu='Khác mẫu, khác cả tử — nhìn không ra.',
           loi=['Ba phần tư và hai phần ba. Khác mẫu, khác cả tử nên nhìn không ra.']),
        _c('y_toan', 'Vì sao nhìn không ra',
           'Phần của hai băng to nhỏ khác nhau.', buoc=1, soBuoc=4,
           loi=['Vì phần của hai băng to nhỏ khác nhau nên không đếm chung được.']),
        _c('y_toan', 'Chia lại cho GIỐNG NHAU',
           'Tìm số chia hết cho cả 4 và 3 — lấy 12.', buoc=2, soBuoc=4,
           loi=['Mình chia lại cả hai băng thành mười hai phần.',
                'Vì mười hai chia hết cho cả bốn và ba.']),
        _c('phan_so', 'Ba phần tư thành chín phần mười hai', tu=9, mau=12,
           chuPhu='Mỗi phần cũ tách làm 3, nên 3 phần thành 9 phần.',
           loi=['Mỗi phần cũ tách làm ba, nên ba phần thành chín phần.',
                'Ba phần tư bằng chín phần mười hai.']),
        _c('phan_so', 'Hai phần ba thành tám phần mười hai', tu=8, mau=12,
           chuPhu='Mỗi phần cũ tách làm 4, nên 2 phần thành 8 phần.',
           loi=['Bên kia mỗi phần cũ tách làm bốn, nên hai phần thành tám phần.']),
        _c('y_toan', 'Bây giờ cùng mẫu rồi', '9 phần nhiều hơn 8 phần',
           buoc=3, soBuoc=4,
           loi=['Bây giờ cùng mẫu rồi. Chín phần nhiều hơn tám phần.']),
        _c('y_toan', 'Nên ba phần tư lớn hơn hai phần ba', '', buoc=4, soBuoc=4,
           loi=['Nên ba phần tư lớn hơn hai phần ba.']),
        _c('cong_thuc', 'Quy đồng mẫu số',
           congThuc='nhân mẫu mấy lần thì nhân tử BẤY NHIÊU lần',
           thay='3/4 = 9/12   ·   2/3 = 8/12',
           loi=['Nhân mẫu mấy lần thì phải nhân tử bấy nhiêu lần.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='quên nhân tử là làm phân số BÉ ĐI',
           loi=['Con nhớ lại một lần nữa. Quên nhân tử số là làm phân số bé đi.',
                'Chia lại băng thì ô nhỏ đi, nhưng phần tô phải giữ nguyên chỗ ấy.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_so_nhanh(b):
    """④ So với 1 và phần bù."""
    return [
        _c('bia', 'So với 1 và phần bù', so_bai(b),
           loi=['Hôm nay mình học hai cách so rất nhanh, không cần quy đồng.']),
        _c('phan_so', 'Cách một: so với 1', tu=5, mau=4,
           chuPhu='Tử lớn hơn mẫu thì đã tô quá cả băng.',
           chuCuoi='Năm phần tư lớn hơn 1.',
           loi=['Cách một là so với một. Tử số lớn hơn mẫu số thì đã tô quá cả băng.',
                'Nên năm phần tư lớn hơn một.']),
        _c('y_toan', 'Còn tử bé hơn mẫu thì bé hơn 1',
           'Ba phần bốn như thế.', buoc=1, soBuoc=3,
           loi=['Còn tử số bé hơn mẫu số thì bé hơn một. Ba phần bốn như thế.',
                'Một bên lớn hơn một, một bên bé hơn một, so ngay được.']),
        _c('phan_so', 'Cách hai: so phần còn thiếu', tu=3, mau=4, tu2=4, mau2=5,
           chuPhu='Băng trên thiếu 1 phần tư, băng dưới thiếu 1 phần năm.',
           loi=['Cách hai là so phần còn thiếu để đầy băng.',
                'Băng trên thiếu một phần tư, băng dưới thiếu một phần năm.']),
        _c('y_toan', 'Thiếu ÍT hơn thì đầy hơn',
           'Một phần năm bé hơn một phần tư.', buoc=2, soBuoc=3,
           loi=['Một phần năm bé hơn một phần tư, nên băng dưới thiếu ít hơn.']),
        _c('y_toan', 'Nên bốn phần năm lớn hơn ba phần tư', '', buoc=3, soBuoc=3,
           loi=['Nên bốn phần năm lớn hơn ba phần tư.']),
        _c('cong_thuc', 'Hai cách so nhanh',
           congThuc='tử > mẫu → lớn hơn 1   ·   thiếu ít hơn → lớn hơn',
           thay='4/5 thiếu 1/5 · 3/4 thiếu 1/4',
           loi=['Tử lớn hơn mẫu thì lớn hơn một. Còn thiếu ít hơn thì lớn hơn.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đều thiếu MỘT phần, nhưng phần ấy to nhỏ khác nhau',
           loi=['Con nhớ lại một lần nữa. Đều thiếu một phần không có nghĩa là bằng nhau.',
                'Phần ấy to nhỏ khác nhau. Không chắc thì cứ quy đồng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tim_ps(b):
    """⑤ Tìm phân số của một số — chia rồi nhân."""
    return [
        _c('bia', 'Tìm phân số của một số', so_bai(b),
           loi=['Hôm nay mình lấy một phần của một con số thật.']),
        _c('de_toan', 'Tìm ba phần tư của số 20.', '',
           loi=['Tìm ba phần tư của số hai mươi.']),
        _c('y_toan', 'Đọc phân số ra thành việc làm',
           'Chia làm 4 phần rồi lấy 3 phần.', buoc=1, soBuoc=3,
           loi=['Ba phần tư nghĩa là chia làm bốn phần rồi lấy ba phần.']),
        _c('y_toan', 'Bước một, chia', '20 : 4 = 5', buoc=2, soBuoc=3,
           loi=['Bước một, chia hai mươi thành bốn phần. Mỗi phần là năm.']),
        _c('phan_so', 'Băng 20 chia làm 4 ô, mỗi ô 5', tu=3, mau=4,
           chuPhu='Tô 3 ô thì được 15.',
           loi=['Vẽ ra thì thấy. Băng hai mươi chia làm bốn ô, mỗi ô năm.',
                'Tô ba ô thì được mười lăm.']),
        _c('y_toan', 'Bước hai, lấy', '3 × 5 = 15', buoc=3, soBuoc=3,
           loi=['Bước hai, lấy ba phần, được mười lăm.']),
        _c('cong_thuc', 'Tìm phân số của một số',
           congThuc='CHIA cho mẫu số  ⟶  NHÂN với tử số',
           thay='20 : 4 = 5, rồi 3 × 5 = 15',
           loi=['Chia cho mẫu số trước, rồi nhân với tử số.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='lấy một phần của số thì kết quả phải BÉ HƠN số ấy',
           loi=['Con nhớ lại một lần nữa. Lấy một phần của số thì kết quả phải bé hơn.',
                'Ra lớn hơn là chắc chắn làm ngược thứ tự.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tim_so(b):
    """⑥ Tìm số khi biết phân số của nó — bài ngược."""
    return [
        _c('bia', 'Tìm số khi biết phân số của nó', so_bai(b),
           loi=['Hôm nay mình đi ngược lại bài hôm qua.']),
        _c('de_toan', 'Ba phần tư của một số bằng 15.', 'Tìm số đó.',
           loi=['Ba phần tư của một số bằng mười lăm. Tìm số đó.']),
        _c('y_toan', 'So với bài hôm qua', 'Hôm qua có 20 tìm ra 15. Nay có 15 tìm lại 20.',
           buoc=1, soBuoc=3,
           loi=['Hôm qua có hai mươi rồi tìm ra mười lăm. Hôm nay ngược lại.']),
        _c('phan_so', '15 ứng với MẤY phần', tu=3, mau=4,
           chuPhu='15 là 3 phần, không phải 4 phần.',
           loi=['Mười lăm ứng với ba phần, không phải bốn phần. Đây là chỗ hay nhầm.']),
        _c('y_toan', 'Bước một, tìm một phần', '15 : 3 = 5', buoc=2, soBuoc=3,
           loi=['Bước một, chia cho tử số. Mười lăm chia ba bằng năm.']),
        _c('y_toan', 'Bước hai, nhân cho đủ mẫu', '4 × 5 = 20', buoc=3, soBuoc=3,
           loi=['Bước hai, cả số gồm bốn phần nên nhân bốn, được hai mươi.']),
        _c('cong_thuc', 'Bài đi ngược',
           congThuc='CHIA cho tử số  ⟶  NHÂN với mẫu số',
           thay='15 : 3 = 5, rồi 4 × 5 = 20',
           loi=['Bài ngược thì chia cho tử số rồi nhân với mẫu số.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='xuôi chia MẪU · ngược chia TỬ',
           loi=['Con nhớ lại một lần nữa. Bài xuôi chia cho mẫu, bài ngược chia cho tử.',
                'Nhầm hai chỗ này là sai cả bài.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_day_tong(b):
    """⑦ Dãy phân số · tổng — tách thành hiệu."""
    return [
        _c('bia', 'Dãy phân số · phép cộng', so_bai(b),
           loi=['Hôm nay mình cộng một dãy phân số dài.']),
        _c('de_toan', 'Tính một phần hai cộng một phần sáu cộng một phần mười hai.', '',
           loi=['Tính một phần hai cộng một phần sáu cộng một phần mười hai.']),
        _c('y_toan', 'Nhìn kỹ các mẫu số',
           '2 = 1×2 · 6 = 2×3 · 12 = 3×4', buoc=1, soBuoc=4,
           loi=['Nhìn kỹ các mẫu số. Toàn là tích của hai số liên tiếp.']),
        _c('y_toan', 'Tách mỗi số thành một HIỆU',
           '1/(1×2) = 1/1 − 1/2', buoc=2, soBuoc=4,
           loi=['Tách mỗi số hạng thành một hiệu.',
                'Một phần một nhân hai bằng một trừ một phần hai.']),
        _c('y_toan', 'Cộng lại thì các phần GIỮA triệt tiêu',
           'Một phần hai trừ rồi lại cộng nên mất.', buoc=3, soBuoc=4,
           loi=['Cộng lại thì các phần ở giữa triệt tiêu nhau.',
                'Một phần hai trừ rồi lại cộng nên mất. Một phần ba cũng thế.']),
        _c('y_toan', 'Chỉ còn số đầu và số cuối', '1 − 1/4 = 3/4', buoc=4, soBuoc=4,
           loi=['Chỉ còn một trừ một phần tư, bằng ba phần tư.']),
        _c('phan_so', 'Tổng đúng bằng ba phần tư', tu=3, mau=4,
           chuPhu='Cộng dài mà kết quả rất gọn.',
           loi=['Tổng đúng bằng ba phần tư. Cộng dài mà kết quả rất gọn.']),
        _c('cong_thuc', 'Tổng dãy phân số',
           congThuc='tách mỗi số thành HIỆU  ⟶  phần giữa triệt tiêu',
           thay='1 − 1/4 = 3/4',
           loi=['Tách mỗi số thành một hiệu thì phần giữa triệt tiêu.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chỉ dùng được khi mẫu là tích hai số LIÊN TIẾP',
           loi=['Con nhớ lại một lần nữa. Chỉ dùng được khi mẫu là tích hai số liên tiếp.',
                'Kiểm điều ấy trước khi tách.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_day_tich(b):
    """⑧ Dãy phân số · tích — gạch chéo."""
    return [
        _c('bia', 'Dãy phân số · phép nhân', so_bai(b),
           loi=['Hôm nay là phép nhân dài, và cách làm khác hẳn hôm qua.']),
        _c('de_toan', 'Tính một phần hai nhân hai phần ba nhân ba phần tư.', '',
           loi=['Tính một phần hai nhân hai phần ba nhân ba phần tư.']),
        _c('y_toan', 'Nhìn kỹ các con số',
           'Mẫu của số này giống tử của số sau.', buoc=1, soBuoc=3,
           loi=['Nhìn kỹ. Mẫu của phân số này giống tử của phân số sau.',
                'Số hai, rồi số ba, đều xuất hiện hai lần.']),
        _c('y_toan', 'Gạch chéo cho triệt tiêu',
           'Số 2 và số 3 triệt tiêu nhau.', buoc=2, soBuoc=3,
           loi=['Gạch chéo thì số hai và số ba triệt tiêu nhau.']),
        _c('y_toan', 'Chỉ còn tử ĐẦU và mẫu CUỐI', 'Tích bằng một phần tư.',
           buoc=3, soBuoc=3,
           loi=['Chỉ còn tử số đầu tiên và mẫu số cuối cùng. Tích bằng một phần tư.']),
        _c('phan_so', 'Tích bằng một phần tư', tu=1, mau=4,
           chuPhu='Nhân dài mà kết quả rất gọn.',
           loi=['Tích bằng một phần tư.']),
        _c('y_toan', 'Đừng lẫn với bài hôm qua',
           'Bài CỘNG tách thành hiệu. Bài NHÂN gạch chéo.', buoc=3, soBuoc=3,
           loi=['Đừng lẫn với bài hôm qua. Bài cộng thì tách thành hiệu.',
                'Bài nhân thì gạch chéo. Hai cách cho hai phép khác nhau.']),
        _c('cong_thuc', 'Tích dãy phân số',
           congThuc='gạch chéo  ⟶  chỉ còn tử ĐẦU và mẫu CUỐI',
           thay='1/2 × 2/3 × 3/4 = 1/4',
           loi=['Gạch chéo thì chỉ còn tử đầu và mẫu cuối.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='bài CỘNG tách hiệu · bài NHÂN gạch chéo',
           loi=['Con nhớ lại một lần nữa. Bài cộng tách thành hiệu, bài nhân gạch chéo.',
                'Gặp bài thì hỏi trước: đây là phép cộng hay phép nhân.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_cung_them_ps(b):
    """⑨ Cùng thêm ở tử và mẫu — hiệu không đổi."""
    return [
        _c('bia', 'Cùng thêm ở tử và mẫu', so_bai(b),
           loi=['Hôm nay mình thêm cùng một số vào cả tử và mẫu.']),
        _c('phan_so', 'Phân số ba phần tư', tu=3, mau=4,
           chuPhu='Mẫu trừ tử bằng 1.',
           loi=['Cho phân số ba phần tư. Mẫu trừ tử bằng một.']),
        _c('y_toan', 'Thêm 2 vào cả hai đầu', '3 + 2 = 5  ·  4 + 2 = 6',
           buoc=1, soBuoc=3,
           loi=['Thêm hai vào cả tử và mẫu. Tử thành năm, mẫu thành sáu.']),
        _c('phan_so', 'Được phân số năm phần sáu', tu=5, mau=6,
           chuPhu='Mẫu trừ tử vẫn bằng 1.',
           loi=['Được phân số năm phần sáu. Mẫu trừ tử vẫn bằng một.']),
        _c('y_toan', 'Hiệu KHÔNG đổi', 'Đúng như chương tổng - hiệu đã học.',
           buoc=2, soBuoc=3,
           loi=['Hiệu không đổi. Đúng như chương tổng trừ hiệu con đã học.',
                'Cùng thêm vào cả hai thì khoảng cách giữa chúng như cũ.']),
        _c('y_toan', 'Nhưng phân số thì ĐỔI',
           'Năm phần sáu lớn hơn ba phần tư.', buoc=3, soBuoc=3,
           loi=['Nhưng phân số thì đổi. Năm phần sáu lớn hơn ba phần tư.',
                'Chỉ hiệu là không đổi thôi.']),
        _c('cong_thuc', 'Cùng thêm vào tử và mẫu',
           congThuc='HIỆU giữa mẫu và tử không đổi',
           thay='4 − 3 = 1   và   6 − 5 = 1',
           loi=['Cùng thêm vào cả tử và mẫu thì hiệu giữa chúng không đổi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hiệu không đổi · nhưng PHÂN SỐ thì đổi',
           loi=['Con nhớ lại một lần nữa. Hiệu không đổi, nhưng phân số thì đổi.',
                'Đừng lẫn hai chuyện ấy.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_chuyen_ps(b):
    """⑩ Chuyển giữa tử và mẫu — tổng không đổi."""
    return [
        _c('bia', 'Chuyển giữa tử và mẫu', so_bai(b),
           loi=['Hôm nay mình chuyển từ đầu này sang đầu kia.']),
        _c('phan_so', 'Vẫn phân số ba phần tư', tu=3, mau=4,
           chuPhu='Tử cộng mẫu bằng 7.',
           loi=['Vẫn phân số ba phần tư. Tử cộng mẫu bằng bảy.']),
        _c('y_toan', 'Chuyển 1 từ mẫu sang tử', 'Mẫu bớt 1, tử thêm 1.',
           buoc=1, soBuoc=3,
           loi=['Chuyển một đơn vị từ mẫu sang tử. Mẫu bớt một, tử thêm một.']),
        _c('phan_so', 'Được phân số bốn phần ba', tu=4, mau=3,
           chuPhu='Tử cộng mẫu vẫn bằng 7.',
           loi=['Được phân số bốn phần ba. Tử cộng mẫu vẫn bằng bảy.']),
        _c('y_toan', 'TỔNG không đổi',
           'Bên này bớt bao nhiêu thì bên kia thêm bấy nhiêu.', buoc=2, soBuoc=3,
           loi=['Tổng không đổi. Vì bên này bớt bao nhiêu thì bên kia được thêm đúng '
                'bấy nhiêu.']),
        _c('y_toan', 'Đừng lẫn với bài hôm qua',
           'THÊM vào hai đầu → hiệu không đổi. CHUYỂN qua lại → tổng không đổi.',
           buoc=3, soBuoc=3,
           loi=['Đừng lẫn với bài hôm qua. Thêm vào cả hai đầu thì hiệu không đổi.',
                'Còn chuyển qua lại thì tổng không đổi. Hai bài khác hẳn.']),
        _c('cong_thuc', 'Chuyển giữa tử và mẫu',
           congThuc='TỔNG của tử và mẫu không đổi',
           thay='3 + 4 = 7   và   4 + 3 = 7',
           loi=['Chuyển giữa tử và mẫu thì tổng của chúng không đổi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='THÊM → hiệu yên   ·   CHUYỂN → tổng yên',
           loi=['Con nhớ lại một lần nữa. Thêm vào hai đầu thì hiệu đứng yên.',
                'Chuyển qua lại thì tổng đứng yên. Đọc kỹ đề xem gặp bài nào.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_ps_thuc_te(b):
    """⑪ Phân số trong bài toán thực tế — đọc ra phân số CỦA CÁI GÌ."""
    return [
        _c('bia', 'Phân số trong bài toán thực tế', so_bai(b),
           loi=['Bài cuối chương, và nó không dạy phép mới nào.']),
        _c('de_toan', 'Cửa hàng có 20 tấn gạo, ngày đầu bán ba phần tư số gạo.',
           'Bán được bao nhiêu tấn, còn lại bao nhiêu?',
           loi=['Một cửa hàng có hai mươi tấn gạo. Ngày đầu bán được ba phần tư số gạo.']),
        _c('y_toan', 'Câu hỏi quan trọng nhất',
           'Ba phần tư ấy là của CÁI GÌ?', buoc=1, soBuoc=4,
           loi=['Câu hỏi quan trọng nhất là ba phần tư ấy là của cái gì.']),
        _c('y_toan', 'Ở đây là của SỐ GẠO BAN ĐẦU', 'Tức của 20 tấn.',
           buoc=2, soBuoc=4,
           loi=['Ở đây là của số gạo ban đầu, tức của hai mươi tấn.']),
        _c('phan_so', 'Băng 20 tấn chia 4 phần, bán 3 phần', tu=3, mau=4,
           chuPhu='Mỗi phần 5 tấn, bán 15 tấn.',
           chuCuoi='Còn lại đúng một phần, tức 5 tấn.',
           loi=['Băng hai mươi tấn chia bốn phần, mỗi phần năm tấn.',
                'Bán ba phần là mười lăm tấn, còn lại một phần là năm tấn.']),
        _c('y_toan', 'Soi lại cho hợp lý',
           'Bán 3/4 thì còn 1/4 — khớp với 5 tấn.', buoc=3, soBuoc=4,
           loi=['Soi lại. Bán ba phần tư thì còn một phần tư, đúng bằng năm tấn.']),
        _c('y_toan', 'Nếu đề nói "ba phần tư CHỖ CÒN LẠI"',
           'Thì gốc đã đổi, phải lấy của 5 tấn.', buoc=4, soBuoc=4,
           loi=['Nếu đề nói ba phần tư chỗ còn lại thì gốc đã đổi.',
                'Lúc ấy phải lấy của năm tấn, không phải của hai mươi tấn.']),
        _c('cong_thuc', 'Việc đầu tiên của bài lời văn',
           congThuc='đọc ra phân số ấy là CỦA CÁI GÌ',
           thay='3/4 của 20 tấn = 15 tấn',
           loi=['Việc đầu tiên là đọc ra phân số ấy là của cái gì.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='lấy nhầm GỐC thì mọi phép sau đều sai',
           loi=['Con nhớ lại một lần nữa. Lấy nhầm gốc thì mọi phép sau đều sai.',
                'Dù con tính rất đúng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# CHƯƠNG 10 · ĐỢT MỘT — SÁU KỊCH BẢN VỀ CHU VI VÀ DIỆN TÍCH
# ═══════════════════════════════════════════════════════════════════════════
# Số neo: hình chữ nhật 6 mét nhân 4 mét. Chu vi 20, diện tích 24 — HAI CON SỐ KHÁC
# HẲN NHAU, nên bé không lẫn được như khi gặp hình vuông cạnh 4 (chu vi 16, diện tích
# cũng 16).
DAI, RONG = 6, 4


def kb_cv_dt(b):
    """① Chu vi và diện tích khác nhau chỗ nào — bài KHÁI NIỆM."""
    return [
        _c('bia', 'Chu vi và diện tích khác nhau chỗ nào', so_bai(b),
           loi=['Hôm nay mình phân biệt hai chữ rất hay bị lẫn.']),
        _c('hinh_cn', 'Chu vi — đường đi quanh mép', dai=DAI, rong=RONG,
           vienDam=True, nhanDai='6 mét', nhanRong='4 mét',
           chuPhu='Đi bộ một vòng quanh mép vườn.',
           loi=['Tưởng tượng con đi bộ một vòng quanh mép vườn.',
                'Quãng đường ấy gọi là chu vi.']),
        _c('y_toan', 'Đi hết bốn cạnh', '6 + 4 + 6 + 4 = 20 mét', buoc=1, soBuoc=4,
           loi=['Đi hết bốn cạnh thì được hai mươi mét.']),
        _c('hinh_cn', 'Diện tích — mặt bị phủ kín', dai=DAI, rong=RONG,
           oVuong=True, nhanDai='6 mét', nhanRong='4 mét',
           chuPhu='Lát gạch kín cả mảnh vườn.',
           loi=['Bây giờ tưởng tượng lát gạch kín cả mảnh vườn.',
                'Mỗi viên gạch là một ô vuông cạnh một mét.']),
        _c('y_toan', 'Đếm số ô', 'Mỗi hàng 6 ô, có 4 hàng — tất cả 24 ô',
           buoc=2, soBuoc=4,
           loi=['Mỗi hàng sáu ô, có bốn hàng, tất cả hai mươi tư ô.',
                'Diện tích là hai mươi tư mét vuông.']),
        _c('y_toan', 'Hai con số khác nhau', 'Chu vi 20 · diện tích 24',
           buoc=3, soBuoc=4,
           loi=['Chu vi hai mươi, diện tích hai mươi tư. Hai con số khác nhau.']),
        _c('y_toan', 'Nên đơn vị cũng khác',
           'Chu vi đo bằng mét · diện tích đo bằng mét vuông', buoc=4, soBuoc=4,
           loi=['Chúng đo hai thứ khác hẳn nên đơn vị cũng khác.',
                'Một bên là mét, một bên là mét vuông.']),
        _c('cong_thuc', 'Hai thứ khác hẳn nhau',
           congThuc='chu vi = đi quanh MÉP   ·   diện tích = phủ kín MẶT',
           thay='20 mét   ·   24 mét vuông',
           loi=['Chu vi là đi quanh mép, còn diện tích là phủ kín mặt.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='rào lưới → chu vi   ·   trồng cỏ → diện tích',
           loi=['Con nhớ lại một lần nữa. Rào lưới quanh vườn thì tính chu vi.',
                'Trồng cỏ phủ kín vườn thì tính diện tích.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_hai_ct(b):
    """② Hai công thức — SUY RA từ hình."""
    return [
        _c('bia', 'Hai công thức', so_bai(b),
           loi=['Hôm nay mình viết hai công thức, nhưng tự nhìn hình mà ra.']),
        _c('hinh_cn', 'Đi quanh hình gặp mấy cạnh', dai=DAI, rong=RONG,
           vienDam=True, nhanDai='6 mét', nhanRong='4 mét',
           chuPhu='Chiều dài gặp HAI lần, chiều rộng cũng HAI lần.',
           loi=['Đi quanh hình thì gặp chiều dài hai lần, chiều rộng cũng hai lần.']),
        _c('y_toan', 'Nên gọn lại được', '(6 + 4) × 2 = 20', buoc=1, soBuoc=3,
           loi=['Thay vì cộng bốn số, ta cộng dài với rộng rồi nhân đôi.',
                'Sáu cộng bốn được mười, nhân đôi được hai mươi.']),
        _c('hinh_cn', 'Bây giờ đếm ô theo hàng', dai=DAI, rong=RONG,
           oVuong=True, nhanDai='6 ô mỗi hàng', nhanRong='4 hàng',
           chuPhu='Số ô mỗi hàng đúng bằng chiều dài.',
           loi=['Mỗi hàng có sáu ô, đúng bằng chiều dài.',
                'Có bốn hàng, đúng bằng chiều rộng.']),
        _c('y_toan', 'Nên đếm nhanh bằng phép nhân', '6 × 4 = 24', buoc=2, soBuoc=3,
           loi=['Nên số ô là sáu nhân bốn, bằng hai mươi tư.',
                'Chẳng cần đếm từng ô một.']),
        _c('y_toan', 'Chỗ hay quên nhất', 'Quên nhân đôi khi tính chu vi.',
           buoc=3, soBuoc=3,
           loi=['Chỗ hay quên nhất là quên nhân đôi khi tính chu vi.',
                'Hình có bốn cạnh chứ đâu phải hai.']),
        _c('cong_thuc', 'Hai công thức',
           congThuc='chu vi = (dài + rộng) × 2   ·   diện tích = dài × rộng',
           thay='(6 + 4) × 2 = 20   ·   6 × 4 = 24',
           loi=['Chu vi bằng dài cộng rộng rồi nhân đôi. Diện tích bằng dài nhân rộng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='nhân đôi vì hình có HAI dài và HAI rộng',
           loi=['Con nhớ lại một lần nữa. Nhân đôi vì hình có hai chiều dài và hai '
                'chiều rộng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_don_vi(b):
    """③ Đơn vị đo diện tích — vì sao bậc đổi là một trăm."""
    return [
        _c('bia', 'Đơn vị đo diện tích', so_bai(b),
           loi=['Hôm nay mình xem vì sao đổi đơn vị diện tích lại nhân trăm.']),
        _c('de_toan', 'Một mét bằng mười đề-xi-mét.',
           'Vậy một mét vuông bằng bao nhiêu đề-xi-mét vuông?',
           loi=['Một mét bằng mười đề-xi-mét.',
                'Vậy một mét vuông bằng bao nhiêu đề-xi-mét vuông?']),
        _c('y_toan', 'Nhiều bạn đoán là mười', 'Nhưng thử vẽ ra mà xem.',
           buoc=1, soBuoc=3,
           loi=['Nhiều bạn đoán là mười. Nhưng thử vẽ ra mà xem.']),
        _c('hinh_cn', 'Ô vuông cạnh một mét, chia cả HAI chiều', dai=10, rong=10,
           oVuong=True, nhanDai='10 phần', nhanRong='10 phần',
           chuPhu='Chia ngang mười phần, chia dọc cũng mười phần.',
           loi=['Ô vuông cạnh một mét. Chia ngang mười phần, chia dọc cũng mười phần.']),
        _c('y_toan', 'Đếm số ô nhỏ', '10 × 10 = 100 ô', buoc=2, soBuoc=3,
           loi=['Mỗi hàng mười ô, có mười hàng, tất cả một trăm ô.']),
        _c('y_toan', 'Vì sao bậc đổi lớn hơn',
           'Chiều dài chia MỘT chiều · diện tích chia CẢ HAI chiều', buoc=3, soBuoc=3,
           loi=['Chiều dài chỉ chia theo một chiều, còn diện tích chia theo cả hai.',
                'Nên bậc đổi phải nhân hai lần.']),
        _c('cong_thuc', 'Bậc đổi của diện tích',
           congThuc='1 m² = 100 dm²   ·   1 ha = 10 000 m²',
           thay='10 × 10 = 100',
           loi=['Một mét vuông bằng một trăm đề-xi-mét vuông.',
                'Một héc-ta bằng mười nghìn mét vuông.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='diện tích có HAI chiều nên bậc đổi nhân hai lần',
           loi=['Con nhớ lại một lần nữa. Đừng lấy bậc đổi của chiều dài áp cho diện tích.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tim_canh(b):
    """④ Biết diện tích tìm cạnh — đọc ngược phép nhân."""
    return [
        _c('bia', 'Biết diện tích, tìm cạnh', so_bai(b),
           loi=['Hôm nay đề cho kết quả rồi bắt mình tìm cạnh.']),
        _c('de_toan', 'Hình chữ nhật có diện tích 24 mét vuông, chiều dài 6 mét.',
           'Tính chiều rộng.',
           loi=['Hình chữ nhật có diện tích hai mươi tư mét vuông, chiều dài sáu mét.']),
        _c('y_toan', 'Nhớ lại chiều xuôi', 'Diện tích = dài × rộng', buoc=1, soBuoc=3,
           loi=['Đi xuôi thì diện tích bằng chiều dài nhân chiều rộng.']),
        _c('y_toan', 'Đọc ngược phép nhân', 'Đi ngược của nhân là CHIA',
           buoc=2, soBuoc=3,
           loi=['Đi ngược của phép nhân là phép chia.',
                'Hai mươi tư chia sáu bằng bốn mét.']),
        _c('hinh_cn', 'Nghĩ theo hình cũng ra thế', dai=DAI, rong=RONG,
           oVuong=True, nhanDai='6 ô mỗi hàng', nhanRong='? hàng',
           chuPhu='Tất cả 24 ô, mỗi hàng 6 ô — vậy mấy hàng?',
           loi=['Nghĩ theo hình cũng ra thế. Tất cả hai mươi tư ô, mỗi hàng sáu ô.',
                'Nên số hàng là hai mươi tư chia sáu.']),
        _c('y_toan', 'Nếu đề cho chu vi thì khác', 'Nửa chu vi = dài + rộng',
           buoc=3, soBuoc=3,
           loi=['Nếu đề cho chu vi thì chia đôi để lấy nửa chu vi.',
                'Nửa chu vi chính là dài cộng rộng, rồi trừ đi cạnh đã biết.']),
        _c('cong_thuc', 'Hai bài ngược',
           congThuc='có diện tích → CHIA   ·   có chu vi → chia đôi rồi TRỪ',
           thay='24 : 6 = 4   ·   20 : 2 − 6 = 4',
           loi=['Có diện tích thì chia. Có chu vi thì chia đôi rồi trừ.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='diện tích đi bằng phép NHÂN nên đi ngược là phép CHIA',
           loi=['Con nhớ lại một lần nữa. Đừng lấy diện tích trừ cạnh.',
                'Diện tích đi bằng phép nhân nên đi ngược phải là phép chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tang_mot(b):
    """⑤ Tăng một chiều — phần thêm là một DẢI."""
    return [
        _c('bia', 'Tăng một chiều', so_bai(b),
           loi=['Hôm nay mình kéo dài một cạnh rồi xem diện tích đổi thế nào.']),
        _c('hinh_cn', 'Hình cũ: 6 mét nhân 4 mét', dai=DAI, rong=RONG,
           oVuong=True, nhanDai='6 mét', nhanRong='4 mét',
           chuPhu='Diện tích 24 mét vuông.',
           loi=['Hình cũ dài sáu mét, rộng bốn mét, diện tích hai mươi tư mét vuông.']),
        _c('hinh_cn', 'Kéo dài thêm 3 mét', dai=9, rong=RONG,
           oVuong=True, nhanDai='9 mét', nhanRong='4 mét',
           chuPhu='Phần thêm là một DẢI rộng 3 mét, cao 4 mét.',
           loi=['Kéo dài thêm ba mét. Phần thêm là một dải rộng ba mét, cao bốn mét.']),
        _c('y_toan', 'Dải ấy cũng là hình chữ nhật', '3 × 4 = 12 mét vuông',
           buoc=1, soBuoc=3,
           loi=['Dải ấy cũng là hình chữ nhật nên diện tích bằng ba nhân bốn.',
                'Được mười hai mét vuông.']),
        _c('y_toan', 'Kiểm lại bằng cách tính cả hình',
           '9 × 4 = 36 · 6 × 4 = 24 · chênh 12', buoc=2, soBuoc=3,
           loi=['Kiểm lại. Hình mới ba mươi sáu, hình cũ hai mươi tư, chênh nhau mười hai.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thêm 3 mét KHÔNG phải thêm 3 mét vuông.',
           buoc=3, soBuoc=3,
           loi=['Chỗ hay nhầm là tưởng thêm ba mét thì thêm ba mét vuông.',
                'Phần thêm là cả một dải cao bốn mét cơ mà.']),
        _c('cong_thuc', 'Tăng một chiều',
           congThuc='diện tích thêm = phần kéo dài × chiều KIA',
           thay='3 × 4 = 12 mét vuông',
           loi=['Diện tích thêm bằng phần kéo dài nhân với chiều kia.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='phần thêm là một DẢI, không phải một ô',
           loi=['Con nhớ lại một lần nữa. Phần thêm là cả một dải, không phải một ô.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_tang_giam(b):
    """⑥ Tăng chiều này giảm chiều kia — diện tích có thể không đổi."""
    return [
        _c('bia', 'Tăng chiều này, giảm chiều kia', so_bai(b),
           loi=['Hôm nay mình đổi cả hai chiều cùng một lúc.']),
        _c('hinh_cn', 'Hình cũ: 6 nhân 4', dai=DAI, rong=RONG,
           oVuong=True, nhanDai='6 mét', nhanRong='4 mét',
           chuPhu='Diện tích 24 mét vuông.',
           loi=['Hình cũ sáu nhân bốn, diện tích hai mươi tư mét vuông.']),
        _c('hinh_cn', 'Tăng dài 2, giảm rộng 1', dai=8, rong=3,
           oVuong=True, nhanDai='8 mét', nhanRong='3 mét',
           chuPhu='8 nhân 3 cũng bằng 24 mét vuông!',
           chuCuoi='Hình khác hẳn mà diện tích như nhau.',
           loi=['Tăng dài hai, giảm rộng một. Tám nhân ba cũng bằng hai mươi tư.',
                'Hình khác hẳn mà diện tích như nhau.']),
        _c('y_toan', 'Diện tích KHÔNG đổi', 'Một hình dài hẹp, một hình ngắn rộng.',
           buoc=1, soBuoc=3,
           loi=['Diện tích không đổi. Một hình dài và hẹp, một hình ngắn và rộng.',
                'Nhưng chúng phủ kín cùng một mặt.']),
        _c('y_toan', 'Còn chu vi thì sao', 'Cũ 20 mét · mới 22 mét', buoc=2, soBuoc=3,
           loi=['Còn chu vi thì đổi. Cũ hai mươi mét, mới hai mươi hai mét.']),
        _c('y_toan', 'Vì sao hai thứ phản ứng khác nhau',
           'Diện tích là phép NHÂN, chu vi là phép CỘNG.', buoc=3, soBuoc=3,
           loi=['Vì diện tích tính bằng phép nhân còn chu vi tính bằng phép cộng.',
                'Nên chúng phản ứng khác nhau.']),
        _c('cong_thuc', 'Đổi cả hai chiều',
           congThuc='phải TÍNH tích hai cạnh mới, đừng đoán bù trừ',
           thay='8 × 3 = 24, vẫn như cũ',
           loi=['Phải tính tích hai cạnh mới, đừng đoán rằng chúng bù trừ nhau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='diện tích có thể giữ nguyên · chu vi thì vẫn đổi',
           loi=['Con nhớ lại một lần nữa. Diện tích có thể giữ nguyên.',
                'Nhưng chu vi thì vẫn đổi. Hỏi riêng từng thứ một.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# Khoá theo MÃ BÀI, không theo số bài. Từ 14-08 (lối C) số bài đếm từ vị trí trong
# `thu_tu.json`, nên nó đổi mỗi khi chèn bài mới — khoá theo nó thì chèn chín bài
# vào chương 3 là tám kịch bản này nhảy sang nhầm bài, mà vẫn dựng ra video hợp lệ.
def kb_bon_goc(b):
    """① Bốn loại góc — cả bài dựng quanh MỘT dụng cụ: cái ê ke."""
    return [
        _c('bia', 'Bốn loại góc', so_bai(b),
           loi=['Hôm nay con có bốn cái tên cho bốn loại góc.']),
        _c('y_toan', 'Mắt thường hay đoán sai', 'Nhất là với góc gần vuông.',
           buoc=1, soBuoc=2,
           loi=['Nhìn một cái góc rồi đoán nó lớn hay bé, mắt thường hay đoán sai.',
                'Nhất là với những góc gần vuông.']),
        _c('y_toan', 'Ê ke có sẵn một góc vuông chuẩn',
           'Nó là cái thước để đo góc.', buoc=2, soBuoc=2,
           loi=['Ê ke có sẵn một góc vuông chuẩn. Nó là cái thước để đo góc.',
                'Áp ê ke vào đỉnh góc, cho một cạnh nằm khít lên một cạnh của góc.']),
        _c('goc', 'Cạnh góc chui gọn bên trong ê ke', 'Bé hơn góc vuông.',
           do=42, eKe=True, ten='GÓC NHỌN',
           loi=['Cạnh còn lại chui gọn bên trong ê ke. Đó là góc nhọn.',
                'Góc nhọn bé hơn góc vuông.']),
        _c('goc', 'Cạnh góc trùng khít với cạnh ê ke', 'Đây là góc con đã quen.',
           do=90, eKe=True, ten='GÓC VUÔNG',
           loi=['Cạnh còn lại trùng khít với cạnh ê ke. Đó là góc vuông.']),
        _c('goc', 'Cạnh góc xoè rộng ra ngoài ê ke', 'Lớn hơn góc vuông.',
           do=125, eKe=True, ten='GÓC TÙ',
           loi=['Cạnh còn lại xoè rộng ra ngoài ê ke. Đó là góc tù.',
                'Góc tù lớn hơn góc vuông.']),
        _c('goc', 'Hai cạnh duỗi thẳng thành một đường',
           'Bằng đúng hai góc vuông ghép lại.', do=180, eKe=True, ten='GÓC BẸT',
           loi=['Mở tiếp nữa thì hai cạnh duỗi thẳng thành một đường. Đó là góc bẹt.',
                'Góc bẹt bằng đúng hai góc vuông ghép lại.']),
        _c('y_toan', 'Kéo dài cạnh KHÔNG làm góc lớn lên',
           'Góc lớn hay bé là do độ MỞ giữa hai cạnh.',
           loi=['Con nhớ một chỗ rất hay nhầm. Kéo dài hai cạnh ra thì góc không lớn '
                'lên.',
                'Góc lớn hay bé là do độ mở giữa hai cạnh, không phải do cạnh dài ngắn.']),
        _c('cong_thuc', 'Bốn loại góc xếp theo độ mở',
           congThuc='nhọn  <  vuông  <  tù  <  bẹt',
           thay='góc bẹt bằng đúng hai góc vuông',
           loi=['Bốn loại góc xếp theo độ mở. Nhọn, rồi vuông, rồi tù, rồi bẹt.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ĐO bằng ê ke  ·  đừng đoán bằng mắt',
           loi=['Con nhớ lại một lần nữa. Muốn biết một góc thuộc loại nào thì áp ê ke '
                'vào.',
                'Đừng đoán bằng mắt.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_duong_cao(b):
    """② Đường cao — bài này không tính gì, nó dạy MỘT ĐIỀU KIỆN."""
    return [
        _c('bia', 'Đường cao của tam giác', so_bai(b),
           loi=['Hôm nay vẫn cái ê ke ấy, nhưng dùng để vẽ.']),
        _c('tam_giac', 'Cạnh nằm ngang gọi là đáy', day=8, cao=5, dinh=0.45,
           nhanDay='đáy', chuPhu='Đỉnh ở trên, đối diện với đáy.',
           loi=['Đây là một tam giác. Cạnh nằm ngang gọi là đáy.',
                'Đỉnh ở trên, đối diện với đáy.']),
        _c('y_toan', 'Đường cao là gì',
           'Đoạn từ ĐỈNH xuống ĐÁY, gặp đáy theo một góc vuông.', buoc=1, soBuoc=3,
           loi=['Đường cao là đoạn thẳng đi từ đỉnh xuống đáy.',
                'Và nó phải gặp đáy theo một góc vuông. Đó là điều kiện duy nhất.']),
        _c('tam_giac', 'Hạ đường cao từ đỉnh xuống đáy', day=8, cao=5, dinh=0.45,
           duongCao=True, nhanCao='đường cao', nhanDay='đáy',
           chuPhu='Dấu ô vuông nhỏ ghi rằng đã kiểm góc vuông.',
           loi=['Hạ đường cao từ đỉnh xuống đáy. Chỗ nó gặp đáy có một dấu ô vuông nhỏ.',
                'Dấu ấy ghi rằng mình đã kiểm góc vuông, không phải vẽ ước chừng.']),
        _c('y_toan', 'Vẽ bằng ê ke thế nào',
           'Áp cạnh góc vuông vào đáy, trượt cho cạnh kia chạm đỉnh.',
           buoc=2, soBuoc=3,
           loi=['Vẽ bằng ê ke. Áp một cạnh góc vuông của ê ke sát vào đáy.',
                'Trượt ê ke dọc theo đáy cho tới khi cạnh kia chạm đúng đỉnh, rồi kẻ.']),
        _c('y_toan', 'Chỗ gặp đáy gọi là chân đường cao',
           'Không đòi đi qua điểm giữa đáy.', buoc=3, soBuoc=3,
           loi=['Chỗ đường cao gặp đáy gọi là chân đường cao.',
                'Con nhớ kỹ. Đường cao không đòi đi qua điểm giữa đáy, nó chỉ đòi vuông '
                'góc.']),
        _c('tam_giac', 'Tam giác tù — chân rơi RA NGOÀI đáy', day=7, cao=4, dinh=1.42,
           duongCao=True, nhanCao='đường cao', nhanDay='đáy',
           chuPhu='Kéo dài đáy ra mà đón, vẽ bằng nét đứt.',
           loi=['Gặp tam giác có góc tù thì chân đường cao có thể rơi ra ngoài đáy.',
                'Đừng hoảng. Cứ kéo dài đáy ra mà đón, phần kéo dài vẽ bằng nét đứt.']),
        _c('y_toan', 'Ba đỉnh nên ba đường cao',
           'Mỗi đỉnh hạ được một đường cao xuống cạnh đối diện.',
           loi=['Tam giác có ba đỉnh nên vẽ được ba đường cao.',
                'Mỗi đỉnh hạ một đường cao xuống cạnh đối diện với nó.']),
        _c('cong_thuc', 'Điều kiện của đường cao',
           congThuc='từ ĐỈNH  ·  xuống ĐÁY  ·  VUÔNG GÓC với đáy',
           thay='đi qua điểm giữa đáy thì KHÔNG phải điều kiện',
           loi=['Đường cao đi từ đỉnh xuống đáy và vuông góc với đáy.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='vuông góc thì mới là đường cao',
           loi=['Con nhớ lại một lần nữa. Vuông góc với đáy thì mới là đường cao.',
                'Kẻ xuống giữa đáy mà không vuông góc thì đó là đoạn khác.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_cat_ghep(b):
    """③ Cắt rồi ghép — lấy lại ĐÚNG bộ số sáu nhân bốn của đợt một."""
    return [
        _c('bia', 'Cắt rồi ghép', so_bai(b),
           loi=['Hôm nay mình cầm kéo cắt một tờ giấy quen thuộc.']),
        _c('hinh_cn', 'Tờ giấy sáu nhân bốn — con đã quen', dai=6, rong=4, oVuong=True,
           nhanDai='6 cm', nhanRong='4 cm', chuPhu='Đếm ô: 24 ô vuông.',
           loi=['Tờ giấy hình chữ nhật, dài sáu, rộng bốn. Con đã quen bộ số này rồi.',
                'Đếm ô thì được hai mươi tư ô vuông.']),
        _c('y_toan', 'Diện tích tờ giấy', '6 × 4 = 24 xăng-ti-mét vuông',
           buoc=1, soBuoc=3,
           loi=['Diện tích tờ giấy là sáu nhân bốn, bằng hai mươi tư xăng ti mét '
                'vuông.']),
        _c('hinh_cn', 'Cắt theo đường chéo', dai=6, rong=4, oVuong=True,
           duongCheo=True, nhanDai='6 cm', nhanRong='4 cm',
           chuPhu='Được hai mảnh tam giác.',
           loi=['Bây giờ cắt theo đường chéo. Được hai mảnh tam giác.']),
        _c('y_toan', 'Hai mảnh bằng nhau', 'Úp mảnh này lên mảnh kia thì khít.',
           buoc=2, soBuoc=3,
           loi=['Hai mảnh bằng nhau. Úp mảnh này lên mảnh kia thì chúng khít nhau.']),
        _c('y_toan', 'Cắt không làm mất giấy',
           'Không thêm mảnh nào, không mất mảnh nào.', buoc=3, soBuoc=3,
           loi=['Cắt ra thì giấy vẫn là ngần ấy giấy. Không thêm mảnh nào, không mất '
                'mảnh nào.',
                'Nên hai mảnh cộng lại vẫn đúng hai mươi tư ô.']),
        _c('y_toan', 'Vậy mỗi mảnh bằng nửa', '24 : 2 = 12 xăng-ti-mét vuông',
           loi=['Hai mảnh bằng nhau và cộng lại bằng hai mươi tư.',
                'Nên mỗi mảnh là hai mươi tư chia hai, bằng mười hai xăng ti mét vuông.',
                'Con tính được diện tích tam giác mà chưa cần công thức nào.']),
        _c('y_toan', 'Nhưng CHU VI thì đổi',
           'Mỗi mảnh nay có thêm một mép cắt.',
           loi=['Còn chu vi thì đổi. Mỗi mảnh nay có thêm một mép cắt mà lúc chưa cắt '
                'không có.',
                'Đường đi quanh mép dài ra.']),
        _c('cong_thuc', 'Luật cắt ghép',
           congThuc='cắt rồi ghép  →  DIỆN TÍCH không đổi',
           thay='còn CHU VI thì có thể đổi',
           loi=['Cắt rồi ghép lại thì diện tích không đổi. Còn chu vi thì có thể đổi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='không thêm không bớt mảnh nào  ·  nên mặt phủ vẫn ngần ấy',
           loi=['Con nhớ lại một lần nữa. Ghép kiểu nào thì phần mặt bị phủ vẫn ngần '
                'ấy.',
                'Vì không thêm không bớt mảnh giấy nào cả.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_hinh_tron(b):
    """④ Hình tròn — cả bài đứng ở hai chữ ĐI QUA TÂM."""
    return [
        _c('bia', 'Bán kính và đường kính', so_bai(b),
           loi=['Hôm nay cất ê ke đi, lấy com pa ra.']),
        _c('hinh_tron', 'Cắm com pa xuống một điểm rồi xoay một vòng',
           chuPhu='Điểm cắm ấy gọi là TÂM.',
           loi=['Cắm mũi nhọn của com pa xuống một điểm rồi xoay một vòng.',
                'Điểm cắm ấy gọi là tâm của hình tròn.']),
        _c('hinh_tron', 'Đoạn nối tâm với một điểm trên nét vẽ', hienR=True,
           nhanR='3 cm', chuPhu='Đoạn ấy gọi là BÁN KÍNH.',
           loi=['Đoạn nối tâm với một điểm trên nét vẽ gọi là bán kính.',
                'Ở đây com pa mở ba xăng ti mét, nên bán kính ba xăng ti mét.']),
        _c('y_toan', 'Vì sao mọi bán kính bằng nhau',
           'Suốt vòng xoay, độ mở của com pa không đổi.',
           loi=['Suốt vòng xoay, độ mở của com pa không đổi một chút nào.',
                'Nên mọi điểm trên nét vẽ đều cách tâm đúng bằng nhau.',
                'Mọi bán kính của một hình tròn đều bằng nhau.']),
        _c('hinh_tron', 'Đoạn nối hai mép VÀ đi qua tâm', hienR=True, hienD=True,
           nhanR='3 cm', nhanD='6 cm', chuPhu='Đoạn ấy gọi là ĐƯỜNG KÍNH.',
           loi=['Đoạn nối hai mép và đi qua tâm gọi là đường kính.',
                'Bốn chữ đi qua tâm là chỗ quan trọng nhất của cả bài.']),
        _c('y_toan', 'Đường kính gồm hai bán kính nối tiếp',
           'Từ mép tới tâm, rồi từ tâm sang mép kia.',
           loi=['Đường kính đi từ mép này, qua tâm, sang mép kia.',
                'Nên nó gồm đúng hai bán kính nối tiếp nhau. Ba nhân hai bằng sáu.']),
        _c('hinh_tron', 'Dây không qua tâm thì NGẮN HƠN', dayLech=True, hienD=True,
           nhanD='6 cm', nhanLech='dây lệch tâm',
           chuPhu='Đường kính là cái dây dài nhất của hình tròn.',
           loi=['Đây là chỗ hay nhầm. Dây nối hai mép mà đi lệch, không qua tâm, thì '
                'ngắn hơn.',
                'Đường kính là cái dây dài nhất của hình tròn.']),
        _c('cong_thuc', 'Đường kính và bán kính',
           congThuc='đường kính  =  bán kính  ×  2',
           thay='3 × 2 = 6 xăng-ti-mét',
           loi=['Đường kính bằng bán kính nhân hai.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='phải ĐI QUA TÂM mới là đường kính',
           loi=['Con nhớ lại một lần nữa. Phải đi qua tâm mới là đường kính.',
                'Đi lệch thì chỉ là một cái dây thường, và nó ngắn hơn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_trai_phang(b):
    """⑤ Trải phẳng hộp ra — chỗ đáng dạy là BA CẶP, không phải sáu mặt."""
    return [
        _c('bia', 'Trải phẳng hộp ra', so_bai(b),
           loi=['Hôm nay mình rọc một cái hộp ra rồi trải phẳng nó lên bàn.']),
        _c('khoi', 'Cái hộp dài bốn, rộng ba, cao hai', kieu='chong',
           dai=4, rong=3, cao=2, chuPhu='Ba số đo của một cái hộp.',
           loi=['Một cái hộp chữ nhật, dài bốn, rộng ba, cao hai xăng ti mét.']),
        _c('khoi', 'Rọc theo mép rồi trải phẳng ra', kieu='trai',
           dai=4, rong=3, cao=2,
           chuPhu='Hai mặt cùng màu là hai mặt đối diện.',
           chuCuoi='Sáu mặt, nhưng chỉ ba cặp.',
           loi=['Rọc theo mép rồi trải phẳng ra. Sáu mặt hiện ra hết.',
                'Hai mặt cùng màu là hai mặt đối diện nhau, và chúng bằng hệt nhau.']),
        _c('y_toan', 'Sáu mặt nhưng chỉ BA CẶP',
           'Nên chỉ phải tính ba lần, không phải sáu lần.',
           loi=['Sáu mặt ấy hợp thành ba cặp. Nên mình chỉ phải tính ba lần thôi.']),
        _c('y_toan', 'Cặp đáy và nắp', '4 × 3 = 12 xăng-ti-mét vuông',
           buoc=1, soBuoc=3,
           loi=['Cặp đáy và nắp dựng từ chiều dài và chiều rộng.',
                'Bốn nhân ba bằng mười hai xăng ti mét vuông.']),
        _c('y_toan', 'Cặp trước và sau', '4 × 2 = 8 xăng-ti-mét vuông',
           buoc=2, soBuoc=3,
           loi=['Cặp trước và sau dựng từ chiều dài và chiều cao.',
                'Bốn nhân hai bằng tám xăng ti mét vuông.']),
        _c('y_toan', 'Cặp hai bên hông', '3 × 2 = 6 xăng-ti-mét vuông',
           buoc=3, soBuoc=3,
           loi=['Cặp hai bên hông dựng từ chiều rộng và chiều cao.',
                'Ba nhân hai bằng sáu xăng ti mét vuông.']),
        _c('y_toan', 'Cộng ba mặt rồi nhân đôi MỘT LẦN',
           '12 + 8 + 6 = 26   rồi   26 × 2 = 52',
           loi=['Cộng ba mặt khác nhau lại được hai mươi sáu.',
                'Mỗi mặt có một mặt đối diện bằng nó, nên nhân đôi một lần ở cuối.',
                'Hai mươi sáu nhân hai bằng năm mươi hai xăng ti mét vuông.']),
        _c('cong_thuc', 'Tổng diện tích sáu mặt',
           congThuc='tổng sáu mặt  =  (mặt 1 + mặt 2 + mặt 3)  ×  2',
           thay='(12 + 8 + 6) × 2 = 52',
           loi=['Tổng sáu mặt bằng tổng ba mặt khác nhau, rồi nhân hai.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chỉ hình lập phương mới có sáu mặt bằng nhau',
           loi=['Con nhớ lại một lần nữa. Chỉ hình lập phương mới có sáu mặt bằng nhau.',
                'Hộp chữ nhật có ba cặp khác nhau, phải tính từng cặp.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_dem_khoi(b):
    """⑥ Đếm khối — hình khối là mấy tầng phẳng xếp chồng."""
    return [
        _c('bia', 'Đếm khối theo tầng', so_bai(b),
           loi=['Vẫn cái hộp hôm qua, nhưng lần này nó không rỗng.']),
        _c('khoi', 'Hộp xếp đầy khối lập phương nhỏ', kieu='chong',
           dai=4, rong=3, cao=2,
           chuPhu='Dài 4 khối, rộng 3 khối, cao 2 khối.',
           loi=['Cái hộp nay xếp đầy những khối lập phương nhỏ.',
                'Dài bốn khối, rộng ba khối, cao hai khối. Đếm bao nhiêu khối đây.']),
        _c('y_toan', 'Đọc chiều cao thành SỐ TẦNG',
           'Cao 2 khối nghĩa là 2 tầng chồng lên nhau.', buoc=1, soBuoc=3,
           loi=['Bước đầu tiên là đọc chiều cao thành số tầng.',
                'Cao hai khối nghĩa là hộp gồm hai tầng chồng lên nhau.']),
        _c('khoi', 'Tách rời từng tầng ra mà đếm', kieu='tang',
           dai=4, rong=3, cao=2,
           chuPhu='Mỗi tầng là một sàn phẳng.',
           loi=['Tách rời từng tầng ra. Mỗi tầng là một sàn phẳng, đếm dễ hơn hẳn.']),
        _c('y_toan', 'Đếm một tầng', '4 × 3 = 12 khối', buoc=2, soBuoc=3,
           loi=['Mỗi tầng là một sàn chữ nhật dài bốn khối, rộng ba khối.',
                'Bốn nhân ba bằng mười hai khối.']),
        _c('y_toan', 'Nhân với số tầng', '12 × 2 = 24 khối', buoc=3, soBuoc=3,
           loi=['Hai tầng giống hệt nhau. Mười hai nhân hai bằng hai mươi bốn khối.']),
        _c('khoi', 'Khối bị nhấc mất một chỗ thì sao', kieu='chong',
           dai=3, rong=3, cao=3, khuyet=[0, 0, 1],
           chuPhu='Vẫn lát từng tầng ra mà đếm.',
           loi=['Gặp khối bị nhấc mất mấy chỗ thì vẫn một lối ấy thôi.',
                'Lát từng tầng ra, tầng nào thiếu thì đếm đúng tầng ấy.']),
        _c('y_toan', 'Tầng dưới đầy, tầng trên thiếu một',
           '9 + 9 + 8 = 26 khối',
           loi=['Tầng dưới chín khối, tầng giữa chín khối, tầng trên chỉ còn tám.',
                'Cộng lại được hai mươi sáu khối.']),
        _c('cong_thuc', 'Đếm khối theo tầng',
           congThuc='tổng khối  =  (dài × rộng)  ×  số tầng',
           thay='(4 × 3) × 2 = 24 khối',
           loi=['Tổng số khối bằng số khối một tầng, nhân với số tầng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đếm theo TẦNG  ·  đừng đếm theo MẶT',
           loi=['Con nhớ lại một lần nữa. Đếm theo tầng, đừng đếm theo mặt.',
                'Đếm theo mặt là đếm vỏ, mà khối thì đặc ruột.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_doc_so(b):
    """C1① Đọc số to — chia lớp trước rồi đọc."""
    return [
        _c('bia', 'Đọc số to', so_bai(b),
           loi=['Hôm nay con có cách đọc chắc chắn cho những số thật dài.']),
        _c('bang_hang', 'Bảng hàng đếm từ PHẢI sang trái', so='24358',
           chuPhu='Đơn vị, chục, trăm — rồi nghìn, chục nghìn, trăm nghìn.',
           loi=['Bảng hàng đếm từ phải sang trái. Đơn vị, chục, trăm, rồi nghìn.']),
        _c('y_toan', 'Cứ BA HÀNG gom thành MỘT LỚP',
           'Lớp đơn vị · lớp nghìn · lớp triệu', buoc=1, soBuoc=3,
           loi=['Cứ ba hàng thì gom thành một lớp. Lớp đơn vị, lớp nghìn, rồi lớp '
                'triệu.']),
        _c('bang_hang', 'Số 1 745 230 tách được ba lớp', so='1745230',
           chuPhu='Một · bảy trăm bốn mươi lăm · hai trăm ba mươi.',
           loi=['Số này có bảy chữ số nên tách được ba lớp.']),
        _c('y_toan', 'Đọc từng lớp từ TRÁI sang',
           'Đọc xong lớp nào thì gắn tên lớp ấy vào sau.', buoc=2, soBuoc=3,
           loi=['Đọc từng lớp từ trái sang. Đọc xong lớp nào thì gắn tên lớp ấy vào '
                'sau.',
                'Một triệu. Rồi bảy trăm bốn mươi lăm nghìn. Rồi hai trăm ba mươi.']),
        _c('y_toan', 'Riêng lớp đơn vị đọc xong là thôi',
           'Không phải gắn tên lớp.', buoc=3, soBuoc=3,
           loi=['Riêng lớp đơn vị thì đọc xong là thôi, không phải gắn tên lớp vào.']),
        _c('y_toan', 'Chỗ hay đọc hỏng',
           'Số 24 358 KHÔNG đọc là "hai bốn nghìn".',
           loi=['Con nhớ chỗ này. Hai chữ số đầu ghép lại thành số hai mươi bốn.',
                'Nên phải đọc là hai mươi bốn nghìn, không đọc rời từng chữ số.']),
        _c('cong_thuc', 'Cách đọc số to',
           congThuc='tách lớp trước  ·  đọc từng lớp  ·  gắn tên lớp',
           thay='1 745 230  →  1 · 745 · 230',
           loi=['Tách lớp trước, đọc từng lớp, rồi gắn tên lớp vào sau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='mỗi lớp đọc như MỘT SỐ ba chữ số',
           loi=['Con nhớ lại một lần nữa. Mỗi lớp đọc như một số ba chữ số riêng.',
                'Đọc rời từng chữ số là hỏng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_gia_tri(b):
    """C1② Giá trị của một chữ số."""
    return [
        _c('bia', 'Giá trị của một chữ số', so_bai(b),
           loi=['Cùng một chữ số mà đứng chỗ khác thì đáng khác nhau.']),
        _c('bang_hang', 'Chữ số 7 đứng ở hàng nào', so='1745230', toSang=[5],
           chuPhu='Đếm từ phải sang: nó đứng hàng trăm nghìn.',
           loi=['Xếp số vào bảng hàng rồi đếm từ phải sang.',
                'Chữ số bảy đứng ở hàng trăm nghìn.']),
        _c('y_toan', 'Cân chữ số ấy', 'Chữ số × giá trị hàng nó đứng',
           buoc=1, soBuoc=3,
           loi=['Giá trị một chữ số bằng chính chữ số ấy, nhân với giá trị hàng nó '
                'đứng.',
                'Một trăm nghìn nhân bảy được bảy trăm nghìn.']),
        _c('bang_hang', 'Cân cho MỌI hàng thì được tổng', so='52604',
           chuPhu='50 000 + 2 000 + 600 + 4', buoc=2,
           loi=['Cân như thế cho mọi hàng thì được số ấy viết thành tổng.',
                'Năm mươi nghìn, cộng hai nghìn, cộng sáu trăm, cộng bốn.']),
        _c('bang_hang', 'Hàng chục đang TRỐNG', so='52604', toSang=[1],
           chuPhu='Chữ số 0 giữ chỗ — không đọc, nhưng không bỏ được.',
           loi=['Hàng chục đang trống nên không có số hạng nào cho nó.',
                'Nhưng chữ số không vẫn phải viết để giữ chỗ. Bỏ đi là mọi chữ số tụt '
                'hàng.']),
        _c('y_toan', 'Đừng tách rời từng chữ số',
           'Phân tích là tách theo GIÁ TRỊ.', buoc=3, soBuoc=3,
           loi=['Con nhớ chỗ hay nhầm. Phân tích không phải là tách rời từng chữ số ra.',
                'Phải tách theo giá trị của chúng.']),
        _c('cong_thuc', 'Giá trị của một chữ số',
           congThuc='giá trị = chữ số  ×  giá trị của hàng',
           thay='chữ số 7 ở hàng trăm nghìn  →  700 000',
           loi=['Giá trị bằng chữ số nhân với giá trị của hàng nó đứng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đứng đâu  ·  nặng đấy',
           loi=['Con nhớ lại một lần nữa. Đứng đâu thì nặng đấy.',
                'Hỏi chỗ đứng trước, rồi mới cân.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_bang_liet_ke(b):
    """C1③ Tìm số bằng bảng liệt kê."""
    return [
        _c('bia', 'Tìm số bằng bảng liệt kê', so_bai(b),
           loi=['Hôm nay con có cách tìm số mà không bỏ sót trường hợp nào.']),
        _c('de_toan', 'Tìm số có hai chữ số, tổng hai chữ số bằng 9.',
           'Và chữ số hàng chục hơn chữ số hàng đơn vị 3 đơn vị.',
           loi=['Tìm số có hai chữ số. Tổng hai chữ số bằng chín.',
                'Và chữ số hàng chục hơn chữ số hàng đơn vị ba đơn vị.']),
        _c('y_toan', 'Đừng thử mò', 'Thử mò thì không biết đã thử hết chưa.',
           buoc=1, soBuoc=3,
           loi=['Thử mò thì hên xui, mà lại không biết mình đã thử hết chưa.']),
        _c('y_toan', 'Lập bảng cho điều kiện THỨ NHẤT',
           '9 và 0 · 8 và 1 · 7 và 2 · 6 và 3 · 5 và 4', buoc=2, soBuoc=3,
           loi=['Lập bảng mọi cặp có tổng bằng chín, chữ số lớn hơn đứng trước.',
                'Chín và không. Tám và một. Bảy và hai. Sáu và ba. Năm và bốn.',
                'Được năm cặp, không sót cặp nào.']),
        _c('y_toan', 'Soi điều kiện THỨ HAI trên bảng',
           'Hiệu từng cặp: 9 · 7 · 5 · 3 · 1', buoc=3, soBuoc=3,
           loi=['Nay tính hiệu từng cặp. Chín, bảy, năm, ba, một.',
                'Chỉ một cặp có hiệu bằng ba, đó là cặp sáu và ba.']),
        _c('y_toan', 'Đáp số', 'Số cần tìm là 63.',
           loi=['Số cần tìm là sáu mươi ba.',
                'Thử lại: sáu cộng ba bằng chín, sáu trừ ba bằng ba. Khớp cả hai.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Số 36 cũng có tổng 9, nhưng hàng chục lại BÉ hơn.',
           loi=['Con nhớ chỗ này. Số ba mươi sáu cũng có tổng chín.',
                'Nhưng hàng chục của nó lại bé hơn hàng đơn vị, nên không đạt.']),
        _c('cong_thuc', 'Cách làm bài tìm số',
           congThuc='lập bảng cho điều kiện MỘT  ·  soi điều kiện HAI',
           thay='tổng bằng 9 → năm cặp → cặp nào hiệu bằng 3',
           loi=['Lập bảng cho điều kiện thứ nhất, rồi soi điều kiện thứ hai trên bảng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='lập bảng thì KHÔNG SÓT  ·  thử mò thì hên xui',
           loi=['Con nhớ lại một lần nữa. Lập bảng thì không sót trường hợp nào.',
                'Và làm xong nhớ thử lại cả hai điều kiện.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_them_phai(b):
    """C1④ Thêm một chữ số vào bên phải — sơ đồ mười phần."""
    return [
        _c('bia', 'Thêm chữ số vào bên phải', so_bai(b),
           loi=['Thêm một chữ số không mà giá nhảy vọt. Nhảy bao nhiêu đây.']),
        _c('de_toan', 'Máy in giá 3 500 đồng thành 35 000 đồng.',
           'Giá bị đội lên bao nhiêu?',
           loi=['Máy in giá ba nghìn năm trăm đồng thành ba mươi lăm nghìn đồng.']),
        _c('y_toan', 'Thêm 0 vào bên phải là GẤP MƯỜI',
           'Mọi chữ số dịch sang trái một hàng.', buoc=1, soBuoc=3,
           loi=['Thêm số không vào bên phải thì mọi chữ số dịch sang trái một hàng.',
                'Mỗi hàng nặng gấp mười hàng bên phải nó, nên cả số nặng gấp mười.']),
        _c('so_do_doan', 'Vẽ ra thành sơ đồ', be=1, lon=10, phanLon=10,
           nhanBe='số cũ', nhanLon='số mới', hienHieu=True, chuHieu='9 phần đội thêm',
           chuPhu='Số cũ 1 phần, số mới 10 phần.',
           loi=['Vẽ ra thì thấy ngay. Số cũ một phần, số mới mười phần.',
                'Vậy phần đội thêm là chín phần, tức chín lần số cũ.']),
        _c('y_toan', 'Tính thử xem có khớp không',
           '35 000 − 3 500 = 31 500', buoc=2, soBuoc=3,
           loi=['Lấy hiệu: ba mươi lăm nghìn trừ ba nghìn năm trăm, được ba mươi mốt '
                'nghìn năm trăm.']),
        _c('y_toan', 'Kiểm bằng phép nhân', '3 500 × 9 = 31 500',
           buoc=3, soBuoc=3,
           loi=['Kiểm lại bằng phép nhân. Ba nghìn năm trăm nhân chín cũng ra đúng con '
                'số ấy.']),
        _c('y_toan', 'Thêm chữ số KHÁC 0 thì sao',
           'Thêm 5 vào bên phải 35 → 9 lần số cũ, rồi cộng 5.',
           loi=['Thêm chữ số khác không thì phần thêm gồm chín lần số cũ, cộng chính '
                'chữ số ấy.',
                'Ba mươi lăm nhân chín được ba trăm mười lăm, cộng năm được ba trăm '
                'hai mươi.']),
        _c('cong_thuc', 'Thêm chữ số vào bên phải',
           congThuc='tăng thêm  =  9 × số cũ  +  chữ số vừa thêm',
           thay='thêm 0 vào 3 500  →  9 × 3 500 = 31 500',
           loi=['Phần tăng thêm bằng chín lần số cũ, cộng chữ số vừa thêm.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số mới là MƯỜI phần  ·  không phải hai phần',
           loi=['Con nhớ lại một lần nữa. Số mới là mười phần chứ không phải hai phần.',
                'Nên nó đội thêm chín lần, không phải gấp đôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_them_trai(b):
    """C1⑤ Thêm bên trái và xen vào giữa."""
    return [
        _c('bia', 'Thêm bên trái và xen vào giữa', so_bai(b),
           loi=['Còn hai cánh cửa nữa, mỗi cửa để lại một dấu vết riêng.']),
        _c('bang_hang', 'Cửa TRÁI — chữ số mới ngồi vào hàng trăm', so='475',
           toSang=[2], chuPhu='Hai chữ số cũ đứng yên tại chỗ.',
           loi=['Thêm chữ số bốn vào bên trái số bảy mươi lăm được bốn trăm bảy mươi '
                'lăm.',
                'Hai chữ số cũ đứng yên, chỉ chữ số mới ngồi vào hàng trăm.']),
        _c('y_toan', 'Nên số tăng đúng một số TRÒN TRĂM',
           '4 × 100 = 400', buoc=1, soBuoc=3,
           loi=['Nên số tăng thêm đúng bằng giá trị chữ số mới ở hàng trăm.',
                'Bốn nhân một trăm bằng bốn trăm. Kiểm lại cũng đúng bốn trăm.']),
        _c('bang_hang', 'Cửa GIỮA — chữ số 8 bị ĐẨY lên hàng trăm', so='804',
           toSang=[2], chuPhu='Còn chữ số 4 vẫn đứng yên.',
           loi=['Xen số không vào giữa số tám mươi tư được tám trăm linh tư.',
                'Lần này chữ số tám bị đẩy từ hàng chục lên hàng trăm.']),
        _c('y_toan', 'Chữ số bị đẩy đội thêm 90 lần chính nó',
           'Đang đáng 80, nay đáng 800 → thêm 720', buoc=2, soBuoc=3,
           loi=['Chữ số tám đang đáng tám mươi, nay đáng tám trăm.',
                'Nó đội thêm bảy trăm hai mươi, đúng bằng chín mươi nhân tám.']),
        _c('y_toan', 'Kiểm lại', '804 − 84 = 720', buoc=3, soBuoc=3,
           loi=['Kiểm lại bằng phép trừ. Tám trăm linh tư trừ tám mươi tư được bảy '
                'trăm hai mươi.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Số 0 không đáng gì, nhưng nó ĐẨY chữ số kia lên.',
           loi=['Con nhớ chỗ này. Bản thân số không chẳng đáng gì.',
                'Nhưng nó đẩy chữ số bên cạnh lên một hàng, và chính cái đẩy ấy làm số '
                'to lên.']),
        _c('cong_thuc', 'Hai cửa còn lại',
           congThuc='cửa TRÁI: + chữ số × 100   ·   cửa GIỮA: + 90 × chữ số bị đẩy',
           thay='4 vào trái 75 → 400   ·   0 vào giữa 84 → 720',
           loi=['Cửa trái thêm chữ số nhân một trăm. Cửa giữa thêm chín mươi nhân chữ '
                'số bị đẩy.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='lên một hàng  =  nặng gấp mười',
           loi=['Con nhớ lại một lần nữa. Lên một hàng là nặng gấp mười.',
                'Hiểu câu ấy thì cả ba cánh cửa đều dễ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_thang_may(b):
    """C1⑥ Nhân và chia cho 10, 100, 1000."""
    return [
        _c('bia', 'Nhân và chia cho mười', so_bai(b),
           loi=['Thêm một chữ số không là nhân mười. Hôm nay con biết vì sao.']),
        _c('y_toan', 'Vì sao thêm 0 là nhân mười',
           'Mọi chữ số dịch sang trái một hàng.', buoc=1, soBuoc=3,
           loi=['Thêm một chữ số không vào bên phải thì mọi chữ số dịch sang trái một '
                'hàng.',
                'Mỗi hàng nặng gấp mười hàng bên phải nó, nên cả số nặng gấp mười.']),
        _c('y_toan', 'Đi LÊN từng tầng',
           '47  →  470  →  4 700  →  47 000', buoc=2, soBuoc=3,
           loi=['Bốn mươi bảy nhân mười được bốn trăm bảy mươi.',
                'Nhân một trăm thì thêm hai chữ số không. Nhân một nghìn thì thêm ba.',
                'Bốn số ấy cùng một nhà, chỉ khác tầng đang đứng.']),
        _c('y_toan', 'Đi XUỐNG thì bớt', '4 700 : 100 = 47', buoc=3, soBuoc=3,
           loi=['Chia là đi ngược lại. Bốn nghìn bảy trăm chia một trăm thì bớt hai '
                'chữ số không, còn bốn mươi bảy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Chia 100 phải bớt HAI chữ số 0, không phải một.',
           loi=['Con nhớ chỗ này. Chia cho một trăm phải bớt hai chữ số không.',
                'Bớt có một là ra số lớn gấp mười lần đáp án đúng.']),
        _c('y_toan', 'Ghi thiếu một chữ số 0 thì hụt bao nhiêu',
           'Số đúng 10 phần, số ghi sai 1 phần → hụt 9 phần',
           loi=['Một khoản bị ghi thiếu một chữ số không thì số ghi sai chỉ bằng một '
                'phần mười.',
                'Nên phần hụt là chín phần, tức chín lần số đã ghi.']),
        _c('cong_thuc', 'Thang máy chữ số 0',
           congThuc='nhân 10, 100, 1000  →  thêm 1, 2, 3 chữ số 0',
           thay='chia thì làm ngược lại — bớt đi từng ấy',
           loi=['Nhân mười, một trăm, một nghìn thì thêm một, hai, ba chữ số không.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ĐẾM số chữ số 0 trước  ·  rồi mới viết',
           loi=['Con nhớ lại một lần nữa. Đếm số chữ số không trước, rồi mới viết.',
                'Nhầm ở bài này gần như luôn là nhầm một chữ số không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_xoa_chu_so(b):
    """C1⑦ Xoá một chữ số — ở đuôi khác hẳn ở đầu."""
    return [
        _c('bia', 'Xoá một chữ số', so_bai(b),
           loi=['Xoá ở đuôi và xoá ở đầu là hai chuyện khác hẳn nhau.']),
        _c('bang_hang', 'Xoá ở ĐẦU — các chữ số còn lại ĐỨNG YÊN', so='725',
           toSang=[2], chuPhu='Xoá chữ số 7 thì còn số 25.',
           loi=['Xoá chữ số hàng trăm của bảy trăm hai mươi lăm thì còn hai mươi lăm.',
                'Hai chữ số còn lại đứng nguyên chỗ cũ, không ai phải dịch đi đâu.']),
        _c('y_toan', 'Nên số giảm đúng GIÁ TRỊ chữ số bị cắt',
           '725 − 25 = 700', buoc=1, soBuoc=3,
           loi=['Nên số giảm đúng bằng giá trị của chữ số vừa bị cắt, tức bảy trăm.']),
        _c('bang_hang', 'Xoá ở ĐUÔI — mọi chữ số TỤT một hàng', so='303',
           toSang=[0], chuPhu='Xoá chữ số 3 thì còn số 30.',
           loi=['Xoá chữ số tận cùng của ba trăm linh ba thì còn ba mươi.',
                'Lần này mọi chữ số còn lại đều tụt xuống một hàng.']),
        _c('y_toan', 'Dựng lại số cũ', 'số cũ = số mới × 10 + chữ số bị xoá',
           buoc=2, soBuoc=3,
           loi=['Số cũ bằng số mới nhân mười, rồi cộng chữ số bị xoá.',
                'Ba mươi nhân mười được ba trăm, cộng ba được ba trăm linh ba.']),
        _c('y_toan', 'Số giảm bao nhiêu', '303 − 30 = 273', buoc=3, soBuoc=3,
           loi=['Số giảm là ba trăm linh ba trừ ba mươi, được hai trăm bảy mươi ba.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Xoá ở đuôi KHÔNG phải lúc nào cũng giảm mười lần.',
           loi=['Con nhớ chỗ này. Xoá ở đuôi chỉ giảm đúng mười lần khi chữ số bị xoá '
                'là số không.',
                'Khác không thì còn phải cộng thêm chữ số ấy nữa.']),
        _c('cong_thuc', 'Hai kiểu xoá',
           congThuc='xoá ở ĐẦU: giảm đúng giá trị chữ số ấy',
           thay='xoá ở ĐUÔI: số cũ = số mới × 10 + chữ số bị xoá',
           loi=['Xoá ở đầu thì giảm đúng giá trị chữ số ấy. Xoá ở đuôi thì phải dựng '
                'lại bằng phép nhân mười.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi: các chữ số còn lại có phải DỊCH CHỖ không',
           loi=['Con nhớ lại một lần nữa. Hỏi xem các chữ số còn lại có phải dịch chỗ '
                'không.',
                'Không dịch thì dễ, có dịch thì phải nhân mười.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_trao_chu_so(b):
    """C1⑧ Tráo hai chữ số — họ 9 và họ 11."""
    return [
        _c('bia', 'Tráo hai chữ số', so_bai(b),
           loi=['Tráo hai chữ số rồi trừ nhau, các đáp số đều họ hàng với nhau.']),
        _c('y_toan', 'Thử vài lần đã',
           '72 − 27 = 45   ·   63 − 36 = 27   ·   91 − 19 = 72', buoc=1, soBuoc=3,
           loi=['Bảy mươi hai trừ hai mươi bảy bằng bốn mươi lăm.',
                'Sáu mươi ba trừ ba mươi sáu bằng hai mươi bảy.',
                'Chín mươi mốt trừ mười chín bằng bảy mươi hai.']),
        _c('tach_so', 'Soi hiệu hai chữ số của từng số', so='72', sang=[1, 2],
           phep='7 − 2 = 5, mà 5 × 9 = 45', chuPhu='Hiệu hai chữ số nhân chín.',
           loi=['Soi hiệu hai chữ số của từng số. Năm, ba, tám.',
                'Nhân chín lên được bốn mươi lăm, hai mươi bảy, bảy mươi hai. Khớp cả '
                'ba.']),
        _c('y_toan', 'Vì sao lại thế',
           'Chữ số hàng chục tụt xuống thì MẤT chín lần chính nó.',
           buoc=2, soBuoc=3,
           loi=['Chữ số hàng chục vốn đáng gấp mười chính nó. Tráo xuống hàng đơn vị '
                'thì chỉ còn đáng chính nó.',
                'Tức là mất đi chín lần. Chữ số kia thì ngược lại, được thêm chín lần.']),
        _c('y_toan', 'Luật anh em: đem CỘNG',
           '74 + 47 = 121, mà 7 + 4 = 11 và 11 × 11 = 121', buoc=3, soBuoc=3,
           loi=['Nay thử đem cộng. Bảy mươi tư cộng bốn mươi bảy bằng một trăm hai '
                'mươi mốt.',
                'Mà bảy cộng bốn bằng mười một, rồi mười một nhân mười một cũng ra con '
                'số ấy.']),
        _c('y_toan', 'Đừng lẫn hai luật',
           'Trừ thì họ 9. Cộng thì họ 11.',
           loi=['Con đừng lẫn hai luật. Trừ thì mang họ chín, cộng thì mang họ mười '
                'một.']),
        _c('cong_thuc', 'Hai định luật tráo chữ số',
           congThuc='HIỆU = 9 × hiệu hai chữ số',
           thay='TỔNG = 11 × tổng hai chữ số',
           loi=['Hiệu bằng chín nhân hiệu hai chữ số. Tổng bằng mười một nhân tổng hai '
                'chữ số.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='biết hiệu → chia 9  ·  biết tổng → chia 11',
           loi=['Con nhớ lại một lần nữa. Biết hiệu thì chia chín, biết tổng thì chia '
                'mười một.',
                'Chia xong là lộ ra hai chữ số, rồi tra bảng liệt kê là tìm được số.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_thua_so_chung(b):
    """C2① Đặt thừa số chung."""
    return [
        _c('bia', 'Đặt thừa số chung', so_bai(b),
           loi=['Có phép tính dài mà làm được trong đầu. Bí quyết là nhìn ra thứ chung '
                'nhau.']),
        _c('de_toan', 'Tính nhanh 4 × 38 + 4 × 62.', 'Đừng vội nhân từng tích.',
           loi=['Tính nhanh bốn nhân ba mươi tám, cộng bốn nhân sáu mươi hai.']),
        _c('y_toan', 'Nhìn ra thứ CHUNG NHAU', 'Cả hai tích đều có thừa số 4.',
           buoc=1, soBuoc=3,
           loi=['Cả hai tích đều có thừa số bốn. Bốn ấy chính là thứ chung.']),
        _c('y_toan', 'Vì sao gộp được',
           'Ba mươi tám hộp gà và sáu mươi hai hộp tôm, hộp nào cũng đáng 4.',
           buoc=2, soBuoc=3,
           loi=['Có ba mươi tám hộp gà và sáu mươi hai hộp tôm, hộp nào cũng đáng bốn '
                'nghìn.',
                'Vậy đếm chung số hộp trước rồi mới nhân giá, kết quả vẫn thế.']),
        _c('y_toan', 'Gộp lại rồi tính', '4 × (38 + 62) = 4 × 100 = 400',
           buoc=3, soBuoc=3,
           loi=['Gộp lại thành bốn nhân với ngoặc. Trong ngoặc được đúng một trăm.',
                'Bốn nhân một trăm bằng bốn trăm.']),
        _c('y_toan', 'Chiều TRỪ cũng gộp được', '9 × 47 − 9 × 37 = 9 × 10 = 90',
           loi=['Chiều trừ cũng gộp được. Chín nhân bốn mươi bảy trừ chín nhân ba mươi '
                'bảy.',
                'Trong ngoặc còn mười, nhân chín được chín mươi.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thừa số chung chỉ viết MỘT lần ra ngoài ngoặc.',
           loi=['Con nhớ chỗ này. Thừa số chung chỉ viết một lần ra ngoài ngoặc.',
                'Cộng cả hai thừa số lại là hỏng.']),
        _c('cong_thuc', 'Đặt thừa số chung',
           congThuc='a × b + a × c  =  a × (b + c)',
           thay='4 × 38 + 4 × 62 = 4 × 100 = 400',
           loi=['Thừa số chung đưa ra ngoài, hai số kia gộp vào trong ngoặc.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='trước khi tính, hỏi: CÓ GÌ CHUNG KHÔNG',
           loi=['Con nhớ lại một lần nữa. Trước khi tính hãy hỏi: có gì chung không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_nham_25(b):
    """C2② Nhẩm nhanh với 25."""
    return [
        _c('bia', 'Nhẩm nhanh với hai mươi lăm', so_bai(b),
           loi=['Số hai mươi lăm lúc nào cũng đi tìm bạn.']),
        _c('y_toan', 'Cặp bài trùng của số 25', '25 × 4 = 100', buoc=1, soBuoc=3,
           loi=['Hai mươi lăm nhân bốn bằng một trăm. Nên gặp nó là đi tìm số bốn.']),
        _c('y_toan', 'Tách để LỘ số 4 ra', '36 = 4 × 9', buoc=2, soBuoc=3,
           loi=['Số ba mươi sáu tách được thành bốn nhân chín.',
                'Vậy hai mươi lăm nhân ba mươi sáu thành hai mươi lăm nhân bốn nhân '
                'chín.']),
        _c('y_toan', 'Ghép cặp trước rồi mới nhân',
           '25 × 4 = 100, rồi 100 × 9 = 900', buoc=3, soBuoc=3,
           loi=['Ghép cặp trước được một trăm. Rồi một trăm nhân chín bằng chín trăm.']),
        _c('y_toan', 'Không tách được thì đi lối khác',
           '48 × 100 = 4 800, rồi 4 800 : 4 = 1 200',
           loi=['Gặp bốn mươi tám nhân hai mươi lăm thì nhân một trăm trước.',
                'Nhân một trăm là nhân gấp bốn lần so với nhân hai mươi lăm, nên sau '
                'đó phải chia cho bốn.',
                'Bốn nghìn tám trăm chia bốn được một nghìn hai trăm.']),
        _c('y_toan', 'Người anh của số 25', '125 × 8 = 1 000',
           loi=['Số một trăm hai mươi lăm ghép với tám thì được một nghìn.',
                'Cùng một lối nghĩ, chỉ khác con số.']),
        _c('cong_thuc', 'Hai cặp phải thuộc',
           congThuc='25 × 4 = 100      ·      125 × 8 = 1 000',
           thay='25 × 36 = 25 × 4 × 9 = 900',
           loi=['Hai mươi lăm ghép với bốn. Một trăm hai mươi lăm ghép với tám.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='gặp 25 thì mắt đi tìm số 4',
           loi=['Con nhớ lại một lần nữa. Gặp hai mươi lăm thì mắt đi tìm số bốn.',
                'Tìm được là bài xong một nửa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_nham_11(b):
    """C2③ Nhẩm nhanh với 11."""
    return [
        _c('bia', 'Nhẩm nhanh với mười một', so_bai(b),
           loi=['Nhân với mười một nghe khó mà thật ra rất dễ.']),
        _c('y_toan', 'Cách chắc chắn nhất', '11 = 10 + 1', buoc=1, soBuoc=3,
           loi=['Mười một bằng mười cộng một.',
                'Nên nhân mười một là nhân mười rồi cộng thêm chính số ấy một lần.']),
        _c('y_toan', 'Làm thử', '35 × 10 = 350, rồi 350 + 35 = 385',
           buoc=2, soBuoc=3,
           loi=['Ba mươi lăm nhân mười bằng ba trăm năm mươi.',
                'Cộng thêm ba mươi lăm được ba trăm tám mươi lăm.']),
        _c('tach_so', 'Mẹo hai đầu — nhanh hơn nữa', so='385', sang=[2],
           phep='3 và 5 ra hai bên, tổng 8 nhét vào giữa',
           chuPhu='Ra đúng con số vừa tính.',
           loi=['Có mẹo nhanh hơn. Viết hai chữ số ra hai bên, cộng chúng lại rồi nhét '
                'vào giữa.',
                'Ba và năm ra hai bên, tổng tám vào giữa. Được ba trăm tám mươi lăm.']),
        _c('y_toan', 'Chỗ phải cẩn thận',
           'Với 57 thì tổng là 12 — hai chữ số mà chỗ giữa chỉ chứa được một.',
           buoc=3, soBuoc=3,
           loi=['Với năm mươi bảy thì tổng hai chữ số là mười hai.',
                'Hai chữ số mà chỗ giữa chỉ chứa được một, nên phải nhớ.']),
        _c('y_toan', 'Nhớ 1 sang trái', '5 thêm 1 thành 6 → được 627',
           loi=['Để lại chữ số hai ở giữa, nhớ một sang bên trái. Năm thêm một thành '
                'sáu.',
                'Được sáu trăm hai mươi bảy. Kiểm bằng cách chắc chắn cũng ra thế.']),
        _c('cong_thuc', 'Nhân với mười một',
           congThuc='× 11  =  × 10  rồi  cộng chính nó',
           thay='mẹo hai đầu: hai chữ số ra hai bên, TỔNG vào giữa',
           loi=['Nhân mười một là nhân mười rồi cộng chính nó.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tổng vượt 9  →  NHỚ 1 sang trái',
           loi=['Con nhớ lại một lần nữa. Tổng vượt chín thì nhớ một sang trái.',
                'Lẫn thì quay về cách chắc chắn, chậm vài giây nhưng không bao giờ '
                'sai.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_thua_so_0(b):
    """C2④ Nhìn kỹ trước khi tính — thừa số 0 ẩn."""
    return [
        _c('bia', 'Nhìn kỹ trước khi tính', so_bai(b),
           loi=['Có bài dài cả dòng mà đáp số là số không.']),
        _c('de_toan', 'Tính giá trị của ngoặc 13 trừ 78 chia 6, nhân 231, nhân 8.',
           'Đừng vội nhân.',
           loi=['Tính giá trị của ngoặc mười ba trừ bảy mươi tám chia sáu, rồi nhân '
                'hai trăm ba mươi mốt, rồi nhân tám.']),
        _c('y_toan', 'Soi cái ngoặc trước', '78 : 6 = 13', buoc=1, soBuoc=3,
           loi=['Soi cái ngoặc trước đã. Trong ngoặc có phép chia.',
                'Bảy mươi tám chia sáu bằng mười ba.']),
        _c('y_toan', 'Ngoặc bằng KHÔNG', '13 − 13 = 0', buoc=2, soBuoc=3,
           loi=['Mười ba trừ mười ba bằng không. Vậy cái ngoặc bằng không.']),
        _c('y_toan', 'Một thừa số bằng 0 là xong',
           'Cả tích bằng 0 — khỏi nhân gì thêm.', buoc=3, soBuoc=3,
           loi=['Trong một tích, chỉ cần một thừa số bằng không thì cả tích bằng không.',
                'Không phải nhân gì thêm nữa. Đáp số là không.']),
        _c('y_toan', 'So sánh cũng không cần tính hết',
           '52 × 25 hơn 51 × 25 đúng một lần 25 — mà bên kia chỉ hơn 20.',
           loi=['So năm mươi hai nhân hai mươi lăm với năm mươi mốt nhân hai mươi lăm '
                'cộng hai mươi.',
                'Bên trái hơn đúng một lần hai mươi lăm, mà bên phải chỉ hơn có hai '
                'mươi. Vậy bên trái lớn hơn.']),
        _c('cong_thuc', 'Ba câu soi trước khi đặt bút',
           congThuc='có thừa số CHUNG không  ·  có cặp TRÒN TRĂM không',
           thay='có thừa số 0 ẩn không',
           loi=['Ba câu hỏi soi nhanh: có thừa số chung không, có cặp tròn trăm không, '
                'có thừa số không ẩn không.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='soi ba giây  ·  tiết kiệm cả bài',
           loi=['Con nhớ lại một lần nữa. Soi ba giây trước khi đặt bút.',
                'Có khi tiết kiệm được cả bài tính.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_gom_x(b):
    """C2⑤ X xuất hiện hai lần."""
    return [
        _c('bia', 'X xuất hiện hai lần', so_bai(b),
           loi=['Gặp bài mà số cần tìm hiện ra hai lần thì gom chúng lại trước đã.']),
        _c('de_toan', 'Tìm X, biết X nhân 3 cộng X nhân 2 bằng 45.',
           'X hiện ra hai lần.',
           loi=['Bài cho biết số cần tìm nhân ba, cộng số ấy nhân hai, bằng bốn mươi lăm.']),
        _c('y_toan', 'Chưa gom thì chưa giải được',
           'Không biết phải chia cho cái gì.', buoc=1, soBuoc=3,
           loi=['Chưa gom lại thì chưa giải được, vì không biết phải chia cho cái gì.']),
        _c('y_toan', 'Gom bằng thừa số chung', 'X × (3 + 2) = X × 5',
           buoc=2, soBuoc=3,
           loi=['Cả hai số hạng đều có số cần tìm. Đưa nó ra ngoài ngoặc.',
                'Trong ngoặc ba cộng hai bằng năm. Bài thành số ấy nhân năm bằng bốn '
                'mươi lăm.']),
        _c('y_toan', 'Nay là bài quen rồi', '45 : 5 = 9', buoc=3, soBuoc=3,
           loi=['Muốn tìm thừa số chưa biết thì lấy tích chia cho thừa số kia.',
                'Bốn mươi lăm chia năm bằng chín. Vậy số cần tìm là chín.']),
        _c('y_toan', 'Thử lại', '9 × 3 = 27, rồi 9 × 2 = 18, và 27 + 18 = 45',
           loi=['Lắp chín vào đề. Hai mươi bảy cộng mười tám bằng bốn mươi lăm.',
                'Đúng bằng vế phải.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Trong ngoặc hai số CỘNG nhau, không nhân nhau.',
           loi=['Con nhớ chỗ này. Trong ngoặc hai số cộng nhau chứ không nhân nhau.',
                'Gom ra năm chứ không phải sáu.']),
        _c('cong_thuc', 'Gom X về một chỗ',
           congThuc='X × a + X × b  =  X × (a + b)',
           thay='X × 3 + X × 2 = X × 5 = 45  →  X = 9',
           loi=['Số cần tìm nhân số này, cộng số ấy nhân số kia, bằng số ấy nhân với '
                'tổng hai số.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='X đứng lẻ  =  X × 1',
           loi=['Con nhớ lại một lần nữa. Số cần tìm đứng lẻ chính là nó nhân một.',
                'Nhờ thế mà gom được cả những bài có nó đứng lẻ một mình.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_boc_ngoac(b):
    """C2⑥ Bóc ngoặc từ ngoài vào."""
    return [
        _c('bia', 'Bóc ngoặc từ ngoài vào', so_bai(b),
           loi=['Bóc ngoặc cũng như bóc củ hành, mỗi lần một lớp.']),
        _c('de_toan', 'Tìm X, biết ngoặc X trừ 15, chia cho 3, bằng 8.',
           'Có một lớp ngoặc.',
           loi=['Bài cho biết ngoặc số cần tìm trừ mười lăm, chia cho ba, bằng tám.']),
        _c('y_toan', 'Coi cả ngoặc là MỘT số bí ẩn',
           'Bài thành: số gì chia 3 thì được 8?', buoc=1, soBuoc=3,
           loi=['Cứ coi cả cặp ngoặc là một số bí ẩn.',
                'Bài thành: số gì chia ba thì được tám.']),
        _c('y_toan', 'Bóc lớp thứ nhất', '3 × 8 = 24, nên X − 15 = 24',
           buoc=2, soBuoc=3,
           loi=['Số trong ngoặc là ba nhân tám, tức hai mươi tư. Vậy số cần tìm trừ '
                'mười lăm bằng hai mươi tư.']),
        _c('y_toan', 'Bóc lớp thứ hai', '24 + 15 = 39', buoc=3, soBuoc=3,
           loi=['Nay bài quen rồi. Số cần tìm bằng hai mươi tư cộng mười lăm, tức ba '
                'mươi chín.']),
        _c('y_toan', 'Thử lại', '39 − 15 = 24, rồi 24 : 3 = 8',
           loi=['Lắp ba mươi chín vào đề. Ba mươi chín trừ mười lăm bằng hai mươi tư.',
                'Hai mươi tư chia ba bằng tám. Đúng vế phải.']),
        _c('y_toan', 'Mẹo tìm lớp phải bóc trước',
           'Lấy ngón tay che cái ngoặc lại rồi đọc phần còn thấy.',
           loi=['Con lấy ngón tay che cái ngoặc lại rồi đọc to phần còn nhìn thấy.',
                'Đó chính là lớp phải bóc trước.']),
        _c('cong_thuc', 'Bóc ngoặc',
           congThuc='coi cả ngoặc là MỘT số  ·  bóc từ NGOÀI vào',
           thay='(X − 15) : 3 = 8  →  X − 15 = 24  →  X = 39',
           loi=['Coi cả ngoặc là một số, rồi bóc từ ngoài vào, mỗi bước một lớp.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đừng nhảy cóc  ·  và luôn thử lại',
           loi=['Con nhớ lại một lần nữa. Đừng nhảy cóc, đi từng bước một.',
                'Và giải xong phải lắp số vừa tìm ngược vào đề để thử lại.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_x_chia_du(b):
    """C2⑦ Tìm X trong phép chia có dư."""
    return [
        _c('bia', 'Tìm X trong phép chia có dư', so_bai(b),
           loi=['Phép chia có dư quay lại, nhưng chỗ chưa biết nay khác.']),
        _c('y_toan', 'Nhớ lại luật vàng',
           'số bị chia = số chia × thương + số dư', buoc=1, soBuoc=3,
           loi=['Số bị chia bằng số chia nhân thương, rồi cộng số dư.',
                'Nhớ câu ấy là làm được cả hai chiều.']),
        _c('y_toan', 'Chiều một: tìm số bị chia',
           'X : 7 = 8 dư 3  →  7 × 8 = 56, rồi 56 + 3 = 59', buoc=2, soBuoc=3,
           loi=['Số cần tìm chia bảy được tám dư ba. Nhân trước, bảy nhân tám bằng '
                'năm mươi sáu.',
                'Cộng số dư: năm mươi sáu cộng ba bằng năm mươi chín.']),
        _c('y_toan', 'Chiều hai: tìm số chia',
           '45 : X = 6 dư 3  →  bớt dư trước: 45 − 3 = 42', buoc=3, soBuoc=3,
           loi=['Bốn mươi lăm chia cho số cần tìm được sáu dư ba. Lần này bớt số dư ra '
                'trước cho gọn.',
                'Bốn mươi lăm trừ ba bằng bốn mươi hai. Phần ấy mới chia hết.']),
        _c('y_toan', 'Rồi chia nốt', '42 : 6 = 7',
           loi=['Bốn mươi hai chia sáu bằng bảy. Vậy số cần tìm là bảy.']),
        _c('y_toan', 'Kiểm điều kiện bắt buộc',
           'Số dư PHẢI bé hơn số chia — ở đây 3 bé hơn 7.',
           loi=['Kiểm điều kiện bắt buộc. Số dư phải bé hơn số chia.',
                'Ở đây dư ba mà chia bảy, đúng luật.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Đừng đem cả 45 ra chia — ba đơn vị kia không chia được cho ai.',
           loi=['Con nhớ chỗ này. Đừng đem cả bốn mươi lăm ra chia.',
                'Ba đơn vị dư ấy không chia được cho ai, phải bớt ra trước.']),
        _c('cong_thuc', 'Phép chia có dư',
           congThuc='số bị chia  =  số chia × thương  +  số dư',
           thay='tìm số chia: bớt số dư ra trước rồi mới chia',
           loi=['Số bị chia bằng số chia nhân thương cộng số dư.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số dư luôn BÉ HƠN số chia',
           loi=['Con nhớ lại một lần nữa. Số dư luôn bé hơn số chia.',
                'Và thử lại phải khớp cả thương lẫn số dư, thiếu một là hỏng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_dem_cach_deu(b):
    """C2⑧ Đếm số cách đều."""
    return [
        _c('bia', 'Đếm số cách đều', so_bai(b),
           loi=['Đếm dãy dài thì có công thức, nhưng công thức ấy có một cái bẫy.']),
        _c('de_toan', 'Dãy 8, 12, 16 cho tới 96. Dãy có bao nhiêu số?',
           'Các số cách đều nhau.',
           loi=['Dãy tám, mười hai, mười sáu, cứ thế cách đều cho tới chín mươi sáu.']),
        _c('y_toan', 'Ba thứ phải tìm trước',
           'số đầu 8  ·  số cuối 96  ·  khoảng cách 4', buoc=1, soBuoc=3,
           loi=['Ba thứ phải tìm trước. Số đầu là tám, số cuối là chín mươi sáu, '
                'khoảng cách là bốn.']),
        _c('y_toan', 'Đếm số BƯỚC NHẢY', '96 − 8 = 88, rồi 88 : 4 = 22',
           buoc=2, soBuoc=3,
           loi=['Từ tám đi tới chín mươi sáu phải vượt quãng tám mươi tám.',
                'Mỗi bước dài bốn nên có hai mươi hai bước nhảy.']),
        _c('y_toan', 'Nhưng đó là BƯỚC, không phải SỐ',
           'Số đầu tiên chưa nhảy đã đứng sẵn ở đó.', buoc=3, soBuoc=3,
           loi=['Nhưng hai mươi hai là số bước nhảy, không phải số số.',
                'Số đầu tiên chưa nhảy bước nào đã đứng sẵn ở đó, phải đếm nó vào.',
                'Vậy dãy có hai mươi ba số.']),
        _c('y_toan', 'Đếm số chia hết cũng vậy',
           'Từ 1 tới 200 chia hết cho 5: 200 − 5 = 195, rồi 195 : 5 = 39, cộng 1',
           loi=['Đếm số chia hết cũng một lối ấy. Từ một tới hai trăm, số chia hết cho '
                'năm.',
                'Dãy là năm, mười, cho tới hai trăm. Tính ra ba mươi chín, cộng một '
                'được bốn mươi.']),
        _c('cong_thuc', 'Công thức đếm dãy cách đều',
           congThuc='số các số  =  (cuối − đầu) : khoảng  +  1',
           thay='(96 − 8) : 4 + 1 = 23',
           loi=['Số các số bằng hiệu chia khoảng, rồi cộng một.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ĐỪNG QUÊN cộng một',
           loi=['Con nhớ lại một lần nữa. Đừng quên cộng một.',
                'Giống đếm bậc thang: đi chín bước mà có tới mười bậc.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_dem_trang(b):
    """C2⑨ Đếm chữ số khi đánh số trang."""
    return [
        _c('bia', 'Đếm chữ số trang sách', so_bai(b),
           loi=['Đánh số trang cho cuốn sổ thì tốn bao nhiêu con chữ.']),
        _c('y_toan', 'Không đếm chung được',
           'Trang 7 tốn một chữ số, trang 250 tốn ba.', buoc=1, soBuoc=3,
           loi=['Trang bảy tốn một chữ số, trang bảy mươi tốn hai, trang hai trăm năm '
                'mươi tốn ba.',
                'Nên phải tách thành từng nhóm cùng độ dài.']),
        _c('y_toan', 'Nhóm một chữ số', 'Trang 1 tới 9: 9 trang × 1 = 9',
           buoc=2, soBuoc=3,
           loi=['Từ trang một đến trang chín có chín trang, mỗi trang một chữ số. '
                'Được chín.']),
        _c('y_toan', 'Nhóm hai chữ số', 'Trang 10 tới 99: 90 trang × 2 = 180',
           buoc=3, soBuoc=3,
           loi=['Từ trang mười đến trang chín mươi chín có chín mươi trang, mỗi trang '
                'hai chữ số. Được một trăm tám mươi.']),
        _c('y_toan', 'Nhóm ba chữ số', 'Trang 100 tới 250: 151 trang × 3 = 453',
           loi=['Từ trang một trăm đến trang hai trăm năm mươi có một trăm năm mươi '
                'mốt trang.',
                'Mỗi trang ba chữ số, được bốn trăm năm mươi ba.']),
        _c('y_toan', 'Cộng cả ba nhóm', '9 + 180 + 453 = 642',
           loi=['Cộng cả ba nhóm được sáu trăm bốn mươi hai chữ số.']),
        _c('y_toan', 'Bài ngược thì TRỪ DẦN',
           '552 − 9 = 543, rồi 543 − 180 = 363, rồi 363 : 3 = 121 trang',
           loi=['Biết cuốn sách dùng hết năm trăm năm mươi hai chữ số thì trừ dần.',
                'Bớt phần nhóm một, bớt phần nhóm hai, còn ba trăm sáu mươi ba.',
                'Chia ba được một trăm hai mươi mốt trang, cộng với chín mươi chín '
                'trang trước là hai trăm hai mươi trang.']),
        _c('cong_thuc', 'Đếm chữ số trang sách',
           congThuc='chia NHÓM theo độ dài  ·  mỗi nhóm một phép nhân',
           thay='9 + 180 + 453 = 642',
           loi=['Chia nhóm theo độ dài, mỗi nhóm một phép nhân, rồi cộng lại.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='bài ngược  →  TRỪ DẦN theo từng nhóm',
           loi=['Con nhớ lại một lần nữa. Bài ngược thì trừ dần theo từng nhóm.',
                'Trừ hết nhóm nào thì bỏ nhóm ấy đi, phần còn lại mới chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_quy_tac_nhan(b):
    """C2⑩ Quy tắc nhân."""
    return [
        _c('bia', 'Quy tắc nhân', so_bai(b),
           loi=['Ổ khoá ba vòng có bao nhiêu mật khẩu. Liệt kê thì chép cả ngày.']),
        _c('y_toan', 'Kẻ một ô cho mỗi hàng', '9 cách  ·  9 cách  ·  9 cách',
           buoc=1, soBuoc=3,
           loi=['Ba vòng thì kẻ ba ô. Mỗi ô ghi số cách chọn của vòng ấy.',
                'Chín, chín, và chín.']),
        _c('y_toan', 'Vì sao lại NHÂN',
           'Mỗi cách của vòng một ghép được với ĐỦ 9 cách của vòng hai.',
           buoc=2, soBuoc=3,
           loi=['Mỗi cách của vòng một ghép được với đủ chín cách của vòng hai.',
                'Rồi mỗi cặp ấy lại ghép được với đủ chín cách của vòng ba.']),
        _c('y_toan', 'Nhân dồn lại', '9 × 9 × 9 = 729', buoc=3, soBuoc=3,
           loi=['Nhân dồn lại được bảy trăm hai mươi chín mật khẩu.']),
        _c('y_toan', 'Kiểm bằng người quen',
           'Số có ba chữ số: 9 × 10 × 10 = 900 — đúng bằng số các số ba chữ số.',
           loi=['Đếm mọi số có ba chữ số cũng một lối ấy.',
                'Hàng trăm chín cách vì không được là không. Hai hàng sau mỗi hàng '
                'mười cách.',
                'Được chín trăm, đúng bằng số các số có ba chữ số.']),
        _c('y_toan', 'Thêm điều kiện thì siết ĐÚNG hàng ấy',
           'Mật khẩu chẵn: hàng đơn vị chỉ còn 4 cách → 9 × 9 × 4 = 324',
           loi=['Mật khẩu không chứa số không mà lại chẵn thì chỉ hàng đơn vị bị siết.',
                'Chỉ còn chọn được hai, bốn, sáu, tám, tức bốn cách. Kết quả ba trăm '
                'hai mươi tư.']),
        _c('cong_thuc', 'Quy tắc nhân',
           congThuc='kẻ một ô cho mỗi hàng  ·  rồi NHÂN DỒN',
           thay='9 × 9 × 9 = 729',
           loi=['Kẻ một ô cho mỗi hàng, điền số cách chọn, rồi nhân dồn.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ghép MỖI NHÓM một thứ  →  NHÂN, không cộng',
           loi=['Con nhớ lại một lần nữa. Chọn mỗi nhóm một thứ rồi ghép lại thì nhân.',
                'Cộng là khi chỉ chọn một thứ trong nhiều nhóm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_phan_bu(b):
    """C2⑪ Đếm bằng phần bù."""
    return [
        _c('bia', 'Đếm bằng phần bù', so_bai(b),
           loi=['Có câu hỏi đếm ngược lại thì dễ hơn hẳn.']),
        _c('de_toan', 'Có bao nhiêu số ba chữ số CÓ chứa chữ số 0?',
           'Đếm thẳng thì rối.',
           loi=['Có bao nhiêu số có ba chữ số mà trong đó có chứa chữ số không.']),
        _c('y_toan', 'Vì sao đếm thẳng thì rối',
           'Số 0 nấp ở hàng chục, ở hàng đơn vị, hoặc ở cả hai.', buoc=1, soBuoc=3,
           loi=['Chữ số không có thể nằm ở hàng chục, ở hàng đơn vị, hoặc ở cả hai.',
                'Ba trường hợp lại chồng lên nhau, dễ sót mà cũng dễ đếm trùng.']),
        _c('y_toan', 'Đếm cái NGƯỢC LẠI thì gọn',
           'Không chứa số 0: mỗi hàng chỉ còn 9 cách → 9 × 9 × 9 = 729',
           buoc=2, soBuoc=3,
           loi=['Đếm những số không chứa chữ số không thôi.',
                'Khi ấy mỗi hàng chỉ chọn từ một đến chín, tức chín cách. Nhân dồn '
                'được bảy trăm hai mươi chín.']),
        _c('y_toan', 'Lấy tất cả trừ đi', '900 − 729 = 171', buoc=3, soBuoc=3,
           loi=['Tất cả các số có ba chữ số là chín trăm.',
                'Chín trăm trừ bảy trăm hai mươi chín được một trăm bảy mươi mốt.']),
        _c('y_toan', 'Dấu hiệu nhận ra',
           'Gặp chữ "CÓ chứa" hay "ÍT NHẤT MỘT" thì nghĩ tới phần bù.',
           loi=['Gặp chữ có chứa hoặc ít nhất một thì nghĩ ngay tới phần bù.',
                'Vì cái ngược lại của chúng là không có cái nào, mà cái ấy đếm rất '
                'gọn.']),
        _c('cong_thuc', 'Đếm bằng phần bù',
           congThuc='cần đếm  =  TẤT CẢ  −  phần không thoả',
           thay='900 − 729 = 171',
           loi=['Phần cần đếm bằng tất cả trừ đi phần không thoả điều kiện.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='trừ MỘT lần  ·  không lo đếm trùng',
           loi=['Con nhớ lại một lần nữa. Trừ một lần là xong, không lo đếm trùng.',
                'Còn cộng nhiều trường hợp thì rất dễ đếm một số tới hai lần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_nhip_chan(b):
    """C11① Nhịp chân một giờ."""
    return [
        _c('bia', 'Quãng đường đi trong một giờ', so_bai(b),
           loi=['Trước khi hỏi gì thêm, phải biết một con số đã.']),
        _c('de_toan', 'Xe chạy đều, 3 giờ đi được 120 km.',
           'Hỏi mỗi giờ xe đi được bao nhiêu ki-lô-mét?',
           loi=['Một xe chạy đều, ba giờ đi được một trăm hai mươi ki lô mét.']),
        _c('y_toan', 'Chạy ĐỀU nghĩa là gì',
           'Giờ nào cũng đi được bằng nhau — không giờ nhanh giờ chậm.',
           buoc=1, soBuoc=3,
           loi=['Chạy đều nghĩa là giờ nào xe cũng đi được đúng bằng nhau.',
                'Không có giờ nhanh giờ chậm.']),
        _c('so_do_doan', 'Ba giờ chia đường thành ba khúc bằng nhau',
           be=1, lon=3, phanLon=3, nhanBe='một giờ', nhanLon='ba giờ',
           chuTong='120 km', chuPhu='Mỗi khúc là quãng đường đi trong một giờ.',
           loi=['Ba giờ chia đường thành ba khúc bằng nhau.',
                'Mỗi khúc chính là quãng đường đi trong một giờ.']),
        _c('y_toan', 'Vậy chia đều ra', '120 : 3 = 40 ki-lô-mét',
           buoc=2, soBuoc=3,
           loi=['Một trăm hai mươi chia ba bằng bốn mươi ki lô mét.']),
        _c('y_toan', 'Con số ấy là tấm căn cước của chiếc xe',
           'Biết nó rồi thì hỏi gì cũng trả lời được.', buoc=3, soBuoc=3,
           loi=['Bốn mươi ấy là tấm căn cước của chiếc xe.',
                'Biết nó rồi thì hỏi quãng đường, hỏi thời gian, hay so với xe khác '
                'đều làm được.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Một giờ phải đi ÍT HƠN ba giờ — nên CHIA.',
           loi=['Con nhớ chỗ này. Một giờ phải đi ít hơn ba giờ.',
                'Nên phải chia chứ không nhân.']),
        _c('cong_thuc', 'Rút về đơn vị',
           congThuc='quãng đường một giờ  =  quãng đường  :  số giờ',
           thay='120 : 3 = 40 ki-lô-mét',
           loi=['Quãng đường một giờ bằng quãng đường chia cho số giờ.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='tìm con số MỘT GIỜ trước mọi câu hỏi khác',
           loi=['Con nhớ lại một lần nữa. Tìm con số một giờ trước đã.',
                'Chưa có nó thì mấy bài sau đều tắc.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_xuoi_nguoc(b):
    """C11② Biết một giờ thì tính được mọi giờ."""
    return [
        _c('bia', 'Hai chiều xuôi và ngược', so_bai(b),
           loi=['Có con số một giờ rồi, nay đem dùng.']),
        _c('y_toan', 'Chiều XUÔI: hỏi quãng đường',
           'Mỗi giờ một khúc 40 km, năm giờ là năm khúc.', buoc=1, soBuoc=3,
           loi=['Chiều xuôi là hỏi quãng đường. Mỗi giờ một khúc bốn mươi ki lô mét.',
                'Năm giờ là năm khúc như thế.']),
        _c('y_toan', 'Nhân lên', '40 × 5 = 200 ki-lô-mét', buoc=2, soBuoc=3,
           loi=['Bốn mươi nhân năm bằng hai trăm ki lô mét.']),
        _c('y_toan', 'Chiều NGƯỢC: hỏi thời gian',
           '200 km chứa được mấy khúc 40?', buoc=3, soBuoc=3,
           loi=['Chiều ngược là hỏi thời gian. Hai trăm ki lô mét chứa được mấy khúc '
                'bốn mươi.',
                'Hai trăm chia bốn mươi bằng năm giờ.']),
        _c('y_toan', 'Hai chiều ngược nhau',
           'Hỏi quãng đường thì NHÂN. Hỏi thời gian thì CHIA.',
           loi=['Hai chiều ngược nhau. Hỏi quãng đường thì nhân, hỏi thời gian thì '
                'chia.']),
        _c('y_toan', 'Chốt lộ trình', 'Xuất phát 7 giờ, đi 5 giờ → tới lúc 12 giờ',
           loi=['Xuất phát lúc bảy giờ, đi hết năm giờ, vậy tới nơi lúc mười hai giờ '
                'trưa.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Hỏi thời gian mà đem nhân thì ra tám nghìn giờ — gần một năm.',
           loi=['Con nhớ chỗ này. Hỏi thời gian mà đem nhân thì ra tám nghìn giờ.',
                'Gần một năm. Một chuyến xe đâu có đi lâu thế.']),
        _c('cong_thuc', 'Ba việc từ một con số',
           congThuc='quãng đường = một giờ × số giờ   ·   số giờ = quãng đường : một giờ',
           thay='giờ đến = giờ xuất phát + số giờ',
           loi=['Quãng đường bằng con số một giờ nhân số giờ. Số giờ thì chia ngược '
                'lại.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ƯỚC LƯỢNG trước bằng lời  ·  rồi mới tính',
           loi=['Con nhớ lại một lần nữa. Ước lượng trước bằng lời rồi mới tính.',
                'Đáp số lệch quá xa ước lượng là biết mình làm nhầm phép.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_so_hai_xe(b):
    """C11③ So hai xe phải quy về cùng một giờ."""
    return [
        _c('bia', 'So hai xe', so_bai(b),
           loi=['Xe này ba giờ đi trăm hai, xe kia hai giờ đi chín mươi. Xe nào nhanh '
                'hơn.']),
        _c('y_toan', 'Cái bẫy',
           '120 lớn hơn 90 — nhưng hai con số ấy đo trong SỐ GIỜ KHÁC NHAU.',
           buoc=1, soBuoc=3,
           loi=['Một trăm hai mươi lớn hơn chín mươi, nên nhiều bạn kết luận ngay.',
                'Nhưng hai con số ấy đo trong số giờ khác nhau.']),
        _c('y_toan', 'Giống so hai bạn ăn cơm',
           'Một bạn ba bát trong ba bữa, một bạn hai bát trong một bữa.',
           loi=['Giống như so hai bạn ăn cơm. Một bạn ăn ba bát trong ba bữa.',
                'Một bạn ăn hai bát trong một bữa. So thẳng thì vô nghĩa.']),
        _c('y_toan', 'Quy cả hai về MỘT GIỜ',
           '120 : 3 = 40   ·   90 : 2 = 45', buoc=2, soBuoc=3,
           loi=['Quy cả hai về một giờ. Xe buýt bốn mươi, xe chở đồ bốn mươi lăm.']),
        _c('y_toan', 'Nay mới so được',
           'Xe chở đồ nhanh hơn, hơn 5 ki-lô-mét mỗi giờ.', buoc=3, soBuoc=3,
           loi=['Nay mới so được. Bốn mươi lăm lớn hơn bốn mươi.',
                'Xe chở đồ mới là xe nhanh hơn, hơn năm ki lô mét mỗi giờ.']),
        _c('y_toan', 'Bài học chung',
           'Muốn so hai thứ thì đưa chúng về CÙNG MỘT THƯỚC ĐO.',
           loi=['Muốn so hai thứ thì phải đưa chúng về cùng một thước đo.',
                'So giá ngoài chợ cũng thế: gói nửa cân với gói một cân, phải quy về '
                'cùng đơn vị.']),
        _c('cong_thuc', 'So hai chuyển động',
           congThuc='quy cả hai về QUÃNG ĐƯỜNG MỘT GIỜ  ·  rồi mới so',
           thay='120 : 3 = 40   và   90 : 2 = 45',
           loi=['Quy cả hai về quãng đường một giờ, rồi mới so.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi trước: hai bên đã CÙNG THƯỚC ĐO chưa',
           loi=['Con nhớ lại một lần nữa. Trước khi so cái gì, hỏi xem hai bên đã cùng '
                'thước đo chưa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_duoi_kip(b):
    """C11④ Đuổi kịp."""
    return [
        _c('bia', 'Bài toán đuổi kịp', so_bai(b),
           loi=['Xe đồ đi trước một quãng, xe buýt đuổi theo. Bao lâu thì bắt kịp.']),
        _c('de_toan', 'Xe đồ đi trước 30 km, mỗi giờ đi 30 km.',
           'Xe buýt đuổi theo cùng chiều, mỗi giờ đi 40 km.',
           loi=['Xe chở đồ đi trước ba mươi ki lô mét, mỗi giờ đi ba mươi.',
                'Xe buýt đuổi theo cùng chiều, mỗi giờ đi bốn mươi.']),
        _c('y_toan', 'Lập bảng cho dễ thấy',
           'Đầu: cách 30  ·  sau 1 giờ: còn 20  ·  sau 2 giờ: còn 10  ·  sau 3 giờ: 0',
           buoc=1, soBuoc=3,
           loi=['Lúc xuất phát hai xe cách nhau ba mươi ki lô mét.',
                'Sau một giờ còn hai mươi. Sau hai giờ còn mười. Sau ba giờ còn không.']),
        _c('y_toan', 'Quy luật lộ ra',
           'Mỗi giờ khép được đúng 10 — mà 10 chính là 40 trừ 30.', buoc=2, soBuoc=3,
           loi=['Mỗi giờ khoảng cách khép lại đúng mười ki lô mét.',
                'Mà mười chính là bốn mươi trừ ba mươi, tức hiệu hai nhịp chân.']),
        _c('y_toan', 'Nên chia cho HIỆU', '30 : 10 = 3 giờ', buoc=3, soBuoc=3,
           loi=['Nên thời gian đuổi kịp bằng khoảng cách chia cho hiệu.',
                'Ba mươi chia mười bằng ba giờ.']),
        _c('y_toan', 'Kiểm bằng hai cột quãng đường',
           'Buýt đi 40 × 3 = 120  ·  xe đồ đi 30 × 3 = 90, cộng 30 đi trước = 120',
           loi=['Lúc kịp, xe buýt đã đi một trăm hai mươi.',
                'Xe đồ đi chín mươi, cộng ba mươi đi trước cũng là một trăm hai mươi.',
                'Hai xe đứng đúng một chỗ.']),
        _c('cong_thuc', 'Bài toán đuổi kịp',
           congThuc='thời gian  =  khoảng cách  :  HIỆU hai nhịp',
           thay='30 : (40 − 30) = 3 giờ',
           loi=['Thời gian đuổi kịp bằng khoảng cách chia cho hiệu hai nhịp chân.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='người đi trước KHÔNG đứng yên  ·  nên chỉ khép được phần HƠN',
           loi=['Con nhớ lại một lần nữa. Người đi trước không đứng yên.',
                'Nên mỗi giờ chỉ khép được phần hơn, tức là hiệu.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_gap_nhau(b):
    """C11⑤ Gặp nhau."""
    return [
        _c('bia', 'Bài toán gặp nhau', so_bai(b),
           loi=['Nay hai xe từ hai đầu chạy vào nhau. Đổi một dấu thôi.']),
        _c('de_toan', 'Hai đầu quãng đường 180 km, hai xe cùng lúc chạy vào nhau.',
           'Xe thứ nhất 25 km mỗi giờ, xe thứ hai 35 km mỗi giờ.',
           loi=['Hai đầu một quãng đường dài một trăm tám mươi ki lô mét.',
                'Hai xe cùng lúc chạy vào nhau, xe thứ nhất hai mươi lăm, xe thứ hai '
                'ba mươi lăm.']),
        _c('y_toan', 'Lần này không ai chạy trốn',
           'Cả hai cùng lao vào, nên góp cả hai phần.', buoc=1, soBuoc=3,
           loi=['Lần này không ai chạy trốn cả. Cả hai cùng lao vào nhau.',
                'Nên quãng đường ngắn lại cả hai phần.']),
        _c('y_toan', 'Mỗi giờ gần thêm bằng TỔNG', '25 + 35 = 60 ki-lô-mét',
           buoc=2, soBuoc=3,
           loi=['Mỗi giờ hai xe gần thêm nhau hai mươi lăm cộng ba mươi lăm, bằng sáu '
                'mươi ki lô mét.']),
        _c('y_toan', 'Chia ra là xong', '180 : 60 = 3 giờ', buoc=3, soBuoc=3,
           loi=['Cả quãng đường một trăm tám mươi, mỗi giờ nuốt được sáu mươi.',
                'Một trăm tám mươi chia sáu mươi bằng ba giờ.']),
        _c('y_toan', 'Kiểm bằng hai cột quãng đường',
           '25 × 3 = 75  ·  35 × 3 = 105  ·  75 + 105 = 180',
           loi=['Xe thứ nhất đi bảy mươi lăm, xe thứ hai đi một trăm linh năm.',
                'Cộng lại vừa đúng cả quãng đường.']),
        _c('cong_thuc', 'Hai bài ngược nhau',
           congThuc='CÙNG chiều → chia HIỆU      ·      NGƯỢC chiều → chia TỔNG',
           thay='180 : (25 + 35) = 3 giờ',
           loi=['Cùng chiều thì chia hiệu. Ngược chiều thì chia tổng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi TRƯỚC: cùng chiều hay ngược chiều',
           loi=['Con nhớ lại một lần nữa. Hỏi trước xem hai xe cùng chiều hay ngược '
                'chiều.',
                'Hỏi xong rồi mới chọn phép tính.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb_kim_dong_ho(b):
    """C11⑥ Góc giữa hai kim đồng hồ — bài cuối quyển."""
    return [
        _c('bia', 'Góc giữa hai kim đồng hồ', so_bai(b),
           loi=['Bài cuối quyển, và nó bắt tay với bài bốn loại góc.']),
        _c('y_toan', 'Mặt đồng hồ là một cái thước',
           'Mười hai con số chia vòng tròn thành 12 khấc bằng nhau.',
           buoc=1, soBuoc=3,
           loi=['Mười hai con số chia vòng tròn thành mười hai khấc bằng nhau.']),
        _c('goc', 'Ướm ê ke vào: góc vuông phủ từ số 12 tới số 3',
           'Đúng 3 khấc.', do=90, eKe=True, ten='3 KHẤC = GÓC VUÔNG',
           loi=['Ướm ê ke vào thì thấy góc vuông phủ từ số mười hai tới số ba.',
                'Đúng ba khấc.']),
        _c('goc', 'Nửa vòng thì đúng 6 khấc', 'Hai kim duỗi thẳng.',
           do=180, eKe=True, ten='6 KHẤC = GÓC BẸT',
           loi=['Nửa vòng là góc bẹt, và nửa vòng thì đúng sáu khấc. Hai kim duỗi '
                'thẳng.']),
        _c('y_toan', 'Giờ đúng thì kim phút luôn ở số 12',
           'Nên chỉ cần đếm khấc từ số 12 tới kim giờ.', buoc=2, soBuoc=3,
           loi=['Giờ đúng thì kim phút luôn chỉ số mười hai.',
                'Nên chỉ cần đếm khấc từ số mười hai tới kim giờ.']),
        _c('y_toan', 'Điểm danh cả mặt đồng hồ',
           'dưới 3 khấc: nhọn  ·  đúng 3: vuông  ·  4 tới 5: tù  ·  đúng 6: bẹt',
           buoc=3, soBuoc=3,
           loi=['Dưới ba khấc thì góc nhọn. Đúng ba khấc là vuông.',
                'Từ bốn tới năm khấc là tù. Đúng sáu khấc là bẹt.']),
        _c('y_toan', 'Quá 6 khấc thì đếm phía NGẮN',
           'Lúc 7 giờ đếm ngược chỉ 5 khấc → vẫn là góc tù.',
           loi=['Quá sáu khấc thì đếm phía ngắn.',
                'Lúc bảy giờ, đếm ngược chỉ năm khấc, nên vẫn là góc tù, giống lúc năm '
                'giờ.']),
        _c('cong_thuc', 'Mặt đồng hồ là thước đo góc',
           congThuc='góc vuông = 3 khấc      ·      góc bẹt = 6 khấc',
           thay='3 giờ và 9 giờ đều cho góc vuông',
           loi=['Góc vuông là ba khấc, góc bẹt là sáu khấc.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='góc giữa hai kim luôn lấy phía NGẮN',
           loi=['Con nhớ lại một lần nữa. Góc giữa hai kim luôn lấy phía ngắn.',
                'Đó là bài cuối cùng của quyển. Con giỏi lắm.']),
        _c('ket', 'Con học xong cả quyển rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con học xong cả quyển rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 1 · VƯƠNG QUỐC SỐ — mười kịch bản
#
# Bác chốt: video KHÔNG nhân vật, giống hệt lớp 4. Nhưng lời đọc cho bé 7 tuổi
# thì phải ngắn hơn nữa và dùng chữ quen hơn — "phòng" chứ không "hàng", "to gấp
# mười" chứ không "gấp mười lần giá trị".
# ═══════════════════════════════════════════════════════════════════════════

def kb2_ba_phong(b):
    """C1① Ba phòng của một số."""
    return [
        _c('bia', 'Ba phòng của một số', so_bai(b),
           loi=['Số có ba chữ số ở trong một ngôi nhà ba phòng.']),
        _c('bang_hang', 'Bên trái là phòng TRĂM', so='245', hienLop=False,
           chuPhu='Ở giữa là phòng chục, bên phải là phòng đơn vị.',
           loi=['Bên trái là phòng trăm. Ở giữa là phòng chục. Bên phải là phòng đơn '
                'vị.']),
        _c('bang_hang', 'Chữ số 2 ngồi phòng trăm', so='245', toSang=[2],
           hienLop=False, chuPhu='Nó đứng ngoài cùng bên trái.',
           loi=['Xếp số hai trăm bốn mươi lăm vào nhà.',
                'Chữ số hai ngồi phòng trăm, vì nó đứng ngoài cùng bên trái.']),
        _c('bang_hang', 'Chữ số 4 ngồi phòng chục', so='245', toSang=[1],
           hienLop=False, chuPhu='Nó đứng ở giữa.',
           loi=['Chữ số bốn ngồi phòng chục, vì nó đứng ở giữa.']),
        _c('bang_hang', 'Chữ số 5 ngồi phòng đơn vị', so='245', toSang=[0],
           hienLop=False, chuPhu='Nó đứng ngoài cùng bên phải.',
           loi=['Chữ số năm ngồi phòng đơn vị, vì nó đứng ngoài cùng bên phải.']),
        _c('y_toan', 'Đáp số', '2 trăm · 4 chục · 5 đơn vị',
           loi=['Vậy số này có hai trăm, bốn chục, năm đơn vị.']),
        _c('cong_thuc', 'Ngôi nhà ba phòng',
           congThuc='trăm  ·  chục  ·  đơn vị',
           thay='đọc từ TRÁI sang phải',
           loi=['Ba phòng là trăm, chục, đơn vị. Đọc từ trái sang phải.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='phòng đơn vị luôn ở NGOÀI CÙNG BÊN PHẢI',
           loi=['Con nhớ lại một lần nữa. Phòng đơn vị luôn ở ngoài cùng bên phải.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_gia_tri(b):
    """C1② Mỗi chữ số đáng bao nhiêu."""
    return [
        _c('bia', 'Mỗi chữ số đáng bao nhiêu', so_bai(b),
           loi=['Chữ số đáng bao nhiêu là do phòng nó ngồi.']),
        _c('bang_hang', 'Chữ số 2 ở phòng trăm nên đáng 200', so='245', toSang=[2],
           hienLop=False, chuPhu='Không phải đáng 2 đâu.',
           loi=['Chữ số hai ngồi phòng trăm nên nó đáng hai trăm. Không phải đáng '
                'hai.']),
        _c('bang_hang', 'Chữ số 4 ở phòng chục nên đáng 40', so='245', toSang=[1],
           hienLop=False, chuPhu='Bốn thanh chục.',
           loi=['Chữ số bốn ngồi phòng chục nên nó đáng bốn mươi.']),
        _c('bang_hang', 'Chữ số 5 ở phòng đơn vị nên đáng 5', so='245', toSang=[0],
           hienLop=False, chuPhu='Năm hạt lẻ.',
           loi=['Chữ số năm ngồi phòng đơn vị nên nó chỉ đáng năm.']),
        _c('y_toan', 'Mở cửa từng phòng rồi cộng lại',
           '200 + 40 + 5 = 245', buoc=1, soBuoc=2,
           loi=['Mở cửa từng phòng rồi cộng lại. Hai trăm, cộng bốn mươi, cộng năm.',
                'Được đúng số ban đầu.']),
        _c('bang_hang', 'Khi có phòng trống', so='507', toSang=[1], hienLop=False,
           chuPhu='507 tách ra là 500 + 7.',
           chuCuoi='Nhưng khi VIẾT SỐ thì chữ số 0 vẫn phải có.',
           loi=['Số năm trăm linh bảy có phòng chục trống.',
                'Tách ra chỉ còn năm trăm cộng bảy.',
                'Nhưng khi viết số thì chữ số không vẫn phải có, không thì còn lại năm '
                'mươi bảy.']),
        _c('cong_thuc', 'Tách số thành tổng',
           congThuc='245  =  200  +  40  +  5',
           thay='tách theo cái mỗi chữ số ĐÁNG',
           loi=['Tách số là tách theo cái mỗi chữ số đáng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='KHÔNG phải 2 + 4 + 5',
           loi=['Con nhớ lại một lần nữa. Không phải tách rời từng chữ số ra cộng.',
                'Cộng thế thì chỉ được mười một thôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_so_sanh(b):
    """C1③ So hai số."""
    return [
        _c('bia', 'So hai số', so_bai(b),
           loi=['So hai số thì nhìn phòng bên trái trước.']),
        _c('bang_hang', 'Số thứ nhất', so='245', toSang=[2], hienLop=False,
           chuPhu='Phòng trăm có chữ số 2.',
           loi=['Số thứ nhất là hai trăm bốn mươi lăm. Phòng trăm của nó có chữ số '
                'hai.']),
        _c('bang_hang', 'Số thứ hai', so='198', toSang=[2], hienLop=False,
           chuPhu='Phòng trăm chỉ có chữ số 1.',
           loi=['Số thứ hai là một trăm chín mươi tám. Phòng trăm chỉ có chữ số một.']),
        _c('y_toan', 'Hai lớn hơn một', 'Nên 245 lớn hơn 198.', buoc=1, soBuoc=3,
           loi=['Hai lớn hơn một, nên số thứ nhất lớn hơn.',
                'Không cần nhìn hai phòng sau nữa. Phòng trăm đã phân thắng bại.']),
        _c('y_toan', 'Khi phòng trăm hoà nhau',
           '245 và 254 đều có 2 ở phòng trăm.', buoc=2, soBuoc=3,
           loi=['Nhưng có khi phòng trăm hoà nhau. Hai số này đều có chữ số hai ở '
                'phòng trăm.']),
        _c('y_toan', 'Thì nhìn tiếp phòng chục',
           '4 với 5 — năm lớn hơn nên 254 lớn hơn.', buoc=3, soBuoc=3,
           loi=['Khi ấy nhìn tiếp phòng chục. Bốn với năm.',
                'Năm lớn hơn bốn nên số hai trăm năm mươi tư lớn hơn.',
                'Hoà tiếp nữa thì mới nhìn phòng đơn vị.']),
        _c('cong_thuc', 'Cách so hai số',
           congThuc='so phòng TRĂM trước  ·  hoà thì so CHỤC  ·  rồi ĐƠN VỊ',
           thay='phòng bên trái luôn quyền lực hơn',
           loi=['So phòng trăm trước. Hoà thì so phòng chục, rồi mới tới phòng đơn '
                'vị.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='phòng bên trái nói TRƯỚC',
           loi=['Con nhớ lại một lần nữa. Phòng bên trái nói trước.',
                'Số nào nhiều trăm hơn thì lớn hơn, dù các chữ số sau có to đến đâu.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_them_khong(b):
    """C1④ Thêm số 0 vào bên phải."""
    return [
        _c('bia', 'Thêm số 0 vào bên phải', so_bai(b),
           loi=['Thêm một chữ số không mà số to hẳn lên.']),
        _c('bang_hang', 'Số 3 ngồi phòng đơn vị', so='3', hienLop=False, toSang=[0],
           chuPhu='Ba hạt lẻ.',
           loi=['Số ba ngồi ở phòng đơn vị. Nó chỉ đáng ba hạt.']),
        _c('bang_hang', 'Thêm số 0 — chữ số 3 bị ĐẨY sang phòng chục', so='30',
           hienLop=False, toSang=[1], chuPhu='Nay nó đáng ba chục.',
           loi=['Thêm chữ số không vào bên phải. Chữ số không chen vào phòng đơn vị.',
                'Chữ số ba bị đẩy sang phòng chục, nay nó đáng ba chục.']),
        _c('y_toan', 'Ba hạt thành ba chục hạt', '3  →  30, to gấp 10 lần',
           buoc=1, soBuoc=2,
           loi=['Ba hạt lẻ nay thành ba chục hạt. To gấp mười lần.']),
        _c('bang_hang', 'Số nào cũng thế', so='250', hienLop=False, toSang=[0],
           chuPhu='25 thêm số 0 thành 250.',
           loi=['Số nào cũng thế. Hai mươi lăm thêm chữ số không thành hai trăm năm '
                'mươi.',
                'Cả số dọn nhà sang trái một phòng.']),
        _c('y_toan', 'Chữ số 0 không đáng gì',
           'Nhưng nó ĐẨY các chữ số kia sang trái.', buoc=2, soBuoc=2,
           loi=['Con nhớ chỗ này. Bản thân chữ số không chẳng đáng gì.',
                'Nhưng nó đẩy các chữ số kia sang trái, và chính cái đẩy ấy làm số to '
                'lên.']),
        _c('cong_thuc', 'Thêm số 0 vào bên phải',
           congThuc='thêm 0  →  to gấp MƯỜI lần',
           thay='3 → 30      25 → 250',
           loi=['Thêm chữ số không vào bên phải thì số to gấp mười lần.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='cả số dọn nhà sang TRÁI một phòng',
           loi=['Con nhớ lại một lần nữa. Cả số dọn nhà sang trái một phòng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_xoa_khong(b):
    """C1⑤ Xoá số 0 tận cùng."""
    return [
        _c('bia', 'Xoá số 0 ở tận cùng', so_bai(b),
           loi=['Hôm nay mình làm ngược lại bài hôm qua.']),
        _c('bang_hang', 'Số 70 — chữ số 7 đang ngồi phòng chục', so='70',
           hienLop=False, toSang=[1], chuPhu='Nó đáng bảy chục.',
           loi=['Số bảy mươi. Chữ số bảy đang ngồi phòng chục nên nó đáng bảy chục.']),
        _c('bang_hang', 'Xoá số 0 — chữ số 7 TỤT về phòng đơn vị', so='7',
           hienLop=False, toSang=[0], chuPhu='Nay nó chỉ đáng bảy hạt.',
           loi=['Xoá chữ số không ở cuối. Mất chỗ dựa, chữ số bảy tụt về phòng đơn vị.',
                'Nay nó chỉ còn đáng bảy hạt.']),
        _c('y_toan', 'Nhỏ đi mười lần', '70  →  7', buoc=1, soBuoc=3,
           loi=['Bảy chục thành bảy hạt. Số nhỏ đi mười lần.']),
        _c('y_toan', 'Hai chiều ngược nhau',
           'Thêm 0 thì to gấp mười. Xoá 0 thì nhỏ đi mười lần.', buoc=2, soBuoc=3,
           loi=['Hai chiều ngược nhau. Thêm chữ số không thì to gấp mười.',
                'Xoá chữ số không thì nhỏ đi mười lần.']),
        _c('bang_hang', 'Nhưng chỉ xoá được ở TẬN CÙNG', so='405', hienLop=False,
           toSang=[1], chuPhu='Số 405 có chữ số 0 ở GIỮA — không xoá kiểu này được.',
           buoc=3, soBuoc=3,
           loi=['Nhưng chỉ xoá được khi chữ số không đứng ở tận cùng.',
                'Số bốn trăm linh năm có chữ số không nằm ở giữa. Xoá nó là số đổi '
                'hẳn.']),
        _c('cong_thuc', 'Xoá số 0 ở tận cùng',
           congThuc='xoá 0 ở CUỐI  →  nhỏ đi MƯỜI lần',
           thay='70 → 7      250 → 25',
           loi=['Xoá chữ số không ở cuối thì số nhỏ đi mười lần.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi trước: chữ số CUỐI CÙNG có phải số 0 không',
           loi=['Con nhớ lại một lần nữa. Hỏi trước xem chữ số cuối cùng có phải số '
                'không.',
                'Không phải thì đừng xoá.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_doi_cho(b):
    """C1⑥ Đổi chỗ hai chữ số."""
    return [
        _c('bia', 'Đổi chỗ hai chữ số', so_bai(b),
           loi=['Đổi chỗ hai thẻ số thì được số khác hẳn.']),
        _c('bang_hang', 'Số 25 — chữ số 2 ngồi phòng chục', so='25', hienLop=False,
           toSang=[1], chuPhu='Nó đáng 20. Còn chữ số 5 chỉ đáng 5.',
           loi=['Số hai mươi lăm. Chữ số hai ngồi phòng chục nên nó đáng hai mươi.',
                'Chữ số năm ngồi phòng đơn vị nên chỉ đáng năm.']),
        _c('bang_hang', 'Đổi chỗ — nay chữ số 5 chiếm phòng chục', so='52',
           hienLop=False, toSang=[1], chuPhu='Nó đáng 50.',
           loi=['Đổi chỗ hai thẻ thì được số năm mươi hai.',
                'Nay chữ số năm chiếm phòng chục, nó đáng năm mươi.']),
        _c('y_toan', 'Nên số mới lớn hơn', 'Thẻ TO đang ở phòng chục của 52.',
           buoc=1, soBuoc=3,
           loi=['Nên số mới lớn hơn số cũ. Thẻ to đang ở phòng chục của nó.']),
        _c('y_toan', 'Muốn biết số nào lớn hơn',
           'Chỉ cần hỏi: thẻ TO đang ở phòng chục của số nào.', buoc=2, soBuoc=3,
           loi=['Muốn biết số nào lớn hơn thì chỉ cần hỏi một câu.',
                'Thẻ to đang ở phòng chục của số nào. Số đó thắng.']),
        _c('bang_hang', 'Một chỗ phải cẩn thận', so='50', hienLop=False, toSang=[0],
           chuPhu='Đổi chỗ số 50 thì chữ số 0 lên đứng đầu.',
           chuCuoi='Mà số 0 không được đứng đầu.', buoc=3, soBuoc=3,
           loi=['Có một chỗ phải cẩn thận. Đổi chỗ số năm mươi thì chữ số không lên '
                'đứng đầu.',
                'Mà chữ số không thì không được đứng đầu, nên số ấy chỉ còn là số '
                'năm.']),
        _c('cong_thuc', 'Đổi chỗ hai chữ số',
           congThuc='thẻ TO ở phòng chục  →  số ấy LỚN HƠN',
           thay='25  →  52,  và 52 lớn hơn',
           loi=['Thẻ to ở phòng chục thì số ấy lớn hơn.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hai thẻ vẫn thế  ·  nhưng ĐỔI PHÒNG thì đáng khác',
           loi=['Con nhớ lại một lần nữa. Hai thẻ vẫn là hai thẻ ấy.',
                'Nhưng chúng đổi phòng, mà phòng khác nhau thì đáng khác nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hieu_bang_chin(b):
    """C1⑦ Hiệu hai số đổi chỗ."""
    return [
        _c('bia', 'Hiệu của hai số đổi chỗ', so_bai(b),
           loi=['Hôm nay con tự tìm ra một luật.']),
        _c('y_toan', 'Thử cặp đầu tiên', '52 − 25 = 27', buoc=1, soBuoc=3,
           loi=['Năm mươi hai trừ hai mươi lăm bằng hai mươi bảy.']),
        _c('y_toan', 'Thử thêm vài cặp nữa',
           '31 − 13 = 18   ·   42 − 24 = 18   ·   51 − 15 = 36', buoc=2, soBuoc=3,
           loi=['Ba mươi mốt trừ mười ba bằng mười tám.',
                'Bốn mươi hai trừ hai mươi bốn cũng bằng mười tám.',
                'Năm mươi mốt trừ mười lăm bằng ba mươi sáu.']),
        _c('y_toan', 'Con nhìn ra gì chưa',
           '18 · 27 · 36 — toàn số trong bảng nhân 9', buoc=3, soBuoc=3,
           loi=['Con nhìn ra gì chưa. Mười tám, hai mươi bảy, ba mươi sáu.',
                'Toàn là số trong bảng nhân chín.']),
        _c('tach_so', 'Đoán trước được luôn', so='52', sang=[1, 2],
           phep='5 − 2 = 3,  rồi  3 × 9 = 27',
           chuPhu='Lấy hiệu hai chữ số rồi nhân chín.',
           loi=['Đoán trước được luôn. Lấy hiệu hai chữ số rồi nhân chín.',
                'Năm trừ hai bằng ba. Ba nhân chín bằng hai mươi bảy — đúng đáp số '
                'vừa tính.']),
        _c('y_toan', 'Thử lại với một cặp mới', '71 − 17: hiệu chữ số 6, mà 6 × 9 = 54',
           loi=['Thử lại với một cặp mới. Bảy mươi mốt và mười bảy.',
                'Hiệu hai chữ số là sáu, sáu nhân chín bằng năm mươi bốn.',
                'Tính thật cũng ra năm mươi bốn.']),
        _c('cong_thuc', 'Luật con vừa tìm ra',
           congThuc='hiệu  =  hiệu hai chữ số  ×  9',
           thay='52 − 25 = 27,  mà (5 − 2) × 9 = 27',
           loi=['Hiệu bằng hiệu hai chữ số nhân chín.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='thử vài cặp rồi mới tin  ·  đó là cách người giỏi làm',
           loi=['Con nhớ lại một lần nữa. Thử vài cặp rồi mới tin.',
                'Đó chính là cách người giỏi tìm ra luật.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_xep_the(b):
    """C1⑧ Xếp thẻ để được số lớn nhất và bé nhất."""
    return [
        _c('bia', 'Xếp thẻ số', so_bai(b),
           loi=['Có ba thẻ số, xếp thế nào để được số lớn nhất.']),
        _c('y_toan', 'Nhớ lại bài đầu chương',
           'Phòng bên trái quyền lực nhất.', buoc=1, soBuoc=3,
           loi=['Nhớ lại bài đầu chương. Phòng bên trái quyền lực nhất.',
                'Muốn số lớn thì phải làm cho phòng trăm to nhất đã.']),
        _c('bang_hang', 'Số lớn nhất — xếp từ TO đến BÉ', so='852', hienLop=False,
           toSang=[2], chuPhu='Thẻ 8 vào phòng trăm, thẻ 5 vào phòng chục.',
           buoc=2, soBuoc=3,
           loi=['Xếp từ to đến bé. Thẻ tám vào phòng trăm, thẻ năm vào phòng chục, '
                'thẻ hai xuống cuối.',
                'Được số tám trăm năm mươi hai.']),
        _c('bang_hang', 'Số bé nhất — làm NGƯỢC LẠI', so='258', hienLop=False,
           toSang=[2], chuPhu='Thẻ 2 vào phòng trăm, thẻ 8 xuống cuối.',
           buoc=3, soBuoc=3,
           loi=['Số bé nhất thì làm ngược lại. Xếp từ bé đến to.',
                'Được số hai trăm năm mươi tám.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Sau thẻ TO NHẤT phải tới thẻ TO NHÌ.',
           loi=['Con nhớ chỗ hay nhầm. Sau thẻ to nhất thì phải tới thẻ to nhì.',
                'Đặt lộn hai thẻ sau là ra số bé hơn ngay.']),
        _c('y_toan', 'Thử lại', 'Đổi thử hai thẻ bất kỳ — không ra số nào lớn hơn.',
           loi=['Thử lại bằng cách đổi hai thẻ bất kỳ. Không ra số nào lớn hơn được.',
                'Vì thẻ to nhất đã nằm ở phòng quyền lực nhất rồi.']),
        _c('cong_thuc', 'Xếp thẻ số',
           congThuc='số LỚN nhất: xếp từ TO đến BÉ',
           thay='số BÉ nhất: xếp từ BÉ đến TO',
           loi=['Số lớn nhất thì xếp từ to đến bé. Số bé nhất thì làm ngược lại.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='thẻ to nhất đi vào phòng BÊN TRÁI NHẤT',
           loi=['Con nhớ lại một lần nữa. Thẻ to nhất đi vào phòng bên trái nhất.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_the_khong(b):
    """C1⑨ Khi có thẻ số 0."""
    return [
        _c('bia', 'Khi có thẻ số 0', so_bai(b),
           loi=['Lần này trong tay có một thẻ số không.']),
        _c('y_toan', 'Làm như bài trước thì sao',
           'Ba thẻ 0, 3, 7 — xếp từ bé đến to được 0, 3, 7.', buoc=1, soBuoc=3,
           loi=['Ba thẻ là không, ba, bảy. Làm như bài trước thì xếp từ bé đến to.',
                'Được không, ba, bảy.']),
        _c('bang_hang', 'Nhưng khoan đã', so='037', hienLop=False, toSang=[2],
           chuPhu='Chữ số 0 ở phòng trăm nghĩa là KHÔNG CÓ TRĂM NÀO.',
           chuCuoi='Số ấy chỉ còn là 37 — có hai chữ số thôi.',
           loi=['Nhưng khoan đã. Chữ số không ở phòng trăm nghĩa là không có trăm nào.',
                'Số ấy chỉ còn là ba mươi bảy, có hai chữ số thôi.']),
        _c('y_toan', 'Luật của thẻ số 0',
           'Không được đứng ở phòng bên trái nhất.', buoc=2, soBuoc=3,
           loi=['Vậy thẻ số không không được đứng ở phòng bên trái nhất.',
                'Nhưng các phòng còn lại thì nó vẫn ngồi được bình thường.']),
        _c('bang_hang', 'Xếp lại cho đúng', so='307', hienLop=False, toSang=[2],
           chuPhu='Thẻ bé nhất KHÁC 0 đứng đầu, rồi thẻ 0 ngồi ngay sau.',
           buoc=3, soBuoc=3,
           loi=['Xếp lại cho đúng. Cho thẻ bé nhất khác không đứng đầu, tức thẻ ba.',
                'Rồi thẻ không ngồi ngay phòng thứ hai. Được số ba trăm linh bảy.']),
        _c('y_toan', 'Còn số lớn nhất thì không vướng gì',
           'Vẫn xếp từ to đến bé: 730.',
           loi=['Còn số lớn nhất thì không vướng gì cả. Vẫn xếp từ to đến bé.',
                'Được bảy trăm ba mươi.']),
        _c('cong_thuc', 'Khi có thẻ số 0',
           congThuc='số 0 KHÔNG đứng đầu',
           thay='số bé nhất: thẻ bé nhất KHÁC 0 đứng đầu, rồi mới tới thẻ 0',
           loi=['Thẻ số không không đứng đầu. Số bé nhất thì cho thẻ bé nhất khác '
                'không đứng đầu.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số 0 chỉ kiêng phòng đầu  ·  các phòng khác vẫn ngồi được',
           loi=['Con nhớ lại một lần nữa. Số không chỉ kiêng phòng đầu thôi.',
                'Các phòng khác nó vẫn ngồi được bình thường.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_tuan_tra(b):
    """C1⑩ Tìm đủ mọi số — bài cuối chương."""
    return [
        _c('bia', 'Tìm đủ mọi số', so_bai(b),
           loi=['Tìm tất cả các số có hai chữ số mà tổng hai chữ số bằng năm.']),
        _c('y_toan', 'Kể lộn xộn thì dễ sót',
           'Nhớ ra số nào kể số ấy — dễ quên, mà cũng dễ kể trùng.',
           buoc=1, soBuoc=3,
           loi=['Nhớ ra số nào kể số ấy thì rất dễ bỏ quên, mà cũng dễ kể trùng.']),
        _c('y_toan', 'Đi tuần tra CÓ THỨ TỰ',
           'Cho hàng chục tăng dần từng nấc một.', buoc=2, soBuoc=3,
           loi=['Có cách chắc hơn. Cho hàng chục tăng dần từng nấc một.',
                'Mỗi nấc hỏi một câu: đơn vị phải là mấy thì tổng bằng năm.']),
        _c('y_toan', 'Đi từng nấc',
           'chục 1 → 14   ·   chục 2 → 23   ·   chục 3 → 32   ·   chục 4 → 41   ·   chục 5 → 50',
           buoc=3, soBuoc=3,
           loi=['Chục bằng một thì đơn vị bằng bốn, được mười bốn.',
                'Chục hai thì đơn vị ba, được hai mươi ba. Rồi ba mươi hai, bốn mươi '
                'mốt, năm mươi.']),
        _c('y_toan', 'Vì sao bắt đầu từ chục bằng 1',
           'Vì chục bằng 0 thì số 0 đứng đầu — không còn là số có hai chữ số.',
           loi=['Vì sao bắt đầu từ chục bằng một. Vì chục bằng không thì chữ số không '
                'đứng đầu.',
                'Khi ấy không còn là số có hai chữ số nữa.']),
        _c('y_toan', 'Vì sao dừng ở chục bằng 5',
           'Vì chục bằng 6 thì đơn vị phải là 5 trừ 6 — không có chữ số nào như thế.',
           loi=['Vì sao dừng ở chục bằng năm. Vì chục bằng sáu thì đơn vị phải là năm '
                'trừ sáu.',
                'Không có chữ số nào như thế cả.']),
        _c('cong_thuc', 'Tìm đủ mọi số',
           congThuc='cho hàng chục TĂNG DẦN  ·  mỗi nấc hỏi đơn vị là mấy',
           thay='tổng bằng 5  →  đủ 5 số: 14, 23, 32, 41, 50',
           loi=['Cho hàng chục tăng dần, mỗi nấc hỏi đơn vị là mấy.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='phải nói được VÌ SAO DỪNG',
           loi=['Con nhớ lại một lần nữa. Làm xong phải nói được vì sao mình dừng ở '
                'đó.',
                'Nói được thì mới chắc là không sót số nào.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


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
    # ── chương 5 · sáu bài trung bình cộng ──
    'DL:KSN4.B55': kb_tbc_la_gi, 'DL:KSN4.B21': kb_tim_tbc,
    'DL:KSN4.B56': kb_tim_tong, 'DL:KSN4.B57': kb_so_thieu,
    'DL:KSN4.B22': kb_hon_kem,  'DL:KSN4.B23': kb_them_so,
    # ── chương 6 · bảy bài tổng - hiệu ──
    'DL:KSN4.B58': kb_so_do,     'DL:KSN4.B24': kb_so_lon,
    'DL:KSN4.B59': kb_so_be,     'DL:KSN4.B25': kb_giau_tong,
    'DL:KSN4.B26': kb_giau_hieu, 'DL:KSN4.B27': kb_cung_them,
    'DL:KSN4.B60': kb_ba_so,
    # ── chương 7 · bảy bài tỉ số ──
    'DL:KSN4.B61': kb_ti_la_gi,  'DL:KSN4.B28': kb_tong_ti,
    'DL:KSN4.B30': kb_hieu_ti,   'DL:KSN4.B62': kb_giau_ti,
    'DL:KSN4.B29': kb_giau_tong_ti, 'DL:KSN4.B31': kb_ba_so_ti,
    'DL:KSN4.B63': kb_noi_ti,
    # ── chương 8 · đợt một, năm bài đầu ──
    'DL:KSN4.B32': kb_tuoi_mot,  'DL:KSN4.B64': kb_tuoi_hai,
    'DL:KSN4.B33': kb_lam_chung, 'DL:KSN4.B65': kb_mot_nguoi_nghi,
    'DL:KSN4.B34': kb_tinh_nguoc,
    # ── chương 8 · đợt hai ──
    'DL:KSN4.B35': kb_gia_thiet, 'DL:KSN4.B36': kb_khu,
    'DL:KSN4.B66': kb_the,       'DL:KSN4.B37': kb_ven,
    'DL:KSN4.B67': kb_chuong_tho,
    # ── chương 9 · mười một bài phân số ──
    'DL:KSN4.B68': kb_ps_la_gi,  'DL:KSN4.B38': kb_so_de,
    'DL:KSN4.B69': kb_quy_dong,  'DL:KSN4.B70': kb_so_nhanh,
    'DL:KSN4.B39': kb_tim_ps,    'DL:KSN4.B71': kb_tim_so,
    'DL:KSN4.B40': kb_day_tong,  'DL:KSN4.B72': kb_day_tich,
    'DL:KSN4.B41': kb_cung_them_ps, 'DL:KSN4.B73': kb_chuyen_ps,
    'DL:KSN4.B42': kb_ps_thuc_te,
    # ── chương 10 · đợt một, sáu bài chu vi và diện tích ──
    'DL:KSN4.B74': kb_cv_dt,     'DL:KSN4.B43': kb_hai_ct,
    'DL:KSN4.B75': kb_don_vi,    'DL:KSN4.B76': kb_tim_canh,
    'DL:KSN4.B44': kb_tang_mot,  'DL:KSN4.B77': kb_tang_giam,
    # ── chương 10 · đợt hai, sáu bài góc, hình và khối ──
    'DL:KSN4.B45': kb_bon_goc,   'DL:KSN4.B78': kb_duong_cao,
    'DL:KSN4.B79': kb_cat_ghep,  'DL:KSN4.B80': kb_hinh_tron,
    'DL:KSN4.B46': kb_trai_phang, 'DL:KSN4.B81': kb_dem_khoi,
    # ── chương 1 · tám bài số đến lớp triệu ──
    'DL:KSN4.B01': kb_doc_so,      'DL:KSN4.B82': kb_gia_tri,
    'DL:KSN4.B83': kb_bang_liet_ke, 'DL:KSN4.B02': kb_them_phai,
    'DL:KSN4.B84': kb_them_trai,   'DL:KSN4.B03': kb_thang_may,
    'DL:KSN4.B85': kb_xoa_chu_so,  'DL:KSN4.B04': kb_trao_chu_so,
    # ── chương 2 · mười một bài bốn phép tính và đếm ──
    'DL:KSN4.B05': kb_thua_so_chung, 'DL:KSN4.B86': kb_nham_25,
    'DL:KSN4.B87': kb_nham_11,      'DL:KSN4.B88': kb_thua_so_0,
    'DL:KSN4.B06': kb_gom_x,        'DL:KSN4.B89': kb_boc_ngoac,
    'DL:KSN4.B90': kb_x_chia_du,    'DL:KSN4.B07': kb_dem_cach_deu,
    'DL:KSN4.B91': kb_dem_trang,    'DL:KSN4.B08': kb_quy_tac_nhan,
    'DL:KSN4.B92': kb_phan_bu,
    # ── chương 11 · sáu bài quãng đường, khép lại cả quyển ──
    'DL:KSN4.B47': kb_nhip_chan,    'DL:KSN4.B93': kb_xuoi_nguoc,
    'DL:KSN4.B94': kb_so_hai_xe,    'DL:KSN4.B48': kb_duoi_kip,
    'DL:KSN4.B95': kb_gap_nhau,     'DL:KSN4.B49': kb_kim_dong_ho,
    # ══ LỚP 2 · chương 1 · Vương quốc Số — mười bài ══
    'DL:KSN2.B01': kb2_ba_phong,    'DL:KSN2.B34': kb2_gia_tri,
    'DL:KSN2.B35': kb2_so_sanh,     'DL:KSN2.B02': kb2_them_khong,
    'DL:KSN2.B36': kb2_xoa_khong,   'DL:KSN2.B03': kb2_doi_cho,
    'DL:KSN2.B37': kb2_hieu_bang_chin, 'DL:KSN2.B04': kb2_xep_the,
    'DL:KSN2.B38': kb2_the_khong,   'DL:KSN2.B05': kb2_tuan_tra,
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
    bai = json.loads((_thu_muc(ma) / f'{ma}.json').read_text('utf8'))
    lam = BO.get(bai['id'])
    if not lam:
        raise SystemExit(f'{bai["id"]}: chưa viết kịch bản video cho bài này')
    ds = lam(bai)
    xau = soi(ds, bai['id'])
    if xau:
        raise SystemExit('\n'.join('  ✗ ' + x for x in xau))
    return {'bai': bai['id'], 'tep': f'{ma}_giang.mp4', 'canh': ds}
