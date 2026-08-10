# -*- coding: utf-8 -*-
"""
LỚP 4 · BƯỚC 2c — bóc 11 kỳ ôn tập: đề chính · BẢNG TỰ SOI · đề B.

    python3 tools/rut_lop4.py && python3 tools/dapan_lop4.py && python3 tools/ontap_lop4.py

Nguồn là `sauBai` của bài cuối mỗi chương (bước 1 đã cất riêng).

**ĐỌC CẤU TRÚC, ĐỪNG DÒ TỪNG DÒNG.** Bài học đắt nhất của lớp 3: mỗi ôn tập luôn có
ba phần ngăn bởi mốc `✦`, và ở phần nào thì chỉ dùng mẫu của phần ấy —

    thân đề  →  ✦ BẢNG TỰ SOI  →  ✦ ĐỀ B  →  ✦ SỔ ĐƠN HÀNG

Làm thế thì dòng mối nối hết cửa rơi xuống thành câu hỏi: mẫu trượt thì MẤT mối nối
và bộ đếm kêu, chứ không đẻ ra câu hỏi ma như lượt lớp 3 đầu tiên (5/8 ôn tập thừa
1-5 câu, và ba hỏng câm đi kèm mà không phép đếm nào bắt được).

BẢNG TỰ SOI của lớp 4 nằm gọn trong MỘT ô bảng, các mối nối viết nối đuôi nhau, và
có **năm dạng** — mẫu chỉ biết dạng đầu là mất mối nối lặng lẽ:

    Câu 1, 2, 3 → thuộc Bài 1 (…)          ← chuẩn
    Câu 1, 2, 3 và Câu 12 → thuộc Bài 5    ← có chữ "và"
    Câu 12 → Bài 19 mức ★★★ (…)            ← KHÔNG có chữ "thuộc"
    Câu 10 → ghép Bài 9 + Bài 10           ← HAI bài
    Câu 10 → tổng hợp cả chương (…)        ← KHÔNG bài nào → canCu 'chuong'

Nên `veCau` là **danh sách** mã bài, không phải một mã. Chốt bắt buộc: mọi câu 1..N
đều phải có mối nối — thiếu một câu là dừng.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop4_tho.json')
DAP = os.path.join(GOC_KHO, 'data', 'lop4_dapan.json')
RA = os.path.join(GOC_KHO, 'data', 'lop4_ontap.json')
TIEN_TO = 'DL:KSN4.'

R_OT = re.compile(r'^ÔN TẬP (\d+)\s*·\s*(.+)$')
# Ngưỡng đạt nhận theo HÌNH DẠNG `a/b`, không liệt kê động từ — liệt kê thì sót, và
# sót lặng lẽ (lớp 3: hai ôn tập tụt về mặc định 10 trong khi sách nói 12).
R_NGUONG = re.compile(r'(\d+)\s*/\s*(\d+)')
R_CAU = re.compile(r'^Câu (\d+)\s*[.:]\s*(.+)$')
R_DEB = re.compile(r'^B(\d+)\s*[.:]\s*(.+)$')
R_MOC = re.compile(r'^✦\s*(.+)$')
R_NOI = re.compile(r'Câu\s*([\d,\s]+(?:và\s*Câu\s*[\d,\s]+)*)→\s*([^.]+?)(?=\.\s|\.$|$)')


def ma_bai(so):
    return f'{TIEN_TO}B{so:02d}'


def _tach_moi_noi(chu, bai_cua_chuong):
    """BẢNG TỰ SOI → {số câu: [mã bài, …]} + căn cứ từng câu."""
    ve, can = {}, {}
    for m in R_NOI.finditer(chu.replace('→', '→')):
        sos = [int(x) for x in re.findall(r'\d+', m.group(1))]
        dich = m.group(2)
        bai = [int(x) for x in re.findall(r'Bài (\d+)', dich)]
        for s in sos:
            if bai:
                ve[s] = [ma_bai(x) for x in bai]
                can[s] = 'sach'
            else:
                # "tổng hợp cả chương" — có thật, không phải lỗi mẫu. Trỏ về đủ các
                # bài của chương, và nói rõ căn cứ để sau này không ai tưởng là sót.
                ve[s] = [ma_bai(x) for x in bai_cua_chuong]
                can[s] = 'chuong'
    return ve, can


def main():
    tho = json.load(open(THO, encoding='utf-8'))
    dap = json.load(open(DAP, encoding='utf-8'))['dapAn']
    bai_theo_chuong = {}
    for b in tho['bai']:
        bai_theo_chuong.setdefault(b['chuong'], []).append(b['so'])

    ky = []
    for b in tho['bai']:
        if not b['sauBai']:
            continue
        dong = b['sauBai']
        # ── tìm đầu ôn tập ──
        i = next((k for k, t in enumerate(dong) if R_OT.match(t)), None)
        if i is None:
            continue
        m = R_OT.match(dong[i])
        so, ten = int(m.group(1)), m.group(2).strip()

        # ── cắt thành ba vùng theo mốc ✦ ──
        vung, ten_vung = {'de': []}, 'de'
        nguong, tong = 0, 0
        for t in dong[i + 1:]:
            if t.startswith('ĐÁP ÁN CHI TIẾT') or re.match(r'^\S+\s+ĐÁP ÁN', t):
                break
            mv = R_MOC.match(t)
            if mv:
                nhan = mv.group(1)
                ten_vung = ('soi' if 'BẢNG TỰ SOI' in nhan else
                            'deB' if nhan.startswith('ĐỀ B') else 'khac')
                vung.setdefault(ten_vung, [])
                continue
            if ten_vung == 'de' and not nguong:
                g = R_NGUONG.search(t)
                if g and 'Đạt' in t:
                    nguong, tong = int(g.group(1)), int(g.group(2))
            vung.setdefault(ten_vung, []).append(t)

        de = [{'qno': int(c.group(1)), 'text': c.group(2)}
              for c in (R_CAU.match(t) for t in vung.get('de', [])) if c]
        deB = [{'qno': int(c.group(1)), 'text': c.group(2)}
               for c in (R_DEB.match(t) for t in vung.get('deB', [])) if c]
        ve, can = _tach_moi_noi(' '.join(vung.get('soi', [])),
                                bai_theo_chuong.get(b['chuong'], []))

        for q in de:
            q['answer'] = dap.get(f'OT{so}#C{q["qno"]}', '')
            q['veCau'] = ve.get(q['qno'], [])
            q['canCu'] = can.get(q['qno'], 'khong')
        for q in deB:
            q['answer'] = dap.get(f'OT{so}#B{q["qno"]}', '')

        ky.append({
            'id': f'DCR:KSN4.C{so}', 'chapter': b['chuong'], 'loai': 'ontap',
            'so': so, 'name': f'ÔN TẬP {so} · {ten}',
            'need': nguong, 'tong': tong,
            'examA': de, 'deB': deB,
        })

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump({'tienTo': TIEN_TO, 'ky': ky}, f, ensure_ascii=False, indent=1)

    # ── CHỐT ──
    loi = []
    if len(ky) != 11:
        loi.append(f'{len(ky)} kỳ ôn tập, sách có 11')
    for k in ky:
        n = len(k['examA'])
        if not 10 <= n <= 12:
            loi.append(f"{k['name']}: {n} câu đề chính")
        if not 10 <= len(k['deB']) <= 12:
            loi.append(f"{k['name']}: {len(k['deB'])} câu đề B")
        if k['need'] < 1 or k['tong'] != n:
            loi.append(f"{k['name']}: ngưỡng {k['need']}/{k['tong']} mà đề có {n} câu")
        # số thứ tự phải liền mạch 1..n — thiếu hay thừa đều là mẫu trượt
        if [q['qno'] for q in k['examA']] != list(range(1, n + 1)):
            loi.append(f"{k['name']}: số câu đề chính không liền mạch")
        # MỐI NỐI phải phủ ĐỦ. Đây là chốt đáng giá nhất của cả bước.
        thieu = [q['qno'] for q in k['examA'] if not q['veCau']]
        if thieu:
            loi.append(f"{k['name']}: {len(thieu)} câu MẤT mối nối: {thieu}")
        trong = [q['qno'] for q in k['examA'] + k['deB'] if not q['answer']]
        if trong:
            loi.append(f"{k['name']}: {len(trong)} câu không có đáp án: {trong}")
        xau = [x for q in k['examA'] for x in q['veCau']
               if x not in {ma_bai(b['so']) for b in tho['bai']}]
        if xau:
            loi.append(f"{k['name']}: trỏ về bài không có thật: {xau}")

    print(f'đã ghi {RA}')
    print(f"  {len(ky)} kỳ ôn tập · {sum(len(k['examA']) for k in ky)} câu đề chính"
          f" · {sum(len(k['deB']) for k in ky)} câu đề B")
    cc = {}
    for k in ky:
        for q in k['examA']:
            cc[q['canCu']] = cc.get(q['canCu'], 0) + 1
    print(f'  căn cứ mối nối: {cc}')
    if loi:
        print(f'  ⚠ {len(loi)} chỗ lệch:')
        for x in loi[:20]:
            print('     ·', x)
        raise SystemExit(1)
    print('  ✓ chốt: đủ 11 kỳ · số câu liền mạch · MỌI câu có mối nối và đáp án')


if __name__ == '__main__':
    main()
