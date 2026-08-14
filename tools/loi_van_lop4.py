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
MOI = [B32, B64, B33, B65, B34]
SAU = {'DL:KSN4.B64': 'DL:KSN4.B32', 'DL:KSN4.B65': 'DL:KSN4.B33'}   # chèn ngay sau ai

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
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {'DL:KSN4.B32', 'DL:KSN4.B33', 'DL:KSN4.B34'}
    moi_ = {'DL:KSN4.B64', 'DL:KSN4.B65'}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')
    # Neo THEO CẶP — chương này không có một bộ neo chung, xem chú thích đầu tệp.
    CAP = [({'DL:KSN4.B32', 'DL:KSN4.B64'}, ('30 tuổi', 'mẹ 30', '24 tuổi')),
           ({'DL:KSN4.B33', 'DL:KSN4.B65'}, ('12 phần', '6 giờ')),
           ({'DL:KSN4.B34'}, ('26', '10'))]
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
