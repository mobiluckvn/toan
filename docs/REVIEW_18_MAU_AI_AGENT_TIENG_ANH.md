# REVIEW 18 MẪU KIẾN TRÚC AI AGENT → ÁP DỤNG CHO MÔN TIẾNG ANH (web5 / Kỹ Sư Nhí)

> Nguồn: `Kien_truc_AI_Agent.docx` (18 mẫu + 1 mẫu cắt ngang, 10/2026) đối chiếu với mã nguồn repo web5 (`web/src/mon/tienganh/**`, `web/functions/src/**`), rà ngày 09-10-2026. Bản gốc dạng Excel: `docs/Review_18_mau_AI_Agent_cho_Tieng_Anh.xlsx`.
>
> **Dành cho Claude Code:** đọc §0 (quy ước), §1 (chẩn đoán), rồi làm theo §7 (từng việc) + §8 (ca kiểm) + §9 (lời dặn). §10 là prompt giao việc dán thẳng.


## §0 · QUY ƯỚC BẮT BUỘC CHO MỌI VIỆC

1. `cd web && npm test` phải **0 FAIL** trước và sau mỗi việc (hiện 74+ tệp kiểm, chạy bằng `node`, không cần trình duyệt).
2. **Không import chéo** `mon/toan` ↔ `mon/tienganh`, và browser (`src/`) ↔ máy chủ (`functions/`). Cổng `test/ranh_gioi.test.mjs` chặn. Cần dùng chung thì **chép + viết cổng so hai bản** (mẫu: `lib/onlai.js` ↔ `functions/src/schedule.js`, cổng `tienganh_onlai.test.mjs`).
3. **Máy chủ KHÔNG lưu gì.** Mọi lời gọi LLM đi qua callable có chốt cửa (`soiGoi` / `soiBaiViet`). Ngữ cảnh do máy con giữ và tự đẩy lên Firestore theo luật.
4. **Mọi câu tiếng Anh do AI sinh ra** phải qua `soiCau()` / `cauHopLe()` / `cauHoiHopLe()` trước khi tới bé. Các mẫu mới chỉ thay cách **xử lý khi soi trượt**, không bỏ cổng.
5. Mọi vòng lặp / trần ký tự / trần bước là **hằng export** và có cổng canh.
6. Sửa lời dặn đáng kể → tăng `PHIEN_BAN_MAU` trong `functions/src/vantay.js`; dòng mang dữ liệu riêng của bé phải nằm trong `DAU_RIENG` (hoặc khối `<<RIENG … RIENG>>` sau V3).
7. Tiêm hàm mạng qua tham số (`taoClient`, `goi`) để test bằng `node` — **không mock module**.
8. Viết chú thích đầu hàm theo giọng hiện có của kho (VÌ SAO / ⚠ / "bác chốt ngày…").
9. Mỗi việc một phiên Claude Code riêng, một commit riêng. Thứ tự khuyến nghị: **V1 → V2 → V3 → V6 → V4 → V5** (GĐ 1), **V7 → V8 → V9 → V10** (GĐ 2), **V11 → V12** (GĐ 3).


## §1 · TỔNG QUAN & CHẨN ĐOÁN


### A. HIỆN TRẠNG — AI đang được dùng ở ĐÂU trong môn Tiếng Anh

**Phòng luyện nói (PhongNoi.jsx · lib/phongnoi.js · functions/luyennoi.js)**

1 lời gọi LLM / lượt (Groq gpt-oss-120b, reasoning_effort=low, temp 0.4). MÁY CON tự chọn việc (xoay vòng cứng tu → mau → thay theo số lượt, `viecTiepTheo`), mô hình chỉ lo 'diễn đạt' trong khuôn 10 luật cứng. Câu trả về bị `soiCau()` soi: trượt (lặp / ô trống / ngoài vốn) → thay bằng câu đóng sẵn `cauThayThe()` ('Con nghe rồi nói lại từ … nhé'). KHÔNG có vòng gọi lại để sửa. Lời bé nói chấm bằng so chuỗi STT (`chamnoi.js`), LLM không hề biết bé nói gì ngoài điểm số và chữ thiếu.

**Chấm bài viết ngắn lớp 3 (VietBai.jsx · chamviet.js · functions/chamviet.js)**

1 lời gọi LLM, trả JSON {diem, khen, loi[], choBoMe}. Câu sửa chứa từ chưa học → bị GIẤU (boQua) chứ không được yêu cầu viết lại. Chưa chạy vòng thật lần nào (tiep_theo_tienganh.md §2).

**Phụ đạo (PhuDao.jsx · lib/phudao.js · lantruyen.js · doThi.js)**

Tìm nút gốc rễ bằng lan truyền α/β trên đồ thị tri thức (thuần code, không LLM). Lấy câu TĨNH trước; LLM chỉ gọi khi kho tĩnh thiếu — và thực tế chưa có đường gọi nào được nối (grep: chỉ 2 callable luyenNoi · chamViet). Tức là phụ đạo hiện 100% tĩnh.

**Thích ứng (bkt.js · zpd.js · chinhsach.js · hoso.js · cefr.js · onlai.js · ara.js)**

BKT P(L) θ=0,85; xếp câu theo ZPD; chính sách π 3 nhánh; hồ sơ định dạng; Leitner 1-3-7-14-30; A-R-A đo ΔC theo mẫu prompt. Toàn bộ là luật thuần, rất tốt về kiểm soát — nhưng KHÔNG mô-đun nào đưa tri thức này vào lời dặn cho LLM, trừ `dongHoSo` (sở thích + định dạng yếu).

**Nội dung tĩnh (tools/sinh_bai_tienganh.py, sinh_dochieu, sinh_vietbai, kịch bản nói…)**

Sinh offline bằng Python + 83 cổng kiểm. Không có LLM trong dây chuyền sinh; 'không bịa câu tiếng Anh' là luật cứng. Hội thoại (HoiThoai.jsx) đi theo kịch bản viết sẵn.


### B. VÌ SAO CẢM GIÁC 'KHÔNG THÔNG MINH' — 6 nguyên nhân gốc đọc ra từ code

**1. AI chỉ là 'lớp diễn đạt' (Bậc 0)**

Mọi quyết định sư phạm (nói từ nào, kiểu việc gì, khi nào khen/sửa) do code xoay vòng cứng. LLM không được nhìn thấy bé vừa nói gì (chỉ nhận điểm + chữ thiếu), không có kế hoạch buổi, không có trí nhớ. → Thiếu: Plan-and-Execute, Memory-augmented.

**2. Cổng soi là CỬA CHẶN, không phải VÒNG SỬA**

`soiCau()` / `soiLoiCham()` / `loiVietHopLe()` bác câu là xong → rơi về câu đóng sẵn. Chính câu đóng sẵn ('Con nghe rồi nói lại…') là thứ bé thấy lặp đi lặp lại, thành 'máy'. Dữ liệu kiểm (lý do bác: lap / oTrong / ngoaiVon) đã có sẵn nhưng không được gửi ngược cho mô hình. → Thiếu: Evaluator–Optimizer.

**3. Một prompt 10 luật gánh mọi tình huống**

Bé im lặng, bé nói tiếng Việt, bé hỏi lại 'cô ơi X là gì', bé nói sai thứ tự, bé nhầm dog/duck — tất cả đi chung một lời dặn 2–8 nghìn ký tự. Mô hình làm 'đều đều' cho an toàn. → Thiếu: Routing (phân loại lượt bé rồi mới chọn nhánh prompt chuyên biệt, mỗi nhánh ngắn).

**4. Tri thức thích ứng không chạm tới AI**

P(L) từng nút, nút gốc rễ, hồ sơ định dạng, hộp Leitner, ΔC… đều có, nhưng lời dặn chỉ mang vốn từ + 1 sở thích. AI không biết bé yếu mẫu câu nào, hay nhầm cặp từ nào, lần trước đã học gì. → Thiếu: Memory-augmented + Blackboard (trạng thái bé thành một 'bảng' mà mọi lời dặn đọc được).

**5. Phụ đạo tĩnh, không chẩn đoán bằng ngôn ngữ**

Nút gốc rễ chọn bằng α^bước × (1−P(L)) rồi bốc 4 câu bậc thấp. Không ai 'nói' cho bé/bố mẹ biết vì sao bé sai và vì sao học lại chỗ này. → Thiếu: Agentic RAG trên đồ thị + Reflexion (ghi 'bài học' bằng lời).

**6. Không học từ chính mình**

`ara.js` đo được ΔC theo mẫu prompt, nhưng vòng tối ưu prompt chưa đóng; không có cơ chế tự ghi 'lượt này hỏng vì…' để lượt sau/buổi sau tránh. → Thiếu: Reflexion (trong buổi và giữa các buổi), Evaluator offline.


### C. KẾT LUẬN NHANH

**Áp dụng được: 11/18 mẫu**

6 mẫu LÀM NGAY (Evaluator–Optimizer · Routing · Memory-augmented · Plan-and-Execute · Prompt Chaining · Human-in-the-loop) + 5 mẫu NÊN LÀM / CÂN NHẮC (Agentic RAG · Reflexion · Parallelization · Blackboard · ReAct cho lớp 3+).

**Chỉ dùng OFFLINE (dây chuyền sinh nội dung): 4 mẫu**

Supervisor–Workers · CodeAct · ToT/LATS · Debate — tốn kém, không được chạy lúc bé đang học; dùng để sinh & soát kịch bản/đọc hiểu/phụ đạo rồi đóng thành dữ liệu tĩnh.

**Không nên dùng: 3 mẫu**

ReWOO · LLMCompiler · Hierarchical · Swarm/Handoff(cho lớp 1) — không có nhiều tool độc lập, độ trễ hiện đã do 1 lời gọi quyết định, hệ không rộng tới mức cần nhiều tầng.

**Nguyên tắc giữ nguyên**

Đúng tinh thần tài liệu §8.3: leo thang từng bậc. Hiện đang ở Bậc 0; đích hợp lý là Bậc 1 (workflow có vòng sửa + định tuyến) cho lớp 1–2, Bậc 2–3 (ReAct ngắn + bộ nhớ + kế hoạch) cho phòng nói lớp 3+. KHÔNG lên Bậc 4 (multi-agent) lúc chạy. Mọi câu AI sinh ra vẫn phải qua `soiCau()` — mẫu mới chỉ thay cách XỬ LÝ khi soi trượt, không bỏ cổng.

**Chi phí**

Routing dùng model nhỏ/rẻ (hoặc regex) nên ~0; Evaluator–Optimizer chỉ tốn thêm khi soi trượt (ước <30% lượt); Memory & Plan là 1 lời gọi đầu buổi. Tổng tăng ước 1,3–1,8× so với hiện tại, đổi lại bỏ được phần lớn câu đóng sẵn.


## §2 · ĐÁNH GIÁ 18 MẪU (+ Human-in-the-loop)

Chú giải *Kết luận*: **Làm ngay** = áp dụng được ngay, lợi ích rõ, rẻ · **Nên làm** = áp dụng được, cần nền (#13/#18) · **Cân nhắc** = chỉ lớp 3+ hoặc khi mẫu rẻ hơn không đủ · **Chỉ offline** = dùng lúc dựng nội dung, không chạy khi bé học · **Không** = không phù hợp.

### Bảng tóm tắt

| # | Nhóm | Mẫu | Kết luận | Ưu tiên | Độ khó | GĐ | Áp dụng vào |
|---|---|---|---|---|---|---|---|
| 1 | A. Workflow | Prompt Chaining | Làm ngay | Cao | Thấp | GĐ 1 | Chấm bài viết · Sinh bài phụ đạo · Dây chuyền sinh nội dung (kịch bản nói, đọc hiểu, video) |
| 2 | A. Workflow | Routing | Làm ngay | Cao | Thấp | GĐ 1 | Phòng luyện nói (lượt của bé) · Chính sách π · Chọn model theo nhánh |
| 3 | A. Workflow | Parallelization | Nên làm | Trung bình | Thấp | GĐ 2 | Soát nội dung offline · Chấm viết (2 góc nhìn) · Chấm nói khi STT mơ hồ |
| 4 | A. Workflow | Evaluator–Optimizer | Làm ngay | Cao | Thấp | GĐ 1 | Phòng luyện nói (câu của cô) · Chấm bài viết (câu sửa) · Phụ đạo LLM · Lời tiếng Việt |
| 5 | B. Single-agent | ReAct | Cân nhắc | Trung bình | Trung bình | GĐ 3 | Phòng nói TỰ DO cho lớp 3+ (sau khi xong kịch bản) · Trợ lý 'hỏi cô' trong bài đọc hiểu |
| 6 | B. Single-agent | Plan-and-Execute | Làm ngay | Cao | Trung bình | GĐ 2 | Buổi luyện nói · Buổi ôn tập (thẻ đến hạn) · Bài phụ đạo |
| 7 | B. Single-agent | ReWOO | Không | Thấp | — | — | — |
| 8 | B. Single-agent | LLMCompiler | Không | Thấp | — | — | — |
| 9 | B. Single-agent | Reflexion | Nên làm | Trung bình | Trung bình | GĐ 2 | Phòng nói (trong buổi + giữa các buổi) · Tối ưu prompt theo ΔC (ara.js) · Phụ đạo |
| 10 | B. Single-agent | ToT / LATS | Chỉ offline | Thấp | Cao | GĐ 3 | Sinh kịch bản hội thoại / bài phụ đạo CHẤT LƯỢNG CAO (offline) |
| 11 | B. Single-agent | CodeAct | Chỉ offline | Thấp | — | — | Công cụ rà soát/sinh nội dung (tools/*.py, *.mjs) — đã làm bằng Claude Code |
| 12 | B. Single-agent | Agentic RAG | Nên làm | Trung bình | Trung bình | GĐ 2 | Phụ đạo (chẩn đoán trên đồ thị tri thức) · Nhánh 'bé hỏi lại' · Gợi ý trong bài đọc hiểu |
| 13 | B. Single-agent | Memory-augmented (MemGPT) | Làm ngay | Cao | Trung bình | GĐ 1 | Phòng luyện nói · Chấm viết · Phụ đạo · Ôn tập — mọi chỗ có lời dặn |
| 14 | C. Multi-agent | Supervisor–Workers | Chỉ offline | Thấp | Cao | GĐ 3 | Xưởng sinh nội dung theo unit (từ mới · mẫu câu · kịch bản · đọc hiểu · video) cho lớp 4–5 và các quyển mới |
| 15 | C. Multi-agent | Hierarchical | Không | Thấp | — | — | — |
| 16 | C. Multi-agent | Swarm / Handoff | Cân nhắc | Thấp | Cao | GĐ 3+ | Phòng nói tự do lớp 3+ (sau khi có Routing) |
| 17 | C. Multi-agent | Debate | Chỉ offline | Thấp | Trung bình | GĐ 3 | Soát 'tự nhiên / hợp tuổi' của nội dung sinh tự động (một phần nhỏ, khó quyết) |
| 18 | C. Multi-agent | Blackboard | Nên làm | Trung bình | Trung bình | GĐ 1–2 | Kiến trúc trạng thái bé dùng chung cho mọi mô-đun thích ứng (không nhất thiết nhiều LLM) |
| 19 | D. Cắt ngang | Human-in-the-loop | Làm ngay | Cao | Thấp | GĐ 1 | Điểm AI chấm vào học bạ · Nội dung LLM sinh ra (phụ đạo, kịch bản) · Bộ nhớ về bé · Đổi phiên bản prompt |


### Chi tiết từng mẫu


#### #1 · Prompt Chaining  (A. Workflow) — **Làm ngay** · ưu tiên Cao · độ khó Thấp · GĐ 1

**Ý tưởng:** Chia việc thành chuỗi bước cố định; đầu ra bước trước là đầu vào bước sau; chèn cổng kiểm bằng code giữa các mắt xích.


**Áp dụng vào chức năng:** Chấm bài viết · Sinh bài phụ đạo · Dây chuyền sinh nội dung (kịch bản nói, đọc hiểu, video)


**Hiện trạng trong code:** functions/chamviet.js: 1 prompt làm cả 4 việc (tìm lỗi, viết câu sửa, khen, giải thích cho bố mẹ) → mô hình hay trộn, câu sửa dùng từ ngoài vốn rồi bị giấu. tools/*.py: sinh nội dung bằng rule, không có LLM.


**Cách áp dụng cụ thể:** CHẤM VIẾT thành 3 mắt xích: (1) LLM liệt kê lỗi dạng JSON {câu, loại lỗi, vị trí} — không sửa; (2) code lọc lỗi thuộc phạm vi vốn/mẫu câu đã học; (3) LLM viết câu sửa + lời khen CHỈ với bảng vốn ↔ cổng `soiLoiCham` ↔ nếu trượt quay lại (3) với lý do (xem Evaluator–Optimizer); (4) LLM nhỏ viết lời cho bố mẹ. OFFLINE: chuỗi sinh kịch bản hội thoại: dàn ý bước → cổng 'đủ N bước, đúng vốn' → viết câu → cổng `soiCau` → viết lời Việt → cổng `loiVietHopLe`.


**Tác dụng cho bé / trải nghiệm:** Lời chấm đủ 4 phần, không còn mục bị giấu; mỗi bước hẹp nên ít bịa; bé nhận câu sửa dùng đúng từ đã học. Kịch bản nói phong phú hơn 16 kịch bản tay mà vẫn qua cổng.


**Chi phí · độ trễ · rủi ro:** Online: 3–4 lời gọi thay vì 1 cho một bài viết (bé viết 5 bài/quyển → không đáng kể). Offline: chi phí 0 lúc chạy. Rủi ro: lỗi bước 1 lan xuống — chặn bằng cổng code giữa các bước (đã có sẵn hàm soi).



#### #2 · Routing  (A. Workflow) — **Làm ngay** · ưu tiên Cao · độ khó Thấp · GĐ 1

**Ý tưởng:** Bộ phân loại (model nhỏ hoặc rule) gắn nhãn đầu vào rồi chuyển sang nhánh có prompt/tool/model riêng.


**Áp dụng vào chức năng:** Phòng luyện nói (lượt của bé) · Chính sách π · Chọn model theo nhánh


**Hiện trạng trong code:** lib/phongnoi.js `loiDan()`: MỘT lời dặn 10 luật + 8b/8c cho mọi tình huống; `viecTiepTheo` xoay vòng theo số lượt, không nhìn lượt bé. `chinhsach.js` đã là một router 3 nhánh (tiep/vuotAi/phuDao) nhưng chỉ dẫn tới màn hình, không dẫn tới prompt.


**Cách áp dụng cụ thể:** Thêm bước PHÂN LOẠI LƯỢT BÉ trước khi gọi cô giáo máy: nhãn = {đúng · sai_thiếu_từ · sai_thứ_tự · nhầm_từ_cạnh_tranh (dog/duck từ `chamnoi`) · nói_tiếng_Việt · hỏi_lại · im_lặng · lạc_đề}. Nhãn 1–4 và 7 lấy THẲNG từ `datNoi()`/`chamnoi` (code, 0 chi phí); 5–6–8 dùng regex dấu tiếng Việt + model nhỏ (llama-3.1-8b trên Groq, ~100 token). Mỗi nhãn một lời dặn NGẮN (≤ 600 ký tự) và một kiểu việc: 'sửa 1 lỗi' / 'khen rồi nâng' / 'trả lời câu hỏi bằng vốn' / 'gợi lại bằng tiếng Việt'. Router cũng chọn model: nhánh khen/gợi dùng model nhỏ, nhánh sửa lỗi dùng 120b.


**Tác dụng cho bé / trải nghiệm:** Cô giáo phản ứng ĐÚNG việc bé vừa làm thay vì đi tiếp theo lịch cứng — đây là thứ làm bé thấy 'cô hiểu mình'. Trả lời được khi bé hỏi lại. Lời dặn ngắn → mô hình tuân luật tốt hơn, ít lặp.


**Chi phí · độ trễ · rủi ro:** +1 lời gọi nhỏ hoặc 0 (phần lớn nhãn có sẵn từ chấm nói). Rủi ro: phân loại sai → nhánh sai; giảm bằng ngưỡng tin cậy và nhánh mặc định = nhánh hiện tại. Cần 8 lời dặn thay vì 1 → thêm 8 cổng kiểm bằng node.



#### #3 · Parallelization  (A. Workflow) — **Nên làm** · ưu tiên Trung bình · độ khó Thấp · GĐ 2

**Ý tưởng:** Chạy nhiều lời gọi đồng thời rồi gộp (chia phần) hoặc bỏ phiếu (cùng việc chạy nhiều lần).


**Áp dụng vào chức năng:** Soát nội dung offline · Chấm viết (2 góc nhìn) · Chấm nói khi STT mơ hồ


**Hiện trạng trong code:** `ara.js` và các cổng chỉ kiểm bằng rule. Chấm viết 1 lần, không có góc nhìn thứ hai. Phụ đạo LLM (nếu nối) không có bỏ phiếu.


**Cách áp dụng cụ thể:** OFFLINE (giá trị nhất): mỗi câu/kịch bản sinh ra chạy 3 'giám khảo' song song — (a) đúng vốn & mẫu câu, (b) tự nhiên với người bản ngữ, (c) hợp tuổi 6–8 — chặn khi ≥2 phiếu bác; thay cho việc bác tự nhìn từng câu. ONLINE: chấm bài viết tách 2 lời gọi song song 'tìm lỗi' và 'tìm điểm khen' rồi gộp bằng code — độ trễ không đổi, nhận xét kỹ hơn. Chấm nói: khi điểm 5–7 (vùng mơ hồ) chạy 2 lời gọi 'bé nói giống từ nào hơn' rồi lấy đa số.


**Tác dụng cho bé / trải nghiệm:** Nội dung sinh tự động đáng tin hơn → cho phép dùng LLM sinh nhiều hơn mà vẫn an toàn. Lời chấm viết cân (có khen cụ thể, không chỉ lỗi).


**Chi phí · độ trễ · rủi ro:** Token ×3 cho mỗi câu soát offline — chấp nhận vì chạy một lần. Online chỉ dùng cho bài viết (ít). Rủi ro: các nhánh mâu thuẫn → tổng hợp bằng code theo luật ưu tiên, không bằng LLM.



#### #4 · Evaluator–Optimizer  (A. Workflow) — **Làm ngay** · ưu tiên Cao · độ khó Thấp · GĐ 1

**Ý tưởng:** LLM sinh → LLM/code chấm theo tiêu chí → gửi nhận xét về cho bên sinh sửa; lặp tới khi đạt hoặc hết vòng.


**Áp dụng vào chức năng:** Phòng luyện nói (câu của cô) · Chấm bài viết (câu sửa) · Phụ đạo LLM · Lời tiếng Việt


**Hiện trạng trong code:** ĐÃ CÓ sẵn Evaluator rất tốt: `soiCau()` trả {ok, duong, bac: rong|lap|oTrong|ngoaiVon}, `loiVietHopLe()`, `soiLoiCham()`. NHƯNG khi trượt thì rơi thẳng về `cauThayThe()` (câu đóng sẵn) hoặc giấu mục (boQua) — KHÔNG có vòng Optimizer. Đây là chỗ sinh ra cảm giác 'máy' rõ nhất.


**Cách áp dụng cụ thể:** Nối vòng: soi trượt → gọi lại mô hình với lời nhắn ngắn ghép từ `bac` ('Câu vừa rồi lặp y lượt trước, đổi từ trong ô trống' / 'Câu chứa từ "chips" ngoài bảng, chỉ dùng: …' / 'Ô [Month B] chưa điền') — tối đa 2 vòng, rồi MỚI rơi về `cauThayThe`. Làm tương tự ở `soiLoiCham` (câu sửa có chữ lạ → yêu cầu viết lại bằng bảng vốn, thay vì giấu) và ở lời tiếng Việt (xưng hô sai → sửa). Thêm Evaluator LLM nhẹ cho tiêu chí mà rule không đo được: 'lời Việt có nói về ĐÚNG câu này không hay chung chung' (luật 8c) — chấm 0/1, chỉ chạy khi rule qua.


**Tác dụng cho bé / trải nghiệm:** Giảm mạnh số lượt rơi về câu đóng sẵn (nguyên nhân #2 ở sheet 1) → cô giáo máy bớt lặp, lời Việt bám vào câu bé vừa nói. Bài viết không còn gợi ý bị cắt. Có thể đo ngay bằng cổng: tỉ lệ `cauThayThe` được dùng trước/sau.


**Chi phí · độ trễ · rủi ro:** Chỉ tốn thêm khi trượt (ước 10–30% lượt) → +0,2–0,6 lời gọi/lượt, thêm ~1–2 s khi phải sửa. Rủi ro: vòng không hội tụ → trần 2 vòng là bắt buộc; evaluator dễ dãi → giữ rule cứng làm evaluator chính, LLM chỉ phụ.



#### #5 · ReAct  (B. Single-agent) — **Cân nhắc** · ưu tiên Trung bình · độ khó Trung bình · GĐ 3

**Ý tưởng:** LLM xen kẽ suy luận và gọi tool trong vòng lặp; dừng khi có câu trả lời hoặc chạm giới hạn bước.


**Áp dụng vào chức năng:** Phòng nói TỰ DO cho lớp 3+ (sau khi xong kịch bản) · Trợ lý 'hỏi cô' trong bài đọc hiểu


**Hiện trạng trong code:** Không có tool nào cho mô hình; mọi dữ liệu nhét sẵn vào lời dặn. Lớp 1–2 không cần (vốn 60 từ, tool thừa). Lớp 3 (204 từ, 43 mẫu, bài đọc hiểu) bắt đầu có việc đáng để mô hình tự tra.


**Cách áp dụng cụ thể:** Chỉ cho LỚP 3+: cô giáo máy có 4–5 tool hẹp, mô tả rõ: `tra_tu(tu)` (nghĩa, IPA, câu ví dụ từ kho), `mau_cau_cua_unit`, `muc_thao(nut)` (P(L) từ BKT), `nghe_lai(clip)`, `ghi_nho(ghi_chu)`. Trần 3 bước/lượt, phát hiện lặp, cắt gọn kết quả tool. Dùng khi bé HỎI ('cô ơi, "kitchen" là gì?', 'con nói thế đúng chưa?') — router (mẫu #2) mới rẽ vào nhánh này; lượt thường vẫn đi workflow 1 lời gọi.


**Tác dụng cho bé / trải nghiệm:** Bé lớp 3 hỏi được và được trả lời bằng dữ liệu thật của kho (không bịa nghĩa); cô 'tra' trước khi nói nên ít sai.


**Chi phí · độ trễ · rủi ro:** n+1 lời gọi/lượt, độ trễ 3–8 s trên Groq — chấp nhận được vì chỉ ở nhánh hỏi. Rủi ro: trôi mục tiêu → giới hạn bước, `soiCau` vẫn soi câu cuối. Tốn công viết tool + cổng.



#### #6 · Plan-and-Execute  (B. Single-agent) — **Làm ngay** · ưu tiên Cao · độ khó Trung bình · GĐ 2

**Ý tưởng:** Planner lập kế hoạch nhiều bước; Executor làm từng bước; Replanner sửa phần còn lại theo kết quả.


**Áp dụng vào chức năng:** Buổi luyện nói · Buổi ôn tập (thẻ đến hạn) · Bài phụ đạo


**Hiện trạng trong code:** `viecTiepTheo` chọn việc theo công thức xoay vòng, `tinhBuoi` chỉ có 3 ngưỡng (20 phút, 3 đạt liền, 3 kém liền). `buocTiepTheo` đi theo kịch bản tĩnh. Không có 'kế hoạch buổi' nào bé hay bố mẹ nhìn thấy. `onlai.js` chọn câu cho thẻ ôn nhưng không xếp thành buổi.


**Cách áp dụng cụ thể:** Đầu buổi: PLANNER (1 lời gọi, model mạnh, hoặc thậm chí CODE) nhận bảng trạng thái (P(L) từng nút, nhóm ZPD, thẻ Leitner đến hạn, lỗi gần nhất, sở thích) → trả KẾ HOẠCH 5–7 bước dạng JSON {bước, nút, kiểu việc, lý do ngắn tiếng Việt}. EXECUTOR = đúng vòng 1 lời gọi hiện có, mỗi bước một việc. REPLANNER = code: bé sai 2 lần liền ở một bước → hạ bậc (mau → tu) hoặc chèn bước phụ đạo; đạt 3 liền → bỏ bước luyện lại. Kế hoạch hiện lên màn hình: 'Hôm nay mình làm 5 việc: ① nghe 2 từ cũ · ② nói câu mới …' — tiến độ nhìn thấy được.


**Tác dụng cho bé / trải nghiệm:** Buổi học có đầu-giữa-cuối, không 'nói mãi không hết' (hiện phòng nói 'không bao giờ hết câu'). Bé thấy đường đi và đích, bố mẹ thấy vì sao hôm nay học cái này. Kế hoạch dùng được TRI THỨC THÍCH ỨNG đang nằm chết (nguyên nhân #4).


**Chi phí · độ trễ · rủi ro:** +1 lời gọi đầu buổi (hoặc 0 nếu planner viết bằng code — khuyến nghị bắt đầu bằng code vì mọi đầu vào đã có cấu trúc). Rủi ro: kế hoạch sai vì P(L) sai → giữ lưới đỡ `dandat.js` (2 lần thử là được đi), replan tối đa 2 lần/buổi.



#### #7 · ReWOO  (B. Single-agent) — **Không** · ưu tiên Thấp · độ khó — · —

**Ý tưởng:** Planner viết cả kế hoạch một lần với biến giữ chỗ; Worker chạy hết tool; Solver trả lời. Chỉ 2 lời gọi LLM.


**Áp dụng vào chức năng:** —


**Hiện trạng trong code:** Không có chuỗi tra cứu nhiều tool. Mọi dữ liệu (vốn, mẫu câu, P(L)) đã nằm ở máy con dưới dạng JSON tĩnh.


**Cách áp dụng cụ thể:** Không áp dụng. Lợi thế của ReWOO là bớt vòng gửi lịch sử khi có nhiều tool; ở đây đã 1 lời gọi/lượt và client tự cắt lịch sử (`LUOT_GUI_TOI_DA = 12`). Nếu sau này ReAct lớp 3 (mẫu #5) tốn quá, mới xét ReWOO cho nhánh 'hỏi cô'.


**Tác dụng cho bé / trải nghiệm:** —


**Chi phí · độ trễ · rủi ro:** Không mang lại gì so với hiện trạng; thêm độ phức tạp.



#### #8 · LLMCompiler  (B. Single-agent) — **Không** · ưu tiên Thấp · độ khó — · —

**Ý tưởng:** Planner sinh DAG lời gọi tool, chạy song song các tác vụ độc lập, Joiner quyết định trả lời/lập lại.


**Áp dụng vào chức năng:** —


**Hiện trạng trong code:** Độ trễ hiện tại = 1 lời gọi Groq (+ phần reasoning). Không có 'nhiều tra cứu độc lập' cần song song.


**Cách áp dụng cụ thể:** Không áp dụng lúc chạy. Phần song song hữu ích đã được mẫu #3 (Parallelization bằng code) phủ cho offline.


**Tác dụng cho bé / trải nghiệm:** —


**Chi phí · độ trễ · rủi ro:** Cài đặt phức tạp nhất nhóm, lợi ích ≈ 0.



#### #9 · Reflexion  (B. Single-agent) — **Nên làm** · ưu tiên Trung bình · độ khó Trung bình · GĐ 2

**Ý tưởng:** Sau lần thử thất bại, agent tự viết bài học bằng ngôn ngữ tự nhiên, lưu lại, đọc ở lần thử sau.


**Áp dụng vào chức năng:** Phòng nói (trong buổi + giữa các buổi) · Tối ưu prompt theo ΔC (ara.js) · Phụ đạo


**Hiện trạng trong code:** `buocSua` cho sửa tối đa 2 lần nhưng không ghi 'vì sao bé sai'. `ara.js` đo ΔC theo `phienBanMau` nhưng không có vòng nào đọc kết quả để sửa prompt. Không có chỗ nào lưu 'bài học về bé'.


**Cách áp dụng cụ thể:** HAI TẦNG. (a) VỀ BÉ: cuối mỗi bước thất bại (sai ≥2) hoặc cuối buổi, 1 lời gọi nhỏ viết 1–2 dòng 'bài học' tiếng Việt cho cô ('Bo hay bỏ "a" trước danh từ; nhầm dog↔duck; nói tốt hơn khi được gợi bằng tiếng Việt trước') → lưu vào hồ sơ (mẫu #13) → ghép vào lời dặn buổi sau. (b) VỀ PROMPT: job offline đọc ΔC từ `gomTheoMau`, với mẫu kém nhất gọi LLM 'đọc 20 buổi thất bại, đề xuất 1 sửa đổi lời dặn' → người duyệt (HITL) → tăng `phienBanMau`. Đóng vòng 2.5.3 của luận văn.


**Tác dụng cho bé / trải nghiệm:** Cô giáo máy 'nhớ' bé sai kiểu gì và nhắc đúng chỗ ở buổi sau — khác hẳn mỗi buổi bắt đầu từ số 0. Prompt được cải tiến có bằng chứng (ΔC) thay vì cảm tính.


**Chi phí · độ trễ · rủi ro:** +1 lời gọi nhỏ/buổi. Rủi ro lớn nhất theo tài liệu: 'phản tư sai làm lệch các lần sau' → bài học phải NGẮN, có hạn dùng (ví dụ 5 buổi), và bị ghi đè khi bé đã thạo (P(L) ≥ 0,85) nút liên quan. Không ghi gì về cảm xúc/đánh giá bé.



#### #10 · ToT / LATS  (B. Single-agent) — **Chỉ offline** · ưu tiên Thấp · độ khó Cao · GĐ 3

**Ý tưởng:** Sinh nhiều hướng ở mỗi bước, chấm, mở rộng hướng tốt, quay lui khi bế tắc.


**Áp dụng vào chức năng:** Sinh kịch bản hội thoại / bài phụ đạo CHẤT LƯỢNG CAO (offline)


**Hiện trạng trong code:** Kịch bản nói (16·153 bước lớp 1 … 21·346 lớp 3) viết tay + rule; không có tìm kiếm.


**Cách áp dụng cụ thể:** OFFLINE thôi: khi sinh kịch bản hội thoại cho một unit, sinh 3–4 biến thể mỗi bước, chấm bằng cổng (`soiCau`, độ dài, số từ mới/bước, không lặp) + giám khảo LLM, giữ 2 nhánh tốt nhất đi tiếp (beam search). Kết quả đóng thành JSON tĩnh như hiện nay.


**Tác dụng cho bé / trải nghiệm:** Kịch bản tự nhiên, ít lặp mẫu hơn mà vẫn 100% trong vốn. Bé không thấy gì khác về cơ chế, chỉ thấy nội dung hay hơn.


**Chi phí · độ trễ · rủi ro:** Đắt nhất nhóm (b×d×2 lời gọi); chỉ chạy lúc dựng. Không bao giờ dùng lúc bé đang học — độ trễ không chấp nhận được.



#### #11 · CodeAct  (B. Single-agent) — **Chỉ offline** · ưu tiên Thấp · độ khó — · —

**Ý tưởng:** LLM viết code chạy trong sandbox thay cho từng lời gọi tool JSON.


**Áp dụng vào chức năng:** Công cụ rà soát/sinh nội dung (tools/*.py, *.mjs) — đã làm bằng Claude Code


**Hiện trạng trong code:** Dây chuyền sinh/soát đã là Python/Node (83 cổng, `do_an_toan_noi_dung.mjs`, `soi_ban_ghi_tienganh.mjs`). Đây chính là CodeAct do con người điều khiển.


**Cách áp dụng cụ thể:** Không đưa vào app. Chỉ dùng như hiện tại (Claude Code viết/chạy script rà kho dữ liệu, đối chiếu lớp 1–5). Tuyệt đối không cho mô hình chạy code lúc bé học (không sandbox, không lợi ích).


**Tác dụng cho bé / trải nghiệm:** Giúp bác soát dữ liệu nhanh, gián tiếp tăng chất lượng bài.


**Chi phí · độ trễ · rủi ro:** Cần sandbox; rủi ro bảo mật nếu mở ra runtime.



#### #12 · Agentic RAG  (B. Single-agent) — **Nên làm** · ưu tiên Trung bình · độ khó Trung bình · GĐ 2

**Ý tưởng:** Agent tự quyết có truy xuất không, nguồn nào, chấm tài liệu lấy về, viết lại truy vấn khi chưa đủ.


**Áp dụng vào chức năng:** Phụ đạo (chẩn đoán trên đồ thị tri thức) · Nhánh 'bé hỏi lại' · Gợi ý trong bài đọc hiểu


**Hiện trạng trong code:** ĐÃ CÓ 'kho': `doThi.js` (1194 nút, 253 cạnh), `lantruyen.js` (nút gốc rễ), `baiCuaNut`, kho câu tĩnh theo nút. Truy xuất hiện là một lượt cứng: nút gốc rễ = argmax doNgo → bốc 4 câu bậc thấp. Không có bước 'chấm xem câu lấy về có đúng chỗ hổng không' và không có 'tìm lại'.


**Cách áp dụng cụ thể:** Thêm 2 điểm quyết định vào `dungPhuDao`: (1) GRADER — LLM (hoặc rule mạnh hơn) chấm từng câu tĩnh lấy về: 'câu này có luyện ĐÚNG nút gốc rễ X không, hay chỉ chứa từ của X?' → bỏ câu không trúng; (2) RE-QUERY — nếu còn < 4 câu, lấy nút gốc rễ thứ hai trong danh sách `nutGocRe` (đã xếp sẵn theo doNgo) hoặc nới sang bài tiên quyết; chỉ khi vẫn thiếu mới sinh câu bằng LLM rồi qua `cauHopLe`. Kèm 1 dòng chẩn đoán tiếng Việt cho bé/bố mẹ: 'Con sai câu đếm sách vì số đếm từ unit 2 chưa chắc — mình ôn số trước nhé'. Nhánh HỎI LẠI (router #2): mô hình phải tra `tra_tu` trước khi trả lời, có nghĩa thật trong kho thì mới nói.


**Tác dụng cho bé / trải nghiệm:** Phụ đạo trúng chỗ hổng thật → ΔC tăng (đo được bằng `ara.js`). Bé và bố mẹ hiểu VÌ SAO phải học lại — biến 'thích ứng' từ con số ẩn thành lời nói ra. Trả lời câu hỏi của bé không bịa.


**Chi phí · độ trễ · rủi ro:** 2–4 lời gọi mỗi lần phụ đạo (chỉ khi bé sai 3 liền → hiếm). Rủi ro: tìm mãi → trần 2 vòng; chấm nhầm câu → giữ `cauHopLe` sau cùng, và đường lùi tĩnh như hiện nay.



#### #13 · Memory-augmented (MemGPT)  (B. Single-agent) — **Làm ngay** · ưu tiên Cao · độ khó Trung bình · GĐ 1

**Ý tưởng:** Context = RAM, kho ngoài = đĩa; agent tự ghi/tìm/sửa bộ nhớ để làm việc qua nhiều phiên và cá nhân hoá.


**Áp dụng vào chức năng:** Phòng luyện nói · Chấm viết · Phụ đạo · Ôn tập — mọi chỗ có lời dặn


**Hiện trạng trong code:** Máy chủ 'không lưu gì' (bác chốt 13-08) — đúng cho riêng tư, nhưng MÁY CON cũng chỉ nhớ: sở thích 1 từ (`hoSo.thich`), tỉ lệ đúng theo định dạng (`hoso.js`), và P(L) trên Firestore. `dongHoSo()` chỉ ghép 2 dòng vào lời dặn. Buổi nói chuyện lưu `phongNoiTA/{uid}/buoi` nhưng không buổi nào đọc lại buổi trước. → mỗi buổi cô giáo máy gặp bé như lần đầu.


**Cách áp dụng cụ thể:** Dựng HỒ SƠ BÉ có cấu trúc (giữ nguyên nguyên tắc client giữ, Firestore theo uid, server không lưu): {tên, sở thích (mở rộng từ 1 lên 3–5), vật nuôi/người thân bé đã kể, 5 lỗi lặp lại gần nhất, cặp từ hay nhầm, định dạng bé hợp, nút đang chông chênh (ZPD) kèm nhãn, bài học Reflexion (#9), câu bé đã nói ĐÚNG gần nhất, lần cuối học}. Mỗi phần có trần ký tự và hạn dùng. `loiDan()` nhận hồ sơ này thành 5–8 dòng 'ABOUT THIS CHILD'. Ghi bộ nhớ = CODE (từ `chamnoi`, `buocSua`, điểm) + 1 lời gọi tóm tắt cuối buổi; KHÔNG cho mô hình tự do ghi. Hiển thị cho bố mẹ ở Góc bố mẹ + nút xoá.


**Tác dụng cho bé / trải nghiệm:** Cá nhân hoá thật: 'Hôm qua con nói "I like fish" rất hay, hôm nay thử "I like milk" nhé'; cô nhớ bé hay bỏ 'a'. Đây là thứ tách 'gia sư' khỏi 'máy đọc thẻ'. Cũng là đầu vào cho Planner (#6).


**Chi phí · độ trễ · rủi ro:** 0–1 lời gọi/buổi. Rủi ro theo tài liệu: bộ nhớ cũ/sai → hạn dùng, bị xoá khi P(L) vượt ngưỡng, bố mẹ xoá được; riêng tư → chỉ lưu dữ liệu học, không lưu lời nói thô, đúng luật Firestore hiện có.



#### #14 · Supervisor–Workers  (C. Multi-agent) — **Chỉ offline** · ưu tiên Thấp · độ khó Cao · GĐ 3

**Ý tưởng:** Một agent điều phối phân rã việc, giao cho worker có context riêng, tổng hợp lại.


**Áp dụng vào chức năng:** Xưởng sinh nội dung theo unit (từ mới · mẫu câu · kịch bản · đọc hiểu · video) cho lớp 4–5 và các quyển mới


**Hiện trạng trong code:** Sinh nội dung hiện là script Python chạy tuần tự do bác điều khiển. Lớp 4–5 tiếng Anh chưa có nội dung.


**Cách áp dụng cụ thể:** OFFLINE: Supervisor nhận bản đồ tri thức của 1 unit → tạo 4 worker (mỗi worker 1 loại nội dung, context riêng, prompt riêng, chỉ trả JSON tóm tắt) → mỗi worker tự đi chuỗi sinh + cổng (#1, #4, #3) → Supervisor ghép thành `ta4/unitXX.json` → HITL (#18) duyệt → chạy 83 cổng → deploy tĩnh. App lúc chạy không đổi gì.


**Tác dụng cho bé / trải nghiệm:** Rút ngắn thời gian dựng quyển mới (lớp 4–5) trong khi giữ nguyên chất lượng cổng; bé hưởng nội dung đều tay hơn.


**Chi phí · độ trễ · rủi ro:** Tốn token ×10–15 (tài liệu §5) nhưng chạy một lần cho mỗi quyển. Rủi ro: worker làm trùng/sót → giao việc theo schema JSON cố định, không mô tả tự do.



#### #15 · Hierarchical  (C. Multi-agent) — **Không** · ưu tiên Thấp · độ khó — · —

**Ý tưởng:** Supervisor nhiều tầng như sơ đồ tổ chức; mỗi tầng chỉ thấy tóm tắt tầng dưới.


**Áp dụng vào chức năng:** —


**Hiện trạng trong code:** Hệ gồm 1 môn, 5 quyển, 4–5 loại nội dung — một supervisor (#14) quản đủ.


**Cách áp dụng cụ thể:** Không áp dụng. Tài liệu nói rõ: chỉ dùng khi Supervisor một tầng đã chứng minh là thiếu.


**Tác dụng cho bé / trải nghiệm:** —


**Chi phí · độ trễ · rủi ro:** Đắt nhất, khó debug nhất; thông tin méo qua tầng tóm tắt — tệ nhất với nội dung cho trẻ cần 100% trong vốn.



#### #16 · Swarm / Handoff  (C. Multi-agent) — **Cân nhắc** · ưu tiên Thấp · độ khó Cao · GĐ 3+

**Ý tưởng:** Không có điều phối trung tâm; agent đang giữ lượt chuyển cả hội thoại cho agent chuyên môn hơn.


**Áp dụng vào chức năng:** Phòng nói tự do lớp 3+ (sau khi có Routing)


**Hiện trạng trong code:** Hội thoại lớp 1–3 đi theo kịch bản tĩnh hoặc việc do máy con chọn; không có 'nhiều chuyên môn' thật.


**Cách áp dụng cụ thể:** Chỉ xét ở lớp 3+ nếu Routing (#2) tỏ ra không đủ: 3 'cô' nhỏ — cô dạy mẫu câu, cô sửa phát âm (có tool `nghe_lai`, từ cạnh tranh), cô kể chuyện ngắn (đọc hiểu) — chuyển lượt bằng tool `chuyen_cho(...)`. Mỗi cô một lời dặn ngắn. Với lớp 1–2: KHÔNG, Routing bằng code là đủ và kiểm soát được.


**Tác dụng cho bé / trải nghiệm:** Giọng điệu đa dạng hơn, mỗi 'cô' làm một việc sâu. Nhưng phần lớn lợi ích đã đạt được bằng Routing rẻ hơn.


**Chi phí · độ trễ · rủi ro:** Rủi ro chính theo tài liệu: chuyển lòng vòng, không ai giữ bức tranh toàn cục — với trẻ 6–8 tuổi là rủi ro trải nghiệm lớn. Thêm độ trễ mỗi lần chuyển.



#### #17 · Debate  (C. Multi-agent) — **Chỉ offline** · ưu tiên Thấp · độ khó Trung bình · GĐ 3

**Ý tưởng:** Nhiều agent độc lập đưa câu trả lời, phản biện nhau vài vòng, trọng tài chốt.


**Áp dụng vào chức năng:** Soát 'tự nhiên / hợp tuổi' của nội dung sinh tự động (một phần nhỏ, khó quyết)


**Hiện trạng trong code:** Việc duyệt nội dung hiện do bác quyết bằng mắt sau khi cổng rule xanh.


**Cách áp dụng cụ thể:** OFFLINE, chỉ cho các câu/kịch bản mà 3 giám khảo song song (#3) chia phiếu 2–1: cho 2 agent (ủng hộ / phản đối) tranh luận 2 vòng, trọng tài tổng hợp lý do → đưa cho bác quyết (HITL). Không dùng để sinh nội dung, không dùng online.


**Tác dụng cho bé / trải nghiệm:** Bác chỉ phải nhìn những câu thật sự khó quyết, kèm lý do hai phía.


**Chi phí · độ trễ · rủi ro:** a×r+1 lời gọi/câu; chỉ chạy trên phần nhỏ. Rủi ro: cùng model đồng thuận sai → dùng 2 model khác nhau cho 2 phía.



#### #18 · Blackboard  (C. Multi-agent) — **Nên làm** · ưu tiên Trung bình · độ khó Trung bình · GĐ 1–2

**Ý tưởng:** Các agent cùng đọc/ghi lên một bảng trạng thái chung; bộ điều khiển chọn agent kế tiếp theo trạng thái bảng.


**Áp dụng vào chức năng:** Kiến trúc trạng thái bé dùng chung cho mọi mô-đun thích ứng (không nhất thiết nhiều LLM)


**Hiện trạng trong code:** Trạng thái bé đang RẢI ở nhiều chỗ: `progressTA` (sổ), `mastery/{uid}/units` (P(L)), `hoSo` (định dạng, sở thích), `reviewQueue` (Leitner), lịch sử buổi nói (`phongNoiTA`), ΔC (`ara`). Mỗi mô-đun đọc một phần; lời dặn LLM đọc gần như không gì. Đây là một blackboard chưa được gọi tên.


**Cách áp dụng cụ thể:** Gom thành MỘT đối tượng `bangTrangThai(uid)` (thuần JS, cổng kiểm được): {P(L) theo nút, nhóm ZPD, nút gốc rễ gần nhất, thẻ ôn đến hạn, hồ sơ (#13), bài học (#9), kế hoạch buổi (#6), lượt gần nhất + nhãn router (#2)}. Mọi 'tác nhân' — chính sách π, planner, lời dặn phòng nói, chấm viết, phụ đạo — đọc và ghi qua đúng đối tượng này; bộ điều khiển = `chinhsach.js` mở rộng. Lúc đầu không thêm LLM nào; sau này mỗi tác nhân có thể thành 1 lời gọi riêng mà không phải nối dây lại.


**Tác dụng cho bé / trải nghiệm:** Là nền để 5 mẫu 'Làm ngay' dùng CHUNG một nguồn sự thật về bé; tránh hai mô-đun kết luận ngược nhau về cùng một bé.


**Chi phí · độ trễ · rủi ro:** Chi phí = công tái cấu trúc, 0 token. Rủi ro: bảng phình to → trần kích thước, hàm `tomTat()` cắt cho lời dặn; xung đột ghi → mọi ghi qua hàm thuần, có cổng.



#### #19 · Human-in-the-loop  (D. Cắt ngang) — **Làm ngay** · ưu tiên Cao · độ khó Thấp · GĐ 1

**Ý tưởng:** Điểm dừng chờ người duyệt/sửa trước hành động rủi ro; cần checkpoint và giao diện đủ ngữ cảnh.


**Áp dụng vào chức năng:** Điểm AI chấm vào học bạ · Nội dung LLM sinh ra (phụ đạo, kịch bản) · Bộ nhớ về bé · Đổi phiên bản prompt


**Hiện trạng trong code:** Điểm AI đã gắn nhãn `nguon:'ai'` và vào sổ ngay. Góc bố mẹ chỉ ĐỌC. Bảng cô giáo (`teacherboard.js`) có nhưng `bangCoGiao` của môn TA trả null. Không có hàng đợi 'chờ duyệt' nào.


**Cách áp dụng cụ thể:** 4 điểm duyệt: (1) ĐIỂM AI — vào sổ ở trạng thái 'tạm', bố mẹ/cô bấm 'đồng ý' hoặc sửa 1 chạm trong Góc bố mẹ; (2) CÂU LLM SINH (phụ đạo #12, kịch bản #10/#14) — nằm ở hàng đợi `choDuyetTA`, người duyệt chấp nhận thì đóng vào kho tĩnh → lần sau không cần LLM nữa (kho tự lớn, có kiểm); (3) BỘ NHỚ VỀ BÉ (#13) — bố mẹ xem/xoá được; (4) ĐỔI PROMPT theo đề xuất Reflexion (#9) — người tăng `phienBanMau`. Nguyên tắc tài liệu: duyệt ít mà đúng chỗ, không duyệt mọi lượt nói chuyện.


**Tác dụng cho bé / trải nghiệm:** Niềm tin của bố mẹ vào điểm số và vào thứ AI nói với con; kho câu phụ đạo lớn dần từ câu AI đã qua tay người → càng dùng càng ít gọi LLM, càng nhanh.


**Chi phí · độ trễ · rủi ro:** Thông lượng bị giới hạn bởi người duyệt → chỉ đặt ở hành động KHÔNG hoàn tác được (điểm vào sổ, nội dung đóng vào kho, prompt production). Cần lưu trạng thái chờ (Firestore đã đủ).



## §3 · TỔ HỢP MẪU THEO TỪNG CHỨC NĂNG


### Phòng luyện nói (lớp 1–2)

**Hiện nay:** Bậc 0: 1 lời gọi, việc do code xoay vòng, soi trượt → câu đóng sẵn


**Đích đề xuất:** Bậc 1 (workflow có vòng sửa)


**Tổ hợp mẫu:** Blackboard #18 → Plan-and-Execute #6 (planner = code) → Routing #2 → Evaluator–Optimizer #4 → Memory #13 → Reflexion #9


**Luồng mới:** ĐẦU BUỔI: đọc bảng trạng thái → kế hoạch 5–7 bước (code) → hiện cho bé. MỖI LƯỢT: chấm lời bé (`chamnoi`) → nhãn lượt (code/regex, model nhỏ nếu cần) → chọn lời dặn ngắn theo nhãn + 5 dòng hồ sơ → 1 lời gọi → `soiCau` + `loiVietHopLe` → trượt thì gửi lý do, gọi lại ≤2 → vẫn trượt mới `cauThayThe` → replanner (code) chỉnh bước còn lại. CUỐI BUỔI: 1 lời gọi nhỏ viết bài học → hồ sơ (bố mẹ xem/xoá được).


**Số lời gọi LLM ước tính:** 1,2–1,6 / lượt + 1 / buổi (hiện 1,0)


**Cái bé thấy khác:** Cô biết hôm nay làm gì và còn mấy việc; cô phản ứng đúng cái bé vừa nói; cô nhớ bé; gần như không còn câu 'Con nghe rồi nói lại… nhé' lặp.



### Phòng luyện nói (lớp 3+)

**Hiện nay:** Như lớp 1 + kịch bản `buocTiepTheo`


**Đích đề xuất:** Bậc 2 (ReAct ngắn ở nhánh hỏi)


**Tổ hợp mẫu:** Tổ hợp trên + ReAct #5 (4–5 tool, trần 3 bước) ở nhánh 'bé hỏi lại' · (sau) Swarm #16 nếu cần


**Luồng mới:** Router rẽ 'hỏi_lại' → vòng ReAct: tra_tu / mau_cau / muc_thao / nghe_lai → câu trả lời qua `soiCau`. Lượt thường đi luồng lớp 1.


**Số lời gọi LLM ước tính:** 1,2–1,6 thường; 3–4 ở nhánh hỏi


**Cái bé thấy khác:** Bé hỏi 'kitchen là gì' được trả lời bằng nghĩa/ví dụ thật của kho, kèm nút nghe clip.



### Chấm bài viết ngắn (lớp 3)

**Hiện nay:** Bậc 0: 1 lời gọi, mục chứa từ lạ bị giấu


**Đích đề xuất:** Bậc 1


**Tổ hợp mẫu:** Prompt Chaining #1 → Parallelization #3 (lỗi ∥ khen) → Evaluator–Optimizer #4 → HITL #19


**Luồng mới:** (1) tìm lỗi ∥ tìm điểm khen → (2) code lọc theo vốn → (3) viết câu sửa + gợi ý chỉ bằng bảng vốn → `soiLoiCham` → trượt thì gọi lại với từ lạ bị nêu tên ≤2 → (4) lời cho bố mẹ → điểm vào sổ trạng thái 'AI chấm – chờ bố mẹ xác nhận'.


**Số lời gọi LLM ước tính:** 3–5 / bài (bé viết 5 bài/quyển)


**Cái bé thấy khác:** Lời chấm đầy đủ, không mất mục; bố mẹ xác nhận 1 chạm; câu sửa dùng đúng từ con đã học.



### Phụ đạo

**Hiện nay:** Bậc 0 (thuần code, không LLM, câu tĩnh)


**Đích đề xuất:** Bậc 1–2


**Tổ hợp mẫu:** Agentic RAG #12 trên đồ thị (`doThi`, `lantruyen`) → Evaluator #4 (`cauHopLe`) → HITL #19 (đóng câu AI vào kho) → Reflexion #9 (ΔC)


**Luồng mới:** Nút gốc rễ → lấy câu tĩnh → GRADER chấm 'có luyện đúng nút không' → thiếu thì nút gốc rễ #2 / bài tiên quyết → vẫn thiếu mới sinh LLM → `cauHopLe` → câu AI vào hàng đợi duyệt, duyệt xong thành tĩnh. Kèm 1 câu chẩn đoán tiếng Việt cho bé/bố mẹ. A-R-A đo ΔC → job offline gợi ý sửa prompt.


**Số lời gọi LLM ước tính:** 0–4 / lần phụ đạo (hiếm: chỉ khi sai 3 liền)


**Cái bé thấy khác:** Bé được nói rõ 'vì sao học lại chỗ này'; bài vá trúng hơn; kho câu vá tự lớn.



### Ôn tập ngắt quãng (thẻ Leitner)

**Hiện nay:** Bậc 0: chọn câu từ bài của thẻ (`onlai.js`)


**Đích đề xuất:** Bậc 1


**Tổ hợp mẫu:** Plan-and-Execute #6 + Memory #13


**Luồng mới:** Planner gom thẻ đến hạn + nút chông chênh thành 1 buổi ôn 5 phút có thứ tự (ZPD trước, yếu sau), cô giáo máy đọc lời dẫn cá nhân hoá ('hôm nay ôn 3 từ con hay quên: …').


**Số lời gọi LLM ước tính:** 0–1 / buổi


**Cái bé thấy khác:** Ôn tập có 'buổi' thật, không phải danh sách thẻ.



### Đọc hiểu · Hội thoại kịch bản · Video

**Hiện nay:** Tĩnh, viết tay + rule


**Đích đề xuất:** Giữ tĩnh lúc chạy; nâng bậc OFFLINE


**Tổ hợp mẫu:** Supervisor–Workers #14 → Prompt Chaining #1 → ToT #10 (kịch bản) → Parallelization #3 (3 giám khảo) → Debate #17 (câu 2–1) → HITL #19 → 83 cổng


**Luồng mới:** Xưởng offline sinh unit cho lớp 4–5 và làm phong phú lớp 1–3; mọi thứ qua cổng rule + giám khảo + bác duyệt rồi mới đóng JSON.


**Số lời gọi LLM ước tính:** 0 lúc chạy


**Cái bé thấy khác:** Nội dung nhiều, đều, tự nhiên hơn; app vẫn offline-first và không phí API.



### Hồ sơ / Góc bố mẹ / Bảng cô giáo

**Hiện nay:** Đọc sổ, `bangCoGiao` TA = null


**Đích đề xuất:** —


**Tổ hợp mẫu:** Blackboard #18 + Memory #13 + HITL #19


**Luồng mới:** Một bảng trạng thái cho mọi mô-đun; Góc bố mẹ hiện bộ nhớ AI về bé + nút xoá + nút xác nhận điểm; bảng cô giáo đọc được cả tiếng Anh.


**Số lời gọi LLM ước tính:** 0


**Cái bé thấy khác:** Bố mẹ hiểu AI 'nghĩ' gì về con và kiểm soát được.



## §4 · 9 ĐIỂM YẾU QUAN SÁT ĐƯỢC & CÁCH VÁ


### Y1 · Soi trượt → rơi thẳng về câu đóng sẵn, không gọi lại

**Bằng chứng trong code:** lib/phongnoi.js `cauThayThe()` ('Con nghe rồi nói lại từ … nhé'); PhongNoi.jsx gọi `cauHopLe` rồi thay; `soiCau` đã trả `bac` (rong/lap/oTrong/ngoaiVon) nhưng không ai gửi lại cho mô hình.


**Hệ quả với bé:** Chính câu đóng sẵn là câu bé nghe lặp nhiều nhất → cảm giác 'máy'.


**Mẫu vá:** #4 Evaluator–Optimizer


**Việc cụ thể:** Trong `goiPhongNoi.hoiCoGiao`: nếu `soiCau(...).ok === false` → đẩy thêm 1 lượt user 'Your last sentence was rejected: <lý do từ bac, kèm bảng vốn>' rồi gọi lại, tối đa `SUA_TOI_DA_CO = 2`; ghi `lanSua` vào bản ghi buổi. Thêm cổng node đo tỉ lệ dùng `cauThayThe`.


**Cách đo trước/sau:** Tỉ lệ lượt dùng `cauThayThe` (mục tiêu: từ ~? xuống < 5%); số lượt bị `bac:'lap'`.



### Y2 · Một lời dặn cho mọi tình huống; việc chọn theo số lượt, không theo lượt bé

**Bằng chứng trong code:** `loiDan()` 10 luật + 8b/8c; `viecTiepTheo`: `kieu = vong[cuaCo.length % vong.length]` — kiểu việc phụ thuộc SỐ LƯỢT CỦA CÔ, không phụ thuộc bé nói đúng/sai/im/hỏi.


**Hệ quả với bé:** Bé nói sai thứ tự từ vẫn được chuyển sang việc mới theo lịch; bé hỏi lại thì bị 'steer back'.


**Mẫu vá:** #2 Routing


**Việc cụ thể:** Viết `nhanLuot(luotBe, chamNoi, lichSu)` → 8 nhãn; bảng `LOI_DAN_THEO_NHAN` (8 lời dặn ≤600 ký tự); `viecTiepTheo` nhận nhãn làm đầu vào (sai → lặp lại cùng việc với gợi ý; đúng → nâng). Cổng node: mỗi nhãn có đúng 1 lời dặn và đều qua `locKhung`.


**Cách đo trước/sau:** Phân phối nhãn/buổi; tỉ lệ bé nói đúng ở lượt kế sau khi bị sửa.



### Y3 · AI không có trí nhớ giữa các buổi; chỉ 1 sở thích

**Bằng chứng trong code:** `hoso.js` (định dạng + `thich`), `dongHoSo()` 2 dòng; `luuBuoi` ghi `phongNoiTA/{uid}/buoi` nhưng không có hàm đọc lại.


**Hệ quả với bé:** Mỗi buổi là lần đầu gặp; không nhắc lại thứ bé đã làm tốt/kém.


**Mẫu vá:** #13 Memory + #9 Reflexion


**Việc cụ thể:** Schema `hoSoAI` trong `hoso.js` (trần 1.200 ký tự, mỗi mục có `hetHan`); hàm thuần `capNhatHoSo(hoSo, buoi)` từ dữ liệu chấm; 1 lời gọi `tomTatBuoi` cuối buổi (JSON 3 trường); `loiDan` thêm khối ABOUT THIS CHILD; Góc bố mẹ hiển thị + xoá.


**Cách đo trước/sau:** Số buổi có nhắc lại chính xác nội dung buổi trước (đọc log); phản hồi bố mẹ.



### Y4 · Tri thức thích ứng (P(L), ZPD, gốc rễ, Leitner) không vào lời dặn và không thành kế hoạch buổi

**Bằng chứng trong code:** `zpd.js`, `chinhsach.js`, `lantruyen.js`, `onlai.js` chỉ nối tới màn hình; `tinhBuoi` 3 ngưỡng cứng; phòng nói 'không bao giờ hết câu'.


**Hệ quả với bé:** Buổi học không có đích; cô không biết bé yếu nút nào.


**Mẫu vá:** #6 Plan-and-Execute + #18 Blackboard


**Việc cụ thể:** `bangTrangThai(uid)` thuần JS gom 6 nguồn; `lapKeHoachBuoi(bang)` thuần code trả 5–7 bước; `PhongNoi.jsx` hiện thanh bước; `replan` khi sai 2 liền/đạt 3 liền; lời dặn mang 'bước này luyện nút X vì P(L)=0,42'.


**Cách đo trước/sau:** Thời lượng buổi trung bình; tỉ lệ buổi kết thúc bằng 'xong kế hoạch' thay vì hết 20 phút.



### Y5 · Chấm viết: mục có từ lạ bị giấu thay vì viết lại

**Bằng chứng trong code:** `goiChamViet.nhoCham`: `soiLoiCham` → `boQua` → màn hình nói 'bỏ vì có từ chưa học'.


**Hệ quả với bé:** Bé mất đúng gợi ý sửa lỗi của mình.


**Mẫu vá:** #1 Chaining + #4 E-O


**Việc cụ thể:** Tách `loiDanCham` thành 3 prompt; sau `soiLoiCham` nếu `boQua.length` → gọi lại bước 3 với 'Rewrite using ONLY: …; you used: <từ lạ>' ≤2 lần.


**Cách đo trước/sau:** `LOI_CHU_LA.so` trước/sau; số bài có mục bị bỏ.



### Y6 · Phụ đạo 100% tĩnh, không chẩn đoán bằng lời, chưa có đường LLM thật

**Bằng chứng trong code:** `phudao.js` 'LLM chỉ gọi khi kho tĩnh thiếu' nhưng grep chỉ thấy 2 callable (luyenNoi, chamViet); `PhuDao.jsx` không gọi mạng.


**Hệ quả với bé:** Bé được 4 câu 'tự nhiên xuất hiện', không hiểu vì sao; nếu kho thiếu thì phụ đạo rỗng.


**Mẫu vá:** #12 Agentic RAG + #19 HITL


**Việc cụ thể:** Cloud function `sinhPhuDao` (cùng khuôn luyenNoi, không lưu); grader câu tĩnh; re-query nút gốc rễ #2; câu LLM → `cauHopLe` → `choDuyetTA`; 1 dòng chẩn đoán tiếng Việt lấy từ `nhanNut` + lý do.


**Cách đo trước/sau:** ΔC theo `ara.gomTheoMau` trước/sau; số lần phụ đạo 'khongCo'.



### Y7 · Điểm AI vào sổ ngay, không có điểm duyệt; bảng cô giáo TA = null

**Bằng chứng trong code:** `chamviet.js` `nguon:'ai'`; `index.js` `bangCoGiao: async () => null`.


**Hệ quả với bé:** Bố mẹ/cô không có cách nói 'điểm này sai'.


**Mẫu vá:** #19 HITL


**Việc cụ thể:** Trường `trangThai: 'tam'|'xacNhan'` ở mục `viet` trong `hocBaTA`; nút xác nhận/sửa ở GocBoMe; nối `teacherboard.js` đọc attempts tiếng Anh.


**Cách đo trước/sau:** % điểm được xác nhận; số lần bố mẹ sửa điểm.



### Y8 · Vòng tối ưu prompt chưa đóng dù đã đo ΔC

**Bằng chứng trong code:** `ara.js` `mauTotNhat()` có, nhưng không job nào gọi và không ai đọc.


**Hệ quả với bé:** Prompt sửa theo cảm tính (lịch sử 13-08, 14-08, 18-08 trong chú thích).


**Mẫu vá:** #9 Reflexion (offline)


**Việc cụ thể:** Script `tools/doc_delta_c.mjs` chạy tay/định kỳ: gom cặp A-R-A → với mẫu kém, gọi LLM đề xuất 1 sửa → in ra cho bác duyệt → tăng `phienBanMau`.


**Cách đo trước/sau:** ΔC trung bình theo phiên bản prompt tăng dần theo thời gian.



### Y9 · Chấm nói chỉ so chuỗi; vùng điểm 5–7 mơ hồ

**Bằng chứng trong code:** `chamnoi.js` tiền xử lý + so khớp + từ cạnh tranh; Web Speech en-GB.


**Hệ quả với bé:** Bé nói đúng nhưng STT lệch → bị trừ; bé nhầm từ → đôi khi vẫn qua.


**Mẫu vá:** #3 Parallelization (bỏ phiếu) — chỉ khi mơ hồ


**Việc cụ thể:** Khi `diem` trong [5,7]: 2 lời gọi nhỏ song song 'transcript này gần từ nào hơn trong {đích, cạnh tranh}' → đa số → điều chỉnh ±1 và câu nhận xét.


**Cách đo trước/sau:** Tỉ lệ bé bấm 'nói lại' sau điểm 5–7; khớp với đánh giá tay trên 50 mẫu.



## §5 · LỘ TRÌNH


### GĐ 1 — Hết 'máy' (2–3 tuần)

**Mục tiêu:** Bỏ phần lớn câu đóng sẵn; cô phản ứng đúng lượt bé; cô nhớ bé; điểm AI có duyệt


**Mẫu áp dụng:** #4 Evaluator–Optimizer · #2 Routing · #13 Memory · #1 Chaining (chấm viết) · #19 HITL · #18 Blackboard (bước 1)


**Việc chính:** 1) Vòng gọi lại ≤2 ở phòng nói + chấm viết. 2) `nhanLuot` + 8 lời dặn ngắn. 3) `hoSoAI` + ABOUT THIS CHILD + Góc bố mẹ. 4) Tách chấm viết 3 mắt xích. 5) Điểm AI trạng thái 'tạm' + xác nhận. 6) `bangTrangThai` gom nguồn (chưa thêm LLM).


**Điều kiện xong (cổng kiểm):** Cổng node: tỉ lệ `cauThayThe` < 5% trên bộ mô phỏng 200 lượt; mỗi nhãn có đúng 1 lời dặn qua `locKhung`; hồ sơ ≤ trần, có hạn dùng; `tienganh_chamviet.test` thêm ca 'từ lạ → viết lại'. 74 tệp kiểm hiện có vẫn 0 FAIL.


**Ước lượng công:** ~10–15 ngày công


**Phụ thuộc:** Khoá Groq trên production để thử vòng thật (đang chưa thử — tiep_theo §2)



### GĐ 2 — Có kế hoạch & chẩn đoán (3–4 tuần)

**Mục tiêu:** Buổi học có đích; phụ đạo trúng chỗ hổng và nói được vì sao; AI học từ ΔC


**Mẫu áp dụng:** #6 Plan-and-Execute · #12 Agentic RAG · #9 Reflexion · #3 Parallelization (chấm viết, chấm nói mơ hồ)


**Việc chính:** 1) `lapKeHoachBuoi` (code) + thanh bước + replanner. 2) Cloud function `sinhPhuDao` + grader + re-query + hàng đợi duyệt. 3) `tomTatBuoi` cuối buổi → bài học → lời dặn buổi sau. 4) Script `doc_delta_c` đề xuất sửa prompt. 5) Chấm viết lỗi ∥ khen; bỏ phiếu chấm nói 5–7.


**Điều kiện xong (cổng kiểm):** Mô phỏng 50 bé giả lập: ≥90% buổi kết thúc 'xong kế hoạch'; ΔC trung bình > 0 với ≥5 cặp hợp lệ; câu LLM phụ đạo 100% qua `cauHopLe` trước khi hiện.


**Ước lượng công:** ~15–20 ngày công


**Phụ thuộc:** GĐ 1 (hồ sơ + bảng trạng thái)



### GĐ 3 — Lớp 3+ và xưởng nội dung (song song, không chặn)

**Mục tiêu:** Bé lớp 3 hỏi được cô; dựng lớp 4–5 nhanh mà vẫn 100% trong vốn


**Mẫu áp dụng:** #5 ReAct (nhánh hỏi) · #14 Supervisor–Workers · #10 ToT · #17 Debate · #3 (3 giám khảo) — 4 mẫu sau OFFLINE


**Việc chính:** 1) 4–5 tool hẹp + vòng ReAct trần 3 bước cho nhánh 'hỏi_lại'. 2) Xưởng offline: supervisor theo unit → worker → chuỗi + cổng → giám khảo song song → debate cho câu 2–1 → bác duyệt → 83 cổng → JSON tĩnh.


**Điều kiện xong (cổng kiểm):** ReAct: không lượt nào vượt 3 bước, câu cuối qua `soiCau`. Xưởng: 100% câu qua cổng, tỉ lệ bác bác bỏ < 10%.


**Ước lượng công:** ~20+ ngày công


**Phụ thuộc:** GĐ 1–2; Groq cho model nhỏ; thời gian duyệt của bác



### KHÔNG LÀM

**Mục tiêu:** —


**Mẫu áp dụng:** #7 ReWOO · #8 LLMCompiler · #15 Hierarchical · #16 Swarm (lớp 1–2) · #11 CodeAct trong app


**Việc chính:** Giữ nguyên nguyên tắc: nội dung tĩnh lúc chạy, server không lưu, mọi câu AI qua cổng, không multi-agent lúc bé học.


**Điều kiện xong (cổng kiểm):** —


**Ước lượng công:** —


**Phụ thuộc:** —



## §6 · BẢNG ĐIỂM ƯU TIÊN

Điểm = Tác dụng × Phù hợp ÷ Chi phí (chấm chủ quan của người review; ≥10 nên làm sớm, <3 không nên làm).

| Hạng | # | Mẫu | Tác dụng | Phù hợp | Chi phí | Điểm | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Routing | 5 | 5 | 1 | 25 | Nhãn lấy sẵn từ chấm nói; lời dặn ngắn. Thay đổi trải nghiệm lớn nhất với chi phí nhỏ nhất. |
| 2 | 1 | Prompt Chaining | 4 | 5 | 1 | 20 | Chấm viết tách bước; offline chuỗi sinh. Rẻ, dễ kiểm. |
| 2 | 6 | Plan-and-Execute | 5 | 4 | 1 | 20 | Planner bằng code vì đầu vào đã có cấu trúc; LLM chỉ diễn đạt. Cho buổi học cái đích. |
| 2 | 13 | Memory-augmented | 5 | 4 | 1 | 20 | Client giữ, server không lưu — hợp quy ước; hồ sơ có trần và hạn dùng. |
| 2 | 18 | Blackboard | 4 | 5 | 1 | 20 | Tái cấu trúc trạng thái, 0 token; nền cho các mẫu khác. |
| 2 | 19 | Human-in-the-loop | 4 | 5 | 1 | 20 | Duyệt ít, đúng chỗ không hoàn tác được: điểm, kho, prompt, bộ nhớ. |
| 7 | 4 | Evaluator–Optimizer | 5 | 5 | 2 | 12.5 | Evaluator đã có sẵn (soiCau…), chỉ thiếu vòng gọi lại. Chi phí chỉ khi trượt. |
| 8 | 9 | Reflexion | 4 | 4 | 2 | 8 | Bài học ngắn, có hạn dùng; đóng vòng ΔC đã đo. |
| 8 | 12 | Agentic RAG | 4 | 4 | 2 | 8 | Kho + đồ thị + nút gốc rễ đã có; thêm grader và re-query. |
| 10 | 3 | Parallelization | 3 | 4 | 2 | 6 | Giá trị chính ở soát nội dung offline; online chỉ chấm viết/chấm nói mơ hồ. |
| 11 | 5 | ReAct | 3 | 3 | 3 | 3 | Chỉ lớp 3+ nhánh hỏi; lớp 1–2 không cần tool. |
| 12 | 14 | Supervisor–Workers | 2 | 3 | 4 | 1.5 | Offline, xưởng nội dung lớp 4–5. |
| 13 | 16 | Swarm / Handoff | 2 | 2 | 4 | 1 | Lớp 3+ nếu Routing không đủ; rủi ro chuyển lòng vòng với trẻ nhỏ. |
| 13 | 17 | Debate | 2 | 2 | 4 | 1 | Offline, chỉ câu giám khảo chia phiếu. |
| 15 | 10 | ToT / LATS | 2 | 2 | 5 | 0.8 | Chỉ offline cho kịch bản; đắt. |
| 16 | 7 | ReWOO | 1 | 1 | 2 | 0.5 | Không có chuỗi tool để tiết kiệm. |
| 17 | 11 | CodeAct | 1 | 2 | 5 | 0.4 | Đã dùng qua Claude Code cho tools/; không đưa vào app. |
| 18 | 8 | LLMCompiler | 1 | 1 | 4 | 0.3 | Không có tác vụ song song lúc chạy. |
| 19 | 15 | Hierarchical | 1 | 1 | 5 | 0.2 | Hệ không đủ rộng. |


## §7 · VIỆC CHO CLAUDE CODE (V1–V12)

Đường dẫn tính từ `web/` trừ khi ghi `tools/` (gốc repo).

| Mã | GĐ | Mẫu | Tên việc | Phụ thuộc |
|---|---|---|---|---|
| V1 | GĐ 1 | #4 Evaluator–Optimizer | Vòng GỌI LẠI khi `soiCau` bác câu của cô (phòng nói) | — |
| V2 | GĐ 1 | #2 Routing | Phân loại LƯỢT CỦA BÉ → lời dặn ngắn theo nhãn | V1 |
| V3 | GĐ 1 | #13 Memory | Hồ sơ AI về bé — giữ qua nhiều buổi, bố mẹ xem/xoá | — |
| V4 | GĐ 1 | #1 Chaining + #4 E–O | Chấm bài viết 3 mắt xích + viết lại khi có từ lạ | — |
| V5 | GĐ 1 | #19 HITL | Điểm AI ở trạng thái 'tạm' — bố mẹ xác nhận/sửa | V4 |
| V6 | GĐ 1 | #18 Blackboard | `bangTrangThai(uid)` — một nguồn sự thật về bé cho mọi mô-đun | V3 |
| V7 | GĐ 2 | #6 Plan-and-Execute | Kế hoạch buổi (planner = code) + thanh bước + replanner | V2, V6 |
| V8 | GĐ 2 | #9 Reflexion | Bài học cuối buổi (1 lời gọi) + job ΔC đề xuất sửa prompt | V3 |
| V9 | GĐ 2 | #12 Agentic RAG | Phụ đạo có grader + re-query + chẩn đoán bằng lời + đường LLM thật | V6 |
| V10 | GĐ 2 | #3 Parallelization | Chấm viết 'lỗi ∥ khen'; chấm nói mơ hồ bỏ phiếu | V4 |
| V11 | GĐ 3 | #5 ReAct | Nhánh 'hỏi lại' lớp 3+ với 4 tool, trần 3 bước | V2, V1 |
| V12 | GĐ 3 | #14 #10 #17 #3 offline | Xưởng sinh nội dung offline (supervisor → worker → cổng → giám khảo → duyệt) | — |


### V1 · Vòng GỌI LẠI khi `soiCau` bác câu của cô (phòng nói)

*GĐ 1 · #4 Evaluator–Optimizer · phụ thuộc: —*


**Tệp SỬA:**

```
src/mon/tienganh/lib/phongnoi.js
src/mon/tienganh/lib/goiPhongNoi.js
src/mon/tienganh/components/PhongNoi.jsx (chỉ đọc `tra.lanSua` để ghi log)
```


**Tệp TẠO MỚI:**

```
—
```


**Hàm / hằng mới (chữ ký):**

```
phongnoi.js:
  export const SUA_CO_TOI_DA = 2;
  export function loiNhacSua(bac, { von, cauTruoc, en }) → string  // từ `bac` của soiCau dựng 1 lượt user ngắn (≤300 ký tự) bằng TIẾNG ANH cho mô hình
  export function loiNhacSuaViet(kq, { von }) → string  // từ `loiVietHopLe(...).vi` (lý do) dựng lời nhắc sửa lời Việt

goiPhongNoi.js:
  export const LOI_SUA_CO = { so: 0, thanh: 0, ganNhat: null };  // đếm để đo
  async function goiMay(messages) → {data}  // tách phần httpsCallable ra hàm riêng để tiêm giả trong test
  export async function hoiCoGiao(..., { goi = goiMay } = {})  // thêm tham số tiêm
```


**Các bước làm (theo thứ tự):**

1) Trong `phongnoi.js` viết `loiNhacSua(bac, ctx)`: map lý do → câu nhắc:  
   rong → 'Your reply had no English sentence. Reply as JSON with one English sentence using only the allowed words.'  
   lap → `You repeated your previous sentence "${cauTruoc}". Say a DIFFERENT sentence: change the word in the slot.`  
   oTrong → 'Your sentence still contains an unfilled [slot]. Fill every slot with an allowed word or the child\'s name.'  
   ngoaiVon → `Your sentence used a word outside the allowed list: ${tuLa.join(', ')}. Allowed words: ${…}. Rewrite.` (lấy từ lạ bằng `tuTrongCau`)  
2) Trong `goiPhongNoi.hoiCoGiao`, nhánh KHÔNG kịch bản (sau dòng `if (!cauHopLe(tra.en, …))`): thay vì gọi `cauThayThe` ngay, lặp tối đa `SUA_CO_TOI_DA` lần: push `{role:'assistant', content: JSON.stringify({en: tra.en, vi: tra.vi})}` + `{role:'user', content: loiNhacSua(...)}` vào `messages`, gọi lại `goi(messages)`, `docTraLoi`, `soiCau` lại. Qua → dùng câu mới, `tra.lanSua = n`. Hết vòng vẫn trượt → `cauThayThe` như cũ, `tra.lanSua = SUA_CO_TOI_DA`, `tra.daThay = true`.  
3) Làm tương tự cho lời Việt: `loiVietSach` hiện lui về `LUI_CHUNG`; thêm 1 vòng gọi lại với `loiNhacSuaViet` TRƯỚC khi lui (chỉ 1 vòng, vì câu Anh đã đúng).  
4) Nhánh CÓ kịch bản (`buoc`) không cần vòng cho câu Anh (đã ép về `dung`), nhưng ÁP vòng cho lời Việt.  
5) Tăng `LOI_SUA_CO.so` mỗi lần phải gọi lại, `thanh` khi gọi lại thành công; log DEV như `LOI_LUU`.  
6) Máy chủ `luyennoi.js`: KHÔNG đổi luật; chỉ kiểm `TOI_DA_LUOT=24` đủ chỗ cho +4 lượt sửa (12 lịch sử + 1 system + 4 = 17 < 24 ✓).


**Ràng buộc KHÔNG được phá:**

- Server vẫn không lưu gì.  
- Vòng có trần cứng `SUA_CO_TOI_DA = 2`; cổng phải canh hằng này.  
- KHÔNG bỏ `cauThayThe` — nó là đường lùi cuối.  
- Lượt sửa KHÔNG được ghi vào `lichSu` hiển thị (bé không thấy cô 'nói nhầm'); chỉ ghi `lanSua` vào bản ghi buổi (`luuBuoi`).  
- Lời nhắc sửa là role `user`, không chèn system thứ hai (`soiGoi` bác system ở vị trí ≠0).


**Tệp kiểm & lệnh chạy:**

SỬA: test/tienganh_phongnoi.test.mjs (thêm 4 test cho `loiNhacSua`)  
TẠO: test/tienganh_sua_co.test.mjs — tiêm `goi` giả trả lần 1 câu lặp, lần 2 câu đúng; assert `lanSua===1`, `daThay===false`, `en` là câu lần 2; và ca 'trượt cả 2 lần → cauThayThe, daThay true, lanSua 2'; ca 'đã qua ngay → không gọi lại (goi được gọi đúng 1 lần)'.  
Chạy: cd web && node test/tienganh_sua_co.test.mjs && npm test


**Định nghĩa XONG:**

- `npm test` 0 FAIL (giữ 74+ tệp).  
- Mô phỏng 200 lượt với mô hình giả 'lặp 40%': tỉ lệ `daThay` < 5% (trước: ≈40%).  
- Trên bản thật: `LOI_SUA_CO.thanh / LOI_SUA_CO.so` ≥ 0,7 sau 20 buổi.



### V2 · Phân loại LƯỢT CỦA BÉ → lời dặn ngắn theo nhãn

*GĐ 1 · #2 Routing · phụ thuộc: V1*


**Tệp SỬA:**

```
src/mon/tienganh/lib/phongnoi.js (`viecTiepTheo`, `loiDan`)
src/mon/tienganh/lib/goiPhongNoi.js (`hoiCoGiao`)
functions/src/vantay.js (`DAU_RIENG` thêm dấu hiệu dòng mới nếu dòng mang dữ liệu bé)
```


**Tệp TẠO MỚI:**

```
src/mon/tienganh/lib/nhanluot.js
src/mon/tienganh/lib/loidan_nhan.js
```


**Hàm / hằng mới (chữ ký):**

```
nhanluot.js:
  export const NHAN = { dung:'dung', thieuTu:'thieuTu', saiThuTu:'saiThuTu', nhamTu:'nhamTu', tiengViet:'tiengViet', hoiLai:'hoiLai', imLang:'imLang', lacDe:'lacDe', moDau:'moDau' };
  export function nhanLuot(luotBe, { von, datNguong = 6 }) → { nhan, doTin: 0..1, chiTiet }
     // luotBe = { chu, diem, mau, thieu, thieuChucNang, nhamThanh? } đúng hình dạng PhongNoi.jsx đang đẩy vào lichSu
loidan_nhan.js:
  export const LOI_DAN_THEO_NHAN = { [nhan]: (ctx) => string }  // mỗi cái ≤ 600 ký tự, KHÔNG chứa bảng vốn (bảng vốn vẫn ở khối chung)
  export function dongTheoNhan(nhan, ctx) → string
phongnoi.js:
  viecTiepTheo({ …, nhan })  // thêm tham số: nhan ∈ {thieuTu, saiThuTu, nhamTu} → GIỮ nguyên `tu`/`mau` của lượt trước (kieu='mau'), không xoay vòng
  loiDan({ …, nhan })  // chèn `dongTheoNhan` ngay sau khối HARD RULES, trước `dongViec`
```


**Các bước làm (theo thứ tự):**

1) Viết `nhanLuot` THUẦN CODE (không LLM):  
- !chu hoặc chu.trim()==='' → imLang  
- chưa có lượt 'may' nào → moDau  
- có dấu tiếng Việt (regex đã có ở `docTraLoi`) và kết thúc '?' hoặc chứa 'là gì|nghĩa|cô ơi' → hoiLai; chỉ dấu Việt → tiengViet  
- diem ≥ datNguong → dung  
- chamnoi trả `nhamThanh` → nhamTu (chiTiet = {dich, nham})  
- thieu.length>0 → thieuTu (chiTiet = thieu)  
- diem < datNguong && thieu rỗng && mau có → saiThuTu  
- còn lại → lacDe  
   doTin: 1.0 cho nhánh suy từ điểm/chữ thiếu; 0.6 cho regex; nhãn doTin<0.5 → coi như lacDe.  
2) Viết 9 lời dặn ngắn (xem sheet 9, mục A). Mỗi lời: VIỆC DUY NHẤT của lượt này + 1 ví dụ cấu trúc câu trả lời.  
3) `hoiCoGiao`: tính `nhan = nhanLuot(luotBeCuoi(lichSu), {von})` → truyền vào `viecTiepTheo` và `loiDan`. Nhánh kịch bản (`buoc`) giữ nguyên `dongBuoc`, chỉ thêm `dongTheoNhan` khi nhan ∈ {hoiLai, tiengViet, imLang}.  
4) GIẢM lời dặn chung: luật 7, 8, 8b, 8c chuyển thành nội dung của các nhánh tương ứng (không lặp 2 nơi).  
5) `vantay.js`: nếu `dongTheoNhan` chứa chữ bé nói / từ nhầm → thêm regex vào `DAU_RIENG` (ví dụ /child said/i, /she said/i) để không lọt vào vân tay.  
6) Ghi `nhan` vào lượt 'may' trong `lichSu` (để `luuBuoi` lưu, và để cổng đo phân phối nhãn).


**Ràng buộc KHÔNG được phá:**

- Router là CODE, không gọi mạng — 0 chi phí, kiểm được bằng node.  
- Không đổi `datNguong` (6) và không thêm ngưỡng thứ hai.  
- Lời dặn tổng (chung + nhãn) ≤ `TOI_DA_CHU_LOI_DAN` 8000 — cổng canh.  
- Không xoá luật 1–6, 9, 10 (vốn từ, 1 câu, JSON, xưng hô, trích đúng chữ).


**Tệp kiểm & lệnh chạy:**

TẠO: test/tienganh_nhanluot.test.mjs — 9 ca mỗi nhãn 1 ca (xem sheet 8); ca 'mỗi nhãn có đúng 1 lời dặn, ≤600 ký tự, không chứa chữ "bạn/em/tớ/cậu"'; ca 'loiDan có nhãn vẫn ≤ 8000 với vốn lớp 3 (204 từ)'; ca 'nhãn thieuTu → viecTiepTheo giữ nguyên mau của lượt trước'.  
SỬA: test/vantay_prompt.test.mjs — thêm ca: lời dặn có nhãn `nhamTu` (chứa chữ bé nói) → `locKhung` phải bỏ dòng ấy (vân tay 2 bé khác nhau phải BẰNG nhau).  
Chạy: cd web && node test/tienganh_nhanluot.test.mjs && node test/vantay_prompt.test.mjs


**Định nghĩa XONG:**

- 100% lượt bé có nhãn; phân phối nhãn in ra được từ `phongNoiTA` buổi.  
- Khi bé sai, lượt kế của cô nhắc ĐÚNG câu/chữ bé vừa sai (kiểm tay 10 buổi).  
- Khi bé hỏi 'X là gì', cô trả lời nghĩa từ bảng vốn (không 'steer back').



### V3 · Hồ sơ AI về bé — giữ qua nhiều buổi, bố mẹ xem/xoá

*GĐ 1 · #13 Memory · phụ thuộc: —*


**Tệp SỬA:**

```
src/mon/tienganh/lib/hoso.js
src/mon/tienganh/lib/progress.js (thêm trường `hoSoAI` vào sổ `ttd5.tienganh.v1`, gộp theo `capNhatLuc` mới hơn thắng)
src/mon/tienganh/lib/phongnoi.js (`dongHoSo` đọc thêm `hoSoAI`)
src/mon/tienganh/components/PhongNoi.jsx (ghi hồ sơ cuối buổi)
src/mon/tienganh/components/GocBoMe.jsx (hiện + nút xoá)
firestore.rules (cho `progressTA/{uid}` ghi thêm trường — kiểm bằng test/luat_firestore.test.mjs)
```


**Tệp TẠO MỚI:**

```
src/mon/tienganh/lib/hosoai.js
```


**Hàm / hằng mới (chữ ký):**

```
hosoai.js:
  export const TRAN_KY_TU = 1200; export const HAN_BUOI = 5;
  export const hoSoRong = () => ({ soThich: [], nguoiVat: [], loiLap: [], tuNham: [], cauDungGanNhat: [], baiHoc: [], buoiThu: 0, capNhatLuc: 0 });
  export function capNhatTuBuoi(hs, { lichSu, bai, bayGio }) → hs'  // THUẦN CODE từ dữ liệu chấm: loiLap từ `thieuChucNang` lặp ≥2 lần, tuNham từ `nhamThanh`, cauDungGanNhat từ lượt diem≥6 (giữ 3), soThich từ `hoSo.thich`
  export function themBaiHoc(hs, { chu, nut, buoi }) → hs'  // từ V5 (Reflexion); mỗi bài học {chu ≤160 ký tự, nut, hetHanBuoi = buoi + HAN_BUOI}
  export function donHoSo(hs, { mucThao, buoiHienTai }) → hs'  // xoá bài học hết hạn; xoá loiLap/tuNham có nut đã thạo (P(L) ≥ NGUONG_THAO); cắt về TRAN_KY_TU
  export function dongHoSoAI(hs, tenBe) → string  // ≤ 8 dòng tiếng Anh cho lời dặn, KHÔNG số, KHÔNG câu nào 'không nên đọc to' (quy ước của `dongHoSo`)
  export const xoaHoSoAI = () => hoSoRong()
```


**Các bước làm (theo thứ tự):**

1) Viết `hosoai.js` thuần, có cổng. Hình dạng cố định, mọi mảng có trần phần tử (soThich 5, nguoiVat 5, loiLap 5, tuNham 5, cauDungGanNhat 3, baiHoc 5).  
2) `progress.js`: sổ tiến độ thêm `hoSoAI` (một đối tượng/bé, không theo bài); `gopTienDo` gộp theo `capNhatLuc` lớn hơn thắng.  
3) `PhongNoi.jsx`: khi `buoi.trangThai !== 'dang'` (kết buổi) → `capNhatTuBuoi` → `donHoSo` → `luuTienDo`. KHÔNG gọi LLM ở V3 (bài học LLM là V5).  
4) `phongnoi.js` `dongHoSo`: nối thêm `dongHoSoAI(hoSo.ai, tenBe)` — giữ quy ước 'câu nào đọc to lên cũng không sao'.  
5) `GocBoMe.jsx`: mục 'Cô giáo máy đang nhớ gì về con' liệt kê bằng tiếng Việt + nút 'Xoá trí nhớ của cô' → `xoaHoSoAI` + lưu.  
6) `vantay.js` `DAU_RIENG`: thêm /ABOUT THIS CHILD/i … hoặc tốt hơn: bọc khối hồ sơ trong 2 dòng đánh dấu `<<RIENG` `RIENG>>` và `locKhung` bỏ cả khối giữa hai dấu (sửa `locKhung` + test).


**Ràng buộc KHÔNG được phá:**

- Server KHÔNG lưu gì thêm; hồ sơ nằm trong `progressTA` (đã có luật) và localStorage.  
- KHÔNG lưu lời nói thô của bé, không lưu cảm xúc/đánh giá ('bé lười'), chỉ dữ liệu học.  
- Mọi mục có hạn dùng hoặc điều kiện xoá tự động.  
- `ranh_gioi.test` vẫn xanh (không import toan).


**Tệp kiểm & lệnh chạy:**

TẠO: test/tienganh_hosoai.test.mjs — ca: trần ký tự; hết hạn bị dọn; nút thạo thì loiLap bị dọn; `dongHoSoAI` không chứa chữ số và ≤ 8 dòng; `capNhatTuBuoi` từ lichSu giả (3 lượt bé thiếu 'a' → loiLap có 'a'); gộp sổ: bản mới hơn thắng.  
SỬA: test/vantay_prompt.test.mjs (khối RIÊNG bị bỏ khỏi khung), test/luat_firestore.test.mjs (ghi `hoSoAI` được, với emulator).  
Chạy: cd web && node test/tienganh_hosoai.test.mjs && npm test


**Định nghĩa XONG:**

- Buổi thứ 2 trở đi, lời dặn có khối ABOUT THIS CHILD với ≥1 mục từ buổi trước (kiểm bằng log DEV).  
- Góc bố mẹ hiện và xoá được; sau xoá, lời dặn không còn khối ấy.



### V4 · Chấm bài viết 3 mắt xích + viết lại khi có từ lạ

*GĐ 1 · #1 Chaining + #4 E–O · phụ thuộc: —*


**Tệp SỬA:**

```
functions/src/chamviet.js
functions/index.js (callable `chamViet` nhận thêm `buoc` ∈ {timLoi, sua, boMe}; hoặc 1 callable chạy cả chuỗi phía server — CHỌN cách 2 để máy con chỉ gọi 1 lần)
src/mon/tienganh/lib/chamviet.js (`soiLoiCham` trả thêm `tuLa` theo từng mục)
src/mon/tienganh/lib/goiChamViet.js (gọi lại khi `boQua`)
functions/src/vantay.js (`PHIEN_BAN_MAU.chamviet` → 2)
```


**Tệp TẠO MỚI:**

```
—
```


**Hàm / hằng mới (chữ ký):**

```
functions/src/chamviet.js:
  export function loiDanTimLoi(goi) → string      // bước 1: CHỈ liệt kê lỗi {cau, loai ∈ chinhTa|thieuTu|thuTu|mauCau|khac, viTri} — cấm sửa
  export function loiDanSua(goi, loiDs, tuLaTruoc = []) → string   // bước 2: viết `sua` + `viSao` + `khen` + `goiY`, CHỈ dùng bảng vốn; nếu `tuLaTruoc` có → dòng 'Lần trước bạn dùng từ ngoài bảng: …, không được dùng lại'
  export function loiDanBoMe(goi, cham) → string   // bước 3: 2 câu tiếng Việt cho bố mẹ
  export const SUA_LAI_TOI_DA = 2;
  export async function chamBaiViet(du, taoClient) // chạy chuỗi 1→2→(soi chữ lạ bằng cùng luật với máy con: chuyển `chuLa` sang module dùng chung functions/src/chula.js hoặc chép + cổng so 2 bản)→2'→3; trả { chu (JSON gộp), lanSuaLai, …vanTay }
```


**Các bước làm (theo thứ tự):**

1) Chuyển hàm `chuLa(cau, vonTu)` từ `src/mon/tienganh/lib/chamviet.js` thành bản chép ở `functions/src/chula.js` (KHÔNG import chéo browser↔functions); thêm test so 2 bản giống hệt (cùng lối `tienganh_onlai.test.mjs` so `BOX_DAYS`).  
2) Tách `loiDanCham` thành 3 hàm. Bước 1 temperature 0.1, max_tokens 400; bước 2 0.2/700; bước 3 0.3/200.  
3) Trong `chamBaiViet`: sau bước 2, chạy `chuLa` trên mọi `loi[].sua` và `goiY`; có chữ lạ → gọi lại bước 2 với `tuLaTruoc`, tối đa `SUA_LAI_TOI_DA`; vẫn còn → giữ cơ chế `boQua` hiện có ở máy con (đường lùi).  
4) Máy con `goiChamViet.nhoCham` không đổi giao diện trả về; đọc thêm `lanSuaLai` để ghi vào `hocBaTA`.  
5) `khungCham` dựng từ cả 3 lời dặn ghép lại (khung = 3 khung).  
6) Tăng `PHIEN_BAN_MAU.chamviet = 2`.


**Ràng buộc KHÔNG được phá:**

- Máy chủ vẫn không lưu gì.  
- Chốt cửa `soiBaiViet` giữ nguyên.  
- `soiLoiCham` ở máy con GIỮ — là hàng rào cuối.  
- Mỗi bước có trần token riêng; tổng ≤ 1300 token trả lời.


**Tệp kiểm & lệnh chạy:**

SỬA: test/tienganh_chamviet.test.mjs — thêm: 'lời dặn bước 1 CẤM sửa' (regex 'không sửa'); 'bước 2 có dòng tuLaTruoc khi truyền'; 'chamBaiViet với client giả: lần 1 trả sua có "delicious" (ngoài vốn) → gọi lại; lần 2 sạch → lanSuaLai===1 và kết quả không còn boQua'; 'trượt 2 lần → trả về với chữ lạ, máy con boQua như cũ'.  
TẠO: test/chula_hai_ban.test.mjs — 2 bản `chuLa` cho cùng 30 đầu vào ra cùng kết quả.  
Chạy: cd web && node test/tienganh_chamviet.test.mjs && node test/chula_hai_ban.test.mjs


**Định nghĩa XONG:**

- `LOI_CHU_LA.so` trên 20 bài thật giảm về ≈0.  
- Lời chấm luôn đủ 5 trường; không mục nào bị giấu khi mô hình hợp tác.



### V5 · Điểm AI ở trạng thái 'tạm' — bố mẹ xác nhận/sửa

*GĐ 1 · #19 HITL · phụ thuộc: V4*


**Tệp SỬA:**

```
src/mon/tienganh/lib/hocba.js (mục loai 'viet' thêm `trangThai: 'tam'|'xacNhan'`, `diemNguoi?`)
src/mon/tienganh/components/VietBai.jsx (ghi `trangThai:'tam'`)
src/mon/tienganh/components/GocBoMe.jsx (nút Đồng ý / Sửa điểm 1 chạm)
src/mon/tienganh/lib/duLieu.js (đẩy cập nhật lên `hocBaTA`)
firestore.rules (cho phép cập nhật 2 trường ấy, KHÔNG cho sửa bài viết/lời chấm)
src/mon/tienganh/index.js (`bangCoGiao` → đọc attempts có `mon:'tienganh'`) — tuỳ chọn
```


**Tệp TẠO MỚI:**

```
—
```


**Hàm / hằng mới (chữ ký):**

```
hocba.js:
  export const TRANG_THAI_DIEM = { tam:'tam', xacNhan:'xacNhan' };
  export function xacNhanDiem(muc, { diemNguoi = null, luc }) → muc'  // diemNguoi null = đồng ý điểm AI
  export function diemHienThi(muc) → { diem, nhan: 'máy chấm – chờ bố mẹ' | 'bố mẹ đã xác nhận' | 'bố mẹ sửa: x' }
```


**Các bước làm (theo thứ tự):**

1) Thêm 2 trường vào mục học bạ `viet`; mặc định `tam`.  
2) `diemHienThi` dùng ở MỌI chỗ hiện điểm viết (thẻ, sổ, Góc bố mẹ) — cổng grep đảm bảo không chỗ nào hiện điểm viết mà không qua hàm này (cùng lối test 'máy chấm' hiện có).  
3) Góc bố mẹ: danh sách bài 'chờ xác nhận' + 2 nút.  
4) BKT: `onAttempt` pha `worked` chỉ nhận bản ghi viết khi đã `xacNhan`? → KHÔNG đổi (giữ như nay) để không chặn engine; chỉ hiển thị là có nhãn. Ghi rõ quyết định này trong chú thích.  
5) firestore.rules: `hocBaTA/{uid}/muc/{id}` cho update khi chỉ đổi `trangThai`, `diemNguoi`, `xacNhanLuc` (dùng `affectedKeys().hasOnly`).


**Ràng buộc KHÔNG được phá:**

- Nhật ký `attempts` vẫn bất biến.  
- Không có nút nào cho BÉ xác nhận điểm của mình (chỉ Góc bố mẹ, sau cổng người lớn hiện có).


**Tệp kiểm & lệnh chạy:**

SỬA: test/tienganh_chamviet.test.mjs (ca 'diemHienThi luôn có nhãn nguồn'); test/hocba.test.mjs hoặc tienganh_moc.test.mjs (ca `xacNhanDiem`); test/luat_firestore.test.mjs (update chỉ 3 trường được, đổi `cham` bị từ chối).  
Chạy: cd web && npm test && npm run test:luat (cần emulator)


**Định nghĩa XONG:**

- Mọi điểm viết trên màn có 1 trong 3 nhãn.  
- Luật Firestore từ chối sửa lời chấm, cho phép xác nhận.



### V6 · `bangTrangThai(uid)` — một nguồn sự thật về bé cho mọi mô-đun

*GĐ 1 · #18 Blackboard · phụ thuộc: V3*


**Tệp SỬA:**

```
src/mon/tienganh/components/PhongNoi.jsx, BaiHoc.jsx, OnLai.jsx, PhuDao.jsx (đọc qua bảng thay vì tự gom)
src/mon/tienganh/lib/chinhsach.js (`vectorS` nhận bảng)
```


**Tệp TẠO MỚI:**

```
src/mon/tienganh/lib/bangtrangthai.js
```


**Hàm / hằng mới (chữ ký):**

```
bangtrangthai.js (THUẦN, không fetch):
  export function dungBang({ tienDo, mucThao, doThi, cards, hoSoAI, bai, bayGio }) → {
    mucThao, nhomZPD: xepTheoZPD(...), nutGocRe: nutGocRe(...) | null, theDenHan: theDenHan(cards,…),
    hoSo: { ...vectorS(...), ai: hoSoAI }, luotGanNhat: null, nhanGanNhat: null, keHoach: null, buoiThu }
  export function ghiLuot(bang, luot, nhan) → bang'     // bất biến, trả bản mới
  export function tomTatChoLoiDan(bang) → string ≤ 900 ký tự  // dùng bởi loiDan
  export const TRAN_BANG_KY_TU = 4000;
```


**Các bước làm (theo thứ tự):**

1) Gom 6 nguồn đang rải (xem sheet 2 #18) thành 1 hàm dựng thuần; các màn chỉ truyền dữ liệu đã nạp vào.  
2) `PhongNoi.jsx`: thay `hoSoBe` useMemo bằng `dungBang(...)`; `hoiCoGiao` nhận `bang` thay cho `hoSo`+`haDoKho` rời (giữ chữ ký cũ tương thích 1 bản).  
3) `loiDan`: khối ABOUT THE CHILD = `tomTatChoLoiDan(bang)`.  
4) Mọi hàm ghi (`ghiLuot`, V3 `capNhatTuBuoi`, V7 `datKeHoach`) đều trả bản mới — không sửa tại chỗ.


**Ràng buộc KHÔNG được phá:**

- Không fetch trong tệp này; cổng chạy bằng node.  
- Trần kích thước; vượt → `tomTat` cắt theo ưu tiên: nhãn gần nhất > ZPD > bài học > sở thích.


**Tệp kiểm & lệnh chạy:**

TẠO: test/tienganh_bangtrangthai.test.mjs — dựng từ fixture 1 bé (mucThao 6 nút, 2 thẻ đến hạn, hoSoAI có 1 loiLap) → kiểm đủ trường; `tomTatChoLoiDan` ≤ 900, không số; bất biến (ghiLuot không đổi đối tượng cũ).  
Chạy: cd web && node test/tienganh_bangtrangthai.test.mjs


**Định nghĩa XONG:**

- 4 màn đều lấy trạng thái từ 1 hàm; grep không còn `vectorS(` ngoài `bangtrangthai.js`.



### V7 · Kế hoạch buổi (planner = code) + thanh bước + replanner

*GĐ 2 · #6 Plan-and-Execute · phụ thuộc: V2, V6*


**Tệp SỬA:**

```
src/mon/tienganh/lib/phongnoi.js (`viecTiepTheo` ưu tiên bước kế hoạch nếu có)
src/mon/tienganh/components/PhongNoi.jsx (thanh 'Hôm nay mình làm N việc')
src/mon/tienganh/lib/goiPhongNoi.js (dòng 'THIS STEP: …' vào lời dặn)
```


**Tệp TẠO MỚI:**

```
src/mon/tienganh/lib/kehoach.js
```


**Hàm / hằng mới (chữ ký):**

```
kehoach.js:
  export const SO_BUOC = [5, 7];
  export function lapKeHoach(bang, { von, kichBan = null }) → { buoc: [{ i, nut, tu, mau, kieu ∈ KIEU_VIEC, lyDo (tiếng Việt ≤ 60 ký tự), trangThai:'cho' }], tao: ts }
     // thứ tự: 1–2 bước ôn thẻ đến hạn / nút ZPD (chongChenh) → 2–3 bước nút mới của bài → 1 bước thay từ theo sở thích → 1 bước 'nói về mình'
  export function buocHienTai(kh) → buoc | null
  export function capNhatSauLuot(kh, { nhan, diem }) → kh'   // dung → bước xong; sai 2 lần liền → hạ kieu (thay→mau→tu); sai 3 → chèn bước phụ đạo (nut gốc rễ từ bang) và đánh dấu bước cũ 'bo'
  export const REPLAN_TOI_DA = 2;
```


**Các bước làm (theo thứ tự):**

1) Planner thuần code (không LLM) theo luật trên; dữ liệu vào từ `bangTrangThai` (V6).  
2) `viecTiepTheo`: nếu `kh` và `buocHienTai` → trả việc từ bước ấy (tu/mau/kieu), chỉ rơi về xoay vòng khi không có kế hoạch (bài chưa có nút).  
3) Lời dặn thêm 1 dòng `THIS STEP (${i}/${n}): practise "${tu}" with pattern ${mau} — because ${lyDoEn}` (lyDo tiếng Anh ngắn hoặc bỏ).  
4) `PhongNoi.jsx`: thanh bước (dùng lại `ThanhViec.jsx`), đọc lời giới thiệu kế hoạch bằng giọng Việt: 'Hôm nay mình làm 5 việc nhé: …'.  
5) `tinhBuoi`: thêm điều kiện kết 'xong kế hoạch' bên cạnh 20 phút / 3 đạt liền.  
6) Kịch bản (`buocTiepTheo`) vẫn ưu tiên khi bài có kịch bản; kế hoạch chỉ áp cho phần luyện tự do.


**Ràng buộc KHÔNG được phá:**

- Lưới đỡ `dandat.js` không đổi.  
- Không bỏ câu/nút nào khỏi bài; kế hoạch chỉ XẾP THỨ TỰ và chọn kiểu việc.  
- Replan tối đa 2 lần/buổi.


**Tệp kiểm & lệnh chạy:**

TẠO: test/tienganh_kehoach.test.mjs — kế hoạch từ bảng giả: có 5–7 bước; bước 1 là thẻ đến hạn nếu có; sai 2 lần → kieu hạ bậc; sai 3 → có bước phụ đạo và không quá 2 replan; mọi `tu` thuộc `von`.  
SỬA: test/tienganh_phongnoi.test.mjs (`viecTiepTheo` với kh → trả đúng bước).  
Chạy: cd web && node test/tienganh_kehoach.test.mjs


**Định nghĩa XONG:**

- Mô phỏng 50 bé giả (script tools/mo_phong_buoi.mjs, viết mới): ≥90% buổi kết thúc 'xong kế hoạch'.  
- Bé thấy thanh bước và nghe lời giới thiệu kế hoạch.



### V8 · Bài học cuối buổi (1 lời gọi) + job ΔC đề xuất sửa prompt

*GĐ 2 · #9 Reflexion · phụ thuộc: V3*


**Tệp SỬA:**

```
src/mon/tienganh/lib/goiPhongNoi.js (`tomTatBuoi`)
src/mon/tienganh/components/PhongNoi.jsx (gọi cuối buổi, không chờ)
functions/index.js + functions/src/luyennoi.js (cho phép gói 'tomTat' qua cùng callable `luyenNoi` — hoặc callable mới `tomTatBuoi` cùng chốt cửa)
```


**Tệp TẠO MỚI:**

```
src/mon/tienganh/lib/baihoc.js
tools/doc_delta_c.mjs
```


**Hàm / hằng mới (chữ ký):**

```
baihoc.js:
  export function loiDanTomTat({ lichSu, von, tenBe }) → string  // ≤ 1500 ký tự; yêu cầu JSON {baiHoc:[{chu ≤160, nut?}], khen ≤120}; cấm từ ngoài vốn trong phần trích tiếng Anh
  export function docTomTat(chu) → {baiHoc:[], khen} | null
  export function soiBaiHoc(bh, { von }) → {ok, vi}  // bác bài học có chữ Anh ngoài vốn, có số, có đánh giá tính cách (danh sách từ cấm: lười, kém, dốt, chậm…)
tools/doc_delta_c.mjs: đọc `phongNoiTA`+`mastery` bằng khoá quản trị → dựng cặp A-R-A → `gomTheoMau` → in bảng; cờ --de-xuat gọi LLM 1 lần đề xuất sửa cho mẫu kém nhất (in ra, KHÔNG tự sửa tệp).
```


**Các bước làm (theo thứ tự):**

1) Cuối buổi (`trangThai !== 'dang'`): gọi 1 lượt `luyenNoi` với system = `loiDanTomTat`, lịch sử = `goiGui(lichSu)` → `docTomTat` → `soiBaiHoc` → `themBaiHoc` (V3). Lỗi mạng → bỏ qua im lặng (đếm `LOI_TOM_TAT`).  
2) Bài học hiện ở Góc bố mẹ (V3) dưới dạng tiếng Việt.  
3) `tools/doc_delta_c.mjs` chạy tay, dùng `ara.js` sẵn có.  
4) Quy ước: sửa lời dặn theo đề xuất → tăng `PHIEN_BAN_MAU.luyennoi`; cổng `vantay_prompt.test` đã canh băm.


**Ràng buộc KHÔNG được phá:**

- Bài học ≤ 160 ký tự, hết hạn 5 buổi, bị xoá khi nút thạo (V3).  
- Không ghi cảm xúc/tính cách; `soiBaiHoc` chặn bằng danh sách từ.  
- Job ΔC không bao giờ tự sửa prompt — chỉ in đề xuất (HITL).


**Tệp kiểm & lệnh chạy:**

TẠO: test/tienganh_baihoc.test.mjs — `docTomTat` bóc JSON lẫn chữ thừa; `soiBaiHoc` bác 'bé lười', bác chữ Anh ngoài vốn, bác có số; lời dặn ≤ 1500 và nằm trong `TOI_DA_CHU_LOI_DAN`.  
SỬA: test/luyennoi.test.mjs nếu thêm callable.  
Chạy: cd web && node test/tienganh_baihoc.test.mjs


**Định nghĩa XONG:**

- Buổi sau, lời dặn chứa ≥1 bài học của buổi trước (log DEV).  
- `node tools/doc_delta_c.mjs` in được bảng ΔC theo `phienBanMau`.



### V9 · Phụ đạo có grader + re-query + chẩn đoán bằng lời + đường LLM thật

*GĐ 2 · #12 Agentic RAG · phụ thuộc: V6*


**Tệp SỬA:**

```
src/mon/tienganh/lib/phudao.js (`dungPhuDao` thêm grader & vòng 2)
src/mon/tienganh/components/PhuDao.jsx (hiện dòng chẩn đoán; nút 'Để sau' giữ)
functions/index.js (callable mới `sinhPhuDao`)
src/mon/tienganh/lib/doThi.js (`nhanNut` đã có — dùng cho câu chẩn đoán)
```


**Tệp TẠO MỚI:**

```
functions/src/phudao.js
src/mon/tienganh/lib/goiPhuDao.js
src/mon/tienganh/lib/chandoan.js
```


**Hàm / hằng mới (chữ ký):**

```
chandoan.js (thuần):
  export function cauChanDoan({ nutSai, nutGocRe, nhan }) → string tiếng Việt ≤ 120 ký tự  // 'Con sai câu … vì … từ bài … chưa chắc — mình ôn … trước nhé'
  export function chamCauTinh(cau, { maNut, doThi }) → 0|1  // câu có chứa từ/mẫu của ĐÚNG nút không (dựa `maNutDs` của câu), không phải chỉ 'cùng bài'
phudao.js:
  dungPhuDao({ …, goiLLM = null, toiDaVong = 2 })  // vòng 1: nút gốc rễ #1 tĩnh → chấm → thiếu → vòng 2: nút #2 / bài tiên quyết → vẫn thiếu & có goiLLM → sinh → `cauHoiHopLe`
functions/src/phudao.js:
  export function loiDanSinhPhuDao({ nut, nhan, von, mau, soCau }) → string; export async function sinhPhuDao(du, taoClient)  // cùng khuôn `chamBaiViet`: soi gói, không lưu, trả chữ trần + vân tay 'phudao'
goiPhuDao.js: export async function nhoSinh(...)  // chỗ duy nhất biết mạng
```


**Các bước làm (theo thứ tự):**

1) Viết `chamCauTinh` bằng code trước (đủ dùng, 0 chi phí); chỉ cân nhắc grader LLM nếu đo thấy câu tĩnh lệch nút nhiều.  
2) Nối `dungPhuDao` 2 vòng như chữ ký; câu LLM phải qua `cauHoiHopLe` (đã có) và được gắn `nguon:'ai'`.  
3) Câu AI hợp lệ → đẩy vào `choDuyetTA/{maNut}/{id}` (Firestore, luật: bé tạo, chỉ người lớn đọc/duyệt) — duyệt xong, script `tools/nhap_cau_duyet.py` ghép vào `data/tienganh/phudao_lopN.json` → bộ sinh → tĩnh.  
4) `PhuDao.jsx`: hiện `cauChanDoan` phía trên lời mời; đọc bằng giọng Việt.  
5) `PHIEN_BAN_MAU.phudao = 1`; vân tay như 2 mẫu kia.


**Ràng buộc KHÔNG được phá:**

- Đường lùi tĩnh giữ nguyên; không có mạng vẫn có phụ đạo khi kho tĩnh đủ.  
- Server không lưu; hàng đợi duyệt do máy con ghi, có luật.  
- Trần 2 vòng, trần 1 lời gọi LLM/lần phụ đạo.


**Tệp kiểm & lệnh chạy:**

SỬA: test (tìm tệp đang kiểm `dungPhuDao` — grep 'dungPhuDao' test/) — thêm: vòng 2 chạy khi vòng 1 < 4 câu; `goiLLM` giả trả 6 câu, 2 câu ngoài vốn → chỉ 4 vào bài, cả 4 `nguon:'ai'`; `goiLLM` ném lỗi → vẫn có phần tĩnh; `cauChanDoan` ≤ 120 ký tự, có tên nút gốc rễ.  
TẠO: test/phudao_may_chu.test.mjs (soi gói, lời dặn đòi JSON, client giả).  
Chạy: cd web && npm test


**Định nghĩa XONG:**

- ΔC (A-R-A) dương với ≥5 cặp hợp lệ sau 1 tháng.  
- Số lần phụ đạo `khongCo` → 0 với bài có đồ thị.



### V10 · Chấm viết 'lỗi ∥ khen'; chấm nói mơ hồ bỏ phiếu

*GĐ 2 · #3 Parallelization · phụ thuộc: V4*


**Tệp SỬA:**

```
functions/src/chamviet.js (bước 1 tách 2 lời gọi `Promise.all`)
src/mon/tienganh/lib/chamnoi.js (hàm `vungMoHo(diem)`), src/mon/tienganh/components/NutNoi.jsx (gọi bỏ phiếu khi mơ hồ)
functions/index.js (callable `phanXuNoi`, cùng chốt cửa)
```


**Tệp TẠO MỚI:**

```
functions/src/phanxu.js
```


**Hàm / hằng mới (chữ ký):**

```
chamnoi.js: export const VUNG_MO_HO = [5, 7]; export const vungMoHo = (d) => d >= 5 && d <= 7;
phanxu.js: export function loiDanPhanXu({ nghe, dich, canhTranh }) → string; export async function phanXu(du, taoClient) // 2 lời gọi song song temp 0.2, mỗi cái trả {gan:'dich'|'canhTranh'|'khac'}; đa số (2/2) mới điều chỉnh ±1, lệch nhau → giữ điểm
```


**Các bước làm (theo thứ tự):**

1) Chấm viết: `Promise.all([timLoi, timKhen])` rồi gộp bằng code → bước 2 (V4).  
2) Chấm nói: chỉ khi `vungMoHo(diem)` và có `canhTranh` → gọi `phanXu`; trả về điểm điều chỉnh + 1 câu nhận xét lấy từ `chamnoi.loiNhanXet` (không để LLM viết lời cho bé).  
3) Mất mạng → giữ điểm cũ, không báo lỗi cho bé.


**Ràng buộc KHÔNG được phá:**

- Không bao giờ hạ điểm dưới 5 hay nâng trên 7 bằng bỏ phiếu (±1).  
- 2 lời gọi dùng `temperature` khác nhau (0.2 / 0.5) để không 'đồng thuận sai' cùng kiểu.


**Tệp kiểm & lệnh chạy:**

TẠO: test/phanxu.test.mjs — 2 phiếu 'canhTranh' → −1; 1–1 → giữ; lỗi → giữ; không gọi khi diem ∉ [5,7].  
Chạy: cd web && node test/phanxu.test.mjs


**Định nghĩa XONG:**

- Trên 50 mẫu chấm tay: khớp tăng ≥10 điểm % ở vùng 5–7.



### V11 · Nhánh 'hỏi lại' lớp 3+ với 4 tool, trần 3 bước

*GĐ 3 · #5 ReAct · phụ thuộc: V2, V1*


**Tệp SỬA:**

```
functions/src/luyennoi.js (cho phép `tools` + vòng ≤3 bước ở server, model gọi tool; kết quả tool do SERVER tính từ gói `kho` máy con gửi lên — vẫn không lưu)
src/mon/tienganh/lib/goiPhongNoi.js (nhánh nhan===hoiLai && lop>=3 → gửi `kho` = {vonTu, mauCau, mucThaoTomTat})
```


**Tệp TẠO MỚI:**

```
functions/src/tool_phongnoi.js
src/mon/tienganh/lib/hoico.js
```


**Hàm / hằng mới (chữ ký):**

```
tool_phongnoi.js: export const TOOLS = [tra_tu, mau_cau_cua_unit, muc_thao, nghe_lai]; export function chayTool(ten, args, kho) → string (cắt ≤ 300 ký tự); export const BUOC_TOI_DA = 3;
luyennoi.js: export async function hoiMayCoTool(du, taoClient) // vòng ReAct, phát hiện lặp (cùng tool+args 2 lần → dừng), trả chữ trần như `hoiMay`
```


**Các bước làm (theo thứ tự):**

1) Tool là hàm thuần trên `kho` gửi kèm (server không có dữ liệu riêng) — giữ 'không lưu gì'.  
2) Chỉ rẽ vào khi `nhan===hoiLai` (V2) và `lop>=3`; lớp 1–2 trả lời bằng nhánh workflow.  
3) Câu cuối vẫn qua `soiCau` + V1.


**Ràng buộc KHÔNG được phá:**

- Trần 3 bước, trần token, phát hiện lặp.  
- Kết quả tool ≤ 300 ký tự.  
- Không thêm tool nào có tác dụng phụ.


**Tệp kiểm & lệnh chạy:**

TẠO: test/luyennoi_tool.test.mjs — client giả gọi tool 4 lần → dừng ở 3; lặp cùng tool → dừng; `chayTool` cắt 300; `tra_tu` từ ngoài kho → 'không có trong bài'.


**Định nghĩa XONG:**

- Bé lớp 3 hỏi nghĩa từ → trả lời đúng nghĩa trong kho, kèm clip (kiểm tay 10 câu).



### V12 · Xưởng sinh nội dung offline (supervisor → worker → cổng → giám khảo → duyệt)

*GĐ 3 · #14 #10 #17 #3 offline · phụ thuộc: —*


**Tệp SỬA:**

```
tools/sinh_bai_tienganh.py (nhận thêm đầu vào từ xưởng)
tools/README.md
```


**Tệp TẠO MỚI:**

```
tools/xuong/ (python): dieu_phoi.py · worker_tu_moi.py · worker_mau_cau.py · worker_kich_ban.py · worker_doc_hieu.py · giam_khao.py · tranh_luan.py · duyet.md
```


**Hàm / hằng mới (chữ ký):**

```
dieu_phoi.py: `python tools/xuong/dieu_phoi.py --lop 4 --unit 3 --ra data/tienganh/xuong/lop4_u03.json`
giam_khao.py: 3 lời gọi song song (vốn/mẫu · tự nhiên · hợp tuổi) → phiếu; ≥2 bác → loại; 2–1 → `tranh_luan.py` 2 vòng → ghi lý do vào `duyet.md` cho bác.
```


**Các bước làm (theo thứ tự):**

1) Mọi worker trả JSON theo schema cố định của `sinh_bai_tienganh.py` (không văn tự do).  
2) Mọi câu qua `soiCau`-tương-đương bằng Python (đã có trong `chuan_tienganh.py`) TRƯỚC giám khảo LLM.  
3) Đầu ra chỉ vào `data/` sau khi bác duyệt `duyet.md`; rồi chạy bộ sinh + 83 cổng như hiện nay.


**Ràng buộc KHÔNG được phá:**

- Không bao giờ chạy lúc bé học.  
- Không ghi thẳng vào `public/content/`.


**Tệp kiểm & lệnh chạy:**

Cổng Python hiện có + `npm test` sau khi sinh. Thêm `tools/xuong/test_schema.py` kiểm schema đầu ra worker.


**Định nghĩa XONG:**

- Sinh được 1 unit lớp 4 đủ 4 loại nội dung, qua 83 cổng, bác duyệt < 10% bác bỏ.



## §8 · CA KIỂM (TEST CASES)

Khuôn test của kho: `import { test } from 'node:test'; import assert from 'node:assert/strict';` (các tệp `tienganh_*.test.mjs`) hoặc bộ đếm pass/fail tự viết (`luyennoi.test.mjs`). Fixture bài học: hàm `bai(id, tu, cau)` trong `test/tienganh_phongnoi.test.mjs` (mẫu câu phải có công thức với ô trống).


### V1

- **lặp lượt trước → gọi lại 1 lần rồi nhận câu mới** — `tienganh_sua_co.test.mjs` *(unit)*

  - Dựng: von = vonTu(bai fixture U1); lichSu = [may:'Hi, I\'m Bo.', be:{chu:'hi im bo', diem:8}]; goi giả: lần1 trả {en:'Hi, I\'m Bo.',vi:'…'}, lần2 trả {en:'Hi, I\'m Lan.',vi:'…'}

  - Hành động: `await hoiCoGiao({von, lichSu, tenBe:'Lan', lop:1}, {goi})`

  - Kỳ vọng: goi.mock.callCount()===2; tra.en==='Hi, I\'m Lan.'; tra.lanSua===1; tra.daThay===false; messages lần 2 có role user chứa 'repeated'

- **trượt cả 2 vòng → cauThayThe, daThay true** — `tienganh_sua_co.test.mjs` *(unit)*

  - Dựng: goi giả luôn trả câu chứa 'chips' (ngoài vốn)

  - Hành động: `như trên`

  - Kỳ vọng: goi.mock.callCount()===3 (1 + SUA_CO_TOI_DA); tra.daThay===true; tra.lanSua===SUA_CO_TOI_DA; tra.en ∈ {tu.tu, mau.cau}

- **qua ngay → không gọi lại** — `tienganh_sua_co.test.mjs` *(unit)*

  - Dựng: goi giả trả câu hợp lệ

  - Hành động: `như trên`

  - Kỳ vọng: callCount()===1; tra.lanSua===0

- **loiNhacSua mỗi lý do cho đúng câu nhắc, ≤300 ký tự, không có dấu tiếng Việt** — `tienganh_phongnoi.test.mjs` *(unit)*

  - Dựng: bac ∈ {rong, lap, oTrong, ngoaiVon}

  - Hành động: `loiNhacSua(bac, ctx)`

  - Kỳ vọng: match regex riêng từng loại; length ≤ 300; !/[àáảãạ…]/

- **lượt sửa không lọt vào lichSu hiển thị** — `tienganh_sua_co.test.mjs` *(unit)*

  - Dựng: như ca 1

  - Hành động: `kiểm `sau` trả về PhongNoi (hoặc kiểm `tra` không mang mảng lượt phụ)`

  - Kỳ vọng: tra không có trường chứa câu bị bác; LOI_SUA_CO.so tăng 1, thanh tăng 1


### V2

- **9 nhãn, mỗi nhãn 1 ca** — `tienganh_nhanluot.test.mjs` *(unit)*

  - Dựng: luotBe lần lượt: null/'' → imLang; {chu:'hello',diem:9} → dung; {chu:'im bo',diem:4,thieu:['hi']} → thieuTu; {chu:'bo im hi',diem:4,thieu:[],mau:'Hi, I\'m Bo.'} → saiThuTu; {nhamThanh:'duck'} → nhamTu; {chu:'cô ơi con không biết'} → tiengViet; {chu:'cô ơi dog là gì?'} → hoiLai; {chu:'xyz zzz',diem:0,mau:null} → lacDe; lichSu rỗng → moDau

  - Hành động: `nhanLuot(luotBe, {von})`

  - Kỳ vọng: nhan đúng; doTin ≥ 0.6; chiTiet đúng (thieu / {dich,nham})

- **mỗi nhãn có đúng 1 lời dặn hợp lệ** — `tienganh_nhanluot.test.mjs` *(unit)*

  - Dựng: Object.keys(NHAN)

  - Hành động: `dongTheoNhan(nhan, ctx)`

  - Kỳ vọng: typeof string; length ≤ 600; không chứa 'bạn|em|tớ|cậu' (XUNG_HO_CAM); chứa chữ 'ONE' hoặc 'one' (một việc)

- **lời dặn tổng ≤ 8000 với vốn lớp 3** — `tienganh_nhanluot.test.mjs` *(dữ liệu thật)*

  - Dựng: bai lớp 3 thật (public/content/ta3/u21.json) + nhan mỗi loại

  - Hành động: `loiDan({von, nhan, hoSo})`

  - Kỳ vọng: length ≤ TOI_DA_CHU_LOI_DAN

- **thieuTu giữ nguyên mẫu câu lượt trước** — `tienganh_nhanluot.test.mjs` *(unit)*

  - Dựng: lichSu có may {en:'Hi, I\'m Bo.'} rồi be thieuTu

  - Hành động: `viecTiepTheo({von, lichSu, nhan:'thieuTu'})`

  - Kỳ vọng: viec.kieu==='mau' && viec.mau.cau==='Hi, I\'m + [Name].'-ví dụ tương ứng

- **dòng theo nhãn chứa chữ bé nói không lọt vào vân tay** — `vantay_prompt.test.mjs` *(unit)*

  - Dựng: 2 lời dặn cùng nhãn nhamTu, bé A nhầm 'duck', bé B nhầm 'cat'

  - Hành động: `locKhung(a) vs locKhung(b)`

  - Kỳ vọng: bằng nhau


### V3

- **capNhatTuBuoi rút loiLap từ thieuChucNang lặp** — `tienganh_hosoai.test.mjs` *(unit)*

  - Dựng: lichSu 3 lượt be có thieuChucNang:['a']

  - Hành động: `capNhatTuBuoi(hoSoRong(), {lichSu})`

  - Kỳ vọng: hs.loiLap chứa 'a'; buoiThu===1

- **trần ký tự và trần phần tử** — `tienganh_hosoai.test.mjs` *(unit)*

  - Dựng: hs với 20 soThich dài

  - Hành động: `donHoSo(hs,{})`

  - Kỳ vọng: JSON.stringify(hs').length ≤ TRAN_KY_TU; soThich.length ≤ 5

- **bài học hết hạn và nút đã thạo bị dọn** — `tienganh_hosoai.test.mjs` *(unit)*

  - Dựng: baiHoc {hetHanBuoi:3}, buoiHienTai 4; loiLap {nut:'x'} với mucThao.x=0.9

  - Hành động: `donHoSo(hs,{mucThao, buoiHienTai:4})`

  - Kỳ vọng: baiHoc rỗng; loiLap rỗng

- **dongHoSoAI không số, ≤ 8 dòng, đọc to được** — `tienganh_hosoai.test.mjs` *(unit)*

  - Dựng: hs đầy đủ

  - Hành động: `dongHoSoAI(hs,'Bo')`

  - Kỳ vọng: !/\d/; split('\n').length ≤ 8; không chứa 'score|percent|%'

- **gộp sổ: capNhatLuc mới hơn thắng** — `tienganh_hosoai.test.mjs` *(unit)*

  - Dựng: 2 sổ khác hoSoAI

  - Hành động: `gopTienDo(a,b)`

  - Kỳ vọng: hoSoAI là bản có capNhatLuc lớn hơn


### V4

- **lời dặn bước 1 cấm sửa, bước 2 nêu từ lạ lần trước** — `tienganh_chamviet.test.mjs` *(unit)*

  - Dựng: goi fixture VON

  - Hành động: `loiDanTimLoi / loiDanSua(goi, loi, ['delicious'])`

  - Kỳ vọng: /không sửa|KHÔNG sửa/ ở bước 1; /delicious/ ở bước 2

- **chuỗi gọi lại khi có từ lạ** — `tienganh_chamviet.test.mjs` *(unit)*

  - Dựng: client giả: tạo create() trả theo thứ tự [timLoi, sua(có 'delicious'), sua(sạch), boMe]

  - Hành động: `chamBaiViet(du, ()=>client)`

  - Kỳ vọng: create gọi 4 lần; kq.lanSuaLai===1; JSON gộp không còn 'delicious'

- **2 bản chuLa giống hệt** — `chula_hai_ban.test.mjs` *(unit)*

  - Dựng: 30 cặp (câu, vốn) kể cả cụm nhiều chữ, dấu nháy cong

  - Hành động: `chuLa (lib) vs chuLa (functions)`

  - Kỳ vọng: deepEqual từng cặp


### V5

- **xacNhanDiem và diemHienThi** — `hocba.test.mjs (hoặc tienganh_moc)` *(unit)*

  - Dựng: muc {cham:{diem:8}, trangThai:'tam'}

  - Hành động: `xacNhanDiem(muc,{diemNguoi:7}) → diemHienThi`

  - Kỳ vọng: nhan chứa 'bố mẹ sửa'; diem===7; muc cũ không bị sửa tại chỗ

- **chỉ 3 trường được update** — `luat_firestore.test.mjs` *(emulator)*

  - Dựng: emulator; user uid

  - Hành động: `update {trangThai,diemNguoi,xacNhanLuc} → OK; update {cham} → bị từ chối`

  - Kỳ vọng: assertSucceeds / assertFails


### V6

- **dựng bảng đủ trường và bất biến** — `tienganh_bangtrangthai.test.mjs` *(unit)*

  - Dựng: fixture: mucThao 6 nút, cards 2 thẻ đến hạn, hoSoAI 1 loiLap

  - Hành động: `b=dungBang(...); b2=ghiLuot(b, luot, 'dung')`

  - Kỳ vọng: b có nhomZPD, nutGocRe, theDenHan.length===2; b!==b2; b.luotGanNhat===null

- **tomTatChoLoiDan ≤ 900, không số** — `tienganh_bangtrangthai.test.mjs` *(unit)*

  - Dựng: bảng đầy

  - Hành động: `tomTatChoLoiDan(b)`

  - Kỳ vọng: length ≤ 900; !/\d/


### V7

- **kế hoạch 5–7 bước, thẻ đến hạn lên đầu, mọi từ trong vốn** — `tienganh_kehoach.test.mjs` *(unit)*

  - Dựng: bảng V6 fixture + von

  - Hành động: `kh=lapKeHoach(b,{von})`

  - Kỳ vọng: SO_BUOC[0] ≤ kh.buoc.length ≤ SO_BUOC[1]; buoc[0].nut ∈ theDenHan; mọi buoc.tu ∈ moiTuDuocDung(von)

- **sai 2 lần hạ bậc, sai 3 chèn phụ đạo, replan ≤ 2** — `tienganh_kehoach.test.mjs` *(unit)*

  - Dựng: kh với bước kieu 'thay'

  - Hành động: `capNhatSauLuot ×3 với nhan 'thieuTu'`

  - Kỳ vọng: sau 2: kieu==='mau'; sau 3: có bước loai 'phuDao'; soReplan ≤ REPLAN_TOI_DA


### V8

- **soiBaiHoc bác tính cách / ngoài vốn / số** — `tienganh_baihoc.test.mjs` *(unit)*

  - Dựng: ['Bé lười nói', 'She forgets "chips"', 'Nói được 3/5 câu', 'Bé hay bỏ chữ "a" trước "dog"']

  - Hành động: `soiBaiHoc từng cái`

  - Kỳ vọng: false,false,false,true

- **docTomTat bóc JSON lẫn chữ thừa; lời dặn trong trần** — `tienganh_baihoc.test.mjs` *(unit)*

  - Dựng: 'Sure! {"baiHoc":[…],"khen":"…"} bye'

  - Hành động: `docTomTat / loiDanTomTat`

  - Kỳ vọng: baiHoc.length≥1; loiDanTomTat(...).length ≤ 1500


### V9

- **vòng 2 + LLM giả + lỗi mạng** — `(tệp đang kiểm dungPhuDao)` *(unit)*

  - Dựng: doThi fixture 3 nút chuỗi; bai với 2 câu tĩnh của nút gốc; goiLLM giả trả 6 câu (2 ngoài vốn)

  - Hành động: `dungPhuDao({…, goiLLM})`

  - Kỳ vọng: bai.cau.length===4; 2 câu đầu nguon 'tinh', 2 sau 'ai'; goiLLM ném → vẫn 2 câu tĩnh, trangThai 'xong'

- **cauChanDoan** — `(cùng tệp)` *(unit)*

  - Dựng: nutSai 'sp_g1_u12_1', nutGocRe 'v_g1_u2_num', nhan 'thieuTu'

  - Hành động: `cauChanDoan(...)`

  - Kỳ vọng: length ≤ 120; chứa nhanNut(gốc rễ); tiếng Việt


### V10

- **bỏ phiếu ±1, 1–1 giữ, lỗi giữ, ngoài vùng không gọi** — `phanxu.test.mjs` *(unit)*

  - Dựng: client giả trả [canhTranh,canhTranh] / [dich,canhTranh] / ném lỗi; diem 6 và 9

  - Hành động: `phanXu(...)`

  - Kỳ vọng: −1 / giữ / giữ / không gọi (callCount 0)


### V11

- **trần 3 bước và phát hiện lặp** — `luyennoi_tool.test.mjs` *(unit)*

  - Dựng: client giả luôn trả tool_call tra_tu('dog')

  - Hành động: `hoiMayCoTool(du, ()=>client)`

  - Kỳ vọng: create gọi ≤ BUOC_TOI_DA+1; dừng sớm vì lặp ở lần 2


### Chung

- **npm test toàn kho** — `tất cả` *(hồi quy)*

  - Dựng: —

  - Hành động: `cd web && npm test`

  - Kỳ vọng: exit 0; số tệp kiểm ≥ 74 + số tệp mới

- **mô phỏng 50 bé × 1 buổi với mô hình giả** — `tools/mo_phong_buoi.mjs (mới, V7)` *(đo)*

  - Dựng: mô hình giả: 40% lặp, 10% ngoài vốn, bé: đúng 60%

  - Hành động: `node tools/mo_phong_buoi.mjs`

  - Kỳ vọng: in: tỉ lệ daThay, phân phối nhãn, % buổi xong kế hoạch — mục tiêu < 5% / đủ 9 nhãn / ≥ 90%


## §9 · PROMPT & LỜI DẶN (BẢN NHÁP)

Ký hiệu `{…}` là chỗ code điền. Các khối A thay cho luật 7/8/8b/8c của `loiDan()` (không lặp hai nơi); luật 1–6, 9, 10 giữ ở khối chung. Sau khi sửa lời dặn: tăng `PHIEN_BAN_MAU`.


### A1 · nhãn moDau  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: it is the first turn. Greet once by name, then do the first task of the plan. One English sentence.
```

Ràng buộc: ≤600 ký tự; không bảng vốn (đã ở khối chung)


### A2 · nhãn dung  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: her last sentence was correct. Put a SHORT, specific praise in the Vietnamese line (name the word she got right), then give the NEXT task in English. Do not repeat the sentence she just said.
```

Ràng buộc: praise cụ thể, cấm 'giỏi lắm' trần


### A3 · nhãn thieuTu  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: she said "{beNoi}" but the target was "{mau}". She LEFT OUT: {thieu}. In the Vietnamese line, say the one thing that was right, then name ONLY the missing word (quote it exactly). In English, say the target sentence again, unchanged. Do not move on.
```

Ràng buộc: `{beNoi}` được trích đúng chữ (luật 10); V1 vẫn soi


### A4 · nhãn saiThuTu  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: she said the right words in the WRONG ORDER: "{beNoi}" vs target "{mau}". In Vietnamese, tell her which word comes FIRST. In English, say the target sentence slowly (same words). Do not move on.
```


### A5 · nhãn nhamTu  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: she said "{nham}" instead of "{dich}" — two different words from this unit. In Vietnamese, say what "{nham}" means and what "{dich}" means (use the meanings from the word list), then ask her to say "{dich}". English: the single word "{dich}", or the target sentence.
```

Ràng buộc: nghĩa lấy từ bảng vốn, không tự dịch


### A6 · nhãn tiengViet  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: she spoke VIETNAMESE: "{beNoi}". Answer her in the Vietnamese line kindly and briefly (one sentence), then invite her to try the SAME English target again. English: the target sentence.
```

Ràng buộc: không đổi việc


### A7 · nhãn hoiLai  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: she ASKED a question: "{beNoi}". If it is about a word in the allowed list, answer with that word's meaning from the list (Vietnamese line). If it is about anything else, say gently that we will learn it later. English: say the word she asked about (if allowed) or the target sentence.
```

Ràng buộc: lớp 3+: V11 rẽ sang ReAct


### A8 · nhãn imLang  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: she said NOTHING. Do not scold. In Vietnamese, say the target sentence's meaning in a playful way and ask her to try — even just the first word. English: the first WORD of the target only.
```

Ràng buộc: hạ bậc về từ


### A9 · nhãn lacDe  *(việc V2 · vị trí: sau HARD RULES)*

```
THIS TURN: her reply did not match the task ("{beNoi}"). Do not comment on it. Restate the target task in Vietnamese with one concrete hint (which word to start with). English: the target sentence.
```


### B1 · nhắc sửa (rong)  *(việc V1 · vị trí: role user, sau assistant bị bác)*

```
Your reply had no English sentence. Reply as JSON {"en": …, "vi": …} with ONE English sentence using only the allowed words.
```

Ràng buộc: ≤300 ký tự, tiếng Anh thuần


### B2 · nhắc sửa (lap)  *(việc V1 · vị trí: role user)*

```
You repeated your previous sentence: "{cauTruoc}". Say a DIFFERENT sentence for the same task — change the word in the slot. Reply as JSON.
```


### B3 · nhắc sửa (oTrong)  *(việc V1 · vị trí: role user)*

```
Your sentence still contains an unfilled slot like [Name] or [Month]. Fill every slot with an allowed word or the child's name. Reply as JSON.
```


### B4 · nhắc sửa (ngoaiVon)  *(việc V1 · vị trí: role user)*

```
Your sentence used words that are NOT allowed: {tuLa}. Use ONLY: {bangTu}. Rewrite the sentence for the same task. Reply as JSON.
```

Ràng buộc: `tuLa` từ `tuTrongCau`


### B5 · nhắc sửa lời Việt  *(việc V1 · vị trí: role user)*

```
Keep the English sentence exactly: "{en}". Rewrite ONLY the Vietnamese line: {lyDo}. Call yourself "cô" and the child "con". Reply as JSON.
```

Ràng buộc: `lyDo` = `loiVietHopLe().vi`


### C1 · tóm tắt buổi (Reflexion)  *(việc V8 · vị trí: system của lời gọi cuối buổi)*

```
You are reviewing a short English practice session of a Vietnamese child named {tenBe} (grade {lop}). Below is the conversation. Write, IN VIETNAMESE, for the teacher's private notebook:
- "baiHoc": 1–3 short notes (≤160 chars each) about SPECIFIC language errors that repeated (missing word, swapped order, confused pair). Quote English words only from this list: {bangTu}. No numbers, no scores, no comments about the child's character or mood.
- "khen": one sentence (≤120 chars) naming one thing she did well.
Reply as JSON only: {"baiHoc":[{"chu":"…","nut":"<optional>"}],"khen":"…"}
```

Ràng buộc: `soiBaiHoc` chặn từ cấm & ngoài vốn; ≤1500 ký tự


### D1 · chấm viết bước 1 (tìm lỗi)  *(việc V4 · vị trí: system)*

```
Bạn là cô giáo tiếng Anh tiểu học. CHỈ LIỆT KÊ LỖI trong bài viết dưới đây, KHÔNG SỬA, KHÔNG KHEN. Mỗi lỗi: {"cau": "<câu bé viết, nguyên văn>", "loai": "chinhTa|thieuTu|thuTu|mauCau|khac", "ghiChu": "<≤ 15 chữ tiếng Việt>"}. Bài không lỗi → []. Trả JSON: {"loi": [...]}
ĐỀ: {de}
BÀI: {viet}
```

Ràng buộc: temp 0.1; không bảng vốn (không cần)


### D2 · chấm viết bước 2 (sửa + khen)  *(việc V4 · vị trí: system)*

```
(giữ phần đầu của `loiDanCham` hiện có: vai, đề, VỐN TỪ, MẪU CÂU) + 'DANH SÁCH LỖI đã tìm được: {loiDs}. Với MỖI lỗi, viết "sua" (tiếng Anh, CHỈ dùng từ trong bảng vốn) và "viSao" (tiếng Việt ≤ 20 chữ). Viết "khen" cụ thể và "goiY" một câu.' + (nếu có) 'LẦN TRƯỚC bạn đã dùng từ ngoài bảng: {tuLaTruoc}. KHÔNG được dùng lại; nếu không diễn đạt được bằng bảng vốn thì bỏ câu sửa ấy và ghi "sua": "".' + khối JSON {diem, khen, loi:[{cau,sua,viSao}], goiY}
```

Ràng buộc: temp 0.2; `chuLa` soi; gọi lại ≤2


### D3 · chấm viết bước 3 (bố mẹ)  *(việc V4 · vị trí: system)*

```
Dưới đây là lời chấm một bài viết tiếng Anh của bé lớp {lop}. Viết 2 câu tiếng Việt cho BỐ MẸ: (1) con làm được gì, (2) tuần này nên tập gì — chỉ dùng tên từ/mẫu câu có trong lời chấm. Trả JSON {"choBoMe": "…"}. LỜI CHẤM: {cham}
```

Ràng buộc: model nhỏ được


### E1 · sinh câu phụ đạo  *(việc V9 · vị trí: system)*

```
You write practice items for a Vietnamese child (grade {lop}) who is struggling with: {nhanNut} (knowledge node {nut}). Her last error type: {nhan}. Write {soCau} items of format "chon" (multiple choice, 4 options, 1 correct) that practise EXACTLY this node. Use ONLY these English words: {bangTu} and these patterns: {mau}. Each item: {"hoi": "<Vietnamese instruction>", "en": "<English stem>", "luaChon": [..4..], "dung": <index>}. Reply as JSON {"cau": [...]}
```

Ràng buộc: qua `cauHoiHopLe`; nguon 'ai'; vào hàng đợi duyệt


### E2 · câu chẩn đoán (CODE, không LLM)  *(việc V9 · vị trí: màn PhuDao, giọng Việt)*

```
Con sai câu {tenNutSai} vì {tenNutGocRe} (học ở {tenBai}) chưa chắc — mình ôn {tenNutGocRe} trước nhé.
```

Ràng buộc: ≤120 ký tự; `nhanNut` từ doThi


### F1 · phân xử chấm nói  *(việc V10 · vị trí: system (2 lời gọi, temp 0.2 và 0.5))*

```
A speech recogniser heard: "{nghe}". The child was asked to say "{dich}". Other words from the same lesson: {canhTranh}. Which is the transcript closest to? Reply JSON {"gan": "dich" | "canhTranh" | "khac", "tu": "<the word>"}
```

Ràng buộc: chỉ khi điểm 5–7; ±1


## §10 · PROMPT GIAO VIỆC (DÁN THẲNG VÀO CLAUDE CODE)

### Bối cảnh chung (dán trước mỗi prompt)

```
Bối cảnh: repo web5 (React+Vite, môn Tiếng Anh ở web/src/mon/tienganh, cloud functions ở web/functions). Đọc trước: web/src/mon/tienganh/index.js, docs/tiep_theo_tienganh.md, và sheet '7. Việc cho Claude Code' + '8. Ca kiểm' + '9. Prompt & lời dặn' trong docs/Review_18_mau_AI_Agent_cho_Tieng_Anh.xlsx (đọc bằng python openpyxl hoặc markitdown). Quy ước bắt buộc: cd web && npm test phải 0 FAIL trước và sau; không import chéo mon/toan↔mon/tienganh và browser↔functions (test/ranh_gioi.test.mjs); máy chủ không lưu gì; mọi câu tiếng Anh AI sinh phải qua soiCau/cauHoiHopLe; hằng số trần phải export và có cổng; viết chú thích đầu hàm theo giọng hiện có (VÌ SAO / ⚠). Làm xong: liệt kê tệp đã sửa/tạo, số test thêm, kết quả npm test, và điều gì CHƯA thử được (ví dụ thiếu khoá Groq).
```


### 1. V1

```
VIỆC V1 — Vòng gọi lại khi soiCau bác câu của cô (mẫu Evaluator–Optimizer). Làm đúng cột 'Các bước làm' của hàng V1 sheet 7: thêm SUA_CO_TOI_DA, loiNhacSua, loiNhacSuaViet vào lib/phongnoi.js (nội dung lời nhắc ở sheet 9 mục B1–B5); tách httpsCallable trong goiPhongNoi.js thành hàm goiMay tiêm được; nối vòng gọi lại ≤2 trước khi rơi về cauThayThe; thêm LOI_SUA_CO; lượt sửa không vào lichSu hiển thị. Viết test/tienganh_sua_co.test.mjs theo 5 ca ở sheet 8 (V1) với hàm goi giả. Không đổi luật máy chủ.
```

Kiểm sau khi xong: node test/tienganh_sua_co.test.mjs; npm test; đọc diff goiPhongNoi.js: vòng có trần, cauThayThe vẫn là đường lùi.


### 2. V2

```
VIỆC V2 — Routing lượt của bé. Tạo lib/nhanluot.js (nhanLuot thuần code, 9 nhãn, doTin) và lib/loidan_nhan.js (9 lời dặn ≤600 ký tự, bản nháp ở sheet 9 mục A1–A9, chỉnh cho khớp giọng loiDan hiện có). Sửa viecTiepTheo nhận nhan (thieuTu/saiThuTu/nhamTu → giữ nguyên tu/mau), loiDan chèn dongTheoNhan sau HARD RULES và GỠ luật 7/8/8b/8c khỏi khối chung; hoiCoGiao tính nhãn từ luotBeCuoi và ghi nhan vào lượt 'may'. Cập nhật DAU_RIENG ở functions/src/vantay.js cho dòng chứa chữ bé nói. Viết test/tienganh_nhanluot.test.mjs theo sheet 8 (V2) và thêm ca vào test/vantay_prompt.test.mjs.
```

Kiểm sau khi xong: node test/tienganh_nhanluot.test.mjs; node test/vantay_prompt.test.mjs; npm test; đọc 2 lời dặn in ra (DEV) với nhãn thieuTu và hoiLai.


### 3. V3

```
VIỆC V3 — Hồ sơ AI về bé qua nhiều buổi (Memory-augmented). Tạo lib/hosoai.js đúng chữ ký ở sheet 7 hàng V3 (hoSoRong, capNhatTuBuoi, themBaiHoc, donHoSo, dongHoSoAI, xoaHoSoAI; trần 1200 ký tự, hạn 5 buổi, trần phần tử). Thêm trường hoSoAI vào sổ ttd5.tienganh.v1 trong lib/progress.js và gộp theo capNhatLuc. PhongNoi.jsx cập nhật hồ sơ khi buổi kết thúc (chưa gọi LLM). dongHoSo trong phongnoi.js nối thêm dongHoSoAI — giữ quy ước 'câu nào đọc to cũng không sao', không số. Góc bố mẹ: hiện tiếng Việt + nút xoá. Bọc khối riêng trong lời dặn bằng dấu <<RIENG … RIENG>> và sửa locKhung bỏ cả khối. Viết test/tienganh_hosoai.test.mjs (6 ca sheet 8).
```

Kiểm sau khi xong: node test/tienganh_hosoai.test.mjs; npm test; mở app 2 buổi liền, bật DEV log xem khối ABOUT THIS CHILD buổi 2.


### 4. V4

```
VIỆC V4 — Chấm bài viết 3 mắt xích + viết lại khi có từ lạ (Prompt Chaining + Evaluator–Optimizer) trong web/functions/src/chamviet.js. Tách loiDanCham thành loiDanTimLoi / loiDanSua(goi, loiDs, tuLaTruoc) / loiDanBoMe (nháp ở sheet 9 D1–D3); chamBaiViet chạy chuỗi 1→2→soi chữ lạ→2'(≤SUA_LAI_TOI_DA=2)→3 rồi trả JSON gộp + lanSuaLai; chép chuLa sang functions/src/chula.js và viết test/chula_hai_ban.test.mjs so hai bản; khungCham dựng từ 3 khung; tăng PHIEN_BAN_MAU.chamviet=2. Máy con goiChamViet giữ giao diện, đọc thêm lanSuaLai. Bổ sung ca vào test/tienganh_chamviet.test.mjs theo sheet 8 (V4) với client giả create() trả theo thứ tự.
```

Kiểm sau khi xong: node test/tienganh_chamviet.test.mjs; node test/chula_hai_ban.test.mjs; npm test; nếu có khoá Groq: firebase emulators + 1 bài thật, kiểm LOI_CHU_LA.so.


### 5. V5

```
VIỆC V5 — Điểm AI ở trạng thái tạm, bố mẹ xác nhận (Human-in-the-loop). Thêm TRANG_THAI_DIEM, xacNhanDiem, diemHienThi vào lib/hocba.js; VietBai.jsx ghi trangThai 'tam'; mọi chỗ hiện điểm viết đi qua diemHienThi (viết cổng grep); GocBoMe.jsx có danh sách chờ + 2 nút; duLieu.js đẩy cập nhật lên hocBaTA; firestore.rules cho update chỉ 3 trường (affectedKeys().hasOnly). KHÔNG đổi onAttempt/BKT, ghi rõ quyết định này trong chú thích. Thêm ca vào test hocba và luat_firestore (sheet 8 V5).
```

Kiểm sau khi xong: npm test; npm run test:luat (emulator); mở Góc bố mẹ xác nhận 1 bài.


### 6. V6

```
VIỆC V6 — bangTrangThai (Blackboard). Tạo lib/bangtrangthai.js thuần (dungBang, ghiLuot bất biến, tomTatChoLoiDan ≤900 ký tự không số, TRAN_BANG_KY_TU). Thay hoSoBe trong PhongNoi.jsx bằng dungBang; hoiCoGiao nhận bang (giữ chữ ký cũ tương thích); loiDan dùng tomTatChoLoiDan cho khối ABOUT THE CHILD; BaiHoc/OnLai/PhuDao đọc qua bảng. Sau khi xong, grep 'vectorS(' chỉ còn trong bangtrangthai.js. Viết test/tienganh_bangtrangthai.test.mjs (sheet 8 V6).
```

Kiểm sau khi xong: node test/tienganh_bangtrangthai.test.mjs; npm test; grep -rn 'vectorS(' src/mon/tienganh | wc -l == 1 (+ định nghĩa).


### 7. V7

```
VIỆC V7 — Kế hoạch buổi (Plan-and-Execute, planner bằng CODE). Tạo lib/kehoach.js (lapKeHoach 5–7 bước theo luật ở sheet 7 hàng V7, buocHienTai, capNhatSauLuot với hạ bậc thay→mau→tu và chèn bước phụ đạo, REPLAN_TOI_DA=2). viecTiepTheo ưu tiên bước kế hoạch; lời dặn thêm dòng THIS STEP (i/n); PhongNoi.jsx thanh bước (dùng ThanhViec.jsx) + đọc lời giới thiệu kế hoạch giọng Việt; tinhBuoi thêm điều kiện 'xong kế hoạch'. Kịch bản (buocTiepTheo) vẫn ưu tiên. Viết test/tienganh_kehoach.test.mjs và tools/mo_phong_buoi.mjs (50 bé giả, mô hình giả 40% lặp/10% ngoài vốn) in tỉ lệ daThay, phân phối nhãn, % buổi xong kế hoạch.
```

Kiểm sau khi xong: node test/tienganh_kehoach.test.mjs; node tools/mo_phong_buoi.mjs (mục tiêu: daThay <5%, xong kế hoạch ≥90%); npm test.


### 8. V8

```
VIỆC V8 — Reflexion: bài học cuối buổi + job ΔC. Tạo lib/baihoc.js (loiDanTomTat ≤1500 ký tự theo sheet 9 C1, docTomTat, soiBaiHoc với danh sách từ cấm về tính cách và chặn chữ Anh ngoài vốn/số). PhongNoi.jsx gọi 1 lượt luyenNoi cuối buổi (không chờ, lỗi thì bỏ qua và đếm) → themBaiHoc (V3). Tạo tools/doc_delta_c.mjs dùng functions/src/ara.js: dựng cặp A-R-A từ phongNoiTA + mastery (khoá quản trị), in bảng gomTheoMau; cờ --de-xuat gọi LLM 1 lần đề xuất sửa lời dặn cho mẫu kém nhất, CHỈ IN RA. Viết test/tienganh_baihoc.test.mjs (sheet 8 V8).
```

Kiểm sau khi xong: node test/tienganh_baihoc.test.mjs; npm test; node tools/doc_delta_c.mjs (cần khoá quản trị) in được bảng.


### 9. V9

```
VIỆC V9 — Phụ đạo Agentic RAG. Tạo lib/chandoan.js (cauChanDoan ≤120 ký tự tiếng Việt từ nhanNut; chamCauTinh bằng code theo maNutDs). Sửa lib/phudao.js dungPhuDao: vòng 1 nút gốc rễ #1 → chấm → thiếu → vòng 2 nút #2/bài tiên quyết → vẫn thiếu & có goiLLM → sinh → cauHoiHopLe, gắn nguon 'ai'; trần 2 vòng. Tạo functions/src/phudao.js (loiDanSinhPhuDao theo sheet 9 E1, sinhPhuDao cùng khuôn chamBaiViet, vân tay 'phudao', PHIEN_BAN_MAU.phudao=1) + callable sinhPhuDao trong functions/index.js cùng chốt cửa; lib/goiPhuDao.js là chỗ duy nhất biết mạng; câu AI hợp lệ đẩy vào choDuyetTA (viết luật Firestore: bé tạo, người lớn đọc). PhuDao.jsx hiện và đọc câu chẩn đoán. Thêm test theo sheet 8 V9 (tìm tệp đang kiểm dungPhuDao bằng grep) + test/phudao_may_chu.test.mjs.
```

Kiểm sau khi xong: npm test; npm run test:luat; mô phỏng sai 3 liền trong app xem câu chẩn đoán.


### 10. V10

```
VIỆC V10 — Parallelization. (a) functions/src/chamviet.js bước 1 chạy Promise.all([timLoi, timKhen]) rồi gộp bằng code. (b) Tạo functions/src/phanxu.js (loiDanPhanXu sheet 9 F1; phanXu chạy 2 lời gọi song song temp 0.2/0.5; đa số 2/2 mới ±1; lệch → giữ; lỗi → giữ) + callable phanXuNoi; lib/chamnoi.js thêm VUNG_MO_HO/vungMoHo; NutNoi.jsx chỉ gọi khi vungMoHo(diem) && có canhTranh, lời nhận xét vẫn từ chamnoi. Viết test/phanxu.test.mjs (sheet 8 V10).
```

Kiểm sau khi xong: node test/phanxu.test.mjs; npm test.


### 11. V11

```
VIỆC V11 — ReAct cho nhánh 'hỏi lại' lớp 3+. Tạo functions/src/tool_phongnoi.js (TOOLS tra_tu/mau_cau_cua_unit/muc_thao/nghe_lai chạy trên gói kho máy con gửi lên; chayTool cắt ≤300 ký tự; BUOC_TOI_DA=3) và hoiMayCoTool trong luyennoi.js (vòng ReAct, phát hiện lặp cùng tool+args, trả chữ trần như hoiMay). goiPhongNoi.js: khi nhan==='hoiLai' && lop>=3 gửi kho và gọi nhánh tool; câu cuối vẫn qua soiCau + vòng V1. Viết test/luyennoi_tool.test.mjs (sheet 8 V11).
```

Kiểm sau khi xong: node test/luyennoi_tool.test.mjs; npm test.


### 12. V12

```
VIỆC V12 — Xưởng sinh nội dung offline (chỉ Python, không đụng app). Tạo tools/xuong/: dieu_phoi.py (supervisor theo unit), 4 worker trả JSON theo schema của tools/sinh_bai_tienganh.py, giam_khao.py (3 lời gọi song song: vốn/mẫu · tự nhiên · hợp tuổi; ≥2 bác → loại), tranh_luan.py (chỉ cho phiếu 2–1, 2 vòng, 2 model khác nhau), duyet.md (danh sách chờ bác duyệt kèm lý do). Mọi câu qua kiểm vốn bằng hàm trong tools/chuan_tienganh.py TRƯỚC giám khảo. Đầu ra vào data/tienganh/xuong/, không ghi public/content. Thêm tools/xuong/test_schema.py. Cập nhật tools/README.md.
```

Kiểm sau khi xong: python tools/xuong/dieu_phoi.py --lop 4 --unit 1 (cần khoá); python tools/xuong/test_schema.py; sau duyệt: chạy bộ sinh + npm test.
