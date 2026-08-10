# -*- coding: utf-8 -*-
"""
BẢN MÔ TẢ HÌNH LỚP 4 — nguồn sự thật, sinh ra `data/lop4_hinh.json`.

    python3 tools/mota_hinh_lop4.py

Viết bằng Python chứ không viết thẳng JSON, vì mỗi hình cần một dòng LÝ DO đi kèm,
mà JSON thì không đặt được chú thích. Bộ vẽ (`ve_hinh_lop4.py`) đọc tệp JSON sinh ra.

HAI LUẬT PHẢI GIỮ Ở ĐÂY (chuẩn mục 6):

1. **Hình màn mở là bản ĐỀ** — bỏ hết dấu vết đáp án: không `note` chốt kết quả,
   không nhãn có dấu `=`, không tên loại góc, không tô sẵn phần phải tìm. Ảnh gốc
   của sách vi phạm đúng chỗ này (hình bài 1 in sẵn *"đọc theo lớp: hai mươi bốn
   nghìn | ba trăm năm mươi tám"*), nên vẽ lại chứ không dùng lại.
2. **Hình giảng đi kèm một BƯỚC cụ thể** (`neoBuoc`), không rải đều mọi bước —
   bước nào chỉ diễn giải bằng lời thì thêm hình là thêm thứ để bé phải đọc.
"""
import json, os

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC_KHO, 'data', 'lop4_hinh.json')
MA = 'DL:KSN4.B{:02}'

H = []


def mo(so, ma, arch, params, caption, goc=''):
    """Hình MÀN MỞ — bản đề, gắn vào mục ② nên khuôn chung đặt nó ở màn `hook`."""
    H.append({'id': ma, 'arch': arch, 'params': params, 'caption': caption,
              'bai': MA.format(so), 'muc': 'chuyenMoBai', 'goc': goc or f'B{so} ②'})


def giang(so, ma, arch, params, caption, buoc, goc=''):
    """Hình GIẢNG — neo theo thứ tự bước trong mục ④."""
    H.append({'id': ma, 'arch': arch, 'params': params, 'caption': caption,
              'bai': MA.format(so), 'muc': 'khamPha', 'neoBuoc': buoc,
              'goc': goc or f'B{so} ④ bước {buoc}'})


def bt(so, ma, cau, arch, params, caption, vai=None):
    """Hình BÀI TẬP — cặp `item:CX` (đề) và `item:CX:giai` (lời giải)."""
    H.append({'id': ma, 'arch': arch, 'params': params, 'caption': caption,
              'bai': MA.format(so), 'muc': 'luyenTap', 'neoCau': cau,
              'vaiTro': vai, 'goc': f'B{so} ⑧ {cau}'})


# ═══════════ CHƯƠNG 1 · ĐẠI CÔNG TRƯỜNG LỚP TRIỆU ═══════════

mo(1, 'L4H_B01_MO', 'cau_truc_so', {
    'title': 'BẢNG TIN PHƯỜNG — ĐỌC SỐ NÀY THẾ NÀO?',
    'kieu': 'nha',
    'phong': [{'ten': 'CHỤC NGHÌN', 'so': 2, 'mau': 'teal'},
              {'ten': 'NGHÌN', 'so': 4, 'mau': 'teal'},
              {'ten': 'TRĂM', 'so': 3, 'mau': 'gold'},
              {'ten': 'CHỤC', 'so': 5, 'mau': 'gold'},
              {'ten': 'ĐƠN VỊ', 'so': 8, 'mau': 'gold'}],
}, 'Số 24 358 thả vào bảng hàng - lớp, mỗi chữ số một cột.')
giang(1, 'L4H_B01_G2', 'cau_truc_so', {
    'title': 'ĐỌC THEO LỚP — mỗi lớp ba hàng',
    'kieu': 'nha',
    'phong': [{'ten': 'TRIỆU', 'so': 1, 'mau': 'do', 'duoi': 'lớp triệu'},
              {'ten': 'TRĂM NGHÌN', 'so': 7, 'mau': 'teal', 'duoi': 'lớp nghìn'},
              {'ten': 'CHỤC NGHÌN', 'so': 4, 'mau': 'teal', 'duoi': 'lớp nghìn'},
              {'ten': 'NGHÌN', 'so': 5, 'mau': 'teal', 'duoi': 'lớp nghìn'},
              {'ten': 'TRĂM', 'so': 2, 'mau': 'gold', 'duoi': 'lớp đơn vị'},
              {'ten': 'CHỤC', 'so': 3, 'mau': 'gold', 'duoi': 'lớp đơn vị'},
              {'ten': 'ĐƠN VỊ', 'so': 0, 'mau': 'gold', 'duoi': 'lớp đơn vị'}],
    'note': 'Cứ ba hàng gom thành một lớp: triệu | nghìn | đơn vị.',
}, 'Số 1 745 230 chia ba lớp.', 2)
giang(1, 'L4H_B01_G4', 'bang_luoi', {
    'title': 'BẢNG LIỆT KÊ — không đoán mò',
    'cot': ['cặp chữ số', 'tổng', 'hiệu'],
    'hang': [['9 - 0', '9', '9'], ['8 - 1', '9', '7'], ['7 - 2', '9', '5'],
             ['6 - 3', '9', '3'], ['5 - 4', '9', '1']],
    'to': [[3, 2]],
    'note': 'Liệt kê đủ theo TỔNG rồi mới soi cột HIỆU.',
}, 'Bảng liệt kê mọi cặp có tổng 9, soi tiếp cột hiệu.', 4)

mo(2, 'L4H_B02_MO', 'doan_thang', {
    'title': 'TEM GIÁ IN THÊM MỘT SỐ 0 — GIÁ ĐỘI LÊN BAO NHIÊU?',
    'thanh': [{'ten': 'giá đúng', 'phan': [{'dai': 1, 'nhan': '3 500', 'mau': 'teal'}]},
              {'ten': 'giá trên tem', 'phan': [{'dai': 10, 'nhan': '35 000', 'mau': 'gold'}]}],
}, 'Giá đúng một phần, giá trên tem mười phần.')
giang(2, 'L4H_B02_G1', 'doan_thang', {
    'title': 'SƠ ĐỒ 10 PHẦN — thêm 0 bên phải',
    'thanh': [{'ten': 'số cũ', 'phan': [{'dai': 1, 'nhan': '1 phần', 'mau': 'teal'}]},
              {'ten': 'số mới', 'phan': [{'dai': 10, 'nhan': '10 phần', 'mau': 'gold'}]}],
    'note': 'Phần tăng thêm là 9 phần — đúng 9 lần số cũ.',
}, 'Số mới 10 phần, phần hơn là 9 phần.', 1)

mo(3, 'L4H_B03_MO', 'may_bien_doi', {
    # Khoản hụt 315 000 là DỮ KIỆN ĐỀ CHO nên phải hiện; còn số đúng (350 000) là
    # thứ bé phải tìm nên để dấu hỏi — bản đề giữ số đo cho sẵn, bỏ dấu vết đáp án.
    'title': 'SỔ QUỸ HỤT ĐÚNG 315 000 ĐỒNG — CHỮ SỐ 0 NÀO ĐÃ RƠI?',
    'rows': [{'mau': 'teal', 'o': [{'t': '?', 'mau': 'do'},
                                   {'may': 'XÓA 0 CUỐI'}, {'t': '?', 'mau': 'do'}]}],
}, 'Ghi thiếu một chữ số 0 tận cùng thì sổ hụt bao nhiêu.')
giang(3, 'L4H_B03_G1', 'may_bien_doi', {
    'title': 'THANG MÁY ×10 — lên và xuống',
    'rows': [{'mau': 'teal', 'o': [{'t': '38', 'mau': 'gold'}, {'may': '× 10'},
                                   {'t': '380', 'mau': 'gold'}]},
             {'mau': 'do', 'nguoc': True,
              'o': [{'t': '38', 'mau': 'gold'}, {'may': ': 10'},
                    {'t': '380', 'mau': 'gold'}]}],
    'note': 'Thêm 0 là đi lên một tầng, xóa 0 là đi xuống một tầng.',
}, 'Thang máy ×10 chạy hai chiều.', 1)

mo(4, 'L4H_B04_MO', 'day_o', {
    'title': 'GÕ NGƯỢC 72 THÀNH 27 — THIẾU BAO NHIÊU?',
    'hang': [{'nhan': 'giá đúng', 'o': [{'t': '7', 'mau': 'teal'}, {'t': '2', 'mau': 'teal'}]},
             {'nhan': 'màn hình', 'o': [{'t': '2', 'mau': 'gold'}, {'t': '7', 'mau': 'gold'}]}],
}, 'Hai chữ số đổi chỗ cho nhau.')
giang(4, 'L4H_B04_G2', 'day_o', {
    'title': 'ĐỊNH LUẬT HỌ 9 — hiệu luôn chia hết cho 9',
    'hang': [{'nhan': '82 − 28', 'o': [{'t': '8', 'mau': 'teal'}, {'t': '2', 'mau': 'teal'},
                                       {'t': '−', 'mo': True},
                                       {'t': '2', 'mau': 'gold'}, {'t': '8', 'mau': 'gold'}]}],
    'note': 'ab − ba = 9 × (a − b): 82 − 28 = 9 × 6 = 54.',
}, 'Hiệu của số và số viết ngược luôn là 9 lần hiệu hai chữ số.', 2)

# ═══════════ CHƯƠNG 2 · CỖ MÁY BỐN PHÉP TÍNH ═══════════

mo(5, 'L4H_B05_MO', 'hang_hop', {
    'title': 'HAI KỆ MÌ CÙNG GIÁ — TÍNH KIỂU NÀO NHANH HƠN?',
    'hop': [{'ten': 'Kệ mì gà', 'dong': ['38 hộp', '4 nghìn/hộp'], 'mau': 'teal'},
            {'ten': 'Kệ mì tôm', 'dong': ['62 hộp', '4 nghìn/hộp'], 'mau': 'gold'}],
}, 'Hai kệ khác số hộp nhưng CÙNG giá một hộp.')
giang(5, 'L4H_B05_G1', 'hang_hop', {
    'title': 'GỘP KỆ — đặt thừa số chung',
    'hop': [{'ten': 'Tính từng kệ', 'dong': ['4 × 38 = 152', '4 × 62 = 248',
                                             'cộng lại 400'], 'mau': 'gold'},
            {'ten': 'Gộp kệ trước', 'dong': ['4 × (38 + 62)', '= 4 × 100',
                                             '= 400'], 'mau': 'teal'}],
    'ket': 'a × b + a × c = a × (b + c) — gộp trước, nhân sau.',
}, 'Hai cách cùng ra 400, nhưng gộp trước thì nhẩm được.', 1)

mo(6, 'L4H_B06_MO', 'bap_benh', {
    'title': 'HÓA ĐƠN DÍNH MỰC — MỖI LOẠI MẤY GÓI?',
    'trai': {'t': 'X × 3 + X × 2', 'mau': 'teal'},
    'phai': {'t': '45', 'mau': 'gold'},
    'nghieng': 'can',
}, 'Hai vế cân nhau: tiền kẹo cộng tiền bánh bằng 45 nghìn.')
giang(6, 'L4H_B06_G1', 'may_bien_doi', {
    'title': 'BÓC NGOẶC NHƯ BÓC HÀNH — đi lùi từng lớp',
    'rows': [{'mau': 'do', 'nguoc': True,
              'o': [{'t': 'X', 'mau': 'gold'}, {'may': '× 5'},
                    {'t': '45', 'mau': 'gold'}]}],
    'note': 'X × 3 + X × 2 = X × 5 = 45 → X = 45 : 5.',
}, 'Gộp hai vế về một phép nhân rồi đi lùi.', 1)

mo(7, 'L4H_B07_MO', 'bang_luoi', {
    'title': 'ĐÁNH SỐ 250 TRANG — CẦN BAO NHIÊU MIẾNG DECAL?',
    'cot': ['nhóm trang', 'mấy số', 'mấy chữ số'],
    'hang': [['1 → 9', '9', '1'], ['10 → 99', '90', '2'], ['100 → 250', '151', '3']],
}, 'Ba nhóm trang, mỗi nhóm số chữ số khác nhau.')
giang(7, 'L4H_B07_G1', 'tia_so', {
    'title': 'ĐẾM SỐ TRONG MỘT ĐOẠN',
    'moc': [{'so': 10, 'danh': True}, {'so': 20}, {'so': 30}, {'so': 40, 'danh': True}],
    'nhan': '+10',
    'note': 'Số số hạng = (cuối − đầu) : khoảng cách + 1.',
}, 'Đếm mốc trên tia số, không đếm khoảng.', 1)

mo(8, 'L4H_B08_MO', 'bang_luoi', {
    'title': 'KHÓA 3 VÒNG SỐ, KIÊNG SỐ 0 — CÓ MẤY MẬT KHẨU?',
    'cot': ['vòng 1', 'vòng 2', 'vòng 3'],
    'hang': [['1 → 9', '1 → 9', '1 → 9'], ['9 cách', '9 cách', '9 cách']],
}, 'Ba vòng số, mỗi vòng chọn được mấy chữ số.')
giang(8, 'L4H_B08_G1', 'hang_hop', {
    'title': 'PHẦN BÙ — đếm cái KHÔNG rồi trừ đi',
    'hop': [{'ten': 'Tất cả số 3 chữ số', 'dong': ['900 số'], 'mau': 'gold'},
            {'ten': 'Số CÓ chữ số 0', 'dong': ['900 − 648'], 'mau': 'do'},
            {'ten': 'Số KHÔNG có 0', 'dong': ['9 × 9 × 9', '= 648'], 'mau': 'teal'}],
}, 'Khó đếm cái CÓ thì đếm cái KHÔNG rồi lấy tất cả trừ đi.', 1)

# ═══════════ CHƯƠNG 3 · MẬT MÃ CHIA HẾT ═══════════

mo(9, 'L4H_B09_MO', 'day_o', {
    # Bản đầu vẽ 12 chấm "hàng đôi" — mà đề nói 234 em. Bé không đếm nổi 234 chấm,
    # và 12 thì chẳng dính gì tới đề: hình có vẽ, có nhãn, nhưng KHÔNG nói về bài
    # toán đang hỏi. Bài này dạy "chỉ cần nhìn CHỮ SỐ TẬN CÙNG", nên hình phải là
    # chính con số ấy với cái đuôi được chỉ ra.
    'title': '234 EM RƯỚC ĐÈN — XẾP HÀNG ĐÔI CÓ VỪA KHÔNG?',
    'hang': [{'nhan': 'số em', 'o': [{'t': '2', 'mo': True}, {'t': '3', 'mo': True},
                                     {'t': '4', 'mau': 'teal', 'duoi': 'chữ số tận cùng'}]}],
}, 'Số 234 với chữ số tận cùng được chỉ ra.')

mo(10, 'L4H_B10_MO', 'day_o', {
    'title': '348 CHIẾC BÁNH — ĐÓNG HỘP 3 CÓ VỪA KHÔNG?',
    'hang': [{'nhan': 'số bánh', 'o': [{'t': '3', 'mau': 'teal'},
                                       {'t': '4', 'mau': 'teal'}, {'t': '8', 'mau': 'teal'}]}],
}, 'Đuôi số 8 không cho biết gì về phép chia cho 3.')
giang(10, 'L4H_B10_G1', 'day_o', {
    'title': 'CỘNG TẤT CẢ CHỮ SỐ LẠI',
    'hang': [{'nhan': '348', 'o': [{'t': '3', 'mau': 'gold'}, {'t': '+', 'mo': True},
                                   {'t': '4', 'mau': 'gold'}, {'t': '+', 'mo': True},
                                   {'t': '8', 'mau': 'gold'}, {'t': '=', 'mo': True},
                                   {'t': '15', 'mau': 'teal'}]}],
    'note': '15 chia hết cho 3 nên 348 chia hết cho 3.',
}, 'Dấu hiệu 3 và 9 xem TỔNG các chữ số, không xem đuôi.', 1)

mo(11, 'L4H_B11_MO', 'hang_hop', {
    # Bản đầu vẽ 8 chấm + 3 chấm thừa, tức 11 chiếc — trong khi đề nói chồng ghế có
    # TỪ 30 ĐẾN 50 chiếc. Hình đá nhau với đề ngay dòng đầu bé đọc. Số ghế đúng là
    # thứ bé phải TÌM, nên bản đề chỉ được bày ba dữ kiện, không bày một con số nào.
    'title': 'CHỒNG GHẾ CÓ MẤY CÁI?',
    'hop': [{'ten': 'Xếp hàng 4', 'dong': ['thừa 3 cái'], 'mau': 'gold'},
            {'ten': 'Xếp hàng 5', 'dong': ['thừa 4 cái'], 'mau': 'gold'},
            {'ten': 'Biết thêm', 'dong': ['có từ 30', 'đến 50 cái'], 'mau': 'teal'}],
}, 'Ba dữ kiện của đề, chưa có con số nào là đáp án.')
giang(11, 'L4H_B11_G2', 'hang_hop', {
    'title': 'NHÌN PHẦN THIẾU THAY VÌ PHẦN THỪA',
    'hop': [{'ten': 'Hàng 4 thừa 3', 'dong': ['còn THIẾU 1 cái', 'là tròn hàng'],
             'mau': 'gold'},
            {'ten': 'Hàng 5 thừa 4', 'dong': ['còn THIẾU 1 cái', 'là tròn hàng'],
             'mau': 'gold'},
            {'ten': 'Vậy', 'dong': ['thêm 1 cái thì', 'chia hết cả 4 lẫn 5'],
             'mau': 'teal'}],
}, 'Hai manh mối dư cùng lúc — đổi sang phần thiếu là hết rối.', 2)

mo(12, 'L4H_B12_MO', 'day_o', {
    'title': 'TÍCH 1 × 2 × … × 9 TẬN CÙNG LÀ SỐ MẤY?',
    # KHÔNG tô đỏ 5 và 6: bài hỏi "tận cùng là số mấy", mà tô đỏ đúng cặp 2 × 5 cho
    # đuôi 0 là chỉ thẳng lời giải ngay trên bản ĐỀ.
    'hang': [{'nhan': 'dãy thừa số', 'o': [{'t': '1'}, {'t': '2'}, {'t': '3'}, {'t': '4'},
                                           {'t': '5'}, {'t': '6'},
                                           {'t': '7'}, {'t': '8'}, {'t': '9'}]}],
}, 'Cả dãy thừa số — chưa nhân, chỉ nhìn đuôi.')

# ═══════════ CHƯƠNG 4 · NHÀ GA DÃY SỐ ═══════════

mo(13, 'L4H_B13_MO', 'tia_so', {
    'title': 'RẠP 18 HÀNG, MỖI HÀNG 8 GHẾ — GHẾ ĐẦU HÀNG 15 VÀ VÉ SỐ 113 Ở ĐÂU?',
    'moc': [{'so': 1, 'danh': True}, {'so': 9}, {'so': 17}, {'so': 25}],
    'nhan': '+8',
}, 'Ghế đầu mỗi hàng cách nhau đúng 8 — bốn hàng đầu làm mẫu.')
giang(13, 'L4H_B13_G1', 'tia_so', {
    'title': 'BỘ TỨ CỦA DÃY CÁCH ĐỀU',
    'moc': [{'so': 5, 'danh': True}, {'so': 10}, {'so': 15}, {'so': 20}],
    'nhan': '+5',
    'note': 'Số hạng thứ n = số đầu + khoảng cách × (n − 1).',
}, 'Dãy cách đều: số đầu, khoảng cách, số hạng, tổng.', 1)

mo(14, 'L4H_B14_MO', 'day_o', {
    'title': 'MỖI TUẦN BỎ HƠN TUẦN TRƯỚC 1 NGHÌN — TUẦN 10 ĐƯỢC MẤY, KHI NÀO ĐỦ 120 NGHÌN?',
    'hang': [{'nhan': 'tuần', 'o': [{'t': '1'}, {'t': '2'}, {'t': '3'}, {'t': '4'},
                                    {'t': '5'}]},
             {'nhan': 'bỏ heo', 'o': [{'t': '1', 'mau': 'teal'}, {'t': '2', 'mau': 'teal'},
                                      {'t': '3', 'mau': 'teal'}, {'t': '4', 'mau': 'teal'},
                                      {'t': '?', 'mau': 'do'}],
              'cung': [{'tu': 0, 'den': 1, 'nhan': '+1'}, {'tu': 1, 'den': 2, 'nhan': '+1'}]}],
}, 'Hai tầng: tầng trên là tuần, tầng dưới là số tiền.')
giang(14, 'L4H_B14_G1', 'day_o', {
    'title': 'DÃY HAI TẦNG — nhìn HIỆU của hiệu',
    'hang': [{'nhan': 'dãy', 'o': [{'t': '1', 'mau': 'teal'}, {'t': '2', 'mau': 'teal'},
                                   {'t': '4', 'mau': 'teal'}, {'t': '7', 'mau': 'teal'},
                                   {'t': '11', 'mau': 'teal'}],
              'cung': [{'tu': 0, 'den': 1, 'nhan': '+1'}, {'tu': 1, 'den': 2, 'nhan': '+2'},
                       {'tu': 2, 'den': 3, 'nhan': '+3'}, {'tu': 3, 'den': 4, 'nhan': '+4'}]}],
    'note': 'Tầng hiệu lại là một dãy cách đều: 1, 2, 3, 4…',
}, 'Dãy hai tầng: hiệu của dãy mới là dãy cách đều.', 1)

mo(15, 'L4H_B15_MO', 'hang_cay', {
    # Số đo của sân là DỮ KIỆN ĐỀ CHO nên được phép hiện, nhưng phải nằm ở TIÊU ĐỀ
    # chứ không nằm ở dòng chốt: dòng chốt của bản đề phải trống trơn (chuẩn mục 6).
    'title': 'SÂN 30 M × 20 M, TREO ĐÈN QUANH SÂN CỨ 5 MÉT MỘT CHIẾC',
    'so_cay': 6, 'khoang': '5 m',
}, 'Treo quanh một vòng khép kín — đếm cây và đếm khoảng.')
giang(15, 'L4H_B15_G1', 'hang_cay', {
    'title': 'BA THẾ TRẬN TRỒNG CÂY',
    'so_cay': 5, 'khoang': '5 m',
    'note': 'Đường thẳng trồng hai đầu: số cây = số khoảng + 1.',
}, 'Đường thẳng trồng cả hai đầu — cây nhiều hơn khoảng 1.', 1)

# ═══════════ CHƯƠNG 5 · TRUNG BÌNH CỘNG ═══════════

mo(16, 'L4H_B16_MO', 'cot_san_bang', {
    'title': 'BA TRẬN GHI 2 - 5 - 2 BÀN — SAN ĐỀU THÌ MỖI TRẬN MẤY BÀN?',
    'cot': [{'ten': 'trận 1', 'cao': 2}, {'ten': 'trận 2', 'cao': 5},
            {'ten': 'trận 3', 'cao': 2}],
    'muc': 3, 'nhanMuc': 'mức san đều',
}, 'Ba cột cao thấp khác nhau, vạch san đều cắt ngang.')
giang(16, 'L4H_B16_G1', 'cot_san_bang', {
    'title': 'SAN CHO ĐỀU — cột cao bù cho cột thấp',
    'cot': [{'ten': 'trận 1', 'cao': 2}, {'ten': 'trận 2', 'cao': 5},
            {'ten': 'trận 3', 'cao': 2}],
    'muc': 3, 'hieuSo': True,
    'note': 'Tổng = trung bình cộng × số số hạng — đó là cây cầu TỔNG.',
}, 'Phần vượt của trận 2 bù đúng phần hụt của hai trận kia.', 1)

mo(17, 'L4H_B17_MO', 'cot_san_bang', {
    'title': 'AN CAO HƠN MỨC TRUNG BÌNH 4 CM, BÌNH THẤP HƠN 2 CM',
    'cot': [{'ten': 'An', 'cao': 134}, {'ten': 'Bình', 'cao': 128},
            {'ten': 'Cường', 'cao': 128}],
    'muc': 130, 'nhanMuc': 'trung bình', 'hieuSo': True,
}, 'Ba cột quanh vạch trung bình, phần vượt và phần hụt.')

mo(18, 'L4H_B18_MO', 'cot_san_bang', {
    'title': 'BẠN MỚI GÓP 15 NGHÌN THÌ MỨC TRUNG BÌNH LUNG LAY THẾ NÀO? MUỐN MỨC 11 THÌ SAO?',
    'cot': [{'ten': 'bạn 1', 'cao': 10}, {'ten': 'bạn 2', 'cao': 10},
            {'ten': 'bạn 3', 'cao': 10}, {'ten': 'bạn 4', 'cao': 10},
            {'ten': 'bạn mới', 'cao': 15}],
    'muc': 10, 'nhanMuc': 'mức cũ',
}, 'Bốn bạn đã góp đều 10; cột bạn mới cao 15 — vạch trung bình sẽ nhích lên.')

# ═══════════ CHƯƠNG 6 · CÁN CÂN TỔNG - HIỆU ═══════════

mo(19, 'L4H_B19_MO', 'doan_thang', {
    'title': 'HAI ANH EM CÓ 500 NGHÌN, ANH HƠN EM 60 NGHÌN',
    'thanh': [{'ten': 'em', 'phan': [{'dai': 4.4, 'nhan': '?', 'mau': 'teal'}]},
              {'ten': 'anh', 'phan': [{'dai': 4.4, 'nhan': '?', 'mau': 'teal'},
                                      {'dai': 1.2, 'nhan': '60', 'mau': 'gold'}]}],
}, 'Hai thanh, thanh anh dài hơn đúng phần 60 nghìn.')
giang(19, 'L4H_B19_G2', 'doan_thang', {
    'title': 'CẮT PHẦN HƠN — hai thanh bằng nhau',
    'thanh': [{'ten': 'em', 'phan': [{'dai': 4.4, 'nhan': '220', 'mau': 'teal'}]},
              {'ten': 'anh', 'phan': [{'dai': 4.4, 'nhan': '220', 'mau': 'teal'},
                                      {'dai': 1.2, 'nhan': '60', 'mau': 'gold'}]}],
    'note': 'Bớt 60 rồi chia đôi: (500 − 60) : 2 = 220 — đó là phần em.',
}, 'Bớt phần hơn rồi chia đôi ra số bé.', 2)

mo(20, 'L4H_B20_MO', 'hinh_chu_vi', {
    'title': 'VƯỜN CÓ CHU VI 18 M, DÀI HƠN RỘNG 3 M',
    'hinh': [{'loai': 'chunhat', 'canh': ['?', '?', '?', '?'], 'ten': 'mảnh vườn',
              'mau': 'teal'}],
}, 'Mảnh vườn chữ nhật, chỉ biết chu vi và phần hơn.')
giang(20, 'L4H_B20_G1', 'hang_hop', {
    'title': 'TỔNG TRỐN Ở ĐÂU?',
    'hop': [{'ten': 'Trốn trong CHU VI', 'dong': ['nửa chu vi', '= dài + rộng'],
             'mau': 'gold'},
            {'ten': 'Trốn trong TBC', 'dong': ['tổng = TBC ×', 'số số hạng'],
             'mau': 'teal'}],
}, 'Hai chỗ tổng hay nấp: chu vi và trung bình cộng.', 1)

mo(21, 'L4H_B21_MO', 'doan_thang', {
    'title': 'CHUYỂN 5 CUỐN TỪ KỆ A SANG KỆ B THÌ BẰNG NHAU',
    'thanh': [{'ten': 'kệ A', 'phan': [{'dai': 6, 'nhan': '?', 'mau': 'teal'}]},
              {'ten': 'kệ B', 'phan': [{'dai': 4, 'nhan': '?', 'mau': 'gold'}]}],
}, 'Hai kệ chưa bằng nhau, chưa biết hiệu là bao nhiêu.')
giang(21, 'L4H_B21_G1', 'doan_thang', {
    'title': 'CHUYỂN k THÌ HIỆU ĐỔI 2k',
    'thanh': [{'ten': 'kệ A', 'phan': [{'dai': 5, 'nhan': '', 'mau': 'teal'},
                                       {'dai': 1, 'nhan': '5', 'mau': 'do'}]},
              {'ten': 'kệ B', 'phan': [{'dai': 5, 'nhan': '', 'mau': 'gold'}]}],
    'note': 'Chuyển 5 thì bên này bớt 5, bên kia thêm 5 — hiệu là 10, không phải 5.',
}, 'Chuyển k đơn vị làm hiệu đổi 2k — cú lừa danh tiếng nhất.', 1)

mo(22, 'L4H_B22_MO', 'doan_thang', {
    'title': 'BA BẠN CÓ 100 VIÊN BI — AN HƠN BÌNH 5, BÌNH HƠN CƯỜNG 10',
    'thanh': [{'ten': 'Cường', 'phan': [{'dai': 4, 'nhan': '?', 'mau': 'teal'}]},
              {'ten': 'Bình', 'phan': [{'dai': 4, 'nhan': '?', 'mau': 'teal'},
                                       {'dai': 1.4, 'nhan': '10', 'mau': 'gold'}]},
              {'ten': 'An', 'phan': [{'dai': 4, 'nhan': '?', 'mau': 'teal'},
                                     {'dai': 1.4, 'nhan': '10', 'mau': 'gold'},
                                     {'dai': 0.7, 'nhan': '5', 'mau': 'do'}]}],
}, 'Ba đoạn thẳng, quy về bạn ít bi nhất.')

# ═══════════ CHƯƠNG 7 · CHIA PHẦN THEO TỈ ═══════════

mo(23, 'L4H_B23_MO', 'doan_thang', {
    'title': 'BÌNH 30 LÍT — CỨ 2 PHẦN CỐT CAM THÌ 3 PHẦN NƯỚC LỌC',
    'thanh': [{'ten': 'cốt cam', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'gold'},
                                          {'dai': 2, 'nhan': '', 'mau': 'gold'}]},
              {'ten': 'nước lọc', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'teal'},
                                           {'dai': 2, 'nhan': '', 'mau': 'teal'},
                                           {'dai': 2, 'nhan': '', 'mau': 'teal'}]}],
}, 'Hai phần và ba phần, mỗi ô là một phần bằng nhau.')
giang(23, 'L4H_B23_G2', 'doan_thang', {
    'title': 'MỘT PHẦN ĐÁNG GIÁ BAO NHIÊU?',
    'thanh': [{'ten': 'cốt cam', 'phan': [{'dai': 2, 'nhan': '6', 'mau': 'gold'},
                                          {'dai': 2, 'nhan': '6', 'mau': 'gold'}]},
              {'ten': 'nước lọc', 'phan': [{'dai': 2, 'nhan': '6', 'mau': 'teal'},
                                           {'dai': 2, 'nhan': '6', 'mau': 'teal'},
                                           {'dai': 2, 'nhan': '6', 'mau': 'teal'}]}],
    'note': 'Cả bình 5 phần: 30 : 5 = 6 lít mỗi phần.',
}, 'Chia tổng cho TỔNG SỐ PHẦN ra giá trị một phần.', 2)

mo(24, 'L4H_B24_MO', 'doan_thang', {
    'title': 'KHAY 40 CHIẾC — BÁNH NƯỚNG GẤP RƯỠI BÁNH DẺO',
    'thanh': [{'ten': 'bánh dẻo', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'teal'},
                                           {'dai': 2, 'nhan': '', 'mau': 'teal'}]},
              {'ten': 'bánh nướng', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'gold'},
                                             {'dai': 2, 'nhan': '', 'mau': 'gold'},
                                             {'dai': 2, 'nhan': '', 'mau': 'gold'}]}],
}, '"Gấp rưỡi" đã được dịch thành 3 phần so với 2 phần.')

mo(25, 'L4H_B25_MO', 'doan_thang', {
    'title': 'TRUYỆN GẤP 3 LẦN THƠ VÀ NHIỀU HƠN THƠ 24 CUỐN',
    'thanh': [{'ten': 'thơ', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'teal'}]},
              {'ten': 'truyện', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'gold'},
                                         {'dai': 2, 'nhan': '', 'mau': 'gold'},
                                         {'dai': 2, 'nhan': '', 'mau': 'gold'}]}],
}, 'Ba phần so một phần — phần chênh là chìa khóa.')
giang(25, 'L4H_B25_G1', 'doan_thang', {
    'title': 'CHIA CHO HIỆU SỐ PHẦN',
    'thanh': [{'ten': 'thơ', 'phan': [{'dai': 2, 'nhan': '12', 'mau': 'teal'}]},
              {'ten': 'truyện', 'phan': [{'dai': 2, 'nhan': '12', 'mau': 'gold'},
                                         {'dai': 2, 'nhan': '12', 'mau': 'gold'},
                                         {'dai': 2, 'nhan': '12', 'mau': 'gold'}]}],
    'note': 'Phần chênh là 2 phần: 24 : 2 = 12 cuốn mỗi phần.',
}, 'Tổng - tỉ chia cho TỔNG số phần, hiệu - tỉ chia cho HIỆU số phần.', 1)

mo(26, 'L4H_B26_MO', 'doan_thang', {
    'title': 'BA ỐNG HEO ĐƯỢC 90 NGHÌN — ANH HAI GẤP ĐÔI, ANH CẢ GẤP BA EM',
    'thanh': [{'ten': 'em út', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'teal'}]},
              {'ten': 'anh hai', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'gold'},
                                          {'dai': 2, 'nhan': '', 'mau': 'gold'}]},
              {'ten': 'anh cả', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'navy'},
                                         {'dai': 2, 'nhan': '', 'mau': 'navy'},
                                         {'dai': 2, 'nhan': '', 'mau': 'navy'}]}],
}, 'Ba hàng trên cùng một sơ đồ phần.')

# ═══════════ CHƯƠNG 8 · BÀI TOÁN CÓ CỐT TRUYỆN ═══════════

mo(27, 'L4H_B27_MO', 'doan_thang', {
    'title': 'MẸ 36 TUỔI, CON 12 — TRƯỚC ĐÂY MẤY NĂM MẸ GẤP 5 LẦN CON?',
    'thanh': [{'ten': 'con nay', 'phan': [{'dai': 2, 'nhan': '12', 'mau': 'teal'}]},
              {'ten': 'mẹ nay', 'phan': [{'dai': 6, 'nhan': '36', 'mau': 'gold'}]}],
}, 'Tuổi hiện nay — hiệu 24 năm sẽ không bao giờ đổi.')
giang(27, 'L4H_B27_G1', 'doan_thang', {
    'title': 'HIỆU TUỔI ĐỨNG IM NHƯ MỎ NEO',
    'thanh': [{'ten': 'con trước', 'phan': [{'dai': 1, 'nhan': '6', 'mau': 'teal'}]},
              {'ten': 'mẹ trước', 'phan': [{'dai': 1, 'nhan': '6', 'mau': 'teal'},
                                           {'dai': 4, 'nhan': '24', 'mau': 'gold'}]}],
    'note': 'Hiệu vẫn 24. Mẹ gấp 5 lần con nên hiệu là 4 phần: 24 : 4 = 6.',
}, 'Tỉ số trôi theo năm tháng, hiệu thì đứng im.', 1)

mo(28, 'L4H_B28_MO', 'doan_thang', {
    'title': 'BÁC TÂM SƠN 4 GIỜ XONG, CHÚ HÒA 12 GIỜ — CÙNG LÀM THÌ MẤY GIỜ?',
    'thanh': [{'ten': 'bác Tâm 1 giờ', 'phan': [{'dai': 3, 'nhan': '', 'mau': 'teal'}]},
              {'ten': 'chú Hòa 1 giờ', 'phan': [{'dai': 1, 'nhan': '', 'mau': 'gold'}]}],
}, 'Chia hàng rào thành phần đều — mỗi giờ mỗi người làm được mấy phần.')

mo(29, 'L4H_B29_MO', 'may_bien_doi', {
    'title': 'CHO BẠN MỘT NỬA, ĐƯỢC THÊM 2 VIÊN, CÒN 12 — LÚC ĐẦU MẤY VIÊN?',
    'rows': [{'mau': 'teal', 'o': [{'t': '?', 'mau': 'do'}, {'may': 'CHO 1/2'},
                                   {'may': '+ 2'}, {'t': '12', 'mau': 'gold'}]}],
}, 'Băng chuyền chạy xuôi, chỉ biết con số ở cuối.')
giang(29, 'L4H_B29_G1', 'may_bien_doi', {
    'title': 'ĐẢO CHIỀU BĂNG CHUYỀN',
    'rows': [{'mau': 'do', 'nguoc': True,
              'o': [{'t': '20', 'mau': 'gold'}, {'may': '× 2'}, {'may': '− 2'},
                    {'t': '12', 'mau': 'gold'}]}],
    'note': 'Đi ngược thì mỗi trạm đổi phép: cho một nửa ↔ nhân 2, thêm 2 ↔ bớt 2.',
}, 'Đi ngược băng chuyền, mỗi trạm đảo phép tính.', 1)

mo(30, 'L4H_B30_MO', 'con_vat', {
    'title': '36 CON VỪA GÀ VỪA CHÓ, ĐẾM ĐƯỢC 100 CÁI CHÂN',
    'con': [{'chan': 2, 'mau': 'gold', 'ten': 'gà'}, {'chan': 2, 'mau': 'gold', 'ten': 'gà'},
            {'chan': 4, 'mau': 'teal', 'ten': 'chó'}, {'chan': 2, 'mau': 'gold', 'ten': 'gà'},
            {'chan': 4, 'mau': 'teal', 'ten': 'chó'}],
}, 'Đếm đầu ra số con, đếm chân ra số chân.')
giang(30, 'L4H_B30_G1', 'con_vat', {
    'title': 'GIẢ SỬ TẤT CẢ ĐỀU LÀ GÀ',
    'con': [{'chan': 2, 'mau': 'gold', 'ten': 'gà'}, {'chan': 2, 'mau': 'gold', 'ten': 'gà'},
            {'chan': 2, 'mau': 'gold', 'ten': 'gà'}, {'chan': 2, 'mau': 'gold', 'ten': 'gà'},
            {'chan': 2, 'mau': 'gold', 'ten': 'gà'}],
    'note': '36 con gà thì chỉ có 72 chân — hụt 28 chân so với 100.',
}, 'Giả sử tất cả là gà rồi soi phần chân còn hụt.', 1)

mo(31, 'L4H_B31_MO', 'hang_hop', {
    'title': 'HAI HÓA ĐƠN CÙNG SỐ BÚT — GIÁ MỘT QUYỂN VỞ LÀ BAO NHIÊU?',
    'hop': [{'ten': 'Hóa đơn 1', 'dong': ['3 bút + 2 vở', '22 nghìn'], 'mau': 'teal'},
            {'ten': 'Hóa đơn 2', 'dong': ['3 bút + 5 vở', '37 nghìn'], 'mau': 'gold'}],
}, 'Hai hóa đơn có chung phần "3 bút".')
giang(31, 'L4H_B31_G1', 'hang_hop', {
    'title': 'TRỪ HAI HÓA ĐƠN — MÓN CHUNG TỰ BIẾN MẤT',
    'hop': [{'ten': 'Lấy hóa đơn 2', 'dong': ['3 bút + 5 vở', '37 nghìn'], 'mau': 'gold'},
            {'ten': 'Trừ hóa đơn 1', 'dong': ['3 bút + 2 vở', '22 nghìn'], 'mau': 'teal'},
            {'ten': 'Còn lại', 'dong': ['3 vở', '15 nghìn'], 'mau': 'do'}],
    'ket': 'Phần GIỐNG NHAU bị khử, để lộ giá món còn lại.',
}, 'Trừ hai hóa đơn thì phần bút biến mất.', 1)

mo(32, 'L4H_B32_MO', 'ven_hai_vong', {
    'title': 'LỚP 38 BẠN — 25 THÍCH BÓNG ĐÁ, 18 THÍCH CỜ VUA, 8 THÍCH CẢ HAI',
    'trai': {'ten': 'BÓNG ĐÁ', 'tong': 25, 'rieng': 17},
    'phai': {'ten': 'CỜ VUA', 'tong': 18, 'rieng': 10},
    'giua': 8, 'ngoai': {'ten': 'không thích môn nào', 'so': 3},
    'tong': 38, 'an': ['ngoai'],
}, 'Hai vòng giao nhau, phần giữa là bạn thích cả hai môn.')

# ═══════════ CHƯƠNG 9 · ĐẦU BẾP PHÂN SỐ ═══════════

mo(33, 'L4H_B33_MO', 'phan_so_lat', {
    'title': 'LÁT NÀO TO HƠN: 7/8 HAY 9/10?',
    'banh': [{'tu': 7, 'mau': 8}, {'tu': 9, 'mau': 10}],
}, 'Hai phân số trên hai cái bánh TO BẰNG NHAU.')
giang(33, 'L4H_B33_G2', 'phan_so_lat', {
    'title': 'PHẦN CÒN THIẾU MỚI DỄ SO',
    'banh': [{'tu': 1, 'mau': 8, 'ten': 'thiếu 1/8', 'mauSac': 'do'},
             {'tu': 1, 'mau': 10, 'ten': 'thiếu 1/10', 'mauSac': 'do'}],
    'note': 'Thiếu ít hơn thì lớn hơn: 1/10 bé hơn 1/8 nên 9/10 lớn hơn 7/8.',
}, 'So phần CÒN THIẾU của mỗi cái bánh.', 2)

mo(34, 'L4H_B34_MO', 'phan_so_lat', {
    'title': '2/5 SỐ BÁNH LÀ 12 CHIẾC — CẢ HỘP CÓ MẤY CHIẾC?',
    'banh': [{'tu': 2, 'mau': 5, 'kieu': 'thanh', 'nhan': '12 chiếc'}],
    'so': False,
}, 'Thanh chia 5 phần, hai phần đã biết là 12 chiếc.')
giang(34, 'L4H_B34_G1', 'phan_so_lat', {
    'title': 'TÌM GIÁ TRỊ MỘT PHẦN TRƯỚC',
    'banh': [{'tu': 2, 'mau': 5, 'kieu': 'thanh', 'nhan': 'mỗi phần 6 chiếc'}],
    'so': False,
    'note': '12 : 2 = 6 chiếc một phần → cả hộp 6 × 5 = 30 chiếc.',
}, 'Chia cho tử số ra một phần, nhân mẫu số ra cả hộp.', 1)

mo(35, 'L4H_B35_MO', 'day_o', {
    'title': 'CỘNG DÃY PHÂN SỐ NÀY MÀ KHÔNG QUY ĐỒNG ĐƯỢC KHÔNG?',
    'hang': [{'nhan': 'dãy', 'o': [{'t': '1/(1×2)', 'mau': 'teal'},
                                   {'t': '+', 'mo': True},
                                   {'t': '1/(2×3)', 'mau': 'teal'},
                                   {'t': '+', 'mo': True},
                                   {'t': '1/(3×4)', 'mau': 'teal'}]}],
}, 'Dãy phân số mẫu số là tích hai số liền nhau.')

mo(36, 'L4H_B36_MO', 'phan_so_lat', {
    'title': 'CÙNG CỘNG THÊM MẤY VÀO CẢ TỬ VÀ MẪU ĐỂ 3/8 THÀNH 2/3?',
    'banh': [{'tu': 3, 'mau': 8, 'ten': 'phân số đầu'},
             {'tu': 2, 'mau': 3, 'ten': 'phân số đích', 'mauSac': 'gold'}],
}, 'Phân số đầu và phân số đích — hiệu tử mẫu là thứ không đổi.')

mo(37, 'L4H_B37_MO', 'doan_thang', {
    'title': 'BÁN ĐƯỢC 36 NGHÌN, LÃI BẰNG 1/5 TIỀN VỐN',
    'thanh': [{'ten': 'vốn', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'teal'},
                                      {'dai': 2, 'nhan': '', 'mau': 'teal'},
                                      {'dai': 2, 'nhan': '', 'mau': 'teal'},
                                      {'dai': 2, 'nhan': '', 'mau': 'teal'},
                                      {'dai': 2, 'nhan': '', 'mau': 'teal'}]},
              {'ten': 'lãi', 'phan': [{'dai': 2, 'nhan': '', 'mau': 'gold'}]}],
}, 'Vốn 5 phần, lãi 1 phần — tiền bán là 6 phần.')

# ═══════════ CHƯƠNG 10 · KIẾN TRÚC SƯ MÉT VUÔNG ═══════════

mo(38, 'L4H_B38_MO', 'hinh_chu_vi', {
    'title': 'SÂN CHƠI CHU VI 100 M, DÀI HƠN RỘNG 10 M',
    'hinh': [{'loai': 'chunhat', 'canh': ['?', '?', '?', '?'], 'ten': 'sân chơi',
              'mau': 'teal'}],
}, 'Sân chữ nhật, mới biết chu vi và phần hơn.')
giang(38, 'L4H_B38_G2', 'luoi_dien_tich', {
    'title': 'ĐẾM TỪNG VIÊN GẠCH 1 M²',
    'hinh': [{'dai': 6, 'rong': 4, 'ten': 'sân chơi', 'hienTich': False}],
    'note': 'Diện tích là phần LÒNG bên trong, đếm bằng viên gạch 1 m².',
}, 'Lưới ô vuông đếm được từng mét vuông.', 2)

mo(39, 'L4H_B39_MO', 'luoi_dien_tich', {
    'title': 'KÉO DÀI THÊM 5 M THÌ DIỆN TÍCH TĂNG BAO NHIÊU?',
    'hinh': [{'dai': 6, 'rong': 4, 'ten': 'sân cũ', 'hienTich': False},
             {'dai': 7, 'rong': 4, 'ten': 'sân sau khi nới', 'hienTich': False}],
}, 'Sân cũ và dải đất được nới thêm bên phải.')

mo(40, 'L4H_B40_MO', 'hinh_chu_vi', {
    'title': 'CẮT CHỮ NHẬT 8 CM × 6 CM THEO ĐƯỜNG CHÉO',
    'hinh': [{'loai': 'chunhat', 'canh': ['8 cm', '6 cm', '8 cm', '6 cm'],
              'ten': 'tấm bìa', 'mau': 'teal', 'dinh': True}],
}, 'Hình chữ nhật có số đo trên từng cạnh, chưa cắt.')
giang(40, 'L4H_B40_G4', 'hinh_tron', {
    'title': 'GIẢI PHẪU HÌNH TRÒN',
    'hinh': [{'tam': 'O', 'ten': 'bồn hoa tròn',
              'banKinh': {'ten': 'OA'}, 'duongKinh': {'ten': 'MN'}}],
}, 'Tâm, bán kính, đường kính của bồn hoa tròn.', 4)

mo(41, 'L4H_B41_MO', 'thap_khoi', {
    'title': 'KHỐI HỘP DÀI 4 - RỘNG 3 - CAO 2 GỒM MẤY KHỐI NHỎ?',
    'tang': [{'hang': 3, 'cot': 4, 'ten': 'tầng dưới'},
             {'hang': 3, 'cot': 4, 'ten': 'tầng trên'}],
}, 'Tháp khối thật, có khối nấp hàng sau, kèm bản trải từng tầng.')
giang(41, 'L4H_B41_G3', 'khai_trien_hop', {
    'title': 'HỘP GIẤY TRẢI PHẲNG — ĐỦ SÁU MẶT',
    'dai': 4, 'rong': 3, 'cao': 2, 'donVi': 'cm', 'danhSo': True,
    'note': 'Sáu mặt: nắp và đáy giống nhau, bốn mặt xung quanh từng đôi giống nhau.',
}, 'Bản trải phẳng của hộp, đếm được đủ sáu mặt.', 3)

# ═══════════ CHƯƠNG 11 · HOA TIÊU CÂY SỐ ═══════════

mo(42, 'L4H_B42_MO', 'bang_luoi', {
    'title': '3 GIỜ ĐI 120 KM — ĐI 200 KM HẾT MẤY GIỜ?',
    'cot': ['thời gian', 'quãng đường'],
    'hang': [['1 giờ', '?'], ['3 giờ', '120 km'], ['? giờ', '200 km']],
}, 'Bảng thời gian - quãng đường, dòng "một giờ" còn trống.')
giang(42, 'L4H_B42_G1', 'bang_luoi', {
    'title': 'NHỊP CHÂN MỘT GIỜ',
    'cot': ['thời gian', 'quãng đường'],
    'hang': [['1 giờ', '40 km'], ['2 giờ', '80 km'], ['3 giờ', '120 km'],
             ['5 giờ', '200 km']],
    'to': [[0, 1]],
    'note': 'Tìm quãng đường MỘT GIỜ trước, rồi mọi câu hỏi đều trả lời được.',
}, 'Rút về một giờ rồi nhân lên.', 1)

mo(43, 'L4H_B43_MO', 'bang_luoi', {
    'title': 'XE SAU NHANH HƠN 10 KM MỖI GIỜ — BAO LÂU ĐUỔI KỊP?',
    'cot': ['sau mấy giờ', 'còn cách (km)'],
    'hang': [['lúc đầu', '30 km'], ['1 giờ', '?'], ['2 giờ', '?'], ['3 giờ', '?']],
}, 'Bảng theo giờ, cột khoảng cách còn trống.')
giang(43, 'L4H_B43_G1', 'bang_luoi', {
    'title': 'MỖI GIỜ KHÉP ĐƯỢC BAO NHIÊU?',
    'cot': ['sau mấy giờ', 'còn cách (km)'],
    'hang': [['lúc đầu', '30 km'], ['1 giờ', '20 km'], ['2 giờ', '10 km'],
             ['3 giờ', '0 km']],
    'to': [[3, 1]],
    'note': 'Cùng chiều thì mỗi giờ khép lại bằng HIỆU hai vận tốc.',
}, 'Lập bảng theo giờ là thấy ngay lúc gặp nhau.', 1)

mo(44, 'L4H_B44_MO', 'goc_kim', {
    'title': 'LÚC 3 GIỜ ĐÚNG, HAI KIM TẠO THÀNH GÓC GÌ?',
    'gio': 3, 'phut': 0,
}, 'Mặt đồng hồ 12 khấc, hai kim lúc 3 giờ — chưa nói tên góc.')
giang(44, 'L4H_B44_G2', 'goc_kim', {
    'title': 'ĐẾM KHẤC GIỮA HAI KIM',
    'gio': 3, 'phut': 0, 'tenGoc': 'GÓC VUÔNG',
    'note': 'Cả mặt 12 khấc; góc vuông ứng với đúng 3 khấc.',
}, 'Ba khấc giữa hai kim — đó là góc vuông.', 2)


# ═══════════ HÌNH BÀI TẬP — cặp `item:CX` (đề) + `item:CX:giai` (lời giải) ═══════════
#
# Chỉ vẽ cho câu bé PHẢI NHÌN MỚI LÀM ĐƯỢC — 8 câu, đã soát tay từng câu, kết luận
# ghi trong `tools/khao_sat_hinh_lop4.py`. Gộp đề với lời giải làm MỘT hình là lộ đáp
# án lúc bé chưa làm; bỏ hình lời giải thì bài đếm chỉ còn một câu chữ, bé vẫn không
# biết mình SÓT cái nào (chuẩn mục 4).

bt(11, 'L4H_B11_C8', 'C8', 'hang_hop', {
    'title': 'BA CÁCH XẾP, BA PHẦN THỪA',
    'hop': [{'ten': 'Vỉ 3 quả', 'dong': ['thừa 2 quả'], 'mau': 'gold'},
            {'ten': 'Vỉ 4 quả', 'dong': ['thừa 3 quả'], 'mau': 'gold'},
            {'ten': 'Vỉ 5 quả', 'dong': ['thừa 4 quả'], 'mau': 'gold'}],
}, 'Ba cách xếp và phần thừa của từng cách.')
bt(11, 'L4H_B11_C8_G', 'C8', 'hang_hop', {
    'title': 'NHÌN PHẦN THIẾU THÌ BA MANH MỐI HỢP LÀM MỘT',
    'hop': [{'ten': 'Vỉ 3 quả', 'dong': ['thừa 2', 'thiếu 1'], 'mau': 'teal'},
            {'ten': 'Vỉ 4 quả', 'dong': ['thừa 3', 'thiếu 1'], 'mau': 'teal'},
            {'ten': 'Vỉ 5 quả', 'dong': ['thừa 4', 'thiếu 1'], 'mau': 'teal'}],
    'ket': 'Thêm 1 quả thì chia hết cho cả 3, 4 và 5 nên rổ có 60 − 1 = 59 quả.',
}, 'Cả ba cách đều THIẾU ĐÚNG 1 — chỗ ba manh mối gặp nhau.', 'giai')

bt(15, 'L4H_B15_C7', 'C7', 'tia_so', {
    'title': 'TỪ TẦNG 1 LÊN TẦNG 4 — ĐẾM QUÃNG CẦU THANG',
    'moc': [{'so': 1, 'danh': True}, {'so': 2}, {'so': 3}, {'so': 4}],
    'nhan': '12 bậc',
}, 'Bốn tầng, mỗi quãng giữa hai tầng có 12 bậc.')
bt(15, 'L4H_B15_C7_G', 'C7', 'tia_so', {
    'title': 'BỐN TẦNG NHƯNG CHỈ BA QUÃNG',
    'moc': [{'so': 1, 'danh': True}, {'so': 2}, {'so': 3}, {'so': 4}],
    'nhan': '12 bậc',
    'note': 'Số quãng = 4 − 1 = 3 nên phải bước 3 × 12 = 36 bậc. Đếm TẦNG ra 4, đếm QUÃNG mới ra 3.',
}, 'Ba quãng cầu thang, không phải bốn — chỗ bé hay đếm thừa một.', 'giai')

bt(15, 'L4H_B15_C8', 'C8', 'hinh_chu_vi', {
    'title': 'ĐÓNG CỌC QUANH SÂN, BỐN GÓC ĐỀU CÓ CỌC',
    'hinh': [{'loai': 'chunhat', 'canh': ['30 m', '20 m', '30 m', '20 m'],
              'ten': 'sân đình', 'mau': 'teal', 'dinh': True}],
}, 'Sân 30 m × 20 m, bốn góc đã có cọc — chưa biết khoảng cách.')
bt(15, 'L4H_B15_C8_G', 'C8', 'hinh_chu_vi', {
    'title': 'KHOẢNG CÁCH PHẢI CHIA HẾT CẢ 30 LẪN 20',
    'hinh': [{'loai': 'chunhat', 'canh': ['30 m', '20 m', '30 m', '20 m'],
              'ten': 'sân đình', 'mau': 'teal', 'dinh': True}],
    'note': 'Chia hết cả 30 và 20 có 1, 2, 5, 10 nên lớn nhất là 10 m. Vòng khép kín thì số cọc bằng số khoảng: 100 : 10 = 10 cọc.',
}, 'Vòng khép kín thì số cọc bằng số khoảng — khác hẳn hàng thẳng.', 'giai')

bt(32, 'L4H_B32_C1', 'C1', 'ven_hai_vong', {
    'title': '25 BẠN THÍCH BÓNG ĐÁ, TRONG ĐÓ 8 BẠN THÍCH CẢ HAI MÔN',
    'trai': {'ten': 'BÓNG ĐÁ', 'tong': 25, 'rieng': 17},
    'phai': {'ten': 'CỜ VUA', 'tong': 18, 'rieng': 10},
    'giua': 8, 'an': ['rieng'],
}, 'Hai vòng giao nhau; phần CHỈ thích một môn còn để dấu hỏi.')
bt(32, 'L4H_B32_C1_G', 'C1', 'ven_hai_vong', {
    'title': 'PHẦN CHỈ THÍCH BÓNG ĐÁ LÀ 25 BỚT 8',
    'trai': {'ten': 'BÓNG ĐÁ', 'tong': 25, 'rieng': 17},
    'phai': {'ten': 'CỜ VUA', 'tong': 18, 'rieng': 10},
    'giua': 8,
    'note': 'Số 25 đã GỒM 8 bạn thích cả hai môn — bớt đi mới còn phần chỉ thích bóng đá.',
}, 'Điền vùng giữa trước, hai cánh sau.', 'giai')

bt(33, 'L4H_B33_C9', 'C9', 'phan_so_lat', {
    'title': 'XẾP BA PHÂN SỐ TỪ BÉ ĐẾN LỚN',
    'banh': [{'tu': 7, 'mau': 8}, {'tu': 9, 'mau': 10}, {'tu': 5, 'mau': 6}],
}, 'Ba phân số trên ba cái bánh TO BẰNG NHAU.')
bt(33, 'L4H_B33_C9_G', 'C9', 'phan_so_lat', {
    'title': 'SO PHẦN CÒN THIẾU — THIẾU NHIỀU HƠN THÌ BÉ HƠN',
    'banh': [{'tu': 1, 'mau': 6, 'ten': '5/6 thiếu 1/6', 'mauSac': 'do'},
             {'tu': 1, 'mau': 8, 'ten': '7/8 thiếu 1/8', 'mauSac': 'do'},
             {'tu': 1, 'mau': 10, 'ten': '9/10 thiếu 1/10', 'mauSac': 'do'}],
    'so': False,
    'note': 'Cùng tử số 1 thì 1/6 lớn hơn 1/8, 1/8 lớn hơn 1/10 — thiếu nhiều hơn thì bé hơn.',
}, 'Chỉ MỘT phép so phần bù là xếp được cả ba.', 'giai')

bt(41, 'L4H_B41_C6', 'C6', 'khai_trien_hop', {
    'title': 'HỘP BÌA 4 × 3 × 2 — KỂ TÊN BA CẶP MẶT ĐỐI DIỆN',
    'dai': 4, 'rong': 3, 'cao': 2, 'donVi': 'ô',
}, 'Hộp trải phẳng, sáu mặt đã ghi tên — chưa ghi số ô.')
bt(41, 'L4H_B41_C6_G', 'C6', 'khai_trien_hop', {
    'title': 'BA CẶP MẶT, MỖI CẶP HAI MẶT BẰNG NHAU',
    'dai': 4, 'rong': 3, 'cao': 2, 'donVi': 'ô', 'to': ['tren', 'duoi'],
    'note': 'Đáy và nắp 4 × 3 là 12 ô; trước và sau 4 × 2 là 8 ô; hai hông 3 × 2 là 6 ô. Tổng bìa 2 × (12 + 8 + 6) = 52 ô.',
}, 'Nắp và đáy tô đậm — cặp thứ nhất trong ba cặp.', 'giai')

bt(41, 'L4H_B41_C9', 'C9', 'thap_khoi', {
    'title': 'KHỐI 3 × 3 × 3 TRƯỚC KHI KHOÉT HẦM',
    'tang': [{'hang': 3, 'cot': 3, 'ten': 'tầng dưới'},
             {'hang': 3, 'cot': 3, 'ten': 'tầng giữa'},
             {'hang': 3, 'cot': 3, 'ten': 'tầng trên'}],
}, 'Tháp 3 tầng, mỗi tầng 3 × 3 khối — kèm bản trải phẳng từng tầng.')
bt(41, 'L4H_B41_C9_G', 'C9', 'bang_luoi', {
    'title': 'LÁT TỪNG TẦNG — TẦNG NÀO MẤT KHỐI?',
    'cot': ['tầng', 'lúc đầu', 'mất', 'còn lại'],
    'hang': [['trên', '9', '0', '9'], ['giữa', '9', '3', '6'], ['dưới', '9', '0', '9']],
    'to': [[1, 2], [1, 3]],
    'note': 'Hầm xuyên giữa nằm TRỌN ở tầng giữa nên còn 9 + 6 + 9 = 24 khối.',
}, 'Trải từng tầng ra là thấy ngay chỉ tầng giữa mất khối.', 'giai')

bt(44, 'L4H_B44_C8', 'C8', 'goc_kim', {
    'title': 'GIỜ NÀO HAI KIM TẠO THÀNH GÓC VUÔNG?',
    'gio': 3, 'phut': 0,
}, 'Mặt đồng hồ 12 khấc — đếm khấc để dò.')
bt(44, 'L4H_B44_C8_G', 'C8', 'goc_kim', {
    'title': 'CHỖ ĐỨNG THỨ HAI CÁCH SỐ 12 ĐÚNG 3 KHẤC',
    'gio': 9, 'phut': 0, 'tenGoc': 'GÓC VUÔNG',
    'note': 'Kim giờ chỉ có hai chỗ cách số 12 đúng 3 khấc: số 3 đếm xuôi và số 9 đếm phía ngắn.',
}, 'Lúc 9 giờ cũng đúng 3 khấc — nên chỉ có 3 giờ và 9 giờ.', 'giai')


def main():
    with open(RA, 'w', encoding='utf-8') as f:
        json.dump(H, f, ensure_ascii=False, indent=1)
    from collections import Counter
    c = Counter(m['muc'] for m in H)
    a = Counter(m['arch'] for m in H)
    bai = {m['bai'] for m in H}
    print(f'đã ghi {RA}')
    print(f'  {len(H)} hình · {len(bai)}/44 bài có hình · theo mục: {dict(c)}')
    print(f'  nguyên mẫu dùng: {len(a)} loại')
    thieu = sorted(int(MA.format(i)[-2:]) for i in range(1, 45)
                   if MA.format(i) not in bai)
    if thieu:
        print(f'  ⚠ bài chưa có hình nào: {thieu}')
        return 1
    khong_mo = sorted(b for b in bai
                      if not any(m['bai'] == b and m['muc'] == 'chuyenMoBai' for m in H))
    if khong_mo:
        print(f'  ⚠ bài không có hình MÀN MỞ: {khong_mo}')
        return 1
    print('  ✓ chốt: 44/44 bài có hình màn mở')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
