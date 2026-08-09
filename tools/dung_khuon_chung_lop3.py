# -*- coding: utf-8 -*-
"""
LỚP 3 · BƯỚC 5 — dựng bản cho app theo KHUÔN CHUNG với lớp 5.

    python3 tools/dung_khuon_chung_lop3.py

Hai thư mục, hai vai khác nhau — đừng sửa nhầm:
    data/lop3/                    BẢN GỐC: giữ nguyên 8 mục ①…⑧ của sách, để người
                                  đối chiếu với sách giấy. Các bước 3–4 ghi vào đây.
    web/public/content/lop3/      BẢN CHO APP: đúng khuôn lớp 5, sinh ra từ bản gốc.
                                  KHÔNG sửa tay ở đây, chạy lại bước này là mất.

Nhờ cùng khuôn mà lớp 3 dùng được nguyên bộ mã đã có: nhật ký học, sổ phụ huynh,
bảng cô giáo, BKT, nhớ chỗ học dở, gợi ý theo số lần sai — không viết thêm dòng nào.

DÙNG CHUNG `khuon_chung.sang_khuon_chung` với lớp 2, không chép ra bản thứ hai. Hàm
ấy tự đọc `quyen` từ bản gốc để biết đang dựng lớp mấy, nên không có tham số nào để
gọi nhầm. Hai trường riêng của lớp 3 (`hatMam`, `duongLui`) cũng do nó ghi ra, và
CHỈ ghi khi bản gốc thật sự có.

── KỲ SÁT HẠCH ──

8 ôn tập + 3 ải → 11 kỳ sát hạch, đúng khuôn `DCR_*`. Lớp 2 có Bảng tự soi thành
bảng riêng; lớp 3 viết nó thành LỜI trong khối đáp án, và bước 2c đã bóc ra thành
`veCau`. Nhờ thế mọi câu ôn tập lớp 3 đều trỏ đích danh về bài — không câu nào phải
suy theo chương như lớp 2 từng phải làm.

Một câu trỏ về HAI bài là chuyện thật (ôn tập 3 câu 10, ôn tập 4 câu 12). Khuôn lớp 5
chỉ có một ô `diagnosesMicro`, nên ô ấy lấy đích đầu, còn `veBai` giữ đủ danh sách —
mất đích thứ hai thì bé ôn nửa vời mà không ai biết.
"""
import json, os, re, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'tools'))
from khuon_chung import sang_khuon_chung                    # noqa: E402

NGUON = os.path.join(GOC_KHO, 'data', 'lop3')
NGUON_ON = os.path.join(GOC_KHO, 'data', 'lop3_ontap.json')
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop3_hinh_manifest.json')
RA = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop3')
RA_ON = os.path.join(GOC_KHO, 'web', 'public', 'content', 'reviews')
SO_DK = os.path.join(GOC_KHO, 'data', 'chuong_trinh.json')
RA_DK = os.path.join(GOC_KHO, 'web', 'public', 'content', 'chuong_trinh.json')

# Ải xếp tiếp sau 8 chương, cùng cách đánh số với lớp 2
LECH_AI = 8
KHAI_SO = {
    'ma': 'lop3', 'mon': 'toan', 'lop': 3, 'loai': 'hoc',
    'ten': 'Toán Tư Duy lớp 3',
    'phuDe': 'Cùng Su Kem và Su Bống ra khơi Vạn Số',
    'doTuoi': 'Dành cho bé lớp 2 – lớp 3',
    'bieuTuong': '🧭', 'tienTo': 'DL:KSN3.', 'thuMuc': 'lop3',
    'soChuong': 8, 'trangThai': 'dangCo', 'donVi': 'bài',
    'doc': {'chuTo': True, 'moiManMotMuc': True,
            '_vi_sao': 'Bé 8-9 tuổi vẫn đọc chậm như lớp 2: chữ to hơn lớp 5 và mỗi '
                       'màn chỉ một ý. Bài dài hơn lớp 2 nhưng nhịp đọc thì chưa đổi.'},
}


def dung_on_tap(ten_bai):
    """8 ôn tập + 3 ải → kỳ sát hạch khuôn DCR_*, kèm mối nối sai-câu-nào-ôn-bài-đó."""
    if not os.path.exists(NGUON_ON):
        print('  ⚠ chưa có data/lop3_ontap.json — bỏ qua kỳ sát hạch')
        return []
    khoi = json.load(open(NGUON_ON, encoding='utf-8'))['khoi']
    os.makedirs(RA_ON, exist_ok=True)

    so_tay = json.load(open(SO_TAY, encoding='utf-8')) if os.path.exists(SO_TAY) else {}
    hinh_ky = {}
    for hid, h in so_tay.items():
        if h.get('onTap'):
            hinh_ky.setdefault(h['onTap'], []).append(
                {'id': hid, 'file': h['file'], 'caption': h['caption'],
                 'sha256_16': h['sha256_16']})

    ra, thieu_noi = [], 0
    for ma, d in sorted(khoi.items(), key=lambda kv: (kv[1]['loai'] != 'onTap', kv[1]['so'])):
        ai = d['loai'] == 'ai'
        # Bản gốc lớp 3 ghi 'onTap', bản lớp 2 ghi 'ontap', mà giao diện lọc theo
        # 'ontap'. Lệch một chữ hoa là cả 8 ôn tập BIẾN MẤT khỏi màn hình — dữ liệu
        # vẫn đủ, tệp vẫn đúng, chỉ là không ai thấy. Chuẩn hoá ngay tại đây, chỗ
        # dựng bản cho app, chứ đừng bắt giao diện học thêm một cách viết.
        loai = 'ai' if ai else 'ontap'
        ch = d['so'] + (LECH_AI if ai else 0)
        cau = []
        for c in d['cau']:
            ve = d['veCau'].get(c['id']) or []
            if not ve and not ai:
                thieu_noi += 1
            cau.append({
                'id': f"REVITEM:KSN3.C{ch}.A{c['so']}", 'qno': c['so'],
                'star': c.get('mucDo', 1), 'text': c['text'],
                'answer': d['dapAn'].get(c['id'], ''),
                'diagnosesMicro': ve[0] if ve else None,
                # đủ danh sách, vì một câu chốt thường ghép ý của hai bài
                'veBai': [{'id': x, 'ten': ten_bai.get(x, '')} for x in ve],
                # Tên bài viết đủ chữ: bé lớp 3 không biết "micro" là gì, mà đây đúng
                # là dòng bé đọc khi làm sai và cần ôn lại.
                'trapName': ten_bai.get(ve[0], 'ôn lại bài này') if ve else 'ôn lại bài này',
            })
        doc = {
            'id': f'DCR:KSN3.C{ch}', 'quyen': 'lop3', 'chapter': ch,
            'loai': loai, 'so': d['so'],
            'name': re.sub(r'^★+\s*', '', d['ten']).replace('—', '·'),
            'gioiThieu': ' '.join(d['dong'][:2]),
            'need': d['can'], 'tong': d['tong'],
            'passRule': f"Đạt {d['can']}/{d['tong']} câu là qua." if d['can']
                        else f"Làm hết {d['tong']} câu.",
            'examA': cau,
            'deB': [{'id': c['id'], 'qno': c['so'], 'text': c['text'],
                     'answer': d['dapAnB'].get(c['id'], '')} for c in d['cauDeB']],
            'selfCheck': 'Sai câu nào, bấm vào câu đó để mở lại đúng bài cần ôn.',
            'canCu': d['canCu'],
            'hinh': hinh_ky.get(f'C{ch}', []),
        }
        with open(os.path.join(RA_ON, f'DCR_KSN3_C{ch}.json'), 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        ra.append({'id': doc['id'], 'chapter': ch, 'loai': loai, 'so': d['so'],
                   'name': doc['name'], 'soCau': len(cau), 'soCauB': len(doc['deB']),
                   'need': d['can'], 'soHinh': len(doc['hinh'])})

    if thieu_noi:
        print(f'  ⚠ {thieu_noi} câu ôn tập không trỏ về bài nào — bé sai sẽ không '
              f'biết học lại đâu')
    print(f"  {len(ra)} kỳ sát hạch · {sum(x['soCau'] for x in ra)} câu"
          f" · {sum(x['soCauB'] for x in ra)} câu đề B")
    return ra


def main():
    os.makedirs(RA, exist_ok=True)
    teps = sorted(f for f in os.listdir(NGUON) if f.startswith('DL_KSN3_B'))
    bais = [json.load(open(os.path.join(NGUON, t), encoding='utf-8')) for t in teps]
    bais.sort(key=lambda b: b['so'])
    ids = [b['id'] for b in bais]

    idx, canh_bao = [], []
    for k, b in enumerate(bais):
        d = sang_khuon_chung(b, truoc=ids[k - 1] if k else None,
                             sau=ids[k + 1] if k + 1 < len(ids) else None)
        # Chặng giảng rỗng là hỏng CÂM: bài vẫn dựng ra, phòng học vẫn mở, chỉ là
        # không dạy gì. Đây đúng chỗ mẫu tên bước bỏ sót thì không ai hay.
        if not d['knowledgeCore']['statements']:
            canh_bao.append(f"{d['id']}: không có nguyên tắc nào — mẫu tên bước "
                            f"trong khuon_chung.py bỏ sót cách đặt tên của bài này?")
        ten = b['id'].replace('DL:', 'DL_').replace('.', '_') + '.json'
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
            'coDuongLui': 'duongLui' in d,
        })

    ten_bai = {x['id']: x['title'] for x in idx}
    on = dung_on_tap(ten_bai)

    with open(os.path.join(RA, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    with open(os.path.join(RA, 'ontap.json'), 'w', encoding='utf-8') as f:
        json.dump(on, f, ensure_ascii=False, indent=1)

    # ── sổ đăng ký: nơi DUY NHẤT khai khác biệt giữa các quyển ──
    dk = json.load(open(SO_DK, encoding='utf-8'))
    cu = dk['chuongTrinh'].get('lop3', {})
    dk['chuongTrinh']['lop3'] = {**KHAI_SO, **{k: v for k, v in cu.items()
                                               if k not in KHAI_SO},
                                 'soBai': len(ids), 'bai': ids}
    for duong in (SO_DK, RA_DK):
        with open(duong, 'w', encoding='utf-8') as f:
            json.dump(dk, f, ensure_ascii=False, indent=1)

    for c in canh_bao:
        print(f'  ⚠ {c}')
    print(f'dựng {len(idx)} bài theo khuôn chung → {os.path.relpath(RA, GOC_KHO)}')
    print(f"  {sum(x['soCau'] for x in idx)} câu luyện tập"
          f" · {sum(x['soQuiz'] for x in idx)} câu sát hạch"
          f" · {sum(x['soHinh'] for x in idx)} hình"
          f" · {sum(1 for x in idx if x['coDuongLui'])} bài có đường lùi")
    return 1 if canh_bao else 0


if __name__ == '__main__':
    raise SystemExit(main())
