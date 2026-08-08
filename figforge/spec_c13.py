# -*- coding: utf-8 -*-
"""Lô A13 · Chương 13 (B49–B52): hình tròn · vành khăn – hình ghép · diện tích xung quanh · thể tích."""

SPEC = {
# ── B49 · Hình tròn ───────────────────────────────────────────────
'DL:KSN5Q1.B49.M1': dict(archetype='plane_geometry', params=dict(
    title='HAI CÁNH CỬA: C ĐÓN ĐƯỜNG KÍNH — S CHỈ ĐÓN BÁN KÍNH',
    shape='circle', dims=dict(d='d = 1 m', r='r = 0,5 m'),
    memo=['C = d × 3,14', 'S = r × r × 3,14'],
    caption='Miệng giếng d = 1 m: C = 3,14 m nhưng S phải đổi r = 0,5 → 0,785 m²'),
    caption='Nghi thức BƯỚC 0: thấy đường kính mà cần diện tích thì chia đôi ngay'),

'DL:KSN5Q1.B49.M2': dict(archetype='two_way_compare', params=dict(
    title='BÀI NGƯỢC: TỪ C VÀ TỪ S VỀ BÁN KÍNH', neutral=True,
    wrong=dict(head='NGƯỢC TỪ CHU VI', steps=['31,4 : 3,14 = 10'], result='d = 10 → r = 5'),
    right=dict(head='NGƯỢC TỪ DIỆN TÍCH', steps=['78,5 : 3,14 = 25', 'số nào nhân chính nó ra 25?'],
               result='r = 5 (thử 5 × 5 = 25)'),
    verdict='CẤM chia 25 cho 2 — phải đố "số nhân chính nó"'),
    caption='Từ C thì chia thẳng · từ S thì còn một câu đố nữa mới ra bán kính'),

'DL:KSN5Q1.B49.M3': dict(archetype='geo_shape', params=dict(
    title='HỒ MỞ RỘNG: r GẤP 2 THÌ S GẤP 4 — PHẦN THÊM GẤP 3',
    points=dict(O=[0, 0], A=[10, 0], B=[5, 0]),
    shapes=[dict(circle=dict(at='O', r=10), fill='teal', label=''),
            dict(circle=dict(at='O', r=5, z=4), fill='gold', label='hồ cũ 78,5', dy=0)],
    segments=[dict(**{'from': 'O', 'to': 'A'}, label='r mới = 10', dy=5, dx=12)],
    show_points=[],
    formula='S mới = 314  ·  phần mở rộng = 314 − 78,5 = 235,5 m² = 3 lần hồ cũ',
    note='C chứa MỘT lần r → gấp 2 · S chứa HAI lần r → gấp 2 × 2 = 4'),
    caption='Đếm số chữ r trong công thức là biết gấp mấy lần'),

# ── B50 · Vành khăn · hình ghép · bánh xe ─────────────────────────
'DL:KSN5Q1.B50.M1': dict(archetype='geo_shape', params=dict(
    title='VÀNH KHĂN = HIỆU HAI DIỆN TÍCH',
    points=dict(O=[0, 0], A=[5, 0], C=[0, 3]),
    shapes=[dict(circle=dict(at='O', r=5), fill='teal', label=''),
            dict(circle=dict(at='O', r=3, z=4), fill='white', label='S trong 28,26', dy=0)],
    segments=[dict(**{'from': 'O', 'to': 'A'}, label='R = 5', dx=14, dy=5),
              dict(**{'from': 'O', 'to': 'C'}, label='r = 3', dx=-11, dy=-2)],
    show_points=[],
    formula='vành khăn = 78,5 − 28,26 = 50,24 cm²',
    note='(5 − 3) × (5 − 3) × 3,14 = 12,56 là hình tròn bán kính 2 — trong hình KHÔNG có đường tròn ấy'),
    caption='Khoét tròn là TRỪ hai diện tích, không phải bình phương hiệu bán kính'),

'DL:KSN5Q1.B50.M2': dict(archetype='geo_shape', params=dict(
    title='CHỮ NHẬT ĐỘI NỬA TRÒN — LẦN NGÓN TAY MỘT VÒNG KÍN',
    points=dict(D=[0, 0], C=[10, 0], B=[10, 6], A=[0, 6], O=[5, 6]),
    shapes=[dict(pts=['D', 'C', 'B', 'A'], fill='pale', label='60 cm²'),
            dict(circle=dict(at='O', r=5, a0=0, a1=180), fill='teal', label='39,25 cm²', dy=2)],
    edge_labels=[dict(**{'from': 'D', 'to': 'C'}, text='10 cm', dy=-5),
                 dict(**{'from': 'D', 'to': 'A'}, text='6 cm', dx=-8)],
    show_points=['A', 'B', 'C', 'D'],
    formula='S = 60 + 39,25 = 99,25 cm²  ·  chu vi = 6 + 10 + 6 + 15,7 = 37,7 cm',
    note='Cạnh chung AB nằm BÊN TRONG hình — không cộng vào chu vi; cong cộng cong, thẳng lộ mới cộng'),
    caption='Nửa tròn: cong 15,7 phải CỘNG đoạn đáy thẳng mới thành vòng kín'),

'DL:KSN5Q1.B50.M3': dict(archetype='fence_posts', params=dict(
    title='BÁNH XE LĂN: MỖI VÒNG ĐI ĐƯỢC ĐÚNG MỘT CHU VI',
    first=0, last=314, step='1,57 m', show=6, show_step=True,
    labels=['0', '1,57', '3,14', '…', '312,4', '314 m'], gap_at=3,
    gap_note='mỗi bước = 1 vòng = 1 chu vi',
    formula='C = 0,5 × 3,14 = 1,57 m  →  số vòng = 314 : 1,57 = 200 vòng',
    note='Đơn vị phải bắt tay trước phép chia — mét với mét, xăng-ti-mét với xăng-ti-mét'),
    caption='Dựng chu vi từ đường kính trước, rồi mới chia quãng đường'),

# ── B51 · Diện tích xung quanh – toàn phần ────────────────────────
'DL:KSN5Q1.B51.M1': dict(archetype='solid_3d', params=dict(
    title='TẤM ÁO TRẢI PHẲNG: Sxq = CHU VI ĐÁY × CAO',
    kind='box', dims=dict(a='dài 6 dm', b='rộng 4 dm', c='cao 3 dm'),
    memo=['Sxq = 20 × 3 = 60 dm²', 'hai đáy = 2 × 24 = 48', 'Stp = 60 + 48 = 108'],
    caption='Chu vi đáy (6 + 4) × 2 = 20 chính là chiều dài tấm áo'),
    caption='Tấm áo dài bằng chu vi đáy, rộng bằng chiều cao — trải ra là một chữ nhật'),

'DL:KSN5Q1.B51.M2': dict(archetype='two_way_compare', params=dict(
    title='THÙNG KHÔNG NẮP — TRỪ MẤY MẶT?',
    wrong=dict(head='TRỪ CẢ HAI ĐÁY', steps=['chỉ lấy Sxq = 60'], result='thùng thành ống thủng ✗'),
    right=dict(head='TRỪ ĐÚNG MỘT MẶT', steps=['Sxq + 1 đáy = 60 + 24'], result='84 dm² ✓'),
    verdict='Sơn cả trong lẫn ngoài: 84 × 2 = 168 dm² — mỗi tấm ván hai mặt ăn sơn'),
    caption='Đọc hợp đồng: không nắp thì bỏ nắp, đáy vẫn còn nguyên'),

'DL:KSN5Q1.B51.M3': dict(archetype='ladder_steps', params=dict(
    title='QUÉT VÔI: TRẦN CÓ — SÀN KHÔNG — CỬA TRỪ',
    steps=[dict(text='Bốn bức tường', sub='(8 + 6) × 2 × 4 = 112 m²'),
           dict(text='Cộng TRẦN (không cộng sàn)', sub='+ 8 × 6 = 48'),
           dict(text='Trừ diện tích cửa', sub='− 10  →  150 m²')],
    note='Chiều ngược: cao = Sxq : chu vi đáy = 60 : 20 = 3 dm → rộng = 10 − 6 = 4 dm'),
    caption='Ba chi tiết phải nhớ đủ: trần có, sàn không, cửa trừ'),

# ── B52 · Thể tích ────────────────────────────────────────────────
'DL:KSN5Q1.B52.M1': dict(archetype='solid_3d', params=dict(
    title='XẾP VIÊN ĐƯỜNG 1 dm³ ĐẦY BỂ',
    kind='box', dims=dict(a='dài 8 dm', b='rộng 5 dm', c='cao 4 dm'), layers=4,
    memo=['V = 8 × 5 × 4 = 160 dm³', '1 dm³ = 1 lít', 'bể chứa 160 lít'],
    caption='Hàng 8 viên · 5 hàng một lớp · 4 lớp chồng lên'),
    caption='Bộ ba gấp k: chu vi × k — diện tích × k × k — thể tích × k × k × k'),

'DL:KSN5Q1.B52.M2': dict(archetype='stack_compare', params=dict(
    title='BỂ LÀ CÁI VỎ — NƯỚC MỚI LÀ HIỆN TRẠNG',
    cols=[dict(tag='bể 160 lít', total=160, total_label='V bể = 160',
               parts=[dict(label='nước 128 lít (80%)', val=128, color='water'),
                      dict(label='phần trống 32', val=32, color='')]),
          dict(tag='thả hòn đá', total=160, total_label='dâng 0,5 dm',
               parts=[dict(label='nước 128 lít', val=128, color='water'),
                      dict(label='đá 20 dm³', val=20, color='anchor'),
                      dict(label='trống 12', val=12, color='')])],
    anchor_label='V đá = S đáy BỂ × độ dâng = 40 × 0,5 = 20 dm³',
    formula='V nước = 160 × 0,8 = 128 lít  →  cao nước = 128 : 40 = 3,2 dm',
    note='Nước dâng ĐỀU trên khắp đáy bể — không dâng riêng chỗ hòn đá'),
    caption='Chụp ảnh hiện trạng trước: dòng đầu luôn là "V nước = ..."'),

'DL:KSN5Q1.B52.M3': dict(archetype='place_value_chart', params=dict(
    title='BẢN ĐỒ CHỖ NGỒI TRONG RẠP SƠN',
    headers=['chỗ ngồi', 'số mặt sơn', 'công thức', 'khối 3³', 'khối 4³'], comma_after=None,
    rows=[dict(label='', cells=['ĐỈNH', '3 mặt', 'luôn 8', '8', '8'], color='#FFF4DF', highlight=[2]),
          dict(label='', cells=['CẠNH', '2 mặt', '12(n−2)', '12', '24'], color='#E6FAF5'),
          dict(label='', cells=['MẶT', '1 mặt', '6(n−2)²', '6', '24'], color='white'),
          dict(label='', cells=['LÕI', '0 mặt', '(n−2)³', '1', '8'], color='#EAF2FB')],
    note='SOI TỔNG tự chấm: 8 + 12 + 6 + 1 = 27 ✓  ·  8 + 24 + 24 + 8 = 64 ✓'),
    caption='Khối 3 mặt LUÔN là 8 với mọi n — vì hình hộp nào cũng chỉ có 8 đỉnh'),
}
