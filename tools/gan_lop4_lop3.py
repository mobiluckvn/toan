# -*- coding: utf-8 -*-
"""
ĐƯỜNG LÙI · lớp 4 → lớp 3 — dựng `data/lop4_gan_lop3.json`.

    python3 tools/gan_lop4_lop3.py

Bé học bài lớp 4 mà đuối thì phải có lối về luyện lại gốc ở lớp 3, chứ không bỏ dở.
Chuẩn (mục 4) đòi **đủ mọi bài, kể cả dòng `khong`** — bỏ trống thì không phân biệt
được "chưa xét" với "đã xét và kết luận là không có".

BỐN CĂN CỨ (lớp 3 chỉ có ba — dòng thứ tư sinh ra từ chính quyển này):

    sach     sách chỉ ĐÍCH DANH "Lớp 3, ở Bài n" và mô tả khớp bài ấy
    sachSua  sách chỉ đích danh MỘT bài, nhưng mô tả lại là bài KHÁC → đã sửa tay
    chuDe    sách chỉ nhắc chủ đề; ghép theo tên bài — đã soát tay từng dòng
    khong    lớp 3 không có bài cùng chủ đề — cố ghép là chỉ đường sai

⚠ **`Bài n` TRẦN trong HẠT MẦM là bài LỚP 4, không phải lớp 3.** Chỉ những số nằm
trong câu có nêu "Lớp 3" mới là đích thật. Mẫu bắt mọi `Bài n` cho ra 32/44 dòng
"đích danh" — 18 trong số đó trỏ ngược vào chính lớp 4, và bài 37 trỏ ra "Bài 36"
trong khi lớp 3 chỉ có 34 bài. Máy tự dò được **14 dòng**; 30 dòng còn lại soát tay.

⚠ **Một chỗ sách trỏ sai, đã sửa** (dòng `sachSua`): bài 8 ghi "Lớp 3, ở Bài 8, con
đếm số chứa một chữ số bằng liệt kê chăm chỉ" — nhưng Bài 8 lớp 3 là "GẤP LÊN —
GIẢM ĐI NHIỀU LẦN", còn việc "đếm số bằng liệt kê có thứ tự" nằm ở **Bài 4**. Theo
MÔ TẢ chứ không theo con số, vì bé bấm nút là đi thẳng tới bài ấy.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop4_tho.json')
IDX3 = os.path.join(GOC_KHO, 'data', 'lop3', 'index.json')
RA = os.path.join(GOC_KHO, 'data', 'lop4_gan_lop3.json')

MA3 = 'DL:KSN3.B{:02}'
MA4 = 'DL:KSN4.B{:02}'

# ── Soát tay: bài lớp 4 → bài lớp 3, kèm LÝ DO. Chỉ ghi những dòng máy không tự
#    dò được, cộng một dòng sửa lại chỗ sách trỏ nhầm.
TAY = {
    8:  (['sachSua'], [4],      'sách ghi "Lớp 3, ở Bài 8" nhưng mô tả "đếm số bằng '
                                'liệt kê chăm chỉ" — đó là Bài 4 (Đếm số & đếm trang); '
                                'Bài 8 lớp 3 là gấp lên - giảm đi'),
    3:  (['chuDe'], [2, 8],     'xóa chữ số là chiều ngược của thêm chữ số (B02); '
                                'xóa số 0 tận cùng = giảm đi 10 lần (B08)'),
    10: (['chuDe'], [6],        'dấu hiệu chia hết là mới ở lớp 4; gốc gần nhất là '
                                'phép chia có dư "chính danh" — dư 0 tức chia hết'),
    12: (['chuDe'], [5],        'đoán chữ số tận cùng của tích dựa trên phép nhân '
                                'ra ngoài bảng'),
    17: (['chuDe'], [18, 19],   'so vượt - hụt quanh một mức là "hơn mấy đơn vị" (B18) '
                                'và "thêm bớt để bằng nhau" (B19)'),
    18: (['chuDe'], [17],       'thêm người vào nhóm rồi tính lại trung bình là bài '
                                'hai bước tính'),
    20: (['chuDe'], [27, 17],   'tổng trốn trong CHU VI (B27) và trong bài hai bước (B17)'),
    21: (['chuDe'], [19, 18],   'hiệu trốn trong "thêm bớt để bằng nhau" (B19) và '
                                '"hơn mấy đơn vị" (B18)'),
    22: (['chuDe'], [20],       'tổng và hiệu cùng biến theo thời gian — gốc là toán '
                                'tuổi hai gia đình'),
    23: (['chuDe'], [18, 9],    'tỉ số "gấp mấy lần" (B18) và "một phần mấy của một '
                                'số" (B09) là hai gốc của sơ đồ phần'),
    24: (['chuDe'], [18, 9],    'cùng gốc với B23, thêm bước lột tỉ ẩn'),
    25: (['chuDe'], [18, 9],    'cùng gốc với B23, đổi tổng thành hiệu'),
    26: (['chuDe'], [18],       'ba số một sơ đồ vẫn quy về "gấp mấy lần"'),
    27: (['chuDe'], [20],       'toán tuổi hai gia đình là bài tuổi đầu tiên của bé'),
    28: (['chuDe'], [21],       'làm chung việc = rút về đơn vị, chỉ đổi "giá một gói" '
                                'thành "phần việc một giờ"'),
    29: (['chuDe'], [22],       'tính ngược từ cuối chính là "đi lùi nhiều trạm"'),
    30: (['chuDe'], [23],       'giả thiết tạm "giả sử tất cả là gà" là bài gà - chó'),
    31: (['chuDe'], [26],       'khử và thế là "trò chơi thay thế" lên trình'),
    32: (['chuDe'], [25],       'sơ đồ Ven hai vòng — cùng công cụ, thêm chuồng thỏ'),
    33: (['chuDe'], [9],        'so sánh phân số nối tiếp "tìm một phần mấy của một số"'),
    34: (['chuDe'], [9],        'tìm phân số của một số là chính bài B09 mở rộng tử số'),
    35: (['chuDe'], [12, 9],    'dãy phân số có quy luật — gốc là dãy hai tầng (B12) '
                                'và phân số (B09)'),
    36: (['chuDe'], [19],       'đại lượng bất biến: cùng thêm vào hai số thì hiệu '
                                'đứng im — gốc là "thêm bớt để bằng nhau"'),
    37: (['chuDe'], [9],        'lãi vốn - bay hơi đều là "phân số của một đại lượng"; '
                                'sách nhắc "Bài 36" là bài LỚP 4, không phải lớp 3'),
    38: (['chuDe'], [27, 30],   'chu vi có công thức (B27) và diện tích tấm thảm ô '
                                'vuông (B30)'),
    39: (['chuDe'], [28, 30],   'nới sân - thu sân là "chu vi biến hình" (B28) áp cho '
                                'diện tích (B30)'),
    40: (['chuDe'], [29],       'hình tròn đã giải phẫu ở B29; góc và đường cao là mới'),
    41: (['chuDe'], [31],       'đếm khối theo tầng — cùng tên, cùng cách làm'),
    42: (['chuDe'], [21],       'sách nhắc "Bài 9 con từng rút về đơn vị" nhưng rút về '
                                'đơn vị là Bài 21 lớp 3; theo mô tả, không theo số'),
    43: (['khong'], [],         'đuổi kịp - gặp nhau: lớp 3 không có bài chuyển động nào'),
    44: (['chuDe'], [32],       'góc hai kim đồng hồ dựa trên mặt đồng hồ đã học ở '
                                '"xem giờ đến từng phút"'),
}


def lop3_tu_hat_mam(hm):
    """Chỉ lấy 'Bài n' nằm trong CÂU có nêu 'Lớp 3'. Nở cả dải 'Bài 10-11'."""
    ra = []
    for cau in re.split(r'(?<=[.!?])\s+', hm):
        if not re.search(r'\bLớp 3\b', cau):
            continue
        for m in re.finditer(r'Bài (\d+)\s*(?:-\s*(\d+))?', cau):
            a = int(m.group(1))
            ra.append(a)
            if m.group(2):
                ra.extend(range(a + 1, int(m.group(2)) + 1))
    return sorted(set(ra))


def main():
    tho = json.load(open(THO, encoding='utf-8'))
    ten3 = {x['so']: x['ten'] for x in json.load(open(IDX3, encoding='utf-8'))}

    gan, loi = {}, []
    for b in tho['bai']:
        so = b['so']
        if so in TAY:
            can, ve, vi_sao = TAY[so][0][0], TAY[so][1], TAY[so][2]
        else:
            ve = lop3_tu_hat_mam(b['hatMam'])
            can, vi_sao = ('sach', 'sách chỉ đích danh trong HẠT MẦM NĂM NGOÁI') \
                if ve else ('khong', 'chưa xét')
        xau = [x for x in ve if x not in ten3]
        if xau:
            loi.append(f'bài {so}: trỏ về bài lớp 3 không có thật {xau}')
        if can != 'khong' and not ve:
            loi.append(f'bài {so}: căn cứ {can} mà danh sách đích rỗng')
        if can == 'khong' and ve:
            loi.append(f'bài {so}: căn cứ khong mà lại có đích {ve}')
        gan[MA4.format(so)] = {
            've': [MA3.format(x) for x in ve],
            'ten': [ten3.get(x, '') for x in ve],
            'canCu': can, 'lopDuoi': 3, 'viSao': vi_sao,
        }

    if len(gan) != 44:
        loi.append(f'{len(gan)} dòng, phải đủ 44 bài')

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump({'_doc': 'Đường lùi lớp 4 → lớp 3. Đủ 44 dòng, kể cả dòng khong.',
                   'tuLop': 'lop4', 'veLop': 'lop3', 'gan': gan},
                  f, ensure_ascii=False, indent=1)

    dem = {}
    for v in gan.values():
        dem[v['canCu']] = dem.get(v['canCu'], 0) + 1
    co = sum(1 for v in gan.values() if v['ve'])
    print(f'đã ghi {RA}')
    print(f'  {len(gan)} dòng · {co} bài có đích · căn cứ: {dem}')
    if loi:
        print(f'  ⚠ {len(loi)} chỗ lệch:')
        for x in loi:
            print('     ·', x)
        raise SystemExit(1)
    print('  ✓ chốt: đủ 44 dòng · mọi đích có thật · căn cứ khớp danh sách đích')


if __name__ == '__main__':
    main()
