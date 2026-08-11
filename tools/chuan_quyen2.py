# -*- coding: utf-8 -*-
"""
BƯỚC 3 — chuyển bản trích thô thành dữ liệu bài học của phần mềm.

    python3 tools/chuan_quyen2.py

NGUYÊN TẮC AN TOÀN: thà để con TỰ CHẤM còn hơn máy chấm SAI.

Lời chữa trong sách là văn xuôi, chứa cả các con số trung gian của phép tính
("10 × a − a = 9 × a = 27,9 → a = 3,1"). Đoán bừa "con số cuối cùng" là đáp án thì
sẽ có câu con làm đúng mà máy báo sai — hỏng tệ nhất, vì con mất niềm tin và cổng
mở khoá chặn oan. Ở Quyển 1 đã dính đúng lỗi này (90 câu).

Nên chỗ nào rút được đáp số RÕ RÀNG thì máy chấm; chỗ nào không chắc thì để
`tuluan` — con làm ra nháp, xem lời chữa của sách rồi tự chấm theo barem. Kiểu này
vốn đã đúng tinh thần Quyển 2, không phải giải pháp chữa cháy.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'data', 'quyen2_tho.json')
RA_DIR = os.path.join(GOC_KHO, 'web', 'public', 'content', 'quyen2')
RA_DATA = os.path.join(GOC_KHO, 'data', 'quyen2')

# Đáp án người đọc lời chữa rồi khai tay — 212 câu mà luật máy không dám đoán.
# Xem tools/dapan_quyen2.py (bản vá nóng) và data/quyen2_dapan_tay.json.
_TAY_TEP = os.path.join(GOC_KHO, 'data', 'quyen2_dapan_tay.json')
TAY = {k: v for k, v in json.load(open(_TAY_TEP, encoding='utf-8')).items()
       if not k.startswith('_')} if os.path.exists(_TAY_TEP) else {}

# Vòng đấu n dùng chuyên đề của chương n Quyển 1 → mở khi xong chương ấy.
# (14 vòng ↔ 14 chương; sách ghi rõ ở dòng "Chuyên đề: … (Chương k Quyển 1 …)")
R_CHUONG_Q1 = re.compile(r'Chương\s+(\d+)\s+Quyển\s+1')
# Đề trộn và kỳ thi thử PHỦ NHIỀU CHƯƠNG: "rút từ Chương 1 - 2 - 3",
# "phủ trọn Chương 1 đến Chương 11". Mở khoá phải theo chương CAO NHẤT nó phủ.
# Không bắt được thì chuongQ1 = null và khối mở tự do — con mới xong chương 1 đã
# vào được kỳ chung kết phủ 14 chương (lỗi này chỉ lộ khi chạy thử end-to-end).
# Bắt cả hai cách sách viết phạm vi:
#   "Chương 1 đến Chương 11"  → 1, 11
#   "Chương 1 - 2 - 3"        → 1, 2, 3   (số 2 và 3 KHÔNG đứng sau chữ "Chương")
R_MOI_CHUONG = re.compile(r'Chương\s+((?:\d+\s*[-–]\s*)*\d+)')
R_PHUT = re.compile(r'(\d+)\s*phút')
R_THANG = re.compile(r'thang\s*điểm\s*(\d+)')

# Chỗ lời chữa chuyển sang bình luận — cắt ở đây để lấy phần đáp án.
DUNG = re.compile(r'(Mất điểm nếu|Bẫy CĐ-|Câu "sạch"|Câu “sạch”|Thử lại|Lưu ý|Khác Câu)')

# Ba dạng đáp số CHẮC CHẮN, đo trên chính dữ liệu:
#   1. câu cuối kết bằng "= <số>" kèm đơn vị tuỳ ý   → "… t = 5 : 5 = 1 (giờ)."
#   2. lời chữa MỞ ĐẦU bằng đáp số rồi mới giải thích → "25,47 — đọc …"
#   3. ghi thẳng "Đáp số: <số>"
# Không nhận dạng nào khác: đoán thêm là bắt đầu vơ phải số trung gian của phép tính.
R_KET_BANG = re.compile(r'=\s*(-?\d[\d.,]*)\s*(?:\([^)]{0,14}\)|[a-zA-ZÀ-ỹ%²³/ ]{0,12})?\s*[.;]?\s*$')
R_MO_DAU   = re.compile(r'^(-?\d[\d.,]*)\s*(?:—|-|\.|;)')
R_DAP_SO   = re.compile(r'[Đđ]áp số:?\s*(-?\d[\d.,]*)')
# Đáp án PHÂN SỐ ("5/6") và TỈ SỐ ("9 : 8") — flow.js chấm được cả hai, bỏ qua thì
# câu dễ như "1/2 + 1/3" lại rơi vào tự luận oan.
R_PHAN_SO  = re.compile(r'(?:^|=\s*)(\d+\s*/\s*\d+)\s*[.;]?\s*$')


def so_sach(s):
    """'3,1' → '3,1' (giữ dấu phẩy thập phân kiểu Việt); bỏ dấu chấm phân nhóm."""
    s = s.strip().rstrip('.,;')
    if re.fullmatch(r'\d{1,3}(\.\d{3})+', s):     # 1.234 → 1234
        return s.replace('.', '')
    return s


# Câu đòi HAI GIÁ TRỊ trở lên ("Tìm hai số", "mỗi bạn bao nhiêu") — gói vào một
# đáp số là chấm oan con viết đủ cả hai. Soi mắt 20 mẫu mới lộ ra: câu "Tổng 84,
# hiệu 16, tìm hai số" bị rút thành 50, con viết "34 và 50" sẽ bị báo sai.
R_NHIEU_GIA_TRI = re.compile(
    r'(tìm hai|tính hai|hai số|hai bạn|hai kho|hai thùng|hai đội|hai vòi|hai người|hai xe'
    r'|mỗi (bạn|người|kho|xe|đội|lớp|thùng|vòi|loại|số|phần)'
    r'|tìm (tuổi|số) .+ và |, .+ và .+\?)', re.I)
# Lời chữa nêu từ hai kết quả trở lên: "số bé = 34; số lớn = 50"
R_HAI_KET = re.compile(r'=\s*-?\d[\d.,]*\s*[;,]\s*[^=]{0,30}=\s*-?\d')


def rut_dap_so(loi_chua, de_bai=''):
    """
    Rút đáp số nếu CHẮC CHẮN, không thì trả None → câu ấy để con tự chấm.

    Loại thẳng hai kiểu không gói được thành một đáp số:
      · nhiều ý a) b) c)  — đáp án là mấy dòng, không phải một số
      · dãy so sánh/xếp thứ tự (có < hoặc >) — đáp án là cả một dãy
    """
    loi = DUNG.split(loi_chua)[0].strip()
    if not loi:
        return None
    if re.search(r'\b[b-d]\)', loi):
        return None
    if re.search(r'[<>]', loi):
        return None
    if R_NHIEU_GIA_TRI.search(de_bai or ''):
        return None
    if R_HAI_KET.search(loi):
        return None

    m = R_DAP_SO.search(loi)
    if m:
        return so_sach(m.group(1))

    cau_cuoi = re.split(r'(?<=[.;])\s+', loi)[-1].strip()
    m = R_KET_BANG.search(cau_cuoi)
    if m:
        return so_sach(m.group(1))

    m = R_MO_DAU.match(loi)
    if m:
        return so_sach(m.group(1))

    m = R_PHAN_SO.search(cau_cuoi)
    if m:
        return m.group(1).replace(' ', '')
    return None


def kieu_khoi(loai, so):
    return {'vong': 'V', 'detron': 'T', 'thithu': 'K'}[loai] + f'{so:02d}'


def dung_khoi(loai, k):
    ma = kieu_khoi(loai, k['so'])
    mo = k.get('moTa', '')
    if loai == 'vong':
        m = R_CHUONG_Q1.search(mo)
        chuong = int(m.group(1)) if m else k['so']        # vòng n ↔ chương n
    else:
        cac = [int(x) for cum in R_MOI_CHUONG.findall(mo)
               for x in re.findall(r'\d+', cum)]
        # Kỳ chung kết không liệt kê chương nào trong dòng mô tả — nó là trận cuối,
        # phủ trọn cả 14 chương (sách nói ở phần luật).
        chuong = max(cac) if cac else 14
    phut = int(R_PHUT.search(mo).group(1)) if R_PHUT.search(mo) else None
    thang = int(R_THANG.search(mo).group(1)) if R_THANG.search(mo) else len(k['cau'])

    bay_theo_cau = {}
    for b in k.get('bay', []):
        for n in b.get('cacCau', [b.get('cau')]):
            bay_theo_cau.setdefault(n, []).append(b['ma'])

    cau = []
    for c in k['cau']:
        dap = rut_dap_so(c['dap'], c['de'])
        it = {
            'id': c['ma'],
            'so': c['so'],
            'muc': c['muc'],
            'de': (c.get('de_phu') or ''),
            'text': c['de'],
            'loiChua': c['dap'],
            'bay': bay_theo_cau.get(c['so'], []),
        }
        # SỔ TAY ĐI TRƯỚC LUẬT MÁY. Người đã đọc lời chữa rồi khai đáp án thì cứ theo
        # người; luật rút tự động chỉ lo phần còn lại. Không có nhánh này thì chạy lại
        # bộ dựng là xoá sạch 212 đáp án viết tay — mà dữ liệu vẫn hợp lệ, không báo gì.
        khoa = f"{ma}#{c['ma']}"
        if khoa in TAY:
            it['answerKey'] = TAY[khoa]['answerKey']
            if TAY[khoa].get('choices'):
                it['format'] = 'mcq'
                it['choices'] = TAY[khoa]['choices']
        elif dap is not None:
            it['answerKey'] = {'value': dap}
        else:
            it['tuLuan'] = True
        cau.append(it)

    return {
        'id': f'DR:KSN5Q2.{ma}',
        'quyen': 2,
        'loai': loai,
        'so': k['so'],
        'ten': k['ten'],
        'moTa': mo,
        'chuongQ1': chuong,
        'phut': phut,
        'thang': thang,
        'dat': round(thang * 0.8) if thang else None,
        'man': k.get('man', {}),
        'cau': cau,
        'bay': k.get('bay', []),
    }


def main():
    B = json.load(open(NGUON, encoding='utf-8'))
    os.makedirs(RA_DIR, exist_ok=True)
    os.makedirs(RA_DATA, exist_ok=True)

    khoi, may, tu = [], 0, 0
    for loai in ('vong', 'detron', 'thithu'):
        for k in B[loai]:
            d = dung_khoi(loai, k)
            khoi.append(d)
            may += sum(1 for c in d['cau'] if 'answerKey' in c)
            tu += sum(1 for c in d['cau'] if c.get('tuLuan'))
            ten = d['id'].replace('DR:', 'DR_').replace('.', '_') + '.json'
            for thu_muc in (RA_DIR, RA_DATA):
                with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False, indent=1)

    # hồ sơ bẫy + thẻ chiến thuật: hai tệp tra cứu dùng chung
    for ten, du_lieu in (('ho_so_bay.json', B['hoSo']),
                         ('the_chien_thuat.json', B['the']),
                         ('bai_ky_nang.json', B['kyNang'])):
        for thu_muc in (RA_DIR, RA_DATA):
            with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as f:
                json.dump(du_lieu, f, ensure_ascii=False, indent=1)

    # chỉ mục
    idx = [{'id': d['id'], 'loai': d['loai'], 'so': d['so'], 'ten': d['ten'],
            'chuongQ1': d['chuongQ1'], 'phut': d['phut'], 'thang': d['thang'],
            'dat': d['dat'], 'soCau': len(d['cau'])} for d in khoi]
    for thu_muc in (RA_DIR, RA_DATA):
        with open(os.path.join(thu_muc, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump(idx, f, ensure_ascii=False, indent=1)

    print(f'đã ghi {len(khoi)} khối vào {RA_DIR}')
    print(f'  máy chấm {may} câu · tự luận {tu} câu · tổng {may + tu}')


if __name__ == '__main__':
    main()
