# -*- coding: utf-8 -*-
"""
BÀI MẪU — cắt dãy bước phẳng thành các PHẦN của một bài toán trình bày chuẩn.

    python3 tools/bai_mau.py --soat     # in thử, KHÔNG ghi
    python3 tools/bai_mau.py            # ghi vào web/public/content

⚠ PHẢI CHẠY SAU MỌI BỘ DỰNG, cùng lý do với tools/dinh_dang.py: bộ dựng ghi đè
trọn tệp từ bản gốc. Thứ tự đúng: dựng → gắn hình → định dạng → bài mẫu.

── VẤN ĐỀ ──

`workedExample.steps` là một DÃY PHẲNG gồm 1634 dòng `{show: "…"}`. Bé đọc thấy
một cột chữ chạy dài, không phân biệt đâu là tóm tắt, đâu là phân tích, đâu là
bài giải. Trong khi sách VỐN ĐÃ viết đủ các mục ấy — chỉ là chúng nằm lẫn trong
cùng một dãy:

    "Tóm tắt"                         ← tiêu đề mục
    "Tổng: 30 lít; tỉ số 2 : 3."      ← nội dung mục
    "Bài giải:"                       ← tiêu đề mục
    "Tổng số phần bằng nhau là: …"    ← nội dung mục
    "Đáp số: con 3 quả; bố 9 quả."

Đếm được: 44 dòng "Bài giải" ở lớp 4, 34 ở lớp 3, 33 ở lớp 2; 168×3 dòng "Bước n"
ở lớp 5; 150 dòng "Đáp số"; 62 dòng "Thử lại"; 45 "Tóm tắt"; 14 "Sơ đồ".

── CÁCH LÀM: CẮT KHÚC, KHÔNG VIẾT MỚI ──

Không thêm một chữ toán nào. Chỉ gắn cho mỗi bước một nhãn `phan`, rồi giao diện
gom theo nhãn và in tiêu đề. Bước NÀO CHỈ LÀ TIÊU ĐỀ ("Tóm tắt", "Bài giải:")
thì bỏ hẳn — nó đã thành tiêu đề mục, in lại là in hai lần.

Năm phần, đúng thứ tự cô giáo dạy trình bày vào vở:

    tomtat    Tóm tắt      đề cho gì, hỏi gì
    phantich  Phân tích    nghĩ thế nào, chọn công cụ gì (lớp 5: các "Bước n")
    giai      Bài giải     lời văn + phép tính, từng dòng như viết vở
    thulai    Thử lại      kiểm tra đáp số
    dapso     Đáp số       một dòng chốt

Bài nào không có nhãn nào (sách viết liền một mạch) thì để nguyên cả dãy ở phần
`giai` — thà không chia còn hơn chia sai.
"""
import json, os, re, sys, collections

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOI = [('lop2', 'lop2'), ('lop3', 'lop3'), ('lop4', 'lop4'), ('lop5', 'lessons')]

# Dòng CHỈ LÀ TIÊU ĐỀ: khớp trọn, không mang nội dung nào khác.
R_TIEU_DE = {
    'tomtat': re.compile(r'^(Tóm tắt|Đề bài|Đề)\s*[:.]?$', re.I),
    'phantich': re.compile(r'^(Phân tích|Nhận xét|Sơ đồ|Mô hình|Suy nghĩ)\s*[:.]?$', re.I),
    'giai': re.compile(r'^(Bài giải|Trình bày|Lời giải)\s*[:.]?$', re.I),
    'thulai': re.compile(r'^(Thử lại|Kiểm tra)\s*[:.]?$', re.I),
    'dapso': re.compile(r'^(Đáp số|Kết luận)\s*[:.]?$', re.I),
}
# Dòng MỞ ĐẦU một phần nhưng CÓ mang nội dung — giữ dòng, chỉ đổi phần.
R_MO_PHAN = [
    ('dapso', re.compile(r'^(Đáp số|Kết luận)\s*[:.]', re.I)),
    ('thulai', re.compile(r'^(Thử lại|Kiểm tra lại)\s*[:.]', re.I)),
    ('phantich', re.compile(r'^(Bước|Nhịp)\s*\d+\s*[—–-]')),
    ('tomtat', re.compile(r'^(Tóm tắt|Đề bài)\s*[:.]', re.I)),
]
TEN_PHAN = {
    'tomtat': 'TÓM TẮT', 'phantich': 'PHÂN TÍCH', 'giai': 'BÀI GIẢI',
    'thulai': 'THỬ LẠI', 'dapso': 'ĐÁP SỐ', 'ghichu': 'NÓI THÊM',
}
THU_TU = ['tomtat', 'phantich', 'giai', 'thulai', 'dapso', 'ghichu']


def cat_khuc(steps):
    """Dãy bước phẳng → cùng dãy ấy, mỗi bước thêm khoá `phan`.

    Trả (dãy mới, có chia được không). Bỏ những bước chỉ là tiêu đề.
    """
    ra, hien_tai, thay_nhan = [], None, False
    for s in steps:
        t = (s.get('show') or '').strip()

        # 1 · dòng chỉ là tiêu đề → đổi phần, KHÔNG giữ dòng
        xong = False
        for phan, r in R_TIEU_DE.items():
            if r.match(t):
                hien_tai, thay_nhan, xong = phan, True, True
                break
        if xong:
            continue

        # 2 · dòng mở đầu một phần nhưng có nội dung → đổi phần VÀ giữ dòng
        for phan, r in R_MO_PHAN:
            if r.match(t):
                # "Bước n" chỉ mở phần PHÂN TÍCH khi chưa vào bài giải; đã vào
                # bài giải rồi thì các bước ấy chính là dòng giải.
                if phan == 'phantich' and hien_tai in ('giai', 'thulai', 'dapso'):
                    break
                hien_tai, thay_nhan = phan, True
                break

        # ĐÁP SỐ là MỘT dòng chốt, không phải một mục chứa nhiều dòng. Dòng nào
        # đứng sau nó là lời bàn thêm ("Nói thêm của Trí Long: …") — gom vào NÓI
        # THÊM, chứ để chung thì đáp số của bé dài ba dòng và không còn là đáp số.
        if hien_tai == 'dapso' and ra and ra[-1].get('phan') == 'dapso':
            hien_tai = 'ghichu'
        ra.append({**s, 'phan': hien_tai or 'giai'})
    return ra, thay_nhan


def main(chi_soat=False):
    dem = collections.Counter()
    vd = []
    for quyen, thu_muc in NOI:
        d = os.path.join(GOC_KHO, 'web', 'public', 'content', thu_muc)
        for f in sorted(os.listdir(d)):
            if not f.startswith('DL_'):
                continue
            duong = os.path.join(d, f)
            b = json.load(open(duong, encoding='utf-8'))
            we = b.get('workedExample')
            if not we or not we.get('steps'):
                dem[f'{quyen}·không có bài mẫu'] += 1
                continue
            moi, chia = cat_khuc(we['steps'])
            dem[f'{quyen}·bài mẫu'] += 1
            if chia:
                dem[f'{quyen}·CHIA ĐƯỢC phần'] += 1
            else:
                dem[f'{quyen}·để nguyên (sách viết liền)'] += 1
            for s in moi:
                dem['dòng · ' + TEN_PHAN[s['phan']]] += 1
            dem['dòng tiêu đề đã bỏ'] += len(we['steps']) - len(moi)
            we['steps'] = moi
            if chia and len(vd) < 3:
                vd.append((b['id'], moi))
            if not chi_soat:
                with open(duong, 'w', encoding='utf-8') as g:
                    json.dump(b, g, ensure_ascii=False, indent=1)

    for k in sorted(dem):
        print(f'{dem[k]:>5}  {k}')
    for i, ds in vd:
        print(f'\n── {i}')
        for s in ds[:8]:
            print(f'   [{TEN_PHAN[s["phan"]]:<9}] {(s.get("show") or "")[:96]}')
    return dem


if __name__ == '__main__':
    main('--soat' in sys.argv)
