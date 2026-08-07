# THIẾT KẾ AGENT SẢN XUẤT VIDEO — TOÁN TƯ DUY LỚP 5 · QUYỂN 1
**MOBILUCK · VideoForge Agent v1** · Nguồn dữ liệu: km_v1_23 + 168 file DL (videoSpec tự đủ) · Ngày: 03/08/2026

---

## 1. Bài toán & tài sản sẵn có

**Mục tiêu:** biến 168 `videoSpec` (5 cảnh/micro, tổng ≈ 242 phút, trần 90s/video) thành 168 video hoàn chỉnh, qua vòng lặp: **Gemini Flash sinh code Python → agent kiểm tra → execute → tự sửa khi lỗi → người duyệt → comment → tái sinh có ngữ cảnh → đạt thì chốt.**

**Tài sản đã có (lợi thế quyết định):**
| Tài sản | Ý nghĩa cho agent |
|---|---|
| videoSpec chuẩn hóa 5 cảnh: `no, duration, templateHint, voiceover, screenText, visual, transitionOut` | Prompt sinh code KHÔNG cần suy diễn — chỉ "thi công theo bản vẽ" |
| Duration đã tính sẵn theo nhịp ≤ 2,85 từ/s | Timeline là **nguồn chân lý** — code không được tự tính lại |
| Catalog 19 template layout (dự án vertical-video trước) | Skeleton deterministic — thu hẹp không gian code Gemini phải sinh |
| Brand cố định: NAVY #0C3B70 · TEAL #1FC3A6 · GOLD #F8B942 · đỏ #C0392B; nhân vật Su Kem, Trí Long, Cáo Đề, sư phụ Trí Dũng | Đưa vào **hợp đồng code** như hằng số, không cho model tự chọn |
| TTS: **Kokoro Vietnamese** (bản cộng đồng người Việt, đã chốt) — giọng nữ ấm ~2,7 từ/s | Audio tách khỏi codegen, chạy local — xem §4.2 |

**Bài học từ dự án 113-video trước** (đã pivot từ Gemini-codegen thuần → template deterministic): codegen tự do KHÔNG hội tụ ổn định ở quy mô hàng trăm video. → Thiết kế này dùng **kiến trúc lai (hybrid)**: template library làm khung xương chịu lực, Gemini chỉ sinh phần "tùy biến theo cảnh" trong khung — vừa đúng yêu cầu vòng lặp codegen của anh, vừa kế thừa bài học cũ. (Model để dạng cấu hình `GEMINI_MODEL`, anh trỏ vào bản Flash đang dùng.)

---

## 2. Kiến trúc tổng thể

```
                    ┌──────────────────────────────────────────────────────────┐
                    │                     ORCHESTRATOR                          │
                    │        (máy trạng thái / job · SQLite jobs.db)            │
                    └──┬───────┬───────────┬───────────┬───────────┬──────────┘
                       │       │           │           │           │
   km_v1_23 + DL json  ▼       ▼           ▼           ▼           ▼
  ┌──────────┐  ┌──────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ ┌─────────────┐
  │ 1.Script │  │ 2.CodeGen│ │3.Static │ │4.Sandbox│ │ 5.Auto │ │ 6.Review UI │
  │ Extractor│→ │  Gemini  │→│Validator│→│Executor │→│   QC   │→│ (người xem) │
  └──────────┘  └────▲─────┘ └────┬────┘ └────┬────┘ └───┬────┘ └──────┬──────┘
                     │            │ lỗi AST/  │ traceback│ lệch │      │ comment
                     │            │ vi phạm   │          │ QC   │      │ có cấu trúc
                     └────────────┴───────────┴──────────┴──────┴──────┘
                              VÒNG LẶP SỬA (kèm code cũ + lỗi/comment)
                                          │ quá N lần
                                          ▼
                              7. Fallback template thuần + cờ ESCALATE
```

**Thành phần:**
1. **Extract + TTS Kokoro** — đọc `DL_*.json` → `scene_manifest`; chạy Kokoro Vietnamese sinh audio TRƯỚC, đo `audio_duration` thật bằng ffprobe ghi vào manifest (luật Đ1.1 audio-first); kiểm chéo checksum MANIFEST_Q1.
2. **CodeGen Worker** — gọi Gemini Flash với prompt 3 tầng (§4.1) — Tầng 1 SYSTEM chính là **BỘ LUẬT CODEGEN** (`rules/luat_codegen.md`, toàn văn kèm bàn giao); trả về đúng MỘT file Python.
3. **Static Validator** — chưa chạy đã lọc: parse AST, whitelist import (`matplotlib, numpy, PIL, moviepy, json, math`), cấm `os.system / subprocess / requests / open` ngoài workdir, bắt buộc tồn tại `render_scene(spec) -> ClipResult` và `SCENES == 5`.
4. **Sandbox Executor** — chạy `python job.py` trong thư mục cô lập, `timeout 300s`, không mạng, RAM cap; stdout/stderr ghi log.
5. **Auto QC** — ffprobe đối chiếu: duration từng cảnh = spec ± 0,3s, tổng = `totalDuration` ± 0,5s; độ phân giải đúng; đủ 5 cảnh; audio track khớp file TTS; sample 1 frame/cảnh kiểm màu brand xuất hiện (histogram) + chữ không tràn mép (bounding box text layer).
5b. **VISION QC — Gemini soi video** — gửi CHÍNH VIDEO mp4 + code + scene_manifest + bộ luật cho Gemini (multimodal) làm giám khảo → findings JSON đúng schema comment người (thêm loại `DE_HINH`); có BLOCK → tự mở vòng sửa (`attempts_vision` ≤ 2) TRƯỚC khi đến người.
6. **Review UI (chốt chặn cuối)** — trang web nhẹ: player + timeline 5 cảnh + form comment có cấu trúc (§5); nút **Duyệt / Yêu cầu sửa**.
7. **Fallback** — sau `MAX_ATTEMPTS = 3` lỗi máy hoặc 3 vòng người-chê: render bằng template thuần theo `templateHint` (chấp nhận "đúng nhưng mộc"), gắn cờ cho người quyết.

---

## 3. Máy trạng thái job (mỗi video một job)

```
QUEUED → CODEGEN → STATIC_CHECK ─fail→ CODEGEN (attempt+1, kèm lỗi)
                        │ pass
                        ▼
                    EXECUTING ─runtime error→ CODEGEN (kèm traceback + code cũ)
                        │ ok
                        ▼
                     AUTO_QC ─lệch spec→ CODEGEN (kèm báo cáo QC + code cũ)
                        │ pass                      ↑
                        ▼                            │
                VISION_QC ─findings BLOCK (≤2)──────┘
                        │ sạch BLOCK
                        ▼
                AWAITING_REVIEW ──"Yêu cầu sửa"──────┘ (kèm comment người + code cũ + video cũ ref)
                        │ "Duyệt"
                        ▼
                    APPROVED → xuất bản vào video_manifest.json (khóa version)
   (mọi nhánh) → attempts > MAX → FALLBACK_TEMPLATE → AWAITING_REVIEW (cờ escalate)
```

**Bảng `jobs` (SQLite):** `job_id · micro_id · version · state · attempts_machine · attempts_vision · attempts_human · model · prompt_hash · code_path · video_path · qc_report · created/updated`. Mọi version giữ vĩnh viễn: `videos/{micro_id}/v{n}/{code.py, render.mp4, prompt.txt, qc.json, vision_findings.json, comments.json, log.txt}` — tái lập 100%.

---

## 4. Hai quyết định thiết kế then chốt

### 4.1 · Prompt 3 tầng + hợp đồng code (giảm bề mặt lỗi)
- **Tầng 1 — SYSTEM (bất biến, cache):** hợp đồng kỹ thuật: canvas 1920×1080 (hoặc 1080×1920 nếu anh chốt dọc — tham số `ORIENTATION`), font hỗ trợ tiếng Việt có dấu (Be Vietnam Pro/Noto Sans, nhúng sẵn trong image Docker), 4 hằng màu brand, fps 30, API bắt buộc: `def render_scene(spec: dict) -> str  # trả path mp4 cảnh`, cấm mọi I/O ngoài `./out/`, cấm tự tính duration — đọc `spec["duration"]`.
- **Tầng 2 — TEMPLATE SKELETON:** với `templateHint` của cảnh (title_hook, concept_diagram, trap_reveal, step_by_step, mantra_card, cta_practice…), chèn code khung tương ứng từ catalog 19 mẫu — Gemini chỉ **điền phần vẽ `visual` và bố cục `screenText`** vào khung, không viết lại phần dựng clip/transition/timing.
- **Tầng 3 — SCENE DATA:** JSON 5 cảnh nguyên văn từ videoSpec.
- **Vòng sửa:** prompt = 3 tầng trên + `<PREVIOUS_CODE>` + `<ERROR hoặc QC_REPORT hoặc HUMAN_COMMENTS>` + chỉ thị "sửa tối thiểu, không refactor". Đây chính là yêu cầu "gửi lại cả code cũ và comment" của anh — làm ở cả 3 điểm hồi: static, runtime, QC, và người.

### 4.2 · Audio tách khỏi codegen (deterministic)
TTS chạy **một lần, ngoài vòng lặp**: `voiceover` → **Kokoro Vietnamese** (bản cộng đồng — model ~82M chạy local CPU/GPU, không phí API, không phụ thuộc mạng) với tham số `speed` hiệu chỉnh về ~2,7 từ/s; điểm yếu chuẩn hóa số của Kokoro đã hóa giải sẵn vì voiceover viết số thành chữ 100% → `scene_{n}.mp3` + đo duration thật. Code Gemini chỉ render **hình câm** đúng `spec.duration`; ghép audio ở bước lắp ráp chung (moviepy concat + transition theo `transitionOut`). Lợi ích: (a) giọng đồng nhất 168 video; (b) lỗi codegen không bao giờ làm hỏng audio; (c) nếu TTS đọc dài hơn duration ±0,5s → cảnh tự giãn theo audio và ghi chú QC (hiếm, vì duration đã tính theo 2,85 từ/s > tốc độ đọc thật).

---

### 4.3 · Bộ luật CodeGen — nội dung Tầng 1 SYSTEM
Toàn văn 9 chương tại **`luat_codegen_videoforge.md`** (nạp nguyên văn vào SYSTEM và làm rubric cho Vision QC), đánh số điều để feedback trích dẫn được ("vi phạm Đ3.4"). Tóm tắt: **Ch.0** ba nguyên tắc tối thượng (audio là nguồn chân lý · spec là bản vẽ · deterministic) · **Ch.I** đồng bộ âm–hình AUDIO-FIRST (hình dựng từ audio_duration thật ± 1 frame; video cảnh = audio + 0,4s PAD; transition chỉ ăn PAD; kết quả không hiện trước 30% cảnh) · **Ch.II** bố cục sạch (bbox khai báo — không giao nhau; ≤ 5 phần tử; safe 5%) · **Ch.III** chữ (nguyên văn; sàn 24px; fit-check xuống dòng → giảm cỡ → raise, không cắt chữ) · **Ch.IV** phụ đề là lớp hệ thống, code chỉ chừa trống dải đáy 15% · **Ch.V** bảng màu đóng · **Ch.VI** kỹ thuật code · **Ch.VII** self_check bắt buộc trước khi xuất · **Ch.VIII** Vision QC. **Ba tầng khóa một con số**: audio_duration thật → self_check Đ7.3 → Auto-QC ± 1 frame ⇒ khớp tuyệt đối.

## 5. Giao diện web điều khiển (Control App) & vòng người duyệt

Một web app duy nhất `control_app/` vừa **ra lệnh sản xuất** vừa **duyệt kết quả** — ba màn hình:

### 5.1 · Ba màn hình
- **A · Bảng điều khiển sản xuất** — cây 14 chương → 168 micro đọc thẳng từ km_v1_23, mỗi micro một huy hiệu trạng thái (CHƯA TẠO / ĐANG CHẠY / CHỜ DUYỆT / APPROVED / ESCALATE) + bộ lọc; tick chọn từng micro, cả bài, cả chương hoặc cả lô → nút **"Tạo video (n đã chọn)"** đẩy job vào hàng đợi. Micro đã APPROVED muốn làm lại phải bấm "Tạo lại" riêng (tránh đè nhầm bản đã chốt).
- **B · Hàng đợi & tiến độ** — thẻ job hiển thị trạng thái máy (CODEGEN → STATIC → EXECUTING → QC), thanh tiến độ, attempt thứ mấy, dòng log cuối; cập nhật realtime qua SSE; nút hủy job đang xếp hàng.
- **C · Xem & duyệt** — player + timeline 5 cảnh (bấm cảnh nhảy đúng timecode), **tab version v1/v2/v3 xem so sánh**, form comment có cấu trúc gắn theo cảnh, hai nút **DUYỆT / YÊU CẦU SỬA**. Bấm YÊU CẦU SỬA → job version +1 tự quay lại hàng đợi kèm comments.json + code cũ. Mobile-friendly để duyệt trên điện thoại.

### 5.2 · API backend (FastAPI)
| Endpoint | Chức năng |
|---|---|
| `POST /api/jobs` (micro_ids[] / lesson / chapter / "all") | Đẩy job tạo video theo lựa chọn màn A |
| `GET /api/jobs?state=` + `GET /api/jobs/stream` (SSE) | Danh sách + tiến độ realtime cho màn B |
| `DELETE /api/jobs/{job_id}` | Hủy job còn trong hàng đợi |
| `GET /api/videos/{micro_id}` | Danh sách version + url mp4 + qc.json cho màn C |
| `POST /api/videos/{micro_id}/v{n}/comments` | Ghi comments.json (schema 5.3) |
| `POST /api/videos/{micro_id}/v{n}/decision` (approve / revise) | Duyệt → khóa manifest; Sửa → enqueue version +1 |
| `GET /api/manifest` | Trả video_manifest.json cho trang học tập (giai đoạn 2) |

Màn C đọc kèm chính file DL của micro để hiện **đáp án chuẩn cạnh player** — người duyệt soi số liệu (rubric ①) không phải mở tài liệu khác.

### 5.3 · Comment có cấu trúc

Comment tự do khiến model sửa mò. Form review ép cấu trúc:

```json
{ "scene": 3, "timecode": "0:41",
  "type": "SO_SAI | CHU_TRAN | HINH_SAI_Y | SAI_MAU_BRAND | LECH_VOICEOVER | KHAC",
  "note": "Phép 78,5 − 28,26 hiển thị thành 78,5 − 28,6",
  "severity": "BLOCK | NICE_TO_HAVE" }
```
- `BLOCK` → bắt buộc vòng sửa; `NICE_TO_HAVE` gom lại, sửa nếu tiện.
- UI cho phép chấm **từng cảnh** (timeline 5 đoạn như bàn review hiện tại) — người duyệt là anh hoặc cô giáo/con gái anh xem trên mobile.
- Rubric duyệt in sẵn cạnh player: ① số liệu khớp lời giải ② chữ không tràn/không che hình ③ đúng 4 màu brand ④ hình khớp mô tả `visual` ⑤ nhịp chữ xuất hiện khớp voiceover.

---

## 6. Chống lặp vô hạn & chi phí

| Cơ chế | Ngưỡng |
|---|---|
| Vòng máy (AST/runtime/QC) | 3 lần/version → fallback template |
| Vòng Vision QC (Gemini soi video) | findings BLOCK → tự sửa ≤ 2 vòng — chặn lỗi hình trước khi phiền người |
| Vòng người | 3 version bị chê → escalate cờ đỏ, họp người quyết |
| Phát hiện dậm chân | diff code v(n) vs v(n−1) < 5% và cùng lỗi → đổi chiến lược: bơm lại từ skeleton sạch thay vì sửa tiếp |
| Ước chi phí | 168 video × ~2,2 call trung bình × prompt ~6K tokens — Flash: không đáng kể so với công người duyệt; render CPU ~1-2 phút/video → 1 máy chạy đêm xong toàn bộ đợt 1 |

**KPI vận hành:** tỉ lệ pass-QC-lần-1 (mục tiêu ≥ 70% nhờ skeleton), số vòng người trung bình (mục tiêu ≤ 1,5), video/giờ máy.

---

## 7. Cấu trúc repo & giao diện với trang học tập

```
videoforge/
├── config.yaml            # GEMINI_MODEL, ORIENTATION, MAX_ATTEMPTS, KOKORO_VOICE/speed
├── orchestrator.py        # máy trạng thái + SQLite
├── extract.py             # DL json → scene_manifest
├── codegen.py             # 3-tầng prompt + vòng sửa
├── validate_static.py     # AST + whitelist + hợp đồng
├── sandbox.py             # executor cô lập
├── qc.py                  # ffprobe + frame checks
├── vision_qc.py           # gửi mp4 + luật cho Gemini → findings JSON
├── tts.py                 # Kokoro Vietnamese local — sinh audio 1 lần/micro
├── assemble.py            # ghép cảnh + audio + transition
├── templates/             # 19 skeleton theo templateHint
├── rules/luat_codegen.md  # BỘ LUẬT — Tầng 1 SYSTEM + rubric Vision QC
├── control_app/           # FastAPI + 3 màn hình: điều khiển · hàng đợi · duyệt
└── videos/{micro_id}/v{n}/...
```
### 7.1 · Hồ sơ video — ghi ở đâu, ai ghi, khi nào
| Tầng | File | Ai ghi · khi nào | Trả lời |
|---|---|---|---|
| 1 · Hồ sơ version | `videos/{micro_id}/v{n}/meta.json` | assemble.py — ngay khi render, kể cả chưa duyệt | bản v(n) là file nào, duration thật từng cảnh, render từ spec nào |
| 2 · Sổ vận hành | `jobs.db` | orchestrator — mỗi lần đổi trạng thái | job ở đâu, mấy attempts, path |
| 3 · **SỔ CÁI** | `video_manifest.json` | control_app — đúng lúc bấm DUYỆT | **"bài này có video là cái gì"** — tra micro_id ra ngay |
| 4 · Ghi ngược km | `km_v1_24` (append-only) | builder theo lô APPROVED | node DL mang `payload.media.video` trỏ manifest |

Bản ghi manifest: `{file, srt, version, durationSec, sceneDurations[], resolution, sha256, specHash, kmVersion, approvedAt, approvedBy, status}`. **`specHash`** = sha256(videoSpec lúc render) — spec đổi sau này → hash lệch → Bảng điều khiển tự gắn huy hiệu **STALE "SPEC ĐÃ ĐỔI — cần tạo lại"**, không để video cũ âm thầm sai nội dung.

**Đầu ra cho trang học tập thích ứng (giai đoạn 2):** `video_manifest.json` — `{micro_id → {url, version, duration, sha256, approved_at}}`. Trang học chỉ cần manifest này + chính file DL (đã có đủ entryCheck/practice/assessment/BKT unit) → hai hệ ghép khít, không cần chỉnh dữ liệu.

## 8. Lộ trình thực thi

| Sprint | Nội dung | Nghiệm thu |
|---|---|---|
| S1 (2-3 ngày) | Extractor + TTS + assemble + 3 skeleton phổ biến nhất (title_hook, concept_diagram, mantra_card); render tay B49.M1 làm chuẩn vàng | 1 video mẫu anh duyệt |
| S2 | CodeGen + static validator + sandbox + vòng sửa máy; chạy pilot **B49–B52 (12 video)** | pass-QC-lần-1 ≥ 60% |
| S3 | Auto QC frame-check + Review UI + vòng comment người | anh review 12 video trên UI |
| S4 | Đủ 19 skeleton + chạy đại trà 168, fallback + báo cáo KPI | 168/168 APPROVED, video_manifest.json |

---
*Đã chốt: ② TTS = Kokoro Vietnamese (bản cộng đồng). Còn chờ anh: ① khổ ngang 1920×1080 hay dọc 1080×1920; ③ tên model Gemini điền vào config.*
