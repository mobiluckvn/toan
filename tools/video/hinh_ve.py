#!/usr/bin/env python3
"""
BẢY HÌNH VẼ TAY, DỰNG THÀNH ẢNH CHO VIDEO.

Đọc ĐÚNG tệp mà màn hình đang đọc — `web/src/mon/tienganh/lib/hinh_ve.json`. Đây
là điểm chính của cả tệp này: không vẽ lại bằng Pillow.

Vẽ lại thì thành hai bản của cùng một cái cổng, và hai bản thì sớm muộn cũng
lệch. Lệch kiểu ấy không cổng nào bắt được — bản dựng xanh, video chạy, chỉ có bé
là thấy cái cổng trên màn hình khác cái cổng trong video, rồi không chắc mình đã
học đúng từ nào.

`figforge` không thay được: nó dựng sơ đồ toán bằng matplotlib, không rasterize
SVG. Ở đây dùng `cairosvg` (cài trong `tools/tts/.venv`).
"""
import io
import json
from functools import lru_cache
from pathlib import Path

import cairosvg
from PIL import Image

GOC = Path(__file__).resolve().parent.parent.parent
NGUON = GOC / 'web' / 'src' / 'mon' / 'tienganh' / 'lib' / 'hinh_ve.json'


@lru_cache(maxsize=1)
def _kho():
    with open(NGUON, encoding='utf-8') as f:
        return json.load(f)


def co_hinh(khoa: str) -> bool:
    return bool(khoa) and khoa in _kho().get('hinh', {})


@lru_cache(maxsize=64)
def anh(khoa: str, co: int = 320) -> Image.Image:
    """
    Ảnh RGBA của một hình vẽ tay, cạnh `co` điểm ảnh.

    Dựng ở đúng cỡ cần dùng chứ không dựng to rồi thu nhỏ: SVG là vector nên
    rasterize thẳng ở cỡ đích cho nét sắc hơn, và cũng nhanh hơn.
    """
    v = _kho()['hinh'][khoa]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="{_kho()["_khungNhin"]}">{v["than"]}</svg>')
    png = cairosvg.svg2png(bytestring=svg.encode('utf-8'),
                           output_width=co, output_height=co)
    return Image.open(io.BytesIO(png)).convert('RGBA')


def dan(im: Image.Image, khoa: str, tam_x: int, tam_y: int, co: int) -> bool:
    """Dán hình vào khung, canh giữa theo `tam_x`/`tam_y`. Trả False nếu không có hình."""
    if not co_hinh(khoa):
        return False
    h = anh(khoa, co)
    # PASTE có mặt nạ, KHÔNG alpha_composite: khung của bộ dựng là ảnh "RGB"
    # (nền đặc), mà alpha_composite đòi cả hai bên đều RGBA — gọi thẳng là ném lỗi
    # giữa lúc dựng, sau khi đã tốn công rasterize cả bộ.
    im.paste(h, (int(tam_x - co / 2), int(tam_y - co / 2)), h)
    return True


if __name__ == '__main__':
    kho = _kho()['hinh']
    print(f'{NGUON.relative_to(GOC)} · {len(kho)} hình')
    for k, v in kho.items():
        a = anh(k, 256)
        dac = sum(1 for p in a.getdata() if p[3] > 20)
        print(f'  {k:6s} {v["ten"]:10s} → {dac:6d} điểm ảnh có màu')
