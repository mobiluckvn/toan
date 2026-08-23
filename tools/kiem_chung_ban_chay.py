#!/usr/bin/env python3
"""BIÊN BẢN ĐI THỬ BẢN CHẠY THẬT — đối chiếu với Chương 2 luận văn.

    tools/tts/.venv/bin/python tools/kiem_chung_ban_chay.py
        → docs/kiem_chung_ban_chay.xlsx

Bác yêu cầu 23-08-2026: đăng nhập vào PRODUCTION bằng tài khoản thử, lấy OTP qua
mail, đi hết các luồng, giả lập các trường hợp, xem dữ liệu, rồi đối chiếu với
tài liệu Chương 2 và liệt kê chứng cứ.

── ⚠ BIÊN BẢN NÀY VIẾT TAY, KHÔNG PHẢI MÁY ĐO ──
Mọi dòng dưới đây là thứ TÔI ĐÃ NHÌN THẤY trên `ky-su-nhi.web.app` trong phiên
23-08-2026, hoặc đọc thẳng từ mã/dữ liệu trong kho. Chỗ nào KHÔNG kiểm được thì
ghi rõ là không kiểm được và vì sao — không suy ra từ mã rồi ghi thành "đã chạy
đúng". Đó là chỗ dễ nói quá nhất của một bản kiểm chứng.

── TÀI KHOẢN THỬ ──
`ksnthunghiemc2@emalupe.com` (hộp thư dùng-một-lần mail.tm) · uid
`wQsSiQeXYUSFhQTj7KVjfWxM1f03` · tên "Be Thu Nghiem C2" · lớp 5 · vai `learner`.
Đây là TÀI KHOẢN THẬT trên production, có sinh dữ liệu thật.

── VÌ SAO KHÔNG ĐỌC THẲNG FIRESTORE ──
Phép đọc Firestore bằng token của phiên đăng nhập bị chặn (trông y như hành vi
rút thông tin đăng nhập). Nên bằng chứng "dữ liệu" ở đây lấy từ hai đường KHÁC:
những gì chính app bày ra màn hình, và mã nguồn quyết định app ghi gì.
"""
from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/kiem_chung_ban_chay.xlsx"
NGUON = GOC / "docs/benchmark_chuong2.xlsx"

DAT, HONG, THIEU, KHONG = "ĐẠT", "⚠ LỆCH", "⚠ LỖ THỦNG", "chưa kiểm được"

# ── ① NHẬT KÝ BUỔI THỬ ────────────────────────────────────────────────────────
BUOC = [
    ("1", "Đăng nhập bằng OTP qua email thật",
     "Nhập `ksnthunghiemc2@emalupe.com` → bấm “Gửi mã cho tôi”",
     "Thư tới sau ~10 giây, từ `mobiluckvn@gmail.com`, tiêu đề “928071 là mã đăng "
     "nhập Toán Tư Duy lớp 5”. Nhập mã → vào thẳng màn “Con tên là gì nhỉ?”.",
     DAT, "Hộp thư mail.tm; ảnh màn đăng nhập"),
    ("2", "Lập hồ sơ bé lần đầu",
     "Điền tên “Be Thu Nghiem C2”, chọn lớp 5 → “Bắt đầu học”",
     "Vào Kệ sách, thẻ hồ sơ hiện tên + “Lớp 5”. Vai trò trong token là `learner` "
     "(máy chủ đặt, không phải máy con tự khai).",
     DAT, "ảnh Kệ sách sau đăng nhập"),
    ("3", "Nền trước khi học",
     "Mở Tiếng Anh lớp 5 → mở “Góc bố mẹ”",
     "“Xong 0/20 bài · 0%”. Góc bố mẹ CHỈ có một dòng: “A1 — khung tham chiếu "
     "châu Âu (CEFR)”, kèm lời rào “Chỉ tính lượt trả lời ĐẦU của mỗi câu…”.",
     DAT, "ảnh 03_goc_bo_me_trong.jpg (nền)"),
    ("4", "Chặng học bị KHOÁ theo thứ tự",
     "Mở Unit 1 → nhìn 4 thẻ chặng",
     "“1. Từ mới” mở; “🔒Mẫu câu”, “🔒Luyện tập”, “🔒Sát hạch” khoá. Nút “Sang mẫu "
     "câu” xám, kèm lời “Con làm nốt mấy ô còn trắng ở trên đi tiếp nhé.”",
     DAT, "ảnh màn Unit 1"),
    ("5", "⚠ CHẶNG 1 ĐÒI MICRO — không nói thì không qua được",
     "Bấm “Nghe cô đọc” cho từ `city`",
     "Ô việc chuyển sang dấu TAI (đã nghe) nhưng vẫn còn dấu BÚT (chưa nói). "
     "“Còn 8 việc nữa” không giảm. Mỗi từ trong 7 từ đều đòi một lượt NÓI.",
     HONG, "ảnh dải “VIỆC CỦA CON”"),
    ("6", "Đọc hiểu — trả lời SAI có chủ ý",
     "Unit 1 → “📖 Đọc hiểu” → câu 1 chọn “It's a cat.”",
     "“🤔 Chưa đúng. Con nghe lại rồi thử lần nữa nhé.” + nút “Thử lại”. KHÔNG lộ "
     "đáp án, KHÔNG cho đi tiếp.",
     DAT, "ảnh câu hỏi sau khi chọn sai"),
    ("7", "Đọc hiểu — bài vừa sửa 22-08 chạy đúng",
     "Đọc đoạn văn của Unit 1 trên bản chạy",
     "Đoạn nay là “This is my class. This is Mary. Mary is my friend. **My "
     "favourite animal is a dolphin.** I can see a dolphin.” — câu hỏi “What's "
     "your favourite animal?” nay TRẢ LỜI ĐƯỢC từ đoạn.",
     DAT, "ảnh màn đọc hiểu"),
    ("8", "Đọc hiểu — làm đúng cả hai câu",
     "Thử lại → chọn “It's a dolphin.” → câu 2 chọn “I can see a dolphin.”",
     "“2/2 câu đúng · Con đọc hiểu được cả đoạn rồi!”. ⚠ Điểm tính theo trạng "
     "thái CUỐI, không trừ lần sai đầu.",
     DAT, "ảnh màn kết bài đọc"),
    ("9", "Viết — AI chấm bài có lỗi cài sẵn",
     "Unit 1 → “✍ Viết”, gõ “…I can see dolphin…” (cố ý thiếu mạo từ `a`)",
     "AI trả **9/10**. Mục “CHỖ CẦN SỬA” gạch “I can see dolphin.” → “I can see a "
     "dolphin.”, giải thích “Câu cần có mạo từ 'a' trước danh từ số ít khi nói lần "
     "đầu.” BẮT ĐÚNG lỗi đã cài.",
     DAT, "docs/anh_kiem_chung/01_ai_cham_bai_viet.jpg"),
    ("10", "⭐ Tầng HẬU KIỂM chặn câu AI bịa — thấy tận mắt",
     "Đọc dòng cuối phần chấm",
     "“Cô có 1 câu gợi ý dùng từ con chưa học, nên cô giấu đi rồi.” — tức mô hình "
     "ĐÃ sinh ra một câu ngoài vốn từ, và tầng soi ĐÃ chặn nó lại trước khi tới "
     "mắt bé. Đây là bằng chứng CHẠY THẬT cho tầng hậu kiểm, không phải suy từ mã.",
     DAT, "docs/anh_kiem_chung/01_ai_cham_bai_viet.jpg"),
    ("11", "Minh bạch AI với bố mẹ",
     "Mở “Góc bố mẹ · bài viết và lời chấm”",
     "Bày đủ: CON VIẾT (nguyên văn) · MÁY CHẤM “9/10 · 1 lỗi” · LỜI CHO BỐ MẸ · và "
     "AI CHẤM: “Điểm và lời chấm do mô hình **openai/gpt-oss-120b** sinh ra. Đây là "
     "gợi ý cho con tự sửa, không phải điểm của giáo viên.”",
     DAT, "docs/anh_kiem_chung/02_goc_bo_me_bai_viet.jpg"),
    ("12", "Ôn tập — trộn bài, có ghi nguồn",
     "Mở “ÔN TẬP 1 · Thi thử”",
     "10 câu. Câu 1 “Từ bài: Unit 1”, câu 2 “Từ bài: Unit 2” — trộn nhiều unit "
     "trong một kỳ. Mỗi câu đều ghi rõ nó lấy từ bài nào.",
     DAT, "ảnh màn ôn tập"),
    ("13", "Ôn tập — gợi ý khi sai",
     "Trả lời sai câu nghe-chọn-hình",
     "“🤔 Chưa đúng…” + “💡 Nghe lại xem từ này bắt đầu bằng âm nào.” — gợi ý "
     "HƯỚNG SỰ CHÚ Ý, không đưa đáp án.",
     DAT, "ảnh câu ôn tập sai"),
    ("14", "⚠ Sau tất cả: Góc bố mẹ VẪN TRỐNG",
     "Về màn quyển, mở lại Góc bố mẹ",
     "“Đọc hiểu ✓” và “Viết ✓” đã đánh dấu xong ở Unit 1, nhưng tiến độ vẫn "
     "“Xong 0/20 bài · 0%”, và Góc bố mẹ VẪN chỉ có mỗi dòng CEFR A1 — không ma "
     "trận mức thạo, không dòng nào về cách bé học.",
     THIEU, "docs/anh_kiem_chung/03_goc_bo_me_trong.jpg"),
]

# ── ② PHÁT HIỆN ───────────────────────────────────────────────────────────────
PHAT_HIEN = [
    ("P1", "Ba trong bốn hoạt động KHÔNG vào BKT", "CAO",
     "Đọc hiểu · Viết · Ôn tập đều không phát `onLuot`, nên không sinh bản ghi "
     "`attempts`, nên KHÔNG cập nhật P(L) và không hiện trong ma trận Góc bố mẹ. "
     "Chỉ `BaiHoc.jsx` (Luyện tập + Sát hạch) phát.",
     "Đo hai tầng. Mã: `grep onLuot` — chỉ `CauHoi.jsx` phát, `BaiHoc.jsx` nối "
     "(dòng 148 · 160); `DocHieu.jsx` · `VietBai.jsx` · `OnTap.jsx` = 0. Dữ liệu: "
     "176 câu đọc hiểu (ta3·4·5) có 0/176 `maNut`; bài viết không có trường nào. "
     "Chạy thật: làm xong đọc hiểu + viết + 1 câu ôn tập → Góc bố mẹ vẫn trống.",
     "Nối `onLuot` cho ba màn ấy, và bổ `maNut` cho 176 câu đọc hiểu. Ôn tập thì "
     "dữ liệu ĐÃ có `maNut` (vá 23-08) — chỉ còn thiếu chỗ phát."),
    ("P2", "Chặng Từ mới đòi micro, không có đường vòng", "CAO",
     "Mỗi từ đòi một lượt NÓI mới tính xong. Bé không có micro, không cho phép "
     "micro, hoặc micro hỏng thì đứng luôn ở chặng 1 và KHÔNG BAO GIỜ tới được "
     "Luyện tập · Sát hạch — tức không bao giờ sinh được dữ liệu BKT.",
     "Chạy thật: bấm “Nghe cô đọc” cho `city` → ô việc mới xong nửa (tai xanh, "
     "bút vẫn trắng), “Còn 8 việc nữa” không giảm, nút “Sang mẫu câu” vẫn xám.",
     "Cho một đường lui: nghe đủ N lần thì tính xong, hoặc nút “con chưa nói "
     "được” — như `SatHach` đã có đường lui khi hỏng micro."),
    ("P3", "Thư OTP mang tên sản phẩm CŨ", "THẤP",
     "Tiêu đề thư: “928071 là mã đăng nhập **Toán Tư Duy lớp 5**”, và màn đăng "
     "nhập cũng in “Toán Tư Duy lớp 5” — trong khi sản phẩm nay là **Kỹ Sư Nhí**, "
     "hai môn, năm quyển. Bố mẹ nhận thư dễ tưởng thư lạ.",
     "Chạy thật: nguyên văn tiêu đề thư trong hộp thư thử.",
     "Sửa mặc định `appName` của `otpEmail()` trong `functions/src/otp.js` và "
     "tiêu đề màn đăng nhập."),
    ("P4", "Điểm bài đọc không trừ lần sai đầu", "THẤP",
     "Sai câu 1 rồi sửa lại vẫn ra “2/2 câu đúng”. Không sai về sư phạm (cho "
     "sửa là đúng), nhưng con số ấy KHÔNG phải thứ đo được năng lực.",
     "Chạy thật: sai “It's a cat.” → thử lại đúng → màn kết vẫn 2/2.",
     "Nếu muốn con số ấy đo được thì ghi thêm lần trả lời ĐẦU, như chính lời rào "
     "Góc bố mẹ đã hứa (“Chỉ tính lượt trả lời ĐẦU của mỗi câu”)."),
    ("P5", "Đọc hiểu KHÔNG đẩy lên máy chủ — nhưng là CHỦ Ý", "(không phải lỗi)",
     "Kết quả đọc hiểu chỉ ghi sổ tại máy. Đây KHÔNG phải sót: mã ghi rõ lý do và "
     "dẫn quyết định của bác.",
     "`ManTiengAnh.jsx` dòng ~157: “chỉ ghi sổ TẠI MÁY, không đẩy máy chủ… bác "
     "chốt bài đọc hiểu không cần vào sổ”.",
     "Không phải việc phải sửa. Ghi ở đây để bản kiểm chứng không báo nhầm."),
]

# ── ③ MỤC CHƯƠNG 2 — KIỂM ĐƯỢC TỚI ĐÂU TRÊN BẢN CHẠY ─────────────────────────
#
# ⚠ KHOÁ THEO SỐ THỨ TỰ DÒNG, KHÔNG KHỚP THEO TỪ KHOÁ.
# Bản đầu tôi khớp chữ ("RAG", "CEFR", "phản hồi") và nó báo ĐẠT cho 9 mục, trong
# đó "RT_avg — thời gian phản hồi trung bình" đạt chỉ vì chứa chữ "phản hồi", và
# cả ba bước RAG đạt chỉ vì chứa chữ "RAG". Một bản kiểm chứng mà tự nói quá thì
# tệ hơn không có. Nay chọn tay từng mục.
MOT_PHAN = "MỘT PHẦN"
CHAN_P2 = ("chưa kiểm được — CHẶN BỞI P2: không qua nổi chặng Từ mới vì đòi "
           "micro, nên phiên này không sinh được bản ghi `attempts` nào")

KIEM = {
    26: (MOT_PHAN, "Thấy “A1 — khung tham chiếu châu Âu (CEFR)” ở Góc bố mẹ. "
                   "Phần SỞ THÍCH và ĐỊNH DẠNG ƯA THÍCH thì không thấy bày ra."),
    35: (DAT, "AI đóng vai cô giáo chấm bài viết: có lời khen, có chỗ cần sửa, "
              "có lời riêng cho bố mẹ (bước 9 · 11)."),
    36: (MOT_PHAN, "Thấy LLM SINH RA một câu gợi ý cho bé (nó bị tầng soi chặn — "
                   "chính việc bị chặn chứng minh nó có sinh). Chưa thấy LLM sinh "
                   "BÀI TẬP, vì đường tới đó bị P2 chặn."),
    37: (DAT, "Không chỉ báo sai: gạch câu sai → viết câu đúng → GIẢI THÍCH “Câu "
              "cần có mạo từ 'a' trước danh từ số ít khi nói lần đầu.” (bước 9)."),
    38: (DAT, "⭐ Bằng chứng mạnh nhất của buổi: “Cô có 1 câu gợi ý dùng từ con "
              "chưa học, nên cô giấu đi rồi.” Mô hình CÓ bịa từ lạ, tầng soi CÓ "
              "chặn, và bé thấy đúng thông báo ấy (bước 10)."),
    41: (DAT, "Cùng bằng chứng mục 38 — đây là tầng “tạo sinh có kiểm soát” chạy "
              "thật, không phải suy từ mã."),
}

# Mục nào chặn vì P2, mục nào đơn giản là không chạm tới trong phiên.
BI_CHAN_P2 = {1, 2, 3, 5, 13, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31,
              32, 33, 34, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54}



def main() -> int:
    wb = Workbook()
    dam = Font(bold=True, color="FFFFFF")
    nen = PatternFill("solid", fgColor="2F4A6B")
    do = PatternFill("solid", fgColor="F8D7DA")
    vang = PatternFill("solid", fgColor="FFF3CD")
    luc = PatternFill("solid", fgColor="D4EDDA")
    tren = Alignment(vertical="top", wrap_text=True)

    def bang(ws, dau, rong):
        ws.append(dau)
        for c in ws[1]:
            c.font, c.fill = dam, nen
        for c, r in zip("ABCDEFG", rong):
            ws.column_dimensions[c].width = r

    def don(ws):
        for r in ws.iter_rows(min_row=1):
            for c in r:
                c.alignment = tren
        ws.freeze_panes = "A2"

    ws = wb.active
    ws.title = "Buổi thử trên bản chạy"
    bang(ws, ["#", "Việc", "Tôi làm gì", "Máy trả lời gì", "Kết quả", "Chứng cứ"],
         (5, 34, 40, 62, 14, 34))
    for b in BUOC:
        ws.append(list(b))
        m = ws[ws.max_row]
        if b[4] == DAT:
            m[4].fill = luc
        elif b[4] == THIEU:
            m[4].fill = do
        elif b[4] == HONG:
            m[4].fill = vang
    don(ws)

    w2 = wb.create_sheet("Phát hiện")
    bang(w2, ["Mã", "Phát hiện", "Mức", "Bé chịu gì", "Đo bằng gì", "Cách sửa"],
         (6, 40, 12, 56, 64, 48))
    for p in PHAT_HIEN:
        w2.append(list(p))
        if p[2] == "CAO":
            for c in w2[w2.max_row]:
                c.fill = do
        elif p[2] == "THẤP":
            for c in w2[w2.max_row]:
                c.fill = vang
    don(w2)

    # ── đối chiếu 54 mục ──
    w3 = wb.create_sheet("Đối chiếu Chương 2")
    bang(w3, ["Mục", "YÊU CẦU trong luận văn", "Trạng thái theo bản rà 22-08",
              "KIỂM TRÊN BẢN CHẠY 23-08", "Chứng cứ chạy thật"],
         (9, 56, 20, 20, 62))
    n_dat = n_khong = 0
    if NGUON.exists():
        src = load_workbook(NGUON)["Đối chiếu"]
        for r in range(2, src.max_row + 1):
            muc = src.cell(r, 1).value
            yeu = str(src.cell(r, 2).value or "")
            cu = src.cell(r, 3).value
            i = r - 1
            if i in KIEM:
                kq, bc = KIEM[i]
            elif i in BI_CHAN_P2:
                kq, bc = KHONG, CHAN_P2
            else:
                kq = KHONG
                bc = ("chưa chạm tới trong phiên này — mục thuộc TẦNG DỮ LIỆU/ĐỒ "
                      "THỊ, không bày ra màn hình nào để nhìn. Đã rà bằng mã và "
                      "dữ liệu ngày 22-08, xem cột bên trái.")
            n_dat += kq == DAT
            n_khong += kq == KHONG
            w3.append([muc, yeu, cu, kq, bc])
            if kq == DAT:
                w3.cell(w3.max_row, 4).fill = luc
            elif kq == MOT_PHAN:
                w3.cell(w3.max_row, 4).fill = vang
    don(w3)

    w4 = wb.create_sheet("Làm lại buổi thử")
    bang(w4, ["Bước", "Lệnh / thao tác", "Ghi chú"], (6, 66, 60))
    for i, (l, g) in enumerate([
        ("Lập hộp thư dùng-một-lần: POST https://api.mail.tm/accounts",
         "Địa chỉ bị bỏ dấu chấm — lấy địa chỉ trong phản hồi mà dùng, đừng dùng "
         "địa chỉ mình gõ."),
        ("Mở https://ky-su-nhi.web.app → Đăng nhập → nhập địa chỉ ấy",
         "OTP sống 10 phút, 60 giây mới cho xin lại, tối đa 5 mã/giờ."),
        ("GET https://api.mail.tm/messages với Bearer token",
         "Mã 6 số nằm ngay trong TIÊU ĐỀ thư, không cần mở nội dung."),
        ("Nhập mã → đặt tên bé → chọn lớp",
         "Tài khoản mới nhận vai `learner` do MÁY CHỦ đặt."),
        ("Đi các luồng: Đọc hiểu → Viết → Ôn tập",
         "Chặng Từ mới cần micro, không đi bằng chuột được."),
        ("Đọc dữ liệu",
         "⚠ Không đọc thẳng Firestore bằng token phiên được (bị chặn, và đúng). "
         "Dùng những gì app bày ra + đọc mã quyết định app ghi gì."),
    ], 1):
        w4.append([i, l, g])
    don(w4)

    w5 = wb.create_sheet("Tài khoản thử")
    bang(w5, ["Trường", "Giá trị"], (26, 70))
    for k, v in [
        ("Email", "ksnthunghiemc2@emalupe.com (mail.tm, dùng-một-lần)"),
        ("uid", "wQsSiQeXYUSFhQTj7KVjfWxM1f03"),
        ("Tên bé", "Be Thu Nghiem C2"),
        ("Lớp", "5"),
        ("Vai", "learner (máy chủ đặt qua custom claim)"),
        ("Ngày thử", "23-08-2026"),
        ("⚠ Dữ liệu thật", "Tài khoản này CÓ sinh dữ liệu thật trên production: "
                           "users/, hocBaTA (bài viết), otpCodes. Muốn dọn thì "
                           "dùng tools/xoa_log_tienganh.mjs (cần khoá quản trị)."),
    ]:
        w5.append([k, v])
    don(w5)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   {len(BUOC)} bước đi thử · {len(PHAT_HIEN)} phát hiện")
    print(f"   đối chiếu 54 mục: {n_dat} kiểm được trên bản chạy · "
          f"{n_khong} chưa chạm tới trong phiên này")
    return 0


if __name__ == "__main__":
    sys.exit(main())
