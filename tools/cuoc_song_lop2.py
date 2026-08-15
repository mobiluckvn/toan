# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 8 · TOÁN TRONG CUỘC SỐNG — ba bài chữ thành sáu bài video.

Chương cuối của quyển. Xong đợt này thì lớp 2 KHÔNG CÒN BÀI CHỮ NÀO.

  · B31 gộp "một nửa của một HÌNH" với "một nửa của một NHÓM đồ vật";
  · B32 gộp "vốn - bán - lãi" với "tiền thừa khi mua hàng";
  · B33 gộp "giờ đúng" với "giờ rưỡi và cộng giờ".

── SỐ NEO ──
    gấp đôi tờ giấy      → một nửa; gấp đôi lần nữa → một phần tư
    8 viên kẹo           → nửa là 8 : 2 = 4; một phần tư là 8 : 4 = 2
    vốn 10 · bán 16      → lãi 16 − 10 = 6; ế thì lỗ 10 − 8 = 2
    đưa 10 mua 7         → thối lại 10 − 7 = 3
    kim phút chỉ 12      → giờ đúng; kim phút chỉ 6 → giờ rưỡi
    kim giờ giữa 3 và 4  → đọc là 3 giờ rưỡi, theo số ĐÃ ĐI QUA

    python3 tools/cuoc_song_lop2.py --xem
    python3 tools/cuoc_song_lop2.py
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

TEN_CHUONG = 'Toán trong cuộc sống'
CHUONG = 8
CO_KHONG = ['có', 'không']
LAI_LO = ['lãi', 'lỗ']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B31 · MỘT NỬA CỦA MỘT HÌNH ═══
B31 = bai(
    31, 'MỘT NỬA VÀ MỘT PHẦN TƯ — CÁC PHẦN PHẢI BẰNG NHAU',
    'PS 1.1a — Một nửa và một phần tư của một hình, điều kiện các phần bằng nhau.',
    video(
        ['Nhận biết một nửa là một trong hai phần bằng nhau.',
         'Nhận biết một phần tư là một trong bốn phần bằng nhau.',
         'Hiểu các phần phải bằng nhau mới được gọi tên như vậy.'],
        ['Đề bài: Gấp một tờ giấy vuông làm đôi rồi làm đôi lần nữa. Mỗi phần được gọi '
         'là gì?',
         'Gấp đôi thật khít',
         'Hai phần chồng khít lên nhau, tức là hai phần bằng nhau. Mỗi phần gọi là '
         'MỘT NỬA.',
         'Gấp đôi thêm lần nữa',
         'Mở ra thì tờ giấy chia thành 4 phần bằng chằn chặn. Mỗi phần gọi là MỘT '
         'PHẦN TƯ.',
         'Luật sống còn: các phần phải BẰNG NHAU',
         'Cắt một miếng to một miếng nhỏ thì hai miếng không chồng khít lên nhau '
         'được, nên không miếng nào được gọi là một nửa cả.',
         'Cùng một cái bánh, chia càng nhiều phần thì mỗi phần càng bé',
         'Miếng một nửa to hơn miếng một phần tư.',
         'Đáp số: gấp đôi được một nửa, gấp đôi hai lần được một phần tư.',
         'Nghe "một nửa" thì chia hai; nghe "một phần tư" thì chia bốn.'],
        ['Có bạn cắt bánh thành hai miếng to nhỏ khác nhau rồi vẫn gọi miếng to là một '
         'nửa.',
         'Gợi ý 1: Con thử đặt hai miếng chồng lên nhau xem có khít không.',
         'Gợi ý 2: Không khít thì hai phần có bằng nhau không?',
         'Chữa: các phần phải bằng nhau mới được gọi là một nửa. Cắt lệch thì không '
         'miếng nào được mang tên ấy.'],
        ['Gấp giấy cùng con là cách nhanh nhất — gấp đôi một lần, rồi gấp đôi lần nữa, '
         'mở ra đếm các phần.',
         'Bố mẹ hỏi: "Hai phần này có chồng khít lên nhau không?"'],
    ),
    [
        lt(1, 1, 'Gấp một tờ giấy làm đôi thì được mấy phần bằng nhau?',
           'Gấp đôi thì được 2 phần bằng nhau.'),
        lt(2, 1, 'Gấp đôi rồi gấp đôi lần nữa thì được mấy phần bằng nhau?',
           'Gấp đôi hai lần thì được 4 phần bằng nhau.'),
        lt(3, 1, 'Một trong hai phần bằng nhau gọi là gì?',
           'Một trong hai phần bằng nhau gọi là một nửa.'),
        lt(4, 2, 'Một trong bốn phần bằng nhau gọi là gì?',
           'Một trong bốn phần bằng nhau gọi là một phần tư.'),
        lt(5, 2, 'Cắt bánh thành hai miếng to nhỏ khác nhau thì miếng to có phải một '
                 'nửa không?',
           'Không phải, vì các phần chưa bằng nhau.'),
        lt(6, 2, 'Cùng một cái bánh, miếng một nửa và miếng một phần tư, miếng nào to '
                 'hơn?',
           'Miếng một nửa to hơn, vì chia càng nhiều phần thì mỗi phần càng bé.'),
        lt(7, 3, 'Gấp đôi ba lần thì tờ giấy được chia thành mấy phần bằng nhau?',
           'Gấp lần đầu được 2 phần, lần hai được 4 phần, lần ba được 8 phần.'),
        lt(8, 3, 'Một cái bánh chia thành 4 phần bằng nhau. Hai phần gộp lại thì bằng '
                 'mấy phần trong hai phần bằng nhau của cái bánh?',
           'Hai phần tư gộp lại vừa đúng 1 nửa cái bánh.'),
    ] + [
        q_tf(1, 'Một nửa là một trong hai phần bằng nhau.', True,
             'Đúng — và chữ "bằng nhau" là chỗ then chốt.'),
        q_mcq(2, 'Gấp đôi hai lần thì được mấy phần bằng nhau?',
              ['4', '2', '3', '8'], '4', 'Mỗi phần là một phần tư.'),
        q_tf(3, 'Cắt hai miếng to nhỏ khác nhau thì miếng to là một nửa.', False,
             'Sai. Các phần phải bằng nhau mới được gọi thế.'),
        q_mcq(4, 'Cùng một cái bánh, miếng nào to hơn?',
              ['một nửa', 'một phần tư', 'bằng nhau'], 'một nửa',
              'Chia càng nhiều phần thì mỗi phần càng bé.'),
        q_tf(5, 'Chia càng nhiều phần thì mỗi phần càng to.', False,
             'Sai. Chia càng nhiều phần thì mỗi phần càng bé.'),
    ],
)

# ═══ ② B69 · MỘT NỬA CỦA MỘT NHÓM ═══
B69 = bai(
    69, 'MỘT NỬA CỦA MỘT NHÓM ĐỒ VẬT',
    'PS 1.1b — Tìm một nửa và một phần tư của một nhóm bằng phép chia.',
    video(
        ['Tìm được một nửa của một nhóm đồ vật.',
         'Tìm được một phần tư của một nhóm đồ vật.',
         'Biết nghe "một nửa" là chia hai, nghe "một phần tư" là chia bốn.'],
        ['Đề bài: Có 8 viên kẹo. Hỏi một nửa số kẹo là mấy viên, và một phần tư số kẹo '
         'là mấy viên?',
         'Một nửa thì chia thành hai phần bằng nhau',
         'Chia 8 viên thành hai phần bằng nhau: 8 : 2 = 4 viên.',
         'Một phần tư thì chia thành bốn phần bằng nhau',
         'Chia 8 viên thành bốn phần bằng nhau: 8 : 4 = 2 viên.',
         'Đáp số: một nửa là 4 viên, một phần tư là 2 viên.',
         'Nghe "một nửa" thì chia hai, nghe "một phần tư" thì chia bốn — phép chia đã '
         'học ở bài chia đều quay lại giúp sức.'],
        ['Có bạn nghe "một phần tư của 8 viên" rồi lấy 8 trừ 4 được 4 viên.',
         'Gợi ý 1: Một phần tư nghĩa là chia thành mấy phần bằng nhau?',
         'Gợi ý 2: Chia đều thành các phần bằng nhau là việc của phép gì?',
         'Chữa: chia thành bốn phần bằng nhau, tức là 8 : 4 = 2 viên.'],
        ['Chia kẹo thật cho hai người rồi cho bốn người — con thấy ngay vì sao một '
         'phần tư bé hơn một nửa.',
         'Bố mẹ hỏi: "Một nửa thì chia mấy, một phần tư thì chia mấy?"'],
    ),
    [
        lt(1, 1, 'Tính 8 : 2.', 'Lấy 8 : 2 = 4.'),
        lt(2, 1, 'Một nửa của 8 viên kẹo là mấy viên?',
           'Chia thành hai phần bằng nhau: 8 : 2 = 4 viên.'),
        lt(3, 1, 'Một phần tư của 8 viên kẹo là mấy viên?',
           'Chia thành bốn phần bằng nhau: 8 : 4 = 2 viên.'),
        lt(4, 2, 'Mẹ có 12 quả quýt và cho một nửa. Được mấy quả?',
           'Chia thành hai phần bằng nhau: 12 : 2 = 6 quả.'),
        lt(5, 2, 'Nghe "một phần tư" thì phải chia cho mấy?',
           'Nghe một phần tư thì chia cho 4.'),
        lt(6, 2, 'Một phần tư của 20 viên bi là mấy viên?',
           'Chia thành bốn phần bằng nhau: 20 : 4 = 5 viên.'),
        lt(7, 3, 'Có 16 cái bánh. Cho biết một nửa là mấy cái và một phần tư là mấy '
                 'cái.',
           'Một nửa là 16 : 2 = 8 cái. Một phần tư là 16 : 4 = 4 cái.'),
        lt(8, 3, 'Một nửa số kẹo trong túi là 7 viên. Cả túi có mấy viên kẹo?',
           'Cả túi gồm hai nửa bằng nhau, nên có 7 + 7 = 14 viên.'),
    ] + [
        q_tf(1, 'Nghe "một nửa" thì chia cho hai.', True,
             'Đúng — hai phần bằng nhau.'),
        q_mcq(2, 'Một nửa của 8 viên kẹo là mấy viên?',
              ['4', '2', '6', '16'], '4', 'Chia tám cho hai.'),
        q_mcq(3, 'Một phần tư của 8 viên kẹo là mấy viên?',
              ['2', '4', '6', '32'], '2', 'Chia tám cho bốn.'),
        q_tf(4, 'Một phần tư của 8 viên là 8 trừ 4, tức 4 viên.', False,
             'Sai. Phải chia bốn, được 2 viên.'),
        q_tf(5, 'Một nửa của 12 quả quýt là 6 quả.', True, 'Đúng — chia mười hai cho '
             'hai.'),
    ],
)

# ═══ ③ B32 · VỐN, BÁN, LÃI ═══
B32 = bai(
    32, 'VỐN, BÁN VÀ LÃI — SỔ CỦA ÔNG CHỦ',
    'PS 5.1a — Tiền vốn, tiền bán, tiền lãi, và khi nào thì lỗ.',
    video(
        ['Phân biệt tiền vốn bỏ ra và tiền bán thu về.',
         'Tính được lãi bằng cách lấy tiền bán trừ tiền vốn.',
         'Nhận ra khi nào bị lỗ.'],
        ['Đề bài: Mua chanh và đường hết 10 nghìn đồng, bán được 4 cốc, mỗi cốc 4 '
         'nghìn. Hỏi lãi bao nhiêu?',
         'Tiền VỐN là tiền bỏ ra trước',
         'Mua chanh và đường hết 10 nghìn. Đó là tiền vốn.',
         'Tiền BÁN là tiền thu về',
         'Bốn cốc, mỗi cốc 4 nghìn, nên thu về 4 × 4 = 16 nghìn.',
         'Tiền LÃI là phần thật sự kiếm thêm',
         'Lấy tiền bán trừ tiền vốn: 16 − 10 = 6 nghìn.',
         'Đáp số: lãi 6 nghìn đồng.',
         'Giàu thêm 6 nghìn chứ không phải 16 nghìn, vì 10 nghìn vốn vốn dĩ đã là của '
         'mình từ đầu.'],
        ['Có bạn bán được 16 nghìn rồi bảo lãi 16 nghìn.',
         'Gợi ý 1: Trong 16 nghìn ấy có bao nhiêu là tiền vốn bỏ ra lúc đầu?',
         'Gợi ý 2: Tiền vốn vốn dĩ đã là của mình rồi, có phải kiếm thêm đâu.',
         'Chữa: lãi bằng tiền bán trừ tiền vốn, tức 16 − 10 = 6 nghìn.'],
        ['Cho con bán nước chanh hay đồ chơi cũ thật một buổi rồi cùng ghi sổ ba dòng '
         'vốn, bán, lãi — bài này học bằng tay là nhớ nhất.',
         'Bố mẹ hỏi: "Trong số tiền thu về, bao nhiêu là vốn của mình?"'],
    ),
    [
        lt(1, 1, 'Mua chanh và đường hết 6 nghìn và 4 nghìn. Tiền vốn là mấy nghìn?',
           'Cộng lại: 6 + 4 = 10 nghìn.'),
        lt(2, 1, 'Bán 4 cốc, mỗi cốc 4 nghìn. Tiền bán là mấy nghìn?',
           'Lấy 4 × 4 = 16 nghìn.'),
        lt(3, 1, 'Vốn 10 nghìn, bán được 16 nghìn. Lãi mấy nghìn?',
           'Lấy tiền bán trừ tiền vốn: 16 − 10 = 6 nghìn.'),
        lt(4, 2, 'Muốn tính lãi thì lấy cái gì trừ cái gì?',
           'Lấy tiền bán trừ tiền vốn.'),
        lt(5, 2, 'Vốn 10 nghìn mà cả ngày chỉ bán được 8 nghìn. Đó là lãi hay lỗ?',
           'Thu về ít hơn bỏ ra nên bị lỗ.'),
        lt(6, 2, 'Vốn 10 nghìn, bán được 8 nghìn. Lỗ mấy nghìn?',
           'Lấy 10 − 8 = 2 nghìn.'),
        lt(7, 3, 'Mua gánh rau hết 12 nghìn, bán cả gánh được 20 nghìn. Lãi mấy nghìn, '
                 'và thử lại vốn cộng lãi được bao nhiêu?',
           'Lãi là 20 − 12 = 8 nghìn. Thử lại: 12 + 8 = 20 nghìn, đúng bằng tiền bán.'),
        lt(8, 3, 'Vốn 15 nghìn, bán 5 cốc mỗi cốc 4 nghìn. Cho biết tiền bán là mấy '
                 'nghìn và lãi mấy nghìn.',
           'Tiền bán là 5 × 4 = 20 nghìn. Lãi là 20 − 15 = 5 nghìn.'),
    ] + [
        q_tf(1, 'Lãi bằng tiền bán trừ tiền vốn.', True,
             'Đúng — đó là dòng thứ ba của sổ ông chủ.'),
        q_mcq(2, 'Vốn 10 nghìn, bán 16 nghìn. Lãi mấy nghìn?',
              ['6', '16', '26', '10'], '6', 'Lấy mười sáu bớt mười.'),
        q_tf(3, 'Bán được 16 nghìn thì lãi 16 nghìn.', False,
             'Sai. Phải trừ đi tiền vốn đã bỏ ra.'),
        q_mcq(4, 'Vốn 10 nghìn mà bán được 8 nghìn thì sao?',
              ['lỗ 2 nghìn', 'lãi 2 nghìn', 'hoà vốn'], 'lỗ 2 nghìn',
              'Thu về ít hơn bỏ ra.'),
        q_tf(5, 'Buôn bán thì lúc nào cũng có lãi.', False,
             'Sai. Bán ít hơn vốn thì bị lỗ.'),
    ],
)

# ═══ ④ B70 · TIỀN THỪA ═══
B70 = bai(
    70, 'TIỀN THỪA — ĐỨNG Ở PHÍA NGƯỜI MUA',
    'PS 5.1b — Tính tiền thối lại và kiểm tra có đủ tiền không.',
    video(
        ['Tính được tiền thối lại khi mua hàng.',
         'Biết tiền thừa bằng tiền đưa trừ tiền mua.',
         'Kiểm tra được có đủ tiền mua hay không.'],
        ['Đề bài: Một cô khách đưa 10 nghìn để mua món hàng giá 7 nghìn. Hỏi phải thối '
         'lại bao nhiêu?',
         'Bài trước đứng ở phía người bán, bài này đứng ở phía người mua',
         'Người mua đưa tiền ra, người bán thối lại phần dư.',
         'Tiền thừa bằng tiền đưa trừ tiền mua',
         'Lấy 10 − 7 = 3 nghìn.',
         'Đáp số: thối lại 3 nghìn đồng.',
         'Muốn biết có đủ tiền mua không thì so tiền mình có với giá món hàng — ít hơn '
         'giá thì chưa mua được.'],
        ['Có bạn cộng tiền đưa với giá món hàng để tính tiền thối.',
         'Gợi ý 1: Thối lại là đưa bớt tiền ra hay nhận thêm tiền vào?',
         'Gợi ý 2: Tiền thối phải ít hơn tiền đưa chứ, đúng không?',
         'Chữa: tiền thừa bằng tiền đưa trừ tiền mua, tức 10 − 7 = 3 nghìn.'],
        ['Cho con cầm tiền đi mua một món nhỏ rồi tự đếm tiền thối — không gì dạy bài '
         'này nhanh bằng một lần đi chợ.',
         'Bố mẹ hỏi: "Con đưa bao nhiêu, món hàng bao nhiêu?"'],
    ),
    [
        lt(1, 1, 'Đưa 10 nghìn mua món 7 nghìn. Thối lại mấy nghìn?',
           'Lấy 10 − 7 = 3 nghìn.'),
        lt(2, 1, 'Tiền thừa bằng cái gì trừ cái gì?',
           'Tiền thừa bằng tiền đưa trừ tiền mua.'),
        lt(3, 1, 'Đưa 20 nghìn mua món 15 nghìn. Thối lại mấy nghìn?',
           'Lấy 20 − 15 = 5 nghìn.'),
        lt(4, 2, 'Đưa 10 nghìn mua 2 cốc nước chanh, mỗi cốc 4 nghìn. Thối lại mấy '
                 'nghìn?',
           'Hai cốc hết 4 × 2 = 8 nghìn, nên thối lại 10 − 8 = 2 nghìn.'),
        lt(5, 2, 'Có 5 nghìn mà món hàng giá 8 nghìn. Có đủ tiền mua không?',
           'Không đủ, vì tiền mình có ít hơn giá món hàng.'),
        lt(6, 2, 'Có 5 nghìn mà món hàng giá 8 nghìn. Còn thiếu mấy nghìn?',
           'Lấy 8 − 5 = 3 nghìn.'),
        lt(7, 3, 'Đưa 50 nghìn mua 3 quyển vở, mỗi quyển 12 nghìn. Cho biết hết mấy '
                 'nghìn và thối lại mấy nghìn.',
           'Ba quyển hết 12 × 3 = 36 nghìn, nên thối lại 50 − 36 = 14 nghìn.'),
        lt(8, 3, 'Có 20 nghìn, mua một cây bút 6 nghìn và một quyển vở 9 nghìn. Cho '
                 'biết hết mấy nghìn và còn lại mấy nghìn.',
           'Hết 6 + 9 = 15 nghìn, còn lại 20 − 15 = 5 nghìn.'),
    ] + [
        q_tf(1, 'Tiền thừa bằng tiền đưa trừ tiền mua.', True,
             'Đúng — đứng ở phía người mua thì tính thế.'),
        q_mcq(2, 'Đưa 10 nghìn mua món 7 nghìn. Thối lại mấy nghìn?',
              ['3', '17', '7', '10'], '3', 'Lấy mười bớt bảy.'),
        q_mcq(3, 'Đưa 20 nghìn mua món 15 nghìn. Thối lại mấy nghìn?',
              ['5', '35', '15', '20'], '5', 'Lấy hai mươi bớt mười lăm.'),
        q_tf(4, 'Tính tiền thối thì cộng tiền đưa với giá món hàng.', False,
             'Sai. Phải trừ, chứ cộng thì tiền thối nhiều hơn tiền đưa.'),
        q_tf(5, 'Có 5 nghìn thì mua được món giá 8 nghìn.', False,
             'Sai. Tiền mình có ít hơn giá nên chưa mua được.'),
    ],
)

# ═══ ⑤ B33 · GIỜ ĐÚNG ═══
B33 = bai(
    33, 'GIỜ ĐÚNG — KIM PHÚT CHỈ SỐ 12',
    'CĐ 6.1a — Phân biệt hai kim và đọc giờ đúng.',
    video(
        ['Phân biệt kim giờ ngắn và kim phút dài.',
         'Đọc được giờ đúng khi kim phút chỉ số 12.',
         'Nhìn kim phút trước rồi mới hỏi kim giờ.'],
        ['Đề bài: Kim phút chỉ số 12, kim giờ chỉ số 3. Hỏi mấy giờ?',
         'Làm quen hai chiếc kim',
         'Kim ngắn và mập là kim giờ. Kim dài là kim phút. Kim giờ đi chậm rãi, kim '
         'phút chạy nhanh hơn nhiều.',
         'Nhìn kim PHÚT trước',
         'Kim phút chỉ thẳng số 12, nghĩa là giờ đúng, không lẻ phút nào.',
         'Rồi mới hỏi kim GIỜ',
         'Kim giờ chỉ số 3, nên đọc là 3 giờ đúng.',
         'Đáp số: 3 giờ.',
         'Cứ nhìn kim phút trước, rồi mới hỏi kim giờ — làm ngược lại là dễ đọc nhầm.'],
        ['Có bạn nhìn nhầm kim dài thành kim giờ, nên đọc sai hẳn.',
         'Gợi ý 1: Kim giờ ngắn hay dài? Kim phút ngắn hay dài?',
         'Gợi ý 2: Kim nào chạy nhanh hơn thì kim ấy đi được quãng dài hơn.',
         'Chữa: kim ngắn và mập là kim giờ, kim dài là kim phút.'],
        ['Chỉ vào đồng hồ trong nhà rồi hỏi con mấy giờ, mỗi ngày vài lần — bài này '
         'học bằng thói quen chứ không bằng vở.',
         'Bố mẹ hỏi: "Kim nào ngắn hơn?"'],
    ),
    [
        lt(1, 1, 'Kim nào ngắn và mập hơn?', 'Kim giờ ngắn và mập hơn kim phút.'),
        lt(2, 1, 'Kim phút chỉ số 12 nghĩa là gì?',
           'Nghĩa là đang ở giờ đúng, không lẻ phút nào.'),
        lt(3, 1, 'Kim phút chỉ 12, kim giờ chỉ 3. Mấy giờ?',
           'Kim phút chỉ 12 nên là giờ đúng, kim giờ chỉ 3 nên là 3 giờ.'),
        lt(4, 2, 'Kim phút chỉ 12, kim giờ chỉ 7. Mấy giờ?',
           'Giờ đúng, và kim giờ chỉ 7 nên là 7 giờ.'),
        lt(5, 2, 'Khi xem giờ thì nên nhìn kim nào trước?',
           'Nhìn kim phút trước, rồi mới hỏi kim giờ.'),
        lt(6, 2, 'Bây giờ 3 giờ. Một giờ nữa là mấy giờ?',
           'Kim giờ tiến thêm đúng một số, nên 3 + 1 = 4 giờ.'),
        lt(7, 3, 'Bây giờ 7 giờ, phim bắt đầu lúc 8 giờ. Còn mấy giờ nữa thì phim bắt '
                 'đầu?',
           'Từ 7 giờ đến 8 giờ, kim giờ đi thêm đúng một số, nên còn 1 giờ.'),
        lt(8, 3, 'Bây giờ 9 giờ. Ba giờ nữa là mấy giờ?',
           'Kim giờ tiến thêm ba số: 9 + 3 = 12 giờ.'),
    ] + [
        q_tf(1, 'Kim ngắn và mập là kim giờ.', True, 'Đúng — kim dài là kim phút.'),
        q_mcq(2, 'Kim phút chỉ 12, kim giờ chỉ 3. Mấy giờ?',
              ['3 giờ', '12 giờ', '3 giờ rưỡi', '4 giờ'], '3 giờ',
              'Kim phút chỉ 12 nên là giờ đúng.'),
        q_tf(3, 'Kim phút chỉ số 12 nghĩa là giờ đúng.', True,
             'Đúng — không lẻ phút nào.'),
        q_mcq(4, 'Khi xem giờ nên nhìn kim nào trước?',
              ['kim phút', 'kim giờ', 'kim nào cũng được'], 'kim phút',
              'Kim phút cho biết là giờ đúng hay giờ rưỡi.'),
        q_tf(5, 'Bây giờ 3 giờ thì một giờ nữa là 4 giờ.', True,
             'Đúng — kim giờ tiến thêm một số.'),
    ],
)

# ═══ ⑥ B71 · GIỜ RƯỠI ═══
B71 = bai(
    71, 'GIỜ RƯỠI — ĐỌC THEO SỐ KIM GIỜ ĐÃ ĐI QUA',
    'CĐ 6.1b — Đọc giờ rưỡi và cộng thêm nửa giờ.',
    video(
        ['Đọc được giờ rưỡi khi kim phút chỉ số 6.',
         'Đọc theo số mà kim giờ đã đi qua.',
         'Cộng được nửa giờ và một giờ.'],
        ['Đề bài: Kim phút chỉ số 6, kim giờ nằm giữa số 3 và số 4. Hỏi mấy giờ?',
         'Kim phút chỉ số 6 nghĩa là đi được một nửa vòng',
         'Nửa vòng là nửa giờ, nên đây là giờ rưỡi.',
         'Kim giờ cũng đi được nửa đường giữa hai số',
         'Nó nằm giữa số 3 và số 4, chưa tới số 4.',
         'Luật đọc: đọc theo số kim giờ ĐÃ ĐI QUA',
         'Kim giờ đã đi qua số 3, nên đọc là 3 giờ rưỡi, chứ không phải 4 giờ rưỡi.',
         'Đáp số: 3 giờ rưỡi.',
         'Từ 3 giờ thêm nửa giờ là 3 giờ rưỡi; từ 3 giờ rưỡi thêm nửa giờ nữa là tròn '
         '4 giờ.'],
        ['Có bạn thấy kim giờ nằm giữa 3 và 4 rồi đọc là 4 giờ rưỡi, vì nó gần số 4.',
         'Gợi ý 1: Kim giờ đã đi qua số nào rồi?',
         'Gợi ý 2: Nó mới mon men tới gần số 4 chứ đã tới đâu.',
         'Chữa: đọc theo số kim giờ đã đi qua, nên là 3 giờ rưỡi.'],
        ['Xoay kim đồng hồ đồ chơi cùng con rồi hỏi mấy giờ, nhất là những lúc kim giờ '
         'nằm giữa hai số.',
         'Bố mẹ hỏi: "Kim giờ đã đi qua số nào rồi?"'],
    ),
    [
        lt(1, 1, 'Kim phút chỉ số 6 nghĩa là gì?',
           'Nghĩa là kim phút đã đi được một nửa vòng, tức là giờ rưỡi.'),
        lt(2, 1, 'Kim phút chỉ 6, kim giờ nằm giữa 3 và 4. Mấy giờ?',
           'Đọc theo số kim giờ đã đi qua, nên là 3 giờ rưỡi.'),
        lt(3, 1, 'Đọc giờ rưỡi thì đọc theo số nào của kim giờ?',
           'Đọc theo số mà kim giờ đã đi qua.'),
        lt(4, 2, 'Kim phút chỉ 6, kim giờ nằm giữa 8 và 9. Mấy giờ?',
           'Kim giờ đã đi qua số 8, nên là 8 giờ rưỡi.'),
        lt(5, 2, 'Bây giờ 3 giờ. Nửa giờ nữa là mấy giờ?',
           'Từ 3 giờ thêm nửa giờ là 3 giờ rưỡi.'),
        lt(6, 2, 'Bây giờ 3 giờ rưỡi. Nửa giờ nữa là mấy giờ?',
           'Từ 3 giờ rưỡi thêm nửa giờ nữa là tròn 4 giờ.'),
        lt(7, 3, 'Kim giờ nằm giữa 6 và 7, kim phút chỉ 6. Có bạn đọc là 7 giờ rưỡi. '
                 'Cho biết bạn ấy sai ở đâu và giờ đúng là mấy.',
           'Bạn ấy đọc theo số kim giờ sắp tới. Phải đọc theo số đã đi qua, nên là 6 '
           'giờ rưỡi.'),
        lt(8, 3, 'Bây giờ 8 giờ rưỡi. Một giờ nữa là mấy giờ?',
           'Kim giờ tiến thêm một số, nên 8 + 1 = 9, tức 9 giờ rưỡi.'),
    ] + [
        q_tf(1, 'Kim phút chỉ số 6 thì đang là giờ rưỡi.', True,
             'Đúng — kim phút đi được nửa vòng.'),
        q_mcq(2, 'Kim phút chỉ 6, kim giờ giữa 3 và 4. Mấy giờ?',
              ['3 giờ rưỡi', '4 giờ rưỡi', '3 giờ', '6 giờ'], '3 giờ rưỡi',
              'Đọc theo số đã đi qua.'),
        q_tf(3, 'Kim giờ nằm giữa 3 và 4 thì đọc là 4 giờ rưỡi.', False,
             'Sai. Phải đọc theo số đã đi qua, tức 3 giờ rưỡi.'),
        q_mcq(4, 'Bây giờ 3 giờ, nửa giờ nữa là mấy giờ?',
              ['3 giờ rưỡi', '4 giờ', '3 giờ', '4 giờ rưỡi'], '3 giờ rưỡi',
              'Nửa giờ là nửa vòng kim phút.'),
        q_tf(5, 'Từ 3 giờ rưỡi thêm nửa giờ nữa là tròn 4 giờ.', True,
             'Đúng — hai nửa giờ thành một giờ.'),
    ],
)

MOI = [B31, B69, B32, B70, B33, B71]

SAU = {
    'DL:KSN2.B69': 'DL:KSN2.B31',
    'DL:KSN2.B70': 'DL:KSN2.B32',
    'DL:KSN2.B71': 'DL:KSN2.B33',
}


def _o(gt, chon=None, nhan=None):
    d = {'value': gt}
    if chon:
        d['options'] = list(chon)
    if nhan:
        d['label'] = nhan
    return d


GIO = ['3 giờ', '4 giờ', '7 giờ', '12 giờ']
GIO_RUOI = ['3 giờ rưỡi', '4 giờ rưỡi', '8 giờ rưỡi', '6 giờ rưỡi', '9 giờ rưỡi']

O_NHAP_MOI = {
 # ① B31
 'DL:KSN2.B31#C1': {'value': 2},
 'DL:KSN2.B31#C2': {'value': 4},
 'DL:KSN2.B31#C3': {'parts': [_o('một nửa', ['một nửa', 'một phần tư'], 'gọi là gì')]},
 'DL:KSN2.B31#C4': {'parts': [_o('một phần tư', ['một nửa', 'một phần tư'],
                                 'gọi là gì')]},
 'DL:KSN2.B31#C5': {'parts': [_o('không', CO_KHONG, 'có phải một nửa không')]},
 'DL:KSN2.B31#C6': {'parts': [_o('một nửa', ['một nửa', 'một phần tư', 'bằng nhau'],
                                 'miếng nào to hơn')]},
 'DL:KSN2.B31#C7': {'value': 8},
 'DL:KSN2.B31#C8': {'value': 1},

 # ② B69
 'DL:KSN2.B69#C1': {'value': 4},
 'DL:KSN2.B69#C2': {'value': 4},
 'DL:KSN2.B69#C3': {'value': 2},
 'DL:KSN2.B69#C4': {'value': 6},
 'DL:KSN2.B69#C5': {'value': 4},
 'DL:KSN2.B69#C6': {'value': 5},
 'DL:KSN2.B69#C7': {'parts': [_o(8, nhan='một nửa'), _o(4, nhan='một phần tư')]},
 'DL:KSN2.B69#C8': {'value': 14},

 # ③ B32
 'DL:KSN2.B32#C1': {'value': 10},
 'DL:KSN2.B32#C2': {'value': 16},
 'DL:KSN2.B32#C3': {'value': 6},
 'DL:KSN2.B32#C4': {'parts': [_o('tiền bán trừ tiền vốn',
                                 ['tiền bán trừ tiền vốn', 'tiền vốn trừ tiền bán'],
                                 'cách tính lãi')]},
 'DL:KSN2.B32#C5': {'parts': [_o('lỗ', LAI_LO, 'lãi hay lỗ')]},
 'DL:KSN2.B32#C6': {'value': 2},
 'DL:KSN2.B32#C7': {'parts': [_o(8, nhan='lãi mấy nghìn'),
                              _o(20, nhan='vốn cộng lãi')]},
 'DL:KSN2.B32#C8': {'parts': [_o(20, nhan='tiền bán'), _o(5, nhan='lãi')]},

 # ④ B70
 'DL:KSN2.B70#C1': {'value': 3},
 'DL:KSN2.B70#C2': {'parts': [_o('tiền đưa trừ tiền mua',
                                 ['tiền đưa trừ tiền mua', 'tiền mua trừ tiền đưa'],
                                 'cách tính')]},
 'DL:KSN2.B70#C3': {'value': 5},
 'DL:KSN2.B70#C4': {'value': 2},
 'DL:KSN2.B70#C5': {'parts': [_o('không', CO_KHONG, 'có đủ tiền không')]},
 'DL:KSN2.B70#C6': {'value': 3},
 'DL:KSN2.B70#C7': {'parts': [_o(36, nhan='hết mấy nghìn'),
                              _o(14, nhan='thối lại mấy nghìn')]},
 'DL:KSN2.B70#C8': {'parts': [_o(15, nhan='hết mấy nghìn'),
                              _o(5, nhan='còn lại mấy nghìn')]},

 # ⑤ B33
 'DL:KSN2.B33#C1': {'parts': [_o('kim giờ', ['kim giờ', 'kim phút'], 'kim nào')]},
 'DL:KSN2.B33#C2': {'parts': [_o('giờ đúng', ['giờ đúng', 'giờ rưỡi'], 'nghĩa là')]},
 'DL:KSN2.B33#C3': {'parts': [_o('3 giờ', GIO, 'mấy giờ')]},
 'DL:KSN2.B33#C4': {'parts': [_o('7 giờ', GIO, 'mấy giờ')]},
 'DL:KSN2.B33#C5': {'parts': [_o('kim phút', ['kim phút', 'kim giờ'], 'nhìn kim nào')]},
 'DL:KSN2.B33#C6': {'value': 4},
 'DL:KSN2.B33#C7': {'value': 1},
 'DL:KSN2.B33#C8': {'value': 12},

 # ⑥ B71
 'DL:KSN2.B71#C1': {'parts': [_o('giờ rưỡi', ['giờ rưỡi', 'giờ đúng'], 'nghĩa là')]},
 'DL:KSN2.B71#C2': {'parts': [_o('3 giờ rưỡi', GIO_RUOI, 'mấy giờ')]},
 'DL:KSN2.B71#C3': {'parts': [_o('số đã đi qua', ['số đã đi qua', 'số sắp tới'],
                                 'đọc theo số nào')]},
 'DL:KSN2.B71#C4': {'parts': [_o('8 giờ rưỡi', GIO_RUOI, 'mấy giờ')]},
 'DL:KSN2.B71#C5': {'parts': [_o('3 giờ rưỡi', GIO_RUOI, 'mấy giờ')]},
 'DL:KSN2.B71#C6': {'parts': [_o('4 giờ', GIO, 'mấy giờ')]},
 'DL:KSN2.B71#C7': {'parts': [_o('đọc theo số kim giờ sắp tới',
                                 ['đọc theo số kim giờ sắp tới', 'không sai gì cả'],
                                 'sai ở đâu'),
                              _o('6 giờ rưỡi', GIO_RUOI, 'giờ đúng là')]},
 'DL:KSN2.B71#C8': {'parts': [_o('9 giờ rưỡi', GIO_RUOI, 'mấy giờ')]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (31, 32, 33)}
    moi_ = {f'DL:KSN2.B{n}' for n in (69, 70, 71)}
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
    NEO = {'DL:KSN2.B31': 'bằng nhau', 'DL:KSN2.B69': '8 : 2 = 4',
           'DL:KSN2.B32': '16 − 10 = 6', 'DL:KSN2.B70': '10 − 7 = 3',
           'DL:KSN2.B33': 'kim phút', 'DL:KSN2.B71': 'đã đi qua'}
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
