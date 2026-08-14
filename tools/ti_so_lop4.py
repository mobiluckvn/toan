# -*- coding: utf-8 -*-
"""CHƯƠNG 7 · TỔNG - TỈ, HIỆU - TỈ — bốn bài cũ tách thành BẢY.

Bốn bài cũ gói đôi hết:
  · B29 gộp "tỉ số bị giấu" **với** "tổng bị giấu" — hai việc đọc hiểu khác nhau;
  · B30 gộp công thức hiệu - tỉ **với** hiệu bị giấu;
  · B31 gộp bài ba số **với** bài nối hai tỉ số qua mắt xích chung.
Và vẫn thiếu bài gốc: **không bài nào nói tỉ số là gì**, cũng không bài nào dạy cách
đọc nó trên sơ đồ. Bé được đưa thẳng vào quy trình bốn bước.

── BỘ NEO: HAI SỐ 20 VÀ 50 ──
Chọn bộ này vì một mình nó chạy được CẢ CHƯƠNG, và nối luôn với chương vừa học:

    tổng 70   ← đúng tổng của chương 6, bé vừa quen
    hiệu 30
    tỉ số 2 : 5   →  tổng gồm 7 phần, hiệu gồm 3 phần, mỗi phần 10

Nên bài tổng - tỉ và bài hiệu - tỉ dùng CHUNG MỘT BỨC TRANH, chỉ khác chỗ nhìn: một
bên nhìn cả bảy phần, một bên nhìn ba phần chênh. Bé thấy chúng là một, không phải
hai quy trình phải nhớ.

── MÃ BÀI (lối C) ──
Bốn mã cũ B28 tới B31 GIỮ NGUYÊN, ba bài mới lấy mã trống kế tiếp B61 tới B63.

    python3 tools/ti_so_lop4.py --xem     # in ra, chưa ghi
    python3 tools/ti_so_lop4.py           # ghi vào data/lop4/
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

TEN_CHUONG = 'TỔNG - TỈ, HIỆU - TỈ'
CHUONG = 7
CO_KHONG = ['có', 'không']

LUI_TI = {'ve': ['DL:KSN3.B18', 'DL:KSN3.B09'],
          'ten': ['HƠN MẤY ĐƠN VỊ HAY GẤP MẤY LẦN?', 'TÌM MỘT PHẦN MẤY CỦA MỘT SỐ'],
          'canCu': 'sach', 'lopDuoi': 3}
LUI_GAP = {'ve': ['DL:KSN3.B18'], 'ten': ['HƠN MẤY ĐƠN VỊ HAY GẤP MẤY LẦN?'],
           'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B61 · TỈ SỐ LÀ GÌ — bài KHÁI NIỆM, KHÔNG một phép tính nào
# ═══════════════════════════════════════════════════════════════════════════
B61 = bai(
    61, 'TỈ SỐ LÀ GÌ — VẼ THÀNH NHỮNG PHẦN BẰNG NHAU',
    'Dạng gốc: LV 3.0 mức Lớp 4 — Khái niệm tỉ số và cách đọc nó trên sơ đồ đoạn '
    'thẳng chia phần bằng nhau. KHÔNG công thức, KHÔNG bài toán.',
    'Chương trước con đã vẽ được hai đoạn thẳng và biết khúc dôi ra là hiệu. Hôm nay '
    'vẫn hai đoạn ấy, nhưng con chia chúng thành những phần bằng nhau. Chia được rồi '
    'thì sáu bài sau con nhìn hình là ra cách làm.',
    LUI_GAP,
    video(
        ['Đọc được tỉ số 2 trên 5 nghĩa là gì.',
         'Vẽ được sơ đồ chia phần bằng nhau cho một tỉ số.',
         'Đếm được tổng số phần và số phần chênh nhau.'],
        ['Đề bài: Hai số có tỉ số là 2 trên 5. Hãy vẽ sơ đồ và cho biết cả hai gộp lại '
         'gồm mấy phần, chênh nhau mấy phần.',
         'Đọc tỉ số',
         'Tỉ số 2 trên 5 nghĩa là: số bé gồm 2 phần, số lớn gồm 5 phần, và mọi phần '
         'đều bằng nhau.',
         'Vẽ ra',
         'Đoạn ngắn chia 2 phần, đoạn dài chia 5 phần. Các phần vẽ rộng bằng nhau — đây '
         'là điều quan trọng nhất.',
         'Đếm tổng số phần',
         '2 + 5 = 7. Cả hai gộp lại gồm 7 phần bằng nhau.',
         'Đếm số phần chênh',
         '5 − 2 = 3. Đoạn dài hơn đoạn ngắn 3 phần.',
         'Đáp số: gộp lại 7 phần, chênh nhau 3 phần. Mọi phần đều bằng nhau.'],
        ['Có bạn vẽ đoạn ngắn 2 phần, đoạn dài 5 phần, nhưng vẽ các phần của đoạn dài '
         'nhỏ hơn cho vừa giấy.',
         'Gợi ý 1: Con đo thử một phần của đoạn ngắn và một phần của đoạn dài xem.',
         'Gợi ý 2: Hai phần ấy phải rộng BẰNG NHAU thì sơ đồ mới đúng.',
         'Chữa: mọi phần phải bằng nhau. Vẽ phần to phần nhỏ thì sơ đồ nói sai tỉ số, '
         'và tính ra sẽ sai theo.'],
        ['Lấy que tính xếp thành hai hàng: hàng trên 2 que, hàng dưới 5 que. Đó chính '
         'là sơ đồ tỉ số 2 trên 5, và que nào cũng dài như nhau.',
         'Con hay vẽ phần to phần nhỏ cho vừa giấy. Bố mẹ hỏi một câu: "Các phần có '
         'bằng nhau không?"'],
    ),
    [
        lt(1, 1, 'Tỉ số hai số là 2 : 5 — đúng tỉ số trong video. Số bé gồm mấy phần và '
                 'số lớn gồm mấy phần?',
           'Số bé gồm 2 phần, số lớn gồm 5 phần, và mọi phần đều bằng nhau.'),
        lt(2, 1, 'Vẫn tỉ số ấy. Cả hai gộp lại gồm mấy phần?',
           '2 + 5 = 7 phần.'),
        lt(3, 1, 'Vẫn tỉ số ấy. Đoạn dài hơn đoạn ngắn mấy phần?',
           '5 − 2 = 3 phần.'),
        lt(4, 2, 'Hai số có tỉ số 3 : 4. Gộp lại gồm mấy phần, chênh nhau mấy phần?',
           'Gộp lại 3 + 4 = 7 phần; chênh nhau 4 − 3 = 1 phần.'),
        lt(5, 2, 'Bạn Nam vẽ đoạn dài có các phần nhỏ hơn phần của đoạn ngắn cho vừa '
                 'giấy. Bạn sai ở đâu?',
           'Mọi phần trên sơ đồ tỉ số phải BẰNG NHAU. Vẽ to nhỏ khác nhau thì sơ đồ nói '
           'sai tỉ số.'),
        lt(6, 2, 'Số lớn gấp 3 lần số bé. Viết tỉ số hai số và cho biết gộp lại mấy phần.',
           'Tỉ số là 1 : 3 (số bé 1 phần, số lớn 3 phần). Gộp lại 1 + 3 = 4 phần.'),
        lt(7, 2, 'Trên một sơ đồ, đoạn ngắn có 2 phần và đoạn dài có 5 phần. Nếu mỗi '
                 'phần bằng 10 thì hai số là bao nhiêu?',
           'Số bé = 2 × 10 = 20; số lớn = 5 × 10 = 50.'),
        lt(8, 3, 'Hai số có tỉ số 2 : 5 và cả hai gộp lại là 70. Mỗi phần bằng bao nhiêu?',
           'Gộp lại 7 phần, mà 7 phần là 70, nên mỗi phần bằng 70 : 7 = 10.'),
        lt(9, 3, 'Số bé bằng một phần tư số lớn. Viết tỉ số, cho biết gộp lại mấy phần '
                 'và chênh nhau mấy phần.',
           'Tỉ số 1 : 4. Gộp lại 5 phần, chênh nhau 3 phần.'),
        q_tf(1, 'Trên sơ đồ tỉ số, mọi phần đều phải bằng nhau.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Tỉ số 2 : 5 nghĩa là số bé bằng 2 và số lớn bằng 5.', False,
             'SAI — nó nói số PHẦN, không nói giá trị. Mỗi phần có thể bằng bao nhiêu cũng được.'),
        q_mcq(3, 'Tỉ số 2 : 5 thì cả hai gộp lại gồm:',
              ['A. 7 phần', 'B. 10 phần', 'C. 3 phần'], 'A. 7 phần', '2 + 5 = 7.'),
        q_mcq(4, 'Tỉ số 2 : 5 thì đoạn dài hơn đoạn ngắn:',
              ['A. 3 phần', 'B. 7 phần', 'C. 2 phần'], 'A. 3 phần', '5 − 2 = 3.'),
        q_mcq(5, 'Số lớn gấp 3 lần số bé thì tỉ số hai số là:',
              ['A. 1 : 3', 'B. 3 : 1', 'C. 1 : 4'], 'A. 1 : 3',
              'Số bé 1 phần, số lớn 3 phần.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B28 · BÀI TOÁN TỔNG - TỈ  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
B28 = bai(
    28, 'BÀI TOÁN TỔNG - TỈ — CHIA TỔNG CHO SỐ PHẦN',
    'Dạng gốc: LV 3.1 mức Lớp 4 — Tìm hai số biết tổng và tỉ số, dựa trên việc tổng '
    'gồm bao nhiêu phần bằng nhau.',
    'Bài trước con đã vẽ được sơ đồ tỉ số. Hôm nay con thêm một thông tin nữa: cả hai '
    'gộp lại bằng bao nhiêu. Và con sẽ thấy cách làm hiện ra ngay trên hình — không '
    'phải nhớ quy trình nào cả.',
    LUI_TI,
    video(
        ['Tìm được giá trị một phần từ tổng và tổng số phần.',
         'Từ một phần suy ra cả hai số.',
         'Thử lại bằng cách cộng hai số.'],
        ['Đề bài: Hai số có tổng bằng 70 và tỉ số là 2 trên 5. Tìm hai số.',
         'Vẽ sơ đồ',
         'Đoạn ngắn 2 phần, đoạn dài 5 phần, các phần bằng nhau. Ngoặc ngoài ghi 70.',
         'Đếm tổng số phần',
         '2 + 5 = 7 phần. Cả 7 phần ấy gộp lại đúng bằng 70.',
         'Tìm một phần',
         '7 phần là 70, nên một phần là 70 : 7 = 10.',
         'Suy ra hai số',
         'Số bé có 2 phần: 2 × 10 = 20. Số lớn có 5 phần: 5 × 10 = 50.',
         'Thử lại',
         '20 + 50 = 70, đúng bằng tổng. Và 20 so với 50 đúng là 2 so với 5.',
         'Đáp số: hai số là 20 và 50.'],
        ['Có bạn lấy luôn 70 chia 2 rồi chia 5, ra 35 và 14.',
         'Gợi ý 1: Con đếm trên sơ đồ xem cả thảy có mấy phần?',
         'Gợi ý 2: Có 7 phần chứ không phải 2 hay 5. Vậy chia cho mấy?',
         'Chữa: phải chia cho TỔNG SỐ PHẦN là 7, được một phần bằng 10. Rồi mới nhân '
         'lên: 2 phần là 20, 5 phần là 50.'],
        ['Bảo con chỉ tay đếm số phần trên sơ đồ trước khi tính. Đếm đúng 7 thì phần '
         'còn lại chỉ là một phép chia và hai phép nhân.',
         'Chỗ sai duy nhất của bài này là chia nhầm số. Bố mẹ hỏi: "Cả thảy mấy phần?"'],
    ),
    [
        lt(1, 1, 'Hai số có tổng 70 và tỉ số 2 : 5 — đúng bài trong video. Cả thảy có '
                 'mấy phần?',
           '2 + 5 = 7 phần.'),
        lt(2, 1, 'Vẫn bài trên. Một phần bằng bao nhiêu?',
           '7 phần là 70, nên một phần = 70 : 7 = 10.'),
        lt(3, 1, 'Vẫn bài trên. Tìm hai số.',
           'Số bé = 2 × 10 = 20; số lớn = 5 × 10 = 50.'),
        lt(4, 2, 'Chia 20 viên kẹo cho hai bạn theo tỉ số 1 : 3. Mỗi bạn được mấy viên?',
           'Cả thảy 1 + 3 = 4 phần. Một phần = 20 : 4 = 5. Bạn thứ nhất 5 viên, bạn thứ '
           'hai 15 viên.'),
        lt(5, 2, 'Bạn Lan lấy 70 chia 2 rồi chia 5. Bạn sai ở đâu? Kết quả đúng là gì?',
           'Phải chia cho TỔNG SỐ PHẦN là 7, không chia riêng cho 2 hay 5. Đúng là một '
           'phần bằng 10, hai số là 20 và 50.'),
        lt(6, 2, 'Tìm hai số có tổng bằng 56 và tỉ số 3 : 5.',
           'Cả thảy 8 phần. Một phần = 56 : 8 = 7. Số bé = 21; số lớn = 35.'),
        lt(7, 2, 'Bình nước cam 30 lít pha theo tỉ lệ cốt cam trên nước lọc là 2 : 3. '
                 'Mỗi thứ bao nhiêu lít?',
           'Cả thảy 5 phần. Một phần = 30 : 5 = 6 lít. Cốt cam 12 lít, nước lọc 18 lít.'),
        lt(8, 3, 'Hai lớp trồng được 45 cây, số cây lớp A bằng một nửa số cây lớp B. '
                 'Mỗi lớp trồng bao nhiêu cây?',
           'Tỉ số 1 : 2, cả thảy 3 phần. Một phần = 45 : 3 = 15. Lớp A 15 cây, lớp B 30 cây.'),
        lt(9, 3, 'Tổng hai số là 84, số lớn gấp 6 lần số bé. Tìm hai số rồi thử lại.',
           'Tỉ số 1 : 6, cả thảy 7 phần. Một phần = 12. Số bé 12, số lớn 72. Thử: '
           '12 + 72 = 84 và 72 gấp 6 lần 12.'),
        q_tf(1, 'Muốn tìm một phần, ta lấy tổng chia cho TỔNG SỐ PHẦN.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Tổng 70, tỉ số 2 : 5 thì lấy 70 chia 2 được số bé.', False,
             'SAI — phải chia cho 7 phần, được một phần bằng 10, rồi nhân 2.'),
        q_mcq(3, 'Tổng 70, tỉ số 2 : 5. Một phần bằng:',
              ['A. 10', 'B. 35', 'C. 14'], 'A. 10', '70 : 7 = 10.'),
        q_mcq(4, 'Tổng 70, tỉ số 2 : 5. Số lớn bằng:',
              ['A. 50', 'B. 20', 'C. 35'], 'A. 50', '5 phần × 10 = 50.'),
        q_mcq(5, 'Chia 20 viên kẹo theo tỉ số 1 : 3 thì bạn nhiều được:',
              ['A. 15 viên', 'B. 5 viên', 'C. 10 viên'], 'A. 15 viên',
              'Một phần 5 viên, 3 phần là 15.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B30 · BÀI TOÁN HIỆU - TỈ  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Đặt NGAY SAU bài tổng - tỉ, và dùng ĐÚNG bộ số ấy (20 và 50) — để bé thấy hai bài
# là CÙNG MỘT BỨC TRANH, chỉ khác chỗ nhìn: một bên nhìn cả 7 phần, một bên nhìn 3
# phần chênh. Đúng cách chương 6 ghép số lớn với số bé.
B30 = bai(
    30, 'BÀI TOÁN HIỆU - TỈ — CHIA HIỆU CHO SỐ PHẦN CHÊNH',
    'Dạng gốc: LV 4.1 mức Lớp 4 — Tìm hai số biết hiệu và tỉ số, dựa trên số phần '
    'chênh nhau giữa hai đoạn.',
    'Bài trước con biết tổng. Hôm nay đề không cho tổng nữa mà cho HIỆU. Con sẽ thấy '
    'vẫn đúng bức tranh ấy, chỉ khác chỗ nhìn: lần trước con nhìn cả bảy phần, lần này '
    'con nhìn ba phần chênh nhau.',
    LUI_TI,
    video(
        ['Đếm được số phần chênh nhau giữa hai đoạn.',
         'Tìm một phần từ hiệu và số phần chênh.',
         'Thấy bài hiệu - tỉ là cùng bức tranh với bài tổng - tỉ.'],
        ['Đề bài: Hai số có hiệu bằng 30 và tỉ số là 2 trên 5. Tìm hai số.',
         'Vẫn sơ đồ ấy',
         'Đoạn ngắn 2 phần, đoạn dài 5 phần. Nhưng lần này ngoặc ngoài không ghi tổng.',
         'Nhìn phần chênh',
         'Đoạn dài hơn đoạn ngắn 5 − 2 = 3 phần. Ba phần ấy chính là hiệu, tức bằng 30.',
         'Tìm một phần',
         '3 phần là 30, nên một phần là 30 : 3 = 10.',
         'Suy ra hai số',
         'Số bé 2 phần: 20. Số lớn 5 phần: 50.',
         'So với bài hôm qua',
         'Vẫn ra hai số 20 và 50. Vì đó cùng một bức tranh, chỉ khác chỗ mình nhìn vào.',
         'Đáp số: hai số là 20 và 50.'],
        ['Có bạn làm bài hiệu - tỉ mà vẫn lấy 30 chia cho 7 phần.',
         'Gợi ý 1: Số 30 trong đề là của cả hai đoạn hay chỉ của phần chênh?',
         'Gợi ý 2: Chỉ của phần chênh. Vậy phần chênh có mấy phần?',
         'Chữa: phần chênh có 3 phần, nên chia cho 3 chứ không chia cho 7. Chia 7 là '
         'nhầm sang bài tổng - tỉ.'],
        ['Hỏi con một câu trước khi tính: "Con số đề cho là của CẢ HAI đoạn hay chỉ của '
         'phần chênh?" Trả lời đúng thì con chọn đúng số để chia.',
         'Hai bài này giống nhau tới mức bé rất dễ lẫn. Bố mẹ nhấn: có tổng thì chia '
         'tổng số phần, có hiệu thì chia số phần chênh.'],
    ),
    [
        lt(1, 1, 'Hai số có hiệu 30 và tỉ số 2 : 5 — đúng bài trong video. Phần chênh '
                 'nhau có mấy phần?',
           '5 − 2 = 3 phần.'),
        lt(2, 1, 'Vẫn bài trên. Một phần bằng bao nhiêu?',
           '3 phần là 30, nên một phần = 30 : 3 = 10.'),
        lt(3, 1, 'Vẫn bài trên. Tìm hai số.',
           'Số bé = 2 × 10 = 20; số lớn = 5 × 10 = 50.'),
        lt(4, 2, 'Hai số có hiệu 24 và tỉ số 1 : 4. Tìm hai số.',
           'Phần chênh 3 phần. Một phần = 24 : 3 = 8. Số bé 8, số lớn 32.'),
        lt(5, 2, 'Bạn Tú làm bài hiệu - tỉ mà lấy 30 chia cho 7. Bạn sai ở đâu?',
           'Số 30 là của phần CHÊNH, mà phần chênh chỉ có 3 phần. Chia cho 7 là nhầm '
           'sang bài tổng - tỉ.'),
        lt(6, 2, 'Mẹ hơn con 30 tuổi, tuổi con bằng một phần tư tuổi mẹ. Tính tuổi mỗi người.',
           'Tỉ số 1 : 4, phần chênh 3 phần. Một phần = 30 : 3 = 10. Con 10 tuổi, mẹ 40 tuổi.'),
        lt(7, 2, 'Vì sao bài tổng - tỉ chia cho 7 mà bài hiệu - tỉ lại chia cho 3?',
           'Vì con số đề cho ứng với phần khác nhau: tổng ứng với cả 7 phần, còn hiệu '
           'chỉ ứng với 3 phần chênh nhau.'),
        lt(8, 3, 'Số lớn hơn số bé 45, số bé bằng hai phần năm số lớn. Tìm hai số.',
           'Tỉ số 2 : 5, phần chênh 3 phần. Một phần = 45 : 3 = 15. Số bé 30, số lớn 75.'),
        lt(9, 3, 'Hai số có hiệu 30 và tỉ số 2 : 5. Tìm hai số, rồi cho biết tổng của '
                 'chúng bằng bao nhiêu.',
           'Một phần 10, hai số là 20 và 50. Tổng = 20 + 50 = 70 — đúng bằng bài tổng - '
           'tỉ hôm trước, vì cùng một bức tranh.'),
        q_tf(1, 'Bài hiệu - tỉ thì lấy hiệu chia cho số phần CHÊNH nhau.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Bài hiệu - tỉ cũng chia cho tổng số phần như bài tổng - tỉ.', False,
             'SAI — hiệu chỉ ứng với phần chênh.'),
        q_mcq(3, 'Hiệu 30, tỉ số 2 : 5. Phần chênh có:',
              ['A. 3 phần', 'B. 7 phần', 'C. 5 phần'], 'A. 3 phần', '5 − 2 = 3.'),
        q_mcq(4, 'Hiệu 30, tỉ số 2 : 5. Một phần bằng:',
              ['A. 10', 'B. 6', 'C. 15'], 'A. 10', '30 : 3 = 10.'),
        q_mcq(5, 'Có tổng thì chia cho tổng số phần, có hiệu thì chia cho:',
              ['A. số phần chênh nhau', 'B. tổng số phần', 'C. số phần của số bé'],
              'A. số phần chênh nhau', 'Vì hiệu chỉ ứng với phần chênh.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B62 · KHI ĐỀ GIẤU TỈ SỐ
# ═══════════════════════════════════════════════════════════════════════════
# Tách ra khỏi B29 cũ. Đây là bài ĐỌC HIỂU: "gấp rưỡi", "bằng hai phần ba", "gấp ba
# lần" đều là tỉ số nói bằng lời. Dịch được thành hai con số rồi thì bài chỉ còn là
# bài đã học.
B62 = bai(
    62, 'KHI ĐỀ GIẤU TỈ SỐ — DỊCH CÂU CHỮ THÀNH HAI CON SỐ',
    'Dạng gốc: LV 3.2 mức Lớp 4 — Tỉ số ẩn trong lời văn: gấp rưỡi, gấp mấy lần, bằng '
    'mấy phần mấy.',
    'Hai bài vừa rồi đề cho sẵn tỉ số dạng hai chấm. Nhưng đề thật thường nói bằng lời: '
    '"gấp rưỡi", "bằng hai phần ba". Hôm nay con học đúng một việc — dịch mấy câu ấy '
    'thành hai con số.',
    LUI_GAP,
    video(
        ['Dịch được mấy cách nói quen thuộc thành tỉ số.',
         'Hiểu gấp rưỡi nghĩa là gấp một lần rưỡi, tức tỉ số 2 trên 3.',
         'Dịch xong thì làm tiếp như bài đã học.'],
        ['Đề bài: Khay có 40 chiếc bánh, số bánh nướng gấp rưỡi số bánh dẻo. Tính số '
         'bánh mỗi loại.',
         'Đề không cho tỉ số dạng hai chấm',
         'Nó nói "gấp rưỡi". Phải dịch câu ấy ra trước.',
         'Gấp rưỡi nghĩa là gì',
         'Gấp rưỡi là gấp một lần rưỡi. Nếu bánh dẻo là 2 phần thì bánh nướng là 3 phần.',
         'Vậy tỉ số là 2 trên 3',
         'Cả thảy 2 + 3 = 5 phần. Một phần là 40 : 5 = 8 chiếc.',
         'Suy ra hai số',
         'Bánh dẻo 2 phần: 16 chiếc. Bánh nướng 3 phần: 24 chiếc.',
         'Mấy cách nói khác',
         'Gấp 3 lần là tỉ số 1 trên 3. Bằng hai phần ba là tỉ số 2 trên 3.',
         'Đáp số: bánh dẻo 16 chiếc, bánh nướng 24 chiếc.'],
        ['Có bạn dịch "gấp rưỡi" thành tỉ số 1 trên 5.',
         'Gợi ý 1: Gấp rưỡi là gấp mấy lần?',
         'Gợi ý 2: Gấp một lần rưỡi, chứ không phải năm lần.',
         'Chữa: gấp rưỡi là tỉ số 2 trên 3. Chữ "rưỡi" nghĩa là một nửa, không phải số 5.'],
        ['Đọc cho con vài câu rồi hỏi tỉ số: "gấp đôi", "gấp rưỡi", "bằng ba phần tư", '
         '"kém một nửa". Con dịch được cả bốn là nắm bài.',
         'Bài này khó ở chỗ đọc hiểu chứ không ở phép tính. Bố mẹ đọc chậm giúp con.'],
    ),
    [
        lt(1, 1, 'Số bánh nướng gấp rưỡi số bánh dẻo — đúng bài trong video. Viết tỉ số '
                 'bánh dẻo trên bánh nướng.',
           'Gấp rưỡi là gấp một lần rưỡi, nên tỉ số là 2 : 3.'),
        lt(2, 1, 'Vẫn bài trên, khay có 40 chiếc. Một phần bằng bao nhiêu chiếc?',
           'Cả thảy 5 phần, nên một phần = 40 : 5 = 8 chiếc.'),
        lt(3, 1, 'Vẫn bài trên. Tính số bánh mỗi loại.',
           'Bánh dẻo = 2 × 8 = 16 chiếc; bánh nướng = 3 × 8 = 24 chiếc.'),
        lt(4, 2, '"Số lớn gấp 3 lần số bé" thì tỉ số hai số là bao nhiêu?',
           'Tỉ số 1 : 3.'),
        lt(5, 2, 'Bạn Bình dịch "gấp rưỡi" thành tỉ số 1 : 5. Bạn sai ở đâu?',
           'Gấp rưỡi là gấp một lần RƯỠI, tức 2 : 3. Chữ "rưỡi" nghĩa là một nửa, không '
           'phải số 5.'),
        lt(6, 2, '"Số bé bằng hai phần ba số lớn" thì tỉ số là bao nhiêu, và gộp lại '
                 'mấy phần?',
           'Tỉ số 2 : 3; gộp lại 5 phần.'),
        lt(7, 2, 'Hai số có tổng 45, số lớn gấp đôi số bé. Tìm hai số.',
           'Tỉ số 1 : 2, cả thảy 3 phần. Một phần = 15. Số bé 15, số lớn 30.'),
        lt(8, 3, 'Một mảnh vườn có 60 cây, số cây cam gấp rưỡi số cây bưởi. Tính số cây '
                 'mỗi loại.',
           'Tỉ số bưởi trên cam là 2 : 3, cả thảy 5 phần. Một phần = 12. Bưởi 24 cây, '
           'cam 36 cây.'),
        lt(9, 3, 'Hai số có hiệu 20, số lớn gấp 3 lần số bé. Tìm hai số.',
           'Tỉ số 1 : 3, phần chênh 2 phần. Một phần = 20 : 2 = 10. Số bé 10, số lớn 30.'),
        q_tf(1, 'Gấp rưỡi nghĩa là gấp một lần rưỡi, tức tỉ số 2 : 3.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Gấp rưỡi nghĩa là tỉ số 1 : 5.', False,
             'SAI — "rưỡi" là một nửa, không phải số 5.'),
        q_mcq(3, '"Số lớn gấp 3 lần số bé" thì tỉ số là:',
              ['A. 1 : 3', 'B. 3 : 1', 'C. 1 : 4'], 'A. 1 : 3',
              'Số bé 1 phần, số lớn 3 phần.'),
        q_mcq(4, '"Số bé bằng hai phần ba số lớn" thì tỉ số là:',
              ['A. 2 : 3', 'B. 3 : 2', 'C. 2 : 5'], 'A. 2 : 3', 'Đọc thẳng từ phân số.'),
        q_mcq(5, 'Khay 40 chiếc, bánh nướng gấp rưỡi bánh dẻo. Bánh nướng có:',
              ['A. 24 chiếc', 'B. 16 chiếc', 'C. 20 chiếc'], 'A. 24 chiếc',
              'Một phần 8 chiếc, 3 phần là 24.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B29 · KHI ĐỀ GIẤU TỔNG HOẶC HIỆU  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Gộp tổng và hiệu vào MỘT bài là có chủ ý: kỹ năng ở đây y hệt bài "tổng bị giấu" của
# chương 6 mà bé vừa học xong, nên chỉ cần nhắc lại và cho luyện, không cần dạy mới.
B29 = bai(
    29, 'KHI ĐỀ GIẤU TỔNG HOẶC HIỆU — LÔI CON SỐ ẤY RA TRƯỚC',
    'Dạng gốc: LV 3.3 mức Lớp 4 — Tổng ẩn qua trung bình cộng hoặc chu vi; hiệu ẩn '
    'qua tuổi bất biến hoặc "bớt thì bằng". Dùng lại kỹ năng của chương trước.',
    'Chương trước con đã quen việc này: đề giấu tổng thì lôi tổng ra, giấu hiệu thì lôi '
    'hiệu ra. Hôm nay vẫn đúng kỹ năng ấy, chỉ khác là sau khi lôi ra thì con dùng tỉ '
    'số chứ không dùng công thức tổng - hiệu.',
    LUI_TI,
    video(
        ['Nhận ra tổng hoặc hiệu đang bị giấu.',
         'Lôi nó ra bằng cách đã học ở chương trước.',
         'Có rồi thì làm tiếp bằng tỉ số.'],
        ['Đề bài: Trung bình cộng của hai số là 35, số bé bằng hai phần năm số lớn. Tìm '
         'hai số.',
         'Đề giấu tổng',
         'Nó cho trung bình cộng chứ không cho tổng.',
         'Lôi tổng ra',
         'Tổng bằng trung bình cộng nhân số lượng: 35 × 2 = 70.',
         'Bây giờ mới dùng tỉ số',
         'Tỉ số 2 trên 5, cả thảy 7 phần. Một phần là 70 : 7 = 10. Hai số là 20 và 50.',
         'Một kiểu giấu hiệu',
         'Nếu đề nói mẹ hơn con 30 tuổi thì đó chính là hiệu. Tuổi mẹ hơn tuổi con bao '
         'nhiêu thì mãi mãi hơn bấy nhiêu, như con đã học ở chương trước.',
         'Đáp số: hai số là 20 và 50.'],
        ['Có bạn thấy "trung bình cộng là 35" rồi lấy luôn 35 chia cho 7 phần.',
         'Gợi ý 1: 35 là của một phần hay của cả hai số?',
         'Gợi ý 2: Là trung bình của hai số, nên tổng phải gấp đôi nó.',
         'Chữa: tổng = 35 × 2 = 70, rồi mới chia cho 7 phần. Lấy nhầm 35 thì một phần '
         'ra 5, và hai số cộng lại chỉ được 35, không khớp đề.'],
        ['Hỏi con hai câu trước khi tính: "Đề đã cho tổng chưa?" và "Đề đã cho tỉ số '
         'chưa?" Thiếu cái nào thì lôi cái ấy ra trước.',
         'Đây là bài tổng hợp, con phải tự nhận ra thiếu gì. Bố mẹ đừng chỉ luôn, để '
         'con tự soi.'],
    ),
    [
        lt(1, 1, 'Trung bình cộng của hai số là 35 — đúng bài trong video. Tổng hai số '
                 'bằng bao nhiêu?',
           'Tổng = 35 × 2 = 70.'),
        lt(2, 1, 'Vẫn bài trên, số bé bằng hai phần năm số lớn. Cả thảy mấy phần?',
           'Tỉ số 2 : 5, cả thảy 7 phần.'),
        lt(3, 1, 'Vẫn bài trên. Tìm hai số.',
           'Một phần = 70 : 7 = 10. Số bé 20, số lớn 50.'),
        lt(4, 2, 'Một hình chữ nhật có chu vi 48 m, chiều rộng bằng một nửa chiều dài. '
                 'Tính chiều dài và chiều rộng.',
           'Tổng dài rộng = 48 : 2 = 24 m. Tỉ số 1 : 2, cả thảy 3 phần. Một phần = 8 m. '
           'Chiều rộng 8 m, chiều dài 16 m.'),
        lt(5, 2, 'Bạn An lấy luôn 35 chia cho 7 phần. Bạn sai ở đâu?',
           '35 là trung bình cộng, không phải tổng. Tổng phải là 35 × 2 = 70.'),
        lt(6, 2, 'Mẹ hơn con 30 tuổi, tuổi con bằng một phần tư tuổi mẹ. Tính tuổi mỗi '
                 'người.',
           'Hiệu là 30 (mẹ hơn con). Tỉ số 1 : 4, phần chênh 3 phần. Một phần = 10. Con '
           '10 tuổi, mẹ 40 tuổi.'),
        lt(7, 2, 'Trung bình cộng hai số là 24, số lớn gấp đôi số bé. Tìm hai số.',
           'Tổng = 48. Tỉ số 1 : 2, cả thảy 3 phần. Một phần = 16. Số bé 16, số lớn 32.'),
        lt(8, 3, 'Một mảnh đất hình chữ nhật có chu vi 100 m, chiều dài gấp rưỡi chiều '
                 'rộng. Tính diện tích.',
           'Tổng dài rộng = 50 m. Tỉ số rộng trên dài là 2 : 3, cả thảy 5 phần. Một '
           'phần = 10 m. Rộng 20 m, dài 30 m. Diện tích = 600 mét vuông.'),
        lt(9, 3, 'Anh hơn em 12 tuổi. Nếu 4 năm nữa tuổi em bằng một nửa tuổi anh thì '
                 'hiện nay mỗi người bao nhiêu tuổi?',
           'Hiệu tuổi không đổi nên 4 năm nữa vẫn hơn 12. Lúc ấy tỉ số 1 : 2, phần chênh '
           '1 phần = 12. Em 12 tuổi, anh 24 tuổi. Hiện nay: em 8 tuổi, anh 20 tuổi.'),
        q_tf(1, 'Trung bình cộng của hai số là 35 thì tổng của chúng là 70.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Có thể lấy thẳng trung bình cộng chia cho tổng số phần.', False,
             'SAI — phải tìm tổng trước.'),
        q_mcq(3, 'Chu vi 48 m thì tổng chiều dài và chiều rộng là:',
              ['A. 24 m', 'B. 48 m', 'C. 96 m'], 'A. 24 m', 'Chu vi chia đôi.'),
        q_mcq(4, '"Mẹ hơn con 30 tuổi" cho ta biết:',
              ['A. hiệu', 'B. tổng', 'C. tỉ số'], 'A. hiệu', 'Đó là phần chênh nhau.'),
        q_mcq(5, 'Trung bình cộng 24, số lớn gấp đôi số bé. Số bé bằng:',
              ['A. 16', 'B. 8', 'C. 24'], 'A. 16', 'Tổng 48, ba phần, một phần 16.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B31 · BA SỐ THEO TỈ  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
B31 = bai(
    31, 'BA SỐ THEO TỈ — VẼ BA ĐOẠN, ĐẾM CẢ THẢY MẤY PHẦN',
    'Dạng gốc: LV 3.4 mức Lớp 4 — Chia một số thành ba phần theo tỉ số cho trước.',
    'Con đã làm quen bài hai số theo tỉ. Hôm nay có ba số, nên sơ đồ có ba đoạn. Cách '
    'làm y hệt: đếm cả thảy mấy phần, chia ra một phần, rồi nhân lên.',
    LUI_TI,
    video(
        ['Vẽ được sơ đồ ba đoạn theo tỉ số.',
         'Đếm đúng tổng số phần của cả ba.',
         'Tìm một phần rồi suy ra ba số.'],
        ['Đề bài: Chia 90 quyển vở cho ba lớp theo tỉ số 2 : 3 : 4. Mỗi lớp được bao '
         'nhiêu quyển?',
         'Vẽ ba đoạn',
         'Đoạn thứ nhất 2 phần, đoạn thứ hai 3 phần, đoạn thứ ba 4 phần. Mọi phần bằng nhau.',
         'Đếm cả thảy mấy phần',
         '2 + 3 + 4 = 9 phần. Cả 9 phần gộp lại đúng bằng 90 quyển.',
         'Tìm một phần',
         '9 phần là 90, nên một phần là 90 : 9 = 10 quyển.',
         'Suy ra ba số',
         'Lớp một: 2 × 10 = 20. Lớp hai: 3 × 10 = 30. Lớp ba: 4 × 10 = 40.',
         'Thử lại',
         '20 + 30 + 40 = 90, đúng bằng số vở ban đầu.',
         'Đáp số: ba lớp được 20, 30 và 40 quyển.'],
        ['Có bạn cộng 2 + 3 + 4 rồi quên, lấy 90 chia cho 3 vì có ba lớp.',
         'Gợi ý 1: Ba lớp nhưng cả thảy có mấy PHẦN?',
         'Gợi ý 2: Có 9 phần chứ không phải 3. Ba lớp nhận số phần khác nhau.',
         'Chữa: chia cho 9 phần, được một phần bằng 10. Chia cho 3 là chia đều, mà đề '
         'không nói chia đều.'],
        ['Bảo con đếm số phần bằng cách chỉ tay lên sơ đồ. Đếm ra 9 rồi thì phần còn '
         'lại rất nhanh.',
         'Chỗ sai duy nhất là chia nhầm cho SỐ LỚP thay vì SỐ PHẦN. Bố mẹ hỏi: "Cả thảy '
         'mấy phần?"'],
    ),
    [
        lt(1, 1, 'Chia 90 quyển vở theo tỉ số 2 : 3 : 4 — đúng bài trong video. Cả thảy '
                 'có mấy phần?',
           '2 + 3 + 4 = 9 phần.'),
        lt(2, 1, 'Vẫn bài trên. Một phần bằng bao nhiêu quyển?',
           '90 : 9 = 10 quyển.'),
        lt(3, 1, 'Vẫn bài trên. Mỗi lớp được bao nhiêu quyển?',
           'Lớp một 20 quyển, lớp hai 30 quyển, lớp ba 40 quyển.'),
        lt(4, 2, 'Chia 60 viên kẹo cho ba bạn theo tỉ số 1 : 2 : 3. Mỗi bạn được mấy viên?',
           'Cả thảy 6 phần. Một phần = 10. Ba bạn được 10, 20 và 30 viên.'),
        lt(5, 2, 'Bạn Hoa lấy 90 chia cho 3 vì có ba lớp. Bạn sai ở đâu?',
           'Ba lớp nhưng cả thảy 9 PHẦN, và ba lớp nhận số phần khác nhau. Chia cho 3 '
           'là chia đều, mà đề không nói chia đều.'),
        lt(6, 2, 'Ba số có tổng 84 và tỉ số 1 : 2 : 4. Tìm ba số.',
           'Cả thảy 7 phần. Một phần = 12. Ba số là 12, 24 và 48.'),
        lt(7, 2, 'Ba lớp trồng 120 cây theo tỉ số 3 : 4 : 5. Lớp trồng nhiều nhất được '
                 'bao nhiêu cây?',
           'Cả thảy 12 phần. Một phần = 10. Lớp nhiều nhất có 5 phần: 50 cây.'),
        lt(8, 3, 'Chia 96 quyển sách cho ba tủ theo tỉ số 2 : 3 : 3. Mỗi tủ bao nhiêu '
                 'quyển, và hai tủ sau có bằng nhau không?',
           'Cả thảy 8 phần. Một phần = 12. Tủ một 24 quyển, hai tủ sau đều 36 quyển — '
           'bằng nhau vì cùng 3 phần.'),
        lt(9, 3, 'Ba số có tổng 90, số thứ hai gấp đôi số thứ nhất, số thứ ba gấp ba số '
                 'thứ nhất. Tìm ba số.',
           'Tỉ số 1 : 2 : 3, cả thảy 6 phần. Một phần = 15. Ba số là 15, 30 và 45.'),
        q_tf(1, 'Bài ba số theo tỉ vẫn chia cho TỔNG SỐ PHẦN.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Chia 90 cho ba lớp theo tỉ số thì lấy 90 chia 3.', False,
             'SAI — chia cho tổng số phần, ở đây là 9.'),
        q_mcq(3, 'Tỉ số 2 : 3 : 4 thì cả thảy có:',
              ['A. 9 phần', 'B. 3 phần', 'C. 24 phần'], 'A. 9 phần', '2 + 3 + 4 = 9.'),
        q_mcq(4, 'Chia 90 theo tỉ số 2 : 3 : 4 thì một phần bằng:',
              ['A. 10', 'B. 30', 'C. 9'], 'A. 10', '90 : 9 = 10.'),
        q_mcq(5, 'Chia 60 theo tỉ số 1 : 2 : 3 thì phần lớn nhất bằng:',
              ['A. 30', 'B. 20', 'C. 10'], 'A. 30', 'Một phần 10, ba phần là 30.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑦ B63 · NỐI HAI TỈ SỐ QUA MẮT XÍCH CHUNG
# ═══════════════════════════════════════════════════════════════════════════
# Bài khó nhất chương, tách hẳn ra khỏi B31. Ý duy nhất: hai tỉ số nói về cùng một
# thứ ở giữa, nhưng đếm nó bằng hai loại phần khác nhau — phải quy về cùng một loại
# phần trước đã.
B63 = bai(
    63, 'NỐI HAI TỈ SỐ — QUY VỀ CÙNG MỘT LOẠI PHẦN',
    'Dạng gốc: LV 5.1 mức Lớp 4 — Nối hai tỉ số có chung một đại lượng, bằng cách quy '
    'số phần của đại lượng chung về cùng một con số.',
    'Bài cuối chương, và là bài khó nhất. Đề cho hai tỉ số, và có một thứ xuất hiện ở '
    'cả hai. Nhưng hai tỉ số ấy đếm nó bằng hai loại phần khác nhau — nên việc đầu tiên '
    'là làm cho chúng nói cùng một thứ tiếng.',
    LUI_TI,
    video(
        ['Nhận ra đại lượng chung của hai tỉ số.',
         'Quy số phần của đại lượng chung về cùng một con số.',
         'Nối thành một tỉ số ba số rồi làm như bài trước.'],
        ['Đề bài: Ba bạn có 90 viên bi. Bi của An so với bi của Bình là 2 trên 3. Bi của '
         'Bình so với bi của Cường là 6 trên 5. Tìm số bi mỗi bạn.',
         'Tìm mắt xích chung',
         'Bình có mặt ở cả hai tỉ số. Nhưng tỉ số đầu đếm Bình là 3 phần, tỉ số sau đếm '
         'Bình là 6 phần. Hai cách đếm khác nhau.',
         'Quy về cùng một loại phần',
         'Nhân cả tỉ số đầu với 2 thì Bình thành 6 phần: An trên Bình là 4 trên 6.',
         'Bây giờ nối được',
         'An 4 phần, Bình 6 phần, Cường 5 phần. Tỉ số ba bạn là 4 trên 6 trên 5.',
         'Làm như bài trước',
         'Cả thảy 4 + 6 + 5 = 15 phần. Một phần là 90 : 15 = 6 viên.',
         'Suy ra ba số',
         'An 24 viên, Bình 36 viên, Cường 30 viên. Thử lại: cộng đủ 90 viên.',
         'Đáp số: An 24 viên, Bình 36 viên, Cường 30 viên.'],
        ['Có bạn ghép thẳng thành 2 trên 3 trên 5, lấy luôn số phần của hai tỉ số.',
         'Gợi ý 1: Trong tỉ số đầu Bình là mấy phần? Trong tỉ số sau Bình là mấy phần?',
         'Gợi ý 2: Một bên 3, một bên 6. Cùng một bạn Bình mà hai con số khác nhau thì '
         'ghép sao được.',
         'Chữa: phải quy Bình về cùng một con số trước. Nhân tỉ số đầu với 2 để Bình '
         'thành 6, rồi mới ghép thành 4 trên 6 trên 5.'],
        ['Vẽ ba đoạn ra giấy rồi bảo con chỉ vào đoạn của Bình và hỏi: "Đoạn này có mấy '
         'phần?" Nếu hai tỉ số trả lời khác nhau thì chưa nối được.',
         'Đây là bài khó nhất chương. Con làm chậm cũng không sao, miễn nhận ra được '
         'mắt xích chung.'],
    ),
    [
        lt(1, 1, 'Bi của An so với Bình là 2 : 3, bi của Bình so với Cường là 6 : 5 — '
                 'đúng bài trong video. Bạn nào là mắt xích chung?',
           'Bình — bạn ấy có mặt ở cả hai tỉ số.'),
        lt(2, 1, 'Vẫn bài trên. Trong hai tỉ số, Bình được đếm là mấy phần?',
           'Tỉ số đầu đếm Bình 3 phần, tỉ số sau đếm Bình 6 phần — hai cách đếm khác nhau.'),
        lt(3, 1, 'Vẫn bài trên. Nhân tỉ số đầu với mấy thì Bình thành 6 phần?',
           'Nhân với 2: tỉ số An trên Bình thành 4 : 6.'),
        lt(4, 2, 'Vẫn bài trên. Viết tỉ số ba bạn và cho biết cả thảy mấy phần.',
           'Tỉ số 4 : 6 : 5, cả thảy 4 + 6 + 5 = 15 phần.'),
        lt(5, 2, 'Vẫn bài trên, ba bạn có 90 viên. Tìm số bi mỗi bạn.',
           'Một phần = 90 : 15 = 6 viên. An 24 viên, Bình 36 viên, Cường 30 viên.'),
        lt(6, 2, 'Bạn Minh ghép thẳng thành 2 : 3 : 5. Bạn sai ở đâu?',
           'Bình bị đếm là 3 phần ở tỉ số đầu và 6 phần ở tỉ số sau. Cùng một bạn mà hai '
           'con số khác nhau thì chưa ghép được, phải quy về cùng một loại phần trước.'),
        lt(7, 2, 'Tỉ số a trên b là 1 : 2, tỉ số b trên c là 4 : 5. Quy về rồi viết tỉ '
                 'số ba số.',
           'Quy b về 4: nhân tỉ số đầu với 2 được 2 : 4. Vậy tỉ số ba số là 2 : 4 : 5.'),
        lt(8, 3, 'Ba bạn có 68 viên bi. An so với Bình là 1 : 2, Bình so với Cường là '
                 '3 : 4. Tìm số bi mỗi bạn.',
           'Quy Bình về 6: tỉ số đầu thành 3 : 6, tỉ số sau thành 6 : 8. Ba bạn là '
           '3 : 6 : 8, cả thảy 17 phần. Một phần = 68 : 17 = 4. An 12 viên, Bình 24 '
           'viên, Cường 32 viên.'),
        lt(9, 3, 'Ba bạn có 100 viên bi. An so với Bình là 2 : 3, Bình so với Cường là '
                 '3 : 5. Tìm số bi mỗi bạn.',
           'Bình đã là 3 phần ở cả hai tỉ số nên nối thẳng: 2 : 3 : 5, cả thảy 10 phần. '
           'Một phần = 10. An 20 viên, Bình 30 viên, Cường 50 viên.'),
        q_tf(1, 'Muốn nối hai tỉ số, phải quy đại lượng chung về cùng một số phần.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Tỉ số 2 : 3 và 6 : 5 ghép thẳng được thành 2 : 3 : 5.', False,
             'SAI — Bình bị đếm 3 phần rồi 6 phần, phải quy về trước.'),
        q_mcq(3, 'Trong hai tỉ số An trên Bình là 2 : 3 và Bình trên Cường là 6 : 5, mắt '
                 'xích chung là:',
              ['A. Bình', 'B. An', 'C. Cường'], 'A. Bình', 'Bình có ở cả hai.'),
        q_mcq(4, 'Nhân tỉ số 2 : 3 với 2 thì được:',
              ['A. 4 : 6', 'B. 2 : 6', 'C. 4 : 3'], 'A. 4 : 6', 'Nhân cả hai vế.'),
        q_mcq(5, 'Tỉ số ba bạn là 4 : 6 : 5 và cả thảy 90 viên. Một phần bằng:',
              ['A. 6 viên', 'B. 15 viên', 'C. 10 viên'], 'A. 6 viên', '90 : 15 = 6.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
MOI = [B61, B28, B30, B62, B29, B31, B63]
TRUOC = 'DL:KSN4.B60'          # chèn ngay sau bài cuối chương 6

O_NHAP_MOI = {
    'DL:KSN4.B61#C1': {'parts': [{'label': 'số bé mấy phần', 'value': 2},
                                 {'label': 'số lớn mấy phần', 'value': 5}]},
    'DL:KSN4.B61#C2': {'value': 7},
    'DL:KSN4.B61#C3': {'value': 3},
    'DL:KSN4.B61#C4': {'parts': [{'label': 'gộp lại', 'value': 7},
                                 {'label': 'chênh nhau', 'value': 1}]},
    'DL:KSN4.B61#C5': {'parts': [{'label': 'mọi phần phải thế nào',
                                  'options': ['bằng nhau', 'khác nhau'],
                                  'value': 'bằng nhau'}]},
    'DL:KSN4.B61#C6': {'parts': [{'label': 'số bé mấy phần', 'value': 1},
                                 {'label': 'số lớn mấy phần', 'value': 3},
                                 {'label': 'gộp lại', 'value': 4}]},
    'DL:KSN4.B61#C7': {'parts': [{'label': 'số bé', 'value': 20},
                                 {'label': 'số lớn', 'value': 50}]},
    'DL:KSN4.B61#C8': {'value': 10},
    'DL:KSN4.B61#C9': {'parts': [{'label': 'gộp lại', 'value': 5},
                                 {'label': 'chênh nhau', 'value': 3}]},

    'DL:KSN4.B28#C1': {'value': 7},
    'DL:KSN4.B28#C2': {'value': 10},
    'DL:KSN4.B28#C3': {'parts': [{'label': 'số bé', 'value': 20},
                                 {'label': 'số lớn', 'value': 50}]},
    'DL:KSN4.B28#C4': {'parts': [{'label': 'bạn thứ nhất', 'value': 5},
                                 {'label': 'bạn thứ hai', 'value': 15}]},
    'DL:KSN4.B28#C5': {'parts': [{'label': 'phải chia cho mấy phần', 'value': 7},
                                 {'label': 'một phần', 'value': 10}]},
    'DL:KSN4.B28#C6': {'parts': [{'label': 'số bé', 'value': 21},
                                 {'label': 'số lớn', 'value': 35}]},
    'DL:KSN4.B28#C7': {'parts': [{'label': 'cốt cam', 'value': 12},
                                 {'label': 'nước lọc', 'value': 18}]},
    'DL:KSN4.B28#C8': {'parts': [{'label': 'lớp A', 'value': 15},
                                 {'label': 'lớp B', 'value': 30}]},
    'DL:KSN4.B28#C9': {'parts': [{'label': 'số bé', 'value': 12},
                                 {'label': 'số lớn', 'value': 72}]},

    'DL:KSN4.B30#C1': {'value': 3},
    'DL:KSN4.B30#C2': {'value': 10},
    'DL:KSN4.B30#C3': {'parts': [{'label': 'số bé', 'value': 20},
                                 {'label': 'số lớn', 'value': 50}]},
    'DL:KSN4.B30#C4': {'parts': [{'label': 'số bé', 'value': 8},
                                 {'label': 'số lớn', 'value': 32}]},
    'DL:KSN4.B30#C5': {'parts': [{'label': 'phải chia cho mấy phần', 'value': 3}]},
    'DL:KSN4.B30#C6': {'parts': [{'label': 'tuổi con', 'value': 10},
                                 {'label': 'tuổi mẹ', 'value': 40}]},
    'DL:KSN4.B30#C7': {'parts': [{'label': 'tổng ứng với mấy phần', 'value': 7},
                                 {'label': 'hiệu ứng với mấy phần', 'value': 3}]},
    'DL:KSN4.B30#C8': {'parts': [{'label': 'số bé', 'value': 30},
                                 {'label': 'số lớn', 'value': 75}]},
    'DL:KSN4.B30#C9': {'parts': [{'label': 'số bé', 'value': 20},
                                 {'label': 'số lớn', 'value': 50},
                                 {'label': 'tổng', 'value': 70}]},

    'DL:KSN4.B62#C1': {'parts': [{'label': 'bánh dẻo mấy phần', 'value': 2},
                                 {'label': 'bánh nướng mấy phần', 'value': 3}]},
    'DL:KSN4.B62#C2': {'value': 8},
    'DL:KSN4.B62#C3': {'parts': [{'label': 'bánh dẻo', 'value': 16},
                                 {'label': 'bánh nướng', 'value': 24}]},
    'DL:KSN4.B62#C4': {'parts': [{'label': 'số bé mấy phần', 'value': 1},
                                 {'label': 'số lớn mấy phần', 'value': 3}]},
    'DL:KSN4.B62#C5': {'parts': [{'label': 'gấp rưỡi là gấp mấy phần trên mấy phần',
                                  'options': ['2 : 3', '1 : 5'], 'value': '2 : 3'}]},
    'DL:KSN4.B62#C6': {'parts': [{'label': 'số bé mấy phần', 'value': 2},
                                 {'label': 'số lớn mấy phần', 'value': 3},
                                 {'label': 'gộp lại', 'value': 5}]},
    'DL:KSN4.B62#C7': {'parts': [{'label': 'số bé', 'value': 15},
                                 {'label': 'số lớn', 'value': 30}]},
    'DL:KSN4.B62#C8': {'parts': [{'label': 'cây bưởi', 'value': 24},
                                 {'label': 'cây cam', 'value': 36}]},
    'DL:KSN4.B62#C9': {'parts': [{'label': 'số bé', 'value': 10},
                                 {'label': 'số lớn', 'value': 30}]},

    'DL:KSN4.B29#C1': {'value': 70},
    'DL:KSN4.B29#C2': {'value': 7},
    'DL:KSN4.B29#C3': {'parts': [{'label': 'số bé', 'value': 20},
                                 {'label': 'số lớn', 'value': 50}]},
    'DL:KSN4.B29#C4': {'parts': [{'label': 'chiều rộng', 'value': 8},
                                 {'label': 'chiều dài', 'value': 16}]},
    'DL:KSN4.B29#C5': {'parts': [{'label': 'tổng đúng', 'value': 70}]},
    'DL:KSN4.B29#C6': {'parts': [{'label': 'tuổi con', 'value': 10},
                                 {'label': 'tuổi mẹ', 'value': 40}]},
    'DL:KSN4.B29#C7': {'parts': [{'label': 'số bé', 'value': 16},
                                 {'label': 'số lớn', 'value': 32}]},
    'DL:KSN4.B29#C8': {'parts': [{'label': 'chiều rộng', 'value': 20},
                                 {'label': 'chiều dài', 'value': 30},
                                 {'label': 'diện tích', 'value': 600}]},
    'DL:KSN4.B29#C9': {'parts': [{'label': 'tuổi em hiện nay', 'value': 8},
                                 {'label': 'tuổi anh hiện nay', 'value': 20}]},

    'DL:KSN4.B31#C1': {'value': 9},
    'DL:KSN4.B31#C2': {'value': 10},
    'DL:KSN4.B31#C3': {'parts': [{'label': 'lớp một', 'value': 20},
                                 {'label': 'lớp hai', 'value': 30},
                                 {'label': 'lớp ba', 'value': 40}]},
    'DL:KSN4.B31#C4': {'parts': [{'label': 'bạn một', 'value': 10},
                                 {'label': 'bạn hai', 'value': 20},
                                 {'label': 'bạn ba', 'value': 30}]},
    'DL:KSN4.B31#C5': {'parts': [{'label': 'phải chia cho mấy phần', 'value': 9}]},
    'DL:KSN4.B31#C6': {'parts': [{'label': 'số một', 'value': 12},
                                 {'label': 'số hai', 'value': 24},
                                 {'label': 'số ba', 'value': 48}]},
    'DL:KSN4.B31#C7': {'value': 50},
    'DL:KSN4.B31#C8': {'parts': [{'label': 'tủ một', 'value': 24},
                                 {'label': 'mỗi tủ sau', 'value': 36}]},
    'DL:KSN4.B31#C9': {'parts': [{'label': 'số một', 'value': 15},
                                 {'label': 'số hai', 'value': 30},
                                 {'label': 'số ba', 'value': 45}]},

    'DL:KSN4.B63#C1': {'parts': [{'label': 'mắt xích chung là bạn',
                                  'options': ['Bình', 'An', 'Cường'], 'value': 'Bình'}]},
    'DL:KSN4.B63#C2': {'parts': [{'label': 'tỉ số đầu đếm Bình', 'value': 3},
                                 {'label': 'tỉ số sau đếm Bình', 'value': 6}]},
    'DL:KSN4.B63#C3': {'value': 2},
    'DL:KSN4.B63#C4': {'parts': [{'label': 'An mấy phần', 'value': 4},
                                 {'label': 'Bình mấy phần', 'value': 6},
                                 {'label': 'cả thảy', 'value': 15}]},
    'DL:KSN4.B63#C5': {'parts': [{'label': 'An', 'value': 24},
                                 {'label': 'Bình', 'value': 36},
                                 {'label': 'Cường', 'value': 30}]},
    'DL:KSN4.B63#C6': {'parts': [{'label': 'Bình bị đếm hai con số khác nhau không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B63#C7': {'parts': [{'label': 'a mấy phần', 'value': 2},
                                 {'label': 'b mấy phần', 'value': 4},
                                 {'label': 'c mấy phần', 'value': 5}]},
    'DL:KSN4.B63#C8': {'parts': [{'label': 'cả thảy mấy phần', 'value': 17},
                                 {'label': 'An', 'value': 12},
                                 {'label': 'Bình', 'value': 24},
                                 {'label': 'Cường', 'value': 32}]},
    'DL:KSN4.B63#C9': {'parts': [{'label': 'An', 'value': 20},
                                 {'label': 'Bình', 'value': 30},
                                 {'label': 'Cường', 'value': 50}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)

    # B61 là bài KHÁI NIỆM: được ĐẾM phần, nhưng chưa được nêu quy trình tìm hai số.
    van = ' '.join(x['text'] + x['loiChua'] for x in B61['cau'])
    if 'chia cho tổng số phần' in van:
        loi.append('B61 là bài KHÁI NIỆM, chưa được nêu cách chia tổng cho số phần')

    cu = {f'DL:KSN4.B{n}' for n in (28, 29, 30, 31)}
    moi_ = {f'DL:KSN4.B{n}' for n in (61, 62, 63)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')

    # Bộ neo 20 và 50 (tổng 70, hiệu 30, tỉ 2 : 5) phải chạy suốt — luật 3.
    #
    # MIỄN TRỪ CÓ LÝ DO: B63 là bài nối hai tỉ số, mà nối tỉ số thì phải có BA đại
    # lượng. Bộ neo của chương là một cặp hai số, chở không nổi bài ấy — ép vào chỉ
    # ra một ví dụ gượng. Khai miễn trừ ở đây, kèm lý do, thay vì lặng lẽ bỏ phép
    # kiểm: bỏ lặng thì lần sau ai quên bộ neo ở bài khác cũng không ai hay.
    MIEN_TRU = {'DL:KSN4.B63': 'bài nối tỉ số cần ba đại lượng, neo hai số không chở được'}
    NEO = ('2 : 5', '20 và 50', '2 phần', 'hai phần năm')
    for b in MOI:
        if b['id'] in MIEN_TRU:
            continue
        van = json.dumps(b, ensure_ascii=False)
        if not any(x in van for x in NEO):
            loi.append(f'{b["id"]}: thiếu bộ neo 2 : 5 của chương')
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
                if isinstance(cu_m, dict) and cu_m.get('hinh') and not m.get('hinh'):
                    m['hinh'] = cu_m['hinh']
        tep.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n', 'utf8')
    tt = json.loads(THU_TU.read_text('utf8'))
    ds = [x for x in tt['thuTu'] if x not in {b['id'] for b in MOI}]
    i = ds.index(TRUOC) + 1
    tt['thuTu'] = ds[:i] + [b['id'] for b in MOI] + ds[i:]
    THU_TU.write_text(json.dumps(tt, ensure_ascii=False, indent=1) + '\n', 'utf8')
    o = json.loads(O_NHAP.read_text('utf8'))
    o.update(O_NHAP_MOI)
    O_NHAP.write_text(json.dumps(o, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'\nghi {len(MOI)} bài · thứ tự học nay {len(tt["thuTu"])} bài '
          f'(chèn sau {TRUOC}) · thêm {len(O_NHAP_MOI)} ô nhập')


if __name__ == '__main__':
    main()
