# -*- coding: utf-8 -*-
"""
Nguyên mẫu riêng cho LỚP 3.

Chín trên mười ba nhóm hình lớp 3 dùng lại được nguyên mẫu lớp 2 (xem
`docs/phan_loai_hinh_lop3.md`). Nên tệp này KHÔNG chép lại chúng — nó nhập thẳng
từ `arch_l2` rồi chỉ viết thêm phần lớp 3 mới có. Bộ vẽ tra nguyên mẫu bằng
`getattr(arch_l3, tên)`, nên nhập vào đây là đủ để dùng, và sửa một nguyên mẫu
lớp 2 thì hình lớp 3 được sửa theo — thứ mà bản chép tay không làm được.

Nguyên mẫu lớp 3 phải dựng mới (5 cái, theo bước 1):
    hinh_tron        ✔ bài 29 · tâm - bán kính - đường kính - dây cung - vòng đồng tâm
    luoi_dien_tich   ✔ bài 30 · chữ nhật chia ô đơn vị, ĐẾM ĐƯỢC từng ô
    ven_hai_vong     — bài 25
    lich_thang       — bài 32
    can_ong_dong     — bài 33
    tien_viet        — bài 34
    bieu_thuc_ngoac  — bài 13-14
"""
import math

from core import (canvas, save, txt_fit, txt_wrap, _txt, FS,
                  NAVY, TEAL, GOLD, RED, DARKTEAL, INK, MUTE, LINE, SOFT, PALETEAL)
from arch_l2 import (MAU,                                          # noqa: F401
                     may_bien_doi, day_o, hang_hop, cham_tron, con_vat,
                     doan_thang, tia_so, hinh_phang, khoi_hop, bang_luoi,
                     bap_benh, noi_cap, cau_truc_so, dong_ho, hang_cay,
                     ban_tay, loi_thoai, hinh_ghep, thap_khoi, dong_hinh,
                     hinh_chu_vi, dong_xu_cham)


def hinh_tron(p, out):
    """
    GIẢI PHẪU HÌNH TRÒN — tâm, bán kính, đường kính, dây cung, vòng đồng tâm.

    params:
      title · note · hinh: [{...}]
        r         bán kính vẽ ra (đơn vị canvas); mặc định tự co cho vừa
        ten       tên hình, ghi dưới
        tam       nhãn tâm, thường 'O'. Bỏ trống thì không chấm tâm
        banKinh   {'ten': 'OA', 'so': '3 cm'}  → vẽ MỘT bán kính, ghi nhãn
        duongKinh {'ten': 'MN', 'so': '6 cm'}  → vẽ MỘT đường kính đi qua tâm
        day       {'ten': 'AB', 'so': '9 cm'}  → dây cung KHÔNG qua tâm
        dongTam   [2, 4] → hai vòng cùng tâm, số là bán kính thật (cm)

    Vì sao phải có `day` riêng: bài 29 câu 5 hỏi "đoạn AB = 9 cm nối hai mép có
    phải đường kính không?". Đáp là KHÔNG, vì nó không đi qua tâm. Vẽ dây cung
    thành một đoạn qua tâm là hình tự trả lời SAI ngay trước mắt bé.

    `dongTam` nhận bán kính THẬT rồi tự quy đổi theo tỉ lệ, không vẽ hai vòng
    "to nhỏ cho đẹp" — bài 29 câu 7 dạy vòng 4 cm phải gấp đúng đôi vòng 2 cm.
    """
    from matplotlib.patches import Circle
    hs = p.get('hinh') or []
    if not hs:
        raise ValueError('hinh_tron cần ít nhất một hình')
    n = len(hs)
    W = 88.0 / n
    tren = 11.0 if p.get('title') else 4.0
    CAO = min(34.0, W * 1.0)
    # chỗ cho tên hình: NGẮT DÒNG chứ không thu nhỏ mãi. Bản đầu dùng txt_fit nên
    # tên hình chạm sàn cỡ chữ rồi vẫn tràn, ba cái tên dính liền nhau thành một
    # dòng chữ đọc không ra chỗ nào của hình nào.
    TEN = 9.0 if any(h.get('ten') for h in hs) else 0.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.8, (tren + CAO + 8.0 + TEN + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - CAO / 2

    for i, h in enumerate(hs):
        cx = 6.0 + W * (i + 0.5)
        vien, nen, chu = MAU.get(h.get('mau', 'teal'), MAU['teal'])
        # chừa chỗ cho nhãn nằm NGOÀI mép, nên hình nhỏ hơn khung một chút
        r = float(h.get('r') or min(W * 0.30, CAO * 0.36))

        dong_tam = [float(x) for x in (h.get('dongTam') or [])]
        if dong_tam:
            # giữ ĐÚNG tỉ lệ giữa các vòng: vòng lớn nhất chiếm hết chỗ cho phép
            to = max(dong_tam)
            for k, bk in enumerate(sorted(dong_tam, reverse=True)):
                rr = r * bk / to
                ax.add_patch(Circle((cx, yc), rr, fc=nen if k == 0 else 'white',
                                    ec=vien, lw=2.4, zorder=4 + k))
                _txt(ax, cx + rr * 0.62, yc + rr * 0.62, f'{bk:g} cm',
                     fs=FS['tiny'], c=chu, w='bold', z=9)
        else:
            ax.add_patch(Circle((cx, yc), r, fc=nen, ec=vien, lw=2.4, zorder=4))

        # MỌI NHÃN ĐẶT NGOÀI MÉP. Bản đầu đặt nhãn ngay cạnh đoạn thẳng nên
        # "OA 3 cm" nằm đè lên đường viền hình tròn và "MN 6 cm" chen với chữ O ở
        # tâm — hình vẽ đúng toán mà đọc không ra.
        def nhan_ngoai(goc, s, mau):
            """Ghi nhãn ở ngoài mép, theo hướng `goc` tính từ tâm."""
            _txt(ax, cx + (r + 4.2) * math.cos(goc), yc + (r + 3.0) * math.sin(goc),
                 s, fs=FS['tiny'], c=mau, w='bold', z=9)

        # ── đường kính: đi QUA tâm, hai đầu chạm mép ──
        dk = h.get('duongKinh')
        if dk:
            ax.plot([cx - r, cx + r], [yc, yc], color=RED, lw=2.6, zorder=8)
            for sx in (-1, 1):
                ax.add_patch(Circle((cx + sx * r, yc), 1.0, fc=RED, ec=RED, zorder=9))
            nhan_ngoai(math.radians(90),
                       ' '.join(x for x in (dk.get('ten'), dk.get('so')) if x), RED)

        # ── bán kính: từ tâm ra mép, vẽ chếch lên để không nằm đè đường kính ──
        bk = h.get('banKinh')
        if bk:
            a = math.radians(52)
            ex, ey = cx + r * math.cos(a), yc + r * math.sin(a)
            ax.plot([cx, ex], [yc, ey], color=DARKTEAL, lw=2.6, zorder=8)
            ax.add_patch(Circle((ex, ey), 1.0, fc=DARKTEAL, ec=DARKTEAL, zorder=9))
            nhan_ngoai(a, ' '.join(x for x in (bk.get('ten'), bk.get('so')) if x), DARKTEAL)

        # ── dây cung: nối hai điểm trên mép, KHÔNG qua tâm ──
        dy = h.get('day')
        if dy:
            a1, a2 = math.radians(-38), math.radians(-142)
            x1, y1 = cx + r * math.cos(a1), yc + r * math.sin(a1)
            x2, y2 = cx + r * math.cos(a2), yc + r * math.sin(a2)
            ax.plot([x1, x2], [y1, y2], color='#7E57C2', lw=2.6, zorder=8)
            for x, y in ((x1, y1), (x2, y2)):
                ax.add_patch(Circle((x, y), 1.0, fc='#7E57C2', ec='#7E57C2', zorder=9))
            nhan_ngoai(math.radians(-90),
                       ' '.join(x for x in (dy.get('ten'), dy.get('so')) if x), '#7E57C2')

        if h.get('tam'):
            ax.add_patch(Circle((cx, yc), 1.1, fc=NAVY, ec=NAVY, zorder=10))
            # đẩy chữ O xuống chếch trái: đường kính chạy ngang qua tâm, đặt sát
            # quá là chữ nằm trên nét vẽ
            _txt(ax, cx - 3.2, yc - 3.2, str(h['tam']), fs=FS['small'], c=NAVY, w='bold', z=10)
        if h.get('ten'):
            txt_wrap(ax, cx, yc - CAO / 2 - 4.4, h['ten'], W - 4, FS['body'], chu,
                     z=7, max_lines=2)

    if p.get('note'):
        txt_fit(ax, 50, yc - CAO / 2 - TEN - 3.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def luoi_dien_tich(p, out):
    """
    CHỮ NHẬT CHIA Ô ĐƠN VỊ — bài diện tích, và bài so chu vi với diện tích.

    params:
      title · note · hinh: [{dai, rong, ten, mau, hienTich, thieuO, do}]
        dai, rong  số ô theo chiều dài và chiều rộng (số nguyên, đơn vị cm)
        hienTich   True → ghi sẵn "6 × 4 = 24 cm²" trên hình. Bản ĐỀ phải để False
        thieuO     số ô bỏ trống ở góc phải-trên, cho bài hình khuyết
        do         'tham' (mặc định) vẽ ô lòng để ĐẾM · 'rao' bỏ hết ô lòng, chỉ
                   còn viền dày kèm vạch chia từng xăng-ti-mét trên viền

    `do: 'rao'` không phải chuyện trang trí. Bản đầu tôi vẽ hình RÀO y hệt hình
    THẢM rồi chỉ đổi cái tên bên dưới — hai hình giống hệt nhau mà bài thì đang
    dạy bé phân biệt chúng, tức là hình phản lại chính bài. Rào đếm ô trên VIỀN,
    thảm đếm ô trong LÒNG; vẽ khác nhau thì bé nhìn một cái là thấy.

    Ô LƯỚI LÀ CÁI PHẢI ĐẾM ĐƯỢC. Nguyên mẫu lớp 2 `hinh_chu_vi` ghi số đo lên
    từng cạnh nhưng lòng hình để trống, `hinh_phang` kẻ được lưới nhưng không ghi
    số đo lên cạnh. Bài diện tích cần CẢ HAI cùng lúc: bé nhìn cạnh biết 6 và 4,
    nhìn lòng hình đếm ra 24 ô, rồi mới tin 6 × 4 = 24 chứ không phải học thuộc.

    Chu vi thì đếm ô VIỀN, diện tích đếm ô LÒNG — cùng một hình, hai phép đếm
    khác nhau. Đó là chỗ bé lớp 3 hay lẫn, nên hình phải đỡ được cả hai.
    """
    from matplotlib.patches import Rectangle
    hs = p.get('hinh') or []
    if not hs:
        raise ValueError('luoi_dien_tich cần ít nhất một hình')
    n = len(hs)
    W = 88.0 / n
    tren = 11.0 if p.get('title') else 4.0
    CAO = min(32.0, W * 0.92)
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.8, (tren + CAO + 16.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    yc = H - tren - CAO / 2

    # CẠNH Ô TÍNH MỘT LẦN CHO CẢ HÌNH, không tính riêng từng hình. Bản đầu tính
    # riêng nên trong cùng một bức, ô của hình 6×4 to hơn ô của hình 5×5 — mà bài
    # thì đang bảo bé SO hai diện tích ấy. Đơn vị đo lệch cỡ là hình nói dối: nhìn
    # vào tưởng ô bên này to hơn nên tấm này rộng hơn. (Đúng bẫy 26 của chuẩn, chỗ
    # lớp 2 từng vẽ hàng 2 chấm to hơn hàng 3 chấm trong cùng một rổ kẹo.)
    s = min(min((W - 12.0) / max(int(h['dai']), 1) for h in hs),
            min((CAO - 8.0) / max(int(h['rong']), 1) for h in hs))

    for i, h in enumerate(hs):
        cx = 6.0 + W * (i + 0.5)
        vien, nen, chu = MAU.get(h.get('mau', 'teal'), MAU['teal'])
        dai, rong = int(h['dai']), int(h['rong'])
        w, hgt = s * dai, s * rong
        x0, y0 = cx - w / 2, yc - hgt / 2

        thieu = int(h.get('thieuO', 0) or 0)
        if h.get('do') == 'rao':
            # RÀO: lòng để trống, viền dày, và vạch chia từng cm TRÊN viền — cái
            # bé phải đếm nằm ở đường bao, không nằm trong ruột
            ax.add_patch(Rectangle((x0, y0), w, hgt, fc=nen, ec=vien, lw=3.4, zorder=4))
            for c in range(1, dai):
                for yy in (y0, y0 + hgt):
                    ax.plot([x0 + c * s] * 2, [yy - s * 0.16, yy + s * 0.16],
                            color=vien, lw=2.0, zorder=7)
            for r in range(1, rong):
                for xx in (x0, x0 + w):
                    ax.plot([xx - s * 0.16, xx + s * 0.16], [y0 + r * s] * 2,
                            color=vien, lw=2.0, zorder=7)
        else:
            bo = set()
            for k in range(thieu):                # khuyết từ góc phải-TRÊN đi sang trái
                bo.add((rong - 1, dai - 1 - k))
            for r in range(rong):
                for c in range(dai):
                    if (r, c) in bo:
                        continue
                    ax.add_patch(Rectangle((x0 + c * s, y0 + r * s), s, s,
                                           fc=nen, ec=vien, lw=1.4, zorder=4))
            # viền ngoài đậm hơn lưới: bé nhìn ra MỘT hình bị vạch chia, không phải
            # một đống ô rời — đúng luật hình ghép của chuẩn
            if not thieu:
                ax.add_patch(Rectangle((x0, y0), w, hgt, fc='none', ec=vien,
                                       lw=2.8, zorder=6))

        _txt(ax, cx, y0 - 3.2, f'{dai} cm', fs=FS['small'], c=chu, w='bold', z=8)
        _txt(ax, x0 - 3.4, yc, f'{rong} cm', fs=FS['small'], c=chu, w='bold', z=8)
        if h.get('ten'):
            txt_wrap(ax, cx, y0 - 8.4, h['ten'], W - 4, FS['body'], chu, z=7, max_lines=2)
        if h.get('hienTich'):
            so = dai * rong - thieu
            _txt(ax, cx, y0 + hgt + 3.2,
                 f'{so} ô = {so} cm²' if thieu else f'{dai} × {rong} = {so} cm²',
                 fs=FS['small'], c=RED, w='bold', z=8)

    if p.get('note'):
        txt_fit(ax, 50, yc - CAO / 2 - 13.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def ven_hai_vong(p, out):
    """
    SƠ ĐỒ VEN HAI VÒNG — bài 25.

    params:
      title · note
      trai   {'ten': 'BÓNG ĐÁ', 'tong': 20, 'rieng': 12}
      phai   {'ten': 'CẦU LÔNG', 'tong': 18, 'rieng': 10}
      giua   8            số ở vùng hai vòng ôm nhau
      ngoai  {'ten': 'không mê môn nào', 'so': 5}
      tong   35           sĩ số cả lớp, ghi ở khung ngoài
      an     ['rieng', 'ngoai']   vùng nào để DẤU CHẤM HỎI thay vì số

    `an` là thứ làm nên bản ĐỀ. Sách dạy "điền vùng GIỮA trước, hai cánh sau", nên
    hình đề phải để trống đúng hai cánh ấy — điền sẵn là bé khỏi phải làm gì, mà
    hình vẫn trông đầy đủ nên nhìn lướt không thấy sai.
    """
    from matplotlib.patches import Circle, FancyBboxPatch
    tr, ph = p.get('trai') or {}, p.get('phai') or {}
    an = set(p.get('an') or [])
    tren = 11.0 if p.get('title') else 4.0
    CAO = 40.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(3.0, (tren + CAO + 6.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    yc = H - tren - CAO / 2
    r = 14.0
    cxt, cxp = 50 - r * 0.62, 50 + r * 0.62

    # khung ngoài = cả lớp. Vùng NGOÀI hai vòng cũng là một đáp số của bài (bước 4),
    # nên nó phải có chỗ đứng nhìn thấy được, không phải một dòng chữ rời.
    ax.add_patch(FancyBboxPatch((8, yc - r - 6.0), 84, (r + 6.0) * 2,
                                boxstyle='round,pad=0.6,rounding_size=2',
                                fc='white', ec=LINE, lw=2.0, zorder=2))
    if p.get('tong') is not None:
        _txt(ax, 11.5, yc + r + 3.4, f"cả lớp {p['tong']}", fs=FS['small'], c=MUTE,
             w='bold', ha='left', z=6)

    ax.add_patch(Circle((cxt, yc), r, fc=PALETEAL, ec=TEAL, lw=2.6, alpha=0.85, zorder=4))
    ax.add_patch(Circle((cxp, yc), r, fc='#FFF4DF', ec=GOLD, lw=2.6, alpha=0.75, zorder=4))

    def so(v, khoa):
        return '?' if khoa in an else str(v)

    _txt(ax, cxt - r * 0.52, yc, so(tr.get('rieng'), 'rieng'), fs=FS['big'],
         c=DARKTEAL, w='bold', z=8)
    _txt(ax, cxp + r * 0.52, yc, so(ph.get('rieng'), 'rieng'), fs=FS['big'],
         c='#5A3A00', w='bold', z=8)
    _txt(ax, 50, yc, so(p.get('giua'), 'giua'), fs=FS['big'], c=RED, w='bold', z=9)

    _txt(ax, cxt - r * 0.35, yc + r + 2.2, f"{tr.get('ten', '')} · {tr.get('tong', '')}",
         fs=FS['small'], c=DARKTEAL, w='bold', z=8)
    _txt(ax, cxp + r * 0.35, yc - r - 3.0, f"{ph.get('ten', '')} · {ph.get('tong', '')}",
         fs=FS['small'], c='#5A3A00', w='bold', z=8)
    _txt(ax, 50, yc - 5.4, 'cả hai', fs=FS['tiny'], c=RED, w='bold', z=9)

    ng = p.get('ngoai') or {}
    if ng:
        # góc phải-TRÊN, đối diện nhãn "cả lớp" ở góc trái-trên. Đặt ở dưới thì nó
        # đè lên tên vòng phải, mà cả hai đều là chữ đậm nên chồng lên nhau là mất
        # đọc cả đôi.
        _txt(ax, 88.5, yc + r + 3.4, f"{ng.get('ten', '')}: {so(ng.get('so'), 'ngoai')}",
             fs=FS['small'], c=MUTE, w='bold', ha='right', z=6)
    if p.get('note'):
        txt_fit(ax, 50, yc - r - 9.5, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def lich_thang(p, out):
    """
    TỜ LỊCH THÁNG — bài 32, và mọi bài hỏi "ngày ấy là thứ mấy".

    params:
      title · note
      batDau  thứ của ngày 1, tính 0 = thứ Hai … 6 = Chủ nhật
      soNgay  số ngày của tháng
      toDam   [6, 13, 20, 27]  các ngày cần làm nổi
      cot     chỉ số cột cần tô nhạt cả cột (0-6) — cho bài "cùng cột là cùng thứ"
      hoi     [22]  ngày để DẤU HỎI thay vì số, dùng cho bản ĐỀ

    Cột dọc chính là bài học: các ngày cùng cột cách nhau đúng 7. Vẽ lịch mà không
    làm nổi được cột thì bé không thấy "đoàn tàu nhịp 7" mà bài đang nói tới.
    """
    from matplotlib.patches import Rectangle
    THU = ['Hai', 'Ba', 'Tư', 'Năm', 'Sáu', 'Bảy', 'CN']
    bd = int(p.get('batDau', 0))
    n = int(p.get('soNgay', 30))
    to_dam = set(p.get('toDam') or [])
    hoi = set(p.get('hoi') or [])
    cot = p.get('cot')

    hang = -(-(bd + n) // 7)                 # số hàng cần, làm tròn lên
    tren = 11.0 if p.get('title') else 4.0
    O = 11.0
    CAO = O * (hang + 1) + 3.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.8, (tren + CAO + 6.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    x0 = 50 - O * 7 / 2
    ytr = H - tren - O
    if cot is not None:
        ax.add_patch(Rectangle((x0 + int(cot) * O, ytr - O * hang), O, O * (hang + 1),
                               fc='#FFF4DF', ec='none', zorder=2))
    for c in range(7):
        _txt(ax, x0 + (c + 0.5) * O, ytr + O / 2, THU[c], fs=FS['small'], c=NAVY,
             w='bold', z=6)
    for ngay in range(1, n + 1):
        k = bd + ngay - 1
        r, c = k // 7, k % 7
        x, y = x0 + c * O, ytr - (r + 1) * O
        dam = ngay in to_dam
        ax.add_patch(Rectangle((x + 0.6, y + 0.6), O - 1.2, O - 1.2,
                               fc=PALETEAL if dam else 'white',
                               ec=TEAL if dam else LINE, lw=2.2 if dam else 1.2, zorder=4))
        _txt(ax, x + O / 2, y + O / 2, '?' if ngay in hoi else str(ngay),
             fs=FS['body'], c=RED if ngay in hoi else (DARKTEAL if dam else INK),
             w='bold', z=6)
    if p.get('note'):
        txt_fit(ax, 50, ytr - O * hang - 4.6, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def can_ong_dong(p, out):
    """
    CÂN HAI ĐĨA và ỐNG ĐONG — bài 33.

    params:
      title · note
      can  {'trai': ['túi bột', '200 g'], 'phai': ['500 g']}
           mỗi đĩa là danh sách nhãn xếp chồng lên nhau
      ong  [{'ten': 'ca', 'ml': 250, 'day': 250, 'toiDa': 500}, …]
           `day` là mức nước đang có, `toiDa` là vạch cao nhất của ống

    Cân phải vẽ THĂNG BẰNG, đòn ngang phẳng. Vẽ lệch cho "sinh động" là hình tự
    nói vật nặng hơn quả cân, ngược hẳn đề bài.
    """
    from matplotlib.patches import Rectangle, Polygon
    can = p.get('can')
    ong = p.get('ong') or []
    tren = 11.0 if p.get('title') else 4.0
    CAO = 34.0 if can else 30.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.8, (tren + CAO + 8.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)
    ytr = H - tren - CAO

    if can:
        cx = 50 if not ong else 27
        yd = ytr + CAO * 0.62                # cao độ đòn cân
        ax.plot([cx, cx], [ytr + 2, yd], color=MUTE, lw=3.4, zorder=4)
        ax.add_patch(Polygon([(cx - 5, ytr + 2), (cx + 5, ytr + 2), (cx, ytr + 7)],
                             fc=SOFT, ec=MUTE, lw=2.0, zorder=3))
        ax.plot([cx - 17, cx + 17], [yd, yd], color=MUTE, lw=3.4, zorder=5)
        # DÂY TREO PHẢI ĐỦ DÀI. Bản đầu treo đĩa ngay sát đòn nên vật xếp lên đĩa
        # chồng đè cả lên đòn cân — nhìn ra một mớ khung chữ nhật, không ra cái cân.
        DAY, CAO_O = 15.0, 5.2
        for ben, ds in ((-1, can.get('trai') or []), (1, can.get('phai') or [])):
            px = cx + ben * 17
            ax.plot([px, px], [yd - DAY, yd], color=MUTE, lw=1.8, zorder=5)
            ax.add_patch(Polygon([(px - 8, yd - DAY), (px + 8, yd - DAY),
                                  (px + 6, yd - DAY - 3.0), (px - 6, yd - DAY - 3.0)],
                                 fc=SOFT, ec=MUTE, lw=2.0, zorder=5))
            for j, nh in enumerate(reversed(ds)):     # xếp CHỒNG LÊN từ mặt đĩa
                yy = yd - DAY + 0.4 + j * (CAO_O + 0.8)
                ax.add_patch(Rectangle((px - 8.5, yy), 17, CAO_O, fc=PALETEAL,
                                       ec=TEAL, lw=2.0, zorder=6))
                txt_fit(ax, px, yy + CAO_O / 2, str(nh), 15.5, FS['small'], DARKTEAL, z=7)
        _txt(ax, cx, yd + 3.4, 'THĂNG BẰNG', fs=FS['tiny'], c=RED, w='bold', z=8)

    for i, o in enumerate(ong):
        n = len(ong)
        px = (50 if not can else 73) + (i - (n - 1) / 2) * 16
        w, hgt = 11.0, 22.0
        y0 = ytr + 6.0
        toi_da = float(o.get('toiDa') or o.get('ml') or 1)
        muc = min(float(o.get('day', 0)) / toi_da, 1.0) * hgt
        ax.add_patch(Rectangle((px - w / 2, y0), w, muc, fc='#BDE9FF', ec='none', zorder=4))
        ax.add_patch(Rectangle((px - w / 2, y0), w, hgt, fc='none', ec=NAVY, lw=2.4, zorder=6))
        for k in range(1, 5):                # vạch chia — không có vạch thì không đong được
            ax.plot([px - w / 2, px - w / 2 + 3], [y0 + hgt * k / 4] * 2,
                    color=NAVY, lw=1.4, zorder=7)
        _txt(ax, px, y0 - 3.2, f"{o.get('ten', '')} {o.get('ml', '')} ml".strip(),
             fs=FS['tiny'], c=NAVY, w='bold', z=7)
    if p.get('note'):
        txt_fit(ax, 50, ytr - 3.4, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def tien_viet(p, out):
    """
    TIỀN VIỆT và SỔ VỐN - BÁN - LÃI — bài 34.

    params:
      title · note
      to  [{'gia': 20, 'so': 1}, …]  các tờ tiền, `gia` tính bằng NGHÌN đồng
      so  [{'ten': 'VỐN', 'gia': 24, 'mau': 'do'}, …]  ba dòng sổ vàng

    Tờ tiền vẽ ĐỦ SỐ TỜ, không vẽ một tờ rồi ghi "× 3": bài này bé phải cộng được
    tiền trên tay, mà đếm hộ rồi thì còn gì để đếm.
    """
    from matplotlib.patches import Rectangle
    to = p.get('to') or []
    so = p.get('so') or []
    tren = 11.0 if p.get('title') else 4.0
    CAO_T = 17.0 if to else 0.0
    CAO_S = 9.0 * len(so) + (3.0 if so else 0.0)
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + CAO_T + CAO_S + 8.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren
    if to:
        phang = [t for t in to for _ in range(int(t.get('so', 1)))]
        n = max(len(phang), 1)
        w = min(19.0, 88.0 / n - 2.0)
        x = 50 - (w + 2.0) * n / 2 + 1.0
        y -= 14.0
        for t in phang:
            ax.add_patch(Rectangle((x, y), w, 11.0, fc='#FFF4DF', ec=GOLD, lw=2.2, zorder=4))
            txt_fit(ax, x + w / 2, y + 6.6, f"{t['gia']}", w - 3, FS['mid'], '#5A3A00', z=6)
            txt_fit(ax, x + w / 2, y + 2.8, 'nghìn', w - 3, FS['tiny'], MUTE, z=6)
            x += w + 2.0
        y -= 3.0

    for d in so:
        y -= 9.0
        vien, nen, chu = MAU.get(d.get('mau', 'teal'), MAU['teal'])
        ax.add_patch(Rectangle((18, y), 64, 7.4, fc=nen, ec=vien, lw=2.0, zorder=4))
        _txt(ax, 21, y + 3.7, str(d.get('ten', '')), fs=FS['small'], c=chu, w='bold',
             ha='left', z=6)
        _txt(ax, 79, y + 3.7, f"{d.get('gia')} nghìn", fs=FS['small'], c=chu, w='bold',
             ha='right', z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 5.0, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)


def bieu_thuc_ngoac(p, out):
    """
    BIỂU THỨC TÍNH TỪNG NHỊP — bài 13 (thứ tự) và 14 (ngoặc).

    params:
      title · note
      buoc [{'bt': '5 + 3 × 2', 'to': '3 × 2', 'loi': 'bóc túi trước'}, …]
        bt   biểu thức, các phần cách nhau bằng KHOẢNG TRẮNG
        to   phần đang được tính ở nhịp này — khoanh lại
        loi  lời giải thích một dòng (tuỳ chọn)

    Khoanh đúng phần SẮP TÍNH là toàn bộ bài học: "rà mắt tìm × và :, khoanh chúng
    lại như khoanh xe ưu tiên". Nên `to` phải khớp một cụm LIỀN NHAU của `bt` —
    không khớp thì dừng hẳn, vì khoanh nhầm chỗ là dạy ngược.
    """
    from matplotlib.patches import FancyBboxPatch
    buoc = p.get('buoc') or []
    if not buoc:
        raise ValueError('bieu_thuc_ngoac cần ít nhất một nhịp')
    tren = 11.0 if p.get('title') else 4.0
    D = 13.0
    duoi = 8.0 if p.get('note') else 4.0
    fig, ax, H = canvas(7.6, max(2.4, (tren + D * len(buoc) + 6.0 + duoi) * 7.6 / 100))
    if p.get('title'):
        txt_fit(ax, 50, H - 5.4, p['title'], 92, FS['title'], NAVY, z=6)

    y = H - tren
    for b in buoc:
        y -= D
        tok = str(b['bt']).split()
        rong = [max(len(t), 1) * 2.6 + 2.2 for t in tok]
        tong = sum(rong)
        x = 50 - tong / 2
        vt = []                                   # (x đầu, x cuối) của từng phần
        for t, w in zip(tok, rong):
            vt.append((x, x + w))
            _txt(ax, x + w / 2, y + 6.4, t, fs=FS['mid'], c=INK, w='bold', z=7)
            x += w

        if b.get('to'):
            can = str(b['to']).split()
            i = next((k for k in range(len(tok) - len(can) + 1)
                      if tok[k:k + len(can)] == can), None)
            if i is None:
                raise ValueError(f"bieu_thuc_ngoac: không tìm thấy '{b['to']}' "
                                 f"trong '{b['bt']}' — khoanh nhầm chỗ là dạy ngược")
            x1, x2 = vt[i][0], vt[i + len(can) - 1][1]
            ax.add_patch(FancyBboxPatch((x1, y + 2.6), x2 - x1, 7.6,
                                        boxstyle='round,pad=0.4,rounding_size=1.6',
                                        fc='none', ec=RED, lw=2.4, zorder=8))
        if b.get('loi'):
            txt_fit(ax, 50, y + 0.4, b['loi'], 88, FS['small'], DARKTEAL, z=6)
    if p.get('note'):
        txt_fit(ax, 50, y - 4.6, p['note'], 92, FS['body'], DARKTEAL, z=5)
    save(fig, out)
