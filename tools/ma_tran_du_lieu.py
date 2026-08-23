#!/usr/bin/env python3
"""MA TRẬN DỮ LIỆU + ENGINE ĐANG CHẠY THẾ NÀO → docs/ma_tran_du_lieu.xlsx

    tools/tts/.venv/bin/python tools/ma_tran_du_lieu.py

Bác hỏi 23-08-2026: ma trận chi tiết DỮ LIỆU NÀO được ghi, CÁCH THỨC ghi, TẦN
SUẤT ghi; và cho thấy engine đang hoạt động thế nào, adaptive thể hiện ra sao ở
từng chức năng người dùng.

── ⚠ TRANG "ENGINE CHẠY THẬT" KHÔNG PHẢI SƠ ĐỒ ──
Nó là ĐẦU RA của `tools/chay_thu_engine.mjs`, tệp ấy `import` thẳng
`functions/src/bkt.js` · `lib/zpd.js` · `lib/chinhsach.js` · `lib/lantruyen.js` ·
`lib/onlai.js` — đúng những tệp máy chủ và máy con đang chạy. Sai công thức thì
số trong bảng sai theo. Sơ đồ thì không có tính chất ấy.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/ma_tran_du_lieu.xlsx"

# ── ① MA TRẬN: DỮ LIỆU · CÁCH GHI · TẦN SUẤT ────────────────────────────────
# (nhóm, trường, nghĩa, kho, cách ghi, TẦN SUẤT, ai đọc)
MA_TRAN = [
    # ── nhật ký từng lượt ──
    ("Lượt trả lời", "id", "mã bản ghi = uid+phiên+bài+câu+thứ tự",
     "attempts/{id}", "máy con dựng, `setDoc` có merge",
     "mỗi lượt · gửi theo LÔ cuối phiên", "hàm nền · cô giáo · bố mẹ"),
    ("Lượt trả lời", "learnerId · sessionId · microId", "ai · buổi nào · bài nào",
     "attempts/{id}", "máy con", "mỗi lượt", "cô giáo · bố mẹ"),
    ("Lượt trả lời", "bktUnit", "MÃ NÚT tri thức — biến 'xong bài' thành 'vững từ nào'",
     "attempts/{id}", "suy từ `cau.maNut` của chính câu",
     "mỗi lượt", "hàm nền BKT"),
    ("Lượt trả lời", "maNutDs", "mọi nút câu ấy chạm (để lan truyền chẩn đoán)",
     "attempts/{id}", "máy con", "mỗi lượt", "(dành cho mục 2.3.3)"),
    ("Lượt trả lời", "mauPrompt · phienBanMau · vanTayPrompt",
     "VÂN TAY của khung lời nhắc đã sinh ra lời chấm này",
     "attempts/{id}", "hàm nền `vantay.js` băm KHUNG → trả về máy con → ghi kèm lượt",
     "mỗi lượt CÓ AI CHẤM (bài viết · phòng nói), mới từ 23-08",
     "kiểm toán mục 2.5.2 · so ΔC giữa các mẫu nhắc"),
    ("Lượt trả lời", "phase", "practice · assess · check · worked",
     "attempts/{id}", "màn tự khai", "mỗi lượt", "hàm nền lọc theo đây"),
    ("Lượt trả lời", "mode", "dạng câu: chon · go · noiTu · noiCau · phongNoi …",
     "attempts/{id}", "từ `cau.format`", "mỗi lượt", "hồ sơ chiều Sư phạm"),
    ("Lượt trả lời", "correct", "đúng/sai", "attempts/{id}", "bộ chấm tại máy",
     "mỗi lượt", "hàm nền BKT"),
    ("Lượt trả lời", "tries", "lượt thứ mấy của CÙNG câu ấy",
     "attempts/{id}", "máy con đếm", "mỗi lượt", "cô giáo (cột 'bé đang mắc')"),
    ("Lượt trả lời", "hintsUsed", "H_req — đã THẤY mấy gợi ý",
     "attempts/{id}", "máy con đếm", "mỗi lượt", "hàm nền → `goiTrungBinh`"),
    ("Lượt trả lời", "ms", "RT — đo TRƯỚC khi đổi state",
     "attempts/{id}", "`Date.now()` hai mốc",
     "mỗi lượt · `null` ở bài viết và lượt nói", "hàm nền → `msTrungBinh`"),
    ("Lượt trả lời", "answer · expected", "bé chọn/nói gì · đáp án đúng là gì",
     "attempts/{id}", "máy con", "mỗi lượt", "cô giáo · chấm lại về sau"),
    ("Lượt trả lời", "ts · serverTs", "mốc máy con (ms) và mốc MÁY CHỦ",
     "attempts/{id}", "`serverTimestamp()`",
     "mỗi lượt", "mọi phép đếm theo cửa sổ ngày"),
    ("Lượt trả lời", "quyen · mon", "quyển nào · môn nào",
     "attempts/{id}", "máy con", "mỗi lượt", "lọc theo môn"),
    # ── mức thạo ──
    ("Mức thạo", "p", "P(L) — xác suất bé đã nắm nút này",
     "mastery/{uid}/units/{nút}", "HÀM NỀN `onAttempt` chạy BKT",
     "mỗi lần có bản ghi attempts mới", "Góc bố mẹ · ZPD · chính sách"),
    ("Mức thạo", "pTruoc", "P(L) TRƯỚC lượt ấy — để tính ΔC",
     "mastery/{uid}/units/{nút}", "hàm nền", "mỗi lượt", "đo hiệu quả bài LLM sinh"),
    ("Mức thạo", "mastered", "p ≥ θ chưa", "mastery/{uid}/units/{nút}", "hàm nền",
     "mỗi lượt", "chính sách vượt ải"),
    ("Mức thạo", "saiLienTiep", "struggle_count — sai liền mấy lần",
     "mastery/{uid}/units/{nút}", "hàm nền", "mỗi lượt", "chính sách phụ đạo"),
    ("Mức thạo", "nAttempts · nCorrect", "tổng số lượt · số lượt đúng",
     "mastery/{uid}/units/{nút}", "hàm nền cộng dồn", "mỗi lượt", "đường cong học tập"),
    ("Mức thạo", "msTong · msDem · msTrungBinh", "RT_avg tại nút này",
     "mastery/{uid}/units/{nút}", "hàm nền cộng dồn",
     "mỗi lượt CÓ đo được ms", "Góc bố mẹ"),
    ("Mức thạo", "goiTong · goiTrungBinh", "H_req trung bình tại nút này",
     "mastery/{uid}/units/{nút}", "hàm nền cộng dồn", "mỗi lượt", "Góc bố mẹ"),
    ("Mức thạo", "lastSeen · lastMicroId", "lần gần nhất chạm nút · ở bài nào",
     "mastery/{uid}/units/{nút}", "hàm nền", "mỗi lượt", "đường cong quên"),
    # ── tiến độ bài ──
    ("Tiến độ bài", "pass · score · total · bac", "đạt chưa · điểm cao nhất · bậc",
     "progressTA/{uid}/micros/{bài}", "máy con `luuBai`",
     "MỖI LẦN XONG MỘT BÀI", "sổ tiến độ · sinh thẻ ôn"),
    ("Tiến độ bài", "attempts · at", "làm bài mấy lần · lần gần nhất",
     "progressTA/{uid}/micros/{bài}", "máy con", "mỗi lần xong bài", "cô giáo"),
    # ── học bạ ──
    ("Học bạ", "loai=chuong", "kết quả kỳ ôn tập chương",
     "hocBaTA/{uid}/muc", "máy con `luuMucHocBa`", "mỗi lần xong một kỳ ôn",
     "bố mẹ · cô giáo · huy hiệu"),
    ("Học bạ", "loai=viet", "NGUYÊN VĂN bài bé viết + lời chấm AI",
     "hocBaTA/{uid}/muc", "máy con, ngay khi AI trả kết quả",
     "mỗi lần nộp bài viết", "bố mẹ · cô giáo"),
    ("Học bạ", "loai=doc", "kết quả bài đọc hiểu",
     "hocBaTA/{uid}/muc", "máy con", "mỗi lần xong một bài đọc (mới từ 23-08)",
     "bố mẹ · cô giáo"),
    ("Học bạ", "loai=hoSo", "bé làm tốt DẠNG câu nào (chiều Sư phạm)",
     "hocBaTA/{uid}/muc", "máy con cộng dồn",
     "mỗi lượt trả lời ĐẦU của một câu", "Góc bố mẹ · lời dặn LLM"),
    ("Học bạ", "loai=phien", "BỎ DỞ: chặng đang dở · số lượt · số giây (chiều Thời gian)",
     "hocBaTA/{uid}/muc", "máy con phát lúc GỠ MÀN bài học",
     "mỗi lần rời màn khi chưa xong — KHÔNG gộp theo bài (mới từ 23-08)",
     "bố mẹ · phân tích mệt mỏi nhận thức"),
    ("Học bạ", "loai=soThich", "từ bé thích nhất trong quyển (chiều Động lực)",
     "hocBaTA/{uid}/muc", "máy con", "mỗi lần bé chọn", "cô giáo máy lấy làm ngữ cảnh"),
    # ── thẻ ôn ──
    ("Thẻ ôn", "bac · henLai · lan", "hộp Leitner · ngày tới hạn",
     "reviewQueue/{uid}/cards/{thẻ}", "HÀM NỀN sinh khi `progressTA` được ghi; "
     "máy con cập nhật khi bé ôn xong",
     "sinh: mỗi lần xong bài · đẩy bậc: mỗi lần ôn một thẻ", "màn Ôn lại"),
    # ── phòng nói ──
    ("Phòng nói", "lichSu", "cả buổi: bé nói gì · cô sửa gì · điểm từng lượt",
     "phongNoiTA/{uid}/buoi/{buổi}", "máy con `luuBuoi`",
     "mỗi lượt nói (ghi đè cả buổi)", "CHỈ chính chủ + admin (riêng tư)"),
    # ── chỉ ở máy ──
    ("CHỈ Ở MÁY", "moc.daXem", "đã xem video nào",
     "localStorage", "máy con", "mỗi lần xem xong một video",
     "chỉ để bé vào lại đúng chỗ"),
    ("CHỈ Ở MÁY", "moc.daNghe", "đã nghe từ nào", "localStorage", "máy con",
     "mỗi lần bấm nghe", "như trên"),
    ("CHỈ Ở MÁY", "moc.soNoi", "điểm nói cao nhất + số lần, TỪNG TỪ",
     "localStorage", "máy con",
     "mỗi lượt nói", "thanh VIỆC CỦA CON — điểm này nay CÓ bản sao trong attempts"),
    ("CHỈ Ở MÁY", "hàng đợi `ttd5.queueTA.v1`", "lượt chưa đẩy được lên mạng",
     "localStorage", "máy con", "khi mạng hỏng — đẩy lại ở phiên sau",
     "không ai đọc, chỉ để không mất bản ghi"),
    ("CHỈ Ở MÁY", "sổ đã gửi `ttd5.daGuiTA.v1`", "mã những lượt ĐÃ lên máy chủ",
     "localStorage", "máy con", "sau mỗi lô gửi thành công",
     "chặn việc gửi lại bản ghi đã có — mới từ 23-08, xem nhịp ghi ở trang sau"),
]

# ── ② NHỊP GHI — vì sao gom lô ─────────────────────────────────────────────
NHIP = [
    ("Bé bấm một đáp án", "NGAY LẬP TỨC, tại máy",
     "`onLuot` → `ghiLuot` đẩy vào nhật ký trong bộ nhớ (`nhatKy.current.ds`). "
     "Chưa đụng mạng."),
    ("Bé làm xong một câu / rời màn", "gửi phần CHƯA GỬI lên `attempts`",
     "Mã bản ghi nhúng SỐ THỨ TỰ của lượt trong phiên, nên phải dựng lại từ CẢ "
     "nhật ký mới đánh số đúng — đẩy lẻ thì số thứ tự lúc nào cũng là 0 và mọi "
     "lượt của cùng một câu đè lên nhau.\n"
     "⚠ NHƯNG CHỈ GỬI PHẦN CHƯA LÊN. Bản trước gửi lại CẢ PHIÊN mỗi lượt, tin "
     "rằng 'mã cũ dựng lại ra đúng mã cũ nên ghi đè vô hại'. SAI: `attempts` là "
     "nhật ký BẤT BIẾN (`allow update: if false`), ghi đè là `update` và bị từ "
     "chối; mà `writeBatch` nguyên khối nên CẢ LÔ rơi. Hệ quả: mỗi phiên chỉ "
     "ĐÚNG MỘT lượt lên tới máy chủ, phần còn lại chết trong localStorage. Đo "
     "23-08-2026 bằng khoá quản trị: cả dự án có 2 bản ghi Tiếng Anh cho hai "
     "buổi ~10 lượt. Nay có sổ 'đã gửi' + thử lẻ khi lô hỏng; đo lại: 2 → 18."),
    ("Mỗi bản ghi `attempts` mới", "HÀM NỀN chạy trong ~1–3 giây",
     "`onAttempt` (Firestore trigger) đọc `bktUnit`, chạy BKT trong một giao dịch, "
     "ghi `mastery/{uid}/units/{nút}`. Bé không phải chờ."),
    ("Xong một bài", "ghi `progressTA` ngay",
     "Việc ghi ấy KÍCH HOẠT `onMicroDoneTA` → sinh thẻ ôn +1/+3/+7 ngày."),
    ("Mất mạng", "nằm lại hàng đợi tại máy",
     "`LOI_GHI` đếm số lần bị từ chối — KHÔNG nuốt im. Phiên sau đẩy lại."),
    ("Bé mở Góc bố mẹ", "đọc `mastery/` một lần lúc mở màn",
     "Không nghe realtime — vào lại màn mới thấy số mới."),
]

# ── ③ ADAPTIVE ↔ CHỨC NĂNG NGƯỜI DÙNG ──────────────────────────────────────
ADAPTIVE = [
    ("BKT cập nhật P(L)", "mọi màn có câu hỏi",
     "Bé không thấy trực tiếp. Nhưng nó là đầu vào của MỌI thứ dưới đây.",
     "Góc bố mẹ: 'con đang mắc ở đâu' + phần trăm nắm từng nút"),
    ("ZPD xếp lại thứ tự câu", "chặng Luyện tập",
     "Câu bé GẦN LÀM ĐƯỢC hiện trước; câu đã thạo đẩy xuống cuối; câu quá khó "
     "không dồn lên đầu.",
     "Bé thấy: bài luyện 'vừa sức', không nhàm cũng không nản"),
    ("Chính sách π · phụ đạo", "chặng Luyện tập",
     "Sai 3 lần liên tiếp tại một nút → chuyển sang câu dễ hơn cùng nút, hoặc "
     "LLM sinh câu vá.",
     "Bé thấy: 'cô cho con làm lại kiểu khác nhé'"),
    ("Chính sách π · vượt ải", "cuối bài",
     "Đạt bài + đủ 3 nút + MỌI nút đều ≥ θ → cho nhảy tiếp.",
     "Bé thấy: được đi thẳng, không phải luyện lại thứ đã vững"),
    ("Đường cong quên", "thẻ ôn",
     "Không dùng thì P(L) tụt theo hàm mũ, nửa đời 14 ngày.",
     "Bé thấy: thẻ ôn màu vàng mời quay lại đúng thứ sắp quên"),
    ("Lặp lại ngắt quãng", "màn Ôn lại",
     "Đúng thì giãn ra (1→3→7→14→30 ngày); sai thì về bậc đầu.",
     "Bé thấy: thẻ tới hạn xuất hiện trên trang chính"),
    ("Lan truyền chẩn đoán", "Góc bố mẹ",
     "Bé sai ở ngọn → lần ngược theo cạnh tiên quyết tìm nút GỐC yếu.",
     "Bố mẹ thấy: 'Gốc đáng ngờ: football — quả bóng đá (cách 2 bước, nắm 12%)'"),
    ("Hồ sơ dạng câu (chiều P)", "Góc bố mẹ + lời dặn LLM",
     "Đếm tỉ lệ đúng theo TỪNG DẠNG câu, chỉ tính lượt trả lời ĐẦU.",
     "Bố mẹ thấy: 'DẠNG CÂU CON LÀM TỐT NHẤT — chọn đáp án, đúng 50% (8 câu)'"),
    ("Sở thích (chiều M)", "phòng luyện nói",
     "Bé chọn từ mình thích → cô giáo máy lấy làm ngữ cảnh buổi sau.",
     "Bé thấy: cô nhắc lại đúng thứ mình thích"),
    ("Tầng hậu kiểm LLM", "bài viết · phòng nói",
     "Mọi câu mô hình sinh ra bị soi lại theo vốn từ của bài; câu dùng từ lạ bị "
     "BỎ trước khi tới mắt bé.",
     "Bé thấy: 'Cô có 1 câu gợi ý dùng từ con chưa học, nên cô giấu đi rồi.'"),
    ("Đường lui khi không có micro", "chặng Từ mới",
     "Thích ứng theo ĐIỀU KIỆN của bé, không theo điểm.",
     "Bé thấy: 'Con chưa nói được — cho con đi tiếp nhé'"),
]


def main() -> int:
    kq = subprocess.run(
        ["node", str(GOC / "tools/chay_thu_engine.mjs"), "--json"],
        capture_output=True, text=True, cwd=GOC,
    )
    if kq.returncode != 0:
        print("✗ chạy thử engine hỏng:\n" + kq.stderr[-800:], file=sys.stderr)
        return 1
    engine = json.loads(kq.stdout)

    wb = Workbook()
    dam = Font(bold=True, color="FFFFFF")
    nen = PatternFill("solid", fgColor="2F4A6B")
    vang = PatternFill("solid", fgColor="FFF3CD")
    xam = PatternFill("solid", fgColor="EEF1F5")
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
    ws.title = "Ma trận dữ liệu"
    bang(ws, ["Nhóm", "Trường", "Nghĩa", "Kho", "Cách ghi", "TẦN SUẤT", "Ai đọc"],
         (14, 26, 40, 26, 40, 34, 32))
    for m in MA_TRAN:
        ws.append(list(m))
        if m[0] == "CHỈ Ở MÁY":
            for c in ws[ws.max_row]:
                c.fill = vang
    don(ws)

    w2 = wb.create_sheet("Nhịp ghi")
    bang(w2, ["Lúc nào", "Ghi gì, ở đâu", "Vì sao làm thế"], (32, 34, 92))
    for n in NHIP:
        w2.append(list(n))
    don(w2)

    w3 = wb.create_sheet("Engine chạy thật")
    w3.append(["ĐẦU RA CỦA `node tools/chay_thu_engine.mjs` — chạy bằng CHÍNH mã "
               "engine đang chạy thật, không phải sơ đồ."])
    w3["A1"].font = Font(bold=True, color="FFFFFF")
    w3["A1"].fill = nen
    for c, r in zip("ABCDEFGHIJ", (40, 16, 14, 14, 14, 14, 14, 14, 16, 16)):
        w3.column_dimensions[c].width = r
    for c in engine["canh"]:
        w3.append([])
        w3.append([c["ten"]])
        for cc in w3[w3.max_row]:
            cc.fill = xam
        w3.cell(w3.max_row, 1).font = Font(bold=True)
        dong = c["dong"]
        if not dong:
            continue
        khoa = list(dong[0].keys())
        w3.append(khoa)
        for cc in w3[w3.max_row][:len(khoa)]:
            cc.font = Font(bold=True, color="2F4A6B")
        for d in dong:
            w3.append([d.get(k) for k in khoa])
    for r in w3.iter_rows(min_row=1):
        for cc in r:
            cc.alignment = tren
    w3.freeze_panes = "A2"

    w4 = wb.create_sheet("Adaptive ↔ người dùng")
    bang(w4, ["Cơ chế", "Ở chức năng nào", "Máy làm gì", "NGƯỜI DÙNG THẤY GÌ"],
         (28, 26, 60, 60))
    for a in ADAPTIVE:
        w4.append(list(a))
    don(w4)

    w5 = wb.create_sheet("Đường đi một lượt")
    bang(w5, ["Bước", "Ở đâu", "Chuyện gì xảy ra"], (6, 26, 96))
    for i, (o, x) in enumerate([
        ("máy con · CauHoi", "Bé bấm đáp án. `chamTiengAnh` chấm ngay, đo `ms` TRƯỚC "
         "khi đổi state, đếm số gợi ý bé đã thấy."),
        ("máy con · BaiHoc/DocHieu/…", "Bọc thêm `maPhien` · `microId` · `phase` rồi "
         "gọi `onLuot`."),
        ("máy con · ManTiengAnh", "`ghiLuot` nhét lượt vào nhật ký phiên, cộng ngay "
         "vào hồ sơ 'dạng câu bé làm tốt' (chỉ lượt ĐẦU)."),
        ("máy con · duLieu.js", "`luuSuKien` dựng lại CẢ PHIÊN thành các bản ghi có "
         "mã ổn định rồi đẩy lên `attempts`. Hỏng mạng thì nằm hàng đợi."),
        ("máy chủ · onAttempt", "Trigger Firestore. Lọc theo `phase`, đọc `bktUnit`, "
         "chạy BKT trong giao dịch, ghi `mastery/{uid}/units/{nút}`."),
        ("máy chủ · onMicroDoneTA", "Nếu là lần ghi `progressTA` (xong bài) thì sinh "
         "thẻ ôn +1/+3/+7 ngày."),
        ("máy con · lần mở màn sau", "`docMucThao` đọc `mastery/` → ZPD xếp lại câu, "
         "chính sách chọn việc tiếp, Góc bố mẹ vẽ ma trận."),
        ("máy chủ · nightlyTeacherBoard", "Dựng sẵn bảng cô giáo từ `attempts` + "
         "`progressTA` + `hocBaTA` của cả lớp."),
    ], 1):
        w5.append([i, o, x])
    don(w5)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}")
    print(f"   {len(MA_TRAN)} trường dữ liệu · {len(engine['canh'])} cảnh engine "
          f"· {len(ADAPTIVE)} cơ chế adaptive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
