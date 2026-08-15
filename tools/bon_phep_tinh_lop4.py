# -*- coding: utf-8 -*-
"""CHƯƠNG 2 · BỐN PHÉP TÍNH VÀ ĐẾM — bốn bài chữ thành mười một bài video.

Bốn bài cũ đều là bài "nhiều mẹo": mỗi bài dạy ba bốn kỹ thuật chẳng liên quan gì
nhau, và bé học xong nhớ được một hai cái rồi lẫn hết.

  · B05 gộp đặt thừa số chung, nhẩm nhân 25, nhẩm nhân 11, và soi thừa số 0 ẩn;
  · B06 gộp gom X, bóc ngoặc nhiều lớp, và tìm X trong phép chia có dư;
  · B07 gộp công thức đếm số cách đều với đếm chữ số trang sách và bài ngược;
  · B08 gộp quy tắc nhân với phép đếm phần bù.

Mỗi kỹ thuật nay một bài, vì chúng dùng những cái đầu khác nhau: gộp kệ là nhìn
thấy thừa số chung, còn phần bù là nghĩ ngược hẳn lại.

── SỐ NEO ──
    4 × 38 + 4 × 62     đặt thừa số chung, ra tròn 400
    25 và 11            hai bảng nhẩm nhanh
    45 và 59            tìm X
    trang 1 tới 250     đếm chữ số
    ba vòng khoá 9 cách quy tắc nhân và phần bù

    python3 tools/bon_phep_tinh_lop4.py --xem
    python3 tools/bon_phep_tinh_lop4.py
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

TEN_CHUONG = 'BỐN PHÉP TÍNH VÀ TÍNH NHANH'
CHUONG = 2
CO_KHONG = ['có', 'không']

LUI_NHAM = {'ve': ['DL:KSN3.B05'], 'ten': ['TÍNH NHANH BẰNG CẶP TRÒN CHỤC'],
            'canCu': 'chuDe', 'lopDuoi': 3}
LUI_X = {'ve': ['DL:KSN3.B06'], 'ten': ['TÌM X'], 'canCu': 'chuDe', 'lopDuoi': 3}
LUI_DEM = {'ve': ['DL:KSN3.B04'], 'ten': ['ĐẾM SỐ & ĐẾM TRANG NÂNG CẤP'],
           'canCu': 'sach', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)

LUI_NHAM = {'ve': ['DL:KSN3.B05'], 'ten': ['NHÂN RA NGOÀI BẢNG'],
            'canCu': 'sach', 'lopDuoi': 3}
LUI_NHAM_CD = {'ve': ['DL:KSN3.B05'], 'ten': ['NHÂN RA NGOÀI BẢNG'],
               'canCu': 'chuDe', 'lopDuoi': 3}
LUI_X = {'ve': ['DL:KSN3.B07'], 'ten': ['TRUY TÌM SỐ CHIA a DƯ b'],
         'canCu': 'chuDe', 'lopDuoi': 3}
LUI_XDU = {'ve': ['DL:KSN3.B06'], 'ten': ['PHÉP CHIA CÓ DƯ CHÍNH DANH'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_DEM = {'ve': ['DL:KSN3.B10'], 'ten': ['TOA TÀU THỨ n Ở ĐÂU?'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_TRANG = {'ve': ['DL:KSN3.B04'], 'ten': ['ĐẾM SỐ & ĐẾM TRANG NÂNG CẤP'],
             'canCu': 'sach', 'lopDuoi': 3}
LUI_NHAN = {'ve': ['DL:KSN3.B11'], 'ten': ['GA NÀY TÀU CÓ DỪNG KHÔNG?'],
            'canCu': 'chuDe', 'lopDuoi': 3}

# ═══ ① B05 · ĐẶT THỪA SỐ CHUNG ═══
B05 = bai(
    5, 'ĐẶT THỪA SỐ CHUNG — GỘP RỒI MỚI NHÂN',
    'Dạng gốc: SỐ 7.1 mức Lớp 4 — Đặt thừa số chung để tính nhanh, cả với phép '
    'cộng lẫn phép trừ.',
    'Có những phép tính trông dài ngoằng mà làm được trong đầu, không cần đặt bút. '
    'Bí quyết đầu tiên là nhìn ra thứ chung nhau.',
    LUI_NHAM,
    video(
        ['Nhận ra thừa số chung của hai tích cộng hoặc trừ nhau.',
         'Gộp lại thành một phép nhân duy nhất.',
         'Nói được vì sao gộp được: đếm số phần trước, nhân giá sau.'],
        ['Đề bài: Tính nhanh 4 × 38 + 4 × 62.',
         'Nhìn ra thứ chung nhau',
         'Hai tích này đều có thừa số 4. Bốn ấy chính là thứ chung.',
         'Vì sao gộp được',
         'Có ba mươi tám hộp gà và sáu mươi hai hộp tôm, hộp nào cũng đáng bốn nghìn. '
         'Vậy đếm chung số hộp trước rồi mới nhân giá, kết quả vẫn thế.',
         'Gộp lại',
         'Viết thành 4 nhân với ngoặc ba mươi tám cộng sáu mươi hai.',
         'Trong ngoặc: 38 + 62 = 100 — vừa tròn.',
         'Nhân nốt: 4 × 100 = 400.',
         'Đáp số: 400.',
         'Chiều trừ cũng gộp được',
         'Ví dụ 9 × 47 − 9 × 37 gộp thành 9 nhân ngoặc bốn mươi bảy trừ ba mươi bảy, '
         'tức 9 × 10 = 90.'],
        ['Có bạn gộp nhầm thành cộng cả hai thừa số: "4 × 38 + 4 × 62 = 8 × 100".',
         'Gợi ý 1: Bạn ấy cộng hai số 4 lại. Nhưng số hộp có nhiều lên gấp đôi không?',
         'Gợi ý 2: Giá mỗi hộp vẫn là bốn nghìn chứ, sao lại thành tám nghìn?',
         'Chữa: thừa số chung chỉ viết MỘT lần ra ngoài ngoặc. Kết quả đúng là '
         '4 × 100 = 400, không phải 800.'],
        ['Đi chợ cùng con: mua 3 gói bánh và 2 gói kẹo, mỗi gói đều 5 nghìn. Hỏi con '
         'tính kiểu nào nhanh hơn — cộng số gói trước hay nhân từng loại trước.',
         'Con quen tay rồi thì mọi bài tính nhanh ở lớp đều bắt đầu bằng một câu: '
         '"Có gì chung không?"'],
    ),
    [
        lt(1, 1, 'Trong phép 4 × 38 + 4 × 62, thừa số chung của hai tích là số nào?',
           'Cả hai tích đều có thừa số 4, nên thừa số chung là 4.'),
        lt(2, 1, 'Gộp lại rồi tính trong ngoặc: 38 + 62 bằng bao nhiêu?',
           'Cộng trong ngoặc: 38 + 62 = 100.'),
        lt(3, 1, 'Vậy 4 × 38 + 4 × 62 bằng bao nhiêu?',
           'Nhân nốt: 4 × 100 = 400.'),
        lt(4, 2, 'Tính nhanh 7 × 25 + 7 × 75.',
           'Trong ngoặc: 25 + 75 = 100. Rồi 7 × 100 = 700.'),
        lt(5, 2, 'Tính nhanh 9 × 47 − 9 × 37.',
           'Trong ngoặc: 47 − 37 = 10. Rồi 9 × 10 = 90.'),
        lt(6, 2, 'Tính nhanh 6 × 14 + 6 × 6.',
           'Trong ngoặc: 14 + 6 = 20. Rồi 6 × 20 = 120.'),
        lt(7, 2, 'Tính nhanh 25 × 13 + 25 × 7.',
           'Trong ngoặc: 13 + 7 = 20. Rồi 25 × 20 = 500.'),
        lt(8, 3, 'Tính nhanh 8 × 99 + 8. Gợi ý: viết số 8 đứng lẻ thành 8 × 1.',
           'Viết thành 8 × 99 + 8 × 1. Trong ngoặc: 99 + 1 = 100. Rồi 8 × 100 = 800.'),
        lt(9, 3, 'Tính nhanh 15 × 36 − 15 × 26.',
           'Trong ngoặc: 36 − 26 = 10. Rồi 15 × 10 = 150.'),
    ] + [
        q_tf(1, 'Phép 4 × 38 + 4 × 62 viết gọn được thành 4 nhân với tổng 38 và 62.',
             True, 'Đúng. Thừa số chung đưa ra ngoài, hai số kia gộp vào ngoặc.'),
        q_tf(2, 'Gộp thừa số chung thì phải cộng cả hai thừa số chung lại.', False,
             'Sai. Thừa số chung chỉ viết một lần ra ngoài ngoặc.'),
        q_mcq(3, 'Tính 4 × 38 + 4 × 62.', ['400', '800', '100', '380'], '400',
              'Gộp lại được 4 × 100 = 400.'),
        q_mcq(4, 'Tính 9 × 47 − 9 × 37.', ['90', '9', '900', '10'], '90',
              'Gộp lại được 9 × 10 = 90.'),
        q_tf(5, 'Cách đặt thừa số chung dùng được cả với phép trừ.', True,
             'Đúng. Chỉ khác dấu trong ngoặc.'),
    ],
)

# ═══ ② B86 · NHẨM NHANH VỚI 25 ═══
B86 = bai(
    86, 'NHẨM NHANH VỚI 25 — BẮT CẶP CHO TRÒN TRĂM',
    'Dạng gốc: SỐ 7.1 mức Lớp 4 — Nhẩm nhân với 25 và 125 bằng cách ghép thành 100 '
    'và 1000.',
    'Số 25 lúc nào cũng đi tìm bạn: gặp được số 4 là hai đứa thành 100 ngay. Biết '
    'chuyện ấy thì nhân với 25 nhẩm được trong đầu.',
    LUI_NHAM_CD,
    video(
        ['Biết 25 ghép với 4 thành 100, và 125 ghép với 8 thành 1000.',
         'Tách một thừa số ra để lộ số 4 hoặc số 8 ẩn trong đó.',
         'Biết cách nhân 100 rồi chia 4 khi không tách được.'],
        ['Đề bài: Tính nhanh 25 × 36, rồi tính nhanh 48 × 25.',
         'Cặp bài trùng của số 25',
         'Hai mươi lăm nhân bốn bằng một trăm. Nên gặp 25 là đi tìm số 4.',
         'Tách để lộ số 4 ra',
         'Số 36 tách được thành 4 nhân 9. Vậy 25 × 36 = 25 × 4 × 9.',
         'Ghép cặp trước: 25 × 4 = 100. Rồi 100 × 9 = 900.',
         'Không tách được thì làm sao',
         'Với 48 × 25 thì đi lối khác: nhân 100 trước rồi trả lại phần thừa. Nhân 100 '
         'tức là nhân gấp bốn lần so với nhân 25, nên sau đó phải chia cho 4.',
         'Tính: 48 × 100 = 4 800. Rồi 4 800 : 4 = 1 200.',
         'Đáp số: 900 và 1 200.',
         'Người anh của số 25',
         'Số 125 ghép với 8 thì được 1000 — cùng một lối nghĩ, chỉ khác con số.'],
        ['Có bạn tính 25 × 36 bằng cách nhân 25 với 30 rồi nhân 25 với 6, xong cộng '
         'lại, mất cả phút.',
         'Gợi ý 1: Cách ấy vẫn ra đúng, nhưng con thử tách 36 thành hai số nhân nhau '
         'xem có số nào hợp với 25 không.',
         'Gợi ý 2: Con số nào ghép với 25 thì thành một trăm tròn trịa?',
         'Chữa: tách 36 thành 4 × 9 rồi ghép 25 với 4 thành 100, phép tính chỉ còn '
         '100 × 9 — nhẩm một cái là xong.'],
        ['Cho con nhẩm giá tiền: 25 nghìn một hộp thì 8 hộp bao nhiêu, 12 hộp bao '
         'nhiêu. Nhẩm được là con thấy cái lợi ngay.',
         'Bí quyết duy nhất của bài này: gặp 25 thì mắt đi tìm số 4, gặp 125 thì đi '
         'tìm số 8.'],
    ),
    [
        lt(1, 1, 'Số 25 nhân với số nào thì được 100?',
           'Hai mươi lăm nhân bốn: 25 × 4 = 100.'),
        lt(2, 1, 'Tách 36 thành 4 nhân 9 rồi tính 25 × 36.',
           'Ghép cặp trước: 25 × 4 = 100. Rồi 100 × 9 = 900.'),
        lt(3, 1, 'Tính nhanh 25 × 8.',
           'Tách 8 thành 4 × 2: 25 × 4 = 100, rồi 100 × 2 = 200.'),
        lt(4, 2, 'Tính nhanh 25 × 16.',
           'Tách 16 thành 4 × 4: 25 × 4 = 100, rồi 100 × 4 = 400.'),
        lt(5, 2, 'Tính 48 × 25 bằng cách nhân 100 rồi chia 4.',
           'Trước hết 48 × 100 = 4 800. Rồi trả lại phần thừa: 4 800 : 4 = 1 200.'),
        lt(6, 2, 'Tính nhanh 25 × 12.',
           'Tách 12 thành 4 × 3: 25 × 4 = 100, rồi 100 × 3 = 300.'),
        lt(7, 2, 'Số 125 nhân với số nào thì được 1000?',
           'Một trăm hai mươi lăm nhân tám: 125 × 8 = 1 000.'),
        lt(8, 3, 'Tính nhanh 125 × 24. Gợi ý: tách 24 thành 8 nhân mấy?',
           'Tách 24 thành 8 × 3. Ghép cặp: 125 × 8 = 1 000, rồi 1 000 × 3 = 3 000.'),
        lt(9, 3, 'Tính nhanh 25 × 44.',
           'Tách 44 thành 4 × 11: 25 × 4 = 100, rồi 100 × 11 = 1 100.'),
    ] + [
        q_tf(1, 'Số 25 nhân 4 được 100.', True, 'Đúng, và đó là cặp bài trùng của nó.'),
        q_mcq(2, 'Tính 25 × 36.', ['900', '810', '90', '9 000'], '900',
              'Tách 36 thành 4 × 9 rồi ghép: 100 × 9 = 900.'),
        q_tf(3, 'Số 125 ghép với 8 thì được 1000.', True,
             'Đúng. Cùng lối nghĩ với cặp 25 và 4.'),
        q_mcq(4, 'Muốn tính nhanh 48 × 25 thì',
              ['nhân 100 rồi chia 4', 'nhân 4 rồi chia 100', 'cộng thêm 100'],
              'nhân 100 rồi chia 4',
              'Nhân 100 là nhân gấp bốn lần so với nhân 25, nên phải chia 4 để trả lại.'),
        q_tf(5, 'Gặp số 25 thì mắt đi tìm số 4 trước đã.', True,
             'Đúng. Tìm được số 4 là bài xong một nửa.'),
    ],
)

# ═══ ③ B87 · NHẨM NHANH VỚI 11 ═══
B87 = bai(
    87, 'NHẨM NHANH VỚI 11 — NHÂN MƯỜI RỒI CỘNG CHÍNH NÓ',
    'Dạng gốc: SỐ 7.1 mức Lớp 4 — Nhẩm nhân với 11 bằng hai cách: nhân mười rồi '
    'cộng, và mẹo hai đầu.',
    'Nhân với 11 nghe khó, mà thật ra chỉ là nhân với 10 rồi cộng thêm một lần nữa. '
    'Còn có một mẹo nhanh hơn nữa, nhưng phải cẩn thận một chỗ.',
    LUI_NHAM_CD,
    video(
        ['Nhẩm nhân 11 bằng cách nhân 10 rồi cộng chính số ấy.',
         'Dùng được mẹo hai đầu: hai chữ số ra hai bên, tổng của chúng vào giữa.',
         'Biết khi tổng hai chữ số vượt 9 thì phải nhớ 1 sang trái.'],
        ['Đề bài: Tính nhanh 35 × 11, rồi tính nhanh 57 × 11.',
         'Cách chắc chắn nhất',
         'Mười một bằng mười cộng một. Nên nhân với mười một là nhân mười rồi cộng '
         'thêm chính số ấy một lần.',
         'Ba mươi lăm nhân mười bằng ba trăm năm mươi. Cộng thêm ba mươi lăm được ba '
         'trăm tám mươi lăm.',
         'Mẹo hai đầu, nhanh hơn nữa',
         'Viết hai chữ số ra hai bên: 3 và 5. Cộng chúng lại được 8, nhét vào giữa. '
         'Được 385 — đúng như vừa tính.',
         'Chỗ phải cẩn thận',
         'Với 57 thì tổng hai chữ số là 12, hai chữ số mà nhét vào một chỗ không vừa.',
         'Khi ấy để lại chữ số 2 ở giữa và nhớ 1 sang bên trái: 5 thêm 1 thành 6. '
         'Được 627.',
         'Kiểm bằng cách chắc chắn: 570 + 57 = 627 — khớp.',
         'Đáp số: 385 và 627.'],
        ['Có bạn tính 57 × 11 bằng mẹo hai đầu rồi ghi thẳng 5, 12, 7 thành "5127".',
         'Gợi ý 1: Số 5127 có mấy chữ số? Một số hai chữ số nhân 11 thì được số mấy '
         'chữ số?',
         'Gợi ý 2: Chỗ ở giữa chỉ chứa được MỘT chữ số thôi. Tổng 12 thì phần thừa đi '
         'đâu?',
         'Chữa: giữ chữ số 2 ở giữa, nhớ 1 sang trái cộng vào chữ số 5 thành 6. Kết '
         'quả là 627.'],
        ['Cho con nhẩm nhanh vài phép nhân 11 rồi kiểm bằng máy tính. Sai ở đâu gần '
         'như luôn là chỗ nhớ 1.',
         'Nếu con lẫn thì bảo con quay về cách chắc chắn: nhân 10 rồi cộng. Chậm hơn '
         'vài giây nhưng không bao giờ sai.'],
    ),
    [
        lt(1, 1, 'Tính 35 × 10.', 'Thêm một chữ số 0: 35 × 10 = 350.'),
        lt(2, 1, 'Tính 350 + 35.', 'Cộng lại: 350 + 35 = 385.'),
        lt(3, 1, 'Vậy 35 × 11 bằng bao nhiêu?',
           'Nhân mười rồi cộng chính nó, được 385.'),
        lt(4, 2, 'Tính nhanh 24 × 11.',
           'Nhân mười được 240, cộng 24 được 264. Mẹo hai đầu cũng ra: 2 và 4 hai bên, '
           'tổng 6 vào giữa.'),
        lt(5, 2, 'Dùng mẹo hai đầu cho 35 × 11: viết 3 và 5 ra hai bên, ở giữa là số '
                 'nào?',
           'Ở giữa là tổng hai chữ số: 3 + 5 = 8.'),
        lt(6, 2, 'Tính nhanh 62 × 11.',
           'Nhân mười được 620, cộng 62 được 682.'),
        lt(7, 2, 'Tính nhanh 57 × 11.',
           'Nhân mười được 570, cộng 57 được 627.'),
        lt(8, 3, 'Với 57 × 11, tổng hai chữ số là 12 — hai chữ số mà chỗ giữa chỉ chứa '
                 'được một. Phải làm gì?',
           'Giữ chữ số 2 ở giữa và nhớ 1 sang bên trái, cộng vào chữ số 5 thành 6.'),
        lt(9, 3, 'Tính nhanh 11 × 11.',
           'Nhân mười được 110, cộng 11 được 121.'),
    ] + [
        q_tf(1, 'Nhân với 11 là nhân 10 rồi cộng thêm chính số ấy.', True,
             'Đúng, vì 11 bằng 10 cộng 1.'),
        q_mcq(2, 'Tính 35 × 11.', ['385', '350', '355', '3 511'], '385',
              'Nhân mười được 350, cộng 35 được 385.'),
        q_tf(3, 'Mẹo hai đầu: hai chữ số ra hai bên, tổng của chúng nhét vào giữa.',
             True, 'Đúng, và nhớ để ý khi tổng vượt 9.'),
        q_mcq(4, 'Tính 57 × 11.', ['627', '517', '5 127', '587'], '627',
              'Tổng hai chữ số là 12, giữ 2 ở giữa và nhớ 1 sang trái.'),
        q_tf(5, 'Tổng hai chữ số vượt 9 thì bỏ bớt chữ số hàng chục của tổng đi.',
             False, 'Sai. Phải nhớ 1 sang bên trái chứ không được bỏ.'),
    ],
)

# ═══ ④ B88 · NHÌN KỸ TRƯỚC KHI TÍNH ═══
B88 = bai(
    88, 'NHÌN KỸ TRƯỚC KHI TÍNH — THỪA SỐ 0 ẨN',
    'Dạng gốc: SỐ 7.1 mức Lớp 4 — Phát hiện thừa số 0 ẩn trong tích dài; so sánh '
    'hai biểu thức mà không tính hết.',
    'Có những bài trông dài đến phát sợ, mà đáp số là 0 — chỉ cần nhìn ba giây là '
    'thấy. Bài này dạy con nhìn ba giây ấy.',
    LUI_NHAM_CD,
    video(
        ['Biết một tích chỉ cần có một thừa số bằng 0 thì cả tích bằng 0.',
         'Soi được thừa số 0 nấp trong một cặp ngoặc.',
         'So sánh được hai biểu thức mà không phải tính hết ra.'],
        ['Đề bài: Tính giá trị của biểu thức có ngoặc mười ba trừ bảy mươi tám chia '
         'sáu, rồi nhân hai trăm ba mươi mốt, rồi nhân tám.',
         'Đừng vội nhân',
         'Nhìn thấy tích dài là nhiều bạn cắm cúi nhân ngay. Nhưng hãy soi từng thừa '
         'số trước đã.',
         'Soi cái ngoặc',
         'Trong ngoặc có phép chia: bảy mươi tám chia sáu bằng mười ba.',
         'Mười ba trừ mười ba bằng không. Vậy cái ngoặc bằng 0.',
         'Một thừa số bằng 0 là xong',
         'Trong một tích, chỉ cần một thừa số bằng 0 thì cả tích bằng 0 — không cần '
         'nhân gì thêm nữa.',
         'Đáp số: 0.',
         'So sánh cũng không cần tính',
         'So 52 nhân 25 với 51 nhân 25 cộng 20. Bên trái hơn 51 nhân 25 đúng một lần '
         '25, mà bên phải chỉ hơn có 20. Vậy bên trái lớn hơn.'],
        ['Có bạn thấy biểu thức dài liền nhân hết ra, mất năm phút rồi mới ra 0.',
         'Gợi ý 1: Con thử tính riêng cái ngoặc trước xem nó bằng bao nhiêu.',
         'Gợi ý 2: Nếu một thừa số đã bằng 0 thì nhân tiếp có thay đổi được gì không?',
         'Chữa: soi ba giây trước khi đặt bút. Thấy một thừa số bằng 0 là ghi đáp số 0 '
         'ngay, khỏi nhân.'],
        ['Đưa con vài biểu thức dài trong đó có một ngoặc bằng 0. Bấm giờ xem con mất '
         'bao lâu — lần đầu lâu, lần sau vài giây.',
         'Ba câu hỏi soi nhanh: có thừa số chung không, có cặp tròn trăm không, có '
         'thừa số 0 ẩn không. Ba câu ấy đáng cả buổi luyện tính.'],
    ),
    [
        lt(1, 1, 'Tính 78 : 6.', 'Chia ra: 78 : 6 = 13.'),
        lt(2, 1, 'Vậy giá trị của ngoặc 13 trừ 78 chia 6 bằng bao nhiêu?',
           'Trong ngoặc: 13 − 13 = 0.'),
        lt(3, 1, 'Vậy ngoặc ấy nhân 231 rồi nhân 8 thì bằng bao nhiêu?',
           'Một thừa số đã bằng 0 nên cả tích bằng 0.'),
        lt(4, 2, 'Tính giá trị của ngoặc 25 nhân 4 trừ 100, rồi nhân 999.',
           'Trong ngoặc: 25 × 4 = 100, rồi 100 − 100 = 0. Cả tích bằng 0.'),
        lt(5, 2, 'Phép 52 × 25 hơn phép 51 × 25 bao nhiêu đơn vị?',
           'Hơn đúng một lần 25, tức là hơn 25 đơn vị.'),
        lt(6, 2, 'So sánh 52 × 25 với 51 × 25 + 20. Bên nào lớn hơn?',
           'Bên trái hơn 51 × 25 đúng 25, bên phải chỉ hơn 20, nên 52 × 25 lớn hơn.'),
        lt(7, 2, 'Tính giá trị của ngoặc 100 trừ 10 nhân 10, rồi nhân 4 567.',
           'Trong ngoặc: 10 × 10 = 100, rồi 100 − 100 = 0. Cả tích bằng 0.'),
        lt(8, 3, 'So sánh 37 × 18 với 37 × 17 + 37. Hai bên bằng nhau hay khác nhau?',
           'Bên trái hơn 37 × 17 đúng một lần 37, mà bên phải cũng cộng thêm đúng 37, '
           'nên hai bên bằng nhau.'),
        lt(9, 3, 'Tính giá trị của ngoặc 9 nhân 9 trừ 81, rồi nhân 1 234, rồi nhân 567.',
           'Trong ngoặc: 9 × 9 = 81, rồi 81 − 81 = 0. Cả tích bằng 0.'),
    ] + [
        q_tf(1, 'Trong một tích, chỉ cần một thừa số bằng 0 thì cả tích bằng 0.', True,
             'Đúng, và đó là mẹo soi nhanh nhất của bài này.'),
        q_mcq(2, 'Ngoặc 13 trừ 78 chia 6, nhân 231, nhân 8 thì bằng',
              ['0', '13', '231', '1'], '0',
              'Ngoặc bằng 0 nên cả tích bằng 0.'),
        q_tf(3, 'Muốn so sánh hai biểu thức thì bao giờ cũng phải tính hết ra.', False,
             'Sai. Nhiều khi chỉ cần so phần chênh lệch là đủ.'),
        q_mcq(4, 'Phép 52 × 25 hơn phép 51 × 25 bao nhiêu?', ['25', '1', '52', '51'],
              '25', 'Hơn đúng một lần thừa số 25.'),
        q_tf(5, 'Soi ba giây trước khi đặt bút có khi tiết kiệm được cả bài tính.',
             True, 'Đúng. Đó là thói quen của người tính giỏi.'),
    ],
)

# ═══ ⑤ B06 · X XUẤT HIỆN HAI LẦN ═══
B06 = bai(
    6, 'X XUẤT HIỆN HAI LẦN — GOM VỀ MỘT CHỖ',
    'Dạng gốc: SỐ 7.2 mức Lớp 4 — Tìm X khi X có mặt ở hai số hạng; đặt thừa số '
    'chung để đưa về bài tìm X quen thuộc.',
    'Bài tìm X con làm quen rồi. Nhưng gặp bài mà X hiện ra hai lần thì bối rối: '
    'biết bắt đầu từ đâu? Bắt đầu bằng cách gom chúng lại.',
    LUI_X,
    video(
        ['Nhận ra X xuất hiện ở hai số hạng.',
         'Gom hai số hạng ấy lại bằng cách đặt thừa số chung.',
         'Đưa về bài tìm X một lần rồi giải như đã quen.'],
        ['Đề bài: Tìm X, biết X nhân 3 cộng X nhân 2 bằng 45.',
         'Nhìn ra chỗ khó',
         'X hiện ra hai lần. Chưa gom lại thì không giải được, vì không biết chia cho '
         'cái gì.',
         'Gom lại bằng thừa số chung',
         'Cả hai số hạng đều có X. Đưa X ra ngoài: X nhân với ngoặc ba cộng hai.',
         'Trong ngoặc: 3 + 2 = 5. Vậy bài thành X nhân 5 bằng 45.',
         'Giải như bài quen',
         'Muốn tìm thừa số chưa biết thì lấy tích chia cho thừa số kia: 45 : 5 = 9.',
         'Đáp số: X bằng 9.',
         'Thử lại',
         'Lắp 9 vào đề: 9 × 3 = 27, rồi 9 × 2 = 18, cộng lại 27 + 18 = 45 — đúng bằng '
         'vế phải.'],
        ['Có bạn thấy X nhân 3 cộng X nhân 2 rồi cộng luôn thành X nhân 6.',
         'Gợi ý 1: Bạn ấy nhân 3 với 2. Nhưng ở đây hai số ấy đang cộng hay đang nhân '
         'nhau?',
         'Gợi ý 2: Thử với một số cụ thể xem: lấy X bằng 1 thì vế trái bằng bao nhiêu?',
         'Chữa: gom lại thì hai số trong ngoặc CỘNG nhau, được 5 chứ không phải 6. '
         'Bài đúng là X nhân 5 bằng 45.'],
        ['Cho con thay X bằng một vật thật: ba cái bút cộng hai cái bút là mấy cái '
         'bút. Gom được ngoài đời thì gom được trong bài.',
         'Con làm xong luôn bắt lắp lại vào đề để thử. Bài tìm X mà không thử lại thì '
         'sai cũng không biết.'],
    ),
    [
        lt(1, 1, 'Gom X × 3 + X × 2 lại thì được X nhân với số nào?',
           'Đưa X ra ngoài: trong ngoặc 3 + 2 = 5, nên được X × 5.'),
        lt(2, 1, 'Từ X × 5 = 45, tìm X.',
           'Lấy tích chia cho thừa số kia: 45 : 5 = 9.'),
        lt(3, 1, 'Thử lại: 9 × 3 + 9 × 2 bằng bao nhiêu?',
           'Tính ra: 27 + 18 = 45 — đúng bằng vế phải.'),
        lt(4, 2, 'Tìm X, biết X × 4 + X × 6 = 80.',
           'Gom lại: 4 + 6 = 10, nên X × 10 = 80. Vậy X = 80 : 10 = 8.'),
        lt(5, 2, 'Tìm X, biết X × 7 − X × 3 = 24.',
           'Gom lại: 7 − 3 = 4, nên X × 4 = 24. Vậy X = 24 : 4 = 6.'),
        lt(6, 2, 'Tìm X, biết X + X + X = 27.',
           'Ba lần X nên X × 3 = 27. Vậy X = 27 : 3 = 9.'),
        lt(7, 2, 'Tìm X, biết X × 5 + X = 36.',
           'Số X đứng lẻ chính là X × 1, nên gom được X × 6 = 36. Vậy X = 36 : 6 = 6.'),
        lt(8, 3, 'Tìm X, biết X × 8 − X = 63.',
           'Gom lại: 8 − 1 = 7, nên X × 7 = 63. Vậy X = 63 : 7 = 9.'),
        lt(9, 3, 'Tìm X, biết X × 2 + X × 3 + X × 5 = 100.',
           'Gom cả ba: 2 + 3 + 5 = 10, nên X × 10 = 100. Vậy X = 100 : 10 = 10.'),
    ] + [
        q_tf(1, 'Phép X × 3 + X × 2 gom lại được thành X × 5.', True,
             'Đúng. Hai số trong ngoặc cộng nhau.'),
        q_tf(2, 'Phép X × 3 + X × 2 gom lại được thành X × 6.', False,
             'Sai. Ba và hai đang cộng nhau chứ không nhân nhau.'),
        q_mcq(3, 'Từ X × 5 = 45 thì X bằng', ['9', '40', '50', '5'], '9',
              'Lấy tích chia cho thừa số kia: 45 : 5 = 9.'),
        q_mcq(4, 'Phép X + X + X gom lại được thành', ['X × 3', 'X × 111', 'đúng 3'],
              'X × 3', 'Ba lần chính nó, nên viết X × 3.'),
        q_tf(5, 'Gặp X hai lần thì gom về một chỗ trước rồi mới giải.', True,
             'Đúng. Chưa gom thì chưa biết chia cho cái gì.'),
    ],
)

# ═══ ⑥ B89 · BÓC NGOẶC TỪ NGOÀI VÀO ═══
B89 = bai(
    89, 'BÓC NGOẶC TỪ NGOÀI VÀO — MỖI BƯỚC MỘT LỚP',
    'Dạng gốc: SỐ 7.2 mức Lớp 4 — Tìm X trong biểu thức có một hoặc nhiều lớp '
    'ngoặc; coi cả ngoặc là một số chưa biết.',
    'Gặp bài tìm X có ngoặc trong ngoặc, con hay nản. Nhưng bóc nó cũng như bóc củ '
    'hành: mỗi lần một lớp, từ ngoài vào trong.',
    LUI_X,
    video(
        ['Coi cả cặp ngoặc là một số chưa biết duy nhất.',
         'Bóc từng lớp ngoặc, mỗi bước một lớp, từ ngoài vào trong.',
         'Thử lại bằng cách lắp X ngược vào đề ban đầu.'],
        ['Đề bài: Tìm X, biết ngoặc X trừ 15, chia cho 3, bằng 8.',
         'Đừng nhìn vào trong vội',
         'Cứ coi cả cặp ngoặc là một số bí ẩn. Bài thành: số gì chia 3 thì được 8?',
         'Bóc lớp thứ nhất',
         'Số ấy là 3 nhân 8, tức 24. Vậy X trừ 15 bằng 24.',
         'Bóc lớp thứ hai',
         'Nay bài quen rồi: X bằng 24 cộng 15, tức 39.',
         'Đáp số: X bằng 39.',
         'Thử lại',
         'Lắp 39 vào đề: 39 − 15 = 24, rồi 24 : 3 = 8 — đúng vế phải.',
         'Nhiều lớp cũng vậy',
         'Gặp ngoặc trong ngoặc thì cứ bóc dần, mỗi bước một lớp, không nhảy cóc.'],
        ['Có bạn gặp ngoặc X trừ 15 chia 3 bằng 8 rồi làm ngay X trừ 15 chia 3, mỗi '
         'thứ một phép, thành ra loạn.',
         'Gợi ý 1: Trong đề, phép nào làm sau cùng — phép trừ trong ngoặc hay phép '
         'chia ngoài ngoặc?',
         'Gợi ý 2: Bóc thì phải bóc phép làm sau cùng trước. Con thử che cả ngoặc lại '
         'bằng ngón tay xem còn nhìn thấy phép gì.',
         'Chữa: che ngoặc lại thì chỉ còn "số gì chia 3 bằng 8". Giải cái ấy trước, '
         'rồi mới mở ngoặc ra.'],
        ['Bảo con lấy ngón tay che cái ngoặc lại rồi đọc to phần còn nhìn thấy. Đó '
         'chính là lớp phải bóc trước.',
         'Bài này không khó, chỉ đòi kiên nhẫn. Con nhảy cóc là sai, đi từng bước là '
         'đúng.'],
    ),
    [
        lt(1, 1, 'Trong bài ngoặc X trừ 15, chia 3, bằng 8: số nào chia 3 thì được 8?',
           'Số ấy là 3 × 8 = 24.'),
        lt(2, 1, 'Vậy từ X − 15 = 24, tìm X.',
           'Lấy 24 + 15 = 39.'),
        lt(3, 1, 'Thử lại: ngoặc 39 trừ 15, chia 3, bằng bao nhiêu?',
           'Tính ra: 39 − 15 = 24, rồi 24 : 3 = 8 — đúng vế phải.'),
        lt(4, 2, 'Tìm X, biết ngoặc X cộng 7, nhân 2, bằng 30.',
           'Ngoặc bằng 30 : 2 = 15. Vậy X = 15 − 7 = 8.'),
        lt(5, 2, 'Tìm X, biết X nhân 3 trừ 5 bằng 16.',
           'Trước hết X × 3 = 16 + 5 = 21. Vậy X = 21 : 3 = 7.'),
        lt(6, 2, 'Trong bài ngoặc lớn chia 6 bằng 5, giá trị của ngoặc lớn ấy bằng bao '
                 'nhiêu?',
           'Ngoặc lớn bằng 6 × 5 = 30.'),
        lt(7, 2, 'Biết ngoặc X cộng 5, nhân 2, rồi trừ 4 thì bằng 30. Vậy ngoặc X cộng '
                 '5 nhân 2 bằng bao nhiêu?',
           'Cộng số vừa trừ trở lại: 30 + 4 = 34.'),
        lt(8, 3, 'Từ đó tìm ngoặc X cộng 5, rồi tìm X.',
           'Ngoặc X cộng 5 bằng 34 : 2 = 17. Vậy X = 17 − 5 = 12.'),
        lt(9, 3, 'Tìm X, biết ngoặc X chia 4 cộng 3, nhân 5, bằng 40.',
           'Ngoặc bằng 40 : 5 = 8. Rồi X : 4 = 8 − 3 = 5. Vậy X = 5 × 4 = 20.'),
    ] + [
        q_tf(1, 'Bóc ngoặc thì bóc từ lớp ngoài cùng vào trong.', True,
             'Đúng. Phép làm sau cùng phải bóc trước.'),
        q_mcq(2, 'Từ ngoặc X trừ 15, chia 3, bằng 8 thì X bằng',
              ['39', '24', '9', '45'], '39',
              'Ngoặc bằng 24, rồi X bằng 24 cộng 15.'),
        q_tf(3, 'Coi cả cặp ngoặc là một số chưa biết rồi giải như bài quen.', True,
             'Đúng. Đó là cả bí quyết của bài này.'),
        q_mcq(4, 'Từ ngoặc X cộng 7, nhân 2, bằng 30 thì ngoặc ấy bằng',
              ['15', '30', '60', '7'], '15',
              'Lấy 30 chia cho 2 được 15.'),
        q_tf(5, 'Giải xong phải lắp X ngược vào đề để thử lại.', True,
             'Đúng. Bài tìm X mà không thử lại thì sai cũng không biết.'),
    ],
)

# ═══ ⑦ B90 · TÌM X TRONG PHÉP CHIA CÓ DƯ ═══
B90 = bai(
    90, 'TÌM X TRONG PHÉP CHIA CÓ DƯ',
    'Dạng gốc: SỐ 7.2 mức Lớp 4 — Tìm số bị chia và tìm số chia trong phép chia có '
    'dư; kiểm điều kiện số dư bé hơn số chia.',
    'Phép chia có dư con học từ lớp 3. Nay nó quay lại, nhưng chỗ chưa biết không '
    'còn là kết quả mà là chính số bị chia hoặc số chia.',
    LUI_XDU,
    video(
        ['Nhớ lại luật: số bị chia bằng số chia nhân thương rồi cộng số dư.',
         'Tìm được số bị chia khi biết thương và số dư.',
         'Tìm được số chia bằng cách bớt số dư ra trước, rồi kiểm số dư bé hơn số '
         'chia.'],
        ['Đề bài: Tìm X trong hai bài: X chia 7 được 8 dư 3; và 45 chia X được 6 dư 3.',
         'Nhớ lại luật vàng',
         'Số bị chia bằng số chia nhân thương, rồi cộng số dư. Nhớ câu ấy là làm được '
         'cả hai bài.',
         'Bài thứ nhất: tìm số bị chia',
         'Nhân trước: 7 × 8 = 56. Rồi cộng số dư: 56 + 3 = 59. Vậy X bằng 59.',
         'Bài thứ hai: tìm số chia',
         'Lần này bớt số dư ra trước cho gọn: 45 − 3 = 42. Phần 42 ấy chia hết cho X.',
         'Mà 42 chia X được 6, nên X bằng 42 : 6 = 7.',
         'Kiểm điều kiện bắt buộc',
         'Số dư phải bé hơn số chia. Ở đây dư 3 mà chia 7 — đúng luật.',
         'Đáp số: 59 và 7.',
         'Thử lại phải khớp cả thương lẫn số dư, thiếu một là hỏng.'],
        ['Có bạn tìm số chia trong bài 45 chia X được 6 dư 3, rồi làm luôn 45 : 6 và '
         'ra một số lẻ, đành làm tròn.',
         'Gợi ý 1: Trong 45 ấy có 3 đơn vị không chia được cho ai. Chúng có nên đem '
         'chia không?',
         'Gợi ý 2: Bớt phần dư ra trước thì còn bao nhiêu, và số ấy có chia hết không?',
         'Chữa: phải bớt số dư ra trước đã. Còn 42, chia cho 6 được đúng 7 — không '
         'phải làm tròn gì cả.'],
        ['Chia thật bằng kẹo: đưa con một nắm kẹo và bảo chia đều cho mấy bạn. Phần '
         'thừa chính là số dư, và nó bao giờ cũng ít hơn số bạn.',
         'Con hay quên điều kiện số dư bé hơn số chia. Bố mẹ chỉ cần hỏi thêm một câu '
         'sau mỗi bài: "Số dư có bé hơn số chia không?"'],
    ),
    [
        lt(1, 1, 'Trong bài X chia 7 được 8 dư 3, phần chia hết bằng bao nhiêu?',
           'Lấy số chia nhân thương: 7 × 8 = 56.'),
        lt(2, 1, 'Vậy X bằng bao nhiêu?',
           'Cộng số dư vào: 56 + 3 = 59.'),
        lt(3, 1, 'Thử lại: 59 chia 7 được thương mấy và dư mấy?',
           'Chia ra: 59 : 7 = 8 (dư 3) — khớp cả thương lẫn số dư.'),
        lt(4, 2, 'Tìm X, biết X chia 5 được 9 dư 4.',
           'Nhân trước: 5 × 9 = 45. Cộng số dư: 45 + 4 = 49.'),
        lt(5, 2, 'Trong bài 45 chia X được 6 dư 3, bớt số dư ra thì còn bao nhiêu?',
           'Bớt phần không chia được: 45 − 3 = 42.'),
        lt(6, 2, 'Vậy X bằng bao nhiêu?',
           'Phần 42 chia cho X được 6, nên X = 42 : 6 = 7.'),
        lt(7, 2, 'Kiểm lại: số dư 3 có bé hơn số chia 7 không?',
           'Có. Số dư luôn phải bé hơn số chia, ở đây 3 bé hơn 7 nên hợp luật.'),
        lt(8, 3, 'Tìm X, biết X chia 6 được 7 dư 5.',
           'Nhân trước: 6 × 7 = 42. Cộng số dư: 42 + 5 = 47.'),
        lt(9, 3, 'Tìm X, biết 58 chia X được 8 dư 2.',
           'Bớt số dư: 58 − 2 = 56. Rồi X = 56 : 8 = 7.'),
    ] + [
        q_tf(1, 'Số bị chia bằng số chia nhân thương rồi cộng số dư.', True,
             'Đúng. Đó là luật vàng của phép chia có dư.'),
        q_mcq(2, 'Từ X chia 7 được 8 dư 3 thì X bằng', ['59', '56', '24', '11'], '59',
              'Nhân được 56 rồi cộng số dư 3.'),
        q_tf(3, 'Số dư có thể lớn hơn số chia.', False,
             'Sai. Số dư luôn phải bé hơn số chia, nếu không thì còn chia được nữa.'),
        q_mcq(4, 'Từ 45 chia X được 6 dư 3 thì X bằng', ['7', '6', '8', '42'], '7',
              'Bớt số dư còn 42, rồi chia cho thương 6.'),
        q_tf(5, 'Thử lại phép chia có dư phải khớp cả thương lẫn số dư.', True,
             'Đúng. Khớp một cái thôi thì chưa chắc đúng.'),
    ],
)

# ═══ ⑧ B07 · ĐẾM SỐ CÁCH ĐỀU ═══
B07 = bai(
    7, 'ĐẾM SỐ CÁCH ĐỀU — VÌ SAO PHẢI CỘNG MỘT',
    'Dạng gốc: SỐ 4.1 mức Lớp 4 — Công thức đếm số hạng của dãy cách đều bất kỳ, '
    'và đếm số chia hết trong một khoảng.',
    'Đếm dãy 1, 2, 3 thì dễ. Nhưng đếm dãy 8, 12, 16 cho tới 96 thì đếm tay mỏi '
    'tay. Có một công thức, và nó có một cái bẫy nho nhỏ.',
    LUI_DEM,
    video(
        ['Đếm số hạng của một dãy cách đều bằng hiệu chia khoảng rồi cộng một.',
         'Nói được vì sao phải cộng một.',
         'Đếm được số chia hết cho một số trong một khoảng cho trước.'],
        ['Đề bài: Dãy 8, 12, 16 và cứ thế cách đều cho tới 96. Hỏi dãy có bao nhiêu số?',
         'Ba thứ phải tìm trước',
         'Số đầu là 8, số cuối là 96, và khoảng cách giữa hai số liền nhau là 4.',
         'Đếm số bước nhảy',
         'Từ 8 đi tới 96 phải vượt qua quãng 96 trừ 8, tức 88. Mỗi bước nhảy dài 4 nên '
         'có 88 chia 4, tức 22 bước nhảy.',
         'Vì sao phải cộng một',
         'Hai mươi hai là số BƯỚC NHẢY, không phải số SỐ. Số đầu tiên chưa nhảy bước '
         'nào đã đứng sẵn ở đó rồi, phải đếm nó vào.',
         'Vậy dãy có 22 cộng 1, tức 23 số.',
         'Đáp số: 23 số.',
         'Đếm số chia hết cũng vậy',
         'Từ 1 đến 200 có bao nhiêu số chia hết cho 5? Dãy ấy là 5, 10 cho tới 200, '
         'cách đều 5. Tính: 200 − 5 = 195, rồi 195 : 5 = 39, rồi cộng một được 40.'],
        ['Có bạn tính xong 88 chia 4 được 22 rồi ghi luôn đáp số 22.',
         'Gợi ý 1: Con thử đếm tay một dãy ngắn cho dễ: 8, 12, 16. Được mấy số, và mấy '
         'bước nhảy?',
         'Gợi ý 2: Số bước nhảy bao giờ cũng ít hơn số số đúng một. Vì sao?',
         'Chữa: hai mươi hai là số bước nhảy. Số đầu tiên đứng sẵn ở đó, chưa nhảy '
         'bước nào, nên phải cộng thêm một: 23 số.'],
        ['Đếm bậc cầu thang cùng con: đi từ bậc 1 lên bậc 10 thì bước mấy bước. Bước '
         'thì 9, mà bậc thì 10 — đúng cái bẫy của bài này.',
         'Bố mẹ chỉ cần nhắc một câu mỗi lần: "Con vừa đếm bước nhảy hay đếm số?"'],
    ),
    [
        lt(1, 1, 'Dãy 8, 12, 16 cho tới 96 cách đều bao nhiêu?',
           'Hai số liền nhau hơn kém 4 nên khoảng cách là 4.'),
        lt(2, 1, 'Tính 96 trừ 8 rồi chia cho 4.',
           'Lấy hiệu: 96 − 8 = 88. Rồi 88 : 4 = 22.'),
        lt(3, 1, 'Vậy dãy ấy có bao nhiêu số?',
           'Hai mươi hai là số bước nhảy, cộng thêm số đầu tiên nữa là 23 số.'),
        lt(4, 2, 'Dãy 5, 10, 15 cho tới 200 có bao nhiêu số?',
           'Tính: 200 − 5 = 195, rồi 195 : 5 = 39, rồi cộng một được 40 số.'),
        lt(5, 2, 'Từ 1 đến 200 có bao nhiêu số chia hết cho 5?',
           'Chính là dãy 5, 10 cho tới 200, tức 40 số.'),
        lt(6, 2, 'Từ 20 đến 150 có bao nhiêu số chia hết cho 4? Hãy tìm số đầu, số cuối '
                 'rồi đếm.',
           'Số đầu chia hết cho 4 là 20, số cuối là 148. Tính: 148 − 20 = 128, rồi '
           '128 : 4 = 32, cộng một được 33 số.'),
        lt(7, 2, 'Dãy 1, 2, 3 cho tới 100 có bao nhiêu số?',
           'Khoảng cách là 1: 100 − 1 = 99, rồi 99 : 1 = 99, cộng một được 100 số.'),
        lt(8, 3, 'Dãy 3, 7, 11 cho tới 99 có bao nhiêu số?',
           'Khoảng cách là 4: 99 − 3 = 96, rồi 96 : 4 = 24, cộng một được 25 số.'),
        lt(9, 3, 'Một dãy cách đều 5, số đầu là 12 và có tất cả 20 số. Số cuối là bao '
                 'nhiêu?',
           'Có 20 số thì có 19 bước nhảy: 19 × 5 = 95. Số cuối là 12 + 95 = 107.'),
    ] + [
        q_tf(1, 'Đếm dãy cách đều thì lấy hiệu chia khoảng rồi cộng một.', True,
             'Đúng, và chữ "cộng một" là chỗ hay quên nhất.'),
        q_tf(2, 'Không cần cộng một, vì cộng một là thừa.', False,
             'Sai. Số đầu tiên chưa nhảy bước nào đã đứng sẵn, phải đếm nó vào.'),
        q_mcq(3, 'Dãy 8, 12 cho tới 96 có bao nhiêu số?', ['23', '22', '24', '88'],
              '23', 'Có 22 bước nhảy, cộng thêm số đầu tiên là 23 số.'),
        q_mcq(4, 'Vì sao phải cộng một?',
              ['vì số đầu tiên chưa nhảy đã đứng sẵn ở đó', 'vì cho số chẵn',
               'vì dãy nào cũng bắt đầu từ 1'],
              'vì số đầu tiên chưa nhảy đã đứng sẵn ở đó',
              'Phép chia đếm được số bước nhảy, còn số đầu tiên thì không nhảy bước '
              'nào.'),
        q_tf(5, 'Từ 1 đến 200 có 40 số chia hết cho 5.', True,
             'Đúng. Đó là dãy 5, 10 cho tới 200.'),
    ],
)

# ═══ ⑨ B91 · ĐẾM CHỮ SỐ TRANG SÁCH ═══
B91 = bai(
    91, 'ĐẾM CHỮ SỐ KHI ĐÁNH SỐ TRANG — CHIA NHÓM MÀ ĐẾM',
    'Dạng gốc: SỐ 4.3 mức Lớp 4 — Đếm tổng số chữ số dùng để đánh số trang, và bài '
    'ngược tìm số trang khi biết số chữ số.',
    'Đánh số trang cho một cuốn sổ thì tốn bao nhiêu con chữ? Trang 7 tốn một chữ '
    'số, trang 250 tốn ba. Không đếm chung được — phải chia nhóm.',
    LUI_TRANG,
    video(
        ['Chia số trang thành ba nhóm theo độ dài: một, hai và ba chữ số.',
         'Tính số chữ số của từng nhóm rồi cộng lại.',
         'Giải được bài ngược: biết tổng số chữ số, tìm số trang.'],
        ['Đề bài: Một cuốn sổ dày 250 trang. Đánh số trang thì tốn bao nhiêu chữ số?',
         'Không đếm chung được',
         'Trang 7 tốn một chữ số, trang 70 tốn hai, trang 250 tốn ba. Nên phải tách '
         'thành từng nhóm cùng độ dài.',
         'Nhóm một chữ số',
         'Từ trang 1 đến trang 9 có 9 trang, mỗi trang một chữ số: 9 chữ số.',
         'Nhóm hai chữ số',
         'Từ trang 10 đến trang 99 có 90 trang, mỗi trang hai chữ số: 90 nhân 2 bằng '
         '180 chữ số.',
         'Nhóm ba chữ số',
         'Từ trang 100 đến trang 250 có 151 trang, mỗi trang ba chữ số: 151 nhân 3 '
         'bằng 453 chữ số.',
         'Cộng cả ba nhóm: 9 + 180 + 453 = 642.',
         'Đáp số: 642 chữ số.',
         'Bài ngược thì trừ dần',
         'Biết cuốn sách dùng hết 552 chữ số thì trừ dần: bớt 9 của nhóm một, bớt 180 '
         'của nhóm hai, còn 363. Chia cho 3 được 121 trang, cộng với 99 trang trước đó '
         'là 220 trang.'],
        ['Có bạn lấy 250 nhân 3 rồi bảo cuốn sổ tốn 750 chữ số.',
         'Gợi ý 1: Trang số 7 có tốn ba chữ số không? Còn trang 70 thì mấy?',
         'Gợi ý 2: Vậy có phải trang nào cũng tốn ba chữ số đâu. Con phải tách chúng '
         'thành mấy nhóm?',
         'Chữa: chỉ nhóm từ trang 100 trở đi mới tốn ba chữ số. Phải chia ba nhóm rồi '
         'cộng lại, được 642 chứ không phải 750.'],
        ['Lấy một cuốn sách thật, giở trang 9, trang 10 và trang 100 cho con so. Con '
         'thấy tận mắt chỗ đổi nhóm là hiểu ngay.',
         'Đây là bài dễ nhầm ở chỗ đếm số trang mỗi nhóm. Bố mẹ hỏi lại một câu: "Từ '
         'trang 100 đến trang 250 có bao nhiêu trang?" — bài trước vừa học cách đếm.'],
    ),
    [
        lt(1, 1, 'Từ trang 1 đến trang 9 có bao nhiêu trang, và tốn bao nhiêu chữ số?',
           'Có 9 trang, mỗi trang một chữ số nên tốn 9 chữ số.'),
        lt(2, 1, 'Từ trang 10 đến trang 99 có bao nhiêu trang?',
           'Đếm cách đều 1: 99 − 10 = 89, cộng một được 90 trang.'),
        lt(3, 1, 'Nhóm ấy tốn bao nhiêu chữ số?',
           'Mỗi trang hai chữ số: 90 × 2 = 180 chữ số.'),
        lt(4, 2, 'Từ trang 100 đến trang 250 có bao nhiêu trang?',
           'Đếm cách đều 1: 250 − 100 = 150, cộng một được 151 trang.'),
        lt(5, 2, 'Nhóm ấy tốn bao nhiêu chữ số?',
           'Mỗi trang ba chữ số: 151 × 3 = 453 chữ số.'),
        lt(6, 2, 'Cả cuốn 250 trang tốn bao nhiêu chữ số?',
           'Cộng ba nhóm: 9 + 180 + 453 = 642 chữ số.'),
        lt(7, 2, 'Một cuốn sách dùng hết 552 chữ số. Trừ phần của nhóm một chữ số và '
                 'nhóm hai chữ số thì còn bao nhiêu?',
           'Trừ dần: 552 − 9 = 543, rồi 543 − 180 = 363 chữ số.'),
        lt(8, 3, 'Phần còn lại ấy đủ đánh cho bao nhiêu trang ba chữ số?',
           'Mỗi trang ba chữ số nên 363 : 3 = 121 trang.'),
        lt(9, 3, 'Vậy cuốn sách ấy dày bao nhiêu trang?',
           'Chín trang nhóm một cộng 90 trang nhóm hai là 99 trang, cộng thêm 121 '
           'trang: 99 + 121 = 220 trang.'),
    ] + [
        q_tf(1, 'Từ trang 10 đến trang 99 có 90 trang.', True,
             'Đúng: 99 − 10 = 89, cộng một được 90.'),
        q_mcq(2, 'Cuốn sổ 250 trang tốn bao nhiêu chữ số?',
              ['642', '750', '453', '250'], '642',
              'Cộng ba nhóm: 9 rồi 180 rồi 453.'),
        q_tf(3, 'Trang nào cũng tốn đúng ba chữ số.', False,
             'Sai. Trang một chữ số, hai chữ số và ba chữ số tốn khác nhau.'),
        q_mcq(4, 'Bài ngược thì làm thế nào?',
              ['trừ dần theo từng nhóm', 'chia luôn cho 3', 'nhân với 3'],
              'trừ dần theo từng nhóm',
              'Bớt phần của nhóm một, rồi nhóm hai, phần còn lại mới chia cho 3.'),
        q_tf(5, 'Từ trang 100 đến trang 250 có 151 trang.', True,
             'Đúng: 250 − 100 = 150, cộng một được 151.'),
    ],
)

# ═══ ⑩ B08 · QUY TẮC NHÂN ═══
B08 = bai(
    8, 'QUY TẮC NHÂN — MỖI HÀNG MỘT Ô, RỒI NHÂN DỒN',
    'Dạng gốc: SỐ 4.2 mức Lớp 4 — Quy tắc nhân: đếm số cách chọn của từng hàng rồi '
    'nhân lại; áp thêm điều kiện vào đúng hàng.',
    'Ổ khoá ba vòng, mỗi vòng chín chữ số. Có bao nhiêu mật khẩu? Liệt kê ra thì '
    'chép cả ngày. Có một cách đếm không phải liệt kê.',
    LUI_NHAN,
    video(
        ['Kẻ một ô cho mỗi hàng rồi điền số cách chọn của hàng ấy.',
         'Nhân dồn các số cách lại để ra tổng số cách.',
         'Biết điều kiện rơi vào hàng nào thì sửa số cách của đúng hàng ấy.'],
        ['Đề bài: Một ổ khoá có ba vòng, mỗi vòng chọn được một chữ số từ 1 đến 9. Hỏi '
         'có bao nhiêu mật khẩu?',
         'Kẻ ô cho từng hàng',
         'Ba vòng thì kẻ ba ô. Mỗi ô ghi số cách chọn của vòng ấy: 9, rồi 9, rồi 9.',
         'Vì sao lại nhân',
         'Mỗi cách của vòng một ghép được với đủ chín cách của vòng hai, rồi mỗi cặp '
         'ấy lại ghép được với đủ chín cách của vòng ba.',
         'Nên nhân dồn: 9 × 9 × 9 = 729.',
         'Đáp số: 729 mật khẩu.',
         'Kiểm bằng người quen',
         'Đếm mọi số có ba chữ số cũng một lối ấy: hàng trăm 9 cách vì không được là '
         '0, hàng chục 10 cách, hàng đơn vị 10 cách. Được 9 × 10 × 10 = 900 — đúng '
         'bằng số các số có ba chữ số.',
         'Thêm điều kiện thì sao',
         'Mật khẩu không chứa 0 mà lại là số chẵn thì chỉ hàng đơn vị bị siết, chỉ còn '
         'chọn được 2, 4, 6 hoặc 8, tức 4 cách. Kết quả: 9 × 9 × 4 = 324.'],
        ['Có bạn đếm ba vòng khoá rồi cộng lại: "9 cộng 9 cộng 9 bằng 27 mật khẩu."',
         'Gợi ý 1: Con thử với ổ khoá hai vòng, mỗi vòng chỉ có 2 chữ số thôi. Liệt kê '
         'ra giấy xem được mấy mật khẩu.',
         'Gợi ý 2: Liệt kê được 4 chứ không phải 4 do cộng — con thử xem 2 và 2 phải '
         'làm phép gì mới ra 4.',
         'Chữa: mỗi cách của vòng trước ghép được với ĐỦ mọi cách của vòng sau, nên '
         'phải nhân chứ không cộng. Kết quả là 729.'],
        ['Lấy hai bộ quần áo và ba cái mũ, cho con thử mọi cách phối. Đếm ra 6 chứ '
         'không phải 5 — đó chính là quy tắc nhân.',
         'Con hay lẫn cộng với nhân. Mẹo phân biệt: chọn MỘT thứ trong nhiều nhóm thì '
         'cộng; chọn MỖI NHÓM một thứ rồi ghép lại thì nhân.'],
    ),
    [
        lt(1, 1, 'Ổ khoá ba vòng, mỗi vòng 9 cách chọn. Có bao nhiêu mật khẩu?',
           'Nhân dồn ba ô: 9 × 9 × 9 = 729.'),
        lt(2, 1, 'Chữ số hàng trăm của một số có ba chữ số có mấy cách chọn?',
           'Chọn từ 1 đến 9, tức 9 cách — không được là 0 vì số sẽ tụt mất một chữ số.'),
        lt(3, 1, 'Chữ số hàng chục của số ấy có mấy cách chọn?',
           'Chọn từ 0 đến 9, tức 10 cách.'),
        lt(4, 2, 'Vậy có bao nhiêu số có ba chữ số?',
           'Nhân dồn: 9 × 10 × 10 = 900.'),
        lt(5, 2, 'Mật khẩu ba chữ số không chứa 0 và phải là số chẵn. Hàng đơn vị có '
                 'mấy cách chọn?',
           'Chỉ chọn được 2, 4, 6, 8 — tức 4 cách.'),
        lt(6, 2, 'Vậy có bao nhiêu mật khẩu như thế?',
           'Nhân dồn: 9 × 9 × 4 = 324.'),
        lt(7, 2, 'Ổ khoá hai vòng, mỗi vòng 9 cách chọn thì có bao nhiêu mật khẩu?',
           'Nhân dồn hai ô: 9 × 9 = 81.'),
        lt(8, 3, 'Lập số có hai chữ số KHÁC NHAU từ các chữ số 1 đến 9. Hàng chục mấy '
                 'cách, hàng đơn vị mấy cách, và tất cả bao nhiêu số?',
           'Hàng chục 9 cách. Hàng đơn vị phải khác chữ số vừa chọn nên chỉ còn 8 cách. '
           'Tất cả: 9 × 8 = 72 số.'),
        lt(9, 3, 'Ổ khoá bốn vòng, mỗi vòng 9 cách chọn thì có bao nhiêu mật khẩu?',
           'Nhân dồn bốn ô: 9 × 9 × 9 × 9 = 6 561.'),
    ] + [
        q_tf(1, 'Quy tắc nhân là nhân số cách chọn của từng hàng với nhau.', True,
             'Đúng. Kẻ một ô cho mỗi hàng rồi nhân dồn.'),
        q_mcq(2, 'Ba vòng khoá, mỗi vòng 9 cách, có bao nhiêu mật khẩu?',
              ['729', '27', '81', '999'], '729',
              'Nhân dồn 9 × 9 × 9.'),
        q_tf(3, 'Chữ số hàng trăm của một số ba chữ số có 10 cách chọn.', False,
             'Sai. Chỉ 9 cách, vì nó không được là 0.'),
        q_mcq(4, 'Có bao nhiêu số có ba chữ số?', ['900', '999', '1 000', '899'],
              '900', 'Nhân dồn 9 × 10 × 10.'),
        q_tf(5, 'Điều kiện rơi vào hàng nào thì sửa số cách của đúng hàng ấy.', True,
             'Đúng. Các hàng khác giữ nguyên.'),
    ],
)

# ═══ ⑪ B92 · ĐẾM BẰNG PHẦN BÙ ═══
B92 = bai(
    92, 'ĐẾM BẰNG PHẦN BÙ — ĐẾM NGƯỢC CHO NHANH',
    'Dạng gốc: SỐ 4.2 mức Lớp 4 — Phép đếm phần bù: lấy tất cả trừ đi phần không '
    'thoả điều kiện.',
    'Có những câu hỏi mà đếm thẳng thì rối tung, nhưng đếm cái ngược lại thì dễ như '
    'chơi. Rồi lấy tất cả trừ đi là xong.',
    LUI_NHAN,
    video(
        ['Biết khi nào nên đếm ngược: khi đếm thẳng phải chia nhiều trường hợp.',
         'Đếm phần không thoả điều kiện, rồi lấy tất cả trừ đi.',
         'Nhận ra dấu hiệu: gặp chữ "có chứa" hay "ít nhất một" thì nghĩ tới phần bù.'],
        ['Đề bài: Có bao nhiêu số có ba chữ số mà trong đó CÓ chứa chữ số 0?',
         'Vì sao đếm thẳng thì rối',
         'Chữ số 0 có thể nằm ở hàng chục, ở hàng đơn vị, hoặc ở cả hai. Ba trường hợp, '
         'lại còn chồng lên nhau — đếm dễ sót mà cũng dễ đếm trùng.',
         'Đếm ngược thì gọn',
         'Đếm những số KHÔNG chứa chữ số 0 thôi. Khi ấy mỗi hàng chỉ chọn từ 1 đến 9, '
         'tức 9 cách.',
         'Nhân dồn: 9 × 9 × 9 = 729 số.',
         'Lấy tất cả trừ đi',
         'Tất cả các số có ba chữ số là 900. Vậy số có chứa chữ số 0 là 900 − 729 = 171.',
         'Đáp số: 171 số.',
         'Dấu hiệu nhận ra',
         'Gặp chữ "có chứa" hoặc "ít nhất một" thì nghĩ ngay tới phần bù — vì cái ngược '
         'lại của chúng là "không có cái nào", mà cái ấy đếm rất gọn.'],
        ['Có bạn đếm thẳng số có chứa chữ số 0, cộng ba trường hợp lại rồi ra một số '
         'lớn hơn cả 900.',
         'Gợi ý 1: Số 100 có chữ số 0 ở hàng chục, mà cũng có ở hàng đơn vị. Bạn ấy '
         'đếm nó mấy lần?',
         'Gợi ý 2: Thay vì đếm số CÓ, con thử đếm số KHÔNG có xem có gọn hơn không.',
         'Chữa: cộng ba trường hợp thì những số có hai chữ số 0 bị đếm hai lần. Đếm '
         'ngược rồi trừ thì không bao giờ trùng: 900 − 729 = 171.'],
        ['Chơi trò đếm ngược ngoài đời: trong nhà có mấy đồ KHÔNG phải màu trắng — dễ '
         'hơn nhiều so với đếm từng đồ trắng một.',
         'Bí quyết chỉ có một câu: gặp chữ "có chứa" hay "ít nhất một" là nghĩ ngay '
         'tới đếm ngược.'],
    ),
    [
        lt(1, 1, 'Có bao nhiêu số có ba chữ số?',
           'Nhân dồn: 9 × 10 × 10 = 900 số.'),
        lt(2, 1, 'Có bao nhiêu số có ba chữ số mà KHÔNG chứa chữ số 0?',
           'Mỗi hàng chỉ chọn từ 1 đến 9: 9 × 9 × 9 = 729 số.'),
        lt(3, 1, 'Vậy có bao nhiêu số có ba chữ số CÓ chứa chữ số 0?',
           'Lấy tất cả trừ đi: 900 − 729 = 171 số.'),
        lt(4, 2, 'Vì sao đếm ngược lại dễ hơn đếm thẳng ở bài này?',
           'Vì đếm thẳng phải chia nhiều trường hợp, mà các trường hợp ấy còn chồng '
           'lên nhau nên dễ đếm trùng.'),
        lt(5, 2, 'Có bao nhiêu số có hai chữ số?',
           'Hàng chục 9 cách, hàng đơn vị 10 cách: 9 × 10 = 90 số.'),
        lt(6, 2, 'Có bao nhiêu số có hai chữ số mà không chứa chữ số 0?',
           'Cả hai hàng đều chọn từ 1 đến 9: 9 × 9 = 81 số.'),
        lt(7, 2, 'Vậy có bao nhiêu số có hai chữ số có chứa chữ số 0?',
           'Lấy hiệu: 90 − 81 = 9 số. Đó là 10, 20 cho tới 90.'),
        lt(8, 3, 'Có bao nhiêu số có ba chữ số không chứa chữ số 5, và bao nhiêu số có '
                 'ít nhất một chữ số 5?',
           'Không chứa 5: hàng trăm 8 cách, hai hàng sau mỗi hàng 9 cách, được '
           '8 × 9 × 9 = 648 số. Có ít nhất một chữ số 5: 900 − 648 = 252 số.'),
        lt(9, 3, 'Có bao nhiêu số có ba chữ số mà cả ba chữ số đều lẻ?',
           'Mỗi hàng chọn trong 1, 3, 5, 7, 9 nên đều 5 cách: 5 × 5 × 5 = 125 số.'),
    ] + [
        q_tf(1, 'Gặp chữ "có chứa" thì nên nghĩ tới đếm phần bù.', True,
             'Đúng, vì cái ngược lại của nó thường đếm rất gọn.'),
        q_mcq(2, 'Có bao nhiêu số ba chữ số có chứa chữ số 0?',
              ['171', '729', '900', '100'], '171',
              'Lấy 900 trừ đi 729 số không chứa chữ số 0.'),
        q_tf(3, 'Phần bù là lấy tất cả trừ đi phần không thoả điều kiện.', True,
             'Đúng. Trừ một lần là xong, không lo đếm trùng.'),
        q_mcq(4, 'Số có ba chữ số không chứa chữ số 0 thì có',
              ['729', '900', '171', '81'], '729',
              'Mỗi hàng 9 cách nên nhân dồn được 729.'),
        q_tf(5, 'Đếm thẳng bao giờ cũng nhanh hơn đếm phần bù.', False,
             'Sai. Có bài đếm thẳng phải chia nhiều trường hợp chồng nhau, rối hơn '
             'hẳn.'),
    ],
)

MOI = [B05, B86, B87, B88, B06, B89, B90, B07, B91, B08, B92]

SAU = {
    'DL:KSN4.B86': 'DL:KSN4.B05',
    'DL:KSN4.B87': 'DL:KSN4.B86',
    'DL:KSN4.B88': 'DL:KSN4.B87',
    'DL:KSN4.B89': 'DL:KSN4.B06',
    'DL:KSN4.B90': 'DL:KSN4.B89',
    'DL:KSN4.B91': 'DL:KSN4.B07',
    'DL:KSN4.B92': 'DL:KSN4.B08',
}

O_NHAP_MOI = {
 'DL:KSN4.B05#C1': {'value': 4},
 'DL:KSN4.B05#C2': {'value': 100},
 'DL:KSN4.B05#C3': {'value': 400},
 'DL:KSN4.B05#C4': {'parts': [{'label': 'trong ngoặc', 'value': 100},
                              {'label': 'kết quả', 'value': 700}]},
 'DL:KSN4.B05#C5': {'parts': [{'label': 'trong ngoặc', 'value': 10},
                              {'label': 'kết quả', 'value': 90}]},
 'DL:KSN4.B05#C6': {'value': 120},
 'DL:KSN4.B05#C7': {'value': 500},
 'DL:KSN4.B05#C8': {'parts': [{'label': 'trong ngoặc', 'value': 100},
                              {'label': 'kết quả', 'value': 800}]},
 'DL:KSN4.B05#C9': {'value': 150},

 'DL:KSN4.B86#C1': {'value': 4},
 'DL:KSN4.B86#C2': {'value': 900},
 'DL:KSN4.B86#C3': {'value': 200},
 'DL:KSN4.B86#C4': {'value': 400},
 'DL:KSN4.B86#C5': {'parts': [{'label': 'nhân 100 trước được', 'value': 4800},
                              {'label': 'kết quả', 'value': 1200}]},
 'DL:KSN4.B86#C6': {'value': 300},
 'DL:KSN4.B86#C7': {'value': 8},
 'DL:KSN4.B86#C8': {'parts': [{'label': 'thừa số còn lại sau khi tách', 'value': 3},
                              {'label': 'kết quả', 'value': 3000}]},
 'DL:KSN4.B86#C9': {'value': 1100},

 'DL:KSN4.B87#C1': {'value': 350},
 'DL:KSN4.B87#C2': {'value': 385},
 'DL:KSN4.B87#C3': {'value': 385},
 'DL:KSN4.B87#C4': {'value': 264},
 'DL:KSN4.B87#C5': {'value': 8},
 'DL:KSN4.B87#C6': {'value': 682},
 'DL:KSN4.B87#C7': {'value': 627},
 'DL:KSN4.B87#C8': {'parts': [{'label': 'phải làm gì',
                               'options': ['nhớ 1 sang trái', 'bỏ bớt chữ số đi'],
                               'value': 'nhớ 1 sang trái'}]},
 'DL:KSN4.B87#C9': {'value': 121},

 'DL:KSN4.B88#C1': {'value': 13},
 'DL:KSN4.B88#C2': {'value': 0},
 'DL:KSN4.B88#C3': {'value': 0},
 'DL:KSN4.B88#C4': {'value': 0},
 'DL:KSN4.B88#C5': {'value': 25},
 'DL:KSN4.B88#C6': {'parts': [{'label': 'bên nào lớn hơn',
                               'options': ['bên trái', 'bên phải'],
                               'value': 'bên trái'}]},
 'DL:KSN4.B88#C7': {'value': 0},
 'DL:KSN4.B88#C8': {'parts': [{'label': 'hai bên thế nào',
                               'options': ['bằng nhau', 'khác nhau'],
                               'value': 'bằng nhau'}]},
 'DL:KSN4.B88#C9': {'value': 0},

 'DL:KSN4.B06#C1': {'value': 5},
 'DL:KSN4.B06#C2': {'value': 9},
 'DL:KSN4.B06#C3': {'value': 45},
 'DL:KSN4.B06#C4': {'parts': [{'label': 'gom lại thành X nhân', 'value': 10},
                              {'label': 'X', 'value': 8}]},
 'DL:KSN4.B06#C5': {'parts': [{'label': 'gom lại thành X nhân', 'value': 4},
                              {'label': 'X', 'value': 6}]},
 'DL:KSN4.B06#C6': {'value': 9},
 'DL:KSN4.B06#C7': {'value': 6},
 'DL:KSN4.B06#C8': {'parts': [{'label': 'gom lại thành X nhân', 'value': 7},
                              {'label': 'X', 'value': 9}]},
 'DL:KSN4.B06#C9': {'value': 10},

 'DL:KSN4.B89#C1': {'value': 24},
 'DL:KSN4.B89#C2': {'value': 39},
 'DL:KSN4.B89#C3': {'value': 8},
 'DL:KSN4.B89#C4': {'parts': [{'label': 'giá trị của ngoặc', 'value': 15},
                              {'label': 'X', 'value': 8}]},
 'DL:KSN4.B89#C5': {'value': 7},
 'DL:KSN4.B89#C6': {'value': 30},
 'DL:KSN4.B89#C7': {'value': 34},
 'DL:KSN4.B89#C8': {'parts': [{'label': 'giá trị của ngoặc trong', 'value': 17},
                              {'label': 'X', 'value': 12}]},
 'DL:KSN4.B89#C9': {'value': 20},

 'DL:KSN4.B90#C1': {'value': 56},
 'DL:KSN4.B90#C2': {'value': 59},
 'DL:KSN4.B90#C3': {'parts': [{'label': 'thương', 'value': 8},
                              {'label': 'số dư', 'value': 3}]},
 'DL:KSN4.B90#C4': {'value': 49},
 'DL:KSN4.B90#C5': {'value': 42},
 'DL:KSN4.B90#C6': {'value': 7},
 'DL:KSN4.B90#C7': {'parts': [{'label': 'có hợp luật không', 'options': CO_KHONG,
                               'value': 'có'}]},
 'DL:KSN4.B90#C8': {'value': 47},
 'DL:KSN4.B90#C9': {'parts': [{'label': 'phần chia hết', 'value': 56},
                              {'label': 'X', 'value': 7}]},

 'DL:KSN4.B07#C1': {'value': 4},
 'DL:KSN4.B07#C2': {'value': 22},
 'DL:KSN4.B07#C3': {'value': 23},
 'DL:KSN4.B07#C4': {'value': 40},
 'DL:KSN4.B07#C5': {'value': 40},
 'DL:KSN4.B07#C6': {'parts': [{'label': 'số đầu', 'value': 20},
                              {'label': 'số cuối', 'value': 148},
                              {'label': 'có mấy số', 'value': 33}]},
 'DL:KSN4.B07#C7': {'value': 100},
 'DL:KSN4.B07#C8': {'value': 25},
 'DL:KSN4.B07#C9': {'value': 107},

 'DL:KSN4.B91#C1': {'parts': [{'label': 'số trang', 'value': 9},
                              {'label': 'số chữ số', 'value': 9}]},
 'DL:KSN4.B91#C2': {'value': 90},
 'DL:KSN4.B91#C3': {'value': 180},
 'DL:KSN4.B91#C4': {'value': 151},
 'DL:KSN4.B91#C5': {'value': 453},
 'DL:KSN4.B91#C6': {'value': 642},
 'DL:KSN4.B91#C7': {'value': 363},
 'DL:KSN4.B91#C8': {'value': 121},
 'DL:KSN4.B91#C9': {'value': 220},

 'DL:KSN4.B08#C1': {'value': 729},
 'DL:KSN4.B08#C2': {'value': 9},
 'DL:KSN4.B08#C3': {'value': 10},
 'DL:KSN4.B08#C4': {'value': 900},
 'DL:KSN4.B08#C5': {'value': 4},
 'DL:KSN4.B08#C6': {'value': 324},
 'DL:KSN4.B08#C7': {'value': 81},
 'DL:KSN4.B08#C8': {'parts': [{'label': 'hàng chục', 'value': 9},
                              {'label': 'hàng đơn vị', 'value': 8},
                              {'label': 'tất cả', 'value': 72}]},
 'DL:KSN4.B08#C9': {'value': 6561},

 'DL:KSN4.B92#C1': {'value': 900},
 'DL:KSN4.B92#C2': {'value': 729},
 'DL:KSN4.B92#C3': {'value': 171},
 'DL:KSN4.B92#C4': {'parts': [{'label': 'vì sao',
                               'options': ['vì đếm thẳng phải chia nhiều trường hợp',
                                           'vì con số nhỏ hơn'],
                               'value': 'vì đếm thẳng phải chia nhiều trường hợp'}]},
 'DL:KSN4.B92#C5': {'value': 90},
 'DL:KSN4.B92#C6': {'value': 81},
 'DL:KSN4.B92#C7': {'value': 9},
 'DL:KSN4.B92#C8': {'parts': [{'label': 'không chứa chữ số 5', 'value': 648},
                              {'label': 'có ít nhất một chữ số 5', 'value': 252}]},
 'DL:KSN4.B92#C9': {'value': 125},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN4.B{n:02d}' for n in (5, 6, 7, 8)}
    moi_ = {f'DL:KSN4.B{n}' for n in range(86, 93)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        for m in ('chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
    NEO = {'DL:KSN4.B05': '4 × 38', 'DL:KSN4.B86': '25 × 36',
           'DL:KSN4.B87': '35 × 11', 'DL:KSN4.B06': '45',
           'DL:KSN4.B91': '642', 'DL:KSN4.B08': '729', 'DL:KSN4.B92': '171'}
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
        print(f"  {b['id']}  {b['ten'][:52]:52} {n} luyện + {q} quiz")
    if a.xem:
        print('\n(--xem: chưa ghi gì)')
        return
    for b in MOI:
        tep = RA / f"DL_KSN4_B{b['so']:02d}.json"
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
    o = json.loads(O_NHAP.read_text('utf8'))
    o.update(O_NHAP_MOI)
    O_NHAP.write_text(json.dumps(o, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'\nghi {len(MOI)} bài · thứ tự học nay {len(tt["thuTu"])} bài · '
          f'thêm {len(O_NHAP_MOI)} ô nhập')


if __name__ == '__main__':
    main()
