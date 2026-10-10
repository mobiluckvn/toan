#!/usr/bin/env python3
"""
HÌNH VẼ CHO CHƯƠNG 3 (bản viết lại) → docs/hinh_c3v3/*.png

    tools/tts/.venv/bin/python tools/chuong3_v3_hinh.py

Sáu hình, mỗi hình trả lời đúng một câu hỏi Thầy đặt ra trong phần nhận xét:

    h1_kien_truc     kiến trúc bốn tầng và vòng lặp thích ứng
    h2_thanh_hinh    đồ thị tri thức THÀNH HÌNH như thế nào (6 bước, kèm số)
    h3_manh_do_thi   một MẢNH đồ thị thật, trích bằng chính phép duyệt của hệ thống
    h4_luu_phien     một phiên của một cá nhân lưu những gì, ở đâu
    h5_pl_phien      diễn biến P(L) qua 11 lượt của phiên ví dụ
    h6_lan_truyen    cây lan truyền ngược kèm độ ngờ của từng ứng viên

⚠ SỐ TRONG HÌNH 3, 5, 6 KHÔNG GÕ TAY. Chúng lấy từ `chuong3_v3_so.json` — tệp do
`tools/chuong3_v3_so.mjs` sinh ra bằng cách gọi CHÍNH mã đang chạy thật (bkt.js,
lantruyen.js, chinhsach.js, zpd.js, phudao.js). Sửa công thức thì hình sai theo,
nên hình là bằng chứng chứ không phải lời kể.
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                              # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs" / "hinh_c3v3"
SO = json.loads((GOC / "docs" / "chuong3_v3_so.json").read_text("utf8"))

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["savefig.dpi"] = 200

LAM = "#dbe8f5"
LAM_VIEN = "#3f6f9f"
VANG = "#fdf0d0"
VANG_VIEN = "#c58f1d"
LUC = "#dcecd8"
LUC_VIEN = "#4b7a42"
HONG = "#f7dcdf"
HONG_VIEN = "#b0424d"
XAM = "#eeeeee"
XAM_VIEN = "#777777"


def hop(ax, x, y, w, h, tieu_de, than="", nen=LAM, vien=LAM_VIEN, co=9.0, co_td=9.8):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor=nen, edgecolor=vien, linewidth=1.3))
    if than:
        ax.text(x + w / 2, y + h * 0.70, tieu_de, ha="center", va="center",
                fontsize=co_td, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.33, than, ha="center", va="center", fontsize=co)
    else:
        ax.text(x + w / 2, y + h / 2, tieu_de, ha="center", va="center",
                fontsize=co_td, fontweight="bold")


def mui_ten(ax, xy1, xy2, chu="", mau="#444444", net="-", co=8.0, lech=0.0):
    ax.add_patch(FancyArrowPatch(
        xy1, xy2, arrowstyle="-|>", mutation_scale=13, linewidth=1.2,
        color=mau, linestyle=net, shrinkA=2, shrinkB=2))
    if chu:
        ax.text((xy1[0] + xy2[0]) / 2 + lech, (xy1[1] + xy2[1]) / 2 + 0.018, chu,
                ha="center", va="bottom", fontsize=co, color=mau, style="italic")


def khung(w=12.0, h=5.4):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def luu(fig, ten):
    RA.mkdir(parents=True, exist_ok=True)
    p = RA / f"{ten}.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {p.relative_to(GOC)}")


# ══════════════════════════════════════════════════════════════════ HÌNH 1 ══
def h1_kien_truc():
    fig, ax = khung(12.4, 6.0)
    ax.text(0.5, 0.98, "MÁY NGƯỜI HỌC — chạy được khi mất kết nối (ràng buộc R4)",
            ha="center", fontsize=10, fontweight="bold", color=LAM_VIEN)
    hop(ax, 0.02, 0.76, 0.30, 0.17, "TẦNG TRÌNH DIỄN",
        "màn bài học · phòng luyện nói · màn ôn tập\nGóc phụ huynh · Sổ phụ huynh · Bảng cô giáo")
    hop(ax, 0.35, 0.76, 0.30, 0.17, "TẦNG THÍCH ỨNG",
        "vectơ S · hàm chính sách π\nxếp câu theo ZPD · dựng bài phụ đạo")
    hop(ax, 0.68, 0.76, 0.30, 0.17, "ĐỒ THỊ RÚT GỌN (127 KB)",
        "1.194 nút · 253 cạnh\nduyệt ngược / duyệt xuôi tại máy")

    ax.text(0.98, 0.665, "MÁY CHỦ — hàm nền, kích hoạt bởi một bản ghi mới",
            ha="right", fontsize=10, fontweight="bold", color=VANG_VIEN)
    hop(ax, 0.02, 0.44, 0.30, 0.17, "TẦNG DỮ LIỆU",
        "attempts (bất biến) · mastery\nprogressTA · hocBaTA · reviewQueue",
        nen=VANG, vien=VANG_VIEN)
    hop(ax, 0.35, 0.44, 0.30, 0.17, "HÀM NỀN onAttempt",
        "cập nhật Bayes có cơ chế quên\nghi hồ sơ nút trong một giao dịch",
        nen=VANG, vien=VANG_VIEN)
    hop(ax, 0.68, 0.44, 0.30, 0.17, "DỊCH VỤ MÔ HÌNH",
        "trung chuyển lời gọi · không lưu\nnội dung riêng tư của trẻ (R5)",
        nen=VANG, vien=VANG_VIEN)

    mui_ten(ax, (0.12, 0.76), (0.12, 0.61))
    ax.text(0.135, 0.685, "bản ghi lượt trả lời", fontsize=8,
            style="italic", color="#444444", va="center")
    mui_ten(ax, (0.47, 0.61), (0.47, 0.76))
    ax.text(0.485, 0.685, "hồ sơ nút đã cập nhật", fontsize=8,
            style="italic", color="#444444", va="center")
    mui_ten(ax, (0.32, 0.525), (0.35, 0.525))
    mui_ten(ax, (0.65, 0.525), (0.68, 0.525))

    b = ["1. người học trả lời → đo thời gian riêng cho lượt ấy",
         "2. dựng bản ghi bất biến, xếp hàng đợi cục bộ, đẩy theo lô",
         "3. hàm nền chạy BKT có quên, ghi hồ sơ nút trong giao dịch",
         "4. máy người học nạp lại hồ sơ nút, tính vectơ S",
         "5. π = tịnh tiến → xếp lại thứ tự câu theo ZPD",
         "6. π = phụ đạo → duyệt ngược tìm nút gốc rễ, dựng bài vá",
         "7. đạt bài → sinh thẻ ôn theo lịch 1·3·7·14·30 ngày"]
    ax.add_patch(FancyBboxPatch(
        (0.02, 0.03), 0.96, 0.33, boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor="#fbfbfb", edgecolor=XAM_VIEN, linewidth=1.0))
    ax.text(0.5, 0.325, "VÒNG LẶP THÍCH ỨNG — lặp sau mỗi lượt trả lời",
            ha="center", fontsize=9.6, fontweight="bold")
    for i, x in enumerate(b):
        ax.text(0.05 if i < 4 else 0.52, 0.265 - (i % 4) * 0.058, x,
                fontsize=8.6, va="center")
    luu(fig, "h1_kien_truc")


# ══════════════════════════════════════════════════════════════════ HÌNH 2 ══
def h2_thanh_hinh():
    fig, ax = khung(13.0, 4.4)
    buoc = [
        ("① SỐ HOÁ", "sách giáo khoa + Thông tư\n32/2018 → bảng chuẩn", XAM, XAM_VIEN),
        ("② KHAI NÚT", "740 mục từ · 164 mẫu câu\ntrong chuan_lopN.json", LAM, LAM_VIEN),
        ("③ KHAI CẠNH", "215 mối tiên quyết\n(trường thang[])", LAM, LAM_VIEN),
        ("④ HỢP NHẤT", "đồ thị đầy đủ 1–12\n3.989 nút · 7.602 cạnh", LAM, LAM_VIEN),
        ("⑤ KIỂM", "0 cạnh treo · 0 chu trình\ntrên quan hệ REQUIRES", LUC, LUC_VIEN),
        ("⑥ RÚT GỌN", "bản lúc chạy 1–6\n1.194 nút · 253 cạnh · 127 KB", VANG, VANG_VIEN),
    ]
    w, khe = 0.140, 0.022
    for i, (td, than, nen, vien) in enumerate(buoc):
        x = 0.025 + i * (w + khe)
        hop(ax, x, 0.42, w, 0.34, td, than, nen=nen, vien=vien, co=8.0, co_td=9.4)
        if i:
            mui_ten(ax, (x - khe, 0.59), (x, 0.59))
    ax.text(0.5, 0.94, "ĐỒ THỊ TRI THỨC THÀNH HÌNH QUA SÁU BƯỚC — mỗi bước có "
                       "một con số kiểm chứng được",
            ha="center", fontsize=10.4, fontweight="bold")
    ax.text(0.5, 0.26,
            "Chỉ bước ⑥ chạy mỗi lần dựng lại học liệu; năm bước đầu chạy một lần "
            "cho mỗi năm học.\nBản lúc chạy CHỈ giữ quan hệ — không nhãn dài, không "
            "ví dụ, không nghĩa: học liệu đã mang đủ phần ngữ nghĩa.",
            ha="center", fontsize=8.8, style="italic", color="#444444")
    ax.text(0.5, 0.08,
            "data/tienganh/chuan_lop1..5.json   →   data/ban_do_tieng_anh.json   →   "
            "web/public/content/tienganh/do_thi.json",
            ha="center", fontsize=8.4, family="monospace", color=LAM_VIEN)
    luu(fig, "h2_thanh_hinh")


# ══════════════════════════════════════════════════════════════════ HÌNH 3 ══
def h3_manh_do_thi():
    """Mảnh đồ thị quanh nút người học đang mắc — toạ độ đặt tay cho dễ đọc."""
    fig, ax = khung(13.0, 4.6)
    g = SO["manhDoThi"]
    nut = {n["ma"]: n for n in g["nut"]}

    #                       cột (trái = xa chỗ sai),  hàng
    dat = {
        "sp_g3_u3_1": (0, 0), "sp_g3_u3_2": (1, 0), "sp_g3_u8_1": (1, 1),
        "sp_g3_u4_1": (2, 0), "sp_g3_u9_1": (2, 1),
        "sp_g3_u13_1": (3, 0), "sp_g3_u9_2": (3, 1),
        "sp_g3_u13_2": (4, 0.5),
    }
    W, H = 0.175, 0.21
    X = [0.0025, 0.2075, 0.4125, 0.6175, 0.8225]
    Y = [0.58, 0.23]

    def o(ma):
        c, h = dat[ma]
        return X[c], Y[0] + (Y[1] - Y[0]) * h

    for ma, n in ((m, nut[m]) for m in dat if m in nut):
        x, y = o(ma)
        p = n["p"]
        if ma == "sp_g3_u13_2":
            nen, vien = HONG, HONG_VIEN
        elif p is not None and p >= 0.85:
            nen, vien = LUC, LUC_VIEN
        else:
            nen, vien = LAM, LAM_VIEN
        ax.add_patch(FancyBboxPatch(
            (x, y), W, H, boxstyle="round,pad=0.006,rounding_size=0.014",
            facecolor=nen, edgecolor=vien, linewidth=1.3))
        ax.text(x + W / 2, y + H * 0.79, ma, ha="center", va="center",
                fontsize=7.6, family="monospace", color="#333333")
        nhan = "\n".join(textwrap.wrap(n["nhan"], 30)[:3])
        ax.text(x + W / 2, y + H * 0.47, nhan, ha="center", va="center", fontsize=7.4)
        pp = "chưa có số liệu" if p is None else f"P(L) = {p:.3f}".replace(".", ",")
        ax.text(x + W / 2, y + H * 0.13, f"{pp}  ·  {n['bai']}", ha="center",
                va="center", fontsize=7.0, style="italic", color="#555555")

    for e in g["canh"]:
        a, b = e["can"], e["truoc_khi"]
        if a not in dat or b not in dat:
            continue
        xa, ya = o(a)
        xb, yb = o(b)
        if dat[a][0] == dat[b][0]:                 # cùng cột → mũi tên dọc
            xuong = ya > yb
            mui_ten(ax, (xa + W / 2, ya if xuong else ya + H),
                    (xb + W / 2, yb + H if xuong else yb))
        else:
            mui_ten(ax, (xa + W, ya + H / 2), (xb, yb + H / 2))

    ax.text(0.5, 0.95, "MỘT MẢNH ĐỒ THỊ THẬT — trích bằng chính phép duyệt "
                       "duyetNguoc() của hệ thống, trần độ sâu 4",
            ha="center", fontsize=10.4, fontweight="bold")
    ax.text(0.5, 0.855, "tám đỉnh · bảy cạnh loại ban_do · mọi giá trị P(L) do hàm "
                        "nền tính ra từ chuỗi trả lời ở Bảng 3.19",
            ha="center", fontsize=8.4, style="italic", color="#555555")
    ax.text(0.5, 0.075,
            "Hướng cạnh: A → B đọc là “phải có A trước khi học B”. "
            "Hồng: nơi lỗi biểu hiện.  Xanh lá: nút đã đạt ngưỡng tinh thông nên bị "
            "LOẠI khỏi danh sách khả nghi.  Xanh dương: ứng viên được xếp hạng.",
            ha="center", fontsize=8.2, style="italic", color="#444444")
    luu(fig, "h3_manh_do_thi")



# ══════════════════════════════════════════════════════════════════ HÌNH 4 ══
def h4_luu_phien():
    fig, ax = khung(12.6, 5.6)
    ax.text(0.5, 0.965, "MỘT PHIÊN CỦA MỘT NGƯỜI HỌC ĐƯỢC LƯU Ở ĐÂU",
            ha="center", fontsize=10.6, fontweight="bold")

    hop(ax, 0.02, 0.70, 0.27, 0.16, "MÁY NGƯỜI HỌC",
        "hàng đợi localStorage\nttd5.queueTA.v1 + sổ đã gửi", nen=XAM, vien=XAM_VIEN)
    hop(ax, 0.02, 0.44, 0.27, 0.16, "MỘT LẦN MỞ BÀI = MỘT PHIÊN",
        "mã phiên p<base36><ngẫu nhiên>\nmọi lượt trong phiên dùng chung mã ấy",
        nen=XAM, vien=XAM_VIEN)

    kho = [
        ("attempts/{id}", "1 dòng / 1 lượt trả lời — BẤT BIẾN\n"
                          "id = người học · phiên · bài · câu · số thứ tự",
         "máy người học ghi", HONG, HONG_VIEN, 0.74),
        ("mastery/{uid}/units/{maNut}", "P(L), pTruoc, nAttempts, nCorrect,\n"
                                        "saiLienTiep, msTrungBinh, lastSeen",
         "CHỈ hàm nền onAttempt ghi", VANG, VANG_VIEN, 0.505),
        ("progressTA/{uid}/micros/{maBai}", "pass, score, total, attempts\n"
                                            "— kết quả cuối bài",
         "máy người học ghi", LAM, LAM_VIEN, 0.27),
        ("hocBaTA/{uid}/muc/{khoa}", "loai='phien' (bỏ dở) · loai='phudao'\n"
                                     "(khung A-R-A) · loai='hoSo' (định dạng)",
         "máy người học ghi", LUC, LUC_VIEN, 0.035),
    ]
    for ten, than, ai, nen, vien, y in kho:
        ax.add_patch(FancyBboxPatch(
            (0.40, y), 0.57, 0.185,
            boxstyle="round,pad=0.01,rounding_size=0.018",
            facecolor=nen, edgecolor=vien, linewidth=1.3))
        ax.text(0.425, y + 0.138, ten, ha="left", va="center", fontsize=9.0,
                family="monospace", fontweight="bold")
        ax.text(0.425, y + 0.062, than, ha="left", va="center", fontsize=8.2)
        ax.text(0.955, y + 0.138, ai, ha="right", va="center", fontsize=7.8,
                style="italic", color=vien)

    for y1, y2 in [(0.78, 0.83), (0.52, 0.60), (0.50, 0.36), (0.47, 0.13)]:
        mui_ten(ax, (0.29, y1), (0.40, y2))
    ax.text(0.5, -0.02,
            "Luật máy chủ: attempts cho create, CẤM update và delete; mastery thì "
            "máy người học chỉ ĐỌC, chỉ hàm nền được ghi.",
            ha="center", fontsize=8.4, style="italic", color="#444444")
    luu(fig, "h4_luu_phien")


# ══════════════════════════════════════════════════════════════════ HÌNH 5 ══
def h5_pl_phien():
    """Mỗi lượt một mũi tên P(L) trước → sau. Xanh: đúng. Đỏ: sai."""
    l = SO["luot"]
    fig, ax = plt.subplots(figsize=(12.4, 5.2))
    n = len(l)
    for i, x in enumerate(l):
        mau = "#2f7d32" if x["dung"] else "#b0424d"
        ax.annotate("", xy=(i + 1, x["p"]), xytext=(i + 1, x["pTruoc"]),
                    arrowprops=dict(arrowstyle="-|>", color=mau, linewidth=2.4,
                                    mutation_scale=15))
        ax.plot([i + 1], [x["pTruoc"]], marker="_", markersize=14, color="#888888")
        ax.text(i + 1, max(x["p"], x["pTruoc"]) + 0.035,
                f"{x['p']:.3f}".replace(".", ","), ha="center", fontsize=8.0,
                color=mau, fontweight="bold")
    ax.axhline(0.85, color=LUC_VIEN, linestyle="--", linewidth=1.2)
    ax.axhline(0.30, color=VANG_VIEN, linestyle="--", linewidth=1.2)
    ax.text(n + 0.55, 0.855, "θ = 0,85\nngưỡng tinh thông", fontsize=8.2,
            color=LUC_VIEN, va="bottom")
    ax.text(n + 0.55, 0.305, "θ_yếu = 0,30", fontsize=8.2, color=VANG_VIEN, va="bottom")
    ax.axvspan(8.5, 11.5, color=HONG, alpha=0.5, zorder=0)
    ax.text(10, 0.70, "ba lượt sai liên tiếp tại cùng một nút\n"
                      "→ hàm chính sách π trả về PHỤ ĐẠO",
            ha="center", fontsize=9.0, color=HONG_VIEN, style="italic")
    ax.set_xticks(range(1, n + 1))
    ax.set_xticklabels(
        [f"{i+1}\n{x['item']}\n{x['nut'].replace('v_g3_u13_', '').replace('sp_g3_u13_', 'MC')}"
         for i, x in enumerate(l)], fontsize=7.6)
    ax.set_xlabel("lượt trả lời trong phiên  ·  mã câu  ·  nút được cập nhật",
                  fontsize=9.4, labelpad=10)
    ax.set_ylabel("P(L) — mức tinh thông", fontsize=9.4)
    ax.set_ylim(0, 1.0)
    ax.set_xlim(0.4, n + 2.2)
    ax.grid(axis="y", alpha=0.25)
    ax.set_title("DIỄN BIẾN MỨC TINH THÔNG QUA 11 LƯỢT CỦA MỘT PHIÊN — mỗi mũi tên "
                 "là một lần hàm nền chạy cập nhật Bayes",
                 fontsize=10.2, fontweight="bold")
    ax.text(0.5, -0.29, "Vạch xám là P(L) TRƯỚC lượt ấy (pTruoc), đầu mũi tên là "
                        "P(L) SAU (p). MC1 · MC2 là hai mẫu câu của bài; "
                        "các tên còn lại là mục từ vựng.",
            transform=ax.transAxes, ha="center", fontsize=8.2, style="italic",
            color="#444444")
    fig.tight_layout()
    luu(fig, "h5_pl_phien")


# ══════════════════════════════════════════════════════════════════ HÌNH 6 ══
def h6_lan_truyen():
    fig, ax = khung(12.0, 5.2)
    ung = SO["ungVien"]
    ax.text(0.5, 0.96, "ĐỘ NGỜ CỦA TỪNG ỨNG VIÊN — doNgo(v) = α^bước · (1 − P(L)), "
                       "với α = 0,6",
            ha="center", fontsize=10.4, fontweight="bold")
    n = len(ung)
    cao = 0.68 / n
    for i, u in enumerate(ung):
        y = 0.80 - i * cao
        loai = u["loai"]
        mau = {"chon": LUC_VIEN, "xet": LAM_VIEN, "loai": "#aaaaaa"}[loai]
        nen = {"chon": LUC, "xet": LAM, "loai": XAM}[loai]
        ax.add_patch(FancyBboxPatch(
            (0.02, y), 0.40 * max(u["doNgo"] / ung[0]["doNgo"], 0.06) + 0.005,
            cao * 0.66, boxstyle="round,pad=0.004,rounding_size=0.008",
            facecolor=nen, edgecolor=mau, linewidth=1.1))
        dai = 0.40 * max(u["doNgo"] / ung[0]["doNgo"], 0.06) + 0.005
        so = f"{u['doNgo']:.3f}".replace(".", ",")
        if dai > 0.09:
            ax.text(0.03, y + cao * 0.33, so, ha="left", va="center",
                    fontsize=8.4, fontweight="bold", color=mau)
        else:
            ax.text(0.02 + dai + 0.008, y + cao * 0.33, so, ha="left", va="center",
                    fontsize=8.4, fontweight="bold", color=mau)
        nhan = textwrap.shorten(u["nhan"], 46, placeholder="…")
        ax.text(0.455, y + cao * 0.33,
                f"{u['ma']}   ({nhan})", ha="left", va="center", fontsize=8.2)
        ax.text(0.455, y - cao * 0.06,
                f"bước {u['buoc']} · P(L) = "
                + ("chưa có số → 0,10" if u["p"] is None
                   else f"{u['p']:.3f}".replace(".", ","))
                + " · " + u["ghi_chu"],
                ha="left", va="center", fontsize=7.6, style="italic", color="#555555")
    ax.text(0.02, 0.055,
            "Xanh lá: nút được chọn làm đích phụ đạo.  Xanh dương: được xét nhưng "
            "xếp sau.  Xám: bị LOẠI vì đã đạt ngưỡng tinh thông — một nút người học "
            "làm đúng mãi thì không thể là thủ phạm.",
            ha="left", fontsize=8.2, style="italic", color="#444444")
    luu(fig, "h6_lan_truyen")


def main() -> int:
    print("Dựng hình Chương 3 (bản viết lại):")
    h1_kien_truc()
    h2_thanh_hinh()
    h3_manh_do_thi()
    h4_luu_phien()
    h5_pl_phien()
    h6_lan_truyen()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
