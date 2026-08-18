#!/usr/bin/env python3
"""DỰNG BÀI ĐỌC HIỂU NGẮN — mỗi chương một bài.

    python3 tools/sinh_dochieu_tienganh.py --lop 3
    python3 tools/sinh_dochieu_tienganh.py --lop 3 --thieu /tmp/loi.json   # lời chưa có clip

Bác chốt 18-08-2026: mỗi chương một đoạn đọc 4–6 câu, dựng CHỈ từ vốn từ đã học
(lớp 1 + lớp 2 + lớp 3 tính tới chương ấy), rồi hỏi Ý CHÍNH và hỏi CHI TIẾT.

── LUẬT SỐ MỘT: KHÔNG BỊA CÂU TIẾNG ANH ──

Đoạn đọc KHÔNG phải văn mới. Mỗi dòng là một câu SẴN CÓ của chính bốn bài trong
chương (`canonicalExamples`), cắt đôi ở cặp hỏi–đáp. Đây là luật xuyên suốt cả môn,
và đã có hai lần trả giá: mô hình sinh `"Bye, bike."` (nhét đồ vật vào ô tên người),
và bộ sinh bài đầu tiên đẻ ra `"facePoint to your hand."` Câu có sẵn thì:

  · chắc chắn đúng ngữ pháp — người soạn sách đã duyệt;
  · chắc chắn nằm trong vốn từ đã học;
  · và CÓ SẴN CLIP TIẾNG, không phải chạy lại cả dây chuyền TTS cho một đoạn văn.

Xếp bốn tới sáu câu ấy cạnh nhau theo đúng thứ tự unit thì tự nó thành một mẩu hội
thoại đọc được:

    Hello. I'm Ben.
    Hello, Ben. I'm Lucy.
    How are you?
    Fine, thank you.

── BỐN CÂU HỎI, BA DẠNG, VÀ VÌ SAO ĐÚNG BA DẠNG ẤY ──

**Ý chính** — "Bài đọc này nói về chuyện gì?", bốn lựa chọn là TÊN CHƯƠNG (tiếng
Việt) của chương này và ba chương khác. Hỏi ý chính mà đáp án là một câu trong bài
thì đó không phải ý chính, đó là chi tiết. Tên chương chính là ý chính, và nó có
sẵn — không phải soạn thêm dòng nào.

**Chi tiết · câu nào CÓ trong bài** (hai câu) — ba tới bốn câu tiếng Anh, mồi là câu
CÙNG KHUÔN khác từ (`I have a pen.` ↔ `I have a book.`). Mồi cùng khuôn buộc bé phải
đọc lại đoạn để tìm đúng chi tiết; mồi khác khuôn thì bé loại được bằng hình dạng
câu, không cần đọc lấy một chữ.

**Chi tiết · có hay không** — một câu KHÔNG có trong đoạn, hỏi "câu này có trong bài
đọc không?", hai lựa chọn Có/Không. Đáp án cố ý là KHÔNG: ba câu trên đáp án đều là
"câu CÓ trong bài", nên câu cuối mà cũng "có" nốt thì bé qua được bằng cách bấm bừa
một dáng.

Cả bốn đều KHÔNG đòi bé dịch, vì cả quyển chưa dạy dịch câu bao giờ.

── CHỮ LẠ ──
`_kho_tu()` dựng túi từ ĐÃ HỌC TỚI CHƯƠNG ẤY. Câu nào có chữ ngoài túi thì bị loại
ngay tại đây, và `test/tienganh_dochieu.test.mjs` hỏi lại lần nữa trên tệp đã ghi —
bộ sinh tự kiểm lấy mình thì chẳng chứng minh được gì.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}

SO_DONG_TOI_DA = 6      # bác chốt: đoạn 4–6 câu
SO_DONG_TOI_THIEU = 4
# Qua bài khi sai NHIỀU NHẤT MỘT CÂU. Không đòi đúng hết: đây là bài đọc đầu tiên
# của cả môn, và sai một câu chi tiết rồi phải làm lại từ đầu thì bé bỏ.


def ma_am(loai: str, chu: str) -> str:
    """Cùng luật đặt mã với `tools/tts/sinh_am.py`. Lệch một ký tự là nút nghe câm."""
    sach = "".join(c if c.isalnum() else "_" for c in str(chu).lower()).strip("_")
    return f"{loai}_{sach}"[:60]


def chu_trong(s: str) -> list[str]:
    return re.findall(r"[a-z']+", str(s or "").lower())


def _kho_tu(chuans: list[dict], den_chuong: int | None, chuong_cua: dict) -> set[str]:
    """Túi từ bé ĐÃ HỌC — cùng phép dựng với `tienganh_bai.test.mjs`.

    Gồm: từ vựng (cả dạng số nhiều và -ing) · chữ trong CÔNG THỨC ngoài phần ô
    trống · và ba nhóm từ phụ (`số đếm · màu · tên`). Quyển lớp 1·2 vào trọn vẹn;
    quyển đang xét chỉ tính tới chương `den_chuong`.
    """
    kho: set[str] = set()

    def nap(s):
        kho.update(chu_trong(s))

    for i, chuan in enumerate(chuans):
        cuoi = (i == len(chuans) - 1)
        for u in chuan["unit"]:
            if cuoi and den_chuong is not None and chuong_cua.get(u["so"], 99) > den_chuong:
                continue
            for x in u["tu"]:
                for k in ("tu", "so_it", "so_nhieu", "dang_ing"):
                    nap(x.get(k))
            for m in u["mau_cau"]:
                nap(re.sub(r"\[[^\]]*\]", " ", str(m.get("cong_thuc") or "")))
                nap(m.get("vi_du"))
        for nhom in ("so_dem", "mau", "ten"):
            for m in ((chuan.get("them") or {}).get(nhom) or {}).get("muc") or []:
                nap(m if isinstance(m, str) else m.get("word"))
    return kho


def _tach_doi(c: str) -> list[str]:
    """`"How are you? - Fine, thank you."` → hai dòng. Cặp hỏi–đáp là HAI lượt nói.

    Vế đáp còn có thể là cặp phương án `"Yes, I do. / No, I don't."` — đoạn đọc thì
    phải chọn MỘT, vì không ai vừa đồng ý vừa từ chối trong một câu. Lấy vế đầu,
    cùng luật với `cau_noi_duoc()` của bộ dựng video.
    """
    ds = [x.strip() for x in str(c or "").split(" - ") if x.strip()]
    return [x.split(" / ")[0].strip() for x in ds]


TEN_RIENG = re.compile(r"\b(Ben|Lucy|Mai|Minh|Bill|Linh|Mary|Nam|Ms Hoa|Mr Long)\b")


def _doan(bais: list[dict], kho: set[str]) -> list[str]:
    """Đoạn đọc: mỗi bài trong chương góp một mẩu, theo đúng thứ tự học.

    Góp lần lượt chứ không lấy hết của bài đầu: đoạn phải đi qua cả bốn unit thì
    câu hỏi Ý CHÍNH mới có nghĩa là ý chính của CHƯƠNG.

    Trong một bài thì ưu tiên câu có TÊN ĐÃ XUẤT HIỆN ở dòng trên. Cùng một vốn
    câu, cùng một luật, nhưng đoạn đọc ra hẳn khác:

        Hello. I'm Ben.        Hello. I'm Ben.
        What's your name?      What's your name?
        My name's Mary.        My name's Ben.      ← cùng một bạn, đọc thành chuyện
    """
    dong: list[str] = []
    ten_da_dung: list[str] = []

    def diem(c: str) -> tuple:
        """Câu nào nên lấy trước: có tên đã dùng > có tên mới > không tên."""
        tens = TEN_RIENG.findall(c)
        return (0 if any(t in ten_da_dung for t in tens) else (1 if tens else 2),)

    for vong in range(4):
        them = False
        for b in bais:
            if len(dong) >= SO_DONG_TOI_DA:
                break
            ds = [c for c in (b["knowledgeCore"].get("canonicalExamples") or [])
                  if all(w in kho for w in chu_trong(c))]
            # Vòng 0 chọn theo tên; vòng sau lấy tiếp câu chưa dùng, giữ thứ tự sách.
            ds = sorted(ds, key=diem) if vong == 0 else ds
            con = [c for c in ds if not set(_tach_doi(c)) & set(dong)]
            if not con:
                continue
            # Lấy TRỌN cặp hỏi–đáp hoặc không lấy. Cắt giữa cặp thì đoạn văn kết
            # thúc bằng một câu hỏi bỏ lửng — "What can you see?" rồi hết bài, và
            # bé ngồi tìm câu trả lời không có ở đâu cả.
            mau = _tach_doi(con[0])
            if len(dong) + len(mau) > SO_DONG_TOI_DA:
                continue
            them = True
            for x in mau:
                if x not in dong:
                    dong.append(x)
                    ten_da_dung += TEN_RIENG.findall(x)
        if not them or len(dong) >= SO_DONG_TOI_DA:
            break
    return dong


def _cung_khuon(bais: list[dict], cau: str, tru: set[str]) -> list[str]:
    """Câu CÙNG KHUÔN với `cau` mà KHÔNG nằm trong đoạn — dùng làm mồi nhử.

    Cùng khuôn = cùng CHỮ ĐẦU và cùng SỐ CHỮ. Thô, nhưng đúng việc: mọi câu của
    một mẫu đều sinh ra từ một công thức, nên chúng chỉ khác nhau ở chỗ điền vào ô
    trống — tức là khác nhau ĐÚNG CHI TIẾT mà câu hỏi đang hỏi. Mồi khác khuôn thì
    bé loại được bằng hình dạng câu, không cần đọc đoạn văn lấy một chữ.

    ⚠ So bằng BA CHỮ ĐẦU thì hỏng: chỗ điền của quá nửa mẫu câu lớp 3 nằm ở vế
    ĐÁP (`It's five.` ↔ `It's one.`), mà hai câu ấy chỉ chung đúng một chữ đầu.
    """
    khoa = (cau.split()[0].lower(), len(cau.split()))
    ra = []
    for b in bais:
        for c in b["knowledgeCore"].get("canonicalExamples") or []:
            for x in _tach_doi(c):
                if x in tru or x in ra:
                    continue
                if (x.split()[0].lower(), len(x.split())) == khoa:
                    ra.append(x)
    return ra


def _cau_hoi(ky: dict, doan: list[str], bais: list[dict], ten_chuong: dict) -> list[dict]:
    ra: list[dict] = []

    # ── Q1 · Ý CHÍNH ──
    khac = [t for s, t in sorted(ten_chuong.items()) if s != ky["chapter"]][:3]
    ra.append({
        "id": "D1", "loai": "yChinh",
        "text": "Bài đọc này nói về chuyện gì?",
        "format": "chon",
        "choices": _tron(ten_chuong[ky["chapter"]], khac),
        "answerKey": {"choice": ten_chuong[ky["chapter"]]},
        "solutionNarrative": f"Cả đoạn nói về {ten_chuong[ky['chapter']].lower()}.",
    })

    # ── Q2·Q3 · CHI TIẾT · câu nào CÓ trong bài ──
    # Mồi đã dùng ở câu trước KHÔNG được dùng lại làm mồi câu sau: bé vừa thấy nó
    # bị loại thì lần thứ hai nó không còn nhử được ai.
    trong = set(doan)
    for x in doan:
        if len(ra) >= 3:
            break
        # Hai mồi cũng dựng được câu (ba lựa chọn). Đòi đủ ba mồi thì hai chương
        # cuối mất hẳn câu chi tiết thứ hai, chỉ vì mỗi bài chỉ khai 8 câu ví dụ và
        # số ấy chia cho hai mẫu câu.
        moi = _cung_khuon(bais, x, trong)
        if len(moi) < 2:
            continue
        ra.append({
            "id": f"D{len(ra) + 1}", "loai": "chiTiet",
            "text": "Câu nào CÓ trong bài đọc?",
            "format": "chon",
            "choices": _tron(x, moi[:3]),
            # ⚠ KHÔNG có nút nghe ở câu này. `am` của câu hỏi là clip của ĐÁP ÁN —
            # bé bấm nghe là được đọc thẳng câu đúng cho, và câu hỏi "đọc lại đoạn
            # để tìm" thành câu hỏi "nghe rồi bấm". Đúng cái màn này sinh ra để dạy
            # thì bị chính nút nghe ấy làm hỏng. Sáu dòng của đoạn văn ở trên vẫn có
            # nút nghe riêng — chỗ ấy nghe là để ĐỌC được, không phải để lấy đáp án.
            "answerKey": {"choice": x},
            "solutionNarrative": f"“{x}” — con đọc lại đoạn trên xem nhé.",
        })
        trong = trong | set(moi[:3])

    # ── Q4 · CHI TIẾT · đúng/sai ──
    # Đáp án SAI, cố ý: ba câu trên đáp án đều là "câu có trong bài", nên câu cuối
    # mà cũng đúng nốt thì bé qua được bằng cách bấm bừa một dáng.
    ngoai = next((c for x in doan
                  for c in _cung_khuon(bais, x, set(doan)) if c not in doan), None)
    if ngoai:
        # Hỏi bằng HAI LỰA CHỌN chứ không dùng `format: "tf"`. Bộ chơi `tf` của môn
        # này là `CauNgheNhin` — nghe một từ, NHÌN MỘT HÌNH, hình ấy có đúng không —
        # nó luôn vẽ một ô hình và luôn hỏi "Hình này có đúng không?". Đưa câu chữ
        # vào đó thì bé thấy một dấu ❔ to tướng và một câu hỏi không ăn nhập.
        # Còn `CauHoi` không có `choices` thì rơi vào Ô GÕ CHỮ. Nên: hai lựa chọn.
        ra.append({
            "id": f"D{len(ra) + 1}", "loai": "chiTiet",
            "text": f"Câu “{ngoai}” có trong bài đọc không?",
            "format": "chon",
            "choices": ["Có", "Không"],
            "am": ma_am("cau", ngoai), "amChu": ngoai,
            "answerKey": {"choice": "Không"},
            "solutionNarrative": f"KHÔNG — đoạn trên không có câu “{ngoai}”.",
        })
    return ra


def _tron(dung: str, moi: list[str]) -> list[str]:
    """Xếp đáp án vào giữa đám mồi. KHÔNG random — chạy hai lần phải ra một tệp."""
    ds = list(moi)
    ds.insert(min(len(ds), (len(dung) + len(ds)) % (len(ds) + 1)), dung)
    return ds


def dung(lop: int) -> tuple[list[dict], list[dict]]:
    """Trả (danh mục bài đọc, danh sách lời cần có clip)."""
    tm = GOC / f"web/public/content/{QUYEN[lop]}"
    bais = [json.loads(p.read_text("utf8"))
            for p in sorted(tm.glob(f"DL_{QUYEN[lop].upper()}_B*.json"))]
    chuans = [json.loads((GOC / f"data/tienganh/chuan_lop{i}.json").read_text("utf8"))
              for i in range(1, lop + 1)]

    theo_chuong: dict[int, list[dict]] = {}
    for b in bais:
        theo_chuong.setdefault(b["chuong"], []).append(b)
    ten_chuong = {c: v[0]["tenChuong"] for c, v in theo_chuong.items()}
    # unit số → chương, để cắt túi từ đúng chỗ
    chuong_cua = {b["so"]: b["chuong"] for b in bais}

    ra, loi = [], {}
    for c, ds in sorted(theo_chuong.items()):
        kho = _kho_tu(chuans, c, chuong_cua)
        doan = _doan(ds, kho)
        if len(doan) < SO_DONG_TOI_THIEU:
            print(f"  ⚠ chương {c}: chỉ dựng được {len(doan)} dòng, bỏ qua")
            continue
        ky = {"id": f"DOC:TA{lop}.C{c}", "chapter": c, "loai": "dochieu",
              "name": f"ĐỌC HIỂU {c} · {ten_chuong[c].upper()}",
              "doan": [{"cau": x, "am": ma_am("cau", x)} for x in doan]}
        ky["cau"] = _cau_hoi(ky, doan, ds, ten_chuong)
        ky["soCau"] = len(ky["cau"])
        ky["need"] = max(2, len(ky["cau"]) - 1)
        ra.append(ky)
        for x in doan:
            loi[ma_am("cau", x)] = {"id": ma_am("cau", x), "chu": x, "tieng": "en"}
        for q in ky["cau"]:
            # `amChu` khai THẲNG câu mà clip đọc lên. Suy ngược từ `answerKey` là
            # chỗ vừa sai: câu Có/Không có đáp án là chữ "Không", và bộ sinh âm ngoan
            # ngoãn đem chữ Việt ấy đi đọc bằng giọng Anh.
            if q.get("am") and q.get("amChu"):
                loi[q["am"]] = {"id": q["am"], "chu": q["amChu"], "tieng": "en"}
    return ra, list(loi.values())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3, choices=[1, 2, 3])
    p.add_argument("--thieu", help="ghi ra tệp những dòng chưa có clip")
    a = p.parse_args()

    ds, loi = dung(a.lop)
    ra = GOC / f"web/public/content/{QUYEN[a.lop]}/dochieu.json"
    ra.write_text(json.dumps(ds, ensure_ascii=False, indent=1), "utf8")
    for k in ds:
        print(f"  chương {k['chapter']}: {len(k['doan'])} dòng · {len(k['cau'])} câu hỏi "
              f"· cần {k['need']}/{k['soCau']}")
    print(f"→ {ra}")

    if a.thieu:
        so = json.loads((GOC / f"web/public/content/tienganh/lop{a.lop}_am.json")
                        .read_text("utf8"))
        co = {c["id"] for c in so.get("clip", [])}
        con = [m for m in loi if m["id"] not in co]
        Path(a.thieu).write_text(json.dumps(con, ensure_ascii=False, indent=1), "utf8")
        print(f"{len(con)}/{len(loi)} dòng chưa có clip → {a.thieu}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
