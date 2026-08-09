# -*- coding: utf-8 -*-
"""
LỚP 3 · BƯỚC 3.0 — đếm xem PHẢI VẼ BAO NHIÊU HÌNH, trước khi vẽ cái nào.

    python3 tools/khao_sat_hinh_lop3.py            # in bảng tổng
    python3 tools/khao_sat_hinh_lop3.py --chi-tiet # in từng câu một, để soát tay

Lớp 2 trả giá hai lượt: vẽ đủ 75 hình giảng rồi tưởng xong, mãi tới khi có người đọc
kỹ mới lộ ra màn mở không có hình và **46 câu bài tập nói tới hình mà không câu nào
có hình** — phải quay lại vẽ thêm 45 hình nữa, bằng 3/8 tổng công vẽ.

Nên với lớp 3, đếm cả BA loại hình ngay từ đầu (chuẩn mục 10 · Bước 3):

  1. hình giảng   — neo theo bước, mục ③ khamPha
  2. hình màn mở  — mục ② chuyenMoBai, là bản ĐỀ: bỏ hết đáp án
  3. hình bài tập — cặp `item:CX` + `item:CX:giai` cho mọi câu mà đề MÔ TẢ một hình

Công cụ này KHÔNG quyết thay người. Nó chỉ khoanh vùng: câu nào có từ chỉ hình thì
nêu ra để soát tay. Thà nêu thừa rồi gạch, còn hơn bỏ sót — bỏ sót thì im lặng, mà
im lặng là kiểu hỏng đắt nhất của cả dây chuyền này.
"""
import json, os, re, sys
from collections import Counter, defaultdict

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop3_tho.json')
ONTAP = os.path.join(GOC_KHO, 'data', 'lop3_ontap.json')

# Từ chỉ hình, gom theo NHÓM NGUYÊN MẪU để biết luôn phải viết nguyên mẫu nào.
# Mỗi nhóm là (tên nhóm, mẫu). Một câu có thể rơi vào nhiều nhóm — đó là chuyện
# thường: "tính chu vi hình chữ nhật rồi vẽ sơ đồ" cần cả hai.
NHOM = [
    ('hình phẳng & chu vi - diện tích',
     r'hình (?:chữ nhật|vuông|tam giác|tứ giác)|chu vi|diện tích|cạnh|chiều (?:dài|rộng)'),
    ('hình tròn', r'hình tròn|bán kính|đường kính|tâm |quanh hồ|vòng tròn'),
    ('khối & tầng lầu', r'khối lập phương|xếp khối|mấy khối|tầng (?:trên|dưới)|tòa nhà'),
    ('tia số & dãy số', r'dãy (?:số|thỏ)|số hạng thứ|viết tiếp|quy luật|nhịp|toa tàu'),
    ('sơ đồ đoạn thẳng', r'gấp mấy lần|gấp \d+ lần|hơn .{0,12}(?:đơn vị|viên|tuổi)|tổng .{0,20}(?:là|bằng)'),
    ('chia có dư & chấm tròn', r'chia .{0,10}dư|số dư|thương|chia đều|một phần|1/\d'),
    ('sơ đồ Ven', r'cả hai|thích ít nhất|không (?:mê|thích) môn nào'),
    ('gà - chó, giả thiết tạm', r'\bđầu\b.{0,20}\bchân\b|mấy gà|xe (?:đạp|ba bánh)'),
    ('trồng cây - khoảng cách', r'trồng .{0,10}cây|cây cách cây|nhát cưa|cắm cọc|đoạn'),
    ('máy biến đổi & đi lùi', r'nhân .{0,8}rồi (?:cộng|trừ)|đi lùi|tìm số đó|nghĩ một số'),
    ('biểu thức & ngoặc', r'ngoặc|thứ tự|tính thuận tiện|tìm X'),
    ('đồng hồ & lịch', r'\d+ giờ|kim (?:giờ|phút)|thứ mấy|ngày \d+|tờ lịch|kém'),
    ('cân & ống đong', r'cân|thăng bằng|\bgam\b|\bkg\b|\bml\b|đĩa (?:trái|phải)|ống đong'),
    ('tiền Việt', r'nghìn đồng|tờ \d+ nghìn|tiền|vốn|lãi|trả lại'),
    ('bảng giá trị chỗ', r'chữ số|hàng (?:nghìn|trăm|chục|đơn vị)|tách .{0,10}thành tổng|đọc số'),
]
NHOM = [(t, re.compile(m, re.I)) for t, m in NHOM]

# Từ ĐÒI HÌNH hẳn — đề BẢO bé vẽ, hoặc đề trỏ vào một hình đang có.
R_CHAC = re.compile(r'\bvẽ\b|\bđếm\b.{0,12}hình|hình (?:vẽ|bên|dưới)|trên hình|sơ đồ|'
                    r'bản đồ|quan sát|nhìn hình|tô màu|\bkẻ\b', re.I)

# Tầng giữa: đề KHÔNG bảo vẽ, nhưng nói tới một VẬT THỂ nhìn được — cái mà hình vẽ
# ra thì bé hiểu ngay, còn tả bằng lời thì phải tự dựng trong đầu.
#
# Bảng NHOM ở trên là bản đồ CHỦ ĐỀ (để biết cần viết nguyên mẫu nào), không phải
# bộ lọc: nó bắt cả "đọc số 3 507" vào nhóm bảng giá trị chỗ. Lượt quét đầu của tôi
# dùng nó làm bộ lọc luôn nên ra 306/477 câu "có thể cần" — đó là nhiễu chứ không
# phải sàng lọc, và một danh sách 306 dòng thì không ai soát tay nổi.
R_VAT = re.compile(
    r'hình (?:chữ nhật|vuông|tròn|tam giác|tứ giác)|chu vi|diện tích|bán kính|đường kính|'
    r'khối lập phương|mấy khối|tầng (?:trên|dưới)|đoạn thẳng|điểm giữa|trung điểm|'
    r'dãy (?:số|thỏ)|số hạng thứ|tia số|'
    r'cân (?:thăng bằng|bột)?|đĩa (?:trái|phải)|quả cân|ống đong|cốc \d+ ml|'
    r'kim (?:giờ|phút)|mấy giờ|giờ kém|tờ lịch|thứ mấy|'
    r'tờ \d+ nghìn|trả lại|'
    r'cả hai|ít nhất một|'
    r'\bđầu\b.{0,24}\bchân\b|xe ba bánh|'
    r'trồng .{0,12}cây|cây cách cây|nhát cưa|cắm cọc', re.I)


def nhom_cua(text):
    return [t for t, m in NHOM if m.search(text)]


def can_hinh(text):
    """('chac'|'cothe'|None) — mức chắc chắn rằng câu này cần một hình."""
    if R_CHAC.search(text):
        return 'chac'
    return 'cothe' if R_VAT.search(text) else None


def main(chi_tiet=False):
    d = json.load(open(THO, encoding='utf-8'))
    bai = d['bai']

    # ── loại 1 & 2: bài nào thiếu hình giảng / hình màn mở ──
    # Bản trích chưa gắn hình nào (mục 'hinh' chưa có) nên ở đây đếm theo NHU CẦU:
    # bài nào cũng cần một hình mở, và cần hình giảng cho mỗi bước có thể vẽ.
    can_mo, can_giang = [], []
    for b in bai:
        can_mo.append(b['so'])
        buoc = [x for x in (b['muc']['khamPha'].get('dong') or [])
                if re.match(r'^(Bước|Nhịp|Vũ khí|Chặng)\s*\d', x)]
        can_giang.append((b['so'], len(buoc)))

    # ── loại 3: câu bài tập nào MÔ TẢ một hình ──
    theo_nhom = Counter()
    cau_can = defaultdict(list)          # số bài → [(mã câu, phần, mức, nhóm, lời)]
    tong_cau = 0
    for b in bai:
        for c in b['cau']:
            tong_cau += 1
            for n in nhom_cua(c['text']):    # bản đồ chủ đề: đếm trên MỌI câu
                theo_nhom[n] += 1
            muc = can_hinh(c['text'])
            if muc:
                cau_can[b['so']].append((c['id'], c['phan'], muc,
                                         nhom_cua(c['text']), c['text']))

    # ── ôn tập & ải cũng có câu cần hình, và chúng nằm ở tệp khác ──
    on = json.load(open(ONTAP, encoding='utf-8'))['khoi'] if os.path.exists(ONTAP) else {}
    cau_on = []
    for k, v in on.items():
        for c in v['cau']:
            if can_hinh(c['text']):
                cau_on.append((k, c['id'], nhom_cua(c['text']), c['text']))

    n_chac = sum(1 for ds in cau_can.values() for x in ds if x[2] == 'chac')
    n_co_the = sum(len(ds) for ds in cau_can.values()) - n_chac

    print('LỚP 3 · KHỐI LƯỢNG VẼ HÌNH — ba loại, đếm trước khi vẽ\n')
    print(f'  {len(bai)} bài · {tong_cau} câu\n')
    print('  loại 1 · hình giảng   — mỗi bước một hình, '
          f'{sum(n for _, n in can_giang)} bước ở {len(can_giang)} bài')
    print(f'  loại 2 · hình màn mở  — {len(can_mo)} bài, mỗi bài một hình ĐỀ')
    print(f'  loại 3 · hình bài tập — {n_chac} câu CHẮC CHẮN cần hình '
          f'(có "vẽ"/"đếm hình"/"sơ đồ"…)')
    print(f'                          + {n_co_the} câu có thể cần — phải soát tay')
    print(f'  ôn tập & ải           — {len(cau_on)} câu nhắc tới hình\n')
    print('  Mỗi câu loại 3 cần HAI hình (đề `item:CX` + lời giải `item:CX:giai`),')
    print(f'  nên riêng phần chắc chắn đã là {n_chac * 2} hình.\n')

    print('  ── nhóm nguyên mẫu, xếp theo số câu chạm tới ──')
    for n, c in theo_nhom.most_common():
        print(f'    {c:4}  {n}')

    if chi_tiet:
        print('\n  ── từng câu, để soát tay ──')
        for so in sorted(cau_can):
            print(f'\n  Bài {so} · {next(b["ten"] for b in bai if b["so"] == so)}')
            for ma, phan, muc, ns, text in cau_can[so]:
                print(f'    {"●" if muc == "chac" else "○"} {ma} [{phan}] {text[:96]}')
                print(f'         → {" · ".join(ns) or "chưa xếp nhóm"}')
        print('\n  ── ôn tập & ải ──')
        for k, ma, ns, text in cau_on:
            print(f'    {k} {ma}: {text[:88]}\n         → {" · ".join(ns)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main('--chi-tiet' in sys.argv))
