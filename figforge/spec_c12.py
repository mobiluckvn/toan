# -*- coding: utf-8 -*-
"""Lô A12 · Chương 12 (B45–B48): tam giác · tỉ số diện tích · đường phụ · hình thang."""

SPEC = {
# ── B45 · Diện tích tam giác ──────────────────────────────────────
'DL:KSN5Q1.B45.M1': dict(archetype='geo_shape', params=dict(
    title='TAM GIÁC LÀ NỬA HÌNH CHỮ NHẬT CÙNG ĐÁY CÙNG CAO',
    points=dict(B=[0, 0], C=[12, 0], A=[4, 5], D=[0, 5], E=[12, 5], H=[4, 0]),
    shapes=[dict(pts=['B', 'C', 'E', 'D'], fill='none'),
            dict(pts=['B', 'C', 'A'], fill='teal', label='S = 30 cm²')],
    segments=[dict(**{'from': 'A', 'to': 'H'}, dashed=True, label='cao 5', dx=6)],
    edge_labels=[dict(**{'from': 'B', 'to': 'C'}, text='đáy 12', dy=-5)],
    show_points=['A', 'B', 'C'],
    formula='S = đáy × cao : 2 = 12 × 5 : 2 = 30 cm²',
    note='Bài ngược phải NHÂN 2 TRƯỚC: đáy = 30 × 2 : 5 = 12 (lấy 30 : 5 = 6 chỉ ra nửa đáy)'),
    caption='Nhìn tam giác nằm trong hình chữ nhật là hiểu ngay vì sao có dấu chia 2'),

'DL:KSN5Q1.B45.M2': dict(archetype='geo_shape', params=dict(
    title='CẶP ĐÁY - CAO PHẢI VUÔNG GÓC — CẠNH BÊN 13 LÀ MỒI NHỬ',
    points=dict(B=[0, 0], C=[12, 0], A=[4, 5], H=[4, 0]),
    shapes=[dict(pts=['B', 'C', 'A'], fill='pale')],
    segments=[dict(**{'from': 'A', 'to': 'H'}, dashed=True, label='cao 5 ⊥ đáy', dx=8)],
    edge_labels=[dict(**{'from': 'B', 'to': 'C'}, text='đáy 12', dy=-5),
                 dict(**{'from': 'A', 'to': 'C'}, text='cạnh bên 13 — KHÔNG dùng', dx=13, dy=3)],
    show_points=['A', 'B', 'C'],
    formula='12 × 5 : 2 = 30 m²  ·  bất biến: đáy × cao = 2S = 60',
    note='Đường cao ứng đáy 10 = 60 : 10 = 6 cm — mỗi cạnh có một đường cao riêng'),
    caption='Nghi thức chỉ tay: hai đường vào công thức phải vuông góc với nhau'),

'DL:KSN5Q1.B45.M3': dict(archetype='geo_shape', params=dict(
    title='TAM GIÁC VUÔNG: HAI CẠNH GÓC VUÔNG LÀ CẶP CÓ SẴN',
    points=dict(A=[0, 6], B=[0, 0], C=[8, 0], H=[2.88, 3.84]),
    shapes=[dict(pts=['A', 'B', 'C'], fill='teal', label='S = 24 cm²')],
    segments=[dict(**{'from': 'B', 'to': 'H'}, dashed=True, label='cao xuống huyền 4,8', dx=16)],
    edge_labels=[dict(**{'from': 'A', 'to': 'B'}, text='6 cm', dx=-8),
                 dict(**{'from': 'B', 'to': 'C'}, text='8 cm', dy=-5),
                 dict(**{'from': 'A', 'to': 'C'}, text='huyền 10 cm', dx=10, dy=4)],
    show_points=['A', 'B', 'C'],
    formula='6 × 8 : 2 = 24  →  cao xuống huyền = 24 × 2 : 10 = 4,8',
    note='Cạnh huyền chỉ được làm đáy khi có đường cao hạ xuống chính nó'),
    caption='Tam giác tù thì phải kéo dài đáy ra để đón đường cao rơi bên ngoài'),

# ── B46 · Tỉ số diện tích ─────────────────────────────────────────
'DL:KSN5Q1.B46.M1': dict(archetype='geo_shape', params=dict(
    title='CHUNG CAO → TỈ DIỆN TÍCH BẰNG TỈ ĐÁY',
    points=dict(B=[0, 0], C=[12, 0], A=[5, 6], M=[6, 0]),
    shapes=[dict(pts=['B', 'M', 'A'], fill='teal', label='S(ABM) = 18'),
            dict(pts=['M', 'C', 'A'], fill='gold', label='S(AMC) = 18')],
    edge_labels=[dict(**{'from': 'B', 'to': 'M'}, text='BM', dy=-5),
                 dict(**{'from': 'M', 'to': 'C'}, text='MC = BM', dy=-5)],
    show_points=['A', 'B', 'C', 'M'],
    formula='M là TRUNG ĐIỂM BC  →  S(ABM) = S(AMC) = 36 : 2 = 18 cm²',
    note='Hệ quả vàng: trung tuyến chia tam giác thành hai phần bằng nhau'),
    caption='Hai tam giác chung đường cao từ A — tỉ diện tích chính là tỉ hai đáy'),

'DL:KSN5Q1.B46.M2': dict(archetype='geo_shape', params=dict(
    title='ĐIỂM CHIA BM : MC = 2 : 3 · S(ABC) = 40 cm²',
    points=dict(B=[0, 0], C=[10, 0], A=[4, 6], M=[4, 0]),
    shapes=[dict(pts=['B', 'M', 'A'], fill='teal', label='2 phần = 16'),
            dict(pts=['M', 'C', 'A'], fill='navy', label='3 phần = 24')],
    edge_labels=[dict(**{'from': 'B', 'to': 'M'}, text='2 phần', dy=-5),
                 dict(**{'from': 'M', 'to': 'C'}, text='3 phần', dy=-5)],
    show_points=['A', 'B', 'C', 'M'],
    formula='chia 40 theo 2 : 3  →  16 và 24  ·  thử: 16 + 24 = 40 ✓',
    note='HAI MẪU SO SÁNH: so cả tam giác thì 2/5 · so phần kia thì 2 : 3 — đọc kỹ đề hỏi gì'),
    caption='Cây cọc M chia đáy theo tỉ nào thì chia diện tích theo tỉ ấy'),

'DL:KSN5Q1.B46.M3': dict(archetype='geo_shape', params=dict(
    title='CHUỖI TỈ NỐI TIẾP: NHÂN LỒNG NHAU QUA TỪNG TẦNG',
    points=dict(B=[0, 0], C=[12, 0], A=[5, 7], M=[6, 0], N=[5.5, 3.5]),
    shapes=[dict(pts=['B', 'C', 'A'], fill='none'),
            dict(pts=['A', 'B', 'M'], fill='pale'),
            dict(pts=['A', 'B', 'N'], fill='teal', label='S(ABN) = 12')],
    segments=[dict(**{'from': 'A', 'to': 'M'}, dashed=True),
              dict(**{'from': 'B', 'to': 'N'})],
    show_points=['A', 'B', 'C', 'M', 'N'],
    formula='48 × 1/2 × 1/2 = 12  ·  tầng 1: 24 → tầng 2: 12',
    note='CẤM cộng 1/2 + 1/3 — chuỗi tỉ phải NHÂN: 1/2 × 1/3 = 1/6'),
    caption='Mỗi tầng một lần nhân — đó là ruột của đề thi vào 6 chuyên'),

# ── B47 · Đường phụ & vu hồi ──────────────────────────────────────
'DL:KSN5Q1.B47.M1': dict(archetype='geo_shape', params=dict(
    title='ĐỈNH TRƯỢT TRÊN RAY — DIỆN TÍCH KHÔNG ĐỔI',
    points=dict(A=[0, 6], B=[12, 6], C=[12, 0], D=[0, 0], M=[4, 6], M2=[9, 6]),
    shapes=[dict(pts=['A', 'B', 'C', 'D'], fill='none'),
            dict(pts=['D', 'M', 'C'], fill='teal', label='S(DMC) = 48')],
    segments=[dict(**{'from': 'D', 'to': 'M2'}, dashed=True, color='#C0392B'),
              dict(**{'from': 'M2', 'to': 'C'}, dashed=True, color='#C0392B')],
    show_points=['A', 'B', 'C', 'D', 'M'],
    formula='S(DMC) = 96 : 2 = 48 cm²  —  M ở ĐÂU trên AB cũng vậy',
    note='Luật kỹ sư: mọi nét vẽ thêm phải KHAI BÁO — "nối A với C, ta được hai tam giác bằng nhau"'),
    caption='Đáy DC và đường cao (= chiều rộng) đều không đổi khi M trượt'),

'DL:KSN5Q1.B47.M2': dict(archetype='geo_shape', params=dict(
    title='VU HỒI: LẤY TỔNG TRỪ BA PHẦN TRẮNG',
    points=dict(A=[0, 8], B=[12, 8], C=[12, 0], D=[0, 0], M=[6, 8], N=[0, 4]),
    shapes=[dict(pts=['A', 'B', 'C', 'D'], fill='none'),
            dict(pts=['M', 'N', 'C'], fill='teal', label='S(MNC) = 36'),
            dict(pts=['A', 'M', 'N'], fill='white', label='12'),
            dict(pts=['M', 'B', 'C'], fill='white', label='24'),
            dict(pts=['N', 'D', 'C'], fill='white', label='24')],
    show_points=['A', 'B', 'C', 'D', 'M', 'N'],
    formula='96 − 12 − 24 − 24 = 36 cm²',
    note='Mỗi phần trắng đều là tam giác vuông có cặp đáy - cao lộ sẵn — tính rất nhanh'),
    caption='Phần tô đậm khó tính thẳng thì đánh vu hồi từ phía các phần trắng'),

'DL:KSN5Q1.B47.M3': dict(archetype='fraction_split', params=dict(
    title='ĐẶT S NHỎ = 1 PHẦN — RỒI NHỚ ĐỔI VỀ cm² THẬT',
    shapes=[dict(parts=8, shaded=3, label='tô đậm 3/8 = 36 cm²', kind='bar')],
    note='1 phần = 96 : 8 = 12 cm² → 3 phần = 36 cm² · đừng dừng ở "3 phần"'),
    caption='Chiêu dời hình: xén mảnh nhô lấp chỗ hõm — hình bình hành 12 × 8 hóa chữ nhật 96'),

# ── B48 · Hình thang & hình ghép ──────────────────────────────────
'DL:KSN5Q1.B48.M1': dict(archetype='geo_shape', params=dict(
    title='HÌNH THANG: CỘNG HAI ĐÁY TRƯỚC',
    points=dict(D=[0, 0], C=[8, 0], B=[6, 6], A=[2, 6], H=[2, 0]),
    shapes=[dict(pts=['D', 'C', 'B', 'A'], fill='teal', label='S = 36 m²')],
    segments=[dict(**{'from': 'A', 'to': 'H'}, dashed=True, label='cao 6', dx=7)],
    edge_labels=[dict(**{'from': 'A', 'to': 'B'}, text='đáy bé 4', dy=5),
                 dict(**{'from': 'D', 'to': 'C'}, text='đáy lớn 8', dy=-5)],
    show_points=['A', 'B', 'C', 'D'],
    formula='(8 + 4) × 6 : 2 = 36 m²  ·  ngược: tổng đáy = 36 × 2 : 6 = 12',
    note='Đề không cho quan hệ giữa hai đáy thì KHÔNG tách riêng được — đủ là dừng'),
    caption='Cấu trúc chuẩn "cộng hai đáy trước" mới gánh nổi cả bài xuôi lẫn bài ngược'),

'DL:KSN5Q1.B48.M2': dict(archetype='geo_shape', params=dict(
    title='HAI ĐƯỜNG CHÉO CHIA HÌNH THANG THÀNH BỐN VÙNG',
    points=dict(D=[0, 0], C=[8, 0], B=[6, 6], A=[2, 6], O=[4, 4]),
    shapes=[dict(pts=['A', 'B', 'O'], fill='teal', label='trên 1p = 4'),
            dict(pts=['D', 'C', 'O'], fill='navy', label='dưới 4p = 16'),
            dict(pts=['A', 'D', 'O'], fill='gold', label='bên 2p = 8'),
            dict(pts=['B', 'C', 'O'], fill='gold', label='bên 2p = 8')],
    show_points=['A', 'B', 'C', 'D', 'O'],
    formula='9 phần = 36  →  1 phần = 4  ·  trên 1 · dưới 4 · bên 2 · 2',
    note='Hai tam giác BÊN luôn bằng nhau · trên : dưới = tỉ đáy LẶP HAI LẦN (1 : 4 chứ không phải 1 : 2)'),
    caption='Bốn vùng: bên bằng bên, còn trên và dưới ăn tỉ đáy bình phương'),

'DL:KSN5Q1.B48.M3': dict(archetype='geo_shape', params=dict(
    title='HÌNH CHỮ L — HAI CÁCH CHIA ĐỂ TỰ KIỂM',
    points=dict(A=[0, 6], B=[8, 6], C=[8, 2], D=[5, 2], E=[5, 0], F=[0, 0], P=[5, 6], Q=[0, 2]),
    shapes=[dict(pts=['A', 'B', 'C', 'D', 'E', 'F'], fill='teal', label='S = 42 cm²')],
    segments=[dict(**{'from': 'P', 'to': 'E'}, dashed=True, color='#C0392B'),
              dict(**{'from': 'Q', 'to': 'C'}, dashed=True, color='#F8B942')],
    show_points=['A', 'B', 'C', 'D', 'E', 'F'],
    formula='cách 1: 8 × 6 − 3 × 2 = 42   ·   cách 2: 5 × 6 + 3 × 4 = 42',
    note='Cắt một góc rồi ghép chỗ khác: DIỆN TÍCH giữ nguyên ✓ nhưng CHU VI thay đổi — hai đại lượng hai số phận'),
    caption='Hai cách chia cho cùng một đáp thì gần như chắc chắn đã đúng'),
}
