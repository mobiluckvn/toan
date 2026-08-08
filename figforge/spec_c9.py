# -*- coding: utf-8 -*-
"""Lô A9 · Chương 9 (B33–B36): hai tỉ số & thước bảo toàn · nhân chéo · toán tuổi nâng cao."""

SPEC = {
# ── B33 · Ba cây thước ────────────────────────────────────────────
'DL:KSN5Q1.B33.M1': dict(archetype='before_after_parts', params=dict(
    title='CHỈ SU BỐNG ĐỔI — SU KEM ĐỨNG IM LÀM THƯỚC',
    before=dict(tag='TRƯỚC', a=3, b=6, a_label='Su Bống 3/6', b_label='Su Kem 6 khúc'),
    after=dict(tag='SAU', a=4, b=6, a_label='Su Bống 4/6', b_label='Su Kem 6 khúc'),
    delta=dict(label='nhích 1 khúc = 4 viên'),
    formula='1 khúc = 4  →  Su Kem = 24  ·  Su Bống lúc đầu = 12',
    note='Quy 1/2 và 2/3 về cùng mẫu 6 rồi mới so — kẻ đứng im mới được cầm thước'),
    caption='Câu hỏi mở cửa mọi bài hai tỉ số: CÁI GÌ KHÔNG ĐỔI?'),

'DL:KSN5Q1.B33.M2': dict(archetype='before_after_parts', params=dict(
    title='CÙNG THÊM 5 VIÊN — HIỆU BẤT BIẾN LÀM THƯỚC',
    before=dict(tag='TRƯỚC', a=2, b=6, a_label='A = 1/3 B (quy ×2)', b_label='B 6 khúc'),
    after=dict(tag='SAU', a=3, b=6, a_label='A = 1/2 B', b_label='B 6 khúc'),
    delta=dict(label='A nhích 1 khúc = 5'),
    formula='hiệu trước 4 khúc · hiệu sau 3 khúc → quy cùng khúc rồi so: 1 khúc = 5',
    note='"Phần" của hai sơ đồ chỉ so được khi cây thước hiệu đã cùng số khúc'),
    caption='Cùng thêm hay cùng bớt thì HIỆU không đổi — nhưng phải quy khúc trước'),

'DL:KSN5Q1.B33.M3': dict(archetype='before_after_parts', params=dict(
    title='CHUYỂN QUA LẠI — TỔNG BẤT BIẾN LÀM THƯỚC',
    before=dict(tag='TRƯỚC', a=4, b=6, a_label='kệ A = 2/3 kệ B', b_label='kệ B'),
    after=dict(tag='SAU', a=5, b=5, a_label='hai kệ bằng nhau', b_label='kệ B'),
    delta=dict(label='A nhích 1 khúc = 10 quyển'),
    formula='quy tổng 10 khúc: 4 : 6 → 5 : 5  →  1 khúc = 10  →  A = 40 · B = 60',
    note='Ba trạm thử: đúng tỉ trước · đúng tỉ sau · đúng lượng chuyển'),
    caption='Chuyển qua lại thì tổng đứng im — quy số khúc TỔNG của hai sơ đồ'),

# ── B34 · Khi hết thước → nhân chéo ───────────────────────────────
'DL:KSN5Q1.B34.M1': dict(archetype='place_value_chart', params=dict(
    title='PHÂN LUỒNG: ĐỀ NÀY CÒN THƯỚC NÀO?',
    headers=['tình huống', 'cái gì bảo toàn', 'chiêu dùng'], comma_after=None,
    rows=[dict(label='', cells=['chỉ A đổi', 'B đứng im', 'thước B'], color='#E6FAF5'),
          dict(label='', cells=['cùng thêm/bớt như nhau', 'HIỆU', 'thước hiệu'], color='white'),
          dict(label='', cells=['chuyển qua lại', 'TỔNG', 'thước tổng'], color='#E6FAF5'),
          dict(label='', cells=['đổi KHÁC lượng', 'không gì cả', 'NHÂN CHÉO'], color='#FDECE9',
               highlight=[2])],
    note='Ba thước gãy hết thì mới dựng cân nhân chéo — đừng vội bỏ thước khi vẫn còn'),
    caption='Nhận diện luồng trước, chọn chiêu sau'),

'DL:KSN5Q1.B34.M2': dict(archetype='balance_scale', params=dict(
    title='DỰNG CÂN NHÂN CHÉO: 3 × (1p + 8) = 2 × (2p + 4)',
    left=dict(text='3 × (1 phần + 8) = 3p + 24', weight=1),
    right=dict(text='2 × (2 phần + 4) = 4p + 8', weight=1),
    verdict='Bớt đĩa đều tay: 24 − 8 = 1 phần  →  1 phần = 16',
    note='Truyện 16 · SGK 32 — thử: (16+8)/(32+4) = 24/36 = 2/3 ✓'),
    caption='"A = m/n của B" ⇔ n × A = m × B — cân hai đĩa rồi bớt đều tay'),

'DL:KSN5Q1.B34.M3': dict(archetype='ladder_steps', params=dict(
    title='BA TRẠM THỬ ĐÓNG ÁN MỌI BÀI HAI TỈ SỐ',
    steps=[dict(text='TRẠM 1 · tỉ TRƯỚC', sub='16/32 = 1/2 ✓'),
           dict(text='TRẠM 2 · tỉ SAU', sub='(16+8)/(32+4) = 24/36 = 2/3 ✓'),
           dict(text='TRẠM 3 · đúng CẢ HAI lượng', sub='thêm đúng 8 truyện và 4 SGK ✓')],
    note='Đường thử-đáp: có đáp rồi thì diễn lại kịch bản đề — qua ba trạm là trọn điểm'),
    caption='Qua đủ ba trạm mới được đóng án'),

# ── B35 · Toán tuổi nhiều mốc ─────────────────────────────────────
'DL:KSN5Q1.B35.M1': dict(archetype='sum_diff_bars', params=dict(
    title='TBC TUỔI HAI BỐ CON LÀ 25 · BỐ HƠN CON 28 TUỔI',
    small=dict(label='con 11', val=11), big=dict(label='bố 39', val=39),
    diff_label='hiệu 28', total_label='tổng 50',
    formula='KÉO MÀN: tổng = 25 × 2 = 50  →  bố = (50 + 28) : 2 = 39',
    note='Ba người: tổng 72 · gốc là con → 3 × con + 54 = 72 → con 6 · mẹ 32 · bố 34'),
    caption='Kéo màn TBC nhân ĐÚNG quân số rồi mới lắp máy tổng – hiệu'),

'DL:KSN5Q1.B35.M2': dict(archetype='before_after_parts', params=dict(
    title='HAI MỐC TUỔI — HIỆU BẤT BIẾN CẦM THƯỚC',
    before=dict(tag='5 NĂM TRƯỚC', a=2, b=10, a_label='con 2 khúc', b_label='mẹ 10 khúc (gấp 5)'),
    after=dict(tag='HIỆN NAY', a=3, b=9, a_label='con 3 khúc', b_label='mẹ 9 khúc (gấp 3)'),
    delta=dict(label='con nhích 1 khúc = 5 năm'),
    formula='quy hiệu về BCNN 8 khúc  →  1 khúc = 5  →  nay con 15 · mẹ 45',
    note='Phần nhích của con chính là SỐ NĂM giữa hai mốc'),
    caption='Hiệu tuổi không đổi nên nó là cây thước chung cho cả hai mốc'),

'DL:KSN5Q1.B35.M3': dict(archetype='place_value_chart', params=dict(
    title='TỔNG TUỔI HAI NGƯỜI TRÔI 2 MỖI NĂM',
    headers=['3 năm trước', 'hiện nay', '5 năm nữa'], comma_after=None,
    rows=[dict(label='tổng', cells=['16', '22', '32'], color='#FFF4DF', highlight=[1]),
          dict(label='em', cells=['4', '7', '12'], color='white'),
          dict(label='anh', cells=['12', '15', '20'], color='white')],
    note='Giải tại mốc THUẬN (3 năm trước: 16 = 4 phần) rồi TRƯỢT về mốc được hỏi'),
    caption='Lùi t năm thì tổng giảm 2t · tiến t năm thì tổng tăng 2t'),

# ── B36 · Một neo & hai luật trôi ─────────────────────────────────
'DL:KSN5Q1.B36.M1': dict(archetype='place_value_chart', params=dict(
    title='MỘT NEO 24 XỬ CẢ DÃY MỨC GẤP',
    headers=['mức gấp', 'hiệu mấy phần', 'tuổi con', 'thời điểm'], comma_after=None,
    rows=[dict(label='', cells=['gấp 7', '6 phần', '4 tuổi', '4 năm trước'], color='white'),
          dict(label='', cells=['gấp 5', '4 phần', '6 tuổi', '2 năm trước'], color='#E6FAF5'),
          dict(label='', cells=['gấp 4', '3 phần', '8 tuổi', 'hiện nay'], color='#FFF4DF', highlight=[3]),
          dict(label='', cells=['gấp 3', '2 phần', '12 tuổi', '4 năm nữa'], color='white')],
    note='Neo = 32 − 8 = 24 · gấp k thì hiệu chiếm (k − 1) phần → con = 24 : (k − 1)'),
    caption='Tính neo MỘT lần rồi mọi mốc soi lẫn nhau — mức gấp càng lớn càng lùi xa'),

'DL:KSN5Q1.B36.M2': dict(archetype='two_way_compare', params=dict(
    title='HAI LUẬT TRÔI CỦA NHÀ ĐÔNG NGƯỜI', neutral=True,
    wrong=dict(head='TBC TUỔI', steps=['trôi đúng 1 mỗi năm', 'với MỌI quân số'],
               result='30 → 35 sau 5 năm'),
    right=dict(head='TỔNG NHÓM', steps=['trôi theo ĐÚNG quân số', 'nhóm 2 người · lùi 4 năm'],
               result='giảm 2 × 4 = 8'),
    verdict='TBC trôi 1 · tổng trôi quân số × số năm — đừng lẫn hai luật'),
    caption='Đếm đúng quân số của nhóm đang xét mới tính được tổng trôi'),

'DL:KSN5Q1.B36.M3': dict(archetype='bar_diagram', params=dict(
    title='CHUỖI TỈ BA NGƯỜI: TỔNG TUỔI 84',
    bars=[dict(name='con', units=1, label='1 phần = 6 tuổi'),
          dict(name='mẹ', units=6, label='6 phần = 36'),
          dict(name='bố', units=7, label='7 phần = 42')],
    brace=dict(text='1 + 6 + 7 = 14 phần = 84  →  1 phần = 6 tuổi'),
    note='Tách nhóm: tuổi con = tổng cả nhà − tổng nhóm bố mẹ (mỗi tổng nhân đúng quân số)'),
    caption='Lấy người bé nhất làm gốc rồi xếp hàng như chuỗi tỉ bài 30'),
}
