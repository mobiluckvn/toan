# -*- coding: utf-8 -*-
"""
LỚP 4 · BƯỚC 2c — bóc 11 kỳ ôn tập: đề chính · BẢNG TỰ SOI · đề B.

    python3 tools/rut_lop4.py && python3 tools/dapan_lop4.py && python3 tools/ontap_lop4.py

Nguồn là `sauBai` của bài cuối mỗi chương (bước 1 đã cất riêng).

**ĐỌC CẤU TRÚC, ĐỪNG DÒ TỪNG DÒNG.** Bài học đắt nhất của lớp 3: mỗi ôn tập luôn có
ba phần ngăn bởi mốc `✦`, và ở phần nào thì chỉ dùng mẫu của phần ấy —

    thân đề  →  ✦ BẢNG TỰ SOI  →  ✦ ĐỀ B  →  ✦ SỔ ĐƠN HÀNG

Làm thế thì dòng mối nối hết cửa rơi xuống thành câu hỏi: mẫu trượt thì MẤT mối nối
và bộ đếm kêu, chứ không đẻ ra câu hỏi ma như lượt lớp 3 đầu tiên (5/8 ôn tập thừa
1-5 câu, và ba hỏng câm đi kèm mà không phép đếm nào bắt được).

BẢNG TỰ SOI của lớp 4 nằm gọn trong MỘT ô bảng, các mối nối viết nối đuôi nhau, và
có **năm dạng** — mẫu chỉ biết dạng đầu là mất mối nối lặng lẽ:

    Câu 1, 2, 3 → thuộc Bài 1 (…)          ← chuẩn
    Câu 1, 2, 3 và Câu 12 → thuộc Bài 5    ← có chữ "và"
    Câu 12 → Bài 19 mức ★★★ (…)            ← KHÔNG có chữ "thuộc"
    Câu 10 → ghép Bài 9 + Bài 10           ← HAI bài
    Câu 10 → tổng hợp cả chương (…)        ← KHÔNG bài nào → canCu 'chuong'

Nên `veCau` là **danh sách** mã bài, không phải một mã. Chốt bắt buộc: mọi câu 1..N
đều phải có mối nối — thiếu một câu là dừng.
"""
import json, os, re

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THO = os.path.join(GOC_KHO, 'data', 'lop4_tho.json')
DAP = os.path.join(GOC_KHO, 'data', 'lop4_dapan.json')
RA = os.path.join(GOC_KHO, 'data', 'lop4_ontap.json')
TIEN_TO = 'DL:KSN4.'

R_OT = re.compile(r'^ÔN TẬP (\d+)\s*·\s*(.+)$')
# Ngưỡng đạt nhận theo HÌNH DẠNG `a/b`, không liệt kê động từ — liệt kê thì sót, và
# sót lặng lẽ (lớp 3: hai ôn tập tụt về mặc định 10 trong khi sách nói 12).
R_NGUONG = re.compile(r'(\d+)\s*/\s*(\d+)')
R_CAU = re.compile(r'^Câu (\d+)\s*[.:]\s*(.+)$')
R_DEB = re.compile(r'^B(\d+)\s*[.:]\s*(.+)$')
R_MOC = re.compile(r'^✦\s*(.+)$')
R_NOI = re.compile(r'Câu\s*([\d,\s]+(?:và\s*Câu\s*[\d,\s]+)*)→\s*([^.]+?)(?=\.\s|\.$|$)')


def ma_bai(so):
    return f'{TIEN_TO}B{so:02d}'


# ═══════════════════════════════════════════════════════════════════════════
# SỐ BÀI CỦA SÁCH ĐÃ CHẾT — ĐỪNG SUY MÃ BÀI TỪ NÓ NỮA
# ═══════════════════════════════════════════════════════════════════════════
# `ma_bai()` đổi số bài của SÁCH thành mã bài, và hồi sách còn đúng 44 bài thì hai
# thứ ấy trùng nhau. Nay không còn trùng nữa: mỗi đợt làm video lại tách một bài
# sách thành mấy bài app, mã mới lấy số mới (B50 trở lên) còn số hiển thị thì suy
# từ `thu_tu.json` — xem lối C.
#
# ⚠ CHẠY LẠI TỆP NÀY TỪNG XOÁ MỐI NỐI CỦA 102 CÂU Ở CHÍN CHƯƠNG mà không kêu một
# tiếng: "Bài 42" của sách bị đổi thành B42, trong khi bài ấy nay mang mã B47. Câu
# ôn tập về quãng đường sẽ dẫn bé sang bài phân số để ôn lại. Cả hai đầu đều hợp
# lệ, chỉ chỗ nối là sai — không phép kiểm nào bắt được.
#
# Nên nay mối nối GIỮ LẠI từ bản đã dựng, và chỗ nào cần đổi thì khai đích danh ở
# đây. Sách chỉ còn là đường lui cuối cùng cho câu chưa từng có mối nối.
KHAI_TAY = {
    # ── chương 10 đợt hai: B45 tách làm bốn, B46 tách làm hai ──
    # Bài 45 cũ gộp góc, đường cao, cắt ghép và hình tròn; nay bốn bài riêng, nên
    # câu nào hỏi gì thì trỏ về đúng bài ấy.
    (10, 8): {'ve': ['DL:KSN4.B80']},                       # bán kính, đường kính
    (10, 9): {'ve': ['DL:KSN4.B79']},                       # cắt chéo tấm tôn
    (10, 10): {'ve': ['DL:KSN4.B81']},                      # đếm khối theo tầng
    (10, 11): {'ve': ['DL:KSN4.B46']},                      # sáu mặt của hộp
    (10, 12): {'ve': ['DL:KSN4.B81']},                      # tháp ba tầng khác cỡ
    # ── chương 1: B01 tách làm ba, B02 làm hai, B03 làm hai ──
    (1, 3): {'ve': ['DL:KSN4.B82']},                        # giá trị chữ số
    (1, 6): {'ve': ['DL:KSN4.B03']},                        # thiếu một chữ số 0
    (1, 7): {'ve': ['DL:KSN4.B85']},                        # xoá chữ số tận cùng
    (1, 9): {'ve': ['DL:KSN4.B85']},                        # xoá tận cùng, bài ngược
    (1, 10): {'ve': ['DL:KSN4.B04', 'DL:KSN4.B83']},        # tráo + bảng liệt kê
    # Câu 2 cũ hỏi lại đúng ý câu 1 (vẫn là đọc và viết số), trong khi bài THÊM BÊN
    # TRÁI VÀ XEN VÀO GIỮA không có câu nào hỏi tới. Viết lại câu 2 cho phủ bài ấy.
    (1, 2): {'ve': ['DL:KSN4.B84'],
             'text': 'Thêm chữ số 4 vào bên trái số 75 thì số tăng thêm bao nhiêu? '
                     'Còn xen chữ số 0 vào giữa số 84 thì số tăng thêm bao nhiêu?'},

    # ── chương 2: mỗi mẹo tính nhanh nay một bài riêng ──
    (2, 2): {'ve': ['DL:KSN4.B86']},                        # nhẩm với 25
    (2, 3): {'ve': ['DL:KSN4.B87']},                        # nhẩm với 11
    (2, 4): {'ve': ['DL:KSN4.B89']},                        # bóc ngoặc
    (2, 6): {'ve': ['DL:KSN4.B90']},                        # X trong chia có dư
    (2, 8): {'ve': ['DL:KSN4.B91']},                        # đếm chữ số trang
    (2, 11): {'ve': ['DL:KSN4.B91']},                       # bài ngược đếm chữ số
    (2, 12): {'ve': ['DL:KSN4.B88', 'DL:KSN4.B87']},        # thừa số 0 ẩn + nhẩm 11
    # Câu 9 cũ hỏi lại đúng ý câu 7 (vẫn đếm dãy cách đều), còn bài ĐẾM BẰNG PHẦN BÙ
    # không có câu nào hỏi tới. Viết lại câu 9 cho phủ bài ấy.
    (2, 9): {'ve': ['DL:KSN4.B92'],
             'text': 'Có bao nhiêu số có ba chữ số mà trong đó có chứa chữ số 0? '
                     'Hãy đếm phần không chứa chữ số 0 trước.'},

    # ── chương 11: B47 tách làm ba, B48 làm hai ──
    (11, 2): {'ve': ['DL:KSN4.B93']},                       # chiều xuôi
    (11, 3): {'ve': ['DL:KSN4.B93']},                       # chiều ngược
    (11, 4): {'ve': ['DL:KSN4.B94']},                       # so hai xe
    (11, 7): {'ve': ['DL:KSN4.B95']},                       # gặp nhau
    (11, 8): {'ve': ['DL:KSN4.B95']},                       # gặp nhau, hỏi chỗ gặp
    (11, 12): {'ve': ['DL:KSN4.B95', 'DL:KSN4.B93']},       # gặp nhau + giờ đến

    # Câu 7 cũ hỏi lại đúng ý của câu 6 (cùng chu vi thì diện tích khác nhau), nên
    # cả hai cùng trỏ về một bài — trong khi HAI bài mới của đợt này, bốn loại góc
    # và đường cao, không có câu nào hỏi tới. Viết lại câu 7 để phủ cả hai.
    (10, 7): {'ve': ['DL:KSN4.B45', 'DL:KSN4.B78'],
              'text': 'Áp ê ke vào góc đỉnh của tấm mái tam giác thì thấy cạnh góc '
                      'xoè rộng ra ngoài ê ke. Góc ấy tên là gì? Và muốn dựng cột '
                      'chống từ đỉnh mái xuống nền cho đúng thì cột phải hợp với '
                      'nền một góc gì?'},
}


def _tach_moi_noi(chu, bai_cua_chuong):
    """BẢNG TỰ SOI → {số câu: [mã bài, …]} + căn cứ từng câu."""
    ve, can = {}, {}
    for m in R_NOI.finditer(chu.replace('→', '→')):
        sos = [int(x) for x in re.findall(r'\d+', m.group(1))]
        dich = m.group(2)
        bai = [int(x) for x in re.findall(r'Bài (\d+)', dich)]
        for s in sos:
            if bai:
                ve[s] = [ma_bai(x) for x in bai]
                can[s] = 'sach'
            else:
                # "tổng hợp cả chương" — có thật, không phải lỗi mẫu. Trỏ về đủ các
                # bài của chương, và nói rõ căn cứ để sau này không ai tưởng là sót.
                ve[s] = [ma_bai(x) for x in bai_cua_chuong]
                can[s] = 'chuong'
    return ve, can


def main():
    tho = json.load(open(THO, encoding='utf-8'))
    dap = json.load(open(DAP, encoding='utf-8'))['dapAn']
    bai_theo_chuong = {}
    for b in tho['bai']:
        bai_theo_chuong.setdefault(b['chuong'], []).append(b['so'])

    # Bản đã dựng lần trước — đọc để GIỮ LẠI mối nối, xem KHAI_TAY.
    da_co, da_co_B = {}, {}
    if os.path.exists(RA):
        for k in json.load(open(RA, encoding='utf-8'))['ky']:
            for q in k['examA']:
                da_co[(k['so'], q['qno'])] = q
            da_co_B[k['so']] = {q['qno']: q for q in k['deB']}
    n_tay = n_giu = n_sach = 0
    ky = []
    for b in tho['bai']:
        if not b['sauBai']:
            continue
        dong = b['sauBai']
        # ── tìm đầu ôn tập ──
        i = next((k for k, t in enumerate(dong) if R_OT.match(t)), None)
        if i is None:
            continue
        m = R_OT.match(dong[i])
        so, ten = int(m.group(1)), m.group(2).strip()

        # ── cắt thành ba vùng theo mốc ✦ ──
        vung, ten_vung = {'de': []}, 'de'
        nguong, tong = 0, 0
        for t in dong[i + 1:]:
            if t.startswith('ĐÁP ÁN CHI TIẾT') or re.match(r'^\S+\s+ĐÁP ÁN', t):
                break
            mv = R_MOC.match(t)
            if mv:
                nhan = mv.group(1)
                ten_vung = ('soi' if 'BẢNG TỰ SOI' in nhan else
                            'deB' if nhan.startswith('ĐỀ B') else 'khac')
                vung.setdefault(ten_vung, [])
                continue
            if ten_vung == 'de' and not nguong:
                g = R_NGUONG.search(t)
                if g and 'Đạt' in t:
                    nguong, tong = int(g.group(1)), int(g.group(2))
            vung.setdefault(ten_vung, []).append(t)

        de = [{'qno': int(c.group(1)), 'text': c.group(2)}
              for c in (R_CAU.match(t) for t in vung.get('de', [])) if c]
        deB = [{'qno': int(c.group(1)), 'text': c.group(2)}
               for c in (R_DEB.match(t) for t in vung.get('deB', [])) if c]
        ve, can = _tach_moi_noi(' '.join(vung.get('soi', [])),
                                bai_theo_chuong.get(b['chuong'], []))

        for q in de:
            q['answer'] = dap.get(f'OT{so}#C{q["qno"]}', '')
            # ⚠ MỐI NỐI KHÔNG ĐƯỢC LẤY TỪ SÁCH NỮA — xem chú thích SỐ BÀI CỦA SÁCH
            # ĐÃ CHẾT ở đầu tệp. Thứ tự ưu tiên: bảng khai tay → bản đã có → sách.
            cu = da_co.get((so, q['qno']))
            if (so, q['qno']) in KHAI_TAY:
                moi = KHAI_TAY[(so, q['qno'])]
                q['veCau'], q['canCu'] = moi['ve'], moi.get('canCu', 'sach')
                if moi.get('text'):
                    q['text'] = moi['text']
                n_tay += 1
            elif cu and cu['veCau']:
                q['veCau'], q['canCu'] = cu['veCau'], cu['canCu']
                q['text'] = cu.get('text', q['text'])
                n_giu += 1
            else:
                q['veCau'] = ve.get(q['qno'], [])
                q['canCu'] = can.get(q['qno'], 'khong')
                n_sach += 1
        # ⚠ ĐỀ B CŨNG PHẢI GIỮ CÂU THÊM TAY. Chương 6 và 7 có 12 câu đề B trong bản
        # đang chạy, mà sách chỉ bóc ra 10 — hai câu kia do người thêm ở đợt trước.
        # Dựng lại theo sách là bốn câu ấy biến mất, và không phép chốt nào kêu vì
        # 10 vẫn nằm trong khoảng cho phép. Cùng dòng họ với mối nối: bản dựng lại
        # đè mất phần người sửa tay.
        co = {q['qno'] for q in deB}
        deB += [q for n, q in sorted(da_co_B.get(so, {}).items()) if n not in co]
        deB.sort(key=lambda q: q['qno'])
        for q in deB:
            q['answer'] = q.get('answer') or dap.get(f'OT{so}#B{q["qno"]}', '')

        ky.append({
            'id': f'DCR:KSN4.C{so}', 'chapter': b['chuong'], 'loai': 'ontap',
            'so': so, 'name': f'ÔN TẬP {so} · {ten}',
            'need': nguong, 'tong': tong,
            'examA': de, 'deB': deB,
        })

    with open(RA, 'w', encoding='utf-8') as f:
        json.dump({'tienTo': TIEN_TO, 'ky': ky}, f, ensure_ascii=False, indent=1)

    # ── CHỐT ──
    CO_THAT = set(json.load(open(
        os.path.join(GOC_KHO, 'data', 'lop4', 'thu_tu.json'), encoding='utf-8'))['thuTu'])
    loi = []
    if len(ky) != 11:
        loi.append(f'{len(ky)} kỳ ôn tập, sách có 11')
    for k in ky:
        n = len(k['examA'])
        if not 10 <= n <= 12:
            loi.append(f"{k['name']}: {n} câu đề chính")
        if not 10 <= len(k['deB']) <= 12:
            loi.append(f"{k['name']}: {len(k['deB'])} câu đề B")
        if k['need'] < 1 or k['tong'] != n:
            loi.append(f"{k['name']}: ngưỡng {k['need']}/{k['tong']} mà đề có {n} câu")
        # số thứ tự phải liền mạch 1..n — thiếu hay thừa đều là mẫu trượt
        if [q['qno'] for q in k['examA']] != list(range(1, n + 1)):
            loi.append(f"{k['name']}: số câu đề chính không liền mạch")
        # MỐI NỐI phải phủ ĐỦ. Đây là chốt đáng giá nhất của cả bước.
        thieu = [q['qno'] for q in k['examA'] if not q['veCau']]
        if thieu:
            loi.append(f"{k['name']}: {len(thieu)} câu MẤT mối nối: {thieu}")
        trong = [q['qno'] for q in k['examA'] + k['deB'] if not q['answer']]
        if trong:
            loi.append(f"{k['name']}: {len(trong)} câu không có đáp án: {trong}")
        # ⚠ SOI THEO SỔ THỨ TỰ THẬT, KHÔNG SOI THEO SÁCH. Bản cũ so với số bài của
        # sách, nên nó chỉ xanh khi mối nối cũng suy từ sách — tức là nó xanh đúng
        # lúc mọi thứ cùng sai một kiểu. Sổ `thu_tu.json` mới là chỗ khai bài thật.
        xau = [x for q in k['examA'] for x in q['veCau'] if x not in CO_THAT]
        if xau:
            loi.append(f"{k['name']}: trỏ về bài không có thật: {xau}")

    print(f'đã ghi {RA}')
    print(f'  mối nối: {n_tay} khai tay · {n_giu} giữ từ bản cũ · {n_sach} suy từ sách')
    print(f"  {len(ky)} kỳ ôn tập · {sum(len(k['examA']) for k in ky)} câu đề chính"
          f" · {sum(len(k['deB']) for k in ky)} câu đề B")
    cc = {}
    for k in ky:
        for q in k['examA']:
            cc[q['canCu']] = cc.get(q['canCu'], 0) + 1
    print(f'  căn cứ mối nối: {cc}')
    if loi:
        print(f'  ⚠ {len(loi)} chỗ lệch:')
        for x in loi[:20]:
            print('     ·', x)
        raise SystemExit(1)
    print('  ✓ chốt: đủ 11 kỳ · số câu liền mạch · MỌI câu có mối nối và đáp án')


if __name__ == '__main__':
    main()
