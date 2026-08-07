# -*- coding: utf-8 -*-
"""Lô A1 · Chương 1 (B1–B4): hình MIỀN có số liệu thật, lấy nguyên từ ca mẫu trong sách."""

SPEC = {
# ── B1 · Bản đồ các hàng ──────────────────────────────────────────
'DL:KSN5Q1.B1.M1': dict(archetype='place_value_chart', params=dict(
    title='SỐ 2,73 TÁCH THÀNH TỔNG GIÁ TRỊ CÁC HÀNG',
    headers=['chục', 'đơn vị', 'phần mười', 'phần trăm'], comma_after=1,
    rows=[dict(label='2,73', cells=['', '2', '7', '3'], color='white'),
          dict(label='giá trị', cells=['', '2', '0,7', '0,03'], color='#E9F9F4')],
    note='2,73 = 2 + 0,7 + 0,03 — mỗi chữ số đáng bao nhiêu là do HÀNG quyết định'),
    caption='Ca lõi của bài: chữ số đứng ở hàng nào thì mang giá trị của hàng đó'),

'DL:KSN5Q1.B1.M2': dict(archetype='place_value_chart', params=dict(
    title='CÙNG CHỮ SỐ 5 — KHÁC HÀNG THÌ KHÁC GIÁ TRỊ',
    headers=['chục', 'đơn vị', 'phần mười', 'phần trăm'], comma_after=1,
    rows=[dict(label='3,52', cells=['', '3', '5', '2'], color='white'),
          dict(label='35,2', cells=['3', '5', '2', ''], color='#FFF6E2')],
    shift=dict(steps=1, dir='<', label='cách nhau 1 hàng → gấp 10 lần'),
    note='Trong 3,52 chữ số 5 đáng 0,5 · trong 35,2 chữ số 5 đáng 5'),
    caption='Mỗi bậc hàng là một lần gấp 10 — cách 3 bậc là gấp 1000'),

'DL:KSN5Q1.B1.M3': dict(archetype='bar_diagram', params=dict(
    title='ab = 4 × (a + b)  →  DỌN CÂN CÒN  b = 2a',
    bars=[dict(name='chữ số a', units=1, label='a'),
          dict(name='chữ số b', units=2, label='b = 2a')],
    brace=dict(text='10a + b = 4a + 4b → 6a = 3b → b gấp đôi a'),
    note='Điểm danh a = 1, 2, 3, 4 → các số 12, 24, 36, 48'),
    caption='Sơ đồ đoạn thẳng cho thấy b luôn dài gấp đôi a'),

# ── B2 · Thêm – xóa chữ số, công tắc dấu phẩy ─────────────────────
'DL:KSN5Q1.B2.M1': dict(archetype='bar_diagram', params=dict(
    title='VIẾT THÊM 2 VÀO BÊN PHẢI SỐ 47',
    bars=[dict(name='số cũ 47', units=1, label='47'),
          dict(name='số mới 472', units=10, label='47 × 10 + 2')],
    brace=dict(text='mức tăng = 9 × 47 + 2 = 425'),
    note='Thêm chữ số bên PHẢI: cả số cũ bị đẩy lên một hàng — gấp 10 rồi cộng chữ số mới'),
    caption='Số cũ chiếm 1 ô, số mới chiếm 10 ô — phần dôi ra chính là 9 lần số cũ'),

'DL:KSN5Q1.B2.M2': dict(archetype='place_value_chart', params=dict(
    title='BỎ DẤU PHẨY CỦA 3,45 — GẤP 100 LẦN, KHÔNG PHẢI 10',
    headers=['trăm', 'chục', 'đơn vị', 'phần mười', 'phần trăm'], comma_after=2,
    rows=[dict(label='3,45', cells=['', '', '3', '4', '5'], color='white'),
          dict(label='345', cells=['3', '4', '5', '', ''], color='#FFF6E2')],
    shift=dict(steps=2, dir='<', label='sau phẩy có 2 chữ số → dịch 2 bậc → gấp 100'),
    note='Đếm số chữ số SAU dấu phẩy trước khi trả lời'),
    caption='Bỏ phẩy là kéo cả số lên mấy bậc bằng số chữ số phần thập phân'),

'DL:KSN5Q1.B2.M3': dict(archetype='bar_diagram', params=dict(
    title='BỎ PHẨY 1 CHỮ SỐ → TĂNG THÊM 32,4 ĐƠN VỊ',
    bars=[dict(name='số cũ', units=1, label='số cũ = ?'),
          dict(name='số mới', units=10, label='gấp 10 lần')],
    brace=dict(text='phần tăng = 9 lần số cũ = 32,4 → số cũ = 32,4 : 9 = 3,6'),
    note='Thử lại: 36 − 3,6 = 32,4 ✓  ·  bỏ phẩy 2 chữ số thì chia cho 99'),
    caption='Chìa khóa của bài ngược: phần tăng luôn là 9 lần (hoặc 99 lần) số cũ'),

# ── B3 · Số và bóng gương ─────────────────────────────────────────
'DL:KSN5Q1.B3.M1': dict(archetype='bar_diagram', params=dict(
    title='35 + 53 = 11 × (3 + 5)',
    bars=[dict(name='tổng 88', units=8, label='11 × 8 = 88')],
    brace=dict(text='mỗi ô đáng 11 — có đúng (a + b) = 8 ô'),
    note='Tổng của số và bóng gương LUÔN chia hết cho 11 · hiệu luôn chia hết cho 9'),
    caption='Tổng ăn 11, hiệu ăn 9 — hai định luật soi gương'),

'DL:KSN5Q1.B3.M2': dict(archetype='two_way_compare', params=dict(
    title='TÌM SỐ CÓ TỔNG VỚI BÓNG GƯƠNG BẰNG 66',
    wrong=dict(head='QUÊN SOI GƯƠNG VỠ', steps=['nhận cả số 60'], result='6 đáp án'),
    right=dict(head='LOẠI SỐ TẬN CÙNG 0', steps=['60 soi ra 06 = 6'], result='5 đáp án'),
    verdict='15 · 24 · 33 · 42 · 51 — số 60 bị loại'),
    caption='Gương vỡ: số tận cùng bằng 0 soi ngược không còn là số hai chữ số'),

'DL:KSN5Q1.B3.M3': dict(archetype='place_value_chart', params=dict(
    title='ĐỔI CHỖ CHỮ SỐ: 18 → 81',
    headers=['chục', 'đơn vị'], comma_after=None,
    rows=[dict(label='18', cells=['1', '8'], color='white'),
          dict(label='81', cells=['8', '1'], color='#FFF6E2')],
    note='Tổng chữ số vẫn 9 → chia hết cho 9 ✓  ·  nhưng tận cùng đổi từ 8 sang 1 → hết chia hết cho 2'),
    caption='Họ TỔNG bình an khi đổi chỗ — họ TẬN CÙNG phải khám lại'),

# ── B4 · Thang máy dấu phẩy & vụ án quên phẩy ────────────────────
'DL:KSN5Q1.B4.M1': dict(archetype='place_value_chart', params=dict(
    title='THANG MÁY DẤU PHẨY: 3,45 × 10 VÀ × 100',
    headers=['trăm', 'chục', 'đơn vị', 'phần mười', 'phần trăm'], comma_after=2,
    rows=[dict(label='3,45', cells=['', '', '3', '4', '5'], color='white'),
          dict(label='× 10', cells=['', '3', '4', '5', ''], color='#E9F9F4'),
          dict(label='× 100', cells=['3', '4', '5', '', ''], color='#FFF6E2')],
    shift=dict(steps=2, dir='<', label='nhân 100 → phẩy đi sang phải 2 bậc'),
    note='Chia thì phẩy đi ngược lại: 62,7 : 100 = 0,627 — thiếu bậc thì mượn số 0 làm bậc đệm'),
    caption='Đếm bậc trước, nhân chia sau'),

'DL:KSN5Q1.B4.M2': dict(archetype='bar_diagram', params=dict(
    title='QUÊN PHẨY KHI CỘNG → TỔNG TĂNG 76,5',
    bars=[dict(name='số hạng thật', units=1, label='8,5'),
          dict(name='số hạng bị phình', units=10, label='85')],
    brace=dict(text='phần tăng = 9 lần số hạng = 76,5 → số hạng = 76,5 : 9 = 8,5'),
    note='Dấu vân tay của thủ phạm: chia cho 9 (một chữ số thập phân) hoặc 99 (hai chữ số)'),
    caption='Cùng một dấu vân tay 9 lần như bài bỏ phẩy'),

'DL:KSN5Q1.B4.M3': dict(archetype='two_way_compare', params=dict(
    title='QUÊN PHẨY Ở ĐÂU THÌ HIỆU ĐỔI CHIỀU NẤY',
    wrong=dict(head='QUÊN Ở SỐ TRỪ', steps=['6,3 phình thành 63'], result='hiệu GIẢM 56,7'),
    right=dict(head='QUÊN Ở SỐ BỊ TRỪ', steps=['số bị trừ phình 10 lần'], result='hiệu TĂNG'),
    verdict='Hiệu tăng 74,7 → số bị trừ thật = 74,7 : 9 = 8,3'),
    caption='Hai chiều ngược nhau — đọc kỹ quên phẩy ở số nào'),
}
