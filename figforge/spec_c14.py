# -*- coding: utf-8 -*-
"""Lô A14 · Chương 14 (B53–B56): vận tốc · đuổi gặp · đường vòng – dòng nước · tàu dài – hai kim."""

SPEC = {
# ── B53 · Vận tốc nền ─────────────────────────────────────────────
'DL:KSN5Q1.B53.M1': dict(archetype='place_value_chart', params=dict(
    title='TAM GIÁC V - S - T: CHE Ô CẦN TÌM LÀ RA CÔNG THỨC',
    headers=['che ô nào', 'công thức lộ ra', 'ví dụ'], comma_after=None,
    rows=[dict(label='', cells=['che V', 'V = S : T', '45 : 3 = 15 km/h'], color='#E6FAF5'),
          dict(label='', cells=['che S', 'S = V × T', '5 × 2 = 10 km'], color='white'),
          dict(label='', cells=['che T', 'T = S : V', '30 : 15 = 2 giờ'], color='#FFF4DF')],
    note='Sớm - muộn ba nhịp: T đi 3 : 12 = 15 phút → 6 giờ 50 + 15 = 7 giờ 05 (mốc đồng hồ THẬT)'),
    caption='Một tam giác — ba công thức, khỏi học thuộc ba lần'),

'DL:KSN5Q1.B53.M2': dict(archetype='two_way_compare', params=dict(
    title='ĐỔI 36 km/h SANG m/s — CHIA HAY NHÂN 3,6?',
    wrong=dict(head='NHÂN 3,6', steps=['36 × 3,6 = 129,6', 'đổi ngược = 466 km/h'],
               result='xe đạp vượt tàu cao tốc ✗'),
    right=dict(head='CHIA 3,6', steps=['36 : 3,6 = 10 m/s'], result='số BÉ ĐI đúng luật ✓'),
    verdict='Cặp lính gác 36 km/h = 10 m/s canh cửa · lên km/h thì nhân: 20 × 3,6 = 72'),
    caption='Một giây ngắn hơn một giờ rất nhiều nên xuống m/s số phải bé đi'),

'DL:KSN5Q1.B53.M3': dict(archetype='balance_scale', params=dict(
    title='Vtb ĐI - VỀ: KIM NGHIÊNG VỀ PHÍA CHẬM',
    left=dict(text='đi 30 km/h · LẾT 2 giờ', weight=2),
    right=dict(text='về 60 km/h · bay 1 giờ', weight=1),
    verdict='Vtb = 120 : 3 = 40 km/h  —  KHÔNG phải (30 + 60) : 2 = 45',
    note='Phép thử: 45 × 3 giờ = 135 km mà đường đi về chỉ 120 km — dư 15 km ma!'),
    caption='Nửa THỜI GIAN thì khác: hai nửa giờ bằng nhau → 90 : 2 = 45 mới đúng'),

# ── B54 · Đuổi kịp – gặp nhau ─────────────────────────────────────
'DL:KSN5Q1.B54.M1': dict(archetype='motion_track', params=dict(
    title='NGƯỢC CHIỀU: GẶP NHAU CHIA TỔNG VẬN TỐC',
    from_label='A', to_label='B', length_label='36 km',
    movers=[{'name': 'xe 1', 'from': 0.06, 'dir': '>', 'speed': '10 km/h'},
            {'name': 'xe 2', 'from': 0.94, 'dir': '<', 'speed': '8 km/h'}],
    meet=dict(at=0.555, label='gặp sau 2 giờ · cách A 20 km'),
    notes=['36 : (10 + 8) = 2 giờ', 'kiểm hai phía: 20 + 16 = 36 ✓']),
    caption='Cùng hướng thì chia HIỆU (5 : 5 = 1 giờ) — đối đầu thì chia TỔNG'),

'DL:KSN5Q1.B54.M2': dict(archetype='motion_track', params=dict(
    title='XUẤT PHÁT KHÁC GIỜ — CHỤP ẢNH KHOẢNG CÁCH THẬT',
    from_label='A', to_label='B', length_label='AB = 46 km',
    movers=[{'name': 'xe 1 đi từ 7 giờ', 'from': 0.05, 'dir': '>', 'speed': '10 km/h'},
            {'name': 'xe 2 đi từ 8 giờ', 'from': 0.95, 'dir': '<', 'speed': '8 km/h'}],
    meet=dict(at=0.22, label='lúc 8 giờ xe 1 đã đi 10 km'),
    notes=['khoảng cách THẬT = 46 − 10 = 36', '36 : 18 = 2 giờ → gặp lúc 10 giờ']),
    caption='Chia thẳng 46 là tính với tấm ảnh cũ chụp lúc 7 giờ'),

'DL:KSN5Q1.B54.M3': dict(archetype='motion_track', params=dict(
    title='GẶP LẦN HAI: TỔNG QUÃNG = 3 LẦN AB',
    from_label='A', to_label='B', length_label='AB = 36 km',
    movers=[{'name': 'lần 1: gộp 1 × AB', 'from': 0.10, 'dir': '>', 'speed': '10 km/h'},
            {'name': 'vòng lại: thêm 2 × AB', 'from': 0.90, 'dir': '<', 'speed': '8 km/h'}],
    meet=dict(at=0.555, label='★ gặp lần 1 sau 2 giờ'),
    notes=['3 × 36 = 108 km  →  108 : 18 = 6 giờ', 'đoán "gấp đôi" là hụt nguyên một lần đường']),
    caption='Sau khi gặp: sơ đồ một vạch, sao tại km 20 → còn 16 km → 1 giờ 36 phút'),

# ── B55 · Đường vòng & dòng nước ──────────────────────────────────
'DL:KSN5Q1.B55.M1': dict(archetype='geo_shape', params=dict(
    title='ĐƯỜNG VÒNG 400 m — GẶM TRỌN MỘT VÒNG',
    points=dict(O=[0, 0], S=[0, 5], M=[4.05, -2.94], L=[-2.9, 4.1], R2=[2.9, 4.1]),
    shapes=[dict(circle=dict(at='O', r=5), fill='none')],
    segments=[dict(**{'from': 'S', 'to': 'L'}, color='#1FCBAB', label='3 m/s →', dx=-12, dy=3),
              dict(**{'from': 'S', 'to': 'R2'}, color='#C0392B', label='← 2 m/s', dx=12, dy=3)],
    labels=[dict(at='S', text='xuất phát', dy=5), dict(at='M', text='gặp nhau', dy=-5, dx=8)],
    show_points=['S', 'M'],
    formula='ngược chiều: 400 : (3 + 2) = 80 giây  ·  cùng chiều: 400 : (3 − 2) = 400 giây',
    note='240 + 160 = 400 tròn vòng ✓ — điểm gặp KHÔNG ở nửa vòng vì hai bạn chạy khác tốc độ'),
    caption='Xuất phát cùng điểm mà ngược chiều: khoảng cách cần gặm là trọn một vòng'),

'DL:KSN5Q1.B55.M2': dict(archetype='sum_diff_bars', params=dict(
    title='DÒNG NƯỚC: XUÔI HƠN NGƯỢC ĐÚNG HAI LẦN V NƯỚC',
    small=dict(label='ngược 9 km/h', val=9), big=dict(label='xuôi 15 km/h', val=15),
    diff_label='hiệu 6 = 2 × nước', total_label='tổng 24',
    formula='nước = (15 − 9) : 2 = 3  ·  thực = (15 + 9) : 2 = 12 km/h',
    note='Băng chuyền: xuôi được CÕNG (12 + 3) · ngược bị CẢN (12 − 3) — quên chia 2 là nước gấp đôi'),
    caption='Bộ xương Tổng - Hiệu của bài 43 khoác áo sông nước'),

'DL:KSN5Q1.B55.M3': dict(archetype='two_way_compare', params=dict(
    title='KHÓM BÈO TRÔI 36 km — CHIA CHO VẬN TỐC NÀO?',
    wrong=dict(head='LẤY V THUYỀN', steps=['36 : 12'], result='3 giờ ✗ (bèo mọc chân vịt?)'),
    right=dict(head='LẤY V DÒNG NƯỚC', steps=['bèo KHÔNG có máy', '36 : 3'], result='12 giờ ✓'),
    verdict='Hành trình kép: xuôi 2 giờ 24 phút + ngược 4 giờ = 6 giờ 24 phút'),
    caption='Vật trôi tự do đi đúng bằng vận tốc dòng nước — soi máy trước khi chia'),

# ── B56 · Tàu dài & hai kim ───────────────────────────────────────
'DL:KSN5Q1.B56.M1': dict(archetype='geo_shape', params=dict(
    title='QUAY CHẬM: MŨI CHẠM ĐẦU CẦU — ĐUÔI RỜI CUỐI CẦU',
    points=dict(A=[0, 3.2], B=[12, 3.2], C=[12, 4.6], D=[0, 4.6],
                P=[3, 0], Q=[21, 0], R=[3, 1.6], S2=[21, 1.6]),
    shapes=[dict(pts=['P', 'Q', 'S2', 'R'], fill='pale', label='cầu 180 m'),
            dict(pts=['A', 'B', 'C', 'D'], fill='navy', label='thân tàu 120 m')],
    segments=[dict(**{'from': 'A', 'to': 'P'}, dashed=True, color='#C0392B'),
              dict(**{'from': 'B', 'to': 'Q'}, dashed=True, color='#C0392B', label='mũi chạm → đuôi rời', dx=-6, dy=6)],
    show_points=[],
    formula='quãng = cầu + thân = 180 + 120 = 300 m  →  300 : 15 = 20 giây',
    note='Chia mỗi cầu trần ra 12 giây — lúc ấy ĐUÔI tàu còn nằm giữa cầu, gác chắn chưa mở rào'),
    caption='Mốc là ĐIỂM thì cộng không (120 : 15 = 8 giây) · mốc có chiều dài thì cộng mốc'),

'DL:KSN5Q1.B56.M2': dict(archetype='two_way_compare', params=dict(
    title='MỐC BIẾT CHẠY — THÂN TÀU GIỮ LUẬT, VẬN TỐC ĐỔI', neutral=True,
    wrong=dict(head='NGƯỢC CHIỀU', steps=['người lao tới gặm phụ', '120 : (15 + 1)'],
               result='7,5 giây'),
    right=dict(head='CÙNG CHIỀU', steps=['mốc chạy trốn', '120 : (15 − 5)'], result='12 giây'),
    verdict='Hai tàu qua nhau: cộng CẢ HAI THÂN → (180 + 120) : 25 = 12 giây'),
    caption='Cột đèn đứng yên mất 8 giây — mốc chạy trốn thì lâu hơn, lao tới thì nhanh hơn'),

'DL:KSN5Q1.B56.M3': dict(archetype='clock_face', params=dict(
    title='HAI KIM TRÙNG NHAU — 12 GIỜ CHỈ 11 LẦN',
    clocks=[dict(hour=12, minute=0, label='12:00'),
            dict(hour=1, minute=5, label='≈ 1:05'),
            dict(hour=3, minute=16, label='≈ 3:16')],
    note='hiệu 1 − 1/12 = 11/12 vòng/giờ → chu kỳ 12/11 giờ ≈ 1 giờ 05 → 12 : 12/11 = 11 lần'),
    caption='Bài đuổi kịp trên vòng đua tí hon: kim phút phải dư trọn một vòng'),
}
