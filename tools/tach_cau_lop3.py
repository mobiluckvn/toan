# -*- coding: utf-8 -*-
"""
LỚP 3 · tách câu luyện tập thành Ô ĐIỀN ĐƯỢC để máy chấm.

    python3 tools/tach_cau_lop3.py            # dựng + in bảng tổng
    python3 tools/tach_cau_lop3.py --soat     # chỉ in, không ghi
    python3 tools/tach_cau_lop3.py --in       # in TỪNG CÂU để soát tay

Vì sao cần: cả 307 câu luyện tập đang là "con làm ra vở rồi mở lời giải tự so". Bé
bấm một nút là xong, không ai biết bé có làm hay không — sổ phụ huynh và bảng cô giáo
không thấy gì, tức là KHÔNG đánh giá được việc học. Đúng vấn đề lớp 2 đã chữa.

Cách làm: một câu của sách thường chứa NHIỀU việc nhỏ ("Tách các số thành tổng theo
hàng: 2 435; 5 208"). Tách thành nhiều Ô có nhãn riêng, mỗi ô một đáp án — bé điền
từng ô, máy chấm từng ô. Dùng `answerKey.parts` của bộ chấm sẵn có, không viết bộ
chấm mới.

BA NGUYÊN TẮC, vi phạm là bỏ câu ấy về tự chấm:
  1. KHÔNG BAO GIỜ tự nghĩ ra đáp án. Mọi giá trị rút từ lời giải của sách.
  2. Giá trị rút ra phải XUẤT HIỆN NGUYÊN VĂN trong lời giải (hàm `_that`).
  3. NHÃN Ô lấy từ ĐỀ BÀI, không lấy từ lời giải — nhãn dựng từ lời giải là cho
     không bé đáp án.
Chấm sai một câu là bé mất tin vào cả phần mềm; thà để tự chấm còn hơn.

── HAI LUẬT LỚP 2 ĐÃ THỬ RỒI GỠ, ĐỪNG DỰNG LẠI ──

`tools/tach_cau_lop2.py` giữ nguyên mã của `r_nhieu_ve` và `r_hai_ben` kèm lý do:
  · "số cuối của một vế" thường là số trong lời GIẢI THÍCH chứ không phải đáp án
  · tách thêm ô cho BƯỚC TRUNG GIAN là bịa việc sách không giao
Cả hai đều suy đáp án từ LỜI VĂN của lời giải, và cả hai đều sai hàng loạt. Suy máy
CHỈ dùng được cho khuôn CỐ ĐỊNH nhận ra chắc chắn; còn lại viết tay, chậm nhưng đúng.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'data', 'lop3')
RA = os.path.join(GOC_KHO, 'data', 'lop3_dapan_o.json')
TAY = os.path.join(GOC_KHO, 'data', 'lop3_dapan_tay.json')   # viết tay, đè lên bản suy

# Câu KHÔNG bao giờ chấm máy: hỏi vì sao, việc làm bằng tay, đề mở.
# Giữ tự chấm là CỐ Ý, không phải bỏ sót — chuẩn mục 7 luật 6.
BO_QUA = re.compile(
    r'vì sao|Vì sao|giải thích|Giải thích|đố|Đố|tự nghĩ|Tự nghĩ|kể|Kể|'
    r'^Vẽ |^Dùng compa|^Kẻ |^Úp |^Gấp |^Cắt |^Đặt tên|^Trình bày|'
    r'nghĩ ra|hỏi bố mẹ|cùng bố mẹ|con thử|Con thử|'
    r'Đúng hay sai|đúng hay sai')          # hỏi hai việc một lúc: xét đúng/sai RỒI sửa

# Lời giải nêu MỘT CÁCH LÀM trong nhiều cách đúng — chấm đúng mỗi con số ấy là chấm
# oan mọi đáp án hợp lệ khác. Đề "viết một số chia 6 dư 1 lớn hơn 30" thì 37, 43, 49…
# đều đúng, mà sách chỉ ghi "ví dụ 6 × 6 + 1 = 37".
R_MO = re.compile(r'ví dụ|Ví dụ|chẳng hạn|Chẳng hạn|tuỳ|tùy|có thể')

# Lời giải là CÂU CHỮ chứ không phải đáp số — không nhét nguyên vào ô được.
R_SO_THUAN = re.compile(r'^[\d\s+\-−×x:/.,()=]+$')


def _sach(s):
    return ' '.join(str(s).split()).strip(' .;,')


def _that(gt, loi):
    """Giá trị này có THẬT trong lời giải của sách không? Không thì đừng dùng.

    So KHÔNG phân biệt hoa thường: sách viết hoa để nhấn ("cửa PHẢI", "CÓ thuộc",
    "PHẠM LUẬT") còn khoá thì viết thường cho khớp chữ trên nút bấm. Bộ chấm cũng
    so không phân biệt hoa thường, nên chốt này phải theo cùng một luật — chặt hơn
    bộ chấm thì nó đỏ oan chính những khoá đúng.
    """
    g = str(gt).strip().lower()
    l = str(loi).lower()
    if not g:
        return False
    # so cả bản bỏ khoảng trắng, vì số Việt viết "5 321" mà đôi chỗ ghi "5321"
    return g in l or g.replace(' ', '') in l.replace(' ', '')


def _don(v):
    """Dọn một vế lời giải về phần ĐÁP SỐ, hoặc trả None nếu không phải đáp số."""
    goc = str(v)
    # "13 : 4 = 3 (dư 1)" — số dư là MỘT PHẦN của đáp án, mà bỏ ngoặc là mất nó.
    # Đề "viết chính danh" hỏi cả thương lẫn dư; chấm mỗi thương là đổi đề. Trả về
    # None để câu ấy về tự chấm hoặc chờ viết tay.
    if re.search(r'\(\s*dư\b', goc):
        return None
    v = _sach(re.sub(r'\s*\([^)]*\)\s*', ' ', goc))
    if ':' in v:
        v = v.split(':', 1)[1]
    # LẤY VẾ CUỐI, không phải vế sau dấu = ĐẦU TIÊN. Lời giải hay viết cả đường đi:
    # "12 × 3 = 30 + 6 = 36" — cắt ở dấu = đầu thì ô nhận đáp án "30 + 6 = 36",
    # bé gõ đúng 36 vẫn bị chấm sai.
    if '=' in v:
        v = v.split('=')[-1]
    v = _sach(v)
    # bỏ đuôi đơn vị hay đi sau đáp số
    v = re.sub(r'\s*(?:cm²|cm|dm|m²|m|kg|g|ml|l|viên|con|cây|bạn|hộp|trang|chữ số|'
               r'nghìn đồng|nghìn|đồng|tuổi|quyển|cốc|khối|phần|lần|số|phút|giờ)\b\.?$',
               '', v, flags=re.I)
    v = _sach(v)
    return v if v and R_SO_THUAN.fullmatch(v) and re.search(r'\d', v) else None


def r_moi_muc(text, loi):
    """Đề liệt kê n mục, lời giải n vế ngăn bằng ';' — khớp 1-1, mỗi mục một ô.

    "Tách các số thành tổng theo hàng: 2 435; 5 208."
      → "2 435 = 2 000 + 400 + 30 + 5; 5 208 = 5 000 + 200 + 8."
      → hai ô, nhãn "2 435" và "5 208", đáp "2 000 + 400 + 30 + 5" và "5 000 + 200 + 8"

    Nhãn lấy từ ĐỀ (phần sau dấu hai chấm), nên nó là thứ bé đã đọc thấy chứ không
    phải đáp án bị lộ.
    """
    ve = [v for v in re.split(r';', loi) if v.strip()]
    if not 2 <= len(ve) <= 5:
        return None
    sau = text.split(':', 1)[-1] if ':' in text else text
    muc = [_sach(m) for m in re.split(r'[;?]', sau) if re.search(r'\d', m)]
    muc = [re.sub(r'\s*(?:→|=)\s*\??$', '', m).strip(' "“”') for m in muc]
    if len(muc) != len(ve):
        return None
    parts = []
    for nhan, v in zip(muc, ve):
        gt = _don(v)
        # nhãn phải NGẮN: nó là chữ đứng cạnh ô cho bé biết ô này hỏi gì
        if not gt or not _that(gt, loi) or len(gt) > 26 or not (1 <= len(nhan) <= 26):
            return None
        parts.append({'label': nhan, 'value': gt})
    if len({p['label'] for p in parts}) != len(parts):
        return None
    return {'parts': parts}


def r_day_so(text, loi):
    """"Viết tiếp 3 số của dãy…" / "Liệt kê các số…" → một ô nhận cả dãy.

    Bộ chấm có sẵn khoá `values`: bé viết "18, 22, 26" hay "18; 22; 26" đều nhận,
    thứ tự thì theo `ordered` — dãy số thì THỨ TỰ CÓ NGHĨA nên bắt đúng thứ tự.
    """
    if not re.search(r'viết tiếp|Viết tiếp|liệt kê|Liệt kê|viết \d+ số|Viết \d+ số', text):
        return None
    l = _sach(loi)
    if not re.fullmatch(r'[\d\s,;.]+', l):
        return None
    so = re.findall(r'\d+', l)
    if not 2 <= len(so) <= 8:
        return None
    # đề nêu rõ cần mấy số thì phải khớp — lệch là hiểu sai đề
    m = re.search(r'(?:viết tiếp|viết)\s*(\d+)\s*số', text, re.I)
    if m and int(m.group(1)) != len(so):
        return None
    return {'values': [int(x) for x in so], 'ordered': True}


def r_mot_dap(text, loi):
    """Đề hỏi ĐÚNG MỘT thứ và lời giải là một đáp số → một ô.

    Chỉ nhận khi đề có duy nhất một dấu hỏi và lời giải gọn: không dấu ';', không
    dấu ','. Đề hỏi hai thứ mà chỉ một ô là sai (chuẩn mục 7 luật 3).
    """
    if text.count('?') > 1 or ';' in loi or ',' in loi:
        return None
    gt = _don(loi)
    if not gt or not _that(gt, loi) or len(gt) > 20:
        return None
    # phải là một SỐ, không phải biểu thức — biểu thức một vế thường là lời giải
    # từng bước ("18 : 3 = 6") mà bé thì được hỏi kết quả
    if not re.fullmatch(r'\d[\d\s]*', gt):
        return None
    return {'value': int(gt.replace(' ', ''))}


def r_chia_du(text, loi):
    """"Tính rồi viết chính danh: 13 : 4; 22 : 5" → mỗi phép một ô dạng "3 dư 1".

    Bộ chấm có sẵn kiểu `divmod` (mẫu `^\\d+ dư \\d+$`) và tự hiện lời nhắc "điền
    dạng: 9 dư 2". Nhờ thế giữ được CẢ thương LẪN số dư — đề "viết chính danh" hỏi
    cả hai, chấm mỗi thương là đổi đề.
    """
    # cho phép vài chữ chen giữa thương và số dư: sách viết "18 : 3 = 6 chia hết (dư 0)"
    ph = re.findall(r'(\d+)\s*:\s*(\d+)\s*=\s*(\d+)\s*[^()\d]{0,14}\(\s*dư\s*(\d+)\s*\)', loi)
    if not 1 <= len(ph) <= 4:
        return None
    # ĐỀ HỎI MẤY PHÉP THÌ MẤY Ô. Bỏ sót một phép là đổi đề: câu "Viết kết quả cả
    # hai" mà chỉ hiện một ô thì bé làm đủ vẫn bị coi như làm thiếu — và ngược lại,
    # bé bỏ qua phép còn lại mà vẫn được tính đúng.
    if len(re.findall(r'\d+\s*:\s*\d+', text)) != len(ph):
        return None
    parts = []
    for a, b, q, r in ph:
        # phép chia ấy phải có mặt trong ĐỀ, không thì nó là phép của bước phụ
        if not re.search(rf'{a}\s*:\s*{b}\b', text):
            return None
        # tự kiểm bằng chính phép chia — sách chép nhầm thì đừng chấm theo
        if int(a) != int(b) * int(q) + int(r) or int(r) >= int(b):
            return None
        # NÚT BẤM thay vì ô gõ. Gõ "3 dư 1" bằng bàn phím là việc của người lớn;
        # bé lớp 3 gõ chậm, sai chính tả một chữ là mất điểm oan, mà cái bài đang
        # kiểm là PHÉP CHIA chứ không phải kỹ năng gõ.
        #
        # Ba mồi nhử dựng theo đúng ba lỗi sách nêu: sai thương, sai số dư, và số
        # dư ≥ số chia (luật vàng của bài 6). Mồi nhử phải THẬT SỰ SAI — kiểm bằng
        # chính phép chia, không tin mắt mình.
        nhu = [f'{q} dư {r}']
        for tq, tr in ((int(q) + 1, r), (q, int(r) + 1), (int(q) - 1, int(b))):
            if int(tq) < 0 or int(tr) < 0:
                continue
            if int(tq) * int(b) + int(tr) == int(a) and int(tr) < int(b):
                continue                       # trùng đáp án đúng → bỏ, đừng nhử bậy
            s = f'{tq} dư {tr}'
            if s not in nhu:
                nhu.append(s)
        if len(nhu) < 3:
            return None
        parts.append({'label': f'{a} : {b}', 'value': f'{q} dư {r}',
                      'options': sorted(nhu[:3], key=lambda s: [int(x) for x in re.findall(r'\d+', s)])})
    if len({p['label'] for p in parts}) != len(parts):
        return None
    return {'parts': parts}


def r_lon_be(text, loi):
    """"lập số lớn nhất và số bé nhất" → hai ô có nhãn.

    Lời giải viết gọn "74 và 47" nên phải biết số nào ứng nhãn nào: lấy THỨ TỰ hai
    cụm trong ĐỀ. Rồi tự kiểm — ô "lớn nhất" phải thật sự lớn hơn ô "bé nhất";
    không thì thứ tự lời giải ngược với đề, bỏ câu ấy đi.
    """
    vt_l = text.lower().find('lớn nhất')
    vt_b = text.lower().find('bé nhất')
    if vt_l < 0 or vt_b < 0:
        return None
    so = re.findall(r'\d+', _sach(re.sub(r'\s*\([^)]*\)', ' ', loi)))
    if len(so) != 2:
        return None
    a, b = (so[0], so[1]) if vt_l < vt_b else (so[1], so[0])
    if int(a) <= int(b) or not (_that(a, loi) and _that(b, loi)):
        return None
    return {'parts': [{'label': 'lớn nhất', 'value': int(a)},
                      {'label': 'bé nhất', 'value': int(b)}]}


LUAT = [r_chia_du, r_lon_be, r_moi_muc, r_day_so, r_mot_dap]

# Hai câu ĐÃ XÉT và kết luận KHÔNG chấm máy được — khai đích danh để lần sau khỏi
# tưởng là bỏ sót, và để bảng tổng nói đúng "cố ý" thay vì "chưa khớp luật nào".
CO_Y = {
    'DL:KSN3.B01#C1': 'đọc số thành CHỮ — "năm mươi tư" và "năm mươi bốn" đều đúng, '
                      'ép một cách viết là chấm oan',
    'DL:KSN3.B17#C3': 'chỉ yêu cầu GẠCH CHÂN và gọi tên trạm giữa — đáp là câu văn, '
                      'mỗi bé diễn đạt một kiểu',
}


def suy_ra(c, ma=''):
    text, loi = c['text'], (c.get('loiChua') or '').strip()
    if not loi:
        return None, 'không có lời chữa'
    if ma in CO_Y:
        return None, f'CỐ Ý để tự chấm ({CO_Y[ma]})'
    if BO_QUA.search(text):
        return None, 'CỐ Ý để tự chấm (đề mở · vì sao · làm tay)'
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
        if not tep.startswith('DL_KSN3_B'):
            continue
        d = json.load(open(os.path.join(NGUON, tep), encoding='utf-8'))
        for c in d['cau']:
            if c['phan'] != 'luyenTap':
                continue
            ma = f"{d['id']}#{c['id']}"
            if ma in tay:
                k, ten = tay[ma], 'VIẾT TAY'
                # TỰ SOÁT BÀI CỦA MÌNH: mọi con số viết tay phải XUẤT HIỆN trong
                # lời giải của sách. Chốt này bắt lỗi thật ở lớp 2 (sách viết "một
                # phần tư" bằng chữ, người soạn ghi 4) — và bắt cả lỗi gõ nhầm.
                # Soi cả ĐỀ lẫn LỜI GIẢI. Với ô BẤM CHỌN, chữ trên nút là TÊN LOẠI
                # do chính đề nêu ra ("dãy nào nhịp đều, dãy nào phải thử sâu hơn"),
                # nên nó nằm ở đề chứ không ở lời giải. Chỉ soi lời giải thì chốt đỏ
                # oan đúng những khoá đã lấy chữ từ đề — mà lấy chữ từ đề mới là
                # đúng luật, vì đó là chữ bé đọc thấy.
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

    for c in canh_bao:
        print(f'  ⚠ {c}')
    tong = sum(thong_ke.values())
    o = sum(len(v['parts']) if 'parts' in v else 1 for v in ra.values())
    print(f'{len(ra)}/{tong} câu luyện tập chấm máy được ({len(ra) * 100 // tong}%)'
          f' · {o} ô nhập')
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
