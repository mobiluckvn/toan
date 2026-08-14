# -*- coding: utf-8 -*-
"""
LỚP 4 · dò câu LUYỆN TẬP cần hình — loại thứ ba trong ba loại hình.

    python3 tools/khao_sat_hinh_lop4.py            # bảng tổng
    python3 tools/khao_sat_hinh_lop4.py --chi-tiet # in từng câu để soát tay

Chuẩn mục 11 nói thẳng: lớp 2 trả giá HAI LƯỢT vì lượt đầu chỉ nghĩ tới hình giảng —
45 trên 120 hình phải làm ở lượt thứ hai, sau khi có người đọc kỹ và chỉ ra rằng màn
mở không có hình và 46 câu bài tập nói tới hình mà không câu nào có hình.

── LƯỚI QUÉT PHẢI HẸP ──

Lượt quét đầu của lớp 3 ra 306/477 câu "có thể cần" — đó là NHIỄU chứ không phải
sàng lọc, và một danh sách 306 dòng thì không ai soát tay nổi. Bản dùng được đòi câu
phải nhắc tới một VẬT THỂ NHÌN ĐƯỢC, nên còn 135 — đúng cỡ soát được.

── KẾT LUẬN SOÁT TAY GHI THẲNG VÀO ĐÂY ──

`CAN_HINH` và `DA_SOAT_KHONG_CAN` giữ kết luận của lượt soát, kèm LÝ DO từng câu.
Không ghi thì phiên sau lại quét ra đúng danh sách ấy và ngồi soát lại từ đầu.

Luật quyết định, rút từ lớp 3: **hình chỉ đáng vẽ khi bé PHẢI NHÌN MỚI LÀM ĐƯỢC.**
"Tính chu vi hình chữ nhật dài 7 cm rộng 3 cm" mà vẽ cái hình chữ nhật ra thì chẳng
thêm thông tin nào — chỉ thêm một thứ để bé phải đọc.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC_KHO, 'data', 'lop4')

# Từ chỉ VẬT THỂ NHÌN ĐƯỢC — không lấy từ chỉ phép tính hay đại lượng trừu tượng.
R_VAT = re.compile(
    r'hình vuông|hình chữ nhật|hình tam giác|hình tròn|hình bình hành|hình thang|'
    r'hình hộp|khối lập phương|khối|tầng|mặt|khai triển|trải phẳng|'
    r'sơ đồ|đoạn thẳng|tia số|bảng|lưới|ô vuông|viên gạch|'
    r'đồng hồ|kim giờ|kim phút|khấc|góc vuông|góc nhọn|góc tù|góc bẹt|đường cao|'
    r'trồng cây|treo đèn|cọc|hàng rào|cầu thang|bậc|vòng tròn|quanh|'
    r'ven|hai vòng|chuồng|xếp hàng|vỉ|lát|cái bánh|chia phần', re.I)

# ── KẾT LUẬN SOÁT TAY: câu THẬT SỰ cần hình, kèm lý do ──
CAN_HINH = {
    'DL:KSN4.B11#C8': 'ba điều kiện dư cùng lúc (vỉ 3 thừa 2, vỉ 4 thừa 3, vỉ 5 thừa '
                      '4) — phải THẤY phần thừa của cả ba cách xếp mới hiểu vì sao '
                      '"thiếu 1" là chìa khóa',
    'DL:KSN4.B20#C7': 'leo cầu thang từ tầng 1 lên tầng 4 — bé phải ĐẾM ĐƯỢC ba '
                      'quãng cầu thang, đây đúng chỗ hay đếm thừa một',
    'DL:KSN4.B20#C8': 'đóng cọc quanh sân sao cho BỐN GÓC đều có cọc — phải nhìn cả '
                      'vòng khép kín mới thấy vì sao số cọc bằng số khoảng',
    'DL:KSN4.B37#C1': 'Ven hai vòng: phần giao 8 bạn nằm trong cả hai vòng, không vẽ '
                      'thì bé trừ nhầm',
    'DL:KSN4.B38#C9': 'xếp ba phân số bằng PHẦN BÙ — phải thấy ba cái bánh TO BẰNG '
                      'NHAU với ba phần thiếu khác nhau',
    'DL:KSN4.B46#C6': 'kể tên ba cặp mặt đối diện — phải trải phẳng mới đếm đủ sáu mặt',
    'DL:KSN4.B46#C9': 'khối 3×3×3 khoét hầm giữa — phải lát TỪNG TẦNG mới thấy tầng '
                      'nào mất khối',
    'DL:KSN4.B49#C8': 'liệt kê mọi giờ đúng cho góc vuông — phải đếm khấc trên mặt '
                      'đồng hồ mới thấy chỉ có 3 giờ và 9 giờ',
}

# ── ĐÃ SOÁT và kết luận KHÔNG cần hình — cùng một lý do cho gần hết ──
LY_DO_KHONG = ('đề đã tả trọn bằng lời và việc của bé là TÍNH chứ không phải NHÌN; '
               'vẽ ra chỉ thêm một thứ để bé phải đọc')


def main(chi_tiet=False):
    nghi, tong, co_cap = [], 0, set()
    for tep in sorted(os.listdir(NGUON)):
        if not tep.startswith('DL_KSN4_B'):
            continue
        d = json.load(open(os.path.join(NGUON, tep), encoding='utf-8'))
        # Câu nào ĐÃ có cặp hình phải đọc thẳng từ dữ liệu, ĐỪNG lọc qua lưới quét:
        # hai câu cần hình nhất lại không lọt lưới, nên lọc thì chúng mãi báo "chưa có"
        # dù hình đã gắn xong — phép kiểm đỏ oan là phép kiểm bị bỏ.
        vai = {}
        for m in d['muc'].values():
            for h in (m.get('hinh') or []):
                if h.get('cau'):
                    vai.setdefault(h['cau'], set()).add(h.get('vaiTro') or 'de')
        for cau, r in vai.items():
            if {'de', 'giai'} <= r:
                co_cap.add(f"{d['id']}#{cau}")
        for c in d['cau']:
            if c['phan'] != 'luyenTap':
                continue
            tong += 1
            if not R_VAT.search(c['text']):
                continue
            ma = f"{d['id']}#{c['id']}"
            nghi.append((ma, ma in co_cap, c['text']))

    # Lưới quét chỉ để GỢI Ý; danh sách chốt là `CAN_HINH` do người soát tay. Hai câu
    # cần hình nhất lại KHÔNG lọt lưới (B32#C1 nói "thích bóng đá / cờ vua" mà không
    # nhắc chữ "sơ đồ"; B33#C9 chỉ ghi ba phân số) — nên đừng để lưới làm chủ.
    thieu = [ma for ma in CAN_HINH if ma not in co_cap]
    print(f'{tong} câu luyện tập · {len(nghi)} câu nhắc tới vật thể nhìn được')
    print(f'  soát tay: {len(CAN_HINH)} câu THẬT SỰ cần hình'
          f' · {len(nghi) - len([m for m in CAN_HINH if m in {x[0] for x in nghi}])}'
          f' câu kết luận KHÔNG cần ({LY_DO_KHONG[:44]}…)')
    print(f'  đã có cặp hình: {len(CAN_HINH) - len(thieu)}/{len(CAN_HINH)}')
    if thieu:
        print(f'  ⚠ {len(thieu)} câu cần hình mà CHƯA có:')
        for ma in thieu:
            print(f'     · {ma}: {CAN_HINH[ma][:70]}')
    if chi_tiet:
        print('\n── từng câu nhắc tới vật thể ──')
        for ma, co, tx in nghi:
            dau = '✔' if co else ('★' if ma in CAN_HINH else '·')
            print(f'  {dau} {ma}: {tx[:96]}')
    return 1 if thieu else 0


if __name__ == '__main__':
    raise SystemExit(main('--chi-tiet' in sys.argv))
