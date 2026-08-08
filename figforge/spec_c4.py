# -*- coding: utf-8 -*-
"""Lô A4 · Chương 4 (B13–B16): tính nhanh · dãy phân số domino · rút gọn chéo · tìm X."""

SPEC = {
# ── B13 · Tính nhanh ──────────────────────────────────────────────
'DL:KSN5Q1.B13.M1': dict(archetype='pair_sum', params=dict(
    title='KÉO CẶP SỐ VÀNG VỀ GẦN NHAU: 0,25 × 7,3 × 4',
    seq=['0,25', '7,3', '4'],
    pair_label='cặp vàng 0,25 × 4 = 1',
    formula='(0,25 × 4) × 7,3 = 1 × 7,3 = 7,3',
    note='Kho cặp vàng: 0,25 × 4 = 1 · 0,125 × 8 = 1 · 2,5 × 4 = 10 · 1,25 × 8 = 10 · 12,5 × 8 = 100'),
    caption='Giao hoán – kết hợp cho phép kéo hai bạn vàng đứng cạnh nhau'),

'DL:KSN5Q1.B13.M2': dict(archetype='two_way_compare', params=dict(
    title='4,3 × 99 — TRỪ MẤY LẦN CHÍNH NÓ?',
    wrong=dict(head='TRỪ 99', steps=['430 − 99'], result='331 ✗'),
    right=dict(head='TRỪ MỘT LẦN 4,3', steps=['4,3 × 100 − 4,3 × 1'], result='430 − 4,3 = 425,7'),
    verdict='99 = 100 − 1 → chỉ trừ ĐÚNG MỘT LẦN chính nó'),
    caption='Số gần tròn: mượn cho tròn rồi trả lại đúng phần đã mượn'),

'DL:KSN5Q1.B13.M3': dict(archetype='area_split', params=dict(
    title='RÚT THỪA SỐ CHUNG: 6,8 × 3,7 + 3,7 × 3,2',
    height=dict(label='3,7', val=3.7),
    parts=[dict(label='6,8', val=6.8), dict(label='3,2', val=3.2)],
    formula='3,7 × (6,8 + 3,2) = 3,7 × 10 = 37',
    note='Ngoặc ra số tròn đẹp là CHỦ Ý người ra đề — nhìn 5 giây tìm tên quầy lặp lại'),
    caption='Hai mảnh cùng chiều cao ghép lại thành một hình chữ nhật lớn'),

# ── B14 · Dãy phân số domino ──────────────────────────────────────
'DL:KSN5Q1.B14.M1': dict(archetype='chain_cancel', params=dict(
    title='CÚ SẬP DOMINO: 1/(1×2) + 1/(2×3) + 1/(3×4)',
    terms=['1', '− 1/2', '+ 1/2', '− 1/3', '+ 1/3', '− 1/4'],
    cancel=[1, 2, 3, 4], survive=[0, 5],
    cancel_note='−1/2 gặp +1/2 · −1/3 gặp +1/3 → triệt sạch',
    result='chỉ còn 1 − 1/4 = 3/4',
    note='Cả hàng chín quân cũng vậy: 1 − 1/10 = 9/10'),
    caption='Tách 1/(n×(n+1)) = 1/n − 1/(n+1) rồi để domino tự đổ'),

'DL:KSN5Q1.B14.M2': dict(archetype='two_way_compare', params=dict(
    title='ĐỐI CHIẾU TỬ VỚI KHOẢNG CÁCH TRƯỚC KHI TÁCH', neutral=True,
    wrong=dict(head='TỬ = KHOẢNG CÁCH', steps=['2/(1×3) + 2/(3×5) + …', 'tách thẳng'],
               result='1 − 1/9 = 8/9'),
    right=dict(head='TỬ ≠ KHOẢNG CÁCH', steps=['1/(1×3) + 1/(3×5) + …', 'nhân hệ số 1/2'],
               result='8/9 × 1/2 = 4/9'),
    verdict='Mẫu cách nhau 2 mà tử là 1 → phải nhân thêm hệ số 1/2'),
    caption='Cùng một dãy, chỉ khác tử số — đáp án khác hẳn'),

'DL:KSN5Q1.B14.M3': dict(archetype='grid_count', params=dict(
    title='DÃY NỬA DẦN 1/2 + 1/4 + … + 1/64 = ?',
    cols=8, rows=8, show_dims=False,
    fill=[[c, r] for r in range(8) for c in range(8)][:63],
    fill_color='#1FCBAB',
    memo=['chiếc bánh chia 64 phần', 'ăn 63 phần', 'tổng = 1 − 1/64 = 63/64'],
    note='KHÔNG bằng 1 — góc trống 1/64 (ô trắng duy nhất) vẫn còn nguyên'),
    caption='Tổng = 1 trừ đi đúng mảnh cuối cùng vừa ăn'),

# ── B15 · Rút gọn chéo & hai họ tích ──────────────────────────────
'DL:KSN5Q1.B15.M1': dict(archetype='chain_cancel', params=dict(
    title='DÂY CHUYỀN RÚT CHÉO: 2/3 × 3/4 × 4/5',
    terms=['2', '3', '3', '4', '4', '5'],
    cancel=[1, 2, 3, 4], survive=[0, 5],
    cancel_note='mẫu anh trước gặp tử anh sau: 3–3 ✓  4–4 ✓',
    result='chỉ tử ĐẦU 2 và mẫu CUỐI 5 sống sót → 2/5',
    note='Phải DÒ DÂY xem có liền không rồi mới rút'),
    caption='Dây liền thì cả khúc giữa triệt tiêu, hai đầu sống sót'),

'DL:KSN5Q1.B15.M2': dict(archetype='two_way_compare', params=dict(
    title='HAI HỌ TÍCH — SOI DẤU TRƯỚC RỒI MỚI SẬP CHUYỀN', neutral=True,
    wrong=dict(head='HỌ DẤU TRỪ', steps=['(1 − 1/2)…(1 − 1/10)', '= 1/2 × 2/3 × … × 9/10'],
               result='= 1/10'),
    right=dict(head='HỌ DẤU CỘNG', steps=['(1 + 1/2)…(1 + 1/9)', '= 3/2 × 4/3 × … × 10/9'],
               result='= 10/2 = 5'),
    verdict='Họ trừ còn 1/n · họ cộng còn (n + 1)/2 — hai kết quả trái ngược'),
    caption='Chỉ khác một dấu mà một bên teo lại, một bên phình ra'),

'DL:KSN5Q1.B15.M3': dict(archetype='two_way_compare', params=dict(
    title='RÚT NGUYÊN CỤM — NHƯNG PHẢI KIỂM BỘ LÕI',
    wrong=dict(head='RÚT ẨU', steps=['(1+2+3) / (2+4+7)', 'số cuối 7 ≠ 2 × 3'],
               result='KHÔNG rút được'),
    right=dict(head='CÙNG BỘ LÕI', steps=['tử = 2 × (1 + 4 + 9)', 'mẫu = 6 × (1 + 4 + 9)'],
               result='= 2/6 = 1/3'),
    verdict='Chỉ rút được khi tử và mẫu cùng một bộ lõi'),
    caption='Đặt thừa số chung từng tầng, kiểm đủ mọi số hạng rồi mới rút'),

# ── B16 · Tìm X ───────────────────────────────────────────────────
'DL:KSN5Q1.B16.M1': dict(archetype='two_way_compare', params=dict(
    title='TÌM X: 12,6 − X = 4,8  (X ĐỨNG SAU DẤU TRỪ)',
    wrong=dict(head='CỘNG THEO QUÁN TÍNH', steps=['X = 12,6 + 4,8'], result='17,4 ✗'),
    right=dict(head='X LÀ SỐ TRỪ', steps=['X = 12,6 − 4,8'], result='7,8 ✓'),
    verdict='Thử lại: 12,6 − 7,8 = 4,8 ✓ — luôn thử là bắt được ngay'),
    caption='Nhìn VỊ TRÍ của X so với dấu trước khi gỡ'),

'DL:KSN5Q1.B16.M2': dict(archetype='ladder_steps', params=dict(
    title='BÓC VỎ CỦ HÀNH: X × 2 + 3,5 = 10,5',
    steps=[dict(text='Khoanh khối [X × 2]', sub='coi cả cụm là MỘT khối'),
           dict(text='Bóc vỏ CỘNG', sub='X × 2 = 10,5 − 3,5 = 7'),
           dict(text='Bóc vỏ NHÂN', sub='X = 7 : 2 = 3,5')],
    note='Mỗi lớp một dòng — bóc vỏ ngoài trước, đừng bóc nhảy cóc'),
    caption='Củ hành có mấy lớp thì bóc bấy nhiêu dòng'),

'DL:KSN5Q1.B16.M3': dict(archetype='two_way_compare', params=dict(
    title='X TRONG PHÉP CHIA CÓ DƯ — HAI GHẾ KHÁC NHAU', neutral=True,
    wrong=dict(head='GHẾ SỐ BỊ CHIA', steps=['X : 4 = 5 (dư 3)', 'thương thì NHÂN · dư thì CỘNG'],
               result='X = 4 × 5 + 3 = 23'),
    right=dict(head='GHẾ SỐ CHIA', steps=['39 : X = 7 (dư 4)', 'trừ dư → chia thương → kiểm'],
               result='X = 35 : 7 = 5'),
    verdict='Nhịp 3 bắt buộc: số chia 5 phải LỚN HƠN dư 4 ✓'),
    caption='Cùng một phép chia có dư nhưng X ngồi ghế nào thì làm cách ấy'),
}
