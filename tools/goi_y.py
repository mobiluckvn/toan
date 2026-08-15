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

── GỢI Ý VIẾT TAY, RIÊNG TỪNG CÂU: `data/goi_y_tay.json` ──

Bản đầu chỉ suy được gợi ý theo BÀI: mọi câu trong cùng một bài dùng chung hai
dòng lấy từ câu chốt và bước giảng đầu. Đúng mà nhạt — bé mắc ở câu nào cũng chỉ
nghe lại một lời nhắc chung chung.

Nay mỗi câu có gợi ý riêng, VIẾT TAY, theo đúng chuẩn của lớp 5 (quyển duy nhất
có sẵn gợi ý do người soạn viết). Đọc mấy dòng của lớp 5 mà rút ra khuôn:

    tầng 1  GỌI TÊN CẤU TRÚC — "Dãy cách đều bước 3." · "Hiệu 4 khúc vs 2 khúc."
    tầng 2  NƯỚC ĐI ĐẦU trên chính con số của câu ấy, DỪNG TRƯỚC KẾT QUẢ —
            "(3 + 99) : 2." · "Con nhích 1 khúc = 6 năm."

Rất ngắn (5–12 chữ), bám số của câu, và không bao giờ nói ra đáp số.

⚠ MÁY KHÔNG SUY ĐƯỢC THỨ NÀY. Đã cân nhắc suy tầng 2 từ `solutionNarrative` của
từng câu rồi bỏ: 274/984 câu có lời giải KHÔNG chứa dấu `=` nào, vì lời giải của
chúng CHÍNH LÀ đáp án ("814" · "362; 509; 740" · "gấp 10 lần"). Cắt máy kiểu gì
cũng ra đáp án hoặc ra một mẩu vô nghĩa.

Sửa tay thì sửa `data/goi_y_tay.json`, KHÔNG sửa `web/public/content` — bộ dựng
khuôn chung ghi đè trọn tệp. Câu nào tệp tay chưa có thì vẫn rơi về hai tầng suy
theo bài như cũ, nên thêm dần từng bài được.
"""
import json, os, re, sys, collections

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOI = [('lop2', 'lop2'), ('lop3', 'lop3'), ('lop4', 'lop4')]
DAI_NHAT = 110          # gợi ý dài hơn ngần này thì bé đọc gợi ý còn lâu hơn làm bài
TEP_TAY = os.path.join(GOC_KHO, 'data', 'goi_y_tay.json')


def nap_tay():
    """Gợi ý viết tay, khoá theo `mã bài` → `mã câu` → [tầng 1, tầng 2]."""
    if not os.path.exists(TEP_TAY):
        return {}
    b = json.load(open(TEP_TAY, encoding='utf-8'))
    return {k: v for k, v in b.items() if not k.startswith('_')}


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
    """Hai tầng gợi ý của một bài — lấy từ lời giảng của chính bài ấy.

    ⚠ BÀI DÙNG VIDEO KHÔNG CÓ LỜI GIẢNG BẰNG CHỮ. Từ 14-08, bài nào video thay cả
    mở bài lẫn bài giảng thì `mantra` rỗng và `statements` rỗng — cố ý. Nên hai
    nguồn dưới đây trả về rỗng, và bài ấy **mất sạch gợi ý**.

    Đã dính thật: 24 bài mới của chương 3 tới 9 đi ra với 216 câu không một gợi ý
    nào. Cổng phủ đặt ngưỡng 90% nên nó vẫn xanh suốt, mãi tới khi số bài video đủ
    nhiều mới tụt xuống dưới ngưỡng. Bé sai bao nhiêu lần cũng không được giúp.

    Nay bài video lấy từ hai chỗ VẪN CÓ và đều viết tay:
        tầng 1  mục tiêu đầu tiên của bài      → nhắc HƯỚNG ĐI
        tầng 2  dòng "Gợi ý 1" ở mục chỗ hay nhầm → chỉ BƯỚC ĐẦU
    Cả hai đều là lời dẫn, không phải lời giải, nên không lộ đáp số câu nào.
    """
    K = b.get('knowledgeCore') or {}
    t1 = _gon(K.get('mantra') or '')
    st = K.get('statements') or []
    t2 = _gon(st[0].get('text') if st else '')
    if not (t1 or t2):
        t1, t2 = _goi_y_bai_video(b)
    # Hai tầng mà trùng nhau thì tầng 2 vô nghĩa — bỏ, thà một tầng thật.
    if t2 and t1 and t2[:40] == t1[:40]:
        t2 = _gon(st[1].get('text')) if len(st) > 1 else ''
    return [x for x in (t1, t2) if x]


def _goi_y_bai_video(b):
    """Hai tầng cho bài dùng video — xem chú thích ở `goi_y_cua_bai`.

    Nguồn: mục tiêu bài (câu đầu) và dòng "Gợi ý 1" viết tay ở mục chỗ hay nhầm.
    Dòng ấy nằm trong `knowledgeCore.misconceptions[0].fix` sau khi dựng — tìm được
    bằng cách dò cả cây, chứ đoán chỗ thì trượt.
    """
    t1 = t2 = ''
    ob = b.get('objective') or {}
    if ob.get('text'):
        # Mục tiêu ghép nhiều câu bằng dấu chấm — lấy câu ĐẦU, đủ để nhắc hướng đi.
        t1 = _gon(str(ob['text']).split('.')[0].strip() + '.')
    for mc in (b.get('knowledgeCore') or {}).get('misconceptions') or []:
        van = str(mc.get('fix') or '')
        if 'Gợi ý 1' in van:
            sau = van.split('Gợi ý 1:', 1)[-1]
            t2 = _gon(sau.split('Gợi ý 2')[0].strip())
            break
    return t1, t2


def main(chi_soat=False):
    d = collections.Counter()
    vd = []
    tay = nap_tay()
    for quyen, thu_muc in NOI:
        thu = os.path.join(GOC_KHO, 'web', 'public', 'content', thu_muc)
        for f in sorted(os.listdir(thu)):
            if not f.startswith('DL_'):
                continue
            duong = os.path.join(thu, f)
            b = json.load(open(duong, encoding='utf-8'))
            gy = goi_y_cua_bai(b)
            if not gy:
                d[f'{quyen}·bài KHÔNG suy được gợi ý theo bài'] += 1
            cua_bai = tay.get(b['id']) or {}
            doi = False
            for ds in ((b.get('practice') or {}).get('pools') or {}).values():
                for it in ds:
                    d[f'{quyen}·câu'] += 1
                    # Thứ tự ưu tiên: TAY → đã có sẵn → suy theo bài.
                    #
                    # Gợi ý tay phải ĐÈ LÊN thứ đã có trong bản dựng, chứ không
                    # phải "chỉ điền chỗ trống": lượt trước công cụ này đã gắn gợi
                    # ý suy theo bài vào gần hết 984 câu, nên nếu chỉ điền chỗ
                    # trống thì tệp tay viết bao nhiêu cũng KHÔNG BAO GIỜ vào được
                    # mà chẳng có gì báo.
                    rieng = cua_bai.get(it.get('id'))
                    if rieng:
                        it['hints'] = list(rieng)
                        d[f'{quyen}·gợi ý TAY'] += 1
                        d['tổng dòng gợi ý'] += len(rieng)
                        doi = True
                        if len(vd) < 4:
                            vd.append((b['id'], it.get('text', '')[:52], rieng))
                        continue
                    if it.get('hints'):
                        d[f'{quyen}·đã có sẵn'] += 1
                        continue
                    if not gy:
                        continue
                    dap = _dap_an(it)
                    # Gợi ý nào chứa NGUYÊN VĂN đáp án của chính câu ấy thì bỏ.
                    an = [g for g in gy
                          if not any(a and a in g.replace(' ', '').lower() for a in dap)]
                    d[f'{quyen}·bỏ vì lộ đáp'] += len(gy) - len(an)
                    if an:
                        it['hints'] = an
                        d[f'{quyen}·suy theo bài'] += 1
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
