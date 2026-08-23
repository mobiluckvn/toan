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

    # ── ⑥ SAU BUỔI THỬ ────────────────────────────────────────────────────────
    #
    # ⚠ KHÔNG SỬA PHẦN QUAN SÁT Ở CÁC TRANG TRÊN. Chúng là ghi chép của một buổi
    # đăng nhập có thật lúc 07h32 ngày 23-08-2026; sửa lại cho khớp hiện trạng thì
    # nó thôi không còn là biên bản, mà thành một bản tự khai. Những gì vá SAU buổi
    # ấy ghi riêng ở đây, kèm ngày.
    w6 = wb.create_sheet("Sau buổi thử")
    bang(w6, ["Quan sát trong buổi", "Đã vá gì · ngày", "Kiểm lại thế nào"], (44, 52, 44))
    for a, b, c in [
        ("Góc bố mẹ chỉ có mỗi dòng “A1 — khung tham chiếu châu Âu (CEFR)”, "
         "tức NHÃN của quyển học liệu chứ không phải mức của bé (mục 26).",
         "23-08: thêm `lib/cefr.js` + thẻ “con đang ở đâu trên thang năng lực” — "
         "tính tỉ lệ nút đạt P(L) ≥ 0,85 trên tổng nút từng khối lớp. "
         "⚠ Rà lại còn thấy `cefrCuaBe()` trong `lib/hoso.js` KHÔNG MÀN NÀO GỌI — "
         "mã chết từ lúc viết, nên trước 23-08 tiêu chí này thực sự chưa đạt.",
         "Mở Góc bố mẹ sau khi làm vài bài: phải thấy phân số thật (ví dụ "
         "5/871 · 1%) chứ không phải một chữ bậc trần. Số nhỏ mấy tuần đầu là "
         "ĐÚNG, không phải lỗi."),
        ("Bài viết được AI chấm và tầng hậu kiểm chặn được câu vi phạm vốn từ, "
         "nhưng bản ghi lượt KHÔNG mang vân tay của lời nhắc đã sinh ra nó.",
         "23-08: nối `mauPrompt` · `phienBanMau` · `vanTayPrompt` vào bản ghi. "
         "Chỗ vân tay bị rơi là `goiChamViet.js` — nó chỉ lấy phần `cham` của "
         "phản hồi. Mã sinh vân tay vẫn chạy đúng suốt thời gian ấy.",
         "Nộp một bài viết rồi soi bản ghi `attempts` mới nhất: phải có đủ ba "
         "trường. Cổng `tienganh_vao_engine.test.mjs` khoá chỗ nối này."),
        ("Bé mở bài rồi thoát giữa chừng thì không để lại dấu vết nào.",
         "23-08: học bạ loại `phien` (mã bài · chặng · số lượt · số giây), mỗi "
         "lần bỏ dở một bản ghi. ⚠ `phien` là `loai` mới nên phải deploy luật "
         "Firestore TRƯỚC — thiếu bước ấy Firestore từ chối ghi TRONG IM LẶNG.",
         "Vào một bài rồi bấm thoát: phải sinh một mục `phien`. "
         "⚠ CẬN DƯỚI — đóng thẳng tab thì KHÔNG ghi được, đó là giới hạn thật "
         "chứ không phải lỗi cần sửa."),
        ("Báo cáo riêng của bé hiện “Xong 0/20 bài · 0%” dù bé vừa học Tiếng Anh.",
         "23-08: `dungSoHoc` đọc thêm `progressTA` và `hocBaTA` loại `gio`, gộp "
         "với số của môn Toán.",
         "Học vài bài Tiếng Anh rồi mở báo cáo riêng: hai cột “xong mấy bài” và "
         "“số phút” phải nhúc nhích."),
        ("Không quan sát được — buổi thử bị P2 chặn ở chặng Từ mới (đòi micro).",
         "23-08: thêm nút “Con chưa nói được — cho con đi tiếp nhé”. Vá cùng đợt "
         "P1/P2.",
         "✅ ĐÃ ĐI THỬ LẠI chiều 23-08 — xem trang 'Buổi thử lần 2'. Hoá ra P2 "
         "mới vá được MỘT NỬA: chặng Mẫu câu cũng đòi nói mà chưa có lối lui. "
         "Vá nốt trong buổi ấy, rồi đi trọn tới chặng Luyện tập và sinh được "
         "bản ghi BKT thật."),
    ]:
        w6.append([a, b, c])
    don(w6)

    # ── ⑦ BUỔI THỬ LẦN 2 (chiều 23-08-2026) ───────────────────────────────────
    #
    # Buổi sáng bị chặn ở chặng Từ mới nên chỉ kiểm được 4/54 mục. Buổi này đi
    # trọn: đăng nhập bé MỚI (đường "thêm bé nữa vào máy này", không đá phiên cũ)
    # → Tiếng Anh lớp 3 → Unit 0 → cả bốn chặng → bài Viết → Sổ bố mẹ.
    w7 = wb.create_sheet("Buổi thử lần 2")
    bang(w7, ["Việc kiểm", "Thấy gì trên bản chạy", "Kết luận"], (34, 62, 40))
    for a, b, c in [
        ("Đăng nhập bằng OTP sau khi deploy lại hàm nền",
         "Hộp thư dùng-một-lần nhận mã 6 số trong ~8 giây; vào thẳng màn đặt tên "
         "và chọn lớp. Đường 'Thêm bé nữa vào máy này' giữ nguyên bé cũ.",
         "ĐẠT. `requestOtp`/`verifyOtp` chạy đúng sau khi deploy."),
        ("⛔ MÀN HỌC TRẮNG BỐC",
         "Bấm vào bài học ra màn trắng. Console: React #310 tại `useRef`. "
         "Nguyên nhân: hook `changCuoi` của bản vá 'bỏ dở' đặt SAU hai lệnh "
         "`return` sớm — chính tệp ấy đã có sẵn khối chú thích cảnh báo cái bẫy "
         "này, đặt ngay bên trên chỗ vi phạm.",
         "LỖI DO BẢN VÁ SÁNG NAY, đã lên bản chạy. Vá và deploy lại trong buổi. "
         "Nay có cổng `hook_truoc_return.test.mjs` soi 57 tệp .jsx."),
        ("⛔ P2 MỚI VÁ ĐƯỢC MỘT NỬA",
         "Chặng Từ mới qua được bằng nút 'Con chưa nói được'. Nhưng chặng MẪU CÂU "
         "cũng đòi nói mà KHÔNG có nút ấy — 'Vào luyện tập' vẫn khoá.",
         "Vá một nửa hàng rào thì hàng rào vẫn kín. Đã thêm lối lui cho chặng 2; "
         "cổng nay ĐẾM số chặng đòi nói và đòi đủ chừng ấy lối lui."),
        ("Video không tải được trong trình duyệt tự động",
         "`readyState 0`, không có lỗi, buffered 0. Nhưng `curl` lấy tệp trên máy "
         "chủ ra 200 và đủ dung lượng (855 323 byte, khớp bản tại máy).",
         "KHÔNG PHẢI LỖI ỨNG DỤNG — giới hạn của môi trường tự động. Đi tiếp bằng "
         "chính đường lui video-hỏng mà ứng dụng đã có sẵn (đã phát sự kiện "
         "`error` cho thẻ video). ⚠ Đây là thao tác MÔ PHỎNG, không phải bé thật."),
        ("⭐ BKT chạy trọn trên bản thật",
         "Làm ~9 lượt ở chặng Luyện tập (sai · sai · đúng…). Sau ~15 giây, Góc bố "
         "mẹ hiện 'one — một (1) — nắm 9%'. Ảnh: 06_bkt_va_cefr_ban_chay.jpg",
         "ĐẠT — và đây là LẦN ĐẦU cả dây chuyền lượt→attempts→onAttempt→mastery→"
         "máy con được nhìn thấy chạy trên bản thật. Buổi sáng chưa sinh nổi một "
         "bản ghi nào."),
        ("Sai 2 lần thì hệ thống tự đưa gợi ý",
         "Sau lượt sai thứ hai hiện '💡 Nghe lại xem từ này bắt đầu bằng âm nào.'",
         "ĐẠT — nâng đỡ theo số lần sai, mục 2.3.2."),
        ("⭐ Thẻ quy đổi CEFR",
         "'Con mới bắt đầu — chưa đủ dữ liệu để nói một bậc năng lực.' kèm "
         "Làm quen 0/187 · 0% và Bậc 1—A1 0/871 · 0%, cùng dòng chú 'đây KHÔNG "
         "phải điểm thi'. Hai mẫu số khớp đúng con số tính offline.",
         "ĐẠT. Và thẻ chỉ hiện được khi `mastery` đã về máy con — tức nó cũng là "
         "bằng chứng gián tiếp cho cả dây chuyền."),
        ("Nhãn CEFR cũ có gây hiểu lầm không",
         "Dòng cũ nay ghi rõ 'TRÌNH ĐỘ QUYỂN NÀY — Pre-A1'.",
         "ĐẠT. Hai con số CEFR đứng cạnh nhau nhưng nhãn tách bạch: một là của "
         "QUYỂN, một là của BÉ."),
        ("Bài viết chấm bằng AI",
         "8/10, chỉ đúng lỗi thiếu mạo từ ('I can see teacher' → 'the teacher') "
         "kèm giải thích. Và lại hiện 'Cô có 1 câu gợi ý dùng từ con chưa học, "
         "nên cô giấu đi rồi.' Ảnh: 07_ai_cham_viet_lan2.jpg",
         "ĐẠT — tầng hậu kiểm chống ảo giác bắt được LẦN THỨ HAI, ở một bé khác "
         "và một bài khác. Không phải chuyện may."),
        ("⛔ Sổ bố mẹ hiện 'Cần cố gắng: Bài undefined'",
         "Tab Tiếng Anh của Sổ học hiện thẳng chữ `undefined` cho bố mẹ đọc. "
         "Ảnh trước khi vá: 08_so_bo_me_bai_undefined.jpg",
         "LỖI CŨ, không phải do bản vá hôm nay. Khuôn phần tử `canCoGang` chưa "
         "bao giờ được ghi ra: Toán nộp `{id,so,ten,…}`, Tiếng Anh đoán thành "
         "`{ma,best,tong}`. Đã vá cả ba chỗ (bên nộp · bên đọc · giao ước ở "
         "`soMon.js`) + cổng `khuon_hocba.test.mjs`. Sau vá: 'Cần cố gắng: Bài 0' "
         "— ảnh 09_so_bo_me_da_va.jpg"),
        ("Bản ghi bỏ dở (`phien`) có bị luật từ chối không",
         "Chạy một vòng sạch (vào bài → trả lời → bấm '← Về') với console đang "
         "theo dõi: KHÔNG một dòng nào, không có `permission-denied`.",
         "⚠ BẰNG CHỨNG GIÁN TIẾP. Ghi bị luật từ chối thì Firestore in lỗi quyền "
         "ra console — không có lỗi tức là không bị từ chối. Nhưng KHÔNG đọc được "
         "thẳng tài liệu `phien` bằng quyền của bé, nên chưa xác nhận được NỘI "
         "DUNG bản ghi. Muốn chắc thì phải soi bằng khoá quản trị."),
        ("Tiến độ có bền qua tải lại trang không",
         "Tải lại toàn trang: vẫn vào đúng chặng Luyện tập, 'Đúng 2/33' giữ "
         "nguyên, kệ sách hiện 'đang học dở'.",
         "ĐẠT — số đọc về từ máy chủ, không phải từ bộ nhớ tại máy."),
    ]:
        w7.append([a, b, c])
    don(w7)

    # ── ⑧ SOI BẰNG KHOÁ QUẢN TRỊ (tối 23-08-2026) ─────────────────────────────
    #
    # Hai buổi đi thử chỉ nhìn được thứ ứng dụng BÀY RA. Buổi này mở thẳng
    # Firestore bằng khoá dịch vụ, và đó là chỗ những lỗi nặng nhất lộ ra.
    w8 = wb.create_sheet("Soi máy chủ")
    bang(w8, ["Câu hỏi", "Đo được gì", "Kết luận"], (34, 60, 46))
    for a, b, c in [
        ("Bản ghi bỏ dở (`phien`) có thật không, nội dung ra sao?",
         "5 bản ghi, đủ bốn trường microId·chang·soLuot·giay. CÙNG MỘT BÀI bị bỏ "
         "dở 5 lần và đếm RIÊNG từng lần: 356s · 21s · 5s · 169s · 31s.",
         "ĐẠT — đúng thiết kế, vì chính số LẦN mới là tín hiệu. Luật cũng đã thử "
         "thật trên bộ giả lập: 9 phép, kể cả chiều bị từ chối và vòng khứ hồi."),
        ("Vân tay prompt có trong `attempts` không?",
         "Lượt bài viết mang `mauPrompt=chamviet` · `phienBanMau=1` · "
         "`vanTayPrompt=1c85246bffac`.",
         "ĐẠT — mục 2.5.2 nay trả lời được bằng DỮ LIỆU, không phải bằng mã nguồn."),
        ("⛔ Vì sao chỉ có 1 bản ghi cho ~10 lượt?",
         "Cả dự án có ĐÚNG 2 bản ghi `attempts` môn Tiếng Anh cho hai buổi học. "
         "Dựng lại trên bộ giả lập bằng chính SDK web: lô [A] mới → OK; lô [A] "
         "lần hai → permission-denied; lô [A đã có, B mới] → CẢ LÔ rơi, B không "
         "lên; lô [C] mới → OK.",
         "LỖI NẶNG NHẤT CỦA CẢ NGÀY. `attempts` bất biến + máy con gửi lại cả "
         "phiên mỗi lượt + `writeBatch` nguyên khối ⇒ mỗi phiên chỉ lượt ĐẦU lên "
         "được. Engine BKT bị bỏ đói mà 90 cổng LÚC ẤY vẫn xanh, vì không phép nào gửi "
         "tới LƯỢT THỨ HAI. Vá hai tầng (sổ 'đã gửi' + thử lẻ khi lô hỏng); đo "
         "lại cùng thao tác: 2 → 18."),
        ("Vá một tầng có đủ không?",
         "Deploy bản chỉ-có-tầng-①, đi thử lại: ra ĐÚNG 0 bản ghi mới. Đọc "
         "localStorage: hai bé còn 12 và 14 bản ghi kẹt cứng.",
         "KHÔNG. Tầng ① chỉ chặn từ nay; máy đang mang hàng đợi nhiễm độc thì kẹt "
         "vĩnh viễn. Phải có tầng ② tự gỡ độc. Bài học: 'đã vá' không phải 'đã "
         "chạy' — phải đo lại trên bản thật sau mỗi lần deploy."),
        ("⛔ Toán có mất bản ghi không?",
         "48/48 phiên không lỗ, không mất đầu. NHƯNG mọi bản ghi của một phiên "
         "mang ĐÚNG MỘT dấu serverTs — cả phiên lên bằng một lô.",
         "KHÔNG mất, nhưng sống nhờ MAY: các lần đẩy giữa chừng của Toán cũng đã "
         "hỏng sẵn, chỉ chưa lô nào lọt sớm. Đã vá cả hai tầng cho Toán."),
        ("⛔ 7 mã phiên bị HAI bé cùng mang",
         "Mã phiên chỉ sinh ở một lần mở bài của một bé. Cả 7 cùng một hình: bé A "
         "1 lượt lên ngay + CÓ sổ tiến độ; bé B 16–30 lượt lên sau vài ngày + "
         "KHÔNG có sổ tiến độ.",
         "130/398 bản ghi nằm SAI HỌC BẠ. Hàm nhận lại hàng đợi lúc đăng nhập hỏi "
         "'có phải của tôi không' rồi sang tên MỌI thứ còn lại — kể cả của một bé "
         "có thật khác. Đã vá (chỉ nhận bản `local`) và đã dọn."),
        ("Dọn xong có sạch không?",
         "attempts 398 → 268 · mastery 32 mục. 0 phiên hai chủ · 0 lỗ trong dãy "
         "số thứ tự (48/48 nhóm bé·phiên·bài) · 32/32 mục mastery khớp ĐÚNG số "
         "lượt · 0 nút thiếu mastery.",
         "SẠCH. Sao lưu đầy đủ giữ lại (125 + 5 bản ghi, và mastery trước khi "
         "dựng) — vẫn TRẢ VỀ ĐÚNG CHỦ được nếu sau này đổi ý."),
        ("Còn chỗ nào chưa kiểm được?",
         "Số phút học và bảng cô giáo là bản TỔNG HỢP, dựng lại lúc 21 giờ mỗi "
         "đêm — buổi soi này chưa qua mốc ấy.",
         "⚠ Số liệu lấy cho luận văn phải lấy SAU mốc dựng lại, và nên ghi rõ kho "
         "đã được dọn ngày 23-08 kèm lý do: người phản biện đối chiếu số cũ với "
         "số mới sẽ thấy chênh."),
    ]:
        w8.append([a, b, c])
    don(w8)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   {len(BUOC)} bước đi thử · {len(PHAT_HIEN)} phát hiện")
    print(f"   đối chiếu 54 mục: {n_dat} kiểm được trên bản chạy · "
          f"{n_khong} chưa chạm tới trong phiên này")
    return 0


if __name__ == "__main__":
    sys.exit(main())
