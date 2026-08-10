# -*- coding: utf-8 -*-
"""
LỚP 4 · BƯỚC 2 — bóc đáp án chi tiết, khớp 1:1 với câu hỏi.

    python3 tools/rut_lop4.py && python3 tools/dapan_lop4.py

Đáp án nằm ở CUỐI CHƯƠNG, trong `sauBai` của bài cuối mỗi chương (bước 1 đã cất
riêng ra đó). Một chương cho ra ba loại khối:

    B1   ĐÁP ÁN BÀI 1 — Những con số khổng lồ quanh nhà     ← 9 câu + 5 quiz
    Ô1   ĐÁP ÁN ÔN TẬP 1 — Khai trương xưởng (Đề chính)     ← 10-12 câu
    Ô1B  ĐÁP ÁN ĐỀ B                                        ← 10-12 câu

BA CHỖ PHẢI CẨN THẬN:

1. **Tiền tố dấu trang** (`B1  `, `Ô1B  `) đứng TRƯỚC chữ "ĐÁP ÁN" — mẫu neo
   `^ĐÁP ÁN BÀI` trượt sạch (bẫy 44 của chuẩn).

2. **`Quiz C1:` phải xét TRƯỚC `C1:`** — luật hẹp trước, luật rộng sau. Ngược lại
   thì mọi đáp án quiz bị ghi đè lên đáp án luyện tập cùng số (bẫy 6: đáp án ôn tập
   đè đáp án bài, 60 lời giải gắn sai câu ở lớp 2).

3. **Khoá phải mang mã bài**, không chỉ mã câu: cả bài, cả ôn tập, cả đề B đều đánh
   số lại từ `C1`. Khoá là `<mã bài>#<mã câu>`.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop4_tho.json')
RA = os.path.join(GOC_KHO, 'data', 'lop4_dapan.json')
TIEN_TO = 'DL:KSN4.'

R_DA_BAI = re.compile(r'^(?:\S+\s+)?ĐÁP ÁN BÀI (\d+)\s*[—–-]?\s*(.*)$')
R_DA_OT = re.compile(r'^(?:\S+\s+)?ĐÁP ÁN ÔN TẬP (\d+)\b')
R_DA_DEB = re.compile(r'^(?:\S+\s+)?ĐÁP ÁN ĐỀ B\b')
# hẹp trước
R_QUIZ = re.compile(r'^Quiz\s+C(\d+)\s*[:.]\s*(.+)$')
R_CAU = re.compile(r'^C(\d+)\s*[:.]\s*(.+)$')
R_DEB = re.compile(r'^B(\d+)\s*[:.]\s*(.+)$')


def ma_bai(so):
    return f'{TIEN_TO}B{so:02d}'


def main():
    tho = json.load(open(THO, encoding='utf-8'))

    dap = {}          # khoá → lời giải
    dem = {'bai': 0, 'quiz': 0, 'ontap': 0, 'deB': 0}
    for b in tho['bai']:
        # `cho` phải reset theo TỪNG đuôi chương. Để nó sống qua chương là câu HỎI
        # của đề B chương sau (`B1. Đọc số: 68 205.`) rơi đúng vào mẫu đáp án đề B
        # (`B1: …`) và ghi đè lời giải chương trước — đề thay chỗ đáp án, im lặng,
        # mà tổng vẫn tăng nên nhìn bảng tổng kết thấy "nhiều hơn" chứ không thấy sai.
        cho = None    # ('bai', so) | ('ontap', n) | ('deB', n)
        for t in b['sauBai']:
            m = R_DA_BAI.match(t)
            if m:
                cho = ('bai', int(m.group(1)))
                continue
            m = R_DA_OT.match(t)
            if m:
                cho = ('ontap', int(m.group(1)))
                continue
            if R_DA_DEB.match(t):
                # đề B luôn đứng ngay sau đề chính của CÙNG ôn tập
                cho = ('deB', cho[1] if cho and cho[0] == 'ontap' else 0)
                continue
            if not cho:
                continue

            if cho[0] == 'bai':
                q = R_QUIZ.match(t)
                if q:
                    dap[f'{ma_bai(cho[1])}#Q{q.group(1)}'] = q.group(2).strip()
                    dem['quiz'] += 1
                    continue
                c = R_CAU.match(t)
                if c:
                    dap[f'{ma_bai(cho[1])}#C{c.group(1)}'] = c.group(2).strip()
                    dem['bai'] += 1
                continue

            if cho[0] == 'ontap':
                c = R_CAU.match(t)
                if c:
                    dap[f'OT{cho[1]}#C{c.group(1)}'] = c.group(2).strip()
                    dem['ontap'] += 1
                continue

            if cho[0] == 'deB':
                c = R_DEB.match(t)
                if c:
                    dap[f'OT{cho[1]}#B{c.group(1)}'] = c.group(2).strip()
                    dem['deB'] += 1

    # ── CHỐT: khớp 1:1 với câu hỏi đã trích ở bước 1 ──
    loi = []
    for b in tho['bai']:
        for c in b['cau']:
            k = f"{ma_bai(b['so'])}#{c['id']}"
            if k not in dap:
                loi.append(f'thiếu đáp án {k} — {c["text"][:50]}')
    thua = [k for k in dap if k.startswith(TIEN_TO)
            and k not in {f"{ma_bai(b['so'])}#{c['id']}"
                          for b in tho['bai'] for c in b['cau']}]
    for k in thua:
        loi.append(f'đáp án {k} không có câu hỏi tương ứng')
    # Ôn tập: 11 bộ đề chính (10-12 câu) và 11 bộ đề B (10-12 câu). Ngoài ngưỡng ấy
    # nghĩa là mẫu vừa ăn nhầm phần khác — đúng cái vừa xảy ra với đề B.
    for n in range(1, 12):
        for phan, chu in (('C', 'đề chính'), ('B', 'đề B')):
            c = sum(1 for k in dap if k.startswith(f'OT{n}#{phan}'))
            if not 10 <= c <= 12:
                loi.append(f'ôn tập {n} {chu}: {c} đáp án (phải 10-12)')

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump({'tienTo': TIEN_TO, 'dapAn': dap}, f, ensure_ascii=False, indent=1)

    print(f'đã ghi {RA}')
    print(f"  bài: {dem['bai']} luyện tập + {dem['quiz']} quiz"
          f"  ·  ôn tập: {dem['ontap']} đề chính + {dem['deB']} đề B"
          f'  ·  tổng {len(dap)}')
    if loi:
        print(f'  ⚠ {len(loi)} chỗ lệch:')
        for x in loi[:20]:
            print('     ·', x)
        raise SystemExit(1)
    print('  ✓ chốt: mọi câu của 44 bài đều có đáp án, không câu nào thừa')


if __name__ == '__main__':
    main()
