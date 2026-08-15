# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 5 · CHUYỆN TOÁN LỜI VĂN — sáu bài chữ thành mười hai bài video.

Chương dài nhất của quyển, và bài nào cũng gộp đúng HAI nghề ngược chiều nhau —
nên đợt này tách đôi đều tăm tắp, không bài nào tách ba.

  · B16 gộp "chia đều tìm mỗi phần" với bài NGƯỢC "biết mỗi phần tìm tất cả";
  · B17 gộp "vẽ sơ đồ hai đoạn thẳng" với "bẫy câu chữ đảo" — cái sau là chỗ sách
    tự nêu ra là bẫy, mà lại nằm chung bài với cái trước;
  · B18 gộp "liệt kê có thứ tự" với "dò cột hơn nhau rồi thử lại đủ hai điều kiện";
  · B19 gộp "vẽ theo phần" với "chia tổng cho số phần rồi trả về từng người";
  · B20 gộp "tính tuổi sau mấy năm" với khám phá "hiệu tuổi không bao giờ đổi";
  · B21 gộp "biết mỗi giờ hỏi tất cả" với bài ngược "biết tất cả hỏi mỗi giờ".

── SỐ NEO ──
    15 vở : 5 bạn        → mỗi bạn 3 quyển, khuôn ba dòng
    4 cái × 3 bạn        → khay có 12 cái
    Hoa 14, Lan ít hơn 5 → Lan 9 con hạc
    An 8, An ít hơn Bình 3 → Bình 11 viên, vì BÌNH mới là người nhiều hơn
    tách 12              → 11-1, 10-2, 9-3, 8-4, 7-5, 6-6
    tổng 12, hơn nhau 4  → 8 và 4, thử lại ĐỦ HAI điều kiện
    bố gấp 3 lần con     → 1 + 3 = 4 phần bằng nhau
    12 : 4 = 3           → con 3 quả, bố 9 quả
    mẹ 32, con 7         → hơn 25 tuổi; sau 5 năm là 37 và 12
    anh hơn em 3 tuổi    → mãi mãi vẫn 3
    3 lít × 4 phút       → 12 lít
    15 áo : 3 giờ        → mỗi giờ 5 cái

    python3 tools/loi_van_lop2.py --xem
    python3 tools/loi_van_lop2.py
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

TEN_CHUONG = 'Chuyện toán lời văn'
CHUONG = 5
CO_KHONG = ['có', 'không']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng video: hai mục mở bài và khám phá để RỖNG, video thay cả hai."""
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)


# ═══ ① B16 · CHIA ĐỀU ═══
B16 = bai(
    16, 'CHIA ĐỀU — PHÉP CHIA VÀ KHUÔN BA DÒNG',
    'LV 1.1a — Bài toán chia đều, và cách trình bày bài giải ba dòng.',
    video(
        ['Nhận ra bài chia đều thì dùng phép chia.',
         'Trình bày bài giải đủ ba dòng: lời giải, phép tính, đáp số.',
         'Thử lại kết quả bằng phép nhân.'],
        ['Đề bài: Cô giáo có 15 quyển vở thưởng đều cho 5 bạn. Hỏi mỗi bạn được mấy '
         'quyển vở?',
         'Đọc chậm xem đề cho gì, hỏi gì',
         'Đề cho 15 quyển vở, 5 bạn, và chia đều. Đề hỏi mỗi bạn được mấy quyển.',
         'Chia đều thành các phần bằng nhau là việc của phép chia',
         'Lấy 15 : 5 = 3.',
         'Trình bày đủ ba dòng',
         'Dòng một là lời giải, dòng hai là phép tính kèm đơn vị, dòng ba là đáp số.',
         'Đáp số: 3 quyển vở.',
         'Thử lại bằng phép nhân: 3 × 5 = 15, khớp đúng số vở của cô.'],
        ['Có bạn giải bài 12 cái bánh chia cho 3 bạn bằng phép trừ, lấy 12 − 3 rồi ghi '
         'mỗi bạn 9 cái.',
         'Gợi ý 1: Thử lại xem, mỗi bạn 9 cái mà có 3 bạn thì hết bao nhiêu cái?',
         'Gợi ý 2: Hết những hai mươi bảy cái, mà khay chỉ có mười hai. Bánh ở đâu ra '
         'nhiều thế?',
         'Chữa: chia đều là việc của phép chia, nên lấy 12 : 3 = 4. Mỗi bạn 4 cái.'],
        ['Chia hoa quả trong bữa cơm rồi hỏi con mỗi người mấy quả — bài toán chia đều '
         'có sẵn ngay trên bàn ăn.',
         'Bố mẹ hỏi một câu: "Con dùng phép gì, và vì sao?"'],
    ),
    [
        lt(1, 1, 'Tính 15 : 5.', 'Lấy 15 : 5 = 3.'),
        lt(2, 1, 'Có 12 cái bánh chia đều cho 3 bạn. Mỗi bạn được mấy cái?',
           'Chia đều là việc của phép chia: 12 : 3 = 4.'),
        lt(3, 1, 'Có 20 quyển vở chia đều cho 4 bạn. Mỗi bạn được mấy quyển?',
           'Lấy 20 : 4 = 5.'),
        lt(4, 2, 'Bài giải chuẩn gồm mấy dòng, và dòng thứ ba là dòng gì?',
           'Bài giải có 3 dòng: lời giải, phép tính, rồi đáp số.'),
        lt(5, 2, 'Có 18 quả cam chia đều cho 6 bạn. Mỗi bạn được mấy quả?',
           'Lấy 18 : 6 = 3.'),
        lt(6, 2, 'Chia 12 cái bánh cho 3 bạn mà làm phép trừ thì sai ở đâu?',
           'Chia đều là việc của phép chia, không phải phép trừ.'),
        lt(7, 3, 'Có 24 viên kẹo chia đều cho 4 bạn. Mỗi bạn mấy viên, và thử lại bằng '
                 'phép nhân được bao nhiêu?',
           'Lấy 24 : 4 = 6. Thử lại: 6 × 4 = 24, khớp đúng đề bài.'),
        lt(8, 3, 'Có 30 quyển vở. Chia đều cho 5 bạn thì mỗi bạn mấy quyển, chia đều '
                 'cho 6 bạn thì mỗi bạn mấy quyển, và ít hơn mấy quyển?',
           'Chia 5 bạn: 30 : 5 = 6 quyển. Chia 6 bạn: 30 : 6 = 5 quyển. Ít hơn 1 '
           'quyển.'),
    ] + [
        q_tf(1, 'Chia đều thành các phần bằng nhau là việc của phép chia.', True,
             'Đúng — đó là dấu hiệu để chọn phép tính.'),
        q_mcq(2, 'Có 15 quyển vở chia đều cho 5 bạn. Mỗi bạn mấy quyển?',
              ['3', '10', '20', '5'], '3', 'Lấy mười lăm chia năm.'),
        q_tf(3, 'Bài giải chuẩn có ba dòng: lời giải, phép tính, đáp số.', True,
             'Đúng — cả chương đều trình bày như thế.'),
        q_mcq(4, 'Chia 12 cái bánh cho 3 bạn thì dùng phép gì?',
              ['phép chia', 'phép trừ', 'phép cộng'], 'phép chia',
              'Chia đều ra từng phần thì dùng phép chia.'),
        q_tf(5, 'Dòng phép tính không cần ghi đơn vị.', False,
             'Sai. Dòng phép tính phải ghi đơn vị trong ngoặc.'),
    ],
)

# ═══ ② B54 · BÀI NGƯỢC — BIẾT MỖI PHẦN, TÌM TẤT CẢ ═══
B54 = bai(
    54, 'BÀI NGƯỢC — BIẾT MỖI PHẦN, TÌM TẤT CẢ',
    'LV 1.1b — Bài toán ngược của chia đều: gộp các phần bằng nhau.',
    video(
        ['Nhận ra bài ngược của bài chia đều.',
         'Gộp các phần bằng nhau bằng phép nhân.',
         'Thử lại bằng phép chia.'],
        ['Đề bài: Mỗi bạn được 4 cái bánh, có 3 bạn. Hỏi khay có tất cả bao nhiêu cái '
         'bánh?',
         'Bài này ngược với bài trước',
         'Bài trước biết tất cả rồi hỏi mỗi phần. Bài này biết mỗi phần rồi hỏi tất '
         'cả.',
         'Gộp các phần bằng nhau là việc của phép nhân',
         'Lấy 4 × 3 = 12.',
         'Thử lại bằng phép chia',
         'Chia ngược lại: 12 : 3 = 4, đúng bằng phần của mỗi bạn.',
         'Đáp số: 12 cái bánh.',
         'Nhân và chia là đôi máy ngược chiều, y như đã học ở bài tìm ô trống.'],
        ['Có bạn thấy đề nói "mỗi bạn 4 cái, có 3 bạn" rồi cộng luôn 4 với 3 được 7 '
         'cái.',
         'Gợi ý 1: Bốn là số bánh của MỘT bạn, còn ba là số BẠN. Hai thứ ấy khác loại '
         'nhau.',
         'Gợi ý 2: Vẽ ba khay, mỗi khay bốn cái rồi đếm xem được bao nhiêu.',
         'Chữa: gộp ba phần bằng nhau, mỗi phần 4 cái, là việc của phép nhân: '
         '4 × 3 = 12.'],
        ['Xếp bát đũa cho cả nhà rồi hỏi con cần tất cả bao nhiêu cái — bài ngược này '
         'gặp mỗi bữa cơm.',
         'Bố mẹ hỏi: "Đề cho con biết MỖI phần hay biết TẤT CẢ?"'],
    ),
    [
        lt(1, 1, 'Tính 4 × 3.', 'Lấy 4 × 3 = 12.'),
        lt(2, 1, 'Mỗi bạn được 4 cái bánh, có 3 bạn. Khay có tất cả mấy cái?',
           'Gộp các phần bằng nhau: 4 × 3 = 12.'),
        lt(3, 1, 'Mỗi hộp có 5 chiếc bút, có 4 hộp. Tất cả có mấy chiếc bút?',
           'Lấy 5 × 4 = 20.'),
        lt(4, 2, 'Biết mỗi phần rồi hỏi tất cả thì dùng phép gì?',
           'Gộp các phần bằng nhau lại là việc của phép nhân.'),
        lt(5, 2, 'Mỗi bạn được 6 viên kẹo, có 5 bạn. Tất cả có mấy viên?',
           'Lấy 6 × 5 = 30.'),
        lt(6, 2, 'Mỗi rổ có 7 quả trứng, có 3 rổ. Tất cả mấy quả, và thử lại bằng phép '
                 'chia được bao nhiêu?',
           'Lấy 7 × 3 = 21. Thử lại: 21 : 3 = 7, đúng phần mỗi rổ.'),
        lt(7, 3, 'Mỗi bạn được 4 quyển vở, có 6 bạn. Nếu thêm 2 bạn nữa thì có mấy bạn '
                 'và cần tất cả bao nhiêu quyển?',
           'Thêm hai bạn thành 8 bạn. Cần 4 × 8 = 32 quyển.'),
        lt(8, 3, 'Một khay 24 cái bánh chia đều cho 4 bạn. Cho biết lúc đầu mỗi bạn '
                 'mấy cái, và nếu mỗi bạn được thêm 1 cái thì khay phải có mấy cái?',
           'Lúc đầu 24 : 4 = 6 cái mỗi bạn. Thêm một cái thành 7 cái, nên khay phải có '
           '7 × 4 = 28 cái.'),
    ] + [
        q_tf(1, 'Biết mỗi phần rồi hỏi tất cả thì dùng phép nhân.', True,
             'Đúng — gộp các phần bằng nhau là việc của phép nhân.'),
        q_mcq(2, 'Mỗi bạn 4 cái bánh, có 3 bạn. Tất cả mấy cái?',
              ['12', '7', '1', '9'], '12', 'Ba phần, mỗi phần bốn cái.'),
        q_tf(3, 'Nhân và chia là đôi máy ngược chiều.', True,
             'Đúng — đã gặp ở bài tìm ô trống.'),
        q_mcq(4, 'Mỗi hộp 5 bút, có 4 hộp. Tất cả mấy bút?',
              ['20', '9', '1', '25'], '20', 'Bốn phần, mỗi phần năm bút.'),
        q_tf(5, 'Bài "biết tất cả, hỏi mỗi phần" cũng dùng phép nhân.', False,
             'Sai. Bài ấy dùng phép chia.'),
    ],
)

# ═══ ③ B17 · SƠ ĐỒ HAI ĐOẠN THẲNG ═══
B17 = bai(
    17, 'SƠ ĐỒ HAI ĐOẠN THẲNG — AI DÀI, AI NGẮN',
    'LV 2.1a — Bài toán hơn kém: vẽ sơ đồ rồi mới chọn phép tính.',
    video(
        ['Vẽ được sơ đồ hai đoạn thẳng cho bài hơn kém.',
         'Chọn phép cộng hay phép trừ dựa vào sơ đồ.',
         'Thử lại kết quả bằng chính đề bài.'],
        ['Đề bài: Hoa gấp được 14 con hạc giấy. Lan gấp được ít hơn Hoa 5 con. Hỏi Lan '
         'gấp được bao nhiêu con hạc?',
         'Vẽ mỗi bạn một đoạn thẳng',
         'Đoạn của Hoa dài 14. Đoạn của Lan ngắn hơn, hụt vào 5.',
         'Nhìn sơ đồ chọn phép tính',
         'Đoạn của Lan bằng đoạn của Hoa bớt đi khúc hụt, nên đây là phép trừ.',
         'Tính ra kết quả',
         'Lấy 14 − 5 = 9.',
         'Đáp số: 9 con hạc.',
         'Thử lại: Hoa hơn Lan 14 − 9 = 5 con, khớp đúng đề bài.'],
        ['Có bạn chưa vẽ gì đã nhìn chữ đoán phép tính: thấy chữ "ít hơn" là trừ, thấy '
         'chữ "nhiều hơn" là cộng.',
         'Gợi ý 1: Có đề mà chữ "ít hơn" đứng cạnh người NHIỀU hơn đấy.',
         'Gợi ý 2: Vẽ hai đoạn ra rồi hỏi ai dài ai ngắn, phép tính sẽ tự hiện ra.',
         'Chữa: câu thần chú trước mọi bài hơn kém là ai dài, ai ngắn, thò ra bao '
         'nhiêu. Vẽ xong ba câu ấy mới chọn phép tính.'],
        ['Cho hai anh em đứng cạnh nhau rồi hỏi con ai cao hơn, cao hơn bao nhiêu — đó '
         'chính là sơ đồ hai đoạn thẳng bằng người thật.',
         'Bố mẹ hỏi: "Con vẽ sơ đồ chưa?" Chưa vẽ là chưa làm bài.'],
    ),
    [
        lt(1, 1, 'Tính 14 − 5.', 'Lấy 14 − 5 = 9.'),
        lt(2, 1, 'Hoa gấp 14 con hạc, Lan ít hơn Hoa 5 con. Đoạn thẳng của ai dài hơn?',
           'Lan ít hơn nên đoạn của Hoa dài hơn.'),
        lt(3, 1, 'Hoa gấp 14 con hạc, Lan ít hơn Hoa 5 con. Lan gấp được mấy con?',
           'Lấy 14 − 5 = 9.'),
        lt(4, 2, 'An có 8 viên bi. Bình nhiều hơn An 3 viên. Bình có mấy viên?',
           'Lấy 8 + 3 = 11.'),
        lt(5, 2, 'Trước khi chọn phép tính, việc đầu tiên phải làm là gì?',
           'Vẽ sơ đồ ra xem ai dài ai ngắn, rồi phép tính tự hiện ra.'),
        lt(6, 2, 'Mai có 20 nhãn vở. Hằng ít hơn Mai 7 nhãn. Hằng có mấy nhãn, và cả '
                 'hai có tất cả mấy nhãn?',
           'Hằng có 20 − 7 = 13 nhãn. Cả hai có 20 + 13 = 33 nhãn.'),
        lt(7, 3, 'Nam có 15 viên bi, nhiều hơn Việt 6 viên. Việt có mấy viên?',
           'Nam nhiều hơn nên Việt ít hơn: 15 − 6 = 9.'),
        lt(8, 3, 'Lan có 12 quyển truyện. Mai nhiều hơn Lan 5 quyển. Hùng ít hơn Mai '
                 '4 quyển. Mai và Hùng mỗi người có mấy quyển?',
           'Mai có 12 + 5 = 17 quyển. Hùng có 17 − 4 = 13 quyển.'),
    ] + [
        q_tf(1, 'Vẽ sơ đồ rồi mới chọn phép tính, đừng nhìn chữ mà đoán.', True,
             'Đúng — sơ đồ mới là chỗ phép tính hiện ra.'),
        q_mcq(2, 'Hoa 14 con hạc, Lan ít hơn Hoa 5 con. Lan mấy con?',
              ['9', '19', '5', '14'], '9', 'Đoạn của Lan hụt vào năm.'),
        q_mcq(3, 'An 8 viên bi, Bình nhiều hơn An 3 viên. Bình mấy viên?',
              ['11', '5', '3', '8'], '11', 'Đoạn của Bình thò ra ba.'),
        q_tf(4, 'Ai ít hơn thì đoạn thẳng của người ấy ngắn hơn.', True,
             'Đúng — đó là cách đọc sơ đồ.'),
        q_tf(5, 'Phép tính hiện ra từ chữ "nhiều hơn" hay "ít hơn".', False,
             'Sai. Nó hiện ra từ sơ đồ — ai dài, ai ngắn.'),
    ],
)

# ═══ ④ B55 · BẪY CÂU CHỮ ĐẢO ═══
B55 = bai(
    55, 'BẪY CÂU CHỮ ĐẢO — "AN ÍT HƠN BÌNH" THÌ AI NHIỀU HƠN',
    'LV 2.1b — Bài toán hơn kém: chữ chỉ hơn kém đứng cạnh người kia.',
    video(
        ['Đọc đúng câu có chữ hơn kém đứng cạnh người ít hơn.',
         'Hỏi "ai nhiều hơn" trước khi chọn phép tính.',
         'Thử lại kết quả cho khớp đề bài.'],
        ['Đề bài: An ít hơn Bình 3 viên bi. An có 8 viên. Hỏi Bình có bao nhiêu viên?',
         'Chữ "ít hơn" đứng cạnh An',
         'Đọc lướt thì tưởng phải làm phép trừ, vì thấy ngay chữ ít hơn.',
         'Hỏi lại: ai nhiều hơn',
         'An ít hơn Bình, tức là BÌNH mới là người nhiều bi hơn. Đoạn của Bình dài '
         'hơn.',
         'Nhìn sơ đồ chọn phép tính',
         'Đoạn của Bình bằng đoạn của An thò thêm 3, nên đây là phép cộng: 8 + 3 = 11.',
         'Đáp số: Bình có 11 viên bi.',
         'Thử lại: An ít hơn Bình 11 − 8 = 3 viên, khớp đúng đề bài.'],
        ['Có bạn thấy chữ "ít hơn" là trừ luôn, lấy 8 − 3 rồi ghi Bình có 5 viên.',
         'Gợi ý 1: Bình 5 viên mà lại nhiều bi hơn An 8 viên — nghe có xuôi tai không?',
         'Gợi ý 2: Vẽ sơ đồ xem đoạn của Bình phải dài hơn hay ngắn hơn đoạn của An.',
         'Chữa: Bình mới là người nhiều hơn, nên phải cộng: 8 + 3 = 11 viên.'],
        ['Đọc đề chậm cùng con và hỏi lại bằng lời khác: "Vậy ai nhiều hơn?" — chỉ một '
         'câu ấy là gỡ được cả cái bẫy.',
         'Bố mẹ hỏi: "Chữ ít hơn đang nói về ai?"'],
    ),
    [
        lt(1, 1, 'An ít hơn Bình 3 viên bi. Ai có nhiều bi hơn?',
           'An ít hơn nên Bình mới là người nhiều bi hơn.'),
        lt(2, 1, 'Tính 8 + 3.', 'Lấy 8 + 3 = 11.'),
        lt(3, 1, 'An ít hơn Bình 3 viên, An có 8 viên. Bình có mấy viên?',
           'Bình nhiều hơn nên lấy 8 + 3 = 11.'),
        lt(4, 2, 'Hoa nhiều hơn Mai 6 quyển vở. Mai có 9 quyển. Hoa có mấy quyển?',
           'Hoa nhiều hơn nên lấy 9 + 6 = 15.'),
        lt(5, 2, 'Câu "An ít hơn Bình" nói ai là người nhiều hơn?',
           'Chữ ít hơn đứng cạnh An, nhưng người nhiều hơn là Bình.'),
        lt(6, 2, 'Việt ít hơn Nam 4 viên bi, Việt có 12 viên. Nam có mấy viên, và cả '
                 'hai có tất cả mấy viên?',
           'Nam nhiều hơn nên có 12 + 4 = 16 viên. Cả hai có 12 + 16 = 28 viên.'),
        lt(7, 3, 'Có bạn gặp bài "An ít hơn Bình 3 viên, An có 8 viên" rồi ghi Bình có '
                 '5 viên. Cho biết bạn ấy sai ở đâu và số đúng là bao nhiêu.',
           'Bạn ấy thấy chữ ít hơn là trừ ngay, không hỏi ai nhiều hơn. Bình mới là '
           'người nhiều bi hơn nên phải cộng: 8 + 3 = 11 viên.'),
        lt(8, 3, 'Mai ít hơn Lan 5 nhãn vở. Lan ít hơn Hoa 3 nhãn. Mai có 10 nhãn. Lan '
                 'và Hoa mỗi người có mấy nhãn?',
           'Lan nhiều hơn Mai nên có 10 + 5 = 15 nhãn. Hoa nhiều hơn Lan nên có '
           '15 + 3 = 18 nhãn.'),
    ] + [
        q_tf(1, 'Câu "An ít hơn Bình" nghĩa là Bình nhiều hơn An.', True,
             'Đúng — chữ đứng cạnh ai không quyết định ai nhiều hơn.'),
        q_mcq(2, 'An ít hơn Bình 3 viên, An có 8 viên. Bình mấy viên?',
              ['11', '5', '3', '8'], '11', 'Bình nhiều hơn nên phải cộng.'),
        q_tf(3, 'Thấy chữ "ít hơn" thì cứ làm phép trừ.', False,
             'Sai. Phải hỏi ai nhiều hơn rồi mới chọn phép tính.'),
        q_mcq(4, 'Trước khi chọn phép tính, phải hỏi câu nào?',
              ['ai nhiều hơn, ai ít hơn', 'số nào to hơn', 'có mấy con số'],
              'ai nhiều hơn, ai ít hơn', 'Trả lời xong câu ấy thì vẽ được sơ đồ.'),
        q_tf(5, 'Hoa nhiều hơn Mai 6 quyển, Mai có 9 quyển thì Hoa có 15 quyển.', True,
             'Đúng — chín cộng sáu.'),
    ],
)

# ═══ ⑤ B18 · LIỆT KÊ CÓ THỨ TỰ ═══
B18 = bai(
    18, 'LIỆT KÊ CÓ THỨ TỰ MỌI CÁCH TÁCH TỔNG',
    'LV 2.1c — Tách một tổng thành hai phần: liệt kê có thứ tự.',
    video(
        ['Liệt kê có thứ tự mọi cách tách một tổng thành hai phần.',
         'Đếm được số cách tách.',
         'Hiểu vì sao liệt kê có thứ tự thì không sót và không trùng.'],
        ['Đề bài: Hai bạn có tất cả 12 viên kẹo, mỗi bạn ít nhất một viên. Hãy liệt kê '
         'mọi cách chia số kẹo ấy cho hai bạn.',
         'Liệt kê có thứ tự, đừng đoán bừa',
         'Cho phần thứ nhất giảm dần từ lớn xuống bé, thì phần thứ hai tự hiện ra.',
         'Kẻ bảng ra nháp',
         'Các cách tách là 11 và 1, rồi 10 và 2, rồi 9 và 3, rồi 8 và 4, rồi 7 và 5, '
         'rồi 6 và 6.',
         'Đếm xem có mấy cách',
         'Đếm được 6 cách tách.',
         'Đáp số: có 6 cách.',
         'Liệt kê có thứ tự thì không sót cách nào, cũng không kể trùng cách nào.'],
        ['Có bạn nghĩ ra được vài cách rồi ghi luôn đáp số, không kẻ bảng gì cả.',
         'Gợi ý 1: Làm sao biết mình đã nghĩ hết chưa, hay còn sót cách nào?',
         'Gợi ý 2: Nếu cho phần thứ nhất giảm dần từng một thì có bỏ sót được không?',
         'Chữa: liệt kê có thứ tự mới chắc chắn không sót. Nghĩ tới đâu ghi tới đó thì '
         'vừa dễ sót vừa dễ kể trùng.'],
        ['Đưa con một nắm kẹo rồi bảo chia cho hai bạn búp bê theo đủ mọi cách — con '
         'sẽ tự thấy phải làm có thứ tự mới không rối.',
         'Bố mẹ hỏi: "Con chắc chưa sót cách nào chứ?"'],
    ),
    [
        lt(1, 1, 'Tách 12 thành hai phần, phần thứ nhất là 11 thì phần thứ hai là mấy?',
           'Lấy 12 − 11 = 1.'),
        lt(2, 1, 'Tách 12 thành hai phần, phần thứ nhất là 9 thì phần thứ hai là mấy?',
           'Lấy 12 − 9 = 3.'),
        lt(3, 1, 'Tách 10 thành hai phần, mỗi phần ít nhất một viên và phần trước '
                 'không bé hơn phần sau. Có mấy cách?',
           'Liệt kê 9 và 1, 8 và 2, 7 và 3, 6 và 4, 5 và 5 — đếm được 5 cách.'),
        lt(4, 2, 'Tách 12 thành hai phần, mỗi phần ít nhất một viên và phần trước '
                 'không bé hơn phần sau. Có mấy cách?',
           'Liệt kê từ 11 và 1 cho tới 6 và 6, đếm được 6 cách.'),
        lt(5, 2, 'Vì sao phải liệt kê có thứ tự?',
           'Để không sót cách nào và cũng không kể trùng cách nào.'),
        lt(6, 2, 'Tách 8 thành hai phần, mỗi phần ít nhất một viên và phần trước không '
                 'bé hơn phần sau. Cách đầu tiên và cách cuối cùng có phần thứ nhất là '
                 'mấy?',
           'Cách đầu là 7 và 1, cách cuối là 4 và 4.'),
        lt(7, 3, 'Tách 12 thành hai phần. Nếu phần thứ nhất là 8 thì phần ấy hơn phần '
                 'kia mấy viên?',
           'Phần kia là 12 − 8 = 4, nên hơn nhau 8 − 4 = 4 viên.'),
        lt(8, 3, 'Trong bảng tách 12, cột "hơn nhau" chạy 10, 8, 6, 4, 2, 0. Cho biết '
                 'mỗi lần chuyển một viên thì phần hơn giảm mấy, và vì sao.',
           'Mỗi lần chuyển một viên thì phần hơn giảm 2, vì một bên bớt một viên còn '
           'bên kia thêm một viên.'),
    ] + [
        q_tf(1, 'Liệt kê có thứ tự thì không sót cách nào.', True,
             'Đúng — đó là lý do phải kẻ bảng.'),
        q_mcq(2, 'Tách 12 thành hai phần, mỗi phần ít nhất một viên và phần trước '
                 'không bé hơn phần sau. Có mấy cách?',
              ['6', '12', '5', '11'], '6', 'Từ 11 và 1 cho tới 6 và 6.'),
        q_mcq(3, 'Tách 12 mà phần thứ nhất là 9 thì phần thứ hai là mấy?',
              ['3', '21', '9', '4'], '3', 'Mười hai bớt chín.'),
        q_tf(4, 'Đoán bừa một cách rồi thôi là làm xong bài.', False,
             'Sai. Phải liệt kê đủ để chắc chắn không sót cách nào.'),
        q_tf(5, 'Trong bảng tách một tổng, mỗi lần chuyển một viên thì phần hơn giảm '
                '2.', True, 'Đúng — một bên bớt một, bên kia thêm một.'),
    ],
)

# ═══ ⑥ B56 · DÒ CỘT HƠN NHAU ═══
B56 = bai(
    56, 'DÒ CỘT HƠN NHAU — THỬ LẠI ĐỦ HAI ĐIỀU KIỆN',
    'LV 2.1d — Bài hai điều kiện: chọn dòng đúng rồi kiểm cả tổng lẫn phần hơn.',
    video(
        ['Nhận ra bài có hai điều kiện cùng lúc.',
         'Dò cột "hơn nhau" để chọn đúng dòng.',
         'Thử lại đủ cả hai điều kiện trước khi chốt.'],
        ['Đề bài: Hai bạn có tất cả 12 viên kẹo, bạn An hơn bạn Bình 4 viên. Hỏi mỗi '
         'bạn có mấy viên kẹo?',
         'Bài này có hai điều kiện cùng lúc',
         'Điều kiện thứ nhất là tổng bằng 12. Điều kiện thứ hai là An hơn Bình 4 viên.',
         'Liệt kê theo điều kiện thứ nhất',
         'Các cách tách 12 là 11 và 1, 10 và 2, 9 và 3, 8 và 4, 7 và 5, 6 và 6.',
         'Dò cột hơn nhau theo điều kiện thứ hai',
         'Cột hơn nhau chạy 10, 8, 6, 4, 2, 0. Dòng có số bốn là dòng 8 và 4.',
         'Thử lại đủ cả hai điều kiện',
         'Kiểm tổng: 8 + 4 = 12 đúng. Kiểm phần hơn: 8 − 4 = 4 đúng.',
         'Đáp số: An 8 viên, Bình 4 viên.',
         'Chỉ thử một điều kiện là chưa xong bài — đó là chỗ hay mất điểm nhất.'],
        ['Với bài tổng 10 và hơn nhau 2, có bạn hớn hở ghi anh 7 em 3 vì cộng lại đúng '
         'mười.',
         'Gợi ý 1: Bạn ấy mới kiểm được mấy điều kiện? Còn điều kiện nào chưa kiểm?',
         'Gợi ý 2: Bảy hơn ba mấy viên? Có đúng bằng hai như đề nói không?',
         'Chữa: tổng thì đúng nhưng phần hơn sai. Dòng đúng là 6 và 4.'],
        ['Bài nào có hai điều kiện thì hỏi con hai lần: "Đúng điều kiện thứ nhất '
         'chưa?" rồi "Đúng điều kiện thứ hai chưa?"',
         'Bố mẹ hỏi: "Con kiểm đủ hai điều kiện chưa?"'],
    ),
    [
        lt(1, 1, 'Tính 8 + 4.', 'Lấy 8 + 4 = 12.'),
        lt(2, 1, 'Tính 8 − 4.', 'Lấy 8 − 4 = 4.'),
        lt(3, 1, 'Hai bạn có tất cả 12 viên, An hơn Bình 4 viên. An có mấy viên?',
           'Dò bảng thấy dòng 8 và 4 có phần hơn đúng bốn, nên An có 8 viên.'),
        lt(4, 2, 'Hai bạn có tất cả 12 viên, An hơn Bình 4 viên. Bình có mấy viên?',
           'Dòng đúng là 8 và 4, nên Bình có 4 viên.'),
        lt(5, 2, 'Hai bạn có tất cả 10 viên, anh hơn em 2 viên. Mỗi bạn mấy viên?',
           'Dò bảng tách 10 thấy dòng 6 và 4 có phần hơn đúng hai. Anh 6 viên, em 4 '
           'viên.'),
        lt(6, 2, 'Có bạn giải bài tổng 10 hơn nhau 2 rồi ghi anh 7 em 3. Bạn ấy quên '
                 'kiểm điều kiện nào?',
           'Bạn ấy quên kiểm điều kiện phần hơn: bảy trừ ba bằng bốn chứ không phải '
           'hai.'),
        lt(7, 3, 'Hai bạn có tất cả 14 viên, bạn lớn hơn bạn bé 4 viên. Mỗi bạn mấy '
                 'viên, và thử lại tổng được bao nhiêu?',
           'Dò bảng tách 14 thấy dòng 9 và 5 hơn nhau đúng bốn. Thử lại: 9 + 5 = 14.'),
        lt(8, 3, 'Hai bạn có tất cả 12 viên và bằng nhau. Mỗi bạn mấy viên, và phần '
                 'hơn bằng mấy?',
           'Dòng cuối bảng là 6 và 6, nên mỗi bạn 6 viên và phần hơn bằng 0.'),
    ] + [
        q_tf(1, 'Bài hai điều kiện thì phải thử lại cả hai.', True,
             'Đúng — đó là chỗ hay mất điểm nhất.'),
        q_mcq(2, 'Tổng 12, An hơn Bình 4 viên. An có mấy viên?',
              ['8', '4', '6', '10'], '8', 'Dòng có phần hơn bằng bốn.'),
        q_mcq(3, 'Tổng 10, anh hơn em 2 viên. Anh có mấy viên?',
              ['6', '7', '5', '8'], '6', 'Dòng 6 và 4 hơn nhau đúng hai.'),
        q_tf(4, 'Anh 7 em 3 là đáp án đúng cho bài tổng 10 hơn nhau 2.', False,
             'Sai. Tổng thì đúng nhưng phần hơn lại bằng bốn.'),
        q_tf(5, 'Liệt kê xong thì dò cột hơn nhau để chọn dòng đúng.', True,
             'Đúng — hai bước đi liền nhau.'),
    ],
)

# ═══ ⑦ B19 · VẼ THEO PHẦN ═══
B19 = bai(
    19, 'VẼ THEO PHẦN — GẤP MẤY LẦN LÀ MẤY KHỐI',
    'LV 3.1a — Gấp một số lên nhiều lần: vẽ sơ đồ theo phần và đếm phần.',
    video(
        ['Hiểu "gấp mấy lần" nghĩa là có bấy nhiêu phần bằng nhau.',
         'Vẽ được sơ đồ theo phần.',
         'Đếm được tổng số phần bằng nhau.'],
        ['Đề bài: Bố hái được số cam gấp 3 lần con. Cả hai bố con hái được 12 quả. Vẽ '
         'sơ đồ và cho biết có tất cả mấy phần bằng nhau.',
         'Gấp mấy lần thì vẽ mấy khối',
         'Con vẽ một khối. Bố gấp ba lần con nên bố vẽ ba khối y hệt.',
         'Ngoặc ôm cả hai đoạn',
         'Cả 12 quả nằm trọn trong bốn khối ấy.',
         'Đếm tổng số phần',
         'Lấy 1 + 3 = 4 phần bằng nhau.',
         'Đáp số: có 4 phần bằng nhau.',
         'Chữ "gấp mấy lần" luôn nói về PHẦN, nên việc đầu tiên là vẽ khối rồi đếm '
         'phần.'],
        ['Với bài chị gấp đôi em và cả hai có 9 viên, có bạn lấy luôn 9 nhân 2 rồi ghi '
         'chị được 18 viên.',
         'Gợi ý 1: Cả gói chỉ có chín viên mà chị được những mười tám. Kẹo mọc thêm ở '
         'đâu ra vậy?',
         'Gợi ý 2: Chị gấp đôi AI — gấp đôi cả gói, hay gấp đôi phần của em?',
         'Chữa: chị gấp đôi PHẦN CỦA EM thôi. Vẽ em một khối, chị hai khối, rồi mới '
         'chia.'],
        ['Xếp khối gỗ hoặc que tính thành từng cụm bằng nhau cho con nhìn — "gấp ba '
         'lần" thành ba cụm y hệt, thấy ngay.',
         'Bố mẹ hỏi: "Gấp mấy lần thì vẽ mấy khối?"'],
    ),
    [
        lt(1, 1, 'Chị gấp 2 lần em. Chị vẽ mấy khối?',
           'Gấp hai lần thì vẽ 2 khối y hệt nhau.'),
        lt(2, 1, 'Em vẽ 1 khối, chị vẽ 2 khối. Có tất cả mấy phần bằng nhau?',
           'Lấy 1 + 2 = 3 phần.'),
        lt(3, 1, 'Bố gấp 3 lần con. Có tất cả mấy phần bằng nhau?',
           'Con một khối, bố ba khối: 1 + 3 = 4 phần.'),
        lt(4, 2, 'Anh gấp 4 lần em. Có tất cả mấy phần bằng nhau?',
           'Em một khối, anh bốn khối: 1 + 4 = 5 phần.'),
        lt(5, 2, 'Chữ "gấp mấy lần" nói về cái gì?',
           'Nó nói về số phần bằng nhau, nên phải vẽ khối rồi đếm phần.'),
        lt(6, 2, 'Chị gấp 2 lần em, cả hai có 9 viên kẹo. Vẽ sơ đồ thì em mấy khối, '
                 'chị mấy khối, và tất cả mấy phần?',
           'Em 1 khối, chị 2 khối, cộng lại được 3 phần bằng nhau.'),
        lt(7, 3, 'Có bạn thấy "chị gấp đôi em, cả hai có 9 viên" rồi ghi chị được 18 '
                 'viên. Bạn ấy sai ở đâu?',
           'Chị gấp đôi phần của em chứ không gấp đôi cả gói. Cả gói chỉ có chín viên '
           'thì chị không thể được mười tám viên.'),
        lt(8, 3, 'Bố gấp 3 lần con, mẹ gấp 2 lần con. Vẽ sơ đồ ba người thì có tất cả '
                 'mấy phần bằng nhau?',
           'Con 1 phần, bố 3 phần, mẹ 2 phần: 1 + 3 + 2 = 6 phần.'),
    ] + [
        q_tf(1, 'Gấp mấy lần thì vẽ bấy nhiêu khối bằng nhau.', True,
             'Đúng — đó là cách chuyển lời thành hình.'),
        q_mcq(2, 'Bố gấp 3 lần con. Tất cả mấy phần?', ['4', '3', '2', '12'], '4',
              'Con một phần cộng bố ba phần.'),
        q_mcq(3, 'Chị gấp 2 lần em. Tất cả mấy phần?', ['3', '2', '9', '1'], '3',
              'Em một phần cộng chị hai phần.'),
        q_tf(4, 'Chị gấp đôi em nghĩa là chị gấp đôi cả gói kẹo.', False,
             'Sai. Chị gấp đôi PHẦN của em thôi.'),
        q_tf(5, 'Việc đầu tiên của bài gấp mấy lần là vẽ khối rồi đếm phần.', True,
             'Đúng — chưa đếm phần thì chưa chia được.'),
    ],
)

# ═══ ⑧ B57 · CHIA TỔNG CHO SỐ PHẦN ═══
B57 = bai(
    57, 'CHIA TỔNG CHO SỐ PHẦN RỒI TRẢ VỀ TỪNG NGƯỜI',
    'LV 3.1b — Gấp một số lên nhiều lần: tìm một phần rồi tìm từng người.',
    video(
        ['Chia tổng cho số phần để tìm một phần.',
         'Trả về cho từng người theo số phần của họ.',
         'Thử lại đủ hai điều kiện: đúng tổng và đúng số lần gấp.'],
        ['Đề bài: Bố hái được số cam gấp 3 lần con. Cả hai hái được 12 quả. Hỏi mỗi '
         'người hái được mấy quả?',
         'Đếm tổng số phần trước',
         'Con 1 phần, bố 3 phần, cộng lại 1 + 3 = 4 phần bằng nhau.',
         'Chia tổng cho số phần để tìm MỘT phần',
         'Lấy 12 : 4 = 3. Vậy một phần là 3 quả.',
         'Trả về cho từng người',
         'Con một phần nên được 3 quả. Bố ba phần nên được 3 × 3 = 9 quả.',
         'Thử lại đủ hai điều kiện',
         'Kiểm tổng: 3 + 9 = 12 đúng. Kiểm số lần gấp: chín gấp ba lần ba, đúng.',
         'Đáp số: con 3 quả, bố 9 quả.',
         'Bốn nhịp: đếm phần, chia tìm một phần, trả về từng người, rồi thử lại.'],
        ['Có bạn tìm được một phần bằng 3 rồi ghi luôn đáp số là 3, không trả về cho '
         'từng người nữa.',
         'Gợi ý 1: Ba quả là phần của ai — của con, của bố, hay của cả hai?',
         'Gợi ý 2: Bố có mấy phần? Mỗi phần ba quả thì bố được bao nhiêu?',
         'Chữa: tìm được một phần mới đi được nửa đường. Còn phải nhân số phần của '
         'từng người: bố 3 × 3 = 9 quả.'],
        ['Chia quà cho hai anh em theo kiểu "anh gấp đôi em" rồi cùng con tính xem mỗi '
         'người mấy cái — con sẽ thấy phải tìm một phần trước.',
         'Bố mẹ hỏi: "Ba quả ấy là phần của ai?"'],
    ),
    [
        lt(1, 1, 'Tính 12 : 4.', 'Lấy 12 : 4 = 3.'),
        lt(2, 1, 'Bố gấp 3 lần con, cả hai hái 12 quả. Một phần là mấy quả?',
           'Có bốn phần nên 12 : 4 = 3 quả một phần.'),
        lt(3, 1, 'Một phần là 3 quả, bố có 3 phần. Bố hái được mấy quả?',
           'Lấy 3 × 3 = 9.'),
        lt(4, 2, 'Chị gấp 2 lần em, cả hai có 9 viên kẹo. Em được mấy viên?',
           'Có ba phần nên một phần là 9 : 3 = 3 viên. Em một phần nên được 3 viên.'),
        lt(5, 2, 'Chị gấp 2 lần em, cả hai có 9 viên kẹo. Chị được mấy viên?',
           'Một phần là 3 viên, chị hai phần nên được 3 × 2 = 6 viên.'),
        lt(6, 2, 'Anh gấp 4 lần em, cả hai có 20 quả. Em mấy quả, anh mấy quả?',
           'Có năm phần nên một phần là 20 : 5 = 4 quả. Em 4 quả, anh 4 × 4 = 16 quả.'),
        lt(7, 3, 'Bố gấp 3 lần con, cả hai hái 16 quả. Mỗi người mấy quả, và thử lại '
                 'tổng được bao nhiêu?',
           'Có bốn phần nên một phần là 16 : 4 = 4 quả. Con 4 quả, bố 4 × 3 = 12 quả. '
           'Thử lại: 4 + 12 = 16.'),
        lt(8, 3, 'Chị gấp 2 lần em, chị hơn em 5 viên kẹo. Một phần là mấy viên, và cả '
                 'hai có tất cả mấy viên?',
           'Chị hơn em đúng một phần nên một phần là 5 viên. Em 5 viên, chị '
           '5 × 2 = 10 viên, cả hai có 15 viên.'),
    ] + [
        q_tf(1, 'Lấy tổng chia cho số phần thì được một phần.', True,
             'Đúng — đó là bước then chốt.'),
        q_mcq(2, 'Bố gấp 3 lần con, cả hai 12 quả. Con mấy quả?',
              ['3', '4', '9', '6'], '3', 'Con đúng một phần.'),
        q_mcq(3, 'Bố gấp 3 lần con, cả hai 12 quả. Bố mấy quả?',
              ['9', '3', '4', '12'], '9', 'Bố ba phần, mỗi phần ba quả.'),
        q_tf(4, 'Tìm được một phần rồi là xong bài.', False,
             'Sai. Còn phải trả về cho từng người rồi thử lại.'),
        q_tf(5, 'Chị gấp 2 lần em, cả hai 9 viên thì em được 3 viên.', True,
             'Đúng — ba phần, mỗi phần ba viên.'),
    ],
)

# ═══ ⑨ B20 · TUỔI SAU MẤY NĂM ═══
B20 = bai(
    20, 'TUỔI SAU MẤY NĂM — AI CŨNG THÊM BẰNG NHAU',
    'LV 6.1a — Bài toán tuổi: tìm phần hơn và tính tuổi sau mấy năm.',
    video(
        ['Tìm được phần hơn tuổi giữa hai người.',
         'Tính được tuổi mỗi người sau mấy năm nữa.',
         'Nhớ rằng ai cũng thêm cùng một số tuổi.'],
        ['Đề bài: Năm nay mẹ 32 tuổi, con 7 tuổi. Hỏi mẹ hơn con bao nhiêu tuổi, và '
         'sau 5 năm nữa mỗi người bao nhiêu tuổi?',
         'Tìm phần hơn của năm nay',
         'Lấy 32 − 7 = 25. Mẹ hơn con 25 tuổi.',
         'Sau mấy năm thì AI CŨNG thêm bấy nhiêu',
         'Thời gian công bằng với tất cả. Sau 5 năm thì cả mẹ lẫn con đều thêm đúng 5 '
         'tuổi.',
         'Tính tuổi từng người',
         'Mẹ 32 + 5 = 37 tuổi. Con 7 + 5 = 12 tuổi.',
         'Đáp số: mẹ hơn con 25 tuổi; sau 5 năm mẹ 37 tuổi, con 12 tuổi.',
         'Chỗ hay quên nhất là chỉ cộng tuổi cho một người rồi để người kia đứng yên.'],
        ['Có bạn tính tuổi mẹ sau năm năm thì cộng đúng, mà tuổi con thì để nguyên như '
         'cũ.',
         'Gợi ý 1: Năm năm nữa thì có phải chỉ mình mẹ thêm tuổi không? Con đứng yên '
         'à?',
         'Gợi ý 2: Cộng thêm năm tuổi cho CẢ HAI người rồi hãy so.',
         'Chữa: thời gian trôi thì ai cũng thêm tuổi bằng nhau. Mẹ 32 + 5 = 37 tuổi và '
         'con 7 + 5 = 12 tuổi.'],
        ['Lấy tuổi thật của người nhà ra tính cùng con — bài toán tuổi thú vị nhất khi '
         'nó nói về chính gia đình mình.',
         'Bố mẹ hỏi: "Con đã cộng tuổi cho cả hai người chưa?"'],
    ),
    [
        lt(1, 1, 'Tính 32 − 7.', 'Lấy 32 − 7 = 25.'),
        lt(2, 1, 'Năm nay em 6 tuổi. Sau 2 năm nữa em mấy tuổi?', 'Lấy 6 + 2 = 8.'),
        lt(3, 1, 'Năm nay mẹ 32 tuổi. Sau 5 năm nữa mẹ mấy tuổi?', 'Lấy 32 + 5 = 37.'),
        lt(4, 2, 'Năm nay em 6 tuổi, anh 9 tuổi. Anh hơn em mấy tuổi?',
           'Lấy 9 − 6 = 3.'),
        lt(5, 2, 'Sau 2 năm nữa thì ai được thêm tuổi?',
           'Cả hai người đều thêm hai tuổi, vì thời gian công bằng với tất cả.'),
        lt(6, 2, 'Năm nay em 6 tuổi, anh 9 tuổi. Sau 2 năm nữa mỗi người mấy tuổi?',
           'Em 6 + 2 = 8 tuổi, anh 9 + 2 = 11 tuổi.'),
        lt(7, 3, 'Năm nay mẹ 32 tuổi, con 7 tuổi. Sau 5 năm nữa mẹ mấy tuổi và con mấy '
                 'tuổi?',
           'Mẹ 32 + 5 = 37 tuổi, con 7 + 5 = 12 tuổi.'),
        lt(8, 3, 'Năm nay bố 35 tuổi, con 10 tuổi. Cho biết bố hơn con mấy tuổi, và '
                 'sau 3 năm nữa mỗi người mấy tuổi.',
           'Bố hơn con 35 − 10 = 25 tuổi. Sau ba năm bố 35 + 3 = 38 tuổi, con '
           '10 + 3 = 13 tuổi.'),
    ] + [
        q_tf(1, 'Sau mấy năm thì ai cũng thêm bấy nhiêu tuổi.', True,
             'Đúng — thời gian công bằng với tất cả.'),
        q_mcq(2, 'Mẹ 32 tuổi, con 7 tuổi. Mẹ hơn con mấy tuổi?',
              ['25', '39', '32', '7'], '25', 'Lấy ba mươi hai trừ bảy.'),
        q_mcq(3, 'Em 6 tuổi, sau 2 năm em mấy tuổi?', ['8', '4', '12', '6'], '8',
              'Sáu cộng hai.'),
        q_tf(4, 'Sau 2 năm thì chỉ người lớn thêm tuổi.', False,
             'Sai. Cả hai người đều thêm hai tuổi.'),
        q_tf(5, 'Mẹ 32 tuổi, sau 5 năm mẹ 37 tuổi.', True, 'Đúng — ba mươi hai cộng '
             'năm.'),
    ],
)

# ═══ ⑩ B58 · HIỆU TUỔI KHÔNG ĐỔI ═══
B58 = bai(
    58, 'PHẦN HƠN TUỔI KHÔNG BAO GIỜ ĐỔI',
    'LV 6.1b — Bài toán tuổi: hiệu số tuổi giữ nguyên theo thời gian.',
    video(
        ['Khám phá phần hơn tuổi giữa hai người không đổi.',
         'Giải thích được vì sao nó không đổi.',
         'Dùng phần hơn để trả lời nhanh mà không phải tính lại.'],
        ['Đề bài: Năm nay em 6 tuổi, anh 9 tuổi. Sau 2 năm nữa anh hơn em bao nhiêu '
         'tuổi?',
         'Tính phần hơn của năm nay',
         'Lấy 9 − 6 = 3. Anh hơn em 3 tuổi.',
         'Tính tuổi hai người sau 2 năm',
         'Em 6 + 2 = 8 tuổi. Anh 9 + 2 = 11 tuổi.',
         'Tính lại phần hơn',
         'Lấy 11 − 8 = 3. Vẫn đúng 3 tuổi như cũ.',
         'Đáp số: vẫn 3 tuổi.',
         'Hai bên cùng thêm bằng nhau thì phần hơn giữ nguyên — dù mười năm hay một '
         'trăm năm nữa cũng thế.'],
        ['Có bạn quả quyết anh hơn em ba tuổi thì sau hai năm anh sẽ hơn em năm tuổi, '
         'vì thời gian trôi mà.',
         'Gợi ý 1: Sau hai năm, có phải chỉ mình anh thêm tuổi không? Em đứng yên à?',
         'Gợi ý 2: Lấy số cụ thể mà tính: em sáu tuổi, anh chín tuổi, cộng thêm hai '
         'cho cả hai rồi trừ thử.',
         'Chữa: em cũng thêm hai tuổi nên phần hơn vẫn là ba. Em không bao giờ đuổi '
         'kịp anh được.'],
        ['Hỏi con một câu vui: "Bao giờ thì con bằng tuổi anh?" — câu trả lời không '
         'bao giờ, và bài này nói rõ vì sao.',
         'Bố mẹ hỏi: "Cả hai cùng thêm tuổi thì phần hơn đổi không?"'],
    ),
    [
        lt(1, 1, 'Năm nay em 6 tuổi, anh 9 tuổi. Anh hơn em mấy tuổi?',
           'Lấy 9 − 6 = 3.'),
        lt(2, 1, 'Sau 2 năm em 8 tuổi, anh 11 tuổi. Anh hơn em mấy tuổi?',
           'Lấy 11 − 8 = 3.'),
        lt(3, 1, 'Phần hơn tuổi giữa hai người có đổi theo thời gian không?',
           'Hai bên cùng thêm bằng nhau nên phần hơn giữ nguyên.'),
        lt(4, 2, 'Anh hơn em 3 tuổi. Sau 10 năm nữa anh hơn em mấy tuổi?',
           'Phần hơn không đổi nên vẫn là 3 tuổi.'),
        lt(5, 2, 'Mẹ hơn con 25 tuổi. Sau 8 năm nữa mẹ hơn con mấy tuổi?',
           'Phần hơn không đổi nên vẫn là 25 tuổi.'),
        lt(6, 2, 'Có bạn bảo anh hơn em 3 tuổi thì sau 2 năm anh hơn em 5 tuổi. Bạn ấy '
                 'sai ở đâu?',
           'Bạn ấy tưởng chỉ mình anh thêm tuổi. Em cũng thêm hai tuổi nên phần hơn '
           'vẫn là 3.'),
        lt(7, 3, 'Năm nay bố 35 tuổi, con 10 tuổi. Sau 5 năm nữa bố hơn con mấy tuổi, '
                 'và cách đây 2 năm bố hơn con mấy tuổi?',
           'Bố hơn con 35 − 10 = 25 tuổi. Phần hơn không đổi nên lúc nào cũng là 25 '
           'tuổi.'),
        lt(8, 3, 'Anh hơn em 4 tuổi, năm nay em 7 tuổi. Cho biết năm nay anh mấy tuổi '
                 'và sau 6 năm nữa anh hơn em mấy tuổi.',
           'Anh có 7 + 4 = 11 tuổi. Phần hơn không đổi nên sau sáu năm anh vẫn hơn em '
           '4 tuổi.'),
    ] + [
        q_tf(1, 'Phần hơn tuổi giữa hai người không bao giờ đổi.', True,
             'Đúng — vì cả hai cùng thêm bằng nhau.'),
        q_mcq(2, 'Anh hơn em 3 tuổi. Sau 2 năm anh hơn em mấy tuổi?',
              ['3', '5', '1', '6'], '3', 'Phần hơn giữ nguyên.'),
        q_mcq(3, 'Mẹ hơn con 25 tuổi. Sau 8 năm mẹ hơn con mấy tuổi?',
              ['25', '33', '17', '8'], '25', 'Phần hơn giữ nguyên.'),
        q_tf(4, 'Sau 2 năm thì phần hơn tuổi tăng thêm 2.', False,
             'Sai. Cả hai cùng thêm hai nên phần hơn giữ nguyên.'),
        q_tf(5, 'Bài toán tuổi nào cũng nên tìm phần hơn trước tiên.', True,
             'Đúng — đó là con số không đổi của cả bài.'),
    ],
)

# ═══ ⑪ B21 · BIẾT MỖI GIỜ, HỎI TẤT CẢ ═══
B21 = bai(
    21, 'BIẾT MỖI GIỜ, HỎI TẤT CẢ — PHÉP NHÂN',
    'LV 7.1a — Chữ "mỗi" và bài toán năng suất, chuyển động bằng phép nhân.',
    video(
        ['Hiểu chữ "mỗi" là một phần đều nhau lặp đi lặp lại.',
         'Giải bài biết mỗi giờ, hỏi tất cả bằng phép nhân.',
         'Nhận ra bài may áo, bài đi đường, bài chảy nước chung một bộ xương.'],
        ['Đề bài: Một vòi nước mỗi phút chảy được 3 lít. Hỏi sau 4 phút vòi chảy được '
         'bao nhiêu lít nước?',
         'Chữ "mỗi" nghĩa là gì',
         'Mỗi phút 3 lít nghĩa là phút nào cũng đều tăm tắp 3 lít.',
         'Các phần bằng nhau lặp lại là việc của phép nhân',
         'Lấy 3 × 4 = 12.',
         'Đáp số: 12 lít nước.',
         'Bài may áo, bài đi đường, bài chảy nước — khoác áo khác nhau mà chung một '
         'bộ xương: biết mỗi phần rồi hỏi tất cả thì nhân.'],
        ['Có bạn giải bài "mỗi giờ đi 4 ki lô mét, đi 3 giờ" bằng phép cộng, lấy '
         '4 + 3 rồi ghi 7 ki lô mét.',
         'Gợi ý 1: Bốn là ki lô mét còn ba là giờ. Hai thứ khác loại nhau có cộng '
         'thẳng với nhau được không?',
         'Gợi ý 2: Vẽ con đường ba chặng, mỗi chặng bốn ki lô mét rồi cộng dồn xem.',
         'Chữa: ba chặng bằng nhau, mỗi chặng bốn, là việc của phép nhân: '
         '4 × 3 = 12 ki lô mét.'],
        ['Đi đường cùng con thì hỏi: "Mỗi giờ xe đi được bao xa? Hai giờ nữa mình tới '
         'đâu?" — bài toán này có sẵn trên mọi chuyến đi.',
         'Bố mẹ hỏi: "Chữ mỗi trong đề đang nói về cái gì?"'],
    ),
    [
        lt(1, 1, 'Tính 3 × 4.', 'Lấy 3 × 4 = 12.'),
        lt(2, 1, 'Vòi mỗi phút chảy 3 lít. Sau 4 phút chảy được mấy lít?',
           'Lấy 3 × 4 = 12.'),
        lt(3, 1, 'Cô May mỗi giờ may 5 cái áo. Sau 3 giờ may được mấy cái?',
           'Lấy 5 × 3 = 15.'),
        lt(4, 2, 'Xe mỗi giờ đi 4 ki lô mét. Sau 3 giờ xe đi được mấy ki lô mét?',
           'Lấy 4 × 3 = 12.'),
        lt(5, 2, 'Có bạn giải bài "mỗi giờ đi 4 ki lô mét, đi 3 giờ" bằng phép cộng '
                 'rồi ghi 7. Bạn ấy sai ở đâu?',
           'Bốn là ki lô mét còn ba là giờ, hai thứ khác loại thì không cộng thẳng '
           'được. Phải nhân: 4 × 3 = 12.'),
        lt(6, 2, 'Mỗi hộp có 6 cái bánh, mua 4 hộp. Tất cả mấy cái bánh?',
           'Lấy 6 × 4 = 24.'),
        lt(7, 3, 'Vòi mỗi phút chảy 3 lít. Hỏi sau 4 phút và sau 7 phút vòi chảy được '
                 'bao nhiêu lít?',
           'Sau bốn phút: 3 × 4 = 12 lít. Sau bảy phút: 3 × 7 = 21 lít.'),
        lt(8, 3, 'Cô May mỗi giờ may 5 cái áo, làm 3 giờ. Bác Tài mỗi giờ đi 4 ki lô '
                 'mét, đi 3 giờ. Hai bài dùng chung phép tính nào, và kết quả mỗi bài '
                 'là bao nhiêu?',
           'Hai bài chung một bộ xương, đều dùng phép nhân: 5 × 3 = 15 cái áo và '
           '4 × 3 = 12 ki lô mét.'),
    ] + [
        q_tf(1, 'Biết mỗi phần rồi hỏi tất cả thì dùng phép nhân.', True,
             'Đúng — các phần bằng nhau lặp lại.'),
        q_mcq(2, 'Vòi mỗi phút 3 lít, sau 4 phút được mấy lít?',
              ['12', '7', '1', '34'], '12', 'Bốn phần, mỗi phần ba lít.'),
        q_mcq(3, 'Mỗi giờ đi 4 ki lô mét, đi 3 giờ thì được mấy ki lô mét?',
              ['12', '7', '1', '43'], '12', 'Ba chặng, mỗi chặng bốn.'),
        q_tf(4, 'Cộng 4 ki lô mét với 3 giờ được 7 ki lô mét.', False,
             'Sai. Hai thứ khác loại thì không cộng thẳng được, phải nhân.'),
        q_tf(5, 'Chữ "mỗi" nghĩa là một phần đều nhau lặp đi lặp lại.', True,
             'Đúng — thấy chữ mỗi là thấy một phần.'),
    ],
)

# ═══ ⑫ B59 · BIẾT TẤT CẢ, HỎI MỖI GIỜ ═══
B59 = bai(
    59, 'BIẾT TẤT CẢ, HỎI MỖI GIỜ — PHÉP CHIA',
    'LV 7.1b — Bài toán ngược của năng suất: tách đều cho từng giờ.',
    video(
        ['Nhận ra bài ngược của bài năng suất.',
         'Tách đều tất cả cho từng giờ bằng phép chia.',
         'Thử lại bằng phép nhân.'],
        ['Đề bài: Cô May làm 3 giờ được tất cả 15 cái áo, giờ nào cũng như giờ nào. '
         'Hỏi mỗi giờ cô may được mấy cái áo?',
         'Bài này ngược với bài trước',
         'Bài trước biết mỗi giờ rồi hỏi tất cả. Bài này biết tất cả rồi hỏi mỗi giờ.',
         'Tách đều tất cả cho từng giờ là việc của phép chia',
         'Lấy 15 : 3 = 5.',
         'Thử lại bằng phép nhân',
         'Nhân ngược lại: 5 × 3 = 15, khớp đúng số áo của cả ba giờ.',
         'Đáp số: mỗi giờ 5 cái áo.',
         'Biết MỖI phần rồi hỏi TẤT CẢ thì nhân; biết TẤT CẢ rồi hỏi MỖI phần thì '
         'chia.'],
        ['Có bạn đọc thấy đề có chữ "mỗi giờ" là nhân luôn, lấy 15 × 3 rồi ghi bốn '
         'mươi lăm cái áo.',
         'Gợi ý 1: Đề cho biết con số nào — số áo của một giờ, hay số áo của cả ba '
         'giờ?',
         'Gợi ý 2: Cả ba giờ mới được mười lăm cái, thì một giờ phải ít hơn hay nhiều '
         'hơn mười lăm?',
         'Chữa: đề cho biết TẤT CẢ rồi hỏi MỖI phần, nên phải chia: 15 : 3 = 5.'],
        ['Nấu cơm hay gấp quần áo cùng con rồi hỏi ngược: "Cả buổi làm được ngần này, '
         'vậy mỗi lượt được bao nhiêu?"',
         'Bố mẹ hỏi: "Đề cho biết mỗi phần hay biết tất cả?"'],
    ),
    [
        lt(1, 1, 'Tính 15 : 3.', 'Lấy 15 : 3 = 5.'),
        lt(2, 1, 'Làm 3 giờ được tất cả 15 cái áo. Mỗi giờ may được mấy cái?',
           'Tách đều cho từng giờ: 15 : 3 = 5.'),
        lt(3, 1, 'Đi 4 giờ được tất cả 20 ki lô mét. Mỗi giờ đi được mấy ki lô mét?',
           'Lấy 20 : 4 = 5.'),
        lt(4, 2, 'Biết tất cả rồi hỏi mỗi phần thì dùng phép gì?',
           'Tách đều tất cả ra từng phần là việc của phép chia.'),
        lt(5, 2, 'Vòi chảy 6 phút được tất cả 18 lít. Mỗi phút chảy mấy lít?',
           'Lấy 18 : 6 = 3.'),
        lt(6, 2, 'Làm 3 giờ được 15 cái áo. Mỗi giờ mấy cái, và thử lại bằng phép nhân '
                 'được bao nhiêu?',
           'Lấy 15 : 3 = 5. Thử lại: 5 × 3 = 15.'),
        lt(7, 3, 'Đi 4 giờ được 20 ki lô mét. Hỏi mỗi giờ đi mấy ki lô mét, và đi 7 '
                 'giờ thì được mấy ki lô mét?',
           'Mỗi giờ 20 : 4 = 5 ki lô mét. Đi bảy giờ: 5 × 7 = 35 ki lô mét.'),
        lt(8, 3, 'Cô May làm 3 giờ được 15 cái áo. Hỏi mỗi giờ cô may mấy cái, và muốn '
                 'may 25 cái áo thì cô cần mấy giờ?',
           'Mỗi giờ cô may 15 : 3 = 5 cái. Muốn hai mươi lăm cái thì cần 25 : 5 = 5 '
           'giờ.'),
    ] + [
        q_tf(1, 'Biết tất cả rồi hỏi mỗi phần thì dùng phép chia.', True,
             'Đúng — tách đều ra từng phần.'),
        q_mcq(2, 'Làm 3 giờ được 15 cái áo. Mỗi giờ mấy cái?',
              ['5', '45', '12', '18'], '5', 'Tách mười lăm cho ba giờ.'),
        q_mcq(3, 'Đi 4 giờ được 20 ki lô mét. Mỗi giờ mấy ki lô mét?',
              ['5', '80', '16', '24'], '5', 'Tách hai mươi cho bốn giờ.'),
        q_tf(4, 'Thử lại bài chia bằng phép nhân là hợp lý.', True,
             'Đúng — nhân và chia ngược chiều nhau.'),
        q_tf(5, 'Bài "biết mỗi giờ, hỏi tất cả" cũng dùng phép chia.', False,
             'Sai. Bài ấy dùng phép nhân.'),
    ],
)

MOI = [B16, B54, B17, B55, B18, B56, B19, B57, B20, B58, B21, B59]

SAU = {
    'DL:KSN2.B54': 'DL:KSN2.B16',
    'DL:KSN2.B55': 'DL:KSN2.B17',
    'DL:KSN2.B56': 'DL:KSN2.B18',
    'DL:KSN2.B57': 'DL:KSN2.B19',
    'DL:KSN2.B58': 'DL:KSN2.B20',
    'DL:KSN2.B59': 'DL:KSN2.B21',
}


def _o(gt, chon=None, nhan=None):
    """Một ô nhập. Chuỗi thì BẮT BUỘC kèm nút bấm — luật ô nhập số 1 của lớp 2."""
    d = {'value': gt}
    if chon:
        d['options'] = list(chon)
    if nhan:
        d['label'] = nhan
    return d


O_NHAP_MOI = {
 # ① B16 · chia đều
 'DL:KSN2.B16#C1': {'value': 3},
 'DL:KSN2.B16#C2': {'value': 4},
 'DL:KSN2.B16#C3': {'value': 5},
 'DL:KSN2.B16#C4': {'parts': [_o(3, nhan='mấy dòng'),
                              _o('đáp số', ['lời giải', 'phép tính', 'đáp số'],
                                 'dòng thứ ba')]},
 'DL:KSN2.B16#C5': {'value': 3},
 'DL:KSN2.B16#C6': {'parts': [_o('chia đều phải dùng phép chia',
                                 ['chia đều phải dùng phép chia',
                                  'không sai gì cả'], 'sai ở đâu')]},
 'DL:KSN2.B16#C7': {'parts': [_o(6, nhan='mỗi bạn'), _o(24, nhan='thử lại được')]},
 'DL:KSN2.B16#C8': {'parts': [_o(6, nhan='chia cho 5 bạn'),
                              _o(5, nhan='chia cho 6 bạn'),
                              _o(1, nhan='ít hơn mấy quyển')]},

 # ② B54 · bài ngược
 'DL:KSN2.B54#C1': {'value': 12},
 'DL:KSN2.B54#C2': {'value': 12},
 'DL:KSN2.B54#C3': {'value': 20},
 'DL:KSN2.B54#C4': {'parts': [_o('phép nhân', ['phép nhân', 'phép chia', 'phép trừ'],
                                 'phép tính')]},
 'DL:KSN2.B54#C5': {'value': 30},
 'DL:KSN2.B54#C6': {'parts': [_o(21, nhan='tất cả'), _o(7, nhan='thử lại được')]},
 'DL:KSN2.B54#C7': {'parts': [_o(8, nhan='số bạn'), _o(32, nhan='cần mấy quyển')]},
 'DL:KSN2.B54#C8': {'parts': [_o(6, nhan='lúc đầu mỗi bạn'),
                              _o(28, nhan='khay phải có')]},

 # ③ B17 · sơ đồ hai đoạn thẳng
 'DL:KSN2.B17#C1': {'value': 9},
 'DL:KSN2.B17#C2': {'parts': [_o('Hoa', ['Hoa', 'Lan'], 'đoạn của ai dài hơn')]},
 'DL:KSN2.B17#C3': {'value': 9},
 'DL:KSN2.B17#C4': {'value': 11},
 'DL:KSN2.B17#C5': {'parts': [_o('vẽ sơ đồ xem ai dài ai ngắn',
                                 ['vẽ sơ đồ xem ai dài ai ngắn',
                                  'nhìn chữ đoán phép tính',
                                  'cộng hết các số lại'], 'việc đầu tiên')]},
 'DL:KSN2.B17#C6': {'parts': [_o(13, nhan='Hằng có'), _o(33, nhan='cả hai có')]},
 'DL:KSN2.B17#C7': {'value': 9},
 'DL:KSN2.B17#C8': {'parts': [_o(17, nhan='Mai có'), _o(13, nhan='Hùng có')]},

 # ④ B55 · bẫy câu chữ đảo
 'DL:KSN2.B55#C1': {'parts': [_o('Bình', ['Bình', 'An'], 'ai nhiều bi hơn')]},
 'DL:KSN2.B55#C2': {'value': 11},
 'DL:KSN2.B55#C3': {'value': 11},
 'DL:KSN2.B55#C4': {'value': 15},
 'DL:KSN2.B55#C5': {'parts': [_o('Bình', ['Bình', 'An'], 'ai nhiều hơn')]},
 'DL:KSN2.B55#C6': {'parts': [_o(16, nhan='Nam có'), _o(28, nhan='cả hai có')]},
 'DL:KSN2.B55#C7': {'parts': [
     _o('thấy chữ ít hơn là trừ, không hỏi ai nhiều hơn',
        ['thấy chữ ít hơn là trừ, không hỏi ai nhiều hơn', 'không sai gì cả'],
        'sai ở đâu'),
     _o(11, nhan='số đúng')]},
 'DL:KSN2.B55#C8': {'parts': [_o(15, nhan='Lan có'), _o(18, nhan='Hoa có')]},

 # ⑤ B18 · liệt kê có thứ tự
 'DL:KSN2.B18#C1': {'value': 1},
 'DL:KSN2.B18#C2': {'value': 3},
 'DL:KSN2.B18#C3': {'value': 5},
 'DL:KSN2.B18#C4': {'value': 6},
 'DL:KSN2.B18#C5': {'parts': [_o('để không sót và không kể trùng cách nào',
                                 ['để không sót và không kể trùng cách nào',
                                  'để bài trông dài hơn'], 'vì sao')]},
 'DL:KSN2.B18#C6': {'parts': [_o(7, nhan='cách đầu tiên'),
                              _o(4, nhan='cách cuối cùng')]},
 'DL:KSN2.B18#C7': {'value': 4},
 'DL:KSN2.B18#C8': {'parts': [_o(2, nhan='phần hơn giảm mấy'),
                              _o('vì một bên bớt một viên, bên kia thêm một viên',
                                 ['vì một bên bớt một viên, bên kia thêm một viên',
                                  'vì cho tròn số'], 'vì sao')]},

 # ⑥ B56 · dò cột hơn nhau
 'DL:KSN2.B56#C1': {'value': 12},
 'DL:KSN2.B56#C2': {'value': 4},
 'DL:KSN2.B56#C3': {'value': 8},
 'DL:KSN2.B56#C4': {'value': 4},
 'DL:KSN2.B56#C5': {'parts': [_o(6, nhan='anh'), _o(4, nhan='em')]},
 'DL:KSN2.B56#C6': {'parts': [_o('điều kiện phần hơn',
                                 ['điều kiện phần hơn', 'điều kiện tổng'],
                                 'quên kiểm điều kiện nào')]},
 'DL:KSN2.B56#C7': {'parts': [_o(9, nhan='bạn lớn'), _o(5, nhan='bạn bé'),
                              _o(14, nhan='thử lại tổng')]},
 'DL:KSN2.B56#C8': {'parts': [_o(6, nhan='mỗi bạn'), _o(0, nhan='phần hơn')]},

 # ⑦ B19 · vẽ theo phần
 'DL:KSN2.B19#C1': {'value': 2},
 'DL:KSN2.B19#C2': {'value': 3},
 'DL:KSN2.B19#C3': {'value': 4},
 'DL:KSN2.B19#C4': {'value': 5},
 'DL:KSN2.B19#C5': {'parts': [_o('số phần bằng nhau',
                                 ['số phần bằng nhau', 'số bạn', 'đơn vị đo'],
                                 'nói về cái gì')]},
 'DL:KSN2.B19#C6': {'parts': [_o(1, nhan='em mấy khối'), _o(2, nhan='chị mấy khối'),
                              _o(3, nhan='tất cả mấy phần')]},
 'DL:KSN2.B19#C7': {'parts': [
     _o('chị gấp đôi phần của em chứ không gấp đôi cả gói',
        ['chị gấp đôi phần của em chứ không gấp đôi cả gói', 'không sai gì cả'],
        'sai ở đâu')]},
 'DL:KSN2.B19#C8': {'value': 6},

 # ⑧ B57 · chia tổng cho số phần
 'DL:KSN2.B57#C1': {'value': 3},
 'DL:KSN2.B57#C2': {'value': 3},
 'DL:KSN2.B57#C3': {'value': 9},
 'DL:KSN2.B57#C4': {'value': 3},
 'DL:KSN2.B57#C5': {'value': 6},
 'DL:KSN2.B57#C6': {'parts': [_o(4, nhan='em'), _o(16, nhan='anh')]},
 'DL:KSN2.B57#C7': {'parts': [_o(4, nhan='con'), _o(12, nhan='bố'),
                              _o(16, nhan='thử lại tổng')]},
 'DL:KSN2.B57#C8': {'parts': [_o(5, nhan='một phần'), _o(15, nhan='cả hai có')]},

 # ⑨ B20 · tuổi sau mấy năm
 'DL:KSN2.B20#C1': {'value': 25},
 'DL:KSN2.B20#C2': {'value': 8},
 'DL:KSN2.B20#C3': {'value': 37},
 'DL:KSN2.B20#C4': {'value': 3},
 'DL:KSN2.B20#C5': {'parts': [_o('cả hai người đều thêm 2 tuổi',
                                 ['cả hai người đều thêm 2 tuổi',
                                  'chỉ người lớn thêm tuổi',
                                  'chỉ người nhỏ thêm tuổi'], 'ai thêm tuổi')]},
 'DL:KSN2.B20#C6': {'parts': [_o(8, nhan='em'), _o(11, nhan='anh')]},
 'DL:KSN2.B20#C7': {'parts': [_o(37, nhan='mẹ'), _o(12, nhan='con')]},
 'DL:KSN2.B20#C8': {'parts': [_o(25, nhan='bố hơn con'), _o(38, nhan='bố sau 3 năm'),
                              _o(13, nhan='con sau 3 năm')]},

 # ⑩ B58 · phần hơn tuổi không đổi
 'DL:KSN2.B58#C1': {'value': 3},
 'DL:KSN2.B58#C2': {'value': 3},
 'DL:KSN2.B58#C3': {'parts': [_o('không', CO_KHONG, 'có đổi không')]},
 'DL:KSN2.B58#C4': {'value': 3},
 'DL:KSN2.B58#C5': {'value': 25},
 'DL:KSN2.B58#C6': {'parts': [_o('tưởng chỉ mình anh thêm tuổi',
                                 ['tưởng chỉ mình anh thêm tuổi', 'không sai gì cả'],
                                 'sai ở đâu')]},
 'DL:KSN2.B58#C7': {'parts': [_o(25, nhan='sau 5 năm'), _o(25, nhan='cách đây 2 năm')]},
 'DL:KSN2.B58#C8': {'parts': [_o(11, nhan='anh năm nay'),
                              _o(4, nhan='sau 6 năm hơn mấy')]},

 # ⑪ B21 · biết mỗi giờ, hỏi tất cả
 'DL:KSN2.B21#C1': {'value': 12},
 'DL:KSN2.B21#C2': {'value': 12},
 'DL:KSN2.B21#C3': {'value': 15},
 'DL:KSN2.B21#C4': {'value': 12},
 'DL:KSN2.B21#C5': {'parts': [
     _o('cộng ki lô mét với giờ là cộng hai thứ khác loại',
        ['cộng ki lô mét với giờ là cộng hai thứ khác loại', 'không sai gì cả'],
        'sai ở đâu')]},
 'DL:KSN2.B21#C6': {'value': 24},
 'DL:KSN2.B21#C7': {'parts': [_o(12, nhan='sau 4 phút'), _o(21, nhan='sau 7 phút')]},
 'DL:KSN2.B21#C8': {'parts': [_o('phép nhân', ['phép nhân', 'phép cộng'],
                                 'phép tính chung'),
                              _o(15, nhan='cô May'), _o(12, nhan='bác Tài')]},

 # ⑫ B59 · biết tất cả, hỏi mỗi giờ
 'DL:KSN2.B59#C1': {'value': 5},
 'DL:KSN2.B59#C2': {'value': 5},
 'DL:KSN2.B59#C3': {'value': 5},
 'DL:KSN2.B59#C4': {'parts': [_o('phép chia', ['phép chia', 'phép nhân', 'phép trừ'],
                                 'phép tính')]},
 'DL:KSN2.B59#C5': {'value': 3},
 'DL:KSN2.B59#C6': {'parts': [_o(5, nhan='mỗi giờ'), _o(15, nhan='thử lại được')]},
 'DL:KSN2.B59#C7': {'parts': [_o(5, nhan='mỗi giờ'), _o(35, nhan='đi 7 giờ')]},
 'DL:KSN2.B59#C8': {'parts': [_o(5, nhan='mỗi giờ'), _o(5, nhan='cần mấy giờ')]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (16, 17, 18, 19, 20, 21)}
    moi_ = {f'DL:KSN2.B{n}' for n in (54, 55, 56, 57, 58, 59)}
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
        # "km" đọc thành tiếng Anh; viết chữ ra như đã làm ở lớp 4.
        if ' km' in van or 'km ' in van:
            loi.append(f'{b["id"]}: còn viết tắt "km" — phải viết "ki lô mét"')
    NEO = {'DL:KSN2.B16': '15 : 5 = 3', 'DL:KSN2.B54': '4 × 3 = 12',
           'DL:KSN2.B17': '14 − 5 = 9', 'DL:KSN2.B55': '8 + 3 = 11',
           'DL:KSN2.B18': '11 và 1', 'DL:KSN2.B56': '8 − 4 = 4',
           'DL:KSN2.B19': '1 + 3 = 4', 'DL:KSN2.B57': '12 : 4 = 3',
           'DL:KSN2.B20': '32 − 7 = 25', 'DL:KSN2.B58': '11 − 8 = 3',
           'DL:KSN2.B21': '3 × 4 = 12', 'DL:KSN2.B59': '15 : 3 = 5'}
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
        print(f"  {b['id']}  {b['ten'][:54]:54} {n} luyện + {q} quiz")
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
