# -*- coding: utf-8 -*-
"""
LỚP 2 · BƯỚC 4 — gắn hình đã vẽ vào bài học.

    python3 tools/gan_hinh_lop2.py

PHẢI chạy SAU chuan_lop2.py, và đây là bước CUỐI của dây chuyền. Lý do: chuan_lop2
ghi đè trọn tệp bài học, nên gắn hình trước nó là mất sạch hình — dữ liệu vẫn hợp
lệ, bài vẫn chạy, chỉ là không còn hình nào và KHÔNG CÓ GÌ BÁO. Đúng lỗi đã dính
ở Quyển 2 lớp 5.

Neo hình theo THỨ TỰ BƯỚC, không theo nguyên văn dòng: `neoBuoc: 2` nghĩa là hình
đứng ngay sau dòng "Bước 2." (hoặc "Nhịp 2.", "Vũ khí 2 —" — sách không nhất quán).
`neoBuoc: 0` là hình đứng ở đầu mục, trước mọi bước.

Vì sao không neo theo nguyên văn: lời văn đã được VIẾT LẠI cho dễ hiểu ở bước 2,
nên so nguyên văn với sách là trượt hết. Số thứ tự bước thì không đổi.

Không tìm đủ bước là DỪNG HẲN, không bỏ qua im lặng: thả hình xuống cuối mục thì
hình đứng lạc chỗ, đọc vào không hiểu tại sao.
"""
import hashlib, json, os, re, sys

# Sách không nhất quán tên bước: Bước / Nhịp / Vũ khí / Chặng
R_BUOC = re.compile(r'^(Bước|Nhịp|Vũ khí|Chặng)\s*\d+\s*[.—–-]')

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SO_TAY = os.path.join(GOC_KHO, 'data', 'lop2_hinh_manifest.json')
RA_DIR = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lop2')
RA_DATA = os.path.join(GOC_KHO, 'data', 'lop2')
HINH_DIR = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')


def main():
    if not os.path.exists(SO_TAY):
        sys.exit('chưa có sổ tay hình — chạy `python3 tools/ve_hinh_lop2.py` trước')
    so_tay = json.load(open(SO_TAY, encoding='utf-8'))

    # gom theo bài
    theo_bai = {}
    for hid, h in sorted(so_tay.items()):
        theo_bai.setdefault(h['bai'], []).append({'id': hid, **h})

    loi, gan = [], 0
    for bai_id, ds in sorted(theo_bai.items()):
        ten = bai_id.replace('DL:', 'DL_').replace('.', '_') + '.json'
        duong = os.path.join(RA_DATA, ten)
        if not os.path.exists(duong):
            loi.append(f'{bai_id}: không có tệp bài học {ten}')
            continue
        d = json.load(open(duong, encoding='utf-8'))

        for h in ds:
            # ảnh phải có thật và đúng bản đã ghi sổ
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
                                    'caption': h['caption'], 'sha256_16': h['sha256_16']})
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
                           f"{can} bước — sửa neoBuoc trong data/lop2_hinh.json")
                continue

            muc.setdefault('hinh', [])
            muc['hinh'] = [x for x in muc['hinh'] if x['id'] != h['id']]
            muc['hinh'].append({'id': h['id'], 'sauDong': vt, 'file': h['file'],
                                'caption': h['caption'], 'sha256_16': h['sha256_16']})
            muc['hinh'].sort(key=lambda x: (x['sauDong'], x['id']))
            gan += 1

        with open(os.path.join(RA_DATA, ten), 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)

    for m in loi:
        print('  ✗', m)
    if loi:
        sys.exit(f'\nDỪNG: {len(loi)} hình không gắn được — sửa xong chạy lại')
    print(f'gắn {gan} hình vào {len(theo_bai)} bài')


if __name__ == '__main__':
    main()
