# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 7 · VƯƠNG QUỐC HÌNH HỌC — năm bài chữ thành mười bài video.

  · B26 gộp "nhận mặt hình bằng cạnh và đỉnh" với "đường kiến bò một vòng";
  · B27 gộp "đếm hình đơn" với "đếm hình GHÉP" — cái sau mới là chỗ bé sót;
  · B28 gộp "tâm và nan hoa" với "vì sao bánh xe phải tròn";
  · B29 gộp "hai loại khối, mỗi khối sáu mặt" với "hình dẹt khác khối cầm nắm được";
  · B30 gộp "luật ngồi" với "đếm theo tầng".

── SỐ NEO ──
    tam giác 3 cạnh 3 đỉnh   ·   tứ giác 4 cạnh 4 đỉnh
    3 + 4 + 5 = 12 xăng-ti-mét   → đường kiến bò một vòng
    băng 3 ô                 → 3 hình đơn; ghép được 3 hình nữa
    nan hoa bằng nhau        → tròn thật; trứng nhìn nghiêng là méo
    khối 6 mặt               → lập phương mặt vuông, hộp chữ nhật mặt chữ nhật
    tháp 4 + 1 = 5 khối      → đếm theo tầng, khối bị che vẫn đếm

⚠ Viết "xăng-ti-mét" chứ đừng viết tắt — máy đọc hai chữ cái thành tiếng Anh.

    python3 tools/hinh_hoc_lop2.py --xem
    python3 tools/hinh_hoc_lop2.py
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

TEN_CHUONG = 'Vương quốc hình học'
CHUONG = 7
CO_KHONG = ['có', 'không']
LOAI_HINH = ['hình tam giác', 'hình vuông', 'hình chữ nhật']
LOAI_KHOI = ['khối lập phương', 'khối hộp chữ nhật']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B26 · NHẬN MẶT HÌNH ═══
B26 = bai(
    26, 'NHẬN MẶT HÌNH — ĐẾM CẠNH, ĐẾM ĐỈNH',
    'HH 1.1a — Nhận dạng hình phẳng bằng số cạnh và số đỉnh.',
    video(
        ['Gọi đúng tên tam giác, tứ giác, hình vuông, hình chữ nhật.',
         'Đếm được số cạnh và số đỉnh của mỗi hình.',
         'Biết hình bị xoay nghiêng vẫn là chính nó.'],
        ['Đề bài: Cho biết hình tam giác có mấy cạnh mấy đỉnh, và một hình vuông đặt '
         'xoay nghiêng thì còn là hình vuông nữa không.',
         'Mỗi hình có một tấm danh thiếp',
         'Danh thiếp ấy là số cạnh và số đỉnh. Tam giác có 3 cạnh và 3 đỉnh.',
         'Bốn cạnh bốn đỉnh thì mang họ TỨ GIÁC',
         'Hình vuông có cả 4 cạnh bằng nhau. Hình chữ nhật có hai cạnh dài bằng nhau '
         'và hai cạnh ngắn bằng nhau. Cả hai đều là tứ giác.',
         'Hình bị xoay vẫn là chính nó',
         'Hình vuông đặt xoay nghiêng trông lạ mắt, nhưng đếm vẫn 4 cạnh bằng nhau và '
         '4 đỉnh, nên vẫn là hình vuông.',
         'Đáp số: tam giác có 3 cạnh 3 đỉnh, và hình vuông xoay nghiêng vẫn là hình '
         'vuông.',
         'Nhận hình bằng cách đếm cạnh đếm đỉnh, đừng tin dáng đứng.'],
        ['Có bạn thấy hình vuông đặt xoay nghiêng rồi gọi nó là hình thoi hay hình gì '
         'lạ lắm.',
         'Gợi ý 1: Con đếm xem hình ấy có mấy cạnh, mấy đỉnh.',
         'Gợi ý 2: Bốn cạnh có bằng nhau không? Nếu bằng nhau thì nó là hình gì?',
         'Chữa: xoay nghiêng không đổi được số cạnh số đỉnh, nên nó vẫn là hình '
         'vuông.'],
        ['Chỉ vào đồ vật quanh nhà rồi hỏi con hình gì — cửa sổ, mặt bàn, biển báo. '
         'Nhớ chỉ cả những cái đặt nghiêng.',
         'Bố mẹ hỏi: "Hình này mấy cạnh, mấy đỉnh?"'],
    ),
    [
        lt(1, 1, 'Hình tam giác có mấy cạnh?', 'Hình tam giác có 3 cạnh.'),
        lt(2, 1, 'Hình tam giác có mấy đỉnh?', 'Hình tam giác có 3 đỉnh.'),
        lt(3, 1, 'Hình vuông có mấy cạnh?', 'Hình vuông có 4 cạnh, và bốn cạnh ấy bằng '
                 'nhau.'),
        lt(4, 2, 'Hình có 4 cạnh và 4 đỉnh thì mang họ chung là gì?',
           'Mọi hình 4 cạnh 4 đỉnh đều mang họ tứ giác.'),
        lt(5, 2, 'Một hình vuông đặt xoay nghiêng thì còn là hình vuông không?',
           'Xoay nghiêng không đổi được số cạnh số đỉnh nên nó vẫn là hình vuông.'),
        lt(6, 2, 'Hình chữ nhật khác hình vuông ở chỗ nào?',
           'Hình vuông có cả bốn cạnh bằng nhau, còn hình chữ nhật chỉ có hai cạnh '
           'dài bằng nhau và hai cạnh ngắn bằng nhau.'),
        lt(7, 3, 'Một hình có 3 cạnh và một hình có 4 cạnh. Cộng số cạnh và số đỉnh '
                 'của cả hai hình thì được bao nhiêu?',
           'Số cạnh: 3 + 4 = 7. Số đỉnh cũng vậy: 3 + 4 = 7. Cộng cả hai được 14.'),
        lt(8, 3, 'Trong bốn hình: tam giác, hình vuông, hình chữ nhật, hình tứ giác '
                 'xiêu vẹo — có mấy hình mang họ tứ giác?',
           'Hình vuông, hình chữ nhật và hình xiêu vẹo đều 4 cạnh 4 đỉnh, nên có 3 '
           'hình mang họ tứ giác.'),
    ] + [
        q_tf(1, 'Hình tam giác có 3 cạnh và 3 đỉnh.', True,
             'Đúng — đó là tấm danh thiếp của nó.'),
        q_mcq(2, 'Hình có 4 cạnh 4 đỉnh mang họ gì?',
              ['tứ giác', 'tam giác', 'hình tròn'], 'tứ giác',
              'Kể cả hình xiêu vẹo cũng vậy.'),
        q_tf(3, 'Hình vuông đặt xoay nghiêng thì không còn là hình vuông.', False,
             'Sai. Đếm cạnh đếm đỉnh vẫn thế nên nó vẫn là hình vuông.'),
        q_mcq(4, 'Hình nào có cả bốn cạnh bằng nhau?',
              ['hình vuông', 'hình chữ nhật', 'hình tam giác'], 'hình vuông',
              'Hình chữ nhật chỉ có từng cặp bằng nhau.'),
        q_tf(5, 'Nhận hình thì nhìn dáng đứng là đủ.', False,
             'Sai. Phải đếm cạnh và đếm đỉnh.'),
    ],
)

# ═══ ② B64 · ĐƯỜNG KIẾN BÒ MỘT VÒNG ═══
B64 = bai(
    64, 'ĐƯỜNG KIẾN BÒ MỘT VÒNG — CỘNG ĐỦ CÁC CẠNH',
    'HH 1.1b — Tổng độ dài các cạnh, tiền thân chu vi lớp 3.',
    video(
        ['Hiểu đường kiến bò một vòng là tổng độ dài các cạnh.',
         'Cộng đủ các cạnh, không sót cạnh nào.',
         'Làm được với cả hình vuông và hình chữ nhật.'],
        ['Đề bài: Một hình tam giác có ba cạnh dài 3 xăng-ti-mét, 4 xăng-ti-mét và 5 '
         'xăng-ti-mét. Chú kiến bò đúng một vòng quanh hình. Hỏi chú kiến bò được bao '
         'nhiêu xăng-ti-mét?',
         'Thả chú kiến bò quanh mép hình',
         'Chú kiến đi hết cạnh này sang cạnh kia, đủ một vòng rồi về chỗ cũ.',
         'Quãng đường bằng tổng độ dài các cạnh',
         'Cộng đủ cả ba cạnh: 3 + 4 + 5 = 12.',
         'Đáp số: 12 xăng-ti-mét.',
         'Lên lớp 3, quãng đường kiến bò một vòng sẽ có tên riêng là chu vi.'],
        ['Có bạn cộng thiếu một cạnh, vì cạnh ấy nằm khuất phía dưới hình.',
         'Gợi ý 1: Con đếm xem hình có mấy cạnh, rồi đếm xem đã cộng mấy số.',
         'Gợi ý 2: Chú kiến phải về đúng chỗ xuất phát mới là một vòng.',
         'Chữa: cộng đủ cả ba cạnh, không sót cạnh nào.'],
        ['Cho con lấy sợi dây quấn quanh mép quyển sách rồi kéo thẳng ra đo — đó chính '
         'là đường kiến bò một vòng.',
         'Bố mẹ hỏi: "Con đã cộng đủ mấy cạnh rồi?"'],
    ),
    [
        lt(1, 1, 'Tính 3 + 4 + 5.', 'Lấy 3 + 4 + 5 = 12.'),
        lt(2, 1, 'Tam giác có ba cạnh 3, 4 và 5 xăng-ti-mét. Chú kiến bò một vòng được '
                 'mấy xăng-ti-mét?',
           'Cộng đủ ba cạnh: 3 + 4 + 5 = 12.'),
        lt(3, 1, 'Hình vuông có cạnh 5 xăng-ti-mét. Chú kiến bò một vòng được mấy '
                 'xăng-ti-mét?',
           'Bốn cạnh đều bằng 5, nên 5 + 5 + 5 + 5 = 20.'),
        lt(4, 2, 'Hình chữ nhật có hai cạnh dài 6 xăng-ti-mét và hai cạnh ngắn 3 '
                 'xăng-ti-mét. Chú kiến bò một vòng được mấy xăng-ti-mét?',
           'Cộng đủ bốn cạnh: 6 + 3 + 6 + 3 = 18.'),
        lt(5, 2, 'Đường kiến bò một vòng bằng cái gì?',
           'Nó bằng tổng độ dài của tất cả các cạnh.'),
        lt(6, 2, 'Tam giác có ba cạnh 2, 6 và 7 xăng-ti-mét. Chú kiến bò một vòng được '
                 'mấy xăng-ti-mét?',
           'Cộng đủ ba cạnh: 2 + 6 + 7 = 15.'),
        lt(7, 3, 'Hình vuông cạnh 4 xăng-ti-mét và hình vuông cạnh 6 xăng-ti-mét. Chú '
                 'kiến bò một vòng quanh mỗi hình được mấy xăng-ti-mét?',
           'Hình nhỏ: 4 + 4 + 4 + 4 = 16. Hình to: 6 + 6 + 6 + 6 = 24.'),
        lt(8, 3, 'Chú kiến bò một vòng quanh hình chữ nhật được 20 xăng-ti-mét. Hai '
                 'cạnh dài đều 7 xăng-ti-mét. Mỗi cạnh ngắn dài mấy xăng-ti-mét?',
           'Hai cạnh dài hết 7 + 7 = 14. Còn lại 20 − 14 = 6 cho hai cạnh ngắn, nên '
           'mỗi cạnh ngắn là 3.'),
    ] + [
        q_tf(1, 'Đường kiến bò một vòng bằng tổng độ dài các cạnh.', True,
             'Đúng — lên lớp 3 nó tên là chu vi.'),
        q_mcq(2, 'Tam giác ba cạnh 3, 4, 5 thì kiến bò được mấy xăng-ti-mét?',
              ['12', '9', '15', '7'], '12', 'Cộng đủ ba cạnh.'),
        q_mcq(3, 'Hình vuông cạnh 5 thì kiến bò được mấy xăng-ti-mét?',
              ['20', '10', '25', '15'], '20', 'Bốn cạnh đều bằng nhau.'),
        q_tf(4, 'Hình chữ nhật chỉ cần cộng hai cạnh là đủ.', False,
             'Sai. Phải cộng đủ cả bốn cạnh.'),
        q_tf(5, 'Chú kiến phải về đúng chỗ xuất phát mới là một vòng.', True,
             'Đúng — thiếu một cạnh là chưa đủ vòng.'),
    ],
)

# ═══ ③ B27 · ĐÁNH SỐ MẢNH, ĐẾM HÌNH ĐƠN ═══
B27 = bai(
    27, 'ĐÁNH SỐ MẢNH RỒI ĐẾM HÌNH ĐƠN',
    'HH 2.1a — Đếm hình trong hình ghép: đánh số mảnh và đếm hình đơn.',
    video(
        ['Đánh số từng mảnh nhỏ của một hình ghép.',
         'Đếm được các hình đơn, tức từng mảnh một.',
         'Biết trong hình ghép còn có cả hình to ẩn mình.'],
        ['Đề bài: Một hình chữ nhật được chia thành 3 ô vuông nhỏ xếp thành hàng '
         'ngang. Hỏi có mấy hình đơn, tức mấy mảnh nhỏ?',
         'Đánh số từng mảnh',
         'Viết số 1, 2, 3 vào ba mảnh nhỏ. Đây là bước điểm danh, làm rồi thì không '
         'sót mảnh nào.',
         'Đếm hình đơn',
         'Mỗi mảnh nhỏ là một hình vuông, mà có 3 mảnh, nên có 3 hình đơn.',
         'Đáp số: 3 hình đơn.',
         'Nhưng đếm hình đơn mới xong một nửa việc — trong hình còn hình to ẩn mình, '
         'bài sau sẽ lùng ra.'],
        ['Có bạn đếm luôn bằng mắt mà không đánh số, rồi lúc thì sót mảnh lúc thì đếm '
         'trùng.',
         'Gợi ý 1: Đánh số vào từng mảnh trước đã, như điểm danh vậy.',
         'Gợi ý 2: Đánh số rồi thì đếm số cuối cùng là biết có mấy mảnh.',
         'Chữa: đánh số trước, đếm sau. Làm có thứ tự thì không sót không trùng.'],
        ['Vẽ một hình chữ nhật rồi kẻ vài đường chia cho con đánh số và đếm — trò này '
         'chơi được cả buổi mà không chán.',
         'Bố mẹ hỏi: "Con đánh số các mảnh chưa?"'],
    ),
    [
        lt(1, 1, 'Một hình chữ nhật chia thành 3 ô vuông nhỏ. Có mấy hình đơn?',
           'Mỗi mảnh nhỏ là một hình đơn, mà có 3 mảnh.'),
        lt(2, 1, 'Việc đầu tiên khi đếm hình trong hình ghép là gì?',
           'Đánh số từng mảnh nhỏ, như điểm danh vậy.'),
        lt(3, 1, 'Một tam giác to chia thành 2 tam giác nhỏ. Có mấy hình đơn?',
           'Có 2 mảnh nhỏ nên có 2 hình đơn.'),
        lt(4, 2, 'Một hình vuông chia thành 4 ô vuông nhỏ bằng nhau. Có mấy hình đơn?',
           'Có 4 mảnh nhỏ nên có 4 hình đơn.'),
        lt(5, 2, 'Vì sao phải đánh số các mảnh trước khi đếm?',
           'Để không sót mảnh nào và cũng không đếm trùng mảnh nào.'),
        lt(6, 2, 'Một băng giấy chia thành 5 ô bằng nhau. Có mấy hình đơn?',
           'Có 5 mảnh nhỏ nên có 5 hình đơn.'),
        lt(7, 3, 'Một hình chữ nhật chia thành 3 ô. Ngoài 3 hình đơn thì trong hình có '
                 'còn hình nào nữa không?',
           'Còn nữa, vì ghép mấy mảnh cạnh nhau lại cũng thành hình chữ nhật.'),
        lt(8, 3, 'Một hình vuông to chia thành 4 ô vuông nhỏ. Cho biết có mấy hình đơn '
                 'và hình to nhất có phải hình vuông không.',
           'Có 4 hình đơn, và hình to nhất ôm cả bốn ô cũng là một hình vuông.'),
    ] + [
        q_tf(1, 'Đánh số các mảnh trước rồi mới đếm.', True,
             'Đúng — làm có thứ tự thì không sót không trùng.'),
        q_mcq(2, 'Hình chữ nhật chia thành 3 ô thì có mấy hình đơn?',
              ['3', '6', '1', '4'], '3', 'Mỗi mảnh một hình đơn.'),
        q_tf(3, 'Đếm xong hình đơn là xong bài.', False,
             'Sai. Trong hình còn hình ghép nữa.'),
        q_mcq(4, 'Hình vuông chia thành 4 ô nhỏ thì có mấy hình đơn?',
              ['4', '5', '2', '8'], '4', 'Bốn mảnh nhỏ.'),
        q_tf(5, 'Hình to ôm cả các mảnh cũng là một hình.', True,
             'Đúng — và nó hay bị bỏ sót nhất.'),
    ],
)

# ═══ ④ B65 · ĐẾM HÌNH GHÉP ═══
B65 = bai(
    65, 'ĐẾM HÌNH GHÉP — HÌNH TO HAY ẨN MÌNH NHẤT',
    'HH 2.1b — Đếm hình ghép: ghép hai mảnh, ba mảnh, rồi cả hình.',
    video(
        ['Nhận ra hình ghép do nhiều mảnh hợp lại.',
         'Đếm hình ghép theo thứ tự: ghép hai mảnh, rồi ba mảnh.',
         'Không sót hình to nhất ôm cả hình.'],
        ['Đề bài: Một hình chữ nhật được chia thành 3 ô vuông nhỏ xếp thành hàng ngang '
         'và đánh số 1, 2, 3. Hỏi ghép được thêm mấy hình chữ nhật nữa?',
         'Ghép hai mảnh cạnh nhau trước',
         'Ghép mảnh 1 với mảnh 2 được một hình. Ghép mảnh 2 với mảnh 3 được một hình '
         'nữa. Vậy 2 hình.',
         'Rồi ghép ba mảnh',
         'Ghép cả 1, 2 và 3 được hình to nhất ôm trọn cả hình. Thêm 1 hình.',
         'Cộng lại',
         'Ghép được tất cả 2 + 1 = 3 hình.',
         'Đáp số: 3 hình ghép.',
         'Đi tuần tự ghép hai mảnh rồi ghép ba mảnh thì không sót hình nào — mà hình '
         'to nhất luôn là hình hay ẩn mình nhất.'],
        ['Có bạn đếm được ba mảnh nhỏ rồi ghi luôn đáp số là ba hình.',
         'Gợi ý 1: Ghép mảnh 1 với mảnh 2 lại thì có thành một hình chữ nhật không?',
         'Gợi ý 2: Còn hình to nhất ôm cả ba mảnh thì sao, có tính là một hình '
         'không?',
         'Chữa: ngoài ba hình đơn còn ba hình ghép nữa, tất cả là sáu hình.'],
        ['Cắt một băng giấy thành ba ô rồi cho con lấy hai ngón tay khoanh từng hình — '
         'khoanh được bao nhiêu cách là bấy nhiêu hình.',
         'Bố mẹ hỏi: "Con tìm hình to nhất chưa?"'],
    ),
    [
        lt(1, 1, 'Băng 3 ô đánh số 1, 2, 3. Ghép hai mảnh cạnh nhau được mấy hình?',
           'Ghép được hai cách là mảnh 1 với 2, và mảnh 2 với 3, nên được 2 hình.'),
        lt(2, 1, 'Băng 3 ô. Ghép cả ba mảnh được mấy hình?',
           'Chỉ ghép được một cách duy nhất nên được 1 hình.'),
        lt(3, 1, 'Băng 3 ô. Tất cả có mấy hình ghép?',
           'Ghép hai mảnh được 2 hình, ghép ba mảnh được 1 hình, cộng lại là 3.'),
        lt(4, 2, 'Băng 3 ô. Cộng cả hình đơn lẫn hình ghép thì có tất cả mấy hình chữ '
                 'nhật?',
           'Có 3 hình đơn và 3 hình ghép, cộng lại được 6 hình.'),
        lt(5, 2, 'Hình nào trong hình ghép hay bị bỏ sót nhất?',
           'Hình to nhất ôm trọn cả hình là hình hay bị bỏ sót nhất.'),
        lt(6, 2, 'Băng 4 ô đánh số 1, 2, 3, 4. Ghép hai mảnh cạnh nhau được mấy hình?',
           'Ghép được ba cách là 1 với 2, 2 với 3, và 3 với 4, nên được 3 hình.'),
        lt(7, 3, 'Băng 4 ô. Ghép ba mảnh cạnh nhau được mấy hình, và ghép cả bốn mảnh '
                 'được mấy hình?',
           'Ghép ba mảnh được hai cách nên 2 hình. Ghép cả bốn mảnh chỉ một cách nên '
           '1 hình.'),
        lt(8, 3, 'Băng 4 ô. Cộng cả hình đơn lẫn hình ghép thì có tất cả mấy hình chữ '
                 'nhật?',
           'Hình đơn 4, ghép hai mảnh 3, ghép ba mảnh 2, ghép bốn mảnh 1. Cộng lại '
           'được 10 hình.'),
    ] + [
        q_tf(1, 'Ghép nhiều mảnh cạnh nhau cũng được một hình.', True,
             'Đúng — đó là hình ghép.'),
        q_mcq(2, 'Băng 3 ô có tất cả mấy hình chữ nhật?',
              ['6', '3', '4', '9'], '6', 'Ba hình đơn cộng ba hình ghép.'),
        q_mcq(3, 'Băng 3 ô ghép hai mảnh được mấy hình?',
              ['2', '3', '1', '6'], '2', 'Hai cặp mảnh cạnh nhau.'),
        q_tf(4, 'Đếm ba mảnh nhỏ là đếm xong cả hình.', False,
             'Sai. Còn ba hình ghép nữa.'),
        q_tf(5, 'Hình to nhất luôn là hình hay ẩn mình nhất.', True,
             'Đúng — nhớ lùng nó sau cùng.'),
    ],
)

# ═══ ⑤ B28 · TÂM VÀ NAN HOA ═══
B28 = bai(
    28, 'HÌNH TRÒN — TÂM VÀ NAN HOA BẰNG NHAU',
    'HH 4.1a — Nhận dạng hình tròn: tâm và các nan hoa bằng nhau.',
    video(
        ['Biết tâm là điểm chính giữa hình tròn.',
         'Hiểu mọi nan hoa từ tâm ra viền đều dài bằng nhau.',
         'Phân biệt hình tròn thật với hình méo.'],
        ['Đề bài: Trong các mặt sau, mặt nào có dạng hình tròn: mặt đồng hồ treo '
         'tường, quyển vở, chiếc đĩa, quả trứng nhìn nghiêng, đồng xu?',
         'Hình tròn có một cái rốn chính giữa gọi là TÂM',
         'Từ tâm căng dây ra viền theo hướng nào cũng được, ta gọi đó là các nan hoa.',
         'Bí mật: mọi nan hoa đều dài bằng nhau',
         'Đo thử vài nan hoa mà xem, hướng nào cũng ra cùng một độ dài.',
         'Đo nan hoa là biết tròn thật hay tròn giả',
         'Quả trứng nhìn nghiêng cũng có viền cong, nhưng nan hoa chỗ dài chỗ ngắn nên '
         'nó là hình méo chứ không phải hình tròn.',
         'Đáp số: mặt đồng hồ, chiếc đĩa và đồng xu có dạng hình tròn.',
         'Quyển vở là hình chữ nhật, còn quả trứng nhìn nghiêng là hình méo.'],
        ['Có bạn thấy cái gì viền cong cũng gọi là hình tròn, kể cả quả trứng.',
         'Gợi ý 1: Con thử đo mấy nan hoa của quả trứng xem có bằng nhau không.',
         'Gợi ý 2: Chỗ đầu nhọn và chỗ bụng phình khác nhau xa lắm đấy.',
         'Chữa: viền cong chưa đủ. Phải mọi nan hoa bằng nhau mới là hình tròn.'],
        ['Úp miệng cốc hay nắp hộp lên giấy rồi tô theo viền — con vẽ được hình tròn '
         'đẹp mà không cần khéo tay.',
         'Bố mẹ hỏi: "Nan hoa của nó có bằng nhau không?"'],
    ),
    [
        lt(1, 1, 'Điểm chính giữa hình tròn gọi là gì?',
           'Điểm chính giữa hình tròn gọi là tâm.'),
        lt(2, 1, 'Các nan hoa từ tâm ra viền có bằng nhau không?',
           'Mọi nan hoa của hình tròn đều dài bằng nhau.'),
        lt(3, 1, 'Mặt đồng xu có dạng hình gì?',
           'Mặt đồng xu có dạng hình tròn, vì nan hoa hướng nào cũng bằng nhau.'),
        lt(4, 2, 'Quả trứng nhìn nghiêng có phải hình tròn không?',
           'Không phải, vì nan hoa chỗ dài chỗ ngắn nên nó là hình méo.'),
        lt(5, 2, 'Muốn biết một hình tròn thật hay tròn giả thì làm gì?',
           'Đo vài nan hoa từ tâm ra viền xem có bằng nhau không.'),
        lt(6, 2, 'Mặt quyển vở có dạng hình gì?',
           'Mặt quyển vở có dạng hình chữ nhật, không phải hình tròn.'),
        lt(7, 3, 'Trong bốn thứ: mặt đồng hồ, mặt bàn học, chiếc đĩa, quả trứng nhìn '
                 'nghiêng — có mấy mặt là hình tròn?',
           'Mặt đồng hồ và chiếc đĩa là hình tròn, nên có 2 mặt.'),
        lt(8, 3, 'Một hình tròn có nan hoa dài 3 xăng-ti-mét. Hai nan hoa nối thẳng '
                 'qua tâm thì dài mấy xăng-ti-mét?',
           'Hai nan hoa nối lại: 3 + 3 = 6 xăng-ti-mét.'),
    ] + [
        q_tf(1, 'Mọi nan hoa của hình tròn đều dài bằng nhau.', True,
             'Đúng — đó là bí mật của hình tròn.'),
        q_mcq(2, 'Điểm chính giữa hình tròn gọi là gì?',
              ['tâm', 'đỉnh', 'cạnh'], 'tâm', 'Nó như cái rốn của hình.'),
        q_tf(3, 'Quả trứng nhìn nghiêng là hình tròn.', False,
             'Sai. Nan hoa của nó chỗ dài chỗ ngắn nên nó là hình méo.'),
        q_mcq(4, 'Muốn biết tròn thật hay tròn giả thì làm gì?',
              ['đo nan hoa xem có bằng nhau không', 'nhìn cho kỹ', 'đếm cạnh'],
              'đo nan hoa xem có bằng nhau không', 'Đo là chắc nhất.'),
        q_tf(5, 'Cứ viền cong là hình tròn.', False,
             'Sai. Hình méo cũng có viền cong.'),
    ],
)

# ═══ ⑥ B66 · VÌ SAO BÁNH XE PHẢI TRÒN ═══
B66 = bai(
    66, 'VÌ SAO BÁNH XE PHẢI TRÒN',
    'HH 4.1b — Ứng dụng của hình tròn: trục xe luôn cao đều một mức.',
    video(
        ['Giải thích được vì sao bánh xe tròn thì xe chạy êm.',
         'Hiểu trục xe đặt ở tâm nên luôn cao đều một mức.',
         'Biết bánh vuông thì trục lúc nhô lúc tụt.'],
        ['Đề bài: Vì sao bánh xe phải làm hình tròn mà không làm hình vuông?',
         'Trục xe đặt ở đâu',
         'Trục xe đặt đúng ở tâm bánh xe.',
         'Bánh tròn thì trục luôn cao đều một mức',
         'Vì mọi nan hoa dài bằng nhau, nên chỗ nào chạm đất thì trục cũng cao đúng '
         'bằng một nan hoa. Xe chạy êm ru.',
         'Bánh vuông thì trục lúc nhô lúc tụt',
         'Nan hoa ra góc thì dài, ra giữa cạnh thì ngắn. Trục nhấp nhô nên xe xóc.',
         'Đáp số: vì mọi nan hoa của hình tròn bằng nhau nên trục xe luôn cao đều.',
         'Bài này là chỗ hình học gặp cuộc sống thật — cả cái bánh xe đứng trên đúng '
         'một tính chất ấy.'],
        ['Có bạn bảo bánh vuông cũng lăn được, chỉ hơi xóc thôi.',
         'Gợi ý 1: Trục xe cao bao nhiêu khi bánh vuông đứng trên một cạnh, và khi nó '
         'nghiêng trên một góc?',
         'Gợi ý 2: Hai độ cao ấy khác nhau thì người ngồi trên xe thấy thế nào?',
         'Chữa: trục nhấp nhô thì xe xóc suốt, không đi được. Nan hoa bằng nhau mới '
         'giữ trục cao đều.'],
        ['Cho con lăn thử một đồng xu và một khối vuông trên mặt bàn — sự khác nhau '
         'thấy được ngay bằng tay.',
         'Bố mẹ hỏi: "Trục xe cao lên tụt xuống thì người ngồi thấy sao?"'],
    ),
    [
        lt(1, 1, 'Trục xe đặt ở đâu trên bánh xe?',
           'Trục xe đặt đúng ở tâm bánh xe.'),
        lt(2, 1, 'Bánh xe tròn thì trục xe cao đều hay lúc nhô lúc tụt?',
           'Trục xe luôn cao đều một mức, vì mọi nan hoa bằng nhau.'),
        lt(3, 1, 'Bánh xe vuông thì xe chạy êm hay xóc?',
           'Xe chạy xóc, vì trục lúc nhô lúc tụt.'),
        lt(4, 2, 'Vì sao bánh tròn giữ được trục cao đều?',
           'Vì mọi nan hoa từ tâm ra viền đều dài bằng nhau.'),
        lt(5, 2, 'Bánh vuông thì nan hoa ra góc dài hơn hay ngắn hơn nan hoa ra giữa '
                 'cạnh?',
           'Nan hoa ra góc dài hơn nan hoa ra giữa cạnh.'),
        lt(6, 2, 'Một bánh xe tròn có nan hoa dài 4 xăng-ti-mét. Trục xe cao cách mặt '
                 'đất mấy xăng-ti-mét?',
           'Trục cao đúng bằng một nan hoa, tức 4 xăng-ti-mét.'),
        lt(7, 3, 'Một bánh xe tròn có nan hoa 5 xăng-ti-mét. Bánh xe ấy cao tất cả mấy '
                 'xăng-ti-mét, tính từ mặt đất lên đỉnh?',
           'Từ đất lên tâm là 5, từ tâm lên đỉnh cũng 5, nên 5 + 5 = 10 xăng-ti-mét.'),
        lt(8, 3, 'Có bạn bảo bánh vuông cũng dùng được, chỉ hơi xóc. Nói xem vì sao xe '
                 'lại xóc.',
           'Vì nan hoa của hình vuông chỗ dài chỗ ngắn, nên trục xe lúc nhô lúc tụt.'),
    ] + [
        q_tf(1, 'Trục xe đặt ở tâm bánh xe.', True, 'Đúng — đó là chỗ then chốt.'),
        q_mcq(2, 'Vì sao bánh tròn thì xe chạy êm?',
              ['vì mọi nan hoa bằng nhau nên trục cao đều',
               'vì bánh tròn nhẹ hơn', 'vì bánh tròn đẹp hơn'],
              'vì mọi nan hoa bằng nhau nên trục cao đều',
              'Trục cao đều thì người ngồi không thấy xóc.'),
        q_tf(3, 'Bánh xe vuông thì trục xe vẫn cao đều.', False,
             'Sai. Nan hoa ra góc dài hơn nên trục lúc nhô lúc tụt.'),
        q_mcq(4, 'Bánh tròn nan hoa 4 xăng-ti-mét thì trục cao mấy xăng-ti-mét?',
              ['4', '8', '2', '16'], '4', 'Đúng bằng một nan hoa.'),
        q_tf(5, 'Cái bánh xe đứng trên đúng một tính chất của hình tròn.', True,
             'Đúng — mọi nan hoa bằng nhau.'),
    ],
)

# ═══ ⑦ B29 · HAI LOẠI KHỐI ═══
B29 = bai(
    29, 'HAI LOẠI KHỐI — MỖI KHỐI SÁU MẶT',
    'HH 5.1a — Khối lập phương và khối hộp chữ nhật, đếm sáu mặt.',
    video(
        ['Phân biệt khối lập phương và khối hộp chữ nhật.',
         'Đếm được sáu mặt của một khối.',
         'Gọi tên sáu mặt: trên, dưới, trước, sau, trái, phải.'],
        ['Đề bài: Xếp các đồ vật sau vào đúng nhóm: viên xúc xắc, hộp sữa tươi, khối '
         'ru-bích, viên gạch.',
         'Khối lập phương vuông vức mọi phía',
         'Xúc xắc và ru-bích đều vuông vức, mỗi mặt là một hình vuông giống hệt nhau.',
         'Khối hộp chữ nhật thì dài dài',
         'Hộp sữa và viên gạch có mặt là hình chữ nhật.',
         'Đếm mặt thì khối nào cũng sáu',
         'Cầm hộp lên rồi sờ và đếm: mặt trên, mặt dưới, mặt trước, mặt sau, mặt trái, '
         'mặt phải. Đúng 6 mặt.',
         'Đáp số: xúc xắc và ru-bích là khối lập phương; hộp sữa và viên gạch là khối '
         'hộp chữ nhật.',
         'Khối nào cũng có sáu mặt, chỉ khác nhau ở chỗ mặt ấy vuông hay chữ nhật.'],
        ['Có bạn đếm được bốn mặt rồi thôi, vì quên mất mặt trên và mặt dưới.',
         'Gợi ý 1: Con cầm hộp lên rồi sờ từng mặt một, đừng chỉ nhìn.',
         'Gợi ý 2: Đặt hộp xuống bàn thì mặt nào đang úp xuống? Mặt ấy cũng phải đếm.',
         'Chữa: đếm đủ sáu mặt là trên, dưới, trước, sau, trái, phải.'],
        ['Đưa con một hộp bất kỳ rồi bảo sờ và đếm từng mặt — sờ được thì nhớ lâu hơn '
         'nhìn.',
         'Bố mẹ hỏi: "Con đếm cả mặt đang úp xuống bàn chưa?"'],
    ),
    [
        lt(1, 1, 'Một khối hộp có mấy mặt?', 'Khối nào cũng có 6 mặt.'),
        lt(2, 1, 'Viên xúc xắc là khối gì?',
           'Viên xúc xắc vuông vức mọi phía nên là khối lập phương.'),
        lt(3, 1, 'Hộp sữa tươi là khối gì?',
           'Hộp sữa tươi dài dài, mặt là hình chữ nhật, nên là khối hộp chữ nhật.'),
        lt(4, 2, 'Mỗi mặt của khối lập phương là hình gì?',
           'Mỗi mặt của khối lập phương là một hình vuông giống hệt nhau.'),
        lt(5, 2, 'Kể tên sáu mặt của một khối hộp.',
           'Sáu mặt là mặt trên, mặt dưới, mặt trước, mặt sau, mặt trái và mặt phải.'),
        lt(6, 2, 'Trong bốn thứ: xúc xắc, hộp sữa, ru-bích, viên gạch — có mấy khối '
                 'lập phương?',
           'Xúc xắc và ru-bích là khối lập phương, nên có 2 khối.'),
        lt(7, 3, 'Một khối lập phương có sáu mặt, mỗi mặt là hình vuông cạnh 3 '
                 'xăng-ti-mét. Chú kiến bò một vòng quanh một mặt được mấy '
                 'xăng-ti-mét?',
           'Một mặt là hình vuông cạnh 3, nên 3 + 3 + 3 + 3 = 12 xăng-ti-mét.'),
        lt(8, 3, 'Ba viên xúc xắc thì có tất cả mấy mặt?',
           'Mỗi viên 6 mặt, ba viên thì 6 × 3 = 18 mặt.'),
    ] + [
        q_tf(1, 'Khối nào cũng có sáu mặt.', True,
             'Đúng — trên, dưới, trước, sau, trái, phải.'),
        q_mcq(2, 'Viên xúc xắc là khối gì?',
              ['khối lập phương', 'khối hộp chữ nhật', 'hình vuông'],
              'khối lập phương', 'Vuông vức mọi phía.'),
        q_mcq(3, 'Hộp sữa tươi là khối gì?',
              ['khối hộp chữ nhật', 'khối lập phương', 'hình chữ nhật'],
              'khối hộp chữ nhật', 'Mặt của nó là hình chữ nhật.'),
        q_tf(4, 'Khối lập phương có mọi mặt là hình vuông giống hệt nhau.', True,
             'Đúng — đó là dấu hiệu nhận ra nó.'),
        q_tf(5, 'Đếm mặt thì bỏ qua mặt đang úp xuống bàn.', False,
             'Sai. Mặt ấy vẫn phải đếm.'),
    ],
)

# ═══ ⑧ B67 · HÌNH DẸT VÀ KHỐI ═══
B67 = bai(
    67, 'HÌNH DẸT TRÊN GIẤY, KHỐI CẦM NẮM ĐƯỢC',
    'HH 5.1b — Phân biệt hình phẳng và khối: hình là ảnh chụp một mặt.',
    video(
        ['Phân biệt hình phẳng và khối.',
         'Hiểu hình phẳng là ảnh chụp một mặt của khối.',
         'Đoán được in một mặt của khối ra giấy thì được hình gì.'],
        ['Đề bài: Hình vuông và khối lập phương khác nhau thế nào?',
         'Hình thì dẹt, nằm trên giấy',
         'Hình vuông vẽ trên giấy, mỏng dính, không cầm nắm được.',
         'Khối thì cầm nắm được',
         'Khối lập phương cầm được trong tay, có chỗ rỗng bên trong để giấu kẹo.',
         'Hình chính là ảnh chụp MỘT MẶT của khối',
         'Chấm một mặt của khối lập phương vào mực rồi in lên giấy, ta được một hình '
         'vuông.',
         'Đáp số: hình vuông là hình phẳng, còn khối lập phương là khối có 6 mặt.',
         'Muốn biết một khối là khối gì, cứ hỏi: in một mặt của nó ra giấy thì được '
         'hình gì?'],
        ['Có bạn gọi viên xúc xắc là hình vuông.',
         'Gợi ý 1: Hình vuông có cầm nắm được không, hay chỉ nằm trên giấy?',
         'Gợi ý 2: Viên xúc xắc có mấy mặt? Hình vuông có mấy mặt?',
         'Chữa: viên xúc xắc là KHỐI lập phương. Hình vuông chỉ là ảnh chụp một mặt '
         'của nó.'],
        ['Chấm một mặt hộp vào màu nước rồi in lên giấy cùng con — trò này nói được cả '
         'bài học mà chẳng cần giảng.',
         'Bố mẹ hỏi: "Cái này cầm nắm được không, hay chỉ nằm trên giấy?"'],
    ),
    [
        lt(1, 1, 'Hình vuông là hình dẹt hay khối cầm nắm được?',
           'Hình vuông là hình dẹt nằm trên giấy.'),
        lt(2, 1, 'Khối lập phương là hình dẹt hay khối cầm nắm được?',
           'Khối lập phương cầm nắm được, có sáu mặt.'),
        lt(3, 1, 'In một mặt của khối lập phương ra giấy thì được hình gì?',
           'Được một hình vuông, vì mặt của khối lập phương là hình vuông.'),
        lt(4, 2, 'In một mặt của khối hộp chữ nhật ra giấy thì được hình gì?',
           'Được một hình chữ nhật.'),
        lt(5, 2, 'Viên xúc xắc là hình vuông hay khối lập phương?',
           'Viên xúc xắc cầm nắm được nên là khối lập phương, không phải hình vuông.'),
        lt(6, 2, 'Muốn biết một khối là khối gì thì hỏi câu nào?',
           'Hỏi rằng in một mặt của nó ra giấy thì được hình gì.'),
        lt(7, 3, 'Một khối lập phương in ra giấy được mấy hình vuông khác nhau nếu in '
                 'đủ cả sáu mặt?',
           'Khối có 6 mặt nên in đủ được 6 hình vuông.'),
        lt(8, 3, 'Trong bốn thứ: hình tam giác vẽ trên vở, viên gạch, hình tròn vẽ '
                 'trên bảng, hộp bút — có mấy thứ là khối?',
           'Viên gạch và hộp bút cầm nắm được nên là khối, tức 2 thứ.'),
    ] + [
        q_tf(1, 'Hình phẳng là ảnh chụp một mặt của khối.', True,
             'Đúng — in ra giấy là thấy.'),
        q_mcq(2, 'In một mặt khối lập phương ra giấy được hình gì?',
              ['hình vuông', 'hình tròn', 'hình tam giác'], 'hình vuông',
              'Mặt của nó là hình vuông.'),
        q_tf(3, 'Viên xúc xắc là hình vuông.', False,
             'Sai. Nó là KHỐI lập phương, cầm nắm được.'),
        q_mcq(4, 'Thứ nào cầm nắm được?',
              ['khối hộp chữ nhật', 'hình chữ nhật', 'hình tròn'],
              'khối hộp chữ nhật', 'Khối thì có bề dày.'),
        q_tf(5, 'Hình dẹt trên giấy cũng có sáu mặt.', False,
             'Sai. Sáu mặt là chuyện của khối.'),
    ],
)

# ═══ ⑨ B30 · LUẬT NGỒI ═══
B30 = bai(
    30, 'LUẬT NGỒI — KHỐI BỊ CHE VẪN PHẢI ĐẾM',
    'HH 6.1a — Đếm khối trong hình xếp: luật ngồi bảo lãnh khối bị che.',
    video(
        ['Hiểu luật ngồi: khối tầng trên phải có khối tầng dưới đỡ.',
         'Biết khối bị che vẫn phải đếm.',
         'Suy ra được khối nấp phía sau mà mắt không thấy.'],
        ['Đề bài: Một tháp có một khối ở tầng hai. Hỏi bên dưới khối ấy có khối nào '
         'không, dù mắt không nhìn thấy?',
         'Khối không biết bay',
         'Khối ở tầng trên phải ngồi trên một khối tầng dưới, không thì nó rơi.',
         'Nên thấy khối tầng hai là biết chắc bên dưới có khối',
         'Dù khối ấy bị che gần hết, luật ngồi vẫn bảo lãnh cho nó.',
         'Khối bị che vẫn phải đếm',
         'Đếm bằng mắt thì sót; đếm bằng luật ngồi thì không.',
         'Đáp số: có, bên dưới chắc chắn có một khối đỡ.',
         'Nhìn thấy hay không nhìn thấy không quyết định — luật ngồi mới quyết định.'],
        ['Có bạn chỉ đếm những khối mắt nhìn thấy, nên tháp nào cũng đếm thiếu.',
         'Gợi ý 1: Khối ở tầng hai có bay lơ lửng được không?',
         'Gợi ý 2: Nếu nó không bay được thì bên dưới nó phải có gì?',
         'Chữa: khối bị che vẫn phải đếm, vì luật ngồi bảo lãnh cho nó.'],
        ['Xếp vài khối gỗ thành tháp rồi cho con đếm, sau đó gỡ ra đếm lại — con sẽ '
         'thấy mình vừa sót mấy khối nấp phía sau.',
         'Bố mẹ hỏi: "Khối trên cùng đang ngồi trên cái gì?"'],
    ),
    [
        lt(1, 1, 'Khối ở tầng trên có bay lơ lửng được không?',
           'Không, khối tầng trên phải ngồi trên một khối tầng dưới.'),
        lt(2, 1, 'Thấy một khối ở tầng hai thì bên dưới nó có khối không?',
           'Có, luật ngồi bảo lãnh rằng bên dưới chắc chắn có một khối đỡ.'),
        lt(3, 1, 'Khối bị che khuất có phải đếm không?',
           'Có, khối bị che vẫn phải đếm.'),
        lt(4, 2, 'Tầng hai có 1 khối. Riêng khối đỡ nó ở tầng dưới là mấy khối?',
           'Có 1 khối đỡ ngay bên dưới.'),
        lt(5, 2, 'Vì sao đếm bằng mắt thì hay sót?',
           'Vì có khối nấp phía sau hoặc bị che, mắt không nhìn thấy.'),
        lt(6, 2, 'Tầng hai có 2 khối, mỗi khối đều ngồi trên một khối riêng. Tầng dưới '
                 'có ít nhất mấy khối?',
           'Mỗi khối tầng trên cần một khối đỡ, nên tầng dưới có ít nhất 2 khối.'),
        lt(7, 3, 'Một tháp có tầng ba 1 khối, tầng hai 1 khối, tầng một 1 khối. Tháp '
                 'có mấy khối?',
           'Cộng ba tầng: 1 + 1 + 1 = 3 khối.'),
        lt(8, 3, 'Tầng hai có 3 khối, mỗi khối ngồi trên một khối riêng ở tầng một. '
                 'Tầng một còn thêm 2 khối nữa. Tháp có tất cả mấy khối?',
           'Tầng một có 3 + 2 = 5 khối. Cộng với tầng hai: 5 + 3 = 8 khối.'),
    ] + [
        q_tf(1, 'Khối tầng trên phải có khối tầng dưới đỡ.', True,
             'Đúng — đó là luật ngồi.'),
        q_tf(2, 'Khối bị che thì không đếm.', False,
             'Sai. Luật ngồi bảo lãnh cho nó, vẫn phải đếm.'),
        q_mcq(3, 'Thấy 1 khối ở tầng hai thì bên dưới có mấy khối đỡ?',
              ['1', '0', '2', '4'], '1', 'Một khối đỡ ngay bên dưới.'),
        q_mcq(4, 'Vì sao đếm bằng mắt hay sót?',
              ['vì có khối nấp phía sau', 'vì khối quá nhỏ', 'vì đếm nhanh quá'],
              'vì có khối nấp phía sau', 'Nên phải đếm bằng luật.'),
        q_tf(5, 'Khối biết bay nên không cần khối đỡ.', False,
             'Sai. Khối không biết bay.'),
    ],
)

# ═══ ⑩ B68 · ĐẾM THEO TẦNG ═══
B68 = bai(
    68, 'ĐẾM THEO TẦNG RỒI CỘNG LẠI',
    'HH 6.1b — Đếm khối trong hình xếp: đếm từng tầng rồi cộng.',
    video(
        ['Đếm khối theo từng tầng thay vì đếm lung tung.',
         'Đếm cả hàng nấp phía sau ở mỗi tầng.',
         'Cộng số khối của các tầng lại.'],
        ['Đề bài: Một tháp có tầng dưới xếp 2 hàng, mỗi hàng 2 khối; tầng trên có 1 '
         'khối. Hỏi tháp có tất cả bao nhiêu khối?',
         'Đừng đếm lung tung theo mắt nhìn',
         'Đếm từng tầng một, như đếm nhà cao tầng.',
         'Đếm tầng dưới, kể cả hàng nấp phía sau',
         'Tầng dưới có 2 hàng, mỗi hàng 2 khối, nên 2 × 2 = 4 khối. Một khối ở góc sau '
         'bị che gần hết nhưng vẫn đếm.',
         'Đếm tầng trên',
         'Tầng trên có 1 khối.',
         'Cộng các tầng lại',
         'Tất cả là 4 + 1 = 5 khối.',
         'Đáp số: 5 khối.',
         'Kiểm tra bằng cách tưởng tượng gỡ tháp ra từng khối một — gỡ đủ năm lần mới '
         'hết.'],
        ['Có bạn đếm lung tung theo mắt nhìn nên lúc thì sót khối nấp sau, lúc thì đếm '
         'một khối hai lần.',
         'Gợi ý 1: Đếm từng tầng một, đừng nhảy qua nhảy lại.',
         'Gợi ý 2: Ở mỗi tầng, nhớ đếm cả hàng phía sau bị che.',
         'Chữa: đếm tầng dưới trước, tầng trên sau, rồi cộng lại.'],
        ['Xếp một tháp khối gỗ rồi cùng con đếm theo tầng, sau đó gỡ ra đếm lại để '
         'kiểm tra — hai con số phải bằng nhau.',
         'Bố mẹ hỏi: "Tầng này có mấy khối, kể cả hàng sau?"'],
    ),
    [
        lt(1, 1, 'Tầng dưới xếp 2 hàng, mỗi hàng 2 khối. Tầng dưới có mấy khối?',
           'Lấy 2 × 2 = 4 khối.'),
        lt(2, 1, 'Tầng dưới 4 khối, tầng trên 1 khối. Tháp có mấy khối?',
           'Cộng hai tầng: 4 + 1 = 5 khối.'),
        lt(3, 1, 'Nên đếm khối theo cách nào?',
           'Đếm theo từng tầng, tầng dưới trước rồi tầng trên sau.'),
        lt(4, 2, 'Tầng dưới có 3 khối xếp hàng ngang, tầng trên có 2 khối. Tháp có mấy '
                 'khối?',
           'Cộng hai tầng: 3 + 2 = 5 khối.'),
        lt(5, 2, 'Ở mỗi tầng, phải nhớ đếm cả cái gì?',
           'Phải đếm cả hàng nấp phía sau bị che.'),
        lt(6, 2, 'Tầng dưới xếp 3 hàng, mỗi hàng 3 khối. Tầng dưới có mấy khối?',
           'Lấy 3 × 3 = 9 khối.'),
        lt(7, 3, 'Một tháp có tầng dưới 9 khối, tầng giữa 4 khối, tầng trên 1 khối. '
                 'Tháp có tất cả mấy khối?',
           'Cộng ba tầng: 9 + 4 = 13, rồi 13 + 1 = 14 khối.'),
        lt(8, 3, 'Tầng dưới xếp 2 hàng mỗi hàng 3 khối, tầng trên xếp 1 hàng 2 khối. '
                 'Cho biết mỗi tầng mấy khối và cả tháp mấy khối.',
           'Tầng dưới 2 × 3 = 6 khối, tầng trên 2 khối, cả tháp 6 + 2 = 8 khối.'),
    ] + [
        q_tf(1, 'Nên đếm khối theo từng tầng rồi cộng lại.', True,
             'Đúng — đếm lung tung thì sót.'),
        q_mcq(2, 'Tầng dưới 4 khối, tầng trên 1 khối. Tháp mấy khối?',
              ['5', '4', '3', '8'], '5', 'Cộng hai tầng.'),
        q_mcq(3, 'Tầng dưới xếp 2 hàng mỗi hàng 2 khối thì có mấy khối?',
              ['4', '2', '6', '8'], '4', 'Hai hàng, mỗi hàng hai khối.'),
        q_tf(4, 'Đếm mỗi tầng thì bỏ qua hàng nấp phía sau.', False,
             'Sai. Hàng nấp phía sau vẫn phải đếm.'),
        q_tf(5, 'Có thể kiểm tra bằng cách gỡ tháp ra từng khối một.', True,
             'Đúng — số lần gỡ phải bằng số khối đã đếm.'),
    ],
)

MOI = [B26, B64, B27, B65, B28, B66, B29, B67, B30, B68]

SAU = {
    'DL:KSN2.B64': 'DL:KSN2.B26',
    'DL:KSN2.B65': 'DL:KSN2.B27',
    'DL:KSN2.B66': 'DL:KSN2.B28',
    'DL:KSN2.B67': 'DL:KSN2.B29',
    'DL:KSN2.B68': 'DL:KSN2.B30',
}


def _o(gt, chon=None, nhan=None):
    d = {'value': gt}
    if chon:
        d['options'] = list(chon)
    if nhan:
        d['label'] = nhan
    return d


O_NHAP_MOI = {
 # ① B26
 'DL:KSN2.B26#C1': {'value': 3},
 'DL:KSN2.B26#C2': {'value': 3},
 'DL:KSN2.B26#C3': {'value': 4},
 'DL:KSN2.B26#C4': {'parts': [_o('tứ giác', ['tứ giác', 'tam giác', 'hình tròn'],
                                 'họ chung')]},
 'DL:KSN2.B26#C5': {'parts': [_o('có', CO_KHONG, 'còn là hình vuông không')]},
 'DL:KSN2.B26#C6': {'parts': [
     _o('hình vuông có cả bốn cạnh bằng nhau',
        ['hình vuông có cả bốn cạnh bằng nhau', 'hình vuông có nhiều đỉnh hơn'],
        'khác ở chỗ nào')]},
 'DL:KSN2.B26#C7': {'parts': [_o(7, nhan='tổng số cạnh'), _o(7, nhan='tổng số đỉnh'),
                              _o(14, nhan='cộng cả hai')]},
 'DL:KSN2.B26#C8': {'value': 3},

 # ② B64
 'DL:KSN2.B64#C1': {'value': 12},
 'DL:KSN2.B64#C2': {'value': 12},
 'DL:KSN2.B64#C3': {'value': 20},
 'DL:KSN2.B64#C4': {'value': 18},
 'DL:KSN2.B64#C5': {'parts': [_o('tổng độ dài các cạnh',
                                 ['tổng độ dài các cạnh', 'cạnh dài nhất',
                                  'số cạnh'], 'bằng cái gì')]},
 'DL:KSN2.B64#C6': {'value': 15},
 'DL:KSN2.B64#C7': {'parts': [_o(16, nhan='hình cạnh 4'), _o(24, nhan='hình cạnh 6')]},
 'DL:KSN2.B64#C8': {'value': 3},

 # ③ B27
 'DL:KSN2.B27#C1': {'value': 3},
 'DL:KSN2.B27#C2': {'parts': [_o('đánh số từng mảnh nhỏ',
                                 ['đánh số từng mảnh nhỏ', 'đếm luôn bằng mắt'],
                                 'việc đầu tiên')]},
 'DL:KSN2.B27#C3': {'value': 2},
 'DL:KSN2.B27#C4': {'value': 4},
 'DL:KSN2.B27#C5': {'parts': [_o('để không sót và không đếm trùng',
                                 ['để không sót và không đếm trùng',
                                  'để hình đẹp hơn'], 'vì sao')]},
 'DL:KSN2.B27#C6': {'value': 5},
 'DL:KSN2.B27#C7': {'parts': [_o('có', CO_KHONG, 'còn hình nào nữa không')]},
 'DL:KSN2.B27#C8': {'parts': [_o(4, nhan='mấy hình đơn'),
                              _o('có', CO_KHONG, 'hình to nhất là hình vuông')]},

 # ④ B65
 'DL:KSN2.B65#C1': {'value': 2},
 'DL:KSN2.B65#C2': {'value': 1},
 'DL:KSN2.B65#C3': {'value': 3},
 'DL:KSN2.B65#C4': {'value': 6},
 'DL:KSN2.B65#C5': {'parts': [_o('hình to nhất ôm trọn cả hình',
                                 ['hình to nhất ôm trọn cả hình', 'mảnh nhỏ nhất'],
                                 'hình nào hay sót')]},
 'DL:KSN2.B65#C6': {'value': 3},
 'DL:KSN2.B65#C7': {'parts': [_o(2, nhan='ghép ba mảnh'), _o(1, nhan='ghép bốn mảnh')]},
 'DL:KSN2.B65#C8': {'value': 10},

 # ⑤ B28
 'DL:KSN2.B28#C1': {'parts': [_o('tâm', ['tâm', 'đỉnh', 'cạnh'], 'gọi là gì')]},
 'DL:KSN2.B28#C2': {'parts': [_o('có', CO_KHONG, 'có bằng nhau không')]},
 'DL:KSN2.B28#C3': {'parts': [_o('hình tròn', ['hình tròn', 'hình vuông', 'hình méo'],
                                 'hình gì')]},
 'DL:KSN2.B28#C4': {'parts': [_o('không', CO_KHONG, 'có phải hình tròn không')]},
 'DL:KSN2.B28#C5': {'parts': [_o('đo nan hoa xem có bằng nhau không',
                                 ['đo nan hoa xem có bằng nhau không',
                                  'nhìn cho kỹ'], 'làm gì')]},
 'DL:KSN2.B28#C6': {'parts': [_o('hình chữ nhật',
                                 ['hình chữ nhật', 'hình tròn', 'hình méo'],
                                 'hình gì')]},
 'DL:KSN2.B28#C7': {'value': 2},
 'DL:KSN2.B28#C8': {'value': 6},

 # ⑥ B66
 'DL:KSN2.B66#C1': {'parts': [_o('ở tâm', ['ở tâm', 'ở viền', 'ở góc'],
                                 'trục đặt ở đâu')]},
 'DL:KSN2.B66#C2': {'parts': [_o('cao đều', ['cao đều', 'lúc nhô lúc tụt'],
                                 'trục thế nào')]},
 'DL:KSN2.B66#C3': {'parts': [_o('xóc', ['xóc', 'êm'], 'xe chạy thế nào')]},
 'DL:KSN2.B66#C4': {'parts': [_o('vì mọi nan hoa đều dài bằng nhau',
                                 ['vì mọi nan hoa đều dài bằng nhau',
                                  'vì bánh tròn nhẹ hơn'], 'vì sao')]},
 'DL:KSN2.B66#C5': {'parts': [_o('dài hơn', ['dài hơn', 'ngắn hơn'],
                                 'nan hoa ra góc')]},
 'DL:KSN2.B66#C6': {'value': 4},
 'DL:KSN2.B66#C7': {'value': 10},
 'DL:KSN2.B66#C8': {'parts': [_o('vì nan hoa chỗ dài chỗ ngắn nên trục nhấp nhô',
                                 ['vì nan hoa chỗ dài chỗ ngắn nên trục nhấp nhô',
                                  'vì bánh vuông nặng hơn'], 'vì sao xóc')]},

 # ⑦ B29
 'DL:KSN2.B29#C1': {'value': 6},
 'DL:KSN2.B29#C2': {'parts': [_o('khối lập phương', LOAI_KHOI, 'khối gì')]},
 'DL:KSN2.B29#C3': {'parts': [_o('khối hộp chữ nhật', LOAI_KHOI, 'khối gì')]},
 'DL:KSN2.B29#C4': {'parts': [_o('hình vuông', LOAI_HINH, 'mặt là hình gì')]},
 'DL:KSN2.B29#C5': {'parts': [
     _o('trên, dưới, trước, sau, trái, phải',
        ['trên, dưới, trước, sau, trái, phải', 'trên, dưới, trái, phải'],
        'sáu mặt')]},
 'DL:KSN2.B29#C6': {'value': 2},
 'DL:KSN2.B29#C7': {'value': 12},
 'DL:KSN2.B29#C8': {'value': 18},

 # ⑧ B67
 'DL:KSN2.B67#C1': {'parts': [_o('hình dẹt', ['hình dẹt', 'khối cầm nắm được'],
                                 'là gì')]},
 'DL:KSN2.B67#C2': {'parts': [_o('khối cầm nắm được',
                                 ['khối cầm nắm được', 'hình dẹt'], 'là gì')]},
 'DL:KSN2.B67#C3': {'parts': [_o('hình vuông', LOAI_HINH, 'được hình gì')]},
 'DL:KSN2.B67#C4': {'parts': [_o('hình chữ nhật', LOAI_HINH, 'được hình gì')]},
 'DL:KSN2.B67#C5': {'parts': [_o('khối lập phương',
                                 ['khối lập phương', 'hình vuông'], 'là gì')]},
 'DL:KSN2.B67#C6': {'parts': [
     _o('in một mặt của nó ra giấy thì được hình gì',
        ['in một mặt của nó ra giấy thì được hình gì', 'nó nặng bao nhiêu'],
        'hỏi câu nào')]},
 'DL:KSN2.B67#C7': {'value': 6},
 'DL:KSN2.B67#C8': {'value': 2},

 # ⑨ B30
 'DL:KSN2.B30#C1': {'parts': [_o('không', CO_KHONG, 'có bay được không')]},
 'DL:KSN2.B30#C2': {'parts': [_o('có', CO_KHONG, 'có khối đỡ không')]},
 'DL:KSN2.B30#C3': {'parts': [_o('có', CO_KHONG, 'có phải đếm không')]},
 'DL:KSN2.B30#C4': {'value': 1},
 'DL:KSN2.B30#C5': {'parts': [_o('vì có khối nấp phía sau hoặc bị che',
                                 ['vì có khối nấp phía sau hoặc bị che',
                                  'vì khối quá nhỏ'], 'vì sao')]},
 'DL:KSN2.B30#C6': {'value': 2},
 'DL:KSN2.B30#C7': {'value': 3},
 'DL:KSN2.B30#C8': {'value': 8},

 # ⑩ B68
 'DL:KSN2.B68#C1': {'value': 4},
 'DL:KSN2.B68#C2': {'value': 5},
 'DL:KSN2.B68#C3': {'parts': [_o('đếm theo từng tầng',
                                 ['đếm theo từng tầng', 'đếm lung tung theo mắt'],
                                 'cách đếm')]},
 'DL:KSN2.B68#C4': {'value': 5},
 'DL:KSN2.B68#C5': {'parts': [_o('hàng nấp phía sau',
                                 ['hàng nấp phía sau', 'khối trên cùng'],
                                 'đếm cả cái gì')]},
 'DL:KSN2.B68#C6': {'value': 9},
 'DL:KSN2.B68#C7': {'value': 14},
 'DL:KSN2.B68#C8': {'parts': [_o(6, nhan='tầng dưới'), _o(2, nhan='tầng trên'),
                              _o(8, nhan='cả tháp')]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (26, 27, 28, 29, 30)}
    moi_ = {f'DL:KSN2.B{n}' for n in (64, 65, 66, 67, 68)}
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
        # Viết tắt đơn vị đo bị máy đọc thành tiếng Anh.
        for tu in (' cm', 'cm ', ' m2'):
            if tu in van:
                loi.append(f'{b["id"]}: còn viết tắt "{tu.strip()}" — phải viết ra chữ')
    NEO = {'DL:KSN2.B26': '3 cạnh', 'DL:KSN2.B64': '3 + 4 + 5 = 12',
           'DL:KSN2.B27': 'đánh số', 'DL:KSN2.B65': '2 + 1 = 3',
           'DL:KSN2.B28': 'nan hoa', 'DL:KSN2.B66': 'tâm',
           'DL:KSN2.B29': '6 mặt', 'DL:KSN2.B67': 'ảnh chụp',
           'DL:KSN2.B30': 'luật ngồi', 'DL:KSN2.B68': '4 + 1 = 5'}
    for b in MOI:
        mong = NEO.get(b['id'])
        if mong and mong not in json.dumps(b, ensure_ascii=False):
            loi.append(f'{b["id"]}: không bám neo "{mong}" của chương')
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
