# -*- coding: utf-8 -*-
"""Lô A6 · Chương 6 (B21–B24): trung bình cộng — điểm cân · bù trừ · hơn kém TBC · gộp nhóm."""

SPEC = {
# ── B21 · Điểm cân & luật bù trừ ──────────────────────────────────
'DL:KSN5Q1.B21.M1': dict(archetype='level_bars', params=dict(
    title='TBC LÀ ĐIỂM CÂN — KHÔNG PHẢI SỐ ĐỨNG GIỮA DANH SÁCH',
    values=[22, 38, 31, 29, 35], labels=['ngày 1', 'ngày 2', 'ngày 3', 'ngày 4', 'ngày 5'],
    mean=31, mean_label='TBC 31',
    verdict='tổng 155 : 5 số = 31  ·  kiểm: 22 < 31 < 38 ✓',
    note='Cây cầu ngược: biết TBC thì tổng = TBC × n = 31 × 5 = 155'),
    caption='TBC luôn nằm giữa số bé nhất và số lớn nhất — đó là phép thử nhanh'),

'DL:KSN5Q1.B21.M2': dict(archetype='level_bars', params=dict(
    title='MẸO MỐC NHANH: CHỌN SỐ TRÒN LÀM MỐC RỒI ĐO PHẦN LỆCH',
    values=[97, 103, 101, 99], labels=['97', '103', '101', '99'],
    mean=100, mean_label='mốc 100',
    verdict='lệch −3  +3  +1  −1  →  tổng lệch 0  →  TBC = 100',
    note='Nếu tổng lệch khác 0: chia đều cho số số hạng rồi cộng vào mốc (52·47·55·50 → mốc 50 + 1 = 51)'),
    caption='Luật bù trừ: bên thừa bù đúng bên thiếu quanh điểm cân'),

'DL:KSN5Q1.B21.M3': dict(archetype='fence_posts', params=dict(
    title='DÃY CÁCH ĐỀU: TBC CHÍNH LÀ ĐIỂM GIỮA (ĐẦU + CUỐI) : 2',
    first=3, last=99, step=3, show=5, labels=['3', '…', '51', '…', '99'],
    highlight=[2], show_step=False,
    gap_note='chỉ dãy CÁCH ĐỀU mới có đặc quyền này',
    formula='(3 + 99) : 2 = 51  —  khỏi cộng cả 33 số hạng',
    note='Chiều ngược: TBC năm số lẻ liên tiếp là 27 → số giữa 27 → 23; 25; 27; 29; 31'),
    caption='Đặc quyền không cho mượn: dãy không cách đều thì phải cộng thật rồi chia'),

# ── B22 · Hơn – kém TBC ───────────────────────────────────────────
'DL:KSN5Q1.B22.M1': dict(archetype='ladder_steps', params=dict(
    title='NGÀY THỨ TƯ HƠN TBC CẢ BỐN NGÀY 9 CHIẾC',
    steps=[dict(text='TBC ba ngày cũ', sub='(22 + 31 + 25) : 3 = 26'),
           dict(text='CÂN NHÍCH lên', sub='26 + 9 : 3 = 29 = TBC bốn ngày'),
           dict(text='Ngày tư = TBC mới + 9', sub='29 + 9 = 38  ·  thử 116 : 4 = 29 ✓')],
    note='Phần hơn 9 được BA bạn cũ chia nhau gánh nên cân chỉ nhích 3'),
    caption='Cân nhích trước — cộng phần hơn sau, không được làm ngược'),

'DL:KSN5Q1.B22.M2': dict(archetype='balance_scale', params=dict(
    title='GÓP ĐÚNG BẰNG TBC CẢ NHÓM — CHIẾC CÂN ĐỨNG IM',
    left=dict(text='3 bạn cũ · TBC 24 viên', weight=1),
    right=dict(text='Dũng góp 24 viên', weight=1),
    verdict='Người mới đứng đúng điểm cân → TBC không đổi = 24',
    note='Thử: (72 + 24) : 4 = 24 ✓ — khỏi tính gì thêm'),
    caption='Cân thăng bằng: thêm người đúng mức trung bình thì không kéo lệch'),

'DL:KSN5Q1.B22.M3': dict(archetype='two_way_compare', params=dict(
    title='HAI ĐỀ CHỈ KHÁC VÀI CHỮ — HAI ĐÁP KHÁC HẲN', neutral=True,
    wrong=dict(head='hơn TBC CẢ BỐN ngày 9', steps=['cân nhích: 26 + 9 : 3 = 29'], result='ngày tư = 38'),
    right=dict(head='hơn TBC BA ngày đầu 9', steps=['mốc có sẵn: 26'], result='ngày tư = 35'),
    verdict='Gạch chân "TBC CỦA AI" rồi mới chọn đường'),
    caption='Kiểu A phải cân nhích · kiểu B cộng thẳng vào mốc có sẵn'),

# ── B23 · Thành viên đến – rời ────────────────────────────────────
'DL:KSN5Q1.B23.M1': dict(archetype='ladder_steps', params=dict(
    title='THÊM NGƯỜI VÀO NHÓM — BA NHỊP QUA CẦU TỔNG',
    steps=[dict(text='Tổng cũ', sub='4 bạn có 100 viên'),
           dict(text='Tổng mới', sub='100 + 40 = 140 viên'),
           dict(text='Chia QUÂN SỐ MỚI', sub='140 : 5 = 28 viên')],
    note='Nhớ đếm lại quân số: chia cho 5 chứ không phải 4'),
    caption='Ba nhịp: tổng cũ → tổng mới → chia số người mới'),

'DL:KSN5Q1.B23.M2': dict(archetype='two_way_compare', params=dict(
    title='BÀI NGƯỢC: BẠN MỚI MANG BAO NHIÊU VIÊN?', neutral=True,
    wrong=dict(head='TỔNG MỚI', steps=['TBC mới × số người mới', '28 × 5'], result='140 viên'),
    right=dict(head='TỔNG CŨ', steps=['TBC cũ × số người cũ', '25 × 4'], result='100 viên'),
    verdict='Bạn mới mang = 140 − 100 = 40 viên  ·  thử (100 + 40) : 5 = 28 ✓'),
    caption='Hai phép nhân dựng hai tổng, rồi trừ ra phần người mới mang'),

'DL:KSN5Q1.B23.M3': dict(archetype='grid_count', params=dict(
    title='BÀI NGƯỢC ĐỈNH CAO: TÌM SỐ BẠN CŨ',
    cols=4, rows=3, show_dims=False,
    fill=[[c, r] for r in range(3) for c in range(4)],
    fill_color='#F9B233',
    memo=['phần hơn = 40 − 28 = 12', 'mức kéo cân = 28 − 25 = 3', 'số bạn cũ = 12 : 3 = 4'],
    note='Phần thừa của người mới (đo từ cân MỚI) được chia đều cho các bạn cũ'),
    caption='12 viên thừa chia đều 3 viên mỗi bạn → đúng 4 bạn cũ'),

# ── B24 · Gộp nhóm khác cỡ ────────────────────────────────────────
'DL:KSN5Q1.B24.M1': dict(archetype='bar_diagram', params=dict(
    title='GỘP HAI NHÓM KHÁC CỠ — QUA CẦU TỔNG',
    bars=[dict(name='2 ngày đầu', units=2, label='26 × 2 = 52'),
          dict(name='4 ngày sau', units=4, label='32 × 4 = 128')],
    brace=dict(text='(52 + 128) : 6 ngày = 180 : 6 = 30 chiếc'),
    note='Kẻ bảng NHÓM · QUÂN SỐ · TỔNG rồi mới cộng — đừng cộng TBC với nhau'),
    caption='Nhân ngược ra tổng từng nhóm, cộng tổng, chia tổng quân số'),

'DL:KSN5Q1.B24.M2': dict(archetype='two_way_compare', params=dict(
    title='VÌ SAO KHÔNG ĐƯỢC CỘNG HAI TBC RỒI CHIA ĐÔI?',
    wrong=dict(head='CHIA ĐÔI HAI TBC', steps=['(26 + 32) : 2'], result='29 ✗'),
    right=dict(head='QUA CẦU TỔNG', steps=['(52 + 128) : 6'], result='30 ✓'),
    verdict='Nhóm 4 ngày đông gấp đôi nên kéo điểm cân về phía mình'),
    caption='Chỉ khi hai nhóm BẰNG cỡ thì chia đôi mới hợp lệ'),

'DL:KSN5Q1.B24.M3': dict(archetype='ladder_steps', params=dict(
    title='TRÙM HAI TẦNG: GỘP TỔNG TRƯỚC — KÉO CÂN SAU',
    steps=[dict(text='TẦNG 1 · gộp', sub='tổng sáu ngày = 30 × 6 = 180'),
           dict(text='TẦNG 2 · kéo cân', sub='TBC bảy ngày = 30 + 12 : 6 = 32'),
           dict(text='Chủ nhật', sub='32 + 12 = 44 chiếc')],
    note='Bài ngược cùng cầu: tổng cả 180 − 52 = 128 → TBC bốn ngày sau = 32'),
    caption='Hai tầng nối nhau — làm sai thứ tự là lệch ngay'),
}
