#!/usr/bin/env python3
"""NĂM BÀI DÃY SỐ CÁCH ĐỀU — lớp 4, viết tay.

    python3 tools/day_so_lop4.py            # ghi data/lop4/DL_KSN4_B13..B17.json
    python3 tools/day_so_lop4.py --xem      # in ra xem, không ghi

── VÌ SAO TÁCH NĂM BÀI ──
Bác đọc Bài 13 cũ ("DÃY SỐ CÁCH ĐỀU") thấy khó hiểu. Mở ra soi thì đúng: một bài
nhồi BỐN công thức độc lập (số hạng thứ n · số số hạng · tổng dãy · thuộc dãy) với
9 câu luyện tập cho cả bốn — hơn hai câu mỗi công thức.

Nhưng chỗ hỏng nặng hơn nằm ở phía trước: **không một khái niệm nào được định
nghĩa.** `vocabulary` rỗng ở cả 44 bài lớp 4, và lần ngược xuống lớp 3 (B10·B11·B12
— đúng ba bài mà Bài 13 trỏ về làm đường lui) thì cũng rỗng nốt. Bé gặp thẳng "dãy
cách đều", "số hạng thứ n", "khoảng cách" như thể đã biết rồi.

Bác chốt 14-08: *"mọi định nghĩa cần được giải thích chi tiết trước khi đi đến bài
toán… phải hiểu các khái niệm này xong → test đảm bảo học sinh hiểu rồi mới sang
bài tiếp theo"*.

Nên:

    B13  DÃY SỐ LÀ GÌ            khái niệm, KHÔNG công thức nào
    B14  SỐ HẠNG THỨ n           một công thức
    B15  DÃY CÓ BAO NHIÊU SỐ HẠNG một công thức
    B16  TỔNG DÃY CÁCH ĐỀU        một công thức
    B17  SỐ NÀY CÓ THUỘC DÃY KHÔNG một công thức
    B18  (Bài 13 cũ) bài kết hợp — nay đứng CUỐI cụm, không phải đầu

── LUẬT RIÊNG CỦA BÀI B13 ──
Bài khái niệm KHÔNG được có một công thức nào. Bé chỉ nhìn dãy ngắn, chỉ tay vào
từng chỗ, trả lời hai câu ngược nhau: "chỗ thứ 4 là số nào" và "số 17 đứng thứ
mấy". Có công thức ở đây là quay lại đúng chỗ hỏng. Cổng `day_so_lop4.test.mjs`
canh điều này.

── KHUÔN ──
Viết vào `data/lop4/` — BẢN GỐC 10 mục ①…⑩. Bản cho app do
`tools/dung_khuon_chung_lop4.py` sinh ra; đừng sửa tay bên `web/public/content/`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / 'data' / 'lop4'
O_NHAP = GOC / 'data' / 'lop4_dapan_o.json'

TEN_CHUONG = 'DÃY SỐ'
CHUONG = 4

# Đường lui về lớp 3 — bé chưa vững thì có chỗ quay lại.
LUI_TOA = {'ve': ['DL:KSN3.B10'], 'ten': ['TOA TÀU THỨ n Ở ĐÂU?'],
           'canCu': 'sach', 'lopDuoi': 3}
LUI_GA = {'ve': ['DL:KSN3.B11'], 'ten': ['GA NÀY TÀU CÓ DỪNG KHÔNG?'],
          'canCu': 'sach', 'lopDuoi': 3}


def muc(ten, dong, nhip='', hinh=None):
    return {'ten': ten, 'dong': list(dong), 'hinh': list(hinh or []), 'nhip': nhip}


def bai(so, ten, dang_goc, hat_mam, gan_duoi, m, cau):
    return {
        'id': f'DL:KSN4.B{so:02d}', 'quyen': 'KSN4', 'so': so,
        # `ten` ở BẢN GỐC là tên trần, KHÔNG có tiền tố "Bài n ·" —
        # `khuon_chung` tự ghép tiền tố khi dựng bản cho app. Bản đầu của
        # tệp này ghép sẵn, nên bản dựng sẽ ra "Bài 13 · Bài 13 · DÃY SỐ…".
        'ten': ten, 'chuong': CHUONG, 'tenChuong': TEN_CHUONG,
        'dangGoc': dang_goc, 'hatMam': hat_mam, 'ganDuoi': gan_duoi,
        'muc': m, 'cau': cau,
    }


def lt(so, mucsao, text, loi_chua, ghi_chu=''):
    """Một câu luyện tập. `tuLuan: True` nghĩa là có lời giải chữ; ô nhập chấm máy
    khai riêng ở `lop4_dapan_o.json` — xem `O_NHAP_MOI` cuối tệp."""
    return {'id': f'C{so}', 'maSach': f'C{so}', 'so': so, 'muc': mucsao,
            'phan': 'luyenTap', 'ghiChu': ghi_chu, 'text': text,
            'loiChua': loi_chua, 'tuLuan': True}


def q_tf(so, text, dung, loi_chua, ke=''):
    return {'id': f'Q{so}', 'maSach': f'C{so}', 'so': so, 'muc': 1, 'phan': 'quiz',
            'ghiChu': 'Đúng/Sai?', 'text': text, 'format': 'tf', 'tuLuan': False,
            'answerKey': {'value': dung}, 'loiChua': loi_chua,
            'solutionNarrative': ke or loi_chua}


def q_mcq(so, text, chon, dung, loi_chua, ke=''):
    return {'id': f'Q{so}', 'maSach': f'C{so}', 'so': so, 'muc': 1, 'phan': 'quiz',
            'ghiChu': '', 'text': text, 'choices': chon, 'format': 'mcq',
            'tuLuan': False, 'answerKey': {'choice': dung}, 'loiChua': loi_chua,
            'solutionNarrative': ke or loi_chua}


TEN_MUC = {
    'mucTieu': 'MỤC TIÊU BÀI HỌC — Sau bài này con sẽ:',
    'dichMoHinh': 'PHÂN TÍCH & DỰNG MÔ HÌNH — bàn vẽ của kỹ sư',
    'khamPha': 'KHÁM PHÁ CÙNG SU KEM — vào không gian toán',
    'lapSoi': 'LẮP VỀ CUỘC SỐNG & SOI',
    'viDuMau': 'LỜI GIẢI MẪU TRÌNH BÀY VỞ',
    'suKemNham': 'TRÍ LONG ƠI, NHẦM RỒI!',
    'luyenTap': 'LUYỆN TẬP 3 MỨC SAO',
    'quiz': 'QUIZ — CON HIỂU BÀI CHƯA?',
    'gocBoMe': 'GÓC BỐ MẸ',
}


def dung_muc(mo_bai_ten, mo_bai, muc_tieu, dich, kham, lap, vidu, nham, bome):
    return {
        'mucTieu': muc(TEN_MUC['mucTieu'], muc_tieu),
        'chuyenMoBai': muc(f'CHUYỆN MỞ BÀI — {mo_bai_ten}', mo_bai),
        'dichMoHinh': muc(TEN_MUC['dichMoHinh'], dich, 'NHỊP 1, DỊCH'),
        'khamPha': muc(TEN_MUC['khamPha'], kham, 'NHỊP 2, GIẢI'),
        'lapSoi': muc(TEN_MUC['lapSoi'], lap, 'NHỊP 3, LẮP + NHỊP 4, SOI'),
        'viDuMau': muc(TEN_MUC['viDuMau'], vidu),
        'suKemNham': muc(TEN_MUC['suKemNham'], nham),
        'luyenTap': muc(TEN_MUC['luyenTap'], []),
        'quiz': muc(TEN_MUC['quiz'], ['Khoanh vào đáp án đúng (mỗi câu 1 sao ★)']),
        'gocBoMe': muc(TEN_MUC['gocBoMe'], bome),
    }


# ═══════════════════════════════════════════════════════════════════════════
# B13 · DÃY SỐ LÀ GÌ — bài KHÁI NIỆM, không một công thức nào
# ═══════════════════════════════════════════════════════════════════════════
# Chọn PHỐ NHÀ làm chuyện mở bài vì nó tách được đúng hai thứ bé hay lẫn: "nhà
# THỨ MẤY" và "nhà SỐ MẤY" là hai con số khác nhau nói về CÙNG một ngôi nhà. Rạp
# phim để dành cho bài kết hợp (B18) — ở đó mới cần tới cả bốn công thức.
B13 = bai(
    13, 'DÃY SỐ LÀ GÌ — CHỖ ĐỨNG VÀ SỐ ĐỨNG Ở ĐÓ',
    'Dạng gốc: SỐ 5.1a mức Lớp 4 — Khái niệm dãy số · số hạng · vị trí · giá trị · '
    'cách đều · khoảng cách. KHÔNG công thức.',
    'Lớp 3, ở Bài 10, con đã đi trên "đoàn tàu đếm thêm" và tìm toa thứ n. Nhưng '
    'hôm ấy con làm theo hình vẽ. Hôm nay mình dừng lại gọi ĐÚNG TÊN từng thứ: cái '
    'gì là dãy, cái gì là số hạng, "thứ mấy" khác "số mấy" ở chỗ nào. Gọi đúng tên '
    'rồi thì bốn bài sau chỉ còn là bốn phép tính.',
    LUI_TOA,
    # ⚠ BÀI 13 KHÔNG CÓ MỞ BÀI VÀ BÀI GIẢNG BẰNG CHỮ — VIDEO THAY CẢ HAI.
    # Bác chốt 14-08 sau khi duyệt video: "Video đã thay thế cho cả phần mở bài và
    # bài giảng. Xoá toàn bộ nội dung phần mở bài và bài giảng cũ đi, chỉ để Video."
    #
    # Nên bốn mục ②③④⑤ để RỖNG. Bộ dựng thấy rỗng thì không sinh màn nào, và
    # `buildTeachSteps` trả về danh sách rỗng — bé đi thẳng từ video sang bài mẫu.
    # Đây là chủ ý, không phải bỏ sót; `video_toan.test.mjs` canh đúng điều đó.
    #
    # Giữ lại ⑥ bài mẫu và ⑦ chỗ hay nhầm, nhưng VIẾT LẠI cho khớp video: cùng dãy
    # ví dụ, cùng cách nói, và bỏ nhân vật Trí Long vì video không có nhân vật nào.
    dung_muc(
        '',
        [],
        ['Gọi đúng tên bốn thứ: dãy số, số hạng, thứ tự và giá trị.',
         'Nhìn một dãy và nói được nó có cách đều không, khoảng cách bằng bao nhiêu.',
         'Trả lời được hai chiều: chỗ thứ n là số nào, và số x đứng thứ mấy.'],
        [],
        [],
        [],
        ['Đề bài: Cho dãy 5 ; 10 ; 15 ; 20 ; 25. Dãy này có mấy số hạng? Số hạng thứ '
         'ba có giá trị bao nhiêu? Số 20 đứng thứ mấy? Dãy có cách đều không?',
         'Đếm số hạng',
         'Đếm từng số: 5, 10, 15, 20, 25.',
         'Dãy có 5 số hạng.',
         'Đọc theo thứ tự',
         'Chỗ thứ nhất là 5, chỗ thứ hai là 10, chỗ thứ ba là 15.',
         'Số hạng thứ ba có giá trị 15.',
         'Đọc ngược lại',
         'Đếm tới số 20: 5 (1), 10 (2), 15 (3), 20 (4).',
         'Số 20 đứng thứ 4.',
         'Kiểm cách đều',
         'Lấy số sau trừ số trước: 10 − 5 = 5 ; 15 − 10 = 5 ; 20 − 15 = 5 ; 25 − 20 = 5.',
         'Các hiệu đều bằng 5, nên dãy cách đều và khoảng cách là 5.',
         'Đáp số: 5 số hạng; số hạng thứ ba là 15; số 20 đứng thứ 4; dãy cách đều, '
         'khoảng cách 5.'],
        ['Có bạn nhìn dãy 5 ; 10 ; 15 ; 20 ; 25 rồi nói: "Số 15 đứng thứ 15."',
         'Gợi ý 1: Con đọc lại dãy xem. Dãy chỉ có 5 số hạng, làm gì có chỗ thứ 15.',
         'Gợi ý 2: Số 15 là GIÁ TRỊ. Còn chỗ đứng của nó là THỨ TỰ. Con đếm chỗ xem '
         'nó đứng thứ mấy.',
         'Chữa: số 15 đứng thứ 3. Thứ tự là 3, giá trị là 15 — hai con số khác nhau.'],
        ['Viết ra giấy một dãy cách đều bất kỳ rồi hỏi con hai câu ngược nhau: "Chỗ '
         'thứ tư là số nào?" và "Số này đứng thứ mấy?"',
         'Con lẫn thứ tự với giá trị là chuyện thường. Bố mẹ chỉ cần hỏi lại: "Con '
         'đang nói chỗ đứng hay đang nói con số?"'],
    ),
    # ── BÀI TẬP ĐI ĐÚNG ĐƯỜNG VIDEO ĐÃ DẠY ──
    # Bác duyệt video rồi bảo viết bài tập theo video. Nên bảy câu đầu bám đúng bảy
    # nấc video đi qua, và MỞ ĐẦU BẰNG CHÍNH DÃY TRONG VIDEO (5, 10, 15, 20, 25):
    # bé vừa xem xong, gặp lại dãy quen thì câu đầu không phải là một cửa ải.
    #
    #   nấc video                    câu
    #   ─────────────────────────────────
    #   số hạng, đếm bao nhiêu       C1
    #   thứ tự  → giá trị            C2
    #   giá trị → thứ tự (chiều ngược) C3
    #   hai chiều trên dãy MỚI       C4
    #   thứ tự KHÁC giá trị          C5
    #   lấy số sau trừ số trước      C6
    #   dãy nào cách đều             C7
    #   gộp cả ba                    C8
    #   dãy giảm cũng cách đều       C9
    [
        lt(1, 1, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25 — đúng dãy trong video. Dãy này có '
                 'bao nhiêu số hạng?',
           'Đếm từng số: 5, 10, 15, 20, 25 — dãy có 5 số hạng.'),
        lt(2, 1, 'Vẫn dãy 5 ; 10 ; 15 ; 20 ; 25. Số hạng thứ hai có giá trị là bao nhiêu?',
           'Đếm chỗ: 5 đứng thứ nhất, 10 đứng thứ hai. Vậy số hạng thứ hai có giá trị 10.'),
        lt(3, 1, 'Vẫn dãy 5 ; 10 ; 15 ; 20 ; 25. Số 20 đứng ở thứ tự thứ mấy?',
           'Đếm chỗ: 5 (1), 10 (2), 15 (3), 20 (4). Số 20 đứng thứ tư.'),
        lt(4, 2, 'Cho dãy 3 ; 6 ; 9 ; 12 ; 15. Số hạng thứ tư có giá trị bao nhiêu, '
                 'và số 9 đứng thứ mấy?',
           'Số hạng thứ tư có giá trị 12; số 9 đứng thứ 3.'),
        lt(5, 2, 'Trong dãy 8 ; 16 ; 24 ; 32, bạn An nói: "Số 24 đứng thứ 24." Bạn nói '
                 'đúng hay sai? Số 24 thật ra đứng thứ mấy?',
           'SAI. 24 là GIÁ TRỊ, còn thứ tự của nó là 3. Thứ tự và giá trị là hai '
           'con số khác nhau.'),
        lt(6, 2, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25. Lấy số sau trừ số trước thì được bao '
                 'nhiêu? Dãy này có cách đều không?',
           'Các hiệu: 10 − 5 = 5 ; 15 − 10 = 5 ; 20 − 15 = 5 ; 25 − 20 = 5. Các hiệu '
           'đều bằng 5 nên dãy CÁCH ĐỀU, khoảng cách 5.'),
        lt(7, 2, 'Trong hai dãy sau, dãy nào CÁCH ĐỀU: dãy A là 2 ; 4 ; 6 ; 8 hay dãy '
                 'B là 2 ; 4 ; 8 ; 16?',
           'Dãy A có các hiệu 2 ; 2 ; 2 — bằng nhau nên cách đều. Dãy B có các hiệu '
           '2 ; 4 ; 8 — khác nhau nên KHÔNG cách đều.'),
        lt(8, 3, 'Cho dãy 7 ; 12 ; 17 ; 22 ; 27. Cho biết khoảng cách của dãy, giá trị '
                 'của số hạng thứ tư, và số 17 đứng thứ mấy.',
           'Khoảng cách 5; số hạng thứ tư có giá trị 22; số 17 đứng thứ 3.'),
        lt(9, 3, 'Cho dãy 100 ; 90 ; 80 ; 70 ; 60. Dãy này có cách đều không? Khoảng '
                 'cách bằng bao nhiêu?',
           'Mỗi bước giảm đúng 10 đơn vị, đều nhau, nên dãy vẫn CÁCH ĐỀU với khoảng cách 10.'),
        q_tf(1, 'Mỗi số trong một dãy số được gọi là một số hạng.', True,
             'Đáp án: ĐÚNG'),
        q_tf(2, 'Trong dãy 5 ; 10 ; 15 ; 20 ; 25, số 15 đứng thứ 15.', False,
             'SAI — 15 là giá trị, còn thứ tự của nó là thứ ba.'),
        q_mcq(3, 'Trong dãy 5 ; 10 ; 15 ; 20 ; 25, số hạng thứ tư có giá trị là:',
              ['A. 20', 'B. 4', 'C. 15'], 'A. 20',
              'Đếm chỗ: 5 (1), 10 (2), 15 (3), 20 (4).'),
        q_mcq(4, 'Dãy nào dưới đây là dãy CÁCH ĐỀU?',
              ['A. 1 ; 3 ; 5 ; 7', 'B. 1 ; 2 ; 4 ; 8', 'C. 1 ; 4 ; 9 ; 16'],
              'A. 1 ; 3 ; 5 ; 7', 'Dãy A có các hiệu đều bằng 2.'),
        q_mcq(5, 'Dãy 6 ; 12 ; 18 ; 24 có khoảng cách bằng:',
              ['A. 6', 'B. 4', 'C. 12'], 'A. 6',
              'Lấy số sau trừ số trước: 12 − 6 = 6, và các hiệu sau cũng bằng 6.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# B14 · SỐ HẠNG THỨ n
# ═══════════════════════════════════════════════════════════════════════════
B14 = bai(
    14, 'SỐ HẠNG THỨ n — ĐẾM BƯỚC NHẢY, KHÔNG ĐẾM CHỖ',
    'Dạng gốc: SỐ 5.1b mức Lớp 4 — Công thức số hạng thứ n = số đầu + khoảng cách × (n − 1).',
    'Bài trước con đã gọi đúng tên: dãy số, số hạng, vị trí, giá trị, khoảng cách. '
    'Nhưng muốn biết số hạng thứ 50 thì viết cả dãy ra là hết vở. Hôm nay con học '
    'cách nhảy thẳng tới chỗ ấy — và chỗ tinh tế nhất của cả bài chỉ nằm ở một dấu trừ.',
    LUI_TOA,
    # ⚠ VIDEO THAY CẢ MỞ BÀI LẪN BÀI GIẢNG — bốn mục ②③④⑤ để RỖNG.
    # Cùng khuôn đã chốt ở Bài 13. Giữ ⑥ bài mẫu và ⑦ chỗ hay nhầm, nhưng viết
    # theo đúng đường video đi, và KHÔNG nhân vật nào.
    dung_muc(
        '',
        [],
        ['Đếm được số lần cộng thêm từ chỗ này tới chỗ kia.',
         'Tìm được số hạng ở chỗ xa mà không phải viết cả dãy.',
         'Giải thích được vì sao số lần cộng ít hơn số chỗ đúng một.'],
        [],
        [],
        [],
        ['Đề bài: Cho dãy 5 ; 10 ; 15 ; 20 ; 25 ; ... Tìm số hạng thứ 10.',
         'Tìm khoảng cách',
         'Lấy số sau trừ số trước: 10 − 5 = 5.',
         'Khoảng cách là 5.',
         'Đếm số lần cộng thêm',
         'Từ chỗ thứ nhất đến chỗ thứ 10 phải cộng thêm 10 − 1 = 9 lần.',
         'Chỗ thứ nhất đã có sẵn, không phải cộng lần nào.',
         'Tính',
         'Số hạng thứ 10 = 5 + 5 × 9 = 5 + 45 = 50.',
         'Thử lại: thay số 1 vào thì được 5 + 5 × 0 = 5, đúng bằng số đầu.',
         'Đáp số: số hạng thứ 10 là 50.'],
        ['Có bạn tính số hạng thứ 10 của dãy 5 ; 10 ; 15 ; ... như sau: 5 + 5 × 10 = 55.',
         'Gợi ý 1: Con thử cách ấy với chỗ thứ nhất xem: 5 + 5 × 1 = 10. Nhưng số '
         'hạng thứ nhất rõ ràng là 5 mà?',
         'Gợi ý 2: Từ chỗ thứ nhất đến chỗ thứ 10, con cộng thêm 10 lần hay 9 lần? '
         'Vẽ bốn chỗ ra giấy mà đếm thử.',
         'Chữa: phải nhân với 9, không nhân với 10. Số hạng thứ 10 = 5 + 5 × 9 = 50.'],
        ['Đếm bậc cầu thang nhà mình, đo chiều cao một bậc, rồi hỏi con bậc thứ 8 '
         'cao bao nhiêu. Tính trước rồi cùng đo lại để kiểm.',
         'Mẹo kiểm nhanh: bảo con thay số 1 vào cách tính vừa viết. Ra đúng số đầu '
         'thì đúng; ra số khác là con quên trừ một.'],
    ),
    # Bám đúng nấc video: đếm số lần cộng thêm → vì sao ít hơn một → cách tính →
    # thử ở chỗ xa. Ba câu đầu dùng chính dãy trong video.
    [
        lt(1, 1, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25 — dãy trong video. Từ chỗ thứ nhất '
                 'đến chỗ thứ tư phải cộng thêm mấy lần?',
           'Đếm: từ chỗ 1 sang chỗ 2, sang chỗ 3, sang chỗ 4 — cộng thêm 3 lần, '
           'không phải 4 lần.'),
        lt(2, 1, 'Vẫn dãy 5 ; 10 ; 15 ; 20 ; 25. Khoảng cách bằng bao nhiêu, và số '
                 'hạng thứ tư bằng bao nhiêu?',
           'Khoảng cách 5. Số hạng thứ tư = 5 + 5 × 3 = 20.'),
        lt(3, 1, 'Vẫn dãy 5 ; 10 ; 15 ; ... Số hạng thứ 6 bằng bao nhiêu?',
           '5 + 5 × 5 = 30.'),
        lt(4, 2, 'Cho dãy 5 ; 10 ; 15 ; ... Số hạng thứ 10 bằng bao nhiêu?',
           '5 + 5 × 9 = 50.'),
        lt(5, 2, 'Cho dãy 3 ; 7 ; 11 ; ... Số hạng thứ 8 bằng bao nhiêu?',
           'Khoảng cách 4. Số hạng thứ 8 = 3 + 4 × 7 = 31.'),
        lt(6, 2, 'Một dãy cách đều có số đầu 2, khoảng cách 4. Số hạng thứ 12 bằng '
                 'bao nhiêu?',
           '2 + 4 × 11 = 46.'),
        lt(7, 2, 'Thay số 1 vào cách tính số hạng thứ n của dãy 5 ; 10 ; 15 ; ... thì '
                 'được bao nhiêu?',
           '5 + 5 × 0 = 5, đúng bằng số đầu. Đây là cách kiểm nhanh xem mình có quên '
           'trừ một không.'),
        lt(8, 3, 'Cho dãy 5 ; 10 ; 15 ; ... Số hạng thứ 100 bằng bao nhiêu? Đây chính '
                 'là câu hỏi mở đầu video.',
           '5 + 5 × 99 = 5 + 495 = 500.'),
        lt(9, 3, 'Số hạng thứ 6 của một dãy cách đều là 32, khoảng cách của dãy là 5. '
                 'Số hạng đầu của dãy bằng bao nhiêu?',
           'Từ chỗ 1 đến chỗ 6 cộng thêm 5 lần, tức là thêm 5 × 5 = 25. '
           'Số đầu = 32 − 25 = 7.'),
        q_tf(1, 'Từ chỗ thứ nhất đến chỗ thứ 10 phải cộng thêm 10 lần.', False,
             'SAI — chỉ cộng thêm 9 lần, vì chỗ thứ nhất đã có sẵn.'),
        q_tf(2, 'Muốn tìm số hạng thứ n, ta lấy số đầu cộng khoảng cách nhân với n trừ 1.',
             True, 'Đáp án: ĐÚNG'),
        q_mcq(3, 'Số hạng thứ 12 của dãy 2 ; 5 ; 8 ; ... là:',
              ['A. 35', 'B. 38', 'C. 32'], 'A. 35', '2 + 3 × 11 = 35.'),
        q_mcq(4, 'Thay số 1 vào cách tính số hạng thứ n, kết quả phải bằng:',
              ['A. số đầu của dãy', 'B. khoảng cách', 'C. số 1'], 'A. số đầu của dãy',
              'Vì cộng thêm 0 lần nên ra đúng số đầu.'),
        q_mcq(5, 'Dãy 5 ; 10 ; 15 ; ... có số hạng thứ 10 là:',
              ['A. 50', 'B. 55', 'C. 45'], 'A. 50', '5 + 5 × 9 = 50.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# B15 · DÃY CÓ BAO NHIÊU SỐ HẠNG
# ═══════════════════════════════════════════════════════════════════════════
B15 = bai(
    15, 'DÃY CÓ BAO NHIÊU SỐ HẠNG — VÌ SAO PHẢI CỘNG 1',
    'Dạng gốc: SỐ 5.1c mức Lớp 4 — Công thức số số hạng = (cuối − đầu) : khoảng cách + 1.',
    'Bài trước con đi XUÔI: biết vị trí, tìm giá trị. Hôm nay đi NGƯỢC: biết số đầu '
    'và số cuối, đếm xem cả dãy có bao nhiêu số hạng. Công thức lần này CỘNG 1, '
    'trong khi bài trước TRỪ 1 — hai dấu ngược nhau, và cả hai đều có lý do.',
    LUI_TOA,
    # ⚠ VIDEO THAY CẢ MỞ BÀI LẪN BÀI GIẢNG — bốn mục ②③④⑤ để RỖNG.
    # Cùng khuôn đã chốt ở Bài 13. Giữ ⑥ bài mẫu và ⑦ chỗ hay nhầm, nhưng viết
    # theo đúng đường video đi, và KHÔNG nhân vật nào.
    dung_muc(
        '',
        [],
        ['Đếm được số số hạng của một dãy mà không phải viết cả dãy.',
         'Biết phép chia cho ra số lần cộng thêm, chưa phải số số hạng.',
         'Giải thích được vì sao phải cộng thêm một.'],
        [],
        [],
        [],
        ['Đề bài: Dãy 5 ; 10 ; 15 ; ... ; 100 có bao nhiêu số hạng?',
         'Tìm khoảng cách',
         'Lấy số sau trừ số trước: 10 − 5 = 5.',
         'Khoảng cách là 5.',
         'Lấy số cuối trừ số đầu',
         '100 − 5 = 95.',
         'Chia cho khoảng cách',
         '95 : 5 = 19. Đây là số lần cộng thêm, chưa phải số số hạng.',
         'Cộng thêm một cho chỗ đầu tiên',
         '19 + 1 = 20 số hạng.',
         'Soi lại trên dãy ngắn: 5 ; 10 ; 15 có (15 − 5) : 5 + 1 = 3, đếm tay cũng 3.',
         'Đáp số: dãy có 20 số hạng.'],
        ['Có bạn đếm dãy 5 ; 10 ; 15 ; ... ; 100 rồi nói: "(100 − 5) : 5 = 19 số hạng."',
         'Gợi ý 1: Con thử cách ấy trên dãy ngắn 5 ; 10 ; 15 xem: (15 − 5) : 5 = 2. '
         'Nhưng đếm tay thì rõ ràng có 3 số hạng mà?',
         'Gợi ý 2: Phép chia cho ra số lần cộng thêm. Con đã đếm chỗ đứng đầu tiên '
         'chưa?',
         'Chữa: phải cộng thêm một. Dãy có 19 + 1 = 20 số hạng.'],
        ['Đếm số bậc cầu thang rồi đếm số lần bước từ dưới lên — cho con tự thấy hai '
         'con số lệch nhau đúng một.',
         'Đố vui: từ trang 20 đến trang 80 có bao nhiêu trang? Đáp là 61, không phải '
         '60, vì tính cả trang 20.'],
    ),
    # Bám đúng nấc video: cuối trừ đầu → chia khoảng cách → đó là số lần cộng →
    # cộng thêm một cho chỗ đầu tiên.
    [
        lt(1, 1, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25 — dãy trong video. Lấy số cuối trừ '
                 'số đầu được bao nhiêu?',
           '25 − 5 = 20.'),
        lt(2, 1, 'Lấy 20 vừa tìm được chia cho khoảng cách 5 thì được bao nhiêu?',
           '20 : 5 = 4. Đây là số lần cộng thêm, chưa phải số số hạng.'),
        lt(3, 1, 'Vậy dãy 5 ; 10 ; 15 ; 20 ; 25 có bao nhiêu số hạng?',
           '4 + 1 = 5 số hạng. Đếm tay cũng ra 5.'),
        lt(4, 2, 'Dãy 5 ; 10 ; 15 ; ... ; 100 có bao nhiêu số hạng?',
           '(100 − 5) : 5 + 1 = 19 + 1 = 20 số hạng.'),
        lt(5, 2, 'Dãy 2 ; 4 ; 6 ; ... ; 100 có bao nhiêu số hạng?',
           '(100 − 2) : 2 + 1 = 49 + 1 = 50 số hạng.'),
        lt(6, 2, 'Dãy 3 ; 7 ; 11 ; ... ; 79 có bao nhiêu số hạng?',
           '(79 − 3) : 4 + 1 = 19 + 1 = 20 số hạng.'),
        lt(7, 2, 'Một dãy phải cộng thêm 8 lần mới đi từ số đầu tới số cuối. Dãy ấy '
                 'có bao nhiêu số hạng?',
           '8 + 1 = 9 số hạng. Số chỗ luôn nhiều hơn số lần cộng đúng một.'),
        lt(8, 3, 'Dãy 4 ; 9 ; 14 ; ... ; 99 có bao nhiêu số hạng? Hãy soi lại kết quả '
                 'trên một dãy ngắn cùng kiểu.',
           '(99 − 4) : 5 + 1 = 19 + 1 = 20 số hạng. Soi trên dãy ngắn 4 ; 9 ; 14 : '
           '(14 − 4) : 5 + 1 = 3, đếm tay cũng 3.'),
        lt(9, 3, 'Một dãy cách đều có 25 số hạng, số đầu là 6, khoảng cách là 4. Số '
                 'hạng cuối bằng bao nhiêu?',
           '25 số hạng thì cộng thêm 24 lần: 6 + 4 × 24 = 6 + 96 = 102.'),
        q_tf(1, 'Số số hạng bằng số cuối trừ số đầu, chia cho khoảng cách, rồi cộng 1.',
             True, 'Đáp án: ĐÚNG'),
        q_tf(2, 'Một dãy phải cộng thêm 10 lần thì có 10 số hạng.', False,
             'SAI — có 11 số hạng, vì còn chỗ đứng đầu tiên.'),
        q_mcq(3, 'Dãy 5 ; 10 ; 15 ; ... ; 100 có số số hạng là:',
              ['A. 20', 'B. 19', 'C. 21'], 'A. 20', '(100 − 5) : 5 + 1 = 20.'),
        q_mcq(4, 'Phép chia số cuối trừ số đầu cho khoảng cách cho ra:',
              ['A. số lần cộng thêm', 'B. số số hạng', 'C. số hạng cuối'],
              'A. số lần cộng thêm', 'Muốn ra số số hạng thì phải cộng thêm một.'),
        q_mcq(5, 'Dãy 2 ; 4 ; 6 ; ... ; 100 có số số hạng là:',
              ['A. 50', 'B. 49', 'C. 51'], 'A. 50', '(100 − 2) : 2 + 1 = 50.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# B16 · TỔNG DÃY CÁCH ĐỀU
# ═══════════════════════════════════════════════════════════════════════════
B16 = bai(
    16, 'TỔNG DÃY CÁCH ĐỀU — GHÉP ĐẦU VỚI CUỐI',
    'Dạng gốc: SỐ 5.1d mức Lớp 4 — Công thức tổng = (số đầu + số cuối) × số số hạng : 2.',
    'Con đã biết tìm số hạng thứ n (Bài 14) và đếm số số hạng (Bài 15). Hôm nay dùng '
    'cả hai để làm một việc trông rất nặng: cộng cả trăm số trong một dòng. Có một '
    'cậu bé 10 tuổi từng làm việc ấy trong vài giây — và cách của cậu ấy chỉ là ghép cặp.',
    LUI_TOA,
    # ⚠ VIDEO THAY CẢ MỞ BÀI LẪN BÀI GIẢNG — bốn mục ②③④⑤ để RỖNG.
    # Cùng khuôn đã chốt ở Bài 13. Giữ ⑥ bài mẫu và ⑦ chỗ hay nhầm, nhưng viết
    # theo đúng đường video đi, và KHÔNG nhân vật nào.
    dung_muc(
        '',
        [],
        ['Ghép số đầu với số cuối và thấy cặp nào cũng có tổng bằng nhau.',
         'Tính được tổng của một dãy cách đều mà không cộng lần lượt.',
         'Giải thích được vì sao phải chia đôi.'],
        [],
        [],
        [],
        ['Đề bài: Tính tổng 5 + 10 + 15 + 20 + 25.',
         'Ghép đầu với cuối',
         '5 + 25 = 30 ; 10 + 20 = 30.',
         'Cặp nào cũng bằng 30, đúng bằng số đầu cộng số cuối.',
         'Đếm số số hạng',
         'Dãy có 5 số hạng.',
         'Tính',
         'Tổng = 30 × 5 : 2 = 150 : 2 = 75.',
         'Chia đôi vì khi ghép cặp ta đã cộng mỗi số hai lần.',
         'Soi lại bằng cách cộng tay: 5 + 10 + 15 + 20 + 25 = 75.',
         'Đáp số: tổng bằng 75.'],
        ['Có bạn tính tổng 5 + 10 + 15 + 20 + 25 như sau: (5 + 25) × 5 = 150.',
         'Gợi ý 1: Con thử cộng tay dãy ngắn 1 + 2 + 3 + 4 xem được bao nhiêu, rồi '
         'thử cách ấy: (1 + 4) × 4 = 20. Hai kết quả có khớp không?',
         'Gợi ý 2: Khi ghép cặp, mỗi số được cộng mấy lần? Vậy còn phải làm gì với '
         'kết quả?',
         'Chữa: còn thiếu phép chia đôi. Tổng = (5 + 25) × 5 : 2 = 75.'],
        ['Đố con cộng tất cả các số từ 1 đến 20 trong một phút. Ghép cặp thì làm được, '
         'cộng lần lượt thì không kịp.',
         'Bài đố vui: cộng các số lẻ 1 + 3 + 5 + ... + 19 rồi so với 10 × 10. Trùng '
         'nhau — con thử tìm xem vì sao.'],
    ),
    # Bám đúng nấc video: ghép đầu với cuối → cặp nào cũng bằng nhau → nhân số số
    # hạng → chia đôi vì đã cộng hai lần.
    [
        lt(1, 1, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25 — dãy trong video. Ghép số đầu với '
                 'số cuối được bao nhiêu?',
           '5 + 25 = 30.'),
        lt(2, 1, 'Vẫn dãy ấy. Ghép số thứ hai với số áp chót được bao nhiêu?',
           '10 + 20 = 30 — bằng đúng cặp đầu với cuối.'),
        lt(3, 1, 'Dãy 5 ; 10 ; 15 ; 20 ; 25 có 5 số hạng. Tổng của dãy bằng bao nhiêu?',
           'Tổng = 30 × 5 : 2 = 150 : 2 = 75.'),
        lt(4, 2, 'Tính tổng 1 + 2 + 3 + ... + 10.',
           '(1 + 10) × 10 : 2 = 110 : 2 = 55.'),
        lt(5, 2, 'Tính tổng 1 + 2 + 3 + ... + 50.',
           '(1 + 50) × 50 : 2 = 51 × 25 = 1 275.'),
        lt(6, 2, 'Tính tổng 5 + 10 + 15 + ... + 100.',
           'Dãy có (100 − 5) : 5 + 1 = 20 số hạng. Tổng = (5 + 100) × 20 : 2 = 1 050.'),
        lt(7, 2, 'Tính tổng 3 + 6 + 9 + ... + 30.',
           'Dãy có (30 − 3) : 3 + 1 = 10 số hạng. Tổng = (3 + 30) × 10 : 2 = 165.'),
        lt(8, 3, 'Tính tổng tất cả các số chẵn từ 2 đến 100.',
           'Dãy có (100 − 2) : 2 + 1 = 50 số hạng. Tổng = (2 + 100) × 50 : 2 = 2 550.'),
        lt(9, 3, 'Một dãy cách đều có số đầu 4, khoảng cách 6, gồm 12 số hạng. Tính '
                 'tổng của dãy.',
           'Số hạng cuối = 4 + 6 × 11 = 70. Tổng = (4 + 70) × 12 : 2 = 74 × 6 = 444.'),
        q_tf(1, 'Tổng dãy cách đều bằng số đầu cộng số cuối, nhân với số số hạng.',
             False, 'SAI — còn phải chia đôi, vì ghép cặp là đã cộng mỗi số hai lần.'),
        q_tf(2, 'Cách ghép cặp chỉ dùng được cho dãy cách đều.', True,
             'ĐÚNG — dãy không cách đều thì các cặp không còn bằng nhau.'),
        q_mcq(3, 'Tổng 1 + 2 + ... + 10 bằng:', ['A. 55', 'B. 50', 'C. 45'], 'A. 55',
              '(1 + 10) × 10 : 2 = 55.'),
        q_mcq(4, 'Muốn tính tổng một dãy cách đều, việc phải làm trước tiên là:',
              ['A. đếm số số hạng', 'B. cộng đầu với cuối', 'C. chia đôi'],
              'A. đếm số số hạng', 'Không biết số số hạng thì không có gì để nhân.'),
        q_mcq(5, 'Tổng 5 + 10 + 15 + 20 + 25 bằng:', ['A. 75', 'B. 150', 'C. 60'],
              'A. 75', '(5 + 25) × 5 : 2 = 75.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# B17 · MỘT SỐ CÓ THUỘC DÃY KHÔNG
# ═══════════════════════════════════════════════════════════════════════════
B17 = bai(
    17, 'SỐ NÀY CÓ THUỘC DÃY KHÔNG — VÀ ĐỨNG THỨ MẤY',
    'Dạng gốc: SỐ 5.1e mức Lớp 4 — Kiểm tra thuộc dãy bằng phép chia hết, và tìm vị trí.',
    'Lớp 3, ở Bài 11, con đã soi "ga này tàu có dừng không" bằng phép chia dư. Hôm '
    'nay việc ấy trở lại với đúng tên gọi của nó: cho một số bất kỳ, hỏi nó có nằm '
    'trong dãy không — và nếu có thì nó đứng ở chỗ thứ mấy.',
    LUI_GA,
    # ⚠ VIDEO THAY CẢ MỞ BÀI LẪN BÀI GIẢNG — bốn mục ②③④⑤ để RỖNG.
    # Cùng khuôn đã chốt ở Bài 13. Giữ ⑥ bài mẫu và ⑦ chỗ hay nhầm, nhưng viết
    # theo đúng đường video đi, và KHÔNG nhân vật nào.
    dung_muc(
        '',
        [],
        ['Kiểm tra được một số có nằm trong dãy hay không.',
         'Tìm được chỗ đứng của số ấy nếu nó thuộc dãy.',
         'Nhớ kiểm thêm: số ấy còn phải nằm trong dãy, không vượt quá số cuối.'],
        [],
        [],
        [],
        ['Đề bài: Số 45 có thuộc dãy 5 ; 10 ; 15 ; ... không? Nếu thuộc thì đứng thứ mấy?',
         'Trừ số đầu trước đã',
         '45 − 5 = 40.',
         'Chia cho khoảng cách',
         '40 : 5 = 8, chia hết.',
         'Chia hết nên số 45 thuộc dãy.',
         'Tìm chỗ đứng',
         'Phép chia cho ra 8, là số lần cộng thêm.',
         'Cộng thêm một: 8 + 1 = 9. Số 45 đứng thứ 9.',
         'Soi lại: 5 + 5 × 8 = 45, đúng.',
         'Đáp số: số 45 thuộc dãy và đứng thứ 9.'],
        ['Có bạn soi số 45 với dãy 5 ; 10 ; 15 ; ... như sau: "45 chia 5 được 9, chia '
         'hết, nên đứng thứ 9." Bạn ra đúng đáp số nhưng làm thiếu một bước.',
         'Gợi ý 1: Con thử cách ấy với dãy 3 ; 7 ; 11 ; ... và số 23 xem: 23 chia 4 '
         'dư 3, vậy là không thuộc dãy à? Nhưng đếm ra thì 23 có trong dãy đấy.',
         'Gợi ý 2: Trước khi chia, con phải làm gì với số đầu?',
         'Chữa: phải TRỪ SỐ ĐẦU trước đã, rồi mới chia. Dãy này bắt đầu từ 5 nên '
         '(45 − 5) : 5 = 8, chỗ đứng là 8 + 1 = 9.'],
        ['Mở tờ lịch, chỉ vào một Chủ nhật rồi hỏi con: "Ngày 25 có phải Chủ nhật '
         'không?" Cho con trừ rồi chia 7 để soi.',
         'Nhắc con một câu duy nhất: TRỪ SỐ ĐẦU TRƯỚC ĐÃ. Quên bước ấy là sai cả bài.'],
    ),
    # Bám đúng nấc video: trừ số đầu → chia khoảng cách → hết thì thuộc, dư thì
    # không → cộng một ra chỗ đứng → và còn phải nằm trong dãy.
    [
        lt(1, 1, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25 ; ... Muốn soi số 45, việc đầu tiên '
                 'là lấy 45 trừ số đầu. Được bao nhiêu?',
           '45 − 5 = 40.'),
        lt(2, 1, 'Lấy 40 vừa tìm được chia cho khoảng cách 5. Được bao nhiêu, và có '
                 'chia hết không?',
           '40 : 5 = 8, chia hết.'),
        lt(3, 1, 'Vậy số 45 có thuộc dãy 5 ; 10 ; 15 ; ... không? Nếu thuộc thì đứng '
                 'thứ mấy?',
           'Chia hết nên số 45 THUỘC dãy. Chỗ đứng = 8 + 1 = 9.'),
        lt(4, 2, 'Số 23 có thuộc dãy 3 ; 7 ; 11 ; ... không? Nếu thuộc thì đứng thứ mấy?',
           '(23 − 3) : 4 = 5, chia hết nên thuộc dãy, đứng thứ 6.'),
        lt(5, 2, 'Số 100 có thuộc dãy 3 ; 7 ; 11 ; ... không?',
           '(100 − 3) : 4 = 97 : 4 = 24 dư 1. Còn dư nên số 100 KHÔNG thuộc dãy.'),
        lt(6, 2, 'Số 52 có thuộc dãy 7 ; 12 ; 17 ; ... không? Nếu thuộc thì đứng thứ mấy?',
           '(52 − 7) : 5 = 9, chia hết nên thuộc dãy, đứng thứ 10.'),
        lt(7, 2, 'Số 30 có thuộc dãy 5 ; 10 ; 15 ; ... không? Nếu thuộc thì đứng thứ mấy?',
           '(30 − 5) : 5 = 5, chia hết nên thuộc dãy, đứng thứ 6.'),
        lt(8, 3, 'Cho dãy 5 ; 10 ; 15 ; 20 ; 25 — dãy này DỪNG ở 25. Số 45 có thuộc '
                 'dãy này không?',
           '(45 − 5) : 5 = 8 chia hết, nhưng 45 đã VƯỢT QUÁ số cuối 25, nên số 45 '
           'KHÔNG thuộc dãy này. Chia hết thôi chưa đủ.'),
        lt(9, 3, 'Cho dãy 4 ; 9 ; 14 ; ... ; 99. Số 64 có thuộc dãy không, và đứng '
                 'thứ mấy?',
           '(64 − 4) : 5 = 12 chia hết, và 64 nằm giữa 4 và 99 nên thuộc dãy, đứng '
           'thứ 13.'),
        q_tf(1, 'Muốn soi một số có thuộc dãy không, phải lấy số ấy trừ số đầu rồi '
                'mới chia cho khoảng cách.', True, 'Đáp án: ĐÚNG'),
        q_tf(2, 'Cứ chia hết cho khoảng cách là số ấy chắc chắn thuộc dãy.', False,
             'SAI — còn phải kiểm số ấy có nằm trong dãy không, đừng vượt quá số cuối.'),
        q_mcq(3, 'Số 45 với dãy 5 ; 10 ; 15 ; ...:',
              ['A. thuộc dãy, đứng thứ 9', 'B. không thuộc dãy', 'C. thuộc dãy, đứng thứ 8'],
              'A. thuộc dãy, đứng thứ 9', '(45 − 5) : 5 = 8, chỗ đứng là 8 + 1 = 9.'),
        q_mcq(4, 'Phép chia còn DƯ thì nghĩa là:',
              ['A. số ấy không thuộc dãy', 'B. số ấy thuộc dãy', 'C. số ấy là số cuối'],
              'A. số ấy không thuộc dãy', 'Còn dư nghĩa là nó rơi vào giữa hai số hạng.'),
        q_mcq(5, 'Số 30 với dãy 5 ; 10 ; 15 ; ... đứng ở chỗ thứ:',
              ['A. 6', 'B. 5', 'C. 7'], 'A. 6', '(30 − 5) : 5 = 5, chỗ đứng là 5 + 1 = 6.'),
    ],
)

MOI = [B13, B14, B15, B16, B17]

# ═══════════════════════════════════════════════════════════════════════════
# HÌNH — mỗi bài một hình MÀN MỞ (cổng lớp 4 đòi bài nào cũng có) và một hình
# KHÁM PHÁ cho bài khái niệm. Dùng lại đúng những `arch` quyển này đang có, không
# dựng kiểu vẽ mới: kiểu mới là thêm một chỗ có thể hỏng mà chưa ai soi bao giờ.
# ═══════════════════════════════════════════════════════════════════════════
def _o(t, mau):
    return {'t': str(t), 'mau': mau}


HINH_MOI = [
    # B13 — hai HÀNG chồng nhau là cách duy nhất cho bé THẤY "thứ mấy" khác "số
    # mấy": cùng một cột, hàng trên là chỗ đứng, hàng dưới là con số ở chỗ ấy.
    # B13 KHÔNG có hình màn mở: video đã thay cả mở bài lẫn bài giảng, nên một
    # hình mở bài nữa là thứ không bao giờ hiện ra — đúng nghĩa hình chết.
    {'id': 'L4H_B13_G1', 'arch': 'tia_so',
     'params': {'title': 'CÁCH ĐỀU LÀ GÌ — TRỪ LIÊN TIẾP XEM CÁC HIỆU CÓ BẰNG NHAU',
                'moc': [{'so': 7, 'danh': True}, {'so': 12}, {'so': 17}, {'so': 22},
                        {'so': 27}],
                'nhan': '+5',
                'note': 'Các hiệu đều bằng 5 → dãy cách đều, khoảng cách 5.'},
     'caption': 'Bước chân từ số hạng này sang số hạng kế luôn dài bằng nhau.',
     'bai': 'DL:KSN4.B13', 'muc': 'viDuMau', 'neoBuoc': 0, 'goc': 'B13 ⑥'},

    # B14 — tia số cho THẤY bước nhảy. Bốn chỗ nhưng chỉ ba bước: đó là cả bài.
    {'id': 'L4H_B14_MO', 'arch': 'tia_so',
     'params': {'title': 'BỐN BẬC THANG NHƯNG CHỈ BA LẦN LEO — BẬC THỨ 20 CAO BAO NHIÊU?',
                'moc': [{'so': 15, 'danh': True}, {'so': 30}, {'so': 45}, {'so': 60}],
                # KHÔNG có `note`: hình màn mở là bản ĐỀ. Dòng chốt ở đây là
                # cho không bé đáp án trước khi bé kịp nghĩ (chuẩn mục 6 luật 3) —
                # cổng lớp 4 bắt được ngay.
                'nhan': '+15'},
     'caption': 'Bậc thứ nhất đã đứng sẵn ở đó — không phải leo lần nào để tới nó.',
     'bai': 'DL:KSN4.B14', 'muc': 'chuyenMoBai', 'goc': 'B14 ②'},

    # B15 — hàng rào là hình duy nhất nói được "cột nhiều hơn khoảng đúng một"
    # mà không cần một chữ nào.
    {'id': 'L4H_B15_MO', 'arch': 'hang_cay',
     'params': {'title': 'HÀNG RÀO 40 M, CỨ 5 M MỘT CỘT, CẮM CẢ HAI ĐẦU — MẤY CÂY CỘT?',
                'so_cay': 9, 'khoang': '5 m'},
     'caption': '8 khoảng nhưng 9 cột — bác Tư hụt đúng một cây ở chỗ này.',
     'bai': 'DL:KSN4.B15', 'muc': 'chuyenMoBai', 'goc': 'B15 ②'},

    # B16 — xếp dãy xuôi trên, dãy ngược dưới; cột nào cộng lại cũng bằng nhau.
    # Nhìn một cái là hiểu vì sao phải chia 2.
    {'id': 'L4H_B16_MO', 'arch': 'day_o',
     'params': {'title': 'CÁCH CỦA GAUSS — VIẾT DÃY HAI LẦN, LẦN SAU VIẾT NGƯỢC',
                'hang': [{'nhan': 'xuôi', 'o': [_o(n, 'teal') for n in (1, 2, 3, 4, 5)]},
                         {'nhan': 'ngược', 'o': [_o(n, 'gold') for n in (5, 4, 3, 2, 1)]},
                         {'nhan': 'cộng cột', 'o': [_o(6, 'do') for _ in range(5)]}]},
     'caption': 'Cột nào cũng bằng 6 — vì cộng hai lần nên cuối cùng phải chia đôi.',
     'bai': 'DL:KSN4.B16', 'muc': 'chuyenMoBai', 'goc': 'B16 ②'},

    # B17 — đánh dấu số cần soi ngay trên tia, để bé thấy nó rơi ĐÚNG mốc hay
    # rơi vào giữa hai mốc.
    {'id': 'L4H_B17_MO', 'arch': 'tia_so',
     'params': {'title': 'VÉ SỐ 113 CÓ PHẢI GHẾ ĐẦU HÀNG KHÔNG?',
                'moc': [{'so': 1, 'danh': True}, {'so': 9}, {'so': 17}, {'so': 25}],
                'nhan': '+8'},
     'caption': 'Trừ số đầu trước đã, rồi mới chia cho khoảng cách.',
     'bai': 'DL:KSN4.B17', 'muc': 'chuyenMoBai', 'goc': 'B17 ②'},
]


# ═══════════════════════════════════════════════════════════════════════════
# Ô NHẬP CHẤM MÁY — luật 1 của `luat_o_nhap`: quyển đọc chậm KHÔNG được có ô gõ
# chữ, đáp án không phải số thì phải cho BẤM NÚT (`options`).
# ═══════════════════════════════════════════════════════════════════════════
CO_KHONG = ['có', 'không']

O_NHAP_MOI = {
    # ── B13 · đi theo video ──
    'DL:KSN4.B13#C1': {'value': 5},
    'DL:KSN4.B13#C2': {'value': 10},
    'DL:KSN4.B13#C3': {'value': 4},
    'DL:KSN4.B13#C4': {'parts': [{'label': 'số hạng thứ tư', 'value': 12},
                                 {'label': 'số 9 đứng thứ', 'value': 3}]},
    'DL:KSN4.B13#C5': {'parts': [{'label': 'bạn An nói', 'options': ['đúng', 'sai'],
                                  'value': 'sai'},
                                 {'label': 'số 24 đứng thứ', 'value': 3}]},
    'DL:KSN4.B13#C6': {'parts': [{'label': 'số sau trừ số trước bằng', 'value': 5},
                                 {'label': 'dãy có cách đều không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B13#C7': {'parts': [{'label': 'dãy cách đều là', 'options': ['dãy A', 'dãy B'],
                                  'value': 'dãy A'}]},
    'DL:KSN4.B13#C8': {'parts': [{'label': 'khoảng cách', 'value': 5},
                                 {'label': 'số hạng thứ tư', 'value': 22},
                                 {'label': 'số 17 đứng thứ', 'value': 3}]},
    'DL:KSN4.B13#C9': {'parts': [{'label': 'dãy có cách đều không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'khoảng cách', 'value': 10}]},

    # ── B14 · số hạng thứ n (theo video) ──
    'DL:KSN4.B14#C1': {'value': 3},
    'DL:KSN4.B14#C2': {'parts': [{'label': 'khoảng cách', 'value': 5},
                                 {'label': 'số hạng thứ tư', 'value': 20}]},
    'DL:KSN4.B14#C3': {'value': 30},
    'DL:KSN4.B14#C4': {'value': 50},
    'DL:KSN4.B14#C5': {'value': 31},
    'DL:KSN4.B14#C6': {'value': 46},
    'DL:KSN4.B14#C7': {'value': 5},
    'DL:KSN4.B14#C8': {'value': 500},
    'DL:KSN4.B14#C9': {'value': 7},

    # ── B15 · đếm số số hạng (theo video) ──
    'DL:KSN4.B15#C1': {'value': 20},
    'DL:KSN4.B15#C2': {'value': 4},
    'DL:KSN4.B15#C3': {'value': 5},
    'DL:KSN4.B15#C4': {'value': 20},
    'DL:KSN4.B15#C5': {'value': 50},
    'DL:KSN4.B15#C6': {'value': 20},
    'DL:KSN4.B15#C7': {'value': 9},
    'DL:KSN4.B15#C8': {'value': 20},
    'DL:KSN4.B15#C9': {'value': 102},

    # ── B16 · tổng dãy (theo video) ──
    'DL:KSN4.B16#C1': {'value': 30},
    'DL:KSN4.B16#C2': {'value': 30},
    'DL:KSN4.B16#C3': {'value': 75},
    'DL:KSN4.B16#C4': {'value': 55},
    'DL:KSN4.B16#C5': {'value': 1275},
    'DL:KSN4.B16#C6': {'value': 1050},
    'DL:KSN4.B16#C7': {'value': 165},
    'DL:KSN4.B16#C8': {'value': 2550},
    'DL:KSN4.B16#C9': {'value': 444},

    # ── B17 · thuộc dãy không (theo video) ──
    'DL:KSN4.B17#C1': {'value': 40},
    'DL:KSN4.B17#C2': {'parts': [{'label': 'kết quả phép chia', 'value': 8},
                                 {'label': 'có chia hết không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B17#C3': {'parts': [{'label': 'số 45 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 9}]},
    'DL:KSN4.B17#C4': {'parts': [{'label': 'số 23 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 6}]},
    'DL:KSN4.B17#C5': {'parts': [{'label': 'số 100 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'không'}]},
    'DL:KSN4.B17#C6': {'parts': [{'label': 'số 52 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 10}]},
    'DL:KSN4.B17#C7': {'parts': [{'label': 'số 30 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 6}]},
    'DL:KSN4.B17#C8': {'parts': [{'label': 'số 45 có thuộc dãy NÀY không', 'options': CO_KHONG,
                                  'value': 'không'}]},
    'DL:KSN4.B17#C9': {'parts': [{'label': 'số 64 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 13}]},

}


def soi():
    """Tự soi trước khi ghi — mấy chỗ dưới đây đều là luật đã có cổng canh."""
    loi = []
    for b in MOI:
        n = b['so']
        lt_ = [c for c in b['cau'] if c['phan'] == 'luyenTap']
        qz = [c for c in b['cau'] if c['phan'] == 'quiz']
        if len(lt_) != 9:
            loi.append(f'B{n}: {len(lt_)} câu luyện tập, phải đúng 9')
        if len(qz) != 5:
            loi.append(f'B{n}: {len(qz)} câu quiz, phải đúng 5')
        if [c['muc'] for c in lt_] != [1, 1, 1, 2, 2, 2, 2, 3, 3]:
            loi.append(f'B{n}: mức sao luyện tập không đúng 1,1,1,2,2,2,2,3,3')
        for m in ('mucTieu', 'chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi',
                  'viDuMau', 'suKemNham', 'luyenTap', 'quiz', 'gocBoMe'):
            if m not in b['muc']:
                loi.append(f'B{n}: thiếu mục {m}')
        for c in lt_:
            if f'{b["id"]}#{c["id"]}' not in O_NHAP_MOI:
                loi.append(f'B{n}: câu {c["id"]} chưa có ô nhập chấm máy')
        # đáp án bấm chọn phải nằm trong danh sách nút (luật 3)
        for c in qz:
            if c.get('format') == 'mcq' and c['answerKey']['choice'] not in c['choices']:
                loi.append(f'B{n}: quiz {c["id"]} đáp án không có trong danh sách nút')
    # Bài khái niệm KHÔNG được có công thức
    kham = ' '.join(B13['muc']['khamPha']['dong'])
    if '(n − 1)' in kham or 'n − 1)' in kham:
        loi.append('B13 là bài KHÁI NIỆM, không được có công thức số hạng thứ n')
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
        lt_ = sum(1 for c in b['cau'] if c['phan'] == 'luyenTap')
        qz = sum(1 for c in b['cau'] if c['phan'] == 'quiz')
        print(f"  {b['id']}  Bài {b['so']} · {b['ten'][:44]:44} {lt_} luyện + {qz} quiz")
        if not a.xem:
            (RA / f"DL_KSN4_B{b['so']:02d}.json").write_text(
                json.dumps(b, ensure_ascii=False, indent=1) + '\n', 'utf8')

    if a.xem:
        print('\n(--xem: chưa ghi gì)')
        return

    mt = GOC / 'data' / 'lop4_hinh.json'
    ds = json.loads(mt.read_text('utf8'))
    co = {m['id'] for m in ds}
    them = [h for h in HINH_MOI if h['id'] not in co]
    ds += them
    mt.write_text(json.dumps(ds, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'thêm {len(them)} mô tả hình vào {mt.relative_to(GOC)} (nay {len(ds)} hình)')

    o = json.loads(O_NHAP.read_text('utf8'))
    o.update(O_NHAP_MOI)
    O_NHAP.write_text(json.dumps(o, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'\nghi {len(MOI)} bài vào {RA.relative_to(GOC)}')
    print(f'thêm {len(O_NHAP_MOI)} ô nhập vào {O_NHAP.relative_to(GOC)} (nay {len(o)} mục)')


if __name__ == '__main__':
    main()
