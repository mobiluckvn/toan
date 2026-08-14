# -*- coding: utf-8 -*-
"""
Đưa bài lớp 2 về ĐÚNG khuôn dữ liệu của lớp 5, để hai lớp dùng chung một bộ mã.

Trước đây lớp 2 có khuôn riêng (muc + cau) nên phải có phòng học riêng
(Lop2Player, HomeLop2), và mọi tính năng của lớp 5 — nhật ký học, sổ phụ huynh,
bảng cô giáo, BKT, nhớ chỗ học dở, gợi ý theo số lần sai — đều không dùng được.

Bảng khớp mục:
    ① mucTieu      → objective            (mục tiêu, hiện ở màn mở bài)
    ② chuyenMoBai  → lecture.screens hook (tình huống mở bài)
    ③ khamPha      → knowledgeCore.statements + lecture.screens explain
    ④ viDuMau      → workedExample
    ⑤ suKemNham    → knowledgeCore.misconceptions + screen kind 'trap'
    ⑥ luyenTap     → practice.pools warmup/standard/challenge (theo ★ MỨC 1/2/3)
    ⑦ quiz         → assessment.items  (đã có answerKey nên chấm máy được)
    ⑧ gocBoMe      → parentNote
       hình         → figureSpec

KHÔNG bịa dữ liệu cho những trường lớp 5 có mà sách lớp 2 không có (videoSpec,
entryCheck, spacedReview…): thà thiếu còn hơn hiện ra một màn rỗng cho bé đọc.
"""
import json
import os
import re

# LỜI CHÀO MỞ BÀI viết tay — xem `data/loi_chao.json`. Nạp một lần lúc nạp mô-đun:
# ba bộ dựng (lớp 2 · 3 · 4) đều gọi vào đây, nên đọc lại từng bài là thừa.
_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LC = os.path.join(_GOC, 'data', 'loi_chao.json')
LOI_CHAO = {k: v for k, v in
            (json.load(open(_LC, encoding='utf-8')) if os.path.exists(_LC) else {}).items()
            if not k.startswith('_')}

# Mục nào của lớp 2 rơi vào chỗ nào trong khuôn hình của lớp 5
NOI_DUNG_HINH = {
    'chuyenMoBai': 'hook', 'khamPha': 'teach_domain', 'viDuMau': 'teach_core',
    'suKemNham': 'trap', 'mucTieu': 'mantra', 'luyenTap': 'practice', 'quiz': 'assess',
}
MUC_POOL = {1: 'warmup', 2: 'standard', 3: 'challenge'}
# Sách không nhất quán tên bước. Lớp 2 có bốn kiểu: phần lớn ghi "Bước 1.", nhưng
# bài 16 và 27 ghi "Nhịp 1 —", bài 25 ghi "Vũ khí 2 —". Lớp 3 có thêm TÁM kiểu nữa,
# và chúng không hiếm: bài 29 đặt cả ba bước giảng là "Nhân vật 1/2/3", bài 26 dùng
# "Phép thử", bài 24 dùng "Thế trận", bài 20 dùng "Kho báu".
#
# Bỏ sót là bài ấy KHÔNG có nguyên tắc nào, phòng học dựng ra chặng giảng trống trơn
# mà chẳng có gì báo — hỏng câm, đúng kiểu đắt nhất của dây chuyền này. Nên liệt kê
# ĐÍCH DANH rồi canh bằng phép kiểm, chứ không nới mẫu thành "mấy chữ rồi tới số":
# nới rộng thì "Bài 3 —" hay "Đáp số 2." cũng thành bước.
#
# Thêm tám tên KHÔNG làm lệch một dòng nào của lớp 2 — đã đối chiếu cả 33 bài.
TEN_BUOC = ('Bước', 'Nhịp', 'Vũ khí', 'Chặng', 'Phép thử', 'Chiêu', 'Đường',
            'Tuyệt kỹ', 'Kho báu', 'Thế trận', 'Nhân vật', 'Câu hỏi')
R_BUOC = re.compile(r'^(?:' + '|'.join(TEN_BUOC) + r')\s*\d+\s*[.—–-]'
                    r'|^(?:MẸO|LUẬT)[^:]*:')


def _hoa_dau(s):
    """Viết hoa chữ cái đầu, giữ nguyên phần còn lại.

    `str.capitalize()` thì hạ chữ hoa ở phần sau xuống thường — mà đề bài đầy tên
    riêng và đơn vị viết hoa (Trí Long, TỔNG, km/h), nên phải chừa chúng ra.
    """
    s = (s or '').lstrip()
    return s[:1].upper() + s[1:] if s else s


# Động từ mở đầu một câu SAI KHIẾN. "Hỏi tìm X" hay "Hỏi đọc số ấy" không phải
# tiếng Việt — câu sai khiến đứng một mình đã đủ nghĩa, chỉ câu HỎI mới cần chữ
# "Hỏi" dẫn vào. Danh sách lấy từ chính 44 dòng `HỎI GÌ?` của sách lớp 4.
_SAI_KHIEN = ('đọc', 'viết', 'tìm', 'tính', 'lập', 'nêu', 'so sánh', 'xếp', 'đếm',
              'vẽ', 'kiểm chứng', 'chứng minh', 'giải thích', 'chọn', 'điền',
              'tách', 'ghép', 'phân tích', 'sắp xếp', 'dựng', 'đổi', 'gọi tên',
              'chỉ ra', 'liệt kê', 'hoàn thành')


def _thanh_cau_hoi(hoi):
    """Dòng `HỎI GÌ?` → một câu đứng được một mình.

    Câu HỎI thì thêm chữ "Hỏi" dẫn vào và đóng bằng dấu hỏi; câu SAI KHIẾN thì để
    nguyên và đóng bằng dấu chấm. Cắt dấu câu cũ trước khi đóng, nếu không dòng
    nào sẵn dấu hỏi sẽ thành "??".
    """
    h = re.sub(r'\s*[.?!…]+\s*$', '', (hoi or '').strip())
    if not h:
        return ''
    if h.lower().startswith(_SAI_KHIEN):
        return f'{_hoa_dau(h)}.'
    return f'Hỏi {h}?'


def _dong(bai, ten):
    return list((bai['muc'].get(ten) or {}).get('dong') or [])


def _hinh(bai, ten):
    return list((bai['muc'].get(ten) or {}).get('hinh') or [])


def _cau_meo(dong):
    """Câu 'MẸO THÁM TỬ: …' là câu chốt của bài — lớp 5 gọi là mantra."""
    for d in dong:
        if d.startswith(('MẸO', 'LUẬT')):
            return re.sub(r'^(MẸO[^:]*|LUẬT[^:]*):\s*', '', d).strip()
    return ''


def sang_khuon_chung(bai, truoc=None, sau=None, dap_an=None):
    """bai: bản lớp 2 (muc + cau) → dict đúng khuôn lớp 5.

    `dap_an`: {mã bài#mã câu → answerKey} do tools/tach_cau_lop2.py dựng — đây là
    thứ biến câu luyện tập từ "làm ra vở rồi tự so" thành Ô ĐIỀN ĐƯỢC máy chấm.
    """
    dap_an = dap_an or {}
    so = bai['so']
    # Lớp nào lấy từ CHÍNH bản gốc, không nhận qua tham số: bản gốc đã khai `quyen`
    # ở bước 3, mà một tham số thừa là một chỗ để gọi nhầm — dựng lớp 3 mà quên
    # truyền thì cả 34 bài đội mác lớp 2, hợp lệ y như thật.
    quyen = bai.get('quyen', 'lop2')
    grade = int(quyen[-1]) if quyen[-1:].isdigit() else 2

    # ── ③ khám phá → nguyên tắc + màn giảng ──
    kham = _dong(bai, 'khamPha')
    buoc = [d for d in kham if R_BUOC.match(d)]
    khac = [d for d in kham if not R_BUOC.match(d)]
    statements = [{'id': f'K{i}', 'text': d} for i, d in enumerate(buoc, 1)
                  if not d.startswith(('MẸO', 'LUẬT'))]

    # MỖI BƯỚC MỘT MÀN. Bé 7-8 tuổi đọc chậm, dồn cả 4 bước vào một màn là bé nản
    # ngay từ màn đầu. Đây là chỗ hiện thực "nhịp đọc lớp 2" — làm bằng DỮ LIỆU chứ
    # không phải bằng một phòng học riêng.
    #
    # Lớp 4 có thêm HAI mục giảng mà lớp 2 và lớp 3 không có: ③ dựng mô hình (nhịp
    # DỊCH) đứng TRƯỚC các bước, và ⑤ lắp - soi đứng SAU. Chúng chèn thêm màn nên
    # số thứ tự màn của các bước bị đẩy đi — mà hình phần giảng lại neo theo đúng số
    # ấy ('screen:S3'). Nên tính MỘT chỗ lệch dùng chung cho cả hai nơi; quyển nào
    # không có hai mục này thì lệch bằng 0 và mọi số giữ nguyên như cũ.
    screens = []
    mo = _dong(bai, 'chuyenMoBai')
    dich, lap = _dong(bai, 'dichMoHinh'), _dong(bai, 'lapSoi')
    lech = (1 if mo else 0) + (1 if dich else 0)
    if mo:
        # MÀN MỞ NGẮN VÀ NÊU THẲNG BÀI TOÁN. Cả đoạn `chuyenMoBai` dài trung bình
        # 297 chữ — bé bảy tuổi đọc hết chừng ấy vẫn chưa biết bài hỏi gì. Nay giữ
        # ĐÚNG MỘT câu dẫn (câu đầu, để còn có không khí) rồi vào ngay đề bài.
        # Câu đề lấy từ trường đã soạn sẵn, đừng viết mới (chuẩn mục 6 luật 1).
        #
        # ⚠ Với lớp 4 phải lấy từ mục ③ chứ KHÔNG lấy từ ⑥. Hai mục nói về HAI BÀI
        # TOÁN KHÁC NHAU: ② kể tình huống mở (đọc số 24 358 trên bảng tin) còn ⑥ là
        # bài mẫu trình bày vở (tìm số có tổng chữ số bằng 12). Hình màn mở vẽ theo ②,
        # nên lấy đề của ⑥ là lời và hình kể hai bộ số đá nhau ngay dòng đầu bé đọc —
        # đúng bẫy 32, và tôi đã nhìn thấy nó trên màn hình thật trước khi chữa.
        #
        # Mục ③ có sẵn hai dòng `CHO GÌ?` và `HỎI GÌ?` do chính người soạn viết, đủ
        # 44/44 bài, và cả hai nói về ĐÚNG bài toán của tình huống mở. Quyển nào
        # không có mục ấy thì rơi về nếp cũ, nên lớp 2 và lớp 3 không đổi một chữ.
        #
        # ⚠ BẢN ĐẦU CHỈ LẤY `HỎI GÌ?` — VÀ ĐÓ LÀ MỘT MẨU CÂU CỤT.
        # "sau bao nhiêu giờ xe buýt đuổi kịp xe đồ." Đọc lên không biết xe nào,
        # cách nhau bao xa, đi nhanh chậm ra sao — 38/44 bài lớp 4 mở ra là một
        # mẩu như thế, viết thường ngay chữ đầu. Dữ kiện nằm hết ở `CHO GÌ?` mà
        # dòng ấy bị bỏ. Nay ghép cả hai thành một đề đọc được:
        #
        #     Xe đồ ở trước 30 km, mỗi giờ đi 30 km; xe buýt mỗi giờ đi 40 km,
        #     đuổi theo cùng chiều. Hỏi sau bao nhiêu giờ xe buýt đuổi kịp xe đồ?
        #
        # Vẫn không dựng câu mới (chuẩn mục 6 luật 1) — chỉ nối hai dòng người soạn
        # đã viết, viết hoa chữ đầu và đổi dấu chấm cuối thành dấu hỏi.
        def _muc3(nhan):
            return next((re.sub(rf'^{nhan}\?\s*', '', d) for d in _dong(bai, 'dichMoHinh')
                         if d.startswith(f'{nhan}?')), '')

        cho_gi, hoi_gi = _muc3('CHO GÌ'), _muc3('HỎI GÌ')
        if cho_gi and hoi_gi:
            de_bai = f'{_hoa_dau(cho_gi)} {_thanh_cau_hoi(hoi_gi)}'
        else:
            de_bai = hoi_gi or re.sub(
                r'^Đề bài\s*[:.]\s*', '',
                next((d for d in _dong(bai, 'viDuMau') if d.startswith('Đề bài')), ''))
        cau_dau = re.split(r'(?<=[.!?])\s+', ' '.join(mo))[0]
        # Câu dẫn CHỈ giữ khi không có con số nào: chuyện mở bài hay kể một bộ số
        # khác với bộ số của đề ("ba tấm thẻ 2, 5, 8" rồi đề lại cho 4, 0, 9) — ghép
        # vào nhau thành hai đề đá nhau ngay dòng đầu tiên bé đọc.
        if de_bai:
            giu = (len(cau_dau) <= 90 and not re.search(r'\d', cau_dau)
                   and len(cau_dau) + len(de_bai) <= 200)
            loi = f'{cau_dau} {de_bai}' if giu else de_bai
        else:
            loi = ' '.join(mo)
        screens.append({'id': 'S1', 'kind': 'hook', 'narration': loi})
    if dich:
        # Nhịp DỊCH: CHO GÌ · HỎI GÌ · ĐẠI LƯỢNG · CHỌN CÔNG CỤ · ƯỚC LƯỢNG TRƯỚC.
        # Không mang nguyên tắc nào nên `teaches` rỗng — flow.js vẫn giữ màn lại vì
        # nó có lời giảng, và StepView lấy `nhan` làm nhãn thay cho "NGUYÊN TẮC".
        # Nối bằng XUỐNG DÒNG chứ đừng bằng dấu cách: sáu dòng có nhãn (CHO GÌ ·
        # HỎI GÌ · ĐẠI LƯỢNG · QUAN HỆ · CHỌN CÔNG CỤ · ƯỚC LƯỢNG) dồn thành một
        # đoạn liền là bức tường chữ — đúng thứ nhịp đọc chậm sinh ra để tránh.
        # Quyển cũ không có mục này nên chuỗi của chúng không hề có '\n'.
        screens.append({'id': f'S{len(screens) + 1}', 'kind': 'explain',
                        'narration': '\n'.join(dich), 'teaches': [],
                        'nhan': (bai['muc'].get('dichMoHinh') or {}).get('nhip', '')})
    for i, st in enumerate(statements, 1):
        screens.append({'id': f'S{i + lech}', 'kind': 'explain', 'narration': '',
                        'teaches': [st['id']]})
    if lap:
        screens.append({'id': f'S{len(screens) + 1}', 'kind': 'explain',
                        'narration': '\n'.join(lap), 'teaches': [],
                        'nhan': (bai['muc'].get('lapSoi') or {}).get('nhip', '')})
    if khac:
        # lời dặn thêm (không phải "Bước n") gắn vào màn cuối của phần giảng.
        # NỐI chứ đừng ĐÈ: màn cuối của lớp 2 và lớp 3 luôn rỗng lời nên hai cách
        # cho kết quả y hệt, nhưng ở lớp 4 màn cuối là nhịp LẮP - SOI đã có lời —
        # đè lên là mất trắng cả mục ⑤ mà chẳng có gì báo.
        if screens and screens[-1]['kind'] == 'explain':
            cu = screens[-1]['narration']
            screens[-1]['narration'] = f"{cu} {' '.join(khac)}".strip() if cu \
                else ' '.join(khac)
        else:
            screens.append({'id': f'S{len(screens) + 1}', 'kind': 'explain',
                            'narration': ' '.join(khac), 'teaches': []})

    # ── ⑤ Su Kem nhầm → chỗ hay sai + màn bẫy ──
    nham = _dong(bai, 'suKemNham')
    misconceptions = []
    if nham:
        screens.append({'id': f'S{len(screens) + 1}', 'kind': 'trap',
                        'narration': nham[0], 'teaches': []})
        # Tên nhân vật nói sai lấy từ TIÊU ĐỀ MỤC, đừng ghim cứng "Su Kem": sách lớp
        # 3 và lớp 4 đều đặt mục ấy là "TRÍ LONG ƠI, NHẦM RỒI!" nên dòng dấu hiệu
        # đang gọi nhầm tên bạn — bé đọc thấy một tên chẳng liên quan tới câu vừa đọc.
        ten_muc = (bai['muc'].get('suKemNham') or {}).get('ten', '')
        ai = re.split(r'\s+ƠI|,', ten_muc)[0].strip().title() or 'Su Kem'
        misconceptions.append({
            'wrong': nham[0],
            'signal': f'Bé làm theo cách {ai} vừa nói.',
            'fix': ' '.join(nham[1:]) or 'Con thử làm lại theo đúng các bước ở trên nhé.',
        })

    # ── hình: gắn vào ĐÚNG màn nó minh hoạ ──
    # Lớp 5 chỉ đặt được hai hình trong phần giảng (hình khái niệm, hình cách làm).
    # Hình lớp 2 nhiều hơn thế và mỗi hình thuộc một BƯỚC cụ thể — thiếu hình đúng
    # chỗ thì lời văn treo lơ lửng ở dấu hai chấm. Nên chỉ đích danh màn: 'screen:S3'.
    man_cua_buoc = {}                       # số thứ tự dòng "Bước n" → mã màn
    dem = 0
    for k, d in enumerate(kham):
        if R_BUOC.match(d) and not d.startswith(('MẸO', 'LUẬT')):
            dem += 1
            man_cua_buoc[k] = f'S{dem + lech}'

    fig, n = [], 0
    for ten_muc, cho in NOI_DUNG_HINH.items():
        for h in _hinh(bai, ten_muc):
            n += 1
            noi = cho
            if h.get('cau'):
                # ':giai' = hình chỉ hiện SAU khi bé làm xong. Bài đếm hình thì lời
                # giải phải chỉ từng hình tìm được ngay trên hình vẽ.
                noi = f"item:{h['cau']}" + (':giai' if h.get('vaiTro') == 'giai' else '')
            elif ten_muc == 'khamPha':
                # hình đứng ngay sau dòng nào thì thuộc màn của dòng ấy
                # KHÔNG đặt tên `truoc` ở đây: nó là tham số của hàm (bài liền trước),
                # đè lên là series.prev ra danh sách chỉ số dòng.
                dong_truoc = [k for k in man_cua_buoc if k <= h.get('sauDong', 0)]
                if dong_truoc:
                    noi = f'screen:{man_cua_buoc[max(dong_truoc)]}'
            fig.append({'id': h.get('id') or f'F{n}', 'usedIn': [noi],
                        'file': h['file'], 'caption': h.get('caption', ''),
                        'sha256_16': h.get('sha256_16', ''), 'mucGoc': ten_muc})

    # ── ④ ví dụ mẫu → workedExample ──
    vd = _dong(bai, 'viDuMau')
    de = next((d for d in vd if d.startswith('Đề bài')), '')
    worked = None
    if vd:
        worked = {'title': 'Bài mẫu',
                  'problem': re.sub(r'^Đề bài:\s*', '', de) or vd[0],
                  'steps': [{'show': d} for d in vd if d is not de and d != de]}

    # ── ⑥⑦ câu hỏi ──
    pools = {'warmup': [], 'standard': [], 'challenge': []}
    assess = []
    for c in bai['cau']:
        item = {'id': c['id'], 'text': c['text']}
        if c.get('format'):
            item['format'] = c['format']
        if c.get('choices'):
            item['choices'] = c['choices']
        if c.get('answerKey'):
            item['answerKey'] = c['answerKey']
        elif dap_an.get(f"{bai['id']}#{c['id']}"):
            # câu luyện tập đã tách thành ô điền được
            item['answerKey'] = dap_an[f"{bai['id']}#{c['id']}"]
        # Câu tự luận: lời chữa của sách chính là lời giải mẫu bé đối chiếu.
        if c.get('loiChua'):
            item['solutionNarrative'] = c['loiChua']
        elif not c.get('answerKey'):
            # Sách có vài câu là VIỆC LÀM BẰNG TAY (úp vật tròn lên giấy rồi tô
            # theo viền…) nên cố tình không có đáp án. Nói thẳng với bé thay vì
            # bịa một lời giải, cũng thay vì để trống rồi bé bấm mãi không ra gì.
            item['thucHanh'] = True
            item['solutionNarrative'] = ('Câu này con làm bằng tay rồi khoe bố mẹ nhé — '
                                         'sách không có đáp án để so.')
        if c['phan'] == 'quiz':
            assess.append(item)
        else:
            pools[MUC_POOL.get(c.get('muc', 1), 'warmup')].append(item)

    # ── ⑧ góc bố mẹ ──
    gbm = _dong(bai, 'gocBoMe')
    nen = next((d for d in gbm if d.startswith('NÊN')), '')
    parent = {'onComplete': gbm[0] if gbm else '',
              'homeActivity': gbm[1] if len(gbm) > 1 else '',
              'watchFor': nen}

    muc_tieu = ' '.join(_dong(bai, 'mucTieu'))
    ra = {
        '$schema': 'digital-lesson/v2-micro',
        'id': bai['id'], 'grade': grade, 'quyen': quyen,
        'title': f"Bài {so} · {bai['ten']}",
        'durationMinutes': 10,
        'so': so, 'chuong': bai['chuong'], 'tenChuong': bai['tenChuong'],
        'dangGoc': bai.get('dangGoc', ''),
        'skills': {'bktUnit': f"CHUONG:{bai['chuong']}@G{grade}", 'primary': []},
        'series': {'order': so, 'prev': truoc, 'next': sau},
        # `kidText` là dòng ĐẦU TIÊN bé đọc khi mở bài. Trước đây nó là bản sao y
        # nguyên của `text` — tức mục tiêu giáo án: 30/33 bài lớp 2, 32/34 lớp 3 và
        # 44/44 lớp 4 dài quá 170 chữ, từ ba câu trở lên, lại nói sẵn cách làm. Bé
        # đọc là muốn bỏ. Nay lấy lời chào viết tay ở `data/loi_chao.json`; bài nào
        # chưa có thì vẫn rơi về mục tiêu, và cổng `loi_chao.test.mjs` bắt ngay.
        # `laLoiChao` nói rõ dòng này LÀ lời mời viết tay, không phải mục tiêu giáo
        # án bị dùng tạm. Giao diện chỉ in nó ở màn mở khi cờ này bật — quyển nào
        # chưa có lời chào thì đừng in mục tiêu ra chỗ ấy, vì mục tiêu là câu TRẢ
        # LỜI cho bài toán sắp hỏi. Cờ tường minh, không suy từ nhịp đọc: nhịp đọc
        # và chuyện đã viết lời chào hay chưa là hai việc rời nhau.
        'objective': {'id': 'O1', 'text': muc_tieu,
                      'kidText': LOI_CHAO.get(bai['id']) or muc_tieu,
                      'laLoiChao': bai['id'] in LOI_CHAO,
                      'passRule': 'đúng ≥ 4/5 câu tự kiểm'},
        'knowledgeCore': {
            'statements': statements,
            # Không có mục KHÁM PHÁ thì KHÔNG có câu chốt. Bản cũ lùi về tên bài,
            # nên bài mà video thay phần giảng vẫn hiện một màn NGUYÊN TẮC CẦN NHỚ
            # chỉ chép lại đúng tên bài — một màn không nói gì. Bác chốt 14-08.
            'mantra': _cau_meo(kham) or (f"Bài {so}: {bai['ten']}" if kham else ''),
            'vocabulary': [], 'canonicalExamples': [],
            'misconceptions': misconceptions,
        },
        'lecture': {'screens': screens},
        'workedExample': worked,
        'practice': {'pools': pools},
        'assessment': {'passRule': '≥ 4/5', 'items': assess},
        'parentNote': parent,
        'figureSpec': fig,
    }

    # ── hai trường chỉ quyển nối tiếp mới có (lớp 3 nối lớp 2) ──
    # Chỉ ghi ra khi bản gốc THẬT SỰ có, để bài lớp 2 không mọc thêm trường rỗng —
    # trường rỗng thì giao diện phải đoán "chưa làm" hay "đã xét và không có".
    if bai.get('hatMam'):
        ra['hatMam'] = bai['hatMam']            # lời nối ngược, hiện ở màn kết bài
    # `ganLop2` là tên CŨ, có từ hồi chỉ lớp 3 mới lùi được. Nay lớp 4 lùi về lớp 3
    # và lớp 5 lùi về lớp 4, nên tên chung là `ganDuoi` — vẫn nhận tên cũ để bản gốc
    # lớp 3 đã ghi ra đĩa không phải dựng lại.
    gan = bai.get('ganDuoi') or bai.get('ganLop2') or {}
    if gan.get('ve'):
        # nút "Học lại bài lớp <n−1>". Danh sách rỗng thì KHÔNG ghi trường, nên chỗ
        # hiện nút chỉ cần hỏi "có trường không", khỏi phải biết luật `canCu`.
        #
        # Nhãn phải suy từ ĐÍCH chứ đừng ghim chữ "lớp 2": lớp 4 trỏ về lớp 3 mà nút
        # vẫn mời "Học lại bài lớp 2" thì bé bấm vào một lớp chẳng liên quan — đúng
        # kiểu mất niềm tin vào chính cái nút ấy mà chuẩn mục 4 cảnh báo.
        lop_duoi = gan.get('lopDuoi') or (grade - 1)
        ra['duongLui'] = {'ve': gan['ve'], 'ten': gan.get('ten', []),
                          'canCu': gan.get('canCu', ''),
                          'lopDuoi': lop_duoi,
                          'nhan': f'Học lại bài lớp {lop_duoi}'}
    return ra
