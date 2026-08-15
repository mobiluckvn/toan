# -*- coding: utf-8 -*-
"""CHƯƠNG 10 · HÌNH HỌC — ĐỢT MỘT: sáu bài về chu vi và diện tích.

Chương gói nặng nhất cả quyển:
  · B43 gộp chu vi, diện tích, đơn vị đo, bài ngược và cả kết hợp tổng - hiệu;
  · B44 gộp tăng một chiều, tăng chiều này giảm chiều kia, và chu vi;
  · B45 gộp **bốn thứ chẳng liên quan gì nhau**: góc, đường cao, cắt ghép, hình tròn;
  · B46 gộp hình khai triển, đếm khối, khối lập phương.

── SỐ NEO: HÌNH CHỮ NHẬT 6 MÉT NHÂN 4 MÉT ──
Chu vi 20, diện tích 24. Chọn bộ này vì **hai con số khác hẳn nhau** — bé không thể
lẫn "cái nào là cái nào" như khi gặp hình vuông cạnh 4 (chu vi 16, diện tích 16).

Và nó chở luôn hai bài cuối đợt:
    tăng chiều dài thêm 3  →  diện tích thêm đúng 3 nhân 4, tức 12
    tăng dài 2 giảm rộng 1 →  8 nhân 3 vẫn bằng 24, diện tích KHÔNG đổi

── ĐỢT NÀY LÀM SÁU BÀI ──
Sáu bài sau (bốn loại góc · đường cao · cắt ghép · hình tròn · hình trải phẳng · đếm
khối) để đợt hai; B45 B46 tạm giữ nguyên bài chữ cũ.

    python3 tools/hinh_hoc_lop4.py --xem
    python3 tools/hinh_hoc_lop4.py
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

LUI_CV = {'ve': ['DL:KSN3.B27', 'DL:KSN3.B30'],
          'ten': ['CHU VI CÓ CÔNG THỨC', 'DIỆN TÍCH — TẤM THẢM Ô VUÔNG'],
          'canCu': 'sach', 'lopDuoi': 3}
LUI_DT = {'ve': ['DL:KSN3.B30'], 'ten': ['DIỆN TÍCH — TẤM THẢM Ô VUÔNG'],
          'canCu': 'chuDe', 'lopDuoi': 3}
LUI_BIEN = {'ve': ['DL:KSN3.B28', 'DL:KSN3.B30'],
            'ten': ['CHU VI BIẾN HÌNH', 'DIỆN TÍCH — TẤM THẢM Ô VUÔNG'],
            'canCu': 'sach', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B74 · CHU VI VÀ DIỆN TÍCH KHÁC NHAU CHỖ NÀO — bài KHÁI NIỆM
# ═══════════════════════════════════════════════════════════════════════════
# Đây là chỗ bé lẫn nhiều nhất cả chương, mà chưa bài nào dừng lại nói cho rõ. Hai
# chữ nghe na ná nhau, lại học cùng lúc, nên bé nhớ hai công thức rồi gán bừa.
B74 = bai(
    74, 'CHU VI VÀ DIỆN TÍCH KHÁC NHAU CHỖ NÀO',
    'Dạng gốc: HH 1.0 mức Lớp 4 — Phân biệt chu vi với diện tích bằng hình: một cái '
    'là đường đi quanh mép, một cái là mặt bị phủ kín. KHÔNG công thức.',
    'Lớp 3 con đã tính cả chu vi lẫn diện tích. Nhưng hai chữ ấy nghe na ná nhau nên '
    'rất dễ lẫn. Hôm nay mình dừng lại nhìn cho rõ: chúng đo hai thứ khác hẳn nhau, '
    'và đến đơn vị đo cũng khác.',
    LUI_CV,
    video(
        ['Nói được chu vi là đường đi quanh mép.',
         'Nói được diện tích là phần mặt bị phủ kín.',
         'Biết chu vi đo bằng mét, còn diện tích đo bằng mét vuông.'],
        ['Đề bài: Một mảnh vườn hình chữ nhật dài 6 mét, rộng 4 mét. Hãy chỉ ra đâu là '
         'chu vi, đâu là diện tích.',
         'Chu vi — đi quanh mép',
         'Tưởng tượng con đi bộ một vòng quanh mép vườn. Quãng đường ấy là chu vi.',
         'Đi hết một vòng: 6 rồi 4 rồi 6 rồi 4, cộng lại được 20 mét.',
         'Diện tích — phủ kín mặt',
         'Bây giờ tưởng tượng lát gạch kín cả mảnh vườn, mỗi viên gạch là ô vuông cạnh '
         '1 mét.',
         'Đếm số ô: mỗi hàng 6 ô, có 4 hàng, tất cả 24 ô. Diện tích là 24 mét vuông.',
         'Hai con số khác nhau',
         'Chu vi 20, diện tích 24. Chúng đo hai thứ khác hẳn nên đơn vị cũng khác: một '
         'bên mét, một bên mét vuông.',
         'Đáp số: chu vi 20 mét, diện tích 24 mét vuông.'],
        ['Có bạn tính xong rồi viết: "Diện tích mảnh vườn là 24 mét."',
         'Gợi ý 1: Con đếm 24 cái gì? Đếm mét hay đếm ô vuông?',
         'Gợi ý 2: Đếm ô vuông, mà mỗi ô là một mét vuông chứ.',
         'Chữa: diện tích phải ghi là 24 mét vuông. Ghi nhầm đơn vị là nói sai hẳn thứ '
         'mình vừa đo.'],
        ['Lấy một tờ giấy: bảo con lấy bút chì tô viền quanh mép, rồi lấy bút màu tô '
         'kín cả tờ. Hai việc ấy chính là chu vi và diện tích.',
         'Con lẫn hai chữ này là chuyện rất thường. Bố mẹ hỏi lại: "Con đang đo đường '
         'đi hay đo mặt phẳng?"'],
    ),
    [
        lt(1, 1, 'Mảnh vườn dài 6 mét, rộng 4 mét — đúng hình trong video. Đi một vòng '
                 'quanh mép vườn thì đi hết bao nhiêu mét?',
           'Đi bốn cạnh: 6 + 4 + 6 + 4 = 20 mét. Đó là chu vi.'),
        lt(2, 1, 'Vẫn mảnh vườn ấy. Lát gạch ô vuông cạnh 1 mét thì mỗi hàng mấy ô và '
                 'có mấy hàng?',
           'Mỗi hàng 6 ô, có 4 hàng.'),
        lt(3, 1, 'Vẫn mảnh vườn ấy. Đếm tất cả bao nhiêu ô, tức diện tích bằng bao nhiêu?',
           '6 × 4 = 24 ô, nên diện tích là 24 mét vuông.'),
        lt(4, 2, 'Bạn Nam viết "diện tích mảnh vườn là 24 mét". Bạn sai ở đâu?',
           'Diện tích đếm bằng ô vuông nên phải ghi là 24 mét vuông. Ghi mét là nói về '
           'đường đi, không phải mặt phẳng.'),
        lt(5, 2, 'Muốn rào lưới quanh vườn thì cần tính chu vi hay diện tích?',
           'Chu vi — vì lưới chạy quanh mép vườn.'),
        lt(6, 2, 'Muốn trồng cỏ phủ kín vườn thì cần tính chu vi hay diện tích?',
           'Diện tích — vì cỏ phủ kín cả mặt vườn.'),
        lt(7, 2, 'Một hình vuông cạnh 4 mét. Tính chu vi và diện tích, rồi cho biết vì '
                 'sao hai con số này dễ làm bé nhầm.',
           'Chu vi 4 × 4 = 16 mét; diện tích 4 × 4 = 16 mét vuông. Hai con số bằng nhau '
           'nên rất dễ tưởng chúng là một, dù chúng đo hai thứ khác hẳn.'),
        lt(8, 3, 'Một mảnh vườn dài 8 mét, rộng 3 mét. Tính chu vi và diện tích, ghi đủ '
                 'đơn vị.',
           'Chu vi: 8 + 3 + 8 + 3 = 22 mét. Diện tích: 8 × 3 = 24 mét vuông.'),
        lt(9, 3, 'Hai mảnh vườn: một mảnh 6 mét nhân 4 mét, một mảnh 8 mét nhân 3 mét. '
                 'Mảnh nào cần nhiều lưới rào hơn, mảnh nào trồng được nhiều cỏ hơn?',
           'Chu vi: mảnh đầu 20 mét, mảnh sau 22 mét — mảnh sau cần nhiều lưới hơn. '
           'Diện tích: cả hai đều 24 mét vuông — trồng được cỏ như nhau.'),
        q_tf(1, 'Chu vi là quãng đường đi quanh mép hình.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Diện tích cũng đo bằng mét như chu vi.', False,
             'SAI — diện tích đo bằng mét vuông.'),
        q_mcq(3, 'Mảnh vườn 6 mét nhân 4 mét có chu vi bằng:',
              ['A. 20 mét', 'B. 24 mét', 'C. 10 mét'], 'A. 20 mét', 'Đi hết bốn cạnh.'),
        q_mcq(4, 'Cũng mảnh vườn ấy có diện tích bằng:',
              ['A. 24 mét vuông', 'B. 20 mét vuông', 'C. 24 mét'],
              'A. 24 mét vuông', 'Đếm ô vuông phủ kín mặt.'),
        q_mcq(5, 'Muốn rào lưới quanh vườn thì tính:',
              ['A. chu vi', 'B. diện tích', 'C. cả hai'], 'A. chu vi',
              'Lưới chạy quanh mép.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B43 · HAI CÔNG THỨC  (mã cũ, viết lại — chỉ còn hai công thức)
# ═══════════════════════════════════════════════════════════════════════════
B43 = bai(
    43, 'HAI CÔNG THỨC — VÌ SAO CHU VI NHÂN ĐÔI, DIỆN TÍCH NHÂN CẠNH',
    'Dạng gốc: HH 1.1 mức Lớp 4 — Công thức chu vi và diện tích hình chữ nhật, suy ra '
    'từ hình chứ không nêu ra.',
    'Bài trước con đã biết chu vi và diện tích là hai thứ khác nhau. Hôm nay con viết '
    'chúng thành hai công thức — nhưng không phải học thuộc, mà nhìn hình rồi tự thấy '
    'vì sao lại thế.',
    LUI_CV,
    video(
        ['Suy ra được công thức chu vi từ việc đi quanh bốn cạnh.',
         'Suy ra được công thức diện tích từ việc đếm ô theo hàng.',
         'Giải thích được vì sao chu vi phải nhân đôi.'],
        ['Đề bài: Hình chữ nhật dài 6 mét, rộng 4 mét. Viết công thức tính chu vi và '
         'diện tích, rồi giải thích.',
         'Chu vi — đếm bốn cạnh',
         'Đi quanh hình gặp 6 rồi 4 rồi 6 rồi 4. Chiều dài gặp HAI lần, chiều rộng cũng '
         'gặp HAI lần.',
         'Nên gọn lại',
         'Thay vì cộng bốn số, ta cộng dài với rộng rồi nhân đôi: 6 cộng 4 được 10, '
         'nhân đôi được 20.',
         'Diện tích — đếm ô theo hàng',
         'Mỗi hàng có 6 ô, đúng bằng chiều dài. Có 4 hàng, đúng bằng chiều rộng.',
         'Nên đếm nhanh bằng phép nhân',
         'Số ô là 6 nhân 4, bằng 24. Không cần đếm từng ô một.',
         'Đáp số: chu vi 20 mét, diện tích 24 mét vuông.'],
        ['Có bạn tính chu vi là 6 cộng 4, ra 10 mét.',
         'Gợi ý 1: Con thử đi thật một vòng quanh hình xem gặp mấy cạnh?',
         'Gợi ý 2: Gặp bốn cạnh, mà bạn mới đi có hai.',
         'Chữa: chiều dài có hai cạnh, chiều rộng cũng có hai cạnh. Nên phải nhân đôi: '
         '(6 + 4) × 2 = 20 mét.'],
        ['Bảo con lấy ngón tay đi một vòng quanh hình và đếm to từng cạnh. Đếm ra bốn '
         'cạnh thì con hiểu ngay vì sao phải nhân đôi.',
         'Chỗ sai phổ biến nhất là quên nhân đôi. Bố mẹ hỏi: "Hình có mấy cạnh?"'],
    ),
    [
        lt(1, 1, 'Hình chữ nhật dài 6 mét, rộng 4 mét — đúng hình trong video. Đi quanh '
                 'hình thì gặp chiều dài mấy lần, chiều rộng mấy lần?',
           'Gặp chiều dài 2 lần và chiều rộng 2 lần.'),
        lt(2, 1, 'Vẫn hình ấy. Tính chu vi bằng công thức.',
           'Chu vi = (6 + 4) × 2 = 20 mét.'),
        lt(3, 1, 'Vẫn hình ấy. Mỗi hàng có mấy ô và có mấy hàng, nên diện tích bằng bao nhiêu?',
           'Mỗi hàng 6 ô, có 4 hàng, nên diện tích = 6 × 4 = 24 mét vuông.'),
        lt(4, 2, 'Bạn Lan tính chu vi là 6 + 4 = 10 mét. Bạn sai ở đâu?',
           'Bạn mới đi có hai cạnh. Hình có bốn cạnh nên phải nhân đôi, được 20 mét.'),
        lt(5, 2, 'Một hình chữ nhật dài 9 mét, rộng 5 mét. Tính chu vi và diện tích.',
           'Chu vi = (9 + 5) × 2 = 28 mét. Diện tích = 9 × 5 = 45 mét vuông.'),
        lt(6, 2, 'Vì sao diện tích tính bằng cách nhân chiều dài với chiều rộng?',
           'Vì mỗi hàng có số ô đúng bằng chiều dài, và số hàng đúng bằng chiều rộng. '
           'Nhân hai số ấy là đếm nhanh tất cả các ô.'),
        lt(7, 2, 'Một hình vuông cạnh 7 mét. Tính chu vi và diện tích.',
           'Chu vi = 7 × 4 = 28 mét. Diện tích = 7 × 7 = 49 mét vuông.'),
        lt(8, 3, 'Một mảnh đất dài 12 mét, rộng 8 mét. Tính chu vi và diện tích, ghi đủ '
                 'đơn vị.',
           'Chu vi = (12 + 8) × 2 = 40 mét. Diện tích = 12 × 8 = 96 mét vuông.'),
        lt(9, 3, 'Nửa chu vi của một hình chữ nhật là 10 mét, chiều dài 6 mét. Tính chiều '
                 'rộng và diện tích.',
           'Nửa chu vi là dài cộng rộng, nên chiều rộng = 10 − 6 = 4 mét. Diện tích = '
           '6 × 4 = 24 mét vuông.'),
        q_tf(1, 'Chu vi hình chữ nhật bằng chiều dài cộng chiều rộng rồi nhân đôi.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Chu vi hình chữ nhật bằng chiều dài cộng chiều rộng.', False,
             'SAI — còn phải nhân đôi vì hình có bốn cạnh.'),
        q_mcq(3, 'Hình dài 6 mét rộng 4 mét có chu vi:',
              ['A. 20 mét', 'B. 10 mét', 'C. 24 mét'], 'A. 20 mét', 'Nhân đôi tổng hai cạnh.'),
        q_mcq(4, 'Cũng hình ấy có diện tích:',
              ['A. 24 mét vuông', 'B. 20 mét vuông', 'C. 10 mét vuông'],
              'A. 24 mét vuông', 'Nhân chiều dài với chiều rộng.'),
        q_mcq(5, 'Vì sao chu vi phải nhân đôi?',
              ['A. Vì hình có hai chiều dài và hai chiều rộng',
               'B. Vì hình có hai chiều', 'C. Vì phải làm tròn'],
              'A. Vì hình có hai chiều dài và hai chiều rộng', 'Đi quanh gặp bốn cạnh.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B75 · ĐƠN VỊ ĐO DIỆN TÍCH
# ═══════════════════════════════════════════════════════════════════════════
B75 = bai(
    75, 'ĐƠN VỊ ĐO DIỆN TÍCH — VÌ SAO ĐỔI ĐƠN VỊ LẠI NHÂN TRĂM',
    'Dạng gốc: HH 1.3 mức Lớp 4 — Mét vuông, đề-xi-mét vuông, héc-ta và cách đổi; '
    'giải thích vì sao bậc đổi là một trăm chứ không phải mười.',
    'Đo chiều dài thì một mét bằng mười đề-xi-mét. Nhưng đo diện tích thì một mét '
    'vuông lại bằng MỘT TRĂM đề-xi-mét vuông. Nghe rất lạ — hôm nay con sẽ thấy vì '
    'sao, và thấy rồi thì chẳng bao giờ nhớ nhầm nữa.',
    LUI_DT,
    video(
        ['Biết một mét vuông bằng một trăm đề-xi-mét vuông.',
         'Giải thích được vì sao bậc đổi là một trăm.',
         'Biết một héc-ta bằng mười nghìn mét vuông.'],
        ['Đề bài: Một mét vuông bằng bao nhiêu đề-xi-mét vuông? Vì sao lại thế?',
         'Vẽ một mét vuông ra',
         'Đó là ô vuông cạnh một mét. Mà một mét bằng mười đề-xi-mét.',
         'Chia cả hai chiều',
         'Chiều ngang chia được mười phần, chiều dọc cũng chia được mười phần.',
         'Đếm số ô nhỏ',
         'Mỗi hàng mười ô, có mười hàng, nên tất cả là mười nhân mười, bằng một trăm ô.',
         'Nên bậc đổi là một trăm',
         'Vì diện tích chia theo CẢ HAI chiều, chứ chiều dài chỉ chia theo một chiều.',
         'Héc-ta cũng thế',
         'Một héc-ta là ô vuông cạnh một trăm mét, nên nó bằng một trăm nhân một trăm, '
         'tức mười nghìn mét vuông.',
         'Đáp số: một mét vuông bằng một trăm đề-xi-mét vuông.'],
        ['Có bạn nhớ một mét bằng mười đề-xi-mét nên bảo một mét vuông bằng mười đề-xi-'
         'mét vuông.',
         'Gợi ý 1: Con vẽ ô vuông ấy ra rồi chia cả hai chiều xem được mấy ô nhỏ.',
         'Gợi ý 2: Chia ngang được mười, chia dọc cũng mười. Vậy tất cả mấy ô?',
         'Chữa: được một trăm ô. Đo diện tích thì chia theo cả hai chiều nên bậc đổi '
         'phải nhân hai lần.'],
        ['Vẽ một ô vuông rồi chia mỗi chiều làm mười phần. Bảo con đếm số ô nhỏ — con '
         'sẽ tự thấy con số một trăm.',
         'Con hay lấy bậc đổi của chiều dài áp cho diện tích. Bố mẹ nhắc: diện tích có '
         'hai chiều nên nhân hai lần.'],
    ),
    [
        lt(1, 1, 'Một ô vuông cạnh 1 mét. Chia mỗi chiều thành các phần dài 1 đề-xi-mét '
                 'thì mỗi chiều được mấy phần?',
           'Mỗi chiều được 10 phần, vì 1 mét bằng 10 đề-xi-mét.'),
        lt(2, 1, 'Vẫn ô vuông ấy. Đếm tất cả bao nhiêu ô nhỏ?',
           '10 × 10 = 100 ô nhỏ. Vậy 1 mét vuông bằng 100 đề-xi-mét vuông.'),
        lt(3, 1, 'Một héc-ta là ô vuông cạnh 100 mét. Vậy một héc-ta bằng bao nhiêu mét '
                 'vuông?',
           '100 × 100 = 10 000 mét vuông.'),
        lt(4, 2, 'Bạn Bình bảo một mét vuông bằng mười đề-xi-mét vuông. Bạn sai ở đâu?',
           'Bạn lấy bậc đổi của chiều dài áp cho diện tích. Diện tích chia theo cả hai '
           'chiều nên phải nhân hai lần, được 100.'),
        lt(5, 2, 'Đổi 3 mét vuông ra đề-xi-mét vuông.',
           '3 × 100 = 300 đề-xi-mét vuông.'),
        lt(6, 2, 'Đổi 2 héc-ta ra mét vuông.',
           '2 × 10 000 = 20 000 mét vuông.'),
        lt(7, 2, 'Vì sao bậc đổi của diện tích lớn hơn bậc đổi của chiều dài?',
           'Vì chiều dài chỉ chia theo một chiều, còn diện tích chia theo cả hai chiều. '
           'Nên bậc đổi phải nhân với chính nó.'),
        lt(8, 3, 'Một mảnh ruộng rộng 5 héc-ta. Hỏi mảnh ruộng ấy bao nhiêu mét vuông?',
           '5 × 10 000 = 50 000 mét vuông.'),
        lt(9, 3, 'Một mảnh vườn hình chữ nhật dài 6 mét, rộng 4 mét. Diện tích mảnh vườn '
                 'bằng bao nhiêu đề-xi-mét vuông?',
           'Diện tích là 6 × 4 = 24 mét vuông. Đổi ra: 24 × 100 = 2 400 đề-xi-mét vuông.'),
        q_tf(1, 'Một mét vuông bằng một trăm đề-xi-mét vuông.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Một mét vuông bằng mười đề-xi-mét vuông.', False,
             'SAI — diện tích chia theo cả hai chiều nên bậc đổi là một trăm.'),
        q_mcq(3, 'Một héc-ta bằng:',
              ['A. 10 000 mét vuông', 'B. 1 000 mét vuông', 'C. 100 mét vuông'],
              'A. 10 000 mét vuông', 'Ô vuông cạnh một trăm mét.'),
        q_mcq(4, 'Vì sao bậc đổi diện tích là một trăm?',
              ['A. Vì chia theo cả hai chiều nên nhân hai lần',
               'B. Vì mét vuông lớn hơn', 'C. Vì phải làm tròn'],
              'A. Vì chia theo cả hai chiều nên nhân hai lần', 'Mười nhân mười.'),
        q_mcq(5, 'Đổi 3 mét vuông ra đề-xi-mét vuông được:',
              ['A. 300', 'B. 30', 'C. 3 000'], 'A. 300', 'Nhân với một trăm.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B76 · BIẾT DIỆN TÍCH TÌM CẠNH — bài ngược
# ═══════════════════════════════════════════════════════════════════════════
B76 = bai(
    76, 'BIẾT DIỆN TÍCH TÌM CẠNH — ĐỌC NGƯỢC PHÉP NHÂN',
    'Dạng gốc: HH 1.4 mức Lớp 4 — Bài toán ngược: biết diện tích và một cạnh, tìm cạnh '
    'kia; biết chu vi và một cạnh, tìm cạnh kia.',
    'Hai bài trước con có hai cạnh rồi tính ra chu vi và diện tích. Hôm nay đề làm '
    'ngược lại: cho con kết quả rồi bắt tìm cạnh. Vẫn công thức ấy, chỉ đọc ngược lại '
    'thôi.',
    LUI_DT,
    video(
        ['Từ diện tích và một cạnh, tìm cạnh còn lại.',
         'Từ chu vi và một cạnh, tìm cạnh còn lại.',
         'Thử lại bằng cách tính xuôi.'],
        ['Đề bài: Một hình chữ nhật có diện tích 24 mét vuông, chiều dài 6 mét. Tính '
         'chiều rộng.',
         'Nhớ lại chiều xuôi',
         'Diện tích bằng chiều dài nhân chiều rộng. Ở đây: 6 nhân chiều rộng bằng 24.',
         'Đọc ngược phép nhân',
         'Nếu 6 nhân một số ra 24 thì số ấy là 24 chia 6, bằng 4 mét.',
         'Nghĩ theo hình cũng ra thế',
         'Mỗi hàng có 6 ô, tất cả 24 ô, nên số hàng là 24 chia 6, bằng 4 hàng.',
         'Còn nếu đề cho chu vi',
         'Chu vi 20 mét thì nửa chu vi là 10 mét, đó là dài cộng rộng. Biết dài 6 thì '
         'rộng là 10 trừ 6, bằng 4 mét.',
         'Thử lại',
         '6 nhân 4 bằng 24, đúng bằng diện tích đề cho.',
         'Đáp số: chiều rộng 4 mét.'],
        ['Có bạn thấy diện tích 24 và chiều dài 6 rồi lấy 24 trừ 6.',
         'Gợi ý 1: Diện tích tính bằng phép gì từ hai cạnh?',
         'Gợi ý 2: Bằng phép nhân. Vậy đi ngược lại phải là phép gì?',
         'Chữa: phải chia, không phải trừ. Đi ngược của phép nhân là phép chia, được '
         '24 chia 6 bằng 4 mét.'],
        ['Xếp 24 hạt đậu thành các hàng 6 hạt rồi bảo con đếm số hàng. Con đếm ra bốn '
         'hàng là đã hiểu.',
         'Chỗ sai duy nhất là chọn nhầm phép. Bố mẹ hỏi: "Đi xuôi là nhân, vậy đi ngược '
         'là gì?"'],
    ),
    [
        lt(1, 1, 'Hình chữ nhật có diện tích 24 mét vuông, chiều dài 6 mét — đúng bài '
                 'trong video. Đi xuôi thì diện tích tính bằng phép gì?',
           'Bằng phép nhân: chiều dài nhân chiều rộng.'),
        lt(2, 1, 'Vẫn bài trên. Vậy tính chiều rộng bằng phép gì và bằng bao nhiêu?',
           'Bằng phép chia: 24 : 6 = 4 mét.'),
        lt(3, 1, 'Một hình chữ nhật có chu vi 20 mét. Nửa chu vi bằng bao nhiêu?',
           '20 : 2 = 10 mét — đó chính là chiều dài cộng chiều rộng.'),
        lt(4, 2, 'Bạn Tú lấy 24 trừ 6 để tìm chiều rộng. Bạn sai ở đâu?',
           'Diện tích tính bằng phép NHÂN nên đi ngược phải là phép CHIA, được 4 mét.'),
        lt(5, 2, 'Hình chữ nhật có chu vi 20 mét, chiều dài 6 mét. Tính chiều rộng.',
           'Nửa chu vi 10 mét là dài cộng rộng, nên chiều rộng = 10 − 6 = 4 mét.'),
        lt(6, 2, 'Một hình chữ nhật có diện tích 45 mét vuông, chiều rộng 5 mét. Tính '
                 'chiều dài.',
           '45 : 5 = 9 mét.'),
        lt(7, 2, 'Một hình vuông có diện tích 49 mét vuông. Tính cạnh hình vuông.',
           'Hình vuông có hai cạnh bằng nhau, mà 7 × 7 = 49, nên cạnh bằng 7 mét.'),
        lt(8, 3, 'Một mảnh đất có diện tích 96 mét vuông, chiều dài 12 mét. Tính chiều '
                 'rộng và chu vi.',
           'Chiều rộng = 96 : 12 = 8 mét. Chu vi = (12 + 8) × 2 = 40 mét.'),
        lt(9, 3, 'Một hình chữ nhật có chu vi 20 mét và diện tích 24 mét vuông. Tìm hai '
                 'cạnh của nó.',
           'Nửa chu vi 10 mét là tổng hai cạnh. Thử các cặp có tổng 10: cặp 6 và 4 cho '
           'tích 24, đúng diện tích đề cho. Vậy hai cạnh là 6 mét và 4 mét.'),
        q_tf(1, 'Biết diện tích và một cạnh thì tìm cạnh kia bằng phép chia.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Biết diện tích và một cạnh thì tìm cạnh kia bằng phép trừ.', False,
             'SAI — đi ngược của phép nhân là phép chia.'),
        q_mcq(3, 'Diện tích 24 mét vuông, chiều dài 6 mét thì chiều rộng bằng:',
              ['A. 4 mét', 'B. 18 mét', 'C. 30 mét'], 'A. 4 mét', '24 chia 6.'),
        q_mcq(4, 'Chu vi 20 mét thì nửa chu vi bằng:',
              ['A. 10 mét', 'B. 40 mét', 'C. 5 mét'], 'A. 10 mét', 'Chia đôi chu vi.'),
        q_mcq(5, 'Nửa chu vi chính là:',
              ['A. chiều dài cộng chiều rộng', 'B. chiều dài nhân chiều rộng',
               'C. chiều dài trừ chiều rộng'],
              'A. chiều dài cộng chiều rộng', 'Vì chu vi là tổng ấy nhân đôi.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B44 · TĂNG MỘT CHIỀU  (mã cũ, viết lại — chỉ còn một chiều)
# ═══════════════════════════════════════════════════════════════════════════
B44 = bai(
    44, 'TĂNG MỘT CHIỀU — DIỆN TÍCH THÊM ĐÚNG MỘT DẢI',
    'Dạng gốc: HH 1.2a mức Lớp 4 — Tăng hoặc giảm một chiều, phần diện tích đổi bằng '
    'phần thêm nhân chiều kia.',
    'Hôm nay con xem điều gì xảy ra khi kéo dài một cạnh của hình. Nhìn hình thì thấy '
    'ngay: phần diện tích thêm vào là một DẢI, và dải ấy tính rất gọn.',
    LUI_BIEN,
    video(
        ['Thấy phần diện tích thêm vào là một dải hình chữ nhật.',
         'Tính phần thêm bằng phần kéo dài nhân chiều kia.',
         'Biết chu vi cũng đổi, nhưng đổi khác cách.'],
        ['Đề bài: Hình chữ nhật dài 6 mét, rộng 4 mét. Kéo dài chiều dài thêm 3 mét thì '
         'diện tích tăng thêm bao nhiêu?',
         'Vẽ phần thêm vào',
         'Hình cũ dài 6, nay dài 9. Phần thêm là một dải rộng 3 mét và cao 4 mét.',
         'Dải ấy cũng là hình chữ nhật',
         'Nên diện tích dải là 3 nhân 4, bằng 12 mét vuông.',
         'Kiểm lại bằng cách tính cả hình',
         'Hình mới: 9 nhân 4 bằng 36. Hình cũ: 6 nhân 4 bằng 24. Chênh nhau đúng 12.',
         'Nên nhớ một điều gọn',
         'Kéo dài thêm bao nhiêu thì diện tích thêm đúng phần ấy nhân với chiều KIA.',
         'Đáp số: diện tích tăng thêm 12 mét vuông.'],
        ['Có bạn nghĩ kéo dài thêm 3 mét thì diện tích cũng tăng thêm 3 mét vuông.',
         'Gợi ý 1: Con vẽ phần thêm ra xem nó là hình gì?',
         'Gợi ý 2: Nó là một dải rộng 3 mét nhưng cao tận 4 mét, đâu phải một ô.',
         'Chữa: phần thêm là cả một dải, diện tích bằng 3 nhân 4, tức 12 mét vuông.'],
        ['Cắt thêm một dải giấy rồi dán vào cạnh hình cũ. Con nhìn thấy dải ấy rộng bao '
         'nhiêu và cao bao nhiêu là hiểu ngay.',
         'Con hay nghĩ thêm mấy mét thì thêm mấy mét vuông. Bố mẹ hỏi: "Phần thêm cao '
         'bao nhiêu?"'],
    ),
    [
        lt(1, 1, 'Hình dài 6 mét rộng 4 mét, kéo dài thêm 3 mét — đúng bài trong video. '
                 'Chiều dài mới bằng bao nhiêu?',
           '6 + 3 = 9 mét.'),
        lt(2, 1, 'Vẫn bài trên. Phần thêm vào là một dải rộng mấy mét và cao mấy mét?',
           'Rộng 3 mét (phần kéo dài) và cao 4 mét (chiều kia giữ nguyên).'),
        lt(3, 1, 'Vẫn bài trên. Diện tích tăng thêm bao nhiêu?',
           '3 × 4 = 12 mét vuông.'),
        lt(4, 2, 'Bạn Hoa nghĩ kéo dài thêm 3 mét thì diện tích thêm 3 mét vuông. Bạn '
                 'sai ở đâu?',
           'Phần thêm là cả một dải cao 4 mét, chứ không phải một ô. Diện tích thêm là '
           '3 × 4 = 12 mét vuông.'),
        lt(5, 2, 'Kiểm lại bằng cách tính diện tích hình mới và hình cũ rồi trừ nhau.',
           'Hình mới 9 × 4 = 36; hình cũ 6 × 4 = 24. Chênh nhau 36 − 24 = 12 mét vuông.'),
        lt(6, 2, 'Một hình chữ nhật dài 8 mét rộng 5 mét. Kéo dài chiều dài thêm 2 mét '
                 'thì diện tích tăng thêm bao nhiêu?',
           '2 × 5 = 10 mét vuông.'),
        lt(7, 2, 'Vẫn hình 6 mét nhân 4 mét. Nếu tăng chiều RỘNG thêm 3 mét thì diện '
                 'tích tăng thêm bao nhiêu?',
           'Lần này dải nằm ngang, rộng 6 mét và cao 3 mét, nên tăng 6 × 3 = 18 mét vuông.'),
        lt(8, 3, 'Một mảnh vườn dài 10 mét rộng 6 mét. Người ta cắt bớt chiều dài đi 2 '
                 'mét. Diện tích giảm đi bao nhiêu?',
           'Phần cắt là dải rộng 2 mét cao 6 mét, nên giảm 2 × 6 = 12 mét vuông.'),
        lt(9, 3, 'Hình 6 mét nhân 4 mét, kéo dài chiều dài thêm 3 mét. Tính chu vi hình '
                 'mới và cho biết chu vi tăng thêm bao nhiêu.',
           'Chu vi mới = (9 + 4) × 2 = 26 mét. Chu vi cũ 20 mét, nên tăng 6 mét — đúng '
           'bằng phần kéo dài nhân đôi.'),
        q_tf(1, 'Kéo dài một chiều thì diện tích thêm bằng phần kéo dài nhân chiều kia.',
             True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Kéo dài thêm 3 mét thì diện tích thêm 3 mét vuông.', False,
             'SAI — phần thêm là cả một dải.'),
        q_mcq(3, 'Hình 6 mét nhân 4 mét, kéo dài thêm 3 mét thì diện tích thêm:',
              ['A. 12 mét vuông', 'B. 3 mét vuông', 'C. 36 mét vuông'],
              'A. 12 mét vuông', 'Dải rộng 3 cao 4.'),
        q_mcq(4, 'Cũng hình ấy, nếu tăng chiều rộng thêm 3 mét thì diện tích thêm:',
              ['A. 18 mét vuông', 'B. 12 mét vuông', 'C. 3 mét vuông'],
              'A. 18 mét vuông', 'Dải rộng 6 cao 3.'),
        q_mcq(5, 'Phần diện tích thêm vào có hình dạng:',
              ['A. một dải hình chữ nhật', 'B. một ô vuông', 'C. một hình tròn'],
              'A. một dải hình chữ nhật', 'Nó chạy dọc theo cạnh kia.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B77 · TĂNG CHIỀU NÀY GIẢM CHIỀU KIA
# ═══════════════════════════════════════════════════════════════════════════
B77 = bai(
    77, 'TĂNG CHIỀU NÀY GIẢM CHIỀU KIA — DIỆN TÍCH CÓ THỂ KHÔNG ĐỔI',
    'Dạng gốc: HH 1.2b mức Lớp 4 — Tăng một chiều đồng thời giảm chiều kia; diện tích '
    'đổi hay không tuỳ vào tích hai cạnh mới.',
    'Bài trước con chỉ đổi MỘT chiều. Hôm nay đổi cả hai cùng lúc, một chiều tăng và '
    'một chiều giảm — và con sẽ gặp một chuyện thú vị: đôi khi diện tích chẳng đổi '
    'chút nào, dù hình trông khác hẳn.',
    LUI_BIEN,
    video(
        ['Tính diện tích hình mới khi cả hai chiều cùng đổi.',
         'Thấy diện tích có thể giữ nguyên dù hình khác hẳn.',
         'Biết chu vi thì lại đổi, chứ không giữ nguyên như diện tích.'],
        ['Đề bài: Hình chữ nhật dài 6 mét rộng 4 mét. Tăng chiều dài thêm 2 mét và giảm '
         'chiều rộng đi 1 mét. Diện tích đổi thế nào?',
         'Tính hai cạnh mới',
         'Chiều dài mới là 6 cộng 2, bằng 8 mét. Chiều rộng mới là 4 trừ 1, bằng 3 mét.',
         'Tính diện tích mới',
         '8 nhân 3 bằng 24 mét vuông.',
         'So với hình cũ',
         'Hình cũ là 6 nhân 4, cũng bằng 24 mét vuông. Diện tích KHÔNG đổi.',
         'Hình khác hẳn mà diện tích như nhau',
         'Một hình dài và hẹp, một hình ngắn và rộng, nhưng phủ kín cùng một mặt.',
         'Còn chu vi thì sao',
         'Chu vi cũ là 20 mét, chu vi mới là 8 cộng 3 rồi nhân đôi, bằng 22 mét. Chu vi '
         'ĐỔI, dù diện tích không đổi.',
         'Đáp số: diện tích vẫn 24 mét vuông, còn chu vi tăng từ 20 lên 22 mét.'],
        ['Có bạn nghĩ tăng 2 rồi giảm 1 thì bù trừ nhau nên cả hai đều không đổi.',
         'Gợi ý 1: Con tính thử chu vi cũ và chu vi mới xem.',
         'Gợi ý 2: Một bên 20 mét, một bên 22 mét — đâu có bằng nhau.',
         'Chữa: diện tích không đổi nhưng chu vi thì đổi. Diện tích tính bằng phép nhân '
         'còn chu vi tính bằng phép cộng, nên chúng phản ứng khác nhau.'],
        ['Lấy 24 viên bi xếp thành hình 6 nhân 4 rồi xếp lại thành 8 nhân 3. Con thấy '
         'số bi vẫn thế mà hình khác hẳn.',
         'Chỗ hay nhầm là tưởng cái gì cũng bù trừ được. Bố mẹ hỏi riêng từng thứ: '
         '"Diện tích thế nào? Còn chu vi thì sao?"'],
    ),
    [
        lt(1, 1, 'Hình dài 6 mét rộng 4 mét, tăng dài 2 mét giảm rộng 1 mét — đúng bài '
                 'trong video. Hai cạnh mới bằng bao nhiêu?',
           'Chiều dài mới 6 + 2 = 8 mét; chiều rộng mới 4 − 1 = 3 mét.'),
        lt(2, 1, 'Vẫn bài trên. Diện tích hình mới bằng bao nhiêu?',
           '8 × 3 = 24 mét vuông.'),
        lt(3, 1, 'Vẫn bài trên. So với hình cũ thì diện tích đổi thế nào?',
           'Hình cũ 6 × 4 = 24 mét vuông, nên diện tích KHÔNG đổi.'),
        lt(4, 2, 'Vẫn bài trên. Tính chu vi cũ và chu vi mới rồi so.',
           'Chu vi cũ (6 + 4) × 2 = 20 mét; chu vi mới (8 + 3) × 2 = 22 mét. Chu vi tăng '
           '2 mét.'),
        lt(5, 2, 'Bạn Minh nghĩ tăng 2 giảm 1 thì mọi thứ đều bù trừ nên chẳng đổi gì. '
                 'Bạn sai ở đâu?',
           'Diện tích thì không đổi thật, nhưng chu vi lại đổi. Diện tích tính bằng phép '
           'nhân còn chu vi tính bằng phép cộng nên chúng phản ứng khác nhau.'),
        lt(6, 2, 'Hình chữ nhật dài 10 mét rộng 6 mét. Tăng dài 2 mét, giảm rộng 1 mét. '
                 'Diện tích mới bằng bao nhiêu và có đổi không?',
           'Hình mới 12 × 5 = 60 mét vuông; hình cũ 10 × 6 = 60 mét vuông. Không đổi.'),
        lt(7, 2, 'Hình dài 6 mét rộng 4 mét. Tăng dài 2 mét và giảm rộng 2 mét. Diện tích '
                 'mới bằng bao nhiêu?',
           'Hình mới 8 × 2 = 16 mét vuông, ít hơn hình cũ 24 mét vuông. Lần này diện tích '
           'GIẢM.'),
        lt(8, 3, 'Vì sao có lúc diện tích không đổi, có lúc lại đổi?',
           'Vì diện tích là TÍCH hai cạnh. Chỉ khi tích hai cạnh mới bằng tích hai cạnh '
           'cũ thì diện tích mới giữ nguyên; phải tính ra mới biết, không đoán được.'),
        lt(9, 3, 'Tìm một cách đổi hai cạnh của hình 6 mét nhân 4 mét sao cho diện tích '
                 'vẫn là 24 mét vuông nhưng hình khác đi.',
           'Cần hai số có tích bằng 24: ví dụ 12 và 2, hoặc 24 và 1. Chẳng hạn hình 12 '
           'mét nhân 2 mét cũng có diện tích 24 mét vuông.'),
        q_tf(1, 'Tăng chiều này giảm chiều kia thì diện tích có thể giữ nguyên.', True,
             'Đáp án: ĐÚNG — nhưng phải tính mới biết.'),
        q_tf(2, 'Diện tích giữ nguyên thì chu vi cũng giữ nguyên.', False,
             'SAI — chu vi vẫn đổi.'),
        q_mcq(3, 'Hình 6 nhân 4, tăng dài 2 giảm rộng 1 thì diện tích mới:',
              ['A. 24 mét vuông', 'B. 22 mét vuông', 'C. 30 mét vuông'],
              'A. 24 mét vuông', 'Tám nhân ba.'),
        q_mcq(4, 'Cũng hình ấy, chu vi mới bằng:',
              ['A. 22 mét', 'B. 20 mét', 'C. 24 mét'], 'A. 22 mét', 'Tổng hai cạnh mới nhân đôi.'),
        q_mcq(5, 'Muốn biết diện tích có đổi hay không thì:',
              ['A. phải tính tích hai cạnh mới', 'B. cứ bù trừ là xong',
               'C. nhìn hình là biết'],
              'A. phải tính tích hai cạnh mới', 'Diện tích là tích hai cạnh.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
MOI = [B74, B43, B75, B76, B44, B77]
SAU = {'DL:KSN4.B75': 'DL:KSN4.B43', 'DL:KSN4.B76': 'DL:KSN4.B75',
       'DL:KSN4.B77': 'DL:KSN4.B44'}

O_NHAP_MOI = {
    'DL:KSN4.B74#C1': {'value': 20},
    'DL:KSN4.B74#C2': {'parts': [{'label': 'mỗi hàng mấy ô', 'value': 6},
                                 {'label': 'mấy hàng', 'value': 4}]},
    'DL:KSN4.B74#C3': {'value': 24},
    'DL:KSN4.B74#C4': {'parts': [{'label': 'đơn vị đúng',
                                  'options': ['mét vuông', 'mét'], 'value': 'mét vuông'}]},
    'DL:KSN4.B74#C5': {'parts': [{'label': 'cần tính', 'options': ['chu vi', 'diện tích'],
                                  'value': 'chu vi'}]},
    'DL:KSN4.B74#C6': {'parts': [{'label': 'cần tính', 'options': ['diện tích', 'chu vi'],
                                  'value': 'diện tích'}]},
    'DL:KSN4.B74#C7': {'parts': [{'label': 'chu vi', 'value': 16},
                                 {'label': 'diện tích', 'value': 16}]},
    'DL:KSN4.B74#C8': {'parts': [{'label': 'chu vi', 'value': 22},
                                 {'label': 'diện tích', 'value': 24}]},
    'DL:KSN4.B74#C9': {'parts': [{'label': 'mảnh cần nhiều lưới hơn có chu vi', 'value': 22},
                                 {'label': 'diện tích hai mảnh', 'value': 24}]},

    'DL:KSN4.B43#C1': {'parts': [{'label': 'chiều dài gặp mấy lần', 'value': 2},
                                 {'label': 'chiều rộng gặp mấy lần', 'value': 2}]},
    'DL:KSN4.B43#C2': {'value': 20},
    'DL:KSN4.B43#C3': {'parts': [{'label': 'mỗi hàng mấy ô', 'value': 6},
                                 {'label': 'diện tích', 'value': 24}]},
    'DL:KSN4.B43#C4': {'parts': [{'label': 'chu vi đúng', 'value': 20}]},
    'DL:KSN4.B43#C5': {'parts': [{'label': 'chu vi', 'value': 28},
                                 {'label': 'diện tích', 'value': 45}]},
    'DL:KSN4.B43#C6': {'parts': [{'label': 'số ô mỗi hàng bằng chiều nào',
                                  'options': ['chiều dài', 'chiều rộng'],
                                  'value': 'chiều dài'}]},
    'DL:KSN4.B43#C7': {'parts': [{'label': 'chu vi', 'value': 28},
                                 {'label': 'diện tích', 'value': 49}]},
    'DL:KSN4.B43#C8': {'parts': [{'label': 'chu vi', 'value': 40},
                                 {'label': 'diện tích', 'value': 96}]},
    'DL:KSN4.B43#C9': {'parts': [{'label': 'chiều rộng', 'value': 4},
                                 {'label': 'diện tích', 'value': 24}]},

    'DL:KSN4.B75#C1': {'value': 10},
    'DL:KSN4.B75#C2': {'value': 100},
    'DL:KSN4.B75#C3': {'value': 10000},
    'DL:KSN4.B75#C4': {'parts': [{'label': 'bậc đổi đúng', 'value': 100}]},
    'DL:KSN4.B75#C5': {'value': 300},
    'DL:KSN4.B75#C6': {'value': 20000},
    'DL:KSN4.B75#C7': {'parts': [{'label': 'diện tích chia theo mấy chiều', 'value': 2}]},
    'DL:KSN4.B75#C8': {'value': 50000},
    'DL:KSN4.B75#C9': {'parts': [{'label': 'diện tích theo mét vuông', 'value': 24},
                                 {'label': 'theo đề-xi-mét vuông', 'value': 2400}]},

    'DL:KSN4.B76#C1': {'parts': [{'label': 'phép tính', 'options': ['nhân', 'cộng'],
                                  'value': 'nhân'}]},
    'DL:KSN4.B76#C2': {'parts': [{'label': 'phép tính', 'options': ['chia', 'trừ'],
                                  'value': 'chia'},
                                 {'label': 'chiều rộng', 'value': 4}]},
    'DL:KSN4.B76#C3': {'value': 10},
    'DL:KSN4.B76#C4': {'parts': [{'label': 'phép đúng', 'options': ['chia', 'trừ'],
                                  'value': 'chia'},
                                 {'label': 'chiều rộng', 'value': 4}]},
    'DL:KSN4.B76#C5': {'value': 4},
    'DL:KSN4.B76#C6': {'value': 9},
    'DL:KSN4.B76#C7': {'value': 7},
    'DL:KSN4.B76#C8': {'parts': [{'label': 'chiều rộng', 'value': 8},
                                 {'label': 'chu vi', 'value': 40}]},
    'DL:KSN4.B76#C9': {'parts': [{'label': 'cạnh dài', 'value': 6},
                                 {'label': 'cạnh ngắn', 'value': 4}]},

    'DL:KSN4.B44#C1': {'value': 9},
    'DL:KSN4.B44#C2': {'parts': [{'label': 'dải rộng mấy mét', 'value': 3},
                                 {'label': 'dải cao mấy mét', 'value': 4}]},
    'DL:KSN4.B44#C3': {'value': 12},
    'DL:KSN4.B44#C4': {'parts': [{'label': 'diện tích thêm đúng', 'value': 12}]},
    'DL:KSN4.B44#C5': {'parts': [{'label': 'hình mới', 'value': 36},
                                 {'label': 'hình cũ', 'value': 24},
                                 {'label': 'chênh nhau', 'value': 12}]},
    'DL:KSN4.B44#C6': {'value': 10},
    'DL:KSN4.B44#C7': {'value': 18},
    'DL:KSN4.B44#C8': {'value': 12},
    'DL:KSN4.B44#C9': {'parts': [{'label': 'chu vi mới', 'value': 26},
                                 {'label': 'tăng thêm', 'value': 6}]},

    'DL:KSN4.B77#C1': {'parts': [{'label': 'chiều dài mới', 'value': 8},
                                 {'label': 'chiều rộng mới', 'value': 3}]},
    'DL:KSN4.B77#C2': {'value': 24},
    'DL:KSN4.B77#C3': {'parts': [{'label': 'diện tích có đổi không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B77#C4': {'parts': [{'label': 'chu vi cũ', 'value': 20},
                                 {'label': 'chu vi mới', 'value': 22}]},
    'DL:KSN4.B77#C5': {'parts': [{'label': 'diện tích có đổi không', 'options': CO_KHONG,
                                  'value': 'không'},
                                 {'label': 'chu vi có đổi không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B77#C6': {'value': 60},
    'DL:KSN4.B77#C7': {'value': 16},
    'DL:KSN4.B77#C8': {'parts': [{'label': 'diện tích là phép gì của hai cạnh',
                                  'options': ['tích', 'tổng'], 'value': 'tích'}]},
    'DL:KSN4.B77#C9': {'parts': [{'label': 'một cạnh', 'value': 12},
                                 {'label': 'cạnh kia', 'value': 2}]},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    van = ' '.join(x['text'] + x['loiChua'] for x in B74['cau'])
    if '(6 + 4) × 2' in van:
        loi.append('B74 là bài KHÁI NIỆM, chưa được nêu công thức')
    cu = {f'DL:KSN4.B{n}' for n in (43, 44)}
    moi_ = {f'DL:KSN4.B{n}' for n in (74, 75, 76, 77)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        van = json.dumps(b, ensure_ascii=False)
        if '6 mét' not in van and '24' not in van and '6 × 4' not in van:
            loi.append(f'{b["id"]}: thiếu số neo 6 nhân 4 của chương')
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
    ds = [x for x in tt['thuTu'] if x not in SAU and x != 'DL:KSN4.B74']
    ds.insert(ds.index('DL:KSN4.B43'), 'DL:KSN4.B74')
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
