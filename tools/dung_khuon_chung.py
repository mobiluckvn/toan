# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 5 — dựng bản cho app theo KHUÔN CHUNG với lớp 5.

    python3 tools/dung_khuon_chung.py

Hai thư mục, hai vai khác nhau — đừng sửa nhầm:
    data/lop2/                    BẢN GỐC: giữ nguyên 8 mục ①…⑧ của sách, để người
                                  đối chiếu với sách giấy. Các bước 1–4 ghi vào đây.
    web/public/content/lop2/      BẢN CHO APP: đúng khuôn lớp 5, sinh ra từ bản gốc.
                                  KHÔNG sửa tay ở đây, chạy lại bước này là mất.

Nhờ cùng khuôn mà lớp 2 dùng được nguyên bộ mã của lớp 5: nhật ký học, sổ phụ
huynh, bảng cô giáo, BKT, nhớ chỗ học dở, gợi ý theo số lần sai.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'tools'))
from khuon_chung import sang_khuon_chung
from tach_ontap import cau_de_b                    # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop2')
NGUON_ON = os.path.join(GOC_KHO, 'data', 'lop2_ontap.json')
RA_ON = os.path.join(GOC_KHO, 'web', 'public', 'content', 'reviews')
RA = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop2')
RA_VIDEO = os.path.join(GOC_KHO, 'web', 'public', 'content', 'toan', 'video')
SO_DK = os.path.join(GOC_KHO, 'data', 'chuong_trinh.json')
DAP_AN = os.path.join(GOC_KHO, 'data', 'lop2_dapan.json')
RA_DK = os.path.join(GOC_KHO, 'web', 'public', 'content', 'chuong_trinh.json')


# Khai đích danh mối nối cho những câu mà bài gốc đã tách. Khoá là (chương, số câu).
KHAI_TAY_L2 = {
    # ── chương 1 · Vương quốc Số: năm bài tách thành mười ──
    (1, 1): {'ve': 'DL:KSN2.B34'},    # tách số thành tổng — không còn ở B01
    (1, 5): {'ve': 'DL:KSN2.B35'},    # điền dấu lớn bé — so hai số
    (1, 7): {'ve': 'DL:KSN2.B37'},    # tính số mới hơn số cũ bao nhiêu — hiệu
    (1, 8): {'ve': 'DL:KSN2.B38'},    # ba thẻ có số 0
    (1, 11): {'ve': 'DL:KSN2.B37'},   # đổi chỗ hơn 45 đơn vị — hiệu
    (1, 12): {'ve': 'DL:KSN2.B38'},   # ba thẻ 5, 0, 5
    # Câu 6 cũ hỏi lại đúng ý câu 2 (đều là thêm chữ số 0), trong khi bài XOÁ SỐ 0
    # TẬN CÙNG không có câu nào hỏi tới. Viết lại câu 6 cho phủ bài ấy — vẫn giữ
    # nguyên chuyện cửa hàng ghi nhầm giá, chỉ đổi chiều.
    # ── chương 2 · Bé là vua đếm: ba bài tách thành sáu ──
    (2, 1): {'ve': 'DL:KSN2.B39'},    # cột đèn 5, 10, 15 — đếm nhảy cóc
    (2, 2): {'ve': 'DL:KSN2.B39'},    # ghế đá số chẵn — đếm nhảy cóc
    (2, 7): {'ve': 'DL:KSN2.B41'},    # cuốn vở 13 trang — cộng hai đoàn tàu
    (2, 8): {'ve': 'DL:KSN2.B40'},    # số chứa chữ số 4 — bớt số đếm hai lần
    (2, 9): {'ve': 'DL:KSN2.B39'},    # số chẵn số lẻ — đếm nhảy cóc
    # ── chương 3 · Dãy số kỳ diệu: ba bài tách thành chín ──
    # Chương này gộp nặng nhất: mười câu ôn tập của sách đều trỏ dồn vào ba mã cũ,
    # trong khi nay có chín bài. Khai lại từng câu một theo đúng nghề nó hỏi.
    (3, 4): {'ve': 'DL:KSN2.B42'},    # điền hai số bị mờ ở giữa dãy
    (3, 6): {'ve': 'DL:KSN2.B10'},    # 2, 4, 8, 16 — dãy gấp đôi
    (3, 7): {'ve': 'DL:KSN2.B44'},    # 2, 3, 5, 8 — dãy bậc thang
    (3, 8): {'ve': 'DL:KSN2.B47'},    # tổng chẵn hay lẻ, không tính kết quả
    (3, 9): {'ve': 'DL:KSN2.B43'},    # tàu có dừng ở ga 30 không — nhảy cóc thử
    (3, 10): {'ve': 'DL:KSN2.B45'},   # nhiều dãy khác quy luật trong cùng một đề
    # Câu 5 cũ hỏi "đoàn tàu 3, 6, 9, ..., 27 có mấy toa" — đúng ý câu C8 luyện tập
    # của bài NHẢY CÓC THỬ, mà câu 9 đã phủ bài ấy rồi. Trong khi bài BẢNG NHÂN
    # GIẤU GÌ không có câu nào hỏi tới. Viết lại câu 5 cho phủ bài ấy; nghề đếm toa
    # vẫn còn nguyên ở phần luyện tập nên sách không mất gì.
    (3, 5): {'ve': 'DL:KSN2.B46',
             'text': 'Số 37 có nằm trong bảng nhân 5 không? Nhìn vào chữ số nào là '
                     'biết ngay mà không cần đọc cả bảng?',
             'answer': 'Không. Bảng nhân 5 chỉ có số tận cùng bằng 0 hoặc 5, mà 37 '
                       'tận cùng bằng 7 nên nó không thuộc bảng.',
             'khoa': {'parts': [
                 {'label': 'có trong bảng nhân 5 không',
                  'options': ['có', 'không'], 'value': 'không'},
                 {'label': 'nhìn chữ số nào',
                  'options': ['chữ số tận cùng', 'chữ số đầu tiên'],
                  'value': 'chữ số tận cùng'}]}},
    # ── chương 4 · Siêu nhân tính nhanh: bốn bài tách thành mười ──
    (4, 6): {'ve': 'DL:KSN2.B48'},    # ghép khay kẹo 4 × 2 + 4 × 8
    (4, 7): {'ve': 'DL:KSN2.B50'},    # ô trống nhân 4 — máy nhân chia ngược nhau
    (4, 8): {'ve': 'DL:KSN2.B51'},    # 19 trừ ô trống — ca ô trống đứng sau dấu trừ
    (4, 10): {'ve': 'DL:KSN2.B49'},   # dãy chín số, có một bạn đứng giữa
    (4, 12): {'ve': 'DL:KSN2.B52'},   # số thừa nhiều nhất — luật vàng
    # Câu 5 cũ hỏi lại đúng ý câu 2 (đều là ghép đôi tròn chục ở phép cộng), trong
    # khi bài CHIA HẾT HAY CÒN THỪA không có câu nào hỏi tới. Viết lại câu 5 cho phủ
    # bài ấy — vẫn nằm trong mạch chia kẹo của nửa sau chương.
    (4, 5): {'ve': 'DL:KSN2.B53',
             'text': 'Chia 26 viên kẹo cho 4 bạn thì chia hết hay còn thừa, và thừa '
                     'mấy viên?',
             'answer': 'Số 26 không có trong bảng nhân 4 nên còn thừa. Trạm dừng gần '
                       'nhất mà chưa vượt là 24, nên mỗi bạn 6 viên và còn thừa 2 '
                       'viên.',
             'khoa': {'parts': [
                 {'label': 'chia hết hay còn thừa',
                  'options': ['chia hết', 'còn thừa'], 'value': 'còn thừa'},
                 {'label': 'thừa mấy viên', 'value': 2}]}},

    # Hai câu này chấm máy được mà chưa ai khai ô nhập — đáp là MỘT CHỮ SỐ (cái
    # đuôi), chứ không phải câu chữ. Khai vào để kỳ ôn tập 4 chấm máy trọn vẹn.
    (4, 1): {'khoa': {'parts': [{'label': 'bạn ấy có đuôi mấy', 'value': 3}]}},

    # ── chương 5 · Chuyện toán lời văn: sáu bài tách thành mười hai ──
    (5, 5): {'ve': 'DL:KSN2.B54'},    # mỗi bạn góp 5 quyển, 4 bạn — biết mỗi, hỏi tất cả
    (5, 7): {'ve': 'DL:KSN2.B56'},    # tổng 14 hơn nhau 2 — bài hai điều kiện
    (5, 9): {'ve': 'DL:KSN2.B59'},    # 3 giờ được 18 sản phẩm — biết tất cả, hỏi mỗi
    (5, 10): {'ve': 'DL:KSN2.B18'},   # tổng 9 hơn nhau 2 có chia được không — liệt kê
    (5, 11): {'ve': 'DL:KSN2.B58'},   # khi em 8 tuổi thì chị mấy — hiệu tuổi không đổi
    (5, 12): {'ve': 'DL:KSN2.B57'},   # A gấp đôi B, cả hai 15 — chia tổng cho số phần
    # Câu 6 cũ hỏi lại đúng ý câu 2 (đều là tìm người ÍT hơn, phép trừ thẳng), trong
    # khi bài BẪY CÂU CHỮ ĐẢO không có câu nào hỏi tới. Đảo chiều câu 6 cho người
    # phải tìm thành người NHIỀU hơn — đúng cái bẫy mà bài ấy dạy.
    (5, 6): {'ve': 'DL:KSN2.B55',
             'text': 'Lan có ít hơn Hoa 6 nhãn vở. Lan có 15 nhãn vở. Hỏi Hoa có mấy '
                     'nhãn vở? Cẩn thận nhé — ai mới là người nhiều hơn?',
             'answer': 'Lan ít hơn Hoa nên HOA mới là người nhiều nhãn hơn. Vậy phải '
                       'cộng: 15 + 6 = 21 (nhãn vở). Đáp số: 21 nhãn vở.',
             'khoa': {'parts': [
                 {'label': 'ai nhiều hơn', 'options': ['Hoa', 'Lan'], 'value': 'Hoa'},
                 {'label': 'Hoa có mấy nhãn', 'value': 21}]}},

    # ── chương 6 · Thám tử tí hon: bốn bài tách thành tám ──
    (6, 2): {'ve': 'DL:KSN2.B23'},    # 4 đầu 12 chân — gắn tạm hai chân
    (6, 5): {'ve': 'DL:KSN2.B61'},    # 6 đầu 14 chân — chân thừa chia thành cặp
    (6, 6): {'ve': 'DL:KSN2.B62'},    # đường 18 mét — biết chiều dài, tìm số cây
    (6, 7): {'ve': 'DL:KSN2.B25'},    # xếp hạng cuộc thi chạy — vẽ thang
    (6, 8): {'ve': 'DL:KSN2.B63'},    # ba bạn ba món, hai manh mối — bảng loại trừ
    # Câu 4 vốn đã đúng dạng "đi lùi qua hai máy khác loại", chỉ khai lại cho đúng
    # bài THỨ TỰ ĐI LÙI. Nhân tiện bỏ tên nhân vật: chương này nay không còn bài chữ
    # nào nên cái tên ấy mồ côi — bé đọc thấy một tên chưa gặp ở đâu.
    (6, 4): {'ve': 'DL:KSN2.B60',
             'text': 'Một bạn mua bút hết 6 nghìn đồng, rồi được mẹ cho 9 nghìn. Bây '
                     'giờ bạn ấy có 12 nghìn. Hỏi lúc đầu bạn ấy có bao nhiêu nghìn '
                     'đồng?',
             'answer': 'Đi lùi từ cuối: trước khi được cho 9 nghìn thì có '
                       '12 − 9 = 3 (nghìn). Trước khi mua bút hết 6 nghìn thì có '
                       '3 + 6 = 9 (nghìn). Đáp số: lúc đầu có 9 nghìn đồng.',
             'khoa': {'parts': [
                 {'label': 'lúc đầu có bao nhiêu nghìn', 'value': 9}]}},
    # ── chương 2 · cùng lỗi mồ côi, ở câu cuối ──
    (2, 10): {'text': 'Một bạn đánh số một cuốn sổ từ trang 8 đến trang 21. Hỏi bạn '
                      'ấy đánh số bao nhiêu trang, và cần tất cả bao nhiêu chữ số?',
              'answer': 'Số trang: 21 − 8 = 13, thêm một được 14 trang. Số chữ số: '
                        'trang 8 và 9 mỗi trang một chữ số nên hết 2 chữ số; từ trang '
                        '10 đến trang 21 có 12 trang, mỗi trang hai chữ số nên hết '
                        '24 chữ số. Cộng lại: 2 + 24 = 26 chữ số.',
              'khoa': {'parts': [
                  {'label': 'đánh số mấy trang', 'value': 14},
                  {'label': 'cần mấy chữ số', 'value': 26}]}},

    # ── chương 7 · Vương quốc hình học: năm bài tách thành mười ──
    (7, 2): {'ve': 'DL:KSN2.B64'},    # kiến bò quanh tam giác — tổng các cạnh
    (7, 4): {'ve': 'DL:KSN2.B27'},    # tam giác chia bởi một vạch — đếm hình đơn
    (7, 6): {'ve': 'DL:KSN2.B65'},    # ô cửa sổ 2 × 2 — đếm hình ghép
    (7, 7): {'ve': 'DL:KSN2.B68'},    # tháp hai tầng — đếm theo tầng
    (7, 9): {'ve': 'DL:KSN2.B30'},    # tháp cầu thang — luật ngồi
    # Câu 8 và câu 10 cũ đều hỏi lại ý đã có ở câu 2 và câu 6, trong khi hai bài
    # VÌ SAO BÁNH XE PHẢI TRÒN và HÌNH DẸT KHÁC KHỐI không câu nào hỏi tới. Viết
    # lại hai câu ấy cho phủ hai bài.
    (7, 8): {'ve': 'DL:KSN2.B66',
             'text': 'Vì sao bánh xe phải làm hình tròn mà không làm hình vuông? Nếu '
                     'nan hoa của bánh dài 4 xăng-ti-mét thì trục xe cao cách mặt đất '
                     'mấy xăng-ti-mét?',
             'answer': 'Vì mọi nan hoa của hình tròn đều dài bằng nhau, nên trục xe '
                       'luôn cao đều một mức và xe chạy êm. Trục cao đúng bằng một '
                       'nan hoa, tức 4 xăng-ti-mét. Đáp số: 4 xăng-ti-mét.',
             'khoa': {'parts': [
                 {'label': 'vì sao', 'options': ['vì mọi nan hoa đều bằng nhau',
                                                 'vì bánh tròn nhẹ hơn'],
                  'value': 'vì mọi nan hoa đều bằng nhau'},
                 {'label': 'trục cao mấy xăng-ti-mét', 'value': 4}]}},
    (7, 10): {'ve': 'DL:KSN2.B67',
              'text': 'Viên gạch và hình chữ nhật vẽ trên vở — cái nào là KHỐI, cái '
                      'nào là HÌNH? In một mặt của viên gạch ra giấy thì được hình gì?',
              'answer': 'Viên gạch cầm nắm được và có sáu mặt nên là KHỐI. Hình chữ '
                        'nhật vẽ trên vở thì dẹt nên là HÌNH. In một mặt của viên gạch '
                        'ra giấy thì được một hình chữ nhật.',
              'khoa': {'parts': [
                  {'label': 'viên gạch là', 'options': ['khối', 'hình'],
                   'value': 'khối'},
                  {'label': 'in một mặt ra giấy được',
                   'options': ['hình chữ nhật', 'hình tròn', 'hình tam giác'],
                   'value': 'hình chữ nhật'}]}},

    # ── chương 8 · Toán trong cuộc sống: ba bài tách thành sáu ──
    # Chương này nay cũng hết bài chữ, nên bỏ nốt tên nhân vật ở sáu câu.
    (8, 1): {'ve': 'DL:KSN2.B33',
             'text': 'Một bạn mở mắt, đồng hồ có kim phút chỉ 12, kim giờ chỉ 7. Mấy '
                     'giờ rồi nhỉ?',
             'answer': 'Kim phút chỉ 12 nên là giờ đúng; kim giờ chỉ 7 nên là 7 giờ. '
                       'Đáp số: 7 giờ.',
             'khoa': {'parts': [{'label': 'mấy giờ',
                                 'options': ['7 giờ', '12 giờ', '7 giờ rưỡi'],
                                 'value': '7 giờ'}]}},
    (8, 3): {'ve': 'DL:KSN2.B70'},    # mua bánh mì và sữa — tiền phải trả
    (8, 4): {'ve': 'DL:KSN2.B70'},    # đưa 15 nghìn — tiền thối lại
    (8, 5): {'ve': 'DL:KSN2.B69'},    # một nửa của một chục trứng
    (8, 6): {'ve': 'DL:KSN2.B31',
             'text': 'Bữa trưa có chiếc bánh chia thành 4 phần bằng nhau. Một bạn ăn '
                     '1 phần — bạn ấy ăn một phần mấy của chiếc bánh?',
             'answer': 'Chiếc bánh chia thành 4 phần bằng nhau, ăn 1 phần thì ăn một '
                       'phần tư chiếc bánh. Đáp số: một phần tư.',
             'khoa': {'parts': [{'label': 'ăn một phần mấy',
                                 'options': ['một phần tư', 'một nửa'],
                                 'value': 'một phần tư'}]}},
    (8, 7): {'ve': 'DL:KSN2.B31',
             'text': 'Sau khi bạn ấy ăn một phần, chiếc bánh còn lại mấy phần? Cả nhà '
                     '3 người còn lại mỗi người được một phần chứ?',
             'answer': 'Bánh có 4 phần, ăn mất 1 phần thì còn 4 − 1 = 3 phần. Nhà còn '
                       '3 người nên mỗi người vừa đúng một phần. Đáp số: còn 3 phần, '
                       'mỗi người một phần.',
             'khoa': {'parts': [
                 {'label': 'còn mấy phần', 'value': 3},
                 {'label': 'mỗi người có được một phần không',
                  'options': ['có', 'không'], 'value': 'có'}]}},
    (8, 8): {'ve': 'DL:KSN2.B32',
             'text': 'Chiều, một bạn mở quán nước chanh: vốn mua chanh và đường hết 10 '
                     'nghìn; bán được 4 cốc, mỗi cốc 4 nghìn. Hỏi bạn ấy lãi bao nhiêu?',
             'answer': 'Tiền bán: 4 × 4 = 16 (nghìn đồng). Tiền lãi: 16 − 10 = 6 '
                       '(nghìn đồng). Đáp số: lãi 6 nghìn đồng.',
             'khoa': {'parts': [
                 {'label': 'tiền bán mấy nghìn', 'value': 16},
                 {'label': 'lãi mấy nghìn', 'value': 6}]}},
    (8, 9): {'ve': 'DL:KSN2.B70',
             'text': 'Một cô khách đưa 10 nghìn mua 2 cốc nước chanh, mỗi cốc 4 nghìn. '
                     'Phải thối lại cô ấy bao nhiêu?',
             'answer': 'Hai cốc hết 4 × 2 = 8 (nghìn đồng). Thối lại: 10 − 8 = 2 '
                       '(nghìn đồng). Đáp số: 2 nghìn đồng.',
             'khoa': {'parts': [{'label': 'thối lại mấy nghìn', 'value': 2}]}},
    (8, 10): {'ve': 'DL:KSN2.B71',
              'text': 'Tối, 8 giờ rưỡi là giờ đi ngủ. Lúc đó kim phút chỉ số nào, và '
                      'kim giờ nằm giữa hai số nào?',
              'answer': 'Giờ rưỡi thì kim phút chỉ số 6. Kim giờ nằm giữa số 8 và số '
                        '9, vì nó đã đi qua số 8. Đáp số: kim phút chỉ 6; kim giờ giữa '
                        '8 và 9.',
              'khoa': {'parts': [
                  {'label': 'kim phút chỉ số', 'value': 6},
                  {'label': 'kim giờ đã đi qua số', 'value': 8}]}},

    # ── BA ẢI: cả ba đều trỏ dồn về MỘT bài, suốt từ ngày dựng ──
    #
    # Ải không có "bảng tự soi" trong sách, nên bộ dựng lấy mặc định là bài đầu của
    # chương cùng số: ải 1 về B01, ải 2 về B06, ải 3 về B09. Ba mươi câu trỏ sai.
    # Bé sai câu gà chó ở ải 3, bấm ôn lại, và được dẫn tới bài bắt nhịp đoàn tàu.
    # Cổng `on_tap_noi_bai` không bắt được vì nó lọc bỏ ải ngay từ đầu.
    (9, 1): {'ve': 'DL:KSN2.B34'},    # tách 361 thành trăm chục đơn vị
    (9, 2): {'ve': 'DL:KSN2.B02'},    # thêm chữ số 0 vào bên phải
    (9, 3): {'ve': 'DL:KSN2.B06'},    # từ 6 đến 13 có mấy số
    (9, 4): {'ve': 'DL:KSN2.B09'},    # 5, 10, 15 — bắt nhịp dãy cách đều
    (9, 5): {'ve': 'DL:KSN2.B14'},    # ô trống cộng 7 — cho kết quả chạy ngược
    (9, 6): {'ve': 'DL:KSN2.B16'},    # 12 kẹo chia 3 bạn
    (9, 7): {'ve': 'DL:KSN2.B17'},    # An 8, Bình nhiều hơn 4 — sơ đồ đoạn thẳng
    (9, 8): {'ve': 'DL:KSN2.B20'},    # em 7, anh hơn 3 tuổi
    (9, 9): {'ve': 'DL:KSN2.B64'},    # kiến bò quanh tam giác
    (9, 10): {'ve': 'DL:KSN2.B33'},   # kim phút 12, kim giờ 9 — giờ đúng

    (10, 1): {'ve': 'DL:KSN2.B38'},   # ba thẻ có số 0
    (10, 2): {'ve': 'DL:KSN2.B40'},   # số đứng cả hai cánh — bớt một
    (10, 3): {'ve': 'DL:KSN2.B41'},   # cuốn 15 trang — cộng hai đoàn tàu
    (10, 4): {'ve': 'DL:KSN2.B44'},   # 2, 3, 5, 8, 12 — dãy bậc thang
    (10, 5): {'ve': 'DL:KSN2.B12'},   # 37 + 25 + 13 + 5 — ghép đôi tròn chục
    (10, 6): {'ve': 'DL:KSN2.B13'},   # 1 tới 10 — ghép cặp đầu cuối
    (10, 7): {'ve': 'DL:KSN2.B56'},   # tổng 12 hơn nhau 4 — hai điều kiện
    (10, 8): {'ve': 'DL:KSN2.B61'},   # 5 đầu 14 chân — chân thừa chia cặp
    (10, 9): {'ve': 'DL:KSN2.B62'},   # đường 12 mét — tìm số cây
    (10, 10): {'ve': 'DL:KSN2.B32'},  # vốn 10 bán 16 — tính lãi

    (11, 1): {'ve': 'DL:KSN2.B05'},   # tìm số ba chữ số — liệt kê có thứ tự
    (11, 2): {'ve': 'DL:KSN2.B18'},   # tổng 9 hơn nhau 2 — liệt kê mọi cách tách
    (11, 4): {'ve': 'DL:KSN2.B60'},   # máy hai tầng — thứ tự đi lùi
    (11, 6): {'ve': 'DL:KSN2.B68'},   # tháp bốn tầng — đếm theo tầng
    (11, 7): {'ve': 'DL:KSN2.B61'},   # 7 đầu 20 chân — chân thừa chia cặp
    (11, 9): {'ve': 'DL:KSN2.B57'},   # A gấp đôi B — chia tổng cho số phần
    (11, 10): {'ve': 'DL:KSN2.B69'},  # một nửa của 12 và một phần tư của 20
    # Ba câu còn lại của ải 3 nhắc tên riêng mà cả quyển nay không còn ai nhớ:
    # "dãy thỏ Fibonacci", "cầu vồng Gauss", và tên nhân vật của sách.
    (11, 3): {'ve': 'DL:KSN2.B45',
              'text': 'Dãy 1, 1, 2, 3, 5, 8, ... có một quy luật rất lạ: mỗi số bằng '
                      'TỔNG HAI SỐ đứng ngay trước nó. Viết hai số tiếp theo.',
              'answer': 'Số tiếp theo: 5 + 8 = 13. Số sau nữa: 8 + 13 = 21. Đáp số: '
                        '13 và 21.',
              'khoa': {'parts': [{'label': 'số thứ nhất', 'value': 13},
                                 {'label': 'số thứ hai', 'value': 21}]}},
    (11, 5): {'ve': 'DL:KSN2.B41',
              'text': 'Một bạn đánh số một cuốn sổ từ trang 8 đến trang 21. Hỏi bạn ấy '
                      'đánh số bao nhiêu trang, và cần tất cả bao nhiêu chữ số?',
              'answer': 'Số trang: 21 − 8 = 13, thêm một được 14 trang. Số chữ số: '
                        'trang 8 và 9 hết 2 chữ số; từ trang 10 đến 21 có 12 trang, '
                        'mỗi trang hai chữ số nên hết 24 chữ số. Cộng lại: '
                        '2 + 24 = 26 chữ số.',
              'khoa': {'parts': [{'label': 'đánh số mấy trang', 'value': 14},
                                 {'label': 'cần mấy chữ số', 'value': 26}]}},
    (11, 8): {'ve': 'DL:KSN2.B13',
              'text': 'Tính nhanh: 2 + 4 + 6 + ... + 18 + 20. Nhớ mẹo ghép cặp đầu với '
                      'cuối nhé!',
              'answer': 'Dãy có 10 số nên ghép được 5 cặp, mỗi cặp là 2 + 20 = 22. '
                        'Cộng dồn năm lần 22 được 110. Đáp số: 110.',
              'khoa': {'parts': [{'label': 'mỗi cặp bằng', 'value': 22},
                                 {'label': 'tổng', 'value': 110}]}},

    (1, 6): {'ve': 'DL:KSN2.B36',
             'text': 'Một cửa hàng ghi giá 90 nghìn đồng nhưng viết sót mất chữ số '
                     '0 ở cuối, thành 9 nghìn đồng. Giá bị viết rẻ đi bao nhiêu '
                     'nghìn đồng, và số ghi sai nhỏ hơn số đúng mấy lần?',
             'answer': 'Rẻ đi: 90 − 9 = 81 (nghìn đồng). Xoá một chữ số 0 ở cuối '
                       'thì số nhỏ đi 10 lần.'},
}


# Tên kỳ sát hạch của sách có chỗ nhắc nhân vật. Chương nào đã chuyển hết sang
# video thì trong bài không còn nhân vật nào nữa, nên cái tên ấy thành mồ côi — bé
# đọc thấy một cái tên chưa gặp ở đâu bao giờ. Đổi tên đúng những chương ấy thôi;
# chương còn bài chữ thì giữ nguyên tên của sách.
DOI_TEN_KY_L2 = {
    'ÔN TẬP 5 · TUYỂN TẬP CHUYỆN TOÁN CỦA TRÍ LONG':
        'ÔN TẬP 5 · TUYỂN TẬP CHUYỆN TOÁN LỜI VĂN',
    'ÔN TẬP 8 · MỘT NGÀY RA CHỢ CÙNG SU KEM':
        'ÔN TẬP 8 · MỘT NGÀY RA CHỢ',
}


# Quyển lớp 2 nay KHÔNG CÒN BÀI CHỮ NÀO — mọi bài đều là bài video, và video thì
# bác đã chốt là bỏ hẳn nhân vật. Nên hai cái tên của sách không còn xuất hiện ở đâu
# trong bài học nữa; câu ôn tập nào còn nhắc là bé đọc thấy một cái tên chưa gặp bao
# giờ. `KHAI_TAY_L2` viết lại được câu của examA, nhưng đề B thì không đi qua bảng
# ấy, nên quét nốt ở đây.
VO_NHAN_VAT_L2 = {'Su Kem': 'một bạn', 'Trí Long': 'một bạn'}


def _bo_ten_vo(t):
    for a, b in VO_NHAN_VAT_L2.items():
        if t.startswith(a):
            t = b.capitalize() + t[len(a):]
        t = t.replace(a, b)
    return t


def _ten_ky(ten):
    t = re.sub(r'^★+\s*|\s*\(\d+ câu\)$', '', ten).replace('—', '·')
    return DOI_TEN_KY_L2.get(t, t)


# Ô nhập khai TAY cho ĐỀ B. Khoá là (chương, mã câu).
#
# Đề B không đi qua `KHAI_TAY_L2` — nó lấy ô nhập từ `lop2_ontap_o.json`, mà tệp ấy
# do `tach_ontap.py` dựng lại mỗi lần chạy. Vá thẳng vào đó là mất ở lần chạy sau,
# đúng cái bẫy "bản dựng lại đè mất bản sửa tay" đã dính bốn lần.
KHAI_DE_B_L2 = {
    # Đáp là MỘT CHỮ SỐ (cái đuôi), chấm máy được, chỉ là chưa ai khai.
    (4, 'B1'): {'parts': [{'label': 'đuôi mấy', 'value': 8}]},
    # Hai câu đồng hồ: đáp là giờ và là chữ số trên mặt số, chấm máy được cả.
    (8, 'B2'): {'parts': [{'label': 'mấy giờ',
                           'options': ['6 giờ rưỡi', '6 giờ', '7 giờ'],
                           'value': '6 giờ rưỡi'}]},
    (8, 'B10'): {'parts': [{'label': 'kim phút chỉ số', 'value': 6},
                           {'label': 'kim giờ nằm giữa số này', 'value': 9},
                           {'label': 'và số này', 'value': 10}]},
    # Hai câu còn lại của ôn tập 7 CỐ Ý để tự chấm: "kể 2 đồ vật trong nhà" và "vẽ
    # một bức tranh của riêng con" — đáp mở, máy chấm là chấm oan.
}


def dung_on_tap(bai_cua_chuong, ten_bai):
    """8 ôn tập + 3 ải → kỳ sát hạch, đúng khuôn DCR_* của lớp 5.

    BẢNG TỰ SOI của sách khớp thẳng vào `diagnosesMicro`: bé sai câu nào thì bấm
    một nút là mở đúng bài cần ôn. Đây là thứ đáng giá nhất của phần ôn tập —
    cùng ý tưởng với trục CĐ-x.y ↔ Bx.My đã chạy tốt ở lớp 5.
    """
    if not os.path.exists(NGUON_ON):
        return []
    de = json.load(open(NGUON_ON, encoding='utf-8'))
    os.makedirs(RA_ON, exist_ok=True)
    # hình của kỳ sát hạch (tranh công viên, mật thư, bốn trạm…)
    so_tay = {}
    duong_sotay = os.path.join(GOC_KHO, 'data', 'lop2_hinh_manifest.json')
    if os.path.exists(duong_sotay):
        so_tay = json.load(open(duong_sotay, encoding='utf-8'))
    hinh_ky = {}
    for hid, h in so_tay.items():
        if h.get('onTap'):
            hinh_ky.setdefault(h['onTap'], []).append(
                {'id': hid, 'file': h['file'], 'caption': h['caption'],
                 'sha256_16': h['sha256_16']})
    o_nhap = {}
    duong_o = os.path.join(GOC_KHO, 'data', 'lop2_ontap_o.json')
    if os.path.exists(duong_o):
        o_nhap = json.load(open(duong_o, encoding='utf-8'))
    else:
        print('  ⚠ chưa có data/lop2_ontap_o.json — kỳ sát hạch về TỰ CHẤM hết. '
              'Chạy `python3 tools/tach_ontap.py lop2` trước.')

    ra, chua_soi = [], 0

    for ma, d in sorted(de.items(), key=lambda kv: (kv[0][0], int(kv[0][1:]))):
        ai = d['loai'] == 'ai'
        ch = d['so'] + (8 if ai else 0)          # ải xếp tiếp sau 8 chương
        mac_dinh = bai_cua_chuong.get(d['so'], [None])[0]
        cau = []
        for c in d['cau']:
            # ══ MỐI NỐI KHÔNG SUY TỪ SỐ BÀI CỦA SÁCH NỮA ══
            #
            # Bảng tự soi của sách ghi "Câu 5 → Bài 1", và trước đây mã bài suy
            # thẳng từ con số ấy. Từ khi tách bài làm video thì hỏng: mã B01 vẫn
            # còn, nhưng nay nó CHỈ dạy ba phòng, còn phần so sánh đã sang bài
            # khác. Bé sai câu so sánh, bấm "ôn lại bài này", và được dẫn tới bài
            # dạy đọc số.
            #
            # Cả hai đầu đều hợp lệ, chỉ chỗ nối là sai — không phép kiểm nào bắt
            # được. Nên chỗ nào đổi thì khai ĐÍCH DANH ở đây. Cùng cách làm với
            # `KHAI_TAY` bên `tools/ontap_lop4.py`.
            khai = KHAI_TAY_L2.get((ch, c['so'])) or {}
            b = d['soi'].get(str(c['so'])) or d['soi'].get(c['so'])
            if khai.get('ve'):
                mic = khai['ve']
            elif b:
                mic = f'DL:KSN2.B{int(b):02d}'
            else:
                mic = mac_dinh                    # ải không có bảng tự soi
                chua_soi += 0 if ai else 1
            # Câu viết lại thì ô nhập cũ không còn khớp — cho khai đè luôn ở đây,
            # chứ vá vào `lop2_ontap_o.json` thì lần chạy `tach_ontap.py` sau sẽ dựng
            # lại tệp ấy và xoá mất bản vá, y như bốn lần đã dính trước đây.
            khoa = khai.get('khoa') or o_nhap.get(f"{ma}#C{c['so']}")
            cau.append({'id': f"REVITEM:KSN2.C{ch}.A{c['so']}", 'qno': c['so'],
                        'star': c.get('muc', 1),
                        'text': khai.get('text') or c['text'],
                        'answer': khai.get('answer') or d['dapAn'].get(f"C{c['so']}", ''),
                        'solutionNarrative': (khai.get('answer')
                                              or d['dapAn'].get(f"C{c['so']}", '')),
                        **({'answerKey': khoa} if khoa else {}),
                        'diagnosesMicro': mic,
                        # Tên bài viết đủ chữ: bé lớp 2 không biết "micro" là gì,
                        # mà đây đúng là dòng bé đọc khi làm sai và cần ôn lại.
                        'trapName': ten_bai.get(mic, 'ôn lại bài này')})
        doc = {
            'id': f'DCR:KSN2.C{ch}', 'quyen': 'lop2', 'chapter': ch,
            'loai': d['loai'], 'so': d['so'],
            # Tên hiện lên màn hình: bỏ dấu sao và phần "(10 câu)" — bé đã thấy
            # số câu ở góc màn rồi, nhắc lại trong tên chỉ làm dòng dài thêm.
            'name': _ten_ky(d['ten']),
            'gioiThieu': [_bo_ten_vo(x) for x in (d['gioiThieu'] or [])],
            'need': d['can'], 'passRule': d.get('ketLuan', f"Đạt {d['can']}/{d['tong']} câu là qua."),
            'examA': cau,
            # Đề B của lớp 2 nhồi bốn câu vào MỘT dòng ("B1. … B2. … B3. …") nên
            # trước đây nó là một khối chữ không chấm được, và `ExamPlayer` cũng
            # chưa hề hiện tới. Nay cắt theo `B<số>.` thành từng câu thật, mỗi câu
            # một ô nhập — đáp án thì sách đã tách sẵn theo B1, B2… từ lâu.
            'deB': [{'id': c['id'], 'qno': int(c['id'][1:]),
                     'text': _bo_ten_vo(c['text']),
                     'answer': d['dapAnB'].get(c['id'], ''),
                     'solutionNarrative': d['dapAnB'].get(c['id'], ''),
                     **({'answerKey': KHAI_DE_B_L2.get((ch, c['id']))
                                     or o_nhap[f"{ma}#{c['id']}"]}
                        if (KHAI_DE_B_L2.get((ch, c['id']))
                            or o_nhap.get(f"{ma}#{c['id']}")) else {})}
                    for c in cau_de_b(d)],
            'selfCheck': 'Sai câu nào, bấm vào câu đó để mở lại đúng bài cần ôn.',
            'hinh': hinh_ky.get(f'C{ch}', []),
        }
        with open(os.path.join(RA_ON, f'DCR_KSN2_C{ch}.json'), 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        ra.append({'id': doc['id'], 'chapter': ch, 'loai': d['loai'], 'so': d['so'],
                   'soHinh': len(doc['hinh']),
                   # Tên hiện lên màn hình: bỏ dấu sao và phần "(10 câu)" — bé đã thấy
            # số câu ở góc màn rồi, nhắc lại trong tên chỉ làm dòng dài thêm.
            'name': _ten_ky(d['ten']), 'soCau': len(cau), 'need': d['can']})
    if chua_soi:
        print(f'  ⚠ {chua_soi} câu ôn tập chưa có trong Bảng tự soi → tạm trỏ về bài đầu chương')
    print(f'  {len(ra)} kỳ sát hạch · {sum(x["soCau"] for x in ra)} câu')
    return ra


def _cau_luyen(duong):
    d = json.load(open(duong, encoding='utf-8'))
    return [x for v in d['practice']['pools'].values() for x in v]


def main():
    os.makedirs(RA, exist_ok=True)
    # ══ LỐI C — THỨ TỰ HỌC ĐỌC TỪ `thu_tu.json`, KHÔNG ĐỌC TRƯỜNG `so` ══
    #
    # Trước đây thứ tự lấy từ chính trường `so` trong tệp nguồn. Chèn một bài vào
    # giữa là phải dồn mã của mọi bài phía sau — 353 tệp ở lớp 4, và còn phải dời
    # TIẾN ĐỘ ĐÃ LƯU của từng bé cho khớp. Lối C cắt sợi dây ấy: mã bài chỉ còn là
    # cái TÊN, số hiển thị đếm từ vị trí trong lời khai.
    #
    # ⚠ Bộ dựng ĐÈ `b['so']` theo vị trí. Trường `so` trong tệp nguồn KHÔNG còn là
    # sự thật — đừng đọc nó. Xem `docs/ke_hoach_video_lop4.md` §10.
    teps = sorted(f for f in os.listdir(NGUON) if f.startswith('DL_KSN2_B'))
    thu_tu = json.load(open(os.path.join(NGUON, 'thu_tu.json'), encoding='utf-8'))['thuTu']
    co_tep = {t[:-5].replace('DL_KSN2_', 'DL:KSN2.'): t for t in teps}
    thieu_tep = [i for i in thu_tu if i not in co_tep]
    thieu_khai = sorted(i for i in co_tep if i not in thu_tu)
    if thieu_tep or thieu_khai:
        raise SystemExit(
            'thu_tu.json lệch với thư mục nguồn — DỪNG, chưa ghi gì cả.\n'
            + (f'  khai mà không có tệp: {thieu_tep}\n' if thieu_tep else '')
            + (f'  có tệp mà chưa khai: {thieu_khai}' if thieu_khai else ''))
    bais = []
    for vi_tri, ma in enumerate(thu_tu, 1):
        b = json.load(open(os.path.join(NGUON, co_tep[ma]), encoding='utf-8'))
        b['so'] = vi_tri
        bais.append(b)
    ids = [b['id'] for b in bais]

    dap_an = json.load(open(DAP_AN, encoding='utf-8')) if os.path.exists(DAP_AN) else {}

    idx = []
    for k, b in enumerate(bais):
        d = sang_khuon_chung(b, truoc=ids[k - 1] if k else None,
                             sau=ids[k + 1] if k + 1 < len(ids) else None,
                             dap_an=dap_an)
        # Bài nào đã dựng video thì khai vào đây — `StepView.jsx` đọc trường này
        # cho MỌI quyển, không riêng lớp 4. Khai theo tệp CÓ THẬT chứ đừng gõ tay:
        # gõ tay mà khai một bài chưa dựng thì màn hình hiện ô đen, còn dựng xong
        # mà quên khai thì video nằm đó không ai xem. Cả hai đều im lặng.
        ten_tep = b['id'].replace('DL:', 'DL_').replace('.', '_')
        if os.path.exists(os.path.join(RA_VIDEO, f'{ten_tep}_giang.mp4')):
            d['video'] = {'giang': f'{ten_tep}_giang.mp4'}
        ten = ten_tep + '.json'
        with open(os.path.join(RA, ten), 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        idx.append({
            'id': d['id'], 'so': d['so'], 'ten': b['ten'], 'title': d['title'],
            'chuong': d['chuong'], 'tenChuong': d['tenChuong'],
            'bktUnit': d['skills']['bktUnit'], 'passRule': d['assessment']['passRule'],
            'objective': d['objective']['kidText'],
            'durationMinutes': d['durationMinutes'],
            'soCau': sum(len(v) for v in d['practice']['pools'].values()),
            'soQuiz': len(d['assessment']['items']),
            'soHinh': len(d['figureSpec']),
        })

    theo_chuong = {}
    for x in idx:
        theo_chuong.setdefault(x['chuong'], []).append(x['id'])
    ten_bai = {x['id']: x['title'] for x in idx}
    on = dung_on_tap(theo_chuong, ten_bai)

    with open(os.path.join(RA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    with open(os.path.join(RA, 'ontap.json'), 'w', encoding='utf-8') as f:
        json.dump(on, f, ensure_ascii=False, indent=1)

    # sổ đăng ký chương trình — nơi DUY NHẤT khai khác biệt giữa hai lớp
    dk = json.load(open(SO_DK, encoding='utf-8'))
    dk['chuongTrinh']['lop2']['bai'] = ids
    dk['chuongTrinh']['lop2']['soBai'] = len(ids)
    for thu_muc, duong in ((None, SO_DK), (None, RA_DK)):
        with open(duong, 'w', encoding='utf-8') as f:
            json.dump(dk, f, ensure_ascii=False, indent=1)

    tong_hinh = sum(x['soHinh'] for x in idx)
    tong_cau = sum(x['soCau'] for x in idx)
    tong_quiz = sum(x['soQuiz'] for x in idx)
    print(f'dựng {len(idx)} bài theo khuôn chung → {os.path.relpath(RA, GOC_KHO)}')
    cham_may = sum(1 for f in os.listdir(RA) if f.startswith('DL_')
                   for it in _cau_luyen(os.path.join(RA, f)) if it.get('answerKey'))
    print(f'  {tong_cau} câu luyện tập ({cham_may} chấm máy được)'
          f' · {tong_quiz} câu sát hạch · {tong_hinh} hình')


if __name__ == '__main__':
    main()
