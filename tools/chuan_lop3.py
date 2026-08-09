# -*- coding: utf-8 -*-
"""
LỚP 3 · BƯỚC 3 — dựng dữ liệu bài học cho phần mềm.

    python3 tools/chuan_lop3.py

Khác lớp 2 ở chỗ: lớp 2 phải mở lại docx để bóc đáp án, lớp 3 đã bóc xong từ bước
2b (`data/lop3_dapan.json`, 477 lời chữa khớp 1:1). Ở đây chỉ GẮN đáp án vào câu và
đổ ra khuôn bài — không đọc lại sách, không tách lại câu.

Dùng chung `tach_phuong_an` và `dung_cau_quiz` của lớp 2 thay vì chép lại: hai hàm ấy
mang sẵn mấy bài học đắt (giữ chữ cái đầu phương án vì sách chấm theo chữ cái; sách
không ghi đáp án thì để bé tự chấm chứ KHÔNG đoán bừa). Chép lại là chép một bản sẽ
tụt hậu ngay lần sửa sau.

HAI TRƯỜNG LỚP 2 KHÔNG CÓ:

  · `hatMam`   — lời nối ngược về lớp 2 ("Lớp 2 con đã ở trọ ba tòa tháp… hôm nay xây
                 thêm một tầng"). Sách lớp 3 mở bài nào cũng có, hiện ở màn kết bài.
  · `ganLop2`  — đường LÙI: học đuối thì quay về luyện lại bài lớp 2 cùng chủ đề.
                 Đây là việc bác dặn, và là lý do `data/lop3_gan_lop2.json` ra đời
                 trước cả tệp này.

`ganLop2` giữ CẢ DANH SÁCH đích, không phải một đích. Sổ tay dặn "lấy ve[0]" — làm
thế thì bài 4, 16, 18 mất đích thứ hai, mà cả ba đều do SÁCH chỉ đích danh hai bài
(bài 4 "đếm số & đếm trang" gộp đúng hai bài lớp 2 riêng biệt). Dòng `canCu: khong`
thì danh sách rỗng sẵn — chỗ hiện nút cứ theo danh sách rỗng mà ẩn, khỏi phải biết
thêm luật nào.

CHẤM MÁY: cả 170 câu quiz đều chấm được — 102 trắc nghiệm (đề có sẵn A·B·C) và 68
Đúng/Sai, không câu nào lệch. Luyện tập (307 câu) giữ TỰ CHẤM: đáp án phần lớn là
câu chữ ("cùng mặt, khác tháp là khác giá"), ép thành ô nhập số là chấm oan con viết
đúng. Đúng như lớp 2 và Quyển 2 lớp 5 đã học được.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chuan_lop2 import tach_phuong_an, dung_cau_quiz            # noqa: E402

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop3_tho.json')
DAP_AN = os.path.join(GOC_KHO, 'data', 'lop3_dapan.json')
GAN = os.path.join(GOC_KHO, 'data', 'lop3_gan_lop2.json')
RA_DATA = os.path.join(GOC_KHO, 'data', 'lop3')

MA_BAI = 'DL:KSN3.B{:02}'
TEN_CHUONG = {
    1: 'Vương quốc Vạn Số', 2: 'Nhân chia ra khơi', 3: 'Dãy số thám hiểm',
    4: 'Mật thất biểu thức', 5: 'Chuyện toán lời văn 2.0', 6: 'Thám tử cao cấp',
    7: 'Hình học lên tầng', 8: 'Toán trong cuộc sống 2.0',
}
# Đáp án quiz đã bóc thành chuỗi ở bước 2b: "ĐÚNG" · "SAI (chỉ cộng 300)" · "B" ·
# "A." — dấu chấm cuối là của sách, đừng coi là một phần đáp án.
R_QUIZ = re.compile(r'^\s*(ĐÚNG|SAI|[A-D])\b\.?\s*(?:\((.*)\))?\s*\.?\s*$')


def doc_dap_quiz(s):
    """"SAI (chỉ cộng 300)" → ("SAI", "chỉ cộng 300"). Không đọc được thì trả None
    để câu ấy rơi về tự chấm — thà bé tự so còn hơn máy chấm sai."""
    m = R_QUIZ.match(s or '')
    return (m.group(1), (m.group(2) or '').strip()) if m else None


def main():
    d = json.load(open(THO, encoding='utf-8'))
    dap = json.load(open(DAP_AN, encoding='utf-8'))
    gan = json.load(open(GAN, encoding='utf-8'))['gan']
    os.makedirs(RA_DATA, exist_ok=True)

    idx, co_dap, cham_may, tong, canh_bao = [], 0, 0, 0, []
    for b in d['bai']:
        ma = MA_BAI.format(b['so'])
        da = dap.get(ma, {})
        d_lt, d_qz = da.get('luyenTap', {}), da.get('quiz', {})

        cau = []
        for c in b['cau']:
            tong += 1
            khoa = c.get('maSach', c['id'])
            if c['phan'] == 'quiz':
                x = dung_cau_quiz(c, doc_dap_quiz(d_qz.get(khoa)))
                cau.append(x)
                if x.get('answerKey'):
                    cham_may += 1
                    co_dap += 1
                elif khoa in d_qz:
                    canh_bao.append(f'{ma} {khoa}: có đáp án "{d_qz[khoa]}" mà không '
                                    f'chấm máy được — đề không liệt kê nổi phương án?')
                continue
            loi = d_lt.get(khoa, '')
            if loi:
                co_dap += 1
            else:
                canh_bao.append(f'{ma} {khoa}: không có lời chữa')
            cau.append({**c, 'loiChua': loi, 'tuLuan': True})

        g = gan.get(ma) or {'ve': [], 'ten': [], 'canCu': 'khong'}
        bai = {
            'id': ma,
            'quyen': 'lop3',
            'so': b['so'],
            'ten': b['ten'],
            'chuong': b['chuong'],
            'tenChuong': TEN_CHUONG.get(b['chuong'], ''),
            'dangGoc': b['dangGoc'],
            # lời nối ngược về lớp 2, sách viết sẵn ở đầu mỗi bài
            'hatMam': b.get('hatMam', ''),
            # đường lùi: rỗng thì màn kết bài KHÔNG hiện nút "Học lại bài lớp 2"
            'ganLop2': {'ve': g['ve'], 'ten': g['ten'], 'canCu': g['canCu']},
            'muc': b['muc'],
            'cau': cau,
        }
        # CHỈ ghi bản gốc (muc + cau). Bản cho app do bước 5 dựng qua khuôn chung.
        with open(os.path.join(RA_DATA, f'DL_KSN3_B{b["so"]:02}.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(bai, f, ensure_ascii=False, indent=1)
        idx.append({'id': ma, 'so': b['so'], 'ten': b['ten'], 'chuong': b['chuong'],
                    'tenChuong': bai['tenChuong'],
                    # hai con số tách riêng: trang chính ghi "n câu luyện tập", gộp cả
                    # quiz vào là nói sai với bé — quiz là phần tự kiểm cuối bài
                    'soCau': sum(1 for c in cau if c['phan'] == 'luyenTap'),
                    'soQuiz': sum(1 for c in cau if c['phan'] == 'quiz'),
                    'coDuongLui': bool(g['ve'])})

    with open(os.path.join(RA_DATA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)

    lui = sum(1 for x in idx if x['coDuongLui'])
    print(f'đã ghi {len(idx)} bài GỐC vào {RA_DATA}')
    print(f'  {tong} câu · có lời chữa {co_dap} ({co_dap * 100 // tong}%) · '
          f'chấm máy {cham_may}')
    print(f'  đường lùi về lớp 2: {lui}/{len(idx)} bài có nút, '
          f'{len(idx) - lui} bài sách không có bài tương ứng')
    for c in canh_bao[:20]:
        print(f'  ⚠ {c}')
    if len(canh_bao) > 20:
        print(f'  ⚠ …và {len(canh_bao) - 20} chỗ nữa')
    return 1 if canh_bao else 0


if __name__ == '__main__':
    raise SystemExit(main())
