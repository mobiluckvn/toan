# -*- coding: utf-8 -*-
"""
BƯỚC 1 — trích Quyển 2 từ .docx thành JSON thô.

    python3 tools/rut_quyen2.py

Nguyên tắc: GIỮ NGUYÊN CHỮ của sách, chỉ gắn cấu trúc (vòng → màn → câu / bẫy /
thẻ). Không sửa, không rút gọn, không diễn giải — mọi việc đó để bước sau, và
phải nhìn thấy được là đã đổi gì.

Vì sao tách hẳn bước này: ở Quyển 1 chúng tôi vừa trích vừa biên tập, nên khi cần
đối chiếu "sách viết gì" thì không còn bản gốc nào để so. Lần này bản trích thô là
một mốc bất biến, mọi biến đổi sau đều so được với nó.
"""
import json, os, re, zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'docs', 'KSN5_Q2_TRON_QUYEN_Mua_Giai_Vo_Dich.docx')
RA = os.path.join(GOC_KHO, 'data', 'quyen2_tho.json')


def doan_van(duong_dan):
    """Mọi đoạn có chữ, theo đúng thứ tự trong sách."""
    z = zipfile.ZipFile(duong_dan)
    root = ET.fromstring(z.read('word/document.xml'))
    ra = []
    for p in root.iter(W + 'p'):
        t = ''.join(n.text or '' for n in p.iter(W + 't')).strip()
        if t:
            ra.append(t)
    return ra


# ── các mốc nhận dạng ──────────────────────────────────────────────
R_VONG    = re.compile(r'^VÒNG ĐẤU (\d+)$')
R_TRON    = re.compile(r'^ĐỀ TRỘN (\d+)$')
R_THI     = re.compile(r'^KỲ THI THỬ (\d+)$')
R_MAN     = re.compile(r'^MÀN (\d)\s*·\s*(.+)$')
R_DE      = re.compile(r'^Câu (\d+)\.\s*(.+)$')
R_DAP     = re.compile(r'^Câu (\d+):\s*(.+)$')
# Kỳ thi thử 3 ghi lời chữa theo kiểu "A1: …" / "B1: …" chứ không "Câu 1: …",
# nên 24 câu chung kết từng bị bỏ trắng phần chữa.
R_DAP_AB  = re.compile(r'^([AB])(\d+):\s*(.+)$')
# Đề B ghi nhiều đáp án ngắn TRÊN CÙNG MỘT DÒNG:
#   "B1: 425.   B2: 75.   B3: 20.   B4: 6.   B5: … cm².   B6: 5/6."
# Bắt từng cái một, nếu không chỉ lấy được đáp án đầu dòng (6 câu từng bỏ trắng).
R_DAP_GOP = re.compile(r'([AB])(\d+):\s*(.*?)(?=\s{2,}[AB]\d+:|$)')
# Một bẫy có thể gài ở NHIỀU câu: "CĐ-44.3 · Câu 6 & 15". Đòi kết thúc ngay sau
# một con số là trượt mất bẫy ấy (vòng 11 từng chỉ ra 11 bẫy thay vì 12).
R_BAY_TOA = re.compile(r'^CĐ-(\d+)\.(\d+)\s*·\s*Câu ([\d\s&,và]+)$')
R_BAY_HS  = re.compile(r'^CĐ-(\d+)\.(\d+)\s+(⚠+)\s*·\s*(.+)$')
R_BAI_HS  = re.compile(r'^Bài (\d+)\s*·\s*(.+)$')
R_CHUONG  = re.compile(r'^C(\d+)\s+CHƯƠNG (\d+)\s*·\s*(.+)$')
R_THE     = re.compile(r'^THẺ (\d+)\s*·\s*CHƯƠNG (\d+)\s*—\s*(.+)$')
# Tiêu đề bài kỹ năng: T1–T4 có phần "— phụ đề", riêng T5 KHÔNG có. Bắt phụ đề
# thành tuỳ chọn, nếu không T5 lọt lưới (đã xảy ra ở lần chạy đầu).
R_KYNANG  = re.compile(r'^(T\d)\s*·\s*([A-ZÀ-Ỹ][^—]*?)(?:\s*—\s*(.+))?$')
# Kỳ thi thử 3 có HAI đề (A và B), CÙNG đánh số từ Câu 1. Không tách thì đề B đè
# lên đề A và mất trắng 12 câu — đúng lỗi lần chạy đầu.
R_MAN_DE  = re.compile(r'^MÀN \d\s*·\s*ĐỀ ([AB])\b')
R_MUC     = re.compile(r'^(★+)\s*MỨC (\d)')


def micro_cua(bai, y):
    """CĐ-4.2 → DL:KSN5Q1.B4.M2 — trục nối hai quyển, đã kiểm khớp 168/168."""
    return f'DL:KSN5Q1.B{bai}.M{y}'


def cat_khoi(ps):
    """Chia sách thành các khối lớn, bỏ phần mục lục ở đầu."""
    moc = []
    for i, p in enumerate(ps):
        if i < 45:                      # 45 đoạn đầu là bìa + mục lục + lời mở đầu
            continue
        for rx, loai in ((R_VONG, 'vong'), (R_TRON, 'detron'), (R_THI, 'thithu')):
            m = rx.match(p)
            if m:
                moc.append((i, loai, int(m.group(1))))
                break
    moc.append((len(ps), 'het', 0))
    return moc


def rut_cau(khuc):
    """
    Đề bài (Câu n.) và lời chữa (Câu n:) — sách để ở hai màn khác nhau.

    Khoá theo (ĐỀ, số câu) chứ không theo số câu: kỳ thi thử 3 có đề A và đề B
    cùng đánh số từ 1, khoá theo số là mất trắng một đề.
    """
    de, dap, muc = {}, {}, {}
    muc_hien, de_hien = 1, ''
    for p in khuc:
        m = R_MAN_DE.match(p)
        if m:
            de_hien = m.group(1); continue
        if p.startswith('✦  ĐÁP ÁN ĐỀ '):
            de_hien = p.replace('✦  ĐÁP ÁN ĐỀ ', '').strip()[:1]; continue
        m = R_MUC.match(p)
        if m:
            muc_hien = int(m.group(2)); continue
        m = R_DE.match(p)
        if m:
            k = (de_hien, int(m.group(1)))
            de[k] = m.group(2); muc[k] = muc_hien
            continue
        m = R_DAP.match(p)
        if m:
            dap[(de_hien, int(m.group(1)))] = m.group(2); continue
        if R_DAP_AB.match(p):
            for de_ma, so, loi in R_DAP_GOP.findall(p):
                loi = loi.strip()
                if loi:
                    dap[(de_ma, int(so))] = loi
    return de, dap, muc


def rut_bay_toa(khuc):
    """Màn 3 — phiên tòa: mã bẫy gắn với số câu, kèm tên và thần chú."""
    ra = []
    for i, p in enumerate(khuc):
        m = R_BAY_TOA.match(p)
        if not m:
            continue
        bai, y = int(m.group(1)), int(m.group(2))
        cac_cau = [int(x) for x in re.findall(r'\d+', m.group(3))]
        mo_ta = khuc[i + 1] if i + 1 < len(khuc) else ''
        ten = mo_ta.split('→')[0].strip()
        # Sách ghi thần chú hai kiểu: 'tên → thần chú: "…"' và 'tên → "…"'.
        # Chỉ bắt kiểu có nhãn thì mất phần lớn thần chú (bị mắt phát hiện, không
        # phải bộ kiểm — nên đã bổ sung phép kiểm ở cổng).
        tc = (re.search(r'thần chú:\s*[“"](.+?)[”"]', mo_ta)
              or re.search(r'→\s*[“"](.+?)[”"]', mo_ta))
        ra.append({
            'ma': f'CĐ-{bai}.{y}', 'cau': cac_cau[0], 'cacCau': cac_cau, 'ten': ten,
            'thanChu': tc.group(1) if tc else '',
            'micro': micro_cua(bai, y),
        })
    return ra


def rut_ho_so(ps):
    """Phụ lục 1 — 168 hồ sơ bẫy đầy đủ."""
    try:
        dau = next(i for i, p in enumerate(ps) if p == 'PHẦN II · 168 HỒ SƠ BẪY THEO 14 CHƯƠNG')
    except StopIteration:
        return []
    ra, chuong, bai, ten_bai = [], 0, 0, ''
    for i in range(dau, len(ps)):
        p = ps[i]
        m = R_CHUONG.match(p)
        if m:
            chuong = int(m.group(2)); continue
        m = R_BAI_HS.match(p)
        if m:
            bai = int(m.group(1)); ten_bai = m.group(2); continue
        m = R_BAY_HS.match(p)
        if not m:
            continue
        b, y, canh, ten = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
        lay = lambda nhan: next(
            (ps[k].split(':', 1)[1].strip() for k in range(i + 1, min(i + 5, len(ps)))
             if ps[k].startswith(nhan)), '')
        ra.append({
            'ma': f'CĐ-{b}.{y}', 'chuong': chuong, 'bai': b, 'tenBai': ten_bai,
            'tang': len(canh), 'ten': ten,
            'dauHieu': lay('Dấu hiệu'), 'donGo': lay('Đòn gỡ'),
            'thanChu': lay('Thần chú').strip('“”"'),
            'micro': micro_cua(b, y),
        })
    return ra


def rut_the(ps):
    """Phụ lục 2 — 14 thẻ chiến thuật, mỗi chương một thẻ."""
    vt = [(i, R_THE.match(p)) for i, p in enumerate(ps) if R_THE.match(p)]
    ra = []
    for k, (i, m) in enumerate(vt):
        het = vt[k + 1][0] if k + 1 < len(vt) else len(ps)
        than = [x for x in ps[i + 1:het] if not x.startswith('KỸ SƯ NHÍ')]
        ra.append({'so': int(m.group(1)), 'chuong': int(m.group(2)),
                   'ten': m.group(3), 'dong': than})
    return ra


def rut_ky_nang(ps):
    """Khối 1 — 5 bài kỹ năng phòng thi."""
    # Dòng mục lục liệt kê NHIỀU bài trên một dòng ("T1 · … T2 · … T3 · …") —
    # nhận ra bằng chính dấu hiệu đó, đừng đoán theo chữ hoa hay khoảng trắng.
    nhieu_bai = re.compile(r'T\d\s*·.*T\d\s*·')
    vt = [(i, R_KYNANG.match(p)) for i, p in enumerate(ps[:600])
          if R_KYNANG.match(p) and not nhieu_bai.search(p)]
    # mỗi bài xuất hiện vài lần (mục lục, chân trang) — lấy lần có nội dung dài nhất sau nó
    theo_ma = {}
    for i, m in vt:
        ma = m.group(1)
        if ma not in theo_ma or i > theo_ma[ma][0]:
            theo_ma[ma] = (i, m)
    moc = sorted((i, m) for i, m in theo_ma.values())
    ra = []
    for k, (i, m) in enumerate(moc):
        het = moc[k + 1][0] if k + 1 < len(moc) else min(i + 90, len(ps))
        # Thân bài chia theo dấu ①②③… của sách; đoạn nào không thuộc mục nào thì
        # gom vào mục đang mở. Bỏ dòng chân trang lặp lại ở mọi trang.
        muc, hien = [], None
        for t in ps[i + 1:het]:
            if t.startswith(('KỸ SƯ NHÍ', 'QUYỂN 2 ·')):
                continue
            d = re.match(r'^([①②③④⑤⑥⑦⑧])\s*(.*)$', t)
            if d:
                hien = {'so': d.group(1), 'ten': d.group(2).strip(), 'dong': []}
                muc.append(hien)
            elif hien is not None:
                hien['dong'].append(t)
            else:
                muc.append({'so': '', 'ten': '', 'dong': [t]})
                hien = muc[-1]
        ra.append({'ma': m.group(1), 'ten': m.group(2).strip(),
                   'phuDe': (m.group(3) or '').strip(), 'muc': muc})
    return ra


def main():
    ps = doan_van(NGUON)
    moc = cat_khoi(ps)

    ban = {'nguon': os.path.basename(NGUON), 'soDoan': len(ps),
           'vong': [], 'detron': [], 'thithu': []}

    for k in range(len(moc) - 1):
        i, loai, so = moc[k]
        j = moc[k + 1][0]
        khuc = ps[i:j]
        if loai == 'het':
            continue
        de, dap, muc = rut_cau(khuc)
        muc_dict = {}
        for p in khuc:
            m = R_MAN.match(p)
            if m:
                muc_dict.setdefault(int(m.group(1)), m.group(2))
        khoi = {
            'so': so, 'ten': khuc[1] if len(khuc) > 1 else '',
            'moTa': khuc[2] if len(khuc) > 2 else '',
            'dongDau': i,
            'man': muc_dict,
            'cau': [{'ma': (f'{d}C{n}' if d else f'C{n}'), 'so': n, 'de_phu': d,
                     'muc': muc.get((d, n), 1),
                     'de': de[(d, n)], 'dap': dap.get((d, n), '')}
                    for d, n in sorted(de, key=lambda t: (t[0], t[1]))],
            'bay': rut_bay_toa(khuc),
        }
        ban[loai].append(khoi)

    ban['kyNang'] = rut_ky_nang(ps)
    ban['hoSo'] = rut_ho_so(ps)
    ban['the'] = rut_the(ps)

    os.makedirs(os.path.dirname(RA), exist_ok=True)
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(ban, f, ensure_ascii=False, indent=1)

    tong_cau = sum(len(v['cau']) for k in ('vong', 'detron', 'thithu') for v in ban[k])
    print(f'đã ghi {RA}')
    print(f'  vòng đấu {len(ban["vong"])} · đề trộn {len(ban["detron"])} · thi thử {len(ban["thithu"])}')
    print(f'  câu hỏi {tong_cau} · hồ sơ bẫy {len(ban["hoSo"])} · thẻ {len(ban["the"])}'
          f' · bài kỹ năng {len(ban["kyNang"])}')


if __name__ == '__main__':
    main()
