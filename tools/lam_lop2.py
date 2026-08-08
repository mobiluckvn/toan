# -*- coding: utf-8 -*-
"""
Chạy TRỌN dây chuyền LỚP 2, đúng thứ tự.

    python3 tools/lam_lop2.py

Ba bước phải chạy liền nhau: trích thô → làm dễ hiểu → dựng dữ liệu bài học.
Chạy lẻ bước 3 mà quên bước 2 thì app hiện lại lời văn khó của sách gốc, mà không
có gì báo — cùng loại bẫy đã dính ở Quyển 2 lớp 5.
"""
import subprocess, sys, os
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for i, (ten, tep) in enumerate([
        ('trích thô từ .docx', 'rut_lop2.py'),
        ('làm lời văn dễ hiểu', 'de_hieu_lop2.py'),
        ('dựng dữ liệu bài học', 'chuan_lop2.py')], 1):
    print(f'── {i}/3 · {ten}')
    r = subprocess.run([sys.executable, os.path.join(GOC, 'tools', tep)])
    if r.returncode:
        sys.exit(r.returncode)
print('\nxong — chạy `npm test` để cổng soi lại.')
