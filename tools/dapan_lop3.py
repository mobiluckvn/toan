# -*- coding: utf-8 -*-
"""
LỚP 3 · BƯỚC 2b — bóc đáp án từ khối cuối sách.

    python3 tools/dapan_lop3.py

Sách gom hết đáp án vào một khối riêng `ĐÁP ÁN CHI TIẾT — GIỌNG SU KEM`, bên trong
là 34 mục `B<n>  ĐÁP ÁN BÀI <n> — <tên>`, xen giữa là đáp án 8 ôn tập, 7 Đề B và
ba ải.

⚠ BẪY 6 CỦA CHUẨN, lớp 2 đã dính và mất 60 lời giải: đáp án ôn tập / Đề B / ải
CŨNG đánh `C1, C2…`. Nếu không ĐÓNG bài đang mở khi gặp tiêu đề của chúng thì
`C1..C12` của ôn tập ghi đè lên `C1..C12` của bài — dữ liệu vẫn hợp lệ, bài vẫn
chạy, chỉ là lời giải gắn sai câu và KHÔNG CÓ GÌ BÁO.

⚠ Tiêu đề có TIỀN TỐ dấu trang (`B1  ĐÁP ÁN BÀI 1`) nên mẫu neo `^ĐÁP ÁN` trượt hết.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop3_tho.json')
RA = os.path.join(GOC_KHO, 'data', 'lop3_dapan.json')

R_MO = re.compile(r'^(?:\S+\s+)?ĐÁP ÁN BÀI (\d+)\b')
# Mọi thứ dưới đây ĐÓNG bài đang mở. Thiếu một dòng ở đây là đáp án của nó chảy
# vào bài trước — xem bẫy 6.
R_DONG = re.compile(r'^(?:\S+\s+)?(?:ĐÁP ÁN (?:ÔN TẬP|ĐỀ B|BA ẢI)|Đáp án ba ải'
                    r'|CHƯƠNG \d+|Ải \d+|Ôn tập \d+)')
R_PHAN = re.compile(r'^(Luyện tập|Quiz)\s*[—:-]\s*(.*)$')
# Luyện tập viết "C1: …" — ĐÒI dấu hai chấm, vì lời giải dài có nhắc "C5" giữa câu,
# nhận bừa là cắt nhầm giữa lời giải.
R_CAU = re.compile(r'(?:^|\s)(C\d+)\s*[:.]\s*')
# Quiz viết "C1 ĐÚNG · C2 SAI · C3 B" — KHÔNG có dấu hai chấm. Dùng chung một mẫu
# thì quiz ra 0 đáp án mà chẳng thấy vì sao.
R_CAU_QUIZ = re.compile(r'(?:^|\s)(C\d+)\s+')


def tach_cau(s, mau=R_CAU):
    """'C1: abc. C2: def' → {'C1': 'abc.', 'C2': 'def'}"""
    vt = [(m.group(1), m.start(), m.end()) for m in mau.finditer(s)]
    ra = {}
    for k, (ma, _, het) in enumerate(vt):
        cuoi = vt[k + 1][1] if k + 1 < len(vt) else len(s)
        ra[ma] = s[het:cuoi].strip().rstrip('·').strip()
    return ra


def main():
    d = json.load(open(THO, encoding='utf-8'))
    dong = [t for b in d['bai'] for t in b['sauBai']]

    khoi, hien = {}, None
    for t in dong:
        m = R_MO.match(t)
        if m:
            hien = int(m.group(1))
            khoi.setdefault(hien, [])
            continue
        if R_DONG.match(t):
            hien = None            # ĐÓNG bài — không thì đáp án ôn tập đè lên
            continue
        if hien is not None:
            khoi[hien].append(t)

    ra, thieu = {}, []
    for so, ds in sorted(khoi.items()):
        phan, dang = {}, None
        for t in ds:
            p = R_PHAN.match(t)
            if p:
                dang = 'luyenTap' if p.group(1) == 'Luyện tập' else 'quiz'
                phan.setdefault(dang, '')
                phan[dang] += ' ' + p.group(2)
            elif dang:
                phan[dang] += ' ' + t
        ma = f'DL:KSN3.B{so:02}'
        ra[ma] = {k: tach_cau(v, R_CAU_QUIZ if k == 'quiz' else R_CAU)
                  for k, v in phan.items()}
        if not ra[ma].get('luyenTap'):
            thieu.append(f'B{so} thiếu đáp án luyện tập')
        if len(ra[ma].get('quiz') or {}) != 5:
            thieu.append(f'B{so} có {len(ra[ma].get("quiz") or {})} đáp án quiz, phải 5')

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(ra, f, ensure_ascii=False, indent=1)
    n_lt = sum(len(v.get('luyenTap') or {}) for v in ra.values())
    n_q = sum(len(v.get('quiz') or {}) for v in ra.values())
    print(f'đã ghi {RA}')
    print(f'  {len(ra)} bài · {n_lt} đáp án luyện tập · {n_q} đáp án quiz')
    for x in thieu[:12]:
        print('  ⚠', x)
    if thieu:
        print(f'  ⚠ tổng {len(thieu)} chỗ cần soát')


if __name__ == '__main__':
    main()
