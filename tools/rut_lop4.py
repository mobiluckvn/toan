# -*- coding: utf-8 -*-
"""
LỚP 4 · BƯỚC 1 — trích sách thành JSON thô, GIỮ NGUYÊN CHỮ.

    python3 tools/rut_lop4.py

Bản trích này là mốc bất biến để đối chiếu với sách giấy. Không ai sửa tay.

BỐN CHỖ KHÁC LỚP 3 — xem `docs/khao_sat_lop4.md`:

1. **Sách lớp 4 dựng bằng BẢNG.** 469 bảng, và phần lớn nội dung giảng nằm TRONG ô
   bảng chứ không phải đoạn văn rời. Bộ trích lớp 3 chỉ đọc `<w:p>` ở tầng ngoài nên
   áp vào đây sẽ mất gần hết chữ mà vẫn dựng ra 44 bài trông hợp lệ. Phải đọc cả
   bảng, và **tách theo từng `<w:p>` bên trong ô** — gộp cả ô thành một dòng thì
   "CHO GÌ? … HỎI GÌ? … ĐẠI LƯỢNG…" dính liền thành một câu vô nghĩa.

2. **Mười mục ①…⑩** thay vì tám. Hai mục mới là ③ (DỊCH — CHO GÌ / HỎI GÌ) và
   ⑤ (LẮP & SOI). Cả hai đều là chữ CON đọc, không phải chú thích của người soạn.

3. **Đáp án nằm cuối CHƯƠNG**, sau ôn tập. Bài phải đóng tại mốc `ĐÁP ÁN CHI TIẾT`
   / `ÔN TẬP` / bảng mở chương — cắt "tới tiêu đề bài kế tiếp" là nuốt trọn đáp án
   của cả chương vào mục ⑩ của bài cuối (bẫy 5 và 6 của chuẩn).

4. **`HẠT MẦM NĂM NGOÁI` nằm trong BẢNG TIÊU ĐỀ BÀI**, không phải đoạn văn riêng.

Cấu trúc rất đều — 44/44 bài đủ ①…⑩ đúng thứ tự, 44 × 4 bước, 44 × (9 + 5) câu —
nên mọi con số đếm được đều được CHỐT ở cuối tệp. Lệch một cái là dừng, vì lệch ở
đây nghĩa là bộ trích trượt chứ không phải sách khác thường.
"""
import json, os, re, zipfile, html

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'docs', 'KSN4_SACH_HOAN_CHINH_Ky_Su_Nhi_Lop4.docx')
RA = os.path.join(GOC_KHO, 'data', 'lop4_tho.json')

R_T = re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
R_KHOI = re.compile(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>|<w:p/>', re.S)
R_P = re.compile(r'<w:p[ >].*?</w:p>|<w:p/>', re.S)
R_TR = re.compile(r'<w:tr[ >].*?</w:tr>', re.S)
R_TC = re.compile(r'<w:tc[ >].*?</w:tc>', re.S)

# `<w:t[^>]*>` cũng khớp `<w:tcPr>` — dấu `c` rơi vào `[^>]*`. Lỗi ấy đổ nguyên văn
# XML vào chữ của bài mà vẫn chạy trót lọt, nên mẫu phải chốt đúng thẻ `w:t`.
R_TIEU_DE_BAI = re.compile(r'^Bài (\d+)\s*·\s*(.+)$')
R_CHUONG = re.compile(r'^CHƯƠNG (\d+)\s*·\s*(.+)$')
R_MUC = re.compile(r'^([①②③④⑤⑥⑦⑧⑨⑩])\s*(.*)$')
R_MUC_SAO = re.compile(r'^(★+)\s*MỨC (\d)')
R_CAU = re.compile(r'^Câu (\d+)\s*(?:\(([^)]*)\))?\s*[.:]\s*(.+)$')
R_DANG = re.compile(r'^Dạng gốc:\s*(.+)$')
R_HAT_MAM = re.compile(r'^HẠT MẦM NĂM NGOÁI:\s*(.+)$')
# `▸ NHỊP 1 · DỊCH — từ bảng tin sang bảng hàng - lớp` là NHÃN của mục, không phải
# một câu giảng. Để lẫn vào `dong` thì nó thành lời văn treo đầu màn (và ở mục ④ nó
# còn đè lên lời của màn giảng cuối, vì khuôn chung dồn "dòng không phải Bước" vào đó).
# Bốn nhịp DỊCH - GIẢI - LẮP - SOI là cái xương sống sách dạy, nên giữ làm nhãn màn.
R_NHIP = re.compile(r'^▸\s*(.+)$')
# Mốc ĐÓNG bài. `ĐÁP ÁN CHI TIẾT` và `ÔN TẬP` là hai mốc thật sự hay gặp; hai mốc
# còn lại đỡ cho trang bìa chương và trang cuối sách.
#
# ⚠ Phải soi VÀI DÒNG ĐẦU của khối, không chỉ dòng thứ nhất. Bảng tiêu đề ôn tập mở
# bằng `CHƯƠNG 1 · ĐẠI CÔNG TRƯỜNG LỚP TRIỆU` rồi mới tới `ÔN TẬP 1 · …`, nên mẫu
# neo vào dòng đầu trượt sạch: 11 bài cuối chương nuốt trọn ôn tập VÀ đáp án chi
# tiết của cả chương vào mục ⑩ Góc bố mẹ — 121-155 dòng rác mỗi bài, lộ nguyên đáp
# án cho người lớn đọc, mà mọi phép đếm câu vẫn đúng nên không có gì kêu. Đây đúng
# là bẫy 5 và 6 của chuẩn, quyển thứ tư vẫn dính.
R_KET = re.compile(r'^(?:ĐÁP ÁN CHI TIẾT|ÔN TẬP \d+|BẢNG SƯU TẬP|KỸ SƯ NHÍ LỚP 4)')
SOI_MAY_DONG = 3

TEN_MUC = {
    '①': 'mucTieu', '②': 'chuyenMoBai', '③': 'dichMoHinh', '④': 'khamPha',
    '⑤': 'lapSoi', '⑥': 'viDuMau', '⑦': 'suKemNham', '⑧': 'luyenTap',
    '⑨': 'quiz', '⑩': 'gocBoMe',
}
CON_DOC = {'mucTieu', 'chuyenMoBai', 'dichMoHinh', 'khamPha', 'lapSoi',
           'viDuMau', 'suKemNham', 'luyenTap', 'quiz'}


def _chu(p):
    p = re.sub(r'<w:tab/>', ' ', p)
    p = re.sub(r'<w:br/>', '\n', p)
    return html.unescape(''.join(R_T.findall(p)))


def _dong_cua(xml_doan):
    """Một `<w:p>` có thể chứa nhiều dòng nhờ `<w:br/>` — trả về từng dòng đã gọn."""
    ra = []
    for ln in _chu(xml_doan).split('\n'):
        ln = ' '.join(ln.split())
        if ln:
            ra.append(ln)
    return ra


def doc_khoi(duong_dan):
    """Đọc tài liệu thành danh sách khối theo ĐÚNG thứ tự in trong sách.

    Mỗi khối: {'dong': [...], 'anh': [...], 'bang': True/False}
    Ô bảng được trải thành dòng theo từng đoạn văn con — xem ghi chú 1 ở đầu tệp.
    """
    z = zipfile.ZipFile(duong_dan)
    xml = z.read('word/document.xml').decode('utf-8')
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',
                           z.read('word/_rels/document.xml.rels').decode('utf-8')))
    than = re.search(r'<w:body>(.*)</w:body>', xml, re.S).group(1)

    ra = []
    for m in R_KHOI.finditer(than):
        blk = m.group(0)
        anh = [rels.get(r, '') for r in re.findall(r'r:embed="(rId\d+)"', blk)]
        if blk.startswith('<w:tbl'):
            dong = []
            for tr in R_TR.findall(blk):
                for tc in R_TC.findall(tr):
                    tc = re.sub(r'<w:tcPr>.*?</w:tcPr>', '', tc, flags=re.S)
                    for p in R_P.findall(tc):
                        dong.extend(_dong_cua(p))
            ra.append({'dong': dong, 'anh': anh, 'bang': True})
        else:
            ra.append({'dong': _dong_cua(blk), 'anh': anh, 'bang': False})
    return [k for k in ra if k['dong'] or k['anh']]


def _la_tieu_de_bai(khoi):
    """Bảng tiêu đề bài: dòng 1 là CHƯƠNG, dòng 2 là 'Bài n · TÊN IN HOA'.

    Dòng mục lục cũng viết 'Bài 1 · Những con số…' nhưng chữ thường và không nằm
    trong bảng có dòng CHƯƠNG đứng trước — so bằng `s == s.upper()` chứ đừng dùng
    dải `à-ỹ`: dải ấy CHỨA CẢ `Đ` `Ơ` `Ư` viết hoa nên mọi tiêu đề tiếng Việt đều
    trượt (bẫy 41).
    """
    if not khoi['bang'] or len(khoi['dong']) < 2:
        return None
    ch = R_CHUONG.match(khoi['dong'][0])
    b = R_TIEU_DE_BAI.match(khoi['dong'][1])
    if not ch or not b:
        return None
    ten = b.group(2).strip()
    if ten != ten.upper():
        return None
    return int(b.group(1)), ten, int(ch.group(1)), ch.group(2).strip()


def main():
    khoi = doc_khoi(NGUON)

    moc = []
    for i, k in enumerate(khoi):
        t = _la_tieu_de_bai(k)
        if t:
            moc.append((i,) + t)
    moc.append((len(khoi), None, None, None, None))

    bai = []
    for n in range(len(moc) - 1):
        i, so, ten, chuong, ten_chuong = moc[n]
        j = moc[n + 1][0]

        muc, hien, dang, mucsao, hat_mam = {}, None, '', 1, ''
        cau, sau_bai, het = [], [], False

        # dòng 3 trở đi của chính bảng tiêu đề: Dạng gốc + HẠT MẦM NĂM NGOÁI
        for t in khoi[i]['dong'][2:]:
            d = R_DANG.match(t)
            if d:
                dang = d.group(1)
            h = R_HAT_MAM.match(t)
            if h:
                hat_mam = h.group(1)

        for k in khoi[i + 1:j]:
            if het or any(R_KET.match(d) for d in k['dong'][:SOI_MAY_DONG]):
                het = True
                sau_bai.extend(k['dong'])
                continue
            for t in k['dong']:
                m = R_MUC.match(t)
                if m:
                    hien = TEN_MUC.get(m.group(1))
                    muc.setdefault(hien, {'ten': m.group(2).strip(), 'dong': [],
                                          'hinh': [], 'nhip': ''})
                    continue
                nh = R_NHIP.match(t)
                if nh and hien:
                    muc[hien]['nhip'] = nh.group(1).strip()
                    continue
                s = R_MUC_SAO.match(t)
                if s and hien == 'luyenTap':
                    mucsao = int(s.group(2))
                    continue
                c = R_CAU.match(t)
                if c and hien in ('luyenTap', 'quiz'):
                    stt = sum(1 for x in cau if x['phan'] == hien) + 1
                    # Mức sao chỉ có ở luyện tập; quiz đứng SAU nên nếu không ghim
                    # `muc: 1` thì mọi câu quiz thừa hưởng "★★★ MỨC 3" của luyện tập.
                    cau.append({'id': ('Q' if hien == 'quiz' else 'C') + str(stt),
                                'maSach': f'C{stt}', 'so': int(c.group(1)),
                                'muc': 1 if hien == 'quiz' else mucsao,
                                'phan': hien, 'ghiChu': (c.group(2) or '').strip(),
                                'text': c.group(3)})
                    continue
                if hien:
                    muc[hien]['dong'].append(t)
            # ảnh gắn vào mục đang mở, ghi rõ đứng sau dòng thứ mấy
            if hien and k['anh']:
                for a in k['anh']:
                    muc[hien]['hinh'].append({'nguon': a,
                                              'sauDong': len(muc[hien]['dong'])})

        bai.append({'so': so, 'ten': ten, 'chuong': chuong,
                    'tenChuong': ten_chuong, 'quyen': 'lop4',
                    'dangGoc': dang, 'hatMam': hat_mam,
                    'muc': muc, 'cau': cau, 'sauBai': sau_bai})

    ban = {'nguon': os.path.basename(NGUON), 'soKhoi': len(khoi),
           'conDoc': sorted(CON_DOC), 'bai': bai}
    os.makedirs(os.path.dirname(RA), exist_ok=True)
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(ban, f, ensure_ascii=False, indent=1)

    # ── CHỐT: sách này đều tuyệt đối, lệch một con số là bộ trích trượt ──
    loi = []
    if len(bai) != 44:
        loi.append(f'{len(bai)} bài, sách có 44')
    for b in bai:
        thieu = [k for k in TEN_MUC.values() if k not in b['muc']]
        if thieu:
            loi.append(f"bài {b['so']} thiếu mục {thieu}")
        lt = [c for c in b['cau'] if c['phan'] == 'luyenTap']
        qz = [c for c in b['cau'] if c['phan'] == 'quiz']
        if len(lt) != 9 or len(qz) != 5:
            loi.append(f"bài {b['so']}: {len(lt)} luyện tập + {len(qz)} quiz"
                       f' (phải là 9 + 5)')
        if not b['hatMam']:
            loi.append(f"bài {b['so']} không có HẠT MẦM NĂM NGOÁI")
        nbuoc = sum(1 for d in b['muc'].get('khamPha', {}).get('dong', [])
                    if re.match(r'^Bước \d+\s*[—–-]', d))
        if nbuoc != 4:
            loi.append(f"bài {b['so']}: {nbuoc} bước trong mục ④ (phải là 4)")
        # Chốt chống bẫy 5/6: phần KHÁC không được lẫn vào bài. Phép đếm câu không
        # bắt được loại này — rác rơi vào mục ⑩ thì mọi con số vẫn tròn trịa.
        for ten, m in b['muc'].items():
            ban = [d for d in m['dong']
                   if re.match(r'^(ĐÁP ÁN|ÔN TẬP \d+|✦\s+(BẢNG TỰ SOI|ĐỀ B)'
                               r'|B\d+\s+ĐÁP ÁN|Ô\d+B?\s+ĐÁP ÁN)', d)]
            if ban:
                loi.append(f"bài {b['so']} mục {ten} lẫn phần khác: {ban[0][:60]!r}")
        # Mục ⑩ dài bất thường là dấu hiệu sớm của cùng một bệnh.
        ngoai = len(b['muc'].get('gocBoMe', {}).get('dong', []))
        if ngoai > 8:
            loi.append(f"bài {b['so']}: Góc bố mẹ {ngoai} dòng — nghi nuốt phần khác")

    print(f'đã ghi {RA}')
    print(f'  {len(bai)} bài · {len({b["chuong"] for b in bai})} chương'
          f' · {sum(len(b["cau"]) for b in bai)} câu'
          f' · {sum(len(m["hinh"]) for b in bai for m in b["muc"].values())} chỗ neo ảnh')
    if loi:
        print(f'  ⚠ {len(loi)} chỗ lệch:')
        for x in loi[:20]:
            print('     ·', x)
        raise SystemExit(1)
    print('  ✓ chốt: 44 bài · đủ ①…⑩ · 9+5 câu · 4 bước · đủ HẠT MẦM')


if __name__ == '__main__':
    main()
