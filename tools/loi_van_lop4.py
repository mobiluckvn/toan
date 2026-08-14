# -*- coding: utf-8 -*-
"""CHƯƠNG 8 · BÀI TOÁN LỜI VĂN — ĐỢT MỘT: năm bài đầu.

Chương này KHÁC hẳn năm chương trước, và phải nói rõ chỗ khác:

  · Chương 3 tới 7, sáu bảy bài là các mặt của MỘT ý (dấu hiệu chia hết, trung bình
    cộng, tổng - hiệu, tỉ số). Nên mỗi chương có một bài khái niệm gốc và một bộ neo
    chạy suốt.
  · Chương 8 thì mỗi bài là MỘT PHƯƠNG PHÁP RIÊNG — tuổi, làm chung, tính ngược, giả
    thiết tạm, khử và thế, sơ đồ Ven. Không có khái niệm gốc chung, và **không có một
    bộ neo nào chở nổi cả chương**. Ép một bộ neo vào đây là gượng.

Nên chương này neo THEO CẶP: hai bài tuổi dùng chung một bộ số, hai bài làm chung
dùng chung một bộ số. Bài tính ngược đứng riêng, vì nó vốn là một trò chơi một mình.

── ĐỢT NÀY LÀM NĂM BÀI ──
Bác muốn xem khuôn trước rồi mới làm nốt. Năm bài sau (giả thiết tạm · khử · thế ·
sơ đồ Ven · nguyên lý chuồng thỏ) để đợt hai; B35 B36 B37 tạm giữ nguyên bài chữ cũ.

    python3 tools/loi_van_lop4.py --xem
    python3 tools/loi_van_lop4.py
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

TEN_CHUONG = 'BÀI TOÁN LỜI VĂN'
CHUONG = 8
CO_KHONG = ['có', 'không']

LUI_TUOI = {'ve': ['DL:KSN3.B20'], 'ten': ['TOÁN TUỔI HAI GIA ĐÌNH'],
            'canCu': 'chuDe', 'lopDuoi': 3}
LUI_DON_VI = {'ve': ['DL:KSN3.B21'], 'ten': ['RÚT VỀ ĐƠN VỊ'],
              'canCu': 'chuDe', 'lopDuoi': 3}
LUI_LUI = {'ve': ['DL:KSN3.B22'], 'ten': ['ĐI LÙI NHIỀU TRẠM'],
           'canCu': 'chuDe', 'lopDuoi': 3}
LUI_GA = {'ve': ['DL:KSN3.B23'], 'ten': ['GÀ - CHÓ RỜI TRANG TRẠI'],
          'canCu': 'sach', 'lopDuoi': 3}
LUI_THAY = {'ve': ['DL:KSN3.B26'], 'ten': ['TRÒ CHƠI THAY THẾ'],
            'canCu': 'chuDe', 'lopDuoi': 3}
LUI_VEN = {'ve': ['DL:KSN3.B25'], 'ten': ['SƠ ĐỒ VEN HAI VÒNG'],
           'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B32 · BÀI TOÁN TUỔI · MỘT MỐC — không có gì mới, chỉ là NHẬN RA
# ═══════════════════════════════════════════════════════════════════════════
# Ý duy nhất của bài: bài toán tuổi ở MỘT thời điểm không phải dạng mới. Nó chính là
# tổng - hiệu hoặc tổng - tỉ mặc áo khác. Dạy được điều ấy thì bé bớt sợ hẳn — chương
# này vốn làm bé sợ vì tưởng mỗi bài một phép thần.
B32 = bai(
    32, 'BÀI TOÁN TUỔI Ở MỘT THỜI ĐIỂM — LÀ BÀI CŨ MẶC ÁO MỚI',
    'Dạng gốc: LV 6.1 mức Lớp 4 — Bài toán tuổi tại một mốc thời gian, đưa về tổng - '
    'hiệu hoặc tổng - tỉ đã học.',
    'Hai chương vừa rồi con đã giải tổng - hiệu và tổng - tỉ rất thạo. Hôm nay con sẽ '
    'thấy một điều nhẹ cả người: bài toán tuổi ở một thời điểm KHÔNG phải dạng mới. '
    'Nó chính là bài cũ, chỉ thay chữ "số" bằng chữ "tuổi".',
    LUI_TUOI,
    video(
        ['Nhận ra bài toán tuổi một mốc là tổng - hiệu hay tổng - tỉ.',
         'Vẽ được sơ đồ đoạn thẳng cho tuổi hai người.',
         'Giải xong biết thử lại bằng cả tổng lẫn hiệu.'],
        ['Đề bài: Tổng số tuổi của hai mẹ con là 36. Mẹ hơn con 24 tuổi. Tính tuổi mỗi '
         'người.',
         'Đọc lại đề cho kỹ',
         'Đề cho TỔNG là 36 và HIỆU là 24. Đúng hai thứ mà bài tổng - hiệu cần.',
         'Vẽ sơ đồ như cũ',
         'Đoạn ngắn là tuổi con, đoạn dài là tuổi mẹ, khúc dôi ra là 24, ngoặc ngoài '
         'là 36.',
         'Dùng công thức đã học',
         'Tuổi mẹ là số lớn: 36 + 24 = 60, rồi 60 : 2 = 30 tuổi.',
         'Tìm tuổi con',
         'Tuổi con là 36 − 30 = 6 tuổi.',
         'Thử lại',
         'Cộng lại: 30 + 6 = 36, đúng bằng tổng. Trừ nhau: 30 − 6 = 24, đúng bằng hiệu.',
         'Đáp số: mẹ 30 tuổi, con 6 tuổi.'],
        ['Có bạn thấy chữ "tuổi" là hoảng, tưởng phải có cách giải riêng cho bài toán '
         'tuổi.',
         'Gợi ý 1: Con thử che chữ "tuổi" đi rồi đọc lại đề xem.',
         'Gợi ý 2: Đề nói tổng hai số là 36, số này hơn số kia 24. Con đã giải dạng ấy '
         'rồi mà.',
         'Chữa: bài toán tuổi ở một thời điểm chính là bài tổng - hiệu. Không có phép '
         'nào mới cả, chỉ là chữ khác.'],
        ['Bảo con che chữ "tuổi" trong đề rồi đọc lại. Con nhận ra đó là bài cũ thì đã '
         'nắm được ý chính của bài này.',
         'Chương này hay làm con sợ vì tưởng mỗi bài một phép riêng. Bố mẹ nhấn giúp: '
         'phần lớn là bài cũ mặc áo mới.'],
    ),
    [
        lt(1, 1, 'Tổng tuổi hai mẹ con là 36, mẹ hơn con 24 tuổi — đúng bài trong video. '
                 'Đề đang cho con biết TỔNG và HIỆU, hay TỔNG và TỈ SỐ?',
           'Cho TỔNG (36) và HIỆU (24). Vậy đây là bài tổng - hiệu.'),
        lt(2, 1, 'Vẫn bài trên. Tính tuổi mẹ.',
           'Tuổi mẹ là số lớn. 36 + 24 = 60, rồi 60 : 2 = 30 tuổi.'),
        lt(3, 1, 'Vẫn bài trên. Tính tuổi con rồi thử lại.',
           'Tuổi con là 36 − 30 = 6 tuổi. Thử: 30 + 6 = 36 và 30 − 6 = 24, đúng cả hai.'),
        lt(4, 2, 'Tổng tuổi hai anh em là 30, tuổi em bằng một nửa tuổi anh. Tính tuổi '
                 'mỗi người.',
           'Đây là bài tổng - tỉ, tỉ số 1 : 2. Cả thảy 3 phần, một phần là 30 : 3 = 10. '
           'Em 10 tuổi, anh 20 tuổi.'),
        lt(5, 2, 'Bạn Nam thấy chữ "tuổi" là hoảng, tưởng phải có cách giải riêng. Bạn '
                 'nhầm ở đâu?',
           'Bài toán tuổi ở một thời điểm chính là bài tổng - hiệu hoặc tổng - tỉ đã '
           'học. Che chữ "tuổi" đi thì thấy ngay là bài cũ.'),
        lt(6, 2, 'Bố hơn con 28 tuổi, tổng số tuổi hai bố con là 44. Tính tuổi mỗi người.',
           'Tuổi bố: 44 + 28 = 72, rồi 72 : 2 = 36 tuổi. Tuổi con: 44 − 36 = 8 tuổi.'),
        lt(7, 2, 'Tổng tuổi ba mẹ con là 60, mẹ 34 tuổi, anh hơn em 4 tuổi. Tính tuổi '
                 'hai anh em.',
           'Tổng tuổi hai anh em: 60 − 34 = 26. Anh: 26 + 4 = 30, rồi 30 : 2 = 15 tuổi. '
           'Em: 26 − 15 = 11 tuổi.'),
        lt(8, 3, 'Tuổi mẹ gấp 5 lần tuổi con, tổng số tuổi hai mẹ con là 36. Tính tuổi '
                 'mỗi người.',
           'Bài tổng - tỉ, tỉ số 1 : 5, cả thảy 6 phần. Một phần là 36 : 6 = 6. Con 6 '
           'tuổi, mẹ 30 tuổi.'),
        lt(9, 3, 'Tuổi mẹ hơn tuổi con 24 tuổi và tuổi mẹ gấp 5 lần tuổi con. Tính tuổi '
                 'mỗi người.',
           'Bài hiệu - tỉ, tỉ số 1 : 5, phần chênh 4 phần. Một phần là 24 : 4 = 6. Con '
           '6 tuổi, mẹ 30 tuổi.'),
        q_tf(1, 'Bài toán tuổi ở một thời điểm có thể đưa về bài tổng - hiệu đã học.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Bài toán tuổi phải có một cách giải riêng, không dùng được cách cũ.',
             False, 'SAI — che chữ "tuổi" đi thì thấy ngay là bài cũ.'),
        q_mcq(3, 'Tổng tuổi hai mẹ con là 36, mẹ hơn con 24 tuổi. Tuổi mẹ là:',
              ['A. 30', 'B. 24', 'C. 6'], 'A. 30', '36 + 24 = 60, rồi 60 : 2 = 30.'),
        q_mcq(4, '"Tổng tuổi là 30, tuổi em bằng một nửa tuổi anh" là dạng:',
              ['A. tổng - tỉ', 'B. tổng - hiệu', 'C. hiệu - tỉ'],
              'A. tổng - tỉ', 'Đề cho tổng và tỉ số.'),
        q_mcq(5, 'Tuổi mẹ gấp 5 lần tuổi con, tổng là 36. Tuổi con là:',
              ['A. 6', 'B. 30', 'C. 9'], 'A. 6', 'Cả thảy 6 phần, một phần là 6.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B64 · BÀI TOÁN TUỔI · HAI MỐC — hiệu tuổi không đổi
# ═══════════════════════════════════════════════════════════════════════════
# Đây mới là bài có ý MỚI, và ý ấy chỉ có một: hiệu tuổi không bao giờ đổi, nên nó là
# sợi dây nối hai thời điểm. Bé đã gặp câu ấy ở chương 6 (cùng thêm vào cả hai số),
# nay dùng nó làm chìa khoá.
B64 = bai(
    64, 'BÀI TOÁN TUỔI Ở HAI THỜI ĐIỂM — HIỆU TUỔI KHÔNG BAO GIỜ ĐỔI',
    'Dạng gốc: LV 6.2 mức Lớp 4 — Bài toán tuổi nối hai mốc thời gian bằng hiệu tuổi '
    'không đổi.',
    'Ở chương tổng - hiệu con đã biết một điều: cùng thêm vào cả hai số thì hiệu không '
    'đổi. Hôm nay con dùng chính điều ấy — vì hiệu tuổi không bao giờ '
    'đổi, nó nối được hiện tại với tương lai.',
    LUI_TUOI,
    video(
        ['Dùng hiệu tuổi không đổi để nối hai thời điểm.',
         'Tìm tuổi tại thời điểm sau bằng hiệu và tỉ số.',
         'Suy ra khoảng thời gian giữa hai mốc.'],
        ['Đề bài: Hiện nay mẹ 30 tuổi, con 6 tuổi. Hỏi sau bao nhiêu năm nữa thì tuổi '
         'mẹ gấp 3 lần tuổi con?',
         'Tìm cái KHÔNG đổi',
         'Hiệu tuổi hiện nay: 30 − 6 = 24 tuổi. Cả hai cùng lớn lên nên hiệu này không '
         'bao giờ đổi.',
         'Sang thời điểm sau',
         'Lúc ấy tuổi mẹ gấp 3 lần tuổi con, tức tỉ số 1 trên 3. Nhưng hiệu vẫn là 24.',
         'Đây là bài hiệu - tỉ đã học',
         'Phần chênh là 3 − 1 = 2 phần, ứng với 24 tuổi. Một phần là 24 : 2 = 12.',
         'Tuổi lúc ấy',
         'Con 12 tuổi, mẹ 36 tuổi. Kiểm lại: 36 gấp 3 lần 12, và 36 − 12 = 24, đúng hiệu.',
         'Sau bao nhiêu năm',
         'Con từ 6 tuổi lên 12 tuổi, vậy sau 6 năm nữa.',
         'Đáp số: sau 6 năm nữa.'],
        ['Có bạn nghĩ sau vài năm thì hiệu tuổi cũng tăng theo, nên đi tìm hiệu mới.',
         'Gợi ý 1: Mỗi năm mẹ thêm mấy tuổi? Con thêm mấy tuổi?',
         'Gợi ý 2: Cả hai cùng thêm một tuổi, nên khoảng cách giữa hai người có đổi không?',
         'Chữa: không đổi. Hiệu tuổi là thứ DUY NHẤT đứng yên trong bài này, và chính '
         'vì đứng yên nên nó mới nối được hai thời điểm.'],
        ['Hỏi con: "Bố hơn con mấy tuổi? Hai mươi năm nữa bố hơn con mấy tuổi?" Trả lời '
         'cùng một số là con đã nắm chìa khoá.',
         'Bài này khó ở chỗ nhận ra cái gì đứng yên. Bố mẹ hỏi giúp: "Trong bài này, '
         'cái gì không đổi?"'],
    ),
    [
        lt(1, 1, 'Hiện nay mẹ 30 tuổi, con 6 tuổi — đúng bài trong video. Hiệu tuổi hai '
                 'mẹ con là bao nhiêu?',
           '30 − 6 = 24 tuổi.'),
        lt(2, 1, 'Vẫn bài trên. Sau 10 năm nữa hiệu tuổi hai mẹ con là bao nhiêu?',
           'Vẫn 24 tuổi. Cả hai cùng thêm 10 tuổi nên hiệu không đổi.'),
        lt(3, 1, 'Vẫn bài trên. Khi tuổi mẹ gấp 3 lần tuổi con thì phần chênh là mấy phần?',
           'Tỉ số 1 : 3, phần chênh là 3 − 1 = 2 phần.'),
        lt(4, 2, 'Vẫn bài trên. Tính tuổi hai mẹ con lúc mẹ gấp 3 lần con.',
           'Một phần là 24 : 2 = 12. Con 12 tuổi, mẹ 36 tuổi.'),
        lt(5, 2, 'Vẫn bài trên. Vậy sau bao nhiêu năm nữa?',
           'Con từ 6 lên 12 tuổi, nên sau 6 năm nữa.'),
        lt(6, 2, 'Bạn Lan đi tìm hiệu tuổi MỚI sau vài năm. Bạn nhầm ở đâu?',
           'Hiệu tuổi không bao giờ đổi, vì mỗi năm cả hai cùng thêm một tuổi. Không có '
           'hiệu mới nào cả.'),
        lt(7, 2, 'Anh hơn em 8 tuổi. Khi tuổi anh gấp 3 lần tuổi em thì em bao nhiêu tuổi?',
           'Phần chênh 2 phần ứng với 8 tuổi, một phần là 8 : 2 = 4. Em 4 tuổi, anh 12 tuổi.'),
        lt(8, 3, 'Hiện nay bố 40 tuổi, con 10 tuổi. Hỏi sau bao nhiêu năm nữa tuổi bố '
                 'gấp đôi tuổi con?',
           'Hiệu 30 tuổi không đổi. Lúc ấy tỉ số 1 : 2, phần chênh 1 phần ứng với 30. '
           'Con 30 tuổi, bố 60 tuổi. Con từ 10 lên 30, vậy sau 20 năm.'),
        lt(9, 3, 'Cách đây 3 năm mẹ 27 tuổi, con 3 tuổi. Hỏi hiện nay tuổi mẹ gấp mấy '
                 'lần tuổi con?',
           'Hiện nay mẹ 30 tuổi, con 6 tuổi. 30 : 6 = 5, nên tuổi mẹ gấp 5 lần tuổi con.'),
        q_tf(1, 'Hiệu tuổi của hai người không bao giờ thay đổi.', True,
             'Đáp án: ĐÚNG — mỗi năm cả hai cùng thêm một tuổi.'),
        q_tf(2, 'Sau 10 năm thì hiệu tuổi hai mẹ con tăng thêm 10.', False,
             'SAI — hiệu tuổi đứng yên.'),
        q_mcq(3, 'Mẹ 30 tuổi, con 6 tuổi. Hiệu tuổi là:',
              ['A. 24', 'B. 36', 'C. 5'], 'A. 24', '30 − 6 = 24.'),
        q_mcq(4, 'Khi tuổi mẹ gấp 3 lần tuổi con thì phần chênh là:',
              ['A. 2 phần', 'B. 3 phần', 'C. 4 phần'], 'A. 2 phần', '3 − 1 = 2.'),
        q_mcq(5, 'Trong bài toán tuổi hai mốc, thứ đứng yên là:',
              ['A. hiệu tuổi', 'B. tổng tuổi', 'C. tỉ số tuổi'],
              'A. hiệu tuổi', 'Tổng và tỉ số đều đổi theo thời gian.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B33 · LÀM CHUNG CÔNG VIỆC — chia việc thành phần
# ═══════════════════════════════════════════════════════════════════════════
# Lớp 4 chưa học phân số nên KHÔNG dùng lối "mỗi giờ làm được một phần mấy công việc".
# Lối của lớp 4 là chia công việc thành số phần chia hết cho cả hai thời gian — vừa
# đúng sức bé, vừa nhìn thấy được trên hình.
B33 = bai(
    33, 'LÀM CHUNG CÔNG VIỆC — CHIA CÔNG VIỆC THÀNH PHẦN',
    'Dạng gốc: LV 7.1 mức Lớp 4 — Hai người làm chung, giải bằng cách chia công việc '
    'thành số phần chia hết cho cả hai thời gian. KHÔNG dùng phân số.',
    'Hai người cùng làm một việc thì xong nhanh hơn — nhưng nhanh bao nhiêu? Hôm nay '
    'con học một cách rất gọn: chia công việc thành những phần bằng nhau, rồi đếm mỗi '
    'người làm được mấy phần trong một giờ.',
    LUI_DON_VI,
    video(
        ['Chia công việc thành số phần chia hết cho cả hai thời gian.',
         'Tính số phần mỗi người làm được trong một giờ.',
         'Cộng lại để biết làm chung mất mấy giờ.'],
        ['Đề bài: Anh làm một mình xong việc trong 6 giờ, em làm một mình xong việc ấy '
         'trong 12 giờ. Hỏi hai anh em làm chung thì mấy giờ xong?',
         'Chia công việc thành phần',
         'Chọn số phần chia hết cho cả 6 và 12. Số gọn nhất là 12 phần.',
         'Mỗi người làm được mấy phần một giờ',
         'Anh xong 12 phần trong 6 giờ, nên mỗi giờ anh làm 12 : 6 = 2 phần.',
         'Em xong 12 phần trong 12 giờ, nên mỗi giờ em làm 12 : 12 = 1 phần.',
         'Làm chung một giờ được mấy phần',
         'Cộng lại: 2 + 1 = 3 phần mỗi giờ.',
         'Chia ra thời gian',
         'Cả việc là 12 phần, mỗi giờ làm 3 phần, nên xong sau 12 : 3 = 4 giờ.',
         'Đáp số: hai anh em làm chung 4 giờ thì xong.'],
        ['Có bạn cộng thẳng hai thời gian rồi chia đôi: 6 cộng 12 bằng 18, chia hai '
         'được 9 giờ.',
         'Gợi ý 1: Anh làm một mình đã xong trong 6 giờ rồi. Có thêm em giúp mà lại lâu '
         'hơn thành 9 giờ à?',
         'Gợi ý 2: Làm chung thì phải NHANH HƠN người nhanh nhất chứ.',
         'Chữa: không cộng thời gian được. Phải đếm số PHẦN làm được mỗi giờ rồi mới '
         'cộng. Đáp số đúng là 4 giờ, nhanh hơn cả 6 giờ.'],
        ['Hỏi con một câu soi rất nhanh: "Làm chung thì phải nhanh hơn hay chậm hơn '
         'người làm nhanh nhất?" Nhanh hơn — nên đáp số lớn hơn 6 là chắc chắn sai.',
         'Con hay cộng thẳng thời gian. Bố mẹ nhấn: cộng được là cộng SỐ PHẦN mỗi giờ, '
         'không phải cộng giờ.'],
    ),
    [
        lt(1, 1, 'Anh xong việc trong 6 giờ, em xong trong 12 giờ — đúng bài trong video. '
                 'Nên chia công việc thành mấy phần cho gọn?',
           '12 phần — vì 12 chia hết cho cả 6 và 12.'),
        lt(2, 1, 'Vẫn bài trên. Mỗi giờ anh làm được mấy phần, em làm được mấy phần?',
           'Anh: 12 : 6 = 2 phần. Em: 12 : 12 = 1 phần.'),
        lt(3, 1, 'Vẫn bài trên. Làm chung thì mấy giờ xong?',
           'Mỗi giờ chung làm 2 + 1 = 3 phần. Cả việc 12 phần nên 12 : 3 = 4 giờ.'),
        lt(4, 2, 'Bạn Bình cộng 6 với 12 rồi chia đôi, ra 9 giờ. Vì sao chắc chắn sai?',
           'Anh làm một mình đã xong trong 6 giờ. Có thêm người giúp thì phải nhanh hơn '
           '6 giờ, không thể thành 9 giờ.'),
        lt(5, 2, 'Một vòi chảy đầy bể trong 4 giờ, vòi kia chảy đầy trong 12 giờ. Mở cả '
                 'hai thì mấy giờ đầy bể?',
           'Chia bể thành 12 phần. Vòi một: 12 : 4 = 3 phần mỗi giờ; vòi hai: 1 phần. '
           'Chung 4 phần mỗi giờ, nên 12 : 4 = 3 giờ.'),
        lt(6, 2, 'Vì sao ta chọn 12 phần mà không chọn 5 phần?',
           'Vì 12 chia hết cho cả 6 và 12, nên số phần mỗi giờ ra số tròn. Chọn 5 thì '
           'chia không hết, tính ra số lẻ rất khó.'),
        lt(7, 2, 'Hai người làm chung xong một việc trong 4 giờ. Người thứ nhất làm một '
                 'mình xong trong 6 giờ. Mỗi giờ người thứ hai làm được mấy phần trong '
                 '12 phần?',
           'Chung mỗi giờ 12 : 4 = 3 phần. Người thứ nhất 12 : 6 = 2 phần. Người thứ '
           'hai: 3 − 2 = 1 phần.'),
        lt(8, 3, 'Anh làm một mình xong trong 10 giờ, em xong trong 15 giờ. Làm chung '
                 'mấy giờ xong?',
           'Chia việc thành 30 phần. Anh 30 : 10 = 3 phần mỗi giờ, em 30 : 15 = 2 phần. '
           'Chung 5 phần mỗi giờ, nên 30 : 5 = 6 giờ.'),
        lt(9, 3, 'Ba người cùng làm một việc: người thứ nhất xong trong 4 giờ, người '
                 'thứ hai 6 giờ, người thứ ba 12 giờ. Cả ba làm chung mấy giờ xong?',
           'Chia việc thành 12 phần. Mỗi giờ: 3 phần, 2 phần và 1 phần. Chung 6 phần '
           'mỗi giờ, nên 12 : 6 = 2 giờ.'),
        q_tf(1, 'Làm chung bao giờ cũng nhanh hơn người làm nhanh nhất.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Muốn tính thời gian làm chung, ta cộng hai thời gian rồi chia đôi.',
             False, 'SAI — phải cộng số phần làm được mỗi giờ.'),
        q_mcq(3, 'Anh xong trong 6 giờ, em xong trong 12 giờ. Chung mấy giờ xong?',
              ['A. 4 giờ', 'B. 9 giờ', 'C. 18 giờ'], 'A. 4 giờ',
              'Mỗi giờ chung 3 phần trong 12 phần.'),
        q_mcq(4, 'Chia công việc thành mấy phần thì gọn nhất khi hai người xong trong '
                 '6 giờ và 12 giờ?',
              ['A. 12 phần', 'B. 6 phần', 'C. 18 phần'], 'A. 12 phần',
              'Chia hết cho cả 6 và 12.'),
        q_mcq(5, 'Hai người làm chung mà ra đáp số 9 giờ, trong khi một người làm riêng '
                 'chỉ 6 giờ. Điều đó có nghĩa:',
              ['A. bài làm sai', 'B. bài làm đúng', 'C. còn tuỳ'],
              'A. bài làm sai', 'Làm chung phải nhanh hơn.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B65 · LÀM CHUNG RỒI MỘT NGƯỜI NGHỈ
# ═══════════════════════════════════════════════════════════════════════════
# Không có phép mới — chỉ là dùng lại đúng cách đếm phần của bài trước, thêm một bước
# trừ. Tách riêng vì đây là chỗ bé phải TỰ THEO DÕI công việc còn lại bao nhiêu phần,
# và quên trừ là sai cả bài.
B65 = bai(
    65, 'LÀM CHUNG RỒI MỘT NGƯỜI NGHỈ — ĐẾM SỐ PHẦN CÒN LẠI',
    'Dạng gốc: LV 7.2 mức Lớp 4 — Hai người làm chung một lúc rồi một người nghỉ; '
    'theo dõi số phần đã làm và số phần còn lại.',
    'Bài trước con đã biết đếm số phần mỗi giờ. Hôm nay vẫn cách đếm ấy, chỉ thêm một '
    'việc: theo dõi xem đã làm được mấy phần rồi và còn lại mấy phần. Không có phép '
    'nào mới cả.',
    LUI_DON_VI,
    video(
        ['Tính số phần đã làm được trong khoảng thời gian làm chung.',
         'Tính số phần còn lại.',
         'Tính thời gian người còn lại làm nốt.'],
        ['Đề bài: Anh làm một mình xong trong 6 giờ, em xong trong 12 giờ. Hai anh em '
         'làm chung 2 giờ thì anh phải nghỉ, em làm nốt. Hỏi em còn phải làm mấy giờ nữa?',
         'Vẫn chia việc thành 12 phần',
         'Mỗi giờ anh làm 2 phần, em làm 1 phần, chung được 3 phần.',
         'Hai giờ làm chung được mấy phần',
         'Mỗi giờ 3 phần, hai giờ là 3 × 2 = 6 phần.',
         'Còn lại mấy phần',
         'Cả việc 12 phần, đã làm 6 phần, còn 12 − 6 = 6 phần.',
         'Em làm nốt mất mấy giờ',
         'Em làm 1 phần mỗi giờ, còn 6 phần nên mất 6 : 1 = 6 giờ.',
         'Đáp số: em còn phải làm 6 giờ nữa.'],
        ['Có bạn tính xong 6 phần còn lại rồi lấy 6 chia cho 3 phần mỗi giờ, ra 2 giờ.',
         'Gợi ý 1: Sau khi anh nghỉ thì còn mấy người làm?',
         'Gợi ý 2: Còn một mình em. Vậy mỗi giờ làm được mấy phần?',
         'Chữa: em một mình chỉ làm 1 phần mỗi giờ, nên phải chia cho 1, được 6 giờ. '
         'Lấy 3 phần là vẫn tính như còn cả hai người.'],
        ['Bảo con vẽ 12 ô rồi tô dần: hai giờ đầu tô 6 ô, còn 6 ô để trống. Con nhìn '
         'thấy phần còn lại thì khó quên trừ.',
         'Chỗ sai duy nhất là quên rằng sau khi một người nghỉ thì tốc độ đổi. Bố mẹ '
         'hỏi: "Bây giờ còn mấy người làm?"'],
    ),
    [
        lt(1, 1, 'Anh 6 giờ, em 12 giờ, chia việc thành 12 phần — đúng bài trong video. '
                 'Làm chung mỗi giờ được mấy phần?',
           'Anh 2 phần, em 1 phần, chung 2 + 1 = 3 phần mỗi giờ.'),
        lt(2, 1, 'Vẫn bài trên. Làm chung 2 giờ thì được mấy phần?',
           '3 × 2 = 6 phần.'),
        lt(3, 1, 'Vẫn bài trên. Còn lại mấy phần?',
           '12 − 6 = 6 phần.'),
        lt(4, 2, 'Vẫn bài trên. Em làm nốt một mình thì mất mấy giờ?',
           'Em làm 1 phần mỗi giờ, còn 6 phần nên mất 6 giờ.'),
        lt(5, 2, 'Bạn Tú lấy 6 phần còn lại chia cho 3 phần mỗi giờ, ra 2 giờ. Bạn sai '
                 'ở đâu?',
           'Anh đã nghỉ nên chỉ còn em làm, mỗi giờ 1 phần. Lấy 3 phần là vẫn tính như '
           'còn cả hai người. Đúng là 6 giờ.'),
        lt(6, 2, 'Hai vòi cùng chảy vào bể: vòi một đầy bể trong 4 giờ, vòi hai trong '
                 '12 giờ. Mở cả hai trong 1 giờ rồi khoá vòi một. Vòi hai chảy nốt mất '
                 'mấy giờ?',
           'Chia bể 12 phần: vòi một 3 phần, vòi hai 1 phần, chung 4 phần. Một giờ được '
           '4 phần, còn 12 − 4 = 8 phần. Vòi hai chảy 1 phần mỗi giờ nên mất 8 giờ.'),
        lt(7, 2, 'Vì sao sau khi một người nghỉ thì phải tính lại số phần mỗi giờ?',
           'Vì số phần mỗi giờ là của những người ĐANG làm. Bớt một người thì tốc độ '
           'giảm, không dùng lại con số cũ được.'),
        lt(8, 3, 'Anh xong trong 12 giờ, em xong trong 6 giờ. Làm chung 2 giờ rồi em '
                 'nghỉ, anh làm nốt. Anh còn phải làm mấy giờ?',
           'Chia việc 12 phần: anh 1 phần, em 2 phần, chung 3 phần mỗi giờ. Hai giờ '
           'được 6 phần, còn 12 − 6 = 6 phần. Anh làm 1 phần mỗi giờ nên mất 6 giờ.'),
        lt(9, 3, 'Anh xong trong 6 giờ, em xong trong 12 giờ. Làm chung 3 giờ rồi anh '
                 'nghỉ. Em làm nốt mất mấy giờ?',
           'Chung 3 phần mỗi giờ, 3 giờ được 9 phần. Còn 12 − 9 = 3 phần. Em làm 1 phần '
           'mỗi giờ nên mất 3 giờ.'),
        q_tf(1, 'Sau khi một người nghỉ, số phần làm được mỗi giờ phải tính lại.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Phần còn lại vẫn chia cho số phần của cả hai người.', False,
             'SAI — chỉ còn một người làm.'),
        q_mcq(3, 'Chung 3 phần mỗi giờ, làm 2 giờ thì được:',
              ['A. 6 phần', 'B. 3 phần', 'C. 5 phần'], 'A. 6 phần', '3 × 2 = 6.'),
        q_mcq(4, 'Cả việc 12 phần, đã làm 6 phần thì còn:',
              ['A. 6 phần', 'B. 18 phần', 'C. 2 phần'], 'A. 6 phần', '12 − 6 = 6.'),
        q_mcq(5, 'Còn 6 phần, em làm 1 phần mỗi giờ thì mất:',
              ['A. 6 giờ', 'B. 2 giờ', 'C. 3 giờ'], 'A. 6 giờ', '6 : 1 = 6.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B34 · TÍNH NGƯỢC TỪ CUỐI  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Một ý duy nhất và rất gọn: đi ngược thì ĐỔI PHÉP. Cộng thành trừ, nhân thành chia,
# và đi từ số cuối cùng ngược về đầu.
B34 = bai(
    34, 'TÍNH NGƯỢC TỪ CUỐI — ĐI LÙI THÌ ĐỔI PHÉP',
    'Dạng gốc: LV 8.1 mức Lớp 4 — Tính ngược nhiều bước với bốn phép tính, đi từ kết '
    'quả cuối cùng ngược về số ban đầu.',
    'Có những bài chỉ cho con biết kết quả CUỐI CÙNG rồi hỏi số ban đầu. Đi xuôi thì '
    'chịu, vì chưa biết bắt đầu từ đâu. Nhưng đi lùi thì được — và đi lùi chỉ cần nhớ '
    'đúng một điều.',
    LUI_LUI,
    video(
        ['Đi ngược từ kết quả cuối về số ban đầu.',
         'Đổi phép khi đi lùi: cộng thành trừ, nhân thành chia.',
         'Thử lại bằng cách đi xuôi.'],
        ['Đề bài: Nghĩ một số, nhân với 2, rồi cộng 10, rồi trừ 4 thì được 26. Tìm số '
         'đã nghĩ.',
         'Đi xuôi thì chịu',
         'Vì chưa biết số ban đầu là bao nhiêu để mà nhân với 2.',
         'Nên đi lùi từ số cuối',
         'Số cuối là 26. Bước cuối cùng là trừ 4, nên đi lùi phải cộng 4: 26 + 4 = 30.',
         'Lùi tiếp',
         'Trước đó là cộng 10, nên đi lùi phải trừ 10: 30 − 10 = 20.',
         'Lùi nốt bước đầu',
         'Đầu tiên là nhân 2, nên đi lùi phải chia 2: 20 : 2 = 10.',
         'Thử lại bằng cách đi xuôi',
         'Lấy 10 nhân 2 được 20, cộng 10 được 30, trừ 4 được 26. Đúng bằng đề cho.',
         'Đáp số: số đã nghĩ là 10.'],
        ['Có bạn đi lùi nhưng giữ nguyên phép: thấy trừ 4 thì cũng trừ 4, được 22.',
         'Gợi ý 1: Đi xuôi con trừ 4 thì số nhỏ đi. Đi lùi thì số phải làm sao?',
         'Gợi ý 2: Phải to lại chứ. Vậy đi lùi của phép trừ là phép gì?',
         'Chữa: đi lùi thì ĐỔI PHÉP. Trừ thành cộng, cộng thành trừ, nhân thành chia, '
         'chia thành nhân. Giữ nguyên phép là đi sai hướng.'],
        ['Chơi với con: bố mẹ nghĩ một số rồi đọc các bước, con đi lùi tìm lại. Đổi vai '
         'vài lần là con thuộc.',
         'Chỗ sai duy nhất là quên đổi phép. Bố mẹ hỏi: "Đi lùi thì phép này thành phép gì?"'],
    ),
    [
        lt(1, 1, 'Nghĩ một số, nhân 2, cộng 10, trừ 4 thì được 26 — đúng bài trong video. '
                 'Bước cuối cùng là trừ 4, vậy đi lùi phải làm phép gì và được bao nhiêu?',
           'Đi lùi của trừ là cộng: 26 + 4 = 30.'),
        lt(2, 1, 'Vẫn bài trên. Lùi tiếp qua bước cộng 10 thì được bao nhiêu?',
           'Đi lùi của cộng là trừ: 30 − 10 = 20.'),
        lt(3, 1, 'Vẫn bài trên. Lùi nốt qua bước nhân 2 thì số đã nghĩ là bao nhiêu?',
           'Đi lùi của nhân là chia: 20 : 2 = 10.'),
        lt(4, 2, 'Thử lại bằng cách đi xuôi từ số 10. Con được bao nhiêu?',
           '10 × 2 = 20; 20 + 10 = 30; 30 − 4 = 26. Đúng bằng đề cho.'),
        lt(5, 2, 'Bạn Minh đi lùi mà vẫn trừ 4, được 22. Bạn sai ở đâu?',
           'Đi lùi thì phải ĐỔI PHÉP. Trừ thành cộng, nên phải lấy 26 + 4 = 30.'),
        lt(6, 2, 'Nghĩ một số, cộng 5, rồi nhân 3 thì được 30. Tìm số đã nghĩ.',
           'Đi lùi: 30 : 3 = 10; 10 − 5 = 5. Số đã nghĩ là 5.'),
        lt(7, 2, 'Đi lùi của phép chia là phép gì? Cho một ví dụ.',
           'Là phép nhân. Ví dụ đi xuôi chia 4 được 5 thì đi lùi lấy 5 × 4 = 20.'),
        lt(8, 3, 'Một số nhân 3, trừ 6, rồi chia 2 thì được 12. Tìm số đó.',
           'Đi lùi: 12 × 2 = 24; 24 + 6 = 30; 30 : 3 = 10. Số cần tìm là 10.'),
        lt(9, 3, 'An có một số kẹo. An cho bạn 4 cái, rồi mẹ cho thêm gấp đôi số còn '
                 'lại, thì An có 24 cái. Hỏi lúc đầu An có mấy cái kẹo?',
           'Mẹ cho thêm gấp đôi số còn lại nghĩa là số còn lại được nhân 3. Đi lùi: '
           '24 : 3 = 8; 8 + 4 = 12. Lúc đầu An có 12 cái kẹo.'),
        q_tf(1, 'Đi lùi thì phép cộng đổi thành phép trừ.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Đi lùi thì giữ nguyên phép như lúc đi xuôi.', False,
             'SAI — phải đổi phép, không thì đi sai hướng.'),
        q_mcq(3, 'Đi lùi của phép nhân là:',
              ['A. phép chia', 'B. phép cộng', 'C. phép nhân'], 'A. phép chia',
              'Hai phép ngược nhau.'),
        q_mcq(4, 'Số cuối là 26, bước cuối là trừ 4. Đi lùi được:',
              ['A. 30', 'B. 22', 'C. 26'], 'A. 30', '26 + 4 = 30.'),
        q_mcq(5, 'Một số nhân 2, cộng 10, trừ 4 được 26. Số đã nghĩ là:',
              ['A. 10', 'B. 20', 'C. 26'], 'A. 10', 'Đi lùi ba bước.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B35 · GIẢ THIẾT TẠM  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Ý duy nhất: ĐOÁN BỪA một trường hợp cực đoan, xem lệch bao nhiêu, rồi đổi dần cho
# khớp. Nghe lạ nhưng bé làm được ngay, vì mỗi lần đổi một con thì lệch đi đúng một
# con số cố định.
B35 = bai(
    35, 'GIẢ THIẾT TẠM — ĐOÁN BỪA RỒI SỬA DẦN',
    'Dạng gốc: LV 8.2 mức Lớp 4 — Phương pháp giả thiết tạm với bài gà - chó và bài '
    'hai loại vé.',
    'Có những bài chẳng biết bắt đầu từ đâu. Hôm nay con học một cách rất lạ mà rất '
    'hiệu quả: cứ đoán bừa một trường hợp dễ tính nhất, xem nó lệch bao nhiêu, rồi '
    'sửa dần cho khớp.',
    LUI_GA,
    video(
        ['Giả thiết tạm rằng tất cả cùng một loại.',
         'Tính phần lệch so với đề bài.',
         'Biết đổi một con thì lệch thay đổi bao nhiêu, rồi chia ra.'],
        ['Đề bài: Vừa gà vừa chó có 36 con, đếm được 100 cái chân. Tính số con mỗi loại.',
         'Đoán bừa cho dễ',
         'Giả sử tất cả 36 con đều là gà. Gà 2 chân nên có 36 × 2 = 72 chân.',
         'Xem lệch bao nhiêu',
         'Đề nói 100 chân, mà đoán ra 72 chân. Thiếu mất 100 − 72 = 28 chân.',
         'Đổi một con thì lệch bao nhiêu',
         'Đổi một con gà thành một con chó thì thêm 2 chân, vì chó 4 chân còn gà 2 chân.',
         'Chia ra',
         'Thiếu 28 chân, mỗi lần đổi được thêm 2 chân, nên phải đổi 28 : 2 = 14 con.',
         'Đáp số',
         'Có 14 con chó và 36 − 14 = 22 con gà. Thử lại: 14 × 4 = 56 chân chó, '
         '22 × 2 = 44 chân gà, cộng lại đúng 100 chân.'],
        ['Có bạn giả sử tất cả là gà, tính ra thiếu 28 chân, rồi trả lời luôn có 28 con chó.',
         'Gợi ý 1: Đổi một con gà thành chó thì thêm mấy chân?',
         'Gợi ý 2: Thêm 2 chân, chứ không phải 1. Vậy 28 chân thiếu ứng với mấy con?',
         'Chữa: 28 : 2 = 14 con chó. Lấy thẳng 28 là quên chia cho phần lệch mỗi lần đổi.'],
        ['Lấy que tính xếp thử: 36 con mà đều 2 chân thì được 72 que. Bảo con thêm que '
         'cho đủ 100 — con sẽ tự thấy mỗi con phải thêm 2 que.',
         'Chỗ sai duy nhất là quên chia. Bố mẹ hỏi: "Mỗi lần đổi một con thì lệch đi mấy?"'],
    ),
    [
        lt(1, 1, 'Vừa gà vừa chó có 36 con, 100 chân — đúng bài trong video. Giả sử tất '
                 'cả đều là gà thì có bao nhiêu chân?',
           '36 × 2 = 72 chân.'),
        lt(2, 1, 'Vẫn bài trên. So với đề, số chân đoán ra thiếu bao nhiêu?',
           '100 − 72 = 28 chân.'),
        lt(3, 1, 'Vẫn bài trên. Đổi một con gà thành chó thì thêm mấy chân?',
           'Thêm 2 chân, vì chó 4 chân còn gà 2 chân.'),
        lt(4, 2, 'Vẫn bài trên. Tính số con mỗi loại.',
           'Số chó: 28 : 2 = 14 con. Số gà: 36 − 14 = 22 con.'),
        lt(5, 2, 'Bạn Tú tính ra thiếu 28 chân rồi trả lời có 28 con chó. Bạn sai ở đâu?',
           'Bạn quên chia cho phần lệch mỗi lần đổi. Mỗi con đổi được thêm 2 chân nên '
           'số chó là 28 : 2 = 14 con.'),
        lt(6, 2, 'Vừa gà vừa chó có 20 con, 56 chân. Tính số con mỗi loại.',
           'Giả sử tất cả là gà: 20 × 2 = 40 chân, thiếu 56 − 40 = 16 chân. Số chó: '
           '16 : 2 = 8 con. Số gà: 20 − 8 = 12 con.'),
        lt(7, 2, 'Vì sao ta giả sử tất cả là GÀ mà không giả sử tất cả là CHÓ?',
           'Giả sử nào cũng được, chỉ khác là thừa hay thiếu. Giả sử tất cả là gà thì '
           'thiếu chân, giả sử tất cả là chó thì thừa chân — rồi vẫn chia cho 2.'),
        lt(8, 3, 'Bán 30 vé gồm loại 2 nghìn và loại 5 nghìn đồng, thu được 99 nghìn '
                 'đồng. Tính số vé mỗi loại.',
           'Giả sử tất cả là vé 2 nghìn: 30 × 2 = 60 nghìn, thiếu 99 − 60 = 39 nghìn. '
           'Mỗi vé đổi lên loại 5 nghìn thì thêm 3 nghìn. Số vé 5 nghìn: 39 : 3 = 13 vé. '
           'Số vé 2 nghìn: 30 − 13 = 17 vé.'),
        lt(9, 3, 'Vừa gà vừa chó có 36 con, 100 chân. Lần này con hãy giả sử tất cả là '
                 'CHÓ rồi giải lại.',
           'Giả sử tất cả là chó: 36 × 4 = 144 chân, THỪA 144 − 100 = 44 chân. Đổi một '
           'con chó thành gà thì bớt 2 chân, nên số gà là 44 : 2 = 22 con, số chó là '
           '36 − 22 = 14 con. Vẫn ra đúng kết quả cũ.'),
        q_tf(1, 'Giả thiết tạm là đoán bừa một trường hợp dễ tính rồi sửa dần.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Thiếu 28 chân thì có đúng 28 con chó.', False,
             'SAI — còn phải chia cho 2, vì mỗi lần đổi được thêm 2 chân.'),
        q_mcq(3, 'Giả sử 36 con đều là gà thì có:',
              ['A. 72 chân', 'B. 100 chân', 'C. 144 chân'], 'A. 72 chân', '36 × 2 = 72.'),
        q_mcq(4, 'Đổi một con gà thành một con chó thì số chân:',
              ['A. thêm 2', 'B. thêm 4', 'C. thêm 1'], 'A. thêm 2', '4 − 2 = 2.'),
        q_mcq(5, '36 con, 100 chân thì số chó là:',
              ['A. 14 con', 'B. 28 con', 'C. 22 con'], 'A. 14 con', '28 : 2 = 14.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑦ B36 · PHƯƠNG PHÁP KHỬ  (mã cũ, viết lại — chỉ còn KHỬ)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ gộp khử VỚI thế. Nay tách. Ý của khử rất gọn và rất đẹp: hai lần mua có một
# thứ GIỐNG HỆT nhau, nên trừ hai dữ kiện là thứ ấy biến mất.
B36 = bai(
    36, 'PHƯƠNG PHÁP KHỬ — TRỪ HAI LẦN MUA CHO MỘT THỨ BIẾN MẤT',
    'Dạng gốc: LV 8.3a mức Lớp 4 — Khử một đại lượng bằng cách trừ hai dữ kiện có '
    'phần giống nhau.',
    'Có bài cho con hai lần mua, mỗi lần gồm hai thứ. Nhìn thì rối, nhưng nếu để ý sẽ '
    'thấy một thứ xuất hiện y hệt ở cả hai lần. Trừ hai dòng cho nhau thì thứ ấy biến '
    'mất, và bài chỉ còn một ẩn.',
    LUI_THAY,
    video(
        ['Nhận ra phần giống hệt nhau ở hai dữ kiện.',
         'Trừ hai dòng để khử phần ấy đi.',
         'Tìm nốt thứ còn lại rồi quay về tìm thứ đã khử.'],
        ['Đề bài: Mua 3 bút và 2 vở hết 22 nghìn đồng. Mua 3 bút và 5 vở hết 37 nghìn '
         'đồng. Tính giá một bút và một vở.',
         'Viết hai dòng cho thẳng hàng',
         'Lần một: 3 bút và 2 vở hết 22 nghìn. Lần hai: 3 bút và 5 vở hết 37 nghìn.',
         'Tìm phần giống hệt',
         'Cả hai lần đều mua đúng 3 bút. Phần ấy giống hệt nhau.',
         'Trừ hai dòng',
         'Lấy dòng hai trừ dòng một thì 3 bút biến mất. Còn lại 5 − 2 = 3 vở, và tiền '
         'là 37 − 22 = 15 nghìn.',
         'Tìm giá một vở',
         '3 vở hết 15 nghìn nên một vở là 15 : 3 = 5 nghìn đồng.',
         'Quay về tìm giá bút',
         'Lần một: 2 vở hết 2 × 5 = 10 nghìn. Vậy 3 bút hết 22 − 10 = 12 nghìn, một bút '
         'là 12 : 3 = 4 nghìn đồng.',
         'Đáp số: một bút 4 nghìn, một vở 5 nghìn đồng.'],
        ['Có bạn trừ hai dòng nhưng chỉ trừ số vở mà quên trừ số tiền.',
         'Gợi ý 1: Nếu con bớt đi mấy quyển vở thì số tiền có bớt theo không?',
         'Gợi ý 2: Phải bớt theo chứ. Hai bên dấu bằng cùng bớt thì mới còn bằng nhau.',
         'Chữa: trừ thì trừ CẢ HAI VẾ. Còn 3 vở và 15 nghìn, chứ không phải 3 vở và 37 '
         'nghìn.'],
        ['Viết hai dòng ra giấy cho thẳng cột rồi bảo con khoanh phần giống nhau. '
         'Khoanh đúng thì phần còn lại rất nhanh.',
         'Chỗ sai hay gặp là trừ một vế. Bố mẹ nhắc: hai bên dấu bằng cùng bớt như nhau.'],
    ),
    [
        lt(1, 1, 'Mua 3 bút và 2 vở hết 22 nghìn; mua 3 bút và 5 vở hết 37 nghìn — đúng '
                 'bài trong video. Phần nào giống hệt ở cả hai lần mua?',
           'Cả hai lần đều mua đúng 3 bút.'),
        lt(2, 1, 'Vẫn bài trên. Trừ hai dòng cho nhau thì còn lại mấy quyển vở và bao '
                 'nhiêu tiền?',
           'Còn 5 − 2 = 3 vở và 37 − 22 = 15 nghìn đồng.'),
        lt(3, 1, 'Vẫn bài trên. Giá một quyển vở là bao nhiêu?',
           '15 : 3 = 5 nghìn đồng.'),
        lt(4, 2, 'Vẫn bài trên. Tính giá một cái bút.',
           '2 vở hết 2 × 5 = 10 nghìn. Vậy 3 bút hết 22 − 10 = 12 nghìn, một bút là '
           '12 : 3 = 4 nghìn đồng.'),
        lt(5, 2, 'Bạn Minh trừ số vở mà quên trừ số tiền. Bạn sai ở đâu?',
           'Trừ thì phải trừ CẢ HAI VẾ. Bớt vở thì tiền cũng bớt theo, nên còn 3 vở và '
           '15 nghìn.'),
        lt(6, 2, 'Mua 2 áo và 3 quần hết 62 nghìn; mua 2 áo và 5 quần hết 82 nghìn. '
                 'Tính giá một quần.',
           'Trừ hai dòng: còn 2 quần và 20 nghìn. Một quần là 20 : 2 = 10 nghìn đồng.'),
        lt(7, 2, 'Vẫn bài trên. Tính giá một cái áo.',
           '3 quần hết 3 × 10 = 30 nghìn. Vậy 2 áo hết 62 − 30 = 32 nghìn, một áo là '
           '32 : 2 = 16 nghìn đồng.'),
        lt(8, 3, 'Mua 4 bút và 3 vở hết 39 nghìn; mua 4 bút và 7 vở hết 59 nghìn. Tính '
                 'giá mỗi thứ.',
           'Trừ hai dòng: còn 4 vở và 20 nghìn, nên một vở là 5 nghìn. 3 vở hết 15 '
           'nghìn, 4 bút hết 39 − 15 = 24 nghìn, một bút là 6 nghìn đồng.'),
        lt(9, 3, 'Vì sao phương pháp khử chỉ dùng được khi hai lần mua có một thứ giống '
                 'HỆT nhau?',
           'Vì chỉ khi giống hệt thì trừ đi mới biến mất hoàn toàn. Nếu số lượng khác '
           'nhau thì trừ xong vẫn còn lại một phần, không khử được.'),
        q_tf(1, 'Khử là trừ hai dữ kiện để một thứ biến mất.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Khi trừ hai dòng, ta chỉ cần trừ số lượng, không trừ số tiền.', False,
             'SAI — phải trừ cả hai vế.'),
        q_mcq(3, '3 bút và 2 vở hết 22 nghìn; 3 bút và 5 vở hết 37 nghìn. Trừ hai dòng '
                 'còn lại:',
              ['A. 3 vở và 15 nghìn', 'B. 3 vở và 37 nghìn', 'C. 7 vở và 15 nghìn'],
              'A. 3 vở và 15 nghìn', 'Trừ cả hai vế.'),
        q_mcq(4, 'Giá một quyển vở là:',
              ['A. 5 nghìn', 'B. 3 nghìn', 'C. 15 nghìn'], 'A. 5 nghìn', '15 : 3 = 5.'),
        q_mcq(5, 'Phương pháp khử dùng được khi:',
              ['A. hai lần mua có một thứ giống HỆT nhau',
               'B. hai lần mua có tổng tiền bằng nhau',
               'C. lúc nào cũng dùng được'],
              'A. hai lần mua có một thứ giống HỆT nhau',
              'Giống hệt thì trừ đi mới biến mất hoàn toàn.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑧ B66 · PHƯƠNG PHÁP THẾ
# ═══════════════════════════════════════════════════════════════════════════
# Tách khỏi B36. Khác khử ở chỗ: khử cần hai thứ GIỐNG HỆT, còn thế cần một câu QUY
# ĐỔI ("2 cái này bằng 3 cái kia"). Dùng câu ấy đổi hết về một loại.
B66 = bai(
    66, 'PHƯƠNG PHÁP THẾ — ĐỔI HẾT VỀ MỘT LOẠI',
    'Dạng gốc: LV 8.3b mức Lớp 4 — Thế một đại lượng bằng đại lượng kia nhờ quan hệ '
    'quy đổi cho trước.',
    'Bài trước con khử được vì hai lần mua có một thứ giống hệt. Nhưng có bài không '
    'cho thế, mà cho một câu quy đổi kiểu "hai cái này bằng ba cái kia". Câu ấy cho '
    'phép con đổi hết về một loại, và bài rối thành bài dễ.',
    LUI_THAY,
    video(
        ['Đọc được câu quy đổi trong đề.',
         'Đổi hết mọi thứ về cùng một loại.',
         'Tìm ra giá một loại rồi quay về loại kia.'],
        ['Đề bài: Biết 2 hộp sữa giá bằng 3 gói bánh. Mua 4 hộp sữa và 6 gói bánh hết '
         '72 nghìn đồng. Tính giá mỗi thứ.',
         'Đọc câu quy đổi',
         'Đề nói 2 hộp sữa giá bằng 3 gói bánh. Đây là câu cho phép đổi qua đổi lại.',
         'Đổi sữa thành bánh',
         '4 hộp sữa gấp đôi 2 hộp sữa, nên nó bằng gấp đôi 3 gói bánh, tức 6 gói bánh.',
         'Bây giờ tất cả là bánh',
         'Cả lần mua thành 6 + 6 = 12 gói bánh, hết 72 nghìn đồng.',
         'Tìm giá một gói bánh',
         '72 : 12 = 6 nghìn đồng một gói bánh.',
         'Quay về tìm giá sữa',
         '2 hộp sữa bằng 3 gói bánh, tức 3 × 6 = 18 nghìn. Một hộp sữa là 18 : 2 = 9 '
         'nghìn đồng.',
         'Đáp số: một hộp sữa 9 nghìn, một gói bánh 6 nghìn đồng.'],
        ['Có bạn thấy "2 hộp sữa bằng 3 gói bánh" rồi đổi 4 hộp sữa thành 3 gói bánh.',
         'Gợi ý 1: 4 hộp sữa gấp mấy lần 2 hộp sữa?',
         'Gợi ý 2: Gấp đôi. Vậy phải đổi thành gấp đôi 3 gói bánh chứ.',
         'Chữa: 4 hộp sữa bằng 6 gói bánh. Đổi mà quên nhân lên thì mất một nửa số bánh.'],
        ['Bảo con đọc to câu quy đổi rồi hỏi: "Gấp đôi bên này thì bên kia thế nào?" '
         'Trả lời được là con nắm được cách thế.',
         'Chỗ sai duy nhất là quên nhân lên khi đổi. Bố mẹ hỏi: "Gấp mấy lần?"'],
    ),
    [
        lt(1, 1, '2 hộp sữa giá bằng 3 gói bánh — đúng đề trong video. Vậy 4 hộp sữa giá '
                 'bằng mấy gói bánh?',
           '4 hộp sữa gấp đôi 2 hộp sữa nên bằng gấp đôi 3 gói bánh, tức 6 gói bánh.'),
        lt(2, 1, 'Mua 4 hộp sữa và 6 gói bánh hết 72 nghìn. Đổi hết về bánh thì được mấy '
                 'gói bánh?',
           '4 hộp sữa bằng 6 gói bánh, cộng 6 gói bánh sẵn có, tất cả 12 gói bánh.'),
        lt(3, 1, 'Vẫn bài trên. Giá một gói bánh là bao nhiêu?',
           '72 : 12 = 6 nghìn đồng.'),
        lt(4, 2, 'Vẫn bài trên. Tính giá một hộp sữa.',
           '2 hộp sữa bằng 3 gói bánh, tức 3 × 6 = 18 nghìn. Một hộp sữa là 18 : 2 = 9 '
           'nghìn đồng.'),
        lt(5, 2, 'Bạn Hoa đổi 4 hộp sữa thành 3 gói bánh. Bạn sai ở đâu?',
           '4 hộp sữa gấp đôi 2 hộp sữa nên phải đổi thành gấp đôi 3 gói bánh, tức 6 '
           'gói bánh. Quên nhân lên thì mất một nửa.'),
        lt(6, 2, 'Biết 1 quyển vở giá bằng 2 cái bút. Mua 3 quyển vở và 4 cái bút hết 50 '
                 'nghìn. Tính giá một cái bút.',
           'Đổi vở thành bút: 3 vở bằng 6 bút. Tất cả 6 + 4 = 10 bút, hết 50 nghìn. Một '
           'bút là 50 : 10 = 5 nghìn đồng.'),
        lt(7, 2, 'Vẫn bài trên. Tính giá một quyển vở.',
           '1 vở bằng 2 bút, tức 2 × 5 = 10 nghìn đồng.'),
        lt(8, 3, 'Biết 3 cái ghế giá bằng 1 cái bàn. Mua 2 cái bàn và 3 cái ghế hết 180 '
                 'nghìn. Tính giá mỗi thứ.',
           'Đổi bàn thành ghế: 2 bàn bằng 6 ghế. Tất cả 6 + 3 = 9 ghế, hết 180 nghìn. '
           'Một ghế là 180 : 9 = 20 nghìn. Một bàn là 3 × 20 = 60 nghìn đồng.'),
        lt(9, 3, 'Phương pháp KHỬ và phương pháp THẾ khác nhau ở chỗ nào?',
           'Khử cần hai lần mua có một thứ GIỐNG HỆT để trừ đi. Thế cần một câu QUY ĐỔI '
           'để đưa hết về một loại. Hai cách dùng cho hai kiểu đề khác nhau.'),
        q_tf(1, 'Phương pháp thế dùng câu quy đổi để đưa hết về một loại.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Biết 2 hộp sữa bằng 3 gói bánh thì 4 hộp sữa bằng 3 gói bánh.', False,
             'SAI — gấp đôi bên này thì bên kia cũng gấp đôi, tức 6 gói bánh.'),
        q_mcq(3, '2 hộp sữa bằng 3 gói bánh thì 4 hộp sữa bằng:',
              ['A. 6 gói bánh', 'B. 3 gói bánh', 'C. 12 gói bánh'], 'A. 6 gói bánh',
              'Gấp đôi cả hai bên.'),
        q_mcq(4, '12 gói bánh hết 72 nghìn thì một gói bánh:',
              ['A. 6 nghìn', 'B. 12 nghìn', 'C. 9 nghìn'], 'A. 6 nghìn', '72 : 12 = 6.'),
        q_mcq(5, 'Phương pháp khử khác phương pháp thế ở chỗ:',
              ['A. khử cần hai thứ giống hệt, thế cần câu quy đổi',
               'B. khử dùng phép cộng, thế dùng phép trừ',
               'C. hai phương pháp giống hệt nhau'],
              'A. khử cần hai thứ giống hệt, thế cần câu quy đổi',
              'Hai cách cho hai kiểu đề khác nhau.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑨ B37 · SƠ ĐỒ VEN  (mã cũ, viết lại — chỉ còn VEN)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ gộp Ven VỚI nguyên lý chuồng thỏ — hai thứ chẳng liên quan gì nhau. Nay tách.
# Ý của Ven chỉ có một, và nó KHÔNG nói bằng lời được: phần giao bị đếm hai lần.
B37 = bai(
    37, 'SƠ ĐỒ VEN — PHẦN CHỒNG NHAU BỊ ĐẾM HAI LẦN',
    'Dạng gốc: LV 8.4a mức Lớp 4 — Sơ đồ Ven hai tập hợp, công thức A cộng B trừ phần '
    'chung.',
    'Có bài hỏi về hai nhóm mà một số bạn thuộc cả hai nhóm. Cộng thẳng hai nhóm lại '
    'là sai — và hôm nay con sẽ NHÌN THẤY vì sao sai, chứ không phải nghe kể.',
    LUI_VEN,
    video(
        ['Vẽ được hai vòng giao nhau cho hai nhóm.',
         'Chỉ ra phần chồng nhau bị đếm hai lần.',
         'Tính số bạn thuộc ít nhất một nhóm.'],
        ['Đề bài: Lớp có 38 bạn. Có 25 bạn thích bóng đá, 18 bạn thích cờ vua, 8 bạn '
         'thích cả hai môn. Hỏi có bao nhiêu bạn không thích môn nào?',
         'Cộng thẳng thì sai',
         '25 + 18 = 43, mà lớp chỉ có 38 bạn. Số bạn không thể nhiều hơn cả lớp.',
         'Vì sao lại thừa',
         'Vì 8 bạn thích cả hai môn đã bị đếm một lần ở nhóm bóng đá, rồi lại đếm thêm '
         'một lần ở nhóm cờ vua.',
         'Vẽ ra thì thấy ngay',
         'Hai vòng chồng nhau. Phần chồng chính là 8 bạn ấy, và nó nằm trong cả hai vòng.',
         'Trừ đi một lần',
         'Số bạn thích ít nhất một môn là 25 + 18 − 8 = 35 bạn.',
         'Tìm số bạn không thích môn nào',
         'Cả lớp 38 bạn, có 35 bạn thích ít nhất một môn, nên 38 − 35 = 3 bạn không '
         'thích môn nào.',
         'Đáp số: 3 bạn không thích môn nào.'],
        ['Có bạn cộng 25 với 18 được 43 rồi bảo lớp có 43 bạn thích ít nhất một môn.',
         'Gợi ý 1: Lớp có bao nhiêu bạn tất cả?',
         'Gợi ý 2: Chỉ 38 bạn. Sao số bạn thích lại nhiều hơn cả lớp được?',
         'Chữa: vì 8 bạn thích cả hai đã bị đếm hai lần. Phải trừ đi một lần: '
         '25 + 18 − 8 = 35 bạn.'],
        ['Vẽ hai vòng tròn chồng nhau rồi bảo con chỉ vào chỗ chồng và hỏi: "Chỗ này '
         'nằm trong mấy vòng?" Trả lời hai vòng là con hiểu vì sao phải trừ.',
         'Chỗ sai duy nhất là quên trừ phần chung. Bố mẹ hỏi: "Có ai bị đếm hai lần không?"'],
    ),
    [
        lt(1, 1, 'Lớp 38 bạn: 25 thích bóng đá, 18 thích cờ vua, 8 thích cả hai — đúng '
                 'bài trong video. Cộng thẳng 25 với 18 được bao nhiêu?',
           '25 + 18 = 43 bạn — nhiều hơn cả lớp, nên chắc chắn có chỗ sai.'),
        lt(2, 1, 'Vẫn bài trên. Vì sao cộng thẳng lại thừa?',
           'Vì 8 bạn thích cả hai môn bị đếm hai lần: một lần ở nhóm bóng đá, một lần ở '
           'nhóm cờ vua.'),
        lt(3, 1, 'Vẫn bài trên. Có bao nhiêu bạn thích ít nhất một môn?',
           '25 + 18 − 8 = 35 bạn.'),
        lt(4, 2, 'Vẫn bài trên. Có bao nhiêu bạn không thích môn nào?',
           '38 − 35 = 3 bạn.'),
        lt(5, 2, 'Bạn Nam cộng 25 với 18 rồi bảo có 43 bạn thích ít nhất một môn. Bạn '
                 'sai ở đâu?',
           'Lớp chỉ có 38 bạn nên không thể có 43 bạn thích. Bạn quên trừ 8 bạn bị đếm '
           'hai lần.'),
        lt(6, 2, 'Vẫn bài trên. Có bao nhiêu bạn CHỈ thích bóng đá?',
           '25 − 8 = 17 bạn.'),
        lt(7, 2, 'Lớp 40 bạn: 22 bạn học vẽ, 25 bạn học nhạc, 12 bạn học cả hai. Hỏi bao '
                 'nhiêu bạn học ít nhất một môn?',
           '22 + 25 − 12 = 35 bạn.'),
        lt(8, 3, 'Vẫn bài trên. Bao nhiêu bạn không học môn nào, và bao nhiêu bạn CHỈ '
                 'học nhạc?',
           'Không học môn nào: 40 − 35 = 5 bạn. Chỉ học nhạc: 25 − 12 = 13 bạn.'),
        lt(9, 3, 'Một nhóm 30 bạn: 20 bạn biết bơi, 15 bạn biết đi xe đạp, tất cả đều '
                 'biết ít nhất một trong hai. Hỏi bao nhiêu bạn biết cả hai?',
           'Nếu không ai bị đếm hai lần thì tổng là 20 + 15 = 35, mà chỉ có 30 bạn. '
           'Phần thừa 35 − 30 = 5 chính là số bạn biết cả hai.'),
        q_tf(1, 'Phần chồng nhau trên sơ đồ Ven bị đếm hai lần.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Muốn biết số bạn thích ít nhất một môn, ta cộng thẳng hai nhóm.', False,
             'SAI — phải trừ đi phần chung một lần.'),
        q_mcq(3, 'Lớp 38 bạn, 25 thích bóng đá, 18 thích cờ vua, 8 thích cả hai. Số bạn '
                 'thích ít nhất một môn là:',
              ['A. 35', 'B. 43', 'C. 38'], 'A. 35', '25 + 18 − 8 = 35.'),
        q_mcq(4, 'Số bạn CHỈ thích bóng đá là:',
              ['A. 17', 'B. 25', 'C. 8'], 'A. 17', '25 − 8 = 17.'),
        q_mcq(5, 'Vì sao phải trừ phần chung đi một lần?',
              ['A. Vì phần ấy đã bị đếm ở cả hai nhóm',
               'B. Vì phần ấy không thuộc nhóm nào',
               'C. Vì phần ấy luôn nhỏ nhất'],
              'A. Vì phần ấy đã bị đếm ở cả hai nhóm', 'Đếm hai lần thì thừa một lần.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑩ B67 · NGUYÊN LÝ CHUỒNG THỎ
# ═══════════════════════════════════════════════════════════════════════════
# Tách hẳn khỏi B37 — nó chẳng liên quan gì tới sơ đồ Ven. Đây là bài KẾT chương, và
# là bài lạ nhất: nó không tính ra con số, nó CHỨNG MINH rằng một điều phải xảy ra.
B67 = bai(
    67, 'NGUYÊN LÝ CHUỒNG THỎ — NHIỀU HƠN CHỖ THÌ PHẢI CÓ CHỖ CHỨA HAI',
    'Dạng gốc: LV 8.4b mức Lớp 4 — Nguyên lý Dirichlet phát biểu đơn giản: nhiều đồ '
    'hơn số chỗ thì có chỗ chứa từ hai đồ trở lên.',
    'Bài cuối chương, và là bài lạ nhất con từng gặp: nó không bắt con tính ra con số '
    'nào cả. Nó bắt con CHỨNG MINH rằng một điều chắc chắn phải xảy ra — dù con không '
    'biết cụ thể xảy ra ở đâu.',
    LUI_VEN,
    video(
        ['Phát biểu được nguyên lý: nhiều đồ hơn chỗ thì có chỗ chứa từ hai trở lên.',
         'Xác định đâu là "đồ" và đâu là "chỗ" trong một bài toán.',
         'Trả lời được câu hỏi kiểu "chắc chắn có ít nhất mấy bạn".'],
        ['Đề bài: Một nhóm có 13 bạn. Chứng tỏ rằng chắc chắn có ít nhất 2 bạn sinh cùng '
         'một tháng.',
         'Đếm số CHỖ',
         'Một năm có 12 tháng. Vậy có 12 chỗ để xếp.',
         'Đếm số ĐỒ',
         'Có 13 bạn, tức 13 đồ cần xếp vào 12 chỗ.',
         'Thử xếp mỗi chỗ một bạn',
         'Xếp 12 bạn vào 12 tháng, mỗi tháng một bạn. Vẫn còn thừa 1 bạn.',
         'Bạn thừa phải vào đâu',
         'Bạn ấy vẫn sinh vào một tháng nào đó, mà 12 tháng đều đã có người. Nên chắc '
         'chắn có một tháng chứa 2 bạn.',
         'Điều hay của bài này',
         'Ta không biết đó là tháng nào, nhưng chắc chắn có. Đó là điều bài toán hỏi.',
         'Đáp số: chắc chắn có ít nhất 2 bạn sinh cùng tháng.'],
        ['Có bạn nói: "Không chắc đâu, biết đâu 13 bạn sinh 13 tháng khác nhau."',
         'Gợi ý 1: Một năm có mấy tháng?',
         'Gợi ý 2: Chỉ 12 tháng thôi. Làm gì có tháng thứ 13 để xếp bạn thứ 13.',
         'Chữa: chỉ có 12 tháng nên không thể có 13 tháng khác nhau. Bạn thứ 13 buộc '
         'phải trùng tháng với một bạn nào đó.'],
        ['Lấy 13 hạt đậu và một khay 12 ô, bảo con xếp mỗi ô một hạt. Con sẽ thấy hạt '
         'cuối không còn ô trống nào.',
         'Bài này lạ vì không ra con số cụ thể. Bố mẹ nhấn: ta chứng minh điều đó PHẢI '
         'xảy ra, chứ không tìm xem xảy ra ở đâu.'],
    ),
    [
        lt(1, 1, 'Nhóm 13 bạn — đúng bài trong video. Một năm có bao nhiêu tháng, tức '
                 'bao nhiêu chỗ để xếp?',
           'Một năm có 12 tháng, tức 12 chỗ.'),
        lt(2, 1, 'Vẫn bài trên. Xếp mỗi tháng một bạn thì xếp được mấy bạn và còn thừa '
                 'mấy bạn?',
           'Xếp được 12 bạn, còn thừa 13 − 12 = 1 bạn.'),
        lt(3, 1, 'Vẫn bài trên. Bạn thừa ấy buộc phải trùng tháng với một bạn khác, vậy '
                 'có ít nhất mấy bạn sinh cùng tháng?',
           'Ít nhất 2 bạn.'),
        lt(4, 2, 'Bạn An nói "biết đâu 13 bạn sinh 13 tháng khác nhau". Bạn sai ở đâu?',
           'Một năm chỉ có 12 tháng, làm gì có tháng thứ 13. Nên không thể có 13 tháng '
           'khác nhau.'),
        lt(5, 2, 'Một hộp có bi xanh và bi đỏ. Lấy ra 3 viên bất kỳ. Chứng tỏ chắc chắn '
                 'có ít nhất 2 viên cùng màu.',
           'Có 2 chỗ (hai màu) và 3 viên. Xếp mỗi màu một viên thì còn thừa 1 viên, viên '
           'ấy buộc phải trùng màu. Vậy ít nhất 2 viên cùng màu.'),
        lt(6, 2, 'Trong một lớp có 8 bạn. Chứng tỏ chắc chắn có ít nhất 2 bạn sinh cùng '
                 'một ngày trong tuần.',
           'Một tuần có 7 ngày, tức 7 chỗ, mà có 8 bạn. Thừa 1 bạn nên chắc chắn có 2 '
           'bạn trùng ngày.'),
        lt(7, 2, 'Muốn chắc chắn có 2 bạn sinh cùng tháng thì nhóm phải có ít nhất bao '
                 'nhiêu bạn?',
           'Ít nhất 13 bạn. Với 12 bạn thì có thể mỗi bạn một tháng khác nhau.'),
        lt(8, 3, 'Một hộp có bi ba màu. Phải lấy ra ít nhất mấy viên để chắc chắn có 2 '
                 'viên cùng màu?',
           'Có 3 chỗ (ba màu). Lấy 3 viên thì có thể mỗi viên một màu. Lấy 4 viên thì '
           'chắc chắn có 2 viên cùng màu.'),
        lt(9, 3, 'Một nhóm 25 bạn. Chứng tỏ chắc chắn có ít nhất 3 bạn sinh cùng một '
                 'tháng.',
           'Nếu mỗi tháng chỉ có nhiều nhất 2 bạn thì cả năm nhiều nhất 12 × 2 = 24 bạn. '
           'Mà nhóm có 25 bạn, nhiều hơn 24, nên chắc chắn có một tháng chứa từ 3 bạn '
           'trở lên.'),
        q_tf(1, 'Có 13 bạn thì chắc chắn có ít nhất 2 bạn sinh cùng tháng.', True,
             'Đáp án: ĐÚNG — chỉ có 12 tháng.'),
        q_tf(2, 'Bài này cho ta biết chính xác tháng nào có 2 bạn.', False,
             'SAI — ta chỉ biết chắc chắn CÓ, không biết là tháng nào.'),
        q_mcq(3, 'Một năm có 12 tháng. Muốn chắc chắn 2 bạn cùng tháng cần ít nhất:',
              ['A. 13 bạn', 'B. 12 bạn', 'C. 24 bạn'], 'A. 13 bạn',
              'Với 12 bạn thì có thể mỗi bạn một tháng.'),
        q_mcq(4, 'Hộp có bi hai màu, lấy 3 viên thì:',
              ['A. chắc chắn có 2 viên cùng màu', 'B. chắc chắn ba viên khác màu',
               'C. không kết luận được'],
              'A. chắc chắn có 2 viên cùng màu', 'Chỉ có 2 màu mà lấy 3 viên.'),
        q_mcq(5, 'Nguyên lý này cho ta biết:',
              ['A. điều đó chắc chắn xảy ra, nhưng không biết ở đâu',
               'B. chính xác nơi điều đó xảy ra',
               'C. xác suất điều đó xảy ra'],
              'A. điều đó chắc chắn xảy ra, nhưng không biết ở đâu',
              'Đó là điều hay của nguyên lý này.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
MOI = [B32, B64, B33, B65, B34, B35, B36, B66, B37, B67]
SAU = {'DL:KSN4.B64': 'DL:KSN4.B32', 'DL:KSN4.B65': 'DL:KSN4.B33',
       'DL:KSN4.B66': 'DL:KSN4.B36', 'DL:KSN4.B67': 'DL:KSN4.B37'}   # chèn ngay sau ai

O_NHAP_MOI = {
    'DL:KSN4.B32#C1': {'parts': [{'label': 'đề cho', 'options': ['tổng và hiệu',
                                  'tổng và tỉ số'], 'value': 'tổng và hiệu'}]},
    'DL:KSN4.B32#C2': {'value': 30},
    'DL:KSN4.B32#C3': {'value': 6},
    'DL:KSN4.B32#C4': {'parts': [{'label': 'tuổi em', 'value': 10},
                                 {'label': 'tuổi anh', 'value': 20}]},
    'DL:KSN4.B32#C5': {'parts': [{'label': 'bài toán tuổi một mốc là dạng',
                                  'options': ['bài cũ mặc áo mới', 'dạng hoàn toàn mới'],
                                  'value': 'bài cũ mặc áo mới'}]},
    'DL:KSN4.B32#C6': {'parts': [{'label': 'tuổi bố', 'value': 36},
                                 {'label': 'tuổi con', 'value': 8}]},
    'DL:KSN4.B32#C7': {'parts': [{'label': 'tuổi anh', 'value': 15},
                                 {'label': 'tuổi em', 'value': 11}]},
    'DL:KSN4.B32#C8': {'parts': [{'label': 'tuổi con', 'value': 6},
                                 {'label': 'tuổi mẹ', 'value': 30}]},
    'DL:KSN4.B32#C9': {'parts': [{'label': 'tuổi con', 'value': 6},
                                 {'label': 'tuổi mẹ', 'value': 30}]},

    'DL:KSN4.B64#C1': {'value': 24},
    'DL:KSN4.B64#C2': {'value': 24},
    'DL:KSN4.B64#C3': {'value': 2},
    'DL:KSN4.B64#C4': {'parts': [{'label': 'tuổi con', 'value': 12},
                                 {'label': 'tuổi mẹ', 'value': 36}]},
    'DL:KSN4.B64#C5': {'value': 6},
    'DL:KSN4.B64#C6': {'parts': [{'label': 'hiệu tuổi có đổi không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B64#C7': {'parts': [{'label': 'tuổi em', 'value': 4},
                                 {'label': 'tuổi anh', 'value': 12}]},
    'DL:KSN4.B64#C8': {'parts': [{'label': 'tuổi con lúc ấy', 'value': 30},
                                 {'label': 'sau mấy năm', 'value': 20}]},
    'DL:KSN4.B64#C9': {'value': 5},

    'DL:KSN4.B33#C1': {'value': 12},
    'DL:KSN4.B33#C2': {'parts': [{'label': 'anh mấy phần', 'value': 2},
                                 {'label': 'em mấy phần', 'value': 1}]},
    'DL:KSN4.B33#C3': {'value': 4},
    'DL:KSN4.B33#C4': {'parts': [{'label': 'làm chung phải nhanh hơn mấy giờ', 'value': 6}]},
    'DL:KSN4.B33#C5': {'value': 3},
    'DL:KSN4.B33#C6': {'parts': [{'label': 'vì 12 chia hết cho cả 6 và', 'value': 12}]},
    'DL:KSN4.B33#C7': {'value': 1},
    'DL:KSN4.B33#C8': {'value': 6},
    'DL:KSN4.B33#C9': {'value': 2},

    'DL:KSN4.B65#C1': {'value': 3},
    'DL:KSN4.B65#C2': {'value': 6},
    'DL:KSN4.B65#C3': {'value': 6},
    'DL:KSN4.B65#C4': {'value': 6},
    'DL:KSN4.B65#C5': {'parts': [{'label': 'phải chia cho mấy phần mỗi giờ', 'value': 1},
                                 {'label': 'đáp số đúng mấy giờ', 'value': 6}]},
    'DL:KSN4.B65#C6': {'value': 8},
    'DL:KSN4.B65#C7': {'parts': [{'label': 'bớt một người thì tốc độ',
                                  'options': ['giảm', 'tăng', 'không đổi'],
                                  'value': 'giảm'}]},
    'DL:KSN4.B65#C8': {'parts': [{'label': 'còn mấy phần', 'value': 6},
                                 {'label': 'anh làm thêm mấy giờ', 'value': 6}]},
    'DL:KSN4.B65#C9': {'value': 3},

    'DL:KSN4.B34#C1': {'value': 30},
    'DL:KSN4.B34#C2': {'value': 20},
    'DL:KSN4.B34#C3': {'value': 10},
    'DL:KSN4.B34#C4': {'value': 26},
    'DL:KSN4.B34#C5': {'parts': [{'label': 'phải đổi trừ thành',
                                  'options': ['cộng', 'nhân', 'chia'], 'value': 'cộng'},
                                 {'label': 'kết quả đúng', 'value': 30}]},
    'DL:KSN4.B34#C6': {'value': 5},
    'DL:KSN4.B34#C7': {'parts': [{'label': 'đi lùi của chia là',
                                  'options': ['nhân', 'cộng', 'trừ'], 'value': 'nhân'}]},
    'DL:KSN4.B34#C8': {'value': 10},
    'DL:KSN4.B34#C9': {'value': 12},

    # ── ⑥ B35 · giả thiết tạm ──
    'DL:KSN4.B35#C1': {'value': 72},
    'DL:KSN4.B35#C2': {'value': 28},
    'DL:KSN4.B35#C3': {'value': 2},
    'DL:KSN4.B35#C4': {'parts': [{'label': 'số chó', 'value': 14},
                                 {'label': 'số gà', 'value': 22}]},
    'DL:KSN4.B35#C5': {'parts': [{'label': 'phải chia cho', 'value': 2},
                                 {'label': 'số chó đúng', 'value': 14}]},
    'DL:KSN4.B35#C6': {'parts': [{'label': 'số chó', 'value': 8},
                                 {'label': 'số gà', 'value': 12}]},
    'DL:KSN4.B35#C7': {'parts': [{'label': 'giả sử toàn chó thì chân sẽ',
                                  'options': ['thừa', 'thiếu'], 'value': 'thừa'}]},
    'DL:KSN4.B35#C8': {'parts': [{'label': 'vé 5 nghìn', 'value': 13},
                                 {'label': 'vé 2 nghìn', 'value': 17}]},
    'DL:KSN4.B35#C9': {'parts': [{'label': 'số gà', 'value': 22},
                                 {'label': 'số chó', 'value': 14}]},

    # ── ⑦ B36 · khử ──
    'DL:KSN4.B36#C1': {'value': 3},
    'DL:KSN4.B36#C2': {'parts': [{'label': 'còn mấy vở', 'value': 3},
                                 {'label': 'còn bao nhiêu nghìn', 'value': 15}]},
    'DL:KSN4.B36#C3': {'value': 5},
    'DL:KSN4.B36#C4': {'value': 4},
    'DL:KSN4.B36#C5': {'parts': [{'label': 'phải trừ mấy vế', 'value': 2},
                                 {'label': 'còn bao nhiêu nghìn', 'value': 15}]},
    'DL:KSN4.B36#C6': {'value': 10},
    'DL:KSN4.B36#C7': {'value': 16},
    'DL:KSN4.B36#C8': {'parts': [{'label': 'một vở', 'value': 5},
                                 {'label': 'một bút', 'value': 6}]},
    'DL:KSN4.B36#C9': {'parts': [{'label': 'hai lần mua phải có một thứ',
                                  'options': ['giống hệt', 'khác nhau'],
                                  'value': 'giống hệt'}]},

    # ── ⑧ B66 · thế ──
    'DL:KSN4.B66#C1': {'value': 6},
    'DL:KSN4.B66#C2': {'value': 12},
    'DL:KSN4.B66#C3': {'value': 6},
    'DL:KSN4.B66#C4': {'value': 9},
    'DL:KSN4.B66#C5': {'parts': [{'label': '4 hộp sữa bằng mấy gói bánh', 'value': 6}]},
    'DL:KSN4.B66#C6': {'value': 5},
    'DL:KSN4.B66#C7': {'value': 10},
    'DL:KSN4.B66#C8': {'parts': [{'label': 'một ghế', 'value': 20},
                                 {'label': 'một bàn', 'value': 60}]},
    'DL:KSN4.B66#C9': {'parts': [{'label': 'khử cần hai thứ',
                                  'options': ['giống hệt', 'quy đổi'],
                                  'value': 'giống hệt'},
                                 {'label': 'thế cần câu',
                                  'options': ['quy đổi', 'giống hệt'],
                                  'value': 'quy đổi'}]},

    # ── ⑨ B37 · sơ đồ Ven ──
    'DL:KSN4.B37#C1': {'value': 43},
    'DL:KSN4.B37#C2': {'parts': [{'label': 'số bạn bị đếm hai lần', 'value': 8}]},
    'DL:KSN4.B37#C3': {'value': 35},
    'DL:KSN4.B37#C4': {'value': 3},
    'DL:KSN4.B37#C5': {'parts': [{'label': 'phải trừ đi mấy bạn', 'value': 8},
                                 {'label': 'kết quả đúng', 'value': 35}]},
    'DL:KSN4.B37#C6': {'value': 17},
    'DL:KSN4.B37#C7': {'value': 35},
    'DL:KSN4.B37#C8': {'parts': [{'label': 'không học môn nào', 'value': 5},
                                 {'label': 'chỉ học nhạc', 'value': 13}]},
    'DL:KSN4.B37#C9': {'value': 5},

    # ── ⑩ B67 · nguyên lý chuồng thỏ ──
    'DL:KSN4.B67#C1': {'value': 12},
    'DL:KSN4.B67#C2': {'parts': [{'label': 'xếp được mấy bạn', 'value': 12},
                                 {'label': 'thừa mấy bạn', 'value': 1}]},
    'DL:KSN4.B67#C3': {'value': 2},
    'DL:KSN4.B67#C4': {'parts': [{'label': 'một năm có mấy tháng', 'value': 12}]},
    'DL:KSN4.B67#C5': {'value': 2},
    'DL:KSN4.B67#C6': {'value': 2},
    'DL:KSN4.B67#C7': {'value': 13},
    'DL:KSN4.B67#C8': {'value': 4},
    'DL:KSN4.B67#C9': {'parts': [{'label': 'mỗi tháng nhiều nhất 2 bạn thì cả năm',
                                  'value': 24},
                                 {'label': 'nên chắc chắn có tháng chứa từ mấy bạn',
                                  'value': 3}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN4.B{n}' for n in (32, 33, 34, 35, 36, 37)}
    moi_ = {f'DL:KSN4.B{n}' for n in (64, 65, 66, 67)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')
    # Neo THEO CẶP — chương này không có một bộ neo chung, xem chú thích đầu tệp.
    CAP = [({'DL:KSN4.B32', 'DL:KSN4.B64'}, ('30 tuổi', 'mẹ 30', '24 tuổi')),
           ({'DL:KSN4.B33', 'DL:KSN4.B65'}, ('12 phần', '6 giờ')),
           ({'DL:KSN4.B34'}, ('26', '10')),
           ({'DL:KSN4.B35'}, ('36 con', '100')),
           ({'DL:KSN4.B36', 'DL:KSN4.B66'}, ('bút', 'vở', 'hộp sữa', 'gói bánh')),
           ({'DL:KSN4.B37', 'DL:KSN4.B67'}, ('38 bạn', '13 bạn', '12 tháng'))]
    for ma, neo in CAP:
        for b in MOI:
            if b['id'] in ma:
                van = json.dumps(b, ensure_ascii=False)
                if not any(x in van for x in neo):
                    loi.append(f'{b["id"]}: thiếu bộ neo {neo} của cặp bài')
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

    # Chèn hai bài MỚI vào ngay sau bài chúng nối tiếp — ba mã cũ đã nằm đúng chỗ.
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
