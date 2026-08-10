# -*- coding: utf-8 -*-
"""
ĐỊNH DẠNG — đưa lời văn của cả bốn quyển về markdown + LaTeX.

    python3 tools/dinh_dang.py --soat      # in thử, KHÔNG ghi
    python3 tools/dinh_dang.py             # ghi vào web/public/content

⚠ PHẢI CHẠY SAU MỌI BỘ DỰNG. Công cụ này sửa thẳng bản DỰNG (web/public/content),
mà `dung_khuon_chung*.py` thì ghi đè trọn tệp từ bản gốc — chạy bộ dựng sau là mất
sạch định dạng, dữ liệu vẫn hợp lệ và KHÔNG CÓ GÌ BÁO. Cùng một cái bẫy với việc
gắn hình (xem gan_hinh_lop2.py). Thứ tự đúng: dựng → gắn hình → ĐỊNH DẠNG.

── VẤN ĐỀ ──

Mọi màn đang in thẳng chuỗi thô, nên bài toán không trông ra bài toán:

    "Dãy phân số 1/(1×2) ; 1/(2×3) ; 1/(3×4) — mẫu là tích hai số liền nhau."
    "Một phần 30 : 5 = 6 → cốt cam 12 lít. Thử: 12 + 18 = 30 ✓; 12 : 18 = 2 : 3 ✓."

Phân số nằm ngang lẫn với phép chia, dấu × lẫn với chữ x, m2 đọc thành "m hai".
Đếm trên bốn quyển: 5097 phân số a/b · 3193 tỉ số a : b · 5263 dấu × · 488 đơn vị
bình phương. Sửa tay từng chỗ là vô vọng; sửa bằng luật thì phải rất dè dặt.

── NGUYÊN TẮC: THÀ BỎ SÓT CÒN HƠN BỌC NHẦM ──

Bọc nhầm một mẩu lời văn vào `$…$` là bé đọc thấy một cục chữ đơn cách giữa câu
văn — xấu hơn hẳn lúc chưa sửa. Nên mọi luật ở đây đều đòi HAI ĐẦU LÀ SỐ, và
danh sách chữ đứng cạnh được liệt kê đích danh. Chỗ nào ngờ ngợ thì để nguyên;
số bỏ sót in ra ở bảng tổng để còn biết mà soi.

Ba luật, theo thứ tự chạy:

  1. PHÂN SỐ   `3/4` `1/(1×2)` → `$\\frac{3}{4}$` `$\\frac{1}{1 \\times 2}$`
               Chỉ khi hai bên là SỐ (hoặc ngoặc chứa phép nhân số).
               KHÔNG đụng ngày tháng (12/3), tỉ lệ km/h, và đường dẫn tệp.
  2. BIỂU THỨC Chuỗi liền gồm số và phép tính → bọc `$…$`, đổi × thành \\times.
               Phải có ÍT NHẤT một dấu phép tính và hai số, nếu không thì mọi
               con số lẻ trong câu văn đều bị bọc.
  3. ĐƠN VỊ    `m2 cm2 dm2 km2` → `$m^2$` …  (chỉ khi đứng sau một con số)
"""
import json, os, re, sys, collections

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOI = [('lop2', 'lop2'), ('lop3', 'lop3'), ('lop4', 'lop4'), ('lop5', 'lessons')]

# Trường nào là LỜI VĂN cho bé đọc. Cố ý KHÔNG đụng `id`, `file`, `answerKey`,
# `sha256_16`… — bọc `$` vào một mã kiểm là hỏng cả bộ kiểm tra hình.
TRUONG_CHU = {
    'text', 'narration', 'solutionNarrative', 'problem', 'show', 'kidText',
    'mantra', 'wrong', 'fix', 'signal', 'counterExample', 'hint', 'title',
    'caption', 'onComplete', 'homeActivity', 'watchFor', 'objective', 'back',
    'front', 'ten', 'moTa', 'de', 'loiChua', 'ghiChu',
}
# …trừ mấy chỗ `title` là NHÃN HÌNH, đã canh cỡ chữ theo bề ngang ảnh; chèn
# LaTeX vào đó là vỡ bố cục hình đã vẽ.
BO_QUA_DUONG = ('figureSpec', 'hinh', 'figures')

SO = r'\d+(?:[.,]\d+)?'

# ── 1 · PHÂN SỐ ──────────────────────────────────────────────────────────────
# `1/(1×2)` — mẫu là một tích trong ngoặc
R_PS_NGOAC = re.compile(rf'(?<![\w/]) ({SO}) \s*/\s* \(\s*({SO})\s*[×x]\s*({SO})\s*\)', re.X)
# `3/4` — hai đầu đều là số, và KHÔNG dính chữ hai bên (loại km/h, 12/3/2024)
R_PS = re.compile(rf'(?<![\w/.,]) ({SO}) \s*/\s* ({SO}) (?![\w/.,]|\s*[a-zA-Zà-ỹ])', re.X)

# ── 2 · BIỂU THỨC ────────────────────────────────────────────────────────────
# Chuỗi số - phép tính liền mạch: "30 : 5 = 6", "12 + 18 = 30", "2 : 3".
# Đòi ít nhất một phép tính và kết thúc bằng số → "Bài 3." hay "lớp 5" không dính.
# Hai hạng phép tính, vì hai dấu này còn có nghĩa KHÁC trong lời văn:
#   `-`  "trang 1 - 9", "Chương 6 - 7" là KHOẢNG, không phải phép trừ
#   `:`  "Bài 6: 59 …" là nhãn, không phải tỉ số
# Cách phân biệt: hai dấu ấy chỉ tính là phép tính khi có DẤU CÁCH cả hai bên
# (sách viết nhãn liền: "Bài 6:"), VÀ cụm ấy không phải một KHOẢNG đứng sau chữ
# chỉ thứ tự — xem `la_khoang()`.
PHEP_LIEN = r'[+×x=<>≤≥]'
PHEP_ROI = r'[-−:]'
MOT_PHEP = rf'(?: \s*{PHEP_LIEN}\s* | \s+{PHEP_ROI}\s+ )'
R_BT = re.compile(rf'(?<![\w,.]) ({SO}) (?: {MOT_PHEP} {SO} )+ (?![\w%])', re.X)

# Chữ chỉ THỨ TỰ: số đứng sau chúng là số hiệu, nên "a - b" liền sau là một
# khoảng ("trang 1 - 9"), không phải phép trừ.
#
# ⚠ Viết bằng chuỗi thường, KHÔNG nhét vào mẫu `re.X`: ở chế độ ấy Python BỎ HẾT
# dấu cách trong mẫu, nên `(?<!trang )` lặng lẽ thành `(?<!trang)` và chẳng chặn
# gì. Đã dính đúng lỗi này: "trang $1 - 9$" vẫn lọt.
CHU_THU_TU = ('lớp', 'bài', 'trang', 'chương', 'câu', 'phần', 'tuần', 'vòng',
              'mức', 'hàng', 'nhóm', 'tuổi', 'đợt', 'kỳ', 'quyển')


def la_khoang(chuoi, bat_dau, cum):
    """Cụm này là một KHOẢNG chứ không phải phép tính?

    Đúng khi cả ba: chỉ có MỘT dấu, dấu ấy là `-` hoặc `:`, và ngay trước cụm là
    một chữ chỉ thứ tự. Có dấu `=` hay từ hai phép trở lên thì chắc chắn là phép
    tính — "cả lớp 14 + 10 = 24 bạn" phải được bọc, dù đứng sau chữ "lớp".
    """
    if '=' in cum:
        return False
    if len(re.findall(r'[-−:+×x]', cum)) != 1:
        return False
    if not re.search(r'[-−:]', cum):
        return False
    truoc = chuoi[max(0, bat_dau - 24):bat_dau].lower().rstrip()
    return any(truoc.endswith(c) for c in CHU_THU_TU)


# ── 3 · ĐƠN VỊ BÌNH PHƯƠNG ───────────────────────────────────────────────────
R_DV = re.compile(r'(?<=\d)\s*(m|cm|dm|km|mm)\s*2\b')
R_DV2 = re.compile(r'\b(m|cm|dm|km|mm)²')


def _bt_latex(bt):
    """Một biểu thức thô → LaTeX: đổi dấu nhân, giữ nguyên phần còn lại."""
    return (bt.replace('×', r' \times ').replace(' x ', r' \times ')
              .replace('−', '-').strip())


def dinh_dang(s):
    """Một chuỗi lời văn → markdown + LaTeX. Trả (chuỗi mới, số chỗ đã đổi)."""
    if not isinstance(s, str) or '$' in s:      # đã định dạng rồi thì thôi
        return s, 0
    n = 0

    def ps_ngoac(m):
        nonlocal n
        n += 1
        return rf'$\frac{{{m.group(1)}}}{{{m.group(2)} \times {m.group(3)}}}$'

    def ps(m):
        nonlocal n
        n += 1
        return rf'$\frac{{{m.group(1)}}}{{{m.group(2)}}}$'

    def bt(m):
        nonlocal n
        if la_khoang(m.string, m.start(), m.group(0)):
            return m.group(0)
        n += 1
        return f'${_bt_latex(m.group(0))}$'

    def dv(m):
        nonlocal n
        n += 1
        return f'${m.group(1)}^2$'

    s = R_PS_NGOAC.sub(ps_ngoac, s)
    s = R_PS.sub(ps, s)
    s = R_BT.sub(bt, s)
    s = R_DV.sub(dv, s)
    s = R_DV2.sub(lambda m: f'${m.group(1)}^2$', s)
    # Hai cụm `$…$` sát nhau chỉ cách một dấu cách thì gộp, cho đỡ vụn.
    s = re.sub(r'\$\s+\$', ' ', s)
    return s, n


def di(o, duong=()):
    """Duyệt cây JSON, chỉ đổi những trường là lời văn."""
    dem = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k in BO_QUA_DUONG:
                continue
            if isinstance(v, str) and k in TRUONG_CHU:
                moi, n = dinh_dang(v)
                if n:
                    o[k] = moi
                    dem += n
            else:
                dem += di(v, duong + (k,))
    elif isinstance(o, list):
        for v in o:
            dem += di(v, duong)
    return dem


def main(chi_soat=False):
    tong = collections.Counter()
    vd = []
    for quyen, thu_muc in NOI:
        d = os.path.join(GOC_KHO, 'web', 'public', 'content', thu_muc)
        for f in sorted(os.listdir(d)):
            if not f.startswith('DL_'):
                continue
            duong = os.path.join(d, f)
            goc = open(duong, encoding='utf-8').read()
            b = json.loads(goc)
            n = di(b)
            tong[quyen] += n
            if n:
                tong[f'{quyen}·bài đổi'] += 1
            if n and len(vd) < 6:
                for k in ('solutionNarrative', 'text'):
                    x = json.dumps(b, ensure_ascii=False)
                    m = re.search(r'"' + k + r'": "([^"]*\$[^"]*)"', x)
                    if m:
                        vd.append((b['id'], m.group(1)[:150]))
                        break
            if not chi_soat and n:
                with open(duong, 'w', encoding='utf-8') as g:
                    json.dump(b, g, ensure_ascii=False, indent=1)
    for k in sorted(tong):
        print(f'{tong[k]:>6}  {k}')
    print()
    for i, s in vd:
        print(f'  {i}: {s}')
    return tong


if __name__ == '__main__':
    main('--soat' in sys.argv)
