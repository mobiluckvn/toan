# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 2 — làm lời văn dễ hiểu cho trẻ 7-8 tuổi.

    python3 tools/de_hieu_lop2.py

HAI MỨC CAN THIỆP, cố ý tách bạch:

  1. NGẮT CÂU (máy làm, KHÔNG đổi một chữ nào)
     Câu dài trong sách hay nối nhiều ý bằng dấu ; và —. Ngắt ở đó thành câu ngắn
     là đủ ngắn cho 46% số câu khó, mà nghĩa không xê dịch mảy may. An toàn tuyệt
     đối nên làm trước.

  2. VIẾT LẠI (người viết tay, có bảng đối chiếu)
     Chỉ dùng cho những câu ngắt xong vẫn khó. Mỗi câu viết lại đều ghi rõ bản gốc
     để đối chiếu — VIẾT LẠI LỜI VĂN, KHÔNG ĐỔI TOÁN.

Bản gốc luôn được giữ trong `goc` để so lại bất cứ lúc nào.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'data', 'lop2_tho.json')
RA = os.path.join(GOC_KHO, 'data', 'lop2_dehieu.json')

TOI_DA = 20          # số chữ tối đa một câu cho trẻ lớp 2

# ── Bảng viết tay: bản gốc → bản cho con. Chỉ đổi CÁCH NÓI, giữ nguyên con số. ──
VIET_LAI = {
 "Mỗi số có 3 chữ số sống trong một ngôi nhà có 3 phòng: phòng TRĂM (to nhất, bên trái) → phòng CHỤC (ở giữa) → phòng ĐƠN VỊ (bên phải).":
   "Số có 3 chữ số ở trong một ngôi nhà 3 phòng. Bên trái là phòng TRĂM. Ở giữa là phòng CHỤC. Bên phải là phòng ĐƠN VỊ.",

 "Nhìn vào từng phòng, ta biết mỗi chữ số đáng giá bao nhiêu: chữ số 2 ở phòng trăm đáng giá 200; chữ số 4 ở phòng chục đáng giá 40; chữ số 5 ở phòng đơn vị đáng giá đúng 5.":
   "Mỗi chữ số đáng giá bao nhiêu là do phòng của nó. Số 2 ở phòng trăm đáng 200. Số 4 ở phòng chục đáng 40. Số 5 ở phòng đơn vị đáng 5.",

 "Trên Phố Số Nhà, con để ý một điều hay: một bên đường toàn nhà LẺ (1, 3, 5, 7, 9), bên kia toàn nhà CHẴN (2, 4, 6, 8, 10) — giống phố thật ngoài đời đấy!":
   "Ở phố thật cũng vậy: một bên đường là nhà số LẺ 1, 3, 5, 7, 9. Bên kia là nhà số CHẴN 2, 4, 6, 8, 10.",

 "Hai số có đuôi cộng lại bằng 10 sẽ tạo thành đôi bạn tròn chục: đuôi 6 với đuôi 4, đuôi 8 với đuôi 2, đuôi 5 với đuôi 5, đuôi 1 với đuôi 9...":
   "Hai số có đuôi cộng lại bằng 10 thì thành một đôi bạn. Đuôi 6 đi với đuôi 4. Đuôi 8 đi với đuôi 2. Đuôi 1 đi với đuôi 9.",

 "Con để ý cột \"hơn nhau\" đi từ 8 → 6 → 4 → 2 → 0: mỗi lần chuyển 1 viên từ người nhiều sang người ít, phần hơn giảm đi 2 (một bên bớt 1, một bên thêm 1).":
   "Con nhìn cột \"hơn nhau\": 8 → 6 → 4 → 2 → 0. Mỗi lần chuyển 1 viên, phần hơn giảm 2. Vì một bên bớt 1 viên, bên kia thêm 1 viên.",

 "Trong họ tứ giác có hai nhân vật nổi tiếng: HÌNH CHỮ NHẬT (hai cạnh dài bằng nhau, hai cạnh ngắn bằng nhau) và HÌNH VUÔNG (cả 4 cạnh bằng chằn chặn — em ruột đặc biệt nhất họ).":
   "Hình có 4 cạnh thì có hai bạn quen nhất. HÌNH CHỮ NHẬT có hai cạnh dài bằng nhau và hai cạnh ngắn bằng nhau. HÌNH VUÔNG có cả 4 cạnh bằng nhau.",

 "Giả sử cả ngày chỉ bán được 2 cốc = 8 nghìn, mà vốn những 10 nghìn → thu về ít hơn bỏ ra → bị LỖ 10 − 8 = 2 nghìn.":
   "Nếu cả ngày chỉ bán được 2 cốc thì thu về 8 nghìn. Mà tiền bỏ ra là 10 nghìn. Thu ít hơn bỏ ra nên bị LỖ 10 − 8 = 2 nghìn.",

 "MẸO THÁM TỬ: Gặp bài đếm chân, con cứ nhớ 3 nhịp: VẼ ĐẦU → GẮN 2 CHÂN CHO TẤT CẢ → CHÂN THỪA ĐEM GẮN TIẾP CHO CON 4 CHÂN.":
   "MẸO: bài đếm chân làm theo 3 bước. Một là vẽ đủ số đầu. Hai là gắn 2 chân cho tất cả. Ba là chân còn thừa thì gắn thêm cho con 4 chân.",

 "MẸO THÁM TỬ: Gặp chữ \"gấp mấy lần\" là nghĩ ngay đến PHẦN: vẽ khối → đếm tổng số phần → chia tổng cho số phần → trả về từng người.":
   "MẸO: thấy chữ \"gấp mấy lần\" thì nghĩ đến PHẦN. Vẽ các khối. Đếm xem có tất cả mấy phần. Lấy tổng chia cho số phần. Rồi trả về cho từng người.",

 "Nhớ hai luật: (1) máy nào số đi qua SAU CÙNG thì mình lùi qua ĐẦU TIÊN — giống buổi sáng con mặc áo rồi mới khoác ba lô, thì lúc về phải tháo ba lô trước rồi mới cởi áo; (2) mỗi máy phải đảo thành máy ngược (Bài 14): × 2 thành : 2, + 3 thành − 3.":
   "Nhớ hai điều. Một: máy nào làm SAU CÙNG thì mình đi lùi qua ĐẦU TIÊN. Giống như cởi ba lô trước rồi mới cởi áo. Hai: mỗi máy phải làm ngược lại. Máy × 2 thành máy : 2. Máy + 3 thành máy − 3.",
}


def cau_cua(doan):
    return [c.strip() for c in re.split(r'(?<=[.!?…])\s+', doan) if c.strip()]


def ngat(c):
    """Ngắt câu dài ở ; và — . Không đổi chữ nào."""
    ph = [p.strip() for p in re.split(r'\s*;\s*|\s+—\s+', c) if p.strip()]
    if len(ph) < 2:
        return [c]
    ra = []
    for i, p in enumerate(ph):
        if not re.search(r'[.!?…:]$', p) and i < len(ph) - 1:
            p += '.'
        ra.append(p[0].upper() + p[1:] if i and p[:1].islower() else p)
    return ra


def de_hieu(doan):
    """Trả (đoạn đã dễ hơn, số câu đã viết tay lại)."""
    ra, tay = [], 0
    for c in cau_cua(doan):
        if c in VIET_LAI:
            ra.append(VIET_LAI[c]); tay += 1; continue
        ra.extend(ngat(c) if len(c.split()) > TOI_DA else [c])
    return ' '.join(ra), tay


def main():
    B = json.load(open(NGUON, encoding='utf-8'))
    CON = set(B['conDoc'])
    doi_dong = tay_tong = 0

    for b in B['bai']:
        for k, v in b['muc'].items():
            if k not in CON:
                continue
            moi = []
            for d in v['dong']:
                m, t = de_hieu(d)
                tay_tong += t
                if m != d:
                    doi_dong += 1
                moi.append(m)
            v['goc'] = v['dong']          # giữ bản gốc để đối chiếu
            v['dong'] = moi

    # Bảng viết tay khớp theo NGUYÊN VĂN. Sách sửa một dấu phẩy là không khớp nữa,
    # và câu ấy im lặng giữ nguyên bản khó — nên phải báo ngay, đừng để trôi.
    if tay_tong != len(VIET_LAI):
        khop = set()
        for b2 in B['bai']:
            for k2, v2 in b2['muc'].items():
                if k2 in CON:
                    for d2 in v2['goc']:
                        for c2 in cau_cua(d2):
                            if c2 in VIET_LAI:
                                khop.add(c2)
        thieu = [c for c in VIET_LAI if c not in khop]
        print(f'  ⚠ {len(thieu)}/{len(VIET_LAI)} câu viết tay KHÔNG khớp bản gốc:')
        for c in thieu:
            print(f'     {c[:96]}…')

    B['dehieu'] = {'toiDa': TOI_DA, 'soDongDoi': doi_dong, 'soCauVietTay': tay_tong,
                   'soCauDinhVietTay': len(VIET_LAI)}
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(B, f, ensure_ascii=False, indent=1)

    print(f'đã ghi {RA}')
    print(f'  đoạn có thay đổi: {doi_dong} · câu viết lại bằng tay: {tay_tong}')


if __name__ == '__main__':
    main()
