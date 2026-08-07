# -*- coding: utf-8 -*-
"""Lô A11 · Chương 11 (B41–B44): công việc chung · vòi nước – tỉ lệ nghịch · tính ngược – giả thiết tạm · khử thế – Ven – Dirichlet."""

SPEC = {
# ── B41 · Công việc chung ─────────────────────────────────────────
'DL:KSN5Q1.B41.M1': dict(archetype='fraction_split', params=dict(
    title='CẢ CÔNG VIỆC = 1 · NĂNG SUẤT MỖI NGÀY LÀ 1/t',
    shapes=[dict(parts=12, shaded=2, label='bác Ba 1/6 = 2/12', kind='bar'),
            dict(parts=12, shaded=1, label='chú Tư 1/12', kind='bar'),
            dict(parts=12, shaded=3, label='cùng nhau 3/12 = 1/4', kind='bar')],
    note='Chỉ NĂNG SUẤT biết cộng — ngày công thì không: 1 : 1/4 = 4 ngày (không phải 6 + 12)'),
    caption='Phản chứng: hai người mà lâu hơn một người làm một mình thì vô lý'),

'DL:KSN5Q1.B41.M2': dict(archetype='ladder_steps', params=dict(
    title='GHÉP ĐOẠN: CHUNG 2 NGÀY RỒI BÁC BA LÀM NỐT',
    steps=[dict(text='Khúc CHUNG 2 ngày', sub='2 × 1/4 = 1/2 công việc'),
           dict(text='Phần việc CÒN LẠI', sub='1 − 1/2 = 1/2'),
           dict(text='Khúc RIÊNG của bác Ba', sub='1/2 : 1/6 = 3 ngày  →  bác Ba làm tổng 5 ngày')],
    note='Chiều lật: riêng 3 ngày trước (3/6 = 1/2) → khúc chung còn 1/2 : 1/4 = 2 ngày'),
    caption='Cộng dồn phần việc từng đoạn cho đủ 1 rồi mới đọc số ngày'),

'DL:KSN5Q1.B41.M3': dict(archetype='ladder_steps', params=dict(
    title='LUÂN PHIÊN MỖI NGƯỜI MỘT GIỜ — BA NHỊP',
    steps=[dict(text='GÓI chu kỳ', sub='2 giờ (cô Năm + chú Sáu) = 1/4 + 1/6 = 5/12'),
           dict(text='NHÂN chu kỳ NGUYÊN', sub='2 chu kỳ = 4 giờ = 10/12  ·  còn 2/12 = 1/6'),
           dict(text='XÉT DƯ: ai cầm ca?', sub='giờ thứ 5 là cô Năm: 1/6 : 1/4 = 2/3 giờ = 40 phút')],
    note='Đổi chuẩn: 2,4 giờ = 2 giờ 24 phút (0,4 × 60) — không đọc là 2 giờ 4 phút'),
    caption='Không lấy 1 chia thẳng cho phần việc mỗi chu kỳ — phải đếm chu kỳ nguyên trước'),

# ── B42 · Vòi nước & tỉ lệ nghịch ─────────────────────────────────
'DL:KSN5Q1.B42.M1': dict(archetype='two_way_compare', params=dict(
    title='VÀO THÌ CỘNG — RA THÌ TRỪ', neutral=True,
    wrong=dict(head='HAI VÒI CÙNG VÀO', steps=['1/3 + 1/6 = 1/2'], result='đầy sau 2 giờ'),
    right=dict(head='VÒI VÀO + VÒI THÁO', steps=['1/3 − 1/6 = 1/6'], result='đầy sau 6 giờ'),
    verdict='Chuông soi: có tháo thì PHẢI chậm hơn — 6 > 2 ✓'),
    caption='Bể không nhận, mà bể mất — nên vòi tháo mang dấu trừ'),

'DL:KSN5Q1.B42.M2': dict(archetype='stack_compare', params=dict(
    title='BỂ CÓ SẴN 1/3 NƯỚC — CHỈ BƠM PHẦN THIẾU',
    cols=[dict(tag='lúc đầu', total=3, total_label='bể 1/3 đầy',
               parts=[dict(label='có sẵn 1/3', val=1, color='anchor'),
                      dict(label='phần thiếu 2/3', val=2, color='water')]),
          dict(tag='sau 2 giờ', total=3, total_label='bể đầy',
               parts=[dict(label='có sẵn 1/3', val=1, color='anchor'),
                      dict(label='vừa bơm 2/3', val=2, color='')])],
    anchor_label='chỉ bơm PHẦN THIẾU = 1 − 1/3 = 2/3',
    formula='2/3 : 1/3 = 2 giờ  ·  bể rò: 1/4 − 1/12 = 1/6 → 6 giờ',
    note='Nghi thức tóm tắt: MỨC ĐẦU · năng suất · phần cần bơm — rò là vòi tháo đội mũ'),
    caption='Đừng lấy cả bể chia năng suất khi bể đã có sẵn nước'),

'DL:KSN5Q1.B42.M3': dict(archetype='place_value_chart', params=dict(
    title='TỈ LỆ NGHỊCH — MỎ NEO LÀ TỔNG CÔNG',
    headers=['số người', 'số ngày', 'tổng công'], comma_after=None,
    rows=[dict(label='', cells=['6 người', '10 ngày', '60'], color='#E9F9F4', highlight=[2]),
          dict(label='', cells=['4 người', '15 ngày', '60'], color='#FFF6E2', highlight=[2]),
          dict(label='', cells=['3 máy', '6 giờ', '18'], color='white'),
          dict(label='', cells=['2 máy', '9 giờ', '18'], color='white')],
    note='Kiểm chiều: ÍT người thì NHIỀU ngày — 15 > 10 ✓ (nếu ra ngược là sai)'),
    caption='Người × ngày = số công không đổi — đổi quân số thì chia lại tổng công'),

# ── B43 · Tính ngược & giả thiết tạm ──────────────────────────────
'DL:KSN5Q1.B43.M1': dict(archetype='ladder_steps', params=dict(
    title='GỠ NGƯỢC TỪ SỐ CUỐI — ĐỌC ĐÚNG HỆ SỐ NGƯỢC',
    steps=[dict(text='Số cuối cùng', sub='còn 12 viên'),
           dict(text='Tầng "dùng 1/2" → nhân 2', sub='12 × 2 = 24'),
           dict(text='Tầng "dùng 1/3 CHỖ CÒN" → nhân 3/2', sub='vì sau tầng ấy CÒN 2/3')],
    note='Nhân 3 là lấy nhầm hệ số — con số đang cầm là phần CÒN, không phải phần dùng'),
    caption='Lưu đồ hai chiều: xuôi ghi từng tầng, ngược gỡ từ số cuối'),

'DL:KSN5Q1.B43.M2': dict(archetype='two_way_compare', params=dict(
    title='TÚI 24 VIÊN · ĂN 1/2 CÒN 12 — RỒI CHO ĐI', neutral=True,
    wrong=dict(head='CHO 1/3 CHỖ CÒN LẠI', steps=['1/3 của 12 = 4'], result='còn 8 viên'),
    right=dict(head='CHO 1/3 TỔNG', steps=['1/3 của 24 = 8'], result='còn 4 viên'),
    verdict='Hai chữ "còn lại" — hai thế giới: khoanh tròn trước khi đặt bút'),
    caption='Cùng một đề, chỉ khác hai chữ, đáp lệch nhau gấp đôi'),

'DL:KSN5Q1.B43.M3': dict(archetype='two_way_compare', params=dict(
    title='GIẢ THIẾT TẠM: 36 CON · 100 CHÂN', neutral=True,
    wrong=dict(head='GIẢ CẢ 36 LÀ GÀ', steps=['36 × 2 = 72 chân'], result='thiếu 28 chân'),
    right=dict(head='ĐỔI GÀ THÀNH CHÓ', steps=['mỗi lần đổi thêm 2 chân'], result='28 : 2 = 14 chó'),
    verdict='Gà = 36 − 14 = 22  ·  thử: 22 × 2 + 14 × 4 = 100 ✓'),
    caption='Giả kịch bản cực đoan — đo độ lệch — chia cho chênh mỗi suất'),

# ── B44 · Khử thế · Ven · Dirichlet ───────────────────────────────
'DL:KSN5Q1.B44.M1': dict(archetype='two_way_compare', params=dict(
    title='HAI HÓA ĐƠN — KHỬ HAY THẾ?', neutral=True,
    wrong=dict(head='KHỬ (hệ số khớp)', steps=['3 bút + 2 vở = 21', '3 bút + 5 vở = 30'],
               result='3 vở = 9 → vở 3 · bút 5'),
    right=dict(head='THẾ (đổi tiền)', steps=['1 táo = 2 cam', '3 táo + 4 cam = 10 cam'],
               result='cam 3 · táo 6'),
    verdict='Hệ số LỆCH thì ba nhịp: SO — NHÂN cả hóa đơn — TRỪ'),
    caption='Nhân phải nhân CẢ hóa đơn (mọi cột), không nhân mỗi một cột'),

'DL:KSN5Q1.B44.M2': dict(archetype='venn_three', params=dict(
    title='LỚP 30 BẠN: BƠI · CỜ · VẼ',
    sets=[dict(label='bơi', count=15), dict(label='cờ', count=12), dict(label='vẽ', count=10)],
    pairs=dict(ab=5, ac=4, bc=3), triple=2,
    outside=dict(label='không môn nào', count=3),
    result='15 + 12 + 10 − 5 − 4 − 3 + 2 = 27  →  30 − 27 = 3 bạn',
    note='Hai vòng thì đơn giản hơn: 25 + 20 − 10 = 35 → 40 − 35 = 5 bạn'),
    caption='Trừ ba giao đôi rồi CỘNG TRẢ giao ba đúng một lần'),

'DL:KSN5Q1.B44.M3': dict(archetype='two_way_compare', params=dict(
    title='TỦ TỐI: 5 TẤT ĐỎ · 4 XANH · 3 VÀNG — BỐC MẤY CHIẾC?', neutral=True,
    wrong=dict(head='ĐÔI CÙNG MÀU', steps=['xấu nhất: 3 chiếc 3 màu khác nhau'], result='3 + 1 = 4 chiếc'),
    right=dict(head='ĐÔI MÀU ĐỎ', steps=['xấu nhất: vét sạch xanh + vàng = 7'], result='7 + 2 = 9 chiếc'),
    verdict='Hai câu na ná — kịch bản xấu nhất khác hẳn nhau'),
    caption='Máy Dirichlet: dựng kịch bản XẤU NHẤT rồi cộng thêm cho chắc chắn'),
}
