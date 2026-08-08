# -*- coding: utf-8 -*-
"""Lô A7 · Chương 7 (B25–B28): tổng – hiệu · ba số biết tổng đôi · cú chuyển · toán tuổi."""

SPEC = {
# ── B25 · Tổng – hiệu ─────────────────────────────────────────────
'DL:KSN5Q1.B25.M1': dict(archetype='sum_diff_bars', params=dict(
    title='TỔNG 50 · HIỆU 8 — SƠ ĐỒ HAI ĐOẠN THẲNG',
    small=dict(label='số bé 21', val=21), big=dict(label='số lớn 29', val=29),
    diff_label='hiệu 8', total_label='tổng 50',
    formula='bé = (50 − 8) : 2 = 21    ·    lớn = (50 + 8) : 2 = 29',
    note='Thử hai trạm: 29 + 21 = 50 ✓  và  29 − 21 = 8 ✓'),
    caption='Bớt phần dôi ra rồi chia đôi — hoặc thêm vào rồi chia đôi'),

'DL:KSN5Q1.B25.M2': dict(archetype='sum_diff_bars', params=dict(
    title='DẤU PHẨY KHÔNG ĐỔI LUẬT: TỔNG 9,5 · HIỆU 1,3',
    small=dict(label='số bé 4,1', val=4.1), big=dict(label='số lớn 5,4', val=5.4),
    diff_label='hiệu 1,3', total_label='tổng 9,5',
    formula='lớn = (9,5 + 1,3) : 2 = 5,4    ·    bé = 9,5 − 5,4 = 4,1',
    note='Ca sư phụ dịch chữ ra số: tổng = 99 · hiệu = 11 → 55 và 44'),
    caption='Chỉ cần cẩn thận đặt thẳng hàng dấu phẩy khi cộng trừ'),

'DL:KSN5Q1.B25.M3': dict(archetype='two_way_compare', params=dict(
    title='CHU VI 36 cm — DÙNG SỐ NÀO LÀM TỔNG?',
    wrong=dict(head='DÙNG CẢ VÒNG', steps=['tổng = 36'], result='dài 20 · rộng 16 ✗'),
    right=dict(head='DÙNG NỬA CHU VI', steps=['tổng = 36 : 2 = 18'], result='dài 11 · rộng 7 ✓'),
    verdict='Kiểm: (11 + 7) × 2 = 36 ✓ — chu vi là HAI lần (dài + rộng)'),
    caption='Tổng – hiệu hay trốn sau chu vi hoặc sau lời khai "thêm k thì bằng nhau"'),

# ── B26 · Ba số & số liên tiếp ────────────────────────────────────
'DL:KSN5Q1.B26.M1': dict(archetype='ladder_steps', params=dict(
    title='BA HỘP CÂN TỪNG ĐÔI: A+B = 25 · B+C = 30 · C+A = 29',
    steps=[dict(text='Cộng ba cặp', sub='25 + 30 + 29 = 84'),
           dict(text='Mỗi hộp bị ĐẾM HAI LẦN', sub='tổng ba hộp = 84 : 2 = 42'),
           dict(text='Trừ từng cặp ra từng hộp', sub='C = 42 − 25 = 17 · A = 12 · B = 13')],
    note='Bỏ cặp không chứa C ra khỏi tổng thì phần còn lại đúng bằng C'),
    caption='Cộng cặp là đếm đôi — chia 2 rồi mới trừ'),

'DL:KSN5Q1.B26.M2': dict(archetype='sum_diff_bars', params=dict(
    title='"LIÊN TIẾP" LÀ LỜI KHAI HIỆU TRÁ HÌNH',
    small=dict(label='số bé 42', val=42), big=dict(label='số lớn 44', val=44),
    diff_label='hiệu 2', total_label='tổng 86',
    formula='hai số CHẴN liên tiếp → hiệu 2 → bé = (86 − 2) : 2 = 42',
    note='Tự nhiên liên tiếp thì hiệu 1 · chẵn (hay lẻ) liên tiếp thì hiệu 2'),
    caption='Nghe chữ "liên tiếp" là biết ngay hiệu bằng bao nhiêu'),

'DL:KSN5Q1.B26.M3': dict(archetype='two_way_compare', params=dict(
    title='MÁY CHẴN LẺ SOI ĐỀ TRƯỚC KHI GIẢI',
    wrong=dict(head='VÉ MA — vô nghiệm', steps=['hai số CHẴN liên tiếp', 'tổng = 99 (LẺ)'],
               result='chẵn + chẵn = CHẴN ✗'),
    right=dict(head='VÉ THẬT', steps=['ba số LẺ liên tiếp', 'tổng 99 : 3 = 33'],
               result='31 · 33 · 35 ✓'),
    verdict='Biên bản một dòng là trọn điểm — khỏi mò mẫm'),
    caption='Soi chẵn lẻ ở cổng: đề vô nghiệm thì phát hiện ngay'),

# ── B27 · Cú chuyển ───────────────────────────────────────────────
'DL:KSN5Q1.B27.M1': dict(archetype='two_way_compare', params=dict(
    title='CHUYỂN 5 QUYỂN TỪ KỆ A SANG KỆ B — LUẬT KÉP', neutral=True,
    wrong=dict(head='TỔNG', steps=['của không sinh không mất', 'chỉ đổi kệ'], result='KHÔNG ĐỔI'),
    right=dict(head='HIỆU', steps=['bên mất 5 · bên được 5'], result='ĐỔI 2 × 5 = 10'),
    verdict='Kiểm: 30 − 5 = 25 = 20 + 5 → hiệu 10 khép trọn'),
    caption='Tổng đứng im — hiệu đổi HAI lần lượng chuyển'),

'DL:KSN5Q1.B27.M2': dict(archetype='sum_diff_bars', params=dict(
    title='CHUYỂN 5 QUYỂN THÌ HAI KỆ BẰNG NHAU (TỔNG 90)',
    small=dict(label='kệ 2 · 40', val=40), big=dict(label='kệ 1 · 50', val=50),
    diff_label='hiệu 10 = 2 × 5', total_label='tổng 90',
    formula='hiệu ban đầu = 2 × 5 = 10 → kệ 1 = (90 + 10) : 2 = 50',
    note='Thử: 50 − 5 = 45 = 40 + 5 ✓'),
    caption='"Chuyển k thì bằng nhau" → hiệu ban đầu đúng bằng 2k'),

'DL:KSN5Q1.B27.M3': dict(archetype='two_way_compare', params=dict(
    title='HAI CA NÂNG CAO CỦA CÚ CHUYỂN', neutral=True,
    wrong=dict(head='NỚI KHOẢNG CÁCH', steps=['chuyển 3 từ bên ÍT sang bên NHIỀU', 'hiệu sau = 16'],
               result='hiệu đầu = 16 − 6 = 10'),
    right=dict(head='ĐỔI NGÔI', steps=['chuyển 5, bên kia hơn ngược 4'],
               result='hiệu đầu = 2 × 5 − 4 = 6'),
    verdict='Vẽ sơ đồ TRƯỚC – SAU hai tầng rồi mới lắp máy tổng – hiệu'),
    caption='Chuyển từ bên ít sang bên nhiều thì hiệu NỚI thêm 2k'),

# ── B28 · Toán tuổi ───────────────────────────────────────────────
'DL:KSN5Q1.B28.M1': dict(archetype='place_value_chart', params=dict(
    title='ĐƯỜNG RAY SONG SONG: HIỆU TUỔI KHÔNG BAO GIỜ ĐỔI',
    headers=['hiện nay', 'sau 3 năm', 'sau 5 năm'], comma_after=None,
    rows=[dict(label='mẹ', cells=['32', '35', '37'], color='white'),
          dict(label='con', cells=['8', '11', '13'], color='white'),
          dict(label='hiệu', cells=['24', '24', '24'], color='#E6FAF5', highlight=[0, 1, 2]),
          dict(label='tổng', cells=['40', '46', '50'], color='#FFF4DF')],
    note='Hiệu ĐỨNG IM 24 · tổng TRÔI 2 tuổi mỗi năm (mỗi người thêm 1)'),
    caption='Hai đường ray song song: khoảng cách giữa chúng không bao giờ đổi'),

'DL:KSN5Q1.B28.M2': dict(archetype='sum_diff_bars', params=dict(
    title='MẤY NĂM NỮA TUỔI MẸ GẤP 3 LẦN TUỔI CON?',
    small=dict(label='con lúc đó · 1 phần = 12', val=12),
    big=dict(label='mẹ lúc đó · 3 phần = 36', val=36),
    diff_label='hiệu 24 = 2 phần', total_label='tổng 48',
    formula='hiệu 24 = (3 − 1) = 2 phần → 1 phần = 12 → con 12 tuổi → 12 − 8 = 4 năm nữa',
    note='Vẽ sơ đồ phần TẠI MỐC ĐÍCH — hiệu vẫn là 24 vì hiệu không đổi'),
    caption='Gấp k lần thì hiệu chiếm đúng (k − 1) phần'),

'DL:KSN5Q1.B28.M3': dict(archetype='ladder_steps', params=dict(
    title='QUY MỌI DỮ KIỆN VỀ MỘT MỐC RỒI MỚI GIẢI',
    steps=[dict(text='Quy TỔNG về hôm nay', sub='24 − 2 × 3 = 18 (ba năm nữa mỗi người +3)'),
           dict(text='Hiệu là NEO, giữ nguyên', sub='hiệu 6 tuổi'),
           dict(text='Lắp máy tổng – hiệu', sub='anh = (18 + 6) : 2 = 12 · em = 6')],
    note='Định vị thời điểm: tuổi đích BÉ hơn tuổi nay → "mấy năm TRƯỚC" (bố 41/con 9 → 1 năm trước)'),
    caption='Tổng phải quy về mốc — hiệu thì khỏi, vì hiệu không đổi'),
}
