# -*- coding: utf-8 -*-
"""Lô A3 · Chương 3 (B9–B12): dấu hiệu chia hết mở rộng · chia có dư · vòng tận cùng · dãy cách đều."""

SPEC = {
# ── B9 · Ba ống kính & số hợp ─────────────────────────────────────
'DL:KSN5Q1.B9.M1': dict(archetype='place_value_chart', params=dict(
    title='SOI ĐUÔI SÂU DẦN: 4 · 25 SOI 2 CHỮ SỐ — 8 · 125 SOI 3 CHỮ SỐ',
    headers=['nghìn', 'trăm', 'chục', 'đơn vị'], comma_after=None,
    rows=[dict(label='1236', cells=['1', '2', '3', '6'], color='white', highlight=[2, 3]),
          dict(label='5104', cells=['5', '1', '0', '4'], color='white', highlight=[1, 2, 3])],
    note='1236: cụm 36 = 4 × 9 → ⋮ 4 ✓  ·  5104: cụm 104 = 8 × 13 → ⋮ 8 ✓'),
    caption='Ống kính càng sâu thì soi càng nhiều chữ số cuối — không cần nhìn cả số'),

'DL:KSN5Q1.B9.M2': dict(archetype='two_way_compare', params=dict(
    title='TÌM x ĐỂ 53x CHIA HẾT CHO 6 = 2 × 3', neutral=True,
    wrong=dict(head='CỬA TỔNG ⋮ 3', steps=['5 + 3 + x = 8 + x'], result='x ∈ {1; 4; 7}'),
    right=dict(head='CỬA CHẴN ⋮ 2', steps=['giữ lại x chẵn'], result='x = 4 → số 534'),
    verdict='Phải qua ĐỦ hai cửa — chỉ một cửa là chưa đủ'),
    caption='Số hợp không có dấu hiệu riêng: tháo thành cặp nguyên tố cùng nhau rồi khám từng cửa'),

'DL:KSN5Q1.B9.M3': dict(archetype='two_way_compare', params=dict(
    title='MẬT THƯ x47y CHIA HẾT CHO 45 = 9 × 5', neutral=True,
    wrong=dict(head='NHÁNH y = 0', steps=['x + 4 + 7 + 0 = x + 11 ⋮ 9'], result='x = 7 → 7470'),
    right=dict(head='NHÁNH y = 5', steps=['x + 4 + 7 + 5 = x + 16 ⋮ 9'], result='x = 2 → 2475'),
    verdict='Chốt y theo cửa tận cùng TRƯỚC — mỗi y mở một nhánh riêng'),
    caption='Hai ẩn thì đi hai nhánh, không được bỏ sót nhánh nào'),

# ── B10 · Chia có dư ──────────────────────────────────────────────
'DL:KSN5Q1.B10.M1': dict(archetype='grid_count', params=dict(
    title='47 : 5 = 9 DƯ 2  —  DƯ LUÔN BÉ HƠN SỐ CHIA',
    cols=5, rows=10,
    fill=[[c, r] for r in range(9) for c in range(5)] + [[0, 9], [1, 9]],
    fill_color='#1FC3A6', show_dims=False,
    row_labels=[dict(row=9, text='lẻ 2'), dict(row=8, text='túi 9'), dict(row=0, text='túi 1')],
    memo=['9 túi đầy × 5 = 45', 'còn lẻ 2 viên', 'dư lớn nhất = 5 − 1 = 4'],
    note='Nếu dư bằng 5 thì gom thêm được một túi nữa — nên dư luôn bé hơn số chia'),
    caption='Chín hàng đầy đủ 5 viên, hàng cuối chỉ có 2 viên lẻ'),

'DL:KSN5Q1.B10.M2': dict(archetype='two_way_compare', params=dict(
    title='VÁ SỐ 100 CHO CHIA HẾT CHO 9  (100 : 9 = 11 dư 1)', neutral=True,
    wrong=dict(head='CỬA BỚT — lùi vạch sau', steps=['bớt đúng SỐ DƯ = 1'], result='99 = 9 × 11'),
    right=dict(head='CỬA THÊM — tiến vạch trước', steps=['thêm PHẦN BÙ = 9 − 1 = 8'], result='108 = 9 × 12'),
    verdict='Hai đáp cộng lại đúng bằng số chia: 1 + 8 = 9'),
    caption='Thêm 1 không đủ — phải thêm đúng phần bù mới tới vạch kế tiếp'),

'DL:KSN5Q1.B10.M3': dict(archetype='fence_posts', params=dict(
    title='CHIA 3 DƯ 1 VÀ CHIA 5 DƯ 2 — DÒ NGHIỆM ĐẦU RỒI NHẢY BƯỚC',
    first=7, last=97, step=15, show=6, labels=['7', '22', '37', '…', '82', '97'], gap_at=3,
    gap_note='bước nhảy = 3 × 5 = 15',
    formula='nghiệm đầu 7  →  7; 22; 37; 52; 67; 82; 97',
    note='Số lớn nhất có hai chữ số là 97 · số kế 112 đã vượt'),
    caption='Dò trên dãy thưa hơn để tìm nghiệm đầu, rồi nhảy đều bằng tích hai số chia'),

# ── B11 · Vòng quay chữ số tận cùng ───────────────────────────────
'DL:KSN5Q1.B11.M1': dict(archetype='cycle_ring', params=dict(
    title='VÒNG QUAY CHỮ SỐ TẬN CÙNG KHI NHÂN MÃI SỐ 2',
    items=['2', '4', '8', '6'],
    rule=['nhóm ĐỨNG IM: 0 · 1 · 5 · 6', 'vòng ĐÔI: 4 (4-6) · 9 (9-1)', 'vòng BỐN: 2 · 3 · 7 · 8'],
    note='2 → 4 → 8 → 16 giữ đuôi 6 → 12 giữ đuôi 2: khép vòng, chu kỳ 4'),
    caption='Ba nhóm ghế: đứng im · vòng đôi · vòng bốn'),

'DL:KSN5Q1.B11.M2': dict(archetype='cycle_ring', params=dict(
    title='TÍCH 20 THỪA SỐ 2 CÓ ĐUÔI LÀ GÌ?',
    items=['2', '4', '8', '6'], pointer=4,
    rule=['20 : 4 = 5 dư 0', 'dư 0 → phần tử CUỐI', 'đuôi là 6'],
    note='Cửa dư r thì lấy phần tử thứ r · cửa dư 0 thì quay về phần tử cuối vòng'),
    caption='Chia số thừa số cho 4 rồi đọc số dư đúng hai cửa'),

'DL:KSN5Q1.B11.M3': dict(archetype='two_way_compare', params=dict(
    title='ĐUÔI CỦA TỔNG HAI TÍCH (10 thừa số 2) + (10 thừa số 3)', neutral=True,
    wrong=dict(head='CỤM SỐ 2', steps=['10 : 4 = 2 dư 2', 'vòng 2-4-8-6'], result='đuôi 4'),
    right=dict(head='CỤM SỐ 3', steps=['10 : 4 = 2 dư 2', 'vòng 3-9-7-1'], result='đuôi 9'),
    verdict='Gộp hai đuôi rồi LẠI lấy đuôi: 4 + 9 = 13 → đuôi 3'),
    caption='Tìm đuôi từng cụm trước, cộng xong vẫn phải lấy đuôi lần nữa'),

# ── B12 · Dãy cách đều & dãy lặp ──────────────────────────────────
'DL:KSN5Q1.B12.M1': dict(archetype='fence_posts', params=dict(
    title='DÃY 2; 5; 8; 11; … — SỐ HẠNG THỨ 10 LÀ SỐ NÀO?',
    first=2, last=29, step=3, show=6, labels=['2', '5', '8', '…', '26', '29'], gap_at=3,
    gap_note='từ số 1 đến số 10 chỉ có 9 bước nhảy',
    formula='số hạng thứ 10 = 2 + (10 − 1) × 3 = 29',
    note='Là (n − 1) chứ không phải n — vì số đầu tiên chưa nhảy bước nào'),
    caption='Cùng lý lẽ cọc và khoảng: đứng ở cọc thứ 10 thì đã đi 9 khoảng'),

'DL:KSN5Q1.B12.M2': dict(archetype='pair_sum', params=dict(
    title='TỔNG 3 + 6 + 9 + … + 99 — GHÉP CẶP',
    seq=['3', '6', '9', '…', '93', '96', '99'],
    pair_label='mỗi cặp = 102 · số số hạng = 33',
    formula='(3 + 99) × 33 : 2 = 102 × 33 : 2 = 1 683',
    note='Quên chia 2 là kết quả gấp đôi — một cặp ăn HAI số hạng'),
    caption='Ghép đầu với cuối: mọi cặp đều cho cùng một tổng'),

'DL:KSN5Q1.B12.M3': dict(archetype='cycle_ring', params=dict(
    title='DÃY LẶP 2; 0; 2; 6 — PHẦN TỬ THỨ 100 LÀ SỐ NÀO?',
    items=['2', '0', '2', '6'], pointer=4,
    rule=['chu kỳ 4', '100 : 4 = 25 dư 0', 'dư 0 → phần tử CUỐI = 6'],
    note='Đèn xanh - đỏ - vàng chu kỳ 3: bóng thứ 14 → 14 : 3 = 4 dư 2 → màu ĐỎ'),
    caption='Dãy lặp cũng đọc dư hai cửa như vòng tận cùng'),
}
