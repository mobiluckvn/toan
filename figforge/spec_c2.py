# -*- coding: utf-8 -*-
"""Lô A2 · Chương 2 (B5–B8): lập số · đếm bằng quy tắc nhân · dãy cách đều · đánh trang."""

SPEC = {
# ── B5 · Lập số từ bộ thẻ ─────────────────────────────────────────
'DL:KSN5Q1.B5.M1': dict(archetype='place_value_chart', params=dict(
    title='BỘ THẺ 0; 3; 5; 8 — LỚN NHẤT VÀ NHỎ NHẤT',
    headers=['nghìn', 'trăm', 'chục', 'đơn vị'], comma_after=None,
    rows=[dict(label='lớn nhất', cells=['8', '5', '3', '0'], color='#E6FAF5'),
          dict(label='nhỏ nhất', cells=['3', '0', '5', '8'], color='#FFF4DF')],
    note='Số nhỏ nhất KHÔNG phải 0358 — luật hàng đầu cấm số 0 dẫn đội, thẻ 3 phải ra trước'),
    caption='Tham lam từng hàng: lớn nhất xếp giảm dần · nhỏ nhất xếp tăng dần nhưng né số 0 ở đầu'),

'DL:KSN5Q1.B5.M2': dict(archetype='two_way_compare', params=dict(
    title='LẬP SỐ LỚN NHẤT CHIA HẾT CHO 5 — PHẢI SO ĐỦ HAI NHÁNH', neutral=True,
    wrong=dict(head='NHÁNH ĐUÔI 0', steps=['còn {3;5;8} xếp giảm'], result='8530'),
    right=dict(head='NHÁNH ĐUÔI 5', steps=['còn {0;3;8} xếp giảm'], result='8305'),
    verdict='So hai nhánh → chọn 8530'),
    caption='Chia hết cho 2 hay 5 thì chốt ĐUÔI trước — nhưng phải so đủ mọi nhánh mới kết luận'),

'DL:KSN5Q1.B5.M3': dict(archetype='ladder_steps', params=dict(
    title='ĐIỀU KIỆN KÉP: HỌ TỔNG TRƯỚC — HỌ TẬN CÙNG SAU',
    steps=[dict(text='TRẠM 1 · chọn bộ thẻ', sub='tổng 5 thẻ = 16 → bỏ thẻ 7 còn 9 ⋮ 9'),
           dict(text='TRẠM 2 · chốt đuôi', sub='số chẵn → đuôi ∈ {0; 2; 4}'),
           dict(text='XẾP GIẢM DẦN phần còn lại', sub='bộ {0;2;3;4} → số lớn nhất 4320')],
    note='Bài 5 micro 3 · làm ngược thứ tự là phải xếp lại từ đầu'),
    caption='Hai trạm nối tiếp — chọn bộ thẻ xong mới bàn tới đuôi'),

# ── B6 · Quy tắc nhân (dây chuyền toa tàu) ────────────────────────
'DL:KSN5Q1.B6.M1': dict(archetype='bar_diagram', params=dict(
    title='ĐẾM SỐ CÓ 3 CHỮ SỐ TỪ 0; 3; 5; 8 (ĐƯỢC LẶP)',
    bars=[dict(name='toa trăm', units=3, label='3 cách — bỏ số 0'),
          dict(name='toa chục', units=4, label='4 cách'),
          dict(name='toa đơn vị', units=4, label='4 cách')],
    brace=dict(text='3 × 4 × 4 = 48 số'),
    note='Toa đầu luôn phải bỏ thẻ 0 — bộ {1;2;3;4} không có số 0 nên được 4 × 4 × 4 = 64'),
    caption='Mỗi hàng là một toa tàu — số cách chọn của các toa NHÂN dọc dây chuyền'),

'DL:KSN5Q1.B6.M2': dict(archetype='bar_diagram', params=dict(
    title='CHỮ SỐ KHÁC NHAU — KHO THẺ VƠI DẦN',
    bars=[dict(name='toa trăm', units=3, label='3 (bỏ số 0)'),
          dict(name='toa chục', units=3, label='vơi 1, thả số 0 → 3'),
          dict(name='toa đơn vị', units=2, label='2')],
    brace=dict(text='3 × 3 × 2 = 18 số'),
    note='So với bài trước (48 số): thẻ dùng rồi không quay lại nên kho vơi dần'),
    caption='Thẻ 0 bị cấm ở toa đầu nhưng được trả tự do từ toa thứ hai'),

'DL:KSN5Q1.B6.M3': dict(archetype='bar_diagram', params=dict(
    title='ĐẾM SỐ CHẴN CÓ 3 CHỮ SỐ KHÁC NHAU TỪ 0; 3; 5; 8',
    bars=[dict(name='nhánh đuôi 0', units=6, label='3 × 2 = 6 số'),
          dict(name='nhánh đuôi 8', units=4, label='2 × 2 = 4 số')],
    brace=dict(text='hai nhánh KHÁC luật → đếm riêng rồi cộng: 6 + 4 = 10 số'),
    note='Nhánh đuôi 0 rộng hơn vì số 0 nằm ở đuôi thì toa trăm không bị mất thẻ nào'),
    caption='Chọn toa ràng buộc trước — nhánh khác luật thì tách riêng'),

# ── B7 · Dãy cách đều & đếm chia hết ──────────────────────────────
'DL:KSN5Q1.B7.M1': dict(archetype='fence_posts', params=dict(
    title='DÃY 3; 6; 9; …; 99 CÓ BAO NHIÊU SỐ HẠNG?',
    first=3, last=99, step=3, show=6, labels=['3', '6', '9', '…', '96', '99'], gap_at=3,
    gap_note='đếm KHOẢNG trước — cộng 1 ra CỌC',
    formula='(99 − 3) : 3 = 32 khoảng  →  32 + 1 = 33 số hạng',
    note='Cọc luôn nhiều hơn khoảng đúng 1 — đó chính là lý do có dấu +1'),
    caption='Hình ảnh hàng rào giải thích vì sao công thức có "+1"'),

'DL:KSN5Q1.B7.M2': dict(archetype='fence_posts', params=dict(
    title='TỪ 10 ĐẾN 100 CÓ BAO NHIÊU SỐ CHIA HẾT CHO 3?',
    first=12, last=99, step=3, show=6, labels=['12', '15', '18', '…', '96', '99'], gap_at=3,
    gap_note='đầu THẬT là 12 (10 và 11 trượt) · cuối THẬT là 99',
    formula='(99 − 12) : 3 + 1 = 30 số',
    note='Phải dò số đầu và số cuối THẬT SỰ thỏa mãn rồi mới áp công thức'),
    caption='"Từ a đến b" giữ hai đầu · "giữa a và b" thì đuổi hai đầu ra'),

'DL:KSN5Q1.B7.M3': dict(archetype='venn_two', params=dict(
    title='TỪ 1 ĐẾN 30: CHIA HẾT CHO 2 HOẶC CHO 3',
    left=dict(label='chia hết 2', count=15), right=dict(label='chia hết 3', count=10),
    both=dict(label='chia hết cả hai (⋮ 6)', count=5),
    result='15 + 10 − 5 = 20 số',
    note='Phần giao bị đếm hai lần nên phải trừ đi đúng một lần'),
    caption='Đếm "hoặc" = cộng hai nhóm rồi trừ phần giao'),

# ── B8 · Đánh trang & định vị chữ số ──────────────────────────────
'DL:KSN5Q1.B8.M1': dict(archetype='ladder_steps', params=dict(
    title='ĐÁNH SỐ TRANG SÁCH DÀY 256 TRANG',
    steps=[dict(text='Khu 1 · trang 1–9', sub='9 trang × 1 chữ số = 9'),
           dict(text='Khu 2 · trang 10–99', sub='90 trang × 2 = 180  (mốc vàng 189)'),
           dict(text='Khu 3 · trang 100–256', sub='157 trang × 3 = 471')],
    note='Tổng: 9 + 180 + 471 = 660 chữ số'),
    caption='Ba vùng · hai mốc vàng phải thuộc lòng: 9 và 189'),

'DL:KSN5Q1.B8.M2': dict(archetype='ladder_steps', params=dict(
    title='BÀI NGƯỢC: DÙNG 660 CHỮ SỐ — SÁCH DÀY BAO NHIÊU TRANG?',
    steps=[dict(text='TRỪ vùng đầu', sub='660 − 9 − 180 = 471'),
           dict(text='CHIA 3', sub='471 : 3 = 157 trang khu ba'),
           dict(text='CỘNG mốc 99', sub='99 + 157 = 256 trang')],
    note='Thử xuôi lại ra đúng 660 chữ số ✓ — bỏ nhịp nào cũng lệch'),
    caption='Ba nhịp bắt buộc: TRỪ — CHIA — CỘNG MỐC'),

'DL:KSN5Q1.B8.M3': dict(archetype='two_way_compare', params=dict(
    title='CHỮ SỐ THỨ N — HAI CỬA ĐỌC SỐ DƯ', neutral=True,
    wrong=dict(head='CỬA DƯ 0', steps=['15 − 9 = 6 · 6 : 2 = 3 dư 0'],
               result='chữ số CUỐI của số 12'),
    right=dict(head='CỬA DƯ r', steps=['200 − 189 = 11 · 11 : 3 = 3 dư 2'],
               result='chữ số thứ 2 của số 103'),
    verdict='Dư 0 → quay lại số vừa đi hết · dư r → bước r chữ số vào số kế'),
    caption='Trừ mốc vùng — chia có dư — rồi đọc dư đúng cửa'),
}
