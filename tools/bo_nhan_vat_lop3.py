#!/usr/bin/env python3
"""BỎ NHÂN VẬT THƯƠNG HIỆU KHỎI QUYỂN LỚP 3.

    chạy:  python3 tools/bo_nhan_vat_lop3.py          (sửa data/lop3/*.json tại chỗ)
           python3 tools/bo_nhan_vat_lop3.py --thu    (chỉ in ra, không ghi)

── VÌ SAO ──

Lớp 2 và lớp 4 đã bỏ hẳn nhân vật; lớp 3 là quyển cuối còn giữ Su Kem · Su Bống ·
Trí Long, 267 chỗ. Bác chốt 16-08-2026: bỏ hẳn khỏi cả quyển, bốn quyển một giọng.

── HAI VAI, HAI LỐI XỬ — ĐỪNG GỘP ──

Thay máy móc một-đổi-một hỏng ngay tiếng Việt, đã thử:

    "Bố Su Kem 38 tuổi. Hỏi khi Su Kem 15 tuổi thì bố bao nhiêu tuổi?"
        → "Bố bạn ấy 38 tuổi. Hỏi khi bạn ấy 15 tuổi…"     ← không ai nói thế
    "Anh Trí Dũng hơn Trí Long mấy tuổi? Su Kem hơn Su Bống mấy tuổi?"
        → "Anh Trí Dũng hơn bạn ấy mấy tuổi? bạn ấy hơn em nhỏ mấy tuổi?"

Vì nhân vật ở lớp 3 gánh HAI vai khác hẳn nhau:

  ① NGƯỜI TRONG ĐỀ TOÁN — "Bố Su Kem 38 tuổi", "Su Bống gấp 6 con hạc". Đây là
     chủ ngữ, thay bằng đại từ là vỡ câu. Thay bằng TÊN BẠN NHỎ THƯỜNG, đúng như
     lớp 2 và lớp 4 vẫn làm: hai quyển ấy đầy Bình · An · Mai · Lan · Nam · Hoa ·
     Minh · Cường. Bỏ nhân vật KHÔNG có nghĩa là bỏ tên người khỏi đề toán — nó
     có nghĩa là bỏ cái vỏ truyện riêng của quyển.

  ② NGƯỜI LÀM SAI — "Trí Long viết vèo một cái: 372! Xong trước cả lớp!". Chỗ này
     lớp 4 cố ý KHÔNG gọi tên: "Có bạn đọc số 24 358 là…". Gọi đích danh một đứa
     trẻ rồi bảo nó sai là chuyện khác hẳn với kể một cái sai thường gặp. Nên ở
     `misconceptions` và màn bẫy, dùng lối giấu tên của lớp 4.

Cùng một cái tên, ở ô này thành `Nam`, ở ô kia thành `Có bạn` — nên bộ này phải đi
theo TÊN TRƯỜNG, không thể quét một lượt cả tệp.

── TÊN CHỌN THEO DÀN CÓ SẴN ──

Lấy đúng tên đã dùng ở lớp 2 và lớp 4 để bốn quyển chung một dàn nhân vật vô danh,
và giữ nguyên VAI để đề toán không đổi nghĩa (Su Bống là em, nên tên thay cũng phải
đọc ra là em).

`Trí Dũng` và `Ngọc Anh` GIỮ NGUYÊN: đó là tên người Việt bình thường, không nằm
trong vỏ truyện, không có trong `TU_CAM`. Bỏ cả những tên ấy là dọn quá tay.
"""
import argparse
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
DATA = GOC / 'data/lop3'

# Mọi tệp nguồn khác của quyển. `lop3_tho.json` KHÔNG có trong danh sách: đó là bản
# trích thô từ sách, cố ý giữ nguyên văn để còn đối chiếu được với sách giấy. Bộ này
# được gọi ở CUỐI `chuan_lop3.py`, nên chạy lại dây chuyền vẫn sạch.
TEP_KHAC = [
    'data/lop3_ontap.json',
    'data/lop3_dapan.json',
    'data/lop3_dapan_tay.json',
    'data/lop3_dapan_o.json',
    # ── CỬA THỨ NĂM: SỔ HÌNH ──
    # `gan_hinh_lop3.py` chép `caption` từ hai tệp này NGƯỢC vào `data/lop3/*.json`,
    # và nó chạy SAU bước dọn. Nên dọn xong, quét ra 0, rồi chạy lại dây chuyền một
    # lượt là lời chú hình mang tên cũ quay về — "Ba thanh: Su Bống 6 con, Su Kem
    # gấp đôi…". Cùng dòng họ với cửa lời chào và cửa gợi ý tay: tệp nằm ngoài thư
    # mục quyển, được một bước sau ghi đè vào.
    'data/lop3_hinh.json',
    'data/lop3_hinh_manifest.json',
]

# ── LỜI CHÀO · TỆP DÙNG CHUNG BỐN QUYỂN ──
#
# `data/loi_chao.json` giữ 203 lời chào của CẢ BỐN quyển trong một tệp phẳng, khoá
# là mã bài. Nó nằm ngoài `data/lop3/` nên mọi phép dọn theo thư mục đều trượt — và
# nó chính là dòng ĐẦU TIÊN bé đọc khi mở bài (`objective.kidText`). Ba bài lớp 3
# còn tên ở đây: B18 · B29 · B34.
#
# Chỉ đụng khoá bắt đầu bằng `DL:KSN3.` — lớp 3 và lớp 5 vẫn giữ nhân vật của mình,
# quét cả tệp là dọn nhầm sang quyển khác.
TEP_LOI_CHAO = 'data/loi_chao.json'
TIEN_TO_LOP3 = 'DL:KSN3.'

# ── GỢI Ý VIẾT TAY · CỬA THỨ TƯ ──
#
# `data/goi_y_tay.json` cũng là tệp phẳng dùng chung bốn quyển, khoá là mã bài, và
# `goi_y.py` chạy Ở BƯỚC CUỐI dây chuyền — sau khi mọi thứ đã sạch. Nên dọn xong,
# quét xong, báo xanh xong, rồi chạy `goi_y.py` một phát là tên quay lại hai bài
# (B17 · B20). Cùng hình dạng với cửa lời chào: tệp chung, nằm ngoài thư mục quyển,
# và ghi ĐÈ vào bản dựng ở bước sau cùng.
TEP_GOI_Y = 'data/goi_y_tay.json'

# Phụ đề quyển. Sửa ở CẢ HAI nơi — `data/` là bản gốc, `web/public/content/` là bản
# dựng, và không có bước nào chép tự động giữa hai chỗ ấy cho riêng tệp này.
PHU_DE_CU = 'Cùng Su Kem và Su Bống ra khơi Vạn Số'
PHU_DE_MOI = 'Nhân chia ra ngoài bảng, biểu thức, hình học và xem giờ'
TEP_PHU_DE = ['data/chuong_trinh.json', 'web/public/content/chuong_trinh.json']

# ── ① Vai NGƯỜI TRONG ĐỀ TOÁN ──
# Giữ vai: Su Kem là anh/chị lớn hơn, Su Bống là em. Tên lấy từ dàn lớp 2·4.
TEN = {
    'Su Kem': 'Minh',
    'Su Bống': 'Mai',
    'Trí Long': 'Nam',
    'Cáo Đề': 'Bình',
}

# ── ② Vai NGƯỜI LÀM SAI ──
# Đầu câu thì "Có bạn", giữa câu thì "bạn ấy" — hai chỗ khác nhau về ngữ pháp.
# Thứ tự trong danh sách có ý: cụm DÀI phải đi trước, không thì "Trí Long" bị
# "Trí" của "Trí Dũng" ăn mất một nửa.
AN_DANH = ['Su Kem', 'Su Bống', 'Trí Long', 'Cáo Đề']

# Trường nào thuộc vai nào. Khoá là đường đi trong tệp gốc `data/lop3/*.json`.
# Sai bảng này là sai cả hai chiều, nên phép kiểm bên dưới đếm lại từng vai.
VAI_AN_DANH = {
    'muc.suKemNham',        # mục "bạn ấy nhầm" — nguồn của misconceptions
}

# ── VÁ TAY: câu có HAI người ──
#
# Giấu tên chỉ đúng khi trong câu có MỘT người. Bốn câu dưới đây nhắc hai nhân vật
# khác nhau — người làm sai, và người sửa/người được cho quà. Thay máy thì cả hai
# thành "bạn ấy", câu vẫn xuôi tai mà mất hẳn nghĩa:
#
#     "…nhắc cậu ấy nghi thức mà chính Su Kem đã học được năm ngoái"
#         → "…nhắc cậu ấy nghi thức mà chính bạn ấy đã học được năm ngoái"
#           (hoá ra tự nhắc chính mình)
#
# Phép quét tự tìm ra đúng bốn câu này (chuỗi vai giấu tên có ≥2 nhân vật), nên
# thêm bài mới mà quên khai thì phép kiểm bên dưới báo ngay, không im lặng.
VA_TAY = {
    'Gợi ý 2: Trí Long viết nhanh nên bỏ rơi ai ở tháp Trăm? Viết lại chuẩn giúp '
    'cậu ấy — và nhắc cậu ấy nghi thức mà chính Su Kem đã học được năm ngoái: '
    'viết xong ĐỌC LẠI một lần!':
        'Gợi ý 2: Bạn ấy viết nhanh nên bỏ rơi ai ở tháp Trăm? Con viết lại cho '
        'chuẩn, và nhớ lấy nghi thức đã học từ năm ngoái: viết xong ĐỌC LẠI '
        'một lần!',

    'Gợi ý 2: Viết phép cân thành câu tìm X quen thuộc: bột + 50 = 500. Bột là bao '
    'nhiêu — và nếu trộn theo con số 550 g của Trí Long, bánh sinh nhật của Su Bống '
    'sẽ ra... gạch nướng đấy!':
        'Gợi ý 2: Viết phép cân thành câu tìm X quen thuộc: bột + 50 = 500. Bột là '
        'bao nhiêu — và nếu trộn theo con số 550 g kia, bánh sinh nhật sẽ ra... '
        'gạch nướng đấy!',

    'Cuối buổi, Trí Long đổ hộp tiền ra đếm: "Bốn mươi nghìn tròn trĩnh! Lãi 40 '
    'nghìn — quà cho Su Bống mua được cả gấu bông khổng lồ!"':
        'Cuối buổi, có bạn đổ hộp tiền ra đếm: "Bốn mươi nghìn tròn trĩnh! Lãi 40 '
        'nghìn — mua quà cho em được cả gấu bông khổng lồ!"',

    # Chỗ này KHÔNG phải hai người — nó là MỘT người NHƯNG ĐỨNG SAI VAI. Trong mục
    # "chỗ hay nhầm", cái tên trong ngoặc đơn chỉ NGƯỜI TRONG ĐỀ TOÁN (em gái đang
    # phải tìm số nhãn vở), không phải người làm sai. Máy giấu tên theo đường dẫn
    # nên biến nó thành "(bạn ấy)" — đọc lên thành ra đang nói về đứa trẻ vừa tính
    # nhầm. Một mục có thể chứa CẢ HAI vai; đường dẫn không phân biệt nổi.
    'Gợi ý 1: Câu hỏi vàng số 2 bị bỏ qua rồi: AI gấp AI? Người đang giữ số 15 là '
    'người NHIỀU phần hay ÍT phần? Người cần tìm (Su Bống) đứng ở phía nào?':
        'Gợi ý 1: Câu hỏi vàng số 2 bị bỏ qua rồi: AI gấp AI? Người đang giữ số 15 '
        'là người NHIỀU phần hay ÍT phần? Người cần tìm (Mai) đứng ở phía nào?',

    'Gợi ý 2: Mở sổ của Su Kem: dòng VỐN ghi gì? Tính lại tiền lãi thật — và xem '
    'với số ấy thì mua được gấu bông cỡ nào. (Đừng buồn Trí Long ơi, 16 nghìn vẫn '
    'là buổi bán hàng ra trò!)':
        'Gợi ý 2: Mở sổ ra xem: dòng VỐN ghi gì? Tính lại tiền lãi thật — và xem '
        'với số ấy thì mua được gấu bông cỡ nào. (Đừng buồn nhé, 16 nghìn vẫn là '
        'buổi bán hàng ra trò!)',
}


# ── TIÊU ĐỀ MỤC · CỬA SAU MÀ TÊN CHUI VỀ ──
#
# `tools/khuon_chung.py` SUY dòng "dấu hiệu" của misconception từ chính tiêu đề mục:
#
#     'TRÍ LONG ƠI, NHẦM RỒI!'  →  'Bé làm theo cách Trí Long vừa nói.'
#
# Nên dọn sạch lời văn mà bỏ quên tiêu đề thì tên quay lại đủ 34 bài, ở một trường
# KHÔNG hề có chữ "Trí Long" trong nguồn — không grep nào tìm ra. Đã dính thật.
#
# Tiêu đề viết HOA nên phép thay theo đúng chữ ở `TEN`/`AN_DANH` cũng trượt. Đặt
# thẳng về đúng cái tên trung tính mà `khuon_chung` nhận là "không có ai":
# nó thấy 'CHỖ HAY NHẦM' thì tự viết 'Bé làm theo cách sai vừa nêu ở trên.'
TEN_MUC_NHAM = 'CHỖ HAY NHẦM'


def _an_danh(t: str) -> str:
    """Giấu tên: đầu câu thành 'Có bạn', giữa câu thành 'bạn ấy'."""
    for ten in AN_DANH:
        # đầu chuỗi, hoặc ngay sau dấu chấm/hỏi/than/xuống dòng/mở ngoặc kép
        t = re.sub(rf'(^|(?<=[.!?:\n"“])\s*){re.escape(ten)}', r'\1Có bạn', t)
        t = t.replace(ten, 'bạn ấy')
    # "Có bạn" đứng ngay sau "Có bạn" trong cùng một câu đọc rất kỳ — hạ cái sau xuống
    t = re.sub(r'(Có bạn[^.!?]*?)Có bạn', r'\1bạn ấy', t)
    return t


def _doi_ten(t: str) -> str:
    """Đổi sang tên bạn nhỏ thường, giữ nguyên ngữ pháp."""
    for a, b in TEN.items():
        t = t.replace(a, b)
    return t


def sua(o, duong: str, dem: dict):
    """Đi khắp tệp, chọn lối xử theo ĐƯỜNG ĐI của trường."""
    if isinstance(o, str):
        # Tiêu đề mục "bạn ấy nhầm": đặt thẳng, đừng thay chữ. Tiêu đề viết HOA nên
        # phép thay theo chữ thường trượt hết — mà đây lại là cửa `khuon_chung` suy
        # ra dòng dấu hiệu, tức là chỗ tên quay về mà không ai thấy.
        if duong == 'muc.suKemNham.ten' and o != TEN_MUC_NHAM:
            dem['tenMuc'] += 1
            return TEN_MUC_NHAM
        if not any(x in o for x in AN_DANH):
            return o
        an = any(duong.startswith(k) for k in VAI_AN_DANH)
        if an and o in VA_TAY:
            dem['vaTay'] += 1
            return VA_TAY[o]
        # Câu vai giấu tên mà có HAI nhân vật thì máy không xử được — phải khai tay.
        # Kêu to chứ đừng lặng lẽ thay bừa: đây đúng chỗ đã suýt mất nghĩa.
        if an and sum(1 for x in AN_DANH if x in o) >= 2:
            dem['thieuVaTay'] += 1
            print(f'  ⚠ CHƯA KHAI `VA_TAY` cho câu hai người:\n      {o[:150]}',
                  file=sys.stderr)
            return o
        moi = _an_danh(o) if an else _doi_ten(o)
        dem['anDanh' if an else 'doiTen'] += 1
        return moi
    if isinstance(o, dict):
        return {k: sua(v, f'{duong}.{k}' if duong else k, dem) for k, v in o.items()}
    if isinstance(o, list):
        return [sua(v, duong + '[]', dem) for v in o]
    return o


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--thu', action='store_true', help='chỉ in, không ghi')
    ns = ap.parse_args(argv)

    dem = {'anDanh': 0, 'doiTen': 0, 'vaTay': 0, 'thieuVaTay': 0, 'phuDe': 0, 'tenMuc': 0, 'loiChao': 0, 'goiYTay': 0}
    doi_tep = 0
    vd = []
    for p in sorted(DATA.glob('DL_KSN3_B*.json')):
        goc = p.read_text('utf8')
        d = json.loads(goc)
        moi = sua(d, '', dem)
        ra = json.dumps(moi, ensure_ascii=False, indent=1)
        if ra != json.dumps(d, ensure_ascii=False, indent=1) or ra != goc:
            doi_tep += 1
            if len(vd) < 4:
                for a, b in zip(goc.split('\n'), ra.split('\n')):
                    if a != b and len(vd) < 4 and any(x in a for x in AN_DANH):
                        vd.append((a.strip()[:110], b.strip()[:110]))
            if not ns.thu:
                p.write_text(ra, 'utf8')

    # ── các tệp nguồn khác: ôn tập, ải, đáp án ──
    # Toàn bộ là ĐỀ TOÁN, không có mục "bạn ấy nhầm", nên chỉ một lối: đổi tên.
    for ten in TEP_KHAC:
        p = GOC / ten
        if not p.exists():
            continue
        s = p.read_text('utf8')
        moi = _doi_ten(s)
        if moi != s:
            doi_tep += 1
            dem['doiTen'] += sum(s.count(x) for x in AN_DANH)
            if not ns.thu:
                p.write_text(moi, 'utf8')

    # ── hai tệp phẳng dùng chung bốn quyển: lời chào và gợi ý tay ──
    # Cùng một hình dạng, cùng một cái bẫy: khoá là mã bài, nằm ngoài `data/lop3/`,
    # và được ghi ĐÈ vào bản dựng ở bước SAU CÙNG của dây chuyền. Chỉ đụng khoá của
    # lớp 3 — lớp 5 vẫn giữ nhân vật của mình.
    for ten, khoa_dem in ((TEP_LOI_CHAO, 'loiChao'), (TEP_GOI_Y, 'goiYTay')):
        p = GOC / ten
        if not p.exists():
            continue
        kho = json.loads(p.read_text('utf8'))
        doi = 0
        for k, v in kho.items():
            if not k.startswith(TIEN_TO_LOP3):
                continue
            cu = json.dumps(v, ensure_ascii=False)
            moi = _doi_ten(cu)
            if moi != cu:
                kho[k] = json.loads(moi)
                doi += 1
        if doi:
            doi_tep += 1
            dem[khoa_dem] += doi
            if not ns.thu:
                p.write_text(json.dumps(kho, ensure_ascii=False, indent=1), 'utf8')

    # ── phụ đề quyển ──
    for ten in TEP_PHU_DE:
        p = GOC / ten
        if not p.exists() or PHU_DE_CU not in p.read_text('utf8'):
            continue
        doi_tep += 1
        dem['phuDe'] += 1
        if not ns.thu:
            p.write_text(p.read_text('utf8').replace(PHU_DE_CU, PHU_DE_MOI), 'utf8')

    print(f'{doi_tep} tệp đổi · {dem["doiTen"]} chuỗi đổi tên · '
          f'{dem["anDanh"]} chuỗi giấu tên · {dem["vaTay"]} chuỗi vá tay · '
          f'{dem["phuDe"]} phụ đề · {dem["tenMuc"]} tiêu đề mục · '
          f'{dem["loiChao"]} lời chào · {dem["goiYTay"]} gợi ý tay')
    if dem['thieuVaTay']:
        print(f'  ⚠ {dem["thieuVaTay"]} câu hai người CHƯA khai `VA_TAY` — '
              'để nguyên, chưa đụng vào')
    for a, b in vd:
        print(f'\n  TRƯỚC: {a}\n  SAU  : {b}')
    if ns.thu:
        print('\n(--thu: chưa ghi gì cả)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
