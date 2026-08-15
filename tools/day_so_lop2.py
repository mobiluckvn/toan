# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 3 · DÃY SỐ KỲ DIỆU — ba bài chữ thành chín bài video.

Chương này gộp nặng hơn hai chương trước: mỗi bài của sách ôm trọn BA nghề khác
nhau, nên tách ra thành ba chứ không phải hai.

  · B09 gộp "tìm nhịp rồi đi tiếp" · "điền số mờ ở giữa" · "số này có thuộc dãy
    không". Nghề đầu là ĐI XUÔI, nghề hai là LẦN NGƯỢC, nghề ba là KIỂM TRA — ba
    động tác khác nhau, bé tắc ở chỗ nào cũng phải xem lại đúng chỗ ấy.
  · B10 gộp "dãy gấp đôi" · "dãy bậc thang" · "quy luật phải đúng với mọi số".
    Cái thứ ba mới là bài học thật, mà nó lại nằm lọt thỏm ở bước 4 của sách.
  · B11 gộp "nhìn đuôi đoán chẵn lẻ" · "bí mật hai bảng nhân" · "cộng chẵn lẻ".

── SỐ NEO ──
    4, 8, 12, 16       → nhịp 4, tiếp là 20 và 24
    5, __, 15, 20      → toa mờ là 10
    3, 6, 9, ...       → ga 20 tàu không dừng, nhảy từ 18 sang 21
    1, 2, 4, 8         → gấp đôi, tiếp là 16
    2, 3, 5, 8, 12     → bậc thang, tiếp là 17
    1, 2, 4, 8 ≠ 1, 2, 4, 7   → ba số đầu giống hệt mà hai quy luật khác nhau
    134 chẵn · 275 lẻ  → nhìn chữ số tận cùng
    bảng nhân 2 và 5   → toàn chẵn · đuôi 0 hoặc 5
    26 + 13            → chẵn cộng lẻ ra lẻ

    python3 tools/day_so_lop2.py --xem
    python3 tools/day_so_lop2.py
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

TEN_CHUONG = 'Dãy số kỳ diệu'
CHUONG = 3
CO_KHONG = ['có', 'không']
CHAN_LE = ['chẵn', 'lẻ']
LOAI_DAY = ['dãy gấp đôi', 'dãy cách đều', 'dãy bậc thang']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng video: hai mục mở bài và khám phá để RỖNG, video thay cả hai."""
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B09 · BẮT NHỊP ĐOÀN TÀU ═══
B09 = bai(
    9, 'BẮT NHỊP ĐOÀN TÀU — TRỪ ĐỂ TÌM NHỊP, CỘNG ĐỂ ĐI TIẾP',
    'SỐ 5.1a — Dãy số cách đều: tìm nhịp rồi viết tiếp.',
    video(
        ['Tìm được nhịp của một dãy số cách đều.',
         'Biết lấy số sau trừ số trước để ra nhịp.',
         'Cộng nhịp vào số cuối để viết tiếp dãy.'],
        ['Đề bài: Cho dãy số 4, 8, 12, 16, ... Hãy viết hai số tiếp theo của dãy.',
         'Tìm nhịp trước đã',
         'Lấy số sau trừ số trước: 8 − 4 = 4.',
         'Thử lại cho chắc',
         'Thử tiếp hai cặp nữa: 12 − 8 = 4 và 16 − 12 = 4. Nhịp đều tăm tắp là 4.',
         'Cộng nhịp để đi tiếp',
         'Số tiếp theo là 16 + 4 = 20. Số tiếp theo nữa là 20 + 4 = 24.',
         'Đáp số: 20 và 24.',
         'Một dãy chỉ gọi là cách đều khi MỌI khoảng đều bằng nhau, chứ không phải '
         'chỉ hai số đầu.'],
        ['Có bạn gặp dãy 2, 4, 6 rồi điền tiếp số 7, vì nghĩ miễn số sau to hơn số '
         'trước là được.',
         'Gợi ý 1: Dãy này đang chạy nhịp mấy? Lấy 4 − 2 rồi 6 − 4 xem.',
         'Gợi ý 2: Từ 6 sang 7 là bước dài bao nhiêu? Có bằng nhịp cũ không?',
         'Chữa: nhịp của dãy là 2, nên sau số 6 phải là số 8 chứ không phải 7.'],
        ['Số nhà trên một dãy phố, số ghế trong rạp, vạch đo trên cốc — chúng đều '
         'chạy theo một nhịp. Chỉ vào rồi hỏi con nhịp mấy.',
         'Bố mẹ chỉ cần hỏi một câu mỗi lần: "Từ số này sang số kia con nhảy bao xa?"'],
    ),
    [
        lt(1, 1, 'Dãy 3, 6, 9, 12 chạy nhịp mấy?',
           'Lấy số sau trừ số trước: 6 − 3 = 3.'),
        lt(2, 1, 'Dãy 4, 8, 12, 16 chạy nhịp mấy?',
           'Lấy số sau trừ số trước: 8 − 4 = 4.'),
        lt(3, 1, 'Dãy 3, 6, 9, 12, ... — số tiếp theo là số nào?',
           'Nhịp của dãy là 3, nên 12 + 3 = 15.'),
        lt(4, 2, 'Dãy 5, 10, 15, 20, ... — viết hai số tiếp theo.',
           'Nhịp là 5: 20 + 5 = 25, rồi 25 + 5 = 30.'),
        lt(5, 2, 'Dãy 7, 14, 21, ... — số tiếp theo là số nào?',
           'Nhịp là 7 vì 14 − 7 = 7, nên 21 + 7 = 28.'),
        lt(6, 2, 'Muốn tìm nhịp của một dãy cách đều thì làm gì?',
           'Lấy số sau trừ số trước là ra nhịp, rồi thử thêm vài cặp cho chắc.'),
        lt(7, 3, 'Dãy 2, 5, 8, 11, ... — số thứ sáu của dãy là số nào?',
           'Nhịp là 3. Số thứ năm là 11 + 3 = 14, số thứ sáu là 14 + 3 = 17.'),
        lt(8, 3, 'Một dãy cách đều bắt đầu từ 6 và chạy nhịp 4. Số thứ tư của dãy là '
                 'số nào?',
           'Từ số đầu tới số thứ tư có ba bước nhảy: 6 + 4 = 10, 10 + 4 = 14, '
           '14 + 4 = 18.'),
    ] + [
        q_tf(1, 'Muốn tìm nhịp của dãy cách đều, ta lấy số sau trừ số trước.', True,
             'Đúng, và nên thử lại với vài cặp nữa cho chắc.'),
        q_tf(2, 'Dãy 2, 4, 6 thì số tiếp theo có thể là 7.', False,
             'Sai. Nhịp của dãy là 2 nên sau số 6 phải là số 8.'),
        q_mcq(3, 'Dãy 3, 6, 9, 12, ... — số tiếp theo là số nào?',
              ['15', '13', '14', '18'], '15', 'Nhịp là 3 nên 12 + 3 = 15.'),
        q_mcq(4, 'Dãy 5, 10, 15, 20 chạy nhịp mấy?', ['5', '10', '15', '2'], '5',
              'Lấy số sau trừ số trước: 10 − 5 = 5.'),
        q_tf(5, 'Dãy cách đều thì mọi khoảng giữa hai số liền nhau đều bằng nhau.',
             True, 'Đúng — đó chính là nghĩa của chữ "cách đều".'),
    ],
)

# ═══ ② B42 · TOA MỜ Ở GIỮA ═══
B42 = bai(
    42, 'TOA MỜ Ở GIỮA — TÌM NHỊP TỪ HAI SỐ CÒN RÕ',
    'SỐ 5.1b — Dãy số cách đều: điền số còn thiếu ở giữa dãy.',
    video(
        ['Điền được số còn thiếu nằm giữa một dãy cách đều.',
         'Biết bắt nhịp từ hai số liền nhau còn rõ.',
         'Lần ngược lại chỗ bị thiếu bằng phép trừ.'],
        ['Đề bài: Điền số còn thiếu vào dãy 5, ..., 15, 20.',
         'Bắt nhịp ở chỗ còn rõ số',
         'Hai số 15 và 20 đứng cạnh nhau và còn rõ: 20 − 15 = 5. Nhịp của dãy là 5.',
         'Lần ngược lại chỗ bị thiếu',
         'Số đứng ngay trước 15 là 15 − 5 = 10.',
         'Thử lại xuôi từ đầu dãy',
         'Đi xuôi: 5 + 5 = 10, rồi 10 + 5 = 15, rồi 15 + 5 = 20. Cả dãy đúng nhịp.',
         'Đáp số: số còn thiếu là 10.',
         'Chỗ bị thiếu nằm đâu cũng được — miễn còn hai số liền nhau để bắt nhịp.'],
        ['Có bạn thấy dãy 5, ..., 15, 20 rồi điền luôn số 6, vì nghĩ cứ điền số nào to '
         'hơn số bên trái là xong.',
         'Gợi ý 1: Nhìn sang bên phải xem, hai số 15 và 20 cách nhau bao xa?',
         'Gợi ý 2: Nếu điền 6 thì bước từ 6 sang 15 dài bao nhiêu? Có bằng 5 không?',
         'Chữa: nhịp của dãy là 5, nên số còn thiếu là 15 − 5 = 10.'],
        ['Che một số trên thước kẻ hoặc trên lịch rồi hỏi con số bị che là số nào — '
         'đúng cái nghề của bài này.',
         'Bố mẹ hỏi: "Con bắt nhịp ở chỗ nào?" Trả lời được chỗ ấy là hiểu bài.'],
    ),
    [
        lt(1, 1, 'Dãy 2, ..., 6, 8 — nhịp của dãy là mấy?',
           'Hai số 6 và 8 còn rõ và đứng cạnh nhau: 8 − 6 = 2.'),
        lt(2, 1, 'Dãy 2, ..., 6, 8 — số còn thiếu là số nào?',
           'Nhịp là 2, nên số đứng trước 6 là 6 − 2 = 4.'),
        lt(3, 1, 'Dãy 10, 20, ..., 40 — số còn thiếu là số nào?',
           'Nhịp là 10, nên số sau 20 là 20 + 10 = 30.'),
        lt(4, 2, 'Dãy 5, ..., 15, 20 — số còn thiếu là số nào?',
           'Nhịp là 5 vì 20 − 15 = 5, nên số trước 15 là 15 − 5 = 10.'),
        lt(5, 2, 'Dãy 3, 6, ..., 12, 15 — số còn thiếu là số nào?',
           'Nhịp là 3, nên số sau 6 là 6 + 3 = 9.'),
        lt(6, 2, 'Dãy ..., 8, 12, 16 — số đầu tiên của dãy là số nào?',
           'Nhịp là 4, nên số đứng trước 8 là 8 − 4 = 4.'),
        lt(7, 3, 'Dãy 7, ..., ..., 22 — hai số còn thiếu là mấy?',
           'Từ 7 tới 22 có ba bước nhảy. Thử nhịp 5: 7 + 5 = 12, 12 + 5 = 17, '
           '17 + 5 = 22 — vừa khít. Vậy hai số là 12 và 17.'),
        lt(8, 3, 'Dãy 6, ..., 16, 21 — cho biết nhịp của dãy và số còn thiếu.',
           'Hai số 16 và 21 còn rõ: 21 − 16 = 5, nhịp là 5. Số trước 16 là '
           '16 − 5 = 11.'),
    ] + [
        q_tf(1, 'Muốn điền số còn thiếu ở giữa, phải bắt nhịp từ hai số liền nhau '
                'còn rõ.', True, 'Đúng — hai số liền nhau là đủ để ra nhịp.'),
        q_mcq(2, 'Dãy 5, ..., 15, 20 — số còn thiếu là số nào?',
              ['10', '9', '12', '8'], '10', 'Nhịp là 5 nên 15 − 5 = 10.'),
        q_tf(3, 'Số bị thiếu nằm giữa dãy thì không tìm được nhịp nữa.', False,
             'Sai. Chỉ cần còn hai số liền nhau ở bất cứ đâu là bắt được nhịp.'),
        q_mcq(4, 'Dãy 10, 20, ..., 40 — số còn thiếu là số nào?',
              ['30', '25', '35', '50'], '30', 'Nhịp là 10 nên 20 + 10 = 30.'),
        q_tf(5, 'Điền xong nên đi xuôi lại cả dãy xem có đúng nhịp không.', True,
             'Đúng — thử lại một lượt là chắc ăn.'),
    ],
)

# ═══ ③ B43 · GA NÀY TÀU CÓ DỪNG KHÔNG ═══
B43 = bai(
    43, 'SỐ NÀY CÓ TRONG DÃY KHÔNG — NHẢY CÓC THỬ',
    'SỐ 5.1c — Dãy số cách đều: kiểm tra một số có thuộc dãy hay không.',
    video(
        ['Kiểm tra được một số có nằm trong dãy đếm thêm hay không.',
         'Biết nhảy cóc thử cho tới khi vượt qua số cần hỏi.',
         'Nhận ra chỗ dãy nhảy vượt qua số ấy.'],
        ['Đề bài: Dãy 3, 6, 9, 12, ... cứ thế cộng thêm 3. Số 20 có nằm trong dãy '
         'không?',
         'Nhảy cóc thử từ đầu dãy',
         'Đi từng bước một: 3, 6, 9, 12, 15, 18, 21.',
         'Xem chỗ dãy vượt qua',
         'Dãy nhảy thẳng từ 18 sang 21, không đặt chân xuống 20. Vậy 20 không nằm '
         'trong dãy.',
         'Đáp số: không.',
         'Chỉ cần nhảy tới khi vượt qua số cần hỏi là dừng lại, không phải nhảy mãi.'],
        ['Có bạn thấy dãy 3, 6, 9 rồi bảo số 20 chắc chắn có, vì 20 to hơn 9 và dãy '
         'thì cứ tăng mãi.',
         'Gợi ý 1: Dãy tăng mãi thật, nhưng nó đặt chân xuống những số nào?',
         'Gợi ý 2: Nhảy thử tới gần 20 xem dãy dừng ở đâu.',
         'Chữa: dãy đi 15 rồi 18 rồi 21, nhảy qua mất 20 nên số 20 không có trong '
         'dãy.'],
        ['Đi cầu thang bộ mà bước cách hai bậc, rồi hỏi con có đặt chân xuống bậc 7 '
         'không — cùng một nghề với bài này.',
         'Bố mẹ hỏi: "Con dừng nhảy lúc nào?" Trả lời "khi đã vượt qua" là hiểu bài.'],
    ),
    [
        lt(1, 1, 'Dãy 2, 4, 6, 8, ... cộng thêm 2. Số 10 có trong dãy không?',
           'Nhảy tiếp từ 8 thêm 2 được đúng 10, nên số ấy có trong dãy.'),
        lt(2, 1, 'Dãy 5, 10, 15, ... cộng thêm 5. Số 25 có trong dãy không?',
           'Nhảy tiếp: 15, 20, 25 — đặt chân đúng vào 25, nên có trong dãy.'),
        lt(3, 1, 'Dãy 3, 6, 9, ... cộng thêm 3. Số 20 có trong dãy không?',
           'Nhảy tới 18 rồi 21, vượt qua mất 20 nên không có trong dãy.'),
        lt(4, 2, 'Dãy 4, 8, 12, ... cộng thêm 4. Số 30 có trong dãy không?',
           'Nhảy tới 28 rồi 32, vượt qua mất 30 nên không có trong dãy.'),
        lt(5, 2, 'Dãy 3, 6, 9, ... cộng thêm 3. Viết số của dãy đứng ngay trước số 20.',
           'Nhảy cóc: 15 rồi 18, mà 18 + 3 = 21 đã vượt qua 20. Vậy số ấy là 18.'),
        lt(6, 2, 'Dãy 6, 12, 18, ... cộng thêm 6. Số 36 có trong dãy không?',
           'Nhảy tiếp: 24, 30, 36 — đặt chân đúng vào 36, nên có trong dãy.'),
        lt(7, 3, 'Dãy 7, 14, 21, ... cộng thêm 7. Số 50 có trong dãy không, và số nào '
                 'của dãy gần 50 nhất mà vẫn bé hơn 50?',
           'Nhảy cóc: 28, 35, 42, 49, rồi 56 đã vượt. Số 50 không có trong dãy, còn '
           'số gần nhất mà vẫn bé hơn là 49.'),
        lt(8, 3, 'Dãy 3, 6, 9, ... cộng thêm 3 và dừng lại ở 27. Dãy ấy có bao nhiêu '
                 'số?',
           'Nhảy cóc rồi đếm: 3, 6, 9, 12, 15, 18, 21, 24, 27 — đúng 9 số. Cũng chính '
           'là bảng nhân 3 đọc từ đầu tới hết.'),
    ] + [
        q_tf(1, 'Muốn biết một số có trong dãy đếm thêm không, ta nhảy cóc thử tới '
                'khi vượt qua nó.', True, 'Đúng, và vượt qua rồi thì dừng.'),
        q_tf(2, 'Số 20 có trong dãy 3, 6, 9, 12, ...', False,
             'Sai. Dãy nhảy thẳng từ 18 sang 21, bỏ qua 20.'),
        q_mcq(3, 'Số nào sau đây có trong dãy 5, 10, 15, ...?',
              ['25', '22', '27', '31'], '25', 'Nhảy tiếp từ 15 được 20 rồi 25.'),
        q_mcq(4, 'Nhảy cóc thử thì dừng lúc nào?',
              ['khi đã vượt qua số cần hỏi', 'khi mỏi tay', 'khi tới số 100'],
              'khi đã vượt qua số cần hỏi',
              'Vượt qua rồi thì biết chắc, nhảy thêm cũng vô ích.'),
        q_tf(5, 'Dãy 4, 8, 12, ... có chứa số 30.', False,
             'Sai. Dãy nhảy từ 28 sang 32, không đặt chân xuống 30.'),
    ],
)

# ═══ ④ B10 · DÃY GẤP ĐÔI ═══
B10 = bai(
    10, 'DÃY GẤP ĐÔI — MỖI SỐ BẰNG SỐ TRƯỚC CỘNG CHÍNH NÓ',
    'SỐ 5.2a — Dãy không cách đều: dãy gấp đôi.',
    video(
        ['Nhận ra một dãy không cách đều.',
         'Nhận ra dãy gấp đôi: mỗi số bằng số trước cộng chính nó.',
         'Viết tiếp được dãy gấp đôi.'],
        ['Đề bài: Tìm quy luật rồi viết số tiếp theo của dãy 1, 2, 4, 8, ...',
         'Thử tìm nhịp trước đã',
         'Các khoảng là 2 − 1 = 1, rồi 4 − 2 = 2, rồi 8 − 4 = 4. Không bằng nhau, nên '
         'đây không phải dãy cách đều.',
         'Thử xem có phải gấp đôi không',
         'Nhìn lại từ đầu: 1 + 1 = 2, rồi 2 + 2 = 4, rồi 4 + 4 = 8. Mỗi số đúng bằng '
         'số trước cộng chính nó.',
         'Đi tiếp theo đúng quy luật ấy',
         'Số tiếp theo là 8 + 8 = 16.',
         'Đáp số: 16.',
         'Gặp dãy lạ thì thử nhịp trước; nhịp không đều mới đi tìm quy luật khác.'],
        ['Có bạn thấy dãy 1, 2, 4, 8 rồi bảo nhịp là 4 vì 8 − 4 = 4, và điền tiếp 12.',
         'Gợi ý 1: Bạn ấy mới thử đúng một cặp cuối. Thử cặp đầu xem, 2 − 1 bằng mấy?',
         'Gợi ý 2: Các khoảng có bằng nhau không? Nếu không thì đây đâu phải dãy cách '
         'đều.',
         'Chữa: các khoảng là 1, 2 rồi 4 nên dãy không cách đều. Đây là dãy gấp đôi, '
         'số tiếp theo là 8 + 8 = 16.'],
        ['Gấp đôi hạt gạo trên bàn cờ là câu chuyện cổ rất hợp lúc này — con sẽ thấy '
         'dãy gấp đôi lớn nhanh đến mức nào.',
         'Bố mẹ hỏi một câu: "Số này bằng số trước cộng cái gì?"'],
    ),
    [
        lt(1, 1, 'Dãy 1, 2, 4, 8 có phải dãy cách đều không?',
           'Các khoảng là 1, 2 rồi 4 — không bằng nhau nên không phải dãy cách đều.'),
        lt(2, 1, 'Tính 8 + 8.', 'Lấy 8 + 8 = 16.'),
        lt(3, 1, 'Dãy 1, 2, 4, 8, ... — số tiếp theo là số nào?',
           'Mỗi số bằng số trước cộng chính nó, nên 8 + 8 = 16.'),
        lt(4, 2, 'Dãy 3, 6, 12, 24, ... — số tiếp theo là số nào?',
           'Dãy gấp đôi, nên 24 + 24 = 48.'),
        lt(5, 2, 'Dãy 1, 2, 4, 8, 16, ... — viết hai số tiếp theo.',
           'Gấp đôi tiếp: 16 + 16 = 32, rồi 32 + 32 = 64.'),
        lt(6, 2, 'Một dãy gấp đôi bắt đầu từ số 5. Viết ba số đầu tiên của dãy.',
           'Số đầu là 5, rồi 5 + 5 = 10, rồi 10 + 10 = 20.'),
        lt(7, 3, 'Dãy 2, 4, 8, 16, ... — số thứ sáu của dãy là số nào?',
           'Đi tiếp: 16 + 16 = 32, rồi 32 + 32 = 64.'),
        lt(8, 3, 'Một dãy gấp đôi có số thứ ba là 12. Số đầu tiên của dãy là số nào?',
           'Lần ngược: số nào cộng chính nó ra 12? Là 6. Số nào cộng chính nó ra 6? '
           'Là 3.'),
    ] + [
        q_tf(1, 'Dãy gấp đôi là dãy mà mỗi số bằng số trước cộng chính nó.', True,
             'Đúng — đó là cách nhận ra nó.'),
        q_mcq(2, 'Dãy 1, 2, 4, 8, ... — số tiếp theo là số nào?',
              ['16', '10', '12', '9'], '16', 'Gấp đôi: 8 + 8 = 16.'),
        q_tf(3, 'Dãy 1, 2, 4, 8 là dãy cách đều.', False,
             'Sai. Các khoảng là 1, 2 rồi 4 — không bằng nhau.'),
        q_mcq(4, 'Gặp một dãy lạ thì nên thử điều gì trước?',
              ['tìm nhịp xem có cách đều không', 'đoán bừa một số',
               'cộng hết cả dãy lại'],
              'tìm nhịp xem có cách đều không',
              'Thử nhịp là rẻ nhất; không đều mới đi tìm quy luật khác.'),
        q_tf(5, 'Dãy 3, 6, 12, 24 là dãy gấp đôi.', True,
             'Đúng: 3 + 3 = 6, 6 + 6 = 12, 12 + 12 = 24.'),
    ],
)

# ═══ ⑤ B44 · DÃY BẬC THANG ═══
B44 = bai(
    44, 'DÃY BẬC THANG — BƯỚC NHẢY DÀI THÊM MỘT',
    'SỐ 5.2b — Dãy không cách đều: dãy bậc thang.',
    video(
        ['Viết được các bước nhảy của một dãy ra giấy.',
         'Nhận ra dãy bậc thang: bước nhảy mỗi lần dài thêm một.',
         'Viết tiếp được dãy bậc thang.'],
        ['Đề bài: Tìm quy luật rồi viết số tiếp theo của dãy 2, 3, 5, 8, 12, ...',
         'Viết các bước nhảy ra',
         'Các bước là 3 − 2 = 1, rồi 5 − 3 = 2, rồi 8 − 5 = 3, rồi 12 − 8 = 4.',
         'Nhìn chính các bước nhảy',
         'Các bước xếp thành 1, 2, 3, 4 — mỗi lần dài thêm một. Vậy bước tiếp theo '
         'dài 5.',
         'Đi thêm một bước nữa',
         'Số tiếp theo là 12 + 5 = 17.',
         'Đáp số: 17.',
         'Dãy cách đều thì các bước bằng nhau; dãy bậc thang thì chính các bước mới '
         'xếp thành dãy đều.'],
        ['Có bạn thấy dãy 2, 3, 5, 8 rồi bảo nhịp là 3 vì 8 − 5 = 3, và điền tiếp 11.',
         'Gợi ý 1: Viết cả bốn bước nhảy ra xem chúng có bằng nhau không.',
         'Gợi ý 2: Nếu các bước là 1, 2, 3 thì bước sau phải dài bao nhiêu?',
         'Chữa: các bước dài thêm một mỗi lần, nên bước sau dài 4 và số tiếp theo là '
         '8 + 4 = 12.'],
        ['Xếp que tính thành tam giác từng tầng: tầng 1 một que, tầng 2 hai que — số '
         'que cộng dồn chính là một dãy bậc thang.',
         'Bố mẹ hỏi: "Con viết các bước nhảy ra chưa?" Chưa viết là chưa làm được bài.'],
    ),
    [
        lt(1, 1, 'Dãy 1, 2, 4, 7 — bước nhảy từ số 1 sang số 2 dài bao nhiêu?',
           'Lấy 2 − 1 = 1.'),
        lt(2, 1, 'Dãy 1, 2, 4, 7 — bước nhảy từ số 4 sang số 7 dài bao nhiêu?',
           'Lấy 7 − 4 = 3.'),
        lt(3, 1, 'Dãy 1, 2, 4, 7, ... — số tiếp theo là số nào?',
           'Các bước là 1, 2, 3 nên bước sau dài 4: 7 + 4 = 11.'),
        lt(4, 2, 'Dãy 2, 3, 5, 8, ... — số tiếp theo là số nào?',
           'Các bước là 1, 2, 3 nên bước sau dài 4: 8 + 4 = 12.'),
        lt(5, 2, 'Dãy 1, 2, 4, 7, 11, ... — số tiếp theo là số nào?',
           'Bước sau dài 5, nên 11 + 5 = 16.'),
        lt(6, 2, 'Dãy bậc thang 3, 4, 6, 9 — viết ba bước nhảy của dãy.',
           'Lấy 4 − 3 = 1, rồi 6 − 4 = 2, rồi 9 − 6 = 3.'),
        lt(7, 3, 'Dãy 5, 6, 8, 11, 15, ... — viết hai số tiếp theo.',
           'Các bước là 1, 2, 3, 4. Bước tiếp dài 5: 15 + 5 = 20. Bước sau nữa dài 6: '
           '20 + 6 = 26.'),
        lt(8, 3, 'Một dãy bậc thang bắt đầu từ số 1 và bước đầu tiên dài 1. Số thứ năm '
                 'của dãy là số nào?',
           'Các bước là 1, 2, 3, 4: 1 + 1 = 2, rồi 2 + 2 = 4, rồi 4 + 3 = 7, rồi '
           '7 + 4 = 11.'),
    ] + [
        q_tf(1, 'Dãy bậc thang là dãy mà bước nhảy mỗi lần dài thêm một.', True,
             'Đúng — chính các bước mới là dãy đều.'),
        q_mcq(2, 'Dãy 1, 2, 4, 7, ... — số tiếp theo là số nào?',
              ['11', '10', '14', '8'], '11', 'Bước sau dài 4 nên 7 + 4 = 11.'),
        q_tf(3, 'Dãy 2, 3, 5, 8 là dãy cách đều.', False,
             'Sai. Các bước là 1, 2 rồi 3 — dài dần chứ không bằng nhau.'),
        q_mcq(4, 'Muốn nhận ra dãy bậc thang thì làm gì?',
              ['viết các bước nhảy ra rồi nhìn chính chúng', 'cộng cả dãy lại',
               'chỉ nhìn số cuối cùng'],
              'viết các bước nhảy ra rồi nhìn chính chúng',
              'Quy luật nằm ở các bước chứ không nằm ở các số.'),
        q_tf(5, 'Dãy 1, 2, 4, 7, 11 có các bước nhảy là 1, 2, 3, 4.', True,
             'Đúng — mỗi bước dài thêm một.'),
    ],
)

# ═══ ⑥ B45 · QUY LUẬT PHẢI ĐÚNG VỚI MỌI SỐ ═══
B45 = bai(
    45, 'QUY LUẬT PHẢI ĐÚNG VỚI MỌI SỐ — MỘT SỐ ĐỔI LÀ ĐỔI CẢ DÃY',
    'SỐ 5.2c — Dãy không cách đều: kiểm quy luật với tất cả các số đã cho.',
    video(
        ['Hiểu rằng quy luật phải đúng với tất cả các số đã cho.',
         'Phân biệt được dãy gấp đôi và dãy bậc thang khi mấy số đầu giống nhau.',
         'Biết kiểm lại quy luật từ đầu dãy chứ không chỉ hai số cuối.'],
        ['Đề bài: Hai dãy 1, 2, 4, 8, ... và 1, 2, 4, 7, ... chỉ khác nhau một con số. '
         'Mỗi dãy đi tiếp thế nào?',
         'Ba số đầu giống hệt nhau',
         'Cả hai dãy đều mở đầu bằng 1, 2, 4. Nhìn ba số ấy thôi thì chưa quyết được '
         'gì cả.',
         'Số thứ tư mới lộ ra quy luật',
         'Dãy thứ nhất có 4 + 4 = 8 nên là dãy gấp đôi. Dãy thứ hai có các bước 1, 2, '
         '3 nên là dãy bậc thang.',
         'Đi tiếp theo đúng quy luật của từng dãy',
         'Dãy gấp đôi: 8 + 8 = 16. Dãy bậc thang: bước sau dài 4, nên 7 + 4 = 11.',
         'Đáp số: 16 và 11.',
         'Một quy luật chỉ được nhận khi nó đúng với TẤT CẢ các số đã cho, chứ không '
         'phải chỉ hai số cuối.'],
        ['Có bạn nhìn dãy 3, 6, 12, 24, 48 rồi bảo đây là dãy cách đều nhịp 3, vì '
         '6 − 3 = 3.',
         'Gợi ý 1: Bạn ấy mới thử đúng cặp đầu. Cặp sau thì sao, 12 − 6 bằng mấy?',
         'Gợi ý 2: Một quy luật phải đúng với mọi cặp, không phải chỉ một cặp.',
         'Chữa: cặp sau đã lệch vì 12 − 6 = 6 chứ không phải 3. Đây là dãy gấp đôi.'],
        ['Cho con hai dãy chỉ khác nhau một số rồi hỏi chúng có cùng quy luật không — '
         'câu hỏi này khó hơn vẻ ngoài của nó rất nhiều.',
         'Bố mẹ hỏi: "Quy luật con vừa nói có đúng với số đầu tiên không?"'],
    ),
    [
        lt(1, 1, 'Ba số đầu của hai dãy 1, 2, 4, 8 và 1, 2, 4, 7 có giống nhau không?',
           'Cả hai dãy đều mở đầu bằng 1, 2, 4 nên ba số đầu giống hệt.'),
        lt(2, 1, 'Dãy 1, 2, 4, 8, ... — số tiếp theo là số nào?',
           'Đây là dãy gấp đôi, nên 8 + 8 = 16.'),
        lt(3, 1, 'Dãy 1, 2, 4, 7, ... — số tiếp theo là số nào?',
           'Đây là dãy bậc thang, bước sau dài 4 nên 7 + 4 = 11.'),
        lt(4, 2, 'Dãy 2, 4, 8, 16 là dãy gì?',
           'Mỗi số bằng số trước cộng chính nó nên đây là dãy gấp đôi.'),
        lt(5, 2, 'Dãy 2, 4, 6, 8 là dãy gì?',
           'Mọi khoảng đều bằng 2 nên đây là dãy cách đều.'),
        lt(6, 2, 'Dãy 2, 4, 7, 11 là dãy gì?',
           'Các bước là 2, 3, 4 — dài thêm một mỗi lần, nên đây là dãy bậc thang.'),
        lt(7, 3, 'Dãy mở đầu 1, 2, 4. Nếu là dãy gấp đôi thì số thứ tư là mấy, còn nếu '
                 'là dãy bậc thang thì số thứ tư là mấy?',
           'Gấp đôi thì 4 + 4 = 8. Bậc thang thì bước sau dài 3, nên 4 + 3 = 7.'),
        lt(8, 3, 'Có bạn bảo dãy 3, 6, 12, 24, 48 là dãy cách đều nhịp 3. Cho biết bạn '
                 'ấy sai ở đâu, rồi viết số tiếp theo của dãy.',
           'Cặp sau đã lệch: 12 − 6 = 6 chứ không phải 3. Đây là dãy gấp đôi nên số '
           'tiếp theo là 48 + 48 = 96.'),
    ] + [
        q_tf(1, 'Một quy luật phải đúng với tất cả các số đã cho, không phải chỉ hai '
                'số cuối.', True, 'Đúng — đây là bài học chính của bài này.'),
        q_mcq(2, 'Dãy 1, 2, 4, 8, ... — số tiếp theo là số nào?',
              ['16', '11', '12', '10'], '16', 'Dãy gấp đôi: 8 + 8 = 16.'),
        q_mcq(3, 'Dãy 1, 2, 4, 7, ... — số tiếp theo là số nào?',
              ['11', '14', '8', '12'], '11', 'Dãy bậc thang: 7 + 4 = 11.'),
        q_tf(4, 'Nhìn ba số 1, 2, 4 là đủ biết dãy chạy quy luật nào.', False,
             'Sai. Ba số ấy hợp với cả dãy gấp đôi lẫn dãy bậc thang.'),
        q_tf(5, 'Dãy 3, 6, 12, 24 là dãy cách đều.', False,
             'Sai. Các khoảng là 3, 6 rồi 12 — không bằng nhau.'),
    ],
)

# ═══ ⑦ B11 · CHẴN HAY LẺ NHÌN Ở ĐUÔI ═══
B11 = bai(
    11, 'CHẴN HAY LẺ NHÌN Ở ĐUÔI — CHỮ SỐ TẬN CÙNG',
    'SỐ 6.1 — Số chẵn số lẻ nhận ra bằng chữ số tận cùng.',
    video(
        ['Hiểu số chẵn là số chia đôi được đều, số lẻ thì thừa một.',
         'Nhận ra số chẵn số lẻ bằng chữ số tận cùng.',
         'Làm được với cả số lớn mà không phải chia thử.'],
        ['Đề bài: Trong hai số 134 và 275, số nào chẵn số nào lẻ?',
         'Chẵn và lẻ nghĩa là gì',
         'Số chẵn chia đôi được đều tăm tắp. Số lẻ chia đôi thì luôn thừa đúng một.',
         'Bí mật nằm ở chữ số cuối cùng bên phải',
         'Tận cùng là 0, 2, 4, 6 hoặc 8 thì số ấy chẵn. Tận cùng là 1, 3, 5, 7 hoặc 9 '
         'thì số ấy lẻ.',
         'Soi cái đuôi của hai số đã cho',
         'Số 134 tận cùng là 4 nên chẵn. Số 275 tận cùng là 5 nên lẻ.',
         'Đáp số: 134 là số chẵn, 275 là số lẻ.',
         'Số to cỡ nào cũng vậy — không cần chia thử, chỉ cần nhìn cái đuôi.'],
        ['Có bạn bảo 35 là số chẵn, vì 3 cộng 5 bằng 8 mà 8 là số chẵn.',
         'Gợi ý 1: Bài học bảo nhìn vào chữ số nào của số 35?',
         'Gợi ý 2: Chữ số tận cùng của 35 là mấy? Nó nằm trong nhóm chẵn hay nhóm lẻ?',
         'Chữa: cộng các chữ số lại là một nghề khác. Chẵn lẻ chỉ nhìn cái đuôi, mà '
         'đuôi của 35 là 5 nên 35 là số lẻ.'],
        ['Biển số xe, số nhà, số trang sách — chỉ vào rồi hỏi con chẵn hay lẻ. Một '
         'giây là trả lời được, không cần giấy bút.',
         'Bố mẹ hỏi: "Con nhìn chữ số nào để biết?" Chỉ đúng cái đuôi là hiểu bài.'],
    ),
    [
        lt(1, 1, 'Số 8 là số chẵn hay số lẻ?',
           'Chữ số tận cùng là 8 nên đây là số chẵn.'),
        lt(2, 1, 'Số 7 là số chẵn hay số lẻ?',
           'Chữ số tận cùng là 7 nên đây là số lẻ.'),
        lt(3, 1, 'Số 134 là số chẵn hay số lẻ?',
           'Chữ số tận cùng là 4 nên đây là số chẵn.'),
        lt(4, 2, 'Số 275 là số chẵn hay số lẻ?',
           'Chữ số tận cùng là 5 nên đây là số lẻ.'),
        lt(5, 2, 'Viết chữ số tận cùng của số 460, rồi cho biết số ấy chẵn hay lẻ.',
           'Chữ số tận cùng là 0, mà tận cùng 0 thì số ấy chẵn.'),
        lt(6, 2, 'Trong ba số 21, 34 và 55 có mấy số lẻ?',
           'Số 21 tận cùng 1 và số 55 tận cùng 5 đều lẻ, còn 34 tận cùng 4 là chẵn. '
           'Vậy có 2 số lẻ.'),
        lt(7, 3, 'Số bé nhất có hai chữ số là số chẵn hay số lẻ?',
           'Số bé nhất có hai chữ số là 10, tận cùng là 0 nên đây là số chẵn.'),
        lt(8, 3, 'Viết số chẵn lớn nhất có hai chữ số và số lẻ lớn nhất có hai chữ số.',
           'Số lớn nhất có hai chữ số là 99, tận cùng 9 nên lẻ. Lùi một bước được 98, '
           'tận cùng 8 nên chẵn.'),
    ] + [
        q_tf(1, 'Muốn biết một số chẵn hay lẻ, chỉ cần nhìn chữ số tận cùng.', True,
             'Đúng — số to cỡ nào cũng vậy.'),
        q_mcq(2, 'Số 134 là số nào?', ['số chẵn', 'số lẻ', 'vừa chẵn vừa lẻ'],
              'số chẵn', 'Tận cùng là 4 nên chẵn.'),
        q_tf(3, 'Số 275 là số chẵn.', False, 'Sai. Tận cùng là 5 nên đây là số lẻ.'),
        q_mcq(4, 'Số nào sau đây là số lẻ?', ['47', '36', '80', '24'], '47',
              'Tận cùng là 7 nên lẻ; ba số kia tận cùng 6, 0 và 4.'),
        q_tf(5, 'Số nào tận cùng bằng 0 thì số ấy là số chẵn.', True,
             'Đúng — tận cùng 0 luôn là số chẵn.'),
    ],
)

# ═══ ⑧ B46 · BẢNG NHÂN GIẤU GÌ ═══
B46 = bai(
    46, 'BẢNG NHÂN GIẤU GÌ — BẢNG 2 TOÀN CHẴN, BẢNG 5 ĐUÔI 0 HOẶC 5',
    'SỐ 6.4a — Chữ số tận cùng của bảng nhân 2 và bảng nhân 5.',
    video(
        ['Đọc được bảng nhân 2 và bảng nhân 5.',
         'Nhận ra bảng nhân 2 toàn số chẵn.',
         'Nhận ra bảng nhân 5 chỉ tận cùng bằng 0 hoặc 5.'],
        ['Đề bài: Đọc bảng nhân 2 và bảng nhân 5 rồi cho biết mỗi bảng giấu bí mật gì '
         'về cái đuôi.',
         'Đọc bảng nhân 2 rồi soi đuôi',
         'Bảng chạy 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. Cái đuôi chỉ có 2, 4, 6, 8 và '
         '0 — toàn số chẵn.',
         'Đọc bảng nhân 5 rồi soi đuôi',
         'Bảng chạy 5, 10, 15, 20, 25, 30, 35, 40, 45, 50. Cái đuôi chỉ có 5 và 0, '
         'thay nhau lần lượt.',
         'Vì sao bảng nhân 2 toàn số chẵn',
         'Vì mỗi số của bảng là hai phần bằng nhau ghép lại, nên chia đôi lúc nào '
         'cũng đều tăm tắp.',
         'Đáp số: bảng nhân 2 toàn số chẵn, bảng nhân 5 tận cùng bằng 0 hoặc 5.',
         'Nhờ hai bí mật này, nhìn cái đuôi là loại ngay được nhiều số không thuộc '
         'bảng.'],
        ['Có bạn bảo số 37 nằm trong bảng nhân 5, vì 37 to hơn 35 mà lại bé hơn 40.',
         'Gợi ý 1: Bảng nhân 5 có những cái đuôi nào?',
         'Gợi ý 2: Đuôi của 37 là mấy? Nó có nằm trong hai cái đuôi ấy không?',
         'Chữa: bảng nhân 5 chỉ có đuôi 0 hoặc 5, mà 37 đuôi 7 nên không thuộc bảng. '
         'Nằm giữa hai số của bảng không có nghĩa là thuộc bảng.'],
        ['Đọc thuộc bảng nhân là một việc, NHÌN RA quy luật trong bảng là việc khác — '
         'bài này làm việc thứ hai.',
         'Bố mẹ đọc một số bất kỳ rồi hỏi: "Số này chắc chắn không nằm trong bảng nào?"'],
    ),
    [
        lt(1, 1, 'Đọc bảng nhân 2 rồi viết số thứ ba của bảng.',
           'Bảng nhân 2 chạy 2, 4, 6 nên số thứ ba là 6.'),
        lt(2, 1, 'Các số trong bảng nhân 2 là số chẵn hay số lẻ?',
           'Cả bảng đều chia đôi được đều nên toàn số chẵn.'),
        lt(3, 1, 'Đọc bảng nhân 5 rồi viết số thứ tư của bảng.',
           'Bảng nhân 5 chạy 5, 10, 15, 20 nên số thứ tư là 20.'),
        lt(4, 2, 'Các số trong bảng nhân 5 tận cùng bằng những chữ số nào?',
           'Bảng chạy 5, 10, 15, 20 — cái đuôi chỉ có 0 và 5 thay nhau.'),
        lt(5, 2, 'Số 37 có nằm trong bảng nhân 5 không?',
           'Đuôi của 37 là 7, mà bảng nhân 5 chỉ có đuôi 0 hoặc 5 nên không thuộc.'),
        lt(6, 2, 'Số 25 có nằm trong bảng nhân 2 không?',
           'Đuôi của 25 là 5 nên đây là số lẻ, mà bảng nhân 2 toàn số chẵn.'),
        lt(7, 3, 'Trong bốn số 15, 20, 27 và 33, số nào vừa có trong bảng nhân 2 vừa '
                 'có trong bảng nhân 5?',
           'Phải vừa là số chẵn vừa có đuôi 0 hoặc 5 — chỉ số 20 đủ cả hai điều ấy.'),
        lt(8, 3, 'Viết ba số của bảng nhân 5 mà cũng là số chẵn.',
           'Bảng nhân 5 chạy 5, 10, 15, 20, 25, 30 — trong đó 10, 20 và 30 tận cùng 0 '
           'nên chẵn.'),
    ] + [
        q_tf(1, 'Mọi số trong bảng nhân 2 đều là số chẵn.', True,
             'Đúng — mỗi số là hai phần bằng nhau ghép lại.'),
        q_tf(2, 'Bảng nhân 5 có số tận cùng bằng 3.', False,
             'Sai. Bảng nhân 5 chỉ có đuôi 0 hoặc 5.'),
        q_mcq(3, 'Số nào sau đây chắc chắn KHÔNG có trong bảng nhân 5?',
              ['32', '35', '40', '25'], '32',
              'Đuôi 2 không phải 0 cũng không phải 5.'),
        q_mcq(4, 'Bảng nhân 2 giấu bí mật gì?',
              ['các số đều chẵn', 'các số đều lẻ', 'các số đều tận cùng bằng 5'],
              'các số đều chẵn', 'Vì mỗi số là hai phần bằng nhau ghép lại.'),
        q_tf(5, 'Nhìn cái đuôi là loại ngay được nhiều số không thuộc bảng.', True,
             'Đúng — đỡ phải đọc lại cả bảng.'),
    ],
)

# ═══ ⑨ B47 · CỘNG CHẴN LẺ ═══
B47 = bai(
    47, 'CỘNG CHẴN LẺ — CHƯA TÍNH ĐÃ BIẾT TỔNG',
    'SỐ 6.4b — Tính nết chẵn lẻ của tổng, không cần tính kết quả.',
    video(
        ['Nhớ ba luật: chẵn cộng chẵn ra chẵn, lẻ cộng lẻ ra chẵn, chẵn cộng lẻ ra lẻ.',
         'Đoán được tổng chẵn hay lẻ mà chưa cần tính.',
         'Biết thử lại bằng cách tính ra rồi soi đuôi.'],
        ['Đề bài: Không tính kết quả, cho biết tổng 26 + 13 là số chẵn hay số lẻ.',
         'Soi tính nết từng số hạng',
         'Số 26 tận cùng là 6 nên chẵn. Số 13 tận cùng là 3 nên lẻ.',
         'Nhớ ba luật cộng',
         'Chẵn cộng chẵn ra chẵn. Lẻ cộng lẻ cũng ra chẵn, vì hai cái lẻ bắt cặp được '
         'với nhau. Chẵn cộng lẻ thì ra lẻ.',
         'Áp luật vào bài',
         'Đây là chẵn cộng lẻ, nên tổng là số lẻ.',
         'Đáp số: số lẻ.',
         'Thử lại cho chắc: 26 + 13 = 39, tận cùng là 9 — đúng là số lẻ.'],
        ['Có bạn bảo lẻ cộng lẻ thì ra lẻ, vì hai số lẻ cộng lại thì vẫn lẻ chứ sao.',
         'Gợi ý 1: Lấy 3 viên kẹo và 5 viên kẹo xếp ra bàn xem được bao nhiêu viên.',
         'Gợi ý 2: Mỗi bên thừa một viên lẻ loi. Hai viên lẻ loi ấy gặp nhau thì '
         'thành mấy?',
         'Chữa: hai viên lẻ loi bắt cặp với nhau thành một cặp đủ, nên lẻ cộng lẻ ra '
         'chẵn: 3 + 5 = 8.'],
        ['Chia kẹo là cách nhìn ra luật này nhanh nhất — số lẻ luôn thừa đúng một viên '
         'lẻ loi, và hai viên lẻ loi gặp nhau thì bắt cặp.',
         'Bố mẹ hỏi trước khi con bấm máy tính: "Con đoán tổng chẵn hay lẻ?"'],
    ),
    [
        lt(1, 1, 'Tổng 4 + 6 là số chẵn hay số lẻ?',
           'Cả hai đều chẵn, mà chẵn cộng chẵn ra chẵn.'),
        lt(2, 1, 'Tổng 3 + 5 là số chẵn hay số lẻ?',
           'Cả hai đều lẻ, mà lẻ cộng lẻ ra chẵn vì hai cái lẻ bắt cặp với nhau.'),
        lt(3, 1, 'Tổng 4 + 5 là số chẵn hay số lẻ?',
           'Một số chẵn cộng một số lẻ thì ra số lẻ.'),
        lt(4, 2, 'Không tính kết quả, cho biết tổng 26 + 13 là số chẵn hay số lẻ.',
           'Số 26 chẵn, số 13 lẻ. Chẵn cộng lẻ ra lẻ.'),
        lt(5, 2, 'Không tính kết quả, cho biết tổng 17 + 25 là số chẵn hay số lẻ.',
           'Cả 17 và 25 đều lẻ. Lẻ cộng lẻ ra chẵn.'),
        lt(6, 2, 'Tính 26 + 13, rồi viết chữ số tận cùng của tổng.',
           'Lấy 26 + 13 = 39, chữ số tận cùng của tổng là 9.'),
        lt(7, 3, 'Tổng của ba số lẻ là số chẵn hay số lẻ?',
           'Hai số lẻ đầu bắt cặp thành chẵn, rồi cộng thêm số lẻ thứ ba nên tổng là '
           'số lẻ.'),
        lt(8, 3, 'Không tính kết quả, cho biết tổng 12 + 34 + 57 là số chẵn hay số lẻ, '
                 'và trong ba số ấy có mấy số lẻ.',
           'Số 12 và 34 đều chẵn, chỉ 57 là lẻ nên có đúng 1 số lẻ. Chẵn cộng chẵn ra '
           'chẵn, rồi cộng thêm một số lẻ nên tổng là số lẻ.'),
    ] + [
        q_tf(1, 'Lẻ cộng lẻ ra số chẵn.', True,
             'Đúng — hai cái lẻ bắt cặp được với nhau.'),
        q_tf(2, 'Chẵn cộng lẻ ra số chẵn.', False, 'Sai. Chẵn cộng lẻ thì ra số lẻ.'),
        q_mcq(3, 'Tổng 26 + 13 là số nào?',
              ['số lẻ', 'số chẵn', 'vừa chẵn vừa lẻ'], 'số lẻ',
              'Số 26 chẵn cộng số 13 lẻ thì ra lẻ.'),
        q_mcq(4, 'Tổng 17 + 25 là số nào?',
              ['số chẵn', 'số lẻ', 'không đoán được'], 'số chẵn',
              'Cả hai đều lẻ, mà lẻ cộng lẻ ra chẵn.'),
        q_tf(5, 'Muốn biết tổng chẵn hay lẻ thì bắt buộc phải tính ra kết quả.', False,
             'Sai. Chỉ cần nhìn tính nết của từng số hạng.'),
    ],
)

MOI = [B09, B42, B43, B10, B44, B45, B11, B46, B47]

# Thứ tự học: mỗi bài mới chèn ngay SAU bài đã nêu. Đọc lần lượt từ trên xuống —
# B43 chèn sau B42 nên phải đứng dưới dòng của B42.
SAU = {
    'DL:KSN2.B42': 'DL:KSN2.B09',
    'DL:KSN2.B43': 'DL:KSN2.B42',
    'DL:KSN2.B44': 'DL:KSN2.B10',
    'DL:KSN2.B45': 'DL:KSN2.B44',
    'DL:KSN2.B46': 'DL:KSN2.B11',
    'DL:KSN2.B47': 'DL:KSN2.B46',
}

_CHON_CHAN_LE = ['chẵn', 'lẻ']
_CHON_CO_KHONG = ['có', 'không']


def _o(gt, chon=None, nhan=None):
    """Một ô nhập. Chuỗi thì BẮT BUỘC kèm nút bấm — luật ô nhập số 1 của lớp 2."""
    d = {'value': gt}
    if chon:
        d['options'] = list(chon)
    if nhan:
        d['label'] = nhan
    return d


O_NHAP_MOI = {
 # ① B09 · bắt nhịp
 'DL:KSN2.B09#C1': {'value': 3},
 'DL:KSN2.B09#C2': {'value': 4},
 'DL:KSN2.B09#C3': {'value': 15},
 'DL:KSN2.B09#C4': {'parts': [_o(25, nhan='số thứ nhất'),
                              _o(30, nhan='số thứ hai')]},
 'DL:KSN2.B09#C5': {'value': 28},
 'DL:KSN2.B09#C6': {'parts': [_o('lấy số sau trừ số trước',
                                 ['lấy số sau trừ số trước', 'cộng cả dãy lại',
                                  'nhìn số cuối cùng'], 'cách tìm nhịp')]},
 'DL:KSN2.B09#C7': {'value': 17},
 'DL:KSN2.B09#C8': {'value': 18},

 # ② B42 · toa mờ ở giữa
 'DL:KSN2.B42#C1': {'value': 2},
 'DL:KSN2.B42#C2': {'value': 4},
 'DL:KSN2.B42#C3': {'value': 30},
 'DL:KSN2.B42#C4': {'value': 10},
 'DL:KSN2.B42#C5': {'value': 9},
 'DL:KSN2.B42#C6': {'value': 4},
 'DL:KSN2.B42#C7': {'parts': [_o(12, nhan='số thứ nhất'),
                              _o(17, nhan='số thứ hai')]},
 'DL:KSN2.B42#C8': {'parts': [_o(5, nhan='nhịp'),
                              _o(11, nhan='số còn thiếu')]},

 # ③ B43 · nhảy cóc thử
 'DL:KSN2.B43#C1': {'parts': [_o('có', _CHON_CO_KHONG, 'có trong dãy không')]},
 'DL:KSN2.B43#C2': {'parts': [_o('có', _CHON_CO_KHONG, 'có trong dãy không')]},
 'DL:KSN2.B43#C3': {'parts': [_o('không', _CHON_CO_KHONG, 'có trong dãy không')]},
 'DL:KSN2.B43#C4': {'parts': [_o('không', _CHON_CO_KHONG, 'có trong dãy không')]},
 'DL:KSN2.B43#C5': {'value': 18},
 'DL:KSN2.B43#C6': {'parts': [_o('có', _CHON_CO_KHONG, 'có trong dãy không')]},
 'DL:KSN2.B43#C7': {'parts': [_o('không', _CHON_CO_KHONG, 'có trong dãy không'),
                              _o(49, nhan='số gần nhất mà vẫn bé hơn')]},
 'DL:KSN2.B43#C8': {'value': 9},

 # ④ B10 · dãy gấp đôi
 'DL:KSN2.B10#C1': {'parts': [_o('không', _CHON_CO_KHONG, 'có cách đều không')]},
 'DL:KSN2.B10#C2': {'value': 16},
 'DL:KSN2.B10#C3': {'value': 16},
 'DL:KSN2.B10#C4': {'value': 48},
 'DL:KSN2.B10#C5': {'parts': [_o(32, nhan='số thứ nhất'),
                              _o(64, nhan='số thứ hai')]},
 'DL:KSN2.B10#C6': {'parts': [_o(5, nhan='số thứ nhất'),
                              _o(10, nhan='số thứ hai'),
                              _o(20, nhan='số thứ ba')]},
 'DL:KSN2.B10#C7': {'value': 64},
 'DL:KSN2.B10#C8': {'value': 3},

 # ⑤ B44 · dãy bậc thang
 'DL:KSN2.B44#C1': {'value': 1},
 'DL:KSN2.B44#C2': {'value': 3},
 'DL:KSN2.B44#C3': {'value': 11},
 'DL:KSN2.B44#C4': {'value': 12},
 'DL:KSN2.B44#C5': {'value': 16},
 'DL:KSN2.B44#C6': {'parts': [_o(1, nhan='bước thứ nhất'),
                              _o(2, nhan='bước thứ hai'),
                              _o(3, nhan='bước thứ ba')]},
 'DL:KSN2.B44#C7': {'parts': [_o(20, nhan='số thứ nhất'),
                              _o(26, nhan='số thứ hai')]},
 'DL:KSN2.B44#C8': {'value': 11},

 # ⑥ B45 · quy luật phải đúng với mọi số
 'DL:KSN2.B45#C1': {'parts': [_o('có', _CHON_CO_KHONG, 'ba số đầu có giống nhau')]},
 'DL:KSN2.B45#C2': {'value': 16},
 'DL:KSN2.B45#C3': {'value': 11},
 'DL:KSN2.B45#C4': {'parts': [_o('dãy gấp đôi', LOAI_DAY, 'loại dãy')]},
 'DL:KSN2.B45#C5': {'parts': [_o('dãy cách đều', LOAI_DAY, 'loại dãy')]},
 'DL:KSN2.B45#C6': {'parts': [_o('dãy bậc thang', LOAI_DAY, 'loại dãy')]},
 'DL:KSN2.B45#C7': {'parts': [_o(8, nhan='nếu là dãy gấp đôi'),
                              _o(7, nhan='nếu là dãy bậc thang')]},
 'DL:KSN2.B45#C8': {'parts': [_o('chỉ thử một cặp, các cặp sau đã lệch',
                                 ['chỉ thử một cặp, các cặp sau đã lệch',
                                  'bạn ấy không sai gì cả'], 'bạn ấy sai ở đâu'),
                              _o(96, nhan='số tiếp theo')]},

 # ⑦ B11 · chẵn lẻ nhìn ở đuôi
 'DL:KSN2.B11#C1': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B11#C2': {'parts': [_o('lẻ', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B11#C3': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B11#C4': {'parts': [_o('lẻ', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B11#C5': {'parts': [_o(0, nhan='chữ số tận cùng'),
                              _o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B11#C6': {'value': 2},
 'DL:KSN2.B11#C7': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B11#C8': {'parts': [_o(98, nhan='số chẵn lớn nhất'),
                              _o(99, nhan='số lẻ lớn nhất')]},

 # ⑧ B46 · bí mật hai bảng nhân
 'DL:KSN2.B46#C1': {'value': 6},
 'DL:KSN2.B46#C2': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B46#C3': {'value': 20},
 'DL:KSN2.B46#C4': {'parts': [_o(0, nhan='chữ số thứ nhất'),
                              _o(5, nhan='chữ số thứ hai')]},
 'DL:KSN2.B46#C5': {'parts': [_o('không', _CHON_CO_KHONG, 'có trong bảng không')]},
 'DL:KSN2.B46#C6': {'parts': [_o('không', _CHON_CO_KHONG, 'có trong bảng không')]},
 'DL:KSN2.B46#C7': {'parts': [_o('20', ['15', '20', '27', '33'], 'số cần tìm')]},
 'DL:KSN2.B46#C8': {'parts': [_o(10, nhan='số thứ nhất'),
                              _o(20, nhan='số thứ hai'),
                              _o(30, nhan='số thứ ba')]},

 # ⑨ B47 · cộng chẵn lẻ
 'DL:KSN2.B47#C1': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B47#C2': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B47#C3': {'parts': [_o('lẻ', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B47#C4': {'parts': [_o('lẻ', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B47#C5': {'parts': [_o('chẵn', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B47#C6': {'parts': [_o(39, nhan='tổng'),
                              _o(9, nhan='chữ số tận cùng')]},
 'DL:KSN2.B47#C7': {'parts': [_o('lẻ', _CHON_CHAN_LE, 'chẵn hay lẻ')]},
 'DL:KSN2.B47#C8': {'parts': [_o('lẻ', _CHON_CHAN_LE, 'tổng chẵn hay lẻ'),
                              _o(1, nhan='có mấy số lẻ')]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (9, 10, 11)}
    moi_ = {f'DL:KSN2.B{n}' for n in (42, 43, 44, 45, 46, 47)}
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
    # Mỗi bài phải bám đúng số neo của nó — đổi ví dụ mà quên đổi video là lệch.
    NEO = {'DL:KSN2.B09': '8 − 4 = 4', 'DL:KSN2.B42': '15 − 5 = 10',
           'DL:KSN2.B43': '18 sang 21', 'DL:KSN2.B10': '8 + 8 = 16',
           'DL:KSN2.B44': '12 + 5 = 17', 'DL:KSN2.B45': '16 và 11',
           'DL:KSN2.B11': '275', 'DL:KSN2.B46': 'bảng nhân 5',
           'DL:KSN2.B47': '26 + 13 = 39'}
    for b in MOI:
        mong = NEO.get(b['id'])
        if mong and mong not in json.dumps(b, ensure_ascii=False):
            loi.append(f'{b["id"]}: không bám số neo "{mong}" của chương')
    # Thứ tự chèn phải chèn được: bài mốc hoặc đã có, hoặc đã chèn ở dòng trên.
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
