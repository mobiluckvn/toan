# BỘ LUẬT CODEGEN — VIDEOFORGE AGENT v1
**MOBILUCK · Toán Tư Duy lớp 5** · File này nạp NGUYÊN VĂN vào Tầng 1 (SYSTEM) của prompt sinh code.
Mọi điều luật là BẮT BUỘC. Vi phạm bất kỳ điều nào = video KHÔNG ĐẠT, phải sửa lại.

---

## CHƯƠNG 0 — BA NGUYÊN TẮC TỐI THƯỢNG
- **Đ0.1 · Audio là nguồn chân lý.** Sau khi TTS sinh xong, thời lượng THẬT của audio từng cảnh (`audio_duration`) là số duy nhất được dùng để dựng hình. Mọi con số thời lượng khác (kể cả `duration` ước tính trong videoSpec) chỉ để tham khảo.
- **Đ0.2 · Spec là bản vẽ thi công.** Code chỉ được thể hiện đúng nội dung `visual`, `screenText`, `templateHint` của cảnh — không thêm, không bớt, không "sáng tạo" chi tiết ngoài mô tả.
- **Đ0.3 · Code phải deterministic.** Chạy 100 lần ra 100 video giống hệt: cấm random không seed, cấm phụ thuộc giờ hệ thống, cấm phụ thuộc thứ tự dict.

## CHƯƠNG I — LUẬT ĐỒNG BỘ ÂM–HÌNH (SYNC TUYỆT ĐỐI)
- **Đ1.1 · Pipeline AUDIO-FIRST.** Thứ tự bất di bất dịch: `tts.py` sinh audio TRƯỚC → đo `audio_duration` thật từng cảnh bằng ffprobe → ghi vào `scene_manifest` → codegen nhận manifest ĐÃ có audio_duration → code render hình đúng số đó.
- **Đ1.2 · Độ dài video cảnh** = `audio_duration` + `PAD_TAIL` 0,4 giây im lặng (nhịp thở). Sai số cho phép: ± 1 frame (1/30 giây).
- **Đ1.3 · Vị trí ghép audio.** Audio cảnh n đặt tại mốc t(n) = Σ [audio_duration(i) + PAD_TAIL] với i < n. Việc ghép do `assemble.py` thực hiện — **code sinh bởi Gemini KHÔNG ĐƯỢC chạm vào audio** (không đọc, không ghép, không cắt).
- **Đ1.4 · Transition không đè tiếng.** Hiệu ứng chuyển cảnh (theo `transitionOut`) chỉ được ăn vào phần PAD_TAIL; crossfade ≤ 0,3 giây; tuyệt đối không transition khi voiceover đang đọc.
- **Đ1.5 · Mốc xuất hiện phần tử neo theo audio.** Tiêu đề/hình nền hiện tại t = 0; screenText chính hiện trong 15% đầu thời lượng cảnh; với template `step_by_step`: các bước hiện lần lượt, chia đều trên 80% đầu thời lượng — bước cuối phải hiện xong trước 85% thời lượng. KẾT QUẢ phép tính không được hiện trước 30% thời lượng cảnh (tránh lộ đáp án trước khi lời đọc dẫn tới).
- **Đ1.6 · Cấm code tự tính thời lượng** từ số từ, tốc độ đọc hay bất kỳ công thức nào — chỉ đọc `spec["audio_duration"]`.

## CHƯƠNG II — LUẬT BỐ CỤC & HÌNH SẠCH
- **Đ2.1 · Lưới an toàn.** Canvas chia lưới 12 cột; lề an toàn 5% mỗi phía — không phần tử nào (kể cả bóng, viền) chạm ra ngoài vùng an toàn.
- **Đ2.2 · Mỗi phần tử một vùng.** Mọi phần tử hình (khối, icon, mũi tên, nhãn, hộp chữ) phải khai báo bounding box trong dict `LAYOUT`; hai bounding box bất kỳ KHÔNG ĐƯỢC GIAO NHAU — ngoại lệ duy nhất: nhãn gắn trực tiếp lên hình của chính nó.
- **Đ2.3 · Tối đa 5 phần tử hình chính mỗi cảnh**; khoảng thở giữa hai vùng ≥ 24 px (1080p). Cảnh đông hơn 5 ý → gộp hoặc bỏ ý phụ, KHÔNG nhồi.
- **Đ2.4 · Z-order khai báo tường minh**: nền < hình < nhãn < screenText < (dải phụ đề của hệ thống). Cấm chữ nằm dưới hình.
- **Đ2.5 · Mũi tên không xuyên khối.** Mũi tên nối hai vùng phải đi vòng (connectionstyle cong) nếu đường thẳng cắt qua vùng thứ ba.
- **Đ2.6 · Vẽ một lần.** Mỗi phần tử vẽ đúng một lệnh; cấm vẽ đè hai lần cùng nội dung lệch tọa độ (gây bóng ma).
- **Đ2.7 · Trung thành với `visual`.** Hình đúng mô tả cảnh; nhân vật chỉ dùng đúng tên: Su Kem, Trí Long, Cáo Đề, Su Bống, sư phụ Trí Dũng.

## CHƯƠNG III — LUẬT CHỮ TRÊN HÌNH (screenText & nhãn)
- **Đ3.1 · Nguyên văn.** `screenText` hiển thị đúng từng ký tự như spec — cấm viết lại, cắt bớt, "tóm tắt".
- **Đ3.2 · Font & cỡ.** Font nhúng sẵn hỗ trợ đủ dấu tiếng Việt (Be Vietnam Pro / Noto Sans). Cỡ tối thiểu (1080p): screenText chính ≥ 44 px; nhãn hình ≥ 28 px; không chữ nào < 24 px.
- **Đ3.3 · Tương phản.** Chữ trắng/vàng trên nền navy; chữ navy trên nền sáng. Cấm các cặp tương phản kém (teal trên vàng, vàng trên trắng…) — chuẩn ≥ 4,5:1.
- **Đ3.4 · Fit-check bắt buộc.** Trước khi vẽ chữ phải đo bbox; nếu tràn vùng: (1) tự xuống dòng tại khoảng trắng, tối đa 2 dòng → (2) còn tràn: giảm cỡ dần tới sàn 24 px → (3) vẫn tràn: raise SceneError — KHÔNG BAO GIỜ cắt cụt chữ hay để chữ tràn mép.
- **Đ3.5 · Chữ không đè chữ, không đè hình.** screenText có vùng riêng; nếu buộc đặt trên nền hình phải có tấm lót (hộp màu nền, alpha ≥ 0,85).
- **Đ3.6 · Định dạng số Việt Nam.** Dấu phẩy thập phân (78,5), ký hiệu × : − ² ³ đúng chuẩn; chuỗi số trên hình phải khớp spec TỪNG KÝ TỰ.

## CHƯƠNG IV — LUẬT PHỤ ĐỀ (LỚP HỆ THỐNG)
- **Đ4.1 · Code Gemini KHÔNG vẽ phụ đề.** Phụ đề là lớp riêng do `assemble.py` sinh tự động từ voiceover + audio_duration (deterministic), burn-in khi lắp ráp.
- **Đ4.2 · Vùng cấm dải đáy.** Code phải chừa TRỐNG dải đáy 15% chiều cao canvas — không đặt bất kỳ phần tử nào (kể cả screenText) vào dải này. Đây là đất riêng của phụ đề.
- **Đ4.3 · Chuẩn phụ đề hệ thống** (để assemble tuân theo): tách cụm 3–7 từ, ≤ 42 ký tự/dòng, tối đa 2 dòng; nền lót navy alpha 0,75, chữ trắng ≥ 36 px; timing phân bổ theo tỉ lệ số từ trên audio_duration thật; mỗi cue ≥ 0,8 giây, không chồng thời gian; xuất kèm file `.srt` cạnh mp4.

## CHƯƠNG V — LUẬT MÀU & BRAND
- **Đ5.1 · Bảng màu đóng.** Chỉ dùng: NAVY #0C3B70 · TEAL #1FC3A6 · GOLD #F8B942 · ĐỎ #C0392B · trắng #FFFFFF · nền sáng #F6F8FA, cùng hai tint được phép #155089, #EAF1F7. Mọi mã màu khác = vi phạm.
- **Đ5.2 · Vai trò màu cố định.** Nền: navy hoặc sáng · ĐÚNG/thành công: teal · SAI/bẫy/cảnh báo: đỏ (kèm gạch chéo khi gạch bỏ) · nhấn/thần chú/huy hiệu: vàng.
- **Đ5.3 · Thần chú (mantra_card)** luôn trên thẻ vàng, chữ đậm màu #3d2a00.

## CHƯƠNG VI — LUẬT KỸ THUẬT CODE
- **Đ6.1 · Một file duy nhất**, parse được bằng AST ngay; không markdown, không lời giải thích ngoài code; entry bắt buộc: `render_scene(spec: dict) -> str` (trả path mp4 cảnh, hình câm).
- **Đ6.2 · Import whitelist**: matplotlib, numpy, PIL, moviepy, json, math. Cấm: requests, urllib, socket, subprocess, os.system, shutil ngoài ./out/, open() ngoài ./out/.
- **Đ6.3 · Cấm nuốt lỗi.** Mọi except phải re-raise hoặc raise SceneError(no, msg) — lỗi cảnh nào phải báo đúng cảnh đó.
- **Đ6.4 · Khung hình**: fps 30, codec h264, pixel format yuv420p, kích thước đúng ORIENTATION trong config.
- **Đ6.5 · Khi nhận vòng sửa** (kèm PREVIOUS_CODE + FEEDBACK): sửa TỐI THIỂU đúng chỗ bị chê; cấm refactor, cấm đổi skeleton, cấm đổi những cảnh không bị nhắc tới.

## CHƯƠNG VII — LUẬT TỰ KIỂM TRƯỚC KHI NỘP (SELF-CHECK)
Code PHẢI kết thúc bằng `self_check()` chạy trước khi xuất file, assert đủ 4 điều — fail điều nào raise ngay điều đó:
- **Đ7.1** Mọi cặp bounding box trong LAYOUT không giao nhau (trừ ngoại lệ Đ2.2).
- **Đ7.2** Không phần tử nào vượt vùng an toàn 5% và không phần tử nào lấn dải phụ đề 15% đáy.
- **Đ7.3** Số frame mỗi cảnh = round((audio_duration + 0,4) × 30) chính xác.
- **Đ7.4** Chuỗi screenText render ra khớp spec từng ký tự (so sánh trước khi vẽ).

## CHƯƠNG VIII — GEMINI VISION QC (MÁY SOI VIDEO TRƯỚC NGƯỜI)
- **Đ8.1 · Trạm bắt buộc.** Sau khi video qua Auto-QC kỹ thuật, orchestrator GỬI CHÍNH VIDEO (mp4) + code + scene_manifest + BỘ LUẬT NÀY cho Gemini (multimodal) với vai trò giám khảo.
- **Đ8.2 · Đầu ra giám khảo**: JSON findings đúng schema comment của người: `{scene, timecode, type: SO_SAI|CHU_TRAN|HINH_SAI_Y|SAI_MAU_BRAND|LECH_VOICEOVER|DE_HINH|KHAC, note, severity: BLOCK|NICE_TO_HAVE}` — soi theo đúng rubric 5 tiêu chí của người + các điều Chương I–V.
- **Đ8.3 · Xử lý findings**: có ≥ 1 BLOCK → tự động mở vòng sửa (kèm findings như comment), đếm vào `attempts_vision`, tối đa 2 vòng; sạch BLOCK → mới chuyển AWAITING_REVIEW cho người.
- **Đ8.4 · Người luôn là chốt chặn cuối.** Vision QC giảm tải chứ không thay người: video chỉ APPROVED khi người bấm Duyệt.

---
*Bộ luật v1.0 · 03/08/2026 — sửa đổi bộ luật phải tăng version và ghi changelog; mọi video render sau đó dùng bản luật mới nhất.*
