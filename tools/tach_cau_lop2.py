# -*- coding: utf-8 -*-
"""
LỚP 2 · tách câu luyện tập thành Ô ĐIỀN ĐƯỢC để máy chấm.

    python3 tools/tach_cau_lop2.py            # dựng + in bản soát
    python3 tools/tach_cau_lop2.py --soat     # chỉ in bản soát, không ghi

Vì sao cần: 281 câu luyện tập đang là "con làm ra vở rồi mở lời giải tự so". Bé làm
xong không ai biết đúng sai, sổ phụ huynh và bảng cô giáo không thấy gì — tức là
KHÔNG đánh giá được việc học.

Cách làm: một câu của sách thường chứa NHIỀU việc nhỏ ("Tách các số sau thành tổng:
452; 703; 290"). Tách thành nhiều Ô có nhãn riêng, mỗi ô một đáp án — bé điền từng ô,
máy chấm từng ô. Dùng `answerKey.parts` của bộ chấm lớp 5, không viết bộ chấm mới.

HAI NGUYÊN TẮC, vi phạm là bỏ câu ấy về tự chấm:
  1. KHÔNG BAO GIỜ tự nghĩ ra đáp án. Mọi giá trị phải rút từ lời giải của sách.
  2. Giá trị rút ra phải XUẤT HIỆN NGUYÊN VĂN trong lời giải (hàm `_that()`).
     Chấm sai một câu là bé mất tin vào cả phần mềm — thà để tự chấm còn hơn.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'data', 'lop2')
RA = os.path.join(GOC_KHO, 'data', 'lop2_dapan.json')
TAY = os.path.join(GOC_KHO, 'data', 'lop2_dapan_tay.json')   # sửa tay, đè lên bản suy ra

DAU = ['>', '<', '=']
# đuôi đơn vị hay đi sau đáp số — cắt đi để so, nhưng KHÔNG cắt chữ đổi nghĩa
DON_VI = (r'(?:số|trang|cột đèn|nhà|cây|viên|cái|con|quả|khối|hình|chữ số|tuổi|m|cm|'
          r'nghìn đồng|nghìn|đồng|đơn vị|phần|lần|giờ|phút|cốc|bạn|ghế|toa|cách)')


def _so(s):
    return re.findall(r'-?\d+', str(s))


def _that(gt, loi):
    """Giá trị này có THẬT trong lời giải của sách không? Không thì đừng dùng."""
    return str(gt).strip() and str(gt).strip() in loi


def _sach(s):
    return ' '.join(str(s).split()).strip(' .;,')


# ── các luật, mỗi luật một khuôn nhận ra được ────────────────────────────────
def r_dien_dau(text, loi):
    """"Điền dấu >, <, =: 352 ▢ 325; 460 ▢ 406" → mỗi cặp một ô BẤM CHỌN."""
    if 'Điền dấu' not in text:
        return None
    cap = re.findall(r'(\d+)\s*▢\s*(\d+)', text)
    if not cap:
        return None
    parts = []
    for a, b in cap:
        m = re.search(rf'\b{a}\s*([<>=])\s*{b}\b', loi)
        if not m:
            return None
        parts.append({'label': f'{a} ▢ {b}', 'value': m.group(1), 'options': DAU})
    return {'parts': parts}


def r_moi_so(text, loi):
    """Đề liệt kê nhiều số, lời giải cũng nhiều phần ngăn bằng ';' — khớp 1-1.

    "Viết thêm số 0 vào bên phải mỗi số: 7 → ?; 9 → ?; 25 → ?; 60 → ?"
      → "70; 90; 250; 600"
    """
    if '▢' in text or 'Điền dấu' in text:
        return None
    ve = [v.strip() for v in loi.split(';') if v.strip()]
    if len(ve) < 2:
        return None
    # nhãn = các số/cụm đề nêu ra, phải đúng bằng số vế của lời giải
    sau = text.split(':', 1)[-1] if ':' in text else text
    muc = [m.strip(' .') for m in re.split(r'[;?]', sau) if re.search(r'\d', m)]
    muc = [re.sub(r'\s*(→|=)\s*\??$', '', m).strip() for m in muc]
    if len(muc) != len(ve):
        return None
    parts = []
    for nhan, v in zip(muc, ve):
        v = _sach(v)
        # bỏ phần giải thích trong ngoặc; lời giải kiểu "452 = 400 + 50 + 2" thì
        # lấy vế phải, còn lại lấy nguyên
        v = re.sub(r'\s*\([^)]*\)\s*$', '', v).strip()
        if '=' in v:
            v = v.split('=', 1)[1].strip()
        # Đáp án phải là SỐ hoặc PHÉP TÍNH thuần. Lời giải kiểu "số đó là 320" hay
        # "40 gồm 4 chục" mà nhét nguyên vào ô thì bé gõ đúng số vẫn bị chấm sai.
        if not re.fullmatch(r'[\d\s+\-×x:/.,]+', v):
            return None
        if not _that(v, loi) or len(v) > 24 or not re.search(r'\d', v):
            return None
        # nhãn phải NGẮN, vì nó là chữ đứng cạnh ô cho bé biết ô này hỏi gì
        if len(nhan) > 22:
            return None
        parts.append({'label': nhan, 'value': v})
    return {'parts': parts}


def r_ba_phong(text, loi):
    """"Số 368 có mấy trăm, mấy chục, mấy đơn vị?" → "3 trăm, 6 chục, 8 đơn vị"."""
    if not re.search(r'mấy trăm.*mấy chục.*mấy đơn vị', text):
        return None
    m = re.match(r'^\s*(\d+)\s*trăm,\s*(\d+)\s*chục,\s*(\d+)\s*đơn vị', loi)
    if not m:
        return None
    return {'parts': [{'label': 'trăm', 'value': int(m.group(1))},
                      {'label': 'chục', 'value': int(m.group(2))},
                      {'label': 'đơn vị', 'value': int(m.group(3))}]}


def r_lon_be(text, loi):
    """"lập số lớn nhất và số bé nhất" → hai ô có nhãn."""
    if not re.search(r'lớn nhất.*bé nhất|bé nhất.*lớn nhất', text):
        return None
    ln = re.search(r'lớn nhất\s*(?:là\s*)?(\d+)', loi)
    bn = re.search(r'bé nhất\s*(?:là\s*)?(\d+)', loi)
    if not (ln and bn):
        m = re.match(r'^\s*(\d+)\s*và\s*(\d+)\s*$', _sach(loi))
        if not m:
            return None
        ln_v, bn_v = m.group(1), m.group(2)
    else:
        ln_v, bn_v = ln.group(1), bn.group(1)
    return {'parts': [{'label': 'số lớn nhất', 'value': int(ln_v)},
                      {'label': 'số bé nhất', 'value': int(bn_v)}]}


def r_day_tiep(text, loi):
    """"Viết tiếp dãy: 2, 4, 6, ▢, ▢, ▢." → "8, 10, 12" (mỗi ▢ một ô)."""
    n_o = text.count('▢')
    if n_o < 1 or 'Điền dấu' in text:
        return None
    ss = _so(loi)
    # lời giải phải là dãy số THUẦN, đúng bằng số ô trống
    if len(ss) != n_o or not re.fullmatch(r'[\d\s,;và.]+', _sach(loi)):
        return None
    return {'parts': [{'label': f'ô trống {i + 1}', 'value': int(v)} for i, v in enumerate(ss)]}


def r_dap_so(text, loi):
    """Một đáp số duy nhất, nằm sau '→' hoặc sau dấu '=' cuối cùng.

    "9 − 4 = 5, thêm 1 → 6 số"          → 6
    "80 − 8 = 72 (nghìn đồng)"          → 72
    "5, 10, ..., 35 → 7 cột đèn"        → 7
    """
    l = _sach(re.sub(r'\s*\([^)]*\)', '', loi))
    # Đơn vị có thể đứng SAU số ("→ 6 số") hoặc TRƯỚC số ("→ số 460")
    m = re.search(rf'→\s*(?:số|là)?\s*(-?\d+)\s*{DON_VI}?\s*$', l) or \
        re.search(rf'=\s*(-?\d+)\s*{DON_VI}?\s*$', l) or \
        re.fullmatch(rf'(?:số\s*)?(-?\d+)\s*{DON_VI}?', l)
    if not m:
        return None
    gt = m.group(1)
    if not _that(gt, loi):
        return None
    # Đề phải hỏi ĐÚNG MỘT việc. Bỏ khi:
    #   · nhiều dấu ? → hỏi nhiều thứ
    #   · còn ô trống ▢ → đề cần điền nhiều ô, một đáp số là thiếu
    #   · nói rõ "HAI số" → B10C4 "viết HAI số tiếp theo" đáp là 20 VÀ 26, máy chỉ
    #     bắt được 26; bé điền đủ hai số lại bị chấm sai.
    #   · hỏi hai đối tượng ("mấy con gà, mấy con vịt?", "mỗi người có mấy cái?")
    #     → một đáp số là thiếu một nửa; B19C4/C5 dính đúng kiểu này.
    if (text.count('?') > 1 or '▢' in text
            or re.search(r'\bHAI số\b|\bhai số tiếp\b', text)
            or len(re.findall(r'\bmấy\b', text)) > 1
            or re.search(r'mỗi người|mỗi bạn có', text)):
        return None
    return {'value': int(gt)}


def r_tim_tat_ca(text, loi):
    """"Tìm TẤT CẢ các số… bằng 6" → "15; 24; 33; 42; 51; 60 — đủ 6 số".

    Cắt ở dấu "—": bên phải là lời đếm ("đủ 6 số"), lấy vào là thừa mất một số.
    Thứ tự không bắt buộc — bé liệt kê kiểu nào cũng được, miễn đủ và không thừa.
    """
    if not re.search(r'TẤT CẢ|tất cả các số', text):
        return None
    trai = _sach(re.split(r'[—–]', loi)[0])
    if not re.fullmatch(r'[\d\s;,và]+', trai):
        return None
    ss = _so(trai)
    if len(ss) < 2:
        return None
    return {'values': [int(x) for x in ss], 'ordered': False}


def r_so_nao(text, loi):
    """"Trong các số 35, 53, 30, 15, 51 — số nào KHÔNG chứa chữ số 5?" → bấm chọn.

    Phương án lấy TỪ CHÍNH ĐỀ BÀI, đáp án lấy từ lời giải và phải nằm trong đó —
    bé bấm một trong những số đề đã nêu, không phải gõ.
    """
    if not re.search(r'số nào', text):
        return None
    m = re.search(r'(?:các số|những số)\s*([\d,\s]+?)\s*[—–-]', text)
    if not m:
        return None
    pa = _so(m.group(1))
    if len(pa) < 3:
        return None
    d = re.match(r'^\s*(?:số\s*)?(\d+)', _sach(loi))
    if not d or d.group(1) not in pa:
        return None
    return {'choice': d.group(1), 'choices': pa}


def r_nhieu_ve(text, loi):
    """Lời giải ngăn bằng ';', MỖI VẾ kết thúc bằng một số → mỗi vế một ô.

    "trong 462, chữ số 6 ở phòng chục → đáng giá 60; trong 620 nó ở phòng trăm
     → đáng giá 600"   →  hai ô: [trong 462] = 60 · [trong 620] = 600

    ĐÃ GỠ KHỎI DANH SÁCH LUẬT — soát tay 51 câu thì thấy sai hàng loạt:
      · "số cuối của vế" thường KHÔNG phải đáp án mà là số trong lời giải thích:
        "75 − 57 = 18 — nằm trong bảng nhân 9" → nó lấy 9 thay vì 18
        "phần hơn = 9 lần số bé; 9 × 5 = 45" → lấy 9 và 45, đáp án thật là 5 và 50
      · NHÃN dựng từ lời giải nên LỘ LUÔN ĐÁP ÁN: ô ghi "[40 gồm 4 chục]" rồi hỏi
        bé điền gì nữa? Nhãn phải lấy từ ĐỀ BÀI, không bao giờ lấy từ lời giải.
    Giữ lại hàm để người sau khỏi nghĩ ra lại cùng một ý và dính lại cùng một lỗi.
    """
    return None
    # (mã cũ giữ nguyên bên dưới, không chạy tới)
    ve = [v.strip() for v in loi.split(';') if v.strip()]
    if not 2 <= len(ve) <= 4:
        return None
    parts = []
    for v in ve:
        v = re.sub(r'\s*\([^)]*\)', '', v).strip()
        # số CUỐI của vế là đáp án của vế ấy
        m = re.search(r'(-?\d+)\s*[^\d]{0,18}$', v)
        if not m:
            return None
        gt = m.group(1)
        # nhãn: cụm mở đầu của vế, cắt ở dấu phẩy / mũi tên đầu tiên
        nhan = _sach(re.split(r'[,→=]', v)[0])
        if not (2 <= len(nhan) <= 22) or not _that(gt, loi):
            return None
        parts.append({'label': nhan, 'value': int(gt)})
    # hai ô mà nhãn trùng nhau thì bé không biết ô nào hỏi gì
    if len({p['label'] for p in parts}) != len(parts):
        return None
    return {'parts': parts}


def r_hai_ben(text, loi):
    """Đề hỏi HAI đối tượng, lời giải ghi rõ nhãn: "gà: 8 : 4 = 2 con; vịt: 2 × 3 = 6 con".

    Nhãn (gà · vịt · em · chị) lấy từ LỜI GIẢI nhưng BẮT BUỘC phải có mặt trong ĐỀ
    BÀI — nên nó là danh từ đề đã nêu, không phải đáp án bị lộ.
    """
    ve = [v.strip() for v in loi.split(';') if v.strip()]
    if len(ve) < 2:
        return None
    parts = []
    for v in ve:
        m = re.match(r'^([A-Za-zÀ-ỹ][A-Za-zÀ-ỹ\s]{0,9}?)\s*:\s*(.+)$', v)
        if not m:
            return None
        nhan, than = m.group(1).strip(), re.sub(r'\s*\([^)]*\)', '', m.group(2))
        if nhan.lower() not in text.lower():
            return None
        d = re.findall(r'=\s*(-?\d+)', than) or re.findall(r'^\s*(-?\d+)', than)
        if not d or not _that(d[-1], loi):
            return None
        parts.append({'label': nhan, 'value': int(d[-1])})
    if len({p['label'] for p in parts}) != len(parts):
        return None
    return {'parts': parts}


# `r_nhieu_ve` ĐÃ BỊ GỠ — xem ghi chú trong hàm. Giữ lại mã để đừng ai viết lại.
# ĐÃ GỠ `r_nhieu_ve` và `r_hai_ben` — cả hai đều suy đáp án từ LỜI VĂN của lời giải
# và cả hai đều sai. Bài học chung, ghi lại để đừng thử lại lần thứ ba:
#   · số cuối một vế thường là số trong lời GIẢI THÍCH, không phải đáp án
#     ("kiến Đen: 5+5+5 = 15 cm → kiến Đỏ xa hơn 16 − 15 = 1 cm" → lấy nhầm 1)
#   · tách thêm ô cho BƯỚC TRUNG GIAN là bịa việc sách không giao
#     (B17C7 chỉ hỏi Cúc, thêm ô cho Bình là đổi đề)
# Suy máy CHỈ dùng được cho những khuôn CỐ ĐỊNH nhận ra chắc chắn. Còn lại phải
# viết tay ở data/lop2_dapan_tay.json — chậm nhưng đúng.
LUAT = [r_dien_dau, r_ba_phong, r_lon_be, r_day_tiep, r_tim_tat_ca, r_so_nao,
        r_moi_so, r_dap_so]
# Câu KHÔNG bao giờ chấm máy: hỏi vì sao, việc làm bằng tay, đề mở
BO_QUA = re.compile(r'vì sao|Vì sao|giải thích|Giải thích|tự nghĩ|Tự nghĩ|kể cho|đố bố mẹ|'
                    r'^Vẽ |^Viết một|^Úp |^Gấp |^Cắt |^Lấy |^Kể ra|^Con hãy|^Đố ')


def suy_ra(c):
    text, loi = c['text'], (c.get('loiChua') or '').strip()
    if not loi or BO_QUA.search(text):
        return None, 'để tự chấm'
    for r in LUAT:
        try:
            k = r(text, loi)
        except Exception:
            k = None
        if k:
            return k, r.__name__
    return None, 'không khớp luật nào'


def main(chi_soat=False):
    tay = json.load(open(TAY, encoding='utf-8')) if os.path.exists(TAY) else {}
    ra, thong_ke = {}, {}
    dong_soat = []
    for tep in sorted(os.listdir(NGUON)):
        if not tep.startswith('DL_KSN2_B'):
            continue
        d = json.load(open(os.path.join(NGUON, tep), encoding='utf-8'))
        for c in d['cau']:
            if c['phan'] != 'luyenTap':
                continue
            ma = f"{d['id']}#{c['id']}"
            if ma in tay:
                k, ten = tay[ma], 'SỬA TAY'
            else:
                k, ten = suy_ra(c)
            thong_ke[ten] = thong_ke.get(ten, 0) + 1
            if k:
                ra[ma] = k
                dong_soat.append((ma, ten, c['text'], c.get('loiChua', ''), k))

    if not chi_soat:
        with open(RA, 'w', encoding='utf-8') as f:
            json.dump(ra, f, ensure_ascii=False, indent=1, sort_keys=True)

    tong = sum(thong_ke.values())
    print(f'{len(ra)}/{tong} câu luyện tập chấm máy được ({len(ra) * 100 // tong}%)')
    for k, v in sorted(thong_ke.items(), key=lambda x: -x[1]):
        print(f'  {v:>4}  {k}')
    return dong_soat


if __name__ == '__main__':
    ds = main('--soat' in sys.argv)
    if '--in' in sys.argv:
        for ma, ten, text, loi, k in ds:
            print(f'\n{ma}  [{ten}]')
            print(f'  ĐỀ  : {text[:100]}')
            print(f'  SÁCH: {loi[:100]}')
            print(f'  MÁY : {json.dumps(k, ensure_ascii=False)[:110]}')
