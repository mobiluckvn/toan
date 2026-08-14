# -*- coding: utf-8 -*-
"""CHƯƠNG 6 · TỔNG - HIỆU — bốn bài cũ tách thành BẢY, mỗi bài một việc.

Chương này gói chặt hơn hai chương trước:
  · B24 dạy **cả hai công thức** cùng lúc, lại kèm luôn việc vẽ sơ đồ;
  · B27 gộp bài toán tuổi (cùng thêm vào cả hai số) **với** bài ba số biết tổng và
    hai hiệu — hai dạng chẳng liên quan gì nhau.
Và như hai chương trước, **không bài nào dạy sơ đồ đoạn thẳng là gì** — nó được dùng
ngay từ bài đầu như thể bé đã biết.

── BÁC DẶN RIÊNG: VẼ KIỂU ĐOẠN THẲNG ──
Cảnh `so_do_doan` vẽ đúng bằng đoạn thẳng nằm ngang có ngoặc hai đầu, như sách giáo
khoa, chứ không phải cột hay ô vuông. Cả chương chứng minh BẰNG HÌNH:

    thêm HIỆU vào đoạn ngắn  →  hai đoạn bằng nhau  →  hai lần số lớn = tổng + hiệu
    bớt HIỆU khỏi đoạn dài   →  hai đoạn bằng nhau  →  hai lần số bé  = tổng − hiệu

Không có hình thì hai công thức ấy chỉ còn là hai câu phải học thuộc, và bé lẫn dấu
cộng với dấu trừ ngay.

── SỐ NEO CHUNG CẢ CHƯƠNG ──
`tổng 70 · hiệu 10` chạy suốt bảy bài — số lớn 40, số bé 30. Chọn bộ này vì cả hai
công thức đều ra số chẵn đẹp, và trung bình cộng của chúng là 35, đúng bằng nửa tổng,
nên bài "tổng bị giấu" nối lại được với chương 5 vừa học.

── MÃ BÀI (lối C) ──
Bốn mã cũ B24 tới B27 GIỮ NGUYÊN, ba bài mới lấy mã trống kế tiếp B58 tới B60.

    python3 tools/tong_hieu_lop4.py --xem     # in ra, chưa ghi
    python3 tools/tong_hieu_lop4.py           # ghi vào data/lop4/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from khuon_bai_lop4 import (                                       # noqa: E402
    lt, q_tf, q_mcq, dung_muc, soi_bai, bai as _bai,
)

GOC = Path(__file__).resolve().parent.parent
RA = GOC / 'data' / 'lop4'
O_NHAP = GOC / 'data' / 'lop4_dapan_o.json'
THU_TU = RA / 'thu_tu.json'

TEN_CHUONG = 'TỔNG - HIỆU'
CHUONG = 6
CO_KHONG = ['có', 'không']

LUI_BANG = {'ve': ['DL:KSN3.B19'], 'ten': ['THÊM BỚT ĐỂ BẰNG NHAU'],
            'canCu': 'chuDe', 'lopDuoi': 3}
LUI_CHU_VI = {'ve': ['DL:KSN3.B27', 'DL:KSN3.B17'],
              'ten': ['CHU VI CÓ CÔNG THỨC', 'BÀI TOÁN HAI BƯỚC TÍNH'],
              'canCu': 'sach', 'lopDuoi': 3}
LUI_HON = {'ve': ['DL:KSN3.B19', 'DL:KSN3.B18'],
           'ten': ['THÊM BỚT ĐỂ BẰNG NHAU', 'HƠN MẤY ĐƠN VỊ HAY GẤP MẤY LẦN?'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_TUOI = {'ve': ['DL:KSN3.B20'], 'ten': ['TOÁN TUỔI HAI GIA ĐÌNH'],
            'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B58 · SƠ ĐỒ ĐOẠN THẲNG LÀ GÌ — bài KHÁI NIỆM, KHÔNG công thức
# ═══════════════════════════════════════════════════════════════════════════
# Bài này không giải bài toán tổng - hiệu nào. Nó chỉ dạy đọc và vẽ cái hình mà sáu
# bài sau đều dùng. Bỏ qua bước này thì bé phải vừa học hình vừa học công thức, và
# thường là học thuộc công thức rồi bỏ hình.
B58 = bai(
    58, 'SƠ ĐỒ ĐOẠN THẲNG — VẼ BÀI TOÁN RA THÀNH HAI ĐOẠN',
    'Dạng gốc: LV 2.0 mức Lớp 4 — Đọc và vẽ sơ đồ đoạn thẳng cho hai số: đoạn dài, '
    'đoạn ngắn, phần dôi ra là hiệu, cả hai gộp lại là tổng. KHÔNG công thức.',
    'Lớp 3 con đã làm bài "thêm bớt để bằng nhau". Hôm nay con học cách VẼ việc ấy '
    'ra giấy thành hai đoạn thẳng. Vẽ được rồi thì sáu bài sau con nhìn hình là ra '
    'cách làm, không phải nhớ công thức nào cả.',
    LUI_BANG,
    video(
        ['Đọc được một sơ đồ đoạn thẳng: đâu là số bé, số lớn, hiệu, tổng.',
         'Vẽ được sơ đồ cho một bài toán có hai số.',
         'Chỉ ra được phần dôi ra chính là hiệu của hai số.'],
        ['Đề bài: Hai số có tổng bằng 70 và hiệu bằng 10. Hãy vẽ sơ đồ đoạn thẳng cho '
         'bài toán này và chỉ ra từng phần.',
         'Vẽ hai đoạn',
         'Vẽ một đoạn ngắn cho số bé, một đoạn dài hơn cho số lớn. Hai đoạn vẽ thẳng '
         'hàng, đầu bên trái ngang nhau.',
         'Chỉ ra phần dôi ra',
         'Đoạn dài dôi ra một khúc so với đoạn ngắn. Khúc ấy chính là HIỆU, ở đây bằng 10.',
         'Chỉ ra tổng',
         'Gộp cả hai đoạn lại thì được TỔNG, ở đây bằng 70. Ta ngoặc hai đoạn lại và '
         'ghi số 70 bên ngoài.',
         'Đọc lại sơ đồ',
         'Nhìn hình là biết: đoạn trên ngắn hơn, đoạn dưới dài hơn, khúc dôi ra là 10, '
         'cả hai gộp lại là 70.',
         'Đáp số: sơ đồ gồm hai đoạn thẳng; khúc dôi ra ghi 10 là hiệu; ngoặc ngoài '
         'ghi 70 là tổng.'],
        ['Có bạn vẽ sơ đồ rồi ghi số 70 lên ngay đoạn dài.',
         'Gợi ý 1: Số 70 là của riêng một đoạn hay của cả hai đoạn cộng lại?',
         'Gợi ý 2: Của cả hai. Vậy nó phải ghi ở đâu?',
         'Chữa: 70 là TỔNG nên ghi ở ngoặc ôm cả hai đoạn, không ghi lên một đoạn. '
         'Ghi lên một đoạn là biến nó thành số lớn, sai hẳn bài.'],
        ['Bảo con vẽ hai đoạn thẳng cho một bài bất kỳ rồi hỏi ba câu: "Khúc dôi ra là '
         'gì?", "Số 70 ghi ở đâu?", "Đoạn nào là số bé?"',
         'Vẽ được sơ đồ là đã làm xong nửa bài. Con nào bỏ qua hình mà nhảy vào công '
         'thức thường lẫn dấu cộng với dấu trừ ở bài sau.'],
    ),
    [
        lt(1, 1, 'Hai số có tổng 70 và hiệu 10 — đúng bài trong video. Trên sơ đồ, khúc '
                 'dôi ra của đoạn dài so với đoạn ngắn gọi là gì và bằng bao nhiêu?',
           'Khúc dôi ra chính là HIỆU của hai số, bằng 10.'),
        lt(2, 1, 'Vẫn sơ đồ ấy. Số 70 ghi ở đâu trên sơ đồ?',
           'Ghi ở ngoặc ôm cả hai đoạn, vì 70 là TỔNG của hai số.'),
        lt(3, 1, 'Trên sơ đồ hai đoạn, đoạn ngắn hơn biểu diễn số nào?',
           'Đoạn ngắn hơn biểu diễn SỐ BÉ.'),
        lt(4, 2, 'Bạn Nam vẽ sơ đồ rồi ghi số 70 lên đoạn dài. Bạn sai ở đâu?',
           '70 là tổng của cả hai số nên phải ghi ở ngoặc ôm cả hai đoạn. Ghi lên một '
           'đoạn là biến nó thành số lớn.'),
        lt(5, 2, 'Hai số có tổng 100 và hiệu 20. Trên sơ đồ, khúc dôi ra bằng bao nhiêu '
                 'và ngoặc ngoài ghi số mấy?',
           'Khúc dôi ra là hiệu, bằng 20. Ngoặc ngoài ghi tổng, bằng 100.'),
        lt(6, 2, 'Nếu hai đoạn thẳng trên sơ đồ dài bằng nhau thì hiệu của hai số bằng '
                 'bao nhiêu?',
           'Bằng 0 — không có khúc nào dôi ra, nghĩa là hai số bằng nhau.'),
        lt(7, 2, 'Anh có 8 viên bi, em có 5 viên. Vẽ sơ đồ thì khúc dôi ra bằng mấy viên, '
                 'và ngoặc ngoài ghi mấy viên?',
           'Khúc dôi ra: 8 − 5 = 3 viên. Ngoặc ngoài: 8 + 5 = 13 viên.'),
        lt(8, 3, 'Nhìn một sơ đồ có đoạn ngắn 30 và khúc dôi ra 10. Đoạn dài bằng bao '
                 'nhiêu, và tổng bằng bao nhiêu?',
           'Đoạn dài = 30 + 10 = 40. Tổng = 30 + 40 = 70.'),
        lt(9, 3, 'Một sơ đồ có ngoặc ngoài ghi 70 và hai đoạn dài bằng nhau. Mỗi đoạn '
                 'bằng bao nhiêu?',
           'Hai đoạn bằng nhau nên mỗi đoạn là 70 : 2 = 35.'),
        q_tf(1, 'Khúc dôi ra của đoạn dài so với đoạn ngắn chính là hiệu của hai số.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Số tổng được ghi ngay trên đoạn dài.', False,
             'SAI — tổng ghi ở ngoặc ôm cả hai đoạn.'),
        q_mcq(3, 'Trên sơ đồ hai đoạn, đoạn ngắn hơn biểu diễn:',
              ['A. số bé', 'B. số lớn', 'C. hiệu'], 'A. số bé',
              'Đoạn dài hơn mới là số lớn.'),
        q_mcq(4, 'Hai đoạn thẳng dài bằng nhau nghĩa là:',
              ['A. hiệu bằng 0', 'B. tổng bằng 0', 'C. một số bằng 0'],
              'A. hiệu bằng 0', 'Không có khúc nào dôi ra.'),
        q_mcq(5, 'Sơ đồ có đoạn ngắn 30 và khúc dôi ra 10 thì đoạn dài bằng:',
              ['A. 40', 'B. 20', 'C. 70'], 'A. 40', '30 + 10 = 40.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B24 · SỐ LỚN = (TỔNG + HIỆU) : 2  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ dạy CẢ HAI công thức. Nay chỉ còn một — và công thức ấy được SUY RA từ hình
# chứ không nêu ra: thêm hiệu vào đoạn ngắn thì hai đoạn bằng nhau, nên tổng cộng
# hiệu chính là hai lần số lớn.
B24 = bai(
    24, 'SỐ LỚN = (TỔNG + HIỆU) : 2 — THÊM HIỆU CHO HAI ĐOẠN BẰNG NHAU',
    'Dạng gốc: LV 2.1a mức Lớp 4 — Công thức tìm số lớn, suy ra từ sơ đồ đoạn thẳng '
    'bằng cách thêm hiệu vào đoạn ngắn.',
    'Bài trước con đã vẽ được sơ đồ. Hôm nay con làm một việc rất hay trên chính cái '
    'hình ấy: thêm khúc hiệu vào đoạn ngắn cho hai đoạn bằng nhau. Làm xong con sẽ tự '
    'nhìn ra công thức, không phải ai đọc cho chép.',
    LUI_BANG,
    video(
        ['Suy ra được công thức số lớn bằng tổng cộng hiệu rồi chia đôi.',
         'Giải thích được vì sao lại cộng, và vì sao lại chia hai.',
         'Giải được bài toán tổng - hiệu để tìm số lớn.'],
        ['Đề bài: Hai số có tổng bằng 70 và hiệu bằng 10. Tìm số lớn.',
         'Vẽ sơ đồ',
         'Đoạn ngắn là số bé, đoạn dài là số lớn, khúc dôi ra là 10, ngoặc ngoài là 70.',
         'Thêm hiệu vào đoạn ngắn',
         'Nối thêm một khúc 10 vào đoạn ngắn. Bây giờ hai đoạn dài bằng nhau, và mỗi '
         'đoạn đúng bằng số lớn.',
         'Xem tổng đổi thế nào',
         'Ta vừa thêm 10 nên tổng cũng tăng thêm 10, thành 70 + 10 = 80.',
         'Chia đôi',
         '80 chính là hai lần số lớn. Nên số lớn là 80 : 2 = 40.',
         'Đáp số: số lớn bằng 40. Công thức là tổng cộng hiệu rồi chia đôi.'],
        ['Có bạn nhớ công thức nhưng viết thành: số lớn bằng tổng cộng hiệu, rồi ra 80.',
         'Gợi ý 1: Con nhìn lại sơ đồ. Sau khi thêm hiệu vào, có mấy đoạn bằng nhau?',
         'Gợi ý 2: Có HAI đoạn. Vậy 80 là của một đoạn hay của hai đoạn?',
         'Chữa: 80 là của hai đoạn nên còn phải chia đôi: 80 : 2 = 40. Quên chia hai '
         'là ra số lớn gấp đôi số thật.'],
        ['Bảo con vẽ sơ đồ rồi lấy bút nối thêm khúc hiệu vào đoạn ngắn. Con tự thấy '
         'hai đoạn bằng nhau thì sẽ không quên chia hai nữa.',
         'Chỗ sai phổ biến nhất là quên chia hai. Bố mẹ hỏi lại: "Con vừa tính ra số '
         'của mấy đoạn?"'],
    ),
    [
        lt(1, 1, 'Hai số có tổng 70 và hiệu 10 — đúng bài trong video. Sau khi thêm hiệu '
                 'vào đoạn ngắn thì tổng mới bằng bao nhiêu?',
           'Tổng mới = 70 + 10 = 80.'),
        lt(2, 1, 'Vẫn bài trên. Số 80 là của mấy đoạn, và số lớn bằng bao nhiêu?',
           '80 là của HAI đoạn bằng nhau, nên số lớn = 80 : 2 = 40.'),
        lt(3, 1, 'Hai số có tổng 30 và hiệu 10. Tìm số lớn.',
           'Số lớn = (30 + 10) : 2 = 40 : 2 = 20.'),
        lt(4, 2, 'Tổng hai số là 145, hiệu là 27. Tìm số lớn.',
           'Số lớn = (145 + 27) : 2 = 172 : 2 = 86.'),
        lt(5, 2, 'Bạn Lan tính (70 + 10) rồi trả lời số lớn là 80. Bạn sai ở đâu? Số '
                 'lớn đúng là bao nhiêu?',
           'Bạn quên chia hai. 80 là số của hai đoạn bằng nhau, nên số lớn = 80 : 2 = 40.'),
        lt(6, 2, 'Vì sao khi thêm hiệu vào đoạn ngắn thì hai đoạn lại bằng nhau?',
           'Vì đoạn ngắn thiếu đúng một khúc bằng hiệu so với đoạn dài. Bù đúng khúc '
           'ấy vào thì hai đoạn bằng nhau, và mỗi đoạn bằng số lớn.'),
        lt(7, 2, 'Hai anh em có tất cả 500 nghìn đồng lì xì, anh hơn em 60 nghìn. Anh '
                 'có bao nhiêu?',
           'Anh (số lớn) = (500 + 60) : 2 = 560 : 2 = 280 nghìn đồng.'),
        lt(8, 3, 'Tổng hai số là 96, hiệu là 14. Tìm số lớn rồi thử lại bằng cách tính '
                 'số bé và cộng lại.',
           'Số lớn = (96 + 14) : 2 = 55. Số bé = 96 − 55 = 41. Thử: 55 + 41 = 96 và '
           '55 − 41 = 14, đúng cả hai.'),
        lt(9, 3, 'Một mảnh vườn hình chữ nhật có tổng chiều dài và chiều rộng là 24 m, '
                 'chiều dài hơn chiều rộng 6 m. Chiều dài bằng bao nhiêu?',
           'Chiều dài (số lớn) = (24 + 6) : 2 = 30 : 2 = 15 m.'),
        q_tf(1, 'Số lớn bằng tổng cộng hiệu rồi chia cho 2.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Tổng 70, hiệu 10 thì số lớn bằng 80.', False,
             'SAI — còn phải chia hai: 80 : 2 = 40.'),
        q_mcq(3, 'Tổng 70, hiệu 10 thì số lớn bằng:',
              ['A. 40', 'B. 80', 'C. 30'], 'A. 40', '(70 + 10) : 2 = 40.'),
        q_mcq(4, 'Vì sao phải chia hai ở cuối công thức?',
              ['A. Vì tổng cộng hiệu là số của HAI đoạn bằng nhau',
               'B. Vì bài toán có hai số', 'C. Vì hiệu luôn chia hết cho 2'],
              'A. Vì tổng cộng hiệu là số của HAI đoạn bằng nhau',
              'Mỗi đoạn mới bằng số lớn.'),
        q_mcq(5, 'Tổng hai số là 30, hiệu là 10. Số lớn là:',
              ['A. 20', 'B. 40', 'C. 10'], 'A. 20', '(30 + 10) : 2 = 20.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B59 · SỐ BÉ = (TỔNG − HIỆU) : 2
# ═══════════════════════════════════════════════════════════════════════════
# Công thức đối xứng, và cố ý dạy sau — để bé thấy nó KHÔNG phải công thức thứ hai
# phải học thuộc, mà là cùng một cách nghĩ soi từ phía kia: thay vì bù cho đoạn ngắn,
# ta cắt bớt đoạn dài.
B59 = bai(
    59, 'SỐ BÉ = (TỔNG − HIỆU) : 2 — CẮT BỚT CHO HAI ĐOẠN BẰNG NHAU',
    'Dạng gốc: LV 2.1b mức Lớp 4 — Công thức tìm số bé, suy ra từ sơ đồ bằng cách cắt '
    'bỏ khúc hiệu khỏi đoạn dài; và cách kiểm chéo hai công thức.',
    'Bài trước con bù thêm cho đoạn ngắn. Hôm nay con làm ngược lại: cắt bớt khúc hiệu '
    'khỏi đoạn dài. Vẫn là hai đoạn bằng nhau, chỉ khác ở chỗ lần này mỗi đoạn bằng số '
    'bé. Con sẽ thấy đây không phải công thức mới, mà là cùng một cách nghĩ soi từ '
    'phía kia.',
    LUI_BANG,
    video(
        ['Suy ra được công thức số bé bằng tổng trừ hiệu rồi chia đôi.',
         'Hiểu nó là cùng một cách nghĩ với bài trước, chỉ soi từ phía kia.',
         'Kiểm chéo được kết quả bằng cả hai công thức.'],
        ['Đề bài: Hai số có tổng bằng 70 và hiệu bằng 10. Tìm số bé.',
         'Vẫn sơ đồ ấy',
         'Đoạn ngắn là số bé, đoạn dài là số lớn, khúc dôi ra là 10.',
         'Lần này cắt bớt đoạn dài',
         'Cắt bỏ khúc 10 khỏi đoạn dài. Bây giờ hai đoạn bằng nhau, và mỗi đoạn đúng '
         'bằng số bé.',
         'Xem tổng đổi thế nào',
         'Ta vừa cắt đi 10 nên tổng cũng giảm 10, còn 70 − 10 = 60.',
         'Chia đôi',
         '60 chính là hai lần số bé. Nên số bé là 60 : 2 = 30.',
         'Kiểm chéo',
         'Bài trước tìm được số lớn là 40. Cộng lại: 30 + 40 = 70, đúng bằng tổng. '
         'Trừ nhau: 40 − 30 = 10, đúng bằng hiệu.',
         'Đáp số: số bé bằng 30. Công thức là tổng trừ hiệu rồi chia đôi.'],
        ['Có bạn nhớ nhầm thành: số bé bằng hiệu trừ tổng, rồi bảo không trừ được.',
         'Gợi ý 1: Con nhìn sơ đồ. Cái nào lớn hơn, tổng hay hiệu?',
         'Gợi ý 2: Tổng lớn hơn. Vậy phải lấy cái lớn trừ cái nhỏ.',
         'Chữa: số bé bằng TỔNG trừ HIỆU rồi chia đôi: (70 − 10) : 2 = 30. Tổng bao '
         'giờ cũng lớn hơn hiệu nên trừ được.'],
        ['Cho con một bài rồi bắt tính CẢ HAI số bằng hai công thức, sau đó cộng lại '
         'xem có ra đúng tổng không. Đó là cách tự soi rất chắc.',
         'Con lẫn dấu cộng với dấu trừ là chuyện thường. Bố mẹ hỏi: "Con đang tìm số '
         'to hay số nhỏ?" — tìm số to thì cộng, tìm số nhỏ thì trừ.'],
    ),
    [
        lt(1, 1, 'Hai số có tổng 70 và hiệu 10 — đúng bài trong video. Sau khi cắt bớt '
                 'hiệu khỏi đoạn dài thì tổng còn bao nhiêu?',
           'Tổng còn 70 − 10 = 60.'),
        lt(2, 1, 'Vẫn bài trên. Số 60 là của mấy đoạn, và số bé bằng bao nhiêu?',
           '60 là của HAI đoạn bằng nhau, nên số bé = 60 : 2 = 30.'),
        lt(3, 1, 'Hai số có tổng 30 và hiệu 10. Tìm số bé.',
           'Số bé = (30 − 10) : 2 = 20 : 2 = 10.'),
        lt(4, 2, 'Tổng hai số là 145, hiệu là 27. Tìm số bé.',
           'Số bé = (145 − 27) : 2 = 118 : 2 = 59.'),
        lt(5, 2, 'Bạn Bình viết số bé bằng hiệu trừ tổng rồi bảo không trừ được. Bạn sai '
                 'ở đâu? Số bé đúng là bao nhiêu?',
           'Phải lấy TỔNG trừ HIỆU, vì tổng bao giờ cũng lớn hơn hiệu. Số bé = '
           '(70 − 10) : 2 = 30.'),
        lt(6, 2, 'Tìm cả hai số khi tổng là 70 và hiệu là 10, rồi kiểm chéo.',
           'Số lớn = (70 + 10) : 2 = 40; số bé = (70 − 10) : 2 = 30. Kiểm: 40 + 30 = 70 '
           'và 40 − 30 = 10, đúng cả hai.'),
        lt(7, 2, 'Hai anh em có 500 nghìn đồng, anh hơn em 60 nghìn. Em có bao nhiêu?',
           'Em (số bé) = (500 − 60) : 2 = 440 : 2 = 220 nghìn đồng.'),
        lt(8, 3, 'Tổng hai số là 96, hiệu là 14. Tìm cả hai số và kiểm chéo.',
           'Số lớn = (96 + 14) : 2 = 55; số bé = (96 − 14) : 2 = 41. Kiểm: 55 + 41 = 96 '
           'và 55 − 41 = 14.'),
        lt(9, 3, 'Một mảnh vườn có tổng chiều dài và chiều rộng là 24 m, chiều dài hơn '
                 'chiều rộng 6 m. Tìm chiều rộng, rồi tính diện tích mảnh vườn.',
           'Chiều rộng = (24 − 6) : 2 = 9 m; chiều dài = 24 − 9 = 15 m. Diện tích = '
           '15 × 9 = 135 mét vuông.'),
        q_tf(1, 'Số bé bằng tổng trừ hiệu rồi chia cho 2.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Số bé bằng hiệu trừ tổng rồi chia cho 2.', False,
             'SAI — phải lấy tổng trừ hiệu, vì tổng luôn lớn hơn hiệu.'),
        q_mcq(3, 'Tổng 70, hiệu 10 thì số bé bằng:',
              ['A. 30', 'B. 60', 'C. 40'], 'A. 30', '(70 − 10) : 2 = 30.'),
        q_mcq(4, 'Muốn tìm số bé trên sơ đồ, ta:',
              ['A. cắt bớt khúc hiệu khỏi đoạn dài',
               'B. thêm khúc hiệu vào đoạn ngắn', 'C. bỏ hẳn đoạn ngắn đi'],
              'A. cắt bớt khúc hiệu khỏi đoạn dài',
              'Cắt xong thì mỗi đoạn bằng số bé.'),
        q_mcq(5, 'Sau khi tìm được cả hai số, cách kiểm chắc nhất là:',
              ['A. cộng lại xem có bằng tổng và trừ xem có bằng hiệu không',
               'B. chỉ cần cộng lại', 'C. không cần kiểm'],
              'A. cộng lại xem có bằng tổng và trừ xem có bằng hiệu không',
              'Phải khớp CẢ HAI điều đề cho.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B25 · KHI ĐỀ KHÔNG CHO SẴN TỔNG  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Một việc duy nhất: TÌM TỔNG RA TRƯỚC. Đề giấu tổng bằng nhiều cách (chu vi, trung
# bình cộng, thêm bớt), nhưng cách nghĩ chỉ có một, nên vẫn là một bài.
B25 = bai(
    25, 'KHI ĐỀ KHÔNG CHO SẴN TỔNG — TÌM TỔNG RA TRƯỚC ĐÃ',
    'Dạng gốc: LV 2.2 mức Lớp 4 — Tổng bị giấu qua chu vi, qua trung bình cộng, hoặc '
    'qua việc thêm bớt vào một số; tìm tổng rồi mới dùng công thức.',
    'Hai bài vừa rồi đề cho sẵn cả tổng lẫn hiệu. Nhưng đề thật thường giấu tổng đi — '
    'nó cho con chu vi, hoặc cho trung bình cộng. Hôm nay con học đúng một việc: nhận '
    'ra tổng đang nấp ở đâu và lôi nó ra trước.',
    LUI_CHU_VI,
    video(
        ['Nhận ra tổng đang bị giấu trong đề.',
         'Tìm tổng ra từ chu vi hoặc từ trung bình cộng.',
         'Tìm được tổng rồi thì làm tiếp như hai bài trước.'],
        ['Đề bài: Trung bình cộng của hai số là 35, hiệu của chúng là 10. Tìm hai số.',
         'Đề không cho tổng',
         'Đề chỉ cho trung bình cộng và hiệu. Muốn dùng công thức thì phải có tổng.',
         'Lôi tổng ra',
         'Chương trước con đã học: tổng bằng trung bình cộng nhân số lượng. '
         'Ở đây: 35 × 2 = 70.',
         'Bây giờ mới làm như cũ',
         'Số lớn = (70 + 10) : 2 = 40. Số bé = (70 − 10) : 2 = 30.',
         'Một kiểu giấu khác',
         'Nếu đề cho chu vi hình chữ nhật là 48 mét thì tổng chiều dài và chiều rộng '
         'là 48 : 2 = 24 mét, vì chu vi bằng hai lần cái tổng ấy.',
         'Đáp số: hai số là 40 và 30. Việc đầu tiên luôn là tìm tổng.'],
        ['Có bạn thấy "trung bình cộng của hai số là 35" rồi lấy luôn 35 làm tổng.',
         'Gợi ý 1: 35 là số của một phần hay của cả hai phần?',
         'Gợi ý 2: Của một phần. Vậy cả hai phần là bao nhiêu?',
         'Chữa: tổng = 35 × 2 = 70. Lấy nhầm 35 làm tổng thì ra hai số 22 và 12, cộng '
         'lại chỉ được 34, không khớp đề.'],
        ['Cho con một bài có chu vi rồi hỏi: "Chu vi 48 mét thì chiều dài cộng chiều '
         'rộng bằng mấy?" Trả lời được 24 là con đã hiểu.',
         'Bài dạng này con thường nhảy thẳng vào công thức. Bố mẹ hỏi một câu: "Đề đã '
         'cho tổng chưa?"'],
    ),
    [
        lt(1, 1, 'Trung bình cộng của hai số là 35 — đúng bài trong video. Tổng của hai '
                 'số bằng bao nhiêu?',
           'Tổng = 35 × 2 = 70.'),
        lt(2, 1, 'Vẫn bài trên, hiệu là 10. Tìm hai số.',
           'Số lớn = (70 + 10) : 2 = 40; số bé = (70 − 10) : 2 = 30.'),
        lt(3, 1, 'Một hình chữ nhật có chu vi 48 m. Tổng chiều dài và chiều rộng bằng '
                 'bao nhiêu?',
           'Chu vi bằng hai lần tổng ấy, nên tổng = 48 : 2 = 24 m.'),
        lt(4, 2, 'Cuộn lưới 18 m rào vừa khít quanh vườn hình chữ nhật, chiều dài hơn '
                 'chiều rộng 1 m. Tìm chiều dài và chiều rộng.',
           'Tổng dài và rộng = 18 : 2 = 9 m. Chiều dài = (9 + 1) : 2 = 5 m; chiều rộng '
           '= 9 − 5 = 4 m.'),
        lt(5, 2, 'Bạn An thấy "trung bình cộng của hai số là 35" rồi lấy 35 làm tổng. '
                 'Bạn sai ở đâu?',
           '35 là số của MỘT phần. Tổng phải là 35 × 2 = 70. Lấy nhầm thì hai số cộng '
           'lại không khớp đề.'),
        lt(6, 2, 'Trung bình cộng của hai số là 20, hiệu là 8. Tìm hai số.',
           'Tổng = 20 × 2 = 40. Số lớn = (40 + 8) : 2 = 24; số bé = 40 − 24 = 16.'),
        lt(7, 2, 'Vì sao chu vi hình chữ nhật chia đôi thì được tổng chiều dài và chiều '
                 'rộng?',
           'Vì chu vi gồm hai chiều dài và hai chiều rộng, tức đúng hai lần cái tổng ấy. '
           'Chia đôi thì còn một lần.'),
        lt(8, 3, 'Một hình chữ nhật có chu vi 60 m, chiều dài hơn chiều rộng 10 m. Tính '
                 'diện tích.',
           'Tổng dài rộng = 60 : 2 = 30 m. Chiều dài = (30 + 10) : 2 = 20 m; chiều rộng '
           '= 10 m. Diện tích = 20 × 10 = 200 mét vuông.'),
        lt(9, 3, 'Trung bình cộng của hai số là 50. Nếu bớt số lớn đi 12 thì hai số bằng '
                 'nhau. Tìm hai số.',
           'Tổng = 50 × 2 = 100. Bớt 12 thì bằng nhau nghĩa là hiệu bằng 12. Số lớn = '
           '(100 + 12) : 2 = 56; số bé = 44.'),
        q_tf(1, 'Muốn dùng công thức tổng - hiệu thì phải có tổng trước.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Trung bình cộng của hai số là 35 thì tổng của chúng là 35.', False,
             'SAI — tổng là 35 × 2 = 70.'),
        q_mcq(3, 'Chu vi hình chữ nhật là 48 m thì tổng chiều dài và chiều rộng là:',
              ['A. 24 m', 'B. 48 m', 'C. 96 m'], 'A. 24 m', 'Chu vi chia đôi.'),
        q_mcq(4, 'Trung bình cộng hai số là 20 thì tổng của chúng là:',
              ['A. 40', 'B. 20', 'C. 10'], 'A. 40', '20 × 2 = 40.'),
        q_mcq(5, 'Gặp bài giấu tổng, việc đầu tiên phải làm là:',
              ['A. tìm tổng ra trước', 'B. dùng luôn công thức',
               'C. tìm hiệu trước'], 'A. tìm tổng ra trước',
              'Không có tổng thì công thức không dùng được.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B26 · KHI ĐỀ KHÔNG CHO SẴN HIỆU  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Đối xứng với bài trước, và cố ý đặt ngay sau — bé nhận ra hai bài là một cách nghĩ:
# thiếu cái gì thì lôi cái ấy ra trước.
B26 = bai(
    26, 'KHI ĐỀ KHÔNG CHO SẴN HIỆU — LÔI HIỆU RA TỪ CÂU CHỮ',
    'Dạng gốc: LV 2.3 mức Lớp 4 — Hiệu bị giấu: hai số liền nhau, hai số chẵn hoặc lẻ '
    'liền nhau, "bớt k thì bằng nhau", "chuyển k từ số này sang số kia".',
    'Bài trước đề giấu tổng, hôm nay đề giấu hiệu. Cách nghĩ vẫn y hệt: thiếu cái gì '
    'thì lôi cái ấy ra trước. Chỉ khác ở chỗ hiệu thường nấp trong CÂU CHỮ chứ không '
    'nấp trong con số.',
    LUI_HON,
    video(
        ['Nhận ra hiệu đang nấp trong câu chữ của đề.',
         'Lôi được hiệu ra từ mấy kiểu nói quen thuộc.',
         'Có hiệu rồi thì làm tiếp như bài trước.'],
        ['Đề bài: Hai số tự nhiên liên tiếp có tổng bằng 71. Tìm hai số.',
         'Đề không cho hiệu',
         'Đề chỉ nói hai số LIÊN TIẾP. Muốn dùng công thức thì phải có hiệu.',
         'Lôi hiệu ra',
         'Hai số tự nhiên liên tiếp thì hơn kém nhau đúng một đơn vị. Vậy hiệu bằng 1.',
         'Bây giờ mới làm như cũ',
         'Số lớn = (71 + 1) : 2 = 36. Số bé = 71 − 36 = 35.',
         'Mấy kiểu nấp khác',
         'Hai số chẵn liên tiếp thì hiệu là 2. Nói bớt số lớn đi 8 thì hai số bằng nhau, '
         'nghĩa là hiệu bằng 8.',
         'Đáp số: hai số là 35 và 36. Việc đầu tiên luôn là tìm hiệu.'],
        ['Có bạn thấy "hai số chẵn liên tiếp" rồi lấy hiệu bằng 1.',
         'Gợi ý 1: Con kể vài số chẵn liên tiếp xem: 4, rồi số nào?',
         'Gợi ý 2: Là 6. Vậy hai số chẵn liên tiếp cách nhau mấy đơn vị?',
         'Chữa: cách nhau 2, nên hiệu bằng 2 chứ không phải 1. Chỉ số tự nhiên liên '
         'tiếp mới cách nhau 1.'],
        ['Đọc cho con vài câu rồi hỏi hiệu bằng mấy: "hai số liên tiếp", "hai số lẻ liên '
         'tiếp", "bớt số lớn 5 thì bằng nhau". Con dịch được ba câu này là nắm bài.',
         'Bài này khó ở chỗ ĐỌC HIỂU chứ không ở phép tính. Bố mẹ đọc chậm giúp con.'],
    ),
    [
        lt(1, 1, 'Hai số tự nhiên liên tiếp có tổng bằng 71 — đúng bài trong video. Hiệu '
                 'của hai số bằng bao nhiêu?',
           'Hai số tự nhiên liên tiếp hơn kém nhau 1 đơn vị, nên hiệu bằng 1.'),
        lt(2, 1, 'Vẫn bài trên. Tìm hai số đó.',
           'Số lớn = (71 + 1) : 2 = 36; số bé = 71 − 36 = 35.'),
        lt(3, 1, 'Hai số chẵn liên tiếp thì hiệu của chúng bằng bao nhiêu?',
           'Bằng 2 — ví dụ 4 và 6 cách nhau 2 đơn vị.'),
        lt(4, 2, 'Hai số chẵn liên tiếp có tổng bằng 42. Tìm hai số.',
           'Hiệu bằng 2. Số lớn = (42 + 2) : 2 = 22; số bé = 20.'),
        lt(5, 2, 'Bạn Tú thấy "hai số chẵn liên tiếp" rồi lấy hiệu bằng 1. Bạn sai ở đâu?',
           'Hai số chẵn liên tiếp cách nhau 2 đơn vị chứ không phải 1. Chỉ số tự nhiên '
           'liên tiếp mới cách nhau 1.'),
        lt(6, 2, 'Tổng hai số là 100. Nếu bớt số lớn đi 8 thì hai số bằng nhau. Tìm hai số.',
           'Bớt 8 thì bằng nhau nghĩa là hiệu bằng 8. Số lớn = (100 + 8) : 2 = 54; số '
           'bé = 46.'),
        lt(7, 2, 'Hai số lẻ liên tiếp có tổng bằng 56. Tìm hai số.',
           'Hai số lẻ liên tiếp cách nhau 2. Số lớn = (56 + 2) : 2 = 29; số bé = 27.'),
        lt(8, 3, 'Hai kho có tất cả 180 tấn thóc. Nếu chuyển 15 tấn từ kho lớn sang kho '
                 'bé thì hai kho bằng nhau. Tìm số thóc mỗi kho.',
           'Chuyển 15 tấn thì bằng nhau, nghĩa là kho lớn hơn kho bé 15 × 2 = 30 tấn. '
           'Kho lớn = (180 + 30) : 2 = 105 tấn; kho bé = 75 tấn.'),
        lt(9, 3, 'Ba số tự nhiên liên tiếp có tổng bằng 96. Tìm ba số đó.',
           'Số ở giữa bằng 96 : 3 = 32. Ba số là 31, 32 và 33.'),
        q_tf(1, 'Hai số tự nhiên liên tiếp có hiệu bằng 1.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Hai số chẵn liên tiếp có hiệu bằng 1.', False,
             'SAI — chúng cách nhau 2 đơn vị.'),
        q_mcq(3, 'Hai số lẻ liên tiếp có hiệu bằng:',
              ['A. 2', 'B. 1', 'C. 3'], 'A. 2', 'Ví dụ 5 và 7.'),
        q_mcq(4, '"Bớt số lớn đi 8 thì hai số bằng nhau" nghĩa là hiệu bằng:',
              ['A. 8', 'B. 4', 'C. 16'], 'A. 8', 'Bớt đúng phần dôi ra.'),
        q_mcq(5, '"Chuyển 15 từ số lớn sang số bé thì bằng nhau" nghĩa là hiệu bằng:',
              ['A. 30', 'B. 15', 'C. 7'], 'A. 30',
              'Chuyển đi 15 thì bên kia được thêm 15, nên hiệu là hai lần 15.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B27 · CÙNG THÊM VÀO CẢ HAI SỐ — HIỆU KHÔNG ĐỔI  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ gộp dạng này VỚI dạng ba số. Nay tách. Cái đáng dạy ở đây chỉ có một: cùng
# thêm vào cả hai thì hiệu ĐỨNG YÊN còn tổng tăng gấp đôi phần thêm — và nhìn sơ đồ
# là thấy ngay, vì hai đoạn cùng dài thêm một khúc như nhau.
B27 = bai(
    27, 'CÙNG THÊM VÀO CẢ HAI SỐ — HIỆU ĐỨNG YÊN, TỔNG TĂNG GẤP ĐÔI',
    'Dạng gốc: LV 2.4 mức Lớp 4 — Bài toán tuổi: cùng thêm t vào cả hai số thì hiệu '
    'không đổi, tổng tăng thêm hai lần t.',
    'Con đã biết tìm hai số khi có tổng và hiệu. Hôm nay con xem điều gì xảy ra khi CẢ '
    'HAI số cùng lớn lên — như tuổi của hai người sau vài năm. Nhìn sơ đồ là con thấy '
    'ngay cái gì đổi và cái gì đứng yên.',
    LUI_TUOI,
    video(
        ['Biết cùng thêm vào cả hai số thì hiệu không đổi.',
         'Biết tổng tăng thêm hai lần phần vừa thêm.',
         'Giải được bài toán tuổi bằng hai điều đó.'],
        ['Đề bài: Hiện nay tổng số tuổi của hai anh em là 20, anh hơn em 4 tuổi. Hỏi '
         'sau 3 năm nữa mỗi người bao nhiêu tuổi?',
         'Nhìn sơ đồ trước',
         'Hai đoạn thẳng, khúc dôi ra là 4. Sau 3 năm, CẢ HAI đoạn cùng dài thêm 3.',
         'Hiệu không đổi',
         'Vì hai đoạn cùng dài thêm đúng 3 nên khúc dôi ra vẫn y nguyên. Anh vẫn hơn em '
         '4 tuổi, mãi mãi.',
         'Tổng thì tăng gấp đôi phần thêm',
         'Mỗi người thêm 3 tuổi, hai người nên tổng thêm 3 × 2 = 6. Tổng mới là '
         '20 + 6 = 26.',
         'Bây giờ mới tính',
         'Tuổi anh sau 3 năm = (26 + 4) : 2 = 15. Tuổi em = 26 − 15 = 11.',
         'Đáp số: sau 3 năm anh 15 tuổi, em 11 tuổi.'],
        ['Có bạn nghĩ sau 3 năm thì hiệu tuổi cũng tăng lên thành 7.',
         'Gợi ý 1: Con vẽ hai đoạn ra rồi cùng nối thêm một khúc 3 vào cả hai xem.',
         'Gợi ý 2: Khúc dôi ra có dài thêm không?',
         'Chữa: không. Hai đoạn cùng dài thêm như nhau thì khúc dôi ra y nguyên, nên '
         'hiệu tuổi mãi là 4. Chỉ TỔNG mới đổi.'],
        ['Hỏi con: "Bố hơn con mấy tuổi? Mười năm nữa bố hơn con mấy tuổi?" Con trả lời '
           'đúng cùng một số là đã hiểu.',
         'Đây là chỗ con hay sai nhất trong bài toán tuổi. Bố mẹ nhấn một câu: hiệu tuổi '
         'không bao giờ đổi.'],
    ),
    [
        lt(1, 1, 'Tổng tuổi hai anh em hiện nay là 20, anh hơn em 4 tuổi — đúng bài trong '
                 'video. Sau 3 năm anh còn hơn em mấy tuổi?',
           'Vẫn 4 tuổi. Cả hai cùng thêm 3 tuổi nên hiệu không đổi.'),
        lt(2, 1, 'Vẫn bài trên. Sau 3 năm tổng số tuổi hai anh em bằng bao nhiêu?',
           'Mỗi người thêm 3, hai người nên tổng thêm 3 × 2 = 6. Tổng mới = 20 + 6 = 26.'),
        lt(3, 1, 'Vẫn bài trên. Sau 3 năm anh bao nhiêu tuổi?',
           'Tuổi anh = (26 + 4) : 2 = 15 tuổi.'),
        lt(4, 2, 'Bạn Hoa nghĩ sau 3 năm hiệu tuổi thành 7. Bạn sai ở đâu?',
           'Cả hai cùng thêm 3 tuổi nên khúc dôi ra trên sơ đồ y nguyên. Hiệu tuổi mãi '
           'là 4, không bao giờ đổi.'),
        lt(5, 2, 'Tổng tuổi hai chị em hiện nay là 30, chị hơn em 6 tuổi. Sau 5 năm tổng '
                 'tuổi hai người bằng bao nhiêu?',
           'Tổng thêm 5 × 2 = 10, thành 30 + 10 = 40.'),
        lt(6, 2, 'Vẫn bài trên. Sau 5 năm chị bao nhiêu tuổi, em bao nhiêu tuổi?',
           'Hiệu vẫn 6. Chị = (40 + 6) : 2 = 23 tuổi; em = 40 − 23 = 17 tuổi.'),
        lt(7, 2, 'Vì sao cùng thêm vào cả hai số thì hiệu không đổi?',
           'Vì trên sơ đồ hai đoạn cùng dài thêm một khúc bằng nhau, nên khúc dôi ra '
           'của đoạn dài so với đoạn ngắn vẫn y nguyên.'),
        lt(8, 3, 'Hiện nay mẹ hơn con 26 tuổi. Sau 4 năm tổng số tuổi hai mẹ con là 52. '
                 'Hỏi hiện nay mỗi người bao nhiêu tuổi?',
           'Tổng hiện nay = 52 − 4 × 2 = 44. Mẹ = (44 + 26) : 2 = 35 tuổi; con = 9 tuổi.'),
        lt(9, 3, 'Tổng tuổi hai anh em hiện nay là 20, anh hơn em 4 tuổi. Cách đây 2 năm '
                 'tổng tuổi hai người là bao nhiêu, và em mấy tuổi?',
           'Lùi 2 năm thì tổng bớt 2 × 2 = 4, còn 16. Hiệu vẫn 4. Em = (16 − 4) : 2 = 6 tuổi.'),
        q_tf(1, 'Cùng thêm một số năm vào tuổi cả hai người thì hiệu tuổi không đổi.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Sau 3 năm thì hiệu tuổi của hai anh em tăng thêm 3.', False,
             'SAI — hiệu tuổi không bao giờ đổi.'),
        q_mcq(3, 'Hai người mỗi người thêm 3 tuổi thì tổng tuổi tăng thêm:',
              ['A. 6', 'B. 3', 'C. 9'], 'A. 6', 'Ba tuổi nhân hai người.'),
        q_mcq(4, 'Anh hơn em 4 tuổi. Mười năm nữa anh hơn em:',
              ['A. 4 tuổi', 'B. 14 tuổi', 'C. 24 tuổi'], 'A. 4 tuổi',
              'Hiệu tuổi không đổi.'),
        q_mcq(5, 'Trên sơ đồ, cùng thêm vào cả hai đoạn thì:',
              ['A. khúc dôi ra y nguyên', 'B. khúc dôi ra dài thêm',
               'C. khúc dôi ra ngắn đi'], 'A. khúc dôi ra y nguyên',
              'Hai đoạn cùng dài thêm bằng nhau.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑦ B60 · BA SỐ, BIẾT TỔNG VÀ HAI HIỆU
# ═══════════════════════════════════════════════════════════════════════════
# Tách ra khỏi B27 vì nó là một dạng khác hẳn — ba đoạn thẳng chứ không phải hai, và
# cách làm là quy về đoạn ngắn nhất. Bài khép chương.
B60 = bai(
    60, 'BA SỐ BIẾT TỔNG VÀ HAI HIỆU — QUY VỀ ĐOẠN NGẮN NHẤT',
    'Dạng gốc: LV 2.5 mức Lớp 4 — Ba số biết tổng và hai hiệu so với số bé nhất; vẽ '
    'ba đoạn thẳng và cắt cho bằng đoạn ngắn nhất.',
    'Bài cuối chương, và là bài dùng lại tất cả. Lần này có BA số chứ không phải hai, '
    'nên sơ đồ có ba đoạn. Cách làm vẫn đúng như cũ: cắt cho ba đoạn bằng nhau, rồi '
    'chia đều.',
    LUI_HON,
    video(
        ['Vẽ được sơ đồ ba đoạn thẳng.',
         'Cắt bớt cho ba đoạn bằng nhau rồi chia ba.',
         'Tìm lại được hai số kia sau khi có số bé nhất.'],
        ['Đề bài: Ba số có tổng bằng 90. Số thứ hai hơn số thứ nhất 5, số thứ ba hơn số '
         'thứ nhất 10. Tìm ba số.',
         'Vẽ ba đoạn',
         'Đoạn thứ nhất ngắn nhất. Đoạn thứ hai dôi ra 5, đoạn thứ ba dôi ra 10.',
         'Cắt cho ba đoạn bằng nhau',
         'Cắt bỏ khúc 5 của đoạn hai và khúc 10 của đoạn ba. Bây giờ ba đoạn bằng nhau, '
         'mỗi đoạn đúng bằng số thứ nhất.',
         'Xem tổng đổi thế nào',
         'Ta vừa cắt đi 5 và 10, tất cả là 15. Tổng còn 90 − 15 = 75.',
         'Chia ba',
         '75 là ba lần số thứ nhất, nên số thứ nhất là 75 : 3 = 25.',
         'Tìm hai số kia',
         'Số thứ hai = 25 + 5 = 30. Số thứ ba = 25 + 10 = 35. Thử lại: 25 + 30 + 35 = 90.',
         'Đáp số: ba số là 25, 30 và 35.'],
        ['Có bạn cắt xong rồi vẫn chia đôi như bài hai số, được 75 chia 2.',
         'Gợi ý 1: Sau khi cắt, con còn mấy đoạn bằng nhau?',
         'Gợi ý 2: Còn BA đoạn. Vậy chia cho mấy?',
         'Chữa: chia cho 3, được 75 : 3 = 25. Có mấy đoạn bằng nhau thì chia cho bấy '
         'nhiêu, không phải lúc nào cũng chia đôi.'],
        ['Bảo con vẽ ba đoạn rồi lấy bút gạch bỏ hai khúc dôi ra. Con nhìn thấy ba đoạn '
         'bằng nhau thì sẽ chia ba chứ không chia hai.',
         'Chỗ sai duy nhất của bài này là chia nhầm số. Bố mẹ hỏi: "Còn mấy đoạn bằng '
         'nhau?"'],
    ),
    [
        lt(1, 1, 'Ba số có tổng 90, số hai hơn số một 5, số ba hơn số một 10 — đúng bài '
                 'trong video. Cắt bỏ hai khúc dôi ra thì tổng còn bao nhiêu?',
           'Cắt đi 5 và 10, tất cả 15. Tổng còn 90 − 15 = 75.'),
        lt(2, 1, 'Vẫn bài trên. Sau khi cắt còn mấy đoạn bằng nhau, và số thứ nhất bằng '
                 'bao nhiêu?',
           'Còn 3 đoạn bằng nhau. Số thứ nhất = 75 : 3 = 25.'),
        lt(3, 1, 'Vẫn bài trên. Tìm số thứ hai và số thứ ba.',
           'Số thứ hai = 25 + 5 = 30; số thứ ba = 25 + 10 = 35.'),
        lt(4, 2, 'Bạn Minh cắt xong rồi chia 75 cho 2. Bạn sai ở đâu?',
           'Sau khi cắt còn BA đoạn bằng nhau nên phải chia cho 3, được 25.'),
        lt(5, 2, 'Ba số có tổng 60. Số hai hơn số một 3, số ba hơn số một 6. Tìm số thứ nhất.',
           'Tổng sau khi cắt = 60 − 3 − 6 = 51. Số thứ nhất = 51 : 3 = 17.'),
        lt(6, 2, 'Vẫn bài trên. Tìm số thứ hai và số thứ ba, rồi thử lại.',
           'Số hai = 17 + 3 = 20; số ba = 17 + 6 = 23. Thử: 17 + 20 + 23 = 60, đúng.'),
        lt(7, 2, 'Vì sao phải cắt bỏ các khúc dôi ra trước khi chia?',
           'Vì chỉ khi ba đoạn bằng nhau thì phép chia đều mới cho ra đúng một đoạn. '
           'Còn khúc dôi ra thì ba đoạn không bằng nhau.'),
        lt(8, 3, 'Ba lớp trồng được 120 cây. Lớp B trồng hơn lớp A 8 cây, lớp C trồng '
                 'hơn lớp A 16 cây. Mỗi lớp trồng bao nhiêu cây?',
           'Tổng sau khi cắt = 120 − 8 − 16 = 96. Lớp A = 96 : 3 = 32 cây; lớp B = 40 '
           'cây; lớp C = 48 cây.'),
        lt(9, 3, 'Ba số có tổng 99. Số thứ hai hơn số thứ nhất 6, số thứ ba hơn số thứ '
                 'nhất 12. Tìm ba số rồi thử lại.',
           'Tổng sau khi cắt = 99 − 6 − 12 = 81. Số thứ nhất = 81 : 3 = 27; số thứ hai '
           '= 33; số thứ ba = 39. Thử: 27 + 33 + 39 = 99, đúng.'),
        q_tf(1, 'Sau khi cắt bỏ các khúc dôi ra, ba đoạn bằng nhau nên chia cho 3.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Bài ba số cũng chia đôi như bài hai số.', False,
             'SAI — có mấy đoạn bằng nhau thì chia cho bấy nhiêu.'),
        q_mcq(3, 'Ba số tổng 90, hai khúc dôi ra là 5 và 10. Sau khi cắt, tổng còn:',
              ['A. 75', 'B. 85', 'C. 90'], 'A. 75', '90 − 5 − 10 = 75.'),
        q_mcq(4, 'Sau khi cắt còn 75 và ba đoạn bằng nhau, số thứ nhất là:',
              ['A. 25', 'B. 37', 'C. 15'], 'A. 25', '75 : 3 = 25.'),
        q_mcq(5, 'Trên sơ đồ ba đoạn, đoạn ngắn nhất là:',
              ['A. số thứ nhất', 'B. số thứ hai', 'C. số thứ ba'],
              'A. số thứ nhất', 'Hai số kia đều hơn nó.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
MOI = [B58, B24, B59, B25, B26, B27, B60]
TRUOC = 'DL:KSN4.B23'          # chèn ngay sau bài cuối chương 5

O_NHAP_MOI = {
    # ── ① B58 · sơ đồ đoạn thẳng ──
    'DL:KSN4.B58#C1': {'parts': [{'label': 'khúc dôi ra gọi là',
                                  'options': ['hiệu', 'tổng', 'số bé'], 'value': 'hiệu'},
                                 {'label': 'bằng bao nhiêu', 'value': 10}]},
    'DL:KSN4.B58#C2': {'parts': [{'label': 'ghi ở đâu',
                                  'options': ['ngoặc ôm cả hai đoạn', 'trên đoạn dài',
                                              'trên đoạn ngắn'],
                                  'value': 'ngoặc ôm cả hai đoạn'}]},
    'DL:KSN4.B58#C3': {'parts': [{'label': 'đoạn ngắn là',
                                  'options': ['số bé', 'số lớn', 'hiệu'], 'value': 'số bé'}]},
    'DL:KSN4.B58#C4': {'parts': [{'label': 'bạn Nam sai vì 70 là',
                                  'options': ['tổng', 'số lớn', 'hiệu'], 'value': 'tổng'}]},
    'DL:KSN4.B58#C5': {'parts': [{'label': 'khúc dôi ra', 'value': 20},
                                 {'label': 'ngoặc ngoài ghi', 'value': 100}]},
    'DL:KSN4.B58#C6': {'value': 0},
    'DL:KSN4.B58#C7': {'parts': [{'label': 'khúc dôi ra', 'value': 3},
                                 {'label': 'ngoặc ngoài ghi', 'value': 13}]},
    'DL:KSN4.B58#C8': {'parts': [{'label': 'đoạn dài', 'value': 40},
                                 {'label': 'tổng', 'value': 70}]},
    'DL:KSN4.B58#C9': {'value': 35},

    # ── ② B24 · số lớn ──
    'DL:KSN4.B24#C1': {'value': 80},
    'DL:KSN4.B24#C2': {'parts': [{'label': '80 là của mấy đoạn', 'value': 2},
                                 {'label': 'số lớn', 'value': 40}]},
    'DL:KSN4.B24#C3': {'value': 20},
    'DL:KSN4.B24#C4': {'value': 86},
    'DL:KSN4.B24#C5': {'parts': [{'label': 'bạn Lan quên bước', 'options': ['chia hai', 'cộng hiệu'],
                                  'value': 'chia hai'},
                                 {'label': 'số lớn đúng', 'value': 40}]},
    'DL:KSN4.B24#C6': {'parts': [{'label': 'đoạn ngắn thiếu đúng một khúc bằng',
                                  'options': ['hiệu', 'tổng'], 'value': 'hiệu'}]},
    'DL:KSN4.B24#C7': {'value': 280},
    'DL:KSN4.B24#C8': {'parts': [{'label': 'số lớn', 'value': 55},
                                 {'label': 'số bé', 'value': 41}]},
    'DL:KSN4.B24#C9': {'value': 15},

    # ── ③ B59 · số bé ──
    'DL:KSN4.B59#C1': {'value': 60},
    'DL:KSN4.B59#C2': {'parts': [{'label': '60 là của mấy đoạn', 'value': 2},
                                 {'label': 'số bé', 'value': 30}]},
    'DL:KSN4.B59#C3': {'value': 10},
    'DL:KSN4.B59#C4': {'value': 59},
    'DL:KSN4.B59#C5': {'parts': [{'label': 'phải lấy', 'options': ['tổng trừ hiệu', 'hiệu trừ tổng'],
                                  'value': 'tổng trừ hiệu'},
                                 {'label': 'số bé đúng', 'value': 30}]},
    'DL:KSN4.B59#C6': {'parts': [{'label': 'số lớn', 'value': 40},
                                 {'label': 'số bé', 'value': 30}]},
    'DL:KSN4.B59#C7': {'value': 220},
    'DL:KSN4.B59#C8': {'parts': [{'label': 'số lớn', 'value': 55},
                                 {'label': 'số bé', 'value': 41}]},
    'DL:KSN4.B59#C9': {'parts': [{'label': 'chiều rộng', 'value': 9},
                                 {'label': 'diện tích', 'value': 135}]},

    # ── ④ B25 · tổng bị giấu ──
    'DL:KSN4.B25#C1': {'value': 70},
    'DL:KSN4.B25#C2': {'parts': [{'label': 'số lớn', 'value': 40},
                                 {'label': 'số bé', 'value': 30}]},
    'DL:KSN4.B25#C3': {'value': 24},
    'DL:KSN4.B25#C4': {'parts': [{'label': 'chiều dài', 'value': 5},
                                 {'label': 'chiều rộng', 'value': 4}]},
    'DL:KSN4.B25#C5': {'parts': [{'label': 'tổng đúng', 'value': 70}]},
    'DL:KSN4.B25#C6': {'parts': [{'label': 'tổng', 'value': 40},
                                 {'label': 'số lớn', 'value': 24},
                                 {'label': 'số bé', 'value': 16}]},
    'DL:KSN4.B25#C7': {'parts': [{'label': 'chu vi gồm mấy lần cái tổng ấy', 'value': 2}]},
    'DL:KSN4.B25#C8': {'parts': [{'label': 'chiều dài', 'value': 20},
                                 {'label': 'diện tích', 'value': 200}]},
    'DL:KSN4.B25#C9': {'parts': [{'label': 'số lớn', 'value': 56},
                                 {'label': 'số bé', 'value': 44}]},

    # ── ⑤ B26 · hiệu bị giấu ──
    'DL:KSN4.B26#C1': {'value': 1},
    'DL:KSN4.B26#C2': {'parts': [{'label': 'số lớn', 'value': 36},
                                 {'label': 'số bé', 'value': 35}]},
    'DL:KSN4.B26#C3': {'value': 2},
    'DL:KSN4.B26#C4': {'parts': [{'label': 'số lớn', 'value': 22},
                                 {'label': 'số bé', 'value': 20}]},
    'DL:KSN4.B26#C5': {'parts': [{'label': 'hiệu đúng', 'value': 2}]},
    'DL:KSN4.B26#C6': {'parts': [{'label': 'hiệu', 'value': 8},
                                 {'label': 'số lớn', 'value': 54},
                                 {'label': 'số bé', 'value': 46}]},
    'DL:KSN4.B26#C7': {'parts': [{'label': 'số lớn', 'value': 29},
                                 {'label': 'số bé', 'value': 27}]},
    'DL:KSN4.B26#C8': {'parts': [{'label': 'hiệu', 'value': 30},
                                 {'label': 'kho lớn', 'value': 105},
                                 {'label': 'kho bé', 'value': 75}]},
    'DL:KSN4.B26#C9': {'parts': [{'label': 'số ở giữa', 'value': 32},
                                 {'label': 'số bé nhất', 'value': 31}]},

    # ── ⑥ B27 · cùng thêm vào cả hai ──
    'DL:KSN4.B27#C1': {'value': 4},
    'DL:KSN4.B27#C2': {'value': 26},
    'DL:KSN4.B27#C3': {'value': 15},
    'DL:KSN4.B27#C4': {'parts': [{'label': 'hiệu tuổi sau 3 năm', 'value': 4}]},
    'DL:KSN4.B27#C5': {'value': 40},
    'DL:KSN4.B27#C6': {'parts': [{'label': 'tuổi chị', 'value': 23},
                                 {'label': 'tuổi em', 'value': 17}]},
    'DL:KSN4.B27#C7': {'parts': [{'label': 'khúc dôi ra có đổi không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B27#C8': {'parts': [{'label': 'tuổi mẹ', 'value': 35},
                                 {'label': 'tuổi con', 'value': 9}]},
    'DL:KSN4.B27#C9': {'parts': [{'label': 'tổng cách đây 2 năm', 'value': 16},
                                 {'label': 'tuổi em khi đó', 'value': 6}]},

    # ── ⑦ B60 · ba số ──
    'DL:KSN4.B60#C1': {'value': 75},
    'DL:KSN4.B60#C2': {'parts': [{'label': 'còn mấy đoạn bằng nhau', 'value': 3},
                                 {'label': 'số thứ nhất', 'value': 25}]},
    'DL:KSN4.B60#C3': {'parts': [{'label': 'số thứ hai', 'value': 30},
                                 {'label': 'số thứ ba', 'value': 35}]},
    'DL:KSN4.B60#C4': {'parts': [{'label': 'phải chia cho', 'value': 3}]},
    'DL:KSN4.B60#C5': {'value': 17},
    'DL:KSN4.B60#C6': {'parts': [{'label': 'số thứ hai', 'value': 20},
                                 {'label': 'số thứ ba', 'value': 23}]},
    'DL:KSN4.B60#C7': {'parts': [{'label': 'chỉ khi ba đoạn thế nào thì mới chia đều được',
                                  'options': ['bằng nhau', 'khác nhau'],
                                  'value': 'bằng nhau'}]},
    'DL:KSN4.B60#C8': {'parts': [{'label': 'lớp A', 'value': 32},
                                 {'label': 'lớp B', 'value': 40},
                                 {'label': 'lớp C', 'value': 48}]},
    'DL:KSN4.B60#C9': {'parts': [{'label': 'số thứ nhất', 'value': 27},
                                 {'label': 'số thứ hai', 'value': 33},
                                 {'label': 'số thứ ba', 'value': 39}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)

    # Bài khái niệm KHÔNG được nêu công thức — nêu ra là hai bài sau mất chỗ đứng.
    van = ' '.join(x['text'] + x['loiChua'] for x in B58['cau'])
    if '(tổng + hiệu)' in van or 'tổng cộng hiệu rồi chia' in van:
        loi.append('B58 là bài KHÁI NIỆM, chưa được nêu công thức')

    cu = {f'DL:KSN4.B{n}' for n in (24, 25, 26, 27)}
    moi_ = {f'DL:KSN4.B{n}' for n in (58, 59, 60)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')

    # Bộ neo tổng 70 · hiệu 10 phải chạy suốt — luật 3.
    NEO = ('70', '40', '30')
    for b in MOI:
        van = json.dumps(b, ensure_ascii=False)
        if not any(x in van for x in NEO):
            loi.append(f'{b["id"]}: thiếu bộ neo tổng 70 hiệu 10 của chương')
    return loi


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--xem', action='store_true', help='in ra, không ghi')
    a = p.parse_args()

    loi = soi()
    if loi:
        for x in loi:
            print('  ✗', x)
        sys.exit(f'{len(loi)} chỗ chưa đạt — chưa ghi gì cả')

    for b in MOI:
        n = sum(1 for c in b['cau'] if c['phan'] == 'luyenTap')
        q = sum(1 for c in b['cau'] if c['phan'] == 'quiz')
        print(f"  {b['id']}  {b['ten'][:56]:56} {n} luyện + {q} quiz")
    if a.xem:
        print('\n(--xem: chưa ghi gì)')
        return

    for b in MOI:
        tep = RA / f"DL_KSN4_B{b['so']:02d}.json"
        if tep.exists():
            cu = json.loads(tep.read_text('utf8'))
            for ten, m in b['muc'].items():
                cu_m = cu.get('muc', {}).get(ten)
                if isinstance(cu_m, dict) and cu_m.get('hinh') and not m.get('hinh'):
                    m['hinh'] = cu_m['hinh']
        tep.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n', 'utf8')

    tt = json.loads(THU_TU.read_text('utf8'))
    ds = [x for x in tt['thuTu'] if x not in {b['id'] for b in MOI}]
    i = ds.index(TRUOC) + 1
    tt['thuTu'] = ds[:i] + [b['id'] for b in MOI] + ds[i:]
    THU_TU.write_text(json.dumps(tt, ensure_ascii=False, indent=1) + '\n', 'utf8')

    o = json.loads(O_NHAP.read_text('utf8'))
    o.update(O_NHAP_MOI)
    O_NHAP.write_text(json.dumps(o, ensure_ascii=False, indent=1) + '\n', 'utf8')

    print(f'\nghi {len(MOI)} bài vào {RA.relative_to(GOC)}')
    print(f'thứ tự học nay {len(tt["thuTu"])} bài (chèn sau {TRUOC})')
    print(f'thêm {len(O_NHAP_MOI)} ô nhập (nay {len(o)} mục)')


if __name__ == '__main__':
    main()
