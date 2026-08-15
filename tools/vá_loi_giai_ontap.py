# -*- coding: utf-8 -*-
"""VÁ LỜI GIẢI KỲ SÁT HẠCH — chương 3, 5, 6, 7 (và hai câu lẻ ở 8, 9).

── LỖI ĐANG CHẠY THẬT ──
Bé làm xong một câu ôn tập thì màn hình chìa ra lời giải để bé tự soi. Ở bốn
chương này, lời giải hiện ra là của MỘT CÂU KHÁC:

    ôn tập 7 · C1 hỏi "Tỉ số hai số là 2 : 5, cả hai gộp lại gồm mấy phần?"
              lời giải hiện ra "một phần 20 : 4 = 5 → 5 viên và 15 viên"

── VÌ SAO ──
Mấy đợt làm video trước có VIẾT LẠI đề của mấy kỳ ôn tập cho khớp bài mới tách.
Đề đổi, ô nhập đổi theo, nhưng `lop4_dapan.json` thì không — mà nó đánh khoá theo
SỐ THỨ TỰ CÂU (`OT7#C1`), nên khoá vẫn khớp còn nội dung thì đã là của câu cũ.
Cùng dòng họ với lỗi mối nối ở `ontap_lop4.py`: hai đầu đều hợp lệ, chỉ chỗ nối sai.

── VÌ SAO TIN ĐƯỢC Ô NHẬP ──
Đã đối chiếu bằng mắt từng câu của bốn chương: ô nhập khớp đề, chỉ lời giải lệch.
Nên lời giải dưới đây viết BÁM VÀO Ô NHẬP đã xác minh, và tệp này soi lại: mọi giá
trị số của ô nhập phải xuất hiện nguyên văn trong lời giải mới.

    python3 tools/vá_loi_giai_ontap.py --soat
    python3 tools/vá_loi_giai_ontap.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
DAP = GOC / 'data' / 'lop4_dapan.json'
ONTAP = GOC / 'data' / 'lop4_ontap.json'
O_NHAP = GOC / 'data' / 'lop4_ontap_o.json'

MOI = {
 # ═══ ÔN TẬP 3 · dấu hiệu chia hết và chia có dư ═══
 'OT3#C1': 'Mỗi đĩa 6 quả thì 18 : 6 = 3 (đĩa), không thừa quả nào. '
           'Mỗi đĩa 4 quả thì 18 : 4 = 4 (dư 2) — thừa 2 quả.',
 'OT3#C2': 'Số 132 và số 208 chia hết cho 2, vì hai số ấy tận cùng bằng chữ số chẵn. '
           'Còn 145 tận cùng bằng 5 nên không chia hết cho 2.',
 'OT3#C3': 'Chia hết cho 5 thì chữ số tận cùng phải là 0 hoặc 5. '
           'Vậy điền được 0 hoặc 5, được hai số 470 và 475.',
 'OT3#C4': 'Số 130. Muốn chia hết cho cả 2 và 5 thì tận cùng phải bằng 0. '
           'Số 135 tận cùng bằng 5 nên chỉ chia hết cho 5; số 142 tận cùng bằng 2 '
           'nên chỉ chia hết cho 2.',
 'OT3#C5': 'Có. Cộng các chữ số lại: 2 + 7 + 0 = 9. Số 9 chia hết cho 9 nên 270 '
           'cũng chia hết cho 9.',
 'OT3#C6': 'Cộng các chữ số: 3 + 4 + 8 = 15. Số 15 chia hết cho 3 nhưng không chia '
           'hết cho 9, nên 348 chỉ chia hết cho 3 thôi.',
 'OT3#C7': 'Bạn sai ở số dư: bạn ghi dư 8 mà 8 lại lớn hơn số chia 5. Số dư bao giờ '
           'cũng phải bé hơn số chia. Kết quả đúng là 23 : 5 = 4 (dư 3).',
 'OT3#C8': 'Số bị chia bằng thương nhân số chia rồi cộng số dư: 7 × 5 = 35, '
           'rồi 35 + 3 = 38.',
 'OT3#C9': 'Chia thử: 25 : 6 = 4 (dư 1). Có 4 xe chở đầy 6 bạn, còn 1 bạn lẻ. '
           'Bạn ấy vẫn cần một xe nữa, nên cần ít nhất 5 xe.',
 'OT3#C10': 'Chữ số tận cùng là 0. Trong tích có 12 là số chẵn và 15 tận cùng bằng 5, '
            'ghép được một cặp 2 nhân 5 nên cả tích chia hết cho 10.',

 # ═══ ÔN TẬP 5 · trung bình cộng ═══
 'OT5#C1': 'Gộp lại rồi chia đều: 4 + 6 + 8 = 18 (cái). '
           'Mỗi bạn được 18 : 3 = 6 (cái).',
 'OT5#C2': 'Tổng số bàn bốn trận: 2 + 5 + 2 + 3 = 12 (bàn). '
           'Có 4 trận nên trung bình mỗi trận 12 : 4 = 3 (bàn).',
 'OT5#C3': 'Tổng bằng trung bình cộng nhân số các số: 25 × 4 = 100.',
 'OT5#C4': 'Tổng hai số: 36 × 2 = 72. Số còn lại: 72 − 40 = 32.',
 'OT5#C5': 'Mức trung bình là 3 bàn, trận một ghi hơn mức ấy 2 bàn, '
           'nên trận một ghi 3 + 2 = 5 (bàn).',
 'OT5#C6': 'Bạn ấy cao hơn mức trung bình: 134 − 130 = 4 (cm).',
 'OT5#C7': 'Bốn bạn góp: 10 × 4 = 40 (nghìn đồng). Thêm bạn thứ năm: 40 + 15 = 55. '
           'Trung bình của năm bạn: 55 : 5 = 11 (nghìn đồng).',
 'OT5#C8': 'Muốn trung bình năm bạn là 11 thì tổng phải có 11 × 5 = 55 (nghìn đồng). '
           'Bốn bạn đã góp 40, nên bạn thứ năm góp 55 − 40 = 15 (nghìn đồng).',
 'OT5#C9': 'Tổng ba số: 6 × 3 = 18. Số thứ ba: 18 − 4 − 6 = 8. '
           'Thử lại: 4 + 6 + 8 = 18, rồi 18 : 3 = 6 — đúng bằng mức đã cho.',
 'OT5#C10': 'Đừng lấy trung bình của hai mức. Phải đi qua tổng: ba trận đầu ghi '
            '3 × 3 = 9 (bàn), thêm trận bán kết là 9 + 7 = 16 (bàn). Trung bình bốn '
            'trận: 16 : 4 = 4 (bàn). Bán kết hơn mức mới: 7 − 4 = 3 (bàn).',

 # ═══ ÔN TẬP 6 · tổng và hiệu ═══
 'OT6#C1': 'Khúc dôi ra của đoạn dài so với đoạn ngắn chính là hiệu của hai số. '
           'Còn tổng thì ghi ở ngoặc ôm cả hai đoạn.',
 'OT6#C2': 'Số lớn bằng tổng cộng hiệu rồi chia đôi: 70 + 10 = 80, rồi 80 : 2 = 40.',
 'OT6#C3': 'Số bé bằng tổng trừ hiệu rồi chia đôi: 70 − 10 = 60, rồi 60 : 2 = 30. '
           'Kiểm chéo với số lớn 40: 30 + 40 = 70 và 40 − 30 = 10 — khớp cả hai.',
 'OT6#C4': 'Số lớn: 145 + 27 = 172, rồi 172 : 2 = 86. '
           'Số bé: 145 − 27 = 118, rồi 118 : 2 = 59.',
 'OT6#C5': 'Trung bình cộng là 25 nên tổng hai số là 25 × 2 = 50. '
           'Số lớn: 50 + 6 = 56, rồi 56 : 2 = 28. Số bé: 28 − 6 = 22.',
 'OT6#C6': 'Nửa chu vi: 18 : 2 = 9 (m) — đó chính là tổng của chiều dài và chiều rộng. '
           'Chiều dài: 9 + 1 = 10, rồi 10 : 2 = 5 (m). Chiều rộng: 5 − 1 = 4 (m).',
 'OT6#C7': 'Hai số chẵn liên tiếp cách nhau 2, nên hiệu bằng 2. '
           'Số lớn: 42 + 2 = 44, rồi 44 : 2 = 22. Số bé: 22 − 2 = 20.',
 'OT6#C8': 'Chuyển 15 tấn mà hai kho bằng nhau, nghĩa là kho lớn hơn kho bé '
           '15 × 2 = 30 (tấn). Kho lớn: 180 + 30 = 210, rồi 210 : 2 = 105 (tấn). '
           'Kho bé: 105 − 30 = 75 (tấn).',
 'OT6#C9': 'Hiện nay anh: 20 + 4 = 24, rồi 24 : 2 = 12 (tuổi); em 12 − 4 = 8 (tuổi). '
           'Sau 3 năm mỗi người thêm 3 tuổi nên anh 15 tuổi, em 11 tuổi, '
           'tổng tuổi hai anh em là 26 tuổi.',
 'OT6#C10': 'Bớt phần hơn của lớp B và lớp C đi: 120 − 8 − 16 = 96 (cây) — đó là ba '
            'lần số cây lớp A. Lớp A: 96 : 3 = 32 (cây). Lớp B: 32 + 8 = 40 (cây). '
            'Lớp C: 32 + 16 = 48 (cây).',
 'OT6#C11': 'Đoạn dài bằng đoạn ngắn cộng khúc dôi ra: 30 + 10 = 40. '
            'Tổng hai đoạn: 30 + 40 = 70.',
 'OT6#C12': 'Số bé: 96 − 14 = 82, rồi 82 : 2 = 41. Số lớn: 41 + 14 = 55. '
            'Thử lại: 41 + 55 = 96 và 55 − 41 = 14 — khớp cả tổng lẫn hiệu.',

 # ═══ ÔN TẬP 7 · tỉ số ═══
 'OT7#C1': 'Cả hai gộp lại gồm 2 + 5 = 7 (phần). Chênh nhau: 5 − 2 = 3 (phần).',
 'OT7#C2': 'Cả thảy 1 + 3 = 4 (phần). Một phần: 20 : 4 = 5 (viên). '
           'Bạn được ít 5 viên, bạn được nhiều 5 × 3 = 15 (viên).',
 'OT7#C3': 'Cả thảy 2 + 5 = 7 (phần). Một phần: 70 : 7 = 10. '
           'Số bé: 10 × 2 = 20. Số lớn: 10 × 5 = 50.',
 'OT7#C4': 'Cả thảy 3 + 5 = 8 (phần). Một phần: 56 : 8 = 7. '
           'Số bé: 7 × 3 = 21. Số lớn: 7 × 5 = 35.',
 'OT7#C5': 'Hiệu không phải là tổng số phần: hiệu gồm 5 − 2 = 3 (phần). '
           'Một phần: 30 : 3 = 10. Số bé: 10 × 2 = 20. Số lớn: 10 × 5 = 50.',
 'OT7#C6': 'Tuổi con bằng một phần tư tuổi mẹ nên tỉ số là 1 : 4, và hiệu gồm '
           '4 − 1 = 3 (phần). Một phần: 30 : 3 = 10. '
           'Con 10 tuổi, mẹ 10 × 4 = 40 (tuổi).',
 'OT7#C7': 'Gấp rưỡi nghĩa là tỉ số 3 : 2, cả thảy 3 + 2 = 5 (phần). '
           'Một phần: 40 : 5 = 8 (chiếc). Bánh dẻo: 8 × 2 = 16 (chiếc). '
           'Bánh nướng: 8 × 3 = 24 (chiếc).',
 'OT7#C8': 'Số lớn gấp đôi số bé nên tỉ số là 1 : 2, cả thảy 1 + 2 = 3 (phần). '
           'Một phần: 45 : 3 = 15. Số bé 15, số lớn 15 × 2 = 30.',
 'OT7#C9': 'Trung bình cộng là 35 nên tổng hai số là 35 × 2 = 70. Tỉ số 2 : 5 nên cả '
           'thảy 2 + 5 = 7 (phần). Một phần: 70 : 7 = 10. '
           'Số bé: 10 × 2 = 20. Số lớn: 10 × 5 = 50.',
 'OT7#C10': 'Nửa chu vi: 48 : 2 = 24 (m). Chiều rộng bằng nửa chiều dài nên tỉ số là '
            '1 : 2, cả thảy 3 phần. Một phần: 24 : 3 = 8 (m). '
            'Chiều rộng 8 m, chiều dài 8 × 2 = 16 (m).',
 'OT7#C11': 'Cả thảy 2 + 3 + 4 = 9 (phần). Một phần: 90 : 9 = 10 (quyển). '
            'Ba lớp lần lượt được 10 × 2 = 20, rồi 10 × 3 = 30, '
            'rồi 10 × 4 = 40 (quyển).',
 'OT7#C12': 'Quy số phần của Bình về cùng một con số: An so với Bình là 2 : 3, '
            'tức là 4 : 6. Vậy ba bạn là 4 : 6 : 5, cả thảy 4 + 6 + 5 = 15 (phần). '
            'Một phần: 90 : 15 = 6 (viên). An 6 × 4 = 24, Bình 6 × 6 = 36, '
            'Cường 6 × 5 = 30 (viên).',

 # ═══ hai câu lẻ ═══
 'OT8#C6': 'Một năm có 12 tháng. Nếu mỗi tháng chỉ có nhiều nhất một bạn thì xếp được '
           '12 bạn, mà nhóm có 13 bạn nên còn thừa 1 bạn. Bạn thừa ấy phải rơi vào '
           'một tháng đã có người, nên chắc chắn có ít nhất 2 bạn sinh cùng tháng.',
 'OT9#C5': 'Băng giấy chia làm 4 phần bằng nhau nên mẫu số là 4; tô 3 phần nên tử số '
           'là 3. Phân số chỉ phần đã tô là ba phần tư — tử số 3 viết trên, '
           'mẫu số 4 viết dưới.',
}


def _gt(kh):
    if not kh:
        return []
    if 'parts' in kh:
        return [p.get('value') for p in kh['parts']]
    if 'values' in kh:
        return kh['values']
    return [kh.get('value')]


def soi() -> list[str]:
    """Mọi giá trị SỐ của ô nhập phải nằm nguyên văn trong lời giải mới."""
    o = json.loads(O_NHAP.read_text('utf8'))
    ky = {k['so']: k for k in json.loads(ONTAP.read_text('utf8'))['ky']}
    loi = []
    for ma, van in MOI.items():
        so_ky = int(ma[2:ma.index('#')])
        n = int(ma.split('#C')[1])
        cau = next((q for q in ky[so_ky]['examA'] if q['qno'] == n), None)
        if cau is None:
            loi.append(f'{ma}: kỳ ôn tập không có câu này')
            continue
        phang = van.replace(' ', '')
        for v in _gt(o.get(ma)):
            if isinstance(v, (int, float)) and not re.search(
                    rf'(?<!\d){v}(?!\d)', phang):
                loi.append(f'{ma}: ô nhập có giá trị {v} mà lời giải mới không nhắc tới')
    return loi


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--soat', action='store_true')
    a = p.parse_args()
    loi = soi()
    if loi:
        for x in loi:
            print('  ✗', x)
        print(f'\n{len(loi)} chỗ chưa đạt — CHƯA ghi gì cả')
        return 1
    print(f'  ✓ {len(MOI)} lời giải khớp đủ giá trị của ô nhập')
    if a.soat:
        print('(--soat: chưa ghi)')
        return 0
    d = json.loads(DAP.read_text('utf8'))
    d['dapAn'].update(MOI)
    DAP.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', 'utf8')
    print(f'ghi {len(MOI)} lời giải vào {DAP.relative_to(GOC)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
