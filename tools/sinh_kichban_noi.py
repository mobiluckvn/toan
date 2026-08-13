#!/usr/bin/env python3
"""SINH KỊCH BẢN PHÒNG LUYỆN NÓI — mỗi unit một kịch bản viết sẵn.

    python3 tools/sinh_kichban_noi.py            # sinh cho cả quyển ta1

Đọc `web/public/content/ta1/DL_TA1_B*.json` rồi đẻ ra `ta1/kichban_noi.json`.

── VÌ SAO PHẢI CÓ TỆP NÀY ──
Bác chốt 13-08: "viết sẵn kịch bản theo từng bài học để AI theo bài nào thì dùng
kịch bản đó sẽ đảm bảo hơn."

Đúng, và có bằng chứng. Trong một buổi đi thử, mô hình đã hai lần KHÔNG theo lời
dặn dù lời dặn viết rất rõ:

  · sinh ra "Bye, bike." — nhét đồ vật vào ô dành cho TÊN NGƯỜI;
  · nói y một câu hai lượt liền, ngay sau khi được dặn "đừng lặp".

Dặn dò là thứ mô hình CÓ THỂ theo. Kịch bản viết sẵn là thứ nó KHÔNG CẦN theo —
câu tiếng Anh đã nằm sẵn trong tệp, nó chỉ còn việc diễn đạt lời tiếng Việt và
phản ứng với cái bé vừa nói. Rút đúng cái quyền hay hỏng ra khỏi tay nó.

── VÌ SAO SINH CHỨ KHÔNG GÕ TAY 16 TỆP ──
Từ mới và mẫu câu đã nằm trong bài học rồi. Gõ tay lần nữa là chép, mà chép thì
sớm muộn lệch — sửa từ trong bài mà quên sửa trong kịch bản, không cổng nào bắt
được. Sinh ra từ chính bài học thì hai bên không thể lệch.

Sinh xong VẪN SỬA TAY ĐƯỢC: tệp là JSON thường, unit nào cần kịch bản riêng thì
sửa thẳng rồi thêm cờ `tay: true` để lần sinh sau không đè lên.

── BA CHỖ THAY LÚC CHẠY ──
    {ten}     tên bé
    {thich}   thứ bé vừa chọn ở màn "Con thích cái nào nhất?"
Chỗ nào không thay được thì máy con điền mặc định đã ghi sẵn ở `mac_dinh`.
"""
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NOI_DUNG = GOC / 'web' / 'public' / 'content' / 'ta1'
RA_PUBLIC = NOI_DUNG / 'kichban_noi.json'
RA_DATA = GOC / 'data' / 'tienganh' / 'kichban_noi.json'


def so_o_trong(cong_thuc):
    return len(re.findall(r'\[[^\]]+\]', cong_thuc or ''))


def o_trong(cong_thuc):
    """Ô trống của công thức nhận TÊN người hay nhận TỪ VỰNG.

    `Bye, + [Name].` mà điền từ vựng vào là ra "Bye, book." — vô nghĩa, và với bé
    đang tập nhại thì đó là dạy sai. Đã sinh ra thật khi thả cho mô hình tự điền.
    """
    m = re.search(r'\[([^\]]+)\]', cong_thuc or '')
    if not m:
        return None
    return 'ten' if re.search(r'name|tên', m.group(1), re.I) else 'tu'


def ten_trong_vi_du(cong_thuc, cau):
    """Giá trị mà chính SÁCH điền vào ô trống — `Hi, I'm + [Name].` + `Hi, I'm Bill.`
    thì ra "Bill".

    Dùng làm giá trị dự phòng khi bé chưa khai tên. Bịa sẵn một cái tên ("Bo") thì
    bé nào không khai tên cũng bị gọi bằng tên người khác; lấy tên trong sách thì
    ít nhất bé đang nhại đúng nhân vật của bài.
    """
    khung = re.sub(r'\s*\+\s*', ' ', cong_thuc or '')
    mau = re.escape(khung).replace(r'\[', '[').replace(r'\]', ']')
    mau = re.sub(r'\[[^\]]+\]', '(.+?)', mau)
    m = re.fullmatch(mau, cau or '')
    return m.group(1) if m else None


def dien(cong_thuc, gia_tri):
    """Điền một giá trị vào ô trống, bỏ dấu `+` nối của công thức."""
    return re.sub(r'\[[^\]]+\]', gia_tri, re.sub(r'\s*\+\s*', ' ', cong_thuc))


def kich_ban_cua(bai):
    tu = bai['knowledgeCore'].get('vocabulary', [])
    mau = bai['knowledgeCore'].get('mauCauDs') or []
    if not mau and bai['knowledgeCore'].get('mauCau'):
        mau = [bai['knowledgeCore']['mauCau']]

    buoc = [{'loai': 'chao', 'en': 'Hello!',
             'vi': 'Chào con! Hôm nay mình tập nói nhé.'}]

    # Hỏi sở thích khi có từ hai cái trở lên — chọn giữa một cái không phải là chọn.
    if len(tu) >= 2:
        buoc.append({'loai': 'hoiThich'})

    # Vòng 1: từng TỪ một. Đây là việc dễ nhất, và cũng là chỗ bé lùi về khi đuối.
    for t in tu:
        buoc.append({'loai': 'tu', 'en': t['tu'], 'tu': t['tu'],
                     'vi': f"Con nghe rồi nói lại từ này nhé — nghĩa là {t['nghia']}."})

    # Vòng 2: cả CÂU mẫu, rồi THAY chỗ trống — chỗ bé thấy mẫu câu "sống".
    for m in mau:
        buoc.append({'loai': 'mau', 'en': m['cau'],
                     'vi': 'Con nghe rồi nói lại cả câu này nhé.'})
        ct = m.get('congThuc')
        if not ct:
            continue
        # ── CHỈ THAY KHI CÔNG THỨC CÓ ĐÚNG MỘT Ô TRỐNG ──
        # Ba bài có công thức HAI ô: `It's a + [Colour] + [Noun].` (U6) và
        # `How many + [Noun-plural]? - [Number].` (U9 · U16). Bản đầu điền cùng một
        # giá trị vào MỌI ô, đẻ ra "It's a bell bell." — cổng bắt được ngay.
        #
        # Điền cho đúng hai ô thì phải biết ô nào nhận màu, ô nào nhận danh từ, ô
        # nào nhận số — mà bài không khai. Đoán ở đây là đoán sai. Nên bỏ bước
        # THAY cho mấy bài ấy: bước MẪU vẫn còn, bé vẫn được nói cả câu ví dụ.
        # Muốn hay hơn thì sửa tay kịch bản của ba bài ấy rồi đặt cờ `tay: true`.
        if so_o_trong(ct) != 1:
            continue
        loai = o_trong(ct)
        if loai == 'ten':
            buoc.append({'loai': 'thay', 'khung': ct, 'o': 'ten',
                         'en': dien(ct, '{ten}'),
                         'mac_dinh': ten_trong_vi_du(ct, m['cau']) or 'Bill',
                         'vi': 'Cùng mẫu câu ấy, nhưng nói về chính con.'})
        elif tu:
            buoc.append({'loai': 'thay', 'khung': ct, 'o': 'tu',
                         'en': dien(ct, '{thich}'), 'mac_dinh': tu[0]['tu'],
                         'vi': 'Cùng mẫu câu ấy, nay nói về thứ con thích.'})

    buoc.append({'loai': 'ket'})
    return {
        'bai': bai['id'],
        'ten': bai.get('title', ''),
        'tu': [t['tu'] for t in tu],
        'buoc': buoc,
    }


def main():
    tep = sorted(NOI_DUNG.glob('DL_TA1_B*.json'))
    if not tep:
        sys.exit(f'không thấy bài học nào ở {NOI_DUNG}')

    cu = {}
    if RA_PUBLIC.exists():
        cu = {k['bai']: k for k in json.loads(RA_PUBLIC.read_text('utf-8'))}

    ra, giu_tay = [], []
    for f in tep:
        bai = json.loads(f.read_text('utf-8'))
        # Kịch bản đã sửa tay thì GIỮ NGUYÊN — sinh lại mà đè lên là mất công người sửa.
        if cu.get(bai['id'], {}).get('tay'):
            ra.append(cu[bai['id']])
            giu_tay.append(bai['id'])
        else:
            ra.append(kich_ban_cua(bai))

    for p in (RA_PUBLIC, RA_DATA):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(ra, ensure_ascii=False, indent=1) + '\n', 'utf-8')

    tong = sum(len(k['buoc']) for k in ra)
    print(f'{len(ra)} kịch bản · {tong} bước · trung bình {tong / len(ra):.1f} bước một bài')
    if giu_tay:
        print('giữ nguyên bản sửa tay:', ', '.join(giu_tay))
    print('ghi:', RA_PUBLIC.relative_to(GOC), 'và', RA_DATA.relative_to(GOC))


if __name__ == '__main__':
    main()
