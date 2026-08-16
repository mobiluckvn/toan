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
# ⚠ `KSN5Q1` phải đứng TRƯỚC — không thì `KSN2` không khớp nhưng một mã lớp 5 nào
# đó chứa chuỗi khác lại khớp nhầm. Thư mục nguồn của lớp 5 tên là `lessons`, không
# theo nếp `lop<n>` của ba quyển kia.
QUYEN_CUA = {'KSN5Q1': 'lessons', 'KSN2': 'lop2', 'KSN3': 'lop3', 'KSN4': 'lop4'}


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
    # ── LỚP 5 ĐÁNH SỐ KHÁC ──
    # Mã bài đã mang sẵn số: `DL:KSN5Q1.B1.M2` là bài 1 phần 2. Màn hình cũng suy
    # đúng thế (`soBaiCua` trong noiDung.js), nên đừng dựng thêm `thu_tu.json` cho
    # quyển này — hai nguồn số bài là hai chỗ để lệch nhau.
    m5 = re.match(r'DL:KSN5Q1\.B(\d+)\.M(\d+)', b['id'])
    if m5:
        return f'Bài {m5.group(1)} · phần {m5.group(2)}'
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
        _c('nhom_deu', 'Đối chiếu với cách viết sai', tong=14, moiNhom=4,
           chuPhu='Có bạn viết 14 : 4 = 2 (dư 6) — con đếm lại hình mà xem',
           soSai=[6],
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
        _c('nhom_deu', 'Hai giờ làm chung được 6 phần', tong=6, moiNhom=3,
           chuPhu='Mỗi giờ 3 phần, hai giờ là 6 phần.',
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
           chuPhu='50 000 + 2 000 + 600 + 4',
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
           chuCuoi='Mà số 0 không được đứng đầu.',
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
           loi=['Xếp từ to đến bé. Thẻ tám vào phòng trăm, thẻ năm vào phòng chục, '
                'thẻ hai xuống cuối.',
                'Được số tám trăm năm mươi hai.']),
        _c('bang_hang', 'Số bé nhất — làm NGƯỢC LẠI', so='258', hienLop=False,
           toSang=[2], chuPhu='Thẻ 2 vào phòng trăm, thẻ 8 xuống cuối.',
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



def kb2_dem_khoang(b):
    """C2① Đếm từ đâu đến đâu."""
    return [
        _c('bia', 'Đếm từ đâu đến đâu', so_bai(b),
           loi=['Đếm số nhà trên một dãy phố, mà phép trừ lại ra thiếu.']),
        _c('y_toan', 'Đếm thẳng tay xem sao',
           'nhà 3 · nhà 4 · nhà 5 · nhà 6 · nhà 7  →  5 nhà', buoc=1, soBuoc=3,
           loi=['Đếm thẳng tay: nhà ba, nhà bốn, nhà năm, nhà sáu, nhà bảy.',
                'Đúng năm nhà.']),
        _c('y_toan', 'Nhưng phép trừ lại ra bốn', '7 − 3 = 4', buoc=2, soBuoc=3,
           loi=['Nhưng bảy trừ ba lại bằng bốn. Lệch mất một nhà.']),
        _c('y_toan', 'Vì phép trừ chỉ đếm BƯỚC NHẢY',
           'Nhà đầu tiên chưa nhảy đã đứng sẵn ở đó.', buoc=3, soBuoc=3,
           loi=['Vì phép trừ chỉ đếm bước nhảy từ nhà nọ sang nhà kia.',
                'Mà nhà đầu tiên thì chưa nhảy bước nào đã đứng sẵn ở đó rồi.']),
        _c('y_toan', 'Nên phải thêm một', '7 − 3 = 4, thêm 1 được 5',
           loi=['Nên phải thêm một. Bảy trừ ba bằng bốn, thêm một được năm.',
                'Đáp số là năm ngôi nhà.']),
        _c('y_toan', 'Giống đếm bậc cầu thang',
           'Từ bậc 1 lên bậc 5: bước bốn bước, mà bậc thì năm.',
           loi=['Giống đếm bậc cầu thang. Từ bậc một lên bậc năm thì bước bốn bước.',
                'Nhưng bậc thì có năm.']),
        _c('cong_thuc', 'Đếm từ đâu đến đâu',
           congThuc='số cuối  −  số đầu  +  1',
           thay='7 − 3 = 4,  thêm 1  →  5 nhà',
           loi=['Lấy số cuối trừ số đầu, rồi thêm một.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ĐỪNG QUÊN thêm một',
           loi=['Con nhớ lại một lần nữa. Đừng quên thêm một.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_nhay_coc(b):
    """C2② Đếm nhảy cóc."""
    return [
        _c('bia', 'Đếm nhảy cóc', so_bai(b),
           loi=['Không đếm từng số một, mà mỗi lần nhảy qua một quãng đều nhau.']),
        _c('y_toan', 'Dãy cách hai', '2 · 4 · 6 · 8 · 10 · 12', buoc=1, soBuoc=3,
           loi=['Hai, bốn, sáu, rồi tám, mười, mười hai. Mỗi lần thêm hai.']),
        _c('y_toan', 'Dãy này toàn số CHẴN',
           'Bắt đầu từ 1 thì được dãy số LẺ: 1 · 3 · 5 · 7 · 9', buoc=2, soBuoc=3,
           loi=['Dãy này toàn số chẵn.',
                'Bắt đầu từ một thì được dãy số lẻ: một, ba, năm, bảy, chín.']),
        _c('y_toan', 'Dãy cách năm', '5 · 10 · 15 · 20 · 25 · 30', buoc=3, soBuoc=3,
           loi=['Năm, mười, mười lăm, rồi hai mươi, hai mươi lăm, ba mươi.',
                'Chính là bảng nhân năm con đã thuộc.']),
        _c('y_toan', 'Đếm dãy nhảy cóc',
           'Từ 2 đến 10 cách hai: 2, 4, 6, 8, 10 — đúng 5 số.',
           loi=['Đếm dãy nhảy cóc thì cứ lần theo từng nấc một.',
                'Từ hai đến mười, đếm cách hai được đúng năm số.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Nhảy được mấy bước rồi thì lần sau vẫn nhảy đúng bấy nhiêu.',
           loi=['Con nhớ chỗ này. Nhảy cóc thì lần nào cũng nhảy đúng bằng nhau.',
                'Đang nhảy năm một mà tự dưng nhảy một bước là hỏng.']),
        _c('cong_thuc', 'Hai dãy nhảy cóc quen thuộc',
           congThuc='cách 2:  2 · 4 · 6 · 8 · 10',
           thay='cách 5:  5 · 10 · 15 · 20  —  chính là bảng nhân 5',
           loi=['Dãy cách hai và dãy cách năm là hai dãy con gặp nhiều nhất.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='mỗi lần nhảy ĐỀU BẰNG NHAU',
           loi=['Con nhớ lại một lần nữa. Mỗi lần nhảy đều bằng nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hai_canh(b):
    """C2③ Truy tìm chữ số — chia hai cánh quân."""
    return [
        _c('bia', 'Chữ số trốn ở đâu', so_bai(b),
           loi=['Một chữ số trốn được ở hai chỗ khác nhau.']),
        _c('bang_hang', 'Trốn ở hàng ĐƠN VỊ', so='35', hienLop=False, toSang=[0],
           chuPhu='Số có đuôi bằng 5.',
           loi=['Chỗ thứ nhất là hàng đơn vị, tức là số có đuôi bằng năm.']),
        _c('bang_hang', 'Trốn ở hàng CHỤC', so='53', hienLop=False, toSang=[1],
           chuPhu='Số thuộc phố 50.',
           loi=['Chỗ thứ hai là hàng chục, tức là số thuộc phố năm mươi.']),
        _c('y_toan', 'Cánh thứ nhất: các số đuôi 5',
           '5 · 15 · 25 · 35 · 45 · 55 · 65 · 75 · 85 · 95', buoc=1, soBuoc=3,
           loi=['Cánh thứ nhất gồm các số đuôi năm. Mỗi chục đúng một bạn.',
                'Từ chục không tới chục chín, được mười số.']),
        _c('y_toan', 'Cánh thứ hai: phố 50', '50 · 51 · … · 59', buoc=2, soBuoc=3,
           loi=['Cánh thứ hai là cả phố năm mươi, từ năm mươi tới năm mươi chín.']),
        _c('y_toan', 'Đếm phố bằng mẹo bài trước',
           '59 − 50 = 9, thêm 1 được 10 số', buoc=3, soBuoc=3,
           loi=['Đếm phố bằng mẹo bài trước. Năm mươi chín trừ năm mươi bằng chín, '
                'thêm một được mười số.']),
        _c('cong_thuc', 'Truy tìm một chữ số',
           congThuc='chia HAI CÁNH: cánh ĐUÔI · cánh PHỐ',
           thay='cánh đuôi 10 số  ·  cánh phố 10 số',
           loi=['Truy tìm chữ số nào cũng chia hai cánh: cánh đuôi và cánh phố.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='lùng MỘT cánh thôi là sót mất một nửa',
           loi=['Con nhớ lại một lần nữa. Lùng một cánh thôi là sót mất một nửa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_bot_mot(b):
    """C2④ Số đứng ở cả hai cánh."""
    return [
        _c('bia', 'Số đứng ở cả hai cánh', so_bai(b),
           loi=['Cộng hai cánh lại thì thừa mất một bạn.']),
        _c('y_toan', 'Cộng hai cánh đã', '10 + 10 = 20', buoc=1, soBuoc=3,
           loi=['Cánh đuôi mười số, cánh phố cũng mười số. Cộng lại được hai mươi.']),
        _c('bang_hang', 'Khoan đã — nhìn số này', so='55', hienLop=False,
           toSang=[0, 1], chuPhu='Vừa có đuôi bằng 5, vừa thuộc phố 50.',
           loi=['Khoan đã. Nhìn số năm mươi lăm xem.',
                'Nó vừa có đuôi bằng năm, vừa thuộc phố năm mươi.']),
        _c('y_toan', 'Nó bị đếm HAI lần',
           'Một lần ở cánh đuôi, một lần ở cánh phố.', buoc=3, soBuoc=3,
           loi=['Nó đứng ở cả hai cánh, nên khi cộng thì nó bị đếm hai lần.',
                'Một lần ở cánh đuôi, một lần ở cánh phố.']),
        _c('y_toan', 'Bớt một lần đi', '20 − 1 = 19',
           loi=['Bớt một lần đi. Hai mươi bớt một còn mười chín.',
                'Đáp số là mười chín số.']),
        _c('y_toan', 'Chữ số nào cũng thế',
           'Với chữ số 3 thì số đứng cả hai cánh là 33 — cũng ra 19.',
           loi=['Chữ số nào cũng thế. Với chữ số ba thì số đứng cả hai cánh là ba mươi '
                'ba.',
                'Và kết quả cũng là mười chín.']),
        _c('cong_thuc', 'Khi hai nhóm giao nhau',
           congThuc='cộng hai nhóm  −  phần đứng ở CẢ HAI',
           thay='10 + 10 − 1 = 19',
           loi=['Cộng hai nhóm rồi bớt đi phần đứng ở cả hai.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi trước: có bạn nào đứng ở CẢ HAI nhóm không',
           loi=['Con nhớ lại một lần nữa. Trước khi cộng, hỏi xem có bạn nào đứng ở cả '
                'hai nhóm không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hai_doan_tau(b):
    """C2⑤ Trang khác chữ số."""
    return [
        _c('bia', 'Trang khác chữ số', so_bai(b),
           loi=['Dán số trang cho cuốn truyện thì tốn bao nhiêu con chữ.']),
        _c('y_toan', 'Trang 4 chỉ cần MỘT chữ số',
           'Nhưng trang 37 phải cần HAI — chữ 3 và chữ 7.', buoc=1, soBuoc=3,
           loi=['Trang bốn chỉ cần dán một chữ số.',
                'Nhưng trang ba mươi bảy phải dán hai chữ số, là chữ ba và chữ bảy.',
                'Nên không đếm chung được.']),
        _c('y_toan', 'Đoàn tàu MỘT TOA',
           'Trang 1 đến trang 9 — mỗi trang một chữ số.', buoc=2, soBuoc=3,
           loi=['Đoàn tàu một toa gồm trang một tới trang chín, mỗi trang một chữ số.',
                'Có chín trang.']),
        _c('y_toan', 'Đoàn tàu HAI TOA',
           'Từ trang 10 trở đi — mỗi trang hai chữ số.', buoc=3, soBuoc=3,
           loi=['Đoàn tàu hai toa chạy từ trang mười trở đi, mỗi trang hai chữ số.']),
        _c('y_toan', 'Đếm số trang của đoàn hai toa',
           'Cuốn 25 trang: 25 − 10 = 15, thêm 1 được 16 trang',
           loi=['Với cuốn hai mươi lăm trang thì đoàn hai toa chạy từ trang mười tới '
                'trang hai mươi lăm.',
                'Đếm bằng mẹo bài trước: hai mươi lăm trừ mười bằng mười lăm, thêm một '
                'được mười sáu trang.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Đếm TRANG khác đếm CHỮ SỐ.',
           loi=['Con nhớ chỗ này. Đếm trang khác đếm chữ số.',
                'Đếm trang xong rồi mới tính ra chữ số.']),
        _c('cong_thuc', 'Chia thành hai đoàn tàu',
           congThuc='đoàn MỘT TOA: trang 1 tới 9',
           thay='đoàn HAI TOA: từ trang 10 trở đi',
           loi=['Chia trang thành đoàn một toa và đoàn hai toa.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='trang đầu tiên cần hai chữ số là trang 10',
           loi=['Con nhớ lại một lần nữa. Trang đầu tiên cần hai chữ số là trang mười.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_cong_hai_doan(b):
    """C2⑥ Đếm chữ số cả cuốn — bài cuối chương."""
    return [
        _c('bia', 'Đếm chữ số cả cuốn', so_bai(b),
           loi=['Cuốn truyện hai mươi lăm trang cần bao nhiêu con chữ.']),
        _c('y_toan', 'Đoàn tàu một toa', '9 trang × 1 chữ số = 9 chữ số',
           buoc=1, soBuoc=3,
           loi=['Đoàn tàu một toa có chín trang, mỗi trang một chữ số. Cần chín chữ '
                'số.']),
        _c('y_toan', 'Đoàn tàu hai toa', '16 trang, mỗi trang 2 chữ số',
           buoc=2, soBuoc=3,
           loi=['Đoàn tàu hai toa có mười sáu trang, mỗi trang hai chữ số.']),
        _c('y_toan', 'Tính đoàn hai toa', '16 + 16 = 32 chữ số',
           loi=['Mười sáu cộng mười sáu bằng ba mươi hai chữ số.']),
        _c('y_toan', 'Cộng hai đoàn lại', '9 + 32 = 41', buoc=3, soBuoc=3,
           loi=['Cộng hai đoàn lại. Chín cộng ba mươi hai bằng bốn mươi mốt.',
                'Đáp số là bốn mươi mốt chữ số.']),
        _c('y_toan', 'Thử với cuốn khác',
           'Cuốn 12 trang: 9 + 6 = 15 chữ số',
           loi=['Thử với cuốn mười hai trang. Đoàn một toa chín chữ số.',
                'Đoàn hai toa có ba trang nên sáu chữ số. Cộng lại được mười lăm.']),
        _c('cong_thuc', 'Đếm chữ số cả cuốn',
           congThuc='chữ số cả cuốn  =  đoàn MỘT TOA  +  đoàn HAI TOA',
           thay='9 + 32 = 41 chữ số',
           loi=['Chữ số cả cuốn bằng đoàn một toa cộng đoàn hai toa.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='đừng quên bước CỘNG cuối cùng',
           loi=['Con nhớ lại một lần nữa. Tính riêng hai đoàn xong đừng quên bước cộng '
                'cuối cùng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 3 · DÃY SỐ KỲ DIỆU — chín kịch bản.
#
# Ba bài của sách ôm chín nghề khác nhau. Chín video, mỗi video đúng một nghề, và
# cả chín bám vào bốn dãy neo để bé không phải làm quen dãy mới ở mỗi bài:
#     4, 8, 12, 16   ·   5, ?, 15, 20   ·   1, 2, 4, 8   ·   1, 2, 4, 7
# ═══════════════════════════════════════════════════════════════════════════
DAY_DEU = [4, 8, 12, 16]
DAY_MO = [5, '?', 15, 20]
DAY_DOI = [1, 2, 4, 8]
DAY_THANG = [1, 2, 4, 7]


def kb2_bat_nhip(b):
    """C3① Tìm nhịp rồi đi tiếp."""
    return [
        _c('bia', 'Bắt nhịp của dãy', so_bai(b),
           loi=['Dãy số cách đều chạy theo một nhịp. Tìm được nhịp là đi tiếp được.']),
        _c('day_so', 'Một dãy cách đều', so=DAY_DEU,
           chuPhu='Các số cách nhau đều nhau.',
           loi=['Đây là một dãy cách đều. Bốn, tám, mười hai, mười sáu.']),
        _c('y_toan', 'Lấy số sau trừ số trước', '8 − 4 = 4', buoc=1, soBuoc=3,
           loi=['Muốn biết nhịp, lấy số sau trừ số trước.',
                'Tám trừ bốn bằng bốn. Nhịp của dãy là bốn.']),
        _c('y_toan', 'Thử thêm hai cặp nữa', '12 − 8 = 4   ·   16 − 12 = 4',
           buoc=2, soBuoc=3,
           loi=['Thử thêm hai cặp nữa cho chắc.',
                'Mười hai trừ tám bằng bốn. Mười sáu trừ mười hai cũng bằng bốn.',
                'Nhịp đều tăm tắp là bốn.']),
        _c('y_toan', 'Cộng nhịp để đi tiếp', '16 + 4 = 20   ·   20 + 4 = 24',
           buoc=3, soBuoc=3,
           loi=['Giờ cộng nhịp vào số cuối là đi tiếp được.',
                'Mười sáu cộng bốn bằng hai mươi. Hai mươi cộng bốn bằng hai mươi bốn.']),
        _c('y_toan', 'Đáp số', '20 và 24',
           loi=['Hai số tiếp theo là hai mươi và hai mươi bốn.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Chỉ cần số sau to hơn số trước là chưa đủ.',
           loi=['Có bạn thấy dãy hai, bốn, sáu rồi điền tiếp số bảy.',
                'Số bảy đúng là to hơn sáu, nhưng nhịp của dãy là hai nên phải điền '
                'số tám.']),
        _c('cong_thuc', 'Hai động tác của cả bài',
           congThuc='TRỪ để tìm nhịp  ·  CỘNG nhịp để đi tiếp',
           thay='dãy cách đều thì MỌI khoảng đều bằng nhau',
           loi=['Trừ để tìm nhịp, rồi cộng nhịp để đi tiếp.',
                'Dãy cách đều thì mọi khoảng đều bằng nhau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='thử NHIỀU cặp rồi hãy tin',
           loi=['Con nhớ lại một lần nữa. Thử nhiều cặp rồi hãy tin.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_so_mo(b):
    """C3② Điền số còn thiếu ở giữa dãy."""
    return [
        _c('bia', 'Số còn thiếu ở giữa', so_bai(b),
           loi=['Số bị thiếu nằm giữa dãy thì vẫn tìm ra được.']),
        _c('day_so', 'Một số bị thiếu', so=DAY_MO, chiSo=2,
           chuPhu='Ô thứ hai chưa có số.',
           loi=['Dãy này thiếu mất số thứ hai. Năm, rồi trống, rồi mười lăm, hai mươi.']),
        _c('day_so', 'Bắt nhịp ở chỗ còn rõ số', so=DAY_MO, chiSo=4,
           chuPhu='Hai số 15 và 20 đứng cạnh nhau và còn rõ.',
           loi=['Nhìn sang chỗ còn rõ số. Mười lăm và hai mươi đứng cạnh nhau.']),
        _c('y_toan', 'Lấy hiệu hai số ấy', '20 − 15 = 5', buoc=1, soBuoc=3,
           loi=['Hai mươi trừ mười lăm bằng năm. Nhịp của dãy là năm.']),
        _c('y_toan', 'Lần ngược lại chỗ thiếu', '15 − 5 = 10', buoc=2, soBuoc=3,
           loi=['Giờ lần ngược lại. Số đứng ngay trước mười lăm là mười lăm trừ năm.',
                'Mười lăm trừ năm bằng mười.']),
        _c('y_toan', 'Thử lại xuôi cả dãy',
           '5 + 5 = 10   ·   10 + 5 = 15   ·   15 + 5 = 20', buoc=3, soBuoc=3,
           loi=['Thử lại đi xuôi từ đầu.',
                'Năm cộng năm bằng mười. Mười cộng năm bằng mười lăm. Mười lăm cộng '
                'năm bằng hai mươi.',
                'Cả dãy đúng nhịp.']),
        _c('day_so', 'Điền vào là xong', so=[5, 10, 15, 20], chiSo=2,
           loi=['Số còn thiếu là mười.']),
        _c('cong_thuc', 'Hai động tác của cả bài',
           congThuc='bắt nhịp ở hai số còn rõ  ·  TRỪ nhịp để lần ngược',
           thay='chỗ thiếu nằm đâu cũng làm được',
           loi=['Bắt nhịp ở hai số còn rõ, rồi trừ nhịp để lần ngược lại.',
                'Chỗ thiếu nằm ở đâu cũng làm được.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='cần đúng HAI số liền nhau là đủ',
           loi=['Con nhớ lại một lần nữa. Cần đúng hai số liền nhau là đủ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_nhay_thu(b):
    """C3③ Kiểm tra một số có thuộc dãy không."""
    return [
        _c('bia', 'Số này có trong dãy không', so_bai(b),
           loi=['Cho một dãy đếm thêm và một số. Số ấy có nằm trong dãy không?']),
        _c('day_so', 'Dãy cộng thêm 3', so=[3, 6, 9, 12],
           chuPhu='Câu hỏi: số 20 có trong dãy này không?',
           loi=['Dãy này cộng thêm ba. Ba, sáu, chín, mười hai.',
                'Câu hỏi là số hai mươi có nằm trong dãy không.']),
        _c('y_toan', 'Nhảy thử từng bước một', '12 · 15 · 18 · 21', buoc=1, soBuoc=3,
           loi=['Cứ nhảy thử từng bước một.',
                'Mười hai, mười lăm, mười tám, rồi hai mươi mốt.']),
        _c('y_toan', 'Xem chỗ dãy vượt qua', '18 rồi tới 21, không dừng ở 20',
           buoc=2, soBuoc=3,
           loi=['Dãy đi từ mười tám thẳng tới hai mươi mốt.',
                'Nó không đặt chân xuống hai mươi.']),
        _c('y_toan', 'Vượt qua rồi thì dừng lại', 'Không cần nhảy thêm nữa',
           buoc=3, soBuoc=3,
           loi=['Đã vượt qua rồi thì biết chắc, không cần nhảy thêm nữa.']),
        _c('y_toan', 'Đáp số', 'Số 20 KHÔNG có trong dãy',
           loi=['Số hai mươi không có trong dãy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Nằm giữa hai số của dãy không có nghĩa là thuộc dãy.',
           loi=['Có bạn thấy hai mươi to hơn chín nên đoán là có.',
                'Dãy tăng mãi thật, nhưng nó chỉ đặt chân xuống đúng mấy số theo nhịp.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='nhảy thử tới khi VƯỢT QUA số cần hỏi',
           thay='dừng đúng chỗ ấy, đừng nhảy tiếp',
           loi=['Nhảy thử tới khi vượt qua số cần hỏi, rồi dừng đúng chỗ ấy.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='vượt qua là biết chắc',
           loi=['Con nhớ lại một lần nữa. Vượt qua là biết chắc.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_gap_doi(b):
    """C3④ Dãy gấp đôi."""
    return [
        _c('bia', 'Dãy gấp đôi', so_bai(b),
           loi=['Có dãy không cách đều. Hôm nay mình gặp loại thứ nhất.']),
        _c('day_so', 'Một dãy lạ', so=DAY_DOI,
           chuPhu='Số tiếp theo là số nào?',
           loi=['Đây là một dãy lạ. Một, hai, bốn, tám.']),
        _c('y_toan', 'Thử tìm nhịp trước đã', '2 − 1 = 1   ·   4 − 2 = 2   ·   8 − 4 = 4',
           buoc=1, soBuoc=3,
           loi=['Việc đầu tiên vẫn là thử tìm nhịp.',
                'Hai trừ một bằng một. Bốn trừ hai bằng hai. Tám trừ bốn bằng bốn.',
                'Các khoảng không bằng nhau, nên đây không phải dãy cách đều.']),
        _c('y_toan', 'Thử xem có phải gấp đôi không',
           '1 + 1 = 2   ·   2 + 2 = 4   ·   4 + 4 = 8', buoc=2, soBuoc=3,
           loi=['Nhìn lại từ đầu theo cách khác.',
                'Một cộng một bằng hai. Hai cộng hai bằng bốn. Bốn cộng bốn bằng tám.',
                'Mỗi số đúng bằng số trước cộng chính nó.']),
        _c('y_toan', 'Đi tiếp theo quy luật ấy', '8 + 8 = 16', buoc=3, soBuoc=3,
           loi=['Tám cộng tám bằng mười sáu.']),
        _c('y_toan', 'Đáp số', 'Số tiếp theo là 16',
           loi=['Số tiếp theo là mười sáu.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thử một cặp cuối rồi kết luận là hỏng.',
           loi=['Có bạn chỉ thử cặp cuối, thấy tám trừ bốn bằng bốn nên bảo nhịp là bốn.',
                'Cặp đầu đã lệch rồi. Phải thử từ đầu dãy.']),
        _c('cong_thuc', 'Dãy gấp đôi là gì',
           congThuc='mỗi số  =  số trước  +  chính nó',
           thay='gặp dãy lạ thì thử nhịp TRƯỚC, không đều mới đổi cách',
           loi=['Dãy gấp đôi là dãy mà mỗi số bằng số trước cộng chính nó.',
                'Gặp dãy lạ thì thử nhịp trước, không đều mới đổi cách.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='cộng CHÍNH NÓ, không phải cộng một số cố định',
           loi=['Con nhớ lại một lần nữa. Cộng chính nó, không phải cộng một số cố định.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_bac_thang(b):
    """C3⑤ Dãy bậc thang."""
    return [
        _c('bia', 'Dãy bậc thang', so_bai(b),
           loi=['Loại dãy không cách đều thứ hai. Bước nhảy mỗi lần dài thêm một.']),
        _c('day_so', 'Một dãy lạ nữa', so=[2, 3, 5, 8, 12],
           chuPhu='Số tiếp theo là số nào?',
           loi=['Đây là một dãy lạ nữa. Hai, ba, năm, tám, mười hai.']),
        _c('y_toan', 'Viết các bước nhảy ra',
           '3 − 2 = 1   ·   5 − 3 = 2   ·   8 − 5 = 3   ·   12 − 8 = 4',
           buoc=1, soBuoc=3,
           loi=['Viết các bước nhảy ra giấy.',
                'Ba trừ hai bằng một. Năm trừ ba bằng hai. Tám trừ năm bằng ba. '
                'Mười hai trừ tám bằng bốn.']),
        _c('day_so', 'Nhìn chính các bước nhảy', so=[1, 2, 3, 4],
           chuPhu='Mỗi bước dài thêm 1.',
           loi=['Giờ nhìn chính các bước nhảy. Một, hai, ba, bốn.',
                'Mỗi bước dài thêm một. Vậy bước tiếp theo dài năm.']),
        _c('y_toan', 'Đi thêm một bước nữa', '12 + 5 = 17', buoc=3, soBuoc=3,
           loi=['Mười hai cộng năm bằng mười bảy.']),
        _c('y_toan', 'Đáp số', 'Số tiếp theo là 17',
           loi=['Số tiếp theo là mười bảy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Lấy bước cuối làm nhịp cho cả dãy.',
           loi=['Có bạn thấy bước cuối dài ba nên cộng thêm ba.',
                'Bước sau phải dài hơn bước trước một đơn vị, nên nó dài bốn chứ '
                'không phải ba.']),
        _c('cong_thuc', 'Hai loại dãy khác nhau ở đâu',
           congThuc='cách đều: các BƯỚC bằng nhau',
           thay='bậc thang: chính các BƯỚC mới xếp thành dãy đều',
           loi=['Dãy cách đều thì các bước bằng nhau.',
                'Dãy bậc thang thì chính các bước mới xếp thành dãy đều.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chưa viết các bước ra thì chưa làm được bài',
           loi=['Con nhớ lại một lần nữa. Chưa viết các bước ra thì chưa làm được bài.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_dung_moi_so(b):
    """C3⑥ Quy luật phải đúng với mọi số đã cho."""
    return [
        _c('bia', 'Quy luật phải đúng với mọi số', so_bai(b),
           loi=['Hai dãy chỉ khác nhau một con số mà thành hai câu đố khác nhau.']),
        _c('day_so', 'Dãy thứ nhất', so=DAY_DOI, chiSo=4,
           chuPhu='Ba số đầu là 1, 2, 4.',
           loi=['Dãy thứ nhất. Một, hai, bốn, tám.']),
        _c('day_so', 'Dãy thứ hai', so=DAY_THANG, chiSo=4,
           chuPhu='Ba số đầu cũng là 1, 2, 4.',
           loi=['Dãy thứ hai. Một, hai, bốn, bảy.',
                'Ba số đầu của hai dãy giống hệt nhau. Chỉ số thứ tư là khác.']),
        _c('y_toan', 'Nhìn ba số đầu thì chưa quyết được gì',
           'Cả hai dãy đều mở đầu 1, 2, 4', buoc=1, soBuoc=3,
           loi=['Nhìn ba số đầu thôi thì chưa quyết được gì cả.']),
        _c('y_toan', 'Số thứ tư mới lộ quy luật',
           'dãy một: 4 + 4 = 8   ·   dãy hai: các bước 1, 2, 3', buoc=2, soBuoc=3,
           loi=['Số thứ tư mới lộ ra quy luật.',
                'Dãy thứ nhất có bốn cộng bốn bằng tám, nên là dãy gấp đôi.',
                'Dãy thứ hai có các bước một, hai, ba, nên là dãy bậc thang.']),
        _c('y_toan', 'Mỗi dãy đi tiếp theo cách của nó',
           '8 + 8 = 16   ·   7 + 4 = 11', buoc=3, soBuoc=3,
           loi=['Dãy gấp đôi đi tiếp là tám cộng tám bằng mười sáu.',
                'Dãy bậc thang có bước sau dài bốn, nên bảy cộng bốn bằng mười một.']),
        _c('y_toan', 'Đáp số', '16 và 11',
           loi=['Hai số tiếp theo là mười sáu và mười một.']),
        _c('cong_thuc', 'Luật của cả bài',
           congThuc='quy luật phải đúng với TẤT CẢ các số đã cho',
           thay='không phải chỉ đúng với hai số cuối',
           loi=['Một quy luật chỉ được nhận khi nó đúng với tất cả các số đã cho.',
                'Không phải chỉ đúng với hai số cuối.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='kiểm lại từ SỐ ĐẦU TIÊN',
           loi=['Con nhớ lại một lần nữa. Kiểm lại từ số đầu tiên.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_nhin_duoi(b):
    """C3⑦ Chẵn lẻ nhìn ở chữ số tận cùng."""
    return [
        _c('bia', 'Chẵn hay lẻ nhìn ở đuôi', so_bai(b),
           loi=['Một số chẵn hay lẻ, nhìn chữ số cuối cùng là biết.']),
        _c('nhom_deu', 'Số chẵn chia đôi được đều', tong=8, moiNhom=4,
           chuPhu='8 viên chia đôi: mỗi bên 4 viên, không thừa.',
           loi=['Số chẵn là số chia đôi được đều tăm tắp.',
                'Tám viên chia đôi thì mỗi bên bốn viên, không thừa viên nào.']),
        _c('nhom_deu', 'Số lẻ luôn thừa một', tong=7, moiNhom=3,
           chuPhu='7 viên chia đôi: mỗi bên 3 viên, thừa 1 viên.',
           loi=['Số lẻ chia đôi thì luôn thừa đúng một viên.']),
        _c('y_toan', 'Bí mật nằm ở chữ số tận cùng',
           'tận cùng 0, 2, 4, 6, 8  →  chẵn', buoc=1, soBuoc=3,
           loi=['Bí mật nằm ở chữ số cuối cùng bên phải.',
                'Tận cùng là không, hai, bốn, sáu hoặc tám thì số ấy chẵn.']),
        _c('y_toan', 'Còn nhóm kia là số lẻ',
           'tận cùng 1, 3, 5, 7, 9  →  lẻ', buoc=2, soBuoc=3,
           loi=['Tận cùng là một, ba, năm, bảy hoặc chín thì số ấy lẻ.']),
        _c('y_toan', 'Thử với hai số lớn', '134 tận cùng 4   ·   275 tận cùng 5',
           buoc=3, soBuoc=3,
           loi=['Thử với hai số lớn.',
                'Một trăm ba mươi tư có đuôi là bốn, nên chẵn.',
                'Hai trăm bảy mươi lăm có đuôi là năm, nên lẻ.']),
        _c('y_toan', 'Đáp số', '134 chẵn  ·  275 lẻ',
           loi=['Số một trăm ba mươi tư là số chẵn. Số hai trăm bảy mươi lăm là số lẻ.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='chỉ nhìn CHỮ SỐ TẬN CÙNG',
           thay='số to cỡ nào cũng vậy, không cần chia thử',
           loi=['Chỉ nhìn chữ số tận cùng. Số to cỡ nào cũng vậy, không cần chia thử.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='cộng các chữ số lại là một nghề KHÁC',
           loi=['Con nhớ lại một lần nữa. Cộng các chữ số lại là một nghề khác.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_duoi_bang_nhan(b):
    """C3⑧ Bí mật cái đuôi của bảng nhân 2 và bảng nhân 5."""
    return [
        _c('bia', 'Bảng nhân giấu gì', so_bai(b),
           loi=['Hai bảng nhân quen thuộc đang giấu hai bí mật rất đẹp về cái đuôi.']),
        _c('day_so', 'Bảng nhân 2', so=[2, 4, 6, 8, 10],
           chuPhu='Đuôi chỉ có 2, 4, 6, 8 và 0.',
           loi=['Bảng nhân hai. Hai, bốn, sáu, tám, mười.',
                'Cái đuôi chỉ có hai, bốn, sáu, tám và không.']),
        _c('y_toan', 'Cả bảng toàn số chẵn', 'không có số lẻ nào', buoc=1, soBuoc=3,
           loi=['Nhìn kỹ mà xem, cả bảng toàn số chẵn. Không có số lẻ nào.']),
        _c('nhom_deu', 'Vì sao lại thế', tong=6, moiNhom=3,
           chuPhu='Mỗi số của bảng nhân 2 là hai phần bằng nhau ghép lại.',
           loi=['Vì mỗi số của bảng là hai phần bằng nhau ghép lại.',
                'Nên chia đôi lúc nào cũng đều.']),
        _c('day_so', 'Bảng nhân 5', so=[5, 10, 15, 20, 25],
           chuPhu='Đuôi chỉ có 5 và 0, thay nhau.',
           loi=['Bảng nhân năm. Năm, mười, mười lăm, hai mươi, hai mươi lăm.',
                'Cái đuôi chỉ có năm và không, thay nhau lần lượt.']),
        _c('y_toan', 'Dùng bí mật ấy để loại nhanh',
           '37 có đuôi 7  →  không thuộc bảng nhân 5', buoc=3, soBuoc=3,
           loi=['Dùng bí mật ấy để loại nhanh.',
                'Ba mươi bảy có đuôi là bảy, mà bảng nhân năm chỉ có đuôi năm hoặc '
                'không. Vậy nó không thuộc bảng.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Nằm giữa 35 và 40 không có nghĩa là thuộc bảng.',
           loi=['Có bạn bảo ba mươi bảy thuộc bảng nhân năm vì nó nằm giữa ba mươi '
                'lăm và bốn mươi.',
                'Nằm giữa hai số của bảng không có nghĩa là thuộc bảng.']),
        _c('cong_thuc', 'Hai bí mật của bài',
           congThuc='bảng nhân 2:  toàn số CHẴN',
           thay='bảng nhân 5:  đuôi chỉ 0 hoặc 5',
           loi=['Bảng nhân hai toàn số chẵn. Bảng nhân năm chỉ có đuôi không hoặc năm.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='nhìn đuôi là LOẠI được ngay',
           loi=['Con nhớ lại một lần nữa. Nhìn đuôi là loại được ngay.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_cong_chan_le(b):
    """C3⑨ Đoán tổng chẵn hay lẻ mà chưa cần tính."""
    return [
        _c('bia', 'Chưa tính đã biết tổng', so_bai(b),
           loi=['Nhìn hai số hạng là đoán được tổng chẵn hay lẻ, chưa cần tính.']),
        _c('y_toan', 'Đề bài', 'Tổng 26 + 13 là số chẵn hay số lẻ?',
           loi=['Tổng hai mươi sáu cộng mười ba là số chẵn hay số lẻ?']),
        _c('y_toan', 'Soi tính nết từng số', '26 đuôi 6 → chẵn   ·   13 đuôi 3 → lẻ',
           buoc=1, soBuoc=3,
           loi=['Hai mươi sáu có đuôi là sáu nên chẵn.',
                'Mười ba có đuôi là ba nên lẻ.']),
        _c('nhom_deu', 'Lẻ cộng lẻ lại ra CHẴN', tong=8, moiNhom=4,
           chuPhu='Tổng 8 viên chia đôi vừa khít: mỗi bên 4 viên.',
           loi=['Chỗ lạ nhất là lẻ cộng lẻ lại ra chẵn.',
                'Ba viên thừa một, năm viên cũng thừa một. Hai viên lẻ loi ấy gặp '
                'nhau thì bắt cặp, nên tổng chia đôi được đều.']),
        _c('cong_thuc', 'Ba luật cộng', congThuc='chẵn + chẵn = chẵn',
           thay='lẻ + lẻ = chẵn   ·   chẵn + lẻ = lẻ',
           loi=['Chẵn cộng chẵn ra chẵn. Lẻ cộng lẻ ra chẵn. Chẵn cộng lẻ ra lẻ.']),
        _c('y_toan', 'Áp luật vào bài', 'chẵn + lẻ  →  tổng LẺ', buoc=3, soBuoc=3,
           loi=['Bài này là chẵn cộng lẻ, nên tổng là số lẻ.']),
        _c('y_toan', 'Thử lại cho chắc', '26 + 13 = 39, đuôi 9 → lẻ',
           loi=['Thử lại cho chắc. Hai mươi sáu cộng mười ba bằng ba mươi chín.',
                'Đuôi là chín, đúng là số lẻ.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='soi ĐUÔI từng số hạng rồi áp luật',
           thay='không phải tính ra kết quả',
           loi=['Soi đuôi từng số hạng rồi áp luật. Không phải tính ra kết quả.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hai cái lẻ gặp nhau thì BẮT CẶP',
           loi=['Con nhớ lại một lần nữa. Hai cái lẻ gặp nhau thì bắt cặp.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 4 · SIÊU NHÂN TÍNH NHANH — mười kịch bản.
#
# ⚠ KHÔNG gọi ô trống là "X". Sách đặt tên bài là "ĐI TÌM SỐ BÍ MẬT X", mà máy đọc
# chữ ấy thành tiếng Anh — lớp 4 đã dính đúng mười lăm chỗ. Cả bốn bài tìm ô trống
# ở đây gọi thẳng là "ô trống", trên màn hình cũng vẽ ô trống chứ không viết chữ.
# ═══════════════════════════════════════════════════════════════════════════


def kb2_ghep_doi(b):
    """C4① Ghép đôi tròn chục ở phép cộng."""
    return [
        _c('bia', 'Ghép đôi tròn chục', so_bai(b),
           loi=['Cộng một dãy dài mà không phải đặt tính dọc lần nào.']),
        _c('y_toan', 'Đề bài', '37 + 25 + 13 + 5',
           loi=['Tính tổng ba mươi bảy, hai mươi lăm, mười ba, năm.']),
        _c('y_toan', 'Dòm đuôi tìm đôi bạn', '7 + 3 = 10   ·   5 + 5 = 10',
           buoc=1, soBuoc=3,
           loi=['Đừng vội cộng. Nhìn cái đuôi của từng số trước.',
                'Đuôi bảy đi với đuôi ba, vì bảy cộng ba bằng mười.',
                'Đuôi năm đi với đuôi năm, vì năm cộng năm cũng bằng mười.']),
        _c('y_toan', 'Kéo đôi bạn về cạnh nhau', '37 + 13 = 50   ·   25 + 5 = 30',
           buoc=2, soBuoc=3,
           loi=['Phép cộng đổi chỗ thoải mái mà tổng vẫn vậy, nên kéo đôi bạn về '
                'đứng cạnh nhau.',
                'Ba mươi bảy cộng mười ba bằng năm mươi. Hai mươi lăm cộng năm bằng '
                'ba mươi.']),
        _c('y_toan', 'Cộng hai số tròn chục', '50 + 30 = 80', buoc=3, soBuoc=3,
           loi=['Còn lại phép dễ nhất. Năm mươi cộng ba mươi bằng tám mươi.']),
        _c('y_toan', 'Đáp số', '80',
           loi=['Tổng cả dãy là tám mươi.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Không bắt buộc phải cộng từ trái sang phải.',
           loi=['Có bạn bảo phải cộng từ trái sang phải nên không được đổi chỗ.',
                'Con thử tính ba cộng năm rồi năm cộng ba mà xem. Đổi chỗ thì tổng '
                'vẫn giữ nguyên.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='dòm ĐUÔI tìm đôi bạn tròn chục',
           thay='rồi kéo đôi bạn về đứng cạnh nhau',
           loi=['Dòm đuôi tìm đôi bạn tròn chục, rồi kéo đôi bạn về đứng cạnh nhau.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hai đuôi cộng lại bằng 10 là một đôi',
           loi=['Con nhớ lại một lần nữa. Hai đuôi cộng lại bằng mười là một đôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_ghep_khay(b):
    """C4② Ghép hai khay cùng số hàng — mầm non của thừa số chung."""
    return [
        _c('bia', 'Ghép hai khay kẹo', so_bai(b),
           loi=['Mẹo ghép đôi dùng được cho cả phép nhân, không riêng phép cộng.']),
        _c('y_toan', 'Đề bài', '3 × 4 + 3 × 6',
           loi=['Tính ba nhân bốn cộng ba nhân sáu.']),
        _c('luoi_cham', 'Khay thứ nhất: 3 hàng, mỗi hàng 4 viên', hang=3, cot=4,
           chuPhu='3 × 4 = 12 viên',
           loi=['Khay thứ nhất có ba hàng, mỗi hàng bốn viên. Tất cả mười hai viên.']),
        _c('luoi_cham', 'Khay thứ hai: 3 hàng, mỗi hàng 6 viên', hang=3, cot=6,
           chuPhu='3 × 6 = 18 viên',
           loi=['Khay thứ hai cũng ba hàng, mỗi hàng sáu viên. Tất cả mười tám viên.']),
        _c('y_toan', 'Đẩy hai khay sát vào nhau', 'số hàng vẫn là 3',
           buoc=1, soBuoc=3,
           loi=['Giờ đẩy hai khay sát vào nhau. Hàng nối vào hàng.',
                'Số hàng không đổi, vẫn là ba hàng.']),
        _c('y_toan', 'Mỗi hàng dài thêm', '4 + 6 = 10 viên', buoc=2, soBuoc=3,
           loi=['Nhưng mỗi hàng nay dài ra. Bốn viên nối sáu viên thành mười viên.']),
        _c('luoi_cham', 'Thành một khay to', hang=3, cot=4, cot2=6,
           chuPhu='3 × 10 = 30 viên',
           chuCuoi='Phần vàng là khay thứ hai vừa nối vào.',
           loi=['Khay to là ba hàng mười viên. Ba nhân mười bằng ba mươi.']),
        _c('y_toan', 'Tính riêng cũng ra đúng thế', '12 + 18 = 30',
           loi=['Tính riêng từng khay rồi cộng cũng ra ba mươi. Nhưng ghép khay thì '
                'nhanh hơn nhiều.']),
        _c('cong_thuc', 'Điều kiện để ghép được',
           congThuc='hai khay phải CÙNG SỐ HÀNG',
           thay='ghép xong: số hàng giữ nguyên, mỗi hàng dài thêm',
           loi=['Hai khay phải cùng số hàng thì mới ghép được.',
                'Ghép xong thì số hàng giữ nguyên, chỉ mỗi hàng dài thêm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_cap_dau_cuoi(b):
    """C4③ Ghép cặp đầu với cuối."""
    return [
        _c('bia', 'Ghép cặp đầu với cuối', so_bai(b),
           loi=['Cộng cả một dãy dài chỉ bằng vài phép tính.']),
        _c('day_so', 'Đề bài', so=[1, 2, 3, 4, 5, 6, 7, 8],
           chuPhu='Tính tổng cả dãy.',
           loi=['Tính tổng từ một đến tám.']),
        _c('y_toan', 'Bắc cầu nối số đầu với số cuối', '1 + 8 = 9', buoc=1, soBuoc=3,
           loi=['Đừng cộng từ trái sang. Bắc cầu nối số đầu với số cuối.',
                'Một cộng tám bằng chín.']),
        _c('y_toan', 'Lùi vào trong, cặp nào cũng bằng chín',
           '2 + 7 = 9   ·   3 + 6 = 9   ·   4 + 5 = 9', buoc=2, soBuoc=3,
           loi=['Lùi vào trong một nấc. Hai cộng bảy bằng chín.',
                'Rồi ba cộng sáu bằng chín. Rồi bốn cộng năm cũng bằng chín.',
                'Cặp nào cũng bằng chín cả.']),
        _c('y_toan', 'Vì sao cặp nào cũng bằng nhau',
           'bên trái tăng 1 thì bên phải giảm 1',
           loi=['Mỗi lần lùi vào trong, số bên trái tăng một còn số bên phải giảm một.',
                'Một bên đưa, một bên nhận, nên tổng của cặp giữ nguyên.']),
        _c('y_toan', 'Đếm số cặp rồi cộng dồn', '9 + 9 + 9 + 9 = 36',
           buoc=3, soBuoc=3,
           loi=['Tám số ghép vừa khít thành bốn cặp, mỗi cặp chín.',
                'Cộng dồn bốn lần chín được ba mươi sáu.']),
        _c('y_toan', 'Đáp số', '36',
           loi=['Tổng cả dãy là ba mươi sáu.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Số 9 là tổng MỘT CẶP, chưa phải tổng cả dãy.',
           loi=['Có bạn ghép cặp xong rồi ghi luôn đáp số là chín.',
                'Chín mới là tổng một cặp thôi. Còn phải cộng dồn tất cả các cặp nữa.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='ghép ĐẦU với CUỐI, mọi cặp bằng nhau',
           thay='đếm số cặp rồi cộng dồn',
           loi=['Ghép đầu với cuối thì mọi cặp bằng nhau. Đếm số cặp rồi cộng dồn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_ban_giua(b):
    """C4④ Dãy lẻ số thì có một bạn đứng giữa."""
    return [
        _c('bia', 'Một bạn đứng giữa', so_bai(b),
           loi=['Ghép cặp xong mà vẫn còn một số lẻ loi. Bài này nói về số ấy.']),
        _c('day_so', 'Đề bài', so=[1, 2, 3, 4, 5, 6, 7, 8, 9],
           chuPhu='Tính tổng cả dãy.',
           loi=['Tính tổng từ một đến chín.']),
        _c('y_toan', 'Ghép cặp đầu cuối như bài trước',
           '1 + 9 = 10   ·   2 + 8 = 10   ·   3 + 7 = 10   ·   4 + 6 = 10',
           buoc=1, soBuoc=3,
           loi=['Ghép cặp đầu cuối như bài trước. Một cộng chín bằng mười.',
                'Rồi hai cộng tám, ba cộng bảy, bốn cộng sáu. Cặp nào cũng bằng mười.']),
        _c('day_so', 'Đếm xem đã dùng hết số chưa', so=[1, 2, 3, 4, 5, 6, 7, 8, 9],
           chiSo=5, chuPhu='Bốn cặp mới dùng tám số. Số 5 chưa ai ghép cùng.',
           loi=['Đếm lại xem đã dùng hết số chưa.',
                'Bốn cặp mới dùng hết tám số, mà dãy có chín số.',
                'Số năm đứng chính giữa, chưa ai ghép cùng.']),
        _c('y_toan', 'Cộng dồn bốn cặp trước', '10 + 10 + 10 + 10 = 40',
           buoc=2, soBuoc=3,
           loi=['Cộng dồn bốn cặp mười được bốn mươi.']),
        _c('y_toan', 'Rồi cộng thêm bạn đứng giữa', '40 + 5 = 45', buoc=3, soBuoc=3,
           loi=['Rồi cộng thêm số năm đứng giữa. Bốn mươi cộng năm bằng bốn mươi lăm.']),
        _c('y_toan', 'Đáp số', '45',
           loi=['Tổng cả dãy là bốn mươi lăm.']),
        _c('y_toan', 'Khi nào có bạn đứng giữa',
           'Dãy có SỐ LƯỢNG LẺ thì luôn còn đúng một số.',
           loi=['Dãy có số lượng lẻ thì luôn còn đúng một số đứng giữa.',
                'Dãy có số lượng chẵn thì ghép vừa khít, không ai lẻ loi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ghép xong phải ĐẾM LẠI xem hết số chưa',
           loi=['Con nhớ lại một lần nữa. Ghép xong phải đếm lại xem đã hết số chưa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_chay_nguoc(b):
    """C4⑤ Tìm ô trống của phép cộng và phép trừ."""
    return [
        _c('bia', 'Cho kết quả chạy ngược', so_bai(b),
           loi=['Tìm số đang trốn trong ô trống, bằng cách cho kết quả chạy ngược.']),
        _c('y_toan', 'Đề bài', 'ô trống  +  5  =  12',
           loi=['Ô trống cộng năm bằng mười hai. Ô trống đang giấu số nào?']),
        _c('y_toan', 'Máy chạy xuôi thế nào', 'số cần tìm  →  máy + 5  →  12',
           buoc=1, soBuoc=3,
           loi=['Số cần tìm chui vào máy cộng năm rồi chạy ra thành mười hai.']),
        _c('y_toan', 'Máy ngược của máy cộng là máy trừ', '12  →  máy − 5  →  ?',
           buoc=2, soBuoc=3,
           loi=['Máy ngược của máy cộng năm là máy trừ năm.',
                'Cho mười hai chạy ngược qua máy ấy.']),
        _c('y_toan', 'Cho kết quả chạy ngược', '12 − 5 = 7', buoc=3, soBuoc=3,
           loi=['Mười hai trừ năm bằng bảy.']),
        _c('y_toan', 'Thử lại trước khi chốt', '7 + 5 = 12',
           loi=['Chưa xong đâu. Thay bảy vào ô trống rồi tính xuôi một lần.',
                'Bảy cộng năm bằng mười hai, khớp đúng đề bài.']),
        _c('y_toan', 'Đáp số', 'Số cần tìm là 7',
           loi=['Số cần tìm là bảy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Bài ô trống − 4 = 9 thì KHÔNG lấy 9 trừ 4.',
           loi=['Có bạn gặp bài ô trống trừ bốn bằng chín, thấy dấu trừ thì cứ trừ, '
                'lấy chín trừ bốn bằng năm.',
                'Thử lại thì năm trừ bốn bằng một, không ra chín. Máy ngược của máy '
                'trừ là máy cộng, nên phải lấy chín cộng bốn bằng mười ba.']),
        _c('cong_thuc', 'Đôi máy ngược chiều thứ nhất',
           congThuc='cộng  ⇄  trừ',
           thay='tìm xong PHẢI thử lại',
           loi=['Cộng và trừ là đôi máy ngược chiều. Tìm xong phải thử lại.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_nhan_chia_nguoc(b):
    """C4⑥ Tìm ô trống của phép nhân và phép chia."""
    return [
        _c('bia', 'Máy nhân và máy chia', so_bai(b),
           loi=['Phép nhân cũng có máy ngược của nó. Đó là phép chia.']),
        _c('y_toan', 'Đề bài', 'ô trống  ×  4  =  28',
           loi=['Ô trống nhân bốn bằng hai mươi tám. Ô trống đang giấu số nào?']),
        _c('y_toan', 'Máy chạy xuôi thế nào', 'số cần tìm  →  máy × 4  →  28',
           buoc=1, soBuoc=3,
           loi=['Số cần tìm chui vào máy nhân bốn rồi chạy ra thành hai mươi tám.']),
        _c('y_toan', 'Máy ngược của máy nhân là máy chia', '28  →  máy : 4  →  ?',
           buoc=2, soBuoc=3,
           loi=['Máy ngược của máy nhân bốn là máy chia bốn.',
                'Cho hai mươi tám chạy ngược qua máy ấy.']),
        _c('y_toan', 'Cho kết quả chạy ngược', '28 : 4 = 7', buoc=3, soBuoc=3,
           loi=['Hai mươi tám chia bốn bằng bảy.']),
        _c('y_toan', 'Thử lại trước khi chốt', '7 × 4 = 28',
           loi=['Thay bảy vào ô trống rồi tính xuôi. Bảy nhân bốn bằng hai mươi tám, '
                'khớp đúng đề bài.']),
        _c('y_toan', 'Đáp số', 'Số cần tìm là 7',
           loi=['Số cần tìm là bảy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Bài ô trống : 3 = 6 thì KHÔNG lấy 6 chia 3.',
           loi=['Có bạn gặp bài ô trống chia ba bằng sáu, thấy dấu chia thì cứ chia, '
                'lấy sáu chia ba bằng hai.',
                'Máy ngược của máy chia là máy nhân, nên phải lấy sáu nhân ba bằng '
                'mười tám.']),
        _c('cong_thuc', 'Đôi máy ngược chiều thứ hai',
           congThuc='nhân  ⇄  chia',
           thay='y như cộng ⇄ trừ ở bài trước',
           loi=['Nhân và chia là đôi máy ngược chiều, y như cộng và trừ ở bài trước.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_bi_lay_di(b):
    """C4⑦ Ca ô trống đứng SAU dấu trừ."""
    return [
        _c('bia', 'Khi số cần tìm bị lấy đi', so_bai(b),
           loi=['Có một ca làm ngược hẳn hai bài trước. Bài này chỉ nói về ca ấy.']),
        _c('y_toan', 'Đề bài', '14  −  ô trống  =  6',
           loi=['Mười bốn trừ ô trống bằng sáu. Ô trống đang giấu số nào?']),
        _c('y_toan', 'Ca này khác ở đâu', 'ô trống đứng SAU dấu trừ',
           buoc=1, soBuoc=3,
           loi=['Nhìn kỹ chỗ đứng của ô trống. Nó nằm sau dấu trừ.',
                'Số cần tìm không chui vào máy nào cả. Nó chính là phần bị lấy đi.']),
        _c('y_toan', 'Hỏi lại cho dễ hiểu', 'Từ 14 lấy đi bao nhiêu thì còn 6?',
           buoc=2, soBuoc=3,
           loi=['Câu hỏi thật ra rất dễ. Từ mười bốn lấy đi bao nhiêu thì còn sáu?']),
        _c('y_toan', 'Lấy số ban đầu trừ phần còn lại', '14 − 6 = 8',
           buoc=3, soBuoc=3,
           loi=['Mười bốn trừ sáu bằng tám. Phần bị lấy đi là tám.']),
        _c('y_toan', 'Thử lại trước khi chốt', '14 − 8 = 6',
           loi=['Thay tám vào ô trống rồi tính xuôi. Mười bốn trừ tám bằng sáu, khớp '
                'đúng đề bài.']),
        _c('y_toan', 'Đáp số', 'Số cần tìm là 8',
           loi=['Số cần tìm là tám.']),
        _c('y_toan', 'Hai bài trông giống nhau mà khác hẳn',
           'ô trống − 6 = 14  →  20      ·      14 − ô trống = 6  →  8',
           loi=['Hai bài này trông giống nhau mà đáp số khác hẳn.',
                'Ô trống trừ sáu bằng mười bốn thì ra hai mươi. Còn mười bốn trừ ô '
                'trống bằng sáu thì ra tám.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='nhìn ô trống đứng TRƯỚC hay SAU dấu trừ',
           thay='đứng sau thì lấy số đầu trừ kết quả',
           loi=['Con nhớ lại một lần nữa. Nhìn ô trống đứng trước hay sau dấu trừ '
                'rồi mới chọn cách làm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_chia_vong(b):
    """C4⑧ Chia theo vòng, tìm trạm dừng trong bảng nhân."""
    return [
        _c('bia', 'Chia theo vòng', so_bai(b),
           loi=['Chia một gói đồ cho mấy bạn, mà không chia hết được.']),
        _c('y_toan', 'Đề bài', '20 viên bi chia đều cho 6 bạn',
           loi=['Có hai mươi viên bi chia đều cho sáu bạn.',
                'Mỗi bạn được mấy viên, và còn thừa mấy viên?']),
        _c('y_toan', 'Chia theo vòng cho công bằng', 'mỗi vòng tốn 6 viên',
           buoc=1, soBuoc=3,
           loi=['Chia theo vòng cho công bằng. Mỗi vòng phát cho mỗi bạn đúng một '
                'viên.',
                'Có sáu bạn nên mỗi vòng tốn sáu viên.']),
        _c('y_toan', 'Lần theo bảng nhân 6 tìm trạm dừng',
           '6 × 3 = 18 chưa vượt   ·   6 × 4 = 24 vượt mất', buoc=2, soBuoc=3,
           loi=['Lần theo bảng nhân sáu tìm trạm dừng gần nhất mà chưa vượt.',
                'Sáu nhân ba bằng mười tám, chưa vượt hai mươi.',
                'Sáu nhân bốn bằng hai mươi tư, vượt mất rồi. Vậy dừng ở ba vòng.']),
        _c('nhom_deu', 'Ba vòng: mỗi bạn 3 viên, còn thừa 2', tong=20, moiNhom=6,
           chuPhu='Hai viên đỏ là phần còn thừa.',
           loi=['Ba vòng thì mỗi bạn được ba viên.',
                'Nhìn hai viên tô đỏ đứng riêng kia, đó là phần còn thừa.']),
        _c('y_toan', 'Đếm số viên còn lại', '20 − 18 = 2', buoc=3, soBuoc=3,
           loi=['Đã phát đi mười tám viên. Hai mươi trừ mười tám bằng hai.']),
        _c('y_toan', 'Đáp số', 'mỗi bạn 3 viên, thừa 2 viên',
           loi=['Mỗi bạn được ba viên, còn thừa hai viên.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Phải nói ĐỦ HAI SỐ.',
           loi=['Có bạn ghi mỗi bạn ba viên rồi thôi, quên không nói thừa mấy viên.',
                'Bài chia còn thừa phải nói đủ hai số.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='lần theo BẢNG NHÂN tìm trạm dừng gần nhất',
           thay='rồi lấy tổng trừ đi phần đã phát',
           loi=['Lần theo bảng nhân tìm trạm dừng gần nhất mà chưa vượt, rồi lấy tổng '
                'trừ đi phần đã phát.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_luat_vang(b):
    """C4⑨ Luật vàng: số thừa phải bé hơn số bạn."""
    return [
        _c('bia', 'Luật vàng của phép chia', so_bai(b),
           loi=['Có một luật giúp con biết ngay mình chia đúng hay chia sai.']),
        _c('y_toan', 'Đề bài',
           'Có bạn chia 17 viên cho 3 bạn rồi bảo: mỗi bạn 4 viên, thừa 5 viên.',
           loi=['Có bạn chia mười bảy viên kẹo cho ba bạn.',
                'Bạn ấy bảo mỗi bạn bốn viên, còn thừa năm viên. Chỗ ấy vô lý ở đâu?']),
        _c('y_toan', 'Soi luật vàng trước đã', 'thừa 5   ·   số bạn 3   ·   5 > 3',
           buoc=1, soBuoc=3,
           loi=['Soi luật vàng trước đã. Số thừa là năm, mà chỉ có ba bạn.',
                'Số thừa đang lớn hơn số bạn.']),
        _c('y_toan', 'Vì sao thế là vô lý', 'còn 5 viên thì phát thêm được một vòng',
           buoc=2, soBuoc=3,
           loi=['Còn năm viên trong tay thì phát thêm được cả một vòng nữa.',
                'Một vòng chỉ tốn ba viên thôi mà.']),
        _c('nhom_deu', 'Chia lại cho đúng', tong=17, moiNhom=3,
           chuPhu='Mỗi bạn 5 viên, hai viên đỏ là phần thừa.',
           loi=['Chia lại cho đúng. Phát thêm một vòng thì mỗi bạn thành năm viên.',
                'Chỉ còn hai viên tô đỏ đứng riêng.']),
        _c('y_toan', 'Đếm phần còn lại', '17 − 15 = 2', buoc=3, soBuoc=3,
           loi=['Đã phát mười lăm viên. Mười bảy trừ mười lăm bằng hai.']),
        _c('y_toan', 'Đáp số', 'mỗi bạn 5 viên, thừa 2 viên',
           loi=['Mỗi bạn được năm viên, còn thừa hai viên.',
                'Lần này số thừa là hai, đã bé hơn ba bạn nên chia xong thật.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thừa BẰNG số bạn thì vẫn còn chia thêm được.',
           loi=['Có bạn chia cho sáu bạn rồi bảo thừa đúng sáu viên, và tưởng thế là '
                'hợp luật.',
                'Còn sáu viên mà có sáu bạn thì vẫn phát thêm được một vòng nữa. Luật '
                'đòi thừa phải bé hơn hẳn.']),
        _c('cong_thuc', 'Luật vàng',
           congThuc='số THỪA phải BÉ HƠN số bạn',
           thay='không thì còn phát thêm được một vòng nữa',
           loi=['Số thừa phải bé hơn số bạn. Không thì còn phát thêm được một vòng '
                'nữa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_chia_het(b):
    """C4⑩ Chia hết hay còn thừa — bảng nhân là danh sách chia đẹp."""
    return [
        _c('bia', 'Chia hết hay còn thừa', so_bai(b),
           loi=['Nhìn bảng nhân là biết trước một số chia có hết hay không.']),
        _c('y_toan', 'Đề bài',
           'Chia 15 viên cho 3 bạn có vừa khít không? Còn 17 viên thì sao?',
           loi=['Chia mười lăm viên kẹo cho ba bạn có vừa khít không?',
                'Còn mười bảy viên thì sao?']),
        _c('day_so', 'Soi bảng nhân 3', so=[3, 6, 9, 12, 15, 18], chiSo=5,
           chuPhu='Số 15 có mặt trong bảng.',
           loi=['Soi bảng nhân ba. Ba, sáu, chín, mười hai, mười lăm, mười tám.',
                'Số mười lăm có mặt trong bảng.']),
        _c('nhom_deu', 'Số nằm trong bảng thì chia vừa khít', tong=15, moiNhom=3,
           chuPhu='Năm vòng, không viên nào đứng riêng.',
           loi=['Chia mười lăm viên cho ba bạn được đúng năm vòng.',
                'Không viên nào đứng riêng. Đó là chia hết.']),
        _c('y_toan', 'Còn số không có trong bảng', '17 không có trong bảng nhân 3',
           buoc=1, soBuoc=3,
           loi=['Số mười bảy thì không có trong bảng nhân ba.',
                'Bảng nhảy thẳng từ mười lăm sang mười tám, bỏ qua nó.']),
        _c('y_toan', 'Tìm trạm dừng gần nhất mà chưa vượt', '17 − 15 = 2',
           buoc=2, soBuoc=3,
           loi=['Trạm dừng gần nhất mà chưa vượt là mười lăm.',
                'Mười bảy trừ mười lăm bằng hai. Còn thừa hai viên.']),
        _c('nhom_deu', 'Chia 17 viên thì còn thừa 2', tong=17, moiNhom=3,
           chuPhu='Hai viên đỏ không đủ phát thêm một vòng.',
           loi=['Hai viên tô đỏ không đủ phát thêm một vòng cho ba bạn.']),
        _c('y_toan', 'Chỗ hay nhầm',
           'Nằm GIỮA hai số của bảng không có nghĩa là thuộc bảng.',
           loi=['Có bạn thấy mười bảy nằm giữa mười lăm và mười tám nên bảo nó cũng '
                'chia hết cho ba.',
                'Nằm giữa hai số của bảng không có nghĩa là thuộc bảng.']),
        _c('cong_thuc', 'Bảng nhân dùng để làm gì',
           congThuc='bảng nhân = danh sách các số chia VỪA KHÍT',
           thay='thuộc bảng thì biết trước, khỏi chia thử',
           loi=['Bảng nhân chính là danh sách những số chia vừa khít.',
                'Thuộc bảng thì biết trước, khỏi phải chia thử.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 5 · CHUYỆN TOÁN LỜI VĂN — mười hai kịch bản.
#
# Chương dài nhất của quyển. Bốn bài dùng cảnh `so_do_doan` — sơ đồ đoạn thẳng vốn
# dựng cho chương tổng-hiệu của lớp 4, nay dùng lại cho hai dạng của lớp 2:
#   · hơn kém   → hai đoạn lệch nhau, khúc dôi ra là phần hơn;
#   · chia phần → hai đoạn chia vạch, mỗi vạch là một phần bằng nhau.
#
# ⚠ Viết "ki lô mét" chứ đừng viết "km": máy đọc hai chữ cái ấy thành tiếng Anh.
# ═══════════════════════════════════════════════════════════════════════════


def kb2_chia_deu(b):
    """C5① Chia đều và khuôn ba dòng."""
    return [
        _c('bia', 'Chia đều', so_bai(b),
           loi=['Bài toán lời văn đầu tiên, và cách trình bày bài giải cho đúng.']),
        _c('de_toan', 'Đề bài',
           de='Cô giáo có 15 quyển vở thưởng đều cho 5 bạn. Hỏi mỗi bạn được mấy quyển?',
           loi=['Cô giáo có mười lăm quyển vở thưởng đều cho năm bạn.',
                'Hỏi mỗi bạn được mấy quyển vở.']),
        _c('y_toan', 'Đề cho gì, hỏi gì', 'cho: 15 quyển · 5 bạn · chia đều',
           buoc=1, soBuoc=3,
           loi=['Đọc chậm xem đề cho gì. Cho mười lăm quyển vở, năm bạn, và chia đều.',
                'Đề hỏi mỗi bạn được mấy quyển.']),
        _c('nhom_deu', 'Chia đều thành 5 phần bằng nhau', tong=15, moiNhom=3,
           chuPhu='Mỗi bạn được 3 quyển, không thừa quyển nào.',
           loi=['Chia đều mười lăm quyển thành năm phần bằng nhau.',
                'Mỗi phần được ba quyển, không thừa quyển nào.']),
        _c('y_toan', 'Chia đều là việc của phép chia', '15 : 5 = 3',
           buoc=2, soBuoc=3,
           loi=['Chia đều thành các phần bằng nhau là việc của phép chia.',
                'Mười lăm chia năm bằng ba.']),
        _c('cong_thuc', 'Trình bày đủ ba dòng',
           congThuc='① lời giải   ② phép tính kèm đơn vị   ③ đáp số',
           thay='mọi bài toán lời văn của cả chương đều trình bày như thế',
           loi=['Trình bày đủ ba dòng. Dòng một là lời giải, dòng hai là phép tính '
                'kèm đơn vị, dòng ba là đáp số.']),
        _c('y_toan', 'Đáp số', '3 quyển vở', buoc=3, soBuoc=3,
           loi=['Đáp số là ba quyển vở.']),
        _c('y_toan', 'Thử lại cho chắc', '3 × 5 = 15',
           loi=['Thử lại bằng phép nhân. Ba nhân năm bằng mười lăm, khớp đúng số vở '
                'của cô.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia đều → phép CHIA',
           loi=['Con nhớ lại một lần nữa. Chia đều thì dùng phép chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_bai_nguoc_chia(b):
    """C5② Biết mỗi phần, tìm tất cả."""
    return [
        _c('bia', 'Bài ngược', so_bai(b),
           loi=['Bài trước biết tất cả rồi hỏi mỗi phần. Bài này ngược lại.']),
        _c('de_toan', 'Đề bài',
           de='Mỗi bạn được 4 cái bánh, có 3 bạn. Hỏi khay có tất cả bao nhiêu cái bánh?',
           loi=['Mỗi bạn được bốn cái bánh, có ba bạn.',
                'Hỏi khay có tất cả bao nhiêu cái bánh.']),
        _c('y_toan', 'Đề cho biết cái gì', 'biết MỖI phần, hỏi TẤT CẢ',
           buoc=1, soBuoc=3,
           loi=['Lần này đề cho biết mỗi phần rồi hỏi tất cả.',
                'Đúng ngược với bài trước.']),
        _c('luoi_cham', 'Ba phần bằng nhau, mỗi phần 4 cái', hang=3, cot=4,
           chuPhu='3 × 4 = 12 cái bánh',
           loi=['Vẽ ba phần bằng nhau, mỗi phần bốn cái.']),
        _c('y_toan', 'Gộp các phần bằng nhau là việc của phép nhân', '4 × 3 = 12',
           buoc=2, soBuoc=3,
           loi=['Gộp các phần bằng nhau lại là việc của phép nhân.',
                'Bốn nhân ba bằng mười hai.']),
        _c('y_toan', 'Thử lại bằng phép chia', '12 : 3 = 4', buoc=3, soBuoc=3,
           loi=['Thử lại bằng phép chia. Mười hai chia ba bằng bốn, đúng bằng phần của '
                'mỗi bạn.']),
        _c('y_toan', 'Đáp số', '12 cái bánh',
           loi=['Đáp số là mười hai cái bánh.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Không cộng 4 cái với 3 bạn.',
           loi=['Có bạn cộng luôn bốn với ba được bảy.',
                'Bốn là số bánh của một bạn, còn ba là số bạn. Hai thứ khác loại nhau '
                'thì không cộng thẳng được.']),
        _c('cong_thuc', 'Hai bài đi cặp với nhau',
           congThuc='biết TẤT CẢ, hỏi MỖI phần  →  chia',
           thay='biết MỖI phần, hỏi TẤT CẢ  →  nhân',
           loi=['Biết tất cả rồi hỏi mỗi phần thì chia. Biết mỗi phần rồi hỏi tất cả '
                'thì nhân.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_so_do_doan(b):
    """C5③ Sơ đồ hai đoạn thẳng cho bài hơn kém."""
    return [
        _c('bia', 'Sơ đồ hai đoạn thẳng', so_bai(b),
           loi=['Bài hơn kém thì vẽ sơ đồ trước, phép tính tự hiện ra sau.']),
        _c('de_toan', 'Đề bài',
           de='Hoa gấp được 14 con hạc. Lan gấp được ít hơn Hoa 5 con. Hỏi Lan gấp được mấy con?',
           loi=['Hoa gấp được mười bốn con hạc giấy.',
                'Lan gấp được ít hơn Hoa năm con. Hỏi Lan gấp được mấy con.']),
        _c('so_do_doan', 'Vẽ mỗi bạn một đoạn thẳng', be=9, lon=14,
           nhanBe='Lan', nhanLon='Hoa',
           chuPhu='Đoạn của Hoa dài 14. Đoạn của Lan ngắn hơn.',
           loi=['Vẽ mỗi bạn một đoạn thẳng. Đoạn của Hoa dài mười bốn.',
                'Lan ít hơn nên đoạn của Lan ngắn hơn.']),
        _c('so_do_doan', 'Khúc hụt vào chính là phần ít hơn', be=9, lon=14,
           nhanBe='Lan', nhanLon='Hoa', hienHieu=True, chuHieu='ít hơn 5 con',
           chuPhu='Đoạn của Lan hụt vào đúng 5 con.',
           loi=['Khúc hụt vào chính là phần ít hơn, ở đây bằng năm con.']),
        _c('y_toan', 'Nhìn sơ đồ chọn phép tính', 'Lan = Hoa bớt đi khúc hụt',
           buoc=1, soBuoc=3,
           loi=['Nhìn sơ đồ mà chọn phép tính.',
                'Đoạn của Lan bằng đoạn của Hoa bớt đi khúc hụt, nên đây là phép trừ.']),
        _c('y_toan', 'Tính ra kết quả', '14 − 5 = 9', buoc=2, soBuoc=3,
           loi=['Mười bốn trừ năm bằng chín.']),
        _c('y_toan', 'Thử lại cho chắc', '14 − 9 = 5', buoc=3, soBuoc=3,
           loi=['Thử lại. Hoa hơn Lan mười bốn trừ chín bằng năm con, khớp đúng đề '
                'bài.']),
        _c('y_toan', 'Đáp số', '9 con hạc',
           loi=['Đáp số là chín con hạc.']),
        _c('cong_thuc', 'Ba câu hỏi trước mọi bài hơn kém',
           congThuc='AI DÀI?  AI NGẮN?  THÒ RA BAO NHIÊU?',
           thay='vẽ xong ba câu ấy thì phép tính tự hiện ra',
           loi=['Trước mọi bài hơn kém, hỏi ba câu. Ai dài? Ai ngắn? Thò ra bao '
                'nhiêu?']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_cau_chu_dao(b):
    """C5④ Bẫy câu chữ đảo."""
    return [
        _c('bia', 'Bẫy câu chữ đảo', so_bai(b),
           loi=['Có kiểu đề mà chữ ít hơn lại đứng cạnh người nhiều hơn.']),
        _c('de_toan', 'Đề bài',
           de='An ít hơn Bình 3 viên bi. An có 8 viên. Hỏi Bình có bao nhiêu viên?',
           loi=['An ít hơn Bình ba viên bi. An có tám viên.',
                'Hỏi Bình có bao nhiêu viên.']),
        _c('y_toan', 'Đọc lướt thì dễ mắc bẫy', 'thấy chữ "ít hơn" là trừ ngay',
           buoc=1, soBuoc=3,
           loi=['Đọc lướt thì thấy ngay chữ ít hơn, và nhiều bạn trừ luôn.',
                'Tám trừ ba bằng năm. Nhưng thế là sai.']),
        _c('y_toan', 'Hỏi lại: AI nhiều hơn', 'An ít hơn Bình → BÌNH nhiều hơn',
           buoc=2, soBuoc=3,
           loi=['Hỏi lại cho rõ. An ít hơn Bình, tức là Bình mới là người nhiều bi '
                'hơn.']),
        _c('so_do_doan', 'Vẽ ra thì thấy ngay', be=8, lon=11,
           nhanBe='An', nhanLon='Bình', hienHieu=True, chuHieu='thò ra 3 viên',
           chuPhu='Đoạn của Bình dài hơn, thò ra 3 viên.',
           loi=['Vẽ ra thì thấy ngay. Đoạn của Bình dài hơn đoạn của An, thò ra ba '
                'viên.']),
        _c('y_toan', 'Nhìn sơ đồ chọn phép tính', '8 + 3 = 11', buoc=3, soBuoc=3,
           loi=['Đoạn của Bình bằng đoạn của An thò thêm ba, nên đây là phép cộng.',
                'Tám cộng ba bằng mười một.']),
        _c('y_toan', 'Thử lại cho chắc', '11 − 8 = 3',
           loi=['Thử lại. An ít hơn Bình mười một trừ tám bằng ba viên, khớp đúng đề '
                'bài.']),
        _c('y_toan', 'Đáp số', 'Bình có 11 viên bi',
           loi=['Đáp số là Bình có mười một viên bi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chữ đứng cạnh AI không quyết định AI nhiều hơn',
           thay='hỏi "ai nhiều hơn" rồi mới vẽ, rồi mới tính',
           loi=['Con nhớ lại một lần nữa. Chữ đứng cạnh ai không quyết định ai nhiều '
                'hơn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_liet_ke(b):
    """C5⑤ Liệt kê có thứ tự mọi cách tách tổng."""
    return [
        _c('bia', 'Liệt kê có thứ tự', so_bai(b),
           loi=['Có bao nhiêu cách chia một gói kẹo cho hai bạn?']),
        _c('de_toan', 'Đề bài',
           de='Hai bạn có tất cả 12 viên kẹo, mỗi bạn ít nhất một viên. Liệt kê mọi cách chia.',
           loi=['Hai bạn có tất cả mười hai viên kẹo, mỗi bạn ít nhất một viên.',
                'Hãy liệt kê mọi cách chia.']),
        _c('y_toan', 'Đừng nghĩ tới đâu ghi tới đó', 'nghĩ bừa thì vừa sót vừa trùng',
           buoc=1, soBuoc=3,
           loi=['Nghĩ tới đâu ghi tới đó thì vừa dễ sót cách, vừa dễ kể trùng.']),
        _c('y_toan', 'Cho phần thứ nhất giảm dần', '11 · 10 · 9 · 8 · 7 · 6',
           buoc=2, soBuoc=3,
           loi=['Làm có thứ tự. Cho phần thứ nhất giảm dần từ lớn xuống bé.',
                'Mười một, mười, chín, tám, bảy, sáu.']),
        _c('bang_hang', 'Phần thứ hai tự hiện ra', so='12', hienLop=False,
           chuChinh='Kẻ bảng hai cột rồi điền',
           chuPhu='11 và 1 · 10 và 2 · 9 và 3 · 8 và 4 · 7 và 5 · 6 và 6',
           loi=['Phần thứ hai tự hiện ra, vì hai phần phải cộng lại bằng mười hai.',
                'Mười một và một. Mười và hai. Chín và ba. Tám và bốn. Bảy và năm. '
                'Sáu và sáu.']),
        _c('y_toan', 'Đếm xem có mấy cách', 'đúng 6 cách', buoc=3, soBuoc=3,
           loi=['Đếm lại được đúng sáu cách.']),
        _c('y_toan', 'Đáp số', 'có 6 cách tách',
           loi=['Đáp số là có sáu cách.']),
        _c('y_toan', 'Một bí mật nhỏ trong bảng',
           'cột hơn nhau chạy 10, 8, 6, 4, 2, 0 — mỗi lần giảm 2',
           loi=['Nhìn cột hơn nhau mà xem. Nó chạy mười, tám, sáu, bốn, hai, không.',
                'Mỗi lần chuyển một viên thì phần hơn giảm hai, vì một bên bớt một '
                'viên còn bên kia thêm một viên.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='cho MỘT phần giảm dần, phần kia tự hiện ra',
           thay='có thứ tự thì không sót, không trùng',
           loi=['Cho một phần giảm dần thì phần kia tự hiện ra. Có thứ tự thì không '
                'sót cách nào, cũng không kể trùng cách nào.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_do_cot(b):
    """C5⑥ Dò cột hơn nhau, thử lại đủ hai điều kiện."""
    return [
        _c('bia', 'Bài có hai điều kiện', so_bai(b),
           loi=['Bài này bắt thoả hai điều kiện cùng lúc, không phải một.']),
        _c('de_toan', 'Đề bài',
           de='Hai bạn có tất cả 12 viên kẹo, An hơn Bình 4 viên. Hỏi mỗi bạn mấy viên?',
           loi=['Hai bạn có tất cả mười hai viên kẹo, bạn An hơn bạn Bình bốn viên.',
                'Hỏi mỗi bạn có mấy viên.']),
        _c('y_toan', 'Gạch ra hai điều kiện',
           '① tổng bằng 12      ② An hơn Bình 4', buoc=1, soBuoc=3,
           loi=['Gạch ra hai điều kiện. Điều kiện một là tổng bằng mười hai.',
                'Điều kiện hai là An hơn Bình bốn viên.']),
        _c('bang_hang', 'Liệt kê theo điều kiện thứ nhất', so='12', hienLop=False,
           chuChinh='Mọi cách tách 12',
           chuPhu='11 và 1 · 10 và 2 · 9 và 3 · 8 và 4 · 7 và 5 · 6 và 6',
           loi=['Liệt kê theo điều kiện thứ nhất, như bài trước đã làm.']),
        _c('y_toan', 'Dò cột hơn nhau theo điều kiện thứ hai',
           'cột hơn nhau: 10 · 8 · 6 · 4 · 2 · 0', buoc=2, soBuoc=3,
           loi=['Giờ dò cột hơn nhau. Nó chạy mười, tám, sáu, bốn, hai, không.',
                'Dòng có số bốn là dòng tám và bốn.']),
        _c('so_do_doan', 'Sơ đồ của dòng vừa chọn', be=4, lon=8,
           nhanBe='Bình', nhanLon='An', hienHieu=True, chuHieu='hơn 4',
           chuTong='tổng 12',
           loi=['Vẽ ra thì thấy An tám viên, Bình bốn viên, khúc dôi ra đúng bốn.']),
        _c('y_toan', 'Thử lại ĐỦ CẢ HAI điều kiện',
           'tổng: 8 + 4 = 12   ·   hơn nhau: 8 − 4 = 4', buoc=3, soBuoc=3,
           loi=['Thử lại đủ cả hai điều kiện. Tám cộng bốn bằng mười hai, đúng tổng.',
                'Tám trừ bốn bằng bốn, đúng phần hơn.']),
        _c('y_toan', 'Đáp số', 'An 8 viên · Bình 4 viên',
           loi=['Đáp số là An tám viên, Bình bốn viên.']),
        _c('cong_thuc', 'Chỗ hay mất điểm nhất',
           congThuc='chỉ thử MỘT điều kiện là chưa xong bài',
           thay='có bạn chọn 7 và 3 vì cộng lại đúng 10, mà quên phần hơn',
           loi=['Chỉ thử một điều kiện là chưa xong bài. Đó là chỗ hay mất điểm nhất.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_ve_theo_phan(b):
    """C5⑦ Vẽ theo phần: gấp mấy lần là mấy khối."""
    return [
        _c('bia', 'Vẽ theo phần', so_bai(b),
           loi=['Chữ gấp mấy lần luôn nói về phần. Bài này học cách vẽ nó ra.']),
        _c('de_toan', 'Đề bài',
           de='Bố hái được số cam gấp 3 lần con. Cả hai hái được 12 quả. Có tất cả mấy phần bằng nhau?',
           loi=['Bố hái được số cam gấp ba lần con. Cả hai bố con hái được mười hai '
                'quả.',
                'Hỏi có tất cả mấy phần bằng nhau.']),
        _c('y_toan', 'Gấp mấy lần thì vẽ mấy khối', 'con 1 khối · bố 3 khối',
           buoc=1, soBuoc=3,
           loi=['Gấp mấy lần thì vẽ bấy nhiêu khối. Con một khối.',
                'Bố gấp ba lần con nên bố ba khối y hệt.']),
        _c('so_do_doan', 'Vẽ ra thành sơ đồ phần', be=3, lon=9,
           nhanBe='con', nhanLon='bố', phanBe=1, phanLon=3, chuTong='tổng 12 quả',
           chuPhu='Mọi khối đều bằng nhau.',
           loi=['Vẽ ra thành sơ đồ. Đoạn của con một khối, đoạn của bố ba khối.',
                'Mọi khối đều bằng nhau.']),
        _c('y_toan', 'Ngoặc ôm cả hai đoạn', 'cả 12 quả nằm trọn trong các khối ấy',
           buoc=2, soBuoc=3,
           loi=['Ngoặc ôm cả hai đoạn lại. Cả mười hai quả nằm trọn trong các khối '
                'ấy.']),
        _c('y_toan', 'Đếm tổng số phần', '1 + 3 = 4 phần', buoc=3, soBuoc=3,
           loi=['Đếm tổng số phần. Một cộng ba bằng bốn phần bằng nhau.']),
        _c('y_toan', 'Đáp số', 'có 4 phần bằng nhau',
           loi=['Đáp số là có bốn phần bằng nhau.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Chị gấp đôi PHẦN CỦA EM, không gấp đôi cả gói.',
           loi=['Có bạn thấy chị gấp đôi em, cả hai có chín viên, rồi lấy chín nhân '
                'hai được mười tám viên cho chị.',
                'Cả gói chỉ có chín viên thì kẹo mọc thêm ở đâu ra. Chị gấp đôi phần '
                'của em thôi.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='"gấp mấy lần" nói về PHẦN',
           thay='vẽ khối trước, đếm phần sau, rồi mới tính',
           loi=['Con nhớ lại một lần nữa. Gấp mấy lần thì nói về phần. Vẽ khối trước, '
                'đếm phần sau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_chia_phan(b):
    """C5⑧ Chia tổng cho số phần rồi trả về từng người."""
    return [
        _c('bia', 'Tìm một phần rồi trả về', so_bai(b),
           loi=['Đếm phần xong rồi thì chia, rồi trả kẹo về cho từng người.']),
        _c('de_toan', 'Đề bài',
           de='Bố hái được số cam gấp 3 lần con. Cả hai hái được 12 quả. Hỏi mỗi người mấy quả?',
           loi=['Bố hái được số cam gấp ba lần con. Cả hai hái được mười hai quả.',
                'Hỏi mỗi người hái được mấy quả.']),
        _c('y_toan', 'Đếm tổng số phần trước', '1 + 3 = 4 phần', buoc=1, soBuoc=3,
           loi=['Đếm tổng số phần trước. Con một phần, bố ba phần, cộng lại bốn phần '
                'bằng nhau.']),
        _c('y_toan', 'Chia tổng cho số phần để tìm MỘT phần', '12 : 4 = 3',
           buoc=2, soBuoc=3,
           loi=['Chia tổng cho số phần để tìm một phần.',
                'Mười hai chia bốn bằng ba. Vậy một phần là ba quả.']),
        _c('so_do_doan', 'Mỗi khối là 3 quả', be=3, lon=9,
           nhanBe='con', nhanLon='bố', phanBe=1, phanLon=3, chuTong='tổng 12 quả',
           chuPhu='Con 1 khối là 3 quả. Bố 3 khối là 9 quả.',
           loi=['Giờ mỗi khối đã biết là ba quả.',
                'Con một khối nên được ba quả. Bố ba khối nên được chín quả.']),
        _c('y_toan', 'Trả về cho từng người', 'con: 3 quả   ·   bố: 3 × 3 = 9 quả',
           buoc=3, soBuoc=3,
           loi=['Trả về cho từng người. Con ba quả. Bố ba nhân ba bằng chín quả.']),
        _c('y_toan', 'Thử lại đủ hai điều kiện', '3 + 9 = 12  ·  9 gấp 3 lần 3',
           loi=['Thử lại đủ hai điều kiện. Ba cộng chín bằng mười hai, đúng tổng.',
                'Và chín gấp ba lần ba, đúng số lần gấp.']),
        _c('y_toan', 'Đáp số', 'con 3 quả · bố 9 quả',
           loi=['Đáp số là con ba quả, bố chín quả.']),
        _c('cong_thuc', 'Bốn nhịp, không bỏ nhịp nào',
           congThuc='đếm phần → chia tìm 1 phần → trả về từng người → thử lại',
           thay='tìm được 1 phần mới đi được nửa đường',
           loi=['Bốn nhịp. Đếm phần, chia tìm một phần, trả về từng người, rồi thử '
                'lại.',
                'Tìm được một phần mới đi được nửa đường thôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_tuoi_sau_nam(b):
    """C5⑨ Tuổi sau mấy năm."""
    return [
        _c('bia', 'Tuổi sau mấy năm', so_bai(b),
           loi=['Thời gian trôi thì ai cũng thêm tuổi, và thêm bằng nhau.']),
        _c('de_toan', 'Đề bài',
           de='Năm nay mẹ 32 tuổi, con 7 tuổi. Mẹ hơn con mấy tuổi, và sau 5 năm mỗi người mấy tuổi?',
           loi=['Năm nay mẹ ba mươi hai tuổi, con bảy tuổi.',
                'Hỏi mẹ hơn con bao nhiêu tuổi, và sau năm năm nữa mỗi người bao nhiêu '
                'tuổi.']),
        _c('y_toan', 'Tìm phần hơn của năm nay', '32 − 7 = 25', buoc=1, soBuoc=3,
           loi=['Tìm phần hơn của năm nay. Ba mươi hai trừ bảy bằng hai mươi lăm.',
                'Mẹ hơn con hai mươi lăm tuổi.']),
        _c('y_toan', 'Sau mấy năm thì AI CŨNG thêm bấy nhiêu',
           'cả mẹ lẫn con đều thêm đúng 5 tuổi', buoc=2, soBuoc=3,
           loi=['Sau mấy năm thì ai cũng thêm bấy nhiêu. Thời gian công bằng với tất '
                'cả.',
                'Sau năm năm thì cả mẹ lẫn con đều thêm đúng năm tuổi.']),
        _c('y_toan', 'Tính tuổi mẹ', '32 + 5 = 37', buoc=3, soBuoc=3,
           loi=['Mẹ ba mươi hai cộng năm bằng ba mươi bảy tuổi.']),
        _c('y_toan', 'Tính tuổi con', '7 + 5 = 12',
           loi=['Con bảy cộng năm bằng mười hai tuổi.']),
        _c('so_do_doan', 'Hai đoạn cùng dài thêm 5', be=12, lon=37,
           nhanBe='con', nhanLon='mẹ', hienHieu=True, chuHieu='hơn 25 tuổi',
           chuPhu='Sau 5 năm: mẹ 37 tuổi, con 12 tuổi.',
           loi=['Vẽ ra thì thấy hai đoạn cùng dài thêm năm.']),
        _c('y_toan', 'Đáp số', 'hơn 25 tuổi · mẹ 37 · con 12',
           loi=['Đáp số là mẹ hơn con hai mươi lăm tuổi. Sau năm năm mẹ ba mươi bảy '
                'tuổi, con mười hai tuổi.']),
        _c('cong_thuc', 'Chỗ hay quên nhất',
           congThuc='cộng tuổi cho CẢ HAI người',
           thay='đừng để một người đứng yên',
           loi=['Chỗ hay quên nhất là chỉ cộng tuổi cho một người rồi để người kia '
                'đứng yên.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hieu_tuoi(b):
    """C5⑩ Phần hơn tuổi không bao giờ đổi."""
    return [
        _c('bia', 'Phần hơn tuổi không đổi', so_bai(b),
           loi=['Một khám phá rất đẹp, và nó đúng mãi mãi.']),
        _c('de_toan', 'Đề bài',
           de='Năm nay em 6 tuổi, anh 9 tuổi. Sau 2 năm nữa anh hơn em bao nhiêu tuổi?',
           loi=['Năm nay em sáu tuổi, anh chín tuổi.',
                'Hỏi sau hai năm nữa anh hơn em bao nhiêu tuổi.']),
        _c('so_do_doan', 'Phần hơn của năm nay', be=6, lon=9,
           nhanBe='em', nhanLon='anh', hienHieu=True, chuHieu='hơn 3 tuổi',
           chuPhu='9 − 6 = 3 tuổi.',
           loi=['Phần hơn của năm nay. Chín trừ sáu bằng ba. Anh hơn em ba tuổi.']),
        _c('y_toan', 'Sau 2 năm, tính tuổi hai người', 'em 6 + 2 = 8 · anh 9 + 2 = 11',
           buoc=1, soBuoc=3,
           loi=['Sau hai năm, em sáu cộng hai bằng tám tuổi.',
                'Anh chín cộng hai bằng mười một tuổi.']),
        _c('so_do_doan', 'Hai đoạn cùng dài thêm 2', be=8, lon=11,
           nhanBe='em', nhanLon='anh', hienHieu=True, chuHieu='vẫn hơn 3 tuổi',
           chuPhu='Khúc dôi ra không hề đổi.',
           loi=['Vẽ lại thì thấy hai đoạn cùng dài thêm hai.',
                'Khúc dôi ra không hề đổi.']),
        _c('y_toan', 'Tính lại phần hơn', '11 − 8 = 3', buoc=2, soBuoc=3,
           loi=['Tính lại phần hơn. Mười một trừ tám bằng ba. Vẫn đúng ba tuổi như '
                'cũ.']),
        _c('y_toan', 'Vì sao lại thế', 'hai bên cùng thêm bằng nhau', buoc=3, soBuoc=3,
           loi=['Vì hai bên cùng thêm bằng nhau, nên phần hơn giữ nguyên.']),
        _c('y_toan', 'Đáp số', 'vẫn 3 tuổi',
           loi=['Đáp số là vẫn ba tuổi.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Không phải chỉ mình anh thêm tuổi.',
           loi=['Có bạn bảo anh hơn em ba tuổi thì sau hai năm anh hơn em năm tuổi.',
                'Em cũng thêm hai tuổi chứ có đứng yên đâu.']),
        _c('cong_thuc', 'Kho báu của mọi bài toán tuổi',
           congThuc='phần HƠN tuổi KHÔNG BAO GIỜ đổi',
           thay='dù mười năm hay một trăm năm nữa',
           loi=['Phần hơn tuổi giữa hai người không bao giờ đổi, dù mười năm hay một '
                'trăm năm nữa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_moi_gio_nhan(b):
    """C5⑪ Biết mỗi giờ, hỏi tất cả."""
    return [
        _c('bia', 'Chữ "mỗi"', so_bai(b),
           loi=['Thấy chữ mỗi là thấy một phần đều nhau lặp đi lặp lại.']),
        _c('de_toan', 'Đề bài',
           de='Một vòi nước mỗi phút chảy được 3 lít. Hỏi sau 4 phút vòi chảy được mấy lít?',
           loi=['Một vòi nước mỗi phút chảy được ba lít.',
                'Hỏi sau bốn phút vòi chảy được bao nhiêu lít nước.']),
        _c('y_toan', 'Chữ "mỗi" nghĩa là gì', 'phút nào cũng đều tăm tắp 3 lít',
           buoc=1, soBuoc=3,
           loi=['Mỗi phút ba lít nghĩa là phút nào cũng đều tăm tắp ba lít.']),
        _c('luoi_cham', 'Bốn phút, mỗi phút 3 lít', hang=4, cot=3,
           chuPhu='4 × 3 = 12 lít',
           loi=['Vẽ bốn phút, mỗi phút ba lít.']),
        _c('y_toan', 'Các phần bằng nhau lặp lại là việc của phép nhân', '3 × 4 = 12',
           buoc=2, soBuoc=3,
           loi=['Các phần bằng nhau lặp lại là việc của phép nhân.',
                'Ba nhân bốn bằng mười hai.']),
        _c('y_toan', 'Đáp số', '12 lít nước', buoc=3, soBuoc=3,
           loi=['Đáp số là mười hai lít nước.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Không cộng 4 ki lô mét với 3 giờ.',
           loi=['Có bạn giải bài mỗi giờ đi bốn ki lô mét, đi ba giờ, bằng phép cộng.',
                'Bốn là ki lô mét còn ba là giờ. Hai thứ khác loại thì không cộng '
                'thẳng với nhau được.']),
        _c('cong_thuc', 'Ba bài, một bộ xương',
           congThuc='mỗi giờ 5 áo · 3 giờ  →  5 × 3 = 15 áo',
           thay='mỗi giờ 4 ki lô mét · 3 giờ  →  4 × 3 = 12 ki lô mét',
           loi=['Bài may áo, bài đi đường, bài chảy nước khoác áo khác nhau mà chung '
                'một bộ xương.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='biết MỖI phần, hỏi TẤT CẢ  →  NHÂN',
           loi=['Con nhớ lại một lần nữa. Biết mỗi phần rồi hỏi tất cả thì nhân.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_moi_gio_chia(b):
    """C5⑫ Biết tất cả, hỏi mỗi giờ."""
    return [
        _c('bia', 'Bài ngược của chữ "mỗi"', so_bai(b),
           loi=['Bài trước biết mỗi giờ rồi hỏi tất cả. Bài này ngược lại.']),
        _c('de_toan', 'Đề bài',
           de='Cô May làm 3 giờ được tất cả 15 cái áo, giờ nào cũng như giờ nào. Hỏi mỗi giờ mấy cái?',
           loi=['Cô May làm ba giờ được tất cả mười lăm cái áo, giờ nào cũng như giờ '
                'nào.',
                'Hỏi mỗi giờ cô may được mấy cái áo.']),
        _c('y_toan', 'Đề cho biết cái gì', 'biết TẤT CẢ, hỏi MỖI phần',
           buoc=1, soBuoc=3,
           loi=['Lần này đề cho biết tất cả rồi hỏi mỗi phần.',
                'Đúng ngược với bài trước.']),
        _c('nhom_deu', 'Tách đều 15 cái áo cho 3 giờ', tong=15, moiNhom=5,
           chuPhu='Mỗi giờ được 5 cái áo.',
           loi=['Tách đều mười lăm cái áo cho ba giờ.',
                'Mỗi giờ được năm cái áo.']),
        _c('y_toan', 'Tách đều là việc của phép chia', '15 : 3 = 5', buoc=2, soBuoc=3,
           loi=['Tách đều tất cả ra từng phần là việc của phép chia.',
                'Mười lăm chia ba bằng năm.']),
        _c('y_toan', 'Thử lại bằng phép nhân', '5 × 3 = 15', buoc=3, soBuoc=3,
           loi=['Thử lại bằng phép nhân. Năm nhân ba bằng mười lăm, khớp đúng số áo '
                'của cả ba giờ.']),
        _c('y_toan', 'Đáp số', 'mỗi giờ 5 cái áo',
           loi=['Đáp số là mỗi giờ năm cái áo.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thấy chữ "mỗi giờ" không có nghĩa là nhân.',
           loi=['Có bạn thấy đề có chữ mỗi giờ là nhân luôn, được bốn mươi lăm cái '
                'áo.',
                'Cả ba giờ mới được mười lăm cái, thì một giờ phải ít hơn mười lăm '
                'chứ.']),
        _c('cong_thuc', 'Hai bài đi cặp với nhau',
           congThuc='biết MỖI phần, hỏi TẤT CẢ  →  nhân',
           thay='biết TẤT CẢ, hỏi MỖI phần  →  chia',
           loi=['Biết mỗi phần rồi hỏi tất cả thì nhân. Biết tất cả rồi hỏi mỗi phần '
                'thì chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 6 · THÁM TỬ TÍ HON — tám kịch bản.
#
# ⚠ Chữ "thám tử" và "vũ khí" nằm trong TU_CAM — chúng là vỏ nhân vật của sách.
# Tên chương giữ nguyên trong dữ liệu, nhưng lời đọc và chữ trên màn phải tránh.
# ═══════════════════════════════════════════════════════════════════════════


def kb2_di_lui(b):
    """C6① Đi lùi qua hai máy, đảo phép từng máy."""
    return [
        _c('bia', 'Đi lùi qua hai máy', so_bai(b),
           loi=['Số cần tìm đi qua hai máy rồi mới ra kết quả. Mình đi lùi để bắt '
                'nó.']),
        _c('de_toan', 'Đề bài',
           de='Một số đem trừ đi 2, rồi nhân với 3 thì được 12. Tìm số ấy.',
           loi=['Một số đem trừ đi hai, rồi nhân với ba thì được mười hai.',
                'Tìm số ấy.']),
        _c('y_toan', 'Vẽ hành trình xuôi', '?  →  máy − 2  →  máy × 3  →  12',
           buoc=1, soBuoc=3,
           loi=['Vẽ hành trình xuôi của số cần tìm.',
                'Nó chui vào máy trừ hai, rồi vào máy nhân ba, và chạy ra thành mười '
                'hai.']),
        _c('cong_thuc', 'Đi lùi thì đảo phép từng máy',
           congThuc='máy × 3  lùi thành  máy : 3',
           thay='máy − 2  lùi thành  máy + 2',
           loi=['Đi lùi là gỡ lại việc máy vừa làm, nên phải đảo phép.',
                'Máy nhân ba lùi thành máy chia ba. Máy trừ hai lùi thành máy cộng '
                'hai.']),
        _c('y_toan', 'Lùi qua máy thứ nhất', '12 : 3 = 4', buoc=2, soBuoc=3,
           loi=['Trước khi nhân ba, số ấy là mười hai chia ba bằng bốn.']),
        _c('y_toan', 'Lùi qua máy thứ hai', '4 + 2 = 6', buoc=3, soBuoc=3,
           loi=['Trước khi trừ hai, số ấy là bốn cộng hai bằng sáu.']),
        _c('y_toan', 'Thử lại bằng cách chạy xuôi', '6 − 2 = 4   ·   4 × 3 = 12',
           loi=['Thử lại bằng cách chạy xuôi. Sáu trừ hai bằng bốn, rồi bốn nhân ba '
                'bằng mười hai, khớp đúng đề bài.']),
        _c('y_toan', 'Đáp số', 'Số cần tìm là 6',
           loi=['Số cần tìm là sáu.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='cộng ⇄ trừ      ·      nhân ⇄ chia',
           loi=['Con nhớ lại một lần nữa. Cộng đảo thành trừ, nhân đảo thành chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_thu_tu_lui(b):
    """C6② Máy làm sau cùng thì lùi qua trước."""
    return [
        _c('bia', 'Thứ tự đi lùi', so_bai(b),
           loi=['Đảo phép đúng rồi mà lùi sai thứ tự thì vẫn tắc đường.']),
        _c('de_toan', 'Đề bài',
           de='Một số đem cộng 3, rồi nhân với 2 thì được 16. Tìm số ấy.',
           loi=['Một số đem cộng ba, rồi nhân với hai thì được mười sáu.',
                'Tìm số ấy.']),
        _c('y_toan', 'Máy nào làm sau cùng', '?  →  máy + 3  →  máy × 2  →  16',
           buoc=1, soBuoc=3,
           loi=['Số ấy đi qua máy cộng ba trước, rồi mới qua máy nhân hai.',
                'Vậy máy nhân hai là máy làm sau cùng.']),
        _c('cong_thuc', 'Máy làm sau cùng thì lùi qua trước',
           congThuc='cởi ba lô trước, rồi mới cởi áo',
           thay='việc gì làm SAU thì gỡ TRƯỚC',
           loi=['Cởi ba lô trước rồi mới cởi áo. Việc gì làm sau thì gỡ trước.']),
        _c('y_toan', 'Lùi qua máy nhân 2 trước', '16 : 2 = 8', buoc=2, soBuoc=3,
           loi=['Nên lùi qua máy nhân hai trước. Mười sáu chia hai bằng tám.']),
        _c('y_toan', 'Rồi mới lùi qua máy cộng 3', '8 − 3 = 5', buoc=3, soBuoc=3,
           loi=['Rồi mới lùi qua máy cộng ba. Tám trừ ba bằng năm.']),
        _c('y_toan', 'Thử lại bằng cách chạy xuôi', '5 + 3 = 8   ·   8 × 2 = 16',
           loi=['Thử lại. Năm cộng ba bằng tám, rồi tám nhân hai bằng mười sáu, khớp '
                'đúng đề bài.']),
        _c('y_toan', 'Nếu lùi sai thứ tự thì sao', '16 − 3 = 13  →  13 không chia đôi được',
           loi=['Nếu lùi qua máy cộng ba trước thì được mười sáu trừ ba bằng mười ba.',
                'Rồi tắc, vì mười ba không chia đôi được. Tắc đường chính là chuông '
                'báo động.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='máy làm SAU CÙNG thì lùi qua TRƯỚC',
           loi=['Con nhớ lại một lần nữa. Máy làm sau cùng thì lùi qua trước.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_gan_hai_chan(b):
    """C6③ Gắn tạm hai chân cho tất cả."""
    return [
        _c('bia', 'Đếm chân gà và chó', so_bai(b),
           loi=['Biết tổng số đầu và tổng số chân, tìm ra mỗi loại mấy con.']),
        _c('de_toan', 'Đề bài',
           de='Trong sân có gà và chó, đếm được 5 cái đầu và 14 cái chân. Sau khi gắn tạm mỗi con hai chân thì còn thừa mấy chân?',
           loi=['Trong sân có gà và chó, đếm được năm cái đầu và mười bốn cái chân.',
                'Hỏi sau khi gắn tạm mỗi con hai chân thì còn thừa mấy chân.']),
        _c('y_toan', 'Mỗi con vật chỉ có một cái đầu', '5 cái đầu  →  5 con vật',
           buoc=1, soBuoc=3,
           loi=['Mỗi con vật, dù gà hay chó, đều chỉ có một cái đầu.',
                'Đếm được năm cái đầu nên chắc chắn có năm con vật.']),
        _c('luoi_cham', 'Gắn tạm mỗi con hai chân', hang=5, cot=2,
           chuPhu='5 × 2 = 10 chân',
           loi=['Gà có hai chân, chó có bốn chân, nên con nào cũng có ít nhất hai '
                'chân.',
                'Gắn tạm mỗi con hai chân thì được mười chân.']),
        _c('y_toan', 'Đề nói có 14 chân', '14 − 10 = 4', buoc=2, soBuoc=3,
           loi=['Đề nói có mười bốn chân mà mình mới gắn mười chân.',
                'Mười bốn trừ mười bằng bốn. Còn thừa bốn chân.']),
        _c('y_toan', 'Đáp số', 'còn thừa 4 chân', buoc=3, soBuoc=3,
           loi=['Đáp số là còn thừa bốn chân.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Không lấy số CHÂN trừ số ĐẦU.',
           loi=['Có bạn lấy mười bốn cái chân trừ năm cái đầu được chín, rồi bảo có '
                'chín con chó.',
                'Chân và đầu khác loại nhau. Với lại cả sân chỉ có năm con vật.']),
        _c('cong_thuc', 'Ba bước của bài đếm chân',
           congThuc='① vẽ đủ số đầu   ② gắn tạm 2 chân cho tất cả',
           thay='③ chân còn thừa thì gắn thêm cho con bốn chân',
           loi=['Ba bước. Vẽ đủ số đầu. Gắn tạm hai chân cho tất cả. Rồi xem chân còn '
                'thừa.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='số ĐẦU chính là số CON',
           loi=['Con nhớ lại một lần nữa. Số đầu chính là số con vật.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_chan_thua(b):
    """C6④ Chân thừa chia thành từng cặp."""
    return [
        _c('bia', 'Chân thừa là của ai', so_bai(b),
           loi=['Bốn chân còn thừa kia là của mấy chú chó? Bài này tìm ra.']),
        _c('de_toan', 'Đề bài',
           de='Có 5 cái đầu và 14 cái chân. Gắn tạm mỗi con hai chân thì còn thừa 4 chân. Hỏi mấy con gà, mấy con chó?',
           loi=['Có năm cái đầu và mười bốn cái chân. Gắn tạm mỗi con hai chân thì còn '
                'thừa bốn chân.',
                'Hỏi có mấy con gà, mấy con chó.']),
        _c('y_toan', 'Mỗi chú chó còn thiếu hai chân', '4 − 2 = 2', buoc=1, soBuoc=3,
           loi=['Chó có bốn chân mà mới được gắn hai chân.',
                'Bốn trừ hai bằng hai. Mỗi chú chó còn thiếu đúng hai chân nữa.']),
        _c('nhom_deu', 'Chia 4 chân thừa thành từng cặp', tong=4, moiNhom=2,
           chuPhu='4 chia 2 được 2 cặp — mỗi cặp cho một chú chó.',
           loi=['Chia bốn chân thừa thành từng cặp. Bốn chia hai được hai cặp.',
                'Mỗi cặp gắn cho một chú chó.']),
        _c('y_toan', 'Vậy có 2 con chó', '5 − 2 = 3 con gà', buoc=2, soBuoc=3,
           loi=['Vậy có hai con chó. Còn lại năm trừ hai bằng ba con chỉ có hai chân, '
                'đó là gà.']),
        _c('y_toan', 'Thử lại cho chắc',
           'gà 3 × 2 = 6 chân   ·   chó 2 × 4 = 8 chân   ·   6 + 8 = 14',
           buoc=3, soBuoc=3,
           loi=['Thử lại. Gà ba nhân hai bằng sáu chân. Chó hai nhân bốn bằng tám '
                'chân.',
                'Sáu cộng tám bằng mười bốn chân, khớp đúng đề bài.']),
        _c('y_toan', 'Đáp số', '3 con gà và 2 con chó',
           loi=['Đáp số là ba con gà và hai con chó.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thừa 4 chân KHÔNG có nghĩa là 4 con chó.',
           loi=['Có bạn thấy thừa bốn chân rồi bảo luôn là có bốn con chó.',
                'Mỗi chú chó cần một cặp hai chân, nên bốn chân thừa chỉ gắn được cho '
                'hai chú.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chân thừa chia thành từng CẶP',
           thay='rồi cộng chân của tất cả để thử lại',
           loi=['Con nhớ lại một lần nữa. Chân thừa chia thành từng cặp, rồi cộng chân '
                'của tất cả để thử lại.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_cay_khoang(b):
    """C6⑤ Cây và khoảng — luật bàn tay."""
    return [
        _c('bia', 'Cây và khoảng', so_bai(b),
           loi=['Số cây và số khoảng không bằng nhau, và đó là cả bài học.']),
        _c('de_toan', 'Đề bài',
           de='Một lối đi trồng 5 cây, cây nọ cách cây kia 2 mét, trồng ở cả hai đầu. Lối đi dài bao nhiêu mét?',
           loi=['Một lối đi trồng năm cây, cây nọ cách cây kia hai mét, trồng ở cả hai '
                'đầu.',
                'Hỏi lối đi dài bao nhiêu mét.']),
        _c('y_toan', 'Xòe bàn tay ra mà đếm', '5 ngón  —  chỉ có 4 kẽ',
           buoc=1, soBuoc=3,
           loi=['Xòe bàn tay ra mà đếm. Năm ngón tay nhưng chỉ có bốn kẽ tay.',
                'Ngón là cây, kẽ là khoảng.']),
        _c('day_so', 'Năm cây thì bốn khoảng', so=[1, 2, 3, 4, 5],
           chuPhu='Giữa 5 cây chỉ có 4 khoảng.',
           loi=['Trồng năm cây thì chỉ có bốn khoảng.',
                'Số khoảng luôn ít hơn số cây đúng một, khi trồng cả hai đầu.']),
        _c('y_toan', 'Chiều dài đi với KHOẢNG', '2 × 4 = 8 mét', buoc=2, soBuoc=3,
           loi=['Chiều dài đi với khoảng, không đi với cây.',
                'Mỗi khoảng hai mét, có bốn khoảng, nên lối đi dài tám mét.']),
        _c('y_toan', 'Đáp số', '8 mét', buoc=3, soBuoc=3,
           loi=['Đáp số là tám mét.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Nhân với số CÂY thì ra 10 mét — sai.',
           loi=['Có bạn nhân hai với năm cây được mười mét.',
                'Cây chỉ đứng ở các mốc chứ không tạo nên chiều dài. Thứ tạo nên chiều '
                'dài là khoảng.']),
        _c('cong_thuc', 'Luật bàn tay',
           congThuc='trồng cả hai đầu:  số CÂY = số KHOẢNG + 1',
           thay='chiều dài thì nhân với số KHOẢNG',
           loi=['Trồng cả hai đầu thì số cây bằng số khoảng cộng một. Còn chiều dài '
                'thì nhân với số khoảng.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi trước: đề đang hỏi CÂY hay hỏi KHOẢNG?',
           loi=['Con nhớ lại một lần nữa. Hỏi trước xem đề đang hỏi cây hay hỏi '
                'khoảng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_tim_so_cay(b):
    """C6⑥ Biết chiều dài, tìm số cây."""
    return [
        _c('bia', 'Biết chiều dài, tìm số cây', so_bai(b),
           loi=['Bài trước biết số cây rồi hỏi chiều dài. Bài này ngược lại.']),
        _c('de_toan', 'Đề bài',
           de='Trồng cây dọc đoạn đường dài 15 mét, cây nọ cách cây kia 3 mét, trồng ở cả hai đầu. Trồng được mấy cây?',
           loi=['Trồng cây dọc một đoạn đường dài mười lăm mét, cây nọ cách cây kia ba '
                'mét, trồng ở cả hai đầu.',
                'Hỏi trồng được bao nhiêu cây.']),
        _c('y_toan', 'Tìm số khoảng trước đã', '15 : 3 = 5 khoảng', buoc=1, soBuoc=3,
           loi=['Chiều dài đi với khoảng, nên chia trước để ra số khoảng.',
                'Mười lăm chia ba bằng năm khoảng.']),
        _c('day_so', 'Năm khoảng thì sáu cây', so=[1, 2, 3, 4, 5, 6],
           chuPhu='Thêm một cây nữa ở đầu kia đường.',
           loi=['Năm khoảng thì có sáu cây, vì trồng cả hai đầu.']),
        _c('y_toan', 'Số cây nhiều hơn số khoảng đúng một', '5 + 1 = 6 cây',
           buoc=2, soBuoc=3,
           loi=['Số cây nhiều hơn số khoảng đúng một. Năm cộng một bằng sáu cây.']),
        _c('y_toan', 'Thử lại cho chắc', '3 × 5 = 15 mét', buoc=3, soBuoc=3,
           loi=['Thử lại. Sáu cây có năm khoảng, mỗi khoảng ba mét, ba nhân năm bằng '
                'mười lăm mét, khớp đúng đề bài.']),
        _c('y_toan', 'Đáp số', '6 cây',
           loi=['Đáp số là sáu cây.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Chia xong mới ra số KHOẢNG, chưa phải số cây.',
           loi=['Có bạn chia xong là ghi luôn đáp số, quên mất bước cộng một.',
                'Quên cộng một thì mất hẳn một cây ở đầu đường.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='chia ra số KHOẢNG  →  cộng 1  →  số CÂY',
           loi=['Con nhớ lại một lần nữa. Chia ra số khoảng, rồi cộng một mới ra số '
                'cây.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_ve_thang(b):
    """C6⑦ Vẽ thang xếp thứ tự."""
    return [
        _c('bia', 'Vẽ thang xếp thứ tự', so_bai(b),
           loi=['Đố kiểu ai hơn ai thì vẽ một chiếc thang ra là xong.']),
        _c('de_toan', 'Đề bài',
           de='Voi nặng hơn Gấu. Gấu nặng hơn Thỏ. Ai nặng nhất, ai nhẹ nhất, và Voi có nặng hơn Thỏ không?',
           loi=['Voi nặng hơn Gấu. Gấu nặng hơn Thỏ.',
                'Hỏi ai nặng nhất, ai nhẹ nhất, và Voi có nặng hơn Thỏ không.']),
        _c('y_toan', 'Manh mối thứ nhất xếp được một bạn', 'Voi đứng trên Gấu',
           buoc=1, soBuoc=3,
           loi=['Manh mối thứ nhất nói Voi nặng hơn Gấu, nên Voi đứng trên Gấu.']),
        _c('san_bang', 'Manh mối thứ hai xếp nốt bạn còn lại', so=[9, 6, 3],
           chuPhu='Từ trên xuống: Voi, Gấu, Thỏ.',
           loi=['Manh mối thứ hai nói Gấu nặng hơn Thỏ, nên Thỏ đứng dưới Gấu.',
                'Thang thành Voi, Gấu, Thỏ từ trên xuống.']),
        _c('y_toan', 'Đọc thang là biết ngay', 'Voi nặng nhất  ·  Thỏ nhẹ nhất',
           buoc=2, soBuoc=3,
           loi=['Đọc thang là biết ngay. Voi đứng trên cùng nên nặng nhất. Thỏ đứng '
                'dưới cùng nên nhẹ nhất.']),
        _c('y_toan', 'Thang cho biết cả điều đề không nói thẳng',
           'Voi trên cùng, Thỏ dưới cùng  →  Voi nặng hơn Thỏ', buoc=3, soBuoc=3,
           loi=['Đề không nói gì về Voi với Thỏ, nhưng thang thì nói.',
                'Voi đứng trên cùng còn Thỏ đứng dưới cùng, nên Voi nặng hơn Thỏ.']),
        _c('y_toan', 'Đáp số', 'Voi nặng nhất · Thỏ nhẹ nhất · Voi nặng hơn Thỏ',
           loi=['Đáp số là Voi nặng nhất, Thỏ nhẹ nhất, và Voi nặng hơn Thỏ.']),
        _c('cong_thuc', 'Hai manh mối, ba câu trả lời',
           congThuc='mỗi manh mối xếp được MỘT bạn vào thang',
           thay='xếp xong thì thang trả lời được cả câu đề không hỏi thẳng',
           loi=['Mỗi manh mối xếp được một bạn vào thang. Xếp xong thì thang trả lời '
                'được cả câu đề không hỏi thẳng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_bang_loai_tru(b):
    """C6⑧ Bảng loại trừ."""
    HANG = ['Mai', 'Đào', 'Cúc']
    COT = ['hồng', 'sen', 'cúc']
    return [
        _c('bia', 'Bảng loại trừ', so_bai(b),
           loi=['Đố kiểu ai cầm cái gì thì kẻ một cái bảng ra là tìm được, không phải '
                'đoán mò.']),
        _c('de_toan', 'Đề bài',
           de='Ba bạn Mai, Đào, Cúc cầm ba bông hoa hồng, sen, cúc. Mai không cầm hoa hồng. Đào cầm hoa sen. Hỏi mỗi bạn cầm hoa gì?',
           loi=['Ba bạn Mai, Đào, Cúc cầm ba bông hoa hồng, sen, cúc.',
                'Biết Mai không cầm hoa hồng, và Đào cầm hoa sen. Hỏi mỗi bạn cầm hoa '
                'gì.']),
        _c('bang_loai_tru', 'Kẻ bảng ba hàng ba cột', hang=HANG, cot=COT,
           o=[['', '', ''], ['', '', ''], ['', '', '']],
           chuPhu='Mỗi hàng một bạn, mỗi cột một bông hoa.',
           loi=['Kẻ bảng ba hàng ba cột. Mỗi hàng một bạn, mỗi cột một bông hoa.']),
        _c('bang_loai_tru', 'Đánh dấu từ manh mối chắc nhất', hang=HANG, cot=COT,
           o=[['', '', ''], ['', 'v', ''], ['', '', '']],
           chuPhu='Đào cầm hoa sen — đánh dấu đúng ô ấy.',
           loi=['Đánh dấu từ manh mối chắc nhất. Đào cầm hoa sen, nên đánh dấu đúng ô '
                'ấy.']),
        _c('bang_loai_tru', 'Gạch cả hàng và cả cột', hang=HANG, cot=COT,
           o=[['', 'x', ''], ['x', 'v', 'x'], ['', 'x', '']],
           chuPhu='Một bạn chỉ cầm một bông, một bông chỉ một chủ.',
           loi=['Gạch cả hàng Đào và cả cột sen.',
                'Vì một bạn chỉ cầm một bông, và một bông chỉ có một chủ.']),
        _c('bang_loai_tru', 'Dùng nốt manh mối còn lại', hang=HANG, cot=COT,
           o=[['x', 'x', 'v'], ['x', 'v', 'x'], ['', 'x', 'x']],
           chuPhu='Mai không cầm hồng → hàng Mai chỉ còn ô cúc.',
           loi=['Mai không cầm hoa hồng nên gạch ô ấy.',
                'Hàng Mai chỉ còn một ô trống là hoa cúc, vậy Mai cầm hoa cúc.']),
        _c('bang_loai_tru', 'Hàng cuối chỉ còn một ô', hang=HANG, cot=COT,
           o=[['x', 'x', 'v'], ['x', 'v', 'x'], ['v', 'x', 'x']],
           chuPhu='Còn lại Cúc cầm hoa hồng.',
           loi=['Hàng cuối chỉ còn một ô trống, vậy Cúc cầm hoa hồng.']),
        _c('y_toan', 'Đáp số', 'Mai cúc · Đào sen · Cúc hồng',
           loi=['Đáp số là Mai cầm hoa cúc, Đào cầm hoa sen, Cúc cầm hoa hồng.',
                'Bạn tên Cúc lại không cầm hoa cúc. Đề trêu mình đấy, nhưng bảng thì '
                'không bị lừa.']),
        _c('cong_thuc', 'Ba bước của bảng loại trừ',
           congThuc='① đánh dấu từ manh mối chắc nhất',
           thay='② gạch cả hàng cả cột   ③ hàng nào còn một ô, ô ấy là đáp án',
           loi=['Ba bước. Đánh dấu từ manh mối chắc nhất. Gạch cả hàng cả cột. Hàng '
                'nào chỉ còn một ô, ô ấy chính là đáp án.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 7 · VƯƠNG QUỐC HÌNH HỌC — mười kịch bản.
# ⚠ Viết "xăng-ti-mét" chứ đừng viết tắt: máy đọc hai chữ cái thành tiếng Anh.
# ═══════════════════════════════════════════════════════════════════════════


def kb2_nhan_hinh(b):
    """C7① Nhận mặt hình bằng cạnh và đỉnh."""
    return [
        _c('bia', 'Nhận mặt hình', so_bai(b),
           loi=['Nhận ra hình bằng cách đếm cạnh đếm đỉnh, đừng tin dáng đứng.']),
        _c('tam_giac', 'Tam giác có 3 cạnh và 3 đỉnh', day=8, cao=6,
           loi=['Mỗi hình có một tấm danh thiếp, là số cạnh và số đỉnh.',
                'Tam giác có ba cạnh và ba đỉnh.']),
        _c('hinh_cn', 'Hình chữ nhật: 4 cạnh, 4 đỉnh', dai=6, rong=4,
           loi=['Hình chữ nhật có bốn cạnh và bốn đỉnh.',
                'Hai cạnh dài bằng nhau, hai cạnh ngắn bằng nhau.']),
        _c('hinh_cn', 'Hình vuông: 4 cạnh BẰNG NHAU', dai=5, rong=5,
           loi=['Hình vuông cũng bốn cạnh bốn đỉnh, nhưng cả bốn cạnh bằng nhau.']),
        _c('y_toan', 'Bốn cạnh bốn đỉnh thì mang họ TỨ GIÁC',
           'hình vuông · hình chữ nhật · cả hình xiêu vẹo', buoc=1, soBuoc=3,
           loi=['Mọi hình bốn cạnh bốn đỉnh đều mang họ tứ giác.',
                'Kể cả hình xiêu vẹo cũng được dự hội đàng hoàng.']),
        _c('y_toan', 'Hình bị XOAY vẫn là chính nó',
           'hình vuông xoay nghiêng vẫn đủ 4 cạnh bằng nhau', buoc=2, soBuoc=3,
           loi=['Hình vuông đặt xoay nghiêng trông lạ mắt.',
                'Nhưng đếm vẫn bốn cạnh bằng nhau và bốn đỉnh, nên vẫn là hình '
                'vuông.']),
        _c('y_toan', 'Đáp số', 'tam giác 3 cạnh 3 đỉnh · hình vuông xoay vẫn là hình vuông',
           buoc=3, soBuoc=3,
           loi=['Tam giác có ba cạnh ba đỉnh. Hình vuông xoay nghiêng vẫn là hình '
                'vuông.']),
        _c('cong_thuc', 'Cách nhận hình',
           congThuc='ĐẾM CẠNH  ·  ĐẾM ĐỈNH',
           thay='đừng tin dáng đứng của hình',
           loi=['Đếm cạnh, đếm đỉnh. Đừng tin dáng đứng của hình.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='4 cạnh 4 đỉnh  →  họ TỨ GIÁC',
           loi=['Con nhớ lại một lần nữa. Bốn cạnh bốn đỉnh thì mang họ tứ giác.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_kien_bo(b):
    """C7② Đường kiến bò một vòng."""
    return [
        _c('bia', 'Đường kiến bò một vòng', so_bai(b),
           loi=['Thả một chú kiến bò quanh mép hình, xem nó đi được bao xa.']),
        _c('de_toan', 'Đề bài',
           de='Tam giác có ba cạnh 3, 4 và 5 xăng-ti-mét. Chú kiến bò đúng một vòng quanh hình được bao nhiêu xăng-ti-mét?',
           loi=['Một hình tam giác có ba cạnh dài ba, bốn và năm xăng ti mét.',
                'Chú kiến bò đúng một vòng quanh hình được bao nhiêu xăng ti mét?']),
        _c('tam_giac', 'Chú kiến đi hết cạnh này sang cạnh kia', day=10, cao=6,
           chuPhu='Đi đủ một vòng rồi về đúng chỗ cũ.',
           loi=['Chú kiến đi hết cạnh này sang cạnh kia, đủ một vòng rồi về chỗ cũ.']),
        _c('y_toan', 'Quãng đường bằng tổng độ dài các cạnh', '3 + 4 + 5 = 12',
           buoc=1, soBuoc=3,
           loi=['Quãng đường chú kiến đi bằng tổng độ dài các cạnh.',
                'Ba cộng bốn cộng năm bằng mười hai.']),
        _c('y_toan', 'Đáp số', '12 xăng-ti-mét', buoc=2, soBuoc=3,
           loi=['Đáp số là mười hai xăng ti mét.']),
        _c('hinh_cn', 'Hình chữ nhật thì cộng đủ BỐN cạnh', dai=6, rong=3,
           loi=['Với hình chữ nhật thì phải cộng đủ bốn cạnh.',
                'Sáu cộng ba cộng sáu cộng ba bằng mười tám.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Cộng thiếu cạnh nằm khuất phía dưới.',
           buoc=3, soBuoc=3,
           loi=['Có bạn cộng thiếu một cạnh, vì cạnh ấy nằm khuất phía dưới hình.',
                'Chú kiến phải về đúng chỗ xuất phát mới là một vòng.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='cộng ĐỦ các cạnh, không sót cạnh nào',
           thay='lên lớp 3, quãng đường ấy có tên riêng là CHU VI',
           loi=['Cộng đủ các cạnh, không sót cạnh nào.',
                'Lên lớp ba, quãng đường ấy sẽ có tên riêng là chu vi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hinh_don(b):
    """C7③ Đánh số mảnh rồi đếm hình đơn."""
    return [
        _c('bia', 'Đánh số rồi đếm', so_bai(b),
           loi=['Đếm hình trong hình ghép thì phải làm có thứ tự, không thì sót.']),
        _c('de_toan', 'Đề bài',
           de='Một hình chữ nhật chia thành 3 ô vuông nhỏ xếp hàng ngang. Có mấy hình đơn?',
           loi=['Một hình chữ nhật được chia thành ba ô vuông nhỏ xếp thành hàng '
                'ngang.',
                'Hỏi có mấy hình đơn, tức là mấy mảnh nhỏ.']),
        _c('hinh_cn', 'Kẻ hình ra rồi nhìn cho kỹ', dai=6, rong=2, oVuong=True,
           chuPhu='Ba ô vuông nhỏ xếp thành hàng ngang.',
           loi=['Kẻ hình ra rồi nhìn cho kỹ. Ba ô vuông nhỏ xếp thành hàng ngang.']),
        _c('day_so', 'Đánh số từng mảnh — điểm danh', so=[1, 2, 3],
           chuPhu='Viết số 1, 2, 3 vào ba mảnh.',
           loi=['Đánh số từng mảnh. Viết số một, số hai, số ba vào ba mảnh.',
                'Đây là bước điểm danh, làm rồi thì không sót mảnh nào.']),
        _c('y_toan', 'Đếm hình đơn', 'mỗi mảnh là một hình  →  3 hình đơn',
           buoc=1, soBuoc=3,
           loi=['Mỗi mảnh nhỏ là một hình đơn. Có ba mảnh nên có ba hình đơn.']),
        _c('y_toan', 'Đáp số', '3 hình đơn', buoc=2, soBuoc=3,
           loi=['Đáp số là ba hình đơn.']),
        _c('y_toan', 'Nhưng mới xong một nửa việc',
           'trong hình còn hình TO ẩn mình', buoc=3, soBuoc=3,
           loi=['Nhưng đếm hình đơn mới xong một nửa việc.',
                'Trong hình còn hình to đang ẩn mình, bài sau sẽ lùng ra.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='ĐÁNH SỐ trước, ĐẾM sau',
           thay='có thứ tự thì không sót, không trùng',
           loi=['Con nhớ lại một lần nữa. Đánh số trước, đếm sau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hinh_ghep(b):
    """C7④ Đếm hình ghép."""
    return [
        _c('bia', 'Hình ghép ẩn mình', so_bai(b),
           loi=['Ghép mấy mảnh cạnh nhau lại cũng thành một hình. Đó là hình ghép.']),
        _c('de_toan', 'Đề bài',
           de='Băng 3 ô đánh số 1, 2, 3. Ghép được thêm mấy hình chữ nhật nữa?',
           loi=['Băng ba ô đánh số một, hai, ba.',
                'Hỏi ghép được thêm mấy hình chữ nhật nữa.']),
        _c('y_toan', 'Ghép HAI mảnh cạnh nhau trước',
           '(1 và 2)  ·  (2 và 3)  →  2 hình', buoc=1, soBuoc=3,
           loi=['Ghép hai mảnh cạnh nhau trước.',
                'Ghép mảnh một với mảnh hai được một hình. Ghép mảnh hai với mảnh ba '
                'được một hình nữa. Vậy hai hình.']),
        _c('y_toan', 'Rồi ghép BA mảnh', '(1 và 2 và 3)  →  1 hình to nhất',
           buoc=2, soBuoc=3,
           loi=['Rồi ghép cả ba mảnh, được hình to nhất ôm trọn cả hình. Thêm một '
                'hình.']),
        _c('y_toan', 'Cộng lại', '2 + 1 = 3 hình ghép', buoc=3, soBuoc=3,
           loi=['Cộng lại được ba hình ghép.']),
        _c('y_toan', 'Cả hình có mấy hình chữ nhật', '3 hình đơn + 3 hình ghép = 6',
           loi=['Cộng cả hình đơn lẫn hình ghép thì băng ba ô có sáu hình chữ nhật.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Đếm ba mảnh nhỏ rồi ghi luôn đáp số là 3.',
           loi=['Có bạn đếm được ba mảnh nhỏ rồi ghi luôn đáp số là ba.',
                'Còn ba hình ghép nữa chưa đếm.']),
        _c('cong_thuc', 'Đi tuần tự thì không sót',
           congThuc='ghép 2 mảnh  →  ghép 3 mảnh  →  ghép cả hình',
           thay='hình TO NHẤT luôn là hình hay ẩn mình nhất',
           loi=['Đi tuần tự: ghép hai mảnh, ghép ba mảnh, rồi ghép cả hình.',
                'Hình to nhất luôn là hình hay ẩn mình nhất.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_tam_nan_hoa(b):
    """C7⑤ Tâm và nan hoa bằng nhau."""
    return [
        _c('bia', 'Bí mật của hình tròn', so_bai(b),
           loi=['Hình tròn có một bí mật, và cả cái bánh xe đứng trên bí mật ấy.']),
        _c('hinh_tron', 'Cái rốn chính giữa gọi là TÂM', chuPhu='Từ tâm căng dây ra viền, ta được các nan hoa.',
           loi=['Hình tròn có một cái rốn chính giữa gọi là tâm.',
                'Từ tâm căng dây ra viền theo hướng nào cũng được, ta gọi đó là các '
                'nan hoa.']),
        _c('hinh_tron', 'Mọi nan hoa đều dài BẰNG NHAU', hienR=True, chuPhu='Đo hướng nào cũng ra cùng một độ dài.',
           loi=['Bí mật là mọi nan hoa đều dài bằng nhau.',
                'Đo thử vài nan hoa mà xem, hướng nào cũng ra cùng một độ dài.']),
        _c('y_toan', 'Đo nan hoa là biết tròn thật hay tròn giả',
           'nan hoa bằng nhau  →  hình tròn', buoc=1, soBuoc=3,
           loi=['Muốn biết tròn thật hay tròn giả thì cứ đo nan hoa.']),
        _c('y_toan', 'Quả trứng nhìn nghiêng thì sao',
           'viền cong nhưng nan hoa chỗ dài chỗ ngắn  →  hình MÉO',
           buoc=2, soBuoc=3,
           loi=['Quả trứng nhìn nghiêng cũng có viền cong.',
                'Nhưng nan hoa chỗ dài chỗ ngắn, nên nó là hình méo chứ không phải '
                'hình tròn.']),
        _c('y_toan', 'Đáp số',
           'mặt đồng hồ · chiếc đĩa · đồng xu  đều là hình tròn', buoc=3, soBuoc=3,
           loi=['Mặt đồng hồ, chiếc đĩa và đồng xu đều có dạng hình tròn.',
                'Quyển vở là hình chữ nhật, còn quả trứng nhìn nghiêng là hình méo.']),
        _c('cong_thuc', 'Cách kiểm tra',
           congThuc='đo NAN HOA xem có bằng nhau không',
           thay='viền cong thôi thì chưa đủ',
           loi=['Đo nan hoa xem có bằng nhau không. Viền cong thôi thì chưa đủ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_banh_xe(b):
    """C7⑥ Vì sao bánh xe phải tròn."""
    return [
        _c('bia', 'Vì sao bánh xe phải tròn', so_bai(b),
           loi=['Đây là chỗ hình học gặp cuộc sống thật.']),
        _c('hinh_tron', 'Trục xe đặt đúng ở TÂM', hienR=True, chuPhu='Trục nằm ở tâm, nan hoa chống xuống mặt đất.',
           loi=['Trục xe đặt đúng ở tâm bánh xe.']),
        _c('y_toan', 'Bánh tròn thì trục luôn cao đều một mức',
           'nan hoa nào cũng bằng nhau  →  trục cao đều', buoc=1, soBuoc=3,
           loi=['Vì mọi nan hoa dài bằng nhau, nên chỗ nào chạm đất thì trục cũng cao '
                'đúng bằng một nan hoa.',
                'Xe chạy êm ru.']),
        _c('hinh_cn', 'Còn bánh vuông thì sao', dai=5, rong=5, duongCheo=True,
           chuPhu='Nan hoa ra góc DÀI, ra giữa cạnh NGẮN.',
           loi=['Còn bánh vuông thì nan hoa ra góc dài, ra giữa cạnh ngắn.']),
        _c('y_toan', 'Trục lúc nhô lúc tụt', 'xe xóc suốt, không đi được',
           buoc=2, soBuoc=3,
           loi=['Nên trục xe lúc nhô lúc tụt. Xe xóc suốt, không đi được.']),
        _c('y_toan', 'Đáp số',
           'vì mọi nan hoa của hình tròn bằng nhau nên trục luôn cao đều',
           buoc=3, soBuoc=3,
           loi=['Bánh xe phải tròn vì mọi nan hoa của hình tròn bằng nhau, nên trục '
                'luôn cao đều.']),
        _c('y_toan', 'Tính chiều cao của trục', 'nan hoa 4  →  trục cao 4 xăng-ti-mét',
           loi=['Nan hoa dài bốn xăng ti mét thì trục cao cách mặt đất đúng bốn xăng '
                'ti mét.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='cả cái bánh xe đứng trên MỘT tính chất',
           thay='mọi nan hoa đều bằng nhau',
           loi=['Con nhớ lại một lần nữa. Cả cái bánh xe đứng trên một tính chất, là '
                'mọi nan hoa đều bằng nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hai_loai_khoi(b):
    """C7⑦ Hai loại khối, mỗi khối sáu mặt."""
    return [
        _c('bia', 'Hai loại khối', so_bai(b),
           loi=['Khối là thứ cầm nắm được, và khối nào cũng có sáu mặt.']),
        _c('khoi', 'Khối lập phương: vuông vức mọi phía', dai=3, rong=3, cao=3,
           kieu='chong', chuPhu='Mỗi mặt là một hình vuông giống hệt nhau.',
           loi=['Khối lập phương vuông vức mọi phía, như viên xúc xắc hay khối '
                'ru bích.',
                'Mỗi mặt của nó là một hình vuông giống hệt nhau.']),
        _c('khoi', 'Khối hộp chữ nhật: dài dài', dai=4, rong=2, cao=2,
           kieu='chong', chuPhu='Mỗi mặt là một hình chữ nhật.',
           loi=['Khối hộp chữ nhật thì dài dài, như hộp sữa hay viên gạch.',
                'Mỗi mặt của nó là một hình chữ nhật.']),
        _c('khoi', 'Trải phẳng ra thì thấy đủ SÁU mặt', dai=4, rong=2, cao=2,
           kieu='trai', chuPhu='Hai mặt cùng màu là hai mặt đối diện.',
           loi=['Trải phẳng ra thì thấy đủ sáu mặt. Hai mặt cùng màu là hai mặt đối '
                'diện.']),
        _c('y_toan', 'Đếm mặt kiểu sờ tay',
           'trên · dưới · trước · sau · trái · phải', buoc=1, soBuoc=3,
           loi=['Cầm hộp lên rồi sờ và đếm: mặt trên, mặt dưới, mặt trước, mặt sau, '
                'mặt trái, mặt phải.',
                'Đúng sáu mặt, khối nào cũng vậy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Quên mặt đang úp xuống bàn.', buoc=2, soBuoc=3,
           loi=['Có bạn đếm được bốn mặt rồi thôi, vì quên mặt trên và mặt đang úp '
                'xuống bàn.']),
        _c('y_toan', 'Đáp số',
           'xúc xắc và ru-bích là khối lập phương · hộp sữa và viên gạch là khối hộp chữ nhật',
           buoc=3, soBuoc=3,
           loi=['Xúc xắc và ru bích là khối lập phương. Hộp sữa và viên gạch là khối '
                'hộp chữ nhật.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='khối nào cũng có SÁU mặt',
           thay='chỉ khác nhau ở chỗ mặt ấy vuông hay chữ nhật',
           loi=['Con nhớ lại một lần nữa. Khối nào cũng có sáu mặt.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_hinh_va_khoi(b):
    """C7⑧ Hình dẹt và khối."""
    return [
        _c('bia', 'Hình dẹt và khối', so_bai(b),
           loi=['Hình vuông và khối lập phương là hai thứ khác nhau.']),
        _c('hinh_cn', 'HÌNH thì dẹt, nằm trên giấy', dai=5, rong=5,
           chuPhu='Mỏng dính, không cầm nắm được.',
           loi=['Hình vuông vẽ trên giấy, mỏng dính, không cầm nắm được.']),
        _c('khoi', 'KHỐI thì cầm nắm được', dai=3, rong=3, cao=3, kieu='chong',
           chuPhu='Có chỗ rỗng bên trong để giấu kẹo.',
           loi=['Khối lập phương cầm được trong tay, có chỗ rỗng bên trong để giấu '
                'kẹo.']),
        _c('y_toan', 'Hình chính là ẢNH CHỤP một mặt của khối',
           'chấm một mặt vào mực rồi in lên giấy', buoc=1, soBuoc=3,
           loi=['Hình chính là ảnh chụp một mặt của khối.',
                'Chấm một mặt của khối lập phương vào mực rồi in lên giấy, ta được một '
                'hình vuông.']),
        _c('y_toan', 'In một mặt khối hộp chữ nhật', 'được một hình chữ nhật',
           buoc=2, soBuoc=3,
           loi=['In một mặt của khối hộp chữ nhật thì được một hình chữ nhật.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Gọi viên xúc xắc là "hình vuông".',
           buoc=3, soBuoc=3,
           loi=['Có bạn gọi viên xúc xắc là hình vuông.',
                'Viên xúc xắc là khối lập phương. Hình vuông chỉ là ảnh chụp một mặt '
                'của nó.']),
        _c('cong_thuc', 'Cách phân biệt',
           congThuc='dẹt trên giấy  →  HÌNH',
           thay='cầm nắm được, có 6 mặt  →  KHỐI',
           loi=['Dẹt trên giấy thì gọi là hình. Cầm nắm được và có sáu mặt thì gọi là '
                'khối.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='hỏi: "in một mặt ra giấy thì được hình gì?"',
           loi=['Con nhớ lại một lần nữa. Hỏi rằng in một mặt của nó ra giấy thì được '
                'hình gì.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_luat_ngoi(b):
    """C7⑨ Luật ngồi."""
    return [
        _c('bia', 'Khối bị che vẫn phải đếm', so_bai(b),
           loi=['Đếm bằng mắt thì sót. Phải đếm bằng luật.']),
        _c('khoi', 'Một tòa tháp hai tầng', dai=2, rong=2, cao=2, kieu='chong',
           chuPhu='Có khối nấp phía sau mà mắt không thấy.',
           loi=['Nhìn tòa tháp này. Có khối nấp phía sau mà mắt không nhìn thấy.']),
        _c('y_toan', 'Khối không biết bay', 'khối tầng trên phải NGỒI trên một khối',
           buoc=1, soBuoc=3,
           loi=['Khối ở tầng trên không biết bay. Nó phải ngồi trên một khối tầng '
                'dưới.']),
        _c('y_toan', 'Nên thấy khối tầng hai là biết chắc bên dưới có khối',
           'dù khối ấy bị che gần hết', buoc=2, soBuoc=3,
           loi=['Nên hễ thấy khối ở tầng hai, mình biết chắc bên dưới nó có một khối '
                'đỡ.',
                'Dù khối ấy bị che gần hết.']),
        _c('khoi', 'Tách tầng ra thì thấy hết', dai=2, rong=2, cao=2, kieu='tang',
           chuPhu='Tách từng tầng ra là đếm được cả khối bị che.',
           loi=['Tách từng tầng ra thì thấy hết, đếm được cả khối bị che.']),
        _c('y_toan', 'Đáp số', 'có, bên dưới chắc chắn có một khối đỡ',
           buoc=3, soBuoc=3,
           loi=['Đáp số là có, bên dưới chắc chắn có một khối đỡ.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Chỉ đếm những khối mắt nhìn thấy.',
           loi=['Có bạn chỉ đếm những khối mắt nhìn thấy, nên tháp nào cũng đếm '
                'thiếu.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='khối bị che VẪN PHẢI ĐẾM',
           thay='nhìn thấy hay không không quyết định — luật ngồi mới quyết định',
           loi=['Con nhớ lại một lần nữa. Khối bị che vẫn phải đếm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_dem_tang(b):
    """C7⑩ Đếm theo tầng."""
    return [
        _c('bia', 'Đếm theo tầng', so_bai(b),
           loi=['Đừng đếm lung tung theo mắt nhìn. Đếm từng tầng như đếm nhà cao '
                'tầng.']),
        _c('de_toan', 'Đề bài',
           de='Tháp có tầng dưới xếp 2 hàng mỗi hàng 2 khối, tầng trên có 1 khối. Tháp có mấy khối?',
           loi=['Một tháp có tầng dưới xếp hai hàng, mỗi hàng hai khối. Tầng trên có '
                'một khối.',
                'Hỏi tháp có tất cả bao nhiêu khối.']),
        _c('khoi', 'Tháp trông thế này', dai=2, rong=2, cao=2, kieu='chong',
           loi=['Tháp trông thế này. Nhìn thôi thì khó đếm.']),
        _c('khoi', 'Tách từng tầng ra mà đếm', dai=2, rong=2, cao=2, kieu='tang',
           chuPhu='Tầng dưới 4 khối, tầng trên 1 khối.',
           loi=['Tách từng tầng ra mà đếm. Tầng dưới bốn khối, tầng trên một khối.']),
        _c('y_toan', 'Đếm tầng dưới, kể cả hàng nấp phía sau', '2 × 2 = 4 khối',
           buoc=1, soBuoc=3,
           loi=['Tầng dưới có hai hàng, mỗi hàng hai khối, nên bốn khối.',
                'Một khối ở góc sau bị che gần hết nhưng vẫn đếm.']),
        _c('y_toan', 'Cộng các tầng lại', '4 + 1 = 5 khối', buoc=2, soBuoc=3,
           loi=['Cộng các tầng lại. Bốn cộng một bằng năm khối.']),
        _c('y_toan', 'Kiểm tra lại', 'gỡ tháp ra từng khối một — gỡ đủ 5 lần',
           buoc=3, soBuoc=3,
           loi=['Kiểm tra bằng cách tưởng tượng gỡ tháp ra từng khối một. Gỡ đủ năm '
                'lần mới hết.']),
        _c('cong_thuc', 'Cách làm của cả bài',
           congThuc='đếm TỪNG TẦNG, kể cả hàng nấp phía sau',
           thay='rồi cộng các tầng lại',
           loi=['Đếm từng tầng, kể cả hàng nấp phía sau, rồi cộng các tầng lại.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 2 · CHƯƠNG 8 · TOÁN TRONG CUỘC SỐNG — sáu kịch bản, khép lại cả quyển.
# ═══════════════════════════════════════════════════════════════════════════


def kb2_mot_nua_hinh(b):
    """C8① Một nửa và một phần tư của một hình."""
    return [
        _c('bia', 'Một nửa và một phần tư', so_bai(b),
           loi=['Gấp một tờ giấy là hiểu ngay hai chữ ấy.']),
        _c('phan_so', 'Gấp ĐÔI: hai phần bằng nhau', tu=1, mau=2,
           nhan='mỗi phần là MỘT NỬA',
           loi=['Gấp đôi tờ giấy thật khít. Hai phần chồng khít lên nhau, tức là hai '
                'phần bằng nhau.',
                'Mỗi phần được gọi là một nửa.']),
        _c('phan_so', 'Gấp đôi thêm lần nữa: bốn phần bằng nhau', tu=1, mau=4,
           nhan='mỗi phần là MỘT PHẦN TƯ',
           loi=['Gấp đôi thêm lần nữa rồi mở ra. Tờ giấy chia thành bốn phần bằng '
                'chằn chặn.',
                'Mỗi phần được gọi là một phần tư.']),
        _c('y_toan', 'Luật sống còn: các phần phải BẰNG NHAU',
           'cắt lệch thì không miếng nào được gọi là một nửa', buoc=1, soBuoc=3,
           loi=['Luật sống còn là các phần phải bằng nhau.',
                'Cắt một miếng to một miếng nhỏ thì không miếng nào được gọi là một '
                'nửa cả.']),
        _c('phan_so', 'So hai miếng bánh', tu=1, mau=2, nhan='một nửa',
           tu2=1, mau2=4, nhan2='một phần tư',
           loi=['So hai miếng của cùng một cái bánh. Miếng một nửa to hơn miếng một '
                'phần tư.']),
        _c('y_toan', 'Chia càng nhiều phần thì mỗi phần càng bé',
           'cùng một cái bánh', buoc=2, soBuoc=3,
           loi=['Cùng một cái bánh, chia càng nhiều phần thì mỗi phần càng bé.']),
        _c('y_toan', 'Đáp số',
           'gấp đôi → một nửa   ·   gấp đôi hai lần → một phần tư',
           buoc=3, soBuoc=3,
           loi=['Gấp đôi được một nửa. Gấp đôi hai lần được một phần tư.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='các phần phải BẰNG NHAU mới được gọi tên',
           loi=['Con nhớ lại một lần nữa. Các phần phải bằng nhau mới được gọi tên '
                'như vậy.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_mot_nua_nhom(b):
    """C8② Một nửa của một nhóm."""
    return [
        _c('bia', 'Một nửa của một nhóm', so_bai(b),
           loi=['Không chỉ cái bánh mới chia được. Cả một nhóm đồ vật cũng vậy.']),
        _c('de_toan', 'Đề bài',
           de='Có 8 viên kẹo. Một nửa số kẹo là mấy viên, và một phần tư là mấy viên?',
           loi=['Có tám viên kẹo.',
                'Hỏi một nửa số kẹo là mấy viên, và một phần tư số kẹo là mấy viên.']),
        _c('nhom_deu', 'Một nửa: chia thành HAI phần bằng nhau', tong=8, moiNhom=4,
           chuPhu='8 chia 2 được 4 viên mỗi phần.',
           loi=['Một nửa thì chia thành hai phần bằng nhau.',
                'Tám chia hai được bốn viên mỗi phần.']),
        _c('y_toan', 'Phép tính', '8 : 2 = 4', buoc=1, soBuoc=3,
           loi=['Tám chia hai bằng bốn.']),
        _c('nhom_deu', 'Một phần tư: chia thành BỐN phần bằng nhau', tong=8, moiNhom=2,
           chuPhu='8 chia 4 được 2 viên mỗi phần.',
           loi=['Một phần tư thì chia thành bốn phần bằng nhau.',
                'Tám chia bốn được hai viên mỗi phần.']),
        _c('y_toan', 'Phép tính', '8 : 4 = 2', buoc=2, soBuoc=3,
           loi=['Tám chia bốn bằng hai.']),
        _c('y_toan', 'Đáp số', 'một nửa là 4 viên  ·  một phần tư là 2 viên',
           buoc=3, soBuoc=3,
           loi=['Một nửa là bốn viên. Một phần tư là hai viên.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='nghe "một nửa"  →  CHIA 2',
           thay='nghe "một phần tư"  →  CHIA 4',
           loi=['Con nhớ lại một lần nữa. Nghe một nửa thì chia hai, nghe một phần tư '
                'thì chia bốn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_von_lai(b):
    """C8③ Vốn, bán, lãi."""
    return [
        _c('bia', 'Sổ của ông chủ', so_bai(b),
           loi=['Sổ của ông chủ chỉ có ba dòng: vốn, bán, và lãi.']),
        _c('de_toan', 'Đề bài',
           de='Mua chanh và đường hết 10 nghìn, bán được 4 cốc mỗi cốc 4 nghìn. Lãi bao nhiêu?',
           loi=['Mua chanh và đường hết mười nghìn đồng, bán được bốn cốc, mỗi cốc bốn '
                'nghìn.',
                'Hỏi lãi bao nhiêu.']),
        _c('y_toan', 'Tiền VỐN là tiền bỏ ra trước', '6 + 4 = 10 nghìn',
           buoc=1, soBuoc=3,
           loi=['Tiền vốn là tiền bỏ ra trước khi bán được đồng nào.',
                'Sáu cộng bốn bằng mười nghìn.']),
        _c('y_toan', 'Tiền BÁN là tiền thu về', '4 × 4 = 16 nghìn', buoc=2, soBuoc=3,
           loi=['Tiền bán là tiền thu về. Bốn cốc, mỗi cốc bốn nghìn, nên bốn nhân bốn '
                'bằng mười sáu nghìn.']),
        _c('y_toan', 'Tiền LÃI là phần thật sự kiếm thêm', '16 − 10 = 6 nghìn',
           buoc=3, soBuoc=3,
           loi=['Tiền lãi là phần thật sự kiếm thêm. Mười sáu trừ mười bằng sáu '
                'nghìn.']),
        _c('y_toan', 'Đáp số', 'lãi 6 nghìn đồng',
           loi=['Đáp số là lãi sáu nghìn đồng.',
                'Giàu thêm sáu nghìn chứ không phải mười sáu nghìn, vì mười nghìn vốn '
                'vốn dĩ đã là của mình từ đầu.']),
        _c('y_toan', 'Còn nếu ế hàng', 'bán 8 nghìn mà vốn 10  →  LỖ 10 − 8 = 2 nghìn',
           loi=['Nếu cả ngày chỉ bán được hai cốc thì thu về tám nghìn.',
                'Mà tiền bỏ ra là mười nghìn, nên bị lỗ hai nghìn.']),
        _c('cong_thuc', 'Sổ ông chủ chỉ có ba dòng',
           congThuc='VỐN bỏ ra  →  BÁN thu về',
           thay='LÃI = BÁN − VỐN   ·   bán ít hơn vốn là LỖ',
           loi=['Vốn là tiền bỏ ra, bán là tiền thu về, còn lãi bằng bán trừ vốn.',
                'Bán ít hơn vốn thì bị lỗ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_tien_thua(b):
    """C8④ Tiền thừa."""
    return [
        _c('bia', 'Tiền thối lại', so_bai(b),
           loi=['Bài trước đứng ở phía người bán. Bài này đứng ở phía người mua.']),
        _c('de_toan', 'Đề bài',
           de='Một cô khách đưa 10 nghìn để mua món hàng giá 7 nghìn. Phải thối lại bao nhiêu?',
           loi=['Một cô khách đưa mười nghìn để mua món hàng giá bảy nghìn.',
                'Hỏi phải thối lại bao nhiêu.']),
        _c('y_toan', 'Người mua đưa tiền ra', 'người bán thối lại phần dư',
           buoc=1, soBuoc=3,
           loi=['Người mua đưa tiền ra, người bán thối lại phần dư.']),
        _c('y_toan', 'Tiền thừa bằng tiền đưa trừ tiền mua', '10 − 7 = 3 nghìn',
           buoc=2, soBuoc=3,
           loi=['Tiền thừa bằng tiền đưa trừ tiền mua. Mười trừ bảy bằng ba nghìn.']),
        _c('y_toan', 'Đáp số', 'thối lại 3 nghìn đồng', buoc=3, soBuoc=3,
           loi=['Đáp số là thối lại ba nghìn đồng.']),
        _c('y_toan', 'Có đủ tiền mua không', 'có 5 nghìn mà món hàng 8 nghìn → chưa đủ',
           loi=['Muốn biết có đủ tiền mua không thì so tiền mình có với giá món hàng.',
                'Có năm nghìn mà món hàng tám nghìn thì chưa mua được, còn thiếu ba '
                'nghìn.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Cộng tiền đưa với giá món hàng.',
           loi=['Có bạn cộng tiền đưa với giá món hàng để tính tiền thối.',
                'Cộng thì tiền thối lại nhiều hơn tiền đưa, nghe đã thấy vô lý.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='THỪA = ĐƯA − MUA',
           loi=['Con nhớ lại một lần nữa. Tiền thừa bằng tiền đưa trừ tiền mua.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_gio_dung(b):
    """C8⑤ Giờ đúng."""
    return [
        _c('bia', 'Giờ đúng', so_bai(b),
           loi=['Hai chiếc kim trên mặt đồng hồ, mỗi chiếc kể một chuyện.']),
        _c('dong_ho', 'Làm quen hai chiếc kim', gio=3, phut=12,
           chuPhu='Kim ngắn và mập là kim giờ. Kim dài là kim phút.',
           loi=['Kim ngắn và mập là kim giờ. Kim dài là kim phút.',
                'Kim giờ đi chậm rãi, kim phút chạy nhanh hơn nhiều.']),
        _c('y_toan', 'Nhìn kim PHÚT trước', 'chỉ thẳng số 12  →  giờ đúng',
           buoc=1, soBuoc=3,
           loi=['Nhìn kim phút trước. Kim phút chỉ thẳng số mười hai nghĩa là giờ '
                'đúng, không lẻ phút nào.']),
        _c('y_toan', 'Rồi mới hỏi kim GIỜ', 'kim giờ chỉ 3  →  đọc "3 giờ"',
           buoc=2, soBuoc=3,
           loi=['Rồi mới hỏi kim giờ. Kim giờ chỉ số ba nên đọc là ba giờ đúng.']),
        _c('y_toan', 'Đáp số', '3 giờ', buoc=3, soBuoc=3,
           loi=['Đáp số là ba giờ.']),
        _c('dong_ho', 'Một giờ nữa thì kim giờ tiến thêm một số', gio=4, phut=12,
           chuPhu='Từ 3 giờ, một giờ nữa là 4 giờ.',
           loi=['Một giờ nữa thì kim giờ tiến thêm đúng một số.',
                'Từ ba giờ, một giờ nữa là bốn giờ.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Nhìn nhầm kim dài thành kim giờ.',
           loi=['Có bạn nhìn nhầm kim dài thành kim giờ nên đọc sai hẳn.',
                'Kim giờ là kim ngắn và mập.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='nhìn kim PHÚT trước, rồi mới hỏi kim GIỜ',
           loi=['Con nhớ lại một lần nữa. Nhìn kim phút trước, rồi mới hỏi kim giờ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb2_gio_ruoi(b):
    """C8⑥ Giờ rưỡi — bài cuối cùng của quyển."""
    return [
        _c('bia', 'Giờ rưỡi', so_bai(b),
           loi=['Khi kim phút chỉ số sáu thì đọc thế nào?']),
        _c('dong_ho', 'Kim phút chỉ số 6 — đi được NỬA vòng', gio=3, phut=6,
           chuPhu='Nửa vòng là nửa giờ, nên đây là giờ rưỡi.',
           loi=['Kim phút chỉ số sáu nghĩa là nó đi được một nửa vòng.',
                'Nửa vòng là nửa giờ, nên đây là giờ rưỡi.']),
        _c('y_toan', 'Kim giờ cũng đi được nửa đường',
           'nó nằm giữa số 3 và số 4, chưa tới số 4', buoc=1, soBuoc=3,
           loi=['Kim giờ cũng đi được nửa đường giữa hai số.',
                'Nó nằm giữa số ba và số bốn, chưa tới số bốn.']),
        _c('y_toan', 'Luật đọc: theo số kim giờ ĐÃ ĐI QUA', 'đã đi qua số 3  →  3 giờ rưỡi',
           buoc=2, soBuoc=3,
           loi=['Luật đọc là đọc theo số mà kim giờ đã đi qua.',
                'Nó đã đi qua số ba, nên đọc là ba giờ rưỡi, chứ không phải bốn giờ '
                'rưỡi.']),
        _c('y_toan', 'Đáp số', '3 giờ rưỡi', buoc=3, soBuoc=3,
           loi=['Đáp số là ba giờ rưỡi.']),
        _c('dong_ho', 'Thêm nửa giờ nữa thì tròn 4 giờ', gio=4, phut=12,
           chuPhu='Hai nửa giờ ghép lại thành một giờ.',
           loi=['Từ ba giờ rưỡi thêm nửa giờ nữa thì tròn bốn giờ.',
                'Hai nửa giờ ghép lại thành một giờ.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Đọc theo số kim giờ SẮP TỚI.',
           loi=['Có bạn thấy kim giờ nằm giữa ba và bốn rồi đọc là bốn giờ rưỡi, vì nó '
                'gần số bốn.',
                'Nó mới mon men tới gần số bốn chứ đã tới đâu.']),
        _c('cong_thuc', 'Con nhớ kỹ chỗ này nhé',
           congThuc='kim phút chỉ 6  →  giờ RƯỠI',
           thay='đọc theo số kim giờ ĐÃ ĐI QUA',
           loi=['Con nhớ lại một lần nữa. Kim phút chỉ sáu là giờ rưỡi, và đọc theo số '
                'kim giờ đã đi qua.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 1 · Hàng nghìn và các chữ số — bốn bài
# ═══════════════════════════════════════════════════════════════════════════
# Quyển lớp 3 là quyển cuối chuyển sang video. Bốn bài này đều xoay quanh MỘT thứ:
# chữ số đứng ở đâu thì đáng bấy nhiêu. Nhưng mỗi video chỉ được nói MỘT việc, nên
# chia thế này:
#   B01 tháp thứ tư (nghìn) và giá trị theo chỗ đứng
#   B02 thêm chữ số bên trái khác hẳn bên phải
#   B03 có điều kiện chẵn lẻ thì ĐUÔI đặt trước
#   B04 đếm ngược: biết số chữ số, tìm số trang
#
# `bang_hang` vẽ được bốn ô và tự đóng khung "lớp nghìn · lớp đơn vị" — đúng thứ
# chương này cần, không phải vẽ thêm kiểu cảnh mới nào.


def kb3_thap_nghin(b):
    """L3·C1① Tòa tháp thứ tư mang tên nghìn."""
    return [
        _c('bia', 'Tòa tháp thứ tư', so_bai(b),
           loi=['Năm ngoái con học ba tháp. Nay có thêm một tháp nữa.']),
        _c('y_toan', 'Luật cũ leo thêm một tầng',
           '10 trăm gom lại thành 1 nghìn', buoc=1, soBuoc=3,
           loi=['Mười đơn vị gom thành một chục. Mười chục gom thành một trăm.',
                'Nay thêm một nấc nữa. Mười trăm gom lại thành một nghìn.']),
        # `hienLop=False`: quyển lớp 3 dạy THÁP THỨ TƯ, chưa dạy khái niệm "lớp"
        # (lớp nghìn · lớp đơn vị) — đó là chuyện của lớp 4. Bày thêm một khung có
        # tên lạ ở đây là thêm một thứ phải hiểu mà bài không dùng tới.
        _c('bang_hang', 'Số 2 435 ở trong bốn tháp', so='2435', hienLop=False,
           chuPhu='Đọc từ tháp cao nhất xuống thấp dần.',
           loi=['Số hai nghìn bốn trăm ba mươi lăm dọn vào bốn tháp.',
                'Con đọc từ tháp cao nhất xuống dần thì ra đúng tên của nó.']),
        _c('bang_hang', 'Chữ số 2 đứng ở tháp nghìn', so='2435', hienLop=False,
           toSang=[3],
           chuPhu='Nên nó đáng 2 nghìn, chứ không phải 2.',
           loi=['Chữ số hai đứng ở tháp nghìn, nên nó đáng hai nghìn.',
                'Cùng một chữ số ấy mà đứng ở tháp đơn vị thì chỉ đáng hai thôi.']),
        _c('tach_so', 'Tách số theo từng tháp', so='2435',
           phep='2 435 = 2 000 + 400 + 30 + 5',
           chuPhu='Mỗi chữ số góp đúng phần của tháp nó đứng.',
           loi=['Tách ra thì thấy rõ. Hai nghìn, cộng bốn trăm, cộng ba mươi, cộng '
                'năm.',
                'Mỗi chữ số góp đúng phần của cái tháp nó đang đứng.']),
        _c('y_toan', 'Tháp trống thì ai giữ chỗ?',
           'Chữ số 0 đứng canh cho tháp khỏi mất chỗ.', buoc=2, soBuoc=3,
           loi=['Có khi một tháp trống không. Lúc ấy chữ số không đứng canh chỗ.']),
        _c('bang_hang', 'Ba nghìn không trăm bảy mươi hai', so='3072',
           hienLop=False, toSang=[2],
           chuPhu='Bỏ chữ số 0 đi thì còn 372 — sai hẳn số.',
           loi=['Số ba nghìn không trăm bảy mươi hai viết ra là ba, không, bảy, hai.',
                'Bỏ chữ số không đi thì còn ba trăm bảy mươi hai. Sai hẳn thành số '
                'khác.']),
        _c('y_toan', 'Thử lại', 'Cộng bốn phần vừa tách — phải ra đúng số cũ.',
           buoc=3, soBuoc=3,
           loi=['Con thử lại được. Cộng bốn phần vừa tách thì phải ra đúng số ban '
                'đầu.']),
        _c('cong_thuc', 'Muốn biết một chữ số đáng bao nhiêu',
           congThuc='nhìn CHỖ NÓ ĐỨNG, đừng nhìn mặt nó',
           thay='vì mỗi tháp có một sức nặng riêng',
           loi=['Con nhớ chỗ này. Muốn biết một chữ số đáng bao nhiêu thì nhìn chỗ nó '
                'đứng.',
                'Đừng nhìn mặt chữ số, vì mỗi tháp có một sức nặng riêng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_hai_cua(b):
    """L3·C1② Thêm chữ số bên trái khác hẳn bên phải."""
    return [
        _c('bia', 'Thêm bên trái, thêm bên phải', so_bai(b),
           loi=['Thêm một chữ số vào số cũ. Thêm bên nào thì khác nhau hẳn.']),
        _c('bang_hang', 'Số cũ là 45', so='45', hienLop=False,
           chuPhu='Chữ số 4 ở tháp chục, chữ số 5 ở tháp đơn vị.',
           loi=['Số cũ là bốn mươi lăm. Chữ số bốn ở tháp chục, chữ số năm ở tháp đơn '
                'vị.']),
        _c('bang_hang', 'Thêm 0 vào BÊN PHẢI', so='450', hienLop=False,
           toSang=[1, 2], chuPhu='Cả hai chữ số cũ bị đẩy lên một tháp.',
           loi=['Thêm chữ số không vào bên phải. Cả hai chữ số cũ bị đẩy lên một tháp.',
                'Bốn lên tháp trăm, năm lên tháp chục. Số cũ to gấp mười lần.']),
        _c('y_toan', 'Bên phải là CẢ NHÀ CHUYỂN TẦNG',
           'Số cũ × 10, rồi cộng chữ số mới', buoc=1, soBuoc=2,
           loi=['Thêm bên phải thì cả nhà chuyển tầng. Lấy số cũ nhân mười, rồi cộng '
                'chữ số mới vào.']),
        _c('bang_hang', 'Thêm 3 vào BÊN TRÁI', so='345', hienLop=False,
           toSang=[2], chuPhu='Chữ số 4 và 5 KHÔNG hề nhúc nhích.',
           loi=['Nay thêm chữ số ba vào bên trái. Con nhìn kỹ hai chữ số cũ.',
                'Bốn vẫn ở tháp chục, năm vẫn ở tháp đơn vị. Không ai nhúc nhích cả.',
                'Chỉ có chữ số ba dọn vào cái tháp còn trống ở bên trái.']),
        _c('tach_so', 'Nên số mới chỉ hơn số cũ đúng một phần', so='345',
           phep='345 = 300 + 45', sang=[1],
           chuPhu='Phần thêm chính là 3 trăm — giá trị chỗ nó vừa dọn vào.',
           loi=['Nên số mới bằng số cũ cộng thêm ba trăm.',
                'Ba trăm chính là giá trị của cái tháp mà chữ số ba vừa dọn vào.']),
        _c('y_toan', 'Bên trái là HÀNG XÓM MỚI DỌN ĐẾN',
           'Số cũ đứng yên, chỉ CỘNG thêm', buoc=2, soBuoc=2,
           loi=['Thêm bên trái thì số cũ đứng yên, chỉ cộng thêm phần của người mới.']),
        _c('cong_thuc', 'Hai cửa, hai luật khác hẳn',
           congThuc='phải  →  NHÂN     ·     trái  →  CỘNG',
           thay='vì chỉ cửa phải mới đẩy các chữ số cũ đi',
           loi=['Con nhớ hai cửa này. Thêm bên phải thì nhân, thêm bên trái thì cộng.',
                'Vì chỉ có cửa bên phải mới đẩy các chữ số cũ sang chỗ khác.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_duoi_dat_ve(b):
    """L3·C1③ Có điều kiện chẵn lẻ thì đuôi đặt vé trước."""
    return [
        _c('bia', 'Xếp thẻ khi có thêm điều kiện', so_bai(b),
           loi=['Xếp ba thẻ số, nhưng lần này có thêm một điều kiện.']),
        _c('y_toan', 'Luật cũ con đã biết',
           'Muốn số lớn nhất: xếp thẻ TO trước', buoc=1, soBuoc=3,
           loi=['Luật cũ con đã biết. Muốn được số lớn nhất thì xếp thẻ to lên trước.']),
        _c('tach_so', 'Từ ba thẻ 3, 8, 5 — số lớn nhất là 853', so='853', sang=[3],
           chuPhu='Nhưng đuôi là 3, nên nó LẺ.',
           loi=['Từ ba thẻ ba, tám, năm thì số lớn nhất là tám trăm năm mươi ba.',
                'Nhưng đề đòi số chẵn. Mà đuôi của nó là ba, nên nó lẻ.']),
        _c('y_toan', 'Chẵn hay lẻ do ĐUÔI quyết định',
           'Nên phải chọn đuôi TRƯỚC, xếp phần đầu SAU', buoc=2, soBuoc=3,
           loi=['Một số chẵn hay lẻ là do cái đuôi quyết định.',
                'Nên khi đề đòi chẵn, con phải chọn đuôi trước đã, rồi mới xếp phần '
                'đầu.']),
        _c('tach_so', 'Trong ba thẻ chỉ có 8 là chẵn', so='8', sang=[1],
           chuPhu='Vậy đuôi bắt buộc là 8 — không còn lựa chọn nào khác.',
           loi=['Trong ba thẻ chỉ có thẻ tám là chẵn.',
                'Vậy đuôi bắt buộc phải là tám. Không còn lựa chọn nào khác.']),
        _c('tach_so', 'Hai thẻ còn lại xếp to trước', so='538', sang=[3],
           phep='5 trước, 3 sau, đuôi giữ chỗ cho 8',
           chuPhu='Được số chẵn lớn nhất: 538.',
           loi=['Hai thẻ còn lại là năm và ba, xếp to trước bé sau.',
                'Được số năm trăm ba mươi tám. Đây là số chẵn lớn nhất lập được.']),
        _c('y_toan', 'Thử lại', 'Mọi cách xếp khác có đuôi 8 đều bé hơn.',
           buoc=3, soBuoc=3,
           loi=['Con thử lại. Mọi cách xếp khác mà đuôi vẫn là tám thì đều bé hơn.']),
        # ⚠ Màn NGAY TRƯỚC `ket` bắt buộc là `cong_thuc` — luật của `soi()`, bác chốt
        # 14-08: đã dạy xong thì phải nhắc lại công thức lần cuối rồi mới chào.
        _c('cong_thuc', 'Khi đề đòi chẵn hay lẻ',
           congThuc='ĐUÔI chọn trước  ·  phần đầu xếp sau',
           thay='vì đuôi quyết định chẵn lẻ, còn phần đầu quyết định to nhỏ',
           loi=['Con nhớ chỗ này. Đuôi chọn trước, phần đầu xếp sau.',
                'Vì đuôi quyết định chẵn lẻ, còn phần đầu mới quyết định số to hay '
                'nhỏ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_dem_nguoc_trang(b):
    """L3·C1④ Biết số chữ số, tìm số trang."""
    return [
        _c('bia', 'Đánh số trang — và đi ngược lại', so_bai(b),
           loi=['Đánh số trang một cuốn sách tốn bao nhiêu chữ số.']),
        _c('y_toan', 'Trang 1 đến 9 — mỗi trang MỘT chữ số',
           'Chín trang ấy tốn 9 chữ số', buoc=1, soBuoc=3,
           loi=['Từ trang một đến trang chín, mỗi trang chỉ có một chữ số.',
                'Chín trang ấy tốn chín chữ số.']),
        _c('y_toan', 'Từ trang 10 trở đi — mỗi trang HAI chữ số',
           'Nên số chữ số tăng gấp đôi theo trang', buoc=2, soBuoc=3,
           loi=['Từ trang mười trở đi, mỗi trang có hai chữ số.',
                'Nên từ đó mỗi trang tốn gấp đôi.']),
        _c('de_toan', 'Dùng hết đúng 45 chữ số. Sách dày mấy trang?',
           chuPhu='Lần này biết số chữ số, phải tìm ngược ra số trang.',
           loi=['Nay đề cho ngược lại. Dùng hết đúng bốn mươi lăm chữ số, hỏi sách dày '
                'mấy trang.']),
        _c('tach_so', 'Trả phần của chín trang đầu trước', so='45',
           phep='45 − 9 = 36', chuPhu='Còn 36 chữ số cho các trang hai chữ số.',
           loi=['Chín trang đầu đã ngốn chín chữ số. Trả phần ấy ra trước.',
                'Bốn mươi lăm trừ chín còn ba mươi sáu chữ số.']),
        _c('tach_so', 'Mỗi trang hai chữ số nên chia đôi', so='36',
           phep='36 : 2 = 18', chuPhu='Có 18 trang loại hai chữ số.',
           loi=['Mỗi trang loại này tốn hai chữ số, nên lấy ba mươi sáu chia hai.',
                'Được mười tám trang.']),
        _c('y_toan', 'Cộng hai phần lại', '9 + 18 = 27 trang', buoc=3, soBuoc=3,
           loi=['Cộng hai phần lại. Chín trang đầu cộng mười tám trang sau, được hai '
                'mươi bảy trang.']),
        _c('y_toan', 'Thử lại cho chắc', '9 + 18 × 2 = 45 chữ số — đúng đề.',
           loi=['Con thử lại cho chắc. Chín cộng mười tám nhân hai bằng bốn mươi lăm '
                'chữ số, đúng như đề cho.']),
        _c('cong_thuc', 'Đếm ngược thì TRẢ NỢ từng nhóm',
           congThuc='trừ phần nhóm 1 chữ số  →  phần còn lại chia 2',
           thay='vì mỗi nhóm trang tốn số chữ số khác nhau',
           loi=['Con nhớ cách đi ngược. Trừ phần của nhóm một chữ số ra trước, phần còn '
                'lại mới chia đôi.',
                'Vì mỗi nhóm trang tốn số chữ số khác nhau, không gộp chung được.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 2 · Nhân chia ra ngoài bảng — năm bài
# ═══════════════════════════════════════════════════════════════════════════
# Năm bài này là chỗ bé rời khỏi bảng cửu chương và bắt đầu tính với số to. Mỗi
# video một việc:
#   B05 nhân số to bằng cách TÁCH theo hàng
#   B06 chia có dư: bốn cái tên, và vì sao dư phải bé hơn số chia
#   B07 các số chia a dư b xếp thành một dãy đếm thêm a
#   B08 chữ LẦN là còi hiệu của nhân chia
#   B09 tìm một phần mấy là chia, và chiều ngược lại là nhân
#
# `nhom_deu` vẽ được cả phần DƯ (viên lẻ đứng riêng, tô đỏ) — đó đúng là thứ B06
# cần, và cũng là lý do bé thấy được vì sao dư không bao giờ bằng số chia.


def kb3_nhan_ngoai_bang(b):
    """L3·C2① Nhân số to bằng cách tách theo hàng."""
    return [
        _c('bia', 'Nhân số to bằng cách tách', so_bai(b),
           loi=['Số to quá không có trong bảng nhân. Con tách nó ra.']),
        _c('de_toan', 'Đề bài', de='Tính 23 × 4',
           loi=['Tính hai mươi ba nhân bốn. Bảng nhân không có dòng nào như thế.']),
        _c('tach_so', 'Tách 23 thành hai phần', so='23', sang=[1],
           phep='23 = 20 + 3', chuPhu='Hai chục để riêng, ba đơn vị để riêng.',
           loi=['Con tách hai mươi ba thành hai chục và ba đơn vị.']),
        _c('y_toan', 'Nhân từng phần một', '20 × 4 = 80  ·  3 × 4 = 12',
           buoc=1, soBuoc=2,
           loi=['Nhân từng phần một. Hai chục nhân bốn được tám chục.',
                'Ba nhân bốn được mười hai.']),
        _c('y_toan', 'Rồi gộp hai phần lại', '80 + 12 = 92', buoc=2, soBuoc=2,
           loi=['Rồi gộp hai phần lại. Tám mươi cộng mười hai bằng chín mươi hai.']),
        _c('cong_thuc', 'Vì sao tách được?',
           congThuc='4 lần của (20 + 3) = 4 lần 20, rồi 4 lần 3',
           thay='lấy bốn lần cả cụm cũng bằng lấy bốn lần từng phần',
           loi=['Vì sao tách được. Lấy bốn lần cả cụm cũng bằng lấy bốn lần từng '
                'phần rồi cộng lại.']),
        _c('y_toan', 'Ướm trước một con số cho chắc',
           '23 gần 20, mà 20 × 4 = 80 — đáp số phải quanh 80', buoc=1, soBuoc=1,
           loi=['Trước khi tính, con ướm thử. Hai mươi ba gần hai mươi, mà hai mươi '
                'nhân bốn là tám mươi.',
                'Vậy đáp số phải quanh tám mươi. Ra tám trăm mười hai là con biết '
                'mình vừa sai chỗ nào đó.']),
        _c('cong_thuc', 'Nhân số to',
           congThuc='TÁCH theo hàng  →  nhân từng phần  →  GỘP',
           thay='vì mỗi hàng có sức nặng riêng, tách ra mới nhân được bằng bảng',
           loi=['Con nhớ ba nhịp. Tách theo hàng, nhân từng phần, rồi gộp lại.',
                'Tách ra thì mỗi phần đều nằm trong bảng nhân con đã thuộc.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_chia_co_du(b):
    """L3·C2② Phép chia có dư và luật dư bé hơn số chia."""
    return [
        _c('bia', 'Chia mà còn thừa', so_bai(b),
           loi=['Chia xong mà vẫn còn thừa. Chỗ thừa ấy cũng có tên riêng.']),
        _c('de_toan', 'Đề bài', de='Chia 17 viên bi vào các hộp, mỗi hộp 3 viên',
           loi=['Chia mười bảy viên bi vào các hộp, mỗi hộp ba viên.']),
        _c('nhom_deu', 'Xếp thử: mỗi hộp 3 viên', tong=17, moiNhom=3,
           chuPhu='Được 5 hộp đầy, và còn 2 viên lẻ.',
           loi=['Xếp thử. Mỗi hộp ba viên thì được năm hộp đầy.',
                'Còn hai viên lẻ không đủ thành một hộp nữa.']),
        _c('y_toan', 'Viết cho chính danh', '17 : 3 = 5 (dư 2)', buoc=1, soBuoc=3,
           loi=['Viết cho chính danh. Mười bảy chia ba bằng năm, dư hai.']),
        _c('cong_thuc', 'Bốn cái tên phải gọi đúng',
           congThuc='17 bị chia  ·  3 số chia  ·  5 thương  ·  2 số dư',
           thay='gọi sai tên thì đọc đề sai, không phải chuyện hình thức',
           loi=['Bốn cái tên. Mười bảy là số bị chia, ba là số chia.',
                'Năm là thương, và hai là số dư.']),
        _c('nhom_deu', 'Vì sao dư luôn BÉ HƠN số chia?', tong=17, moiNhom=3,
           chuPhu='Nếu còn thừa 3 viên thì đã xếp thêm được một hộp nữa rồi.',
           loi=['Con nhìn chỗ thừa. Nếu còn thừa đủ ba viên thì đã xếp thêm được '
                'một hộp nữa.',
                'Nên phép chia chưa xong việc. Vì thế số dư luôn phải bé hơn số '
                'chia.']),
        _c('y_toan', 'Thử lại bằng phép nhân', '5 × 3 + 2 = 17', buoc=3, soBuoc=3,
           loi=['Thử lại. Năm hộp, mỗi hộp ba viên, cộng hai viên lẻ, bằng mười bảy '
                'viên ban đầu.']),
        _c('cong_thuc', 'Ba nhịp của phép chia có dư',
           congThuc='tìm bến gần nhất  ·  viết thương và dư  ·  soi dư < số chia',
           thay='vì bến vượt quá là chia lố, còn dư to là chia chưa xong',
           loi=['Con nhớ ba nhịp. Tìm bến gần nhất mà không vượt quá, viết thương và '
                'dư, rồi soi xem dư đã bé hơn số chia chưa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_doan_tau_du(b):
    """L3·C2③ Các số chia a dư b xếp thành một dãy đếm thêm a."""
    return [
        _c('bia', 'Tìm những số chia còn dư', so_bai(b),
           loi=['Tìm tất cả những số chia cho một số mà còn dư đúng bằng ấy.']),
        _c('de_toan', 'Đề bài', de='Tìm các số chia 4 dư 1, từ 10 đến 25',
           loi=['Tìm các số chia bốn dư một, nằm trong khoảng từ mười đến hai mươi '
                'lăm.']),
        _c('y_toan', 'Cách chậm: thử từng số một',
           'Số nào cũng đem chia 4 rồi xem dư mấy', buoc=1, soBuoc=3,
           loi=['Cách chậm là thử từng số một. Số nào cũng đem chia bốn rồi xem dư '
                'mấy.',
                'Làm được, nhưng lâu và dễ sót.']),
        _c('day_so', 'Cách nhanh: chúng xếp thành một dãy',
           so=[1, 5, 9, 13, 17, 21, 25], hienThuTu=False,
           chuPhu='Ga đầu là 1, và cứ đếm thêm 4.',
           loi=['Cách nhanh hơn. Những số ấy xếp thành một dãy rất trật tự.',
                'Bắt đầu từ một, rồi cứ đếm thêm bốn.']),
        _c('y_toan', 'Vì sao lại đều đặn như thế?',
           'Cộng thêm đúng 4 thì phần dư không đổi', buoc=2, soBuoc=3,
           loi=['Vì sao lại đều đặn như thế. Cộng thêm đúng bốn là thêm tròn một '
                'nhóm.',
                'Thêm tròn một nhóm thì phần dư không đổi chút nào.']),
        _c('day_so', 'Lấy phần nằm trong khoảng đề cho',
           so=[13, 17, 21, 25], hienThuTu=False,
           chuPhu='Từ 10 đến 25 thì dãy dừng ở 4 ga này.',
           loi=['Lấy phần nằm trong khoảng đề cho. Từ mười đến hai mươi lăm thì dãy '
                'dừng ở bốn số.']),
        _c('y_toan', 'Thử một số cho chắc', '21 : 4 = 5 (dư 1)', buoc=3, soBuoc=3,
           loi=['Thử một số cho chắc. Hai mươi mốt chia bốn bằng năm, dư một.']),
        _c('cong_thuc', 'Muốn CHẾ một số chia a dư b',
           congThuc='số = a × thương + b',
           thay='đây chính là phép thử lại, dùng ngược chiều',
           loi=['Muốn tự chế ra một số như thế thì lấy số chia nhân với thương, rồi '
                'cộng phần dư.',
                'Đây chính là phép thử lại, nay dùng ngược chiều.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_chu_lan(b):
    """L3·C2④ Chữ LẦN là còi hiệu của nhân chia."""
    return [
        _c('bia', 'Một chữ đổi cả phép tính', so_bai(b),
           loi=['Chỉ một chữ trong đề mà đổi hẳn phép tính con phải làm.']),
        _c('so_do_doan', 'Gấp 3 lần: xếp NGUYÊN KHỐI ra ba lần', be=5, lon=15,
           nhanBe='số cũ', nhanLon='gấp 3 lần',
           chuPhu='5 gấp 3 lần là 5 × 3 = 15.',
           loi=['Gấp ba lần nghĩa là xếp nguyên khối ấy ra ba lần.',
                'Năm gấp ba lần là năm nhân ba, bằng mười lăm.']),
        _c('so_do_doan', 'Thêm 3: chỉ bỏ thêm 3 vào', be=5, lon=8,
           nhanBe='số cũ', nhanLon='thêm 3', hienHieu=True, chuHieu='thêm 3',
           chuPhu='5 thêm 3 chỉ là 5 + 3 = 8.',
           loi=['Còn thêm ba thì chỉ bỏ thêm ba vào. Năm thêm ba là tám.',
                'Mười lăm với tám, khác nhau xa lắm.']),
        _c('y_toan', 'Chữ LẦN là còi hiệu', 'Có LẦN → nhân chia. Không LẦN → cộng trừ.',
           buoc=1, soBuoc=3,
           loi=['Con nghe kỹ chữ lần. Có chữ lần thì nghĩ tới nhân và chia.',
                'Không có chữ lần thì là cộng và trừ.']),
        _c('so_do_doan', 'Giảm 3 lần: cắt thành 3 phần, lấy một phần',
           be=6, lon=18, nhanBe='giảm 3 lần', nhanLon='số cũ',
           chuPhu='18 giảm 3 lần là 18 : 3 = 6.',
           loi=['Giảm ba lần thì làm ngược lại. Cắt thành ba phần bằng nhau rồi lấy '
                'một phần.',
                'Mười tám giảm ba lần là mười tám chia ba, bằng sáu.']),
        _c('y_toan', 'Gấp và giảm là đôi máy ngược chiều',
           'Gấp k lần: × k     ·     Giảm k lần: : k', buoc=2, soBuoc=3,
           loi=['Gấp và giảm là đôi máy chạy ngược chiều nhau.']),
        _c('so_do_doan', 'Hỏi "gấp mấy lần" thì lấy số lớn CHIA số bé',
           be=4, lon=12, nhanBe='4', nhanLon='12',
           chuPhu='Khối 4 xếp 3 lần thì đầy 12, nên 12 gấp 3 lần 4.',
           loi=['Có khi đề hỏi ngược. Mười hai gấp mấy lần bốn.',
                'Xem khối bốn xếp mấy lần thì đầy mười hai. Lấy số lớn chia số bé, '
                'được ba lần.']),
        _c('cong_thuc', 'Nghe chữ LẦN thì nhớ ba việc',
           congThuc='gấp k lần: × k  ·  giảm k lần: : k  ·  gấp mấy lần: lớn : bé',
           thay='vì chữ LẦN nói về SỐ KHỐI, còn thêm bớt nói về SỐ ĐƠN VỊ',
           loi=['Con nhớ ba việc. Gấp thì nhân, giảm thì chia, hỏi gấp mấy lần thì '
                'lấy số lớn chia số bé.',
                'Vì chữ lần nói về số khối, còn thêm bớt chỉ nói về số đơn vị.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_mot_phan_may(b):
    """L3·C2⑤ Tìm một phần mấy của một số."""
    return [
        _c('bia', 'Một phần mấy của một số', so_bai(b),
           loi=['Một nửa, một phần ba, một phần tư. Nay con viết chúng gọn lại.']),
        _c('phan_so', 'Số dưới cho biết chia làm mấy phần', tu=1, mau=3,
           nhan='một phần ba',
           chuPhu='Số 1 ở trên nghĩa là lấy MỘT phần trong số ấy.',
           loi=['Số ở dưới cho biết chia làm mấy phần bằng nhau.',
                'Số một ở trên nghĩa là lấy đúng một phần.']),
        _c('nhom_deu', 'Tìm một phần ba của 12', tong=12, moiNhom=4,
           chuPhu='Chia 12 thành 3 phần bằng nhau, mỗi phần 4.',
           loi=['Tìm một phần ba của mười hai. Con chia mười hai thành ba phần bằng '
                'nhau.',
                'Mỗi phần được bốn. Vậy một phần ba của mười hai là bốn.']),
        _c('y_toan', 'Nên tìm một phần mấy chính là CHIA',
           '1/3 của 12  →  12 : 3 = 4', buoc=1, soBuoc=3,
           loi=['Nên tìm một phần mấy của một số chính là đem số ấy chia đi.']),
        _c('phan_so', 'Cùng số 12, ba anh em cho ba kết quả', tu=1, mau=2,
           nhan='1/2 của 12 là 6', tu2=1, mau2=4, nhan2='1/4 của 12 là 3',
           chuPhu='Số dưới càng to thì phần nhận càng bé.',
           loi=['Vẫn số mười hai ấy. Một phần hai được sáu, một phần tư chỉ được ba.',
                'Số ở dưới càng to thì chia càng nhiều phần, nên mỗi phần càng bé.']),
        _c('y_toan', 'Chiều ngược lại', 'Biết 1/5 là 4 — cả số là bao nhiêu?',
           buoc=2, soBuoc=3,
           loi=['Có khi đề đi ngược. Biết một phần năm là bốn, hỏi cả số là bao '
                'nhiêu.']),
        _c('y_toan', 'Một phần là 4, mà cả số gồm 5 phần', '4 × 5 = 20',
           buoc=3, soBuoc=3,
           loi=['Một phần là bốn, mà cả số gồm năm phần. Vậy lấy bốn nhân năm, được '
                'hai mươi.']),
        _c('cong_thuc', 'Hai chiều của cùng một việc',
           congThuc='tìm 1/k của số:  : k     ·     biết 1/k, tìm cả số:  × k',
           thay='và chỉ gọi là một phần mấy khi các phần BẰNG NHAU',
           loi=['Con nhớ hai chiều. Tìm một phần mấy thì chia, biết một phần rồi tìm '
                'cả số thì nhân.',
                'Và chỉ được gọi là một phần mấy khi các phần bằng nhau.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 3 · Dãy số thám hiểm — ba bài
# ═══════════════════════════════════════════════════════════════════════════
# Cả ba bài đứng hay đổ ở MỘT chỗ: TOA LÀ CÂY, BƯỚC NHẢY LÀ KHOẢNG. Từ toa thứ
# nhất tới toa thứ năm chỉ có bốn bước nhảy, không phải năm. Mọi dấu trừ một và
# cộng một trong cả chương đều từ đó mà ra.
#
# `day_so` bật `hienThuTu` vẽ HAI hàng chồng nhau: hàng trên là ĐỨNG THỨ MẤY, hàng
# dưới là SỐ NÀO. Đó đúng là hai thứ bé hay trộn vào nhau, và cũng là lý do cảnh
# này được viết ra từ đầu.


def kb3_toa_thu_n(b):
    """L3·C3① Toa thứ n ở đâu — toa là cây, bước nhảy là khoảng."""
    return [
        _c('bia', 'Toa thứ mấy thì mang số nào', so_bai(b),
           loi=['Không cần viết cả dãy vẫn biết toa thứ mười mang số nào.']),
        _c('day_so', 'Dãy này có nhịp đều', so=[5, 8, 11, 14, 17],
           hienThuTu=True, chuPhu='Cứ mỗi toa lại cộng thêm 3.',
           loi=['Dãy này có nhịp đều. Cứ sang toa sau là cộng thêm ba.',
                'Hàng trên là đứng thứ mấy, hàng dưới là số nào. Hai thứ khác nhau '
                'đấy.']),
        _c('day_so', 'Từ toa 1 đến toa 5 có mấy bước nhảy?', so=[5, 8, 11, 14, 17],
           hienThuTu=True, chiSo=5,
           chuPhu='Chỉ 4 bước, không phải 5 — toa là cây, bước nhảy là khoảng.',
           loi=['Con đếm kỹ chỗ này. Từ toa thứ nhất tới toa thứ năm có mấy bước '
                'nhảy.',
                'Chỉ bốn bước thôi, không phải năm. Toa giống như cây, còn bước nhảy '
                'là khoảng giữa hai cây.']),
        _c('y_toan', 'Nên toa thứ 5 tính thế này', '5 + 3 × 4 = 17',
           buoc=1, soBuoc=3,
           loi=['Nên toa thứ năm bằng số đầu cộng ba nhân bốn, được mười bảy.']),
        _c('cong_thuc', 'Công thức của cả chương',
           congThuc='toa thứ n = số đầu + nhịp × (n − 1)',
           thay='trừ một, vì đi từ toa đầu tới toa thứ n chỉ có n trừ một khoảng',
           loi=['Toa thứ en-nờ bằng số đầu cộng nhịp nhân với en-nờ trừ một.',
                'Trừ một là vì đi từ toa đầu tới toa ấy chỉ có ngần ấy khoảng.']),
        _c('y_toan', 'Thử toa thứ 10 — đứng yên mà tính', '5 + 3 × 9 = 32',
           buoc=2, soBuoc=3,
           loi=['Thử toa thứ mười. Năm cộng ba nhân chín, bằng ba mươi hai.']),
        _c('day_so', 'Liệt kê ra để đối chiếu',
           so=[5, 8, 11, 14, 17, 20, 23, 26, 29, 32], hienThuTu=False, chiSo=10,
           chuPhu='Đếm tay cũng ra 32 — hai con đường gặp nhau.',
           loi=['Đếm tay cũng ra ba mươi hai. Hai con đường gặp nhau ở cùng một chỗ.']),
        _c('y_toan', 'Bài ngược: số 29 ở toa thứ mấy?',
           '(29 − 5) : 3 = 8 bước  →  toa thứ 9', buoc=3, soBuoc=3,
           loi=['Đề đi ngược thì làm ngược. Hai mươi chín trừ năm được hai mươi bốn.',
                'Chia cho nhịp ba được tám bước nhảy. Cộng thêm một vì đếm cả toa xuất '
                'phát, ra toa thứ chín.']),
        _c('cong_thuc', 'Hai chiều, cùng một lẽ',
           congThuc='xuôi: đầu + nhịp × (n−1)   ·   ngược: (số − đầu) : nhịp + 1',
           thay='cả hai chỗ lệch một đều vì TOA LÀ CÂY, BƯỚC NHẢY LÀ KHOẢNG',
           loi=['Hai chiều, mà chỗ lệch một đều từ cùng một lẽ. Toa là cây, bước nhảy '
                'là khoảng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_ma_du(b):
    """L3·C3② Số này có thuộc dãy không — soi mã dư."""
    return [
        _c('bia', 'Số này có thuộc dãy không', so_bai(b),
           loi=['Cho một số lạ, hỏi nó có nằm trong dãy hay không.']),
        _c('day_so', 'Dãy nhịp 4, bắt đầu từ 3', so=[3, 7, 11, 15, 19],
           hienThuTu=False, chuPhu='Viết mãi cũng không hết dãy.',
           loi=['Dãy này nhịp bốn, bắt đầu từ ba. Viết mãi cũng không hết được.']),
        _c('y_toan', 'Chia thử vài số cho nhịp 4',
           '3 dư 3  ·  7 dư 3  ·  11 dư 3  ·  15 dư 3', buoc=1, soBuoc=3,
           loi=['Con chia thử vài số cho nhịp bốn. Ba dư ba, bảy dư ba, mười một dư '
                'ba. Cả dãy chung một phần dư.']),
        _c('cong_thuc', 'Vì sao cả dãy chung một phần dư?',
           congThuc='mỗi bước cộng thêm ĐÚNG một nhịp',
           thay='thêm tròn một nhóm thì phần dư không đổi chút nào',
           loi=['Vì mỗi bước cộng thêm đúng một nhịp, tức là thêm tròn một nhóm.',
                'Thêm tròn một nhóm thì phần dư không đổi chút nào.']),
        _c('tach_so', 'Soi số lạ: 30 có thuộc dãy không?', so='30',
           phep='30 : 4 = 7 (dư 2)', chuPhu='Dư 2, mà dãy dư 3 — tàu KHÔNG dừng.',
           loi=['Soi số ba mươi. Chia bốn được bảy, dư hai.',
                'Dãy thì dư ba, lệch nhau nên ba mươi không thuộc dãy.']),
        _c('tach_so', 'Còn số 39?', so='39', phep='39 : 4 = 9 (dư 3)',
           chuPhu='Khớp — 39 thuộc dãy.',
           loi=['Còn ba mươi chín. Chia bốn được chín, dư ba. Khớp, nên nó thuộc dãy.']),
        _c('y_toan', 'Và nó đứng ở toa thứ mấy?',
           '(39 − 3) : 4 + 1 = 10', buoc=2, soBuoc=3,
           loi=['Ba mươi chín trừ ba, chia bốn, cộng một, được toa thứ mười.']),
        _c('y_toan', 'Cạm bẫy: nhìn chẵn lẻ chỉ để LOẠI',
           'Dãy 4, 8, 12… toàn số chẵn — nhưng 34 chẵn mà KHÔNG thuộc',
           buoc=3, soBuoc=3,
           loi=['Con cẩn thận chỗ này. Dãy bốn, tám, mười hai toàn số chẵn.',
                'Số ba mươi tư cũng chẵn, nhưng chia bốn lại dư hai nên không thuộc '
                'dãy.',
                'Nhìn chẵn lẻ chỉ giúp loại nhanh, chưa đủ để kết luận.']),
        _c('cong_thuc', 'Muốn biết một số có thuộc dãy',
           congThuc='chia cho NHỊP, so PHẦN DƯ với phần dư của dãy',
           thay='vì cả dãy chung một phần dư, còn chẵn lẻ chỉ loại được một nửa',
           loi=['Con nhớ cách soi. Chia cho nhịp rồi so phần dư với phần dư của dãy.',
                'Vì cả dãy chung một phần dư, còn nhìn chẵn lẻ mới loại được một nửa '
                'thôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_nhip_khong_deu(b):
    """L3·C3③ Nhịp không đều thì thử tiếp, đừng vội bảo đề sai."""
    return [
        _c('bia', 'Khi nhịp không đều', so_bai(b),
           loi=['Có dãy nhịp không đều. Đề không sai đâu, chỉ là quy luật khác.']),
        _c('day_so', 'Dãy này thì sao?', so=[1, 2, 4, 7, 11],
           hienThuTu=False, chuPhu='Thử phép thử thứ nhất: tính hiệu.',
           loi=['Dãy một, hai, bốn, bảy, mười một. Con thử phép thử thứ nhất, tính '
                'hiệu hai số liền nhau.']),
        _c('y_toan', 'Phép thử 1 — hiệu có đều không?',
           '1, 2, 3, 4 — KHÔNG đều', buoc=1, soBuoc=4,
           loi=['Hiệu lần lượt là một, hai, ba, bốn. Không đều.',
                'Nhiều bạn dừng ở đây và bảo đề sai. Con đừng dừng.']),
        _c('day_so', 'Phép thử 3 — soi chính hàng hiệu ấy', so=[1, 2, 3, 4],
           hienThuTu=False, chuPhu='Hàng hiệu lại là một bậc thang đều tăm tắp!',
           loi=['Con soi chính hàng hiệu ấy. Một, hai, ba, bốn.',
                'Hàng dưới lại là một bậc thang đều tăm tắp.']),
        _c('y_toan', 'Nên số tiếp theo cộng thêm 5', '11 + 5 = 16',
           buoc=2, soBuoc=4,
           loi=['Nên phần cộng thêm lần sau là năm. Mười một cộng năm bằng mười sáu.']),
        _c('y_toan', 'Phép thử 2 — cộng hai toa trước?',
           'Dãy 1, 1, 2, 3, 5, 8 — mỗi số là tổng hai số liền trước',
           buoc=3, soBuoc=4,
           loi=['Còn một kiểu nữa. Dãy một, một, hai, ba, năm, tám.',
                'Mỗi số bằng tổng của hai số đứng ngay trước nó. Hai cộng ba bằng '
                'năm, ba cộng năm bằng tám.']),
        _c('y_toan', 'Phép thử 4 — hai phép thay phiên?',
           'Dãy 2, 4, 5, 10, 11, 22 — nhân 2 rồi cộng 1, luân phiên',
           buoc=4, soBuoc=4,
           loi=['Kiểu cuối là hai phép thay phiên nhau. Hai nhân hai được bốn, bốn '
                'cộng một được năm.',
                'Rồi năm nhân hai được mười, mười cộng một được mười một.']),
        _c('cong_thuc', 'Bốn phép thử, thử lần lượt',
           congThuc='① hiệu đều?  ② cộng hai số trước?  ③ soi hàng hiệu?  ④ luân phiên?',
           thay='nhịp không đều KHÔNG có nghĩa là đề sai, chỉ là chưa thử tới',
           loi=['Con nhớ bốn phép thử, làm lần lượt từng phép một.',
                'Nhịp không đều không có nghĩa là đề sai, chỉ là mình chưa thử tới '
                'thôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 4 · Thứ tự phép tính — bốn bài
# ═══════════════════════════════════════════════════════════════════════════
# Bốn bài này dạy MỘT thứ tự và cách dùng nó:
#   B13 không ngoặc: nhân chia trước, cộng trừ sau, cùng loại thì trái trước
#   B14 có ngoặc: mở trong cùng ra ngoài
#   B15 tìm X hai máy: gỡ máy ngoài trước, đảo phép
#   B16 rà mắt tìm cấu trúc trước khi cắm đầu tính
#
# ⚠ Sách viết chương này bằng rất nhiều ví von bị `TU_CAM` cấm (mật thất, tuyệt kỹ,
# thám tử, Gauss). Kịch bản nói thẳng bằng chữ toán — đó chính là điều bác chốt khi
# bỏ nhân vật: giữ Ý của sách, bỏ VỎ của sách.


def kb3_lan_uu_tien(b):
    """L3·C4① Nhân chia tính trước, cộng trừ tính sau."""
    return [
        _c('bia', 'Phép nào tính trước', so_bai(b),
           loi=['Một dãy phép tính. Làm phép nào trước thì ra kết quả khác nhau.']),
        _c('de_toan', 'Đề bài', de='Tính 5 + 3 × 2',
           loi=['Tính năm cộng ba nhân hai.']),
        _c('y_toan', 'Hai cách làm, hai đáp số khác nhau',
           'cộng trước: 8 × 2 = 16     ·     nhân trước: 5 + 6 = 11',
           buoc=1, soBuoc=3,
           loi=['Cộng trước thì được mười sáu. Nhân trước thì được mười một.',
                'Chỉ một trong hai là đúng, nên phải có luật.']),
        _c('luoi_cham', 'Đọc lại đề bằng đồ vật: 3 túi, mỗi túi 2 viên',
           hang=3, cot=2,
           chuPhu='Muốn biết cả thảy mấy viên thì phải bóc túi ra đã.',
           loi=['Con đọc lại đề bằng đồ vật. Có ba túi, mỗi túi hai viên.',
                'Muốn biết cả thảy bao nhiêu viên thì phải bóc túi ra trước đã.']),
        _c('y_toan', 'Nên nhân tính trước', '5 + 3 × 2 = 5 + 6 = 11',
           buoc=2, soBuoc=3,
           loi=['Nên phép nhân tính trước. Ba nhân hai bằng sáu, rồi cộng năm, được '
                'mười một.']),
        _c('y_toan', 'Chia cũng đi cùng làn với nhân', '20 − 12 : 4 = 20 − 3 = 17',
           buoc=3, soBuoc=3,
           loi=['Phép chia cũng đi cùng nhóm với phép nhân.',
                'Hai mươi trừ mười hai chia bốn. Chia trước được ba, rồi lấy hai mươi '
                'trừ ba, bằng mười bảy.']),
        _c('y_toan', 'Cùng một nhóm thì làm từ TRÁI sang',
           '24 : 4 × 2 = 6 × 2 = 12, không phải 24 : 8', buoc=1, soBuoc=1,
           loi=['Gặp hai phép cùng một nhóm thì làm lần lượt từ trái sang phải.',
                'Hai mươi tư chia bốn được sáu, rồi nhân hai được mười hai. Không '
                'được nhảy cóc nhân bốn với hai trước.']),
        _c('cong_thuc', 'Luật của mọi dãy phép tính',
           congThuc='NHÂN CHIA trước  ·  CỘNG TRỪ sau  ·  cùng nhóm thì TRÁI trước',
           thay='vì nhân là gộp nhiều nhóm bằng nhau, phải gộp xong mới cộng thêm được',
           loi=['Con nhớ luật này. Nhân chia làm trước, cộng trừ làm sau, cùng nhóm '
                'thì làm từ trái sang.',
                'Vì nhân là gộp nhiều nhóm bằng nhau, gộp xong mới cộng thêm được.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_dau_ngoac(b):
    """L3·C4② Dấu ngoặc — mở trong cùng ra ngoài."""
    return [
        _c('bia', 'Dấu ngoặc đổi cả đáp số', so_bai(b),
           loi=['Cùng những con số ấy, thêm một dấu ngoặc là đáp số khác hẳn.']),
        _c('y_toan', 'Cùng bộ số, khác một dấu ngoặc',
           '5 + 3 × 2 = 11     ·     (5 + 3) × 2 = 16', buoc=1, soBuoc=3,
           loi=['Con nhìn hai dòng này. Cùng ba con số ấy, cùng hai phép tính ấy.',
                'Một bên được mười một, một bên được mười sáu. Khác nhau chỉ ở dấu '
                'ngoặc.']),
        _c('y_toan', 'Ngoặc được quyền đi trước tất cả',
           'Trong ngoặc  →  nhân chia  →  cộng trừ', buoc=2, soBuoc=3,
           loi=['Dấu ngoặc được quyền đi trước tất cả. Tính trong ngoặc xong đã.',
                'Rồi mới tới nhân chia, sau cùng mới tới cộng trừ.']),
        _c('de_toan', 'Hai lớp ngoặc thì sao?', de='Tính 20 − (12 − (3 + 1))',
           loi=['Có khi ngoặc nằm trong ngoặc. Tính hai mươi trừ, mở ngoặc, mười hai '
                'trừ, mở ngoặc, ba cộng một.']),
        _c('y_toan', 'Mở từ lớp TRONG CÙNG ra ngoài',
           '(3 + 1) = 4  →  (12 − 4) = 8  →  20 − 8 = 12', buoc=3, soBuoc=3,
           loi=['Mở từ lớp trong cùng ra ngoài. Ba cộng một bằng bốn.',
                'Rồi mười hai trừ bốn bằng tám. Sau cùng hai mươi trừ tám bằng mười '
                'hai.']),
        _c('y_toan', 'Một dấu ngoặc đổi hẳn phép chia',
           '36 : (2 + 4) = 6     nhưng     36 : 2 + 4 = 22', buoc=1, soBuoc=1,
           loi=['Con xem chỗ này. Ba mươi sáu chia cho, mở ngoặc, hai cộng bốn, được '
                'sáu.',
                'Còn ba mươi sáu chia hai rồi cộng bốn thì được hai mươi hai. Chép '
                'sót một dấu ngoặc là lạc sang bài khác.']),
        _c('cong_thuc', 'Thứ tự đầy đủ, và một phép soát đề',
           congThuc='NGOẶC → NHÂN CHIA → CỘNG TRỪ  ·  đếm ngoặc mở = ngoặc đóng',
           thay='vì ngoặc nói rõ phần nào phải gộp lại thành một cụm trước',
           loi=['Con nhớ thứ tự đầy đủ. Ngoặc trước, rồi nhân chia, sau cùng cộng trừ.',
                'Và khi chép đề, đếm xem số ngoặc mở có bằng số ngoặc đóng không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_tim_x_hai_may(b):
    """L3·C4③ Tìm X khi có hai phép — gỡ phép ngoài trước."""
    return [
        _c('bia', 'Tìm số bí mật khi có hai phép', so_bai(b),
           loi=['Tìm số bí mật. Lần này nó đi qua hai phép tính chứ không phải một.']),
        _c('de_toan', 'Đề bài', de='Tìm X, biết  X × 4 + 5 = 29',
           loi=['Tìm ích, biết ích nhân bốn rồi cộng năm thì được hai mươi chín.']),
        _c('y_toan', 'X đi qua hai phép, theo đúng thứ tự',
           'X  →  × 4  →  + 5  →  29', buoc=1, soBuoc=3,
           loi=['Ích đi qua hai phép. Nhân bốn trước, rồi cộng năm, ra hai mươi '
                'chín.']),
        _c('y_toan', 'Đi lùi thì gỡ phép VÀO SAU trước',
           'Mặc áo rồi mới khoác ba lô — cởi thì cởi ba lô trước', buoc=2, soBuoc=3,
           loi=['Muốn đi lùi thì gỡ cái vào sau cùng ra trước.',
                'Giống như mặc áo rồi mới khoác ba lô. Lúc cởi thì phải cởi ba lô '
                'trước.']),
        _c('y_toan', 'Gỡ phép cộng 5 — đảo thành trừ 5', 'X × 4 = 29 − 5 = 24',
           buoc=3, soBuoc=3,
           loi=['Gỡ phép cộng năm thì đảo thành trừ năm. Hai mươi chín trừ năm bằng '
                'hai mươi bốn.',
                'Nay chỉ còn ích nhân bốn bằng hai mươi bốn, quen rồi.']),
        _c('y_toan', 'Gỡ nốt phép nhân 4 — đảo thành chia 4', 'X = 24 : 4 = 6',
           buoc=1, soBuoc=1,
           loi=['Gỡ nốt phép nhân bốn thì đảo thành chia bốn. Hai mươi bốn chia bốn '
                'bằng sáu.',
                'Vậy ích bằng sáu.']),
        _c('y_toan', 'Thử lại — và nhớ luật thứ tự',
           '6 × 4 + 5 = 24 + 5 = 29 ✓',
           loi=['Thử lại. Sáu nhân bốn bằng hai mươi bốn, cộng năm bằng hai mươi '
                'chín. Đúng đề.',
                'Lúc thử vẫn phải theo luật nhân trước cộng sau.']),
        _c('cong_thuc', 'Hai phép thì làm hai nấc',
           congThuc='gỡ phép NGOÀI trước, đảo phép  ·  còn lại là bài một phép',
           thay='vì cụm chứa X phải coi như MỘT ô trống to, gỡ xong mới mở ra được',
           loi=['Con nhớ cách làm. Gỡ phép ngoài trước và đảo phép ấy lại.',
                'Vì cụm chứa ích phải coi như một ô trống to, gỡ xong mới mở nó ra '
                'được.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_ra_mat_truoc(b):
    """L3·C4④ Rà mắt tìm cấu trúc trước khi cắm đầu tính."""
    return [
        _c('bia', 'Nhìn trước, tính sau', so_bai(b),
           loi=['Có những dãy tính, nhìn một cái là làm được ngay trong đầu.']),
        _c('de_toan', 'Đề bài', de='Tính nhanh  37 + 25 + 13 + 5',
           loi=['Tính nhanh ba mươi bảy cộng hai mươi lăm cộng mười ba cộng năm.']),
        _c('y_toan', 'Rà đuôi số tìm cặp tròn chục',
           '37 với 13 thành 50   ·   25 với 5 thành 30', buoc=1, soBuoc=3,
           loi=['Con rà đuôi các số. Ba mươi bảy với mười ba thành năm mươi.',
                'Hai mươi lăm với năm thành ba mươi.']),
        _c('y_toan', 'Ghép cặp rồi cộng', '50 + 30 = 80', buoc=2, soBuoc=3,
           loi=['Ghép cặp xong chỉ còn năm mươi cộng ba mươi, bằng tám mươi.']),
        _c('de_toan', 'Kiểu thứ hai', de='Tính nhanh  2 × 36 + 2 × 64',
           loi=['Kiểu thứ hai. Tính nhanh hai nhân ba mươi sáu, cộng hai nhân sáu '
                'mươi tư.']),
        # ⚠ HÌNH VẼ ĐƯỢC BAO NHIÊU THÌ NÓI BẤY NHIÊU. Bản đầu để lưới 2×3 và 2×4 mà
        # lời chú ghi "2 khay 36 và 2 khay 64" — bé đếm ra 6 với 8, đọc thấy 36 với
        # 64. Đúng cái bẫy đã dính ở lớp 2 (`hinh-trong-video-phai-khop-loi-doc`).
        # Nay lưới dạy NGUYÊN TẮC bằng đúng số nó vẽ, rồi màn sau mới áp vào đề.
        _c('luoi_cham', 'Hai cụm cùng có phần "2 hàng"', hang=2, cot=3, cot2=4,
           chuPhu='2 hàng 3 và 2 hàng 4 ghép lại đúng bằng 2 hàng 7.',
           loi=['Hai hàng ba viên, ghép với hai hàng bốn viên, đúng bằng hai hàng '
                'bảy viên.',
                'Phần hai hàng giữ nguyên, chỉ cộng phần ruột lại.']),
        _c('y_toan', 'Đề bài cũng đúng nguyên tắc ấy',
           '2 × 36 + 2 × 64 = 2 × (36 + 64) = 2 × 100 = 200', buoc=3, soBuoc=3,
           loi=['Đề bài cũng đúng nguyên tắc ấy. Giữ phần hai nhân, cộng phần ruột '
                'lại.',
                'Ba mươi sáu cộng sáu mươi tư được một trăm chẵn. Hai nhân một trăm '
                'bằng hai trăm.']),
        _c('y_toan', 'Một số đứng lẻ cũng gom được',
           '4 × 9 + 4 = 4 × 9 + 4 × 1 = 4 × 10 = 40',
           loi=['Số bốn đứng lẻ ấy chính là bốn nhân một. Gom lại thành bốn nhân, '
                'mở ngoặc, chín cộng một, bằng bốn mươi.']),
        _c('cong_thuc', 'Rà một vòng trước khi cắm đầu tính',
           congThuc='có cặp tròn chục?  ·  có hai cụm cùng một thừa số?',
           thay='vì đổi chỗ và gom nhóm không làm đổi kết quả, chỉ làm nhẹ việc',
           loi=['Con rà một vòng trước khi cắm đầu tính. Có cặp nào tròn chục không, '
                'có hai cụm nào cùng một thừa số không.',
                'Đổi chỗ và gom nhóm không làm đổi kết quả, chỉ làm việc nhẹ đi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 5 · Toán lời văn — năm bài
# ═══════════════════════════════════════════════════════════════════════════
# Cả chương xoay quanh một nghi thức: ĐỨNG Ở CÂU HỎI CUỐI MÀ HỎI NGƯỢC. Bài 17 dạy
# nghi thức ấy, bốn bài sau là bốn dạng trạm giữa khác nhau:
#   B18 trạm giữa là "ai nhiều phần, ai một phần"
#   B19 trạm giữa là HIỆU, và chuyển qua lại thì chỉ cần một nửa hiệu
#   B20 trạm giữa là hiệu tuổi (không đổi) hoặc số người (tổng tăng theo)
#   B21 trạm giữa luôn mang tên MỘT ĐƠN VỊ
#
# `so_do_doan` vẽ hai đoạn dài ngắn khác nhau — đúng thứ bốn bài này cần, vì vẽ
# xong thì phép tính gần như tự lộ ra.


def kb3_hai_buoc_tinh(b):
    """L3·C5① Bài toán hai bước — tìm trạm giữa bị giấu."""
    return [
        _c('bia', 'Bài toán phải tính hai lần', so_bai(b),
           loi=['Có bài không tính một phép là xong. Phải đi qua một trạm giữa.']),
        _c('de_toan', 'Đề bài',
           de='Thùng 1 có 18 lít. Thùng 2 ít hơn thùng 1 sáu lít. Cả hai thùng mấy lít?',
           loi=['Thùng thứ nhất có mười tám lít. Thùng thứ hai ít hơn thùng thứ nhất '
                'sáu lít.',
                'Hỏi cả hai thùng có bao nhiêu lít.']),
        _c('y_toan', 'Đứng ở câu hỏi cuối mà hỏi ngược',
           'Muốn tính CẢ HAI thùng thì cần biết gì?', buoc=1, soBuoc=3,
           loi=['Con đứng ở câu hỏi cuối rồi hỏi ngược lại. Muốn tính cả hai thùng '
                'thì cần biết gì.',
                'Cần biết thùng một và thùng hai. Thùng một đề cho rồi, thùng hai thì '
                'chưa.']),
        _c('so_do_doan', 'Thùng 2 chính là trạm giữa bị giấu', be=12, lon=18,
           nhanBe='thùng 2 · chưa biết', nhanLon='thùng 1 · 18 lít',
           hienHieu=True, chuHieu='ít hơn 6 lít',
           chuPhu='Vẽ ra thì thấy ngay phải tìm gì trước.',
           loi=['Thùng hai chính là trạm giữa bị giấu. Vẽ hai đoạn ra thì thấy ngay.']),
        _c('y_toan', 'Chặng 1 — tìm trạm giữa', '18 − 6 = 12 (lít)',
           buoc=2, soBuoc=3,
           loi=['Chặng một, tìm trạm giữa. Mười tám trừ sáu bằng mười hai lít.']),
        _c('y_toan', 'Chặng 2 — mới về đích', '18 + 12 = 30 (lít)',
           buoc=3, soBuoc=3,
           loi=['Chặng hai mới về đích. Mười tám cộng mười hai bằng ba mươi lít.']),
        _c('y_toan', 'Soi lại trước khi ghi đáp số',
           'Số 12 mới là trạm giữa — dừng ở đó là chưa trả lời đề',
           loi=['Con soi lại trước khi ghi đáp số. Số mười hai mới chỉ là trạm giữa.',
                'Dừng ở đó là chưa trả lời câu hỏi của đề.']),
        _c('cong_thuc', 'Nghi thức của mọi bài hai bước',
           congThuc='hỏi ngược từ đích  →  thứ CHƯA BIẾT là trạm giữa  →  tìm nó trước',
           thay='vì cái đề hỏi luôn dựa trên một cái mà đề chưa cho sẵn',
           loi=['Con nhớ nghi thức này. Hỏi ngược từ đích, thứ chưa biết chính là '
                'trạm giữa, tìm nó trước rồi mới về đích.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_hon_hay_gap(b):
    """L3·C5② Hơn mấy đơn vị hay gấp mấy lần — hai câu hỏi vàng."""
    return [
        _c('bia', 'Hơn mấy, hay gấp mấy lần', so_bai(b),
           loi=['Hai kiểu đề trông giống nhau mà làm khác hẳn nhau.']),
        _c('y_toan', 'Câu hỏi thứ nhất: đề có chữ LẦN không?',
           'Có LẦN → nhân chia, vẽ sơ đồ PHẦN. Không → cộng trừ, vẽ đoạn nối dài.',
           buoc=1, soBuoc=3,
           loi=['Câu hỏi thứ nhất. Đề có chữ lần hay không.',
                'Có chữ lần thì đi đường nhân chia. Không có thì đi đường cộng trừ.']),
        _c('de_toan', 'Đề bài',
           de='Chị có 15 chiếc nhãn vở, gấp 3 lần số nhãn của Mai. Mai có mấy chiếc?',
           loi=['Chị có mười lăm chiếc nhãn vở, gấp ba lần số nhãn của Mai.',
                'Hỏi Mai có mấy chiếc.']),
        _c('y_toan', 'Câu hỏi thứ hai: AI gấp AI?',
           'Chị = 3 phần   ·   Mai = 1 phần', buoc=2, soBuoc=3,
           loi=['Câu hỏi thứ hai. Ai gấp ai. Chị gấp ba lần Mai, nên chị là ba phần, '
                'Mai là một phần.']),
        _c('so_do_doan', 'Vẽ sơ đồ phần rồi nhìn', be=5, lon=15,
           nhanBe='Mai · 1 phần', nhanLon='chị · 3 phần',
           chuPhu='Chị 3 phần là 15, nên mỗi phần là 15 : 3.',
           loi=['Vẽ ra rồi nhìn. Ba phần của chị là mười lăm, nên mỗi phần là mười '
                'lăm chia ba.']),
        _c('y_toan', 'Người ẩn ÍT phần thì CHIA', '15 : 3 = 5 (chiếc)',
           buoc=3, soBuoc=3,
           loi=['Người đang phải tìm ít phần hơn, nên lấy chia. Mười lăm chia ba bằng '
                'năm chiếc.',
                'Nếu ngược lại, biết Mai mà tìm chị, thì mới lấy nhân.']),
        _c('y_toan', 'Thử lại', '5 × 3 = 15 ✓ đúng bằng số nhãn của chị',
           loi=['Thử lại. Năm nhân ba bằng mười lăm, đúng bằng số nhãn của chị.']),
        _c('cong_thuc', 'Hai câu hỏi vàng trước mọi đề so sánh',
           congThuc='① có chữ LẦN không?   ② AI hơn/gấp AI, và ai đang ẩn?',
           thay='vẽ sơ đồ xong thì phép tính gần như tự lộ ra',
           loi=['Con nhớ hai câu hỏi vàng. Đề có chữ lần không, và ai gấp ai.',
                'Vẽ sơ đồ xong thì phép tính gần như tự lộ ra.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_them_bot_bang_nhau(b):
    """L3·C5③ Chuyển qua lại thì chỉ cần một nửa hiệu."""
    return [
        _c('bia', 'Làm sao cho hai bên bằng nhau', so_bai(b),
           loi=['Hai giỏ lệch nhau. Làm sao cho hai bên bằng nhau.']),
        _c('so_do_doan', 'Giỏ A hơn giỏ B đúng 6 quả', be=14, lon=20,
           nhanBe='giỏ B · 14', nhanLon='giỏ A · 20',
           hienHieu=True, chuHieu='hiệu 6 quả',
           loi=['Giỏ A có hai mươi quả, giỏ B có mười bốn. Giỏ A hơn đúng sáu quả.']),
        _c('y_toan', 'Thêm vào bên ít — thêm đúng bằng hiệu',
           'B thêm 6 quả  →  hai giỏ cùng 20', buoc=1, soBuoc=3,
           loi=['Cách thứ nhất, thêm vào bên ít. Thêm đúng sáu quả thì hai giỏ cùng '
                'hai mươi.']),
        _c('y_toan', 'Bớt ở bên nhiều — cũng đúng bằng hiệu',
           'A bớt 6 quả  →  hai giỏ cùng 14', buoc=2, soBuoc=3,
           loi=['Cách thứ hai, bớt ở bên nhiều. Bớt đúng sáu quả thì hai giỏ cùng '
                'mười bốn.']),
        _c('y_toan', 'Nhưng CHUYỂN qua lại thì khác hẳn',
           'Mỗi quả chuyển đi: bên kia hụt 1 VÀ bên này phình 1', buoc=3, soBuoc=3,
           loi=['Nhưng chuyển qua lại thì khác hẳn. Mỗi quả chuyển đi làm bên cho hụt '
                'một, mà bên nhận lại phình lên một.',
                'Nên một lần chuyển làm hiệu giảm những hai.']),
        _c('so_do_doan', 'Nên chỉ cần chuyển một NỬA hiệu', be=17, lon=17,
           nhanBe='giỏ B · 17', nhanLon='giỏ A · 17',
           chuPhu='6 : 2 = 3 quả. A còn 17, B được 17.',
           loi=['Nên chỉ cần chuyển một nửa hiệu. Sáu chia hai bằng ba quả.',
                'Giỏ A còn mười bảy, giỏ B cũng mười bảy.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Chuyển 6 quả thì lệch ngược lại — B hơn A',
           loi=['Đây là chỗ hay nhầm. Chuyển hẳn sáu quả thì lệch ngược lại, thành B '
                'hơn A.']),
        _c('cong_thuc', 'Ba đường, hai con số khác nhau',
           congThuc='thêm HOẶC bớt một bên: đúng bằng HIỆU  ·  chuyển qua lại: HIỆU : 2',
           thay='vì chuyển thì một bên hụt và một bên phình, hiệu đổi gấp đôi',
           loi=['Con nhớ hai con số. Thêm hoặc bớt một bên thì đúng bằng hiệu.',
                'Còn chuyển qua lại thì chỉ cần một nửa hiệu, vì hiệu đổi gấp đôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_toan_tuoi(b):
    """L3·C5④ Hiệu tuổi đóng băng, tổng tuổi tăng theo số người."""
    return [
        _c('bia', 'Hai điều về tuổi', so_bai(b),
           loi=['Hai điều về tuổi mà biết rồi thì bài nào cũng làm được.']),
        _c('so_do_doan', 'Mẹ 32, con 8 — mẹ hơn con 24 tuổi', be=8, lon=32,
           nhanBe='con · 8', nhanLon='mẹ · 32',
           hienHieu=True, chuHieu='hơn 24 tuổi',
           loi=['Mẹ ba mươi hai tuổi, con tám tuổi. Mẹ hơn con hai mươi bốn tuổi.']),
        _c('y_toan', 'Điều thứ nhất: HIỆU tuổi không bao giờ đổi',
           'Mỗi năm cả hai cùng thêm 1 — khoảng cách giữ nguyên', buoc=1, soBuoc=3,
           loi=['Điều thứ nhất. Hiệu tuổi không bao giờ đổi.',
                'Vì mỗi năm cả hai người cùng thêm một tuổi, nên khoảng cách giữ '
                'nguyên mãi.']),
        _c('de_toan', 'Đề bài', de='Khi con 12 tuổi thì mẹ bao nhiêu tuổi?',
           loi=['Hỏi khi con mười hai tuổi thì mẹ bao nhiêu tuổi.']),
        _c('y_toan', 'Dùng ngay hiệu đóng băng', '12 + 24 = 36 (tuổi)',
           buoc=2, soBuoc=3,
           loi=['Dùng ngay cái hiệu đóng băng ấy. Mười hai cộng hai mươi bốn bằng ba '
                'mươi sáu tuổi.',
                'Thử lại cũng được. Con thêm bốn năm thì mẹ cũng thêm bốn năm.']),
        _c('y_toan', 'Điều thứ hai: TỔNG tuổi thì có đổi',
           'Mỗi năm tổng tăng đúng bằng SỐ NGƯỜI', buoc=3, soBuoc=3,
           loi=['Điều thứ hai. Tổng tuổi thì có đổi, và mỗi năm nó tăng đúng bằng số '
                'người.']),
        _c('y_toan', 'Năm anh chị em, tổng nay 46 tuổi',
           'Hai năm nữa: 46 + 2 × 5 = 56, không phải 48',
           loi=['Năm anh chị em, tổng nay bốn mươi sáu tuổi. Hai năm nữa mỗi người '
                'thêm hai tuổi.',
                'Nên tổng thành bốn mươi sáu cộng hai nhân năm, bằng năm mươi sáu. '
                'Không phải bốn mươi tám.']),
        _c('cong_thuc', 'Hai điều, đừng lẫn',
           congThuc='HIỆU tuổi: đóng băng  ·  TỔNG tuổi: mỗi năm tăng bằng SỐ NGƯỜI',
           thay='vì hiệu là khoảng cách, còn tổng là cộng dồn của từng người',
           loi=['Con nhớ hai điều, đừng lẫn. Hiệu tuổi đóng băng, còn tổng tuổi mỗi '
                'năm tăng đúng bằng số người.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_rut_ve_don_vi(b):
    """L3·C5⑤ Rút về một đơn vị trước đã."""
    return [
        _c('bia', 'Ghé trạm MỘT trước đã', so_bai(b),
           loi=['Đề cho giá của nhiều món. Muốn tính gì cũng phải ghé trạm một trước.']),
        _c('de_toan', 'Đề bài', de='Mua 3 hộp sữa chua hết 21 nghìn. Mua 5 hộp hết bao nhiêu?',
           loi=['Mua ba hộp sữa chua hết hai mươi mốt nghìn. Hỏi mua năm hộp hết bao '
                'nhiêu tiền.']),
        _c('y_toan', 'Đọc kỹ chỗ này trước đã',
           '21 nghìn là giá của BA hộp, không phải một hộp', buoc=1, soBuoc=3,
           loi=['Con đọc kỹ chỗ này. Hai mươi mốt nghìn là giá của ba hộp, không phải '
                'của một hộp.',
                'Cái bẫy nằm ngay đó.']),
        _c('y_toan', 'Bước 1 — rút về MỘT hộp', '21 : 3 = 7 (nghìn)',
           buoc=2, soBuoc=3,
           loi=['Bước một, rút về một hộp. Hai mươi mốt chia ba bằng bảy nghìn.']),
        _c('y_toan', 'Bước 2 — nhân ra số hộp cần', '7 × 5 = 35 (nghìn)',
           buoc=3, soBuoc=3,
           loi=['Bước hai, nhân ra số hộp cần. Bảy nhân năm bằng ba mươi lăm nghìn.']),
        _c('y_toan', 'Ướm lại cho chắc',
           '5 hộp phải đắt hơn 3 hộp — 35 so với 21, hợp lý',
           loi=['Ướm lại cho chắc. Năm hộp phải đắt hơn ba hộp.',
                'Ba mươi lăm so với hai mươi mốt, hợp lý.']),
        _c('y_toan', 'Đề đi ngược cũng ghé đúng trạm ấy',
           'Có 42 nghìn mua được mấy hộp?  →  42 : 7 = 6 hộp',
           loi=['Đề đi ngược cũng ghé đúng trạm ấy. Có bốn mươi hai nghìn thì mua '
                'được mấy hộp.',
                'Vẫn tìm giá một hộp trước, rồi lấy bốn mươi hai chia bảy, được sáu '
                'hộp.']),
        _c('cong_thuc', 'Gặp đề cho giá của nhiều món',
           congThuc='rút về MỘT trước  →  muốn nhiều thì NHÂN, muốn biết mấy thì CHIA',
           thay='vì trạm MỘT là chỗ duy nhất hai chiều đều đi qua',
           loi=['Con nhớ nghi thức. Rút về một trước đã.',
                'Rồi muốn tính nhiều món thì nhân, muốn biết mua được mấy món thì '
                'chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 6 · Suy luận — năm bài
# ═══════════════════════════════════════════════════════════════════════════
# Năm dạng suy luận, mỗi dạng một mẹo riêng, không dạng nào suy được từ dạng kia:
#   B22 đi lùi thì phải ĐẢO KÉP — đảo thứ tự VÀ đảo phép
#   B23 giả sử tất cả cùng loại, rồi đổi dần
#   B24 cây và khoảng: hỏi đường thẳng hay vòng tròn TRƯỚC khi cộng một
#   B25 hai nhóm chồng nhau: phần giao bị đếm hai lần
#   B26 hai loại lẫn lộn thì chưa được cộng — quy về một loại đã
#
# ⚠ Tên chương trong sách là "Thám tử cao cấp", mà `TU_CAM` cấm chữ ấy trong video.
# Màn hình bên ngoài vẫn giữ tên chương của sách — chỉ LỜI VIDEO là nói thẳng.


def kb3_di_lui_nhieu_tram(b):
    """L3·C6① Đi lùi nhiều trạm — đảo kép."""
    return [
        _c('bia', 'Đi lùi qua nhiều trạm', so_bai(b),
           loi=['Số bí mật đi qua ba trạm. Muốn tìm nó thì phải đi lùi cho đúng.']),
        _c('de_toan', 'Đề bài',
           de='Kho gạo bán một nửa, rồi bán thêm 5 kg, còn lại 15 kg. Lúc đầu có mấy kg?',
           loi=['Kho gạo bán đi một nửa, rồi bán thêm năm ki lô gam, thì còn lại mười '
                'lăm ki lô gam.',
                'Hỏi lúc đầu kho có bao nhiêu ki lô gam.']),
        _c('y_toan', 'Vẽ hành trình XUÔI ra đã',
           'kho  →  bán một nửa  →  bán thêm 5 kg  →  còn 15 kg', buoc=1, soBuoc=3,
           loi=['Con vẽ hành trình xuôi ra đã. Kho, bán một nửa, bán thêm năm ki lô '
                'gam, còn mười lăm.']),
        _c('y_toan', 'Đi lùi phải ĐẢO HAI THỨ',
           'đảo THỨ TỰ trạm  ·  và đảo cả PHÉP ở từng trạm', buoc=2, soBuoc=3,
           loi=['Đi lùi thì phải đảo hai thứ. Đảo thứ tự các trạm, và đảo luôn phép '
                'tính ở từng trạm.',
                'Thiếu một trong hai cú đảo là lạc đường ngay.']),
        _c('y_toan', 'Lùi trạm cuối trước: gỡ "bán thêm 5"',
           '15 + 5 = 20 (kg)', buoc=3, soBuoc=3,
           loi=['Lùi trạm cuối trước. Gỡ phép bán thêm năm thì đảo thành cộng năm.',
                'Mười lăm cộng năm bằng hai mươi ki lô gam.']),
        _c('y_toan', 'Rồi lùi tiếp: 20 kg chính là MỘT NỬA kho',
           '20 × 2 = 40 (kg)',
           loi=['Rồi lùi tiếp. Hai mươi ki lô gam ấy chính là một nửa kho.',
                'Gỡ phép chia đôi thì đảo thành nhân hai, được bốn mươi ki lô gam.']),
        _c('y_toan', 'Chốt lại bằng chuyến đi XUÔI',
           '40 bán nửa còn 20  ·  bán thêm 5 còn 15 ✓',
           loi=['Chốt lại bằng chuyến đi xuôi. Bốn mươi bán nửa còn hai mươi.',
                'Bán thêm năm thì còn mười lăm. Đúng đề.']),
        _c('cong_thuc', 'Đi lùi là ĐẢO KÉP',
           congThuc='đảo THỨ TỰ trạm  +  đảo PHÉP từng trạm',
           thay='vì trạm vào sau cùng là trạm phải gỡ ra trước nhất',
           loi=['Con nhớ hai cú đảo. Đảo thứ tự trạm và đảo phép từng trạm.',
                'Vì trạm vào sau cùng là trạm phải gỡ ra trước nhất.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_ga_cho(b):
    """L3·C6② Giả sử tất cả cùng một loại rồi đổi dần."""
    return [
        _c('bia', 'Đếm đầu, đếm chân', so_bai(b),
           loi=['Biết số con và số chân, tìm mỗi loài mấy con.']),
        _c('de_toan', 'Đề bài', de='Sân có gà và chó: 8 con, 22 cái chân. Mỗi loài mấy con?',
           loi=['Trong sân có gà và chó. Tất cả tám con và hai mươi hai cái chân.',
                'Hỏi có mấy con gà, mấy con chó.']),
        _c('y_toan', 'Nhịp 1 — giả sử tất cả đều là GÀ',
           '8 × 2 = 16 (chân)', buoc=1, soBuoc=4,
           loi=['Nhịp một. Giả sử cả tám con đều là gà. Mỗi con hai chân thì được '
                'mười sáu chân.']),
        _c('y_toan', 'Nhịp 2 — so với số chân đếm thật',
           '22 − 16 = 6 chân còn thừa, chưa có chủ', buoc=2, soBuoc=4,
           loi=['Nhịp hai. Đếm thật thì có hai mươi hai chân.',
                'Hai mươi hai trừ mười sáu, còn thừa sáu chân chưa có chủ.']),
        _c('y_toan', 'Nhịp 3 — đổi một con gà thành chó',
           'Mỗi lần đổi, đàn thêm đúng 4 − 2 = 2 chân', buoc=3, soBuoc=4,
           loi=['Nhịp ba. Mỗi lần đổi một con gà giả thành chó thật, đàn thêm đúng '
                'hai chân.',
                'Vì chó bốn chân, gà hai chân, hơn nhau hai.']),
        _c('y_toan', 'Nhịp 4 — chia cho phần chênh', '6 : 2 = 3 con chó',
           buoc=4, soBuoc=4,
           loi=['Nhịp bốn. Muốn tiêu hết sáu chân thừa thì phải đổi ba lần.',
                'Vậy có ba con chó, và gà là tám trừ ba, còn năm con.']),
        _c('y_toan', 'Thử lại cả hai điều đề cho',
           '5 × 2 + 3 × 4 = 22 chân ✓   ·   5 + 3 = 8 con ✓',
           loi=['Thử lại cả hai điều đề cho. Năm con gà mười chân, ba con chó mười '
                'hai chân, cộng lại hai mươi hai.',
                'Và tổng số con vẫn là tám.']),
        _c('cong_thuc', 'Bốn nhịp của bài đếm chân',
           congThuc='giả sử cùng loại ÍT chân  →  so chân thừa  →  chia phần chênh',
           thay='vì mỗi cú đổi làm số chân nhích đúng bằng phần chênh giữa hai loài',
           loi=['Con nhớ bốn nhịp. Giả sử tất cả là loài ít chân, tính chân giả vờ.',
                'So với số chân thật xem thừa bao nhiêu, rồi chia cho phần chênh giữa '
                'hai loài.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_ba_the_tran_cay(b):
    """L3·C6③ Cây và khoảng — ba thế trận."""
    return [
        _c('bia', 'Cây và khoảng, ba kiểu đề', so_bai(b),
           loi=['Cùng một bài trồng cây mà ba kiểu đề cho ba đáp số khác nhau.']),
        _c('y_toan', 'Xòe bàn tay ra mà nhớ', '5 ngón tay  —  chỉ 4 kẽ',
           buoc=1, soBuoc=3,
           loi=['Con xòe bàn tay ra mà nhớ. Năm ngón tay nhưng chỉ có bốn kẽ.']),
        _c('luoi_cham', 'Thế trận 1 — đường thẳng, trồng CẢ HAI đầu',
           hang=1, cot=5,
           chuPhu='5 cây thì chỉ có 4 khoảng ở giữa.',
           loi=['Thế trận thứ nhất. Đường thẳng và trồng ở cả hai đầu.',
                'Con đếm mà xem. Năm cây thì chỉ có bốn khoảng nằm giữa chúng.']),
        _c('y_toan', 'Nên phải cộng thêm 1',
           'Lối đi 12 m cách 3 m: 12 : 3 = 4 khoảng  →  5 cây', buoc=1, soBuoc=1,
           loi=['Nên phải cộng thêm một. Lối đi mười hai mét, cách ba mét, chia ra '
                'được bốn khoảng.',
                'Bốn khoảng thì năm cây.']),
        _c('y_toan', 'Thế trận 2 — một đầu đã có cột đèn',
           'Mất một cây ở đầu ấy  →  cây = khoảng = 4', buoc=2, soBuoc=3,
           loi=['Thế trận thứ hai. Một đầu lối đi đã có cột đèn, không trồng cây ở '
                'đó.',
                'Mất một cây, nên số cây đúng bằng số khoảng, là bốn.']),
        _c('y_toan', 'Thế trận 3 — quanh hồ, vòng khép kín',
           '24 m cách 4 m: 6 khoảng  →  cũng đúng 6 cây', buoc=3, soBuoc=3,
           loi=['Thế trận thứ ba. Trồng quanh hồ, vòng khép kín lại.',
                'Đi trọn một vòng thì chỗ cuối trùng đúng chỗ đầu, nên sáu khoảng '
                'cũng đúng sáu cây.']),
        _c('y_toan', 'Tiếng chuông cũng là cây',
           'Đồng hồ điểm 6 tiếng, cách nhau 2 giây  →  5 khoảng  →  10 giây',
           loi=['Tiếng chuông cũng là cây. Sáu tiếng chuông thì chỉ có năm khoảng, '
                'nên nghe trọn mất mười giây.']),
        _c('cong_thuc', 'Hỏi hai câu TRƯỚC khi cộng một',
           congThuc='① đường thẳng hay vòng tròn?  ② hai đầu có trồng không?',
           thay='chỉ đường thẳng đủ hai đầu mới cộng một, còn lại cây bằng khoảng',
           loi=['Con hỏi hai câu trước khi cộng một. Đường thẳng hay vòng tròn, và '
                'hai đầu có trồng không.',
                'Chỉ đường thẳng đủ hai đầu mới cộng một. Còn lại thì cây bằng '
                'khoảng.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_hai_vong_giao_nhau(b):
    """L3·C6④ Hai nhóm chồng nhau — phần giao bị đếm hai lần."""
    return [
        _c('bia', 'Khi hai nhóm chồng lên nhau', so_bai(b),
           loi=['Hai nhóm có người đứng ở cả hai bên. Cộng thô là ra số vô lý.']),
        _c('de_toan', 'Đề bài',
           de='Lớp 35 bạn: 20 thích bóng đá, 18 thích cầu lông, 8 thích cả hai. Mấy bạn không thích môn nào?',
           loi=['Lớp có ba mươi lăm bạn. Hai mươi bạn thích bóng đá, mười tám bạn '
                'thích cầu lông.',
                'Trong đó tám bạn thích cả hai môn. Hỏi mấy bạn không thích môn nào.']),
        _c('y_toan', 'Cộng thô thì vỡ trần ngay',
           '20 + 18 = 38, mà cả lớp chỉ có 35 bạn', buoc=1, soBuoc=3,
           loi=['Cộng thô thì vỡ trần ngay. Hai mươi cộng mười tám bằng ba mươi tám.',
                'Mà cả lớp chỉ có ba mươi lăm bạn. Con số ấy chính là dấu hiệu có '
                'nhóm thích cả hai.']),
        _c('so_do_ven', 'Vẽ hai vòng, điền vùng GIỮA trước',
           tenA='bóng đá', tenB='cầu lông', caHai='8',
           chuGiao='8 bạn thích cả hai môn đứng ở vùng giữa',
           chuPhu='Luật vàng: điền giữa trước, hai cánh sau.',
           loi=['Con vẽ hai vòng chồng nhau rồi điền vùng giữa trước.',
                'Tám bạn thích cả hai môn đứng đúng ở chỗ hai vòng ôm nhau.']),
        _c('so_do_ven', 'Hai cánh suy ra từ vùng giữa',
           tenA='bóng đá', tenB='cầu lông', chiA='12', caHai='8', chiB='10',
           chuGiao='20 − 8 = 12    và    18 − 8 = 10',
           chuPhu='Chỉ bóng đá 12 bạn, chỉ cầu lông 10 bạn.',
           loi=['Hai cánh suy ra từ vùng giữa. Hai mươi trừ tám còn mười hai bạn chỉ '
                'thích bóng đá.',
                'Mười tám trừ tám còn mười bạn chỉ thích cầu lông.']),
        _c('y_toan', 'Nay cộng ba vùng thì không trùng nữa',
           '12 + 8 + 10 = 30 bạn thích ít nhất một môn', buoc=3, soBuoc=3,
           loi=['Nay cộng ba vùng thì không ai bị đếm hai lần nữa.',
                'Mười hai cộng tám cộng mười, bằng ba mươi bạn thích ít nhất một '
                'môn.']),
        _c('y_toan', 'Còn lại là vùng ngoài cả hai vòng',
           '35 − 30 = 5 bạn không thích môn nào',
           loi=['Còn lại là vùng ngoài cả hai vòng. Ba mươi lăm trừ ba mươi, còn năm '
                'bạn.']),
        _c('cong_thuc', 'Đường tắt, và vì sao nó đúng',
           congThuc='ít nhất một môn  =  A + B − cả hai',
           thay='vì nhóm cả hai bị hai danh sách đếm hai lần, phải trả lại một lần',
           loi=['Có đường tắt. Lấy nhóm thứ nhất cộng nhóm thứ hai rồi trừ nhóm cả '
                'hai.',
                'Vì nhóm cả hai bị hai danh sách đếm những hai lần, nên phải trả lại '
                'một lần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_quy_ve_mot_loai(b):
    """L3·C6⑤ Hai loại lẫn lộn thì chưa được cộng."""
    return [
        _c('bia', 'Quy về một loại rồi mới cộng', so_bai(b),
           loi=['Hai loại lẫn lộn thì chưa được cộng. Phải đổi hết về một loại đã.']),
        _c('de_toan', 'Đề bài',
           de='1 quả dưa đổi được 3 quả cam. Hỏi 2 quả dưa và 4 quả cam đổi được mấy quả cam?',
           loi=['Một quả dưa đổi được ba quả cam.',
                'Hỏi hai quả dưa và bốn quả cam đổi được tất cả bao nhiêu quả cam.']),
        _c('y_toan', 'Cân thăng bằng cho phép ta THAY',
           'Gặp 1 dưa ở đâu cũng được nhấc ra, đặt 3 cam vào', buoc=1, soBuoc=3,
           loi=['Cân thăng bằng nói một quả dưa nặng bằng ba quả cam.',
                'Nghĩa là gặp một quả dưa ở đâu, ta cũng được nhấc nó ra và đặt ba '
                'quả cam vào thay.']),
        _c('luoi_cham', 'Thay 2 quả dưa bằng cam', hang=2, cot=3,
           chuPhu='Mỗi quả dưa thành 3 quả cam, hai quả dưa thành 6 quả cam.',
           loi=['Thay hai quả dưa bằng cam. Mỗi quả thành ba, nên hai quả thành sáu '
                'quả cam.']),
        _c('y_toan', 'Giờ mới được cộng — vì đã cùng một loại',
           '6 + 4 = 10 (quả cam)', buoc=2, soBuoc=3,
           loi=['Giờ mới được cộng, vì tất cả đã cùng một loại.',
                'Sáu cộng bốn bằng mười quả cam.']),
        _c('y_toan', 'Chỗ hay hỏng', 'Cộng thẳng 2 + 4 = 6 là cộng dưa với cam',
           loi=['Đây là chỗ hay hỏng. Cộng thẳng hai với bốn là đang cộng dưa với '
                'cam.',
                'Hai thứ khác nhau thì không cộng được.']),
        _c('y_toan', 'Phép thay chạy được cả hai chiều',
           'Có 6 quả cam đổi mấy quả dưa?  →  6 : 3 = 2 quả dưa',
           buoc=3, soBuoc=3,
           loi=['Phép thay chạy được cả hai chiều. Có sáu quả cam thì đổi được mấy '
                'quả dưa.',
                'Lấy sáu chia ba, được hai quả dưa.']),
        _c('cong_thuc', 'Gặp hai loại lẫn lộn',
           congThuc='đổi hết về MỘT loại (thường là loại nhỏ)  →  rồi mới tính',
           thay='vì cộng hai thứ khác loại thì con số ra không mang nghĩa gì',
           loi=['Con nhớ nghi thức. Đổi hết về một loại, thường là loại nhỏ, rồi mới '
                'tính.',
                'Vì cộng hai thứ khác loại thì con số ra không mang nghĩa gì cả.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 7 · Hình học — năm bài
# ═══════════════════════════════════════════════════════════════════════════
# Chương này CHỈ dạy được bằng hình. Năm bài, năm câu hỏi khác nhau về cùng một
# hình chữ nhật:
#   B27 đi vòng quanh hết bao nhiêu — chu vi có công thức
#   B28 nới một chiều thì vòng rào đổi bao nhiêu
#   B29 hình tròn có ba bộ phận và một quan hệ
#   B30 phủ kín ruột hết bao nhiêu viên — diện tích, khác hẳn chu vi
#   B31 đếm khối thì đếm bằng BẢN ĐỒ TẦNG, đừng đếm bằng mắt nhìn nghiêng
#
# `hinh_cn` có sẵn `vienDam` (tô đậm đường viền — chu vi) và `oVuong` (lát lưới ô
# — diện tích). Hai chế độ ấy đứng cạnh nhau là cả bài B30: cùng một hình, hai câu
# hỏi khác hẳn nhau.


def kb3_chu_vi_cong_thuc(b):
    """L3·C7① Chu vi hình chữ nhật và hình vuông."""
    return [
        _c('bia', 'Đi hết một vòng quanh hình', so_bai(b),
           loi=['Đi hết một vòng quanh hình thì được bao nhiêu mét.']),
        _c('hinh_cn', 'Cộng cả vòng thì cũng ra', dai=6, rong=4, vienDam=True,
           nhanDai='6 m', nhanRong='4 m',
           chuPhu='6 + 4 + 6 + 4 = 20 m — đúng, nhưng dài dòng.',
           loi=['Cách cũ là cộng cả vòng. Sáu cộng bốn cộng sáu cộng bốn, bằng hai '
                'mươi mét.',
                'Đúng, nhưng dài dòng.']),
        _c('y_toan', 'Mắt tinh sẽ thấy ngay',
           'Số 6 xuất hiện HAI lần, số 4 cũng HAI lần', buoc=1, soBuoc=3,
           loi=['Mắt tinh sẽ thấy ngay. Số sáu xuất hiện hai lần, số bốn cũng hai '
                'lần.',
                'Vì hình chữ nhật có hai cặp cạnh bằng nhau.']),
        _c('cong_thuc', 'Nên gom lại cho gọn',
           congThuc='chu vi hình chữ nhật = (dài + rộng) × 2',
           thay='gom một cặp dài với rộng rồi lấy hai lần — đúng phép gom đã học',
           loi=['Nên gom lại cho gọn. Lấy dài cộng rộng rồi nhân hai.',
                'Sáu cộng bốn là mười, nhân hai bằng hai mươi mét.']),
        _c('hinh_cn', 'Hình vuông thì bốn cạnh bằng nhau', dai=5, rong=5,
           vienDam=True, nhanDai='5 m', nhanRong='5 m',
           chuPhu='Chu vi = cạnh × 4 = 5 × 4 = 20 m.',
           loi=['Hình vuông thì cả bốn cạnh bằng nhau, nên lấy cạnh nhân bốn.',
                'Năm nhân bốn cũng bằng hai mươi mét.']),
        _c('y_toan', 'Đề chạy ngược thì chia trả lại',
           'Chu vi 20 m  →  cạnh vuông = 20 : 4 = 5 m', buoc=2, soBuoc=3,
           loi=['Đề chạy ngược thì chia trả lại. Biết chu vi hai mươi mét thì cạnh '
                'hình vuông là hai mươi chia bốn, bằng năm mét.']),
        _c('y_toan', 'Chữ nhật chạy ngược thì chia ĐÔI trước',
           '20 : 2 = 10 là NỬA vòng (dài + rộng)  →  rộng = 10 − 6 = 4 m',
           buoc=3, soBuoc=3,
           loi=['Hình chữ nhật chạy ngược thì chia đôi trước. Hai mươi chia hai được '
                'mười.',
                'Mười ấy là nửa vòng, tức dài cộng rộng. Biết dài sáu thì rộng là '
                'bốn mét.']),
        _c('cong_thuc', 'Hai công thức, một phép ngược',
           congThuc='chữ nhật: (dài + rộng) × 2   ·   vuông: cạnh × 4',
           thay='vì mỗi chiều đều có mặt ở HAI phía của hình',
           loi=['Con nhớ hai công thức. Chữ nhật lấy dài cộng rộng nhân hai, vuông '
                'lấy cạnh nhân bốn.',
                'Vì mỗi chiều đều có mặt ở hai phía của hình.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_chu_vi_bien_hinh(b):
    """L3·C7② Nới một chiều thì chu vi đổi gấp đôi."""
    return [
        _c('bia', 'Nới vườn thì cần thêm mấy mét rào', so_bai(b),
           loi=['Nới vườn ra một chút thì phải mua thêm mấy mét rào.']),
        _c('hinh_cn', 'Vườn cũ: dài 6, rộng 4', dai=6, rong=4, vienDam=True,
           nhanDai='6 m', nhanRong='4 m', chuPhu='Chu vi (6 + 4) × 2 = 20 m.',
           loi=['Vườn cũ dài sáu mét, rộng bốn mét. Chu vi là hai mươi mét.']),
        _c('hinh_cn', 'Nới chiều dài thêm 2 m', dai=8, rong=4, vienDam=True,
           nhanDai='8 m', nhanRong='4 m', chuPhu='Chu vi mới (8 + 4) × 2 = 24 m.',
           loi=['Nay nới chiều dài thêm hai mét. Chu vi mới là hai mươi tư mét.',
                'Tăng những bốn mét, chứ không phải hai.']),
        _c('y_toan', 'Vì sao tăng gấp đôi phần nới?',
           'Chiều dài nằm ở CẢ cạnh trên lẫn cạnh dưới', buoc=1, soBuoc=3,
           loi=['Vì sao lại tăng gấp đôi phần nới.',
                'Vì chiều dài nằm ở cả cạnh trên lẫn cạnh dưới. Nới hai mét là nới ở '
                'hai nơi cùng lúc.']),
        _c('y_toan', 'Nên có đường tắt, khỏi tính lại từ đầu',
           'chu vi mới = chu vi cũ + 2 × phần nới = 20 + 4 = 24', buoc=2, soBuoc=3,
           loi=['Nên có đường tắt, khỏi phải tính lại từ đầu.',
                'Chu vi mới bằng chu vi cũ cộng hai lần phần nới.']),
        _c('hinh_cn', 'Dài thêm 2 mà rộng BỚT 2 thì sao?', dai=8, rong=2,
           vienDam=True, nhanDai='8 m', nhanRong='2 m',
           chuPhu='Chu vi (8 + 2) × 2 = 20 m — y nguyên vòng rào cũ.',
           loi=['Nay thử dài thêm hai mà rộng bớt hai. Chu vi vẫn đúng hai mươi mét.',
                'Hình đổi dáng hẳn, mà vòng rào cũ vẫn ôm vừa.']),
        _c('y_toan', 'Vì phần thêm và phần bớt triệt tiêu nhau',
           'Thêm 2 ở dài: +4  ·  bớt 2 ở rộng: −4',
           loi=['Vì phần thêm và phần bớt triệt tiêu nhau. Thêm hai ở chiều dài là '
                'cộng bốn.',
                'Bớt hai ở chiều rộng là trừ bốn. Cộng lại thành không.']),
        _c('cong_thuc', 'Mọi thay đổi ở một chiều đều nhân đôi',
           congThuc='thêm k  →  chu vi tăng 2k     ·     bớt k  →  giảm 2k',
           thay='vì chiều nào cũng có mặt ở hai phía của hình',
           loi=['Con nhớ luật này. Thêm bao nhiêu ở một chiều thì chu vi tăng gấp đôi '
                'chừng ấy.',
                'Vì chiều nào cũng có mặt ở hai phía của hình.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_giai_phau_hinh_tron(b):
    """L3·C7③ Tâm, bán kính, đường kính."""
    return [
        _c('bia', 'Ba bộ phận của hình tròn', so_bai(b),
           loi=['Hình tròn có ba bộ phận, và giữa chúng có một quan hệ rất gọn.']),
        _c('hinh_tron', 'Chân nhọn com pa đứng ở đâu — đó là TÂM',
           chuPhu='Thường đặt tên là O.',
           loi=['Cắm chân nhọn com pa xuống một điểm rồi xoay trọn một vòng.',
                'Điểm ấy gọi là tâm, thường đặt tên là O.']),
        _c('hinh_tron', 'Từ tâm ra mép — đó là BÁN KÍNH', hienR=True, nhanR='r',
           chuPhu='Chính là độ mở của com pa.',
           loi=['Đoạn từ tâm ra tới mép gọi là bán kính. Nó chính là độ mở của com '
                'pa.']),
        _c('y_toan', 'Bí mật thứ nhất',
           'Mọi bán kính của MỘT hình tròn đều bằng nhau', buoc=1, soBuoc=3,
           loi=['Bí mật thứ nhất. Mọi bán kính của cùng một hình tròn đều bằng nhau.',
                'Vì com pa có đổi độ mở giữa chừng đâu.']),
        _c('hinh_tron', 'Nối hai mép VÀ đi qua tâm — đó là ĐƯỜNG KÍNH',
           hienR=True, hienD=True, nhanR='r', nhanD='d',
           chuPhu='Nó ghép từ hai bán kính chụm đầu.',
           loi=['Đoạn nối hai mép mà đi qua tâm gọi là đường kính.',
                'Nó ghép từ đúng hai bán kính chụm đầu vào nhau.']),
        _c('cong_thuc', 'Nên quan hệ rất gọn',
           congThuc='đường kính = bán kính × 2',
           thay='vì đường kính đúng bằng hai bán kính nối lại ở tâm',
           loi=['Nên quan hệ rất gọn. Đường kính bằng bán kính nhân hai.',
                'Bán kính ba xăng ti mét thì đường kính sáu xăng ti mét.']),
        _c('hinh_tron', 'Đoạn nối hai mép mà KHÔNG qua tâm thì sao?',
           dayLech=True, nhanLech='dây lệch tâm',
           chuPhu='Nó ngắn hơn đường kính — không phải đường kính.',
           loi=['Đoạn nối hai mép mà không đi qua tâm thì ngắn hơn.',
                'Nó không phải đường kính. Muốn kiểm tra, con hỏi nó có đi qua tâm '
                'không.']),
        _c('y_toan', 'Và tâm là ĐIỂM GIỮA của đường kính',
           'Muốn tìm điểm giữa đoạn 8 cm: 8 : 2 = 4 cm', buoc=3, soBuoc=3,
           loi=['Tâm chia đường kính thành hai nửa bằng nhau, nên tâm là điểm giữa.',
                'Muốn tìm điểm giữa của một đoạn tám xăng ti mét thì lấy tám chia '
                'hai, được bốn.']),
        _c('cong_thuc', 'Nhớ cả bộ bằng một cú xoay com pa',
           congThuc='chân đứng = TÂM  ·  độ mở = BÁN KÍNH  ·  hai lần độ mở = ĐƯỜNG KÍNH',
           thay='và đường kính buộc phải ĐI QUA TÂM, không thì chỉ là dây thường',
           loi=['Con nhớ cả bộ bằng một cú xoay com pa. Chân đứng là tâm, độ mở là '
                'bán kính, hai lần độ mở là đường kính.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_dien_tich(b):
    """L3·C7④ Diện tích — và nó khác hẳn chu vi."""
    return [
        _c('bia', 'Phủ kín ruột hết bao nhiêu viên', so_bai(b),
           loi=['Lần này không đi vòng quanh nữa, mà phủ kín ruột hình.']),
        _c('y_toan', 'Chọn một viên gạch chuẩn',
           'Ô vuông cạnh 1 cm — gọi là 1 xăng-ti-mét vuông', buoc=1, soBuoc=3,
           loi=['Chọn một viên gạch chuẩn. Ô vuông mỗi cạnh một xăng ti mét.',
                'Nó tên là một xăng ti mét vuông.']),
        _c('hinh_cn', 'Lát thử vào hình 4 × 3', dai=4, rong=3, oVuong=True,
           nhanDai='4 cm', nhanRong='3 cm',
           chuPhu='Vừa khít 3 hàng, mỗi hàng 4 viên.',
           loi=['Lát thử vào hình dài bốn rộng ba. Vừa khít ba hàng, mỗi hàng bốn '
                'viên.']),
        _c('y_toan', 'Không cần đếm từng viên — phép nhân đếm hộ',
           '4 × 3 = 12 (cm²)', buoc=2, soBuoc=3,
           loi=['Không cần đếm từng viên. Bốn nhân ba bằng mười hai, phép nhân đếm '
                'hộ rồi.']),
        _c('cong_thuc', 'Công thức diện tích',
           congThuc='chữ nhật: dài × rộng   ·   vuông: cạnh × cạnh',
           thay='vì mỗi hàng có "dài" viên, và có đúng "rộng" hàng như thế',
           loi=['Chữ nhật thì lấy dài nhân rộng. Vuông là chữ nhật có dài bằng rộng, '
                'nên lấy cạnh nhân cạnh.',
                'Vì mỗi hàng có đúng bằng chiều dài số viên, và có đúng bằng chiều '
                'rộng số hàng.']),
        _c('hinh_cn', 'Cùng hình ấy, hỏi VÒNG RÀO thì khác', dai=4, rong=3,
           vienDam=True, nhanDai='4 cm', nhanRong='3 cm',
           chuPhu='Chu vi (4 + 3) × 2 = 14 cm — đi vòng quanh.',
           loi=['Vẫn hình ấy, nhưng hỏi vòng rào thì khác hẳn.',
                'Chu vi là mười bốn xăng ti mét, còn diện tích là mười hai xăng ti '
                'mét vuông.']),
        _c('y_toan', 'Hai câu hỏi khác nhau, hai đơn vị khác nhau',
           'rào: đi VÒNG QUANH, cm   ·   thảm: phủ KÍN RUỘT, cm²',
           loi=['Hai câu hỏi khác nhau nên hai đơn vị cũng khác nhau.',
                'Vòng rào đo bằng xăng ti mét. Tấm thảm đo bằng xăng ti mét vuông.']),
        _c('cong_thuc', 'Hỏi trước khi tính',
           congThuc='đề muốn VÒNG RÀO hay TẤM THẢM?',
           thay='thiếu chữ vuông bé xíu ở đơn vị là trả lời sang câu hỏi khác',
           loi=['Con hỏi trước khi tính. Đề muốn vòng rào hay tấm thảm.',
                'Thiếu chữ vuông bé xíu ở đơn vị là trả lời sang câu hỏi khác mất '
                'rồi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_dem_khoi_theo_tang(b):
    """L3·C7⑤ Đếm khối bằng bản đồ tầng."""
    return [
        _c('bia', 'Đếm khối, đừng tin con mắt', so_bai(b),
           loi=['Đếm khối xếp chồng. Con mắt nhìn nghiêng hay đánh lừa lắm.']),
        # `khuyet` khai theo TỪNG TẦNG (chỉ số 0 là tầng dưới cùng), không phải
        # một con số chung — truyền số trần vào là bộ vẽ vỡ ngay.
        _c('khoi', 'Khối gỗ hai tầng', kieu='chong', dai=3, rong=2, cao=2,
           khuyet=[0, 2], chuPhu='Tầng trên bị nhấc mất mấy khối.',
           loi=['Một khối gỗ xếp hai tầng. Tầng trên bị nhấc mất mấy khối.']),
        _c('y_toan', 'Đừng đếm mặt nhìn thấy',
           'Khối đứng sau và đứng dưới bị che khuất hết', buoc=1, soBuoc=3,
           loi=['Con đừng đếm những mặt nhìn thấy. Khối đứng sau và đứng dưới bị che '
                'khuất hết.']),
        _c('khoi', 'Tách từng tầng ra mà đếm', kieu='tang', dai=3, rong=2, cao=2,
           khuyet=[0, 2], chuPhu='Mỗi tầng một bản đồ riêng.',
           loi=['Con tách từng tầng ra. Mỗi tầng vẽ một bản đồ riêng.']),
        _c('y_toan', 'Tầng dưới nguyên vẹn', '3 × 2 = 6 (khối)',
           loi=['Tầng dưới còn nguyên vẹn. Ba nhân hai bằng sáu khối.',
                'Đếm y như đếm khay kẹo ở bài diện tích.']),
        _c('y_toan', 'Tầng trên bị khoét mất 2', '6 − 2 = 4 (khối)',
           loi=['Tầng trên vốn cũng sáu khối, bị nhấc đi hai, nên còn bốn khối.']),
        _c('y_toan', 'Cộng dọc các tầng', '6 + 4 = 10 (khối)', buoc=3, soBuoc=3,
           loi=['Cộng dọc các tầng lại. Sáu cộng bốn bằng mười khối.']),
        _c('cong_thuc', 'Đếm bằng bản đồ, không đếm bằng mắt',
           congThuc='mỗi tầng một lưới  →  tầng khoét thì trừ  →  cộng dọc các tầng',
           thay='vì bản đồ tầng thấy cả khối bị che, còn mắt nhìn nghiêng thì không',
           loi=['Con nhớ cách đếm. Mỗi tầng một lưới, tầng nào bị khoét thì trừ đi, '
                'rồi cộng dọc các tầng.',
                'Vì bản đồ tầng thấy được cả khối bị che, còn mắt nhìn nghiêng thì '
                'không.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 3 · chương 8 · Toán trong cuộc sống — ba bài (CHƯƠNG CUỐI)
# ═══════════════════════════════════════════════════════════════════════════
# Ba bài đo đạc và tiền nong. Điểm chung: đơn vị. Bài nào cũng có một chỗ mà lẫn
# đơn vị là hỏng hẳn:
#   B32 mỗi số trên mặt đồng hồ đáng 5 phút, không phải 1
#   B33 gam với mi-li-lít KHÔNG cộng được với nhau
#   B34 tiền trong hộp chưa phải lãi — phải trừ vốn đã


def kb3_xem_gio_to_lich(b):
    """L3·C8① Xem giờ đến từng phút, và tờ lịch chạy nhịp bảy."""
    return [
        _c('bia', 'Xem giờ đến từng phút', so_bai(b),
           loi=['Xem giờ cho đúng tới từng phút, và đọc tờ lịch.']),
        _c('dong_ho', 'Kim phút đi trọn vòng hết 60 phút', gio=3, phut=12,
           chuPhu='Vòng ấy có 12 số, nên mỗi chặng dài 60 : 12 = 5 phút.',
           loi=['Kim phút đi trọn một vòng hết sáu mươi phút, qua mười hai số.',
                'Nên mỗi chặng dài năm phút.']),
        _c('dong_ho', 'Kim phút chỉ số 3 nghĩa là 15 phút', gio=7, phut=3,
           chuPhu='3 chặng, mỗi chặng 5 phút: 3 × 5 = 15.',
           loi=['Kim phút chỉ số ba là đã đi ba chặng. Ba nhân năm bằng mười lăm '
                'phút.']),
        _c('cong_thuc', 'Đọc số phút bằng phép nhân',
           congThuc='số phút = số kim phút chỉ × 5',
           thay='vì mỗi chặng giữa hai số đúng bằng năm phút',
           loi=['Con nhớ cách đọc. Lấy số mà kim phút chỉ, nhân với năm.',
                'Còn kim giờ thì đọc theo số nó vừa đi qua.']),
        _c('dong_ho', 'Kim phút chỉ số 11 là 55 phút', gio=8, phut=11,
           chuPhu='Người lớn hay nói gọn: "9 giờ kém 5".',
           loi=['Kim phút chỉ số mười một là năm mươi lăm phút.',
                'Người lớn hay nói gọn là chín giờ kém năm, nghĩa là còn năm phút nữa '
                'thì tròn chín giờ.']),
        _c('y_toan', 'Quá nửa vòng thì thử đọc kiểu KÉM',
           '60 − 55 = 5, mượn tên giờ sắp tới', buoc=1, soBuoc=2,
           loi=['Quá nửa vòng thì con thử đọc kiểu kém. Lấy sáu mươi trừ số phút, rồi '
                'mượn tên giờ sắp tới.']),
        _c('day_so', 'Tờ lịch thì chạy nhịp 7', so=[6, 13, 20, 27],
           hienThuTu=False, chuPhu='Cùng một cột dọc là cùng thứ, cách nhau 7 ngày.',
           loi=['Tờ lịch thì chạy nhịp bảy. Các ngày cùng một cột dọc là cùng thứ.',
                'Chúng cách nhau đúng bảy ngày, lại là đoàn tàu đếm thêm quen thuộc.']),
        _c('y_toan', 'Nên biết một ngày là suy ra ngày khác',
           'Thứ Ba ngày 8  →  ngày 22 cách 14 ngày = 2 tuần tròn  →  cũng thứ Ba',
           buoc=2, soBuoc=2,
           loi=['Hôm nay thứ ba ngày tám. Ngày hai mươi hai cách mười bốn ngày, '
                'đúng hai tuần tròn, nên cũng là thứ ba.']),
        _c('cong_thuc', 'Hai nhịp phải nhớ',
           congThuc='mặt đồng hồ: mỗi số 5 phút   ·   tờ lịch: mỗi cột 7 ngày',
           thay='đếm số trên mặt đồng hồ như đếm phút là sai gấp năm lần',
           loi=['Con nhớ hai nhịp. Trên mặt đồng hồ mỗi số đáng năm phút, còn trên tờ '
                'lịch mỗi cột cách nhau bảy ngày.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_can_va_dong(b):
    """L3·C8② Gam, mi-li-lít, và luật cùng phe trên cân hai đĩa."""
    return [
        _c('bia', 'Cân nặng và lượng nước', so_bai(b),
           loi=['Hai thứ đo bằng hai đơn vị khác nhau, và không cộng được với nhau.']),
        _c('y_toan', 'Cầu nối vạn năng mang tên một nghìn',
           '1 kg = 1000 g     ·     1 l = 1000 ml', buoc=1, soBuoc=3,
           loi=['Cầu nối mang tên một nghìn. Một ki lô gam bằng một nghìn gam, một '
                'lít bằng một nghìn mi li lít.']),
        _c('y_toan', 'Cỡ nào thì hình dung ra được',
           'Quả trứng ~50 g  ·  gói mì ~75 g  ·  ca nước 250 ml',
           loi=['Con hình dung cỡ cho quen. Quả trứng chừng năm mươi gam.',
                'Một ca nước chừng hai trăm năm mươi mi li lít, bốn ca là tròn một '
                'lít.']),
        _c('de_toan', 'Đề bài', de='Chai 1 lít, rót ra cốc hết 350 ml. Trong chai còn mấy ml?',
           loi=['Chai nước ngọt chứa một lít, rót ra cốc hết ba trăm năm mươi mi li '
                'lít.',
                'Hỏi trong chai còn lại bao nhiêu mi li lít.']),
        _c('y_toan', 'Đổi về CÙNG đơn vị trước đã',
           '1 l = 1000 ml  →  1000 − 350 = 650 (ml)', buoc=2, soBuoc=3,
           loi=['Đổi về cùng đơn vị trước đã. Một lít là một nghìn mi li lít.',
                'Một nghìn trừ ba trăm năm mươi, còn sáu trăm năm mươi mi li lít.']),
        _c('y_toan', 'Cân hai đĩa: quả cân đứng ở phe nào?',
           'bột + 50 = 500  →  bột = 500 − 50 = 450 (g)', buoc=3, soBuoc=3,
           loi=['Cân thăng bằng nghĩa là hai đĩa nặng bằng nhau.',
                'Quả cân năm mươi gam đứng cùng phe với bột, đang gánh hộ, nên phải '
                'trừ ra. Bột nặng bốn trăm năm mươi gam.']),
        _c('y_toan', 'Chỗ hỏng nặng nhất',
           '400 g + 100 ml — hai thứ khác loại, KHÔNG cộng được',
           loi=['Đây là chỗ hỏng nặng nhất. Bốn trăm gam cộng một trăm mi li lít.',
                'Gam là cân nặng, mi li lít là lượng nước. Hai thứ khác loại thì không '
                'cộng được.']),
        _c('cong_thuc', 'Ba điều phải nhớ',
           congThuc='cầu nối 1000  ·  quả cân cùng phe thì TRỪ  ·  khác loại thì đừng cộng',
           thay='vì con số cộng ra từ hai loại khác nhau không mang nghĩa gì cả',
           loi=['Con nhớ ba điều. Cầu nối là một nghìn, quả cân cùng phe thì trừ ra.',
                'Và hai thứ khác loại thì đừng cộng, vì con số ra không mang nghĩa gì '
                'cả.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb3_tien_va_lai(b):
    """L3·C8③ Vốn, bán, lãi — và tiền trong hộp chưa phải lãi."""
    return [
        _c('bia', 'Bán hàng thì lãi bao nhiêu', so_bai(b),
           loi=['Hộp tiền đầy chưa chắc đã lãi nhiều. Phải trừ vốn đã.']),
        _c('y_toan', 'Cùng một số tiền, nhiều bộ áo khác nhau',
           '1 tờ 10 nghìn = 2 tờ 5 nghìn = 10 tờ 1 nghìn', buoc=1, soBuoc=3,
           loi=['Cùng một số tiền mà nhiều cách đổi. Một tờ mười nghìn bằng hai tờ '
                'năm nghìn, hay mười tờ một nghìn.']),
        _c('y_toan', 'Trả tiền thừa cũng là một phép trừ',
           'Đưa 20 nghìn, mua cốc 8 nghìn  →  trả lại 12 nghìn',
           loi=['Trả tiền thừa cũng chỉ là một phép trừ. Đưa hai mươi nghìn, mua cốc '
                'tám nghìn, trả lại mười hai nghìn.']),
        _c('de_toan', 'Đề bài',
           de='Vốn 24 nghìn, pha 8 cốc, bán 5 nghìn một cốc. Buổi bán hàng lãi mấy nghìn?',
           loi=['Bỏ vốn hai mươi tư nghìn, pha được tám cốc, bán năm nghìn một cốc.',
                'Hỏi buổi bán hàng lãi bao nhiêu nghìn đồng.']),
        _c('y_toan', 'Ba dòng sổ, đừng lẫn',
           'VỐN bỏ ra  ·  BÁN thu về  ·  LÃI là phần thực sự kiếm được',
           buoc=2, soBuoc=3,
           loi=['Ba dòng sổ, con đừng lẫn. Vốn là tiền bỏ ra lúc đầu.',
                'Bán là toàn bộ tiền thu về. Còn lãi mới là phần thực sự kiếm được.']),
        _c('y_toan', 'Tính tiền bán trước', '5 × 8 = 40 (nghìn đồng)',
           loi=['Tính tiền bán trước. Năm nghìn một cốc, tám cốc, được bốn mươi nghìn '
                'đồng.']),
        _c('cong_thuc', 'Rồi mới ra lãi',
           congThuc='LÃI = BÁN − VỐN = 40 − 24 = 16 (nghìn đồng)',
           thay='vì hộp tiền đang giữ cả phần vốn mình bỏ ra lúc đầu',
           loi=['Rồi mới ra lãi. Lãi bằng bán trừ vốn, bốn mươi trừ hai mươi tư, được '
                'mười sáu nghìn đồng.',
                'Vì hộp tiền đang giữ cả phần vốn mình bỏ ra lúc đầu.']),
        _c('y_toan', 'Muốn biết mỗi cốc lãi bao nhiêu thì rút về một',
           'vốn mỗi cốc 24 : 8 = 3  →  mỗi cốc lãi 5 − 3 = 2 nghìn',
           buoc=3, soBuoc=3,
           loi=['Muốn biết mỗi cốc lãi bao nhiêu thì rút về một cốc. Vốn mỗi cốc là '
                'ba nghìn, bán năm nghìn, nên lãi hai nghìn.']),
        _c('cong_thuc', 'Nhớ một câu thôi',
           congThuc='LÃI = BÁN − VỐN',
           thay='và hễ thấy chữ MỖI thì tay với ngay phép chia',
           loi=['Con nhớ một câu thôi. Lãi bằng bán trừ vốn.',
                'Và hễ thấy chữ mỗi thì tay với ngay phép chia.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LỚP 5 QUYỂN 1 · bài 1 — BA MICRO ĐẦU TIÊN (bài mẫu)
# ═══════════════════════════════════════════════════════════════════════════
# Lớp 5 khác ba quyển kia ở bốn chỗ, phải nhớ trước khi viết tiếp:
#
#   ① 56 bài lớn × 3 micro = 168 micro, mỗi micro là một buổi học riêng có hook,
#      có phần giảng, có câu chốt của nó. Nên MỘT VIDEO MỘT MICRO, không gộp.
#   ② Mỗi micro đã có sẵn khối `videoSpec` viết tay trong sách: 840 cảnh, trung
#      bình 87 giây. Đó là NGUỒN quý — nhịp dạy và số liệu đã có — nhưng KHÔNG
#      dùng thẳng được: nó viết cho video dọc 9:16 có hoạt hình, 363/840 cảnh có
#      từ `TU_CAM` cấm, 191 cảnh gọi tên nhân vật, và 532/840 câu dài quá 130 chữ.
#      Nên đọc `videoSpec` để lấy Ý, rồi viết lại theo luật của mình.
#   ③ Chặng giảng của lớp 5 có thêm bước `check` — một CÂU HỎI tương tác, không
#      phải màn chữ. Video thay hook và hai màn giảng và màn câu chốt, nhưng
#      PHẢI GIỮ `check` lại.
#   ④ Mỗi micro khai 4 hình; hình `mantra` (F3) chưa từng hiện lên kể từ ngày dựng
#      vì bước `mantra` không mang khoá hình nào — 168 hình chết, dọn theo luôn.


def kb5_ban_do_cac_hang(b):
    """L5·B1·M1 Bản đồ các hàng của số thập phân."""
    return [
        _c('bia', 'Bản đồ các hàng', so_bai(b),
           loi=['Số thập phân là hai dãy nhà hai bên dấu phẩy.']),
        _c('de_toan', 'Câu hỏi mở đầu', de='3,05 với 3,5 — một số hay hai số?',
           loi=['Ba phẩy không năm với ba phẩy năm. Một số hay hai số khác nhau.']),
        _c('y_toan', 'Dấu phẩy là cái cổng',
           'trái cổng: đơn vị · chục · trăm   ·   phải cổng: phần mười · phần trăm',
           buoc=1, soBuoc=3,
           loi=['Dấu phẩy là cái cổng. Bên trái cổng là đơn vị, chục, trăm.',
                'Bên phải cổng là phần mười, phần trăm, phần nghìn.']),
        _c('y_toan', 'Mỗi bước sang phải, giá trị nhỏ đi 10 lần',
           'đơn vị  →  phần mười  →  phần trăm  →  phần nghìn', buoc=2, soBuoc=3,
           loi=['Cứ mỗi bước sang phải thì giá trị nhỏ đi mười lần.']),
        _c('y_toan', 'Tách số là viết thành tổng theo hàng',
           '35,46 = 30 + 5 + 0,4 + 0,06',
           loi=['Tách số là viết nó thành tổng giá trị của từng hàng.',
                'Ba mươi lăm phẩy bốn sáu bằng ba mươi, cộng năm, cộng không phẩy '
                'bốn, cộng không phẩy không sáu.']),
        _c('y_toan', 'Chiều ngược cũng phải thạo',
           '3 chục · 5 đơn vị · 4 phần mười · 6 phần trăm  →  35,46', buoc=3, soBuoc=3,
           loi=['Chiều ngược cũng phải thạo. Ba chục, năm đơn vị, bốn phần mười, sáu '
                'phần trăm, ghép lại thành ba mươi lăm phẩy bốn sáu.']),
        _c('y_toan', 'Số 0 ở CUỐI thì bỏ được', '3,50 = 3,5 — giá trị không đổi',
           loi=['Số không ở cuối phần thập phân thì bỏ được. Ba phẩy năm mươi đúng '
                'bằng ba phẩy năm.']),
        _c('y_toan', 'Nhưng số 0 ở GIỮA thì đang giữ chỗ',
           '3,05 bỏ số 0 đi thành 3,5 — sai hẳn thành số khác',
           loi=['Nhưng số không ở giữa thì đang giữ chỗ cho một hàng.',
                'Ba phẩy không năm mà bỏ số không đi là thành ba phẩy năm, sai hẳn '
                'thành số khác.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='0 ở ĐUÔI thì rụng  ·  0 ở GIỮA thì giữ chỗ',
           thay='vì số 0 ở giữa đang giữ một hàng, nhấc nó ra là mọi hàng sau dồn lên',
           loi=['Con nhớ câu này. Số không ở đuôi thì rụng, số không ở giữa thì giữ '
                'chỗ.',
                'Vì nhấc nó ra là mọi hàng phía sau dồn lên một bậc.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_cung_chu_so_khac_hang(b):
    """L5·B1·M2 Cùng chữ số, khác hàng thì khác giá trị."""
    return [
        _c('bia', 'Cùng chữ số mà khác giá trị', so_bai(b),
           loi=['Cùng một chữ số, đứng hai hàng khác nhau thì đáng khác nhau xa.']),
        _c('de_toan', 'Câu hỏi mở đầu',
           de='Chữ số 8 trong 84,6 và chữ số 8 trong 4,68 — bằng nhau không?',
           loi=['Chữ số tám trong tám mươi tư phẩy sáu, và chữ số tám trong bốn phẩy '
                'sáu tám.',
                'Cùng mặt chữ số, nhưng có bằng nhau không.']),
        _c('tach_so', 'Chữ số 8 thứ nhất đứng hàng chục', so='84,6', sang=[1],
           phep='đáng 80', chuPhu='Nó ở bên trái dấu phẩy, hàng chục.',
           loi=['Chữ số tám thứ nhất đứng ở hàng chục, nên nó đáng tám mươi.']),
        _c('tach_so', 'Chữ số 8 thứ hai đứng hàng phần trăm', so='4,68', sang=[3],
           phep='đáng 0,08', chuPhu='Nó ở bên phải dấu phẩy, hàng phần trăm.',
           loi=['Chữ số tám thứ hai đứng ở hàng phần trăm, nên nó chỉ đáng không phẩy '
                'không tám.']),
        _c('y_toan', 'Nghi thức ba bước', 'DỊCH ra giá trị  →  SO  →  CHIA kiểm chứng',
           buoc=1, soBuoc=3,
           loi=['Nghi thức ba bước. Dịch ra giá trị theo hàng, rồi mới so, rồi chia '
                'để kiểm chứng.']),
        _c('y_toan', 'Chia để kiểm chứng', '80 : 0,08 = 1000 lần', buoc=2, soBuoc=3,
           loi=['Lấy giá trị lớn chia giá trị bé. Tám mươi chia không phẩy không tám '
                'bằng một nghìn lần.']),
        _c('y_toan', 'Đếm BƯỚC NHẢY, đừng đếm căn hộ',
           'chục → đơn vị → phần mười → phần trăm: 3 bước  →  1000 lần',
           buoc=3, soBuoc=3,
           loi=['Cách đếm cho nhanh. Từ hàng chục sang hàng phần trăm là ba bước nhảy.',
                'Ba bước thì hơn kém nhau một nghìn lần. Con đếm bước, đừng đếm căn '
                'hộ.']),
        _c('tach_so', 'Bẫy kinh điển', so='2,73', sang=[2],
           phep='chữ số 7 đáng 0,7 — KHÔNG phải 7',
           chuPhu='Nó đang ở hàng phần mười.',
           loi=['Đây là bẫy kinh điển. Hỏi giá trị chữ số bảy trong hai phẩy bảy ba.',
                'Nhiều bạn trả lời bảy. Sai. Nó đang ở hàng phần mười nên chỉ đáng '
                'không phẩy bảy.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='KHÔNG so chữ số  ·  chỉ so GIÁ TRỊ THEO HÀNG',
           thay='vì mặt chữ số không nói lên gì, chỗ đứng mới quyết định',
           loi=['Con nhớ câu này. Đừng so chữ số, chỉ so giá trị theo hàng.',
                'Vì mặt chữ số không nói lên gì cả, chỗ nó đứng mới quyết định.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_so_gap_k_lan_tong(b):
    """L5·B1·M3 Số hai chữ số gấp k lần tổng các chữ số."""
    return [
        _c('bia', 'Số gấp mấy lần tổng chữ số của nó', so_bai(b),
           loi=['Tìm số có hai chữ số gấp bốn lần tổng các chữ số của nó.']),
        _c('de_toan', 'Đề bài', de='Tìm số có 2 chữ số gấp 4 lần tổng các chữ số',
           loi=['Tìm số có hai chữ số gấp bốn lần tổng các chữ số của nó.',
                'Có bạn thử được số hai mươi tư, đúng. Nhưng đã tìm hết chưa.']),
        _c('cong_thuc', 'Khai triển số hai chữ số ra đã',
           congThuc='số ab = 10 × a + b',
           thay='vì a đứng hàng chục nên nó mang theo mười lần chính nó',
           loi=['Khai triển số hai chữ số ra đã. Số a b bằng mười nhân a, cộng b.',
                'Vì a đứng hàng chục nên nó mang theo mười lần chính nó.']),
        _c('y_toan', 'Dịch đề thành một cái cân', '10a + b = 4 × (a + b)',
           buoc=1, soBuoc=3,
           loi=['Dịch đề thành một cái cân. Vế trái mười a cộng b, vế phải bốn lần '
                'a cộng b.']),
        _c('y_toan', 'Dọn cân: bớt đều hai vế', '10a + b − 4a − b = 6a = 3b',
           buoc=2, soBuoc=3,
           loi=['Dọn cân bằng cách bớt đều hai vế, còn lại sáu a bằng ba b.']),
        _c('y_toan', 'Rút gọn thành quan hệ đơn giản', 'b = 2a', buoc=3, soBuoc=3,
           loi=['Rút gọn cho ba, được b bằng hai a. Chữ số hàng đơn vị gấp đôi chữ '
                'số hàng chục.']),
        _c('day_so', 'Điểm danh cho ĐỦ, đừng bắt được một số đã nghỉ',
           so=[12, 24, 36, 48], hienThuTu=False,
           chuPhu='a = 1, 2, 3, 4. Tới a = 5 thì b = 10, vượt quá 9 nên dừng.',
           loi=['Nay điểm danh cho đủ. Mười hai, hai mươi tư, ba mươi sáu, bốn mươi '
                'tám.',
                'Tới a bằng năm thì b thành mười, vượt quá chín nên dừng lại.']),
        _c('y_toan', 'Thử lại một số cho chắc',
           '48 có tổng chữ số 12, mà 12 × 4 = 48 ✓',
           loi=['Thử lại một số cho chắc. Bốn mươi tám có tổng chữ số là mười hai.',
                'Mười hai nhân bốn đúng bằng bốn mươi tám.']),
        _c('cong_thuc', 'Bốn nhịp của dạng này',
           congThuc='khai triển 10a + b  →  dọn cân  →  điểm danh đủ  →  thử lại',
           thay='ném nguyên cụm ab lên cân mà quên phần mười a là sai từ gốc',
           loi=['Con nhớ bốn nhịp. Khai triển, dọn cân, điểm danh cho đủ, rồi thử lại.',
                'Ném nguyên cụm a b lên cân mà quên phần mười a là sai ngay từ gốc.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_chuyen_nha(b):
    """L5·B2·M1 Xóa một chữ số thì cả dãy chuyển nhà."""
    return [
        _c('bia', 'Xóa một chữ số, cả dãy chuyển nhà', so_bai(b),
           loi=['Xóa một chữ số khỏi số, thì các chữ số còn lại không đứng yên đâu.']),
        _c('de_toan', 'Câu hỏi mở đầu', de='Xóa chữ số 4 khỏi 345 thì còn số nào?',
           loi=['Xóa chữ số bốn khỏi ba trăm bốn mươi lăm thì còn số nào.',
                'Nhiều bạn trả lời ngay ba trăm bốn mươi mốt. Con thử nghĩ lại.']),
        _c('tach_so', 'Số cũ: mỗi chữ số ở một hàng', so='345', sang=[2],
           phep='3 trăm · 4 chục · 5 đơn vị',
           chuPhu='Chữ số 4 đang đứng giữa.',
           loi=['Số cũ có ba trăm, bốn chục, năm đơn vị. Chữ số bốn đứng ở giữa.']),
        _c('tach_so', 'Rút chữ số 4 ra — chữ số 3 TỤT HÀNG', so='35', sang=[1],
           phep='3 chục · 5 đơn vị = 35',
           chuPhu='Chữ số 3 từ hàng trăm tụt xuống hàng chục.',
           loi=['Rút chữ số bốn ra thì chữ số ba tụt hàng ngay.',
                'Từ hàng trăm xuống hàng chục, nó chỉ còn đáng ba chục. Số mới là ba '
                'mươi lăm.']),
        _c('y_toan', 'Nên số giảm rất nhiều, không phải giảm 4',
           '345 − 35 = 310, chứ không phải 4', buoc=1, soBuoc=3,
           loi=['Nên số giảm những ba trăm mười, chứ không phải giảm bốn.',
                'Vì mất một chỗ đứng thì mọi chữ số bên trái đều tụt xuống một hàng.']),
        _c('cong_thuc', 'Thêm bên phải: cả dãy dọn sang trái',
           congThuc='số mới = số cũ × 10 + c',
           thay='vì chữ số mới chiếm hàng đơn vị, đẩy mọi chữ số cũ lên một hàng',
           loi=['Thêm chữ số vào bên phải thì cả dãy dọn sang trái. Lấy số cũ nhân '
                'mười rồi cộng chữ số mới.']),
        _c('y_toan', 'Thêm bên trái: không ai phải dọn',
           'số mới = số cũ + c × giá của hàng mới', buoc=2, soBuoc=3,
           loi=['Thêm vào bên trái thì không ai phải dọn nhà. Chỉ cộng thêm phần của '
                'người mới.']),
        _c('y_toan', 'Xóa chữ số TẬN CÙNG', 'số mới = (số cũ − c) : 10',
           buoc=3, soBuoc=3,
           loi=['Xóa chữ số tận cùng thì trừ nó ra rồi chia mười, vì cả dãy tụt xuống '
                'một hàng.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='tính bằng HIỆU hai số  ·  đừng trừ chữ số',
           thay='vì xóa một chữ số là đổi CHỖ ĐỨNG của mọi chữ số bên trái nó',
           loi=['Con nhớ câu này. Tính bằng hiệu của hai số, đừng trừ chữ số.',
                'Vì xóa một chữ số là đổi chỗ đứng của mọi chữ số bên trái nó.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_cong_tac_dau_phay(b):
    """L5·B2·M2 Bỏ dấu phẩy là nhân 10 mũ k."""
    return [
        _c('bia', 'Bỏ dấu phẩy thì gấp mấy lần', so_bai(b),
           loi=['Bỏ dấu phẩy đi thì số gấp lên. Nhưng gấp mấy lần mới đúng.']),
        _c('de_toan', 'Câu hỏi mở đầu', de='Bỏ dấu phẩy của 3,45 — gấp 10 lần?',
           loi=['Bỏ dấu phẩy của ba phẩy bốn lăm. Có phải gấp mười lần không.']),
        _c('tach_so', 'Đếm trước đã: sau dấu phẩy có mấy chữ số?', so='3,45',
           sang=[2, 3], phep='2 chữ số',
           chuPhu='Nghi thức hai giây — đếm rồi mới nhân.',
           loi=['Nghi thức hai giây. Đếm trước khi nhân.',
                'Sau dấu phẩy của ba phẩy bốn lăm có hai chữ số.']),
        _c('y_toan', 'Nên bỏ phẩy là nhân MỘT TRĂM',
           '3,45  →  345, gấp 100 lần', buoc=1, soBuoc=3,
           loi=['Nên bỏ phẩy là nhân một trăm. Ba phẩy bốn lăm thành ba trăm bốn mươi '
                'lăm.']),
        _c('cong_thuc', 'Luật chung',
           congThuc='phẩy cõng k chữ số  →  bỏ phẩy là nhân 10 mũ k',
           thay='vì mỗi chữ số vượt qua cổng phẩy là nó lên một hàng',
           loi=['Luật chung. Phẩy cõng mấy chữ số thì bỏ phẩy là nhân bấy nhiêu lần '
                'mười.',
                'Vì mỗi chữ số vượt qua cổng phẩy là nó lên một hàng.']),
        _c('y_toan', 'Số 0 ở đuôi có HAI thế giới',
           'đuôi số tự nhiên  ·  đuôi phần thập phân', buoc=2, soBuoc=3,
           loi=['Còn số không ở đuôi thì có hai thế giới khác hẳn nhau.']),
        _c('tach_so', 'Thêm 0 vào đuôi SỐ TỰ NHIÊN: gấp 10 lần', so='470', sang=[3],
           phep='47  →  470', chuPhu='Cả hai chữ số cũ đều lên một hàng.',
           loi=['Thêm số không vào đuôi số tự nhiên thì gấp mười. Bốn mươi bảy thành '
                'bốn trăm bảy mươi.']),
        _c('tach_so', 'Thêm 0 vào đuôi PHẦN THẬP PHÂN: y nguyên', so='3,50',
           sang=[3], phep='3,5 = 3,50', chuPhu='Số 0 này chỉ đứng trang trí.',
           loi=['Nhưng thêm số không vào đuôi phần thập phân thì số y nguyên.',
                'Ba phẩy năm bằng ba phẩy năm mươi. Số không ấy chỉ đứng trang trí.']),
        _c('cong_thuc', 'Hai câu, đừng lẫn',
           congThuc='phẩy cõng k chữ số → × 10 mũ k  ·  0 đuôi thập phân → y nguyên',
           thay='vì bên trái phẩy thì thêm 0 là chiếm chỗ, bên phải thì không',
           loi=['Con nhớ hai câu, đừng lẫn. Phẩy cõng mấy chữ số thì nhân bấy nhiêu '
                'lần mười.',
                'Còn số không ở đuôi phần thập phân thì số cũ y nguyên.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_chia_chin_khong_chia_muoi(b):
    """L5·B2·M3 Bài ngược — phần tăng là 9 lần, không phải 10."""
    return [
        _c('bia', 'Biết phần tăng, tìm số cũ', so_bai(b),
           loi=['Đề cho biết số tăng thêm bao nhiêu, hỏi ngược lại số cũ.']),
        _c('de_toan', 'Đề bài', de='Bỏ dấu phẩy làm một số TĂNG THÊM 32,4. Số cũ là số nào?',
           loi=['Bỏ mất dấu phẩy làm một số tăng thêm ba mươi hai phẩy bốn đơn vị.',
                'Hỏi số cũ là số nào. Nhiều bạn chia ngay cho mười. Sai.']),
        _c('so_do_doan', 'Vẽ ra thì thấy ngay', be=1, lon=10,
           nhanBe='số cũ · 1 phần', nhanLon='số mới · 10 phần',
           hienHieu=True, chuHieu='phần tăng = 9 phần',
           chuPhu='Số mới gấp 10 lần, nên phần TĂNG THÊM chỉ là 9 lần.',
           loi=['Vẽ ra thì thấy ngay. Số cũ là một phần, số mới gấp mười nên là mười '
                'phần.',
                'Phần tăng thêm là mười phần trừ một phần, còn chín phần.']),
        _c('cong_thuc', 'Nên phải chia cho 9',
           congThuc='số cũ = phần tăng : 9',
           thay='vì mười lần trừ một lần thì còn chín lần, không phải mười',
           loi=['Nên phải chia cho chín. Vì mười lần trừ đi một lần thì còn chín lần.']),
        _c('y_toan', 'Phá án', '32,4 : 9 = 3,6', buoc=1, soBuoc=3,
           loi=['Ba mươi hai phẩy bốn chia chín, bằng ba phẩy sáu.']),
        _c('y_toan', 'Thử lại — dựng lại hiện trường',
           '3,6 bỏ phẩy thành 36 · 36 − 3,6 = 32,4 ✓', buoc=2, soBuoc=3,
           loi=['Thử lại. Ba phẩy sáu bỏ phẩy thành ba mươi sáu.',
                'Ba mươi sáu trừ ba phẩy sáu, đúng bằng ba mươi hai phẩy bốn.']),
        _c('y_toan', 'Số có HAI chữ số thập phân thì khác',
           'gấp 100 lần  →  phần tăng là 99 lần  →  chia 99', buoc=3, soBuoc=3,
           loi=['Số có hai chữ số thập phân thì bỏ phẩy là gấp một trăm.',
                'Phần tăng thành chín mươi chín lần, nên phải chia cho chín mươi '
                'chín.']),
        _c('y_toan', 'Chỗ hay hỏng', 'Chia cho 10 hay 100 là sai — phải chia 9 hay 99',
           loi=['Đây là chỗ hay hỏng. Chia cho mười hay một trăm là sai.',
                'Phần tăng luôn ít hơn số mới đúng một lần số cũ.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='mười lần trừ một lần — còn CHÍN lần',
           thay='đề cho PHẦN TĂNG thì chia 9 hoặc 99, đề cho SỐ MỚI mới chia 10',
           loi=['Con nhớ câu này. Mười lần trừ một lần còn chín lần.',
                'Đề cho phần tăng thì chia chín. Đề cho số mới thì mới chia mười.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_ba_cong_thuc_guong(b):
    """L5·B3·M1 Tổng ăn 11, hiệu ăn 9, ba chữ số hiệu ăn 99."""
    return [
        _c('bia', 'Số và số viết ngược', so_bai(b),
           loi=['Lấy một số hai chữ số rồi viết ngược nó lại. Cộng và trừ hai số ấy.']),
        _c('de_toan', 'Thử với số 47', de='47 + 74 = 121   ·   74 − 47 = 27',
           loi=['Thử với số bốn mươi bảy. Viết ngược thành bảy mươi tư.',
                'Cộng lại được một trăm hai mươi mốt, trừ nhau được hai mươi bảy.']),
        _c('y_toan', 'Khai triển theo hàng đã', 'ab = 10a + b   ·   ba = 10b + a',
           buoc=1, soBuoc=3,
           loi=['Khai triển theo hàng đã. Số a b là mười a cộng b.',
                'Còn số viết ngược là mười b cộng a.']),
        _c('y_toan', 'Cộng lại rồi gom nhóm',
           '10a + b + 10b + a = 11a + 11b = 11 × (a + b)', buoc=2, soBuoc=3,
           loi=['Gom nhóm lại. Mười a với a thành mười một a, b với mười b thành '
                'mười một b.',
                'Nên tổng luôn chia hết cho mười một.']),
        _c('y_toan', 'Trừ nhau thì ra số 9',
           '10a + b − 10b − a = 9a − 9b = 9 × (a − b)', buoc=3, soBuoc=3,
           loi=['Trừ nhau thì ra số chín. Nên hiệu luôn chia hết cho chín.']),
        _c('tach_so', 'Số ba chữ số: chữ số GIỮA triệt tiêu', so='abc', sang=[2],
           phep='abc − cba = 99 × (a − c)',
           chuPhu='Chữ số giữa soi gương vẫn là chính nó.',
           loi=['Với số ba chữ số thì chữ số ở giữa soi gương vẫn là chính nó, nên nó '
                'triệt tiêu.',
                'Còn lại chín mươi chín lần hiệu của hai chữ số đầu và cuối.']),
        _c('y_toan', 'Thử lại bằng số thật', '121 : 11 = 11 ✓   ·   27 : 9 = 3 ✓',
           loi=['Thử lại bằng số thật. Một trăm hai mươi mốt chia mười một được mười '
                'một.',
                'Hai mươi bảy chia chín được ba. Đúng cả hai.']),
        _c('cong_thuc', 'Ba công thức, một cách chứng minh',
           congThuc='tổng ăn 11  ·  hiệu ăn 9  ·  ba chữ số hiệu ăn 99',
           thay='cả ba đều ra từ một việc: khai triển theo hàng rồi gom nhóm',
           loi=['Con nhớ ba công thức. Tổng ăn mười một, hiệu ăn chín, ba chữ số thì '
                'hiệu ăn chín mươi chín.',
                'Cả ba đều ra từ một việc thôi, là khai triển theo hàng rồi gom '
                'nhóm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_guong_vo(b):
    """L5·B3·M2 Tìm số từ tổng hoặc hiệu — coi chừng số tận cùng 0."""
    return [
        _c('bia', 'Tìm số từ tổng với bóng gương', so_bai(b),
           loi=['Đề cho tổng của một số với số viết ngược, hỏi số ấy là số nào.']),
        _c('de_toan', 'Đề bài', de='Tổng của số và số viết ngược bằng 66. Tìm số đó.',
           loi=['Tổng của một số hai chữ số và số viết ngược của nó bằng sáu mươi '
                'sáu.']),
        _c('y_toan', 'Dùng ngay công thức bài trước', '66 : 11 = 6, nên a + b = 6',
           buoc=1, soBuoc=3,
           loi=['Dùng ngay công thức bài trước. Tổng chia mười một được sáu.',
                'Nghĩa là hai chữ số cộng lại bằng sáu.']),
        _c('day_so', 'Duyệt hết các cặp có tổng 6', so=[15, 24, 33, 42, 51, 60],
           hienThuTu=False, chuPhu='Sáu số — nhưng có một số không hợp lệ.',
           loi=['Duyệt hết các cặp có tổng bằng sáu. Được sáu số.',
                'Nhưng trong đó có một số không hợp lệ.']),
        _c('y_toan', 'Soi gương số 51', '51  →  15, hai chữ số ✓',
           loi=['Soi gương số năm mươi mốt được mười lăm. Vẫn là số hai chữ số, hợp '
                'lệ.']),
        _c('y_toan', 'Nhưng soi gương số 60 thì VỠ',
           '60  →  06, mà 06 chỉ là số 6 — mất một chữ số', buoc=3, soBuoc=3,
           loi=['Nhưng soi gương số sáu mươi thì vỡ. Nó thành không sáu.',
                'Mà không sáu chỉ là số sáu, đâu còn là số hai chữ số nữa. Nên loại '
                'số sáu mươi.']),
        _c('y_toan', 'Bài HIỆU làm y hệt, chỉ đổi số chia',
           'hiệu 45 : 9 = 5  →  61, 72, 83, 94 — và loại 50',
           loi=['Bài hiệu làm y hệt, chỉ đổi số chia. Bốn mươi lăm chia chín được năm.',
                'Ra sáu mốt, bảy hai, tám ba, chín tư. Còn số năm mươi thì loại, vì '
                'soi gương lại vỡ.']),
        _c('cong_thuc', 'Điều kiện ẩn phải ghi ngay từ đầu',
           congThuc='số tận cùng 0  →  soi gương là VỠ, loại ngay',
           thay='vì bóng gương cũng phải là số có đủ chữ số như số gốc',
           loi=['Con nhớ điều kiện ẩn này, ghi vào tóm tắt ngay từ đầu.',
                'Số tận cùng bằng không thì soi gương là vỡ, phải loại.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_hai_ho_dau_hieu(b):
    """L5·B3·M3 Đổi chỗ chữ số: họ tổng bình an, họ tận cùng khám lại."""
    return [
        _c('bia', 'Viết ngược thì còn chia hết không', so_bai(b),
           loi=['Một số chia hết cho vài số. Viết ngược nó lại thì còn chia hết không.']),
        _c('de_toan', 'Đề bài', de='18 chia hết cho 9 và cho 2. Viết ngược thành 81 thì sao?',
           loi=['Số mười tám chia hết cho chín và cho hai.',
                'Viết ngược thành tám mươi mốt thì còn chia hết cho những số nào.']),
        _c('y_toan', 'Chẻ câu hỏi làm HAI HỌ trước đã',
           'họ TỔNG: 3 và 9   ·   họ TẬN CÙNG: 2 và 5', buoc=1, soBuoc=3,
           loi=['Con chẻ câu hỏi làm hai họ trước đã.',
                'Họ tổng gồm số ba và số chín. Họ tận cùng gồm số hai và số năm.']),
        _c('tach_so', 'Họ TỔNG chỉ nhìn tổng các chữ số', so='18', sang=[1, 2],
           phep='1 + 8 = 9', chuPhu='Đổi chỗ thì tổng ấy KHÔNG đổi.',
           loi=['Họ tổng chỉ nhìn tổng các chữ số. Một cộng tám bằng chín.',
                'Đổi chỗ hai chữ số thì tổng ấy không đổi chút nào.']),
        _c('tach_so', 'Nên 81 vẫn chia hết cho 9', so='81', sang=[1, 2],
           phep='8 + 1 = 9 — vẫn thế', chuPhu='Họ tổng: CHẮC CHẮN còn chia hết.',
           loi=['Nên tám mươi mốt vẫn chia hết cho chín. Họ tổng thì chắc chắn còn.']),
        _c('tach_so', 'Nhưng họ TẬN CÙNG nhìn chữ số cuối', so='81', sang=[2],
           phep='đuôi là 1 — số lẻ', chuPhu='18 đuôi 8 chia hết cho 2, còn 81 thì không.',
           loi=['Nhưng họ tận cùng chỉ nhìn chữ số cuối. Mười tám có đuôi tám nên chia '
                'hết cho hai.',
                'Còn tám mươi mốt đuôi là một, số lẻ, hết chia hết cho hai.']),
        _c('y_toan', 'Nên trả lời phải khác nhau',
           'họ tổng: "chắc chắn còn"   ·   họ tận cùng: "chưa chắc, phải khám lại"',
           loi=['Nên hai họ phải trả lời khác nhau. Họ tổng thì nói chắc chắn còn.',
                'Họ tận cùng thì nói chưa chắc, phải khám lại từng số một.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='đổi chỗ  →  họ TỔNG bình an  ·  họ TẬN CÙNG khám lại',
           thay='vì đổi chỗ không đụng tổng, nhưng có thể đổi hẳn chữ số cuối',
           loi=['Con nhớ câu này. Đổi chỗ thì họ tổng bình an, họ tận cùng phải khám '
                'lại.',
                'Vì đổi chỗ không đụng tới tổng, nhưng có thể đổi hẳn chữ số cuối.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_thang_may_dau_phay(b):
    """L5·B4·M1 Nhân chia cho 10·100·1000 — đếm bậc rồi đệm 0."""
    return [
        _c('bia', 'Dấu phẩy đi thang máy', so_bai(b),
           loi=['Nhân hay chia cho mười, một trăm, một nghìn thì dấu phẩy dịch chỗ.']),
        _c('y_toan', 'Đếm BẬC trước, rồi mới cho thang chạy',
           'nhân/chia cho 10 mũ k  →  đúng k bậc', buoc=1, soBuoc=3,
           loi=['Nghi thức: đếm bậc trước rồi mới cho thang chạy.',
                'Nhân hay chia cho mười mũ mấy thì đi đúng bấy nhiêu bậc.']),
        _c('tach_so', 'Nhân thì phẩy chạy sang PHẢI', so='34,5',
           phep='3,45 × 10 = 34,5', chuPhu='Một bậc sang phải.',
           loi=['Nhân thì phẩy chạy sang phải. Ba phẩy bốn lăm nhân mười thành ba '
                'mươi tư phẩy năm.']),
        _c('tach_so', 'Hết chữ số bên phải thì thêm 0 vào đuôi', so='3450',
           sang=[4], phep='3,45 × 1000 = 3450', chuPhu='Ba bậc — bậc cuối phải thêm 0.',
           loi=['Ba phẩy bốn lăm nhân một nghìn là ba bậc. Nhưng bên phải chỉ còn hai '
                'chữ số.',
                'Hết phòng thì xây thêm một phòng số không, được ba nghìn bốn trăm '
                'năm mươi.']),
        _c('tach_so', 'Chia thì phẩy chạy sang TRÁI', so='0,35',
           phep='3,5 : 10 = 0,35', chuPhu='Một bậc sang trái.',
           loi=['Chia thì phẩy chạy sang trái. Ba phẩy năm chia mười thành không phẩy '
                'ba lăm.']),
        _c('tach_so', 'Thiếu bậc bên trái thì ĐỆM 0 vào trước', so='0,035',
           sang=[2], phep='3,5 : 100 = 0,035',
           chuPhu='Hai bậc — bậc thứ hai phải đệm thêm một số 0.',
           loi=['Ba phẩy năm chia một trăm là hai bậc. Đi được một bậc thì hết chữ '
                'số.',
                'Thiếu bậc thì đệm thêm số không vào trước, được không phẩy không ba '
                'lăm.']),
        _c('y_toan', 'Chỗ hay hỏng', 'Hết chữ số rồi DỪNG GIỮA CHỪNG là sai',
           loi=['Đây là chỗ hay hỏng. Đi được một bậc, hết chữ số rồi dừng lại luôn.',
                'Thang máy phải đi đủ số bậc, không được dừng giữa chừng.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='đếm bậc  →  chạy đủ bậc  →  thiếu chỗ thì ĐỆM 0',
           thay='vì mỗi bậc là một hàng, bỏ dở một bậc là sai hẳn mười lần',
           loi=['Con nhớ ba nhịp. Đếm bậc, chạy đủ bậc, thiếu chỗ thì đệm số không.',
                'Vì mỗi bậc là một hàng, bỏ dở một bậc là sai hẳn mười lần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_quen_phay_khi_cong(b):
    """L5·B4·M2 Quên dấu phẩy khi cộng — tổng tăng 9 lần số hạng."""
    return [
        _c('bia', 'Quên dấu phẩy khi cộng', so_bai(b),
           loi=['Cộng hai số mà quên dấu phẩy của một số hạng, tổng vọt lên.']),
        _c('de_toan', 'Đề bài', de='Quên phẩy một số hạng làm TỔNG tăng thêm 76,5. Số hạng đó là số nào?',
           loi=['Quên dấu phẩy của một số hạng làm tổng tăng thêm bảy mươi sáu phẩy '
                'năm.',
                'Hỏi số hạng ấy là số nào.']),
        _c('so_do_doan', 'Dựng lại hiện trường bằng sơ đồ', be=1, lon=10,
           nhanBe='số hạng thật · 1 phần', nhanLon='số bị quên phẩy · 10 phần',
           hienHieu=True, chuHieu='phần phình = 9 phần',
           chuPhu='Cả 9 phần phình ấy đổ trọn vào tổng.',
           loi=['Dựng lại hiện trường. Số hạng thật là một phần, quên phẩy làm nó '
                'phình thành mười phần.',
                'Chín phần phình ấy đổ trọn vào tổng.']),
        _c('cong_thuc', 'Nên tìm số hạng thì chia 9',
           congThuc='số hạng = mức lệch : 9',
           thay='vì tổng chỉ tăng bằng PHẦN PHÌNH, không tăng bằng cả số mới',
           loi=['Nên muốn tìm số hạng thì lấy mức lệch chia chín.',
                'Vì tổng chỉ tăng bằng phần phình thôi, không tăng bằng cả số mới.']),
        _c('y_toan', 'Phá án', '76,5 : 9 = 8,5', buoc=1, soBuoc=3,
           loi=['Bảy mươi sáu phẩy năm chia chín, bằng tám phẩy năm.']),
        _c('y_toan', 'Thử lại', '8,5 quên phẩy thành 85 · 85 − 8,5 = 76,5 ✓',
           buoc=2, soBuoc=3,
           loi=['Thử lại. Tám phẩy năm quên phẩy thành tám mươi lăm.',
                'Tám mươi lăm trừ tám phẩy năm, đúng bằng bảy mươi sáu phẩy năm.']),
        _c('y_toan', 'Số hạng có HAI chữ số thập phân thì chia 99',
           'quên phẩy làm nó gấp 100 lần  →  phần phình là 99 phần',
           buoc=3, soBuoc=3,
           loi=['Số hạng có hai chữ số thập phân thì quên phẩy làm nó gấp một trăm '
                'lần.',
                'Phần phình thành chín mươi chín phần, nên phải chia chín mươi chín.']),
        _c('y_toan', 'Có khi đề chưa cho sẵn mức lệch',
           'mức lệch = tổng nhầm − tổng đúng — tính nó trước đã',
           loi=['Có khi đề chưa cho sẵn mức lệch. Con lấy tổng nhầm trừ tổng đúng để '
                'tìm nó trước đã.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='mười lần trừ một lần — còn CHÍN lần',
           thay='đề cho MỨC LỆCH thì chia 9 hoặc 99, đừng chia 10 hay 100',
           loi=['Con nhớ câu này. Mười lần trừ một lần còn chín lần.',
                'Đề cho mức lệch thì chia chín, đừng chia mười.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_quen_phay_khi_tru(b):
    """L5·B4·M3 Quên dấu phẩy trong phép trừ — hai chiều ngược nhau."""
    return [
        _c('bia', 'Quên dấu phẩy trong phép trừ', so_bai(b),
           loi=['Cũng là quên một dấu phẩy, nhưng trong phép trừ thì có hai vụ khác '
                'hẳn nhau.']),
        _c('y_toan', 'Gọi đúng tên hai số trước đã',
           'hiệu = SỐ BỊ TRỪ − SỐ TRỪ', buoc=1, soBuoc=3,
           loi=['Gọi đúng tên hai số trước đã. Số bị trừ đứng trước dấu trừ, số trừ '
                'đứng sau.']),
        _c('so_do_doan', 'Vụ A — phình ở SỐ TRỪ', be=1, lon=10,
           nhanBe='số trừ thật', nhanLon='số trừ bị phình',
           hienHieu=True, chuHieu='trừ đi nhiều hơn 9 phần',
           chuPhu='Trừ đi nhiều hơn, nên HIỆU TỤT XUỐNG.',
           loi=['Vụ thứ nhất, phình ở số trừ. Trừ đi nhiều hơn chín phần.',
                'Nên hiệu tụt xuống, giảm đi chín lần số trừ thật.']),
        _c('so_do_doan', 'Vụ B — phình ở SỐ BỊ TRỪ', be=1, lon=10,
           nhanBe='số bị trừ thật', nhanLon='số bị trừ bị phình',
           hienHieu=True, chuHieu='có nhiều hơn 9 phần',
           chuPhu='Có nhiều hơn để trừ, nên HIỆU VỌT LÊN.',
           loi=['Vụ thứ hai, phình ở số bị trừ. Có nhiều hơn chín phần để mà trừ.',
                'Nên hiệu vọt lên, tăng thêm chín lần số bị trừ thật.']),
        _c('y_toan', 'Hai vụ, hai chiều ngược hẳn nhau',
           'phình SỐ TRỪ → hiệu giảm   ·   phình SỐ BỊ TRỪ → hiệu tăng',
           buoc=3, soBuoc=3,
           loi=['Hai vụ, hai chiều ngược hẳn nhau. Cùng là quên một dấu phẩy đấy.']),
        _c('y_toan', 'Làm thử vụ A', 'số trừ 6,3 phình thành 63 · hiệu giảm 56,7',
           loi=['Làm thử vụ thứ nhất. Số trừ sáu phẩy ba phình thành sáu mươi ba.',
                'Hiệu giảm đi sáu mươi ba trừ sáu phẩy ba, tức năm mươi sáu phẩy '
                'bảy.']),
        _c('y_toan', 'Nên trước khi tính, vẽ hiện trường ra',
           'viết hiệu = bị trừ − trừ  →  khoanh chỗ bị phình  →  mới kết luận',
           loi=['Nên trước khi tính, con vẽ hiện trường ra. Viết hiệu bằng số bị trừ '
                'trừ số trừ.',
                'Khoanh tròn chỗ bị phình, rồi mới kết luận hiệu tăng hay giảm.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='phình TRƯỚC dấu trừ → hiệu vọt lên  ·  phình SAU → hiệu tụt xuống',
           thay='vì số bị trừ đẩy hiệu lên, còn số trừ kéo hiệu xuống',
           loi=['Con nhớ câu này. Phình trước dấu trừ thì hiệu vọt lên, phình sau thì '
                'hiệu tụt xuống.',
                'Vì số bị trừ đẩy hiệu lên, còn số trừ kéo hiệu xuống.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_xep_doi_hinh(b):
    """L5·B5·M1 Lập số lớn nhất, nhỏ nhất — và luật hàng đầu."""
    return [
        _c('bia', 'Xếp thẻ thành số lớn nhất, nhỏ nhất', so_bai(b),
           loi=['Có bộ thẻ số. Xếp thế nào cho được số lớn nhất, số nhỏ nhất.']),
        _c('de_toan', 'Bộ thẻ', de='Bốn thẻ: 0 · 3 · 5 · 8',
           loi=['Bốn tấm thẻ mang các chữ số không, ba, năm, tám.']),
        _c('tach_so', 'Số LỚN NHẤT — xếp giảm dần từ hàng cao', so='8530',
           sang=[1], phep='8 · 5 · 3 · 0',
           chuPhu='Thẻ to nhất chiếm hàng cao nhất, rồi to nhì, to ba.',
           loi=['Số lớn nhất thì xếp giảm dần. Thẻ to nhất chiếm hàng cao nhất, rồi '
                'to nhì, to ba.']),
        _c('y_toan', 'Số NHỎ NHẤT thì KHÔNG làm ngược y hệt',
           'Xếp tăng dần được 0358 — mà số 0 không được đứng đầu', buoc=1, soBuoc=3,
           loi=['Số nhỏ nhất thì không làm ngược y hệt được.',
                'Xếp tăng dần thì số không đứng đầu, mà số không không được đứng '
                'đầu.']),
        _c('tach_so', 'Vì số 0 cầm đầu thì đội hình RỤNG một người', so='358',
           phep='0358 đọc lên chỉ là 358',
           chuPhu='Đang là số 4 chữ số, hoá thành số 3 chữ số.',
           loi=['Vì không ba năm tám đọc lên chỉ là ba trăm năm mươi tám.',
                'Đang là số bốn chữ số, hoá thành số ba chữ số. Sai đề.']),
        _c('tach_so', 'Nên số nhỏ nhất xếp thế này', so='3058', sang=[1, 2],
           phep='thẻ bé nhất KHÁC 0 dẫn đầu · số 0 chen ngay sau',
           chuPhu='Rồi các thẻ còn lại xếp tăng dần.',
           loi=['Nên thẻ bé nhất khác không dẫn đầu, số không chen ngay sau nó.',
                'Các thẻ còn lại xếp tăng dần, được ba nghìn không trăm năm mươi '
                'tám.']),
        _c('y_toan', 'Còn một cụm từ phải gạch chân ngay khi đọc đề',
           '"bốn chữ số KHÁC NHAU"   ·   "ĐƯỢC PHÉP LẶP"', buoc=3, soBuoc=3,
           loi=['Còn một cụm từ phải gạch chân ngay khi đọc đề.',
                'Bốn chữ số khác nhau, hay được phép lặp. Hai đề, hai thế giới.',
                'Được phép lặp thì thẻ to nhất phủ mọi hàng, thành tám nghìn tám trăm '
                'tám mươi tám.']),
        _c('cong_thuc', 'Hai câu cần nhớ',
           congThuc='số 0 cầm đầu → đội hình rụng một người',
           thay='và luôn hỏi đề: các chữ số KHÁC NHAU hay ĐƯỢC LẶP?',
           loi=['Con nhớ hai câu. Số không cầm đầu thì đội hình rụng một người.',
                'Và luôn hỏi đề xem các chữ số phải khác nhau hay được phép lặp.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_lap_so_chia_het(b):
    """L5·B5·M2 Lập số chia hết — đuôi có mấy nhánh thì tính đủ."""
    return [
        _c('bia', 'Lập số mà phải chia hết', so_bai(b),
           loi=['Lập số từ bộ thẻ, nhưng số ấy còn phải chia hết cho một số nữa.']),
        _c('de_toan', 'Đề bài',
           de='Thẻ 0·2·5·7·9 — số NHỎ NHẤT 4 chữ số khác nhau, chia hết cho 5',
           loi=['Từ năm thẻ không, hai, năm, bảy, chín.',
                'Lập số nhỏ nhất có bốn chữ số khác nhau và chia hết cho năm.']),
        _c('y_toan', 'Chia hết cho 5 thuộc họ TẬN CÙNG',
           'nên chốt chữ số ĐUÔI trước, rồi mới xếp phần đầu', buoc=1, soBuoc=3,
           loi=['Chia hết cho năm thuộc họ tận cùng, nên chốt chữ số đuôi trước đã.',
                'Đuôi phải là không hoặc năm. Có hai nhánh.']),
        _c('tach_so', 'Nhánh 1 — đuôi là 0', so='2570', sang=[4],
           phep='phần đầu xếp tăng dần: 2 · 5 · 7',
           chuPhu='Được số 2570.',
           loi=['Nhánh thứ nhất, đuôi là không. Phần đầu xếp tăng dần, được hai nghìn '
                'năm trăm bảy mươi.']),
        _c('tach_so', 'Nhánh 2 — đuôi là 5, số 0 quay về phần đầu', so='2075',
           sang=[2, 4], phep='thẻ 2 dẫn đội · số 0 chen ngay sau',
           chuPhu='Được số 2075 — nhỏ hơn nhánh 1.',
           loi=['Nhánh thứ hai, đuôi là năm. Số không quay về phần đầu.',
                'Nó không được dẫn đội nên chen ngay sau thẻ hai, được hai nghìn không '
                'trăm bảy mươi lăm. Nhỏ hơn nhánh trước.']),
        _c('y_toan', 'Chốt vội một nhánh là mất đáp số',
           'Đuôi có 2 nhánh thì phải tính đủ 2, rồi mới so', buoc=3, soBuoc=3,
           loi=['Chốt vội một nhánh là mất đáp số. Đuôi có mấy nhánh thì tính đủ bấy '
                'nhiêu, rồi mới so chọn.']),
        _c('y_toan', 'Chia hết cho 9 thì họ TỔNG chỉ huy từ vòng chọn thẻ',
           'thẻ 1·2·3·5·8 tổng 19 — bỏ thẻ 1 còn 18, chia hết 9 ✓',
           loi=['Còn chia hết cho chín thì họ tổng chỉ huy ngay từ vòng chọn thẻ.',
                'Năm thẻ có tổng mười chín. Thử bỏ từng thẻ, bỏ thẻ một thì còn mười '
                'tám, chia hết cho chín.']),
        _c('cong_thuc', 'Hai họ, hai chỗ ra lệnh',
           congThuc='họ TẬN CÙNG quyết ĐUÔI  ·  họ TỔNG quyết BỘ THẺ',
           thay='vì tổng không đổi khi xếp lại, còn đuôi thì đổi theo cách xếp',
           loi=['Con nhớ hai họ ra lệnh ở hai chỗ khác nhau.',
                'Họ tận cùng quyết chữ số đuôi, còn họ tổng quyết cả bộ thẻ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_dieu_kien_kep(b):
    """L5·B5·M3 Điều kiện kép — họ tổng trước, họ tận cùng sau."""
    return [
        _c('bia', 'Hai điều kiện cùng lúc', so_bai(b),
           loi=['Đề đòi hai điều kiện cùng lúc. Làm điều nào trước mới đúng.']),
        _c('de_toan', 'Đề bài',
           de='Thẻ 0·2·3·4·7 — chọn 4 thẻ, lập số LỚN NHẤT vừa chẵn vừa chia hết cho 9',
           loi=['Từ năm thẻ không, hai, ba, bốn, bảy, chọn bốn thẻ.',
                'Lập số lớn nhất vừa chẵn vừa chia hết cho chín.']),
        _c('y_toan', 'Thứ tự vàng', 'họ TỔNG trước  →  họ TẬN CÙNG sau',
           buoc=1, soBuoc=3,
           loi=['Thứ tự vàng. Họ tổng trước, họ tận cùng sau.',
                'Vì họ tổng quyết bộ thẻ, mà chưa có bộ thẻ thì chốt đuôi làm gì.']),
        _c('y_toan', 'Trạm 1 — họ TỔNG soát bộ thẻ',
           'tổng 5 thẻ = 16 · bỏ thẻ 7 còn 9 — chia hết cho 9 ✓', buoc=2, soBuoc=3,
           loi=['Trạm một, họ tổng soát bộ thẻ. Tổng năm thẻ là mười sáu.',
                'Thử bỏ từng thẻ. Bỏ thẻ bảy thì còn chín, chia hết cho chín.',
                'Vậy bộ thẻ là không, hai, ba, bốn.']),
        _c('y_toan', 'Trạm 2 — điều kiện CHẴN mở ba nhánh đuôi',
           'đuôi 0  ·  đuôi 2  ·  đuôi 4', buoc=3, soBuoc=3,
           loi=['Trạm hai, điều kiện chẵn mở ba nhánh đuôi. Đuôi không, đuôi hai, đuôi '
                'bốn.']),
        _c('day_so', 'Tính đủ cả ba nhánh rồi mới so', so=[4320, 4302, 3240],
           hienThuTu=False, chuPhu='Lớn nhất là 4320.',
           loi=['Tính đủ cả ba nhánh rồi mới so. Bốn nghìn ba trăm hai mươi là lớn '
                'nhất.']),
        _c('y_toan', 'Làm ngược thứ tự thì hỏng ở đâu?',
           'Chốt đuôi trước, rồi mới soát tổng — dễ tuyển nhầm bộ thẻ',
           loi=['Làm ngược thứ tự thì dễ tuyển nhầm bộ thẻ, rồi phải quay lại từ '
                'đầu.']),
        _c('cong_thuc', 'Và một mẹo gộp',
           congThuc='vừa chia hết 2 vừa chia hết 5  →  tận cùng bằng 0',
           thay='hai lệnh gộp thành một, khỏi phải đi hai nhánh',
           loi=['Còn một mẹo gộp. Vừa chia hết cho hai vừa chia hết cho năm thì tận '
                'cùng phải bằng không.',
                'Hai lệnh gộp thành một, khỏi phải đi hai nhánh.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_quy_tac_nhan(b):
    """L5·B6·M1 Đếm số lập được — nhân dọc, và hàng đầu cấm thẻ 0."""
    return [
        _c('bia', 'Lập được bao nhiêu số', so_bai(b),
           loi=['Không phải lập ra số nào, mà đếm xem lập được tất cả bao nhiêu số.']),
        _c('de_toan', 'Đề bài', de='Thẻ 0·3·5·8 — lập được mấy số 3 chữ số? (được lặp)',
           loi=['Từ bốn thẻ không, ba, năm, tám. Lập được bao nhiêu số có ba chữ số.',
                'Các chữ số được phép lặp lại.']),
        _c('y_toan', 'Mỗi hàng là một chỗ phải điền',
           'hàng trăm  ·  hàng chục  ·  hàng đơn vị', buoc=1, soBuoc=3,
           loi=['Mỗi hàng là một chỗ phải điền. Ba hàng, ba chỗ.']),
        _c('y_toan', 'Nhiều bạn nhân ngay 4 × 4 × 4 = 64',
           'Nhưng hàng trăm KHÔNG được nhận thẻ 0', buoc=2, soBuoc=3,
           loi=['Nhiều bạn nhân ngay bốn nhân bốn nhân bốn, được sáu mươi tư.',
                'Nhưng hàng trăm không được nhận thẻ không.']),
        _c('tach_so', 'Vì thẻ 0 đứng đầu thì số rụng một chữ số', so='058',
           sang=[1], phep='058 chỉ là 58',
           chuPhu='Đang là số 3 chữ số, hoá thành số 2 chữ số.',
           loi=['Vì không năm tám đọc lên chỉ là năm mươi tám. Số rụng mất một chữ '
                'số.']),
        _c('cong_thuc', 'Nên hàng đầu ít hơn đúng một lựa chọn',
           congThuc='3 × 4 × 4 = 48 số',
           thay='hàng trăm chỉ có 3 thẻ dùng được, hai hàng sau đủ cả 4',
           loi=['Nên hàng trăm chỉ có ba thẻ dùng được, hai hàng sau đủ cả bốn.',
                'Ba nhân bốn nhân bốn, được bốn mươi tám số.']),
        _c('y_toan', 'Đối chứng: bộ thẻ KHÔNG có số 0',
           'thẻ 1·2·3·4  →  4 × 4 × 4 = 64 số', buoc=3, soBuoc=3,
           loi=['Đối chứng với bộ thẻ một, hai, ba, bốn. Bộ này không có thẻ không.',
                'Hàng đầu đủ bốn lựa chọn, nên được sáu mươi tư số.',
                'Cùng bốn thẻ mà hai bộ cho hai kết quả khác nhau.']),
        _c('cong_thuc', 'Nghi thức mở bài đếm',
           congThuc='viết dòng "hàng đầu: … cách (đã bỏ thẻ 0)"  rồi mới nhân',
           thay='vì chỗ hỏng duy nhất của dạng này nằm đúng ở hàng đầu',
           loi=['Con nhớ nghi thức. Viết dòng hàng đầu có mấy cách, đã bỏ thẻ không '
                'chưa, rồi mới nhân.',
                'Vì chỗ hỏng duy nhất của dạng này nằm đúng ở hàng đầu.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_kho_the_voi_dan(b):
    """L5·B6·M2 Chữ số khác nhau — kho thẻ vơi dần theo hàng."""
    return [
        _c('bia', 'Khi đề đòi các chữ số KHÁC NHAU', so_bai(b),
           loi=['Đề thêm một dòng: các chữ số phải khác nhau. Cách đếm đổi hẳn.']),
        _c('de_toan', 'Đề bài', de='Thẻ 0·3·5·8 — mấy số 3 chữ số KHÁC NHAU?',
           loi=['Vẫn bốn thẻ ấy, nhưng nay các chữ số phải khác nhau.']),
        _c('y_toan', 'Mỗi thẻ chỉ dùng MỘT lần',
           'nên chọn xong hàng nào, kho vơi đi một thẻ cho hàng sau',
           buoc=1, soBuoc=3,
           loi=['Mỗi thẻ chỉ dùng được một lần. Chọn xong hàng nào thì kho vơi đi một '
                'thẻ cho hàng sau.']),
        _c('y_toan', 'Hàng trăm: 3 cách', 'bỏ thẻ 0 — còn 3 · 5 · 8',
           loi=['Hàng trăm vẫn ba cách, vì phải bỏ thẻ không ra.']),
        _c('y_toan', 'Hàng chục: cũng 3 cách — nghe lạ mà đúng',
           'kho vơi một thẻ đã dùng, NHƯNG thẻ 0 được trả tự do', buoc=2, soBuoc=3,
           loi=['Hàng chục cũng ba cách. Nghe lạ mà đúng.',
                'Kho vơi một thẻ vừa dùng, nhưng thẻ không nay được trả tự do vì nó '
                'không còn đứng đầu.']),
        _c('cong_thuc', 'Hàng đơn vị còn 2 — nhân dọc là xong',
           congThuc='3 × 3 × 2 = 18 số',
           thay='dãy thừa số GIẢM DẦN chính là dấu hiệu của đề "khác nhau"',
           loi=['Hàng đơn vị còn hai thẻ. Ba nhân ba nhân hai, được mười tám số.']),
        _c('y_toan', 'Mẹo đọc ngược: nhìn dãy thừa số biết ngay đề',
           '3 × 4 × 4 — các hàng sau BẰNG NHAU → được lặp', buoc=3, soBuoc=3,
           loi=['Có mẹo đọc ngược. Nhìn dãy thừa số là biết đề nào.',
                'Ba nhân bốn nhân bốn, các hàng sau bằng nhau, là đề được lặp.']),
        _c('y_toan', 'Còn dãy giảm dần thì là đề "khác nhau"',
           '3 × 3 × 2 — giảm dần từng nấc',
           loi=['Còn ba nhân ba nhân hai, giảm dần từng nấc, là đề các chữ số khác '
                'nhau.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='mỗi thẻ một lần  →  kho vơi theo hàng',
           thay='và thẻ 0 được tự do từ hàng thứ hai trở đi',
           loi=['Con nhớ câu này. Mỗi thẻ một lần thì kho vơi theo hàng.',
                'Và thẻ không được tự do từ hàng thứ hai trở đi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_dem_co_dieu_kien(b):
    """L5·B6·M3 Đếm có điều kiện — khác luật thì phải tách nhánh."""
    return [
        _c('bia', 'Đếm khi có thêm điều kiện', so_bai(b),
           loi=['Đề đòi đếm, mà số lập ra còn phải chẵn nữa.']),
        _c('de_toan', 'Đề bài', de='Thẻ 0·3·5·8 — mấy số CHẴN 3 chữ số khác nhau?',
           loi=['Từ bốn thẻ không, ba, năm, tám. Đếm xem có mấy số chẵn ba chữ số khác '
                'nhau.']),
        _c('y_toan', 'Cho hàng KHÓ TÍNH chọn trước',
           'đuôi phải chẵn: chỉ có thẻ 0 hoặc thẻ 8', buoc=1, soBuoc=3,
           loi=['Cho hàng khó tính chọn trước. Đuôi phải chẵn nên chỉ có thẻ không '
                'hoặc thẻ tám.']),
        _c('y_toan', 'Nhánh 1 — đuôi là thẻ 0', 'hàng trăm 3 · hàng chục 2  →  6 số',
           buoc=2, soBuoc=3,
           loi=['Nhánh thứ nhất, đuôi là thẻ không. Thẻ không đã bị giam ở đuôi rồi.',
                'Nên hàng trăm có ba cách, hàng chục còn hai. Được sáu số.']),
        _c('y_toan', 'Nhánh 2 — đuôi là thẻ 8', 'hàng trăm chỉ 2 · hàng chục 2  →  4 số',
           buoc=3, soBuoc=3,
           loi=['Nhánh thứ hai, đuôi là thẻ tám. Nay thẻ không còn ở trong kho.',
                'Nhưng nó không được đứng đầu, nên hàng trăm chỉ hai cách. Được bốn '
                'số.']),
        _c('y_toan', 'Cộng hai nhánh lại', '6 + 4 = 10 số',
           loi=['Cộng hai nhánh lại được mười số.']),
        _c('y_toan', 'Vì sao KHÔNG nhân gộp một lần?',
           'Hai nhánh cho hàng trăm hai luật khác nhau: 3 cách và 2 cách',
           loi=['Vì sao không nhân gộp một lần cho nhanh.',
                'Vì hai nhánh cho hàng trăm hai luật khác nhau, ba cách và hai cách.',
                'Nhân gộp là lấy một luật áp cho cả hai, sai ngay.']),
        _c('cong_thuc', 'Thứ tự vàng, và luật tách nhánh',
           congThuc='hàng RÀNG BUỘC trước  →  hàng ĐẦU  →  các hàng dễ sau',
           thay='cùng luật mới nhân chung, khác luật thì phải tách nhánh rồi cộng',
           loi=['Con nhớ thứ tự vàng. Hàng ràng buộc chọn trước, rồi tới hàng đầu, '
                'rồi các hàng dễ.',
                'Cùng luật mới nhân chung. Khác luật thì phải tách nhánh rồi cộng '
                'lại.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_hang_rao_coc(b):
    """L5·B7·M1 Số số hạng dãy cách đều — chia ra khoảng, cộng 1 ra cọc."""
    return [
        _c('bia', 'Đếm số hạng của dãy cách đều', so_bai(b),
           loi=['Một dãy số cách đều nhau. Đếm xem nó có bao nhiêu số.']),
        _c('de_toan', 'Đề bài', de='Rào từ mét số 3 đến mét số 99, cứ 3 m một cọc. Mấy cọc?',
           loi=['Rào từ mét số ba đến mét số chín mươi chín, cứ ba mét một cọc.',
                'Nhiều bạn tính chín mươi chín trừ ba, chia ba, được ba mươi hai cọc.']),
        _c('luoi_cham', 'Thu nhỏ lại mà đếm cho chắc', hang=1, cot=4,
           chuPhu='4 cọc — nhưng chỉ 3 khoảng ở giữa.',
           loi=['Thu nhỏ lại mà đếm cho chắc. Bốn cọc thì chỉ có ba khoảng ở giữa.',
                'Cọc luôn đông hơn khoảng đúng một.']),
        _c('y_toan', 'Phép chia chỉ đếm được KHOẢNG',
           '(cuối − đầu) : khoảng cách  →  ra số KHOẢNG, chưa phải số cọc',
           buoc=1, soBuoc=3,
           loi=['Phép chia ấy chỉ đếm được số khoảng, chưa phải số cọc.']),
        _c('cong_thuc', 'Nên phải cộng thêm 1',
           congThuc='số số hạng = (cuối − đầu) : khoảng + 1',
           thay='vì cọc luôn nhiều hơn khoảng đúng một — hàng rào nào cũng thế',
           loi=['Nên phải cộng thêm một. Số số hạng bằng cuối trừ đầu, chia khoảng '
                'cách, rồi cộng một.']),
        _c('y_toan', 'Làm lại đề trên cho đúng',
           '(99 − 3) : 3 + 1 = 32 + 1 = 33 cọc', buoc=2, soBuoc=3,
           loi=['Làm lại đề trên. Chín mươi chín trừ ba, chia ba, được ba mươi hai.',
                'Cộng một, được ba mươi ba cọc.']),
        _c('y_toan', 'Thử một đề nữa', 'số chẵn từ 1 đến 50: (50 − 2) : 2 + 1 = 25',
           buoc=3, soBuoc=3,
           loi=['Thử một đề nữa. Các số chẵn từ một đến năm mươi là dãy hai, bốn, và '
                'cứ thế.',
                'Năm mươi trừ hai, chia hai, cộng một, được hai mươi lăm số.']),
        _c('cong_thuc', 'Ba nhịp, đừng thiếu nhịp nào',
           congThuc='tính HIỆU  →  chia KHOẢNG  →  cộng 1',
           thay='thiếu nhịp ba là đếm hụt đúng một số hạng, lần nào cũng thế',
           loi=['Con nhớ ba nhịp. Tính hiệu, chia khoảng, rồi cộng một.',
                'Thiếu nhịp ba là đếm hụt đúng một số hạng, lần nào cũng thế.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_tu_khac_giua(b):
    """L5·B7·M2 Đếm số chia hết trong đoạn — dò đầu cuối thật, và "từ" khác "giữa"."""
    return [
        _c('bia', 'Đếm số chia hết trong một đoạn', so_bai(b),
           loi=['Trong một đoạn số, đếm xem có mấy số chia hết cho một số cho trước.']),
        _c('y_toan', 'Dãy ấy cũng cách đều, nên dùng lại công thức cũ',
           'nhưng phải tìm ĐẦU THẬT và CUỐI THẬT trước đã', buoc=1, soBuoc=3,
           loi=['Dãy các số chia hết cũng cách đều, nên dùng lại công thức bài trước.',
                'Nhưng phải tìm số đầu thật và số cuối thật đã.']),
        _c('day_so', 'Đầu thật không phải lúc nào cũng là mép đoạn',
           so=[12, 15, 18, 21], hienThuTu=False,
           chuPhu='Từ 10 đến 100, đếm số chia hết cho 3: mép là 10 nhưng đầu thật là 12.',
           loi=['Đầu thật không phải lúc nào cũng là mép đoạn.',
                'Từ mười đến một trăm mà đếm số chia hết cho ba, thì mười trượt, mười '
                'một trượt, mười hai mới là số đầu thật.']),
        _c('de_toan', 'Hai đề chỉ khác nhau MỘT chữ',
           de='TỪ 10 đến 100   ·   GIỮA 10 và 100',
           loi=['Nay xem hai đề chỉ khác nhau một chữ. Từ mười đến một trăm, và giữa '
                'mười và một trăm.']),
        _c('y_toan', 'Đề "TỪ" thì hai mép được ở lại',
           '10 và 100 đều chia hết 5  →  đầu 10, cuối 100  →  19 số',
           buoc=2, soBuoc=3,
           loi=['Đề từ thì hai mép được ở lại nếu chúng thoả điều kiện.',
                'Mười và một trăm đều chia hết cho năm, nên đếm được mười chín số.']),
        _c('y_toan', 'Đề "GIỮA" thì đuổi cả hai mép',
           'dù chúng có thoả  →  đầu 15, cuối 95  →  17 số', buoc=3, soBuoc=3,
           loi=['Đề giữa thì đuổi cả hai mép, dù chúng có thoả điều kiện đi nữa.',
                'Nên đầu thật là mười lăm, cuối thật là chín mươi lăm, đếm được mười '
                'bảy số.']),
        _c('y_toan', 'Một chữ lệch, hai đáp số', '19 số  ·  17 số',
           loi=['Một chữ lệch mà ra hai đáp số khác nhau.']),
        _c('cong_thuc', 'Nghi thức đọc đề',
           congThuc='khoanh tròn chữ TỪ / GIỮA ngay khi đọc',
           thay='từ thì giữ hai đầu, giữa thì đuổi cả đôi',
           loi=['Con khoanh tròn chữ từ hay giữa ngay khi đọc đề.',
                'Từ thì giữ hai đầu, giữa thì đuổi cả đôi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_dem_hoac(b):
    """L5·B7·M3 Đếm "hoặc" — trừ phần giao, và phép đếm ngược."""
    return [
        _c('bia', 'Đếm "chia hết cho a HOẶC cho b"', so_bai(b),
           loi=['Đếm những số chia hết cho số này hoặc chia hết cho số kia.']),
        _c('de_toan', 'Đề bài', de='Từ 1 đến 30, mấy số chia hết cho 2 HOẶC cho 3?',
           loi=['Từ một đến ba mươi, có mấy số chia hết cho hai hoặc chia hết cho ba.',
                'Nhiều bạn cộng luôn mười lăm với mười, được hai mươi lăm.']),
        _c('so_do_ven', 'Vẽ hai vòng ra thì thấy ngay',
           tenA='chia hết 2', tenB='chia hết 3', caHai='5',
           chuGiao='6 · 12 · 18 · 24 · 30 — chia hết cho CẢ HAI',
           chuPhu='Năm số này đứng ở phần giao.',
           loi=['Vẽ hai vòng ra thì thấy ngay. Có năm số chia hết cho cả hai.',
                'Chúng đứng ở chỗ hai vòng ôm nhau.']),
        _c('y_toan', 'Năm số ấy bị điểm danh HAI lần',
           'một lần ở hàng chia hết 2, một lần ở hàng chia hết 3', buoc=1, soBuoc=3,
           loi=['Năm số ấy bị điểm danh hai lần. Một lần ở hàng chia hết cho hai, một '
                'lần ở hàng chia hết cho ba.']),
        _c('so_do_ven', 'Nên phải trả lại một lần',
           tenA='chia hết 2', tenB='chia hết 3', chiA='10', caHai='5', chiB='5',
           chuGiao='15 + 10 − 5 = 20 số',
           chuPhu='Ba vùng cộng lại: 10 + 5 + 5 = 20.',
           loi=['Nên phải trả lại một lần. Mười lăm cộng mười, trừ năm, được hai mươi '
                'số.',
                'Cộng ba vùng cũng ra hai mươi.']),
        _c('cong_thuc', 'Công thức đếm "hoặc"',
           congThuc='hoặc = A + B − (cả hai)',
           thay='vì ai đứng cả hai hàng đều bị đếm hai lần',
           loi=['Công thức đếm hoặc. Lấy nhóm thứ nhất cộng nhóm thứ hai, trừ nhóm cả '
                'hai.']),
        _c('y_toan', 'Đếm "KHÔNG chia hết" thì đếm NGƯỢC cho nhanh',
           'từ 1 đến 100: 100 − 33 = 67 số không chia hết cho 3', buoc=3, soBuoc=3,
           loi=['Còn đếm những số không chia hết thì đếm ngược cho nhanh.',
                'Từ một đến một trăm có ba mươi ba số chia hết cho ba.',
                'Lấy một trăm trừ ba mươi ba, còn sáu mươi bảy số không chia hết.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='ai đứng hai hàng — chỉ được điểm danh MỘT lần',
           thay='và đếm xuôi khó thì đếm ngược: cả sân trừ đi phần không cần',
           loi=['Con nhớ câu này. Ai đứng hai hàng thì chỉ được điểm danh một lần.',
                'Và đếm xuôi khó thì đếm ngược, lấy cả sân trừ đi phần không cần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_danh_trang_xuoi(b):
    """L5·B8·M1 Đếm chữ số đánh trang — ba vùng và hai mốc vàng."""
    return [
        _c('bia', 'Đánh số trang tốn bao nhiêu chữ số', so_bai(b),
           loi=['Dán số cho từng trang một cuốn sách. Tốn bao nhiêu chữ số dán.']),
        _c('de_toan', 'Đề bài', de='Cuốn sách 256 trang cần bao nhiêu chữ số?',
           loi=['Cuốn sách hai trăm năm mươi sáu trang cần bao nhiêu chữ số dán.']),
        _c('y_toan', 'Chia sách làm BA vùng',
           'trang 1–9  ·  trang 10–99  ·  trang 100 trở lên', buoc=1, soBuoc=3,
           loi=['Chia sách làm ba vùng, vì mỗi vùng dùng thẻ dán khác cỡ.']),
        _c('y_toan', 'Hai mốc vàng phải thuộc lòng',
           'hết trang 9: 9 chữ số   ·   hết trang 99: 189 chữ số', buoc=2, soBuoc=3,
           loi=['Hai mốc vàng phải thuộc lòng. Hết trang chín là chín chữ số.',
                'Vùng hai có chín mươi trang, mỗi trang hai chữ số. Nên hết trang chín '
                'mươi chín là một trăm tám mươi chín.']),
        _c('y_toan', 'Vùng ba đếm bằng công thức đoạn',
           'từ 100 đến 256: (256 − 100) + 1 = 157 trang', buoc=3, soBuoc=3,
           loi=['Vùng ba đếm bằng công thức đoạn của bài trước, được một trăm năm '
                'mươi bảy trang.']),
        _c('cong_thuc', 'Ghép lại thành đáp số',
           congThuc='189 + 157 × 3 = 189 + 471 = 660 chữ số',
           thay='mỗi trang vùng ba tốn ba chữ số, cộng vào mốc 189',
           loi=['Ghép lại. Một trăm năm bảy trang nhân ba, được bốn trăm bảy mươi '
                'mốt.',
                'Cộng mốc một trăm tám mươi chín, được sáu trăm sáu mươi chữ số.']),
        _c('tach_so', 'Bẫy ranh giới', so='100', sang=[1, 2, 3],
           phep='trang 100 đã tốn BA chữ số',
           chuPhu='Cửa ngăn giữa các vùng nằm ở 9 và 99, không ở số tròn.',
           loi=['Đây là bẫy ranh giới. Trang một trăm đã tốn ba chữ số rồi.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='ranh giới vùng ở 9 – 99 – 999, KHÔNG ở số tròn',
           thay='vì trang 100 đã là cư dân đầu tiên của vùng ba chữ số',
           loi=['Con nhớ câu này. Ranh giới vùng nằm ở chín, chín mươi chín, chín trăm '
                'chín mươi chín.',
                'Không nằm ở số tròn, vì trang một trăm đã là cư dân của vùng ba chữ '
                'số.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_danh_trang_nguoc(b):
    """L5·B8·M2 Biết số chữ số, tìm số trang — trừ vùng, chia, cộng mốc."""
    return [
        _c('bia', 'Biết số chữ số, tìm số trang', so_bai(b),
           loi=['Đề cho biết đã dùng hết bao nhiêu chữ số, hỏi sách dày mấy trang.']),
        _c('de_toan', 'Đề bài', de='Dùng hết 660 chữ số dán trang. Sách dày mấy trang?',
           loi=['Dùng hết sáu trăm sáu mươi chữ số. Hỏi sách dày bao nhiêu trang.',
                'Nhiều bạn chia luôn cho ba. Sai ngay từ đó.']),
        _c('y_toan', 'Vì sao KHÔNG chia 3 ngay từ đầu?',
           'Vùng 1 dùng thẻ 1 chữ số, vùng 2 dùng thẻ 2 — chia sớm là gán oan cho chúng',
           buoc=1, soBuoc=3,
           loi=['Vì sao không chia ba ngay từ đầu. Vùng một dùng thẻ một chữ số, '
                'vùng hai dùng thẻ hai.',
                'Chia ba ngay là gán oan cho chúng dùng thẻ ba chữ số.']),
        _c('y_toan', 'Nhịp 1 — TRỪ hai vùng đầu ra',
           '660 − 9 = 651  →  651 − 180 = 471', buoc=2, soBuoc=3,
           loi=['Nhịp một, trừ hai vùng đầu ra. Trừ chín rồi trừ một trăm tám mươi, '
                'còn bốn trăm bảy mươi mốt.',
                'Nay mới toàn thẻ ba chữ số.']),
        _c('y_toan', 'Nhịp 2 — CHIA cho 3', '471 : 3 = 157 trang', buoc=3, soBuoc=3,
           loi=['Nhịp hai, chia cho ba. Bốn trăm bảy mốt chia ba, được một trăm năm '
                'mươi bảy trang.']),
        _c('y_toan', 'Nhịp 3 — CỘNG mốc trở lại', '157 + 99 = 256 trang',
           loi=['Nhịp ba, cộng mốc trở lại, được hai trăm năm mươi sáu trang.',
                'Vì con số vừa chia mới chỉ là số trang của riêng vùng ba.']),
        _c('y_toan', 'Hai cú trượt kinh điển',
           'chia sớm khi chưa trừ vùng  ·  chia xong quên cộng mốc',
           loi=['Hai cú trượt kinh điển. Chia sớm khi chưa trừ vùng, và chia xong '
                'quên cộng mốc.']),
        _c('cong_thuc', 'Ba nhịp, ghi thành ba dòng',
           congThuc='TRỪ vùng  →  CHIA  →  CỘNG mốc',
           thay='và luôn thử lại bằng phép đếm xuôi của bài trước',
           loi=['Con nhớ ba nhịp, ghi thành ba dòng. Trừ vùng, chia, cộng mốc.',
                'Rồi thử lại bằng phép đếm xuôi của bài trước.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_dinh_vi_chu_so(b):
    """L5·B8·M3 Chữ số thứ n của dãy — hai cửa đọc số dư."""
    return [
        _c('bia', 'Chữ số thứ mấy là chữ số nào', so_bai(b),
           loi=['Viết liền các số lại thành một dãy dài, rồi hỏi chữ số ở một vị trí '
                'là chữ số gì.']),
        _c('de_toan', 'Đề bài', de='Dãy 123456789101112… — chữ số thứ 200 là chữ số nào?',
           loi=['Hỏi chữ số thứ hai trăm của dãy ấy là chữ số nào.']),
        _c('y_toan', 'Bước 1 — trừ mốc để biết đang ở vùng nào',
           '200 > 189  →  đã sang vùng 3 chữ số  ·  200 − 189 = 11', buoc=1, soBuoc=3,
           loi=['Bước một, trừ mốc. Hai trăm lớn hơn một tám chín nên đã sang vùng ba '
                'chữ số, còn dư mười một.']),
        _c('y_toan', 'Bước 2 — chia cho cỡ thẻ, LẤY CẢ SỐ DƯ',
           '11 : 3 = 3 dư 2', buoc=2, soBuoc=3,
           loi=['Bước hai, chia cho cỡ thẻ. Mười một chia ba bằng ba dư hai.',
                'Đi trọn ba số, rồi bước thêm hai chữ số.']),
        _c('y_toan', 'Đi trọn 3 số kể từ mốc 99', '100 · 101 · 102 — dừng ở 102',
           buoc=3, soBuoc=3,
           loi=['Đi trọn ba số kể từ mốc chín mươi chín, là một trăm, một linh một, '
                'một linh hai.']),
        _c('y_toan', 'Bước 3 — DƯ 2 nên bước vào số KẾ TIẾP',
           'số kế là 103 · lấy chữ số thứ 2 của nó  →  chữ số 0',
           loi=['Bước ba. Dư hai nên phải bước vào số kế tiếp là một linh ba.',
                'Lấy chữ số thứ hai của nó, chính là chữ số không.']),
        _c('y_toan', 'Thử một vị trí xa hơn',
           '2026 − 189 = 1837 · 1837 : 3 = 612 dư 1  →  số kế 712, lấy chữ số đầu',
           loi=['Thử một vị trí xa hơn. Trừ mốc rồi chia ba, được sáu trăm mười hai '
                'dư một.',
                'Đi trọn tới số bảy trăm mười một, rồi lấy chữ số đầu của số kế.']),
        _c('cong_thuc', 'HAI CỬA đọc số dư — đây là chỗ hỏng',
           congThuc='dư 0 → chữ số CUỐI của số vừa đi trọn  ·  dư r → chữ số thứ r của số KẾ',
           thay='dư khác 0 nghĩa là kim đã RỜI số cũ, đang đứng giữa số mới',
           loi=['Hai cửa đọc số dư, đây là chỗ hỏng.',
                'Dư không thì lấy chữ số cuối của số vừa đi trọn.',
                'Dư khác không thì kim đã rời số cũ, phải lấy chữ số thứ ấy của số kế '
                'tiếp.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_soi_duoi_may_chu_so(b):
    """L5·B9·M1 Soi đuôi mấy chữ số — hỏi số tròn nó ăn theo."""
    return [
        _c('bia', 'Soi đuôi mấy chữ số mới đủ', so_bai(b),
           loi=['Chia hết cho hai thì soi một chữ số cuối. Cho bốn thì mấy chữ số.']),
        _c('tach_so', 'Chia hết cho 4 — soi HAI chữ số cuối', so='1236', sang=[3, 4],
           phep='36 : 4 = 9  ✓', chuPhu='Không cần đụng tới hai chữ số đầu.',
           loi=['Chia hết cho bốn thì soi hai chữ số cuối. Ba mươi sáu chia bốn được '
                'chín.']),
        _c('y_toan', 'Vì sao chỉ cần soi hai chữ số?',
           'vì 100 chia hết cho 4 — mọi hàng từ trăm trở lên tự qua cửa',
           buoc=1, soBuoc=3,
           loi=['Vì một trăm chia hết cho bốn. Mọi hàng từ trăm trở lên tự qua cửa.']),
        _c('cong_thuc', 'Nên hỏi: số này ăn theo số tròn nào?',
           congThuc='2·5 ăn theo 10 → soi 1  ·  4·25 ăn theo 100 → soi 2',
           thay='số tròn ấy có mấy số 0 thì soi bấy nhiêu chữ số cuối',
           loi=['Nên trước khi soi, con hỏi số này ăn theo số tròn nào.',
                'Hai và năm ăn theo mười nên soi một chữ số. Bốn và hai lăm ăn theo '
                'một trăm nên soi hai.']),
        _c('y_toan', 'Sâu thêm một bậc nữa', '8 · 125 ăn theo 1000 → soi 3 chữ số cuối',
           buoc=2, soBuoc=3,
           loi=['Sâu thêm một bậc. Tám và một trăm hai lăm ăn theo một nghìn nên soi '
                'ba chữ số cuối.']),
        _c('tach_so', 'Số 11 thì soi kiểu khác hẳn — XEN KẼ', so='2728',
           sang=[2, 4], phep='(8 + 7) − (2 + 2) = 11  ✓',
           chuPhu='Cộng cách quãng hai bên, rồi lấy hiệu.',
           loi=['Số mười một soi kiểu khác hẳn. Cộng các chữ số ở vị trí lẻ, rồi cộng '
                'ở vị trí chẵn.',
                'Đếm từ phải sang. Tám cộng bảy được mười lăm, hai cộng hai được bốn.',
                'Hiệu bằng mười một nên số ấy chia hết cho mười một.']),
        _c('y_toan', 'Còn họ TỔNG thì vẫn như cũ', '3 và 9 — cộng hết các chữ số',
           loi=['Còn ba và chín thì vẫn cộng hết các chữ số như con đã học.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='soi đuôi mấy chữ số — hỏi SỐ TRÒN nó ăn theo',
           thay='chọn nhầm ống kính là soi thiếu, số trượt mà tưởng đạt',
           loi=['Con nhớ câu này. Soi đuôi mấy chữ số thì hỏi số tròn nó ăn theo.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_so_hop_thao_cap(b):
    """L5·B9·M2 Số hợp không có dấu hiệu riêng — tháo thành cặp không chung ước."""
    return [
        _c('bia', 'Số 6 có dấu hiệu riêng không?', so_bai(b),
           loi=['Có bạn bảo tổng chữ số chia hết cho sáu thì số chia hết cho sáu.']),
        _c('tach_so', 'Thử ngay một số', so='15', sang=[1, 2],
           phep='1 + 5 = 6, chia hết cho 6', chuPhu='Nhưng 15 là số LẺ — đâu chia hết cho 6.',
           loi=['Thử ngay số mười lăm. Tổng chữ số bằng sáu, chia hết cho sáu.',
                'Nhưng mười lăm là số lẻ, đâu chia hết cho sáu. Vậy là không có dấu '
                'hiệu ấy.']),
        _c('cong_thuc', 'Số 6 phải khám HAI cửa',
           congThuc='6 = 2 × 3  →  khám cửa CHẴN và cửa TỔNG chia hết 3',
           thay='số hợp không có dấu hiệu riêng, phải tháo ra thành cặp thừa số',
           loi=['Số sáu phải khám hai cửa, vì sáu bằng hai nhân ba.',
                'Khám cửa chẵn, rồi khám cửa tổng chia hết cho ba.']),
        _c('y_toan', 'Làm thử', '53x chia hết 6: chẵn → x ∈ 0,2,4,6,8',
           buoc=1, soBuoc=3,
           loi=['Làm thử. Tìm chữ số ích để năm ba ích chia hết cho sáu.',
                'Cửa chẵn cho ích là không, hai, bốn, sáu hoặc tám.']),
        _c('y_toan', 'Cửa thứ hai lọc tiếp', 'tổng 8 + x chia hết 3 → x ∈ 1,4,7',
           buoc=2, soBuoc=3,
           loi=['Cửa thứ hai lọc tiếp. Tổng tám cộng ích phải chia hết cho ba, nên ích '
                'là một, bốn hoặc bảy.']),
        _c('y_toan', 'Qua ĐỦ hai cửa mới được', 'chỉ còn x = 4  →  số 534',
           buoc=3, soBuoc=3,
           loi=['Qua đủ hai cửa mới được. Chỉ còn ích bằng bốn, được số năm trăm ba '
                'mươi tư.']),
        _c('y_toan', 'Nhưng THÁO thế nào cũng được sao?',
           '45 = 15 × 3 — hai mảnh CHUNG ước 3, tháo thế là sai',
           loi=['Nhưng tháo thế nào cũng được sao. Bốn lăm bằng mười lăm nhân ba.',
                'Hai mảnh ấy chung ước ba, nên tháo thế là sai.']),
        _c('cong_thuc', 'Luật tháo',
           congThuc='hai mảnh phải KHÔNG chung ước nào ngoài 1',
           thay='số 15 qua cả cửa 15 lẫn cửa 3 mà vẫn không chia hết 45',
           loi=['Luật tháo. Hai mảnh phải không chung ước nào ngoài một.',
                'Ví dụ số mười lăm qua cả cửa mười lăm lẫn cửa ba, mà vẫn không chia '
                'hết cho bốn lăm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_hai_an_x_y(b):
    """L5·B9·M3 Hai chữ số bị xoá — chốt ẩn ở đuôi trước."""
    return [
        _c('bia', 'Hai chữ số bị xoá', so_bai(b),
           loi=['Một số bị xoá mất hai chữ số. Tìm lại chúng.']),
        _c('de_toan', 'Đề bài', de='Số x47y chia hết cho 45. Tìm x và y.',
           loi=['Số ích bốn bảy ích dài chia hết cho bốn lăm. Tìm hai chữ số bị xoá.']),
        _c('y_toan', 'Tháo 45 thành cặp không chung ước',
           '45 = 9 × 5  ·  mỗi mảnh phụ trách một ẩn', buoc=1, soBuoc=3,
           loi=['Tháo bốn lăm thành chín nhân năm. Hai mảnh này không chung ước.']),
        _c('y_toan', 'Chốt ẩn ở ĐUÔI trước — vì nó ít lựa chọn nhất',
           'chia hết 5  →  y chỉ có thể là 0 hoặc 5', buoc=2, soBuoc=3,
           loi=['Chốt ẩn ở đuôi trước, vì cửa đuôi cho ít lựa chọn nhất.',
                'Chia hết cho năm nên chữ số cuối chỉ có thể là không hoặc năm.']),
        _c('y_toan', 'Mỗi giá trị là MỘT NHÁNH riêng',
           'nhánh y = 0  ·  nhánh y = 5', buoc=3, soBuoc=3,
           loi=['Mỗi giá trị là một nhánh riêng, phải đi trọn cả hai.']),
        _c('tach_so', 'Nhánh y = 0 — dò x theo cửa tổng', so='7470',
           sang=[1], phep='7 + 4 + 7 + 0 = 18, chia hết 9 ✓',
           chuPhu='Được số 7470.',
           loi=['Nhánh thứ nhất, đuôi bằng không. Tổng phải chia hết cho chín.',
                'Dò được ích bằng bảy, thành số bảy nghìn bốn trăm bảy mươi.']),
        _c('tach_so', 'Nhánh y = 5 — cũng dò như thế', so='2475',
           sang=[1], phep='2 + 4 + 7 + 5 = 18, chia hết 9 ✓',
           chuPhu='Được số 2475 — nghiệm thứ hai.',
           loi=['Nhánh thứ hai, đuôi bằng năm. Dò được ích bằng hai, thành số hai '
                'nghìn bốn trăm bảy mươi lăm.',
                'Bài này có tới hai đáp số, dừng ở nhánh đầu là mất một nửa.']),
        _c('y_toan', 'Thử lại từng số', '7470 : 45 = 166  ·  2475 : 45 = 55',
           loi=['Thử lại từng số bằng phép chia cho chắc.']),
        _c('cong_thuc', 'Nghi thức ba nhịp',
           congThuc='tháo cặp  →  chốt ẩn ĐUÔI trước  →  dò ẩn kia TỪNG NHÁNH',
           thay='và gom đủ mọi nghiệm, đừng bắt được một số đã nghỉ',
           loi=['Con nhớ ba nhịp. Tháo cặp, chốt ẩn ở đuôi trước, rồi dò ẩn kia theo '
                'từng nhánh.',
                'Và gom đủ mọi nghiệm, đừng bắt được một số đã vội nghỉ.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_luat_nen_chia_du(b):
    """L5·B10·M1 Dư luôn bé hơn số chia — dư tối đa là số chia trừ 1."""
    return [
        _c('bia', 'Số dư lớn nhất là bao nhiêu', so_bai(b),
           loi=['Chia một số cho năm thì số dư lớn nhất có thể là mấy.']),
        _c('nhom_deu', 'Xếp 14 viên vào túi 5 viên', tong=14, moiNhom=5,
           chuPhu='Được 2 túi đầy, còn 4 viên lẻ — đó là dư lớn nhất.',
           loi=['Xếp mười bốn viên vào túi năm viên. Được hai túi đầy, còn bốn viên '
                'lẻ.',
                'Bốn là số dư lớn nhất khi chia cho năm.']),
        _c('y_toan', 'Vì sao dư không thể bằng 5?',
           'đủ 5 viên lẻ thì chúng TỰ đóng thêm một túi', buoc=1, soBuoc=3,
           loi=['Vì sao dư không thể bằng năm. Vì đủ năm viên lẻ thì chúng tự đóng '
                'thêm một túi nữa.',
                'Lúc ấy thương nhảy thêm một, và tay lại trống.']),
        _c('cong_thuc', 'Nên có một luật nền cho mọi phép chia',
           congThuc='số dư < số chia  ·  dư lớn nhất = số chia − 1',
           thay='chia cho 5 dư tối đa 4, chia cho 7 dư tối đa 6',
           loi=['Nên có luật nền cho mọi phép chia. Số dư luôn bé hơn số chia.',
                'Dư lớn nhất bằng số chia trừ một. Chia cho bảy thì dư tối đa là '
                'sáu.']),
        _c('y_toan', 'Phép thử lại của mọi bài chia có dư',
           'số bị chia = số chia × thương + số dư', buoc=2, soBuoc=3,
           loi=['Phép thử lại của mọi bài chia có dư. Số chia nhân thương, cộng số '
                'dư, phải ra đúng số bị chia.']),
        _c('y_toan', 'Thử một số', '100 : 9 = 11 dư 1  →  9 × 11 + 1 = 100 ✓',
           loi=['Thử một số. Một trăm chia chín bằng mười một dư một.',
                'Chín nhân mười một cộng một, đúng bằng một trăm.']),
        _c('y_toan', 'Phản xạ bắt lỗi', '"43 : 5 = 7 dư 8" — dư 8 lớn hơn số chia 5',
           buoc=3, soBuoc=3,
           loi=['Con tập phản xạ bắt lỗi. Có bạn viết bốn ba chia năm bằng bảy dư '
                'tám.',
                'Dư tám mà số chia có năm, phạm luật ngay. Đáp đúng là tám dư ba.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='dư mà bằng số chia — thương đã kịp lớn thêm một',
           thay='nên soi số dư trước khi ghi đáp số, lần nào cũng soi',
           loi=['Con nhớ câu này. Dư mà bằng số chia thì thương đã kịp lớn thêm một.',
                'Nên soi số dư trước khi ghi đáp số.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_bot_bang_du_them_bang_bu(b):
    """L5·B10·M2 Bớt bằng dư, thêm bằng bù — cộng lại tròn một khoảng."""
    return [
        _c('bia', 'Vá cho tròn', so_bai(b),
           loi=['Một số chưa chia hết. Bớt hay thêm ít nhất bao nhiêu cho nó chia '
                'hết.']),
        _c('de_toan', 'Đề bài', de='100 : 9 dư 1. Thêm ít nhất mấy để chia hết cho 9?',
           loi=['Một trăm chia chín dư một. Thêm ít nhất bao nhiêu để chia hết cho '
                'chín.',
                'Nhiều bạn trả lời ngay là thêm một. Con thử nghĩ lại.']),
        _c('day_so', 'Vẽ con đường kẻ vạch mỗi 9 mét', so=[90, 99, 108],
           hienThuTu=False, chuPhu='Số 100 đứng GIỮA hai vạch 99 và 108.',
           loi=['Vẽ con đường kẻ vạch mỗi chín mét. Chín mươi, chín mươi chín, một '
                'trăm linh tám.',
                'Số một trăm đứng giữa hai vạch.']),
        _c('y_toan', 'Lùi về vạch SAU thì bớt đúng số DƯ',
           '100 − 1 = 99  ·  đó chính là số dư', buoc=1, soBuoc=3,
           loi=['Lùi về vạch sau thì bớt đúng số dư. Một trăm bớt một được chín mươi '
                'chín.']),
        _c('y_toan', 'Tiến tới vạch TRƯỚC thì thêm PHẦN BÙ',
           'phần bù = số chia − dư = 9 − 1 = 8  →  108', buoc=2, soBuoc=3,
           loi=['Tiến tới vạch trước thì phải thêm phần bù. Phần bù bằng số chia trừ '
                'số dư.',
                'Chín trừ một bằng tám, nên thêm tám được một trăm linh tám.']),
        _c('cong_thuc', 'Hai cửa ngược chiều — và có phép thử nhanh',
           congThuc='bớt + thêm = dư + bù = SỐ CHIA',
           thay='cộng hai đáp không ra số chia thì chắc chắn sai một cái',
           loi=['Hai cửa ngược chiều nhau. Bớt một, thêm tám, cộng lại đúng chín.',
                'Đó là phép thử nhanh. Cộng hai đáp không ra số chia thì chắc chắn '
                'sai một cái.']),
        _c('y_toan', 'Chỗ hay nhầm', 'Thấy dư 1 là thêm 1 — nhưng 101 vẫn không chia hết',
           buoc=3, soBuoc=3,
           loi=['Chỗ hay nhầm là thấy dư một thì thêm một.',
                'Nhưng một trăm linh một vẫn chưa chia hết cho chín.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='BỚT bằng dư  ·  THÊM bằng bù',
           thay='vì lùi về vạch sau khác hẳn tiến tới vạch trước',
           loi=['Con nhớ câu này. Bớt thì bằng dư, thêm thì bằng bù.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_hai_dieu_kien_du(b):
    """L5·B10·M3 Hai điều kiện dư cùng lúc — bước nhảy bằng tích hai số chia."""
    return [
        _c('bia', 'Hai điều kiện dư cùng lúc', so_bai(b),
           loi=['Tìm số vừa chia ba dư một, vừa chia năm dư hai.']),
        _c('y_toan', 'Dò trên dãy của số chia LỚN hơn cho nhanh',
           'chia 5 dư 2: 2, 7, 12, 17…  — thưa hơn nên ít số phải thử',
           buoc=1, soBuoc=3,
           loi=['Dò trên dãy của số chia lớn hơn cho nhanh, vì dãy ấy thưa hơn.',
                'Chia năm dư hai được dãy hai, bảy, mười hai, mười bảy.']),
        _c('y_toan', 'Kiểm từng số bằng điều kiện còn lại',
           '2 chia 3 dư 2 ✗  ·  7 chia 3 dư 1 ✓', buoc=2, soBuoc=3,
           loi=['Kiểm từng số bằng điều kiện còn lại. Hai chia ba dư hai, trượt.',
                'Bảy chia ba dư một, khớp. Vậy bảy là nghiệm đầu tiên.']),
        _c('day_so', 'Các nghiệm sau cách đều 15', so=[7, 22, 37, 52],
           hienThuTu=False, chuPhu='Bước nhảy 15 = 3 × 5.',
           loi=['Các nghiệm sau cách đều mười lăm. Bảy, hai mươi hai, ba mươi bảy, năm '
                'mươi hai.']),
        _c('cong_thuc', 'Vì sao bước nhảy là 15?',
           congThuc='bước nhảy = tích hai số chia',
           thay='chỉ bước đúng bội chung mới giữ nguyên CẢ HAI số dư',
           loi=['Vì sao bước nhảy là mười lăm. Vì chỉ bước đúng bội chung của hai số '
                'chia.',
                'Bước ba thì giữ được dư của ba nhưng gãy dư của năm.']),
        _c('y_toan', 'Có một mẹo cho trường hợp riêng',
           'chia 3 dư 2 VÀ chia 5 dư 4 — cả hai dư đều HỤT ĐÚNG 1', buoc=3, soBuoc=3,
           loi=['Có một mẹo cho trường hợp riêng. Chia ba dư hai và chia năm dư bốn.',
                'Cả hai số dư đều hụt đúng một so với số chia.']),
        _c('y_toan', 'Thì cộng 1 vào là chia hết cả hai',
           'số + 1 chia hết 15  →  số = 14, 29, 44…',
           loi=['Thì cộng một vào là số ấy chia hết cho cả hai. Nên số cần tìm là mười '
                'lăm trừ một, bằng mười bốn.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='tìm nghiệm ĐẦU  →  rồi nhảy đều bằng TÍCH hai số chia',
           thay='và nếu các dư cùng hụt 1 thì cộng 1 cho gọn',
           loi=['Con nhớ hai nhịp. Tìm nghiệm đầu, rồi nhảy đều bằng tích hai số chia.',
                'Và nếu các số dư cùng hụt một thì cộng một vào cho gọn.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_ban_do_vong_duoi(b):
    """L5·B11·M1 Vòng quay chữ số tận cùng — nhóm đứng im và vòng đôi."""
    return [
        _c('bia', 'Nhân mãi thì chữ số cuối chạy đi đâu', so_bai(b),
           loi=['Nhân một số với chính nó nhiều lần. Chữ số cuối đổi thế nào.']),
        _c('day_so', 'Đuôi 5 thì không đổi chút nào', so=[5, 25, 125, 625],
           hienThuTu=False, chuPhu='Nhân bao nhiêu lần, đuôi vẫn là 5.',
           loi=['Đuôi năm thì không đổi chút nào. Năm, hai lăm, một trăm hai lăm, sáu '
                'trăm hai lăm.',
                'Nhân bao nhiêu lần đuôi vẫn là năm.']),
        _c('y_toan', 'Bốn chữ số đứng im', 'đuôi 0 · 1 · 5 · 6 — nhân mãi vẫn thế',
           buoc=1, soBuoc=3,
           loi=['Có bốn chữ số đứng im. Đuôi không, một, năm, sáu.',
                'Sáu nhân sáu bằng ba mươi sáu, đuôi vẫn sáu.']),
        _c('day_so', 'Đuôi 4 thì quay vòng ĐÔI', so=[4, 6, 4, 6],
           hienThuTu=False, chuPhu='4 → 6 → 4 → 6 …',
           loi=['Đuôi bốn thì quay vòng đôi. Bốn, sáu, bốn, sáu.',
                'Đuôi chín cũng vòng đôi. Chín, một, chín, một.']),
        _c('y_toan', 'Vòng đôi thì đọc theo LẺ hay CHẴN',
           'số thừa số lẻ → lấy nhịp đầu  ·  chẵn → lấy nhịp sau',
           loi=['Vòng đôi thì đọc theo số thừa số. Lẻ thì lấy nhịp đầu, chẵn thì lấy '
                'nhịp sau.']),
        _c('day_so', 'Còn 2 · 3 · 7 · 8 quay vòng BỐN', so=[2, 4, 8, 6],
           hienThuTu=False, chuPhu='Vòng của đuôi 2 — bài sau khai thác kỹ.',
           loi=['Còn đuôi hai, ba, bảy, tám thì quay vòng bốn. Vòng của đuôi hai là '
                'hai, bốn, tám, sáu.']),
        _c('y_toan', 'Quên vòng thì dựng lại được',
           'nhân đuôi liên tiếp, mỗi lần CHỈ GIỮ chữ số cuối',
           loi=['Quên vòng thì dựng lại được. Nhân đuôi liên tiếp, mỗi lần chỉ giữ chữ '
                'số cuối.',
                'Hai, bốn, tám, mười sáu lấy sáu, rồi sáu nhân hai được mười hai lấy '
                'hai. Vòng khép lại.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='không phải đuôi nào cũng quay — 0 · 1 · 5 · 6 ngồi im',
           thay='nên hỏi "đuôi này thuộc nhóm nào" trước khi tính',
           loi=['Con nhớ câu này. Không phải đuôi nào cũng quay, bốn chữ số ngồi im.',
                'Nên hỏi đuôi này thuộc nhóm nào trước khi tính.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_vong_bon(b):
    """L5·B11·M2 Vòng bốn — chia số thừa số cho 4 rồi đọc dư."""
    return [
        _c('bia', 'Vòng bốn và số dư', so_bai(b),
           loi=['Nhân hai mươi lần số có đuôi hai. Chữ số cuối là mấy.']),
        _c('day_so', 'Vòng của đuôi 2 có bốn nhịp', so=[2, 4, 8, 6],
           hienThuTu=True, chuPhu='Nhịp 1 · 2 · 3 · 4 rồi lặp lại.',
           loi=['Vòng của đuôi hai có bốn nhịp. Hai, bốn, tám, sáu, rồi lặp lại.']),
        _c('y_toan', 'Nên chia số thừa số cho 4', '20 : 4 = 5 dư 0', buoc=1, soBuoc=3,
           loi=['Nên chia số thừa số cho bốn. Hai mươi chia bốn bằng năm dư không.']),
        _c('y_toan', 'Dư 0 — nhiều bạn quay về nhịp ĐẦU',
           'trả lời đuôi 2 — nhưng sai', buoc=2, soBuoc=3,
           loi=['Dư không thì nhiều bạn quay về nhịp đầu và trả lời đuôi hai. Sai.']),
        _c('y_toan', 'Kiểm bằng một vòng nhỏ', '4 thừa số 2 = 16  →  đuôi 6',
           buoc=3, soBuoc=3,
           loi=['Kiểm bằng một vòng nhỏ. Bốn thừa số hai là mười sáu, đuôi sáu.',
                'Đúng là nhịp cuối vòng, không phải nhịp đầu.']),
        _c('y_toan', 'Đổi vòng vẫn một luật', '13 thừa số 3: 13 : 4 dư 1  →  đuôi 3',
           loi=['Đổi vòng vẫn một luật. Mười ba thừa số ba, chia bốn dư một, lấy nhịp '
                'đầu của vòng ba chín bảy một, được đuôi ba.']),
        _c('y_toan', 'Thêm một ca nữa', '30 thừa số 7: 30 : 4 dư 2  →  đuôi 9',
           loi=['Thêm một ca. Ba mươi thừa số bảy, chia bốn dư hai, lấy nhịp thứ hai '
                'của vòng bảy chín ba một, được đuôi chín.']),
        _c('cong_thuc', 'HAI CỬA đọc số dư — đúng như máy định vị bài trước',
           congThuc='dư r → nhịp thứ r  ·  dư 0 → nhịp CUỐI vòng',
           thay='đi tròn vòng thì dừng ở cuối, chưa bước sang vòng mới',
           loi=['Hai cửa đọc số dư, đúng như máy định vị bài trước.',
                'Dư mấy thì lấy nhịp ấy. Dư không thì lấy nhịp cuối vòng, vì đi tròn '
                'vòng là dừng ở cuối, chưa bước sang vòng mới.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_gop_duoi_chinh_phuong(b):
    """L5·B11·M3 Gộp đuôi, và cửa loại của số chính phương."""
    return [
        _c('bia', 'Gộp đuôi, và một cửa loại rất nhanh', so_bai(b),
           loi=['Cộng hai tích khổng lồ. Chữ số cuối của tổng là mấy.']),
        _c('y_toan', 'Tìm đuôi từng cụm trước',
           '10 thừa số 2 → đuôi 4   ·   10 thừa số 3 → đuôi 9', buoc=1, soBuoc=3,
           loi=['Tìm đuôi từng cụm trước. Mười thừa số hai cho đuôi bốn, mười thừa số '
                'ba cho đuôi chín.']),
        _c('y_toan', 'Cộng hai đuôi rồi LẠI LẤY ĐUÔI',
           '4 + 9 = 13  →  đuôi của tổng là 3', buoc=2, soBuoc=3,
           loi=['Cộng hai đuôi lại được mười ba, rồi lại lấy đuôi. Đuôi của tổng là '
                'ba.',
                'Nhiều bạn dừng ở mười ba và ghi luôn, đó là chỗ hỏng.']),
        _c('day_so', 'Bình phương mọi đuôi chỉ ra 6 kết quả',
           so=[0, 1, 4, 5, 6, 9], hienThuTu=False,
           chuPhu='Không bao giờ ra 2, 3, 7 hay 8.',
           loi=['Nhân thử mười đuôi từ không tới chín với chính nó.',
                'Đuôi ra chỉ có sáu con số. Không bao giờ ra hai, ba, bảy hay tám.']),
        _c('tach_so', 'Nên có cửa loại rất nhanh', so='1327', sang=[4],
           phep='đuôi 7 — LOẠI THẲNG', chuPhu='Chắc chắn không phải số chính phương.',
           loi=['Nên có cửa loại rất nhanh. Số một ba hai bảy có đuôi bảy, loại '
                'thẳng.',
                'Chắc chắn nó không phải bình phương của số nào cả.']),
        _c('tach_so', 'Nhưng đuôi đẹp thì CHƯA duyệt', so='2116', sang=[4],
           phep='đuôi 6 — chưa kết luận được gì',
           chuPhu='Phải kiểm thêm cách khác. Số này đúng là chính phương.',
           loi=['Nhưng đuôi đẹp thì chưa duyệt. Số hai một một sáu có đuôi sáu.',
                'Phải kiểm thêm cách khác mới biết. Số này đúng là bình phương của bốn '
                'mươi sáu.']),
        _c('y_toan', 'Đây là cửa MỘT CHIỀU',
           'đuôi xấu → kết luận được ngay   ·   đuôi đẹp → chưa kết luận gì',
           loi=['Đây là cửa một chiều. Đuôi xấu thì kết luận được ngay, đuôi đẹp thì '
                'chưa kết luận được gì.']),
        _c('cong_thuc', 'Hai câu cần nhớ',
           congThuc='gộp xong LẠI LẤY ĐUÔI  ·  đuôi xấu loại thẳng, đuôi đẹp chưa duyệt',
           thay='vì cửa đuôi chỉ loại được, không chứng minh được',
           loi=['Con nhớ hai câu. Gộp xong thì lại lấy đuôi.',
                'Và đuôi xấu loại thẳng, đuôi đẹp chưa duyệt, vì cửa đuôi chỉ loại '
                'được chứ không chứng minh được.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_so_hang_thu_n(b):
    """L5·B12·M1 Số hạng thứ n của dãy cách đều."""
    return [
        _c('bia', 'Số hạng thứ n là số nào', so_bai(b),
           loi=['Dãy cách đều. Không viết cả dãy vẫn biết số hạng thứ mười là số nào.']),
        _c('day_so', 'Dãy 2 · 5 · 8 · 11 — nhịp 3', so=[2, 5, 8, 11, 14],
           hienThuTu=True, chuPhu='Hàng trên là ĐỨNG THỨ MẤY, hàng dưới là SỐ NÀO.',
           loi=['Dãy hai, năm, tám, mười một. Nhịp ba.',
                'Hàng trên là đứng thứ mấy, hàng dưới là số nào.']),
        _c('y_toan', 'Đứng ở số ĐẦU là chưa nhảy bước nào',
           'tới số thứ 2 mới là 1 bước · thứ 3 là 2 bước', buoc=1, soBuoc=3,
           loi=['Đứng ở số đầu là chưa nhảy bước nào cả.',
                'Tới số thứ hai mới là một bước, số thứ ba là hai bước.']),
        _c('y_toan', 'Nên tới số thứ 10 chỉ mới nhảy 9 bước',
           '2 + 9 × 3 = 29, không phải 2 + 10 × 3', buoc=2, soBuoc=3,
           loi=['Nên tới số thứ mười chỉ mới nhảy chín bước.',
                'Hai cộng chín nhân ba, bằng hai mươi chín. Không phải hai cộng mười '
                'nhân ba.']),
        _c('cong_thuc', 'Công thức số hạng thứ n',
           congThuc='số thứ n = số đầu + (n − 1) × khoảng cách',
           thay='trừ một vì đứng ở số đầu là chưa nhảy bước nào',
           loi=['Số hạng thứ en-nờ bằng số đầu, cộng en-nờ trừ một, nhân khoảng cách.',
                'Trừ một vì đứng ở số đầu là chưa nhảy bước nào.']),
        _c('y_toan', 'Còn một mẹo nữa cho dãy cách đều',
           'trung bình cộng = (số đầu + số cuối) : 2', buoc=3, soBuoc=3,
           loi=['Còn một mẹo nữa. Trung bình cộng của dãy cách đều bằng số đầu cộng số '
                'cuối, chia hai.']),
        _c('y_toan', 'Khỏi cộng cả dãy', 'dãy 3 · 6 · 9 … 99  →  (3 + 99) : 2 = 51',
           loi=['Khỏi phải cộng cả dãy. Dãy ba, sáu, chín tới chín mươi chín.',
                'Ba cộng chín mươi chín, chia hai, được năm mươi mốt.']),
        _c('cong_thuc', 'Vì sao mẹo ấy đúng',
           congThuc='dãy cách đều cân xứng qua điểm giữa',
           thay='hai đầu cân nhau, nên trung bình cộng nằm đúng giữa',
           loi=['Vì dãy cách đều cân xứng qua điểm giữa. Hai đầu cân nhau, nên trung '
                'bình cộng nằm đúng ở giữa.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_tong_ghep_cap(b):
    """L5·B12·M2 Tổng dãy cách đều — ghép cặp rồi chia đôi."""
    return [
        _c('bia', 'Cộng cả dãy trong mười giây', so_bai(b),
           loi=['Cộng từ một tới một trăm. Có cách làm trong mười giây.']),
        _c('y_toan', 'Ghép đầu với cuối thành từng cặp',
           '1 + 100 = 101   ·   2 + 99 = 101   ·   3 + 98 = 101', buoc=1, soBuoc=3,
           loi=['Ghép đầu với cuối thành từng cặp. Một cộng một trăm bằng một trăm '
                'linh một.',
                'Hai cộng chín mươi chín cũng thế. Ba cộng chín mươi tám cũng thế.']),
        _c('y_toan', 'Mỗi cặp ăn HAI số hạng',
           '100 số hạng  →  chỉ 50 cặp, không phải 100', buoc=2, soBuoc=3,
           loi=['Nhưng mỗi cặp ăn hai số hạng. Một trăm số hạng thì chỉ được năm mươi '
                'cặp.']),
        _c('y_toan', 'Nên nhân xong phải chia đôi', '101 × 100 : 2 = 5050',
           buoc=3, soBuoc=3,
           loi=['Nên nhân xong phải chia đôi. Một trăm linh một nhân một trăm, chia '
                'hai, bằng năm nghìn không trăm năm mươi.']),
        _c('cong_thuc', 'Công thức tổng dãy cách đều',
           congThuc='tổng = (đầu + cuối) × số số hạng : 2',
           thay='số số hạng đếm bằng công thức của bài 7 — cộng 1 ra cọc',
           loi=['Tổng bằng đầu cộng cuối, nhân số số hạng, rồi chia hai.',
                'Số số hạng thì đếm bằng công thức bài trước, nhớ cộng một.']),
        _c('y_toan', 'Chỗ hay quên', 'Nhân xong ghi luôn — quên chia đôi là gấp đôi đáp số',
           loi=['Chỗ hay quên là nhân xong ghi luôn. Quên chia đôi thì đáp số gấp đôi '
                'sự thật.']),
        _c('y_toan', 'Bài ngược cũng làm được', 'tổng 1 tới n bằng 210 — tìm n',
           loi=['Bài ngược cũng làm được. Tổng từ một tới en-nờ bằng hai trăm mười, '
                'tìm en-nờ.']),
        _c('cong_thuc', 'Chạy ngược công thức',
           congThuc='n × (n + 1) = 2 × tổng = 420 = 20 × 21  →  n = 20',
           thay='tách 2 lần tổng thành tích HAI SỐ LIỀN NHAU, n là số bé',
           loi=['Chạy ngược công thức. En-nờ nhân en-nờ cộng một, bằng hai lần tổng, '
                'tức bốn trăm hai mươi.',
                'Tách bốn trăm hai mươi thành hai số liền nhau là hai mươi nhân hai '
                'mươi mốt. Vậy en-nờ bằng hai mươi.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_day_lap_chu_ky(b):
    """L5·B12·M3 Dãy lặp chu kỳ — phần tử thứ n và tổng có đuôi lẻ."""
    return [
        _c('bia', 'Dãy lặp đi lặp lại', so_bai(b),
           loi=['Dàn đèn lặp bộ bốn, rồi lại lặp. Bóng thứ một trăm ghi số mấy.']),
        _c('day_so', 'Chu kỳ có bốn phần tử', so=[2, 0, 2, 6],
           hienThuTu=True, chuPhu='Rồi lặp lại y hệt: 2 · 0 · 2 · 6 · 2 · 0 …',
           loi=['Chu kỳ có bốn phần tử. Hai, không, hai, sáu, rồi lặp lại y hệt.']),
        _c('y_toan', 'Chia vị trí cho độ dài chu kỳ', '100 : 4 = 25 dư 0',
           buoc=1, soBuoc=3,
           loi=['Chia vị trí cho độ dài chu kỳ. Một trăm chia bốn bằng hai mươi lăm dư '
                'không.']),
        _c('y_toan', 'Dư 0 thì lấy phần tử CUỐI chu kỳ',
           'đếm tay bộ đầu: bóng thứ 4 chính là số 6', buoc=2, soBuoc=3,
           loi=['Dư không thì lấy phần tử cuối chu kỳ.',
                'Đếm tay bộ đầu mà xem. Bóng thứ tư chính là số sáu, không phải số '
                'hai.']),
        _c('y_toan', 'Đây là lần thứ BA gặp luật ấy',
           'định vị chữ số · vòng đuôi luỹ thừa · và nay dãy lặp', buoc=3, soBuoc=3,
           loi=['Đây là lần thứ ba con gặp luật ấy. Định vị chữ số, vòng đuôi luỹ '
                'thừa, và nay dãy lặp.',
                'Cùng một luật đọc số dư.']),
        _c('y_toan', 'Còn tính TỔNG thì đếm theo xấp',
           'tổng 2026 phần tử của dãy 1 · 2 · 3 lặp mãi',
           loi=['Còn tính tổng thì đếm theo xấp. Tổng hai nghìn không trăm hai sáu '
                'phần tử đầu của dãy một, hai, ba lặp mãi.']),
        _c('y_toan', 'Chia ra xấp trọn và cái đuôi lẻ',
           '2026 : 3 = 675 xấp trọn, dư 1 phần tử',
           loi=['Chia ra xấp trọn và cái đuôi lẻ. Hai nghìn không trăm hai sáu chia '
                'ba, được sáu trăm bảy lăm xấp trọn, dư một phần tử.']),
        _c('cong_thuc', 'Nghi thức hai dòng',
           congThuc='675 × 6 + 1 = 4051',
           thay='xấp trọn × tổng một chu kỳ, CỘNG tổng cái đuôi lẻ — đừng bỏ quên đuôi',
           loi=['Sáu trăm bảy lăm xấp, mỗi xấp tổng sáu, cộng phần tử lẻ là một.',
                'Được bốn nghìn không trăm năm mươi mốt. Bỏ quên cái đuôi lẻ là hụt '
                'ngay.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_cap_so_vang(b):
    """L5·B13·M1 Cặp số cho ra số tròn — và 0,5 là một nửa."""
    return [
        _c('bia', 'Những cặp số cho ra số tròn', so_bai(b),
           loi=['Có những cặp số nhân vào nhau là ra số tròn. Nhớ chúng thì tính rất '
                'nhanh.']),
        _c('de_toan', 'Đề bài', de='Tính nhanh  0,25 × 7,3 × 4',
           loi=['Tính nhanh không phẩy hai lăm, nhân bảy phẩy ba, nhân bốn.']),
        _c('y_toan', 'Trong tích thì được ĐỔI CHỖ và GHÉP NHÓM tuỳ ý',
           'kéo số 4 về cạnh 0,25', buoc=1, soBuoc=3,
           loi=['Trong một tích thì được đổi chỗ và ghép nhóm tuỳ ý.',
                'Con kéo số bốn về cạnh không phẩy hai lăm.']),
        _c('cong_thuc', 'Vì hai số ấy là một cặp vàng',
           congThuc='0,25 × 4 = 1  →  còn lại đúng 7,3',
           thay='nhân với 1 thì số kia giữ nguyên, khỏi tính gì thêm',
           loi=['Vì hai số ấy là một cặp vàng. Không phẩy hai lăm nhân bốn bằng một.',
                'Nhân với một thì số kia giữ nguyên, nên đáp số đúng bằng bảy phẩy '
                'ba.']),
        _c('day_so', 'Kho cặp vàng nên thuộc', so=[4, 2, 8, 4],
           hienThuTu=False,
           chuPhu='0,25 × 4 · 0,5 × 2 · 0,125 × 8 · 2,5 × 4 — đều ra số tròn.',
           loi=['Kho cặp vàng nên thuộc. Không phẩy hai lăm với bốn, không phẩy năm '
                'với hai.',
                'Không phẩy một hai lăm với tám, và hai phẩy năm với bốn.']),
        _c('y_toan', 'Còn một chỗ bẫy về NGHĨA',
           'nhân 0,5 là chia 5?  —  KHÔNG', buoc=2, soBuoc=3,
           loi=['Còn một chỗ bẫy về nghĩa. Nhiều bạn tưởng nhân không phẩy năm là chia '
                'năm.']),
        _c('y_toan', 'Nhân 0,5 là lấy MỘT NỬA', '48 × 0,5 = 24, không phải 9,6',
           buoc=3, soBuoc=3,
           loi=['Nhân không phẩy năm là lấy một nửa, vì không phẩy năm chính là một '
                'nửa.',
                'Bốn mươi tám nhân không phẩy năm bằng hai mươi tư, không phải chín '
                'phẩy sáu.']),
        _c('cong_thuc', 'Nhẩm theo NGHĨA thì nhanh hơn đặt tính',
           congThuc='× 0,5 là chia 2  ·  × 0,25 là chia 4  ·  × 0,2 là chia 5',
           thay='vì 0,5 là một nửa, 0,25 là một phần tư, 0,2 là một phần năm',
           loi=['Nhẩm theo nghĩa thì nhanh hơn đặt tính. Nhân không phẩy năm là chia '
                'hai.',
                'Nhân không phẩy hai lăm là chia bốn. Nhân không phẩy hai là chia '
                'năm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_muon_roi_tra(b):
    """L5·B13·M2 Số gần tròn — nhân 99, và mượn rồi trả."""
    return [
        _c('bia', 'Số sát vách số tròn', so_bai(b),
           loi=['Gặp số sát vách số tròn thì mượn cho tròn, rồi trả lại.']),
        _c('de_toan', 'Đề bài', de='Tính nhanh  4,3 × 99',
           loi=['Tính nhanh bốn phẩy ba nhân chín mươi chín.']),
        _c('cong_thuc', 'Tách 99 ra một dòng trước đã',
           congThuc='99 = 100 − 1  →  4,3 × 99 = 4,3 × 100 − 4,3',
           thay='trừ MỘT LẦN chính nó, không phải trừ 1',
           loi=['Tách chín mươi chín ra một dòng trước đã. Chín mươi chín bằng một '
                'trăm trừ một.',
                'Nên bốn phẩy ba nhân chín mươi chín bằng bốn phẩy ba nhân một trăm, '
                'trừ một lần bốn phẩy ba.']),
        _c('y_toan', 'Chỗ hỏng nằm ngay đây',
           'Nhiều bạn trừ đi 1, chứ không trừ một LẦN chính nó', buoc=1, soBuoc=3,
           loi=['Chỗ hỏng nằm ngay đây. Nhiều bạn trừ đi một, chứ không trừ một lần '
                'chính nó.']),
        _c('y_toan', 'Làm cho trọn', '430 − 4,3 = 425,7', buoc=2, soBuoc=3,
           loi=['Làm cho trọn. Bốn trăm ba mươi trừ bốn phẩy ba, bằng bốn trăm hai '
                'mươi lăm phẩy bảy.']),
        _c('y_toan', 'Mua 99 món mà trả tiền 100 món', 'thì phải được thối lại 1 món',
           loi=['Nghĩ như đi chợ. Mua chín mươi chín món mà trả tiền một trăm món.',
                'Thì phải được thối lại tiền của đúng một món.']),
        _c('de_toan', 'Phép CỘNG cũng mượn được', de='Tính nhanh  4,98 + 3,97',
           loi=['Phép cộng cũng mượn được. Tính nhanh bốn phẩy chín tám cộng ba phẩy '
                'chín bảy.']),
        _c('y_toan', 'Mượn cho tròn — nhưng phải mở SỔ NỢ ngay',
           '5 + 4 = 9  ·  nợ 0,02 và 0,03  →  9 − 0,05 = 8,95', buoc=3, soBuoc=3,
           loi=['Mượn cho tròn thành năm và bốn, cộng lại được chín.',
                'Nhưng mở sổ nợ ngay. Nợ không phẩy không hai và không phẩy không ba.',
                'Chín trừ không phẩy không năm, bằng tám phẩy chín lăm.']),
        _c('cong_thuc', 'Hai câu cần nhớ',
           congThuc='nhân 99 — trừ MỘT LẦN chính nó  ·  mượn cho tròn — TRẢ cho đủ',
           thay='ghi dòng tách hoặc dòng nợ ra giấy, đừng giữ trong đầu',
           loi=['Con nhớ hai câu. Nhân chín mươi chín thì trừ một lần chính nó.',
                'Mượn cho tròn thì trả cho đủ, và ghi dòng nợ ra giấy chứ đừng giữ '
                'trong đầu.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_rut_thua_so_chung(b):
    """L5·B13·M3 Rút thừa số chung, và nghi thức nhìn 5 giây."""
    return [
        _c('bia', 'Khi hai tích dùng chung một thừa số', so_bai(b),
           loi=['Hai tích cùng có một thừa số lặp lại. Rút nó ra là xong ngay.']),
        _c('de_toan', 'Đề bài', de='Tính nhanh  6,8 × 3,7 + 3,7 × 3,2',
           loi=['Tính nhanh sáu phẩy tám nhân ba phẩy bảy, cộng ba phẩy bảy nhân ba '
                'phẩy hai.']),
        _c('y_toan', 'Cả hai tích đều có 3,7', 'rút nó ra ngoài ngoặc',
           buoc=1, soBuoc=3,
           loi=['Cả hai tích đều có ba phẩy bảy. Con rút nó ra ngoài ngoặc.']),
        _c('cong_thuc', 'Phần còn lại vào trong ngoặc',
           congThuc='3,7 × (6,8 + 3,2) = 3,7 × 10 = 37',
           thay='trong ngoặc thường tròn đẹp — đó là dấu hiệu con rút đúng',
           loi=['Phần còn lại vào trong ngoặc. Sáu phẩy tám cộng ba phẩy hai bằng mười '
                'chẵn.',
                'Ba phẩy bảy nhân mười, bằng ba mươi bảy.',
                'Trong ngoặc tròn đẹp chính là dấu hiệu con rút đúng.']),
        _c('y_toan', 'Phép trừ cũng rút được y hệt',
           '0,25 × 611 − 0,25 × 211 = 0,25 × 400 = 100', buoc=2, soBuoc=3,
           loi=['Phép trừ cũng rút được y hệt. Không phẩy hai lăm nhân sáu trăm mười '
                'một, trừ không phẩy hai lăm nhân hai trăm mười một.',
                'Rút ra còn không phẩy hai lăm nhân bốn trăm, bằng một trăm.']),
        _c('y_toan', 'Nghi thức trước mọi biểu thức tính nhanh',
           'nhìn 5 giây và quét ba câu hỏi', buoc=3, soBuoc=3,
           loi=['Nay con có ba chiêu. Nên trước mọi biểu thức tính nhanh, nhìn năm '
                'giây và quét ba câu hỏi.']),
        _c('y_toan', 'Ba câu quét',
           '① có CẶP VÀNG?  ② có SỐ GẦN TRÒN?  ③ có THỪA SỐ CHUNG?',
           loi=['Có cặp vàng nào không. Có số nào sát vách số tròn không.',
                'Có thừa số nào lặp lại ở hai tích không.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='nhìn 5 giây: CẶP VÀNG — GẦN TRÒN — THỪA SỐ CHUNG',
           thay='năm giây ấy rẻ hơn nhiều so với đặt tính cột dọc hai tích',
           loi=['Con nhớ câu này. Nhìn năm giây, soi cặp vàng, số gần tròn, thừa số '
                'chung.',
                'Năm giây ấy rẻ hơn nhiều so với đặt tính cột dọc hai lần.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_cu_sap_domino(b):
    """L5·B14·M1 Tách phân số mẫu là tích hai số liền kề."""
    return [
        _c('bia', 'Cộng cả một dãy phân số', so_bai(b),
           loi=['Cộng một dãy phân số rất dài. Có cách làm trong một phút.']),
        _c('de_toan', 'Đề bài',
           de='1/(1×2) + 1/(2×3) + … + 1/(9×10)',
           loi=['Một phần một nhân hai, cộng một phần hai nhân ba, cộng mãi tới một '
                'phần chín nhân mười.']),
        _c('cong_thuc', 'Mỗi phân số tách được thành một HIỆU',
           congThuc='1/(n × (n+1)) = 1/n − 1/(n+1)',
           thay='vì mẫu là tích của hai số liền kề nhau',
           loi=['Mỗi phân số ấy tách được thành một hiệu, vì mẫu là tích của hai số '
                'liền kề.']),
        _c('phan_so', 'Kiểm thử một quân bằng quy đồng', tu=1, mau=6,
           nhan='1/(2×3)', chuPhu='1/2 − 1/3 = 3/6 − 2/6 = 1/6 ✓',
           chuCuoi='Tách đúng thì hai vế bằng nhau.',
           loi=['Kiểm thử một quân bằng quy đồng. Một phần hai trừ một phần ba.',
                'Quy đồng thành ba phần sáu trừ hai phần sáu, đúng bằng một phần '
                'sáu.']),
        _c('y_toan', 'Viết cả dãy thành các hiệu thì có chuyện hay',
           '(1 − 1/2) + (1/2 − 1/3) + (1/3 − 1/4) + …', buoc=1, soBuoc=3,
           loi=['Viết cả dãy thành các hiệu thì có chuyện hay xảy ra.']),
        _c('y_toan', 'Các mảnh GIỮA triệt tiêu từng đôi một',
           'trừ 1/2 rồi cộng 1/2 · trừ 1/3 rồi cộng 1/3 …', buoc=2, soBuoc=3,
           loi=['Các mảnh ở giữa triệt tiêu từng đôi một. Trừ một phần hai rồi lại '
                'cộng một phần hai.',
                'Cả hàng đổ sập, chỉ còn hai đầu.']),
        _c('y_toan', 'Còn lại đúng hai đầu', '1 − 1/10', buoc=3, soBuoc=3,
           loi=['Còn lại đúng hai đầu. Một trừ một phần mười.']),
        _c('cong_thuc', 'Nhưng CHƯA XONG — phải dọn hiện trường',
           congThuc='1 − 1/10 = 10/10 − 1/10 = 9/10',
           thay='tính gọn ra một phân số, rồi tối giản nếu còn rút được',
           loi=['Nhưng chưa xong. Phải tính gọn ra một phân số, rồi tối giản nếu còn '
                'rút được.',
                'Mười phần mười trừ một phần mười, bằng chín phần mười.',
                'Nộp bài mà để nguyên một trừ một phần mười là chưa dọn hiện '
                'trường.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_doi_chieu_tu_va_khoang(b):
    """L5·B14·M2 Tử bằng khoảng cách thì tách thẳng, khác thì nhân hệ số."""
    return [
        _c('bia', 'Không phải dãy nào cũng tách thẳng được', so_bai(b),
           loi=['Không phải dãy nào cũng tách thẳng được. Phải cân trước đã.']),
        _c('phan_so', 'Quân này tách thẳng được', tu=2, mau=3,
           nhan='2/(1×3)', chuPhu='Tử 2, mẫu cách nhau 2 — khớp nhau.',
           chuCuoi='2/(1×3) = 1 − 1/3 = 2/3 ✓',
           loi=['Quân này tách thẳng được. Tử bằng hai, mà hai mẫu cách nhau cũng '
                'bằng hai.',
                'Hai phần một nhân ba bằng một trừ một phần ba, tức hai phần ba.']),
        _c('phan_so', 'Nhưng quân này chỉ nặng MỘT NỬA', tu=1, mau=3,
           nhan='1/(1×3)', chuPhu='Tử 1, mà mẫu vẫn cách nhau 2.',
           chuCuoi='Tách thẳng ra 2/3 là gấp đôi sự thật.',
           loi=['Nhưng quân này chỉ nặng một nửa. Tử bằng một, mà hai mẫu vẫn cách '
                'nhau hai.',
                'Tách thẳng thì ra hai phần ba, gấp đôi sự thật.']),
        _c('cong_thuc', 'Nên phải nhân thêm hệ số điều chỉnh',
           congThuc='hệ số = tử : khoảng cách',
           thay='tử 1, khoảng 2 thì hệ số là một nửa',
           loi=['Nên phải nhân thêm hệ số điều chỉnh. Hệ số bằng tử chia khoảng cách.',
                'Tử một, khoảng hai, nên hệ số là một nửa.']),
        _c('y_toan', 'Làm lại cho đúng', '1/(1×3) = (1 − 1/3) × 1/2 = 1/3',
           buoc=1, soBuoc=3,
           loi=['Làm lại cho đúng. Một trừ một phần ba, rồi nhân một nửa, được một '
                'phần ba.']),
        _c('y_toan', 'Giữ hệ số NGOÀI ngoặc tới phút cuối',
           '(mảnh đầu − mảnh cuối) × hệ số  →  rồi mới dọn', buoc=2, soBuoc=3,
           loi=['Khi sập cả hàng thì giữ hệ số ngoài ngoặc tới phút cuối.',
                'Lấy mảnh đầu trừ mảnh cuối, nhân hệ số, rồi mới dọn tối giản.']),
        _c('y_toan', 'Làm trọn một dãy',
           '1/(1×3) + 1/(3×5) + … + 1/(7×9) = (1 − 1/9) × 1/2 = 4/9',
           buoc=3, soBuoc=3,
           loi=['Làm trọn một dãy. Một trừ một phần chín, được tám phần chín.',
                'Nhân một nửa, còn bốn phần chín.']),
        _c('cong_thuc', 'Nghi thức an toàn',
           congThuc='tách MỘT quân · thử MỘT quân · rồi mới đẩy cả hàng',
           thay='quen tay tách bừa là cả dãy sai theo, không cứu được',
           loi=['Con nhớ nghi thức an toàn. Tách một quân, thử lại một quân bằng quy '
                'đồng, rồi mới đẩy cả hàng.',
                'Quen tay tách bừa là cả dãy sai theo.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_day_nua_dan(b):
    """L5·B14·M3 Dãy nửa dần — tổng bằng 1 trừ mảnh còn trống."""
    return [
        _c('bia', 'Chiếc bánh ăn mãi không hết', so_bai(b),
           loi=['Ăn nửa cái bánh, rồi nửa phần còn lại, rồi lại nửa nữa.']),
        _c('phan_so', 'Bữa đầu: ăn một nửa', tu=1, mau=2, nhan='đã ăn',
           chuPhu='Còn trống đúng 1/2.',
           loi=['Bữa đầu ăn một nửa. Còn trống đúng một nửa.']),
        _c('phan_so', 'Bữa hai: ăn nửa của phần còn lại', tu=3, mau=4,
           nhan='đã ăn', tu2=1, mau2=4, nhan2='còn trống',
           chuPhu='Ăn thêm 1/4 — phần trống teo còn 1/4.',
           loi=['Bữa hai ăn nửa của phần còn lại, tức một phần tư.',
                'Đã ăn ba phần tư, phần trống teo còn một phần tư.']),
        _c('phan_so', 'Bữa ba cũng thế', tu=7, mau=8, nhan='đã ăn',
           tu2=1, mau2=8, nhan2='còn trống',
           chuPhu='Phần trống lại teo một nửa.',
           loi=['Bữa ba cũng thế. Đã ăn bảy phần tám, còn trống một phần tám.']),
        _c('cong_thuc', 'Nhìn ra ngay quy luật',
           congThuc='tổng đã ăn = 1 − mảnh còn trống',
           thay='mà mảnh còn trống đúng bằng mảnh vừa ăn ở bữa cuối',
           loi=['Nhìn ra ngay quy luật. Tổng đã ăn bằng một trừ mảnh còn trống.',
                'Mà mảnh còn trống đúng bằng mảnh vừa ăn ở bữa cuối.']),
        _c('y_toan', 'Nên tính rất nhanh', 'ăn tới mảnh 1/64  →  tổng = 1 − 1/64 = 63/64',
           buoc=1, soBuoc=3,
           loi=['Nên tính rất nhanh. Ăn tới mảnh một phần sáu tư thì tổng bằng sáu '
                'mươi ba phần sáu tư.']),
        _c('y_toan', 'Cộng thêm bao nhiêu bữa nữa cũng thế',
           'phần trống chỉ TEO ĐI một nửa, không biến mất', buoc=2, soBuoc=3,
           loi=['Cộng thêm bao nhiêu bữa nữa cũng thế. Mỗi bữa chỉ ăn đúng một nửa '
                'phần còn lại.',
                'Nên phần trống chỉ teo đi một nửa, không bao giờ biến mất.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='gần 1 mà KHÔNG là 1 — chiếc bánh còn mảnh trống',
           thay='tổng tiến sát 1 tuỳ ý, nhưng không bao giờ chạm tới',
           loi=['Con nhớ câu này. Gần một mà không là một, chiếc bánh vẫn còn mảnh '
                'trống.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_rut_cheo_day_chuyen(b):
    """L5·B15·M1 Rút chéo dây chuyền — cần dây liền mạch."""
    return [
        _c('bia', 'Nhân một dây phân số', so_bai(b),
           loi=['Nhân ba phân số nối nhau. Có cách khỏi phải quy đồng.']),
        _c('de_toan', 'Đề bài', de='2/3 × 3/4 × 4/5',
           loi=['Hai phần ba, nhân ba phần tư, nhân bốn phần năm.']),
        _c('y_toan', 'Xếp chúng thành một hàng rồi soi',
           'mẫu của anh trước TRÙNG tử của anh sau', buoc=1, soBuoc=3,
           loi=['Xếp chúng thành một hàng rồi soi. Mẫu của anh trước trùng tử của anh '
                'sau.']),
        _c('y_toan', 'Hai số trùng nhau thì tự xoá',
           'số 3 gặp số 3 — xoá  ·  số 4 gặp số 4 — xoá', buoc=2, soBuoc=3,
           loi=['Hai số trùng nhau thì tự xoá. Số ba gặp số ba, xoá. Số bốn gặp số '
                'bốn, xoá.']),
        _c('phan_so', 'Chỉ tử ĐẦU và mẫu CUỐI sống sót', tu=2, mau=5,
           nhan='đáp số', chuPhu='2/3 × 3/4 × 4/5 = 2/5',
           chuCuoi='Cả hàng giữa triệt tiêu hết.',
           loi=['Chỉ tử đầu và mẫu cuối sống sót. Đáp số là hai phần năm.']),
        _c('y_toan', 'Nhưng dây phải LIỀN MẠCH', '2/3 × 3/4 × 5/6 — số 4 gặp số 5',
           buoc=3, soBuoc=3,
           loi=['Nhưng dây phải liền mạch. Xem dãy này. Số ba gặp số ba thì xoá được.',
                'Nhưng số bốn gặp số năm, không xoá được. Dây đứt ở đó.']),
        _c('y_toan', 'Đứt một mắt là DỪNG TAY',
           'phần trước mắt đứt rút được  ·  phần sau phải tính thường',
           loi=['Đứt một mắt là dừng tay ngay. Phần trước mắt đứt rút được, phần sau '
                'phải tính như thường.',
                'Rút ào cả dây là sai từ chỗ đứt.']),
        _c('cong_thuc', 'Nghi thức, và đừng quên dọn',
           congThuc='DÒ dây một lượt  →  rút chéo  →  DỌN tối giản',
           thay='rút xong ra 2/10 thì vẫn phải rút tiếp về 1/5',
           loi=['Con nhớ nghi thức. Dò dây một lượt trước, rồi mới rút chéo, rồi dọn '
                'tối giản.',
                'Rút xong ra hai phần mười thì vẫn phải rút tiếp về một phần năm.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_hai_ho_tich(b):
    """L5·B15·M2 Họ dấu trừ co lại, họ dấu cộng nở ra."""
    return [
        _c('bia', 'Một dấu đổi cả kết quả', so_bai(b),
           loi=['Cùng một dãy ngoặc, đổi dấu trừ thành dấu cộng là kết quả khác hẳn.']),
        _c('y_toan', 'Quy mỗi ngoặc về MỘT phân số trước đã',
           '1 − 1/n = (n−1)/n   ·   1 + 1/n = (n+1)/n', buoc=1, soBuoc=3,
           loi=['Quy mỗi ngoặc về một phân số trước đã.',
                'Một trừ một phần en-nờ thành en-nờ trừ một, trên en-nờ.']),
        _c('phan_so', 'Họ dấu TRỪ: 1/2 × 2/3 × … × 8/9', tu=1, mau=9,
           nhan='đáp số', chuPhu='Dây liền mạch, sập chuyền còn 1/9.',
           loi=['Họ dấu trừ cho dãy một phần hai, nhân hai phần ba, và cứ thế.',
                'Dây liền mạch nên sập chuyền, còn một phần chín.']),
        _c('phan_so', 'Họ dấu CỘNG: 3/2 × 4/3 × … × 10/9', tu=5, mau=1,
           nhan='đáp số', chuPhu='Kẻ sống sót ĐỔI VAI: mẫu đầu và tử cuối  →  10/2 = 5.',
           loi=['Họ dấu cộng cho dãy ba phần hai, nhân bốn phần ba, và cứ thế.',
                'Kẻ sống sót đổi vai. Nay là mẫu đầu và tử cuối, được mười trên hai, '
                'bằng năm.']),
        _c('y_toan', 'Một đoàn CO lại, một đoàn NỞ ra', '1/9  ·  và  5',
           buoc=3, soBuoc=3,
           loi=['Một đoàn co lại, một đoàn nở ra. Cùng chín cái ngoặc.']),
        _c('y_toan', 'Đáp số bé quá — có sai không?',
           'chín thừa số nhân nhau mà chỉ ra 1/9',
           loi=['Nhiều bạn hoảng. Chín thừa số nhân nhau mà chỉ ra một phần chín, chắc '
                'sai.']),
        _c('cong_thuc', 'Tin bằng lý lẽ, không tin bằng cảm giác',
           congThuc='mỗi thừa số (1 − 1/n) đều BÉ HƠN 1',
           thay='nhân với số bé hơn 1 thì tích teo đi — nhân càng nhiều càng teo',
           loi=['Tin bằng lý lẽ chứ đừng tin bằng cảm giác. Mỗi thừa số họ trừ đều bé '
                'hơn một.',
                'Nhân với số bé hơn một thì tích teo đi. Nhân càng nhiều càng teo.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


def kb5_rut_nguyen_cum(b):
    """L5·B15·M3 Gom từng tầng rồi rút nguyên cụm."""
    return [
        _c('bia', 'Tử và mẫu đều là một tổng', so_bai(b),
           loi=['Tử và mẫu đều là tổng của nhiều tích. Rút thế nào cho đúng.']),
        _c('de_toan', 'Đề bài', de='(1×2 + 2×4 + 3×6) / (2×3 + 4×6 + 6×9)',
           loi=['Trên là một nhân hai, cộng hai nhân bốn, cộng ba nhân sáu.',
                'Dưới là hai nhân ba, cộng bốn nhân sáu, cộng sáu nhân chín.']),
        _c('y_toan', 'Chớ gạch chéo ngay — trong TỔNG chưa gom thì CẤM gạch',
           'gạch số 2 trên với số 2 dưới là sai hẳn', buoc=1, soBuoc=3,
           loi=['Chớ gạch chéo ngay. Trong một tổng chưa gom thì cấm gạch.']),
        _c('y_toan', 'Gom thừa số chung của TỬ trước',
           '1×2 = 2×1  ·  2×4 = 2×4  ·  3×6 = 2×9   →   tử = 2 × (1 + 4 + 9)',
           buoc=2, soBuoc=3,
           loi=['Gom thừa số chung của tử trước. Mỗi số hạng đều có một thừa số hai.',
                'Nên tử bằng hai nhân, mở ngoặc, một cộng bốn cộng chín.']),
        _c('y_toan', 'Rồi gom MẪU y hệt',
           '2×3 = 6×1  ·  4×6 = 6×4  ·  6×9 = 6×9   →   mẫu = 6 × (1 + 4 + 9)',
           buoc=3, soBuoc=3,
           loi=['Rồi gom mẫu y hệt. Mỗi số hạng đều có một thừa số sáu.',
                'Nên mẫu bằng sáu nhân, mở ngoặc, một cộng bốn cộng chín.']),
        _c('phan_so', 'Nay lộ ra CỤM CHUNG giống hệt nhau', tu=1, mau=3,
           nhan='đáp số', chuPhu='Cụm (1 + 4 + 9) ở cả trên lẫn dưới — rút nguyên cụm.',
           chuCuoi='Còn 2/6, dọn tối giản thành 1/3.',
           loi=['Nay lộ ra cụm chung giống hệt nhau ở cả trên lẫn dưới.',
                'Rút nguyên cụm ấy đi như rút một thừa số, còn hai phần sáu.',
                'Dọn tối giản thành một phần ba.']),
        _c('y_toan', 'Luật an toàn', 'cụm phải giống hệt ở TỪNG số hạng mới được rút',
           loi=['Luật an toàn. Cụm phải giống hệt ở từng số hạng mới được rút.',
                'Lệch một số hạng là khác bộ lõi, cấm rút.']),
        _c('cong_thuc', 'Câu cần nhớ',
           congThuc='GOM từng tầng  →  RÚT nguyên cụm',
           thay='trong tổng chưa gom thì cấm gạch — đó là chỗ hỏng nặng nhất',
           loi=['Con nhớ câu này. Gom từng tầng rồi mới rút nguyên cụm.',
                'Trong tổng chưa gom thì cấm gạch. Đó là chỗ hỏng nặng nhất của '
                'dạng này.']),
        _c('ket', 'Con hiểu rồi đấy', 'Bây giờ mình làm bài nhé',
           loi=['Con hiểu rồi đấy. Bây giờ mình làm bài nhé.']),
    ]


BO = {
    'DL:KSN5Q1.B15.M1': kb5_rut_cheo_day_chuyen,
    'DL:KSN5Q1.B15.M2': kb5_hai_ho_tich,
    'DL:KSN5Q1.B15.M3': kb5_rut_nguyen_cum,
    'DL:KSN5Q1.B14.M1': kb5_cu_sap_domino,
    'DL:KSN5Q1.B14.M2': kb5_doi_chieu_tu_va_khoang,
    'DL:KSN5Q1.B14.M3': kb5_day_nua_dan,
    'DL:KSN5Q1.B13.M1': kb5_cap_so_vang,
    'DL:KSN5Q1.B13.M2': kb5_muon_roi_tra,
    'DL:KSN5Q1.B13.M3': kb5_rut_thua_so_chung,
    'DL:KSN5Q1.B12.M1': kb5_so_hang_thu_n,
    'DL:KSN5Q1.B12.M2': kb5_tong_ghep_cap,
    'DL:KSN5Q1.B12.M3': kb5_day_lap_chu_ky,
    'DL:KSN5Q1.B11.M1': kb5_ban_do_vong_duoi,
    'DL:KSN5Q1.B11.M2': kb5_vong_bon,
    'DL:KSN5Q1.B11.M3': kb5_gop_duoi_chinh_phuong,
    'DL:KSN5Q1.B10.M1': kb5_luat_nen_chia_du,
    'DL:KSN5Q1.B10.M2': kb5_bot_bang_du_them_bang_bu,
    'DL:KSN5Q1.B10.M3': kb5_hai_dieu_kien_du,
    'DL:KSN5Q1.B9.M1': kb5_soi_duoi_may_chu_so,
    'DL:KSN5Q1.B9.M2': kb5_so_hop_thao_cap,
    'DL:KSN5Q1.B9.M3': kb5_hai_an_x_y,
    'DL:KSN5Q1.B8.M1': kb5_danh_trang_xuoi,
    'DL:KSN5Q1.B8.M2': kb5_danh_trang_nguoc,
    'DL:KSN5Q1.B8.M3': kb5_dinh_vi_chu_so,
    'DL:KSN5Q1.B7.M1': kb5_hang_rao_coc,
    'DL:KSN5Q1.B7.M2': kb5_tu_khac_giua,
    'DL:KSN5Q1.B7.M3': kb5_dem_hoac,
    'DL:KSN5Q1.B6.M1': kb5_quy_tac_nhan,
    'DL:KSN5Q1.B6.M2': kb5_kho_the_voi_dan,
    'DL:KSN5Q1.B6.M3': kb5_dem_co_dieu_kien,
    'DL:KSN5Q1.B5.M1': kb5_xep_doi_hinh,
    'DL:KSN5Q1.B5.M2': kb5_lap_so_chia_het,
    'DL:KSN5Q1.B5.M3': kb5_dieu_kien_kep,
    'DL:KSN5Q1.B4.M1': kb5_thang_may_dau_phay,
    'DL:KSN5Q1.B4.M2': kb5_quen_phay_khi_cong,
    'DL:KSN5Q1.B4.M3': kb5_quen_phay_khi_tru,
    'DL:KSN5Q1.B3.M1': kb5_ba_cong_thuc_guong,
    'DL:KSN5Q1.B3.M2': kb5_guong_vo,
    'DL:KSN5Q1.B3.M3': kb5_hai_ho_dau_hieu,
    'DL:KSN5Q1.B2.M1': kb5_chuyen_nha,
    'DL:KSN5Q1.B2.M2': kb5_cong_tac_dau_phay,
    'DL:KSN5Q1.B2.M3': kb5_chia_chin_khong_chia_muoi,
    'DL:KSN5Q1.B1.M1': kb5_ban_do_cac_hang,
    'DL:KSN5Q1.B1.M2': kb5_cung_chu_so_khac_hang,
    'DL:KSN5Q1.B1.M3': kb5_so_gap_k_lan_tong,
    'DL:KSN3.B01': kb3_thap_nghin,   'DL:KSN3.B02': kb3_hai_cua,
    'DL:KSN3.B03': kb3_duoi_dat_ve,  'DL:KSN3.B04': kb3_dem_nguoc_trang,
    # ══ LỚP 3 · chương 2 · Nhân chia ra ngoài bảng — năm bài ══
    'DL:KSN3.B05': kb3_nhan_ngoai_bang, 'DL:KSN3.B06': kb3_chia_co_du,
    'DL:KSN3.B07': kb3_doan_tau_du,     'DL:KSN3.B08': kb3_chu_lan,
    'DL:KSN3.B09': kb3_mot_phan_may,
    # ══ LỚP 3 · chương 3 · Dãy số thám hiểm — ba bài ══
    'DL:KSN3.B10': kb3_toa_thu_n,       'DL:KSN3.B11': kb3_ma_du,
    'DL:KSN3.B12': kb3_nhip_khong_deu,
    # ══ LỚP 3 · chương 4 · Thứ tự phép tính — bốn bài ══
    'DL:KSN3.B13': kb3_lan_uu_tien,     'DL:KSN3.B14': kb3_dau_ngoac,
    'DL:KSN3.B15': kb3_tim_x_hai_may,   'DL:KSN3.B16': kb3_ra_mat_truoc,
    # ══ LỚP 3 · chương 5 · Toán lời văn — năm bài ══
    'DL:KSN3.B17': kb3_hai_buoc_tinh,   'DL:KSN3.B18': kb3_hon_hay_gap,
    'DL:KSN3.B19': kb3_them_bot_bang_nhau, 'DL:KSN3.B20': kb3_toan_tuoi,
    'DL:KSN3.B21': kb3_rut_ve_don_vi,
    # ══ LỚP 3 · chương 6 · Suy luận — năm bài ══
    'DL:KSN3.B22': kb3_di_lui_nhieu_tram, 'DL:KSN3.B23': kb3_ga_cho,
    'DL:KSN3.B24': kb3_ba_the_tran_cay,   'DL:KSN3.B25': kb3_hai_vong_giao_nhau,
    'DL:KSN3.B26': kb3_quy_ve_mot_loai,
    # ══ LỚP 3 · chương 7 · Hình học — năm bài ══
    'DL:KSN3.B27': kb3_chu_vi_cong_thuc, 'DL:KSN3.B28': kb3_chu_vi_bien_hinh,
    'DL:KSN3.B29': kb3_giai_phau_hinh_tron, 'DL:KSN3.B30': kb3_dien_tich,
    'DL:KSN3.B31': kb3_dem_khoi_theo_tang,
    # ══ LỚP 3 · chương 8 · Toán trong cuộc sống — ba bài (chương cuối) ══
    'DL:KSN3.B32': kb3_xem_gio_to_lich, 'DL:KSN3.B33': kb3_can_va_dong,
    'DL:KSN3.B34': kb3_tien_va_lai,
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
    # ══ LỚP 2 · chương 2 · Bé là vua đếm — sáu bài ══
    'DL:KSN2.B06': kb2_dem_khoang,  'DL:KSN2.B39': kb2_nhay_coc,
    'DL:KSN2.B07': kb2_hai_canh,    'DL:KSN2.B40': kb2_bot_mot,
    'DL:KSN2.B08': kb2_hai_doan_tau, 'DL:KSN2.B41': kb2_cong_hai_doan,
    # ══ LỚP 2 · chương 3 · Dãy số kỳ diệu — chín bài ══
    'DL:KSN2.B09': kb2_bat_nhip,    'DL:KSN2.B42': kb2_so_mo,
    'DL:KSN2.B43': kb2_nhay_thu,    'DL:KSN2.B10': kb2_gap_doi,
    'DL:KSN2.B44': kb2_bac_thang,   'DL:KSN2.B45': kb2_dung_moi_so,
    'DL:KSN2.B11': kb2_nhin_duoi,   'DL:KSN2.B46': kb2_duoi_bang_nhan,
    'DL:KSN2.B47': kb2_cong_chan_le,
    # ══ LỚP 2 · chương 4 · Siêu nhân tính nhanh — mười bài ══
    'DL:KSN2.B12': kb2_ghep_doi,    'DL:KSN2.B48': kb2_ghep_khay,
    'DL:KSN2.B13': kb2_cap_dau_cuoi, 'DL:KSN2.B49': kb2_ban_giua,
    'DL:KSN2.B14': kb2_chay_nguoc,  'DL:KSN2.B50': kb2_nhan_chia_nguoc,
    'DL:KSN2.B51': kb2_bi_lay_di,   'DL:KSN2.B15': kb2_chia_vong,
    'DL:KSN2.B52': kb2_luat_vang,   'DL:KSN2.B53': kb2_chia_het,
    # ══ LỚP 2 · chương 5 · Chuyện toán lời văn — mười hai bài ══
    'DL:KSN2.B16': kb2_chia_deu,    'DL:KSN2.B54': kb2_bai_nguoc_chia,
    'DL:KSN2.B17': kb2_so_do_doan,  'DL:KSN2.B55': kb2_cau_chu_dao,
    'DL:KSN2.B18': kb2_liet_ke,     'DL:KSN2.B56': kb2_do_cot,
    'DL:KSN2.B19': kb2_ve_theo_phan, 'DL:KSN2.B57': kb2_chia_phan,
    'DL:KSN2.B20': kb2_tuoi_sau_nam, 'DL:KSN2.B58': kb2_hieu_tuoi,
    'DL:KSN2.B21': kb2_moi_gio_nhan, 'DL:KSN2.B59': kb2_moi_gio_chia,
    # ══ LỚP 2 · chương 6 · Thám tử tí hon — tám bài ══
    'DL:KSN2.B22': kb2_di_lui,      'DL:KSN2.B60': kb2_thu_tu_lui,
    'DL:KSN2.B23': kb2_gan_hai_chan, 'DL:KSN2.B61': kb2_chan_thua,
    'DL:KSN2.B24': kb2_cay_khoang,  'DL:KSN2.B62': kb2_tim_so_cay,
    'DL:KSN2.B25': kb2_ve_thang,    'DL:KSN2.B63': kb2_bang_loai_tru,
    # ══ LỚP 2 · chương 7 · Vương quốc hình học — mười bài ══
    'DL:KSN2.B26': kb2_nhan_hinh,   'DL:KSN2.B64': kb2_kien_bo,
    'DL:KSN2.B27': kb2_hinh_don,    'DL:KSN2.B65': kb2_hinh_ghep,
    'DL:KSN2.B28': kb2_tam_nan_hoa, 'DL:KSN2.B66': kb2_banh_xe,
    'DL:KSN2.B29': kb2_hai_loai_khoi, 'DL:KSN2.B67': kb2_hinh_va_khoi,
    'DL:KSN2.B30': kb2_luat_ngoi,   'DL:KSN2.B68': kb2_dem_tang,
    # ══ LỚP 2 · chương 8 · Toán trong cuộc sống — sáu bài, khép lại quyển ══
    'DL:KSN2.B31': kb2_mot_nua_hinh, 'DL:KSN2.B69': kb2_mot_nua_nhom,
    'DL:KSN2.B32': kb2_von_lai,     'DL:KSN2.B70': kb2_tien_thua,
    'DL:KSN2.B33': kb2_gio_dung,    'DL:KSN2.B71': kb2_gio_ruoi,
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

        # ── HÌNH ĐẾM ĐƯỢC THÌ LỜI PHẢI NÓI ĐÚNG SỐ ẤY ──
        #
        # Ba cảnh dưới đây vẽ ra từng viên bé ĐẾM ĐƯỢC. Nói một con số mà hình không
        # đếm ra được là hình nói dối — và bé tin mắt chứ không tin tai.
        #
        # Đã dính hai lần: `nhom_deu` vẽ "nhóm" trong khi lời đọc "hàng" (lớp 2, năm
        # chỗ), và `luoi_cham` vẽ lưới 2×3 với 2×4 mà lời chú ghi "2 khay 36 và 2
        # khay 64" (lớp 3 B16). Cả hai lần đều chỉ lộ ra khi rút khung hình ra nhìn.
        if c['loai'] in ('luoi_cham', 'nhom_deu'):
            h, k, k2 = c.get('hang', 0), c.get('cot', 0), c.get('cot2', 0)
            tong, moi = c.get('tong', 0), c.get('moiNhom', 0)
            # Mọi con số bé có thể ĐẾM RA từ hình này.
            dem = {h, k, k2, h * k, h * k2, h * (k + k2), k + k2,
                   tong, moi, tong // moi if moi else 0, tong % moi if moi else 0}
            # SỐ KHOẢNG cũng đếm được từ hình: một hàng n chấm thì nhìn thấy n trừ
            # một cái khe giữa chúng. Cả bài "cây và khoảng" đứng ở chỗ ấy, và nó là
            # thứ bé ĐẾM ĐƯỢC chứ không phải suy ra — nên phải cho vào danh sách,
            # không thì cổng báo chết oan đúng cái hình phục vụ bài tốt nhất.
            dem |= {x - 1 for x in (h, k, k2, tong) if x and x > 1}
            dem |= {0, 1, 2}          # số đếm chung chung, không phải khai gì
            # Màn BẪY cố ý nhắc lại một con số SAI để bé thấy nó sai. Số ấy dĩ nhiên
            # không đếm ra được từ hình — đó là cả điểm của màn. Phải khai rõ bằng
            # `soSai` chứ đừng nới luật: khai ra thì người đọc kịch bản biết ngay
            # đây là số cố ý, còn nới luật thì mọi lỗi thật cũng lọt theo.
            dem |= set(c.get('soSai') or [])
            chu = f"{c['chuChinh']} {c['chuPhu']} " + ' '.join(x for x, _ in c['loiAm'])
            la = [int(x) for x in re.findall(r'(?<![\d,.])\d+(?![\d,.])', chu)]
            thua = sorted({x for x in la if x not in dem})
            if thua:
                loi.append(f'{bai_id} · {c["loai"]}: nói số {thua} mà hình không đếm '
                           f'ra được (hình cho {sorted(x for x in dem if x > 2)})')
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
