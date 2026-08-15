# -*- coding: utf-8 -*-
"""CHƯƠNG 11 · QUÃNG ĐƯỜNG — ba bài chữ thành sáu bài video. Chương cuối quyển.

  · B47 gộp rút về đơn vị, chiều xuôi, chiều ngược, và so hai xe;
  · B48 gộp đuổi kịp với gặp nhau — hai kịch bản ngược nhau, dễ lẫn nhất chương;
  · B49 đứng riêng, và nó nối thẳng vào bài bốn loại góc ở chương 10.

── SỐ NEO ──
    3 giờ đi 120 km   →  nhịp chân 40 km một giờ, chở cả cụm ba bài đầu
    cách nhau 30 km   →  đuổi kịp sau 3 giờ
    hai đầu 180 km    →  gặp nhau sau 3 giờ
    mặt đồng hồ 12 khấc

    python3 tools/quang_duong_lop4.py --xem
    python3 tools/quang_duong_lop4.py
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

TEN_CHUONG = 'QUÃNG ĐƯỜNG VÀ THỜI GIAN'
CHUONG = 11
CO_KHONG = ['có', 'không']

LUI_RUT = {'ve': ['DL:KSN3.B09'], 'ten': ['TÌM MỘT PHẦN MẤY CỦA MỘT SỐ'],
           'canCu': 'chuDe', 'lopDuoi': 3}
LUI_GOC = {'ve': ['DL:KSN3.B27'], 'ten': ['CHU VI CÓ CÔNG THỨC'],
           'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)

# ═══ ① B47 · NHỊP CHÂN MỘT GIỜ ═══
B47 = bai(
    47, 'NHỊP CHÂN MỘT GIỜ — RÚT VỀ ĐƠN VỊ',
    'Dạng gốc: CĐ 1.1 mức Lớp 4 — Rút về đơn vị với quãng đường và thời gian: tìm '
    'quãng đường đi được trong một giờ.',
    'Xe chạy đều, ba giờ đi được một trăm hai mươi ki-lô-mét. Trước khi hỏi gì '
    'thêm, phải biết một con số đã: mỗi giờ nó đi được bao nhiêu.',
    LUI_RUT,
    video(
        ['Hiểu "chạy đều" nghĩa là giờ nào cũng đi được bằng nhau.',
         'Tìm được quãng đường đi trong một giờ bằng cách chia.',
         'Biết vì sao phải tìm con số ấy trước mọi câu hỏi khác.'],
        ['Đề bài: Một xe chạy đều, 3 giờ đi được 120 ki-lô-mét. Hỏi mỗi giờ xe đi được '
         'bao nhiêu ki-lô-mét?',
         'Chạy đều nghĩa là gì',
         'Chạy đều nghĩa là giờ nào xe cũng đi được đúng bằng nhau. Không có giờ nhanh '
         'giờ chậm.',
         'Vậy chia đều ra',
         'Ba giờ chia đường thành ba khúc bằng nhau. Mỗi khúc là quãng đường đi trong '
         'một giờ.',
         'Tính: 120 : 3 = 40 (ki-lô-mét).',
         'Đáp số: mỗi giờ xe đi được 40 ki-lô-mét.',
         'Vì sao con số ấy quan trọng',
         'Bốn mươi ấy là tấm căn cước của chiếc xe. Biết nó rồi thì hỏi gì cũng trả '
         'lời được: hỏi quãng đường, hỏi thời gian, hay so với xe khác.',
         'Thử lại: đi ba giờ thì được 40 × 3 = 120 — đúng đề đã cho.'],
        ['Có bạn thấy đề cho 3 giờ và 120 ki-lô-mét liền nhân luôn: "mỗi giờ đi được '
         '360 ki-lô-mét".',
         'Gợi ý 1: Đi cả ba giờ mới được 120. Vậy đi có một giờ thì được nhiều hơn hay '
         'ít hơn 120?',
         'Gợi ý 2: Ít hơn thì phải làm phép gì — nhân hay chia?',
         'Chữa: một giờ phải đi ÍT HƠN ba giờ, nên phải chia chứ không nhân. Đáp số là '
         '40 ki-lô-mét.'],
        ['Đi đường cùng con, xem đồng hồ và biển báo: nửa tiếng đi được bao nhiêu, một '
         'tiếng bao nhiêu. Con thấy tận mắt nghĩa của "mỗi giờ".',
         'Bài này là nền của cả chương. Con chưa chắc chỗ "mỗi giờ đi được bao nhiêu" '
         'thì mấy bài sau đều tắc.'],
    ),
    [
        lt(1, 1, 'Xe chạy đều, 3 giờ đi được 120 km. Mỗi giờ xe đi được bao nhiêu '
                 'ki-lô-mét?',
           'Chia đều cho số giờ: 120 : 3 = 40 (km).'),
        lt(2, 1, 'Chạy đều nghĩa là các giờ đi được bằng nhau hay khác nhau?',
           'Bằng nhau. Không có giờ nào nhanh hơn giờ nào.'),
        lt(3, 1, 'Thử lại: đi 3 giờ với nhịp 40 km mỗi giờ thì được bao nhiêu km?',
           'Nhân lên: 40 × 3 = 120 (km) — đúng đề đã cho.'),
        lt(4, 2, 'Một xe 4 giờ đi được 200 km. Mỗi giờ đi được bao nhiêu?',
           'Chia đều: 200 : 4 = 50 (km).'),
        lt(5, 2, 'Một người 2 giờ đi được 90 km. Mỗi giờ đi được bao nhiêu?',
           'Chia đều: 90 : 2 = 45 (km).'),
        lt(6, 2, 'Một xe 5 giờ đi được 225 km. Mỗi giờ đi được bao nhiêu?',
           'Chia đều: 225 : 5 = 45 (km).'),
        lt(7, 2, 'Đi cả 3 giờ được 120 km. Vậy đi 1 giờ thì được nhiều hơn hay ít hơn '
                 '120 km?',
           'Ít hơn, vì một giờ chỉ là một phần ba của ba giờ. Nên phải chia chứ không '
           'nhân.'),
        lt(8, 3, 'Một xe 6 giờ đi được 270 km. Mỗi giờ đi bao nhiêu, và trong 2 giờ đi '
                 'được bao nhiêu?',
           'Mỗi giờ: 270 : 6 = 45 (km). Hai giờ: 45 × 2 = 90 (km).'),
        lt(9, 3, 'Một xe đi 3 giờ được 120 km, một xe khác đi 2 giờ được 90 km. Mỗi xe '
                 'đi được bao nhiêu ki-lô-mét trong một giờ?',
           'Xe thứ nhất: 120 : 3 = 40 (km). Xe thứ hai: 90 : 2 = 45 (km).'),
    ] + [
        q_tf(1, 'Chạy đều nghĩa là giờ nào cũng đi được quãng đường bằng nhau.', True,
             'Đúng. Nhờ thế mới chia đều ra được.'),
        q_tf(2, 'Ba giờ đi 120 km thì mỗi giờ đi 360 km.', False,
             'Sai. Một giờ phải đi ít hơn ba giờ, nên phải chia: 120 : 3 = 40 km.'),
        q_mcq(3, 'Xe 3 giờ đi được 120 km thì mỗi giờ đi được',
              ['40 km', '360 km', '120 km', '60 km'], '40 km',
              'Chia đều cho ba giờ.'),
        q_mcq(4, 'Muốn tìm quãng đường đi trong một giờ thì lấy',
              ['quãng đường chia số giờ', 'quãng đường nhân số giờ',
               'số giờ chia quãng đường'], 'quãng đường chia số giờ',
              'Chia đường thành từng ấy khúc bằng nhau, mỗi khúc là một giờ.'),
        q_tf(5, 'Biết quãng đường đi trong một giờ thì trả lời được nhiều câu hỏi '
                'khác.', True, 'Đúng. Đó là con số phải tìm trước tiên.'),
    ],
)

# ═══ ② B93 · BIẾT MỘT GIỜ THÌ TÍNH ĐƯỢC MỌI GIỜ ═══
B93 = bai(
    93, 'BIẾT MỘT GIỜ THÌ TÍNH ĐƯỢC MỌI GIỜ — HAI CHIỀU XUÔI NGƯỢC',
    'Dạng gốc: CĐ 1.1 mức Lớp 4 — Từ quãng đường một giờ, tính quãng đường theo số '
    'giờ và tính số giờ theo quãng đường; suy ra giờ đến.',
    'Bài trước con tìm được con số bốn mươi ki-lô-mét mỗi giờ. Nay dùng nó: hỏi '
    'quãng đường thì nhân, hỏi thời gian thì chia.',
    LUI_RUT,
    video(
        ['Tính quãng đường bằng cách lấy quãng đường một giờ nhân số giờ.',
         'Tính số giờ bằng cách lấy quãng đường chia quãng đường một giờ.',
         'Tính được giờ đến bằng cách cộng số giờ vào giờ xuất phát.'],
        ['Đề bài: Xe đi được 40 ki-lô-mét mỗi giờ. Hỏi 5 giờ xe đi được bao nhiêu, và '
         'đi 200 ki-lô-mét thì hết mấy giờ?',
         'Chiều xuôi: hỏi quãng đường',
         'Mỗi giờ một khúc 40 ki-lô-mét, năm giờ là năm khúc như thế.',
         'Tính: 40 × 5 = 200 (ki-lô-mét).',
         'Chiều ngược: hỏi thời gian',
         'Nay hỏi ngược lại: hai trăm ki-lô-mét chứa được mấy khúc bốn mươi?',
         'Tính: 200 : 40 = 5 (giờ).',
         'Hai chiều ngược nhau: hỏi quãng đường thì nhân, hỏi thời gian thì chia.',
         'Chốt lộ trình',
         'Xuất phát lúc 7 giờ, đi hết 5 giờ, vậy tới nơi lúc 7 + 5 = 12 giờ.',
         'Đáp số: 200 ki-lô-mét, 5 giờ, và tới nơi lúc 12 giờ trưa.'],
        ['Có bạn biết mỗi giờ xe đi 40 km, hỏi đi 200 km hết mấy giờ, liền nhân: '
         '"200 nhân 40 bằng 8 000 giờ".',
         'Gợi ý 1: Tám nghìn giờ là gần một năm. Một chuyến xe có đi lâu thế không?',
         'Gợi ý 2: Con đang hỏi 200 chứa được mấy khúc 40. Đó là phép gì?',
         'Chữa: hỏi thời gian thì chia chứ không nhân. Đáp số là 200 : 40 = 5 giờ.'],
        ['Trước mỗi chuyến đi, cho con tra quãng đường rồi tự tính mất mấy tiếng và '
         'mấy giờ thì tới. Đúng hay sai đường về sẽ biết.',
         'Mẹo chống nhầm: bảo con ước lượng trước bằng lời — "chắc khoảng mấy tiếng" — '
         'rồi mới tính. Đáp số lệch quá xa ước lượng là biết mình làm nhầm phép.'],
    ),
    [
        lt(1, 1, 'Xe đi 40 km mỗi giờ. Trong 5 giờ xe đi được bao nhiêu ki-lô-mét?',
           'Nhân lên: 40 × 5 = 200 (km).'),
        lt(2, 1, 'Xe đi 40 km mỗi giờ. Đi 200 km thì hết mấy giờ?',
           'Chia ra: 200 : 40 = 5 (giờ).'),
        lt(3, 1, 'Hỏi quãng đường thì làm phép gì, hỏi thời gian thì làm phép gì?',
           'Hỏi quãng đường thì nhân, hỏi thời gian thì chia.'),
        lt(4, 2, 'Xe đi 40 km mỗi giờ, xuất phát lúc 7 giờ và đi 5 giờ. Mấy giờ thì '
                 'tới nơi?',
           'Cộng vào giờ xuất phát: 7 + 5 = 12 (giờ).'),
        lt(5, 2, 'Một xe đi 50 km mỗi giờ. Trong 4 giờ đi được bao nhiêu?',
           'Nhân lên: 50 × 4 = 200 (km).'),
        lt(6, 2, 'Một xe đi 45 km mỗi giờ. Đi 225 km thì hết mấy giờ?',
           'Chia ra: 225 : 45 = 5 (giờ).'),
        lt(7, 2, 'Xe đi 60 km mỗi giờ, xuất phát lúc 6 giờ, đi 3 giờ. Mấy giờ tới nơi?',
           'Cộng vào giờ xuất phát: 6 + 3 = 9 (giờ).'),
        lt(8, 3, 'Xe đi 40 km mỗi giờ, phải đi 280 km. Hỏi hết mấy giờ, và xuất phát '
                 'lúc 6 giờ thì mấy giờ tới?',
           'Thời gian: 280 : 40 = 7 (giờ). Giờ tới: 6 + 7 = 13 (giờ).'),
        lt(9, 3, 'Một xe đi 3 giờ được 150 km. Hỏi mỗi giờ đi bao nhiêu, và đi 250 km '
                 'thì hết mấy giờ?',
           'Mỗi giờ: 150 : 3 = 50 (km). Thời gian đi 250 km: 250 : 50 = 5 (giờ).'),
    ] + [
        q_tf(1, 'Quãng đường bằng quãng đường một giờ nhân số giờ.', True,
             'Đúng. Mỗi giờ một khúc, có mấy giờ thì mấy khúc.'),
        q_tf(2, 'Hỏi đi 200 km hết mấy giờ thì lấy 200 nhân 40.', False,
             'Sai. Hỏi thời gian thì chia: 200 : 40 = 5 giờ.'),
        q_mcq(3, 'Xe đi 40 km mỗi giờ thì 5 giờ đi được',
              ['200 km', '45 km', '8 km', '2 000 km'], '200 km',
              'Lấy 40 nhân 5.'),
        q_mcq(4, 'Xe đi 40 km mỗi giờ, đi 200 km thì hết',
              ['5 giờ', '8 000 giờ', '160 giờ', '240 giờ'], '5 giờ',
              'Lấy 200 chia 40.'),
        q_tf(5, 'Giờ đến bằng giờ xuất phát cộng số giờ đi đường.', True,
             'Đúng, khi xe đi liền một mạch không nghỉ.'),
    ],
)

# ═══ ③ B94 · SO HAI XE PHẢI QUY VỀ CÙNG MỘT GIỜ ═══
B94 = bai(
    94, 'SO HAI XE — PHẢI QUY VỀ CÙNG MỘT GIỜ',
    'Dạng gốc: CĐ 1.1 mức Lớp 4 — So sánh hai chuyển động bằng cách quy cả hai về '
    'quãng đường đi trong một giờ.',
    'Xe này ba giờ đi 120 ki-lô-mét, xe kia hai giờ đi 90. Xe nào nhanh hơn? Nhìn '
    'hai con số 120 và 90 mà kết luận là mắc bẫy ngay.',
    LUI_RUT,
    video(
        ['Biết không so được hai quãng đường đi trong số giờ khác nhau.',
         'Quy cả hai về quãng đường đi trong một giờ rồi mới so.',
         'Nói được vì sao phải quy về cùng một giờ.'],
        ['Đề bài: Xe buýt 3 giờ đi được 120 ki-lô-mét. Xe chở đồ 2 giờ đi được 90 '
         'ki-lô-mét. Xe nào đi nhanh hơn?',
         'Cái bẫy',
         'Một trăm hai mươi lớn hơn chín mươi, nên nhiều bạn kết luận ngay xe buýt '
         'nhanh hơn. Nhưng hai con số ấy đo trong số giờ khác nhau.',
         'Giống như so hai bạn ăn cơm: một bạn ăn ba bát trong ba bữa, một bạn ăn hai '
         'bát trong một bữa. So thẳng thì vô nghĩa.',
         'Quy về cùng một giờ',
         'Xe buýt: 120 : 3 = 40 (ki-lô-mét mỗi giờ).',
         'Xe chở đồ: 90 : 2 = 45 (ki-lô-mét mỗi giờ).',
         'Nay mới so được',
         'Bốn mươi lăm lớn hơn bốn mươi, nên xe chở đồ đi nhanh hơn.',
         'Đáp số: xe chở đồ nhanh hơn, hơn 5 ki-lô-mét mỗi giờ.',
         'Bài học chung: muốn so hai thứ thì phải đưa chúng về cùng một thước đo.'],
        ['Có bạn nhìn 120 và 90 rồi kết luận: "Xe buýt đi được xa hơn nên nhanh hơn."',
         'Gợi ý 1: Xe buýt đi mấy giờ mới được 120? Còn xe kia đi mấy giờ được 90?',
         'Gợi ý 2: Hai con số ấy đo trong khoảng thời gian khác nhau. Muốn so thì phải '
         'đưa về cùng cái gì?',
         'Chữa: quy cả hai về một giờ đã. Xe buýt 40, xe chở đồ 45 — hoá ra xe chở đồ '
         'mới là xe nhanh hơn.'],
        ['So giá ngoài siêu thị cùng con: gói 500 gam giá này, gói 1 ki-lô-gam giá kia, '
         'gói nào rẻ hơn. Cũng đúng một lối nghĩ — quy về cùng một đơn vị.',
         'Đây là bài dạy một thói quen chứ không phải một công thức: trước khi so cái '
         'gì, hỏi xem hai bên có cùng thước đo chưa.'],
    ),
    [
        lt(1, 1, 'Xe buýt 3 giờ đi 120 km. Mỗi giờ xe buýt đi được bao nhiêu?',
           'Chia đều: 120 : 3 = 40 (km).'),
        lt(2, 1, 'Xe chở đồ 2 giờ đi 90 km. Mỗi giờ xe chở đồ đi được bao nhiêu?',
           'Chia đều: 90 : 2 = 45 (km).'),
        lt(3, 1, 'Vậy xe nào đi nhanh hơn?',
           'Xe chở đồ, vì 45 km mỗi giờ nhiều hơn 40 km mỗi giờ.'),
        lt(4, 2, 'Xe chở đồ hơn xe buýt bao nhiêu ki-lô-mét mỗi giờ?',
           'Lấy hiệu: 45 − 40 = 5 (km mỗi giờ).'),
        lt(5, 2, 'Vì sao không so thẳng 120 với 90 được?',
           'Vì hai quãng đường ấy đo trong số giờ khác nhau, không cùng một thước đo.'),
        lt(6, 2, 'Xe A 4 giờ đi 200 km, xe B 3 giờ đi 165 km. Mỗi xe đi bao nhiêu '
                 'ki-lô-mét mỗi giờ?',
           'Xe A: 200 : 4 = 50 (km). Xe B: 165 : 3 = 55 (km).'),
        lt(7, 2, 'Trong hai xe ấy, xe nào nhanh hơn?',
           'Xe B, vì 55 km mỗi giờ nhiều hơn 50 km mỗi giờ.'),
        lt(8, 3, 'Xe A 5 giờ đi 300 km, xe B 4 giờ đi 240 km. Tính nhịp mỗi xe rồi cho '
                 'biết hai xe thế nào.',
           'Xe A: 300 : 5 = 60 (km mỗi giờ). Xe B: 240 : 4 = 60 (km mỗi giờ). Hai xe '
           'đi nhanh bằng nhau.'),
        lt(9, 3, 'Xe A 2 giờ đi 130 km, xe B 3 giờ đi 180 km. Xe nào nhanh hơn và hơn '
                 'bao nhiêu ki-lô-mét mỗi giờ?',
           'Xe A: 130 : 2 = 65 (km). Xe B: 180 : 3 = 60 (km). Xe A nhanh hơn 65 − 60 = '
           '5 (km mỗi giờ).'),
    ] + [
        q_tf(1, 'So hai xe thì so thẳng hai quãng đường là được.', False,
             'Sai, nếu hai quãng đường ấy đo trong số giờ khác nhau.'),
        q_tf(2, 'Muốn so hai xe thì quy cả hai về quãng đường đi trong một giờ.', True,
             'Đúng. Cùng một thước đo thì mới so được.'),
        q_mcq(3, 'Xe buýt 3 giờ đi 120 km, xe chở đồ 2 giờ đi 90 km. Xe nào nhanh hơn?',
              ['xe chở đồ', 'xe buýt', 'bằng nhau'], 'xe chở đồ',
              'Quy về một giờ: 40 và 45, nên xe chở đồ nhanh hơn.'),
        q_mcq(4, 'Xe chở đồ hơn xe buýt mỗi giờ bao nhiêu ki-lô-mét?',
              ['5 km', '30 km', '45 km', '1 km'], '5 km',
              'Lấy 45 trừ 40.'),
        q_tf(5, 'Muốn so hai thứ thì phải đưa chúng về cùng một thước đo.', True,
             'Đúng. Bài này dạy một thói quen chứ không phải một công thức.'),
    ],
)

# ═══ ④ B48 · ĐUỔI KỊP ═══
B48 = bai(
    48, 'ĐUỔI KỊP — MỖI GIỜ KHÉP LẠI ĐƯỢC BAO NHIÊU',
    'Dạng gốc: CĐ 2.1 mức Lớp 4 — Bài toán đuổi kịp: khoảng cách khép lại mỗi giờ '
    'bằng hiệu hai nhịp chân.',
    'Xe đồ đi trước 30 ki-lô-mét, xe buýt đuổi theo. Xe buýt nhanh hơn, nên mỗi giờ '
    'lại rút ngắn được một ít. Bao lâu thì bắt kịp?',
    LUI_RUT,
    video(
        ['Biết khi cùng chiều thì mỗi giờ khoảng cách khép lại bằng hiệu hai nhịp.',
         'Tính được thời gian đuổi kịp bằng khoảng cách chia hiệu.',
         'Kiểm lại bằng hai cột quãng đường: lúc kịp thì hai xe đứng cùng một chỗ.'],
        ['Đề bài: Xe chở đồ đi trước 30 ki-lô-mét, mỗi giờ đi 30 ki-lô-mét. Xe buýt '
         'đuổi theo cùng chiều, mỗi giờ đi 40 ki-lô-mét. Hỏi sau bao lâu xe buýt đuổi '
         'kịp?',
         'Lập bảng cho dễ thấy',
         'Lúc xuất phát hai xe cách nhau 30 ki-lô-mét.',
         'Sau một giờ, xe buýt đi 40 còn xe đồ đi 30, nên khoảng cách còn 20.',
         'Sau hai giờ còn 10. Sau ba giờ còn 0 — đuổi kịp.',
         'Quy luật lộ ra',
         'Mỗi giờ khoảng cách khép lại đúng 10 ki-lô-mét, mà 10 chính là 40 trừ 30 — '
         'hiệu hai nhịp chân.',
         'Nên thời gian đuổi kịp bằng khoảng cách ban đầu chia cho hiệu: 30 : 10 = 3 '
         '(giờ).',
         'Đáp số: sau 3 giờ.',
         'Kiểm bằng hai cột quãng đường',
         'Lúc kịp, xe buýt đã đi 40 × 3 = 120. Xe đồ đi 30 × 3 = 90, cộng 30 đi trước '
         'là 120. Hai xe đứng đúng một chỗ.'],
        ['Có bạn tính thời gian đuổi kịp bằng cách lấy khoảng cách chia cho TỔNG hai '
         'nhịp: 30 chia cho 70.',
         'Gợi ý 1: Hai xe đi cùng chiều hay ngược chiều? Xe đi trước có chạy về phía '
         'xe sau không?',
         'Gợi ý 2: Sau một giờ, xe buýt đi 40 mà xe đồ cũng đi thêm 30. Khoảng cách '
         'rút ngắn được đúng bao nhiêu?',
         'Chữa: đi cùng chiều thì xe trước cũng chạy đi, nên mỗi giờ chỉ khép được '
         'phần HƠN, tức hiệu 40 − 30 = 10. Thời gian là 30 : 10 = 3 giờ.'],
        ['Chơi trò đuổi bắt ngoài sân: bố mẹ đi trước mấy bước rồi cùng bước đều, con '
         'bước dài hơn. Đếm xem mấy bước thì bắt kịp.',
         'Chỗ khó duy nhất là nhớ dùng HIỆU. Bố mẹ hỏi một câu: "Người đi trước có '
         'đứng yên không?" — không đứng yên thì phải trừ.'],
    ),
    [
        lt(1, 1, 'Xe buýt đi 40 km mỗi giờ, xe đồ đi 30 km mỗi giờ. Mỗi giờ xe buýt '
                 'rút ngắn được bao nhiêu ki-lô-mét?',
           'Lấy hiệu hai nhịp: 40 − 30 = 10 (km).'),
        lt(2, 1, 'Hai xe cách nhau 30 km. Sau 1 giờ còn cách nhau bao nhiêu?',
           'Khép được 10 km nên còn 30 − 10 = 20 (km).'),
        lt(3, 1, 'Vậy sau bao nhiêu giờ thì xe buýt đuổi kịp?',
           'Lấy khoảng cách chia hiệu: 30 : 10 = 3 (giờ).'),
        lt(4, 2, 'Lúc đuổi kịp, xe buýt đã đi được bao nhiêu ki-lô-mét?',
           'Nhân lên: 40 × 3 = 120 (km).'),
        lt(5, 2, 'Lúc ấy xe đồ đã đi thêm bao nhiêu, và tính cả 30 km đi trước thì '
                 'tổng bằng bao nhiêu?',
           'Xe đồ đi thêm 30 × 3 = 90 (km). Cộng phần đi trước: 90 + 30 = 120 (km) — '
           'đúng bằng xe buýt.'),
        lt(6, 2, 'Hai xe cách nhau 60 km, nhịp 50 và 40 km mỗi giờ. Sau bao lâu đuổi '
                 'kịp?',
           'Hiệu hai nhịp: 50 − 40 = 10 (km). Thời gian: 60 : 10 = 6 (giờ).'),
        lt(7, 2, 'Hai xe cách nhau 24 km, nhịp 45 và 33 km mỗi giờ. Sau bao lâu đuổi '
                 'kịp?',
           'Hiệu hai nhịp: 45 − 33 = 12 (km). Thời gian: 24 : 12 = 2 (giờ).'),
        lt(8, 3, 'Muốn tính thời gian đuổi kịp thì lấy khoảng cách chia cho tổng hay '
                 'chia cho hiệu hai nhịp?',
           'Chia cho hiệu, vì người đi trước cũng đang chạy nên mỗi giờ chỉ khép được '
           'phần hơn.'),
        lt(9, 3, 'Hai xe cách nhau 45 km, xe sau đi 60 km mỗi giờ và đuổi kịp sau 3 '
                 'giờ. Xe trước đi bao nhiêu ki-lô-mét mỗi giờ?',
           'Mỗi giờ khép được 45 : 3 = 15 (km) — đó là hiệu hai nhịp. Nhịp xe trước: '
           '60 − 15 = 45 (km mỗi giờ).'),
    ] + [
        q_tf(1, 'Đi cùng chiều thì mỗi giờ khoảng cách khép lại bằng hiệu hai nhịp.',
             True, 'Đúng, vì người đi trước cũng đang chạy.'),
        q_tf(2, 'Thời gian đuổi kịp bằng khoảng cách chia tổng hai nhịp.', False,
             'Sai. Cùng chiều thì chia cho hiệu.'),
        q_mcq(3, 'Cách 30 km, nhịp 40 và 30 km mỗi giờ. Sau bao lâu đuổi kịp?',
              ['3 giờ', '30 giờ', '1 giờ', '7 giờ'], '3 giờ',
              'Hiệu hai nhịp là 10, rồi 30 chia 10 được 3.'),
        q_mcq(4, 'Lúc đuổi kịp, hai xe',
              ['đứng cùng một chỗ', 'cách nhau như cũ', 'xe sau vượt lên trước'],
              'đứng cùng một chỗ',
              'Đó cũng là cách kiểm lại bằng hai cột quãng đường.'),
        q_tf(5, 'Kiểm bài đuổi kịp bằng cách tính quãng đường của cả hai xe rồi so.',
             True, 'Đúng. Hai bên phải bằng nhau.'),
    ],
)

# ═══ ⑤ B95 · GẶP NHAU ═══
B95 = bai(
    95, 'GẶP NHAU — MỖI GIỜ GẦN THÊM ĐƯỢC BAO NHIÊU',
    'Dạng gốc: CĐ 3.1 mức Lớp 4 — Bài toán gặp nhau khi đi ngược chiều: mỗi giờ '
    'gần thêm bằng tổng hai nhịp chân.',
    'Bài trước hai xe đi cùng chiều. Nay hai xe từ hai đầu chạy vào nhau. Cùng một '
    'lối nghĩ, nhưng đổi một dấu — và đúng chỗ ấy hay nhầm nhất.',
    LUI_RUT,
    video(
        ['Biết khi đi ngược chiều thì mỗi giờ hai xe gần thêm bằng tổng hai nhịp.',
         'Tính được thời gian gặp nhau bằng quãng đường chia tổng.',
         'Phân biệt được với bài đuổi kịp: cùng chiều thì hiệu, ngược chiều thì tổng.'],
        ['Đề bài: Hai đầu một quãng đường dài 180 ki-lô-mét, hai xe cùng lúc chạy vào '
         'nhau. Xe thứ nhất mỗi giờ đi 25 ki-lô-mét, xe thứ hai mỗi giờ đi 35 '
         'ki-lô-mét. Hỏi sau bao lâu hai xe gặp nhau?',
         'Cả hai cùng lao vào',
         'Lần này không ai chạy trốn cả. Sau một giờ, xe thứ nhất đi được 25, xe thứ '
         'hai đi được 35 — hai bên gần thêm nhau cả hai phần.',
         'Mỗi giờ gần thêm: 25 + 35 = 60 (ki-lô-mét).',
         'Chia ra là xong',
         'Cả quãng đường 180 ki-lô-mét, mỗi giờ nuốt được 60, nên hết 180 : 60 = 3 '
         '(giờ).',
         'Đáp số: sau 3 giờ hai xe gặp nhau.',
         'Kiểm bằng hai cột quãng đường',
         'Xe thứ nhất đi 25 × 3 = 75. Xe thứ hai đi 35 × 3 = 105. Cộng lại 75 + 105 = '
         '180 — vừa đúng cả quãng đường.',
         'Nhớ cho kỹ chỗ khác nhau',
         'Cùng chiều là đuổi, mỗi giờ khép bằng HIỆU. Ngược chiều là gặp, mỗi giờ gần '
         'thêm bằng TỔNG.'],
        ['Có bạn làm bài gặp nhau mà vẫn lấy hiệu hai nhịp, ra 180 chia 10 bằng 18 giờ.',
         'Gợi ý 1: Hai xe đi cùng chiều hay chạy vào nhau? Cả hai có cùng làm quãng '
         'đường ngắn lại không?',
         'Gợi ý 2: Sau một giờ, phần đường bị nuốt mất gồm phần của xe nào?',
         'Chữa: chạy vào nhau thì cả hai cùng góp, nên phải cộng: 25 + 35 = 60. Thời '
         'gian là 180 : 60 = 3 giờ.'],
        ['Hai người đứng hai đầu hành lang rồi cùng bước vào nhau. Đếm xem mấy bước thì '
         'chạm — cả hai cùng bước nên nhanh gấp đôi.',
         'Cách phân biệt gọn nhất: hỏi con "hai xe đi cùng chiều hay ngược chiều?" '
         'trước khi làm bất cứ phép tính nào.'],
    ),
    [
        lt(1, 1, 'Hai xe chạy vào nhau, nhịp 25 và 35 km mỗi giờ. Mỗi giờ hai xe gần '
                 'thêm nhau bao nhiêu ki-lô-mét?',
           'Cả hai cùng góp nên lấy tổng: 25 + 35 = 60 (km).'),
        lt(2, 1, 'Quãng đường dài 180 km. Sau bao lâu hai xe gặp nhau?',
           'Lấy quãng đường chia tổng: 180 : 60 = 3 (giờ).'),
        lt(3, 1, 'Đi ngược chiều thì mỗi giờ gần thêm bằng tổng hay hiệu hai nhịp?',
           'Bằng tổng, vì cả hai cùng làm quãng đường ngắn lại.'),
        lt(4, 2, 'Lúc gặp nhau, xe thứ nhất đã đi được bao nhiêu ki-lô-mét?',
           'Nhân lên: 25 × 3 = 75 (km).'),
        lt(5, 2, 'Lúc ấy xe thứ hai đi được bao nhiêu, và hai phần cộng lại bằng bao '
                 'nhiêu?',
           'Xe thứ hai: 35 × 3 = 105 (km). Cộng lại: 75 + 105 = 180 (km) — đúng cả '
           'quãng đường.'),
        lt(6, 2, 'Hai đầu cách nhau 240 km, hai xe chạy vào nhau với nhịp 50 và 30 km '
                 'mỗi giờ. Sau bao lâu gặp nhau?',
           'Tổng hai nhịp: 50 + 30 = 80 (km). Thời gian: 240 : 80 = 3 (giờ).'),
        lt(7, 2, 'Hai đầu cách nhau 150 km, nhịp 45 và 30 km mỗi giờ. Sau bao lâu gặp '
                 'nhau?',
           'Tổng hai nhịp: 45 + 30 = 75 (km). Thời gian: 150 : 75 = 2 (giờ).'),
        lt(8, 3, 'Bài đuổi kịp chia cho hiệu, bài gặp nhau chia cho tổng. Vì sao lại '
                 'khác nhau như thế?',
           'Cùng chiều thì người đi trước cũng chạy đi nên chỉ khép được phần hơn, tức '
           'hiệu. Ngược chiều thì cả hai cùng lao vào nên góp cả hai phần, tức tổng.'),
        lt(9, 3, 'Hai đầu cách nhau 210 km, hai xe gặp nhau sau 3 giờ, xe thứ nhất đi '
                 '30 km mỗi giờ. Xe thứ hai đi bao nhiêu ki-lô-mét mỗi giờ?',
           'Mỗi giờ hai xe gần thêm 210 : 3 = 70 (km) — đó là tổng hai nhịp. Nhịp xe '
           'thứ hai: 70 − 30 = 40 (km mỗi giờ).'),
    ] + [
        q_tf(1, 'Đi ngược chiều thì mỗi giờ hai xe gần thêm bằng tổng hai nhịp.', True,
             'Đúng, vì cả hai cùng làm quãng đường ngắn lại.'),
        q_tf(2, 'Bài gặp nhau cũng chia cho hiệu hai nhịp như bài đuổi kịp.', False,
             'Sai. Gặp nhau thì chia cho tổng.'),
        q_mcq(3, 'Hai đầu 180 km, nhịp 25 và 35 km mỗi giờ. Sau bao lâu gặp nhau?',
              ['3 giờ', '18 giờ', '6 giờ', '5 giờ'], '3 giờ',
              'Tổng hai nhịp là 60, rồi 180 chia 60 được 3.'),
        q_mcq(4, 'Lúc gặp nhau, tổng quãng đường hai xe đã đi bằng',
              ['cả quãng đường ban đầu', 'một nửa quãng đường', 'gấp đôi quãng đường'],
              'cả quãng đường ban đầu',
              'Đó cũng là cách kiểm lại bài gặp nhau.'),
        q_tf(5, 'Cùng chiều thì hiệu, ngược chiều thì tổng.', True,
             'Đúng. Nhớ đúng một câu ấy là không lẫn hai bài.'),
    ],
)

# ═══ ⑥ B49 · GÓC GIỮA HAI KIM ĐỒNG HỒ ═══
B49 = bai(
    49, 'GÓC GIỮA HAI KIM ĐỒNG HỒ — ĐẾM KHẤC',
    'Dạng gốc: CĐ 6.1 mức Lớp 4 — Góc giữa hai kim đồng hồ tại các giờ đúng; nối '
    'với bài bốn loại góc.',
    'Bài cuối quyển, và nó bắt tay với bài bốn loại góc con đã học. Mặt đồng hồ '
    'chính là một cái thước đo góc có sẵn trong nhà.',
    LUI_GOC,
    video(
        ['Biết mặt đồng hồ chia thành 12 khấc bằng nhau.',
         'Biết góc vuông là 3 khấc và góc bẹt là 6 khấc.',
         'Gọi tên được góc giữa hai kim tại một giờ đúng bất kỳ.'],
        ['Đề bài: Lúc 3 giờ đúng và lúc 6 giờ đúng, hai kim đồng hồ tạo thành góc gì?',
         'Mặt đồng hồ là một cái thước',
         'Mười hai con số chia vòng tròn thành 12 khấc bằng nhau.',
         'Ướm ê ke vào: góc vuông phủ từ số 12 tới số 3, đúng 3 khấc.',
         'Nửa vòng là góc bẹt, và nửa vòng thì đúng 6 khấc.',
         'Đọc mặt đồng hồ',
         'Giờ đúng thì kim phút luôn chỉ số 12. Nên chỉ cần đếm khấc từ số 12 tới kim '
         'giờ.',
         'Lúc 3 giờ: đếm được 3 khấc, đúng bằng góc vuông.',
         'Lúc 6 giờ: đếm được 6 khấc, đúng bằng góc bẹt — hai kim duỗi thẳng.',
         'Đáp số: 3 giờ là góc vuông, 6 giờ là góc bẹt.',
         'Điểm danh cả mặt đồng hồ',
         'Dưới 3 khấc thì góc nhọn, đúng 3 khấc là vuông, từ 4 tới 5 khấc là tù, đúng '
         '6 khấc là bẹt.',
         'Quá 6 khấc thì đếm phía ngắn: lúc 7 giờ đếm ngược chỉ 5 khấc, nên vẫn là góc '
         'tù.'],
        ['Có bạn xem đồng hồ lúc 7 giờ rồi đếm xuôi từ 12 tới 7 được 7 khấc, và bảo '
         '"góc ấy lớn hơn góc bẹt".',
         'Gợi ý 1: Hai kim tạo ra hai góc, một góc bên này và một góc bên kia. Con lấy '
         'góc nào?',
         'Gợi ý 2: Đếm ngược từ số 12 sang trái tới số 7 xem được mấy khấc.',
         'Chữa: góc giữa hai kim luôn lấy phía NGẮN. Đếm ngược chỉ 5 khấc, nên lúc 7 '
         'giờ là góc tù, giống hệt lúc 5 giờ.'],
        ['Lấy đồng hồ kim thật trong nhà, xoay kim tới từng giờ đúng và cho con gọi '
         'tên góc. Có thể ướm ê ke vào kiểm.',
         'Trò hay: bố mẹ đọc một loại góc, con phải chỉnh kim tới đúng giờ tạo ra góc '
         'ấy. Có giờ có tới hai đáp án, ví dụ 3 giờ và 9 giờ.'],
    ),
    [
        lt(1, 1, 'Mặt đồng hồ chia thành bao nhiêu khấc bằng nhau?',
           'Mười hai con số chia vòng tròn thành 12 khấc.'),
        lt(2, 1, 'Góc vuông phủ mấy khấc trên mặt đồng hồ?',
           'Từ số 12 tới số 3 là 3 khấc.'),
        lt(3, 1, 'Góc bẹt phủ mấy khấc?',
           'Nửa vòng, tức 6 khấc.'),
        lt(4, 2, 'Lúc 3 giờ đúng, hai kim tạo thành góc gì?',
           'Kim phút ở số 12, kim giờ ở số 3, cách nhau 3 khấc nên là góc vuông.'),
        lt(5, 2, 'Lúc 6 giờ đúng, hai kim tạo thành góc gì?',
           'Cách nhau 6 khấc, hai kim duỗi thẳng nên là góc bẹt.'),
        lt(6, 2, 'Lúc 2 giờ đúng, hai kim tạo thành góc gì?',
           'Cách nhau 2 khấc, dưới 3 khấc nên là góc nhọn.'),
        lt(7, 2, 'Lúc 5 giờ đúng, hai kim tạo thành góc gì?',
           'Cách nhau 5 khấc, hơn 3 mà chưa tới 6 nên là góc tù.'),
        lt(8, 3, 'Lúc 7 giờ đúng, đếm phía ngắn thì được mấy khấc, và đó là góc gì?',
           'Đếm ngược từ số 12 tới số 7 được 5 khấc, nên là góc tù — giống lúc 5 giờ.'),
        lt(9, 3, 'Ngoài 3 giờ ra, còn giờ đúng nào nữa mà hai kim tạo thành góc vuông?',
           'Lúc 9 giờ. Đếm phía ngắn từ số 12 sang trái tới số 9 cũng được 3 khấc.'),
    ] + [
        q_tf(1, 'Mặt đồng hồ chia thành 12 khấc bằng nhau.', True,
             'Đúng, mỗi con số một khấc.'),
        q_mcq(2, 'Lúc 3 giờ đúng, hai kim tạo thành',
              ['góc vuông', 'góc nhọn', 'góc tù', 'góc bẹt'], 'góc vuông',
              'Cách nhau đúng 3 khấc.'),
        q_mcq(3, 'Lúc 6 giờ đúng, hai kim tạo thành',
              ['góc bẹt', 'góc vuông', 'góc nhọn', 'góc tù'], 'góc bẹt',
              'Cách nhau 6 khấc, hai kim duỗi thẳng thành một đường.'),
        q_tf(4, 'Lúc 7 giờ, góc giữa hai kim lớn hơn góc bẹt.', False,
             'Sai. Góc giữa hai kim lấy phía ngắn, đếm được 5 khấc nên là góc tù.'),
        q_tf(5, 'Lúc 12 giờ đúng, hai kim trùng nhau.', True,
             'Đúng, cách nhau 0 khấc.'),
    ],
)

MOI = [B47, B93, B94, B48, B95, B49]

SAU = {
    'DL:KSN4.B93': 'DL:KSN4.B47',
    'DL:KSN4.B94': 'DL:KSN4.B93',
    'DL:KSN4.B95': 'DL:KSN4.B48',
}

BON_GOC = ['góc nhọn', 'góc vuông', 'góc tù', 'góc bẹt']

O_NHAP_MOI = {
 'DL:KSN4.B47#C1': {'value': 40},
 'DL:KSN4.B47#C2': {'parts': [{'label': 'các giờ thế nào',
                               'options': ['bằng nhau', 'khác nhau'],
                               'value': 'bằng nhau'}]},
 'DL:KSN4.B47#C3': {'value': 120},
 'DL:KSN4.B47#C4': {'value': 50},
 'DL:KSN4.B47#C5': {'value': 45},
 'DL:KSN4.B47#C6': {'value': 45},
 'DL:KSN4.B47#C7': {'parts': [{'label': 'nhiều hơn hay ít hơn',
                               'options': ['ít hơn', 'nhiều hơn'], 'value': 'ít hơn'}]},
 'DL:KSN4.B47#C8': {'parts': [{'label': 'mỗi giờ', 'value': 45},
                              {'label': 'trong 2 giờ', 'value': 90}]},
 'DL:KSN4.B47#C9': {'parts': [{'label': 'xe thứ nhất', 'value': 40},
                              {'label': 'xe thứ hai', 'value': 45}]},

 'DL:KSN4.B93#C1': {'value': 200},
 'DL:KSN4.B93#C2': {'value': 5},
 'DL:KSN4.B93#C3': {'parts': [{'label': 'hỏi quãng đường thì',
                               'options': ['nhân', 'chia'], 'value': 'nhân'},
                              {'label': 'hỏi thời gian thì',
                               'options': ['nhân', 'chia'], 'value': 'chia'}]},
 'DL:KSN4.B93#C4': {'value': 12},
 'DL:KSN4.B93#C5': {'value': 200},
 'DL:KSN4.B93#C6': {'value': 5},
 'DL:KSN4.B93#C7': {'value': 9},
 'DL:KSN4.B93#C8': {'parts': [{'label': 'hết mấy giờ', 'value': 7},
                              {'label': 'mấy giờ tới nơi', 'value': 13}]},
 'DL:KSN4.B93#C9': {'parts': [{'label': 'mỗi giờ đi', 'value': 50},
                              {'label': 'đi 250 km hết', 'value': 5}]},

 'DL:KSN4.B94#C1': {'value': 40},
 'DL:KSN4.B94#C2': {'value': 45},
 'DL:KSN4.B94#C3': {'parts': [{'label': 'xe nào nhanh hơn',
                               'options': ['xe chở đồ', 'xe buýt'],
                               'value': 'xe chở đồ'}]},
 'DL:KSN4.B94#C4': {'value': 5},
 'DL:KSN4.B94#C5': {'parts': [{'label': 'vì sao',
                               'options': ['vì đo trong số giờ khác nhau',
                                           'vì hai xe khác loại'],
                               'value': 'vì đo trong số giờ khác nhau'}]},
 'DL:KSN4.B94#C6': {'parts': [{'label': 'xe A', 'value': 50},
                              {'label': 'xe B', 'value': 55}]},
 'DL:KSN4.B94#C7': {'parts': [{'label': 'xe nào nhanh hơn',
                               'options': ['xe B', 'xe A'], 'value': 'xe B'}]},
 'DL:KSN4.B94#C8': {'parts': [{'label': 'xe A', 'value': 60},
                              {'label': 'xe B', 'value': 60}]},
 'DL:KSN4.B94#C9': {'parts': [{'label': 'xe nào nhanh hơn',
                               'options': ['xe A', 'xe B'], 'value': 'xe A'},
                              {'label': 'hơn mấy km mỗi giờ', 'value': 5}]},

 'DL:KSN4.B48#C1': {'value': 10},
 'DL:KSN4.B48#C2': {'value': 20},
 'DL:KSN4.B48#C3': {'value': 3},
 'DL:KSN4.B48#C4': {'value': 120},
 'DL:KSN4.B48#C5': {'parts': [{'label': 'xe đồ đi thêm', 'value': 90},
                              {'label': 'tổng', 'value': 120}]},
 'DL:KSN4.B48#C6': {'value': 6},
 'DL:KSN4.B48#C7': {'value': 2},
 'DL:KSN4.B48#C8': {'parts': [{'label': 'chia cho cái gì',
                               'options': ['hiệu hai nhịp', 'tổng hai nhịp'],
                               'value': 'hiệu hai nhịp'}]},
 'DL:KSN4.B48#C9': {'value': 45},

 'DL:KSN4.B95#C1': {'value': 60},
 'DL:KSN4.B95#C2': {'value': 3},
 'DL:KSN4.B95#C3': {'parts': [{'label': 'tổng hay hiệu',
                               'options': ['tổng', 'hiệu'], 'value': 'tổng'}]},
 'DL:KSN4.B95#C4': {'value': 75},
 'DL:KSN4.B95#C5': {'parts': [{'label': 'xe thứ hai đi', 'value': 105},
                              {'label': 'cộng lại', 'value': 180}]},
 'DL:KSN4.B95#C6': {'value': 3},
 'DL:KSN4.B95#C7': {'value': 2},
 'DL:KSN4.B95#C8': {'parts': [{'label': 'cùng chiều thì dùng',
                               'options': ['hiệu', 'tổng'], 'value': 'hiệu'},
                              {'label': 'ngược chiều thì dùng',
                               'options': ['hiệu', 'tổng'], 'value': 'tổng'}]},
 'DL:KSN4.B95#C9': {'value': 40},

 'DL:KSN4.B49#C1': {'value': 12},
 'DL:KSN4.B49#C2': {'value': 3},
 'DL:KSN4.B49#C3': {'value': 6},
 'DL:KSN4.B49#C4': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                               'value': 'góc vuông'}]},
 'DL:KSN4.B49#C5': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                               'value': 'góc bẹt'}]},
 'DL:KSN4.B49#C6': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                               'value': 'góc nhọn'}]},
 'DL:KSN4.B49#C7': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                               'value': 'góc tù'}]},
 'DL:KSN4.B49#C8': {'parts': [{'label': 'mấy khấc', 'value': 5},
                              {'label': 'tên góc', 'options': BON_GOC,
                               'value': 'góc tù'}]},
 'DL:KSN4.B49#C9': {'value': 9},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN4.B{n}' for n in (47, 48, 49)}
    moi_ = {f'DL:KSN4.B{n}' for n in (93, 94, 95)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        for m in ('chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
    NEO = {'DL:KSN4.B47': '120', 'DL:KSN4.B93': '200', 'DL:KSN4.B94': '90',
           'DL:KSN4.B48': '30', 'DL:KSN4.B95': '180', 'DL:KSN4.B49': '12 khấc'}
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
