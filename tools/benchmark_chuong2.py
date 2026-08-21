#!/usr/bin/env python3
"""ĐỐI CHIẾU CHƯƠNG 2 LUẬN VĂN ↔ HỆ THỐNG THẬT → docs/benchmark_chuong2.xlsx

    tools/tts/.venv/bin/python tools/benchmark_chuong2.py

Nguồn yêu cầu: `docs/Chuong2_Luan_van_Thac_sy_1_v3.docx`.
Phạm vi soi:   MÔN TIẾNG ANH, lớp 1 → lớp 5, dữ liệu và mã ở commit e60772c1.

── ĐỌC CỘT "BẰNG CHỨNG" TRƯỚC KHI TIN CỘT "TRẠNG THÁI" ──
Mỗi dòng đều dẫn tệp và con số đếm được. Không dòng nào chấm điểm bằng cảm nhận.

── BỐN TRẠNG THÁI, VÀ VÌ SAO KHÔNG PHẢI BA ──
Bác hỏi ba nhóm: đáp ứng · chưa đáp ứng · không thể đáp ứng. Nhưng gộp thật thì
mất mát nhiều nhất ở nhóm giữa: có những mục đã làm ĐÚNG MỘT NỬA — thuật toán
viết xong và chạy được, chỉ chưa nối vào môn Tiếng Anh. Xếp nó vào "chưa đáp
ứng" thì phần việc đã xong biến mất khỏi bảng; xếp vào "đáp ứng" thì bảng nói
dối. Nên tách riêng nhóm MỘT PHẦN.

── ⚠ MỘT DÒNG BẢN TRƯỚC CHẤM SAI, ĐÃ SỬA ──
Bản đầu ghi `tense` và `sentence_type` là 0/148 → xếp MỘT PHẦN. Sai ở chỗ soi
nhầm tầng: đúng là hai trường ấy trống trên nút thô của `ban_do_tieng_anh.json`,
NHƯNG tầng bản chuẩn — thứ mà bộ sinh bài thật sự dùng — có `thi` và `kieu_cau`
đủ 163/164 mẫu câu cả 5 quyển. Nay xếp ĐÁP ỨNG, và cột cách làm chỉ còn việc
ghi ngược lên nút thô cho khớp chữ nghĩa luận văn.

── BA PHÁT HIỆN LÀM ĐỔI HẲN LỘ TRÌNH (soi ngày 21-08) ──
 1. `chuan_lopN.json` GIỮ NGUYÊN mã nút đồ thị: `ma: "v_g5_u1_city"` ·
    `ma: "sp_g5_u1_1"`, đủ 740/740 từ. Bộ sinh bài đang cầm mã nút trong tay mà
    không ghi ra tệp bài. Nên "BKT theo từng nút" KHÔNG phải việc lớn như tưởng.
 2. Bản ghi lượt làm của TOÁN (`mon/toan/lib/sync.js:105`) đã có gần đủ những gì
    mục 2.5.2 đòi: `bktUnit` · `itemId` · `correct` · `tries` · `hintsUsed` ·
    `ms` · `answer` · `expected` · `mode` · `revealed` · `sessionId`. Tức là
    RT_avg và H_req không phải viết mới — chỉ là chưa bê sang Tiếng Anh.
 3. Bảng cô giáo ĐÃ đọc cả hai môn và ĐÃ đọc `attempts` không lọc theo môn
    (`functions/index.js:169`), kèm ghi chú "mã bài hai môn không bao giờ trùng".
    Nghĩa là Tiếng Anh ghi thẳng vào `attempts/` được, hàm nền BKT ăn ngay,
    KHÔNG phải sửa một dòng nào ở phía đọc.
"""
from __future__ import annotations

from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/benchmark_chuong2.xlsx"

DU, PH, CH, KO = "ĐÁP ỨNG", "MỘT PHẦN", "CHƯA ĐÁP ỨNG", "KHÔNG THỂ (như mô tả)"
# Nâng lên được không
OK = "✅ NÂNG ĐƯỢC"
GAN = "🟡 NÂNG ĐƯỢC PHẦN LỚN"
QUYET = "🔑 ĐƯỢC — nhưng cần bác quyết"
XONG = "— đã đạt"
KHONG = "⛔ KHÔNG nâng được"


def R(muc, yeu_cau, tt, bang_chung, con_thieu, nang, cach, phu, dot, cong):
    return (muc, yeu_cau, tt, bang_chung, con_thieu, nang, cach, phu, dot, cong)


D0 = "Đợt 0 · vá lặt vặt"
D1 = "Đợt 1 · ghi lượt làm"
D2 = "Đợt 2 · mô hình người học"
D3 = "Đợt 3 · đồ thị lúc chạy"
D4 = "Đợt 4 · điều hướng và đo"
DX = "—"

B = [
# ═══════════════════ 2.1.2 Mô hình thích ứng đa chiều ════════════════════
R("2.1.2", "Chiều NHẬN THỨC (C): đo mức tinh thông P(L) từng nút tri thức, xác định ZPD", CH,
  "Thuật toán BKT có thật ở `web/functions/src/bkt.js` (4 tham số, ngưỡng 0.85) nhưng "
  "hàm nền `onAttempt` chỉ lắng nghe collection `attempts/` của môn TOÁN "
  "(`functions/index.js:29`). Tiếng Anh ghi vào `progressTA/{uid}/micros` "
  "(`tienganh/lib/duLieu.js:30`) — không tài liệu nào rơi vào `attempts/`.",
  "Tiếng Anh không có P(L) cho bất kỳ nút nào. Sổ chỉ có mức BÀI: pass · best · "
  "attempts. Không có ZPD.",
  OK,
  "Là hệ quả TỰ ĐỘNG của Đợt 1 + Đợt 2 — không phải việc riêng. Khi màn Tiếng Anh "
  "ghi `attempts` kèm `bktUnit` mức nút, hàm `onAttempt` ghi thẳng `mastery/{uid}/"
  "units/{maNut}` mà không phải sửa gì. ZPD = lọc nút có 0.3 < P(L) < 0.85 rồi "
  "giao cho bộ chọn câu.",
  "2.3.2-nối · 2.3.1-overlay", D2, "≈2 ngày (phần lọc ZPD)"),

R("2.1.2", "Chiều THỜI GIAN (T): lặp lại ngắt quãng, đường cong quên, đo mệt mỏi nhận thức", CH,
  "Có bộ sinh thẻ ôn `onMicroDone` lịch +1/+3/+7 ngày (`index.js:43`), nhưng nó lắng "
  "nghe `progress/{uid}/micros` của TOÁN. Tiếng Anh có 4 kỳ ôn/quyển nhưng là ĐỀ CỐ "
  "ĐỊNH theo chương (`ta5/ontap.json`), không theo lịch quên của từng bé.",
  "Không có `T_last` mức nút, không có hàm phân rã, không đo thời gian phản hồi.",
  OK,
  "Ba bước: (1) đổi `onDocumentWritten` của `onMicroDone` thành hai trigger, thêm "
  "`progressTA/{learnerId}/micros` — hàm thân KHÔNG phải sửa, nó chỉ đọc `pass` và "
  "`microId`; (2) thêm hàm phân rã vào `bkt.js`: trước khi cập nhật thì nhân P(L) "
  "với hệ số theo số ngày kể từ `lastSeen` (`applyAttempt` đã lưu sẵn trường này); "
  "(3) mệt mỏi nhận thức suy từ `ms` — thời gian phản hồi dài dần trong một phiên.",
  "2.3.2-quên", D2, "≈2 ngày"),

R("2.1.2", "Chiều SƯ PHẠM (P): đo và thích ứng theo ĐỊNH DẠNG bài tập bé hợp nhất", CH,
  "Có 6 định dạng (chọn · điền · xếp thẻ · ghép chữ · nghe-nhìn · nói) xoay theo BẬC, "
  "nhưng xoay theo LUẬT CHUNG chứ không theo bé.",
  "Không có bản ghi 'bé này làm dạng nào tốt hơn'.",
  OK,
  "Rẻ bất ngờ vì `format` đã có sẵn trên từng câu. Đợt 1 ghi `format` vào bản ghi "
  "lượt làm (một dòng), rồi cộng tỉ lệ đúng theo từng `format` vào "
  "`hocBaTA/{uid}/hoSo`. Bộ chọn câu ưu tiên định dạng bé mạnh khi bé đang đuối, và "
  "định dạng bé yếu khi bé đang tốt.",
  "2.5.2-hành vi", D2, "≈1 ngày"),

R("2.1.2", "Chiều ĐỘNG LỰC (M): lồng ngữ cảnh theo SỞ THÍCH cá nhân", PH,
  "Phòng nói CÓ hỏi bé thích gì rồi truyền vào lời dặn LLM: `hoSo: { thich }` "
  "(`PhongNoi.jsx:208`) → `dongHoSo()` (`phongnoi.js:1213`) sinh câu 'The child told "
  "you they like …'. Bài tập cũng ưu tiên từ bé đã chọn (`phongnoi.js:263`).",
  "Sở thích chỉ sống trong MỘT phiên: `useState(null)` (`PhongNoi.jsx:95`), không lưu "
  "xuống sổ. Mở lại là hỏi lại từ đầu. Ba màn còn lại không dùng sở thích.",
  OK,
  "Việc nhỏ, làm được ngay, không phụ thuộc gì: (1) đổi `useState(null)` thành đọc "
  "từ `hocBaTA/{uid}/hoSo.thich`; (2) khi bé chọn thì `luuMucHocBa(uid,'hoSo',...)`; "
  "(3) truyền `hoSo` vào `loiDanCham()` của màn Viết và vào bộ chọn đề màn Đọc. "
  "⚠ Giữ nhánh `laTranh` không hỏi sở thích — bác đã chốt 19-08.",
  "—", D0, "nửa ngày"),

R("2.1.2", "Siêu vector trạng thái S = [C, T, P, M] làm ràng buộc cho LLM", CH,
  "Chỉ một mảnh của M (sở thích, một phiên) đi vào prompt.",
  "Ba chiều C · T · P chưa tồn tại nên không có gì để đóng gói.",
  OK,
  "Chỉ là việc GOM sau khi có đủ bốn chiều: thêm hàm `trangThaiBe(uid, maNut)` trả "
  "`{P_L, ngayQuen, dangManh, thich}`, rồi nhét vào `loiDan()` cạnh chỗ `dongHoSo()` "
  "đang đứng. Cấu trúc prompt không phải dựng lại.",
  "cả 4 chiều trên", D4, "≈1 ngày"),

# ═══════════════════════ 2.2.1 Đồ thị tri thức ═══════════════════════════
R("2.2.1", "Biểu diễn chương trình lớp 1–5 thành đồ thị G=(V,E)", DU,
  "`data/ban_do_tieng_anh.json` — 3 989 nút · 7 602 cạnh; riêng lớp 1–5 có 1 189 nút.",
  "—", XONG, "—", "—", DX, "—"),

R("2.2.1", "Tầng nút VĨ MÔ: Course · CEFR_Level · Unit · Theme", DU,
  "Đủ: `course` (12) · `unit` (176) · `theme` (38) · `program` (2). CEFR nằm ở thuộc "
  "tính `cefr_level` từng nút và `cefr` từng quyển (Pre-A1 ×3 · A1 ×2).",
  "CEFR là THUỘC TÍNH chứ không phải NÚT riêng như mô tả.",
  OK,
  "Đã đạt về chức năng. Nếu hội đồng soi đúng chữ 'nút CEFR_Level' thì thêm 6 nút "
  "`cefr_pre_a1`…`cefr_c2` và cạnh `HAS_LEVEL` sinh máy từ `cefr_level` sẵn có — "
  "một vòng lặp 10 dòng trong `chuan_tienganh.py`.",
  "—", D0, "30 phút"),

R("2.2.1", "Tầng nút HẠT NHÂN: Vocabulary · Sentence_Patterns · Pronunciation · Competences", DU,
  "Lớp 1–5: 680 nút từ vựng · 148 nút ngữ pháp · `pronunciation` (128) và `phonics` "
  "(95) · `skill_objective` (48) đóng vai Competences.", "—", XONG, "—", "—", DX, "—"),

R("2.2.1", "Cạnh CẤU THÀNH: isPartOf / contains", DU,
  "`CONTAINS` 3 336 · `HAS_UNIT` 192 · `HAS_VOCABULARY` 849 · `HAS_GRAMMAR` 85.",
  "—", XONG, "—", "—", DX, "—"),

R("2.2.1", "Cạnh NGỮ NGHĨA: hasFormula / hasTargetSlot", DU,
  "`grammar_form` đủ 148/148 nút ngữ pháp lớp 1–5 (vai trò hasFormula). `HAS_SLOT` "
  "827 cạnh; `target_vocab_slots` có ở 98/148 nút.",
  "50/148 nút ngữ pháp chưa khai ô đích.",
  OK,
  "Bù 50 nút còn thiếu. KHÔNG khai tay từ đầu: `cong_thuc` đã có dấu ngoặc vuông "
  "`[Class]` · `[place]` — viết một hàm rút tên ô từ công thức rồi đối chiếu với "
  "`vai` của từ trong unit, chỉ những chỗ máy không đoán được mới khai tay vào "
  "`lopN_bu.json`. Bên lớp 5 đã bù tay 21 mẫu theo đúng lối này.",
  "—", D0, "≈1 ngày"),

R("2.2.1", "Siêu dữ liệu nút TỪ VỰNG: id duy nhất · lexical_type · component_words", DU,
  "680/680 có `word` và `lexical_type`; 285/680 có `component_words` (đúng — chỉ CỤM "
  "mới có từ cấu thành); 660/680 có IPA; 661/680 có nghĩa tiếng Việt.",
  "19 nút thiếu nghĩa/IPA — phần lớn là TÊN RIÊNG (Ben · Mary · Ms Hoa), kho cố ý "
  "không dịch.", XONG, "—", "—", DX, "—"),

R("2.2.1", "Siêu dữ liệu nút NGỮ PHÁP: tense · sentence_type · formula", DU,
  "⚠ SỬA SO VỚI BẢN TRƯỚC. Bản đầu tôi soi nhầm tầng và báo 0/148. Đúng là hai "
  "trường ấy trống trên NÚT THÔ, nhưng ở tầng BẢN CHUẨN — thứ bộ sinh bài thật sự "
  "dùng — thì có đủ: `thi` 163/164 và `kieu_cau` 163/164 mẫu câu cả 5 quyển "
  "(`chuan_lop5.json`: present_simple 25 · past_simple 7 · future_simple 4 · "
  "future_be_going_to 2 · conditional_would 2; wh_question 32 · yes_no_question 6). "
  "`formula` (grammar_form) đủ 148/148.",
  "Một mẫu câu lớp 3 chưa khai. Và hai trường chưa được ghi NGƯỢC lên nút thô, nên "
  "ai đọc thẳng `ban_do_tieng_anh.json` sẽ tưởng là thiếu.",
  OK,
  "Hai việc nhỏ: (1) tìm mẫu câu lớp 3 còn trống rồi khai vào `lop3_bu.json`; "
  "(2) cho `chuan_tienganh.py` ghi ngược `thi`/`kieu_cau` lên nút đồ thị khi dựng, "
  "để bản đồ tự nó cũng đủ. ⚠ KHÔNG sửa tay `ban_do_tieng_anh.json` — kho gốc.",
  "—", D0, "≈2 giờ"),

R("2.2.1", "Duyệt đồ thị (DFS/BFS) để CHẨN ĐOÁN lúc chạy", CH,
  "Không mã nào trong `web/src/` đọc `ban_do_tieng_anh.json`. Đồ thị chỉ dùng LÚC "
  "DỰNG (`tools/chuan_tienganh.py`); app đọc tệp bài phẳng đã sinh sẵn.",
  "Lúc chạy không có đồ thị để duyệt.",
  OK,
  "Xuất ĐỒ THỊ CON, không bê cả kho: viết `tools/xuat_do_thi_con.py` lấy 1 189 nút "
  "lớp 1–5 + 195 cạnh REQUIRES + 157 mối `thang`, bỏ hết trường không cần (example, "
  "ipa, nghĩa — bài học đã có rồi), ghi ra "
  "`web/public/content/tienganh/do_thi.json`. Ước dưới 200 KB, nạp một lần rồi giữ "
  "trong bộ nhớ. Thêm `lib/doThi.js` với `truoc(maNut)` · `sau(maNut)` · `duyetNguoc"
  "(maNut, sau)`. Nhớ cổng canh: mọi mã nút trong tệp bài phải có mặt trong đồ thị.",
  "—", D3, "≈2 ngày"),

R("2.2.1", "Đồ thị làm bộ truy xuất (Retriever) cho RAG", PH,
  "Ràng buộc từ vựng cho LLM CÓ THẬT và chặt: `vonTu()` gom vốn tích luỹ tới đúng "
  "unit (`phongnoi.js:148`), `loiDan()` ép 'CHỈ dùng từ trong danh sách' (`:177`).",
  "Nguồn truy xuất là TỆP BÀI ĐÃ SINH, không phải đồ thị. Kết quả tương đương về "
  "phạm vi từ vựng, nhưng không lấy được đồ thị con theo quan hệ.",
  OK,
  "Sau khi có `doThi.js`: đổi ruột `vonTu()` từ 'gom mọi unit số nhỏ hơn' sang "
  "'duyệt ngược theo REQUIRES từ nút của bài này'. ⚠ ĐỔI RUỘT, GIỮ NGUYÊN HÌNH "
  "DẠNG TRẢ VỀ — `cauHopLe()` và `loiVietHopLe()` đang ăn kết quả của nó, đổi hình "
  "dạng là gãy cả tầng chống ảo giác. Chạy đối chiếu hai lối trên cả 94 unit trước "
  "khi bỏ lối cũ: lối mới mà cho vốn HẸP hơn là cô giáo máy cụt từ.",
  "2.2.1-duyệt", D3, "≈1 ngày"),

# ═══════════════════ 2.2.2 Ràng buộc tiên quyết ══════════════════════════
R("2.2.2", "Thuộc tính `prerequisite_links` trên nút", PH,
  "92 nút lớp 1–5 có `prerequisite_links`, trong đó 82/148 nút NGỮ PHÁP.",
  "0/680 nút TỪ VỰNG có thuộc tính này — trong khi luận văn nêu đích danh chuỗi số "
  "đếm `v_g2_u13_eleven` → `v_g1_u9_numbers` ở mục 2.2.2c.",
  OK,
  "Sinh MÁY chứ không khai tay 680 nút: từ vựng đã có `nhom_nghia` và `vai` "
  "(`so_dem` · `mau` · `thang` · `thu`…). Với mỗi nhóm có THỨ TỰ TỰ NHIÊN, nối nút "
  "sau ← nút trước theo thứ tự ấy. Đúng ví dụ luận văn nêu. Những nhóm không có thứ "
  "tự (đồ vật · con vật) thì KHÔNG nối — nối bừa là đặt mìn cho lan truyền chẩn "
  "đoán ở mục 2.3.3.",
  "—", D0, "≈1 ngày"),

R("2.2.2", "Cạnh REQUIRES có hướng trong đồ thị", DU,
  "583 cạnh `REQUIRES` toàn bản đồ; 195 cạnh chạm lớp 1–5.", "—", XONG, "—", "—", DX, "—"),

R("2.2.2", "Ràng buộc XUYÊN LỚP (cross-grade dependencies)", DU,
  "38 cạnh REQUIRES nối hai lớp khác nhau, có cờ `cross_grade: true` kèm lý do tiếng "
  "Việt. Ví dụ thật: `sp_g5_u1_1` (lớp 5) → `sp_g4_self_intro` (lớp 4).",
  "—", XONG, "—", "—", DX, "—"),

R("2.2.2", "Thang tiên quyết đi được vào tầng dữ liệu app dùng", PH,
  "`chuan_lopN.json` có mảng `thang` (10 · 10 · 39 · 64 · 34 mối cho lớp 1→5), tổng "
  "157 mối.",
  "`chuan_lopN.json` nằm ở `data/`, KHÔNG được đẩy sang `web/public/`. App không đọc "
  "`thang` ở bất kỳ đâu.",
  OK,
  "Đi kèm `do_thi.json` của Đợt 3 — `thang` gộp thẳng vào đó làm cạnh REQUIRES, "
  "không cần tệp riêng.",
  "2.2.1-duyệt", D3, "nửa ngày"),

R("2.2.2", "Lan truyền chẩn đoán NGƯỢC để tìm nút gốc rễ", CH,
  "Không có mã nào thực hiện.", "Toàn bộ cơ chế.",
  OK,
  "Sau khi có P(L) mức nút và `doThi.js`: hàm `goc(maNut, nguong)` duyệt ngược theo "
  "REQUIRES, tại mỗi bước nhân độ ngờ với hệ số suy giảm α, dừng khi gặp nút có "
  "P(L) thấp nhất trong chuỗi. ⚠ Nhớ chặn vòng lặp — 195 cạnh mà lỡ có chu trình là "
  "treo máy bé. Cổng: dựng một bé giả sai đúng một nút gốc rồi kiểm hàm có tìm ra.",
  "2.3.2-nối · 2.2.1-duyệt", D3, "≈2 ngày"),

# ═══════════════════ 2.3.1 Bản sao số người học ══════════════════════════
R("2.3.1", "Mô hình che phủ (Overlay) trạng thái lên từng nút đồ thị", CH,
  "Sổ của bé khoá theo MÃ BÀI (`DL:TA5.B01`), không theo mã nút (`v_g5_u1_dolphin`). "
  "`progressTA/{uid}/micros` lưu: pass · score · total · bac · attempts · at "
  "(`duLieu.js:67`).",
  "Không có lớp phủ mức nút.",
  OK,
  "RẺ HƠN TƯỞNG — đây là phát hiện quan trọng nhất của lần soi này. Không phải đổi "
  "khoá sổ hiện có (việc lớn, đụng cả 4 màn). `chuan_lopN.json` ĐÃ GIỮ mã nút đồ "
  "thị: `ma: \"v_g5_u1_city\"` đủ 740/740 từ và `ma: \"sp_g5_u1_1\"` cho mẫu câu. Bộ "
  "sinh bài đang cầm mã ấy trong tay mà không ghi ra. Nên chỉ cần: (1) "
  "`sinh_bai_tienganh.py` gắn `maNut: [...]` vào từng câu luyện; (2) dựng lại 5 "
  "quyển; (3) lớp phủ chính là `mastery/{uid}/units/{maNut}` mà `onAttempt` tự ghi. "
  "Sổ cũ theo bài GIỮ NGUYÊN — hai sổ song song, không đụng nhau.",
  "—", D1, "≈2 ngày (gồm dựng lại 5 quyển)"),

R("2.3.1", "`p_learned` — xác suất nắm vững từng nút", CH,
  "Không tồn tại cho Tiếng Anh (xem 2.1.2-C).", "Toàn bộ.",
  OK, "Không phải viết gì thêm: `applyAttempt()` (`bkt.js:53`) đã tính và ghi sẵn. "
  "Là quà kèm của Đợt 1.", "2.3.1-overlay", D1, "0 (kèm theo)"),

R("2.3.1", "`struggle_count` — đếm số lần sai LIÊN TIẾP tại một nút", PH,
  "Có `attempts` (số lần LÀM BÀI) ở `progress.js:57`, và phòng nói có cờ `haDoKho` "
  "hạ độ khi bé đuối.",
  "`attempts` đếm số lượt làm CẢ BÀI, không phải số lần sai liên tiếp tại một nút — "
  "hai đại lượng khác hẳn nhau.",
  OK,
  "Cộng vào chính chỗ `applyAttempt` đang ghi: `sai_lien_tiep = correct ? 0 : "
  "sai_lien_tiep + 1`. Một dòng, và nó đếm đúng mức NÚT vì tài liệu đã khoá theo "
  "nút.", "2.3.1-overlay", D1, "1 giờ"),

R("2.3.1", "`last_interacted` — dấu thời gian lần gần nhất", PH,
  "Có `at` (ISO) và `serverTs` (`duLieu.js:88`) — nhưng ở mức BÀI và mức MỤC HỌC BẠ.",
  "Không có ở mức nút; độ phân giải là lần làm bài chứ không phải mili-giây.",
  OK, "`applyAttempt()` đã ghi `lastSeen` mức nút sẵn. Quà kèm của Đợt 1.",
  "2.3.1-overlay", D1, "0 (kèm theo)"),

R("2.3.1", "`RT_avg` — thời gian phản hồi trung bình", CH,
  "Tìm `responseTime`/`RT` trong `web/src/mon/tienganh/` — không kết quả nào.",
  "Không đo giờ nào cả.",
  OK,
  "KHÔNG phải viết mới: bên Toán đã đo và ghi trường `ms` (`sync.js:115`, nguồn ở "
  "`PracticeItem.jsx`). Bê cùng lối sang `CauHoi.jsx`: `useRef(Date.now())` lúc câu "
  "hiện ra, hiệu số lúc bé bấm. ⚠ Trừ lúc bé nghe clip tiếng — câu `nhinNghe` bắt "
  "buộc nghe hết mới trả lời được, tính cả thời gian ấy là RT của mọi bé lớp 1 đều "
  "'chậm'.",
  "2.5.2-hành vi", D1, "nửa ngày"),

R("2.3.1", "`H_req` — số lần dùng trợ giúp", CH,
  "LẠI ĐÚNG MẪU CŨ: bên TOÁN đếm đủ và màn cô giáo hiện ra ('xem N gợi ý' — "
  "`HocSinhChiTiet.jsx:349`, nguồn `PracticeItem.jsx:47` → `sync.js:115`). Bên TIẾNG "
  "ANH gợi ý CÓ HIỆN cho bé (`CauHoi.jsx:270`, sau `HIEN_GOI_Y` lần thử) nhưng "
  "KHÔNG ĐẾM.",
  "Số lần bé mở gợi ý ở môn Tiếng Anh không được ghi lại ở đâu.",
  OK,
  "Việc nhỏ nhất trong cả bảng. Gợi ý bên Tiếng Anh hiện TỰ ĐỘNG theo số lần thử "
  "chứ không do bé bấm, nên `H_req` = số lần `goi` khác null. Cộng biến đếm ở "
  "`CauHoi.jsx:270` rồi gửi kèm lượt làm, đúng tên trường `hintsUsed` của Toán để "
  "màn cô giáo hiện được ngay mà không sửa gì.",
  "2.5.2-hành vi", D1, "1 giờ"),

R("2.3.1", "Hồ sơ bé: CEFR hiện tại · sở thích · định dạng ưa thích", PH,
  "CEFR khai mức QUYỂN (Pre-A1 / A1), không mức BÉ. Sở thích có nhưng chỉ sống trong "
  "một phiên phòng nói.",
  "Không hồ sơ bé nào lưu ba trường này.",
  OK,
  "Dựng `hocBaTA/{uid}/hoSo` giữ ba trường. Sở thích làm ở Đợt 0; CEFR suy từ quyển "
  "cao nhất bé đã đạt (đã có `cefr` từng quyển); định dạng ưa thích là kết quả Đợt "
  "2. ⚠ Nhớ deploy `firestore.rules` cho khoá mới — nếu không Firestore từ chối "
  "TRONG IM LẶNG, lỗi này đã dính thật một lần.",
  "2.1.2-M · 2.1.2-P", D2, "nửa ngày"),

# ══════════════════════════ 2.3.2 BKT ════════════════════════════════════
R("2.3.2", "Bốn tham số P(L₀) · P(T) · P(G) · P(S)", DU,
  "`bkt.js:13` — `{L0: 0.10, T: 0.08, slip: 0.10, guess: 0.30}`, hiệu chỉnh bằng "
  "thực nghiệm, có cổng riêng `test/bkt.test.mjs`. Còn có `paramsFor()` siết `guess` "
  "xuống 0.15 cho câu bẫy.", "—", XONG, "—", "—", DX, "—"),

R("2.3.2", "Công thức cập nhật Bayes sau mỗi câu trả lời", DU,
  "`bktUpdate()` (`bkt.js:17`) đúng công thức hậu nghiệm rồi cộng T. Có `bktSequence()` "
  "chạy cả chuỗi.", "—", XONG, "—", "—", DX, "—"),

R("2.3.2", "Ngưỡng tinh thông θ", PH,
  "`MASTERY_THRESHOLD = 0.85` ở cả `bkt.js:14` và `toan/lib/adaptive.js:13`.",
  "Luận văn viết θ = 0,95 (mục 2.5.1 và tài liệu [6]). Hệ thống chạy 0,85 — LỆCH so "
  "với mô tả.",
  QUYET,
  "Không phải việc kỹ thuật — sửa số là 5 phút, chọn số mới khó. HAI ĐƯỜNG: "
  "(a) sửa hệ thống về 0,95 → bé phải làm đúng nhiều hơn mới qua ải, hợp luận văn "
  "nhưng có thể làm bé lớp 1 nản; (b) giữ 0,85 và sửa luận văn, ghi rõ đây là con số "
  "HIỆU CHỈNH THEO THỰC NGHIỆM cho trẻ tiểu học Việt Nam — chính `bkt.js` đã ghi lý "
  "do: bộ tham số cũ tuyên thạo chỉ sau 2 câu, quá dễ dãi. Tôi nghiêng về (b): con "
  "số có lý do đo được thì mạnh hơn con số chép từ tài liệu.",
  "—", D0, "5 phút mã · phần khó là quyết"),

R("2.3.2", "BKT chạy cho môn TIẾNG ANH", CH,
  "Hàm nền nghe `attempts/{attemptId}`; Tiếng Anh không ghi vào đó (đã grep cả thư "
  "mục `mon/tienganh/`).",
  "Toàn bộ đường nối.",
  OK,
  "★ VIỆC THEN CHỐT — mở khoá nhiều dòng đỏ nhất trong bảng. Và RẺ hơn tưởng nhờ "
  "phát hiện: bảng cô giáo ĐÃ đọc `attempts` KHÔNG lọc theo môn "
  "(`functions/index.js:169`, kèm ghi chú 'mã bài hai môn không bao giờ trùng'). "
  "Nghĩa là Tiếng Anh ghi thẳng vào `attempts/` được, KHÔNG phải sửa một dòng nào ở "
  "phía đọc. Ba bước: (1) chép `mon/toan/lib/sync.js` sang "
  "`mon/tienganh/lib/suKien.js` — ⚠ PHẢI CHÉP, không được import: cổng `ranh_gioi` "
  "cấm hai môn dính nhau; (2) `CauHoi.jsx` gọi nó sau mỗi câu với `bktUnit` = mã nút "
  "(Đợt 1) và `microId` = mã bài; (3) luật `firestore.rules` cho `attempts` đã đòi "
  "đủ `['learnerId','microId','itemId','phase','correct','ts']` — ghi thiếu trường "
  "là bị từ chối TRONG IM LẶNG, nhớ đủ sáu.",
  "2.3.1-overlay", D1, "≈2 ngày"),

R("2.3.2", "Cơ chế QUÊN (forgetting) tích hợp vào BKT", CH,
  "`applyAttempt()` lưu `lastSeen` nhưng không dùng nó để giảm P(L) theo thời gian.",
  "Không có hàm phân rã.",
  OK,
  "Trong `bkt.js`, trước khi `bktUpdate`: `p = 0.5 + (p - 0.5) * exp(-λ * soNgay)` — "
  "kéo về phía 0,5 chứ không về 0, vì bé quên thì thành 'không chắc', không thành "
  "'chưa từng biết'. ⚠ Sửa `bkt.js` là ĐỤNG CẢ MÔN TOÁN đang chạy thật — chạy "
  "`test/bkt.test.mjs` và đối chiếu điểm thạo của vài bé trước/sau.",
  "2.3.2-nối", D2, "≈1 ngày"),

# ═══════════════ 2.3.3 Lan truyền trên đồ thị ════════════════════════════
R("2.3.3", "Lan truyền NGƯỢC kèm hệ số suy giảm α", CH, "Không có mã.", "Toàn bộ.",
  OK, "Là chính hàm `goc()` ở mục 2.2.2 — cùng một việc, không phải hai.",
  "2.2.2-lan truyền", D3, "kèm theo"),
R("2.3.3", "Lan truyền XUÔI kèm hệ số cộng hưởng β (vượt ải)", CH, "Không có mã.", "Toàn bộ.",
  OK,
  "Chiều ngược lại của cùng hàm duyệt: bé thạo nút A thì cộng β vào P(L) của các nút "
  "A là tiên quyết. ⚠ CHỈ CỘNG, ĐỪNG CHO VƯỢT NGƯỠNG: để β đẩy một nút lên thẳng "
  "'đã thạo' mà bé chưa từng làm câu nào của nút ấy là tuyên thạo khống.",
  "2.2.1-duyệt", D3, "≈1 ngày"),
R("2.3.3", "Ma trận trạng thái đồ thị định vị nút gốc rễ", CH, "Không có mã.", "Toàn bộ.",
  OK, "Là kết quả hiện ra của hai mục trên, cộng một màn cho cô giáo xem.",
  "2.3.3-ngược · 2.3.3-xuôi", D3, "≈1 ngày"),

# ═════════════════════════ 2.4 GenAI ═════════════════════════════════════
R("2.4.1", "LLM đóng vai gia sư (AI Agent)", DU,
  "Có thật, chạy trên bản deploy: `functions/src/luyennoi.js` (mô hình "
  "`openai/gpt-oss-120b`) cho phòng luyện nói, `chamviet.js` cho chấm bài viết. Gọi "
  "qua `onCall` (`functions/index.js:469, 492`).", "—", XONG, "—", "—", DX, "—"),

R("2.4.1", "Cá nhân hoá NỘI DUNG trên quy mô lớn (LLM sinh bài tập)", PH,
  "LLM sinh LỜI THOẠI của cô giáo trong phòng nói theo thời gian thực, có bám sở "
  "thích bé.",
  "3 752 câu luyện tập và 470 câu sát hạch là SINH SẴN bằng Python lúc dựng, không "
  "phải LLM sinh lúc chạy. Bài tả tranh cũng soạn tay (cờ `\"tay\": true`).",
  GAN,
  "NÊN nâng có chọn lọc, ĐỪNG nâng toàn bộ. Cho LLM sinh BÀI PHỤ ĐẠO lúc chạy (Đợt "
  "4) — số lượng ít, đúng chỗ bé đang hổng, và tầng hậu kiểm `cauHopLe()` đã sẵn để "
  "gác. Nhưng ĐỪNG chuyển 3 752 câu chính sang LLM sinh lúc chạy: nội dung tĩnh nên "
  "74 cổng soi được TRƯỚC KHI tới tay bé, còn câu sinh lúc chạy thì không cổng nào "
  "đứng trước được. Đây là chỗ hệ thống CỐ Ý khác luận văn, và tôi cho là khác đúng "
  "— nên ghi vào luận văn như một lựa chọn có lý do, chứ không phải một thiếu sót.",
  "2.5.1-phụ đạo", D4, "≈3 ngày (phần phụ đạo)"),

R("2.4.1", "Phản hồi có giải thích (Explainable Feedback)", DU,
  "`chamviet.js:88` ép mô hình: 'Mỗi lỗi phải chỉ ra: câu bé viết sai, câu sửa lại "
  "cho đúng, và vì sao'. Kết quả lưu ở `hocBaTA` kèm `khen` · `soLoi` · `choBoMe` "
  "(`progress.js:219`).", "—", XONG, "—", "—", DX, "—"),

R("2.4.2", "Nhận diện và chặn 'Ảo giác từ vựng'", DU,
  "Chặn HAI TẦNG, mạnh hơn mô tả trong luận văn: (1) prompt giới hạn vốn từ; (2) SOI "
  "LẠI ĐẦU RA — `cauHopLe()` (`phongnoi.js:648`) và `loiVietHopLe()` (`:922`) bác câu "
  "có chữ ngoài vốn, `soiLoiCham()` lọc lời chấm và trả `boQua` để màn hình NÓI RA "
  "chứ không giấu.", "—", XONG, "—", "—", DX, "—"),

R("2.4.3", "RAG bước 1 — Truy xuất tri thức", PH,
  "Có truy xuất và có ground-truth, nhưng nguồn là tệp bài đã sinh chứ không phải đồ "
  "thị (xem 2.2.1).", "Truy xuất theo quan hệ đồ thị.",
  OK, "Cùng một việc với mục 2.2.1-Retriever.", "2.2.1-retriever", D3, "kèm theo"),

R("2.4.3", "RAG bước 2 — Tăng cường nhắc lệnh (Prompt Augmentation)", DU,
  "`loiDan()` đóng gói: vốn từ · mẫu câu · tên bé · lớp · việc cần làm · hồ sơ sở "
  "thích · kịch bản bài (`phongnoi.js:312`). `loiDanCham()` tương tự cho bài viết.",
  "—", XONG, "—", "—", DX, "—"),

R("2.4.3", "RAG bước 3 — Tạo sinh có kiểm soát, 'đảm bảo 100% không từ lạ'", KO,
  "Hệ thống đạt kết quả ấy, nhưng KHÔNG bằng cách luận văn mô tả. Prompt là lời dặn, "
  "không phải ràng buộc cứng — mô hình vẫn có thể vi phạm. Cái làm nên con số 100% "
  "là TẦNG SOI ĐẦU RA phía sau (`cauHopLe` · `loiVietHopLe` · `soiLoiCham`), và câu "
  "vi phạm thì bị BỎ.",
  "Không thể đảm bảo 100% CHỈ BẰNG prompt như câu chữ ở mục 2.4.3 bước 3.",
  KHONG,
  "Không nâng được vì không có gì để nâng — phần mềm đã làm ĐÚNG rồi, chỗ sai nằm ở "
  "câu chữ luận văn. Sửa mô tả thành 'sinh có kiểm soát + HẬU KIỂM BẮT BUỘC, câu vi "
  "phạm bị loại'. Đây là điểm MẠNH của hệ thống: nói đúng thì luận văn được lợi, vì "
  "hội đồng nào cũng biết prompt không ràng buộc cứng được mô hình.",
  "—", DX, "sửa luận văn, không sửa mã"),

# ═══════════════ 2.5 Điều hướng và đánh giá ══════════════════════════════
R("2.5.1", "Hàm chính sách π: S_u(t) → hành động sư phạm", PH,
  "Có luật điều hướng thật ở `tienganh/lib/dandat.js`: 'đi tiếp được khi đã ĐẠT hoặc "
  "đã THỬ THẬT ≥2 lần', dùng chung cho ba tầng (mở bài · mở chặng · bỏ qua câu). "
  "Phòng nói có nhánh `haDoKho`.",
  "Đầu vào là pass/attempts, KHÔNG phải vector S_u(t). Không có P(L) nên không có ba "
  "nhánh 0.6 / 0.95 như mô tả.",
  OK,
  "Thay ĐIỀU KIỆN chứ không thay CẤU TRÚC: `dandat.js` đã gom luật vào một chỗ, nên "
  "chỉ đổi `daThuDu()` thành hàm đọc P(L). ⚠ GIỮ NHÁNH 'đã thử ≥2 lần thì cho đi "
  "tiếp' làm lưới đỡ — bỏ nó đi là bé kẹt vĩnh viễn ở một nút khi BKT chấm sai. "
  "Cổng `dandat.test.mjs` đang canh, phải đảo chiều thử lại cả hai nhánh.",
  "2.3.2-nối", D4, "≈2 ngày"),

R("2.5.1", "Nhánh 'Tịnh tiến' khi 0.6 ≤ P(L) < 0.95", CH, "Không có P(L).", "Toàn bộ.",
  OK, "Một nhánh trong hàm chính sách ở dòng trên.", "2.5.1-chính sách", D4, "kèm theo"),

R("2.5.1", "Nhánh 'Vượt ải' khi P(L) ≥ 0.95", PH,
  "Có cơ chế vượt ải NHƯNG theo BẬC chứ không theo P(L): `startLevel()` "
  "(`toan/lib/adaptive.js:24`) cho bé giỏi bắt đầu thẳng từ `standard`/`challenge`. "
  "Bên Tiếng Anh, bài đã ĐẠT thì không bắt làm lại.",
  "Không theo ngưỡng xác suất.",
  OK,
  "Chép lối `startLevel()` sang Tiếng Anh, đổi đầu vào thành P(L). ⚠ Con số ngưỡng "
  "phải khớp quyết định ở mục 2.3.2-θ, đừng để hai chỗ hai số.",
  "2.5.1-chính sách · 2.3.2-θ", D4, "kèm theo"),

R("2.5.1", "Nhánh 'Can thiệp phụ đạo' truy vết nút gốc rễ rồi cho LLM vá", CH,
  "Có hạ độ khó trong phiên nói, nhưng không truy vết đồ thị và không sinh bài vá.",
  "Cơ chế truy vết và bài phụ đạo.",
  OK,
  "Việc NẶNG NHẤT bảng, và là đỉnh của cả lộ trình: (1) `goc()` tìm nút gốc rễ; "
  "(2) gọi LLM sinh 3–5 câu quanh đúng nút ấy, vốn từ lấy bằng Retriever; (3) đẩy "
  "qua `cauHopLe()` rồi mới cho bé thấy. ⚠ Phải có ĐƯỜNG LÙI khi LLM hỏng hoặc mất "
  "mạng — rơi về ngân hàng câu tĩnh của chính unit ấy. Bé đang học mà màn trắng vì "
  "gọi mạng thất bại là hỏng nặng hơn không có phụ đạo.",
  "2.3.3-ngược · 2.5.1-chính sách", D4, "≈4 ngày"),

R("2.5.2", "Lưu vết HƯỚNG SỰ KIỆN — chuỗi sự kiện bất biến", PH,
  "MỘT chỗ đã làm gần đúng: PHÒNG NÓI ghi mỗi buổi thành MỘT tài liệu riêng khoá "
  "theo mã buổi — `phongNoiTA/{uid}/buoi/{maBuoi}`, giữ nguyên từng lượt "
  "`{vai, chu, en, vi}` đúng thứ tự (`goiPhongNoi.js:167`). Buổi cũ không bị buổi "
  "mới đè.",
  "Ba màn còn lại thì ngược hẳn: `luuMucHocBa()` dùng `setDoc(merge)` trên khoá cố "
  "định `{loai}__{khoa}` (`duLieu.js:87`) — lần làm sau ĐÈ lần trước, đúng thứ "
  "event-sourcing sinh ra để tránh. `gopTienDo()` cũng lấy bản mới hơn thắng.",
  OK,
  "Nhân lối của phòng nói ra ba màn kia — mà chính là `attempts/` của Đợt 1: mỗi "
  "lượt một tài liệu, khoá tự sinh, không bao giờ đè. ⚠ GIỮ NGUYÊN sổ trạng thái "
  "hiện có bên cạnh, đừng thay bằng chuỗi sự kiện: màn hình cần biết 'bé đã đạt bài "
  "này chưa' trong một lần đọc, dựng lại từ chuỗi sự kiện mỗi lần mở app là chậm và "
  "tốn. Hai thứ song song, mỗi thứ một việc.",
  "2.3.2-nối", D1, "kèm theo"),

R("2.5.2", "Dữ liệu định danh & thời gian (mili-giây)", PH,
  "Phòng nói CÓ mã phiên thật (`maBuoi` làm tên tài liệu) kèm `at` (ISO) và "
  "`serverTs`. Ba màn kia chỉ có `at` mức bài.",
  "Không mã phiên ngoài phòng nói; độ phân giải là lần làm bài, không tới mili-giây.",
  OK,
  "Bản ghi của Toán đã có `sessionId` và `ts` mili-giây sẵn — chép sang là xong. "
  "⚠ Quy về mốc MÁY CHỦ khi tổng hợp: `functions/index.js:172` đã ghi rõ lý do — "
  "máy tính bảng đặt sai ngày thì chuỗi ngày học của bé nhảy loạn.",
  "2.3.2-nối", D1, "kèm theo"),

R("2.5.2", "Dữ liệu nhận thức: Node_ID · đúng/sai · câu trả lời THÔ", PH,
  "Hai màn có lưu nguyên văn bé làm: BÀI VIẾT giữ `viet: String(viet)` "
  "(`progress.js:224`), PHÒNG NÓI giữ trọn hội thoại từng lượt. Đủ để đọc ra bé sai "
  "chỗ nào.",
  "Câu trắc nghiệm / điền từ / xếp thẻ KHÔNG lưu bé đã chọn gì — chỉ lưu điểm tổng. "
  "Và khoá là mã BÀI chứ không phải mã NÚT.",
  OK,
  "Bản ghi của Toán đã có `answer` · `expected` · `mode` · `revealed` "
  "(`sync.js:118`), kèm ghi chú đúng lý do: 'hai con sai hai kiểu khác nhau cần hai "
  "cách giúp khác nhau'. Chép sang. ⚠ Ô NHẬP thì lưu nguyên văn bé gõ, đừng lưu bản "
  "đã chuẩn hoá — mất đúng cái cần xem.",
  "2.3.1-overlay · 2.3.2-nối", D1, "kèm theo"),

R("2.5.2", "Dữ liệu hành vi: thời gian phản hồi · số lần trợ giúp", CH, "Không đo.",
  "Toàn bộ.",
  OK, "Chính là hai mục 2.3.1-RT và 2.3.1-H_req. Cùng một lần sửa `CauHoi.jsx`.",
  "—", D1, "nửa ngày cho cả hai"),

R("2.5.2", "Bối cảnh hệ thống: P(L) trước/sau · mã prompt để kiểm toán", KO,
  "Không có P(L) (xem trên). Mã prompt thì KHÔNG THỂ lưu theo thiết kế hiện hành: "
  "máy chủ CỐ Ý không lưu gì — ghi rõ ở `goiPhongNoi.js:7` và `goiChamViet.js:9` "
  "('Máy chủ KHÔNG lưu gì (bác chốt)').",
  "Muốn kiểm toán prompt thì phải đổi chính quyết định ấy.",
  QUYET,
  "Tách làm hai, đừng gộp: NỬA P(L) trước/sau thì nâng được vô điều kiện — "
  "`bktUpdate` đang cầm cả hai giá trị trong tay, ghi thêm hai trường là xong, làm ở "
  "Đợt 2. NỬA MÃ PROMPT mới cần bác quyết. Có đường giữa đáng cân nhắc: lưu VÂN TAY "
  "prompt (mã băm + phiên bản mẫu) thay vì lưu nguyên văn — đủ để đối chiếu "
  "'phiên bản prompt nào cho ΔC cao hơn' mà không lưu thêm chữ nào về bé.",
  "2.3.2-nối", D2, "nửa ngày (nửa P(L))"),

R("2.5.3", "Giao thức A-R-A (Assess → Remediate → Assess)", CH, "Không có mã nào.",
  "Toàn bộ.",
  OK,
  "Sau khi có phụ đạo: gói ba bước thành một vòng — đo P(L) trước, cho bài vá, đo "
  "lại. ⚠ Lần đo SAU phải dùng câu KHÁC lần đo trước, nếu không đo trí nhớ ngắn hạn "
  "chứ không đo hiểu bài. Ngân hàng câu hiện có đủ để bốc hai bộ rời nhau.",
  "2.5.1-phụ đạo", D4, "≈2 ngày"),

R("2.5.3", "Chỉ số ΔC (Knowledge Gain) đánh giá hiệu quả bài LLM sinh", CH, "Không có.",
  "Toàn bộ.",
  OK, "Là phép trừ hai đầu của A-R-A, cộng một bảng gom theo mẫu prompt.",
  "2.5.3-ARA", D4, "≈1 ngày"),

R("2.5.3", "Tối ưu hoá prompt theo ΔC", KO,
  "Cần lưu prompt và lưu P(L) — cả hai vướng ràng buộc 'máy chủ không lưu gì'.",
  "Xem mục 2.5.2 dòng trên.",
  QUYET,
  "Nếu bác chọn đường VÂN TAY PROMPT ở mục 2.5.2 thì mục này nâng được đầy đủ mà "
  "không phải lưu thêm dữ liệu nào về bé: gom ΔC trung bình theo từng mã băm prompt, "
  "mẫu nào cho ΔC cao hơn thì giữ. Nếu bác giữ nguyên 'không lưu gì' thì mục này "
  "đóng, và luận văn nên ghi rõ đó là ranh giới RIÊNG TƯ tự đặt, không phải hạn chế "
  "kỹ thuật — đó là một lựa chọn đáng viết ra.",
  "2.5.2-bối cảnh · 2.5.3-ΔC", D4, "≈1 ngày nếu bác đồng ý"),

R("2.5.3", "Đường cong học tập (tỉ lệ lỗi theo số lần luyện)", CH,
  "Tìm `errorRate`/`duongCong` trong `web/src/` — không kết quả. Sổ bố mẹ hiện số bài "
  "xong, không vẽ đường cong.",
  "Toàn bộ.",
  OK,
  "MÓN DỄ NHẤT trong nhóm 2.5 và KHÔNG cần BKT: chỉ cần chuỗi sự kiện có `correct` + "
  "số thứ tự lần luyện, tức là có ngay sau Đợt 1. Gom theo (nút, lần thứ n) rồi vẽ "
  "tỉ lệ sai giảm dần. Đặt vào Sổ bố mẹ — đây là thứ bố mẹ nhìn ra tiến bộ rõ hơn "
  "mọi con số phần trăm.",
  "2.3.2-nối", D2, "≈1 ngày"),
]

TK_THEM = [
    ("Nội dung đã dựng xong (lớp 1→5)", ""),
    ("Quyển · unit", "5 quyển · 94 unit"),
    ("Từ vựng · mẫu câu", "740 từ · 164 mẫu câu"),
    ("Câu luyện tập · câu sát hạch", "3 752 · 470"),
    ("Bài tả tranh (đọc · viết · nói quanh 1 bức)", "62 bức, lớp 3·4·5"),
    ("Clip tiếng · video", "5 366 · 345"),
    ("Cổng tự động", "74 tệp, tất cả xanh"),
    ("", ""),
    ("Đồ thị tri thức", ""),
    ("Nút · cạnh (toàn bản đồ)", "3 989 · 7 602"),
    ("Nút thuộc lớp 1–5", "1 189"),
    ("Cạnh REQUIRES chạm lớp 1–5", "195 (38 xuyên lớp)"),
    ("Nút có prerequisite_links (lớp 1–5)", "92 / 1 189"),
    ("Mối tiên quyết đã vào bản chuẩn", "157 (10·10·39·64·34)"),
    ("Mã nút đồ thị giữ được ở bản chuẩn", "740/740 từ · 164/164 mẫu câu"),
    ("`thi` · `kieu_cau` ở bản chuẩn", "163/164 · 163/164"),
]

LO_TRINH = [
    (D0, "Vá lặt vặt — không phụ thuộc gì, làm được ngay tuần này",
     "Lưu sở thích xuống sổ · ghi ngược `thi`/`kieu_cau` lên nút · bù 50 ô đích · "
     "nối cạnh tiên quyết cho chuỗi từ vựng có thứ tự · (nếu bác chọn) đổi θ · "
     "(tuỳ) thêm 6 nút CEFR",
     "≈3 ngày", "nhích lên, trong đó 4 mục lên hẳn ĐÁP ỨNG",
     "Không đụng gì đang chạy. Riêng đổi θ thì ĐỤNG MÔN TOÁN — chạy lại "
     "`bkt.test.mjs` và đối chiếu điểm thạo vài bé trước/sau."),
    (D1, "★ GHI LƯỢT LÀM — việc then chốt, mở khoá nhiều nhất",
     "Gắn `maNut` vào từng câu luyện rồi dựng lại 5 quyển · chép `sync.js` sang "
     "`tienganh/lib/suKien.js` · `CauHoi.jsx` ghi `attempts` kèm `bktUnit` · đo `ms` "
     "và đếm `hintsUsed`",
     "≈4 ngày", "— BKT bắt đầu chạy cho Tiếng Anh, lưu vết sự kiện đầy đủ",
     "⚠ PHẢI CHÉP `sync.js` chứ không import — cổng `ranh_gioi` cấm hai môn dính "
     "nhau. ⚠ Luật `attempts` đòi đủ 6 trường, thiếu là Firestore từ chối TRONG IM "
     "LẶNG. ⚠ Dựng lại 5 quyển thì `cp` rồi `diff` trước khi tin — bốn bộ dựng đã "
     "từng đè mất bản sửa tay."),
    (D2, "Mô hình người học — P(L), quên, hồ sơ bé",
     "Lọc ZPD · nối `onMicroDone` sang `progressTA` · hàm phân rã theo ngày · hồ sơ "
     "`hocBaTA/{uid}/hoSo` · ghi P(L) trước/sau · đường cong học tập cho Sổ bố mẹ",
     "≈6 ngày", "— bốn chiều C·T·P·M đủ mặt",
     "⚠ Sửa `bkt.js` là đụng môn Toán đang chạy thật. ⚠ Khoá Firestore mới thì phải "
     "`deploy --only firestore:rules` TRƯỚC, không thì ghi bị từ chối im lặng."),
    (D3, "Đồ thị lúc chạy — chẩn đoán và truy xuất theo quan hệ",
     "Xuất `do_thi.json` (dưới 200 KB) · `lib/doThi.js` · lan truyền ngược α và xuôi "
     "β · đổi ruột Retriever · màn ma trận cho cô giáo",
     "≈7 ngày", "— RAG truy xuất đúng theo đồ thị, tìm được nút gốc rễ",
     "⚠ Đổi ruột `vonTu()` phải GIỮ NGUYÊN hình dạng trả về — `cauHopLe()` đang ăn "
     "kết quả của nó, đổi là gãy tầng chống ảo giác. Đối chiếu hai lối trên cả 94 "
     "unit trước khi bỏ lối cũ. ⚠ Chặn chu trình khi duyệt."),
    (D4, "Điều hướng và đo — chính sách theo P(L), phụ đạo, A-R-A",
     "Đổi điều kiện `dandat.js` sang P(L) · ba nhánh chính sách · phụ đạo do LLM "
     "sinh có hậu kiểm · A-R-A · ΔC · gom vector S",
     "≈12 ngày", "— vòng thích ứng khép kín",
     "⚠ GIỮ nhánh 'đã thử ≥2 lần thì cho đi tiếp' làm lưới đỡ, bỏ đi là bé kẹt vĩnh "
     "viễn khi BKT chấm sai. ⚠ Phụ đạo phải có đường lùi khi mất mạng."),
]


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

    wb = Workbook()
    vien = Border(*[Side(style="thin", color="C8D4E2")] * 4)
    MAU = {DU: "D6F0DC", PH: "FFF3D6", CH: "FBE0DC", KO: "E2DDF0"}
    MAU_N = {OK: "D6F0DC", GAN: "FFF3D6", QUYET: "FDE7C8", XONG: "EDF1F5",
             KHONG: "E2DDF0"}

    def dau(ws, cot, rong, cao=44):
        ws.append(cot)
        for i, _ in enumerate(cot, 1):
            o = ws.cell(row=1, column=i)
            o.font = Font(bold=True, color="FFFFFF", size=11)
            o.fill = PatternFill("solid", fgColor="0B4EA8")
            o.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = cao
        for c, w in rong.items():
            ws.column_dimensions[c].width = w

    # ── Sheet 1 · bảng đối chiếu ──
    ws = wb.active
    ws.title = "Đối chiếu"
    dau(ws, ["Mục", "YÊU CẦU trong luận văn", "TRẠNG THÁI NAY",
             "BẰNG CHỨNG trong hệ thống (tệp · số đếm)", "CÒN THIẾU GÌ",
             "NÂNG LÊN ĐÁP ỨNG ĐƯỢC KHÔNG?", "CÁCH LÀM — bước cụ thể, tệp cụ thể",
             "PHỤ THUỘC MỤC NÀO", "ĐỢT", "CÔNG ƯỚC LƯỢNG"],
        {"A": 8, "B": 46, "C": 16, "D": 62, "E": 40, "F": 22, "G": 82, "H": 22,
         "I": 20, "J": 18})
    for i, hang in enumerate(B, start=2):
        ws.append(list(hang))
        ws.cell(row=i, column=3).fill = PatternFill("solid", fgColor=MAU[hang[2]])
        ws.cell(row=i, column=3).font = Font(bold=True, size=10)
        ws.cell(row=i, column=6).fill = PatternFill("solid", fgColor=MAU_N[hang[5]])
        ws.cell(row=i, column=6).font = Font(bold=True, size=10)
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:J{len(B) + 1}"

    # ── Sheet 2 · lộ trình ──
    w2 = wb.create_sheet("Lộ trình")
    dau(w2, ["Đợt", "Làm gì", "Việc cụ thể", "Công", "Được gì",
             "⚠ CHỖ DỄ HỎNG"],
        {"A": 24, "B": 40, "C": 62, "D": 12, "E": 46, "F": 62})
    for d, lam, viec, cong, duoc, canh in LO_TRINH:
        # đếm bằng máy, đừng gõ tay: số mục mỗi đợt đổi theo bảng
        n = sum(1 for x in B if x[8] == d)
        w2.append([d, lam, viec, cong, f"{n} mục {duoc}", canh])
    tong = sum(1 for x in B if x[5] in (OK, GAN, QUYET))
    w2.append([])
    w2.append(["TỔNG", f"{tong}/{len(B)} mục nâng được",
               f"Trong đó {sum(1 for x in B if x[5] == OK)} nâng lên hẳn ĐÁP ỨNG · "
               f"{sum(1 for x in B if x[5] == GAN)} nâng được phần lớn · "
               f"{sum(1 for x in B if x[5] == QUYET)} chờ bác quyết",
               "≈32 ngày",
               f"{sum(1 for x in B if x[5] == XONG)} mục đã đạt sẵn · "
               f"{sum(1 for x in B if x[5] == KHONG)} mục sửa luận văn thay vì sửa mã",
               ""])
    for o in w2[w2.max_row]:
        o.font = Font(bold=True)
    for r in w2.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
            o.border = vien

    # ── Sheet 3 · tổng hợp ──
    w3 = wb.create_sheet("Tổng hợp")
    dem = {k: sum(1 for x in B if x[2] == k) for k in (DU, PH, CH, KO)}
    dau(w3, ["Trạng thái", "Số mục", "Tỉ lệ", "Nghĩa là gì"],
        {"A": 26, "B": 10, "C": 10, "D": 86})
    ngh = {
        DU: "Đã có, chạy thật, chỉ ra được bằng chứng trong mã hoặc dữ liệu.",
        PH: "Làm xong một nửa. Thường là: thuật toán CÓ nhưng chưa nối vào môn Tiếng "
            "Anh, hoặc dữ liệu CÓ nhưng app chưa đọc tới.",
        CH: "Chưa có, nhưng LÀM ĐƯỢC bằng kiến trúc hiện tại. Cột 'cách làm' nói rõ.",
        KO: "Không đạt được ĐÚNG NHƯ MÔ TẢ — hoặc vì mô tả tự nó không khả thi "
            "(prompt không thể đảm bảo 100%), hoặc vì vướng một quyết định đã chốt "
            "(máy chủ không lưu gì).",
    }
    for k in (DU, PH, CH, KO):
        w3.append([k, dem[k], f"{dem[k] / len(B) * 100:.0f}%", ngh[k]])
        w3.cell(row=w3.max_row, column=1).fill = PatternFill("solid", fgColor=MAU[k])
    w3.append(["TỔNG", len(B), "100%", ""])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True)

    w3.append([]); w3.append(["SAU KHI NÂNG CẤP THÌ RA SAO", "", "", ""])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True, size=12)
    dn = {k: sum(1 for x in B if x[5] == k) for k in (OK, GAN, QUYET, XONG, KHONG)}
    for k, y in [
        (XONG, "Đã đạt sẵn, không phải làm gì."),
        (OK, "Nâng lên ĐÁP ỨNG đầy đủ được. Cách làm ghi ở cột G."),
        (GAN, "Nâng được phần lớn, nhưng có phần CỐ Ý không nâng — xem cột G để rõ "
              "vì sao không nâng lại là đúng."),
        (QUYET, "Kỹ thuật làm được; vướng một quyết định của bác (θ · lưu prompt)."),
        (KHONG, "Không nâng được vì không có gì để nâng — phần mềm đã đúng, chỗ cần "
                "sửa nằm ở câu chữ luận văn."),
    ]:
        w3.append([k, dn[k], f"{dn[k] / len(B) * 100:.0f}%", y])
        w3.cell(row=w3.max_row, column=1).fill = PatternFill("solid", fgColor=MAU_N[k])
    w3.append(["", "", "", ""])
    w3.append(["Đích đến", f"{dn[XONG] + dn[OK]}/{len(B)}",
               f"{(dn[XONG] + dn[OK]) / len(B) * 100:.0f}%",
               "Số mục ở trạng thái ĐÁP ỨNG sau khi chạy hết 5 đợt, CHƯA tính 3 mục "
               "chờ bác quyết. Tính cả ba thì lên "
               f"{dn[XONG] + dn[OK] + dn[QUYET]}/{len(B)} "
               f"({(dn[XONG] + dn[OK] + dn[QUYET]) / len(B) * 100:.0f}%)."])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True)

    w3.append([]); w3.append(["THEO TỪNG MỤC CỦA CHƯƠNG 2", "", "", ""])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True, size=12)
    muc = {}
    for hang in B:
        muc.setdefault(hang[0], []).append(hang[2])
    for m in sorted(muc):
        ds = muc[m]
        w3.append([m, len(ds), "",
                   " · ".join(f"{k}: {sum(1 for x in ds if x == k)}"
                              for k in (DU, PH, CH, KO) if any(x == k for x in ds))])

    w3.append([]); w3.append(["CÔNG THEO ĐỢT", "", "", ""])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True, size=12)
    for d, lam, _, cong, _, _ in LO_TRINH:
        w3.append([d, cong, sum(1 for x in B if x[8] == d), lam])

    w3.append([]); w3.append(["SỐ LIỆU HIỆN TRẠNG", "", "", ""])
    w3.cell(row=w3.max_row, column=1).font = Font(bold=True, size=12)
    for a, b in TK_THEM:
        w3.append([a, b, "", ""])
    for r in w3.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)

    # ── Sheet 4 · đọc trước ──
    w4 = wb.create_sheet("Đọc trước")
    for a, b in [
        ("ĐỐI CHIẾU CHƯƠNG 2 ↔ HỆ THỐNG THẬT", ""),
        ("", ""),
        ("Nguồn yêu cầu", "docs/Chuong2_Luan_van_Thac_sy_1_v3.docx"),
        ("Phạm vi soi", "Môn Tiếng Anh, lớp 1 → lớp 5. Dữ liệu và mã ở commit "
                        "e60772c1 (đã deploy)."),
        ("Cách soi", "Mở tệp mã và dữ liệu ra đếm, không suy từ trí nhớ. Mỗi dòng "
                     "trong sheet Đối chiếu đều dẫn tệp và con số."),
        ("", ""),
        ("MỘT CÂU TÓM TẮT", ""),
        ("", "Tầng DỮ LIỆU (đồ thị tri thức, ràng buộc tiên quyết, siêu dữ liệu) và "
             "tầng NỘI DUNG (5 quyển đã dựng xong) đáp ứng tốt. Tầng AI có thật và "
             "phần chống ảo giác còn LÀM MẠNH HƠN mô tả. Chỗ hụt nằm gần như trọn "
             "vẹn ở tầng MÔ HÌNH NGƯỜI HỌC — và hụt vì MỘT nguyên nhân duy nhất: "
             "BKT viết xong rồi mà chưa nối vào môn Tiếng Anh."),
        ("", ""),
        ("BA PHÁT HIỆN LÀM LỘ TRÌNH RẺ ĐI NHIỀU", ""),
        ("1 · Mã nút đã có sẵn",
         "`chuan_lopN.json` giữ nguyên mã nút đồ thị — `ma: \"v_g5_u1_city\"`, đủ "
         "740/740 từ. Bộ sinh bài đang CẦM mã nút trong tay mà không ghi ra tệp bài. "
         "Nên 'BKT theo từng nút' không phải đổi khoá cả bốn màn như tôi tưởng lúc "
         "đầu, chỉ là thêm một trường rồi dựng lại."),
        ("2 · Bản ghi lượt làm đã có sẵn",
         "`mon/toan/lib/sync.js:105` đã ghi đủ `bktUnit` · `itemId` · `correct` · "
         "`tries` · `hintsUsed` · `ms` · `answer` · `expected` · `sessionId`. Tức là "
         "RT_avg và H_req của mục 2.3.1 không phải viết mới — chỉ chưa bê sang."),
        ("3 · Phía đọc đã sẵn sàng cho hai môn",
         "Bảng cô giáo đã đọc cả hai môn và đọc `attempts` KHÔNG lọc theo môn "
         "(`functions/index.js:169`). Nên Tiếng Anh ghi thẳng vào `attempts/` được, "
         "hàm nền BKT ăn ngay, không phải sửa một dòng nào ở phía đọc."),
        ("", ""),
        ("MỘT VIỆC ĐÁNG LÀM TRƯỚC NHẤT", ""),
        ("", "Đợt 1 — cho màn Tiếng Anh ghi `attempts` kèm mã nút. Một việc ấy mở "
             "khoá: chiều Nhận thức · chiều Thời gian · chiều Sư phạm · lưu vết "
             "hướng sự kiện · RT · H_req · struggle_count · đường cong học tập. "
             "Khoảng một phần ba số dòng đỏ phụ thuộc vào nó."),
        ("", ""),
        ("HAI CHỖ CẦN BÁC QUYẾT, KHÔNG PHẢI CHỖ KỸ THUẬT", ""),
        ("1 · Máy chủ có lưu prompt không?",
         "Hiện CỐ Ý không lưu gì ('Máy chủ KHÔNG lưu gì (bác chốt)'). Giữ nguyên thì "
         "mục 2.5.2 (kiểm toán prompt) và 2.5.3 (tối ưu prompt theo ΔC) đóng. Có "
         "ĐƯỜNG GIỮA: lưu VÂN TAY prompt (mã băm + phiên bản mẫu) thay vì nguyên "
         "văn — đủ để so 'mẫu nào dạy hiệu quả hơn' mà không lưu thêm chữ nào về bé. "
         "Tôi nghiêng về đường giữa này."),
        ("2 · Ngưỡng tinh thông θ",
         "Luận văn viết 0,95; hệ thống chạy 0,85 và con số ấy hiệu chỉnh bằng thực "
         "nghiệm (`bkt.js` ghi rõ: tham số cũ tuyên thạo chỉ sau 2 câu — quá dễ dãi "
         "với trẻ). Tôi nghiêng về giữ 0,85 và sửa luận văn kèm lý do: con số có "
         "phép đo đứng sau thì mạnh hơn con số chép từ tài liệu."),
        ("", ""),
        ("MỘT CHỖ LUẬN VĂN NÊN SỬA", ""),
        ("Mục 2.4.3 bước 3",
         "Luận văn viết 'Nhờ các giới hạn từ Bước 2, kết quả tạo sinh đảm bảo 100% "
         "không chứa từ vựng lạ'. Prompt là LỜI DẶN, không phải ràng buộc cứng — "
         "không đảm bảo được 100%. Hệ thống thật đạt điều đó nhờ một tầng nữa mà "
         "luận văn chưa nhắc: HẬU KIỂM đầu ra, câu nào vi phạm thì bỏ. Mô tả đúng "
         "thì luận văn mạnh hơn chứ không yếu đi."),
        ("", ""),
        ("MỘT DÒNG BẢN TRƯỚC TÔI CHẤM SAI", ""),
        ("Mục 2.2.1 · tense · sentence_type",
         "Bản đầu tôi báo 0/148 và xếp MỘT PHẦN. Sai vì soi nhầm tầng: hai trường ấy "
         "trống trên nút thô, nhưng ở tầng bản chuẩn — thứ bộ sinh bài thật sự dùng — "
         "có `thi` và `kieu_cau` đủ 163/164 mẫu câu. Nay xếp ĐÁP ỨNG."),
        ("", ""),
        ("CHỖ TÔI CHƯA SOI", ""),
        ("", "Bảng này soi MÃ và DỮ LIỆU. Nó không đo được: bé học có tiến bộ thật "
             "không, lời cô giáo máy nói có hay không, và 62 bức tranh có hợp mắt trẻ "
             "không. Ba câu ấy phải có người ngồi xem cùng bé. Cột 'công ước lượng' "
             "là ước lượng của tôi, chưa ai kiểm."),
    ]:
        w4.append([a, b])
    w4.column_dimensions["A"].width = 34
    w4.column_dimensions["B"].width = 104
    for row in w4.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    for r in range(1, w4.max_row + 1):
        v = w4.cell(row=r, column=1).value or ""
        if v and not w4.cell(row=r, column=2).value and v.isupper() is False:
            pass
        if v in ("ĐỐI CHIẾU CHƯƠNG 2 ↔ HỆ THỐNG THẬT", "MỘT CÂU TÓM TẮT",
                 "BA PHÁT HIỆN LÀM LỘ TRÌNH RẺ ĐI NHIỀU",
                 "MỘT VIỆC ĐÁNG LÀM TRƯỚC NHẤT",
                 "HAI CHỖ CẦN BÁC QUYẾT, KHÔNG PHẢI CHỖ KỸ THUẬT",
                 "MỘT CHỖ LUẬN VĂN NÊN SỬA", "MỘT DÒNG BẢN TRƯỚC TÔI CHẤM SAI",
                 "CHỖ TÔI CHƯA SOI"):
            w4.cell(row=r, column=1).font = Font(bold=True, size=12)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(B)} tiêu chí)")
    print("  ── trạng thái nay ──")
    for k in (DU, PH, CH, KO):
        print(f"     {k:24s} {dem[k]:2d}  ({dem[k] / len(B) * 100:3.0f}%)")
    print("  ── nâng cấp ──")
    for k in (XONG, OK, GAN, QUYET, KHONG):
        print(f"     {k:26s} {dn[k]:2d}")
    print(f"  ── đích đến: {dn[XONG] + dn[OK]}/{len(B)} đáp ứng "
          f"({(dn[XONG] + dn[OK]) / len(B) * 100:.0f}%), "
          f"tính cả 3 mục bác quyết thì {dn[XONG] + dn[OK] + dn[QUYET]}/{len(B)} "
          f"({(dn[XONG] + dn[OK] + dn[QUYET]) / len(B) * 100:.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
