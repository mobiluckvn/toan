# -*- coding: utf-8 -*-
"""DỰNG VIDEO MỞ BÀI + BÀI GIẢNG cho Toán lớp 4.

    tools/tts/.venv/bin/python tools/video/dung_video_toan.py --loi   # gom lời cần đọc
    tools/tts/.venv/bin/python tools/video/dung_video_toan.py --bai DL_KSN4_B13
    tools/tts/.venv/bin/python tools/video/dung_video_toan.py --tat-ca

Bác chốt 14-08: mở bài và bài giảng phải thành video, không ẩn dụ, và **dùng đúng
cách tạo video như Tiếng Anh lớp 1**.

── DÙNG CHUNG, KHÔNG CHÉP BẢN THỨ HAI ──
Tệp này KHÔNG có khung vẽ riêng. Nó gọi thẳng `dung_video.khung()` và
`dung_video.dung()` — cùng phông, cùng màu, cùng cách ghép tiếng với hình mà 37
video Tiếng Anh đang dùng. Ba loại cảnh riêng của Toán (`de_toan` · `hinh_toan` ·
`y_toan`) đã thêm vào chính hàm `khung` ấy.

Chép một bộ dựng thứ hai thì hai bộ sớm muộn lệch nhau: sửa phông ở bên này, video
bên kia vẫn phông cũ, và không cổng nào bắt được vì cả hai đều dựng ra mp4 hợp lệ.
Đây đúng bài học của `hinh_ve.json` — một nguồn cho cả màn hình lẫn video.

── HAI BƯỚC, ĐỪNG GỘP ──
1. `--loi` gom mọi câu cần đọc ra một tệp, để `tools/tts/sinh_am.py` sinh clip.
2. `--bai` / `--tat-ca` mới dựng mp4, và nó ĐÒI clip phải có sẵn.
Gộp lại thì mỗi lần sửa một chữ là nạp lại model Kokoro ~1 GB.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

O = Path(__file__).resolve().parent
sys.path.insert(0, str(O))
import dung_video                                            # noqa: E402
import kich_ban_toan                                         # noqa: E402

GOC = O.parent.parent
NGUON = GOC / 'data' / 'lop4'
RA = GOC / 'web' / 'public' / 'content' / 'toan' / 'video'
SO_AM = GOC / 'web' / 'public' / 'content' / 'toan' / 'lop4_am.json'
LOI_CAN = GOC / 'data' / 'lop4_loi_video.json'

# Danh sách bài mặc định SUY TỪ KỊCH BẢN ĐÃ VIẾT, không gõ tay một dải số.
# Bản đầu gõ dải `range(13, 21)`. Rồi chương 3 viết thêm chín kịch bản mang mã
# B50 tới B54 và bốn mã cũ — không mã nào nằm trong dải ấy, nên chạy `--tat-ca`
# vẫn im lặng bỏ qua đúng chín bài vừa viết. Suy từ `BO` thì viết xong bài nào là
# bài ấy vào danh sách, không phải nhớ nới dải.
BAI_MAC_DINH = sorted(m.replace('DL:', 'DL_').replace('.', '_')
                      for m in kich_ban_toan.BO)


def ds_bai(a) -> list[str]:
    if a.bai:
        return [a.bai]
    if a.tat_ca:
        # ⚠ `--tat-ca` KHÔNG phải là "mọi tệp bài". Bản cũ quét cả thư mục nguồn,
        # nên nó chết ngay ở B01 — bài chưa viết kịch bản video. Chưa đợt nào dựng
        # nổi bằng cờ này, mà cờ thì vẫn nằm trong phần hướng dẫn đầu tệp.
        # "Tất cả" ở đây nghĩa là mọi bài ĐÃ CÓ KỊCH BẢN, đúng như khi không có cờ.
        return BAI_MAC_DINH
    return BAI_MAC_DINH


def gom_loi(mas: list[str]) -> list[dict]:
    """Mọi câu cần đọc, mỗi câu một dòng, KHÔNG trùng.

    Cùng hình dạng với `data/tienganh/lop1_loi.json` để dùng chung `sinh_am.py`:
    `{id, chu, tieng}`. Tất cả đều `vi` — bài Toán không có câu tiếng Anh nào."""
    thay, ra = set(), []
    for ma in mas:
        for c in kich_ban_toan.kich_ban(ma)['canh']:
            for chu, tieng in c['loiAm']:
                i = kich_ban_toan.ma_am(chu)
                if i in thay:
                    continue
                thay.add(i)
                ra.append({'id': i, 'chu': chu, 'tieng': tieng})
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--bai')
    p.add_argument('--tat-ca', action='store_true')
    p.add_argument('--loi', action='store_true', help='gom lời cần đọc rồi dừng')
    a = p.parse_args()
    mas = ds_bai(a)

    if a.loi:
        ds = gom_loi(mas)
        LOI_CAN.write_text(json.dumps(ds, ensure_ascii=False, indent=1) + '\n', 'utf8')
        print(f'{len(ds)} dòng cần sinh âm → {LOI_CAN.relative_to(GOC)}')
        return 0

    if not SO_AM.exists():
        sys.exit(f'chưa có sổ tra âm {SO_AM.relative_to(GOC)} — chạy --loi rồi sinh âm trước')
    so = json.loads(SO_AM.read_text('utf8'))
    # `dung_video` tra clip trong thư mục AUDIO của nó; trỏ sang thư mục của Toán.
    dung_video.AUDIO = GOC / 'web' / 'public' / 'content' / 'toan' / 'audio'

    tong = 0.0
    for ma in mas:
        kb = kich_ban_toan.kich_ban(ma)
        tt = dung_video.dung(ma, RA / kb['tep'], kb['canh'], so)
        print(f"  ✓ {kb['tep']}  {len(kb['canh']):2} cảnh · {tt['giay']:5.1f}s "
              f"· {tt['mb']:.2f} MB")
        tong += tt['giay']
    print(f'\n{len(mas)} video · tổng {tong / 60:.1f} phút → {RA.relative_to(GOC)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
