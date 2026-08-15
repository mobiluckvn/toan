# -*- coding: utf-8 -*-
"""CHƯƠNG 1 · SỐ ĐẾN LỚP TRIỆU — bốn bài chữ thành tám bài video.

Chương mở màn cả quyển, mà bốn bài đầu đều gộp ba bốn ý vào một chỗ:

  · B01 gộp bảng hàng - lớp, cách đọc, phân tích thành tổng, và cả mẹo lập bảng
    liệt kê để truy số — bốn thứ dùng bốn cái đầu khác nhau;
  · B02 gộp ba cánh cửa thêm chữ số (phải, trái, giữa), mỗi cửa một luật riêng;
  · B03 gộp thang máy nhân chia mười với hai kiểu xoá chữ số;
  · B04 gộp hai định luật tráo chữ số.

── SỐ NEO ──
    24 358 và 1 745 230   đọc số, tách lớp, giá trị chữ số
    3 500 → 35 000        cả cụm thêm và xoá chữ số (con số của bài tem trong sách)
    72 và 27              tráo hai chữ số

── KIỂU CẢNH MỚI: `bang_hang` ──
Cả chương đứng ở một ý mà nói bằng lời thì rối: chữ số đứng đâu nặng đấy, và cứ BA
HÀNG gom thành MỘT LỚP. Vẽ ra thì hai chuyện ấy thành một cái nhìn.

    python3 tools/so_lop_trieu_lop4.py --xem
    python3 tools/so_lop_trieu_lop4.py
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

TEN_CHUONG = 'SỐ ĐẾN LỚP TRIỆU'
CHUONG = 1
CO_KHONG = ['có', 'không']

LUI_DOC = {'ve': ['DL:KSN3.B01'], 'ten': ['TÒA THÁP THỨ TƯ MANG TÊN NGHÌN'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_GT = {'ve': ['DL:KSN3.B02'], 'ten': ['GIÁ TRỊ THEO CHỖ ĐỨNG'],
          'canCu': 'sach', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)

LUI_DOC = {'ve': ['DL:KSN3.B01'], 'ten': ['TÒA THÁP THỨ TƯ MANG TÊN NGHÌN'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_CD = {'ve': ['DL:KSN3.B01'], 'ten': ['TÒA THÁP THỨ TƯ MANG TÊN NGHÌN'],
          'canCu': 'chuDe', 'lopDuoi': 3}
LUI_THE = {'ve': ['DL:KSN3.B03'], 'ten': ['XẾP THẺ SỐ PHIÊN BẢN KHÓ'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_THEM = {'ve': ['DL:KSN3.B02'], 'ten': ['THÊM CHỮ SỐ BÊN TRÁI — BÊN PHẢI'],
            'canCu': 'sach', 'lopDuoi': 3}
LUI_XOA = {'ve': ['DL:KSN3.B02'], 'ten': ['THÊM CHỮ SỐ BÊN TRÁI — BÊN PHẢI'],
           'canCu': 'chuDe', 'lopDuoi': 3}

# ═══ ① B01 · ĐỌC SỐ TO — CHIA LỚP TRƯỚC RỒI ĐỌC ═══
B01 = bai(
    1, 'ĐỌC SỐ TO — CHIA LỚP TRƯỚC RỒI ĐỌC',
    'Dạng gốc: SỐ 1.1 mức Lớp 4 — Bảng hàng và lớp; đọc và viết số đến lớp triệu.',
    'Số nhỏ thì con đọc vèo một cái. Nhưng gặp số dài bảy chữ số thì mắt hoa lên, '
    'không biết bắt đầu từ đâu. Hôm nay con có một cách chắc chắn.',
    LUI_DOC,
    video(
        ['Biết cứ ba hàng gom thành một lớp: lớp đơn vị, lớp nghìn, lớp triệu.',
         'Tách một số dài thành từng lớp trước khi đọc.',
         'Đọc mỗi lớp như một số ba chữ số rồi gắn tên lớp vào sau.'],
        ['Đề bài: Đọc số 1 745 230.',
         'Bảng hàng đếm từ phải sang',
         'Từ phải sang trái là hàng đơn vị, hàng chục, hàng trăm, rồi hàng nghìn, '
         'chục nghìn, trăm nghìn, rồi hàng triệu.',
         'Cứ ba hàng một lớp',
         'Ba hàng đầu làm thành lớp đơn vị. Ba hàng tiếp làm thành lớp nghìn. Rồi tới '
         'lớp triệu.',
         'Tách số ra thành 1, rồi 745, rồi 230.',
         'Đọc từng lớp từ trái sang',
         'Đọc xong lớp nào thì gắn ngay tên lớp ấy vào sau: một triệu, rồi bảy trăm '
         'bốn mươi lăm nghìn, rồi hai trăm ba mươi.',
         'Riêng lớp đơn vị đọc xong là thôi, không phải gắn tên.',
         'Đáp số: một triệu bảy trăm bốn mươi lăm nghìn hai trăm ba mươi.',
         'Thử lại: số có 7 chữ số, tách được 3 lớp — đúng như đã đếm.'],
        ['Có bạn đọc số 24 358 là "hai bốn nghìn ba trăm năm mươi tám".',
         'Gợi ý 1: Con tách lớp ra xem. Hai chữ số 2 và 4 nằm ở lớp nghìn, ghép lại '
         'thành số nào?',
         'Gợi ý 2: Đọc lớp ấy như một số riêng cho xong đã, rồi mới gắn chữ nghìn vào '
         'sau.',
         'Chữa: hai chữ số ấy làm thành số 24, đọc là "hai mươi bốn". Vậy số ấy đọc là '
         'hai mươi bốn nghìn ba trăm năm mươi tám.'],
        ['Cho con đọc số thật: giá tiền trong siêu thị, số nhà, số trên hoá đơn. Số '
         'thật bao giờ cũng dễ nhớ hơn số trong sách.',
         'Con đọc sai thì đừng chữa ngay. Bảo con lấy bút tách lớp ra rồi đọc lại — '
         'tách lớp chính là cả bài này.'],
    ),
    [
        lt(1, 1, 'Số 24 358 có mấy chữ số, và tách được mấy lớp?',
           'Số ấy có 5 chữ số. Ba chữ số bên phải là lớp đơn vị, hai chữ số còn lại là '
           'lớp nghìn — tất cả 2 lớp.'),
        lt(2, 1, 'Trong số 24 358, hai chữ số của lớp nghìn ghép lại thành số nào?',
           'Hai chữ số 2 và 4 ghép lại thành số 24, đọc là hai mươi bốn.'),
        lt(3, 1, 'Đọc số 24 358 thì lớp đơn vị đọc lên thành gì?',
           'Ba chữ số 3, 5, 8 làm thành số 358, đọc là ba trăm năm mươi tám.'),
        lt(4, 2, 'Số 1 745 230 tách được mấy lớp?',
           'Số có 7 chữ số nên tách được 3 lớp: lớp đơn vị, lớp nghìn và lớp triệu.'),
        lt(5, 2, 'Trong số 1 745 230, ba chữ số của lớp nghìn ghép thành số nào?',
           'Ba chữ số 7, 4, 5 ghép thành số 745, đọc là bảy trăm bốn mươi lăm.'),
        lt(6, 2, 'Viết bằng chữ số: sáu trăm linh hai nghìn không trăm bốn mươi.',
           'Lớp nghìn là 602, lớp đơn vị là 040, ghép lại được 602 040.'),
        lt(7, 2, 'Trong số 52 604, chữ số 0 đứng ở hàng nào?',
           'Đếm từ phải sang: 4 ở hàng đơn vị, 0 ở hàng chục. Chữ số 0 giữ chỗ cho '
           'hàng chục.'),
        lt(8, 3, 'Một số có 7 chữ số thì lớp triệu của nó gồm mấy chữ số?',
           'Sáu chữ số bên phải chia đủ cho lớp đơn vị và lớp nghìn, nên lớp triệu chỉ '
           'còn 1 chữ số.'),
        lt(9, 3, 'Viết số gồm 3 triệu, 5 trăm nghìn, 8 nghìn, 2 trăm và 6 đơn vị.',
           'Xếp vào bảng hàng rồi đọc ra: 3 508 206. Hàng chục nghìn và hàng chục '
           'không có gì nên viết chữ số 0 giữ chỗ.'),
    ] + [
        q_tf(1, 'Cứ ba hàng thì gom thành một lớp.', True,
             'Đúng. Lớp đơn vị, lớp nghìn, lớp triệu — mỗi lớp ba hàng.'),
        q_tf(2, 'Số 24 358 đọc là "hai bốn nghìn ba trăm năm mươi tám".', False,
             'Sai. Lớp nghìn ghép thành số 24, phải đọc là "hai mươi bốn nghìn".'),
        q_mcq(3, 'Số 1 745 230 tách được mấy lớp?', ['hai', 'ba', 'bốn'], 'ba',
              'Bảy chữ số chia thành lớp đơn vị, lớp nghìn và lớp triệu.'),
        q_mcq(4, 'Lớp đứng ngoài cùng bên phải là lớp nào?',
              ['lớp đơn vị', 'lớp nghìn', 'lớp triệu'], 'lớp đơn vị',
              'Bảng hàng đếm từ phải sang, nên lớp đơn vị đứng ngoài cùng bên phải.'),
        q_tf(5, 'Đọc xong lớp đơn vị thì không phải gắn tên lớp vào sau.', True,
             'Đúng. Chỉ lớp nghìn và lớp triệu mới phải gắn tên.'),
    ],
)

# ═══ ② B82 · GIÁ TRỊ CỦA MỘT CHỮ SỐ ═══
B82 = bai(
    82, 'GIÁ TRỊ CỦA MỘT CHỮ SỐ — ĐỨNG ĐÂU NẶNG ĐẤY',
    'Dạng gốc: SỐ 1.1 mức Lớp 4 — Giá trị chữ số theo hàng; phân tích số thành tổng.',
    'Cùng một chữ số 7, nhưng đứng chỗ này thì đáng bảy, đứng chỗ kia lại đáng bảy '
    'trăm nghìn. Hôm nay con biết cách cân nó.',
    LUI_CD,
    video(
        ['Nói được giá trị của một chữ số bằng chữ số ấy nhân giá trị hàng nó đứng.',
         'Phân tích một số thành tổng giá trị các hàng.',
         'Biết chữ số 0 giữ chỗ cho một hàng trống, không đọc nhưng không bỏ được.'],
        ['Đề bài: Nêu giá trị của chữ số 7 trong số 1 745 230.',
         'Tìm chỗ đứng trước',
         'Xếp số vào bảng hàng rồi đếm từ phải sang: 0 đơn vị, 3 chục, 2 trăm, 5 nghìn, '
         '4 chục nghìn, 7 trăm nghìn, 1 triệu.',
         'Chữ số 7 đứng ở hàng trăm nghìn.',
         'Cân chữ số ấy',
         'Giá trị của một chữ số bằng chính chữ số ấy nhân với giá trị của hàng nó '
         'đứng. Một trăm nghìn nhân bảy được bảy trăm nghìn.',
         'Đáp số: chữ số 7 có giá trị 700 000.',
         'Phân tích cả số thành tổng',
         'Cũng một cách cân ấy, làm cho mọi hàng: 52 604 = 50 000 + 2 000 + 600 + 4.',
         'Hàng chục đang trống nên không có số hạng nào, nhưng chữ số 0 vẫn phải viết '
         'để giữ chỗ.',
         'Thử lại: cộng các số hạng lại: 50 000 + 2 000 + 600 + 4 = 52 604.'],
        ['Có bạn bảo: "Số 52 604 phân tích thành 5 + 2 + 6 + 0 + 4."',
         'Gợi ý 1: Cộng năm số ấy lại được bao nhiêu? Có ra lại số cũ không?',
         'Gợi ý 2: Chữ số 5 ấy đứng ở hàng nào, và một chữ số đứng ở hàng ấy thì đáng '
         'bao nhiêu?',
         'Chữa: phân tích là tách theo GIÁ TRỊ chứ không phải tách rời từng chữ số. '
         'Phải viết 50 000 + 2 000 + 600 + 4.'],
        ['Lấy tờ tiền ra chơi: 50 nghìn, 2 nghìn, 5 trăm. Con xếp tiền để trả đúng một '
         'số tiền — đó chính là phân tích số thành tổng.',
         'Hỏi con câu này thường xuyên: "Chữ số này đứng ở hàng nào, và nó đáng bao '
         'nhiêu?" Hai câu ấy là cả bài.'],
    ),
    [
        lt(1, 1, 'Trong số 1 745 230, chữ số 7 đứng ở hàng nào?',
           'Đếm từ phải sang, chữ số 7 đứng ở hàng trăm nghìn.'),
        lt(2, 1, 'Vậy chữ số 7 trong số ấy có giá trị bằng bao nhiêu?',
           'Đứng ở hàng trăm nghìn nên giá trị là 700 000.'),
        lt(3, 1, 'Trong số 24 358, chữ số 4 có giá trị bằng bao nhiêu?',
           'Chữ số 4 đứng ở hàng nghìn nên giá trị là 4 000.'),
        lt(4, 2, 'Phân tích số 52 604 thành tổng thì có mấy số hạng khác 0?',
           'Được 4 số hạng: 50 000 + 2 000 + 600 + 4. Hàng chục trống nên không có số '
           'hạng cho hàng ấy.'),
        lt(5, 2, 'Trong số 52 604, chữ số 5 có giá trị bằng bao nhiêu?',
           'Chữ số 5 đứng ở hàng chục nghìn nên giá trị là 50 000.'),
        lt(6, 2, 'Số 3 072 có chữ số 0 ở hàng nào, và chữ số 3 đáng bao nhiêu?',
           'Chữ số 0 ở hàng trăm. Chữ số 3 đứng ở hàng nghìn nên đáng 3 000.'),
        lt(7, 2, 'Cộng lại: 50 000 + 2 000 + 600 + 4 bằng bao nhiêu?',
           'Cộng các số hạng: 50 000 + 2 000 + 600 + 4 = 52 604 — đúng số ban đầu.'),
        lt(8, 3, 'Trong số 777, ba chữ số 7 có giá trị lần lượt là bao nhiêu?',
           'Từ trái sang: 700, rồi 70, rồi 7. Cùng một chữ số mà đứng khác hàng thì '
           'đáng khác nhau.'),
        lt(9, 3, 'Một số có chữ số hàng nghìn là 6 và chữ số hàng chục là 6. Hai chữ '
                 'số ấy chênh nhau bao nhiêu về giá trị?',
           'Chữ số hàng nghìn đáng 6 000, chữ số hàng chục đáng 60. Chênh nhau: '
           '6 000 − 60 = 5 940.'),
    ] + [
        q_tf(1, 'Giá trị của một chữ số phụ thuộc vào hàng nó đứng.', True,
             'Đúng. Cùng một chữ số, đứng hàng khác thì đáng khác nhau.'),
        q_tf(2, 'Phân tích số 52 604 thành tổng là viết 5 + 2 + 6 + 0 + 4.', False,
             'Sai. Phải tách theo giá trị: 50 000 + 2 000 + 600 + 4.'),
        q_mcq(3, 'Chữ số 4 trong số 24 358 có giá trị là',
              ['4 000', '400', '4', '40 000'], '4 000',
              'Chữ số 4 đứng ở hàng nghìn nên đáng 4 000.'),
        q_mcq(4, 'Chữ số 0 trong một số dùng để',
              ['giữ chỗ cho hàng trống', 'cho số dài ra', 'không dùng làm gì'],
              'giữ chỗ cho hàng trống',
              'Bỏ chữ số 0 đi thì các chữ số khác tụt hàng và số đổi hẳn.'),
        q_tf(5, 'Trong số 777, ba chữ số 7 đều có giá trị bằng nhau.', False,
             'Sai. Chúng đáng 700, 70 và 7 — khác hẳn nhau.'),
    ],
)

# ═══ ③ B83 · TÌM SỐ BẰNG BẢNG LIỆT KÊ ═══
B83 = bai(
    83, 'TÌM SỐ BẰNG BẢNG LIỆT KÊ — ĐỪNG ĐOÁN MÒ',
    'Dạng gốc: SỐ 1.1 mức Lớp 4 — Tìm số theo tổng và hiệu của hai chữ số, bằng '
    'cách lập bảng liệt kê thay vì thử mò.',
    'Gặp bài "tìm số có hai chữ số, tổng hai chữ số bằng chín…", con hay thử đại '
    'vài số rồi chán. Hôm nay có cách làm không bỏ sót số nào.',
    LUI_THE,
    video(
        ['Lập được bảng liệt kê mọi cặp chữ số thoả điều kiện thứ nhất.',
         'Soi điều kiện thứ hai trên bảng để chọn ra cặp đúng.',
         'Biết vì sao cách này chắc hơn thử mò: nó không bỏ sót cặp nào.'],
        ['Đề bài: Tìm số có hai chữ số, biết tổng hai chữ số bằng 9 và chữ số hàng '
         'chục hơn chữ số hàng đơn vị 3 đơn vị.',
         'Đừng thử mò',
         'Thử mò thì hên xui, mà lại không biết mình đã thử hết chưa. Lập bảng thì '
         'chắc chắn không sót cặp nào.',
         'Bảng cặp chữ số có tổng bằng 9',
         'Chữ số hàng chục lớn hơn nên xếp nó đứng trước: 9 và 0, rồi 8 và 1, rồi 7 và '
         '2, rồi 6 và 3, rồi 5 và 4. Được 5 cặp.',
         'Soi điều kiện thứ hai',
         'Tính hiệu từng cặp: 9, rồi 7, rồi 5, rồi 3, rồi 1. Chỉ một cặp có hiệu bằng '
         '3, đó là cặp 6 và 3.',
         'Đáp số: số cần tìm là 63.',
         'Thử lại: 6 + 3 = 9 và 6 − 3 = 3 — khớp cả hai điều kiện.'],
        ['Có bạn thử vài số rồi tuyên bố: "Chắc là 36, vì 3 cộng 6 bằng 9."',
         'Gợi ý 1: Số 36 có chữ số hàng chục là mấy, hàng đơn vị là mấy? Cái nào lớn '
         'hơn?',
         'Gợi ý 2: Đề đòi chữ số hàng chục PHẢI HƠN chữ số hàng đơn vị. Con soi lại '
         'điều kiện ấy trên bảng xem.',
         'Chữa: số 36 có hàng chục là 3, nhỏ hơn hàng đơn vị 6, nên không đạt. Cặp '
         'đúng phải là 6 đứng trước 3, tức số 63.'],
        ['Chơi trò đoán số: bố mẹ nghĩ một số hai chữ số rồi cho hai manh mối (tổng và '
         'hiệu của hai chữ số). Con phải lập bảng ra giấy, không được đoán.',
         'Con làm xong nhớ bắt thử lại cả hai điều kiện. Nhiều bài sai chỉ vì bé khớp '
         'điều kiện đầu rồi quên mất điều kiện sau.'],
    ),
    [
        lt(1, 1, 'Có bao nhiêu cặp chữ số có tổng bằng 9, trong đó chữ số đứng trước '
                 'lớn hơn chữ số đứng sau?',
           'Có 5 cặp: 9 và 0, 8 và 1, 7 và 2, 6 và 3, 5 và 4.'),
        lt(2, 1, 'Trong bảng ấy, cặp nào có hiệu bằng 3?',
           'Cặp 6 và 3, vì 6 − 3 = 3.'),
        lt(3, 1, 'Vậy số cần tìm là số nào?',
           'Chữ số hàng chục là 6, hàng đơn vị là 3, nên số cần tìm là 63.'),
        lt(4, 2, 'Tìm số có hai chữ số, tổng hai chữ số bằng 7 và chữ số hàng chục hơn '
                 'hàng đơn vị 3 đơn vị.',
           'Bảng cặp có tổng 7: 7 và 0, 6 và 1, 5 và 2, 4 và 3. Cặp có hiệu 3 là 5 và '
           '2, nên số cần tìm là 52.'),
        lt(5, 2, 'Tìm số có hai chữ số, tổng hai chữ số bằng 11 và chữ số hàng chục '
                 'hơn hàng đơn vị 1 đơn vị.',
           'Bảng cặp có tổng 11: 9 và 2, 8 và 3, 7 và 4, 6 và 5. Cặp có hiệu 1 là 6 và '
           '5, nên số cần tìm là 65.'),
        lt(6, 2, 'Có bao nhiêu số có hai chữ số mà tổng hai chữ số bằng 5?',
           'Các số ấy là 50, 41, 32, 23, 14 — tất cả 5 số. Số 05 không phải số có hai '
           'chữ số.'),
        lt(7, 2, 'Số có hai chữ số mà tổng hai chữ số bằng 9 và hiệu cũng bằng 9 là số '
                 'nào?',
           'Cặp duy nhất là 9 và 0, nên số ấy là 90.'),
        lt(8, 3, 'Tìm số có hai chữ số, tổng hai chữ số bằng 12 và hiệu bằng 4.',
           'Bảng cặp có tổng 12: 9 và 3, 8 và 4, 7 và 5. Cặp có hiệu 4 là 8 và 4, nên '
           'số cần tìm là 84.'),
        lt(9, 3, 'Tìm số có hai chữ số, biết chữ số hàng chục gấp đôi chữ số hàng đơn '
                 'vị và tổng hai chữ số bằng 9.',
           'Cặp gấp đôi nhau: 2 và 1, 4 và 2, 6 và 3, 8 và 4. Cặp có tổng 9 là 6 và 3, '
           'nên số cần tìm là 63.'),
    ] + [
        q_tf(1, 'Gặp bài tìm số theo tổng và hiệu chữ số thì nên đoán mò cho nhanh.',
             False, 'Sai. Đoán mò dễ sót; lập bảng liệt kê thì chắc chắn không bỏ cặp '
                    'nào.'),
        q_tf(2, 'Chữ số hàng chục của một số có hai chữ số không thể bằng 0.', True,
             'Đúng. Chữ số 0 đứng đầu thì số ấy chỉ còn một chữ số.'),
        q_mcq(3, 'Số có hai chữ số, tổng hai chữ số bằng 9 và hiệu bằng 3 là',
              ['63', '36', '54', '72'], '63',
              'Cặp 6 và 3 có tổng 9, hiệu 3, và hàng chục phải là số lớn hơn.'),
        q_mcq(4, 'Có bao nhiêu cặp chữ số có tổng bằng 9 mà chữ số đứng trước lớn hơn?',
              ['bốn', 'năm', 'sáu'], 'năm',
              'Đó là 9 và 0, 8 và 1, 7 và 2, 6 và 3, 5 và 4.'),
        q_tf(5, 'Lập bảng xong thì chỉ việc soi điều kiện thứ hai trên bảng.', True,
             'Đúng. Bảng lo điều kiện thứ nhất, mắt lo điều kiện thứ hai.'),
    ],
)

# ═══ ④ B02 · THÊM MỘT CHỮ SỐ VÀO BÊN PHẢI ═══
B02 = bai(
    2, 'THÊM MỘT CHỮ SỐ VÀO BÊN PHẢI — SƠ ĐỒ MƯỜI PHẦN',
    'Dạng gốc: SỐ 1.2 mức Lớp 4 — Thêm chữ số vào bên phải; sơ đồ mười phần và bài '
    'ngược tìm số cũ.',
    'Máy in giá 3 500 đồng bỗng in thành 35 000 đồng. Chỉ thêm một chữ số 0 mà giá '
    'nhảy vọt. Nhảy bao nhiêu, và vì sao đúng bấy nhiêu?',
    LUI_THEM,
    video(
        ['Biết thêm chữ số 0 vào bên phải là gấp số ấy lên 10 lần.',
         'Nhìn ra phần tăng thêm gồm đúng 9 phần, tức 9 lần số cũ.',
         'Giải được bài ngược: biết phần tăng thêm, tìm lại số cũ.'],
        ['Đề bài: Máy in thêm một chữ số 0 vào giá 3 500 đồng, thành 35 000 đồng. Giá '
         'bị đội lên bao nhiêu, và con số ấy có quan hệ gì với giá cũ?',
         'Thêm 0 vào bên phải là gấp mười',
         'Mọi chữ số đều dịch sang trái một hàng, mà mỗi hàng nặng gấp mười hàng bên '
         'phải nó. Nên số mới bằng số cũ nhân mười.',
         'Vẽ ra thành sơ đồ',
         'Số cũ là 1 phần. Số mới là 10 phần. Vậy phần đội thêm là 10 trừ 1, bằng '
         '9 phần — tức 9 lần số cũ.',
         'Tính thử: 35 000 − 3 500 = 31 500 (đồng).',
         'Kiểm lại bằng phép nhân: 3 500 × 9 = 31 500 — khớp từng đồng.',
         'Đáp số: đội thêm 31 500 đồng, đúng bằng 9 lần giá cũ.',
         'Thêm chữ số khác 0 thì sao',
         'Thêm chữ số 5 vào bên phải số 35 được 355. Phần thêm gồm 9 lần số cũ, cộng '
         'thêm chính chữ số ấy: 35 × 9 = 315, rồi 315 + 5 = 320.'],
        ['Có bạn bảo: "Thêm một chữ số 0 vào bên phải thì số tăng thêm đúng bằng chính '
         'nó, tức là gấp đôi."',
         'Gợi ý 1: Con vẽ sơ đồ ra xem. Số cũ mấy phần, số mới mấy phần?',
         'Gợi ý 2: Thử với số nhỏ cho dễ: 5 thêm 0 thành 50. Số tăng thêm là bao '
         'nhiêu, có bằng 5 không?',
         'Chữa: số mới là 10 phần chứ không phải 2 phần, nên phần tăng thêm là 9 phần '
         '— gấp 9 lần số cũ, không phải gấp đôi.'],
        ['Đưa con một tờ giấy giá tiền rồi bảo thêm một chữ số 0 vào cuối. Hỏi con giá '
         'đội lên bao nhiêu, rồi bấm máy tính kiểm.',
         'Chuyện in nhầm giá hay xảy ra thật ngoài chợ. Con nhận ra được "sai một chữ '
         'số 0" là con đã dùng được bài này.'],
    ),
    [
        lt(1, 1, 'Thêm chữ số 0 vào bên phải số 3 500 thì được số nào?',
           'Mọi chữ số dịch sang trái một hàng nên số mới là 35 000.'),
        lt(2, 1, 'Số mới hơn số cũ bao nhiêu đơn vị?',
           'Lấy số mới trừ số cũ: 35 000 − 3 500 = 31 500.'),
        lt(3, 1, 'Phần tăng thêm ấy gấp mấy lần số cũ?',
           'Số cũ 1 phần, số mới 10 phần nên phần tăng thêm là 9 phần — gấp 9 lần.'),
        lt(4, 2, 'Thêm chữ số 0 vào bên phải số 24 thì được số nào, và tăng thêm bao '
                 'nhiêu?',
           'Được số 240. Tăng thêm: 240 − 24 = 216, đúng bằng 24 × 9.'),
        lt(5, 2, 'Thêm chữ số 0 vào bên phải một số thì số ấy tăng thêm 216. Tìm số cũ.',
           'Phần tăng thêm gấp 9 lần số cũ nên số cũ là 216 : 9 = 24.'),
        lt(6, 2, 'Thêm chữ số 5 vào bên phải số 35 thì được số nào, và tăng thêm bao '
                 'nhiêu?',
           'Được số 355. Tăng thêm: 355 − 35 = 320, gồm 35 × 9 = 315 rồi cộng 5.'),
        lt(7, 2, 'Thêm chữ số 5 vào bên phải một số thì số ấy tăng thêm 320. Tìm số cũ.',
           'Bớt chữ số vừa thêm ra: 320 − 5 = 315. Phần còn lại gấp 9 lần số cũ nên số '
           'cũ là 315 : 9 = 35.'),
        lt(8, 3, 'Thêm chữ số 7 vào bên phải số 12 thì phần tăng thêm gồm 9 lần số cũ '
                 'bằng bao nhiêu, và tất cả tăng bao nhiêu?',
           'Chín lần số cũ: 12 × 9 = 108. Cộng thêm chữ số vừa thêm: 108 + 7 = 115.'),
        lt(9, 3, 'Thêm chữ số 3 vào bên phải một số thì số ấy tăng thêm 300. Tìm số cũ.',
           'Bớt chữ số vừa thêm: 300 − 3 = 297. Số cũ là 297 : 9 = 33.'),
    ] + [
        q_tf(1, 'Thêm chữ số 0 vào bên phải thì số gấp lên 10 lần.', True,
             'Đúng. Mọi chữ số dịch sang trái một hàng, mà mỗi hàng nặng gấp mười.'),
        q_tf(2, 'Thêm chữ số 0 vào bên phải thì số tăng thêm đúng bằng chính nó.',
             False, 'Sai. Số mới là 10 phần nên phần tăng thêm là 9 phần, gấp 9 lần.'),
        q_mcq(3, 'Thêm chữ số 0 vào bên phải số 3 500 thì số tăng thêm',
              ['31 500', '3 500', '35 000', '315 000'], '31 500',
              'Phần tăng thêm gấp 9 lần số cũ: 3 500 × 9 = 31 500.'),
        q_mcq(4, 'Thêm chữ số 5 vào bên phải một số thì số mới bằng',
              ['số cũ nhân 10 rồi cộng 5', 'số cũ cộng 5', 'số cũ nhân 5'],
              'số cũ nhân 10 rồi cộng 5',
              'Số cũ dịch lên một hàng thành mười lần, rồi chữ số 5 điền vào hàng đơn '
              'vị.'),
        q_tf(5, 'Thêm một chữ số khác 0 vào bên phải thì phần tăng gồm 9 lần số cũ '
                'cộng chính chữ số ấy.', True,
             'Đúng. Đó là cách giải mọi bài ngược của dạng này.'),
    ],
)

# ═══ ⑤ B84 · THÊM BÊN TRÁI VÀ XEN VÀO GIỮA ═══
B84 = bai(
    84, 'THÊM BÊN TRÁI VÀ XEN VÀO GIỮA — HAI CỬA CÒN LẠI',
    'Dạng gốc: SỐ 1.2 mức Lớp 4 — Thêm chữ số vào bên trái và xen vào giữa số có '
    'hai chữ số.',
    'Bài trước con vào bằng cửa bên phải. Còn hai cửa nữa: cửa bên trái và cửa xen '
    'vào giữa. Mỗi cửa để lại một dấu vết riêng.',
    LUI_THEM,
    video(
        ['Biết thêm một chữ số vào bên trái số có hai chữ số là đặt nó vào hàng trăm.',
         'Tính được phần tăng thêm của cửa trái: chữ số ấy nhân một trăm.',
         'Tính được phần tăng thêm của cửa giữa: chín mươi nhân chữ số bị đẩy lên.'],
        ['Đề bài: Thêm chữ số 4 vào bên trái số 75, rồi xen chữ số 0 vào giữa số 84. '
         'Mỗi số tăng thêm bao nhiêu?',
         'Cửa bên trái hiền nhất',
         'Thêm 4 vào bên trái số 75 được 475. Hai chữ số cũ đứng yên tại chỗ, chỉ có '
         'chữ số mới ngồi vào hàng trăm.',
         'Nên số tăng thêm đúng bằng giá trị của chữ số mới ở hàng trăm: 4 × 100 = 400.',
         'Kiểm lại: 475 − 75 = 400.',
         'Cửa xen giữa khó hơn một bậc',
         'Xen chữ số 0 vào giữa số 84 được 804. Lần này chữ số 8 bị đẩy từ hàng chục '
         'lên hàng trăm, còn chữ số 4 vẫn đứng yên.',
         'Chữ số 8 đang đáng 80, nay đáng 800, nên nó đội thêm 720.',
         'Con số 720 ấy chính là 90 nhân 8 — chín mươi nhân chữ số bị đẩy lên.',
         'Kiểm lại: 804 − 84 = 720.',
         'Đáp số: cửa trái tăng 400, cửa giữa tăng 720.'],
        ['Có bạn xen 0 vào giữa số 84 rồi bảo: "Xen thêm số 0 thôi mà, 0 thì có đáng '
         'gì đâu, số không đổi."',
         'Gợi ý 1: Con viết hai số ra cạnh nhau: 84 và 804. Chúng có bằng nhau không?',
         'Gợi ý 2: Chữ số 8 lúc đầu đứng hàng nào, sau khi xen thì đứng hàng nào?',
         'Chữa: bản thân chữ số 0 không đáng gì, nhưng nó ĐẨY chữ số 8 lên một hàng, '
         'và chính cái đẩy ấy làm số tăng thêm 720.'],
        ['Lấy ba mẩu giấy viết ba chữ số rồi cho con chèn thêm một mẩu vào các vị trí '
         'khác nhau. Mỗi lần chèn, hỏi con số nào bị đẩy đi và đẩy lên hàng nào.',
         'Cửa giữa là cửa khó nhất trong ba cửa. Con hiểu được "đẩy lên một hàng thì '
         'nặng gấp mười" là con qua được cả bài.'],
    ),
    [
        lt(1, 1, 'Thêm chữ số 4 vào bên trái số 75 thì được số nào?',
           'Chữ số 4 ngồi vào hàng trăm nên được số 475.'),
        lt(2, 1, 'Số ấy tăng thêm bao nhiêu so với số 75?',
           'Chỉ chữ số mới ở hàng trăm là thêm vào: 4 × 100 = 400.'),
        lt(3, 1, 'Xen chữ số 0 vào giữa số 84 thì được số nào?',
           'Chữ số 8 bị đẩy lên hàng trăm, được số 804.'),
        lt(4, 2, 'Số 804 hơn số 84 bao nhiêu đơn vị?',
           'Lấy hiệu: 804 − 84 = 720. Đó chính là 90 × 8.'),
        lt(5, 2, 'Thêm chữ số 6 vào bên trái số 25 thì số tăng thêm bao nhiêu?',
           'Chữ số 6 ngồi vào hàng trăm nên tăng thêm 6 × 100 = 600.'),
        lt(6, 2, 'Thêm một chữ số vào bên trái số 38 làm số tăng thêm 500. Chữ số ấy '
                 'là mấy?',
           'Phần tăng thêm bằng chữ số ấy nhân 100, nên chữ số ấy là 500 : 100 = 5.'),
        lt(7, 2, 'Xen chữ số 0 vào giữa số 51 thì được số nào, và tăng thêm bao nhiêu?',
           'Được số 501. Chữ số 5 bị đẩy lên nên tăng thêm 90 × 5 = 450.'),
        lt(8, 3, 'Xen chữ số 0 vào giữa một số có hai chữ số làm nó tăng thêm 630. '
                 'Chữ số hàng chục của số cũ là mấy?',
           'Phần tăng thêm bằng 90 nhân chữ số hàng chục, nên chữ số ấy là 630 : 90 = 7.'),
        lt(9, 3, 'Với số 47: thêm chữ số 3 vào bên trái được số nào, xen chữ số 0 vào '
                 'giữa được số nào, và số nào lớn hơn?',
           'Thêm trái được 347, xen giữa được 407. Số xen giữa lớn hơn, vì nó đẩy chữ '
           'số 4 lên hàng trăm.'),
    ] + [
        q_tf(1, 'Thêm một chữ số vào bên trái số có hai chữ số thì chữ số ấy đứng ở '
                'hàng trăm.', True,
             'Đúng, và hai chữ số cũ vẫn đứng yên tại chỗ.'),
        q_mcq(2, 'Thêm chữ số 4 vào bên trái số 75 thì số tăng thêm',
              ['400', '4', '475', '40'], '400',
              'Chữ số 4 ở hàng trăm nên đáng 400.'),
        q_tf(3, 'Xen chữ số 0 vào giữa số 84 thì số không đổi, vì số 0 không đáng gì.',
             False, 'Sai. Chữ số 0 đẩy chữ số 8 lên một hàng, làm số tăng thêm 720.'),
        q_mcq(4, 'Xen chữ số 0 vào giữa một số có hai chữ số thì số tăng thêm',
              ['90 nhân chữ số hàng chục', '10 nhân chữ số hàng chục', 'đúng 100'],
              '90 nhân chữ số hàng chục',
              'Chữ số hàng chục nhảy lên hàng trăm nên đáng gấp mười, đội thêm 90 lần '
              'chính nó.'),
        q_tf(5, 'Cửa bên trái làm số tăng thêm đúng một số tròn trăm.', True,
             'Đúng, vì chữ số mới ngồi thẳng vào hàng trăm.'),
    ],
)

# ═══ ⑥ B03 · NHÂN VÀ CHIA CHO 10, 100, 1000 ═══
B03 = bai(
    3, 'NHÂN VÀ CHIA CHO 10, 100, 1000 — THANG MÁY CHỮ SỐ 0',
    'Dạng gốc: SỐ 2.1 mức Lớp 4 — Gấp và giảm 10, 100, 1000 lần bằng cách thêm '
    'hoặc bớt chữ số 0.',
    'Nhân với 10 thì thêm một chữ số 0. Nhân với 100 thì thêm hai. Nghe như mẹo '
    'vặt, nhưng nó có lý do — và biết lý do thì không bao giờ nhầm.',
    LUI_CD,
    video(
        ['Nhân một số với 10, 100, 1000 bằng cách thêm 1, 2, 3 chữ số 0.',
         'Chia một số tròn cho 10, 100, 1000 bằng cách bớt đi từng ấy chữ số 0.',
         'Nói được vì sao: mỗi lần thêm một chữ số 0 là mọi chữ số lên một hàng.'],
        ['Đề bài: Tính 47 × 10, rồi 47 × 100, rồi 4 700 : 100.',
         'Vì sao thêm 0 là nhân mười',
         'Thêm một chữ số 0 vào bên phải thì mọi chữ số dịch sang trái một hàng. Mỗi '
         'hàng nặng gấp mười hàng bên phải nó, nên cả số nặng gấp mười.',
         'Đi lên từng tầng',
         'Số 47 nhân 10 được 470. Nhân 100 thì thêm hai chữ số 0, được 4 700. Nhân '
         '1000 thì thêm ba, được 47 000.',
         'Bốn số ấy cùng một nhà, chỉ khác tầng đang đứng.',
         'Đi xuống thì bớt',
         'Chia là đi ngược lại: 4 700 chia 100 thì bớt hai chữ số 0, còn 47.',
         'Đáp số: 470, rồi 4 700, rồi 47.',
         'Thử lại: 47 nhân 100 được 4 700, rồi 4 700 chia 100 lại về 47 — đi lên rồi '
         'đi xuống thì về đúng chỗ cũ.'],
        ['Có bạn tính 4 700 chia 100 rồi ghi 470.',
         'Gợi ý 1: Chia cho 100 thì phải bớt mấy chữ số 0, một hay hai?',
         'Gợi ý 2: Con thử đi ngược lại xem: 470 nhân 100 có ra 4 700 không?',
         'Chữa: chia cho 100 phải bớt hai chữ số 0, nên kết quả là 47. Bạn ấy mới bớt '
         'có một.'],
        ['Cho con đổi đơn vị tiền: 5 nghìn là bao nhiêu trăm, bao nhiêu chục. Mỗi lần '
         'đổi là một lần đi thang máy.',
         'Bí quyết chống nhầm: bảo con ĐẾM SỐ CHỮ SỐ 0 của số nhân hay số chia trước, '
         'rồi mới viết. Nhầm ở đây gần như luôn là nhầm một chữ số 0.'],
    ),
    [
        lt(1, 1, 'Tính 47 × 10.',
           'Thêm một chữ số 0 vào bên phải: 47 × 10 = 470.'),
        lt(2, 1, 'Tính 47 × 100.',
           'Thêm hai chữ số 0 vào bên phải: 47 × 100 = 4 700.'),
        lt(3, 1, 'Tính 4 700 : 100.',
           'Bớt hai chữ số 0: 4 700 : 100 = 47.'),
        lt(4, 2, 'Tính 350 000 : 10.',
           'Bớt một chữ số 0: 350 000 : 10 = 35 000.'),
        lt(5, 2, 'Một khoản 350 000 đồng bị ghi thiếu một chữ số 0 tận cùng. Số ghi sai '
                 'là bao nhiêu, và sổ bị hụt bao nhiêu?',
           'Ghi sai thành 350 000 : 10 = 35 000 (đồng). Hụt: 350 000 − 35 000 = 315 000 '
           '(đồng).'),
        lt(6, 2, 'Phần hụt ấy gấp mấy lần số đã ghi sai?',
           'Số đúng gấp 10 lần số ghi sai, nên phần hụt là 9 phần — gấp 9 lần.'),
        lt(7, 2, 'Tính 6 × 1000.',
           'Thêm ba chữ số 0 vào bên phải: 6 × 1000 = 6 000.'),
        lt(8, 3, 'Một số đem nhân 100 rồi chia 10 thì kết quả gấp mấy lần số ấy?',
           'Lên hai tầng rồi xuống một tầng, còn lại lên một tầng: gấp 10 lần.'),
        lt(9, 3, 'Số nào nhân 10 thì được 8 200? Và nếu đem chính số ấy nhân 100 thì '
                 'được bao nhiêu?',
           'Đi ngược lại: 8 200 : 10 = 820. Rồi 820 × 100 = 82 000.'),
    ] + [
        q_tf(1, 'Nhân một số với 100 thì thêm hai chữ số 0 vào bên phải.', True,
             'Đúng, vì mọi chữ số dịch sang trái hai hàng.'),
        q_tf(2, 'Chia 4 700 cho 100 thì được 470.', False,
             'Sai. Chia cho 100 phải bớt hai chữ số 0, được 47.'),
        q_mcq(3, 'Tính 47 × 1000.', ['47 000', '4 700', '470 000', '470'], '47 000',
              'Thêm ba chữ số 0 vào bên phải số 47.'),
        q_mcq(4, 'Bớt một chữ số 0 tận cùng của một số tròn chục thì số ấy',
              ['giảm 10 lần', 'giảm 10 đơn vị', 'không đổi'], 'giảm 10 lần',
              'Mọi chữ số tụt xuống một hàng nên số nhẹ đi mười lần.'),
        q_tf(5, 'Ghi thiếu một chữ số 0 tận cùng thì phần hụt bằng 9 lần số đã ghi.',
             True, 'Đúng. Số đúng là 10 phần, số ghi sai là 1 phần, hụt 9 phần.'),
    ],
)

# ═══ ⑦ B85 · XOÁ MỘT CHỮ SỐ ═══
B85 = bai(
    85, 'XOÁ MỘT CHỮ SỐ — Ở ĐUÔI KHÁC HẲN Ở ĐẦU',
    'Dạng gốc: SỐ 1.3 mức Lớp 4 — Xoá chữ số tận cùng và xoá chữ số hàng cao nhất; '
    'bài ngược dựng lại số cũ.',
    'Thêm chữ số thì con đã biết. Nay làm ngược: xoá đi một chữ số. Xoá ở đuôi và '
    'xoá ở đầu là hai chuyện khác hẳn nhau.',
    LUI_XOA,
    video(
        ['Biết xoá chữ số hàng cao nhất thì số giảm đúng bằng giá trị chữ số ấy.',
         'Biết xoá chữ số tận cùng thì số cũ bằng số mới nhân mười cộng chữ số bị xoá.',
         'Giải được bài ngược: biết số giảm bao nhiêu, tìm lại số cũ.'],
        ['Đề bài: Xoá chữ số hàng trăm của số 725, rồi xoá chữ số tận cùng của số 303. '
         'Mỗi lần số giảm bao nhiêu?',
         'Xoá ở đầu thì dễ',
         'Xoá chữ số hàng trăm của 725 thì còn 25. Hai chữ số còn lại đứng nguyên chỗ '
         'cũ, không ai phải dịch đi đâu.',
         'Nên số giảm đúng bằng giá trị của chữ số vừa bị cắt: 725 − 25 = 700.',
         'Xoá ở đuôi thì khác',
         'Xoá chữ số tận cùng của 303 thì còn 30. Lần này mọi chữ số còn lại đều tụt '
         'xuống một hàng.',
         'Số cũ bằng số mới nhân mười rồi cộng chữ số bị xoá: 30 nhân 10 được 300, '
         'cộng 3 được 303.',
         'Số giảm: 303 − 30 = 273.',
         'Đáp số: xoá ở đầu giảm 700, xoá ở đuôi giảm 273.',
         'Thử lại chiều ngược: 30 × 10 = 300, rồi 300 + 3 = 303 — về đúng số cũ.'],
        ['Có bạn bảo: "Xoá một chữ số ở đuôi thì số nào cũng giảm đi mười lần."',
         'Gợi ý 1: Con thử với số 47 xem. Xoá chữ số 7 còn số 4. Số 4 nhân mười có ra '
         'lại 47 không?',
         'Gợi ý 2: Chỉ khi chữ số bị xoá là chữ số nào thì mới về đúng được số cũ?',
         'Chữa: chỉ đúng khi chữ số bị xoá là 0. Còn khác 0 thì số cũ bằng số mới nhân '
         'mười RỒI CỘNG chữ số ấy, nên không giảm tròn mười lần.'],
        ['Viết một số lên giấy rồi lấy tay che một chữ số. Che ở đầu và che ở cuối, '
         'mỗi lần hỏi con số còn lại là bao nhiêu và mất đi bao nhiêu.',
         'Đây là bài dễ nhầm nhất chương một. Bố mẹ chỉ cần hỏi đúng một câu mỗi lần: '
         '"Các chữ số còn lại có phải dịch chỗ không?"'],
    ),
    [
        lt(1, 1, 'Xoá chữ số hàng trăm của số 725 thì còn số nào?',
           'Hai chữ số còn lại đứng nguyên chỗ cũ nên còn số 25.'),
        lt(2, 1, 'Số ấy giảm đi bao nhiêu đơn vị?',
           'Giảm đúng bằng giá trị chữ số bị cắt: 725 − 25 = 700.'),
        lt(3, 1, 'Xoá chữ số tận cùng của số 303 thì còn số nào?',
           'Bỏ chữ số 3 ở hàng đơn vị, còn lại số 30.'),
        lt(4, 2, 'Số 303 giảm đi bao nhiêu sau khi xoá chữ số tận cùng?',
           'Lấy hiệu: 303 − 30 = 273.'),
        lt(5, 2, 'Xoá chữ số hàng trăm của một số làm nó giảm 600. Chữ số hàng trăm ấy '
                 'là mấy?',
           'Số giảm bằng giá trị chữ số ấy ở hàng trăm, nên chữ số ấy là 600 : 100 = 6.'),
        lt(6, 2, 'Xoá chữ số tận cùng của số 4 856 thì còn số nào?',
           'Bỏ chữ số 6 ở hàng đơn vị, còn lại số 485.'),
        lt(7, 2, 'Số 4 856 giảm đi bao nhiêu sau khi xoá chữ số tận cùng?',
           'Lấy hiệu: 4 856 − 485 = 4 371.'),
        lt(8, 3, 'Xoá chữ số tận cùng của một số có ba chữ số thì được số mới kém số cũ '
                 '273 đơn vị. Tìm số mới và số cũ.',
           'Số cũ bằng số mới nhân mười cộng chữ số bị xoá, nên phần chênh gồm 9 lần số '
           'mới cộng chữ số ấy. Thử số mới 30: 30 × 9 = 270, cộng 3 được 273 — khớp. '
           'Số mới là 30, số cũ là 303.'),
        lt(9, 3, 'Xoá chữ số 0 tận cùng của số 380 thì số ấy giảm đi mấy lần?',
           'Còn lại 38, mà 38 × 10 = 380, nên số ấy giảm đi 10 lần.'),
    ] + [
        q_tf(1, 'Xoá chữ số hàng cao nhất thì số giảm đúng bằng giá trị chữ số ấy.',
             True, 'Đúng, vì các chữ số còn lại không phải dịch chỗ.'),
        q_tf(2, 'Xoá một chữ số ở đuôi thì số nào cũng giảm đi đúng 10 lần.', False,
             'Sai. Chỉ đúng khi chữ số bị xoá là 0.'),
        q_mcq(3, 'Xoá chữ số hàng trăm của số 725 thì số giảm',
              ['700', '7', '25', '70'], '700',
              'Chữ số 7 đứng ở hàng trăm nên đáng 700.'),
        q_mcq(4, 'Xoá chữ số tận cùng của một số thì số cũ bằng',
              ['số mới nhân 10 rồi cộng chữ số bị xoá', 'số mới cộng chữ số bị xoá',
               'số mới nhân chữ số bị xoá'],
              'số mới nhân 10 rồi cộng chữ số bị xoá',
              'Các chữ số còn lại đều tụt một hàng, nên phải nhân mười để trả về chỗ cũ.'),
        q_tf(5, 'Xoá chữ số 0 tận cùng của số 380 thì được 38, tức là giảm 10 lần.',
             True, 'Đúng. Chữ số bị xoá là 0 nên về đúng một phần mười.'),
    ],
)

# ═══ ⑧ B04 · TRÁO HAI CHỮ SỐ ═══
B04 = bai(
    4, 'TRÁO HAI CHỮ SỐ — HỌ 9 VÀ HỌ 11',
    'Dạng gốc: SỐ 1.4 mức Lớp 4 — Hai định luật khi tráo hai chữ số: hiệu chia hết '
    'cho 9, tổng chia hết cho 11.',
    'Lấy số 72 rồi tráo hai chữ số được 27. Trừ nhau ra 45. Thử số khác cũng ra '
    'những con số họ hàng với nhau. Hôm nay con biết vì sao.',
    LUI_THE,
    video(
        ['Biết tráo hai chữ số rồi trừ thì hiệu bằng 9 nhân hiệu hai chữ số.',
         'Biết tráo hai chữ số rồi cộng thì tổng bằng 11 nhân tổng hai chữ số.',
         'Dùng được hai luật ấy để truy ra số khi biết hiệu hoặc tổng.'],
        ['Đề bài: Số 72 tráo hai chữ số được 27. Tính hiệu và tổng của hai số ấy, rồi '
         'tìm quy luật.',
         'Thử vài lần đã',
         'Bảy mươi hai trừ hai mươi bảy bằng bốn mươi lăm. Sáu mươi ba trừ ba mươi sáu '
         'bằng hai mươi bảy. Chín mươi mốt trừ mười chín bằng bảy mươi hai.',
         'Soi hiệu hai chữ số của từng số: 5, rồi 3, rồi 8. Nhân chín lên: 45, rồi 27, '
         'rồi 72 — khớp cả ba.',
         'Vì sao lại thế',
         'Chữ số hàng chục vốn đáng gấp mười chính nó; tráo xuống hàng đơn vị thì chỉ '
         'còn đáng chính nó, tức mất đi chín lần. Chữ số kia thì ngược lại, được thêm '
         'chín lần. Nên hiệu hai số bằng chín nhân hiệu hai chữ số.',
         'Luật anh em: đem cộng',
         'Bảy mươi tư cộng bốn mươi bảy bằng một trăm hai mươi mốt, đúng bằng mười một '
         'nhân mười một. Mà bảy cộng bốn cũng bằng mười một.',
         'Đáp số: hiệu mang họ 9, tổng mang họ 11.',
         'Thử lại: 72 − 27 = 45, mà 45 chia 9 được 5 — đúng bằng 7 trừ 2.'],
        ['Có bạn nhớ nhầm: "Tráo hai chữ số rồi cộng thì tổng cũng chia hết cho 9."',
         'Gợi ý 1: Con thử với 74 và 47 xem. Tổng bằng bao nhiêu, có chia hết cho 9 '
         'không?',
         'Gợi ý 2: Chia tổng ấy cho 11 xem được số nào, rồi so với tổng hai chữ số của '
         'số ban đầu.',
         'Chữa: cộng thì mang họ 11 chứ không phải họ 9. Hiệu mới mang họ 9. Hai luật '
         'khác nhau, đừng lẫn.'],
        ['Chơi trò tráo số: con viết một số hai chữ số, bố mẹ tráo lại, rồi cả nhà đoán '
         'trước hiệu bằng bao nhiêu trước khi tính.',
         'Con đoán đúng vài lần là tin luật. Nhưng nhớ hỏi con thêm câu "vì sao" — bài '
         'này có lời giải thích, không phải mẹo học thuộc.'],
    ),
    [
        lt(1, 1, 'Tính 72 − 27.',
           'Lấy hiệu: 72 − 27 = 45.'),
        lt(2, 1, 'Hiệu hai chữ số của số 72 bằng bao nhiêu, và 45 gấp mấy lần nó?',
           'Hiệu hai chữ số: 7 − 2 = 5. Mà 45 : 5 = 9 nên gấp 9 lần.'),
        lt(3, 1, 'Tính 74 + 47.',
           'Lấy tổng: 74 + 47 = 121.'),
        lt(4, 2, 'Tổng hai chữ số của số 74 bằng bao nhiêu, và 121 gấp mấy lần nó?',
           'Tổng hai chữ số: 7 + 4 = 11. Mà 121 : 11 = 11 nên gấp 11 lần.'),
        lt(5, 2, 'Tính 63 − 36.',
           'Lấy hiệu: 63 − 36 = 27, đúng bằng 9 nhân hiệu hai chữ số 6 − 3 = 3.'),
        lt(6, 2, 'Số 85 tráo hai chữ số được 58. Hiệu hai số ấy bằng bao nhiêu?',
           'Hiệu hai chữ số là 8 − 5 = 3, nên hiệu hai số là 9 × 3 = 27.'),
        lt(7, 2, 'Số 26 tráo hai chữ số được 62. Tổng hai số ấy bằng bao nhiêu?',
           'Tổng hai chữ số là 2 + 6 = 8, nên tổng hai số là 11 × 8 = 88.'),
        lt(8, 3, 'Hiệu của một số có hai chữ số và số viết ngược của nó bằng 45. Hai '
                 'chữ số của nó chênh nhau bao nhiêu?',
           'Hiệu mang họ 9 nên hiệu hai chữ số là 45 : 9 = 5.'),
        lt(9, 3, 'Một số có hai chữ số, hiệu của nó với số viết ngược bằng 45, và tổng '
                 'hai chữ số bằng 9. Tìm hai chữ số rồi tìm số ấy.',
           'Hiệu hai chữ số: 45 : 9 = 5. Tra bảng cặp có tổng 9: cặp có hiệu 5 là 7 và '
           '2. Số cần tìm là 72.'),
    ] + [
        q_tf(1, 'Tráo hai chữ số rồi trừ thì hiệu luôn chia hết cho 9.', True,
             'Đúng, vì hiệu bằng 9 nhân hiệu hai chữ số.'),
        q_tf(2, 'Tráo hai chữ số rồi cộng thì tổng luôn chia hết cho 9.', False,
             'Sai. Cộng thì mang họ 11 chứ không phải họ 9.'),
        q_mcq(3, 'Tính 72 − 27.', ['45', '54', '99', '35'], '45',
              'Hiệu hai chữ số là 5, nhân 9 được 45.'),
        q_mcq(4, 'Một số hai chữ số cộng với số viết ngược của nó luôn bằng',
              ['11 nhân tổng hai chữ số', '9 nhân tổng hai chữ số',
               '11 nhân hiệu hai chữ số'], '11 nhân tổng hai chữ số',
              'Mỗi chữ số một lần đứng hàng chục, một lần hàng đơn vị, nên góp đúng '
              '11 lần chính nó.'),
        q_tf(5, 'Nếu hiệu của một số và số viết ngược là 45 thì hai chữ số của nó chênh '
                'nhau 5.', True, 'Đúng, vì 45 : 9 = 5.'),
    ],
)

MOI = [B01, B82, B83, B02, B84, B03, B85, B04]

# Bài mới chèn vào đâu — khai theo BÀI ĐỨNG TRƯỚC, không khai theo số thứ tự.
SAU = {
    'DL:KSN4.B82': 'DL:KSN4.B01',
    'DL:KSN4.B83': 'DL:KSN4.B82',
    'DL:KSN4.B84': 'DL:KSN4.B02',
    'DL:KSN4.B85': 'DL:KSN4.B03',
}

BON_HANG = ['chục', 'trăm', 'nghìn']

O_NHAP_MOI = {
 'DL:KSN4.B01#C1': {'parts': [{'label': 'số chữ số', 'value': 5},
                              {'label': 'số lớp', 'value': 2}]},
 'DL:KSN4.B01#C2': {'value': 24},
 'DL:KSN4.B01#C3': {'parts': [{'label': 'lớp đơn vị đọc là',
                               'options': ['ba trăm năm mươi tám', 'ba trăm năm mươi',
                                           'ba năm tám'],
                               'value': 'ba trăm năm mươi tám'}]},
 'DL:KSN4.B01#C4': {'value': 3},
 'DL:KSN4.B01#C5': {'value': 745},
 'DL:KSN4.B01#C6': {'value': 602040},
 'DL:KSN4.B01#C7': {'parts': [{'label': 'hàng nào', 'options': BON_HANG,
                               'value': 'chục'}]},
 'DL:KSN4.B01#C8': {'value': 1},
 'DL:KSN4.B01#C9': {'value': 3508206},

 'DL:KSN4.B82#C1': {'parts': [{'label': 'hàng nào',
                               'options': ['trăm nghìn', 'chục nghìn', 'nghìn'],
                               'value': 'trăm nghìn'}]},
 'DL:KSN4.B82#C2': {'value': 700000},
 'DL:KSN4.B82#C3': {'value': 4000},
 'DL:KSN4.B82#C4': {'value': 4},
 'DL:KSN4.B82#C5': {'value': 50000},
 'DL:KSN4.B82#C6': {'parts': [{'label': 'chữ số 0 ở hàng', 'options': BON_HANG,
                               'value': 'trăm'},
                              {'label': 'chữ số 3 đáng bao nhiêu', 'value': 3000}]},
 'DL:KSN4.B82#C7': {'value': 52604},
 'DL:KSN4.B82#C8': {'parts': [{'label': 'chữ số đứng đầu', 'value': 700},
                              {'label': 'chữ số đứng giữa', 'value': 70},
                              {'label': 'chữ số đứng cuối', 'value': 7}]},
 'DL:KSN4.B82#C9': {'value': 5940},

 'DL:KSN4.B83#C1': {'value': 5},
 'DL:KSN4.B83#C2': {'parts': [{'label': 'chữ số hàng chục', 'value': 6},
                              {'label': 'chữ số hàng đơn vị', 'value': 3}]},
 'DL:KSN4.B83#C3': {'value': 63},
 'DL:KSN4.B83#C4': {'value': 52},
 'DL:KSN4.B83#C5': {'value': 65},
 'DL:KSN4.B83#C6': {'value': 5},
 'DL:KSN4.B83#C7': {'value': 90},
 'DL:KSN4.B83#C8': {'value': 84},
 'DL:KSN4.B83#C9': {'value': 63},

 'DL:KSN4.B02#C1': {'value': 35000},
 'DL:KSN4.B02#C2': {'value': 31500},
 'DL:KSN4.B02#C3': {'value': 9},
 'DL:KSN4.B02#C4': {'parts': [{'label': 'số mới', 'value': 240},
                              {'label': 'tăng thêm', 'value': 216}]},
 'DL:KSN4.B02#C5': {'value': 24},
 'DL:KSN4.B02#C6': {'parts': [{'label': 'số mới', 'value': 355},
                              {'label': 'tăng thêm', 'value': 320}]},
 'DL:KSN4.B02#C7': {'value': 35},
 'DL:KSN4.B02#C8': {'parts': [{'label': 'chín lần số cũ', 'value': 108},
                              {'label': 'tất cả tăng thêm', 'value': 115}]},
 'DL:KSN4.B02#C9': {'value': 33},

 'DL:KSN4.B84#C1': {'value': 475},
 'DL:KSN4.B84#C2': {'value': 400},
 'DL:KSN4.B84#C3': {'value': 804},
 'DL:KSN4.B84#C4': {'value': 720},
 'DL:KSN4.B84#C5': {'value': 600},
 'DL:KSN4.B84#C6': {'value': 5},
 'DL:KSN4.B84#C7': {'parts': [{'label': 'số mới', 'value': 501},
                              {'label': 'tăng thêm', 'value': 450}]},
 'DL:KSN4.B84#C8': {'value': 7},
 'DL:KSN4.B84#C9': {'parts': [{'label': 'thêm bên trái được', 'value': 347},
                              {'label': 'xen vào giữa được', 'value': 407},
                              {'label': 'cách nào cho số lớn hơn',
                               'options': ['xen vào giữa', 'thêm bên trái'],
                               'value': 'xen vào giữa'}]},

 'DL:KSN4.B03#C1': {'value': 470},
 'DL:KSN4.B03#C2': {'value': 4700},
 'DL:KSN4.B03#C3': {'value': 47},
 'DL:KSN4.B03#C4': {'value': 35000},
 'DL:KSN4.B03#C5': {'parts': [{'label': 'số ghi sai', 'value': 35000},
                              {'label': 'sổ bị hụt', 'value': 315000}]},
 'DL:KSN4.B03#C6': {'value': 9},
 'DL:KSN4.B03#C7': {'value': 6000},
 'DL:KSN4.B03#C8': {'value': 10},
 'DL:KSN4.B03#C9': {'parts': [{'label': 'số ấy', 'value': 820},
                              {'label': 'nhân 100 thì được', 'value': 82000}]},

 'DL:KSN4.B85#C1': {'value': 25},
 'DL:KSN4.B85#C2': {'value': 700},
 'DL:KSN4.B85#C3': {'value': 30},
 'DL:KSN4.B85#C4': {'value': 273},
 'DL:KSN4.B85#C5': {'value': 6},
 'DL:KSN4.B85#C6': {'value': 485},
 'DL:KSN4.B85#C7': {'value': 4371},
 'DL:KSN4.B85#C8': {'parts': [{'label': 'số mới', 'value': 30},
                              {'label': 'số cũ', 'value': 303}]},
 'DL:KSN4.B85#C9': {'value': 10},

 'DL:KSN4.B04#C1': {'value': 45},
 'DL:KSN4.B04#C2': {'parts': [{'label': 'hiệu hai chữ số', 'value': 5},
                              {'label': 'gấp mấy lần', 'value': 9}]},
 'DL:KSN4.B04#C3': {'value': 121},
 'DL:KSN4.B04#C4': {'parts': [{'label': 'tổng hai chữ số', 'value': 11},
                              {'label': 'gấp mấy lần', 'value': 11}]},
 'DL:KSN4.B04#C5': {'value': 27},
 'DL:KSN4.B04#C6': {'value': 27},
 'DL:KSN4.B04#C7': {'value': 88},
 'DL:KSN4.B04#C8': {'value': 5},
 'DL:KSN4.B04#C9': {'parts': [{'label': 'hiệu hai chữ số', 'value': 5},
                              {'label': 'số cần tìm', 'value': 72}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN4.B{n:02d}' for n in (1, 2, 3, 4)}
    moi_ = {f'DL:KSN4.B{n}' for n in (82, 83, 84, 85)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        for m in ('chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
    # Số neo của chương — chỉ soi bài có tính toán trên bộ số ấy.
    NEO = {'DL:KSN4.B01': '24 358', 'DL:KSN4.B82': '1 745 230',
           'DL:KSN4.B02': '3 500', 'DL:KSN4.B03': '350 000', 'DL:KSN4.B04': '72'}
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
        print(f"  {b['id']}  {b['ten'][:54]:54} {n} luyện + {q} quiz")
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
