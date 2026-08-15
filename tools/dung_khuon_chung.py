# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 5 — dựng bản cho app theo KHUÔN CHUNG với lớp 5.

    python3 tools/dung_khuon_chung.py

Hai thư mục, hai vai khác nhau — đừng sửa nhầm:
    data/lop2/                    BẢN GỐC: giữ nguyên 8 mục ①…⑧ của sách, để người
                                  đối chiếu với sách giấy. Các bước 1–4 ghi vào đây.
    web/public/content/lop2/      BẢN CHO APP: đúng khuôn lớp 5, sinh ra từ bản gốc.
                                  KHÔNG sửa tay ở đây, chạy lại bước này là mất.

Nhờ cùng khuôn mà lớp 2 dùng được nguyên bộ mã của lớp 5: nhật ký học, sổ phụ
huynh, bảng cô giáo, BKT, nhớ chỗ học dở, gợi ý theo số lần sai.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'tools'))
from khuon_chung import sang_khuon_chung
from tach_ontap import cau_de_b                    # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop2')
NGUON_ON = os.path.join(GOC_KHO, 'data', 'lop2_ontap.json')
RA_ON = os.path.join(GOC_KHO, 'web', 'public', 'content', 'reviews')
RA = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop2')
RA_VIDEO = os.path.join(GOC_KHO, 'web', 'public', 'content', 'toan', 'video')
SO_DK = os.path.join(GOC_KHO, 'data', 'chuong_trinh.json')
DAP_AN = os.path.join(GOC_KHO, 'data', 'lop2_dapan.json')
RA_DK = os.path.join(GOC_KHO, 'web', 'public', 'content', 'chuong_trinh.json')


# Khai đích danh mối nối cho những câu mà bài gốc đã tách. Khoá là (chương, số câu).
KHAI_TAY_L2 = {
    # ── chương 1 · Vương quốc Số: năm bài tách thành mười ──
    (1, 1): {'ve': 'DL:KSN2.B34'},    # tách số thành tổng — không còn ở B01
    (1, 5): {'ve': 'DL:KSN2.B35'},    # điền dấu lớn bé — so hai số
    (1, 7): {'ve': 'DL:KSN2.B37'},    # tính số mới hơn số cũ bao nhiêu — hiệu
    (1, 8): {'ve': 'DL:KSN2.B38'},    # ba thẻ có số 0
    (1, 11): {'ve': 'DL:KSN2.B37'},   # đổi chỗ hơn 45 đơn vị — hiệu
    (1, 12): {'ve': 'DL:KSN2.B38'},   # ba thẻ 5, 0, 5
    # Câu 6 cũ hỏi lại đúng ý câu 2 (đều là thêm chữ số 0), trong khi bài XOÁ SỐ 0
    # TẬN CÙNG không có câu nào hỏi tới. Viết lại câu 6 cho phủ bài ấy — vẫn giữ
    # nguyên chuyện cửa hàng ghi nhầm giá, chỉ đổi chiều.
    # ── chương 2 · Bé là vua đếm: ba bài tách thành sáu ──
    (2, 1): {'ve': 'DL:KSN2.B39'},    # cột đèn 5, 10, 15 — đếm nhảy cóc
    (2, 2): {'ve': 'DL:KSN2.B39'},    # ghế đá số chẵn — đếm nhảy cóc
    (2, 7): {'ve': 'DL:KSN2.B41'},    # cuốn vở 13 trang — cộng hai đoàn tàu
    (2, 8): {'ve': 'DL:KSN2.B40'},    # số chứa chữ số 4 — bớt số đếm hai lần
    (2, 9): {'ve': 'DL:KSN2.B39'},    # số chẵn số lẻ — đếm nhảy cóc
    # ── chương 3 · Dãy số kỳ diệu: ba bài tách thành chín ──
    # Chương này gộp nặng nhất: mười câu ôn tập của sách đều trỏ dồn vào ba mã cũ,
    # trong khi nay có chín bài. Khai lại từng câu một theo đúng nghề nó hỏi.
    (3, 4): {'ve': 'DL:KSN2.B42'},    # điền hai số bị mờ ở giữa dãy
    (3, 6): {'ve': 'DL:KSN2.B10'},    # 2, 4, 8, 16 — dãy gấp đôi
    (3, 7): {'ve': 'DL:KSN2.B44'},    # 2, 3, 5, 8 — dãy bậc thang
    (3, 8): {'ve': 'DL:KSN2.B47'},    # tổng chẵn hay lẻ, không tính kết quả
    (3, 9): {'ve': 'DL:KSN2.B43'},    # tàu có dừng ở ga 30 không — nhảy cóc thử
    (3, 10): {'ve': 'DL:KSN2.B45'},   # nhiều dãy khác quy luật trong cùng một đề
    # Câu 5 cũ hỏi "đoàn tàu 3, 6, 9, ..., 27 có mấy toa" — đúng ý câu C8 luyện tập
    # của bài NHẢY CÓC THỬ, mà câu 9 đã phủ bài ấy rồi. Trong khi bài BẢNG NHÂN
    # GIẤU GÌ không có câu nào hỏi tới. Viết lại câu 5 cho phủ bài ấy; nghề đếm toa
    # vẫn còn nguyên ở phần luyện tập nên sách không mất gì.
    (3, 5): {'ve': 'DL:KSN2.B46',
             'text': 'Số 37 có nằm trong bảng nhân 5 không? Nhìn vào chữ số nào là '
                     'biết ngay mà không cần đọc cả bảng?',
             'answer': 'Không. Bảng nhân 5 chỉ có số tận cùng bằng 0 hoặc 5, mà 37 '
                       'tận cùng bằng 7 nên nó không thuộc bảng.',
             'khoa': {'parts': [
                 {'label': 'có trong bảng nhân 5 không',
                  'options': ['có', 'không'], 'value': 'không'},
                 {'label': 'nhìn chữ số nào',
                  'options': ['chữ số tận cùng', 'chữ số đầu tiên'],
                  'value': 'chữ số tận cùng'}]}},
    # ── chương 4 · Siêu nhân tính nhanh: bốn bài tách thành mười ──
    (4, 6): {'ve': 'DL:KSN2.B48'},    # ghép khay kẹo 4 × 2 + 4 × 8
    (4, 7): {'ve': 'DL:KSN2.B50'},    # ô trống nhân 4 — máy nhân chia ngược nhau
    (4, 8): {'ve': 'DL:KSN2.B51'},    # 19 trừ ô trống — ca ô trống đứng sau dấu trừ
    (4, 10): {'ve': 'DL:KSN2.B49'},   # dãy chín số, có một bạn đứng giữa
    (4, 12): {'ve': 'DL:KSN2.B52'},   # số thừa nhiều nhất — luật vàng
    # Câu 5 cũ hỏi lại đúng ý câu 2 (đều là ghép đôi tròn chục ở phép cộng), trong
    # khi bài CHIA HẾT HAY CÒN THỪA không có câu nào hỏi tới. Viết lại câu 5 cho phủ
    # bài ấy — vẫn nằm trong mạch chia kẹo của nửa sau chương.
    (4, 5): {'ve': 'DL:KSN2.B53',
             'text': 'Chia 26 viên kẹo cho 4 bạn thì chia hết hay còn thừa, và thừa '
                     'mấy viên?',
             'answer': 'Số 26 không có trong bảng nhân 4 nên còn thừa. Trạm dừng gần '
                       'nhất mà chưa vượt là 24, nên mỗi bạn 6 viên và còn thừa 2 '
                       'viên.',
             'khoa': {'parts': [
                 {'label': 'chia hết hay còn thừa',
                  'options': ['chia hết', 'còn thừa'], 'value': 'còn thừa'},
                 {'label': 'thừa mấy viên', 'value': 2}]}},

    # ── chương 5 · Chuyện toán lời văn: sáu bài tách thành mười hai ──
    (5, 5): {'ve': 'DL:KSN2.B54'},    # mỗi bạn góp 5 quyển, 4 bạn — biết mỗi, hỏi tất cả
    (5, 7): {'ve': 'DL:KSN2.B56'},    # tổng 14 hơn nhau 2 — bài hai điều kiện
    (5, 9): {'ve': 'DL:KSN2.B59'},    # 3 giờ được 18 sản phẩm — biết tất cả, hỏi mỗi
    (5, 10): {'ve': 'DL:KSN2.B18'},   # tổng 9 hơn nhau 2 có chia được không — liệt kê
    (5, 11): {'ve': 'DL:KSN2.B58'},   # khi em 8 tuổi thì chị mấy — hiệu tuổi không đổi
    (5, 12): {'ve': 'DL:KSN2.B57'},   # A gấp đôi B, cả hai 15 — chia tổng cho số phần
    # Câu 6 cũ hỏi lại đúng ý câu 2 (đều là tìm người ÍT hơn, phép trừ thẳng), trong
    # khi bài BẪY CÂU CHỮ ĐẢO không có câu nào hỏi tới. Đảo chiều câu 6 cho người
    # phải tìm thành người NHIỀU hơn — đúng cái bẫy mà bài ấy dạy.
    (5, 6): {'ve': 'DL:KSN2.B55',
             'text': 'Lan có ít hơn Hoa 6 nhãn vở. Lan có 15 nhãn vở. Hỏi Hoa có mấy '
                     'nhãn vở? Cẩn thận nhé — ai mới là người nhiều hơn?',
             'answer': 'Lan ít hơn Hoa nên HOA mới là người nhiều nhãn hơn. Vậy phải '
                       'cộng: 15 + 6 = 21 (nhãn vở). Đáp số: 21 nhãn vở.',
             'khoa': {'parts': [
                 {'label': 'ai nhiều hơn', 'options': ['Hoa', 'Lan'], 'value': 'Hoa'},
                 {'label': 'Hoa có mấy nhãn', 'value': 21}]}},

    (1, 6): {'ve': 'DL:KSN2.B36',
             'text': 'Một cửa hàng ghi giá 90 nghìn đồng nhưng viết sót mất chữ số '
                     '0 ở cuối, thành 9 nghìn đồng. Giá bị viết rẻ đi bao nhiêu '
                     'nghìn đồng, và số ghi sai nhỏ hơn số đúng mấy lần?',
             'answer': 'Rẻ đi: 90 − 9 = 81 (nghìn đồng). Xoá một chữ số 0 ở cuối '
                       'thì số nhỏ đi 10 lần.'},
}


# Tên kỳ sát hạch của sách có chỗ nhắc nhân vật. Chương nào đã chuyển hết sang
# video thì trong bài không còn nhân vật nào nữa, nên cái tên ấy thành mồ côi — bé
# đọc thấy một cái tên chưa gặp ở đâu bao giờ. Đổi tên đúng những chương ấy thôi;
# chương còn bài chữ thì giữ nguyên tên của sách.
DOI_TEN_KY_L2 = {
    'ÔN TẬP 5 · TUYỂN TẬP CHUYỆN TOÁN CỦA TRÍ LONG':
        'ÔN TẬP 5 · TUYỂN TẬP CHUYỆN TOÁN LỜI VĂN',
}


def _ten_ky(ten):
    t = re.sub(r'^★+\s*|\s*\(\d+ câu\)$', '', ten).replace('—', '·')
    return DOI_TEN_KY_L2.get(t, t)


def dung_on_tap(bai_cua_chuong, ten_bai):
    """8 ôn tập + 3 ải → kỳ sát hạch, đúng khuôn DCR_* của lớp 5.

    BẢNG TỰ SOI của sách khớp thẳng vào `diagnosesMicro`: bé sai câu nào thì bấm
    một nút là mở đúng bài cần ôn. Đây là thứ đáng giá nhất của phần ôn tập —
    cùng ý tưởng với trục CĐ-x.y ↔ Bx.My đã chạy tốt ở lớp 5.
    """
    if not os.path.exists(NGUON_ON):
        return []
    de = json.load(open(NGUON_ON, encoding='utf-8'))
    os.makedirs(RA_ON, exist_ok=True)
    # hình của kỳ sát hạch (tranh công viên, mật thư, bốn trạm…)
    so_tay = {}
    duong_sotay = os.path.join(GOC_KHO, 'data', 'lop2_hinh_manifest.json')
    if os.path.exists(duong_sotay):
        so_tay = json.load(open(duong_sotay, encoding='utf-8'))
    hinh_ky = {}
    for hid, h in so_tay.items():
        if h.get('onTap'):
            hinh_ky.setdefault(h['onTap'], []).append(
                {'id': hid, 'file': h['file'], 'caption': h['caption'],
                 'sha256_16': h['sha256_16']})
    o_nhap = {}
    duong_o = os.path.join(GOC_KHO, 'data', 'lop2_ontap_o.json')
    if os.path.exists(duong_o):
        o_nhap = json.load(open(duong_o, encoding='utf-8'))
    else:
        print('  ⚠ chưa có data/lop2_ontap_o.json — kỳ sát hạch về TỰ CHẤM hết. '
              'Chạy `python3 tools/tach_ontap.py lop2` trước.')

    ra, chua_soi = [], 0

    for ma, d in sorted(de.items(), key=lambda kv: (kv[0][0], int(kv[0][1:]))):
        ai = d['loai'] == 'ai'
        ch = d['so'] + (8 if ai else 0)          # ải xếp tiếp sau 8 chương
        mac_dinh = bai_cua_chuong.get(d['so'], [None])[0]
        cau = []
        for c in d['cau']:
            # ══ MỐI NỐI KHÔNG SUY TỪ SỐ BÀI CỦA SÁCH NỮA ══
            #
            # Bảng tự soi của sách ghi "Câu 5 → Bài 1", và trước đây mã bài suy
            # thẳng từ con số ấy. Từ khi tách bài làm video thì hỏng: mã B01 vẫn
            # còn, nhưng nay nó CHỈ dạy ba phòng, còn phần so sánh đã sang bài
            # khác. Bé sai câu so sánh, bấm "ôn lại bài này", và được dẫn tới bài
            # dạy đọc số.
            #
            # Cả hai đầu đều hợp lệ, chỉ chỗ nối là sai — không phép kiểm nào bắt
            # được. Nên chỗ nào đổi thì khai ĐÍCH DANH ở đây. Cùng cách làm với
            # `KHAI_TAY` bên `tools/ontap_lop4.py`.
            khai = KHAI_TAY_L2.get((ch, c['so'])) or {}
            b = d['soi'].get(str(c['so'])) or d['soi'].get(c['so'])
            if khai.get('ve'):
                mic = khai['ve']
            elif b:
                mic = f'DL:KSN2.B{int(b):02d}'
            else:
                mic = mac_dinh                    # ải không có bảng tự soi
                chua_soi += 0 if ai else 1
            # Câu viết lại thì ô nhập cũ không còn khớp — cho khai đè luôn ở đây,
            # chứ vá vào `lop2_ontap_o.json` thì lần chạy `tach_ontap.py` sau sẽ dựng
            # lại tệp ấy và xoá mất bản vá, y như bốn lần đã dính trước đây.
            khoa = khai.get('khoa') or o_nhap.get(f"{ma}#C{c['so']}")
            cau.append({'id': f"REVITEM:KSN2.C{ch}.A{c['so']}", 'qno': c['so'],
                        'star': c.get('muc', 1),
                        'text': khai.get('text') or c['text'],
                        'answer': khai.get('answer') or d['dapAn'].get(f"C{c['so']}", ''),
                        'solutionNarrative': (khai.get('answer')
                                              or d['dapAn'].get(f"C{c['so']}", '')),
                        **({'answerKey': khoa} if khoa else {}),
                        'diagnosesMicro': mic,
                        # Tên bài viết đủ chữ: bé lớp 2 không biết "micro" là gì,
                        # mà đây đúng là dòng bé đọc khi làm sai và cần ôn lại.
                        'trapName': ten_bai.get(mic, 'ôn lại bài này')})
        doc = {
            'id': f'DCR:KSN2.C{ch}', 'quyen': 'lop2', 'chapter': ch,
            'loai': d['loai'], 'so': d['so'],
            # Tên hiện lên màn hình: bỏ dấu sao và phần "(10 câu)" — bé đã thấy
            # số câu ở góc màn rồi, nhắc lại trong tên chỉ làm dòng dài thêm.
            'name': _ten_ky(d['ten']),
            'gioiThieu': d['gioiThieu'],
            'need': d['can'], 'passRule': d.get('ketLuan', f"Đạt {d['can']}/{d['tong']} câu là qua."),
            'examA': cau,
            # Đề B của lớp 2 nhồi bốn câu vào MỘT dòng ("B1. … B2. … B3. …") nên
            # trước đây nó là một khối chữ không chấm được, và `ExamPlayer` cũng
            # chưa hề hiện tới. Nay cắt theo `B<số>.` thành từng câu thật, mỗi câu
            # một ô nhập — đáp án thì sách đã tách sẵn theo B1, B2… từ lâu.
            'deB': [{'id': c['id'], 'qno': int(c['id'][1:]), 'text': c['text'],
                     'answer': d['dapAnB'].get(c['id'], ''),
                     'solutionNarrative': d['dapAnB'].get(c['id'], ''),
                     **({'answerKey': o_nhap[f"{ma}#{c['id']}"]}
                        if o_nhap.get(f"{ma}#{c['id']}") else {})}
                    for c in cau_de_b(d)],
            'selfCheck': 'Sai câu nào, bấm vào câu đó để mở lại đúng bài cần ôn.',
            'hinh': hinh_ky.get(f'C{ch}', []),
        }
        with open(os.path.join(RA_ON, f'DCR_KSN2_C{ch}.json'), 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        ra.append({'id': doc['id'], 'chapter': ch, 'loai': d['loai'], 'so': d['so'],
                   'soHinh': len(doc['hinh']),
                   # Tên hiện lên màn hình: bỏ dấu sao và phần "(10 câu)" — bé đã thấy
            # số câu ở góc màn rồi, nhắc lại trong tên chỉ làm dòng dài thêm.
            'name': _ten_ky(d['ten']), 'soCau': len(cau), 'need': d['can']})
    if chua_soi:
        print(f'  ⚠ {chua_soi} câu ôn tập chưa có trong Bảng tự soi → tạm trỏ về bài đầu chương')
    print(f'  {len(ra)} kỳ sát hạch · {sum(x["soCau"] for x in ra)} câu')
    return ra


def _cau_luyen(duong):
    d = json.load(open(duong, encoding='utf-8'))
    return [x for v in d['practice']['pools'].values() for x in v]


def main():
    os.makedirs(RA, exist_ok=True)
    # ══ LỐI C — THỨ TỰ HỌC ĐỌC TỪ `thu_tu.json`, KHÔNG ĐỌC TRƯỜNG `so` ══
    #
    # Trước đây thứ tự lấy từ chính trường `so` trong tệp nguồn. Chèn một bài vào
    # giữa là phải dồn mã của mọi bài phía sau — 353 tệp ở lớp 4, và còn phải dời
    # TIẾN ĐỘ ĐÃ LƯU của từng bé cho khớp. Lối C cắt sợi dây ấy: mã bài chỉ còn là
    # cái TÊN, số hiển thị đếm từ vị trí trong lời khai.
    #
    # ⚠ Bộ dựng ĐÈ `b['so']` theo vị trí. Trường `so` trong tệp nguồn KHÔNG còn là
    # sự thật — đừng đọc nó. Xem `docs/ke_hoach_video_lop4.md` §10.
    teps = sorted(f for f in os.listdir(NGUON) if f.startswith('DL_KSN2_B'))
    thu_tu = json.load(open(os.path.join(NGUON, 'thu_tu.json'), encoding='utf-8'))['thuTu']
    co_tep = {t[:-5].replace('DL_KSN2_', 'DL:KSN2.'): t for t in teps}
    thieu_tep = [i for i in thu_tu if i not in co_tep]
    thieu_khai = sorted(i for i in co_tep if i not in thu_tu)
    if thieu_tep or thieu_khai:
        raise SystemExit(
            'thu_tu.json lệch với thư mục nguồn — DỪNG, chưa ghi gì cả.\n'
            + (f'  khai mà không có tệp: {thieu_tep}\n' if thieu_tep else '')
            + (f'  có tệp mà chưa khai: {thieu_khai}' if thieu_khai else ''))
    bais = []
    for vi_tri, ma in enumerate(thu_tu, 1):
        b = json.load(open(os.path.join(NGUON, co_tep[ma]), encoding='utf-8'))
        b['so'] = vi_tri
        bais.append(b)
    ids = [b['id'] for b in bais]

    dap_an = json.load(open(DAP_AN, encoding='utf-8')) if os.path.exists(DAP_AN) else {}

    idx = []
    for k, b in enumerate(bais):
        d = sang_khuon_chung(b, truoc=ids[k - 1] if k else None,
                             sau=ids[k + 1] if k + 1 < len(ids) else None,
                             dap_an=dap_an)
        # Bài nào đã dựng video thì khai vào đây — `StepView.jsx` đọc trường này
        # cho MỌI quyển, không riêng lớp 4. Khai theo tệp CÓ THẬT chứ đừng gõ tay:
        # gõ tay mà khai một bài chưa dựng thì màn hình hiện ô đen, còn dựng xong
        # mà quên khai thì video nằm đó không ai xem. Cả hai đều im lặng.
        ten_tep = b['id'].replace('DL:', 'DL_').replace('.', '_')
        if os.path.exists(os.path.join(RA_VIDEO, f'{ten_tep}_giang.mp4')):
            d['video'] = {'giang': f'{ten_tep}_giang.mp4'}
        ten = ten_tep + '.json'
        with open(os.path.join(RA, ten), 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        idx.append({
            'id': d['id'], 'so': d['so'], 'ten': b['ten'], 'title': d['title'],
            'chuong': d['chuong'], 'tenChuong': d['tenChuong'],
            'bktUnit': d['skills']['bktUnit'], 'passRule': d['assessment']['passRule'],
            'objective': d['objective']['kidText'],
            'durationMinutes': d['durationMinutes'],
            'soCau': sum(len(v) for v in d['practice']['pools'].values()),
            'soQuiz': len(d['assessment']['items']),
            'soHinh': len(d['figureSpec']),
        })

    theo_chuong = {}
    for x in idx:
        theo_chuong.setdefault(x['chuong'], []).append(x['id'])
    ten_bai = {x['id']: x['title'] for x in idx}
    on = dung_on_tap(theo_chuong, ten_bai)

    with open(os.path.join(RA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    with open(os.path.join(RA, 'ontap.json'), 'w', encoding='utf-8') as f:
        json.dump(on, f, ensure_ascii=False, indent=1)

    # sổ đăng ký chương trình — nơi DUY NHẤT khai khác biệt giữa hai lớp
    dk = json.load(open(SO_DK, encoding='utf-8'))
    dk['chuongTrinh']['lop2']['bai'] = ids
    dk['chuongTrinh']['lop2']['soBai'] = len(ids)
    for thu_muc, duong in ((None, SO_DK), (None, RA_DK)):
        with open(duong, 'w', encoding='utf-8') as f:
            json.dump(dk, f, ensure_ascii=False, indent=1)

    tong_hinh = sum(x['soHinh'] for x in idx)
    tong_cau = sum(x['soCau'] for x in idx)
    tong_quiz = sum(x['soQuiz'] for x in idx)
    print(f'dựng {len(idx)} bài theo khuôn chung → {os.path.relpath(RA, GOC_KHO)}')
    cham_may = sum(1 for f in os.listdir(RA) if f.startswith('DL_')
                   for it in _cau_luyen(os.path.join(RA, f)) if it.get('answerKey'))
    print(f'  {tong_cau} câu luyện tập ({cham_may} chấm máy được)'
          f' · {tong_quiz} câu sát hạch · {tong_hinh} hình')


if __name__ == '__main__':
    main()
