# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 4 · SIÊU NHÂN TÍNH NHANH — bốn bài chữ thành mười bài video.

  · B12 gộp "ghép đôi tròn chục" (phép CỘNG) với "ghép hai khay kẹo" (phép NHÂN).
    Hai phép tính khác nhau, hai hình dung khác nhau — gộp một bài thì bé nhớ được
    mẹo nhưng không biết lúc nào dùng cái nào.
  · B13 gộp "ghép cặp đầu cuối" với "dãy lẻ số thì có một bạn đứng giữa". Cái sau
    chính là chỗ sách tự nêu ra là hay sai nhất.
  · B14 gộp BA ca tìm ô trống: cộng trừ ngược nhau, nhân chia ngược nhau, và ca
    ô trống đứng SAU dấu trừ — ca cuối làm ngược lại hai ca đầu.
  · B15 gộp "chia theo vòng" với "luật vàng số thừa bé hơn số bạn" và "chia hết
    hay còn thừa".

── SỐ NEO ──
    37 + 25 + 13 + 5   → ghép đuôi thành 50 và 30, tổng 80
    3 × 4 + 3 × 6      → cùng 3 hàng, gộp thành 3 × 10 = 30
    1 tới 8            → bốn cặp chín, tổng 36
    1 tới 9            → bốn cặp mười và số 5 đứng giữa, tổng 45
    ô trống + 5 = 12   → cho 12 chạy ngược, được 7
    ô trống × 4 = 28   → cho 28 chạy ngược, được 7
    14 − ô trống = 6   → lấy 14 trừ 6, được 8
    20 viên · 6 bạn    → mỗi bạn 3 viên, thừa 2
    17 viên · 3 bạn    → "thừa 5" là vô lý, đúng ra mỗi bạn 5 thừa 2
    15 và 17 chia 3    → một số chia hết, một số thừa 2

⚠ KHÔNG dùng chữ "X" làm tên ô trống. Sách đặt tên bài là "ĐI TÌM SỐ BÍ MẬT X",
mà máy đọc chữ X thành "ích-xì" kiểu tiếng Anh — cổng video đã bắt mười lăm chỗ
như thế ở lớp 4. Cả mười bài này gọi là "ô trống".

    python3 tools/tinh_nhanh_lop2.py --xem
    python3 tools/tinh_nhanh_lop2.py
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

TEN_CHUONG = 'Siêu nhân tính nhanh'
CHUONG = 4
CO_KHONG = ['có', 'không']
DUNG_SAI = ['đúng', 'sai']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng video: hai mục mở bài và khám phá để RỖNG, video thay cả hai."""
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B12 · GHÉP ĐÔI TRÒN CHỤC ═══
B12 = bai(
    12, 'GHÉP ĐÔI TRÒN CHỤC — DÒM ĐUÔI TÌM ĐÔI BẠN',
    'SỐ 7.1a — Tính thuận tiện phép cộng: ghép cặp có tổng tròn chục.',
    video(
        ['Nhìn chữ số tận cùng để bắt cặp hai số có tổng tròn chục.',
         'Biết đổi chỗ các số hạng cho đôi bạn đứng cạnh nhau.',
         'Cộng dãy dài nhanh mà không phải đặt tính dọc.'],
        ['Đề bài: Tính bằng cách thuận tiện: 37 + 25 + 13 + 5.',
         'Dòm đuôi tìm đôi bạn',
         'Đuôi 7 bắt cặp với đuôi 3 vì 7 + 3 = 10. Đuôi 5 bắt cặp với đuôi 5 vì '
         '5 + 5 = 10.',
         'Kéo đôi bạn về đứng cạnh nhau',
         'Phép cộng đổi chỗ thoải mái mà tổng vẫn vậy, nên ghép được 37 + 13 = 50 và '
         '25 + 5 = 30.',
         'Cộng hai số tròn chục',
         'Còn lại phép dễ nhất: 50 + 30 = 80.',
         'Đáp số: 80.',
         'Số tròn chục thì nhẩm được ngay, không phải đặt tính dọc lần nào.'],
        ['Có bạn phản đối, bảo phép tính phải làm từ trái sang phải nên phải cộng 37 '
         'với 25 trước đã.',
         'Gợi ý 1: Con tính 3 + 5 rồi tính 5 + 3 xem hai kết quả có khác nhau không.',
         'Gợi ý 2: Tính cả dãy theo hai cách — từ trái sang, và ghép đôi — rồi so hai '
         'kết quả.',
         'Chữa: phép cộng đổi chỗ thì tổng giữ nguyên, nên kéo đôi bạn về cạnh nhau '
         'là hợp luật, mà lại nhanh hơn nhiều.'],
        ['Đi chợ cùng con: cộng nhẩm mấy món có giá đuôi bù nhau, ví dụ 26 nghìn với '
         '24 nghìn. Con sẽ thấy mẹo này dùng được thật.',
         'Bố mẹ hỏi một câu: "Đuôi của hai số này cộng lại có tròn chục không?"'],
    ),
    [
        lt(1, 1, 'Tính 6 + 4.', 'Lấy 6 + 4 = 10.'),
        lt(2, 1, 'Số có đuôi 8 phải bắt cặp với số có đuôi mấy để tổng tròn chục?',
           'Vì 8 + 2 = 10 nên đuôi 8 đi với đuôi 2.'),
        lt(3, 1, 'Tính 26 + 4.', 'Lấy 26 + 4 = 30.'),
        lt(4, 2, 'Tính nhanh 26 + 18 + 4 + 12 bằng cách ghép đôi.',
           'Ghép 26 + 4 = 30 và 18 + 12 = 30, rồi 30 + 30 = 60.'),
        lt(5, 2, 'Tính nhanh 37 + 25 + 13 + 5.',
           'Ghép 37 + 13 = 50 và 25 + 5 = 30, rồi 50 + 30 = 80.'),
        lt(6, 2, 'Vì sao được phép đổi chỗ các số trong một dãy cộng?',
           'Vì phép cộng đổi chỗ thì tổng vẫn giữ nguyên.'),
        lt(7, 3, 'Tính nhanh 15 + 47 + 35 + 3.',
           'Ghép 15 + 35 = 50 và 47 + 3 = 50, rồi 50 + 50 = 100.'),
        lt(8, 3, 'Trong dãy 22 + 19 + 8 + 11, số 22 nên bắt cặp với số nào, và tổng '
                 'cả dãy bằng bao nhiêu?',
           'Đuôi 2 bắt cặp đuôi 8 nên 22 đi với 8: 22 + 8 = 30. Còn lại 19 + 11 = 30. '
           'Tổng là 30 + 30 = 60.'),
    ] + [
        q_tf(1, 'Hai số có đuôi cộng lại bằng 10 thì tổng của chúng tròn chục.', True,
             'Đúng — đó là cách nhận ra đôi bạn.'),
        q_tf(2, 'Đổi chỗ các số trong một dãy cộng thì tổng thay đổi.', False,
             'Sai. Phép cộng đổi chỗ thì tổng giữ nguyên.'),
        q_mcq(3, 'Số có đuôi 8 bắt cặp với số có đuôi mấy?', ['2', '8', '1', '5'],
              '2', 'Vì 8 cộng 2 vừa tròn một chục.'),
        q_mcq(4, 'Tính nhanh 26 + 18 + 4 + 12.', ['60', '50', '58', '62'], '60',
              'Hai cặp đều bằng 30.'),
        q_tf(5, 'Trước khi cộng một dãy dài, nên dòm đuôi tìm đôi bạn tròn chục.',
             True, 'Đúng — nhìn trước một giây, đỡ tính cả phút.'),
    ],
)

# ═══ ② B48 · GHÉP HAI KHAY KẸO ═══
B48 = bai(
    48, 'GHÉP HAI KHAY KẸO — CÙNG SỐ HÀNG THÌ GỘP LÀM MỘT',
    'SỐ 7.1b — Tính thuận tiện phép nhân: mầm non của thừa số chung.',
    video(
        ['Nhận ra hai phép nhân có cùng số hàng.',
         'Gộp hai khay cùng số hàng thành một khay to.',
         'Hiểu vì sao số hàng giữ nguyên mà mỗi hàng dài thêm.'],
        ['Đề bài: Tính nhanh 3 × 4 + 3 × 6.',
         'Hai khay đều có 3 hàng',
         'Khay thứ nhất 3 hàng, mỗi hàng 4 viên. Khay thứ hai cũng 3 hàng, mỗi hàng '
         '6 viên.',
         'Đẩy hai khay sát vào nhau',
         'Số hàng vẫn là 3, còn mỗi hàng nay dài thêm: 4 + 6 = 10 viên.',
         'Thành một khay to',
         'Khay to là 3 hàng mười viên: 3 × 10 = 30.',
         'Đáp số: 30.',
         'Tính riêng cũng ra đúng thế: 3 × 4 = 12 và 3 × 6 = 18, mà 12 + 18 = 30.'],
        ['Có bạn ghép hai khay rồi cộng luôn cả số hàng, ra khay 6 hàng mười viên.',
         'Gợi ý 1: Đẩy hai khay sát vào nhau thì hàng nằm chồng lên nhau hay nối dài '
         'ra?',
         'Gợi ý 2: Con đếm lại số hàng của khay to xem có đúng 3 hàng không.',
         'Chữa: đẩy sát vào nhau thì mỗi hàng nối dài ra, còn số hàng giữ nguyên là '
         '3. Khay to là 3 × 10 chứ không phải 6 × 10.'],
        ['Xếp kẹo hoặc hạt ra bàn thành hai khay rồi đẩy sát vào nhau cho con nhìn — '
         'thấy tận mắt một lần là nhớ.',
         'Bố mẹ hỏi: "Ghép xong thì số hàng đổi hay mỗi hàng đổi?"'],
    ),
    [
        lt(1, 1, 'Tính 3 × 4.', 'Lấy 3 × 4 = 12.'),
        lt(2, 1, 'Tính 3 × 6.', 'Lấy 3 × 6 = 18.'),
        lt(3, 1, 'Hai khay đều 3 hàng, một khay mỗi hàng 4 viên, khay kia mỗi hàng '
                 '6 viên. Ghép lại thì mỗi hàng có mấy viên?',
           'Mỗi hàng nối dài ra: 4 + 6 = 10 viên.'),
        lt(4, 2, 'Tính nhanh 3 × 4 + 3 × 6 bằng cách ghép hai khay.',
           'Ghép lại thành 3 hàng mười viên: 3 × 10 = 30.'),
        lt(5, 2, 'Tính nhanh 5 × 3 + 5 × 7.',
           'Vẫn 5 hàng, mỗi hàng dài thành 3 + 7 = 10 viên, nên 5 × 10 = 50.'),
        lt(6, 2, 'Ghép hai khay 2 × 8 và 2 × 2 thì được khay mấy hàng, mỗi hàng mấy '
                 'viên?',
           'Số hàng vẫn là 2, mỗi hàng dài thành 8 + 2 = 10 viên.'),
        lt(7, 3, 'Tính nhanh 4 × 6 + 4 × 4.',
           'Vẫn 4 hàng, mỗi hàng dài thành 6 + 4 = 10 viên, nên 4 × 10 = 40.'),
        lt(8, 3, 'Hai khay 3 × 5 và 2 × 6 có ghép thành một khay to được không, và cả '
                 'hai khay có tất cả bao nhiêu viên?',
           'Khay này 3 hàng, khay kia 2 hàng nên không ghép được. Phải tính riêng: '
           '3 × 5 = 15 và 2 × 6 = 12, cộng lại được 27 viên.'),
    ] + [
        q_tf(1, 'Hai khay có cùng số hàng thì ghép lại thành một khay to.', True,
             'Đúng — đó là điều kiện để ghép.'),
        q_mcq(2, 'Tính nhanh 3 × 4 + 3 × 6.', ['30', '24', '18', '36'], '30',
              'Ghép thành 3 hàng mười viên.'),
        q_tf(3, 'Ghép hai khay 5 × 3 và 5 × 7 thì được khay 5 × 10.', True,
             'Đúng — vẫn 5 hàng, mỗi hàng dài thành mười.'),
        q_mcq(4, 'Ghép hai khay cùng 4 hàng, một khay mỗi hàng 6 viên, khay kia mỗi '
                 'hàng 4 viên. Khay to có mấy hàng?',
              ['4', '8', '10', '40'], '4', 'Số hàng không đổi, chỉ mỗi hàng dài thêm.'),
        q_tf(5, 'Ghép hai khay thì số hàng cộng lại với nhau.', False,
             'Sai. Số hàng giữ nguyên, chỉ mỗi hàng dài thêm.'),
    ],
)

# ═══ ③ B13 · GHÉP CẶP ĐẦU VỚI CUỐI ═══
B13 = bai(
    13, 'GHÉP CẶP ĐẦU VỚI CUỐI — MỌI CẶP ĐỀU BẰNG NHAU',
    'SỐ 7.1c — Tổng dãy cách đều bằng cách ghép cặp đầu với cuối.',
    video(
        ['Tính tổng một dãy bằng cách ghép số đầu với số cuối.',
         'Giải thích được vì sao mọi cặp đều bằng nhau.',
         'Đếm số cặp rồi cộng dồn.'],
        ['Đề bài: Tính nhanh tổng 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8.',
         'Bắc cầu nối số đầu với số cuối',
         'Cặp ngoài cùng là 1 + 8 = 9. Lùi vào trong: 2 + 7 = 9, rồi 3 + 6 = 9, rồi '
         '4 + 5 = 9.',
         'Vì sao cặp nào cũng bằng nhau',
         'Mỗi lần lùi vào trong, số bên trái tăng một còn số bên phải giảm một. Một '
         'bên đưa, một bên nhận, nên tổng của cặp giữ nguyên.',
         'Đếm số cặp rồi cộng dồn',
         'Tám số ghép vừa khít thành bốn cặp, mỗi cặp chín: 9 + 9 + 9 + 9 = 36.',
         'Đáp số: 36.',
         'Tám số là số lượng chẵn nên ghép vừa khít, không bạn nào lẻ loi.'],
        ['Có bạn ghép cặp xong rồi ghi luôn đáp số là 9, vì cặp nào cũng bằng 9.',
         'Gợi ý 1: Số 9 là tổng của MỘT cặp hay của cả dãy?',
         'Gợi ý 2: Cả dãy có mấy cặp như thế? Phải làm gì với mấy cặp ấy nữa?',
         'Chữa: chín mới là tổng một cặp. Có bốn cặp nên phải cộng dồn: '
         '9 + 9 + 9 + 9 = 36.'],
        ['Xếp tám que tính thành hàng rồi cho con lấy hai đầu vào giữa từng cặp — bé '
         'thấy ngay vì sao cặp nào cũng bằng nhau.',
         'Bố mẹ hỏi: "Chín là tổng một cặp hay tổng cả dãy?"'],
    ),
    [
        lt(1, 1, 'Tính 1 + 8.', 'Lấy 1 + 8 = 9.'),
        lt(2, 1, 'Trong dãy 1, 2, 3, 4, 5, 6, 7, 8 — ghép số đầu với số cuối được '
                 'tổng bằng mấy?',
           'Số đầu là 1, số cuối là 8, mà 1 + 8 = 9.'),
        lt(3, 1, 'Dãy 1 đến 8 có tám số. Ghép cặp đầu với cuối thì được mấy cặp?',
           'Tám số ghép vừa khít thành 4 cặp.'),
        lt(4, 2, 'Tính nhanh tổng 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8.',
           'Bốn cặp, mỗi cặp chín. Cộng dồn: 9 + 9 + 9 + 9 = 36.'),
        lt(5, 2, 'Tính nhanh tổng 1 + 2 + 3 + 4 + 5 + 6.',
           'Ba cặp, mỗi cặp bảy. Cộng dồn: 7 + 7 + 7 = 21.'),
        lt(6, 2, 'Vì sao ghép cặp đầu với cuối thì cặp nào cũng bằng nhau?',
           'Vì lùi vào trong thì bên trái tăng một mà bên phải giảm một.'),
        lt(7, 3, 'Tính nhanh tổng 2 + 4 + 6 + 8 + 10 + 12. Cho biết mỗi cặp bằng bao '
                 'nhiêu và tổng bằng bao nhiêu.',
           'Mỗi cặp là 2 + 12 = 14. Có ba cặp, cộng dồn: 14 + 14 + 14 = 42.'),
        lt(8, 3, 'Tính nhanh tổng 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10. Cho biết số '
                 'cặp, mỗi cặp bằng bao nhiêu, và tổng bằng bao nhiêu.',
           'Mười số ghép thành 5 cặp, mỗi cặp là 1 + 10 = 11. Cộng dồn năm lần được '
           '55.'),
    ] + [
        q_tf(1, 'Ghép cặp đầu với cuối thì mọi cặp đều có tổng bằng nhau.', True,
             'Đúng — bên trái tăng bao nhiêu thì bên phải giảm bấy nhiêu.'),
        q_mcq(2, 'Tổng 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 bằng bao nhiêu?',
              ['36', '32', '40', '28'], '36', 'Bốn cặp, mỗi cặp chín.'),
        q_mcq(3, 'Dãy 1 đến 8 ghép được mấy cặp?', ['4', '8', '3', '5'], '4',
              'Tám số chia thành từng đôi.'),
        q_tf(4, 'Mỗi lần lùi vào trong, số bên trái tăng một và số bên phải giảm một.',
             True, 'Đúng — nên tổng của cặp không đổi.'),
        q_tf(5, 'Ghép cặp xong là có đáp số luôn, khỏi cộng dồn.', False,
             'Sai. Đó mới là tổng một cặp, còn phải cộng dồn tất cả các cặp.'),
    ],
)

# ═══ ④ B49 · MỘT BẠN ĐỨNG GIỮA ═══
B49 = bai(
    49, 'DÃY LẺ SỐ THÌ CÓ MỘT BẠN ĐỨNG GIỮA',
    'SỐ 7.1d — Ghép cặp đầu cuối khi dãy có số lượng lẻ.',
    video(
        ['Đếm được dãy có số lượng chẵn hay lẻ.',
         'Nhận ra số đứng giữa khi dãy có số lượng lẻ.',
         'Cộng dồn các cặp rồi cộng thêm số đứng giữa.'],
        ['Đề bài: Tính nhanh tổng 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9.',
         'Ghép cặp đầu với cuối như bài trước',
         'Cặp ngoài cùng là 1 + 9 = 10. Lùi vào: 2 + 8 = 10, rồi 3 + 7 = 10, rồi '
         '4 + 6 = 10.',
         'Đếm xem đã dùng hết số chưa',
         'Bốn cặp mới dùng hết tám số, mà dãy có chín số. Số 5 đứng chính giữa, không '
         'ai ghép cùng.',
         'Cộng dồn rồi cộng thêm bạn đứng giữa',
         'Bốn cặp mười là 10 + 10 + 10 + 10 = 40. Cộng thêm số đứng giữa: 40 + 5 = 45.',
         'Đáp số: 45.',
         'Dãy có số lượng lẻ thì luôn còn đúng một số đứng giữa — nhớ cộng nó vào.'],
        ['Có bạn tính tổng từ 1 đến 9 rồi ghi 40, vì ghép được bốn cặp mười.',
         'Gợi ý 1: Bốn cặp thì dùng hết mấy số? Dãy có mấy số?',
         'Gợi ý 2: Có một số không được ghép với ai. Số ấy là số nào?',
         'Chữa: bốn cặp mới dùng tám số, còn số 5 đứng giữa chưa được cộng. Tổng '
         'đúng là 45.'],
        ['Xếp chín viên kẹo thành hàng rồi cho con nhặt từ hai đầu vào — tới lúc chỉ '
         'còn một viên ở giữa thì bé hiểu ngay.',
         'Bố mẹ hỏi: "Ghép hết chưa, còn ai lẻ loi không?"'],
    ),
    [
        lt(1, 1, 'Dãy 1 đến 9 có bao nhiêu số?', 'Đếm từ 1 tới 9 được 9 số.'),
        lt(2, 1, 'Số lượng số của dãy 1 đến 9 là chẵn hay lẻ?',
           'Dãy có chín số, mà 9 tận cùng là 9 nên là số lẻ.'),
        lt(3, 1, 'Trong dãy 1 đến 9, số nào đứng chính giữa?',
           'Có bốn số đứng trước và bốn số đứng sau, nên số 5 đứng giữa.'),
        lt(4, 2, 'Dãy 1 đến 9 ghép được mấy cặp đầu cuối?',
           'Tám số ghép thành 4 cặp, còn một số đứng giữa.'),
        lt(5, 2, 'Tính nhanh tổng 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9.',
           'Bốn cặp mười là 10 + 10 + 10 + 10 = 40, cộng thêm số 5 đứng giữa được 45.'),
        lt(6, 2, 'Tính nhanh tổng 1 + 2 + 3 + 4 + 5. Cho biết số đứng giữa và tổng.',
           'Hai cặp sáu là 6 + 6 = 12, cộng thêm số 3 đứng giữa được 15.'),
        lt(7, 3, 'Tính nhanh tổng 2 + 3 + 4 + 5 + 6 + 7 + 8. Cho biết số đứng giữa và '
                 'tổng.',
           'Ba cặp mười là 10 + 10 + 10 = 30, cộng thêm số 5 đứng giữa được 35.'),
        lt(8, 3, 'Có bạn tính tổng từ 1 đến 9 rồi ghi 40. Cho biết bạn ấy quên điều gì '
                 'và tổng đúng là bao nhiêu.',
           'Bốn cặp mười mới được 40, bạn ấy quên cộng số đứng giữa. Tổng đúng là 45.'),
    ] + [
        q_tf(1, 'Dãy có số lượng lẻ thì còn một số đứng giữa không ghép được với ai.',
             True, 'Đúng — và phải cộng nó vào.'),
        q_mcq(2, 'Tổng các số từ 1 đến 9 bằng bao nhiêu?', ['45', '40', '50', '36'],
              '45', 'Bốn cặp mười, cộng thêm số đứng giữa.'),
        q_mcq(3, 'Trong dãy 1 đến 9, số nào đứng chính giữa?', ['5', '4', '9', '1'],
              '5', 'Bốn số đứng trước, bốn số đứng sau.'),
        q_tf(4, 'Dãy 1 đến 9 ghép được đúng bốn cặp và dùng hết số.', False,
             'Sai. Bốn cặp mới dùng tám số, còn số 5 đứng giữa.'),
        q_tf(5, 'Ghép cặp xong thì phải đếm lại xem đã dùng hết số chưa.', True,
             'Đúng — đó là chỗ hay quên nhất.'),
    ],
)

# ═══ ⑤ B14 · CHO KẾT QUẢ CHẠY NGƯỢC ═══
B14 = bai(
    14, 'CHO KẾT QUẢ CHẠY NGƯỢC — CỘNG VÀ TRỪ',
    'SỐ 7.2a — Tìm thành phần chưa biết của phép cộng và phép trừ.',
    video(
        ['Tìm được số trong ô trống của phép cộng và phép trừ.',
         'Biết cộng và trừ là đôi máy ngược chiều nhau.',
         'Luôn thử lại trước khi chốt đáp số.'],
        ['Đề bài: Tìm số thích hợp điền vào ô trống: ô trống cộng 5 bằng 12.',
         'Máy chạy xuôi thế nào',
         'Số cần tìm chui vào máy cộng 5 rồi chạy ra thành 12.',
         'Cho kết quả chạy ngược',
         'Máy ngược của máy cộng 5 là máy trừ 5. Cho 12 chạy ngược: 12 − 5 = 7.',
         'Thử lại trước khi chốt',
         'Thay 7 vào ô trống rồi tính xuôi: 7 + 5 = 12, khớp đúng đề bài.',
         'Đáp số: số cần tìm là 7.',
         'Cộng và trừ là đôi máy ngược chiều — một máy làm gì thì máy kia gỡ ra.'],
        ['Với bài ô trống trừ 4 bằng 9, có bạn giải là thấy dấu trừ thì cứ trừ, lấy '
         '9 − 4 = 5.',
         'Gợi ý 1: Thử lại giúp bạn ấy xem 5 − 4 có bằng 9 không.',
         'Gợi ý 2: Số cần tìm bị máy trừ 4 lấy bớt đi mà vẫn còn 9. Vậy lúc đầu nó '
         'phải to hơn hay bé hơn 9?',
         'Chữa: máy ngược của máy trừ 4 là máy cộng 4, nên số cần tìm là 9 + 4 = 13.'],
        ['Trò chơi ở nhà: bố mẹ nghĩ một số, cộng thêm mấy rồi đọc kết quả, con đoán '
         'ngược lại số ban đầu. Đổi vai cho con ra đề.',
         'Bố mẹ hỏi một câu mỗi lần: "Con thử lại chưa?"'],
    ),
    [
        lt(1, 1, 'Tính 12 − 5.', 'Lấy 12 − 5 = 7.'),
        lt(2, 1, 'Máy ngược của máy cộng 5 là máy nào?',
           'Cộng và trừ ngược chiều nhau, nên máy ngược là máy trừ 5.'),
        lt(3, 1, 'Tìm số trong ô trống: ô trống cộng 5 bằng 12.',
           'Cho 12 chạy ngược qua máy trừ 5: 12 − 5 = 7.'),
        lt(4, 2, 'Tìm số trong ô trống: ô trống cộng 8 bằng 20.',
           'Cho 20 chạy ngược qua máy trừ 8: 20 − 8 = 12.'),
        lt(5, 2, 'Tìm số trong ô trống: ô trống trừ 4 bằng 9.',
           'Máy ngược của máy trừ 4 là máy cộng 4, nên số cần tìm là 9 + 4 = 13.'),
        lt(6, 2, 'Tìm số trong ô trống rồi thử lại: ô trống cộng 7 bằng 15.',
           'Cho 15 chạy ngược: 15 − 7 = 8. Thử lại xuôi: 8 + 7 = 15.'),
        lt(7, 3, 'Có bạn giải bài ô trống trừ 4 bằng 9 rồi ghi số cần tìm là 5. Cho '
                 'biết bạn ấy sai ở đâu và số đúng là bao nhiêu.',
           'Thử lại thì 5 − 4 = 1 chứ không ra 9. Bạn ấy trừ tiếp thay vì cho chạy '
           'ngược. Số đúng là 9 + 4 = 13.'),
        lt(8, 3, 'Một số cộng 9 thì được 21. Cho biết số ấy là số nào, rồi tính số ấy '
                 'cộng thêm 4 nữa thì được bao nhiêu.',
           'Cho 21 chạy ngược: 21 − 9 = 12. Rồi 12 + 4 = 16.'),
    ] + [
        q_tf(1, 'Cộng và trừ là đôi máy ngược chiều nhau.', True,
             'Đúng — một máy làm gì thì máy kia gỡ ra.'),
        q_mcq(2, 'Ô trống cộng 5 bằng 12. Số trong ô trống là mấy?',
              ['7', '17', '5', '12'], '7', 'Cho kết quả chạy ngược qua máy trừ 5.'),
        q_mcq(3, 'Ô trống trừ 4 bằng 9. Số trong ô trống là mấy?',
              ['13', '5', '36', '9'], '13', 'Máy ngược của máy trừ là máy cộng.'),
        q_tf(4, 'Tìm xong số trong ô trống thì nên thử lại một lần.', True,
             'Đúng — thử lại là bước cuối bắt buộc.'),
        q_tf(5, 'Bài ô trống trừ 4 bằng 9 thì lấy 9 trừ 4 là ra.', False,
             'Sai. Phải cho 9 chạy ngược qua máy cộng 4, được 13.'),
    ],
)

# ═══ ⑥ B50 · MÁY NHÂN VÀ MÁY CHIA ═══
B50 = bai(
    50, 'MÁY NHÂN VÀ MÁY CHIA NGƯỢC NHAU',
    'SỐ 7.2b — Tìm thành phần chưa biết của phép nhân và phép chia.',
    video(
        ['Tìm được số trong ô trống của phép nhân và phép chia.',
         'Biết nhân và chia là đôi máy ngược chiều nhau.',
         'Thử lại bằng chính phép tính của đề bài.'],
        ['Đề bài: Tìm số thích hợp điền vào ô trống: ô trống nhân 4 bằng 28.',
         'Máy nhân cũng có bạn ngược của nó',
         'Máy ngược của máy nhân 4 là máy chia 4.',
         'Cho kết quả chạy ngược',
         'Cho 28 chạy ngược qua máy chia 4: 28 : 4 = 7.',
         'Thử lại trước khi chốt',
         'Thay 7 vào ô trống rồi tính xuôi: 7 × 4 = 28, khớp đúng đề bài.',
         'Đáp số: số cần tìm là 7.',
         'Nhân và chia là đôi máy ngược chiều, y như cộng và trừ ở bài trước.'],
        ['Với bài ô trống chia 3 bằng 6, có bạn giải là thấy dấu chia thì cứ chia, lấy '
         '6 : 3 = 2.',
         'Gợi ý 1: Thử lại giúp bạn ấy xem 2 chia cho 3 có ra 6 không.',
         'Gợi ý 2: Số cần tìm bị máy chia 3 làm nhỏ đi mà vẫn còn 6. Vậy lúc đầu nó '
         'phải to hơn hay bé hơn 6?',
         'Chữa: máy ngược của máy chia 3 là máy nhân 3, nên số cần tìm là 6 × 3 = 18.'],
        ['Chia kẹo thật rồi hỏi ngược: "Mỗi bạn được 4 viên, có 5 bạn, vậy lúc đầu '
         'gói có mấy viên?" — đó chính là cho kết quả chạy ngược.',
         'Bố mẹ hỏi: "Máy ngược của máy này là máy gì?"'],
    ),
    [
        lt(1, 1, 'Tính 28 : 4.', 'Lấy 28 : 4 = 7.'),
        lt(2, 1, 'Máy ngược của máy nhân 4 là máy nào?',
           'Nhân và chia ngược chiều nhau, nên máy ngược là máy chia 4.'),
        lt(3, 1, 'Tìm số trong ô trống: ô trống nhân 4 bằng 28.',
           'Cho 28 chạy ngược qua máy chia 4: 28 : 4 = 7.'),
        lt(4, 2, 'Tìm số trong ô trống: ô trống nhân 5 bằng 45.',
           'Cho 45 chạy ngược qua máy chia 5: 45 : 5 = 9.'),
        lt(5, 2, 'Tìm số trong ô trống: ô trống chia 3 bằng 6.',
           'Máy ngược của máy chia 3 là máy nhân 3, nên số cần tìm là 6 × 3 = 18.'),
        lt(6, 2, 'Tìm số trong ô trống rồi thử lại: ô trống nhân 2 bằng 16.',
           'Cho 16 chạy ngược: 16 : 2 = 8. Thử lại xuôi: 8 × 2 = 16.'),
        lt(7, 3, 'Có bạn giải bài ô trống chia 3 bằng 6 rồi ghi số cần tìm là 2. Cho '
                 'biết bạn ấy sai ở đâu và số đúng là bao nhiêu.',
           'Thử lại thì 2 chia cho 3 không ra 6. Bạn ấy chia tiếp thay vì cho chạy '
           'ngược. Số đúng là 6 × 3 = 18.'),
        lt(8, 3, 'Một số nhân 5 thì được 40. Cho biết số ấy là số nào, rồi tính số ấy '
                 'nhân 3 thì được bao nhiêu.',
           'Cho 40 chạy ngược: 40 : 5 = 8. Rồi 8 × 3 = 24.'),
    ] + [
        q_tf(1, 'Nhân và chia là đôi máy ngược chiều nhau.', True,
             'Đúng — cùng luật với cộng và trừ.'),
        q_mcq(2, 'Ô trống nhân 4 bằng 28. Số trong ô trống là mấy?',
              ['7', '24', '32', '4'], '7', 'Cho kết quả chạy ngược qua máy chia 4.'),
        q_mcq(3, 'Ô trống chia 3 bằng 6. Số trong ô trống là mấy?',
              ['18', '2', '9', '3'], '18', 'Máy ngược của máy chia là máy nhân.'),
        q_tf(4, 'Bài ô trống chia 3 bằng 6 thì lấy 6 chia 3 là ra.', False,
             'Sai. Phải cho 6 chạy ngược qua máy nhân 3, được 18.'),
        q_tf(5, 'Thử lại là bước cuối bắt buộc.', True,
             'Đúng — chưa thử lại thì chưa được hô đáp án.'),
    ],
)

# ═══ ⑦ B51 · SỐ BỊ LẤY ĐI ═══
B51 = bai(
    51, 'KHI SỐ CẦN TÌM BỊ LẤY ĐI — 14 TRỪ Ô TRỐNG BẰNG 6',
    'SỐ 7.2c — Tìm số trừ: ca ô trống đứng SAU dấu trừ.',
    video(
        ['Nhận ra ca ô trống đứng sau dấu trừ.',
         'Hiểu số cần tìm chính là phần bị lấy đi.',
         'Lấy số ban đầu trừ phần còn lại để tìm nó.'],
        ['Đề bài: Tìm số thích hợp điền vào ô trống: 14 trừ ô trống bằng 6.',
         'Ca này khác hai bài trước',
         'Số cần tìm không chui vào máy nào cả. Nó chính là phần bị lấy đi khỏi 14.',
         'Hỏi lại cho dễ hiểu',
         'Câu hỏi thật ra là: từ 14 lấy đi bao nhiêu thì còn 6?',
         'Lấy số ban đầu trừ phần còn lại',
         'Phần bị lấy đi là 14 − 6 = 8.',
         'Thử lại trước khi chốt',
         'Thay 8 vào ô trống rồi tính xuôi: 14 − 8 = 6, khớp đúng đề bài.',
         'Đáp số: số cần tìm là 8.',
         'Ô trống đứng SAU dấu trừ thì cách làm khác hẳn ô trống đứng trước.'],
        ['Có bạn giải bài 14 trừ ô trống bằng 6 rồi ghi số cần tìm là 20, vì quen tay '
         'cho kết quả chạy ngược qua máy cộng.',
         'Gợi ý 1: Thử lại giúp bạn ấy xem 14 − 20 có làm được không.',
         'Gợi ý 2: Ô trống đứng trước hay đứng sau dấu trừ? Nó là số bị lấy đi hay số '
         'ban đầu?',
         'Chữa: ô trống đứng sau dấu trừ nên nó là phần bị lấy đi. Lấy 14 − 6 = 8.'],
        ['Cầm 14 viên kẹo rồi giấu đi một nắm, đếm số còn lại là 6, hỏi con vừa giấu '
         'mấy viên — đúng cái ca của bài này.',
         'Bố mẹ hỏi: "Ô trống đứng trước hay sau dấu trừ?"'],
    ),
    [
        lt(1, 1, 'Tính 14 − 6.', 'Lấy 14 − 6 = 8.'),
        lt(2, 1, 'Từ 14 lấy đi bao nhiêu thì còn lại 6?',
           'Phần bị lấy đi là 14 − 6 = 8.'),
        lt(3, 1, 'Tìm số trong ô trống: 14 trừ ô trống bằng 6.',
           'Ô trống là phần bị lấy đi, nên lấy 14 − 6 = 8.'),
        lt(4, 2, 'Tìm số trong ô trống: 20 trừ ô trống bằng 12.',
           'Phần bị lấy đi là 20 − 12 = 8.'),
        lt(5, 2, 'Tìm số trong ô trống: 30 trừ ô trống bằng 11.',
           'Phần bị lấy đi là 30 − 11 = 19.'),
        lt(6, 2, 'Hai bài "ô trống trừ 6 bằng 14" và "14 trừ ô trống bằng 6" có cùng '
                 'đáp số không?',
           'Bài đầu ra 20 còn bài sau ra 8, nên hai đáp số khác hẳn nhau.'),
        lt(7, 3, 'Tìm số trong ô trống rồi thử lại: 25 trừ ô trống bằng 9.',
           'Phần bị lấy đi là 25 − 9 = 16. Thử lại xuôi: 25 − 16 = 9.'),
        lt(8, 3, 'Có bạn giải bài 14 trừ ô trống bằng 6 rồi ghi số cần tìm là 20. Cho '
                 'biết bạn ấy sai ở đâu và số đúng là bao nhiêu.',
           'Bạn ấy cộng 14 với 6 vì quen tay cho chạy ngược. Ô trống đứng sau dấu trừ '
           'nên phải lấy 14 − 6 = 8.'),
    ] + [
        q_tf(1, 'Ô trống đứng sau dấu trừ thì lấy số ban đầu trừ đi kết quả.', True,
             'Đúng — nó chính là phần bị lấy đi.'),
        q_mcq(2, 'Bài 14 trừ ô trống bằng 6. Số trong ô trống là mấy?',
              ['8', '20', '6', '14'], '8', 'Lấy số ban đầu trừ phần còn lại.'),
        q_mcq(3, 'Bài ô trống trừ 6 bằng 14. Số trong ô trống là mấy?',
              ['20', '8', '14', '6'], '20', 'Ca này thì cho kết quả chạy ngược.'),
        q_tf(4, 'Hai bài "ô trống trừ 6 bằng 14" và "14 trừ ô trống bằng 6" có cùng '
                'đáp số.', False, 'Sai. Một bài ra 20, bài kia ra 8.'),
        q_tf(5, 'Phải nhìn xem ô trống đứng trước hay sau dấu trừ rồi mới chọn cách '
                'làm.', True, 'Đúng — hai chỗ đứng là hai cách làm khác nhau.'),
    ],
)

# ═══ ⑧ B15 · CHIA THEO VÒNG ═══
B15 = bai(
    15, 'CHIA THEO VÒNG — MỖI BẠN MẤY VIÊN, THỪA MẤY VIÊN',
    'SỐ 6.3a — Phép chia có dư ở mức thao tác: chia theo vòng.',
    video(
        ['Chia một nhóm đồ vật thành các phần bằng nhau.',
         'Lần theo bảng nhân để tìm trạm dừng gần nhất mà chưa vượt.',
         'Nói rõ mỗi bạn được mấy và còn thừa mấy.'],
        ['Đề bài: Có 20 viên bi chia đều cho 6 bạn. Hỏi mỗi bạn được mấy viên và còn '
         'thừa mấy viên?',
         'Chia theo vòng cho công bằng',
         'Mỗi vòng phát cho mỗi bạn đúng một viên, tức là mỗi vòng tốn 6 viên.',
         'Lần theo bảng nhân 6 tìm trạm dừng',
         'Trạm 6 × 3 = 18, chưa vượt 20. Trạm sau là 6 × 4 = 24, vượt mất rồi. Vậy '
         'dừng ở ba vòng.',
         'Đếm số viên còn lại trong tay',
         'Đã phát đi 18 viên, còn lại 20 − 18 = 2 viên.',
         'Đáp số: mỗi bạn 3 viên, còn thừa 2 viên.',
         'Còn 2 viên mà có tới 6 bạn nên không phát thêm vòng nào được nữa.'],
        ['Có bạn chia 20 viên cho 6 bạn rồi ghi mỗi bạn 3 viên, mà quên không nói còn '
         'thừa mấy viên.',
         'Gợi ý 1: Ba vòng đã phát đi bao nhiêu viên rồi?',
         'Gợi ý 2: Gói có 20 viên, đã phát 18 viên. Trong tay còn lại mấy viên?',
         'Chữa: bài chia còn thừa phải nói ĐỦ HAI SỐ — mỗi bạn 3 viên, và còn thừa '
         '20 − 18 = 2 viên.'],
        ['Chia thật một nắm kẹo cho cả nhà theo vòng, mỗi vòng mỗi người một viên — '
         'con sẽ thấy chỗ thừa hiện ra rất tự nhiên.',
         'Bố mẹ hỏi: "Con đã nói đủ hai số chưa — mỗi bạn mấy, và thừa mấy?"'],
    ),
    [
        lt(1, 1, 'Tính 6 × 3.', 'Lấy 6 × 3 = 18.'),
        lt(2, 1, 'Tính 20 − 18.', 'Lấy 20 − 18 = 2.'),
        lt(3, 1, 'Chia 20 viên bi cho 6 bạn thì mỗi bạn được mấy viên?',
           'Lần theo bảng nhân 6: trạm 6 × 3 = 18 chưa vượt 20, nên mỗi bạn 3 viên.'),
        lt(4, 2, 'Chia 20 viên bi cho 6 bạn thì còn thừa mấy viên?',
           'Đã phát 18 viên, còn lại 20 − 18 = 2 viên.'),
        lt(5, 2, 'Chia 17 viên kẹo cho 3 bạn. Mỗi bạn được mấy viên và thừa mấy viên?',
           'Lần theo bảng nhân 3: trạm 3 × 5 = 15 chưa vượt 17. Mỗi bạn 5 viên, còn '
           '17 − 15 = 2 viên.'),
        lt(6, 2, 'Chia 22 viên cho 4 bạn. Mỗi bạn được mấy viên và thừa mấy viên?',
           'Lần theo bảng nhân 4: trạm 4 × 5 = 20 chưa vượt 22. Mỗi bạn 5 viên, còn '
           '22 − 20 = 2 viên.'),
        lt(7, 3, 'Chia 29 viên cho 5 bạn. Mỗi bạn được mấy viên và thừa mấy viên?',
           'Lần theo bảng nhân 5: trạm 5 × 5 = 25 chưa vượt 29. Mỗi bạn 5 viên, còn '
           '29 − 25 = 4 viên.'),
        lt(8, 3, 'Chia 31 viên cho 7 bạn. Cho biết mỗi bạn mấy viên, đã phát đi tất cả '
                 'bao nhiêu viên, và còn thừa mấy viên.',
           'Lần theo bảng nhân 7: trạm 7 × 4 = 28 chưa vượt 31. Mỗi bạn 4 viên, đã '
           'phát 28 viên, còn 31 − 28 = 3 viên.'),
    ] + [
        q_tf(1, 'Chia theo vòng thì mỗi vòng phát cho mỗi bạn đúng một viên.', True,
             'Đúng — chia thế mới công bằng.'),
        q_mcq(2, 'Chia 20 viên cho 6 bạn thì mỗi bạn được mấy viên?',
              ['3', '4', '2', '5'], '3', 'Trạm dừng là ba vòng.'),
        q_mcq(3, 'Chia 20 viên cho 6 bạn thì thừa mấy viên?', ['2', '4', '0', '6'],
              '2', 'Đã phát 18 viên trong tổng số 20.'),
        q_tf(4, 'Chia 17 viên cho 3 bạn thì mỗi bạn được 5 viên và thừa 2 viên.', True,
             'Đúng — trạm dừng là 15.'),
        q_tf(5, 'Bài chia còn thừa chỉ cần nói mỗi bạn được mấy viên là đủ.', False,
             'Sai. Phải nói đủ hai số: mỗi bạn mấy, và còn thừa mấy.'),
    ],
)

# ═══ ⑨ B52 · LUẬT VÀNG ═══
B52 = bai(
    52, 'LUẬT VÀNG — SỐ THỪA PHẢI BÉ HƠN SỐ BẠN',
    'SỐ 6.3b — Luật của số dư: dư luôn nhỏ hơn số chia.',
    video(
        ['Biết số thừa luôn phải bé hơn số bạn được chia.',
         'Nhận ra cách chia sai khi số thừa còn quá lớn.',
         'Chia lại cho đúng bằng cách phát thêm vòng.'],
        ['Đề bài: Có bạn chia 17 viên kẹo cho 3 bạn rồi bảo mỗi bạn 4 viên, thừa 5 '
         'viên. Chỗ ấy vô lý ở đâu?',
         'Soi luật vàng trước đã',
         'Số thừa là 5, mà chỉ có 3 bạn. Số thừa đang lớn hơn số bạn.',
         'Vì sao thế là vô lý',
         'Còn 5 viên trong tay thì phát thêm được cả một vòng nữa, mỗi bạn một viên '
         'hết 3 viên.',
         'Chia lại cho đúng',
         'Phát thêm một vòng thì mỗi bạn thành 5 viên, đã phát 15 viên, còn '
         '17 − 15 = 2 viên.',
         'Đáp số: mỗi bạn 5 viên, thừa 2 viên.',
         'Số thừa 2 đã bé hơn số bạn là 3, nên lần này không chia thêm được nữa.'],
        ['Có bạn chia cho 6 bạn rồi bảo thừa đúng 6 viên, và cho rằng thế là hợp luật '
         'vì thừa không lớn hơn số bạn.',
         'Gợi ý 1: Còn 6 viên mà có 6 bạn thì phát thêm được vòng nào nữa không?',
         'Gợi ý 2: Luật vàng nói thừa phải BÉ HƠN số bạn, hay bé hơn hoặc bằng?',
         'Chữa: thừa bằng đúng số bạn thì vẫn phát thêm được một vòng, nên chưa chia '
         'xong. Luật vàng đòi thừa phải bé hơn hẳn.'],
        ['Sau mỗi lần chia kẹo ở nhà, hỏi con một câu: "Chỗ thừa này còn chia thêm '
         'được không?" Trả lời được là hiểu luật vàng.',
         'Bố mẹ hỏi: "Thừa mấy, có mấy bạn, số nào lớn hơn?"'],
    ),
    [
        lt(1, 1, 'Chia cho 3 bạn thì số thừa nhiều nhất có thể là mấy?',
           'Số thừa phải bé hơn 3, nên nhiều nhất là 2.'),
        lt(2, 1, 'Chia 17 viên cho 3 bạn mà bảo thừa 5 viên thì đúng hay sai?',
           'Số thừa 5 đang lớn hơn số bạn là 3 nên vô lý.'),
        lt(3, 1, 'Chia cho 4 bạn thì số thừa nhiều nhất có thể là mấy?',
           'Số thừa phải bé hơn 4, nên nhiều nhất là 3.'),
        lt(4, 2, 'Chia 17 viên cho 3 bạn thì đúng ra mỗi bạn mấy viên và thừa mấy '
                 'viên?',
           'Bảng nhân 3 có trạm 3 × 5 = 15 chưa vượt 17. Mỗi bạn 5 viên, còn '
           '17 − 15 = 2 viên.'),
        lt(5, 2, 'Chia cho 6 bạn mà bảo thừa 6 viên thì sai ở đâu?',
           'Còn 6 viên thì phát thêm được một vòng nữa, vì thừa phải bé hơn số bạn.'),
        lt(6, 2, 'Chia một gói kẹo cho 5 bạn, mỗi bạn được 4 viên và thừa 7 viên. Cách '
                 'chia ấy đúng hay sai?',
           'Số thừa 7 lớn hơn số bạn là 5 nên còn phát thêm được một vòng nữa.'),
        lt(7, 3, 'Chia một gói cho 5 bạn, mỗi bạn 4 viên và thừa 7 viên. Cho biết cả '
                 'gói có bao nhiêu viên, rồi chia lại cho đúng.',
           'Đã phát 5 × 4 = 20 viên, cộng 7 viên thừa nên cả gói có 27 viên. Bảng '
           'nhân 5 có trạm 5 × 5 = 25 chưa vượt, nên mỗi bạn 5 viên và còn '
           '27 − 25 = 2 viên.'),
        lt(8, 3, 'Chia cho 8 bạn thì số thừa lớn nhất có thể là mấy, và bé nhất có thể '
                 'là mấy?',
           'Số thừa phải bé hơn 8 nên lớn nhất là 7. Chia vừa khít thì thừa 0.'),
    ] + [
        q_tf(1, 'Số thừa luôn phải bé hơn số bạn được chia.', True,
             'Đúng — đó là luật vàng của phép chia còn thừa.'),
        q_tf(2, 'Chia 17 viên cho 3 bạn thì có thể thừa 5 viên.', False,
             'Sai. Còn 5 viên thì phát thêm được một vòng nữa.'),
        q_mcq(3, 'Chia cho 4 bạn thì số thừa nhiều nhất là mấy?',
              ['3', '4', '5', '0'], '3', 'Thừa phải bé hơn số bạn.'),
        q_mcq(4, 'Chia 17 viên cho 3 bạn thì thừa mấy viên?', ['2', '5', '1', '3'],
              '2', 'Trạm dừng là 15.'),
        q_tf(5, 'Thừa bằng đúng số bạn thì vẫn hợp luật.', False,
             'Sai. Thừa bằng số bạn thì còn phát thêm được một vòng.'),
    ],
)

# ═══ ⑩ B53 · CHIA HẾT HAY CÒN THỪA ═══
B53 = bai(
    53, 'CHIA HẾT HAY CÒN THỪA — BẢNG NHÂN LÀ DANH SÁCH CHIA ĐẸP',
    'SỐ 6.3c — Phân biệt chia hết và chia còn thừa qua bảng nhân.',
    video(
        ['Phân biệt chia hết và chia còn thừa.',
         'Dùng bảng nhân để biết trước một số có chia hết hay không.',
         'Tìm trạm dừng gần nhất khi số không có trong bảng.'],
        ['Đề bài: Chia 15 viên kẹo cho 3 bạn có vừa khít không? Còn 17 viên thì sao?',
         'Soi bảng nhân 3',
         'Bảng nhân 3 chạy 3, 6, 9, 12, 15, 18. Số 15 có mặt trong bảng.',
         'Số nằm trong bảng thì chia vừa khít',
         'Chia 15 viên cho 3 bạn được đúng năm vòng, thừa 0 viên. Đó là chia hết.',
         'Còn số không có trong bảng thì sao',
         'Số 17 không có trong bảng nhân 3. Trạm dừng gần nhất mà chưa vượt là 15, '
         'nên còn 17 − 15 = 2 viên.',
         'Đáp số: 15 chia hết cho 3, còn 17 thì thừa 2 viên.',
         'Bảng nhân chính là danh sách những số chia vừa khít — thuộc bảng là biết '
         'trước.'],
        ['Có bạn thấy 17 nằm giữa 15 và 18 của bảng nhân 3 nên bảo 17 cũng chia hết '
         'cho 3.',
         'Gợi ý 1: Bảng nhân 3 có đọc tới số 17 bao giờ không?',
         'Gợi ý 2: Nằm giữa hai số của bảng thì có nghĩa là thuộc bảng không?',
         'Chữa: bảng nhảy thẳng từ 15 sang 18, bỏ qua 17. Nằm giữa hai số của bảng '
         'không có nghĩa là thuộc bảng, nên 17 chia 3 còn thừa 2.'],
        ['Đố con nhanh: "Số này chia hết cho 5 không?" — bé chỉ cần nhớ bảng nhân là '
         'trả lời được, không phải chia thử.',
         'Bố mẹ hỏi: "Số này có trong bảng nhân ấy không?"'],
    ),
    [
        lt(1, 1, 'Số 15 có trong bảng nhân 3 không?',
           'Bảng nhân 3 chạy 3, 6, 9, 12, 15 nên số ấy có trong bảng.'),
        lt(2, 1, 'Chia 15 viên cho 3 bạn thì thừa mấy viên?',
           'Chia vừa khít thành năm vòng nên thừa 0 viên.'),
        lt(3, 1, 'Số 17 có trong bảng nhân 3 không?',
           'Bảng nhân 3 nhảy thẳng từ 15 sang 18, bỏ qua số ấy.'),
        lt(4, 2, 'Chia 17 viên cho 3 bạn thì thừa mấy viên?',
           'Trạm dừng gần nhất là 15, còn 17 − 15 = 2 viên.'),
        lt(5, 2, 'Trong hai số 24 và 25, số nào chia hết cho 4?',
           'Bảng nhân 4 có 24 mà không có 25.'),
        lt(6, 2, 'Chia 25 viên cho 4 bạn thì thừa mấy viên?',
           'Trạm dừng gần nhất là 24, còn 25 − 24 = 1 viên.'),
        lt(7, 3, 'Trong bốn số 18, 20, 21 và 23, số nào chia hết cho 5?',
           'Bảng nhân 5 chỉ có số đuôi 0 hoặc 5, trong bốn số ấy chỉ 20 hợp.'),
        lt(8, 3, 'Chia 34 viên cho 5 bạn. Cho biết chia hết hay còn thừa, mỗi bạn mấy '
                 'viên và thừa mấy viên.',
           'Số 34 không có trong bảng nhân 5 nên còn thừa. Trạm dừng gần nhất là '
           '5 × 6 = 30, nên mỗi bạn 6 viên và còn 34 − 30 = 4 viên.'),
    ] + [
        q_tf(1, 'Số nằm trong bảng nhân thì chia vừa khít, không thừa viên nào.', True,
             'Đúng — bảng nhân là danh sách các số chia đẹp.'),
        q_mcq(2, 'Chia 15 viên cho 3 bạn thì thừa mấy viên?', ['0', '2', '3', '5'],
              '0', 'Số 15 có trong bảng nhân 3.'),
        q_mcq(3, 'Chia 17 viên cho 3 bạn thì thừa mấy viên?', ['2', '1', '3', '0'],
              '2', 'Trạm dừng gần nhất là 15.'),
        q_tf(4, 'Số 25 chia hết cho 4.', False,
             'Sai. Bảng nhân 4 không có 25, chia còn thừa 1 viên.'),
        q_tf(5, 'Nằm giữa hai số của bảng nhân thì cũng coi như thuộc bảng.', False,
             'Sai. Bảng nhảy qua số ấy, nên chia vẫn còn thừa.'),
    ],
)

MOI = [B12, B48, B13, B49, B14, B50, B51, B15, B52, B53]

# Mỗi bài mới chèn ngay SAU bài đã nêu; đọc lần lượt từ trên xuống nên B51 phải
# đứng dưới dòng của B50, B53 dưới dòng của B52.
SAU = {
    'DL:KSN2.B48': 'DL:KSN2.B12',
    'DL:KSN2.B49': 'DL:KSN2.B13',
    'DL:KSN2.B50': 'DL:KSN2.B14',
    'DL:KSN2.B51': 'DL:KSN2.B50',
    'DL:KSN2.B52': 'DL:KSN2.B15',
    'DL:KSN2.B53': 'DL:KSN2.B52',
}

_CHAN_LE = ['chẵn', 'lẻ']


def _o(gt, chon=None, nhan=None):
    """Một ô nhập. Chuỗi thì BẮT BUỘC kèm nút bấm — luật ô nhập số 1 của lớp 2."""
    d = {'value': gt}
    if chon:
        d['options'] = list(chon)
    if nhan:
        d['label'] = nhan
    return d


O_NHAP_MOI = {
 # ① B12 · ghép đôi tròn chục
 'DL:KSN2.B12#C1': {'value': 10},
 'DL:KSN2.B12#C2': {'value': 2},
 'DL:KSN2.B12#C3': {'value': 30},
 'DL:KSN2.B12#C4': {'parts': [_o(30, nhan='cặp thứ nhất'),
                              _o(30, nhan='cặp thứ hai'),
                              _o(60, nhan='tổng')]},
 'DL:KSN2.B12#C5': {'value': 80},
 'DL:KSN2.B12#C6': {'parts': [_o('vì đổi chỗ thì tổng vẫn giữ nguyên',
                                 ['vì đổi chỗ thì tổng vẫn giữ nguyên',
                                  'vì làm thế cho nhanh tay',
                                  'vì cô giáo cho phép'], 'vì sao')]},
 'DL:KSN2.B12#C7': {'value': 100},
 'DL:KSN2.B12#C8': {'parts': [_o(8, nhan='22 bắt cặp với số nào'),
                              _o(60, nhan='tổng cả dãy')]},

 # ② B48 · ghép hai khay kẹo
 'DL:KSN2.B48#C1': {'value': 12},
 'DL:KSN2.B48#C2': {'value': 18},
 'DL:KSN2.B48#C3': {'value': 10},
 'DL:KSN2.B48#C4': {'value': 30},
 'DL:KSN2.B48#C5': {'value': 50},
 'DL:KSN2.B48#C6': {'parts': [_o(2, nhan='số hàng'),
                              _o(10, nhan='mỗi hàng mấy viên')]},
 'DL:KSN2.B48#C7': {'value': 40},
 'DL:KSN2.B48#C8': {'parts': [_o('không', CO_KHONG, 'ghép được không'),
                              _o(27, nhan='cả hai khay có mấy viên')]},

 # ③ B13 · ghép cặp đầu với cuối
 'DL:KSN2.B13#C1': {'value': 9},
 'DL:KSN2.B13#C2': {'value': 9},
 'DL:KSN2.B13#C3': {'value': 4},
 'DL:KSN2.B13#C4': {'value': 36},
 'DL:KSN2.B13#C5': {'value': 21},
 'DL:KSN2.B13#C6': {'parts': [_o('vì bên trái tăng một thì bên phải giảm một',
                                 ['vì bên trái tăng một thì bên phải giảm một',
                                  'vì các số đều bằng nhau',
                                  'vì dãy bắt đầu từ số một'], 'vì sao')]},
 'DL:KSN2.B13#C7': {'parts': [_o(14, nhan='mỗi cặp'), _o(42, nhan='tổng')]},
 'DL:KSN2.B13#C8': {'parts': [_o(5, nhan='số cặp'), _o(11, nhan='mỗi cặp'),
                              _o(55, nhan='tổng')]},

 # ④ B49 · một bạn đứng giữa
 'DL:KSN2.B49#C1': {'value': 9},
 'DL:KSN2.B49#C2': {'parts': [_o('lẻ', _CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B49#C3': {'value': 5},
 'DL:KSN2.B49#C4': {'value': 4},
 'DL:KSN2.B49#C5': {'value': 45},
 'DL:KSN2.B49#C6': {'parts': [_o(3, nhan='số đứng giữa'), _o(15, nhan='tổng')]},
 'DL:KSN2.B49#C7': {'parts': [_o(5, nhan='số đứng giữa'), _o(35, nhan='tổng')]},
 'DL:KSN2.B49#C8': {'parts': [_o('quên cộng số đứng giữa',
                                 ['quên cộng số đứng giữa', 'không quên gì cả'],
                                 'bạn ấy quên điều gì'),
                              _o(45, nhan='tổng đúng')]},

 # ⑤ B14 · cho kết quả chạy ngược
 'DL:KSN2.B14#C1': {'value': 7},
 'DL:KSN2.B14#C2': {'parts': [_o('máy trừ 5',
                                 ['máy trừ 5', 'máy cộng 5', 'máy nhân 5'],
                                 'máy ngược')]},
 'DL:KSN2.B14#C3': {'value': 7},
 'DL:KSN2.B14#C4': {'value': 12},
 'DL:KSN2.B14#C5': {'value': 13},
 'DL:KSN2.B14#C6': {'parts': [_o(8, nhan='số cần tìm'),
                              _o(15, nhan='thử lại được')]},
 'DL:KSN2.B14#C7': {'parts': [_o('trừ tiếp thay vì cho chạy ngược',
                                 ['trừ tiếp thay vì cho chạy ngược',
                                  'không sai gì cả'], 'bạn ấy sai ở đâu'),
                              _o(13, nhan='số đúng')]},
 'DL:KSN2.B14#C8': {'parts': [_o(12, nhan='số cần tìm'),
                              _o(16, nhan='cộng thêm 4 được')]},

 # ⑥ B50 · máy nhân và máy chia
 'DL:KSN2.B50#C1': {'value': 7},
 'DL:KSN2.B50#C2': {'parts': [_o('máy chia 4',
                                 ['máy chia 4', 'máy nhân 4', 'máy trừ 4'],
                                 'máy ngược')]},
 'DL:KSN2.B50#C3': {'value': 7},
 'DL:KSN2.B50#C4': {'value': 9},
 'DL:KSN2.B50#C5': {'value': 18},
 'DL:KSN2.B50#C6': {'parts': [_o(8, nhan='số cần tìm'),
                              _o(16, nhan='thử lại được')]},
 'DL:KSN2.B50#C7': {'parts': [_o('chia tiếp thay vì cho chạy ngược',
                                 ['chia tiếp thay vì cho chạy ngược',
                                  'không sai gì cả'], 'bạn ấy sai ở đâu'),
                              _o(18, nhan='số đúng')]},
 'DL:KSN2.B50#C8': {'parts': [_o(8, nhan='số cần tìm'),
                              _o(24, nhan='nhân 3 được')]},

 # ⑦ B51 · số bị lấy đi
 'DL:KSN2.B51#C1': {'value': 8},
 'DL:KSN2.B51#C2': {'value': 8},
 'DL:KSN2.B51#C3': {'value': 8},
 'DL:KSN2.B51#C4': {'value': 8},
 'DL:KSN2.B51#C5': {'value': 19},
 'DL:KSN2.B51#C6': {'parts': [_o('không', CO_KHONG, 'cùng đáp số không')]},
 'DL:KSN2.B51#C7': {'parts': [_o(16, nhan='số cần tìm'),
                              _o(9, nhan='thử lại được')]},
 'DL:KSN2.B51#C8': {'parts': [_o('cộng vào thay vì trừ đi',
                                 ['cộng vào thay vì trừ đi', 'không sai gì cả'],
                                 'bạn ấy sai ở đâu'),
                              _o(8, nhan='số đúng')]},

 # ⑧ B15 · chia theo vòng
 'DL:KSN2.B15#C1': {'value': 18},
 'DL:KSN2.B15#C2': {'value': 2},
 'DL:KSN2.B15#C3': {'value': 3},
 'DL:KSN2.B15#C4': {'value': 2},
 'DL:KSN2.B15#C5': {'parts': [_o(5, nhan='mỗi bạn'), _o(2, nhan='thừa')]},
 'DL:KSN2.B15#C6': {'parts': [_o(5, nhan='mỗi bạn'), _o(2, nhan='thừa')]},
 'DL:KSN2.B15#C7': {'parts': [_o(5, nhan='mỗi bạn'), _o(4, nhan='thừa')]},
 'DL:KSN2.B15#C8': {'parts': [_o(4, nhan='mỗi bạn'), _o(28, nhan='đã phát'),
                              _o(3, nhan='thừa')]},

 # ⑨ B52 · luật vàng
 'DL:KSN2.B52#C1': {'value': 2},
 'DL:KSN2.B52#C2': {'parts': [_o('sai', DUNG_SAI, 'đúng hay sai')]},
 'DL:KSN2.B52#C3': {'value': 3},
 'DL:KSN2.B52#C4': {'parts': [_o(5, nhan='mỗi bạn'), _o(2, nhan='thừa')]},
 'DL:KSN2.B52#C5': {'parts': [_o('còn 6 viên thì phát thêm được một vòng nữa',
                                 ['còn 6 viên thì phát thêm được một vòng nữa',
                                  'không sai gì cả'], 'sai ở đâu')]},
 'DL:KSN2.B52#C6': {'parts': [_o('sai', DUNG_SAI, 'đúng hay sai')]},
 'DL:KSN2.B52#C7': {'parts': [_o(27, nhan='cả gói có mấy viên'),
                              _o(5, nhan='mỗi bạn'), _o(2, nhan='thừa')]},
 'DL:KSN2.B52#C8': {'parts': [_o(7, nhan='thừa lớn nhất'),
                              _o(0, nhan='thừa bé nhất')]},

 # ⑩ B53 · chia hết hay còn thừa
 'DL:KSN2.B53#C1': {'parts': [_o('có', CO_KHONG, 'có trong bảng không')]},
 'DL:KSN2.B53#C2': {'value': 0},
 'DL:KSN2.B53#C3': {'parts': [_o('không', CO_KHONG, 'có trong bảng không')]},
 'DL:KSN2.B53#C4': {'value': 2},
 'DL:KSN2.B53#C5': {'parts': [_o('24', ['24', '25'], 'số chia hết cho 4')]},
 'DL:KSN2.B53#C6': {'value': 1},
 'DL:KSN2.B53#C7': {'parts': [_o('20', ['18', '20', '21', '23'],
                                 'số chia hết cho 5')]},
 'DL:KSN2.B53#C8': {'parts': [_o('còn thừa', ['chia hết', 'còn thừa'],
                                 'chia hết hay còn thừa'),
                              _o(6, nhan='mỗi bạn'), _o(4, nhan='thừa')]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (12, 13, 14, 15)}
    moi_ = {f'DL:KSN2.B{n}' for n in (48, 49, 50, 51, 52, 53)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        for m in ('chuyenMoBai', 'khamPha'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
        van = json.dumps(b, ensure_ascii=False)
        for ten in ('Trí Long', 'Su Kem', 'Gauss'):
            if ten in van:
                loi.append(f'{b["id"]}: còn tên riêng của sách "{ten}"')
        # Sách đặt tên ô trống là "X"; máy đọc chữ ấy thành tiếng Anh.
        if ' X ' in van or '▢' in van:
            loi.append(f'{b["id"]}: còn ký hiệu ô trống dạng "X" hoặc "▢" — '
                       f'phải gọi bằng chữ "ô trống"')
    NEO = {'DL:KSN2.B12': '50 + 30 = 80', 'DL:KSN2.B48': '3 × 10 = 30',
           'DL:KSN2.B13': '9 + 9 + 9 + 9 = 36', 'DL:KSN2.B49': '40 + 5 = 45',
           'DL:KSN2.B14': '12 − 5 = 7', 'DL:KSN2.B50': '28 : 4 = 7',
           'DL:KSN2.B51': '14 − 6 = 8', 'DL:KSN2.B15': '20 − 18 = 2',
           'DL:KSN2.B52': '17 − 15 = 2', 'DL:KSN2.B53': '17 − 15 = 2'}
    for b in MOI:
        mong = NEO.get(b['id'])
        if mong and mong not in json.dumps(b, ensure_ascii=False):
            loi.append(f'{b["id"]}: không bám số neo "{mong}" của chương')
    da = {b['id'] for b in MOI}
    for moi_ma, sau_ma in SAU.items():
        if sau_ma not in da:
            loi.append(f'{moi_ma}: chèn sau {sau_ma} mà bài ấy không có trong đợt này')
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
