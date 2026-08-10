# -*- coding: utf-8 -*-
"""
LỚP 4 — nói THẲNG vào bài toán: bỏ ví von, bỏ mã nội bộ, bỏ dấu ngăn khó hiểu.

Đây là MODULE, `chuan_lop4.py` gọi khi dựng tầng GỐC từ tầng THÔ. Đặt ở đó chứ
không sửa tệp đã dựng, vì lần chạy dây chuyền sau sẽ ghi đè sạch mà chẳng có gì báo
(chuẩn mục 6: "sửa ở BỘ DỰNG").

── BA VIỆC ──

**1. Bỏ lớp vỏ ví von.** Sách lớp 4 bọc mọi thứ trong "Xưởng Mô Hình": bài toán là
"đơn hàng", cách làm là "tuyệt kỹ", dấu hiệu chia hết là "mật mã", người giải là
"kỹ sư"/"thám tử"/"quan tòa". Phần sau dấu hai chấm đã là toán nói thẳng; chỉ cái
vỏ là ví von — **bỏ vỏ, giữ ruột** (chuẩn mục 5). Riêng "Anh Trí Dũng đố: …" bọc
44 câu hỏi: bỏ vỏ là câu hỏi hiện ra nguyên vẹn.

Giữ TÊN NHÂN VẬT trong đề toán (Su Bống, bác Hòa, An, Bình): đó là "ai" của bài
toán, đúng như mọi sách toán vẫn viết — không phải ví von.

**2. Bỏ dấu · dùng làm dấu ngăn giữa câu.** Sách dùng nó khắp nơi ("9-3 · 8-4 ·
7-5"), mà bé không biết nó nghĩa là gì — dấu phẩy thì bé đọc được ngay. GIỮ dấu ·
ở TIÊU ĐỀ ("Bài 1 · TÊN BÀI"): chỗ ấy nó ngăn số bài với tên bài, cả bốn quyển đều
dùng, và bé không phải đọc nó thành lời.

**3. Bỏ mã nội bộ.** "CÔNG THỨC ③", "Dạng gốc: SỐ 1.2 mức Lớp 4".

── CHỐT BẮT BUỘC ──

`soat_mat_so` so đa tập chữ số trước và sau. Luật viết lại rất dễ nuốt mất một con
số mà câu vẫn đọc trôi — chuẩn mục 5 chốt 2 sinh ra từ đúng lỗi ấy.
"""
import collections, re

# ── luật hẹp trước, luật rộng sau (chuẩn mục 5) ──
LUAT = [
    # 1 · lớp vỏ bọc câu hỏi — bỏ vỏ, giữ nguyên ruột bên trong ngoặc kép
    (re.compile(r'^Anh Trí Dũng đố:\s*"(.+?)"\s*(\(.*\))?\s*$', re.S),
     lambda m: (m.group(1) + (' ' + m.group(2) if m.group(2) else '')).strip()),
    (re.compile(r'^\s*TRÙM CUỐI\s*[—-]?\s*[^:]{0,40}:\s*'), ''),
    (re.compile(r'^\s*GÓC KHÁM PHÁ:\s*'), ''),
    (re.compile(r'\bGÓC KHÁM PHÁ\b\s*&?\s*'), ''),

    # 2 · cụm dài trước (luật hẹp trước, luật rộng sau)
    (re.compile(r'\bCON MẮT KỸ SƯ\b', re.I), 'NHÌN KỸ TRƯỚC KHI TÍNH'),
    (re.compile(r'\bĐếm số kiểu kỹ sư\b', re.I), 'Cách đếm'),
    (re.compile(r'\b(?:là |thì )?thua kỹ sư\b', re.I), 'là mất công vô ích'),
    (re.compile(r'\bNGHI THỨC THỬ LẠI\b'), 'THỬ LẠI'),
    (re.compile(r'\bQUAN TÒA Ê KE XỬ GÓC\b', re.I), 'DÙNG Ê KE ĐO GÓC'),
    (re.compile(r'\b[Kk]ết luận thám tử\b'), 'Kết luận'),
    (re.compile(r'\b(?:người |cựu )?(?:kỹ sư|thám tử|quan tòa|hoa tiêu|thủ kho|'
                r'nghệ nhân|trọng tài|đầu bếp|kiến trúc sư)\s+(?:nhí\s+)?'), ''),
    (re.compile(r'\b[Cc]ả xưởng\b'), 'cả nhóm'),
    (re.compile(r'\b[Xx]ưởng (?:đề xuất|ghi|chốt)\b'), 'Ta chốt'),
    (re.compile(r'\b(?:của |cả )?[Xx]ưởng( Mô Hình)?\b'), ''),

    # 4 · mã nội bộ của người soạn
    (re.compile(r'\bCÔNG THỨC\s*[①②③④⑤⑥⑦⑧⑨⑩]\s*'), 'CÔNG THỨC '),
    (re.compile(r'^\s*Dạng gốc:[^—]*—\s*'), ''),
]

# Dấu · dùng làm dấu ngăn GIỮA CÂU. Chỉ đổi khi hai bên là chữ hay số, để không
# đụng dấu · của tiêu đề (xử riêng bằng cách không gọi hàm này cho `title`).
R_CHAM_GIUA = re.compile(r'(?<=[^\s])\s+·\s+(?=[^\s])')

# Thay theo TỪ ĐIỂN, giữ nguyên kiểu viết hoa. Bản đầu viết mỗi kiểu một luật nên
# "MẬT MÃ" và "mật mã" thì trúng, còn "Mật mã" đầu câu thì lọt — 20 chỗ sót lại
# đúng vì thế. Một luật lo cả ba kiểu thì không còn khe nào.
THAY = {
    'tuyệt kỹ': 'cách nhẩm nhanh', 'tuyệt chiêu': 'cách', 'bí kíp': 'cách',
    'vũ khí': 'công cụ', 'thần chú': 'câu cần nhớ', 'mật mã': 'dấu hiệu',
    'mật thư': 'câu đố', 'cao thủ': 'người làm giỏi', 'đơn hàng': 'bài toán',
    'kỹ sư': 'người giải', 'thám tử': 'người giải', 'quan tòa': 'người giải',
    'góc khám phá': 'tìm hiểu thêm',
}
R_THAY = re.compile(r'\b(' + '|'.join(THAY) + r')\b', re.I)


def _giu_hoa(m):
    goc, moi = m.group(0), THAY[m.group(0).lower()]
    if goc.isupper():
        return moi.upper()
    if goc[:1].isupper():
        return moi[0].upper() + moi[1:]
    return moi


R_GON = re.compile(r'\s{2,}')
R_TRONG = re.compile(r'^[\s.,;:—-]+|[\s,;:—-]+$')


def sua(s, giu_cham=False):
    """Viết lại một chuỗi cho bé đọc thẳng. `giu_cham`: giữ dấu · (dùng cho tiêu đề)."""
    if not isinstance(s, str) or not s.strip():
        return s
    for pat, thay in LUAT:
        s = pat.sub(thay, s)
    s = R_THAY.sub(_giu_hoa, s)
    if not giu_cham:
        s = R_CHAM_GIUA.sub(', ', s)
    s = R_GON.sub(' ', s)
    # Bỏ vỏ xong đôi khi còn trơ dấu câu ở đầu ("— Đọc số…"). Nếu chỉ còn dấu câu
    # thì trả về RỖNG chứ đừng trả một dấu chấm lơ lửng (bẫy 18 của chuẩn).
    s = R_TRONG.sub('', s)
    if not re.search(r'[0-9A-Za-zÀ-ỹ]', s):
        return ''
    # viết hoa lại chữ đầu nếu lớp vỏ bị bỏ làm câu mở bằng chữ thường
    return s[0].upper() + s[1:] if s[:1].islower() and len(s) > 1 else s


def soat_mat_so(truoc, sau):
    """Trả danh sách chữ số bị NUỐT MẤT. Luật viết lại rất dễ ăn mất một con số mà
    câu vẫn đọc trôi — đây là chốt 2 của chuẩn mục 5."""
    a = collections.Counter(re.findall(r'\d', truoc or ''))
    b = collections.Counter(re.findall(r'\d', sau or ''))
    thieu = a - b
    return sorted(thieu.elements())
