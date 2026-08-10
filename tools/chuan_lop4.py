# -*- coding: utf-8 -*-
"""
LỚP 4 · BƯỚC 3 — dựng dữ liệu bài học GỐC cho phần mềm.

    python3 tools/chuan_lop4.py

Không mở lại docx: bước 1 đã trích, bước 2 đã bóc 852 đáp án khớp 1:1. Ở đây chỉ
GẮN đáp án vào câu rồi ghi ra `data/lop4/`.

Dùng chung `tach_phuong_an` của lớp 2 thay vì chép lại — hàm ấy mang sẵn bài học
"giữ chữ cái đầu phương án vì sách chấm theo chữ cái".

**Đáp án quiz của lớp 4 viết KHÁC lớp 2 và lớp 3.** Hai quyển kia ghi lý do trong
ngoặc (`SAI (chỉ cộng 300)`); lớp 4 ghi sau gạch ngang dài:

    ĐÚNG — chữ số 4 đứng hàng chục nghìn.
    SAI — phải là 2 300 000.
    B (70 000).
    A — 6 + 2 = 8 và 6 − 2 = 4.

Mẫu của lớp 3 đòi phần sau phải nằm trong ngoặc nên **đọc được đúng dạng thứ ba**;
220 câu quiz sẽ tụt về tự chấm mà không có gì báo, vì "không đọc được đáp án thì để
bé tự chấm" là hành vi ĐÚNG của bộ dựng. Nên ở đây viết mẫu riêng, và CHỐT lại bằng
số: cả 220 câu quiz phải chấm máy được.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chuan_lop2 import tach_phuong_an                             # noqa: E402

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop4_tho.json')
DAP_AN = os.path.join(GOC_KHO, 'data', 'lop4_dapan.json')
GAN = os.path.join(GOC_KHO, 'data', 'lop4_gan_lop3.json')
RA_DATA = os.path.join(GOC_KHO, 'data', 'lop4')

MA_BAI = 'DL:KSN4.B{:02}'
# Đáp số đứng đầu, rồi tới lời giải thích ngăn bằng gạch ngang dài / ngoặc / dấu chấm.
R_QUIZ = re.compile(r'^\s*(ĐÚNG|SAI|[A-D])\b\s*\.?\s*(?:[—–-]\s*|\(\s*)?(.*?)\)?\s*$')


def doc_dap_quiz(s):
    """"SAI — phải là 2 300 000." → ("SAI", "phải là 2 300 000.").

    Không đọc được thì trả None để câu ấy rơi về tự chấm — thà bé tự so còn hơn máy
    chấm sai. Nhưng chốt cuối tệp sẽ kêu nếu chuyện ấy xảy ra, vì sách lớp 4 ghi đáp
    án quiz đều tăm tắp: không đọc được nghĩa là mẫu hỏng, không phải sách thiếu.
    """
    m = R_QUIZ.match(s or '')
    return (m.group(1), (m.group(2) or '').strip()) if m else None


def dung_cau_quiz(c, dap):
    """Một câu quiz thành câu CHẤM ĐƯỢC: Đúng/Sai hoặc trắc nghiệm A·B·C."""
    de, pa = tach_phuong_an(c['text'])
    if dap is None:
        return {**c, 'text': de, 'choices': pa, 'loiChua': '', 'tuLuan': True}
    kq, giai = dap

    if kq in ('ĐÚNG', 'SAI'):
        return {**c, 'text': de, 'format': 'tf', 'tuLuan': False,
                'answerKey': {'value': kq == 'ĐÚNG'},
                'loiChua': giai or f'Đáp án: {kq}',
                'solutionNarrative': giai}

    # trắc nghiệm: đối chiếu CHỮ CÁI với phương án đã tách từ đề. Không khớp thì
    # để tự chấm chứ đừng đoán — chấm sai một câu là bé mất tin vào cả phần mềm.
    chon = next((p for p in pa if p.startswith(f'{kq}.')), '')
    if not chon:
        return {**c, 'text': de, 'choices': pa, 'loiChua': giai, 'tuLuan': True}
    return {**c, 'text': de, 'choices': pa, 'format': 'mcq', 'tuLuan': False,
            'answerKey': {'choice': chon},
            'loiChua': giai or f'Đáp án: {chon}',
            'solutionNarrative': giai}


# Mục ⑥ dựng bằng BẢNG HAI CỘT, nên hai ô tiêu đề cột lọt vào danh sách dòng và
# trở thành hai "bước giải" rỗng ruột trong màn Bài mẫu — bé bấm "Bước tiếp" hai lần
# chỉ để đọc hai cái nhãn cột. Chúng là nhãn của bảng giấy, không phải lời giải.
TIEU_DE_COT = {'TRANG VỞ CỦA CON', 'VÌ SAO VIẾT DÒNG NÀY?'}


def _muc_sach(muc):
    """Dọn danh sách hình về RỖNG trước khi ghi tầng GỐC.

    Tầng THÔ ghi lại chỗ neo ảnh CỦA SÁCH (`{'nguon': 'media/image33.png'}`) làm
    bằng chứng đối chiếu. Nhưng app dùng hình do `figforge` vẽ lại, và bước gắn hình
    tìm khoá `id` trong danh sách ấy — để lẫn hai loại vào nhau là bước gắn vỡ, hoặc
    tệ hơn: gắn xen kẽ ảnh sách với hình vẽ mới, hai bảng màu đá nhau trên cùng màn.
    """
    return {k: {**v, 'hinh': [],
                'dong': [d for d in v.get('dong', []) if d not in TIEU_DE_COT]}
            for k, v in muc.items()}


def main():
    d = json.load(open(THO, encoding='utf-8'))
    dap = json.load(open(DAP_AN, encoding='utf-8'))['dapAn']
    gan = {}
    if os.path.exists(GAN):
        gan = json.load(open(GAN, encoding='utf-8'))['gan']
    os.makedirs(RA_DATA, exist_ok=True)

    idx, co_dap, cham_may, tong, canh_bao = [], 0, 0, 0, []
    for b in d['bai']:
        ma = MA_BAI.format(b['so'])
        cau = []
        for c in b['cau']:
            tong += 1
            loi = dap.get(f"{ma}#{c['id']}", '')
            if c['phan'] == 'quiz':
                x = dung_cau_quiz(c, doc_dap_quiz(loi))
                cau.append(x)
                if x.get('answerKey'):
                    cham_may += 1
                    co_dap += 1
                else:
                    canh_bao.append(f'{ma} {c["id"]}: đáp án "{loi[:40]}" không chấm '
                                    f'máy được')
                continue
            if loi:
                co_dap += 1
            else:
                canh_bao.append(f'{ma} {c["id"]}: không có lời chữa')
            cau.append({**c, 'loiChua': loi, 'tuLuan': True})

        g = gan.get(ma) or {'ve': [], 'ten': [], 'canCu': 'khong'}
        bai = {
            'id': ma, 'quyen': 'lop4', 'so': b['so'], 'ten': b['ten'],
            'chuong': b['chuong'], 'tenChuong': b['tenChuong'],
            'dangGoc': b['dangGoc'],
            # lời nối ngược về lớp 3, sách viết sẵn ở đầu mỗi bài
            'hatMam': b.get('hatMam', ''),
            # đường lùi: rỗng thì màn kết bài KHÔNG hiện nút "Học lại bài lớp 3"
            'ganDuoi': {'ve': g['ve'], 'ten': g['ten'], 'canCu': g['canCu'],
                        'lopDuoi': 3},
            'muc': _muc_sach(b['muc']), 'cau': cau,
        }
        with open(os.path.join(RA_DATA, f'DL_KSN4_B{b["so"]:02}.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(bai, f, ensure_ascii=False, indent=1)
        idx.append({'id': ma, 'so': b['so'], 'ten': b['ten'], 'chuong': b['chuong'],
                    'tenChuong': b['tenChuong'],
                    'soCau': sum(1 for c in cau if c['phan'] == 'luyenTap'),
                    'soQuiz': sum(1 for c in cau if c['phan'] == 'quiz'),
                    'coDuongLui': bool(g['ve'])})

    with open(os.path.join(RA_DATA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)

    lui = sum(1 for x in idx if x['coDuongLui'])
    print(f'đã ghi {len(idx)} bài GỐC vào {RA_DATA}')
    print(f'  {tong} câu · có lời chữa {co_dap} ({co_dap * 100 // tong}%) · '
          f'quiz chấm máy {cham_may}/220')
    print(f'  đường lùi về lớp 3: {lui}/{len(idx)} bài có nút')
    for c in canh_bao[:15]:
        print(f'  ⚠ {c}')
    if len(canh_bao) > 15:
        print(f'  ⚠ …và {len(canh_bao) - 15} chỗ nữa')
    return 1 if canh_bao else 0


if __name__ == '__main__':
    raise SystemExit(main())
