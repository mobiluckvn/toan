# -*- coding: utf-8 -*-
"""
LỚP 2 · trích 8 BÀI ÔN TẬP và 3 ẢI thành kỳ sát hạch.

    python3 tools/rut_ontap_lop2.py

Nguồn là trường `sauBai` của bản trích thô — phần sách nằm GIỮA hai bài học, gồm
ôn tập cuối chương, ba ải cuối sách và toàn bộ đáp án. Trước đây phần này rơi hết
vào mục "Góc bố mẹ" của bài cuối chương (639 dòng rác); nay cất riêng nên trích lại
không phải bóc lại .docx.

Ra đúng khuôn kỳ sát hạch của lớp 5 (`content/reviews/DCR_*.json`) để dùng chung
ExamPlayer — trong đó BẢNG TỰ SOI của sách khớp thẳng vào `diagnosesMicro`:
sai câu nào thì bấm một nút là mở đúng bài cần ôn.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'data', 'lop2_tho.json')
RA = os.path.join(GOC_KHO, 'data', 'lop2_ontap.json')

R_ON = re.compile(r'^ÔN TẬP (\d+)\s*·\s*(.+)$')
R_AI = re.compile(r'^★+\s*ẢI (\d+)\s*—\s*(.+?)\s*\(\d+ câu\)')
R_PHAN = re.compile(r'^(★+)\s*(PHẦN \d+|BUỔI [^—]*)\s*—\s*(.+?)\s*\((\d+) câu\)')
R_CAU = re.compile(r'^(?:Câu|Vụ) (\d+)\.\s*(.+)$')
R_SOI = re.compile(r'^✦\s*BẢNG TỰ SOI')
R_DEB = re.compile(r'^✦\s*(?:ĐỀ B|HỒ SƠ B)\b')
# Dòng tự soi hay có chữ chen giữa các số:
#   "Câu 6, 7 và dãy C của mật thư → thuộc Bài 10"
#   "Vụ 7 câu (a), Vụ 8 → thuộc Bài 25"
# Nên lấy MỌI số ở vế trái dấu →, không đòi chúng phải liền nhau.
R_SOI_DONG = re.compile(r'^(?:Câu|Vụ)\b(.*?)→\s*thuộc Bài (\d+)')
R_DAP_ON = re.compile(r'^Ô(\d+)(B?)\s+ĐÁP ÁN')
R_DAP_AI = re.compile(r'^★+\s*ĐÁP ÁN ẢI (\d+)')
# Sách không nhất quán cách đánh mã đáp án:
#   "C1:"  · "C4 (tổng 3):"  · "C10 — MẬT THƯ:"  · Ôn tập 6 dùng "Vụ 1:" và "VB1:"
# Bỏ sót kiểu nào là câu ấy mất trắng lời giải mà chẳng có gì báo.
R_MA = re.compile(r'\b(?:([CB])(\d+)|(Vụ|VB)\s*(\d+))'
                  r'\s*(?:\([^)]*\)|[—–-]\s*[^:]{0,32})?\s*:\s*')
# Ngưỡng đạt cũng mỗi chương một giọng: "Đạt 8/12 câu" · "Phá được 6/8 vụ"
R_DAT = re.compile(r'(?:Đạt|Phá được|Đúng)\s*(\d+)\s*/\s*(\d+)')


def _tach_ma(dong):
    """Gộp các dòng đáp án rồi tách theo mã C1/B1 → {mã: lời giải}."""
    gop = ' '.join(dong)
    vt = []
    for m in R_MA.finditer(gop):
        if m.group(1):                       # C1 / B1
            ma = m.group(1) + m.group(2)
        else:                                # Vụ 1 → C1 · VB1 → B1
            ma = ('B' if m.group(3) == 'VB' else 'C') + m.group(4)
        vt.append((ma, m.start(), m.end()))
    ra = {}
    for i, (ma, _, het) in enumerate(vt):
        ket = vt[i + 1][1] if i + 1 < len(vt) else len(gop)
        loi = gop[het:ket].strip().rstrip('.;, ')
        if loi:
            ra[ma] = loi
    return ra


def main():
    B = json.load(open(NGUON, encoding='utf-8'))
    dong = [s for b in B['bai'] for s in b['sauBai']]

    de = {}          # 'O1' / 'A1' → {ten, gioiThieu, can, tong, cau[], deB[], soi{}}
    dap = {}         # 'O1' / 'O1B' / 'A1' → {mã: lời giải}
    hien = phan = None
    che_do = 'de'    # de | soi | deb
    dap_hien = None

    for t in dong:
        m = R_ON.match(t)
        if m:
            hien = f'O{m.group(1)}'; phan = 1; che_do = 'de'; dap_hien = None
            de[hien] = {'loai': 'ontap', 'so': int(m.group(1)), 'ten': t,
                        'gioiThieu': [], 'cau': [], 'deB': [], 'soi': {}}
            continue
        m = R_AI.match(t)
        if m:
            hien = f'A{m.group(1)}'; phan = int(m.group(1)); che_do = 'de'; dap_hien = None
            de[hien] = {'loai': 'ai', 'so': int(m.group(1)), 'ten': t,
                        'gioiThieu': [], 'cau': [], 'deB': [], 'soi': {}}
            continue
        m = R_DAP_ON.match(t)
        if m:
            dap_hien = f'O{m.group(1)}' + ('B' if m.group(2) else ''); hien = None
            dap.setdefault(dap_hien, []); continue
        m = R_DAP_AI.match(t)
        if m:
            dap_hien = f'A{m.group(1)}'; hien = None
            dap.setdefault(dap_hien, []); continue
        if re.match(r'^(TOÁN TƯ DUY|CHƯƠNG \d|BẢNG SƯU TẬP|LỜI KẾT|VƯỢT ẢI TOÀN SÁCH)', t):
            hien = dap_hien = None; continue

        if dap_hien is not None:
            if R_MA.search(t):
                dap[dap_hien].append(t)
            continue
        if hien is None:
            continue

        d = de[hien]
        if R_SOI.match(t): che_do = 'soi'; continue
        if R_DEB.match(t): che_do = 'deb'; continue
        m = R_PHAN.match(t)
        if m:
            phan = len(m.group(1)); continue

        if che_do == 'soi':
            m = R_SOI_DONG.match(t)
            if m:
                for so in re.findall(r'\d+', m.group(1)):
                    # Câu nào được nhắc ở HAI bài (ví dụ Vụ 7 của Ôn tập 6) thì
                    # giữ bài nhắc TRƯỚC — đó là bài dạy ý chính của câu ấy.
                    d['soi'].setdefault(int(so), int(m.group(2)))
            elif R_DAT.search(t):
                d['ketLuan'] = t
            continue
        if che_do == 'deb':
            d['deB'].append(t); continue

        m = R_CAU.match(t)
        if m:
            d['cau'].append({'so': int(m.group(1)), 'muc': phan, 'text': m.group(2)})
        elif not d['cau']:
            d['gioiThieu'].append(t)
            g = R_DAT.search(t)
            if g:
                d['can'], d['tong'] = int(g.group(1)), int(g.group(2))

    for k, v in dap.items():
        dap[k] = _tach_ma(v)
    for k, d in de.items():
        d['dapAn'] = dap.get(k, {})
        d['dapAnB'] = dap.get(k + 'B', {})
        d.setdefault('can', 8)
        d.setdefault('tong', len(d['cau']))

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(de, f, ensure_ascii=False, indent=1)

    print(f'đã ghi {RA}')
    for k in sorted(de, key=lambda x: (x[0], int(x[1:]))):
        d = de[k]
        thieu = [c['so'] for c in d['cau'] if f"C{c['so']}" not in d['dapAn']]
        print(f"  {k}  {len(d['cau']):>2} câu · đáp án {len(d['dapAn']):>2}"
              f" · tự soi {len(d['soi']):>2} · đạt {d['can']}/{d['tong']}"
              f"{'  ⚠ thiếu đáp án câu ' + str(thieu) if thieu else ''}")


if __name__ == '__main__':
    main()
