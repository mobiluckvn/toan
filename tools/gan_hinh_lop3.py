# -*- coding: utf-8 -*-
"""
LỚP 3 · BƯỚC 4 — gắn hình đã vẽ vào bài học.

    python3 tools/gan_hinh_lop3.py

PHẢI chạy SAU `chuan_lop3.py`, và đây là bước CUỐI của dây chuyền. Lý do: chuan_lop3
ghi đè trọn tệp bài học, nên gắn hình trước nó là mất sạch hình — dữ liệu vẫn hợp lệ,
bài vẫn chạy, chỉ là không còn hình nào và KHÔNG CÓ GÌ BÁO. Đúng lỗi đã dính ở Quyển
2 lớp 5, rồi lớp 2 dính lại.

Neo hình theo THỨ TỰ BƯỚC, không theo nguyên văn dòng: `neoBuoc: 2` nghĩa là hình
đứng ngay sau dòng bước thứ hai. `neoBuoc: 0` là hình đứng đầu mục.

── SÁCH LỚP 3 ĐẶT TÊN BƯỚC MƯỜI KIỂU ──

Lớp 2 có bốn: Bước · Nhịp · Vũ khí · Chặng. Lớp 3 có thêm sáu nữa, và chúng KHÔNG
hiếm — bài 29 (hình tròn) đặt cả ba bước giảng là "Nhân vật 1/2/3", bài 23 (giả thiết
tạm) dùng "Nhịp", bài 26 dùng "Phép thử". Đem mẫu lớp 2 sang thì 26 bước ở nhiều bài
biến mất, mà biến mất thì im lặng: bài vẫn dựng ra, chỉ là chặng giảng trống trơn.

Nên tệp này KHÔNG đoán bằng mẫu rộng ("mấy chữ rồi tới số"), mà liệt kê đích danh —
rồi CANH: bài nào có mục khám phá mà không nhận ra bước nào thì kêu lên. Thêm một
cách đặt tên mới là phép canh ấy đỏ ngay, chứ không phải chờ người đọc phát hiện.
"""
import hashlib, json, os, re, sys

# Mười cách sách lớp 3 đặt tên một bước giảng (khảo sát trên cả 34 bài).
TEN_BUOC = ('Bước', 'Nhịp', 'Vũ khí', 'Chặng', 'Phép thử', 'Chiêu', 'Đường',
            'Tuyệt kỹ', 'Kho báu', 'Thế trận', 'Nhân vật', 'Câu hỏi')
R_BUOC = re.compile(r'^(?:' + '|'.join(TEN_BUOC) + r')\s*\d+\s*[.—–-]')

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop3_hinh_manifest.json')
RA_DATA = os.path.join(GOC_KHO, 'data', 'lop3')
THO = os.path.join(GOC_KHO, 'data', 'lop3_tho.json')
HINH_DIR = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')


def canh_ten_buoc():
    """Bài nào có mục khám phá mà không nhận ra bước nào → sách đặt tên kiểu mới."""
    d = json.load(open(THO, encoding='utf-8'))
    lo = []
    for b in d['bai']:
        dong = b['muc']['khamPha'].get('dong') or []
        if dong and not any(R_BUOC.match(x) for x in dong):
            dau = next((x[:52] for x in dong if not x.startswith(('MẸO', 'LUẬT'))), '')
            lo.append(f'Bài {b["so"]}: không nhận ra bước nào — dòng đầu là "{dau}…"')
    return lo


def main():
    if not os.path.exists(SO_TAY):
        sys.exit('chưa có sổ tay hình — chạy `python3 tools/ve_hinh_lop3.py` trước')
    so_tay = json.load(open(SO_TAY, encoding='utf-8'))

    for x in canh_ten_buoc():
        print(f'  ⚠ {x}')

    theo_bai = {}
    for hid, h in sorted(so_tay.items()):
        theo_bai.setdefault(h['bai'], []).append({'id': hid, **h})

    # Hình đã VẼ nhưng chưa có chỗ đặt. Bỏ qua nhưng phải NÓI RA — im lặng bỏ qua
    # thì lần sau tưởng đã gắn rồi.
    for k, v in sorted((k, v) for k, v in so_tay.items() if v.get('hoan')):
        print(f"  ⏸ {k}: {v['hoan']}")
    theo_bai = {b: [x for x in ds if not x.get('hoan') and not x.get('onTap')]
                for b, ds in theo_bai.items()}
    theo_bai = {b: ds for b, ds in theo_bai.items() if ds}

    loi, gan = [], 0
    for bai_id, ds in sorted(theo_bai.items()):
        ten = bai_id.replace('DL:', 'DL_').replace('.', '_') + '.json'
        duong = os.path.join(RA_DATA, ten)
        if not os.path.exists(duong):
            loi.append(f'{bai_id}: không có tệp bài học {ten}')
            continue
        d = json.load(open(duong, encoding='utf-8'))

        for h in ds:
            # ảnh phải có thật và đúng bản đã ghi sổ — sửa params mà quên vẽ lại thì
            # dữ liệu nói một đằng, ảnh hiện một nẻo, và cả hai đều hợp lệ (bẫy 20)
            png = os.path.join(HINH_DIR, os.path.basename(h['file']))
            if not os.path.exists(png):
                loi.append(f"{h['id']}: thiếu ảnh {h['file']}")
                continue
            sha = hashlib.sha256(open(png, 'rb').read()).hexdigest()[:16]
            if sha != h['sha256_16']:
                loi.append(f"{h['id']}: ảnh lệch sổ tay ({sha} ≠ {h['sha256_16']}) — vẽ lại")
                continue

            muc = d['muc'].get(h['muc'])
            if not muc:
                loi.append(f"{h['id']}: bài {bai_id} không có mục {h['muc']}")
                continue

            # Hình của riêng một CÂU HỎI (đề nằm trong hình) — neo theo mã câu chứ
            # không theo dòng: mục luyện tập không còn dòng nào, câu đã tách riêng.
            if h.get('neoCau'):
                if not any(c['id'] == h['neoCau'] and c['phan'] == h['muc'] for c in d['cau']):
                    loi.append(f"{h['id']}: {bai_id} không có câu {h['neoCau']} ở mục {h['muc']}")
                    continue
                muc.setdefault('hinh', [])
                muc['hinh'] = [x for x in muc['hinh'] if x['id'] != h['id']]
                muc['hinh'].append({'id': h['id'], 'cau': h['neoCau'], 'file': h['file'],
                                    'caption': h['caption'], 'sha256_16': h['sha256_16'],
                                    'vaiTro': h.get('vaiTro')})
                gan += 1
                continue

            dong = muc.get('dong') or []
            can = int(h.get('neoBuoc', 0))
            if can == 0:
                vt = 0 if dong else None
            else:
                moc = [k for k, s in enumerate(dong) if R_BUOC.match(str(s))]
                vt = moc[can - 1] if len(moc) >= can else None
            if vt is None:
                loi.append(f"{h['id']}: mục {h['muc']} của {bai_id} không có đủ "
                           f"{can} bước — sửa neoBuoc trong data/lop3_hinh.json")
                continue

            muc.setdefault('hinh', [])
            muc['hinh'] = [x for x in muc['hinh'] if x['id'] != h['id']]
            muc['hinh'].append({'id': h['id'], 'sauDong': vt, 'file': h['file'],
                                'caption': h['caption'], 'sha256_16': h['sha256_16']})
            muc['hinh'].sort(key=lambda x: (x['sauDong'], x['id']))
            gan += 1

        with open(duong, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)

    for m in loi:
        print('  ✗', m)
    if loi:
        sys.exit(f'\nDỪNG: {len(loi)} hình không gắn được — sửa xong chạy lại')
    print(f'gắn {gan} hình vào {len(theo_bai)} bài')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
