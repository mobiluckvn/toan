# -*- coding: utf-8 -*-
"""
Chạy TRỌN dây chuyền LỚP 2, đúng thứ tự.

    python3 tools/lam_lop2.py

Sáu bước phải chạy liền nhau: trích thô → làm dễ hiểu → dựng dữ liệu → gắn hình
→ dựng bản khuôn chung (bản app đọc).
Chạy lẻ bước 3 mà quên bước 2 thì app hiện lại lời văn khó của sách gốc, mà không
có gì báo — cùng loại bẫy đã dính ở Quyển 2 lớp 5.

GẮN HÌNH PHẢI Ở CUỐI: bước 3 ghi đè trọn tệp bài học, nên gắn hình trước nó là
mất sạch hình mà dữ liệu vẫn hợp lệ và bài vẫn chạy — không có gì báo.
Riêng việc VẼ hình thì tách ra `tools/ve_hinh_lop2.py`, chạy khi sửa hình thôi,
vì vẽ tốn thời gian mà bản mô tả hình gần như không đổi theo lời văn.
"""
import subprocess, sys, os
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUOC = [
    ('trích thô từ .docx', 'rut_lop2.py'),
    ('làm lời văn dễ hiểu', 'de_hieu_lop2.py'),
    ('dựng dữ liệu bài học', 'chuan_lop2.py'),
    ('gắn hình vào bài', 'gan_hinh_lop2.py'),
    ('trích 8 ôn tập + 3 ải', 'rut_ontap_lop2.py'),
    ('dựng bản khuôn chung với lớp 5', 'dung_khuon_chung.py'),
]
for i, (ten, tep) in enumerate(BUOC, 1):
    print(f'── {i}/{len(BUOC)} · {ten}')
    r = subprocess.run([sys.executable, os.path.join(GOC, 'tools', tep)])
    if r.returncode:
        sys.exit(r.returncode)
print('\nxong — chạy `npm test` để cổng soi lại.')
