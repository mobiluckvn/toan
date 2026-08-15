# -*- coding: utf-8 -*-
"""LỚP 2 · CHƯƠNG 1 · VƯƠNG QUỐC SỐ — năm bài chữ thành mười bài video.

Đợt đầu tiên của quyển lớp 2. Năm bài cũ đều gộp ba bốn ý:

  · B01 gộp cấu tạo số, giá trị theo phòng, tách thành tổng, VÀ so sánh hai số;
  · B02 gộp thêm số 0 với xoá số 0 — hai chiều ngược nhau;
  · B03 gộp "số nào lớn hơn" với "hiệu mang họ chín";
  · B04 gộp xếp thẻ thường với ca có thẻ số 0;
  · B05 đứng riêng — liệt kê có thứ tự.

── BÁC CHỐT: VIDEO KHÔNG NHÂN VẬT, GIỐNG HỆT LỚP 4 ──
Quyển lớp 2 lấy nhân vật làm khung (phụ đề kệ sách, tên chương), nhưng video thì đi
thẳng vào toán. Nên bốn mục còn chữ của bài cũng bỏ tên nhân vật luôn — để bé xem
video xong đọc tiếp không thấy đổi giọng.

── SỐ NEO ──
    245 và 368     ba phòng, giá trị chữ số, tách thành tổng
    507            chữ số 0 giữ chỗ
    25 và 52       đổi chỗ hai chữ số
    thẻ 8, 5, 2    xếp thẻ; thẻ 0, 3, 7 cho ca có số 0
    tổng bằng 5    liệt kê có thứ tự

── KHÁC LỚP 4 BA CHỖ ──
Tám mục (không có dựng mô hình và lắp - soi) · số câu luyện tập không cố định · và
LUẬT Ô NHẬP SỐ 1: quyển đọc chậm KHÔNG được có ô gõ chữ, đáp không phải số thì phải
cho bấm nút. Xem `tools/khuon_bai_lop2.py`.

    python3 tools/vuong_quoc_so_lop2.py --xem
    python3 tools/vuong_quoc_so_lop2.py
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

TEN_CHUONG = 'Vương quốc Số'
CHUONG = 1
CO_KHONG = ['có', 'không']
PHONG = ['phòng trăm', 'phòng chục', 'phòng đơn vị']


def bai(so, ten, dang_goc, m, cau):
    return _bai(so, ten, dang_goc, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng video: mục mở bài và khám phá để RỖNG, video thay cả hai."""
    return dung_muc('', [], muc_tieu, [], vidu, nham, bome)

# ═══ ① B01 · BA PHÒNG CỦA MỘT SỐ ═══
B01 = bai(
    1, 'BA PHÒNG CỦA MỘT SỐ — TRĂM, CHỤC, ĐƠN VỊ',
    'SỐ 1.1 — Cấu tạo số có ba chữ số: mỗi chữ số ngồi ở một phòng.',
    video(
        ['Biết số có ba chữ số ở trong một ngôi nhà ba phòng.',
         'Gọi đúng tên ba phòng: trăm, chục, đơn vị.',
         'Chỉ ra được chữ số nào đang ngồi ở phòng nào.'],
        ['Đề bài: Số 245 có mấy trăm, mấy chục, mấy đơn vị?',
         'Ngôi nhà ba phòng',
         'Số có ba chữ số ở trong một ngôi nhà ba phòng. Bên trái là phòng trăm, ở '
         'giữa là phòng chục, bên phải là phòng đơn vị.',
         'Xếp số 245 vào nhà',
         'Chữ số 2 ngồi phòng trăm. Chữ số 4 ngồi phòng chục. Chữ số 5 ngồi phòng '
         'đơn vị.',
         'Đáp số: 2 trăm, 4 chục, 5 đơn vị.',
         'Thử lại: đọc theo ba phòng thì được hai trăm bốn mươi lăm — đúng số ban đầu.'],
        ['Có bạn nhìn số 245 rồi bảo chữ số 2 ngồi ở phòng đơn vị.',
         'Gợi ý 1: Con chỉ tay vào chữ số đứng ngoài cùng bên phải xem là chữ số nào.',
         'Gợi ý 2: Phòng đơn vị luôn ở ngoài cùng bên phải, còn phòng trăm ở ngoài '
         'cùng bên trái.',
         'Chữa: chữ số 2 đứng ngoài cùng bên trái nên nó ngồi phòng trăm. Chữ số 5 '
         'mới là chữ số ngồi phòng đơn vị.'],
        ['Lấy ba cái cốc xếp thành hàng, dán nhãn trăm - chục - đơn vị, rồi cho con '
         'thả hạt đậu vào. Con nhìn thấy nhà số thật là nhớ ngay.',
         'Hỏi con một câu thôi mỗi lần: "Chữ số này đang ngồi phòng nào?"'],
    ),
    [
        lt(1, 1, 'Số 368 có mấy trăm, mấy chục, mấy đơn vị?',
           'Xếp vào nhà ba phòng: 3 trăm, 6 chục, 8 đơn vị.'),
        lt(2, 1, 'Trong số 245, chữ số nào ngồi ở phòng chục?',
           'Chữ số ở giữa là 4, nên chữ số 4 ngồi phòng chục.'),
        lt(3, 1, 'Phòng nào ở ngoài cùng bên trái của số có ba chữ số?',
           'Ngoài cùng bên trái là phòng trăm.'),
        lt(4, 2, 'Số 507 có mấy trăm, mấy chục, mấy đơn vị?',
           'Xếp vào nhà: 5 trăm, 0 chục, 7 đơn vị. Phòng chục đang trống.'),
        lt(5, 2, 'Số 90 có mấy chục, mấy đơn vị?',
           'Số 90 có 9 chục và 0 đơn vị.'),
        lt(6, 2, 'Viết số có 4 trăm, 1 chục, 6 đơn vị.',
           'Xếp lần lượt vào ba phòng được số 416.'),
        lt(7, 3, 'Viết số có 7 trăm, 0 chục, 3 đơn vị.',
           'Phòng chục trống vẫn phải viết chữ số 0 giữ chỗ, nên được số 703.'),
        lt(8, 3, 'Viết số có chữ số 8 ở phòng trăm, chữ số 0 ở phòng chục và chữ số 2 '
                 'ở phòng đơn vị.',
           'Xếp lần lượt vào ba phòng được số 802.'),
    ] + [
        q_tf(1, 'Số có ba chữ số thì phòng bên trái là phòng trăm.', True,
             'Đúng. Bên trái là trăm, ở giữa là chục, bên phải là đơn vị.'),
        q_tf(2, 'Trong số 245, chữ số 2 ngồi ở phòng đơn vị.', False,
             'Sai. Chữ số 2 ở ngoài cùng bên trái nên nó ngồi phòng trăm.'),
        q_mcq(3, 'Số 368 có mấy chục?', ['6', '3', '8', '68'], '6',
              'Chữ số ở giữa là 6 nên số ấy có 6 chục.'),
        q_mcq(4, 'Phòng ở ngoài cùng bên phải gọi là gì?', PHONG, 'phòng đơn vị',
              'Ngoài cùng bên phải luôn là phòng đơn vị.'),
        q_tf(5, 'Số 507 có 0 chục.', True,
             'Đúng. Phòng chục đang trống nên viết chữ số 0 giữ chỗ.'),
    ],
)

# ═══ ② B34 · MỖI CHỮ SỐ ĐÁNG BAO NHIÊU ═══
B34 = bai(
    34, 'MỖI CHỮ SỐ ĐÁNG BAO NHIÊU — TÁCH SỐ THÀNH TỔNG',
    'SỐ 1.1 — Giá trị của chữ số theo phòng; tách số thành tổng các phòng.',
    video(
        ['Biết mỗi chữ số đáng bao nhiêu là do phòng nó ngồi.',
         'Tách một số thành tổng của ba phòng.',
         'Biết phòng trống thì viết chữ số 0 giữ chỗ, và bỏ nó khỏi tổng.'],
        ['Đề bài: Trong số 245, mỗi chữ số đáng bao nhiêu? Tách số ấy thành tổng.',
         'Đáng bao nhiêu là do phòng',
         'Chữ số 2 ngồi phòng trăm nên nó đáng 200. Chữ số 4 ngồi phòng chục nên đáng '
         '40. Chữ số 5 ngồi phòng đơn vị nên đáng 5.',
         'Cùng là chữ số, ngồi phòng khác nhau thì đáng khác nhau.',
         'Tách thành tổng',
         'Mở cửa từng phòng rồi cộng lại: 200 + 40 + 5 = 245.',
         'Đáp số: 245 = 200 + 40 + 5.',
         'Khi có phòng trống',
         'Số 507 có phòng chục trống. Tách ra là 500 + 0 + 7, viết gọn thành 500 + 7.',
         'Nhưng khi VIẾT SỐ thì chữ số 0 vẫn phải có, nếu không thì còn lại 57 — số '
         'khác hẳn.'],
        ['Có bạn tách số 245 thành 2 + 4 + 5 rồi bảo bằng 11.',
         'Gợi ý 1: Con cộng 2 với 4 với 5 xem được bao nhiêu. Có ra lại số 245 không?',
         'Gợi ý 2: Chữ số 2 đang ngồi phòng nào, và ngồi phòng ấy thì nó đáng bao '
         'nhiêu?',
         'Chữa: tách số là tách theo cái mỗi chữ số ĐÁNG, không phải tách rời từng '
         'chữ số. Phải viết 200 + 40 + 5.'],
        ['Dùng tiền thật cho con xếp: tờ 200, tờ 40 thì lấy bốn tờ 10, rồi 5 đồng lẻ. '
         'Xếp xong là con thấy phép tách bằng mắt.',
         'Con hay quên chữ số 0 giữ chỗ. Bố mẹ thử che nó đi rồi hỏi "còn số mấy?" — '
         'con sẽ thấy ngay vì sao không bỏ được.'],
    ),
    [
        lt(1, 1, 'Trong số 245, chữ số 2 đáng bao nhiêu?',
           'Chữ số 2 ngồi phòng trăm nên nó đáng 200.'),
        lt(2, 1, 'Trong số 245, chữ số 4 đáng bao nhiêu?',
           'Chữ số 4 ngồi phòng chục nên nó đáng 40.'),
        lt(3, 1, 'Trong số 245, chữ số 5 đáng bao nhiêu?',
           'Chữ số 5 ngồi phòng đơn vị nên nó đáng 5.'),
        lt(4, 2, 'Tách số 245 thành tổng của ba phòng.',
           'Mở cửa từng phòng: 200 + 40 + 5.'),
        lt(5, 2, 'Tách số 368 thành tổng của ba phòng.',
           'Mở cửa từng phòng: 300 + 60 + 8.'),
        lt(6, 2, 'Trong số 507, chữ số 5 đáng bao nhiêu và chữ số 7 đáng bao nhiêu?',
           'Chữ số 5 ngồi phòng trăm nên đáng 500; chữ số 7 ngồi phòng đơn vị nên '
           'đáng 7.'),
        lt(7, 3, 'Số nào tách ra được 600 + 20 + 9?',
           'Ghép ba phòng lại được số 629.'),
        lt(8, 3, 'Trong số 444, ba chữ số 4 lần lượt đáng bao nhiêu?',
           'Từ trái sang: 400, rồi 40, rồi 4. Cùng chữ số mà ngồi khác phòng thì đáng '
           'khác nhau.'),
    ] + [
        q_tf(1, 'Chữ số 2 trong số 245 đáng 200.', True,
             'Đúng, vì nó đang ngồi phòng trăm.'),
        q_tf(2, 'Tách số 245 thành tổng là viết 2 cộng 4 cộng 5.', False,
             'Sai. Phải tách theo cái mỗi chữ số đáng: 200 + 40 + 5.'),
        q_mcq(3, 'Chữ số 6 trong số 368 đáng bao nhiêu?', ['60', '6', '600', '68'],
              '60', 'Chữ số 6 ngồi phòng chục nên đáng 60.'),
        q_mcq(4, 'Số 507 tách thành tổng là',
              ['500 + 7', '5 + 0 + 7', '50 + 7'], '500 + 7',
              'Phòng chục trống nên không có số hạng cho nó.'),
        q_tf(5, 'Cùng một chữ số mà ngồi phòng khác nhau thì đáng khác nhau.', True,
             'Đúng. Trong số 444, ba chữ số 4 đáng 400, 40 và 4.'),
    ],
)

# ═══ ③ B35 · SO HAI SỐ ═══
B35 = bai(
    35, 'SO HAI SỐ — SO PHÒNG BÊN TRÁI TRƯỚC',
    'SỐ 1.1 — So sánh hai số bằng cách so từng phòng từ trái sang phải.',
    video(
        ['So hai số bằng cách so phòng trăm trước.',
         'Biết hoà phòng trăm thì so tiếp phòng chục, rồi phòng đơn vị.',
         'Biết phòng bên trái luôn quyền lực hơn các phòng sau.'],
        ['Đề bài: So sánh 245 với 198. Số nào lớn hơn?',
         'So phòng bên trái trước',
         'Phòng trăm của 245 có chữ số 2. Phòng trăm của 198 có chữ số 1.',
         'Hai lớn hơn một, nên 245 lớn hơn 198.',
         'Không cần nhìn hai phòng sau nữa — phòng trăm đã phân thắng bại.',
         'Đáp số: 245 lớn hơn 198.',
         'Khi phòng trăm hoà nhau',
         'So 245 với 254 thì phòng trăm đều là 2, hoà. Nhìn tiếp phòng chục: 4 với 5. '
         'Năm lớn hơn bốn nên 254 lớn hơn.',
         'Hoà tiếp thì mới nhìn phòng đơn vị.'],
        ['Có bạn so 88 với 100 rồi bảo 88 lớn hơn, vì trong 88 có hai chữ số 8 to.',
         'Gợi ý 1: Con đếm xem mỗi số có mấy chữ số. Số nào dài hơn?',
         'Gợi ý 2: Số 100 có chữ số ở phòng trăm, còn số 88 thì phòng trăm trống '
         'không.',
         'Chữa: so số thì so phòng chứ không so chữ số nào to. Số 100 có 1 trăm, số '
         '88 không có trăm nào, nên 100 lớn hơn.'],
        ['Cho con so giá hai món đồ trong siêu thị. Bảo con chỉ tay vào phòng trăm '
         'của cả hai trước khi nói số nào đắt hơn.',
         'Mẹo nhắc con: "Phòng bên trái nói trước." Chỉ khi hai phòng bên trái bằng '
         'nhau thì mới được hỏi phòng tiếp theo.'],
    ),
    [
        lt(1, 1, 'So sánh 245 với 198. Số nào lớn hơn?',
           'Phòng trăm của 245 là 2, của 198 là 1. Hai lớn hơn một nên 245 lớn hơn.'),
        lt(2, 1, 'Phòng trăm của 245 có chữ số mấy, phòng trăm của 198 có chữ số mấy?',
           'Số 245 có 2 ở phòng trăm; số 198 có 1 ở phòng trăm.'),
        lt(3, 1, 'So sánh 368 với 372. Số nào lớn hơn?',
           'Phòng trăm hoà nhau đều là 3. Nhìn phòng chục: 7 lớn hơn 6 nên 372 lớn '
           'hơn.'),
        lt(4, 2, 'So sánh 245 với 254. Số nào lớn hơn?',
           'Phòng trăm hoà. Phòng chục: 5 lớn hơn 4 nên 254 lớn hơn.'),
        lt(5, 2, 'So sánh 507 với 570. Số nào lớn hơn?',
           'Phòng trăm hoà đều là 5. Phòng chục: 7 lớn hơn 0 nên 570 lớn hơn.'),
        lt(6, 2, 'So sánh 88 với 100. Số nào lớn hơn?',
           'Số 100 có 1 trăm, số 88 không có trăm nào, nên 100 lớn hơn.'),
        lt(7, 3, 'Xếp ba số 245, 254 và 198 từ bé đến lớn.',
           'Bé nhất là 198 vì chỉ có 1 trăm. Rồi tới 245, và lớn nhất là 254.'),
        lt(8, 3, 'Hai số cùng có chữ số 3 ở phòng trăm và chữ số 6 ở phòng chục. Muốn '
                 'biết số nào lớn hơn thì phải so phòng nào?',
           'Hai phòng đầu đã hoà nên phải so phòng đơn vị.'),
    ] + [
        q_tf(1, 'So hai số thì so phòng bên trái trước.', True,
             'Đúng. Phòng bên trái luôn quyền lực hơn.'),
        q_tf(2, 'Số 88 lớn hơn số 100 vì trong 88 có hai chữ số 8 to.', False,
             'Sai. So số thì so phòng: 100 có 1 trăm còn 88 không có trăm nào.'),
        q_mcq(3, 'So 245 với 254 thì phải nhìn phòng nào để phân thắng bại?',
              PHONG, 'phòng chục',
              'Phòng trăm hoà nhau nên phải nhìn tiếp phòng chục.'),
        q_mcq(4, 'Trong ba số 198, 245, 254 thì số nào bé nhất?',
              ['198', '245', '254'], '198',
              'Số 198 chỉ có 1 trăm, ít nhất trong ba số.'),
        q_tf(5, 'Nếu phòng trăm đã phân thắng bại thì không cần nhìn hai phòng sau.',
             True, 'Đúng. Các phòng sau không cứu lại được.'),
    ],
)

# ═══ ④ B02 · THÊM SỐ 0 VÀO BÊN PHẢI ═══
B02 = bai(
    2, 'THÊM SỐ 0 VÀO BÊN PHẢI — TO GẤP MƯỜI',
    'SỐ 1.2 — Thêm chữ số 0 vào bên phải: mọi chữ số dọn sang phòng bên trái.',
    video(
        ['Biết thêm chữ số 0 vào bên phải thì số to gấp mười lần.',
         'Nói được vì sao: mọi chữ số dọn sang phòng bên trái một bậc.',
         'Thêm được chữ số 0 cho số có một và hai chữ số.'],
        ['Đề bài: Thêm chữ số 0 vào bên phải số 3 thì được số nào, và số mới to gấp '
         'mấy lần số cũ?',
         'Thêm vào thì được số nào',
         'Viết số 3 rồi đặt chữ số 0 vào ngay sau, được số 30.',
         'Vì sao to gấp mười',
         'Chữ số 0 chen vào phòng đơn vị, nên chữ số 3 bị đẩy sang phòng chục.',
         'Ở phòng đơn vị thì 3 chỉ đáng ba hạt. Sang phòng chục thì 3 đáng ba thanh '
         'chục, tức ba mươi hạt.',
         'Đáp số: được số 30, và nó to gấp 10 lần số 3.',
         'Số nào cũng thế',
         'Số 25 thêm chữ số 0 thành 250. Số 60 thêm chữ số 0 thành 600.',
         'Cả số dọn nhà sang trái một phòng, nên lần nào cũng to gấp mười.'],
        ['Có bạn thêm chữ số 0 vào bên phải số 3 rồi bảo số mới hơn số cũ đúng 3 đơn '
         'vị, vì chỉ thêm có một chữ số 0.',
         'Gợi ý 1: Con đếm xem từ 3 tới 30 phải đi qua bao nhiêu số.',
         'Gợi ý 2: Chữ số 3 lúc đầu ngồi phòng nào, sau khi thêm thì nó ngồi phòng '
         'nào?',
         'Chữa: chữ số 0 tuy không đáng gì, nhưng nó ĐẨY chữ số 3 sang phòng bên '
         'trái. Số mới to gấp mười chứ không chỉ hơn vài đơn vị.'],
        ['Lấy que tính cho con làm thật: 3 que rời, rồi 3 bó mười que. Con cầm tay là '
         'thấy ngay ba mươi khác ba thế nào.',
         'Hỏi con: "Chữ số 3 vừa dọn sang phòng nào?" Trả lời được câu ấy là con hiểu '
         'cả bài.'],
    ),
    [
        lt(1, 1, 'Thêm chữ số 0 vào bên phải số 7 thì được số nào?',
           'Viết 7 rồi đặt chữ số 0 vào sau, được số 70.'),
        lt(2, 1, 'Thêm chữ số 0 vào bên phải số 25 thì được số nào?',
           'Viết 25 rồi đặt chữ số 0 vào sau, được số 250.'),
        lt(3, 1, 'Số 70 to gấp mấy lần số 7?',
           'Cả số dọn sang trái một phòng nên to gấp 10 lần.'),
        lt(4, 2, 'Thêm chữ số 0 vào bên phải số 12 thì được số nào?',
           'Được số 120, tức là 12 chục.'),
        lt(5, 2, 'Số 3 thêm chữ số 0 thành 30. Chữ số 3 dọn từ phòng nào sang phòng '
                 'nào?',
           'Nó dọn từ phòng đơn vị sang phòng chục.'),
        lt(6, 2, 'Thêm chữ số 0 vào bên phải số 60 thì được số nào?',
           'Được số 600.'),
        lt(7, 3, 'Số nào thêm chữ số 0 vào bên phải thì được 450?',
           'Bỏ chữ số 0 ở cuối ra thì còn số 45.'),
        lt(8, 3, 'Thêm chữ số 0 vào bên phải số 9, rồi thêm tiếp một chữ số 0 nữa thì '
                 'được số nào?',
           'Lần đầu được 90, lần sau được 900.'),
    ] + [
        q_tf(1, 'Thêm chữ số 0 vào bên phải thì số to gấp mười lần.', True,
             'Đúng, vì mọi chữ số dọn sang phòng bên trái một bậc.'),
        q_tf(2, 'Thêm chữ số 0 vào bên phải số 3 thì số mới chỉ hơn số cũ 3 đơn vị.',
             False, 'Sai. Được số 30, to gấp mười lần chứ không hơn vài đơn vị.'),
        q_mcq(3, 'Thêm chữ số 0 vào bên phải số 25 thì được', ['250', '205', '26', '2500'],
              '250', 'Chữ số 0 vào phòng đơn vị, hai chữ số cũ dọn sang trái.'),
        q_mcq(4, 'Số 3 thêm chữ số 0 thì chữ số 3 dọn sang phòng nào?',
              PHONG, 'phòng chục',
              'Nó rời phòng đơn vị và sang phòng chục.'),
        q_tf(5, 'Chữ số 0 không đáng gì nên thêm vào thì số không đổi.', False,
             'Sai. Nó không đáng gì nhưng nó đẩy các chữ số kia sang trái.'),
    ],
)

# ═══ ⑤ B36 · XOÁ SỐ 0 TẬN CÙNG ═══
B36 = bai(
    36, 'XOÁ SỐ 0 TẬN CÙNG — NHỎ ĐI MƯỜI LẦN',
    'SỐ 1.3 — Xoá chữ số 0 ở tận cùng: chiều ngược của phép thêm; chỉ làm được khi '
    'chữ số cuối đúng là 0.',
    video(
        ['Biết xoá chữ số 0 tận cùng thì số nhỏ đi mười lần.',
         'Biết đó là chiều ngược của bài hôm trước.',
         'Biết chỉ xoá được khi chữ số cuối đúng là 0.'],
        ['Đề bài: Xoá chữ số 0 ở tận cùng số 70 thì còn số nào, và số ấy nhỏ đi mấy '
         'lần?',
         'Hai chiều ngược nhau',
         'Bài trước là thêm chữ số 0 để số to gấp mười. Nay làm ngược lại.',
         'Xoá chữ số 0 ở cuối số 70 thì còn số 7.',
         'Vì sao nhỏ đi mười lần',
         'Chữ số 7 đang ngồi phòng chục, mất chỗ dựa thì nó tụt về phòng đơn vị.',
         'Ở phòng chục nó đáng bảy chục; về phòng đơn vị chỉ còn đáng bảy hạt.',
         'Đáp số: còn số 7, và nó nhỏ đi 10 lần.',
         'Chỉ xoá được khi cuối là chữ số 0',
         'Số 250 xoá được, còn 25. Nhưng số 405 thì không xoá kiểu ấy được, vì chữ số '
         'cuối của nó là 5 chứ không phải 0.'],
        ['Có bạn thấy số 405 có chữ số 0 nên xoá luôn chữ số 0 ở giữa, còn 45.',
         'Gợi ý 1: Con nhìn chữ số ở tận cùng của số 405 xem là chữ số nào.',
         'Gợi ý 2: Phép xoá này chỉ làm được với chữ số 0 đứng ở chỗ nào?',
         'Chữa: chữ số 0 của 405 nằm ở giữa, không phải ở tận cùng. Xoá nó đi là chữ '
         'số 4 tụt phòng và số đổi hẳn, không còn nhỏ đi mười lần nữa.'],
        ['Cho con đổi tiền: một tờ 50 nghìn đổi thành mấy tờ 5 nghìn. Đổi đi đổi lại '
         'là con quen hai chiều.',
         'Con hay xoá nhầm chữ số 0 ở giữa. Bố mẹ chỉ cần hỏi: "Chữ số cuối cùng là '
         'chữ số mấy?"'],
    ),
    [
        lt(1, 1, 'Xoá chữ số 0 ở tận cùng số 70 thì còn số nào?',
           'Bỏ chữ số 0 ở cuối, còn số 7.'),
        lt(2, 1, 'Xoá chữ số 0 ở tận cùng số 250 thì còn số nào?',
           'Bỏ chữ số 0 ở cuối, còn số 25.'),
        lt(3, 1, 'Số 25 nhỏ hơn số 250 mấy lần?',
           'Cả số tụt về bên phải một phòng nên nhỏ đi 10 lần.'),
        lt(4, 2, 'Xoá chữ số 0 ở tận cùng số 600 thì còn số nào?',
           'Bỏ một chữ số 0 ở cuối, còn số 60.'),
        lt(5, 2, 'Số 405 có xoá chữ số 0 theo cách này được không?',
           'Không. Chữ số 0 của nó nằm ở giữa chứ không ở tận cùng, và chữ số cuối là '
           '5.'),
        lt(6, 2, 'Xoá chữ số 0 ở tận cùng số 120 thì còn số nào?',
           'Bỏ chữ số 0 ở cuối, còn số 12.'),
        lt(7, 3, 'Số nào xoá chữ số 0 ở tận cùng thì còn 45?',
           'Làm ngược lại là thêm chữ số 0 vào, được số 450.'),
        lt(8, 3, 'Xoá chữ số 0 ở tận cùng số 900 hai lần liền thì còn số nào?',
           'Lần đầu còn 90, lần sau còn 9.'),
    ] + [
        q_tf(1, 'Xoá chữ số 0 ở tận cùng thì số nhỏ đi mười lần.', True,
             'Đúng, vì mọi chữ số tụt về bên phải một phòng.'),
        q_tf(2, 'Số nào có chữ số 0 thì cũng xoá được theo cách này.', False,
             'Sai. Chỉ xoá được khi chữ số 0 đứng ở tận cùng.'),
        q_mcq(3, 'Xoá chữ số 0 ở tận cùng số 250 thì còn', ['25', '20', '50', '5'],
              '25', 'Bỏ chữ số 0 ở cuối, hai chữ số còn lại tụt về một phòng.'),
        q_mcq(4, 'Số 405 xoá chữ số 0 ở giữa thì',
              ['số đổi hẳn, không còn nhỏ đi mười lần', 'số nhỏ đi mười lần',
               'số không đổi'],
              'số đổi hẳn, không còn nhỏ đi mười lần',
              'Chữ số 0 ấy không ở tận cùng nên phép này không dùng được.'),
        q_tf(5, 'Thêm chữ số 0 và xoá chữ số 0 là hai chiều ngược nhau.', True,
             'Đúng. Một chiều to gấp mười, chiều kia nhỏ đi mười lần.'),
    ],
)

# ═══ ⑥ B03 · ĐỔI CHỖ HAI CHỮ SỐ ═══
B03 = bai(
    3, 'ĐỔI CHỖ HAI CHỮ SỐ — SỐ NÀO LỚN HƠN',
    'SỐ 1.4 — Đổi chỗ hai chữ số của số có hai chữ số; số nào có thẻ to ở phòng chục '
    'thì lớn hơn.',
    video(
        ['Đổi chỗ hai chữ số của một số có hai chữ số.',
         'Biết số nào có chữ số to hơn ở phòng chục thì lớn hơn.',
         'Biết chữ số 0 không được lên đứng đầu.'],
        ['Đề bài: Đổi chỗ hai chữ số của số 25 thì được số nào, và số nào lớn hơn?',
         'Đổi chỗ là đổi phòng ở',
         'Trong số 25, chữ số 2 ngồi phòng chục nên đáng 20. Chữ số 5 ngồi phòng đơn '
         'vị nên đáng 5.',
         'Đổi chỗ hai thẻ thì được số 52. Nay chữ số 5 chiếm phòng chục, đáng 50.',
         'Số nào lớn hơn',
         'Phòng chục quyền lực hơn, mà thẻ to hơn đang ở phòng chục của 52.',
         'Đáp số: được số 52, và 52 lớn hơn 25.',
         'Có một chỗ phải cẩn thận',
         'Số 50 đổi chỗ thì chữ số 0 lên đứng đầu. Nhưng chữ số 0 không được đứng đầu '
         'nên số ấy không còn là số có hai chữ số nữa.'],
        ['Có bạn đổi chỗ hai chữ số của 25 rồi bảo hai số bằng nhau, vì vẫn là hai '
         'chữ số ấy chứ có mất đi đâu.',
         'Gợi ý 1: Con thử đếm xem 25 và 52 cách nhau bao nhiêu.',
         'Gợi ý 2: Thẻ số 5 lúc ở phòng đơn vị thì đáng mấy, lúc lên phòng chục thì '
         'đáng mấy?',
         'Chữa: hai thẻ vẫn thế nhưng chúng đổi phòng, mà phòng khác nhau thì đáng '
         'khác nhau. Nên hai số khác hẳn.'],
        ['Viết hai chữ số lên hai mẩu giấy rồi cho con tráo qua tráo lại, mỗi lần đọc '
         'to số vừa được.',
         'Trò hay: bố mẹ đọc một số, con phải nói ngay số đổi chỗ và số nào lớn hơn.'],
    ),
    [
        lt(1, 1, 'Đổi chỗ hai chữ số của số 25 thì được số nào?',
           'Hai thẻ đổi phòng cho nhau, được số 52.'),
        lt(2, 1, 'Trong hai số 25 và 52, số nào lớn hơn?',
           'Số 52 lớn hơn, vì thẻ to hơn đang ở phòng chục của nó.'),
        lt(3, 1, 'Trong số 52, chữ số nào đang ngồi phòng chục?',
           'Chữ số 5 ngồi phòng chục nên nó đáng 50.'),
        lt(4, 2, 'Đổi chỗ hai chữ số của số 14 thì được số nào?',
           'Được số 41.'),
        lt(5, 2, 'Đổi chỗ hai chữ số của số 27 thì được số nào?',
           'Được số 72.'),
        lt(6, 2, 'Đổi chỗ hai chữ số của số 50 thì chữ số 0 lên đứng đầu. Số ấy còn là '
                 'số có hai chữ số không?',
           'Không. Chữ số 0 không được đứng đầu, nên số ấy chỉ còn là số 5.'),
        lt(7, 3, 'Trong hai số 38 và 83, số nào lớn hơn?',
           'Số 83 lớn hơn, vì thẻ 8 đang ở phòng chục của nó.'),
        lt(8, 3, 'Số 46 đổi chỗ hai chữ số được số nào, và số mới lớn hơn hay bé hơn '
                 'số cũ?',
           'Được số 64. Thẻ 6 lên phòng chục nên số mới lớn hơn số cũ.'),
    ] + [
        q_tf(1, 'Đổi chỗ hai chữ số thì hai số vẫn bằng nhau.', False,
             'Sai. Hai thẻ đổi phòng, mà phòng khác nhau thì đáng khác nhau.'),
        q_tf(2, 'Số nào có chữ số to hơn ở phòng chục thì lớn hơn.', True,
             'Đúng. Phòng chục quyền lực hơn phòng đơn vị.'),
        q_mcq(3, 'Đổi chỗ hai chữ số của số 27 thì được', ['72', '27', '270', '7'],
              '72', 'Hai thẻ đổi phòng cho nhau.'),
        q_mcq(4, 'Đổi chỗ hai chữ số của số 50 thì',
              ['chữ số 0 lên đầu nên không còn là số có hai chữ số',
               'được số 05 lớn hơn 50', 'số không đổi'],
              'chữ số 0 lên đầu nên không còn là số có hai chữ số',
              'Chữ số 0 không được đứng đầu.'),
        q_tf(5, 'Trong hai số 38 và 83 thì 83 lớn hơn.', True,
             'Đúng, vì thẻ 8 đang ở phòng chục của 83.'),
    ],
)

# ═══ ⑦ B37 · HIỆU HAI SỐ ĐỔI CHỖ ═══
B37 = bai(
    37, 'HIỆU HAI SỐ ĐỔI CHỖ — TOÀN SỐ TRONG BẢNG NHÂN 9',
    'SỐ 1.4 — Hiệu của một số và số đổi chỗ luôn nằm trong bảng nhân 9.',
    video(
        ['Tính được hiệu của một số và số đổi chỗ của nó.',
         'Nhận ra mọi hiệu ấy đều nằm trong bảng nhân 9.',
         'Đoán trước hiệu bằng cách lấy hiệu hai chữ số nhân 9.'],
        ['Đề bài: Tính 52 trừ 25. Rồi thử vài cặp khác xem có gì lạ.',
         'Tính cặp đầu tiên',
         'Năm mươi hai trừ hai mươi lăm bằng hai mươi bảy.',
         'Thử thêm vài cặp',
         'Ba mươi mốt trừ mười ba bằng mười tám. Bốn mươi hai trừ hai mươi bốn cũng '
         'bằng mười tám. Năm mươi mốt trừ mười lăm bằng ba mươi sáu.',
         'Nhìn ra điều lạ',
         'Mười tám, hai mươi bảy, ba mươi sáu — toàn là số trong bảng nhân chín.',
         'Đoán trước được luôn',
         'Lấy hiệu hai chữ số rồi nhân chín. Số 52 có hiệu hai chữ số là ba, mà ba '
         'nhân chín bằng hai mươi bảy — đúng đáp số vừa tính.',
         'Đáp số: 52 − 25 = 27, và mọi hiệu như thế đều trong bảng nhân 9.'],
        ['Có bạn tính 42 trừ 24 rồi ghi 22, vì lấy 4 trừ 2 rồi lấy 2 trừ 4.',
         'Gợi ý 1: Trừ số có hai chữ số thì phải đặt tính cho thẳng cột rồi trừ, '
         'không trừ rời từng chữ số.',
         'Gợi ý 2: Hàng đơn vị 2 không trừ được 4 thì phải mượn của hàng chục.',
         'Chữa: đặt tính rồi trừ có nhớ, được 18. Và 18 nằm trong bảng nhân chín, '
         'đúng như luật.'],
        ['Cho con thử năm sáu cặp rồi ghi các đáp số ra một cột. Con tự nhìn ra bảng '
         'nhân chín là thích lắm.',
         'Đây là bài đầu tiên con gặp một LUẬT do chính mình tìm ra. Bố mẹ đừng nói '
         'trước đáp án, để con thử đủ vài cặp đã.'],
    ),
    [
        lt(1, 1, 'Tính 52 − 25.', 'Đặt tính rồi trừ: 52 − 25 = 27.'),
        lt(2, 1, 'Tính 31 − 13.', 'Đặt tính rồi trừ: 31 − 13 = 18.'),
        lt(3, 1, 'Hai số 27 và 18 nằm trong bảng nhân mấy?',
           'Cả hai đều trong bảng nhân 9.'),
        lt(4, 2, 'Tính 42 − 24.', 'Đặt tính rồi trừ: 42 − 24 = 18.'),
        lt(5, 2, 'Tính 51 − 15.', 'Đặt tính rồi trừ: 51 − 15 = 36.'),
        lt(6, 2, 'Tính 93 − 39.', 'Đặt tính rồi trừ: 93 − 39 = 54.'),
        lt(7, 3, 'Hiệu hai chữ số của số 52 bằng mấy, và 27 gấp mấy lần số ấy?',
           'Hiệu hai chữ số: 5 − 2 = 3. Mà 27 : 3 = 9 nên gấp 9 lần.'),
        lt(8, 3, 'Số 71 đổi chỗ được 17. Hãy đoán trước hiệu bằng cách lấy hiệu hai '
                 'chữ số nhân 9, rồi tính để kiểm.',
           'Hiệu hai chữ số là 6, mà 6 × 9 = 54. Tính thật: 71 − 17 = 54 — khớp.'),
    ] + [
        q_tf(1, 'Hiệu của một số và số đổi chỗ luôn nằm trong bảng nhân 9.', True,
             'Đúng. Thử bao nhiêu cặp cũng thấy thế.'),
        q_tf(2, 'Trừ hai số có hai chữ số thì trừ rời từng chữ số cho nhanh.', False,
             'Sai. Phải đặt tính thẳng cột rồi trừ, có khi phải mượn.'),
        q_mcq(3, 'Tính 52 − 25.', ['27', '37', '33', '22'], '27',
              'Đặt tính rồi trừ có mượn.'),
        q_mcq(4, 'Số 51 đổi chỗ được 15. Hiệu hai số ấy là',
              ['36', '46', '44', '4'], '36',
              'Hiệu hai chữ số là 4, mà 4 nhân 9 bằng 36.'),
        q_tf(5, 'Muốn đoán trước hiệu thì lấy hiệu hai chữ số nhân với 9.', True,
             'Đúng, và tính lại bao giờ cũng khớp.'),
    ],
)

# ═══ ⑧ B04 · XẾP THẺ ĐỂ ĐƯỢC SỐ LỚN NHẤT VÀ BÉ NHẤT ═══
B04 = bai(
    4, 'XẾP THẺ ĐỂ ĐƯỢC SỐ LỚN NHẤT VÀ BÉ NHẤT',
    'SỐ 3.1 — Lập số lớn nhất và bé nhất từ các thẻ số cho trước.',
    video(
        ['Xếp thẻ để được số lớn nhất: thẻ to nhất vào phòng bên trái.',
         'Xếp thẻ để được số bé nhất: làm ngược lại.',
         'Nói được vì sao phòng bên trái quyết định.'],
        ['Đề bài: Có ba thẻ số 8, 5 và 2. Hãy lập số lớn nhất và số bé nhất có ba chữ '
         'số.',
         'Nhớ lại bài đầu chương',
         'Phòng bên trái quyền lực nhất. Muốn số lớn thì phải làm cho phòng trăm to '
         'nhất đã.',
         'Số lớn nhất',
         'Xếp từ to đến bé: thẻ 8 vào phòng trăm, thẻ 5 vào phòng chục, thẻ 2 vào '
         'phòng đơn vị. Được số 852.',
         'Số bé nhất',
         'Làm ngược lại, xếp từ bé đến to: được số 258.',
         'Đáp số: số lớn nhất là 852, số bé nhất là 258.',
         'Thử lại',
         'Đổi thử hai thẻ bất kỳ xem có ra số lớn hơn 852 không. Không có, vì thẻ to '
         'nhất đã nằm ở phòng quyền lực nhất rồi.'],
        ['Có bạn lập số lớn nhất từ ba thẻ 8, 5, 2 rồi viết 825, vì thấy 25 nghe to '
         'hơn 52.',
         'Gợi ý 1: Con so hai số 852 và 825 xem số nào lớn hơn.',
         'Gợi ý 2: Hai số ấy cùng phòng trăm, nên phải nhìn tiếp phòng chục. Phòng '
         'chục nào có thẻ to hơn?',
         'Chữa: sau khi đặt thẻ to nhất vào phòng trăm thì phải đặt thẻ to NHÌ vào '
         'phòng chục. Số đúng là 852.'],
        ['Cắt ba mẩu giấy viết ba chữ số rồi cho con xếp thật. Xếp xong đọc to lên, '
         'rồi thử đổi chỗ xem có ra số lớn hơn không.',
         'Bí quyết chỉ một câu: "Thẻ to nhất đi vào phòng bên trái nhất."'],
    ),
    [
        lt(1, 1, 'Từ hai thẻ 3 và 8, lập số lớn nhất có hai chữ số.',
           'Thẻ to hơn vào phòng chục, được số 83.'),
        lt(2, 1, 'Từ hai thẻ 3 và 8, lập số bé nhất có hai chữ số.',
           'Thẻ bé hơn vào phòng chục, được số 38.'),
        lt(3, 1, 'Từ ba thẻ 8, 5, 2, lập số lớn nhất có ba chữ số.',
           'Xếp từ to đến bé, được số 852.'),
        lt(4, 2, 'Từ ba thẻ 8, 5, 2, lập số bé nhất có ba chữ số.',
           'Xếp từ bé đến to, được số 258.'),
        lt(5, 2, 'Muốn được số lớn nhất thì thẻ to nhất phải đặt vào phòng nào?',
           'Vào phòng trăm, vì phòng bên trái quyền lực nhất.'),
        lt(6, 2, 'Từ ba thẻ 4, 7, 1, lập số lớn nhất và số bé nhất.',
           'Số lớn nhất là 741, số bé nhất là 147.'),
        lt(7, 3, 'Từ ba thẻ 9, 3, 6: lập số lớn nhất, số bé nhất, rồi tính hiệu hai số '
                 'ấy.',
           'Số lớn nhất 963, số bé nhất 369. Hiệu: 963 − 369 = 594.'),
        lt(8, 3, 'Từ hai thẻ 6 và 6 thì lập được mấy số có hai chữ số khác nhau?',
           'Hai thẻ giống hệt nhau nên đổi chỗ vẫn ra số 66. Chỉ lập được 1 số.'),
    ] + [
        q_tf(1, 'Muốn số lớn nhất thì đặt thẻ to nhất vào phòng bên trái.', True,
             'Đúng, vì phòng bên trái quyền lực nhất.'),
        q_tf(2, 'Từ ba thẻ 8, 5, 2 thì số lớn nhất là 825.', False,
             'Sai. Sau thẻ to nhất phải tới thẻ to nhì, nên số đúng là 852.'),
        q_mcq(3, 'Từ ba thẻ 4, 7, 1 thì số bé nhất là', ['147', '174', '417', '741'],
              '147', 'Xếp từ bé đến to.'),
        q_mcq(4, 'Muốn số bé nhất thì xếp thẻ thế nào?',
              ['từ bé đến to', 'từ to đến bé', 'xếp lộn xộn cũng được'],
              'từ bé đến to', 'Ngược hẳn với cách lập số lớn nhất.'),
        q_tf(5, 'Từ hai thẻ giống hệt nhau thì chỉ lập được một số.', True,
             'Đúng, vì đổi chỗ hai thẻ ấy vẫn ra số cũ.'),
    ],
)

# ═══ ⑨ B38 · KHI CÓ THẺ SỐ 0 ═══
B38 = bai(
    38, 'KHI CÓ THẺ SỐ 0 — SỐ 0 KHÔNG ĐỨNG ĐẦU',
    'SỐ 3.1 — Lập số bé nhất khi trong tay có thẻ số 0.',
    video(
        ['Biết chữ số 0 không được đứng ở phòng bên trái nhất.',
         'Lập được số bé nhất khi có thẻ số 0: thẻ bé nhất khác 0 đứng đầu.',
         'Biết thẻ 0 vẫn đứng được ở các phòng còn lại.'],
        ['Đề bài: Có ba thẻ số 0, 3 và 7. Hãy lập số bé nhất có ba chữ số.',
         'Làm như bài trước thì sao',
         'Xếp từ bé đến to được không, ba, bảy. Nhưng khoan đã.',
         'Số ấy viết ra là 037 — mà chữ số 0 đứng đầu thì nó chẳng làm nên trăm nào, '
         'số chỉ còn là 37 có hai chữ số.',
         'Luật của thẻ số 0',
         'Chữ số 0 không được đứng ở phòng bên trái nhất. Nhưng các phòng còn lại thì '
         'nó vẫn ngồi được.',
         'Xếp lại cho đúng',
         'Cho thẻ bé nhất KHÁC 0 đứng đầu, tức thẻ 3. Rồi thẻ 0 ngồi ngay phòng thứ '
         'hai. Còn thẻ 7 xuống cuối.',
         'Đáp số: số bé nhất là 307.',
         'Còn số lớn nhất thì không vướng gì, vẫn xếp từ to đến bé: 730.'],
        ['Có bạn lập số bé nhất từ ba thẻ 0, 3, 7 rồi viết 037.',
         'Gợi ý 1: Con đếm xem số 037 có mấy chữ số thật sự.',
         'Gợi ý 2: Chữ số 0 đứng ở phòng trăm thì số ấy có mấy trăm?',
         'Chữa: chữ số 0 ở phòng trăm nghĩa là không có trăm nào, nên số ấy chỉ là 37. '
         'Muốn đủ ba chữ số thì cho thẻ 3 đứng đầu, được 307.'],
        ['Cho con xếp thẻ có số 0 thật. Xếp xong bảo con đọc to — đọc "không trăm ba '
         'mươi bảy" là con tự thấy nó vô lý.',
         'Câu nhắc: "Số 0 nhút nhát, không dám đứng đầu hàng." Nhưng nó vẫn đứng giữa '
         'được bình thường.'],
    ),
    [
        lt(1, 1, 'Từ ba thẻ 0, 3, 7, lập số lớn nhất có ba chữ số.',
           'Xếp từ to đến bé, được số 730.'),
        lt(2, 1, 'Xếp từ bé đến to được 0, 3, 7. Số 037 có phải số có ba chữ số không?',
           'Không. Chữ số 0 đứng đầu thì không có trăm nào, số ấy chỉ là 37.'),
        lt(3, 1, 'Vậy từ ba thẻ 0, 3, 7 thì số bé nhất có ba chữ số là số nào?',
           'Cho thẻ bé nhất khác 0 đứng đầu, được số 307.'),
        lt(4, 2, 'Từ ba thẻ 0, 5, 9, lập số bé nhất có ba chữ số.',
           'Thẻ 5 đứng đầu, thẻ 0 vào phòng chục, được số 509.'),
        lt(5, 2, 'Từ ba thẻ 0, 5, 9, lập số lớn nhất có ba chữ số.',
           'Xếp từ to đến bé, được số 950.'),
        lt(6, 2, 'Thẻ số 0 không được đứng ở phòng nào?',
           'Không được đứng ở phòng trăm, tức phòng bên trái nhất.'),
        lt(7, 3, 'Từ ba thẻ 0, 2, 8: lập số lớn nhất, số bé nhất, rồi tính hiệu.',
           'Số lớn nhất 820, số bé nhất 208. Hiệu: 820 − 208 = 612.'),
        lt(8, 3, 'Từ hai thẻ 0 và 6, lập được số có hai chữ số nào?',
           'Thẻ 0 không đứng đầu được, nên chỉ lập được số 60.'),
    ] + [
        q_tf(1, 'Chữ số 0 không được đứng ở phòng bên trái nhất.', True,
             'Đúng. Đứng đó thì số bị mất một chữ số.'),
        q_tf(2, 'Từ ba thẻ 0, 3, 7 thì số bé nhất có ba chữ số là 037.', False,
             'Sai. Số ấy chỉ là 37. Số bé nhất đúng là 307.'),
        q_mcq(3, 'Từ ba thẻ 0, 5, 9 thì số bé nhất có ba chữ số là',
              ['509', '059', '905', '950'], '509',
              'Thẻ bé nhất khác 0 đứng đầu, rồi mới tới thẻ 0.'),
        q_mcq(4, 'Thẻ số 0 đứng được ở phòng nào?',
              ['phòng chục và phòng đơn vị', 'chỉ phòng trăm', 'không phòng nào'],
              'phòng chục và phòng đơn vị',
              'Nó chỉ kiêng phòng bên trái nhất thôi.'),
        q_tf(5, 'Từ hai thẻ 0 và 6 chỉ lập được số 60.', True,
             'Đúng, vì thẻ 0 không đứng đầu được.'),
    ],
)

# ═══ ⑩ B05 · TÌM ĐỦ MỌI SỐ ═══
B05 = bai(
    5, 'TÌM ĐỦ MỌI SỐ — ĐI TUẦN TRA CÓ THỨ TỰ',
    'SỐ 3.2 — Liệt kê đủ mọi số thoả điều kiện, không sót và không trùng.',
    video(
        ['Tính được tổng hai chữ số của một số.',
         'Liệt kê đủ mọi số có tổng chữ số cho trước, theo thứ tự.',
         'Nói được vì sao bắt đầu ở đâu và vì sao dừng ở đâu.'],
        ['Đề bài: Tìm tất cả các số có hai chữ số mà tổng hai chữ số bằng 5.',
         'Kể lộn xộn thì dễ sót',
         'Nhớ ra số nào kể số ấy thì rất dễ bỏ quên, mà cũng dễ kể trùng.',
         'Đi tuần tra có thứ tự',
         'Cho chữ số hàng chục tăng dần từng nấc một. Mỗi nấc hỏi: đơn vị phải là mấy '
         'thì tổng bằng năm?',
         'Chục bằng một thì đơn vị bằng bốn, được số 14. Chục hai thì đơn vị ba, được '
         '23. Rồi 32, rồi 41, rồi 50.',
         'Vì sao bắt đầu từ chục bằng một',
         'Vì chục bằng không thì chữ số 0 đứng đầu, không còn là số có hai chữ số.',
         'Vì sao dừng ở chục bằng năm',
         'Vì chục bằng sáu thì đơn vị phải là năm trừ sáu — không có chữ số nào như '
         'thế.',
         'Đáp số: đủ 5 số là 14, 23, 32, 41, 50.'],
        ['Có bạn kể được 14, 23, 41 rồi bảo hết rồi.',
         'Gợi ý 1: Con xếp mấy số ấy theo hàng chục tăng dần xem có nấc nào bị nhảy '
         'cóc không.',
         'Gợi ý 2: Chục bằng ba thì đơn vị phải là mấy? Còn chục bằng năm thì sao?',
         'Chữa: kể lộn xộn nên sót mất 32 và 50. Đi tuần tra theo thứ tự thì không '
         'bao giờ sót.'],
        ['Cho con kẻ một bảng hai cột: chục và đơn vị. Điền chục từ một tăng dần, con '
         'tự thấy đơn vị giảm theo.',
         'Câu hỏi quan trọng nhất không phải "được mấy số" mà là "vì sao dừng ở đây?". '
         'Bố mẹ nhớ hỏi thêm câu ấy.'],
    ),
    [
        lt(1, 1, 'Tính tổng hai chữ số của số 25.', 'Cộng hai chữ số: 2 + 5 = 7.'),
        lt(2, 1, 'Tính tổng hai chữ số của số 43.', 'Cộng hai chữ số: 4 + 3 = 7.'),
        lt(3, 1, 'Số có hai chữ số, tổng hai chữ số bằng 5. Nếu hàng chục là 1 thì '
                 'hàng đơn vị phải là mấy?',
           'Tổng phải bằng 5 nên đơn vị là 5 − 1 = 4.'),
        lt(4, 2, 'Vẫn tổng bằng 5. Nếu hàng chục là 2 thì được số nào?',
           'Đơn vị là 5 − 2 = 3, nên được số 23.'),
        lt(5, 2, 'Vẫn tổng bằng 5. Nếu hàng chục là 5 thì được số nào?',
           'Đơn vị là 5 − 5 = 0, nên được số 50.'),
        lt(6, 2, 'Có tất cả bao nhiêu số có hai chữ số mà tổng hai chữ số bằng 5?',
           'Đi tuần tra được 14, 23, 32, 41, 50 — tất cả 5 số.'),
        lt(7, 3, 'Vì sao không bắt đầu từ hàng chục bằng 0?',
           'Vì chữ số 0 đứng đầu thì không còn là số có hai chữ số.'),
        lt(8, 3, 'Có bao nhiêu số có hai chữ số mà tổng hai chữ số bằng 3?',
           'Đi tuần tra: 12, 21, 30 — tất cả 3 số.'),
    ] + [
        q_tf(1, 'Kể lộn xộn thì dễ sót số.', True,
             'Đúng. Đi tuần tra theo thứ tự mới chắc.'),
        q_tf(2, 'Có 5 số có hai chữ số mà tổng hai chữ số bằng 5.', True,
             'Đúng: 14, 23, 32, 41, 50.'),
        q_mcq(3, 'Tổng hai chữ số bằng 5, hàng chục là 3 thì được số',
              ['32', '35', '23', '53'], '32',
              'Đơn vị phải là 5 trừ 3, tức 2.'),
        q_mcq(4, 'Vì sao dừng ở hàng chục bằng 5?',
              ['vì chục bằng 6 thì đơn vị không có số nào',
               'vì kể thế là đủ đẹp', 'vì mỏi tay'],
              'vì chục bằng 6 thì đơn vị không có số nào',
              'Năm trừ sáu thì không ra chữ số nào cả.'),
        q_tf(5, 'Hàng chục có thể bằng 0 khi lập số có hai chữ số.', False,
             'Sai. Khi ấy chữ số 0 đứng đầu và số mất một chữ số.'),
    ],
)

MOI = [B01, B34, B35, B02, B36, B03, B37, B04, B38, B05]

# Bài mới chèn vào đâu — khai theo BÀI ĐỨNG TRƯỚC, không khai theo số thứ tự.
SAU = {
    'DL:KSN2.B34': 'DL:KSN2.B01',
    'DL:KSN2.B35': 'DL:KSN2.B34',
    'DL:KSN2.B36': 'DL:KSN2.B02',
    'DL:KSN2.B37': 'DL:KSN2.B03',
    'DL:KSN2.B38': 'DL:KSN2.B04',
}

# ⚠ LUẬT Ô NHẬP SỐ 1 — quyển đọc chậm KHÔNG được có ô gõ chữ. Đáp không phải con số
# thì BẮT BUỘC khai `options` cho bé bấm. `khuon_bai_lop2.soi_bai` canh đúng điều đó.
LON_BE = ['lớn hơn', 'bé hơn']

O_NHAP_MOI = {
 'DL:KSN2.B01#C1': {'parts': [{'label': 'trăm', 'value': 3},
                              {'label': 'chục', 'value': 6},
                              {'label': 'đơn vị', 'value': 8}]},
 'DL:KSN2.B01#C2': {'value': 4},
 'DL:KSN2.B01#C3': {'parts': [{'label': 'phòng nào', 'options': PHONG,
                               'value': 'phòng trăm'}]},
 'DL:KSN2.B01#C4': {'parts': [{'label': 'trăm', 'value': 5},
                              {'label': 'chục', 'value': 0},
                              {'label': 'đơn vị', 'value': 7}]},
 'DL:KSN2.B01#C5': {'parts': [{'label': 'chục', 'value': 9},
                              {'label': 'đơn vị', 'value': 0}]},
 'DL:KSN2.B01#C6': {'value': 416},
 'DL:KSN2.B01#C7': {'value': 703},
 'DL:KSN2.B01#C8': {'value': 802},

 'DL:KSN2.B34#C1': {'value': 200},
 'DL:KSN2.B34#C2': {'value': 40},
 'DL:KSN2.B34#C3': {'value': 5},
 'DL:KSN2.B34#C4': {'parts': [{'label': 'phòng trăm', 'value': 200},
                              {'label': 'phòng chục', 'value': 40},
                              {'label': 'phòng đơn vị', 'value': 5}]},
 'DL:KSN2.B34#C5': {'parts': [{'label': 'phòng trăm', 'value': 300},
                              {'label': 'phòng chục', 'value': 60},
                              {'label': 'phòng đơn vị', 'value': 8}]},
 'DL:KSN2.B34#C6': {'parts': [{'label': 'chữ số 5 đáng', 'value': 500},
                              {'label': 'chữ số 7 đáng', 'value': 7}]},
 'DL:KSN2.B34#C7': {'value': 629},
 'DL:KSN2.B34#C8': {'parts': [{'label': 'chữ số đứng đầu', 'value': 400},
                              {'label': 'chữ số đứng giữa', 'value': 40},
                              {'label': 'chữ số đứng cuối', 'value': 4}]},

 'DL:KSN2.B35#C1': {'parts': [{'label': 'số lớn hơn', 'options': ['245', '198'],
                               'value': '245'}]},
 'DL:KSN2.B35#C2': {'parts': [{'label': 'số 245 có', 'value': 2},
                              {'label': 'số 198 có', 'value': 1}]},
 'DL:KSN2.B35#C3': {'parts': [{'label': 'số lớn hơn', 'options': ['372', '368'],
                               'value': '372'}]},
 'DL:KSN2.B35#C4': {'parts': [{'label': 'số lớn hơn', 'options': ['254', '245'],
                               'value': '254'}]},
 'DL:KSN2.B35#C5': {'parts': [{'label': 'số lớn hơn', 'options': ['570', '507'],
                               'value': '570'}]},
 'DL:KSN2.B35#C6': {'parts': [{'label': 'số lớn hơn', 'options': ['100', '88'],
                               'value': '100'}]},
 'DL:KSN2.B35#C7': {'parts': [{'label': 'bé nhất', 'value': 198},
                              {'label': 'ở giữa', 'value': 245},
                              {'label': 'lớn nhất', 'value': 254}]},
 'DL:KSN2.B35#C8': {'parts': [{'label': 'phòng nào', 'options': PHONG,
                               'value': 'phòng đơn vị'}]},

 'DL:KSN2.B02#C1': {'value': 70},
 'DL:KSN2.B02#C2': {'value': 250},
 'DL:KSN2.B02#C3': {'value': 10},
 'DL:KSN2.B02#C4': {'value': 120},
 'DL:KSN2.B02#C5': {'parts': [{'label': 'dọn từ phòng', 'options': PHONG,
                               'value': 'phòng đơn vị'},
                              {'label': 'sang phòng', 'options': PHONG,
                               'value': 'phòng chục'}]},
 'DL:KSN2.B02#C6': {'value': 600},
 'DL:KSN2.B02#C7': {'value': 45},
 'DL:KSN2.B02#C8': {'value': 900},

 'DL:KSN2.B36#C1': {'value': 7},
 'DL:KSN2.B36#C2': {'value': 25},
 'DL:KSN2.B36#C3': {'value': 10},
 'DL:KSN2.B36#C4': {'value': 60},
 'DL:KSN2.B36#C5': {'parts': [{'label': 'xoá được không', 'options': CO_KHONG,
                               'value': 'không'}]},
 'DL:KSN2.B36#C6': {'value': 12},
 'DL:KSN2.B36#C7': {'value': 450},
 'DL:KSN2.B36#C8': {'value': 9},

 'DL:KSN2.B03#C1': {'value': 52},
 'DL:KSN2.B03#C2': {'parts': [{'label': 'số lớn hơn', 'options': ['52', '25'],
                               'value': '52'}]},
 'DL:KSN2.B03#C3': {'value': 5},
 'DL:KSN2.B03#C4': {'value': 41},
 'DL:KSN2.B03#C5': {'value': 72},
 'DL:KSN2.B03#C6': {'parts': [{'label': 'còn là số hai chữ số không',
                               'options': CO_KHONG, 'value': 'không'}]},
 'DL:KSN2.B03#C7': {'parts': [{'label': 'số lớn hơn', 'options': ['83', '38'],
                               'value': '83'}]},
 'DL:KSN2.B03#C8': {'parts': [{'label': 'số mới', 'value': 64},
                              {'label': 'so với số cũ', 'options': LON_BE,
                               'value': 'lớn hơn'}]},

 'DL:KSN2.B37#C1': {'value': 27},
 'DL:KSN2.B37#C2': {'value': 18},
 'DL:KSN2.B37#C3': {'value': 9},
 'DL:KSN2.B37#C4': {'value': 18},
 'DL:KSN2.B37#C5': {'value': 36},
 'DL:KSN2.B37#C6': {'value': 54},
 'DL:KSN2.B37#C7': {'parts': [{'label': 'hiệu hai chữ số', 'value': 3},
                              {'label': 'gấp mấy lần', 'value': 9}]},
 'DL:KSN2.B37#C8': {'parts': [{'label': 'đoán trước', 'value': 54},
                              {'label': 'tính ra', 'value': 54}]},

 'DL:KSN2.B04#C1': {'value': 83},
 'DL:KSN2.B04#C2': {'value': 38},
 'DL:KSN2.B04#C3': {'value': 852},
 'DL:KSN2.B04#C4': {'value': 258},
 'DL:KSN2.B04#C5': {'parts': [{'label': 'phòng nào', 'options': PHONG,
                               'value': 'phòng trăm'}]},
 'DL:KSN2.B04#C6': {'parts': [{'label': 'số lớn nhất', 'value': 741},
                              {'label': 'số bé nhất', 'value': 147}]},
 'DL:KSN2.B04#C7': {'parts': [{'label': 'số lớn nhất', 'value': 963},
                              {'label': 'số bé nhất', 'value': 369},
                              {'label': 'hiệu', 'value': 594}]},
 'DL:KSN2.B04#C8': {'value': 1},

 'DL:KSN2.B38#C1': {'value': 730},
 'DL:KSN2.B38#C2': {'parts': [{'label': 'có phải không', 'options': CO_KHONG,
                               'value': 'không'}]},
 'DL:KSN2.B38#C3': {'value': 307},
 'DL:KSN2.B38#C4': {'value': 509},
 'DL:KSN2.B38#C5': {'value': 950},
 'DL:KSN2.B38#C6': {'parts': [{'label': 'phòng nào', 'options': PHONG,
                               'value': 'phòng trăm'}]},
 'DL:KSN2.B38#C7': {'parts': [{'label': 'số lớn nhất', 'value': 820},
                              {'label': 'số bé nhất', 'value': 208},
                              {'label': 'hiệu', 'value': 612}]},
 'DL:KSN2.B38#C8': {'value': 60},

 'DL:KSN2.B05#C1': {'value': 7},
 'DL:KSN2.B05#C2': {'value': 7},
 'DL:KSN2.B05#C3': {'value': 4},
 'DL:KSN2.B05#C4': {'value': 23},
 'DL:KSN2.B05#C5': {'value': 50},
 'DL:KSN2.B05#C6': {'value': 5},
 'DL:KSN2.B05#C7': {'parts': [{'label': 'vì sao',
                               'options': ['vì khi ấy không còn là số có hai chữ số',
                                           'vì số 0 quá bé'],
                               'value': 'vì khi ấy không còn là số có hai chữ số'}]},
 'DL:KSN2.B05#C8': {'value': 3},
}


def soi():
    loi = soi_bai(MOI, O_NHAP_MOI)
    cu = {f'DL:KSN2.B{n:02d}' for n in (1, 2, 3, 4, 5)}
    moi_ = {f'DL:KSN2.B{n}' for n in (34, 35, 36, 37, 38)}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: {co ^ (cu | moi_)}')
    for b in MOI:
        for m in ('chuyenMoBai', 'khamPha'):
            if b['muc'][m]['dong']:
                loi.append(f'{b["id"]}: mục {m} phải RỖNG với bài dùng video')
    # Bác chốt: video KHÔNG nhân vật — nên bài cũng bỏ luôn tên nhân vật.
    for b in MOI:
        van = json.dumps(b, ensure_ascii=False)
        for ten in ('Trí Long', 'Su Kem'):
            if ten in van:
                loi.append(f'{b["id"]}: còn tên nhân vật "{ten}"')
    NEO = {'DL:KSN2.B01': '245', 'DL:KSN2.B34': '245', 'DL:KSN2.B35': '245',
           'DL:KSN2.B02': '25', 'DL:KSN2.B36': '250', 'DL:KSN2.B03': '52',
           'DL:KSN2.B37': '52', 'DL:KSN2.B04': '852', 'DL:KSN2.B38': '307'}
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
        print(f"  {b['id']}  {b['ten'][:50]:50} {n} luyện + {q} quiz")
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
