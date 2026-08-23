#!/usr/bin/env python3
"""SOÁT DỮ LIỆU GIÁM SÁT — mọi hành động của bé có được ghi lại không?

    tools/tts/.venv/bin/python tools/soat_giam_sat.py → docs/soat_giam_sat.xlsx

Bác hỏi 23-08-2026: rà lại xem số liệu đã lưu hết chưa, để mọi hành động của con
đều có dữ liệu giám sát phục vụ adaptive learning như đề tài; thống kê chi tiết,
đối chiếu Chương 2 (đáp ứng · chưa · không thể), và chứng cứ adaptive qua test
end-to-end, kèm phần báo cáo cho giáo viên.

── ⚠ BẢN NÀY ĐO, KHÔNG ĐOÁN ──
Mỗi dòng dưới đây đến từ một trong ba nguồn, và cột "đo bằng gì" nói rõ nguồn nào:
  MÃ      đọc thẳng mã nguồn (ví dụ `grep onLuot` từng màn);
  DỮ LIỆU đếm trên tệp nội dung đã dựng;
  CHẠY    nhìn thấy trên `ky-su-nhi.web.app` bằng tài khoản thử.
Chỗ nào CHƯA kiểm được thì ghi là chưa, không suy từ mã rồi ghi thành "đã chạy".
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/soat_giam_sat.xlsx"
SRC = GOC / "web/src/mon/tienganh"

DU, THIEU, KHONG, COYS = "ĐỦ", "⚠ THIẾU", "✗ KHÔNG CÓ", "cố ý không có"

# ── ① MỌI HÀNH ĐỘNG CỦA BÉ ───────────────────────────────────────────────────
# (hành động, màn, có attempts?, ghi ở đâu nữa, nhận xét)
HANH_DONG = [
    ("Xem video từ mới", "BaiHoc · chặng 1", KHONG,
     "`moc.daXem` — CHỈ Ở MÁY",
     "`luuBai` không đẩy `moc` lên máy chủ. CỐ Ý: đổi máy thì bé vào lại từ đầu "
     "chặng, mất mấy phút chứ không mất bài. Nhưng nghĩa là 'con đã xem giảng "
     "chưa' KHÔNG có bằng chứng trên máy chủ."),
    ("Nghe một từ mới", "BaiHoc · chặng 1", KHONG,
     "`moc.daNghe` — CHỈ Ở MÁY", "Cùng lý do trên."),
    ("Nói một từ (micro)", "BaiHoc · chặng 1", KHONG,
     "`moc.soNoi` — CHỈ Ở MÁY",
     "⚠ Đây là phần LUYỆN PHÁT ÂM, có chấm điểm từng lượt, mà điểm ấy không lên "
     "máy chủ. Chiều Nhận thức của kỹ năng NÓI vì thế trống."),
    ("Khai 'con chưa nói được'", "BaiHoc · chặng 1", KHONG, "chỉ là state trong màn",
     "Thêm 23-08 để bé không có micro vẫn đi tiếp được (lỗ thủng P2). Việc bé "
     "PHẢI dùng đường lui này là một tín hiệu đáng ghi mà nay chưa ghi."),
    ("Xem video mẫu câu", "BaiHoc · chặng 2", KHONG, "`moc.daXem` — CHỈ Ở MÁY", ""),
    ("Nói cả câu (micro)", "BaiHoc · chặng 2", KHONG, "`moc.soNoi` — CHỈ Ở MÁY", ""),
    ("Trả lời câu LUYỆN TẬP", "BaiHoc · chặng 3", DU,
     "`attempts` (phase `practice`) → BKT → `mastery/`",
     "⚠ CHỖ NỐI NÀY MỚI CÓ TỪ 23-08. Trước đó `<BaiHoc>` không được truyền "
     "`onLuot`, nên 4226 câu đã gắn mã nút vẫn KHÔNG vào engine lần nào."),
    ("Trả lời câu SÁT HẠCH", "BaiHoc · chặng 4", DU,
     "`attempts` (phase `assess`) → BKT → `mastery/`", "Cùng chỗ nối trên."),
    ("Xong cả bài", "BaiHoc", "—",
     "`progressTA/{uid}/micros` + `hocBaTA` loai `hoSo`",
     "`progressTA` là thứ kích hoạt `onMicroDoneTA` sinh thẻ ôn +1/+3/+7."),
    ("Trả lời câu ĐỌC HIỂU", "DocHieu", DU,
     "`attempts` (phase `check`) + `hocBaTA` loai `doc`",
     "Cả hai đường đều MỚI CÓ TỪ 23-08. Trước đó đọc hiểu không ghi gì lên máy chủ."),
    ("Nộp BÀI VIẾT (AI chấm)", "VietBai", DU,
     "`attempts` (phase `worked`) + `hocBaTA` loai `viet`",
     "`hocBaTA` giữ NGUYÊN VĂN bài viết và lời chấm — bố mẹ và cô giáo đọc được. "
     "Đường vào engine mới có từ 23-08; ngưỡng đạt 7/10 khai ở `VietBai.DIEM_DAT`."),
    ("Làm kỳ ÔN TẬP chương", "OnTap", DU,
     "`attempts` (phase `assess`) + `hocBaTA` loai `chuong`", "Đường engine mới từ 23-08."),
    ("Ôn lại một THẺ tới hạn", "OnLai", DU,
     "`attempts` + `reviewQueue/{uid}/cards`",
     "Màn DUY NHẤT nuôi engine trước ngày 23-08 — nhưng thẻ chỉ sinh sau khi xong "
     "bài, nên gần như không bao giờ tới lượt."),
    ("Nói chuyện ở PHÒNG LUYỆN NÓI", "PhongNoi", KHONG,
     "`phongNoiTA/{uid}/buoi` — có bản ghi buổi",
     "⚠ KHOẢNG TRỐNG CÒN LẠI. Cả buổi nói được lưu (bé nói gì, cô sửa gì), nhưng "
     "KHÔNG phát `onLuot` nên không sinh `attempts`: kỹ năng NÓI hoàn toàn nằm "
     "ngoài BKT. Đây là kỹ năng duy nhất còn ngoài engine."),
    ("Chọn từ mình thích nhất", "PhongNoi", "—", "`hocBaTA` loai `soThich`",
     "Chiều Động lực (M) của mục 2.1.2 — cô giáo máy lấy làm ngữ cảnh buổi sau."),
    ("Bỏ dở giữa chừng", "mọi màn", KHONG, "không ghi gì",
     "Bé mở bài rồi thoát, hoặc sai ba lần rồi bỏ — không dấu vết nào. Chiều Thời "
     "gian (T) của luận văn có nhắc 'đo mệt mỏi nhận thức'; muốn đo thì phải có "
     "sự kiện RỜI MÀN, nay chưa có."),
]

# ── ② TRƯỜNG DỮ LIỆU vs MỤC 2.5.2 / 2.3.1 CỦA LUẬN VĂN ───────────────────────
TRUONG = [
    ("Node_ID", "2.5.2 · dữ liệu nhận thức", "`bktUnit` + `maNutDs`", DU,
     "MÃ · `suKien.js` dòng 106. DỮ LIỆU · 176/176 câu đọc hiểu và 75/75 bài viết "
     "nay có mã nút (vá 23-08)."),
    ("Đúng / sai", "2.5.2 · dữ liệu nhận thức", "`correct`", DU, "MÃ · `suKien.js`"),
    ("Câu trả lời THÔ", "2.5.2 · dữ liệu nhận thức", "`answer` + `expected`", DU,
     "MÃ · giữ cả đáp án bé chọn lẫn đáp án đúng, nên chấm lại được về sau."),
    ("Thời gian phản hồi (RT)", "2.5.2 · dữ liệu hành vi", "`ms` → `msTrungBinh`", DU,
     "MÃ · đo TRƯỚC khi đổi state. ⚠ Bài VIẾT để `ms: null` — màn không biết bé gõ "
     "bài bao lâu, điền số vào đó là bịa."),
    ("Số lần trợ giúp (H_req)", "2.5.2 · dữ liệu hành vi", "`hintsUsed` → `goiTrungBinh`",
     DU, "MÃ · ⚠ nghĩa hơi khác Toán: bên Tiếng Anh gợi ý hiện TỰ ĐỘNG, nên đây là "
     "'đã THẤY mấy gợi ý', không phải 'đã XIN mấy lần'."),
    ("P(L) trước / sau", "2.5.2 · bối cảnh hệ thống", "`pTruoc` và `p` trong `mastery/`",
     DU, "MÃ · `bkt.js` ghi cả hai, nên `ΔC = p - pTruoc` lúc nào cũng tính được."),
    ("Mã prompt để kiểm toán", "2.5.2 · bối cảnh hệ thống", "`vantay.js` — băm KHUNG lời dặn",
     "MỘT PHẦN", "MÃ · vân tay đi kèm KẾT QUẢ trả về cho máy con, KHÔNG nằm trong "
     "`attempts`. Muốn kiểm toán 'câu này sinh bởi prompt nào' thì phải nối thêm."),
    ("Mốc thời gian mili-giây", "2.5.2 · định danh & thời gian", "`ts` + `serverTs`", DU,
     "MÃ · mốc RIÊNG từng lượt, không dùng chung một mốc cho cả loạt."),
    ("Chuỗi sự kiện BẤT BIẾN", "2.5.2 · lưu vết hướng sự kiện", "`attempts` immutable",
     DU, "MÃ · `firestore.rules` — `allow update, delete: if false`. Không ai sửa "
     "được điểm đã ghi, kể cả admin."),
    ("struggle_count", "2.3.1 · che phủ trạng thái", "`saiLienTiep`", DU, "MÃ · `bkt.js`"),
    ("last_interacted", "2.3.1 · che phủ trạng thái", "`lastSeen`", DU, "MÃ · `bkt.js`"),
    ("p_learned", "2.3.1 · che phủ trạng thái", "`p`", DU, "MÃ · `bkt.js`"),
    ("Hồ sơ: định dạng bé hợp", "2.3.1 · hồ sơ bé", "`hocBaTA` loai `hoSo`", DU,
     "CHẠY · Góc bố mẹ hiện 'DẠNG CÂU CON LÀM TỐT NHẤT — chọn đáp án, đúng 50% "
     "(8 câu)' sau khi bé làm 3 bài đọc."),
    ("Hồ sơ: sở thích", "2.3.1 · hồ sơ bé", "`hocBaTA` loai `soThich`", DU, "MÃ"),
    ("Hồ sơ: CEFR", "2.3.1 · hồ sơ bé", "suy từ quyển đang học", DU,
     "CHẠY · Góc bố mẹ hiện 'A1 — khung tham chiếu châu Âu (CEFR)'."),
    ("Điểm phát âm từng từ", "2.1.2 · chiều Nhận thức (kỹ năng NÓI)", "chỉ ở máy",
     COYS, "MÃ · `moc.soNoi` không nằm trong danh sách trường `luuBai` đẩy lên."),
    ("Sự kiện RỜI MÀN / bỏ dở", "2.1.2 · chiều Thời gian (mệt mỏi)", "không có", KHONG,
     "MÃ · không màn nào phát sự kiện thoát."),
]

# ── ③ ADAPTIVE: CHỨNG CỨ TỪ TEST END-TO-END ──────────────────────────────────
ADAPTIVE = [
    ("Khoá chặng theo thứ tự", "CHẠY ✓",
     "Mở Unit 1: '1. Từ mới' mở, '🔒Mẫu câu' '🔒Luyện tập' '🔒Sát hạch' khoá. "
     "Làm xong chặng 1 thì chặng 2 mở ra và chặng 1 đổi thành '✓ Từ mới'.",
     "Ảnh: trước và sau khi xong chặng 1."),
    ("Phản hồi hình thành, không lộ đáp án", "CHẠY ✓",
     "Chọn sai → '🤔 Chưa đúng. Con nghe lại rồi thử lần nữa nhé.' + nút 'Thử lại'. "
     "Không hiện đáp án đúng, không cho đi tiếp.", "Ảnh màn đọc hiểu."),
    ("Gợi ý phân tầng khi sai", "CHẠY ✓",
     "Kỳ ôn tập, sai câu nghe-chọn-hình → thêm dòng '💡 Nghe lại xem từ này bắt "
     "đầu bằng âm nào.' — hướng sự chú ý, không đưa đáp án.", "Ảnh màn ôn tập."),
    ("Đường lui khi bé không nói được", "CHẠY ✓",
     "Bấm 'Con chưa nói được — cho con đi tiếp nhé' → thanh việc đổi từ 'Còn 8 "
     "việc nữa' sang 'Con đi tiếp được rồi. Ô nào còn trắng thì làm thêm cũng "
     "hay.' Đây là thích ứng theo ĐIỀU KIỆN của bé, không phải theo điểm.",
     "Ảnh thanh VIỆC CỦA CON trước/sau."),
    ("Hồ sơ 'dạng câu bé làm tốt' tự dựng", "CHẠY ✓",
     "Sau 3 bài đọc (8 lượt trả lời đầu), Góc bố mẹ mọc thêm khối 'DẠNG CÂU CON "
     "LÀM TỐT NHẤT — chọn đáp án, đúng 50% (8 câu)'. Trước khi vá P1 khối này "
     "KHÔNG tồn tại. Đây là chiều Sư phạm (P) của mục 2.1.2 chạy thật.",
     "Ảnh Góc bố mẹ trước và sau."),
    ("AI chấm có giải thích + chặn ảo giác", "CHẠY ✓",
     "Bài viết cài lỗi thiếu mạo từ → AI trả 9/10, gạch câu sai, viết câu đúng, "
     "GIẢI THÍCH lý do. Và: 'Cô có 1 câu gợi ý dùng từ con chưa học, nên cô giấu "
     "đi rồi' — mô hình CÓ bịa, tầng hậu kiểm CÓ chặn.",
     "docs/anh_kiem_chung/01_ai_cham_bai_viet.jpg"),
    ("Xếp câu theo ZPD", "CHƯA KIỂM ĐƯỢC",
     "Nằm trong chặng Luyện tập. Phiên này không tới được: chặng Mẫu câu khoá "
     "theo 'đã xem hết video', mà video trong trình duyệt tự động của tôi kẹt ở "
     "vòng quay. ⚠ Tệp video tải bình thường (HTTP 200, ~800 KB) nên đây nhiều "
     "phần là môi trường tôi chạy, KHÔNG kết luận là lỗi sản phẩm.", "—"),
    ("Nhánh Vượt ải / Phụ đạo", "CHƯA KIỂM ĐƯỢC",
     "Cần P(L) vượt ngưỡng hoặc sai liên tiếp ≥3 tại một nút, tức phải qua được "
     "Luyện tập. Cùng lý do trên.", "—"),
    ("Lặp lại ngắt quãng (+1/+3/+7)", "CHƯA KIỂM ĐƯỢC",
     "Thẻ ôn sinh khi `progressTA` được ghi (xong một bài), và chỉ tới hạn sau ít "
     "nhất một NGÀY. Một phiên không đủ.", "—"),
    ("Lan truyền chẩn đoán tới nút gốc", "CHƯA KIỂM ĐƯỢC",
     "Khối 'Góc bố mẹ · con đang mắc ở đâu' chỉ hiện khi có nút p < 0,5 trong "
     "`mastery/`. Chưa thấy hiện trong phiên; chưa tách được là do chưa đủ dữ "
     "liệu, do trễ hàm nền, hay do ngưỡng.", "—"),
]

# ── ④ BÁO CÁO CHO GIÁO VIÊN ──────────────────────────────────────────────────
GIAO_VIEN = [
    ("Bảng cô giáo (`teacherBoard/global`)", "ĐỌC ĐƯỢC dữ liệu Tiếng Anh",
     "`docDuLieuChung` gộp CẢ HAI môn: `progress` + `progressTA`, `hocBa` + "
     "`hocBaTA`, và `attempts` không lọc môn.",
     "MÃ · `functions/index.js` dòng 249–257."),
    ("Cột 'bẫy hay dính' (topTraps)", "CÓ", "Đếm theo `itemId` trên `attempts` — "
     "môn nào cũng vào.", "MÃ · `teacherboard.js`"),
    ("Cột 'bé đang mắc' (stuckLearners)", "CÓ", "Lọc `attempts` có `tries >= 3`.",
     "MÃ · `teacherboard.js`"),
    ("Số phút học", "CÓ, nhưng LỆCH", "`minutesOf` chỉ tính bản ghi có `v >= 2`. "
     "Bản ghi Tiếng Anh có `v` nên vào được.", "MÃ · `teacherboard.js` dòng 87"),
    ("Bài viết + lời chấm AI", "CÓ", "`hocBaTA` loai `viet` giữ nguyên văn bài bé "
     "viết và lời chấm; luật cho giáo viên đọc (`canRead`).", "MÃ · `firestore.rules`"),
    ("⚠ Báo cáo RIÊNG của bé (`report/{uid}`)", "THIẾU MÔN TIẾNG ANH",
     "`dungSoHoc` đọc `attempts` (đủ) và `mastery/` (đủ), nhưng `progress/` và "
     "`hocBa/…loai='gio'` thì CHỈ của Toán. Nên phần 'xong bao nhiêu bài' và 'số "
     "phút học' của bé bỏ sót toàn bộ Tiếng Anh.",
     "MÃ · `functions/index.js` dòng 138–145."),
    ("⚠ Bảng xếp hạng", "CHƯA CÓ TIẾNG ANH",
     "`bangXepHang` hàm nền hiện chỉ đếm sao của Toán; bên Tiếng Anh trả `null` "
     "thay vì bày một bảng chỉ có điểm Toán mà gắn nhãn Tiếng Anh.",
     "MÃ · `duLieu.js` — đã ghi rõ là chủ ý tạm thời."),
]


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
        for c, r in zip("ABCDEF", rong):
            ws.column_dimensions[c].width = r

    def don(ws):
        for r in ws.iter_rows(min_row=1):
            for c in r:
                c.alignment = tren
        ws.freeze_panes = "A2"

    def to(ws, cot, dieu):
        for c in ws[ws.max_row]:
            if dieu == KHONG:
                c.fill = do
            elif dieu in (THIEU, COYS, "MỘT PHẦN"):
                c.fill = vang
            elif dieu == DU:
                c.fill = luc

    ws = wb.active
    ws.title = "Hành động → dữ liệu"
    bang(ws, ["Hành động của bé", "Màn", "Có vào ENGINE?", "Còn ghi ở đâu",
              "Nhận xét"], (30, 22, 16, 34, 66))
    for h in HANH_DONG:
        ws.append(list(h))
        to(ws, 3, h[2])
    don(ws)

    w2 = wb.create_sheet("Trường dữ liệu vs luận văn")
    bang(w2, ["Trường luận văn ĐÒI", "Mục", "Hệ thống có gì", "Đáp ứng",
              "Đo bằng gì"], (28, 30, 34, 14, 58))
    for t in TRUONG:
        w2.append(list(t))
        to(w2, 4, t[3])
    don(w2)

    w3 = wb.create_sheet("Chứng cứ ADAPTIVE (E2E)")
    bang(w3, ["Cơ chế thích ứng", "Kiểm được chưa", "Thấy gì trên bản chạy",
              "Chứng cứ"], (34, 20, 74, 42))
    for a in ADAPTIVE:
        w3.append(list(a))
        if a[1].startswith("CHẠY"):
            w3.cell(w3.max_row, 2).fill = luc
        else:
            w3.cell(w3.max_row, 2).fill = vang
    don(w3)

    w4 = wb.create_sheet("Báo cáo cho giáo viên")
    bang(w4, ["Mục", "Trạng thái", "Chi tiết", "Đo bằng gì"], (36, 30, 66, 40))
    for g in GIAO_VIEN:
        w4.append(list(g))
        if g[1].startswith("⚠") or "THIẾU" in g[1] or "CHƯA" in g[1] or "LỆCH" in g[1]:
            w4.cell(w4.max_row, 2).fill = vang
        else:
            w4.cell(w4.max_row, 2).fill = luc
    don(w4)

    w5 = wb.create_sheet("Tổng hợp")
    bang(w5, ["Câu hỏi của bác", "Trả lời"], (40, 92))
    for k, v in [
        ("Số liệu đã lưu hết chưa?",
         "CHƯA HẾT. 6/16 hành động của bé vào được engine — nhưng trước 23-08 con "
         "số ấy là 1/16 (chỉ màn ôn thẻ, mà thẻ gần như không bao giờ tới hạn). "
         "Còn thiếu ba nhóm: (a) mọi thao tác trong chặng Từ mới và Mẫu câu — xem "
         "video, nghe, NÓI — chỉ ghi ở máy; (b) phòng luyện nói có lưu buổi nhưng "
         "không sinh `attempts`; (c) không có sự kiện bỏ dở."),
        ("Chỗ nào ĐÁP ỨNG đề tài?",
         "9/10 trường mà mục 2.5.2 và 2.3.1 đòi đã có thật trong `attempts` và "
         "`mastery/`: Node_ID · đúng/sai · câu trả lời thô · RT · H_req · P(L) "
         "trước/sau · mốc mili-giây · chuỗi bất biến · struggle_count."),
        ("Chỗ nào CHƯA đáp ứng?",
         "① Mã prompt chưa nằm trong `attempts` (vân tay có, nhưng đi kèm kết quả "
         "trả về chứ không lưu cùng lượt) → chưa kiểm toán được 'câu này do prompt "
         "nào sinh'. ② Kỹ năng NÓI hoàn toàn ngoài BKT. ③ Báo cáo riêng của bé bỏ "
         "sót tiến độ và số phút của Tiếng Anh."),
        ("Chỗ nào KHÔNG THỂ đáp ứng?",
         "Điểm phát âm từng từ: máy con chấm bằng bộ nhận dạng giọng nói của "
         "trình duyệt, kết quả phụ thuộc micro và tiếng ồn phòng học. Đẩy con số "
         "ấy vào mức thạo là đưa nhiễu của thiết bị vào hồ sơ học tập. Muốn đo "
         "thật thì cần chấm phát âm phía máy chủ — một hệ khác hẳn."),
        ("Adaptive thể hiện thế nào?",
         "6 cơ chế THẤY TẬN MẮT trên bản chạy (xem trang 'Chứng cứ ADAPTIVE'): "
         "khoá chặng tuần tự · phản hồi hình thành · gợi ý phân tầng · đường lui "
         "theo điều kiện của bé · hồ sơ 'dạng câu bé làm tốt' tự dựng sau 8 lượt · "
         "AI chấm có giải thích kèm tầng chặn ảo giác. 4 cơ chế CHƯA kiểm được "
         "(ZPD · vượt ải/phụ đạo · lặp ngắt quãng · lan truyền chẩn đoán) — mỗi "
         "cái ghi rõ vì sao chưa."),
        ("Giáo viên thấy được chứng cứ không?",
         "CÓ. Bảng cô giáo gộp cả hai môn (`attempts` + `progressTA` + `hocBaTA`), "
         "nên cô đọc được bẫy hay dính, bé đang mắc, số phút, và NGUYÊN VĂN bài "
         "viết kèm lời chấm AI. ⚠ Riêng báo cáo cá nhân của bé còn thiếu môn "
         "Tiếng Anh ở hai cột."),
    ]:
        w5.append([k, v])
    don(w5)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    n_du = sum(1 for h in HANH_DONG if h[2] == DU)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   {len(HANH_DONG)} hành động · {n_du} vào được engine")
    print(f"   {len(TRUONG)} trường đối chiếu · {len(ADAPTIVE)} cơ chế adaptive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
