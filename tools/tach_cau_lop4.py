# -*- coding: utf-8 -*-
"""
LỚP 4 · tách câu luyện tập thành Ô ĐIỀN ĐƯỢC để máy chấm.

    python3 tools/tach_cau_lop4.py            # dựng + in bảng tổng
    python3 tools/tach_cau_lop4.py --soat     # chỉ in, không ghi
    python3 tools/tach_cau_lop4.py --in       # in TỪNG CÂU để soát tay

Nếu không làm bước này thì cả 396 câu luyện tập là "con làm ra vở rồi bấm xem lời
giải" — bé bấm một nút là xong, sổ phụ huynh và bảng cô giáo trống trơn, tức là
không đánh giá được việc học. Lớp 2 và lớp 3 đều đã phải chữa đúng chỗ này.

**DÙNG LẠI luật của lớp 3, không chép.** Năm luật `r_chia_du · r_lon_be · r_moi_muc
· r_day_so · r_mot_dap` cùng ba hàm nền `_sach · _that · _don` mang sẵn bốn bài học
đắt (lấy vế CUỐI chứ không phải vế sau dấu `=` đầu; giữ số dư trong ngoặc; đếm số
phép trong ĐỀ; thấy "ví dụ" là để tự chấm). Chép ra bản thứ hai là bản ấy tụt hậu
ngay lần sửa sau.

── LUẬT RIÊNG CỦA LỚP 4 ──

Lời giải lớp 4 hay viết cả đường đi rồi mới chốt bằng mũi tên:

    C5: lập bảng cặp có tổng 9: 9-0, 8-1, … → cột hiệu: 9, 7, 5, 3 ✓, 1 → số cần tìm là 63.
    C1: được 480; hơn số cũ 480 − 48 = 432 (đúng bằng 9 × 48).

nên thêm ba luật: `r_chot_mui_ten` (lấy vế sau mũi tên CUỐI), `r_hai_viec` (đề hỏi
hai thứ nối bằng "và"/"bao nhiêu … bao nhiêu"), `r_gap_may_lan` (đáp là "gấp 10 lần").

── LUẬT Ô NHẬP (chuẩn mục 7) — quyển này là quyển ĐỌC CHẬM ──

Mọi ô chỉ được là **điền SỐ** hoặc **BẤM CHỌN**. Bé 9-10 tuổi gõ chậm; sai chính tả
một chữ, hay thừa một dấu cách trong biểu thức, là mất điểm oan — mà bài đang kiểm
TOÁN chứ không kiểm kỹ năng gõ. Nên mọi đáp án là CHỮ đều phải thành nút bấm
(`options`), và `web/test/luat_o_nhap.test.mjs` soi ngay khi lớp 4 vào sổ đăng ký.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tach_cau_lop3 import (_sach, _that, _don, BO_QUA, R_MO,        # noqa: E402
                           r_chia_du, r_lon_be, r_moi_muc, r_day_so, r_mot_dap)

NGUON = os.path.join(GOC_KHO, 'data', 'lop4')
RA = os.path.join(GOC_KHO, 'data', 'lop4_dapan_o.json')
TAY = os.path.join(GOC_KHO, 'data', 'lop4_dapan_tay.json')

R_MUI_TEN = re.compile(r'[→⇒]')

# Đơn vị đi sau đáp số. Lớp 3 có danh sách riêng trong `_don`; ở đây phải rộng hơn
# vì sách lớp 4 đo đủ thứ (km, lít, bàn thắng, số hạng, chữ số…). KHÔNG sửa danh
# sách của lớp 3: sửa ở đó là 298 đáp án lớp 3 đổi theo mà chẳng ai yêu cầu.
DON_VI = (r'cm²|dm²|m²|km²|cm|dm|mm|km|m|kg|g|ml|l|lít|tạ|tấn|'
          r'số hạng|chữ số|số|viên|con|cây|bạn|hộp|gói|chiếc|quyển|cuốn|tờ|trang|'
          r'ghế|bàn|đèn|cột|khối|mặt|phần|lần|khấc|độ|'
          r'nghìn đồng|nghìn|đồng|tuổi|năm|giờ|phút|ngày|tuần|tháng|'
          r'học sinh|em|người|bút|thước|vở|hàng|đội|lớp|bao|thùng|kệ|túi')
R_DON_VI = re.compile(rf'\s*(?:{DON_VI})\b\.?$', re.I)
R_SO_THUAN4 = re.compile(r'^[\d\s+\-−×x:/.,()=]+$')


def _don4(v):
    """Như `_don` của lớp 3 nhưng biết nhiều đơn vị hơn. Trả None nếu không phải đáp số."""
    goc = str(v)
    if re.search(r'\(\s*dư\b', goc):
        return None
    s = _sach(re.sub(r'\s*\([^)]*\)\s*', ' ', goc))
    # bỏ phần dẫn trước dấu '=' CUỐI; lấy vế cuối chứ không phải vế sau '=' đầu tiên
    if '=' in s:
        s = s.split('=')[-1]
    elif ':' in s and not re.search(r'\d\s*:\s*\d', s):
        s = s.split(':', 1)[1]
    s = _sach(s)
    truoc = None
    while truoc != s:                       # "42 kg" → "42";  "20 số hạng" → "20"
        truoc = s
        s = _sach(R_DON_VI.sub('', s))
    return s if s and R_SO_THUAN4.fullmatch(s) and re.search(r'\d', s) else None


def _so_don(v):
    """Vế lời giải → MỘT số nguyên, hoặc None."""
    gt = _don4(v)
    if not gt or not re.fullmatch(r'\d[\d\s]*', gt):
        return None
    return int(gt.replace(' ', ''))


# Đuôi KIỂM CHỨNG — sách lớp 4 gần như bài nào cũng đóng lời giải bằng một câu thử
# lại ("Thử lại: 355 − 35 = 320 ✓"). Đó là nhịp SOI, không phải đáp án; để nguyên thì
# mọi luật đếm vế đều thấy hai vế và tưởng đề hỏi hai thứ, rồi bỏ câu về tự chấm.
R_THU_LAI = re.compile(r'\s*(?:Thử lại|Thử|Kiểm chứng|Kiểm tra|Kiểm|Soi lại|Soi)\s*[:.]',
                       re.I)


def _bo_thu_lai(loi):
    m = R_THU_LAI.search(loi)
    return _sach(loi[:m.start()]) if m else _sach(loi)


def _ve_chot(loi):
    """Phần CHỐT của lời giải: sau mũi tên cuối cùng, đã bỏ đuôi kiểm chứng.

    Sách viết cả đường đi rồi mới chốt ("tổng = 45 × 2 = 90 → bao hai = 42 kg; bao
    một = 48 kg"). Đọc từ đầu thì nhãn ô hoá thành "tổng" — một bước trung gian —
    còn đáp số thật thì nằm sau mũi tên.
    """
    s = _bo_thu_lai(loi)
    return _sach(R_MUI_TEN.split(s)[-1]) if R_MUI_TEN.search(s) else s


def _nhan_tu_de(nhan, text):
    """Nhãn ô CHỈ được dùng khi chính chữ ấy có trong ĐỀ.

    Chuẩn mục 7 luật 2: nhãn dựng từ lời giải là cho không bé đáp án. Nhưng lời giải
    lớp 4 hay mở mỗi vế bằng đúng cái tên mà đề đã nêu ("thùng hai = 42; thùng một
    = 54" — đề viết "thùng thứ nhất… thùng thứ hai"). Nhãn như thế là chữ bé ĐÃ ĐỌC
    THẤY, dùng được. Nên lọc bằng chính đề, đừng lọc bằng cảm tính.
    """
    n = _sach(nhan).lower().strip(' :')
    if not 2 <= len(n) <= 24 or re.search(r'\d', n):
        return None
    t = text.lower()
    goc = re.sub(r'\b(?:thứ nhất|thứ hai|một|hai|nhất)\b', '', n).strip()
    if n in t:
        return n
    # "thùng một" ↔ đề viết "thùng thứ nhất": so phần GỐC của cụm
    if goc and len(goc) >= 3 and goc in t:
        return n
    return None


def r_chot_mui_ten(text, loi):
    """Lời giải kể cả đường đi rồi chốt sau mũi tên CUỐI → lấy đúng vế chốt.

        "… → cột hiệu: 9, 7, 5, 3 ✓, 1 → số cần tìm là 63."  → 63

    Lấy vế CUỐI chứ không phải vế đầu: vế đầu là bước trung gian, mà chấm bước trung
    gian là đổi đề. Và chỉ nhận khi vế chốt có ĐÚNG MỘT con số — nhiều số thì không
    biết số nào là đáp, đoán bừa là chấm oan.
    """
    if not R_MUI_TEN.search(loi) or text.count('?') > 1:
        return None
    ve = re.sub(r'\s*\([^)]*\)', ' ', _ve_chot(loi))
    so = re.findall(r'\d[\d\s]*\d|\d', ve)
    if len(so) != 1:
        return None
    gt = _sach(so[0])
    if not _that(gt, loi):
        return None
    return {'value': int(gt.replace(' ', ''))}


def r_gap_may_lan(text, loi):
    """"Xóa chữ số 0 tận cùng thì số đó giảm đi mấy lần?" → "giảm 10 lần" → ô SỐ.

    Đáp là một con số kèm chữ "lần". Ô chỉ nhận con số, còn chữ "lần" nằm ở nhãn —
    bắt bé gõ chữ "lần" là kiểm kỹ năng gõ chứ không kiểm toán.
    """
    if not re.search(r'mấy lần|bao nhiêu lần|gấp mấy', text, re.I):
        return None
    m = re.search(r'(?:gấp|giảm(?:\s+đi)?)\s+(\d+)\s*lần', _sach(loi), re.I)
    if not m:
        return None
    return {'parts': [{'label': 'số lần', 'value': int(m.group(1))}]}


def r_hai_viec(text, loi):
    """Đề hỏi HAI thứ, lời giải hai vế ngăn bằng ';' → hai ô có nhãn từ ĐỀ.

        "Số mới là bao nhiêu và hơn số cũ bao nhiêu đơn vị?"
        "được 480; hơn số cũ 480 − 48 = 432 (đúng bằng 9 × 48)."
        → ô "số mới" = 480 · ô "hơn số cũ" = 432

    Nhãn lấy từ ĐỀ nên là chữ bé đã đọc thấy, không phải đáp án bị lộ (chuẩn mục 7
    luật 2). Không dựng được đủ hai nhãn từ đề thì bỏ — thà tự chấm còn hơn ô không
    nhãn, vì nhiều ô không nhãn thì bé không biết ô nào hỏi gì.
    """
    ve = [v for v in re.split(r';', loi) if v.strip()]
    if len(ve) != 2:
        return None
    NHAN = [(r'số mới', 'số mới'), (r'hơn số cũ|tăng thêm', 'hơn số cũ'),
            (r'kém số (?:đúng|cũ)|giảm đi', 'kém số cũ'),
            (r'chiều dài', 'chiều dài'), (r'chiều rộng', 'chiều rộng'),
            (r'bánh nướng', 'bánh nướng'), (r'bánh dẻo', 'bánh dẻo'),
            (r'con gà', 'số gà'), (r'con chó', 'số chó')]
    nhan = [ten for pat, ten in NHAN if re.search(pat, text, re.I)]
    if len(nhan) != 2:
        return None
    parts = []
    for ten, v in zip(nhan, ve):
        gt = _don(v)
        if not gt or not _that(gt, loi) or not re.fullmatch(r'\d[\d\s]*', gt):
            return None
        parts.append({'label': ten, 'value': int(gt.replace(' ', ''))})
    return {'parts': parts}


def r_hai_ve_co_ten(text, loi):
    """Lời giải hai vế, mỗi vế mở bằng TÊN mà đề đã nêu → hai ô có nhãn.

        đề : "Hai thùng dầu chứa tất cả 96 lít, thùng thứ nhất nhiều hơn… 12 lít."
        giải: "thùng hai = (96 − 12) : 2 = 42; thùng một = 54 (lít)."
        → ô "thùng hai" = 42 · ô "thùng một" = 54

    Nhãn phải có mặt trong ĐỀ (xem `_nhan_tu_de`), nếu không thì bỏ câu về tự chấm.
    Đây là khuôn hay gặp nhất của cả quyển: dạng Tổng - Hiệu, Tổng - Tỉ, Hiệu - Tỉ
    đều trả lời hai số, và sách luôn viết theo đúng nếp này.
    """
    ve = [v for v in re.split(r'[;.]', _ve_chot(loi)) if v.strip()]
    ve = [v for v in ve if re.search(r'\d', v)]
    if len(ve) != 2:
        return None
    parts = []
    for v in ve[:2]:
        m = re.match(r'\s*([^=:]{2,26}?)\s*[=:]\s*(.+)$', v)
        if not m:
            return None
        nhan = _nhan_tu_de(m.group(1), text)
        gt = _so_don(m.group(2))
        if not nhan or gt is None or not _that(gt, loi):
            return None
        parts.append({'label': nhan, 'value': gt})
    if len({p['label'] for p in parts}) != 2:
        return None
    return {'parts': parts}


def r_tim_hai_so(text, loi):
    """"Tìm hai số có tổng… và hiệu/tỉ số…" → hai ô "số bé" và "số lớn".

        giải: "tổng phần 5; một phần 6 → hai số là 12 và 18."  → bé 12 · lớn 18

    Nhãn "số bé"/"số lớn" là từ vựng chính của cả chương, và sắp theo GIÁ TRỊ chứ
    không theo thứ tự sách viết — sách có chỗ viết số lớn trước, gán theo thứ tự
    xuất hiện là đảo đáp án của bé.
    """
    if not re.search(r'tìm hai số|hai số có tổng|tính hai số', text, re.I):
        return None
    m = re.search(r'hai số (?:là|bằng)?\s*([\d\s]+)\s*và\s*([\d\s]+)',
                  _bo_thu_lai(loi), re.I)
    if not m:
        return None
    a, b = _so_don(m.group(1)), _so_don(m.group(2))
    if a is None or b is None or a == b:
        return None
    be, lon = min(a, b), max(a, b)
    if not (_that(be, loi) and _that(lon, loi)):
        return None
    return {'parts': [{'label': 'số bé', 'value': be},
                      {'label': 'số lớn', 'value': lon}]}


def _muc_cua_de(text):
    """Đề liệt kê mấy mục? Trả danh sách NHÃN, hoặc [].

        'Viết số: "sáu trăm linh hai nghìn…" ; "ba triệu hai trăm nghìn".'
            → ['sáu trăm linh hai nghìn…', 'ba triệu hai trăm nghìn']
        'Đọc các số: 24 358 ; 1 745 230.'  → ['24 358', '1 745 230']

    Ưu tiên cụm trong NGOẶC KÉP — sách dùng ngoặc kép để tách hẳn từng mục, và cụm
    ấy chính là chữ bé nhìn thấy nên dùng làm nhãn ô là đúng luật.
    """
    trong_nhay = re.findall(r'"([^"]{2,60})"', text)
    if len(trong_nhay) >= 2:
        return [_sach(x) for x in trong_nhay]
    sau = text.split(':', 1)[-1] if ':' in text else ''
    muc = [_sach(m).strip(' "“”.') for m in re.split(r'\s;\s', sau)]
    muc = [m for m in muc if m]
    return muc if len(muc) >= 2 else []


def r_hai_muc_de(text, loi):
    """Đề liệt kê n mục, phần chốt cho n số → mỗi mục một ô, nhãn lấy từ ĐỀ.

        đề : 'Viết số: "sáu trăm linh hai nghìn không trăm bốn mươi" ; "ba triệu…"'
        chốt: '602 040 ; 3 200 000'
        → ô "sáu trăm linh hai nghìn…" = 602040 · ô "ba triệu…" = 3200000

    Khác `r_moi_muc` của lớp 3 đúng một chỗ: lớp 3 đòi mỗi mục phải CHỨA CHỮ SỐ, nên
    mọi đề đọc - viết số bằng lời đều trượt. Ở đây nhãn được phép là chữ.
    """
    muc = _muc_cua_de(text)
    if not 2 <= len(muc) <= 4:
        return None
    ve = [v for v in re.split(r'[;,]', _ve_chot(loi)) if re.search(r'\d', v)]
    if len(ve) != len(muc):
        return None
    parts = []
    for nhan, v in zip(muc, ve):
        gt = _so_don(v)
        if gt is None or not _that(gt, loi) or not 2 <= len(nhan) <= 46:
            return None
        parts.append({'label': nhan, 'value': gt})
    if len({p['label'] for p in parts}) != len(parts):
        return None
    return {'parts': parts}


def r_nhieu_ve_co_ten(text, loi):
    """Phần chốt có n vế dạng "tên = số", mọi tên đều có trong ĐỀ → n ô có nhãn.

    Mở rộng `r_hai_ve_co_ten` cho bài ba số (chương 6 và 7 đều có), nhưng vẫn đòi
    MỌI nhãn phải xuất hiện trong đề — một nhãn không kiểm được là bỏ cả câu, vì ô
    không nhãn thì bé không biết ô ấy hỏi gì (chuẩn mục 7 luật 4).
    """
    ve = [v for v in re.split(r'[;]', _ve_chot(loi)) if re.search(r'\d', v)]
    if not 3 <= len(ve) <= 4:
        return None
    parts = []
    for v in ve:
        m = re.match(r'\s*([^=:]{2,26}?)\s*[=:]\s*(.+)$', v)
        if not m:
            return None
        nhan = _nhan_tu_de(m.group(1), text)
        gt = _so_don(m.group(2))
        if not nhan or gt is None or not _that(gt, loi):
            return None
        parts.append({'label': nhan, 'value': gt})
    if len({p['label'] for p in parts}) != len(parts):
        return None
    return {'parts': parts}


def r_liet_ke(text, loi):
    """"Tìm TẤT CẢ các số…" / "Liệt kê…" → một ô nhận cả danh sách, KHÔNG xét thứ tự.

        "bốn số: 70, 61, 52, 43"   → values [70, 61, 52, 43], ordered False
        "x = 1 ; 4 ; 7"            → values [1, 4, 7]

    Khác `r_day_so` của lớp 3 ở đúng một chỗ: dãy số thì THỨ TỰ CÓ NGHĨA, còn "tìm
    tất cả" là một TẬP HỢP — bắt bé viết đúng thứ tự sách in là chấm oan em nào liệt
    kê từ bé đến lớn.

    Nếu đề nêu rõ có mấy số ("bốn số", "Có bao nhiêu…") thì phải khớp số lượng ấy.
    """
    if not re.search(r'tất cả các số|tất cả các chữ số|liệt kê|Liệt kê|'
                     r'tìm các số|Tìm các số|những số nào', text, re.I):
        return None
    chot = re.sub(r'\s*\([^)]*\)', ' ', _ve_chot(loi))
    chot = re.sub(r'^[^:]{0,24}:', '', chot)          # bỏ nhãn dẫn "bốn số:", "x ="
    chot = re.sub(r'^\s*x\s*=\s*', '', chot, flags=re.I)
    if not re.fullmatch(r'[\d\s,;và]+', chot.strip(' .')):
        return None
    so = [int(x.replace(' ', '')) for x in re.findall(r'\d[\d\s]*\d|\d', chot)]
    if not 2 <= len(so) <= 12 or len(set(so)) != len(so):
        return None
    m = re.search(r'\b(hai|ba|bốn|năm|sáu|bảy|tám|chín|\d+)\s+số\b', _ve_chot(loi))
    if m:
        CHU = {'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5, 'sáu': 6, 'bảy': 7,
               'tám': 8, 'chín': 9}
        n = CHU.get(m.group(1), None)
        n = int(m.group(1)) if n is None and m.group(1).isdigit() else n
        if n and n != len(so):
            return None
    return {'values': so, 'ordered': False}


def r_mot_so_co_don_vi(text, loi):
    """Đề hỏi MỘT thứ, lời giải chốt bằng một con số kèm đơn vị → một ô SỐ.

        "40 × 3 = 120 km."          → 120
        "(100 − 5) : 5 + 1 = 20 số hạng."  → 20
        "40 : 5 + 1 = 9 cây (8 khoảng, trồng cả hai đầu)."  → 9

    Rộng hơn `r_mot_dap` của lớp 3 đúng ở chỗ ĐƠN VỊ (`_don4`). Vẫn giữ chốt "đề chỉ
    có một dấu hỏi", vì đề hỏi hai thứ mà chỉ một ô là sai (chuẩn mục 7 luật 3).
    """
    if text.count('?') > 1:
        return None
    ve = [v for v in re.split(r'[;.]', _ve_chot(loi)) if re.search(r'\d', v)]
    if len(ve) != 1:
        return None
    gt = _so_don(ve[0])
    if gt is None or not _that(gt, loi):
        return None
    return {'value': gt}


# Luật HẸP trước, luật RỘNG sau — luật rộng chạy trước sẽ nuốt mất ngữ cảnh mà luật
# hẹp cần (chuẩn mục 5). Hai luật "một ô" rộng nhất nên xếp cuối.
LUAT = [r_chia_du, r_lon_be, r_gap_may_lan, r_hai_viec, r_tim_hai_so,
        r_hai_ve_co_ten, r_nhieu_ve_co_ten, r_moi_muc, r_hai_muc_de,
        r_day_so, r_liet_ke, r_chot_mui_ten,
        r_mot_dap, r_mot_so_co_don_vi]

# Chỉ những đề THẬT SỰ không đo được mới bỏ hẳn: đề mở, việc làm bằng tay, tự sáng
# tác. Đề "vì sao / giải thích" thì KHÔNG bỏ — lớp 3 đã học: câu ấy hỏi MỘT con số
# kèm MỘT lời giải thích, nên tách con số ra là đo được ngay, còn lời giải thích để
# bé đối chiếu với `solutionNarrative`. Bỏ cả nhóm là mất trắng 28 câu như lượt đầu.
KHONG_DO_DUOC = re.compile(
    r'^Vẽ |^Kẻ |^Dùng compa|^Úp |^Gấp |^Cắt |^Đặt tên|^Trình bày|'
    r'tự nghĩ|Tự nghĩ|tự đặt|Tự đặt|tự tìm|Tự tìm|nghĩ ra|'
    r'hỏi bố mẹ|cùng bố mẹ|kể lại|Kể lại')

# Câu ĐÃ XÉT và kết luận KHÔNG chấm máy được — khai đích danh để lần sau khỏi tưởng
# là bỏ sót, và để bảng tổng nói đúng "cố ý" thay vì "chưa khớp luật nào".
# Bốn câu, mỗi câu một lý do khác nhau; cả bốn đều thuộc nhóm chuẩn mục 7 luật 6.
CO_Y = {
    'DL:KSN4.B01#C1': 'đọc số thành CHỮ — "một triệu bảy trăm bốn mươi lăm nghìn" và '
                      '"…bốn mươi năm nghìn" đều là cách đọc bé được dạy, ép một '
                      'cách viết là chấm oan',
    'DL:KSN4.B14#C3': 'nêu quy luật bằng MỘT CÂU VĂN — mỗi bé diễn đạt một kiểu, mà '
                      'chính đề đang rèn việc NÓI được quy luật thành lời',
    'DL:KSN4.B18#C7': 'hỏi từng số hạng "gánh" cho ai — đáp là lời giải thích, không '
                      'có con số nào để tách ra làm ô',
    'DL:KSN4.B40#C4': 'việc làm bằng tay: vẽ tam giác rồi dùng ê ke hạ đường cao',
}


def suy_ra(c, ma=''):
    text, loi = c['text'], (c.get('loiChua') or '').strip()
    if not loi:
        return None, 'không có lời chữa'
    if ma in CO_Y:
        return None, f'CỐ Ý để tự chấm ({CO_Y[ma]})'
    if KHONG_DO_DUOC.search(text):
        return None, 'CỐ Ý để tự chấm (đề mở · việc làm bằng tay)'
    if R_MO.search(loi):
        return None, 'CỐ Ý để tự chấm (nhiều đáp án đều đúng)'
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
    tay = {k: v for k, v in tay.items() if not k.startswith('_')}
    ra, thong_ke, soat, canh_bao = {}, {}, [], []
    for tep in sorted(os.listdir(NGUON)):
        if not tep.startswith('DL_KSN4_B'):
            continue
        d = json.load(open(os.path.join(NGUON, tep), encoding='utf-8'))
        for c in d['cau']:
            if c['phan'] != 'luyenTap':
                continue
            ma = f"{d['id']}#{c['id']}"
            if ma in tay:
                k, ten = tay[ma], 'VIẾT TAY'
                # TỰ SOÁT BÀI CỦA MÌNH: mọi giá trị viết tay phải xuất hiện trong
                # ĐỀ hoặc LỜI GIẢI của sách. Chốt này bắt lỗi thật ở lớp 2 (sách
                # viết "một phần tư" bằng chữ, người soạn ghi 4).
                nguon = (c.get('loiChua') or '') + ' ⟂ ' + c['text']
                for gt in ([p['value'] for p in k['parts']] if 'parts' in k
                           else k.get('values') or [k.get('value')]):
                    if gt is not None and not _that(gt, nguon):
                        canh_bao.append(f'{ma}: viết tay "{gt}" mà sách không có '
                                        f'chữ ấy ở đề lẫn lời giải')
            else:
                k, ten = suy_ra(c, ma)
            thong_ke[ten] = thong_ke.get(ten, 0) + 1
            if k:
                ra[ma] = k
                soat.append((ma, ten, c['text'], c.get('loiChua', ''), k))

    if not chi_soat:
        with open(RA, 'w', encoding='utf-8') as f:
            json.dump(ra, f, ensure_ascii=False, indent=1, sort_keys=True)

    for c in canh_bao[:20]:
        print(f'  ⚠ {c}')
    tong = sum(thong_ke.values())
    o = sum(len(v['parts']) if 'parts' in v else 1 for v in ra.values())
    nut = sum(1 for v in ra.values() for p in v.get('parts', []) if p.get('options'))
    print(f'{len(ra)}/{tong} câu luyện tập chấm máy được ({len(ra) * 100 // tong}%)'
          f' · {o} ô nhập · {nut} ô bấm chọn')
    for k, v in sorted(thong_ke.items(), key=lambda x: -x[1]):
        print(f'  {v:>4}  {k}')
    return soat, canh_bao


if __name__ == '__main__':
    ds, cb = main('--soat' in sys.argv)
    if '--in' in sys.argv:
        for ma, ten, text, loi, k in ds:
            print(f'\n{ma}  [{ten}]')
            print(f'  ĐỀ  : {text[:130]}')
            print(f'  SÁCH: {loi[:130]}')
            print(f'  MÁY : {json.dumps(k, ensure_ascii=False)[:150]}')
    raise SystemExit(1 if cb else 0)
