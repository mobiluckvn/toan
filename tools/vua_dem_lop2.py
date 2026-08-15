# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 2 · BÉ LÀ VUA ĐẾM — ba bài chữ thành sáu bài video.

  · B06 gộp "đếm từ a đến b" với "đếm nhảy cóc" — hai nghề khác nhau;
  · B07 gộp "chia hai cánh quân" với "số đứng cả hai cánh thì bớt một";
  · B08 gộp "trang khác chữ số" với "cộng hai đoàn tàu".

── SỐ NEO ──
    từ nhà 3 đến nhà 7   → 5 nhà, và phép trừ chỉ ra 4
    2, 4, 6, 8, 10       → đếm nhảy cóc cách hai
    chữ số 5 từ 1 tới 99 → 10 cộng 10 bớt 1, bằng 19
    cuốn 25 trang        → 9 cộng 32, bằng 41 chữ số

    python3 tools/vua_dem_lop2.py --xem
    python3 tools/vua_dem_lop2.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from khuon_bai_lop2 import (                                       # noqa: E402
    lt, q_tf, q_mcq, dung_muc, soi_bai, bai as _bai,
)

GOC = Path(__file__).resolve().parent.parent
RA = GOC / 'data' / 'lop2'
TAY = GOC / 'data' / 'lop2_dapan_tay.json'
THU_TU = RA / 'thu_tu.json'

TEN_CHUONG = 'Bé là vua đếm'
CHUONG = 2
CO_KHONG = ['có', 'không']
HANG = ['hàng đơn vị', 'hàng chục']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B06 · ĐẾM TỪ ĐÂU ĐẾN ĐÂU ═══
B06 = bai(
    6, 'ĐẾM TỪ ĐÂU ĐẾN ĐÂU — TRỪ RỒI THÊM MỘT',
    'SỐ 4.1 — Đếm số lượng các số trong một khoảng: trừ hai đầu rồi thêm một.',
    video(
        ['Đếm được có bao nhiêu số từ số này đến số kia.',
         'Biết lấy số cuối trừ số đầu rồi thêm một.',
         'Nói được vì sao phải thêm một.'],
        ['Đề bài: Từ nhà số 3 đến nhà số 7 có bao nhiêu ngôi nhà?',
         'Đếm thẳng tay xem sao',
         'Nhà 3, nhà 4, nhà 5, nhà 6, nhà 7. Đúng 5 nhà.',
         'Nhưng phép trừ lại ra 4',
         'Bảy trừ ba bằng bốn. Lệch mất một nhà. Vì sao thế?',
         'Vì phép trừ chỉ đếm BƯỚC NHẢY từ nhà nọ sang nhà kia. Mà nhà đầu tiên thì '
         'chưa nhảy bước nào đã đứng sẵn ở đó rồi.',
         'Nên phải thêm một',
         'Bảy trừ ba bằng bốn, thêm một được năm.',
         'Đáp số: 5 ngôi nhà.',
         'Thử lại bằng cách đếm tay: ba, bốn, năm, sáu, bảy — đúng năm nhà.'],
        ['Có bạn tính từ nhà 3 đến nhà 7 rồi ghi luôn 4 nhà, vì bảy trừ ba bằng bốn.',
         'Gợi ý 1: Con đếm tay thử xem được mấy nhà.',
         'Gợi ý 2: Phép trừ đếm bước nhảy hay đếm nhà? Nhà đầu tiên có phải nhảy bước '
         'nào mới tới không?',
         'Chữa: bốn là số bước nhảy. Nhà đầu tiên đứng sẵn ở đó nên phải đếm nó vào '
         'nữa, thành năm nhà.'],
        ['Đếm bậc cầu thang cùng con: từ bậc 1 lên bậc 5 thì bước mấy bước. Bước có '
         'bốn mà bậc thì năm — đúng cái bẫy của bài này.',
         'Bố mẹ chỉ cần hỏi một câu mỗi lần: "Con vừa đếm bước nhảy hay đếm số?"'],
    ),
    [
        lt(1, 1, 'Đếm xem có bao nhiêu số từ 1 đến 8.',
           'Đếm tay: một, hai, ba cho tới tám — được 8 số.'),
        lt(2, 1, 'Tính 7 − 3, rồi thêm 1 vào kết quả.',
           'Lấy hiệu: 7 − 3 = 4. Thêm một được 5.'),
        lt(3, 1, 'Từ 4 đến 9 có bao nhiêu số?',
           'Lấy hiệu: 9 − 4 = 5, thêm một được 6 số.'),
        lt(4, 2, 'Từ 10 đến 20 có bao nhiêu số?',
           'Lấy hiệu: 20 − 10 = 10, thêm một được 11 số.'),
        lt(5, 2, 'Vì sao đếm xong phép trừ lại phải thêm một?',
           'Vì phép trừ chỉ đếm bước nhảy, mà số đầu tiên chưa nhảy đã đứng sẵn ở đó.'),
        lt(6, 2, 'Từ 15 đến 15 có bao nhiêu số?',
           'Lấy hiệu: 15 − 15 = 0, thêm một được 1 số. Đúng là chỉ có chính nó.'),
        lt(7, 3, 'Từ 21 đến 30 có bao nhiêu số?',
           'Lấy hiệu: 30 − 21 = 9, thêm một được 10 số.'),
        lt(8, 3, 'Một dãy bắt đầu từ số 6 và có 9 số liền nhau. Số cuối cùng là số nào?',
           'Có 9 số thì có 8 bước nhảy: 6 + 8 = 14.'),
    ] + [
        q_tf(1, 'Đếm từ số này đến số kia thì trừ hai đầu rồi thêm một.', True,
             'Đúng, và chữ "thêm một" là chỗ hay quên nhất.'),
        q_tf(2, 'Từ nhà 3 đến nhà 7 có 4 nhà.', False,
             'Sai. Bốn là số bước nhảy; đếm nhà thì được 5.'),
        q_mcq(3, 'Từ 4 đến 9 có bao nhiêu số?', ['6', '5', '4', '13'], '6',
              'Lấy 9 trừ 4 được 5, thêm một là 6.'),
        q_mcq(4, 'Vì sao phải thêm một?',
              ['vì số đầu tiên chưa nhảy đã đứng sẵn ở đó', 'vì cho tròn số',
               'vì đếm cho vui'],
              'vì số đầu tiên chưa nhảy đã đứng sẵn ở đó',
              'Phép trừ đếm bước nhảy chứ không đếm số.'),
        q_tf(5, 'Từ 15 đến 15 có 1 số.', True,
             'Đúng. Hiệu bằng không, thêm một được một.'),
    ],
)

# ═══ ② B39 · ĐẾM NHẢY CÓC ═══
B39 = bai(
    39, 'ĐẾM NHẢY CÓC — CÁCH 2 VÀ CÁCH 5',
    'SỐ 4.1 — Đếm theo dãy nhảy cóc cách 2 và cách 5; số chẵn và số lẻ.',
    video(
        ['Viết tiếp được dãy nhảy cóc cách 2 và cách 5.',
         'Biết dãy cách 2 bắt đầu từ 2 là dãy số chẵn, bắt đầu từ 1 là dãy số lẻ.',
         'Đếm được dãy nhảy cóc có bao nhiêu số.'],
        ['Đề bài: Viết tiếp dãy 2, 4, 6 và dãy 5, 10, 15. Rồi đếm xem từ 2 đến 10 '
         'đếm cách hai được mấy số.',
         'Nhảy cóc là gì',
         'Không đếm từng số một, mà mỗi lần nhảy qua một quãng đều nhau.',
         'Dãy cách hai',
         'Hai, bốn, sáu, rồi tám, mười, mười hai. Mỗi lần thêm hai.',
         'Dãy này toàn số chẵn. Bắt đầu từ một thì được dãy số lẻ: một, ba, năm, bảy, '
         'chín.',
         'Dãy cách năm',
         'Năm, mười, mười lăm, rồi hai mươi, hai mươi lăm, ba mươi. Chính là bảng nhân '
         'năm.',
         'Đếm dãy nhảy cóc',
         'Từ hai đến mười đếm cách hai: hai, bốn, sáu, tám, mười — đúng 5 số.',
         'Đáp số: 8, 10, 12 và 20, 25, 30; từ 2 đến 10 có 5 số.'],
        ['Có bạn viết tiếp dãy 5, 10, 15 thành 16, 17, 18.',
         'Gợi ý 1: Con xem từ số năm sang số mười thì nhảy qua bao nhiêu.',
         'Gợi ý 2: Nhảy cóc thì mỗi lần đều nhảy đúng bằng nhau. Lần sau cũng phải '
         'nhảy đúng bấy nhiêu.',
         'Chữa: dãy này nhảy năm một, nên sau mười lăm là hai mươi chứ không phải mười '
         'sáu.'],
        ['Đếm bậc thang hai bậc một cùng con, rồi năm bậc một. Nhảy thật thì nhớ lâu '
         'hơn viết ra giấy.',
         'Dãy cách năm chính là bảng nhân năm. Con thuộc bảng nhân là viết dãy này '
         'không cần nghĩ.'],
    ),
    [
        lt(1, 1, 'Viết tiếp ba số của dãy: 2, 4, 6, ...',
           'Mỗi lần thêm hai, nên tiếp theo là 8, 10, 12.'),
        lt(2, 1, 'Viết tiếp ba số của dãy: 5, 10, 15, ...',
           'Mỗi lần thêm năm, nên tiếp theo là 20, 25, 30.'),
        lt(3, 1, 'Từ 2 đến 10, đếm nhảy cóc cách 2 thì được bao nhiêu số?',
           'Đếm ra: 2, 4, 6, 8, 10 — được 5 số.'),
        lt(4, 2, 'Từ 1 đến 9, các số lẻ có bao nhiêu số?',
           'Đếm ra: 1, 3, 5, 7, 9 — được 5 số.'),
        lt(5, 2, 'Từ 5 đến 30, đếm cách 5 thì được bao nhiêu số?',
           'Đếm ra: 5, 10, 15, 20, 25, 30 — được 6 số.'),
        lt(6, 2, 'Dãy 2, 4, 6, 8, 10 gồm toàn số chẵn hay toàn số lẻ?',
           'Toàn số chẵn, vì dãy bắt đầu từ số 2 và mỗi lần thêm hai.'),
        lt(7, 3, 'Viết tiếp hai số của dãy: 10, 20, 30, ...',
           'Mỗi lần thêm mười, nên tiếp theo là 40, 50.'),
        lt(8, 3, 'Từ 2 đến 20, đếm nhảy cóc cách 2 thì được bao nhiêu số?',
           'Đếm ra: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 — được 10 số.'),
    ] + [
        q_tf(1, 'Dãy nhảy cóc thì mỗi lần nhảy một quãng đều nhau.', True,
             'Đúng. Lần nào cũng nhảy đúng bấy nhiêu.'),
        q_tf(2, 'Sau số 15 trong dãy 5, 10, 15 là số 16.', False,
             'Sai. Dãy này nhảy năm một nên sau 15 là 20.'),
        q_mcq(3, 'Viết tiếp dãy 2, 4, 6, ...', ['8', '7', '9', '12'], '8',
              'Mỗi lần thêm hai.'),
        q_mcq(4, 'Dãy 5, 10, 15, 20 chính là bảng nhân mấy?',
              ['bảng nhân 5', 'bảng nhân 2', 'bảng nhân 10'], 'bảng nhân 5',
              'Mỗi số là năm nhân với một, hai, ba, bốn.'),
        q_tf(5, 'Dãy 1, 3, 5, 7, 9 là dãy số lẻ.', True,
             'Đúng, vì nó bắt đầu từ số 1 và mỗi lần thêm hai.'),
    ],
)

# ═══ ③ B07 · TRUY TÌM CHỮ SỐ — CHIA HAI CÁNH QUÂN ═══
B07 = bai(
    7, 'TRUY TÌM CHỮ SỐ — CHIA HAI CÁNH QUÂN',
    'SỐ 4.2 — Đếm các số chứa một chữ số cho trước: chia thành cánh đuôi và cánh phố.',
    video(
        ['Biết một chữ số có thể trốn ở hàng đơn vị hoặc hàng chục.',
         'Đếm được cánh đuôi: mỗi chục đúng một số.',
         'Đếm được cánh phố: mười số liền nhau.'],
        ['Đề bài: Trong bảng số từ 1 đến 99, chữ số 5 trốn ở những số nào?',
         'Chữ số 5 trốn được hai chỗ',
         'Một là ở hàng đơn vị, tức là số có đuôi bằng năm. Hai là ở hàng chục, tức '
         'là số thuộc phố năm mươi.',
         'Cánh thứ nhất: các số đuôi 5',
         'Năm, mười lăm, hai mươi lăm, cứ thế tới chín mươi lăm. Mỗi chục đúng một '
         'bạn, nên được 10 số.',
         'Cánh thứ hai: phố 50',
         'Năm mươi, năm mươi mốt, cho tới năm mươi chín. Dùng mẹo bài trước: 59 − 50 = '
         '9, thêm một được 10 số.',
         'Đáp số: cánh đuôi 10 số, cánh phố 10 số.',
         'Nhớ cách chia',
         'Truy tìm chữ số nào cũng chia hai cánh như thế: cánh ĐUÔI ở hàng đơn vị, và '
         'cánh PHỐ ở hàng chục.'],
        ['Có bạn tìm số chứa chữ số 5 rồi chỉ kể được 5, 15, 25 và bảo hết.',
         'Gợi ý 1: Con nhìn số 53 xem. Nó có chữ số 5 không, mà đuôi nó có phải 5 '
         'không?',
         'Gợi ý 2: Vậy chữ số 5 còn trốn được ở chỗ nào nữa ngoài hàng đơn vị?',
         'Chữa: bạn ấy mới lùng có một cánh. Còn cả phố năm mươi nữa, từ năm mươi tới '
         'năm mươi chín.'],
        ['In một bảng số từ 1 đến 100 rồi cho con tô màu mọi ô có chữ số 5. Con nhìn '
         'thấy một cột dọc và một hàng ngang hiện ra.',
         'Câu hỏi quen tay: "Chữ số ấy đang trốn ở hàng đơn vị hay hàng chục?"'],
    ),
    [
        lt(1, 1, 'Số nào có chữ số 5 ở hàng đơn vị: số 35 hay số 53?',
           'Số 35 có đuôi là 5, nên chữ số 5 của nó ở hàng đơn vị.'),
        lt(2, 1, 'Số nào có chữ số 5 ở hàng chục: số 35 hay số 53?',
           'Số 53 có chữ số 5 đứng trước, nên nó ở hàng chục.'),
        lt(3, 1, 'Cánh đuôi 5 gồm 5, 15, 25 cho tới 95. Có bao nhiêu số?',
           'Mỗi chục đúng một bạn, từ chục 0 tới chục 9, nên được 10 số.'),
        lt(4, 2, 'Cánh phố 50 gồm các số từ 50 đến 59. Có bao nhiêu số?',
           'Lấy hiệu: 59 − 50 = 9, thêm một được 10 số.'),
        lt(5, 2, 'Trong các số 35, 53, 30, 15 — số nào KHÔNG có chữ số 5?',
           'Số 30 không có chữ số 5 ở hàng nào cả.'),
        lt(6, 2, 'Cánh đuôi 3 gồm 3, 13, 23 cho tới 93. Có bao nhiêu số?',
           'Cũng mỗi chục một bạn, nên được 10 số.'),
        lt(7, 3, 'Cánh phố 30 gồm những số nào? Cho biết số đầu, số cuối và có bao '
                 'nhiêu số.',
           'Từ 30 đến 39. Lấy hiệu: 39 − 30 = 9, thêm một được 10 số.'),
        lt(8, 3, 'Trong mỗi chục có đúng bao nhiêu số có đuôi bằng 5?',
           'Đúng 1 số. Chẳng hạn chục hai mươi thì chỉ có 25.'),
    ] + [
        q_tf(1, 'Một chữ số có thể trốn ở hàng đơn vị hoặc ở hàng chục.', True,
             'Đúng, nên phải lùng cả hai cánh.'),
        q_tf(2, 'Số 53 không có chữ số 5 vì đuôi nó là 3.', False,
             'Sai. Chữ số 5 của nó đứng ở hàng chục.'),
        q_mcq(3, 'Cánh đuôi 5 từ 1 đến 99 có bao nhiêu số?', ['10', '9', '11', '5'],
              '10', 'Mỗi chục đúng một bạn, có mười chục.'),
        q_mcq(4, 'Cánh phố 50 gồm', ['các số từ 50 đến 59', 'chỉ số 50',
                                     'các số đuôi 5'], 'các số từ 50 đến 59',
              'Đó là những số có chữ số 5 ở hàng chục.'),
        q_tf(5, 'Truy tìm chữ số nào cũng chia hai cánh: cánh đuôi và cánh phố.', True,
             'Đúng. Đó là cách lùng không sót.'),
    ],
)

# ═══ ④ B40 · SỐ ĐỨNG Ở CẢ HAI CÁNH ═══
B40 = bai(
    40, 'SỐ ĐỨNG Ở CẢ HAI CÁNH — CHỈ BẮT MỘT LẦN',
    'SỐ 4.2 — Bớt phần đếm trùng khi hai nhóm giao nhau.',
    video(
        ['Cộng hai cánh lại để đếm tất cả.',
         'Nhận ra số đứng ở CẢ HAI cánh thì bị đếm hai lần.',
         'Bớt đúng một lần để ra con số thật.'],
        ['Đề bài: Từ 1 đến 99 có bao nhiêu số chứa chữ số 5?',
         'Cộng hai cánh đã',
         'Cánh đuôi 5 có mười số. Cánh phố 50 cũng có mười số. Cộng lại được hai mươi.',
         'Khoan đã',
         'Nhìn kỹ chỗ hai cánh gặp nhau. Số năm mươi lăm vừa có đuôi là năm, vừa thuộc '
         'phố năm mươi.',
         'Nó đứng ở cả hai cánh, nên khi cộng thì nó bị đếm HAI lần.',
         'Bớt một lần đi',
         'Hai mươi bớt một còn mười chín.',
         'Đáp số: 19 số.',
         'Chữ số nào cũng thế',
         'Với chữ số ba thì số đứng cả hai cánh là ba mươi ba, và kết quả cũng là mười '
         'chín.'],
        ['Có bạn cộng hai cánh được 20 rồi ghi luôn đáp số 20.',
         'Gợi ý 1: Con kể ra cả hai cánh rồi soi xem có số nào bị kể tới hai lần không.',
         'Gợi ý 2: Số nào vừa có đuôi bằng năm, vừa thuộc phố năm mươi?',
         'Chữa: số năm mươi lăm bị đếm hai lần nên phải bớt đi một, còn mười chín.'],
        ['Cho con tô bảng số: tô cột dọc trước, rồi tô hàng ngang. Ô nào bị tô hai lần '
         'thì chính là ô phải bớt.',
         'Câu hỏi nhắc con mỗi lần cộng hai nhóm: "Có bạn nào đứng ở cả hai nhóm '
         'không?"'],
    ),
    [
        lt(1, 1, 'Cánh đuôi 5 có 10 số, cánh phố 50 có 10 số. Cộng hai cánh được bao '
                 'nhiêu?',
           'Cộng lại: 10 + 10 = 20.'),
        lt(2, 1, 'Số nào vừa có đuôi bằng 5, vừa thuộc phố 50?',
           'Đó là số 55 — nó đứng ở cả hai cánh.'),
        lt(3, 1, 'Vậy từ 1 đến 99 có bao nhiêu số chứa chữ số 5?',
           'Bớt số bị đếm hai lần: 20 − 1 = 19 số.'),
        lt(4, 2, 'Vì sao phải bớt đi một?',
           'Vì số 55 bị đếm hai lần, một lần ở cánh đuôi và một lần ở cánh phố.'),
        lt(5, 2, 'Với chữ số 3 thì số nào đứng ở cả hai cánh?',
           'Đó là số 33 — vừa có đuôi bằng 3, vừa thuộc phố 30.'),
        lt(6, 2, 'Vậy từ 1 đến 99 có bao nhiêu số chứa chữ số 3?',
           'Cũng như trên: 10 + 10 = 20, bớt một còn 19 số.'),
        lt(7, 3, 'Từ 1 đến 99 có bao nhiêu số chứa chữ số 7?',
           'Hai cánh mỗi cánh 10 số, số 77 đứng cả hai cánh nên bớt một: còn 19 số.'),
        lt(8, 3, 'Số 55 có bao nhiêu chữ số 5?',
           'Có 2 chữ số 5, một ở hàng chục và một ở hàng đơn vị.'),
    ] + [
        q_tf(1, 'Cộng hai nhóm mà có số đứng ở cả hai thì phải bớt đi.', True,
             'Đúng, nếu không thì số ấy bị đếm hai lần.'),
        q_tf(2, 'Từ 1 đến 99 có 20 số chứa chữ số 5.', False,
             'Sai. Số 55 bị đếm hai lần nên chỉ có 19 số.'),
        q_mcq(3, 'Số nào đứng ở cả cánh đuôi 5 lẫn cánh phố 50?',
              ['55', '50', '5', '95'], '55',
              'Nó vừa có đuôi bằng 5, vừa thuộc phố 50.'),
        q_mcq(4, 'Từ 1 đến 99 có bao nhiêu số chứa chữ số 3?',
              ['19', '20', '10', '18'], '19',
              'Hai cánh cộng lại 20, bớt số 33 bị đếm hai lần.'),
        q_tf(5, 'Số 55 có hai chữ số 5.', True,
             'Đúng, một ở hàng chục và một ở hàng đơn vị.'),
    ],
)

# ═══ ⑤ B08 · TRANG KHÁC CHỮ SỐ ═══
B08 = bai(
    8, 'TRANG KHÁC CHỮ SỐ — CHIA THÀNH HAI ĐOÀN TÀU',
    'SỐ 4.3 — Phân biệt số trang với số chữ số; chia trang thành nhóm một chữ số và '
    'nhóm hai chữ số.',
    video(
        ['Biết một trang có thể cần một hoặc hai chữ số.',
         'Chia số trang thành đoàn tàu một toa và đoàn tàu hai toa.',
         'Đếm được số trang của từng đoàn.'],
        ['Đề bài: Trang 4 cần mấy chữ số? Còn trang 37 thì mấy? Rồi chia cuốn 25 trang '
         'thành hai đoàn tàu.',
         'Trang khác chữ số',
         'Trang bốn chỉ cần dán một chữ số. Nhưng trang ba mươi bảy phải dán hai chữ '
         'số — chữ ba và chữ bảy.',
         'Nên không đếm chung được.',
         'Đoàn tàu một toa',
         'Từ trang một tới trang chín, mỗi trang chỉ một chữ số. Có 9 trang.',
         'Đoàn tàu hai toa',
         'Từ trang mười trở đi, mỗi trang hai chữ số. Với cuốn hai mươi lăm trang thì '
         'đoàn này chạy từ trang mười tới trang hai mươi lăm.',
         'Đếm số trang bằng mẹo bài trước: 25 − 10 = 15, thêm một được 16 trang.',
         'Đáp số: trang 4 cần 1 chữ số, trang 37 cần 2; đoàn một toa có 9 trang, đoàn '
         'hai toa có 16 trang.'],
        ['Có bạn tính cuốn 25 trang rồi bảo cần 25 chữ số, vì mỗi trang một chữ số.',
         'Gợi ý 1: Con nhìn trang 25 xem nó viết bằng mấy chữ số.',
         'Gợi ý 2: Vậy có phải trang nào cũng chỉ tốn một chữ số đâu. Từ trang nào trở '
         'đi thì tốn hai?',
         'Chữa: từ trang mười trở đi mỗi trang tốn hai chữ số. Phải chia hai đoàn tàu '
         'rồi mới đếm.'],
        ['Giở một cuốn truyện của con, chỉ vào trang 9 rồi trang 10. Con thấy tận mắt '
         'chỗ đổi đoàn tàu.',
         'Bố mẹ nhắc một câu: "Con đang đếm TRANG hay đếm CHỮ SỐ?" Hai thứ ấy khác '
         'nhau.'],
    ),
    [
        lt(1, 1, 'Trang 4 cần mấy chữ số để đánh số?',
           'Số 4 viết bằng 1 chữ số.'),
        lt(2, 1, 'Trang 37 cần mấy chữ số để đánh số?',
           'Số 37 viết bằng 2 chữ số, là chữ 3 và chữ 7.'),
        lt(3, 1, 'Từ trang 1 đến trang 9 có mấy trang, và cần mấy chữ số?',
           'Có 9 trang, mỗi trang một chữ số nên cần 9 chữ số.'),
        lt(4, 2, 'Cuốn 25 trang: đoàn tàu hai toa chạy từ trang 10 đến trang 25, có '
                 'mấy trang?',
           'Lấy hiệu: 25 − 10 = 15, thêm một được 16 trang.'),
        lt(5, 2, 'Mỗi trang của đoàn tàu hai toa cần mấy chữ số?',
           'Mỗi trang cần 2 chữ số.'),
        lt(6, 2, 'Từ trang 10 đến trang 13 cần bao nhiêu chữ số?',
           'Có 4 trang, mỗi trang hai chữ số: 4 + 4 = 8 chữ số.'),
        lt(7, 3, 'Từ trang 10 đến trang 20 có mấy trang và cần bao nhiêu chữ số?',
           'Số trang: 20 − 10 = 10, thêm một được 11 trang. Chữ số: 11 + 11 = 22.'),
        lt(8, 3, 'Trang nào là trang đầu tiên cần tới 2 chữ số?',
           'Trang 10 — từ đó trở đi mỗi trang đều hai chữ số.'),
    ] + [
        q_tf(1, 'Trang nào cũng chỉ cần một chữ số.', False,
             'Sai. Từ trang 10 trở đi mỗi trang cần hai chữ số.'),
        q_tf(2, 'Trang 37 cần hai chữ số.', True,
             'Đúng, là chữ 3 và chữ 7.'),
        q_mcq(3, 'Từ trang 1 đến trang 9 cần bao nhiêu chữ số?',
              ['9', '10', '18', '8'], '9',
              'Chín trang, mỗi trang một chữ số.'),
        q_mcq(4, 'Trang đầu tiên cần hai chữ số là trang',
              ['10', '9', '11', '20'], '10',
              'Số 10 là số đầu tiên có hai chữ số.'),
        q_tf(5, 'Đếm TRANG và đếm CHỮ SỐ là hai việc khác nhau.', True,
             'Đúng. Đếm trang xong mới tính ra chữ số.'),
    ],
)

# ═══ ⑥ B41 · ĐẾM CHỮ SỐ CẢ CUỐN ═══
B41 = bai(
    41, 'ĐẾM CHỮ SỐ CẢ CUỐN — CỘNG HAI ĐOÀN TÀU',
    'SỐ 4.3 — Tính tổng số chữ số cần để đánh số trang cả cuốn.',
    video(
        ['Tính được số chữ số của từng đoàn tàu.',
         'Cộng hai đoàn lại để ra số chữ số cả cuốn.',
         'Làm được với cuốn dày ít hay nhiều trang.'],
        ['Đề bài: Một cuốn truyện có 25 trang. Cần bao nhiêu chữ số để đánh số hết các '
         'trang?',
         'Đoàn tàu một toa',
         'Từ trang một tới trang chín có 9 trang, mỗi trang một chữ số. Cần 9 chữ số.',
         'Đoàn tàu hai toa',
         'Từ trang mười tới trang hai mươi lăm có 16 trang, mỗi trang hai chữ số.',
         'Mười sáu cộng mười sáu bằng ba mươi hai chữ số.',
         'Cộng hai đoàn lại',
         'Chín cộng ba mươi hai bằng bốn mươi mốt.',
         'Đáp số: 41 chữ số.',
         'Thử với cuốn khác',
         'Cuốn mười hai trang: đoàn một toa 9 chữ số, đoàn hai toa có 3 trang nên 6 '
         'chữ số. Cộng lại được mười lăm.'],
        ['Có bạn tính cuốn 25 trang rồi lấy 25 nhân 2, được 50 chữ số.',
         'Gợi ý 1: Con xem chín trang đầu có tốn hai chữ số mỗi trang không.',
         'Gợi ý 2: Chỉ đoàn tàu hai toa mới tốn hai chữ số. Đoàn một toa thì sao?',
         'Chữa: chín trang đầu chỉ tốn một chữ số mỗi trang. Phải tính riêng hai đoàn '
         'rồi cộng, được bốn mươi mốt.'],
        ['Cho con đếm thật trên một cuốn mỏng: đếm chữ số ở chín trang đầu, rồi đếm '
         'tiếp. Đếm tay xong so với tính thì con tin ngay.',
         'Bài này gồm ba bước và bé hay quên bước cuối. Bố mẹ hỏi: "Con đã cộng hai '
         'đoàn tàu lại chưa?"'],
    ),
    [
        lt(1, 1, 'Đoàn tàu một toa gồm trang 1 đến trang 9. Cần bao nhiêu chữ số?',
           'Chín trang, mỗi trang một chữ số nên cần 9 chữ số.'),
        lt(2, 1, 'Đoàn tàu hai toa của cuốn 25 trang có 16 trang. Cần bao nhiêu chữ số?',
           'Mỗi trang hai chữ số: 16 + 16 = 32 chữ số.'),
        lt(3, 1, 'Vậy cuốn 25 trang cần tất cả bao nhiêu chữ số?',
           'Cộng hai đoàn: 9 + 32 = 41 chữ số.'),
        lt(4, 2, 'Một cuốn vở có 12 trang. Cần bao nhiêu chữ số?',
           'Đoàn một toa 9 chữ số. Đoàn hai toa có 3 trang nên 3 + 3 = 6. Cộng lại: '
           '9 + 6 = 15 chữ số.'),
        lt(5, 2, 'Một cuốn có 20 trang. Cần bao nhiêu chữ số?',
           'Đoàn một toa 9. Đoàn hai toa có 11 trang nên 11 + 11 = 22. Cộng lại: '
           '9 + 22 = 31 chữ số.'),
        lt(6, 2, 'Cuốn 15 trang thì đoàn tàu hai toa có mấy trang?',
           'Từ trang 10 đến trang 15: 15 − 10 = 5, thêm một được 6 trang.'),
        lt(7, 3, 'Vậy cuốn 15 trang cần tất cả bao nhiêu chữ số?',
           'Đoàn hai toa: 6 + 6 = 12. Cộng đoàn một toa: 9 + 12 = 21 chữ số.'),
        lt(8, 3, 'Một cuốn có 30 trang. Đoàn tàu hai toa có mấy trang, và cả cuốn cần '
                 'bao nhiêu chữ số?',
           'Đoàn hai toa: 30 − 10 = 20, thêm một được 21 trang, tốn 21 + 21 = 42 chữ '
           'số. Cả cuốn: 9 + 42 = 51 chữ số.'),
    ] + [
        q_tf(1, 'Cuốn 25 trang cần 41 chữ số.', True,
             'Đúng: 9 chữ số cho đoàn một toa, 32 cho đoàn hai toa.'),
        q_tf(2, 'Cuốn 25 trang cần 50 chữ số vì mỗi trang hai chữ số.', False,
             'Sai. Chín trang đầu chỉ tốn một chữ số mỗi trang.'),
        q_mcq(3, 'Cuốn 12 trang cần bao nhiêu chữ số?', ['15', '24', '12', '21'],
              '15', 'Chín chữ số cho đoàn một toa, sáu cho ba trang còn lại.'),
        q_mcq(4, 'Muốn tính chữ số cả cuốn thì', ['cộng hai đoàn tàu lại',
                                                  'nhân số trang với 2',
                                                  'lấy số trang làm đáp số'],
              'cộng hai đoàn tàu lại',
              'Tính riêng từng đoàn rồi mới cộng.'),
        q_tf(5, 'Cuốn 15 trang cần 21 chữ số.', True,
             'Đúng: 9 cộng 12.'),
    ],
)

MOI = [B06, B39, B07, B40, B08, B41]

SAU = {
    'DL:KSN2.B39': 'DL:KSN2.B06',
    'DL:KSN2.B40': 'DL:KSN2.B07',
    'DL:KSN2.B41': 'DL:KSN2.B08',
}

O_NHAP_MOI = {
 'DL:KSN2.B06#C1': {'value': 8},
 'DL:KSN2.B06#C2': {'parts': [{'label': 'hiệu', 'value': 4},
                              {'label': 'thêm một được', 'value': 5}]},
 'DL:KSN2.B06#C3': {'value': 6},
 'DL:KSN2.B06#C4': {'value': 11},
 'DL:KSN2.B06#C5': {'parts': [{'label': 'vì sao',
                               'options': ['vì số đầu tiên chưa nhảy đã đứng sẵn ở đó',
                                           'vì cho tròn số'],
                               'value': 'vì số đầu tiên chưa nhảy đã đứng sẵn ở đó'}]},
 'DL:KSN2.B06#C6': {'value': 1},
 'DL:KSN2.B06#C7': {'value': 10},
 'DL:KSN2.B06#C8': {'value': 14},

 'DL:KSN2.B39#C1': {'parts': [{'label': 'số thứ nhất', 'value': 8},
                              {'label': 'số thứ hai', 'value': 10},
                              {'label': 'số thứ ba', 'value': 12}]},
 'DL:KSN2.B39#C2': {'parts': [{'label': 'số thứ nhất', 'value': 20},
                              {'label': 'số thứ hai', 'value': 25},
                              {'label': 'số thứ ba', 'value': 30}]},
 'DL:KSN2.B39#C3': {'value': 5},
 'DL:KSN2.B39#C4': {'value': 5},
 'DL:KSN2.B39#C5': {'value': 6},
 'DL:KSN2.B39#C6': {'parts': [{'label': 'toàn số gì', 'options': ['số chẵn', 'số lẻ'],
                               'value': 'số chẵn'}]},
 'DL:KSN2.B39#C7': {'parts': [{'label': 'số thứ nhất', 'value': 40},
                              {'label': 'số thứ hai', 'value': 50}]},
 'DL:KSN2.B39#C8': {'value': 10},

 'DL:KSN2.B07#C1': {'value': 35},
 'DL:KSN2.B07#C2': {'value': 53},
 'DL:KSN2.B07#C3': {'value': 10},
 'DL:KSN2.B07#C4': {'value': 10},
 'DL:KSN2.B07#C5': {'value': 30},
 'DL:KSN2.B07#C6': {'value': 10},
 'DL:KSN2.B07#C7': {'parts': [{'label': 'số đầu', 'value': 30},
                              {'label': 'số cuối', 'value': 39},
                              {'label': 'có mấy số', 'value': 10}]},
 'DL:KSN2.B07#C8': {'value': 1},

 'DL:KSN2.B40#C1': {'value': 20},
 'DL:KSN2.B40#C2': {'value': 55},
 'DL:KSN2.B40#C3': {'value': 19},
 'DL:KSN2.B40#C4': {'parts': [{'label': 'vì sao',
                               'options': ['vì số 55 bị đếm hai lần',
                                           'vì đếm thừa cho vui'],
                               'value': 'vì số 55 bị đếm hai lần'}]},
 'DL:KSN2.B40#C5': {'value': 33},
 'DL:KSN2.B40#C6': {'value': 19},
 'DL:KSN2.B40#C7': {'value': 19},
 'DL:KSN2.B40#C8': {'value': 2},

 'DL:KSN2.B08#C1': {'value': 1},
 'DL:KSN2.B08#C2': {'value': 2},
 'DL:KSN2.B08#C3': {'parts': [{'label': 'số trang', 'value': 9},
                              {'label': 'số chữ số', 'value': 9}]},
 'DL:KSN2.B08#C4': {'value': 16},
 'DL:KSN2.B08#C5': {'value': 2},
 'DL:KSN2.B08#C6': {'value': 8},
 'DL:KSN2.B08#C7': {'parts': [{'label': 'số trang', 'value': 11},
                              {'label': 'số chữ số', 'value': 22}]},
 'DL:KSN2.B08#C8': {'value': 10},

 'DL:KSN2.B41#C1': {'value': 9},
 'DL:KSN2.B41#C2': {'value': 32},
 'DL:KSN2.B41#C3': {'value': 41},
 'DL:KSN2.B41#C4': {'value': 15},
 'DL:KSN2.B41#C5': {'value': 31},
 'DL:KSN2.B41#C6': {'value': 6},
 'DL:KSN2.B41#C7': {'value': 21},
 'DL:KSN2.B41#C8': {'parts': [{'label': 'đoàn hai toa có mấy trang', 'value': 21},
                              {'label': 'cả cuốn cần mấy chữ số', 'value': 51}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (6, 7, 8)}
    moi_ = {f'DL:KSN2.B{n}' for n in (39, 40, 41)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        for m in ('chuyenMoBai', 'khamPha'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
        van = json.dumps(b, ensure_ascii=False)
        for ten in ('Trí Long', 'Su Kem'):
            if ten in van:
                loi.append(f'{b["id"]}: còn tên nhân vật "{ten}"')
    NEO = {'DL:KSN2.B06': '7 − 3', 'DL:KSN2.B39': '2, 4, 6',
           'DL:KSN2.B07': '59 − 50', 'DL:KSN2.B40': '55',
           'DL:KSN2.B08': '25', 'DL:KSN2.B41': '41'}
    for b in MOI:
        mong = NEO.get(b['id'])
        if mong and mong not in json.dumps(b, ensure_ascii=False):
            loi.append(f'{b["id"]}: không bám số neo "{mong}" của chương')
    return loi


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--xem', action='store_true')
    a = p.parse_args()
    loi = soi()
    if loi:
        for x in loi:
            print('  ✗', x)
        sys.exit(f'{len(loi)} chỗ chưa đạt — chưa ghi gì cả')
    for b in MOI:
        n = sum(1 for c in b['cau'] if c['phan'] == 'luyenTap')
        q = sum(1 for c in b['cau'] if c['phan'] == 'quiz')
        print(f"  {b['id']}  {b['ten'][:50]:50} {n} luyện + {q} quiz")
    if a.xem:
        print('\n(--xem: chưa ghi gì)')
        return
    for b in MOI:
        tep = RA / f"DL_KSN2_B{b['so']:02d}.json"
        if tep.exists():
            cu = json.loads(tep.read_text('utf8'))
            for ten, m in b['muc'].items():
                cu_m = cu.get('muc', {}).get(ten)
                if (isinstance(cu_m, dict) and cu_m.get('hinh') and not m.get('hinh')
                        and m.get('dong')):
                    m['hinh'] = cu_m['hinh']
        tep.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n', 'utf8')
    tt = json.loads(THU_TU.read_text('utf8'))
    ds = [x for x in tt['thuTu'] if x not in SAU]
    for moi_ma, sau_ma in SAU.items():
        ds.insert(ds.index(sau_ma) + 1, moi_ma)
    tt['thuTu'] = ds
    THU_TU.write_text(json.dumps(tt, ensure_ascii=False, indent=1) + '\n', 'utf8')
    t = json.loads(TAY.read_text('utf8'))
    t.update(O_NHAP_MOI)
    TAY.write_text(json.dumps(t, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'\nghi {len(MOI)} bài · thứ tự học nay {len(tt["thuTu"])} bài · '
          f'thêm {len(O_NHAP_MOI)} ô nhập')


if __name__ == '__main__':
    main()
