# -*- coding: utf-8 -*-
"""CHƯƠNG 3 · DẤU HIỆU CHIA HẾT — bốn bài cũ tách thành CHÍN, mỗi bài một việc.

Bác ra ba luật ở đợt 2, và cả ba đều nằm trong tệp này:

  8 · MỘT VIDEO — MỘT VẤN ĐỀ. Bốn bài cũ gộp đôi ba việc vào một chỗ: B09 dạy dấu
      hiệu cho 2 VÀ cho 5, B10 dạy cho 3 VÀ cho 9, B11 dạy chia có dư VÀ bài toán
      thừa thiếu. Bé chưa kịp nắm cái thứ nhất đã phải nhận cái thứ hai.
  9 · HÌNH CHO CHỖ KHÓ HIỂU. "Chia hết" nói bằng lời thì mãi vẫn trừu tượng; xếp
      mười hai viên thành bốn nhóm ba viên, không thừa viên nào, thì bé THẤY. Cảnh
      `nhom_deu` dựng riêng cho việc đó.
 10 · CÔNG THỨC PHẢI GIẢI THÍCH TỪNG THÀNH PHẦN, VÀ VÌ SAO SUY RA ĐƯỢC. Đây là chỗ
      cả chương này vốn hổng nặng nhất: bốn dấu hiệu chia hết trước nay chỉ được
      NÊU RA, không bài nào nói vì sao chúng đúng. Bé học thuộc rồi quên.

── VÀ MỘT LỖ THỦNG NGAY GỐC ──
Không bài nào trong bốn bài cũ định nghĩa CHIA HẾT LÀ GÌ. Cả chương mang tên "dấu
hiệu chia hết" mà khái niệm gốc thì bỏ trống — đúng lỗi của cụm dãy số trước khi
sửa (ở đó là "dãy số là gì"). Nên bài thứ nhất của chín bài là bài khái niệm.

── MÃ BÀI KHÔNG NÓI LÊN THỨ TỰ (lối C, 14-08) ──
Bốn mã cũ B09 B10 B11 B12 GIỮ NGUYÊN, năm bài mới lấy mã trống kế tiếp B50 tới B54.
Thứ tự học khai ở `data/lop4/thu_tu.json`, nên năm bài mới xen được vào giữa mà
không phải đổi mã bài nào và không phải dời tiến độ đã lưu của bé.

Bốn mã cũ được VIẾT LẠI nội dung. Bé từng học B09 cũ (dấu hiệu cho 2 và cho 5) nay
mở ra thấy B09 mới (chỉ còn dấu hiệu cho 2) — vẫn đúng mảng kiến thức ấy, vẫn chương
ấy, nên giữ mã là hợp lý hơn bỏ đi rồi để tiến độ của bé mồ côi.

── SỐ NEO CHUNG CẢ CHƯƠNG ──
`270` chạy suốt bảy bài đầu. Chọn nó vì một mình nó thoả CẢ BỐN dấu hiệu: tận cùng
là không nên chia hết cho hai và cho năm; tổng chữ số hai cộng bảy cộng không bằng
chín nên chia hết cho ba và cho chín. Bé không phải làm quen số mới ở mỗi bài, và
tới bài thứ tư thì đã thuộc lòng nó.

    tools/tts/.venv/bin/python  — KHÔNG cần, tệp này không sinh tiếng.
    python3 tools/chia_het_lop4.py --xem     # in ra, chưa ghi
    python3 tools/chia_het_lop4.py           # ghi vào data/lop4/
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

TEN_CHUONG = 'DẤU HIỆU CHIA HẾT'
CHUONG = 3

CO_KHONG = ['có', 'không']

# Đường lui về lớp 3 — bé chưa vững phép chia thì có chỗ quay lại.
LUI_CHIA = {'ve': ['DL:KSN3.B06'], 'ten': ['PHÉP CHIA CÓ DƯ CHÍNH DANH'],
            'canCu': 'chuDe', 'lopDuoi': 3}
LUI_CHIA_DU = {'ve': ['DL:KSN3.B06', 'DL:KSN3.B07'],
               'ten': ['PHÉP CHIA CÓ DƯ CHÍNH DANH', 'TRUY TÌM SỐ CHIA a DƯ b'],
               'canCu': 'sach', 'lopDuoi': 3}
LUI_NHAN = {'ve': ['DL:KSN3.B05'], 'ten': ['NHÂN RA NGOÀI BẢNG'],
            'canCu': 'chuDe', 'lopDuoi': 3}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return _bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau, CHUONG, TEN_CHUONG)


def video(muc_tieu, vidu, nham, bome):
    """Bài dùng VIDEO thay cả mở bài lẫn bài giảng — bốn mục ②③④⑤ để RỖNG.

    Bác chốt 14-08: "Video đã thay thế cho cả phần mở bài và bài giảng. Xoá toàn bộ
    nội dung phần mở bài và bài giảng cũ đi, chỉ để Video." Bộ dựng thấy rỗng thì
    không sinh màn nào, bé đi thẳng từ video sang bài mẫu. `video_toan.test.mjs`
    canh đúng điều đó, nên rỗng ở đây là CHỦ Ý chứ không phải bỏ sót.
    """
    return dung_muc('', [], muc_tieu, [], [], [], vidu, nham, bome)


# ═══════════════════════════════════════════════════════════════════════════
# ① B50 · CHIA HẾT LÀ GÌ — bài KHÁI NIỆM, mở đầu cả chương
# ═══════════════════════════════════════════════════════════════════════════
# Không một dấu hiệu nào ở đây. Bài này chỉ làm đúng một việc: cho bé thấy chia hết
# và chia còn thừa khác nhau chỗ nào, rồi gọi đúng tên bốn thứ trong một phép chia.
# Gọi được tên rồi thì tám bài sau chỉ còn là tám cách nhìn nhanh.
B50 = bai(
    50, 'CHIA HẾT LÀ GÌ — VÀ PHẦN THỪA GỌI LÀ GÌ',
    'Dạng gốc: SỐ 3.0 mức Lớp 4 — Khái niệm chia hết · số dư · số bị chia · số chia '
    '· thương. KHÔNG dấu hiệu, KHÔNG mẹo nhìn nhanh.',
    'Lớp 3 con đã làm phép chia có dư rồi. Nhưng hôm ấy con làm theo phép tính. Hôm '
    'nay mình dừng lại gọi đúng tên: chia hết nghĩa là gì, phần thừa gọi là gì, và '
    'trong một phép chia thì số nào tên là gì. Gọi đúng tên rồi thì tám bài sau chỉ '
    'còn là tám cách nhìn cho nhanh.',
    LUI_CHIA,
    video(
        ['Nói được chia hết nghĩa là chia xong không thừa gì.',
         'Gọi đúng tên số bị chia, số chia, thương và số dư.',
         'Biết một số chia hết cho số này nhưng có thể không chia hết cho số khác.'],
        ['Đề bài: Có 12 viên kẹo. Chia đều cho 3 bạn thì mỗi bạn được mấy viên, có '
         'thừa không? Chia đều cho 5 bạn thì sao?',
         'Chia cho 3 bạn',
         'Xếp 12 viên thành từng nhóm 3 viên: được 4 nhóm, không thừa viên nào.',
         '12 : 3 = 4, số dư bằng 0. Vậy 12 chia hết cho 3.',
         'Chia cho 5 bạn',
         'Xếp 12 viên thành từng nhóm 5 viên: được 2 nhóm, còn thừa 2 viên.',
         '12 : 5 = 2 (dư 2). Số dư khác 0 nên 12 KHÔNG chia hết cho 5.',
         'Gọi tên trong phép 12 : 5 = 2 (dư 2)',
         '12 là số bị chia, 5 là số chia, 2 là thương, 2 còn lại là số dư.',
         'Đáp số: 12 chia hết cho 3, mỗi bạn 4 viên không thừa; 12 không chia hết '
         'cho 5, chia được 2 viên mỗi bạn và thừa 2 viên.'],
        ['Có bạn nói: "12 chia hết cho 5, vì chia được 2 viên mỗi bạn."',
         'Gợi ý 1: Con xếp thử ra xem. Chia xong còn thừa mấy viên trên bàn?',
         'Gợi ý 2: Còn thừa thì chưa gọi là chia hết. Chia hết là chia xong KHÔNG '
         'còn viên nào.',
         'Chữa: 12 : 5 = 2 dư 2. Số dư là 2, khác 0, nên 12 KHÔNG chia hết cho 5.'],
        ['Lấy đúng 12 hạt đậu ra bàn rồi bảo con chia đều cho 3 người, sau đó chia '
         'đều cho 5 người. Con sẽ tự thấy lần nào thừa lần nào không.',
         'Con nói "chia được" thay cho "chia hết" là chuyện thường. Bố mẹ chỉ cần '
         'hỏi lại một câu: "Chia xong còn thừa hạt nào không?"'],
    ),
    [
        lt(1, 1, 'Có 12 viên kẹo — đúng số kẹo trong video. Xếp thành từng nhóm 3 '
                 'viên thì được mấy nhóm và thừa mấy viên?',
           'Xếp được 4 nhóm, không thừa viên nào. Vậy 12 chia hết cho 3.'),
        lt(2, 1, 'Vẫn 12 viên kẹo. Xếp thành từng nhóm 5 viên thì được mấy nhóm và '
                 'thừa mấy viên?',
           'Xếp được 2 nhóm, thừa 2 viên. Vậy 12 không chia hết cho 5.'),
        lt(3, 1, 'Trong phép chia 12 : 5 = 2 (dư 2), số nào là số chia và số dư bằng '
                 'bao nhiêu?',
           'Số chia là 5 (số ta đem chia cho), số dư là 2 (phần còn thừa lại).'),
        lt(4, 2, 'Số 20 có chia hết cho 4 không? Số dư bằng bao nhiêu?',
           '20 : 4 = 5, không thừa gì. Số dư bằng 0 nên 20 CHIA HẾT cho 4.'),
        lt(5, 2, 'Số 20 có chia hết cho 3 không? Số dư bằng bao nhiêu?',
           '20 : 3 = 6 (dư 2). Số dư là 2, khác 0, nên 20 KHÔNG chia hết cho 3.'),
        lt(6, 2, 'Bạn Nam nói: "Số 15 chia hết cho 4 vì 15 : 4 = 3 dư 3." Bạn nói '
                 'đúng hay sai? Vì sao?',
           'SAI. Chia xong vẫn còn thừa 3, mà chia hết là chia xong không thừa gì. '
           'Số dư phải bằng 0 mới gọi là chia hết.'),
        lt(7, 2, 'Trong phép chia 27 : 4, thương bằng bao nhiêu và số dư bằng bao nhiêu?',
           '27 : 4 = 6 (dư 3). Thương là 6, số dư là 3.'),
        lt(8, 3, 'Có 18 quả cam. Chia đều vào các đĩa, mỗi đĩa 6 quả thì có thừa '
                 'không? Còn mỗi đĩa 4 quả thì thừa mấy quả?',
           'Mỗi đĩa 6 quả: 18 : 6 = 3 đĩa, không thừa — 18 chia hết cho 6. Mỗi đĩa '
           '4 quả: 18 : 4 = 4 (dư 2), thừa 2 quả — 18 không chia hết cho 4.'),
        lt(9, 3, 'Tìm một số vừa chia hết cho 2 vừa chia hết cho 3, và số đó bé hơn 10.',
           'Số 6 (6 : 2 = 3 không thừa, 6 : 3 = 2 không thừa). Ngoài ra 0 cũng được, '
           'nhưng số thường lấy là 6.'),
        q_tf(1, 'Chia hết nghĩa là chia xong không còn thừa gì.', True,
             'Đáp án: ĐÚNG — chia hết là số dư bằng 0.'),
        q_tf(2, 'Số 12 chia hết cho 5.', False,
             'SAI — 12 : 5 = 2 dư 2, còn thừa 2 nên không chia hết.'),
        q_mcq(3, 'Trong phép chia 17 : 5 = 3 (dư 2), số 2 được gọi là:',
              ['A. số dư', 'B. thương', 'C. số chia'], 'A. số dư',
              'Phần còn thừa lại sau khi chia gọi là số dư.'),
        q_mcq(4, 'Một số chia hết cho 4 khi số dư của phép chia đó bằng:',
              ['A. 0', 'B. 1', 'C. 4'], 'A. 0',
              'Chia hết nghĩa là không thừa gì, tức số dư bằng 0.'),
        q_mcq(5, 'Số nào dưới đây CHIA HẾT cho 3?',
              ['A. 12', 'B. 13', 'C. 14'], 'A. 12',
              '12 : 3 = 4, không thừa. Còn 13 và 14 đều còn dư.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ② B09 · DẤU HIỆU CHIA HẾT CHO 2  (mã cũ, nội dung viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ dạy CẢ cho 2 lẫn cho 5 trong một chỗ. Nay chỉ còn cho 2 — và thêm hẳn phần
# VÌ SAO, thứ mà bài cũ không có: mọi số tròn chục đều chia hết cho 2, nên phần chục
# không bao giờ làm thừa, chỉ chữ số cuối mới quyết định.
B09 = bai(
    9, 'DẤU HIỆU CHIA HẾT CHO 2 — VÌ SAO CHỈ NHÌN CHỮ SỐ CUỐI',
    'Dạng gốc: SỐ 3.1 mức Lớp 4 — Dấu hiệu chia hết cho 2, kèm chứng minh bằng cách '
    'tách số thành phần tròn chục và chữ số đơn vị.',
    'Bài trước con đã biết chia hết là chia xong không thừa gì. Nhưng số to như 270 '
    'thì chia thử rất lâu. Hôm nay con học cách nhìn một cái là biết — và quan trọng '
    'hơn, con sẽ hiểu VÌ SAO chỉ cần nhìn đúng một chữ số cuối cùng.',
    LUI_CHIA,
    video(
        ['Nói được số chia hết cho 2 là số chẵn, tận cùng là 0, 2, 4, 6 hoặc 8.',
         'Giải thích được vì sao chỉ cần nhìn chữ số cuối.',
         'Nhìn một số bất kỳ và nói ngay nó có chia hết cho 2 không.'],
        ['Đề bài: Số 24 có chia hết cho 2 không? Vì sao chỉ cần nhìn chữ số cuối?',
         'Tách số ra hai phần',
         '24 = 20 + 4. Phần tròn chục là 20, chữ số cuối là 4.',
         'Xét phần tròn chục',
         '20 = 2 × 10, mà 10 = 2 × 5, nên 20 luôn chia hết cho 2.',
         'Mọi số tròn chục đều như vậy, nên phần này KHÔNG BAO GIỜ làm thừa.',
         'Vậy chỉ còn chữ số cuối quyết định',
         'Chữ số cuối là 4, mà 4 chia hết cho 2, nên 24 chia hết cho 2.',
         'Thử với số neo của chương',
         '270 có chữ số cuối là 0, mà 0 chia hết cho 2, nên 270 chia hết cho 2.',
         'Đáp số: 24 chia hết cho 2. Chỉ cần nhìn chữ số cuối, vì phần tròn chục '
         'luôn chia hết cho 2 rồi.'],
        ['Có bạn nhìn số 132 rồi nói: "Số này có chữ số 3 là số lẻ, nên 132 không '
         'chia hết cho 2."',
         'Gợi ý 1: Con xem lại xem dấu hiệu bảo nhìn chữ số nào?',
         'Gợi ý 2: Chỉ nhìn chữ số CUỐI CÙNG thôi. Chữ số cuối của 132 là số mấy?',
         'Chữ: chữ số cuối là 2, mà 2 chia hết cho 2, nên 132 CHIA HẾT cho 2. Các '
         'chữ số đứng trước nằm ở phần tròn chục, phần ấy đã chia hết cho 2 sẵn rồi.'],
        ['Đọc to vài số bất kỳ rồi hỏi con "chia hết cho 2 không". Con trả lời được '
         'trong một giây là đã nắm dấu hiệu.',
         'Nếu con còn ngập ngừng, hỏi thêm một câu: "Vì sao chỉ nhìn chữ số cuối?" — '
         'trả lời được câu này thì con hiểu bài, chứ không phải học thuộc.'],
    ),
    [
        lt(1, 1, 'Số 24 — đúng số trong video. Chữ số cuối của nó là mấy, và 24 có '
                 'chia hết cho 2 không?',
           'Chữ số cuối là 4. Số 4 chia hết cho 2, nên 24 CHIA HẾT cho 2.'),
        lt(2, 1, 'Số 25 có chia hết cho 2 không? Vì sao?',
           'Chữ số cuối là 5, mà 5 không chia hết cho 2, nên 25 KHÔNG chia hết cho 2.'),
        lt(3, 1, 'Số 270 có chia hết cho 2 không?',
           'Chữ số cuối là 0, mà 0 chia hết cho 2, nên 270 CHIA HẾT cho 2.'),
        lt(4, 2, 'Trong ba số 132 ; 145 ; 208, những số nào chia hết cho 2?',
           'Nhìn chữ số cuối: 132 cuối là 2 (chia hết), 145 cuối là 5 (không), 208 '
           'cuối là 8 (chia hết). Vậy 132 và 208 chia hết cho 2.'),
        lt(5, 2, 'Bạn Lan nói: "Số 137 có chữ số 3 đứng giữa nên chia hết cho 2." '
                 'Bạn nói đúng hay sai? Số 137 có chia hết cho 2 không?',
           'SAI. Chỉ nhìn chữ số CUỐI. Chữ số cuối của 137 là 7, không chia hết cho '
           '2, nên 137 KHÔNG chia hết cho 2.'),
        lt(6, 2, 'Vì sao khi xét chia hết cho 2 ta không cần quan tâm tới các chữ số '
                 'đứng trước chữ số cuối?',
           'Vì các chữ số đứng trước tạo thành phần tròn chục, mà mọi số tròn chục '
           'đều chia hết cho 2 (do 10 = 2 × 5). Phần ấy không bao giờ làm thừa.'),
        lt(7, 2, 'Viết một số có ba chữ số, chia hết cho 2, và có chữ số hàng trăm là 3.',
           'Ví dụ 302 (chữ số cuối là 2 nên chia hết cho 2). Các số 300, 304, 316… '
           'cũng được, miễn chữ số cuối là 0, 2, 4, 6 hoặc 8.'),
        lt(8, 3, 'Từ ba chữ số 1 ; 4 ; 5 hãy viết một số có ba chữ số chia hết cho 2, '
                 'dùng mỗi chữ số đúng một lần.',
           'Muốn chia hết cho 2 thì chữ số cuối phải chẵn — trong ba chữ số chỉ có 4 '
           'là chẵn. Vậy đặt 4 ở cuối: được 154 hoặc 514.'),
        lt(9, 3, 'Có bao nhiêu số có hai chữ số vừa lớn hơn 20 vừa nhỏ hơn 30 và chia '
                 'hết cho 2?',
           'Các số từ 21 đến 29 có chữ số cuối chẵn là 22, 24, 26, 28 — tất cả 4 số.'),
        q_tf(1, 'Số chia hết cho 2 còn được gọi là số chẵn.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Muốn biết một số có chia hết cho 2 không, phải cộng tất cả các chữ '
                'số của nó lại.', False,
             'SAI — cộng chữ số là dấu hiệu của 3 và 9. Với 2 thì chỉ nhìn chữ số cuối.'),
        q_mcq(3, 'Số nào dưới đây CHIA HẾT cho 2?',
              ['A. 146', 'B. 231', 'C. 405'], 'A. 146',
              'Chữ số cuối của 146 là 6, một số chẵn.'),
        q_mcq(4, 'Chữ số cuối của một số chia hết cho 2 phải là:',
              ['A. 0, 2, 4, 6 hoặc 8', 'B. 0 hoặc 5', 'C. số bất kỳ'],
              'A. 0, 2, 4, 6 hoặc 8', 'Đó là năm chữ số chẵn.'),
        q_mcq(5, 'Vì sao chỉ cần nhìn chữ số cuối để biết một số có chia hết cho 2?',
              ['A. Vì phần tròn chục luôn chia hết cho 2',
               'B. Vì chữ số cuối là chữ số lớn nhất',
               'C. Vì các chữ số khác không có giá trị'],
              'A. Vì phần tròn chục luôn chia hết cho 2',
              '10 = 2 × 5 nên mọi số tròn chục đều chia hết cho 2, không bao giờ làm thừa.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ③ B51 · DẤU HIỆU CHIA HẾT CHO 5
# ═══════════════════════════════════════════════════════════════════════════
# Cùng một lối chứng minh với bài trước, cố ý. Bé vừa thấy "phần tròn chục không làm
# thừa" ở bài cho 2; ở đây thấy lại đúng lối ấy với số 5 thì hiểu rằng đó không phải
# mẹo riêng của số 2, mà là một cách nghĩ dùng được nhiều lần.
B51 = bai(
    51, 'DẤU HIỆU CHIA HẾT CHO 5 — CŨNG CHỈ NHÌN CHỮ SỐ CUỐI',
    'Dạng gốc: SỐ 3.2 mức Lớp 4 — Dấu hiệu chia hết cho 5, kèm chứng minh bằng cách '
    'tách số thành phần tròn chục và chữ số đơn vị.',
    'Bài trước con đã thấy: phần tròn chục của một số luôn chia hết cho 2, nên chỉ '
    'chữ số cuối quyết định. Hôm nay con thử đúng lối nghĩ ấy với số 5, và sẽ thấy '
    'nó lại đúng — vì 10 chia hết cho 5 y như 10 chia hết cho 2.',
    LUI_CHIA,
    video(
        ['Nói được số chia hết cho 5 là số có tận cùng là 0 hoặc 5.',
         'Giải thích được vì sao chỉ cần nhìn chữ số cuối, giống bài trước.',
         'Phân biệt được dấu hiệu chia hết cho 5 với dấu hiệu chia hết cho 2.'],
        ['Đề bài: Số 35 có chia hết cho 5 không? Vì sao chỉ cần nhìn chữ số cuối?',
         'Tách số ra hai phần',
         '35 = 30 + 5. Phần tròn chục là 30, chữ số cuối là 5.',
         'Xét phần tròn chục',
         '30 = 3 × 10, mà 10 = 5 × 2, nên 30 luôn chia hết cho 5.',
         'Mọi số tròn chục đều chia hết cho 5, nên phần này không làm thừa.',
         'Vậy chỉ còn chữ số cuối quyết định',
         'Chữ số cuối là 5, mà 5 chia hết cho 5, nên 35 chia hết cho 5.',
         'Thử với số neo của chương',
         '270 có chữ số cuối là 0, mà 0 chia hết cho 5, nên 270 chia hết cho 5.',
         'Đáp số: 35 chia hết cho 5. Chữ số cuối phải là 0 hoặc 5 thì số mới chia '
         'hết cho 5.'],
        ['Có bạn nói: "Số 52 chia hết cho 5, vì trong số ấy có chữ số 5."',
         'Gợi ý 1: Chữ số 5 ấy đứng ở đâu trong số 52?',
         'Gợi ý 2: Dấu hiệu chỉ xét chữ số CUỐI CÙNG. Chữ số cuối của 52 là mấy?',
         'Chữa: chữ số cuối của 52 là 2, không phải 0 cũng không phải 5, nên 52 '
         'KHÔNG chia hết cho 5. Có chữ số 5 ở giữa số thì không tính.'],
        ['Bảo con đọc các số trên hoá đơn hay biển số xe rồi hỏi số nào chia hết cho 5.',
         'Chỗ con hay nhầm nhất là thấy chữ số 5 ở bất kỳ đâu cũng nói chia hết. Bố '
         'mẹ hỏi lại: "Chữ số CUỐI là mấy?"'],
    ),
    [
        lt(1, 1, 'Số 35 — đúng số trong video. Chữ số cuối là mấy, và 35 có chia hết '
                 'cho 5 không?',
           'Chữ số cuối là 5, nên 35 CHIA HẾT cho 5.'),
        lt(2, 1, 'Số 52 có chia hết cho 5 không? Vì sao?',
           'Chữ số cuối là 2, không phải 0 cũng không phải 5, nên 52 KHÔNG chia hết cho 5.'),
        lt(3, 1, 'Số 270 có chia hết cho 5 không?',
           'Chữ số cuối là 0, nên 270 CHIA HẾT cho 5.'),
        lt(4, 2, 'Trong ba số 145 ; 132 ; 500, những số nào chia hết cho 5?',
           'Nhìn chữ số cuối: 145 cuối là 5 (chia hết), 132 cuối là 2 (không), 500 '
           'cuối là 0 (chia hết). Vậy 145 và 500 chia hết cho 5.'),
        lt(5, 2, 'Số 64 có chia hết cho 2 không, có chia hết cho 5 không?',
           'Chữ số cuối là 4: chẵn nên CHIA HẾT cho 2; nhưng không phải 0 hay 5 nên '
           'KHÔNG chia hết cho 5.'),
        lt(6, 2, 'Vì sao phần tròn chục của một số luôn chia hết cho 5?',
           'Vì mọi số tròn chục đều là mấy lần 10, mà 10 = 5 × 2 nên 10 chia hết cho '
           '5. Bao nhiêu lần 10 thì vẫn chia hết cho 5.'),
        lt(7, 2, 'Viết một số có ba chữ số chia hết cho 5 và có chữ số hàng trăm là 4.',
           'Ví dụ 405 hoặc 450 — chữ số cuối phải là 0 hoặc 5.'),
        lt(8, 3, 'Từ ba chữ số 2 ; 5 ; 7 hãy viết một số có ba chữ số chia hết cho 5, '
                 'dùng mỗi chữ số đúng một lần.',
           'Chữ số cuối phải là 0 hoặc 5 — trong ba chữ số chỉ có 5. Đặt 5 ở cuối: '
           'được 275 hoặc 725.'),
        lt(9, 3, 'Có bao nhiêu số có hai chữ số chia hết cho 5?',
           'Các số đó là 10, 15, 20, 25, … , 95. Từ 10 đến 95 cách đều 5, có '
           '(95 − 10) : 5 + 1 = 18 số.'),
        q_tf(1, 'Số có tận cùng là 5 thì chia hết cho 5.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Số 52 chia hết cho 5 vì trong số đó có chữ số 5.', False,
             'SAI — chỉ xét chữ số cuối. Chữ số cuối của 52 là 2.'),
        q_mcq(3, 'Số nào dưới đây CHIA HẾT cho 5?',
              ['A. 340', 'B. 341', 'C. 342'], 'A. 340',
              'Chữ số cuối của 340 là 0.'),
        q_mcq(4, 'Chữ số cuối của một số chia hết cho 5 phải là:',
              ['A. 0 hoặc 5', 'B. 0, 2, 4, 6 hoặc 8', 'C. 5 mà thôi'],
              'A. 0 hoặc 5', 'Hai chữ số ấy, không có chữ số nào khác.'),
        q_mcq(5, 'Số 64 chia hết cho số nào dưới đây?',
              ['A. chỉ chia hết cho 2', 'B. chỉ chia hết cho 5',
               'C. chia hết cho cả 2 và 5'],
              'A. chỉ chia hết cho 2',
              'Chữ số cuối là 4: chẵn nên chia hết cho 2, nhưng không phải 0 hay 5.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ④ B52 · CHIA HẾT CHO CẢ 2 VÀ CHO 5
# ═══════════════════════════════════════════════════════════════════════════
# Bài rất ngắn về nội dung, nhưng đáng đứng riêng: nó dạy một CÁCH NGHĨ — muốn thoả
# hai điều kiện cùng lúc thì tìm phần chung của hai danh sách. Bé gặp lại lối này ở
# bội chung, ước chung sau này.
B52 = bai(
    52, 'CHIA HẾT CHO CẢ 2 VÀ CHO 5 — PHẦN CHUNG CỦA HAI DẤU HIỆU',
    'Dạng gốc: SỐ 3.3 mức Lớp 4 — Số chia hết đồng thời cho 2 và cho 5, suy ra từ '
    'phần chung của hai danh sách chữ số tận cùng.',
    'Con đã có hai dấu hiệu rồi: chia hết cho 2 thì tận cùng là 0, 2, 4, 6, 8; chia '
    'hết cho 5 thì tận cùng là 0 hoặc 5. Hôm nay con hỏi một câu mới: số nào thoả '
    'CẢ HAI cùng lúc? Cách trả lời câu này con sẽ còn dùng lại rất nhiều lần.',
    LUI_CHIA,
    video(
        ['Tìm được phần chung của hai danh sách chữ số tận cùng.',
         'Nói được số chia hết cho cả 2 và cho 5 là số có tận cùng bằng 0.',
         'Hiểu vì sao chỉ còn đúng một chữ số thoả cả hai điều kiện.'],
        ['Đề bài: Trong các số 270 ; 275 ; 264, số nào chia hết cho CẢ 2 và 5?',
         'Viết ra hai danh sách',
         'Chia hết cho 2 thì tận cùng là 0, 2, 4, 6, 8.',
         'Chia hết cho 5 thì tận cùng là 0 hoặc 5.',
         'Tìm phần chung',
         'Chữ số nào có mặt ở CẢ HAI danh sách? Chỉ có số 0.',
         'Vậy số chia hết cho cả 2 và 5 phải có tận cùng bằng 0.',
         'Xét từng số',
         '270 tận cùng là 0 — thoả cả hai. 275 tận cùng là 5 — chỉ chia hết cho 5. '
         '264 tận cùng là 4 — chỉ chia hết cho 2.',
         'Đáp số: chỉ có 270 chia hết cho cả 2 và cho 5.'],
        ['Có bạn nói: "Số 275 chia hết cho cả 2 và 5, vì nó chia hết cho 5 rồi mà lại '
         'còn to nữa."',
         'Gợi ý 1: Chia hết cho 5 thì đúng rồi. Nhưng chia hết cho 2 thì phải tận '
         'cùng là mấy?',
         'Gợi ý 2: Chữ số cuối của 275 là 5. Số 5 có chẵn không?',
         'Chữa: 275 tận cùng là 5, mà 5 là số lẻ nên KHÔNG chia hết cho 2. Phải thoả '
         'ĐỦ CẢ HAI điều kiện mới được, thoả một cái thì chưa đủ.'],
        ['Viết ra giấy hai hàng chữ số rồi bảo con khoanh chữ số nào có mặt ở cả hai '
         'hàng. Con tự tìm ra số 0 sẽ nhớ lâu hơn nghe kể.',
         'Đây là bài dạy cách nghĩ "phần chung", con sẽ gặp lại ở lớp trên. Bố mẹ '
         'nhấn giúp: thoả một điều kiện chưa đủ, phải thoả hết.'],
    ),
    [
        lt(1, 1, 'Số 270 — số neo của chương. Nó có chia hết cho cả 2 và cho 5 không? '
                 'Vì sao?',
           'Tận cùng là 0. Chữ số 0 vừa chẵn (chia hết cho 2) vừa thuộc nhóm 0 hoặc 5 '
           '(chia hết cho 5), nên 270 chia hết cho CẢ HAI.'),
        lt(2, 1, 'Số 275 có chia hết cho cả 2 và cho 5 không?',
           'Tận cùng là 5: chia hết cho 5 nhưng KHÔNG chia hết cho 2 (vì 5 lẻ). Vậy '
           'không thoả cả hai.'),
        lt(3, 1, 'Một số chia hết cho cả 2 và cho 5 thì chữ số tận cùng của nó là mấy?',
           'Bằng 0 — đó là chữ số duy nhất có mặt trong cả hai danh sách.'),
        lt(4, 2, 'Trong bốn số 130 ; 135 ; 142 ; 200, những số nào chia hết cho cả 2 '
                 'và cho 5?',
           'Số có tận cùng bằng 0: đó là 130 và 200.'),
        lt(5, 2, 'Số 640 chia hết cho những số nào trong hai số 2 và 5?',
           'Tận cùng là 0 nên chia hết cho CẢ 2 và 5.'),
        lt(6, 2, 'Vì sao trong hai danh sách chữ số tận cùng chỉ còn đúng một chữ số '
                 'chung?',
           'Danh sách của 2 là 0, 2, 4, 6, 8; danh sách của 5 là 0 và 5. So hai danh '
           'sách thì chỉ có chữ số 0 có mặt ở cả hai.'),
        lt(7, 2, 'Viết một số có ba chữ số chia hết cho cả 2 và cho 5, có chữ số hàng '
                 'trăm là 8.',
           'Ví dụ 800, 810, 850 — miễn chữ số cuối bằng 0.'),
        lt(8, 3, 'Từ ba chữ số 0 ; 3 ; 7 hãy viết một số có ba chữ số chia hết cho cả '
                 '2 và cho 5, dùng mỗi chữ số đúng một lần.',
           'Chữ số cuối phải là 0, nên đặt 0 ở cuối: được 370 hoặc 730.'),
        lt(9, 3, 'Có bao nhiêu số có hai chữ số chia hết cho cả 2 và cho 5?',
           'Các số tận cùng bằng 0 có hai chữ số: 10, 20, 30, 40, 50, 60, 70, 80, 90 '
           '— tất cả 9 số.'),
        q_tf(1, 'Số chia hết cho cả 2 và cho 5 thì có tận cùng bằng 0.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Số 135 chia hết cho cả 2 và cho 5.', False,
             'SAI — tận cùng là 5, lẻ, nên không chia hết cho 2.'),
        q_mcq(3, 'Số nào dưới đây chia hết cho CẢ 2 và 5?',
              ['A. 490', 'B. 495', 'C. 494'], 'A. 490',
              'Chỉ 490 có tận cùng bằng 0.'),
        q_mcq(4, 'Chữ số nào có mặt trong cả hai danh sách tận cùng của 2 và của 5?',
              ['A. 0', 'B. 5', 'C. 2'], 'A. 0',
              'Danh sách của 2 là 0, 2, 4, 6, 8; của 5 là 0 và 5.'),
        q_mcq(5, 'Một số tận cùng bằng 5 thì:',
              ['A. chia hết cho 5 nhưng không chia hết cho 2',
               'B. chia hết cho cả 2 và 5',
               'C. không chia hết cho số nào trong hai số đó'],
              'A. chia hết cho 5 nhưng không chia hết cho 2',
              'Chữ số 5 là số lẻ nên không chia hết cho 2.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ B10 · DẤU HIỆU CHIA HẾT CHO 9  (mã cũ, nội dung viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# ⚠ ĐÂY LÀ BÀI KHÓ NHẤT CHƯƠNG, và cũng là chỗ luật 10 của bác nặng nhất. Bài cũ chỉ
# NÊU dấu hiệu "cộng các chữ số lại". Nay phải nói được VÌ SAO, và nói bằng số cụ thể
# chứ không bằng chữ nghĩa:
#     270 = 2 × 100 + 7 × 10
#     100 = 99 + 1  và  10 = 9 + 1
#     nên 270 = (2 × 99 + 7 × 9) + (2 + 7)
# Ngoặc đầu luôn chia hết cho 9 (vì 9 và 99 đều chia hết cho 9), nên chỉ ngoặc sau —
# tức TỔNG CÁC CHỮ SỐ — mới quyết định. Đúng một lối nghĩ với hai bài trước: tách ra
# phần chắc chắn chia hết và phần còn lại.
# Dạy cho 9 TRƯỚC cho 3, vì với 9 thì con số khớp đẹp (2 + 7 + 0 = 9) nên bé thấy
# ngay; sang bài 3 thì chỉ còn là cùng lối ấy với số nhỏ hơn.
B10 = bai(
    10, 'DẤU HIỆU CHIA HẾT CHO 9 — VÌ SAO LẠI CỘNG CÁC CHỮ SỐ',
    'Dạng gốc: SỐ 3.4 mức Lớp 4 — Dấu hiệu chia hết cho 9, kèm chứng minh bằng cách '
    'tách 10 = 9 + 1 và 100 = 99 + 1.',
    'Ba bài vừa rồi con chỉ nhìn chữ số cuối là xong. Nhưng với số 9 thì cách ấy '
    'không dùng được — con phải cộng TẤT CẢ các chữ số lại. Nghe rất lạ, nên hôm nay '
    'con sẽ xem vì sao lại thế. Hiểu được chỗ này thì con không bao giờ quên dấu hiệu.',
    LUI_CHIA,
    video(
        ['Nói được dấu hiệu: tổng các chữ số chia hết cho 9 thì số đó chia hết cho 9.',
         'Giải thích được vì sao lại cộng các chữ số, dựa vào 10 = 9 + 1.',
         'Xét được một số bất kỳ có chia hết cho 9 hay không.'],
        ['Đề bài: Số 270 có chia hết cho 9 không? Vì sao lại đi cộng các chữ số?',
         'Viết số ra theo hàng',
         '270 = 2 × 100 + 7 × 10 + 0.',
         'Tách 100 và 10 ra',
         '100 = 99 + 1, và 10 = 9 + 1.',
         'Nên 270 = 2 × 99 + 2 + 7 × 9 + 7 + 0.',
         'Gom lại thành hai phần',
         'Phần một là 2 × 99 + 7 × 9 — phần này luôn chia hết cho 9, vì 9 và 99 đều '
         'chia hết cho 9.',
         'Phần hai là 2 + 7 + 0 — đúng bằng tổng các chữ số.',
         'Vậy chỉ phần hai quyết định',
         '2 + 7 + 0 = 9, mà 9 chia hết cho 9, nên 270 chia hết cho 9.',
         'Đáp số: 270 chia hết cho 9. Ta cộng các chữ số vì phần còn lại của số đã '
         'chia hết cho 9 sẵn rồi, không bao giờ làm thừa.'],
        ['Có bạn nhìn số 72 rồi nói: "Số 72 không chia hết cho 9, vì chữ số cuối là 2 '
         'mà 2 không chia hết cho 9."',
         'Gợi ý 1: Với số 9 thì con có nhìn chữ số cuối không, hay làm cách khác?',
         'Gợi ý 2: Con cộng TẤT CẢ các chữ số của 72 lại xem được bao nhiêu.',
         'Chữa: 7 + 2 = 9, mà 9 chia hết cho 9, nên 72 CHIA HẾT cho 9. Cách nhìn chữ '
         'số cuối chỉ dùng cho 2 và cho 5 thôi.'],
        ['Cho con một số bất kỳ rồi bảo con cộng các chữ số lại, sau đó bấm máy tính '
         'chia thử. Làm vài lần con sẽ tin là dấu hiệu luôn đúng.',
         'Nếu con hỏi "vì sao lại cộng", bố mẹ nói lại đúng một câu trong video: vì '
         '10 hơn 9 đúng một đơn vị, nên mỗi chục để lại đúng một đơn vị.'],
    ),
    [
        lt(1, 1, 'Số 270 — số neo của chương. Tổng các chữ số của nó bằng bao nhiêu, '
                 'và 270 có chia hết cho 9 không?',
           '2 + 7 + 0 = 9. Số 9 chia hết cho 9, nên 270 CHIA HẾT cho 9.'),
        lt(2, 1, 'Số 72 có chia hết cho 9 không? Vì sao?',
           '7 + 2 = 9, chia hết cho 9, nên 72 CHIA HẾT cho 9.'),
        lt(3, 1, 'Số 43 có chia hết cho 9 không?',
           '4 + 3 = 7, mà 7 không chia hết cho 9, nên 43 KHÔNG chia hết cho 9.'),
        lt(4, 2, 'Trong ba số 108 ; 235 ; 459, những số nào chia hết cho 9?',
           'Cộng chữ số: 108 được 9 (chia hết), 235 được 10 (không), 459 được 18 '
           '(chia hết cho 9). Vậy 108 và 459.'),
        lt(5, 2, 'Bạn Bình nói: "Số 63 không chia hết cho 9 vì chữ số cuối là 3." Bạn '
                 'nói đúng hay sai? Số 63 có chia hết cho 9 không?',
           'SAI. Với 9 phải cộng các chữ số: 6 + 3 = 9, chia hết cho 9. Vậy 63 CHIA '
           'HẾT cho 9.'),
        lt(6, 2, 'Vì sao phần 2 × 99 + 7 × 9 trong cách tách số 270 luôn chia hết cho 9?',
           'Vì 9 chia hết cho 9 và 99 cũng chia hết cho 9 (99 = 9 × 11). Bao nhiêu '
           'lần 9 hay bao nhiêu lần 99 thì vẫn chia hết cho 9.'),
        lt(7, 2, 'Tìm chữ số thích hợp điền vào ô trống để số 4 ô 5 chia hết cho 9.',
           'Tổng phải chia hết cho 9: 4 + ô + 5 = 9 + ô. Muốn chia hết cho 9 thì ô = 0 '
           'hoặc ô = 9. Vậy được 405 hoặc 495.'),
        lt(8, 3, 'Từ bốn chữ số 1 ; 2 ; 3 ; 4 hãy chọn ba chữ số để viết một số có ba '
                 'chữ số chia hết cho 9.',
           'Tổng ba chữ số phải chia hết cho 9. Thử: 2 + 3 + 4 = 9 — được. Vậy viết '
           '234 (hoặc 243, 324, 342, 423, 432).'),
        lt(9, 3, 'Số 1 989 có chia hết cho 9 không? Nếu có thì thương bằng bao nhiêu?',
           '1 + 9 + 8 + 9 = 27, mà 27 chia hết cho 9, nên 1 989 chia hết cho 9. '
           'Thương là 1 989 : 9 = 221.'),
        q_tf(1, 'Muốn biết một số có chia hết cho 9 không, ta cộng tất cả các chữ số '
                'của nó lại.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Số 63 không chia hết cho 9 vì chữ số cuối là 3.', False,
             'SAI — 6 + 3 = 9 nên 63 chia hết cho 9. Nhìn chữ số cuối chỉ dùng cho 2 và 5.'),
        q_mcq(3, 'Số nào dưới đây CHIA HẾT cho 9?',
              ['A. 279', 'B. 271', 'C. 275'], 'A. 279',
              '2 + 7 + 9 = 18, chia hết cho 9.'),
        q_mcq(4, 'Tổng các chữ số của 270 bằng:',
              ['A. 9', 'B. 27', 'C. 10'], 'A. 9', '2 + 7 + 0 = 9.'),
        q_mcq(5, 'Vì sao xét chia hết cho 9 thì lại cộng các chữ số?',
              ['A. Vì 10 hơn 9 đúng một đơn vị, nên mỗi chục để lại đúng một đơn vị',
               'B. Vì 9 là chữ số lớn nhất',
               'C. Vì cộng cho nhanh hơn chia'],
              'A. Vì 10 hơn 9 đúng một đơn vị, nên mỗi chục để lại đúng một đơn vị',
              '10 = 9 + 1 và 100 = 99 + 1, phần 9 và 99 đã chia hết cho 9 sẵn.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ B53 · DẤU HIỆU CHIA HẾT CHO 3
# ═══════════════════════════════════════════════════════════════════════════
# Cùng lối chứng minh với bài trước — 9 và 99 chia hết cho 3 y như chúng chia hết cho
# 9. Nên bài này ngắn hơn, và dành nửa sau cho chỗ bé nhầm nhiều nhất: chia hết cho 9
# thì CHẮC CHẮN chia hết cho 3, nhưng chiều ngược lại KHÔNG đúng.
B53 = bai(
    53, 'DẤU HIỆU CHIA HẾT CHO 3 — VÀ KHÁC CHO 9 CHỖ NÀO',
    'Dạng gốc: SỐ 3.5 mức Lớp 4 — Dấu hiệu chia hết cho 3, và quan hệ một chiều giữa '
    'chia hết cho 9 và chia hết cho 3.',
    'Bài trước con đã hiểu vì sao xét số 9 thì phải cộng các chữ số. Hôm nay con thử '
    'đúng lối ấy với số 3 — và sẽ thấy nó lại đúng, vì 9 với 99 cũng chia hết cho 3. '
    'Rồi con học một chỗ rất hay nhầm: hai dấu hiệu giống nhau nhưng KHÔNG thay được '
    'cho nhau.',
    LUI_CHIA,
    video(
        ['Nói được dấu hiệu: tổng các chữ số chia hết cho 3 thì số đó chia hết cho 3.',
         'Giải thích được vì sao lối nghĩ của bài 9 dùng lại được cho 3.',
         'Biết số chia hết cho 9 thì chắc chắn chia hết cho 3, nhưng ngược lại thì không.'],
        ['Đề bài: Số 270 có chia hết cho 3 không? Còn số 12 thì sao — nó có chia hết '
         'cho 3 không, có chia hết cho 9 không?',
         'Xét số 270',
         'Tổng các chữ số: 2 + 7 + 0 = 9. Số 9 chia hết cho 3, nên 270 chia hết cho 3.',
         'Vì sao lại cộng chữ số như với số 9',
         'Vì 270 tách được thành 2 × 99 + 7 × 9 rồi cộng 2 + 7 + 0. Mà 9 và 99 đều '
         'chia hết cho 3, nên phần trước không làm thừa, chỉ tổng chữ số quyết định.',
         'Xét số 12',
         'Tổng chữ số là 1 + 2 = 3. Số 3 chia hết cho 3, nên 12 chia hết cho 3.',
         'Nhưng 3 KHÔNG chia hết cho 9, nên 12 KHÔNG chia hết cho 9.',
         'Rút ra quan hệ một chiều',
         'Số chia hết cho 9 thì chắc chắn chia hết cho 3, vì 9 đã chia hết cho 3. '
         'Nhưng chia hết cho 3 thì chưa chắc chia hết cho 9 — số 12 là ví dụ.',
         'Đáp số: 270 chia hết cho cả 3 và 9; còn 12 chỉ chia hết cho 3.'],
        ['Có bạn nói: "Số 12 chia hết cho 3 rồi, nên nó cũng chia hết cho 9."',
         'Gợi ý 1: Con cộng chữ số của 12 xem được mấy?',
         'Gợi ý 2: Được 3. Số 3 có chia hết cho 9 không?',
         'Chữa: 3 không chia hết cho 9, nên 12 KHÔNG chia hết cho 9. Chiều đúng là '
         'chiều ngược lại: chia hết cho 9 thì mới chắc chắn chia hết cho 3.'],
        ['Hỏi con hai câu liền nhau về cùng một số: "chia hết cho 3 không?" rồi "chia '
         'hết cho 9 không?" Con sẽ tự thấy hai câu không phải lúc nào cũng cùng đáp án.',
         'Chỗ nhầm phổ biến nhất là gộp hai dấu hiệu làm một. Bố mẹ nhấn giúp: 9 chia '
         'hết cho 3, nên đi từ 9 sang 3 thì được; đi ngược lại thì không.'],
    ),
    [
        lt(1, 1, 'Số 270 — số neo của chương. Tổng các chữ số bằng bao nhiêu và 270 '
                 'có chia hết cho 3 không?',
           '2 + 7 + 0 = 9. Số 9 chia hết cho 3, nên 270 CHIA HẾT cho 3.'),
        lt(2, 1, 'Số 12 có chia hết cho 3 không? Có chia hết cho 9 không?',
           '1 + 2 = 3. Số 3 chia hết cho 3 nên 12 chia hết cho 3; nhưng 3 không chia '
           'hết cho 9 nên 12 KHÔNG chia hết cho 9.'),
        lt(3, 1, 'Số 25 có chia hết cho 3 không?',
           '2 + 5 = 7, mà 7 không chia hết cho 3, nên 25 KHÔNG chia hết cho 3.'),
        lt(4, 2, 'Trong ba số 123 ; 145 ; 306, những số nào chia hết cho 3?',
           'Cộng chữ số: 123 được 6 (chia hết cho 3), 145 được 10 (không), 306 được 9 '
           '(chia hết cho 3). Vậy 123 và 306.'),
        lt(5, 2, 'Số 45 chia hết cho 3, có chia hết cho 9 không? Còn số 15 thì sao?',
           '45 có tổng chữ số 9, chia hết cho 9 nên 45 chia hết cho cả 3 và 9. '
           '15 có tổng chữ số 6, chia hết cho 3 nhưng không chia hết cho 9.'),
        lt(6, 2, 'Vì sao số chia hết cho 9 thì chắc chắn chia hết cho 3?',
           'Vì 9 = 3 × 3, tức 9 đã chia hết cho 3. Cái gì chia được thành các nhóm 9 '
           'thì mỗi nhóm 9 lại tách được thành 3 nhóm 3, nên vẫn chia hết cho 3.'),
        lt(7, 2, 'Tìm chữ số thích hợp điền vào ô trống để số 2 ô 4 chia hết cho 3.',
           'Tổng là 2 + ô + 4 = 6 + ô. Muốn chia hết cho 3 thì ô = 0, 3, 6 hoặc 9. '
           'Vậy được 204, 234, 264 hoặc 294.'),
        lt(8, 3, 'Tìm một số có hai chữ số vừa chia hết cho 3 vừa chia hết cho 5.',
           'Chia hết cho 5 thì tận cùng 0 hoặc 5; chia hết cho 3 thì tổng chữ số chia '
           'hết cho 3. Ví dụ 15 (tổng 6) hoặc 30 (tổng 3).'),
        lt(9, 3, 'Số 348 chia hết cho 3 hay cho 9, hay cho cả hai? Giải thích.',
           '3 + 4 + 8 = 15. Số 15 chia hết cho 3 nhưng không chia hết cho 9. Vậy 348 '
           'chia hết cho 3 và KHÔNG chia hết cho 9.'),
        q_tf(1, 'Số có tổng các chữ số chia hết cho 3 thì chia hết cho 3.', True,
             'Đáp án: ĐÚNG.'),
        q_tf(2, 'Số nào chia hết cho 3 thì cũng chia hết cho 9.', False,
             'SAI — số 12 chia hết cho 3 nhưng không chia hết cho 9.'),
        q_mcq(3, 'Số nào dưới đây chia hết cho 3 nhưng KHÔNG chia hết cho 9?',
              ['A. 12', 'B. 18', 'C. 27'], 'A. 12',
              'Tổng chữ số của 12 là 3: chia hết cho 3, không chia hết cho 9.'),
        q_mcq(4, 'Tổng các chữ số của 123 bằng:',
              ['A. 6', 'B. 5', 'C. 123'], 'A. 6', '1 + 2 + 3 = 6.'),
        q_mcq(5, 'Số chia hết cho 9 thì:',
              ['A. chắc chắn chia hết cho 3', 'B. chắc chắn chia hết cho 2',
               'C. chắc chắn chia hết cho 5'],
              'A. chắc chắn chia hết cho 3', 'Vì 9 = 3 × 3, tức 9 đã chia hết cho 3.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑦ B11 · PHÉP CHIA CÓ DƯ  (mã cũ, nội dung viết lại)
# ═══════════════════════════════════════════════════════════════════════════
# Bài cũ gộp phép chia có dư VỚI bài toán thừa - thiếu. Nay tách: ở đây chỉ dựng công
# thức và giải thích từng chữ trong nó; bài sau mới đem đi dùng.
# Luật 10 của bác nằm đúng ở chỗ "vì sao số dư luôn nhỏ hơn số chia" — câu ấy trước
# nay chỉ được nêu như một quy tắc phải nhớ. Hình `nhom_deu` trả lời nó trong một
# giây: nếu phần thừa còn đủ xếp một nhóm nữa thì nó đã vào nhóm rồi.
B11 = bai(
    11, 'PHÉP CHIA CÓ DƯ — VÌ SAO SỐ DƯ LUÔN NHỎ HƠN SỐ CHIA',
    'Dạng gốc: SỐ 3.6 mức Lớp 4 — Công thức số bị chia bằng số chia nhân thương cộng '
    'số dư, và điều kiện số dư nhỏ hơn số chia.',
    'Con đã biết chia còn thừa thì phần thừa gọi là số dư. Hôm nay con viết được cả '
    'phép chia thành một công thức, gọi tên từng chữ trong đó, và hiểu vì sao số dư '
    'không bao giờ được bằng hay lớn hơn số chia.',
    LUI_CHIA_DU,
    video(
        ['Viết được công thức: số bị chia = số chia × thương + số dư.',
         'Gọi đúng tên từng thành phần trong công thức.',
         'Giải thích được vì sao số dư luôn nhỏ hơn số chia.'],
        ['Đề bài: Có 14 cái bánh, xếp vào các hộp, mỗi hộp 4 cái. Xếp được mấy hộp, '
         'thừa mấy cái? Viết phép chia rồi thử lại.',
         'Xếp thử',
         'Xếp 14 cái thành từng nhóm 4 cái: được 3 hộp, còn thừa 2 cái.',
         'Viết phép chia',
         '14 : 4 = 3 (dư 2). Ở đây 14 là số bị chia, 4 là số chia, 3 là thương, 2 là '
         'số dư.',
         'Thử lại bằng công thức',
         'Số bị chia = số chia × thương + số dư.',
         '4 × 3 + 2 = 12 + 2 = 14. Đúng bằng số ban đầu, vậy phép chia không sai.',
         'Vì sao số dư phải nhỏ hơn số chia',
         'Phần thừa là 2, mà mỗi hộp cần 4 cái nên 2 cái không đủ xếp thêm hộp nào. '
         'Nếu phần thừa mà bằng 4 hay hơn 4 thì ta đã xếp thêm được một hộp nữa rồi.',
         'Đáp số: xếp được 3 hộp, thừa 2 cái. Số dư 2 nhỏ hơn số chia 4.'],
        ['Có bạn làm phép 14 : 4 rồi viết: "14 : 4 = 2 (dư 6)."',
         'Gợi ý 1: Con thử lại xem: 4 × 2 + 6 có bằng 14 không?',
         'Gợi ý 2: Bằng 14 thật đấy. Nhưng con nhìn số dư 6 và số chia 4 xem — số dư '
         'có nhỏ hơn số chia không?',
         'Chữa: số dư 6 lớn hơn số chia 4, nghĩa là vẫn còn xếp thêm được một hộp nữa. '
         'Phải viết 14 : 4 = 3 (dư 2). Thử lại đúng thì chưa đủ, số dư còn phải nhỏ '
         'hơn số chia.'],
        ['Đưa con một nắm hạt và một cái khay chia ô. Bảo con xếp cho tới khi không '
         'xếp thêm được nữa — phần còn lại chính là số dư.',
         'Con hay quên điều kiện số dư nhỏ hơn số chia. Bố mẹ hỏi lại một câu: "Chỗ '
         'thừa ấy còn xếp thêm được một nhóm nữa không?"'],
    ),
    [
        lt(1, 1, 'Có 14 cái bánh — đúng bài trong video. Xếp mỗi hộp 4 cái thì được '
                 'mấy hộp và thừa mấy cái?',
           'Được 3 hộp, thừa 2 cái. Phép chia: 14 : 4 = 3 (dư 2).'),
        lt(2, 1, 'Trong phép chia 14 : 4 = 3 (dư 2), thương bằng bao nhiêu và số dư '
                 'bằng bao nhiêu?',
           'Thương là 3, số dư là 2.'),
        lt(3, 1, 'Thử lại phép chia 14 : 4 = 3 (dư 2) bằng công thức. Kết quả bằng bao nhiêu?',
           'Số chia × thương + số dư = 4 × 3 + 2 = 14. Đúng bằng số bị chia.'),
        lt(4, 2, 'Thực hiện phép chia 29 : 6 rồi thử lại.',
           '29 : 6 = 4 (dư 5). Thử lại: 6 × 4 + 5 = 24 + 5 = 29. Số dư 5 nhỏ hơn số chia 6.'),
        lt(5, 2, 'Bạn Hùng viết: "23 : 5 = 3 (dư 8)." Bạn làm sai ở đâu? Kết quả đúng '
                 'là bao nhiêu?',
           'Số dư 8 LỚN HƠN số chia 5, nghĩa là còn xếp thêm được nhóm nữa. Đúng phải '
           'là 23 : 5 = 4 (dư 3).'),
        lt(6, 2, 'Trong một phép chia cho 7, số dư lớn nhất có thể là bao nhiêu?',
           'Số dư phải nhỏ hơn số chia, mà số chia là 7, nên số dư lớn nhất là 6.'),
        lt(7, 2, 'Một phép chia có số chia là 5, thương là 7, số dư là 3. Số bị chia '
                 'bằng bao nhiêu?',
           'Số bị chia = số chia × thương + số dư = 5 × 7 + 3 = 35 + 3 = 38.'),
        lt(8, 3, 'Một phép chia có số bị chia là 47, thương là 6, số dư là 5. Số chia '
                 'bằng bao nhiêu?',
           'Từ công thức: 47 = số chia × 6 + 5, nên số chia × 6 = 42, số chia = 7. '
           'Kiểm lại: số dư 5 nhỏ hơn 7, hợp lệ.'),
        lt(9, 3, 'Tìm một số bé hơn 40, chia cho 6 thì dư 4, và chia cho 5 thì dư 1.',
           'Số chia 6 dư 4: 4, 10, 16, 22, 28, 34. Trong đó số chia 5 dư 1: 16 (16 : 5 '
           '= 3 dư 1). Vậy số cần tìm là 16.'),
        q_tf(1, 'Trong một phép chia có dư, số dư luôn nhỏ hơn số chia.', True,
             'Đáp án: ĐÚNG — nếu bằng hoặc lớn hơn thì còn chia thêm được.'),
        q_tf(2, 'Phép chia 23 : 5 = 3 (dư 8) là phép chia đúng.', False,
             'SAI — số dư 8 lớn hơn số chia 5. Đúng phải là 4 dư 3.'),
        q_mcq(3, 'Công thức thử lại phép chia có dư là:',
              ['A. số chia × thương + số dư', 'B. số chia + thương × số dư',
               'C. thương × số dư + số chia'],
              'A. số chia × thương + số dư', 'Nhân trước rồi mới cộng số dư.'),
        q_mcq(4, 'Trong phép chia cho 4, số dư lớn nhất có thể là:',
              ['A. 3', 'B. 4', 'C. 5'], 'A. 3', 'Số dư phải nhỏ hơn số chia là 4.'),
        q_mcq(5, 'Vì sao số dư không được bằng số chia?',
              ['A. Vì khi đó còn xếp thêm được một nhóm nữa',
               'B. Vì số dư phải là số lẻ',
               'C. Vì số chia luôn lớn hơn thương'],
              'A. Vì khi đó còn xếp thêm được một nhóm nữa',
              'Đủ một nhóm nữa thì phải xếp vào nhóm, không để thừa.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑧ B54 · BÀI TOÁN THỪA - THIẾU
# ═══════════════════════════════════════════════════════════════════════════
# Bài này KHÔNG dạy công thức mới — nó dạy đúng một việc: sau khi chia xong, đọc số
# dư thế nào cho đúng với câu hỏi thật. Cùng một phép chia mà hỏi "được mấy xe đầy"
# thì lấy thương, hỏi "cần mấy xe" thì phải cộng thêm một. Đó là chỗ bé sai nhiều
# nhất, và sai không phải vì tính sai.
B54 = bai(
    54, 'BÀI TOÁN THỪA - THIẾU — SỐ DƯ ĐÒI THÊM MỘT CHỖ NỮA',
    'Dạng gốc: SỐ 3.7 mức Lớp 4 — Bài toán có lời văn dùng phép chia có dư, phân biệt '
    'lấy thương với lấy thương cộng một.',
    'Bài trước con đã chia thành thạo và biết số dư là gì. Nhưng khi gặp bài toán có '
    'lời văn thì phải đọc số dư cho đúng câu hỏi. Cùng một phép chia, hỏi khác nhau '
    'thì đáp số khác nhau — hôm nay con học đúng chỗ đó.',
    LUI_CHIA_DU,
    video(
        ['Giải được bài toán lời văn bằng phép chia có dư.',
         'Biết khi nào lấy thương, khi nào phải cộng thêm 1.',
         'Đọc lại câu hỏi của đề trước khi viết đáp số.'],
        ['Đề bài: Lớp có 25 bạn đi tham quan. Mỗi xe chở được 6 bạn. Hỏi cần ít nhất '
         'bao nhiêu xe để chở hết cả lớp?',
         'Chia thử',
         '25 : 6 = 4 (dư 1). Nghĩa là xếp đầy được 4 xe, còn thừa 1 bạn.',
         'Đọc lại câu hỏi',
         'Đề hỏi cần ít nhất bao nhiêu xe để chở HẾT cả lớp.',
         'Bạn thừa ra vẫn phải đi, nên vẫn phải có thêm một xe nữa cho bạn ấy.',
         'Kết luận',
         'Số xe cần là 4 + 1 = 5 xe.',
         'Nếu đề hỏi khác',
         'Nếu đề hỏi có mấy xe chở ĐẦY 6 bạn thì đáp số chỉ là 4 xe, không cộng thêm.',
         'Đáp số: cần ít nhất 5 xe.'],
        ['Có bạn tính 25 : 6 = 4 dư 1 rồi viết luôn: "Đáp số: 4 xe."',
         'Gợi ý 1: Con tính đúng rồi. Nhưng còn 1 bạn thừa ra thì bạn ấy đi bằng gì?',
         'Gợi ý 2: Bạn ấy cũng phải đi tham quan chứ. Vậy có đủ 4 xe không?',
         'Chữa: phải thêm một xe nữa cho bạn thừa ra, nên đáp số là 5 xe. Chia xong '
         'thì đọc lại câu hỏi rồi mới viết đáp số.'],
        ['Hỏi con những câu đời thường: "Nhà mình 5 người, mỗi mâm ngồi 4, cần mấy '
         'mâm?" Con sẽ tự thấy phải kê thêm mâm nữa.',
         'Con tính đúng mà đáp số sai là chuyện rất hay gặp ở dạng này. Bố mẹ chỉ cần '
         'hỏi: "Phần thừa ra thì sao?"'],
    ),
    [
        lt(1, 1, 'Lớp có 25 bạn — đúng bài trong video. Mỗi xe chở 6 bạn. Chia 25 cho '
                 '6 được thương và số dư bằng bao nhiêu?',
           '25 : 6 = 4 (dư 1). Thương là 4, số dư là 1.'),
        lt(2, 1, 'Vẫn bài trên. Cần ít nhất bao nhiêu xe để chở HẾT 25 bạn?',
           'Xếp đầy được 4 xe, còn 1 bạn thừa vẫn phải đi nên thêm 1 xe nữa. Cần 5 xe.'),
        lt(3, 1, 'Vẫn bài trên. Có bao nhiêu xe chở ĐẦY đủ 6 bạn?',
           'Chỉ 4 xe chở đầy 6 bạn; xe thứ năm chỉ có 1 bạn.'),
        lt(4, 2, 'Có 30 quyển vở xếp vào các thùng, mỗi thùng 7 quyển. Cần ít nhất bao '
                 'nhiêu thùng để xếp hết?',
           '30 : 7 = 4 (dư 2). Còn 2 quyển thừa vẫn phải xếp nên thêm 1 thùng. Cần 5 thùng.'),
        lt(5, 2, 'Có 30 quyển vở, mỗi thùng 7 quyển. Xếp được bao nhiêu thùng ĐẦY và '
                 'còn thừa mấy quyển?',
           '30 : 7 = 4 (dư 2). Xếp đầy 4 thùng, thừa 2 quyển.'),
        lt(6, 2, 'Bạn Mai tính 43 : 8 = 5 (dư 3) rồi trả lời "cần 5 hộp để đựng hết 43 '
                 'viên bi". Bạn trả lời đúng chưa? Đáp số đúng là bao nhiêu?',
           'CHƯA đúng. Còn 3 viên thừa vẫn phải đựng nên cần thêm 1 hộp. Đáp số đúng '
           'là 6 hộp.'),
        lt(7, 2, 'Một sợi dây dài 47 mét, cắt thành các đoạn dài 9 mét. Cắt được mấy '
                 'đoạn dài 9 mét và còn thừa bao nhiêu mét?',
           '47 : 9 = 5 (dư 2). Cắt được 5 đoạn, thừa 2 mét. Ở dạng này KHÔNG cộng '
           'thêm, vì 2 mét không đủ thành một đoạn 9 mét.'),
        lt(8, 3, 'Có 100 học sinh xếp hàng, mỗi hàng 8 bạn. Hỏi xếp được mấy hàng đầy, '
                 'và cần bao nhiêu hàng để đủ chỗ cho tất cả?',
           '100 : 8 = 12 (dư 4). Xếp đầy 12 hàng; muốn đủ chỗ cho cả 4 bạn thừa thì '
           'cần 13 hàng.'),
        lt(9, 3, 'Một cửa hàng có 53 kg gạo, đóng vào các bao 6 kg. Hỏi đóng được mấy '
                 'bao đầy, còn thừa mấy ki-lô-gam, và cần mấy bao để đựng hết số gạo?',
           '53 : 6 = 8 (dư 5). Đóng đầy 8 bao, thừa 5 kg. Muốn đựng hết thì cần 9 bao.'),
        q_tf(1, 'Khi bài hỏi "cần ít nhất bao nhiêu xe để chở hết", nếu còn dư thì '
                'phải cộng thêm một xe.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Trong mọi bài toán chia có dư, ta luôn phải cộng thêm 1 vào thương.',
             False,
             'SAI — chỉ cộng khi phần thừa vẫn cần một chỗ. Cắt dây thì phần thừa '
             'không thành đoạn nên không cộng.'),
        q_mcq(3, 'Có 25 bạn, mỗi xe chở 6 bạn. Cần ít nhất bao nhiêu xe?',
              ['A. 5 xe', 'B. 4 xe', 'C. 6 xe'], 'A. 5 xe',
              '25 : 6 = 4 dư 1, bạn thừa vẫn phải đi nên thêm một xe.'),
        q_mcq(4, 'Có 25 bạn, mỗi xe chở 6 bạn. Có bao nhiêu xe chở ĐẦY 6 bạn?',
              ['A. 4 xe', 'B. 5 xe', 'C. 3 xe'], 'A. 4 xe',
              'Thương là 4, xe thứ năm chỉ chở 1 bạn.'),
        q_mcq(5, 'Sợi dây 47 mét cắt thành đoạn 9 mét thì được mấy đoạn?',
              ['A. 5 đoạn', 'B. 6 đoạn', 'C. 4 đoạn'], 'A. 5 đoạn',
              '47 : 9 = 5 dư 2; 2 mét không đủ thành một đoạn nên không cộng thêm.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# ⑨ B12 · CHỮ SỐ TẬN CÙNG CỦA MỘT TÍCH  (mã cũ, giữ chủ đề, viết lại theo khuôn)
# ═══════════════════════════════════════════════════════════════════════════
# Bài khép chương, và cố ý dùng lại đúng lối nghĩ đã chạy suốt: TÁCH RA PHẦN KHÔNG
# ẢNH HƯỞNG. Ở bài cho 2 và cho 5 là "phần tròn chục không làm thừa"; ở đây là "phần
# tròn chục không chạm tới chữ số cuối của tích". Cùng một cách nghĩ, lần thứ tư.
B12 = bai(
    12, 'CHỮ SỐ TẬN CÙNG CỦA MỘT TÍCH — CHỈ HAI CHỮ SỐ CUỐI QUYẾT ĐỊNH',
    'Dạng gốc: SỐ 3.8 mức Lớp 4 — Xác định chữ số tận cùng của một tích mà không cần '
    'nhân hết, dựa vào việc tách thừa số thành phần tròn chục và chữ số đơn vị.',
    'Con đã ba lần dùng một lối nghĩ: tách ra phần chắc chắn không ảnh hưởng, rồi chỉ '
    'xét phần còn lại. Hôm nay con dùng nó lần thứ tư, để biết chữ số cuối của một '
    'phép nhân mà không phải nhân hết cả phép.',
    LUI_NHAN,
    video(
        ['Tìm được chữ số tận cùng của một tích mà không cần nhân hết.',
         'Giải thích được vì sao chỉ hai chữ số cuối của hai thừa số quyết định.',
         'Dùng được điều đó để kiểm tra nhanh một phép nhân.'],
        ['Đề bài: Tích 23 × 17 có chữ số tận cùng là mấy? Tìm mà không nhân hết cả phép.',
         'Tách hai thừa số',
         '23 = 20 + 3 và 17 = 10 + 7.',
         'Nhân ra thành bốn phần',
         '23 × 17 = 20 × 10 + 20 × 7 + 3 × 10 + 3 × 7.',
         'Xem ba phần đầu',
         'Ba phần đầu đều có thừa số 10 hoặc 20, nên đều là số tròn chục — chữ số cuối '
         'của chúng đều bằng 0, không chạm tới chữ số cuối của tích.',
         'Vậy chỉ phần cuối quyết định',
         '3 × 7 = 21, chữ số cuối là 1. Nên tích 23 × 17 có chữ số tận cùng là 1.',
         'Kiểm lại',
         '23 × 17 = 391, đúng là tận cùng bằng 1.',
         'Đáp số: chữ số tận cùng của tích là 1, lấy từ 3 nhân 7 bằng 21.'],
        ['Có bạn nói: "Tích 23 × 17 tận cùng là 21, vì 3 nhân 7 bằng 21."',
         'Gợi ý 1: 21 có mấy chữ số? Câu hỏi đòi bao nhiêu chữ số?',
         'Gợi ý 2: Đề hỏi CHỮ SỐ tận cùng, tức chỉ một chữ số thôi.',
         'Chữa: 3 × 7 = 21, và chữ số tận cùng của 21 là 1. Vậy tích tận cùng là 1, '
         'không phải 21.'],
        ['Bảo con đoán chữ số cuối của một phép nhân rồi mới bấm máy tính kiểm lại. '
         'Đoán đúng vài lần con sẽ thích cách này.',
         'Đây cũng là mẹo kiểm tra bài: nhân xong nhìn chữ số cuối, lệch là biết sai '
         'ngay mà không phải làm lại cả phép.'],
    ),
    [
        lt(1, 1, 'Tích 23 × 17 — đúng phép trong video. Nhân hai chữ số cuối với nhau '
                 'được bao nhiêu, và chữ số tận cùng của tích là mấy?',
           '3 × 7 = 21. Chữ số tận cùng của 21 là 1, nên tích tận cùng bằng 1.'),
        lt(2, 1, 'Tích 34 × 26 có chữ số tận cùng là mấy?',
           '4 × 6 = 24, tận cùng là 4. Vậy tích tận cùng bằng 4.'),
        lt(3, 1, 'Tích 45 × 12 có chữ số tận cùng là mấy?',
           '5 × 2 = 10, tận cùng là 0. Vậy tích tận cùng bằng 0.'),
        lt(4, 2, 'Vì sao khi tìm chữ số tận cùng của một tích, ta bỏ qua được phần '
                 'tròn chục của hai thừa số?',
           'Vì mọi phần có chứa thừa số tròn chục đều là số tròn chục, chữ số cuối '
           'bằng 0, nên không làm đổi chữ số cuối của tích.'),
        lt(5, 2, 'Bạn Tú nói: "Tích 23 × 17 tận cùng là 21." Bạn nói đúng chưa? Vì sao?',
           'CHƯA đúng. 3 × 7 = 21 nhưng câu hỏi đòi một CHỮ SỐ tận cùng, mà chữ số '
           'tận cùng của 21 là 1.'),
        lt(6, 2, 'Không nhân hết, hãy cho biết tích 128 × 35 có tận cùng bằng mấy.',
           '8 × 5 = 40, tận cùng là 0. Vậy tích tận cùng bằng 0.'),
        lt(7, 2, 'Một bạn tính 23 × 17 = 394. Không cần tính lại cả phép, hãy chỉ ra '
                 'bạn ấy chắc chắn sai.',
           'Chữ số cuối phải là 1 (vì 3 × 7 = 21), mà kết quả bạn ấy viết tận cùng là '
           '4. Vậy chắc chắn sai.'),
        lt(8, 3, 'Tích 2 × 4 × 5 × 7 có chữ số tận cùng là mấy?',
           'Nhân dần và chỉ giữ chữ số cuối: 2 × 4 = 8; 8 × 5 = 40 tận cùng 0; '
           '0 × 7 = 0. Vậy tích tận cùng bằng 0.'),
        lt(9, 3, 'Tìm chữ số tận cùng của tích 13 × 13 × 13.',
           'Chỉ giữ chữ số cuối: 3 × 3 = 9 tận cùng 9; 9 × 3 = 27 tận cùng 7. Vậy '
           'tích tận cùng bằng 7.'),
        q_tf(1, 'Chữ số tận cùng của một tích chỉ phụ thuộc vào chữ số tận cùng của '
                'các thừa số.', True, 'Đáp án: ĐÚNG.'),
        q_tf(2, 'Tích 23 × 17 có chữ số tận cùng là 21.', False,
             'SAI — chữ số tận cùng chỉ là MỘT chữ số. 3 × 7 = 21 nên tận cùng là 1.'),
        q_mcq(3, 'Tích 34 × 26 có chữ số tận cùng là:',
              ['A. 4', 'B. 6', 'C. 24'], 'A. 4', '4 × 6 = 24, tận cùng là 4.'),
        q_mcq(4, 'Tích 45 × 12 có chữ số tận cùng là:',
              ['A. 0', 'B. 5', 'C. 2'], 'A. 0', '5 × 2 = 10, tận cùng là 0.'),
        q_mcq(5, 'Vì sao phần tròn chục của thừa số không làm đổi chữ số cuối của tích?',
              ['A. Vì nhân với số tròn chục thì luôn được số tận cùng bằng 0',
               'B. Vì số tròn chục quá lớn',
               'C. Vì ta được phép bỏ bớt cho nhanh'],
              'A. Vì nhân với số tròn chục thì luôn được số tận cùng bằng 0',
              'Chữ số cuối bằng 0 thì cộng vào không làm đổi chữ số cuối.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# THỨ TỰ HỌC · Ô NHẬP CHẤM MÁY
# ═══════════════════════════════════════════════════════════════════════════
# Chín bài, xếp theo đúng thứ tự dạy: khái niệm gốc trước, rồi bốn dấu hiệu đi từ dễ
# nhìn (chữ số cuối) sang khó nhìn (cộng chữ số), rồi phép chia có dư và cách dùng nó.
MOI = [B50, B09, B51, B52, B10, B53, B11, B54, B12]

# Chỗ chín bài này chen vào mảng thứ tự: ngay sau bài cuối của chương 2.
TRUOC = 'DL:KSN4.B08'

CO_KHONG = ['có', 'không']

O_NHAP_MOI = {
    # ── ① B50 · chia hết là gì ──
    'DL:KSN4.B50#C1': {'parts': [{'label': 'được mấy nhóm', 'value': 4},
                                 {'label': 'thừa mấy viên', 'value': 0}]},
    'DL:KSN4.B50#C2': {'parts': [{'label': 'được mấy nhóm', 'value': 2},
                                 {'label': 'thừa mấy viên', 'value': 2}]},
    'DL:KSN4.B50#C3': {'parts': [{'label': 'số chia là', 'value': 5},
                                 {'label': 'số dư là', 'value': 2}]},
    'DL:KSN4.B50#C4': {'parts': [{'label': '20 có chia hết cho 4 không',
                                  'options': CO_KHONG, 'value': 'có'},
                                 {'label': 'số dư', 'value': 0}]},
    'DL:KSN4.B50#C5': {'parts': [{'label': '20 có chia hết cho 3 không',
                                  'options': CO_KHONG, 'value': 'không'},
                                 {'label': 'số dư', 'value': 2}]},
    'DL:KSN4.B50#C6': {'parts': [{'label': 'bạn Nam nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'số dư của 15 chia 4', 'value': 3}]},
    'DL:KSN4.B50#C7': {'parts': [{'label': 'thương', 'value': 6},
                                 {'label': 'số dư', 'value': 3}]},
    'DL:KSN4.B50#C8': {'parts': [{'label': 'mỗi đĩa 6 quả thì được mấy đĩa', 'value': 3},
                                 {'label': 'mỗi đĩa 4 quả thì thừa mấy quả', 'value': 2}]},
    'DL:KSN4.B50#C9': {'value': 6},

    # ── ② B09 · dấu hiệu chia hết cho 2 ──
    'DL:KSN4.B09#C1': {'parts': [{'label': 'chữ số cuối', 'value': 4},
                                 {'label': 'có chia hết cho 2 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B09#C2': {'parts': [{'label': 'có chia hết cho 2 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B09#C3': {'parts': [{'label': 'có chia hết cho 2 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B09#C4': {'parts': [{'label': 'số thứ nhất', 'value': 132},
                                 {'label': 'số thứ hai', 'value': 208}]},
    'DL:KSN4.B09#C5': {'parts': [{'label': 'bạn Lan nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': '137 có chia hết cho 2 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B09#C6': {'parts': [{'label': 'vì phần tròn chục luôn chia hết cho',
                                  'value': 2}]},
    'DL:KSN4.B09#C7': {'parts': [{'label': 'số con viết', 'value': 302}]},
    'DL:KSN4.B09#C8': {'parts': [{'label': 'chữ số phải đặt ở cuối', 'value': 4},
                                 {'label': 'một số viết được', 'value': 154}]},
    'DL:KSN4.B09#C9': {'value': 4},

    # ── ③ B51 · dấu hiệu chia hết cho 5 ──
    'DL:KSN4.B51#C1': {'parts': [{'label': 'chữ số cuối', 'value': 5},
                                 {'label': 'có chia hết cho 5 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B51#C2': {'parts': [{'label': 'có chia hết cho 5 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B51#C3': {'parts': [{'label': 'có chia hết cho 5 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B51#C4': {'parts': [{'label': 'số thứ nhất', 'value': 145},
                                 {'label': 'số thứ hai', 'value': 500}]},
    'DL:KSN4.B51#C5': {'parts': [{'label': '64 chia hết cho 2 không',
                                  'options': CO_KHONG, 'value': 'có'},
                                 {'label': '64 chia hết cho 5 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B51#C6': {'parts': [{'label': 'vì 10 bằng 5 nhân', 'value': 2}]},
    'DL:KSN4.B51#C7': {'parts': [{'label': 'số con viết', 'value': 405}]},
    'DL:KSN4.B51#C8': {'parts': [{'label': 'chữ số phải đặt ở cuối', 'value': 5},
                                 {'label': 'một số viết được', 'value': 275}]},
    'DL:KSN4.B51#C9': {'value': 18},

    # ── ④ B52 · chia hết cho cả 2 và 5 ──
    'DL:KSN4.B52#C1': {'parts': [{'label': 'có chia hết cho cả hai không',
                                  'options': CO_KHONG, 'value': 'có'},
                                 {'label': 'chữ số cuối', 'value': 0}]},
    'DL:KSN4.B52#C2': {'parts': [{'label': 'có chia hết cho cả hai không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B52#C3': {'value': 0},
    'DL:KSN4.B52#C4': {'parts': [{'label': 'số thứ nhất', 'value': 130},
                                 {'label': 'số thứ hai', 'value': 200}]},
    'DL:KSN4.B52#C5': {'parts': [{'label': 'chia hết cho 2 không',
                                  'options': CO_KHONG, 'value': 'có'},
                                 {'label': 'chia hết cho 5 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B52#C6': {'parts': [{'label': 'chữ số chung duy nhất', 'value': 0}]},
    'DL:KSN4.B52#C7': {'parts': [{'label': 'số con viết', 'value': 800}]},
    'DL:KSN4.B52#C8': {'parts': [{'label': 'chữ số phải đặt ở cuối', 'value': 0},
                                 {'label': 'một số viết được', 'value': 370}]},
    'DL:KSN4.B52#C9': {'value': 9},

    # ── ⑤ B10 · dấu hiệu chia hết cho 9 ──
    'DL:KSN4.B10#C1': {'parts': [{'label': 'tổng các chữ số', 'value': 9},
                                 {'label': 'có chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B10#C2': {'parts': [{'label': 'tổng các chữ số', 'value': 9},
                                 {'label': 'có chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B10#C3': {'parts': [{'label': 'tổng các chữ số', 'value': 7},
                                 {'label': 'có chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B10#C4': {'parts': [{'label': 'số thứ nhất', 'value': 108},
                                 {'label': 'số thứ hai', 'value': 459}]},
    'DL:KSN4.B10#C5': {'parts': [{'label': 'bạn Bình nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': '63 có chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B10#C6': {'parts': [{'label': 'vì 99 bằng 9 nhân', 'value': 11}]},
    'DL:KSN4.B10#C7': {'parts': [{'label': 'chữ số nhỏ nhất điền được', 'value': 0},
                                 {'label': 'chữ số còn lại điền được', 'value': 9}]},
    'DL:KSN4.B10#C8': {'parts': [{'label': 'tổng ba chữ số đã chọn', 'value': 9},
                                 {'label': 'một số viết được', 'value': 234}]},
    'DL:KSN4.B10#C9': {'parts': [{'label': 'tổng các chữ số', 'value': 27},
                                 {'label': 'thương', 'value': 221}]},

    # ── ⑥ B53 · dấu hiệu chia hết cho 3 ──
    'DL:KSN4.B53#C1': {'parts': [{'label': 'tổng các chữ số', 'value': 9},
                                 {'label': 'có chia hết cho 3 không',
                                  'options': CO_KHONG, 'value': 'có'}]},
    'DL:KSN4.B53#C2': {'parts': [{'label': 'chia hết cho 3 không',
                                  'options': CO_KHONG, 'value': 'có'},
                                 {'label': 'chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B53#C3': {'parts': [{'label': 'tổng các chữ số', 'value': 7},
                                 {'label': 'có chia hết cho 3 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B53#C4': {'parts': [{'label': 'số thứ nhất', 'value': 123},
                                 {'label': 'số thứ hai', 'value': 306}]},
    'DL:KSN4.B53#C5': {'parts': [{'label': '45 chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'có'},
                                 {'label': '15 chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'không'}]},
    'DL:KSN4.B53#C6': {'parts': [{'label': 'vì 9 bằng 3 nhân', 'value': 3}]},
    'DL:KSN4.B53#C7': {'parts': [{'label': 'chữ số nhỏ nhất điền được', 'value': 0},
                                 {'label': 'một số viết được', 'value': 234}]},
    'DL:KSN4.B53#C8': {'parts': [{'label': 'số con tìm được', 'value': 15}]},
    'DL:KSN4.B53#C9': {'parts': [{'label': 'tổng các chữ số', 'value': 15},
                                 {'label': 'chia hết cho 9 không',
                                  'options': CO_KHONG, 'value': 'không'}]},

    # ── ⑦ B11 · phép chia có dư ──
    'DL:KSN4.B11#C1': {'parts': [{'label': 'được mấy hộp', 'value': 3},
                                 {'label': 'thừa mấy cái', 'value': 2}]},
    'DL:KSN4.B11#C2': {'parts': [{'label': 'thương', 'value': 3},
                                 {'label': 'số dư', 'value': 2}]},
    'DL:KSN4.B11#C3': {'value': 14},
    'DL:KSN4.B11#C4': {'parts': [{'label': 'thương', 'value': 4},
                                 {'label': 'số dư', 'value': 5}]},
    'DL:KSN4.B11#C5': {'parts': [{'label': 'thương đúng', 'value': 4},
                                 {'label': 'số dư đúng', 'value': 3}]},
    'DL:KSN4.B11#C6': {'value': 6},
    'DL:KSN4.B11#C7': {'value': 38},
    'DL:KSN4.B11#C8': {'value': 7},
    'DL:KSN4.B11#C9': {'value': 16},

    # ── ⑧ B54 · bài toán thừa - thiếu ──
    'DL:KSN4.B54#C1': {'parts': [{'label': 'thương', 'value': 4},
                                 {'label': 'số dư', 'value': 1}]},
    'DL:KSN4.B54#C2': {'value': 5},
    'DL:KSN4.B54#C3': {'value': 4},
    'DL:KSN4.B54#C4': {'value': 5},
    'DL:KSN4.B54#C5': {'parts': [{'label': 'thùng đầy', 'value': 4},
                                 {'label': 'thừa mấy quyển', 'value': 2}]},
    'DL:KSN4.B54#C6': {'parts': [{'label': 'bạn Mai trả lời', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'số hộp đúng', 'value': 6}]},
    'DL:KSN4.B54#C7': {'parts': [{'label': 'cắt được mấy đoạn', 'value': 5},
                                 {'label': 'thừa mấy mét', 'value': 2}]},
    'DL:KSN4.B54#C8': {'parts': [{'label': 'hàng đầy', 'value': 12},
                                 {'label': 'cần bao nhiêu hàng', 'value': 13}]},
    'DL:KSN4.B54#C9': {'parts': [{'label': 'bao đầy', 'value': 8},
                                 {'label': 'thừa mấy ki-lô-gam', 'value': 5},
                                 {'label': 'cần mấy bao', 'value': 9}]},

    # ── ⑨ B12 · chữ số tận cùng của một tích ──
    'DL:KSN4.B12#C1': {'parts': [{'label': 'nhân hai chữ số cuối được', 'value': 21},
                                 {'label': 'chữ số tận cùng của tích', 'value': 1}]},
    'DL:KSN4.B12#C2': {'value': 4},
    'DL:KSN4.B12#C3': {'value': 0},
    'DL:KSN4.B12#C4': {'parts': [{'label': 'chữ số cuối của phần tròn chục', 'value': 0}]},
    'DL:KSN4.B12#C5': {'parts': [{'label': 'bạn Tú nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'chữ số tận cùng đúng', 'value': 1}]},
    'DL:KSN4.B12#C6': {'value': 0},
    'DL:KSN4.B12#C7': {'parts': [{'label': 'chữ số cuối phải là', 'value': 1},
                                 {'label': 'chữ số cuối bạn ấy viết', 'value': 4}]},
    'DL:KSN4.B12#C8': {'value': 0},
    'DL:KSN4.B12#C9': {'value': 7},
}


def soi():
    """Soi trước khi ghi. Phần chung ở `khuon_bai_lop4.soi_bai`; dưới đây là luật
    riêng của chương này."""
    loi = soi_bai(MOI, O_NHAP_MOI)

    # Bài khái niệm KHÔNG được nêu dấu hiệu nào — nêu ra là hỏng mất chỗ đứng của nó
    # trong chuỗi, vì bài sau sẽ chẳng còn gì để dạy.
    van = ' '.join(x['text'] + x['loiChua'] for x in B50['cau'])
    if 'tận cùng là 0, 2, 4' in van or 'tổng các chữ số' in van:
        loi.append('B50 là bài KHÁI NIỆM, không được nêu dấu hiệu chia hết')

    # Mã bài phải là mã CŨ hoặc mã TRỐNG — không được đụng vào mã của bài khác.
    cu = {'DL:KSN4.B09', 'DL:KSN4.B10', 'DL:KSN4.B11', 'DL:KSN4.B12'}
    moi_ = {'DL:KSN4.B50', 'DL:KSN4.B51', 'DL:KSN4.B52', 'DL:KSN4.B53', 'DL:KSN4.B54'}
    co = {b['id'] for b in MOI}
    if co != cu | moi_:
        loi.append(f'mã bài không đúng dự kiến: thừa {co - (cu | moi_)}, '
                   f'thiếu {(cu | moi_) - co}')

    # Số neo của chương phải xuất hiện ở đủ các bài dấu hiệu — luật 3 (một ví dụ
    # chạy suốt cụm). Quên nó thì mỗi bài lại một số mới, bé phải làm quen lại.
    for b in (B09, B51, B52, B10, B53):
        if '270' not in json.dumps(b, ensure_ascii=False):
            loi.append(f'{b["id"]}: thiếu số neo 270 của chương')
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
        print(f"  {b['id']}  {b['ten'][:52]:52} {n} luyện + {q} quiz")
    if a.xem:
        print('\n(--xem: chưa ghi gì)')
        return

    # ⚠ GIỮ LẠI HÌNH ĐÃ GẮN. `gan_hinh_lop4.py` ghi hình vào chính tệp nguồn, nên
    # ghi đè trắng ở đây là xoá sạch hình của bài — đã sập thật một lần khi chạy lại
    # `day_so_lop4.py`. Bài mới thì không có gì để giữ, nhưng bốn mã cũ thì có.
    for b in MOI:
        tep = RA / f"DL_KSN4_B{b['so']:02d}.json"
        if tep.exists():
            cu = json.loads(tep.read_text('utf8'))
            for ten, m in b['muc'].items():
                cu_m = cu.get('muc', {}).get(ten)
                if isinstance(cu_m, dict) and cu_m.get('hinh') and not m.get('hinh'):
                    m['hinh'] = cu_m['hinh']
        tep.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n', 'utf8')

    # Thứ tự học: chèn chín bài vào ngay sau bài cuối chương 2, giữ nguyên mọi mã
    # khác. Đây là toàn bộ việc "đổi số bài" theo lối C.
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
    print(f'thêm {len(O_NHAP_MOI)} ô nhập vào {O_NHAP.relative_to(GOC)} (nay {len(o)} mục)')


if __name__ == '__main__':
    main()
