# -*- coding: utf-8 -*-
"""
MA TRẬN KIẾN THỨC — đọc `docs/Ma_tran_kien_thuc_Toan5_HSG_Cap4.xlsx` và đối chiếu
với bản đồ tri thức `data/km_v1_38.json`.

    python3 tools/ma_tran.py            # in bảng đối chiếu

── VÌ SAO CÓ TỆP NÀY ──

Bác gửi tệp Excel ma trận với ý "dựng bản đồ chủ đề từ đây". Nhưng đối chiếu bằng
máy thì **ma trận ấy ĐÃ CÓ SẴN trong kho** dưới dạng `data/km_v1_38.json`:

    264/264 trường hợp trùng tên  ·  264/264 trùng mức CB/NC  ·  5/5 mảng

Chỗ lệch duy nhất là CÁCH VIẾT: bản đồ viết tắt ("2. Hình tam giác"), Excel viết đủ
("2. Hình tam giác (trọng tâm HSG)"). Số hiệu `1.1.` `2.3.` thì trùng khít.

Nên việc phải làm không phải là dựng ma trận mới — mà là **lấy tên đầy đủ từ Excel
đắp vào bản đồ**, rồi đem bản đồ lên web. Tệp này lo phần đọc Excel và ghép cặp;
`tools/dung_chu_de.py` lo phần dựng ra tệp cho máy con dùng.

Đọc Excel bằng `zipfile` + `ElementTree` chứ không cài thư viện: .xlsx là tệp zip
chứa XML, và cả kho này không có `openpyxl`. Ba mươi dòng thay cho một phụ thuộc.
"""
import json, os, re, sys, unicodedata, zipfile
import xml.etree.ElementTree as ET

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(GOC_KHO, 'docs', 'Ma_tran_kien_thuc_Toan5_HSG_Cap4.xlsx')
KM = os.path.join(GOC_KHO, 'data', 'km_v1_38.json')

N = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

# Cột của sheet "Ma trận Cấp 4" — hàng 3 là tiêu đề, hàng 4 trở đi là dữ liệu.
COT = {'A': 'stt', 'B': 'mang', 'C': 'chuDe', 'D': 'dang', 'E': 'truongHop',
       'F': 'phuongPhap', 'G': 'mucDo'}


def _phang(s):
    """So tên thì bỏ qua hoa - thường và khoảng trắng thừa, giữ nguyên dấu tiếng Việt."""
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s or '').strip().lower())


def doc_xlsx(duong=XLSX):
    """264 dòng cấp 4 của Excel, mỗi dòng một dict theo `COT`."""
    z = zipfile.ZipFile(duong)
    kho_chu = [''.join(t.text or '' for t in si.iter(N + 't'))
               for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    ra = []
    for hang in sheet.iter(N + 'row'):
        o = {}
        for c in hang.iter(N + 'c'):
            v = c.find(N + 'v')
            if v is None:
                continue
            cot = ''.join(ch for ch in c.get('r') if ch.isalpha())
            o[cot] = kho_chu[int(v.text)] if c.get('t') == 's' else (v.text or '')
        # Dòng dữ liệu nhận ra bằng cột STT là số — bỏ tiêu đề và dòng ghi chú.
        if o.get('A', '').isdigit():
            ra.append({ten: o.get(cot, '') for cot, ten in COT.items()})
    return ra


def doc_km(duong=KM):
    """Bản đồ tri thức, tách sẵn theo loại nút."""
    km = json.load(open(duong, encoding='utf-8'))
    nut = km['nodes'] if isinstance(km['nodes'], list) else list(km['nodes'].values())
    theo = {}
    for n in nut:
        theo.setdefault(n.get('type'), {})[n['id']] = n
    return km, theo


def ma_so(ten):
    """'1.1. Phân tích cấu tạo số cơ bản' → '1.1' ·  '2. Cấu tạo số thập phân' → '2'.

    Số hiệu là thứ DUY NHẤT trùng khít giữa hai bản, nên mọi phép ghép cặp đều đi
    qua nó. Ghép theo tên thì hụt 17/82 dạng bài chỉ vì bên viết tắt bên viết đủ.
    """
    m = re.match(r'\s*(\d+(?:\.\d+)*)\s*\.', ten or '')
    return m.group(1) if m else None


def ghep(xl=None, theo=None):
    """Ghép Excel vào bản đồ theo SỐ HIỆU, trong phạm vi từng mảng.

    Trả `(ten_dang, ten_chu_de, lech)`:
      ten_dang   {'PT:I.1.1': 'tên đầy đủ từ Excel'}
      ten_chuDe  {'TOPIC:I.1': 'tên đầy đủ từ Excel'}
      lech       danh sách chỗ không ghép được, để in ra soi tay
    """
    xl = xl if xl is not None else doc_xlsx()
    theo = theo if theo is not None else doc_km()[1]
    pt, top = theo['ProblemType'], theo['Topic']

    # Bản đồ dùng id có sẵn mảng ('PT:I.1.1'), Excel thì mảng nằm ở cột riêng dạng
    # 'I. SỐ HỌC & CẤU TẠO SỐ'. Lấy chữ số La Mã đứng đầu làm khoá mảng.
    ten_dang, ten_cd, lech = {}, {}, []
    for r in xl:
        mang = (r['mang'].split('.', 1)[0] or '').strip()
        for kho, ma_muc, nhan in ((pt, ma_so(r['dang']), 'dang'),
                                  (top, ma_so(r['chuDe']), 'chuDe')):
            if not ma_muc:
                lech.append((nhan, r['stt'], r[nhan], 'không đọc được số hiệu'))
                continue
            khoa = ('PT:' if nhan == 'dang' else 'TOPIC:') + f'{mang}.{ma_muc}'
            if khoa not in kho:
                lech.append((nhan, r['stt'], r[nhan], f'{khoa} không có trong bản đồ'))
                continue
            (ten_dang if nhan == 'dang' else ten_cd)[khoa] = r[nhan].strip()
    return ten_dang, ten_cd, lech


def doi_chieu():
    """In bảng đối chiếu. Trả số chỗ lệch thật sự (không tính khác cách viết)."""
    xl = doc_xlsx()
    km, theo = doc_km()
    case, pt, top, area = (theo['Case'], theo['ProblemType'],
                           theo['Topic'], theo['KnowledgeArea'])

    print(f'Excel : {len(xl)} dòng cấp 4')
    print(f'Bản đồ: {len(area)} mảng · {len(top)} chủ đề · {len(pt)} dạng bài · '
          f'{len(case)} trường hợp\n')

    # ── Trường hợp (cấp 4): ghép theo TÊN, vì id CASE không suy được từ Excel.
    ten_case = {}
    for c in case.values():
        ten_case.setdefault(_phang(c['name']), []).append(c)
    trung = mucdo_trung = mo_ho = 0
    thieu = []
    for r in xl:
        ds = ten_case.get(_phang(r['truongHop']), [])
        if not ds:
            thieu.append(r)
            continue
        trung += 1
        if len(ds) > 1:
            mo_ho += 1
        if any(c.get('difficulty') == r['mucDo'] for c in ds):
            mucdo_trung += 1
    print(f'  trường hợp trùng tên : {trung}/{len(xl)}')
    print(f'  mức độ CB/NC trùng   : {mucdo_trung}/{len(xl)}')
    if mo_ho:
        print(f'  ⓘ {mo_ho} dòng trùng tên với NHIỀU trường hợp — ghép theo tên là mơ hồ,'
              f' nên bản đồ chủ đề chỉ dùng tới cấp DẠNG BÀI, không xuống cấp 4')
    for r in thieu[:10]:
        print(f'  ⚠ Excel dòng {r["stt"]}: "{r["truongHop"][:60]}" không có trong bản đồ')

    # ── Dạng bài & chủ đề: ghép theo SỐ HIỆU.
    ten_dang, ten_cd, lech = ghep(xl, theo)
    print(f'\n  dạng bài ghép được   : {len(ten_dang)}/{len(pt)}')
    print(f'  chủ đề ghép được     : {len(ten_cd)}/{len(top)}')
    for l in lech[:10]:
        print(f'  ⚠ {l[0]} dòng {l[1]}: "{l[2][:50]}" — {l[3]}')

    khac = [(k, pt[k]['name'], v) for k, v in ten_dang.items()
            if _phang(pt[k]['name']) != _phang(v)]
    print(f'\n  dạng bài Excel ghi TÊN ĐẦY ĐỦ HƠN: {len(khac)} — đây là thứ đáng lấy về')
    for k, cu, moi in khac[:6]:
        print(f'      {k}\n         bản đồ: {cu}\n         Excel : {moi}')

    thieu_pt = sorted(set(pt) - set(ten_dang))
    if thieu_pt:
        print(f'\n  ⚠ {len(thieu_pt)} dạng bài của bản đồ KHÔNG có trong Excel: '
              + ', '.join(thieu_pt))
    return len(thieu) + len(lech) + len(thieu_pt)


if __name__ == '__main__':
    raise SystemExit(1 if doi_chieu() else 0)
