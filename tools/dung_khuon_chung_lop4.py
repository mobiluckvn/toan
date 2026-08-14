# -*- coding: utf-8 -*-
"""
LỚP 4 · BƯỚC 5 — dựng bản cho app theo KHUÔN CHUNG với lớp 5.

    python3 tools/dung_khuon_chung_lop4.py

Hai thư mục, hai vai khác nhau — đừng sửa nhầm:
    data/lop4/                    BẢN GỐC: giữ nguyên 10 mục ①…⑩ của sách, để người
                                  đối chiếu với sách giấy. Các bước 3–4 ghi vào đây.
    web/public/content/lop4/      BẢN CHO APP: đúng khuôn lớp 5, sinh ra từ bản gốc.
                                  KHÔNG sửa tay ở đây, chạy lại bước này là mất.

DÙNG CHUNG `khuon_chung.sang_khuon_chung` với lớp 2 và lớp 3, không chép bản thứ ba.
Hàm ấy tự đọc `quyen` từ bản gốc nên không có tham số nào để gọi nhầm; hai mục riêng
của lớp 4 (③ nhịp DỊCH và ⑤ nhịp LẮP - SOI) đã được nó hiểu từ đợt này.

── KỲ SÁT HẠCH ──

11 ôn tập → 11 kỳ sát hạch khuôn `DCR_*`. Lớp 4 KHÔNG có ải, nên không cần độ lệch
số chương như lớp 3.

Mọi câu đề chính đều có mối nối về bài (bước 2c đã chốt 124/124), nên bé sai câu nào
là bấm một nút mở đúng bài cần ôn. Một câu trỏ về HAI bài là chuyện thật (ôn tập 3
câu 10 ghép Bài 9 + Bài 10); khuôn lớp 5 chỉ có một ô `diagnosesMicro` nên ô ấy lấy
đích đầu, còn `veBai` giữ đủ danh sách — mất đích thứ hai thì bé ôn nửa vời.

⚠ **Chưa khai lớp 4 vào sổ đăng ký ở đây.** Việc khai là bước cuối cùng, và nó chỉ
đúng khi ô nhập đã đạt ngưỡng — xem `--khai` bên dưới và `docs/tiep_theo_lop4.md`.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'tools'))
from khuon_chung import sang_khuon_chung                    # noqa: E402
from de_hieu_lop4 import sua                                # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop4')
NGUON_ON = os.path.join(GOC_KHO, 'data', 'lop4_ontap.json')
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop4_hinh_manifest.json')
DAP_AN_O = os.path.join(GOC_KHO, 'data', 'lop4_dapan_o.json')
# Ô nhập cho KỲ SÁT HẠCH. Thiếu tệp này thì 236 câu quan trọng nhất của quyển —
# chỗ quyết định bé qua chương hay không — quay về "con tự đánh dấu đúng/sai", tức
# là sổ phụ huynh và bảng cô giáo nhận đúng con số bé tự chấm cho mình.
ON_TAP_O = os.path.join(GOC_KHO, 'data', 'lop4_ontap_o.json')
RA = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop4')
RA_VIDEO = os.path.join(GOC_KHO, 'web', 'public', 'content', 'toan', 'video')
RA_ON = os.path.join(GOC_KHO, 'web', 'public', 'content', 'reviews')
SO_DK = os.path.join(GOC_KHO, 'data', 'chuong_trinh.json')
RA_DK = os.path.join(GOC_KHO, 'web', 'public', 'content', 'chuong_trinh.json')

KHAI_SO = {
    'ma': 'lop4', 'mon': 'toan', 'lop': 4, 'loai': 'hoc',
    'ten': 'Toán Tư Duy lớp 4',
    'phuDe': 'Số lớp triệu, dấu hiệu chia hết, tổng - hiệu, tổng - tỉ, phân số, diện tích',
    'doTuoi': 'Dành cho bé lớp 3 – lớp 4',
    'bieuTuong': '🏗️', 'tienTo': 'DL:KSN4.', 'thuMuc': 'lop4',
    'soChuong': 11, 'trangThai': 'dangCo', 'donVi': 'bài',
    'doc': {'chuTo': True, 'moiManMotMuc': True,
            '_vi_sao': 'Bé 9-10 tuổi vẫn đọc chậm: chữ to hơn lớp 5 và mỗi màn chỉ '
                       'một ý. Cờ này CÒN quyết định việc cấm ô gõ chữ — xem chuẩn '
                       'mục 7 luật 1.'},
}


# Tên kỳ sát hạch: sách đặt theo cảnh ("KHAI TRƯƠNG XƯỞNG MÔ HÌNH"), bé đọc xong
# vẫn không biết mình sắp ôn cái gì. Đổi sang tên nói đúng nội dung chương.
TEN_KY = {
    1:  'SỐ ĐẾN LỚP TRIỆU',
    2:  'BỐN PHÉP TÍNH VÀ TÍNH NHANH',
    3:  'DẤU HIỆU CHIA HẾT',
    4:  'DÃY SỐ',
    5:  'TRUNG BÌNH CỘNG',
    6:  'TỔNG - HIỆU',
    7:  'TỔNG - TỈ VÀ HIỆU - TỈ',
    8:  'BÀI TOÁN CÓ LỜI VĂN',
    9:  'PHÂN SỐ',
    10: 'CHU VI, DIỆN TÍCH VÀ HÌNH KHỐI',
    11: 'QUÃNG ĐƯỜNG VÀ THỜI GIAN',
}


def dung_on_tap(ten_bai):
    """11 ôn tập → kỳ sát hạch khuôn DCR_*, kèm mối nối sai-câu-nào-ôn-bài-đó."""
    if not os.path.exists(NGUON_ON):
        print('  ⚠ chưa có data/lop4_ontap.json — bỏ qua kỳ sát hạch')
        return []
    ky = json.load(open(NGUON_ON, encoding='utf-8'))['ky']
    o_nhap = json.load(open(ON_TAP_O, encoding='utf-8')) if os.path.exists(ON_TAP_O) else {}
    if not o_nhap:
        print('  ⚠ chưa có data/lop4_ontap_o.json — kỳ sát hạch sẽ về TỰ CHẤM hết. '
              'Chạy tools/tach_ontap_lop4.py trước.')
    os.makedirs(RA_ON, exist_ok=True)

    so_tay = json.load(open(SO_TAY, encoding='utf-8')) if os.path.exists(SO_TAY) else {}
    hinh_ky = {}
    for hid, h in so_tay.items():
        if h.get('onTap'):
            hinh_ky.setdefault(h['onTap'], []).append(
                {'id': hid, 'file': h['file'], 'caption': h['caption'],
                 'sha256_16': h['sha256_16']})

    ra, thieu_noi = [], 0
    for d in sorted(ky, key=lambda x: x['so']):
        ch = d['so']
        cau = []
        for c in d['examA']:
            ve = c.get('veCau') or []
            if not ve:
                thieu_noi += 1
            khoa = o_nhap.get(f"OT{ch}#C{c['qno']}")
            cau.append({
                'id': f"REVITEM:KSN4.C{ch}.A{c['qno']}", 'qno': c['qno'],
                'star': 1, 'text': sua(c['text']), 'answer': sua(c.get('answer', '')),
                **({'answerKey': khoa} if khoa else {}),
                # lời giải của sách để bé đối chiếu sau khi máy đã chấm
                'solutionNarrative': sua(c.get('answer', '')),
                'diagnosesMicro': ve[0] if ve else None,
                'veBai': [{'id': x, 'ten': ten_bai.get(x, '')} for x in ve],
                # Tên bài viết đủ chữ: bé lớp 4 không biết "micro" là gì, mà đây đúng
                # là dòng bé đọc khi làm sai và cần ôn lại.
                'trapName': ten_bai.get(ve[0], 'ôn lại bài này') if ve
                            else 'ôn lại bài này',
                'canCu': c.get('canCu', ''),
            })
        doc = {
            'id': f'DCR:KSN4.C{ch}', 'quyen': 'lop4', 'chapter': ch,
            # Giao diện lọc theo 'ontap' viết thường — lớp 3 từng ghi 'onTap' và cả
            # 8 kỳ biến mất khỏi màn hình dù dữ liệu vẫn đủ. Chuẩn hoá ngay tại đây.
            'loai': 'ontap', 'so': d['so'],
            'name': f"ÔN TẬP {ch} · {TEN_KY.get(ch, '')}".strip(' ·'),
            'need': d['need'], 'tong': d['tong'],
            'passRule': f"Đạt {d['need']}/{d['tong']} câu là qua.",
            'examA': cau,
            'deB': [{'id': f"B{c['qno']}", 'qno': c['qno'], 'text': sua(c['text']),
                     'answer': sua(c.get('answer', '')),
                     'solutionNarrative': sua(c.get('answer', '')),
                     **({'answerKey': o_nhap[f"OT{ch}#B{c['qno']}"]}
                        if o_nhap.get(f"OT{ch}#B{c['qno']}") else {})}
                    for c in d['deB']],
            'selfCheck': 'Sai câu nào, bấm vào câu đó để mở lại đúng bài cần ôn.',
            'hinh': hinh_ky.get(f'C{ch}', []),
        }
        with open(os.path.join(RA_ON, f'DCR_KSN4_C{ch}.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        ra.append({'id': doc['id'], 'chapter': ch, 'loai': 'ontap', 'so': d['so'],
                   'name': doc['name'], 'soCau': len(cau),
                   'soCauB': len(doc['deB']), 'need': d['need'],
                   'soHinh': len(doc['hinh'])})

    if thieu_noi:
        print(f'  ⚠ {thieu_noi} câu ôn tập không trỏ về bài nào — bé sai sẽ không '
              f'biết học lại đâu')
    print(f"  {len(ra)} kỳ sát hạch · {sum(x['soCau'] for x in ra)} câu"
          f" · {sum(x['soCauB'] for x in ra)} câu đề B")
    return ra


def main(khai=False):
    os.makedirs(RA, exist_ok=True)
    teps = sorted(f for f in os.listdir(NGUON) if f.startswith('DL_KSN4_B'))
    bais = [json.load(open(os.path.join(NGUON, t), encoding='utf-8')) for t in teps]
    bais.sort(key=lambda b: b['so'])
    ids = [b['id'] for b in bais]

    if os.path.exists(DAP_AN_O):
        dap_an = json.load(open(DAP_AN_O, encoding='utf-8'))
    else:
        dap_an = {}
        print('  ⚠ chưa có data/lop4_dapan_o.json — MỌI câu luyện tập sẽ về tự chấm. '
              'Chạy tools/tach_cau_lop4.py trước.')

    idx, canh_bao = [], []
    for k, b in enumerate(bais):
        d = sang_khuon_chung(b, truoc=ids[k - 1] if k else None,
                             sau=ids[k + 1] if k + 1 < len(ids) else None,
                             dap_an=dap_an)
        # Chặng giảng rỗng là hỏng CÂM: bài vẫn dựng, phòng học vẫn mở, chỉ là không
        # dạy gì. Đây đúng chỗ mẫu tên bước bỏ sót thì không ai hay.
        if not d['knowledgeCore']['statements']:
            canh_bao.append(f"{d['id']}: không có nguyên tắc nào — mẫu tên bước "
                            f'trong khuon_chung.py bỏ sót cách đặt tên của bài này?')
        # ── VIDEO MỞ BÀI + BÀI GIẢNG ──
        # Bác chốt 14-08. Khai bằng cách DÒ TỆP CÓ THẬT, không gõ tay danh sách:
        # gõ tay thì khai một bài chưa dựng video là màn hình hiện ô đen, còn dựng
        # xong mà quên khai thì video nằm đó không ai xem. Cả hai đều im lặng.
        goc_ten = ten_tep = b['id'].replace('DL:', 'DL_').replace('.', '_')
        tep_video = os.path.join(RA_VIDEO, f'{ten_tep}_giang.mp4')
        if os.path.exists(tep_video):
            d['video'] = {'giang': f'{ten_tep}_giang.mp4'}

        ten = goc_ten + '.json'
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
            'soChamMay': sum(1 for v in d['practice']['pools'].values()
                             for x in v if x.get('answerKey')),
            'coDuongLui': 'duongLui' in d,
        })

    ten_bai = {x['id']: x['title'] for x in idx}
    on = dung_on_tap(ten_bai)

    with open(os.path.join(RA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    with open(os.path.join(RA, 'ontap.json'), 'w', encoding='utf-8') as f:
        json.dump(on, f, ensure_ascii=False, indent=1)

    cm = sum(x['soChamMay'] for x in idx)
    tc = sum(x['soCau'] for x in idx)

    # ── sổ đăng ký ──
    # Khai vào sổ là thứ làm lớp 4 HIỆN LÊN kệ sách. Nhưng nó cũng bật luôn năm luật
    # ô nhập (`web/test/luat_o_nhap.test.mjs` đọc chính sổ này), trong đó có ngưỡng
    # "chấm máy ≥ 85% câu luyện tập". Khai khi chưa đạt ngưỡng là cổng nghiệm thu đỏ
    # ngay — nên chỉ khai khi được gọi đích danh `--khai`, và vẫn báo nếu chưa đạt.
    if khai:
        ty = cm * 100 // max(tc, 1)
        if ty < 85:
            print(f'  ⚠ mới chấm máy {ty}% câu luyện tập (<85%) — khai vào sổ bây '
                  f'giờ là `luat_o_nhap.test.mjs` đỏ. Xem docs/tiep_theo_lop4.md.')
        dk = json.load(open(SO_DK, encoding='utf-8'))
        cu = dk['chuongTrinh'].get('lop4', {})
        dk['chuongTrinh']['lop4'] = {**KHAI_SO,
                                     **{k: v for k, v in cu.items()
                                        if k not in KHAI_SO},
                                     'soBai': len(ids), 'bai': ids}
        # Kệ "sắp có" phải bớt đúng những lớp vừa xong. Dòng cũ ghi gộp "Lớp 1 · 3 · 4"
        # mà lớp 3 và lớp 4 nay đã có thật, nên chỉ còn Lớp 1.
        # ⚠ Phải LỌC CẢ dòng mới rồi mới chèn: bộ dựng chạy được nhiều lần, mà bản
        # đầu chỉ lọc dòng cũ nên mỗi lần chạy lại đẻ thêm một "Lớp 1" — kệ sách hiện
        # hai dòng y hệt nhau, dữ liệu vẫn hợp lệ nên không phép kiểm nào kêu.
        moi = {'mon': 'toan', 'nhom': 'Toán tiểu học', 'ten': 'Lớp 1'}
        dk['sapCo'] = [x for x in dk.get('sapCo', [])
                       if x.get('ten') not in ('Lớp 1 · 3 · 4', 'Lớp 1')]
        dk['sapCo'].insert(0, moi)
        for duong in (SO_DK, RA_DK):
            with open(duong, 'w', encoding='utf-8') as f:
                json.dump(dk, f, ensure_ascii=False, indent=1)
        print('  ✓ đã khai lop4 vào sổ đăng ký (kệ sách tự hiện, không sửa giao diện)')

    for c in canh_bao:
        print(f'  ⚠ {c}')
    print(f'dựng {len(idx)} bài theo khuôn chung → {os.path.relpath(RA, GOC_KHO)}')
    print(f'  {tc} câu luyện tập ({cm} chấm máy được, {tc - cm} tự chấm)'
          f" · {sum(x['soQuiz'] for x in idx)} câu sát hạch"
          f" · {sum(x['soHinh'] for x in idx)} hình"
          f" · {sum(1 for x in idx if x['coDuongLui'])} bài có đường lùi")
    return 1 if canh_bao else 0


if __name__ == '__main__':
    raise SystemExit(main('--khai' in sys.argv))
