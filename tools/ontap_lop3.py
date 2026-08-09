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

── VÌ SAO BẢN NÀY ĐỌC THEO KHỐI, KHÔNG DÒ TỪNG DÒNG ──

Bản trước tách THỪA 1-5 câu ở 5/8 ôn tập. Tôi đã đoán là mẫu tách câu hỏng. Không
phải. In nguyên văn thân khối ra đọc thì thấy: mọi câu thừa đều là một dòng của
BẢNG TỰ SOI bị nhận nhầm thành câu hỏi. Mẫu mối nối trượt, dòng rơi xuống mẫu câu
hỏi ở dưới, thế là "Câu 6 và câu 11 → thuộc Bài 7" hoá ra câu hỏi số 6.

Nên bản này ĐỌC CẤU TRÚC mà sách đã bày sẵn — mỗi ôn tập luôn có ba phần, ngăn bởi
hai mốc ✦ rõ ràng:

    thân đề  →  ✦ BẢNG TỰ SOI  →  ✦ ĐỀ B

Trong phần nào thì chỉ dùng mẫu của phần ấy. Dòng mối nối không còn cửa nào để rơi
xuống thành câu hỏi, kể cả khi mẫu mối nối trượt — trượt thì mất mối nối và bộ đếm
kêu lên, chứ không đẻ ra một câu hỏi ma.

Bốn dạng viết mối nối mà sách dùng, mẫu cũ trượt cả bốn:
    "Câu 6 và câu 11 → thuộc Bài 7"          — chữ "và câu" xen giữa các số
    "Câu 1, 4, 5 và mật thư (A) → Bài 10"    — mật thư là phần của câu cuối
    "Mã 4, 5, 6 và câu (b) mã 12 → Bài 14"   — trỏ tới MỘT Ý của câu 12
    "Vụ 1, 2 → vũ khí ĐI LÙI (Bài 22)"       — số bài nằm trong ngoặc, không có "thuộc"
Và ôn tập 8 nhét CẢ BA mối nối vào chung một dòng — mẫu cũ chỉ lấy cái đầu tiên.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop3_tho.json')
RA = os.path.join(GOC_KHO, 'data', 'lop3_ontap.json')

R_ON = re.compile(r'^ÔN TẬP (\d+)\s*·\s*(.+)$')
# Tiêu đề ải có tiền tố ①②③: "① ẢI 1 · KHỞI ĐỘNG — kiểm tra vũ khí cơ bản"
R_AI = re.compile(r'^[①②③]?\s*ẢI (\d+)\s*·\s*(.+)$')

# ── hai mốc chia khối làm ba phần ──
R_SOI = re.compile(r'BẢNG TỰ SOI')
# Ôn tập 6 gọi đề B là "TẬP HỒ SƠ B" cho hợp chuyện thám tử — mẫu chỉ nhận "ĐỀ B"
# thì đề B của nó chảy ngược vào thân đề.
R_DE_B = re.compile(r'^✦?\s*(?:ĐỀ B|TẬP HỒ SƠ B)\b')

# BẪY 7 · mỗi ôn tập đặt tên câu theo CHỦ ĐỀ riêng: "Câu 1." · "Vụ 1." · "Phòng 5"
# · "Đảo 3". Chỉ nhận "Câu" thì Ôn tập 6 ra 0 câu — mà nó vẫn ghi ra tệp bình thường.
TEN_CAU = r'Câu|Vụ|Phòng|Đảo|Mã|Trạm|Cửa'
R_CAU = re.compile(rf'^(?:{TEN_CAU})\s*(\d+)[.:]?\s*(.+)$')
# "★★ PHẦN 2 — VẬN DỤNG (4 câu)" — số ★ chính là mức khó, sách xếp tăng dần
R_PHAN = re.compile(r'^(★+)\s*(.+)$')
# Mốc ĐÓNG: đáp án, chương sau, bài sau — thiếu là chữ của phần sau chảy ngược vào
R_DONG = re.compile(r'^(?:\S+\s+)?(?:ĐÁP ÁN|CHƯƠNG \d+|Bài \d+\s*·|BẢNG SƯU TẬP'
                    r'|TOÁN TƯ DUY|PHẦN CUỐI SÁCH|LỜI (?:NHẮN|KẾT))')

# Mối nối, quét bằng finditer nên một dòng chứa mấy mối nối vẫn lấy đủ. Vế trái ôm
# mọi thứ tới dấu → (kể cả "và câu", "và mật thư (A)"), vế phải dừng ở "Bài <số>"
# đầu tiên nên "→ vũ khí ĐI LÙI (Bài 22)" cũng ra 22.
R_NOI = re.compile(rf'(?:{TEN_CAU})\s+([^→]*?)\s*→\s*[^→]*?Bài\s*(\d+)')
# Số câu cần đạt KHÔNG cố định 10, và động từ cũng không cố định: "Đạt 8/10 câu" ·
# "Phá 6/8 vụ án" · "Nhập đúng 9/12 mã" · "Nghiệm thu 8/10 phòng". Nhận theo hình
# dạng a/b trong phần mở đầu, đừng liệt kê động từ — liệt kê thì sót, và sót lặng lẽ:
# ôn tập 4 từng bị lấy mặc định 10 trong khi sách nói 12.
R_DAT = re.compile(r'(\d+)\s*/\s*(\d+)')
# Đề B nhồi nhiều câu trên một dòng: "B1. … B2. … B3. …"
R_CAU_B = re.compile(r'(?:^|\s)B(\d+)\.\s*')

MA_BAI = 'DL:KSN3.B{:02}'

# ── đáp án ôn tập, nằm ở khối riêng cuối chương ──
# "Ô1 ĐÁP ÁN ÔN TẬP 1 — Lễ mở cổng (Đề chính)" rồi "Ô1B ĐÁP ÁN ĐỀ B".
# Bản đầu của bộ tách này ĐÓNG khối ngay khi gặp chữ ĐÁP ÁN, nên tám bộ đáp án ôn
# tập rơi hết ra ngoài — mà mất đáp án thì kỳ sát hạch chỉ còn đề, bé làm xong
# không có gì để so.
R_DA_ON = re.compile(r'^Ô(\d+)(B?)\s+ĐÁP ÁN')
# Ải đánh tiêu đề bằng tiền tố "Ả<n>", không phải "★ ĐÁP ÁN ẢI" như tôi đoán lúc đầu
R_DA_AI = re.compile(r'^Ả(\d+)\s+ĐÁP ÁN')
# "C1: … C2: … C10: …" viết liền một dòng, cắt theo mã câu.
# Chữ cái đầu KHÔNG cố định là C: ôn tập 6 đặt tên câu là "Vụ" nên đáp án ghi
# "V1: … V2: …"; đề B thì luôn là "B<n>". Và ôn tập 3 chèn nhãn giữa mã với dấu hai
# chấm: "C10 — MẬT THƯ: (A) …". Nhận rộng ở đây rồi CHUẨN HOÁ về mã câu bên dưới,
# chứ liệt kê từng chữ cái thì cứ mỗi ôn tập lại sót thêm một kiểu.
R_DA_CAU = re.compile(r'\b([A-ZĐ])(\d+)\s*(?:\([^)]*\))?'
                      r'(?:\s*[—–-]\s*[^:：]{0,24})?\s*[:：]\s*')


def moi_noi(dong, cau, tong):
    """Đọc một dòng bảng tự soi → [(số câu, mã bài)]. Trả rỗng nếu dòng không phải
    mối nối; người gọi tự biết mà kêu, chứ hàm này không đoán bừa."""
    ra = []
    for m in R_NOI.finditer(dong):
        ve_trai, bai = m.group(1), int(m.group(2))
        so = [int(x) for x in re.findall(r'\d+', ve_trai)]
        # "mật thư (A)" là một Ý của câu cuối chứ không phải câu riêng — ôn tập 3 trỏ
        # câu 10 về hai bài khác nhau vì ba ý A/B/C của nó thuộc hai bài.
        if 'mật thư' in ve_trai.lower():
            so += [c['so'] for c in cau if 'MẬT THƯ' in c['text']]
        for x in sorted(set(so)):
            if 1 <= x <= tong:                 # số lạc (năm, cỡ…) thì bỏ, đừng đẻ câu ma
                ra.append((x, MA_BAI.format(bai)))
    return ra


def boc_dap_an(dong):
    """{'onTap1': {'C1': '…'}, 'onTap1B': {'B1': '…'}, 'ai1': {'C1': '…'}} — đáp án
    của các kỳ ôn tập và ải, gom từ những khối `Ô<n> ĐÁP ÁN …` ở cuối mỗi chương."""
    ra, hien = {}, None
    for t in dong:
        m = R_DA_ON.match(t)
        if m:
            hien = f'onTap{int(m.group(1))}' + ('B' if m.group(2) else '')
            ra.setdefault(hien, {})
            continue
        m = R_DA_AI.match(t)
        if m:
            hien = f'ai{int(m.group(1))}' if m.group(1) else 'aiChung'
            ra.setdefault(hien, {})
            continue
        # bất kỳ tiêu đề ĐÁP ÁN nào khác (đáp án BÀI) đều ĐÓNG khối đang mở — không
        # đóng thì đáp án của bài chảy ngược vào ôn tập, mà cả hai cùng đánh C1, C2…
        if 'ĐÁP ÁN' in t[:40] or R_DONG.match(t):
            hien = None
            continue
        if hien is None:
            continue
        de_b = hien.endswith('B')
        vt = [(x.group(2), x.start(), x.end()) for x in R_DA_CAU.finditer(t)]
        for i, (so, _, het) in enumerate(vt):
            ket = vt[i + 1][1] if i + 1 < len(vt) else len(t)
            loi = t[het:ket].strip().rstrip('.;, ')
            if loi:
                # Chuẩn hoá về mã câu: khối đề B giữ "B<n>", khối đề chính về "C<n>"
                # bất kể sách viết C, V hay chữ nào — mã câu bên bảng đề luôn là C<n>.
                ra[hien][('B' if de_b else 'C') + so] = loi
    return {k: v for k, v in ra.items() if v}


def main():
    d = json.load(open(THO, encoding='utf-8'))
    chuong = {}
    for b in d['bai']:
        chuong.setdefault(b['chuong'], []).append(b['so'])
    dong = [t for b in d['bai'] for t in b['sauBai']]

    khoi, hien, phan = {}, None, None
    for t in dong:
        m = R_ON.match(t) or R_AI.match(t)
        if m:
            loai = 'onTap' if R_ON.match(t) else 'ai'
            hien = f'{loai}{int(m.group(1))}'
            khoi[hien] = {'loai': loai, 'so': int(m.group(1)), 'ten': m.group(2).strip(),
                          'dong': [], 'phan': [], 'cau': [], 'cauDeB': [],
                          'soiTho': [], 'veCau': {}, 'can': None, 'tong': None}
            phan = None
            continue
        if R_DONG.match(t):
            hien = None
            continue
        if not hien:
            continue
        k = khoi[hien]

        # ── ba phần của một khối, mỗi phần một bộ mẫu riêng ──
        if R_DE_B.match(t):
            k['_phan'] = 'deB'
            continue
        if R_SOI.search(t) and k.get('_phan') != 'deB':
            k['_phan'] = 'soi'
            continue

        if k.get('_phan') == 'deB':
            cat = R_CAU_B.split(t)             # ['', '1', 'nội dung', '2', 'nội dung', …]
            for i in range(1, len(cat) - 1, 2):
                k['cauDeB'].append({'id': f'B{cat[i]}', 'so': int(cat[i]),
                                    'text': cat[i + 1].strip()})
            continue

        if k.get('_phan') == 'soi':
            k['soiTho'].append(t)              # giữ nguyên văn, đọc lại được khi ngờ
            continue

        # ── thân đề ──
        p = R_PHAN.match(t)
        if p:
            phan = {'mucDo': len(p.group(1)), 'ten': p.group(2).strip()}
            k['phan'].append(phan)
            continue
        c = R_CAU.match(t)
        if c:
            k['cau'].append({'id': f'C{c.group(1)}', 'so': int(c.group(1)),
                             'text': c.group(2), 'mucDo': phan['mucDo'] if phan else 1})
            continue
        if k['tong'] is None and not k['cau']:
            # ngưỡng đạt luôn nằm ở mấy dòng mở đầu, TRƯỚC câu hỏi đầu tiên — quét sau
            # đó thì vớ phải phân số trong đề ("Tìm 1/4 của 24 viên ngọc").
            dt = R_DAT.search(t)
            if dt and int(dt.group(1)) < int(dt.group(2)) <= 30:
                k['can'], k['tong'] = int(dt.group(1)), int(dt.group(2))
        k['dong'].append(t)

    # ── đáp án của chính kỳ ôn tập ──
    da = boc_dap_an(dong)

    # ── mối nối ôn tập → bài, thay cho Bảng tự soi mà lớp 3 không có ──
    canh_bao = []
    for k, v in khoi.items():
        v.pop('_phan', None)
        v['dapAn'] = da.get(k, {})
        v['dapAnB'] = da.get(k + 'B', {})
        if v['tong'] is None:
            v['tong'] = len(v['cau'])          # ải không nêu ngưỡng: làm hết là xong
        for t in v['soiTho']:
            for so, ma in moi_noi(t, v['cau'], v['tong']):
                ve = v['veCau'].setdefault(f'C{so}', [])
                if ma not in ve:
                    ve.append(ma)
        if v['veCau']:
            v['canCu'] = 'sach'                # sách chỉ đích danh từng câu
        elif v['loai'] == 'onTap':
            # sách không nói thì mới suy theo chương — và nói rõ là suy
            v['veCau'] = {c['id']: [MA_BAI.format(x) for x in chuong.get(v['so'], [])]
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
          '_veCau': 'mã câu → DANH SÁCH mã bài. Một câu trỏ về hai bài là chuyện có '
                    'thật, không phải lỗi: câu chốt của ôn tập thường ghép ý của hai '
                    'bài (ôn tập 3 câu 10, ôn tập 4 câu 12).',
          'khoi': khoi}
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(ra, f, ensure_ascii=False, indent=1)

    # ── soát: mỗi phép đếm bắt một kiểu hỏng đã xảy ra thật ──
    on = [v for v in khoi.values() if v['loai'] == 'onTap']
    ai = [v for v in khoi.values() if v['loai'] == 'ai']
    print(f'đã ghi {RA}')
    print(f'  {len(on)} ôn tập · {len(ai)} ải · '
          f'{sum(len(v["cau"]) for v in khoi.values())} câu · '
          f'{sum(len(v["cauDeB"]) for v in khoi.values())} câu đề B')
    for v in khoi.values():
        ten = f'{"Ôn tập" if v["loai"] == "onTap" else "Ải"} {v["so"]}'
        if len(v['cau']) != v['tong']:
            canh_bao.append(f'{ten} tách được {len(v["cau"])} câu, sách nói {v["tong"]}')
        # số câu phải liền mạch 1…n: thủng một số là mẫu tách bỏ sót đúng câu ấy
        thieu = [x for x in range(1, v['tong'] + 1) if not any(c['so'] == x for c in v['cau'])]
        if thieu:
            canh_bao.append(f'{ten} thiếu câu số {thieu}')
        # đáp án phải khớp 1:1 với câu — thiếu thì bé làm xong không có gì để so,
        # thừa thì có mã lạ không ứng với câu nào
        hoi = {c['id'] for c in v['cau']}
        thieu_da = sorted(hoi - set(v['dapAn']))
        thua_da = sorted(set(v['dapAn']) - hoi)
        if thieu_da:
            canh_bao.append(f'{ten} thiếu đáp án {thieu_da}')
        if thua_da:
            canh_bao.append(f'{ten} thừa đáp án {thua_da} — đè từ khối khác?')
        if v['loai'] != 'onTap':
            continue
        if not v['cauDeB']:
            canh_bao.append(f'{ten} không có đề B — bé chưa đạt sẽ không có gì để làm lại')
        elif len(v['cauDeB']) != v['tong']:
            canh_bao.append(f'{ten} đề B có {len(v["cauDeB"])} câu, đề chính {v["tong"]}')
        if v['canCu'] != 'sach':
            canh_bao.append(f'{ten} phải SUY mối nối theo chương — sách có nói rõ, '
                            f'mẫu đọc trượt thì phải chữa mẫu chứ đừng suy')
        else:
            ho = [x for x in range(1, v['tong'] + 1) if f'C{x}' not in v['veCau']]
            if ho:
                canh_bao.append(f'{ten} câu {ho} không trỏ về bài nào — bé sai sẽ '
                                f'không biết học lại đâu')
    for c in canh_bao:
        print(f'  ⚠ {c}')
    if not canh_bao:
        print('  ✓ số câu, số đề B và mối nối đều khớp con số sách nêu')
    return 1 if canh_bao else 0


if __name__ == '__main__':
    raise SystemExit(main())
