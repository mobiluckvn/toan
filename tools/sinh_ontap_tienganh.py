#!/usr/bin/env python3
"""
DỰNG ĐỀ ÔN TẬP CHƯƠNG — Tiếng Anh lớp 1.

`ta1/ontap.json` từ trước tới nay chỉ là DANH MỤC: khai có 4 kỳ, mỗi kỳ 10 câu,
cần 8 câu đúng. Không có câu nào thật. Nên màn kỳ ôn tập không dựng được, huy hiệu
chương treo mãi, và `hocBaTA` rỗng.

── VÌ SAO KHÔNG SINH CÂU MỚI ──
Câu mới thì phải có clip mới và hình mới, tức là chạy lại cả dây chuyền TTS. Mà
kỳ ôn tập theo đúng nghĩa của nó KHÔNG nên có gì mới: nó hỏi lại đúng những thứ
bốn unit vừa dạy. Nên đề lấy thẳng từ câu ĐÃ SINH của bốn unit trong chương —
âm có sẵn, hình có sẵn, và bé gặp lại đúng thứ mình đã học.

── ĐỀ GỒM GÌ ──
Hai dạng, và chỉ hai, vì cả hai đều KHÔNG BẮT ĐỌC:
    nghe → bấm hình đúng      (lấy từ pool `warmup` bậc 1)
    nghe → nhìn hình → đúng/sai  (lấy từ `assessment`)
Mỗi unit góp một câu mỗi dạng → 4 unit × 2 = 8, rồi thêm 2 câu nữa cho tròn 10.

── KHÔNG DÙNG RANDOM ──
Chạy hai lần phải ra một đề. Bé làm lại kỳ ôn tập mà đề đổi thì không so được
lần này với lần trước, và bố mẹ cũng không biết con tiến bộ ở đâu.
"""
import json
import os
import sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SO_CAU = 10

# Quyển nào — nhận `--lop N`, mặc định lớp 1 để lệnh cũ trong sổ vẫn chạy.
# Bản đầu ghim cứng 'ta1' ở ba chỗ; thêm quyển lớp 2 là phải sửa cả ba, mà sót một
# chỗ thì bộ dựng đọc bài lớp 2 rồi ghi đè đề ôn tập của lớp 1 — hỏng câm.
LOP = 1
for _i, _a in enumerate(sys.argv):
    if _a == '--lop' and _i + 1 < len(sys.argv):
        LOP = int(sys.argv[_i + 1])
THU_MUC = os.path.join(GOC, 'web', 'public', 'content', f'ta{LOP}')
TEP = os.path.join(THU_MUC, 'ontap.json')
TIEN_TO_BAI = f'DL_TA{LOP}_B'


def nap_bai():
    """16 bài đã sinh, gom theo chương. Chương lấy từ CHÍNH bài, không từ `_gom`."""
    theo_chuong = {}
    for ten in sorted(os.listdir(THU_MUC)):
        if not ten.startswith(TIEN_TO_BAI) or not ten.endswith('.json'):
            continue
        with open(os.path.join(THU_MUC, ten), encoding='utf-8') as f:
            b = json.load(f)
        theo_chuong.setdefault(b['chuong'], []).append(b)
    return theo_chuong


def cau_chon_hinh(bai, n):
    """Câu 'nghe rồi bấm hình đúng' thứ n của bài. Chỉ lấy câu có đủ hình nút."""
    ds = [c for c in bai['practice']['pools'].get('warmup', [])
          if c.get('anhChon') and c.get('choices') and c.get('am')]
    return ds[n % len(ds)] if ds else None


def cau_dung_sai(bai, n, muon_dung):
    """
    Câu nghe–nhìn đúng/sai. `muon_dung` để đề có cả câu ĐÚNG và câu SAI xen kẽ.

    Đề toàn câu đúng thì bé bấm ✓ suốt cũng 10/10 — con số ấy không nói lên gì.
    """
    ds = [c for c in bai['assessment']['items']
          if c.get('nhinNghe') and c.get('am')]
    hop = [c for c in ds if c['answerKey']['value'] is muon_dung] or ds
    return hop[n % len(hop)] if hop else None


def dung_ky(so, bais):
    """Một kỳ ôn tập: 10 câu, rải đều bốn unit, hai dạng xen kẽ."""
    cau, da_co = [], set()

    def them(c, tu_bai):
        if not c:
            return False
        # Mã phải DUY NHẤT trong đề: hai unit đều có câu "C1", trùng mã thì React
        # dùng chung `key` và giữ nguyên state khi sang câu mới — đúng cái lỗi đã
        # làm trắng màn hình giữa bài một lần rồi.
        ma = f"K{so}_{tu_bai['id'].split('.')[-1]}_{c['id']}"
        if ma in da_co:
            return False
        da_co.add(ma)
        cau.append({**c, 'id': ma, 'tuBai': tu_bai['id'], 'tenBai': tu_bai['title']})
        return True

    # Vòng 1 — mỗi unit góp một câu chọn hình và một câu đúng/sai.
    for i, b in enumerate(bais):
        them(cau_chon_hinh(b, 0), b)
        them(cau_dung_sai(b, 0, i % 2 == 0), b)

    # Vòng 2 — bù cho tròn 10, quay lại lấy câu KHÁC của cùng những unit ấy.
    n = 1
    while len(cau) < SO_CAU and n < 8:
        for i, b in enumerate(bais):
            if len(cau) >= SO_CAU:
                break
            them(cau_dung_sai(b, n, (i + n) % 2 == 0), b) or them(cau_chon_hinh(b, n), b)
        n += 1

    return cau[:SO_CAU]


def main():
    theo_chuong = nap_bai()
    if not theo_chuong:
        sys.exit(f'Không thấy bài nào trong {THU_MUC}')

    with open(TEP, encoding='utf-8') as f:
        danh_muc = json.load(f)

    for ky in danh_muc:
        bais = sorted(theo_chuong.get(ky['chapter'], []), key=lambda b: b['id'])
        cau = dung_ky(ky['so'], bais)
        ky['cau'] = cau
        ky['soCau'] = len(cau)
        # `need` khai sẵn là 8/10. Đề hụt câu thì phải hạ theo, không thì kỳ ôn
        # tập thành không bao giờ qua được mà chẳng ai hiểu vì sao.
        ky['need'] = min(ky.get('need', 8), max(1, round(len(cau) * 0.8)))
        ky['tuBai'] = [b['id'] for b in bais]
        dung = sum(1 for c in cau if c.get('answerKey', {}).get('value') is True)
        print(f"  Kỳ {ky['so']} · chương {ky['chapter']}: {len(cau)} câu "
              f"· {len(bais)} unit · cần {ky['need']} · {dung} câu đáp ĐÚNG")

    with open(TEP, 'w', encoding='utf-8') as f:
        json.dump(danh_muc, f, ensure_ascii=False, indent=1)
    print(f"\nĐã ghi {TEP}")


if __name__ == '__main__':
    main()
