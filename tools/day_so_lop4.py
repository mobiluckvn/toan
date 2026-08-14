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
    dung_muc(
        'Con phố nhà bạn Mai',
        ['Bạn Mai chỉ tay xuống dãy nhà bên trái: "Nhà tớ là nhà thứ tư từ đầu phố."',
         'Cậu bé giao báo gãi đầu: "Nhà thứ tư… nhưng số nhà là bao nhiêu ạ? Tớ chỉ '
         'biết bấm chuông theo SỐ NHÀ thôi."',
         'Mai đọc dãy số nhà bên ấy: 6 ; 11 ; 16 ; 21 ; 26 ; 31.',
         'Vậy nhà THỨ TƯ mang số mấy? Và ngược lại, nhà số 26 là nhà THỨ MẤY?'],
        ['Gọi đúng tên bốn thứ: dãy số, số hạng, vị trí (thứ mấy) và giá trị (số mấy).',
         'Nhìn một dãy và nói được: dãy này có CÁCH ĐỀU không, KHOẢNG CÁCH bằng bao nhiêu.',
         'Trả lời được hai câu ngược nhau: "chỗ thứ n là số nào" và "số x đứng thứ mấy".'],
        ['CHO GÌ? dãy số nhà bên trái phố: 6 ; 11 ; 16 ; 21 ; 26 ; 31.',
         'HỎI GÌ? nhà thứ tư mang số mấy; nhà số 26 đứng thứ mấy.',
         'ĐẠI LƯỢNG & ĐƠN VỊ: hai loại số hoàn toàn khác nhau — VỊ TRÍ đếm bằng '
         '"thứ nhất, thứ hai, thứ ba…", còn GIÁ TRỊ là con số sơn trên cửa. Đây '
         'chính là chỗ cậu giao báo bị rối, và cũng là chỗ bé hay nhầm nhất.',
         'QUAN HỆ GIỮA CHÚNG: mỗi vị trí ứng với đúng MỘT giá trị. Vị trí 1 ↔ số 6; '
         'vị trí 2 ↔ số 11; vị trí 3 ↔ số 16…',
         'CHỌN CÔNG CỤ: bài này CHƯA cần công thức nào. Chỉ cần đọc dãy và đếm cho '
         'đúng chỗ. Công thức để dành bốn bài sau.',
         'ƯỚC LƯỢNG TRƯỚC: số nhà cứ tăng dần, nhà thứ tư chắc chắn lớn hơn 16 và '
         'nhỏ hơn 26.'],
        ['Bước 1 — DÃY SỐ LÀ GÌ. Một DÃY SỐ là mấy con số viết nối nhau THEO MỘT THỨ '
         'TỰ đã định, ngăn nhau bằng dấu chấm phẩy: 6 ; 11 ; 16 ; 21 ; 26 ; 31. Mỗi '
         'con số trong dãy gọi là một SỐ HẠNG. Dãy trên có 6 số hạng. Thứ tự là phần '
         'quan trọng: đảo chỗ hai số là thành một dãy KHÁC.',
         'Bước 2 — MỘT SỐ HẠNG CÓ HAI CON SỐ ĐI KÈM, và đây là chỗ dễ nhầm nhất của '
         'cả chương. VỊ TRÍ (còn gọi là SỐ THỨ TỰ) cho biết số hạng ấy đứng THỨ MẤY: '
         'thứ nhất, thứ hai, thứ ba… GIÁ TRỊ cho biết số hạng ấy LÀ SỐ NÀO. Nhà thứ '
         'tư có giá trị 21 — "thứ tư" và "21" cùng nói về một ngôi nhà, nhưng KHÔNG '
         'phải một con số. Hỏi "thứ mấy" thì đếm chỗ; hỏi "số mấy" thì đọc giá trị.',
         'Bước 3 — CÁCH ĐỀU LÀ GÌ. Lấy mỗi số hạng TRỪ số hạng ĐỨNG NGAY TRƯỚC nó: '
         '11 − 6 = 5 ; 16 − 11 = 5 ; 21 − 16 = 5 ; 26 − 21 = 5 ; 31 − 26 = 5. Năm '
         'hiệu đều bằng 5 — dãy này CÁCH ĐỀU, và con số 5 ấy gọi là KHOẢNG CÁCH của '
         'dãy. Nói cách khác: từ một nhà sang nhà ngay bên cạnh, số nhà luôn tăng '
         'đúng 5 đơn vị.',
         'Bước 4 — THỬ TAY HAI DÃY. Dãy 3 ; 6 ; 9 ; 12 : hiệu lần lượt 3 ; 3 ; 3 → '
         'CÁCH ĐỀU, khoảng cách 3. Dãy 1 ; 2 ; 4 ; 8 : hiệu lần lượt 1 ; 2 ; 4 → các '
         'hiệu KHÁC nhau, nên KHÔNG cách đều (dãy này có quy luật khác — mỗi số gấp '
         'đôi số trước — nhưng đó là chuyện của bài sau).',
         'Bước 5 — DÃY GIẢM CŨNG CÁCH ĐỀU ĐƯỢC. 100 ; 95 ; 90 ; 85 có hiệu −5 mỗi '
         'bước, đều tăm tắp → vẫn là dãy cách đều, khoảng cách 5, chỉ khác là bước '
         'LÙI chứ không bước tới.',
         'MẸO NGƯỜI GIẢI: gặp một dãy lạ, làm đúng ba việc theo thứ tự — (1) đếm xem '
         'có mấy số hạng; (2) trừ liên tiếp xem các hiệu có bằng nhau không; (3) nếu '
         'bằng nhau thì ghi ngay KHOẢNG CÁCH ra lề. Ba việc ấy xong là nhận diện xong.'],
        ['LẮP: cậu giao báo dán vào ghi đông xe một mảnh giấy: "Phố này số nhà bắt '
         'đầu từ 6, cách đều 5. Nhà thứ tư = số 21." Từ hôm ấy cậu bấm chuông không '
         'sai nhà nào nữa.',
         'SOI: soi ngược lại cho chắc — nhà số 26 đứng thứ mấy? Đếm từ đầu: 6 (thứ '
         '1) → 11 (thứ 2) → 16 (thứ 3) → 21 (thứ 4) → 26 (thứ 5) ✓. Hỏi xuôi ra 21, '
         'hỏi ngược ra thứ 5 — hai chiều đều thông thì mới thật là hiểu.',
         'DÙNG NGOÀI ĐỜI: số nhà chẵn - lẻ trên phố, bậc thang đánh số, cột cây số '
         'bên đường, các ngày thứ Bảy trong tờ lịch — chỗ nào cũng có dãy cách đều, '
         'và chỗ nào cũng phân biệt "thứ mấy" với "số mấy".'],
        ['Đề bài: Cho dãy 7 ; 12 ; 17 ; 22 ; 27. Dãy này có cách đều không? Nếu có '
         'thì khoảng cách bằng bao nhiêu? Số hạng thứ 3 là số nào? Số 27 đứng thứ mấy?',
         'Tóm tắt',
         'Dãy 5 số hạng: 7 ; 12 ; 17 ; 22 ; 27.',
         'Viết dãy ra giấy, đánh số vị trí 1, 2, 3, 4, 5 ngay bên dưới từng số hạng.',
         'Kiểm cách đều',
         '12 − 7 = 5 ; 17 − 12 = 5 ; 22 − 17 = 5 ; 27 − 22 = 5.',
         'Bốn hiệu bằng nhau → dãy CÁCH ĐỀU, khoảng cách 5.',
         'Đọc hai chiều',
         'Vị trí 3 → nhìn xuống hàng vị trí, thấy số 17. Số hạng thứ 3 là 17.',
         'Số 27 → nhìn lên hàng vị trí, thấy số 5. Số 27 đứng thứ 5.',
         'Đáp số: dãy cách đều, khoảng cách 5; số hạng thứ 3 là 17; số 27 đứng thứ 5.'],
        ['Cô hỏi "nhà thứ tư mang số mấy?", Trí Long đáp ngay: "Thứ tư thì là số 4 ạ!"',
         'Gợi ý 1: Con thử đọc lại dãy số nhà xem — 6 ; 11 ; 16 ; 21 ; 26 ; 31. Có số '
         '4 nào trong đó không?',
         'Gợi ý 2: "Thứ tư" là CHỖ ĐỨNG, còn "số nhà" là con số sơn trên cửa. Hai '
         'thứ khác nhau. Con chỉ tay vào chỗ thứ tư rồi đọc to số ở đó xem.',
         'Chữa: nhà thứ tư là nhà mang số 21. Vị trí 4 ≠ giá trị 4.'],
        ['Đi bộ cùng con dọc một dãy nhà, đọc to số nhà rồi hỏi: "Nhà mình là nhà '
         'thứ mấy tính từ đầu phố?" — cho con tự đếm và tự nói ra hai con số khác nhau.',
         'Mở tờ lịch tháng, khoanh tất cả các ngày Chủ nhật: 3 ; 10 ; 17 ; 24 ; 31. '
         'Hỏi con: dãy này cách đều không? Khoảng cách mấy? Chủ nhật thứ ba là ngày mấy?',
         'Chưa cần công thức nào ở bài này. Con gọi đúng tên và chỉ đúng chỗ là đạt.'],
    ),
    [
        lt(1, 1, 'Cho dãy 4 ; 8 ; 12 ; 16 ; 20. Dãy có mấy số hạng? Số hạng thứ 3 là số nào?',
           'Dãy có 5 số hạng; số hạng thứ 3 là 12.'),
        lt(2, 1, 'Vẫn dãy 4 ; 8 ; 12 ; 16 ; 20. Số 20 đứng ở vị trí thứ mấy?',
           'Đếm từ đầu: 4 (1) ; 8 (2) ; 12 (3) ; 16 (4) ; 20 (5). Số 20 đứng thứ 5.'),
        lt(3, 1, 'Cho dãy 7 ; 10 ; 13 ; 16. Dãy này có cách đều không? Khoảng cách bằng mấy?',
           'Các hiệu: 10 − 7 = 3 ; 13 − 10 = 3 ; 16 − 13 = 3 — bằng nhau, nên dãy '
           'cách đều, khoảng cách 3.'),
        lt(4, 2, 'Trong hai dãy sau, dãy nào CÁCH ĐỀU: dãy A là 2 ; 4 ; 6 ; 8 hay '
                 'dãy B là 2 ; 4 ; 8 ; 16?',
           'Dãy A: hiệu 2 ; 2 ; 2 — cách đều. Dãy B: hiệu 2 ; 4 ; 8 — không bằng nhau '
           'nên KHÔNG cách đều.'),
        lt(5, 2, 'Cho dãy 100 ; 95 ; 90 ; 85 ; 80. Dãy này có cách đều không? Khoảng cách mấy?',
           'Mỗi bước lùi đúng 5 đơn vị, đều tăm tắp → vẫn là dãy cách đều, khoảng cách 5.'),
        lt(6, 2, 'Cho dãy cách đều 5 ; 10 ; 15 ; ... Hãy viết tiếp và cho biết số hạng '
                 'thứ 6 là số nào.',
           'Viết tiếp: 20 ; 25 ; 30. Số hạng thứ 6 là 30.'),
        lt(7, 2, 'Bạn Mai nói: "Trong dãy 6 ; 11 ; 16 ; 21 ; 26, số 16 đứng thứ 16." '
                 'Bạn nói đúng hay sai? Vì sao?',
           'SAI. Số 16 là GIÁ TRỊ, còn vị trí của nó là thứ 3. Vị trí và giá trị là '
           'hai con số khác nhau.'),
        lt(8, 3, 'Cho dãy 3 ; 7 ; 11 ; 15 ; 19 ; 23. Cho biết: khoảng cách của dãy; '
                 'số hạng thứ 5; và số 11 đứng thứ mấy.',
           'Khoảng cách 4; số hạng thứ 5 là 19; số 11 đứng thứ 3.'),
        lt(9, 3, 'Một dãy cách đều bắt đầu bằng 2, khoảng cách 4. Hãy viết 5 số hạng '
                 'đầu tiên của dãy, rồi cho biết số hạng thứ 5 là số nào.',
           'Dãy: 2 ; 6 ; 10 ; 14 ; 18. Số hạng thứ 5 là 18.'),
        q_tf(1, 'Mỗi con số trong một dãy số được gọi là một SỐ HẠNG.', True,
             'Đáp án: ĐÚNG'),
        q_tf(2, 'Trong dãy 6 ; 11 ; 16 ; 21, số 16 đứng ở vị trí thứ 16.', False,
             'SAI — số 16 là GIÁ TRỊ, còn vị trí của nó là thứ 3.'),
        q_mcq(3, 'Dãy nào dưới đây là dãy CÁCH ĐỀU?',
              ['A. 1 ; 3 ; 5 ; 7', 'B. 1 ; 2 ; 4 ; 8', 'C. 1 ; 4 ; 9 ; 16'],
              'A. 1 ; 3 ; 5 ; 7', 'Dãy A có các hiệu đều bằng 2.'),
        q_mcq(4, 'Dãy 9 ; 14 ; 19 ; 24 có khoảng cách bằng:',
              ['A. 5', 'B. 4', 'C. 9'], 'A. 5',
              '14 − 9 = 5, và các hiệu sau cũng đều bằng 5.'),
        q_mcq(5, 'Trong dãy 8 ; 12 ; 16 ; 20 ; 24, số hạng thứ 4 là:',
              ['A. 20', 'B. 4', 'C. 16'], 'A. 20',
              'Đếm chỗ: 8 (1) ; 12 (2) ; 16 (3) ; 20 (4).'),
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
    dung_muc(
        'Bậc thang lên đài quan sát',
        ['Đài quan sát có một cầu thang dài. Bậc thứ nhất cao 15 cm so với mặt đất, '
         'và cứ mỗi bậc lại cao thêm đúng 15 cm.',
         'Bác bảo vệ hỏi con: "Cháu đứng ở bậc thứ 20 thì cao bao nhiêu so với mặt đất?"',
         'Viết cả 20 bậc ra giấy thì được, nhưng nếu bác hỏi bậc thứ 200 thì sao?'],
        ['Hiểu vì sao đi từ vị trí 1 đến vị trí n chỉ có n − 1 bước nhảy, không phải n.',
         'Dùng được công thức: số hạng thứ n = số đầu + khoảng cách × (n − 1).',
         'Tìm số hạng ở vị trí xa mà không phải viết cả dãy.'],
        ['CHO GÌ? bậc thứ nhất cao 15 cm; mỗi bậc thêm 15 cm → dãy độ cao: 15 ; 30 ; 45 ; ...',
         'HỎI GÌ? bậc thứ 20 cao bao nhiêu.',
         'ĐẠI LƯỢNG & ĐƠN VỊ: độ cao tính bằng xăng-ti-mét, còn số bậc là vị trí — '
         'đúng hai thứ con vừa phân biệt ở bài trước.',
         'QUAN HỆ GIỮA CHÚNG: dãy độ cao là dãy CÁCH ĐỀU, số đầu 15, khoảng cách 15.',
         'CHỌN CÔNG CỤ: công thức SỐ HẠNG THỨ n. Đây là công thức DUY NHẤT của bài này.',
         'ƯỚC LƯỢNG TRƯỚC: 20 bậc, mỗi bậc 15 cm, chắc khoảng ba trăm mấy — nếu tính '
         'ra 4 000 cm thì biết ngay là sai.'],
        ['Bước 1 — ĐẾM BƯỚC NHẢY, KHÔNG ĐẾM CHỖ. Đây là chỗ tinh tế nhất của cả bài, '
         'và cũng là chỗ hầu hết bạn sai. Từ bậc 1 lên bậc 4 thì leo mấy lần? Vẽ ra '
         'mà đếm: 1 → 2 (một lần) → 3 (hai lần) → 4 (BA lần). Bốn bậc nhưng chỉ BA '
         'lần leo. Số bước nhảy luôn ÍT HƠN số chỗ đúng 1.',
         'Bước 2 — VÌ SAO ÍT HƠN 1. Vì bậc thứ nhất con ĐÃ ĐỨNG SẴN ở đó rồi, không '
         'phải leo lần nào để tới nó. Chỉ từ bậc 2 trở đi mới cần leo. Cũng như hàng '
         'rào: 5 cây cột thì chỉ có 4 khoảng ở giữa.',
         'Bước 3 — GHÉP THÀNH CÔNG THỨC. Muốn tới vị trí n thì nhảy n − 1 bước, mỗi '
         'bước cộng thêm đúng một KHOẢNG CÁCH. Vậy: số hạng thứ n = số đầu + khoảng '
         'cách × (n − 1).',
         'Bước 4 — GIẢI BÀI BẬC THANG. Số đầu 15, khoảng cách 15, n = 20 → bậc thứ 20 '
         'cao 15 + 15 × (20 − 1) = 15 + 15 × 19 = 15 + 285 = 300 (cm), tức là 3 mét. '
         'Khớp với ước lượng "ba trăm mấy" ✓.',
         'Bước 5 — THỬ NGƯỢC CHO CHẮC. Thay n = 1 vào công thức: 15 + 15 × (1 − 1) = '
         '15 + 0 = 15 ✓ — đúng bằng số hạng đầu. Một công thức tốt phải đúng ngay ở '
         'chỗ dễ nhất; thử n = 1 là cách soi nhanh nhất xem mình có nhớ nhầm dấu trừ '
         'không.',
         'MẸO NGƯỜI GIẢI: viết công thức ra lề rồi khoanh tròn chữ (n − 1). Mỗi lần '
         'thay số, tính (n − 1) TRƯỚC, xong mới nhân.'],
        ['LẮP: con dán lên chân cầu thang một tấm bảng nhỏ: "Bậc thứ n cao 15 × (n − 1) '
         '+ 15 cm". Bác bảo vệ hỏi bậc nào cũng đáp được ngay, không cần leo thử.',
         'SOI: soi chéo bằng đường khác — 20 bậc, mỗi bậc 15 cm, nhưng bậc đầu tiên '
         'đã cao sẵn 15 cm và còn 19 lần leo nữa: 15 × 20 = 300 cm. Hai con đường '
         'cùng ra 300 ✓.',
         'DÙNG NGOÀI ĐỜI: tiền tiết kiệm mỗi tuần bỏ thêm một khoản bằng nhau, số ghế '
         'đầu mỗi hàng trong rạp, cột cây số trên quốc lộ — hỏi "cái thứ n" là dùng '
         'đúng công thức này.'],
        ['Đề bài: Tìm số hạng thứ 20 của dãy 3 ; 7 ; 11 ; 15 ; ...',
         'Tóm tắt',
         'Dãy cách đều, số đầu 3, khoảng cách 4, cần tìm số hạng thứ 20.',
         'Kiểm khoảng cách trước: 7 − 3 = 4 ; 11 − 7 = 4 ; 15 − 11 = 4 ✓.',
         'Mô hình (đếm bước nhảy)',
         'Từ vị trí 1 đến vị trí 20 có 20 − 1 = 19 bước nhảy.',
         'Mỗi bước cộng thêm 4, nên tất cả cộng thêm 4 × 19 = 76.',
         'Tính',
         'Số hạng thứ 20 = 3 + 4 × (20 − 1) = 3 + 4 × 19 = 3 + 76 = 79.',
         'Soi lại: thay n = 1 → 3 + 4 × 0 = 3 ✓ đúng số đầu.',
         'Đáp số: số hạng thứ 20 là 79.'],
        ['Cô hỏi số hạng thứ 20 của dãy 3 ; 7 ; 11 ; ..., Trí Long bấm máy: '
         '"Khoảng cách 4, vị trí 20, vậy lấy 3 + 4 × 20 = 83 ạ!"',
         'Gợi ý 1: Con thử công thức của Trí Long với vị trí thứ NHẤT xem: 3 + 4 × 1 '
         '= 7. Nhưng số hạng thứ nhất rõ ràng là 3 mà?',
         'Gợi ý 2: Từ chỗ thứ nhất đến chỗ thứ 20, con nhảy 20 bước hay 19 bước? Vẽ '
         'bốn chỗ ra mà đếm thử.',
         'Chữa: phải nhân với (20 − 1) = 19, không nhân với 20. Số hạng thứ 20 = '
         '3 + 4 × 19 = 79. Nhớ: ĐẾM BƯỚC NHẢY, KHÔNG ĐẾM CHỖ.'],
        ['Đứng ở chân cầu thang nhà mình, cho con đo chiều cao một bậc rồi hỏi: "Bậc '
         'thứ 8 cao bao nhiêu?" — bắt con tính trước, rồi cùng đo lại để kiểm.',
         'Mẹo kiểm nhanh cho bố mẹ: bảo con thay n = 1 vào công thức con vừa viết. Ra '
         'đúng số đầu thì công thức đúng; ra số khác là con nhớ nhầm dấu trừ.'],
    ),
    [
        lt(1, 1, 'Dãy 5 ; 10 ; 15 ; ... có khoảng cách bằng mấy? Từ vị trí 1 đến vị trí '
                 '10 có bao nhiêu bước nhảy?',
           'Khoảng cách 5; từ vị trí 1 đến vị trí 10 có 10 − 1 = 9 bước nhảy.'),
        lt(2, 1, 'Tìm số hạng thứ 10 của dãy 5 ; 10 ; 15 ; ...',
           '5 + 5 × (10 − 1) = 5 + 45 = 50.'),
        lt(3, 1, 'Tìm số hạng thứ 8 của dãy 2 ; 6 ; 10 ; ...',
           '2 + 4 × (8 − 1) = 2 + 28 = 30.'),
        lt(4, 2, 'Tìm số hạng thứ 20 của dãy 3 ; 7 ; 11 ; ...',
           '3 + 4 × (20 − 1) = 3 + 76 = 79.'),
        lt(5, 2, 'Tìm số hạng thứ 15 của dãy 1 ; 9 ; 17 ; 25 ; ...',
           '1 + 8 × (15 − 1) = 1 + 112 = 113.'),
        lt(6, 2, 'Một dãy cách đều có số đầu 6, khoảng cách 7. Số hạng thứ 12 là số nào?',
           '6 + 7 × (12 − 1) = 6 + 77 = 83.'),
        lt(7, 2, 'Bậc thứ nhất của cầu thang cao 15 cm, mỗi bậc cao thêm 15 cm. Bậc '
                 'thứ 20 cao bao nhiêu xăng-ti-mét?',
           '15 + 15 × (20 − 1) = 15 + 285 = 300 (cm).'),
        lt(8, 3, 'Dãy 4 ; 11 ; 18 ; ... Tìm số hạng thứ 30, rồi thử lại công thức với '
                 'n = 1 xem có ra đúng số đầu không.',
           'Số hạng thứ 30 = 4 + 7 × 29 = 4 + 203 = 207. Thử n = 1: 4 + 7 × 0 = 4 ✓ '
           'đúng bằng số đầu.'),
        lt(9, 3, 'Số hạng thứ 6 của một dãy cách đều là 32, khoảng cách của dãy là 5. '
                 'Hỏi số hạng ĐẦU của dãy là số nào?',
           'Từ vị trí 1 đến vị trí 6 có 5 bước nhảy, cộng thêm 5 × 5 = 25. Vậy số đầu '
           '= 32 − 25 = 7.'),
        q_tf(1, 'Số hạng thứ n của dãy cách đều bằng số đầu + khoảng cách × (n − 1).',
             True, 'Đáp án: ĐÚNG'),
        q_tf(2, 'Từ vị trí thứ nhất đến vị trí thứ 10 có 10 bước nhảy.', False,
             'SAI — chỉ có 9 bước nhảy, vì vị trí thứ nhất đã đứng sẵn ở đó.'),
        q_mcq(3, 'Số hạng thứ 12 của dãy 2 ; 5 ; 8 ; ... là:',
              ['A. 35', 'B. 38', 'C. 32'], 'A. 35', '2 + 3 × (12 − 1) = 2 + 33 = 35.'),
        q_mcq(4, 'Thay n = 1 vào công thức số hạng thứ n, kết quả phải bằng:',
              ['A. số đầu của dãy', 'B. khoảng cách', 'C. số 1'], 'A. số đầu của dãy',
              'Vì (1 − 1) = 0 nên không cộng thêm bước nào — ra đúng số đầu.'),
        q_mcq(5, 'Dãy 1 ; 9 ; 17 ; 25 ; ... có số hạng thứ 15 là:',
              ['A. 113', 'B. 120', 'C. 105'], 'A. 113', '1 + 8 × 14 = 1 + 112 = 113.'),
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
    dung_muc(
        'Hàng rào nhà bác Tư',
        ['Bác Tư đóng một hàng rào thẳng dài 40 mét, cứ 5 mét cắm một cây cột, cột '
         'đầu tiên cắm ngay đầu hàng rào và cột cuối cùng cắm ngay cuối.',
         'Bác nhẩm: "40 chia 5 bằng 8, vậy mua 8 cây cột là đủ."',
         'Cắm xong bác đếm lại thì thiếu mất một cây. Bác thiếu ở đâu?'],
        ['Hiểu vì sao đếm số hạng thì phải CỘNG 1, trong khi tìm số hạng thứ n lại TRỪ 1.',
         'Dùng được công thức: số số hạng = (số cuối − số đầu) : khoảng cách + 1.',
         'Biết soi lại kết quả bằng cách đếm tay trên một dãy ngắn.'],
        ['CHO GÌ? hàng rào dài 40 m, mỗi 5 m một cột, cắm cả hai đầu.',
         'HỎI GÌ? cần bao nhiêu cây cột.',
         'ĐẠI LƯỢNG & ĐƠN VỊ: chiều dài tính bằng mét, còn cột đếm bằng cây — hai thứ '
         'khác nhau, chớ lẫn.',
         'QUAN HỆ GIỮA CHÚNG: vị trí các cột tạo thành dãy cách đều 0 ; 5 ; 10 ; ... ; 40, '
         'khoảng cách 5. Số cột chính là SỐ SỐ HẠNG của dãy ấy.',
         'CHỌN CÔNG CỤ: công thức ĐẾM SỐ SỐ HẠNG. Đây là công thức duy nhất của bài này.',
         'ƯỚC LƯỢNG TRƯỚC: 8 khoảng thì cột phải nhiều hơn 8 một chút — bác Tư hụt '
         'đúng chỗ đó.'],
        ['Bước 1 — CỘT VÀ KHOẢNG LÀ HAI THỨ KHÁC NHAU. Vẽ một hàng rào ngắn ra giấy: '
         '3 cây cột thì có mấy khoảng ở giữa? Đếm mà xem — chỉ 2 khoảng. 4 cột thì 3 '
         'khoảng. Số KHOẢNG luôn ít hơn số CỘT đúng 1, vì hai đầu đều là cột.',
         'Bước 2 — PHÉP CHIA CHO RA SỐ KHOẢNG, KHÔNG PHẢI SỐ CỘT. Bác Tư lấy 40 : 5 = 8 '
         '— con số 8 ấy là số KHOẢNG, đúng chứ không sai. Bác chỉ quên mất rằng còn '
         'phải thêm một cây cột cho cái đầu hàng rào. Vậy số cột = 8 + 1 = 9 cây.',
         'Bước 3 — GHÉP THÀNH CÔNG THỨC. Với một dãy cách đều: (số cuối − số đầu) cho '
         'ra "cả quãng đường", chia cho khoảng cách thì ra SỐ BƯỚC NHẢY, rồi cộng 1 để '
         'đếm cả số hạng đầu tiên. Vậy: số số hạng = (số cuối − số đầu) : khoảng cách + 1.',
         'Bước 4 — GIẢI BÀI HÀNG RÀO. Dãy vị trí cột: 0 ; 5 ; 10 ; ... ; 40. Số cột = '
         '(40 − 0) : 5 + 1 = 8 + 1 = 9 cây ✓.',
         'Bước 5 — VÌ SAO BÀI TRƯỚC TRỪ 1 MÀ BÀI NÀY CỘNG 1. Hai câu hỏi ngược nhau '
         'nên hai phép ngược nhau. Bài trước: biết SỐ CHỖ, tìm SỐ BƯỚC → bớt đi 1. Bài '
         'này: biết SỐ BƯỚC, tìm SỐ CHỖ → thêm vào 1. Nhớ một câu là đủ: CHỖ nhiều '
         'hơn BƯỚC đúng một.',
         'MẸO NGƯỜI GIẢI: tính xong luôn thử lại trên một dãy NGẮN mà đếm tay được. '
         'Dãy 2 ; 4 ; 6 ; 8 : công thức cho (8 − 2) : 2 + 1 = 4 ✓ — đếm tay cũng 4.'],
        ['LẮP: bác Tư mua thêm một cây cột nữa là vừa khít. Bác ghi vào sổ: "Cắm cả '
         'hai đầu thì SỐ CỘT = SỐ KHOẢNG + 1."',
         'SOI: soi lại bằng cách đếm tay đoạn ngắn — hàng rào 10 m, mỗi 5 m một cột: '
         'cột ở 0, ở 5, ở 10 → 3 cây. Công thức: (10 − 0) : 5 + 1 = 2 + 1 = 3 ✓.',
         'DÙNG NGOÀI ĐỜI: trồng cây hai bên đường, treo đèn lồng dọc hành lang, đếm '
         'số trang từ trang 20 đến trang 80 — chỗ nào cũng phải nhớ cộng 1.'],
        ['Đề bài: Dãy 2 ; 4 ; 6 ; ... ; 100 có bao nhiêu số hạng?',
         'Tóm tắt',
         'Dãy cách đều, số đầu 2, số cuối 100, khoảng cách 2.',
         'Kiểm khoảng cách: 4 − 2 = 2 ; 6 − 4 = 2 ✓.',
         'Mô hình (bước nhảy rồi cộng chỗ đầu)',
         'Cả quãng: 100 − 2 = 98.',
         'Số bước nhảy: 98 : 2 = 49.',
         'Cộng thêm chính số hạng đầu: 49 + 1 = 50.',
         'Tính',
         'Số số hạng = (100 − 2) : 2 + 1 = 49 + 1 = 50 số hạng.',
         'Soi lại trên dãy ngắn cùng kiểu: 2 ; 4 ; 6 ; 8 → (8 − 2) : 2 + 1 = 4 ✓ đếm tay cũng 4.',
         'Đáp số: dãy có 50 số hạng.'],
        ['Cô hỏi dãy 2 ; 4 ; 6 ; ... ; 100 có bao nhiêu số hạng, Trí Long đáp: '
         '"Lấy 100 : 2 = 50… à không, lấy (100 − 2) : 2 = 49 số hạng ạ!"',
         'Gợi ý 1: Con thử công thức của Trí Long trên dãy ngắn 2 ; 4 ; 6 ; 8 xem: '
         '(8 − 2) : 2 = 3. Nhưng đếm tay thì rõ ràng có 4 số hạng mà?',
         'Gợi ý 2: Phép chia ấy cho ra số BƯỚC NHẢY. Còn thiếu chính chỗ đứng đầu tiên '
         '— con đã đếm nó chưa?',
         'Chữa: phải cộng thêm 1. Số số hạng = (100 − 2) : 2 + 1 = 50.'],
        ['Cùng con đếm số bậc cầu thang trong nhà rồi đếm số "lần bước" từ dưới lên — '
         'cho con tự thấy hai con số lệch nhau đúng 1.',
         'Bài đố vui: từ trang 20 đến trang 80 của quyển truyện có bao nhiêu trang? '
         '(Đáp: 61 trang, không phải 60 — vì tính cả trang 20.)'],
    ),
    [
        lt(1, 1, 'Một hàng rào có 5 cây cột cắm cách đều. Hỏi giữa các cột có bao nhiêu khoảng?',
           '5 cột thì có 4 khoảng — số khoảng ít hơn số cột đúng 1.'),
        lt(2, 1, 'Dãy 2 ; 4 ; 6 ; ... ; 100 có bao nhiêu số hạng?',
           '(100 − 2) : 2 + 1 = 49 + 1 = 50 số hạng.'),
        lt(3, 1, 'Dãy 5 ; 10 ; 15 ; ... ; 100 có bao nhiêu số hạng?',
           '(100 − 5) : 5 + 1 = 19 + 1 = 20 số hạng.'),
        lt(4, 2, 'Dãy 3 ; 7 ; 11 ; ... ; 79 có bao nhiêu số hạng?',
           '(79 − 3) : 4 + 1 = 19 + 1 = 20 số hạng.'),
        lt(5, 2, 'Hàng rào thẳng dài 40 m, cứ 5 m cắm một cột, cắm cả hai đầu. Cần bao '
                 'nhiêu cây cột?',
           '(40 − 0) : 5 + 1 = 8 + 1 = 9 cây cột.'),
        lt(6, 2, 'Từ trang 20 đến trang 80 của một quyển truyện có bao nhiêu trang?',
           '(80 − 20) : 1 + 1 = 60 + 1 = 61 trang. Nhớ tính cả trang 20.'),
        lt(7, 2, 'Dãy 1 ; 9 ; 17 ; ... ; 113 có bao nhiêu số hạng?',
           '(113 − 1) : 8 + 1 = 14 + 1 = 15 số hạng.'),
        lt(8, 3, 'Dãy 4 ; 9 ; 14 ; ... ; 99 có bao nhiêu số hạng? Hãy soi lại kết quả '
                 'bằng cách đếm tay trên một dãy ngắn cùng kiểu.',
           '(99 − 4) : 5 + 1 = 19 + 1 = 20 số hạng. Soi trên dãy ngắn 4 ; 9 ; 14 : '
           '(14 − 4) : 5 + 1 = 3 ✓ đếm tay cũng 3.'),
        lt(9, 3, 'Một dãy cách đều có 25 số hạng, số đầu là 6, khoảng cách là 4. Hỏi '
                 'số hạng CUỐI của dãy là số nào?',
           '25 số hạng thì có 24 bước nhảy: 6 + 4 × 24 = 6 + 96 = 102.'),
        q_tf(1, 'Số số hạng của dãy cách đều bằng (số cuối − số đầu) : khoảng cách + 1.',
             True, 'Đáp án: ĐÚNG'),
        q_tf(2, 'Một hàng rào có 10 khoảng thì có 10 cây cột.', False,
             'SAI — cắm cả hai đầu thì có 11 cây cột.'),
        q_mcq(3, 'Dãy 5 ; 10 ; 15 ; ... ; 100 có số số hạng là:',
              ['A. 20', 'B. 19', 'C. 21'], 'A. 20', '(100 − 5) : 5 + 1 = 19 + 1 = 20.'),
        q_mcq(4, 'Phép chia (số cuối − số đầu) : khoảng cách cho ra:',
              ['A. số bước nhảy', 'B. số số hạng', 'C. số hạng cuối'], 'A. số bước nhảy',
              'Muốn ra số số hạng thì phải cộng thêm 1.'),
        q_mcq(5, 'Từ trang 20 đến trang 80 có số trang là:',
              ['A. 61', 'B. 60', 'C. 59'], 'A. 61', '(80 − 20) + 1 = 61, vì tính cả trang 20.'),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════
# B16 · TỔNG DÃY CÁCH ĐỀU
# ═══════════════════════════════════════════════════════════════════════════
B16 = bai(
    16, 'TỔNG DÃY CÁCH ĐỀU — CÁCH GHÉP CẶP CỦA GAUSS',
    'Dạng gốc: SỐ 5.1d mức Lớp 4 — Công thức tổng = (số đầu + số cuối) × số số hạng : 2.',
    'Con đã biết tìm số hạng thứ n (Bài 14) và đếm số số hạng (Bài 15). Hôm nay dùng '
    'cả hai để làm một việc trông rất nặng: cộng cả trăm số trong một dòng. Có một '
    'cậu bé 10 tuổi từng làm việc ấy trong vài giây — và cách của cậu ấy chỉ là ghép cặp.',
    LUI_TOA,
    dung_muc(
        'Cậu bé Gauss và bài phạt của thầy giáo',
        ['Chuyện kể hơn hai trăm năm trước: một thầy giáo muốn cả lớp ngồi yên, bèn ra '
         'bài "cộng tất cả các số từ 1 đến 100".',
         'Cả lớp cắm cúi cộng. Riêng cậu bé Gauss đặt bút xuống sau vài giây và nói: '
         '"Thưa thầy, 5 050 ạ."',
         'Cậu không cộng nhanh hơn ai cả. Cậu chỉ nhìn ra một chuyện mà cả lớp không nhìn ra.'],
        ['Hiểu vì sao ghép số đầu với số cuối thì cặp nào cũng có tổng bằng nhau.',
         'Dùng được công thức: tổng = (số đầu + số cuối) × số số hạng : 2.',
         'Giải thích được vì sao công thức phải CHIA 2.'],
        ['CHO GÌ? dãy 1 ; 2 ; 3 ; ... ; 100 — dãy cách đều, khoảng cách 1.',
         'HỎI GÌ? tổng của cả dãy.',
         'ĐẠI LƯỢNG & ĐƠN VỊ: ở đây chỉ có số thuần, không kèm đơn vị nào.',
         'QUAN HỆ GIỮA CHÚNG: dãy cách đều nên đầu với cuối, số thứ hai với số áp '
         'chót… ghép lại đều cho cùng một tổng.',
         'CHỌN CÔNG CỤ: công thức TỔNG DÃY CÁCH ĐỀU. Cần biết SỐ SỐ HẠNG trước, nên '
         'công thức của Bài 15 là bạn đồng hành.',
         'ƯỚC LƯỢNG TRƯỚC: 100 số, số giữa quãng 50, nên tổng chắc quanh 5 000.'],
        ['Bước 1 — GAUSS NHÌN RA GÌ. Cậu viết dãy hai lần, lần sau viết ngược: hàng '
         'trên 1 ; 2 ; 3 ; ... ; 100, hàng dưới 100 ; 99 ; 98 ; ... ; 1. Rồi cộng '
         'theo cột: 1 + 100 = 101 ; 2 + 99 = 101 ; 3 + 98 = 101 … cột nào cũng đúng '
         '101!',
         'Bước 2 — VÌ SAO CỘT NÀO CŨNG BẰNG NHAU. Vì mỗi bước sang phải thì hàng trên '
         'TĂNG một khoảng, còn hàng dưới GIẢM đúng một khoảng ấy. Tăng bao nhiêu thì '
         'giảm bấy nhiêu, nên tổng của cột không đổi. Điều này CHỈ đúng với dãy cách '
         'đều — dãy không cách đều thì mẹo này hỏng.',
         'Bước 3 — VÌ SAO PHẢI CHIA 2. Có 100 cột, mỗi cột 101, nên tất cả bằng 101 × '
         '100 = 10 100. Nhưng con vừa cộng dãy HAI LẦN (một lần xuôi, một lần ngược), '
         'nên phải chia đôi: 10 100 : 2 = 5 050. Đó chính là con số Gauss nói.',
         'Bước 4 — GHÉP THÀNH CÔNG THỨC. Tổng = (số đầu + số cuối) × số số hạng : 2. '
         'Đọc thành lời cho dễ nhớ: "đầu cộng cuối, nhân số số hạng, chia đôi".',
         'Bước 5 — DÙNG VỚI DÃY KHÁC. Tính 5 + 10 + 15 + ... + 100. Trước hết đếm số '
         'số hạng bằng công thức Bài 15: (100 − 5) : 5 + 1 = 20. Rồi tính tổng: '
         '(5 + 100) × 20 : 2 = 105 × 20 : 2 = 2 100 : 2 = 1 050.',
         'MẸO NGƯỜI GIẢI: bao giờ cũng làm hai việc theo thứ tự — (1) ĐẾM số số hạng '
         'trước; (2) mới ghép đầu cộng cuối. Quên bước 1 là không có gì để nhân.'],
        ['LẮP: từ hôm ấy cả lớp học được một mẹo: gặp dãy dài mà cách đều thì đừng '
         'cộng lần lượt, hãy ghép cặp. Việc nửa tiếng rút xuống nửa phút.',
         'SOI: soi trên dãy ngắn đếm tay được — 1 + 2 + 3 + 4 = 10. Công thức: '
         '(1 + 4) × 4 : 2 = 5 × 4 : 2 = 10 ✓.',
         'DÙNG NGOÀI ĐỜI: cộng tiền tiết kiệm tăng đều mỗi tuần, đếm tổng số ghế khi '
         'mỗi hàng thêm đúng một ghế, cộng số bậc thang của nhiều tầng.'],
        ['Đề bài: Tính tổng 5 + 10 + 15 + ... + 100.',
         'Tóm tắt',
         'Dãy cách đều, số đầu 5, số cuối 100, khoảng cách 5.',
         'Gọi tên "dãy cách đều, khoảng cách 5" — nhận diện xong nửa bài.',
         'Bước 1 — đếm số số hạng (dùng công thức Bài 15)',
         '(100 − 5) : 5 + 1 = 19 + 1 = 20 số hạng.',
         'Bước 2 — ghép cặp Gauss',
         '5 + 100 = 105 ; 10 + 95 = 105 ; 15 + 90 = 105 ...',
         'Cặp nào cũng có tổng bằng đầu + cuối.',
         'Tính',
         'Tổng = (5 + 100) × 20 : 2 = 105 × 20 : 2 = 2 100 : 2 = 1 050.',
         'Soi lại trên dãy ngắn cùng kiểu: 5 + 10 + 15 = 30, công thức cho '
         '(5 + 15) × 3 : 2 = 30 ✓.',
         'Đáp số: tổng bằng 1 050.'],
        ['Cô cho tính 1 + 2 + 3 + ... + 10, Trí Long viết: "(1 + 10) × 10 = 110 ạ!"',
         'Gợi ý 1: Con thử cộng tay dãy ngắn 1 + 2 + 3 + 4 xem được bao nhiêu? Rồi '
         'thử công thức của Trí Long: (1 + 4) × 4 = 20. Hai kết quả có khớp không?',
         'Gợi ý 2: Khi ghép cặp, con đã viết dãy MẤY LẦN? Cộng hai lần thì phải làm '
         'gì với kết quả?',
         'Chữa: còn thiếu phép chia 2. Tổng = (1 + 10) × 10 : 2 = 55.'],
        ['Kể con nghe chuyện Gauss 10 tuổi — trẻ con rất thích chuyện một bạn nhỏ '
         'thắng cả lớp bằng cách NGHĨ chứ không phải bằng cách làm nhanh.',
         'Bài đố vui: cộng tất cả các số lẻ từ 1 đến 19, rồi so với 10 × 10. Trùng '
         'nhau — vì sao lại thế? (Gợi ý: 10 số lẻ đầu tiên.)'],
    ),
    [
        lt(1, 1, 'Tính tổng: 1 + 2 + 3 + 4 + 5 + 6. Hãy làm hai cách: cộng lần lượt, và '
                 'ghép cặp đầu với cuối.',
           'Cộng lần lượt: 21. Ghép cặp: (1 + 6) × 6 : 2 = 7 × 3 = 21 ✓ hai cách cùng '
           'một kết quả.'),
        lt(2, 1, 'Tính tổng: 1 + 2 + 3 + ... + 10.',
           '(1 + 10) × 10 : 2 = 110 : 2 = 55.'),
        lt(3, 1, 'Dãy 2 ; 4 ; 6 ; 8 ; 10 có 5 số hạng. Tính tổng của dãy.',
           '(2 + 10) × 5 : 2 = 60 : 2 = 30.'),
        lt(4, 2, 'Tính tổng: 1 + 2 + 3 + ... + 50.',
           '(1 + 50) × 50 : 2 = 51 × 25 = 1 275.'),
        lt(5, 2, 'Tính tổng: 5 + 10 + 15 + ... + 100.',
           'Số số hạng: (100 − 5) : 5 + 1 = 20. Tổng = (5 + 100) × 20 : 2 = 1 050.'),
        lt(6, 2, 'Tính tổng: 3 + 6 + 9 + ... + 30.',
           'Số số hạng: (30 − 3) : 3 + 1 = 10. Tổng = (3 + 30) × 10 : 2 = 165.'),
        lt(7, 2, 'Tính tổng các số chẵn từ 2 đến 100.',
           'Số số hạng: (100 − 2) : 2 + 1 = 50. Tổng = (2 + 100) × 50 : 2 = 2 550.'),
        lt(8, 3, 'Tính tổng 15 số lẻ đầu tiên: 1 + 3 + 5 + ... + 29. Rồi so kết quả với '
                 '15 × 15 và cho biết con thấy điều gì.',
           'Tổng = (1 + 29) × 15 : 2 = 225. Mà 15 × 15 = 225 — trùng nhau! Tổng n số '
           'lẻ đầu tiên luôn bằng n × n.'),
        lt(9, 3, 'Một dãy cách đều có số đầu 4, khoảng cách 6, gồm 12 số hạng. Tính '
                 'tổng của dãy.',
           'Số hạng cuối = 4 + 6 × 11 = 70. Tổng = (4 + 70) × 12 : 2 = 74 × 6 = 444.'),
        q_tf(1, 'Tổng dãy cách đều bằng (số đầu + số cuối) × số số hạng.', False,
             'SAI — còn phải chia 2, vì khi ghép cặp ta đã cộng dãy hai lần.'),
        q_tf(2, 'Mẹo ghép cặp của Gauss chỉ dùng được cho dãy CÁCH ĐỀU.', True,
             'ĐÚNG — dãy không cách đều thì các cặp không còn bằng nhau.'),
        q_mcq(3, 'Tổng 1 + 2 + ... + 10 bằng:', ['A. 55', 'B. 50', 'C. 45'], 'A. 55',
              '(1 + 10) × 10 : 2 = 55.'),
        q_mcq(4, 'Muốn tính tổng một dãy cách đều, việc phải làm TRƯỚC TIÊN là:',
              ['A. đếm số số hạng', 'B. cộng đầu với cuối', 'C. chia 2'],
              'A. đếm số số hạng', 'Không biết số số hạng thì không có gì để nhân.'),
        q_mcq(5, 'Tổng 2 + 4 + 6 + ... + 20 bằng:', ['A. 110', 'B. 100', 'C. 120'],
              'A. 110', 'Có 10 số hạng; (2 + 20) × 10 : 2 = 110.'),
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
    dung_muc(
        'Tấm vé số 113',
        ['Rạp phim mini của cô Hạnh mỗi hàng đúng 8 ghế, đánh số liền từ 1. Vậy ghế '
         'ĐẦU của các hàng lần lượt là 1 ; 9 ; 17 ; 25 ; ...',
         'Một khách cầm vé số 113 hỏi: "Ghế của tôi có phải ghế đầu hàng không cô? '
         'Tôi muốn ngồi sát lối đi."',
         'Cô Hạnh không thể viết cả dãy ra để dò. Cô cần một cách soi nhanh.'],
        ['Kiểm tra được một số có thuộc dãy cách đều hay không, bằng phép chia hết.',
         'Nếu số ấy thuộc dãy thì tìm được nó đứng ở vị trí thứ mấy.',
         'Biết rằng còn phải xét số ấy có nằm trong khoảng từ số đầu đến số cuối không.'],
        ['CHO GÌ? dãy ghế đầu hàng: 1 ; 9 ; 17 ; 25 ; ... — cách đều, số đầu 1, khoảng cách 8.',
         'HỎI GÌ? số 113 có thuộc dãy không; nếu thuộc thì đứng thứ mấy.',
         'ĐẠI LƯỢNG & ĐƠN VỊ: số ghế (chiếc) và số thứ tự hàng — hai loại số khác '
         'nhau, đúng như con đã phân biệt ở Bài 13.',
         'QUAN HỆ GIỮA CHÚNG: mọi số hạng của dãy đều bằng số đầu cộng một số nguyên '
         'lần khoảng cách.',
         'CHỌN CÔNG CỤ: phép CHIA HẾT — dấu hiệu chia hết của Chương 3 quay lại gác '
         'cổng cho bài này.',
         'ƯỚC LƯỢNG TRƯỚC: 113 gần 112 = 8 × 14, nên khả năng cao là thuộc dãy.'],
        ['Bước 1 — MỌI SỐ HẠNG ĐỀU CÁCH SỐ ĐẦU MỘT SỐ NGUYÊN LẦN KHOẢNG CÁCH. Nhìn '
         'dãy 1 ; 9 ; 17 ; 25: lấy từng số trừ số đầu được 0 ; 8 ; 16 ; 24 — toàn bộ '
         'đều chia hết cho 8. Mọi số hạng của dãy đều có tính chất này, còn số không '
         'thuộc dãy thì không.',
         'Bước 2 — CÁCH SOI. Muốn biết số x có thuộc dãy không, lấy (x − số đầu) rồi '
         'chia cho khoảng cách. CHIA HẾT thì x thuộc dãy; CÒN DƯ thì không.',
         'Bước 3 — SOI VÉ 113. (113 − 1) : 8 = 112 : 8 = 14, chia hết → số 113 THUỘC '
         'dãy. Vậy đúng là một ghế đầu hàng.',
         'Bước 4 — NÓ ĐỨNG THỨ MẤY. Phép chia vừa rồi cho ra 14 — đó là SỐ BƯỚC NHẢY '
         'từ số đầu tới nó. Mà chỗ thì nhiều hơn bước đúng 1 (Bài 15 đã nói), nên vị '
         'trí = 14 + 1 = 15. Vé 113 là ghế đầu của hàng 15!',
         'Bước 5 — KHI CÒN DƯ THÌ SAO. Vé 100: (100 − 1) : 8 = 99 : 8 = 12 dư 3 → '
         'KHÔNG thuộc dãy ghế-đầu-hàng. Khách này không được ngồi sát lối đi.',
         'Bước 6 — MỘT CHỐT NỮA DỄ QUÊN. Chia hết CHƯA ĐỦ. Số ấy còn phải nằm TRONG '
         'khoảng từ số đầu đến số cuối. Dãy 1 ; 9 ; 17 ; ... ; 57 (rạp chỉ có 8 hàng) '
         'thì số 113 tuy chia hết nhưng đã vượt quá số cuối — nó KHÔNG thuộc dãy ấy.',
         'MẸO NGƯỜI GIẢI: soi ba việc theo thứ tự — (1) trừ số đầu; (2) chia cho '
         'khoảng cách, xem hết hay dư; (3) nếu hết thì cộng 1 ra vị trí, rồi kiểm xem '
         'có vượt quá số cuối không.'],
        ['LẮP: cô Hạnh dán ở quầy vé một dòng: "Ghế đầu hàng là các số chia 8 dư 1. '
         'Muốn biết hàng mấy: lấy (số ghế − 1) : 8 rồi cộng 1."',
         'SOI: soi chéo bằng công thức Bài 14 — số hạng thứ 15 = 1 + 8 × (15 − 1) = '
         '1 + 112 = 113 ✓. Hai con đường một đáp số.',
         'DÙNG NGOÀI ĐỜI: xem ngày 25 có phải Chủ nhật không khi biết Chủ nhật đầu '
         'tháng là ngày 4; xem số nhà 87 có nằm bên dãy lẻ không; xem chuyến xe buýt '
         'chạy cách nhau 15 phút có chuyến nào đúng 8 giờ 45 không.'],
        ['Đề bài: Số 79 có thuộc dãy 3 ; 7 ; 11 ; ... không? Nếu thuộc thì đứng thứ '
         'mấy? Còn số 100 thì sao?',
         'Tóm tắt',
         'Dãy cách đều, số đầu 3, khoảng cách 4.',
         'Kiểm khoảng cách: 7 − 3 = 4 ; 11 − 7 = 4 ✓.',
         'Soi số 79',
         '79 − 3 = 76 ; 76 : 4 = 19, chia hết → số 79 THUỘC dãy.',
         'Vị trí = 19 + 1 = 20.',
         'Soi lại bằng công thức Bài 14: 3 + 4 × (20 − 1) = 3 + 76 = 79 ✓.',
         'Soi số 100',
         '100 − 3 = 97 ; 97 : 4 = 24 dư 1 → còn dư, nên số 100 KHÔNG thuộc dãy.',
         'Đáp số: 79 thuộc dãy và đứng thứ 20; 100 không thuộc dãy.'],
        ['Cô hỏi số 79 có thuộc dãy 3 ; 7 ; 11 ; ... không, Trí Long soi: '
         '"79 chia 4 được 19 dư 3, còn dư nên không thuộc dãy ạ!"',
         'Gợi ý 1: Con thử cách của Trí Long với chính số 3 — số hạng ĐẦU của dãy: '
         '3 chia 4 dư 3. Vậy theo cách ấy thì số 3 cũng không thuộc dãy à?',
         'Gợi ý 2: Trước khi chia, con phải TRỪ số đầu đi đã. Dãy này bắt đầu từ 3 '
         'chứ không phải từ 0.',
         'Chữa: lấy (79 − 3) : 4 = 19, chia hết → số 79 THUỘC dãy, đứng thứ 20.'],
        ['Mở tờ lịch, chỉ vào một Chủ nhật rồi hỏi con: "Ngày 25 có phải Chủ nhật '
         'không?" — cho con soi bằng phép trừ rồi chia 7.',
         'Nhắc con một câu duy nhất khi làm dạng này: TRỪ SỐ ĐẦU TRƯỚC ĐÃ. Quên bước '
         'ấy là sai cả bài, và đó đúng là lỗi Trí Long mắc.'],
    ),
    [
        lt(1, 1, 'Dãy 3 ; 7 ; 11 ; ... có số đầu và khoảng cách bằng mấy? Muốn soi một '
                 'số có thuộc dãy không, việc đầu tiên phải làm là gì?',
           'Số đầu 3, khoảng cách 4. Việc đầu tiên: lấy số cần soi TRỪ số đầu.'),
        lt(2, 1, 'Số 23 có thuộc dãy 3 ; 7 ; 11 ; ... không?',
           '(23 − 3) : 4 = 5, chia hết → số 23 THUỘC dãy.'),
        lt(3, 1, 'Số 30 có thuộc dãy 2 ; 6 ; 10 ; ... không?',
           '(30 − 2) : 4 = 7, chia hết → số 30 THUỘC dãy.'),
        lt(4, 2, 'Số 79 có thuộc dãy 3 ; 7 ; 11 ; ... không? Nếu thuộc thì đứng thứ mấy?',
           '(79 − 3) : 4 = 19 chia hết → thuộc dãy, đứng thứ 19 + 1 = 20.'),
        lt(5, 2, 'Số 100 có thuộc dãy 3 ; 7 ; 11 ; ... không?',
           '(100 − 3) : 4 = 97 : 4 = 24 dư 1 → còn dư, nên KHÔNG thuộc dãy.'),
        lt(6, 2, 'Số 113 có thuộc dãy 1 ; 9 ; 17 ; ... không? Nếu thuộc thì đứng thứ mấy?',
           '(113 − 1) : 8 = 14 chia hết → thuộc dãy, đứng thứ 15.'),
        lt(7, 2, 'Số 52 có thuộc dãy 7 ; 12 ; 17 ; ... không? Nếu thuộc thì đứng thứ mấy?',
           '(52 − 7) : 5 = 9 chia hết → thuộc dãy, đứng thứ 10.'),
        lt(8, 3, 'Dãy 1 ; 9 ; 17 ; ... ; 57. Hỏi số 113 có thuộc dãy này không? Chú ý '
                 'đọc kỹ số CUỐI của dãy.',
           '(113 − 1) : 8 = 14 chia hết, nhưng 113 đã VƯỢT QUÁ số cuối 57, nên số 113 '
           'KHÔNG thuộc dãy này. Chia hết thôi chưa đủ.'),
        lt(9, 3, 'Cho dãy 4 ; 9 ; 14 ; ... ; 99. Số 64 có thuộc dãy không, đứng thứ '
                 'mấy? Hãy soi lại kết quả bằng công thức số hạng thứ n.',
           '(64 − 4) : 5 = 12 chia hết, và 64 nằm giữa 4 và 99 → thuộc dãy, đứng thứ '
           '13. Soi lại: 4 + 5 × (13 − 1) = 4 + 60 = 64 ✓.'),
        q_tf(1, 'Muốn soi một số có thuộc dãy không, phải lấy số ấy TRỪ số đầu rồi mới '
                'chia cho khoảng cách.', True, 'Đáp án: ĐÚNG'),
        q_tf(2, 'Cứ chia hết cho khoảng cách là số ấy chắc chắn thuộc dãy.', False,
             'SAI — còn phải kiểm số ấy có nằm trong khoảng từ số đầu đến số cuối không.'),
        q_mcq(3, 'Số 52 với dãy 7 ; 12 ; 17 ; ...:',
              ['A. thuộc dãy, đứng thứ 10', 'B. không thuộc dãy', 'C. thuộc dãy, đứng thứ 9'],
              'A. thuộc dãy, đứng thứ 10', '(52 − 7) : 5 = 9 chia hết → vị trí 9 + 1 = 10.'),
        q_mcq(4, 'Phép chia (x − số đầu) : khoảng cách nếu CÒN DƯ thì nghĩa là:',
              ['A. x không thuộc dãy', 'B. x thuộc dãy', 'C. x là số hạng cuối'],
              'A. x không thuộc dãy', 'Còn dư nghĩa là x rơi vào giữa hai số hạng.'),
        q_mcq(5, 'Số 113 với dãy 1 ; 9 ; 17 ; ... đứng ở vị trí thứ:',
              ['A. 15', 'B. 14', 'C. 16'], 'A. 15',
              '(113 − 1) : 8 = 14 bước nhảy, nên vị trí là 14 + 1 = 15.'),
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
    {'id': 'L4H_B13_MO', 'arch': 'day_o',
     'params': {'title': 'NHÀ THỨ TƯ MANG SỐ MẤY? NHÀ SỐ 26 ĐỨNG THỨ MẤY?',
                'hang': [{'nhan': 'đứng thứ', 'o': [_o(i, 'gold') for i in range(1, 7)]},
                         {'nhan': 'số nhà',
                          'o': [_o(n, 'teal') for n in (6, 11, 16, 21, 26, 31)]}]},
     'caption': 'Hai hàng, một ngôi nhà: hàng trên là VỊ TRÍ, hàng dưới là GIÁ TRỊ.',
     'bai': 'DL:KSN4.B13', 'muc': 'chuyenMoBai', 'goc': 'B13 ②'},
    {'id': 'L4H_B13_G1', 'arch': 'tia_so',
     'params': {'title': 'CÁCH ĐỀU LÀ GÌ — TRỪ LIÊN TIẾP XEM CÁC HIỆU CÓ BẰNG NHAU',
                'moc': [{'so': 7, 'danh': True}, {'so': 12}, {'so': 17}, {'so': 22},
                        {'so': 27}],
                'nhan': '+5',
                'note': 'Các hiệu đều bằng 5 → dãy cách đều, khoảng cách 5.'},
     'caption': 'Bước chân từ số hạng này sang số hạng kế luôn dài bằng nhau.',
     'bai': 'DL:KSN4.B13', 'muc': 'khamPha', 'neoBuoc': 2, 'goc': 'B13 ④ bước 3'},

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
    # ── B13 · khái niệm ──
    'DL:KSN4.B13#C1': {'parts': [{'label': 'dãy có mấy số hạng', 'value': 5},
                                 {'label': 'số hạng thứ 3', 'value': 12}]},
    'DL:KSN4.B13#C2': {'value': 5},
    'DL:KSN4.B13#C3': {'parts': [{'label': 'dãy có cách đều không', 'options': CO_KHONG, 'value': 'có'},
                                 {'label': 'khoảng cách', 'value': 3}]},
    'DL:KSN4.B13#C4': {'parts': [{'label': 'dãy cách đều là dãy', 'options': ['dãy A', 'dãy B'],
                                  'value': 'dãy A'}]},
    'DL:KSN4.B13#C5': {'parts': [{'label': 'dãy có cách đều không', 'options': CO_KHONG, 'value': 'có'},
                                 {'label': 'khoảng cách', 'value': 5}]},
    'DL:KSN4.B13#C6': {'value': 30},
    'DL:KSN4.B13#C7': {'parts': [{'label': 'bạn Mai nói', 'options': ['đúng', 'sai'], 'value': 'sai'},
                                 {'label': 'số 16 thật ra đứng thứ', 'value': 3}]},
    'DL:KSN4.B13#C8': {'parts': [{'label': 'khoảng cách', 'value': 4},
                                 {'label': 'số hạng thứ 5', 'value': 19},
                                 {'label': 'số 11 đứng thứ', 'value': 3}]},
    'DL:KSN4.B13#C9': {'value': 18},

    # ── B14 · số hạng thứ n ──
    'DL:KSN4.B14#C1': {'parts': [{'label': 'khoảng cách', 'value': 5},
                                 {'label': 'số bước nhảy', 'value': 9}]},
    'DL:KSN4.B14#C2': {'value': 50},
    'DL:KSN4.B14#C3': {'value': 30},
    'DL:KSN4.B14#C4': {'value': 79},
    'DL:KSN4.B14#C5': {'value': 113},
    'DL:KSN4.B14#C6': {'value': 83},
    'DL:KSN4.B14#C7': {'value': 300},
    'DL:KSN4.B14#C8': {'parts': [{'label': 'số hạng thứ 30', 'value': 207},
                                 {'label': 'thử n = 1 ra', 'value': 4}]},
    'DL:KSN4.B14#C9': {'value': 7},

    # ── B15 · đếm số số hạng ──
    'DL:KSN4.B15#C1': {'value': 4},
    'DL:KSN4.B15#C2': {'value': 50},
    'DL:KSN4.B15#C3': {'value': 20},
    'DL:KSN4.B15#C4': {'value': 20},
    'DL:KSN4.B15#C5': {'value': 9},
    'DL:KSN4.B15#C6': {'value': 61},
    'DL:KSN4.B15#C7': {'value': 15},
    'DL:KSN4.B15#C8': {'value': 20},
    'DL:KSN4.B15#C9': {'value': 102},

    # ── B16 · tổng dãy ──
    'DL:KSN4.B16#C1': {'value': 21},
    'DL:KSN4.B16#C2': {'value': 55},
    'DL:KSN4.B16#C3': {'value': 30},
    'DL:KSN4.B16#C4': {'value': 1275},
    'DL:KSN4.B16#C5': {'value': 1050},
    'DL:KSN4.B16#C6': {'value': 165},
    'DL:KSN4.B16#C7': {'value': 2550},
    'DL:KSN4.B16#C8': {'parts': [{'label': 'tổng', 'value': 225},
                                 {'label': '15 × 15', 'value': 225}]},
    'DL:KSN4.B16#C9': {'value': 444},

    # ── B17 · thuộc dãy không ──
    'DL:KSN4.B17#C1': {'parts': [{'label': 'số đầu', 'value': 3},
                                 {'label': 'khoảng cách', 'value': 4}]},
    'DL:KSN4.B17#C2': {'parts': [{'label': 'số 23 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B17#C3': {'parts': [{'label': 'số 30 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'}]},
    'DL:KSN4.B17#C4': {'parts': [{'label': 'số 79 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 20}]},
    'DL:KSN4.B17#C5': {'parts': [{'label': 'số 100 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'không'}]},
    'DL:KSN4.B17#C6': {'parts': [{'label': 'số 113 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 15}]},
    'DL:KSN4.B17#C7': {'parts': [{'label': 'số 52 có thuộc dãy không', 'options': CO_KHONG,
                                  'value': 'có'},
                                 {'label': 'đứng thứ', 'value': 10}]},
    'DL:KSN4.B17#C8': {'parts': [{'label': 'số 113 có thuộc dãy này không', 'options': CO_KHONG,
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
