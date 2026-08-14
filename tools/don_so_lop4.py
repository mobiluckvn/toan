#!/usr/bin/env python3
"""DỒN SỐ BÀI LỚP 4 — nhường năm chỗ cho cụm DÃY SỐ mới.

    python3 tools/don_so_lop4.py --thu      # chạy THỬ, chỉ in ra, không sửa gì
    python3 tools/don_so_lop4.py --that     # sửa thật

    B13 → B18 · B14 → B19 · … · B44 → B49        (31 bài, dồn xuống 5 chỗ)

── VÌ SAO PHẢI DỒN ──
Bác chốt 14-08: tách "dãy số cách đều" thành năm bài (khái niệm → thứ n → đếm →
tổng → thuộc dãy), và **đánh số lại cho liền mạch** để số hiệu bài khớp đúng thứ tự
học. Năm bài mới chiếm B13–B17, nên mọi bài từ B13 cũ trở đi phải lùi 5 chỗ.

── VÌ SAO PHẢI CÓ TỆP NÀY, KHÔNG SỬA TAY ──
Mã bài lớp 4 nằm rải trong **353 tệp**: bài học, ma trận tri thức, ôn tập, ô nhập
đáp án, sổ đăng ký, sổ tay hình, mô tả hình, TÊN 92 TỆP PNG, và cả bài lớp 5 (chúng
trỏ ngược về lớp 4 làm đường lui). Sửa tay thì chắc chắn sót, mà sót ở đây là bé bấm
"học lại bài lớp dưới" rồi lạc sang một bài chẳng liên quan.

── ĐI TỪ SỐ LỚN XUỐNG SỐ NHỎ ──
B44→B49 trước, B43→B48 sau… Làm ngược lại (13 trước) thì B13→B18 xong, tới lượt
B18 cũ lại bị đổi thành B23 — dồn hai lần, sai toàn bộ. Đây là lỗi kinh điển của
mọi phép đánh số lại.

── KHÔNG ĐỤNG TỚI ──
· `data/lop4/DL_KSN4_B01..B12` và mọi tham chiếu tới chúng — chưa tới lượt dồn.
· Mã bài của quyển khác (KSN2 · KSN3 · KSN5 · TA1) — mẫu tìm có neo `KSN4`.
· Tiến độ học của các bé: việc ấy do `chung/lib/donSoLop4.js` lo lúc nạp sổ.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
DICH = 5                     # lùi 5 chỗ
TU, DEN = 13, 44             # dải bài phải dồn

BO_QUA = {'.git', 'node_modules', 'dist', '.venv', '__pycache__',
          'Kokoro-Vietnamese', 'tool-results'}
DUOI = {'.json', '.js', '.jsx', '.mjs', '.py', '.md'}

# ⚠ HAI TỆP PHẢI ĐỨNG NGOÀI, và đây là chỗ chạy thử đã cứu.
# `day_so_lop4.py` là nơi SINH RA năm bài mới B13–B17. Để nó vào diện dồn thì năm
# bài ấy bị đẩy thành B18–B22 — tức là công cụ tự đẩy chính cái nó vừa tạo, và đè
# lên đúng những bài vừa dồn tới đó. Chạy thử in ra "46 chỗ đổi mã" ở tệp này mới
# lộ. `settings.local.json` chỉ là bộ nhớ quyền của công cụ, đổi vào đó là nhiễu.
DUNG_DUNG = {'tools/day_so_lop4.py', 'tools/don_so_lop4.py',
             '.claude/settings.local.json'}

# `KSN4.B13` (mã bài) · `KSN4_B13` (tên tệp) · `L4H_B13` (mã hình) · `B13 ②` (mục `goc`)
MAU = re.compile(r'(KSN4[._]B|L4H_B)(\d{2})')


def moi(n: int) -> int:
    return n + DICH


def doi_chu(s: str) -> tuple[str, int]:
    """Đổi mọi mã bài trong một chuỗi. Trả về (chuỗi mới, số chỗ đã đổi)."""
    dem = 0

    def thay(m):
        nonlocal dem
        n = int(m.group(2))
        if not (TU <= n <= DEN):
            return m.group(0)
        dem += 1
        return f'{m.group(1)}{moi(n):02d}'

    return MAU.sub(thay, s), dem


def tep_can_soi():
    for p in GOC.rglob('*'):
        if not p.is_file() or any(x in p.parts for x in BO_QUA):
            continue
        if p.suffix in DUOI and str(p.relative_to(GOC)) not in DUNG_DUNG:
            yield p


def sua_so_trong_bai(p: Path, s: str) -> str:
    """Bài học lớp 4 còn có trường `so` và tên "Bài n · …" — mẫu chữ ở trên không
    bắt được hai chỗ ấy vì chúng là SỐ TRẦN, không có tiền tố `KSN4.B`."""
    # CHỈ bản gốc `data/lop4`. Bản dựng `web/public/content/lop4` có khoá khác
    # (`title` chứ không `ten`) và dù sao cũng sẽ được sinh lại — sửa ở đó là sửa
    # bản dựng, đúng cái bẫy đã dính hai lần trong tuần này.
    if p.parent != GOC / 'data' / 'lop4' or not p.name.startswith('DL_KSN4_B'):
        return s
    d = json.loads(s)
    cu = int(re.search(r'B(\d{2})', d['id']).group(1))
    d['so'] = cu
    d['ten'] = re.sub(r'^Bài \d+ · ', f'Bài {cu} · ', d['ten'])
    return json.dumps(d, ensure_ascii=False, indent=1) + '\n'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--thu', action='store_true')
    p.add_argument('--that', action='store_true')
    a = p.parse_args()
    if not (a.thu or a.that):
        p.error('cần --thu (chạy thử) hoặc --that (sửa thật)')

    ban = subprocess.run(['git', 'status', '--porcelain'], cwd=GOC,
                         capture_output=True, text=True).stdout.strip()
    if a.that and ban:
        print('⚠ cây làm việc CHƯA SẠCH. Dồn số đụng hàng trăm tệp, nên phải commit')
        print('  hoặc dọn trước để còn `git checkout .` khi cần lùi lại:')
        print('\n'.join('   ' + x for x in ban.splitlines()[:12]))
        sys.exit(1)

    # ── 1 · đổi chữ trong tệp ──
    doi_tep, tong = [], 0
    for f in tep_can_soi():
        try:
            s = f.read_text('utf8')
        except UnicodeDecodeError:
            continue
        moi_s, n = doi_chu(s)
        if not n:
            continue
        moi_s = sua_so_trong_bai(f, moi_s)
        doi_tep.append((f, n))
        tong += n
        if a.that:
            f.write_text(moi_s, 'utf8')

    # ── 2 · đổi TÊN tệp: bài học lớp 4 và 92 hình PNG ──
    # Đi từ số LỚN xuống, nếu không B13→B18 sẽ đè lên B18 cũ chưa kịp dời.
    doi_ten = []
    for n in range(DEN, TU - 1, -1):
        for thu, mau_ten in ((GOC / 'data/lop4', f'DL_KSN4_B{n:02d}.json'),):
            cu = thu / mau_ten
            if cu.exists():
                doi_ten.append((cu, thu / mau_ten.replace(f'B{n:02d}', f'B{moi(n):02d}')))
        hinh = GOC / 'web/public/content/figures'
        for cu in sorted(hinh.glob(f'L4H_B{n:02d}_*.png')):
            doi_ten.append((cu, hinh / cu.name.replace(f'B{n:02d}_', f'B{moi(n):02d}_')))
    if a.that:
        for cu, ra in doi_ten:
            shutil.move(str(cu), str(ra))

    print(f"{'THỬ' if a.thu else 'ĐÃ SỬA'} · {len(doi_tep)} tệp · {tong} chỗ đổi mã "
          f"· {len(doi_ten)} tệp đổi tên")
    print()
    lon = sorted(doi_tep, key=lambda x: -x[1])[:12]
    for f, n in lon:
        print(f'   {n:4} chỗ  {f.relative_to(GOC)}')
    print(f'   … và {len(doi_tep) - len(lon)} tệp khác')
    print()
    print('   đổi tên, vài ví dụ:')
    for cu, ra in (doi_ten[:3] + doi_ten[-3:]):
        print(f'     {cu.name}  →  {ra.name}')

    if a.thu:
        print('\n(--thu: chưa sửa gì. Chạy --that để làm thật.)')


if __name__ == '__main__':
    main()
