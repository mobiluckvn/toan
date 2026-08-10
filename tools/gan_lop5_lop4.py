# -*- coding: utf-8 -*-
"""
ĐƯỜNG LÙI · lớp 5 → lớp 4 — khai bảng và GẮN thẳng vào 168 bài lớp 5.

    python3 tools/gan_lop5_lop4.py

Bé giải không nổi bài lớp 5 thì có lối về đúng bài lớp 4 cùng chủ đề, thay vì làm
lại bài khó thêm một lượt. Đây là cùng một cơ chế đã chạy cho lớp 3 → lớp 2, nay
nối thêm hai nấc: **lớp 5 → lớp 4 → lớp 3**.

KHÁC LỚP 3 Ở HAI CHỖ:

1. **Lớp 5 không có "HẠT MẦM NĂM NGOÁI".** Quyển 1 lớp 5 soạn trước lớp 4 nên
   không hề trỏ về đâu cả — máy không dò được dòng nào. Cả 56 bài đều là `chuDe`,
   ghép tay theo tên bài, và mỗi dòng ghi rõ lý do ở `viSao`.

2. **Lớp 5 chia MICRO.** Một bài sách (`LESSON:KSN5Q1.B41`) tách thành 3 micro
   (`.M1 .M2 .M3`), mà bé học và trượt ở mức MICRO. Nên bảng khai theo bài sách rồi
   rải xuống cả ba micro của bài ấy — trượt micro nào cũng thấy đúng lối về.

3. **Lớp 5 không dựng qua `khuon_chung.py`**, tệp bài đã nằm sẵn trên đĩa. Nên công
   cụ này ghi thẳng trường `duongLui` vào tệp, và ghi vào **CẢ HAI** nơi:
   `data/lessons/` và `web/public/content/lessons/` — với Quyển 1 lớp 5 hai nơi ấy
   phải giống hệt nhau (khác với lớp 2/3/4, nơi bản gốc và bản dựng cố ý khác nhau).
   Chạy lại nhiều lần cho cùng kết quả: trường cũ bị thay, không cộng dồn.
"""
import json, os

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(GOC_KHO, 'data', 'MANIFEST_Q1.json')
IDX4 = os.path.join(GOC_KHO, 'data', 'lop4', 'index.json')
RA = os.path.join(GOC_KHO, 'data', 'lop5_gan_lop4.json')
NOI = [os.path.join(GOC_KHO, 'data', 'lessons'),
       os.path.join(GOC_KHO, 'web', 'public', 'content', 'lessons')]

MA4 = 'DL:KSN4.B{:02}'

# ── Soát tay: bài sách lớp 5 → bài lớp 4, kèm LÝ DO. Không dòng nào `khong`: sách
#    lớp 4 phủ đủ mọi chủ đề của Quyển 1 lớp 5, chỉ khác độ sâu.
TAY = {
    1:  ([1],      'cấu tạo số theo hàng - lớp, gốc là "số khổng lồ lớp triệu"'),
    2:  ([2, 3],   'thêm chữ số (B02) và xóa chữ số (B03) — dấu phẩy là tầng trên'),
    3:  ([4],      'số viết ngược & định luật họ 9 - 11 — đúng bài tráo thẻ số'),
    4:  ([3],      'thang máy dấu phẩy nối tiếp thang máy ×10'),
    5:  ([4],      'lập số lớn nhất - bé nhất từ thẻ số, thêm điều kiện kép'),
    6:  ([8],      'quy tắc nhân để đếm — lớp 4 gọi là "nhân theo hàng"'),
    7:  ([7, 8],   'đếm số trong đoạn (B07) và phép đếm phần bù (B08)'),
    8:  ([7],      'đánh số trang & chữ số thứ n — cùng công trình thư viện'),
    9:  ([9, 10],  'dấu hiệu chia hết: đuôi số (B09) và cộng chữ số (B10)'),
    10: ([11],     'phép chia có dư, xếp hàng thừa - thiếu'),
    11: ([12],     'chu kỳ chữ số tận cùng của tích'),
    12: ([13, 14], 'dãy cách đều (B13) và dãy nhân - dãy hai tầng (B14)'),
    13: ([5],      'cặp số vàng để tính nhanh — gốc là tính nhanh cấp kỹ sư'),
    14: ([35],     'dãy phân số sai phân — chính là dãy bánh domino'),
    15: ([35],     'tích rút gọn chéo, cùng bài domino'),
    16: ([6],      'gỡ chiều tìm X'),
    17: ([33],     'so sánh phân số - hỗn số'),
    18: ([36],     'thêm - bớt cả tử và mẫu: đại lượng bất biến của phân số'),
    19: ([36],     'thêm một phía làm mất mỏ neo — cùng bài bất biến'),
    20: ([24, 34], 'tỉ số ẩn (B24) và phân số của một số (B34)'),
    21: ([16, 17], 'trung bình cộng cơ bản (B16) và luật bù trừ vượt - hụt (B17)'),
    22: ([17],     'hơn - kém trung bình cộng'),
    23: ([18],     'thành viên đến sau - rời đi: trung bình lung lay'),
    24: ([18, 16], 'gộp hai nhóm khác cỡ — vẫn là cây cầu TỔNG'),
    25: ([19],     'tổng - hiệu dạng chuẩn'),
    26: ([20],     'giấu tổng'),
    27: ([21],     'giấu hiệu, cú lừa "chuyển k đơn vị"'),
    28: ([27, 22], 'hiệu tuổi bất biến (B27) và trước - sau (B22)'),
    29: ([23],     'sơ đồ phần: tổng - tỉ cơ bản'),
    30: ([24, 26], 'giấu tổng (B24) và chuỗi tỉ ba số (B26)'),
    31: ([25],     'hiệu - tỉ: phần chênh là chìa khóa'),
    32: ([24],     'giấu tỉ số, tỉ biết biến hình'),
    33: ([26],     'hai tỉ số nối nhau — mắt xích nối tỉ'),
    34: ([26],     'nhân chéo cân bằng, vẫn là bài nối tỉ'),
    35: ([27],     'toán tuổi nâng cao: hiệu đứng im, tỉ trôi'),
    36: ([27],     'nhiều mốc - nhiều người, cùng một mỏ neo hiệu tuổi'),
    37: ([34],     'ba dạng phần trăm nền tảng — gốc là phân số của một số'),
    38: ([37],     'lãi - lỗ: đúng bài lãi vốn'),
    39: ([37],     'tươi - khô, quả dưa hấu: đúng bài bay hơi'),
    40: ([37],     'pha thêm - cô cạn: đúng bài nước đường'),
    41: ([28],     'làm chung việc chuẩn phân số'),
    42: ([28],     'vòi vào - vòi ra: vẫn là chia việc thành phần đều'),
    43: ([29, 30], 'tính ngược từ cuối (B29) và giả thiết tạm (B30)'),
    44: ([31, 32], 'khử - thế (B31) và Ven - chuồng thỏ (B32)'),
    45: ([40],     'diện tích tam giác, cặp đáy - cao — gốc là góc & đường cao'),
    46: ([39, 40], 'tỉ số diện tích: nới - thu sân (B39) trên hình đã cắt ghép (B40)'),
    47: ([38, 19], 'vẽ hình phụ rồi dùng tổng - hiệu trên diện tích'),
    48: ([40],     'hình thang & hình ghép — nối tiếp cắt ghép'),
    49: ([40],     'hình tròn: chu vi, diện tích'),
    50: ([40],     'hình phức hợp vành khăn - chiếc lá, vẫn dựng trên hình tròn'),
    51: ([41],     'diện tích xung quanh - toàn phần: hộp giấy khai triển'),
    52: ([41],     'thể tích & sơn khối lập phương: đếm khối theo tầng'),
    53: ([42],     'vận tốc - quãng đường - thời gian: nhịp chân một giờ'),
    54: ([43],     'đuổi kịp & gặp nhau'),
    55: ([43],     'đường vòng, xuôi - ngược dòng: vẫn chia cho hiệu hay tổng'),
    56: ([44],     'tàu qua cầu & góc hai kim đồng hồ'),
}


def main():
    man = json.load(open(MANIFEST, encoding='utf-8'))
    ten4 = {x['so']: x['ten'] for x in json.load(open(IDX4, encoding='utf-8'))}

    gan, loi = {}, []
    for l in man['lessons']:
        n = int(l['bai'][1:])
        if n not in TAY:
            loi.append(f'bài lớp 5 {l["bai"]} chưa khai trong bảng soát tay')
            continue
        ve, vi_sao = TAY[n]
        xau = [x for x in ve if x not in ten4]
        if xau:
            loi.append(f'{l["bai"]}: trỏ về bài lớp 4 không có thật {xau}')
        muc = {'ve': [MA4.format(x) for x in ve],
               'ten': [ten4.get(x, '') for x in ve],
               'canCu': 'chuDe', 'lopDuoi': 4, 'nhan': 'Học lại bài lớp 4',
               'viSao': vi_sao}
        for mi in l['micros']:
            gan[mi['id']] = muc
    thua = [n for n in TAY if n > len(man['lessons'])]
    if thua:
        loi.append(f'bảng soát tay khai thừa bài không có trong sách: {thua}')

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump({'_doc': 'Đường lùi lớp 5 → lớp 4, rải xuống từng micro.',
                   'tuLop': 'lop5', 'veLop': 'lop4', 'gan': gan},
                  f, ensure_ascii=False, indent=1)

    # ── gắn vào tệp bài, ở CẢ HAI nơi ──
    da_ghi = 0
    for thu_muc in NOI:
        for mid, muc in gan.items():
            ten_tep = mid.replace(':', '_').replace('.', '_') + '.json'
            duong = os.path.join(thu_muc, ten_tep)
            if not os.path.exists(duong):
                loi.append(f'không thấy tệp {duong}')
                continue
            j = json.load(open(duong, encoding='utf-8'))
            j['duongLui'] = {k: v for k, v in muc.items() if k != 'viSao'}
            with open(duong, 'w', encoding='utf-8') as f:
                json.dump(j, f, ensure_ascii=False, indent=1)
            da_ghi += 1

    print(f'đã ghi {RA}')
    print(f'  {len(man["lessons"])} bài sách lớp 5 → {len(gan)} micro có đường lùi')
    print(f'  gắn vào {da_ghi} tệp ({len(NOI)} nơi × {len(gan)} micro)')
    if loi:
        print(f'  ⚠ {len(loi)} chỗ lệch:')
        for x in loi[:20]:
            print('     ·', x)
        raise SystemExit(1)
    print('  ✓ chốt: đủ 56 bài · mọi đích có thật · hai nơi cùng nội dung')


if __name__ == '__main__':
    main()
