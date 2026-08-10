# -*- coding: utf-8 -*-
"""
Tách câu KỲ SÁT HẠCH của lớp 2 và lớp 3 thành ô điền được để máy chấm.

    python3 tools/tach_ontap.py lop3            # dựng + in bảng tổng
    python3 tools/tach_ontap.py lop2 --soat     # chỉ in, không ghi
    python3 tools/tach_ontap.py lop3 --in       # in TỪNG CÂU để soát tay

── VÌ SAO ──

`web/test/luat_o_nhap.test.mjs` (sau khi mở rộng ở đợt lớp 4) in ra mỗi lần chạy:

    lop2: ⏸ 138 câu kỳ sát hạch CHƯA có ô nhập — bé tự đánh dấu đúng/sai
    lop3: ⏸ 198 câu kỳ sát hạch CHƯA có ô nhập — bé tự đánh dấu đúng/sai

Kỳ sát hạch là chỗ quyết định bé qua chương hay không. Để bé tự bấm "Mình làm đúng"
thì sổ phụ huynh và bảng cô giáo nhận đúng con số bé tự chấm cho mình — tức không
đo được gì ở đúng chỗ cần đo nhất.

MỘT tệp cho CẢ HAI quyển, không chép ra hai bản: hai quyển chỉ khác nhau ở hình
dạng tệp nguồn (lớp 2 để các khối ở tầng gốc, lớp 3 gói trong `khoi`), còn luật tách
thì dùng chung với lớp 4 — và dùng chung nghĩa là sửa một chỗ thì cả ba cùng được.

Khoá kết quả: `<mã khối>#<mã câu>` — ví dụ `O1#C1`, `A2#B3`. Đó là đúng khoá mà bộ
dựng đang cầm trong tay khi nó duyệt từng khối, nên không phải suy lại số chương.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tach_cau_lop4 import suy_ra, _that                            # noqa: E402

# Đề B của lớp 2 nhồi nhiều câu trên MỘT dòng ("B1. … B2. … B3. …"), y như đề B của
# lớp 3 hồi bóc tách. Phải cắt theo `B<số>.` thì mỗi câu mới thành một câu thật.
R_CAT_DEB = re.compile(r'(?=B\d+\.\s)')


def khoi_cua(quyen):
    """Trả {mã khối: khối} cho cả hai kiểu tệp nguồn."""
    d = json.load(open(os.path.join(GOC_KHO, 'data', f'{quyen}_ontap.json'),
                      encoding='utf-8'))
    if 'khoi' in d:
        return d['khoi']
    return {k: v for k, v in d.items() if not k.startswith('_')}


def cau_de_b(khoi):
    """Câu đề B, đã cắt nếu quyển ấy nhồi nhiều câu một dòng."""
    if khoi.get('cauDeB'):
        return [{'id': c.get('id') or f"B{c['so']}", 'text': c['text']}
                for c in khoi['cauDeB']]
    ra = []
    for dong in khoi.get('deB') or []:
        for manh in R_CAT_DEB.split(dong):
            manh = manh.strip()
            m = re.match(r'^B(\d+)\.\s*(.+)$', manh, re.S)
            if m:
                ra.append({'id': f'B{m.group(1)}', 'text': ' '.join(m.group(2).split())})
    return ra


def main(quyen, chi_soat=False):
    ra_duong = os.path.join(GOC_KHO, 'data', f'{quyen}_ontap_o.json')
    tay_duong = os.path.join(GOC_KHO, 'data', f'{quyen}_ontap_tay.json')
    tay = json.load(open(tay_duong, encoding='utf-8')) if os.path.exists(tay_duong) else {}
    tay = {k: v for k, v in tay.items() if not k.startswith('_')}

    ra, thong_ke, soat, canh_bao = {}, {}, [], []
    for ma, b in khoi_cua(quyen).items():
        phan_a = [{'id': c.get('id') or f"C{c['so']}", 'text': c['text']}
                  for c in (b.get('cau') or [])]
        for phan, cs, da in (('C', phan_a, b.get('dapAn') or {}),
                             ('B', cau_de_b(b), b.get('dapAnB') or {})):
            for c in cs:
                khoa_ma = f"{ma}#{c['id']}"
                loi = da.get(c['id'], '')
                cau = {'text': c['text'], 'loiChua': loi}
                if khoa_ma in tay:
                    k, ten = tay[khoa_ma], 'VIẾT TAY'
                    nguon = loi + ' ⟂ ' + c['text']
                    for gt in ([p['value'] for p in k['parts']] if 'parts' in k
                               else k.get('values') or [k.get('value')]):
                        if gt is not None and not _that(gt, nguon):
                            canh_bao.append(f'{khoa_ma}: viết tay "{gt}" mà sách '
                                            f'không có chữ ấy ở đề lẫn lời giải')
                else:
                    k, ten = suy_ra(cau, khoa_ma)
                    # Bẫy 11 — "đề hỏi hai thứ mà chỉ lấy một đáp". Sách ngăn hai
                    # đáp án bằng dấu ';' ("460; gấp 10 lần"), mà luật `r_mot_dap`
                    # chỉ canh số dấu '?' — đề viết theo lối sai khiến ("Đọc số…
                    # Viết số…") thì không có dấu hỏi nào và nó nhận một ô tỉnh bơ.
                    # Gặp dấu ';' có chữ số ở CẢ HAI vế thì trả về soát tay.
                    if k and 'parts' not in k and 'values' not in k and ';' in loi:
                        ve = [x for x in loi.split(';') if re.search(r'\d', x)]
                        if len(ve) > 1:
                            k, ten = None, 'chờ soát tay (đáp án có hai vế)'
                thong_ke[ten] = thong_ke.get(ten, 0) + 1
                if k:
                    ra[khoa_ma] = k
                    soat.append((khoa_ma, ten, c['text'], loi, k))

    if not chi_soat:
        with open(ra_duong, 'w', encoding='utf-8') as f:
            json.dump(ra, f, ensure_ascii=False, indent=1, sort_keys=True)

    for c in canh_bao[:20]:
        print(f'  ⚠ {c}')
    tong = sum(thong_ke.values())
    o = sum(len(v['parts']) if 'parts' in v else 1 for v in ra.values())
    nut = sum(1 for v in ra.values() for p in v.get('parts', []) if p.get('options'))
    print(f'{quyen}: {len(ra)}/{tong} câu kỳ sát hạch chấm máy được '
          f'({len(ra) * 100 // max(tong, 1)}%) · {o} ô nhập · {nut} ô bấm chọn')
    for x, v in sorted(thong_ke.items(), key=lambda y: -y[1]):
        print(f'  {v:>4}  {x}')
    return soat, canh_bao


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        raise SystemExit('cần nêu quyển: lop2 hoặc lop3')
    ds, cb = main(args[0], '--soat' in sys.argv)
    if '--in' in sys.argv:
        for ma, ten, text, loi, k in ds:
            print(f'\n{ma}  [{ten}]')
            print(f'  ĐỀ  : {text[:130]}')
            print(f'  SÁCH: {loi[:130]}')
            print(f'  MÁY : {json.dumps(k, ensure_ascii=False)[:150]}')
    raise SystemExit(1 if cb else 0)
