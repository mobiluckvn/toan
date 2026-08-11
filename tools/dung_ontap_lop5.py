#!/usr/bin/env python3
"""Dựng `lessons/ontap.json` cho lớp 5 — danh mục kỳ sát hạch từng chương.

VÌ SAO CẦN: lớp 2·3·4 đều có sẵn `<quyển>/ontap.json` liệt kê các kỳ ôn tập và ba
cửa ải, nên màn trang chính của quyển đọc từ đó. Lớp 5 thì không có tệp nào — 14 kỳ
sát hạch nằm rải trong `reviews/DCR_KSN5Q1_C*.json`, và màn Home cũ dựng danh sách
bằng `Array.from({length: 14})` gõ cứng ngay trong JSX.

Gõ cứng thì trang chính của lớp 5 và của lớp 2 không bao giờ gộp làm một được. Dựng
tệp danh mục cho lớp 5 là bốn quyển cùng một hình dạng dữ liệu, cùng một màn hình.

`need` lấy từ `passRule` ("đạt 12/15 → huy hiệu…"), không gõ tay: ExamPlayer vốn đã
lùi về 12 khi thiếu, mà 12 chỉ đúng với những chương có 15 câu.

Chạy: python3 tools/dung_ontap_lop5.py
"""
import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NGUON = GOC / 'data' / 'reviews'
# KHÔNG đặt trong `lessons/`: thư mục ấy chỉ chứa BÀI HỌC, và bốn phép kiểm quét
# nó bằng `*.json` rồi đọc thẳng `j.id` — thả một tệp danh mục vào là cả bốn vỡ.
# Sổ đăng ký khai đường dẫn qua `tepOnTap`, nên chỗ đặt không cần theo quy ước.
DICH = [GOC / 'data' / 'ontap_lop5.json',
        GOC / 'web' / 'public' / 'content' / 'ontap_lop5.json']

SO_CHUONG = 14


def doc_nguong(doc, so_cau):
    """Số câu đúng tối thiểu để qua kỳ — đọc từ passRule, thiếu thì lấy 4/5."""
    m = re.search(r'đạt\s+(\d+)\s*/\s*(\d+)', doc.get('passRule') or '')
    if m and int(m.group(2)) == so_cau:
        return int(m.group(1))
    if m:
        # Ngưỡng khai theo một lô đề khác — co lại theo đúng tỉ lệ của lô này.
        return max(1, round(so_cau * int(m.group(1)) / int(m.group(2))))
    return max(1, round(so_cau * 4 / 5))


def main():
    ra = []
    for c in range(1, SO_CHUONG + 1):
        p = NGUON / f'DCR_KSN5Q1_C{c}.json'
        if not p.exists():
            raise SystemExit(f'thiếu {p}')
        doc = json.loads(p.read_text(encoding='utf-8'))
        so_cau = len(doc.get('examA') or [])
        ra.append({
            'id': doc['id'],
            'chapter': doc.get('chapter', c),
            'loai': 'ontap',
            'so': c,
            'name': doc.get('name') or f'KỲ SÁT HẠCH CHƯƠNG {c}',
            'soCau': so_cau,
            'need': doc_nguong(doc, so_cau),
        })

    for d in DICH:
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_text(json.dumps(ra, ensure_ascii=False, indent=1) + '\n',
                     encoding='utf-8')
    print(f'{len(ra)} kỳ sát hạch → ' + ' · '.join(str(d.relative_to(GOC)) for d in DICH))
    print('   câu: ' + ' '.join(f"C{o['so']}={o['soCau']}/{o['need']}" for o in ra))


if __name__ == '__main__':
    main()
