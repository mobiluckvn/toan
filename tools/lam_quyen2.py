# -*- coding: utf-8 -*-
"""
Chạy TRỌN dây chuyền Quyển 2, ĐÚNG THỨ TỰ.

    python3 tools/lam_quyen2.py

Vì sao cần một lệnh: chuan_quyen2.py dựng lại các tệp khối TỪ ĐẦU, nên nếu chạy nó
sau ve_so_do_q2.py thì phần `soDo` vừa gắn bị xoá sạch — dữ liệu vẫn hợp lệ, bài
vẫn chạy, chỉ mất hết sơ đồ mà không có gì báo. Đã dính đúng lỗi này một lần; bộ
kiểm bắt được, nhưng tốt hơn là đừng để xảy ra.
"""
import subprocess, sys, os

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUOC = [
    ('rút bản thô từ .docx', 'rut_quyen2.py'),
    ('rút bảng sơ đồ', 'rut_so_do_q2.py'),
    ('dựng dữ liệu bài học', 'chuan_quyen2.py'),
    ('vẽ sơ đồ & gắn vào khối', 've_so_do_q2.py'),      # PHẢI chạy sau cùng
]

for i, (ten, tep) in enumerate(BUOC, 1):
    print(f'── {i}/{len(BUOC)} · {ten}')
    r = subprocess.run([sys.executable, os.path.join(GOC, 'tools', tep)])
    if r.returncode:
        print(f'   dừng: {tep} lỗi'); sys.exit(r.returncode)
print('\nxong — nhớ chạy `npm test` để cổng nghiệm thu soi lại.')
