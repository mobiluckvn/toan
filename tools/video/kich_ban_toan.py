# -*- coding: utf-8 -*-
"""KỊCH BẢN VIDEO MÔN TOÁN — mở bài và bài giảng.

Bác chốt 14-08: *"phần Mở bài và bài giảng xây thành video và KHÔNG DÙNG ẨN DỤ, để
học sinh lần đầu xem video sẽ hiểu. Dùng cách tạo video như Tiếng Anh lớp 1."*

── VÌ SAO VIDEO ──
Cùng lý do đã đúng ở Tiếng Anh: chữ trên màn hình là kênh của người lớn. Bé 9–10
tuổi đọc được, nhưng đọc một màn 400 chữ về khái niệm mới thì bé lướt chứ không đọc.
Video thì bé NHẬN được — nghe tiếng, nhìn hình, mỗi lúc một ý.

── VÌ SAO LỜI ĐỌC PHẢI VIẾT RIÊNG, KHÔNG ĐỌC THẲNG BÀI ──
Chữ trong bài viết cho MẮT: có ngoặc, có dấu chấm phẩy ngăn dãy số, có chữ IN HOA
để nhấn. Đọc thẳng lên thì máy đọc "6 chấm phẩy 11 chấm phẩy 16". Nên mỗi cảnh khai
hai thứ tách nhau: `chu` là chữ HIỆN LÊN, `loi` là lời ĐỌC RA.

── KHÔNG ẨN DỤ, VÀ ĐÂY LÀ LUẬT CÓ CỔNG CANH ──
Quyển lớp 4 vốn gói bài toán trong lớp vỏ nhân vật: người giải là "kỹ sư", cách làm
là "tuyệt kỹ", dấu hiệu chia hết là "mật mã". `de_hieu_lop4.py` đã bóc vỏ ấy khi
dựng bài. Video thì tuyệt đối không được để nó mọc lại: bé xem video là để HIỂU
KHÁI NIỆM, mà mỗi ẩn dụ là một lớp bé phải bóc trước khi tới được cái cần học.

Danh sách cấm ở `TU_CAM` gồm cả những chữ CHÍNH CHÁU đã viết trong bài — "bước chân",
"dấu vân tay của dãy" — vì chúng cũng là ẩn dụ, chỉ là ẩn dụ dễ thương hơn.

── DỰNG TỪ ĐÂU ──
Đọc bản GỐC `data/lop4/DL_KSN4_B*.json` (10 mục ①…⑩), lấy hai mục:
    ② chuyenMoBai  → cảnh `de_toan` + `hinh_toan`
    ④ khamPha      → mỗi bước một cảnh `y_toan`
Hình lấy đúng tệp PNG màn hình đang dùng, không vẽ bản thứ hai.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent.parent
NGUON = GOC / 'data' / 'lop4'
HINH = GOC / 'web' / 'public' / 'content' / 'figures'
SO_TAY_HINH = GOC / 'data' / 'lop4_hinh_manifest.json'

# Chữ nào lọt vào LỜI ĐỌC là hỏng đúng cái bác dặn. Gồm hai nhóm: vỏ nhân vật của
# quyển, và mấy ví von chính cháu đã viết khi soạn năm bài dãy số.
TU_CAM = re.compile(
    r'\b(kỹ sư|xưởng|thám tử|tuyệt kỹ|vũ khí|bí kíp|thần chú|mật mã|mật thư|hoa tiêu|'
    r'quan tòa|cao thủ|đơn hàng|Su Kem|Trí Long|bước chân|dấu vân tay|'
    r'người giải|mở khoá|chìa khoá|vũ trụ|không gian toán)\b', re.I)


def doc_duoc(s: str) -> str:
    """Chữ đem ĐỌC. Bỏ những thứ chỉ có nghĩa với mắt.

    Dấu `;` ngăn số hạng trong dãy đọc lên thành "chấm phẩy"; ngoặc kép thành khoảng
    lặng; `×` `:` `−` phải đọc thành lời. Không làm bước này thì clip nghe như máy
    đánh vần ký hiệu."""
    s = str(s or '')
    s = re.sub(r'\s*;\s*', ', ', s)
    s = s.replace('“', '').replace('”', '').replace('"', '')
    s = s.replace('—', ',').replace('–', ',')
    s = re.sub(r'\s*×\s*', ' nhân ', s)
    s = re.sub(r'\s*÷\s*', ' chia ', s)
    s = re.sub(r'(\d)\s*:\s*(\d)', r'\1 chia \2', s)
    s = s.replace('−', ' trừ ').replace(' - ', ' trừ ')
    s = re.sub(r'\s*\+\s*', ' cộng ', s)
    s = re.sub(r'\s*=\s*', ' bằng ', s)
    s = re.sub(r'\.\.\.', ' và cứ thế ', s)
    s = re.sub(r'\s+', ' ', s)
    # Dọn dấu câu bị hở sau khi thay: "LÀ GÌ , CHỖ" ← từ gạch dài `—`.
    # Kokoro đọc khoảng lặng ở chỗ hở ấy, nghe như máy vấp.
    s = re.sub(r'\s+([,.])', r'\1', s)
    s = re.sub(r'([,.])(?=\S)', r'\1 ', s)
    return re.sub(r'\s+', ' ', s).strip()


def _canh(loai, chu='', phu='', loi=None, **k):
    """Một cảnh. `loi` là danh sách câu TIẾNG VIỆT sẽ đọc; mã clip suy ra từ chữ,
    không gõ tay — cùng luật với `kich_ban.py` của Tiếng Anh (hai chỗ tính một thứ
    thì sớm muộn lệch)."""
    loi = [doc_duoc(x) for x in (loi or []) if str(x).strip()]
    return {'loai': loai, 'chuChinh': chu, 'chuPhu': phu,
            'loiAm': [[x, 'vi'] for x in loi],
            'am': [ma_am(x) for x in loi], **k}


def ma_am(chu: str) -> str:
    sach = ''.join(c if c.isalnum() else '_' for c in chu.lower()).strip('_')
    return f'loi_{sach}'[:60]


def _cau_dau(s: str, n: int = 2) -> str:
    """n câu đầu của một đoạn — màn hình chỉ hiện chừng ấy, phần còn lại để lời đọc."""
    cau = re.split(r'(?<=[.!?])\s+', str(s or '').strip())
    return ' '.join(cau[:n])


def _hinh_cua(bai_id: str, muc: str) -> str | None:
    so = json.loads(SO_TAY_HINH.read_text('utf8'))
    for k, v in so.items():
        if v.get('bai') == bai_id and v.get('muc') == muc:
            p = HINH / f'{k}.png'
            return str(p) if p.exists() else None
    return None


def canh_cua(bai: dict) -> list[dict]:
    ten = re.sub(r'^Bài \d+ · ', '', bai['ten'])
    mo = bai['muc']['chuyenMoBai']['dong']
    buoc = [d for d in bai['muc']['khamPha']['dong']
            if not d.startswith('MẸO')]      # dòng mẹo là tóm tắt, không phải bước
    ds = []

    # ── 1 · BÌA ──
    ds.append(_canh('bia', ten, f"Bài {bai['so']} · {bai['tenChuong']}",
                    loi=[f"Bài {bai['so']}. {ten}."]))

    # ── 2 · ĐỀ BÀI ──
    # Đọc TRỌN phần mở bài, nhưng chữ trên màn chỉ hai câu đầu — đọc hết một màn
    # 400 chữ thì bé nhìn chữ chứ không nghe.
    ds.append(_canh('de_toan', _cau_dau(' '.join(mo[:2])),
                    'Con nghe kỹ đề trước đã nhé.', loi=[' '.join(mo)]))

    # ── 3 · HÌNH CỦA ĐỀ ──
    tep = _hinh_cua(bai['id'], 'chuyenMoBai')
    if tep:
        ds.append(_canh('hinh_toan', 'Con nhìn hình rồi nghĩ thử xem.',
                        tepHinh=tep, loi=['Con nhìn hình này, rồi thử nghĩ xem làm thế nào.']))

    # ── 4 · TỪNG BƯỚC GIẢNG ──
    for i, d in enumerate(buoc, 1):
        # "Bước 1 — DÃY SỐ LÀ GÌ. Một dãy số là…" → nhan = "DÃY SỐ LÀ GÌ"
        m = re.match(r'^Bước \d+\s*[—-]\s*([^.]+)\.\s*(.*)$', d)
        nhan, than = (m.group(1).strip(), m.group(2).strip()) if m else ('', d)
        ds.append(_canh('y_toan', nhan or _cau_dau(than, 1), _cau_dau(than, 1) if nhan else '',
                        buoc=i, soBuoc=len(buoc), loi=[than or d]))

    # ── 5 · CHỐT ──
    ds.append(_canh('ket', 'Con hiểu rồi đấy!',
                    'Bây giờ mình cùng làm bài nhé.',
                    loi=['Con hiểu rồi đấy. Bây giờ mình cùng làm bài nhé.']))
    return ds


def soi(ds: list[dict], bai_id: str) -> list[str]:
    """Không ẩn dụ, và không câu nào dài quá sức một hơi đọc."""
    loi = []
    for c in ds:
        for chu, _ in c['loiAm']:
            m = TU_CAM.search(chu)
            if m:
                loi.append(f'{bai_id} · {c["loai"]}: lời đọc có ẩn dụ "{m.group(0)}"')
            if len(chu) > 420:
                loi.append(f'{bai_id} · {c["loai"]}: câu đọc dài {len(chu)} chữ')
        if TU_CAM.search(c['chuChinh'] + ' ' + c['chuPhu']):
            loi.append(f'{bai_id} · {c["loai"]}: chữ trên màn có ẩn dụ')
    return loi


def kich_ban(ma: str) -> dict:
    bai = json.loads((NGUON / f'{ma}.json').read_text('utf8'))
    ds = canh_cua(bai)
    xau = soi(ds, bai['id'])
    if xau:
        raise SystemExit('\n'.join('  ✗ ' + x for x in xau))
    return {'bai': bai['id'], 'tep': f'{ma}_giang.mp4', 'canh': ds}
