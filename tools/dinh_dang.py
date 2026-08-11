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
NOI = [('lop2', 'lop2'), ('lop3', 'lop3'), ('lop4', 'lop4'), ('lop5', 'lessons'),
       ('lop5q2', 'quyen2')]      # Mùa giải: lượt đầu bỏ sót cả quyển

# Trường nào là LỜI VĂN cho bé đọc. Cố ý KHÔNG đụng `id`, `file`, `answerKey`,
# `sha256_16`… — bọc `$` vào một mã kiểm là hỏng cả bộ kiểm tra hình.
TRUONG_CHU = {
    'text', 'narration', 'solutionNarrative', 'problem', 'show', 'kidText',
    'mantra', 'wrong', 'fix', 'signal', 'counterExample', 'hint', 'hints',
    'title', 'caption', 'onComplete', 'homeActivity', 'watchFor', 'objective',
    'back', 'front', 'ten', 'moTa', 'de', 'loiChua', 'ghiChu',
    # Lượt đầu bỏ sót — đều là chữ BÉ ĐỌC trên màn hình:
    'screenText', 'solution', 'why', 'note', 'prompt', 'voiceover',
    'vocabulary', 'thanChu', 'dauHieu', 'say', 'lines',
}
# …trừ mấy chỗ `title` là NHÃN HÌNH, đã canh cỡ chữ theo bề ngang ảnh; chèn
# LaTeX vào đó là vỡ bố cục hình đã vẽ.
BO_QUA_DUONG = ('figureSpec', 'hinh', 'figures')

SO = r'\d+(?:[.,]\d+)?'


def tach_doan(s):
    """Cắt chuỗi thành các mẩu ('chu', …) và ('toan', …) theo cặp dấu `$`."""
    ra, i = [], 0
    while i < len(s):
        mo = s.find('$', i)
        if mo < 0:
            ra.append(('chu', s[i:]))
            break
        if mo > i:
            ra.append(('chu', s[i:mo]))
        dong = s.find('$', mo + 1)
        if dong < 0:
            ra.append(('chu', s[mo:]))
            break
        ra.append(('toan', s[mo + 1:dong]))
        i = dong + 1
    return [x for x in ra if x[1] != '']

# ── 1 · PHÂN SỐ ──────────────────────────────────────────────────────────────
# `1/(1×2)` — mẫu là một tích trong ngoặc
R_PS_NGOAC = re.compile(rf'(?<![\w/]) ({SO}) \s*/\s* \(\s*({SO})\s*[×x]\s*({SO})\s*\)', re.X)
# `3/4` — hai đầu đều là số, và KHÔNG dính chữ hai bên (loại km/h, 12/3/2024)
# Chặn hai đầu bằng CHỮ SỐ và dấu `/`, KHÔNG chặn bằng dấu câu hay chữ cái.
# Bản đầu chặn cả `,` `.` và chữ đứng sau, nên bỏ sót hàng loạt phân số thật:
#   "1/2, 1/3, 1/4"     dấu phẩy chặn
#   "1/4 của một số"    chữ "của" chặn
# Mà hai thứ ấy vốn không cần chặn: R_PS đòi SỐ ở CẢ HAI bên nên "km/h" không thể
# khớp, còn ngày tháng "12/3/2024" thì bị chặn bởi dấu `/` đứng sau.
R_PS = re.compile(rf'(?<![\d/]) ({SO}) \s*/\s* ({SO}) (?![\d/])', re.X)

# ── 1b · PHÂN SỐ CÓ CHỮ CÁI ──────────────────────────────────────────────────
# `1/(a × b) = 1/a - 1/b`, `a/b × b/c × c/d`, `1/(n × (n + 1))`.
#
# ⚠ Đã ĐẾM TRƯỚC KHI NỚI, vì `chữ/chữ` phần lớn KHÔNG phải phân số. Trong cả năm
# quyển có 991 cụm `X/Y` mang chữ cái, mà đứng đầu bảng là:
#
#     Đúng/Sai 230 · km/h 224 · m/s 115 · thêm/bớt 15 · phần/giờ 15
#     vòng/giờ 15 · m/giây 14 · 1/năm 5 · 2/g 2 (gam) · Sxq/Stp 2
#
# Nên luật KHÔNG nhận "một đầu có chữ" chung chung. Chỉ nhận đúng MƯỜI chữ cái
# THƯỜNG, ĐƠN LẺ mà sách thật sự dùng làm ẩn — đếm ra thì chỉ có bấy nhiêu:
#
#     p/q 12 · m/n 12 · 1/n 11 · 8/n 11 · a/b 10 · n/12 7 · 1/k 5
#     b/c 4 · c/d 4 · 1/a 4 · 1/b 4 · 1/t 3
#
# Ba chữ bị gạt có chủ ý: `s` và `h` là ĐƠN VỊ (m/s, km/h), còn `x` thì sách
# dùng làm DẤU NHÂN (`1/(1x2)`) chứ không phải ẩn. `g` là gam. Chữ HOA cũng gạt,
# vì nó chỉ xuất hiện ở lời văn (`N/A`, `TỔNG/HIỆU`, `Sxq/Stp`).
BIEN = r'[abcdkmnpqt]'
HANG = rf'(?:{SO}|{BIEN})'
OP = r'\s*[+\-−×x]\s*'

# Mẫu trong ngoặc, viết đích danh HAI dạng có thật thay vì một mẫu ngoặc chung:
# mẫu chung phải cân ngoặc, mà cân sai thì `1/(2 + 3) - (4 + 5)` bị vơ cả cụm sau.
R_PSB_LONG = re.compile(                                  # `1/(n × (n + 1))`
    rf'(?<![\w/])({HANG})\s*/\s*\(\s*({HANG})({OP})\(\s*({HANG})({OP})({HANG})\s*\)\s*\)(?![\w/])')
R_PSB_NGOAC = re.compile(                                 # `1/(a × b)`, `1/(n + 1)`
    rf'(?<![\w/])({HANG})\s*/\s*\(\s*({HANG})({OP})({HANG})\s*\)(?![\w/])')
# `a/b`, `1/n`, `n/12` — đòi ÍT NHẤT một đầu là chữ (hai đầu số thì R_PS lo rồi).
R_PS_BIEN = re.compile(rf'(?<![\w/])({HANG})\s*/\s*({HANG})(?![\w/])')

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


def _op(d):
    """Dấu phép tính trong mẫu phân số → LaTeX, luôn có khoảng cách hai bên.

    Phải tự đặt khoảng cách chứ không giữ nguyên văn: sách viết `1/(1×2)` không
    dấu cách, mà `\\times` là một LỆNH — dán liền thành `\\timesb` là bộ vẽ đọc ra
    lệnh lạ tên `\\timesb` rồi in nguyên văn ra màn hình.
    """
    c = d.strip()
    return {'×': r' \times ', 'x': r' \times ', '−': ' - '}.get(c, f' {c} ')


def _bt_latex(bt):
    """Một biểu thức thô → LaTeX: đổi dấu nhân, giữ nguyên phần còn lại."""
    return (bt.replace('×', r' \times ').replace(' x ', r' \times ')
              .replace('−', '-').strip())


def dinh_dang(s):
    """Một chuỗi lời văn → markdown + LaTeX. Trả (chuỗi mới, số chỗ đã đổi).

    Chuỗi đã có `$…$` thì CHỪA đúng những đoạn ấy ra rồi làm phần còn lại, chứ
    không bỏ qua cả chuỗi. Bản đầu bỏ qua cả chuỗi, nên câu nào lượt trước bọc
    được một nửa thì nửa kia mắc kẹt vĩnh viễn:

        "1/2 của $12 = 6$; 1/3 của $12 = 4$"   ← ba phân số không bao giờ được bọc
    """
    if not isinstance(s, str):
        return s, 0
    if '$' in s:
        manh, tong = [], 0
        for m in tach_doan(s):
            if m[0] == 'toan':
                manh.append(f'${m[1]}$')
            else:
                moi, k = dinh_dang(m[1])
                manh.append(moi)
                tong += k
        return ''.join(manh), tong
    n = 0

    def ps_ngoac(m):
        nonlocal n
        n += 1
        return rf'$\frac{{{m.group(1)}}}{{{m.group(2)} \times {m.group(3)}}}$'

    def ps(m):
        nonlocal n
        n += 1
        return rf'$\frac{{{m.group(1)}}}{{{m.group(2)}}}$'

    def psb_long(m):
        nonlocal n
        n += 1
        trong = (f'{m.group(2)}{_op(m.group(3))}'
                 f'({m.group(4)}{_op(m.group(5))}{m.group(6)})')
        return rf'$\frac{{{m.group(1)}}}{{{trong}}}$'

    def psb_ngoac(m):
        nonlocal n
        n += 1
        return rf'$\frac{{{m.group(1)}}}{{{m.group(2)}{_op(m.group(3))}{m.group(4)}}}$'

    def ps_bien(m):
        # Hai đầu đều là SỐ thì để R_PS lo — luật này chỉ gánh phần có chữ.
        if not re.search(r'[a-z]', m.group(1) + m.group(2)):
            return m.group(0)
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
    # Luật chữ cái chạy SAU luật số: dạng lồng trước dạng ngoặc, ngoặc trước trần,
    # nếu không thì `1/(a × b)` bị `1/(a` cắt cụt ngay từ luật trần.
    s = R_PSB_LONG.sub(psb_long, s)
    s = R_PSB_NGOAC.sub(psb_ngoac, s)
    s = R_PS_BIEN.sub(ps_bien, s)
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
            # Quyển 2 (Mùa giải) đặt tên tệp bằng `DR_` chứ không `DL_` — lượt đầu
            # chỉ lọc `DL_` nên bỏ sót TRỌN cả quyển mà bảng tổng không hề báo,
            # vì bảng chỉ đếm những gì nó đọc được.
            if not f.startswith(('DL_', 'DR_')):
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
