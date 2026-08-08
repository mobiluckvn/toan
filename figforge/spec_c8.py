# -*- coding: utf-8 -*-
"""Lô A8 · Chương 8 (B29–B32): tổng – tỉ · hiệu – tỉ · tỉ ẩn · tỉ biến hình."""

SPEC = {
# ── B29 · Tổng – tỉ ───────────────────────────────────────────────
'DL:KSN5Q1.B29.M1': dict(archetype='bar_diagram', params=dict(
    title='TỔNG 36 · SỐ LỚN GẤP ĐÔI SỐ BÉ',
    bars=[dict(name='số bé', units=1, label='1 phần = 12'),
          dict(name='số lớn', units=2, label='2 phần = 24')],
    brace=dict(text='ĐẾM 3 phần  →  CHIA 36 : 3 = 12  →  NHÂN ra từng số'),
    note='Ba nhịp: đếm tổng số phần — chia ra giá một phần — nhân ra từng số'),
    caption='Sơ đồ phần: mỗi ô là một phần bằng nhau'),

'DL:KSN5Q1.B29.M2': dict(archetype='place_value_chart', params=dict(
    title='THAY ÁO TỈ SỐ VỀ HAI SỐ PHẦN NGUYÊN',
    headers=['trang phục', 'đổi ra phân số', 'tỉ số'], comma_after=None,
    rows=[dict(label='', cells=['75%', '3/4', '3 : 4'], color='#E6FAF5'),
          dict(label='', cells=['40%', '2/5', '2 : 5'], color='white'),
          dict(label='', cells=['gấp rưỡi', '3/2', '3 : 2'], color='#FFF4DF'),
          dict(label='', cells=['bằng nửa', '1/2', '1 : 2'], color='white')],
    note='Thay áo xong thì bài 75% giống hệt bài 3/4: 7 phần = 35 → mè 15 · bơ 20'),
    caption='Mọi trang phục của tỉ đều phải thay về hai số phần nguyên trước khi kẻ ô'),

'DL:KSN5Q1.B29.M3': dict(archetype='bar_diagram', params=dict(
    title='BÌNH 8,4 LÍT · NƯỚC CAM GẤP 3 LẦN XI-RÔ',
    bars=[dict(name='xi-rô', units=1, label='1 phần = 2,1 lít'),
          dict(name='nước cam', units=3, label='3 phần = 6,3 lít')],
    brace=dict(text='4 phần = 8,4  →  1 phần = 8,4 : 4 = 2,1 lít'),
    note='Giá một phần được phép LẺ — thập phân không làm đổi luật · nửa chu vi 30 : 2 = 15 cũng vậy'),
    caption='Chia ra số lẻ vẫn đúng, đừng thấy lẻ mà tưởng làm sai'),

# ── B30 · Tổng ẩn & chuỗi tỉ ──────────────────────────────────────
'DL:KSN5Q1.B30.M1': dict(archetype='bar_diagram', params=dict(
    title='TỈ LÀ ẢNH CHỤP CÓ NGÀY GIỜ — VẼ TẠI ĐÚNG MỐC CÓ TỈ',
    bars=[dict(name='kho 2 (sau bán)', units=1, label='1 phần = 20 tấn'),
          dict(name='kho 1 (sau bán)', units=3, label='3 phần = 60 tấn')],
    brace=dict(text='4 phần = 80 tấn  →  1 phần = 20  →  cộng TRẢ: 72 và 28 tấn'),
    note='Bán 12 ở kho 1 và 8 ở kho 2 → giải xong ở mốc có tỉ rồi mới trả lại phần đã bớt'),
    caption='Giải ở mốc có tỉ — rồi mới trả về mốc đề hỏi'),

'DL:KSN5Q1.B30.M2': dict(archetype='bar_diagram', params=dict(
    title='CHUỖI TỈ BA SỐ — ĐỔI HẾT VỀ MỘT THƯỚC ĐO',
    bars=[dict(name='số thứ nhất', units=1, label='1 phần = 10'),
          dict(name='số thứ hai', units=2, label='2 phần = 20'),
          dict(name='số thứ ba', units=4, label='4 phần = 40')],
    brace=dict(text='thước = số bé nhất  →  1 + 2 + 4 = 7 phần = 70  →  1 phần = 10'),
    note='"C gấp đôi B" mà B đã 2 phần thì C là 4 phần — không phải 2'),
    caption='Một thước đo chung cho cả ba số rồi mới cộng phần'),

'DL:KSN5Q1.B30.M3': dict(archetype='bar_diagram', params=dict(
    title='TBC 20 CỦA BA SỐ · TỈ 1 : 2 : 3',
    bars=[dict(name='số 1', units=1, label='10'),
          dict(name='số 2', units=2, label='20'),
          dict(name='số 3', units=3, label='30')],
    brace=dict(text='KÉO MÀN: tổng = 20 × 3 = 60  →  6 phần  →  1 phần = 10'),
    note='Gặp trung bình cộng thì kéo màn trước — nhân ra TỔNG rồi mới chia phần'),
    caption='Cây cầu tổng của bài 21 nối thẳng sang máy chia phần'),

# ── B31 · Hiệu – tỉ & hai cái hang ────────────────────────────────
'DL:KSN5Q1.B31.M1': dict(archetype='bar_diagram', params=dict(
    title='HIỆU 15 · SỐ LỚN GẤP 4 LẦN SỐ BÉ',
    bars=[dict(name='số bé', units=1, label='1 phần = 5'),
          dict(name='số lớn', units=4, label='4 phần = 20')],
    brace=dict(text='PHẦN CHÊNH = 4 − 1 = 3 phần = 15  →  1 phần = 5'),
    note='Tổng thì cặp với TỔNG số phần · hiệu thì cặp với PHẦN CHÊNH — đừng lẫn'),
    caption='Hiệu nằm ở phần chênh, không phải ở tổng số phần'),

'DL:KSN5Q1.B31.M2': dict(archetype='ladder_steps', params=dict(
    title='HANG TRỐN THỨ NHẤT: HIỆU NÚP TRONG CÚ CHUYỂN',
    steps=[dict(text='TẦNG 1 · khui hiệu', sub='chuyển 10 thì bằng nhau → hiệu = 2 × 10 = 20'),
           dict(text='TẦNG 2 · kẻ ô hiệu – tỉ', sub='gấp 3 → chênh 2 phần = 20 → 1 phần = 10'),
           dict(text='Đọc đáp', sub='kệ dưới 10 · kệ trên 30 · thử: 20 = 20 ✓')],
    note='Ca đổi ngôi: chuyển 6 mà bên kia hơn ngược 4 → hiệu = 2 × 6 − 4 = 8'),
    caption='Khui hiệu bằng luật 2k của bài 27 rồi mới kẻ ô'),

'DL:KSN5Q1.B31.M3': dict(archetype='ladder_steps', params=dict(
    title='HANG TRỐN THỨ HAI: MƯỢN HIỆU TUỔI BẤT BIẾN',
    steps=[dict(text='Hiệu tuổi là NEO', sub='mẹ hơn con 24 tuổi — không bao giờ đổi'),
           dict(text='Mang neo sang mốc gấp 5', sub='chênh 5 − 1 = 4 phần = 24 → con lúc đó 6'),
           dict(text='Định vị thời điểm', sub='6 < 8 → hai năm TRƯỚC · thử: mẹ 30 = 5 × 6 ✓')],
    note='Chiều ngược: sau 4 năm mẹ gấp 3 lần con 12 → mẹ lúc đó 36 → mẹ nay 32'),
    caption='Hiệu tuổi mượn được từ mốc này sang mốc khác vì nó bất biến'),

# ── B32 · Tỉ ẩn & tỉ biến hình ────────────────────────────────────
'DL:KSN5Q1.B32.M1': dict(archetype='two_way_compare', params=dict(
    title='KHUI TỈ ẨN: 2/3 CỦA A BẰNG 3/4 CỦA B', neutral=True,
    wrong=dict(head='QUY ĐỒNG TỬ — VẾ A', steps=['2/3 = 6/9'], result='A chia 9 phần'),
    right=dict(head='QUY ĐỒNG TỬ — VẾ B', steps=['3/4 = 6/8'], result='B chia 8 phần'),
    verdict='A : B = 9 : 8  →  ghép tổng 34 → A 18 · B 16'),
    caption='Miếng lấy ra nhỏ hơn thì cả cái phải nhiều hơn'),

'DL:KSN5Q1.B32.M2': dict(archetype='bar_diagram', params=dict(
    title='THÊM CHỮ SỐ 0 = GẤP 10 · HIỆU 108',
    bars=[dict(name='số bé', units=1, label='1 phần = 12'),
          dict(name='số lớn', units=10, label='10 phần = 120')],
    brace=dict(text='HIỆU 9 phần = 108  →  1 phần = 12  →  hai số 12 và 120'),
    note='Cho TỔNG thì chia 11 phần · cho HIỆU thì chia 9 phần — thử: 120 − 12 = 108 ✓'),
    caption='Cùng một tỉ 1 : 10 nhưng tổng và hiệu đọc ở hai chỗ khác nhau'),

'DL:KSN5Q1.B32.M3': dict(archetype='two_way_compare', params=dict(
    title='TỈ BIẾN HÌNH: AI ĐỨNG IM NGƯỜI ẤY LÀM THƯỚC', neutral=True,
    wrong=dict(head='SƠ ĐỒ TRƯỚC', steps=['Su Bống 1 phần', 'Cáo Đề 3 phần'], result='gấp 3 lần'),
    right=dict(head='SƠ ĐỒ SAU', steps=['Su Bống vẫn 1 phần', 'Cáo Đề 2 phần'], result='gấp 2 lần'),
    verdict='Chênh 1 phần = 6 viên  →  Su Bống 6 · Cáo Đề 18'),
    caption='Su Bống không đổi nên lấy làm thước — chênh tầng chính là manh mối'),
}
