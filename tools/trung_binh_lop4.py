# -*- coding: utf-8 -*-
"""CHƯƠNG 5 · TRUNG BÌNH CỘNG — ba bài cũ tách thành SÁU, mỗi bài một việc.

Cùng ba luật bác ra ở đợt 2 (xem `chia_het_lop4.py`), và cùng một lỗ thủng ở gốc:
**không bài nào nói trung bình cộng LÀ GÌ**. Bài đầu vào thẳng "san bằng" rồi quay
sang bài toán ngược ngay trong cùng một bài.

Ba bài cũ đang gộp:
  · B21 dạy tính trung bình cộng **và** bài toán ngược (biết trung bình tìm số);
  · B22 dạy hơn kém mức trung bình;
  · B23 dạy thêm một số vào nhóm.

Nay sáu bài. Bốn bài đầu đi đúng một mạch: *trung bình cộng là gì* → *tính nó* →
*công thức ngược* → *dùng công thức ngược để tìm số còn thiếu*.

── SỐ NEO CHUNG CẢ CHƯƠNG ──
`4 ; 6 ; 8` chạy suốt sáu bài. Chọn bộ này vì ba lý do, và cả ba đều để bé NHÌN THẤY
thay vì phải tin:
  · tổng 18, chia 3 được đúng 6 — không lẻ, không phải làm quen số xấu;
  · số giữa (6) đúng bằng trung bình, nên "san bằng" thấy ngay là cột 8 nhường 2 cho
    cột 4, còn cột 6 đứng yên;
  · phần nhô lên trên mức trung bình (2) đúng bằng phần hụt xuống dưới (2) — đó là
    toàn bộ bài "hơn kém mức trung bình", nhìn là hiểu.

── MÃ BÀI (lối C) ──
Ba mã cũ B21 B22 B23 GIỮ NGUYÊN, ba bài mới lấy mã trống kế tiếp B55 tới B57. Chèn
vào `thu_tu.json` là xong — không đổi mã nào, không dời tiến độ của bé nào.

    python3 tools/trung_binh_lop4.py --xem     # in ra, chưa ghi
    python3 tools/trung_binh_lop4.py           # ghi vào data/lop4/
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

TEN_CHUONG = 'TRUNG BÌNH CỘNG'
CHUONG = 5
CO_KHONG = ['có', 'không']

LUI_HAI_BUOC = {'ve': ['DL:KSN3.B17'], 'ten': ['BÀI TOÁN HAI BƯỚC TÍNH'],
                'canCu': 'chuDe', 'lopDuoi': 3}
LUI_SAN = {'ve': ['DL:KSN3.B18', 'DL:KSN3.B19'],
           'ten': ['HƠN MẤY ĐƠN VỊ HAY GẤP MẤY LẦN?', 'THÊM BỚT ĐỂ BẰNG NHAU'],
           'canCu': 'sach', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng VIDEO thay cả mở bài lẫn bài giảng — bốn mục ②③④⑤ để RỖNG."""
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B55 · TRUNG BÌNH CỘNG LÀ GÌ — bài KHÁI NIỆM
# ═══════════════════════════════════════════════════════════════════════════
# Bài này KHÔNG giải bài toán nào. Nó chỉ làm một việc: cho bé thấy "san bằng" là gì,
# rồi chỉ ra rằng san bằng bằng tay và lấy tổng chia đều cho ra CÙNG MỘT kết quả —
# đó chính là chỗ công thức sinh ra. Nói được vì sao rồi thì năm bài sau chỉ còn là
# năm cách dùng.
B55 = bai(
    55, 'TRUNG BÌNH CỘNG LÀ GÌ — SAN CHO BẰNG NHAU',
    'Dạng gốc: LV 1.0 mức Lớp 4 — Khái niệm trung bình cộng qua phép san bằng, và vì '
    'sao san bằng cho ra cùng kết quả với lấy tổng chia đều.',
    'Lớp 3 con đã làm bài "thêm bớt để bằng nhau". Hôm nay con gọi đúng tên việc ấy: '
    'san cho bằng nhau thì mỗi phần được bao nhiêu, con số đó gọi là trung bình cộng. '
    'Hiểu nó là gì rồi thì năm bài sau chỉ còn là năm cách dùng.',
    LUI_SAN,
    video(
        ['Nói được trung bình cộng là con số khi đã san đều cho các phần.',
         'Giải thích được vì sao lấy tổng chia cho số lượng lại ra đúng con số ấy.',
         'Tính được trung bình cộng của hai hoặc ba số.'],
        ['Đề bài: Ba bạn có 4, 6 và 8 cái kẹo. Nếu chia lại cho ba bạn bằng nhau thì '
         'mỗi bạn được mấy cái?',
         'Cách 1 — san bằng tay',
         'Bạn có 8 cái nhường 2 cái cho bạn có 4 cái. Bạn có 6 cái đứng yên.',
         'Xong thì cả ba bạn đều có 6 cái.',
         'Cách 2 — gộp lại rồi chia đều',
         'Gộp hết: 4 + 6 + 8 = 18 cái.',
         'Chia đều cho 3 bạn: 18 : 3 = 6 cái.',
         'Hai cách cho cùng một kết quả',
         'Đều ra 6. Vì san bằng chỉ là chuyển kẹo qua lại, tổng số kẹo không đổi — '
         'nên gộp lại rồi chia đều cũng thế.',
         'Đáp số: mỗi bạn được 6 cái. Số 6 gọi là trung bình cộng của 4, 6 và 8.'],
        ['Có bạn nhìn ba số 4, 6, 8 rồi nói: "Trung bình cộng là 18, vì cộng lại được 18."',
         'Gợi ý 1: Con thử xem: nếu mỗi bạn được 18 cái thì ba bạn cần bao nhiêu cái?',
         'Gợi ý 2: Cần tới 54 cái, mà cả ba bạn cộng lại chỉ có 18 cái thôi.',
         'Chữa: 18 mới là TỔNG. Muốn ra trung bình cộng thì còn phải chia cho số phần: '
         '18 : 3 = 6.'],
        ['Lấy ba nắm hạt không bằng nhau rồi bảo con san cho đều. Con làm xong hãy hỏi: '
         '"Mỗi phần được mấy hạt?" — đó chính là trung bình cộng.',
         'Con nhầm trung bình cộng với tổng là chuyện rất thường. Bố mẹ hỏi lại: '
         '"Con vừa cộng xong, nhưng chia cho mấy phần rồi?"'],
    ),
    [
        lt(1, 1, 'Ba bạn có 4, 6 và 8 cái kẹo — đúng bộ số trong video. Gộp lại thì '
                 'được bao nhiêu cái?',
           '4 + 6 + 8 = 18 cái.'),
        lt(2, 1, 'Vẫn 18 cái kẹo chia đều cho 3 bạn. Mỗi bạn được mấy cái?',
           '18 : 3 = 6 cái. Vậy trung bình cộng của 4, 6 và 8 là 6.'),
        lt(3, 1, 'Tìm trung bình cộng của hai số 10 và 20.',
           'Tổng là 10 + 20 = 30, chia cho 2 số: 30 : 2 = 15.'),
        lt(4, 2, 'Tìm trung bình cộng của ba số 12, 15 và 18.',
           'Tổng là 12 + 15 + 18 = 45, chia cho 3 số: 45 : 3 = 15.'),
        lt(5, 2, 'Bạn Nam nói: "Trung bình cộng của 4, 6 và 8 là 18." Bạn nói đúng hay '
                 'sai? Số đúng là bao nhiêu?',
           'SAI. 18 mới là tổng, còn phải chia cho 3 phần nữa: 18 : 3 = 6.'),
        lt(6, 2, 'Vì sao san bằng bằng tay và lấy tổng chia đều lại cho cùng một kết quả?',
           'Vì san bằng chỉ là chuyển bớt từ phần nhiều sang phần ít, TỔNG không đổi. '
           'Tổng không đổi mà chia đều cho cùng số phần thì kết quả phải như nhau.'),
        lt(7, 2, 'Ba bạn có 5, 5 và 5 cái kẹo. Trung bình cộng bằng bao nhiêu? Con có '
                 'cần tính không?',
           'Bằng 5. Ba phần đã bằng nhau sẵn nên không phải san gì, trung bình cộng '
           'chính là con số đó.'),
        lt(8, 3, 'Tìm trung bình cộng của bốn số 2, 4, 6 và 8.',
           'Tổng là 2 + 4 + 6 + 8 = 20, chia cho 4 số: 20 : 4 = 5.'),
        lt(9, 3, 'Một bạn có 9 cái kẹo, một bạn có 3 cái. San cho bằng nhau thì mỗi bạn '
                 'được mấy cái, và bạn nhiều phải nhường mấy cái?',
           'Trung bình cộng: (9 + 3) : 2 = 6 cái mỗi bạn. Bạn có 9 cái phải nhường '
           '9 − 6 = 3 cái.'),
        q_tf(1, 'Trung bình cộng là con số mà mỗi phần nhận được khi đã san đều.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Trung bình cộng của 4, 6 và 8 là 18.', False,
             'SAI — 18 là tổng. Trung bình cộng là 18 : 3 = 6.'),
        q_mcq(3, 'Trung bình cộng của 4, 6 và 8 là:',
              ['A. 6', 'B. 18', 'C. 8'], 'A. 6', 'Tổng 18 chia cho 3 số được 6.'),
        q_mcq(4, 'Muốn tìm trung bình cộng, sau khi cộng hết các số lại ta phải:',
              ['A. chia cho số lượng các số', 'B. nhân với số lượng các số',
               'C. giữ nguyên'], 'A. chia cho số lượng các số',
              'Cộng rồi chia đều — đó là san bằng.'),
        q_mcq(5, 'Trung bình cộng của 10 và 20 là:',
              ['A. 15', 'B. 30', 'C. 10'], 'A. 15', '(10 + 20) : 2 = 15.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B21 · TÌM TRUNG BÌNH CỘNG CỦA NHIỀU SỐ  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ dạy tính trung bình cộng VÀ bài toán ngược trong cùng một chỗ. Nay chỉ còn
# chiều thuận — nhưng làm cho kỹ: đếm đúng SỐ LƯỢNG là chỗ bé sai nhiều nhất, và số
# có thể lặp lại mà vẫn phải đếm đủ.
B21 = bai(
    21, 'TÌM TRUNG BÌNH CỘNG — ĐẾM ĐÚNG XEM CÓ MẤY SỐ',
    'Dạng gốc: LV 1.1 mức Lớp 4 — Tính trung bình cộng của nhiều số, nhấn vào việc '
    'đếm đúng số lượng các số.',
    'Bài trước con đã biết trung bình cộng là gì và công thức từ đâu ra. Hôm nay con '
    'dùng nó cho thật thạo — và chú ý một chỗ rất hay sai: chia cho mấy. Chia nhầm số '
    'là hỏng cả bài dù cộng đúng.',
    LUI_HAI_BUOC,
    video(
        ['Tính được trung bình cộng của ba, bốn hay năm số.',
         'Đếm đúng số lượng các số, kể cả khi có số lặp lại.',
         'Biết trung bình cộng luôn nằm giữa số bé nhất và số lớn nhất.'],
        ['Đề bài: Đội bóng ghi bàn trong 4 trận: 2 ; 5 ; 2 ; 3 bàn. Trung bình mỗi '
         'trận đội ghi mấy bàn?',
         'Cộng hết lại',
         '2 + 5 + 2 + 3 = 12 bàn.',
         'Đếm xem có mấy số',
         'Có 4 trận nên có 4 số. Số 2 xuất hiện hai lần thì vẫn đếm là hai số.',
         'Chia đều',
         '12 : 4 = 3 bàn.',
         'Soi lại cho chắc',
         'Số bé nhất là 2, số lớn nhất là 5. Kết quả 3 nằm giữa hai số ấy nên hợp lý.',
         'Đáp số: trung bình mỗi trận đội ghi 3 bàn.'],
        ['Có bạn tính 2 + 5 + 2 + 3 = 12 rồi chia cho 3, vì "chỉ có ba số khác nhau là '
         '2, 5 và 3".',
         'Gợi ý 1: Đề nói đội đá mấy trận?',
         'Gợi ý 2: Bốn trận thì có bốn con số, dù hai trận cùng ghi 2 bàn.',
         'Chữa: phải chia cho 4, được 12 : 4 = 3 bàn. Số lặp lại vẫn đếm đủ số lần.'],
        ['Hỏi con điểm mấy bài kiểm tra rồi bảo tính điểm trung bình. Nếu có hai bài '
         'cùng điểm, con sẽ gặp đúng cái bẫy trong bài.',
         'Có một cách soi rất nhanh: trung bình cộng phải nằm giữa số bé nhất và số '
         'lớn nhất. Ra ngoài khoảng đó là chắc chắn sai.'],
    ),
    [
        lt(1, 1, 'Đội ghi bàn 4 trận: 2 ; 5 ; 2 ; 3 — đúng bài trong video. Tổng số bàn '
                 'là bao nhiêu?',
           '2 + 5 + 2 + 3 = 12 bàn.'),
        lt(2, 1, 'Vẫn bài trên. Có mấy số cần chia, và trung bình mỗi trận ghi mấy bàn?',
           'Có 4 số (4 trận). 12 : 4 = 3 bàn.'),
        lt(3, 1, 'Tìm trung bình cộng của ba số 4, 6 và 8.',
           '(4 + 6 + 8) : 3 = 18 : 3 = 6.'),
        lt(4, 2, 'Tìm trung bình cộng của năm số 3, 3, 4, 5 và 5.',
           'Tổng 3 + 3 + 4 + 5 + 5 = 20; có 5 số nên 20 : 5 = 4.'),
        lt(5, 2, 'Bạn Lan tính trung bình của 2 ; 5 ; 2 ; 3 rồi chia cho 3 vì "chỉ có ba '
                 'số khác nhau". Bạn sai ở đâu? Kết quả đúng là bao nhiêu?',
           'Sai ở chỗ đếm: bốn trận là bốn số, số lặp lại vẫn đếm đủ. Đúng là 12 : 4 = 3.'),
        lt(6, 2, 'Trung bình cộng của 10, 20 và 60 là bao nhiêu? Kết quả có nằm giữa số '
                 'bé nhất và số lớn nhất không?',
           '(10 + 20 + 60) : 3 = 90 : 3 = 30. Số 30 nằm giữa 10 và 60 nên hợp lý.'),
        lt(7, 2, 'Một bạn tính trung bình cộng của 8, 9 và 10 rồi ra 30. Không cần tính '
                 'lại, hãy chỉ ra bạn ấy chắc chắn sai.',
           'Trung bình cộng phải nằm giữa 8 và 10, mà 30 lớn hơn cả số lớn nhất. Vậy '
           'chắc chắn sai (đúng là 9).'),
        lt(8, 3, 'Bốn bạn cân nặng 28 kg, 30 kg, 31 kg và 35 kg. Cân nặng trung bình '
                 'của bốn bạn là bao nhiêu?',
           'Tổng 28 + 30 + 31 + 35 = 124 kg; 124 : 4 = 31 kg.'),
        lt(9, 3, 'Trong tuần, một cửa hàng bán được 12, 15, 18, 12 và 13 chiếc áo. Trung '
                 'bình mỗi ngày bán mấy chiếc?',
           'Tổng 12 + 15 + 18 + 12 + 13 = 70 chiếc; có 5 ngày nên 70 : 5 = 14 chiếc.'),
        q_tf(1, 'Nếu một số xuất hiện hai lần thì khi đếm ta vẫn tính là hai số.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Trung bình cộng của 8, 9 và 10 có thể bằng 30.', False,
             'SAI — trung bình cộng luôn nằm giữa số bé nhất và số lớn nhất.'),
        q_mcq(3, 'Trung bình cộng của 2 ; 5 ; 2 ; 3 là:',
              ['A. 3', 'B. 4', 'C. 12'], 'A. 3', 'Tổng 12 chia cho 4 số được 3.'),
        q_mcq(4, 'Trung bình cộng của 4, 6 và 8 là:',
              ['A. 6', 'B. 9', 'C. 18'], 'A. 6', '18 : 3 = 6.'),
        q_mcq(5, 'Trung bình cộng của một nhóm số luôn:',
              ['A. nằm giữa số bé nhất và số lớn nhất',
               'B. lớn hơn mọi số trong nhóm', 'C. bằng số lớn nhất'],
              'A. nằm giữa số bé nhất và số lớn nhất',
              'Vì nó là kết quả của việc san đều.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B56 · BIẾT TRUNG BÌNH CỘNG, TÌM TỔNG
# ═══════════════════════════════════════════════════════════════════════════
# Công thức ngược, và luật 10 của bác nằm đúng ở đây: không nêu "tổng bằng trung bình
# nhân số lượng" như một điều phải nhớ, mà cho thấy nó chính là phép chia đọc ngược
# lại — mỗi phần có ngần ấy, có ngần này phần, gộp lại thì được bấy nhiêu.
B56 = bai(
    56, 'BIẾT TRUNG BÌNH CỘNG, TÌM TỔNG — ĐỌC NGƯỢC PHÉP CHIA',
    'Dạng gốc: LV 1.2 mức Lớp 4 — Từ trung bình cộng và số lượng suy ra tổng, dựa '
    'trên quan hệ ngược giữa nhân và chia.',
    'Hai bài trước con đi một chiều: có các số, tìm trung bình cộng. Hôm nay con đi '
    'chiều ngược lại: biết trung bình cộng rồi, tìm tổng. Con sẽ thấy nó không phải '
    'công thức mới, mà chính là phép chia cũ đọc ngược lại.',
    LUI_HAI_BUOC,
    video(
        ['Viết được công thức tổng bằng trung bình cộng nhân số lượng.',
         'Giải thích được vì sao công thức ấy đúng, không phải học thuộc.',
         'Dùng được nó cho bài toán có lời văn.'],
        ['Đề bài: Trung bình cộng của 4 số là 25. Tổng của bốn số ấy bằng bao nhiêu?',
         'Nhớ lại chiều thuận',
         'Trung bình cộng bằng tổng chia cho số lượng. Ở đây: tổng chia 4 được 25.',
         'Đọc ngược phép chia',
         'Nếu chia cho 4 được 25 thì số ban đầu phải là 25 nhân 4.',
         'Nghĩ theo cách san bằng cũng ra thế',
         'Sau khi san đều, mỗi phần có 25. Có 4 phần, nên gộp lại là 25 × 4 = 100.',
         'Tính ra',
         '25 × 4 = 100.',
         'Đáp số: tổng của bốn số là 100.'],
        ['Có bạn đọc "trung bình cộng của 4 số là 25" rồi trả lời luôn: "Tổng là 25."',
         'Gợi ý 1: 25 là số của MỘT phần hay của cả bốn phần?',
         'Gợi ý 2: Của một phần thôi. Vậy bốn phần thì bao nhiêu?',
         'Chữa: 25 là số mỗi phần sau khi đã san đều. Bốn phần thì tổng là '
         '25 × 4 = 100.'],
        ['Hỏi con kiểu đời thường: "Nhà mình bốn người, trung bình mỗi người uống 2 cốc '
         'nước một ngày, cả nhà uống mấy cốc?" Con sẽ tự nhân lên.',
         'Nếu con lúng túng, nhắc lại một câu: trung bình cộng là số của MỘT phần, còn '
         'tổng là số của TẤT CẢ các phần.'],
    ),
    [
        lt(1, 1, 'Trung bình cộng của 4 số là 25 — đúng bài trong video. Tổng của bốn số '
                 'bằng bao nhiêu?',
           'Tổng = trung bình cộng × số lượng = 25 × 4 = 100.'),
        lt(2, 1, 'Trung bình cộng của 3 số là 6. Tổng của ba số bằng bao nhiêu?',
           '6 × 3 = 18.'),
        lt(3, 1, 'Trung bình cộng của 5 số là 10. Tổng của năm số bằng bao nhiêu?',
           '10 × 5 = 50.'),
        lt(4, 2, 'Trung bình mỗi ngày một cửa hàng bán 14 chiếc áo. Trong 5 ngày cửa '
                 'hàng bán được bao nhiêu chiếc?',
           '14 × 5 = 70 chiếc.'),
        lt(5, 2, 'Bạn Bình đọc "trung bình cộng của 4 số là 25" rồi nói tổng là 25. Bạn '
                 'sai ở đâu? Tổng đúng là bao nhiêu?',
           '25 là số của MỘT phần sau khi san đều, không phải của cả bốn phần. Tổng '
           'đúng là 25 × 4 = 100.'),
        lt(6, 2, 'Vì sao lấy trung bình cộng nhân với số lượng thì được tổng?',
           'Vì trung bình cộng là số mỗi phần nhận được sau khi san đều. Có bao nhiêu '
           'phần thì gộp lại đúng bấy nhiêu lần con số ấy — mà san bằng không làm đổi tổng.'),
        lt(7, 2, 'Ba bạn có trung bình 6 cái kẹo. Cả ba bạn có tất cả mấy cái kẹo?',
           '6 × 3 = 18 cái.'),
        lt(8, 3, 'Trung bình mỗi tuần bạn Mai đọc 3 quyển sách. Trong 4 tuần bạn đọc bao '
                 'nhiêu quyển? Nếu tuần thứ năm bạn đọc 5 quyển thì bốn tuần đầu cộng '
                 'tuần năm là bao nhiêu quyển?',
           'Bốn tuần đầu: 3 × 4 = 12 quyển. Cộng tuần thứ năm: 12 + 5 = 17 quyển.'),
        lt(9, 3, 'Trung bình cộng của 6 số là 12. Nếu bớt đi một số bằng 12 thì tổng của '
                 'năm số còn lại bằng bao nhiêu?',
           'Tổng sáu số: 12 × 6 = 72. Bớt đi 12 thì còn 72 − 12 = 60.'),
        q_tf(1, 'Tổng bằng trung bình cộng nhân với số lượng các số.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Nếu trung bình cộng của 4 số là 25 thì tổng của chúng là 25.', False,
             'SAI — 25 là số của một phần. Tổng là 25 × 4 = 100.'),
        q_mcq(3, 'Trung bình cộng của 3 số là 6. Tổng của chúng là:',
              ['A. 18', 'B. 6', 'C. 9'], 'A. 18', '6 × 3 = 18.'),
        q_mcq(4, 'Muốn tìm tổng khi biết trung bình cộng, ta:',
              ['A. nhân trung bình cộng với số lượng',
               'B. chia trung bình cộng cho số lượng',
               'C. cộng trung bình cộng với số lượng'],
              'A. nhân trung bình cộng với số lượng',
              'Đó là phép chia đọc ngược lại.'),
        q_mcq(5, 'Trung bình mỗi ngày bán 14 chiếc áo, 5 ngày bán được:',
              ['A. 70 chiếc', 'B. 19 chiếc', 'C. 14 chiếc'], 'A. 70 chiếc',
              '14 × 5 = 70.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B57 · TÌM SỐ CÒN THIẾU KHI BIẾT TRUNG BÌNH CỘNG
# ═══════════════════════════════════════════════════════════════════════════
# Không có công thức mới — bài này chỉ ghép hai việc đã biết: lấy tổng (bài trước) rồi
# trừ đi phần đã biết. Tách riêng vì đây là chỗ bé phải TỰ CHỌN dùng công thức nào,
# và chọn sai thì không có gì báo.
B57 = bai(
    57, 'TÌM SỐ CÒN THIẾU — LẤY TỔNG RỒI TRỪ ĐI PHẦN ĐÃ BIẾT',
    'Dạng gốc: LV 1.3 mức Lớp 4 — Tìm một số khi biết trung bình cộng và các số còn '
    'lại; hai bước, không công thức mới.',
    'Bài trước con đã biết cách lấy tổng từ trung bình cộng. Hôm nay con dùng đúng nó '
    'để tìm một con số bị giấu đi. Không có công thức nào mới cả — chỉ là hai bước cũ '
    'nối lại: tìm tổng, rồi trừ đi những gì đã biết.',
    LUI_HAI_BUOC,
    video(
        ['Tìm được một số khi biết trung bình cộng và các số còn lại.',
         'Đi đúng hai bước: tìm tổng trước, rồi trừ.',
         'Thử lại kết quả bằng cách tính lại trung bình cộng.'],
        ['Đề bài: Trung bình cộng của hai số là 36, một số bằng 40. Tìm số còn lại.',
         'Bước 1 — tìm tổng',
         'Trung bình cộng là 36, có 2 số, nên tổng là 36 × 2 = 72.',
         'Bước 2 — trừ đi số đã biết',
         'Số còn lại là 72 − 40 = 32.',
         'Thử lại',
         'Tính trung bình cộng của 40 và 32: (40 + 32) : 2 = 72 : 2 = 36. Đúng bằng '
         'đề cho, nên bài làm đúng.',
         'Đáp số: số còn lại là 32.'],
        ['Có bạn đọc đề rồi làm luôn: "Số còn lại là 36 − 40, không trừ được nên đề sai."',
         'Gợi ý 1: 36 là trung bình cộng, còn con đang trừ nó như thể nó là tổng.',
         'Gợi ý 2: Con tìm TỔNG trước đã. Trung bình 36, có hai số thì tổng bằng mấy?',
         'Chữa: tổng là 36 × 2 = 72, rồi mới lấy 72 − 40 = 32. Phải đi tổng trước, '
         'không trừ thẳng vào trung bình cộng được.'],
        ['Cho con một bài kiểu này: "Ba bài kiểm tra con được trung bình 8 điểm, hai bài '
         'đầu được 7 và 8. Bài thứ ba mấy điểm?" Con sẽ phải đi đúng hai bước.',
         'Chỗ sai phổ biến nhất là trừ thẳng vào trung bình cộng. Bố mẹ hỏi một câu: '
         '"Con tìm tổng chưa?"'],
    ),
    [
        lt(1, 1, 'Trung bình cộng của hai số là 36 — đúng bài trong video. Tổng của hai '
                 'số bằng bao nhiêu?',
           '36 × 2 = 72.'),
        lt(2, 1, 'Vẫn bài trên, một số bằng 40. Số còn lại bằng bao nhiêu?',
           '72 − 40 = 32.'),
        lt(3, 1, 'Trung bình cộng của hai số là 10, một số bằng 6. Tìm số còn lại.',
           'Tổng là 10 × 2 = 20; số còn lại là 20 − 6 = 14.'),
        lt(4, 2, 'Trung bình cộng của ba số là 6, hai số đầu là 4 và 6. Tìm số thứ ba.',
           'Tổng là 6 × 3 = 18; số thứ ba là 18 − 4 − 6 = 8.'),
        lt(5, 2, 'Bạn An lấy thẳng 36 − 40 rồi bảo đề sai. Bạn sai ở đâu?',
           'Bạn trừ thẳng vào trung bình cộng. Phải tìm TỔNG trước: 36 × 2 = 72, rồi '
           'mới 72 − 40 = 32.'),
        lt(6, 2, 'Ba bài kiểm tra được trung bình 8 điểm; hai bài đầu được 7 và 8 điểm. '
                 'Bài thứ ba được mấy điểm?',
           'Tổng ba bài: 8 × 3 = 24. Bài thứ ba: 24 − 7 − 8 = 9 điểm.'),
        lt(7, 2, 'Sau khi tìm được số còn lại là 32, con thử lại thế nào để chắc chắn đúng?',
           'Tính lại trung bình cộng của hai số: (40 + 32) : 2 = 36 — đúng bằng đề cho.'),
        lt(8, 3, 'Trung bình cộng của bốn số là 15; ba số đầu là 10, 14 và 20. Tìm số '
                 'thứ tư và thử lại.',
           'Tổng: 15 × 4 = 60. Số thứ tư: 60 − 10 − 14 − 20 = 16. Thử lại: '
           '(10 + 14 + 20 + 16) : 4 = 60 : 4 = 15.'),
        lt(9, 3, 'Bốn bạn cân nặng trung bình 30 kg. Ba bạn đầu nặng 28 kg, 29 kg và '
                 '31 kg. Bạn thứ tư nặng bao nhiêu?',
           'Tổng: 30 × 4 = 120 kg. Bạn thứ tư: 120 − 28 − 29 − 31 = 32 kg.'),
        q_tf(1, 'Muốn tìm số còn thiếu, phải tìm tổng trước rồi mới trừ.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Trung bình cộng hai số là 36, một số là 40, vậy số kia là 36 − 40.',
             False, 'SAI — phải lấy tổng 72 trừ 40, được 32.'),
        q_mcq(3, 'Trung bình cộng của hai số là 36, một số là 40. Số còn lại là:',
              ['A. 32', 'B. 4', 'C. 76'], 'A. 32', 'Tổng 72, trừ 40 được 32.'),
        q_mcq(4, 'Trung bình cộng của ba số là 6, hai số đầu là 4 và 6. Số thứ ba là:',
              ['A. 8', 'B. 6', 'C. 18'], 'A. 8', 'Tổng 18, trừ 4 và 6 được 8.'),
        q_mcq(5, 'Cách thử lại kết quả là:',
              ['A. tính lại trung bình cộng xem có đúng đề cho không',
               'B. cộng tất cả các số lại', 'C. không cần thử'],
              'A. tính lại trung bình cộng xem có đúng đề cho không',
              'Ra đúng con số đề cho thì bài làm đúng.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B22 · HƠN KÉM MỨC TRUNG BÌNH BAO NHIÊU  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Chỗ hay của bài này: phần nhô lên trên mức trung bình LUÔN bằng đúng phần hụt xuống
# dưới. Với bộ neo 4·6·8 thì nhìn thấy ngay — cột 8 nhô 2, cột 4 hụt 2. Đó không phải
# một mẹo, mà chính là định nghĩa san bằng nhìn từ phía khác.
B22 = bai(
    22, 'HƠN KÉM MỨC TRUNG BÌNH — PHẦN NHÔ LÊN BẰNG PHẦN HỤT XUỐNG',
    'Dạng gốc: LV 1.4 mức Lớp 4 — So sánh từng số với trung bình cộng; tổng phần hơn '
    'luôn bằng tổng phần kém.',
    'Con đã biết trung bình cộng là mức san bằng. Hôm nay con nhìn kỹ hơn: mỗi số cách '
    'cái mức ấy bao xa. Và con sẽ thấy một điều rất gọn — phần nhô lên trên mức trung '
    'bình bao giờ cũng vừa đúng bằng phần hụt xuống dưới.',
    LUI_SAN,
    video(
        ['So sánh được từng số với trung bình cộng, hơn hay kém bao nhiêu.',
         'Biết tổng phần hơn luôn bằng tổng phần kém, và vì sao.',
         'Dùng điều đó để tìm một số khi biết nó hơn hay kém mức trung bình.'],
        ['Đề bài: Ba số 4 ; 6 ; 8 có trung bình cộng là 6. Mỗi số hơn hay kém mức 6 bao '
         'nhiêu?',
         'So từng số với mức 6',
         'Số 4 kém mức 6 là 2 đơn vị. Số 6 đúng bằng mức. Số 8 hơn mức 6 là 2 đơn vị.',
         'Cộng riêng hai phía',
         'Phần hơn cộng lại được 2. Phần kém cộng lại cũng được 2.',
         'Vì sao hai bên luôn bằng nhau',
         'Vì san bằng chính là lấy phần nhô lên đắp vào chỗ hụt xuống. Đắp xong vừa '
         'khít thì hai phần phải bằng nhau ngay từ đầu.',
         'Đáp số: số 4 kém 2, số 6 bằng mức, số 8 hơn 2; phần hơn và phần kém đều bằng 2.'],
        ['Có bạn thấy ba số 4 ; 6 ; 8 rồi nói: "Số 8 hơn mức trung bình 8 đơn vị."',
         'Gợi ý 1: Mức trung bình của ba số này là bao nhiêu?',
         'Gợi ý 2: Là 6. Vậy 8 hơn 6 mấy đơn vị?',
         'Chữa: 8 − 6 = 2, nên số 8 hơn mức trung bình 2 đơn vị. Phải trừ đi mức trung '
         'bình, chứ không lấy luôn con số đó.'],
        ['Vẽ ba cột cao thấp rồi kẻ một vạch ngang ở mức trung bình. Bảo con tô phần nhô '
         'lên và phần hụt xuống — con sẽ thấy hai phần bằng nhau.',
         'Đây là cách soi bài rất nhanh: cộng phần hơn và phần kém, không bằng nhau là '
         'chắc chắn tính sai trung bình cộng ở đâu đó.'],
    ),
    [
        lt(1, 1, 'Ba số 4 ; 6 ; 8 có trung bình cộng bằng bao nhiêu?',
           '(4 + 6 + 8) : 3 = 18 : 3 = 6.'),
        lt(2, 1, 'Vẫn ba số ấy. Số 8 hơn mức trung bình mấy đơn vị, số 4 kém mấy đơn vị?',
           'Số 8 hơn 8 − 6 = 2 đơn vị; số 4 kém 6 − 4 = 2 đơn vị.'),
        lt(3, 1, 'Trong ba số 4 ; 6 ; 8, số nào đúng bằng mức trung bình?',
           'Số 6 — nó đúng bằng trung bình cộng nên không hơn cũng không kém.'),
        lt(4, 2, 'Ba trận đội ghi trung bình 3 bàn. Trận một ghi nhiều hơn mức trung bình '
                 '2 bàn. Trận một ghi mấy bàn?',
           'Số bàn trận một = 3 + 2 = 5 bàn.'),
        lt(5, 2, 'Bạn Tú nói "số 8 hơn mức trung bình 8 đơn vị" khi xét ba số 4 ; 6 ; 8. '
                 'Bạn sai ở đâu? Số đúng là bao nhiêu?',
           'Bạn lấy luôn con số 8 thay vì trừ đi mức trung bình. Đúng là 8 − 6 = 2 đơn vị.'),
        lt(6, 2, 'Chiều cao trung bình của ba bạn là 130 cm. Bạn thứ nhất cao 134 cm. Bạn '
                 'ấy cao hơn mức trung bình mấy xăng-ti-mét?',
           '134 − 130 = 4 cm.'),
        lt(7, 2, 'Vì sao tổng phần hơn luôn bằng tổng phần kém?',
           'Vì san bằng chính là lấy phần nhô lên đắp vào chỗ hụt xuống. Đắp xong vừa '
           'khít, không thừa không thiếu, nên hai phần phải bằng nhau.'),
        lt(8, 3, 'Bốn số 10 ; 12 ; 14 ; 20 có trung bình cộng bằng bao nhiêu? Tổng phần '
                 'hơn và tổng phần kém bằng bao nhiêu?',
           'Trung bình: (10 + 12 + 14 + 20) : 4 = 56 : 4 = 14. Phần kém: 4 + 2 = 6; '
           'phần hơn: 0 + 6 = 6. Hai bên bằng nhau.'),
        lt(9, 3, 'Ba bạn cân nặng trung bình 30 kg. Bạn thứ nhất nhẹ hơn mức trung bình '
                 '3 kg, bạn thứ hai nặng hơn mức trung bình 5 kg. Bạn thứ ba nặng bao nhiêu?',
           'Phần hơn phải bằng phần kém. Bạn hai hơn 5, bạn nhất kém 3, nên bạn ba phải '
           'kém 2 kg: 30 − 2 = 28 kg.'),
        q_tf(1, 'Tổng phần hơn mức trung bình luôn bằng tổng phần kém mức trung bình.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Trong ba số 4 ; 6 ; 8, số 8 hơn mức trung bình 8 đơn vị.', False,
             'SAI — mức trung bình là 6, nên 8 hơn 2 đơn vị.'),
        q_mcq(3, 'Ba số 4 ; 6 ; 8 có số nào đúng bằng mức trung bình?',
              ['A. số 6', 'B. số 4', 'C. không số nào'], 'A. số 6',
              'Trung bình cộng là 6.'),
        q_mcq(4, 'Trung bình 3 bàn mỗi trận, trận một hơn mức trung bình 2 bàn thì ghi:',
              ['A. 5 bàn', 'B. 2 bàn', 'C. 1 bàn'], 'A. 5 bàn', '3 + 2 = 5.'),
        q_mcq(5, 'Vì sao phần hơn luôn bằng phần kém?',
              ['A. Vì san bằng là lấy phần nhô đắp vào chỗ hụt, vừa khít',
               'B. Vì các số luôn cách đều nhau',
               'C. Vì trung bình cộng là số lớn nhất'],
              'A. Vì san bằng là lấy phần nhô đắp vào chỗ hụt, vừa khít',
              'Đắp vừa khít nghĩa là hai phần bằng nhau.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B23 · THÊM MỘT SỐ VÀO NHÓM  (mã cũ, viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài khép chương. Nó đòi bé dùng lại CẢ HAI chiều đã học: lấy tổng cũ từ trung bình
# cũ, cộng số mới, rồi chia lại cho số lượng MỚI. Chỗ bé sai nhiều nhất không phải
# phép tính, mà là quên đổi số lượng.
B23 = bai(
    23, 'THÊM MỘT SỐ VÀO NHÓM — NHỚ ĐỔI CẢ SỐ LƯỢNG',
    'Dạng gốc: LV 1.5 mức Lớp 4 — Thêm một phần tử vào nhóm, tính lại trung bình cộng; '
    'so sánh số mới với mức trung bình cũ để đoán chiều tăng giảm.',
    'Đây là bài cuối chương, và nó dùng lại tất cả những gì con đã học: lấy tổng từ '
    'trung bình cộng, cộng thêm số mới, rồi chia lại. Chỗ dễ quên nhất không phải phép '
    'tính, mà là số lượng đã đổi rồi.',
    LUI_HAI_BUOC,
    video(
        ['Tính lại được trung bình cộng sau khi thêm một số vào nhóm.',
         'Nhớ đổi số lượng khi chia lại.',
         'Đoán được trung bình sẽ tăng hay giảm trước khi tính.'],
        ['Đề bài: Ba bạn có trung bình 6 cái kẹo. Thêm một bạn nữa có 10 cái. Trung '
         'bình của bốn bạn bây giờ là bao nhiêu?',
         'Bước 1 — lấy tổng cũ',
         'Ba bạn, trung bình 6, nên tổng cũ là 6 × 3 = 18 cái.',
         'Bước 2 — cộng số mới',
         'Tổng mới là 18 + 10 = 28 cái.',
         'Bước 3 — chia lại cho SỐ LƯỢNG MỚI',
         'Bây giờ có 4 bạn chứ không phải 3 nữa. 28 : 4 = 7 cái.',
         'Đoán trước cho chắc',
         'Bạn mới có 10 cái, nhiều hơn mức cũ là 6, nên trung bình phải TĂNG. Kết quả '
         '7 lớn hơn 6, đúng như đoán.',
         'Đáp số: trung bình của bốn bạn là 7 cái.'],
        ['Có bạn tính tổng mới là 28 rồi chia cho 3, vì "lúc đầu có ba bạn".',
         'Gợi ý 1: Bây giờ nhóm có mấy bạn rồi?',
         'Gợi ý 2: Có bốn bạn. Số kẹo chia cho bốn bạn chứ không phải ba.',
         'Chữa: phải chia cho 4, được 28 : 4 = 7. Thêm người vào nhóm thì số lượng để '
         'chia cũng đổi theo.'],
        ['Hỏi con một câu đoán trước khi tính: "Bạn mới nhiều kẹo hơn mức trung bình cũ, '
         'vậy trung bình sẽ tăng hay giảm?" Đoán đúng rồi mới tính.',
         'Chỗ con hay quên là số lượng đã đổi. Bố mẹ hỏi một câu: "Bây giờ chia cho mấy?"'],
    ),
    [
        lt(1, 1, 'Ba bạn có trung bình 6 cái kẹo — đúng bài trong video. Tổng số kẹo của '
                 'ba bạn là bao nhiêu?',
           '6 × 3 = 18 cái.'),
        lt(2, 1, 'Thêm một bạn có 10 cái. Tổng mới là bao nhiêu và có mấy bạn?',
           'Tổng mới 18 + 10 = 28 cái; nhóm nay có 4 bạn.'),
        lt(3, 1, 'Vẫn bài trên. Trung bình của bốn bạn là bao nhiêu?',
           '28 : 4 = 7 cái.'),
        lt(4, 2, 'Bốn bạn góp quỹ trung bình 10 nghìn đồng. Thêm một bạn góp 15 nghìn. '
                 'Trung bình của năm bạn là bao nhiêu?',
           'Tổng cũ 10 × 4 = 40; tổng mới 40 + 15 = 55; chia 5 bạn được 55 : 5 = 11 nghìn.'),
        lt(5, 2, 'Bạn Hoa tính tổng mới là 28 rồi chia cho 3. Bạn sai ở đâu? Kết quả '
                 'đúng là bao nhiêu?',
           'Nhóm nay có 4 bạn chứ không phải 3. Phải chia cho 4, được 28 : 4 = 7.'),
        lt(6, 2, 'Ba bạn trung bình 6 cái kẹo, thêm một bạn chỉ có 2 cái. Không cần tính '
                 'hết, hãy đoán trung bình sẽ tăng hay giảm. Vì sao?',
           'GIẢM, vì bạn mới có ít hơn mức trung bình cũ (2 nhỏ hơn 6). Tính ra: '
           '(18 + 2) : 4 = 5.'),
        lt(7, 2, 'Ba bạn trung bình 6 cái kẹo, thêm một bạn cũng có đúng 6 cái. Trung '
                 'bình mới bằng bao nhiêu?',
           'Vẫn bằng 6: (18 + 6) : 4 = 24 : 4 = 6. Thêm đúng bằng mức trung bình thì '
           'mức ấy không đổi.'),
        lt(8, 3, 'Bốn bạn góp trung bình 10 nghìn đồng. Muốn trung bình của năm bạn là '
                 '11 nghìn thì bạn thứ năm phải góp bao nhiêu?',
           'Tổng cần có: 11 × 5 = 55 nghìn. Tổng cũ 10 × 4 = 40 nghìn. Bạn thứ năm góp '
           '55 − 40 = 15 nghìn.'),
        lt(9, 3, 'Bốn tuần đầu bỏ heo trung bình mỗi tuần 7 nghìn đồng. Tuần thứ năm bỏ '
                 '12 nghìn. Trung bình mỗi tuần của cả năm tuần là bao nhiêu?',
           'Tổng bốn tuần: 7 × 4 = 28 nghìn. Tổng năm tuần: 28 + 12 = 40 nghìn. '
           'Trung bình: 40 : 5 = 8 nghìn.'),
        q_tf(1, 'Thêm một số vào nhóm thì phải chia lại cho số lượng mới.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Thêm một số đúng bằng mức trung bình cũ thì trung bình sẽ tăng.', False,
             'SAI — nó giữ nguyên.'),
        q_mcq(3, 'Ba bạn trung bình 6 cái kẹo, thêm bạn có 10 cái. Trung bình mới là:',
              ['A. 7 cái', 'B. 8 cái', 'C. 6 cái'], 'A. 7 cái', '(18 + 10) : 4 = 7.'),
        q_mcq(4, 'Thêm một số NHỎ HƠN mức trung bình cũ thì trung bình sẽ:',
              ['A. giảm', 'B. tăng', 'C. không đổi'], 'A. giảm',
              'Số mới kéo mức chung xuống.'),
        q_mcq(5, 'Bốn bạn trung bình 10 nghìn, thêm bạn góp 15 nghìn. Trung bình mới là:',
              ['A. 11 nghìn', 'B. 12 nghìn', 'C. 10 nghìn'], 'A. 11 nghìn',
              '(40 + 15) : 5 = 11.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# THỨ TỰ HỌC · Ô NHẬP CHẤM MÁY
# ═══════════════════════════════════════════════════════════════════════════
MOI = [B55, B21, B56, B57, B22, B23]
TRUOC = 'DL:KSN4.B20'          # chèn ngay sau bài cuối chương 4

O_NHAP_MOI = {
    # ── ① B55 · trung bình cộng là gì ──
    'DL:KSN4.B55#C1': {'value': 18},
    'DL:KSN4.B55#C2': {'value': 6},
    'DL:KSN4.B55#C3': {'value': 15},
    'DL:KSN4.B55#C4': {'parts': [{'label': 'tổng', 'value': 45},
                                 {'label': 'trung bình cộng', 'value': 15}]},
    'DL:KSN4.B55#C5': {'parts': [{'label': 'bạn Nam nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'số đúng', 'value': 6}]},
    'DL:KSN4.B55#C6': {'parts': [{'label': 'san bằng có làm đổi tổng không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B55#C7': {'parts': [{'label': 'trung bình cộng', 'value': 5},
                                 {'label': 'có cần tính không', 'options': CO_KHONG,
                                  'value': 'không'}]},
    'DL:KSN4.B55#C8': {'parts': [{'label': 'tổng', 'value': 20},
                                 {'label': 'trung bình cộng', 'value': 5}]},
    'DL:KSN4.B55#C9': {'parts': [{'label': 'mỗi bạn được mấy cái', 'value': 6},
                                 {'label': 'bạn nhiều nhường mấy cái', 'value': 3}]},

    # ── ② B21 · tìm trung bình cộng ──
    'DL:KSN4.B21#C1': {'value': 12},
    'DL:KSN4.B21#C2': {'parts': [{'label': 'có mấy số', 'value': 4},
                                 {'label': 'trung bình mỗi trận', 'value': 3}]},
    'DL:KSN4.B21#C3': {'value': 6},
    'DL:KSN4.B21#C4': {'parts': [{'label': 'tổng', 'value': 20},
                                 {'label': 'trung bình cộng', 'value': 4}]},
    'DL:KSN4.B21#C5': {'parts': [{'label': 'phải chia cho mấy', 'value': 4},
                                 {'label': 'kết quả đúng', 'value': 3}]},
    'DL:KSN4.B21#C6': {'parts': [{'label': 'trung bình cộng', 'value': 30},
                                 {'label': 'có nằm giữa số bé nhất và lớn nhất không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B21#C7': {'parts': [{'label': 'trung bình cộng đúng', 'value': 9}]},
    'DL:KSN4.B21#C8': {'parts': [{'label': 'tổng', 'value': 124},
                                 {'label': 'cân nặng trung bình', 'value': 31}]},
    'DL:KSN4.B21#C9': {'parts': [{'label': 'tổng', 'value': 70},
                                 {'label': 'trung bình mỗi ngày', 'value': 14}]},

    # ── ③ B56 · biết trung bình cộng, tìm tổng ──
    'DL:KSN4.B56#C1': {'value': 100},
    'DL:KSN4.B56#C2': {'value': 18},
    'DL:KSN4.B56#C3': {'value': 50},
    'DL:KSN4.B56#C4': {'value': 70},
    'DL:KSN4.B56#C5': {'parts': [{'label': 'bạn Bình nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'tổng đúng', 'value': 100}]},
    'DL:KSN4.B56#C6': {'parts': [{'label': 'trung bình cộng là số của mấy phần',
                                  'value': 1}]},
    'DL:KSN4.B56#C7': {'value': 18},
    'DL:KSN4.B56#C8': {'parts': [{'label': 'bốn tuần đầu', 'value': 12},
                                 {'label': 'cả năm tuần', 'value': 17}]},
    'DL:KSN4.B56#C9': {'parts': [{'label': 'tổng sáu số', 'value': 72},
                                 {'label': 'tổng năm số còn lại', 'value': 60}]},

    # ── ④ B57 · tìm số còn thiếu ──
    'DL:KSN4.B57#C1': {'value': 72},
    'DL:KSN4.B57#C2': {'value': 32},
    'DL:KSN4.B57#C3': {'parts': [{'label': 'tổng', 'value': 20},
                                 {'label': 'số còn lại', 'value': 14}]},
    'DL:KSN4.B57#C4': {'parts': [{'label': 'tổng', 'value': 18},
                                 {'label': 'số thứ ba', 'value': 8}]},
    'DL:KSN4.B57#C5': {'parts': [{'label': 'tổng', 'value': 72},
                                 {'label': 'số còn lại', 'value': 32}]},
    'DL:KSN4.B57#C6': {'parts': [{'label': 'tổng ba bài', 'value': 24},
                                 {'label': 'điểm bài thứ ba', 'value': 9}]},
    'DL:KSN4.B57#C7': {'parts': [{'label': 'trung bình cộng tính lại', 'value': 36}]},
    'DL:KSN4.B57#C8': {'parts': [{'label': 'tổng', 'value': 60},
                                 {'label': 'số thứ tư', 'value': 16}]},
    'DL:KSN4.B57#C9': {'parts': [{'label': 'tổng', 'value': 120},
                                 {'label': 'bạn thứ tư nặng', 'value': 32}]},

    # ── ⑤ B22 · hơn kém mức trung bình ──
    'DL:KSN4.B22#C1': {'value': 6},
    'DL:KSN4.B22#C2': {'parts': [{'label': 'số 8 hơn mấy đơn vị', 'value': 2},
                                 {'label': 'số 4 kém mấy đơn vị', 'value': 2}]},
    'DL:KSN4.B22#C3': {'value': 6},
    'DL:KSN4.B22#C4': {'value': 5},
    'DL:KSN4.B22#C5': {'parts': [{'label': 'bạn Tú nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'số đúng', 'value': 2}]},
    'DL:KSN4.B22#C6': {'value': 4},
    'DL:KSN4.B22#C7': {'parts': [{'label': 'phần hơn và phần kém có bằng nhau không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B22#C8': {'parts': [{'label': 'trung bình cộng', 'value': 14},
                                 {'label': 'tổng phần hơn', 'value': 6},
                                 {'label': 'tổng phần kém', 'value': 6}]},
    'DL:KSN4.B22#C9': {'value': 28},

    # ── ⑥ B23 · thêm một số vào nhóm ──
    'DL:KSN4.B23#C1': {'value': 18},
    'DL:KSN4.B23#C2': {'parts': [{'label': 'tổng mới', 'value': 28},
                                 {'label': 'nhóm có mấy bạn', 'value': 4}]},
    'DL:KSN4.B23#C3': {'value': 7},
    'DL:KSN4.B23#C4': {'parts': [{'label': 'tổng mới', 'value': 55},
                                 {'label': 'trung bình của năm bạn', 'value': 11}]},
    'DL:KSN4.B23#C5': {'parts': [{'label': 'phải chia cho mấy', 'value': 4},
                                 {'label': 'kết quả đúng', 'value': 7}]},
    'DL:KSN4.B23#C6': {'parts': [{'label': 'trung bình tăng hay giảm',
                                  'options': ['tăng', 'giảm', 'không đổi'],
                                  'value': 'giảm'},
                                 {'label': 'trung bình mới', 'value': 5}]},
    'DL:KSN4.B23#C7': {'value': 6},
    'DL:KSN4.B23#C8': {'parts': [{'label': 'tổng cần có', 'value': 55},
                                 {'label': 'bạn thứ năm góp', 'value': 15}]},
    'DL:KSN4.B23#C9': {'parts': [{'label': 'tổng năm tuần', 'value': 40},
                                 {'label': 'trung bình mỗi tuần', 'value': 8}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)

    # Bài khái niệm KHÔNG được dùng công thức ngược — nêu ra là hai bài sau mất chỗ đứng.
    van = ' '.join(x['text'] + x['loiChua'] for x in B55['cau'])
    if 'nhân với số lượng' in van or 'tìm tổng khi biết' in van:
        loi.append('B55 là bài KHÁI NIỆM, chưa được dạy công thức ngược')

    cu = {'DL:KSN4.B21', 'DL:KSN4.B22', 'DL:KSN4.B23'}
    moi_ = {'DL:KSN4.B55', 'DL:KSN4.B56', 'DL:KSN4.B57'}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')

    # Bộ neo 4 · 6 · 8 phải chạy suốt — luật 3 (một ví dụ chung cả cụm).
    #
    # Bộ neo xuất hiện dưới NHIỀU DẠNG, cố ý: bài đầu bày cả ba số ra ("4 + 6 + 8"),
    # bài sau chỉ nói kết quả san bằng ("6 cái"), còn bài tìm số còn thiếu thì giấu
    # một số đi và bắt bé tìm ("hai số đầu là 4 và 6" → số thứ ba là 8). Cả ba đều
    # là bộ neo ấy; bắt đúng một dạng chữ thì hoá ra ép bài phải nói cùng một câu.
    DANG_NEO = ('4 + 6 + 8', '4 ; 6 ; 8', '6 cái', 'là 4 và 6')
    for b in MOI:
        van = json.dumps(b, ensure_ascii=False)
        if not any(x in van for x in DANG_NEO):
            loi.append(f'{b["id"]}: thiếu bộ neo 4 · 6 · 8 của chương')
    return loi


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--xem', action='store_true', help='in ra, không ghi')
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

    # ⚠ GIỮ HÌNH ĐÃ GẮN — `gan_hinh_lop4.py` ghi vào chính tệp nguồn.
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

    print(f'\nghi {len(MOI)} bài vào {RA.relative_to(GOC)}')
    print(f'thứ tự học nay {len(tt["thuTu"])} bài (chèn sau {TRUOC})')
    print(f'thêm {len(O_NHAP_MOI)} ô nhập (nay {len(o)} mục)')


if __name__ == '__main__':
    main()
