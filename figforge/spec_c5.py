# -*- coding: utf-8 -*-
"""Lô A5 · Chương 5 (B17–B20): so sánh phân số · neo hiệu – neo tổng · chiều biến thiên & chặn · tỉ số ẩn."""

SPEC = {
# ── B17 · So sánh phân số ─────────────────────────────────────────
'DL:KSN5Q1.B17.M1': dict(archetype='fraction_split', params=dict(
    title='CÙNG TỬ 2 — MẪU LỚN HƠN THÌ PHÂN SỐ BÉ HƠN',
    shapes=[dict(parts=5, shaded=2, label='2/5 — lát dày', kind='circle'),
            dict(parts=7, shaded=2, label='2/7 — lát mỏng', kind='circle')],
    note='Cùng 2 lát nhưng bánh chia 7 phần thì mỗi lát mỏng hơn → 2/5 > 2/7'),
    caption='Hai luật ngược chiều: cùng mẫu thì tử lớn hơn là lớn · cùng tử thì mẫu lớn hơn lại BÉ'),

'DL:KSN5Q1.B17.M2': dict(archetype='two_way_compare', params=dict(
    title='SO BẰNG PHẦN BÙ: 7/8 VÀ 9/10 (KHÔNG QUY ĐỒNG)', neutral=True,
    wrong=dict(head='PHẦN BÙ CỦA 7/8', steps=['thiếu 1/8 nữa mới đầy'], result='hụt 1/8 (nhiều hơn)'),
    right=dict(head='PHẦN BÙ CỦA 9/10', steps=['thiếu 1/10 nữa mới đầy'], result='hụt 1/10 (ít hơn)'),
    verdict='Hụt NHIỀU hơn thì BÉ hơn → 7/8 < 9/10 (chiều đảo!)'),
    caption='Hai phân số sát nút 1 thì đo phần còn thiếu, đừng quy đồng'),

'DL:KSN5Q1.B17.M3': dict(archetype='fence_posts', params=dict(
    title='XẾP DÃY TRỘN: ĐỔI TẤT CẢ VỀ MỘT ĐỒNG PHỤC',
    first=0, last=0, step=0, show=4, show_step=False,
    labels=['4/5 = 0,8', '0,85', '7/8 = 0,875', '0,9'],
    highlight=[0, 2],
    gap_note='hai kẻ mặc áo phân số phải thay đồng phục thập phân',
    formula='4/5  <  0,85  <  7/8  <  0,9',
    note='So từng hàng sau khi cùng dạng: 0,8 < 0,85 < 0,875 < 0,9'),
    caption='Một đồng phục — rồi mới xếp hàng so sánh'),

# ── B18 · Neo hiệu – neo tổng ─────────────────────────────────────
'DL:KSN5Q1.B18.M1': dict(archetype='two_way_compare', params=dict(
    title='CÙNG MỘT SỐ — NHÂN CHIA KHÁC HẲN CỘNG TRỪ',
    wrong=dict(head='CỘNG cùng 8 vào cả hai', steps=['34/41 → 42/49'], result='GIÁ TRỊ ĐỔI ✗'),
    right=dict(head='CHIA cùng 7 cả hai', steps=['42/49 → 6/7'], result='GIÁ TRỊ GIỮ NGUYÊN ✓'),
    verdict='Cộng trừ làm trôi giá — nhưng để lại NEO: hiệu 41 − 34 = 49 − 42 = 7'),
    caption='Nhân chia giữ giá · cộng trừ trôi giá nhưng vẫn còn neo để bám'),

'DL:KSN5Q1.B18.M2': dict(archetype='bar_diagram', params=dict(
    title='NEO HIỆU: 34/41 CỘNG THÊM BAO NHIÊU ĐỂ THÀNH 6/7?',
    bars=[dict(name='tử mới', units=6, label='6 phần'),
          dict(name='mẫu mới', units=7, label='7 phần')],
    brace=dict(text='hiệu 1 phần = 41 − 34 = 7  →  tử mới = 6 × 7 = 42  →  cộng thêm 8'),
    note='Hiệu KHÔNG ĐỔI khi cộng cùng một số vào cả tử và mẫu — dùng hiệu làm thước đo'),
    caption='Đích 6/7 chênh nhau 1 phần, mà 1 phần đáng đúng 7 đơn vị'),

'DL:KSN5Q1.B18.M3': dict(archetype='bar_diagram', params=dict(
    title='NEO TỔNG: 41/58 CHUYỂN TỪ TỬ XUỐNG MẪU BAO NHIÊU ĐỂ BẰNG 4/7?',
    bars=[dict(name='tử mới', units=4, label='4 phần'),
          dict(name='mẫu mới', units=7, label='7 phần')],
    brace=dict(text='tổng 11 phần = 41 + 58 = 99  →  1 phần = 9  →  tử mới 36 → chuyển 5'),
    note='Chuyển qua lại giữa tử và mẫu thì TỔNG không đổi — gạch chân động từ của đề'),
    caption='"Chuyển xuống" hay "chuyển lên" đều giữ nguyên tổng tử + mẫu'),

# ── B19 · Chiều biến thiên & bài chặn ─────────────────────────────
'DL:KSN5Q1.B19.M1': dict(archetype='fraction_split', params=dict(
    title='THÊM VÀO MẪU THÌ PHÂN SỐ XẸP XUỐNG',
    shapes=[dict(parts=8, shaded=3, label='3/8', kind='bar'),
            dict(parts=10, shaded=3, label='3/10 — bé hơn', kind='bar')],
    note='Thêm nước vào cốc cam: vẫn 3 phần cam nhưng cam nhạt đi → 3/8 > 3/10'),
    caption='Tử tăng thì phân số TĂNG · mẫu tăng thì phân số XẸP'),

'DL:KSN5Q1.B19.M2': dict(archetype='two_way_compare', params=dict(
    title='THÊM MỘT PHÍA — QUY ĐỒNG THEO KẺ ĐỨNG IM', neutral=True,
    wrong=dict(head='THÊM VÀO TỬ', steps=['5/21 → 4/7', 'mẫu 21 đứng im · 4/7 = 12/21'],
               result='5 + n = 12 → n = 7'),
    right=dict(head='THÊM VÀO MẪU', steps=['3/8 → 1/4', 'tử 3 đứng im · 1/4 = 3/12'],
               result='8 + n = 12 → n = 4'),
    verdict='Kẻ nào đứng im thì quy đồng theo kẻ ấy'),
    caption='Thêm vào tử thì đưa về cùng mẫu — thêm vào mẫu thì đưa về cùng tử'),

'DL:KSN5Q1.B19.M3': dict(archetype='fence_posts', params=dict(
    title='CHẶN HAI BỜ: 1/3 < n/12 < 3/4  →  4 < n < 9',
    first=4, last=9, step=1, show=6, labels=['4', '5', '6', '7', '8', '9'],
    highlight=[1, 2, 3, 4], show_step=False,
    gap_note='hai BỜ đứng ngoài — không được nhận',
    formula='n ∈ {5; 6; 7; 8} — bốn số',
    note='Sân cùng tử thì mẫu chạy ngược: 8/16 < 8/n < 8/12 → 12 < n < 16'),
    caption='Kéo cả ba lên chung sân rồi đọc — nhớ hai bờ đứng ngoài'),

# ── B20 · Tỉ số ẩn & chia phần ────────────────────────────────────
'DL:KSN5Q1.B20.M1': dict(archetype='two_way_compare', params=dict(
    title='TỈ SỐ ẨN: 2/3 CỦA A BẰNG 3/4 CỦA B', neutral=True,
    wrong=dict(head='QUY ĐỒNG TỬ — VẾ A', steps=['2/3 = 6/9'], result='A chia 9 phần'),
    right=dict(head='QUY ĐỒNG TỬ — VẾ B', steps=['3/4 = 6/8'], result='B chia 8 phần'),
    verdict='Cùng 6 phần bằng nhau → A : B = 9 : 8 (mẫu của ai, phần của người ấy)'),
    caption='Quy đồng TỬ để lượng chung hiện hình, rồi đọc tỉ số ở mẫu'),

'DL:KSN5Q1.B20.M2': dict(archetype='bar_diagram', params=dict(
    title='TỈ SỐ ẨN GHÉP VỚI TỔNG: HAI KHAY CÓ 34 CHIẾC BÁNH',
    bars=[dict(name='khay A', units=9, label='9 phần → 18 chiếc'),
          dict(name='khay B', units=8, label='8 phần → 16 chiếc')],
    brace=dict(text='tổng 17 phần = 34  →  1 phần = 2 chiếc'),
    note='Thử lại: 2/3 × 18 = 12 và 3/4 × 16 = 12 — bằng nhau ✓'),
    caption='Tổng thì chia TỔNG số phần · hiệu thì chia HIỆU số phần'),

'DL:KSN5Q1.B20.M3': dict(archetype='bar_diagram', params=dict(
    title='THÊM CHỮ SỐ 0 = GẤP 10 LẦN (KHÔNG PHẢI CỘNG 10)',
    bars=[dict(name='số bé', units=1, label='1 phần = 12'),
          dict(name='số lớn', units=10, label='10 phần = 120')],
    brace=dict(text='tổng 11 phần = 132  →  1 phần = 12  →  hai số 12 và 120'),
    note='Cho TỔNG thì chia 11 · cho HIỆU thì chia 9 — thử lại: 12 thêm 0 thành 120 ✓'),
    caption='Thêm 0 vào bên phải là mỗi chữ số dọn sang trái một hàng'),
}
