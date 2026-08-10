# -*- coding: utf-8 -*-
"""
BẢN ĐỒ CHỦ ĐỀ — dựng `web/public/content/chu_de.json` để app xem & luyện theo CHỦ ĐỀ
xuyên suốt các lớp, thay vì chỉ đi một chiều kệ sách → quyển → chương → bài.

    python3 tools/dung_chu_de.py            # dựng + in bảng tổng
    python3 tools/dung_chu_de.py --soat     # chỉ in, không ghi
    python3 tools/dung_chu_de.py --in       # in TỪNG DẠNG BÀI để soi tay

── NGUỒN ──

Không dựng ma trận mới. `data/km_v1_38.json` đã có sẵn đúng ma trận bác gửi
(264/264 trường hợp trùng tên và trùng mức CB/NC — xem `tools/ma_tran.py`), gồm:

    5 KnowledgeArea → 34 Topic → 82 ProblemType → 264 Case
    adj.taughtBy: dạng bài → danh sách bài, ĐÃ xuyên lớp

Việc ở đây là ba thứ: dịch id, hạ lớp 5 xuống micro, và rút gọn cho vừa máy con.
Cả tệp bản đồ 5021 nút thì nặng vô ích — bản rút gọn chỉ mang thứ giao diện cần.

── THANG LÙI: LUẬT DỰNG, THEO THỨ TỰ ƯU TIÊN ──

1. Lớp 2·3·4: `adj.taughtBy[PT]` → dịch sang id app → bỏ id không có bài thật.
   Đã đối chiếu với `dangGoc` (ý kiến thứ hai, do người soạn ghi tay từng bài):
   **105/111 bài khớp**, 2 lệch vì `dangGoc` viện dẫn số hiệu không có trong ma trận.
2. Lớp 5: **CHỈ căn cứ `skills.primary` của từng MICRO**, không dùng `taughtBy`.
   Bé học và trượt ở mức micro, mà khai ở mức bài thì thô hơn một tầng — và thô
   đúng chỗ chết người: bản đồ khai bài 11 dạy cả "5.2 dãy số" lẫn "6.4 chữ số tận
   cùng", trong khi **cả ba micro của nó đều dạy 6.4**. Lấy theo bài thì bé trượt
   "dãy số không cách đều" bị đẩy sang ba bài chữ số tận cùng. Có 19 cặp (bài, dạng)
   như thế; nay bỏ hết, bài nào không micro nào dạy thì không thành bậc.
3. `data/chu_de_tay.json` đè lên tất cả — chỗ nào soi mắt thấy sai thì sửa ở đấy.

── ĐƯỜNG LÙI CỦA SÁCH KHÔNG ĐƯỢC LÀM BẬC THANG ──

Bản kế hoạch đầu định lấy `duongLui` có `canCu:'sach'` đè lên thang, vì đó là mối
nối chính sách chỉ đích danh nên "đáng tin hơn". **Thử rồi và phải bỏ:** trong 78
bậc nó thêm vào thì **30 bậc rơi vào bài dạy chủ đề KHÁC**.

    "3.1. Lập số lớn nhất / nhỏ nhất"  ←  DL:KSN3.B06, mà bài ấy dạy phép chia có dư

Vì hai thứ ấy trả lời hai câu hỏi khác nhau: `duongLui` nói **"bài này dựng trên bài
kia"** (quan hệ bài nền), còn thang chủ đề cần **"bài này dạy chủ đề ấy"** (quan hệ
thành viên). Bài nền hoàn toàn có thể thuộc chủ đề khác — và thường là thế, vì học
chủ đề mới bao giờ cũng phải mượn kỹ năng của chủ đề cũ.

Trộn hai quan hệ lại thì bé trượt "lập số lớn nhất" bị đẩy sang bài chia có dư. Nên
thang chỉ dựng từ quan hệ THÀNH VIÊN, còn `duongLui` vẫn giữ nguyên chỗ cũ của nó ở
màn kết mỗi bài. Hai lối lùi, hai việc khác nhau, không cái nào thay được cái nào.

Chưa đưa Mùa giải (`lop5q2`) vào thang: nó nối vào chủ đề qua HAI chặng
(`bay[].micro` → micro lớp 5 → dạng bài) nên độ tin thấp hẳn. Để đợt sau.
"""
import json, os, re, sys, collections

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ma_tran import doc_km, doc_xlsx, ghep                       # noqa: E402

RA_GOC = os.path.join(GOC_KHO, 'data', 'chu_de.json')
RA_WEB = os.path.join(GOC_KHO, 'web', 'public', 'content', 'chu_de.json')
TAY = os.path.join(GOC_KHO, 'data', 'chu_de_tay.json')

# Bản đồ gọi quyển theo mã sách, app gọi theo mã chương trình. Bảng này là chỗ
# DUY NHẤT biết cả hai cách gọi — thêm quyển thì thêm một dòng ở đây.
QUYEN = {
    'TTD2':   {'ma': 'lop2', 'lop': 2, 'tienTo': 'DL:KSN2.',   'dem0': True},
    'TTD3':   {'ma': 'lop3', 'lop': 3, 'tienTo': 'DL:KSN3.',   'dem0': True},
    'KSN4':   {'ma': 'lop4', 'lop': 4, 'tienTo': 'DL:KSN4.',   'dem0': True},
    'KSN5Q1': {'ma': 'lop5', 'lop': 5, 'tienTo': 'DL:KSN5Q1.', 'dem0': False},
}
LOP_CHAM = ('lop2', 'lop3', 'lop4')       # quyển đọc chậm: một bài một tệp


def id_app(les):
    """'LESSON:TTD2.B1' → ('lop2', 2, 'DL:KSN2.B01').

    Hai chỗ khác nhau giữa hai cách đánh id, và cả hai đều từng làm hỏng phép ghép:
    tiền tố khác nhau, và lớp 2·3·4 ĐỆM SỐ 0 còn lớp 5 thì không.
    """
    m = re.match(r'LESSON:(\w+)\.B(\d+)$', les or '')
    if not m or m.group(1) not in QUYEN:
        return None
    q = QUYEN[m.group(1)]
    so = int(m.group(2))
    return q['ma'], q['lop'], q['tienTo'] + (f'B{so:02}' if q['dem0'] else f'B{so}')


def _pt_cua(case_id):
    """'CASE:I.6.3#1' → 'PT:I.6.3'.

    20/168 micro lớp 5 mang mã CASE không tra được nút `Case` trong bản đồ, nhưng
    số hiệu dạng bài vẫn nằm ngay trong chuỗi — nên vẫn suy đúng tới cấp DẠNG.
    """
    m = re.match(r'CASE:([IVX]+(?:\.\d+){2})#', case_id or '')
    return 'PT:' + m.group(1) if m else None


def nap_bai(pt_that=None, teaches=None):
    """Đọc mọi bài có thật. Trả (`ten` id→tên hiện lên màn, `micro5` PT→[micro], `sot`).

    `pt_that` là tập dạng bài CÓ THẬT trong ma trận. Micro nào khai một số hiệu
    không có trong ấy thì mới lùi về lấy khai ở mức BÀI (`teaches`) — vá hẹp, chỉ
    cho 9 micro của bài 19·20·24, chứ không mở rộng thành luật chung (xem lời mở đầu).
    """
    ten, micro5, sot, muc_tieu = {}, collections.defaultdict(list), [], {}

    for ma in LOP_CHAM:
        duong = os.path.join(GOC_KHO, 'web', 'public', 'content', ma, 'index.json')
        for b in json.load(open(duong, encoding='utf-8')):
            ten[b['id']] = b.get('title') or b['ten']
            if b.get('objective'):
                muc_tieu[b['id']] = b['objective']

    thu_muc = os.path.join(GOC_KHO, 'data', 'lessons')
    for f in sorted(os.listdir(thu_muc)):
        if not f.endswith('.json'):
            continue
        b = json.load(open(os.path.join(thu_muc, f), encoding='utf-8'))
        ten[b['id']] = b.get('title') or b['id']
        mt = (b.get('objective') or {})
        if mt.get('text'):
            muc_tieu[b['id']] = mt['text']
        ds = [p for p in ((_pt_cua(c) for c in
                           (b.get('skills') or {}).get('primary') or [])) if p]
        hop = [p for p in ds if pt_that is None or p in pt_that]
        if not hop and ds:
            bai_km = 'LESSON:KSN5Q1.' + b['id'].split('.')[1]
            hop = [p for p in ((teaches or {}).get(bai_km) or [])
                   if pt_that is None or p in pt_that]
            sot.append((b['id'], ds[0], hop))
        for p in hop:
            micro5[p].append(b['id'])
    return ten, micro5, sot, muc_tieu


def nap_duong_lui():
    """{(id trên, lớp dưới): [id dưới]} — mối nối chính sách chỉ đích danh.

    KHÔNG dùng để dựng thang (xem lời mở đầu tệp), chỉ để ĐỐI CHIẾU: bậc nào thang
    và sách cùng nói thì yên tâm, chỗ nào lệch thì in ra cho người soi.
    """
    ra = {}
    for ma in LOP_CHAM + ('lessons',):
        thu_muc = os.path.join(GOC_KHO, 'data', ma)
        if not os.path.isdir(thu_muc):
            continue
        for f in sorted(os.listdir(thu_muc)):
            if not f.endswith('.json') or f == 'index.json':
                continue
            b = json.load(open(os.path.join(thu_muc, f), encoding='utf-8'))
            # ba tên trường cho cùng một thứ, do ba đợt làm khác nhau đặt
            d = b.get('duongLui') or b.get('ganDuoi') or b.get('ganLop2')
            if not isinstance(d, dict) or d.get('canCu') not in ('sach', 'sachSua'):
                continue
            ve = [x for x in (d.get('ve') or []) if x]
            if ve:
                ra[(b['id'], d.get('lopDuoi') or 2)] = ve
    return ra


def dung():
    km, theo = doc_km()
    xl = doc_xlsx()
    ten_dang, ten_cd, _ = ghep(xl, theo)
    ten_bai, micro5, sot, muc_tieu = nap_bai(set(theo['ProblemType']),
                                             km['adj']['teaches'])
    lui = nap_duong_lui()
    tay = json.load(open(TAY, encoding='utf-8')) if os.path.exists(TAY) else {}
    tay = {k: v for k, v in tay.items() if not k.startswith('_')}

    area, top, pt, case = (theo['KnowledgeArea'], theo['Topic'],
                           theo['ProblemType'], theo['Case'])
    cha = km['adj'].get('parentOf') or {}

    # ── đếm CB/NC cho từng dạng bài, qua số hiệu của mã CASE
    muc = collections.defaultdict(lambda: {'CB': 0, 'NC': 0})
    for c in case.values():
        p = _pt_cua(c['id'])
        if p:
            muc[p][c.get('difficulty') or 'NC'] += 1

    canh_bao = []
    for mid, hong, thay in sot:
        if thay:
            print(f'  ⓘ {mid} khai "{hong}" (ma trận không có) → lấy khai mức bài: '
                  + ', '.join(thay))
        else:
            canh_bao.append(f'{mid} khai "{hong}" mà ma trận không có, mức bài cũng '
                            f'không cứu được — micro này không vào bản đồ')
    dang = {}
    for ma_pt, n in pt.items():
        bac = collections.defaultdict(list)
        # lớp 2·3·4 — theo bài, vì một bài là một đơn vị bé mở ra học
        for les in km['adj']['taughtBy'].get(ma_pt) or []:
            a = id_app(les)
            if not a:
                canh_bao.append(f'{ma_pt}: không dịch được id "{les}"')
                continue
            _, lop, i = a
            if lop == 5:
                continue                        # lớp 5 lấy ở dưới, theo micro
            if i in ten_bai:
                bac[lop].append(i)
            else:
                canh_bao.append(f'{ma_pt}: "{i}" không có bài thật')
        # lớp 5 — theo MICRO, và chỉ theo micro
        bac[5] += micro5.get(ma_pt, [])

        thang = []
        for lop in sorted(bac):
            ds = sorted(dict.fromkeys(bac[lop]))
            if not ds:
                continue
            # bậc này có được CHÍNH SÁCH xác nhận là bài nền của bậc trên không —
            # chỉ để ghi công, không quyết định bậc có mặt hay không
            xac_nhan = any(d in (lui.get((t, lop)) or [])
                           for t in bac.get(lop + 1, []) for d in ds)
            thang.append({'lop': lop, 'bai': ds,
                          'ten': [ten_bai.get(x, x) for x in ds],
                          'canCu': 'skills' if lop == 5 else 'km',
                          **({'sachXacNhan': True} if xac_nhan else {})})

        # Lời giới thiệu theo lớp lấy ở bản đồ. Bản đồ khuyết lớp nào mà lớp ấy CÓ
        # bậc thì lấy mục tiêu của chính bài ở bậc ấy — thà nói bằng lời của bài
        # còn hơn để trống một dòng trên màn thang. (4 chỗ: III.3.3 · III.3.4 ·
        # IV.2.2 · IV.3.1 đều khuyết lớp 3.)
        mo_ta = {k: v for k, v in (n.get('grade_content') or {}).items() if v}
        for b in thang:
            if str(b['lop']) not in mo_ta:
                thay = next((muc_tieu[i] for i in b['bai'] if muc_tieu.get(i)), None)
                if thay:
                    mo_ta[str(b['lop'])] = thay

        ma_cd = 'TOPIC:' + ma_pt[3:].rsplit('.', 1)[0]
        dang[ma_pt] = {
            'ten': ten_dang.get(ma_pt) or n['name'],
            'mang': n['area'], 'chuDe': ma_cd,
            'moTaLop': mo_ta,
            'soTruongHop': dict(muc[ma_pt]),
            'thang': thang,
        }

    # ── sửa tay đè lên tất cả
    for ma_pt, sua in tay.items():
        if ma_pt not in dang:
            canh_bao.append(f'chu_de_tay: "{ma_pt}" không phải dạng bài có thật')
            continue
        for lop_s, ds in (sua.get('themBac') or {}).items():
            ds = [x for x in ds if x in ten_bai]
            if not ds:
                continue
            lop = int(lop_s)
            cu = next((b for b in dang[ma_pt]['thang'] if b['lop'] == lop), None)
            if cu:
                cu['bai'] = sorted(dict.fromkeys(cu['bai'] + ds))
                cu['ten'] = [ten_bai[x] for x in cu['bai']]
                cu['canCu'] = 'tay'
            else:
                dang[ma_pt]['thang'].append(
                    {'lop': lop, 'bai': ds, 'ten': [ten_bai[x] for x in ds],
                     'canCu': 'tay'})
        dang[ma_pt]['thang'].sort(key=lambda b: b['lop'])

    chu_de = {}
    for ma_cd, n in top.items():
        ds = sorted((k for k, v in dang.items() if v['chuDe'] == ma_cd),
                    key=lambda k: [int(x) for x in k[3:].split('.')[1:]])
        chu_de[ma_cd] = {'ten': ten_cd.get(ma_cd) or n['name'],
                         'mang': n['area'], 'dang': ds}

    mang = {}
    for ma_m, n in area.items():
        ds = sorted((k for k, v in chu_de.items() if v['mang'] == n['area']),
                    key=lambda k: int(k[6:].split('.')[1]))
        mang[ma_m] = {'ten': n['name'], 'ma': n['area'], 'chuDe': ds}

    ra = {
        '_doc': ('Bản đồ chủ đề xuyên lớp — dựng bằng tools/dung_chu_de.py từ '
                 'data/km_v1_38.json + docs/Ma_tran_kien_thuc_Toan5_HSG_Cap4.xlsx. '
                 'KHÔNG sửa tay tệp này; sửa ở data/chu_de_tay.json rồi dựng lại.'),
        'nguon': 'km_v1_38 + Ma_tran_kien_thuc_Toan5_HSG_Cap4.xlsx',
        'mang': mang, 'chuDe': chu_de, 'dang': dang,
    }
    return ra, canh_bao


def main(chi_soat=False, in_tung=False):
    ra, canh_bao = dung()
    if not chi_soat:
        for d in (RA_GOC, RA_WEB):
            with open(d, 'w', encoding='utf-8') as f:
                json.dump(ra, f, ensure_ascii=False, indent=1, sort_keys=False)

    for c in canh_bao[:20]:
        print(f'  ⚠ {c}')

    dang = ra['dang']
    bac = collections.Counter(len(d['thang']) for d in dang.values())
    tong_bai = sum(len(b['bai']) for d in dang.values() for b in d['thang'])
    theo_lop = collections.Counter(b['lop'] for d in dang.values() for b in d['thang'])
    theo_cc = collections.Counter(b['canCu'] for d in dang.values() for b in d['thang'])
    xn = sum(1 for d in dang.values() for b in d['thang'] if b.get('sachXacNhan'))
    kb = os.path.getsize(RA_WEB) // 1024 if os.path.exists(RA_WEB) else 0

    print(f'bản đồ chủ đề: {len(ra["mang"])} mảng · {len(ra["chuDe"])} chủ đề · '
          f'{len(dang)} dạng bài · {tong_bai} mối nối bài · {kb} KB')
    for k in sorted(bac, reverse=True):
        print(f'  {k} bậc: {bac[k]:>3} dạng' + ('   ← có đường lùi' if k >= 2 else ''))
    print('  bậc theo lớp :', ' · '.join(f'lớp {l}: {n}' for l, n in sorted(theo_lop.items())))
    print('  căn cứ       :', ' · '.join(f'{k}: {v}' for k, v in theo_cc.most_common()))
    print(f'  trong đó {xn} bậc được CHÍNH SÁCH xác nhận là bài nền của bậc trên')

    # Lỗ hổng chương trình: ma trận đòi mà chưa quyển nào dạy. Không phải lỗi của
    # bộ dựng, nhưng phải in ra — im lặng thì bản đồ trông như phủ kín.
    trong = [(k, v['ten']) for k, v in dang.items() if not v['thang']]
    if trong:
        print(f'\n  {len(trong)} dạng bài ma trận có mà CHƯA QUYỂN NÀO DẠY:')
        for k, t in trong:
            print(f'      {k}  {t}')

    if in_tung:
        for ma_pt, d in dang.items():
            print(f'\n{ma_pt}  {d["ten"]}   [CB {d["soTruongHop"].get("CB",0)} · '
                  f'NC {d["soTruongHop"].get("NC",0)}]')
            for b in d['thang']:
                print(f'   lớp {b["lop"]} ({b["canCu"]}): ' +
                      ' | '.join(f'{i} {t[:44]}' for i, t in zip(b['bai'], b['ten'])))
    return canh_bao


if __name__ == '__main__':
    cb = main('--soat' in sys.argv, '--in' in sys.argv)
    raise SystemExit(1 if cb else 0)
