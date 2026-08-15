# -*- coding: utf-8 -*-
"""CHƯƠNG 10 · HÌNH HỌC — ĐỢT HAI: sáu bài về góc, hình và khối.

Đợt một đã làm sáu bài chu vi và diện tích. Còn lại hai bài chữ cũ, và cả hai đều
gộp quá nhiều thứ vào một chỗ:

  · B45 gộp **bốn thứ chẳng liên quan gì nhau** — góc, đường cao, cắt ghép, hình
    tròn. Bốn dụng cụ, bốn ý, một bài;
  · B46 gộp hình trải phẳng, đếm khối, khối lập phương.

Đợt này tách thành sáu bài, mỗi bài một việc:

    73 · B45  bốn loại góc          — ê ke là thước đo, mắt thường thì không
    74 · B78  đường cao             — từ đỉnh hạ xuống đáy, phải VUÔNG GÓC
    75 · B79  cắt rồi ghép          — diện tích không sinh không mất
    76 · B80  hình tròn             — bán kính và đường kính
    77 · B46  trải phẳng hộp ra     — sáu mặt, ba cặp
    78 · B81  đếm khối              — lát từng tầng mà đếm

── SỐ NEO ──
Ba bộ, mỗi bộ chở mấy bài liền:

    hình chữ nhật 6 nhân 4  →  bài cắt ghép, ĐÚNG bộ số của đợt một. Bé đã biết
                               diện tích 24 rồi, nên cắt đôi ra 12 là thấy ngay,
                               không phải làm quen hình mới giữa lúc học ý mới.
    hình tròn bán kính 3    →  đường kính 6. Hai số nhỏ, nhân đôi nhẩm được.
    hộp 4 nhân 3 nhân 2     →  chở CẢ HAI bài cuối: trải phẳng ra sáu mặt tính
                               được 52, xếp lại thành khối đếm được 24 khối.
                               Một cái hộp, hai cách nhìn.

── BỐN KIỂU CẢNH MỚI ──
Kế hoạch ghi ba, nhưng làm mới lộ ra là bốn: `goc` · `tam_giac` · `hinh_tron` ·
`khoi`, cộng cờ `duongCheo` gắn vào `hinh_cn` đã có. Đường cao không mượn được
hình nào sẵn — nó cần một tam giác thật, kèm ca chân đường cao rơi ra ngoài đáy.

    python3 tools/hinh_khoi_lop4.py --xem
    python3 tools/hinh_khoi_lop4.py
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

TEN_CHUONG = 'HÌNH HỌC'
CHUONG = 10
CO_KHONG = ['có', 'không']

LUI_GOC = {'ve': ['DL:KSN3.B27'], 'ten': ['CHU VI CÓ CÔNG THỨC'],
           'canCu': 'chuDe', 'lopDuoi': 3}
LUI_DT = {'ve': ['DL:KSN3.B30'], 'ten': ['DIỆN TÍCH — TẤM THẢM Ô VUÔNG'],
          'canCu': 'chuDe', 'lopDuoi': 3}
LUI_CAT = {'ve': ['DL:KSN3.B30', 'DL:KSN3.B28'],
           'ten': ['DIỆN TÍCH — TẤM THẢM Ô VUÔNG', 'CHU VI BIẾN HÌNH'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_TRON = {'ve': ['DL:KSN3.B29'], 'ten': ['GIẢI PHẪU HÌNH TRÒN'],
            'canCu': 'sach', 'lopDuoi': 3}
LUI_KHOI = {'ve': ['DL:KSN3.B31'], 'ten': ['ĐẾM KHỐI THEO TẦNG'],
            'canCu': 'sach', 'lopDuoi': 3}
LUI_HOP = {'ve': ['DL:KSN3.B31'], 'ten': ['ĐẾM KHỐI THEO TẦNG'],
           'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng video: bốn mục giảng bằng chữ để RỖNG, video thay hẳn."""
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B45 · BỐN LOẠI GÓC — ÁP Ê KE VÀO, ĐỪNG ĐOÁN BẰNG MẮT
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ nhét bốn thứ vào một chỗ. Bài mới chỉ giữ lại phần góc, và dựng cả bài
# quanh MỘT dụng cụ: cái ê ke. Bốn loại góc không định nghĩa bằng số đo độ (lớp 4
# chưa học) mà định nghĩa bằng cái nhìn thấy được: cạnh góc chui gọn trong ê ke,
# trùng khít với ê ke, hay xoè rộng ra ngoài ê ke.
B45 = bai(
    45, 'BỐN LOẠI GÓC — ÁP Ê KE VÀO, ĐỪNG ĐOÁN BẰNG MẮT',
    'Dạng gốc: HH 2.1 mức Lớp 4 — Nhận biết góc nhọn, góc vuông, góc tù, góc bẹt '
    'bằng cách so với ê ke. Chưa dùng số đo độ.',
    'Con đã biết góc vuông từ lớp 3. Nhưng còn những góc không vuông thì gọi là gì? '
    'Hôm nay con có bốn cái tên, và một cách kiểm chắc chắn hơn mắt thường.',
    LUI_GOC,
    video(
        ['Gọi đúng tên bốn loại góc: nhọn, vuông, tù, bẹt.',
         'Dùng ê ke để kiểm một góc, thay vì đoán bằng mắt.',
         'Biết độ lớn của góc không phụ thuộc chiều dài hai cạnh.'],
        ['Đề bài: Áp ê ke vào một góc thì thấy cạnh góc xoè rộng ra ngoài ê ke. Hỏi đó '
         'là góc gì?',
         'Ê ke dùng để làm gì',
         'Ê ke có sẵn một góc vuông chuẩn. Nó là cái thước để đo góc, giống như thước '
         'kẻ là cái thước để đo độ dài.',
         'Cách áp ê ke',
         'Đặt góc vuông của ê ke trùng vào đỉnh góc, cho một cạnh của ê ke nằm khít '
         'lên một cạnh của góc. Rồi nhìn cạnh còn lại.',
         'Bốn cái nhìn, bốn cái tên',
         'Cạnh góc chui gọn bên trong ê ke thì đó là góc nhọn.',
         'Cạnh góc trùng khít với cạnh ê ke thì đó là góc vuông.',
         'Cạnh góc xoè rộng ra ngoài ê ke thì đó là góc tù.',
         'Hai cạnh duỗi thẳng thành một đường thẳng thì đó là góc bẹt, bằng đúng hai '
         'góc vuông.',
         'Bài này cạnh xoè rộng ra ngoài ê ke.',
         'Đáp số: góc tù.',
         'Thử lại: góc tù thì lớn hơn góc vuông mà chưa duỗi thẳng ra — đúng như hình.'],
        ['Có bạn nhìn hai góc mở bằng nhau: góc thứ nhất vẽ hai cạnh rất dài, góc thứ '
         'hai vẽ hai cạnh ngắn. Bạn ấy bảo góc thứ nhất lớn hơn.',
         'Gợi ý 1: Con lấy bút kéo dài hai cạnh của góc thứ hai ra thật dài xem. Hai '
         'cạnh có xoè ra thêm chút nào không?',
         'Gợi ý 2: Áp ê ke vào cả hai góc ấy rồi so hai lần áp với nhau.',
         'Chữa: độ lớn của góc là độ MỞ giữa hai cạnh, không phải chiều dài cạnh. Kéo '
         'dài cạnh bao nhiêu thì góc vẫn y như cũ.'],
        ['Cho con cầm ê ke đi một vòng quanh nhà: góc bàn, góc cửa đang mở, hai kim '
         'đồng hồ. Mỗi góc phải gọi tên kèm chứng cứ ê ke.',
         'Vẽ hai góc mở bằng nhau nhưng một góc cạnh dài, một góc cạnh ngắn, rồi hỏi '
         'con góc nào lớn hơn. Đây là chỗ nhầm phổ biến nhất của cả bài.'],
    ),
    [
        lt(1, 1, 'Góc nhọn so với góc vuông thì bé hơn hay lớn hơn?',
           'Góc nhọn bé hơn góc vuông — áp ê ke vào thì cạnh góc chui gọn bên trong.'),
        lt(2, 1, 'Góc tù so với góc vuông thì bé hơn hay lớn hơn?',
           'Góc tù lớn hơn góc vuông — áp ê ke vào thì cạnh góc xoè rộng ra ngoài.'),
        lt(3, 1, 'Góc bẹt bằng mấy góc vuông?',
           'Góc bẹt bằng 2 góc vuông. Hai cạnh của nó duỗi thẳng thành một đường thẳng.'),
        lt(4, 2, 'Áp ê ke vào một góc, thấy cạnh góc chui gọn bên trong ê ke. Góc ấy '
                 'tên là gì?',
           'Chui gọn bên trong ê ke nghĩa là bé hơn góc vuông, nên đó là góc nhọn.'),
        lt(5, 2, 'Áp ê ke vào một góc, thấy cạnh góc xoè rộng ra ngoài ê ke. Góc ấy '
                 'tên là gì?',
           'Xoè rộng ra ngoài ê ke nghĩa là lớn hơn góc vuông, nên đó là góc tù.'),
        lt(6, 2, 'Một góc có hai cạnh duỗi thẳng, nằm gọn trên một đường thẳng. Góc ấy '
                 'tên là gì?',
           'Hai cạnh duỗi thẳng thành một đường thì đó là góc bẹt.'),
        lt(7, 2, 'Hình chữ nhật có mấy góc vuông?',
           'Hình chữ nhật có 4 góc vuông — bốn góc của nó đều trùng khít với ê ke.'),
        lt(8, 3, 'Vẽ một góc, rồi lấy thước kéo dài cả hai cạnh của nó ra gấp đôi. Độ '
                 'lớn của góc có đổi không?',
           'Không đổi. Độ lớn của góc là độ mở giữa hai cạnh; kéo dài cạnh không làm '
           'hai cạnh xoè ra thêm.'),
        lt(9, 3, 'Lúc 3 giờ đúng, hai kim đồng hồ tạo thành góc gì? Còn lúc 6 giờ đúng '
                 'thì tạo thành góc gì?',
           'Lúc 3 giờ hai kim tạo góc vuông. Lúc 6 giờ hai kim duỗi thẳng ngược nhau '
           'nên tạo góc bẹt.'),
    ] + [
        q_tf(1, 'Góc tù lớn hơn góc vuông.', True,
             'Đúng. Áp ê ke vào thì cạnh góc tù xoè rộng ra ngoài ê ke.'),
        q_tf(2, 'Vẽ hai cạnh của một góc dài ra thì góc ấy lớn lên.', False,
             'Sai. Độ lớn của góc là độ mở giữa hai cạnh, không phải chiều dài cạnh.'),
        q_mcq(3, 'Góc bẹt bằng mấy góc vuông?', ['một', 'hai', 'ba', 'bốn'], 'hai',
              'Góc bẹt bằng hai góc vuông ghép lại, nên hai cạnh của nó duỗi thẳng.'),
        q_mcq(4, 'Áp ê ke vào một góc, cạnh góc chui gọn bên trong ê ke. Đó là góc gì?',
              ['góc nhọn', 'góc vuông', 'góc tù', 'góc bẹt'], 'góc nhọn',
              'Chui gọn bên trong ê ke nghĩa là bé hơn góc vuông — đó là góc nhọn.'),
        q_tf(5, 'Muốn biết một góc thuộc loại nào thì nhìn bằng mắt là chắc chắn đúng.',
             False, 'Sai. Mắt thường hay đoán lệch, nhất là với góc gần vuông. Phải áp '
                    'ê ke vào mới chắc.'),
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# ② B78 · ĐƯỜNG CAO — HẠ TỪ ĐỈNH XUỐNG ĐÁY, PHẢI VUÔNG GÓC
# ═══════════════════════════════════════════════════════════════════════════
# Bài này không tính gì cả, nó dạy MỘT ĐIỀU KIỆN. Và điều kiện ấy đúng là chỗ bé
# hay bỏ qua: kẻ một đoạn từ đỉnh xuống giữa đáy trông rất giống đường cao, mà
# không phải. Nên bài đi thẳng vào chỗ ấy, và có riêng một câu mức ba cho ca chân
# đường cao rơi ra ngoài đáy.
B78 = bai(
    78, 'ĐƯỜNG CAO — HẠ TỪ ĐỈNH XUỐNG ĐÁY, PHẢI VUÔNG GÓC',
    'Dạng gốc: HH 2.3 mức Lớp 4 — Vẽ đường cao của tam giác bằng ê ke, kể cả ca '
    'chân đường cao rơi ra ngoài đáy.',
    'Bài trước con đã dùng ê ke để gọi tên góc. Hôm nay vẫn cái ê ke ấy, nhưng dùng '
    'để VẼ: vẽ đường cao của một tam giác.',
    LUI_DT,
    video(
        ['Biết đường cao là đoạn từ một đỉnh hạ xuống đáy và vuông góc với đáy.',
         'Vẽ được đường cao bằng ê ke và đánh dấu góc vuông ở chân.',
         'Biết khi chân đường cao rơi ra ngoài đáy thì phải kéo dài đáy ra.'],
        ['Đề bài: Cho một tam giác có đáy nằm ngang. Hãy vẽ đường cao hạ từ đỉnh trên '
         'xuống đáy.',
         'Đường cao là gì',
         'Đường cao là đoạn thẳng đi từ một đỉnh xuống cạnh đối diện, và gặp cạnh ấy '
         'theo một góc vuông. Cạnh đối diện ấy gọi là đáy.',
         'Vẽ bằng ê ke',
         'Đặt một cạnh góc vuông của ê ke áp sát vào đáy. Trượt ê ke dọc theo đáy cho '
         'tới khi cạnh còn lại chạm đúng vào đỉnh. Kẻ theo cạnh ấy.',
         'Đánh dấu chân',
         'Chỗ đường cao gặp đáy gọi là chân đường cao. Ở đó phải đánh dấu góc vuông, '
         'để ai nhìn cũng biết mình đã kiểm.',
         'Đáp số: đoạn thẳng nối đỉnh với đáy và vuông góc với đáy.',
         'Thử lại: áp ê ke vào chân đường cao, thấy trùng khít góc vuông.'],
        ['Có bạn kẻ một đoạn từ đỉnh xuống đúng ĐIỂM GIỮA của đáy, rồi bảo đó là đường '
         'cao vì trông nó thẳng đứng.',
         'Gợi ý 1: Điều kiện của đường cao là phải đi tới điểm giữa đáy, hay là phải '
         'gặp đáy theo một góc nhất định?',
         'Gợi ý 2: Lấy ê ke áp vào đúng chỗ đoạn ấy gặp đáy xem hai bên có trùng khít '
         'nhau không.',
         'Chữa: đường cao đòi vuông góc với đáy, chứ không đòi đi qua điểm giữa. Đoạn '
         'nối đỉnh với điểm giữa đáy là một đoạn khác, có tên khác.'],
        ['Cho con vẽ đủ ba kiểu tam giác rồi hạ đường cao trên từng cái: tam giác có ba '
         'góc nhọn, tam giác có một góc vuông, tam giác có một góc tù.',
         'Cái tam giác tù mới là chỗ đáng luyện. Con gặp lần đầu thường hoảng vì đường '
         'cao rơi ra ngoài hình — bố mẹ chỉ cần bảo con kéo dài đáy ra mà đón.'],
    ),
    [
        lt(1, 1, 'Đường cao của tam giác đi từ đâu xuống đâu?',
           'Đường cao đi từ một đỉnh xuống đáy — tức là xuống cạnh đối diện với đỉnh ấy.'),
        lt(2, 1, 'Đường cao gặp đáy tạo thành góc gì?',
           'Tạo thành góc vuông. Đó chính là điều kiện làm nên đường cao.'),
        lt(3, 1, 'Muốn vẽ đường cao cho chuẩn thì dùng dụng cụ nào?',
           'Dùng ê ke, vì ê ke có sẵn góc vuông để áp vào đáy.'),
        lt(4, 2, 'Một tam giác có mấy đỉnh? Mỗi đỉnh hạ được một đường cao, vậy tam '
                 'giác có mấy đường cao?',
           'Tam giác có 3 đỉnh nên có 3 đường cao, mỗi đỉnh một đường.'),
        lt(5, 2, 'Chỗ đường cao gặp đáy được gọi là gì?',
           'Gọi là chân đường cao. Ở đó đánh dấu một ô vuông nhỏ để ghi rằng đã kiểm '
           'góc vuông.'),
        lt(6, 2, 'Tam giác có một góc tù. Hạ đường cao từ đỉnh của một góc nhọn thì '
                 'chân đường cao có thể rơi vào đâu?',
           'Có thể rơi ra ngoài đáy, chứ không nằm gọn trên đáy như tam giác thường.'),
        lt(7, 2, 'Khi chân đường cao rơi ra ngoài đáy thì phải làm gì với đáy để vẽ '
                 'cho được?',
           'Phải kéo dài đáy ra mà đón chân đường cao, thường vẽ phần kéo dài bằng nét '
           'đứt.'),
        lt(8, 3, 'Tam giác vuông có hai cạnh vuông góc với nhau. Nếu lấy một trong hai '
                 'cạnh ấy làm đáy thì cạnh kia có phải là đường cao không?',
           'Có. Cạnh kia đi từ một đỉnh xuống đáy và vuông góc với đáy — đúng đủ điều '
           'kiện của đường cao.'),
        lt(9, 3, 'Một tam giác có đáy dài 8 cm, đường cao hạ xuống đáy ấy dài 5 cm. Nay '
                 'kéo đáy dài thành 12 cm mà giữ nguyên chỗ đứng của đỉnh. Đường cao '
                 'lúc này dài bao nhiêu xăng-ti-mét?',
           'Vẫn 5 cm. Đường cao đo khoảng cách từ đỉnh xuống đường chứa đáy; kéo dài '
           'đáy ra không làm đỉnh cao lên hay thấp xuống.'),
    ] + [
        q_tf(1, 'Đường cao phải vuông góc với đáy.', True,
             'Đúng. Đó là điều kiện duy nhất làm nên đường cao.'),
        q_tf(2, 'Đoạn nối đỉnh với điểm giữa đáy luôn luôn là đường cao.', False,
             'Sai. Nó chỉ là đường cao khi tình cờ vuông góc với đáy; thường thì không.'),
        q_mcq(3, 'Một tam giác vẽ được mấy đường cao?',
              ['một', 'hai', 'ba', 'sáu'], 'ba',
              'Ba đỉnh, mỗi đỉnh hạ được một đường cao xuống cạnh đối diện.'),
        q_mcq(4, 'Chân đường cao có thể rơi ra ngoài đáy khi tam giác có',
              ['một góc tù', 'ba góc nhọn', 'một góc vuông'], 'một góc tù',
              'Góc tù đẩy đỉnh lệch hẳn sang một bên, nên chân đường cao rơi ra ngoài '
              'đáy và phải kéo dài đáy ra mà đón.'),
        q_tf(5, 'Vẽ đường cao xong thì đánh dấu góc vuông ở chân đường cao.', True,
             'Đúng. Dấu ấy cho biết mình đã kiểm bằng ê ke, không phải vẽ ước chừng.'),
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# ③ B79 · CẮT RỒI GHÉP — DIỆN TÍCH KHÔNG SINH KHÔNG MẤT
# ═══════════════════════════════════════════════════════════════════════════
# Bài này lấy lại ĐÚNG bộ số 6 nhân 4 của đợt một. Bé đã biết diện tích ấy là 24,
# nên khi cắt đôi ra 12 thì cả sức chú ý dồn vào Ý MỚI (cắt ghép không đổi diện
# tích) chứ không phải vào việc làm quen một hình lạ.
#
# Và bài kèm một vế NGƯỢC rất đáng nói: chu vi thì CÓ đổi. Đợt một dạy chu vi và
# diện tích là hai thứ khác nhau; đây là lần đầu bé thấy chúng cư xử khác nhau
# trên cùng một việc.
B79 = bai(
    79, 'CẮT RỒI GHÉP — DIỆN TÍCH KHÔNG SINH KHÔNG MẤT',
    'Dạng gốc: HH 4.1 mức Lớp 4 — Luật bảo toàn diện tích khi cắt ghép; dùng nó '
    'tính diện tích nửa hình chữ nhật khi chưa có công thức tam giác.',
    'Con vẫn nhớ mảnh vườn 6 nhân 4 chứ? Hôm nay mình lấy đúng bộ số ấy, nhưng là '
    'một tờ giấy — và mình cầm kéo cắt nó ra.',
    LUI_CAT,
    video(
        ['Biết cắt một hình ra rồi ghép lại thì diện tích không đổi.',
         'Dùng luật ấy tính được diện tích nửa hình chữ nhật, dù chưa học công thức.',
         'Biết chu vi thì ngược lại — cắt ghép xong chu vi có thể đổi.'],
        ['Đề bài: Một tờ giấy hình chữ nhật dài 6 cm, rộng 4 cm, được cắt theo đường '
         'chéo thành hai tam giác. Hỏi diện tích mỗi tam giác bằng bao nhiêu?',
         'Trước khi cắt',
         'Diện tích cả tờ giấy là: 6 × 4 = 24 (cm²)',
         'Đường chéo chia thế nào',
         'Đường chéo chia tờ giấy thành hai tam giác. Úp mảnh này lên mảnh kia thì '
         'chúng khít nhau, nên hai mảnh bằng nhau.',
         'Cắt không làm mất giấy',
         'Cắt ra thì giấy vẫn là ngần ấy giấy — không thêm mảnh nào, không mất mảnh '
         'nào. Hai mảnh cộng lại vẫn đúng 24.',
         'Hai mảnh bằng nhau, cộng lại 24, nên mỗi mảnh là:',
         '24 : 2 = 12 (cm²)',
         'Đáp số: mỗi tam giác 12 cm².',
         'Thử lại: ghép hai tam giác khít lại thành tờ giấy cũ: 12 + 12 = 24',
         'Còn chu vi thì sao',
         'Chu vi thì đổi. Mỗi mảnh nay có thêm một mép cắt mà lúc chưa cắt không có, '
         'nên đường bao quanh dài ra.'],
        ['Có bạn ghép hai tam giác ấy lại thành một hình khác — dài hơn và hẹp hơn — '
         'rồi bảo hình mới có diện tích lớn hơn vì trông nó dài hơn hẳn.',
         'Gợi ý 1: Ghép lại thì vẫn là đúng hai mảnh giấy ấy, không xin thêm mảnh nào. '
         'Số giấy trong tay có đổi không?',
         'Gợi ý 2: Con đếm số ô vuông trên hai mảnh trước khi ghép và sau khi ghép, '
         'rồi so hai lần đếm.',
         'Chữa: ghép kiểu nào thì phần mặt bị phủ vẫn đúng ngần ấy, vì không thêm không '
         'bớt mảnh giấy nào. Cái đổi khi ghép kiểu khác là đường bao quanh.'],
        ['Cắt ghép bằng giấy màu thật, đừng chỉ vẽ. Cho con cắt một tờ chữ nhật theo '
         'đường chéo rồi thử ghép hai mảnh thành những hình khác nhau.',
         'Mỗi lần ghép xong hỏi con hai câu tách bạch: phần mặt bị phủ có đổi không, và '
         'đường đi quanh mép có đổi không. Hai câu ấy là cả bài.'],
    ),
    [
        lt(1, 1, 'Tờ giấy hình chữ nhật dài 6 cm, rộng 4 cm. Diện tích tờ giấy bằng bao '
                 'nhiêu xăng-ti-mét vuông?',
           'Diện tích là 6 × 4 = 24 (cm²).'),
        lt(2, 1, 'Cắt tờ giấy ấy theo đường chéo thì được mấy mảnh, và hai mảnh có bằng '
                 'nhau không?',
           'Được 2 mảnh tam giác, và chúng bằng nhau — úp mảnh này lên mảnh kia thì khít.'),
        lt(3, 1, 'Vậy diện tích mỗi tam giác bằng bao nhiêu xăng-ti-mét vuông?',
           'Hai mảnh bằng nhau và cộng lại bằng 24, nên mỗi mảnh là 24 : 2 = 12 (cm²).'),
        lt(4, 2, 'Lấy hai tam giác vừa cắt ghép lại thành một hình khác. Diện tích hình '
                 'mới bằng bao nhiêu xăng-ti-mét vuông?',
           'Vẫn 24 cm². Ghép kiểu nào cũng đúng ngần ấy giấy, không thêm không bớt.'),
        lt(5, 2, 'Cắt một hình vuông cạnh 5 cm thành vài mảnh rồi ghép lại thành một '
                 'hình khác hẳn. Diện tích hình mới bằng bao nhiêu?',
           'Diện tích hình vuông là 5 × 5 = 25 (cm²), và ghép lại vẫn là 25 cm².'),
        lt(6, 2, 'Hình chữ nhật dài 8 cm rộng 3 cm, cắt theo đường chéo. Tính diện tích '
                 'cả hình rồi tính diện tích mỗi tam giác.',
           'Cả hình: 8 × 3 = 24 (cm²). Mỗi tam giác: 24 : 2 = 12 (cm²).'),
        lt(7, 2, 'Cắt một hình ra rồi ghép lại thành hình khác. Trong hai thứ diện tích '
                 'và chu vi, thứ nào chắc chắn không đổi, thứ nào có thể đổi?',
           'Diện tích chắc chắn không đổi. Chu vi thì có thể đổi, vì các mép cắt làm '
           'đường bao quanh dài ngắn khác đi.'),
        lt(8, 3, 'Hình chữ nhật dài 12 cm, rộng 5 cm, cắt theo đường chéo. Tính diện '
                 'tích cả hình và diện tích mỗi tam giác.',
           'Cả hình: 12 × 5 = 60 (cm²). Mỗi tam giác: 60 : 2 = 30 (cm²).'),
        lt(9, 3, 'Một tam giác là đúng một nửa của hình chữ nhật, và diện tích tam giác '
                 'ấy là 18 cm². Hỏi diện tích hình chữ nhật là bao nhiêu? Nếu hình chữ '
                 'nhật ấy dài 9 cm thì rộng bao nhiêu xăng-ti-mét?',
           'Hình chữ nhật gồm hai tam giác như thế: 18 × 2 = 36 (cm²). Biết diện tích '
           'tìm cạnh: 36 : 9 = 4 (cm).'),
    ] + [
        q_tf(1, 'Cắt một hình ra rồi ghép lại thì diện tích không đổi.', True,
             'Đúng. Không thêm mảnh nào, không mất mảnh nào, nên phần mặt bị phủ vẫn '
             'ngần ấy.'),
        q_tf(2, 'Đường chéo chia hình chữ nhật thành hai tam giác bằng nhau.', True,
             'Đúng. Úp mảnh này lên mảnh kia thì hai mảnh khít nhau.'),
        q_mcq(3, 'Hình chữ nhật 6 nhân 4 cắt theo đường chéo. Diện tích mỗi tam giác là',
              ['12 cm²', '24 cm²', '20 cm²', '10 cm²'], '12 cm²',
              'Cả hình 24 cm², cắt thành hai mảnh bằng nhau nên mỗi mảnh 12 cm².'),
        q_mcq(4, 'Cắt một hình rồi ghép lại thành hình khác thì thứ nào có thể đổi?',
              ['chu vi', 'diện tích', 'cả hai đều không bao giờ đổi'], 'chu vi',
              'Diện tích luôn giữ nguyên; còn chu vi đổi vì mép cắt làm đường bao quanh '
              'khác đi.'),
        q_tf(5, 'Ghép hai mảnh thành một hình trông dài hơn thì diện tích lớn lên.',
             False, 'Sai. Trông dài hơn nhưng vẫn đúng ngần ấy giấy — diện tích y '
                    'nguyên.'),
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# ④ B80 · HÌNH TRÒN — BÁN KÍNH VÀ ĐƯỜNG KÍNH
# ═══════════════════════════════════════════════════════════════════════════
# Cả bài đứng ở HAI CHỮ trong định nghĩa đường kính: "đi qua tâm". Bỏ hai chữ ấy
# thì đường kính thành một cái dây bất kỳ, và mọi số đo sau đó sai theo. Nên chỗ
# hay nhầm của bài chính là cái dây lệch tâm, và hình vẽ có riêng một nét cho nó.
B80 = bai(
    80, 'HÌNH TRÒN — BÁN KÍNH VÀ ĐƯỜNG KÍNH',
    'Dạng gốc: HH 3.1 mức Lớp 4 — Tâm, bán kính, đường kính; quan hệ đường kính '
    'gấp đôi bán kính. Chưa tính chu vi hay diện tích hình tròn.',
    'Hôm nay đổi dụng cụ: cất ê ke đi, lấy com pa ra. Com pa vẽ được hình tròn, và '
    'cách nó vẽ sẽ nói cho con biết hình tròn là gì.',
    LUI_TRON,
    video(
        ['Chỉ ra được tâm, bán kính và đường kính của một hình tròn.',
         'Biết mọi bán kính của cùng một hình tròn đều bằng nhau.',
         'Biết đường kính đi qua tâm và dài gấp đôi bán kính.'],
        ['Đề bài: Một hình tròn có bán kính 3 cm. Tính đường kính của hình tròn ấy.',
         'Com pa vẽ hình tròn thế nào',
         'Cắm mũi nhọn của com pa xuống một điểm, mở com pa ra 3 cm rồi xoay một vòng. '
         'Điểm cắm ấy gọi là tâm.',
         'Vì sao mọi bán kính bằng nhau',
         'Suốt vòng xoay, độ mở của com pa không đổi. Nên mọi điểm trên nét vẽ đều cách '
         'tâm đúng 3 cm. Đoạn nối tâm với một điểm trên nét vẽ gọi là bán kính.',
         'Đường kính là gì',
         'Đường kính là đoạn nối hai điểm trên nét vẽ và đi qua tâm. Bốn chữ đi qua tâm '
         'ấy là chỗ quan trọng nhất.',
         'Đường kính đi từ mép này, qua tâm, sang mép kia — tức là gồm hai bán kính nối '
         'tiếp nhau:',
         '3 × 2 = 6 (cm)',
         'Đáp số: đường kính 6 cm.',
         'Thử lại: đi ngược lại, lấy đường kính chia đôi: 6 : 2 = 3'],
        ['Có bạn căng dây từ mép này sang mép kia nhưng dây đi lệch, không qua tâm. Đo '
         'được 5 cm, bạn ấy liền bảo đường kính hình tròn là 5 cm.',
         'Gợi ý 1: Trong định nghĩa đường kính có bốn chữ nói về chỗ nó bắt buộc phải '
         'đi qua. Dây của bạn ấy có đi qua đó không?',
         'Gợi ý 2: Vẽ thử vài cái dây nối hai mép, cái qua giữa và cái lệch hẳn sang '
         'bên. Đo cả mấy cái rồi so xem cái nào dài nhất.',
         'Chữa: dây không qua tâm bao giờ cũng ngắn hơn. Bán kính 3 cm nên đường kính '
         'đúng 6 cm, không phải 5 cm.'],
        ['Đưa con cái com pa thật, cho vẽ mấy hình tròn to nhỏ khác nhau. Vẽ xong bảo '
         'con đo lại vài bán kính của cùng một hình xem có bằng nhau không.',
         'Trò dễ chơi: cho con tìm hình tròn quanh nhà — nắp nồi, đĩa, đồng hồ — rồi đo '
         'chỗ rộng nhất của nó. Chỗ rộng nhất ấy chính là đường kính.'],
    ),
    [
        lt(1, 1, 'Một hình tròn có bán kính 3 cm. Đường kính dài bao nhiêu xăng-ti-mét?',
           'Đường kính gồm hai bán kính nối tiếp: 3 × 2 = 6 (cm).'),
        lt(2, 1, 'Một hình tròn có đường kính 10 cm. Bán kính dài bao nhiêu xăng-ti-mét?',
           'Bán kính là nửa đường kính: 10 : 2 = 5 (cm).'),
        lt(3, 1, 'Một đoạn nối hai điểm trên nét tròn có bắt buộc đi qua tâm mới được '
                 'gọi là đường kính không?',
           'Có. Không đi qua tâm thì chỉ là một cái dây thường, không phải đường kính.'),
        lt(4, 2, 'Hình tròn có bán kính 7 cm. Tính đường kính.',
           'Đường kính là 7 × 2 = 14 (cm).'),
        lt(5, 2, 'Hình tròn có đường kính 18 cm. Tính bán kính.',
           'Bán kính là 18 : 2 = 9 (cm).'),
        lt(6, 2, 'Vẽ hai bán kính khác nhau của cùng một hình tròn. Hai bán kính ấy có '
                 'bằng nhau không?',
           'Có. Com pa giữ nguyên độ mở suốt vòng xoay nên mọi bán kính đều bằng nhau.'),
        lt(7, 2, 'Một đường kính gồm mấy bán kính nối tiếp nhau?',
           'Gồm 2 bán kính: từ mép tới tâm là một, từ tâm sang mép kia là một nữa.'),
        lt(8, 3, 'Một bồn hoa hình tròn có bán kính 2 m. Muốn đóng một khung gỗ hình '
                 'vuông ôm vừa khít bồn thì mỗi cạnh khung dài bao nhiêu mét?',
           'Khung phải ôm được chỗ rộng nhất của bồn, tức đường kính: 2 × 2 = 4 (m). Vậy '
           'mỗi cạnh khung dài 4 m.'),
        lt(9, 3, 'Một hình tròn có đường kính 12 cm. Vẽ một cái dây nối hai mép nhưng '
                 'không đi qua tâm. Dây ấy dài hơn hay ngắn hơn 12 cm? Và bán kính hình '
                 'tròn bằng bao nhiêu xăng-ti-mét?',
           'Dây không qua tâm thì ngắn hơn — đường kính là cái dây dài nhất. Bán kính '
           'là 12 : 2 = 6 (cm).'),
    ] + [
        q_tf(1, 'Đường kính dài gấp đôi bán kính.', True,
             'Đúng. Đường kính gồm hai bán kính nối tiếp nhau qua tâm.'),
        q_tf(2, 'Mọi đoạn nối hai điểm trên nét tròn đều là đường kính.', False,
             'Sai. Phải đi qua tâm mới là đường kính; đoạn đi lệch chỉ là một cái dây '
             'thường và ngắn hơn.'),
        q_mcq(3, 'Hình tròn bán kính 5 cm có đường kính bằng',
              ['10 cm', '5 cm', '15 cm', '20 cm'], '10 cm',
              'Đường kính gấp đôi bán kính nên bằng 10 cm.'),
        q_mcq(4, 'Trong cùng một hình tròn, các bán kính',
              ['đều bằng nhau', 'dài ngắn khác nhau', 'có cái dài bằng đường kính'],
              'đều bằng nhau',
              'Com pa giữ nguyên độ mở suốt vòng xoay, nên mọi bán kính bằng nhau.'),
        q_tf(5, 'Một cái dây nối hai mép mà không đi qua tâm thì ngắn hơn đường kính.',
             True, 'Đúng. Đường kính là cái dây dài nhất của hình tròn.'),
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B46 · TRẢI PHẲNG HỘP RA — SÁU MẶT, BA CẶP
# ═══════════════════════════════════════════════════════════════════════════
# Chỗ đáng dạy không phải "hộp có sáu mặt" — bé đếm được. Chỗ đáng dạy là sáu mặt
# ấy hợp thành BA CẶP, mỗi cặp hai mặt bằng nhau, nên chỉ phải tính ba lần rồi
# nhân đôi một lần ở cuối. Hình trải phẳng tô màu theo cặp để chuyện ấy nhìn thấy
# được, không phải nghe kể.
B46 = bai(
    46, 'TRẢI PHẲNG HỘP RA — SÁU MẶT, BA CẶP',
    'Dạng gốc: HH 5.1 mức Lớp 4 — Hình khai triển của hình hộp chữ nhật; ba cặp '
    'mặt đối diện bằng nhau; tính tổng diện tích sáu mặt.',
    'Con lấy một cái hộp giấy, rọc theo mép rồi trải phẳng nó ra bàn. Cái hình vừa '
    'hiện ra sẽ nói cho con biết vì sao tính bìa của hộp lại dễ hơn con tưởng.',
    LUI_HOP,
    video(
        ['Biết hình hộp chữ nhật có sáu mặt, hợp thành ba cặp đối diện bằng nhau.',
         'Đọc được hình trải phẳng và chỉ ra mặt nào đối diện với mặt nào.',
         'Tính được tổng diện tích sáu mặt bằng cách nhân đôi tổng ba mặt khác nhau.'],
        ['Đề bài: Một hình hộp chữ nhật dài 4 cm, rộng 3 cm, cao 2 cm. Tính tổng diện '
         'tích sáu mặt của hộp.',
         'Trải phẳng ra thì thấy gì',
         'Sáu mặt hiện ra, và chúng không phải sáu mặt khác nhau: chúng hợp thành ba '
         'cặp, hai mặt trong một cặp bằng hệt nhau.',
         'Ba cặp ấy dựng từ ba cặp số',
         'Cặp đáy và nắp dựng từ dài và rộng: 4 × 3 = 12 (cm²)',
         'Cặp trước và sau dựng từ dài và cao: 4 × 2 = 8 (cm²)',
         'Cặp hai bên hông dựng từ rộng và cao: 3 × 2 = 6 (cm²)',
         'Cộng ba mặt khác nhau rồi nhân đôi',
         'Tổng ba mặt khác nhau là: 12 + 8 + 6 = 26 (cm²)',
         'Mỗi mặt có một mặt đối diện bằng nó, nên nhân đôi một lần ở cuối:',
         '26 × 2 = 52 (cm²)',
         'Đáp số: 52 cm².',
         'Thử lại bằng cách cộng đủ sáu mặt: 12 + 12 + 8 + 8 + 6 + 6 = 52'],
        ['Có bạn tính một mặt là 4 nhân 3 bằng 12, rồi bảo hộp có sáu mặt nên nhân với '
         'sáu: 12 nhân 6 bằng 72 cm².',
         'Gợi ý 1: Sáu mặt của hộp có phải mặt nào cũng giống mặt nào không? Con nhìn '
         'mặt bên hông rồi nhìn mặt nắp mà so.',
         'Gợi ý 2: Mặt bên hông của hộp này dựng từ hai số nào trong ba số đã cho?',
         'Chữa: chỉ hình lập phương mới có sáu mặt bằng nhau. Hộp chữ nhật có ba cặp '
         'khác nhau, phải tính từng cặp rồi mới cộng.'],
        ['Bóc một hộp bánh hay hộp sữa dọc theo mép dán rồi trải phẳng ra. Hình trải '
         'phẳng thật nằm sẵn trong thùng rác tái chế, sinh động hơn mọi hình vẽ.',
         'Cho con tô màu hai mặt đối diện cùng một màu trên tờ trải ấy. Tô xong là con '
         'tự thấy ba cặp, và tự hiểu vì sao chỉ phải tính ba lần.'],
    ),
    [
        lt(1, 1, 'Hình hộp chữ nhật có mấy mặt, và sáu mặt ấy hợp thành mấy cặp đối diện?',
           'Có 6 mặt, hợp thành 3 cặp đối diện; hai mặt trong một cặp bằng nhau.'),
        lt(2, 1, 'Hộp dài 4 cm, rộng 3 cm, cao 2 cm. Tính diện tích mặt đáy.',
           'Mặt đáy dựng từ dài và rộng: 4 × 3 = 12 (cm²).'),
        lt(3, 1, 'Vẫn hộp ấy. Tính diện tích mặt trước, biết mặt trước dựng từ chiều '
                 'dài 4 cm và chiều cao 2 cm.',
           'Mặt trước là 4 × 2 = 8 (cm²).'),
        lt(4, 2, 'Vẫn hộp ấy. Tính diện tích một mặt bên hông, biết mặt hông dựng từ '
                 'chiều rộng 3 cm và chiều cao 2 cm.',
           'Mặt hông là 3 × 2 = 6 (cm²).'),
        lt(5, 2, 'Cộng ba mặt khác nhau của hộp 4 nhân 3 nhân 2 lại với nhau.',
           'Ba mặt khác nhau là 12, 8 và 6, cộng lại: 12 + 8 + 6 = 26 (cm²).'),
        lt(6, 2, 'Từ tổng ba mặt vừa tìm được, tính tổng diện tích cả sáu mặt của hộp.',
           'Mỗi mặt có một mặt đối diện bằng nó nên nhân đôi: 26 × 2 = 52 (cm²).'),
        lt(7, 2, 'Trên hình trải phẳng của một cái hộp, hai mặt đối diện nhau có nằm '
                 'cạnh nhau không?',
           'Không. Hai mặt đối diện luôn bị tách ra bởi một mặt khác — đó là cách kiểm '
           'nhanh xem tờ trải có gấp lại thành hộp được hay không.'),
        lt(8, 3, 'Hộp dài 5 cm, rộng 4 cm, cao 3 cm. Tính tổng ba mặt khác nhau, rồi '
                 'tính tổng diện tích sáu mặt.',
           'Ba mặt: 5 × 4 = 20, rồi 5 × 3 = 15, rồi 4 × 3 = 12. Tổng ba mặt: '
           '20 + 15 + 12 = 47 (cm²). Sáu mặt: 47 × 2 = 94 (cm²).'),
        lt(9, 3, 'Một hình lập phương có cạnh 3 cm. Tính diện tích một mặt, rồi tính '
                 'tổng diện tích sáu mặt.',
           'Một mặt: 3 × 3 = 9 (cm²). Hình lập phương có sáu mặt bằng nhau nên tổng là '
           '9 × 6 = 54 (cm²).'),
    ] + [
        q_tf(1, 'Hình hộp chữ nhật có sáu mặt.', True,
             'Đúng, và sáu mặt ấy hợp thành ba cặp đối diện bằng nhau.'),
        q_tf(2, 'Sáu mặt của một hình hộp chữ nhật luôn bằng nhau.', False,
             'Sai. Chỉ hình lập phương mới thế; hộp chữ nhật có ba cặp khác nhau.'),
        q_mcq(3, 'Hộp 4 nhân 3 nhân 2 có tổng diện tích sáu mặt bằng',
              ['52 cm²', '26 cm²', '72 cm²', '24 cm²'], '52 cm²',
              'Ba mặt khác nhau là 12, 8, 6; cộng được 26 rồi nhân đôi thành 52.'),
        q_mcq(4, 'Ba cặp mặt của một hình hộp chữ nhật dựng từ',
              ['ba cặp số khác nhau', 'cùng một cặp số', 'sáu số khác nhau'],
              'ba cặp số khác nhau',
              'Dài với rộng, dài với cao, rộng với cao — ba cặp số lấy từ ba số đã cho.'),
        q_tf(5, 'Trên hình trải phẳng, hai mặt đối diện nhau nằm sát cạnh nhau.', False,
             'Sai. Chúng luôn bị một mặt khác tách ra; đó là cách kiểm nhanh tờ trải.'),
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B81 · ĐẾM KHỐI — LÁT TỪNG TẦNG MÀ ĐẾM
# ═══════════════════════════════════════════════════════════════════════════
# Cùng cái hộp 4 nhân 3 nhân 2 của bài trước, nhưng nay xếp đặc ruột. Ý của bài
# gọn trong một câu: HÌNH KHỐI LÀ MẤY TẦNG PHẲNG XẾP CHỒNG. Nắm được câu ấy thì
# đếm khối bị khoét cũng chẳng khó hơn — cứ lát từng tầng ra mà đếm.
B81 = bai(
    81, 'ĐẾM KHỐI — LÁT TỪNG TẦNG MÀ ĐẾM',
    'Dạng gốc: HH 5.2 mức Lớp 4 — Đếm số khối lập phương nhỏ trong một khối hộp '
    'bằng cách đếm theo tầng, kể cả khối bị khoét. Chưa gọi tên thể tích.',
    'Vẫn cái hộp 4 nhân 3 nhân 2 của bài trước, nhưng lần này nó không rỗng: bên '
    'trong xếp đầy những khối lập phương nhỏ. Đếm bao nhiêu khối đây?',
    LUI_KHOI,
    video(
        ['Đếm được số khối lập phương nhỏ trong một khối hộp bằng cách đếm theo tầng.',
         'Biết mỗi tầng có số khối bằng dài nhân rộng, và tổng bằng một tầng nhân số '
         'tầng.',
         'Đếm được cả khối bị khoét, bằng cách đếm riêng từng tầng rồi cộng lại.'],
        ['Đề bài: Một khối hộp xếp từ các khối lập phương nhỏ, dài 4 khối, rộng 3 khối, '
         'cao 2 khối. Hỏi khối hộp gồm bao nhiêu khối lập phương nhỏ?',
         'Đọc chiều cao thành số tầng',
         'Cao 2 khối nghĩa là khối hộp gồm 2 tầng chồng lên nhau. Đây là bước biến hình '
         'khối thành mấy hình phẳng.',
         'Đếm một tầng',
         'Mỗi tầng là một sàn chữ nhật dài 4 khối, rộng 3 khối:',
         '4 × 3 = 12 (khối)',
         'Nhân với số tầng',
         'Hai tầng giống hệt nhau nên:',
         '12 × 2 = 24 (khối)',
         'Đáp số: 24 khối lập phương nhỏ.',
         'Thử lại bằng cách đếm khác: đếm theo cột đứng. Có 4 × 3 = 12 cột, mỗi cột '
         'cao 2 khối, vậy 12 × 2 = 24',
         'Hai cách cắt khác nhau mà ra cùng một đáp số.'],
        ['Nhìn khối lập phương 3 nhân 3 nhân 3, có bạn đếm theo ảnh chụp: mặt trước 9 '
         'khối, mặt bên phải 9 khối, mặt trên 9 khối, ba mặt là 27; hộp có sáu mặt nên '
         'bạn ấy nhân đôi thành 54 khối.',
         'Gợi ý 1: Cái khối nằm ở chính giữa ruột hộp thì nó thuộc mặt nào? Còn cái '
         'khối ở góc thì bị đếm mấy lần khi cộng theo mặt?',
         'Gợi ý 2: Bỏ hẳn lối nhìn theo mặt đi. Cắt hộp thành từng tầng nằm ngang rồi '
         'đếm từng tầng một.',
         'Chữa: đếm theo mặt là đếm vỏ, mà khối thì đặc ruột — có khối chẳng nằm trên '
         'mặt nào, lại có khối bị đếm mấy lần. Đếm theo tầng thì mỗi tầng 9 khối, ba '
         'tầng là 27 khối.'],
        ['Xếp bằng đồ thật: rubik nhỏ, xúc xắc, khối gỗ. Bố mẹ ra đề một cỡ hộp, con '
         'tính trước rồi mới xếp ra đếm kiểm chứng.',
         'Trò hay nhất là nhấc bớt vài khối ở tầng trên rồi hỏi lại. Con nào còn đếm '
         'theo mặt sẽ tắc ngay, còn con đếm theo tầng thì vẫn làm được.'],
    ),
    [
        lt(1, 1, 'Một khối hộp cao 2 khối thì gồm mấy tầng chồng lên nhau?',
           'Cao 2 khối nghĩa là 2 tầng.'),
        lt(2, 1, 'Khối hộp dài 4 khối, rộng 3 khối. Mỗi tầng của nó có bao nhiêu khối nhỏ?',
           'Mỗi tầng là một sàn 4 × 3 = 12 (khối).'),
        lt(3, 1, 'Khối hộp dài 4 khối, rộng 3 khối, cao 2 khối gồm tất cả bao nhiêu '
                 'khối nhỏ?',
           'Mỗi tầng 12 khối, có 2 tầng: 12 × 2 = 24 (khối).'),
        lt(4, 2, 'Khối lập phương xếp từ khối nhỏ, mỗi chiều 3 khối. Mỗi tầng mấy khối, '
                 'có mấy tầng, và tất cả bao nhiêu khối?',
           'Mỗi tầng 3 × 3 = 9 (khối), có 3 tầng, tất cả 9 × 3 = 27 (khối).'),
        lt(5, 2, 'Một khối lập phương mỗi chiều 2 khối gồm bao nhiêu khối nhỏ?',
           'Mỗi tầng 2 × 2 = 4 (khối), có 2 tầng: 4 × 2 = 8 (khối).'),
        lt(6, 2, 'Khối hộp dài 5 khối, rộng 4 khối, cao 3 khối. Tính số khối mỗi tầng '
                 'rồi tính tổng số khối.',
           'Mỗi tầng 5 × 4 = 20 (khối). Ba tầng: 20 × 3 = 60 (khối).'),
        lt(7, 2, 'Khối lập phương mỗi chiều 3 khối bị nhấc đi 1 khối ở tầng trên cùng. '
                 'Còn lại bao nhiêu khối?',
           'Tầng dưới 9, tầng giữa 9, tầng trên còn 8. Cộng lại: 9 + 9 + 8 = 26 (khối).'),
        lt(8, 3, 'Một khối hộp có mỗi tầng 15 khối và tất cả 45 khối. Hỏi khối hộp có '
                 'mấy tầng?',
           'Đọc ngược phép nhân: 45 : 15 = 3 (tầng).'),
        lt(9, 3, 'Khối hộp dài 4 khối, rộng 3 khối, cao 3 khối, nhưng tầng trên cùng bị '
                 'nhấc đi 2 khối. Tính số khối của một tầng đầy, rồi tính tổng số khối '
                 'còn lại.',
           'Một tầng đầy: 4 × 3 = 12 (khối). Hai tầng dưới đầy, tầng trên còn 10, nên '
           'tổng là 12 + 12 + 10 = 34 (khối).'),
    ] + [
        q_tf(1, 'Số khối của mỗi tầng bằng chiều dài nhân chiều rộng.', True,
             'Đúng. Mỗi tầng là một sàn chữ nhật, đếm ô như đếm diện tích.'),
        q_tf(2, 'Muốn biết khối hộp có bao nhiêu khối thì cộng số khối nhìn thấy trên '
                'các mặt.', False,
             'Sai. Đếm theo mặt là đếm vỏ: khối ở giữa ruột không nằm trên mặt nào, còn '
             'khối ở góc lại bị đếm mấy lần.'),
        q_mcq(3, 'Khối hộp 4 nhân 3 nhân 2 gồm',
              ['24 khối', '12 khối', '9 khối', '48 khối'], '24 khối',
              'Mỗi tầng 12 khối, hai tầng nên 24 khối.'),
        q_mcq(4, 'Khối lập phương mỗi chiều 3 khối gồm',
              ['27 khối', '9 khối', '54 khối', '18 khối'], '27 khối',
              'Mỗi tầng 9 khối, ba tầng nên 27 khối.'),
        q_tf(5, 'Khối bị nhấc mất vài chỗ thì vẫn đếm được, bằng cách đếm riêng từng '
                'tầng rồi cộng lại.', True,
             'Đúng. Tầng nào thiếu thì đếm đúng tầng ấy, các tầng khác vẫn đầy.'),
    ],
)

MOI = [B45, B78, B79, B80, B46, B81]

# Bài mới chèn vào đâu — khai theo BÀI ĐỨNG TRƯỚC, không khai theo số thứ tự.
# Khai theo số là tự đặt bẫy: chỉ cần một đợt sau chèn thêm bài là mọi con số ở
# đây lệch hết mà không ai báo. Xem lối C ở `docs/ke_hoach_video_lop4.md` §10.
SAU = {
    'DL:KSN4.B78': 'DL:KSN4.B45',
    'DL:KSN4.B79': 'DL:KSN4.B78',
    'DL:KSN4.B80': 'DL:KSN4.B79',
    'DL:KSN4.B81': 'DL:KSN4.B46',
}

BON_GOC = ['góc nhọn', 'góc vuông', 'góc tù', 'góc bẹt']

O_NHAP_MOI = {
    'DL:KSN4.B45#C1': {'parts': [{'label': 'so với góc vuông',
                                  'options': ['bé hơn', 'lớn hơn'], 'value': 'bé hơn'}]},
    'DL:KSN4.B45#C2': {'parts': [{'label': 'so với góc vuông',
                                  'options': ['bé hơn', 'lớn hơn'], 'value': 'lớn hơn'}]},
    'DL:KSN4.B45#C3': {'value': 2},
    'DL:KSN4.B45#C4': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                                  'value': 'góc nhọn'}]},
    'DL:KSN4.B45#C5': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                                  'value': 'góc tù'}]},
    'DL:KSN4.B45#C6': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                                  'value': 'góc bẹt'}]},
    'DL:KSN4.B45#C7': {'value': 4},
    'DL:KSN4.B45#C8': {'parts': [{'label': 'góc có đổi không', 'options': CO_KHONG,
                                  'value': 'không'}]},
    'DL:KSN4.B45#C9': {'parts': [{'label': 'lúc 3 giờ', 'options': BON_GOC,
                                  'value': 'góc vuông'},
                                 {'label': 'lúc 6 giờ', 'options': BON_GOC,
                                  'value': 'góc bẹt'}]},

    'DL:KSN4.B78#C1': {'parts': [{'label': 'đi từ', 'options': ['đỉnh', 'điểm giữa đáy'],
                                  'value': 'đỉnh'},
                                 {'label': 'xuống', 'options': ['đáy', 'cạnh bên'],
                                  'value': 'đáy'}]},
    'DL:KSN4.B78#C2': {'parts': [{'label': 'tên góc', 'options': BON_GOC,
                                  'value': 'góc vuông'}]},
    'DL:KSN4.B78#C3': {'parts': [{'label': 'dụng cụ', 'options': ['ê ke', 'com pa'],
                                  'value': 'ê ke'}]},
    'DL:KSN4.B78#C4': {'parts': [{'label': 'số đỉnh', 'value': 3},
                                 {'label': 'số đường cao', 'value': 3}]},
    'DL:KSN4.B78#C5': {'parts': [{'label': 'tên gọi',
                                  'options': ['chân đường cao', 'đỉnh tam giác'],
                                  'value': 'chân đường cao'}]},
    'DL:KSN4.B78#C6': {'parts': [{'label': 'chân rơi vào đâu',
                                  'options': ['ra ngoài đáy', 'đúng giữa đáy'],
                                  'value': 'ra ngoài đáy'}]},
    'DL:KSN4.B78#C7': {'parts': [{'label': 'phải làm gì với đáy',
                                  'options': ['kéo dài đáy ra', 'vẽ đáy ngắn lại'],
                                  'value': 'kéo dài đáy ra'}]},
    'DL:KSN4.B78#C8': {'parts': [{'label': 'có phải đường cao không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B78#C9': {'value': 5},

    'DL:KSN4.B79#C1': {'value': 24},
    'DL:KSN4.B79#C2': {'parts': [{'label': 'số mảnh', 'value': 2},
                                 {'label': 'hai mảnh bằng nhau không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B79#C3': {'value': 12},
    'DL:KSN4.B79#C4': {'value': 24},
    'DL:KSN4.B79#C5': {'value': 25},
    'DL:KSN4.B79#C6': {'parts': [{'label': 'cả hình', 'value': 24},
                                 {'label': 'mỗi tam giác', 'value': 12}]},
    'DL:KSN4.B79#C7': {'parts': [{'label': 'diện tích',
                                  'options': ['không đổi', 'có thể đổi'],
                                  'value': 'không đổi'},
                                 {'label': 'chu vi',
                                  'options': ['không đổi', 'có thể đổi'],
                                  'value': 'có thể đổi'}]},
    'DL:KSN4.B79#C8': {'parts': [{'label': 'cả hình', 'value': 60},
                                 {'label': 'mỗi tam giác', 'value': 30}]},
    'DL:KSN4.B79#C9': {'parts': [{'label': 'hình chữ nhật', 'value': 36},
                                 {'label': 'chiều rộng', 'value': 4}]},

    'DL:KSN4.B80#C1': {'value': 6},
    'DL:KSN4.B80#C2': {'value': 5},
    'DL:KSN4.B80#C3': {'parts': [{'label': 'bắt buộc không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B80#C4': {'value': 14},
    'DL:KSN4.B80#C5': {'value': 9},
    'DL:KSN4.B80#C6': {'parts': [{'label': 'bằng nhau không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B80#C7': {'value': 2},
    'DL:KSN4.B80#C8': {'value': 4},
    'DL:KSN4.B80#C9': {'parts': [{'label': 'cái dây ấy',
                                  'options': ['ngắn hơn', 'dài hơn'],
                                  'value': 'ngắn hơn'},
                                 {'label': 'bán kính', 'value': 6}]},

    'DL:KSN4.B46#C1': {'parts': [{'label': 'số mặt', 'value': 6},
                                 {'label': 'số cặp đối diện', 'value': 3}]},
    'DL:KSN4.B46#C2': {'value': 12},
    'DL:KSN4.B46#C3': {'value': 8},
    'DL:KSN4.B46#C4': {'value': 6},
    'DL:KSN4.B46#C5': {'value': 26},
    'DL:KSN4.B46#C6': {'value': 52},
    'DL:KSN4.B46#C7': {'parts': [{'label': 'nằm cạnh nhau không', 'options': CO_KHONG,
                                  'value': 'không'}]},
    'DL:KSN4.B46#C8': {'parts': [{'label': 'tổng ba mặt', 'value': 47},
                                 {'label': 'tổng sáu mặt', 'value': 94}]},
    'DL:KSN4.B46#C9': {'parts': [{'label': 'một mặt', 'value': 9},
                                 {'label': 'sáu mặt', 'value': 54}]},

    'DL:KSN4.B81#C1': {'value': 2},
    'DL:KSN4.B81#C2': {'value': 12},
    'DL:KSN4.B81#C3': {'value': 24},
    'DL:KSN4.B81#C4': {'parts': [{'label': 'mỗi tầng', 'value': 9},
                                 {'label': 'số tầng', 'value': 3},
                                 {'label': 'tất cả', 'value': 27}]},
    'DL:KSN4.B81#C5': {'value': 8},
    'DL:KSN4.B81#C6': {'parts': [{'label': 'mỗi tầng', 'value': 20},
                                 {'label': 'tất cả', 'value': 60}]},
    'DL:KSN4.B81#C7': {'value': 26},
    'DL:KSN4.B81#C8': {'value': 3},
    'DL:KSN4.B81#C9': {'parts': [{'label': 'một tầng đầy', 'value': 12},
                                 {'label': 'tổng còn lại', 'value': 34}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {'DL:KSN4.B45', 'DL:KSN4.B46'}
    moi_ = {f'DL:KSN4.B{n}' for n in (78, 79, 80, 81)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    # Hai bài cũ PHẢI mất hết chữ giảng — chúng đang giữ bài chữ dài của bản cũ, và
    # ghi đè nửa vời thì bé xem video xong lại gặp nguyên bài giảng cũ ở dưới.
    for b in MOI:
        for m in ('chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
    # Số neo của đợt — nhưng CHỈ soi bốn bài có tính toán.
    #
    # ⚠ MIỄN CÓ LÝ DO, khai thẳng ra đây chứ không lặng lẽ bỏ qua: bài góc và bài
    # đường cao KHÔNG tính con số nào cả. Chúng dạy cách gọi tên và cách vẽ, đo
    # bằng ê ke chứ không đo bằng số. Ép hai bài ấy nhét bộ số neo vào là bịa việc
    # cho có, đúng cái kiểu sửa nội dung đúng cho vừa lòng cổng.
    NEO = {'DL:KSN4.B79': '6 × 4', 'DL:KSN4.B80': 'bán kính 3',
           'DL:KSN4.B46': '4 × 3', 'DL:KSN4.B81': '4 × 3'}
    for b in MOI:
        mong = NEO.get(b['id'])
        if mong and mong not in json.dumps(b, ensure_ascii=False):
            loi.append(f'{b["id"]}: không bám số neo "{mong}" của đợt')
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
        # Giữ lại hình đã gắn — `gan_hinh_lop4.py` chạy SAU bộ dựng, nên ghi đè
        # trắng chỗ này là mất sạch hình mà không có gì báo. Đã sập một lần.
        #
        # ⚠ NHƯNG CHỈ GIỮ CHO MỤC CÒN CHỮ. Bản đầu của vỏ này chép hình cũ vào cả
        # mục nay đã rỗng, tức là LÀM SỐNG DẬY đúng những hình mồ côi vừa xoá đi:
        # bài chuyển sang video thì mục ② và ④ rỗng, mà hình vẫn được chép về neo
        # vào đó. Hai bài B45 B46 dính đủ tám hình. Cái vỏ dựng ra để khỏi mất hình
        # hoá ra lại giữ hộ mấy cái hình lẽ ra phải chết.
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
