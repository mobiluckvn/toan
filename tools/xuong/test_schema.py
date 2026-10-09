"""CỔNG · XƯỞNG SINH NỘI DUNG (việc V12). Chạy KHÔNG cần mạng, không cần khoá.

    python tools/xuong/test_schema.py

── CÁI DỄ HỎNG, VÀ VÌ SAO CẦN CỔNG ──
Xưởng là chỗ duy nhất trong kho mà một mô hình soạn ra thứ có thể đi vào NỘI DUNG
THẬT. Câu sai ở phòng nói thì bé nghe một lần rồi thôi; câu sai lọt vào
`public/content/` thì mọi bé học nó, mọi lần, cho tới khi có người mở ra đọc.

Nên bốn chốt dưới đây không phải phép kiểm lịch sự:

  A · KHUÔN soi đúng hình dạng BỘ SINH ĐANG ĐỌC — soi lại bằng DỮ LIỆU THẬT của lớp
      4, chứ không bằng fixture tôi tự gõ. Khuôn lệch khỏi hình dạng thật thì bản
      nháp "qua khuôn" vẫn không rót được vào đâu.
  B · HÀNG RÀO phải dùng lại phép soi THẬT (`sinh_kichban_noi`), không phải bản sao
      thứ ba. Và nó phải tách đúng ba loại tiếng Anh (câu · chữ lẻ · công thức) —
      chỗ này đã hỏng thật, bác sạch cả ba mẫu câu vì ô trống `[Noun]`.
  C · ĐƯỜNG RA chỉ được nằm trong `data/tienganh/xuong`, kể cả khi người gọi đưa
      `../../../web/public/content`.
  D · KHÔNG TỆP NÀO TRONG `web/` NHẬP XƯỞNG. "Không ai gọi" là thứ thay đổi lặng lẽ,
      nên phải có chốt — cùng lẽ với cổng `cong-xanh-ma-khong-ai-goi`.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC = HERE.parent.parent
sys.path.insert(0, str(HERE))

import chung  # noqa: E402
import giam_khao  # noqa: E402
import hang_rao  # noqa: E402
import khuon  # noqa: E402
import nen_worker  # noqa: E402
import tranh_luan  # noqa: E402
import worker_doc_hieu  # noqa: E402
import worker_kich_ban  # noqa: E402
import worker_mau_cau  # noqa: E402
import worker_tu_moi  # noqa: E402

pass_ = 0
fail = 0


def t(ten: str, dieu) -> None:
    global pass_, fail
    if dieu:
        pass_ += 1
    else:
        fail += 1
        print("  ✗", ten)


# ══════════════════ A · KHUÔN, SOI BẰNG DỮ LIỆU THẬT ══════════════════

print("\n── A · KHUÔN ──\n")

chuan = json.loads((GOC / "data/tienganh/chuan_lop4.json").read_text("utf8"))
u_that = next(u for u in chuan["unit"] if u.get("so") == 1)

# ⚠ SOI BẰNG MỤC THẬT CỦA SÁCH. Nếu khuôn của tôi chặt hơn hình dạng thật thì mọi
# bản nháp đều bị bác, và không ai hiểu vì sao — cổng này bắt đúng chuyện đó.
k_tu = khuon.soi_khuon("tu", u_that["tu"])
t(f"mọi mục `tu` thật của lớp 4 unit 1 qua khuôn ({len(k_tu['qua'])}/{len(u_that['tu'])})",
  not k_tu["bac"])
k_mau = khuon.soi_khuon("mau_cau", u_that["mau_cau"])
t(f"mọi `mau_cau` thật qua khuôn ({len(k_mau['qua'])}/{len(u_that['mau_cau'])})",
  not k_mau["bac"])

# Đảo chiều: mục thiếu trường PHẢI bị bác, nếu không thì hai dòng trên xanh vô nghĩa.
t("từ thiếu `nghia` → bác", bool(khuon.soi_khuon("tu", [{"tu": "dog", "vai": ["dt"]}])["bac"]))
t("từ thiếu `vai` → bác", bool(khuon.soi_khuon("tu", [{"tu": "dog", "nghia": "con chó"}])["bac"]))
t("từ có chữ số trong nghĩa → bác",
  bool(khuon.soi_khuon("tu", [{"tu": "two", "nghia": "số 2", "vai": ["so"]}])["bac"]))
t("từ có ký tự lạ → bác",
  bool(khuon.soi_khuon("tu", [{"tu": "d*g", "nghia": "con chó", "vai": ["dt"]}])["bac"]))
t("mẫu câu dùng ngoặc TRÒN cho ô trống → bác",
  bool(khuon.soi_khuon("mau_cau", [{"vi_du": "I like fish.",
                                    "cong_thuc": "I like (Noun).",
                                    "dung_de": "nói sở thích"}])["bac"]))
t("mẫu câu dùng ngoặc VUÔNG → qua",
  not khuon.soi_khuon("mau_cau", [{"vi_du": "I like fish.",
                                   "cong_thuc": "I like [Noun].",
                                   "dung_de": "nói sở thích"}])["bac"])

# Đọc hiểu: đúng MỘT đáp án, và đáp án phải nằm trong phương án.
dh_tot = {"doan": [{"cau": "I like fish."}],
          "cau": [{"hoi": "Bé thích gì?", "chon": ["fish", "milk", "bread"], "dung": "fish"}]}
t("bài đọc đúng khuôn → qua", not khuon.soi_khuon("doc_hieu", [dh_tot])["bac"])
t("đáp án không nằm trong phương án → bác",
  bool(khuon.soi_khuon("doc_hieu", [{**dh_tot, "cau": [
      {"hoi": "x", "chon": ["milk", "bread"], "dung": "fish"}]}])["bac"]))
# ⚠ Chỗ hỏng đã bắt được thật 47 câu ở hai đợt bài đọc.
t("đáp án xuất hiện HAI lần trong phương án → bác",
  bool(khuon.soi_khuon("doc_hieu", [{**dh_tot, "cau": [
      {"hoi": "x", "chon": ["fish", "fish", "milk"], "dung": "fish"}]}])["bac"]))
t("chỉ một phương án → bác",
  bool(khuon.soi_khuon("doc_hieu", [{**dh_tot, "cau": [
      {"hoi": "x", "chon": ["fish"], "dung": "fish"}]}])["bac"]))
t("đoạn rỗng → bác",
  bool(khuon.soi_khuon("doc_hieu", [{**dh_tot, "doan": []}])["bac"]))
t("kịch bản không có bước → bác",
  bool(khuon.soi_khuon("kich_ban", [{"ten": "x", "muc_tieu": "y",
                                     "tinh_huong": "z", "buoc": []}])["bac"]))

# ── TRẦN SỐ MỤC ──
# ⚠ `kich_ban` và `doc_hieu` XIN ĐÚNG MỘT MỤC. Trần rộng ở đó đã che một chỗ hỏng
# thật: mô hình đọc `muc` thành danh sách BƯỚC rồi trả về SÁU kịch bản một-bước, và
# trần 12 nhận hết sáu cái ấy như sáu mục hợp lệ.
t("trần kịch bản ≤ 2", khuon.TRAN["kich_ban"] <= 2)
t("trần đọc hiểu ≤ 2", khuon.TRAN["doc_hieu"] <= 2)
t("trả quá trần → bác phần thừa VÀ nói ra",
  any("quá trần" in " ".join(x["ly_do"])
      for x in khuon.soi_khuon("tu", [{"tu": f"w{i}", "nghia": "x", "vai": ["dt"]}
                                      for i in range(khuon.TRAN["tu"] + 3)])["bac"]))

# ── HAI DANH SÁCH TÊN LOẠI PHẢI KHỚP ──
# ⚠ Đã hỏng thật: `chung.TOKEN` viết `"tu_moi"` mà `khuon.LOAI` dùng `"tu"`, nên lượt
# gọi đầu tiên vỡ với `KeyError: 'tu'`. Hai danh sách tên nằm hai tệp thì sớm muộn lệch.
t("mọi loại của khuôn đều có trần token", all(l in chung.TOKEN for l in khuon.LOAI))
t("mọi worker khai đúng một loại của khuôn",
  {m.LOAI for m in (worker_tu_moi, worker_mau_cau, worker_kich_ban, worker_doc_hieu)}
  == set(khuon.LOAI))
t("khuôn khai đủ trần số mục cho mọi loại", all(l in khuon.TRAN for l in khuon.LOAI))


# ══════════════════ B · HÀNG RÀO ══════════════════

print("── B · HÀNG RÀO VỐN TỪ ──\n")

# ⚠ PHẢI LÀ CHÍNH HÀM CỦA `sinh_kichban_noi`, không phải bản sao. Chép thành bản thứ
# ba là tự nhận thêm một chỗ lệch mà không đổi lấy gì — cả hai đều là Python, cùng
# thư mục `tools/`, nên không có lý do `chula_hai_ban` nào ở đây.
sys.path.insert(0, str(GOC / "tools"))
import sinh_kichban_noi as kb_that  # noqa: E402

t("`chu_trong` là CHÍNH hàm của sinh_kichban_noi", hang_rao.chu_trong is kb_that.chu_trong)
t("`cau_lanh_lan` là CHÍNH hàm của sinh_kichban_noi",
  hang_rao.cau_lanh_lan is kb_that.cau_lanh_lan)

bai_that = json.loads(
    (GOC / "web/public/content/ta4/DL_TA4_B01.json").read_text("utf8"))
tui = hang_rao.tui_chu(bai_that, 4)
t(f"túi chữ của bài thật không rỗng ({len(tui)} chữ)", len(tui) > 5)

# ⚠ ĐẶT RỒI TRẢ LẠI `_kb.LOP`. Xưởng chạy nhiều lớp trong một tiến trình; một biến
# module để lại giá trị của lần trước là đúng cái bẫy "sổ cũ còn trên máy".
lop_truoc = kb_that.LOP
hang_rao.tui_chu(bai_that, 5)
t("`tui_chu` trả lại biến LOP của module sau khi dùng", kb_that.LOP == lop_truoc)

cau_sach = next(iter(bai_that["knowledgeCore"]["mauCauDs"]))["cau"]
t(f"câu THẬT của sách qua hàng rào: {cau_sach!r}", not hang_rao.soi_cau(cau_sach, tui))
t("câu có chữ ngoài vốn → bác",
  any("ngoài vốn" in x for x in hang_rao.soi_cau("I have an elephant.", tui)))
t("câu rỗng → bác", bool(hang_rao.soi_cau("", tui)))

# ── SOI TRÙNG Ở MỨC BỘ ──
# Chỗ hỏng đã bắt được thật ở V9: bốn câu phụ đạo y hệt nhau, từng câu đều hợp lệ.
bo = hang_rao.soi_bo([cau_sach, cau_sach], tui)
t("hai câu y hệt nhau → câu thứ hai bị bác là TRÙNG",
  len(bo["qua"]) == 1 and any("trùng" in " ".join(x["ly_do"]) for x in bo["bac"]))

# ── BA LOẠI TIẾNG ANH, TÁCH ĐÚNG ──
# ⚠ ĐÃ HỎNG THẬT, HAI CHỖ. (1) Công thức có ô trống `[Noun]` bị bác vì "chữ ngoài
# vốn: noun" — mà một công thức KHÔNG có ô trống thì không còn là công thức.
# (2) Phương án trắc nghiệm trùng giữa hai câu hỏi bị đếm là "câu lặp" — phép soi
# trùng sinh ra để bắt BỐN CÂU HỎI giống nhau, không phải hai câu dùng chung nhiễu.
p = khuon.cau_tieng_anh("mau_cau", {"vi_du": "I like fish.", "cong_thuc": "I like [Noun]."})
t("mẫu câu: ví dụ vào `cau`, công thức vào `cong_thuc`",
  p["cau"] == ["I like fish."] and p["cong_thuc"] == ["I like [Noun]."])
t("`bo_o_trong` bỏ sạch ô trống",
  "noun" not in khuon.bo_o_trong("I play [Noun] on [Day].").lower())
p2 = khuon.cau_tieng_anh("doc_hieu", {
    "doan": [{"cau": "I like fish."}],
    "cau": [{"hoi": "a", "chon": ["fish", "milk"], "dung": "fish"},
            {"hoi": "b", "chon": ["fish", "bread"], "dung": "bread"}]})
t("đọc hiểu: câu của đoạn vào `cau`", p2["cau"] == ["I like fish."])
t("đọc hiểu: phương án vào `tu_le`, KHÔNG vào `cau`",
  "fish" in p2["tu_le"] and "fish" not in p2["cau"])
t("từ vựng: chữ lẻ KHÔNG bị soi như câu",
  khuon.cau_tieng_anh("tu", {"tu": "dog"})["cau"] == [])


# ══════════════════ C · ĐƯỜNG RA ══════════════════

print("── C · ĐƯỜNG RA ──\n")


def nem_duong_ra(p) -> bool:
    try:
        chung.soi_duong_ra(p)
        return False
    except chung.LoiXuong:
        return True


t("thư mục xưởng → cho qua", not nem_duong_ra(chung.RA_CHO_PHEP))
t("thư mục con của xưởng → cho qua", not nem_duong_ra(chung.RA_CHO_PHEP / "lop4"))
t("public/content → BÁC", nem_duong_ra("web/public/content/ta4"))
t("web/src → BÁC", nem_duong_ra("web/src/mon/tienganh"))
t("web/dist → BÁC", nem_duong_ra("web/dist"))
# ⚠ Soi bằng đường dẫn ĐÃ GIẢI. Chuỗi dưới đây trông rất hợp lệ.
t("lách bằng ../../.. → BÁC",
  nem_duong_ra("data/tienganh/xuong/../../../web/public/content"))
t("chỗ nào khác hẳn → BÁC", nem_duong_ra("data/tienganh"))
t("thư mục tạm của hệ thống → BÁC", nem_duong_ra("/tmp/xuong"))


# ══════════════════ D · KHÔNG AI TRONG web/ GỌI XƯỞNG ══════════════════

print("── D · XƯỞNG KHÔNG BAO GIỜ CHẠY LÚC BÉ HỌC ──\n")

# Ràng buộc của bản thiết kế: "Không bao giờ chạy lúc bé học." Cách duy nhất giữ
# được điều ấy là KHÔNG CÓ ĐƯỜNG NÀO từ app tới đây. "Không ai gọi" là thứ thay đổi
# lặng lẽ, nên nó phải có chốt — cùng lẽ với `cong-xanh-ma-khong-ai-goi`.
ra = subprocess.run(
    ["grep", "-rIl", "-e", "tools/xuong", "-e", "dieu_phoi", "-e", "worker_tu_moi",
     str(GOC / "web/src"), str(GOC / "web/functions"), str(GOC / "web/test")],
    capture_output=True, text=True)
t("không tệp nào trong web/ nhắc tới xưởng", not ra.stdout.strip())

# Và xưởng KHÔNG nhập gì từ `web/` ngoài DỮ LIỆU (đọc json là được, nhập mã thì không).
xau = []
for tep in sorted(HERE.glob("*.py")):
    ma = tep.read_text("utf8")
    if re.search(r"^\s*(import|from)\s+.*\bweb\b", ma, re.M):
        xau.append(tep.name)
t("xưởng không nhập mã nào từ web/", not xau)

# Mô hình phụ: mặc định TRÙNG model chính, và `tranh_luan` phải NÓI RA điều ấy.
t("có hằng cho model phụ", isinstance(chung.MO_HINH_PHU, str) and chung.MO_HINH_PHU)
t("`tranh_luan` đúng 2 vòng", tranh_luan.SO_VONG == 2)
t("giám khảo đúng 3 chiều", len(giam_khao.CHIEU) == 3)
t("≥2 bác thì loại", giam_khao.BAC_DE_LOAI == 2)
t("mọi chiều giám khảo đều có nhiệt và tên",
  all(c in giam_khao.NHIET and c in giam_khao.TEN for c in giam_khao.CHIEU))
# Ba chiều phải cho BA lời dặn KHÁC nhau — gộp lại thì "ba phiếu" chỉ là một phiếu
# nhân ba.
dan = {c: giam_khao._loi_dan(c, lop=4, chu_de="x", bang="dog", loai="tu",
                             muc={"tu": "dog"}) for c in giam_khao.CHIEU}
t("ba chiều cho ba lời dặn khác nhau", len(set(dan.values())) == 3)
t("mỗi lời dặn dặn ĐỪNG xét hai chiều kia",
  all(re.search(r"KHÔNG xét", d) for d in dan.values()))

# ── LỜI DẶN WORKER: mấy chốt không được rơi ──
w_dan = {
    "tu": worker_tu_moi.loi_dan(lop=4, chu_de="x", canh="", da_co=["dog"], so_tu=8),
    "mau_cau": worker_mau_cau.loi_dan(lop=4, chu_de="x", bang="dog", mau_da_co=[], so_mau=3),
    "kich_ban": worker_kich_ban.loi_dan(lop=4, chu_de="x", canh="", bang="dog",
                                        mau=[], so_buoc=6),
    "doc_hieu": worker_doc_hieu.loi_dan(lop=4, chu_de="x", bang="dog",
                                        so_cau_doan=6, so_cau_hoi=4),
}
for ten, d in w_dan.items():
    t(f"lời dặn {ten} đòi đúng một khối JSON", "MỘT KHỐI JSON" in d)
for ten in ("mau_cau", "kich_ban", "doc_hieu"):
    t(f"lời dặn {ten} cấm từ mới", "không từ mới" in w_dan[ten].lower()
      or "Tuyệt đối không từ mới" in w_dan[ten])
# ⚠ Hai chỗ hỏng đã có thật, mỗi chỗ một chốt trong lời dặn.
t("lời dặn kịch bản nói rõ `muc` CÓ ĐÚNG MỘT phần tử",
  "ĐÚNG MỘT PHẦN TỬ" in w_dan["kich_ban"])
t("lời dặn đọc hiểu nói rõ `muc` CÓ ĐÚNG MỘT phần tử",
  "ĐÚNG MỘT PHẦN TỬ" in w_dan["doc_hieu"])
t("lời dặn đọc hiểu đòi câu hỏi trả lời được TỪ ĐOẠN",
  "CHỈ BẰNG ĐOẠN VĂN" in w_dan["doc_hieu"])
t("lời dặn đọc hiểu đòi ĐÚNG MỘT đáp án đúng",
  "ĐÚNG MỘT phương án đúng" in w_dan["doc_hieu"])
t("lời dặn mẫu câu đòi ô trống ngoặc VUÔNG", "ngoặc VUÔNG" in w_dan["mau_cau"])
t("lời dặn từ mới cấm bịa IPA", "ĐỪNG bịa" in w_dan["tu"] or "KHÔNG ghi ipa" in w_dan["tu"])

# ── ĐẮP VÀO BỘ SINH: không đè mục của sách ──
sys.path.insert(0, str(GOC / "tools"))
import sinh_bai_tienganh as sb  # noqa: E402

u = {"tu": [{"tu": "dog", "nghia": "con chó", "ma": "v_g4_u1_dog"}],
     "mau_cau": [{"cong_thuc": "I like [Noun].", "ma": "sp_1"}]}
n = sb.dap_xuong(u, {"tu": [{"tu": "cat", "nghia": "con mèo", "vai": ["dt"]},
                            {"tu": "DOG", "nghia": "đè thử", "vai": ["dt"]}],
                     "mau_cau": [{"cong_thuc": "I like [Noun].", "vi_du": "x"},
                                 {"cong_thuc": "I have [Noun].", "vi_du": "y"}]})
t("đắp thêm mục mới", n["tu"] == 1 and n["mau_cau"] == 1)
t("KHÔNG đè mục đã có (kể cả khác chữ hoa)",
  u["tu"][0]["nghia"] == "con chó" and len(u["tu"]) == 2)
t("mục đắp vào có mã riêng để lần ra",
  any(str(x.get("ma", "")).startswith("v_x_") for x in u["tu"]))

print(f"\n{pass_} PASS · {fail} FAIL\n")
raise SystemExit(1 if fail else 0)
