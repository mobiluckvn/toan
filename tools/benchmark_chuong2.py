#!/usr/bin/env python3
"""ĐỐI CHIẾU CHƯƠNG 2 LUẬN VĂN ↔ HỆ THỐNG THẬT → docs/benchmark_chuong2.xlsx

    tools/tts/.venv/bin/python tools/benchmark_chuong2.py

Nguồn yêu cầu: `docs/Chuong2_Luan_van_Thac_sy_1_v3.docx`.
Phạm vi soi:   MÔN TIẾNG ANH, lớp 1 → lớp 5.
Cập nhật:      22-08-2026, sau khi chạy xong Đợt 0, Đợt 1 và Đợt 2.
               Cả ba đợt ĐÃ DEPLOY. Còn Đợt 3 và Đợt 4.

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
R("2.1.2", "Chiều NHẬN THỨC (C): đo mức tinh thông P(L) từng nút tri thức, xác định ZPD", DU,
  "✅ NỬA ĐẦU XONG Đợt 1: P(L) nay có thật cho từng nút Tiếng Anh — `onAttempt` ghi "
  "`mastery/{uid}/units/{maNut}` với `p` · `pTruoc` · `saiLienTiep` · `msTrungBinh` "
  "· `goiTrungBinh`.",
  "✅ NỬA SAU XONG Đợt 2 (22-08), ĐÃ DEPLOY. `lib/zpd.js` đọc P(L) ra và xếp lại "
  "pool câu; `BaiHoc` gọi trong `useMemo`.",
  OK,
  "Bốn nhóm: chông chênh (0.3≤p<0.85) → chưa biết → yếu hẳn → đã thạo. "
  "⚠ YẾU HẲN xếp SAU chông chênh, không phải trước — luyện thêm cùng kiểu câu ở chỗ "
  "bé đang sai nhiều là bắt bé sai tiếp, mà mở đầu buổi bằng ba câu sai liền thì bé "
  "nghỉ. Chỗ ấy cần bài PHỤ ĐẠO (Đợt 4). "
  "⚠ KHÔNG bỏ câu nào, chỉ đổi thứ tự — thanh đếm câu và phép chấm đều dựa trên số "
  "câu. Bỏ hẳn câu đã thạo là Mastery Skip của Đợt 4, cần ngưỡng riêng cao hơn. "
  "⚠ Chưa-có-tin KHÔNG phải bé-rất-yếu: `p` thiếu mà coi là 0 thì cả nhóm bé chưa "
  "học bị đẩy xuống cuối buổi.",
  "2.3.2-nối · 2.3.1-overlay", D2, "xong"),

R("2.1.2", "Chiều THỜI GIAN (T): lặp lại ngắt quãng, đường cong quên, đo mệt mỏi nhận thức", PH,
  "✅ HAI TRONG BA XONG Đợt 2 (22-08), ĐÃ DEPLOY. LẶP LẠI NGẮT QUÃNG nay chạy trọn "
  "đường ống: `onMicroDoneTA` sinh thẻ → thẻ mời trên trang chính → màn `OnLai` → "
  "hộp Leitner đẩy lên hoặc về 0. ĐƯỜNG CONG QUÊN: `quenDan()` trong `bkt.js`, nửa "
  "đời 14 ngày.",
  "❌ CÒN 'ĐO MỆT MỎI NHẬN THỨC'. Suy được từ `ms` (thời gian phản hồi dài dần trong "
  "một phiên) — số liệu đã có sau Đợt 1, chưa ai tính.",
  OK,
  "⚠ PHÁT HIỆN LÚC LÀM: bộ sinh thẻ ôn đã chạy từ lâu và luật cũng đã cho đọc "
  "`reviewQueue`, nhưng KHÔNG màn nào đọc thư mục ấy — kể cả môn TOÁN. Thẻ sinh ra "
  "rồi nằm đó, và lặp-lại-ngắt-quãng tồn tại trên giấy suốt thời gian dài. Nối thêm "
  "trigger cho Tiếng Anh mà không dựng màn thì chỉ là đạt trên giấy lần nữa. "
  "⚠ QUÊN thì kéo P(L) về 0.5, KHÔNG về 0: bé quên thì thành không-chắc, không "
  "thành chưa-từng-biết — kéo về 0 là phạt bé vì nghỉ vài hôm. "
  "Còn lại: cộng `ms` theo thứ tự lượt trong một phiên rồi xem có dốc lên không.",
  "2.3.2-quên", D2, "gần xong"),

R("2.1.2", "Chiều SƯ PHẠM (P): đo và thích ứng theo ĐỊNH DẠNG bài tập bé hợp nhất", PH,
  "Có 6 định dạng (chọn · điền · xếp thẻ · ghép chữ · nghe-nhìn · nói) xoay theo BẬC, "
  "nhưng xoay theo LUẬT CHUNG chứ không theo bé.",
  "✅ ĐO thì XONG Đợt 2 (22-08), ĐÃ DEPLOY: `lib/hoso.js` cộng tỉ lệ đúng theo từng "
  "`format`, hiện trong Góc bố mẹ ở trang chính. "
  "❌ CHƯA THÍCH ỨNG: bộ chọn câu vẫn không đổi gì theo định dạng bé mạnh hay yếu.",
  OK,
  "⚠ CHỖ NGUY NHẤT LÀ KẾT LUẬN SỚM, và nay có phép canh: bé làm 2 câu gõ chữ sai cả "
  "2 thì kết luận 'yếu dạng gõ chữ 0%' vừa sai vừa TỰ NUÔI CHÍNH NÓ — nhãn ấy dẫn "
  "tới cho bé ít câu gõ chữ đi, nên mẫu không lớn thêm, nên nhãn không bao giờ được "
  "sửa. Nguy hơn nữa vì đây là nhãn dán lên MỘT ĐỨA TRẺ, cho bố mẹ đọc. Nên dưới 8 "
  "lượt thì màn hình IM LẶNG, và khi nói thì hiện cả cỡ mẫu. "
  "Còn lại: cho bộ chọn ưu tiên định dạng bé mạnh khi bé đang đuối, và định dạng bé "
  "yếu khi bé đang tốt.",
  "2.5.2-hành vi", D2, "xong phần đo"),

R("2.1.2", "Chiều ĐỘNG LỰC (M): lồng ngữ cảnh theo SỞ THÍCH cá nhân", PH,
  "Phòng nói CÓ hỏi bé thích gì rồi truyền vào lời dặn LLM: `hoSo: { thich }` "
  "(`PhongNoi.jsx:208`) → `dongHoSo()` (`phongnoi.js:1213`) sinh câu 'The child told "
  "you they like …'. Bài tập cũng ưu tiên từ bé đã chọn (`phongnoi.js:263`).",
  "✅ ĐÃ VÁ 21-08 (Đợt 0) — sở thích nay sống qua buổi. Còn lại: ba màn kia (học · "
  "đọc · viết) vẫn chưa dùng sở thích, nên chiều Động lực mới đủ ở PHÒNG NÓI.",
  OK,
  "Đã làm: `soThich` vào sổ tại máy + `hocBaTA` (`loai: soThich`), gộp theo luật "
  "\'bản mới hơn thắng\', khoá theo QUYỂN chứ không theo unit — vốn phòng nói là vốn "
  "tích luỹ nên nhớ một lần dùng được cả quyển. Nhớ được thì KHÔNG hỏi lại. "
  "⚠ Chỗ suýt hỏng, nay có cổng canh: từ nhớ trong sổ đi THẲNG vào lời dặn LLM, mà "
  "sổ sống lâu hơn nội dung — đổi quyển hay dồn unit là từ ấy rơi ra ngoài vốn, tức "
  "là mình tự chọc thủng tầng chống ảo giác TỪ BÊN TRONG, và `cauHopLe()` phía sau "
  "không cứu được (nó bác câu, cô giáo nói mãi không qua). Nên `PhongNoi` soi lại "
  "từ ấy có trong `von` không, mỗi lần mở màn. Cổng `tienganh_sothich.test.mjs`, "
  "đã đảo chiều thử 3 ca. CÒN LẠI: truyền sang màn Viết (`loiDanCham`).",
  "—", D0, "xong phần phòng nói"),

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
  "⚠ CON SỐ 50/148 GÂY HIỂU LẦM, tôi đã soi kỹ lại. Ở tầng bản chuẩn thì `o_thay` "
  "có ở 153/164 mẫu câu, vì `sua_slot` trong `lopN_bu.json` bù tay phần bản đồ "
  "thiếu (lớp 4 có 20 mục, lớp 5 có 21). Trong 11 mẫu còn trống thì 3 mẫu ĐÚNG là "
  "không có ô nào ('Goodbye.' · 'How are you? - Fine, thank you.') — trống là phải.",
  OK,
  "✅ LÀM XONG PHẦN CÓ HẠI 21-08 (Đợt 0). Soi ngược từ hậu quả thay vì đếm nút: "
  "chỉ 2/94 bài có bậc RÁP CÂU mỏng hơn số mẫu câu, và `DL:TA4.B00` là ca thật — "
  "1 câu ráp cho 4 mẫu, vì `sp_g4_st_4` ('They\'re + [Verb-ing]') không sinh nổi "
  "câu nào: 6 động từ của unit đều thiếu `ing`, mà `o_thay` cũng rỗng. Đã khai "
  "`ing` cho cả 6 và thêm `sua_slot`; bậc ráp 1 → 5 câu, sinh thêm 4 clip tiếng. "
  "`DL:TA1.B16` để nguyên — nó mỏng vì vốn từ chỉ có MỘT danh từ đếm được.",
  "—", D0, "xong"),

R("2.2.1", "Siêu dữ liệu nút TỪ VỰNG: id duy nhất · lexical_type · component_words", DU,
  "680/680 có `word` và `lexical_type`; 285/680 có `component_words` (đúng — chỉ CỤM "
  "mới có từ cấu thành); 660/680 có IPA; 661/680 có nghĩa tiếng Việt.",
  "19 nút thiếu nghĩa/IPA — phần lớn là TÊN RIÊNG (Ben · Mary · Ms Hoa), kho cố ý "
  "không dịch.", XONG, "—", "—", DX, "—"),

R("2.2.1", "Siêu dữ liệu nút NGỮ PHÁP: tense · sentence_type · formula", DU,
  "⚠ SỬA HAI LẦN. Bản đầu báo 0/148 vì tôi đọc khoá TẦNG NGOÀI của nút. Soi lại "
  "21-08 thì hai trường ấy nằm LỒNG trong `grammar_metadata`, và đủ 148/148 nút ngữ "
  "pháp lớp 1–5 — `chuan_tienganh.py:146` đọc thẳng `gm.get(\'tense\')`. Xuống tầng "
  "bản chuẩn thì `thi` 163/164 và `kieu_cau` 163/164 "
  "(`chuan_lop5.json`: present_simple 25 · past_simple 7 · future_simple 4 · "
  "future_be_going_to 2 · conditional_would 2; wh_question 32 · yes_no_question 6). "
  "`formula` (grammar_form) đủ 148/148.",
  "Không thiếu gì. Chỗ 163/164 là `sp_g3_starter_1` — mẫu SOẠN THÊM cho unit Starter "
  "lớp 3, không có nút trong bản đồ nên không thừa hưởng `grammar_metadata`.",
  XONG,
  "✅ LÀM XONG 21-08 (Đợt 0). Khai `thi: present_simple` · `kieu_cau: wh_question` "
  "vào `lop3_bu.json` — chép của `sp_g2_u13_1`, câu y hệt từng chữ ở lớp 2 U13, "
  "không tự nghĩ ra. Nay đủ 164/164. Việc 'ghi ngược lên nút thô' ở bản trước thì "
  "BỎ: nó dựa trên phép soi sai, và `ban_do_tieng_anh.json` là kho gốc cấm sửa.",
  "—", D0, "xong"),

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
  "✅ ĐÃ VÁ 21-08 (Đợt 0). Trên NÚT BẢN ĐỒ thì vẫn 0/680 — kho gốc cấm sửa — nhưng "
  "thang tiên quyết ở tầng bản chuẩn nay có 58 cạnh TỪ VỰNG mới.",
  OK,
  "Đã làm: `thang_tu_vung()` trong `chuan_tienganh.py` sinh MÁY từ `vai`, không khai "
  "tay nút nào. Ra đúng khuôn luận văn nêu ở 2.2.2c: "
  "`v_g3_ustarter_ten` → `v_g3_u11_eleven`, và `v_g4_u4_may` → `v_g4_u9_june`. "
  "⚠ HAI CHỖ CỐ Ý HẸP. (1) Chỉ ba nhóm `so · thang · thu`. `tanso` (always · often "
  "· sometimes) là ca sát nút: nó CÓ thứ tự — thứ tự TẦN SUẤT — nhưng đó không phải "
  "thứ tự HỌC, sách dạy cả sáu từ cùng lúc. Nối bừa thì lan truyền chẩn đoán ở 2.3.3 "
  "đi ngược vào một cạnh vô nghĩa rồi kết luận bé \'hổng gốc ở màu đỏ\': sai mà nghe "
  "rất có lý. (2) Cạnh có NHÃN: `noi_bai` (bắc cầu giữa hai unit — cạnh tiên quyết "
  "thật) tách khỏi `trong_bai` (thứ tự đọc trong cùng một bài). Ai lấy `trong_bai` "
  "đi khoá bài là chặn bé giữa chính bài đang học. CÒN LẠI: cạnh XUYÊN QUYỂN cho từ "
  "vựng (lớp 2 U13 eleven ↔ lớp 3 U11 eleven) — `chuan()` chạy từng quyển một nên "
  "chưa với sang nhau được.",
  "—", D0, "xong phần trong quyển"),

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
R("2.3.1", "Mô hình che phủ (Overlay) trạng thái lên từng nút đồ thị", DU,
  "Sổ của bé khoá theo MÃ BÀI (`DL:TA5.B01`), không theo mã nút (`v_g5_u1_dolphin`). "
  "`progressTA/{uid}/micros` lưu: pass · score · total · bac · attempts · at "
  "(`duLieu.js:67`).",
  "⚠ CHƯA DEPLOY.",
  OK,
  "✅ XONG Đợt 1 (22-08): 4226/4226 câu mang `maNut` (3430 nút từ vựng · 796 nút "
  "mẫu câu); lớp phủ là `mastery/{uid}/units/{maNut}` do `onAttempt` tự ghi. Sổ cũ "
  "theo BÀI giữ nguyên — hai sổ song song. Dựng lại 5 quyển thêm 17 700 dòng, XOÁ "
  "0 dòng. Cổng `tienganh_manut` canh nút có thật và đúng MỘT nút chính. "
  "── Phát hiện đã làm việc này rẻ đi: Không phải đổi "
  "khoá sổ hiện có (việc lớn, đụng cả 4 màn). `chuan_lopN.json` ĐÃ GIỮ mã nút đồ "
  "thị: `ma: \"v_g5_u1_city\"` đủ 740/740 từ và `ma: \"sp_g5_u1_1\"` cho mẫu câu. Bộ "
  "sinh bài đang cầm mã ấy trong tay mà không ghi ra. Nên chỉ cần: (1) "
  "`sinh_bai_tienganh.py` gắn `maNut: [...]` vào từng câu luyện; (2) dựng lại 5 "
  "quyển; (3) lớp phủ chính là `mastery/{uid}/units/{maNut}` mà `onAttempt` tự ghi. "
  "Sổ cũ theo bài GIỮ NGUYÊN — hai sổ song song, không đụng nhau.",
  "—", D1, "≈2 ngày (gồm dựng lại 5 quyển)"),

R("2.3.1", "`p_learned` — xác suất nắm vững từng nút", DU,
  "✅ XONG Đợt 1. `applyAttempt()` ghi `p` cho từng nút, và `pTruoc` giữ mức thạo "
  "TRƯỚC lượt ấy nên ΔC của mục 2.5.3 tính được.",
  "⚠ CHƯA DEPLOY.",
  OK, "Quà kèm của Đợt 1 — không phải viết gì thêm.", "2.3.1-overlay", D1, "xong"),

R("2.3.1", "`struggle_count` — đếm số lần sai LIÊN TIẾP tại một nút", DU,
  "✅ XONG Đợt 1. `saiLienTiep` trong `applyAttempt` — đúng MỘT lần là về 0, vì cái "
  "cần đo là ĐANG BÍ chứ không phải TỪNG BÍ.",
  "⚠ CHƯA DEPLOY.",
  OK,
  "Khác hẳn `nAttempts`, và khác hẳn `attempts` của sổ tiến độ (đếm số lần làm CẢ "
  "BÀI): bé sai 3 lần rồi đúng 10 lần thì tỉ lệ đúng trông vẫn đẹp, mà lúc sai 3 "
  "lần liền mới là lúc bé không tự thoát ra được.", "2.3.1-overlay", D1, "xong"),

R("2.3.1", "`last_interacted` — dấu thời gian lần gần nhất", DU,
  "✅ XONG Đợt 1. `lastSeen` mức NÚT trong `mastery`, và `ts` mili-giây từng lượt "
  "trong `attempts`.",
  "⚠ CHƯA DEPLOY.",
  OK, "Quà kèm của Đợt 1.", "2.3.1-overlay", D1, "xong"),

R("2.3.1", "`RT_avg` — thời gian phản hồi trung bình", DU,
  "✅ XONG Đợt 1. `CauHoi.jsx` bấm giờ từng LƯỢT (đặt lại khi bé bấm Thử lại, để "
  "lượt hai không gồm thời gian bé ngồi đọc lời báo sai), `applyAttempt` gộp thành "
  "`msTrungBinh` ngay trong hồ sơ nút.",
  "⚠ CHƯA DEPLOY.",
  OK,
  "⚠ HAI CHỖ DỄ RA SỐ SAI, đã có cổng canh (`bkt.test.mjs`, đảo chiều thử cả hai): "
  "(1) lượt THIẾU `ms` phải nằm NGOÀI mẫu — coi là 0 thì mỗi dòng thiếu kéo trung "
  "bình xuống, và 'bé trả lời nhanh dần' thành một kết luận do LỖI GHI sinh ra; "
  "(2) cộng dồn bằng TỔNG chứ không nhân trung bình cũ với n — phép sau trôi số "
  "sau vài trăm lượt, mà tài liệu này sống suốt đời học của bé. Chưa đo được lượt "
  "nào thì trả `null`, không trả 0.",
  "2.5.2-hành vi", D1, "xong"),

R("2.3.1", "`H_req` — số lần dùng trợ giúp", DU,
  "LẠI ĐÚNG MẪU CŨ: bên TOÁN đếm đủ và màn cô giáo hiện ra ('xem N gợi ý' — "
  "`HocSinhChiTiet.jsx:349`, nguồn `PracticeItem.jsx:47` → `sync.js:115`). Bên TIẾNG "
  "ANH gợi ý CÓ HIỆN cho bé (`CauHoi.jsx:270`, sau `HIEN_GOI_Y` lần thử) nhưng "
  "KHÔNG ĐẾM.",
  "⚠ CHƯA DEPLOY.",
  OK,
  "✅ XONG Đợt 1. `hintsUsed` từng lượt ở `CauHoi.jsx`, gộp thành `goiTrungBinh` "
  "trong hồ sơ nút. Dùng ĐÚNG tên trường của Toán nên màn cô giáo hiện được ngay. "
  "⚠ Nghĩa hơi khác Toán, chỗ nào đọc cũng nên biết: bên Tiếng Anh gợi ý hiện TỰ "
  "ĐỘNG sau vài lần thử chứ không do bé bấm xin — nên đây là 'đã THẤY mấy gợi ý', "
  "không phải 'đã XIN mấy lần'.",
  "2.5.2-hành vi", D1, "xong"),

R("2.3.1", "Hồ sơ bé: CEFR hiện tại · sở thích · định dạng ưa thích", DU,
  "✅ ĐỦ BA TRƯỜNG, Đợt 0 + Đợt 2, ĐÃ DEPLOY. Sở thích: `loai: soThich` (Đợt 0). "
  "Định dạng: `loai: hoSo`, bảng đúng/tổng theo từng `format` (Đợt 2). CEFR mức BÉ: "
  "`cefrCuaBe()` suy từ quyển cao nhất bé đã xong HẾT bài — `cefr` nay khai trong "
  "sổ đăng ký cho cả 5 quyển, chép từ `chuan_lopN.json` chứ không gõ tay.",
  "Sở thích mới dùng ở PHÒNG NÓI; ba màn kia chưa đọc tới (xem mục 2.1.2-M).",
  OK,
  "⚠ ĐANG HỌC DỞ THÌ KHÔNG TÍNH CEFR. Bé mới xong 1/20 bài quyển A1 mà đã dán nhãn "
  "A1 là nói quá về bé — mà nhãn ấy đi vào lời dặn LLM, tức cô giáo máy sẽ nói bằng "
  "vốn từ bé chưa có. "
  "⚠ Thứ tự CEFR lấy theo thứ tự SỔ ĐĂNG KÝ, không so chuỗi: so chuỗi thì chuỗi A1 "
  "đứng TRƯỚC chuỗi Pre-A1 theo bảng chữ cái, tức là ngược hẳn với thang trình độ. "
  "⚠ Gộp hai máy thì CỘNG bảng định dạng, không lấy bên mới hơn như mọi thứ khác "
  "trong sổ — đây là phép đếm tích luỹ, lấy bản mới hơn là vứt đi 40 câu bé làm "
  "trên máy kia.",
  "2.1.2-M · 2.1.2-P", D2, "xong"),

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
  "Luận văn viết θ = 0,95 (mục 2.5.1 và tài liệu [6]). Hệ thống chạy 0,85. "
  "✅ BÁC ĐÃ CHỐT 21-08-2026: GIỮ 0,85, KHÔNG sửa mã.",
  KHONG,
  "KHÔNG sửa phần mềm — bác chốt giữ 0,85, và một dòng mã cũng không phải đổi. "
  "Việc còn lại nằm ở LUẬN VĂN: sửa θ = 0,95 thành θ = 0,85 ở mục 2.5.1, và ghi rõ "
  "đây là con số HIỆU CHỈNH THEO THỰC NGHIỆM cho trẻ tiểu học Việt Nam chứ không "
  "phải chép từ tài liệu [6]. Lý do đã có sẵn trong `bkt.js`: bộ tham số theo tài "
  "liệu tuyên bé đã thạo chỉ sau 2 câu đúng — quá dễ dãi với trẻ con, và đó là phép "
  "đo trên chính hệ thống này. ⚠ Sửa số ở mã thì phải đổi CẢ HAI chỗ (`bkt.js:14` "
  "và `toan/lib/adaptive.js:13`) và nó ĐỤNG MÔN TOÁN đang chạy thật — thêm một lý "
  "do nữa để giữ nguyên.",
  "—", DX, "sửa luận văn, không sửa mã"),

R("2.3.2", "BKT chạy cho môn TIẾNG ANH", DU,
  "✅ XONG Đợt 1 (22-08). `mon/tienganh/lib/suKien.js` dựng bản ghi rồi đẩy vào "
  "`attempts/` chung; `CauHoi.jsx` gọi sau MỖI lượt trả lời. `bktUnit` là mã nút "
  "đồ thị. Cổng `tienganh_sukien` (14 phép) đối chiếu thẳng với `firestore.rules`.",
  "⚠ CHƯA DEPLOY (22-08) — mã xong, cổng xanh, nhưng chưa lượt học nào chạy qua "
  "đường này trên bản thật.",
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

R("2.3.2", "Cơ chế QUÊN (forgetting) tích hợp vào BKT", DU,
  "✅ XONG Đợt 2 (22-08), ĐÃ DEPLOY. `quenDan(p, soNgay)` trong `bkt.js`, nửa đời 14 "
  "ngày, chạy ngay trước mỗi lần cập nhật BKT.",
  "Nửa đời 14 ngày là con số CHỌN theo lịch ôn sẵn có, chưa hiệu chỉnh bằng dữ liệu "
  "học thật — khi có rồi thì chỉnh lại và ghi lý do như `DEFAULT_PARAMS`.",
  OK,
  "⚠ KÉO VỀ 0,5, KHÔNG VỀ 0. Bé quên thì thành không-chắc, không thành "
  "chưa-từng-biết — kéo về 0 là bắt bé học lại từ đầu một thứ đã từng thạo, tức "
  "phạt bé vì nghỉ vài hôm. Hệ quả nghe ngược đời mà đúng: nút bé từng làm SAI "
  "nhiều sẽ NHÍCH LÊN theo thời gian, vì hiểu biết của hệ thống về bé nhạt đi theo "
  "CẢ HAI chiều. "
  "⚠ Đụng môn Toán đang chạy thật, nên ba phép canh đều đảo chiều thử: bé học đều "
  "mỗi ngày thì mức thạo KHÔNG bị phạt (lệch < 0,02); tài liệu đời cũ thiếu "
  "`lastSeen` thì không phân rã theo mốc bịa ra; `lastSeen` ở tương lai (đồng hồ "
  "máy con sai) thì coi như vừa gặp.",
  "2.3.2-nối", D2, "xong"),

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

R("2.5.2", "Lưu vết HƯỚNG SỰ KIỆN — chuỗi sự kiện bất biến", DU,
  "MỘT chỗ đã làm gần đúng: PHÒNG NÓI ghi mỗi buổi thành MỘT tài liệu riêng khoá "
  "theo mã buổi — `phongNoiTA/{uid}/buoi/{maBuoi}`, giữ nguyên từng lượt "
  "`{vai, chu, en, vi}` đúng thứ tự (`goiPhongNoi.js:167`). Buổi cũ không bị buổi "
  "mới đè.",
  "Ba màn còn lại thì ngược hẳn: `luuMucHocBa()` dùng `setDoc(merge)` trên khoá cố "
  "định `{loai}__{khoa}` (`duLieu.js:87`) — lần làm sau ĐÈ lần trước, đúng thứ "
  "event-sourcing sinh ra để tránh. `gopTienDo()` cũng lấy bản mới hơn thắng.",
  OK,
  "✅ XONG Đợt 1. `attempts/` là chuỗi BẤT BIẾN thật, và bất biến do LUẬT chứ không "
  "do quy ước: `firestore.rules` chốt `allow update, delete: if false` — không ai "
  "sửa được, kể cả admin. Mỗi lượt một tài liệu; mã nhúng số thứ tự nên đẩy lại bao "
  "nhiêu lần cũng không sinh dòng trùng. ⚠ GIỮ NGUYÊN sổ trạng thái (`progressTA`) "
  "bên cạnh, KHÔNG thay bằng chuỗi sự kiện: màn hình cần biết 'bé đã đạt bài này "
  "chưa' trong MỘT lần đọc, dựng lại từ chuỗi sự kiện mỗi lần mở app là chậm và "
  "tốn. Hai thứ song song, mỗi thứ một việc.",
  "2.3.2-nối", D1, "xong"),

R("2.5.2", "Dữ liệu định danh & thời gian (mili-giây)", DU,
  "Phòng nói CÓ mã phiên thật (`maBuoi` làm tên tài liệu) kèm `at` (ISO) và "
  "`serverTs`. Ba màn kia chỉ có `at` mức bài.",
  "⚠ CHƯA DEPLOY.",
  OK,
  "✅ XONG Đợt 1. Mỗi lượt có `sessionId` (một lần mở bài là một phiên), `ts` "
  "mili-giây RIÊNG từng lượt, và `serverTs` do máy chủ đóng dấu lúc gửi. ⚠ Hai mốc "
  "phục vụ hai việc: `ts` là lúc bé LÀM (giữ nguyên dù bản ghi nằm chờ trong hàng "
  "đợi mấy ngày vì mất mạng), `serverTs` là lúc GỬI. Mọi thống kê cô giáo nhìn phải "
  "quy về mốc máy chủ — máy tính bảng đặt sai ngày thì chuỗi ngày học nhảy loạn.",
  "2.3.2-nối", D1, "xong"),

R("2.5.2", "Dữ liệu nhận thức: Node_ID · đúng/sai · câu trả lời THÔ", DU,
  "Hai màn có lưu nguyên văn bé làm: BÀI VIẾT giữ `viet: String(viet)` "
  "(`progress.js:224`), PHÒNG NÓI giữ trọn hội thoại từng lượt. Đủ để đọc ra bé sai "
  "chỗ nào.",
  "⚠ CHƯA DEPLOY. Và `revealed` (bé chịu thua, xem đáp án) chưa ghi thẳng — suy "
  "được từ 'lượt cuối sai rồi không có lượt nào nữa', nhưng suy không chắc bằng ghi.",
  OK,
  "✅ XONG Đợt 1 phần chính. Mỗi lượt mang `bktUnit` (mã NÚT), `correct`, `answer` "
  "(nguyên văn bé gõ hoặc bấm), `expected`, `mode`. Đúng lý do bên Toán đã ghi: "
  "'hai con sai hai kiểu khác nhau cần hai cách giúp khác nhau'. Đáp án dài cắt ở "
  "120 ký tự, để một bài viết không nuốt cả dòng nhật ký.",
  "2.3.1-overlay · 2.3.2-nối", D1, "gần xong"),

R("2.5.2", "Dữ liệu hành vi: thời gian phản hồi · số lần trợ giúp", DU,
  "✅ XONG Đợt 1 — `ms` và `hintsUsed` trên từng lượt, gộp vào hồ sơ nút.",
  "⚠ CHƯA DEPLOY.",
  OK, "Cùng một lần sửa `CauHoi.jsx` với hai mục 2.3.1-RT và 2.3.1-H_req.",
  "—", D1, "xong"),

R("2.5.2", "Bối cảnh hệ thống: P(L) trước/sau · mã prompt để kiểm toán", DU,
  "✅ XONG Đợt 1, CẢ HAI NỬA. P(L) trước/sau: `pTruoc` và `p` trong `applyAttempt`. "
  "Mã prompt: `functions/src/vantay.js` — bác chốt đường VÂN TAY ngày 21-08, nên "
  "giao ước 'máy chủ KHÔNG lưu gì' vẫn nguyên: vân tay trả về cho máy con, máy con "
  "ghi kèm bản ghi của chính bé.",
  "⚠ CHƯA DEPLOY.",
  OK,
  "Vân tay băm phần KHUNG của lời dặn, không băm cả prompt. "
  "⚠ BĂM CẢ PROMPT LÀ HỎNG CẢ HAI ĐẦU: prompt có tên bé, vốn từ, cả lịch sử hội "
  "thoại — nên mỗi lượt ra một vân tay riêng, vừa vô dụng cho việc so mẫu (không "
  "nhóm lại được) vừa thành một mã theo dõi được từng lượt của từng bé. Cổng "
  "`vantay_prompt` bắt chuyện đó bằng cách dựng hai bé khác hẳn nhau rồi ĐÒI vân "
  "tay bằng nhau. "
  "⚠ Hai đường lấy khung KHÔNG ngang nhau: `chamviet` gọi lại chính hàm dựng lời "
  "dặn với dữ liệu rỗng nên ra khung chính xác; `luyennoi` thì lời dặn do MÁY CON "
  "dựng và gửi lên đã thành chữ, máy chủ chỉ lọc được theo dấu hiệu (`locKhung`) "
  "nên SÓT được — thêm một dòng mang tên bé mà quên khai `DAU_RIENG` là nó lọt.",
  "2.3.2-nối", D1, "xong"),

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

R("2.5.3", "Tối ưu hoá prompt theo ΔC", CH,
  "✅ HAI CHÂN ĐÃ CÓ, Đợt 1: vân tay prompt (`vantay.js`) để biết lượt nào dùng mẫu "
  "nào, và `pTruoc`/`p` để tính được ΔC của một lượt. Bác đã gỡ chỗ vướng bằng "
  "quyết định 21-08 — không còn là mục 'chờ bác quyết'.",
  "Chưa có phép ĐO hiệu quả: cần A-R-A (2.5.3) rồi mới gom ΔC theo mẫu prompt được. "
  "ΔC của một lượt lẻ không nói lên gì.",
  OK,
  "Sau A-R-A: gom ΔC trung bình theo từng `(mauPrompt, phienBanMau)`, mẫu nào cao "
  "hơn thì giữ. ⚠ Gom theo `phienBanMau` chứ đừng gom theo mã băm: băm đổi cả khi "
  "sửa một lỗi chính tả, nên gom theo băm là chẻ dữ liệu ra vụn. Mã băm để phát "
  "hiện LỆCH ngoài ý muốn — ai đó sửa lời dặn mà quên tăng số phiên bản.",
  "2.5.3-ΔC", D4, "≈1 ngày"),

R("2.5.3", "Đường cong học tập (tỉ lệ lỗi theo số lần luyện)", DU,
  "✅ XONG Đợt 2 (22-08), ĐÃ DEPLOY. `duongCongHoc()` trong "
  "`functions/src/report.js`, vẽ bằng thanh ngang trong Sổ bố mẹ.",
  "Chỉ tính những nút bé BẮT ĐẦU học trong kỳ — xem lý do ở cột bên.",
  OK,
  "⚠ BẪY ĐÃ TRÁNH: sổ chỉ lấy nhật ký 7 ngày, nên lượt thứ 12 của một từ bé học từ "
  "tháng trước bị ghi thành lần-thứ-1, và đường cong nói dối THEO HƯỚNG ĐẸP LÊN "
  "(điểm đầu tiên lẫn toàn từ bé đã thạo). Lối thoát không phải kéo dài cửa sổ mà là "
  "dùng `nAttempts` của hồ sơ nút: nút nào có tổng số lượt ĐÚNG BẰNG số đếm được "
  "trong cửa sổ thì cả lịch sử nằm trọn ở đây. Màn hình nói thẳng điều đó. "
  "⚠ Điểm dưới 3 mẫu bị BỎ HẲN, không trả kèm cờ: đuôi đường cong luôn thưa, một "
  "điểm dựng trên 2 mẫu nhảy 0% hay 100% tuỳ một câu, mà mắt người nhìn biểu đồ thì "
  "tin ngay.",
  "2.3.2-nối", D2, "xong"),
]

TK_THEM = [
    ("Nội dung đã dựng xong (lớp 1→5)", ""),
    ("Quyển · unit", "5 quyển · 94 unit"),
    ("Từ vựng · mẫu câu", "740 từ · 164 mẫu câu"),
    ("Câu luyện tập · câu sát hạch", "3 752 · 470"),
    ("Bài tả tranh (đọc · viết · nói quanh 1 bức)", "62 bức, lớp 3·4·5"),
    ("Clip tiếng · video", "5 366 · 345"),
    ("Cổng tự động", "82 tệp, tất cả xanh"),
    ("", ""),
    ("Đồ thị tri thức", ""),
    ("Nút · cạnh (toàn bản đồ)", "3 989 · 7 602"),
    ("Nút thuộc lớp 1–5", "1 189"),
    ("Cạnh REQUIRES chạm lớp 1–5", "195 (38 xuyên lớp)"),
    ("Nút có prerequisite_links (lớp 1–5)", "92 / 1 189"),
    ("Mối tiên quyết đã vào bản chuẩn", "157 (10·10·39·64·34)"),
    ("Mã nút đồ thị giữ được ở bản chuẩn", "740/740 từ · 164/164 mẫu câu"),
    ("`thi` · `kieu_cau` ở bản chuẩn", "164/164 · 164/164 (vá 22-08)"),
    ("", ""),
    ("Sau Đợt 0 và Đợt 1", ""),
    ("Câu luyện mang mã nút đồ thị", "4226/4226 (3430 từ vựng · 796 mẫu câu)"),
    ("Cạnh tiên quyết TỪ VỰNG", "58 (trước Đợt 0: 0)"),
    ("Trường mới trong hồ sơ mỗi nút",
     "p · pTruoc · saiLienTiep · msTrungBinh · goiTrungBinh · lastSeen"),
    ("Đã deploy chưa", "Đợt 0 · 1 · 2 đều rồi (21 và 22-08)"),
    ("", ""),
    ("Sau Đợt 2", ""),
    ("Trigger sinh thẻ ôn cho Tiếng Anh", "onMicroDoneTA (tạo mới 22-08)"),
    ("Nửa đời trí nhớ", "14 ngày, kéo P(L) về 0,5"),
    ("Ngưỡng nói được về một định dạng", "8 lượt — dưới đó màn hình im lặng"),
    ("`cefr` trong sổ đăng ký", "cả 5 quyển Tiếng Anh"),
]

LO_TRINH = [
    (D0, "✅ ĐÃ CHẠY XONG 21-08-2026 — trừ hai chỗ chờ bác quyết",
     "XONG: lưu sở thích xuống sổ (kèm cổng mới, đảo chiều thử 3 ca) · khai "
     "`thi`/`kieu_cau` cho `sp_g3_starter_1` (nay 164/164) · vá `DL:TA4.B00` từ 1 "
     "lên 5 câu bậc ráp, sinh thêm 4 clip tiếng · 58 cạnh tiên quyết từ vựng mới. "
     "BỎ khỏi đợt: 'ghi ngược lên nút thô' (dựa trên phép soi sai của tôi) và '6 nút "
     "CEFR' (kho gốc cấm sửa — để Đợt 3 xuất đồ thị con thì thêm). "
     "CHỜ BÁC: đổi θ.",
     "≈1 ngày", "nhích lên, trong đó 4 mục lên hẳn ĐÁP ỨNG",
     "Đã dính hai lỗi trong lúc làm, cả hai đều do phép DIFF bắt chứ không phải cổng: "
     "(1) khai `dang_ing` trong phần bù mà khoá thật là `ing` — dựng lại thấy không "
     "đổi gì mới lộ; (2) `chuan_lop3/4.json` trong kho là bản dựng ĐỜI TRƯỚC, dựng "
     "lại thì mọc thêm `dang_qk`/`dang_ngoi3` toàn null. Nên: `cp` rồi `diff`, và "
     "lọc null ra trước khi đọc. Riêng đổi θ thì ĐỤNG MÔN TOÁN — chạy lại "
     "`bkt.test.mjs` và đối chiếu điểm thạo vài bé trước/sau."),
    (D1, "✅ XONG và ĐÃ DEPLOY 22-08-2026",
     "XONG: 4226/4226 câu mang `maNut` · `lib/suKien.js` đẩy `attempts` sau mỗi "
     "lượt · `ms` (RT_avg) và `hintsUsed` (H_req) đo rồi gộp vào hồ sơ nút · "
     "`saiLienTiep` và `pTruoc` trong `applyAttempt` · vân tay prompt. "
     "LÀM THÊM ngoài kế hoạch: vá 62 câu sát hạch bé không trả lời đúng được.",
     "≈1,5 ngày", "— BKT chạy được cho Tiếng Anh, lưu vết sự kiện đầy đủ",
     "⚠ Deploy phải có CẢ `functions`, không chỉ hosting: `bkt.js` · `onAttempt` · "
     "`vantay.js` đều đổi. Deploy mỗi hosting thì máy con gửi `attempts` lên mà hàm "
     "nền vẫn là bản cũ, sổ thiếu trường mà không gì báo. "
     "⚠ Ba bẫy đã dính lúc làm: cổng `assert.match(ma, /choices/)` XANH GIẢ vì soi "
     "sự-có-mặt-của-chữ (nhánh chết vẫn qua); `dungSuKien` đánh số theo vị trí nên "
     "đẩy lẻ từng lượt là các lượt đè nhau; `sinh_am.py` dựng lại CẢ danh sách chứ "
     "không chỉ clip thiếu."),
    (D2, "✅ XONG và ĐÃ DEPLOY 22-08-2026",
     "XONG: đường cong học tập trong Sổ bố mẹ · `onMicroDoneTA` sinh thẻ ôn cho "
     "Tiếng Anh · phép quên (nửa đời 14 ngày) · MÀN ÔN LẠI cho bé · xếp câu theo "
     "ZPD · hồ sơ bé (định dạng + CEFR mức bé). "
     "LÀM THÊM ngoài kế hoạch: màn ôn lại — vì soi ra `reviewQueue` chưa màn nào "
     "ĐỌC, kể cả môn Toán.",
     "≈2 ngày", "— chiều C xong; T và P mới xong phần ĐO",
     "⚠ Sửa `bkt.js` là đụng môn Toán đang chạy thật — ba phép canh có đảo chiều. "
     "⚠ Khoá `hoSo` mới nên phải `deploy --only firestore:rules` TRƯỚC. "
     "⚠ HAI CỔNG CŨ CẤM NHẦM, và tôi sửa CỔNG chứ không nới mã: một cổng đòi đúng "
     "chữ `canRead` trong khi `reviewQueue` dùng `isMine || isAdmin` (CHẶT HƠN); "
     "cổng kia cấm mọi lần nhắc `mastery/` trong khi tôi chỉ ĐỌC, mà luật "
     "`allow write: if false` khiến ghi là không thể. Cổng đòi một CÁCH VIẾT thay "
     "vì một TÍNH CHẤT thì sớm muộn ép người ta nới luật ra cho nó xanh."),
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
    w2.append(["TỔNG · còn ≈19 ngày cho hai đợt cuối", f"{tong}/{len(B)} mục nâng được",
               f"Trong đó {sum(1 for x in B if x[5] == OK)} nâng lên hẳn ĐÁP ỨNG · "
               f"{sum(1 for x in B if x[5] == GAN)} nâng được phần lớn · "
               f"{sum(1 for x in B if x[5] == QUYET)} chờ bác quyết",
               "Đã tiêu ≈4,5 ngày cho Đợt 0+1+2; còn ≈19 ngày",
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
        (QUYET, "Kỹ thuật làm được; còn vướng một quyết định của bác."),
        (KHONG, "Không nâng được vì không có gì để nâng — phần mềm đã đúng, chỗ cần "
                "sửa nằm ở câu chữ luận văn."),
    ]:
        w3.append([k, dn[k], f"{dn[k] / len(B) * 100:.0f}%", y])
        w3.cell(row=w3.max_row, column=1).fill = PatternFill("solid", fgColor=MAU_N[k])
    w3.append(["", "", "", ""])
    w3.append(["Đích đến", f"{dn[XONG] + dn[OK] + dn[QUYET]}/{len(B)}",
               f"{(dn[XONG] + dn[OK] + dn[QUYET]) / len(B) * 100:.0f}%",
               "Số mục sẽ ở trạng thái ĐÁP ỨNG sau khi chạy hết 5 đợt. "
               f"Nay đã đạt {dem[DU]}/{len(B)} ({dem[DU] / len(B) * 100:.0f}%) — "
               "nhưng xem lại dòng đầu sheet 'Đọc trước': phần của Đợt 1 mới xong "
               "MÃ, chưa deploy."])
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
        ("⚠ ĐỌC DÒNG NÀY TRƯỚC — 'ĐÁP ỨNG' Ở ĐÂY NGHĨA LÀ GÌ", ""),
        ("", "Cột trạng thái nói về MÃ VÀ DỮ LIỆU trong kho. Tính tới 22-08-2026 thì "
             "Đợt 0 · 1 · 2 đều ĐÃ DEPLOY, nên với những dòng ấy hai thứ trùng nhau. "
             "Nhưng cổng xanh vẫn không phải bằng chứng bé học tốt hơn: 82 cổng soi "
             "MÃ và DỮ LIỆU, không cổng nào ngồi cạnh một đứa trẻ."),
        ("", ""),
        ("ĐÃ XONG TỚI ĐÂU", ""),
        ("", "Đợt 0 ✅ · Đợt 1 ✅ · Đợt 2 ✅ — cả ba đã deploy. Đợt 3 và Đợt 4 CHƯA BẮT "
             "ĐẦU, còn khoảng 19 ngày công. Nay 31/54 mục đáp ứng (57%), từ 15 lúc "
             "bắt đầu."),
        ("", ""),
        ("ĐỢT 2 ĐÃ CHẠY XONG — 22-08-2026", ""),
        ("", "Đường cong học tập trong Sổ bố mẹ · thẻ ôn ngắt quãng cho Tiếng Anh · "
             "phép quên (nửa đời 14 ngày) · MÀN ÔN LẠI cho bé · xếp câu theo ZPD · "
             "hồ sơ bé (dạng câu con làm tốt nhất, và CEFR mức bé)."),
        ("Việc ngoài kế hoạch, lần thứ hai",
         "Định nối lịch ôn cho Tiếng Anh thì soi ra `reviewQueue` chỉ được GHI, "
         "KHÔNG màn nào ĐỌC — kể cả môn Toán. Thẻ ôn sinh ra rồi nằm đó, và "
         "lặp-lại-ngắt-quãng tồn tại trên giấy suốt thời gian dài. Không cổng nào "
         "bắt được, vì mỗi cổng chỉ soi phần việc của mình: cổng lịch soi bộ sinh "
         "thẻ (đúng), cổng luật soi firestore.rules (đúng). Cái thiếu là một câu hỏi "
         "không tệp nào sở hữu: AI ĐỌC THỨ NÀY RA? Nên đã dựng màn ôn lại."),
        ("Hai chỗ CỐ Ý chưa ghi là đạt",
         "Chiều Thời gian và chiều Sư phạm mới xong phần ĐO. Mệt mỏi nhận thức chưa "
         "tính, và bộ chọn câu chưa đổi gì theo định dạng bé mạnh/yếu. Đo mà chưa "
         "dùng thì chưa gọi là thích ứng — cùng dạng với chỗ hụt của chiều Nhận thức "
         "sau Đợt 1, nay đã gỡ."),
        ("", ""),
        ("ĐỢT 1 ĐÃ CHẠY XONG — 22-08-2026", ""),
        ("", "4226/4226 câu luyện mang mã nút đồ thị · `lib/suKien.js` đẩy `attempts` "
             "sau MỖI lượt trả lời, nên hàm nền BKT nay ăn được bài Tiếng Anh · đo "
             "RT_avg và H_req rồi gộp vào hồ sơ từng nút · `saiLienTiep` "
             "(struggle_count) và `pTruoc` (để tính ΔC) · vân tay prompt. "
             "12 dòng chuyển sang ĐÁP ỨNG."),
        ("Một việc ngoài kế hoạch",
         "Giữa lúc làm thì lộ ra một lỗi ĐANG CHẠY THẬT: 62 câu sát hạch mà bé bấm "
         "gì cũng bị chấm sai, trong đó 9 bài CẢ kỳ sát hạch không có lấy một câu "
         "đúng được. `SatHach` dựng `CauNgheNhin` cho mọi câu, mà component ấy chỉ "
         "biết dạng đúng/sai. `OnTap` dùng cùng dữ liệu ấy mà không hỏng vì nó rẽ "
         "nhánh — lỗi ở CHỖ NỐI, không tệp nào sở hữu. 75 cổng cũ không bắt được vì "
         "tất cả đều soi DỮ LIỆU, mà dữ liệu thì đúng. Đã vá, đang chờ deploy."),
        ("", ""),
        ("ĐỢT 0 ĐÃ CHẠY XONG — 21-08-2026", ""),
        ("", "Bốn việc: sở thích của bé nay sống qua buổi (kèm cổng canh chỗ nó có "
             "thể chọc thủng tầng chống ảo giác từ bên trong) · mẫu câu Starter lớp 3 "
             "khai đủ `thi`/`kieu_cau`, nay 164/164 · `DL:TA4.B00` từ 1 lên 5 câu bậc "
             "ráp — unit dạy \"They\'re swimming.\" mà trước đó không sinh nổi một câu "
             "luyện nào · 58 cạnh tiên quyết từ vựng đầu tiên, đúng khuôn ví dụ luận "
             "văn nêu. 75/75 cổng xanh."),
        ("Hai việc BỎ khỏi Đợt 0",
         "\'Ghi ngược `thi`/`kieu_cau` lên nút thô\' — bỏ vì nó dựa trên phép soi sai "
         "của tôi (xem mục dưới). \'Thêm 6 nút CEFR\' — bỏ khỏi đợt này vì "
         "`ban_do_tieng_anh.json` là kho gốc cấm sửa; chỗ đúng để thêm là lúc xuất đồ "
         "thị con ở Đợt 3."),
        ("", ""),
        ("VIỆC ĐÁNG LÀM TIẾP THEO", ""),
        ("1 · Xem bằng MẮT trước khi tin bảng",
         "Ba đợt vừa rồi đổi đúng những thứ bé nhìn thấy: thứ tự câu trong bài, thẻ "
         "mời ôn tập, buổi ôn, Góc bố mẹ. Cổng không thay được việc ngồi cạnh một "
         "đứa trẻ mở app ra. Đây là việc đáng làm trước cả Đợt 3."),
        ("2 · Đợt 3 — đồ thị lúc chạy",
         "Xuất đồ thị con (1189 nút + 195 cạnh REQUIRES + 157 mối thang) ra "
         "`web/public/content/`, rồi lan truyền chẩn đoán ngược để tìm nút gốc rễ. "
         "Mở khoá 8 mục, và là chân đế cho phụ đạo ở Đợt 4."),
        ("3 · Hai nửa còn thiếu của Đợt 2",
         "Mệt mỏi nhận thức (cộng `ms` theo thứ tự lượt trong phiên, xem có dốc lên "
         "không) và thích ứng theo định dạng (cho bộ chọn ưu tiên dạng bé mạnh khi "
         "bé đang đuối). Cả hai đều nhỏ, và số liệu đã có sẵn."),
        ("", ""),
        ("HAI CHỖ CẦN BÁC QUYẾT, KHÔNG PHẢI CHỖ KỸ THUẬT", ""),
        ("1 · Máy chủ có lưu prompt không?",
         "Hiện CỐ Ý không lưu gì ('Máy chủ KHÔNG lưu gì (bác chốt)'). Giữ nguyên thì "
         "mục 2.5.2 (kiểm toán prompt) và 2.5.3 (tối ưu prompt theo ΔC) đóng. Có "
         "ĐƯỜNG GIỮA: lưu VÂN TAY prompt (mã băm + phiên bản mẫu) thay vì nguyên "
         "văn — đủ để so 'mẫu nào dạy hiệu quả hơn' mà không lưu thêm chữ nào về bé. "
         "Tôi nghiêng về đường giữa này."),
        ("2 · Ngưỡng tinh thông θ — ✅ ĐÃ CHỐT",
         "Bác chốt 21-08-2026: GIỮ 0,85. Không sửa một dòng mã nào. Việc còn lại nằm "
         "ở luận văn — sửa mục 2.5.1 thành θ = 0,85 kèm lý do: con số hiệu chỉnh "
         "theo thực nghiệm cho trẻ tiểu học Việt Nam, vì bộ tham số theo tài liệu "
         "[6] tuyên bé đã thạo chỉ sau 2 câu đúng. Con số có phép đo đứng sau thì "
         "mạnh hơn con số chép lại."),
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
         "Bản đầu tôi báo 0/148 và xếp MỘT PHẦN. Sai vì đọc khoá TẦNG NGOÀI của nút: "
         "hai trường ấy nằm LỒNG trong `grammar_metadata` và có đủ 148/148 — "
         "`chuan_tienganh.py:146` vẫn đọc chúng suốt. Nay xếp ĐÁP ỨNG, và cái tôi "
         "định làm để \'vá\' (ghi ngược lên nút thô) hoá ra không có gì để vá."),
        ("Mục 2.2.1 · target_vocab_slots",
         "Bản đầu tôi báo 50/148 thiếu và định bù cả 50. Con số ấy gây hiểu lầm: "
         "`sua_slot` trong `lopN_bu.json` đã bù tay phần bản đồ thiếu, nên ở tầng bản "
         "chuẩn `o_thay` có ở 153/164 mẫu, và 3 trong 11 mẫu còn lại ĐÚNG là không có "
         "ô nào (\'Goodbye.\'). Soi ngược từ HẬU QUẢ thay vì đếm nút thì chỉ 2/94 bài "
         "bị mỏng thật — và đó mới là chỗ đáng sửa."),
        ("", ""),
        ("MỘT LỖI CỦA CHÍNH TÔI, ĐÁNG GHI RA", ""),
        ("Phép soát cổng của tôi bị mù một nửa",
         "Tôi soát 79 cổng bằng `grep '^not ok'`. Nhưng chỉ 18 cổng dùng node:test "
         "và báo lỗi kiểu ấy; 61 cổng còn lại tự viết và báo bằng dòng 'N PASS · M "
         "FAIL'. Phép lọc của tôi KHÔNG NHÌN THẤY nhóm 61 — nên mấy lần tôi nói "
         "'75/77/79 cổng xanh' là nói quá. Soát lại bằng MÃ THOÁT (đúng cho cả hai "
         "kiểu) thì lộ ra `tienganh_am` đã ĐỎ từ commit Đợt 0 — commit mà tôi đã "
         "deploy. Nay đã sửa và soát lại: 79/79 xanh thật."),
        ("Lỗi ấy che mất cái gì",
         "4 clip tiếng mới của Đợt 0 có mp3 thật trên máy chủ nhưng CHƯA VÀO SỔ ÂM "
         "`lop4_am.json` — mà app tra clip qua sổ, không quét thư mục. Nguyên nhân: "
         "tôi chạy `sinh_am.py` thiếu cờ `--so`. Công cụ CÓ in cảnh báo đúng chuyện "
         "đó, nhưng tôi chạy nền và chỉ đọc phần đuôi nên không thấy. Chạy lại đúng "
         "lệnh thì 'sinh mới 4 · dùng lại 1115'."),
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
    dich = dn[XONG] + dn[OK] + dn[QUYET]
    print(f"  ── nay {dem[DU]}/{len(B)} ({dem[DU] / len(B) * 100:.0f}%) "
          f"→ đích {dich}/{len(B)} ({dich / len(B) * 100:.0f}%) sau khi chạy hết 5 đợt")
    print("  ✓ Đợt 0 · 1 · 2 đều đã deploy (22-08). Còn Đợt 3 và Đợt 4.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
