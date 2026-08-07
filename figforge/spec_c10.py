# -*- coding: utf-8 -*-
"""Lô A10 · Chương 10 (B37–B40): phần trăm · hệ vốn – khuyến mại · tươi khô · nồng độ."""

SPEC = {
# ── B37 · Ba dạng % & cú lừa đổi gốc ──────────────────────────────
'DL:KSN5Q1.B37.M1': dict(archetype='place_value_chart', params=dict(
    title='BA THỨ TIẾNG CỦA MỘT LƯỢNG — MÁY DỊCH',
    headers=['phân số', 'thập phân', 'phần trăm'], comma_after=None,
    rows=[dict(label='', cells=['3/4', '0,75', '75%'], color='#E9F9F4'),
          dict(label='', cells=['1/5', '0,2', '20%'], color='white'),
          dict(label='', cells=['1/4', '0,25', '25%'], color='#E9F9F4'),
          dict(label='', cells=['1/8', '0,125', '12,5%'], color='white')],
    note='Cơ chế "trên 100": 25% của 240 000 = 240 000 : 4 = 60 000 đồng'),
    caption='Dịch được ba thứ tiếng thì mọi bài phần trăm đều tính nhẩm được'),

'DL:KSN5Q1.B37.M2': dict(archetype='two_way_compare', params=dict(
    title='CÚ LỪA ĐỔI GỐC: A HƠN B 25% THÌ B KÉM A MẤY %?',
    wrong=dict(head='TRẢ LỜI VỘI', steps=['thấy 25% liền đáp'], result='B kém A 25% ✗'),
    right=dict(head='LẮP SỐ ĐẸP', steps=['B = 100 → A = 125', 'chênh 25 so GỐC A'],
               result='25 : 125 = 20% ✓'),
    verdict='Chênh thì MỘT — gốc thì HAI: đổi gốc là đổi cả đáp'),
    caption='"Tăng LÊN 120%" khác hẳn "tăng THÊM 120%" — một chữ đổi cả bài'),

'DL:KSN5Q1.B37.M3': dict(archetype='ladder_steps', params=dict(
    title='GỐI ĐẦU NHÂN HỆ SỐ: TĂNG 10% RỒI GIẢM 10%',
    steps=[dict(text='Giá gốc 100', sub='mốc xuất phát'),
           dict(text='Tăng 10% → × 1,1', sub='100 → 110'),
           dict(text='Giảm 10% trên giá MỚI → × 0,9', sub='110 → 99  ·  hụt 1%')],
    note='Cạnh hình vuông tăng 10% thì diện tích × 1,1 × 1,1 = 1,21 → tăng 21%, không phải 20%'),
    caption='Không bao giờ cộng trừ phần trăm — phải nhân hệ số gối đầu'),

# ── B38 · Hệ vốn & khuyến mại ─────────────────────────────────────
'DL:KSN5Q1.B38.M1': dict(archetype='two_way_compare', params=dict(
    title='BÁN 240 000 · LÃI 20% SO VỐN — TÌM VỐN',
    wrong=dict(head='NHÂN 0,8', steps=['240 000 × 0,8'], result='192 000 ✗'),
    right=dict(head='CHIA 1,2', steps=['bán = 120% vốn', '240 000 : 1,2'], result='200 000 ✓'),
    verdict='× 0,8 là bớt 20% của GIÁ BÁN — không phải về vốn'),
    caption='Đi lên thì nhân, đi xuống phải CHIA — hai đường không thay nhau được'),

'DL:KSN5Q1.B38.M2': dict(archetype='two_way_compare', params=dict(
    title='CÙNG MỘT THƯƠNG VỤ — HAI HỆ QUY CHIẾU', neutral=True,
    wrong=dict(head='THEO VỐN', steps=['lãi 40 000 : vốn 200 000'], result='20%'),
    right=dict(head='THEO GIÁ BÁN', steps=['lãi 40 000 : bán 240 000'], result='1/6 ≈ 16,7%'),
    verdict='Gốc khác nhau nên số khác nhau — phải đọc kỹ "so với cái gì"'),
    caption='Giảm theo niêm yết thì gốc 100% chính là giá niêm yết'),

'DL:KSN5Q1.B38.M3': dict(archetype='place_value_chart', params=dict(
    title='MA TRẬN KHUYẾN MẠI — QUY VỀ HỆ SỐ',
    headers=['khuyến mại', 'hệ số phải trả', 'giảm thực'], comma_after=None,
    rows=[dict(label='', cells=['giảm 10% rồi 20%', '0,9 × 0,8 = 0,72', '28%'], color='#FDECE9',
               highlight=[2]),
          dict(label='', cells=['mua 4 tặng 1', '4/5 = 0,8', '20%'], color='white'),
          dict(label='', cells=['giảm 20%', '0,8', '20%'], color='#E9F9F4')],
    note='Giảm gối đầu KHÔNG phải 10 + 20 = 30% — nhân hệ số mới ra 28%'),
    caption='Mọi chiêu khuyến mại đều quy được về một hệ số phải trả'),

# ── B39 · Tươi – khô ──────────────────────────────────────────────
'DL:KSN5Q1.B39.M1': dict(archetype='stack_compare', params=dict(
    title='PHƠI NHO: NƯỚC BAY — CHẤT KHÔ Ở LẠI',
    cols=[dict(tag='nho TƯƠI', total=100, total_label='100 kg',
               parts=[dict(label='chất khô 10 kg', val=10, color='anchor'),
                      dict(label='nước 90 kg (90%)', val=90, color='water')]),
          dict(tag='nho KHÔ', total=12.5, total_label='12,5 kg',
               parts=[dict(label='chất khô 10 kg', val=10, color='anchor'),
                      dict(label='nước 2,5 kg (20%)', val=2.5, color='water')])],
    anchor_label='MỎ NEO: chất khô 10 kg không đổi',
    formula='chất khô 10 kg = 80% khối khô  →  khối khô = 10 : 0,8 = 12,5 kg',
    note='90% là của khối TƯƠI · 20% là của khối KHÔ — hai ông chủ khác nhau'),
    caption='Cây cầu duy nhất nối hai bờ tươi – khô là khối chất khô'),

'DL:KSN5Q1.B39.M2': dict(archetype='stack_compare', params=dict(
    title='CHIỀU NGƯỢC: MUỐN 15 kg NHO KHÔ THÌ PHƠI BAO NHIÊU NHO TƯƠI?',
    cols=[dict(tag='nho TƯƠI cần', total=120, total_label='120 kg',
               parts=[dict(label='chất khô 12 kg', val=12, color='anchor'),
                      dict(label='nước 108 kg (90%)', val=108, color='water')]),
          dict(tag='nho KHÔ thu', total=15, total_label='15 kg',
               parts=[dict(label='chất khô 12 kg', val=12, color='anchor'),
                      dict(label='nước 3 kg (20%)', val=3, color='water')])],
    anchor_label='đi ngược trên cùng cây cầu: chất khô 12 kg',
    formula='chất khô = 15 × 80% = 12 kg = 10% khối tươi  →  tươi = 120 kg',
    note='Ba câu hỏi thường gặp: còn bao nhiêu kg · bay đi bao nhiêu kg · còn bao nhiêu %'),
    caption='Cùng một cây cầu, chỉ đổi chiều đi'),

'DL:KSN5Q1.B39.M3': dict(archetype='stack_compare', params=dict(
    title='TRUYỀN THUYẾT DƯA HẤU: 99% → 98% MÀ MẤT NỬA QUẢ',
    cols=[dict(tag='TRƯỚC phơi', total=100, total_label='100 kg',
               parts=[dict(label='ruột khô 1 kg', val=1, color='anchor'),
                      dict(label='nước 99 kg (99%)', val=99, color='water')]),
          dict(tag='SAU phơi', total=50, total_label='50 kg',
               parts=[dict(label='ruột khô 1 kg', val=1, color='anchor'),
                      dict(label='nước 49 kg (98%)', val=49, color='water')])],
    anchor_label='ruột khô 1 kg — nhìn PHE CHẤT KHÔ, đừng nhìn phe nước',
    formula='phe khô: 1% → 2% tức GẤP ĐÔI tỉ lệ  →  khối lượng còn một nửa: 50 kg',
    note='Nước 99% → 96% thì phe khô 1% → 4%: quả dưa chỉ còn 25 kg'),
    caption='%nước nhích một li thì khối lượng đi một dặm'),

# ── B40 · Nồng độ ─────────────────────────────────────────────────
'DL:KSN5Q1.B40.M1': dict(archetype='place_value_chart', params=dict(
    title='CÂU HỎI VÀNG: CHẤT NÀO ĐỨNG IM?',
    headers=['biến cố', 'chất đứng im', 'chất thay đổi'], comma_after=None,
    rows=[dict(label='', cells=['pha thêm nước', 'ĐƯỜNG', 'nước · khối'], color='#E9F9F4'),
          dict(label='', cells=['cô cạn bớt nước', 'ĐƯỜNG', 'nước · khối'], color='#E9F9F4'),
          dict(label='', cells=['thêm đường', 'NƯỚC', 'đường · khối'], color='#FFF6E2',
               highlight=[1])],
    note='Nồng độ = đường : cả bình · bình 400 g loại 10% có 40 g đường'),
    caption='Mở mọi biến cố bằng câu hỏi vàng — ai đứng im người ấy làm mỏ neo'),

'DL:KSN5Q1.B40.M2': dict(archetype='stack_compare', params=dict(
    title='THÊM NƯỚC ĐỂ BÌNH 400 g LOẠI 10% THÀNH LOẠI 8%',
    cols=[dict(tag='TRƯỚC', total=400, total_label='400 g · 10%',
               parts=[dict(label='đường 40 g', val=40, color='anchor'),
                      dict(label='nước 360 g', val=360, color='water')]),
          dict(tag='SAU', total=500, total_label='500 g · 8%',
               parts=[dict(label='đường 40 g', val=40, color='anchor'),
                      dict(label='nước 460 g', val=460, color='water')])],
    anchor_label='thêm nước → ĐƯỜNG cầm neo: 40 g',
    formula='40 g = 8% khối mới  →  khối mới = 500 g  →  thêm 100 g nước',
    note='Thêm đường thì đổi neo: NƯỚC 360 g = 80% khối mới → khối mới 450 g → thêm 50 g đường'),
    caption='Khối mới = mỏ neo : tỉ lệ mới — công thức chung cho mọi ca pha chế'),

'DL:KSN5Q1.B40.M3': dict(archetype='balance_scale', params=dict(
    title='TRỘN HAI BÌNH: MỖI GAM MỘT LÁ PHIẾU',
    left=dict(text='200 g loại 5% → 10 g đường', weight=2),
    right=dict(text='300 g loại 10% → 30 g đường', weight=3),
    verdict='40 g đường : 500 g = 8%  —  KHÔNG phải 7,5%',
    note='Bình nặng kéo điểm cân về phía mình — đúng luật đòn gánh lệch của bài 24'),
    caption='Nồng độ hỗn hợp = tổng đường : tổng khối, không phải trung bình hai nồng độ'),
}
