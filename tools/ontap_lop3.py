# -*- coding: utf-8 -*-
"""
LỚP 3 · BƯỚC 2c — bóc 8 ôn tập + 3 ải, và dựng mối nối ôn tập → bài.

    python3 tools/ontap_lop3.py

MỐI NỐI ÔN TẬP → BÀI: lớp 2 có "Bảng tự soi" thành bảng riêng. Lớp 3 KHÔNG có bảng
ấy — nhưng có cùng thông tin, viết thành LỜI trong khối đáp án:

    Câu 4, 5 → thuộc Bài 2 (Thêm chữ số bên trái - bên phải).
    Phòng 5 → thuộc Bài 29 (Giải phẫu hình tròn).

Bản khảo sát ban đầu của tôi kết luận "lớp 3 không có mối nối, phải tự suy theo
chương" — SAI. Suy theo chương thì một câu trỏ về cả 4-5 bài, bé chẳng biết mở bài
nào; sách chỉ đích danh từng câu. Lấy đúng thứ sách cho, chỉ suy khi sách không nói.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop3_tho.json')
RA = os.path.join(GOC_KHO, 'data', 'lop3_ontap.json')

R_ON = re.compile(r'^ÔN TẬP (\d+)\s*·\s*(.+)$')
# Tiêu đề ải có tiền tố ①②③: "① ẢI 1 · KHỞI ĐỘNG — kiểm tra vũ khí cơ bản"
R_AI = re.compile(r'^[①②③]?\s*ẢI (\d+)\s*·\s*(.+)$')
# Trong một ôn tập có ĐỀ CHÍNH rồi tới ĐỀ B, cả hai cùng đánh "Câu n." — gộp lại
# thì ôn tập 10 câu hoá ra 17-20 câu.
R_DE_B = re.compile(r'^✦?\s*ĐỀ B\b')
# "Câu 4, 5 → thuộc Bài 2 (…)" — mối nối câu sai → bài phải học lại
R_VE = re.compile(r'^(?:Câu|Phòng|Vụ|Đảo|Mã)\s+([\d,\s và]+?)\s*→\s*thuộc Bài (\d+)')
# Mốc ĐÓNG: đáp án, chương sau, bài sau — thiếu là chữ của phần sau chảy ngược vào
R_DONG = re.compile(r'^(?:\S+\s+)?(?:ĐÁP ÁN|CHƯƠNG \d+|Bài \d+\s*·|BẢNG SƯU TẬP'
                    r'|TOÁN TƯ DUY|LỜI (?:NHẮN|KẾT))')
# BẪY 7 · mỗi ôn tập đặt tên câu theo CHỦ ĐỀ riêng: "Câu 1." · "Vụ 1." · "Phòng 5"
# · "Đảo 3". Chỉ nhận "Câu" thì Ôn tập 6 ra 0 câu — mà nó vẫn ghi ra tệp bình thường.
R_CAU = re.compile(r'^(?:Câu|Vụ|Phòng|Đảo|Mã|Trạm|Cửa)\s*(\d+)[.:]?\s*(.+)$')
# Số câu cần đạt KHÔNG cố định 10: "Đạt 8/10 câu" · "Phá 6/8 vụ án".
R_DAT = re.compile(r'(?:Đạt|Phá|Vượt)\s*(\d+)\s*/\s*(\d+)')


def main():
    d = json.load(open(THO, encoding='utf-8'))
    # chương của mỗi bài, để suy mối nối ôn tập → bài
    chuong = {}
    for b in d['bai']:
        chuong.setdefault(b['chuong'], []).append(b['so'])
    dong = [t for b in d['bai'] for t in b['sauBai']]

    khoi, hien, loai, de_b = {}, None, None, False
    for t in dong:
        ve = R_VE.match(t)
        if ve and hien:
            for x in re.findall(r'\d+', ve.group(1)):
                khoi[hien]['veCau'].setdefault(f'C{x}', f'DL:KSN3.B{int(ve.group(2)):02}')
            continue
        m = R_ON.match(t) or R_AI.match(t)
        if m:
            loai = 'onTap' if R_ON.match(t) else 'ai'
            hien = f'{loai}{int(m.group(1))}'
            khoi[hien] = {'loai': loai, 'so': int(m.group(1)),
                          'ten': m.group(2).strip(), 'dong': [], 'cau': [],
                          'cauDeB': [], 'veCau': {}, 'can': None, 'tong': None}
            de_b = False
            continue
        if hien and R_DE_B.match(t):
            de_b = True                      # từ đây là ĐỀ B, đếm riêng
            continue
        if R_DONG.match(t):
            hien = None
            continue
        if hien:
            c = R_CAU.match(t)
            if c:
                o = khoi[hien]['cauDeB'] if de_b else khoi[hien]['cau']
                o.append({'id': f'C{len(o) + 1}', 'so': int(c.group(1)), 'text': c.group(2)})
            else:
                dt = R_DAT.search(t)
                if dt and khoi[hien]['can'] is None:
                    khoi[hien]['can'] = int(dt.group(1))
                    khoi[hien]['tong'] = int(dt.group(2))
                khoi[hien]['dong'].append(t)

    # ── mối nối ôn tập → bài, thay cho Bảng tự soi mà lớp 3 không có ──
    for k, v in khoi.items():
        if v['veCau']:
            v['canCu'] = 'sach'                    # sách chỉ đích danh từng câu
        elif v['loai'] == 'onTap':
            # sách không nói thì mới suy theo chương — và nói rõ là suy
            v['veCau'] = {c['id']: [f'DL:KSN3.B{x:02}' for x in chuong.get(v['so'], [])]
                          for c in v['cau']}
            v['canCu'] = 'chuong'
        else:
            v['canCu'] = 'ai'

    ra = {'_doc': 'Tám ôn tập và ba ải của lớp 3, kèm mối nối về bài để bé làm sai '
                  'còn biết học lại chỗ nào.',
          '_canCu': {'chuong': 'ôn tập nằm cuối chương nên trỏ về các bài của chính '
                               'chương ấy — SUY TỪ CẤU TRÚC SÁCH, cần soát tay từng câu',
                     'sach': 'sách chỉ đích danh "Câu n → thuộc Bài m" — chắc chắn',
                     'ai': 'ải phủ cả sách, không trỏ riêng bài nào'},
          'khoi': khoi}
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(ra, f, ensure_ascii=False, indent=1)

    on = [v for v in khoi.values() if v['loai'] == 'onTap']
    ai = [v for v in khoi.values() if v['loai'] == 'ai']
    print(f'đã ghi {RA}')
    print(f'  {len(on)} ôn tập · {len(ai)} ải · {sum(len(v["cau"]) for v in khoi.values())} câu')
    for v in on:
        tong = v['tong'] or 10
        if len(v['cau']) != tong:
            print(f'  ⚠ Ôn tập {v["so"]} tách được {len(v["cau"])} câu, sách nói {tong}')
        if not v['veCau']:
            print(f'  ⚠ Ôn tập {v["so"]} không trỏ về bài nào — bé sai sẽ không biết học lại đâu')


if __name__ == '__main__':
    main()
