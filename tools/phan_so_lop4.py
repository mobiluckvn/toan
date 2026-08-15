# -*- coding: utf-8 -*-
"""CHƯƠNG 9 · PHÂN SỐ — năm bài cũ tách thành MƯỜI MỘT.

Chương gói nặng nhất từ trước tới nay:
  · B38 gộp so sánh cùng mẫu / cùng tử / so với 1 **với** phần bù, phần hơn, phân số
    trung gian — sáu kỹ thuật trong một bài;
  · B39 gộp tìm phân số của một số **với** bài toán ngược **với** đổi đơn vị gốc;
  · B40 gộp tổng tách hiệu **với** tích rút gọn chéo — hai kỹ thuật chẳng liên quan;
  · B41 gộp cùng thêm hai đầu (hiệu không đổi) **với** chuyển giữa hai đầu (tổng
    không đổi) — đúng hai điều bé hay lẫn nhất, mà lại dạy chung một chỗ;
  · B42 gộp ba ứng dụng: lãi, bay hơi, pha trộn.
Và như mọi chương trước: **không bài nào nói phân số là gì**, vào thẳng so sánh.

── BỘ NEO: PHÂN SỐ 3/4 ──
Một mình nó chở gần cả chương, và mọi con số đã kiểm bằng máy trước khi viết:

    3/4 so với 2/3   → quy đồng mẫu 12 được 9/12 và 8/12
    3/4 của 20       → 15
    1/(1×2) + 1/(2×3) + 1/(3×4)  →  đúng bằng 3/4
    1/2 × 2/3 × 3/4  → 1/4
    3/4 thêm 2 ở hai đầu → 5/6, hiệu mẫu trừ tử vẫn là 1
    3/4 chuyển 1 từ mẫu sang tử → 4/3, tổng tử cộng mẫu vẫn là 7

── KIỂU CẢNH MỚI ──
`phan_so` vẽ băng chia phần, tô phần đã lấy. Cả chương đứng hay đổ ở chỗ này: bé
phải THẤY mẫu số là "chia làm mấy phần", tử số là "lấy mấy phần". Nói bằng lời thì
tử với mẫu chỉ là hai cái tên khó nhớ.

    python3 tools/phan_so_lop4.py --xem
    python3 tools/phan_so_lop4.py
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

TEN_CHUONG = 'PHÂN SỐ'
CHUONG = 9
CO_KHONG = ['có', 'không']

LUI_PHAN = {'ve': ['DL:KSN3.B09'], 'ten': ['TÌM MỘT PHẦN MẤY CỦA MỘT SỐ'],
            'canCu': 'chuDe', 'lopDuoi': 3}
LUI_DAY = {'ve': ['DL:KSN3.B12', 'DL:KSN3.B09'],
           'ten': ['FIBONACCI & QUY LUẬT HAI TẦNG', 'TÌM MỘT PHẦN MẤY CỦA MỘT SỐ'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_BANG = {'ve': ['DL:KSN3.B19'], 'ten': ['THÊM BỚT ĐỂ BẰNG NHAU'],
            'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B68 · PHÂN SỐ LÀ GÌ — bài KHÁI NIỆM
# ═══════════════════════════════════════════════════════════════════════════
B68 = bai(
    68, 'PHÂN SỐ LÀ GÌ — MẪU SỐ CHIA MẤY PHẦN, TỬ SỐ LẤY MẤY PHẦN',
    'Dạng gốc: PS 1.0 mức Lớp 4 — Khái niệm phân số, tên gọi tử số và mẫu số, cách '
    'đọc và cách vẽ ra băng chia phần. KHÔNG so sánh, KHÔNG tính toán.',
    'Lớp 3 con đã tìm "một phần mấy của một số". Hôm nay con gọi đúng tên cái "một '
    'phần mấy" ấy: nó là phân số. Và con sẽ thấy hai con số trong phân số nói hai '
    'việc khác nhau, không phải hai con số cùng loại.',
    LUI_PHAN,
    video(
        ['Gọi đúng tên tử số và mẫu số.',
         'Nói được mẫu số là chia làm mấy phần, tử số là lấy mấy phần.',
         'Vẽ được một phân số ra thành băng chia phần.'],
        ['Đề bài: Chia một cái băng giấy thành 4 phần bằng nhau rồi lấy 3 phần. Viết '
         'phân số chỉ phần đã lấy và gọi tên hai con số trong đó.',
         'Chia băng ra',
         'Chia băng giấy thành 4 phần bằng nhau. Phải BẰNG NHAU thì mới đúng.',
         'Lấy phần',
         'Tô 3 phần trong 4 phần ấy. Phần đã tô viết thành phân số ba phần tư.',
         'Gọi tên hai con số',
         'Số 4 viết dưới gọi là MẪU SỐ, nó cho biết chia làm mấy phần.',
         'Số 3 viết trên gọi là TỬ SỐ, nó cho biết lấy mấy phần.',
         'Hai số nói hai việc khác nhau',
         'Mẫu số nói về việc chia, tử số nói về việc lấy. Đổi chỗ chúng là ra phân số '
         'khác hẳn.',
         'Đáp số: phân số là ba phần tư; 3 là tử số, 4 là mẫu số.'],
        ['Có bạn chia băng giấy thành 4 phần nhưng các phần to nhỏ khác nhau.',
         'Gợi ý 1: Con đo thử bốn phần ấy xem có bằng nhau không?',
         'Gợi ý 2: Không bằng nhau thì "một phần" là phần nào, phần to hay phần nhỏ?',
         'Chữa: các phần phải BẰNG NHAU thì phân số mới có nghĩa. Chia to nhỏ khác '
         'nhau thì không nói được "ba phần tư" là bao nhiêu.'],
        ['Gấp một tờ giấy làm bốn phần bằng nhau rồi tô ba phần. Con nhìn thấy ba phần '
         'tư thì hai chữ tử với mẫu thôi khó nhớ.',
         'Con hay lẫn tử với mẫu. Bố mẹ nhắc một câu: số ở DƯỚI nói chia làm mấy phần.'],
    ),
    [
        lt(1, 1, 'Chia băng giấy thành 4 phần bằng nhau, tô 3 phần — đúng bài trong '
                 'video. Mẫu số của phân số ấy là số mấy?',
           'Mẫu số là 4 — nó cho biết chia làm 4 phần.'),
        lt(2, 1, 'Vẫn bài trên. Tử số là số mấy và nó cho biết điều gì?',
           'Tử số là 3, nó cho biết đã lấy 3 phần.'),
        lt(3, 1, 'Chia một cái bánh thành 5 phần bằng nhau rồi ăn 2 phần. Viết phân số '
                 'chỉ phần đã ăn.',
           'Phân số là hai phần năm: tử số 2, mẫu số 5.'),
        lt(4, 2, 'Bạn Nam chia băng giấy thành 4 phần nhưng to nhỏ khác nhau. Bạn sai ở '
                 'đâu?',
           'Các phần phải BẰNG NHAU thì phân số mới có nghĩa. Chia to nhỏ khác nhau thì '
           'không nói được một phần là bao nhiêu.'),
        lt(5, 2, 'Phân số ba phần tư và phân số bốn phần ba có giống nhau không? Vì sao?',
           'KHÔNG giống. Ba phần tư là chia 4 lấy 3, còn bốn phần ba là chia 3 lấy 4. '
           'Đổi chỗ tử và mẫu là ra phân số khác hẳn.'),
        lt(6, 2, 'Một lớp có 30 bạn, trong đó 7 bạn đeo kính. Viết phân số chỉ số bạn '
                 'đeo kính so với cả lớp.',
           'Phân số là bảy phần ba mươi: tử số 7, mẫu số 30.'),
        lt(7, 2, 'Nhìn một băng chia 6 phần bằng nhau, tô 6 phần. Phân số ấy bằng bao nhiêu?',
           'Sáu phần sáu — tô hết cả băng, nên nó bằng 1.'),
        lt(8, 3, 'Chia băng giấy thành 8 phần bằng nhau rồi tô 4 phần. Con thấy phần đã '
                 'tô bằng bao nhiêu phần của cả băng?',
           'Bốn phần tám, tức đúng một nửa băng. Bốn phần tám và một phần hai tô cùng '
           'một chỗ.'),
        lt(9, 3, 'Vẽ hai băng dài bằng nhau: băng một chia 4 phần tô 3 phần, băng hai '
                 'chia 8 phần tô 6 phần. Hai phần tô có bằng nhau không?',
           'Bằng nhau. Ba phần tư và sáu phần tám tô đúng cùng một chỗ trên băng.'),
        q_tf(1, 'Mẫu số cho biết chia làm mấy phần bằng nhau.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Các phần chia ra có thể to nhỏ khác nhau.', False,
             'SAI — phải bằng nhau thì phân số mới có nghĩa.'),
        q_mcq(3, 'Trong phân số ba phần tư, số 4 là:',
              ['A. mẫu số', 'B. tử số', 'C. thương'], 'A. mẫu số', 'Số viết ở dưới.'),
        q_mcq(4, 'Tử số cho biết:',
              ['A. lấy mấy phần', 'B. chia làm mấy phần', 'C. còn lại mấy phần'],
              'A. lấy mấy phần', 'Số viết ở trên.'),
        q_mcq(5, 'Băng chia 6 phần, tô cả 6 phần thì phân số bằng:',
              ['A. 1', 'B. 6', 'C. 0'], 'A. 1', 'Tô hết cả băng.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B38 · SO SÁNH CÙNG MẪU HOẶC CÙNG TỬ  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ nhồi sáu kỹ thuật so sánh. Nay chỉ còn hai trường hợp DỄ NHÌN NHẤT, và cả
# hai đều giải thích được bằng hình chứ không phải bằng quy tắc.
B38 = bai(
    38, 'SO SÁNH CÙNG MẪU HOẶC CÙNG TỬ — NHÌN HÌNH LÀ THẤY',
    'Dạng gốc: PS 1.1 mức Lớp 4 — So sánh hai phân số cùng mẫu số hoặc cùng tử số, '
    'giải thích bằng băng chia phần.',
    'Bài trước con đã vẽ được phân số ra thành băng. Hôm nay con so hai băng với nhau '
    '— nhưng chỉ hai trường hợp dễ nhất, là khi chúng chia giống nhau hoặc lấy giống '
    'nhau. Hai trường hợp ấy nhìn hình là thấy, không cần nhớ quy tắc nào.',
    LUI_PHAN,
    video(
        ['So sánh được hai phân số cùng mẫu số.',
         'So sánh được hai phân số cùng tử số.',
         'Giải thích được vì sao, dựa vào băng chia phần.'],
        ['Đề bài: So sánh hai phân số ba phần tư và hai phần tư. Rồi so sánh ba phần tư '
         'và ba phần năm.',
         'Trường hợp cùng mẫu số',
         'Ba phần tư và hai phần tư đều chia băng làm 4 phần. Phần chia giống hệt nhau.',
         'Nên chỉ cần đếm số phần lấy',
         'Một bên lấy 3 phần, một bên lấy 2 phần. Lấy nhiều hơn thì lớn hơn, nên ba '
         'phần tư lớn hơn hai phần tư.',
         'Trường hợp cùng tử số',
         'Ba phần tư và ba phần năm đều lấy 3 phần. Nhưng phần của bên nào TO hơn?',
         'Chia ít thì mỗi phần to',
         'Chia làm 4 phần thì mỗi phần to hơn chia làm 5 phần. Cùng lấy 3 phần mà phần '
         'to hơn thì được nhiều hơn.',
         'Nên ba phần tư lớn hơn ba phần năm.',
         'Đáp số: ba phần tư lớn hơn hai phần tư, và ba phần tư cũng lớn hơn ba phần năm.'],
        ['Có bạn thấy ba phần năm có mẫu số 5 lớn hơn 4, nên bảo ba phần năm lớn hơn ba '
         'phần tư.',
         'Gợi ý 1: Chia bánh cho 5 người và chia cho 4 người, ai được miếng to hơn?',
         'Gợi ý 2: Chia cho ít người thì miếng to hơn chứ.',
         'Chữa: mẫu số CÀNG LỚN thì mỗi phần CÀNG NHỎ. Cùng lấy 3 phần thì ba phần tư '
         'lớn hơn ba phần năm.'],
        ['Cắt hai băng giấy dài bằng nhau, một chia 4 phần một chia 5 phần. Con đặt '
         'chồng lên nhau là thấy ngay phần nào to hơn.',
         'Chỗ con hay nhầm là tưởng mẫu số lớn thì phân số lớn. Bố mẹ hỏi: "Chia cho '
         'nhiều người thì miếng to hay nhỏ?"'],
    ),
    [
        lt(1, 1, 'So sánh ba phần tư và hai phần tư — đúng bài trong video. Hai phân số '
                 'này giống nhau ở chỗ nào?',
           'Giống mẫu số: cả hai đều chia băng làm 4 phần.'),
        lt(2, 1, 'Vẫn hai phân số ấy. Phân số nào lớn hơn và vì sao?',
           'Ba phần tư lớn hơn, vì chia giống nhau mà lấy nhiều phần hơn.'),
        lt(3, 1, 'So sánh ba phần tư và ba phần năm. Hai phân số này giống nhau ở chỗ nào?',
           'Giống tử số: cả hai đều lấy 3 phần.'),
        lt(4, 2, 'Vẫn hai phân số ấy. Phân số nào lớn hơn và vì sao?',
           'Ba phần tư lớn hơn. Chia làm 4 phần thì mỗi phần to hơn chia làm 5 phần, '
           'mà cùng lấy 3 phần.'),
        lt(5, 2, 'Bạn Lan thấy mẫu số 5 lớn hơn 4 nên bảo ba phần năm lớn hơn ba phần '
                 'tư. Bạn sai ở đâu?',
           'Mẫu số càng lớn thì mỗi phần càng NHỎ. Chia cho nhiều người thì miếng bé đi.'),
        lt(6, 2, 'So sánh năm phần tám và bảy phần tám.',
           'Cùng mẫu số 8, bên nào lấy nhiều phần hơn thì lớn hơn. Bảy phần tám lớn hơn.'),
        lt(7, 2, 'So sánh hai phần ba và hai phần bảy.',
           'Cùng tử số 2. Chia làm 3 phần thì mỗi phần to hơn chia làm 7 phần, nên hai '
           'phần ba lớn hơn.'),
        lt(8, 3, 'Sắp xếp ba phân số sau từ bé đến lớn: một phần tư, ba phần tư, hai '
                 'phần tư.',
           'Cùng mẫu số nên chỉ so tử số: một phần tư, hai phần tư, ba phần tư.'),
        lt(9, 3, 'Sắp xếp ba phân số sau từ bé đến lớn: ba phần tư, ba phần năm, ba '
                 'phần tám.',
           'Cùng tử số nên mẫu càng lớn phân số càng bé: ba phần tám, ba phần năm, ba '
           'phần tư.'),
        q_tf(1, 'Hai phân số cùng mẫu số thì tử số lớn hơn là phân số lớn hơn.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Hai phân số cùng tử số thì mẫu số lớn hơn là phân số lớn hơn.', False,
             'SAI — mẫu càng lớn thì mỗi phần càng nhỏ.'),
        q_mcq(3, 'So sánh ba phần tư và hai phần tư:',
              ['A. ba phần tư lớn hơn', 'B. hai phần tư lớn hơn', 'C. bằng nhau'],
              'A. ba phần tư lớn hơn', 'Cùng mẫu, lấy nhiều phần hơn.'),
        q_mcq(4, 'So sánh ba phần tư và ba phần năm:',
              ['A. ba phần tư lớn hơn', 'B. ba phần năm lớn hơn', 'C. bằng nhau'],
              'A. ba phần tư lớn hơn', 'Cùng tử, mẫu bé thì phần to.'),
        q_mcq(5, 'Mẫu số càng lớn thì mỗi phần:',
              ['A. càng nhỏ', 'B. càng to', 'C. không đổi'], 'A. càng nhỏ',
              'Chia cho nhiều người thì miếng bé đi.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B69 · QUY ĐỒNG MẪU SỐ ĐỂ SO SÁNH
# ═══════════════════════════════════════════════════════════════════════════
B69 = bai(
    69, 'QUY ĐỒNG MẪU SỐ — CHIA LẠI CHO HAI BĂNG GIỐNG NHAU',
    'Dạng gốc: PS 1.2 mức Lớp 4 — Quy đồng mẫu số hai phân số rồi so sánh; giải thích '
    'bằng việc chia lại băng cho khớp nhau.',
    'Bài trước con so được hai trường hợp dễ. Nhưng ba phần tư với hai phần ba thì '
    'khác mẫu, khác cả tử — nhìn không ra. Hôm nay con học cách làm cho hai băng chia '
    'GIỐNG NHAU, rồi lại so như bài dễ.',
    LUI_PHAN,
    video(
        ['Tìm được mẫu số chung của hai phân số.',
         'Đổi hai phân số về cùng mẫu mà không làm đổi giá trị.',
         'So sánh sau khi đã quy đồng.'],
        ['Đề bài: So sánh hai phân số ba phần tư và hai phần ba.',
         'Vì sao nhìn không ra',
         'Một băng chia 4 phần, băng kia chia 3 phần. Phần của hai băng to nhỏ khác '
         'nhau nên không đếm chung được.',
         'Chia lại cho giống nhau',
         'Tìm một số chia hết cho cả 4 và 3. Số gọn nhất là 12. Ta chia lại cả hai băng '
         'thành 12 phần.',
         'Đổi phân số thứ nhất',
         'Băng chia 4 phần nay chia thành 12 phần, tức mỗi phần cũ tách làm 3. Nên 3 '
         'phần cũ thành 9 phần mới: ba phần tư bằng chín phần mười hai.',
         'Đổi phân số thứ hai',
         'Băng chia 3 phần nay chia thành 12 phần, mỗi phần cũ tách làm 4. Nên 2 phần '
         'cũ thành 8 phần mới: hai phần ba bằng tám phần mười hai.',
         'Bây giờ cùng mẫu rồi',
         'Chín phần mười hai lớn hơn tám phần mười hai, nên ba phần tư lớn hơn hai phần ba.',
         'Đáp số: ba phần tư lớn hơn hai phần ba.'],
        ['Có bạn quy đồng mẫu nhưng quên đổi tử: viết ba phần tư thành ba phần mười hai.',
         'Gợi ý 1: Nếu chia lại băng thành nhiều phần hơn mà vẫn tô ba phần thì phần tô '
         'có còn như cũ không?',
         'Gợi ý 2: Bé đi mất rồi. Vậy tử số phải làm sao?',
         'Chữa: nhân mẫu với mấy thì nhân tử với bấy nhiêu. Ba phần tư thành CHÍN phần '
         'mười hai, không phải ba phần mười hai.'],
        ['Gấp hai băng giấy: một gấp 4, một gấp 3, rồi gấp thêm cho cả hai thành 12 ô. '
         'Con nhìn thấy phần tô không đổi, chỉ ô nhỏ đi.',
         'Chỗ sai duy nhất là quên nhân tử số. Bố mẹ hỏi: "Nhân mẫu mấy lần thì tử mấy lần?"'],
    ),
    [
        lt(1, 1, 'So sánh ba phần tư và hai phần ba — đúng bài trong video. Vì sao chưa '
                 'so được ngay?',
           'Vì hai băng chia khác nhau: một chia 4 phần, một chia 3 phần, nên phần của '
           'chúng to nhỏ khác nhau.'),
        lt(2, 1, 'Vẫn bài trên. Số nào chia hết cho cả 4 và 3, và gọn nhất là số mấy?',
           'Số 12 — đó là mẫu số chung gọn nhất.'),
        lt(3, 1, 'Vẫn bài trên. Ba phần tư đổi thành mấy phần mười hai?',
           'Nhân cả tử và mẫu với 3: ba phần tư bằng chín phần mười hai.'),
        lt(4, 2, 'Vẫn bài trên. Hai phần ba đổi thành mấy phần mười hai, và phân số nào '
                 'lớn hơn?',
           'Nhân cả tử và mẫu với 4: hai phần ba bằng tám phần mười hai. Vậy ba phần tư '
           'lớn hơn.'),
        lt(5, 2, 'Bạn Bình viết ba phần tư thành ba phần mười hai. Bạn sai ở đâu?',
           'Nhân mẫu với 3 thì phải nhân tử với 3, được chín phần mười hai. Quên nhân tử '
           'là làm phân số bé đi.'),
        lt(6, 2, 'Quy đồng rồi so sánh hai phần năm và một phần hai.',
           'Mẫu chung 10: hai phần năm bằng bốn phần mười, một phần hai bằng năm phần '
           'mười. Vậy một phần hai lớn hơn.'),
        lt(7, 2, 'Vì sao nhân cả tử và mẫu với cùng một số thì phân số không đổi?',
           'Vì chia lại băng thành nhiều ô nhỏ hơn nhưng phần tô vẫn nguyên chỗ ấy. Số '
           'ô tăng lên bao nhiêu lần thì số ô đã tô cũng tăng bấy nhiêu lần.'),
        lt(8, 3, 'So sánh ba phần tư và năm phần sáu.',
           'Mẫu chung 12: ba phần tư bằng chín phần mười hai, năm phần sáu bằng mười '
           'phần mười hai. Vậy năm phần sáu lớn hơn.'),
        lt(9, 3, 'Sắp xếp từ bé đến lớn: một phần hai, hai phần ba, ba phần tư.',
           'Mẫu chung 12: được sáu phần mười hai, tám phần mười hai, chín phần mười hai. '
           'Thứ tự: một phần hai, hai phần ba, ba phần tư.'),
        q_tf(1, 'Nhân cả tử và mẫu với cùng một số thì phân số không đổi.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Quy đồng mẫu số thì chỉ cần đổi mẫu, giữ nguyên tử.', False,
             'SAI — nhân mẫu mấy lần thì nhân tử bấy nhiêu lần.'),
        q_mcq(3, 'Mẫu số chung gọn nhất của 4 và 3 là:',
              ['A. 12', 'B. 7', 'C. 24'], 'A. 12', 'Số nhỏ nhất chia hết cho cả hai.'),
        q_mcq(4, 'Ba phần tư đổi ra mẫu 12 thì thành:',
              ['A. chín phần mười hai', 'B. ba phần mười hai', 'C. bốn phần mười hai'],
              'A. chín phần mười hai', 'Nhân cả tử và mẫu với 3.'),
        q_mcq(5, 'So sánh ba phần tư và hai phần ba:',
              ['A. ba phần tư lớn hơn', 'B. hai phần ba lớn hơn', 'C. bằng nhau'],
              'A. ba phần tư lớn hơn', 'Chín phần mười hai lớn hơn tám phần mười hai.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B70 · SO VỚI 1 VÀ PHẦN BÙ — mẹo so nhanh
# ═══════════════════════════════════════════════════════════════════════════
B70 = bai(
    70, 'SO VỚI 1 VÀ PHẦN BÙ — HAI CÁCH SO NHANH KHÔNG CẦN QUY ĐỒNG',
    'Dạng gốc: PS 1.3 mức Lớp 4 — So sánh phân số bằng cách so với 1 và bằng cách so '
    'phần còn thiếu.',
    'Quy đồng thì lúc nào cũng làm được, nhưng đôi khi hơi lâu. Hôm nay con học hai '
    'cách nhìn rất nhanh — và cả hai đều nhìn hình mà ra, không phải mẹo học thuộc.',
    LUI_PHAN,
    video(
        ['So một phân số với 1 để biết nó lớn hay bé hơn.',
         'So hai phân số bằng phần còn thiếu để đầy băng.',
         'Biết khi nào dùng được cách nhanh, khi nào phải quy đồng.'],
        ['Đề bài: So sánh năm phần tư với ba phần bốn. Rồi so sánh ba phần tư với bốn '
         'phần năm.',
         'Cách một, so với 1',
         'Phân số nào có tử LỚN HƠN mẫu thì lớn hơn 1, vì đã tô quá cả băng. Năm phần '
         'tư như thế.',
         'Phân số nào có tử BÉ HƠN mẫu thì bé hơn 1. Ba phần bốn như thế.',
         'Một bên lớn hơn 1, một bên bé hơn 1, nên năm phần tư lớn hơn ba phần bốn.',
         'Cách hai, so phần còn thiếu',
         'Ba phần tư còn thiếu một phần tư nữa thì đầy băng. Bốn phần năm còn thiếu một '
         'phần năm.',
         'Bên nào thiếu ÍT hơn thì đầy hơn',
         'Một phần năm bé hơn một phần tư, nên bốn phần năm thiếu ít hơn, tức lớn hơn.',
         'Đáp số: năm phần tư lớn hơn ba phần bốn; và bốn phần năm lớn hơn ba phần tư.'],
        ['Có bạn thấy ba phần tư và bốn phần năm đều thiếu MỘT phần nên bảo hai phân số '
         'bằng nhau.',
         'Gợi ý 1: Một phần tư và một phần năm có bằng nhau không?',
         'Gợi ý 2: Một phần năm bé hơn chứ, vì chia làm 5 phần thì mỗi phần bé hơn.',
         'Chữa: đều thiếu một PHẦN, nhưng phần ấy to nhỏ khác nhau. Thiếu phần bé hơn '
         'thì đầy hơn, nên bốn phần năm lớn hơn.'],
        ['Cắt hai băng giấy, tô ba phần tư và bốn phần năm, rồi hỏi con: "Băng nào còn '
         'trống ít hơn?" Trống ít hơn là lớn hơn.',
         'Đây là mẹo nhìn nhanh, nhưng chỉ dùng được khi hai phân số cùng thiếu MỘT '
         'phần. Không thì cứ quy đồng cho chắc.'],
    ),
    [
        lt(1, 1, 'Phân số năm phần tư lớn hơn hay bé hơn 1? Vì sao?',
           'Lớn hơn 1, vì tử số 5 lớn hơn mẫu số 4 — đã tô quá cả băng.'),
        lt(2, 1, 'Phân số ba phần bốn lớn hơn hay bé hơn 1?',
           'Bé hơn 1, vì tử số 3 bé hơn mẫu số 4.'),
        lt(3, 1, 'Ba phần tư còn thiếu bao nhiêu nữa thì đầy băng?',
           'Thiếu một phần tư.'),
        lt(4, 2, 'Bốn phần năm còn thiếu bao nhiêu, và so với ba phần tư thì phân số nào '
                 'lớn hơn?',
           'Thiếu một phần năm. Một phần năm bé hơn một phần tư nên bốn phần năm thiếu '
           'ít hơn, tức lớn hơn ba phần tư.'),
        lt(5, 2, 'Bạn Tú thấy cả hai đều thiếu MỘT phần nên bảo chúng bằng nhau. Bạn sai '
                 'ở đâu?',
           'Đều thiếu một phần nhưng phần ấy to nhỏ khác nhau. Một phần năm bé hơn một '
           'phần tư nên bốn phần năm lớn hơn.'),
        lt(6, 2, 'Không quy đồng, hãy so sánh bảy phần sáu với năm phần bảy.',
           'Bảy phần sáu có tử lớn hơn mẫu nên lớn hơn 1. Năm phần bảy có tử bé hơn mẫu '
           'nên bé hơn 1. Vậy bảy phần sáu lớn hơn.'),
        lt(7, 2, 'Không quy đồng, hãy so sánh năm phần sáu với sáu phần bảy.',
           'Năm phần sáu thiếu một phần sáu; sáu phần bảy thiếu một phần bảy. Một phần '
           'bảy bé hơn nên sáu phần bảy lớn hơn.'),
        lt(8, 3, 'Trong ba phân số sau, phân số nào lớn hơn 1: hai phần ba, năm phần '
                 'năm, chín phần tám?',
           'Chín phần tám lớn hơn 1 (tử lớn hơn mẫu). Năm phần năm bằng đúng 1. Hai phần '
           'ba bé hơn 1.'),
        lt(9, 3, 'Cách so phần bù dùng được khi nào, và khi nào phải quy đồng?',
           'Dùng được khi hai phân số cùng thiếu ĐÚNG MỘT phần để đầy băng. Trường hợp '
           'khác thì cứ quy đồng cho chắc.'),
        q_tf(1, 'Phân số có tử lớn hơn mẫu thì lớn hơn 1.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Hai phân số cùng thiếu một phần thì bằng nhau.', False,
             'SAI — phần thiếu ấy to nhỏ khác nhau.'),
        q_mcq(3, 'Phân số năm phần năm bằng:',
              ['A. 1', 'B. 5', 'C. 0'], 'A. 1', 'Tô hết cả băng.'),
        q_mcq(4, 'Ba phần tư và bốn phần năm, phân số nào lớn hơn?',
              ['A. bốn phần năm', 'B. ba phần tư', 'C. bằng nhau'],
              'A. bốn phần năm', 'Nó thiếu ít hơn.'),
        q_mcq(5, 'Cách so phần bù dùng được khi:',
              ['A. hai phân số cùng thiếu đúng một phần',
               'B. hai phân số cùng mẫu', 'C. lúc nào cũng dùng được'],
              'A. hai phân số cùng thiếu đúng một phần',
              'Trường hợp khác thì quy đồng.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B39 · TÌM PHÂN SỐ CỦA MỘT SỐ  (mã cũ, viết lại — chỉ còn chiều thuận)
# ═══════════════════════════════════════════════════════════════════════════
B39 = bai(
    39, 'TÌM PHÂN SỐ CỦA MỘT SỐ — CHIA RỒI NHÂN',
    'Dạng gốc: PS 4.1 mức Lớp 4 — Tìm ba phần tư của một số, dựa trên việc chia thành '
    'phần rồi lấy mấy phần.',
    'Con đã biết mẫu số là chia mấy phần, tử số là lấy mấy phần. Hôm nay con làm đúng '
    'hai việc ấy trên một con số thật: chia nó ra rồi lấy về mấy phần.',
    LUI_PHAN,
    video(
        ['Chia một số thành số phần bằng mẫu số.',
         'Lấy về số phần bằng tử số.',
         'Làm được hai bước ấy theo đúng thứ tự.'],
        ['Đề bài: Tìm ba phần tư của số 20.',
         'Đọc phân số ra thành việc làm',
         'Ba phần tư nghĩa là chia làm 4 phần rồi lấy 3 phần.',
         'Bước một, chia',
         'Chia 20 thành 4 phần bằng nhau: 20 : 4 = 5. Mỗi phần là 5.',
         'Bước hai, lấy',
         'Lấy 3 phần: 3 × 5 = 15.',
         'Vẽ ra thì thấy',
         'Băng 20 chia làm 4 ô, mỗi ô 5. Tô 3 ô thì được 15.',
         'Đáp số: ba phần tư của 20 là 15.'],
        ['Có bạn làm ngược thứ tự: nhân 20 với 4 rồi chia cho 3.',
         'Gợi ý 1: Ba phần tư của 20 thì phải bé hơn hay lớn hơn 20?',
         'Gợi ý 2: Bé hơn chứ, vì chỉ lấy có 3 trong 4 phần thôi.',
         'Chữa: phải CHIA cho mẫu số rồi NHÂN với tử số. Làm ngược thì ra số lớn hơn '
         '20, mà lấy một phần của 20 thì không thể lớn hơn 20.'],
        ['Lấy 20 hạt đậu, chia thành 4 nhóm rồi bảo con lấy 3 nhóm. Con đếm được 15 hạt '
         'thì đã hiểu.',
         'Cách soi rất nhanh: lấy một phần của số thì kết quả phải BÉ HƠN số ấy. Ra lớn '
         'hơn là chắc chắn sai.'],
    ),
    [
        lt(1, 1, 'Tìm ba phần tư của 20 — đúng bài trong video. Chia 20 thành 4 phần thì '
                 'mỗi phần bằng bao nhiêu?',
           '20 : 4 = 5.'),
        lt(2, 1, 'Vẫn bài trên. Lấy 3 phần thì được bao nhiêu?',
           '3 × 5 = 15.'),
        lt(3, 1, 'Tìm một phần hai của 30.',
           '30 : 2 = 15, rồi 1 × 15 = 15.'),
        lt(4, 2, 'Bạn Hoa nhân 20 với 4 rồi chia cho 3. Vì sao chắc chắn sai?',
           'Lấy một phần của 20 thì kết quả phải BÉ HƠN 20. Bạn làm ngược thứ tự nên ra '
           'số lớn hơn.'),
        lt(5, 2, 'Tìm hai phần năm của 45.',
           '45 : 5 = 9, rồi 2 × 9 = 18.'),
        lt(6, 2, 'Một lớp có 32 bạn, ba phần tư số bạn là nữ. Lớp có bao nhiêu bạn nữ?',
           '32 : 4 = 8, rồi 3 × 8 = 24 bạn nữ.'),
        lt(7, 2, 'Vì sao phải chia trước rồi mới nhân?',
           'Vì mẫu số nói chia làm mấy phần, phải chia ra mới biết một phần bằng bao '
           'nhiêu. Có một phần rồi mới nhân lên theo tử số.'),
        lt(8, 3, 'Một mảnh vườn 60 mét vuông, người ta trồng rau trên ba phần năm mảnh '
                 'vườn. Diện tích trồng rau là bao nhiêu?',
           '60 : 5 = 12, rồi 3 × 12 = 36 mét vuông.'),
        lt(9, 3, 'Tìm ba phần tư của 20, rồi tìm hai phần ba của kết quả vừa được.',
           'Ba phần tư của 20: 20 : 4 = 5, rồi 3 × 5 = 15. Hai phần ba của 15: '
           '15 : 3 = 5, rồi 2 × 5 = 10.'),
        q_tf(1, 'Tìm phân số của một số thì chia cho mẫu rồi nhân với tử.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Ba phần tư của 20 lớn hơn 20.', False,
             'SAI — lấy một phần của số thì bé hơn số ấy.'),
        q_mcq(3, 'Ba phần tư của 20 bằng:',
              ['A. 15', 'B. 26', 'C. 5'], 'A. 15', '20 : 4 = 5, rồi 3 × 5 = 15.'),
        q_mcq(4, 'Hai phần năm của 45 bằng:',
              ['A. 18', 'B. 9', 'C. 22'], 'A. 18', '45 : 5 = 9, rồi 2 × 9 = 18.'),
        q_mcq(5, 'Thứ tự đúng là:',
              ['A. chia cho mẫu rồi nhân với tử', 'B. nhân với mẫu rồi chia cho tử',
               'C. nhân với tử rồi nhân với mẫu'],
              'A. chia cho mẫu rồi nhân với tử', 'Chia ra mới biết một phần.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B71 · TÌM SỐ KHI BIẾT PHÂN SỐ CỦA NÓ
# ═══════════════════════════════════════════════════════════════════════════
B71 = bai(
    71, 'TÌM SỐ KHI BIẾT PHÂN SỐ CỦA NÓ — ĐI NGƯỢC LẠI',
    'Dạng gốc: PS 4.2 mức Lớp 4 — Bài toán ngược: biết ba phần tư của một số bằng bao '
    'nhiêu, tìm số ấy.',
    'Bài trước con đi xuôi: có số, tìm phân số của nó. Hôm nay con đi ngược: biết phân '
    'số của nó bằng bao nhiêu rồi, tìm lại chính con số ấy. Vẫn hai bước, chỉ đổi thứ '
    'tự và đổi phép.',
    LUI_PHAN,
    video(
        ['Nhận ra bài toán ngược của bài trước.',
         'Tìm một phần rồi nhân lên cho đủ mẫu số.',
         'Thử lại bằng cách đi xuôi.'],
        ['Đề bài: Ba phần tư của một số bằng 15. Tìm số đó.',
         'So với bài hôm qua',
         'Hôm qua có số 20, tìm ra 15. Hôm nay có 15, tìm lại 20.',
         'Bước một, tìm một phần',
         '15 chính là 3 phần. Vậy một phần là 15 : 3 = 5.',
         'Bước hai, nhân cho đủ mẫu',
         'Cả số gồm 4 phần, nên nó là 4 × 5 = 20.',
         'Thử lại bằng cách đi xuôi',
         'Ba phần tư của 20: 20 : 4 = 5, rồi 3 × 5 = 15. Đúng bằng đề cho.',
         'Đáp số: số cần tìm là 20.'],
        ['Có bạn thấy 15 rồi lấy luôn 15 : 4 để tìm một phần.',
         'Gợi ý 1: Số 15 trong đề là mấy phần, 3 phần hay 4 phần?',
         'Gợi ý 2: Là 3 phần thôi, vì đề nói ba phần tư.',
         'Chữa: phải chia cho TỬ SỐ là 3, không chia cho mẫu. Chia nhầm là tìm sai một '
         'phần, và cả bài sai theo.'],
        ['Hỏi con một câu trước khi tính: "Con số đề cho là mấy phần?" Trả lời đúng thì '
         'phần còn lại rất nhanh.',
         'Bài xuôi chia cho mẫu, bài ngược chia cho tử. Con hay lẫn hai chỗ ấy.'],
    ),
    [
        lt(1, 1, 'Ba phần tư của một số bằng 15 — đúng bài trong video. Số 15 ứng với '
                 'mấy phần?',
           '3 phần, vì đề nói ba phần tư.'),
        lt(2, 1, 'Vẫn bài trên. Một phần bằng bao nhiêu?',
           '15 : 3 = 5.'),
        lt(3, 1, 'Vẫn bài trên. Số cần tìm là bao nhiêu?',
           'Cả số gồm 4 phần: 4 × 5 = 20.'),
        lt(4, 2, 'Bạn Minh lấy 15 : 4 để tìm một phần. Bạn sai ở đâu?',
           '15 ứng với 3 phần chứ không phải 4 phần, nên phải chia cho tử số 3.'),
        lt(5, 2, 'Hai phần năm của một số bằng 18. Tìm số đó.',
           'Một phần: 18 : 2 = 9. Cả số: 5 × 9 = 45.'),
        lt(6, 2, 'Ba phần tư số học sinh của lớp là 24 bạn. Lớp có bao nhiêu bạn?',
           'Một phần: 24 : 3 = 8. Cả lớp: 4 × 8 = 32 bạn.'),
        lt(7, 2, 'Bài đi xuôi chia cho số nào, bài đi ngược chia cho số nào?',
           'Đi xuôi chia cho MẪU số rồi nhân với tử. Đi ngược chia cho TỬ số rồi nhân '
           'với mẫu.'),
        lt(8, 3, 'Ba phần năm số gạo trong kho là 36 tấn. Hỏi kho có bao nhiêu tấn gạo, '
                 'rồi thử lại.',
           'Một phần: 36 : 3 = 12. Cả kho: 5 × 12 = 60 tấn. Thử: 60 : 5 = 12, rồi '
           '3 × 12 = 36 tấn, đúng đề cho.'),
        lt(9, 3, 'Một phần tư số vịt trong đàn là 7 con. Hỏi đàn có bao nhiêu con vịt?',
           'Một phần đã là 7 con. Cả đàn 4 phần: 4 × 7 = 28 con.'),
        q_tf(1, 'Bài đi ngược thì chia cho tử số rồi nhân với mẫu số.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Ba phần tư của một số bằng 15 thì số đó là 15 : 4.', False,
             'SAI — 15 ứng với 3 phần, phải chia cho 3.'),
        q_mcq(3, 'Ba phần tư của một số bằng 15. Một phần bằng:',
              ['A. 5', 'B. 4', 'C. 20'], 'A. 5', '15 : 3 = 5.'),
        q_mcq(4, 'Số cần tìm là:',
              ['A. 20', 'B. 15', 'C. 12'], 'A. 20', '4 × 5 = 20.'),
        q_mcq(5, 'Hai phần năm của một số bằng 18. Số đó là:',
              ['A. 45', 'B. 36', 'C. 9'], 'A. 45', 'Một phần 9, cả số 5 phần.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑦ B40 · DÃY PHÂN SỐ · TỔNG TÁCH HIỆU  (mã cũ, viết lại — chỉ còn TỔNG)
# ═══════════════════════════════════════════════════════════════════════════
B40 = bai(
    40, 'DÃY PHÂN SỐ · TỔNG — TÁCH MỖI SỐ THÀNH MỘT HIỆU',
    'Dạng gốc: PS 2.1 mức Lớp 4 — Tổng dãy phân số dạng một phần tích hai số liên '
    'tiếp, giải bằng cách tách mỗi số hạng thành một hiệu.',
    'Có những phép cộng phân số dài dằng dặc, cộng thẳng thì rất lâu. Hôm nay con học '
    'một cách rất đẹp: tách mỗi số hạng thành một HIỆU, rồi hầu hết các phần sẽ tự '
    'triệt tiêu nhau.',
    LUI_DAY,
    video(
        ['Tách một phần tích hai số liên tiếp thành một hiệu.',
         'Thấy các phần giữa triệt tiêu nhau.',
         'Chỉ còn số đầu và số cuối.'],
        ['Đề bài: Tính tổng một phần hai cộng một phần sáu cộng một phần mười hai.',
         'Nhìn kỹ các mẫu số',
         'Hai bằng một nhân hai. Sáu bằng hai nhân ba. Mười hai bằng ba nhân bốn. Toàn '
         'là tích của hai số liên tiếp.',
         'Tách mỗi số thành một hiệu',
         'Một phần một nhân hai bằng một phần một trừ một phần hai.',
         'Một phần hai nhân ba bằng một phần hai trừ một phần ba.',
         'Một phần ba nhân bốn bằng một phần ba trừ một phần tư.',
         'Cộng lại thì các phần giữa triệt tiêu',
         'Một phần hai trừ rồi lại cộng, nên mất. Một phần ba cũng thế. Chỉ còn một '
         'phần một trừ một phần tư.',
         'Tính nốt',
         'Một trừ một phần tư bằng ba phần tư.',
         'Đáp số: tổng bằng ba phần tư.'],
        ['Có bạn cộng thẳng ba phân số mà quên quy đồng, ra một phần hai mươi.',
         'Gợi ý 1: Cộng phân số khác mẫu thì có cộng thẳng tử với tử, mẫu với mẫu được không?',
         'Gợi ý 2: Không được. Nhưng ở bài này còn có cách hay hơn cả quy đồng.',
         'Chữa: tách mỗi số thành một hiệu thì các phần giữa tự triệt tiêu, chỉ còn số '
         'đầu và số cuối. Kết quả là ba phần tư.'],
        ['Viết ba hiệu ra giấy rồi bảo con gạch những phần xuất hiện hai lần. Con thấy '
         'chỉ còn hai đầu là hiểu.',
         'Cách này chỉ dùng được khi mẫu số là tích hai số LIÊN TIẾP. Bố mẹ nhắc con '
         'kiểm điều ấy trước.'],
    ),
    [
        lt(1, 1, 'Tính tổng một phần hai cộng một phần sáu cộng một phần mười hai — đúng '
                 'bài trong video. Mẫu số 6 bằng tích của hai số liên tiếp nào?',
           '6 = 2 × 3.'),
        lt(2, 1, 'Vẫn bài trên. Một phần hai nhân ba tách thành hiệu nào?',
           'Một phần hai trừ một phần ba.'),
        lt(3, 1, 'Vẫn bài trên. Sau khi tách và triệt tiêu, còn lại hiệu nào?',
           'Một trừ một phần tư.'),
        lt(4, 2, 'Vẫn bài trên. Tổng bằng bao nhiêu?',
           'Một trừ một phần tư bằng ba phần tư.'),
        lt(5, 2, 'Bạn Nam cộng thẳng tử với tử, mẫu với mẫu. Bạn sai ở đâu?',
           'Cộng phân số không cộng thẳng tử với tử được. Ở bài này có cách hay hơn: '
           'tách thành hiệu rồi triệt tiêu.'),
        lt(6, 2, 'Tách một phần bốn nhân năm thành một hiệu.',
           'Một phần bốn trừ một phần năm.'),
        lt(7, 2, 'Tính tổng một phần hai cộng một phần sáu.',
           'Tách ra: (một trừ một phần hai) cộng (một phần hai trừ một phần ba). Triệt '
           'tiêu còn một trừ một phần ba, bằng hai phần ba.'),
        lt(8, 3, 'Tính tổng một phần hai cộng một phần sáu cộng một phần mười hai cộng '
                 'một phần hai mươi.',
           'Mẫu cuối 20 = 4 × 5. Sau khi tách và triệt tiêu còn một trừ một phần năm, '
           'bằng bốn phần năm.'),
        lt(9, 3, 'Vì sao cách tách này chỉ dùng được khi mẫu số là tích hai số liên tiếp?',
           'Vì chỉ khi hai số liên tiếp thì hiệu hai phân số mới ra đúng một phần tích '
           'của chúng. Mẫu số kiểu khác thì tách ra không khớp, không triệt tiêu được.'),
        q_tf(1, 'Một phần hai nhân ba bằng một phần hai trừ một phần ba.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Cộng phân số thì cộng thẳng tử với tử, mẫu với mẫu.', False,
             'SAI — không cộng thẳng như thế được.'),
        q_mcq(3, 'Mẫu số 12 bằng tích hai số liên tiếp nào?',
              ['A. 3 × 4', 'B. 2 × 6', 'C. 1 × 12'], 'A. 3 × 4',
              'Phải là hai số liên tiếp.'),
        q_mcq(4, 'Tổng một phần hai cộng một phần sáu cộng một phần mười hai bằng:',
              ['A. ba phần tư', 'B. một phần hai', 'C. một phần hai mươi'],
              'A. ba phần tư', 'Một trừ một phần tư.'),
        q_mcq(5, 'Sau khi tách, các phần ở giữa:',
              ['A. triệt tiêu nhau', 'B. cộng dồn lại', 'C. nhân với nhau'],
              'A. triệt tiêu nhau', 'Trừ rồi lại cộng thì mất.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑧ B72 · DÃY PHÂN SỐ · TÍCH RÚT GỌN CHÉO
# ═══════════════════════════════════════════════════════════════════════════
B72 = bai(
    72, 'DÃY PHÂN SỐ · TÍCH — GẠCH CHÉO CHO GỌN',
    'Dạng gốc: PS 2.2 mức Lớp 4 — Tích dãy phân số nối tiếp, rút gọn chéo giữa tử của '
    'phân số này và mẫu của phân số kia.',
    'Bài trước là phép CỘNG dài. Hôm nay là phép NHÂN dài, và cũng có một cách rất '
    'gọn — nhưng cách khác hẳn. Lần này con gạch chéo cho các số triệt tiêu nhau.',
    LUI_DAY,
    video(
        ['Nhân dãy phân số nối tiếp nhau.',
         'Rút gọn chéo giữa tử của phân số này và mẫu của phân số trước.',
         'Chỉ còn tử đầu và mẫu cuối.'],
        ['Đề bài: Tính tích một phần hai nhân hai phần ba nhân ba phần tư.',
         'Nhìn kỹ các con số',
         'Mẫu của phân số thứ nhất là 2, mà tử của phân số thứ hai cũng là 2.',
         'Mẫu của phân số thứ hai là 3, mà tử của phân số thứ ba cũng là 3.',
         'Gạch chéo cho triệt tiêu',
         'Số 2 ở mẫu và số 2 ở tử triệt tiêu nhau. Số 3 cũng thế.',
         'Còn lại gì',
         'Chỉ còn tử số đầu tiên là 1, và mẫu số cuối cùng là 4.',
         'Nên tích bằng một phần tư.',
         'So với bài hôm qua',
         'Hôm qua cộng dài, các phần GIỮA triệt tiêu. Hôm nay nhân dài, các số CHÉO '
         'triệt tiêu. Hai cách khác nhau, đừng lẫn.',
         'Đáp số: tích bằng một phần tư.'],
        ['Có bạn đem cách của bài cộng sang dùng cho bài nhân, đi tách thành hiệu.',
         'Gợi ý 1: Bài này là phép cộng hay phép nhân?',
         'Gợi ý 2: Phép nhân. Mà tách thành hiệu là cách của phép cộng.',
         'Chữa: bài nhân thì gạch chéo, bài cộng thì tách thành hiệu. Hai cách cho hai '
         'phép khác nhau, không dùng lẫn được.'],
        ['Viết dãy nhân ra giấy rồi bảo con lấy bút gạch các số giống nhau ở tử và mẫu. '
         'Gạch xong chỉ còn hai số là con hiểu.',
         'Con hay lẫn hai cách của hai bài. Bố mẹ hỏi trước: "Bài này cộng hay nhân?"'],
    ),
    [
        lt(1, 1, 'Tính tích một phần hai nhân hai phần ba nhân ba phần tư — đúng bài '
                 'trong video. Số nào ở mẫu phân số đầu và tử phân số thứ hai giống nhau?',
           'Số 2 — nó ở mẫu của phân số đầu và ở tử của phân số thứ hai.'),
        lt(2, 1, 'Vẫn bài trên. Sau khi gạch chéo hết thì còn lại tử số nào và mẫu số nào?',
           'Còn tử số đầu tiên là 1 và mẫu số cuối cùng là 4.'),
        lt(3, 1, 'Vẫn bài trên. Tích bằng bao nhiêu?',
           'Một phần tư.'),
        lt(4, 2, 'Bạn Lan đem cách tách thành hiệu sang dùng cho bài nhân. Bạn sai ở đâu?',
           'Tách thành hiệu là cách của phép CỘNG. Bài nhân thì gạch chéo. Hai cách cho '
           'hai phép khác nhau.'),
        lt(5, 2, 'Tính tích một phần hai nhân hai phần ba.',
           'Số 2 triệt tiêu, còn một phần ba.'),
        lt(6, 2, 'Tính tích một phần hai nhân hai phần ba nhân ba phần tư nhân bốn phần năm.',
           'Các số 2, 3, 4 đều triệt tiêu, còn một phần năm.'),
        lt(7, 2, 'Vì sao gạch chéo được?',
           'Vì nhân phân số thì nhân tử với tử, mẫu với mẫu. Một số vừa có ở tử vừa có '
           'ở mẫu thì chia cho nhau bằng 1, nên bỏ đi được.'),
        lt(8, 3, 'Tính tích hai phần ba nhân ba phần tư nhân bốn phần năm.',
           'Các số 3 và 4 triệt tiêu, còn hai phần năm.'),
        lt(9, 3, 'Bài cộng dài và bài nhân dài dùng hai cách khác nhau thế nào?',
           'Bài CỘNG tách mỗi số thành một hiệu rồi các phần GIỮA triệt tiêu. Bài NHÂN '
           'gạch chéo rồi các số Ở GIỮA triệt tiêu, chỉ còn tử đầu và mẫu cuối.'),
        q_tf(1, 'Tích một phần hai nhân hai phần ba nhân ba phần tư bằng một phần tư.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Bài nhân dài cũng tách mỗi số thành một hiệu như bài cộng.', False,
             'SAI — bài nhân thì gạch chéo.'),
        q_mcq(3, 'Tích một phần hai nhân hai phần ba bằng:',
              ['A. một phần ba', 'B. hai phần sáu', 'C. ba phần hai'],
              'A. một phần ba', 'Số 2 triệt tiêu.'),
        q_mcq(4, 'Sau khi gạch chéo hết, tích chỉ còn:',
              ['A. tử đầu và mẫu cuối', 'B. tử cuối và mẫu đầu', 'C. tất cả các số'],
              'A. tử đầu và mẫu cuối', 'Các số giữa đều triệt tiêu.'),
        q_mcq(5, 'Cách gạch chéo dùng cho phép:',
              ['A. nhân', 'B. cộng', 'C. trừ'], 'A. nhân',
              'Phép cộng dùng cách tách thành hiệu.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑨ B41 · CÙNG THÊM Ở TỬ VÀ MẪU  (mã cũ, viết lại — chỉ còn HIỆU không đổi)
# ═══════════════════════════════════════════════════════════════════════════
B41 = bai(
    41, 'CÙNG THÊM Ở TỬ VÀ MẪU — HIỆU KHÔNG ĐỔI',
    'Dạng gốc: PS 3.1 mức Lớp 4 — Cùng thêm một số vào cả tử và mẫu; hiệu giữa mẫu và '
    'tử không đổi.',
    'Ở chương tổng - hiệu con đã biết: cùng thêm vào cả hai số thì hiệu không đổi. Hôm '
    'nay con gặp lại đúng điều ấy, nhưng lần này hai số là tử số và mẫu số của một '
    'phân số.',
    LUI_BANG,
    video(
        ['Biết cùng thêm vào tử và mẫu thì hiệu giữa chúng không đổi.',
         'Dùng hiệu không đổi để tìm phân số mới.',
         'Nhận ra đây là điều đã học ở chương tổng - hiệu.'],
        ['Đề bài: Cho phân số ba phần tư. Cùng thêm 2 vào cả tử số và mẫu số thì được '
         'phân số nào, và hiệu giữa mẫu với tử có đổi không?',
         'Thêm vào cả hai',
         'Tử số 3 thêm 2 thành 5. Mẫu số 4 thêm 2 thành 6. Được phân số năm phần sáu.',
         'Xem hiệu có đổi không',
         'Lúc đầu mẫu trừ tử là 4 trừ 3, bằng 1. Sau khi thêm là 6 trừ 5, cũng bằng 1.',
         'Hiệu không đổi',
         'Đúng như chương tổng - hiệu: cùng thêm vào cả hai thì khoảng cách giữa chúng '
         'y nguyên.',
         'Dùng điều ấy để giải bài',
         'Nếu đề nói thêm một số vào cả tử và mẫu để được phân số mới, ta biết ngay hiệu '
         'giữa mẫu và tử của phân số mới vẫn là 1.',
         'Đáp số: được năm phần sáu, và hiệu vẫn bằng 1.'],
        ['Có bạn nghĩ thêm 2 vào cả hai thì phân số không đổi, vì "thêm bằng nhau mà".',
         'Gợi ý 1: Ba phần tư và năm phần sáu, con vẽ hai băng ra so thử xem.',
         'Gợi ý 2: Năm phần sáu tô nhiều hơn đấy.',
         'Chữa: chỉ có HIỆU giữa mẫu và tử là không đổi. Còn phân số thì ĐỔI — nó to '
         'lên. Đừng lẫn hai chuyện.'],
        ['Cho con thêm 2 vào cả tử và mẫu vài lần rồi hỏi: "Mẫu trừ tử bằng mấy?" Con '
         'thấy luôn ra cùng một số là hiểu.',
         'Chỗ nhầm là tưởng phân số không đổi. Bố mẹ nhấn: hiệu không đổi, nhưng phân '
         'số thì đổi.'],
    ),
    [
        lt(1, 1, 'Cho phân số ba phần tư, cùng thêm 2 vào tử và mẫu — đúng bài trong '
                 'video. Được phân số nào?',
           'Tử 3 thêm 2 thành 5, mẫu 4 thêm 2 thành 6. Được năm phần sáu.'),
        lt(2, 1, 'Vẫn bài trên. Lúc đầu mẫu trừ tử bằng bao nhiêu?',
           '4 − 3 = 1.'),
        lt(3, 1, 'Vẫn bài trên. Sau khi thêm, mẫu trừ tử bằng bao nhiêu?',
           '6 − 5 = 1 — vẫn như cũ.'),
        lt(4, 2, 'Bạn Tú nghĩ thêm bằng nhau thì phân số không đổi. Bạn sai ở đâu?',
           'Chỉ HIỆU giữa mẫu và tử là không đổi. Phân số thì đổi — năm phần sáu lớn '
           'hơn ba phần tư.'),
        lt(5, 2, 'Cho phân số hai phần năm, cùng thêm 3 vào tử và mẫu. Được phân số nào '
                 'và hiệu bằng bao nhiêu?',
           'Được năm phần tám. Hiệu lúc đầu 5 − 2 = 3, sau vẫn 8 − 5 = 3.'),
        lt(6, 2, 'Vì sao cùng thêm vào cả tử và mẫu thì hiệu không đổi?',
           'Vì cả hai cùng lớn lên bằng nhau nên khoảng cách giữa chúng y nguyên — đúng '
           'như đã học ở chương tổng - hiệu.'),
        lt(7, 2, 'Một phân số có mẫu hơn tử 4 đơn vị. Cùng thêm 10 vào cả tử và mẫu thì '
                 'mẫu hơn tử bao nhiêu?',
           'Vẫn hơn 4 đơn vị.'),
        lt(8, 3, 'Cho phân số ba phần tư. Cùng thêm bao nhiêu vào tử và mẫu để được phân '
                 'số bảy phần tám?',
           'Tử từ 3 lên 7 là thêm 4; mẫu từ 4 lên 8 cũng thêm 4. Vậy thêm 4. Hiệu vẫn '
           'là 1 ở cả hai phân số.'),
        lt(9, 3, 'Một phân số có mẫu hơn tử 1 đơn vị. Sau khi cùng thêm một số vào tử và '
                 'mẫu thì được phân số chín phần mười. Phân số ban đầu có thể là ba phần '
                 'tư không?',
           'Có thể. Chín phần mười có mẫu hơn tử 1, đúng bằng hiệu của ba phần tư. Thêm '
           '6 vào cả hai thì ba phần tư thành chín phần mười.'),
        q_tf(1, 'Cùng thêm một số vào tử và mẫu thì hiệu giữa mẫu và tử không đổi.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Cùng thêm một số vào tử và mẫu thì phân số không đổi.', False,
             'SAI — phân số đổi, chỉ hiệu là không đổi.'),
        q_mcq(3, 'Ba phần tư, thêm 2 vào cả tử và mẫu, được:',
              ['A. năm phần sáu', 'B. ba phần sáu', 'C. năm phần tư'],
              'A. năm phần sáu', 'Cả hai cùng thêm 2.'),
        q_mcq(4, 'Hiệu giữa mẫu và tử của ba phần tư là:',
              ['A. 1', 'B. 7', 'C. 3'], 'A. 1', '4 − 3 = 1.'),
        q_mcq(5, 'Sau khi cùng thêm 2, hiệu ấy bằng:',
              ['A. 1', 'B. 3', 'C. 2'], 'A. 1', 'Hiệu không đổi.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑩ B73 · CHUYỂN GIỮA TỬ VÀ MẪU — tổng không đổi
# ═══════════════════════════════════════════════════════════════════════════
# Tách khỏi B41. Đây đúng chỗ bé lẫn nhiều nhất: thêm vào cả hai thì HIỆU đứng yên,
# còn chuyển qua lại thì TỔNG đứng yên. Dạy chung một bài là chắc chắn lẫn.
B73 = bai(
    73, 'CHUYỂN GIỮA TỬ VÀ MẪU — TỔNG KHÔNG ĐỔI',
    'Dạng gốc: PS 3.2 mức Lớp 4 — Chuyển một số từ mẫu sang tử hoặc ngược lại; tổng '
    'của tử và mẫu không đổi.',
    'Bài trước con THÊM vào cả hai đầu, và hiệu đứng yên. Hôm nay con CHUYỂN từ đầu này '
    'sang đầu kia — và lần này thứ đứng yên là TỔNG. Hai bài rất giống nhau nên phải '
    'phân biệt cho rõ, không thì lẫn ngay.',
    LUI_BANG,
    video(
        ['Biết chuyển giữa tử và mẫu thì tổng của chúng không đổi.',
         'Dùng tổng không đổi để tìm phân số mới.',
         'Phân biệt được với bài cùng thêm hai đầu.'],
        ['Đề bài: Cho phân số ba phần tư. Chuyển 1 đơn vị từ mẫu số sang tử số thì được '
         'phân số nào, và tổng của tử với mẫu có đổi không?',
         'Chuyển qua',
         'Mẫu số 4 bớt 1 còn 3. Tử số 3 thêm 1 thành 4. Được phân số bốn phần ba.',
         'Xem tổng có đổi không',
         'Lúc đầu tử cộng mẫu là 3 cộng 4, bằng 7. Sau khi chuyển là 4 cộng 3, cũng bằng 7.',
         'Tổng không đổi',
         'Vì bên này bớt bao nhiêu thì bên kia được thêm đúng bấy nhiêu, nên gộp lại vẫn '
         'y nguyên.',
         'Đừng lẫn với bài hôm qua',
         'Hôm qua THÊM vào cả hai đầu, thứ đứng yên là HIỆU. Hôm nay CHUYỂN qua lại, thứ '
         'đứng yên là TỔNG. Hai bài khác hẳn.',
         'Đáp số: được bốn phần ba, và tổng vẫn bằng 7.'],
        ['Có bạn nhớ nhầm, tưởng chuyển qua lại thì hiệu không đổi.',
         'Gợi ý 1: Ba phần tư có mẫu trừ tử bằng 1. Bốn phần ba thì mẫu trừ tử bằng mấy?',
         'Gợi ý 2: Bằng âm một, tức đổi hẳn chiều. Vậy hiệu có giữ nguyên không?',
         'Chữa: chuyển qua lại thì TỔNG không đổi, không phải hiệu. Thêm vào cả hai đầu '
         'mới là hiệu không đổi. Nhớ lẫn hai chỗ này là sai cả bài.'],
        ['Lấy 7 hạt đậu chia thành hai nhóm 3 và 4 rồi chuyển qua lại. Con thấy tổng vẫn '
         'là 7 dù chia thế nào.',
         'Hai bài này giống nhau tới mức rất dễ lẫn. Bố mẹ hỏi: "Đề THÊM vào hay CHUYỂN '
         'qua lại?"'],
    ),
    [
        lt(1, 1, 'Cho phân số ba phần tư, chuyển 1 từ mẫu sang tử — đúng bài trong video. '
                 'Được phân số nào?',
           'Mẫu 4 bớt 1 còn 3, tử 3 thêm 1 thành 4. Được bốn phần ba.'),
        lt(2, 1, 'Vẫn bài trên. Lúc đầu tử cộng mẫu bằng bao nhiêu?',
           '3 + 4 = 7.'),
        lt(3, 1, 'Vẫn bài trên. Sau khi chuyển, tử cộng mẫu bằng bao nhiêu?',
           '4 + 3 = 7 — vẫn như cũ.'),
        lt(4, 2, 'Bạn Hoa tưởng chuyển qua lại thì hiệu không đổi. Bạn sai ở đâu?',
           'Chuyển qua lại thì TỔNG không đổi. Thêm vào cả hai đầu mới là hiệu không đổi. '
           'Hai bài khác hẳn nhau.'),
        lt(5, 2, 'Cho phân số hai phần bảy. Chuyển 2 từ mẫu sang tử thì được phân số nào, '
                 'và tổng bằng bao nhiêu?',
           'Được bốn phần năm. Tổng lúc đầu 2 + 7 = 9, sau vẫn 4 + 5 = 9.'),
        lt(6, 2, 'Vì sao chuyển qua lại thì tổng không đổi?',
           'Vì bên này bớt bao nhiêu thì bên kia được thêm đúng bấy nhiêu, nên gộp lại '
           'vẫn y nguyên.'),
        lt(7, 2, 'Một phân số có tử cộng mẫu bằng 12. Sau khi chuyển vài đơn vị giữa tử '
                 'và mẫu, tử cộng mẫu bằng bao nhiêu?',
           'Vẫn bằng 12.'),
        lt(8, 3, 'Cho phân số ba phần tư. Chuyển bao nhiêu từ mẫu sang tử để được phân '
                 'số năm phần hai?',
           'Tử từ 3 lên 5 là thêm 2; mẫu từ 4 xuống 2 là bớt 2. Vậy chuyển 2 đơn vị. '
           'Tổng vẫn là 7 ở cả hai phân số.'),
        lt(9, 3, 'Hai bài "cùng thêm vào tử và mẫu" và "chuyển giữa tử và mẫu" khác nhau '
                 'thế nào?',
           'Cùng THÊM vào cả hai thì HIỆU giữa mẫu và tử không đổi. CHUYỂN qua lại thì '
           'TỔNG của tử và mẫu không đổi. Đọc kỹ đề để biết đang gặp bài nào.'),
        q_tf(1, 'Chuyển giữa tử và mẫu thì tổng của chúng không đổi.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Chuyển giữa tử và mẫu thì hiệu của chúng không đổi.', False,
             'SAI — đó là bài cùng thêm vào cả hai đầu.'),
        q_mcq(3, 'Ba phần tư, chuyển 1 từ mẫu sang tử, được:',
              ['A. bốn phần ba', 'B. bốn phần năm', 'C. hai phần năm'],
              'A. bốn phần ba', 'Tử thêm 1, mẫu bớt 1.'),
        q_mcq(4, 'Tổng của tử và mẫu của ba phần tư là:',
              ['A. 7', 'B. 1', 'C. 12'], 'A. 7', '3 + 4 = 7.'),
        q_mcq(5, 'Cùng THÊM vào hai đầu thì thứ không đổi là:',
              ['A. hiệu', 'B. tổng', 'C. cả hai'], 'A. hiệu',
              'Còn chuyển qua lại thì tổng không đổi.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑪ B42 · PHÂN SỐ TRONG BÀI TOÁN THỰC TẾ  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
B42 = bai(
    42, 'PHÂN SỐ TRONG BÀI TOÁN THỰC TẾ — ĐỌC RA PHÂN SỐ CỦA CÁI GÌ',
    'Dạng gốc: PS 5.1 mức Lớp 4 — Bài toán lời văn dùng phân số; điều quan trọng nhất '
    'là xác định phân số ấy là của đại lượng nào.',
    'Bài cuối chương, và nó không dạy phép mới nào. Nó dạy một việc khác, mà việc ấy '
    'mới là chỗ bé sai nhiều nhất: đọc cho ra phân số trong đề là phân số CỦA CÁI GÌ.',
    LUI_PHAN,
    video(
        ['Xác định phân số trong đề là của đại lượng nào.',
         'Áp dụng cách tìm phân số của một số đã học.',
         'Soi lại kết quả cho hợp lý.'],
        ['Đề bài: Một cửa hàng có 20 tấn gạo. Ngày đầu bán được ba phần tư số gạo. Hỏi '
         'ngày đầu bán được bao nhiêu tấn và còn lại bao nhiêu tấn?',
         'Đọc cho ra phân số CỦA CÁI GÌ',
         'Ba phần tư ở đây là của SỐ GẠO BAN ĐẦU, tức của 20 tấn.',
         'Tính số gạo bán được',
         '20 chia 4 bằng 5, rồi 3 nhân 5 bằng 15 tấn.',
         'Tính số gạo còn lại',
         '20 trừ 15 bằng 5 tấn.',
         'Soi lại cho hợp lý',
         'Bán ba phần tư thì còn một phần tư, tức 5 tấn. Khớp với kết quả vừa tính.',
         'Đáp số: bán được 15 tấn, còn lại 5 tấn.'],
        ['Có bạn đọc "ngày sau bán ba phần tư chỗ còn lại" mà vẫn lấy ba phần tư của số '
         'gạo BAN ĐẦU.',
         'Gợi ý 1: Đề nói ba phần tư của cái gì?',
         'Gợi ý 2: Của chỗ CÒN LẠI, chứ không phải của số ban đầu.',
         'Chữa: phải đọc kỹ phân số ấy là của đại lượng nào. Lấy nhầm gốc thì mọi phép '
         'tính sau đều sai, dù tính rất đúng.'],
        ['Đọc đề chậm rồi hỏi con một câu duy nhất: "Ba phần tư của CÁI GÌ?" Trả lời '
         'đúng là con đã qua chỗ khó nhất.',
         'Bài này không khó ở phép tính mà khó ở đọc hiểu. Bố mẹ đọc chậm giúp con.'],
    ),
    [
        lt(1, 1, 'Cửa hàng có 20 tấn gạo, ngày đầu bán ba phần tư số gạo — đúng bài trong '
                 'video. Ba phần tư ở đây là của cái gì?',
           'Của SỐ GẠO BAN ĐẦU, tức của 20 tấn.'),
        lt(2, 1, 'Vẫn bài trên. Ngày đầu bán được bao nhiêu tấn?',
           '20 : 4 = 5, rồi 3 × 5 = 15 tấn.'),
        lt(3, 1, 'Vẫn bài trên. Còn lại bao nhiêu tấn?',
           '20 − 15 = 5 tấn.'),
        lt(4, 2, 'Bạn Nam đọc "ba phần tư chỗ còn lại" mà lấy ba phần tư của số ban đầu. '
                 'Bạn sai ở đâu?',
           'Phân số ấy là của chỗ CÒN LẠI, không phải của số ban đầu. Lấy nhầm gốc thì '
           'mọi phép sau đều sai.'),
        lt(5, 2, 'Một tấm vải dài 40 mét, người ta cắt đi hai phần năm tấm vải. Hỏi cắt '
                 'đi bao nhiêu mét?',
           '40 : 5 = 8, rồi 2 × 8 = 16 mét.'),
        lt(6, 2, 'Vẫn bài trên. Tấm vải còn lại bao nhiêu mét?',
           '40 − 16 = 24 mét.'),
        lt(7, 2, 'Một lớp có 32 bạn. Ba phần tư số bạn là nữ, còn lại là nam. Lớp có bao '
                 'nhiêu bạn nam?',
           'Số nữ: 32 : 4 = 8, rồi 3 × 8 = 24 bạn. Số nam: 32 − 24 = 8 bạn.'),
        lt(8, 3, 'Kho có 20 tấn gạo. Ngày đầu bán ba phần tư số gạo, ngày sau bán một '
                 'phần năm CHỖ CÒN LẠI. Hỏi ngày sau bán bao nhiêu tấn?',
           'Ngày đầu bán 15 tấn, còn 5 tấn. Ngày sau bán một phần năm của 5 tấn: '
           '5 : 5 = 1 tấn.'),
        lt(9, 3, 'Vẫn bài trên. Sau hai ngày kho còn bao nhiêu tấn gạo?',
           'Còn 5 − 1 = 4 tấn.'),
        q_tf(1, 'Phải đọc kỹ phân số trong đề là của đại lượng nào.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, '"Ba phần tư chỗ còn lại" cũng là ba phần tư của số ban đầu.', False,
             'SAI — hai gốc khác nhau.'),
        q_mcq(3, '20 tấn gạo, bán ba phần tư thì bán được:',
              ['A. 15 tấn', 'B. 5 tấn', 'C. 26 tấn'], 'A. 15 tấn', '20 : 4 × 3 = 15.'),
        q_mcq(4, 'Bán ba phần tư thì còn lại:',
              ['A. một phần tư', 'B. ba phần tư', 'C. một phần ba'],
              'A. một phần tư', 'Cả băng trừ ba phần tư.'),
        q_mcq(5, 'Chỗ khó nhất của bài toán lời văn có phân số là:',
              ['A. đọc ra phân số ấy là của cái gì', 'B. phép chia', 'C. phép nhân'],
              'A. đọc ra phân số ấy là của cái gì',
              'Lấy nhầm gốc thì mọi phép sau đều sai.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
MOI = [B68, B38, B69, B70, B39, B71, B40, B72, B41, B73, B42]
SAU = {'DL:KSN4.B68': None,                       # B68 chèn TRƯỚC B38
       'DL:KSN4.B69': 'DL:KSN4.B38', 'DL:KSN4.B70': 'DL:KSN4.B69',
       'DL:KSN4.B71': 'DL:KSN4.B39', 'DL:KSN4.B72': 'DL:KSN4.B40',
       'DL:KSN4.B73': 'DL:KSN4.B41'}

O_NHAP_MOI = {
    'DL:KSN4.B68#C1': {'value': 4},
    'DL:KSN4.B68#C2': {'parts': [{'label': 'tử số', 'value': 3},
                                 {'label': 'cho biết lấy mấy phần', 'value': 3}]},
    'DL:KSN4.B68#C3': {'parts': [{'label': 'tử số', 'value': 2},
                                 {'label': 'mẫu số', 'value': 5}]},
    'DL:KSN4.B68#C4': {'parts': [{'label': 'các phần phải thế nào',
                                  'options': ['bằng nhau', 'khác nhau'],
                                  'value': 'bằng nhau'}]},
    'DL:KSN4.B68#C5': {'parts': [{'label': 'hai phân số có giống nhau không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B68#C6': {'parts': [{'label': 'tử số', 'value': 7},
                                 {'label': 'mẫu số', 'value': 30}]},
    'DL:KSN4.B68#C7': {'value': 1},
    'DL:KSN4.B68#C8': {'parts': [{'label': 'bằng mấy phần hai', 'value': 1}]},
    'DL:KSN4.B68#C9': {'parts': [{'label': 'hai phần tô có bằng nhau không',
                                  'options': CO_KHONG, 'value': 'có'}]},

    'DL:KSN4.B38#C1': {'parts': [{'label': 'giống nhau ở',
                                  'options': ['mẫu số', 'tử số'], 'value': 'mẫu số'}]},
    'DL:KSN4.B38#C2': {'parts': [{'label': 'tử số của phân số lớn hơn', 'value': 3}]},
    'DL:KSN4.B38#C3': {'parts': [{'label': 'giống nhau ở',
                                  'options': ['tử số', 'mẫu số'], 'value': 'tử số'}]},
    'DL:KSN4.B38#C4': {'parts': [{'label': 'mẫu số của phân số lớn hơn', 'value': 4}]},
    'DL:KSN4.B38#C5': {'parts': [{'label': 'mẫu càng lớn thì mỗi phần',
                                  'options': ['càng nhỏ', 'càng to'],
                                  'value': 'càng nhỏ'}]},
    'DL:KSN4.B38#C6': {'parts': [{'label': 'tử số của phân số lớn hơn', 'value': 7}]},
    'DL:KSN4.B38#C7': {'parts': [{'label': 'mẫu số của phân số lớn hơn', 'value': 3}]},
    'DL:KSN4.B38#C8': {'parts': [{'label': 'tử số bé nhất', 'value': 1},
                                 {'label': 'tử số lớn nhất', 'value': 3}]},
    'DL:KSN4.B38#C9': {'parts': [{'label': 'mẫu số của phân số bé nhất', 'value': 8},
                                 {'label': 'mẫu số của phân số lớn nhất', 'value': 4}]},

    'DL:KSN4.B69#C1': {'parts': [{'label': 'hai băng chia khác nhau không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B69#C2': {'value': 12},
    'DL:KSN4.B69#C3': {'parts': [{'label': 'tử số mới', 'value': 9},
                                 {'label': 'mẫu số mới', 'value': 12}]},
    'DL:KSN4.B69#C4': {'parts': [{'label': 'tử số mới của hai phần ba', 'value': 8},
                                 {'label': 'tử số của phân số lớn hơn', 'value': 9}]},
    'DL:KSN4.B69#C5': {'parts': [{'label': 'tử số đúng', 'value': 9}]},
    'DL:KSN4.B69#C6': {'parts': [{'label': 'mẫu chung', 'value': 10},
                                 {'label': 'tử số của phân số lớn hơn', 'value': 5}]},
    'DL:KSN4.B69#C7': {'parts': [{'label': 'nhân mẫu mấy lần thì nhân tử mấy lần',
                                  'options': ['bấy nhiêu lần', 'một lần'],
                                  'value': 'bấy nhiêu lần'}]},
    'DL:KSN4.B69#C8': {'parts': [{'label': 'mẫu chung', 'value': 12},
                                 {'label': 'tử số của phân số lớn hơn', 'value': 10}]},
    'DL:KSN4.B69#C9': {'parts': [{'label': 'tử số bé nhất khi quy về mẫu 12', 'value': 6},
                                 {'label': 'tử số lớn nhất', 'value': 9}]},

    'DL:KSN4.B70#C1': {'parts': [{'label': 'lớn hơn hay bé hơn 1',
                                  'options': ['lớn hơn', 'bé hơn'], 'value': 'lớn hơn'}]},
    'DL:KSN4.B70#C2': {'parts': [{'label': 'lớn hơn hay bé hơn 1',
                                  'options': ['lớn hơn', 'bé hơn'], 'value': 'bé hơn'}]},
    'DL:KSN4.B70#C3': {'parts': [{'label': 'thiếu mấy phần tư', 'value': 1}]},
    'DL:KSN4.B70#C4': {'parts': [{'label': 'thiếu mấy phần năm', 'value': 1},
                                 {'label': 'mẫu số của phân số lớn hơn', 'value': 5}]},
    'DL:KSN4.B70#C5': {'parts': [{'label': 'phần thiếu có bằng nhau không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B70#C6': {'parts': [{'label': 'mẫu số của phân số lớn hơn', 'value': 6}]},
    'DL:KSN4.B70#C7': {'parts': [{'label': 'mẫu số của phân số lớn hơn', 'value': 7}]},
    'DL:KSN4.B70#C8': {'parts': [{'label': 'tử số của phân số lớn hơn 1', 'value': 9},
                                 {'label': 'tử số của phân số bằng 1', 'value': 5}]},
    'DL:KSN4.B70#C9': {'parts': [{'label': 'dùng được khi cùng thiếu mấy phần', 'value': 1}]},

    'DL:KSN4.B39#C1': {'value': 5},
    'DL:KSN4.B39#C2': {'value': 15},
    'DL:KSN4.B39#C3': {'value': 15},
    'DL:KSN4.B39#C4': {'parts': [{'label': 'kết quả phải thế nào so với 20',
                                  'options': ['bé hơn', 'lớn hơn'], 'value': 'bé hơn'}]},
    'DL:KSN4.B39#C5': {'value': 18},
    'DL:KSN4.B39#C6': {'value': 24},
    'DL:KSN4.B39#C7': {'parts': [{'label': 'phải làm phép nào trước',
                                  'options': ['chia', 'nhân'], 'value': 'chia'}]},
    'DL:KSN4.B39#C8': {'value': 36},
    'DL:KSN4.B39#C9': {'parts': [{'label': 'bước một', 'value': 15},
                                 {'label': 'bước hai', 'value': 10}]},

    'DL:KSN4.B71#C1': {'value': 3},
    'DL:KSN4.B71#C2': {'value': 5},
    'DL:KSN4.B71#C3': {'value': 20},
    'DL:KSN4.B71#C4': {'parts': [{'label': 'phải chia cho', 'value': 3}]},
    'DL:KSN4.B71#C5': {'parts': [{'label': 'một phần', 'value': 9},
                                 {'label': 'cả số', 'value': 45}]},
    'DL:KSN4.B71#C6': {'parts': [{'label': 'một phần', 'value': 8},
                                 {'label': 'cả lớp', 'value': 32}]},
    'DL:KSN4.B71#C7': {'parts': [{'label': 'đi xuôi chia cho',
                                  'options': ['mẫu', 'tử'], 'value': 'mẫu'},
                                 {'label': 'đi ngược chia cho',
                                  'options': ['tử', 'mẫu'], 'value': 'tử'}]},
    'DL:KSN4.B71#C8': {'parts': [{'label': 'một phần', 'value': 12},
                                 {'label': 'cả kho', 'value': 60}]},
    'DL:KSN4.B71#C9': {'value': 28},

    'DL:KSN4.B40#C1': {'parts': [{'label': 'số thứ nhất', 'value': 2},
                                 {'label': 'số thứ hai', 'value': 3}]},
    'DL:KSN4.B40#C2': {'parts': [{'label': 'mẫu của số bị trừ', 'value': 2},
                                 {'label': 'mẫu của số trừ', 'value': 3}]},
    'DL:KSN4.B40#C3': {'parts': [{'label': 'mẫu của phần bị trừ đi', 'value': 4}]},
    'DL:KSN4.B40#C4': {'parts': [{'label': 'tử số của tổng', 'value': 3},
                                 {'label': 'mẫu số của tổng', 'value': 4}]},
    'DL:KSN4.B40#C5': {'parts': [{'label': 'cộng thẳng tử với tử có được không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B40#C6': {'parts': [{'label': 'mẫu của số bị trừ', 'value': 4},
                                 {'label': 'mẫu của số trừ', 'value': 5}]},
    'DL:KSN4.B40#C7': {'parts': [{'label': 'tử số của tổng', 'value': 2},
                                 {'label': 'mẫu số của tổng', 'value': 3}]},
    'DL:KSN4.B40#C8': {'parts': [{'label': 'tử số của tổng', 'value': 4},
                                 {'label': 'mẫu số của tổng', 'value': 5}]},
    'DL:KSN4.B40#C9': {'parts': [{'label': 'mẫu phải là tích của mấy số liên tiếp',
                                  'value': 2}]},

    'DL:KSN4.B72#C1': {'value': 2},
    'DL:KSN4.B72#C2': {'parts': [{'label': 'tử còn lại', 'value': 1},
                                 {'label': 'mẫu còn lại', 'value': 4}]},
    'DL:KSN4.B72#C3': {'parts': [{'label': 'tử số của tích', 'value': 1},
                                 {'label': 'mẫu số của tích', 'value': 4}]},
    'DL:KSN4.B72#C4': {'parts': [{'label': 'tách thành hiệu là cách của phép',
                                  'options': ['cộng', 'nhân'], 'value': 'cộng'}]},
    'DL:KSN4.B72#C5': {'parts': [{'label': 'tử số', 'value': 1},
                                 {'label': 'mẫu số', 'value': 3}]},
    'DL:KSN4.B72#C6': {'parts': [{'label': 'tử số', 'value': 1},
                                 {'label': 'mẫu số', 'value': 5}]},
    'DL:KSN4.B72#C7': {'parts': [{'label': 'số vừa ở tử vừa ở mẫu thì chia nhau bằng',
                                  'value': 1}]},
    'DL:KSN4.B72#C8': {'parts': [{'label': 'tử số', 'value': 2},
                                 {'label': 'mẫu số', 'value': 5}]},
    'DL:KSN4.B72#C9': {'parts': [{'label': 'bài cộng dùng cách',
                                  'options': ['tách thành hiệu', 'gạch chéo'],
                                  'value': 'tách thành hiệu'},
                                 {'label': 'bài nhân dùng cách',
                                  'options': ['gạch chéo', 'tách thành hiệu'],
                                  'value': 'gạch chéo'}]},

    'DL:KSN4.B41#C1': {'parts': [{'label': 'tử số mới', 'value': 5},
                                 {'label': 'mẫu số mới', 'value': 6}]},
    'DL:KSN4.B41#C2': {'value': 1},
    'DL:KSN4.B41#C3': {'value': 1},
    'DL:KSN4.B41#C4': {'parts': [{'label': 'phân số có đổi không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B41#C5': {'parts': [{'label': 'tử số mới', 'value': 5},
                                 {'label': 'mẫu số mới', 'value': 8},
                                 {'label': 'hiệu', 'value': 3}]},
    'DL:KSN4.B41#C6': {'parts': [{'label': 'khoảng cách giữa chúng',
                                  'options': ['y nguyên', 'đổi'], 'value': 'y nguyên'}]},
    'DL:KSN4.B41#C7': {'value': 4},
    'DL:KSN4.B41#C8': {'value': 4},
    'DL:KSN4.B41#C9': {'parts': [{'label': 'có thể không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'thêm bao nhiêu', 'value': 6}]},

    'DL:KSN4.B73#C1': {'parts': [{'label': 'tử số mới', 'value': 4},
                                 {'label': 'mẫu số mới', 'value': 3}]},
    'DL:KSN4.B73#C2': {'value': 7},
    'DL:KSN4.B73#C3': {'value': 7},
    'DL:KSN4.B73#C4': {'parts': [{'label': 'chuyển qua lại thì cái gì không đổi',
                                  'options': ['tổng', 'hiệu'], 'value': 'tổng'}]},
    'DL:KSN4.B73#C5': {'parts': [{'label': 'tử số mới', 'value': 4},
                                 {'label': 'mẫu số mới', 'value': 5},
                                 {'label': 'tổng', 'value': 9}]},
    'DL:KSN4.B73#C6': {'parts': [{'label': 'bên này bớt bao nhiêu thì bên kia thêm',
                                  'options': ['bấy nhiêu', 'gấp đôi'],
                                  'value': 'bấy nhiêu'}]},
    'DL:KSN4.B73#C7': {'value': 12},
    'DL:KSN4.B73#C8': {'value': 2},
    'DL:KSN4.B73#C9': {'parts': [{'label': 'cùng thêm thì cái gì không đổi',
                                  'options': ['hiệu', 'tổng'], 'value': 'hiệu'},
                                 {'label': 'chuyển qua lại thì cái gì không đổi',
                                  'options': ['tổng', 'hiệu'], 'value': 'tổng'}]},

    'DL:KSN4.B42#C1': {'parts': [{'label': 'của số gạo ban đầu là mấy tấn', 'value': 20}]},
    'DL:KSN4.B42#C2': {'value': 15},
    'DL:KSN4.B42#C3': {'value': 5},
    'DL:KSN4.B42#C4': {'parts': [{'label': 'phân số ấy là của',
                                  'options': ['chỗ còn lại', 'số ban đầu'],
                                  'value': 'chỗ còn lại'}]},
    'DL:KSN4.B42#C5': {'value': 16},
    'DL:KSN4.B42#C6': {'value': 24},
    'DL:KSN4.B42#C7': {'parts': [{'label': 'số bạn nữ', 'value': 24},
                                 {'label': 'số bạn nam', 'value': 8}]},
    'DL:KSN4.B42#C8': {'parts': [{'label': 'còn lại sau ngày đầu', 'value': 5},
                                 {'label': 'ngày sau bán', 'value': 1}]},
    'DL:KSN4.B42#C9': {'value': 4},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    van = ' '.join(x['text'] + x['loiChua'] for x in B68['cau'])
    if 'quy đồng' in van:
        loi.append('B68 là bài KHÁI NIỆM, chưa được dạy quy đồng')
    cu = {f'DL:KSN4.B{n}' for n in (38, 39, 40, 41, 42)}
    moi_ = {f'DL:KSN4.B{n}' for n in (68, 69, 70, 71, 72, 73)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')
    # Bộ neo 3/4 — mọi con số đã kiểm bằng máy trước khi viết, xem chú thích đầu tệp.
    for b in MOI:
        van = json.dumps(b, ensure_ascii=False)
        if 'ba phần tư' not in van and '3/4' not in van and 'ba phần bốn' not in van:
            loi.append(f'{b["id"]}: thiếu bộ neo ba phần tư của chương')
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

    tt = json.loads(THU_TU.read_text('utf8'))
    ds = [x for x in tt['thuTu'] if x not in SAU]
    ds.insert(ds.index('DL:KSN4.B38'), 'DL:KSN4.B68')      # bài khái niệm đứng đầu chương
    for moi_ma, sau_ma in SAU.items():
        if sau_ma:
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
