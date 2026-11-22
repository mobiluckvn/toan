"""ĐIỀU PHỐI XƯỞNG — một unit một lượt chạy (việc V12 · mẫu #14 Supervisor).

    python tools/xuong/dieu_phoi.py --lop 4 --unit 3
    python tools/xuong/dieu_phoi.py --lop 4 --unit 3 --kho  # không gọi mạng, in kế hoạch

── DÂY CHUYỀN ──
    1. nạp unit từ `data/tienganh/chuan_lop{N}.json` — chủ đề, vốn đã có, mẫu đã có
    2. worker TỪ MỚI            (một lượt; KHÔNG qua hàng rào — nó định nghĩa vốn)
    3. nới túi chữ bằng từ vừa đề xuất
    4. ba worker còn lại SONG SONG, soi trên túi đã nới
         · mỗi mục qua KHUÔN  (code, miễn phí)
         · rồi qua HÀNG RÀO vốn từ (code, miễn phí)
    5. mỗi mục còn sống → BA GIÁM KHẢO song song
         ≥2 bác → loại · 2–1 → tranh luận 2 vòng · 3 thuận → qua phần sàng
    6. ghi `<ra>/lop{N}_u{NN}.json` (bản nháp) và `<ra>/duyet.md` (cho người đọc)

── ⚠ KHÔNG CÓ BƯỚC 7 ──
Xưởng DỪNG ở đây. Không có đường nào từ đây vào `data/tienganh/chuan_lop{N}.json`,
và tuyệt đối không có đường nào vào `web/public/content/`. Việc tiếp theo là BÁC đọc
`duyet.md`; `chung.soi_duong_ra` chặn mọi đường ra ngoài thư mục xưởng, soi bằng
đường dẫn đã giải nên `../../..` không lách được.

Vì sao chặt thế: một câu sai ở phòng nói thì bé nghe một lần rồi thôi; một câu sai
lọt vào `public/content/` thì mọi bé học nó, mọi lần, cho tới khi có người mở ra đọc.

── VÀ NÓ KHÔNG BAO GIỜ CHẠY LÚC BÉ HỌC ──
Đây là một lệnh dòng lệnh. Không tệp nào trong `web/` nhập nó, và `test_schema.py`
có phép kiểm canh đúng điều ấy — vì "không ai gọi" là thứ sẽ thay đổi lặng lẽ.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chung  # noqa: E402
import giam_khao  # noqa: E402
import hang_rao  # noqa: E402
import nen_worker  # noqa: E402
import tranh_luan as tl  # noqa: E402
import worker_doc_hieu  # noqa: E402
import worker_kich_ban  # noqa: E402
import worker_mau_cau  # noqa: E402
import worker_tu_moi  # noqa: E402

GOC = chung.GOC


# ─────────────────────────── NẠP UNIT ───────────────────────────

def nap_unit(lop: int, so: int) -> dict:
    tep = GOC / f"data/tienganh/chuan_lop{lop}.json"
    if not tep.exists():
        raise chung.LoiXuong(f"không thấy {tep.relative_to(GOC)} — chạy "
                             "tools/chuan_tienganh.py trước")
    d = json.loads(tep.read_text("utf8"))
    for u in d.get("unit") or []:
        if u.get("so") == so:
            return u
    co = sorted(x.get("so") for x in d.get("unit") or [] if x.get("so") is not None)
    raise chung.LoiXuong(f"lớp {lop} không có unit {so}. Có: {co}")


def tui_cua_unit(lop: int, u: dict) -> set[str]:
    """Túi chữ bé đã biết, dựng từ BÀI ĐÃ DỰNG của unit ấy nếu có.

    ⚠ DÙNG BÀI ĐÃ DỰNG (`web/public/content/...`) chứ không dựng lại từ bản chuẩn:
    `hang_rao.tui_chu` gọi `chu_biet()`, mà hàm ấy đọc `knowledgeCore` — hình dạng
    của BÀI, không phải hình dạng của unit trong bản chuẩn. Đưa unit bản chuẩn vào là
    nó trả về túi rỗng, rồi hàng rào bác sạch mọi câu mà không ai hiểu vì sao.

    Chưa có bài đã dựng (unit mới) thì dựng túi từ chính bản chuẩn, bằng tay.
    """
    ma = {1: "ta1", 2: "ta2", 3: "ta3", 4: "ta4", 5: "ta5"}[lop]
    tep = GOC / f"web/public/content/{ma}/DL_TA{lop}_B{u['so']:02d}.json"
    if tep.exists():
        return hang_rao.tui_chu(json.loads(tep.read_text("utf8")), lop)
    tui: set[str] = set()
    for t in u.get("tu") or []:
        for k in ("tu", "so_it", "so_nhieu", "dang_ing", "dang_qk"):
            tui.update(hang_rao.chu_trong(t.get(k)))
    for m in u.get("mau_cau") or []:
        tui.update(hang_rao.chu_trong(m.get("vi_du")))
        tui.update(hang_rao.chu_trong(m.get("cong_thuc")))
    return tui


# ─────────────────────────── CHẠY ───────────────────────────

def chay(*, lop: int, so: int, ra: Path, so_tu: int, kho: bool) -> int:
    u = nap_unit(lop, so)
    chu_de = str(u.get("chu_de") or "").strip()
    canh = str(u.get("canh") or "").strip()
    tui = tui_cua_unit(lop, u)
    mau_da_co = [str(m.get("vi_du") or "") for m in (u.get("mau_cau") or [])]

    print(f"── XƯỞNG · lớp {lop} unit {so} · {chu_de} ──")
    print(f"   túi chữ bé đã biết: {len(tui)} chữ")
    print(f"   mẫu câu đã có     : {len(mau_da_co)}")
    print(f"   đường ra          : {ra.relative_to(GOC)}")
    if kho:
        print("\n   (--kho: in kế hoạch rồi dừng, không gọi mạng)")
        print(f"   sẽ gọi: 1 (từ mới) + 3 (song song) + 3×số mục (giám khảo)")
        return 0

    k = chung.khoa()
    bat_dau = time.time()

    # ── BƯỚC 2 · TỪ MỚI ──
    print("\n   [1/3] worker từ mới…", flush=True)
    r_tu = worker_tu_moi.soan(lop=lop, chu_de=chu_de, canh=canh, tui=tui,
                             so_tu=so_tu, khoa_api=k)
    tu_moi = r_tu["qua"]
    print(f"         {len(tu_moi)} từ qua khuôn · {len(r_tu['bac'])} bị bác"
          + (f" · LỖI: {r_tu['loi']}" if r_tu["loi"] else ""))

    # ── BƯỚC 3+4 · BA WORKER SONG SONG, TRÊN TÚI ĐÃ NỚI ──
    tui_noi = set(tui) | {
        c for t in tu_moi for k2 in ("tu", "so_it", "so_nhieu", "dang_ing", "dang_qk")
        for c in hang_rao.chu_trong(t.get(k2))
    }
    mau_cho_kb = mau_da_co or []
    print(f"   [2/3] ba worker song song (túi nới thành {len(tui_noi)} chữ)…", flush=True)
    with ThreadPoolExecutor(max_workers=3) as bom:
        f_mau = bom.submit(worker_mau_cau.soan, lop=lop, chu_de=chu_de, tui=tui_noi,
                           tu_moi=tu_moi, mau_da_co=mau_da_co, khoa_api=k)
        f_kb = bom.submit(worker_kich_ban.soan, lop=lop, chu_de=chu_de, canh=canh,
                          tui=tui_noi, tu_moi=tu_moi, mau=mau_cho_kb, khoa_api=k)
        f_dh = bom.submit(worker_doc_hieu.soan, lop=lop, chu_de=chu_de, tui=tui_noi,
                          tu_moi=tu_moi, khoa_api=k)
        r_mau, r_kb, r_dh = f_mau.result(), f_kb.result(), f_dh.result()

    phan = {"tu": r_tu, "mau_cau": r_mau, "kich_ban": r_kb, "doc_hieu": r_dh}
    for ten, r in phan.items():
        print(f"         {ten:10s} {len(r['qua'])} qua · {len(r['bac'])} bị bác"
              + (f" · LỖI: {r['loi']}" if r["loi"] else ""))

    # ── BƯỚC 5 · GIÁM KHẢO ──
    bang = nen_worker.bang_tu(tui_noi)
    viec = [(loai, m) for loai, r in phan.items() for m in r["qua"]]
    print(f"   [3/3] {len(viec)} mục × 3 giám khảo…", flush=True)
    xet_ds = []
    with ThreadPoolExecutor(max_workers=4) as bom:
        for (loai, m), kq in zip(viec, bom.map(
                lambda x: giam_khao.xet(x[1], loai=x[0], lop=lop, chu_de=chu_de,
                                        bang=bang, khoa_api=k), viec)):
            xet_ds.append({"loai": loai, "muc": m, **kq})

    # Phiếu 2–1 → tranh luận. Chạy sau, nối tiếp: số mục 2–1 thường ít, và mỗi mục
    # tốn hai lượt nối nhau nên song song ở đây không giúp nhiều.
    for x in xet_ds:
        if x["ket"] != "tranh_luan":
            continue
        ly_do = next((p["ly_do"] for p in x["phieu"] if p["thuan"] is False), "")
        x["tranh_luan"] = tl.tranh_luan(x["muc"], loai=x["loai"], lop=lop,
                                        chu_de=chu_de, ly_do_bac=ly_do, khoa_api=k)

    giay = time.time() - bat_dau
    ghi(ra, lop=lop, so=so, chu_de=chu_de, u=u, phan=phan, xet_ds=xet_ds,
        tui=tui, tui_noi=tui_noi, giay=giay)
    print(f"\n   xong trong {giay:.0f}s")
    chung.in_dem()
    print(f"\n   ĐỌC TIẾP: {(ra / f'duyet_lop{lop}_u{so:02d}.md').relative_to(GOC)}")
    return 0


# ─────────────────────────── GHI ───────────────────────────

def ghi(ra: Path, *, lop: int, so: int, chu_de: str, u: dict, phan: dict,
        xet_ds: list, tui: set, tui_noi: set, giay: float) -> None:
    ra.mkdir(parents=True, exist_ok=True)
    ten = f"lop{lop}_u{so:02d}"

    qua = [x for x in xet_ds if x["ket"] == "qua"]
    ban = [x for x in xet_ds if x["ket"] == "tranh_luan"]
    loai = [x for x in xet_ds if x["ket"] == "loai"]
    thieu = [x for x in xet_ds if x["ket"] == "thieu_phieu"]

    nhap = {
        "_doc": ("BẢN NHÁP DO XƯỞNG SOẠN — CHƯA ĐƯỢC DUYỆT. Không rót vào "
                 "data/tienganh/chuan_lopN.json trước khi đọc duyet.md."),
        "lop": lop, "unit": so, "chu_de": chu_de,
        "mo_hinh": chung.MO_HINH, "giay": round(giay, 1),
        "tui_chu": {"truoc": len(tui), "sau_khi_nhan_tu_moi": len(tui_noi)},
        "qua_sang": {
            "tu": [x["muc"] for x in qua if x["loai"] == "tu"],
            "mau_cau": [x["muc"] for x in qua if x["loai"] == "mau_cau"],
            "kich_ban": [x["muc"] for x in qua if x["loai"] == "kich_ban"],
            "doc_hieu": [x["muc"] for x in qua if x["loai"] == "doc_hieu"],
        },
        "con_ban": [{"loai": x["loai"], "muc": x["muc"], "phieu": x["phieu"],
                     "tranh_luan": x.get("tranh_luan")} for x in ban],
        "bi_loai": [{"loai": x["loai"], "muc": x["muc"], "phieu": x["phieu"]}
                    for x in loai],
        "thieu_phieu": [{"loai": x["loai"], "muc": x["muc"], "phieu": x["phieu"]}
                        for x in thieu],
        "bac_boi_code": {k: v["bac"] for k, v in phan.items() if v["bac"]},
        "loi_worker": {k: v["loi"] for k, v in phan.items() if v["loi"]},
    }
    (ra / f"{ten}.json").write_text(
        json.dumps(nhap, ensure_ascii=False, indent=1) + "\n", "utf8")

    # ⚠ MỖI UNIT MỘT TỆP DUYỆT. Bản cũ ghi `duyet.md` chung, nên chạy unit sau là
    # đè mất danh sách chờ duyệt của unit trước khi chưa ai đọc.
    (ra / f"duyet_{ten}.md").write_text(bao_cao(
        ten=ten, lop=lop, so=so, chu_de=chu_de, phan=phan,
        qua=qua, ban=ban, loai=loai, giay=giay, thieu=thieu), "utf8")


def _mot_dong(loai: str, m: dict) -> str:
    if loai == "tu":
        return f'`{m.get("tu")}` — {m.get("nghia")}'
    if loai == "mau_cau":
        return f'`{m.get("vi_du")}`  (công thức: `{m.get("cong_thuc")}`)'
    if loai == "kich_ban":
        return f'{m.get("ten")} — {len(m.get("buoc") or [])} bước'
    doan = m.get("doan") or []
    return f'bài đọc {len(doan)} câu, {len(m.get("cau") or [])} câu hỏi'


def bao_cao(*, ten: str, lop: int, so: int, chu_de: str, phan: dict,
            qua: list, ban: list, loai: list, giay: float, thieu: list = ()) -> str:
    d = [
        f"# Chờ duyệt · lớp {lop} unit {so} · {chu_de}",
        "",
        f"Xưởng soạn xong trong {giay:.0f} giây, mô hình `{chung.MO_HINH}`.",
        "",
        "> **Chưa có gì vào nội dung thật.** Bản nháp nằm ở `" + ten + ".json`.",
        "> Đọc danh sách dưới đây, chọn mục nào giữ, rồi mới rót vào",
        "> `data/tienganh/chuan_lop" + str(lop) + ".json` và chạy bộ sinh + cổng kiểm.",
        "",
        "| | số mục |",
        "|---|---|",
        f"| ba giám khảo đều thuận | {len(qua)} |",
        f"| **còn bàn (phiếu 2–1)** | **{len(ban)}** |",
        f"| bị loại (≥2 bác) | {len(loai)} |",
        f"| **thiếu phiếu (giám khảo gọi hỏng)** | **{len(thieu)}** |",
        f"| bị code bác trước giám khảo | {sum(len(v['bac']) for v in phan.values())} |",
        "",
        "⚠ **Ba giám khảo đều thuận KHÔNG phải một phép duyệt.** Đó là ba lượt gọi",
        "cùng một mô hình với ba lời dặn khác nhau — chúng không độc lập, nên \"ba",
        "thuận\" chỉ là một phép SÀNG để bác đọc ít hơn.",
        "",
    ]

    if ban:
        d += ["## Còn bàn — đọc trước, mấy mục này cần bác quyết", ""]
        for x in ban:
            p_bac = next((p for p in x["phieu"] if p["thuan"] is False), {})
            t = x.get("tranh_luan") or {}
            d += [
                f"### {x['loai']} · {_mot_dong(x['loai'], x['muc'])}",
                "",
                f"- **Chiều bị bác:** {giam_khao.TEN.get(p_bac.get('chieu'), '?')}",
                f"- **Lý do bác:** {p_bac.get('ly_do') or '(không ghi)'}",
            ]
            for v in t.get("vong") or []:
                nhan = "đáp lại" if v["phia"] == "thuan" else "sau khi đọc câu đáp"
                them = ""
                if v["phia"] == "bac":
                    them = " · **vẫn bác**" if v.get("giu_y") else " · **bỏ lời bác**"
                d.append(f"- **{nhan}{them}:** {v.get('chu') or '(không có)'}")
            if t.get("mot_model"):
                d.append("- ⚠ *Hai phía tranh luận dùng CÙNG một mô hình* — chưa đặt "
                         "mô hình phụ, nên lập luận hai bên kém "
                         "độc lập hơn thiết kế muốn. Đặt `LLM_MODEL_PHU` để có hai "
                         "model thật.")
            d += ["", "```json", json.dumps(x["muc"], ensure_ascii=False, indent=1),
                  "```", ""]

    if thieu:
        d += ["## Thiếu phiếu — giám khảo gọi hỏng, CHƯA ai soát mục này", "",
              "Không phải \"qua\": ít nhất một giám khảo không trả lời được. Đọc kỹ",
              "như một mục chưa được sàng, hoặc chạy lại xưởng cho unit này.", ""]
        for x in thieu:
            hong = "; ".join(f"{giam_khao.TEN.get(p['chieu'], '?')}: {p['loi']}"
                             for p in x["phieu"] if p["thuan"] is None)
            d.append(f"- **{x['loai']}** · {_mot_dong(x['loai'], x['muc'])} — {hong}")
        d.append("")

    if qua:
        d += ["## Ba giám khảo đều thuận", ""]
        for x in qua:
            d.append(f"- **{x['loai']}** · {_mot_dong(x['loai'], x['muc'])}")
        d.append("")

    if loai:
        d += ["## Bị loại (≥2 giám khảo bác)", ""]
        for x in loai:
            ly = "; ".join(p["ly_do"] for p in x["phieu"] if p["thuan"] is False and p["ly_do"])
            d.append(f"- **{x['loai']}** · {_mot_dong(x['loai'], x['muc'])} — {ly or '(không ghi lý do)'}")
        d.append("")

    bac_code = {k: v["bac"] for k, v in phan.items() if v["bac"]}
    if bac_code:
        d += ["## Bị CODE bác trước khi tới giám khảo", "",
              "Mấy mục này không tốn lượt gọi giám khảo nào — khuôn hay hàng rào vốn",
              "từ đã bác. Đọc để biết mô hình đang hay sai chỗ nào, rồi sửa LỜI DẶN",
              "của worker, đừng nới phép soi.", ""]
        for k, ds in bac_code.items():
            for x in ds:
                d.append(f"- **{k}** · {x.get('tang', '?')} — " + "; ".join(x["ly_do"]))
        d.append("")

    loi = {k: v["loi"] for k, v in phan.items() if v["loi"]}
    if loi:
        d += ["## Worker trượt hẳn", ""]
        d += [f"- **{k}** — {v}" for k, v in loi.items()]
        d.append("")

    d += [
        "---", "",
        "## Giữ mục nào thì làm thế này", "",
        "**1 · Tự gõ một tệp chọn.** Không đưa `" + ten + ".json` vào bộ sinh: tệp ấy",
        "có cả phần còn bàn và phần bị loại. Gõ một tệp mới chỉ gồm những mục bác giữ:", "",
        "```json",
        '{ "tu": [ … ], "mau_cau": [ … ] }',
        "```", "",
        "Chính việc gõ tệp ấy LÀ hành động duyệt.", "",
        "**2 · Đắp vào rồi dựng bài:**", "",
        "```bash",
        f"python tools/sinh_bai_tienganh.py --lop {lop} --unit {so} --xuong <tệp chọn>",
        "```", "",
        "`--xuong` KHÔNG sửa `data/tienganh/chuan_lop" + str(lop) + ".json` trên đĩa —",
        "nó đắp trong bộ nhớ rồi dựng. Muốn vào bản chuẩn thì phải đi qua bản đồ",
        "chương trình, và đó là việc khác.", "",
        "**3 · ⚠ MỘT TỪ MỚI KÉO THEO BỐN DÂY CHUYỀN NỮA.** Đo thật: đắp 4 từ vào một",
        "unit lớp 4 rồi chạy cổng thì SÁU tệp cổng đỏ, và cả sáu đỏ đúng chỗ phải đỏ:", "",
        "| cổng đỏ | vì sao | phải làm gì |",
        "|---|---|---|",
        "| `tienganh_am` · `tienganh_hai_loi_22_08` | từ mới chưa có clip đọc | chạy dây chuyền âm |",
        "| `tienganh_dothi` · `tienganh_manut` | nút tri thức mới chưa có trong đồ thị | cập nhật đồ thị |",
        "| `tienganh_hinh_dung_tu` | chưa có hình, và chưa ai SOÁT TẬN MẮT hình ấy | vẽ hình, rồi **người** soát |",
        "| `tienganh_video` | video từ mới chưa render | chạy dây chuyền video |", "",
        "Nên đừng đọc \"qua 83 cổng\" thành \"chạy bộ sinh là xong\". Một mục `mau_cau`",
        "thì nhẹ; một từ MỚI là năm bước, và bước cuối là mắt người.", "",
        "**4 · Cuối cùng:**", "",
        "```bash",
        "cd web && npm run build && npm test",
        "```", ""]
    return "\n".join(d)


def main() -> int:
    p = argparse.ArgumentParser(description="Xưởng sinh nội dung tiếng Anh (offline)")
    p.add_argument("--lop", type=int, required=True, choices=[1, 2, 3, 4, 5])
    p.add_argument("--unit", type=int, required=True)
    p.add_argument("--ra", default=None,
                   help="thư mục đầu ra; mặc định data/tienganh/xuong")
    p.add_argument("--so-tu", type=int, default=8, help="số từ mới muốn đề xuất")
    p.add_argument("--kho", action="store_true",
                   help="in kế hoạch rồi dừng, KHÔNG gọi mạng")
    a = p.parse_args()
    try:
        ra = chung.soi_duong_ra(a.ra or chung.RA_CHO_PHEP)
        return chay(lop=a.lop, so=a.unit, ra=ra, so_tu=a.so_tu, kho=a.kho)
    except chung.LoiXuong as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
