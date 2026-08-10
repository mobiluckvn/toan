# -*- coding: utf-8 -*-
"""
LỚP 4 · tách câu ÔN TẬP và ĐỀ B thành ô điền được để máy chấm.

    python3 tools/tach_ontap_lop4.py            # dựng + in bảng tổng
    python3 tools/tach_ontap_lop4.py --soat     # chỉ in, không ghi
    python3 tools/tach_ontap_lop4.py --in       # in TỪNG CÂU để soát tay

── VÌ SAO CÓ TỆP NÀY ──

Phần luyện tập đã chấm máy 98%, nhưng **kỳ sát hạch thì chưa chấm được câu nào**:
`ExamPlayer.jsx` chỉ hiện một nút "Con làm xong — xem lời giải" rồi hỏi bé tự đánh
dấu đúng/sai. Nghĩa là 236 câu quan trọng NHẤT của quyển — chỗ quyết định bé có qua
chương hay không — lại là chỗ không đo được gì. Sổ phụ huynh và bảng cô giáo nhận
đúng con số bé TỰ CHẤM cho mình.

Đó là nếp cũ từ lớp 5: kỳ sát hạch lớp 5 là câu tự luận dài, tự chấm là hợp lý. Sách
lớp 4 thì khác hẳn — 236 câu đều có đáp số xác định, chấm máy được.

**Dùng lại nguyên bộ luật của `tach_cau_lop4.py`**, vì câu ôn tập cùng khuôn với câu
luyện tập (chính sách lấy lại đề từ các bài trong chương). Chép ra bản thứ hai là bản
ấy tụt hậu ngay lần sửa sau.

Bảng viết tay riêng: `data/lop4_ontap_tay.json`.
"""
import json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tach_cau_lop4 import suy_ra, _that                            # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop4_ontap.json')
RA = os.path.join(GOC_KHO, 'data', 'lop4_ontap_o.json')
TAY = os.path.join(GOC_KHO, 'data', 'lop4_ontap_tay.json')


def main(chi_soat=False):
    ky = json.load(open(NGUON, encoding='utf-8'))['ky']
    tay = json.load(open(TAY, encoding='utf-8')) if os.path.exists(TAY) else {}
    tay = {k: v for k, v in tay.items() if not k.startswith('_')}

    ra, thong_ke, soat, canh_bao = {}, {}, [], []
    for k in ky:
        for phan, ds in (('C', k['examA']), ('B', k['deB'])):
            for q in ds:
                ma = f"OT{k['so']}#{phan}{q['qno']}"
                # `suy_ra` nhận đúng hình dạng câu của bước 3: text + loiChua
                cau = {'text': q['text'], 'loiChua': q.get('answer', '')}
                if ma in tay:
                    khoa, ten = tay[ma], 'VIẾT TAY'
                    nguon = cau['loiChua'] + ' ⟂ ' + cau['text']
                    for gt in ([p['value'] for p in khoa['parts']] if 'parts' in khoa
                               else khoa.get('values') or [khoa.get('value')]):
                        if gt is not None and not _that(gt, nguon):
                            canh_bao.append(f'{ma}: viết tay "{gt}" mà sách không có '
                                            f'chữ ấy ở đề lẫn lời giải')
                else:
                    khoa, ten = suy_ra(cau, ma)
                thong_ke[ten] = thong_ke.get(ten, 0) + 1
                if khoa:
                    ra[ma] = khoa
                    soat.append((ma, ten, q['text'], q.get('answer', ''), khoa))

    if not chi_soat:
        with open(RA, 'w', encoding='utf-8') as f:
            json.dump(ra, f, ensure_ascii=False, indent=1, sort_keys=True)

    for c in canh_bao[:20]:
        print(f'  ⚠ {c}')
    tong = sum(thong_ke.values())
    o = sum(len(v['parts']) if 'parts' in v else 1 for v in ra.values())
    nut = sum(1 for v in ra.values() for p in v.get('parts', []) if p.get('options'))
    print(f'{len(ra)}/{tong} câu ôn tập chấm máy được ({len(ra) * 100 // tong}%)'
          f' · {o} ô nhập · {nut} ô bấm chọn')
    for x, v in sorted(thong_ke.items(), key=lambda y: -y[1]):
        print(f'  {v:>4}  {x}')
    return soat, canh_bao


if __name__ == '__main__':
    ds, cb = main('--soat' in sys.argv)
    if '--in' in sys.argv:
        for ma, ten, text, loi, k in ds:
            print(f'\n{ma}  [{ten}]')
            print(f'  ĐỀ  : {text[:130]}')
            print(f'  SÁCH: {loi[:130]}')
            print(f'  MÁY : {json.dumps(k, ensure_ascii=False)[:150]}')
    raise SystemExit(1 if cb else 0)
