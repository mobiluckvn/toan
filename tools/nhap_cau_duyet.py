#!/usr/bin/env python3
"""ĐƯỜNG RA CỦA HÀNG ĐỢI DUYỆT CÂU PHỤ ĐẠO (`choDuyetTA`).

    export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json
    python3 tools/nhap_cau_duyet.py --lay                 # kéo hàng đợi về, viết phiếu đọc
    python3 tools/nhap_cau_duyet.py --nhap chon.json      # xem thử: ghép gì, bỏ gì
    python3 tools/nhap_cau_duyet.py --nhap chon.json --ghi  # ghi thật vào kho nguồn

── VIỆC NÀY LÀ GÌ, VÀ VÌ SAO NÓ CẦN ──
Việc V9 cho mô hình soạn câu phụ đạo khi kho tĩnh không đủ. Câu ấy là câu DUY NHẤT
trong app không đi qua bộ sinh và 103 cổng, nên nó phải nằm chờ người lớn đọc:
`firestore.rules` cho bé GHI vào `choDuyetTA` mà KHÔNG cho đọc. Từ 09-10-2026 hàng
đợi ấy có đường vào mà chưa có đường ra — nó chỉ đầy lên. Tệp này là đường ra.

── BA CHỐT, CÙNG LẼ VỚI `--xuong` CỦA BỘ SINH ──

1 · KHÔNG SỬA TỆP BÀI ĐÃ DỰNG (`web/public/content/**`). Bản dựng lại sau sẽ đè mất
    — bẫy `ban-dung-lai-de-mat-ban-sua-tay` đã dính bốn lần. Câu duyệt rồi đi vào
    KHO NGUỒN `data/tienganh/cau_duyet.json`, và `sinh_bai_tienganh.py` đắp nó vào
    pool lúc dựng.

2 · ĐỌC TỆP BÁC ĐƯA, KHÔNG ĐỌC THẲNG HÀNG ĐỢI. `--lay` chỉ viết ra phiếu để đọc;
    muốn câu nào vào kho thì bác GÕ TÊN NÓ vào `chon.json`. Chính việc gõ tệp ấy LÀ
    hành động duyệt — hàng đợi mà tự chảy vào kho thì nó không còn là hàng đợi duyệt.

3 · HẬU KIỂM LẠI BẰNG CHÍNH `soiCauAI` CỦA APP, không chép luật sang Python. Hai bản
    luật rồi sẽ trôi xa nhau, mà lệch ở đây thì câu hỏng lọt vào kho tĩnh và từ đó
    trở đi không ai soi nữa. Nên tệp này gọi `node` chạy đúng hàm ấy.

⚠ TỆP NÀY KHÔNG XOÁ GÌ TRÊN MÁY CHỦ. Hàng đợi giữ nguyên; `--nhap` chỉ ghi vào kho
   nguồn tại máy. Muốn dọn hàng đợi thì đó là việc khác, có công cụ khác.

⚠ VÀ `--lay` IN RA CÂU DO BÉ CÓ THẬT SINH RA. Chạy trên máy bác thì được; đừng dán
   nguyên `learnerId` vào tài liệu nộp.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
KHO_NGUON = GOC / "data/tienganh/cau_duyet.json"
THU_MUC_PHIEU = GOC / "data/tienganh/cho_duyet"
NOI_DUNG = GOC / "web/public/content"

CACH_LAY_KHOA = (
    "  Firebase Console → ⚙ Project settings → Service accounts →\n"
    '  "Generate new private key", lưu thành ~/khoa-dich-vu.json rồi:\n'
    "      export GOOGLE_APPLICATION_CREDENTIALS=~/khoa-dich-vu.json"
)

# ── ĐỌC FIRESTORE BẰNG NODE, KHÔNG BẰNG PYTHON ──
# Máy này không có `google-cloud-firestore`, mà `web/functions` thì đã có
# `firebase-admin` sẵn — thêm một thư viện Python nữa chỉ để đọc một kho là thêm một
# thứ phải cài lại trên mỗi máy. Mọi công cụ Firestore khác của kho (`soi_ban_ghi_*`,
# `xoa_log_*`) cũng mượn đúng bản ấy; đi theo cho đồng.
JS_DOC = r"""
import { createRequire } from 'node:module';
const doi = createRequire(process.argv[1]);
const { initializeApp, cert } = doi('firebase-admin/app');
const { getFirestore } = doi('firebase-admin/firestore');
initializeApp({ credential: cert(JSON.parse(await import('node:fs')
  .then(m => m.readFileSync(process.env.GOOGLE_APPLICATION_CREDENTIALS, 'utf8')))) });
const snap = await getFirestore().collection('choDuyetTA').get();
const ra = [];
snap.forEach((d) => ra.push({ _id: d.id, ...d.data() }));
process.stdout.write(JSON.stringify(ra));
"""


def _loi(*dong: str) -> None:
    for d in dong:
        print(d, file=sys.stderr)
    sys.exit(1)


def lay_hang_doi(tu_tep: str | None) -> list[dict]:
    """Kéo cả kho `choDuyetTA` về. `--tu-tep` để chạy thử mà không cần mạng."""
    if tu_tep:
        return json.loads(Path(tu_tep).read_text("utf8"))
    import os

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        _loi("✗ thiếu GOOGLE_APPLICATION_CREDENTIALS.", CACH_LAY_KHOA)
    r = subprocess.run(
        ["node", "--input-type=module", "-e", JS_DOC,
         str(GOC / "web/functions/package.json")],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        _loi("✗ đọc Firestore hỏng:", r.stderr.strip()[:800])
    return json.loads(r.stdout or "[]")


# ─────────── BẢN ĐỒ NÚT → BÀI ───────────

def ban_do_nut() -> dict[str, str]:
    """Nút tri thức nằm ở bài nào — đọc từ CHÍNH tệp bài đã dựng.

    Mã nút có dạng `v_g3_u1_hello` nên suy ra bài bằng chuỗi cũng được, nhưng suy
    bằng quy ước là tin vào một quy ước; đọc tệp là đọc sự thật. Phép suy chỉ dùng
    làm đường lui, và nếu cả hai đều không ra thì câu ấy BỊ BỎ chứ không đoán bừa —
    đặt một câu vào nhầm bài thì bé gặp nó ở chỗ chưa học tới.
    """
    ra: dict[str, str] = {}
    for tep in sorted(NOI_DUNG.glob("ta*/DL_*.json")):
        d = json.loads(tep.read_text("utf8"))
        ma_bai = d.get("id")
        if not ma_bai:
            continue
        for t in (d.get("knowledgeCore", {}).get("vocabulary") or []):
            if t.get("ma"):
                ra.setdefault(t["ma"], ma_bai)
        for pool in (d.get("practice", {}).get("pools") or {}).values():
            for c in pool:
                for m in [c.get("maNut"), *(c.get("maNutDs") or [])]:
                    if m:
                        ra.setdefault(m, ma_bai)
    return ra


def _bai_co_that() -> set[str]:
    """Mã mọi bài CÓ THẬT trên đĩa. Đường lui phải đối chiếu với tập này."""
    return {json.loads(t.read_text("utf8")).get("id")
            for t in NOI_DUNG.glob("ta*/DL_*.json")} - {None}


def bai_cua_nut(ma_nut: str, bd: dict[str, str], co_that: set[str] | None = None) -> str | None:
    if ma_nut in bd:
        return bd[ma_nut]
    # ── ĐƯỜNG LUI: suy từ chính mã nút (`v_g3_u1_hello` → bài 1 của lớp 3) ──
    # ⚠ VÀ PHẢI ĐỐI CHIẾU VỚI BÀI CÓ THẬT. Bản đầu không đối chiếu, nên một nút rác
    # `v_g9_u9_...` suy ra `DL:TA9.B09` — một quyển lớp 9 không tồn tại — rồi phiếu
    # đọc bày ra mã ấy như thể có thật. Không ra bài thì trả `None` để câu bị BỎ,
    # chứ đoán bừa thì câu rơi vào chỗ bé chưa học tới.
    m = re.match(r"^[a-z]+_g(\d+)_u([a-z0-9]+)_", ma_nut or "")
    if not m:
        return None
    lop, u = m.group(1), m.group(2)
    so = 0 if u == "starter" else (int(u) if u.isdigit() else None)
    if so is None:
        return None
    ma_bai = f"DL:TA{lop}.B{so:02d}"
    return ma_bai if ma_bai in (co_that if co_that is not None else _bai_co_that()) else None


# ─────────── HẬU KIỂM BẰNG CHÍNH LUẬT CỦA APP ───────────

JS_SOI = r"""
import { soiCauAI } from '%s';
const ds = JSON.parse(process.argv[1]);
process.stdout.write(JSON.stringify(ds.map((c) => soiCauAI(c))));
"""


def soi_bang_app(ds: list[dict]) -> list[dict]:
    """Chạy `soiCauAI` THẬT của app lên từng câu. Xem chốt 3 ở đầu tệp."""
    if not ds:
        return []
    duong = (GOC / "web/src/mon/tienganh/lib/phudao.js").as_uri()
    r = subprocess.run(
        ["node", "--input-type=module", "-e", JS_SOI % duong, json.dumps(ds)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        _loi("✗ không chạy được soiCauAI của app:", r.stderr.strip()[:800])
    return json.loads(r.stdout or "[]")


# ─────────── --lay: viết phiếu để người lớn đọc ───────────

def viet_phieu(hang: list[dict]) -> tuple[Path, Path]:
    THU_MUC_PHIEU.mkdir(parents=True, exist_ok=True)
    tho = THU_MUC_PHIEU / "hang_doi.json"
    phieu = THU_MUC_PHIEU / "duyet.md"
    tho.write_text(json.dumps(hang, ensure_ascii=False, indent=1), "utf8")

    bd = ban_do_nut()
    co_that = _bai_co_that()
    cau = [h.get("cau") or {} for h in hang]
    soi = soi_bang_app(cau)
    da_co = {c["id"] for c in doc_kho_nguon().get("cau", [])}

    d = [
        "# HÀNG ĐỢI DUYỆT CÂU PHỤ ĐẠO",
        "",
        f"Kéo về lúc {datetime.now().astimezone().strftime('%H:%M %d-%m-%Y')} · "
        f"{len(hang)} câu.",
        "",
        "Đọc rồi GÕ một tệp `chon.json` chỉ gồm câu muốn giữ — chính việc gõ tệp ấy",
        "là hành động duyệt:",
        "",
        "```json",
        '{ "giu": ["<mã>", "<mã>"] }',
        "```",
        "",
        "Muốn sửa lời dẫn hay phương án thì thay chuỗi bằng cả mục, giữ nguyên `_id`.",
        "",
        "⚠ Luật thứ bảy — *phương án nhiễu có thật là cái sai trẻ hay mắc hay chỉ là",
        "một chữ bừa* — KHÔNG máy nào kiểm được. Đó là việc của mắt bác, và là lý do",
        "hàng đợi này tồn tại. Nhìn kỹ xem có **hai đáp án cùng đúng** không: *“Nói",
        "lời chào” → `hello`* trong khi `hi` cũng là lời chào.",
        "",
    ]
    for h, c, s in zip(hang, cau, soi):
        bai = bai_cua_nut(str(c.get("maNut") or h.get("maNut") or ""), bd, co_that)
        dap = (c.get("answerKey") or {})
        dap = dap.get("choice") if isinstance(dap, dict) else dap
        co = []
        if not s.get("ok"):
            co.append(f"🤖 máy bác: {s.get('vi')}")
        if h["_id"] in da_co:
            co.append("⏭ đã có trong kho nguồn")
        if not bai:
            co.append("⚠ không suy ra được bài — sẽ bị bỏ")
        d += [
            f"## `{h['_id']}`",
            "",
            f"- **bài**: {bai or '—'} · **nút**: `{c.get('maNut') or h.get('maNut')}`",
            f"- **lời dẫn**: {c.get('text') or '—'}",
            f"- **phương án**: {' · '.join(c.get('choices') or []) or '—'}",
            f"- **đáp án**: `{dap or '—'}`",
            f"- **gợi ý**: {' / '.join(c.get('hints') or []) or '—'}",
            f"- **lúc**: {h.get('at') or '—'}",
        ]
        if co:
            d.append("- " + " · ".join(co))
        d.append("")
    phieu.write_text("\n".join(d), "utf8")
    return phieu, tho


# ─────────── --nhap: ghép câu đã duyệt vào kho nguồn ───────────

def doc_kho_nguon() -> dict:
    if KHO_NGUON.exists():
        return json.loads(KHO_NGUON.read_text("utf8"))
    return {
        "_doc": [
            "CÂU PHỤ ĐẠO DO MÔ HÌNH SOẠN, BÁC ĐÃ DUYỆT TỪNG CÂU.",
            "",
            "Vào đây qua `tools/nhap_cau_duyet.py --nhap`, ra ở `sinh_bai_tienganh.py`",
            "(đắp vào pool `warmup` của đúng bài). KHÔNG sửa tay tệp bài đã dựng.",
            "",
            "Mỗi mục giữ `nguon: ai` để app hậu kiểm lại lúc chạy, và để còn lần ra",
            "câu nào không do bộ sinh đẻ ra.",
        ],
        "cau": [],
    }


def ma_moi(ma_nut: str, da_dung: set[str]) -> str:
    n = 1
    while f"pd_{ma_nut}_{n}" in da_dung:
        n += 1
    return f"pd_{ma_nut}_{n}"


def nhap(tep_chon: str, ghi: bool) -> int:
    chon = json.loads(Path(tep_chon).read_text("utf8"))
    giu = chon.get("giu") if isinstance(chon, dict) else chon
    if not isinstance(giu, list) or not giu:
        _loi('✗ tệp chọn phải có `{"giu": [...]}` và không rỗng.')

    tho_tep = THU_MUC_PHIEU / "hang_doi.json"
    if not tho_tep.exists():
        _loi("✗ chưa có hàng đợi tại máy. Chạy `--lay` trước.")
    hang = {h["_id"]: h for h in json.loads(tho_tep.read_text("utf8"))}

    kho = doc_kho_nguon()
    da_co = {c["id"] for c in kho["cau"]}
    bd = ban_do_nut()
    co_that = _bai_co_that()

    nhan, bo = [], []
    for g in giu:
        ma = g if isinstance(g, str) else g.get("_id")
        goc = hang.get(ma)
        if not goc:
            bo.append((ma, "không có trong hàng đợi đã kéo về"))
            continue
        c = dict(goc.get("cau") or {})
        if isinstance(g, dict):                 # bác sửa tay thì lấy bản bác sửa
            c.update({k: v for k, v in g.items() if k != "_id"})
        ma_nut = str(c.get("maNut") or goc.get("maNut") or "")
        bai = bai_cua_nut(ma_nut, bd, co_that)
        if not bai:
            bo.append((ma, f"không suy ra được bài cho nút `{ma_nut}`"))
            continue
        nhan.append((ma, bai, ma_nut, c))

    # Hậu kiểm bằng chính luật của app — CHỐT 3.
    for (ma, bai, ma_nut, c), s in zip(nhan[:], soi_bang_app([x[3] for x in nhan])):
        if not s.get("ok"):
            nhan.remove((ma, bai, ma_nut, c))
            bo.append((ma, f"soiCauAI bác: {s.get('vi')}"))

    them = []
    for ma, bai, ma_nut, c in nhan:
        idm = ma_moi(ma_nut, da_co)
        da_co.add(idm)
        them.append({
            "bai": bai,
            "id": idm,
            "maNut": ma_nut,
            "maNutDs": c.get("maNutDs") or [ma_nut],
            "format": "chon",
            "text": c.get("text"),
            "choices": c.get("choices"),
            "answerKey": c.get("answerKey"),
            "hints": c.get("hints") or [],
            "nguon": "ai",
            "tuHangDoi": ma,
            "duyetLuc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    print(f"  nhận {len(them)} câu · bỏ {len(bo)} câu")
    for t in them:
        print(f"    ✔ {t['bai']} · {t['maNut']} · {str(t['text'])[:46]}")
    for ma, vi in bo:
        print(f"    ✗ {ma} — {vi}")

    if not ghi:
        print("\n  (xem thử — chưa ghi gì. Thêm `--ghi` để ghi thật.)")
        return 0
    kho["cau"].extend(them)
    KHO_NGUON.parent.mkdir(parents=True, exist_ok=True)
    KHO_NGUON.write_text(json.dumps(kho, ensure_ascii=False, indent=1), "utf8")
    print(f"\n  đã ghi {KHO_NGUON.relative_to(GOC)} — nay có {len(kho['cau'])} câu.")
    print("  Dựng lại bài thì câu mới vào pool:")
    print("      python3 tools/sinh_bai_tienganh.py --lop <N>")
    return len(them)


def tu_kiem() -> None:
    """Phép tự kiểm, chạy offline. Canh đúng hai chỗ dễ sai mà im lặng.

    Cả hai đều hỏng theo kiểu không ai thấy: đoán nhầm bài thì câu rơi vào chỗ bé
    chưa học tới, còn trùng mã thì câu sau đè câu trước trong pool.
    """
    bd, co_that = {}, {"DL:TA3.B01", "DL:TA3.B00"}
    ca = [
        ("v_g3_u1_hello", "DL:TA3.B01", "suy từ mã nút"),
        ("v_g3_ustarter_eight", "DL:TA3.B00", "unit starter → bài 00"),
        ("v_g9_u9_rac", None, "lớp không có thật thì KHÔNG đoán"),
        ("v_g3_u7_x", None, "bài không có trên đĩa thì KHÔNG đoán"),
        ("rac", None, "mã không đúng khuôn"),
        ("", None, "mã rỗng"),
    ]
    for ma, mong, vi in ca:
        duoc = bai_cua_nut(ma, bd, co_that)
        assert duoc == mong, f"bai_cua_nut({ma!r}) ra {duoc!r}, mong {mong!r} — {vi}"
    # bản đồ đọc từ tệp phải THẮNG phép suy
    assert bai_cua_nut("v_g9_u9_rac", {"v_g9_u9_rac": "DL:TA3.B01"}, co_that) == "DL:TA3.B01"

    da = {"pd_v_g3_u1_how_1", "pd_v_g3_u1_how_2"}
    assert ma_moi("v_g3_u1_how", da) == "pd_v_g3_u1_how_3"
    assert ma_moi("v_g3_u1_new", da) == "pd_v_g3_u1_new_1"
    print("  tự kiểm: ĐẠT —", len(ca) + 3, "phép")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--lay", action="store_true", help="kéo hàng đợi về và viết phiếu đọc")
    p.add_argument("--tu-tep", default=None,
                   help="đọc hàng đợi từ một tệp JSON thay vì Firestore (để chạy thử)")
    p.add_argument("--nhap", default=None, metavar="chon.json",
                   help="ghép câu BÁC ĐÃ DUYỆT vào kho nguồn")
    p.add_argument("--ghi", action="store_true",
                   help="ghi thật (mặc định chỉ in ra xem thử)")
    p.add_argument("--tu-kiem", action="store_true", help="chạy phép tự kiểm, không cần mạng")
    a = p.parse_args()

    if a.tu_kiem:
        tu_kiem()
    elif a.lay:
        hang = lay_hang_doi(a.tu_tep)
        if not hang:
            print("  hàng đợi rỗng — chưa có câu nào chờ duyệt.")
            return
        phieu, tho = viet_phieu(hang)
        print(f"  {len(hang)} câu trong hàng đợi.")
        print(f"  phiếu đọc : {phieu.relative_to(GOC)}")
        print(f"  bản thô   : {tho.relative_to(GOC)}")
        print("\n  Đọc phiếu, rồi gõ `chon.json` chỉ gồm câu muốn giữ.")
    elif a.nhap:
        nhap(a.nhap, a.ghi)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
