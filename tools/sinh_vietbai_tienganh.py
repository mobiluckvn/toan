#!/usr/bin/env python3
"""DỰNG ĐỀ BÀI VIẾT NGẮN — mỗi chương một đề, chấm bằng AI.

    python3 tools/sinh_vietbai_tienganh.py --lop 3

Bác chốt 18-08-2026, bốn điều:
  1. sửa lỗi và khen CỤ THỂ — chỉ ra câu sai ở đâu, sửa lại cho đúng;
  2. có ĐIỂM để vào sổ, và phải nói rõ là AI chấm;
  3. chỉ gợi ý bằng VỐN TỪ ĐÃ HỌC, không dạy từ mới;
  4. bố mẹ đọc được bài viết và lời chấm.

Tệp này lo phần ĐỀ. Ba điều còn lại nằm ở `web/functions/src/chamviet.js` (lời dặn
cho mô hình), `web/src/mon/tienganh/lib/chamviet.js` (bóc và SOI lời chấm) và
`components/VietBai.jsx` (màn hình).

── ĐỀ GỒM NHỮNG GÌ, VÀ VÌ SAO ──

Bé lớp 3 chưa viết được tiếng Anh từ chỗ trống. Nên đề KHÔNG chỉ là một câu hỏi:
nó mang theo cả chỗ dựa.

    de       việc phải làm, bằng TIẾNG VIỆT — bé đọc được tiếng Việt
    mauCau   những mẫu câu của chương, để bé ghép theo
    vonTu    vốn từ đã học TỚI CHƯƠNG NÀY, hiện thành bảng từ bấm được
    toiThieu số câu tối thiểu

`vonTu` còn là thứ ĐEM ĐI CHẤM: máy chấm được dặn chỉ gợi ý bằng đúng bảng ấy, và
`lib/chamviet.js` soi lại lời chấm để bắt chữ lạ. Dặn dò là thứ mô hình *có thể*
theo; soi lại là thứ nó không cần theo. Cả môn này đã học bài ấy hai lần rồi.

── VÌ SAO ĐỀ KHÔNG PHẢI TIẾNG ANH ──
Đề bằng tiếng Anh thì bé phải đọc hiểu đề trước đã, và bài kiểm tra viết hoá ra
kiểm tra đọc. Đề tiếng Việt, viết tiếng Anh — đúng một việc một lúc.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
QUYEN = {1: "ta1", 2: "ta2", 3: "ta3"}

# Bé lớp 3 viết 2–3 câu là một bài. Đòi nhiều hơn thì bé chép lại mẫu cho xong.
CAU_TOI_THIEU = 2

# Đề của từng chương — soạn TAY, vì "viết về cái gì" là việc của người.
# Khoá là số chương; thiếu chương nào thì bộ sinh nói ra chứ không bịa một đề chung.
DE = {
    1: ("Con viết 2–3 câu tự giới thiệu nhé: chào, tên con là gì, "
        "rồi chào tạm biệt."),
    2: ("Con viết 2–3 câu về cơ thể và sở thích của con: con thích làm gì, "
        "và chỉ một bộ phận trên mặt."),
    3: ("Con viết 2–3 câu về đồ dùng học tập của con: con có gì, màu gì."),
    4: ("Con viết 2–3 câu về nhà con: trong phòng có gì, và một người trong nhà "
        "làm nghề gì."),
    5: ("Con viết 2–3 câu về con vật hoặc đồ chơi con thích, và con đang làm gì."),
}


# Nhiều nhất bao nhiêu cụm trong một nhóm gợi ý. Sách có unit khai 12 ví dụ cùng
# khuôn; bày hết ra thì bảng gợi ý dài hơn cả bài bé phải viết.
CUM_TOI_DA = 6


def _tach_doi(s: str) -> tuple[str | None, str]:
    """`"What's your hobby? - It's cooking."` → `("What's your hobby?", "It's cooking.")`.

    Cắt ở `" - "` đúng như `cauSachCuaBai` (phongnoi.js) và `sinh_kichban_noi.py`.
    Không phải cặp thì trả `(None, cả câu)`.
    """
    phan = [x.strip() for x in str(s or "").split(" - ")]
    if len(phan) == 2 and all(phan):
        return phan[0], phan[1]
    return None, str(s or "").strip()


def _khop_khung(cong_thuc: str, cau: str) -> bool:
    """Câu này có phải một cách điền của công thức kia không."""
    if not cong_thuc:
        return False
    khung = re.sub(r"\s*\+\s*", " ", cong_thuc)
    mau = re.escape(khung).replace(r"\[", "[").replace(r"\]", "]")
    mau = re.sub(r"\[[^\]]+\]", "(.+?)", mau)
    return re.fullmatch(mau, str(cau or "").strip()) is not None


def _sach_se(cau: str) -> bool:
    """Câu có sạch để đưa cho bé chép không.

    Bản đồ lớp 2 khai `"Yes,[Pronoun] is."` — thiếu dấu cách sau dấu phẩy. Đưa cho
    bé chép là dạy bé viết sai. Bỏ qua chứ không tự chèn dấu cách: sửa hộ ở đây thì
    câu trong bài viết khác câu trên màn bài học, mà chỗ sai thật vẫn nằm nguyên
    trong bản đồ.
    """
    return bool(cau) and not re.search(r"[,;](?=\S)", cau) and "/" not in cau


# Mục không phải MỘT TỪ bé gõ được thì đừng bày ra bảng bấm. Sách khai
# `"the alphabet (A–Z)"` như một "từ vựng"; bấm vào nó thì bài của bé có một chuỗi
# không ai viết bao giờ. Lọc ở đây chứ không ở màn hình: màn hình chỉ nên bày thứ
# nó nhận được.
def _von_dung_duoc(von: list[dict]) -> list[dict]:
    return [v for v in von if not re.search(r"[()–]", v["tu"])]


def _bo_ten(cau: str, tens: list[str]) -> str:
    """Thay TÊN NGƯỜI trong câu gợi ý bằng một chỗ trống.

    ⚠ Bản đầu bày thẳng câu của sách: "Hello. I'm Ben." Bé tên Mai bấm vào đó thì
    bài của bé viết "I'm Ben" — sai về chính bé, và cô giáo máy chấm đúng ngữ pháp
    nên không ai bắt được. Bốn ví dụ của unit 1 chỉ khác nhau ở cái tên, nên bày cả
    bốn cũng chỉ là bày bốn cái tên người khác.

    Thay tên bằng `___` thì cụm thành đúng cái nó vốn là: một KHUÔN để bé điền tên
    MÌNH vào. Không bịa chữ nào — chỉ bỏ đi một chữ vốn không dành cho bé.
    """
    ra = cau
    for t in sorted(tens, key=len, reverse=True):
        ra = re.sub(rf"\b{re.escape(t)}\b", "___", ra)
    return re.sub(r"___(\s+___)+", "___", ra)


MO_DAU = re.compile(r"^(Hello|Hi)\b|^(I'm|My name's)\b", re.I)
KET_BAI = re.compile(r"^(Bye|Goodbye)\b", re.I)


def _goi_y(bais: list[dict], truoc: list[dict] = (),
             tens: list[str] = ()) -> list[dict]:
    """GỢI Ý THEO NHÓM — mỗi nhóm là một CHỖ trong đoạn văn bé sắp viết.

    ══ VÌ SAO ĐỔI ══ (bác chốt 18-08-2026)

    Bác thử xong bảo: "phần gợi ý nên bổ sung thêm nhiều từ hơn cho con chọn và ghi
    là gợi ý. Con có thể typing thêm theo ý của con. Lưu ý là các từ gợi ý ấy phải
    ghép lại thành được đoạn văn có ý nghĩa chứ như giờ bạn cho linh tinh."

    Bản cũ bày đúng MỘT bảng: toàn bộ từ đã học, dồn từ chương 1 tới đây, xếp theo
    thứ tự sách. Bé lớp 3 unit 4 mở ra thấy:

        one · two · three · … · ten · the alphabet (A–Z) · hello · hi · bye ·
        goodbye · fine · how · I · you · thank you · Ben · Lucy · Mai · Minh · my ·
        name · what · your · old · …

    Năm mươi ba ô chữ rời. Bấm bừa vài cái thì ra "ten hello your old" — không phải
    câu, càng không phải đoạn. Đó đúng là chữ "linh tinh" của bác.

    ── NAY: CỤM GHÉP ĐƯỢC, XẾP THEO CHỖ TRONG ĐOẠN ──

    Mỗi mẫu câu của sách thành MỘT nhóm. Nhãn nhóm là `dungDe` — chính lời sách nói
    mẫu ấy dùng để làm gì ("Hỏi và nói sở thích"). Các mục trong nhóm là những câu
    TRỌN VẸN cùng khuôn, lấy từ `canonicalExamples`.

    Bé bấm mỗi nhóm một cái là ra một đoạn có đầu có cuối:

        Hello. I'm Mai.  ·  It's cooking.  ·  Bye.

    Chỉ lấy VẾ ĐÁP của cặp hỏi–đáp: bài viết là bé kể về mình, không phải bé tự hỏi
    tự trả lời. Vế hỏi vẫn còn ở mục "Mẫu câu con đã học" ngay trên đề bài.
    """
    nhom: list[dict] = []
    da_co: set[str] = set()
    for b in bais:
        vi_du = [str(x) for x in (b["knowledgeCore"].get("canonicalExamples") or [])]
        for m in (b["knowledgeCore"].get("mauCauDs") or []):
            _, dap = _tach_doi(m.get("cau"))
            khung = _tach_doi(m.get("congThuc") or "")[1]
            cum = [dap] + [_tach_doi(x)[1] for x in vi_du
                           if _khop_khung(khung, _tach_doi(x)[1])]
            cum = [_bo_ten(c, tens) for c in cum]
            cum = [c for c in dict.fromkeys(cum) if c and _sach_se(c) and c not in da_co]
            if not cum:
                continue
            da_co.update(cum[:CUM_TOI_DA])
            nhan = str(m.get("dungDe") or "").strip().rstrip(".") or "Câu con có thể viết"
            nhom.append({"nhan": nhan, "cum": cum[:CUM_TOI_DA]})

    # ── ĐOẠN VĂN PHẢI CÓ ĐẦU VÀ CÓ CUỐI ──
    # Unit 5 chỉ dạy về sở thích, nên nhóm của chính nó toàn "It's cooking." Bé bấm
    # ba cái là ra ba câu sở thích liền nhau — đúng khuôn, nhưng không phải một
    # đoạn. Lời chào và lời tự giới thiệu thì bé HỌC RỒI ở mấy unit đầu; mượn lại
    # là đoạn có chỗ mở và chỗ đóng. Không mượn của unit CHƯA học: `truoc` chỉ gồm
    # những bài đứng trước bài này.
    mo, ket = [], []
    for b in list(truoc) + list(bais):
        for x in (b["knowledgeCore"].get("canonicalExamples") or []):
            for nua in (str(x).split(" - ") if " - " in str(x) else [str(x)]):
                nua = _bo_ten(nua.strip(), tens)
                if not _sach_se(nua) or nua in da_co:
                    continue
                if MO_DAU.match(nua) and len(mo) < CUM_TOI_DA:
                    mo.append(nua); da_co.add(nua)
                elif KET_BAI.match(nua) and len(ket) < CUM_TOI_DA:
                    ket.append(nua); da_co.add(nua)
    ra = []
    if mo:
        ra.append({"nhan": "Mở đầu — chào và nói con là ai", "cum": mo})
    ra += nhom
    if ket:
        ra.append({"nhan": "Chào tạm biệt", "cum": ket})
    return ra


def _ten_unit(b: dict) -> str:
    """`"Unit 5 · Sở thích của mình · My hobbies"` → `"Sở thích của mình"`."""
    phan = [x.strip() for x in str(b.get("title") or "").split("·")]
    return phan[1] if len(phan) > 2 else (phan[-1] if phan else "?")


def chu_trong(s: str) -> list[str]:
    return re.findall(r"[a-z']+", str(s or "").lower())


def dung(lop: int) -> list[dict]:
    tm = GOC / f"web/public/content/{QUYEN[lop]}"
    bais = [json.loads(p.read_text("utf8"))
            for p in sorted(tm.glob(f"DL_{QUYEN[lop].upper()}_B*.json"))]
    # Năng lực lấy từ BẢN CHUẨN, nơi nó còn là DANH SÁCH. `objective.text` của bài
    # đã nối chúng lại thành một chuỗi không dấu phân cách ("Đọc số từ một đến mười
    # Nhận mặt bảng chữ cái"), đem làm đề thì đọc không ra câu.
    chuan = json.loads((GOC / f"data/tienganh/chuan_lop{lop}.json").read_text("utf8"))
    nang_luc = {u["so"]: [x for x in (u.get("nang_luc") or []) if x] for u in chuan["unit"]}

    # Tên người SÁCH dạy — để bỏ khỏi câu gợi ý. KHÔNG gõ tay một danh sách: gõ tay
    # thì thêm quyển mới là lệch, mà lệch ở đây nghĩa là bé chép nguyên tên bạn khác
    # vào bài tự giới thiệu của mình.
    #
    # ⚠ HAI NƠI, VÌ BA QUYỂN KHAI HAI KIỂU. Lớp 1 gom tên vào `them.ten`; lớp 3 để
    # tên ngay trong `vocabulary` của từng bài và `them` thì RỖNG. Chỉ đọc `them.ten`
    # thì lớp 3 ra danh sách rỗng, `_bo_ten` không bỏ được gì, và bảng gợi ý lại bày
    # "Hello. I'm Ben." như cũ — im lặng, vì rỗng không phải là lỗi.
    #
    # Dấu nhận biết tên riêng trong bài: `ipa` là null và chữ đầu viết hoa — đúng
    # luật `chuan_tienganh.py` đang dùng, chứ không phải một phép đoán mới.
    tens = [x if isinstance(x, str) else x.get("word")
            for x in (((chuan.get("them") or {}).get("ten") or {}).get("muc") or [])]
    tens += [v["tu"] for b in bais for v in b["knowledgeCore"]["vocabulary"]
             if not v.get("ipa") and v["tu"][:1].isupper()]
    tens = [x for x in dict.fromkeys(tens) if x]

    theo_chuong: dict[int, list[dict]] = {}
    for b in bais:
        theo_chuong.setdefault(b["chuong"], []).append(b)

    ra = []
    von: list[dict] = []          # dồn dần: chương sau có cả vốn của chương trước
    da_co: set[str] = set()

    # ══ MỖI UNIT MỘT ĐỀ ══
    #
    # Bác chốt 18-08: đề theo chương là chỗ viết TỔNG HỢP cả bốn unit, nhưng bé học
    # xong MỘT unit thì cần viết ngay của unit ấy. Đề suy thẳng từ `objective.text`
    # của bài — đó chính là NĂNG LỰC sách khai cho unit ("Nói mình thích làm gì"),
    # nên không phải soạn tay 21 đề và cũng không lệch khỏi sách.
    for b in bais:
        for v in b["knowledgeCore"]["vocabulary"]:
            if v["tu"] not in da_co:
                da_co.add(v["tu"])
                von.append({"tu": v["tu"], "nghia": v["nghia"]})
        nl = [x.strip().rstrip(".") for x in nang_luc.get(b["so"], [])]
        # Nối bằng dấu chấm phẩy, KHÔNG bằng "và": nhiều năng lực tự nó đã có chữ
        # "và" bên trong ("Chào và tạm biệt"), nối thêm nữa thành "và … và …".
        viec = "; ".join(x[0].lower() + x[1:] for x in nl)
        mau = [m["cau"] for m in (b["knowledgeCore"].get("mauCauDs") or [])]
        if not viec or not mau:
            print(f"  ⚠ unit {b['so']}: thiếu năng lực hoặc mẫu câu, bỏ qua")
            continue
        ra.append({
            "id": f"VIET:TA{lop}.U{b['so']:02d}",
            "unit": b["so"], "chapter": b["chuong"], "phamVi": "unit",
            "loai": "vietbai",
            "name": f"BÀI VIẾT · UNIT {b['so']} · {_ten_unit(b).upper()}",
            "de": f"Con viết {CAU_TOI_THIEU}–3 câu: {viec[0].lower()}{viec[1:]}.",
            "toiThieu": CAU_TOI_THIEU,
            "mauCau": list(dict.fromkeys(mau)),
            "goiY": _goi_y([b], bais[:bais.index(b)], tens),
            "vonTu": _von_dung_duoc(von),
        })

    # ══ MỖI CHƯƠNG MỘT ĐỀ — viết tổng hợp cả bốn unit ══
    von, da_co = [], set()
    for c, ds in sorted(theo_chuong.items()):
        for b in ds:
            for v in b["knowledgeCore"]["vocabulary"]:
                if v["tu"] not in da_co:
                    da_co.add(v["tu"])
                    von.append({"tu": v["tu"], "nghia": v["nghia"]})
        if c not in DE:
            print(f"  ⚠ chương {c}: chưa soạn đề, bỏ qua")
            continue
        mau = [m["cau"] for b in ds for m in (b["knowledgeCore"].get("mauCauDs") or [])]
        ra.append({
            "id": f"VIET:TA{lop}.C{c}",
            "chapter": c, "phamVi": "chuong",
            "loai": "vietbai",
            "name": f"BÀI VIẾT CHƯƠNG {c} · {ds[0]['tenChuong'].upper()}",
            "de": DE[c],
            "toiThieu": CAU_TOI_THIEU,
            # Mẫu câu của CHÍNH chương này — bé ghép theo, không phải nhớ suông.
            "mauCau": list(dict.fromkeys(mau)),
            # Gợi ý gom của CẢ BỐN unit — bài chương là chỗ viết tổng hợp, nên
            # nhóm nào cũng phải có mặt để bé ghép thành một đoạn dài hơn.
            "goiY": _goi_y(ds, bais[:bais.index(ds[0])], tens),
            # Vốn từ DỒN từ chương 1 tới đây: bé viết về mình thì vẫn cần "I'm" của
            # chương 1 ở bài chương 4. Cắt theo đúng chương là cắt mất cả câu chào.
            "vonTu": _von_dung_duoc(von),
        })
    return ra


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lop", type=int, default=3, choices=[1, 2, 3])
    a = p.parse_args()
    ds = dung(a.lop)
    ra = GOC / f"web/public/content/{QUYEN[a.lop]}/vietbai.json"
    ra.write_text(json.dumps(ds, ensure_ascii=False, indent=1), "utf8")
    for k in ds:
        cho = f"unit {k['unit']}" if k.get("phamVi") == "unit" else f"chương {k['chapter']}"
        print(f"  {cho:10s}: {len(k['vonTu'])} từ · {len(k['mauCau'])} mẫu câu")
    print(f"→ {ra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
