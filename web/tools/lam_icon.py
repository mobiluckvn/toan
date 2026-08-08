# -*- coding: utf-8 -*-
"""
Sinh bộ icon của trang từ icon/icon.jpg.

    python3 web/tools/lam_icon.py       # chạy từ đâu cũng được

Ảnh gốc là JPG 576×576 có nền trắng và bóng xám ở mép, lề lại lệch (trái 70px,
trên 12px). Cắt sát phần CÓ MÀU rồi đặt lại vào khung vuông với lề đều 6%, nếu
không icon trên màn hình chính điện thoại sẽ lệch hẳn sang một bên.

Đổi ảnh gốc thì chạy lại lệnh này, rồi `npm run build`.
"""
import os
from PIL import Image

# Đường dẫn tính từ VỊ TRÍ TỆP NÀY, không tính từ thư mục đang đứng — chạy từ
# web/ hay từ gốc kho mã đều ra cùng kết quả.
GOC_KHO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GOC = os.path.join(GOC_KHO, 'icon', 'icon.jpg')
RA = os.path.join(GOC_KHO, 'web', 'public')
CO = [(16, 'icon/favicon-16.png'), (32, 'icon/favicon-32.png'),
      (180, 'icon/apple-touch-icon.png'), (192, 'icon/icon-192.png'),
      (512, 'icon/icon-512.png')]


def khung_co_mau(im, nguong=30):
    """Khung bao phần có SẮC MÀU — bỏ nền trắng lẫn bóng xám (xám thì R≈G≈B)."""
    px, (w, h) = im.load(), im.size
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y][:3]
            if max(r, g, b) - min(r, g, b) > nguong:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def main():
    src = Image.open(GOC).convert('RGBA')
    cut = src.crop(khung_co_mau(src))
    cw, ch = cut.size
    canh = max(cw, ch)
    le = int(canh * 0.06)
    nen = Image.new('RGBA', (canh + 2 * le, canh + 2 * le), (255, 255, 255, 255))
    nen.paste(cut, (le + (canh - cw) // 2, le + (canh - ch) // 2), cut)

    for n, ten in CO:
        p = os.path.join(RA, ten)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        nen.resize((n, n), Image.LANCZOS).convert('RGB').save(p, optimize=True)
        print(f'  {ten:28s} {n}px')
    ico = os.path.join(RA, 'favicon.ico')
    nen.resize((48, 48), Image.LANCZOS).convert('RGB').save(
        ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print(f'  {"favicon.ico":28s} 16/32/48px')


if __name__ == '__main__':
    main()
