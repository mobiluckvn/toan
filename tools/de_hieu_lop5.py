# -*- coding: utf-8 -*-
"""
LỚP 5 — làm lời văn TRỰC TIẾP và đúng tầm học sinh lớp 5.

    python3 tools/de_hieu_lop5.py --soat    # in bản soát, KHÔNG ghi
    python3 tools/de_hieu_lop5.py           # ghi vào data/ và web/public/content/

Ba việc, theo đúng yêu cầu:

  1. BỎ KÝ HIỆU VƯỢT CẤP. Lớp 5 chưa học tập hợp (∈), chia hết (⋮), ≤ ≥, ⇒ ⇔.
     Viết bằng lời: "108 ⋮ 9" → "108 chia hết cho 9".
     GIỮ những dấu lớp 5 ĐÃ học: < > = ≠ và dấu phép tính.

  2. BỎ MÃ NỘI BỘ lọt ra màn hình. "K3 — hỏi ngược:…" là mã nguyên tắc của người
     soạn; bé đọc thấy "K3" không hiểu gì, mà nó lại đứng ngay đầu câu.

  3. NÓI THẲNG TOÁN TRƯỚC. Giữ nhân vật và mô hình đếm được (đóng kẹo vào túi),
     nhưng câu đầu của mỗi lời giảng phải là điều toán học cần nói.

CHỈ SỬA TRƯỜNG BÉ ĐỌC. Danh sách `BE_DOC` chốt bằng cách đọc mã giao diện, không
đoán: `mechanism`, `skills`, `videoSpec`, `numberRange` không hiện lên màn hình nên
để nguyên — sửa cả những chỗ ấy là đụng dữ liệu người soạn dùng mà chẳng lợi gì.
"""
import collections, json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(GOC_KHO, 'data', 'lessons')
PUBLIC = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lessons')

# ── trường BÉ ĐỌC (chốt bằng mã giao diện) ───────────────────────────────────
BE_DOC = {
    'title', 'objective.kidText', 'objective.text', 'objective.passRule',
    'knowledgeCore.mantra',
    'knowledgeCore.statements[].text',
    'knowledgeCore.canonicalExamples[].problem', 'knowledgeCore.canonicalExamples[].solution',
    'knowledgeCore.canonicalExamples[].why', 'knowledgeCore.canonicalExamples[].case',
    'knowledgeCore.misconceptions[].wrong', 'knowledgeCore.misconceptions[].signal',
    'knowledgeCore.misconceptions[].fix', 'knowledgeCore.misconceptions[].counterExample',
    'lecture.screens[].narration', 'lecture.screens[].display.caption',
    'workedExample.title', 'workedExample.problem', 'workedExample.steps[].show',
    'workedExample.steps[].askBefore.text',
    'assessment.passRule', 'assessment.items[].text',
    'assessment.items[].solutionNarrative', 'assessment.items[].wrongFeedback',
    'figureSpec[].caption',
    # Trang kết bài: FinaleCard.jsx đọc `flashcards[0].back` và ba dòng parentNote.
    # Sót hai chỗ này ở lần đầu — danh sách phải chốt bằng cách ĐỌC MÃ GIAO DIỆN
    # cho tới hết, không dừng ở màn học.
    'spacedReview.flashcards[].back',
    'parentNote.onComplete', 'parentNote.homeActivity', 'parentNote.watchFor',
}
R_POOL = re.compile(r'^practice\.pools\.(warmup|standard|challenge)\[\]\.'
                    r'(text|solutionNarrative|wrongFeedback|hints\[\])$')
R_FIG = re.compile(r'^figureSpec\[\]\.params\.')
R_VOCAB = re.compile(r'^knowledgeCore\.vocabulary\[\]$')


def be_doc(p):
    return p in BE_DOC or R_POOL.match(p) or R_FIG.match(p) or R_VOCAB.match(p)


# ── luật sửa, chạy THEO THỨ TỰ ───────────────────────────────────────────────
# Luật hẹp trước, luật rộng sau — nếu không thì luật rộng nuốt mất ngữ cảnh mà
# luật hẹp cần để dịch cho đúng.
LUAT = [
    # ĐIỀU KIỆN KÉP: "0 ≤ số dư < số chia" — lớp 5 chỉ cần vế phải là đủ ý
    (r'0\s*≤\s*([^<>≤≥]{1,24}?)\s*<\s*', r'\1 bé hơn '),
    (r'1\s*≤\s*([^<>≤≥]{1,24}?)\s*≤\s*', r'\1 nằm từ 1 đến '),
    # CHUỖI SO SÁNH: "45 ≤ 47 < 50" — viết cả chuỗi bằng lời thì rối hơn số;
    # lớp 5 đọc được "45 < 47 < 50" nên chỉ hạ ≤ thành < khi hai vế KHÁC nhau.
    (r'(\d+)\s*≤\s*(\d+)\s*<', lambda m: f'{m.group(1)} < {m.group(2)} <'
                                    if m.group(1) != m.group(2) else m.group(0)),

    # TỈ LỆ ĐẠT: "≥ 2/3" → "đúng từ 2 trên 3 câu"
    # "đúng ≥ 2/3" → "đúng từ 2 trên 3 câu" (đừng để thành "đúng đúng từ…")
    (r'\bđúng\s*≥\s*(\d+)\s*/\s*(\d+)', r'đúng từ \1 trên \2 câu'),
    (r'≥\s*(\d+)\s*/\s*(\d+)', r'đúng từ \1 trên \2 câu'),
    (r'≤\s*(\d+)\s*/\s*(\d+)', r'nhiều nhất \1 trên \2 câu'),

    # CHIA HẾT: "108 ⋮ 9" → "108 chia hết cho 9"
    (r'\s*⋮\s*', ' chia hết cho '),
    (r'\s*∤\s*', ' không chia hết cho '),

    # TẬP HỢP: "d ∈ {2;3;7;8}" → "d là 2, 3, 7 hoặc 8"
    (r'∈\s*\{([^}]*)\}', lambda m: 'là ' + _liet_ke(m.group(1))),
    (r'\s*∈\s*', ' là '),
    (r'\s*∉\s*', ' không phải là '),

    # SO SÁNH
    (r'\s*≥\s*', ' lớn hơn hoặc bằng '),
    (r'\s*≤\s*', ' bé hơn hoặc bằng '),

    # SUY LUẬN
    (r'\s*⇔\s*', ' cũng có nghĩa là '),
    (r'\s*⇒\s*', ' nên '),

    # KHÁC
    (r'\s*≈\s*', ' khoảng '),
    (r'\s*⊥\s*', ' vuông góc với '),
    (r'\s*∥\s*', ' song song với '),
    (r'\s*∩\s*', ' và '),
    (r'\s*±\s*', ' cộng hoặc trừ '),

    # VÍ VON BỌC NGOÀI CÂU CHỐT. Sách viết "Thần chú tiệm bánh: chia càng nhiều
    # phần — lát càng mỏng!". Phần sau dấu hai chấm đã là toán nói thẳng; chỉ cái
    # vỏ "thần chú <tên tiệm bánh/phiên tòa/nhà ga>" là ví von. Bỏ vỏ, giữ ruột.
    # Mỗi bài chỉ có một câu chốt nên bỏ tên gọi không gây lẫn bài này với bài kia.
    # `[^:]` dừng ở dấu hai chấm ĐẦU TIÊN nên không nuốt sang phần toán.
    (r'^\s*Hai\s+thần\s+chú[^:]{0,32}:\s*', 'Hai câu cần nhớ: '),
    (r'^\s*Thần\s+chú[^:]{0,32}:\s*', 'Câu cần nhớ: '),
    (r'\b(câu|Câu)\s+thần\s+chú\b', r'\1 cần nhớ'),
    (r'\bThần\s+chú:\s*', 'Cần nhớ: '),

    # MÃ NỘI BỘ đứng đầu câu. Sách soạn dùng đủ kiểu nối và đủ kiểu ngăn:
    #   "K3 — hỏi ngược:"  ·  "Ca K1+K3 — cặp đối chiếu"  ·  "K1: ab là 10a + b"
    #   "K2/K3: phép trừ…"  ·  "Ca K3 vế hiệu — LT2"  ·  "K3 + nghi thức soi dấu:"
    (r'^\s*(?:Ca\s+)?K\d+(?:\s*[+/]\s*K\d+)*\s*[:—–-]\s*', ''),
    # dạng không có dấu ngăn: "Ca K3 vế hiệu" · "K2 nhánh 99" → bỏ phần mã, giữ lời
    (r'^\s*(?:Ca\s+)?K\d+(?:\s*[+/]\s*K\d+)*\s+(?=[a-zàáảãạâấầẩẫậăắằẳẵặđeéèẻẽẹêếềể'
     r'ễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵ])', ''),
    # "K3 + nghi thức soi dấu:" — dấu + ở đây nối sang LỜI, không nối sang mã K
    # khác, nên hai luật trên không ăn. Vẫn neo đầu câu.
    (r'^\s*(?:Ca\s+)?K\d+\s*\+\s*(?=[a-zàáảãạâấầẩẫậăắằẳẵặđeéèẻẽẹêếềểễệiíìỉĩị'
     r'oóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵ])', ''),
    # "K4, đề A câu 4 của chương." — ngăn bằng dấu phẩy
    (r'^\s*(?:Ca\s+)?K\d+(?:\s*[+/]\s*K\d+)*\s*,\s*', ''),
    # ĐỪNG viết luật xoá mã K GIỮA CÂU. Đã thử: r'\bK\d+\s+(?=chữ thường)' biến
    # "Ca chuẩn K1+K2 từ sách" thành "Ca chuẩn K1+từ sách" — hỏng câu mà vẫn đọc
    # trôi nên rất dễ lọt. Mã giữa câu xử bằng luật RIÊNG cho từng cụm, bên dưới.
    # Ghi chú của người soạn ở dòng "📌" dưới bài mẫu: bé đọc "Ca chuẩn K1+K2" thì
    # chẳng hiểu gì — bỏ cả cụm, giữ phần lời còn lại.
    (r'^\s*Ca\s+chuẩn\s+K\d+(?:\s*[+/]\s*K\d+)*\s*[—–-]?\s*', ''),
    (r'^\s*Ca\s+K\d+(?:\s*[+/]\s*K\d+)*\s*[—–-]?\s*', ''),
    (r'\bnhánh\s+K\d+\b', 'nhánh'),
    (r'\s*\(\s*(?:xem\s+)?K\d+(?:\s*\+\s*K\d+)*\s*\)', ''),
    (r'\s*—\s*(?:Ca\s+)?K\d+(?:\s*\+\s*K\d+)*\s*$', ''),
    (r'\bĐ\d+\.\d+\b', ''),
    (r'\bHình ảnh brand:\s*', ''),
]


def _liet_ke(s):
    """"2;3;7;8" → "2, 3, 7 hoặc 8" — đọc thành lời, không còn dấu ngoặc nhọn."""
    xs = [x.strip() for x in re.split(r'[;,]', s) if x.strip()]
    if len(xs) <= 1:
        return xs[0] if xs else ''
    return ', '.join(xs[:-1]) + ' hoặc ' + xs[-1]


# ── bảng thay chữ VIẾT TAY ───────────────────────────────────────────────────
# Ví von nằm lẫn giữa câu thì mỗi chỗ một kiểu — viết regex là hỏng nghĩa. Xếp
# chuỗi DÀI trước để "Quy trình cánh cửa kho:" không bị "cánh cửa kho" cắt trước.
_TAY = json.load(open(os.path.join(GOC_KHO, 'data', 'lop5_loi_van_tay.json'),
                      encoding='utf-8'))['thay']
TAY = sorted(_TAY, key=lambda m: -len(m['tim']))
DUNG_TAY = collections.Counter()


def sua(s):
    truoc = s
    for m in TAY:
        if m['tim'] in s:
            DUNG_TAY[m['tim']] += s.count(m['tim'])
            s = s.replace(m['tim'], m['thay'])
    for mau, thay in LUAT:
        s = re.sub(mau, thay, s)
    # dọn khoảng trắng thừa do thay chuỗi để lại
    s = re.sub(r'\s{2,}', ' ', s).strip()
    # KHÔNG đụng dấu ':' — trong toán Việt nó là PHÉP CHIA ("47 : 5"), bỏ dấu cách
    # trước nó thành "47: 5" là hỏng mọi phép chia của cả quyển.
    # Chỉ dồn dấu câu sau CHỮ hoặc SỐ. "= ?" phải giữ nguyên dấu cách — dồn lại
    # thành "=?" là hỏng câu hỏi toán ("1 256 : 314 = ?").
    s = re.sub(r'(?<=[\w\u00C0-\u1EF9])\s+([,.;!?])', r'\1', s)
    # Bỏ mã nội bộ xong mà chỉ còn dấu câu thì trả về RỖNG. "Ca chuẩn K1+K2." mà
    # để lại "." thì màn bài mẫu hiện đúng một dấu chấm dưới biểu tượng 📌.
    if re.fullmatch(r'[\s.,;:—–-]*', s):
        s = ''
    return s, s != truoc


def di(o, p='', ghi=True, sổ=None):
    if isinstance(o, dict):
        return {k: di(v, f'{p}.{k}' if p else k, ghi, sổ) for k, v in o.items()}
    if isinstance(o, list):
        return [di(v, p + '[]', ghi, sổ) for v in o]
    if isinstance(o, str) and be_doc(p):
        moi, doi = sua(o)
        if doi and sổ is not None:
            sổ.append((p, o, moi))
        return moi if ghi else o
    return o


def main(chi_soat=False):
    sổ, n_tep = [], 0
    for ten in sorted(os.listdir(DATA)):
        if not ten.startswith('DL_KSN5Q1_'):
            continue
        d = json.load(open(os.path.join(DATA, ten), encoding='utf-8'))
        rieng = []
        moi = di(d, sổ=rieng)
        if not rieng:
            continue
        n_tep += 1
        sổ += rieng
        if not chi_soat:
            for thu_muc in (DATA, PUBLIC):
                with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as f:
                    json.dump(moi, f, ensure_ascii=False, indent=1)

    # Mục nào trong bảng tay không khớp chỗ nào nghĩa là sách đã đổi chữ mà bảng
    # chưa đổi theo — im lặng bỏ qua thì lần sau tưởng đã sửa rồi. Báo ngay.
    #
    # NHƯNG công cụ này chạy được NHIỀU LẦN: lần thứ hai thì chữ đã đổi xong, mục
    # nào cũng "không khớp" — báo hết là kêu oan, mà kêu oan vài lần là người sau
    # tắt chốt đi. Nên chỉ báo khi bản THAY cũng không có mặt: lúc ấy mới thật là
    # bảng nói một đằng, sách một nẻo.
    ca_quyen = '\n'.join(json.dumps(json.load(open(os.path.join(DATA, x), encoding='utf-8')),
                                    ensure_ascii=False)
                         for x in sorted(os.listdir(DATA)) if x.startswith('DL_KSN5Q1_'))
    thua = [m['tim'] for m in TAY
            if not DUNG_TAY[m['tim']] and m['thay'] and m['thay'] not in ca_quyen]
    if thua:
        print(f'  ⚠ {len(thua)} mục trong bảng tay KHÔNG khớp chỗ nào:')
        for t in thua:
            print(f'      "{t}"')
    print(f'{len(sổ)} chỗ sửa · {n_tep} bài' + (' (CHƯA ghi)' if chi_soat else ''))
    return sổ


if __name__ == '__main__':
    s = main('--soat' in sys.argv)
    if '--in' in sys.argv:
        for p, a, b in s[:int(sys.argv[sys.argv.index('--in') + 1])
                         if '--in' in sys.argv and sys.argv[-1].isdigit() else 40]:
            print(f'\n{p}\n  TRƯỚC: {a[:130]}\n  SAU  : {b[:130]}')
