# -*- coding: utf-8 -*-
"""
GỢI Ý — dựng hai tầng gợi ý cho câu luyện tập lớp 2·3·4.

    python3 tools/goi_y.py --soat      # in thử, KHÔNG ghi
    python3 tools/goi_y.py             # ghi vào web/public/content

⚠ CHẠY SAU BỘ DỰNG (như dinh_dang.py và bai_mau.py) — xem docs/tiep_theo_dinh_dang.md.

── VẤN ĐỀ ──

Giao diện đã có sẵn cơ chế hai tầng: sai lần 1 hiện gợi ý 1, sai lần 2 hiện gợi ý
2, sai lần 3 mở đáp án (`hintState` trong flow.js). Nhưng dữ liệu TRỐNG:

    lớp 2  281 câu luyện tập ·   0 có gợi ý
    lớp 3  307 câu           ·   0
    lớp 4  396 câu           ·   0
    lớp 5  628 câu           · 628      ← quyển duy nhất có

Nên bé lớp 2·3·4 sai bao nhiêu lần cũng không được giúp một câu nào.

── CÁCH LẤY: TỪ CHÍNH BÀI, KHÔNG BỊA ──

Đã THỬ suy gợi ý từ bước tính đầu tiên của lời giải và PHẢI BỎ: 329/720 câu có
bước đầu chính là ĐÁP ÁN ("452 = 400 + 50 + 2" khi đáp là "400+50+2"). Gợi ý mà
nói ra đáp thì không còn là gợi ý.

Nguồn an toàn, lấy từ chính bài học:

    tầng 1  câu chốt của bài (`knowledgeCore.mantra`)  → nhắc HƯỚNG ĐI
    tầng 2  bước giảng đầu tiên (`statements[0]`)      → chỉ BƯỚC ĐẦU

Cả hai đều là lời GIẢNG, không phải lời giải, nên không thể lộ đáp số của một câu
cụ thể. Vẫn kiểm lại từng câu: gợi ý nào chứa nguyên văn đáp án của câu ấy thì bỏ.

── ĐÂY LÀ GỢI Ý THEO BÀI, CHƯA PHẢI THEO CÂU ──

Mọi câu trong cùng một bài dùng chung hai gợi ý. So với lớp 5 — nơi mỗi câu có
gợi ý riêng do người soạn viết — thì đây là bậc thấp hơn. Nhưng so với KHÔNG CÓ GÌ
thì hơn hẳn, và nó đúng: bé đang mắc ở bài nào thì được nhắc đúng cách làm của bài
ấy. Viết gợi ý riêng cho từng câu vẫn là việc còn để lại.
"""
import json, os, re, sys, collections

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOI = [('lop2', 'lop2'), ('lop3', 'lop3'), ('lop4', 'lop4')]
DAI_NHAT = 110          # gợi ý dài hơn ngần này thì bé đọc gợi ý còn lâu hơn làm bài


def _gon(s, dai=DAI_NHAT):
    """Rút một câu giảng thành một lời nhắc ngắn.

    Bỏ nhãn bước, cắt ở dấu câu gần nhất trước mốc, và KHÔNG cắt vào giữa một
    công thức `$…$` — cắt vào giữa là bé thấy một dấu đô-la lẻ loi trên màn.
    """
    s = ' '.join(str(s or '').split())
    # Nhãn bước viết bốn kiểu trong sách: "Bước 1 —", "Bước 1.", "Nhịp 2 -", "Vũ khí 3 —"
    s = re.sub(r'^(Bước|Nhịp|Vũ khí|Chặng|Chiêu|Đường|Tuyệt kỹ|Kho báu|Thế trận'
               r'|Nhân vật|Phép thử|Câu hỏi)\s*\d+\s*[—–.\-:]\s*', '', s)
    s = re.sub(r'^(MẸO[^:]*|LUẬT[^:]*|BÍ MẬT[^:]*)\s*:\s*', '', s)
    s = s.strip()
    if len(s) <= dai:
        return s

    cat = None
    for m in re.finditer(r'[.;!?]\s', s):
        if m.end() > dai:
            break
        if s[:m.end()].count('$') % 2 == 0:
            cat = m.end()
    if cat:
        return s[:cat].strip()

    cut = s.rfind(' ', 0, dai)
    while cut > 0 and s[:cut].count('$') % 2:
        cut = s.rfind(' ', 0, cut)
    return (s[:cut].strip() + '…') if cut > 0 else s[:dai]


def _dap_an(item):
    """Mọi giá trị đáp án của một câu, dạng chuỗi đã bỏ khoảng trắng."""
    ak = item.get('answerKey') or {}
    ra = set()
    for v in ([ak.get('value'), ak.get('choice')]
              + [p.get('value') for p in (ak.get('parts') or [])]
              + list(ak.get('values') or [])):
        if v is not None and str(v).strip():
            ra.add(str(v).replace(' ', '').lower())
    return ra


def goi_y_cua_bai(b):
    """Hai tầng gợi ý của một bài — lấy từ lời giảng của chính bài ấy."""
    K = b.get('knowledgeCore') or {}
    t1 = _gon(K.get('mantra') or '')
    st = K.get('statements') or []
    t2 = _gon(st[0].get('text') if st else '')
    # Hai tầng mà trùng nhau thì tầng 2 vô nghĩa — bỏ, thà một tầng thật.
    if t2 and t1 and t2[:40] == t1[:40]:
        t2 = _gon(st[1].get('text')) if len(st) > 1 else ''
    return [x for x in (t1, t2) if x]


def main(chi_soat=False):
    d = collections.Counter()
    vd = []
    for quyen, thu_muc in NOI:
        thu = os.path.join(GOC_KHO, 'web', 'public', 'content', thu_muc)
        for f in sorted(os.listdir(thu)):
            if not f.startswith('DL_'):
                continue
            duong = os.path.join(thu, f)
            b = json.load(open(duong, encoding='utf-8'))
            gy = goi_y_cua_bai(b)
            if not gy:
                d[f'{quyen}·bài KHÔNG dựng được gợi ý'] += 1
                continue
            doi = False
            for ds in ((b.get('practice') or {}).get('pools') or {}).values():
                for it in ds:
                    d[f'{quyen}·câu'] += 1
                    if it.get('hints'):
                        d[f'{quyen}·đã có sẵn'] += 1
                        continue
                    dap = _dap_an(it)
                    # Gợi ý nào chứa NGUYÊN VĂN đáp án của chính câu ấy thì bỏ.
                    an = [g for g in gy
                          if not any(a and a in g.replace(' ', '').lower() for a in dap)]
                    d[f'{quyen}·bỏ vì lộ đáp'] += len(gy) - len(an)
                    if an:
                        it['hints'] = an
                        d[f'{quyen}·gắn gợi ý'] += 1
                        d['tổng dòng gợi ý'] += len(an)
                        doi = True
                        if len(vd) < 4:
                            vd.append((b['id'], it.get('text', '')[:52], an))
            if doi and not chi_soat:
                with open(duong, 'w', encoding='utf-8') as g:
                    json.dump(b, g, ensure_ascii=False, indent=1)
    for k in sorted(d):
        print(f'{d[k]:>5}  {k}')
    for i, x, an in vd:
        print(f'\n── {i} · "{x}"')
        for k, g in enumerate(an, 1):
            print(f'   gợi ý {k}: {g}')
    return d


if __name__ == '__main__':
    main('--soat' in sys.argv)
