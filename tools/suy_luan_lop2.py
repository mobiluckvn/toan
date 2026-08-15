# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 6 · THÁM TỬ TÍ HON — bốn bài chữ thành tám bài video.

Chương suy luận. Bài nào cũng gộp hai nghề, và cái thứ hai luôn là CHỖ SÁCH TỰ NÊU
RA LÀ HAY SAI NHẤT — đúng thứ đáng đứng riêng một bài:

  · B22 gộp "đảo phép từng máy" với "máy làm SAU CÙNG thì lùi qua TRƯỚC". Bạn nhỏ
    trong sách đảo phép đúng mà lùi sai thứ tự, rồi tắc đường.
  · B23 gộp "gắn tạm hai chân cho tất cả" với "chân thừa chia thành từng cặp".
  · B24 gộp "cây và khoảng" với bài NGƯỢC "biết chiều dài, tìm số cây".
  · B25 gộp "vẽ thang xếp thứ tự" với "bảng loại trừ".

⚠ Chữ "thám tử" nằm trong danh sách cấm của lời đọc video (nó là vỏ nhân vật của
sách). Tên chương thì giữ nguyên trong dữ liệu, nhưng lời đọc phải tránh — cùng lý
do với "vũ khí" mà sách dùng ở bài 25.

── SỐ NEO ──
    ? → −2 → ×3 → 12   → lùi 12 : 3 = 4, rồi 4 + 2 = 6
    ? → +3 → ×2 → 16   → lùi 16 : 2 = 8, rồi 8 − 3 = 5 (lùi sai thứ tự thì tắc ở 13)
    5 đầu · 14 chân    → gắn tạm 10 chân, còn thừa 4
    4 chân thừa        → 2 cặp, tức 2 con chó và 3 con gà
    bàn tay 5 ngón     → 4 kẽ; 5 cây 4 khoảng, mỗi khoảng 2 mét là 8 mét
    đường 15 mét       → 5 khoảng, nên 6 cây
    Voi · Gấu · Thỏ    → thang xếp ba bậc
    Mai · Đào · Cúc    → bảng loại trừ ba hàng ba cột

    python3 tools/suy_luan_lop2.py --xem
    python3 tools/suy_luan_lop2.py
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

TEN_CHUONG = 'Thám tử tí hon'
CHUONG = 6
CO_KHONG = ['có', 'không']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng video: hai mục mở bài và khám phá để RỖNG, video thay cả hai."""
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B22 · ĐI LÙI QUA HAI MÁY ═══
B22 = bai(
    22, 'ĐI LÙI QUA HAI MÁY — ĐẢO PHÉP TỪNG MÁY',
    'LV 8.1a — Tính ngược từ cuối: đảo phép của từng máy.',
    video(
        ['Vẽ được hành trình xuôi của số cần tìm.',
         'Đảo phép từng máy khi đi lùi.',
         'Thử lại bằng cách chạy xuôi.'],
        ['Đề bài: Một số đem trừ đi 2, rồi nhân với 3 thì được 12. Tìm số ấy.',
         'Vẽ hành trình xuôi của số cần tìm',
         'Số cần tìm chui vào máy trừ 2, rồi vào máy nhân 3, và chạy ra thành 12.',
         'Đi lùi thì đảo phép từng máy',
         'Máy nhân 3 lùi lại thành máy chia 3. Máy trừ 2 lùi lại thành máy cộng 2.',
         'Lùi từng máy một',
         'Trước khi nhân 3, số ấy là 12 : 3 = 4. Trước khi trừ 2, số ấy là 4 + 2 = 6.',
         'Thử lại bằng cách chạy xuôi',
         'Lấy 6 − 2 = 4, rồi 4 × 3 = 12, khớp đúng đề bài.',
         'Đáp số: số cần tìm là 6.',
         'Mỗi máy phải đảo phép: cộng thành trừ, trừ thành cộng, nhân thành chia.'],
        ['Có bạn đi lùi mà quên đảo phép, cứ trừ tiếp rồi nhân tiếp như lúc đi xuôi.',
         'Gợi ý 1: Đi lùi là gỡ lại việc máy vừa làm, hay làm thêm một lần nữa?',
         'Gợi ý 2: Máy nhân 3 đã làm số to lên ba lần. Muốn gỡ ra thì phải làm gì?',
         'Chữa: đi lùi thì đảo phép. Máy nhân thành máy chia, máy trừ thành máy '
         'cộng.'],
        ['Trò chơi ở nhà: bố mẹ nghĩ một số rồi làm hai bước, đọc kết quả cho con '
         'đoán ngược. Đổi vai cho con ra đề.',
         'Bố mẹ hỏi: "Con đã đảo phép của từng máy chưa?"'],
    ),
    [
        lt(1, 1, 'Tính 12 : 3.', 'Lấy 12 : 3 = 4.'),
        lt(2, 1, 'Máy ngược của máy nhân 3 là máy nào?',
           'Nhân và chia ngược chiều nhau, nên máy ngược là máy chia 3.'),
        lt(3, 1, 'Một số đem trừ 2, rồi nhân 3 thì được 12. Trước khi nhân 3, số ấy là '
                 'mấy?',
           'Lùi qua máy nhân 3 trước: 12 : 3 = 4.'),
        lt(4, 2, 'Một số đem trừ 2, rồi nhân 3 thì được 12. Số cần tìm là mấy?',
           'Lùi tiếp qua máy trừ 2, tức là cộng lại: 4 + 2 = 6.'),
        lt(5, 2, 'Một số đem cộng 4, rồi nhân 2 thì được 18. Số cần tìm là mấy?',
           'Lùi qua máy nhân 2: 18 : 2 = 9. Rồi lùi qua máy cộng 4: 9 − 4 = 5.'),
        lt(6, 2, 'Đi lùi thì máy nhân đảo thành máy gì?',
           'Máy nhân đảo lại thành máy chia, vì hai phép ấy ngược chiều nhau.'),
        lt(7, 3, 'Một số đem nhân 4, rồi trừ 3 thì được 17. Số cần tìm là mấy, và thử '
                 'lại chạy xuôi được bao nhiêu?',
           'Lùi qua máy trừ 3: 17 + 3 = 20. Rồi lùi qua máy nhân 4: 20 : 4 = 5. Thử '
           'lại: 5 × 4 = 20, rồi 20 − 3 = 17.'),
        lt(8, 3, 'Một số đem chia 2, rồi cộng 7 thì được 12. Số cần tìm là mấy?',
           'Lùi qua máy cộng 7: 12 − 7 = 5. Rồi lùi qua máy chia 2: 5 × 2 = 10.'),
    ] + [
        q_tf(1, 'Đi lùi thì mỗi máy phải đảo phép.', True,
             'Đúng — đi lùi là gỡ lại việc máy vừa làm.'),
        q_mcq(2, 'Máy ngược của máy nhân 3 là máy nào?',
              ['máy chia 3', 'máy nhân 3', 'máy trừ 3'], 'máy chia 3',
              'Nhân và chia ngược chiều nhau.'),
        q_mcq(3, 'Một số trừ 2 rồi nhân 3 thì được 12. Số ấy là mấy?',
              ['6', '4', '2', '36'], '6', 'Lùi qua hai máy là ra.'),
        q_tf(4, 'Tìm xong thì nên chạy xuôi thử lại một lần.', True,
             'Đúng — đó là bước cuối bắt buộc.'),
        q_tf(5, 'Máy chia đảo lại thành máy trừ.', False,
             'Sai. Máy chia đảo lại thành máy nhân.'),
    ],
)

# ═══ ② B60 · THỨ TỰ ĐI LÙI ═══
B60 = bai(
    60, 'MÁY LÀM SAU CÙNG THÌ LÙI QUA TRƯỚC',
    'LV 8.1b — Tính ngược từ cuối: thứ tự đi lùi.',
    video(
        ['Nhận ra máy nào làm sau cùng trong hành trình xuôi.',
         'Lùi qua máy làm sau cùng trước tiên.',
         'Biết tắc đường lúc đi lùi là chuông báo sai thứ tự.'],
        ['Đề bài: Một số đem cộng 3, rồi nhân với 2 thì được 16. Tìm số ấy.',
         'Thứ tự đi lùi mới là chỗ khó',
         'Số ấy đi qua máy cộng 3 trước, rồi mới qua máy nhân 2. Vậy máy nhân 2 là '
         'máy làm sau cùng.',
         'Máy làm sau cùng thì lùi qua trước',
         'Cởi ba lô trước rồi mới cởi áo. Nên phải lùi qua máy nhân 2 trước.',
         'Lùi cho đúng thứ tự',
         'Lấy 16 : 2 = 8, rồi 8 − 3 = 5.',
         'Thử lại bằng cách chạy xuôi',
         'Lấy 5 + 3 = 8, rồi 8 × 2 = 16, khớp đúng đề bài.',
         'Đáp số: số cần tìm là 5.',
         'Lùi sai thứ tự thì thường tắc đường ngay — đó chính là chuông báo động.'],
        ['Có bạn lùi ngay qua máy cộng 3 trước, lấy 16 − 3 = 13, rồi tắc vì 13 không '
         'chia đôi được.',
         'Gợi ý 1: Số ấy đi qua máy nào sau cùng trên đường xuôi?',
         'Gợi ý 2: Máy làm sau cùng thì phải lùi qua trước. Bạn ấy đảo phép đúng mà '
         'lùi sai thứ tự.',
         'Chữa: lùi qua máy nhân 2 trước, được 16 : 2 = 8, rồi 8 − 3 = 5.'],
        ['Cởi áo khoác rồi mới cởi áo trong — việc gì mặc sau thì cởi trước. Nhắc con '
         'câu ấy là con nhớ được thứ tự đi lùi.',
         'Bố mẹ hỏi: "Máy nào làm sau cùng?"'],
    ),
    [
        lt(1, 1, 'Một số đem cộng 3, rồi nhân 2. Máy nào làm sau cùng?',
           'Số ấy qua máy cộng 3 trước, nên máy nhân 2 làm sau cùng.'),
        lt(2, 1, 'Tính 16 : 2.', 'Lấy 16 : 2 = 8.'),
        lt(3, 1, 'Một số đem cộng 3 rồi nhân 2 thì được 16. Phải lùi qua máy nào '
                 'trước?',
           'Máy nhân 2 làm sau cùng nên phải lùi qua nó trước.'),
        lt(4, 2, 'Một số đem cộng 3 rồi nhân 2 thì được 16. Số cần tìm là mấy?',
           'Lùi qua máy nhân 2 trước: 16 : 2 = 8. Rồi 8 − 3 = 5.'),
        lt(5, 2, 'Có bạn lùi bằng cách lấy 16 trừ 3 được 13 rồi tắc. Bạn ấy sai ở đâu?',
           'Bạn ấy lùi sai thứ tự. Phải lùi qua máy làm sau cùng trước đã.'),
        lt(6, 2, 'Một số đem nhân 2, rồi cộng 5 thì được 19. Lùi qua máy nào trước, và '
                 'số cần tìm là mấy?',
           'Máy cộng 5 làm sau cùng nên lùi qua nó trước: 19 − 5 = 14. Rồi 14 : 2 = 7.'),
        lt(7, 3, 'Một số đem trừ 4, rồi nhân 3 thì được 21. Số cần tìm là mấy?',
           'Máy nhân 3 làm sau cùng nên lùi trước: 21 : 3 = 7. Rồi 7 + 4 = 11.'),
        lt(8, 3, 'Một số đem cộng 2, rồi nhân 5 thì được 40. Số cần tìm là mấy, và thử '
                 'lại chạy xuôi được bao nhiêu?',
           'Lùi qua máy nhân 5 trước: 40 : 5 = 8. Rồi 8 − 2 = 6. Thử lại: 6 + 2 = 8, '
           'rồi 8 × 5 = 40.'),
    ] + [
        q_tf(1, 'Máy làm sau cùng thì lùi qua trước.', True,
             'Đúng — cởi ba lô trước rồi mới cởi áo.'),
        q_mcq(2, 'Một số cộng 3 rồi nhân 2 thì được 16. Số ấy là mấy?',
              ['5', '13', '8', '16'], '5', 'Lùi qua máy nhân trước.'),
        q_tf(3, 'Lùi qua máy cộng 3 trước là đúng thứ tự.', False,
             'Sai. Máy nhân 2 làm sau cùng nên phải lùi qua nó trước.'),
        q_mcq(4, 'Đi lùi mà tắc đường thì thường là vì sao?',
              ['lùi sai thứ tự', 'đề bài sai', 'số quá to'], 'lùi sai thứ tự',
              'Đó là chuông báo động rất hữu ích.'),
        q_tf(5, 'Việc gì mặc sau thì cởi trước — đi lùi cũng thế.', True,
             'Đúng — cùng một luật.'),
    ],
)

# ═══ ③ B23 · GẮN TẠM HAI CHÂN ═══
B23 = bai(
    23, 'ĐẾM CHÂN — GẮN TẠM HAI CHÂN CHO TẤT CẢ',
    'LV 8.2a — Bài toán đếm chân: vẽ đủ đầu rồi gắn tạm hai chân.',
    video(
        ['Hiểu số đầu chính là số con vật.',
         'Gắn tạm hai chân cho mọi con rồi đếm.',
         'Tìm được số chân còn thừa.'],
        ['Đề bài: Trong sân có gà và chó, đếm được 5 cái đầu và 14 cái chân. Hỏi sau '
         'khi gắn tạm mỗi con hai chân thì còn thừa mấy chân?',
         'Mỗi con vật chỉ có một cái đầu',
         'Đếm được 5 cái đầu nên chắc chắn có 5 con vật.',
         'Gắn tạm cho mỗi con hai chân',
         'Gà có hai chân, chó có bốn chân, nên con nào cũng có ít nhất hai chân. Gắn '
         'tạm được 5 × 2 = 10 chân.',
         'Đếm số chân còn thừa',
         'Đề nói có 14 chân mà mới gắn 10 chân, nên còn thừa 14 − 10 = 4 chân.',
         'Đáp số: còn thừa 4 chân.',
         'Bốn chân thừa ấy là của mấy chú chó — bài sau sẽ tìm ra là mấy chú.'],
        ['Có bạn lấy 14 cái chân trừ 5 cái đầu được 9, rồi bảo có 9 con chó.',
         'Gợi ý 1: Chân và đầu có cùng loại không mà đem trừ cho nhau?',
         'Gợi ý 2: Cả sân chỉ có 5 con vật, làm sao riêng chó đã có tới 9 con được?',
         'Chữa: phải vẽ đủ 5 cái đầu, gắn tạm mỗi con hai chân, rồi mới đếm chân '
         'thừa.'],
        ['Vẽ ra giấy cùng con: năm vòng tròn làm đầu, rồi gắn que làm chân. Bài này '
         'vẽ ra thì dễ hơn nghĩ trong đầu rất nhiều.',
         'Bố mẹ hỏi: "Con nào cũng có ít nhất mấy chân?"'],
    ),
    [
        lt(1, 1, 'Đếm được 5 cái đầu thì trong sân có mấy con vật?',
           'Mỗi con chỉ có một cái đầu nên có 5 con vật.'),
        lt(2, 1, 'Gà có mấy chân?', 'Gà có 2 chân.'),
        lt(3, 1, 'Gắn tạm mỗi con hai chân, có 5 con thì gắn được mấy chân?',
           'Lấy 5 × 2 = 10 chân.'),
        lt(4, 2, 'Có 5 đầu và 14 chân. Sau khi gắn tạm mỗi con hai chân thì còn thừa '
                 'mấy chân?',
           'Gắn được 10 chân, còn thừa 14 − 10 = 4 chân.'),
        lt(5, 2, 'Vì sao gắn tạm cho mỗi con đúng hai chân?',
           'Vì gà hai chân, chó bốn chân, nên con nào cũng có ít nhất hai chân.'),
        lt(6, 2, 'Có 4 đầu và 10 chân. Gắn tạm được mấy chân, và còn thừa mấy chân?',
           'Gắn được 4 × 2 = 8 chân, còn thừa 10 − 8 = 2 chân.'),
        lt(7, 3, 'Có 6 đầu và 16 chân. Gắn tạm được mấy chân, và còn thừa mấy chân?',
           'Gắn được 6 × 2 = 12 chân, còn thừa 16 − 12 = 4 chân.'),
        lt(8, 3, 'Có bạn lấy 14 cái chân trừ 5 cái đầu được 9 rồi bảo có 9 con chó. '
                 'Nói xem chỗ ấy vô lý ở đâu.',
           'Chân và đầu khác loại nhau nên không trừ cho nhau được. Với lại cả sân '
           'chỉ có 5 con vật, không thể riêng chó đã 9 con.'),
    ] + [
        q_tf(1, 'Số đầu chính là số con vật.', True,
             'Đúng — con nào cũng chỉ có một cái đầu.'),
        q_mcq(2, 'Có 5 đầu, gắn tạm mỗi con hai chân thì được mấy chân?',
              ['10', '7', '14', '5'], '10', 'Năm con, mỗi con hai chân.'),
        q_mcq(3, 'Có 5 đầu và 14 chân thì còn thừa mấy chân?',
              ['4', '9', '24', '2'], '4', 'Mười bốn bớt mười.'),
        q_tf(4, 'Có thể lấy số chân trừ số đầu.', False,
             'Sai. Chân và đầu khác loại nhau.'),
        q_tf(5, 'Gắn tạm hai chân vì con nào cũng có ít nhất hai chân.', True,
             'Đúng — đó là lý do chọn con số hai.'),
    ],
)

# ═══ ④ B61 · CHÂN THỪA CHIA THÀNH CẶP ═══
B61 = bai(
    61, 'CHÂN THỪA CHIA THÀNH TỪNG CẶP',
    'LV 8.2b — Bài toán đếm chân: từ chân thừa ra số con bốn chân.',
    video(
        ['Hiểu mỗi chú chó còn thiếu đúng hai chân sau khi gắn tạm.',
         'Chia chân thừa thành từng cặp để ra số chó.',
         'Thử lại bằng cách cộng chân của tất cả các con.'],
        ['Đề bài: Trong sân có 5 cái đầu và 14 cái chân. Gắn tạm mỗi con hai chân thì '
         'còn thừa 4 chân. Hỏi có mấy con gà, mấy con chó?',
         'Chân thừa là của ai',
         'Chó có bốn chân mà mới được gắn hai, nên mỗi chú chó còn thiếu đúng hai '
         'chân nữa.',
         'Chia chân thừa thành từng cặp',
         'Còn 4 chân thừa, chia thành 4 : 2 = 2 cặp. Mỗi cặp gắn cho một chú chó.',
         'Vậy có 2 con chó',
         'Còn lại 5 − 2 = 3 con chỉ có hai chân, đó là gà.',
         'Thử lại cho chắc',
         'Gà có 3 × 2 = 6 chân. Chó có 2 × 4 = 8 chân. Cộng lại 6 + 8 = 14 chân, khớp '
         'đúng đề bài.',
         'Đáp số: 3 con gà và 2 con chó.',
         'Chân thừa luôn chia thành từng cặp, vì mỗi chú chó thiếu đúng hai chân.'],
        ['Có bạn thấy thừa 4 chân rồi bảo luôn là có 4 con chó.',
         'Gợi ý 1: Mỗi chú chó còn thiếu mấy chân sau khi đã gắn tạm hai chân?',
         'Gợi ý 2: Bốn chân thừa gắn được cho mấy chú, nếu mỗi chú cần hai chân?',
         'Chữa: mỗi chú chó cần một CẶP hai chân, nên 4 chân thừa chỉ gắn được cho 2 '
         'chú.'],
        ['Sau khi giải xong, cùng con cộng chân của tất cả các con vật xem có khớp đề '
         'không — bước thử lại này bắt được gần hết lỗi.',
         'Bố mẹ hỏi: "Mỗi chú chó còn thiếu mấy chân?"'],
    ),
    [
        lt(1, 1, 'Chó có mấy chân?', 'Chó có 4 chân.'),
        lt(2, 1, 'Chó đã được gắn tạm hai chân. Còn thiếu mấy chân nữa?',
           'Chó có bốn chân, mà mới gắn hai, nên còn thiếu 4 − 2 = 2 chân.'),
        lt(3, 1, 'Còn 4 chân thừa, chia thành từng cặp thì được mấy cặp?',
           'Lấy 4 : 2 = 2 cặp.'),
        lt(4, 2, 'Có 5 đầu, 14 chân, sau khi gắn tạm còn thừa 4 chân. Có mấy con chó?',
           'Bốn chân thừa chia thành 2 cặp, mỗi cặp một chú chó, nên có 2 con chó.'),
        lt(5, 2, 'Có 5 con vật, trong đó 2 con là chó. Có mấy con gà?',
           'Lấy 5 − 2 = 3 con gà.'),
        lt(6, 2, 'Có 3 con gà và 2 con chó. Thử lại xem tất cả có mấy chân?',
           'Gà có 3 × 2 = 6 chân, chó có 2 × 4 = 8 chân, cộng lại 6 + 8 = 14 chân.'),
        lt(7, 3, 'Có 4 đầu và 10 chân. Hỏi mấy con gà, mấy con chó?',
           'Gắn tạm được 8 chân, còn thừa 10 − 8 = 2 chân, tức một cặp nên có 1 con '
           'chó. Còn lại 4 − 1 = 3 con gà.'),
        lt(8, 3, 'Có 6 đầu và 16 chân. Hỏi mấy con gà, mấy con chó, và thử lại được '
                 'mấy chân?',
           'Gắn tạm được 12 chân, thừa 4 chân tức hai cặp nên có 2 con chó. Còn lại '
           '6 − 2 = 4 con gà. Thử lại: 4 × 2 = 8 chân cộng 2 × 4 = 8 chân, được 16 '
           'chân.'),
    ] + [
        q_tf(1, 'Chân thừa luôn chia thành từng cặp.', True,
             'Đúng — mỗi chú chó thiếu đúng hai chân.'),
        q_mcq(2, 'Thừa 4 chân thì có mấy con chó?', ['2', '4', '1', '8'], '2',
              'Bốn chân là hai cặp.'),
        q_mcq(3, 'Có 5 con, trong đó 2 con chó. Có mấy con gà?',
              ['3', '7', '2', '5'], '3', 'Năm bớt hai.'),
        q_tf(4, 'Ba con gà và hai con chó có tất cả 14 chân.', True,
             'Đúng — sáu chân gà cộng tám chân chó.'),
        q_tf(5, 'Tìm xong số gà số chó thì khỏi thử lại.', False,
             'Sai. Phải cộng chân của tất cả xem có khớp đề không.'),
    ],
)

# ═══ ⑤ B24 · CÂY VÀ KHOẢNG ═══
B24 = bai(
    24, 'CÂY VÀ KHOẢNG — LUẬT BÀN TAY',
    'LV 8.4a — Bài toán trồng cây: phân biệt số cây và số khoảng.',
    video(
        ['Phân biệt số cây và số khoảng giữa các cây.',
         'Nhớ luật bàn tay: trồng cả hai đầu thì số cây bằng số khoảng cộng một.',
         'Tính được chiều dài hàng cây.'],
        ['Đề bài: Một lối đi trồng 5 cây, cây nọ cách cây kia 2 mét, trồng ở cả hai '
         'đầu. Hỏi lối đi dài bao nhiêu mét?',
         'Xòe bàn tay ra mà đếm',
         'Bàn tay có 5 ngón nhưng chỉ có 4 kẽ. Ngón là cây, kẽ là khoảng.',
         'Số khoảng ít hơn số cây đúng một',
         'Trồng 5 cây thì chỉ có 5 − 1 = 4 khoảng.',
         'Chiều dài đi với KHOẢNG, không đi với CÂY',
         'Mỗi khoảng 2 mét, mà có 4 khoảng, nên lối đi dài 2 × 4 = 8 mét.',
         'Đáp số: 8 mét.',
         'Nhân với số cây thì ra mười mét — sai, vì cây chỉ đứng ở các mốc chứ không '
         'tạo nên chiều dài.'],
        ['Có bạn nhân luôn khoảng cách với số cây, được mười mét.',
         'Gợi ý 1: Xòe bàn tay ra xem: năm ngón thì mấy kẽ?',
         'Gợi ý 2: Thứ tạo nên chiều dài là ngón tay hay là kẽ tay?',
         'Chữa: chiều dài đi với khoảng. Có 4 khoảng nên lối đi dài 2 × 4 = 8 mét.'],
        ['Xòe bàn tay ra đếm cùng con — năm ngón bốn kẽ. Bài này chỉ cần nhớ đúng một '
         'hình ảnh ấy là làm được.',
         'Bố mẹ hỏi: "Đề đang hỏi CÂY hay hỏi KHOẢNG?"'],
    ),
    [
        lt(1, 1, 'Bàn tay có 5 ngón thì có mấy kẽ?', 'Năm ngón thì có 4 kẽ.'),
        lt(2, 1, 'Trồng 5 cây ở cả hai đầu thì có mấy khoảng?',
           'Số khoảng ít hơn số cây đúng một: 5 − 1 = 4 khoảng.'),
        lt(3, 1, 'Có 4 khoảng, mỗi khoảng 2 mét. Lối đi dài mấy mét?',
           'Lấy 2 × 4 = 8 mét.'),
        lt(4, 2, 'Trồng 6 cây ở cả hai đầu thì có mấy khoảng?',
           'Lấy 6 − 1 = 5 khoảng.'),
        lt(5, 2, 'Chiều dài lối đi đi với cái gì?',
           'Chiều dài đi với số khoảng, vì cây chỉ đứng ở các mốc.'),
        lt(6, 2, 'Trồng 8 cây cách nhau 3 mét ở cả hai đầu. Có mấy khoảng, và lối đi '
                 'dài mấy mét?',
           'Có 8 − 1 = 7 khoảng. Lối đi dài 3 × 7 = 21 mét.'),
        lt(7, 3, 'Trồng 5 cây cách nhau 2 mét. Có bạn tính lối đi dài mười mét. Bạn ấy '
                 'sai ở đâu?',
           'Bạn ấy nhân với số cây. Phải nhân với số khoảng, mà số khoảng chỉ có 4.'),
        lt(8, 3, 'Trồng 10 cây cách nhau 4 mét ở cả hai đầu. Có mấy khoảng, và lối đi '
                 'dài mấy mét?',
           'Có 10 − 1 = 9 khoảng. Lối đi dài 4 × 9 = 36 mét.'),
    ] + [
        q_tf(1, 'Trồng cả hai đầu thì số cây bằng số khoảng cộng một.', True,
             'Đúng — như bàn tay năm ngón bốn kẽ.'),
        q_mcq(2, 'Trồng 5 cây ở cả hai đầu thì có mấy khoảng?',
              ['4', '5', '6', '10'], '4', 'Ít hơn số cây đúng một.'),
        q_mcq(3, 'Năm cây cách nhau 2 mét thì lối đi dài mấy mét?',
              ['8', '10', '4', '12'], '8', 'Nhân với số khoảng.'),
        q_tf(4, 'Chiều dài lối đi tính bằng cách nhân với số cây.', False,
             'Sai. Phải nhân với số khoảng.'),
        q_tf(5, 'Bàn tay 5 ngón có 4 kẽ.', True, 'Đúng — xòe tay ra là thấy.'),
    ],
)

# ═══ ⑥ B62 · BIẾT CHIỀU DÀI, TÌM SỐ CÂY ═══
B62 = bai(
    62, 'BIẾT CHIỀU DÀI, TÌM SỐ CÂY',
    'LV 8.4b — Bài toán trồng cây ngược: từ chiều dài ra số cây.',
    video(
        ['Nhận ra bài ngược của bài trồng cây.',
         'Chia chiều dài cho khoảng cách để ra số khoảng.',
         'Cộng thêm một để ra số cây.'],
        ['Đề bài: Trồng cây dọc một đoạn đường dài 15 mét, cây nọ cách cây kia 3 mét, '
         'trồng ở cả hai đầu. Hỏi trồng được bao nhiêu cây?',
         'Bài này ngược với bài trước',
         'Bài trước biết số cây rồi hỏi chiều dài. Bài này biết chiều dài rồi hỏi số '
         'cây.',
         'Tìm số khoảng trước đã',
         'Chiều dài đi với khoảng, nên lấy 15 : 3 = 5 khoảng.',
         'Số cây nhiều hơn số khoảng đúng một',
         'Có 5 khoảng thì trồng được 5 + 1 = 6 cây.',
         'Thử lại cho chắc',
         'Sáu cây có năm khoảng, mỗi khoảng ba mét: 3 × 5 = 15 mét, khớp đúng đề bài.',
         'Đáp số: 6 cây.',
         'Chia ra được số KHOẢNG chứ chưa phải số cây — quên cộng một là mất một cây '
         'ở đầu đường.'],
        ['Có bạn chia xong là ghi luôn đáp số, quên mất bước cộng một.',
         'Gợi ý 1: Phép chia chiều dài cho khoảng cách ra số gì — số cây hay số '
         'khoảng?',
         'Gợi ý 2: Vẽ đoạn đường ra rồi đánh dấu các mốc xem, có phải một đầu đường '
         'bị trống trơn không?',
         'Chữa: chia ra số khoảng, rồi phải cộng thêm một mới ra số cây.'],
        ['Đi bộ cùng con dọc một hàng cột điện rồi hỏi: có mấy cột, có mấy khoảng — '
         'hai con số ấy luôn lệch nhau đúng một.',
         'Bố mẹ hỏi: "Con chia ra số khoảng rồi, đã cộng một chưa?"'],
    ),
    [
        lt(1, 1, 'Tính 15 : 3.', 'Lấy 15 : 3 = 5.'),
        lt(2, 1, 'Đường dài 15 mét, cây cách nhau 3 mét. Có mấy khoảng?',
           'Lấy 15 : 3 = 5 khoảng.'),
        lt(3, 1, 'Có 5 khoảng, trồng cả hai đầu. Trồng được mấy cây?',
           'Số cây nhiều hơn số khoảng một: 5 + 1 = 6 cây.'),
        lt(4, 2, 'Đường dài 12 mét, cây cách nhau 3 mét, trồng cả hai đầu. Trồng được '
                 'mấy cây?',
           'Có 12 : 3 = 4 khoảng, nên trồng được 4 + 1 = 5 cây.'),
        lt(5, 2, 'Phép chia chiều dài cho khoảng cách cho ra số gì?',
           'Nó cho ra số khoảng, chứ chưa phải số cây.'),
        lt(6, 2, 'Đường dài 20 mét, cây cách nhau 4 mét, trồng cả hai đầu. Có mấy '
                 'khoảng và mấy cây?',
           'Có 20 : 4 = 5 khoảng, nên trồng được 5 + 1 = 6 cây.'),
        lt(7, 3, 'Có bạn tính đường dài 12 mét cách nhau 3 mét rồi ghi trồng được 4 '
                 'cây. Cho biết bạn ấy sai ở đâu và số đúng là mấy.',
           'Bốn là số khoảng chứ chưa phải số cây. Trồng cả hai đầu nên phải cộng một, '
           'được 5 cây.'),
        lt(8, 3, 'Đường dài 24 mét, cây cách nhau 4 mét, trồng cả hai đầu. Trồng được '
                 'mấy cây, và thử lại chiều dài được bao nhiêu mét?',
           'Có 24 : 4 = 6 khoảng nên trồng 6 + 1 = 7 cây. Thử lại: 4 × 6 = 24 mét.'),
    ] + [
        q_tf(1, 'Chia chiều dài cho khoảng cách thì ra số khoảng.', True,
             'Đúng — chưa phải số cây.'),
        q_mcq(2, 'Đường dài 15 mét, cách 3 mét, trồng cả hai đầu. Mấy cây?',
              ['6', '5', '4', '45'], '6', 'Năm khoảng cộng một.'),
        q_mcq(3, 'Đường dài 12 mét, cách 3 mét, trồng cả hai đầu. Mấy cây?',
              ['5', '4', '3', '36'], '5', 'Bốn khoảng cộng một.'),
        q_tf(4, 'Chia xong là ra ngay số cây.', False,
             'Sai. Chia ra số khoảng, còn phải cộng một nữa.'),
        q_tf(5, 'Quên cộng một thì mất một cây ở đầu đường.', True,
             'Đúng — vẽ ra là thấy ngay chỗ trống.'),
    ],
)

# ═══ ⑦ B25 · VẼ THANG XẾP THỨ TỰ ═══
B25 = bai(
    25, 'VẼ THANG XẾP THỨ TỰ — AI TRÊN, AI DƯỚI',
    'LV 8.4c — Suy luận: xếp thứ tự nhiều đối tượng từ các manh mối hơn kém.',
    video(
        ['Xếp được thứ tự ba đối tượng từ hai manh mối.',
         'Vẽ thang rồi đọc thứ tự trên thang.',
         'Rút ra được điều đề bài không nói thẳng.'],
        ['Đề bài: Voi nặng hơn Gấu. Gấu nặng hơn Thỏ. Hỏi ai nặng nhất, ai nhẹ nhất, '
         'và Voi có nặng hơn Thỏ không?',
         'Vẽ một chiếc thang rồi xếp từng bạn',
         'Mỗi manh mối xếp được một bạn. Voi nặng hơn Gấu nên Voi đứng trên Gấu.',
         'Xếp tiếp theo manh mối thứ hai',
         'Gấu nặng hơn Thỏ nên Thỏ đứng dưới Gấu. Thang thành Voi, Gấu, Thỏ từ trên '
         'xuống.',
         'Đọc thang thì thấy cả điều đề không nói thẳng',
         'Voi đứng trên cùng, Thỏ đứng dưới cùng, nên Voi nặng hơn Thỏ.',
         'Đáp số: Voi nặng nhất, Thỏ nhẹ nhất, và Voi nặng hơn Thỏ.',
         'Đề chỉ cho hai manh mối mà chiếc thang trả lời được ba câu hỏi.'],
        ['Có bạn bảo đề không nói gì về Voi với Thỏ nên không kết luận được.',
         'Gợi ý 1: Vẽ thang ra rồi nhìn xem Voi đứng đâu, Thỏ đứng đâu.',
         'Gợi ý 2: Voi trên cùng, Thỏ dưới cùng thì ai nặng hơn?',
         'Chữa: thang cho biết cả những cặp mà đề không nói thẳng. Voi nặng hơn Thỏ.'],
        ['Xếp cả nhà theo chiều cao rồi hỏi con ai cao nhất, ai thấp nhất — chiếc '
         'thang bằng người thật.',
         'Bố mẹ hỏi: "Con vẽ thang ra chưa?"'],
    ),
    [
        lt(1, 1, 'Voi nặng hơn Gấu. Trong thang thì ai đứng trên?',
           'Voi nặng hơn nên Voi đứng trên Gấu.'),
        lt(2, 1, 'Voi nặng hơn Gấu, Gấu nặng hơn Thỏ. Ai nặng nhất?',
           'Thang xếp từ trên xuống là Voi, Gấu, Thỏ, nên Voi nặng nhất.'),
        lt(3, 1, 'Voi nặng hơn Gấu, Gấu nặng hơn Thỏ. Ai nhẹ nhất?',
           'Thỏ đứng dưới cùng thang nên Thỏ nhẹ nhất.'),
        lt(4, 2, 'Voi nặng hơn Gấu, Gấu nặng hơn Thỏ. Voi có nặng hơn Thỏ không?',
           'Voi đứng trên cùng còn Thỏ đứng dưới cùng, nên Voi nặng hơn Thỏ.'),
        lt(5, 2, 'An cao hơn Bình, Bình cao hơn Cường. Ai cao nhất?',
           'Thang xếp từ trên xuống là An, Bình, Cường, nên An cao nhất.'),
        lt(6, 2, 'Lan chạy nhanh hơn Mai, Mai chạy nhanh hơn Hoa. Ai đứng giữa thang?',
           'Thang xếp từ nhanh nhất xuống là Lan, Mai, Hoa, nên Mai đứng giữa.'),
        lt(7, 3, 'Nam nhiều bi hơn Việt, Việt nhiều bi hơn Hùng. Ai đứng trên cùng và '
                 'ai đứng dưới cùng thang?',
           'Thang xếp từ trên xuống là Nam, Việt, Hùng.'),
        lt(8, 3, 'Voi nặng hơn Gấu, Gấu nặng hơn Thỏ, Thỏ nặng hơn Chuột. Ai nặng nhất '
                 'và ai nhẹ nhất?',
           'Thang xếp từ trên xuống là Voi, Gấu, Thỏ, Chuột.'),
    ] + [
        q_tf(1, 'Đố kiểu "ai hơn ai" thì vẽ thang ra mà xếp.', True,
             'Đúng — nhìn thang là đọc được cả thứ tự.'),
        q_mcq(2, 'Voi nặng hơn Gấu, Gấu nặng hơn Thỏ. Ai nặng nhất?',
              ['Voi', 'Gấu', 'Thỏ'], 'Voi', 'Voi đứng trên cùng thang.'),
        q_tf(3, 'Đề không nói Voi nặng hơn Thỏ nên không kết luận được.', False,
             'Sai. Nhìn thang là thấy ngay Voi nặng hơn Thỏ.'),
        q_mcq(4, 'An cao hơn Bình, Bình cao hơn Cường. Ai thấp nhất?',
              ['Cường', 'An', 'Bình'], 'Cường', 'Cường đứng dưới cùng thang.'),
        q_tf(5, 'Mỗi manh mối xếp được một bạn vào thang.', True,
             'Đúng — nên phải dùng đủ mọi manh mối.'),
    ],
)

# ═══ ⑧ B63 · BẢNG LOẠI TRỪ ═══
B63 = bai(
    63, 'BẢNG LOẠI TRỪ — ĐÁNH DẤU RỒI GẠCH',
    'LV 8.4d — Suy luận: giải đố "ai với cái gì" bằng bảng loại trừ.',
    video(
        ['Kẻ được bảng loại trừ cho câu đố "ai với cái gì".',
         'Đánh dấu từ manh mối chắc nhất rồi gạch cùng hàng cùng cột.',
         'Đọc ra đáp án từ hàng chỉ còn một ô trống.'],
        ['Đề bài: Ba bạn Mai, Đào, Cúc cầm ba bông hoa hồng, sen, cúc. Biết Mai không '
         'cầm hoa hồng, Đào cầm hoa sen. Hỏi mỗi bạn cầm hoa gì?',
         'Kẻ bảng ba hàng ba cột',
         'Mỗi hàng một bạn, mỗi cột một bông hoa.',
         'Đánh dấu từ manh mối chắc nhất',
         'Đào cầm hoa sen là manh mối chắc chắn, nên đánh dấu đúng ô ấy.',
         'Gạch cả hàng và cả cột của ô vừa đánh dấu',
         'Một bạn chỉ cầm một bông, một bông chỉ có một chủ. Nên gạch hết hàng Đào và '
         'cột sen.',
         'Dùng nốt manh mối còn lại',
         'Mai không cầm hoa hồng nên gạch ô ấy. Hàng Mai chỉ còn ô hoa cúc, vậy Mai '
         'cầm hoa cúc.',
         'Hàng cuối chỉ còn một ô trống',
         'Còn lại Cúc cầm hoa hồng.',
         'Đáp số: Mai cầm hoa cúc, Đào cầm hoa sen, Cúc cầm hoa hồng.',
         'Bạn tên Cúc lại không cầm hoa cúc — đề trêu mình đấy, nhưng bảng thì không '
         'bị lừa.'],
        ['Có bạn mới biết mình không cầm hoa hồng đã vội chốt là cầm hoa sen.',
         'Gợi ý 1: Loại được một ô thì còn mấy ô có thể? Đã đủ để chốt chưa?',
         'Gợi ý 2: Hoa sen đã có chủ rồi đấy, xem lại manh mối thứ hai.',
         'Chữa: phải dùng đủ mọi manh mối trên bảng. Hàng nào chỉ còn một ô trống thì '
         'ô ấy mới là đáp án.'],
        ['Kẻ bảng ra giấy rồi cùng con đánh dấu và gạch — nhìn bảng đầy dần lên là bé '
         'hiểu ngay cách suy luận này.',
         'Bố mẹ hỏi: "Hàng này còn mấy ô trống?"'],
    ),
    [
        lt(1, 1, 'Đào cầm hoa sen. Trong bảng thì đánh dấu vào ô nào?',
           'Đánh dấu ô nằm ở hàng Đào và cột sen.'),
        lt(2, 1, 'Đánh dấu xong một ô thì phải gạch những ô nào?',
           'Gạch cả hàng và cả cột của ô vừa đánh dấu.'),
        lt(3, 1, 'Vì sao phải gạch cả hàng và cả cột?',
           'Vì một bạn chỉ cầm một bông, và một bông chỉ có một chủ.'),
        lt(4, 2, 'Đào cầm hoa sen, Mai không cầm hoa hồng. Mai cầm hoa gì?',
           'Cột sen đã bị gạch, ô hồng cũng bị gạch, nên hàng Mai chỉ còn ô hoa cúc.'),
        lt(5, 2, 'Mai cầm hoa cúc, Đào cầm hoa sen. Cúc cầm hoa gì?',
           'Hai bông kia đã có chủ, nên Cúc cầm hoa hồng.'),
        lt(6, 2, 'Có bạn mới biết mình không cầm hoa hồng đã chốt luôn là cầm hoa sen. '
                 'Bạn ấy sai ở đâu?',
           'Bạn ấy mới loại được một ô đã vội chốt, chưa dùng hết manh mối.'),
        lt(7, 3, 'Ba bạn An, Bình, Cường nuôi chó, mèo, cá. Biết An nuôi cá, Bình '
                 'không nuôi chó. Bình nuôi con gì?',
           'Cột cá đã bị gạch vì An nuôi cá, ô chó cũng bị gạch, nên hàng Bình chỉ còn '
           'ô mèo.'),
        lt(8, 3, 'Vẫn ba bạn An, Bình, Cường nuôi chó, mèo, cá. An nuôi cá, Bình không '
                 'nuôi chó. Cho biết Bình nuôi con gì và Cường nuôi con gì.',
           'Hàng Bình chỉ còn ô mèo. Còn lại Cường nuôi chó.'),
    ] + [
        q_tf(1, 'Đánh dấu một ô thì gạch cả hàng và cả cột của ô ấy.', True,
             'Đúng — một bạn một bông, một bông một chủ.'),
        q_mcq(2, 'Đào cầm sen, Mai không cầm hồng. Mai cầm hoa gì?',
              ['cúc', 'sen', 'hồng'], 'cúc', 'Hàng Mai chỉ còn một ô trống.'),
        q_tf(3, 'Mới loại được một ô là chốt được đáp án.', False,
             'Sai. Phải dùng đủ mọi manh mối trên bảng.'),
        q_mcq(4, 'Hàng nào chỉ còn một ô trống thì sao?',
              ['ô ấy chính là đáp án', 'phải đoán thêm', 'bỏ qua hàng ấy'],
              'ô ấy chính là đáp án', 'Không cần đoán mò nữa.'),
        q_tf(5, 'Bảng loại trừ giúp kết luận mà không phải đoán mò.', True,
             'Đúng — mỗi kết luận đều có manh mối chống lưng.'),
    ],
)

MOI = [B22, B60, B23, B61, B24, B62, B25, B63]

SAU = {
    'DL:KSN2.B60': 'DL:KSN2.B22',
    'DL:KSN2.B61': 'DL:KSN2.B23',
    'DL:KSN2.B62': 'DL:KSN2.B24',
    'DL:KSN2.B63': 'DL:KSN2.B25',
}

MAY = ['máy chia 3', 'máy nhân 3', 'máy cộng 3']
AI_HON = ['Voi', 'Gấu', 'Thỏ']


def _o(gt, chon=None, nhan=None):
    """Một ô nhập. Chuỗi thì BẮT BUỘC kèm nút bấm — luật ô nhập số 1 của lớp 2."""
    d = {'value': gt}
    if chon:
        d['options'] = list(chon)
    if nhan:
        d['label'] = nhan
    return d


O_NHAP_MOI = {
 # ① B22 · đi lùi qua hai máy
 'DL:KSN2.B22#C1': {'value': 4},
 'DL:KSN2.B22#C2': {'parts': [_o('máy chia 3', MAY, 'máy ngược')]},
 'DL:KSN2.B22#C3': {'value': 4},
 'DL:KSN2.B22#C4': {'value': 6},
 'DL:KSN2.B22#C5': {'value': 5},
 'DL:KSN2.B22#C6': {'parts': [_o('máy chia', ['máy chia', 'máy cộng', 'máy trừ'],
                                 'đảo thành')]},
 'DL:KSN2.B22#C7': {'parts': [_o(5, nhan='số cần tìm'), _o(17, nhan='thử lại được')]},
 'DL:KSN2.B22#C8': {'value': 10},

 # ② B60 · thứ tự đi lùi
 'DL:KSN2.B60#C1': {'parts': [_o('máy nhân 2', ['máy nhân 2', 'máy cộng 3'],
                                 'máy làm sau cùng')]},
 'DL:KSN2.B60#C2': {'value': 8},
 'DL:KSN2.B60#C3': {'parts': [_o('máy nhân 2', ['máy nhân 2', 'máy cộng 3'],
                                 'lùi qua máy nào trước')]},
 'DL:KSN2.B60#C4': {'value': 5},
 'DL:KSN2.B60#C5': {'parts': [_o('lùi sai thứ tự',
                                 ['lùi sai thứ tự', 'đảo phép sai', 'không sai gì cả'],
                                 'sai ở đâu')]},
 'DL:KSN2.B60#C6': {'parts': [_o('máy cộng 5', ['máy cộng 5', 'máy nhân 2'],
                                 'lùi qua máy nào trước'),
                              _o(7, nhan='số cần tìm')]},
 'DL:KSN2.B60#C7': {'value': 11},
 'DL:KSN2.B60#C8': {'parts': [_o(6, nhan='số cần tìm'), _o(40, nhan='thử lại được')]},

 # ③ B23 · gắn tạm hai chân
 'DL:KSN2.B23#C1': {'value': 5},
 'DL:KSN2.B23#C2': {'value': 2},
 'DL:KSN2.B23#C3': {'value': 10},
 'DL:KSN2.B23#C4': {'value': 4},
 'DL:KSN2.B23#C5': {'parts': [_o('vì con nào cũng có ít nhất hai chân',
                                 ['vì con nào cũng có ít nhất hai chân',
                                  'vì hai là số chẵn'], 'vì sao')]},
 'DL:KSN2.B23#C6': {'parts': [_o(8, nhan='gắn được'), _o(2, nhan='còn thừa')]},
 'DL:KSN2.B23#C7': {'parts': [_o(12, nhan='gắn được'), _o(4, nhan='còn thừa')]},
 'DL:KSN2.B23#C8': {'parts': [
     _o('chân và đầu khác loại, và cả sân chỉ có 5 con',
        ['chân và đầu khác loại, và cả sân chỉ có 5 con', 'không sai gì cả'],
        'vô lý ở đâu')]},

 # ④ B61 · chân thừa chia thành cặp
 'DL:KSN2.B61#C1': {'value': 4},
 'DL:KSN2.B61#C2': {'value': 2},
 'DL:KSN2.B61#C3': {'value': 2},
 'DL:KSN2.B61#C4': {'value': 2},
 'DL:KSN2.B61#C5': {'value': 3},
 'DL:KSN2.B61#C6': {'value': 14},
 'DL:KSN2.B61#C7': {'parts': [_o(3, nhan='con gà'), _o(1, nhan='con chó')]},
 'DL:KSN2.B61#C8': {'parts': [_o(4, nhan='con gà'), _o(2, nhan='con chó'),
                              _o(16, nhan='thử lại mấy chân')]},

 # ⑤ B24 · cây và khoảng
 'DL:KSN2.B24#C1': {'value': 4},
 'DL:KSN2.B24#C2': {'value': 4},
 'DL:KSN2.B24#C3': {'value': 8},
 'DL:KSN2.B24#C4': {'value': 5},
 'DL:KSN2.B24#C5': {'parts': [_o('số khoảng', ['số khoảng', 'số cây'],
                                 'chiều dài đi với')]},
 'DL:KSN2.B24#C6': {'parts': [_o(7, nhan='số khoảng'), _o(21, nhan='dài mấy mét')]},
 'DL:KSN2.B24#C7': {'parts': [_o('nhân với số cây chứ không nhân với số khoảng',
                                 ['nhân với số cây chứ không nhân với số khoảng',
                                  'không sai gì cả'], 'sai ở đâu')]},
 'DL:KSN2.B24#C8': {'parts': [_o(9, nhan='số khoảng'), _o(36, nhan='dài mấy mét')]},

 # ⑥ B62 · biết chiều dài, tìm số cây
 'DL:KSN2.B62#C1': {'value': 5},
 'DL:KSN2.B62#C2': {'value': 5},
 'DL:KSN2.B62#C3': {'value': 6},
 'DL:KSN2.B62#C4': {'value': 5},
 'DL:KSN2.B62#C5': {'parts': [_o('số khoảng', ['số khoảng', 'số cây'], 'ra số gì')]},
 'DL:KSN2.B62#C6': {'parts': [_o(5, nhan='số khoảng'), _o(6, nhan='số cây')]},
 'DL:KSN2.B62#C7': {'parts': [_o('quên cộng một, đó mới là số khoảng',
                                 ['quên cộng một, đó mới là số khoảng',
                                  'không sai gì cả'], 'sai ở đâu'),
                              _o(5, nhan='số đúng')]},
 'DL:KSN2.B62#C8': {'parts': [_o(7, nhan='số cây'), _o(24, nhan='thử lại mấy mét')]},

 # ⑦ B25 · vẽ thang xếp thứ tự
 'DL:KSN2.B25#C1': {'parts': [_o('Voi', ['Voi', 'Gấu'], 'ai đứng trên')]},
 'DL:KSN2.B25#C2': {'parts': [_o('Voi', AI_HON, 'ai nặng nhất')]},
 'DL:KSN2.B25#C3': {'parts': [_o('Thỏ', AI_HON, 'ai nhẹ nhất')]},
 'DL:KSN2.B25#C4': {'parts': [_o('có', CO_KHONG, 'Voi có nặng hơn Thỏ không')]},
 'DL:KSN2.B25#C5': {'parts': [_o('An', ['An', 'Bình', 'Cường'], 'ai cao nhất')]},
 'DL:KSN2.B25#C6': {'parts': [_o('Mai', ['Lan', 'Mai', 'Hoa'], 'ai đứng giữa')]},
 'DL:KSN2.B25#C7': {'parts': [_o('Nam', ['Nam', 'Việt', 'Hùng'], 'trên cùng'),
                              _o('Hùng', ['Nam', 'Việt', 'Hùng'], 'dưới cùng')]},
 'DL:KSN2.B25#C8': {'parts': [
     _o('Voi', ['Voi', 'Gấu', 'Thỏ', 'Chuột'], 'nặng nhất'),
     _o('Chuột', ['Voi', 'Gấu', 'Thỏ', 'Chuột'], 'nhẹ nhất')]},

 # ⑧ B63 · bảng loại trừ
 'DL:KSN2.B63#C1': {'parts': [_o('hàng Đào cột sen',
                                 ['hàng Đào cột sen', 'hàng Mai cột sen'],
                                 'đánh dấu ô nào')]},
 'DL:KSN2.B63#C2': {'parts': [_o('cả hàng và cả cột của ô ấy',
                                 ['cả hàng và cả cột của ô ấy', 'chỉ ô bên cạnh'],
                                 'gạch những ô nào')]},
 'DL:KSN2.B63#C3': {'parts': [
     _o('vì một bạn chỉ cầm một bông, một bông chỉ một chủ',
        ['vì một bạn chỉ cầm một bông, một bông chỉ một chủ', 'vì cho bảng gọn'],
        'vì sao')]},
 'DL:KSN2.B63#C4': {'parts': [_o('cúc', ['cúc', 'sen', 'hồng'], 'Mai cầm hoa gì')]},
 'DL:KSN2.B63#C5': {'parts': [_o('hồng', ['hồng', 'sen', 'cúc'], 'Cúc cầm hoa gì')]},
 'DL:KSN2.B63#C6': {'parts': [_o('mới loại được một ô đã vội chốt',
                                 ['mới loại được một ô đã vội chốt',
                                  'không sai gì cả'], 'sai ở đâu')]},
 'DL:KSN2.B63#C7': {'parts': [_o('mèo', ['mèo', 'chó', 'cá'], 'Bình nuôi con gì')]},
 'DL:KSN2.B63#C8': {'parts': [_o('mèo', ['mèo', 'chó', 'cá'], 'Bình nuôi'),
                              _o('chó', ['mèo', 'chó', 'cá'], 'Cường nuôi')]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (22, 23, 24, 25)}
    moi_ = {f'DL:KSN2.B{n}' for n in (60, 61, 62, 63)}
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
        # "thám tử" và "vũ khí" là vỏ nhân vật của sách, cấm trong lời đọc video.
        # Tên chương thì giữ, nên chỉ soi phần THÂN bài.
        than = json.dumps({k: v for k, v in b.items() if k != 'tenChuong'},
                          ensure_ascii=False).lower()
        for tu in ('thám tử', 'vũ khí'):
            if tu in than:
                loi.append(f'{b["id"]}: còn chữ cấm "{tu}" trong thân bài')
    NEO = {'DL:KSN2.B22': '12 : 3 = 4', 'DL:KSN2.B60': '16 : 2 = 8',
           'DL:KSN2.B23': '14 − 10 = 4', 'DL:KSN2.B61': '4 : 2 = 2',
           'DL:KSN2.B24': '2 × 4 = 8', 'DL:KSN2.B62': '15 : 3 = 5',
           'DL:KSN2.B25': 'Voi, Gấu, Thỏ', 'DL:KSN2.B63': 'hàng Mai chỉ còn'}
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
